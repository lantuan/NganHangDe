# NGÂN HÀNG ĐỀ TOÁN AI

Repository này dùng để:

- Lưu trữ đề thi Toán
- Quản lý đề LaTeX
- Sinh đề tự động bằng AI
- Tạo ngân hàng đề chuẩn
- Dùng cho n8n, Claude, GPT, NotebookLM

---

# KIẾN TRÚC HỆ THỐNG

Repository gồm 2 hệ riêng biệt:

1. STATIC_EXAMS
2. DYNAMIC_EXAMS

---

# STATIC_EXAMS

Đây là kho đề tĩnh.

Bao gồm:

- đề thật
- đề chuẩn
- đề giáo viên tạo
- đề kiểm chứng

AI chỉ được:
- đọc
- phân tích
- học cấu trúc

AI KHÔNG được:
- sửa nội dung
- đổi format
- thay đổi dữ kiện

---

# DYNAMIC_EXAMS

Đây là hệ sinh đề động bằng AI.

AI được phép:
- sinh đề mới
- tạo biến thể
- random dữ kiện
- tạo đề tương tự

Nhưng phải:
- tuân thủ LATEX_RULES.md
- đúng format
- có lời giải
- đúng mức độ

---

# THỨ TỰ ƯU TIÊN

Khi AI sinh đề:

1. TEMPLATE
2. LATEX_RULES.md
3. STATIC_EXAMS
4. Prompt người dùng

---

# CẤU TRÚC THƯ MỤC

STATIC_EXAMS/
DYNAMIC_EXAMS/
TEMPLATE/

LATEX_RULES.md
AGENT_INSTRUCTIONS.md

---

# FILE QUAN TRỌNG

- LATEX_RULES.md
- AGENT_INSTRUCTIONS.md
- TEMPLATE/de_mau.tex

---

# YÊU CẦU CHUNG

- Mọi bài đều có lời giải
- Dùng UTF-8
- Không đổi cấu trúc
- Không tự ý đổi môi trường LaTeX