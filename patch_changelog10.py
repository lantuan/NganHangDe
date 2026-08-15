import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "Version 2.19" not in content, "Version 2.19 da ton tai - khong chay lai script nay."

expected_tail = '''- CHUA kiem chung end-to-end tren production (can nguoi dung tu dang
  nhap, bam logo ve trang chu de xac nhan van thay "Vao Chat" + ten
  hien thi thay vi "Dang nhap", bam "Dang xuat" trong sidebar chat de
  xac nhan ve dung /login va mat phien that).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien (co the Version 2.18 chua duoc them, "
    "hoac file da doi kho tu luc doc) - dung lai, kiem tra thu cong truoc "
    "khi them Version 2.19."
)

addendum = '''


===============================================================================

Version 2.19

Ngày

2026-08-15

Nội dung

- Sua loi goc re: "Ghi nho dang nhap" (checkbox o /login, xem Version 2.9)
  tich hay khong tich deu nhu nhau - nguoi dung van bi dang xuat giua
  chung khi dang dung web. Nguyen nhan that su: access_token (JWT) cua
  Supabase mac dinh het han sau ~1 gio KE CA KHI cookie sb_access_token
  con song toi 7 ngay (da tick "Ghi nho dang nhap") - truoc gio khong co
  co che lam moi access_token bang refresh_token, nen sau ~1 gio la
  get_current_user() luon that bai bat ke cookie con han hay khong.
  Checkbox "Ghi nho dang nhap" chi quyet dinh cookie song bao lau qua
  cac lan DONG/MO LAI trinh duyet, khong lien quan gi toi viec tu dang
  xuat giua chung nay - do la 2 co che khac nhau, va truoc gio co che
  thu 2 (lam moi access_token) chua ton tai.
- app/core/deps.py: them ham _thu_lam_moi_phien(refresh_token) - goi
  supabase.auth.refresh_session(refresh_token) de xin access_token moi.
  get_current_user() gio thu get_user(access_token) truoc, neu loi (het
  han) thi tu dong thu lam moi bang refresh_token trong cookie
  sb_refresh_token; neu lam moi thanh cong, luu phien moi vao
  request.state.new_session va tra ve user (khong bat dang nhap lai);
  neu ca 2 token deu khong hop le, tra ve None nhu cu (that su can dang
  nhap lai).
- app/main.py: them middleware HTTP lam_moi_cookie_phien - sau moi
  request, neu request.state.new_session vua duoc get_current_user() dat
  (tuc la vua tu lam moi phien), ghi lai 2 cookie sb_access_token/
  sb_refresh_token moi (7/30 ngay) vao response. Ap dung cho MOI route co
  goi get_current_user() (/chat, /chon-lop, /api/chat/..., trang chu "/"
  tu Version 2.18...), khong phai sua tung route rieng le.
- Da kiem chung logic bang test doc lap (FastAPI TestClient + supabase
  gia lap mo phong dung 4 tinh huong): (1) access_token con han -> tra ve
  dung user, khong dong cookie moi; (2) access_token het han nhung
  refresh_token con hop le -> tu dong lam moi, tra ve dung user, dong
  dung 2 cookie moi; (3) ca 2 token deu het han/khong hop le -> tra ve
  None (bat dang nhap lai), khong dong cookie; (4) khong co cookie nao ->
  tra ve None. Ca 4 truong hop deu dung ky vong.
- CHUA kiem chung end-to-end voi Supabase that tren production (test o
  tren dung supabase gia lap, chua goi refresh_session that qua mang -
  can nguoi dung dang nhap that, doi qua ~1 gio (hoac sua tam thoi JWT
  expiry trong Supabase Dashboard xuong vai phut de test nhanh) roi thao
  tac tiep tren web de xac nhan khong bi vang ra /login).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.19 vao {FILE} ({goc} -> {len(content)} ky tu)")
