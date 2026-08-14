import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

anchor = '''- title trang doi tu "QuizAI" (ten sot lai tu ban mau) sang
  "Ngan Hang De AI" cho dung thuong hieu; placeholder o Email cung doi
  tu "hocsinh@quizai.vn" sang "hocsinh@email.com".

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.13."

addendum = '''


===============================================================================

Version 2.14

Ngày

2026-08-14

Nội dung

- register_student.html: them nut "Dang ky bang Google" (thanh chia
  "Hoac" + nut, ngay duoi nut "Dang ky" thuong) - dung chung 1 luong
  OAuth voi trang /login: signInWithOAuth (client-side, Supabase JS)
  -> redirect /auth/callback (trang trung chuyen co san) -> POST
  /auth/set-session (endpoint co san) -> set cookie -> /chat. Khong
  them route/endpoint moi, tai su dung toan bo ha tang OAuth da xay o
  Version 2.9.
- app/routers/auth.py: GET /register/student gio truyen them
  supabase_url/supabase_anon_key qua Jinja2 context (truoc do khong
  truyen gi ca) de Supabase JS tren trang nay chay duoc; ca nhanh loi
  cua POST /register/student (dang ky email/mat khau that bai, render
  lai chinh trang nay kem thong bao loi) cung duoc bo sung 2 gia tri
  nay de nut Google khong bi vo tac dung khi dang hien loi.
- Ghi chu ky thuat: khong can phan biet "vai tro" (hoc sinh/giao vien)
  khi dang ky bang Google, vi luong dang ky bang email/mat khau hien
  tai (supabase_service.sign_up) cung KHONG luu truong role nao vao
  user_metadata (chi luu fullname) - he thong hien chua co co che phan
  quyen theo role o buoc dang ky, nen nut Google o day an toan, khong
  lam lech logic sẵn co.

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.14 vao {FILE} ({goc} -> {len(content)} ky tu)")
