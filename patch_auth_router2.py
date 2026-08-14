import unicodedata

FILE = "app/routers/auth.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)

goc = len(content)

anchor = '''# ======================================================
# LOGOUT
# ======================================================

@router.get("/logout")
async def logout():
    response = RedirectResponse(
        "/login",
        status_code=303,
    )
    response.delete_cookie("sb_access_token")
    response.delete_cookie("sb_refresh_token")
    return response'''

assert content.count(anchor) == 1, "Khong tim thay khoi LOGOUT."

new_block = anchor + '''


# ======================================================
# QUEN MAT KHAU (gui email dat lai mat khau qua Supabase)
# ======================================================

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/forgot_password.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/reset_password.html",
        context={
            "supabase_url": SUPABASE_URL,
            "supabase_anon_key": SUPABASE_KEY,
        },
    )'''

content = content.replace(anchor, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
