# SYSTEM MAP

Version: 2.0

Trạng thái

🟢 Kiến trúc tổng thể

---

# Mục tiêu

Bản đồ tổng thể hệ thống. Mỗi thành phần mô tả ngắn gọn: là gì,
làm gì, nằm ở đâu. Chi tiết xem từng file tương ứng.

---

# Kiến trúc tổng thể

User → Frontend → FastAPI → n8n → Python → LaTeX → PDF/Web Test
→ Supabase

---

# AI Agents (chỉ 3 AI)

| AI | Nhiệm vụ | Tài liệu |
|-----|----------|----------|
| CHV_Fun | Điều phối + phân tích yêu cầu sinh đề | 07_AI_AGENTS |
| CHV_Grader | Chấm tự luận | 07_AI_AGENTS |
| CHV_Analyzer | Phân tích kết quả + gợi ý luyện tập | 07_AI_AGENTS |

---

# Code Nodes

| Node | Nhiệm vụ | Tài liệu |
|------|----------|----------|
| CN_LoadExamScope | Đọc PPCT, xác định phạm vi | 08 |
| CN_LoadCurriculum | Đọc Curriculum | 08 |
| CN_BuildBlueprint | Phân bổ competency, sinh Blueprint | 08 |
| CN_LoadMapping | Đọc Mapping | 08 |
| CN_QuestionSelector | Chọn Generator ID | 08 |
| CN_CallPythonGenerator | Gọi Python | 08 |
| CN_QuestionValidator | Kiểm tra câu hỏi | 08 |
| CN_ExamAssembler | Ghép đề | 08 |
| CN_ResponseFormatter | Trả JSON | 08 |
| CN_GradeAnswer | Chấm MC/TF/SA | 08 |
| CN_MergeGradeResult | Gộp kết quả chấm | 08 |
| CN_AnalyzeResults | Tính điểm yếu/mạnh | 08 |

---

# Workflow

| Workflow | Chức năng |
|----------|-----------|
| WF000 | Điều phối |
| WF001 | Sinh đề |
| WF002 | Sinh đề theo năng lực |
| WF003 | Phân tích học tập |
| WF004 | Tải file |
| WF005 | Hướng dẫn |
| WF006 | Từ chối |
| WF007 | Chấm bài |

---

# APIs

| API | Chức năng |
|------|-----------|
| /api/data/ppct | PPCT |
| /api/data/curriculum | Curriculum |
| /api/data/mapping | Mapping |
| /api/exam/generate | Sinh đề |
| /api/exam/grade | Chấm bài |
| /api/student/analysis | Phân tích học tập |

---

# Python

data/python_bank/ — mỗi chương một file, nhiều hàm mỗi file.

---

# JSON

PPCT → Curriculum → Mapping

---

# Database

Supabase → Profiles → Classes → Exam History → Learning History
(gồm ket_qua_theo_cau, weak_points, strong_points) → AI Logs

---

# Frontend

Trang chủ → Chat → Dashboard → Sinh đề → Thi Online → Chấm bài
→ Kết quả + Gợi ý → Lịch sử → Quản trị

---

# Documents

| File | Nội dung |
|------|----------|
| 00 | Tổng quan |
| 01 | Kiến trúc |
| 02 | Folder |
| 03 | Data |
| 04 | ID |
| 05 | API |
| 06 | Workflow |
| 07 | AI Agents (3 AI) |
| 08 | Code Nodes |
| 09 | Exam Generation |
| 10 | Python Generator |
| 11 | LaTeX |
| 12 | Database |
| 13 | Frontend |
| 14 | Deployment |
| 15 | Roadmap |
| 16 | Changelog |
| 17 | Naming |
| 18 | Prompt Library |
| 19 | System Map |

---

# Quy tắc đọc tài liệu

Kiến trúc → 01
ID → 04
Workflow → 06
AI → 07
Code Node → 08
Sinh đề → 09
Python → 10
Database → 12
Frontend → 13
Deployment → 14
Prompt → 18

---

# TODO

Cập nhật khi có AI mới, Workflow mới, API mới, Database mới.