# EXAM GENERATION

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

WF001_GenerateExam chịu trách nhiệm sinh đề thi.

Workflow này chỉ được gọi từ WF000_Gateway.

Không được gọi trực tiếp từ Frontend.

---

# Đầu vào

Request JSON

↓

Blueprint

↓

Curriculum

↓

Mapping

---

# Luồng tổng thể

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

Question IDs

↓

CN_CallPythonGenerator

↓

Question Objects

↓

CN_QuestionValidator

↓

Validated Questions

↓

CN_ExamAssembler

↓

Exam Object

↓

Switch_OutputFormat

↓

LaTeX

Web Test

JSON

↓

Response

---

===============================================================================

# Giai đoạn 1

Request Parsing

-------------------------------------------------------------------------------

AI

CHV_RequestParser

Input

Message

Output

Request JSON

---

===============================================================================

# Giai đoạn 2

Blueprint

-------------------------------------------------------------------------------

AI

CHV_ExamPlanner

Input

Request

PPCT

Output

Blueprint

Blueprint quy định

- chương
- bài
- số câu
- mức độ
- loại câu
- tỉ lệ

Blueprint KHÔNG chứa Question ID.

---

===============================================================================

# Giai đoạn 3

Candidate Pool

-------------------------------------------------------------------------------

Input

Blueprint

Curriculum

Mapping

Output

Candidate Pool

Candidate Pool gồm toàn bộ năng lực có thể sử dụng.

Chưa chọn câu.

---

===============================================================================

# Giai đoạn 4

Question Selector

-------------------------------------------------------------------------------

Input

Candidate Pool

Blueprint

Output

Question IDs

Ví dụ

L10_C1_B1_TH014_MC_A

L10_C1_B2_VD020_TL_A

...

Đây là bước quyết định sẽ gọi hàm Python nào.

---

===============================================================================

# Giai đoạn 5

Python Generator

-------------------------------------------------------------------------------

Input

Question IDs

Output

Question Objects

Ví dụ

PY_L10_C1.py

↓

L10_C1_B2_VD020_TL_A()

↓

Question Object

Một Question Object gồm

- nội dung
- đáp án
- lời giải
- metadata
- latex
- hình ảnh (nếu có)

---

===============================================================================

# Giai đoạn 6

Question Validator

-------------------------------------------------------------------------------

Kiểm tra

- trùng ID
- trùng nội dung
- đúng Blueprint
- đúng chương
- đúng bài
- đúng mức độ
- đúng loại câu

Nếu lỗi

↓

Sinh lại Question ID

↓

Gọi lại Python

---

===============================================================================

# Giai đoạn 7

Exam Object

-------------------------------------------------------------------------------

Input

Validated Questions

Output

Exam Object

Exam Object là dữ liệu chuẩn của toàn bộ hệ thống.

Mọi định dạng đầu ra đều sinh từ Exam Object.

---

===============================================================================

# Giai đoạn 8

Output

-------------------------------------------------------------------------------

Switch_OutputFormat

↓

latex

↓

Generate tex

↓

Compile pdf

----------------------------

web_test

↓

Generate Online Test

----------------------------

json

↓

Generate JSON

---

===============================================================================

# Question Object

Question Object là đơn vị nhỏ nhất của đề.

Question Object không phụ thuộc định dạng xuất.

---

===============================================================================

# Exam Object

Exam Object là đơn vị lớn nhất.

Exam Object gồm

- thông tin đề
- danh sách Question Object
- đáp án
- metadata
- thống kê

---

===============================================================================

# Quy tắc

- Blueprint không chứa Question ID.
- Candidate Pool không chứa câu hỏi.
- Question Selector chỉ chọn ID.
- Python chỉ sinh Question Object.
- Validator không sửa câu hỏi.
- Exam Object là trung tâm.
- PDF, Web Test và JSON đều sinh từ Exam Object.

---

# TODO

- Sinh DOCX
- Sinh Moodle XML
- Sinh QTI
- Sinh SCORM