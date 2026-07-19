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