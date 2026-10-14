"""Hết phiên đăng nhập khi bấm tải Word (cô Lan 14/10/2026): trước đây route /api/* chuyển hướng 303 về /login,
fetch() theo luôn và lưu trang đăng nhập thành "de_tai_ve.html". Nay /api/* trả 401 JSON; route /gv/* vẫn chuyển hướng."""
from fastapi.testclient import TestClient

from app.main import app


def test_tai_word_khong_dang_nhap_tra_401_json_khong_chuyen_huong():
    r = TestClient(app).get("/api/exam/tai-word/abc?ban=de", follow_redirects=False)
    assert r.status_code == 401
    assert "het han" in r.json()["detail"]


def test_trang_gv_chua_dang_nhap_van_chuyen_huong():
    r = TestClient(app).get("/gv/ra-de", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/login"


def test_js_tai_tep_khong_luu_html_thanh_tep():
    from pathlib import Path
    html = (Path(__file__).resolve().parents[1] / "app/templates/teacher/_base_gv.html").read_text(encoding="utf-8")
    assert "res.redirected" in html and 'text/html' in html
