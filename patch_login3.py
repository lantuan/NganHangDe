import unicodedata

FILE = "app/templates/auth/login.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Title
old_title = '<title>Đăng nhập | Ngân Hàng Đề</title>'
new_title = '<title>Đăng nhập | Ngân Hàng Đề AI</title>'
assert content.count(old_title) == 1, "Khong tim thay title."
content = content.replace(old_title, new_title)

# 2. Logo header -> doi ten AI (da bam duoc ve trang chu tu Version 2.10)
old_logo = '<a href="/" class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề</a>'
new_logo = '<a href="/" class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề AI</a>'
assert content.count(old_logo) == 1, "Khong tim thay logo header."
content = content.replace(old_logo, new_logo)

# 3. Loi chao -> doi ten AI
old_greet = 'Chào mừng bạn quay lại với Ngân Hàng Đề.'
new_greet = 'Chào mừng bạn quay lại với Ngân Hàng Đề AI.'
assert content.count(old_greet) == 1, "Khong tim thay loi chao."
content = content.replace(old_greet, new_greet)

# 4. Footer ban quyen -> doi ten AI, bo trung chu "AI"
old_footer = '<p class="font-label-sm text-label-sm text-outline">© 2024 Ngân Hàng Đề. Nền tảng toán học AI hàng đầu Việt Nam.</p>'
new_footer = '<p class="font-label-sm text-label-sm text-outline">© 2024 Ngân Hàng Đề AI. Nền tảng toán học thông minh hàng đầu Việt Nam.</p>'
assert content.count(old_footer) == 1, "Khong tim thay footer ban quyen."
content = content.replace(old_footer, new_footer)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
