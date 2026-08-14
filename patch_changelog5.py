import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

anchor = '''- teacher_coming_soon.html: logo "Ngan Hang De AI" goc trai header gio
  bam vao ve trang chu "/" (truoc do la <div> tinh, khong bam duoc).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.12."

addendum = '''


===============================================================================

Version 2.13

Ngày

2026-08-14

Nội dung

- register_student.html: logo "Ngan Hang De AI" goc trai header gio bam
  vao ve trang chu "/" (truoc do la <div> tinh, khong bam duoc).
- register_student.html: bo nav "Tinh nang / Ve chung toi" o header vi
  ca 2 deu la link chet (href="#") khong dan di dau.
- register_student.html: nut "Login" o header doi thanh "Dang nhap" (dung
  tieng Viet giong cac trang khac), tu <button> khong co tac dung doi
  thanh <a href="/login"> tro dung ve trang dang nhap that.
- SUA LOI QUAN TRONG: URL Google Fonts nap icon Material Symbols
  Outlined trong register_student.html bi sai cu phap (chi khai bao 1
  truc "wght@100..700,0..1" nhung dua vao 2 khoang gia tri, thieu khai
  bao truc "FILL") - da kiem chung Google Fonts API tra ve RONG cho URL
  loi nay. He qua: font icon khong tai duoc, trinh duyet hien chu that
  "person"/"mail"/"lock"/"lock_reset" (Inter, roi vao dung 1 vung dem
  danh cho icon 24px) de chong len chu vi du (placeholder) trong 4 o
  nhap Ho ten/Email/Mat khau/Xac nhan mat khau - day chinh la nguyen
  nhan bao loi "chu huong dan va vi du chong len nhau". Sua URL thanh
  "wght,FILL@100..700,0..1" (giong dung mau da dung o cac trang
  login.html, register.html, teacher_coming_soon.html).
- title trang doi tu "QuizAI" (ten sot lai tu ban mau) sang
  "Ngan Hang De AI" cho dung thuong hieu; placeholder o Email cung doi
  tu "hocsinh@quizai.vn" sang "hocsinh@email.com".

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.13 vao {FILE} ({goc} -> {len(content)} ky tu)")
