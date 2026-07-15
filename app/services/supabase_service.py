from app.core.supabase import supabase


def sign_up(fullname: str, email: str, password: str):
    """
    Đăng ký tài khoản mới trên Supabase Auth
    """

    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "fullname": fullname
                }
            }
        }
    )


def sign_in(email: str, password: str):
    """
    Đăng nhập
    """

    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )


def sign_out():
    """
    Đăng xuất
    """

    return supabase.auth.sign_out()


def get_user():
    """
    Lấy thông tin user hiện tại
    """

    return supabase.auth.get_user()