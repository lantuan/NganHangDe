"""Bốn lỗi chat cô Lan báo 22/10/2026 (lần 2):

1. Hỏi toán ngay trong chat bị CHV_Fun từ chối -> máy chủ nhận câu hỏi toán (la_cau_hoi_toan) và mở bảng chọn câu
   của đề trong hội thoại, gửi CHÍNH câu học sinh đã gõ cho thầy/cô AI; chưa có đề thì nói rõ cách hỏi bài.
2. Câu trả lời của gia sư trong chat không có ô hỏi tiếp -> mỗi câu trả lời có ô nhập riêng (gửi kèm lich_su), mở lại
   hội thoại vẫn còn (máy chủ lưu "hoi": de_id + so_thu_tu).
3. Tạo đề trong chat thì liên kết "Lời giải của đề này" hiện luôn -> chỉ hiện sau khi bấm "Mình làm xong rồi".
4. Tick "Kèm bản tiếng Anh" mà chat qua n8n chỉ đưa PDF tiếng Việt -> liên kết /api/exam/tai-de/<id>?ngon_ngu=ca-hai
   (.zip Việt + Anh) và ghi rõ mức luyện tập / tiếng Anh đã áp dụng.
"""
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat as C
from app.routers import exam as E
from app.routers import gia_su as G
from app.services import gia_su_service as GS
from app.services import i18n_service as I
from app.services import tuy_chon_de_service as T

GOC = Path(__file__).resolve().parent.parent
HTML = (GOC / "app/templates/chat/chat.html").read_text(encoding="utf-8")
DE_ID = "11111111-2222-3333-4444-555555555555"


class _U:
    id = "99999999-9999-9999-9999-999999999999"


@pytest.fixture
def chat_gia(monkeypatch, tmp_path):
    monkeypatch.setattr(T, "TEP", tmp_path / "tuy_chon.json")
    monkeypatch.setattr(C, "get_current_user", lambda request: _U)
    monkeypatch.setattr(C.profile_service, "lay_vai_tro", lambda uid: "hoc_sinh")
    luu = []
    monkeypatch.setattr(C.history_service, "luu_tin_nhan", lambda **kw: luu.append(kw))
    monkeypatch.setattr(C, "DOWNLOAD_DIR", tmp_path)
    return luu


class _PhanHoiPdf:
    status_code = 200
    headers = {"content-type": "application/pdf"}
    content = b"%PDF-1.4 de"
    text = ""


def _goi_tao_de(monkeypatch, co_anh: bool, chi_yccd: bool, tick_anh: str, lang="vi"):
    de = {"id": DE_ID, "role": "student", "files": {"tex": "x.tex"}, "blueprint": {"chi_yccd": chi_yccd}}
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: de)
    monkeypatch.setattr(E, "_de_co_ban_tieng_anh", lambda d: co_anh)
    monkeypatch.setattr(C, "_goi_n8n", lambda *a, **k: _PhanHoiPdf())
    return TestClient(app).post("/chat", data={"message": "cho tôi đề lớp 10 chương 2", "conversation_id": "h-anh",
                                               "kem_tieng_anh": tick_anh, "chi_yccd": "1" if chi_yccd else "0"},
                                cookies={"lang": lang}).json()


# ---------------------------------------------------------------- 4
def test_n8n_tick_anh_ra_lien_ket_zip_viet_anh(monkeypatch, chat_gia):
    kq = _goi_tao_de(monkeypatch, co_anh=True, chi_yccd=True, tick_anh="1")
    assert kq["data"]["type"] == "file"
    assert kq["data"]["url"] == "/api/exam/tai-de/%s?ngon_ngu=ca-hai" % DE_ID      # không còn PDF tiếng Việt tĩnh
    assert kq["data"]["filename"] == "de_thi.zip" and kq["data"]["de_id"] == DE_ID
    assert "Đúng chương trình" in kq["message"] and ".zip" in kq["message"]
    assert chat_gia[-1]["duong_dan_file"] == kq["data"]["url"]                        # mở lại hội thoại vẫn đúng


def test_n8n_khong_tick_anh_va_nang_cao(monkeypatch, chat_gia):
    kq = _goi_tao_de(monkeypatch, co_anh=False, chi_yccd=False, tick_anh="0")
    assert kq["data"]["url"] == "/api/exam/tai-de/%s" % DE_ID and kq["data"]["filename"] == "de_thi.pdf"
    assert "Nâng cao thêm" in kq["message"] and "tiếng Anh" not in kq["message"]


def test_n8n_tick_anh_ma_chuong_chua_dich_thi_noi_ro(monkeypatch, chat_gia):
    kq = _goi_tao_de(monkeypatch, co_anh=False, chi_yccd=True, tick_anh="1")
    assert "chưa có bản tiếng Anh" in kq["message"]
    en = _goi_tao_de(monkeypatch, co_anh=True, chi_yccd=True, tick_anh="1", lang="en")
    assert "English version included" in en["message"] and "Standard curriculum" in en["message"]


def test_de_gan_nhat_tra_lien_ket_va_lua_chon(monkeypatch):
    monkeypatch.setattr(E.history_service, "lay_de_gan_nhat", lambda cid: {
        "id": DE_ID, "role": "student", "files": {}, "blueprint": {"chi_yccd": True}})
    monkeypatch.setattr(E, "_de_co_ban_tieng_anh", lambda d: True)
    kq = TestClient(app).get("/api/exam/de-gan-nhat", params={"conversation_id": "h"}).json()
    assert kq["url_tai"].endswith("?ngon_ngu=ca-hai") and kq["co_ban_tieng_anh"] is True and kq["chi_yccd"] is True


def test_form_nhanh_va_khung_xac_nhan_dung_lien_ket_co_ban_anh():
    assert HTML.count('url = (thongTinDe && thongTinDe.url_tai) || ("/api/exam/tai-de/" + deId);') == 2
    assert HTML.count('const aiCaption = "Đã tạo đề xong. " + dongTuyChonDe(thongTinDe);') == 2


# ---------------------------------------------------------------- 3
def test_tao_de_khong_kem_lien_ket_loi_giai():
    gui = HTML.split("async function sendMessage(text)", 1)[1].split("// ===== SỰ KIỆN FORM", 1)[0]
    khoi_file = gui.split('data.data.type === "file"', 1)[1].split("} else if (data.reply)", 1)[0]
    assert "htmlNutLoiGiai" not in khoi_file and "tai-loigiai" not in khoi_file
    # Chỉ còn nút hai bước: làm trên giấy xong tự bấm mới hiện liên kết
    nut = HTML.split("function htmlNutLoiGiai(url)", 1)[1].split("function hienLoiGiai", 1)[0]
    assert "tai-loigiai" not in nut and "hienLoiGiai(this," in nut
    lam_bai = HTML.split("function chonLamBai(", 1)[1].split("function doiYeuCauDe", 1)[0]
    assert 'htmlNutLoiGiai("/api/exam/tai-de/" + deId)' in lam_bai


# ---------------------------------------------------------------- 1
@pytest.mark.parametrize("cau", ["câu 3 sao ra 5 vậy", "chứng minh chỗ này thế nào", "cos 60 bằng bao nhiêu",
                                 "tại sao lại ra D vậy", "giảng lại câu 2, lời giải khó hiểu quá"])
def test_nhan_ra_cau_hoi_toan(cau):
    assert GS.la_cau_hoi_toan(cau) is True


@pytest.mark.parametrize("cau", ["cho tôi đề lớp 10 chương 2", "tạo đề lớp 10 chương 1 có hướng dẫn giải",
                                 "cho tôi lời giải", "kiểm tra miệng chương 2", "đề giữa kỳ 1", "làm đề khác",
                                 "hướng dẫn sử dụng web", "học sinh lớp 10", "xin chào", "cho tôi 1 đề phương trình", ""])
def test_khong_cuop_yeu_cau_tao_de(cau):
    assert GS.la_cau_hoi_toan(cau) is False


def _khong_goi_n8n(*a, **k):
    raise AssertionError("câu hỏi toán không được đẩy xuống n8n")


def test_hoi_toan_chua_co_de_thi_huong_dan(monkeypatch, chat_gia):
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: None)
    monkeypatch.setattr(C, "_goi_n8n", _khong_goi_n8n)
    c = TestClient(app)
    vi = c.post("/chat", data={"message": "cos 60 bằng bao nhiêu", "conversation_id": "h"}).json()
    assert vi["success"] and vi["data"]["type"] == "huong_dan_hoi_bai" and "nộp" in vi["message"]
    en = c.post("/chat", data={"message": "cos 60 bằng bao nhiêu", "conversation_id": "h"}, cookies={"lang": "en"}).json()
    assert not I.CO_DAU.search(en["message"])


@pytest.mark.parametrize("da_nop, mo_dau", [(True, "Bạn hỏi về câu nào"), (False, "Bạn chưa nộp bài")])
def test_hoi_toan_co_de_mo_bang_chon_cau_kem_cau_da_go(monkeypatch, chat_gia, da_nop, mo_dau):
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: {"id": DE_ID})
    monkeypatch.setattr(C.gia_su_service, "co_de_da_nop_bai", lambda uid, cid: da_nop)
    monkeypatch.setattr(C, "_goi_n8n", _khong_goi_n8n)
    kq = TestClient(app).post("/chat", data={"message": "câu 3 sao ra 5 vậy", "conversation_id": "h"}).json()
    assert kq["data"]["type"] == "mo_bang_gia_su" and kq["data"]["cau_hoi_goc"] == "câu 3 sao ra 5 vậy"
    assert kq["message"].startswith(mo_dau)


def test_bam_cau_gui_chinh_cau_da_go():
    assert "CAU_HOI_CHO = data.data.cau_hoi_goc || null;" in HTML
    hoi = HTML.split("async function hoiCauTrongDeCu(soThuTu)", 1)[1].split("const messages =", 1)[0]
    assert "cau_hoi: cauHoiGui," in hoi and "CAU_HOI_CHO = null;" in hoi


# ---------------------------------------------------------------- 2
def test_cau_tra_loi_gia_su_co_o_hoi_tiep():
    ve = HTML.split("function htmlTraLoiGiaSu(data, hoi, cauHoiDau)", 1)[1].split("function htmlHoiTiep", 1)[0]
    assert "htmlHoiTiep(hoi || data.hoi, cauHoiDau, d.tra_loi)" in ve
    gui = HTML.split("async function guiHoiTiep(id)", 1)[1].split("let CAU_HOI_CHO", 1)[0]
    assert "lich_su: tt.lich_su.slice(-6)" in gui and "conversation_id: conversationId" in gui
    assert "event.isComposing" in HTML.split("function htmlHoiTiep", 1)[1].split("async function guiHoiTiep", 1)[0]


def test_luu_ngu_canh_cau_de_ve_lai_o_hoi_tiep(monkeypatch):
    luu = []
    monkeypatch.setattr(G, "get_current_user", lambda request: _U)
    monkeypatch.setattr(G.gia_su_service, "hoi", lambda **kw: {"tra_loi": "Bước 1 ...", "dap_an_python": "A"})
    monkeypatch.setattr(G.history_service, "luu_tin_nhan", lambda **kw: luu.append(kw))
    TestClient(app).post("/api/giasu/hoi", json={"de_id": DE_ID, "so_thu_tu": 13, "cau_hoi": "vì sao ra 5",
                                                 "conversation_id": "h", "cau_hien_thi": "PHẦN III câu 1: vì sao ra 5",
                                                 "nhan_cau": "PHẦN III câu 1"})
    goi = json.loads(luu[1]["noi_dung"])
    assert goi["hoi"] == {"de_id": DE_ID, "so_thu_tu": 13, "nhan": "PHẦN III câu 1"}
    assert goi["data"]["tra_loi"] == "Bước 1 ..."


def test_ban_dich_moi_khong_pha_js():
    td = json.loads((GOC / "data/i18n/en_ui.json").read_text(encoding="utf-8"))
    for k in ("📖 Mình làm xong rồi, xem lời giải", "💬 Còn chỗ nào chưa hiểu ở câu này thì hỏi tiếp ngay ở đây."):
        assert k in td and not re.search(r"['\"`<>{}$]", td[k])
