# NGÂN HÀNG ĐỀ AI

Phiên bản: 1.0

---

# 1. Giới thiệu

Ngân Hàng Đề AI không chỉ là một hệ thống tạo đề thi.

Đây là một nền tảng AI Tutor hỗ trợ giáo viên và học sinh trong toàn bộ quá trình dạy và học môn Toán.

Hệ thống có khả năng:

- Quản lý chương trình học.
- Sinh đề thi theo yêu cầu.
- Làm bài trực tuyến.
- Chấm bài.
- Phân tích kết quả.
- Đề xuất lộ trình học.
- Gia sư AI theo từng học sinh.

---

# 2. Triết lý

Không dùng AI để thay thế giáo viên.

AI đóng vai trò trợ lý.

Giáo viên vẫn là người quyết định.

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

AI Analysis

↓

AI Tutor

---

# 4. Thành phần chính

## FastAPI

Cung cấp API.

Quản lý người dùng.

Kết nối Supabase.

Render giao diện.

---

## n8n

Điều phối toàn bộ workflow.

Hầu hết logic sẽ được viết bằng Code Node.

AI chỉ dùng ở những bước cần suy luận.

---

## Python Generator

Sinh câu hỏi.

Đảm bảo tính chính xác.

Không để AI tự nghĩ toán.

---

## AI Agent

Chỉ thực hiện:

- phân tích yêu cầu
- lập kế hoạch sinh đề
- sinh lời giải
- phân tích học sinh
- gia sư AI

---

## Supabase

Quản lý:

- người dùng
- lịch sử
- bài làm
- thống kê

---

# 5. Quy tắc phát triển

Ưu tiên Code hơn AI.

Ưu tiên dữ liệu JSON hơn Prompt.

Ưu tiên Python hơn LLM.

Ưu tiên API hơn xử lý trong n8n.

Ưu tiên tái sử dụng.

Không để logic nghiệp vụ nằm trong Prompt.

---

# 6. Quy ước

Toàn bộ dự án được mô tả trong thư mục docs.

Mọi thay đổi đều phải cập nhật tài liệu.

Không phát triển chức năng khi chưa xác định vị trí trong kiến trúc.

---

# 7. Tài liệu liên quan

01_ARCHITECTURE.md

02_FOLDER_STRUCTURE.md

03_DATA_STRUCTURE.md

...

18_PROMPT_LIBRARY.md