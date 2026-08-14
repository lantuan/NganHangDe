import unicodedata

FILE = "app/templates/auth/register.html"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# 1. Title
old_title = '<title>Đăng ký - Ngân Hàng Đề</title>'
new_title = '<title>Đăng ký - Ngân Hàng Đề AI</title>'
assert content.count(old_title) == 1, "Khong tim thay title."
content = content.replace(old_title, new_title)

# 2. Logo ben trai (nav) -> bam ve trang chu, doi ten AI
old_logo1 = '<div class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề</div>'
new_logo1 = '<a href="/" class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề AI</a>'
assert content.count(old_logo1) == 1, "Khong tim thay logo nav trai."
content = content.replace(old_logo1, new_logo1)

# 3. Logo mobile -> bam ve trang chu, doi ten AI
old_logo2 = '<span class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề</span>'
new_logo2 = '<a href="/" class="text-headline-sm font-headline-lg text-primary tracking-tight">Ngân Hàng Đề AI</a>'
assert content.count(old_logo2) == 1, "Khong tim thay logo mobile."
content = content.replace(old_logo2, new_logo2)

# 4. Footer ban quyen -> doi ten AI
old_footer = '<span class="font-label-sm text-label-sm">© 2024 Ngân Hàng Đề</span>'
new_footer = '<span class="font-label-sm text-label-sm">© 2024 Ngân Hàng Đề AI</span>'
assert content.count(old_footer) == 1, "Khong tim thay footer ban quyen."
content = content.replace(old_footer, new_footer)

# 4b. Dieu khoan dich vu o Step 2 (dead code, khong hien thi nhung sua
#     cho dong bo ten thuong hieu)
old_terms = 'của Ngân Hàng Đề.'
new_terms = 'của Ngân Hàng Đề AI.'
assert content.count(old_terms) == 1, "Khong tim thay dong dieu khoan dich vu."
content = content.replace(old_terms, new_terms)

# 5. Bo nut "Tiep tuc" (khong co tac dung)
old_next_btn = '''<button class="w-full h-14 rounded-[16px] bg-primary text-on-primary font-label-md text-headline-sm shadow-lg shadow-primary/20 hover:opacity-90 active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none" disabled="" id="next-btn" onclick="nextStep()">
                            Tiếp tục
                        </button>
'''
assert content.count(old_next_btn) == 1, "Khong tim thay nut Tiep tuc."
content = content.replace(old_next_btn, '')

# 6. Link "Dang nhap" o footer -> tro toi /login that
old_login_link = '<a class="text-primary font-bold hover:underline" href="#">Đăng nhập</a>'
new_login_link = '<a class="text-primary font-bold hover:underline" href="/login">Đăng nhập</a>'
assert content.count(old_login_link) == 1, "Khong tim thay link Dang nhap footer."
content = content.replace(old_login_link, new_login_link)

# 7. Them hieu ung hover doi mau thanh chi bao giua nut Hoc sinh / Giao vien
old_prevstep_end = '''            indicator2.classList.replace('bg-primary', 'bg-secondary-container');
        }
    </script>'''
assert content.count(old_prevstep_end) == 1, "Khong tim thay cuoi ham prevStep."
new_prevstep_end = '''            indicator2.classList.replace('bg-primary', 'bg-secondary-container');
        }

        // Hover doi mau thanh chi bao giua nut Hoc sinh / Giao vien
        (function () {
            var indicator1 = document.getElementById('step-indicator-1');
            var indicator2 = document.getElementById('step-indicator-2');
            var roleStudentBtn = document.getElementById('role-student');
            var roleTeacherBtn = document.getElementById('role-teacher');

            function chonThanhChiBao(ben) {
                if (!indicator1 || !indicator2) return;
                if (ben === 'student') {
                    indicator1.classList.remove('bg-secondary-container');
                    indicator1.classList.add('bg-primary');
                    indicator2.classList.remove('bg-primary');
                    indicator2.classList.add('bg-secondary-container');
                } else if (ben === 'teacher') {
                    indicator1.classList.remove('bg-primary');
                    indicator1.classList.add('bg-secondary-container');
                    indicator2.classList.remove('bg-secondary-container');
                    indicator2.classList.add('bg-primary');
                }
            }

            if (roleStudentBtn) {
                roleStudentBtn.addEventListener('mouseenter', function () { chonThanhChiBao('student'); });
            }
            if (roleTeacherBtn) {
                roleTeacherBtn.addEventListener('mouseenter', function () { chonThanhChiBao('teacher'); });
            }
        })();
    </script>'''
content = content.replace(old_prevstep_end, new_prevstep_end)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
