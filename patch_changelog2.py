import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)

goc = len(content)

anchor = '''- CHƯA kiểm chứng end-to-end (cần cấu hình Dashboard xong mới bấm thử
  được nút Google thật trên production).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.9."

addendum = '''


===============================================================================

Version 2.10

Ngày

2026-08-14

Nội dung

- Xac nhan: nguoi dung da tu cau hinh xong Google Cloud Console + Supabase
  Dashboard (Version 2.9) - da bat Google provider, tao OAuth Client
  ID/Secret, dang nhap Google hoat dong that tren production.
- login.html: logo "Ngan Hang De" tren header gio bam vao ve trang chu
  "/" (truoc do la <div> tinh, khong bam duoc).
- "Quen mat khau?" chuyen tu link chet (href="#") sang tro toi trang that
  /forgot-password.
- Them app/templates/auth/forgot_password.html: form nhap email, goi
  supabaseClient.auth.resetPasswordForEmail(email, {redirectTo:
  origin + "/reset-password"}) - Supabase gui email chua link dat lai
  mat khau (hoan toan client-side, khong qua backend).
- Them app/templates/auth/reset_password.html: trang nguoi dung mo tu
  link trong email, Supabase JS tu doc token khoi phuc (recovery) trong
  URL fragment va tu thiet lap phien lam viec khi createClient() chay,
  form nhap mat khau moi 2 lan goi supabaseClient.auth.updateUser({
  password}) de doi mat khau that.
- Them GET /forgot-password va GET /reset-password (app/routers/auth.py)
  - deu truyen supabase_url/supabase_anon_key qua Jinja2 context giong
  /login, de Supabase JS o 2 trang nay hoat dong.
- CAN NGUOI DUNG TU CAU HINH THEM: Supabase Dashboard > Authentication >
  URL Configuration > Redirect URLs - them
  https://nganhangdechv.tech/reset-password vao danh sach cho phep (neu
  chua co thi link trong email dat lai mat khau se bi Supabase tu choi
  redirect).
- CHUA kiem chung end-to-end (can nguoi dung tu bam thu gui email that
  tren production sau khi da them Redirect URL o tren).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.10 vao {FILE} ({goc} -> {len(content)} ky tu)")
