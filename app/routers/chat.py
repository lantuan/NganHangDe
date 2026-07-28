from pathlib import Path
import uuid

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

N8N_WEBHOOK_URL = "https://fqrpl.n8npanel.com/webhook-test/chat"

# Nơi lưu file (PDF/TEX/ZIP) do n8n trả về, để Frontend tải qua /static
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

    r = requests.post(
        N8N_WEBHOOK_URL,
        json={"message": message},
        timeout=120,
    )

    print(r.status_code)

    content_type = r.headers.get("content-type", "").split(";")[0].strip()

    # n8n trả JSON bình thường (câu trả lời chat thường, không sinh đề)
    if content_type == "application/json":
        return r.json()

    # n8n trả file nhị phân (PDF/TEX/ZIP từ /api/exam/generate-pdf-auto)
    if content_type in _EXT_THEO_CONTENT_TYPE:
        ext = _EXT_THEO_CONTENT_TYPE[content_type]
        filename = f"{uuid.uuid4().hex[:10]}.{ext}"
        file_path = DOWNLOAD_DIR / filename
        file_path.write_bytes(r.content)

        return {
            "success": True,
            "message": "Đã tạo đề xong.",
            "data": {
                "type": "file",
                "url": f"/static/downloads/{filename}",
                "filename": filename,
            },
        }

    # Trường hợp lạ khác (n8n lỗi, trả HTML/text...) — không để 500 lặng lẽ
    print("LOI CHAT: content-type khong xac dinh ->", content_type)
    print(r.text[:1000])
    return {
        "success": False,
        "message": "Không hiểu phản hồi từ n8n.",
        "data": None,
    }
