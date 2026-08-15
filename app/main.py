from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.routers import home
from app.routers import auth
from app.routers import chat

from app.routers import auth
from app.routers import chat

from app.routers import data

from app.routers import exam

from app.routers import classroom

app = FastAPI(title="Ngân Hàng Đề AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(chat.router)

app.include_router(data.router)

app.include_router(exam.router)

app.include_router(classroom.router)


@app.middleware("http")
async def lam_moi_cookie_phien(request: Request, call_next):
    """
    app/core/deps.py::get_current_user() tu dong lam moi phien bang
    refresh_token khi access_token (JWT Supabase, mac dinh het han sau
    ~1 gio) da het han, va luu phien moi vao request.state.new_session.
    Middleware nay chay sau MOI request - neu route vua roi co goi
    get_current_user() va no vua tu lam moi phien, ghi lai 2 cookie
    sb_access_token/sb_refresh_token moi vao response. Neu khong co gi
    duoc lam moi (nguoi dung chua dang nhap, hoac access_token van con
    han, hoac ca 2 token deu het han that su), response giu nguyen,
    khong lam gi them.
    """
    response = await call_next(request)

    new_session = getattr(request.state, "new_session", None)
    if new_session is not None:
        response.set_cookie(
            key="sb_access_token",
            value=new_session.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
        )
        response.set_cookie(
            key="sb_refresh_token",
            value=new_session.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30,
        )

    return response