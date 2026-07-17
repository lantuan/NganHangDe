# THƯ VIỆN PROMPT

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Lưu toàn bộ Prompt của hệ thống.

Mỗi AI Agent có đúng một Prompt chính thức.

Mọi chỉnh sửa Prompt đều phải cập nhật tại đây trước khi đưa vào n8n.

---

# Quy tắc

- Một Agent = Một Prompt.
- Không tạo nhiều Prompt cùng chức năng.
- Prompt phải đánh version.
- Prompt phải có Input/Output rõ ràng.
- Prompt chỉ xử lý đúng nhiệm vụ được giao.
- Không để Prompt tự suy luận ngoài phạm vi.

---

# Danh sách Prompt

| ID | Agent | Chức năng | Trạng thái |
|----|--------|-----------|-----------|
| P001 | CHV_RequestParser | Phân tích yêu cầu người dùng | TODO |
| P002 | CHV_ExamPlanner | Lập Blueprint đề | TODO |
| P003 | CHV_BlueprintBuilder | Hoàn thiện Blueprint | TODO |
| P004 | CHV_SolutionWriter | Viết lời giải | TODO |
| P005 | CHV_Analyzer | Phân tích kết quả | TODO |
| P006 | CHV_Tutor | Gia sư AI | TODO |
| P007 | CHV_ReportWriter | Báo cáo | TODO |

---

# P001

## Agent

CHV_RequestParser

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# P002

## Agent

CHV_ExamPlanner

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# P003

## Agent

CHV_BlueprintBuilder

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# P004

## Agent

CHV_SolutionWriter

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# P005

## Agent

CHV_Analyzer

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# P006

## Agent

CHV_Tutor

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# P007

## Agent

CHV_ReportWriter

## Mục tiêu

TODO

## Input

TODO

## Output

TODO

## Prompt

TODO

---

# Quy trình cập nhật Prompt

Prompt

↓

Kiểm thử trên ChatGPT

↓

Chỉnh sửa

↓

Lưu vào Prompt Library

↓

Đưa vào n8n

↓

Đánh Version

↓

Triển khai

---

# TODO

- Viết Prompt hoàn chỉnh cho từng Agent.
- Thêm Prompt cho các Agent mới.
- Quản lý Version Prompt.