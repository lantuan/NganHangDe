import unicodedata

FILE = "docs/05_API_SPECIFICATION.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "/gv/classroom/connect" not in content, "Da co addendum nay - khong chay lai script."

expected_tail = """Câu TF (Đúng/Sai) hiện luôn trả về trạng thái can_cham_tay dù đã đọc được
ảnh (answer_parser_service chưa trích được đáp án đúng cho TF). Chi tiết
xem docs/16_CHANGELOG.md, Version 2.8. Đã kiểm chứng end-to-end trên
production bằng ảnh giả (không lỗi, đúng schema); chưa kiểm chứng độ
chính xác đọc bằng ảnh chụp thật."""

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong "
    "truoc khi them addendum."
)

addendum = '''


===============================================================================

# Cập nhật 2026-08-16 — Chọn lớp + Google Classroom (Version 2.17 → 2.22)

Chi tiết đầy đủ xem docs/16_CHANGELOG.md. Route THẬT đang chạy:

## Chọn lớp (học sinh tự chọn, không cần giáo viên xác nhận)

GET  /chon-lop   — trang chọn lớp (yêu cầu đã đăng nhập)
POST /chon-lop   — lưu khoi/lop vào profiles, thử tạo link tham gia
                   Classroom (xem dưới), rồi vào /chat

## Google Classroom (giáo viên kết nối 1 lần, không phải API JSON)

GET /gv/classroom/connect       — chuyển hướng màn hình đồng ý Google
GET /gv/classroom/callback      — nhận code, đổi lấy refresh_token, lưu
GET /gv/classroom/sync          — đồng bộ toàn bộ roster (email học
                                   sinh) từ Classroom về classroom_roster
GET /gv/classroom/debug-roster  — xem dữ liệu đã đồng bộ (debug)

Cả 4 route yêu cầu đã đăng nhập web. Không có API JSON riêng cho
Classroom — toàn bộ là route redirect/HTML, gọi trực tiếp Google
Classroom REST API qua app/services/classroom_service.py (không dùng
SDK google-api-python-client).

GHI CHÚ QUAN TRỌNG: courses.students.create (thêm thẳng học sinh vào
lớp) bị Google chặn 403 PERMISSION_DENIED với tài khoản Gmail cá nhân
(chỉ quản trị viên domain Google Workspace mới thêm thẳng được) — xem
Version 2.22. Cách đang dùng: tạo link + mã lớp (enrollment code) để
học sinh tự bấm "Tham gia" trên Classroom, không gọi API ghi (write)
nào thành công thật trên Classroom ngoài đọc roster/enrollment code.
'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them addendum vao {FILE} ({goc} -> {len(content)} ky tu)")
