from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import home
from app.routers import auth
from app.routers import chat

from app.routers import auth
from app.routers import chat

from app.routers import data

from app.routers import exam

from app.routers import classroom
from app.routers import teacher
from app.routers import gia_su

app = FastAPI(title="Ngân Hàng Đề AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.exception_handler(StarletteHTTPException)
async def xu_ly_khong_du_quyen(request: Request, exc: StarletteHTTPException):
    """
    Loi 403 (khong phai giao vien) truoc day tra ve JSON {"detail": ...} -
    nguoi dung chi thay mot dong chu kho hieu, khong biet tai sao minh bi
    chan va phai lam gi. Nay hien mot trang ro rang, co ghi VAI TRO HIEN
    TAI cua tai khoan va nut di tiep dung cho. Cac loi khac giu nguyen.
    """
    if exc.status_code == 403 and "text/html" in request.headers.get("accept", ""):
        from app.core.deps import get_current_user, lay_vai_tro
        user = get_current_user(request)
        return templates.TemplateResponse(
            request=request,
            name="auth/khong_du_quyen.html",
            context={
                "email": getattr(user, "email", None),
                "vai_tro": lay_vai_tro(request, user),
            },
            status_code=403,
        )
    return await http_exception_handler(request, exc)

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(chat.router)

app.include_router(data.router)

app.include_router(exam.router)

app.include_router(classroom.router)
app.include_router(teacher.router)
app.include_router(gia_su.router)


@app.middleware("http")
async def ngon_ngu_viet_anh(request: Request, call_next):
    """
    Việt / Anh (cô Lan 03/10/2026): trang HTML được chèn nút "Tiếng Việt | English" ở
    góc phải trên và, khi chọn tiếng Anh, dịch theo từ điển data/i18n (app/services/
    i18n_service.py). Thông báo JSON (message, detail, tra_loi...) cũng được dịch.
    Chữ chưa có trong từ điển giữ nguyên tiếng Việt.
    """
    from fastapi.responses import Response
    from app.services import i18n_service as i18n

    response = await call_next(request)
    loai = response.headers.get("content-type", "")
    la_html = loai.startswith("text/html")
    la_json = loai.startswith("application/json")
    if not (la_html or la_json) or request.url.path.startswith("/static"):
        return response
    ngon_ngu = i18n.lay_ngon_ngu(request)
    if la_json and ngon_ngu == "vi":
        return response

    body = b"".join([chunk async for chunk in response.body_iterator])
    try:
        text = body.decode("utf-8")
        if la_html:
            text = i18n.chen_nut_chuyen(i18n.dich_html(text, ngon_ngu), ngon_ngu)
        else:
            import json as _json
            text = _json.dumps(i18n.dich_json(_json.loads(text), ngon_ngu), ensure_ascii=False)
        body = text.encode("utf-8")
    except Exception as e:                       # khong bao gio lam hong trang vi dich loi
        print("I18N: bo qua, loi dich:", e)
    moi = Response(content=body, status_code=response.status_code)
    moi.raw_headers = [(k, v) for k, v in response.raw_headers if k.lower() != b"content-length"]
    moi.headers["content-length"] = str(len(body))
    if request.query_params.get("lang") in i18n.NGON_NGU:
        moi.set_cookie("lang", request.query_params["lang"], max_age=31536000, path="/", samesite="lax")
    return moi


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
        # SUA 2026-09-15: truoc day cho cung han 7/30 ngay o day, bat ke
        # nguoi dung co tick "Ghi nho dang nhap" hay khong -> lua chon dat
        # luc dang nhap (app/routers/auth.py::login) bi xoa sach ngay lan
        # lam moi phien dau tien. Nay doc cookie sb_ghi_nho de giu dung y
        # nguoi dung: co tick thi 7/30 ngay, khong tick thi cookie phien
        # (max_age=None - tat trinh duyet la mat).
        ghi_nho = request.cookies.get("sb_ghi_nho") == "1"
        han_access = 60 * 60 * 24 * 7 if ghi_nho else None
        han_refresh = 60 * 60 * 24 * 30 if ghi_nho else None

        response.set_cookie(
            key="sb_access_token",
            value=new_session.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=han_access,
        )
        response.set_cookie(
            key="sb_refresh_token",
            value=new_session.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=han_refresh,
        )

    return response