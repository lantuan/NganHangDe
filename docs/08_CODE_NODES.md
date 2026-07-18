# CODE NODES

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Code Node chỉ xử lý dữ liệu.

Không thực hiện suy luận AI.

Không sinh câu hỏi.

Không sinh đề.

Không thay thế Python Generator.

---

# Quy tắc đặt tên

CN_<Tên>

Ví dụ

CN_ParseRequest

CN_LoadCurriculum

CN_LoadMapping

CN_BuildCandidatePool

CN_QuestionSelector

CN_CallPythonGenerator

CN_QuestionValidator

CN_ExamAssembler

CN_ResponseFormatter

---

# WF001_GenerateExam

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

CN_QuestionValidator

↓

CN_ExamAssembler

↓

Switch_OutputFormat

↓

CN_ResponseFormatter

---

===============================================================================

CN_ParseRequest

-------------------------------------------------------------------------------

Input

Request JSON

Output

Request Object

Nhiệm vụ

- Chuẩn hóa dữ liệu.
- Kiểm tra dữ liệu bắt buộc.
- Chuyển kiểu dữ liệu.

Không được

- Suy luận.
- Gọi AI.

===============================================================================

CN_LoadCurriculum

-------------------------------------------------------------------------------

Input

Blueprint

Output

Curriculum JSON

Nhiệm vụ

- Đọc Curriculum theo chương.

Không được

- Chọn câu.

===============================================================================

CN_LoadMapping

-------------------------------------------------------------------------------

Input

Blueprint

Output

Mapping JSON

Nhiệm vụ

- Đọc Mapping theo chương.

Không được

- Chọn câu.

===============================================================================

CN_BuildCandidatePool

-------------------------------------------------------------------------------

Input

Blueprint

Curriculum

Mapping

Output

Candidate Pool

Nhiệm vụ

Ghép:

Blueprint

+

Curriculum

+

Mapping

↓

Candidate Pool

Không được

- Chọn ID.
- Gọi Python.

===============================================================================

CN_QuestionSelector

-------------------------------------------------------------------------------

Input

Candidate Pool

Blueprint

Output

Question IDs

Nhiệm vụ

Chọn ID phù hợp Blueprint.

Ví dụ

L10_C1_B1_TH014_MC_A

L10_C1_B2_VD020_TL_A

...

Không được

- Sinh câu hỏi.
- Sinh LaTeX.

===============================================================================

CN_CallPythonGenerator

-------------------------------------------------------------------------------

Input

Question IDs

Output

Question Objects

Nhiệm vụ

Gọi đúng hàm Python.

Ví dụ

L10_C1.py

↓

L10_C1_B2_VD020_TL_A()

↓

Question Object

Không được

- Chọn ID.

===============================================================================

CN_QuestionValidator

-------------------------------------------------------------------------------

Input

Question Objects

Output

Validated Questions

Nhiệm vụ

Kiểm tra

- Trùng câu.
- Đúng chương.
- Đúng bài.
- Đúng Blueprint.
- Đúng mức độ.

===============================================================================

CN_ExamAssembler

-------------------------------------------------------------------------------

Input

Validated Questions

Output

Exam Object

Nhiệm vụ

Ghép Question Object thành Exam Object.

Không được

- Sinh PDF.
- Sinh Web Test.

===============================================================================

Switch_OutputFormat

-------------------------------------------------------------------------------

Input

Exam Object

↓

latex

↓

Generate LaTeX

----------------------------

web_test

↓

Generate Web Test

----------------------------

json

↓

Generate JSON

===============================================================================

CN_ResponseFormatter

-------------------------------------------------------------------------------

Input

PDF

Web Test

JSON

Output

Response

Nhiệm vụ

Chuẩn hóa dữ liệu trả về Frontend.

===============================================================================

# Quy tắc

- Một Code Node chỉ làm một việc.
- Không có AI trong Code Node.
- Không có Prompt trong Code Node.
- Không có Python trong Code Node (trừ CN_CallPythonGenerator).
- Không sinh đề trong Code Node.
- Mọi dữ liệu truyền giữa các Node đều là JSON.

===============================================================================

# TODO

- CN_SaveExamHistory
- CN_SaveQuestionHistory
- CN_SaveStudentLog
- CN_CacheQuestion
- CN_CacheBlueprint