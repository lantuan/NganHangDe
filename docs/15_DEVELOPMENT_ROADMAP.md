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
|3.2|Exam Scope API (CN_LoadExamScope)|✅|
|3.3|Blueprint API (CN_BuildBlueprint)|⬜|
|3.4|Question Selector API (CN_QuestionSelector)|⬜|
|3.5|Generator API|⬜|
|3.6|LaTeX API|⬜|
|3.7|Grade API (CN_GradeAnswer, CN_MergeGradeResult)|🟡|
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
|4.9|WF007_GradeExam|🟡|

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
|6.2|CHV_Grader|🟡|
|6.3|CHV_Analyzer|⬜|

---

# GIAI ĐOẠN 7 - HỌC SINH

|7.1|Làm bài Online|⬜|
|7.2|Upload ảnh (OCR cho bài tự luận)|🟡|
|7.3|CHV_Grader chấm tự luận|🟡|
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

Giai đoạn 6/7 — WF007_GradeExam, nhánh chấm bằng ẢNH (học sinh chụp ảnh
phiếu trả lời + bài tự luận viết tay). Đã xong: DocPhieuTraLoi (đọc
phiếu MC/TF/SA), CHV_Grader (chấm Tự luận từ ảnh), POST
/api/exam/grade-photo (gộp kết quả) — xem chi tiết Version 2.8 ở
docs/16_CHANGELOG.md. Đã kiểm chứng plumbing end-to-end trên production
bằng ảnh giả (không lỗi, đúng schema); CHƯA kiểm chứng độ chính xác đọc
bằng ảnh chụp phiếu/bài làm THẬT (chờ có bản in).

## Đã xong (không lặp lại ở đây, xem CHANGELOG để biết chi tiết)

- WF001_GenerateExam: scope, blueprint, mapping, question selector,
  python generator, latex, pdf — chạy full luồng qua
  /api/exam/generate-pdf-auto.
- CN_GradeAnswer cho MC/SA (POST /api/exam/grade) + lưu kết quả vào
  exam_history.
- CHV_Grader (chấm Tự luận từ ảnh, qua n8n webhook cham-tu-luan) +
  DocPhieuTraLoi (đọc phiếu MC/TF/SA từ ảnh, qua webhook
  doc-phieu-tra-loi) + POST /api/exam/grade-photo gộp cả 2 nhánh
  (xem Version 2.8).

## Bước tiếp theo

1. Test bằng ảnh chụp THẬT (phiếu đã tô + bài tự luận viết tay) để kiểm
   chứng độ chính xác đọc của DocPhieuTraLoi/CHV_Grader — cần bản in.
2. Sửa answer_parser_service để trích được đáp án đúng cho câu TF
   (\choiceTFn/\choiceTFt) — hiện TF luôn phải chấm tay dù đã đọc được
   ảnh (xem "HẠN CHẾ ĐÃ BIẾT" ở Version 2.8).
3. CN_MergeGradeResult — hiện đã gộp thủ công trong
   grade_photo_service.py; cân nhắc tách riêng nếu cần dùng lại ở nơi
   khác (vd chấm bài không qua ảnh).
4. CN_AnalyzeResults + CHV_Analyzer (WF003/WF007) — tính weak_points/
   strong_points và viết nhận xét.
5. Mở rộng Mapping + Python Generator cho các chương còn lại (hiện chỉ
   chương 1 có Mapping, và mới ~28% ID trong Mapping chương 1 có hàm
   Python thật).

## Ghi chú

Mọi Business Logic chuyển dần sang FastAPI/Code Node. n8n chỉ giữ
vai trò Orchestrator. Toàn hệ thống chỉ dùng 3 AI: CHV_Fun,
CHV_Grader, CHV_Analyzer.