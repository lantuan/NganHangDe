from app.core.supabase import supabase


def sign_up(fullname: str, email: str, password: str,
            vai_tro: str = "hoc_sinh", **them):
    """
    Đăng ký tài khoản mới trên Supabase Auth.

    vai_tro: 'hoc_sinh' (mặc định) hoặc 'giao_vien'. Giá trị này đi vào
    user_metadata để trigger handle_new_user ghi xuống profiles.vai_tro.
    Tuy nhiên KHÔNG phụ thuộc vào trigger: sau khi đăng ký, router còn
    gọi profile_service.dat_vai_tro() một lần nữa cho chắc.

    **them: các trường phụ (truong, to_chuyen_mon...) ghi kèm metadata.
    """

    du_lieu = {"fullname": fullname, "vai_tro": vai_tro}
    du_lieu.update({k: v for k, v in them.items() if v})

    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
            "options": {
                "data": du_lieu
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


def lay_lop_hoc_sinh(user_id: str):
    """
    Doc khoi/lop hoc sinh da tu chon o trang /chon-lop, tu bang
    public.profiles. Tra ve dict {"khoi":..., "lop":...} hoac None neu
    chua chon / co loi (khong lam crash luong /chat).
    """
    try:
        ket_qua = (
            supabase.table("profiles")
            .select("khoi, lop")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return ket_qua.data
    except Exception as e:
        print("LOI DOC PROFILE (lay_lop_hoc_sinh):", e)
        return None


def cap_nhat_lop_hoc_sinh(user_id: str, khoi: str, lop: str):
    """
    Ghi khoi/lop hoc sinh tu chon vao public.profiles.
    """
    return (
        supabase.table("profiles")
        .update({"khoi": khoi, "lop": lop})
        .eq("id", user_id)
        .execute()
    )