import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "Version 2.18" not in content, "Version 2.18 da ton tai - khong chay lai script nay."

expected_tail = '''- CHUA kiem chung end-to-end tren production (can nguoi dung chay SQL
  o tren truoc, roi thu dang nhap/dang ky moi de xac nhan trang
  /chon-lop hien ra dung luc, chon lop xong vao duoc /chat binh
  thuong).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien (co the file da doi kho tu luc doc) - "
    "dung lai, kiem tra thu cong truoc khi them Version 2.18."
)

addendum = '''


===============================================================================

Version 2.18

Ngày

2026-08-15

Nội dung

- Sua loi giao dien: bam logo/ve trang chu ("/") lam nguoi dung tuong
  nham la bi dang xuat, du phien (cookie sb_access_token) van con hop
  le. Nguyen nhan: app/routers/home.py truoc day khong doc cookie/kiem
  tra dang nhap nhu /chat, luon render index.html voi nut header/CTA
  cung "Dang nhap" bat ke da dang nhap hay chua.
- app/routers/home.py: GET "/" gio goi get_current_user(request) (dung
  ham co san trong app/core/deps.py, cung co che voi /chat), truyen
  da_dang_nhap + user_display_name qua Jinja2 context.
- app/templates/index.html: nut "Dang nhap" o header va nut CTA lon
  "Dang nhap ngay" o Hero deu doi thanh dieu kien {% if da_dang_nhap %}
  - da dang nhap thi hien "Vao Chat" (tro toi /chat) kem loi chao ten
  hien thi o header, chua dang nhap thi giu nguyen nhu cu.
- app/templates/chat/chat.html: them nut "Dang xuat" that trong sidebar
  (duoi nut "Danh gia hoc luc"), tro toi GET /logout (route nay da co
  san tu Version 2.4, xoa cookie sb_access_token/sb_refresh_token va
  chuyen huong ve /login) - truoc do khong co bat ky nut/link nao dan
  toi /logout tren giao dien, chi vao duoc bang cach go thang URL.
- Xac nhan: co che phien lam viec (cookie) khong doi - van giu dang
  nhap xuyen suot cac trang cho toi khi nguoi dung tu bam "Dang xuat"
  hoac cookie het han tu nhien (7/30 ngay neu tick "Ghi nho dang nhap"
  hoac dang nhap Google, session-only neu khong tick). Day la loi hien
  thi/UX o trang chu, khong phai loi mat phien thuc su.
- CHUA kiem chung end-to-end tren production (can nguoi dung tu dang
  nhap, bam logo ve trang chu de xac nhan van thay "Vao Chat" + ten
  hien thi thay vi "Dang nhap", bam "Dang xuat" trong sidebar chat de
  xac nhan ve dung /login va mat phien that).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.18 vao {FILE} ({goc} -> {len(content)} ky tu)")
