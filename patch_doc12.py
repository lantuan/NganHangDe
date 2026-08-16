import unicodedata

FILE = "docs/12_DATABASE.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "classroom_oauth" not in content, "Da co addendum nay - khong chay lai script."

expected_tail = """Lưu ý vận hành: bảng profiles chỉ được tự động tạo dòng mới nhờ trigger
on_auth_user_created (hàm handle_new_user) — trigger này được thêm sau một
số tài khoản đã đăng ký từ trước, nên các tài khoản đó thiếu dòng profiles
và sẽ lỗi khóa ngoại khi ghi vào các bảng tham chiếu profiles.id (exam_history,
de_da_sinh...). Nếu phát sinh lỗi 23503 tương tự, chạy lại đoạn backfill ở
Version 2.6 (docs/16_CHANGELOG.md) cho tài khoản còn thiếu."""

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong "
    "truoc khi them addendum."
)

addendum = '''


===============================================================================

# Cập nhật 2026-08-16 — Lớp học + Google Classroom (Version 2.17 → 2.22)

Chi tiết đầy đủ xem docs/16_CHANGELOG.md. Bảng/cột THẬT đang dùng:

- profiles — thêm 2 cột khoi, lop (text) từ Version 2.17. Học sinh tự
  chọn ở /chon-lop, hoặc tự động khớp qua email đồng bộ từ Classroom
  (classroom_roster, xem dưới).
- classroom_oauth (mới, Version 2.20) — chỉ 1 dòng (id=1 cố định), lưu
  refresh_token OAuth của giáo viên kết nối Google Classroom lúc
  /gv/classroom/connect. updated_at.
- classroom_roster (mới, Version 2.20) — email (khóa chính), khoi, lop,
  ho_ten, synced_at. Kết quả đồng bộ từ Google Classroom qua
  /gv/classroom/sync — dùng để tự động khớp lớp theo email đăng nhập
  (classroom_service.tim_lop_theo_email), KHÔNG dùng để chấm điểm hay
  quản lý học sinh (việc đó vẫn làm trên Google Classroom thật).

RLS tắt trên cả classroom_oauth và classroom_roster — cùng nguyên tắc
"chỉ FastAPI được đọc/ghi" đã áp dụng cho chat_history, de_da_sinh,
file_de, exam_history, profiles.khoi/lop.
'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them addendum vao {FILE} ({goc} -> {len(content)} ky tu)")
