# CẤU TRÚC DỮ LIỆU

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định cấu trúc dữ liệu chuẩn của toàn bộ hệ thống.

Mọi thành phần phải sử dụng chung một cấu trúc dữ liệu.

Bao gồm

- PPCT
- Curriculum
- Mapping
- Python Bank
- Blueprint
- API
- AI
- Database

---

# Nguyên tắc

## 1

Một loại dữ liệu

=

Một chuẩn JSON.

---

## 2

Không tạo nhiều chuẩn cho cùng một dữ liệu.

---

## 3

Mọi ID đều theo chuẩn

04_ID_STANDARD.md

---

# I. PPCT

## Vai trò

Xác định phạm vi kiến thức.

PPCT

không chứa

- năng lực

- dạng toán

- câu hỏi

---

## Một bản ghi

Ví dụ

```json
{
"id":"L10_C1_B1",
"lop":10,
"hoc_ky":1,
"chuong_so":1,
"chuong":"Mệnh đề và tập hợp",
"bai_so":1,
"bai":"Mệnh đề",
"lesson_type":"theory",
"keywords":[]
}
```

---

## Khóa chính

id

---

## Một file

=

Một khối.

Ví dụ

toan10.json

---

# II. Curriculum

## Vai trò

Mô tả năng lực cần đạt.

Không chứa

đề

đáp án

Python

---

## Một bản ghi

```json
{
"id":"L10_C1_B1_TH014",
"verb":"",
"content":"",
"MucDo":"TH",
"tags":[]
}
```

---

## Một file

=

Một chương.

Ví dụ

L10_C1.json

---

# III. Mapping

## Vai trò

Mô tả dạng câu hỏi.

---

Ví dụ

```json
{
"id":"L10_C1_B2_VD020_TL_A",
"Loai":"Tự luận",
"Dang":"..."
}
```

---

Một file

=

Một chương.

---

# IV. Python Bank

## Vai trò

Sinh câu hỏi.

---

Một file

=

Một chương.

Ví dụ

```
L10_C1.py
```

---

Một hàm

=

Một dạng.

Ví dụ

```
L10_C1_B2_NB017A_MC_A()
```

---

Không chia theo bài.

---

# V. Blueprint

## Vai trò

Kế hoạch sinh đề.

Không phải đề thi.

Không chứa LaTeX.

Không chứa đáp án.

---

Ví dụ

```json
[
 {
  "lesson_id":"L10_C1_B1",
  "level":"NB",
  "count":5
 }
]
```

---

TODO

Thiết kế đầy đủ.

---

# VI. Question Pool

## Vai trò

Danh sách ID sẽ gọi Python.

Ví dụ

```json
[
 "L10_C1_B1_NB001_MC_A",
 "L10_C1_B1_NB004_MC_A"
]
```

---

TODO

---

# VII. Exam

TODO

---

# VIII. Student Result

TODO

---

# IX. AI Analysis

TODO

---

# X. Dashboard

TODO

---

# XI. API Exchange

## Quy tắc

FastAPI

↓

JSON

↓

n8n

↓

JSON

↓

AI

↓

JSON

↓

Python

↓

JSON

↓

FastAPI

Không truyền Text tự do.

---

# XII. Database

TODO

---

# XIII. Version

Sau này mỗi JSON sẽ có version.

Ví dụ

```
schema_version
```

TODO.

---

# XIV. Quy tắc mở rộng

Không sửa schema cũ.

Nếu thay đổi lớn

↓

Tăng version.

---

# TODO

Hoàn thiện Blueprint.

Hoàn thiện Exam JSON.

Hoàn thiện Dashboard.

Hoàn thiện Student Result.

Hoàn thiện AI Analysis.

Hoàn thiện Database Schema.