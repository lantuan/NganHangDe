# FRONTEND

Version: 1.0

Trạng thái

🟡 Đang triển khai

---

# Mục tiêu

Frontend chỉ chịu trách nhiệm hiển thị dữ liệu.

Không xử lý Business Logic.

Không sinh đề.

Không gọi Python trực tiếp.

Mọi xử lý đều thông qua FastAPI.

---

# Công nghệ

Frontend

↓

FastAPI Template

↓

HTML

↓

Tailwind CSS

↓

JavaScript

(Tương lai có thể chuyển React / NextJS)

---

# Kiến trúc

Browser

↓

Frontend

↓

FastAPI API

↓

n8n

↓

Python

↓

FastAPI

↓

Frontend

---

# Module

## Trang chủ

index.html

---

## Đăng nhập

dangnhap.html

---

## Đăng ký

dangky.html

---

## Chat AI

chat.html

---

## Dashboard học sinh

dashboard_student.html

---

## Dashboard giáo viên

dashboard_teacher.html

---

## Sinh đề

exam_generate.html

---

## Làm bài Online

exam_online.html

---

## Kết quả bài làm

exam_result.html

---

## Lịch sử

history.html

---

## Quản lý lớp

classes.html

---

## Quản lý học sinh

students.html

---

## Cài đặt

settings.html

---

# Nguyên tắc

Frontend

↓

Hiển thị

↓

Không xử lý dữ liệu.

---

# API

Frontend chỉ gọi

FastAPI.

Không gọi

Supabase.

Không gọi

Python.

Không gọi

n8n.

---

# Authentication

Supabase Auth.

---

# Session

JWT

(TODO)

---

# Chat AI

Input

↓

FastAPI

↓

n8n

↓

FastAPI

↓

Frontend

---

# Sinh đề

Frontend

↓

POST

/api/exam/generate

↓

Hiển thị kết quả.

---

# Thi Online

Frontend

↓

API

↓

Lưu đáp án.

---

# Dashboard

Frontend

↓

API

↓

Biểu đồ.

---

# Upload

Frontend

↓

FastAPI

↓

uploads/

---

# Download

Frontend

↓

FastAPI

↓

PDF

↓

LaTeX

---

# Loading

Hiển thị

Spinner.

---

# Error

Hiển thị

Toast.

---

# Theme

Light

Dark (TODO)

---

# Responsive

Desktop

Tablet

Mobile

---

# Components

Button

Card

Modal

Dialog

Sidebar

Navbar

Chat Box

Exam Card

Statistic Card

Table

Chart

---

# UI Rule

Không viết Business Logic.

Không tính toán.

Không đọc JSON trực tiếp.

---

# Quan hệ

Frontend

↓

FastAPI

↓

API

↓

n8n

↓

Python

---

# TODO

Thiết kế Design System.

Thiết kế Component Library.

Thiết kế Dashboard.

Thiết kế Exam UI.

Thiết kế Chat UI.

Thiết kế Responsive.

Thiết kế Dark Mode.

Thiết kế Animation.

Thiết kế Notification.

Thiết kế Loading Skeleton.