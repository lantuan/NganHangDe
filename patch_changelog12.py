import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "Version 2.20" in content, "Chua thay Version 2.20 - chay patch_changelog11.py truoc."
assert "Version 2.21" not in content, "Version 2.21 da ton tai - khong chay lai script nay."

expected_tail = "Người thực hiện\n\nMai Hà Lan (cùng Claude)"
assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong truoc "
    "khi them Version 2.21."
)

addendum = '''


===============================================================================

Version 2.21

Ngày

2026-08-15

Nội dung

- Lam chieu NGUOC LAI voi Version 2.20 (doc email tu Classroom ve web):
  gio hoc sinh dang ky/chon lop TREN WEB se tu dong duoc GHI DANH (join)
  vao dung lop that tren Google Classroom, khong can giao vien moi tay
  tung em hoac hoc sinh tu nhap ma lop.
- CAN NGUOI DUNG TU LAM TRUOC TREN GOOGLE CLOUD CONSOLE: vao Data Access,
  them 2 scope MOI (ngoai 2 scope da xin o Version 2.20):
      https://www.googleapis.com/auth/classroom.rosters
      (thay cho classroom.rosters.readonly cu - can quyen GHI de them
      hoc sinh, khong chi doc duoc nua)
      https://www.googleapis.com/auth/classroom.courses.readonly
      (de doc duoc ma dang ky/enrollmentCode cua tung lop, bat buoc phai
      co de goi API them hoc sinh)
- CAN NGUOI DUNG LAM LAI /gv/classroom/connect (ket noi lai tu dau) SAU
  KHI da them 2 scope o tren - refresh_token cu chi mang quyen doc, PHAI
  xin lai moi co quyen ghi. Lam lai khong anh huong du lieu classroom_
  roster da dong bo truoc do.
- Sua app/services/classroom_service.py: doi SCOPES (chi tiet o tren),
  them lay_enrollment_code (doc ma dang ky cua 1 lop qua GET /courses/
  {courseId}), them them_hoc_sinh_vao_lop (goi POST /courses/{courseId}/
  students?enrollmentCode=... voi userId=email - coi ma 409 "da la
  thanh vien" la thanh cong, khong phai loi that), them ham cap cao
  tu_dong_ghi_danh_classroom(email, khoi, lop) - KHONG bao gio raise
  loi ra ngoai (chi tra ve {"success": bool, "message": str}), vi day
  la tien ich them, khong duoc phep chan hoc sinh vao /chat cua web du
  Classroom co loi gi (vd email khong phai tai khoan Google that thi
  chi ghi log, hoc sinh van vao /chat binh thuong).
- Sua app/routers/chat.py: POST /chon-lop, ngay sau khi luu lop vao
  profiles, goi them classroom_service.tu_dong_ghi_danh_classroom() -
  khong kiem tra ket qua (theo dung nguyen tac o tren, khong chan luong
  chinh cua hoc sinh).
- Da test logic trong sandbox (gia lap Google tra ve: them hoc sinh moi
  thanh cong, hoc sinh da la thanh vien san (409), email khong phai tai
  khoan Google that (400), lop khong co trong MA_LOP_CLASSROOM) - ca 4
  truong hop deu dung nhu thiet ke, khong co truong hop nao lam crash
  luong /chon-lop.
- CHUA kiem chung end-to-end tren production (can nguoi dung: (1) them
  2 scope moi tren Google Cloud Console, (2) lam lai /gv/classroom/
  connect de xin refresh_token co quyen ghi, (3) dang ky/dang nhap bang
  1 tai khoan Google that, chon 1 lop bat ky o /chon-lop, (4) vao
  Google Classroom lop do (tab Moi nguoi) kiem tra hoc sinh da tu xuat
  hien trong danh sach chua).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.21 vao {FILE} ({goc} -> {len(content)} ky tu)")
