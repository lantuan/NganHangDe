# FRONTEND

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Frontend là giao diện người dùng của hệ thống.

Frontend chỉ giao tiếp với FastAPI.

Không gọi trực tiếp n8n.

Không gọi trực tiếp Python.

---

# Kiến trúc

Frontend

↓

FastAPI

↓

n8n

↓

Python

---

# Chức năng

- Đăng nhập
- Đăng ký
- Chat AI
- Sinh đề
- Làm bài Online
- Phân tích học tập
- Tải PDF
- Quản lý lớp học
- Quản lý tài khoản

---

# Trang

Trang chủ

↓

Đăng nhập

↓

Đăng ký

↓

Dashboard

↓

Chat AI

↓

Sinh đề

↓

Làm bài

↓

Kết quả

↓

Phân tích học tập

↓

Quản lý tài khoản

---

# Dashboard học sinh

- Thông tin cá nhân
- Lịch sử học tập
- Đề đã tạo
- Điểm số
- Thống kê

---

# Dashboard giáo viên

- Danh sách lớp
- Danh sách học sinh
- Thống kê
- Quản lý đề

---

# Chat AI

Frontend

↓

FastAPI

↓

WF000_Gateway

↓

CHV_Fun

↓

Workflow phù hợp

↓

Response

---

# Sinh đề

Frontend

↓

FastAPI

↓

WF001_GenerateExam

↓

Exam Object

↓

PDF

↓

Frontend

---

# Làm bài Online

Frontend

↓

FastAPI

↓

Web Test

↓

Nộp bài

↓

Chấm điểm

---

# Tải file

Frontend

↓

FastAPI

↓

Download

↓

PDF

LaTeX

JSON

---

# Không được

- Gọi n8n trực tiếp.
- Gọi Python trực tiếp.
- Đọc file JSON trực tiếp.
- Đọc Database trực tiếp.

---

# Quy tắc

- Mọi dữ liệu đều đi qua FastAPI.
- Frontend không xử lý nghiệp vụ.
- Frontend chỉ hiển thị dữ liệu.
- Frontend không sinh đề.
- Frontend không xử lý AI.