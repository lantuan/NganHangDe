"""Nút "📘 Đúng chương trình" / "🚀 Nâng cao thêm" ở khung chat (cô Lan 21/10/2026).

Học sinh không hiểu "YCCĐ", nên nói bằng lời đơn giản: Đúng chương trình = chỉ các dạng theo yêu cầu cần đạt của Bộ
(chi_yccd=True, như "Chỉ theo YCCĐ" của giáo viên); Nâng cao thêm = có cả dạng luyện tập thêm (như trước).
Lựa chọn đi theo MỌI đường tạo đề: gọi thẳng API (form tạo đề nhanh, nút đồng ý), tin nhắn qua n8n (ghi theo hội
thoại), "Làm đề khác" (giữ lựa chọn của đề gốc).
"""
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import exam as router_exam
from app.services import tuy_chon_de_service as T

GOC = Path(__file__).resolve().parent.parent


@pytest.fixture
def tep_tam(monkeypatch, tmp_path):
    monkeypatch.setattr(T, "TEP", tmp_path / "tuy_chon.json")


def test_ghi_hai_lua_chon_khong_de_nhau(tep_tam):
    T.dat_kem_tieng_anh("hoi-1", True)
    T.dat_chi_yccd("hoi-1", True)
    assert T.lay_kem_tieng_anh("hoi-1") is True and T.lay_chi_yccd("hoi-1") is True
    T.dat_kem_tieng_anh("hoi-1", False)
    assert T.lay_chi_yccd("hoi-1") is True                     # đổi ô tiếng Anh không xoá nút mức luyện tập
    T.dat_chi_yccd("hoi-1", False)
    assert T.lay_chi_yccd("hoi-1") is False
    assert T.lay_chi_yccd("hoi-khac") is False and T.lay_chi_yccd(None) is False


def _goi_api(monkeypatch, tmp_path, than):
    da_goi = {}
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "a.tex").write_text("x")

    def gia_generate(**kw):
        da_goi.update(kw)
        return {"pdf_path": str(tmp_path / "a.pdf"), "tex_path": str(tmp_path / "a.tex"), "pdf_loigiai_path": None,
                "dap_an_json_path": None, "so_cau_da_sinh": 1, "so_cau_thieu": 0, "danh_sach_generator_id": []}

    monkeypatch.setattr(router_exam, "generate_exam_pdf_auto", gia_generate)
    luu = {}
    monkeypatch.setattr(router_exam.history_service, "luu_de_da_sinh", lambda **kw: luu.update(kw) or None)
    monkeypatch.setattr(router_exam.profile_service, "la_giao_vien", lambda uid: False)
    r = TestClient(app).post("/api/exam/generate-pdf-auto", json=dict(
        {"lop": 10, "tieu_de": "DE", "role": "student", "loai_he_so": "HeSo1", "pham_vi_chuong": "chuong_3",
         "user_id": "88888888-8888-8888-8888-888888888888"}, **than))
    assert r.status_code == 200, r.text
    return da_goi, luu


def test_api_nhan_nut_gui_thang(monkeypatch, tmp_path, tep_tam):
    da_goi, luu = _goi_api(monkeypatch, tmp_path, {"conversation_id": "hoi-2", "chi_yccd": True})
    assert da_goi["chi_yccd"] is True
    assert luu["blueprint"]["chi_yccd"] is True                 # "Làm đề khác" đọc lại được
    da_goi, _ = _goi_api(monkeypatch, tmp_path, {"conversation_id": "hoi-2", "chi_yccd": False})
    assert da_goi["chi_yccd"] is False


def test_api_tu_n8n_tra_theo_hoi_thoai(monkeypatch, tmp_path, tep_tam):
    T.dat_chi_yccd("hoi-3", True)                               # /chat đã ghi khi học sinh gửi tin nhắn
    da_goi, _ = _goi_api(monkeypatch, tmp_path, {"conversation_id": "hoi-3"})
    assert da_goi["chi_yccd"] is True
    da_goi, _ = _goi_api(monkeypatch, tmp_path, {"conversation_id": "hoi-chua-ghi"})
    assert da_goi["chi_yccd"] is False                          # không ghi nhận: như trước


@pytest.mark.parametrize("goc, mong", [({"chi_yccd": True}, True), ({"chi_yccd": False}, False), ({}, False)])
def test_lam_de_khac_giu_lua_chon(monkeypatch, tmp_path, goc, mong):
    da_goi = {}
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    monkeypatch.setattr(router_exam.history_service, "lay_de_theo_id", lambda de_id: {
        "lop": 10, "role": "student", "loai_he_so": "HeSo1", "pham_vi_chuong": "chuong_3", "blueprint": goc})
    monkeypatch.setattr(router_exam, "generate_exam_pdf_auto", lambda **kw: da_goi.update(kw) or {
        "pdf_path": str(tmp_path / "a.pdf"), "tex_path": str(tmp_path / "a.pdf"), "pdf_loigiai_path": None,
        "dap_an_json_path": None, "so_cau_da_sinh": 1})
    monkeypatch.setattr(router_exam.history_service, "luu_de_da_sinh", lambda **kw: "de-moi")
    monkeypatch.setattr(router_exam.history_service, "luu_file_de", lambda *a, **k: None)
    r = TestClient(app).post("/api/exam/lam-de-khac", json={"de_id": "de-cu"})
    assert r.status_code == 200, r.text
    assert da_goi["chi_yccd"] is mong


def test_trang_chat_co_nut_va_gui_lua_chon():
    html = (GOC / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert "📘 Đúng chương trình" in html and "🚀 Nâng cao thêm" in html
    assert 'id="muc-luyen-chinh"' in html
    # ba đường gửi: hai lời gọi thẳng API + tin nhắn /chat
    assert len(re.findall(r"chi_yccd: chiYccd\(\)", html)) == 2
    assert 'formData.append("chi_yccd", chiYccd() ? "1" : "0")' in html
    # nút có ở form tạo đề nhanh và ở khung xác nhận cấu trúc
    assert html.count("${htmlMucLuyen()}") == 2


def test_khung_nhap_khong_lap_lai_lua_chon_khi_form_da_co():
    """Cô Lan 22/10/2026: form "Tạo đề mới" / khung xác nhận ở trên đã có nút mức luyện tập và ô tiếng Anh thì hàng lựa
    chọn ở khung nhập phía dưới phải ẩn; ô tick tiếng Anh trong form nằm cùng dòng với chữ."""
    html = (GOC / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert 'messages.querySelector(".muc-luyen, .chk-kem-anh") ? "none" : ""' in html
    assert "new MutationObserver(capNhatHangTuyChon).observe(messages" in html
    assert ".form-nhom label.tick-kem-anh input" in html
