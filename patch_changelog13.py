import unicodedata

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "Version 2.21" in content, "Chua thay Version 2.21 - chay patch_changelog12.py truoc."
assert "Version 2.22" not in content, "Version 2.22 da ton tai - khong chay lai script nay."

expected_tail = "Người thực hiện\n\nMai Hà Lan (cùng Claude)"
assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong truoc "
    "khi them Version 2.22."
)

addendum = '''


===============================================================================

Version 2.22

Ngày

2026-08-16

Nội dung

- Test thuc te Version 2.21 tren production: hoc sinh chon lai lop o
  /chon-lop, web goi Google them thang hoc sinh vao lop (courses.
  students.create voi enrollmentCode) - Google tra ve LOI 403
  PERMISSION_DENIED. Nguyen nhan: cach them thang hoc sinh qua API nay
  CHI duoc phep khi nguoi goi la quan tri vien domain Google Workspace
  for Education - khong ap dung duoc voi Classroom tao boi tai khoan
  Gmail ca nhan (nhu nganhangdetoanchv@gmail.com dang dung). Day la gioi
  han cua Google, khong sua duoc bang cach xin them scope.
- SUA LAI CACH LAM (thay Version 2.21): thay vi tu dong them thang hoc
  sinh (khong the lam duoc), sau khi hoc sinh chon lop o /chon-lop, web
  tao san 1 link "Tham gia lop" (dung ma dang ky/enrollment code cua
  lop, dang https://classroom.google.com/c/<course_id ma hoa base64>
  ?cjc=<ma_dang_ky>) va hien thi mot trang xac nhan - hoc sinh chi can
  bam 1 nut, dang nhap dung tai khoan Google, bam "Tham gia" la xong.
  Khong con can tu tim lop hay tu nhap ma tay.
- Them app/services/classroom_service.py: ham tao_link_gia_nhap_lop
  (thay the them_hoc_sinh_vao_lop/tu_dong_ghi_danh_classroom cu - van
  giu lai code cu, khong xoa, phong khi sau nay chuyen sang Google
  Workspace for Education thi dung lai duoc). Them import base64.
- Them app/templates/chat/tham_gia_lop_classroom.html: trang xac nhan
  sau khi chon lop, co nut "Mo Google Classroom & Tham gia" (mo tab moi
  toi link tren), khung hien ma dang ky de nhap tay neu nut khong tu
  nhan dung, va link "Bo qua, vao Chat AI ngay" (khong bat buoc hoc
  sinh phai lam buoc nay).
- Sua app/routers/chat.py: POST /chon-lop, sau khi luu lop, goi
  tao_link_gia_nhap_lop() thay vi tu_dong_ghi_danh_classroom() - neu
  thanh cong thi render trang tham_gia_lop_classroom.html, neu khong
  (vd giao vien chua ket noi Classroom) thi ve /chat nhu binh thuong,
  khong chan hoc sinh.
- Da test logic trong sandbox (mock Google tra ve enrollmentCode, kiem
  tra dung dinh dang link + slug base64 tu course_id, truong hop lop
  khong ton tai, truong hop Google loi khi lay enrollment code) - deu
  dung nhu thiet ke.
- CHUA kiem chung end-to-end tren production (can nguoi dung: (1) dang
  nhap lai bang 1 tai khoan da tung chon lop truoc do - hoac xoa lop cu
  trong Supabase de bi day ve /chon-lop lai, (2) chon 1 lop, (3) kiem
  tra trang xac nhan hien dung link + ma dang ky, (4) bam nut, xac nhan
  Google Classroom tu dong nhan dung lop va ma, chi can bam Tham gia,
  (5) kiem tra lai trong Classroom (tab Moi nguoi) hoc sinh da vao lop
  thanh cong).

Người thực hiện

Mai Hà Lan (cùng Claude))'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.22 vao {FILE} ({goc} -> {len(content)} ky tu)")
