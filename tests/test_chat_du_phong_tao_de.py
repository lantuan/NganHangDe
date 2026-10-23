"""n8n hỏng mà yêu cầu tạo đề rõ ràng -> máy chủ tự đọc, hiện khung xác nhận (cô Lan 22/10/2026: gõ "Lớp 10, thi giữa
kỳ 1" thì chat báo "AI chưa xử lý được yêu cầu này"). Xem app/services/yeu_cau_de_service.py."""
import pytest
import requests
from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat as C
from app.services import i18n_service as I
from app.services.yeu_cau_de_service import doc_yeu_cau_de


class _U:
    id = "99999999-9999-9999-9999-999999999999"


@pytest.mark.parametrize("cau, mong", [
    ("Lớp 10, thi giữa kỳ 1", (10, "HeSo2_HeSo3", "giua_ky_1", None)),
    ("lớp 10 giữa học kì 2", (10, "HeSo2_HeSo3", "giua_ky_2", None)),
    ("đề cuối kì II lớp 11", (11, "HeSo2_HeSo3", "cuoi_ky_2", None)),
    ("học kỳ 1 toán 12", (12, "HeSo2_HeSo3", "cuoi_ky_1", None)),
    ("cho tôi đề lớp 10 chương 2", (10, "HeSo1", "kiem_tra_thuong_xuyen", "chuong_2")),
    ("kiểm tra 15 phút chương 3 lớp 10", (10, "HeSo1", "kiem_tra_thuong_xuyen", "chuong_3")),
])
def test_doc_yeu_cau_ro_rang(cau, mong):
    d = doc_yeu_cau_de(cau)
    assert (d["lop"], d["loai_he_so"], d["ki_thi"], d["pham_vi_chuong"]) == mong
    assert d["type"] == "xac_nhan_de" and d["cau_truc_tong_quat"] is None      # cấu trúc mặc định, không đoán số câu
    assert "mặc định" in d["tra_loi"]


@pytest.mark.parametrize("cau", ["giữa kỳ 1", "tạo đề lớp 10", "xin chào", "chương 2", ""])
def test_thieu_lop_hoac_ky_thi_thi_khong_doan(cau):
    assert doc_yeu_cau_de(cau) is None


def test_ban_tieng_anh_tron_ven():
    assert not I.CO_DAU.search(doc_yeu_cau_de("Lớp 10, thi giữa kỳ 1", "en")["tra_loi"])


class _JsonHong:
    status_code = 200
    headers = {"content-type": "application/json"}
    text = ""

    def json(self):
        raise ValueError("rong")


@pytest.fixture
def chat_gia(monkeypatch, tmp_path):
    from app.services import tuy_chon_de_service as T
    monkeypatch.setattr(T, "TEP", tmp_path / "tc.json")
    monkeypatch.setattr(C, "get_current_user", lambda request: _U)
    monkeypatch.setattr(C.profile_service, "lay_vai_tro", lambda uid: "hoc_sinh")
    luu = []
    monkeypatch.setattr(C.history_service, "luu_tin_nhan", lambda **kw: luu.append(kw))
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: None)
    return luu


def _gui(cau):
    return TestClient(app).post("/chat", data={"message": cau, "conversation_id": "h"}).json()


def test_n8n_tra_json_rong_van_ra_khung_xac_nhan(monkeypatch, chat_gia):
    monkeypatch.setattr(C, "_goi_n8n", lambda *a, **k: _JsonHong())
    kq = _gui("Lớp 10, thi giữa kỳ 1")
    assert kq["success"] and kq["data"]["type"] == "xac_nhan_de" and kq["data"]["lop"] == 10
    assert kq["data"]["ki_thi"] == "giua_ky_1" and chat_gia[-1]["noi_dung"] == kq["message"]


def test_n8n_mat_ket_noi_van_ra_khung_xac_nhan(monkeypatch, chat_gia):
    def _hong(*a, **k):
        raise requests.exceptions.ConnectionError("x")
    monkeypatch.setattr(C, "_goi_n8n", _hong)
    assert _gui("cho tôi đề lớp 10 chương 2")["data"]["pham_vi_chuong"] == "chuong_2"


def test_khong_doc_duoc_thi_bao_loi_nhu_cu(monkeypatch, chat_gia):
    monkeypatch.setattr(C, "_goi_n8n", lambda *a, **k: _JsonHong())
    kq = _gui("làm cái gì đó")
    assert kq["success"] is False and "AI chưa xử lý được" in kq["message"]


# ---------------------------------------------------------------- 23/10/2026
def test_khong_noi_lop_thi_lay_lop_trong_ho_so_va_chi_tu_luan():
    """Cô Lan: "tôi cần đề chuyện tập thêm chương 3, phần tự luận" (không nói lớp; hồ sơ Khối 10)."""
    cau = "tôi cần đề chuyện tập thêm chương 3, phần tự luận"
    assert doc_yeu_cau_de(cau) is None                                       # không hồ sơ: không đoán lớp
    d = doc_yeu_cau_de(cau, "vi", 10)
    assert (d["lop"], d["pham_vi_chuong"]) == (10, "chuong_3")
    assert d["cau_truc_tong_quat"] == {"trac_nghiem": 0, "dung_sai_cau_lon": 0, "tra_loi_ngan": 0, "tu_luan": 3}


def test_so_cau_tung_loai():
    d = doc_yeu_cau_de("đề chương 2 lớp 10, 5 câu tự luận, 10 câu trắc nghiệm")
    assert d["cau_truc_tong_quat"] == {"trac_nghiem": 10, "dung_sai_cau_lon": 1, "tra_loi_ngan": 2, "tu_luan": 5}


def test_hoi_cach_dung_khi_n8n_hong(monkeypatch, chat_gia):
    monkeypatch.setattr(C, "_goi_n8n", lambda *a, **k: _JsonHong())
    monkeypatch.setattr(C.supabase_service, "lay_lop_hoc_sinh", lambda uid: {"khoi": "10", "lop": "C9"})
    kq = _gui("tôi không biết cách tạo đề")
    assert kq["success"] and kq["data"]["type"] == "huong_dan" and "Tạo đề mới" in kq["message"]
    kq = _gui("tôi cần đề chuyện tập thêm chương 3, phần tự luận")
    assert kq["data"]["type"] == "xac_nhan_de" and kq["data"]["cau_truc_tong_quat"]["tu_luan"] == 3


def test_giao_dien_gui_ca_so_0():
    from pathlib import Path
    html = (Path(__file__).resolve().parent.parent / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert 'if (typeof ct[loai] === "number" && ct[loai] >= 0) cauTrucTuHocSinh[loai] = { so_luong: ct[loai] };' in html
    assert "if (ct.trac_nghiem) cauTrucTuHocSinh" not in html
