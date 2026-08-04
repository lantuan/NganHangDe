from pathlib import Path
import uuid

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

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
    return templates.TemplateResponse(
        request=request,
        name="chat/chat.html",
        context={
            "title": "Chat AI",
        },
    )


@router.post("/chat")
async def chat_post(
    message: str = Form(...)
):
    print("========== CHAT ==========")
    print(message)
    print("==========================")

    try:
        r = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": message},
            timeout=240,
        )
    except requests.exceptions.Timeout:
        print("LOI CHAT: n8n qua thoi gian cho (240s)")
        return {
            "success": False,
            "message": "AI xu ly qua lau (qua 4 phut), vui long thu lai.",
            "data": None,
        }
    except requests.exceptions.RequestException as e:
        print("LOI CHAT: khong ket noi duoc n8n ->", e)
        return {
            "success": False,
            "message": "Khong ket noi duoc voi AI, vui long thu lai.",
            "data": None,
        }

    print(r.status_code)

    content_type = r.headers.get("content-type", "").split(";")[0].strip()

    # n8n tra JSON binh thuong (cau tra loi chat thuong, khong sinh de)
    if content_type == "application/json":
        return r.json()

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
