import unicodedata

FILE = "app/templates/auth/register_student.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Sua URL Google Fonts Material Symbols bi loi cu phap (thieu axis "FILL")
#    -> khien font khong tai duoc, trinh duyet hien chu that "person"/"mail"/
#    "lock"/"lock_reset" thay vi icon, de chong len chu vi du (placeholder).
old_font_url = '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&amp;display=swap" rel="stylesheet"/>'
new_font_url = '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>'
assert content.count(old_font_url) == 1, "Khong tim thay link Material Symbols Outlined."
content = content.replace(old_font_url, new_font_url)

# 2. Title -> dung ten thuong hieu (truoc do la "QuizAI" con sot lai)
old_title = '<title>Đăng ký Học sinh | QuizAI</title>'
new_title = '<title>Đăng ký Học sinh | Ngân Hàng Đề AI</title>'
assert content.count(old_title) == 1, "Khong tim thay title."
content = content.replace(old_title, new_title)

# 3. Logo "Ngan Hang De AI" goc trai -> bam ve trang chu "/"
old_logo = '<div class="font-display text-[24px] md:text-[32px] font-bold text-primary-container">Ngân Hàng Đề AI</div>'
new_logo = '<a href="/" class="font-display text-[24px] md:text-[32px] font-bold text-primary-container">Ngân Hàng Đề AI</a>'
assert content.count(old_logo) == 1, "Khong tim thay logo header."
content = content.replace(old_logo, new_logo)

# 4. Bo nav "Tinh nang / Ve chung toi" (link chet href="#")
old_nav = '''<a class="hidden md:block text-on-surface-variant font-medium hover:text-primary-container transition-colors" href="#">Tính năng</a>
<a class="hidden md:block text-on-surface-variant font-medium hover:text-primary-container transition-colors" href="#">Về chúng tôi</a>
'''
assert content.count(old_nav) == 1, "Khong tim thay nav Tinh nang/Ve chung toi."
content = content.replace(old_nav, '')

# 5. Nut "Login" -> doi thanh "Dang nhap" va tro dung ve /login
old_login_btn = '''<button class="bg-primary-container text-white px-stack-lg py-stack-sm rounded-full font-semibold hover:opacity-90 transition-opacity">
                    Login
                </button>'''
assert content.count(old_login_btn) == 1, "Khong tim thay nut Login."
new_login_btn = '''<a href="/login" class="inline-block bg-primary-container text-white px-stack-lg py-stack-sm rounded-full font-semibold hover:opacity-90 transition-opacity">
                    Đăng nhập
                </a>'''
content = content.replace(old_login_btn, new_login_btn)

# 6. Placeholder email con sot ten mien cu "quizai.vn"
old_email_ph = 'placeholder="hocsinh@quizai.vn"'
new_email_ph = 'placeholder="hocsinh@email.com"'
assert content.count(old_email_ph) == 1, "Khong tim thay placeholder email."
content = content.replace(old_email_ph, new_email_ph)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
