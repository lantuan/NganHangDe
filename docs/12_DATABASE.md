# DATABASE

Version: 1.0

Trạng thái

🟡 Đang triển khai

---

# Mục tiêu

Chuẩn hóa toàn bộ Database của hệ thống.

Database là nơi lưu dữ liệu.

Không xử lý Business Logic.

---

# Database

Supabase (PostgreSQL)

---

# Nguyên tắc

- Không lưu dữ liệu trùng.
- Không lưu dữ liệu sinh ra từ Python.
- Không lưu dữ liệu tạm.
- Chỉ lưu dữ liệu cần sử dụng lâu dài.

---

# Kiến trúc

Frontend

↓

FastAPI

↓

Supabase

↓

PostgreSQL

---

# Nhóm bảng

## Authentication

auth.users

profiles

---

## Người dùng

profiles

teachers

students

classes

class_members

---

## Đề thi

exam_templates

exam_blueprints

exam_versions

exam_history

---

## Thi Online

online_exams

online_attempts

attempt_answers

---

## AI

chat_sessions

chat_messages

ai_logs

---

## Ngân hàng câu hỏi

question_history

favorite_questions

question_statistics

---

## Thống kê

student_statistics

teacher_statistics

dashboard_cache

---

## Hệ thống

settings

logs

jobs

---

# profiles

Lưu thông tin người dùng.

---

# teachers

Thông tin giáo viên.

---

# students

Thông tin học sinh.

---

# classes

Danh sách lớp.

---

# class_members

Quan hệ

Học sinh

↓

Lớp

---

# exam_templates

Lưu mẫu đề.

Không lưu PDF.

---

# exam_blueprints

Lưu Blueprint AI sinh.

---

# exam_versions

Lưu các phiên bản đề.

Ví dụ

A

B

C

D

---

# exam_history

Lưu lịch sử sinh đề.

---

# online_exams

Thông tin bài thi Online.

---

# online_attempts

Thông tin mỗi lần làm bài.

---

# attempt_answers

Chi tiết từng câu trả lời.

---

# chat_sessions

Một cuộc trò chuyện.

---

# chat_messages

Từng tin nhắn.

---

# ai_logs

Log AI.

---

# question_history

Lưu ID Python đã sử dụng.

Không lưu câu hỏi.

---

# favorite_questions

TODO

---

# question_statistics

Thống kê số lần xuất hiện.

---

# student_statistics

Dashboard học sinh.

---

# teacher_statistics

Dashboard giáo viên.

---

# dashboard_cache

Cache Dashboard.

---

# settings

Thiết lập hệ thống.

---

# logs

Log hệ thống.

---

# jobs

Background Jobs.

---

# Không lưu

Không lưu

PPCT

Curriculum

Mapping

Python

Các file JSON

LaTeX

PDF

Các dữ liệu này đọc trực tiếp từ Repository.

---

# Quan hệ

Frontend

↓

FastAPI

↓

Supabase

↓

Database

---

# TODO

Thiết kế ERD.

Thiết kế Index.

Thiết kế Foreign Key.

Thiết kế RLS.

Thiết kế Backup.

Thiết kế Migration.

Thiết kế Cache.

Thiết kế Audit Log.


