import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

anchor = '''  ('mouseenter', ...) doi class Tailwind cua step-indicator-1/2.

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.11."

addendum = '''


===============================================================================

Version 2.12

Ngày

2026-08-14

Nội dung

- teacher_coming_soon.html (trang "Sap ra mat" khi bam the Giao vien o
  /register/teacher): bo nav "Tinh nang / Bang gia / Huong dan" o header
  vi ca 3 deu la link chet (href="#") khong dan di dau.
- teacher_coming_soon.html: nut "Dang nhap" / "Dang ky" o header truoc
  do la <button> khong co tac dung, doi thanh <a href="/login">,
  <a href="/register"> tro dung ve 2 trang that.
- teacher_coming_soon.html: logo "Ngan Hang De AI" goc trai header gio
  bam vao ve trang chu "/" (truoc do la <div> tinh, khong bam duoc).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.12 vao {FILE} ({goc} -> {len(content)} ky tu)")
