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
| CN_LoadExamScope | Tra PPCT | ✅ |
| CN_LoadCurriculum | Đọc Curriculum | ✅ |
| CN_LoadMapping | Đọc Mapping | ✅ |
| CN_BuildCandidatePool | Ghép Blueprint + Curriculum + Mapping | ✅ |
| CN_QuestionSelector | Chọn ID Python theo quy tắc | ✅ |
| CN_CallPythonGenerator | Gọi Python | ✅ |
| CN_QuestionValidator | Kiểm tra câu hỏi sau khi sinh | ✅ |
| CN_ExamAssembler | Ghép đề hoàn chỉnh | ✅ |
| CN_GenerateLatex | Sinh LaTeX | TODO |
| CN_GeneratePDF | Sinh PDF | TODO |
| CN_SaveExam | Lưu đề | TODO |
| CN_SaveHistory | Lưu lịch sử | TODO |
| CN_LoadStudent | Đọc học sinh | TODO |
| CN_LoadTeacher | Đọc giáo viên | TODO |
| CN_ResponseFormatter | Chuẩn hóa Response | ✅ |

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

# CN_BuildCandidatePool

## Mục tiêu

- Ghép Blueprint.
- Ghép Curriculum.
- Ghép Mapping.
- Sinh Candidate Pool.

## Input

- Blueprint
- Curriculum
- Mapping

## Output

```json
[
    "L10_C1_B1_NB001_MC_A",
    "L10_C1_B1_NB002_MC_A",
    "L10_C1_B2_TH013_TF_A"
]
```

Không chọn câu.

Chỉ tạo danh sách các ID có thể sử dụng.

---

# CN_QuestionSelector

## Mục tiêu

Chọn các ID Python sẽ được sinh đề.

## Input

Candidate Pool

## Output

Selected Question IDs

## Quy tắc

- Không trùng câu.
- Không trùng dạng.
- Không trùng template.
- Random phiên bản A/B/C/D.
- Đúng Blueprint.
- Đúng số lượng câu.
- Đúng mức độ.
- Đúng chương.
- Đúng bài.
- Sau này: không trùng đề đã làm.

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

## Input

Selected Question IDs

## Công việc

- Import file Python theo chương.
- Gọi đúng hàm theo ID.
- Nhận Question Object.

---

Output

LaTeX.

JSON.

---

Không xử lý Prompt.

---

# CN_QuestionValidator

## Mục tiêu

Kiểm tra kết quả Python sinh.

## Kiểm tra

- Có câu hỏi.
- Có đáp án.
- Có lời giải.
- Có LaTeX.
- Không lỗi.

Nếu lỗi

↓

Loại câu

↓

Quay lại CN_QuestionSelector

↓

Lấy ID khác.

---

# CN_ExamAssembler

## Mục tiêu

Ghép toàn bộ Question Object thành một đề hoàn chỉnh.

## Output

```json
{
    "exam": [],
    "answer": [],
    "metadata": {}
}
```

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
