import unicodedata

FILE = "app/templates/auth/forgot_password.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_title = '<title>Quên mật khẩu | Ngân Hàng Đề</title>'
new_title = '<title>Quên mật khẩu | Ngân Hàng Đề AI</title>'
assert content.count(old_title) == 1, "Khong tim thay title."
content = content.replace(old_title, new_title)

old_logo = '<a href="/" class="text-xl font-bold text-primary">Ngân Hàng Đề</a>'
new_logo = '<a href="/" class="text-xl font-bold text-primary">Ngân Hàng Đề AI</a>'
assert content.count(old_logo) == 1, "Khong tim thay logo."
content = content.replace(old_logo, new_logo)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
