# NGÂN HÀNG ĐỀ AI

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# 1. Giới thiệu

Ngân Hàng Đề AI là nền tảng AI Tutor hỗ trợ giáo viên và học sinh
trong toàn bộ quá trình dạy và học môn Toán THPT.

Hệ thống có khả năng:

- Quản lý chương trình học.
- Sinh đề thi theo yêu cầu.
- Làm bài trực tuyến.
- Chấm bài (trắc nghiệm tự động, tự luận bằng AI).
- Phân tích kết quả, chỉ ra điểm yếu.
- Gợi ý lệnh luyện tập tiếp theo.
- Gia sư AI theo từng học sinh (giai đoạn sau).

---

# 2. Triết lý

Không dùng AI để thay thế giáo viên. AI đóng vai trò trợ lý.
Giáo viên vẫn là người quyết định.

Ưu tiên Code hơn AI. Chỉ dùng AI khi nhiệm vụ thực sự cần hiểu
ngôn ngữ tự nhiên hoặc cần văn phong tự nhiên. Mọi bước có quy tắc
rõ ràng (tra bảng, tính toán, chọn ID, so khớp đáp án) đều dùng Code.

---

# 3. Kiến trúc tổng quát

Dữ liệu
↓
FastAPI
↓
n8n Workflow
↓
Python Generator
↓
LaTeX Engine
↓
PDF / Web Test
↓
Chấm bài
↓
Phân tích kết quả
↓
Gợi ý luyện tập tiếp theo

---

# 4. Ba AI của toàn hệ thống

Toàn bộ vòng lặp "nhập lệnh → ra đề → làm bài → chấm → nhận xét →
gợi ý luyện tiếp" chỉ cần đúng 3 AI:

| AI | Vai trò |
|-----|--------|
| CHV_Fun | Hiểu yêu cầu tự nhiên của học sinh, phân loại nhiệm vụ, xác định cấu trúc đề |
| CHV_Grader | Chấm câu tự luận, dựa trên answer/solution có sẵn trong Question Object |
| CHV_Analyzer | Viết nhận xét kết quả học tập + gợi ý lệnh luyện tập tiếp theo |

Tất cả các bước còn lại (xác định phạm vi PPCT, xây Blueprint, chọn
Generator ID, chấm trắc nghiệm, tính điểm yếu...) đều là Code Node,
không dùng AI.

---

# 5. Thành phần chính

## FastAPI

Cung cấp API. Quản lý người dùng. Kết nối Supabase. Render giao diện.

## n8n

Điều phối toàn bộ workflow. Hầu hết logic là Code Node.
AI chỉ dùng ở 3 điểm nêu trên.

## Python Generator

Sinh câu hỏi, đáp án, lời giải chuẩn. Không dùng AI.
answer/solution sinh ra là căn cứ duy nhất để CHV_Grader chấm tự luận.

## Supabase

Quản lý người dùng, lịch sử, bài làm, thống kê.

---

# 6. Quy tắc phát triển

Ưu tiên Code hơn AI.
Ưu tiên dữ liệu JSON hơn Prompt.
Ưu tiên Python hơn LLM.
Ưu tiên API hơn xử lý trong n8n.
Ưu tiên tái sử dụng.
Không để logic nghiệp vụ nằm trong Prompt.
Không để AI tự suy luận hoặc tự tạo ID.

---

# 7. Tài liệu liên quan

00_PROJECT_OVERVIEW.md
01_ARCHITECTURE.md
02_FOLDER_STRUCTURE.md
03_DATA_STRUCTURE.md
04_ID_STANDARD.md
05_API_SPECIFICATION.md
06_N8N_WORKFLOW.md
07_AI_AGENTS.md
08_CODE_NODES.md
09_EXAM_GENERATION.md
10_PYTHON_GENERATOR.md
11_LATEX_ENGINE.md
12_DATABASE.md
13_FRONTEND.md
14_DEPLOYMENT.md
15_DEVELOPMENT_ROADMAP.md
16_CHANGELOG.md
17_NAMING_CONVENTIONS.md
18_PROMPT_LIBRARY.md
19_SYSTEM_MAP.md