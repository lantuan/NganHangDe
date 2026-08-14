import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

anchor = '''  quyen theo role o buoc dang ky, nen nut Google o day an toan, khong
  lam lech logic sẵn co.

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.14."

addendum = '''


===============================================================================

Version 2.15

Ngày

2026-08-14

Nội dung

- Sua Supabase Dashboard > Authentication > URL Configuration: Site URL
  doi tu localhost:3000 sang https://nganhangdechv.tech; Redirect URLs
  bo sung https://nganhangdechv.tech/auth/callback - truoc do thieu nen
  OAuth luon redirect ve localhost:3000 sau khi dang nhap/dang ky bang
  Google tren production.
- Sua ham handle_new_user (Supabase Database Function, trigger
  on_auth_user_created - da ghi nhan lan dau o Version 2.6): truoc do
  chi doc new.raw_user_meta_data ->> 'fullname', dung cho luong dang ky
  email/mat khau (co gui key fullname tu supabase_service.sign_up) nhung
  KHONG dung cho luong Google OAuth (Google tra ve key full_name/name,
  khong phai fullname) -> ho_ten bi NULL -> insert vao public.profiles
  that bai vi cot ho_ten NOT NULL -> loi "Database error saving new
  user" khi dang ky tai khoan Google moi. Sua thanh coalesce lan luot
  fullname -> full_name -> name -> phan truoc @ cua email, dam bao
  ho_ten khong bao gio NULL du dang ky bang duong nao.
- Da kiem chung end-to-end tren production: dang ky tai khoan Google
  moi thanh cong, vao duoc /chat.

Người thực hiện

Mai Hà Lan (cùng Claude)

===============================================================================

Version 2.16

Ngày

2026-08-14

Nội dung

- chat.html: sua font-size nut Gui / + Chat moi / Danh gia hoc luc -
  truoc do CSS chi reset font-family cho button/input/textarea, khong
  reset font-size, nen cac nut nay dung font-size mac dinh cua trinh
  duyet cho form control (nho hon han text thuong), khac voi cac trang
  khac dung Tailwind (da co san text-base/text-lg). Them font-size:
  16px mac dinh cho button/input/textarea, rieng #new-chat-btn/#send-btn
  len 18px cho dong bo voi cac nut CTA o trang dang nhap/dang ky.
- chat.html: logo "Ngan Hang De AI" o sidebar gio bam vao ve trang chu
  "/" (truoc do la <div> tinh, khong bam duoc).
- chat.html: bo nut Home rieng o goc phai header (da thua viec vi logo
  da lam duoc); thay bang the "account-badge" hien ten hien thi + email
  cua tai khoan dang dang nhap, giup nguoi dung phan biet dang dung tai
  khoan nao khi lam bai (hay gap khi mot nguoi dung nhieu tai khoan
  Google/email khac nhau).
- app/routers/chat.py: GET /chat gio truyen them user_email +
  user_display_name qua Jinja2 context. user_display_name uu tien
  user_metadata['fullname'] (dang ky email/mat khau) -> 'full_name'/
  'name' (Google OAuth) -> fallback ve chinh email neu khong co field
  nao.

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.15 va 2.16 vao {FILE} ({goc} -> {len(content)} ky tu)")
