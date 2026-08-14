import unicodedata

FILE = "app/routers/chat.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Import them lop_config + supabase_service (dung de doc/ghi khoi/lop)
old_imports = '''from app.core.deps import get_current_user
from app.services import history_service'''
assert content.count(old_imports) == 1, "Khong tim thay khoi import."

new_imports = '''from app.core.deps import get_current_user
from app.core.lop_config import DANH_SACH_LOP
from app.services import history_service
from app.services import supabase_service'''
content = content.replace(old_imports, new_imports)

# 2. GET /chat: chan lai neu hoc sinh chua chon lop, dua ve /chon-lop.
#    Con da chon roi thi truyen them khoi/lop de hien trong account-badge.
old_chat_route = '''@router.get("/chat", response_class=HTMLResponse)
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
assert content.count(old_chat_route) == 1, "Khong tim thay route /chat (GET)."

new_chat_route = '''@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    ho_so = supabase_service.lay_lop_hoc_sinh(user.id)
    if not ho_so or not ho_so.get("lop"):
        return RedirectResponse("/chon-lop", status_code=303)

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
            "user_khoi": ho_so.get("khoi"),
            "user_lop": ho_so.get("lop"),
        },
    )


@router.get("/chon-lop", response_class=HTMLResponse)
async def chon_lop_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="chat/chon_lop.html",
        context={
            "danh_sach_lop": DANH_SACH_LOP,
        },
    )


@router.post("/chon-lop")
async def chon_lop_submit(request: Request, lop_full: str = Form(...)):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    if "-" not in lop_full:
        return RedirectResponse("/chon-lop", status_code=303)

    khoi, lop = lop_full.split("-", 1)
    if khoi not in DANH_SACH_LOP or lop not in DANH_SACH_LOP[khoi]:
        return RedirectResponse("/chon-lop", status_code=303)

    supabase_service.cap_nhat_lop_hoc_sinh(user.id, khoi, lop)
    return RedirectResponse("/chat", status_code=303)'''

content = content.replace(old_chat_route, new_chat_route)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
