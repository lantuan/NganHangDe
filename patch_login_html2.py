import unicodedata

FILE = "app/templates/auth/login.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)

goc = len(content)

# 1. Logo "Ngan Hang De" tren header -> bam vao ve trang chu "/"
old_logo = '<div class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề</div>'
new_logo = '<a href="/" class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề</a>'

assert content.count(old_logo) == 1, "Khong tim thay logo header."
content = content.replace(old_logo, new_logo)

# 2. "Quen mat khau?" -> tro toi trang /forgot-password that
old_forgot = '<a class="font-label-md text-label-md text-primary hover:underline" href="#">Quên mật khẩu?</a>'
new_forgot = '<a class="font-label-md text-label-md text-primary hover:underline" href="/forgot-password">Quên mật khẩu?</a>'

assert content.count(old_forgot) == 1, "Khong tim thay link Quen mat khau."
content = content.replace(old_forgot, new_forgot)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
