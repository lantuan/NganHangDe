"""
Kiem tra trang dang nhap KHONG con tra 500 khi sai tai khoan/mat khau.

Vi sao can bai kiem tra nay: ngay 15/09/2026 co 2 loi noi tiep nhau o cung
mot cho, ma bai kiem tra kieu "import co chay khong" deu khong bat duoc:

  1. Khoi try/except ket thuc bang "raise" -> sai mat khau ra 500.
  2. Sua xong lai goi templates.TemplateResponse("ten.html", {...}) theo
     kieu cu; ban Starlette moi coi tham so dau la request nen nem
     "TypeError: unhashable type: 'dict'" -> VAN ra 500.

Ca hai chi lo ra khi co nguoi go sai mat khau tren web that. Bai kiem tra
nay gia lap dung tinh huong do, KHONG can mang va khong can Supabase.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import supabase_service


class _LoiGiaDinh(Exception):
    """Dong vai AuthApiError khi khong import duoc lop that."""


def _loi_sai_mat_khau():
    try:
        from supabase_auth.errors import AuthApiError
        return AuthApiError("Invalid login credentials", 400, "invalid_credentials")
    except Exception:
        return _LoiGiaDinh("Invalid login credentials")


@pytest.fixture
def client():
    return TestClient(app)


def test_sai_mat_khau_khong_ra_500(client, monkeypatch):
    def gia_sign_in(email, password):
        raise _loi_sai_mat_khau()

    monkeypatch.setattr(supabase_service, "sign_in", gia_sign_in)

    res = client.post(
        "/login",
        data={"email": "khongcothat@example.com", "password": "sai"},
        follow_redirects=False,
    )

    assert res.status_code != 500, "Sai mat khau KHONG duoc ra 500"
    assert res.status_code == 401
    assert "Tài khoản không tồn tại hoặc mật khẩu không đúng" in res.text
    # Email vua go phai duoc giu lai de khoi nhap lai
    assert "khongcothat@example.com" in res.text


def test_loi_la_cung_khong_ra_500(client, monkeypatch):
    def gia_sign_in(email, password):
        raise RuntimeError("mat mang")

    monkeypatch.setattr(supabase_service, "sign_in", gia_sign_in)

    res = client.post(
        "/login",
        data={"email": "a@b.c", "password": "x"},
        follow_redirects=False,
    )

    assert res.status_code != 500
    assert "Hệ thống đang bận" in res.text


def test_trang_dang_nhap_binh_thuong_van_mo_duoc(client):
    res = client.get("/login")
    assert res.status_code == 200
    # Khong co loi thi KHONG duoc hien o bao loi
    assert "Tài khoản không tồn tại hoặc mật khẩu không đúng" not in res.text
