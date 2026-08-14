import unicodedata

FILE = "app/templates/auth/callback.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_title = '<title>Đang đăng nhập... | Ngân Hàng Đề</title>'
new_title = '<title>Đang đăng nhập... | Ngân Hàng Đề AI</title>'
assert content.count(old_title) == 1, "Khong tim thay title."
content = content.replace(old_title, new_title)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
