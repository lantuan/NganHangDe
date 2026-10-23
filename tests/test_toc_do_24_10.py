"""Tăng tốc web an toàn (cô Lan 24/10/2026: "tôi muốn tốc độ của web nhanh hơn ... mai tôi nộp ... đừng để chết web").

1. Bộ nhớ tạm ngắn hạn (app/core/bo_nho_tam.py): nhớ kết quả thành công, hết hạn, đầy thì bỏ bớt, không nhớ khi test.
2. Trang / API không dùng await viết dạng `def` (FastAPI chạy trong threadpool) - không chặn cả máy chủ khi chờ Supabase.
3. Nén gzip cho HTML/JSON, KHÔNG nén các đường trả tệp (PDF, Word, ảnh).
4. marked ghi rõ phiên bản (bản mới không còn marked.min.js); khung xác nhận tạo đề không hỏng khi marked chưa tải.
"""
import ast
import time
from pathlib import Path

from fastapi.testclient import TestClient

from app.core import bo_nho_tam as B

GOC = Path(__file__).resolve().parent.parent


def test_bo_nho_tam(monkeypatch):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    m = B.BoNhoTam(0.2, toi_da=4)
    assert m.lay("a") == (False, None)
    m.dat("a", 1)
    assert m.lay("a") == (True, 1)
    time.sleep(0.25)
    assert m.lay("a") == (False, None)                    # hết hạn
    for i in range(6):
        m.dat(i, i)
    assert len(m._du_lieu) <= 4                            # đầy thì bỏ bớt
    m.dat("b", 2)
    m.xoa("b")
    assert m.lay("b") == (False, None)


def test_khi_test_khong_nho():
    m = B.BoNhoTam(100)
    m.dat("a", 1)
    assert m.lay("a") == (False, None)


def test_khong_con_async_def_chi_dung_dong_bo():
    for f in ("auth", "chat", "classroom", "home", "teacher"):
        src = (GOC / "app" / "routers" / (f + ".py")).read_text(encoding="utf-8")
        for n in ast.walk(ast.parse(src)):
            if isinstance(n, ast.AsyncFunctionDef):
                assert any(isinstance(x, ast.Await) for x in ast.walk(n)), (f, n.name)
    chat = (GOC / "app/routers/chat.py").read_text(encoding="utf-8")
    than = chat[chat.index("async def chat_post"):]
    assert "history_service.luu_tin_nhan(" not in than.split("\n@router")[0]
    assert "await run_in_threadpool(get_current_user, request)" in than


def test_nen_gzip():
    from app.main import app
    c = TestClient(app)
    r = c.get("/login", headers={"Accept-Encoding": "gzip"})
    assert r.status_code == 200 and r.headers.get("content-encoding") == "gzip"
    assert c.get("/login", headers={"Accept-Encoding": "identity"}).headers.get("content-encoding") is None
    from app.main import _KHONG_NEN
    for p in ("/api/exam/tai-de/x", "/api/exam/generate-pdf-auto", "/api/exam/hinh/abc", "/api/exam/tai-word/x"):
        assert p.startswith(_KHONG_NEN)


def test_marked_ghi_phien_ban_va_khung_xac_nhan_khong_hong():
    for f in ("chat/chat.html", "chat/lam_bai.html"):
        h = (GOC / "app/templates" / f).read_text(encoding="utf-8")
        assert 'src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"' not in h and "npm/marked@15.0.12/marked.min.js" in h
    h = (GOC / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert "${marked.parseInline(" not in h and "mdMotDong(" in h and "highlight.min.js" not in h
