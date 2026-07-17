# API SPECIFICATION

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định toàn bộ API của hệ thống.

Mọi API đều phải được khai báo tại đây trước khi lập trình.

Không tạo API tùy hứng.

---

# Quy tắc

## RESTful

GET

POST

PUT

DELETE

---

## JSON UTF-8

Toàn bộ Request và Response đều dùng JSON.

---

## Version

Tương lai

```
/api/v1/
```

Hiện tại

```
/api/
```

---

# PHÂN NHÓM API

---

# I. DATA API

Chỉ đọc dữ liệu.

Không xử lý nghiệp vụ.

---

## PPCT

GET

```
/api/data/ppct/{grade}
```

Ví dụ

```
/api/data/ppct/toan10
```

Response

TODO

---

## Curriculum

GET

```
/api/data/curriculum/{chapter}
```

Ví dụ

```
/api/data/curriculum/L10_C1
```

Response

TODO

---

## Mapping

GET

```
/api/data/mapping/{chapter}
```

Ví dụ

```
/api/data/mapping/L10_C1
```

Response

TODO

---

# II. EXAM API

Đây là Business API.

n8n sẽ gọi nhóm API này.

Không xử lý PPCT trong n8n.

---

## Exam Scope

POST

```
/api/exam/scope
```

Mục tiêu

↓

Đổi yêu cầu

↓

lesson_id

Request

TODO

Response

TODO

---

## Question Pool

POST

```
/api/exam/question_pool
```

Request

TODO

Response

TODO

---

## Generate Exam

POST

```
/api/exam/generate
```

Request

TODO

Response

TODO

---

## Generate Latex

POST

```
/api/exam/latex
```

TODO

---

## Generate PDF

POST

```
/api/exam/pdf
```

TODO

---

# III. STUDENT API

---

Login

TODO

---

History

TODO

---

Learning

TODO

---

Dashboard

TODO

---

# IV. TEACHER API

TODO

---

# V. AI API

TODO

---

# VI. DASHBOARD API

TODO

---

# VII. ADMIN API

TODO

---

# VIII. AUTH API

Supabase

TODO

---

# IX. RESPONSE FORMAT

Thành công

```json
{
    "success":true,
    "data":{}
}
```

---

Lỗi

```json
{
    "success":false,
    "message":"",
    "error_code":""
}
```

---

# X. ERROR CODE

TODO

---

# XI. Authentication

Hiện tại

Public

Sau này

JWT

Supabase

---

# XII. API Naming

snake_case

Không dùng tiếng Việt.

---

# XIII. Nguyên tắc

Data API

↓

Business API

↓

AI

↓

Python

↓

Response

Không để Frontend đọc JSON trực tiếp.

Không để n8n xử lý dữ liệu gốc.

---

# TODO

Thiết kế Request/Response đầy đủ.

Thêm Authentication.

Thêm Rate Limit.

Thêm Pagination.

Thêm OpenAPI.