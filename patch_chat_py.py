import unicodedata

FILE = "app/routers/chat.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# GET /chat can truyen them ten hien thi + email cua nguoi dang nhap de
# template hien badge tai khoan (biet dang dung tai khoan nao khi lam bai).
old_block = '''@router.get("/chat", response_class=HTMLResponse)
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
    )'''
assert content.count(old_block) == 1, "Khong tim thay route /chat (GET)."

new_block = '''@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    metadata = user.user_metadata or {}
    ten_hien_thi = (
        metadata.get("fullname")
        or metadata.get("full_name")
        or metadata.get("name")
        or user.email
    )

    return templates.TemplateResponse(
        request=request,
        name="chat/chat.html",
        context={
            "title": "Chat AI",
            "user_email": user.email,
            "user_display_name": ten_hien_thi,
        },
    )'''

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
