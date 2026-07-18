# NAMING CONVENTIONS

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Chuẩn hóa toàn bộ quy tắc đặt tên trong dự án.

Áp dụng cho

- AI Agents
- Code Nodes
- Python
- API
- JSON
- Database
- Frontend
- LaTeX
- n8n
- GitHub

---

# Quy tắc chung

- Không dấu.
- Không khoảng trắng.
- snake_case cho file.
- PascalCase cho Class.
- camelCase chỉ dùng khi bắt buộc.
- ID luôn viết IN HOA.

---

# AI Agent

Format

CHV_<Tên>

Ví dụ

CHV_RequestParser

CHV_ExamPlanner

CHV_Tutor

CHV_Analyzer

CHV_SolutionWriter

---

# Code Node

Format

CN_<Tên>

Ví dụ

CN_LoadExamScope

CN_LoadCurriculum

CN_LoadMapping

CN_BuildCandidatePool

CN_QuestionSelector

CN_CallPythonGenerator

CN_QuestionValidator

CN_ExamAssembler

CN_GenerateLatex

CN_ResponseFormatter

---

# Workflow

Format

WFxxx

Ví dụ

WF001_ExamGeneration

WF002_OnlineExam

WF003_AIChat

WF004_Analysis

---

# API

Format

/api/<module>/<action>

Ví dụ

/api/data/ppct

/api/data/curriculum

/api/data/mapping

/api/exam/generate

/api/exam/history

/api/chat

---

# Python Folder

data/python_bank

↓

toan10

↓

toan11

↓

toan12

---

# Python File

Một chương

=

Một file

Ví dụ

L10_C1.py

L10_C2.py

L11_C3.py

L12_C5.py

---

# Python Function

Tên hàm

=

ID

Ví dụ

L10_C1_B2_VD020_TL_A

Không đổi tên.

---

# PPCT

Một khối

=

Một file JSON

Ví dụ

toan10.json

toan11.json

toan12.json

---

# Curriculum

Một chương

=

Một file JSON

Ví dụ

L10_C1.json

L10_C2.json

L11_C4.json

---

# Mapping

Một chương

=

Một file JSON

Ví dụ

L10_C1.json

L10_C2.json

---

# Database

snake_case

Ví dụ

profiles

exam_history

chat_sessions

question_statistics

---

# Database Column

snake_case

Ví dụ

created_at

updated_at

student_id

teacher_id

exam_id

---

# Frontend

snake_case

Ví dụ

chat.html

dashboard_teacher.html

exam_generate.html

---

# CSS

kebab-case

Ví dụ

chat-box

exam-card

student-table

---

# JavaScript Function

camelCase

Ví dụ

loadExam()

sendMessage()

generateExam()

---

# JSON Key

snake_case

Ví dụ

lesson_id

chapter_id

difficulty

question_type

---

# LaTeX Template

snake_case

Ví dụ

exam.tex

answer.tex

solution.tex

---

# Image

snake_case

Ví dụ

parabola_01.png

graph_circle.png

---

# Upload

UUID

↓

Tên file gốc

Ví dụ

550e8400_exam.pdf

---

# Git Branch

main

dev

feature/<name>

fix/<name>

---

# Git Commit

Ví dụ

feat: add question selector

fix: latex compile error

docs: update workflow

refactor: python generator

---

# Không được

Không viết tiếng Việt có dấu.

Không viết tên file có khoảng trắng.

Không đổi ID sau khi phát hành.

---

# Quy tắc quan trọng

ID là khóa chính của toàn bộ hệ thống.

Một khi đã phát hành

↓

Không đổi.

---

# TODO

Quy tắc đặt tên Test.

Quy tắc đặt tên Docker.

Quy tắc đặt tên Cache.

Quy tắc đặt tên Redis.

Quy tắc đặt tên Queue.