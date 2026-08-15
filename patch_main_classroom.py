import unicodedata

FILE = "app/main.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_block = '''from app.routers import data

from app.routers import exam

app = FastAPI(title="Ngân Hàng Đề AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(chat.router)

app.include_router(data.router)

app.include_router(exam.router)'''

assert content.count(old_block) == 1, "Khong tim thay noi dung goc main.py (phan include_router)."

new_block = '''from app.routers import data

from app.routers import exam

from app.routers import classroom

app = FastAPI(title="Ngân Hàng Đề AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(chat.router)

app.include_router(data.router)

app.include_router(exam.router)

app.include_router(classroom.router)'''

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
