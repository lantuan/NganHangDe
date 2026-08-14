import unicodedata

FILE = "app/routers/auth.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)

goc = len(content)

old_imports = '''from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase_auth.errors import AuthApiError
from app.services import supabase_service

router = APIRouter()'''

new_imports = '''from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from supabase_auth.errors import AuthApiError
from pydantic import BaseModel
from app.services import supabase_service
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from app.core.supabase import supabase

router = APIRouter()'''

assert content.count(old_imports) == 1, "Khong tim thay khoi import dau file."
content = content.replace(old_imports, new_imports)

old_login_page = '''@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
    )'''

new_login_page = '''@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )'''

assert content.count(old_login_page) == 1, "Khong tim thay route GET /login."
content = content.replace(old_login_page, new_login_page)

old_login_post = '''@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
):
    print("===== LOGIN =====")
    print(email)

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
        response.set_cookie(
            key="sb_access_token",
            value=result.session.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
        )
        response.set_cookie(
            key="sb_refresh_token",
            value=result.session.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30,
        )
        return response

    except Exception as e:
        print("LOI LOGIN:", e)
        raise'''

new_login_post = '''@router.post("/login")
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
        raise'''

assert content.count(old_login_post) == 1, "Khong tim thay route POST /login."
content = content.replace(old_login_post, new_login_post)

anchor = '''# ======================================================
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
    return response'''

assert content.count(anchor) == 1, "Khong tim thay khoi LOGOUT."

new_block = anchor + '''


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
    return response'''

content = content.replace(anchor, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
