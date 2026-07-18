# N8N WORKFLOW

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Toàn bộ nghiệp vụ của hệ thống được triển khai bằng nhiều Workflow độc lập.

Mỗi Workflow chỉ thực hiện một nhiệm vụ.

Workflow không xử lý nhiều chức năng cùng lúc.

---

# Danh sách Workflow

| Workflow | Chức năng |
|----------|-----------|
| WF000_Gateway | Điều phối toàn bộ hệ thống |
| WF001_GenerateExam | Sinh đề |
| WF002_GenerateExamByAbility | Sinh đề theo năng lực |
| WF003_StudentAnalysis | Phân tích học tập |
| WF004_DownloadFile | Tải file |
| WF005_Help | Hướng dẫn sử dụng |
| WF006_Reject | Từ chối yêu cầu |

---

# WF000_Gateway

Đây là Workflow đầu tiên.

Mọi request đều đi qua Workflow này.

Luồng

Webhook

↓

CHV_Fun

↓

Switch

↓

Execute Workflow

---

# Switch

Task

↓

Workflow

generate_exam

↓

WF001_GenerateExam

----------------------------

generate_exam_by_ability

↓

WF002_GenerateExamByAbility

----------------------------

student_analysis

↓

WF003_StudentAnalysis

----------------------------

download_file

↓

WF004_DownloadFile

----------------------------

help

↓

WF005_Help

----------------------------

reject_math_solution

↓

WF006_Reject

----------------------------

reject_out_of_scope

↓

WF006_Reject

---

# WF001_GenerateExam

Luồng

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

↓

CN_ResponseFormatter

---

# Switch_OutputFormat

latex

↓

Generate LaTeX

↓

Compile PDF

------------------------

web_test

↓

Generate Web Test

------------------------

json

↓

Generate JSON

---

# WF002_GenerateExamByAbility

Load Student History

↓

Load Weak Knowledge

↓

CHV_AbilityPlanner

↓

WF001_GenerateExam

---

# WF003_StudentAnalysis

Load Student History

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

# Execute Workflow

Các Workflow liên kết với nhau bằng Execute Workflow.

Không gọi trực tiếp Code Node giữa các Workflow.

---

# Quy tắc

- Một Workflow chỉ thực hiện một nhiệm vụ.
- Mỗi AI chỉ thuộc một Workflow.
- Mỗi Code Node chỉ thuộc một Workflow.
- WF000 là cổng vào duy nhất.
- Không tạo Workflow đa nhiệm.

---

# TODO

- WF007_AI_Tutor
- WF008_ExerciseRecommendation
- WF009_ReviewMistakes
- WF010_ClassDashboard