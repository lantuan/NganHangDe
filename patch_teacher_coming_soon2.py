import unicodedata

FILE = "app/templates/auth/teacher_coming_soon.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Bo nav "Tinh nang / Bang gia / Huong dan" (link chet href="#")
old_nav = '''<nav class="hidden md:flex items-center gap-stack-lg">
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary-container transition-colors" href="#">Tính năng</a>
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary-container transition-colors" href="#">Bảng giá</a>
<a class="font-label-md text-label-md text-on-surface-variant hover:text-primary-container transition-colors" href="#">Hướng dẫn</a>
</nav>
'''
assert content.count(old_nav) == 1, "Khong tim thay nav Tinh nang/Bang gia/Huong dan."
content = content.replace(old_nav, '')

# 2. Nut Dang nhap / Dang ky -> tro dung ve /login, /register
old_buttons = '''<button class="px-stack-lg py-stack-sm font-label-md text-label-md text-primary-container border border-primary-container rounded-full hover:bg-surface-container transition-all">Đăng nhập</button>
<button class="px-stack-lg py-stack-sm font-label-md text-label-md bg-primary-container text-on-primary-container rounded-full hover:opacity-90 transition-all">Đăng ký</button>'''
assert content.count(old_buttons) == 1, "Khong tim thay nut Dang nhap/Dang ky."
new_buttons = '''<a href="/login" class="inline-block px-stack-lg py-stack-sm font-label-md text-label-md text-primary-container border border-primary-container rounded-full hover:bg-surface-container transition-all">Đăng nhập</a>
<a href="/register" class="inline-block px-stack-lg py-stack-sm font-label-md text-label-md bg-primary-container text-on-primary-container rounded-full hover:opacity-90 transition-all">Đăng ký</a>'''
content = content.replace(old_buttons, new_buttons)

# 3. Logo "Ngan Hang De AI" goc trai -> bam ve trang chu "/"
old_logo = '<div class="font-headline-md text-headline-md font-bold text-primary-container">Ngân Hàng Đề AI</div>'
new_logo = '<a href="/" class="font-headline-md text-headline-md font-bold text-primary-container">Ngân Hàng Đề AI</a>'
assert content.count(old_logo) == 1, "Khong tim thay logo header."
content = content.replace(old_logo, new_logo)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
