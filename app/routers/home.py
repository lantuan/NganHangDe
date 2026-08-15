from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.deps import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Trang chu truoc day khong biet nguoi dung da dang nhap hay chua
    # (khong doc cookie), nen luon hien nut "Dang nhap" du phien van
    # con hop le - gay cam giac "bi dang xuat" khi bam ve trang chu.
    # Nay kiem tra phien nhu /chat, truyen da_dang_nhap de index.html
    # doi nut "Dang nhap" -> "Vao Chat" khi da dang nhap.
    user = get_current_user(request)

    ten_hien_thi = None
    if user is not None:
        metadata = user.user_metadata or {}
        ten_hien_thi = (
            metadata.get("fullname")
            or metadata.get("full_name")
            or metadata.get("name")
            or user.email
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "da_dang_nhap": user is not None,
            "user_display_name": ten_hien_thi,
        },
    )