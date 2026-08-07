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

===============================================================================

Version 2.3

Ngày

2026-07-28

Nội dung

- Viết app/services/curriculum_service.py (CN_LoadCurriculum):
  load_curriculum, load_curriculum_for_scope, group_by_muc_do.
- Viết lại app/services/exam_blueprint_service.py: build_blueprint
  chọn câu theo curriculum_id (đúng chuẩn doc 04), thêm
  _chon_curriculum_id (round-robin theo bài/mức độ), giới hạn số
  câu tra_loi_ngan/tu_luan tối đa mỗi chương.
- Viết lại app/services/question_selector_service.py: select_questions
  khớp Mapping theo curriculum_id + Loại câu, có cơ chế xoay vòng
  biến thể nội dung (_xoay_vong_bien_the).
- Thêm chế độ nháp `cho_phep_thieu` xuyên suốt build_blueprint,
  select_questions, generate_exam_pdf_auto: khi Mapping/Generator
  còn thiếu, chèn khung "[THIẾU CÂU HỎI: ...]" vào đúng vị trí
  trong PDF thay vì dừng cả đề. Mặc định false (nghiêm ngặt).
- Cập nhật app/services/exam_assembler_service.py: thêm
  _escape_latex (escape ký tự đặc biệt LaTeX: _ % & # $ { } ~ ^ \)
  cho mọi text thô chèn vào tài liệu (curriculum_id, ghi chú lỗi).
- Cập nhật app/services/pdf_service.py: đặt TEXINPUTS trỏ tới
  data/config để pdflatex luôn tìm thấy ex_test.sty bất kể thư mục
  làm việc của subprocess; bắt lỗi FileNotFoundError (thiếu
  pdflatex) và TimeoutExpired rõ ràng.
- Bổ sung data/config/ex_test.sty (bản chính thức "Ex_test v3.3.4",
  Trần Anh Tuấn & Dương Phước Sang) — thay bản dựng tạm trước đó.
- Cập nhật app/routers/exam.py: endpoint /api/exam/generate-pdf-auto
  thêm tham số `dinh_dang` ("pdf" | "tex" | "zip") — Switch_OutputFormat
  rút gọn thành 1 API, trả PDF/TEX/ZIP của CÙNG một lần sinh đề
  (không sinh lại nên không lệch câu hỏi giữa các định dạng).
- Sửa lỗi cài đặt hệ thống trên VPS: PATH thiếu trong systemd
  service khiến không gọi được pdflatex; cài texlive-lang-other
  cho font tiếng Việt.
- Xác nhận: các file app/core/security.py, app/core/supabase.py,
  app/models/user.py, app/routers/auth.py, app/routers/chat.py,
  app/routers/home.py, app/services/supabase_service.py là công
  việc của Mai Hà Lan làm song song (đăng nhập/đăng ký qua
  Supabase, trang Chat AI nối n8n) — chưa có trong sổ tay trước
  Version 2.3, nay được ghi nhận chính thức.
- Ghi nhận: app/routers/ai.py, app/routers/api.py, app/services/
  ai_service.py, app/services/exam_service.py, app/services/
  request_parser.py hiện đang RỖNG (file trống, chưa triển khai) —
  vai trò dự kiến của các file này (phân tích ngôn ngữ tự nhiên,
  cầu nối Chat → API sinh đề) đang tạm thời đảm nhiệm bởi n8n
  (CHV_Fun) theo doc 06 Version 2.3.
- Xác nhận sai lệch giữa doc 05 (API_SPECIFICATION) và API thực tế
  đang chạy: các route thực tế nằm dưới /api/exam/... (scope,
  generator, resolve-rules, blueprint, blueprint-and-select,
  select-questions, generate-pdf, generate-pdf-auto) khác với
  route dự kiến ban đầu (/api/exam/generate, /api/exam/pdf,
  /api/exam/latex...). Xem mục "Hiện trạng triển khai" trong
  doc 05 Version 2.3.

Người thực hiện

Mai Hà Lan


===============================================================================

Version 2.4

Ngày

2026-08-06

Nội dung

- Sửa lỗi frontend/backend không khớp response (chat.html kỳ vọng
  data.reply nhưng backend trả shape khác) — nguyên nhân chính khiến
  chat báo "Lỗi kết nối" dù n8n đã xử lý thành công.
- Thêm phiên đăng nhập thật: app/core/deps.py (get_current_user đọc
  cookie sb_access_token, xác thực qua Supabase); /chat bắt buộc
  đăng nhập, chưa đăng nhập thì chuyển hướng /login; /login set
  cookie HttpOnly sb_access_token + sb_refresh_token; thêm /logout.
- Thêm lưu lịch sử hội thoại: bảng chat_history (mỗi dòng 1 tin
  nhắn, gắn user_id + conversation_id do frontend sinh bằng
  crypto.randomUUID() và giữ nguyên trong suốt 1 cuộc chat).
- Thêm lưu đề đã sinh: bảng de_da_sinh (metadata mỗi lần sinh đề:
  user_id, conversation_id, lop, role, loai_he_so, ki_thi,
  pham_vi_chuong) và file_de (đường dẫn file: de/loigiai/tex, gắn
  de_id).
  ĐỘ LỆCH SO VỚI DOC 12: doc 12 đặt tên 2 bảng này là exam_history/
  exam_files, nhưng exam_history đã tồn tại sẵn trong DB với vai trò
  khác (lưu kết quả chấm bài: diem, chi_tiet_bai_lam — tương ứng
  learning_history trong doc 12). Để tránh xung đột, dùng tên mới
  de_da_sinh/file_de. Cần rà soát lại khi triển khai WF007 (chấm bài)
  để không đặt trùng tên lần nữa.
- RLS (Row Level Security) tắt trên cả 3 bảng mới (chat_history,
  de_da_sinh, file_de) — chủ đích: chỉ FastAPI được đọc/ghi các bảng
  này, đúng nguyên tắc "Frontend không đọc Database trực tiếp"
  (doc 13), nên không cần RLS theo policy của từng user.
- Thêm tính năng "xuất đáp án": endpoint POST /api/exam/export-loigiai
  nhận conversation_id, lấy đề đã sinh gần nhất trong hội thoại đó
  từ de_da_sinh/file_de, đổi \usepackage[dethi]{ex_test} thành
  \usepackage[loigiai]{ex_test} trong file .tex đã lưu rồi biên dịch
  lại — KHÔNG chọn lại câu hỏi, không sinh lại đề. Nếu đề đã bị dọn
  (quá 1 ngày) thì trả lỗi 410 yêu cầu tạo đề mới.
- n8n: thêm nhánh nhận diện "xuất đáp án" — CHV_Fun đã có sẵn task
  download_file, thêm Switch rule 6 (task == "download_file"), thêm
  node Goi_API_XuatDapAn (nhân bản từ Goi_API_Sinh_De, gọi
  /api/exam/export-loigiai) nối vào Respond to Webhook.
- Thêm cron dọn file cũ: scripts/cleanup_old_files.py, chạy 3h sáng
  mỗi ngày, xoá file trong data/exports, data/temp,
  app/static/downloads cũ hơn 1 ngày. Đánh đổi đã thống nhất với
  người dùng: yêu cầu "xuất đáp án" cho đề tạo hơn 1 ngày trước sẽ
  không tái sử dụng được, phải tạo đề mới.
- Frontend chat.html: thêm nút "Về trang chủ"; thêm 2 hàm
  taiDanhSachLichSu()/moHoiThoai() đọc GET /api/chat/history và
  GET /api/chat/history/{conversation_id} để hiện lịch sử hội thoại
  thật ở sidebar (thay 3 mục giả cứng), bấm vào 1 mục sẽ nạp lại
  đúng conversation_id và toàn bộ tin nhắn cũ để tiếp tục hội thoại.
- Backend: thêm GET /api/chat/history, GET /api/chat/history/
  {conversation_id} (app/routers/chat.py) và app/services/
  history_service.py (toàn bộ hàm đọc/ghi chat_history, de_da_sinh,
  file_de — có try/except, lỗi Supabase không làm crash chat).

Ghi nhận còn thiếu / để sau

- Switch trong n8n còn 4 rule cũ (analyze_result, study_advice,
  history, general_chat) không khớp với bất kỳ giá trị task nào
  CHV_Fun thực tế trả về — code chết, cần dọn khi làm WF002/WF003.
- WF001-WF007 trong doc 06 vẫn là mục tiêu kiến trúc, thực tế mới
  triển khai 2 nhánh (sinh đề, xuất đáp án) trong 1 workflow gộp,
  chưa tách thành các Workflow độc lập như doc 06 mô tả.
- Chưa cập nhật nginx config vào git (deploy/nginx/).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.5

Ngày

2026-08-06

Nội dung

- Bắt đầu Giai đoạn A hướng tới WF007_GradeExam (chấm bài), theo lộ trình
  đã thống nhất: WF007 (chấm bài) -> WF003 (phân tích học lực) -> WF002
  (sinh đề theo năng lực), vì WF003/WF002 đều cần dữ liệu điểm số có được
  từ WF007 trước.
- Phát hiện quan trọng: hệ thống hiện tại không có "Question Object" tách
  field (generator_id, answer, solution...) như doc 03 mô tả cho Generator
  dạng mã đề — mỗi câu chỉ là 1 chuỗi LaTeX (latex_block). Tuy nhiên đáp án
  ĐÃ có sẵn trong chuỗi đó dưới dạng macro của ex_test.sty (\True đánh dấu
  đáp án đúng trong \choice, \shortans chứa đáp án tự luận ngắn, \loigiai
  chứa lời giải) — không cần sửa từng hàm sinh câu trong ngân hàng đề.
- Thêm app/services/answer_parser_service.py (CN_GradeAnswer — bước chuẩn
  bị): đọc latex_block bằng cách đếm ngoặc {} lồng nhau (không dùng regex
  đơn giản, vì nội dung LaTeX bên trong có thể chứa {} lồng như \frac{a}{b}),
  trích được: loai_cau (MC/SA/TL), dap_an_dung, phuong_an (4 lựa chọn A-D
  cho MC), loi_giai. Đã kiểm chứng bằng dữ liệu thật qua endpoint debug
  POST /api/exam/debug-parse-answer.
- Hạn chế đã biết: câu tự luận nhiều ý nhỏ dùng lệnh \SA{...} (bí danh của
  \shortans, xem TL_answer_const trong math_type.py) cho đáp số TỪNG Ý —
  bộ trích hiện tại chưa tách được đáp số riêng từng ý, chỉ lấy được lời
  giải chung. Cần tinh chỉnh thêm khi làm chấm câu tự luận nhiều ý.
- Sửa app/services/exam_assembler_service.py: trong lúc sinh đề (đúng 1
  lần gọi generate_exam_pdf_auto, KHÔNG sinh lại câu hỏi), trích đáp án
  của từng câu ngay từ latex_block vừa dùng để ghép PDF, lưu thành 1 file
  JSON (data/temp/{filename}_dapan.json) — đảm bảo JSON này luôn khớp
  100% với đúng đề PDF đã phát cho học sinh trong lần sinh đó.
- Lưu đường dẫn JSON đáp án vào bảng file_de với loai_file = "dapan_json".
  Phải sửa lại CHECK constraint file_de_loai_file_check trên Supabase
  (trước đó chỉ cho phép de/tex/loigiai) để thêm giá trị dapan_json.

Ghi nhận lỗi phát hiện thêm (chưa sửa, để sau)

- Khi yêu cầu tạo đề bằng tên chủ đề (vd "chương mệnh đề") thay vì số
  chương (vd "chương 1"), pham_vi_chuong bị CHV_Fun/n8n trả về sai định
  dạng (vd "menh_de" thay vì "chuong_1"), làm crash
  exam_scope_service.load_scope_heso1 (int("menh_de") lỗi ValueError).
  Không liên quan tới Version 2.5, phát hiện tình cờ khi test.

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.3

Ngày

2026-07-28

Nội dung

- Gộp CN_LoadCurriculum, CN_BuildBlueprint, CN_LoadMapping,
  CN_QuestionSelector, CN_CallPythonGenerator, CN_ExamAssembler thành 1 hàm
  generate_exam_pdf_auto() trong app/services/exam_assembler_service.py,
  chạy trong tiến trình FastAPI (không còn là Code Node riêng trong n8n).
- n8n WF001 chỉ còn 2 việc: CHV_Fun (suy ra tham số JSON) + HTTP Request
  gọi thẳng POST /api/exam/generate-pdf-auto, nhận file nhị phân trả về.
- Thêm API POST /api/exam/generate-pdf-auto (lop, tieu_de, role, loai_he_so,
  ki_thi, pham_vi_chuong, cau_truc_tu_hoc_sinh, socau_ma_de, cho_phep_thieu,
  dinh_dang) — trả file PDF/TEX/ZIP.
- CN_QuestionValidator chưa triển khai; thay bằng cơ chế cho_phep_thieu
  (chế độ nháp, hiện khung "[THIẾU CÂU HỎI: ...]" thay vì lỗi dừng cả đề).
- Đăng nhập/Đăng ký triển khai thực tế bằng Supabase Auth + trang HTML
  (Jinja2), không phải API JSON /api/auth/* như dự kiến ban đầu.

Người thực hiện

Mai Hà Lan

===============================================================================

Version 2.4

Ngày

2026-08-06

Nội dung

- /chat bắt buộc đăng nhập, nhận {message, conversation_id}, giữ đúng 1
  conversation_id trong suốt phiên chat (không tạo lại khi gửi tin tiếp).
- Thêm GET /api/chat/history và GET /api/chat/history/{conversation_id}.
- Thêm POST /api/exam/export-loigiai (tái sử dụng đề vừa sinh gần nhất
  trong hội thoại để xuất PDF lời giải, không sinh lại đề).
- Login/Register dùng Supabase Auth, set cookie sb_access_token,
  sb_refresh_token.
- Database: đề đã sinh lưu ở 2 bảng mới — de_da_sinh (metadata mỗi lần
  sinh đề) và file_de (đường dẫn file, loai_file ∈ {de, tex, loigiai}).
  exam_history (bảng có sẵn từ trước) đổi vai trò sang lưu kết quả chấm
  bài thay vì lưu đề. RLS tắt trên de_da_sinh, file_de, chat_history
  (chủ đích — chỉ FastAPI được đọc/ghi).
- Frontend: đã có chat AI sinh đề qua hội thoại, xuất đáp án, lịch sử hội
  thoại thật ở sidebar, nút "Về trang chủ". Chưa có: dashboard, làm bài
  online, phân tích học tập, nút "Luyện tập ngay", quản lý lớp/tài khoản.

Người thực hiện

Mai Hà Lan

===============================================================================

Version 2.5

Ngày

2026-08-06

Nội dung

- file_de.loai_file bổ sung giá trị thứ 4: dapan_json (chuẩn bị dữ liệu
  cho bước chấm bài — WF007). Sửa CHECK constraint file_de_loai_file_check
  trên Supabase để cho phép giá trị mới.

Người thực hiện

Mai Hà Lan

===============================================================================

Version 2.6

Ngày

2026-08-07

Nội dung

- Giai đoạn A (chấm bài tự động MC/SA) hoàn tất A1-A4:
  - A1: app/services/answer_parser_service.py — trích đáp án đúng và lời
    giải từ latex_block do Generator Function trả về.
  - A2: Mỗi lần sinh đề tự động lưu đáp án từng câu thành JSON
    (data/temp/{ten_file}_dapan.json), đăng ký vào file_de với
    loai_file = dapan_json.
  - A3: Thêm POST /api/exam/grade — chấm tự động câu MC/SA bằng so khớp
    trực tiếp với JSON đáp án đã lưu ở A2; câu TL trả về trạng thái
    can_cham_tay kèm loi_giai (chờ CHV_Grader).
  - A4: Kết quả chấm được lưu vào bảng exam_history (student_id,
    de_thi_id, diem, created_at).
- Bugfix: trigger on_auth_user_created (hàm handle_new_user) chỉ có hiệu
  lực cho tài khoản đăng ký SAU khi trigger được tạo; các tài khoản đăng
  ký trước đó bị thiếu dòng profiles tương ứng, gây lỗi khóa ngoại khi
  ghi exam_history. Đã backfill thủ công cho các tài khoản đang thiếu.
- RLS: tắt row level security cho bảng exam_history (bảng có từ trước
  Version 2.0, không nằm trong nhóm 3 bảng đã tắt RLS ở Version 2.4).
- Ghi chú tồn đọng: format Grade Result thực tế trả về từ /api/exam/grade
  (so_thu_tu, loai_cau, dung, dap_an_hoc_sinh, dap_an_dung, trang_thai,
  loi_giai) CHƯA khớp hoàn toàn với schema Grade Result mô tả ở
  docs/03_DATA_STRUCTURE.md (question_id, dung_sai_hoac_diem, diem_toi_da,
  nhan_xet, tags). Cần quyết định trước khi xây CHV_Grader.

Người thực hiện

Mai Hà Lan
