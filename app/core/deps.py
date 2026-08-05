from fastapi import Request
from app.core.supabase import supabase


def get_current_user(request: Request):
    """
    Doc access_token tu cookie (dat luc dang nhap), xac thuc voi Supabase.
    Tra ve user (co .id, .email, .user_metadata) neu hop le, None neu chua
    dang nhap hoac token het han/khong hop le.
    """
    token = request.cookies.get("sb_access_token")
    if not token:
        return None
    try:
        result = supabase.auth.get_user(token)
        return result.user
    except Exception as e:
        print("LOI XAC THUC PHIEN:", e)
        return None
