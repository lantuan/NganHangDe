# CODE NODES

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định toàn bộ Code Node của hệ thống n8n.

Code Node là nơi xử lý nghiệp vụ.

AI Agent không xử lý nghiệp vụ.

---

# Nguyên tắc

## 1

Một Code Node

=

Một nhiệm vụ.

---

## 2

Không viết nhiều nghiệp vụ trong cùng một Node.

---

## 3

Code Node không được gọi LLM.

Chỉ AI Agent mới gọi LLM.

---

## 4

Code Node được phép

- Gọi API
- Đọc JSON
- Ghép dữ liệu
- Lọc dữ liệu
- Kiểm tra dữ liệu
- Chuẩn hóa dữ liệu
- Gọi Python
- Gọi Database

---

## 5

Không để Code Node chứa Prompt.

Prompt thuộc

18_PROMPT_LIBRARY.md

---

# Kiến trúc

Webhook

↓

Code Node

↓

AI Agent

↓

Code Node

↓

Webhook

---

# Danh sách Code Node

| ID | Code Node | Chức năng | Trạng thái |
|----|-----------|-----------|------------|
| CN_LoadExamScope | Tra PPCT | Đang triển khai |
| CN_LoadCurriculum | Đọc Curriculum | TODO |
| CN_LoadMapping | Đọc Mapping | TODO |
| CN_LoadQuestionPool | Sinh Question Pool | Đang triển khai |
| CN_CallPythonGenerator | Gọi Python | Đang triển khai |
| CN_GenerateLatex | Sinh LaTeX | TODO |
| CN_GeneratePDF | Sinh PDF | TODO |
| CN_SaveExam | Lưu đề | TODO |
| CN_SaveHistory | Lưu lịch sử | TODO |
| CN_LoadStudent | Đọc học sinh | TODO |
| CN_LoadTeacher | Đọc giáo viên | TODO |
| CN_ResponseFormatter | Chuẩn hóa Response | Đang triển khai |

---

# CN_LoadExamScope

## Vai trò

Tra cứu PPCT.

Đổi tên chương

↓

lesson_id

---

## Input

JSON từ RequestParser.

---

## Output

lesson_id

---

## Gọi API

```
GET

/api/data/ppct/{grade}
```

---

## Không được làm

Không sinh câu hỏi.

Không gọi Python.

Không đọc Curriculum.

---

# CN_LoadCurriculum

## Vai trò

Đọc Curriculum.

---

## Input

lesson_id

---

## Output

Danh sách năng lực.

---

## API

```
GET

/api/data/curriculum/{chapter}
```

---

TODO.

---

# CN_LoadMapping

## Vai trò

Đọc Mapping.

---

Input

TODO

Output

TODO

---

# CN_LoadQuestionPool

## Vai trò

Ghép

Curriculum

+

Mapping

↓

Question Pool.

---

Input

lesson_id

Blueprint

---

Output

Danh sách ID Python.

---

Không sinh câu hỏi.

---

# CN_CallPythonGenerator

## Vai trò

Import Python.

↓

Gọi Generator.

---

Ví dụ

```
L10_C1.py
```

↓

```
L10_C1_B2_VD020_TL_A()
```

---

Output

LaTeX.

JSON.

---

Không xử lý Prompt.

---

# CN_GenerateLatex

TODO.

---

# CN_GeneratePDF

TODO.

---

# CN_SaveExam

TODO.

---

# CN_SaveHistory

TODO.

---

# CN_LoadStudent

TODO.

---

# CN_LoadTeacher

TODO.

---

# CN_ResponseFormatter

## Vai trò

Chuẩn hóa Response.

---

Ví dụ

```
success

message

data

metadata
```

---

Không xử lý nghiệp vụ.

---

# Quan hệ với AI

Code Node

↓

AI

↓

Code Node

Không có

AI

↓

AI

---

# Quan hệ với API

Code Node

↓

FastAPI

↓

JSON

---

# Quan hệ với Python

Code Node

↓

Import

↓

Python Generator

↓

LaTeX

---

# Quy tắc đặt tên

CN_

+

Tên chức năng.

Ví dụ

CN_LoadExamScope

CN_LoadCurriculum

CN_LoadMapping

CN_LoadQuestionPool

CN_CallPythonGenerator

CN_ResponseFormatter

---

# Quy tắc Input

Input luôn là JSON.

Không dùng Text.

---

# Quy tắc Output

Output luôn là JSON.

Không trả String tự do.

---

# Error Handling

TODO.

---

# Retry Strategy

TODO.

---

# Logging

TODO.

---

# Performance

TODO.

---

# TODO

Thiết kế toàn bộ Input.

Thiết kế Output.

Thiết kế Error Code.

Thiết kế Logging.

Thiết kế Retry.

Thiết kế Cache.
