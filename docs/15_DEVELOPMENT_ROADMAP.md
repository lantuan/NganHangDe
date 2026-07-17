# DEVELOPMENT ROADMAP

Version: 1.0

---

# Mục tiêu

Roadmap là tài liệu theo dõi toàn bộ quá trình phát triển dự án.

Mỗi hạng mục đều có:

- Trạng thái
- Mục tiêu
- Đã hoàn thành
- Công việc tiếp theo

Quy ước:

- ⬜ Chưa bắt đầu
- 🟡 Đang thực hiện
- ✅ Hoàn thành
- 🔴 Tạm dừng

---

# GIAI ĐOẠN 1 - HẠ TẦNG

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|1.1|GitHub Repository|✅|
|1.2|VPS Ubuntu|✅|
|1.3|SSH GitHub ↔ VPS|✅|
|1.4|Python Virtual Environment|✅|
|1.5|FastAPI|✅|
|1.6|Systemd Service|✅|
|1.7|Supabase|✅|
|1.8|Đăng nhập|✅|
|1.9|Đăng ký|✅|
|1.10|Chat Web|✅|

---

# GIAI ĐOẠN 2 - DỮ LIỆU

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|2.1|PPCT JSON|✅|
|2.2|Curriculum JSON|🟡|
|2.3|Mapping JSON|🟡|
|2.4|Python Bank|⬜|
|2.5|Prompt Library|⬜|

---

# GIAI ĐOẠN 3 - BACKEND API

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|3.1|API đọc dữ liệu|🟡|
|3.2|Exam Scope API|⬜|
|3.3|Question Pool API|⬜|
|3.4|Blueprint API|⬜|
|3.5|Generator API|⬜|
|3.6|LaTeX API|⬜|

---

# GIAI ĐOẠN 4 - N8N

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|4.1|Webhook|✅|
|4.2|Request Parser AI|🟡|
|4.3|Exam Scope|⬜|
|4.4|Blueprint|⬜|
|4.5|Question Pool|⬜|
|4.6|Python Generator|⬜|
|4.7|LaTeX|⬜|
|4.8|PDF|⬜|

---

# GIAI ĐOẠN 5 - PYTHON GENERATOR

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|5.1|Generator chuẩn|⬜|
|5.2|MC|⬜|
|5.3|Đúng Sai|⬜|
|5.4|Tự luận|⬜|
|5.5|Đáp án|⬜|
|5.6|Lời giải|⬜|

---

# GIAI ĐOẠN 6 - AI

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|6.1|CHV_RequestParser|🟡|
|6.2|CHV_ExamPlanner|⬜|
|6.3|CHV_SolutionWriter|⬜|
|6.4|CHV_Analysis|⬜|
|6.5|CHV_Tutor|⬜|

---

# GIAI ĐOẠN 7 - HỌC SINH

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|7.1|Làm bài Online|⬜|
|7.2|Upload ảnh|⬜|
|7.3|AI Chấm|⬜|
|7.4|Dashboard|⬜|
|7.5|AI Gia sư|⬜|

---

# GIAI ĐOẠN 8 - TRIỂN KHAI

| STT | Hạng mục | Trạng thái |
|------|-----------|------------|
|8.1|Domain|⬜|
|8.2|HTTPS|⬜|
|8.3|Backup|⬜|
|8.4|Monitoring|⬜|

---

# ĐIỂM DỪNG HIỆN TẠI

## Đang thực hiện

Giai đoạn 3

### 3.1 API đọc dữ liệu

---

## Bước tiếp theo

3.2 Exam Scope API

---

## Ghi chú

Mọi Business Logic sẽ được chuyển dần sang FastAPI.

n8n chỉ giữ vai trò Orchestrator.

AI chỉ thực hiện suy luận.

Python chịu trách nhiệm sinh câu hỏi.