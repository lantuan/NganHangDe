# KIẾN TRÚC HỆ THỐNG

Version: 1.0

---

# 1. Mục tiêu

Kiến trúc được thiết kế theo hướng:

- Module hóa.
- Dễ mở rộng.
- Tách biệt dữ liệu.
- Giảm phụ thuộc vào AI.
- Có thể thay đổi từng thành phần mà không ảnh hưởng toàn hệ thống.

---

# 2. Kiến trúc tổng thể

```text
                         USER
                           │
                   Web Browser
                           │
──────────────────────────HTTP──────────────────────────
                           │
                       FastAPI
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      │                    │                    │
 Authentication        Business API       Static Web
      │                    │
      │                    ▼
      │              n8n Workflow
      │                    │
      │        ┌───────────┼────────────┐
      │        │           │            │
      │     Code Node   AI Agent   Python
      │        │           │            │
      │        └───────────┼────────────┘
      │                    │
      ▼                    ▼
                 LaTeX / PDF Engine
                           │
                    Web Test Engine
                           │
                     Student Result
                           │
                     AI Analysis
                           │
                        Dashboard
```

---

# 3. Thành phần

## 3.1 Frontend

Chức năng

- Đăng nhập
- Chat AI
- Sinh đề
- Làm bài
- Dashboard

Không chứa nghiệp vụ.

---

## 3.2 FastAPI

Là trung tâm của hệ thống.

Chịu trách nhiệm:

- API
- Authentication
- đọc dữ liệu
- gọi Python
- gọi n8n
- trả kết quả

FastAPI là tầng duy nhất được phép truy cập dữ liệu.

---

## 3.3 n8n

Vai trò:

Workflow Orchestrator.

Không xử lý nghiệp vụ.

Không đọc JSON.

Không xử lý Python.

Không tự sinh dữ liệu.

---

## 3.4 Python Generator

Sinh câu hỏi.

Sinh đáp án.

Sinh lời giải chuẩn.

Không sử dụng AI.

---

## 3.5 AI Agent

Chỉ xử lý các nhiệm vụ cần suy luận.

Ví dụ

- hiểu yêu cầu
- lập kế hoạch
- giải thích
- gia sư AI

---

## 3.6 Database

Supabase.

Lưu

- User
- History
- Exam
- Result
- Dashboard

---

# 4. Nguyên tắc

Business Logic

↓

FastAPI

Workflow

↓

n8n

Mathematics

↓

Python

Reasoning

↓

AI

Presentation

↓

Frontend

---

# 5. Nguyên tắc phát triển

Không để Business Logic nằm trong Prompt.

Không để Business Logic nằm trong n8n.

Không để AI đọc dữ liệu thô.

Mọi dữ liệu đều phải đi qua API.

Code phải quyết định.

AI chỉ hỗ trợ quyết định.

---

# 6. Luồng sinh đề

User

↓

FastAPI

↓

n8n

↓

Code Node

↓

Business API

↓

Python Generator

↓

LaTeX

↓

PDF

↓

Web

---

# 7. Luồng học sinh

Làm bài

↓

Nộp bài

↓

Chấm

↓

AI Phân tích

↓

Dashboard

↓

AI Tutor

---

# 8. Luồng giáo viên

Đăng nhập

↓

Tạo đề

↓

Quản lý đề

↓

Theo dõi học sinh

↓

Phân tích lớp

↓

Điều chỉnh lộ trình