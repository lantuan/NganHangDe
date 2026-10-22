"""Năm lỗi cô Lan báo 22/10/2026 ở trang Chat AI (ảnh chụp):
1. "Có lúc xuất đề ra cả lời giải": n8n trả về tệp LỜI GIẢI của đề gần nhất mà máy chủ vẫn chào "Xong đề rồi đó!".
2. "Ra đáp án chưa đẩy lên được class": lí do không đăng được lên Classroom chỉ nằm ở console trình duyệt.
3. "Ấn Hỏi lại đề cũ không ra ô hỏi trực tiếp câu đó": bảng chọn câu nằm dưới ô nhập, bị đẩy ra ngoài khung nhìn.
4. Trang tiếng Anh, hỏi tiếng Việt thì câu trả lời lẫn Anh - Việt; chữ cuối ("quả") rớt lại trong ô chat (bộ gõ).
5. Đổi Tiếng Việt / English thì mất cuộc chat (phần hỏi gia sư không được lưu, địa chỉ trang không có ?cid=).
"""
import json
import types
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat as C
from app.routers import gia_su as G
from app.services import i18n_service as I

GOC = Path(__file__).resolve().parent.parent
U = types.SimpleNamespace(id="u1", email="gv@x")


# ---------------------------------------------------------------- 1
def test_nhan_ra_tep_loi_giai_cua_de_gan_nhat(monkeypatch, tmp_path):
    lg = tmp_path / "lg.pdf"
    lg.write_bytes(b"%PDF loi giai")
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: {"id": "d1", "files": {"loigiai": str(lg)}})
    assert C._la_tep_loi_giai_de_gan_nhat(b"%PDF loi giai", "h1") is True
    assert C._la_tep_loi_giai_de_gan_nhat(b"%PDF de thi", "h1") is False
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: None)
    assert C._la_tep_loi_giai_de_gan_nhat(b"%PDF loi giai", "h1") is False


# ---------------------------------------------------------------- 2
@pytest.mark.parametrize("la_gv", [True, False])
def test_dang_classroom_tra_kem_vai_tro(monkeypatch, la_gv):
    monkeypatch.setattr(C, "get_current_user", lambda request: U)
    monkeypatch.setattr(C.supabase_service, "lay_lop_hoc_sinh", lambda uid: {"khoi": "10", "lop": "C9"})
    monkeypatch.setattr(C.profile_service, "la_giao_vien", lambda uid: la_gv)
    monkeypatch.setattr(C.classroom_service, "dang_ket_qua_len_classroom",
                        lambda **kw: {"success": False, "message": "Không tạo được bài đăng trên Classroom."})
    r = TestClient(app).post("/api/chat/dang-classroom", json={"de_id": "d1", "diem_html": "", "diem_so": 1,
                                                                "diem_toi_da": 10}).json()
    assert r["success"] is False and r["la_giao_vien"] is la_gv and r["message"]
    html = (GOC / "app/templates/chat/lam_bai.html").read_text(encoding="utf-8")
    assert "if (data && data.la_giao_vien)" in html


# ---------------------------------------------------------------- 3, 4b, 5 (giao diện)
def test_trang_chat():
    html = (GOC / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert "if (e.isComposing || e.keyCode === 229) return;" in html          # bộ gõ tiếng Việt
    assert "function layBangHoiDeCu()" in html and "messages.appendChild(bang)" in html
    assert 'id="bang-hoi-de-cu" style="display:none;" class="mt-3"' not in html  # không còn dưới ô nhập
    assert 'msg.loai_phan_hoi === "gia_su"' in html and "function htmlTraLoiGiaSu(data, hoi, cauHoiDau)" in html
    assert "conversation_id: conversationId," in html and "function ganCidVaoUrl(cid)" in html
    assert html.count("ganCidVaoUrl(conversationId);") >= 4


# ---------------------------------------------------------------- 4a
def test_json_khong_dich_nua_voi():
    cau = "Bạn muốn hỏi bài trong đề vừa làm đúng không? Bấm vào câu nào chưa hiểu bên dưới, thầy/cô AI giảng lại ngay nhé."
    kq = I.dich_json({"message": cau}, "en")["message"]
    assert kq == cau or not I.CO_DAU.search(kq), kq                           # hoặc Anh trọn vẹn, hoặc giữ tiếng Việt
    assert I.dich_json({"message": "Có lỗi xảy ra."}, "en")["message"] == "An error occurred."


def test_cau_mo_bang_gia_su_theo_ngon_ngu(monkeypatch):
    monkeypatch.setattr(C, "get_current_user", lambda request: U)
    monkeypatch.setattr(C.profile_service, "lay_vai_tro", lambda uid: "hoc_sinh")
    monkeypatch.setattr(C.history_service, "luu_tin_nhan", lambda **kw: None)
    monkeypatch.setattr(C.gia_su_service, "la_cau_hoi_toan", lambda m: True)
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: {"id": "d1"})
    monkeypatch.setattr(C.gia_su_service, "co_de_da_nop_bai", lambda uid, cid: True)
    c = TestClient(app)
    en = c.post("/chat", data={"message": "tại sao Q là câu kết quả", "conversation_id": "h1"},
                cookies={"lang": "en"}).json()
    vi = c.post("/chat", data={"message": "tại sao Q là câu kết quả", "conversation_id": "h1"},
                cookies={"lang": "vi"}).json()
    assert en["data"]["type"] == "mo_bang_gia_su" and not I.CO_DAU.search(en["message"]), en
    assert vi["message"].startswith("Bạn hỏi về câu nào")


# ---------------------------------------------------------------- 5
def test_hoi_gia_su_luu_vao_hoi_thoai(monkeypatch):
    luu = []
    monkeypatch.setattr(G, "get_current_user", lambda request: U)
    monkeypatch.setattr(G.gia_su_service, "hoi", lambda **kw: {"tra_loi": "Bước 1 ...", "dap_an_python": "A"})
    monkeypatch.setattr(G.history_service, "luu_tin_nhan", lambda **kw: luu.append(kw))
    c = TestClient(app)
    c.post("/api/giasu/hoi", json={"de_id": "d1", "so_thu_tu": 3, "cau_hoi": "Giảng lại câu 3",
                                   "conversation_id": "h1", "cau_hien_thi": "Giảng lại giúp mình câu 3"})
    assert [x["role"] for x in luu] == ["user", "assistant"]
    assert luu[0]["noi_dung"] == "Giảng lại giúp mình câu 3"
    assert luu[1]["loai_phan_hoi"] == "gia_su" and json.loads(luu[1]["noi_dung"])["data"]["dap_an_python"] == "A"
    luu.clear()
    c.post("/api/giasu/hoi", json={"de_id": "d1", "so_thu_tu": 3, "cau_hoi": "x"})   # trang làm bài: không lưu
    assert luu == []
