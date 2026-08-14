import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

anchor = '''- CHUA kiem chung end-to-end (can nguoi dung tu bam thu gui email that
  tren production sau khi da them Redirect URL o tren).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.10."

addendum = '''


===============================================================================

Version 2.11

Ngày

2026-08-14

Nội dung

- register.html: logo "Ngan Hang De" o ca ben trai (desktop) va o giao
  dien mobile gio bam vao ve trang chu "/" (truoc do la <div>/<span>
  tinh, khong bam duoc); doi ten hien thi thanh "Ngan Hang De AI" cho
  dung ten that cua website.
- Dong bo ten thuong hieu "Ngan Hang De AI" (thay vi "Ngan Hang De" cut
  ngan) o tat ca cac trang xac thuc con lai: login.html (title, logo
  header, loi chao, footer ban quyen), forgot_password.html,
  reset_password.html, callback.html (title + logo/loi chao).
- register.html: link "Dang nhap" o footer chuyen tu link chet (href="#")
  sang tro toi trang that /login.
- Sua loi trang /register/teacher bao loi khi bam nut "Giao vien": route
  nay truoc do render template auth/register_teacher.html (khong ton
  tai trong repo) gay TemplateNotFound. Doi sang render lai template
  auth/teacher_coming_soon.html co san (trang "Sap ra mat" voi icon
  cong truong 🚧), dong thoi viet lai doan gioi thieu cho di dom hon va
  sua nut "Quay lai" tro dung ve /register (truoc do la href="#").
- register.html: bo nut "Tiep tuc" (id="next-btn") vi khong con tac
  dung — 2 the Hoc sinh/Giao vien da dieu huong thang toi
  /register/student, /register/teacher ngay khi bam, khong con di qua
  buoc chon-vai-tro-roi-bam-tiep-tuc (selectRole()/nextStep()) nhu
  thiet ke cu.
- register.html: them hieu ung hover cho thanh chi bao 2 doan ngay tren
  2 the Hoc sinh/Giao vien (truoc do la thanh tinh, khong doi mau) — di
  chuot vao the Hoc sinh thi doan trai chuyen xanh (bg-primary), di
  chuot vao the Giao vien thi doan phai chuyen xanh, dung
  document.getElementById('role-student'/'role-teacher').addEventListener
  ('mouseenter', ...) doi class Tailwind cua step-indicator-1/2.

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.11 vao {FILE} ({goc} -> {len(content)} ky tu)")
