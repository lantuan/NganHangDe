from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from fastapi import Form

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


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
        "https://fqrpl.n8npanel.com/webhook-test/chat",
        json={"message": message},
        timeout=120,
    )

    print(r.status_code)
    print(r.text)

    return r.json()