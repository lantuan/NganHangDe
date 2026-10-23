"""Khung chat trò chuyện bình thường + hỏi kiến thức theo tài liệu lí thuyết (cô Lan 23/10/2026): "tôi cần chat được bình
thường như chatbox bình thường khác... nếu hỏi về kiến thức toán thì AI có thể đọc ngay phần lý thuyết có sẵn để trả
lời, chỉ trả lời trong đó". Xem app/services/tro_chuyen_service.py."""
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat as C
from app.services import gia_su_service as GS
from app.services import tro_chuyen_service as T


@pytest.mark.parametrize("cau", ["tập rỗng là gì", "phương sai là gì", "định lý sin", "công thức tính diện tích tam giác",
                                 "thế nào là hai vectơ cùng phương", "what is the empty set"])
def test_nhan_ra_cau_hoi_kien_thuc(cau):
    assert T.la_cau_hoi_kien_thuc(cau)


@pytest.mark.parametrize("cau", ["cho tôi đề lớp 10 chương 2", "câu 3 công thức là gì", "giảng lại câu 2", "xin chào",
                                 "bạn biết tôi là ai không", "cho tôi lời giải", "tôi muốn đi chơi không học vẫn giỏi"])
def test_khong_nham(cau):
    assert not T.la_cau_hoi_kien_thuc(cau)


@pytest.fixture
def mo_hinh(monkeypatch):
    goi = []
    monkeypatch.setattr(GS, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(GS, "_goi_mo_hinh", lambda p: goi.append(p) or "Tập rỗng là tập hợp không chứa phần tử nào.")
    return goi


def test_tra_loi_kien_thuc_chi_theo_tai_lieu(mo_hinh):
    kq = T.tra_loi_kien_thuc("tập rỗng là gì", 10)
    assert kq and kq["ly_thuyet"][0]["ma_bai"] == "L10_C1_B2"
    lenh = mo_hinh[0]["lenh_he_thong"]
    assert "CHỈ trả lời bằng nội dung trong TÀI LIỆU LÍ THUYẾT" in lenh and "không chứa phần tử nào" in lenh
    assert "KHÔNG tự tính toán" in lenh and mo_hinh[0]["cau_hoi"] == "tập rỗng là gì"
    en = T.tra_loi_kien_thuc("tập rỗng là gì", 10, "en")
    assert en and "THEORY NOTES" in mo_hinh[1]["lenh_he_thong"]


def test_khong_co_tai_lieu_thi_khong_goi_mo_hinh(mo_hinh):
    assert T.tra_loi_kien_thuc("xyz là gì", 10) is None and mo_hinh == []


def test_tro_chuyen_huong_ve_toan(mo_hinh):
    assert T.tro_chuyen("bạn biết tôi là ai không", [("user", "chào"), ("assistant", "chào bạn")])
    lenh = mo_hinh[0]["lenh_he_thong"]
    assert "ngoài Toán" in lenh and "KHÔNG giải bài toán" in lenh and "Người dùng: chào" in lenh


def test_chua_cau_hinh_thi_none(monkeypatch):
    monkeypatch.setattr(GS, "N8N_WEBHOOK_GIA_SU", "")
    assert T.tro_chuyen("hi") is None and T.tra_loi_kien_thuc("tập rỗng là gì", 10) is None


class _U:
    id = "99999999-9999-9999-9999-999999999999"


class _JsonHong:
    status_code = 200
    headers = {"content-type": "application/json"}
    text = ""

    def json(self):
        raise ValueError("rong")


@pytest.fixture
def chat_gia(monkeypatch, tmp_path, mo_hinh):
    from app.services import tuy_chon_de_service as TC
    monkeypatch.setattr(TC, "TEP", tmp_path / "tc.json")
    monkeypatch.setattr(C, "get_current_user", lambda request: _U)
    monkeypatch.setattr(C.profile_service, "lay_vai_tro", lambda uid: "hoc_sinh")
    monkeypatch.setattr(C.supabase_service, "lay_lop_hoc_sinh", lambda uid: {"khoi": "10", "lop": "C9"})
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: None)
    monkeypatch.setattr(C.history_service, "lay_tin_nhan_hoi_thoai", lambda uid, cid: [])
    luu = []
    monkeypatch.setattr(C.history_service, "luu_tin_nhan", lambda **kw: luu.append(kw))
    return luu


def _gui(cau):
    return TestClient(app).post("/chat", data={"message": cau, "conversation_id": "h"}).json()


def test_chat_hoi_kien_thuc_khong_qua_n8n(monkeypatch, chat_gia, mo_hinh):
    def _khong(*a, **k):
        raise AssertionError("không được gọi n8n")
    monkeypatch.setattr(C, "_goi_n8n", _khong)
    kq = _gui("tập rỗng là gì")
    assert kq["data"]["type"] == "kien_thuc" and kq["data"]["ly_thuyet"]
    assert chat_gia[-1]["loai_phan_hoi"] == "gia_su"
    assert json.loads(chat_gia[-1]["noi_dung"])["data"]["ly_thuyet"]          # mở lại hội thoại vẫn có khung tài liệu


def test_n8n_hong_van_tro_chuyen_duoc(monkeypatch, chat_gia, mo_hinh):
    monkeypatch.setattr(C, "_goi_n8n", lambda *a, **k: _JsonHong())
    kq = _gui("bạn biết tôi là ai không")
    assert kq["success"] and kq["data"]["type"] == "tro_chuyen" and kq["message"]


def test_giao_dien_ve_cau_tra_loi_kien_thuc():
    from pathlib import Path
    html = (Path(__file__).resolve().parent.parent / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert 'data.data.type === "kien_thuc"' in html
