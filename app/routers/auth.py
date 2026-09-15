from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from supabase_auth.errors import AuthApiError
from pydantic import BaseModel
from app.services import supabase_service, profile_service
from app.core.config import SUPABASE_URL, SUPABASE_KEY, MA_MOI_GIAO_VIEN
from app.core.deps import get_current_user
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

def _trang_login_loi(request: Request, email: str, thong_bao: str):
    """Hien lai trang dang nhap kem thong bao loi (KHONG tra 500)."""
    # LUU Y: PHAI dung dang tham so co ten (request=..., name=..., context=...).
    # Ban Starlette dang chay tren VPS da BO cach goi cu
    # TemplateResponse("ten.html", {...}) - no coi tham so dau la request va
    # tham so thu hai la ten tep, nen cai dict lot vao cho ten tep va nem
    # "TypeError: unhashable type: 'dict'" -> ra trang trang 500.
    # Gap that ngay 15/09/2026, xem docs/16_CHANGELOG.md Version 2.49.
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "error": thong_bao,
            "email": email,
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
        # ngoai khong do duoc email nao da co tai khoan tren he thong. Vi
        # vay thong bao phai gop ca hai kha nang lam mot, khong the noi ro
        # la "tai khoan khong ton tai". Trang dang nhap da co san 2 cho dan
        # sang /register (thanh tren cung va dong "Chua co tai khoan?" o
        # duoi), nen o bao loi khong can them nut nao nua.
        return _trang_login_loi(
            request, email,
            "Tài khoản không tồn tại hoặc mật khẩu không đúng.",
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
            "Tài khoản không tồn tại hoặc mật khẩu không đúng.",
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

    # Dang nhap bang Google khong co o tick "Ghi nho dang nhap", va o tren
    # da dat han 7/30 ngay - tuc la MAC DINH ghi nho. Phai ghi ca cookie
    # sb_ghi_nho cho khop, neu khong middleware lam_moi_cookie_phien
    # (app/main.py) se thay thieu cookie nay, hieu la "khong ghi nho", va
    # bien 2 cookie tren thanh cookie phien ngay lan lam moi dau tien ->
    # nguoi dang nhap bang Google bi dang xuat khi dong trinh duyet.
    response.set_cookie(
        key="sb_ghi_nho",
        value="1",
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
            request=request,
            name="auth/register_student.html",
            context={
                "error": str(e),
                "fullname": fullname,
                "email": email,
                "supabase_url": SUPABASE_URL,
                "supabase_anon_key": SUPABASE_KEY,
            },
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
            request=request,
            name="auth/register_teacher.html",
            context={
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


# ======================================================
# CHON VAI TRO - man hinh hien NGAY sau khi dang nhap lan dau
#
# Vi sao can: dang nhap bang Google khong di qua trang dang ky nen khong
# he duoc hoi la hoc sinh hay giao vien -> truoc day roi thang vao "Chon
# lop cua em", giao vien khong hieu tai sao. Ban dau chi them mot dong
# chu nho o cuoi trang Chon lop, nhung giao vien phan hoi dung: khong ai
# doc dong chu nho do, va cung khong ai biet trang web nay CO phan vai
# tro. Nen phai la mot man hinh chon hai o to, giong het trang dang ky.
#
# Phan biet "chua duoc hoi" voi "da chon hoc sinh" bang vai_tro =
# 'chua_chon' (mac dinh moi cua cot, xem sql/23_chon_vai_tro.sql).
# ======================================================

@router.get("/chon-vai-tro", response_class=HTMLResponse)
async def chon_vai_tro_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    vai_tro = profile_service.lay_vai_tro(user.id)
    if vai_tro in profile_service.VAI_TRO_GIAO_VIEN:
        return RedirectResponse("/gv", status_code=303)
    if vai_tro == "hoc_sinh":
        return RedirectResponse("/chon-lop", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="auth/chon_vai_tro.html",
        context={"email": user.email},
    )


@router.post("/chon-vai-tro")
async def chon_vai_tro(request: Request, vai_tro: str = Form(...)):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    if vai_tro == "giao_vien":
        # CHUA nang vai tro o day - phai nhap dung ma moi da. Giu nguyen
        # 'chua_chon' de ai bo ngang giua chung thi lan sau vao van duoc
        # hoi lai, khong bi ket o vai tro hoc sinh.
        return RedirectResponse("/toi-la-giao-vien", status_code=303)

    if vai_tro == "hoc_sinh":
        if not profile_service.dat_vai_tro(user.id, "hoc_sinh"):
            return templates.TemplateResponse(
                request=request,
                name="auth/chon_vai_tro.html",
                context={"email": user.email,
                         "error": "Không lưu được lựa chọn, thử lại sau ít phút."},
                status_code=500,
            )
        return RedirectResponse("/chon-lop", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="auth/chon_vai_tro.html",
        context={"email": user.email, "error": "Vai trò không hợp lệ."},
        status_code=400,
    )


# ======================================================
# "TOI LA GIAO VIEN" - nang tai khoan DANG DANG NHAP len giao vien
#
# Vi sao can trang nay: nut "Dang nhap bang Google" khong di qua
# /register/teacher nen khong co cho nhap ma moi, va cung khong hoi vai
# tro -> moi tai khoan Google deu thanh hoc sinh roi bi hoi chon lop.
# Trang nay cho nguoi DA dang nhap (bang Google hay mat khau deu duoc)
# nhap ma moi de tu nang minh len giao vien. Dung duoc ca cho tai khoan
# cu da tro thanh hoc sinh, khong phai xoa di dang ky lai.
#
# Dat o auth.py (KHONG phai teacher.py) vi teacher.py chan het nguoi
# chua phai giao vien - ma trang nay thi danh cho dung nhung nguoi do.
# ======================================================

@router.get("/toi-la-giao-vien", response_class=HTMLResponse)
async def toi_la_giao_vien_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    # Da la giao vien roi thi vao thang khu lam viec, khoi nhap lai ma.
    if profile_service.la_giao_vien(user.id):
        return RedirectResponse("/gv", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="auth/toi_la_giao_vien.html",
        context={"email": user.email},
    )


@router.post("/toi-la-giao-vien")
async def toi_la_giao_vien(request: Request, ma_moi: str = Form(...)):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    def bao_loi(thong_bao: str):
        return templates.TemplateResponse(
            request=request,
            name="auth/toi_la_giao_vien.html",
            context={"error": thong_bao, "email": user.email},
            status_code=400,
        )

    if not MA_MOI_GIAO_VIEN:
        return bao_loi(
            "Hệ thống chưa bật chức năng này (thiếu mã mời trong cấu hình). "
            "Liên hệ quản trị."
        )

    if ma_moi.strip() != MA_MOI_GIAO_VIEN:
        # Ghi log de biet co ai do dang thu mo ma.
        print(f"MA MOI SAI - tai khoan {user.email} thu ma: {ma_moi.strip()[:40]}")
        return bao_loi("Mã mời không đúng.")

    if not profile_service.dat_vai_tro(user.id, "giao_vien"):
        return bao_loi("Không ghi được vai trò, thử lại sau ít phút.")

    print(f"DA NANG LEN GIAO VIEN: {user.email}")
    return RedirectResponse("/gv", status_code=303)


@router.get("/teacher-coming-soon", response_class=HTMLResponse)
async def teacher_coming_soon(request: Request):
    """Duong dan cu - giu lai de link cu khong chet, chuyen sang trang that."""
    return RedirectResponse("/register/teacher", status_code=303)

