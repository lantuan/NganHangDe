# N8N WORKFLOW

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định toàn bộ Workflow của hệ thống.

Mọi Workflow đều phải được thiết kế tại đây trước khi xây dựng trên n8n.

Không tạo Workflow tùy ý.

---

# Nguyên tắc

## 1

Một Workflow

=

Một chức năng.

---

## 2

Một AI Agent

=

Một nhiệm vụ.

---

## 3

Một Code Node

=

Một nhiệm vụ.

---

## 4

Không để AI đọc JSON lớn.

AI chỉ nhận dữ liệu đã được Code Node xử lý.

---

## 5

Mọi dữ liệu đều đi qua API.

Không đọc file JSON trực tiếp trong AI Agent.

---

# Kiến trúc tổng thể

User

↓

FastAPI

↓

Webhook

↓

Workflow n8n

↓

FastAPI

↓

Frontend

---

# Danh sách Workflow

| ID | Workflow | Trạng thái |
|----|----------|------------|
| WF001 | Sinh đề | Đang triển khai |
| WF002 | Làm bài trực tuyến | TODO |
| WF003 | Chấm bài AI | TODO |
| WF004 | Phân tích kết quả | TODO |
| WF005 | Gia sư AI | TODO |
| WF006 | Dashboard học sinh | TODO |
| WF007 | Dashboard giáo viên | TODO |
| WF008 | Báo cáo học tập | TODO |
| WF009 | Import dữ liệu | TODO |
| WF010 | Quản trị hệ thống | TODO |

---

# WF001

## Sinh đề

### Mục tiêu

Sinh đề theo yêu cầu người dùng.

---

## Luồng

User

↓

Webhook

↓

CHV_RequestParser

↓

CN_LoadExamScope

↓

CHV_ExamPlanner

↓

CN_LoadQuestionPool

↓

CN_CallPythonGenerator

↓

CN_ResponseFormatter

↓

Respond To Webhook

---

## Webhook

Input

TODO

Output

TODO

---

## CHV_RequestParser

Mục tiêu

Chuyển yêu cầu tiếng Việt

↓

JSON chuẩn.

Không đọc PPCT.

Không đọc Curriculum.

Không đọc Mapping.

---

Output

TODO

---

## CN_LoadExamScope

Mục tiêu

Tra PPCT.

Đổi

Tên bài

↓

lesson_id

---

Input

TODO

Output

TODO

---

## CHV_ExamPlanner

Mục tiêu

Sinh Blueprint.

Không sinh câu hỏi.

---

Input

TODO

Output

TODO

---

## CN_LoadQuestionPool

Mục tiêu

Tra Curriculum.

Tra Mapping.

Sinh danh sách ID Python.

---

Input

TODO

Output

TODO

---

## CN_CallPythonGenerator

Mục tiêu

Import Python.

Sinh câu hỏi.

---

Input

TODO

Output

TODO

---

## CN_ResponseFormatter

Mục tiêu

Định dạng Response.

JSON.

LaTeX.

HTML.

---

Input

TODO

Output

TODO

---

## Respond To Webhook

Trả kết quả.

---

# WF002

Làm bài trực tuyến

TODO

---

# WF003

Chấm bài AI

TODO

---

# WF004

Phân tích kết quả

TODO

---

# WF005

Gia sư AI

TODO

---

# WF006

Dashboard học sinh

TODO

---

# WF007

Dashboard giáo viên

TODO

---

# WF008

Báo cáo học tập

TODO

---

# WF009

Import dữ liệu

TODO

---

# WF010

Quản trị hệ thống

TODO

---

# Quy tắc Workflow

Workflow không chứa Business Logic.

Business Logic thuộc FastAPI.

---

Workflow không chứa dữ liệu.

Dữ liệu lấy từ API.

---

Workflow không sinh câu hỏi.

Python Generator sinh câu hỏi.

---

Workflow không đọc JSON.

Code Node đọc JSON.

---

Workflow không xử lý LaTeX.

Python Generator xử lý LaTeX.

---

# Danh sách AI Agent

CHV_RequestParser

CHV_ExamPlanner

CHV_SolutionWriter

CHV_Analyzer

CHV_Tutor

CHV_ReportWriter

TODO

---

# Danh sách Code Node

CN_LoadExamScope

CN_LoadQuestionPool

CN_CallPythonGenerator

CN_ResponseFormatter

TODO

---

# TODO

Thiết kế chi tiết WF002.

Thiết kế chi tiết WF003.

Thiết kế chi tiết WF004.

Thiết kế chi tiết WF005.

Thiết kế chi tiết Dashboard.

Thiết kế Workflow Import.

Thiết kế Workflow Admin.

Hoàn thiện Input/Output của từng Node.

Hoàn thiện Error Handling.

Hoàn thiện Retry Strategy.