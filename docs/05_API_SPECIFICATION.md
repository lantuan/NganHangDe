# API SPECIFICATION

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Toàn bộ Frontend, n8n và Python chỉ giao tiếp thông qua FastAPI.

Không Node nào được đọc file trực tiếp nếu đã có API.

---

# Kiến trúc

Frontend

↓

FastAPI

↓

Data

↓

n8n

↓

Python

---

# API

## PPCT

GET

```
/api/data/ppct/{subject}
```

Ví dụ

```
/api/data/ppct/toan10
```

Output

PPCT JSON

---

## Curriculum

GET

```
/api/data/curriculum/{subject}/{chapter}
```

Ví dụ

```
/api/data/curriculum/toan10/L10_C1
```

Output

Curriculum JSON

---

## Mapping

GET

```
/api/data/mapping/{subject}/{chapter}
```

Ví dụ

```
/api/data/mapping/toan10/L10_C1
```

Output

Mapping JSON

---

## Python Bank

GET

```
/api/data/python_bank/{subject}/{chapter}
```

Output

Generator Information

Không trả source code.

---

# Generate Exam

POST

```
/api/exam/generate
```

Input

Blueprint

Output

Exam Object

---

# Generate PDF

POST

```
/api/exam/pdf
```

Input

Exam Object

Output

PDF

---

# Generate LaTeX

POST

```
/api/exam/latex
```

Input

Exam Object

Output

.tex

---

# Generate Web Test

POST

```
/api/exam/web
```

Input

Exam Object

Output

Web Test JSON

---

# Student Analysis

POST

```
/api/student/analysis
```

Input

Student ID

Output

Learning Report

---

# Download

GET

```
/api/download/{file_id}
```

Output

PDF

LaTeX

JSON

---

# Upload

POST

```
/api/upload
```

Output

File ID

---

# Authentication

POST

```
/api/auth/login
```

---

POST

```
/api/auth/register
```

---

POST

```
/api/auth/logout
```

---

GET

```
/api/auth/me
```

---

# Admin

GET

```
/api/admin/users
```

---

GET

```
/api/admin/classes
```

---

POST

```
/api/admin/create_class
```

---

# Response chuẩn

Mọi API đều trả về

```json
{
    "success": true,
    "message": "",
    "data": {}
}
```

Nếu lỗi

```json
{
    "success": false,
    "message": "Error message",
    "data": null
}
```

---

# Quy tắc

- Frontend không đọc file trực tiếp.
- n8n không đọc file trực tiếp nếu có API.
- Python không trả dữ liệu cho Frontend.
- Mọi dữ liệu đều đi qua FastAPI.
- API chỉ trả JSON hoặc File.
- Không trả HTML.