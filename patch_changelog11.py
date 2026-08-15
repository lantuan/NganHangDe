import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "Version 2.20" not in content, "Version 2.20 da ton tai - khong chay lai script nay."

expected_tail = '''- CHUA kiem chung end-to-end voi Supabase that tren production (test o
  tren dung supabase gia lap, chua goi refresh_session that qua mang -
  can nguoi dung dang nhap that, doi qua ~1 gio (hoac sua tam thoi JWT
  expiry trong Supabase Dashboard xuong vai phut de test nhanh) roi thao
  tac tiep tren web de xac nhan khong bi vang ra /login).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien (co the Version 2.19 chua duoc them, "
    "hoac file da doi kho tu luc doc) - dung lai, kiem tra thu cong truoc "
    "khi them Version 2.20."
)

addendum = '''


===============================================================================

Version 2.20

Ngày

2026-08-15

Nội dung

- Bat dau xay tinh nang tu dong ghep hoc sinh vao lop bang email dong bo
  tu Google Classroom (quyet dinh o Version 2.17 la lam sau, gio lam
  tiep theo yeu cau "hoc sinh dang ky thi tu nhay vao lop, khong can gv
  xac thuc"). Giu nguyen /chon-lop tu chon lam phuong an du phong khi
  khong khop duoc email.
- CAN NGUOI DUNG TU LAM TRUOC TREN GOOGLE CLOUD CONSOLE (da lam xong
  luc viet Version nay): tao OAuth Client ID rieng (khac Client dang
  dung cho dang nhap Google qua Supabase) trong cung project, bat
  Google Classroom API, xin 2 scope classroom.rosters.readonly (doc
  danh sach lop) va classroom.profile.emails (xem email hoc sinh - mac
  dinh Google an email, phai xin rieng scope nay moi thay), them Client
  ID/Secret moi vao .env tren VPS voi 2 ten bien GOOGLE_CLASSROOM_
  CLIENT_ID / GOOGLE_CLASSROOM_CLIENT_SECRET, them chinh email giao
  vien lam Test user (app dang o che do Testing, chua verify voi
  Google) va Authorized redirect URI
  https://nganhangdechv.tech/gv/classroom/callback.
- Them app/core/config.py: doc GOOGLE_CLASSROOM_CLIENT_ID/SECRET tu
  .env (giong cach doc SUPABASE_URL/KEY co san).
- Them app/services/classroom_service.py: tron bo ham xu ly OAuth rieng
  cho Classroom (tao_url_xac_thuc, doi_code_lay_token,
  lam_moi_access_token - goi thang REST API cua Google qua thu vien
  requests, khong dung them SDK google-api-python-client de do phu
  thuoc), luu/doc refresh_token (luu_refresh_token, lay_refresh_token),
  dong_bo_toan_bo (lap qua MA_LOP_CLASSROOM co san tu Version 2.16, goi
  Classroom API courses.students.list cho tung lop, co xu ly phan
  trang, ghi vao bang moi classroom_roster), tim_lop_theo_email (tra
  cuu 1 email, dung boi GET /chat), lay_toan_bo_roster (dung de debug).
- Them app/routers/classroom.py: GET /gv/classroom/connect (chuyen
  huong sang man hinh dong y cua Google), GET /gv/classroom/callback
  (nhan code, doi lay refresh_token, luu lai), GET /gv/classroom/sync
  (dong bo toan bo, tra ve so luong email lay duoc moi lop de kiem tra
  bang mat), GET /gv/classroom/debug-roster (xem toan bo du lieu da
  dong bo). Ca 4 route yeu cau da dang nhap; rieng buoc dang nhap Google
  o /gv/classroom/connect con duoc chinh Google chan them 1 lop nua vi
  app dang "Testing" - chi tai khoan da them lam Test user moi hoan tat
  duoc, tai khoan khac se bi Google bao loi tu man hinh dong y quyen.
- Sua app/routers/chat.py: GET /chat, khi hoc sinh chua co profiles.lop,
  gio thu classroom_service.tim_lop_theo_email(user.email) TRUOC khi
  chuyen huong /chon-lop - khop thi tu dong ghi khoi/lop (giong het
  duong di cua /chon-lop tu chon, chi khac la tu dong), khong khop thi
  roi ve /chon-lop nhu cu (hoc sinh chua duoc dong bo, hoac dang nhap
  bang email khac email tren Classroom).
- CAN NGUOI DUNG TU CHAY SQL TREN SUPABASE (SQL Editor) TRUOC KHI DUNG
  TINH NANG NAY - tao 2 bang moi va tat RLS (dung nguyen tac da ap
  dung cho cac bang app tu quan ly tu Version 2.4):
      create table if not exists public.classroom_oauth (
        id int primary key default 1,
        refresh_token text not null,
        updated_at timestamptz not null default now(),
        constraint classroom_oauth_chi_1_dong check (id = 1)
      );
      alter table public.classroom_oauth disable row level security;

      create table if not exists public.classroom_roster (
        email text primary key,
        khoi text not null,
        lop text not null,
        ho_ten text,
        synced_at timestamptz not null default now()
      );
      alter table public.classroom_roster disable row level security;
- CHUA kiem chung end-to-end tren production (can nguoi dung: (1) chay
  SQL tao 2 bang o tren, (2) them GOOGLE_CLASSROOM_CLIENT_ID/SECRET vao
  .env tren VPS, (3) vao /gv/classroom/connect dang nhap Google that,
  (4) vao /gv/classroom/sync xem thong ke so email moi lop co dung
  khong, (5) vao /gv/classroom/debug-roster xem thu du lieu that -
  DAC BIET kiem tra cot email co dung khong bi rong (neu rong tuc la
  scope classroom.profile.emails chua duoc cap dung), (6) dang ky/dang
  nhap bang 1 email hoc sinh co that trong danh sach de xac nhan tu
  dong vao duoc /chat, khong bi roi ve /chon-lop).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.20 vao {FILE} ({goc} -> {len(content)} ky tu)")
