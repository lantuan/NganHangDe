import unicodedata

FILE = "app/routers/auth.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# Trang /register/student can supabase_url/supabase_anon_key de nut
# "Dang ky bang Google" (Supabase JS client-side) hoat dong, giong /login.
old_block = '''@router.get("/register/student", response_class=HTMLResponse)
async def register_student_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register_student.html",
    )'''

assert content.count(old_block) == 1, "Khong tim thay route /register/student."

new_block = '''@router.get("/register/student", response_class=HTMLResponse)
async def register_student_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register_student.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )'''

# Trang loi khi POST /register/student that bai cung phai co du
# supabase_url/supabase_anon_key, khong thi nut Google se bi
# createClient("", "") vo tac dung khi hien loi tren cung trang.
old_error_block = '''        return templates.TemplateResponse(
            "auth/register_student.html",
            {
                "request": request,
                "error": str(e),
                "fullname": fullname,
                "email": email,
            }
        )'''

assert content.count(old_error_block) == 1, "Khong tim thay khoi render loi register_student."

new_error_block = '''        return templates.TemplateResponse(
            "auth/register_student.html",
            {
                "request": request,
                "error": str(e),
                "fullname": fullname,
                "email": email,
                "supabase_url": SUPABASE_URL,
                "supabase_anon_key": SUPABASE_KEY,
            }
        )'''

content = content.replace(old_error_block, new_error_block)

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
