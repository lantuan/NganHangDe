# AI AGENTS

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định toàn bộ AI Agent của hệ thống.

Mỗi AI Agent chỉ có đúng một nhiệm vụ.

Không để một Agent làm nhiều chức năng.

---

# Nguyên tắc

## 1

Một Agent

=

Một nhiệm vụ.

---

## 2

Agent không gọi Database.

Agent không đọc JSON.

Agent chỉ nhận JSON đã được Code Node xử lý.

---

## 3

Agent không gọi Python.

Code Node sẽ gọi Python.

---

## 4

Agent không sinh LaTeX.

Python Generator sinh LaTeX.

---

## 5

Agent không tự suy luận ngoài dữ liệu được cung cấp.

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

Webhook Response

---

# Danh sách AI Agent

| ID | Agent | Chức năng | Trạng thái |
|----|--------|-----------|------------|
| CHV_RequestParser | Phân tích yêu cầu | Đang triển khai |
| CHV_ExamPlanner | Lập Blueprint đề | Đang triển khai |
| CHV_BlueprintReviewer | Kiểm tra Blueprint | TODO |
| CHV_SolutionWriter | Viết lời giải | TODO |
| CHV_AnswerReviewer | Kiểm tra đáp án | TODO |
| CHV_Analyzer | Phân tích kết quả | TODO |
| CHV_Tutor | Gia sư AI | TODO |
| CHV_ReportWriter | Viết báo cáo | TODO |
| CHV_DashboardAdvisor | Gợi ý Dashboard | TODO |
| CHV_AdminAssistant | Hỗ trợ quản trị | TODO |

---

# CHV_RequestParser

## Vai trò

Phân tích yêu cầu tiếng Việt.

Đổi thành JSON chuẩn.

---

## Input

Ngôn ngữ tự nhiên.

---

## Output

JSON.

---

## Không được làm

Không đọc PPCT.

Không đọc Curriculum.

Không đọc Mapping.

Không sinh câu hỏi.

Không sinh Blueprint.

Không suy luận ID.

---

## Ví dụ

Input

```
Sinh đề giữa kỳ chương Mệnh đề.
```

Output

```json
{
  "grade":10,
  "chapter":"Mệnh đề",
  "exam_type":"Giữa kỳ"
}
```

---

# CHV_ExamPlanner

## Vai trò

Sinh Blueprint.

---

## Input

JSON.

---

## Output

Blueprint.

---

## Không được làm

Không sinh câu hỏi.

Không gọi Python.

Không viết LaTeX.

Không chọn ID Python.

---

# CHV_BlueprintReviewer

## Vai trò

Kiểm tra Blueprint.

---

TODO.

---

# CHV_SolutionWriter

## Vai trò

Viết lời giải.

---

TODO.

---

# CHV_AnswerReviewer

## Vai trò

Kiểm tra đáp án.

---

TODO.

---

# CHV_Analyzer

## Vai trò

Phân tích bài làm.

---

TODO.

---

# CHV_Tutor

## Vai trò

Gia sư AI.

---

TODO.

---

# CHV_ReportWriter

## Vai trò

Sinh báo cáo.

---

TODO.

---

# CHV_DashboardAdvisor

## Vai trò

Đưa ra gợi ý Dashboard.

---

TODO.

---

# CHV_AdminAssistant

## Vai trò

Hỗ trợ quản trị.

---

TODO.

---

# Quy tắc đặt tên

CHV_

+

Tên chức năng.

Ví dụ

CHV_RequestParser

CHV_ExamPlanner

CHV_Tutor

---

# Vòng đời của Agent

Input

↓

Prompt

↓

LLM

↓

JSON

↓

Code Node

---

# Quan hệ với Workflow

Workflow

↓

Code Node

↓

AI Agent

↓

Code Node

Không có Agent gọi Agent.

Không có Agent gọi API.

Không có Agent gọi Database.

---

# Quan hệ với Prompt

Mỗi Agent

=

Một Prompt.

Prompt được quản lý tại

18_PROMPT_LIBRARY.md

---

# TODO

Hoàn thiện toàn bộ Input.

Hoàn thiện Output.

Viết Prompt.

Đánh Version.

Thêm Agent mới khi cần.
