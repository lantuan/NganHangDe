# QUY ƯỚC ĐẶT TÊN

Version: 1.0

---

# Mục tiêu

Toàn bộ dự án phải thống nhất cách đặt tên.

Không đặt tên theo cảm hứng.

Không dùng nhiều kiểu đặt tên khác nhau.

---

# 1. AI Agent

Tiền tố

CHV_

Ví dụ

CHV_RequestParser

CHV_ExamPlanner

CHV_BlueprintPlanner

CHV_SolutionWriter

CHV_Analysis

CHV_Tutor

---

# 2. Code Node

Tiền tố

CN_

Ví dụ

CN_LoadExamScope

CN_LoadQuestionPool

CN_FilterDifficulty

CN_FilterLesson

CN_CallPythonGenerator

CN_GenerateLatex

CN_CreatePDF

CN_ResponseFormatter

---

# 3. Workflow

Tiền tố

WF_

Ví dụ

WF_ExamGeneration

WF_ExamAnalysis

WF_StudentLearning

WF_AIChat

---

# 4. FastAPI Router

snake_case

Ví dụ

exam_scope.py

question_pool.py

latex.py

generator.py

student.py

teacher.py

---

# 5. FastAPI Service

snake_case

Ví dụ

exam_scope_service.py

generator_service.py

pdf_service.py

curriculum_service.py

---

# 6. API

RESTful

Ví dụ

/api/exam/scope

/api/exam/question_pool

/api/exam/generate

/api/student/history

/api/teacher/dashboard

---

# 7. Python Generator

Tên file

L10_C1.py

L10_C2.py

L11_C1.py

...

---

# 8. Hàm Generator

Ví dụ

L10_C1_B2_NB017A_MC_A()

L10_C1_B2_TH014_DS_B()

L10_C3_B1_VD020_TL_A()

---

# 9. JSON

snake_case

Ví dụ

curriculum.json

mapping.json

exam_scope.json

question_pool.json

---

# 10. Database

snake_case

Ví dụ

lesson_id

question_id

student_id

teacher_id

created_at

updated_at

---

# 11. Constant

UPPER_CASE

Ví dụ

MAX_QUESTION

DEFAULT_LEVEL

SUPABASE_URL

---

# 12. Biến Python

snake_case

Ví dụ

lesson_id

question_pool

exam_scope

student_result

---

# 13. Class

PascalCase

Ví dụ

ExamScope

QuestionPool

LatexGenerator

ExamPlanner

---

# 14. Không sử dụng

Tên tiếng Việt.

Tên có dấu.

Tên có khoảng trắng.

Tên viết tắt không rõ nghĩa.

---

# Quy tắc

Nhìn tên phải biết ngay chức năng.

Tên phải thống nhất trên:

FastAPI

↓

n8n

↓

Python

↓

Database

↓

AI

↓

Tài liệu