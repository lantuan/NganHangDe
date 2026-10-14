"""Lưu ý "bản tiếng Anh mới có đến lớp / chương nào" cạnh ô "Kèm bản tiếng Anh" (cô Lan 14/10/2026)."""
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services import i18n_service as I

GOC = Path(__file__).resolve().parents[1]


def test_chuong_co_ban_tieng_anh_doc_tu_thu_muc_ngan_hang_anh():
    co = I.chuong_co_ban_tieng_anh()
    tren_dia = sorted(int(p.stem.split("_C")[1]) for p in (GOC / "data" / "python_bank_en" / "toan10").glob("L10_C*.py"))
    assert co[10] == tren_dia
    assert {1, 2, 3, 4} <= set(co[10])


def test_dai_chuong_gop_khoang_lien_tiep():
    assert I._dai_chuong([1, 2, 3]) == "1-3"
    assert I._dai_chuong([1, 2, 3, 5]) == "1-3, 5"
    assert I._dai_chuong([4]) == "4"


def test_luu_y_hai_ngon_ngu(monkeypatch):
    monkeypatch.setattr(I, "chuong_co_ban_tieng_anh", lambda: {10: [1, 2, 3]})
    assert "Lớp 10: Chương 1-3" in I.luu_y_pham_vi_tieng_anh("vi")
    assert "Grade 10: Chapters 1-3" in I.luu_y_pham_vi_tieng_anh("en")
    monkeypatch.setattr(I, "chuong_co_ban_tieng_anh", lambda: {10: [1], 11: [1, 2]})
    assert "Lớp 10: Chương 1; Lớp 11: Chương 1-2" in I.luu_y_pham_vi_tieng_anh("vi")
    monkeypatch.setattr(I, "chuong_co_ban_tieng_anh", lambda: {})
    assert "chưa có chương nào" in I.luu_y_pham_vi_tieng_anh("vi")


def test_endpoint_theo_ngon_ngu_trang():
    c = TestClient(app)
    vi = c.get("/api/exam/pham-vi-tieng-anh", cookies={"lang": "vi"}).json()
    en = c.get("/api/exam/pham-vi-tieng-anh", cookies={"lang": "en"}).json()
    assert vi["success"] and "Lưu ý" in vi["luu_y"] and "Chương" in vi["luu_y"]
    assert en["luu_y"].startswith("Note:") and "Chapter" in en["luu_y"]
    assert vi["chuong"]["10"] == en["chuong"]["10"]


def test_moi_cho_tick_tieng_anh_deu_co_luu_y():
    """Mọi nơi cho người dùng tick "Kèm bản tiếng Anh" phải có phần tử data-pham-vi-anh và nạp script."""
    for f in ("app/templates/chat/chat.html", "app/templates/chat/lam_bai.html", "app/templates/teacher/ra_de.html"):
        t = (GOC / f).read_text(encoding="utf-8")
        assert "data-pham-vi-anh" in t, f
    for f in ("app/templates/chat/chat.html", "app/templates/chat/lam_bai.html", "app/templates/teacher/_base_gv.html"):
        assert "luu_y_tieng_anh.js" in (GOC / f).read_text(encoding="utf-8"), f
    assert (GOC / "app/static/js/luu_y_tieng_anh.js").exists()
