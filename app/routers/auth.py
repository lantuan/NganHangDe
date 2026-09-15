from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from supabase_auth.errors import AuthApiError
from pydantic import BaseModel
from app.services import supabase_service, profile_service
from app.core.config import SUPABASE_URL, SUPABASE_KEY, MA_MOI_GIAO_VIEN
from app.core.supabase import supabase

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# ======================================================
# LOGIN PAGE
# ======================================================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )

# ======================================================
# REGISTER ROLE PAGE
# ======================================================

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
    )


# ======================================================
# REGISTER STUDENT PAGE
# ======================================================

@router.get("/register/student", response_class=HTMLResponse)
async def register_student_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register_student.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )


# ======================================================
# POST /login
# ======================================================

def _trang_login_loi(request: Request, email: str, thong_bao: str,
                    goi_y_dang_ky: bool = False):
    """Hien lai trang dang nhap kem thong bao loi (KHONG tra 500)."""
    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "error": thong_bao,
            "email": email,
            "goi_y_dang_ky": goi_y_dang_ky,
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
        status_code=401,
    )


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: str | None = Form(default=None),
):
    print("===== LOGIN =====")
    print(email, "| remember:", bool(remember))

    # SUA 2026-09-15: truoc day khoi try/except ket thuc bang "raise", nen
    # go sai email hoac mat khau la ra thang trang trang "Internal Server
    # Error" (500). Nay bat loi va hien lai trang dang nhap kem thong bao.
    try:
        result = supabase_service.sign_in(email=email, password=password)
    except AuthApiError as e:
        loi = str(getattr(e, "message", "") or e)
        print("LOI DANG NHAP:", loi)

        if "Email not confirmed" in loi:
            return _trang_login_loi(
                request, email,
                "Tài khoản chưa xác nhận email. Kiểm tra hộp thư (cả mục Thư "
                "rác) và bấm vào liên kết xác nhận, rồi đăng nhập lại.",
            )

        # LUU Y: Supabase co y tra ve CUNG mot loi "Invalid login credentials"
        # cho ca 2 truong hop sai mat khau va email chua dang ky - de nguoi
        # ngoai khong do duoc email nao da co tai khoan. Vi vay KHONG the
        # chuyen thang sang trang dang ky khi "tai khoan khong ton tai": he
        # thong khong phan biet duoc. Thay vao do hien nut "Dang ky tai khoan
        # moi" ngay trong o bao loi.
        return _trang_login_loi(
            request, email,
            "Email hoặc mật khẩu không đúng. Nếu chưa có tài khoản, bấm nút "
            "bên dưới để đăng ký.",
            goi_y_dang_ky=True,
        )
    except Exception as e:
        print("LOI DANG NHAP (khong ro):", type(e), e)
        return _trang_login_loi(
            request, email,
            "Hệ thống đang bận, thử lại sau ít phút.",
        )

    if result.user is None or result.session is None:
        return _trang_login_loi(
            request, email,
            "Email hoặc mật khẩu không đúng. Nếu chưa có tài khoản, bấm nút "
            "bên dưới để đăng ký.",
            goi_y_dang_ky=True,
        )

    response = RedirectResponse("/chat", status_code=303)

    if remember:
        access_max_age = 60 * 60 * 24 * 7
        refresh_max_age = 60 * 60 * 24 * 30
    else:
        access_max_age = None
        refresh_max_age = None

    response.set_cookie(
        key="sb_access_token",
        value=result.session.access_token,
        httponly=True, secure=True, samesite="lax",
        max_age=access_max_age,
    )
    response.set_cookie(
        key="sb_refresh_token",
        value=result.session.refresh_token,
        httponly=True, secure=True, samesite="lax",
        max_age=refresh_max_age,
    )

    # SUA 2026-09-15: ghi lai LUA CHON cua nguoi dung. Truoc day middleware
    # lam_moi_cookie_phien (app/main.py) moi lan lam moi phien deu ghi de
    # cookie voi han co dinh 7/30 ngay, bat ke nguoi dung co tick "Ghi nho
    # dang nhap" hay khong - nen lua chon o day bi xoa sach sau lan lam moi
    # dau tien. Nay middleware doc cookie nay de giu dung lua chon.
    response.set_cookie(
        key="sb_ghi_nho",
        value="1" if remember else "0",
        httponly=True, secure=True, samesite="lax",
        max_age=60 * 60 * 24 * 30 if remember else None,
    )

    return response


# ======================================================
# LOGOUT
# ======================================================

@router.get("/logout")
async def logout():
    response = RedirectResponse(
        "/login",
        status_code=303,
    )
    response.delete_cookie("sb_access_token")
    response.delete_cookie("sb_refresh_token")
    return response


# ======================================================
# QUEN MAT KHAU (gui email dat lai mat khau qua Supabase)
# ======================================================

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/forgot_password.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/reset_password.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )


# ======================================================
# DANG NHAP GOOGLE (OAuth qua Supabase)
# ======================================================

@router.get("/auth/callback", response_class=HTMLResponse)
async def auth_callback_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/callback.html",
    )


class SetSessionRequest(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/auth/set-session")
async def set_session(payload: SetSessionRequest):
    try:
        user_result = supabase.auth.get_user(payload.access_token)
    except Exception as e:
        print("LOI XAC THUC GOOGLE:", e)
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

    if user_result is None or user_result.user is None:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

    response = JSONResponse({"success": True})
    response.set_cookie(
        key="sb_access_token",
        value=payload.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    response.set_cookie(
        key="sb_refresh_token",
        value=payload.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )
    return response

# ======================================================
# REGISTER STUDENT
# ======================================================

@router.post("/register/student")
async def register_student(
    request: Request,
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):

    try:

        supabase_service.sign_up(
            fullname=fullname,
            email=email,
            password=password,
        )

        return RedirectResponse(
            "/login",
            status_code=303
        )

    except Exception as e:

        print(type(e))
        print(e)

        return templates.TemplateResponse(
            "auth/register_student.html",
            {
                "request": request,
                "error": str(e),
                "fullname": fullname,
                "email": email,
                "supabase_url": SUPABASE_URL,
                "supabase_anon_key": SUPABASE_KEY,
            }
        )
    
# ======================================================
# REGISTER TEACHER (that - thay cho trang "Coming soon" cu)
#
# Khac dang ky hoc sinh o 2 diem:
#   1. Phai nhap dung MA MOI (bien moi truong MA_MOI_GIAO_VIEN trong
#      .env tren VPS). Day la cach don gian nhat de hoc sinh khong tu
#      dang ky thanh giao vien ma khong phai dung luong duyet tai khoan.
#   2. Khong co nut "Dang ky bang Google": luong Google khong mang theo
#      duoc ma moi, nen tai khoan giao vien phai tao bang email + mat khau.
#      Sau khi co tai khoan, van dang nhap bang Google binh thuong neu
#      email trung.
# Xem docs/21_TAI_KHOAN_GIAO_VIEN.md.
# ======================================================

@router.get("/register/teacher", response_class=HTMLResponse)
async def register_teacher_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/register_teacher.html",
    )


@router.post("/register/teacher")
async def register_teacher(
    request: Request,
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    ma_moi: str = Form(...),
    truong: str | None = Form(default=None),
    to_chuyen_mon: str | None = Form(default=None),
):

    def bao_loi(thong_bao: str):
        return templates.TemplateResponse(
            "auth/register_teacher.html",
            {
                "request": request,
                "error": thong_bao,
                "fullname": fullname,
                "email": email,
                "truong": truong,
                "to_chuyen_mon": to_chuyen_mon,
            },
        )

    if password != confirm_password:
        return bao_loi("Mat khau xac nhan khong khop.")

    if not MA_MOI_GIAO_VIEN:
        return bao_loi(
            "He thong chua bat dang ky giao vien (thieu MA_MOI_GIAO_VIEN "
            "trong .env). Lien he quan tri."
        )

    if ma_moi.strip() != MA_MOI_GIAO_VIEN:
        return bao_loi("Ma moi khong dung.")

    try:
        ket_qua = supabase_service.sign_up(
            fullname=fullname,
            email=email,
            password=password,
            vai_tro="giao_vien",
            truong=truong,
            to_chuyen_mon=to_chuyen_mon,
        )
    except Exception as e:
        print("LOI DANG KY GIAO VIEN:", type(e), e)
        return bao_loi(str(e))

    # Dat vai_tro mot lan nua o tang ung dung: khong phu thuoc vao viec
    # trigger handle_new_user da duoc sua de doc key "vai_tro" hay chua.
    user = getattr(ket_qua, "user", None)
    if user is not None and getattr(user, "id", None):
        profile_service.dat_vai_tro(user.id, "giao_vien")

    return RedirectResponse("/login", status_code=303)


@router.get("/teacher-coming-soon", response_class=HTMLResponse)
async def teacher_coming_soon(request: Request):
    """Duong dan cu - giu lai de link cu khong chet, chuyen sang trang that."""
    return RedirectResponse("/register/teacher", status_code=303)

