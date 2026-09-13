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
|3.9|Thang điểm 10 theo phần (CN_TinhThangDiem)|✅|
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

TẠM DỪNG nhánh chấm bằng ẢNH (2026-09-04): trang làm bài đã ẩn ô tải ảnh
và hiện thông báo "Chức năng chấm tự luận đang được xây dựng"; học sinh
làm bài trên web được chấm ngay 7 điểm trắc nghiệm, phần tự luận 3 điểm
nộp giấy cho giáo viên. Việc tiếp theo ưu tiên: đề + đáp án đăng lên
Classroom của học sinh (hiện chưa hiện được trong tài khoản người học).

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
- Thang điểm 10 theo phần: MC 3đ, TF 2đ, SA 2đ, TL 3đ, chia đều
  trong từng phần (cấu hình ở data/config/diem_rules.json, tính ở
  app/services/diem_service.py) — xem Version 2.35 ở CHANGELOG.
- CHV_Grader (chấm Tự luận từ ảnh, qua n8n webhook cham-tu-luan) +
  DocPhieuTraLoi (đọc phiếu MC/TF/SA từ ảnh, qua webhook
  doc-phieu-tra-loi) + POST /api/exam/grade-photo gộp cả 2 nhánh
  (xem Version 2.8).

## Bước tiếp theo

1. Test bằng ảnh chụp THẬT (phiếu đã tô + bài tự luận viết tay) để kiểm
   chứng độ chính xác đọc của DocPhieuTraLoi/CHV_Grader — cần bản in.
2. ~~Sửa answer_parser_service để trích đáp án câu TF~~ — ĐÃ XONG (thực
   ra đã xong từ Version 2.27, ghi chú cũ lỗi thời). Kiểm chứng bằng
   tests/test_answer_parser_bank.py trên toàn bộ 46 generator thật.
   Việc còn lại của nhánh ảnh: so khớp kết quả DocPhieuTraLoi với
   dap_an_dung của câu TF — làm cùng lúc với mục 1.
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


===============================================================================

# CẬP NHẬT 2026-09-13 — Tài khoản giáo viên (Version 2.46)

Mục "Quản lý lớp học / quản lý tài khoản" và "Dashboard giáo viên" trong các
giai đoạn ở trên nay đã có phần thật, không còn là TODO hoàn toàn:

| | Nội dung | Trạng thái |
|---|---|---|
|9.1|Phân quyền `vai_tro`, chặn `/gv/*`|✅|
|9.2|Đăng ký tài khoản giáo viên (mã mời)|✅|
|9.3|Mỗi giáo viên một kết nối Google Classroom|✅|
|9.4|Khu làm việc giáo viên (`/gv`, ra đề, đề đã tạo, lớp)|✅|
|9.5|Tải mã nguồn `.tex` của đề|✅|
|9.6|Sinh một lượt NHIỀU MÃ ĐỀ riêng biệt|🟡 ô nhập đã có, ghép đề còn sai|
|9.7|Màn hình gán lớp cho giáo viên|⬜ hiện gán bằng SQL|
|9.8|Đặt ma trận chi tiết cho từng đề|⬜|

## Việc tiếp theo (thứ tự đề nghị)

1. Sửa 9.6 — tách `socau_ma_de` thành N đề riêng thay vì dồn vào một đề.
2. Mở rộng ngân hàng câu hỏi sang chương 2, 3 của lớp 10, ưu tiên dạng trả
   lời ngắn mức vận dụng cao (đang là ô mỏng nhất của ma trận).
3. Chỉ mục ngân hàng + bộ dò trùng (Giai đoạn 0 trong docs/20).
