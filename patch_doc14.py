import unicodedata

FILE = "docs/14_DEPLOYMENT.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "GOOGLE_CLASSROOM_CLIENT_ID" not in content, "Da co addendum nay - khong chay lai script."

expected_tail = '''Xem chi tiết ở docs/06_N8N_WORKFLOW.md, mục "Trạng thái triển khai thực
tế". Tóm tắt: hiện chỉ có 1 Workflow gộp (không tách WF001-WF007 riêng),
Switch có 2 nhánh hoạt động (generate_exam, download_file), phần Business
Logic (Blueprint, Question Selector, Generator, Assembler) nằm trong
FastAPI (app/services/), n8n chỉ gọi 1 API duy nhất cho mỗi nhánh.'''

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong "
    "truoc khi them addendum."
)

addendum = '''


===============================================================================

# Cập nhật 2026-08-16 — Google Classroom OAuth (Version 2.20 → 2.22)

## Biến môi trF�ờng mới (.env trên VPS — KHÔNG qua git, sửa trực tiếp
bằng SSH, xem mục "Quy trình sửa code" ở trên chỉ áp dụng cho code)

- GOOGLE_CLASSROOM_CLIENT_ID
- GOOGLE_CLASSROOM_CLIENT_SECRET

OAuth Client RIÊNG cho tính năng đồng bộ/tham gia lớp Classroom, KHÁC
Client đang dùng cho nút "Đăng nhập bằng Google" qua Supabase (2 Client
độc lập trong cùng 1 project Google Cloud Console).

## Google Cloud Console — cấu hình bắt buộc

- Bật Google Classroom API.
- Scope: classroom.rosters, classroom.profile.emails,
  classroom.courses.readonly (đủ 3 scope — chi tiết lý do từng scope
  xem docs/16_CHANGELOG.md Version 2.20/2.21).
- Authorized redirect URI: https://nganhangdechv.tech/gv/classroom/callback
- App đang ở chế độ Testing (chưa verify với Google) — CHỈ tài khoản
  được thêm làm Test user mới kết nối được; tài khoản khác bị Google
  chặn ngay ở màn hình đồng ý quyền.

## Giới hạn đã biết — không sửa được bằng cấu hình

Google KHÔNG cho phép thêm thẳng học sinh vào lớp qua API
(courses.students.create) trừ khi tài khoản gọi API là quản trị viên
domain Google Workspace for Education. Vì Classroom ở đây dùng tài
khoản Gmail cá nhân, tính năng chỉ dừng ở mức tạo link + mã lớp để học
sinh tự tham gia (xem docs/16_CHANGELOG.md Version 2.22).
'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them addendum vao {FILE} ({goc} -> {len(content)} ky tu)")
