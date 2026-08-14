from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from supabase_auth.errors import AuthApiError
from pydantic import BaseModel
from app.services import supabase_service
from app.core.config import SUPABASE_URL, SUPABASE_KEY
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
    )


# ======================================================
# REGISTER TEACHER PAGE
# ======================================================

@router.get("/register/teacher", response_class=HTMLResponse)
async def register_teacher_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register_teacher.html",
    )

# ======================================================
# POST /login
# ======================================================

@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    remember: str | None = Form(default=None),
):
    print("===== LOGIN =====")
    print(email, "| remember:", bool(remember))

    try:

        result = supabase_service.sign_in(
            email=email,
            password=password,
        )

        print(result)

        if result.user is None or result.session is None:
            return RedirectResponse(
                "/login",
                status_code=303,
            )

        response = RedirectResponse(
            "/chat",
            status_code=303,
        )

        if remember:
            access_max_age = 60 * 60 * 24 * 7
            refresh_max_age = 60 * 60 * 24 * 30
        else:
            access_max_age = None
            refresh_max_age = None

        response.set_cookie(
            key="sb_access_token",
            value=result.session.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=access_max_age,
        )
        response.set_cookie(
            key="sb_refresh_token",
            value=result.session.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=refresh_max_age,
        )
        return response

    except Exception as e:
        print("LOI LOGIN:", e)
        raise


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
        raise HTTPException(status_code=401, detail="Token khong hop le")

    if user_result is None or user_result.user is None:
        raise HTTPException(status_code=401, detail="Token khong hop le")

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
            }
        )
    
# ======================================================
# TEACHER (Coming soon)
# ======================================================

@router.get("/teacher-coming-soon", response_class=HTMLResponse)
async def teacher_coming_soon(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/teacher_coming_soon.html",
    )

