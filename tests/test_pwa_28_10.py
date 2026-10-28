"""Cài web như ứng dụng - PWA (cô Lan 28/10/2026: "tôi có thể tạo app để giảm sự phụ thuộc vào mạng không").

- /sw.js phục vụ đúng (JavaScript, không lưu đệm, phạm vi cả trang); mọi trang HTML có manifest + đăng kí service worker.
- Công tắc an toàn TAT_PWA=1: không chèn đăng kí, /sw.js trả bản tự gỡ (xoá bộ nhớ, huỷ đăng kí).
- Service worker chỉ xử lí GET (nộp bài, chat... đi thẳng mạng), trang HTML lấy mạng trước.
- Trang làm bài tự lưu bài đang làm trong máy, mất mạng lúc nộp thì chờ có mạng tự nộp.
(Đã chạy thử trên Chromium/Playwright: khôi phục MC/Đúng-Sai/trả lời ngắn sau khi tải lại, mất mạng -> có mạng tự nộp
đúng bài làm, máy chủ sập -> hiện trang báo mất kết nối.)
"""
import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

import app.main as M

GOC = Path(__file__).resolve().parent.parent
TINH = GOC / "app" / "static"


def test_sw_phuc_vu_dung():
    r = TestClient(M.app).get("/sw.js")
    assert r.status_code == 200 and r.headers["content-type"].startswith("application/javascript")
    assert r.headers["cache-control"] == "no-cache" and r.headers["service-worker-allowed"] == "/"
    assert "PHIEN_BAN" in r.text


def test_trang_html_co_manifest_va_dang_ki():
    r = TestClient(M.app).get("/login")
    assert r.status_code == 200
    assert r.text.count('rel="manifest"') == 1 and 'serviceWorker.register("/sw.js")' in r.text
    assert r.text.index('rel="manifest"') < r.text.index("</head>")


def test_khong_chen_hai_lan_va_khong_co_head():
    a = M._chen_pwa("<html><head><title>x</title></head><body></body></html>")
    assert M._chen_pwa(a) == a and a.count('rel="manifest"') == 1
    assert M._chen_pwa("<p>khong co head</p>") == "<p>khong co head</p>"


def test_cong_tac_tat_pwa(monkeypatch):
    monkeypatch.setattr(M, "_PWA_TAT", True)
    c = TestClient(M.app)
    assert 'rel="manifest"' not in c.get("/login").text
    sw = c.get("/sw.js").text
    assert "unregister()" in sw and "caches.delete" in sw and "fetch" not in sw


def test_manifest_va_icon():
    mf = json.loads((TINH / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert mf["display"] == "standalone" and mf["scope"] == "/" and mf["start_url"].startswith("/chat")
    for ic in mf["icons"]:
        f = TINH / ic["src"].removeprefix("/static/")
        assert f.exists() and f.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    r = TestClient(M.app).get("/static/manifest.webmanifest")
    assert r.status_code == 200 and "manifest+json" in r.headers["content-type"]
    assert TestClient(M.app).get("/static/offline.html").status_code == 200


def test_sw_chi_xu_li_get_va_khong_luu_api_khac():
    sw = (TINH / "sw.js").read_text(encoding="utf-8")
    assert 'if (req.method !== "GET") return;' in sw
    assert '"/static/downloads/"' in sw and "!res.redirected" in sw
    # chỉ 2 loại /api/ được đụng tới: ảnh hình vẽ và dữ liệu đề làm bài
    assert set(re.findall(r'"(/api/[a-z/]+)"', sw)) == {"/api/exam/hinh/", "/api/exam/quiz/"}


def test_trang_lam_bai_tu_luu_va_cho_mang_nop():
    html = (GOC / "app/templates/chat/lam_bai.html").read_text(encoding="utf-8")
    assert "const KHOA_LUU_BAI = 'bai_lam_' + DE_ID + '_' + USER_ID;" in html
    for f in ("function luuNhapBaiLam", "function khoiPhucBaiLam", "function xoaNhapBaiLam", "function choMangRoiNop"):
        assert f in html
    # khôi phục ngay sau khi vẽ đề; nộp xong mới xoá; mất mạng -> chờ 'online' rồi tự nộp
    assert html.index("khoiPhucBaiLam();") > html.index("main.innerHTML = html;")
    assert "DA_CHAM_XONG = true;\n        xoaNhapBaiLam();" in html
    assert "window.addEventListener('online'" in html and "navigator.onLine === false" in html
