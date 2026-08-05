from pathlib import Path
import uuid

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
import requests

from app.core.deps import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

N8N_WEBHOOK_URL = "https://fqrpl.n8npanel.com/webhook/chat"

# Noi luu file (PDF/TEX/ZIP) do n8n tra ve, de Frontend tai qua /static
DOWNLOAD_DIR = Path("app/static/downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

_EXT_THEO_CONTENT_TYPE = {
    "application/pdf": "pdf",
    "application/zip": "zip",
    "application/x-tex": "tex",
}


@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="chat/chat.html",
        context={
            "title": "Chat AI",
        },
    )


def _goi_n8n(message: str):
    """Ham dong bo (blocking) - se duoc chay trong threadpool rieng,
    khong chan event loop chinh cua uvicorn trong luc cho n8n xu ly lau."""
    return requests.post(
        N8N_WEBHOOK_URL,
        json={"message": message},
        timeout=300,
    )


@router.post("/chat")
async def chat_post(
    request: Request,
    message: str = Form(...),
):
    user = get_current_user(request)
    if user is None:
        return {
            "success": False,
            "message": "Ban chua dang nhap hoac phien da het han. Vui long dang nhap lai.",
            "data": None,
            "need_login": True,
        }

    print("========== CHAT ==========")
    print(message)
    print("==========================")

    r = None
    loi_cuoi = None
    for lan_thu in range(2):
        try:
            r = await run_in_threadpool(_goi_n8n, message)
            break
        except requests.exceptions.Timeout as e:
            loi_cuoi = e
            print(f"LOI CHAT: n8n qua thoi gian cho (lan {lan_thu + 1}/2)")
        except requests.exceptions.RequestException as e:
            loi_cuoi = e
            print(f"LOI CHAT: khong ket noi duoc n8n (lan {lan_thu + 1}/2) ->", e)

    if r is None:
        return {
            "success": False,
            "message": "Khong ket noi duoc voi AI sau 2 lan thu, vui long thu lai.",
            "data": None,
        }

    print(r.status_code)

    content_type = r.headers.get("content-type", "").split(";")[0].strip()

    # n8n tra JSON binh thuong (cau tra loi chat thuong, khong sinh de)
    if content_type == "application/json":
        try:
            return r.json()
        except ValueError:
            print("LOI CHAT: n8n tra ve JSON rong/khong hop le. Body:", repr(r.text[:500]))
            return {
                "success": False,
                "message": "AI chua xu ly duoc yeu cau nay. Vui long thu lai voi yeu cau tao de cu the (lop/chuong/so cau...).",
                "data": None,
            }

    # n8n tra file nhi phan (PDF/TEX/ZIP tu /api/exam/generate-pdf-auto)
    if content_type in _EXT_THEO_CONTENT_TYPE:
        ext = _EXT_THEO_CONTENT_TYPE[content_type]
        filename = f"{uuid.uuid4().hex[:10]}.{ext}"
        file_path = DOWNLOAD_DIR / filename
        file_path.write_bytes(r.content)

        return {
            "success": True,
            "message": "Da tao de xong.",
            "data": {
                "type": "file",
                "url": f"/static/downloads/{filename}",
                "filename": filename,
            },
        }

    # Truong hop la khac (n8n loi, tra HTML/text...) - khong de 500 lang le
    print("LOI CHAT: content-type khong xac dinh ->", content_type)
    print(r.text[:1000])
    return {
        "success": False,
        "message": "Khong hieu phan hoi tu n8n.",
        "data": None,
    }
