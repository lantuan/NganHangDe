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


# ---------------------------------------------------------------------
# Trang "Toi la giao vien" - nang tai khoan dang dang nhap len giao vien
# ---------------------------------------------------------------------

def test_chua_dang_nhap_thi_ve_login(client):
    res = client.get("/toi-la-giao-vien", follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/login"


def test_ma_moi_sai_thi_bao_loi_khong_nang_vai_tro(client, monkeypatch):
    from app.routers import auth as router_auth
    from app.services import profile_service

    class UserGia:
        id = "11111111-1111-1111-1111-111111111111"
        email = "thu@example.com"

    da_goi = {"dat_vai_tro": False}

    monkeypatch.setattr(router_auth, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_auth.profile_service, "la_giao_vien", lambda uid: False)
    def gia_dat_vai_tro(uid, vai_tro):
        da_goi["dat_vai_tro"] = True
        return True
    monkeypatch.setattr(router_auth.profile_service, "dat_vai_tro", gia_dat_vai_tro)
    monkeypatch.setattr(router_auth, "MA_MOI_GIAO_VIEN", "MA-DUNG")

    res = client.post("/toi-la-giao-vien", data={"ma_moi": "MA-SAI"},
                      follow_redirects=False)

    assert res.status_code == 400
    assert "Mã mời không đúng" in res.text
    assert da_goi["dat_vai_tro"] is False, "Ma sai thi TUYET DOI khong duoc nang vai tro"


def test_ma_moi_dung_thi_nang_vai_tro_va_ve_gv(client, monkeypatch):
    from app.routers import auth as router_auth

    class UserGia:
        id = "22222222-2222-2222-2222-222222222222"
        email = "co@example.com"

    da_goi = {}

    monkeypatch.setattr(router_auth, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_auth.profile_service, "la_giao_vien", lambda uid: False)
    def gia_dat_vai_tro(uid, vai_tro):
        da_goi["uid"] = uid
        da_goi["vai_tro"] = vai_tro
        return True
    monkeypatch.setattr(router_auth.profile_service, "dat_vai_tro", gia_dat_vai_tro)
    monkeypatch.setattr(router_auth, "MA_MOI_GIAO_VIEN", "MA-DUNG")

    res = client.post("/toi-la-giao-vien", data={"ma_moi": "  MA-DUNG  "},
                      follow_redirects=False)

    assert res.status_code == 303
    assert res.headers["location"] == "/gv"
    assert da_goi == {"uid": UserGia.id, "vai_tro": "giao_vien"}


# ---------------------------------------------------------------------
# Man hinh chon vai tro (hien sau khi dang nhap lan dau)
# ---------------------------------------------------------------------

def _gia_lap_nguoi_dung(monkeypatch, vai_tro, email="moi@example.com"):
    """Gia lap mot nguoi dung dang dang nhap, dang o vai_tro cho truoc."""
    from app.routers import auth as router_auth

    class UserGia:
        id = "33333333-3333-3333-3333-333333333333"

    UserGia.email = email
    monkeypatch.setattr(router_auth, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_auth.profile_service, "lay_vai_tro", lambda uid: vai_tro)
    return router_auth, UserGia


def test_chua_chon_thi_hien_man_hinh_chon_vai_tro(client, monkeypatch):
    _gia_lap_nguoi_dung(monkeypatch, "chua_chon")
    res = client.get("/chon-vai-tro")
    assert res.status_code == 200
    assert "Học sinh" in res.text and "Giáo viên" in res.text


def test_da_la_hoc_sinh_thi_khong_hoi_lai(client, monkeypatch):
    _gia_lap_nguoi_dung(monkeypatch, "hoc_sinh")
    res = client.get("/chon-vai-tro", follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/chon-lop"


def test_da_la_giao_vien_thi_vao_thang_gv(client, monkeypatch):
    _gia_lap_nguoi_dung(monkeypatch, "giao_vien")
    res = client.get("/chon-vai-tro", follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/gv"


def test_chon_hoc_sinh_thi_luu_vai_tro_va_sang_chon_lop(client, monkeypatch):
    router_auth, UserGia = _gia_lap_nguoi_dung(monkeypatch, "chua_chon")
    da_luu = {}
    monkeypatch.setattr(router_auth.profile_service, "dat_vai_tro",
                        lambda uid, vt: da_luu.update(uid=uid, vai_tro=vt) or True)

    res = client.post("/chon-vai-tro", data={"vai_tro": "hoc_sinh"},
                      follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/chon-lop"
    assert da_luu == {"uid": UserGia.id, "vai_tro": "hoc_sinh"}


def test_chon_giao_vien_thi_sang_nhap_ma_moi_va_CHUA_nang_vai_tro(client, monkeypatch):
    router_auth, _ = _gia_lap_nguoi_dung(monkeypatch, "chua_chon")
    da_goi = {"dat": False}
    monkeypatch.setattr(router_auth.profile_service, "dat_vai_tro",
                        lambda uid, vt: da_goi.update(dat=True) or True)

    res = client.post("/chon-vai-tro", data={"vai_tro": "giao_vien"},
                      follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/toi-la-giao-vien"
    assert da_goi["dat"] is False, "Bam 'Giao vien' thoi CHUA duoc nang vai tro - phai nhap ma moi da"


# ---------------------------------------------------------------------
# Giao vien khong bi hoi chon lop; 403 hien trang ro rang
# ---------------------------------------------------------------------

def test_giao_vien_vao_chon_lop_thi_day_ve_gv(client, monkeypatch):
    from app.routers import chat as router_chat

    class UserGia:
        id = "44444444-4444-4444-4444-444444444444"
        email = "co@example.com"

    monkeypatch.setattr(router_chat, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_chat.profile_service, "lay_vai_tro", lambda uid: "giao_vien")

    res = client.get("/chon-lop", follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/gv"


def test_giao_vien_vao_chat_KHONG_bi_hoi_chon_lop(client, monkeypatch):
    from app.routers import chat as router_chat

    class UserGia:
        id = "55555555-5555-5555-5555-555555555555"
        email = "co@example.com"
        user_metadata = {"fullname": "Cô Lan"}

    monkeypatch.setattr(router_chat, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_chat.profile_service, "lay_vai_tro", lambda uid: "giao_vien")
    monkeypatch.setattr(router_chat.profile_service, "la_giao_vien", lambda uid: True)
    # Giao vien khong co lop - truoc day chinh cho nay day ho sang /chon-lop
    monkeypatch.setattr(router_chat.supabase_service, "lay_lop_hoc_sinh", lambda uid: None)

    res = client.get("/chat", follow_redirects=False)
    assert res.status_code == 200, "Giao vien phai vao thang Chat AI"
    assert "Chọn lớp của em" not in res.text


def test_403_hien_trang_ro_rang_kem_vai_tro(client, monkeypatch):
    from app.core import deps

    class UserGia:
        id = "66666666-6666-6666-6666-666666666666"
        email = "hs@example.com"

    monkeypatch.setattr(deps, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(deps.__dict__["__builtins__"] if False else deps, "lay_vai_tro",
                        lambda request, user=None: "hoc_sinh", raising=False)

    res = client.get("/gv/thong-ke", headers={"accept": "text/html"},
                     follow_redirects=False)
    # Hoc sinh -> 403, va phai la TRANG HTML co huong dan, khong phai JSON
    assert res.status_code == 403
    assert "Trang này dành cho giáo viên" in res.text
    assert "Tôi là giáo viên" in res.text
