# SYSTEM MAP

Version: 1.0

Trạng thái

🟢 Kiến trúc tổng thể

---

# Mục tiêu

Tài liệu này là bản đồ của toàn bộ hệ thống.

Mỗi thành phần chỉ mô tả ngắn gọn:

- Là gì.
- Làm gì.
- Nằm ở đâu.

Không mô tả chi tiết.

Chi tiết xem ở từng file tương ứng.

---

# Kiến trúc tổng thể

User

↓

Frontend

↓

FastAPI

↓

n8n

↓

Python

↓

LaTeX

↓

PDF / Web Test

↓

Supabase

---

# AI Agents

| AI | Nhiệm vụ | Tài liệu |
|-----|----------|----------|
| CHV_RequestParser | Phân tích yêu cầu | 07_AI_AGENTS |
| CHV_ExamPlanner | Sinh Blueprint | 07_AI_AGENTS |
| CHV_Tutor | Gia sư AI | TODO |
| CHV_Analyzer | Phân tích kết quả | TODO |
| CHV_SolutionWriter | Sinh lời giải AI | TODO |

---

# Code Nodes

| Node | Nhiệm vụ | Tài liệu |
|------|----------|----------|
| CN_LoadExamScope | Đọc PPCT | 08_CODE_NODES |
| CN_LoadCurriculum | Đọc Curriculum | 08 |
| CN_LoadMapping | Đọc Mapping | 08 |
| CN_BuildCandidatePool | Ghép Candidate Pool | 08 |
| CN_QuestionSelector | Chọn ID Python | 08 |
| CN_CallPythonGenerator | Gọi Python | 08 |
| CN_QuestionValidator | Kiểm tra câu hỏi | 08 |
| CN_ExamAssembler | Ghép đề | 08 |
| CN_GenerateLatex | Sinh LaTeX | 08 |
| CN_ResponseFormatter | Trả JSON | 08 |

---

# Workflow

| Workflow | Chức năng |
|----------|-----------|
| WF001 | Sinh đề |
| WF002 | Thi Online |
| WF003 | Chat AI |
| WF004 | Chấm bài |
| WF005 | Dashboard |
| WF006 | Gia sư AI |

---

# APIs

| API | Chức năng |
|------|-----------|
| /api/data/ppct | PPCT |
| /api/data/curriculum | Curriculum |
| /api/data/mapping | Mapping |
| /api/chat | Chat |
| /api/exam/generate | Sinh đề |
| /api/exam/history | Lịch sử |

---

# Python

```
data/python_bank/
```

Một chương

↓

Một file Python

↓

Nhiều hàm

---

# JSON

PPCT

↓

Curriculum

↓

Mapping

---

# Database

Supabase

↓

Profiles

↓

Classes

↓

Exam History

↓

Online Exam

↓

AI Logs

---

# Frontend

Trang chủ

↓

Chat

↓

Dashboard

↓

Sinh đề

↓

Thi Online

↓

Lịch sử

↓

Quản trị

---

# Documents

| File | Nội dung |
|------|----------|
| 00 | Tổng quan |
| 01 | Kiến trúc |
| 02 | Folder |
| 03 | Data |
| 04 | ID |
| 05 | API |
| 06 | Workflow |
| 07 | AI Agents |
| 08 | Code Nodes |
| 09 | Exam Generation |
| 10 | Python Generator |
| 11 | LaTeX |
| 12 | Database |
| 13 | Frontend |
| 14 | Deployment |
| 15 | Roadmap |
| 16 | Changelog |
| 17 | Naming |
| 18 | Prompt Library |
| 19 | System Map |

---

# Quy tắc đọc tài liệu

Nếu cần biết

Kiến trúc

↓

01

Nếu cần biết

ID

↓

04

Nếu cần biết

Workflow

↓

06

Nếu cần biết

AI

↓

07

Nếu cần biết

Code Node

↓

08

Nếu cần biết

Sinh đề

↓

09

Nếu cần biết

Python

↓

10

Nếu cần biết

Database

↓

12

Nếu cần biết

Frontend

↓

13

Nếu cần biết

Deployment

↓

14

Nếu cần biết

Prompt

↓

18

---

# TODO

Cập nhật khi có AI mới.

Cập nhật khi có Workflow mới.

Cập nhật khi có API mới.

Cập nhật khi có Database mới.