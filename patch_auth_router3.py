import unicodedata

FILE = "app/routers/auth.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_block = '''@router.get("/register/teacher", response_class=HTMLResponse)
async def register_teacher_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register_teacher.html",
    )'''

assert content.count(old_block) == 1, "Khong tim thay route /register/teacher."

new_block = '''@router.get("/register/teacher", response_class=HTMLResponse)
async def register_teacher_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/teacher_coming_soon.html",
    )'''

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
