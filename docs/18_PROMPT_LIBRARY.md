# PROMPT LIBRARY

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Lưu trữ Prompt chính thức của toàn bộ AI trong hệ thống.

Mỗi AI chỉ có một Prompt chính thức.

Prompt được quản lý theo phiên bản.

---

# Danh sách Prompt

| AI | Prompt |
|-----|--------|
| CHV_Fun | Điều phối hệ thống |
| CHV_RequestParser | Phân tích yêu cầu sinh đề |
| CHV_ExamPlanner | Lập Blueprint |
| CHV_AbilityPlanner | Sinh đề theo năng lực |
| CHV_Analyzer | Phân tích học tập |
| CHV_Help | Hướng dẫn sử dụng |
| CHV_Reject | Từ chối yêu cầu |

---

===============================================================================

CHV_Fun

-------------------------------------------------------------------------------

Workflow

WF000_Gateway

-------------------------------------------------------------------------------

Prompt

Điều phối toàn bộ hệ thống.

Phân loại yêu cầu.

Trả về

{
    "task":"",
    "message":""
}

Không sinh đề.

Không giải toán.

Không trả lời kiến thức.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Fun.md

---

===============================================================================

CHV_RequestParser

-------------------------------------------------------------------------------

Workflow

WF001_GenerateExam

-------------------------------------------------------------------------------

Prompt

Đọc yêu cầu sinh đề.

Chuẩn hóa Request JSON.

-------------------------------------------------------------------------------

File

data/prompts/CHV_RequestParser.md

---

===============================================================================

CHV_ExamPlanner

-------------------------------------------------------------------------------

Workflow

WF001_GenerateExam

-------------------------------------------------------------------------------

Prompt

Sinh Blueprint từ Request và PPCT.

-------------------------------------------------------------------------------

File

data/prompts/CHV_ExamPlanner.md

---

===============================================================================

CHV_AbilityPlanner

-------------------------------------------------------------------------------

Workflow

WF002_GenerateExamByAbility

-------------------------------------------------------------------------------

Prompt

Sinh Blueprint theo năng lực học sinh.

-------------------------------------------------------------------------------

File

data/prompts/CHV_AbilityPlanner.md

---

===============================================================================

CHV_Analyzer

-------------------------------------------------------------------------------

Workflow

WF003_StudentAnalysis

-------------------------------------------------------------------------------

Prompt

Phân tích lịch sử học tập.

Sinh Learning Report.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Analyzer.md

---

===============================================================================

CHV_Help

-------------------------------------------------------------------------------

Workflow

WF005_Help

-------------------------------------------------------------------------------

Prompt

Hướng dẫn sử dụng hệ thống.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Help.md

---

===============================================================================

CHV_Reject

-------------------------------------------------------------------------------

Workflow

WF006_Reject

-------------------------------------------------------------------------------

Prompt

Từ chối các yêu cầu ngoài phạm vi.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Reject.md

---

# Quy tắc

- Một AI chỉ có một Prompt chính thức.
- Prompt được lưu dưới dạng Markdown.
- Không sửa Prompt trực tiếp trong n8n.
- Prompt được quản lý trong thư mục data/prompts.
- Khi thay đổi Prompt phải cập nhật CHANGELOG.