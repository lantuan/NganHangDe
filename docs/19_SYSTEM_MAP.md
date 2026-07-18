# SYSTEM MAP

Version: 1.0

---

# AI Agents

## CHV_RequestParser

File:
07_AI_AGENTS.md

Nhiệm vụ:
- Phân tích yêu cầu người dùng.
- Chuẩn hóa thành JSON.

Không được:
- Đọc PPCT.
- Đọc Curriculum.
- Đọc Mapping.
- Sinh câu hỏi.

---

## CHV_ExamPlanner

File:
07_AI_AGENTS.md

Nhiệm vụ:
- Sinh Blueprint.

Không được:
- Sinh câu hỏi.
- Gọi Python.

---

## CHV_SolutionWriter

TODO

---

## CHV_Tutor

TODO

---

## CHV_Analyzer

TODO

---

# Code Nodes

## CN_LoadExamScope

File:
08_CODE_NODES.md

Nhiệm vụ:
- Gọi API PPCT.
- Xác định lesson_id.

---

## CN_LoadCurriculum

- Gọi API Curriculum.

---

## CN_LoadMapping

- Gọi API Mapping.

---

## CN_BuildCandidatePool

- Ghép Blueprint.
- Ghép Curriculum.
- Ghép Mapping.
- Sinh Candidate Pool.

---

## CN_QuestionSelector

- Chọn ID Python.
- Chống trùng.
- Chọn phiên bản.
- Đúng ma trận.

---

## CN_CallPythonGenerator

- Import file Python.
- Gọi hàm.

---

## CN_QuestionValidator

- Kiểm tra câu hỏi.
- Kiểm tra đáp án.
- Kiểm tra LaTeX.

---

## CN_ExamAssembler

- Ghép đề.

---

## CN_ResponseFormatter

- Chuẩn hóa JSON.

---

# APIs

## /api/data/ppct/{grade}

PPCT.

---

## /api/data/curriculum/{chapter}

Curriculum.

---

## /api/data/mapping/{chapter}

Mapping.

---

## /api/exam/generate

TODO

---

# Python

## data/python_bank/toan10/L10_C1.py

Chứa toàn bộ hàm sinh câu hỏi Chương 1.

---

# Workflow

WF001

Sinh đề.

WF002

Làm bài.

WF003

Chấm bài.

WF004

Gia sư.

---

# Frontend

Trang chủ

Đăng nhập

Đăng ký

Chat AI

Dashboard

Thi Online

Lịch sử

---

# Database

profiles

exam_history

...

---

# TODO

Hoàn thiện khi hệ thống phát triển.