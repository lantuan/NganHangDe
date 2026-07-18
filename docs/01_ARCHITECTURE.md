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

Ngân Hàng Đề AI là một nền tảng AI Tutor dành cho học sinh và giáo viên THPT.

Sinh đề chỉ là một chức năng của hệ thống.

Mọi yêu cầu của người dùng đều đi qua một AI điều phối trung tâm trước khi chuyển đến Workflow phù hợp.

---

# Kiến trúc tổng thể

User

↓

Frontend

↓

FastAPI

↓

WF000_Gateway

↓

CHV_Fun

↓

Switch

├── WF001_GenerateExam
│
├── WF002_GenerateExamByAbility
│
├── WF003_StudentAnalysis
│
├── WF004_DownloadFile
│
├── WF005_Help
│
├── WF006_Reject
│
└── Các Workflow mở rộng trong tương lai

---

# WF000_Gateway

WF000 là Workflow điều phối của toàn bộ hệ thống.

WF000 không xử lý nghiệp vụ.

WF000 chỉ thực hiện các nhiệm vụ sau:

- Nhận yêu cầu từ Frontend.
- Gọi AI CHV_Fun.
- Phân loại yêu cầu.
- Điều hướng sang Workflow phù hợp.

---

# CHV_Fun

CHV_Fun là AI điều phối trung tâm.

CHV_Fun không:

- sinh đề;
- giải toán;
- sinh lời giải;
- trả lời kiến thức;
- đọc PPCT;
- đọc Curriculum;
- đọc Mapping.

CHV_Fun chỉ trả về:

{
    "task": "...",
    "message": "..."
}

Task quyết định Workflow tiếp theo.

---

# Kiến trúc WF001_GenerateExam

CHV_RequestParser

↓

CN_ParseRequest

↓

CHV_ExamPlanner

↓

CN_LoadCurriculum

↓

CN_LoadMapping

↓

CN_BuildCandidatePool

↓

CN_QuestionSelector

↓

CN_CallPythonGenerator

↓

Question Objects

↓

CN_QuestionValidator

↓

CN_ExamAssembler

↓

Exam Object

↓

Switch_OutputFormat

├── Generate LaTeX
│      ↓
│   Compile PDF
│
├── Generate Web Test
│      ↓
│   Online Exam
│
└── Generate JSON
       ↓
   API Response

↓

CN_ResponseFormatter

↓

Respond

---

# WF002_GenerateExamByAbility

Student History

↓

Weak Knowledge

↓

CHV_AbilityPlanner

↓

WF001_GenerateExam

---

# WF003_StudentAnalysis

Student History

↓

CHV_Analyzer

↓

Learning Report

↓

Dashboard

---

# WF004_DownloadFile

Find File

↓

Download

---

# WF005_Help

CHV_Help

↓

Response

---

# WF006_Reject

CHV_Reject

↓

Response

---

# Kiến trúc dữ liệu

PPCT

↓

Curriculum

↓

Mapping

↓

Candidate Pool

↓

Question IDs

↓

Question Objects

↓

Exam Object

↓

Output

---

# Các Output chuẩn

Hệ thống chỉ sinh đề một lần.

Sau đó xuất nhiều định dạng khác nhau.

Các định dạng gồm:

- PDF
- LaTeX
- Web Test
- JSON

Trong tương lai có thể bổ sung:

- DOCX
- Moodle XML
- QTI
- SCORM

mà không cần thay đổi quy trình sinh đề.

---

# Nguyên tắc kiến trúc

- WF000 là cổng vào duy nhất của hệ thống.
- CHV_Fun luôn là AI đầu tiên.
- Mỗi Workflow chỉ thực hiện một nhiệm vụ.
- Generate Exam chỉ là một module của AI Tutor.
- Python chỉ sinh Question Objects.
- Exam Object là trung tâm của toàn bộ quy trình sinh đề.
- Mọi định dạng xuất đều được tạo từ cùng một Exam Object.

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