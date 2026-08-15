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
