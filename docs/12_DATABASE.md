# DATABASE

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Database lưu trữ toàn bộ dữ liệu của hệ thống. Không lưu dữ liệu
tạm, không lưu dữ liệu sinh trong Python.

---

# Database

Supabase (PostgreSQL)

---

# Danh sách bảng

profiles
classes
students
teachers
student_classes
exam_history
exam_files
learning_history
chat_history
system_logs

---

# profiles

Lưu thông tin người dùng.

---

# classes / students / teachers / student_classes

Quản lý lớp học, học sinh, giáo viên, liên kết học sinh–lớp.

---

# exam_history

- user_id
- exam_id
- blueprint
- created_at

---

# exam_files

Lưu thông tin file (PDF, LaTeX, JSON). Chỉ lưu đường dẫn, không
lưu nội dung file.

---

# learning_history

Lưu lịch sử học tập và kết quả chấm bài.

- diem
- thoi_gian_lam_bai
- ket_qua_theo_cau (JSON: question_id, loai_cau, dung_sai_hoac_diem,
  chuong, bai, tags — theo Grade Result ở doc 03)
- diem_tu_luan_chi_tiet (JSON: nhan_xet, loi_sai — từ CHV_Grader)
- weak_points, strong_points (JSON — từ CN_AnalyzeResults)

---

# chat_history

Lưu lịch sử hội thoại AI (CHV_Fun, CHV_Analyzer).

---

# system_logs

Lưu log hệ thống.

---

# Quan hệ

Teacher → Class → Student → Exam History → Learning History

---

# Không lưu

PPCT, Curriculum, Mapping, Python Bank — các dữ liệu này lưu
dưới dạng file JSON trong thư mục data.

---

# Quy tắc

- Mỗi bảng chỉ lưu một loại dữ liệu.
- Không lưu file PDF/LaTeX trong Database.
- Database chỉ lưu metadata và đường dẫn.
- Dữ liệu chương trình học không đưa vào Database.


===============================================================================

# Trạng thái triển khai thực tế (cập nhật 2026-08-06)

Xem chi tiết đầy đủ ở docs/16_CHANGELOG.md, Version 2.4.

- exam_history (bảng có sẵn từ trước) đang đóng vai trò của
  learning_history trong doc này (lưu kết quả chấm bài: diem,
  chi_tiet_bai_lam), KHÔNG phải nơi lưu đề đã sinh.
- Đề đã sinh (mục tiêu ban đầu đặt tên exam_history/exam_files)
  thực tế lưu ở 2 bảng mới: de_da_sinh (metadata mỗi lần sinh đề:
  user_id, conversation_id, lop, role, loai_he_so, ki_thi,
  pham_vi_chuong) và file_de (đường dẫn file, gắn de_id, loai_file
  thuộc {de, tex, loigiai}).
- chat_history đã triển khai đúng như doc mô tả: mỗi dòng là 1 tin
  nhắn, gắn user_id + conversation_id.
- Row Level Security (RLS) tắt trên cả 3 bảng mới — chủ đích, vì
  chỉ FastAPI được đọc/ghi (đúng nguyên tắc "Frontend không đọc
  Database trực tiếp" ở doc 13), không cần policy theo từng user.
- Khi triển khai WF007 (chấm bài) cần rà soát lại tên bảng để không
  trùng lần nữa: exam_history đã bị dùng cho mục đích khác so với
  doc này.


===============================================================================

# Trạng thái triển khai thực tế — file_de (cập nhật 2026-08-06)

Xem chi tiết ở docs/16_CHANGELOG.md, Version 2.5.

file_de.loai_file hiện có 4 giá trị: de, tex, loigiai, dapan_json (thêm
dapan_json cho bước chuẩn bị chấm bài — WF007). Đã sửa CHECK constraint
file_de_loai_file_check trên Supabase để cho phép giá trị mới này.


===============================================================================

# Cập nhật 2026-08-07 — exam_history dùng thật cho chấm bài

exam_history đã xác nhận hoạt động đúng vai trò lưu kết quả chấm bài (không
phải lưu đề — xem cập nhật Version 2.4 ở trên). Đã tắt RLS cho bảng này
(trước đó bị bỏ sót, không nằm trong nhóm 3 bảng tắt RLS ở Version 2.4).

Lưu ý vận hành: bảng profiles chỉ được tự động tạo dòng mới nhờ trigger
on_auth_user_created (hàm handle_new_user) — trigger này được thêm sau một
số tài khoản đã đăng ký từ trước, nên các tài khoản đó thiếu dòng profiles
và sẽ lỗi khóa ngoại khi ghi vào các bảng tham chiếu profiles.id (exam_history,
de_da_sinh...). Nếu phát sinh lỗi 23503 tương tự, chạy lại đoạn backfill ở
Version 2.6 (docs/16_CHANGELOG.md) cho tài khoản còn thiếu.
