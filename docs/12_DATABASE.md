# DATABASE

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Database lưu trữ toàn bộ dữ liệu của hệ thống.

Không lưu dữ liệu tạm.

Không lưu dữ liệu sinh trong Python.

---

# Database

Supabase

(PostgreSQL)

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

# classes

Lưu thông tin lớp học.

---

# students

Lưu thông tin học sinh.

---

# teachers

Lưu thông tin giáo viên.

---

# student_classes

Liên kết

Học sinh

↓

Lớp

---

# exam_history

Lưu lịch sử sinh đề.

Thông tin

- user_id
- exam_id
- blueprint
- created_at

---

# exam_files

Lưu thông tin file.

Ví dụ

- PDF
- LaTeX
- JSON

Không lưu nội dung file.

Chỉ lưu đường dẫn.

---

# learning_history

Lưu lịch sử học tập.

Ví dụ

- điểm
- thời gian làm bài
- kết quả
- thống kê

---

# chat_history

Lưu lịch sử hội thoại AI.

---

# system_logs

Lưu log hệ thống.

---

# Quan hệ

Teacher

↓

Class

↓

Student

↓

Exam History

↓

Learning History

---

# Không lưu

- PPCT
- Curriculum
- Mapping
- Python Bank

Các dữ liệu này lưu dưới dạng file JSON trong thư mục data.

---

# Quy tắc

- Mỗi bảng chỉ lưu một loại dữ liệu.
- Không lưu file PDF trong Database.
- Không lưu file LaTeX trong Database.
- Database chỉ lưu metadata và đường dẫn.
- Dữ liệu chương trình học không đưa vào Database.