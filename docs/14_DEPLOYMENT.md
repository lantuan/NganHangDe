# DEPLOYMENT

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Triển khai toàn bộ hệ thống Ngân Hàng Đề AI lên VPS.

---

# Kiến trúc triển khai

Internet → Nginx → FastAPI → n8n → Python Generator → LaTeX Engine
→ Supabase

---

# Thành phần

## VPS

Chạy FastAPI, n8n, Python, LaTeX.

## FastAPI

Cung cấp API. Giao tiếp Frontend. Giao tiếp n8n.

## n8n

Chạy toàn bộ Workflow:
WF000_Gateway, WF001_GenerateExam, WF002_GenerateExamByAbility,
WF003_StudentAnalysis, WF004_DownloadFile, WF005_Help,
WF006_Reject, WF007_GradeExam.

## Python Generator

Sinh Question Object.

## LaTeX Engine

Sinh .tex, .pdf.

## Supabase

Lưu User, Class, Learning History, Exam History, Metadata.

---

# Thư mục dự án

/root/NganHangDe

---

# Dữ liệu / Kết quả sinh / Log

data/ , output/ , logs/

---

# Khởi động hệ thống

Nginx → FastAPI → n8n → Python

---

# Luồng hoạt động

User → Frontend → FastAPI → WF000_Gateway → Workflow → Python
→ LaTeX → Response

---

# Backup

Source Code, Database, data/, output/

---

# Không triển khai

- Python riêng lẻ.
- n8n riêng lẻ.
- Frontend gọi trực tiếp n8n hoặc Python.

---

# Quy tắc

- Mọi yêu cầu đi qua FastAPI.
- Mọi Workflow chạy trong n8n.
- Python chỉ sinh Question Object.
- LaTeX chỉ sinh PDF.
- Database chỉ lưu dữ liệu.
- Source Code quản lý bằng GitHub.