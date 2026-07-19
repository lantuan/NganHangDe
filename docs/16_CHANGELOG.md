# CHANGELOG

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Theo dõi các thay đổi lớn của dự án. Không ghi thay đổi nhỏ như
sửa chính tả hoặc định dạng.

---

===============================================================================

Version 2.0

Ngày

2026-07

Trạng thái

LOCKED

Nội dung

- Chuẩn hóa lại toàn bộ sổ tay kỹ thuật theo đúng luồng thực tế
  đã triển khai và kiểm chứng cùng người phát triển.
- Sửa mã loại câu: DS → TF (Đúng/Sai).
- Thêm ngoại lệ ID: câu TF ra theo chương, không theo bài, ID rút
  gọn L<khối>_C<chương>_TF_<phiên bản>.
- Thêm quy tắc: Curriculum không có mức VDC; mọi câu VDC dùng
  chung curriculum_id mức VD; quyết định VD/VDC nằm ở
  CN_QuestionSelector.
- Rút gọn AI Agent từ nhiều AI dự kiến (RequestParser, ExamPlanner,
  ExamScopeResolver, BlueprintBuilder, PythonSelector...) xuống
  còn đúng 3 AI: CHV_Fun, CHV_Grader, CHV_Analyzer.
- Chuyển toàn bộ bước xác định phạm vi PPCT, xây Blueprint, chọn
  Generator ID sang Code Node (CN_LoadExamScope, CN_BuildBlueprint,
  CN_QuestionSelector) — không dùng AI.
- Thêm CHV_Grader: chấm câu tự luận dựa trên answer/solution có
  sẵn trong Question Object do Python Generator sinh ra.
- Thêm CN_GradeAnswer, CN_MergeGradeResult, CN_AnalyzeResults.
- Thêm WF007_GradeExam.
- Chuẩn hóa Response API theo doc 05 cho toàn bộ endpoint.
- Cập nhật toàn bộ sơ đồ kiến trúc (doc 01), N8N Workflow (doc 06),
  Exam Generation (doc 09), Data Structure (doc 03), Database
  (doc 12), Frontend (doc 13) cho khớp với luồng 3 AI này.
- Cập nhật Prompt Library (doc 18) và System Map (doc 19) tương ứng.

Người thực hiện

Mai Hà Lan

---

# Quy tắc

- Chỉ ghi các thay đổi lớn.
- Không xóa lịch sử phiên bản kể từ Version 2.0 trở đi.
- Phiên bản mới luôn thêm xuống cuối.
- Sau khi phát hành Version 2.0, mọi thay đổi đều phải cập nhật
  Changelog.


===============================================================================

Version 2.1

Ngày

2026-07-19

Nội dung

- Thêm API /api/data/exam-scope/{lop}/{ki_thi}.
- Thêm app/services/exam_scope_service.py:
  - load_scope_heso1: phạm vi bài cho kiểm tra thường xuyên (HeSo1).
  - load_scope_heso23: phạm vi bài cho giữa kỳ/cuối kỳ (HeSo2_HeSo3),
    có chia tỷ lệ 30/70 cho cuối kỳ.
  - load_exam_scope: hàm điều phối (dispatcher) giữa hai case trên.

Người thực hiện

Mai Hà Lan



===== FILE: docs/16_CHANGELOG.md (thêm vào cuối, sau Version 1.1 đã có) =====

===============================================================================

Version 2.2

Ngày

2026-07-19

Nội dung

- Cập nhật 10_PYTHON_GENERATOR.md: chính thức hoá mô hình Generator Function
  nhận tham số (socau, socot/dong) để sinh nhiều mã đề cùng cấu trúc, khác số liệu.
- Cập nhật 03_DATA_STRUCTURE.md: Question Object có thể là chuỗi LaTeX
  (latex_block) thay vì object tách rời field, khi dùng Generator dạng mã đề.
- Ghi nhận math_type.py là thư viện định dạng LaTeX dùng chung cho toàn bộ
  python_bank, không phải Generator Function.
- Quy định: số mã đề (socau) mặc định = 1 cho tài khoản học sinh,
  do tầng FastAPI/n8n quyết định, không đặt cứng trong Generator Function.
- Cập nhật 04_ID_STANDARD.md: chính thức hoá cơ chế "Biến thể nội dung"
  (Content Variant) — một Generator ID có thể có nhiều hàm Python
  (_01, _02, ...) để bổ sung dần độ phong phú ngân hàng đề. Hậu tố _NN
  chỉ tồn tại trong python_bank, không xuất hiện ở Mapping/Curriculum/
  PPCT/Database/API. Bổ sung quy tắc Function Resolution.

Người thực hiện

Mai Hà Lan