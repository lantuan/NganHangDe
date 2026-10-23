"""Đăng kết quả lên Classroom (cô Lan 23/10/2026: "vẫn không tải được lên Classroom, cần kiểm tra lại").

- Lí do thất bại cụ thể (kết nối hết hạn invalid_grant, Google từ chối 403...) được trả về và hiện (chữ nhỏ) trên trang.
- PDF đề chưa biên dịch xong (đề làm trên web, dịch nền) -> biên dịch ngay; vẫn không có thì vẫn đăng ĐIỂM.
- Endpoint chạy trong threadpool (không chặn máy chủ khi cả lớp nộp bài cùng lúc).
"""
from pathlib import Path

import requests

from app.services import classroom_service as CS


class _Res:
    def __init__(self, ma, du_lieu):
        self.status_code, self._d, self.text = ma, du_lieu, str(du_lieu)

    def json(self):
        return self._d

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("loi", response=self)


def _chuan_bi(monkeypatch, tmp_path, files):
    monkeypatch.setattr(CS, "MA_LOP_CLASSROOM", {("10", "C9"): "course-1"})
    monkeypatch.setattr(CS.history_service, "lay_de_theo_id", lambda i: {"id": i, "files": files})
    monkeypatch.setattr(CS, "lay_refresh_token_theo_lop", lambda k, l: "rt")

    class _Bang:
        def insert(self, *_a):
            return self

        def execute(self):
            return None
    monkeypatch.setattr(CS.supabase, "table", lambda *_a: _Bang())


def _goi():
    return CS.dang_ket_qua_len_classroom("de-1", "hs@x", "10", "C9", "<p>ok</p>", 5, 7)


def test_ket_noi_het_han_noi_ro(monkeypatch, tmp_path):
    _chuan_bi(monkeypatch, tmp_path, {})
    monkeypatch.setattr(CS.requests, "post", lambda *a, **k: _Res(400, {"error": "invalid_grant"}))
    kq = _goi()
    assert not kq["success"] and "invalid_grant" in kq["message"] and "Kết nối Google Classroom" in kq["message"]


def test_chua_co_pdf_van_dang_diem(monkeypatch, tmp_path):
    tex = tmp_path / "exam_x.tex"
    tex.write_text("x", encoding="utf-8")
    _chuan_bi(monkeypatch, tmp_path, {"de": str(tmp_path / "exam_x.pdf"), "tex": str(tex)})
    dich = []
    from app.services import exam_assembler_service as A
    monkeypatch.setattr(A, "bien_dich_pdf_de_hoc_sinh", lambda t: dich.append(t))
    than = []

    def _post(url, **k):
        if "token" in url:
            return _Res(200, {"access_token": "at"})
        than.append(k.get("json"))
        return _Res(200, {"id": "cw-1"})
    monkeypatch.setattr(CS.requests, "post", _post)
    kq = _goi()
    assert kq["success"] and dich == [str(tex)]
    assert than and "materials" not in than[-1] and "5/7" in than[-1]["description"]


def test_google_tu_choi_noi_ro(monkeypatch, tmp_path):
    _chuan_bi(monkeypatch, tmp_path, {})

    def _post(url, **k):
        if "token" in url:
            return _Res(200, {"access_token": "at"})
        return _Res(403, {"error": {"status": "PERMISSION_DENIED"}})
    monkeypatch.setattr(CS.requests, "post", _post)
    kq = _goi()
    assert not kq["success"] and "PERMISSION_DENIED" in kq["message"] and "hs@x" in kq["message"]


def test_trang_lam_bai_hien_li_do_va_endpoint_khong_chan():
    goc = Path(__file__).resolve().parent.parent
    html = (goc / "app/templates/chat/lam_bai.html").read_text(encoding="utf-8")
    assert "'Lí do:'" in html and "escapeHtmlCls(liDo)" in html
    chat = (goc / "app/routers/chat.py").read_text(encoding="utf-8")
    assert "run_in_threadpool(\n        classroom_service.dang_ket_qua_len_classroom" in chat
