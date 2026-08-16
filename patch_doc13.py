import unicodedata

FILE = "docs/13_FRONTEND.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "tham_gia_lop_classroom.html" not in content, "Da co addendum nay - khong chay lai script."

expected_tail = '''Chưa có (theo đúng mục tiêu doc này, để làm ở giai đoạn sau)

- Dashboard học sinh / giáo viên.
- Làm bài Online / Nộp bài / Chấm bài (WF007 chưa triển khai).
- Phân tích học tập (CHV_Analyzer, WF003 chưa triển khai).
- Nút "Luyện tập ngay".
- Quản lý lớp học / quản lý tài khoản.'''

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong "
    "truoc khi them addendum."
)

addendum = '''


===============================================================================

# Cập nhật 2026-08-16 — Chọn lớp + tham gia Classroom (Version 2.17 → 2.22)

Chi tiết đầy đủ xem docs/16_CHANGELOG.md. "Quản lý lớp học" ở danh sách
"Chưa có" phía trên nay có bản tối giản (KHÔNG phải dashboard đầy đủ):

- app/templates/chat/chon_lop.html — học sinh chọn lớp (dropdown nhóm
  theo Khối 10/11) khi chưa có profiles.lop. Có thể quay lại đổi lớp
  bất cứ lúc nào.
- app/templates/chat/tham_gia_lop_classroom.html — hiện sau khi chọn
  lớp (nếu giáo viên đã kết nối Classroom): hướng dẫn 3 bước + mã lớp
  (enrollment code) để học sinh tự tham gia lớp thật trên Google
  Classroom. Có link "Bỏ qua, vào Chat AI ngay" — không bắt buộc.

Vẫn CHƯA có: dashboard học sinh/giáo viên, làm bài online, chấm bài,
phân tích học tập, quản lý tài khoản — đúng như danh sách "Chưa có" ở
trên, không đổi.
'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them addendum vao {FILE} ({goc} -> {len(content)} ky tu)")
