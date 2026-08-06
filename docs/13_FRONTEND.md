# FRONTEND

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Frontend là giao diện người dùng. Chỉ giao tiếp với FastAPI.
Không gọi trực tiếp n8n hoặc Python.

---

# Kiến trúc

Frontend → FastAPI → n8n → Python

---

# Chức năng

Đăng nhập, Đăng ký, Chat AI, Sinh đề, Làm bài Online, Chấm bài,
Phân tích học tập, Tải PDF, Quản lý lớp học, Quản lý tài khoản.

---

# Trang

Trang chủ → Đăng nhập → Đăng ký → Dashboard → Chat AI → Sinh đề
→ Làm bài → Nộp bài → Kết quả → Phân tích học tập → Quản lý tài khoản

---

# Dashboard học sinh

Thông tin cá nhân, lịch sử học tập, đề đã tạo, điểm số, thống kê,
nhận xét từ CHV_Analyzer, nút "Luyện tập ngay" theo gợi ý.

---

# Dashboard giáo viên

Danh sách lớp, danh sách học sinh, thống kê, quản lý đề.

---

# Chat AI

Frontend → FastAPI → WF000_Gateway → CHV_Fun → Workflow phù hợp
→ Response

---

# Sinh đề

Frontend → FastAPI → WF001_GenerateExam → Exam Object → PDF/Web Test
→ Frontend

---

# Làm bài Online → Nộp bài → Chấm điểm

Frontend → FastAPI → Web Test → Nộp bài → WF007_GradeExam
→ Kết quả chấm + Nhận xét (CHV_Analyzer)

---

# Nút gợi ý luyện tập tiếp theo

Sau khi nhận Learning Report, Frontend hiển thị nút bấm với
tham số đã có sẵn từ goi_y_lenh_tiep_theo/tham_so_goi_y của
CHV_Analyzer. Bấm nút này gọi thẳng WF001_GenerateExam,
KHÔNG cần gọi lại CHV_Fun để phân tích ngôn ngữ tự nhiên.

---

# Tải file

Frontend → FastAPI → Download → PDF / LaTeX / JSON

---

# Không được

- Gọi n8n trực tiếp.
- Gọi Python trực tiếp.
- Đọc file JSON trực tiếp.
- Đọc Database trực tiếp.

---

# Quy tắc

- Mọi dữ liệu đều đi qua FastAPI.
- Frontend không xử lý nghiệp vụ, chỉ hiển thị dữ liệu.
- Frontend không sinh đề, không xử lý AI.


===============================================================================

# Trạng thái triển khai thực tế (cập nhật 2026-08-06)

Xem chi tiết ở docs/16_CHANGELOG.md, Version 2.4.

Đã có

- Đăng nhập / Đăng ký (Supabase Auth, cookie HttpOnly).
- /chat bắt buộc đăng nhập, chưa đăng nhập thì chuyển hướng /login.
- Chat AI: sinh đề qua hội thoại tự nhiên, giữ đúng 1
  conversation_id trong suốt phiên chat (không tạo lại khi gửi tin
  nhắn tiếp theo).
- Xuất đáp án: hỏi tiếp trong cùng hội thoại, tái sử dụng đề vừa
  tạo, không sinh lại đề.
- Lịch sử hội thoại thật ở sidebar (đọc từ chat_history qua
  GET /api/chat/history), bấm vào 1 mục sẽ mở lại đúng nội dung.
- Nút "Về trang chủ".

Chưa có (theo đúng mục tiêu doc này, để làm ở giai đoạn sau)

- Dashboard học sinh / giáo viên.
- Làm bài Online / Nộp bài / Chấm bài (WF007 chưa triển khai).
- Phân tích học tập (CHV_Analyzer, WF003 chưa triển khai).
- Nút "Luyện tập ngay".
- Quản lý lớp học / quản lý tài khoản.
