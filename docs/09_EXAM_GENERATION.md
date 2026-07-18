# EXAM GENERATION

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định quy trình sinh đề chuẩn của hệ thống.

Mọi hình thức sinh đề đều phải tuân theo Pipeline này.

Bao gồm

- PDF
- LaTeX
- Web Test
- AI Tutor

---

# Nguyên tắc

## 1

AI không sinh câu hỏi.

---

## 2

Python Generator sinh câu hỏi.

---

## 3

AI chỉ lập kế hoạch sinh đề.

---

## 4

Code Node xử lý toàn bộ Business Logic.

---

## 5

Không cho AI đọc toàn bộ JSON.

---

# GOLDEN PIPELINE

User

↓

CHV_RequestParser
# AI
- Phân tích yêu cầu người dùng.
- Chuẩn hóa Request.

↓

CN_LoadExamScope
# Code Node
- Gọi API PPCT.
- Xác định lesson_id.

↓

CHV_ExamPlanner
# AI
- Sinh Blueprint.
- Phân bố số câu theo ma trận.

↓

CN_LoadCurriculum
# Code Node
- Gọi Curriculum API.
- Lấy năng lực.

↓

CN_LoadMapping
# Code Node
- Gọi Mapping API.
- Lấy Loại và Dạng.

↓

CN_BuildCandidatePool
# Code Node
- Ghép
    Blueprint
    +
    Curriculum
    +
    Mapping
- Sinh Candidate Pool.
- Chưa chọn câu.

↓

CN_QuestionSelector
# Code Node
- Chọn ID Python.
- Không trùng câu.
- Không trùng dạng.
- Không trùng template.
- Random phiên bản.
- Đúng Blueprint.
- Đúng ma trận.
- Đúng phân bố.

↓

CN_CallPythonGenerator
# Code Node
- Import file Python theo chương.
- Gọi đúng hàm.

↓

CN_QuestionValidator
# Code Node
- Kiểm tra câu hỏi.
- Kiểm tra đáp án.
- Kiểm tra lời giải.
- Kiểm tra LaTeX.
- Nếu lỗi:
    quay lại QuestionSelector.

↓

CN_ExamAssembler
# Code Node
- Ghép toàn bộ câu.
- Sinh Exam JSON.

↓

CN_GenerateLatex
# Code Node
- Sinh LaTeX.
- Sinh PDF.

↓

CN_ResponseFormatter
# Code Node
- Chuẩn hóa JSON trả về.

↓

Frontend

---

# BƯỚC 1

## Người dùng

Ví dụ

```
Sinh đề giữa kỳ

Lớp 10

Chương Mệnh đề

20 câu

70% trắc nghiệm

30% đúng sai
```

---

Output

↓

Request tự nhiên.

---

# BƯỚC 2

## CHV_RequestParser

Mục tiêu

↓

Chuẩn hóa yêu cầu.

---

Output

Ví dụ

```json
{
    "grade":10,
    "exam_type":"Giữa kỳ",
    "chapter":"Mệnh đề",
    "question_count":20
}
```

---

# BƯỚC 3

## CN_LoadExamScope

Đọc PPCT.

↓

Tìm lesson_id.

---

Ví dụ

```
L10_C1_B1

L10_C1_B2
```

---

Không đọc Curriculum.

---

# BƯỚC 4

## CHV_ExamPlanner

Sinh Blueprint.

---

Ví dụ

```json
[
    {
        "lesson_id":"L10_C1_B1",
        "level":"NB",
        "count":4
    }
]
```

---

Không sinh câu hỏi.

---

# BƯỚC 5

## CN_LoadCurriculum

Đọc Curriculum.

↓

Lấy năng lực.

---

Không gọi AI.

---

# BƯỚC 6

## CN_LoadMapping

Đọc Mapping.

↓

Biết

Loại

Dạng

---

Ví dụ

```
MC

TF

TL
```

---

# BƯỚC 7

## CN_LoadQuestionPool

Ghép

Blueprint

+

Curriculum

+

Mapping

↓

Question Pool

---

Ví dụ

```json
[
"L10_C1_B2_VD020_TL_A",
"L10_C1_B1_NB004_MC_A"
]
```

---

Đây là bước quan trọng nhất.

---

# BƯỚC 8

## CN_CallPythonGenerator

Import Python.

---

Ví dụ

```
L10_C1.py
```

↓

Gọi

```
L10_C1_B2_VD020_TL_A()
```

↓

Sinh câu hỏi.

---

Output

LaTeX

JSON

Đáp án

Lời giải

---

# BƯỚC 9

## CN_ResponseFormatter

Chuẩn hóa dữ liệu.

---

Ví dụ

```json
{
    "exam":{},
    "answer":{},
    "latex":"..."
}
```

---

# BƯỚC 10

## FastAPI

Trả kết quả.

---

# BƯỚC 11

## Frontend

Hiển thị.

---

PDF

LaTeX

Web Test

---

# MA TRẬN ĐỀ

Người dùng

↓

Ma trận đề

↓

Blueprint

↓

Question Pool

↓

Python

---

Không bỏ qua Blueprint.

---

# CURRICULUM

Vai trò

↓

Năng lực.

Không sinh câu hỏi.

---

# MAPPING

Vai trò

↓

Loại câu.

↓

Dạng toán.

---

# PYTHON

Vai trò

↓

Sinh câu hỏi.

↓

Sinh đáp án.

↓

Sinh lời giải.

↓

Sinh LaTeX.

---

# AI

Vai trò

↓

Lập kế hoạch.

↓

Không sinh câu hỏi.

---

# CODE NODE

Vai trò

↓

Business Logic.

---

# FASTAPI

Vai trò

↓

API.

↓

Response.

---

# FRONTEND

Vai trò

↓

Hiển thị.

---

# KHÔNG ĐƯỢC

AI sinh đề.

AI sinh đáp án.

AI sinh LaTeX.

AI đọc Curriculum.

AI đọc Mapping.

AI đọc PPCT.

---

# TODO

Hoàn thiện Blueprint Schema.

Hoàn thiện Matrix Schema.

Hoàn thiện Exam Schema.

Hoàn thiện Response Schema.

Hoàn thiện Web Test Pipeline.

Hoàn thiện PDF Pipeline.

Hoàn thiện LaTeX Pipeline.

Hoàn thiện AI Tutor Pipeline.

Hoàn thiện Dashboard Pipeline.
