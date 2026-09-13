from fastapi import Request
from app.core.supabase import supabase


def _thu_lam_moi_phien(refresh_token: str):
    """
    access_token (JWT) cua Supabase mac dinh het han sau ~1 gio, du cookie
    sb_access_token con song bao lau di nua (7/30 ngay neu tick "Ghi nho
    dang nhap" - xem app/routers/auth.py::login). Truoc day khong co ham
    nay nen sau ~1 gio la bi dang xuat het, tick hay khong tick "Ghi nho
    dang nhap" cung nhu nhau. Ham nay dung refresh_token (song lau hon
    nhieu, thuong con hop le ca khi access_token da het han) de xin
    access_token moi, khong bat nguoi dung dang nhap lai.
    """
    try:
        ket_qua = supabase.auth.refresh_session(refresh_token)
        if ket_qua and ket_qua.session:
            return ket_qua.session
    except Exception as e:
        print("LOI LAM MOI PHIEN:", e)
    return None


def get_current_user(request: Request):
    """
    Doc access_token tu cookie (dat luc dang nhap), xac thuc voi Supabase.
    Neu access_token het han nhung refresh_token (cookie sb_refresh_token)
    con hop le, tu dong lam moi phien (_thu_lam_moi_phien) va luu phien
    moi vao request.state.new_session de middleware lam_moi_cookie_phien
    (app/main.py) ghi lai 2 cookie moi cho response - nguoi dung khong
    hay biet gi, van tiep tuc dang nhap binh thuong.
    Tra ve user (co .id, .email, .user_metadata) neu hop le, None neu ca
    access_token lan refresh_token deu khong con hop le (that su can dang
    nhap lai).
    """
    token = request.cookies.get("sb_access_token")
    if token:
        try:
            result = supabase.auth.get_user(token)
            return result.user
        except Exception:
            pass  # access_token het han/khong hop le - thu lam moi ben duoi

    refresh_token = request.cookies.get("sb_refresh_token")
    if not refresh_token:
        return None

    session = _thu_lam_moi_phien(refresh_token)
    if session is None:
        return None

    request.state.new_session = session
    return session.user


# ======================================================
# PHAN QUYEN (them 2026-09-13)
# Truoc day moi route /gv/* chi kiem tra DA DANG NHAP, khong kiem tra
# vai tro -> bat ky hoc sinh nao biet duong dan /gv/thong-ke deu xem
# duoc diem ca lop. Hai ham duoi day de chan o TANG SERVER (khong chi
# an nut tren giao dien). Xem docs/21_TAI_KHOAN_GIAO_VIEN.md.
# ======================================================

def lay_vai_tro(request: Request, user=None) -> str:
    """
    Tra ve vai tro cua nguoi dang dang nhap: 'khach' | 'hoc_sinh' |
    'giao_vien' | 'quan_tri' | 'chua_cau_hinh'.
    Truyen san `user` neu da goi get_current_user() truoc do, de khong
    phai xac thuc 2 lan (moi lan la 1 luot goi sang Supabase).
    """
    from app.services import profile_service  # import tre: tranh vong lap import

    if user is None:
        user = get_current_user(request)
    if user is None:
        return "khach"
    return profile_service.lay_vai_tro(user.id)


def yeu_cau_giao_vien(request: Request, user=None):
    """
    Dat o dau MOI route /gv/*:

        chan = yeu_cau_giao_vien(request, user)
        if chan is not None:
            return chan

    Tra ve None neu du quyen. Neu chua dang nhap -> RedirectResponse ve
    /login. Neu da dang nhap nhung khong phai giao vien -> raise 403.
    """
    from fastapi import HTTPException
    from fastapi.responses import RedirectResponse
    from app.services import profile_service

    vai_tro = lay_vai_tro(request, user)

    if vai_tro == "khach":
        return RedirectResponse("/login", status_code=303)

    if vai_tro == profile_service.VAI_TRO_CHUA_CAU_HINH:
        raise HTTPException(
            status_code=500,
            detail=(
                "Chua co cot profiles.vai_tro. Chay doan SQL o Buoc 1 trong "
                "docs/21_TAI_KHOAN_GIAO_VIEN.md roi thu lai."
            ),
        )

    if vai_tro not in profile_service.VAI_TRO_GIAO_VIEN:
        raise HTTPException(
            status_code=403,
            detail="Chuc nang nay danh rieng cho tai khoan giao vien.",
        )

    return None
