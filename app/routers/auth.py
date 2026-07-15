from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase_auth.errors import AuthApiError
from app.services import supabase_service

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
):
    print("===== LOGIN =====")
    print(email)

    try:

        result = supabase_service.sign_in(
            email=email,
            password=password,
        )

        print(result)

        if result.user is None:
            return RedirectResponse(
                "/login",
                status_code=303,
            )

        return RedirectResponse(
            "/chat",
            status_code=303,
        )

    except Exception as e:
        print("LOI LOGIN:", e)
        raise

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

