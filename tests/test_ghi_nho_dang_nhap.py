"""
Kiem tra o "Ghi nho dang nhap" tren trang /login.

Khong can mang, khong can Supabase (gia lap sign_in / get_user).
  - POST /login: co tick -> cookie 7/30 ngay + sb_ghi_nho=1; khong tick -> cookie phien + sb_ghi_nho=0.
  - POST /auth/set-session (Google): cung quy tac, mac dinh (khong gui remember) = ghi nho nhu cu.
  - /logout xoa ca sb_ghi_nho.
  - Trang /login co chu thich + doan JS nho email (khong luu mat khau).
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import auth
from app.services import supabase_service


class _Phien:
    access_token = "AT"
    refresh_token = "RT"


class _User:
    id = "u1"


class _KetQua:
    user = _User()
    session = _Phien()


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(supabase_service, "sign_in", lambda email, password: _KetQua())
    monkeypatch.setattr(auth.supabase.auth, "get_user", lambda token: _KetQua())
    return TestClient(app, follow_redirects=False)


def _cookie(res, ten):
    for h in res.headers.get_list("set-cookie"):
        if h.startswith(ten + "="):
            return h
    raise AssertionError(f"khong co cookie {ten}")


def test_login_khong_tick_la_cookie_phien(client):
    res = client.post("/login", data={"email": "a@b.c", "password": "x"})
    assert res.status_code == 303
    for ten in ("sb_access_token", "sb_refresh_token", "sb_ghi_nho"):
        assert "Max-Age" not in _cookie(res, ten)
    assert _cookie(res, "sb_ghi_nho").startswith("sb_ghi_nho=0")


def test_login_co_tick_cookie_dai_han(client):
    res = client.post("/login", data={"email": "a@b.c", "password": "x", "remember": "true"})
    assert "Max-Age=604800" in _cookie(res, "sb_access_token")
    assert "Max-Age=2592000" in _cookie(res, "sb_refresh_token")
    assert _cookie(res, "sb_ghi_nho").startswith("sb_ghi_nho=1")


@pytest.mark.parametrize("body,dai_han", [
    ({}, True),                      # khong gui remember -> ghi nho nhu cu
    ({"remember": True}, True),
    ({"remember": False}, False),
])
def test_google_set_session_ton_trong_lua_chon(client, body, dai_han):
    res = client.post("/auth/set-session", json={"access_token": "AT", "refresh_token": "RT", **body})
    assert res.status_code == 200
    assert ("Max-Age=604800" in _cookie(res, "sb_access_token")) == dai_han
    assert ("Max-Age=2592000" in _cookie(res, "sb_refresh_token")) == dai_han
    assert _cookie(res, "sb_ghi_nho").startswith("sb_ghi_nho=" + ("1" if dai_han else "0"))


def test_logout_xoa_sb_ghi_nho(client):
    res = client.get("/logout")
    assert "sb_ghi_nho=" in " ".join(res.headers.get_list("set-cookie"))


def test_trang_login_co_chu_thich_va_nho_email(client):
    html = client.get("/login").text
    assert "Lưu email và giữ đăng nhập 7 ngày" in html
    assert "nhd_email_ghi_nho" in html
    assert "nhd_gg_ghi_nho" in html
    # Tuyet doi khong luu mat khau o trinh duyet: moi lenh setItem chi duoc
    # ghi gia tri email (hoac co Google), khong dung toi o mat khau.
    import re
    for m in re.finditer(r"setItem\(([^)]*)\)", html):
        assert "password" not in m.group(1).lower()
