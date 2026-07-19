# DEVELOPMENT ROADMAP

Version: 2.0

---

# Mục tiêu

Theo dõi toàn bộ quá trình phát triển dự án.

Quy ước: ⬜ Chưa bắt đầu | 🟡 Đang thực hiện | ✅ Hoàn thành | 🔴 Tạm dừng

---

# GIAI ĐOẠN 1 - HẠ TẦNG

|1.1|GitHub Repository|✅|
|1.2|VPS Ubuntu|✅|
|1.3|SSH GitHub ↔ VPS|✅|
|1.4|Python Virtual Environment|✅|
|1.5|FastAPI|✅|
|1.6|Systemd Service|✅|
|1.7|Supabase|✅|
|1.8|Đăng nhập (session/cookie thực)|🟡|
|1.9|Đăng ký|✅|
|1.10|Chat Web|✅|

---

# GIAI ĐOẠN 2 - DỮ LIỆU

|2.1|PPCT JSON|✅|
|2.2|Curriculum JSON|🟡|
|2.3|Mapping JSON|🟡|
|2.4|Python Bank|⬜|
|2.5|Prompt Library (rút gọn token)|⬜|

---

# GIAI ĐOẠN 3 - BACKEND API

|3.1|API đọc dữ liệu (bọc Response chuẩn)|🟡|
|3.2|Exam Scope API (CN_LoadExamScope)|⬜|
|3.3|Blueprint API (CN_BuildBlueprint)|⬜|
|3.4|Question Selector API (CN_QuestionSelector)|⬜|
|3.5|Generator API|⬜|
|3.6|LaTeX API|⬜|
|3.7|Grade API (CN_GradeAnswer, CN_MergeGradeResult)|⬜|
|3.8|Analysis API (CN_AnalyzeResults)|⬜|

---

# GIAI ĐOẠN 4 - N8N

|4.1|Webhook|✅|
|4.2|CHV_Fun (gộp phân tích cấu trúc đề)|🟡|
|4.3|CN_LoadExamScope|⬜|
|4.4|CN_BuildBlueprint|⬜|
|4.5|CN_QuestionSelector|⬜|
|4.6|Python Generator|⬜|
|4.7|LaTeX|⬜|
|4.8|PDF|⬜|
|4.9|WF007_GradeExam|⬜|

---

# GIAI ĐOẠN 5 - PYTHON GENERATOR

|5.1|Generator chuẩn|⬜|
|5.2|MC|⬜|
|5.3|TF (Đúng/Sai)|⬜|
|5.4|SA (Trả lời ngắn)|⬜|
|5.5|TL (Tự luận)|⬜|
|5.6|Đáp án (answer)|⬜|
|5.7|Lời giải (solution) — dùng cho CHV_Grader|⬜|

---

# GIAI ĐOẠN 6 - AI (chỉ 3 AI)

|6.1|CHV_Fun|🟡|
|6.2|CHV_Grader|⬜|
|6.3|CHV_Analyzer|⬜|

---

# GIAI ĐOẠN 7 - HỌC SINH

|7.1|Làm bài Online|⬜|
|7.2|Upload ảnh (OCR cho bài tự luận)|⬜|
|7.3|CHV_Grader chấm tự luận|⬜|
|7.4|Dashboard + nút gợi ý luyện tập|⬜|
|7.5|AI Gia sư (giai đoạn sau)|⬜|

---

# GIAI ĐOẠN 8 - TRIỂN KHAI

|8.1|Domain|⬜|
|8.2|HTTPS|⬜|
|8.3|Backup|⬜|
|8.4|Monitoring|⬜|

---

# ĐIỂM DỪNG HIỆN TẠI

## Đang thực hiện

Giai đoạn 3 và 4 — hiện thực hoá CN_LoadExamScope, CN_BuildBlueprint,
CN_QuestionSelector bằng Code (thay vì AI như bản nháp cũ).

## Bước tiếp theo

1. Code CN_LoadExamScope (tra PPCT theo boundary_after).
2. Code CN_BuildBlueprint (thuật toán phân bổ competency).
3. Code CN_QuestionSelector (chọn Generator ID từ Mapping).
4. Hoàn thiện Python Generator cho ít nhất 1 chương để test full
   luồng WF001 đầu đến cuối.
5. Sau khi WF001 chạy được, làm WF007_GradeExam (MC/TF/SA trước,
   CHV_Grader cho TL sau).

## Ghi chú

Mọi Business Logic chuyển dần sang FastAPI/Code Node. n8n chỉ giữ
vai trò Orchestrator. Toàn hệ thống chỉ dùng 3 AI: CHV_Fun,
CHV_Grader, CHV_Analyzer.