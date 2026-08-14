import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

anchor = '''- app/routers/chat.py: GET /chat gio truyen them user_email +
  user_display_name qua Jinja2 context. user_display_name uu tien
  user_metadata['fullname'] (dang ky email/mat khau) -> 'full_name'/
  'name' (Google OAuth) -> fallback ve chinh email neu khong co field
  nao.

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.16."

addendum = '''


===============================================================================

Version 2.17

Ngày

2026-08-15

Nội dung

- Quyet dinh kien truc quan ly lop (thay cho phuong an dong bo Google
  Classroom API da can nhac o Version 2.16 - qua phuc tap, khong lam):
  hoc sinh TU CHON lop cua minh khi dang nhap lan dau (khong doi chieu
  email tu dong), diem so/cham bai van thuc hien tren Google Classroom
  nhu giao vien dang lam, web nay chi can biet "em nay lop nao" de gom
  du lieu (sinh de/thong ke) theo lop sau nay.
- Them app/core/lop_config.py: DANH_SACH_LOP (dict khoi -> danh sach
  ten lop), hien tai co khoi 10 va 11 (13 lop moi khoi: C1A, C1B, C2A,
  C2B, C3A, C3B, C4, C5A, C5B, C6, C7, C8, C9 - dung ten that tren
  Google Classroom). Khoi 12 se them sau khi giao vien tao xong lop
  tren Classroom - chi can them 1 dong vao file nay, khong phai sua
  code cho nao khac.
- Them app/services/supabase_service.py::lay_lop_hoc_sinh(user_id) va
  cap_nhat_lop_hoc_sinh(user_id, khoi, lop) - doc/ghi 2 cot khoi, lop
  moi trong bang public.profiles.
- Them GET/POST /chon-lop (app/routers/chat.py) va template moi
  app/templates/chat/chon_lop.html: hoc sinh chon 1 trong danh sach
  lop (dropdown co nhom theo Khoi 10/Khoi 11), luu vao profiles.khoi/
  profiles.lop, quay ve /chat. Hoc sinh co the tu quay lai trang nay
  doi lop bat cu luc nao (khong khoa sau khi chon).
- GET /chat gio kiem tra profiles.lop truoc khi cho vao chat: chua
  chon thi chuyen huong /chon-lop, da chon thi truyen them user_khoi/
  user_lop vao context, hien them 1 dong "Khoi X - Lop Y" trong
  account-badge o header (canh ten/email) de hoc sinh biet dang o
  lop nao.
- CAN NGUOI DUNG TU CHAY SQL TREN SUPABASE (SQL Editor) TRUOC KHI
  DUNG TINH NANG NAY - bang public.profiles chua co 2 cot khoi, lop:
      alter table public.profiles
        add column if not exists khoi text,
        add column if not exists lop text;
      alter table public.profiles disable row level security;
  Dong disable RLS de dam bao FastAPI (dung anon key, khong phai JWT
  rieng tung user) doc/ghi duoc 2 cot nay - dung nguyen tac da ap dung
  cho chat_history, de_da_sinh, file_de, exam_history tu Version 2.4/
  2.6 ("chi FastAPI duoc doc/ghi cac bang du lieu app tu quan ly").
- CHUA kiem chung end-to-end tren production (can nguoi dung chay SQL
  o tren truoc, roi thu dang nhap/dang ky moi de xac nhan trang
  /chon-lop hien ra dung luc, chon lop xong vao duoc /chat binh
  thuong).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.17 vao {FILE} ({goc} -> {len(content)} ky tu)")
