"""Việt / Anh (cô Lan 03/10/2026): nút chuyển ngôn ngữ, từ điển giao diện, dịch trang HTML và thông báo JSON."""
import importlib.util
import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services import i18n_service as i18n

GOC = Path(__file__).resolve().parents[1]


def _trich():
    spec = importlib.util.spec_from_file_location("trich", GOC / "scripts" / "i18n_trich_chuoi.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.trich_template()


def test_moi_chu_trong_template_co_ban_dich():
    """Template thêm chữ Việt mới thì phải thêm vào data/i18n/en_ui.json
    (xem: python3 scripts/i18n_trich_chuoi.py --chua-dich)."""
    td = json.loads((GOC / "data" / "i18n" / "en_ui.json").read_text(encoding="utf-8"))
    thieu = sorted(k for k in _trich() if k not in td)
    assert not thieu, "Chua dich %d doan, vd: %s" % (len(thieu), thieu[:5])


def test_ban_dich_khong_pha_html_js():
    """Bản dịch nằm trong chuỗi JS / thuộc tính HTML nên không được thêm nháy, <, >, {, }, $, \\."""
    for f in (GOC / "data" / "i18n").glob("en_*.json"):
        for k, v in json.loads(f.read_text(encoding="utf-8")).items():
            for ch in "'\"`<>{}\\$\n":
                assert ch in k or ch not in v, (f.name, k, v)
            assert not i18n.CO_DAU.search(v) or "Tiếng Việt" in v or v == k, (f.name, k, v)


def test_dich_doan_va_cum_ghep_bien():
    assert i18n.dich_html("<button>Tạo đề</button>", "en") == "<button>Create exam</button>"
    assert i18n.dich_html("<p>Xin chào, Lan!</p>", "en") == "<p>Hello, Lan!</p>"
    assert i18n.dich_html("<p>Lớp 10</p>", "en") == "<p>Grade 10</p>"
    assert i18n.dich_html("<p>Xyz hoàn toàn mới ạ</p>", "en") == "<p>Xyz hoàn toàn mới ạ</p>"
    assert i18n.dich_html("<p>Tạo đề</p>", "vi") == "<p>Tạo đề</p>"


def test_dich_json_chi_dich_khoa_thong_bao():
    d = {"message": "Có lỗi xảy ra.", "generator_id": "Tạo đề", "ten_chuong": "Vectơ"}
    kq = i18n.dich_json(d, "en")
    assert kq["message"] == "An error occurred." and kq["ten_chuong"] == "Vectors"
    assert kq["generator_id"] == "Tạo đề"


def test_trang_dang_nhap_hai_ngon_ngu():
    c = TestClient(app)
    vi = c.get("/login")
    assert "Đăng nhập" in vi.text and 'id="chv-lang"' in vi.text and 'lang="vi"' in vi.text
    en = c.get("/login?lang=en")
    assert "Sign in" in en.text and "Đăng nhập" not in en.text and 'lang="en"' in en.text
    assert en.cookies.get("lang") == "en"
    c2 = TestClient(app)
    c2.cookies.set("lang", "en")
    assert "Sign in" in c2.get("/login").text           # cookie nho lua chon
    assert "Tiếng Việt" in c2.get("/login").text         # nut chuyen luon hien tieng goc cua no


def test_khong_dich_file_tinh_va_json_tieng_viet():
    c = TestClient(app)
    c.cookies.set("lang", "en")
    assert c.get("/static/js/nonexistent.js").status_code == 404
    r = c.get("/api/exam/danh-sach-chuong?lop=10")
    assert r.status_code in (200, 401, 403)
    if r.status_code == 200:
        assert "Vectors" in r.text


def test_tu_khong_dau_va_chu_y_duoc_dich():
    """"Sai" (không dấu) chỉ dịch khi cả đoạn khớp từ điển; "ý" ở kết quả Đúng/Sai thành "Part"."""
    from app.services.i18n_service import dich_doan
    assert dich_doan(" Sai", "en") == " False"
    assert dich_doan(" Đúng\u200b", "en") == " True"   # nút Đúng/Sai: True/False
    assert dich_doan(" ý ", "en") == " Part "
    assert dich_doan(" Đúng", "en") == " Correct"
    assert dich_doan("Saigon", "en") == "Saigon"
