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


===============================================================================

Version 2.7

Ngày

2026-08-07

Nội dung

- Sửa /api/exam/grade để trả đúng schema Grade Result theo
  docs/03_DATA_STRUCTURE.md: mỗi câu trong chi_tiet nay có đủ question_id,
  loai_cau, dung_sai_hoac_diem, diem_toi_da, nhan_xet, chuong, bai, tags
  (bên cạnh các field hiển thị cũ: so_thu_tu, dap_an_hoc_sinh, dap_an_dung,
  loi_giai, trang_thai — giữ lại vì doc 03 dùng "Gồm" chứ không giới hạn
  chỉ đúng các field liệt kê).
- Thêm app/services/mapping_service.py::trich_chuong_bai(generator_id) —
  suy ra (chuong, bai) từ Generator ID theo quy tắc ID Standard (doc 04).
- tags hiện luôn là [] (chưa nối với trường "Dang" trong Mapping) — cần bổ
  sung khi làm CN_AnalyzeResults nếu muốn phân tích điểm yếu theo dạng bài.
- Đã kiểm chứng full: gọi /api/exam/grade với dữ liệu thật, xác nhận
  exam_history.chi_tiet_bai_lam lưu đúng field mới, điểm tổng không đổi
  (7.5, không có regression so với Version 2.6).

Người thực hiện

Mai Hà Lan

===============================================================================

Version 2.8

Ngày

2026-08-12

Nội dung

- Quyết định luồng chấm bài chính thức: học sinh làm bài trên giấy in
  (đề PDF + Phiếu trả lời trắc nghiệm CHUẨN của Bộ GD&ĐT, không tự thiết
  kế phiếu riêng), chụp ảnh gửi lên để AI chấm — thay cho phương án làm
  bài online/quét bài tự động ban đầu dự kiến.
- n8n: thêm 2 nhánh Webhook độc lập trong CÙNG workflow NganHangDe (không
  đi qua CHV_Fun/Switch — đây là các lệnh gọi máy-tới-máy, không phải hội
  thoại tự nhiên):
  - doc-phieu-tra-loi -> Convert to File (Move Base64 String to File,
    chuyển field anh_base64 thành binary thật) -> DocPhieuTraLoi (AI
    Agent, model google/gemini-2.0-flash-001, bật "Automatically
    Passthrough Binary Images") -> Respond to Webhook. Đọc ảnh Phiếu
    TLTN đã tô (MC/TF/SA theo so_luong yêu cầu), trả JSON
    {mc, tf, sa} theo vị trí thứ tự trong từng phần.
  - cham-tu-luan -> Convert to File (cùng cơ chế) -> CHV_Grader (AI
    Agent, model google/gemini-2.5-flash) -> Respond to Webhook. Đọc
    ảnh bài làm Tự luận viết tay, chấm theo danh_sach_cau (dap_an_mau =
    loi_giai của từng câu), trả thẳng mảng Grade Result đúng schema
    doc 03.
  - Cả 2 node Respond to Webhook đều phải strip rào markdown
    (```json ... ```) trước JSON.parse vì model đôi khi tự thêm dù đã
    yêu cầu "chỉ trả JSON" trong System Message — dùng
    .replace(/```json/g,'').replace(/```/g,'').trim() trong expression.
  - Đã kiểm chứng: cả 2 node đọc ảnh THẬT (không bịa dữ liệu) — xác nhận
    qua test model text-only vs vision (báo lỗi rõ ràng "No endpoints
    found that support image input" khi chọn nhầm model không hỗ trợ
    ảnh) và test ảnh trắng/không khớp nội dung (model trả null/báo
    "không có nội dung để chấm" thay vì bịa đáp án).
- FastAPI: thêm app/services/grade_photo_service.py + POST
  /api/exam/grade-photo (app/routers/exam.py). Nhận de_id hoặc
  conversation_id, user_id, anh_phieu_base64, anh_tuluan_base64. Tách
  danh_sach_dap_an (đã lưu từ lúc sinh đề, xem Version 2.5) thành 4 nhóm
  MC/SA/TF/TL, gọi 2 webhook n8n ở trên, so khớp MC/SA với dap_an_dung để
  ra đúng/sai, nhận thẳng kết quả TL từ CHV_Grader, gộp thành 1 mảng
  Grade Result (doc 03), lưu vào exam_history nếu có user_id.
- Thêm 2 biến môi trường N8N_WEBHOOK_DOC_PHIEU, N8N_WEBHOOK_CHAM_TU_LUAN
  (app/core/config.py, .env) — trỏ tới URL Production của 2 webhook trên
  (không dùng URL Test).
- HẠN CHẾ ĐÃ BIẾT (chưa xử lý, để sau theo yêu cầu): answer_parser_service
  chưa trích được đáp án đúng cho câu Đúng/Sai (TF, \choiceTFn/\choiceTFt)
  -> mọi câu TF hiện bị lưu nhầm loai_cau="TL" trong *_dapan.json (không
  có dap_an_dung). grade_photo_service dùng generator_id (chứa "_TF_") để
  tách riêng câu TF ra khỏi câu TL thật khi định tuyến ảnh, nhưng CHƯA
  thể tự chấm đúng/sai cho TF (không có đáp án đúng để so sánh) — câu TF
  luôn trả trang_thai="can_cham_tay". Cần sửa answer_parser_service
  trước khi TF chấm tự động được.
- Đã kiểm chứng end-to-end trên production (sinh đề thật qua web, gọi
  POST /api/exam/grade-photo thật, cả 2 webhook n8n Production URL) —
  không lỗi 500/502, đúng schema Grade Result. Ảnh dùng để test là ảnh
  giả (không phải phiếu đã tô/bài làm thật) nên điểm ra 0 — CHƯA kiểm
  chứng độ chính xác đọc ảnh thật (cần bản in để tô/viết tay thật, để
  sau khi có điều kiện in ấn).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.9

Ngày

2026-08-13

Nội dung

- Đơn giản hoá trang đăng nhập (app/templates/auth/login.html): xoá 4
  link nav placeholder (Tính năng/Giải pháp/Bảng giá/Tài liệu) không dẫn
  đi đâu, chỉ giữ logo + Đăng ký.
- "Ghi nhớ đăng nhập" chuyển từ checkbox trang trí sang có tác dụng thật:
  app/routers/auth.py::login() nhận thêm tham số remember (Form); nếu
  tick thì cookie sb_access_token/sb_refresh_token sống lâu như cũ (7/30
  ngày), không tick thì set session cookie (không truyền max_age — tự
  hết khi đóng trình duyệt).
- "Đăng nhập bằng Google" chuyển từ nút trang trí sang OAuth thật qua
  Supabase, theo mô hình client-side.
- CẦN NGƯỜI DÙNG TỰ CẤU HÌNH: bật Google provider trong Supabase
  Dashboard, tạo OAuth Client ID/Secret ở Google Cloud Console, khai báo
  Redirect URL https://nganhangdechv.tech/auth/callback trong Supabase
  Dashboard. Xác nhận SUPABASE_KEY trong .env là khoá "anon public".
- CHƯA kiểm chứng end-to-end (cần cấu hình Dashboard xong mới bấm thử
  được nút Google thật trên production).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.10

Ngày

2026-08-14

Nội dung

- Xac nhan: nguoi dung da tu cau hinh xong Google Cloud Console + Supabase
  Dashboard (Version 2.9) - da bat Google provider, tao OAuth Client
  ID/Secret, dang nhap Google hoat dong that tren production.
- login.html: logo "Ngan Hang De" tren header gio bam vao ve trang chu
  "/" (truoc do la <div> tinh, khong bam duoc).
- "Quen mat khau?" chuyen tu link chet (href="#") sang tro toi trang that
  /forgot-password.
- Them app/templates/auth/forgot_password.html: form nhap email, goi
  supabaseClient.auth.resetPasswordForEmail(email, {redirectTo:
  origin + "/reset-password"}) - Supabase gui email chua link dat lai
  mat khau (hoan toan client-side, khong qua backend).
- Them app/templates/auth/reset_password.html: trang nguoi dung mo tu
  link trong email, Supabase JS tu doc token khoi phuc (recovery) trong
  URL fragment va tu thiet lap phien lam viec khi createClient() chay,
  form nhap mat khau moi 2 lan goi supabaseClient.auth.updateUser({
  password}) de doi mat khau that.
- Them GET /forgot-password va GET /reset-password (app/routers/auth.py)
  - deu truyen supabase_url/supabase_anon_key qua Jinja2 context giong
  /login, de Supabase JS o 2 trang nay hoat dong.
- CAN NGUOI DUNG TU CAU HINH THEM: Supabase Dashboard > Authentication >
  URL Configuration > Redirect URLs - them
  https://nganhangdechv.tech/reset-password vao danh sach cho phep (neu
  chua co thi link trong email dat lai mat khau se bi Supabase tu choi
  redirect).
- CHUA kiem chung end-to-end (can nguoi dung tu bam thu gui email that
  tren production sau khi da them Redirect URL o tren).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.11

Ngày

2026-08-14

Nội dung

- register.html: logo "Ngan Hang De" o ca ben trai (desktop) va o giao
  dien mobile gio bam vao ve trang chu "/" (truoc do la <div>/<span>
  tinh, khong bam duoc); doi ten hien thi thanh "Ngan Hang De AI" cho
  dung ten that cua website.
- Dong bo ten thuong hieu "Ngan Hang De AI" (thay vi "Ngan Hang De" cut
  ngan) o tat ca cac trang xac thuc con lai: login.html (title, logo
  header, loi chao, footer ban quyen), forgot_password.html,
  reset_password.html, callback.html (title + logo/loi chao).
- register.html: link "Dang nhap" o footer chuyen tu link chet (href="#")
  sang tro toi trang that /login.
- Sua loi trang /register/teacher bao loi khi bam nut "Giao vien": route
  nay truoc do render template auth/register_teacher.html (khong ton
  tai trong repo) gay TemplateNotFound. Doi sang render lai template
  auth/teacher_coming_soon.html co san (trang "Sap ra mat" voi icon
  cong truong 🚧), dong thoi viet lai doan gioi thieu cho di dom hon va
  sua nut "Quay lai" tro dung ve /register (truoc do la href="#").
- register.html: bo nut "Tiep tuc" (id="next-btn") vi khong con tac
  dung — 2 the Hoc sinh/Giao vien da dieu huong thang toi
  /register/student, /register/teacher ngay khi bam, khong con di qua
  buoc chon-vai-tro-roi-bam-tiep-tuc (selectRole()/nextStep()) nhu
  thiet ke cu.
- register.html: them hieu ung hover cho thanh chi bao 2 doan ngay tren
  2 the Hoc sinh/Giao vien (truoc do la thanh tinh, khong doi mau) — di
  chuot vao the Hoc sinh thi doan trai chuyen xanh (bg-primary), di
  chuot vao the Giao vien thi doan phai chuyen xanh, dung
  document.getElementById('role-student'/'role-teacher').addEventListener
  ('mouseenter', ...) doi class Tailwind cua step-indicator-1/2.

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.12

Ngày

2026-08-14

Nội dung

- teacher_coming_soon.html (trang "Sap ra mat" khi bam the Giao vien o
  /register/teacher): bo nav "Tinh nang / Bang gia / Huong dan" o header
  vi ca 3 deu la link chet (href="#") khong dan di dau.
- teacher_coming_soon.html: nut "Dang nhap" / "Dang ky" o header truoc
  do la <button> khong co tac dung, doi thanh <a href="/login">,
  <a href="/register"> tro dung ve 2 trang that.
- teacher_coming_soon.html: logo "Ngan Hang De AI" goc trai header gio
  bam vao ve trang chu "/" (truoc do la <div> tinh, khong bam duoc).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.13

Ngày

2026-08-14

Nội dung

- register_student.html: logo "Ngan Hang De AI" goc trai header gio bam
  vao ve trang chu "/" (truoc do la <div> tinh, khong bam duoc).
- register_student.html: bo nav "Tinh nang / Ve chung toi" o header vi
  ca 2 deu la link chet (href="#") khong dan di dau.
- register_student.html: nut "Login" o header doi thanh "Dang nhap" (dung
  tieng Viet giong cac trang khac), tu <button> khong co tac dung doi
  thanh <a href="/login"> tro dung ve trang dang nhap that.
- SUA LOI QUAN TRONG: URL Google Fonts nap icon Material Symbols
  Outlined trong register_student.html bi sai cu phap (chi khai bao 1
  truc "wght@100..700,0..1" nhung dua vao 2 khoang gia tri, thieu khai
  bao truc "FILL") - da kiem chung Google Fonts API tra ve RONG cho URL
  loi nay. He qua: font icon khong tai duoc, trinh duyet hien chu that
  "person"/"mail"/"lock"/"lock_reset" (Inter, roi vao dung 1 vung dem
  danh cho icon 24px) de chong len chu vi du (placeholder) trong 4 o
  nhap Ho ten/Email/Mat khau/Xac nhan mat khau - day chinh la nguyen
  nhan bao loi "chu huong dan va vi du chong len nhau". Sua URL thanh
  "wght,FILL@100..700,0..1" (giong dung mau da dung o cac trang
  login.html, register.html, teacher_coming_soon.html).
- title trang doi tu "QuizAI" (ten sot lai tu ban mau) sang
  "Ngan Hang De AI" cho dung thuong hieu; placeholder o Email cung doi
  tu "hocsinh@quizai.vn" sang "hocsinh@email.com".

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.14

Ngày

2026-08-14

Nội dung

- register_student.html: them nut "Dang ky bang Google" (thanh chia
  "Hoac" + nut, ngay duoi nut "Dang ky" thuong) - dung chung 1 luong
  OAuth voi trang /login: signInWithOAuth (client-side, Supabase JS)
  -> redirect /auth/callback (trang trung chuyen co san) -> POST
  /auth/set-session (endpoint co san) -> set cookie -> /chat. Khong
  them route/endpoint moi, tai su dung toan bo ha tang OAuth da xay o
  Version 2.9.
- app/routers/auth.py: GET /register/student gio truyen them
  supabase_url/supabase_anon_key qua Jinja2 context (truoc do khong
  truyen gi ca) de Supabase JS tren trang nay chay duoc; ca nhanh loi
  cua POST /register/student (dang ky email/mat khau that bai, render
  lai chinh trang nay kem thong bao loi) cung duoc bo sung 2 gia tri
  nay de nut Google khong bi vo tac dung khi dang hien loi.
- Ghi chu ky thuat: khong can phan biet "vai tro" (hoc sinh/giao vien)
  khi dang ky bang Google, vi luong dang ky bang email/mat khau hien
  tai (supabase_service.sign_up) cung KHONG luu truong role nao vao
  user_metadata (chi luu fullname) - he thong hien chua co co che phan
  quyen theo role o buoc dang ky, nen nut Google o day an toan, khong
  lam lech logic sẵn co.

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.15

Ngày

2026-08-14

Nội dung

- Sua Supabase Dashboard > Authentication > URL Configuration: Site URL
  doi tu localhost:3000 sang https://nganhangdechv.tech; Redirect URLs
  bo sung https://nganhangdechv.tech/auth/callback - truoc do thieu nen
  OAuth luon redirect ve localhost:3000 sau khi dang nhap/dang ky bang
  Google tren production.
- Sua ham handle_new_user (Supabase Database Function, trigger
  on_auth_user_created - da ghi nhan lan dau o Version 2.6): truoc do
  chi doc new.raw_user_meta_data ->> 'fullname', dung cho luong dang ky
  email/mat khau (co gui key fullname tu supabase_service.sign_up) nhung
  KHONG dung cho luong Google OAuth (Google tra ve key full_name/name,
  khong phai fullname) -> ho_ten bi NULL -> insert vao public.profiles
  that bai vi cot ho_ten NOT NULL -> loi "Database error saving new
  user" khi dang ky tai khoan Google moi. Sua thanh coalesce lan luot
  fullname -> full_name -> name -> phan truoc @ cua email, dam bao
  ho_ten khong bao gio NULL du dang ky bang duong nao.
- Da kiem chung end-to-end tren production: dang ky tai khoan Google
  moi thanh cong, vao duoc /chat.

Người thực hiện

Mai Hà Lan (cùng Claude)

===============================================================================

Version 2.16

Ngày

2026-08-14

Nội dung

- chat.html: sua font-size nut Gui / + Chat moi / Danh gia hoc luc -
  truoc do CSS chi reset font-family cho button/input/textarea, khong
  reset font-size, nen cac nut nay dung font-size mac dinh cua trinh
  duyet cho form control (nho hon han text thuong), khac voi cac trang
  khac dung Tailwind (da co san text-base/text-lg). Them font-size:
  16px mac dinh cho button/input/textarea, rieng #new-chat-btn/#send-btn
  len 18px cho dong bo voi cac nut CTA o trang dang nhap/dang ky.
- chat.html: logo "Ngan Hang De AI" o sidebar gio bam vao ve trang chu
  "/" (truoc do la <div> tinh, khong bam duoc).
- chat.html: bo nut Home rieng o goc phai header (da thua viec vi logo
  da lam duoc); thay bang the "account-badge" hien ten hien thi + email
  cua tai khoan dang dang nhap, giup nguoi dung phan biet dang dung tai
  khoan nao khi lam bai (hay gap khi mot nguoi dung nhieu tai khoan
  Google/email khac nhau).
- app/routers/chat.py: GET /chat gio truyen them user_email +
  user_display_name qua Jinja2 context. user_display_name uu tien
  user_metadata['fullname'] (dang ky email/mat khau) -> 'full_name'/
  'name' (Google OAuth) -> fallback ve chinh email neu khong co field
  nao.

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.17

Ngày

2026-08-15

Nội dung

- Quyet dinh kien truc quan ly lop (thay cho phuong an dong bo Google
  Classroom API da can nhac o Version 2.16 - qua phuc tap, khong lam):
  hoc sinh TU CHON lop cua minh khi dang nhap lan dau (khong doi chieu
  email tu dong), diem so/cham bai van thuc hien tren Google Classroom
  nhu giao vien dang lam, web nay chi can biet "em nay lop nao" de gom
  du lieu (sinh de/thong ke) theo lop sau nay.
- Them app/core/lop_config.py: DANH_SACH_LOP (dict khoi -> danh sach
  ten lop), hien tai co khoi 10 va 11 (13 lop moi khoi: C1A, C1B, C2A,
  C2B, C3A, C3B, C4, C5A, C5B, C6, C7, C8, C9 - dung ten that tren
  Google Classroom). Khoi 12 se them sau khi giao vien tao xong lop
  tren Classroom - chi can them 1 dong vao file nay, khong phai sua
  code cho nao khac.
- Them app/services/supabase_service.py::lay_lop_hoc_sinh(user_id) va
  cap_nhat_lop_hoc_sinh(user_id, khoi, lop) - doc/ghi 2 cot khoi, lop
  moi trong bang public.profiles.
- Them GET/POST /chon-lop (app/routers/chat.py) va template moi
  app/templates/chat/chon_lop.html: hoc sinh chon 1 trong danh sach
  lop (dropdown co nhom theo Khoi 10/Khoi 11), luu vao profiles.khoi/
  profiles.lop, quay ve /chat. Hoc sinh co the tu quay lai trang nay
  doi lop bat cu luc nao (khong khoa sau khi chon).
- GET /chat gio kiem tra profiles.lop truoc khi cho vao chat: chua
  chon thi chuyen huong /chon-lop, da chon thi truyen them user_khoi/
  user_lop vao context, hien them 1 dong "Khoi X - Lop Y" trong
  account-badge o header (canh ten/email) de hoc sinh biet dang o
  lop nao.
- CAN NGUOI DUNG TU CHAY SQL TREN SUPABASE (SQL Editor) TRUOC KHI
  DUNG TINH NANG NAY - bang public.profiles chua co 2 cot khoi, lop:
      alter table public.profiles
        add column if not exists khoi text,
        add column if not exists lop text;
      alter table public.profiles disable row level security;
  Dong disable RLS de dam bao FastAPI (dung anon key, khong phai JWT
  rieng tung user) doc/ghi duoc 2 cot nay - dung nguyen tac da ap dung
  cho chat_history, de_da_sinh, file_de, exam_history tu Version 2.4/
  2.6 ("chi FastAPI duoc doc/ghi cac bang du lieu app tu quan ly").
- CHUA kiem chung end-to-end tren production (can nguoi dung chay SQL
  o tren truoc, roi thu dang nhap/dang ky moi de xac nhan trang
  /chon-lop hien ra dung luc, chon lop xong vao duoc /chat binh
  thuong).

Người thực hiện

Mai Hà Lan (cùng Claude)



===============================================================================

Version 2.18

Ngày

2026-08-15

Nội dung

- Sua loi giao dien: bam logo/ve trang chu ("/") lam nguoi dung tuong
  nham la bi dang xuat, du phien (cookie sb_access_token) van con hop
  le. Nguyen nhan: app/routers/home.py truoc day khong doc cookie/kiem
  tra dang nhap nhu /chat, luon render index.html voi nut header/CTA
  cung "Dang nhap" bat ke da dang nhap hay chua.
- app/routers/home.py: GET "/" gio goi get_current_user(request) (dung
  ham co san trong app/core/deps.py, cung co che voi /chat), truyen
  da_dang_nhap + user_display_name qua Jinja2 context.
- app/templates/index.html: nut "Dang nhap" o header va nut CTA lon
  "Dang nhap ngay" o Hero deu doi thanh dieu kien {% if da_dang_nhap %}
  - da dang nhap thi hien "Vao Chat" (tro toi /chat) kem loi chao ten
  hien thi o header, chua dang nhap thi giu nguyen nhu cu.
- app/templates/chat/chat.html: them nut "Dang xuat" that trong sidebar
  (duoi nut "Danh gia hoc luc"), tro toi GET /logout (route nay da co
  san tu Version 2.4, xoa cookie sb_access_token/sb_refresh_token va
  chuyen huong ve /login) - truoc do khong co bat ky nut/link nao dan
  toi /logout tren giao dien, chi vao duoc bang cach go thang URL.
- Xac nhan: co che phien lam viec (cookie) khong doi - van giu dang
  nhap xuyen suot cac trang cho toi khi nguoi dung tu bam "Dang xuat"
  hoac cookie het han tu nhien (7/30 ngay neu tick "Ghi nho dang nhap"
  hoac dang nhap Google, session-only neu khong tick). Day la loi hien
  thi/UX o trang chu, khong phai loi mat phien thuc su.
- CHUA kiem chung end-to-end tren production (can nguoi dung tu dang
  nhap, bam logo ve trang chu de xac nhan van thay "Vao Chat" + ten
  hien thi thay vi "Dang nhap", bam "Dang xuat" trong sidebar chat de
  xac nhan ve dung /login va mat phien that).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.19

Ngày

2026-08-15

Nội dung

- Sua loi goc re: "Ghi nho dang nhap" (checkbox o /login, xem Version 2.9)
  tich hay khong tich deu nhu nhau - nguoi dung van bi dang xuat giua
  chung khi dang dung web. Nguyen nhan that su: access_token (JWT) cua
  Supabase mac dinh het han sau ~1 gio KE CA KHI cookie sb_access_token
  con song toi 7 ngay (da tick "Ghi nho dang nhap") - truoc gio khong co
  co che lam moi access_token bang refresh_token, nen sau ~1 gio la
  get_current_user() luon that bai bat ke cookie con han hay khong.
  Checkbox "Ghi nho dang nhap" chi quyet dinh cookie song bao lau qua
  cac lan DONG/MO LAI trinh duyet, khong lien quan gi toi viec tu dang
  xuat giua chung nay - do la 2 co che khac nhau, va truoc gio co che
  thu 2 (lam moi access_token) chua ton tai.
- app/core/deps.py: them ham _thu_lam_moi_phien(refresh_token) - goi
  supabase.auth.refresh_session(refresh_token) de xin access_token moi.
  get_current_user() gio thu get_user(access_token) truoc, neu loi (het
  han) thi tu dong thu lam moi bang refresh_token trong cookie
  sb_refresh_token; neu lam moi thanh cong, luu phien moi vao
  request.state.new_session va tra ve user (khong bat dang nhap lai);
  neu ca 2 token deu khong hop le, tra ve None nhu cu (that su can dang
  nhap lai).
- app/main.py: them middleware HTTP lam_moi_cookie_phien - sau moi
  request, neu request.state.new_session vua duoc get_current_user() dat
  (tuc la vua tu lam moi phien), ghi lai 2 cookie sb_access_token/
  sb_refresh_token moi (7/30 ngay) vao response. Ap dung cho MOI route co
  goi get_current_user() (/chat, /chon-lop, /api/chat/..., trang chu "/"
  tu Version 2.18...), khong phai sua tung route rieng le.
- Da kiem chung logic bang test doc lap (FastAPI TestClient + supabase
  gia lap mo phong dung 4 tinh huong): (1) access_token con han -> tra ve
  dung user, khong dong cookie moi; (2) access_token het han nhung
  refresh_token con hop le -> tu dong lam moi, tra ve dung user, dong
  dung 2 cookie moi; (3) ca 2 token deu het han/khong hop le -> tra ve
  None (bat dang nhap lai), khong dong cookie; (4) khong co cookie nao ->
  tra ve None. Ca 4 truong hop deu dung ky vong.
- CHUA kiem chung end-to-end voi Supabase that tren production (test o
  tren dung supabase gia lap, chua goi refresh_session that qua mang -
  can nguoi dung dang nhap that, doi qua ~1 gio (hoac sua tam thoi JWT
  expiry trong Supabase Dashboard xuong vai phut de test nhanh) roi thao
  tac tiep tren web de xac nhan khong bi vang ra /login).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.20

Ngày

2026-08-15

Nội dung

- Bat dau xay tinh nang tu dong ghep hoc sinh vao lop bang email dong bo
  tu Google Classroom (quyet dinh o Version 2.17 la lam sau, gio lam
  tiep theo yeu cau "hoc sinh dang ky thi tu nhay vao lop, khong can gv
  xac thuc"). Giu nguyen /chon-lop tu chon lam phuong an du phong khi
  khong khop duoc email.
- CAN NGUOI DUNG TU LAM TRUOC TREN GOOGLE CLOUD CONSOLE (da lam xong
  luc viet Version nay): tao OAuth Client ID rieng (khac Client dang
  dung cho dang nhap Google qua Supabase) trong cung project, bat
  Google Classroom API, xin 2 scope classroom.rosters.readonly (doc
  danh sach lop) va classroom.profile.emails (xem email hoc sinh - mac
  dinh Google an email, phai xin rieng scope nay moi thay), them Client
  ID/Secret moi vao .env tren VPS voi 2 ten bien GOOGLE_CLASSROOM_
  CLIENT_ID / GOOGLE_CLASSROOM_CLIENT_SECRET, them chinh email giao
  vien lam Test user (app dang o che do Testing, chua verify voi
  Google) va Authorized redirect URI
  https://nganhangdechv.tech/gv/classroom/callback.
- Them app/core/config.py: doc GOOGLE_CLASSROOM_CLIENT_ID/SECRET tu
  .env (giong cach doc SUPABASE_URL/KEY co san).
- Them app/services/classroom_service.py: tron bo ham xu ly OAuth rieng
  cho Classroom (tao_url_xac_thuc, doi_code_lay_token,
  lam_moi_access_token - goi thang REST API cua Google qua thu vien
  requests, khong dung them SDK google-api-python-client de do phu
  thuoc), luu/doc refresh_token (luu_refresh_token, lay_refresh_token),
  dong_bo_toan_bo (lap qua MA_LOP_CLASSROOM co san tu Version 2.16, goi
  Classroom API courses.students.list cho tung lop, co xu ly phan
  trang, ghi vao bang moi classroom_roster), tim_lop_theo_email (tra
  cuu 1 email, dung boi GET /chat), lay_toan_bo_roster (dung de debug).
- Them app/routers/classroom.py: GET /gv/classroom/connect (chuyen
  huong sang man hinh dong y cua Google), GET /gv/classroom/callback
  (nhan code, doi lay refresh_token, luu lai), GET /gv/classroom/sync
  (dong bo toan bo, tra ve so luong email lay duoc moi lop de kiem tra
  bang mat), GET /gv/classroom/debug-roster (xem toan bo du lieu da
  dong bo). Ca 4 route yeu cau da dang nhap; rieng buoc dang nhap Google
  o /gv/classroom/connect con duoc chinh Google chan them 1 lop nua vi
  app dang "Testing" - chi tai khoan da them lam Test user moi hoan tat
  duoc, tai khoan khac se bi Google bao loi tu man hinh dong y quyen.
- Sua app/routers/chat.py: GET /chat, khi hoc sinh chua co profiles.lop,
  gio thu classroom_service.tim_lop_theo_email(user.email) TRUOC khi
  chuyen huong /chon-lop - khop thi tu dong ghi khoi/lop (giong het
  duong di cua /chon-lop tu chon, chi khac la tu dong), khong khop thi
  roi ve /chon-lop nhu cu (hoc sinh chua duoc dong bo, hoac dang nhap
  bang email khac email tren Classroom).
- CAN NGUOI DUNG TU CHAY SQL TREN SUPABASE (SQL Editor) TRUOC KHI DUNG
  TINH NANG NAY - tao 2 bang moi va tat RLS (dung nguyen tac da ap
  dung cho cac bang app tu quan ly tu Version 2.4):
      create table if not exists public.classroom_oauth (
        id int primary key default 1,
        refresh_token text not null,
        updated_at timestamptz not null default now(),
        constraint classroom_oauth_chi_1_dong check (id = 1)
      );
      alter table public.classroom_oauth disable row level security;

      create table if not exists public.classroom_roster (
        email text primary key,
        khoi text not null,
        lop text not null,
        ho_ten text,
        synced_at timestamptz not null default now()
      );
      alter table public.classroom_roster disable row level security;
- CHUA kiem chung end-to-end tren production (can nguoi dung: (1) chay
  SQL tao 2 bang o tren, (2) them GOOGLE_CLASSROOM_CLIENT_ID/SECRET vao
  .env tren VPS, (3) vao /gv/classroom/connect dang nhap Google that,
  (4) vao /gv/classroom/sync xem thong ke so email moi lop co dung
  khong, (5) vao /gv/classroom/debug-roster xem thu du lieu that -
  DAC BIET kiem tra cot email co dung khong bi rong (neu rong tuc la
  scope classroom.profile.emails chua duoc cap dung), (6) dang ky/dang
  nhap bang 1 email hoc sinh co that trong danh sach de xac nhan tu
  dong vao duoc /chat, khong bi roi ve /chon-lop).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.21

Ngày

2026-08-15

Nội dung

- Lam chieu NGUOC LAI voi Version 2.20 (doc email tu Classroom ve web):
  gio hoc sinh dang ky/chon lop TREN WEB se tu dong duoc GHI DANH (join)
  vao dung lop that tren Google Classroom, khong can giao vien moi tay
  tung em hoac hoc sinh tu nhap ma lop.
- CAN NGUOI DUNG TU LAM TRUOC TREN GOOGLE CLOUD CONSOLE: vao Data Access,
  them 2 scope MOI (ngoai 2 scope da xin o Version 2.20):
      https://www.googleapis.com/auth/classroom.rosters
      (thay cho classroom.rosters.readonly cu - can quyen GHI de them
      hoc sinh, khong chi doc duoc nua)
      https://www.googleapis.com/auth/classroom.courses.readonly
      (de doc duoc ma dang ky/enrollmentCode cua tung lop, bat buoc phai
      co de goi API them hoc sinh)
- CAN NGUOI DUNG LAM LAI /gv/classroom/connect (ket noi lai tu dau) SAU
  KHI da them 2 scope o tren - refresh_token cu chi mang quyen doc, PHAI
  xin lai moi co quyen ghi. Lam lai khong anh huong du lieu classroom_
  roster da dong bo truoc do.
- Sua app/services/classroom_service.py: doi SCOPES (chi tiet o tren),
  them lay_enrollment_code (doc ma dang ky cua 1 lop qua GET /courses/
  {courseId}), them them_hoc_sinh_vao_lop (goi POST /courses/{courseId}/
  students?enrollmentCode=... voi userId=email - coi ma 409 "da la
  thanh vien" la thanh cong, khong phai loi that), them ham cap cao
  tu_dong_ghi_danh_classroom(email, khoi, lop) - KHONG bao gio raise
  loi ra ngoai (chi tra ve {"success": bool, "message": str}), vi day
  la tien ich them, khong duoc phep chan hoc sinh vao /chat cua web du
  Classroom co loi gi (vd email khong phai tai khoan Google that thi
  chi ghi log, hoc sinh van vao /chat binh thuong).
- Sua app/routers/chat.py: POST /chon-lop, ngay sau khi luu lop vao
  profiles, goi them classroom_service.tu_dong_ghi_danh_classroom() -
  khong kiem tra ket qua (theo dung nguyen tac o tren, khong chan luong
  chinh cua hoc sinh).
- Da test logic trong sandbox (gia lap Google tra ve: them hoc sinh moi
  thanh cong, hoc sinh da la thanh vien san (409), email khong phai tai
  khoan Google that (400), lop khong co trong MA_LOP_CLASSROOM) - ca 4
  truong hop deu dung nhu thiet ke, khong co truong hop nao lam crash
  luong /chon-lop.
- CHUA kiem chung end-to-end tren production (can nguoi dung: (1) them
  2 scope moi tren Google Cloud Console, (2) lam lai /gv/classroom/
  connect de xin refresh_token co quyen ghi, (3) dang ky/dang nhap bang
  1 tai khoan Google that, chon 1 lop bat ky o /chon-lop, (4) vao
  Google Classroom lop do (tab Moi nguoi) kiem tra hoc sinh da tu xuat
  hien trong danh sach chua).

Người thực hiện

Mai Hà Lan (cùng Claude)


===============================================================================

Version 2.22

Ngày

2026-08-16

Nội dung

- Test thuc te Version 2.21 tren production: hoc sinh chon lai lop o
  /chon-lop, web goi Google them thang hoc sinh vao lop (courses.
  students.create voi enrollmentCode) - Google tra ve LOI 403
  PERMISSION_DENIED. Nguyen nhan: cach them thang hoc sinh qua API nay
  CHI duoc phep khi nguoi goi la quan tri vien domain Google Workspace
  for Education - khong ap dung duoc voi Classroom tao boi tai khoan
  Gmail ca nhan (nhu nganhangdetoanchv@gmail.com dang dung). Day la gioi
  han cua Google, khong sua duoc bang cach xin them scope.
- SUA LAI CACH LAM (thay Version 2.21): thay vi tu dong them thang hoc
  sinh (khong the lam duoc), sau khi hoc sinh chon lop o /chon-lop, web
  tao san 1 link "Tham gia lop" (dung ma dang ky/enrollment code cua
  lop, dang https://classroom.google.com/c/<course_id ma hoa base64>
  ?cjc=<ma_dang_ky>) va hien thi mot trang xac nhan - hoc sinh chi can
  bam 1 nut, dang nhap dung tai khoan Google, bam "Tham gia" la xong.
  Khong con can tu tim lop hay tu nhap ma tay.
- Them app/services/classroom_service.py: ham tao_link_gia_nhap_lop
  (thay the them_hoc_sinh_vao_lop/tu_dong_ghi_danh_classroom cu - van
  giu lai code cu, khong xoa, phong khi sau nay chuyen sang Google
  Workspace for Education thi dung lai duoc). Them import base64.
- Them app/templates/chat/tham_gia_lop_classroom.html: trang xac nhan
  sau khi chon lop, co nut "Mo Google Classroom & Tham gia" (mo tab moi
  toi link tren), khung hien ma dang ky de nhap tay neu nut khong tu
  nhan dung, va link "Bo qua, vao Chat AI ngay" (khong bat buoc hoc
  sinh phai lam buoc nay).
- Sua app/routers/chat.py: POST /chon-lop, sau khi luu lop, goi
  tao_link_gia_nhap_lop() thay vi tu_dong_ghi_danh_classroom() - neu
  thanh cong thi render trang tham_gia_lop_classroom.html, neu khong
  (vd giao vien chua ket noi Classroom) thi ve /chat nhu binh thuong,
  khong chan hoc sinh.
- Da test logic trong sandbox (mock Google tra ve enrollmentCode, kiem
  tra dung dinh dang link + slug base64 tu course_id, truong hop lop
  khong ton tai, truong hop Google loi khi lay enrollment code) - deu
  dung nhu thiet ke.
- CHUA kiem chung end-to-end tren production (can nguoi dung: (1) dang
  nhap lai bang 1 tai khoan da tung chon lop truoc do - hoac xoa lop cu
  trong Supabase de bi day ve /chon-lop lai, (2) chon 1 lop, (3) kiem
  tra trang xac nhan hien dung link + ma dang ky, (4) bam nut, xac nhan
  Google Classroom tu dong nhan dung lop va ma, chi can bam Tham gia,
  (5) kiem tra lai trong Classroom (tab Moi nguoi) hoc sinh da vao lop
  thanh cong).

Người thực hiện

Mai Hà Lan (cùng Claude))
===============================================================================

Version 2.23

Ngay

2026-08-17

Noi dung

TINH NANG CHINH: "Lam bai truc tiep tren web" (WF007 nhanh WEB, khong
qua chup anh, khong ton token AI) - hoc sinh lam MC/TF/SA ngay tren
trinh duyet, duoc cham diem tu dong ngay lap tuc, cau tu luan van co
the dinh kem anh de CHV_Grader cham qua /grade-photo co san.

1. answer_parser_service.py - trich dap an day du hon
- Them trich_dap_an_tf(): trich dap an cau Dung/Sai (\choiceTFn[N] /
  \choiceTFt, 4 y a/b/c/d doc lap, moi y danh dau \True rieng - khac
  \choice chi co dung 1 dap an). Da kiem chung voi generator that
  L10_C1_TF_A_01.
- Them trich_de_bai(): tach rieng phan "de bai" (hien thi cho hoc
  sinh, AN dap an) tu latex_block, dung cho trang lam bai web. Moc
  chan gom \choiceTFn/\choiceTFt/\shortans/\choice VA \loigiai (them
  \loigiai de chan an toan cho ca cau TL khong co marker nao ca -
  BUG THAT: neu khong co moc nay, toan bo phan loi giai/dap an bi
  lo nguyen vao de bai hien thi cho hoc sinh, phat hien qua test
  thuc te tren production ngay 17/08).
- Them _xoa_khoi_dap_an_an(): don dep cau TL nhieu y ngan dang
  \begin{listEX}...\item... \SA[n]{...}/\shortans[n]{...}...\end{listEX}
  (xem TL_answer_const/TL_answer_text trong math_type.py) - thay moi
  dap an con bang cho trong "......", tranh lo dap an VA tranh loi
  MathJax "Unknown environment listEX" (\SA la bi danh cua \shortans,
  nam LONG trong listEX nen khong bi cac moc tren chan truoc).
- Them _rut_gon_immini(): \immini{TEXT}{HINH_TIKZ} (cau co hinh ve)
  chi giu lai TEXT, bo phan tikzpicture khong the render bang MathJax
  (truoc do gay loi "Unknown environment tikzpicture" y het loi
  listEX o tren).
- Da test lai toan bo 45 ham sinh cau that trong L10_C1.py sau moi
  lan sua, khong con leak loigiai/listEX/immini/tikzpicture trong
  bat ky de bai nao.

2. API moi - GET /api/exam/quiz/{de_id} (app/routers/exam.py)
- Tra ve danh sach cau hoi cua 1 de da sinh, DA AN dap an dung (chi
  co de_bai, phuong_an voi MC, phat_bieu voi TF, khong co gi them
  voi SA, ghi_chu voi TL). Doc tu file dapan_json da luu luc sinh de
  (dung chung nguon voi /grade, /grade-photo, /export-loigiai).
- Tra loi 410 neu khong con file dapan_json (dep sau 1 ngay theo
  cron cleanup_old_files.py co san) - hoc sinh duoc bao ro rang can
  tao de moi, khong loi 500 mo ho.

3. Trang lam bai - GET /lam-bai/{de_id} (app/routers/chat.py) +
   app/templates/chat/lam_bai.html (file moi)
- Goi GET /api/exam/quiz/{de_id} de lay cau hoi, render MC (radio
  4 phuong an)/TF (Dung/Sai cho tung y a/b/c/d)/SA (o nhap text)
  tuong tac duoc; cau TL/co_hinh_ve hien ghi chu "lam ra giay".
  renderLatexText/xuLyDanhSach (JS thuan, khong AI) chuyen doi cac
  macro LaTeX thuong gap (\textbf, \\, \begin{enumerate}...) sang
  HTML, giu nguyen $...$ cho MathJax tu render.
- Nut "Nop bai" goi POST /api/exam/grade (cham MC/TF/SA tu dong).
- Neu de co cau tu luan: hien them 1 o chon/chup anh (khong bat
  buoc). Neu co dinh kem, goi THEM POST /api/exam/grade-photo (chi
  voi anh_tuluan_base64, khong anh_phieu_base64) de cham rieng phan
  tu luan qua CHV_Grader (endpoint nay DA CO SAN va hoat dong that
  tu Version 2.8, chi la chua duoc noi voi trang lam bai web truoc
  gio). Gop ket qua 2 nguon (ham gopKetQua trong JS) thanh 1 diem
  tren 10 duy nhat - tinh lai tu dau dua tren TOAN BO cau da cham
  duoc o ca 2 nguon (khong cong truc tiep 2 diem_tren_10_tam_tinh
  vi moi ben tu chuan hoa /10 tren tap con rieng cua no). Cau TF uu
  tien dung diem_dat_duoc (ty le so_y_dung/4), khong coi la
  true/false toan phan.
- Doc tham so ?cid=<conversation_id> tu URL (do chat.html gan vao
  khi tao link "Bat dau lam bai") de nut "Ve Chat AI" quay lai DUNG
  hoi thoai cu thay vi mo hoi thoai moi rong khong (BUG THAT phat
  hien qua test production: chat.html truoc gio luon tao
  conversationId = crypto.randomUUID() moi hoan toan moi load trang).

4. Cham TF trong /api/exam/grade (app/routers/exam.py) - diem tuyen
   tinh theo ty le
- Truoc gio TF luon tra ve trang_thai=can_cham_tay (answer_parser_service
  chua trich duoc dap an TF). Nay tinh diem = diem_toi_da * so_y_dung/4
  (linear proportional - QUYET DINH RO RANG cua nguoi dung, KHONG
  dung thang diem bac cua Bo GD&DT 0.1/0.25/0.5/1 nhu de xuat ban dau).
  Tra them so_y_dung, chi_tiet_tung_y (dung/sai tung y a/b/c/d) ngoai
  cac field chuan cua Grade Result (doc 03).
- Sua 2 chuoi thong bao khong dau con sot lai tu truoc (nhan_xet cau
  TL, ghi_chu tong ket) - loi khong lien quan TF nhung phat hien cung
  luc khi test.

5. Cau dan vui nhon + luong hoi "lam bai truc tiep" (app/routers/chat.py,
   app/templates/chat/chat.html)
- CAU_DAN_DE (12 bien the), CAU_DAN_LOIGIAI (8 bien the) - random.choice
  thuan Python, KHONG tinh token AI - thay the 2 dong co dinh "Da tao
  de xong."/khong dau truoc do.
- Sau khi tao de (khong phai xin loi giai), chat.py tra them field
  data.de_id (tim qua history_service.lay_de_gan_nhat(conversation_id),
  null neu khong tim thay - khong chan viec tra PDF cho hoc sinh).
- chat.html: neu co de_id, hien 2 nut "Co, lam luon!"/"Khong, de lam
  tren giay" duoi file PDF. Bam Co: doi thanh 1 trong 6 cau giai thich
  (GIAI_THICH_LAM_BAI) + nut "Bat dau lam bai" (mang theo ?cid=...).
  Bam Khong: doi thanh 1 trong 6 cau OK (Y_KHONG_LAM_BAI). Toan bo xu
  ly o JS phia trinh duyet, KHONG goi them n8n/API nao - dung y tuong
  ban dau da duyet ("hoi Co/Khong day du" thay vi ban rut gon truoc do
  chi noi link truc tiep, da bi nguoi dung phat hien va yeu cau quay
  lai dung ban day du).
- Phong cach tra loi cua CHV_Fun (n8n, ngoai repo) cung duoc doi tu
  xung ho "em/anh" sang "ban" (ngang hang) va bo sung chi dan chi
  dung tieng Viet co dau, khong cheo tieng Trung/Anh - xem file rieng
  CHV_Fun_phong_cach_ban_be.txt da gui, khong nam trong repo.

6. Tu dong xoa chat_history sau 10 ngay (scripts/cleanup_chat_history.py,
   file moi) - cron 3h sang, dung SO_NGAY_GIU = 10, doc dung nguyen tac
   "code hon AI" cua doc 00. Ap dung CHUNG 1 con so 10 ngay cho ca noi
   dung chat LAN du lieu cau hoi lam bai web (dapan_json, dung chung
   co che don dep 1 ngay co san cua cleanup_old_files.py - KHONG doi,
   nghia la trang lam bai chi dung duoc ~1 ngay sau khi tao de, ngan
   hon nhieu so voi 10 ngay cua lich su chat - da bao truoc trong cau
   dan giai thich hien cho hoc sinh).

7. Sua tham so "dang" khong duoc ap dung dung khi sinh cau (BUG THAT,
   anh huong tat ca cau SA/MC trong L10_C1.py tu truoc gio)
- Goc bug: data/python_bank/toan10/L10_C1.py co 31 ham dung tham so
  thu 2 ten "dang" (1=MC, 2/3=SA - xem math_type.py) nhung 29/31 ham
  KHONG co gia tri mac dinh (bat buoc phai truyen), va
  app/services/generator_service.py._call_generator_function() khi
  gap tham so ten "dang" ma khong biet gia tri gi thi LUON goi
  func(socau, 1) - tuc LUON ep thanh MC (dang=1) bat ke ham do ten la
  _SA_ hay _MC_. Ket qua: nhung cau du dinh la "tra loi ngan" (SA) bi
  sinh nham thanh trac nghiem (MC) trong moi de da tung sinh ra.
- CACH SUA (theo quyet dinh cua nguoi dung - uu tien sua tan goc trong
  python_bank thay vi truyen dang qua Mapping/exam_assembler_service):
  them dang=1 vao 29 ham _MC_ con thieu mac dinh (2 ham con lai da
  dung san). 2 ham _TL_ (L10_C1_B1_TH003_TL_A_01/02) dung nham ten
  tham so "dang" nhung thuc chat la "dong" (tham so so cot cua
  \begin{listEX}, KHAC nghia voi "dang" cua MC/SA) - doi ten cho dung
  ban chat, giong cac ham TL khac trong file (vd
  L10_C1_B2_VD021_TL_A_01(socau, dong=1)).
- generator_service.py: _call_generator_function them nhanh rieng cho
  second_param == "dang" -> chi goi func(socau) (KHONG truyen gia tri
  cung), de Python tu ap dung dung mac dinh cua tung ham (da sua o
  buoc tren). KHONG con them tham so "dang" rieng vao chu ky ham
  call_generator/exam_assembler_service (thu lam roi bo, theo dung
  yeu cau "it dinh nghia moi nhat co the" cua nguoi dung).
- Da test qua call_generator() that: goi khong truyen gi them cho ca
  3 loai (MC/SA/TL that trong L10_C1.py) deu ra dung loai cau nhu ten
  ham the hien.

8. Trang thong ke nang luc cho GV - GET /gv/thong-ke (trang) + GET
   /gv/thong-ke/data (API JSON), app/routers/classroom.py + ham moi
   history_service.lay_thong_ke_nang_luc() + file moi
   app/templates/teacher/thong_ke.html.
- KHONG can bang moi: doc thang tu exam_history (diem + chi_tiet_bai_lam
  da luu san moi lan cham bai qua /grade hoac /grade-photo), join voi
  profiles (ho_ten/khoi/lop, xem doc 12) o tang Python.
- Hien: 3 the tong quan (so hoc sinh, so luot cham, diem trung binh
  ca lop), bang "chuong/bai ca lop hay sai nhat" (xep theo ty le sai,
  can >=2 luot lam de tranh mau qua nho), bang theo tung hoc sinh
  (diem trung binh, top 3 chuong/bai hay sai). Loc theo khoi/lop qua
  DANH_SACH_LOP (app/core/lop_config.py) co san.
- Cau "sai" tinh thong nhat cho ca cau MC/SA (dung_sai_hoac_diem ===
  false) va cau cham theo diem so (TF/TL tu CHV_Grader) - duoi 50%
  diem toi da tinh la "chua vung", dong vai tro nhu sai trong thong ke.
- Khong co he thong phan quyen giao vien/hoc sinh chinh thuc (dung
  chung nguyen tac "chi can dang nhap" nhu /gv/classroom/* tu Version
  2.20 - he thong hien la 1-giao-vien-ngam-dinh, chua phai da nguoi
  dung).
- Them link "Thong ke nang luc (GV)" vao sidebar app/templates/chat/chat.html.
- Da test logic tong hop bang du lieu gia lap VA goi thang ham route
  that (mock Supabase) - dung nhu thiet ke.

CHUA kiem chung end-to-end tren production

- Nut chup/tai anh cau tu luan tren trang lam bai (muc 3) - da test
  logic gop diem bang Node, CHUA thu tren production voi anh that.
- Trang thong ke nang luc (muc 8) - CHUA mo thu /gv/thong-ke tren
  production voi du lieu that.
- Sua tham so "dang" (muc 7) - da xac nhan code dung tren GitHub/VPS
  (hash khop nhau), CHUA tao thu 1 de co cau SA that de kiem tra PDF
  in ra dung dang tra loi ngan.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.24

Ngày

2026-08-17

Nội dung

1. Sua text khong dau trong thong bao loi chat/classroom/auth
- app/routers/chat.py (4 cho): thong bao "Ban chua dang nhap...",
  "Khong ket noi duoc voi AI sau 2 lan thu...", "AI chua xu ly duoc
  yeu cau nay...", "Khong hieu phan hoi tu n8n." - doi sang co dau
  chuan. Day chinh la nguyen nhan man hinh chat hien chu khong dau
  "AI chua xu ly duoc yeu cau nay..." ma giao vien bao loi.
- app/services/classroom_service.py (12 cho), app/routers/auth.py
  (2 cho): sua tuong tu, du hien chua hien thi truc tiep len UI nhung
  sua truoc cho nhat quan (tranh lo khi sau nay hien thi).

2. Phat hien va sua loi prompt CHV_Fun bi dan nham doan huong dan
   chinh sua vao System Message
- Nguyen nhan sau khi giao vien bao "AI tra loi kem di", kiem tra
  n8n thi phat hien: doan ghi chu huong dan thao tac ("THAY THE doan
  'PHONG CACH CHO FIELD tra_loi' hien tai... bang doan duoi day. Chi
  doi dung doan nay...") da bi dan nguyen van vao GIUA prompt that cua
  CHV_Fun (nam giua rule 4 va doan phong cach tra loi), thay vi chi
  dung lam huong dan roi xoa di. Doan van tu noi ve chinh no nay lam
  nhieu prompt, co the la nguyen nhan AI phan loai/tra loi kem chinh
  xac hon.
- Da gui giao vien toan van System Message da sua (bo dung doan thua,
  giu nguyen moi phan con lai) de dan de vao n8n. KHONG the tu sua
  truc tiep trong n8n (khong co quyen truy cap).

3. Them loi chao mo dau khi vao chat moi
- app/templates/chat/chat.html: bank LOI_CHAO_MO_DAU (4 bien the,
  random.choice thuan JS, khong ton AI token) - tu dong hien khi vao
  /chat lan dau (khong co ?cid=) hoac bam "+ Chat moi". Noi dung: chao
  hoi + tom tat AI lam duoc gi (tao de, xin loi giai, lam bai truc
  tiep tren web, danh gia hoc luc dang phat trien) + hoi hoc sinh muon
  tao de luon hay con thac mac gi. Thay the khoi HTML tinh cu (chi co
  logo + 1 dong text, khong tuong tac).

4. Phat hien them 1 AI node chua duoc ghi vao so tay: GenerateExam_RequestParser
- Node nay chay khi CHV_Fun phan loai task="generate_exam", doc yeu
  cau hoc sinh, neu thieu cau truc de (so cau/ty le muc do) thi tra
  Table Tool "QuyDinhSoLuongCauTrongDe" de lay cau truc chuan:
  + HeSo1 (kiem tra thuong xuyen/15 phut/mieng): 12 cau = 6 TN + 1
    Dung/Sai + 2 Tra loi ngan + 3 Tu luan, ty le muc do NB 40% -
    TH 30% - VD 20% - VDC 10%.
  + HeSo2_HeSo3 (giua ky/cuoi ky/hoc ky): 20 cau = 12 TN + 2 Dung/Sai
    + 3 Tra loi ngan + 3 Tu luan, cung ty le muc do nhu tren.
  Neu hoc sinh da tu quy dinh 1 phan/toan bo cau truc thi uu tien
  dung yeu cau do, khong ghi de bang du lieu bang.
- Da cap nhat doc 06/07/08 (xem cac muc "Cap nhat 2026-08-17"/"DINH
  CHINH 2026-08-17" tuong ung) de ghi lai dung kien truc thuc te dang
  chay, bao gom ca 2 Code Node ho tro: Parse_RequestParserOutput
  (JSON.parse output cua GenerateExam_RequestParser, throw loi neu
  JSON hong) va "Code in JavaScript" (build cau tra loi chat cho cac
  nhanh help/reject_math_solution/reject_out_of_scope/Fallback, dung
  ngan hang 8 cau "chua xong" vui nhon khi CHV_Fun khong co tra_loi).

5. Dang thiet ke (CHUA trien khai): tinh nang "hoi xac nhan cau truc
   de truoc khi tao" - khi hoc sinh khong noi ro so cau/ty le muc do,
   AI se de xuat san cau truc theo bang chuan roi hoi xac nhan ("dong
   y thi minh lam luon, hoac ban noi cu the muon doi gi") thay vi tu
   dien lang le nhu hien tai. Can sua them prompt CHV_Fun (nhan dien
   luot "dong y" tiep theo van la generate_exam) + GenerateExam_RequestParser
   (them nhanh hoi xac nhan) + 1 node dieu huong moi trong n8n (IF
   kiem tra can_xac_nhan). Dang cho giao vien quyet dinh phuong an cu
   the (van ban "dong y" hay nut bam) truoc khi trien khai, de tranh
   lap lai loi dan nham prompt nhu muc 2.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.25

Ngày

2026-08-17

Nội dung

1. Trien khai tinh nang "hoi xac nhan cau truc de truoc khi tao" (da
   thiet ke o Version 2.24, muc 5)
- Phat hien bug quan trong o node Ghep_Tham_So (n8n): code cu luon gan
  cung "cau_truc_tu_hoc_sinh: null" va "socau_ma_de: null" khi goi API
  /api/exam/generate-pdf-auto - nghia la du GenerateExam_RequestParser
  co tinh dung so cau (tu bang QuyDinhSoLuongCauTrongDe hoac tu chinh
  yeu cau hoc sinh), so lieu do bi VUT BO truoc khi toi backend. Hoc
  sinh tu noi ro so cau ("30 cau", "20 cau trac nghiem"...) bi lo di,
  backend luon dung mac dinh rieng cua no (data/config/exam_rules.json).
  Da sua Ghep_Tham_So de forward dung so cau moi loai tu p.cau_truc_
  tong_quat (AN TOAN vi khi nguon_cau_truc="table" so lieu nay von
  giong het mac dinh backend - da doi chieu 2 bang khop nhau). KHONG
  forward ty_le_muc_do_goc (1 ty le CHUNG cho ca de) vi backend can ty
  le RIENG cho tung loai cau (data/config/exam_rules.json), ap chung
  se lam hong cau dung/sai va tu luan - phan nay van de backend tu
  dung bang chuan rieng.
- GenerateExam_RequestParser (n8n): them field can_xac_nhan. Khi
  nguon_cau_truc = "table" hoac "mixed" (co it nhat 1 phan so lieu tu
  Table Tool, khong phai hoc sinh tu noi) -> KHONG ra de ngay, xuat
  JSON hoi xac nhan (can_xac_nhan=true, tra_loi = cau hoi neu ro so
  lieu se dung) kem theo de_xuat (cau_truc_tong_quat, ty_le_muc_do_goc,
  lop, loai_he_so, ki_thi, pham_vi_chuong). Khi nguon_cau_truc="user"
  (hoc sinh da noi ro toan bo) -> ra de ngay nhu cu, khong hoi.
- Them 1 node IF moi (kiem tra can_xac_nhan) + 1 node Code moi (build
  cau tra loi {success,message,data:{type:"xac_nhan_de",de_xuat}}) giua
  Parse_RequestParserOutput va Ghep_Tham_So, noi nhanh true vao lai
  "Respond to Webhook1" co san (dung chung dinh dang JSON voi nhanh
  help/reject_*/Fallback cua CHV_Fun).
- QUAN TRONG: luot "dong y" tiep theo cua hoc sinh KHONG di qua CHV_Fun/
  GenerateExam_RequestParser nua (khong ton them token AI) - chat.html
  hien 2 nut "Dong y, tao de" / "De minh noi cu the hon" ngay duoi cau
  hoi xac nhan; bam "Dong y" goi THANG /api/exam/generate-pdf-auto tu
  JS (dung lai dung nguyen de_xuat da nhan duoc), khong goi lai webhook
  n8n. Day la ly do chon phuong an nut bam thay vi hoc sinh go chu
  "dong y" (phuong an do se can AI phan loai lai, ton them token va
  rui ro nham giong loi dan prompt tung gap o Version 2.24).
- app/routers/exam.py: them API moi GET /api/exam/de-gan-nhat?
  conversation_id=... - tra ve de_id cua de moi nhat trong 1 hoi thoai,
  dung de hien nut Co/Khong lam bai truc tiep SAU KHI tao de qua duong
  goi thang nay (vi FileResponse cua generate-pdf-auto khong tra ve
  de_id, chi tra file PDF thuan tuy).
- app/routers/chat.py: them user_id vao context Jinja2 cua GET /chat
  (truoc chi co user_email/user_display_name/user_khoi/user_lop) - de
  JS o chat.html biet duoc user hien tai khi goi thang generate-pdf-auto.
- app/templates/chat/chat.html: them CURRENT_USER_ID, nhanh xu ly
  data.data.type==="xac_nhan_de" trong sendMessage(), 2 ham moi
  doiYeuCauDe() va xacNhanTaoDe() (fetch generate-pdf-auto, nhan blob
  PDF, tao download link, goi tiep /de-gan-nhat de lay de_id hien nut
  Co/Khong lam bai truc tiep - tai su dung dung UI/logic cua chonLamBai()
  da co).
- Da test: py_compile app/routers/exam.py + chat.py, node --check +
  Jinja2 render chat.html (kiem tra CURRENT_USER_ID duoc dien dung tu
  context). CHUA test duoc phan n8n (IF node moi, Ghep_Tham_So sua) vi
  khong co quyen truy cap n8n - giao vien tu them/noi node theo huong
  dan rieng (file n8n_HUONG_DAN_va_noi_dung.txt) roi tu kiem tra tren
  production.

2. Kiem tra lai tieu de PDF (task ton dong tu Version 2.16/#16)
- Doc lai dung code Ghep_Tham_So hien tai: dong xay tieu_de
  (`Đề ${loai_he_so === "HeSo1" ? "kiểm tra" : "thi"} - Toán ${p.lop}`)
  DA CO DAU DUNG CHUAN san, khong co cho nao lam mat dau trong _escape_
  latex (app/services/exam_assembler_service.py) hay latex_service.py.
  Chua xac dinh duoc nguyen nhan thuc su cua loi "tieu de khong dau" -
  can giao vien gui 1 vi du PDF moi tao + tieu de thuc te hien ra de
  dieu tra tiep (co the la file PDF cu tao truoc khi sua, hoac loi o
  buoc khac chua ro).

CHUA kiem chung end-to-end tren production

- Toan bo tinh nang "hoi xac nhan cau truc de" (muc 1) - CHUA test that
  tren n8n/production (can giao vien tu ap dung 3 buoc trong file
  n8n_HUONG_DAN_va_noi_dung.txt roi thu tao 1 de khong ro cau truc).
- Loi tieu de PDF khong dau (muc 2) - van CHUA xac dinh duoc nguyen
  nhan that su, dang cho vi du cu the tu giao vien.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.26

Ngày

2026-08-18

Nội dung

1. Sua bug AI nham so trong "chuong X" thanh "lop"
- Test thuc te tren n8n (giao vien gui anh Executions log): yeu cau
  "tao de chuong 1" (hoc sinh Khoi 10) bi GenerateExam_RequestParser
  trich nham thanh lop=1 (lop 1 tieu hoc!) thay vi lop=10 mac dinh,
  khien Goi_API_Sinh_De loi 500 Internal Server Error (khong co du
  lieu THPT cho lop 1).
- Sua prompt GenerateExam_RequestParser (BUOC 1): them quy tac ro rang
  - lop CHI duoc la 10/11/12, CHI gan gia tri khi so do di lien voi
  chu "lop" trong cau, tuyet doi khong suy luan tu so trong "chuong
  X"/"bai X"/"cau X". Khong noi ro lop kem chu "lop" o dau -> mac dinh
  lop=10.
- app/routers/exam.py, generate_exam_pdf_auto_endpoint: them kiem tra
  som "payload.lop not in (10, 11, 12)" -> HTTPException 400 ro rang,
  thay vi de cac ham ben duoi crash 500 kho hieu neu lan sau AI van
  lo trich sai (phong thu them, khong thay the cho viec sua prompt).
- Da test: py_compile app/routers/exam.py sach. CHUA test lai tren
  n8n voi prompt moi (giao vien tu dan va thu lai).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.27

Ngày

2026-08-18

Nội dung

1. Sua bug NGHIEM TRONG: cau Dung/Sai (TF) mat dinh dang khi xuat PDF
- Giao vien bao: cau TF tren trang lam bai online (quiz web) hien dung
  dinh dang, nhung ban PDF ("ban giay") lai in 4 y a/b/c/d thanh 1 doan
  van chay lien, khong con khung Dung/Sai nhu ban giao vien tu soan.
- Nguyen nhan: data/python_bank/math_type.py (ham phatbieu_giai va
  TF_baitoan_du, dung chung cho TOAN BO cau TF trong ngan hang de) chon
  lenh LaTeX theo tham so "socot": socot in {1,2,3,4} -> dung
  "\choiceTFn[N]"; con lai -> "\choiceTFt". NHUNG "\choiceTFn" KHONG
  HE TON TAI trong data/config/ex_test.sty - chi co "\choiceTFt" duoc
  dinh nghia that (\newcommand{\choiceTFt}...). generator_service.py
  mac dinh socot=4 khi khong truyen gi them, nen MOI cau TF khi xuat
  PDF deu roi vao nhanh "\choiceTFn[4]" khong ton tai - LaTeX bo qua
  lenh khong xac dinh nay va in thang noi dung 4 khoi {...} thanh doan
  van thuong, mat toan bo dinh dang bang Dung/Sai. Day la loi co san
  tu truoc, anh huong TOAN BO cau TF trong ca ngan hang de khi xuat
  PDF (khong phai loi moi phat sinh tu cac sua doi trong session nay).
  Trang lam bai online khong bi anh huong vi answer_parser_service.py
  trich dap an bang regex tren chinh van ban LaTeX (khong qua bien
  dich PDF nen khong bi anh huong boi loi \choiceTFn).
- Da xac nhan bang cach chay truc tiep L10_C1_TF_B_01() va doc lai
  data/config/ex_test.sty: grep "choiceTFn" trong file .sty tra ve 0
  ket qua dinh nghia that (chi xuat hien trong \choiceTFt/\choiceTFn
  o vai dong tham chieu chu khong phai \newcommand).
- Sua: math_type.py, bo hoan toan nhanh "\choiceTFn[N]", LUON dung
  "\choiceTFt" (macro duy nhat co that trong ex_test.sty). Khong sua
  ex_test.sty (file .sty phuc tap, khong ro co con noi nao khac dung
  \choiceTFn hay khong, sua o Python an toan hon vi la 1 diem duy nhat
  dung chung).
- Da test: chay lai L10_C1_TF_B_01(1, 4) sau khi sua, xac nhan output
  dung "\choiceTFt", khong con "\choiceTFn". answer_parser_service.py
  van trich dap an dung binh thuong (regex da ho tro san ca 2 dang tu
  truoc). CHUA test bien dich PDF that tren VPS (can giao vien tu build
  lai 1 de co cau TF va xem PDF).

2. Hien chi tiet dung/sai tung y (a/b/c/d) o trang ket qua lam bai
- Truoc: trang /lam-bai chi hien "Dung X/4 y - Y diem" cho cau TF,
  khong ro y nao dung y nao sai.
- Backend (app/routers/exam.py) tu truoc da tinh san "chi_tiet_tung_y"
  (dict {a:true/false, b:..., c:..., d:...}) nhung frontend chua dung
  toi.
- app/templates/chat/lam_bai.html, veKetQua(): them dong hien 4 the
  "✅/❌ y A/B/C/D" ngay duoi dong diem, mau xanh/do tuong ung, doc
  truc tiep tu chi_tiet_tung_y co san (khong can sua backend).
- Da test: node --check + Jinja2 render sach.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.28

Ngày

2026-08-18

Nội dung

1. Sua bug: nut "Lam bai truc tiep" bien mat khi quay lai chat qua ?cid=
- Giao vien bao: lam bai online xong, quay lai tab chat (link "Ve Chat
  AI" o /lam-bai co ?cid=...) thi khung "Lam bai truc tiep" duoi de vua
  tao khong con nua.
- Nguyen nhan: moHoiThoai() (ham nap lai lich su that tu Supabase) chi
  ve lai duoc caption + link tai file cho tin nhan loai "file", nhung
  KHONG tu dong hien lai nut Co/Khong lam bai (vi de_id khong duoc luu
  kem trong bang chat_history, chi luu o bang de_da_sinh).
- Sua: app/templates/chat/chat.html, moHoiThoai() - sau khi nap xong
  toan bo lich su, neu tin nhan CUOI CUNG la loai "file", goi them
  GET /api/exam/de-gan-nhat?conversation_id=... (endpoint moi, xem muc
  3) de lay lai de_id va hien lai dung khung "Lam bai truc tiep" nhu
  luc vua tao xong.

2. Sua bug NGHIEM TRONG khac phat hien cung luc: luong "xac nhan cau
   truc de" (nut Dong y tao de, Version 2.25) va form tao de nhanh
   (muc 4 duoi day) goi thang /api/exam/generate-pdf-auto tu trinh
   duyet, KHONG qua /chat, nen truoc day KHONG duoc luu vao chat_history
   - toan bo doan trao doi nay se "bien mat" khi quay lai hoi thoai.
- Them API moi: POST /api/chat/luu-de-truc-tiep (app/routers/chat.py) -
  luu lai 1 cap tin nhan user/assistant vao chat_history cho cac luong
  tao de KHONG qua CHV_Fun. Luu y: PDF trong cac luong nay la blob tai
  truc tiep tren trinh duyet (khong qua DOWNLOAD_DIR nhu luong n8n) nen
  KHONG co URL server on dinh de luu duong_dan_file - luu nhu tin nhan
  van ban thuong. Khi quay lai hoi thoai se thay lai NOI DUNG da trao
  doi (khong bi mat/bien mat nua), nhung khong co lai nut tai file cu
  (can tao lai neu muon file) - han che con lai, ghi nhan de lam sau
  neu can.
- Da noi lai xacNhanTaoDe() (luong Version 2.25) de goi API nay sau
  khi tao de thanh cong.

3. API moi: GET /api/exam/danh-sach-chuong?lop=N
- Tra ve danh sach chuong theo dung phan phoi chuong trinh that
  (data/ppct/toan{lop}.json - da co san tu truoc, chua tung dung toi),
  kem "co_du_cau": true/false dua vao viec da co Mapping that hay chua
  (data/mapping/toan{lop}/L{lop}_C{chuong_so}.json). Hien tai CHI Lop
  10 - Chuong 1 (Menh de va tap hop) la co_du_cau=true, tat ca lop/
  chuong con lai deu false (chua co ngan hang cau hoi).
- Dung cho form tao de nhanh (muc 4).

4. TINH NANG MOI: Form "Tao de nhanh" - chon lop/chuong thay vi go
   van ban tu do
- Boi canh: giao vien phan anh AI (chay tren model qwen/qwen3-8b, xem
  trao doi truoc do) hay hieu sai cac truong hop ro rang (vd "chuong 1"
  thanh "lop 1"), muon co huong khoa san lua chon cho hoc sinh thay vi
  phu thuoc hoan toan vao AI doan y.
- app/templates/chat/chat.html: them nut "Tao de nhanh" ngay duoi loi
  chao mo dau (moFormTaoDe()). Form gom: Lop (nut bam 10/11/12, mac
  dinh theo khoi cua hoc sinh dang nhap neu co), Loai kiem tra (dropdown:
  kiem tra thuong xuyen/15 phut/mieng - can chon Chuong; giua ky/cuoi
  ky/hoc ky - khong can chon Chuong, tu dong theo pham vi ky thi), So
  cau (khong bat buoc), Ghi chu them (khong bat buoc, vd ty le muc do).
- Logic xu ly khi bam "Tao de":
  + Neu KHONG dien So cau va Ghi chu: goi THANG /api/exam/generate-pdf-
    auto (khong qua CHV_Fun/n8n) - 0 token AI, khong the hieu sai vi
    lop/chuong/loai kiem tra da duoc khoa san tu form.
  + Neu CO dien So cau hoac Ghi chu (can AI hieu ngon ngu tu nhien,
    vd chia ty le muc do theo tung loai cau khong the ep may moc):
    van gui qua kenh chat binh thuong (sendMessage(), co qua CHV_Fun/
    GenerateExam_RequestParser nhu cu), NHUNG cau chu da "khoa" san
    lop/chuong/loai kiem tra ro rang trong cau (vd: "Tạo đề lớp 10,
    kiểm tra thường xuyên, chương 1 (Mệnh đề và tập hợp), 20 câu. 40%
    NB 30% TH 30% VD"), giam toi da rui ro AI doan nham cac gia tri co
    the xac dinh chac chan duoc.
- Da test: py_compile exam.py + chat.py sach, node --check + Jinja2
  render chat.html sach (2 truong hop user_khoi co gia tri va None -
  phat hien va sua luon 1 loi nho: Jinja2 "default()" khong ap dung
  cho gia tri None tuong minh, phai dung "or" thay the).
- CHUA test tren production (can build lai giao dien va thu bam nut).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.28

Ngày

2026-08-18

Nội dung

1. Sua bug: nut "Lam bai truc tiep" bien mat khi quay lai chat qua ?cid=
- Giao vien bao: lam bai online xong, quay lai tab chat (link "Ve Chat
  AI" o /lam-bai co ?cid=...) thi khung "Lam bai truc tiep" duoi de vua
  tao khong con nua.
- Nguyen nhan: moHoiThoai() (ham nap lai lich su that tu Supabase) chi
  ve lai duoc caption + link tai file cho tin nhan loai "file", nhung
  KHONG tu dong hien lai nut Co/Khong lam bai (vi de_id khong duoc luu
  kem trong bang chat_history, chi luu o bang de_da_sinh).
- Sua: app/templates/chat/chat.html, moHoiThoai() - sau khi nap xong
  toan bo lich su, neu tin nhan CUOI CUNG la loai "file", goi them
  GET /api/exam/de-gan-nhat?conversation_id=... (endpoint moi, xem muc
  3) de lay lai de_id va hien lai dung khung "Lam bai truc tiep" nhu
  luc vua tao xong.

2. Sua bug NGHIEM TRONG khac phat hien cung luc: luong "xac nhan cau
   truc de" (nut Dong y tao de, Version 2.25) va form tao de nhanh
   (muc 4 duoi day) goi thang /api/exam/generate-pdf-auto tu trinh
   duyet, KHONG qua /chat, nen truoc day KHONG duoc luu vao chat_history
   - toan bo doan trao doi nay se "bien mat" khi quay lai hoi thoai.
- Them API moi: POST /api/chat/luu-de-truc-tiep (app/routers/chat.py) -
  luu lai 1 cap tin nhan user/assistant vao chat_history cho cac luong
  tao de KHONG qua CHV_Fun. Luu y: PDF trong cac luong nay la blob tai
  truc tiep tren trinh duyet (khong qua DOWNLOAD_DIR nhu luong n8n) nen
  KHONG co URL server on dinh de luu duong_dan_file - luu nhu tin nhan
  van ban thuong. Khi quay lai hoi thoai se thay lai NOI DUNG da trao
  doi (khong bi mat/bien mat nua), nhung khong co lai nut tai file cu
  (can tao lai neu muon file) - han che con lai, ghi nhan de lam sau
  neu can.
- Da noi lai xacNhanTaoDe() (luong Version 2.25) de goi API nay sau
  khi tao de thanh cong.

3. API moi: GET /api/exam/danh-sach-chuong?lop=N
- Tra ve danh sach chuong theo dung phan phoi chuong trinh that
  (data/ppct/toan{lop}.json - da co san tu truoc, chua tung dung toi),
  kem "co_du_cau": true/false dua vao viec da co Mapping that hay chua
  (data/mapping/toan{lop}/L{lop}_C{chuong_so}.json). Hien tai CHI Lop
  10 - Chuong 1 (Menh de va tap hop) la co_du_cau=true, tat ca lop/
  chuong con lai deu false (chua co ngan hang cau hoi).
- Dung cho form tao de nhanh (muc 4).

4. TINH NANG MOI: Form "Tao de nhanh" - chon lop/chuong thay vi go
   van ban tu do
- Boi canh: giao vien phan anh AI (chay tren model qwen/qwen3-8b, xem
  trao doi truoc do) hay hieu sai cac truong hop ro rang (vd "chuong 1"
  thanh "lop 1"), muon co huong khoa san lua chon cho hoc sinh thay vi
  phu thuoc hoan toan vao AI doan y.
- app/templates/chat/chat.html: them nut "Tao de nhanh" ngay duoi loi
  chao mo dau (moFormTaoDe()). Form gom: Lop (nut bam 10/11/12, mac
  dinh theo khoi cua hoc sinh dang nhap neu co), Loai kiem tra (dropdown:
  kiem tra thuong xuyen/15 phut/mieng - can chon Chuong; giua ky/cuoi
  ky/hoc ky - khong can chon Chuong, tu dong theo pham vi ky thi), So
  cau (khong bat buoc), Ghi chu them (khong bat buoc, vd ty le muc do).
- Logic xu ly khi bam "Tao de":
  + Neu KHONG dien So cau va Ghi chu: goi THANG /api/exam/generate-pdf-
    auto (khong qua CHV_Fun/n8n) - 0 token AI, khong the hieu sai vi
    lop/chuong/loai kiem tra da duoc khoa san tu form.
  + Neu CO dien So cau hoac Ghi chu (can AI hieu ngon ngu tu nhien,
    vd chia ty le muc do theo tung loai cau khong the ep may moc):
    van gui qua kenh chat binh thuong (sendMessage(), co qua CHV_Fun/
    GenerateExam_RequestParser nhu cu), NHUNG cau chu da "khoa" san
    lop/chuong/loai kiem tra ro rang trong cau (vd: "Tạo đề lớp 10,
    kiểm tra thường xuyên, chương 1 (Mệnh đề và tập hợp), 20 câu. 40%
    NB 30% TH 30% VD"), giam toi da rui ro AI doan nham cac gia tri co
    the xac dinh chac chan duoc.
- Da test: py_compile exam.py + chat.py sach, node --check + Jinja2
  render chat.html sach (2 truong hop user_khoi co gia tri va None -
  phat hien va sua luon 1 loi nho: Jinja2 "default()" khong ap dung
  cho gia tri None tuong minh, phai dung "or" thay the).
- CHUA test tren production (can build lai giao dien va thu bam nut).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.29

Ngày

2026-08-18

Nội dung

1. Sua thiet ke: hoi lai LOP khi hoc sinh khong noi ro, thay vi tu
   mac dinh lop = 10
- Giao vien phat hien: hoc sinh nhan "tao de chuong 1" (khong noi lop
  may), he thong ra de NGAY cho lop 10 ma khong hoi lai gi ca - day la
  hanh vi CHU DINH tu ban truoc (Version 2.26, de tranh loi AI nham
  "chuong 1" thanh "lop 1"), nhung xet ve trai nghiem la sai: hoc sinh
  lop 11/12 go "tao de chuong 1" se bi ra nham de lop 10 ma khong duoc
  bao truoc.
- Sua prompt n8n GenerateExam_RequestParser (v3): khi khong xac dinh
  duoc lop tu cau noi (khong co chu "lop" di kem so), AI PHAI de
  "lop": null va hoi lai HOC SINH LOP MAY truoc, CHUA voi tinh cau truc
  de/ty le muc do (hoi tung thu mot, tranh don dap). Neu hoc sinh da
  tra loi lop o tin nhan truoc do trong cung hoi thoai (dung Memory
  node co san), khong hoi lai nua.
- app/templates/chat/chat.html, sendMessage(): tach nhanh xu ly khi
  data.data.type === "xac_nhan_de": neu data.data.lop la null/rong,
  CHI hien cau hoi bang van ban thuong (KHONG co nut "Dong y" - vi hoc
  sinh chua tra loi lop thi chua co gi de dong y ca), hoc sinh go lai
  lop se di qua kenh chat binh thuong nhu cu. Neu lop da ro, giu
  nguyen luong nut "Dong y tao de" nhu Version 2.25.
- File dinh kem: GenerateExam_RequestParser_SystemMessage_v3.txt (dan
  toan bo vao System Message cua node GenerateExam_RequestParser
  trong n8n, thay the ban v2 cu).

2. Luu y quan trong: giao vien test tren production cho thay luong
   "hoi xac nhan cau truc de" (Version 2.25) hoan toan CHUA hoat dong
   - bam gui la ra file PDF ngay, khong hoi gi ca. Nhieu kha nang 3
   buoc thu cong ben n8n (dan prompt GenerateExam_RequestParser, sua
   code Ghep_Tham_So, noi node IF Can_Xac_Nhan_Cau_Truc - xem file
   n8n_HUONG_DAN_va_noi_dung.txt da giao truoc do) CHUA duoc ap dung
   hoac chua ap dung dung. Version 2.29 nay dong thoi la co hoi de lam
   lai dung 3 buoc do (thay prompt bang ban v3 moi nay), giao vien can
   kiem tra lai tung buoc truoc khi test lai.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.29

Ngày

2026-08-18

Nội dung

1. Sua thiet ke: hoi lai LOP khi hoc sinh khong noi ro, thay vi tu
   mac dinh lop = 10
- Giao vien phat hien: hoc sinh nhan "tao de chuong 1" (khong noi lop
  may), he thong ra de NGAY cho lop 10 ma khong hoi lai gi ca - day la
  hanh vi CHU DINH tu ban truoc (Version 2.26, de tranh loi AI nham
  "chuong 1" thanh "lop 1"), nhung xet ve trai nghiem la sai: hoc sinh
  lop 11/12 go "tao de chuong 1" se bi ra nham de lop 10 ma khong duoc
  bao truoc.
- Sua prompt n8n GenerateExam_RequestParser (v3): khi khong xac dinh
  duoc lop tu cau noi (khong co chu "lop" di kem so), AI PHAI de
  "lop": null va hoi lai HOC SINH LOP MAY truoc, CHUA voi tinh cau truc
  de/ty le muc do (hoi tung thu mot, tranh don dap). Neu hoc sinh da
  tra loi lop o tin nhan truoc do trong cung hoi thoai (dung Memory
  node co san), khong hoi lai nua.
- app/templates/chat/chat.html, sendMessage(): tach nhanh xu ly khi
  data.data.type === "xac_nhan_de": neu data.data.lop la null/rong,
  CHI hien cau hoi bang van ban thuong (KHONG co nut "Dong y" - vi hoc
  sinh chua tra loi lop thi chua co gi de dong y ca), hoc sinh go lai
  lop se di qua kenh chat binh thuong nhu cu. Neu lop da ro, giu
  nguyen luong nut "Dong y tao de" nhu Version 2.25.
- File dinh kem: GenerateExam_RequestParser_SystemMessage_v3.txt (dan
  toan bo vao System Message cua node GenerateExam_RequestParser
  trong n8n, thay the ban v2 cu).

2. Luu y quan trong: giao vien test tren production cho thay luong
   "hoi xac nhan cau truc de" (Version 2.25) hoan toan CHUA hoat dong
   - bam gui la ra file PDF ngay, khong hoi gi ca. Nhieu kha nang 3
   buoc thu cong ben n8n (dan prompt GenerateExam_RequestParser, sua
   code Ghep_Tham_So, noi node IF Can_Xac_Nhan_Cau_Truc - xem file
   n8n_HUONG_DAN_va_noi_dung.txt da giao truoc do) CHUA duoc ap dung
   hoac chua ap dung dung. Version 2.29 nay dong thoi la co hoi de lam
   lai dung 3 buoc do (thay prompt bang ban v3 moi nay), giao vien can
   kiem tra lai tung buoc truoc khi test lai.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.30

Ngày

2026-08-22

Nội dung

Cai thien UX form "Tao de nhanh" theo phan hoi truc tiep cua giao vien
khi test tren production.

1. Gop 3 loai kiem tra he so 1 (kiem tra mieng / kiem tra 15 phut /
   kiem tra thuong xuyen) thanh 1 lua chon duy nhat trong DROPDOWN cua
   form ("Kiem tra thuong xuyen (mieng / 15 phut / thuong xuyen)") -
   ve ban chat ca 3 deu ra de theo 1 chuong cu the, khong can tach 3
   dong rieng gay roi mat cho hoc sinh chon. Kenh chat go van ban tu do
   van hieu duoc ca 3 cach noi rieng le nhu cu (khong doi prompt AI).
2. Them ghi chu ngay duoi dropdown "Loai kiem tra": "Kiem tra thuong
   xuyen: ra de theo 1 chuong cu the (chon Chuong ben duoi). Giua ky /
   Cuoi ky: ra de theo pham vi rong hon, khong chon rieng 1 chuong." -
   giup hoc sinh hieu ngay tai sao co luc form hien o Chuong, co luc
   khong.
3. Sua loi UX nghiem trong: truoc day khi tao de qua form/nut "Dong y
   tao de" bi loi (vi du sai du lieu, thieu ngan hang cau hoi...), toan
   bo form/khung bi XOA TRANG chi con lai 1 dong "Co loi khi tao de,
   ban thu lai nhe" - khong co each nao thu lai, khong biet ly do that.
   Sua: hien THANG noi dung loi that (doc tu field "detail" trong JSON
   loi cua backend) va them nut "Mo lai form, thu lan nua" / "Nhan lai
   yeu cau khac" de thao tac tiep duoc ngay, khong phai bam "+ Chat
   moi" lam lai tu dau.

===============================================================================

Version 2.31

Ngày

2026-08-22

Nội dung

Sua bug: form "Tao de nhanh" va nut "Dong y tao de" bao loi cung
"Loi chon cau hoi: <ID> (SA): khong co Generator nao khop trong
Mapping" thay vi ra de kem canh bao "THIEU" nhu ban PDF sinh qua kenh
chat binh thuong.

Nguyen nhan: 2 luong nay goi THANG toi /api/exam/generate-pdf-auto tu
trinh duyet (khong qua n8n/Ghep_Tham_So), va quen khong bat co
"cho_phep_thieu: true" trong payload gui len - trong khi luong chat
binh thuong qua n8n LUON bat co nay (xac nhan qua man hinh n8n
Goi_API_Sinh_De). Pydantic model GenerateExamAutoRequest mac dinh
cho_phep_thieu=False (che do nghiem ngat), nen thieu du lieu la bao
loi cung 400 thay vi chen "THIEU" nhu thiet ke goc.

Sua: them "cho_phep_thieu: true" vao ca 2 noi goi
/api/exam/generate-pdf-auto trong app/templates/chat/chat.html
(xacNhanTaoDe() va submitFormTaoDe()) - dung hanh vi voi luong chat
qua n8n. Giao vien xac nhan day la hanh vi mong muon: "cu ra de, cai
nao chua co thi hien thong bao thieu la duoc, nhu trong file pdf".

===============================================================================

Version 2.32

Ngày

2026-08-22

Nội dung

1. Sua bug NGHIEM TRONG: route GET /chat thieu "user_id" trong context
   Jinja2
- Phat hien qua qua trinh debug: hang loat trieu chung tuong nhu khong
  lien quan (form tao de nhanh khong hien nut "Lam bai truc tiep" sau
  khi tao xong, "cho toi loi giai" bao loi "AI chua xu ly duoc yeu cau
  nay", GET /api/exam/de-gan-nhat luon tra ve 404) deu bat nguon TU
  CUNG 1 CHO: route GET /chat (ham chat() trong app/routers/chat.py)
  dung templates.TemplateResponse voi context CHUA CO field "user_id"
  (cac route khac nhu /lam-bai/{de_id} da co san field nay, rieng
  route chinh /chat thi thieu). Frontend doc
  const CURRENT_USER_ID = "{{ user_id | default('') }}"; - vi context
  thieu key nay nen Jinja2 default() kich hoat, CURRENT_USER_ID LUON
  la chuoi rong.
- He qua day chuyen: form tao de nhanh/nut "Dong y tao de" goi
  /api/exam/generate-pdf-auto voi user_id="" (rong) -> backend kiem
  tra "if payload.user_id and payload.conversation_id" luon FALSE voi
  chuoi rong -> BO QUA hoan toan buoc luu de vao bang de_da_sinh (va
  file vao file_de) -> moi truy van sau do (de-gan-nhat de hien nut
  "Lam bai truc tiep", export-loigiai de xuat dap an...) deu khong tim
  thay de, bao loi hoac im lang khong hien gi.
- Cach debug: xac nhan tung lop mot bang du lieu that (khong doan) -
  test tu request that qua Network/backend log, phat hien
  /api/exam/de-gan-nhat luon tra ve 404 du backend da tra 200 OK cho
  generate-pdf-auto; roi dung Safari "View Page Source" doc dung dong
  "const CURRENT_USER_ID = "";" trong HTML that su duoc server render
  ra - xac nhan chinh xac gia tri rong ngay tai nguon, khong con nghi
  ngo o dau khac.
- Sua: them "user_id": user.id, vao context cua ham chat() trong
  app/routers/chat.py (1 dong).

2. Tinh nang moi: URL tai file DE on dinh theo de_id, khong con dung
   blob tam thoi
- Boi canh: xacNhanTaoDe()/submitFormTaoDe() (luong tao de KHONG qua
  n8n) truoc day dung URL.createObjectURL(blob) de tao link tai file -
  link nay CHI song trong phien trinh duyet hien tai, mat ngay khi tai
  lai trang. Giao vien phan anh: "quay ve chat thi no bien mat het cac
  phan chat truoc do... nut tao de thi se chuyen thanh cau chat cua
  ban theo lua chon nguoi dung" - muon de tao qua 2 luong nay hien lai
  y het de tao qua chat thuong khi quay lai hoi thoai.
- API moi: GET /api/exam/tai-de/{de_id} (app/routers/exam.py) - tra ve
  truc tiep file PDF da luu (doc duong dan tu bang file_de qua
  history_service.lay_de_theo_id(de_id), ham nay da co san tu truoc,
  chi la chua tung dung toi). URL dang "/api/exam/tai-de/<uuid>", song
  vinh vien (den khi file bi xoa sau 10 ngay theo co che don dep co
  san), khong phu thuoc phien trinh duyet.
- xacNhanTaoDe() va submitFormTaoDe(): sau khi lay duoc de_id (qua
  /api/exam/de-gan-nhat), dung URL on dinh /api/exam/tai-de/{de_id}
  thay cho blob. Chi fall back ve blob (khong song lai duoc sau
  reload) trong truong hop hiem gap khong lay duoc de_id.
- Model LuuDeTrucTiepRequest (app/routers/chat.py) them field tuy chon
  "file_url". Khi co gia tri nay, endpoint POST /api/chat/luu-de-truc-
  tiep luu tin nhan AI vao chat_history voi loai_phan_hoi="file",
  duong_dan_file=file_url - GIONG HET dinh dang tin nhan cua luong
  chat binh thuong qua n8n. Nho vay ham moHoiThoai() (da co san tu
  Version 2.28, xu ly loai_phan_hoi === "file") tu dong hien lai dung
  link tai file + nut "Lam bai truc tiep" khi quay lai hoi thoai, y
  het luong chat thuong - khong can sua them gi o moHoiThoai().
- xacNhanTaoDe(): sua cau user_message luu vao lich su tu cau chung
  chung "Dong y, tao de theo de xuat." thanh cau co day du thong tin
  da chon: "Dong y, tao de: lop <X>, <loai kiem tra>, chuong <Y>." -
  dung yeu cau cua giao vien "nut tao de thi se chuyen thanh cau chat
  cua ban theo lua chon nguoi dung".

Nguoi thuc hien (ca 3 Version 2.30, 2.31, 2.32)

Mai Ha Lan (cung Claude)


===============================================================================

Version 2.33

Ngày

2026-08-23

Nội dung

Sua UX: nut "Bat dau lam bai" (hien sau khi hoc sinh bam "Co, lam
luon!" trong khung hoi lam bai truc tiep) dang mo trang /lam-bai
trong TAB/CUA SO MOI (target="_blank"), khien hoc sinh bam "Ve Chat
AI" tu trang lam bai chi dong duoc tab do, con tab chat ban dau van
mo song song rieng - giao vien phan anh gay roi ("toi muon chi 1 cua
so thoi, tranh roi loan").

Sua: bo target="_blank" (va rel="noopener" di kem) o the <a> nay
trong app/templates/chat/chat.html (ham chonLamBai()) - gio bam vao
se dieu huong ngay trong cung 1 tab/cua so, "Ve Chat AI" quay lai
dung cho cu, khong con tab thua.

===============================================================================

Version 2.34

Ngày

2026-08-23

Nội dung

Tinh nang moi: sau khi hoc sinh nop bai lam truc tiep tren web, DE +
LOI GIAI (PDF) + DIEM cua lan lam bai do duoc tu dong dang len "Bai
tap tren lop" (courseWorkMaterial) cua Google Classroom, RIENG cho
dung hoc sinh vua lam bai (khong ban nao khac trong lop thay duoc),
tu dong xoa sau 10 ngay - dung yeu cau cua giao vien va khop voi thoi
gian da thong bao truoc cho hoc sinh.

1. app/services/classroom_service.py:
   - Them 2 scope OAuth moi vao SCOPES: classroom.coursework.students
     (tao/xoa courseWorkMaterial) va drive.file (tai file len Drive
     cua giao vien, app chi thay duoc file no tu tao ra). QUAN TRONG:
     doi scope nghia la phai vao lai Google Cloud Console > Data
     Access them 2 scope nay, ROI lam lai /gv/classroom/connect de
     xin refresh_token moi (refresh_token cu chi mang quyen cu, khong
     tu nhien co them quyen moi).
   - Ham moi _tai_len_drive(): upload 1 file PDF len Drive qua Drive
     API v3 (multipart), tra ve file id.
   - Ham moi _tao_coursework_material(): tao 1 courseWorkMaterial tren
     dung course_id, dung assigneeMode=INDIVIDUAL_STUDENTS +
     individualStudentsOptions.studentIds=[email hoc sinh] de CHI hoc
     sinh do thay duoc bai dang (Classroom API chap nhan email lam
     studentId, khong can tra numeric user id rieng).
   - Ham cap cao moi dang_ket_qua_len_classroom(de_id, student_email,
     khoi, lop, diem_html, diem_so): tra course_id qua MA_LOP_CLASSROOM,
     doc duong dan file "de"/"loigiai" da luu san qua
     history_service.lay_de_theo_id(), upload len Drive, tao
     courseWorkMaterial voi tieu de dat theo ngay gio + ghi chu
     "Đề, bài giải, điểm", mo ta la diem so + ban tom tat dung/sai (doi
     tu HTML sang text qua _html_sang_text()). Ghi 1 dong vao bang moi
     classroom_coursework de biet duong ma don dep sau nay. KHONG raise
     loi ra ngoai o bat ky buoc nao - luon tra ve {"success": bool,
     "message": str}, vi day la tien ich them, khong duoc phep chan
     hoc sinh xem ket qua bai lam du Classroom co loi gi.

2. app/routers/chat.py: them POST /api/chat/dang-classroom - doc
   user hien tai qua get_current_user(), lay khoi/lop qua
   supabase_service.lay_lop_hoc_sinh(), goi
   classroom_service.dang_ket_qua_len_classroom().

3. app/templates/chat/lam_bai.html: ham moi dangKetQuaLenClassroom(),
   goi ngay sau luuKetQuaVaoChat() trong nopBai() - chay am tham
   (try/catch, khong alert/khong chan giao dien) ngay khi hoc sinh
   nop bai xong.

4. Bang moi public.classroom_coursework (Supabase) - luu de_id,
   student_email, course_id, coursework_id, drive_file_ids (mang id
   file Drive), created_at. Xem huong dan tao bang trong ghi chu trien
   khai kem theo diff nay.

5. scripts/cleanup_classroom_coursework.py (moi, hoan thanh Task #12
   con treo tu truoc): doc cac dong classroom_coursework cu hon 10
   ngay, xoa courseWorkMaterial tren Classroom + tung file tren Drive,
   roi xoa dong tuong ung trong Supabase. Cung mau voi
   cleanup_chat_history.py/cleanup_old_files.py da co - chay hang
   ngay qua cron tren VPS (khuyen nghi cung 3h sang).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.35

Ngày

2026-09-04

Nội dung

Thang diem 10 theo quy dinh cua giao vien, thay cho cach chia deu 10
diem cho tong so cau nhu truoc.

Truoc day: diem_moi_cau = 10 / tong_so_cau - moi cau bang diem nhau du
la trac nghiem 1 lua chon hay tu luan. Gio chia theo PHAN:

   Trac nghiem nhieu lua chon (MC): 3 diem
   Dung/Sai (TF):                   2 diem
   Tra loi ngan (SA):               2 diem
   Tu luan (TL):                    3 diem
   -----------------------------------------
   Tong:                            10 diem

Diem cua moi phan chia DEU cho so cau co that trong de o phan do; cau
TF chia tiep DEU cho 4 y. Vi du de HeSo2 (12 MC, 2 TF, 3 SA, 3 TL):
moi cau MC 0.25d, moi cau TF 1d (moi y 0.25d), moi cau SA 0.67d, moi
cau TL 1d.

Trong so la CO DINH: de thieu phan nao thi diem toi da giam dung phan
do, KHONG chia lai cho cac phan con lai (de chi co MC + TF thi toi da
5 diem). Quyet dinh cua giao vien.

1. data/config/diem_rules.json (MOI): noi khai bao trong so, ten phan,
   so y moi cau TF, so chu so lam tron. Doi thang diem chi can sua file
   nay, khong dong vao code.

2. app/services/diem_service.py (MOI):
   - tinh_thang_diem(danh_sach_dap_an): dem so cau tung phan roi tra ve
     diem moi cau / moi y, diem_toi_da_tong (chi tinh cac phan CO trong
     de) va diem_toi_da_tu_dong (MC + TF + SA).
   - loai_cau_chuan(cau): nhan ra ca cau TF dang bi answer_parser_service
     luu nham thanh loai_cau="TL" (phan biet qua "_TF_" trong
     generator_id) - neu khong se tinh nham cau TF vao diem phan Tu luan.
     Dung CHUNG cho ca /grade va /grade-photo de hai ben khong lech nhau.
   - diem_cau_tf(thang, so_y_dung): tra ve (diem_goc, diem_lam_tron).
   - so_dep(): bo duoi .0 khi hien thi (3.0d -> 3d).

3. app/routers/exam.py (POST /api/exam/grade):
   - Bo diem_moi_cau = 10/tong_so_cau, dung diem_service.
   - Cong don bang so THUC chua lam tron, chi lam tron o buoc cuoi -
     tranh lech kieu 3 cau SA x 0.67 = 2.01 diem (test da phu).
   - diem_tren_10_tam_tinh gio la diem CONG DON tren thang 10 chung
     (khong con chuan hoa lai ve 10 tren tap con da cham).
   - Response them: thang_diem, diem_toi_da_tu_dong, diem_toi_da_tong,
     diem_phan_tu_luan, mo_ta_thang_diem.
   - Cau TL: trang_thai doi tu "can_cham_tay" thanh "dang_xay_dung",
     nhan xet "Phần tự luận (3đ) — đang xây dựng." theo dung yeu cau
     cua giao vien (phan cham tu luan qua anh dang lam do).

4. app/services/grade_photo_service.py: dung chung thang diem tren; bo
   buoc chuan hoa lai ve 10 (tong_diem_dat / tong_toi_da * 10) vi
   diem_toi_da tung cau da nam san tren thang 10 chung.

5. app/templates/chat/lam_bai.html:
   - Diem hien thi la X / diem_toi_da_tu_dong (vd 5.33/7) chu khong
     con /10, kem 1 dong mo ta thang diem va ghi chu "Phần tự luận
     (3đ): đang xây dựng" - de hoc sinh khong hieu nham la bi mat diem.
   - Cau TF hien them "moi y 0.25d".
   - gopKetQua() chi con CONG DON, khong chuan hoa lai ve 10.

6. app/routers/chat.py + app/services/classroom_service.py: bai dang len
   Classroom ghi "Điểm: 5.33/7" thay vi luon "/10" (them truong
   diem_toi_da, mac dinh 10 neu thieu - tuong thich nguoc).

7. tests/test_diem_service.py (MOI): 5 test - de du 4 phan (tong 10, tu
   dong 7), de thieu phan (giu trong so, toi da 5), cau TF chia 4 y,
   de HeSo1, va test lam tron (lam dung het phan trac nghiem phai ra
   dung 7.0).

8. data/config/exam_rules.json: HeSo2_HeSo3 tra_loi_ngan 3 -> 4 cau
   (theo ma tran moi cua giao vien). LUU Y: diem_service KHONG gia dinh
   so cau cua bat ky phan nao - no DEM so cau co that trong de roi moi
   chia diem, nen sau nay sua ma tran trong exam_rules.json thi diem tu
   dong chia lai, khong phai dong vao code diem. Vi du phan Tra loi ngan
   luon 2 diem: 2 cau -> 1d/cau, 4 cau -> 0.5d/cau.

HAN CHE DA BIET (giu nguyen tu Version 2.8): answer_parser_service chua
trich duoc dap an dung cua cau TF (\choiceTFn/\choiceTFt) khi sinh de,
nen o nhanh cham bang ANH cau TF van phai cham tay. Nhanh lam bai truc
tiep tren web khong bi anh huong (dap an TF duoc luu du).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.36

Ngày

2026-09-04

Nội dung

(1) Xac minh lai "HAN CHE DA BIET" ve cau Dung/Sai o Version 2.8 - GHI
CHU DO DA LOI THOI, khong con bug. (2) Sua 1 bug that trong ngan hang
de tim ra khi kiem tra. (3) Tam an o tai anh cham tu luan, thay bang
thong bao "dang xay dung".

--- (1) Cau Dung/Sai: parser DA doc dung tu Version 2.27 ---

Ghi chu tu Version 2.8 noi answer_parser_service chua trich duoc dap an
cau TF (\choiceTFn/\choiceTFt) nen cau TF bi luu nham loai_cau="TL".
Kiem tra lai 2026-09-04: KHONG con dung. Nguyen nhan goc la generator
sinh \choiceTFn[N] - macro khong ton tai trong data/config/ex_test.sty;
Version 2.27 da doi math_type.py sang \choiceTFt (macro co that) va
answer_parser_service.trich_dap_an_tf() doc duoc dinh dang nay. Tu do
cau TF duoc luu dung loai_cau="TF" kem dap_an_dung {a,b,c,d}, va
POST /api/exam/grade van cham TF binh thuong tu luc do den nay.

Da cap nhat lai cac cho ghi chu sai: docstring dau
app/services/grade_photo_service.py, docstring loai_cau_chuan() trong
app/services/diem_service.py, docs/05_API_SPECIFICATION.md,
docs/15_DEVELOPMENT_ROADMAP.md.

loai_cau_chuan() trong diem_service KHONG bo di, nhung doi vai tro:
tu "va bug parser" thanh "luoi an toan cho file *_dapan.json CU sinh
truoc Version 2.27". File dap an chi song 1 ngay (cleanup_old_files.py)
nen co the bo ham nay sau vai thang.

Rieng nhanh cham bang ANH: cau TF van tra ve can_cham_tay, nhung LY DO
gio la chua viet phan so khop ket qua DocPhieuTraLoi voi dap_an_dung -
lam cung luc voi viec hoan thien cham tu luan bang anh.

--- (2) tests/test_answer_parser_bank.py (MOI) ---

Chay TOAN BO generator trong data/python_bank/toan*/L*.py mot lan, dua
latex_block ra trich_dap_an() roi doi chieu loai cau parser doc duoc voi
loai cau ghi trong TEN HAM (_MC_/_TF_/_SA_/_TL_), kiem them: cau TF phai
du 4 y, cau MC/SA phai co dap an dung, generator khong duoc tra ve rong.

Ket qua tren L10_C1.py: 46/46 ham dat (37 MC, 2 TF, 2 SA, 5 TL).

Luu y khi goi generator trong test: chi truyen socau=1, GIU NGUYEN gia
tri mac dinh cua tham so con lai. Vai ham SA co dang=2 lam mac dinh
(vd L10_C1_B1_VD014_SA_A_01, L10_C1_B2_NB017_SA_C) - truyen dang=1 se
sinh ra dang MC va lam test bao sai oan.

BUG THAT DA BAT DUOC:
data/python_bank/toan10/L10_C1.py dong 6250, ham
L10_C1_B2_NB017_MC_B_02 ket thuc bang `return` thay vi `return cauTN`
-> generator tra ve None -> de sinh ra 1 cau RONG, va cau rong do bi
trich_dap_an doc thanh loai_cau="TL". Voi thang diem moi (Version 2.35)
loi nay con nguy hiem hon truoc: cau rong se an vao phan Tu luan 3 diem.
Da sua thanh `return cauTN` (giong ham anh em MC_B_01 o dong 5921).

--- (3) Tam dung nhanh cham tu luan bang anh ---

Theo yeu cau cua giao vien: phan cham tu luan bang anh (CHV_Grader) con
dang xay dung, khong nen de hoc sinh chup anh roi cho vo ich.

- app/templates/chat/lam_bai.html: o tai anh (#anh-tuluan) duoc boc
  trong `if (false) { ... } else { ... }`, nhanh else hien khung mau
  vang: "Chức năng chấm tự luận đang được xây dựng - em chưa cần chụp
  ảnh bài làm gửi lên... Bấm Nộp bài để được chấm ngay phần trắc
  nghiệm (7 điểm)". Lam xong CHV_Grader thi doi `if (false)` thanh
  `if (true)` la khoi phuc.
- Luong goi /grade-photo trong nopBai() GIU NGUYEN, tu dong bo qua khi
  khong tim thay #anh-tuluan - khong phai sua gi them khi bat lai.
- app/routers/exam.py (GET /quiz/{de_id}): ghi chu o tung cau tu luan
  doi thanh "Câu tự luận — em làm ra giấy và nộp cho thầy/cô. Chức năng
  chấm tự luận tự động đang được xây dựng."

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.37

Ngày

2026-09-06

Nội dung

Hoc sinh lam xong 1 de, muon lam tiep de nua thi go "cho toi them de
nua" trong chat -> CHV_Fun phan loai nham thanh reject_out_of_scope va
tra loi "he thong minh chi ho tro tao de, xem hoc luc hoac tai loi giai
thoi nha" (buon cuoi vi day DUNG la yeu cau tao de). Nguyen nhan:
app/routers/chat.py::_goi_n8n() chi gui `message` + `user_id` +
`conversation_id`, KHONG gui lich su hoi thoai - CHV_Fun nhan mot cau
cut lui khong co ngu canh, khong biet truoc do da tao de gi.

Cach xu ly (theo dung nguyen tac doc 00 "Uu tien Code hon AI"): khong
sua prompt CHV_Fun, ma them mot duong di KHONG QUA AI.

1. POST /api/exam/lam-de-khac (MOI) - body {de_id, user_id?,
   conversation_id?}:
   - Doc lai chinh tham so cua de cu trong bang de_da_sinh (lop, role,
     loai_he_so, ki_thi, pham_vi_chuong, blueprint).
   - Goi thang generate_exam_pdf_auto voi dung bo tham so do -> de moi
     CUNG cau truc, chi khac so lieu (generator random lai).
   - Luu de moi + 4 file (de/tex/loigiai/dapan_json) y het duong di cua
     /generate-pdf-auto. Bat buoc phai co dapan_json thi trang lam bai
     va POST /grade moi cham duoc.
   - Tra ve {de_id, url_lam_bai, so_cau_da_sinh}.

2. /generate-pdf-auto: gio luu them vao cot blueprint cua de_da_sinh
   {tieu_de, cau_truc_tu_hoc_sinh, socau_ma_de}. Truoc day cot nay luon
   la null nen neu nguoi dung tu quy dinh cau truc (vd "20 cau MC, 70%
   NB") thi tai tao se roi ve cau truc mac dinh trong exam_rules.json.

3. history_service.luu_de_da_sinh(): neu insert that bai vi cot
   blueprint (vd cot dang la text chu khong phai jsonb), thu lai lan 2
   voi blueprint=None thay vi bo luon. Mat de nghia la mat duong dan
   file dap an -> hoc sinh khong cham bai duoc, khong danh doi duoc.

4. app/templates/chat/lam_bai.html: cuoi trang ket qua them nut
   "🔄 Làm đề khác cùng cấu trúc" -> goi endpoint tren roi chuyen thang
   sang /lam-bai/{de_id_moi}, giu nguyen ?cid= de nut "Ve Chat AI" va
   viec luu ket qua vao chat van chay nhu cu. Loi (neu co) hien ngay
   duoi nut, khong dung alert.

CON TON DONG: neu hoc sinh van go "cho toi them de nua" trong KHUNG
CHAT (khong phai o trang ket qua) thi van bi CHV_Fun tra loi nham nhu
cu. Hai cach xu ly sau nay, chua lam:
  a) Nhan dien cau dan o backend truoc khi goi n8n (regex "them de",
     "de khac", "lam bai tiep"...) + da co de trong hoi thoai -> goi
     thang /api/exam/lam-de-khac.
  b) Gui kem lich su hoi thoai sang n8n va sua prompt CHV_Fun (ton
     token moi luot, va van co the doan sai).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.38

Ngày

2026-09-12

Nội dung

Thuc hien dung quy dinh phan bo de cua giao vien. Truoc day quy dinh nay
DA GHI trong docs/08 (muc CN_BuildBlueprint, y 2) nhung CHUA duoc viet
vao code - khong phai bi xoa, xem git log cua
app/services/exam_blueprint_service.py (chi co 3 commit e776e31 /
8fc3950 / 2041215, khong commit nao dong vao y 2 nay).

QUY DINH (giao vien chot 2026-09-12):
1. Cau Dung/Sai luon tinh la 4 cau: 1 NB + 1 TH + 1 VD + 1 VDC.
2. Chon bai cho cau Dung/Sai TRUOC TIEN, roi TRU 1 cau o moi muc ngay
   tai bai do truoc khi chia cac phan con lai.
3. Chia so cau ve tung bai theo TI LE SO TIET cua bai (truoc day chia
   deu theo SO BAI).
4. VD:VDC giu nguyen theo bang exam_rules.json, khong ep cung 2:1.
5. De dat ti le VDC = 0 thi y VDC cua cau Dung/Sai khong tru di dau ca
   (kep o 0), cau Dung/Sai van giu du 4 y.

1. app/services/exam_scope_service.py:
   - dem_so_tiet(): doc truong "tiet" cua PPCT ("23, 25-26" -> 3 tiet).
     Bai thieu du lieu tinh 1 tiet de khong bi loai khoi pham vi.
   - load_scope_heso1()/load_scope_heso23() tra them so_tiet_theo_bai.
     De o day vi CN_BuildBlueprint KHONG duoc doc PPCT (doc 08).

2. app/services/exam_blueprint_service.py:
   - _chia_theo_so_tiet(): chia so cau ve tung BAI theo ti le so tiet,
     lam tron xuong, phan du RAI LAN LUOT cho bai nhieu tiet nhat truoc
     (khong don het vao 1 bai).
   - _chon_bai_dung_sai(): chon BAI cho cau Dung/Sai theo so tiet giam
     dan (truoc day _chon_chuong_dung_sai chon theo CHUONG).
   - _tru_phan_dung_sai(): tru phan cau Dung/Sai da chiem, ngay tai bai
     do. Neu bai do von khong duoc chia cau nao o muc dang xet thi bo
     qua, KHONG day sang bai khac.
   - Curriculum gio group theo (bai, MucDo) thay vi (chuong, MucDo).
   - _phan_bo_vd_vdc() chay tren danh sach BAI thay vi danh sach CHUONG
     -> "moi don vi kien thuc toi da 1 cau VDC" dung nhu quy dinh.
   - Muc VD/VDC dung MOT ngan sach tru chung cho ca 3 phan MC/SA/TL,
     tru theo thu tu MC -> SA -> TL. Neu khong lam vay, 1 cau Dung/Sai
     se bi tru 3 lan (moi phan 1 lan).
   - Blueprint item gio co them "bai_so"; item dung_sai co them
     "bai_id" + "bai_so" (van giu "chuong_so" de CN_QuestionSelector
     chay nhu cu, khong pha tuong thich).
   - Tra ve them so_tiet_theo_bai de tien doi chieu khi debug.

VI DU KIEM CHUNG (de HeSo1 chuong 1 lop 10, 2 bai deu 4 tiet;
dat hang 6 TN + 1 DS + 2 TLN):
   Chi tieu TN: NB 4, TH 1, VD 1, VDC 0
   DS chon bai L10_C1_B1
   NB: chia theo tiet B1=2, B2=2 -> tru 1 o B1 -> B1=1, B2=2 (con 3)
   TH: chia theo tiet B1=1       -> tru 1 o B1 -> con 0
   VD: TN co 1 -> DS lay het     -> TN het cau VD
   TLN: VD 1 / VDC 1 -> DS lay VDC -> con dung 1 cau VD

HAM CU CON GIU LAI (khong con duoc goi, giu de doi chieu va phong khi
can quay ve cach cu): _chia_theo_so_bai(), _chon_chuong_dung_sai().

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.39

Ngày

2026-09-12

Nội dung

Sua sot cua nut "Lam de khac cung cau truc" (them o Version 2.37): nut
nay sinh de moi roi NHAY THANG sang trang lam bai, khong ghi gi vao hoi
thoai. Hau qua: de thu 2 co that trong he thong, cham diem duoc, nhung
KHONG de lai dau vet nao trong chat - khong co link tai file, quay lai
hoi thoai cung khong thay.

app/templates/chat/lam_bai.html, ham lamDeKhac(): sau khi co de_id moi,
goi /api/chat/luu-de-truc-tiep voi file_url = /api/exam/tai-de/{de_id}
truoc khi chuyen trang - dung chung duong di voi form tao de nhanh, de
moHoiThoai() ve lai duoc link tai file khi tai lai trang. Loi khi luu
chat KHONG chan viec sang de moi (try/catch, chi console.error).

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.40

Ngày

2026-09-12

Nội dung

Nut "Loi giai cua de nay" gan duoi TUNG de trong hoi thoai.

VAN DE: hoc sinh lam 2 de lien tiep roi go "cho toi dap an cua ca 2 de"
-> chi ra loi giai cua DE MOI NHAT. Khong phai bug: luong xin loi giai
goi history_service.lay_de_gan_nhat(), von chi lay 1 de
(.order("created_at", desc=True).limit(1)). He thong khong co khai niem
"nhieu de cung luc".

CACH XU LY (giao vien chon 2026-09-12): khong day viec doan y cho AI,
cung khong lam tinh nang "xuat nhieu de cung luc". Moi de hien san 1 nut
"Loi giai" ngay duoi no - bam la ra dung loi giai cua de do.

1. app/routers/exam.py:
   - Tach phan sinh loi giai ra ham dung chung _xuat_loigiai(de).
   - GET /api/exam/tai-loigiai/{de_id} (MOI): loi giai cua DUNG 1 de
     theo de_id. POST /api/exam/export-loigiai giu nguyen (theo
     conversation_id - de moi nhat) de n8n va luong chat cu khong gay.

2. app/routers/chat.py: URL file de luu vao chat_history duoc gan them
   "?de=<de_id>". May chu file bo qua query string nen link tai file
   chay y nhu cu, nhung khi tai lai lich su thi Frontend van biet tin
   nhan do thuoc de nao. Chi gan cho DE, khong gan cho file loi giai.

3. app/templates/chat/chat.html:
   - layDeIdTuUrl(): boc de_id tu URL, ho tro ca 2 dang -
     "...pdf?de=<id>" (luong chat) va "/api/exam/tai-de/<id>" (nut
     "Lam de khac", Version 2.37).
   - htmlNutLoiGiai(): sinh link "📄 Lời giải của đề này".
   - Gan vao ca 2 cho: luc de vua duoc tao, va luc tai lai lich su
     hoi thoai.

LUU Y: de sinh TRUOC ban nay khong co "?de=" trong lich su nen khong co
nut. De tao tu bay gio tro di moi co.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.41

Ngày

2026-09-12

Nội dung

Sua loi "Loi chon cau hoi: L10_C1_B2_VD021 (SA): khong co Generator nao
khop trong Mapping" khi bam nut "Lam de khac cung cau truc".

NGUYEN NHAN 1 (sot cua Version 2.37): /api/exam/lam-de-khac de cung
cho_phep_thieu=False, trong khi form tao de nhanh o chat.html (dong 782,
998) gui cho_phep_thieu=true. Cung mot cau truc de, tao qua chat thi ra,
bam nut thi bao loi - nut KHAT KHE HON ca luong chinh.

Sua: /generate-pdf-auto luu them "cho_phep_thieu" vao cot blueprint;
/lam-de-khac doc lai gia tri do. De sinh truoc ban nay khong co truong
nay -> mac dinh True cho giong luong chat.

NGUYEN NHAN 2 (goc re, giao vien quyet GIU NGUYEN 2026-09-12): ngan
hang chuong 1 thieu cau Tra loi ngan. Toan bo
data/mapping/toan10/L10_C1.json chi co DUNG 1 cau SA:
    L10_C1_B1_VD014_SA_A   (bai 1)
Bai 2 muc VD chi co VD020 (MC, TL) va VD021 (MC) - khong co SA nao.
De can 2 cau SA muc VD; tu Version 2.38 VD/VDC duoc rai tren tung BAI
nen bai 2 buoc phai lay VD020/VD021 -> khong co generator SA -> loi.
Truoc 2.38 rai theo CHUONG nen hay chon trung VD014 hai lan, che mat lo
hong nay. Thay doi 2.38 khong tao ra van de, chi LAM LO RA.

Quyet dinh: KHONG sua logic chon cau de tranh don vi thieu generator.
Giai doan nay van dang xay ngan hang de, nen de o "THIEU CAU HOI" hien
ra cho biet cho nao con thieu ma bo sung generator, hon la am tham chon
cau khac lam sai ti le theo tiet.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.42

Ngày

2026-09-12

Nội dung

Moi tin nhan BAO LOI trong chat gio hien kem nut "📝 Tạo đề nhanh (chọn
lớp/chương)" - dung cai nut o loi chao mo dau.

Ly do (yeu cau cua giao vien): khi AI khong hieu yeu cau (vd hoc sinh go
"làm đề tiếp theo"), truoc day chat chi bao "AI chua xu ly duoc yeu cau
nay, vui long thu lai voi yeu cau tao de cu the (lop/chuong/so cau...)"
roi de hoc sinh tu nghi ra cau lenh dung cu phap. Gio co san duong di
thu hai: bam nut chon lop/chuong -> goi thang /api/exam/generate-pdf-auto,
KHONG qua AI nen luon chay.

app/templates/chat/chat.html:
- htmlNutTaoDeNhanh(): tach rieng phan HTML cua nut, dung chung cho loi
  chao mo dau va cac tin nhan loi (truoc day viet thang trong
  hienChaoMoDau).
- addAIMessageLoi(): hien tin nhan loi + 1 dong goi y + nut tao de nhanh.
- Ap dung o CA 3 cho bao loi: loi tu server (data.success = false), loi
  ket noi (khoi catch), va loi cu khi tai lai lich su hoi thoai.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.43

Ngày

2026-09-12

Nội dung

Hien LY DO khi khong dang duoc de/bai giai/diem len Google Classroom.

VAN DE: dang_ket_qua_len_classroom() (app/services/classroom_service.py)
luon tra ve {"success": bool, "message": str} va KHONG BAO GIO raise -
dung y do, vi day la tien ich them, khong duoc chan hoc sinh xem diem.
Nhung app/templates/chat/lam_bai.html goi API roi VUT BO hoan toan phan
hoi (chi await fetch(), khong doc res). Hau qua: dang that bai thi im
lang tuyet doi, phai SSH vao VPS doc log moi biet ly do.

app/templates/chat/lam_bai.html:
- Them o #trang-thai-classroom ngay duoi khoi diem o trang ket qua.
- dangKetQuaLenClassroom() gio doc res.json() va hien:
  "⏳ Đang đăng..." -> "✅ Đã đăng..." hoac "📤 Chưa đăng được lên
  Classroom: <message>".
- Luon kem cau "Điểm của em vẫn được lưu bình thường, không ảnh hưởng
  gì" - dang Classroom that bai KHONG lam mat diem da cham.
- Doc ca data.detail (FastAPI tra 401 dang {"detail": ...} khi phien
  dang nhap het han) chu khong chi data.message.

CAC NGUYEN NHAN CO THE GAP (de doi chieu khi thay thong bao):
- "Chưa kết nối Classroom (vào /gv/classroom/connect)": chua co
  refresh_token trong DB.
- "Không tải được file lên Drive." / "Không tạo được bài đăng trên
  Classroom.": NGHI NHIEU NHAT - refresh_token cu xin TRUOC khi them 2
  scope classroom.coursework.students + drive.file (Version 2.34), nen
  khong mang quyen moi. Phai vao Google Cloud Console > Data Access them
  2 scope, ROI lam lai /gv/classroom/connect de xin refresh_token MOI.
  Log VPS se in "LOI TAI FILE LEN DRIVE: 403 ..." hoac "LOI TAO
  COURSEWORK MATERIAL: 403 ...".
- "Chưa có mã lớp Classroom cho <khoi>-<lop>.": thieu trong
  MA_LOP_CLASSROOM (app/core/lop_config.py). Da kiem tra: ("10","Tự do")
  CO san (course_id 874602361962) nen khong phai nguyen nhan hien tai.
- "Chưa xác định được lớp của học sinh.": hoc sinh chua chon lop.

Nguoi thuc hien

Mai Ha Lan (cung Claude)

===============================================================================

Version 2.44

Ngày

2026-09-13

Nội dung

Sua loi 403 khi dang de/bai giai/diem len Google Classroom. Log VPS:

    LOI TAO COURSEWORK MATERIAL: 403
    "message": "Request had insufficient authentication scopes."
    "reason": "ACCESS_TOKEN_SCOPE_INSUFFICIENT"

NGUYEN NHAN: Google tach RIENG 2 scope cho 2 loai bai dang khac nhau,
ten gan giong nhau nen rat de nham:

    classroom.coursework.students  -> courses.courseWork
                                      (BAI TAP, co han nop, cham diem)
    classroom.courseworkmaterials  -> courses.courseWorkMaterials
                                      (TAI LIEU, khong han nop)

_tao_coursework_material() goi .../courses/{id}/courseWorkMaterials (tai
lieu) nhung SCOPES chi khai classroom.coursework.students (bai tap). Xin
dung 1 scope, goi sang API kia -> 403.

Sua: them "https://www.googleapis.com/auth/classroom.courseworkmaterials"
vao SCOPES trong app/services/classroom_service.py.

CAC BUOC DA LAM TRUOC DO trong cung phien go loi nay (deu can, deu
KHONG du mot minh):
1. Version 2.43: hien ly do ra man hinh thay vi im lang - truoc do
   Frontend vut bo phan hoi cua /api/chat/dang-classroom nen khong ai
   biet tai sao that bai.
2. Bat Google Drive API trong project 299388243103. Loi truoc do:
   "Google Drive API has not been used in project ... or it is
   disabled". Xin scope va BAT API la 2 viec khac nhau: scope cho phep
   app XIN QUYEN, con API phai duoc bat thi project moi GOI DUOC.
3. Them scope courseworkmaterials (ban nay).

SAU KHI DEPLOY BAN NAY, BAT BUOC:
- Vao Google Cloud Console > Data Access, them scope
  classroom.courseworkmaterials.
- Vao lai /gv/classroom/connect de xin refresh_token MOI. Token cu
  khong tu nhien co them quyen moi.

Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.45 - 2026-09-13

## Bo sung so tay: tim kiem vecto va tai khoan giao vien

Them 2 tai lieu moi (chua trien khai code, moi la danh gia + ke hoach):

- docs/20_TIM_KIEM_VECTO.md - danh gia y tuong dua ngan hang de sang
  "lap trinh vecto" (embedding). KET LUAN: KHONG tiet kiem token vi
  luong chon cau hien tai khong goi AI lan nao; va KHONG duoc thay tra
  ID bang tim vecto vi ma tran de doi hoi DUNG chu khong phai GAN DUNG.
  Vecto chi dung duoc o 3 cho: o tim kiem cau hoi cho giao vien, do cau
  trung nghia khi nhieu nguoi cung dong gop, va gia su AI (RAG).
  Viec "de quan ly khi ngan hang lon" giai bang CHI MUC + bo do trung
  (Giai doan 0, khong can vecto). Neu lam vecto thi dung pgvector co san
  trong Supabase, va PHAI giu cac cot loc cung (lop/chuong/muc_do/
  loai_cau) de vecto khong bao gio tra ve cau sai muc do.

- docs/21_TAI_KHOAN_GIAO_VIEN.md - thiet ke + ke hoach 5 buoc.
  Hai van de da kiem tra duoc trong ma nguon:
  1. Cac route /gv/* chi kiem tra DA DANG NHAP, KHONG kiem tra vai tro
     -> bat ky hoc sinh nao biet duong dan /gv/thong-ke deu xem duoc
     diem ca lop. LO DU LIEU, phai sua truoc tien.
  2. classroom_service.luu_refresh_token() ghi vao bang classroom_oauth
     CHI 1 DONG (id=1) -> he thong chi phuc vu duoc DUNG 1 giao vien;
     giao vien thu hai ket noi se ghi de token cua nguoi thu nhat.

Khong sua code nao trong ban nay.

## Sua tai lieu (cung ngay)

Buoc 2 trong docs/23 ban dau viet "tao workflow n8n moi" - SAI. Workflow
NganHangDe da co san nhieu webhook trong cung mot canvas (doc-phieu-tra-loi,
cham-tu-luan). Gia su chi can them webhook thu 4 vao day, di thang
Webhook -> AI node -> Respond, KHONG qua CHV_Fun/Switch.

Ly do khong cho qua Switch (Switch nam SAU CHV_Fun):
- ton gap doi luot goi mo hinh (CHV_Fun phan loai roi node sau moi tra loi)
- system prompt cua CHV_Fun tron voi lenh_he_thong -> PHA LOP KHOA 1
- khong co gi de doan: Python da biet chac hoi cau so may, de nao

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.46 - 2026-09-13

## Tai khoan giao vien + va lo hong phan quyen /gv/*

Trien khai ca 5 buoc trong docs/21_TAI_KHOAN_GIAO_VIEN.md.

### BUOC 1 - Vai tro va chan cua (VA LO HONG)

VAN DE: moi route /gv/* chi goi get_current_user() - tuc chi kiem tra DA
DANG NHAP. Bat ky hoc sinh nao biet duong dan /gv/thong-ke deu xem duoc
diem va thong ke ca lop. Repo lai dang cong khai tren GitHub nen duong
dan nay khong he kho doan.

SUA:
- app/services/profile_service.py (MOI): lay_vai_tro / la_giao_vien /
  dat_vai_tro / lay_ho_so, doc cot profiles.vai_tro.
- app/core/deps.py: them lay_vai_tro(request, user) va
  yeu_cau_giao_vien(request, user). Chan o TANG SERVER, khong chi an nut.
- app/routers/classroom.py: ca 6 route /gv/* deu goi yeu_cau_giao_vien().
- Chua dang nhap -> ve /login. Da dang nhap ma khong phai giao vien -> 403.
- Neu chua chay SQL them cot vai_tro -> tra 500 kem loi noi ro phai chay
  SQL nao, KHONG im lang va cung KHONG mo cua.

### BUOC 2 - Dang ky tai khoan giao vien

- Xoa route GET /register/teacher CU (tro ve trang "Coming soon"). Route
  cu nam o dau file auth.py nen neu chi them route moi o cuoi thi FastAPI
  van dung route cu - da kiem tra bang cach liet ke router.routes.
- GET/POST /register/teacher that + app/templates/auth/register_teacher.html.
- Phai nhap dung MA_MOI_GIAO_VIEN (bien moi truong trong .env). De trong
  bien nay thi KHONG ai dang ky duoc giao vien (an toan mac dinh).
- Khong co nut "Dang ky bang Google" o trang nay: luong Google khong mang
  theo duoc ma moi.
- supabase_service.sign_up() them tham so vai_tro + **them (truong,
  to_chuyen_mon) ghi vao user_metadata; sau do router con goi
  profile_service.dat_vai_tro() mot lan nua de khong phu thuoc trigger.
- /teacher-coming-soon giu lai, chuyen huong sang /register/teacher.

### BUOC 3 - Moi giao vien mot ket noi Classroom

VAN DE: luu_refresh_token() ghi vao bang classroom_oauth CHI 1 DONG
(id=1). Giao vien thu hai bam ket noi la ghi de token cua nguoi thu nhat,
tu do bai cua hoc sinh dang nham sang Classroom cua nguoi kia.

SUA (classroom_service.py):
- luu_refresh_token(refresh_token, user_id=None, email_google=None)
- lay_refresh_token(user_id=None)
- lay_giao_vien_cua_lop(khoi, lop)  - doc bang lop_giao_vien
- lay_refresh_token_theo_lop(khoi, lop) - dung cho 3 ham chay trong ngu
  canh HOC SINH: tu_dong_ghi_danh_classroom, dang_ket_qua_len_classroom,
  tao_link_gia_nhap_lop.
- dong_bo_toan_bo(user_id=None)

TUONG THICH NGUOC: moi ham deu tu dong lui ve bang classroom_oauth cu khi
bang moi chua ton tai hoac lop chua gan giao vien. Nghia la deploy ban
nay TRUOC khi chay SQL cung khong lam hong gi.

### BUOC 4 - Khu lam viec giao vien

app/routers/teacher.py (truoc day rong) + 4 template moi:
- GET  /gv            - trang chinh, canh bao neu chua ket noi Classroom
- GET  /gv/ra-de      - bieu mau ra de, co o SO MA DE (1-8)
- POST /gv/ra-de      - goi generate_exam_pdf_auto role="teacher"
- GET  /gv/de-da-tao  - danh sach de, tai PDF de / PDF loi giai / .tex
- GET  /gv/lop        - danh sach lop, ma Classroom, giao vien phu trach

Them app/templates/layouts/tailwind_head.html - khoi <head> dung chung
(Tailwind CDN + bang mau), trich tu teacher_coming_soon.html de moi trang
moi khong phai chep lai ~120 dong cau hinh.

history_service.lay_de_cua_giao_vien(user_id, limit) - MOI.

### BUOC 5 - Tai ma nguon LaTeX

GET /api/exam/tai-tex/{de_id} - CHI giao vien. Tra ve file .tex da luu
san luc sinh de (file_de, loai_file="tex"), khong sinh lai de nen .tex
luon khop voi ban PDF da phat. 410 neu file da bi cron don sau 1 ngay.
Hoc sinh khong duoc tai vi file .tex chua ca \loigiai va cac dau \True.

### SQL PHAI CHAY (chay TRUOC khi deploy, xem docs/21 muc 3)

alter table profiles
  add column if not exists vai_tro text not null default 'hoc_sinh'
  check (vai_tro in ('hoc_sinh','giao_vien','quan_tri'));

update profiles set vai_tro='giao_vien' where email='lantuan2605@gmail.com';

create table if not exists classroom_oauth_gv (
  user_id uuid primary key references profiles(id) on delete cascade,
  refresh_token text not null,
  email_google text,
  updated_at timestamptz default now()
);

create table if not exists lop_giao_vien (
  khoi text not null, lop text not null,
  user_id uuid not null references profiles(id) on delete cascade,
  primary key (khoi, lop)
);

### BIEN MOI TRUONG MOI (.env tren VPS, khong qua git)

MA_MOI_GIAO_VIEN=<chuoi tu dat>

### DON DEP

Xoa 2 tep va cu con sot trong repo cong khai:
patch_classroom_service_link.py.b64, patch_classroom_service_write.py.b64.
Con 12 tep *.b64 cung loai chua xoa - cho giao vien xac nhan.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.47 - 2026-09-13

## VA LO HONG BAO MAT: khoa Supabase dung chung + tat RLS

Phat hien khi doc trigger handle_new_user (dang tim xem cot profiles.role
thua duoc ghi tu dau).

VAN DE - hai diem ghep lai:
1. app/core/supabase.py tao client bang SUPABASE_KEY, va CHINH bien do
   duoc nhung vao trang dang nhap/dang ky duoi ten supabase_anon_key
   (app/routers/auth.py). Ai xem ma nguon trang cung lay duoc.
2. Moi bang trong schema public deu TAT Row Level Security (nhan do
   UNRESTRICTED trong Supabase).

HAU QUA: bat ky ai cung co the doc/ghi thang vao cac bang qua PostgREST:
- Tu dat profiles.vai_tro = 'giao_vien' -> di vong qua ma moi, vao duoc
  het /gv/* (lam hong luon hang rao vua dung o Version 2.46).
- DOC refresh_token Google Classroom trong classroom_oauth /
  classroom_oauth_gv - chia khoa vao tai khoan Google cua giao vien.
- Doc diem moi hoc sinh (exam_history), sua diem cua chinh minh.
- Doc email toan bo hoc sinh (classroom_roster).

Lo hong co tu Version 2.4 (tat RLS cho nhanh) nhung chi thanh van de ro
rang khi co phan quyen giao vien.

SUA:
- app/core/config.py: them SUPABASE_SERVICE_KEY.
- app/core/supabase.py: tach LAM HAI client.
    supabase       = khoa anon  -> CHI xac thuc
    supabase_admin = khoa service_role -> MOI thao tac bang
  Chua dat SUPABASE_SERVICE_KEY thi tam lui ve khoa anon + in canh bao
  that to, de deploy khong lam chet web ngay.
- Doi sang supabase_admin: profile_service.py, history_service.py,
  classroom_service.py (ca file), supabase_service.py (2 ham doc/ghi
  profiles; phan sign_in/sign_up/get_user giu khoa anon).
- app/routers/auth.py va app/core/deps.py giu khoa anon - chi goi
  supabase.auth.*, khong dung .table().
- sql/22_bat_rls.sql (MOI): bat RLS cho MOI bang trong schema public
  bang vong lap, khong tao policy nao.
- docs/22_BAO_MAT_RLS.md (MOI): mo ta lo hong, cach va, thu tu thuc hien.

VI SAO KHONG CAN VIET POLICY CHI TIET: da kiem tra toan bo
app/templates/ - trinh duyet KHONG co mot lenh .from() hay .rpc() nao,
supabase-js phia trinh duyet chi dung de XAC THUC. Moi nghiep vu deu di
qua FastAPI dung nhu quy tac trong docs/13. Nen bat RLS khong policy la
du, va it rui ro nhat.

THU TU BAT BUOC (lam sai thu tu la web chet):
  1. Lay khoa service_role o Supabase > Project Settings > API Keys
  2. Them SUPABASE_SERVICE_KEY vao .env tren VPS
  3. git pull + systemctl restart nganhangde
  4. Thu web: dang nhap, tao de, /gv/thong-ke - phai chay
  5. Chay sql/22_bat_rls.sql
  6. Thu web lai lan nua
  7. DOI refresh_token Classroom (xem docs/22 muc 4) - khoa anon da cong
     khai lau nay nen phai coi nhu token da lo.

## Don dep kem theo

Cot profiles.role la cot THUA - khong mot dong code nao doc no. Trigger
handle_new_user cung KHONG ghi no (chi ghi id, email, ho_ten); gia tri
"student" la do DEFAULT cua cot. Doi ten thanh role_cu_khong_dung, mot
tuan sau khong gay gi thi drop han. Phan biet 3 chu "role" khac nghia:
  profiles.role      -> thua, khong dung
  de_da_sinh.role    -> student/teacher, quyet dinh xuat kem loi giai
  chat_history.role  -> user/assistant, ai noi cau do

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.48 - 2026-09-15

## Sua 2 loi o trang dang nhap

### 1. Go sai email/mat khau -> trang trang "Internal Server Error" (500)

NGUYEN NHAN: khoi try/except trong POST /login ket thuc bang "raise":

    except Exception as e:
        print("LOI LOGIN:", e)
        raise

In log xong nem lai loi -> FastAPI tra 500. Supabase nem AuthApiError khi
sai mat khau HOAC email chua dang ky, nen ca hai truong hop deu ra 500.

SUA: bat AuthApiError, hien lai trang dang nhap kem thong bao tieng Viet
(HTTP 401), giu lai email vua go de khoi nhap lai. Them ham
_trang_login_loi() dung chung. Them khoi {% if error %} vao
app/templates/auth/login.html (truoc do template KHONG co cho hien loi).

Rieng loi "Email not confirmed" co thong bao rieng: nhac kiem tra hop thu
va muc Thu rac.

LUU Y QUAN TRONG: KHONG the chuyen thang sang trang dang ky khi "tai khoan
khong ton tai" - Supabase CO Y tra ve cung mot loi "Invalid login
credentials" cho ca sai mat khau lan email chua dang ky, de nguoi ngoai
khong do duoc email nao da co tai khoan tren he thong. He thong khong
phan biet duoc 2 truong hop nay.

Vi vay thong bao gop ca hai kha nang lam mot:
    "Tai khoan khong ton tai hoac mat khau khong dung."
O bao loi KHONG them nut dang ky: trang dang nhap von da co 2 cho dan
sang /register (nut o thanh tren cung, va dong "Chua co tai khoan?" o
duoi form).

### 2. Nut "Ghi nho dang nhap" khong co tac dung

NGUYEN NHAN: login() dat cookie dung theo lua chon (co tick = 7/30 ngay,
khong tick = cookie phien), NHUNG middleware lam_moi_cookie_phien trong
app/main.py moi lan lam moi phien lai ghi de cookie voi han CO DINH 7/30
ngay, bat ke nguoi dung tick hay khong. Vi access_token het han sau ~1 gio
nen lan lam moi dau tien la lua chon bi xoa sach.

SUA: login() ghi them cookie sb_ghi_nho ("1"/"0"); middleware doc cookie
do va giu dung han nguoi dung chon.

Khong doi gi ve bao mat: sb_ghi_nho la httponly, chi chua "1" hoac "0".

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.49 - 2026-09-15

## Trang dang nhap VAN ra 500 sau khi da sua o Version 2.48

Ban 2.48 sua dung nguyen nhan thu nhat (khoi except ket thuc bang "raise")
nhung lai them nguyen nhan thu hai ngay trong cach sua, nen nguoi dung
khong thay khac gi: van trang trang.

NGUYEN NHAN THU HAI - traceback tren VPS noi ro:

    File "app/routers/auth.py", line 64, in _trang_login_loi
        return templates.TemplateResponse(
    File "starlette/templating.py", line 148, in TemplateResponse
        template = self.get_template(name)
    TypeError: unhashable type: 'dict'

Ban Starlette dang chay (1.6.0) da BO cach goi cu:

    templates.TemplateResponse("ten.html", {...})        # KIEU CU - HONG

No coi tham so vi tri dau la REQUEST va tham so thu hai la TEN TEP, nen
cai dict lot vao cho ten tep -> get_template(dict) -> unhashable.

Cach goi DUNG (tham so co ten):

    templates.TemplateResponse(
        request=request,
        name="ten.html",
        context={...},
    )

SUA: doi ca 3 cho con dung kieu cu trong app/routers/auth.py:
  - _trang_login_loi()                     (dong 64)
  - nhanh bao loi cua register_student()   (dong 285)
  - nhanh bao loi cua register_teacher()   (dong 333)

Ca 3 deu la NHANH BAO LOI - chi chay khi nguoi dung go sai - nen truoc
gio khong ai phat hien. Cac route GET von da dung kieu moi nen van chay
binh thuong.

Da quet lai toan bo app/: khong con cho nao dung kieu cu.

## Them bai kiem tra tu dong: tests/test_login_loi.py

Hai loi noi tiep o cung mot cho ma khong bai kiem tra nao bat duoc, vi
truoc gio chi kiem tra "import co chay khong". Bai moi dung TestClient
gia lap DUNG tinh huong go sai mat khau (monkeypatch supabase_service.
sign_in, KHONG can mang, KHONG can Supabase):

  - test_sai_mat_khau_khong_ra_500      : phai tra 401 + dung thong bao,
                                          va giu lai email vua go
  - test_loi_la_cung_khong_ra_500       : loi bat ngo cung khong duoc 500
  - test_trang_dang_nhap_binh_thuong    : GET /login van 200, khong hien
                                          o bao loi khi khong co loi

Da kiem chung bai test co "rang": goi kieu cu tren may cua giao vien cung
nem dung "TypeError: unhashable type: 'dict'", nen neu ai lo tay quay lai
kieu cu thi test do ngay.

## Bai hoc

Sua loi o nhanh bao loi thi PHAI thu chay that vao nhanh do. Import duoc
va test cu xanh khong chung minh duoc gi ve mot nhanh chi chay khi co loi.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.50 - 2026-09-15

## Trang "Toi la giao vien" + 1 loi do chinh ban 2.48 gay ra

### 1. Dang nhap bang Google khong chon duoc vai tro giao vien

VAN DE (giao vien bao): bam "Dang nhap bang Google" la vao thang, tu tao
tai khoan luon, nhung bi hoi CHON LOP ngay - khong co cho nao noi minh la
giao vien. Ly do: luong Google di duong rieng (supabase-js -> POST
/auth/set-session), KHONG qua /register/teacher nen khong co o nhap ma
moi va khong co buoc hoi vai tro -> moi tai khoan Google deu la hoc sinh.

SUA: them trang nang cap vai tro cho nguoi DA dang nhap:

    GET  /toi-la-giao-vien   - form nhap ma moi
    POST /toi-la-giao-vien   - dung ma -> dat vai_tro='giao_vien' -> /gv

- Dat o app/routers/auth.py, KHONG phai teacher.py: teacher.py chan het
  nguoi chua phai giao vien, ma trang nay danh cho dung nhung nguoi do.
- Da la giao vien roi thi GET tu chuyen thang sang /gv.
- Ma sai: tra 400, ghi log kem email nguoi thu (de biet neu co ai do do
  ma), va TUYET DOI khong dong vao vai_tro.
- Them template app/templates/auth/toi_la_giao_vien.html.
- Them loi ra o cuoi trang Chon lop (app/templates/chat/chon_lop.html):
  "Thay/co dang nhap nham vao day? Toi la giao vien".

Cach nay dung duoc ca cho tai khoan CU da tro thanh hoc sinh - khong phai
xoa di dang ky lai. Da can nhac 2 cach khac (hoi vai tro ngay sau khi
dang nhap Google; cam giao vien dung Google) - giao vien chon cach nay.

### 2. Dang nhap bang Google bi dang xuat khi dong trinh duyet

Loi NAY DO BAN 2.48 GAY RA, phat hien khi ra soat lai vi cau hoi tren.

Ban 2.48 cho middleware lam_moi_cookie_phien doc cookie sb_ghi_nho de
biet nguoi dung co tick "Ghi nho dang nhap" khong. Nhung /auth/set-session
(luong Google) khong he ghi cookie do -> middleware thay thieu, hieu la
"khong ghi nho", va bien 2 cookie phien thanh cookie tam ngay lan lam moi
dau tien -> dong trinh duyet la mat phien.

SUA: /auth/set-session ghi them sb_ghi_nho="1" cho khop voi han 7/30 ngay
ma chinh no dang dat.

BAI HOC: them mot cookie dieu khien thi phai ra soat MOI cho dat cookie
phien, khong chi cho vua sua.

## Them bai kiem tra

tests/test_login_loi.py them 3 bai cho trang moi:
  - chua dang nhap -> 303 ve /login
  - ma sai -> 400, va KIEM CHUNG dat_vai_tro() khong he duoc goi
  - ma dung (ke ca co khoang trang thua) -> 303 ve /gv, dat_vai_tro()
    duoc goi dung (user_id, 'giao_vien')

Tong: 17 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.51 - 2026-09-15

## Man hinh CHON VAI TRO sau khi dang nhap lan dau

Ban 2.50 moi chi them mot dong chu nho o cuoi trang Chon lop ("Thay/co
dang nhap nham vao day? Toi la giao vien"). Giao vien phan hoi dung va
thang: KHONG AI doc dong chu nho do, va cung khong ai biet trang web nay
CO phan vai tro. Phai la mot man hinh chon hai o to, giong het trang
dang ky.

SUA:

    GET  /chon-vai-tro   - 2 o to "Hoc sinh" / "Giao vien"
    POST /chon-vai-tro   - hoc_sinh  -> luu vai tro -> /chon-lop
                         - giao_vien -> /toi-la-giao-vien (nhap ma moi)

Man hinh nay hien NGAY sau khi dang nhap lan dau, truoc ca buoc chon lop.
Them chan o 2 cho trong app/routers/chat.py: GET /chat va GET /chon-lop
deu chuyen sang /chon-vai-tro neu tai khoan chua chon vai tro.

QUAN TRONG - bam "Giao vien" thoi thi CHUA duoc nang vai tro. Phai nhap
dung ma moi o /toi-la-giao-vien roi moi duoc. Trong luc do tai khoan van
giu 'chua_chon' de ai bo ngang giua chung thi lan sau vao van duoc hoi
lai, khong bi ket o vai tro hoc sinh. Co bai kiem tra rieng cho diem nay.

## Trang thai vai_tro moi: 'chua_chon'

Neu tai khoan moi mac dinh la 'hoc_sinh' thi he thong KHONG phan biet
duoc "da chon hoc sinh" voi "chua duoc hoi bao gio" -> khong biet luc nao
nen hien man hinh chon vai tro. Nen them gia tri thu tu:

    chua_chon | hoc_sinh | giao_vien | quan_tri

sql/23_chon_vai_tro.sql: noi rong rang buoc check + doi DEFAULT cua cot
sang 'chua_chon'. Tai khoan CU giu nguyen vai tro dang co, chi tai khoan
tao moi tu luc chay SQL moi mang 'chua_chon'.

'chua_chon' KHONG nam trong VAI_TRO_GIAO_VIEN nen van bi chan o /gv/* nhu
moi vai tro khac ngoai giao_vien - khong ho them duong nao.

## Them 5 bai kiem tra (tong 22, deu xanh)

  - chua chon        -> hien man hinh 2 o
  - da la hoc sinh   -> khong hoi lai, sang /chon-lop
  - da la giao vien  -> vao thang /gv
  - chon hoc sinh    -> luu dung ('hoc_sinh') roi sang /chon-lop
  - chon giao vien   -> sang /toi-la-giao-vien va KIEM CHUNG dat_vai_tro()
                        chua he duoc goi

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.52 - 2026-09-15

## 1. Giao vien bam "Chat AI" bi hoi chon lop nhu hoc sinh

NGUYEN NHAN: route GET /chat bat MOI nguoi phai co profiles.lop moi vao
duoc, khong thi day sang /chon-lop. Giao vien day nhieu lop, khong co
"lop cua minh" theo nghia hoc sinh, nen luon bi day sang do.

SUA (app/routers/chat.py):
- GET /chat : giao vien vao thang, KHONG kiem tra lop. Van dung Chat AI
  de ra de binh thuong.
- GET /chon-lop : giao vien vao nham thi day ve /gv.
- Them co la_giao_vien vao context cua chat.html.

## 2. Lay ma lop Google Classroom ngay trong /gv/lop

Giao vien can ma lop de phat cho hoc sinh (chinh cai ma hoc sinh nhap o
buoc "Tham gia lop"), truoc day khong co cho nao lay.

SUA: moi dong lop trong /gv/lop co nut "Lay ma"; bam thi goi
GET /gv/lop/ma?khoi=..&lop=.. -> tra ve ma dang ky + link tham gia lop,
hien ngay tai dong do kem nut "Mo lop".

Goi rieng tung lop khi bam, KHONG lay ca loat luc mo trang: moi lop la
mot luot goi sang Google, mo trang ma goi ca chuc lan thi rat lau.

## 3. Loi 403 tra ve JSON kho hieu -> hien trang ro rang

Giao vien bao "vao duoc /gv mot lan roi gio khong vao lai duoc" nhung
man hinh chi hien mot dong JSON {"detail": ...}, khong biet tai sao.

SUA (app/main.py): them exception handler cho 403. Neu trinh duyet xin
HTML thi hien trang auth/khong_du_quyen.html, GHI RO:
- dang dang nhap bang tai khoan nao
- VAI TRO HIEN TAI cua tai khoan do
- nut di tiep dung cho: chua_chon -> /chon-vai-tro; hoc_sinh ->
  /toi-la-giao-vien; chua_cau_hinh -> nhac chay SQL.
Cac ma loi khac giu nguyen hanh vi cu.

Trang nay chinh la cong cu tu chan doan: nhin mot cai la biet tai khoan
dang o vai tro nao va phai bam di dau.

## Mot loi tu gay ra trong luc sua, da bat duoc nho bai kiem tra

Lan sua dau tien dat nham doan "giao vien -> /gv" vao GET /chat thay vi
GET /chon-lop (hai ham co doan ma giong het nhau, replace trung cho dau
tien). Ket qua nguoc han y muon: giao vien bi day RA KHOI Chat AI. Bai
test test_giao_vien_vao_chat_KHONG_bi_hoi_chon_lop do ngay.

## Them 3 bai kiem tra (tong 25, deu xanh)

  - giao vien vao /chon-lop  -> 303 ve /gv
  - giao vien vao /chat      -> 200, KHONG co chu "Chon lop cua em"
  - hoc sinh vao /gv/thong-ke -> 403 va la TRANG HTML co huong dan,
    khong phai JSON

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.53 - 2026-09-15

## Trang "De da tao" chi tai duoc DE, khong co dap an va khong co .tex

Hai nguyen nhan doc lap, cong lai thanh mot trieu chung.

### Nguyen nhan 1 - giao dien GIAU nut khi chua co san dong trong file_de

de_da_tao.html va khu_lam_viec.html chi hien lien ket khi
de.files.get("loigiai") / .get("tex") co gia tri. De tao qua Chat AI di
theo role="student" -> assembler KHONG sinh san PDF loi giai
(pdf_loigiai_path = None) -> khong co dong "loigiai" -> nut bi giau.
Giao vien nhin vao tuong he thong khong ho tro.

Thuc ra GET /api/exam/tai-loigiai/{de_id} TU BIEN DICH loi giai tu file
.tex da luu neu chua co san (xem _xuat_loigiai, Version 2.40). Tuc la
chuc nang VAN CHAY, chi co cai nut la khong hien.

SUA: LUON hien ca 3 lien ket (PDF de / PDF loi giai / .tex). File nao
that su khong con thi endpoint bao loi ro rang (404/410) - van hon la
giau nut di khong noi gi.

### Nguyen nhan 2 - ban .tex luu cho giao vien la ban LOI GIAI

Trong exam_assembler_service.py nhanh role == "teacher":

    "tex_path": str(loigiai_tex_path),     # SAI

Ban de (dethi_tex_path) duoc tao ra roi VUT DI, chi giu ban loi giai.
Giao vien bam "tai .tex" tuong lay ma nguon DE, hoa ra ra ban da co san
loi giai - khong dung de in cho hoc sinh duoc.

SUA (ban dau lam phuc tap - xem ghi chu cuoi muc):
- Giu "tex_path" = ban LOI GIAI (nhu cu), CHI luu MOT tep .tex.
- GET /api/exam/tai-tex/{de_id} tra ve dung mot tep do.

GHI CHU - da lam thua roi rut lai: ban dau em sua thanh luu CA HAI ban
.tex (de + loi giai) va tai ve dang tep nen. Giao vien chi ra ngay la
thua: hai ban chi khac nhau dung mot tham so cua goi ex_test, doi
[loigiai] thanh [dethi] o dong \usepackage la an het loi giai - giao
vien nao dung LaTeX cung biet. Luu ban loi giai la du, vi tu do suy ra
ban de duoc, nguoc lai thi khong. Da bo phan zip va cot "tex_loigiai".

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.54 - 2026-09-15

## 1. Chon 4 ma de nhung chi ra 1 - SUA TAN GOC

Loi da ghi nhan tu Version 2.46 (muc "chua lam"), nay sua that.

NGUYEN NHAN: socau_ma_de duoc TRUYEN XUONG ham sinh cau
(call_generator(socau_yeu_cau=socau_ma_de)). Ham sinh tra ve mot chuoi
chua N khoi \begin{ex}, roi tat ca duoc noi vao CUNG MOT de. Ket qua la
mot de ma moi cau lap lai N lan - khong phai N de.

SUA: dao nguoc cach lam. Vong lap N MA DE nam o NGOAI; moi vong goi lai
toan bo ham sinh voi socau_yeu_cau=1 -> moi ma de co bo so lieu rieng.
Ket qua: N ma de that su, cung cau truc, cung don vi kien thuc, chi khac
so lieu - dung nhu giao vien can de in kiem tra.

- Ma de danh so 1001, 1002, 1003... (tinh_ma_de(lop, thu_tu)).
- used_variants rieng cho tung ma de: trong CUNG mot ma de khong lap lai
  bien the, nhung giua cac ma de thi duoc - cac ma de von phai tuong
  duong nhau ve dang toan.
- File dap an: ma de > 1 thi moi ban ghi them truong "ma_de". Van la mot
  danh sach phang nen cho nao dang doc file nay khong bi vo.

## 2. Cau truc de theo dung 4 PHAN cua Bo

Truoc day cac cau noi duoi nhau thanh mot mach, khong co tieu de phan.
Nay gom theo DANG CAU va xuat dung thu tu de cua Bo (QD 764/QD-BGDDT):

    PHAN I.   MC - Thi sinh tra loi tu cau 1 den cau {n}. Moi cau hoi
                   thi sinh chi chon mot phuong an.
    PHAN II.  TF - ... Trong moi y a), b), c), d) o moi cau, thi sinh
                   chon dung hoac sai.
    PHAN III. SA - Thi sinh tra loi tu cau 1 den cau {n}.
    PHAN IV.  TL - Thi sinh trinh bay tu luan tu bai 1 den bai {n}.

- \setcounter{ex}{0} truoc MOI phan -> moi phan danh so lai tu 1.
- So cau trong loi dan lay tu so cau THAT cua phan do, khong ghi cung.
- Phan nao khong co cau nao thi BO HAN va khong chiem so La Ma (khong bi
  nhay coc "PHAN I" roi "PHAN III").

## 3. Moi ma de mot khoi day du, tu sang trang

Moi ma de gio co: \tieude + o "Ho ten thi sinh / Ma de" + \chantrang +
than 4 phan + \hetde\label{made<ma>}, cac ma de cach nhau bang \newpage.
Moi ma de co NHAN RIENG nen \pageref dem dung so trang cua chinh no, va
\setcounter{page}{1} de moi de danh so trang lai tu 1 - giong het cach
lam trong bo de mau cua giao vien.

VIET LAI data/config/latex_template.tex: phan than tai lieu gio chi con
__NOI_DUNG__. Toan bo tieu de / o ho ten / chan trang / het de chuyen
sang Python (exam_assembler_service._khung_mot_ma_de), vi mot tep .tex
nay co the chua nhieu ma de, moi ma de can mot bo day du rieng.
build_latex_document() chi con thay bien o PHAN DAU tai lieu (goi
ex_test, nam hoc).

KHONG dung \input nhu bo de mau cua giao vien: tat ca noi dung nam trong
MOT tep duy nhat, dung yeu cau "chi xuat 1 file".

## 4. Kiem chung

tests/test_cau_truc_de.py (MOI, 8 bai): du 4 phan dung thu tu; moi phan
\setcounter{ex}{0}; so cau trong loi dan khop thuc te; phan rong bi bo
han khong nhay so La Ma; suy loai cau tu Generator ID; mot ma de du tieu
de/o ho ten/chan trang/het de; hoc sinh KHONG co o ho ten va ma de;
4 ma de -> 4 khoi rieng, 3 lan \newpage, noi dung khac nhau.

Tong 33 bai, deu xanh.

CHUA KIEM CHUNG DUOC O DAY: bien dich PDF that. May cua giao vien thieu
tabvar.sty, bclogo.sty... nen pdflatex khong chay het duoc; VPS co ban
TeX day du. Phai xem PDF that tren web sau khi deploy.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.55 - 2026-09-15

## Chat AI phan biet vai tro giao vien / hoc sinh

VAN DE: luong chat luon gui role="student" xuong
/api/exam/generate-pdf-auto (gan cung trong Code Node cua n8n), nen giao
vien dung Chat AI cung chi nhan DE TRAN: khong loi giai, khong o "Ho ten
thi sinh / Ma de".

SUA - dat quyet dinh o MAY CHU, khong sua n8n:

    role_that = payload.role
    if payload.user_id and profile_service.la_giao_vien(payload.user_id):
        role_that = "teacher"

May chu tu tra profiles.vai_tro theo user_id va EP role="teacher" neu
dung la giao vien, bat ke n8n gui gi. Dung nguyen tac docs/00: nghiep vu
thuoc ve Code, AI/n8n khong duoc quyet dinh. Sua trong n8n cung duoc
nhung ai lo tay doi prompt la hong, con cho nay thi chac chan.

Ket qua: giao vien chat mot cau la nhan DU de + loi giai, de co san o ho
ten va ma de. Hoc sinh giu nguyen nhu cu (chi de tran) - da co bai kiem
tra rieng cho ca hai chieu.

role THAT cung duoc luu vao de_da_sinh, nen nut "Lam de khac cung cau
truc" giu dung vai tro.

## Gui them vai_tro sang n8n

_goi_n8n() gui kem truong "vai_tro" de CHV_Fun xung ho cho dung ("em"
voi hoc sinh, "thay/co" voi giao vien) va hieu duoc yeu cau rieng cua
giao vien (vi du "cho 4 ma de"). Log chat cung ghi kem vai tro.

LUU Y: truong nay CHI de AI noi nang cho dung. Viec co xuat loi giai hay
khong KHONG phu thuoc no - da do may chu quyet dinh o tren.

VIEC CON LAI THUOC VE n8n (khong sua duoc tu code): muon giao vien go
"cho toi 4 ma de" trong chat ma ra 4 ma de thi prompt CHV_Fun phai doc
duoc so do va dat vao truong socau_ma_de. Hien chat luon ra 1 ma de;
muon nhieu ma de thi dung bieu mau /gv/ra-de.

## Them 2 bai kiem tra (tong 35, deu xanh)

  - giao vien chat -> may chu ep role=teacher du n8n gui "student"
  - hoc sinh chat  -> van la "student", KHONG duoc nhan loi giai

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.56 - 2026-09-15

## /gv/ra-de chan ca may chu, nhieu ma de thi khong ra de nao

TRIEU CHUNG: giao vien chon 4 ma de, bam Tao de, cho mai roi bang "De da
tao" van y nguyen - khong co dong moi nao. Chay thang ham sinh de tren
VPS thi RA DUNG 4 ma de, nen loi khong nam o bo sinh de.

NGUYEN NHAN: app/routers/teacher.py::ra_de_submit khai la "async def"
nhung goi THANG generate_exam_pdf_auto() - mot ham DONG BO va rat lau
(moi ma de mot lan bien dich LaTeX, khoang 30-60 giay). Goi dong bo
trong "async def" CHAN han event loop cua uvicorn:

  - Ca web dung hinh trong suot luc sinh de (nguoi khac khong vao duoc).
  - Voi nhieu ma de thi vuot thoi gian cho cua nginx -> ket noi bi cat
    truoc khi sinh xong -> khong luu duoc de nao.

Endpoint /api/exam/generate-pdf-auto (luong chat/n8n) KHONG dinh loi nay
vi no khai bang "def" - FastAPI tu day ham dong bo sang threadpool.
Chinh vi the chat van ra de binh thuong con /gv/ra-de thi khong.

SUA: goi qua run_in_threadpool(). Them log ro rang cho moi lan ra de
(lop / ki thi / chuong / so ma de) va canh bao rieng khi sinh de xong
nhung KHONG luu duoc de_da_sinh - truong hop do de cung khong hien
trong bang "De da tao", truoc day im lang hoan toan.

BAI HOC: trong FastAPI, ham xu ly viec NANG va DONG BO thi hoac khai
bang "def" (de FastAPI tu dua sang threadpool), hoac neu da tro thanh
"async def" thi phai boc qua run_in_threadpool. Khong duoc goi thang.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)


===============================================================================

# Version 2.57 - 2026-09-15

## /gv/ra-de: de sinh xong nhung KHONG BAO GIO luu duoc

Log tren VPS chi dung thu pham:

    LOI LUU DE_DA_SINH: invalid input syntax for type uuid:
    "gv-1e07cdec-2185-4483-879e-1dfca2d3430c"  (code 22P02)

NGUYEN NHAN: khi lam khu lam viec giao vien (Version 2.46) da dat

    conversation_id = f"gv-{uuid.uuid4()}"

de phan biet de do giao vien tao voi de tu luong chat. Nhung cot
conversation_id trong bang de_da_sinh co kieu UUID - them tien to "gv-"
vao la chuoi khong con la UUID hop le, Postgres tu choi ca 2 lan ghi
(lan 2 bo blueprint cung the). de_id tra ve None -> khong luu file nao,
bang "De da tao" khong bao gio co dong moi.

Loi nay dinh tu 16:13 ngay 15/09 - tuc la MOI lan bam "Tao de" o
/gv/ra-de tu luc co trang do den gio deu that bai. Giao vien tuong la
"khong co gi thay doi", thuc ra de sinh ra dung het roi bi vut di.

SUA: bo tien to, dung str(uuid.uuid4()). Khong can tien to that: cot
role da ghi "teacher" de biet de do giao vien tao.

## Sinh de xong ma luu hong thi PHAI bao ra man hinh

Truoc day chi ghi log roi van chuyen sang bang "De da tao" - bang trong
tron, khong mot chu nao giai thich. Chinh cho nay lam mat ca buoi do
tim. Nay chuyen ve /gv/ra-de kem thong bao ro rang va chi luon cau lenh
xem log.

Cac thong bao loi khac cung duoc quote() cho dung: truoc day noi thang
chuoi loi vao URL nen tieng Viet co dau bi vo.

## Them bai kiem tra

tests/test_cau_truc_de.py: gui POST /gv/ra-de that (monkeypatch cac ham
cham), roi PARSE conversation_id bang uuid.UUID() - co tien to la hong
ngay. Kiem them role="teacher" va blueprint.socau_ma_de dung bang so
nguoi dung nhap.

Tong 36 bai, deu xanh.

## Bai hoc

Ghi log "khong luu duoc" la dung, nhung CHUA DU: phai bao ra man hinh.
Nguoi dung khong doc log may chu, va im lang thi ho se bao "khong co gi
thay doi" - dung nhu da xay ra.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.58 - 2026-09-16

## GIA SU AI - MUC A

Hoc sinh nop bai xong, o moi cau trong trang ket qua co them nut
"Hoi thay/co AI ve cau nay". Bam vao la mo mot khung hoi dap ngay tai
cho, giang lai DUNG cau do.

Rang buoc goc cua co Lan: "khong ra ngoai bat ki cai nao. Dap an thi
phai lay ngay dap an Python toi da chuan bi theo de. Khong duoc de AI tu
tinh toan." Toan bo thiet ke phuc vu cau nay.

## Ba lop khoa

1. CAU LENH (gia_su_service.LENH_HE_THONG): de bai, dap an dung va loi
   giai chuan duoc nhet SAN vao lenh. Mo hinh chi duoc dien dat lai, cam
   tinh toan, cam ra so khac loi giai mau, cam noi sang cau khac. Co san
   mot cau tu choi de mo hinh dung lai khi bi hoi ra ngoai.
2. HIEN THI: API luon tra ve dap_an_python + loi_giai_python nguyen van,
   giao dien ve chung NGAY CANH cau tra loi cua AI. Lech la thay ngay.
3. NHAT KI: bang gia_su_hoi_dap luu ca cau tra loi cua AI lan dap an
   Python da dua vao lenh. Co doc lai o /gv/gia-su, doi chieu 2 cot.

Quy tac bao trum: KHONG CO LOI GIAI CHUAN THI KHONG GOI MO HINH. Thieu
du lieu -> bao loi va dung, vi luc do AI bat buoc phai tu nghi ra.

## Han muc luot

20 luot/em/ngay (GIA_SU_LUOT_MOI_NGAY trong .env). Ngay chot theo gio
Viet Nam, khong theo UTC - theo UTC thi 7h sang da bi tinh sang ngay hom
sau, hoc sinh mat luot giua buoi hoc. Chi tru luot KHI DA CO cau tra
loi: mat mang, n8n hong, het du lieu deu khong tru. Co nang rieng cho
tung em o /gv/gia-su (chi co hieu luc trong ngay).

## Chay duoc ngay ca khi chua bat AI

N8N_WEBHOOK_GIA_SU de trong -> nut chay o "che do khong AI": bam vao la
hien loi giai chuan cua co. Khong bao gio vo trang hoc sinh. Nho vay
deploy ban nay truoc, tao workflow n8n sau cung duoc.

## Tep

Moi: sql/24_gia_su.sql, app/services/gia_su_service.py,
app/routers/gia_su.py, app/templates/teacher/gia_su.html,
tests/test_gia_su.py, docs/23_GIA_SU_AI.md
Sua: app/core/config.py, app/main.py, app/routers/teacher.py,
app/templates/teacher/_base_gv.html, app/templates/chat/lam_bai.html

## Bai kiem tra

tests/test_gia_su.py - 27 bai, soi dung 3 lop khoa:
- cau lenh co du de bai/dap an/loi giai va du cac cau cam
- thieu ngu canh / het luot / cau hoi rong -> KHONG goi mo hinh (kiem
  bang cach dem so lan _goi_mo_hinh duoc goi, phai bang 0)
- ket qua luon kem dap_an_python + loi_giai_python
- mo hinh loi thi khong tru luot
- user_id lay tu cookie, gui them user_id trong body bi bo qua

Tong 58 bai (36 cu + 22 moi o tang nghiep vu + 5 o tang API), deu xanh.
(tests/test_supabase.py can mang that nen khong tinh o day.)

## Con lai

Muc B (chi dung cho trong tai lieu li thuyet .tex khi hoc sinh van chua
hieu) CHUA LAM - dang cho mot tep .tex mau de xem cau truc. Huong da
chot: tra theo ID truoc (moi cau da co san L10_C1_B2...), vecto tinh sau.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.59 - 2026-09-16

## Ghi lai TUNG NODE cua workflow n8n vao doc 06

Co Lan nhac: da co yeu cau tu truoc la moi lan dong vao n8n phai ghi vao
so tay ki thuat, ghi lai tung node de sau con hieu n8n dang lam gi. Ban
v2.58 chi ghi vao docs/23 cach tao webhook gia su, khong cap nhat
docs/06_N8N_WORKFLOW.md - thieu sot.

Nay doc 06 co them muc "Cap nhat 2026-09-16" ghi day du:

- Toan canh: MOT workflow NganHangDe, BON webhook doc lap
  (/chat, /doc-phieu-tra-loi, /cham-tu-luan, /gia-su). Chi /chat co
  CHV_Fun + Switch; ba cai con lai di thang.
- Bang tung node cho ca 4 nhanh: ten node, loai node, vao gi ra gi,
  va VI SAO no ton tai. Gom ca cac node truoc day chua duoc ghi:
  Sua_Lop_Bang_Regex, Can_Xac_Nhan_Cau_Truc, Tra_Loi_Xac_Nhan.
- Payload vao/ra cua tung webhook, doc chac tu ma nguon Python.
- Bon quy tac rut ra: viec nao Python xac dinh duoc thi dung de AI
  doan; AI nhan san dap an chuan, khong tu tinh; webhook nao viec da
  ro thi di thang, dung nhet vao Switch; toan bo cau lenh dung o
  Python, n8n chi goi mo hinh.
- Bang viec ton dong o n8n (4 rule chet trong Switch, Ghep_Tham_So mat
  dau tieng Viet, CHV_Fun chua hieu "4 ma de", cac cho con danh dau (?)).

## Phan biet nguon

Phan giao tiep (URL, payload) doc CHAC tu ma nguon Python. Phan cau hinh
ben trong tung node doc tu so do canvas - cho nao chua chac danh dau (?)
de sau mo node xac nhan, khong ghi bua thanh su that.

## Quy tac tu nay

Ghi ngay luc dong vao n8n, khong de don. So do n8n nhin thi dep nhung 3
thang sau mo ra khong ai nho node Sua_Lop_Bang_Regex sua cai gi.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.60 - 2026-09-17

## CHV_Fun tu choi giai bai thi phai CHI DUONG sang gia su

Hoc sinh go "giai cho toi bai 3" trong Chat AI. CHV_Fun tra loi "minh
khong co chuc nang giai dau nha" roi dung.

Tu choi la DUNG: bai le ngoai web khong co dap an Python nao de bam,
giang la phai tu tinh, ma mo hinh tinh so hoc rat hay sai. Nhung tu choi
xong thi BO EM AY GIUA DUONG - he thong gio DA CO gia su AI (v2.58)
giang lai tung buoc, chi la em ay khong biet loi vao.

## Da sua

data/prompts/CHV_Fun.md them muc "Cach tu choi": message cua
reject_math_solution phai co du 3 y - tu choi (GIU GIONG VUI, co Lan co
y lam vui), noi ro minh giang duoc voi cau trong de vua lam, chi dung 3
buoc tao de -> nop bai -> bam nut "Hoi thay/co AI ve cau nay".

Sua kem o giao dien (khong phu thuoc AI, luon chay):
- chat.html loi chao mo dau: them dong "Chua hieu bai? Lam xong de roi
  bam Hoi thay/co AI ve cau nay".
- chat.html addAIMessageLoi(): moi tin nhan loi gio chi CA HAI duong -
  nut "Tao de nhanh" va cach hoi bai.
- chat.py: thong bao khi n8n tra JSON hong cung chi duong tuong tu.

## Phat hien them: prompt trong repo LECH voi n8n

data/prompts/*.md la BAN GHI, khong phai ban dang chay. CHV_Fun.md trong
repo (62 dong) NGAN HON ban chay that - ban that co them phan giong dieu,
cach xung ho (nhin cau tra loi tren web la thay). Da ghi canh bao vao
dau tep va vao docs/18 + bang ton dong docs/06.

## Con lai

PHAI DAN prompt moi sang node CHV_Fun tren n8n thi moi co tac dung. Ban
sua o giao dien thi chay ngay sau khi deploy.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.61 - 2026-09-17

## Nut "Hoi lai de cu" trong Chat AI + sua prompt CHV_Fun

Co Lan chi ra dung goc van de: hoc sinh vua tao de xong thi trong dau da
co ngu canh roi, go "giai bai 3" la du voi cac em. Bat mo hinh doan "bai
3 cua de nao" la SAI TU GOC - no khong co cach nao biet. Bam nut thi may
chu BIET CHAC de_id va so_thu_tu, khong phai doan, khong ton mot luot goi
mo hinh nao de phan loai. Dung nguyen tac "Uu tien Code hon AI".

## Giao dien

Hai nut co dinh duoi o nhap chat: [Tao de moi] [Hoi lai de cu].
Bam "Hoi lai de cu" -> hien de gan nhat trong hoi thoai, chia PHAN I/II/
III/IV, moi phan mot hang nut so cau. Bam so cau -> giang lai ngay trong
khung chat, KEM loi giai chuan do Python sinh (lop khoa 2 giu nguyen).

## PHAI NOP BAI ROI MOI HOI DUOC

Cau chua nop bai thi nut MO, khong bam duoc. Ly do co Lan chot: giang lai
luon kem dap an chuan, cho hoi tu do thi hoc sinh bam luot ca de de lay
loi giai ma khong chiu nghi.

Chan o HAI TANG, khong chi lam mo nut:
- giao dien: veBangHoiDeCu() dat disabled khi hoi_duoc = false
- may chu: gia_su_service.hoi() goi _cac_cau_da_lam(), chua lam thi
  GiaSuError va KHONG goi mo hinh, KHONG tru luot

Chan o giao dien thoi la vo nghia: ai cung goi thang API duoc.

Cau da lam nhung khong co loi giai mau (vd cau tu luan) cung mo.

## Prompt CHV_Fun - 4 cho sua

Co Lan gui nguyen ban dang chay tren n8n. Da kiem tra va tim ra LOI THAT:

1. THU TU XET (loi that): chu "bai" nam trong tu khoa Rule 1 (tao de),
   nhung "giai cho toi BAI 3" cung chua chu do. Prompt khong noi rule nao
   xet truoc -> mo hinh tu quyet moi lan mot kieu, co lan tra JSON hong ->
   roi vao fallback. Day chinh la hien tuong "bai cho toi bai 3" co Lan
   thay. Nay them muc THU TU XET tuong minh: Rule 4 > 6 > 7 > 5 > 2 > 3 > 1.
2. XUNG HO THEO VAI TRO: chat.py gui vai_tro tu v2.55 nhung prompt khong
   dung -> giao vien vao chat van bi goi la "ban".
3. Quy tac ki thuat cho tra_loi: xuong dong that lam vo JSON -> phai \n.
4. Rule 5 + Rule 6 chi duong sang gia su AI (ca 2 duong vao).

data/prompts/CHV_Fun.md nay la BAN CHINH THUC, khong con lech voi n8n.

## Viec co Lan phai lam tren n8n

- Dan prompt moi vao node CHV_Fun.
- Sua o Prompt (User Message) cua node CHV_Fun thanh 2 dong:
  "Vai tro nguoi hoi: {{ $json.body.vai_tro }}" + "Tin nhan: {{ $json.body.message }}"
  Khong sua thi muc "Xung ho theo vai tro" vo tac dung.

## Tep

Moi: (khong)
Sua: app/services/gia_su_service.py (liet_ke_cau_de_gan_nhat, TEN_PHAN,
_cac_cau_da_lam, chan trong hoi()), app/routers/gia_su.py
(GET /api/giasu/de-gan-nhat), app/templates/chat/chat.html (2 nut, bang
chon cau, renderLatexText), data/prompts/CHV_Fun.md (viet lai toan bo),
docs/05, docs/06, docs/23

## Hai loi tu bat duoc luc viet giao dien

- chat.html KHONG co ham renderLatexText (lam_bai.html moi co) - loi giai
  chuan co \textbf{} se hien ra chu tho neu khong them.
- addAIMessage() KHONG tra ve element nen khong the .remove() de go tin
  nhan "dang cho" - phai dung addTyping()/removeTyping() co san.

## Bai kiem tra

tests/test_gia_su.py len 36 bai (them 9):
- chua nop bai -> khong hoi duoc, KHONG goi mo hinh, KHONG tru luot
- da nop cau khac nhung chua nop cau nay -> van bi chan
- liet ke chia dung 4 phan, dung thu tu, bo phan rong
- cau chua lam -> hoi_duoc = false
- cau da lam nhung khong co loi giai -> hoi_duoc = false
- GET /api/giasu/de-gan-nhat can dang nhap

Tong 72 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.62 - 2026-09-18

## Go hoi bai trong chat -> mo bang chon cau, khong goi n8n

Hoc sinh vua NOP BAI xong (ket qua cham con hien ngay phia tren trong
cung hoi thoai), go "toi khong hieu bai 1". He thong tra loi: hay TAO DE,
lam xong nop bai, roi bam nut hoi. Trong khi em ay vua lam xong.

Loi cua TA chu khong phai cua prompt: CHV_Fun khong co cach nao biet hoi
thoai nay da co de - no chi doc moi cau chu. May chu thi biet chac:
conversation_id -> de gan nhat -> da nop bai chua.

## Chan ngay o chat.py TRUOC khi goi n8n

Hai dieu kien, phai du ca hai:
1. gia_su_service.la_y_dinh_hoi_bai(message) - bieu thuc chinh quy
2. gia_su_service.co_de_da_nop_bai(user_id, conversation_id)

Du ca hai -> tra {"type": "mo_bang_gia_su"}, KHONG goi n8n (tiet kiem
tron mot luot goi mo hinh). Frontend mo bang PHAN I/II/III/IV de hoc sinh
bam dung cau.

## CO Y KHONG DOAN SO CAU

Co Lan chot. "Bai 1" co the la cau 1 cua de, cung co the la bai 1 trong
sach. Doan sai thi GIANG NHAM CAU - te hon nhieu so voi bat hoc sinh bam
them mot nut. Nhan ra y dinh thi mo bang, de chinh em ay chi dung cau.

## Khong duoc chan nham

la_y_dinh_hoi_bai loai san "huong dan SU DUNG", "cach TAO DE", "TINH
NANG" - nhung cau do thuoc Rule 5 (help) cua CHV_Fun.
co_de_da_nop_bai NUOT MOI LOI: Supabase hong thi tra False de di duong
cu, khong bao gio chan nham vi mot loi doc du lieu.
Hoi thoai chua co de nao -> van de CHV_Fun tu choi nhu cu, luc do dung.

## Bai kiem tra

tests/test_gia_su.py len 60 bai (them 24):
- 9 cau PHAI nhan ra (gom 2 cau that cua hoc sinh trong anh co Lan gui)
- 8 cau KHONG duoc nhan nham (help, tao de, xin loi giai...)
- co_de_da_nop_bai: chua co de / co de chua nop / da nop / Supabase hong
- POST /chat: mo bang va KHONG goi n8n (dem so lan _goi_n8n, phai = 0)
- POST /chat: hoi thoai chua co de -> VAN goi n8n
- POST /chat: "tao de lop 10 chuong 1" -> VAN goi n8n (khong chan nham)

Tong 96 bai, deu xanh.

## Van con: loi tu choi lap nguyen van 2 lan

Prompt yeu cau "moi lan doi cach dien dat" nhung mo hinh mien phi bam
khuon mau. Chua sua, khong gap - va sau ban nay thi truong hop do it xay
ra han vi da chan truoc khi toi CHV_Fun.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.64 - 2026-09-19

## Bang anh xa bai <-> tep ly thuyet (chuan bi cho gia su muc B)

Co Lan da dua 87 tep .tex ly thuyet vao data/ly_thuyet/ (3,1 MB, khong
co .git long nhau, khong tep nang). Cau truc ben trong RAT nhat quan:
\section{TEN BAI} -> \subsection{LY THUYET CAN NHO} -> \subsubsection.

## Vi sao phai viet tay bang anh xa

Khop tu dong theo ten bai chi duoc 11/28 tep lop 10. KHONG phai tep dat
sai - ma cach chia bai cua tai lieu khac cach chia cua chuong trinh, va
quan he la NHIEU-NHIEU:
- L10_C1_B2 "Tap hop va cac phep toan tren tap hop" = 0D1-CD2 + 0D1-CD3
- L10_C4_B8 "Cac phep toan tren vecto"  = 0H4-B2 + 0H4-B3 + 0H4-B5
- L10_C7_B18 "Duong thang trong mp toa do" = 0H7-B1 + 0H7-B2
Vai cho chi khac chu: "NHI THUC NIU-TON" / "Nhi thuc Newton".

-> data/ly_thuyet/anh_xa.json, viet mot lan, canh bang bai kiem tra.

## PHAT HIEN QUAN TRONG: curriculum lop 11 va 12 con RONG

data/curriculum/toan11/ va toan12/ khong co tep nao. Toan he thong moi
co 23 bai LOP 10.

  Khoi 10: 28 tep ly thuyet - 23 bai curriculum -> anh xa DU CA 23 BAI
  Khoi 11: 33 tep ly thuyet - 0 bai            -> chua gan vao dau duoc
  Khoi 12: 26 tep ly thuyet - 0 bai            -> chua gan vao dau duoc

59/87 tep chua dung duoc, KHONG phai vi tep sai ma vi chua co cau hoi
nao de gan. Lam ngan hang 11/12 xong thi bo sung vao anh_xa.json la chay.

## Cat phan nao cua tep - DA DO, khong doan

Do that tren 23 bai lop 10:
  Ca tep, trung binh            : 34.079 ki tu (~8.500 token)
  CHI muc ly thuyet, trung binh :  4.534 ki tu (~1.130 token)
  Chi ly thuyet, dai nhat       : 14.576 (L10_C4_B8, gop 3 tep)
  Chi ly thuyet, ngan nhat      :    914 (L10_C2_B4)

-> Nap ca tep la KHONG DUOC voi tai khoan mo hinh mien phi. Cat lay dung
muc ly thuyet thi duoc, va chi nap khi hoc sinh bam "Em van chua hieu".
Muc A giu nguyen nhe nhu cu.

## Bai kiem tra

tests/test_anh_xa_ly_thuyet.py - 7 bai, canh dung nhung cho de hong am
tham (doi ten tep, go nham ma bai, them bai moi vao curriculum ma quen
bo sung ly thuyet). Khong can mang, khong can chay web.

Tong 103 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.65 - 2026-09-24

## Loc lenh LaTeX rieng cua ex_test truoc khi dua ra web

Co Lan gap: khoi "LOI GIAI CHUAN CUA THAY/CO" in ra dong chu vang
    Unknown environment 'itemchoice'
ngay giua man hinh hoc sinh.

Nguyen nhan: loi giai do Python sinh la LaTeX danh cho goi ex_test (de
bien dich PDF). MathJax tren web khong biet cac moi truong rieng cua goi
do nen in thang loi ra. Dua nguyen van sang mo hinh cung khong hay: no
tuong \begin{itemchoice} la mot phan cua de bai.

## Sua o NGUON, khong sua o giao dien

gia_su_service._lam_sach_latex(): giu DANH SACH TRANG cac moi truong
MathJax that su hieu (align, cases, array, pmatrix, equation...); moi
thu khac thi BO CAP \begin{}/\end{} nhung GIU NGUYEN RUOT. Bo han cac
lenh chi co nghia khi bien dich PDF: \loigiai \choice \choiceTFt \True
\shortans \immini \hetde \tieude \chantrang.

Sua o Python (mot cho) thay vi o renderLatexText (hai cho: chat.html va
lam_bai.html) - va nho vay CAU LENH gui sang mo hinh cung sach theo.

## Bai kiem tra

Them 11 bai: bo dung cac lenh ex_test, GIU nguyen 7 moi truong MathJax
hieu, ruot khong duoc mat, cong thuc thuong khong bi dung den, va mot
bai di duong day du (dapan_json -> lay_ngu_canh_cau -> phai sach).

Tong 114 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.66 - 2026-09-24

## Nut "Kiem tra ket noi n8n" - tra loi mot loi KHONG NHIN THAY DUOC

Co Lan mat nhieu ngay vi node CHV_GiaSu khong nap lenh_he_thong: mo hinh
khong co de bai nen TU BIA ngu canh (tam li hoc hanh vi, phan doan thi
truong, phan phoi ngan sach cho cac tinh). Nhin tu ngoai chi thay "AI tra
loi lung tung", muon biet hong o dau phai mo Executions cua n8n doc JSON.

/gv/gia-su nay co nut "Kiem tra ket noi n8n": gui sang n8n mot cau lenh
chua MA NGAU NHIEN 6 ki tu, bao mo hinh doc lai ma do.
  Ma quay ve     -> lenh_he_thong CO toi mo hinh
  Khong quay ve  -> KHONG toi -> chi thang ra o System Message phai sua

Ma phai NGAU NHIEN moi lan: ma co dinh thi mo hinh co the nho tu luot
truoc va tra dung du lenh khong toi (co bai kiem tra canh diem nay).

Bon ket luan: ok | khong_nap_lenh | khong_goi_duoc | chua_cau_hinh, moi
cai kem mot cau tieng Viet noi ro sua o dau.

Phep thu KHONG tru luot cua hoc sinh nao va KHONG ghi vao nhat ki.

## Sua \itemch -> xuong dong

Cau Dung/Sai dung \itemch danh dau tung y a) b) c) d). Ban v2.65 chua loc
lenh nay nen no hien ra chu tho giua man hinh. Xoa han thi 4 y dinh lien
thanh mot doan dai kho doc -> doi thanh XUONG DONG: vua sach vua de doc.

## Bai kiem tra

Them 7 bai: itemch thanh xuong dong va giu nguyen cong thuc; 4 ket luan
cua tu_kiem_tra (gom dung cau tra loi that co Lan gap lam du lieu thu);
khong tru luot; ma khac nhau moi lan.

Tong 127 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.67 - 2026-09-24

## Khoi "Loi giai chuan" nay co ca DE BAI

Co Lan: "gio nhin giai ma ko the nho de". Dung - khoi do ban dau chi co
dap an va loi giai, hoc sinh doc ma khong biet dang giai cai gi, nhat la
khi hoi lai mot de da lam tu luc nao.

API tra them de_bai_python. Giao dien ve theo dung thu tu trong tep .tex
cua co:
    DE BAI   <- than cau + cac phuong an A/B/C/D (hoac 4 y a,b,c,d)
    DAP AN
    LOI GIAI
De bai dat trong khung nen trang rieng o tren cung, tach khoi loi giai.

Du lieu DA CO SAN tu dau: _mo_ta_de_bai() van dung no de dua vao cau lenh
cho mo hinh, chi la chua tra ra cho giao dien. Khong phai doc them gi.

## renderXuongDong() - dung nham voi renderLatexText()

Loi giai chuan co xuong dong THAT (\n): de bai nhieu dong, va 4 y Dung/Sai
sau khi \itemch doi thanh xuong dong. renderLatexText() chi doi \\ cua
LaTeX thanh <br>, KHONG doi \n - dung no thi tat ca dinh lien mot doan.
renderXuongDong() boc ngoai va lam not viec do. Sua o ca 2 trang.

## Bai kiem tra

Them 4 bai: hoi() tra ve de bai kem phuong an; che do khong AI cung co de
bai; duong du phong (het luot/AI hong) VAN co de bai; cau Dung/Sai liet ke
du 4 y a) b) c) d).

Tong 131 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.68 - 2026-09-25

## Duong di quay lai khu giao vien + hien email dang dang nhap

Co Lan dang nhap tai khoan giao vien, vao thang Chat AI roi MAC KET:
thanh ben khong co muc nao dan sang /gv. Tu /gv thi co muc "Chat AI" de
di sang, nhung chieu nguoc lai khong co gi - muon quay lai phai tu biet
ma go dia chi.

Co Lan: "chi la khong co duong dan quay lai khu quan ly cua gv".

## Da sua

- Thanh ben Chat AI them muc "Khu giao vien" -> /gv, dat tren Dang xuat.
- LOI PHAT HIEN KEM: muc "Thong ke nang luc (GV)" truoc day hien cho CA
  HOC SINH - bam vao la bi chan 403. Vua kho hieu vua lo ra co khu rieng.
  Nay ca 2 muc deu boc trong {% if la_giao_vien %}.
  la_giao_vien da co san trong context cua /chat tu v2.55.
- _base_gv.html hien EMAIL canh nut Dang xuat: profiles co 2 tai khoan
  trung ten "Lan Mai" cung lop C9 (mot giao_vien, mot hoc_sinh), nhin ten
  khong biet dang la ai - ma do chinh la cau hoi dau tien khi bi chan.

## _ngu_canh_chung(user)

Gom thu phai co o MOI trang /gv, moi route trai vao context cua minh.
test_moi_trang_gv_deu_truyen_email DOC CHINH MA NGUON va bat loi neu co
trang nao quen - de lan sau them trang moi khong sot.

## Bai kiem tra

Them 4 bai: giao vien thay loi quay lai; hoc sinh KHONG thay muc nao cua
giao vien; thanh GV hien email; moi trang /gv deu truyen email.

Tong 135 bai, deu xanh.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.69 - 2026-09-26

## Cap nhat SKKN theo he thong da thay doi (13/09 -> 26/09)

Ban SKKN viet ngay 13/09, tu do den nay he thong da di rat xa (v2.45 ->
v2.68). Cap nhat lai cho khop.

## Diem moi thu 6 (02_mo_dau)

"Tro giang tri tue nhan tao bi khoa vao loi giai cua giao vien" - day la
dong gop co gia tri chia se nhat, vi no tra loi cau hoi ma nhieu thay co
e ngai: lam sao chac chan may khong day sai cho hoc sinh.

## Hai giai phap moi (05_giai_phap)

Giai phap 7 - Khu lam viec rieng cho giao vien: ra de nhieu ma theo cau
truc 4 phan cua Bo, tai ma nguon .tex, quan li lop, thong ke. Nhan manh
bai hoc "an nut tren giao dien khong phai la phan quyen".

Giai phap 8 - Tro giang bi khoa vao loi giai: van de dat ra (mo hinh tinh
so hoc hay sai va sai tu tin), loi the cua he thong (dap an da co san tu
truoc), BA LOP KHOA (Bang 8 moi), quy tac bao trum "khong co loi giai
chuan thi khong goi may", dieu kien phai nop bai roi moi duoc hoi, han
muc luot.

## Bang 6 - them 6 lan cai tien (15-20)

Lo hong phan quyen /gv/*; khoa co so du lieu dung chung; chon 4 ma de chi
ra 1; de giao vien khong luu duoc suot 8 tieng ma khong ai biet; tro giang
tra loi lac de vi o nap cau lenh bo trong; hoc sinh vua nop bai go "khong
hieu bai 1" lai bi bao di tao de.

Doan ket luan sau bang viet lai: tu 2 nhom loi thanh 3 nhom, them nhom
"nham viec an di voi viec chan lai". Nhan manh bai hoc ve loi HONG AM
THAM - loai ton thoi gian nhat.

## 08_huong_phat_trien - viet lai

Bo muc "Khu lam viec rieng cho giao vien" va "Hoan thien tai khoan giao
vien" (DA XONG, chuyen sang Giai phap 7). Them muc "Tro giang muc B" kem
so lieu that da do (87 tep li thuyet, bang anh xa nhieu-nhieu, ca tep
34 nghin ki tu vs rieng li thuyet 4,5 nghin).

## 06_huong_dan - them buoc moi

Hoc sinh: Buoc 8 hoi lai thay/co AI (3 dieu can biet, trong do co "neu 2
phan noi khac nhau thi TIN KHUNG XANH").
Giao vien: Buoc 7 doc nhat ki tro giang + nut Kiem tra ket noi n8n.
Bang 7 them 4 dong loi thuong gap moi.

## Anh

Them 4 anh: 20-khu-lam-viec-giao-vien, 21-gia-su-ai, 22-nhat-ki-gia-su,
23-nut-hoi-lai-de-cu. Ban dau danh so 16-19 bi TRUNG voi anh da co, da
doi lai. Tong 19 anh can chup.

## Bien dich thu

latexmk -xelatex chay duoc, ra 52 trang. Loi duy nhat la thieu font Times
New Roman - do may ao Linux khong co font do, may Mac cua co Lan co san.
Da them skkn/skkn.pdf vao .gitignore (co tu bien dich tren may).

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.70 - 2026-09-27

## SKKN: thiet ke thuc nghiem su pham, tinh cap thiet, phieu khao sat

Co Lan se khao sat diem 2 lop truoc/sau khi dung web:
  Lop doi chung  : 10C9 nam hoc 2025-2026
  Lop thuc nghiem: 10C9 nam hoc 2026-2027
Ly do: khoi 10 co chi day 2 lop la chuyen Toan va chuyen Dia, khong the
lay lop nay lam doi chung cho lop kia (khac han ve dinh huong va nang
luc), nen phai so cung mot lop chuyen Dia o hai nam hoc lien ke.

## DIEM YEU PHAI VA - da noi thang trong bai viet

Day la DOI CHUNG LICH SU: hai nhom hoc sinh khac nhau, khong cung thoi
diem. Hoi dong se hoi "lam sao biet chenh lech la do web chu khong phai
do lua nay gioi hon". Ba cach khac phuc, viet ro trong muc moi:
1. Chung minh 2 lua tuong duong dau vao bang DIEM THI VAO 10 MON TOAN
   (de chung toan tinh, cham tap trung, khong phu thuoc co Lan).
2. So dau ra SAU KHI DA KHU anh huong dau vao (ANCOVA).
3. Chay song song thiet ke thu hai: TRUOC-SAU trong chinh lop thuc
   nghiem - khong dinh van de khac lua.

VIEC GAP da bao co Lan: lay diem thi vao 10 cua lua 2025-2026 ngay khi
con tra duoc trong ho so cu.

## Da viet

07_hieu_qua: muc "Thiet ke thuc nghiem su pham" - 2 nhom so sanh, ly do
chon 2 lop khac nam (noi thang rang buoc thuc te), diem yeu + 3 cach
khac phuc, Bang 12 cac phep kiem dinh, Bang 13 ket qua xu li thong ke
(bang trong de co dien).

Phep kiem dinh: Shapiro-Wilk (n<50), t-test doc lap, Mann-Whitney U,
t-test ghep cap, ANCOVA, Cohen's d, Cronbach's alpha. Nhac co Lan BAO CA
p LAN d: voi si so ~30, p co the khong dat 0,05 du chenh lech co y nghia
thuc tien.

02_mo_dau: muc "Tinh cap thiet" (3 ly do) + "Tinh kha thi". Ly do cap
thiet nhat: tri tue nhan tao DA VAO LOP HOC ROI du nha truong co chuan bi
hay khong - van de khong phai "co nen dung hay khong" ma "dung loai co
kiem soat hay de cac em tu dung loai khong kiem soat".

04_thuc_trang: Bang 3 them 4 tieu chi (nhieu ma cung don vi kien thuc,
lay duoc ma nguon .tex, giang lai cau lam sai, LOI GIANG BI KHOA VAO DAP
AN DA KIEM CHUNG) + doan binh luan 3 khac biet ro nhat.

skkn/phieu_khao_sat.tex: tep DOC LAP, 3 trang (2 trang phat cho HS + 1
trang huong dan cho GV). Likert 5 muc, 4 nhom (thai do, tu tin, thoi quen
tu luyen, cam nhan ve he thong) + 4 cau tra loi ngan. Dung 2 lan: dau nam
va cuoi dot.

## Danh lai SO BANG

Bang "Ba lop khoa" (v2.69) chen giua Bang 4 va 5 nhung danh nham la 8 ->
danh lai toan bo: nay lien mach 1-14, tham chieu trong van da khop.

## Bien dich thu

Ca 2 tep sach loi (thu voi font thay the TeX Gyre Termes vi may ao khong
co Times New Roman): skkn 66 trang, phieu_khao_sat 3 trang.

## Loi cua Claude trong luc lam

Xoa nham phieu_khao_sat.tex bang ky tu dai dien "phieu_khao_sat.*" khi
don tep tam. Da viet lai ngay va bien dich kiem chung. Bai hoc: khong
dung dai dien de xoa khi trong thu muc co ca tep nguon lan tep tam.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.71 - 2026-09-27

## SKKN: cat ngan, dan link + QR thay cho in day du

Co Lan yeu cau: bo diem thi vao 10; SKKN ngan gon, tam 50 trang; tap trung vao
phan cot loi la tao web; code Python / json / diff chi neu vai cai co ban roi
dan link + QR len GitHub cho giam khao tu vao coi.

## Ket qua do (tat ghi chu do, la ban se in nop)

  Truoc      : 66 trang
  Sau        : 55 trang  (14pt, gian dong 1,5 - dung quy dinh)
  Neu 13pt   : 35 trang

LUU Y QUAN TRONG: 22/23 cho chen anh hien con la O DO (chua chup). Khi dan anh
that vao, tai lieu se DAI THEM khoang 2,5-3 trang -> ban 14pt se ra ~58 trang.
Muon ve dung ~50 thi phai giam so anh xuong khoang 12 cho.

## Da cat gi

Qua trinh cai tien: 20 dong -> 7 dong tieu bieu, dan QR sang docs/16_CHANGELOG.md
Loi thuong gap    : 14 dong -> 6 dong, dan QR sang docs/
Huong phat trien  : 6 muc con -> 6 doan van ngan gon
Don yeu cau 5.1-5.2: gon lai (than bai da trinh bay day du)
Co so li luan     : gon can cu phap li, bo muc (e) trung voi Mo dau
Thuc trang        : gon ba doan phan tich nhom 1/2/3
Vai tro tro li AI : 3 doan -> 2 doan
Muc tieu cu the   : bo 4 tieu de nhom rieng, gop thanh 1 danh sach 7 muc

## KHONG cat (dung y co Lan)

Huong dan su dung giu day du - co Lan noi "noi dung van phai neu ro, y dinh cua
toi phai co du (doi voi ban hoan chinh)".
Giai phap 1-8 giu nguyen - day la phan cot loi tao web.

## Ma QR

Them goi qrcode. Lenh moi \linkqr{duong-dan}{mo ta}: o co ma QR ben trai,
duong dan ben phai. QR do LaTeX sinh ra TU CHINH duong dan in ben canh nen ma
va duong dan khong the lech nhau - khong con phai dan anh QR thu cong.

5 cho co QR: dia chi web (muc Huong dan), ma nguon + so tay (Giai phap 9),
nhat ki cai tien (Qua trinh cai tien), bang loi day du (Huong dan), va Phu luc
muc B (4 ma QR: he thong dang chay, ma nguon, ngan hang cau hoi Python, so tay).

## Phu luc viet lai

Phan A: 4 phu luc in kem (phieu khao sat, 1 de hoan chinh + loi giai, 2 ma de
cung cau truc, ma tran chi tiet).
Phan B: 4 ma QR de hoi dong quet dien thoai xem truc tiep + bang tai khoan dung
thu cho hoi dong. KHONG in code Python vao bao cao (L10_C1.py co 7855 dong).

## Thiet ke thuc nghiem - viet lai theo huong co Lan chon

Bo hoan toan phan dua vao diem thi vao 10 va ANCOVA. Thay bang 4 co so bao dam
tuong dong: cung la lop chuyen Dia, cung mot giao vien day, cung don vi kien
thuc + cung ma tran trong de, cung thoi diem trong nam hoc.

Van giu mot cau noi thang rang day la doi chung lich su nen khong loai tru het
duoc khac biet giua hai lua - va khac phuc bang thiet ke thu hai chay song song:
so TRUOC-SAU ngay trong lop thuc nghiem (so chinh cac em voi chinh minh, khong
ai bat loi duoc ve chuyen khac lua). Bang 12 rut tu 7 xuong 5 phep kiem dinh
(bo ANCOVA va dong kiem dinh dau vao). Bang 13 rut con 3 dong.

## Sua loi phat hien trong luc lam

1. Loi danh may trong 05: mot cho viet "extit" (thieu dau gach cheo) - da sua.
2. 02_mo_dau con ghi "khu lam viec rieng cho giao vien" o muc DANG XAY DUNG,
   nhung Giai phap 7 lai noi da xong -> mau thuan, hoi dong doc se bat. Da
   chuyen sang muc DA HOAN THANH.
3. Bon anh bi chen HAI LAN trong cung bao cao (01, 02, 07, 15). Da bo ban lap
   trong muc Huong dan, thay bang dan chieu \ref den hinh goc. Them nhan tu
   dong cho moi hinh de dan chieu duoc.
4. Do rong anh khong nhat quan (0.92 / 0.9 / 0.85 / 0.75 / 0.7) - chuan hoa ve
   0.68 het.
5. Bo ngat trang giua cac muc con trong Phan II (tiet kiem 3 trang, khong mat
   chu nao).

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.72 - 2026-09-27

## Lenh got tat day code: scripts/day.sh

Ly do: Claude commit duoc nhung KHONG day len GitHub duoc - thong tin dang nhap
GitHub nam trong Keychain cua may Mac, may ao Claude lam viec khong voi toi
(da thu: "could not read Username for https://github.com"). Nen phan vai la
Claude sua tep + commit + ghi so tay, co Lan day len.

Viet script de co Lan khoi phai nho chuoi lenh:

    day          -> day len GitHub
    day web      -> day len GitHub + cap nhat VPS + kiem tra web

Chi tiet tung buoc: xem docs/14_DEPLOYMENT.md

## Diem quan trong nhat cua script

Truoc khi day, script fetch roi so may nay voi GitHub. Neu GITHUB MOI HON thi
DUNG LAI va nhac pull truoc, khong co day de. Truoc day co Lan tung gap tinh
huong nay va mat thoi gian go xung dot.

Va: script chi bao "xong" sau khi curl that su thay web tra ve 200/302/307.
Restart dich vu thanh cong ma web loi van la loi - khong duoc bao xong.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.73 - 2026-09-27

## Soat curriculum + mapping lop 10, va 5 loi

Doi chieu voi Chuong trinh GDPT mon Toan 2018 (Thong tu 32/2018/TT-BGDDT),
phan lop 10 (tr.79-88).

## Loi 1 (NANG NHAT) - 4 ham da viet xong ma he thong khong dung duoc

question_selector_service chi chon cau TU MAPPING. Ham Python khong co ten
trong mapping thi may khong bao gio nhin thay. Bon ham sau da viet xong, chay
duoc, nhung quen khai vao mapping nen la ma chet:

    L10_C1_B1_TH003_TL_A     Tu luan
    L10_C1_B2_NB017_SA_C     Tra loi ngan
    L10_C1_B2_TH019_TL_A     Tu luan
    L10_C1_B2_VD021_TL_A     Tu luan

Dang chu y: ca bon deu la SA va TL - dung cai o co Lan than la mong nhat trong
SKKN. Da khai vao mapping, dung duoc ngay, khong phai viet them gi.

## Loi 2 - ham L10_C1_B2_NB017_SA_C thieu duoi _01

generator_service._find_variant_functions tim theo mau ^<id>_\d{2}$ nen ham
khong co duoi _01 se khong bao gio duoc tim thay. Da doi ten thanh
L10_C1_B2_NB017_SA_C_01. Neu chi khai vao mapping ma khong sua ten thi van
hong - phai sua ca hai.

## Loi 3 - mot chu A thua trong mapping

L10_C1_B2_NB017A_MC_A -> L10_C1_B2_NB017_MC_A. Dong nay dang tro vao mot ma
curriculum khong ton tai va mot ham Python khong ton tai.

## Loi 4 - curriculum thieu VD014

Mapping da co VD014_MC_A va VD014_SA_A (co Lan chuyen tu TH sang VD vi muc TH
kho ra de) nhung quen them ban ghi ben curriculum. Da them L10_C1_B1_VD014.

## Loi 5 (NANG) - thuat toan chua chan trung don vi kien thuc

Quy uoc cua co Lan: cung don vi kien thuc thi cung so, de ma tran khong lay ca
hai muc ma de bi trung dang. Nhung _chon_curriculum_id dang ghi nho theo ID
DAY DU, ma TH021 va VD021 la hai ID khac nhau -> van lay ca hai duoc. Y dinh
cua co Lan chua he duoc thuc hien.

Da them ham _don_vi_kien_thuc() bo phan muc do khoi ma de lay khoa, va doi
da_dung sang dung khoa do. Chi tiet: docs/04_ID_STANDARD.md.

## Ngoai ra

- NB017 bi mat phan trong ngoac cua van ban Bo ("tap con, hai tap hop bang
  nhau, tap rong va biet su dung cac ki hieu con, chua, rong"). TH018 ngay
  duoi lai giu nguyen ngoac. Da lay lai cho NB017 va ghi vao scope. Phan trong
  ngoac chinh la hang rao pham vi - mat no thi hang sinh cau hoi khong biet
  duoc phep hoi toi dau.
- Bo hau to chu cai o 3 cho dung sai quy uoc: VD084A -> VD084, VD099A -> VD099,
  VD100A -> VD100.
- VD099A con sai them: id ghi VD nhung truong MucDo lai ghi TH, thanh ra trung
  y het TH099. Da sua MucDo thanh VD.

## Kiem thu

142 bai test qua (them tests/test_don_vi_kien_thuc.py, 7 bai).
test_supabase.py khong chay duoc tren may ao (can mang ra Supabase).

Ba lop du lieu cua chuong 1 gio khop het: 17 yeu cau can dat <-> 34 dang cau
hoi <-> 46 ham Python, khong con mo coi chieu nao.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.74 - 2026-09-27

## Soat xong curriculum lop 10 voi van ban Bo

Doi chieu tung dong 126 yeu cau can dat trong data/curriculum/toan10/ voi
Thong tu 32/2018/TT-BGDDT phan lop 10 (tr.79-88).

Ket qua: 24 cho THIEU, 9 cho LECH. Chi tiet tung dong kem muc do de xuat:
docs/24_SOAT_CURRICULUM_L10.md

CHUA them dong nao vao curriculum - cho co Lan duyet, vi viec dat muc do cho
tung yeu cau la chuyen mon cua giao vien.

## Mot so cho dang chu y

C8: Bo tach HAI gach dau dong - "Tinh duoc so cac hoan vi, chinh hop, to hop"
va "... bang may tinh cam tay". Curriculum chi co ban may tinh cam tay. Ban
tinh bang cong thuc moi la ban ra de duoc.

C7: khong co ban ghi nao cho "Mo ta duoc phuong trinh tong quat va phuong
trinh tham so cua duong thang" - day la cau nhan biet ra de nhieu nhat cua
bai 18.

C3: "Mo ta duoc cach giai tam giac" bi bo. Bo viet chung mot gach dau dong voi
ve "van dung vao bai toan thuc tien"; co Lan moi tach ve sau.

C6 thieu nhieu nhat (11 cho), gom ca "tinh xac suat cua bien co doi" va "cac
tinh chat co ban cua xac suat".

C7 dang ghi hoc_phan la "Dai so va Mot so yeu to giai tich" trong khi Bo xep
"Phuong phap toa do trong mat phang" vao HINH HOC VA DO LUONG.

## Viec phai quyet truoc khi them

Them 25 ban ghi moi vao giua se pha tinh lien tuc cua so theo chuong. Day la
CO HOI CUOI CUNG de danh lai so re: C2-C8 hien chua co mapping va chua co ham
Python nao tro vao. Khi da viet ham Python roi thi danh lai se lam mo coi toan
bo. Xem muc C trong docs/24_SOAT_CURRICULUM_L10.md.

## Dinh chinh mot cau Claude noi sai

Claude tung noi voi co Lan rang bai so "nhay B12, B16, B20 vi do la bai tap
cuoi chuong". SAI. Ca 23 bai deu co ban ghi: B12 Phuong trinh quy ve phuong
trinh bac hai, B16 Bien co va dinh nghia co dien cua xac suat, B20 Ba duong
conic. Claude doc nham vi luc do chi xem 14 ban ghi dau moi tep.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.75 - 2026-09-27

## Curriculum lop 10: bo sung 28 yeu cau, danh lai so C2-C8

Co Lan chot: curriculum la nen, phai dung va du truoc; mapping va ham Python
bo sung dan sau.

    Truoc: 126 yeu cau can dat
    Sau  : 154 yeu cau can dat, so lien mach 001-155

## 28 ban ghi moi (theo dung van ban Bo)

C3 +1   Mo ta duoc cach giai tam giac
C4 +1   Su dung vecto giai thich hien tuong Vat li, Hoa hoc
C5 +4   mo hinh thuc te dan den khai niem ham so; VD ham so vao bai toan thuc
        tien; lap bang bien thien; tinh chat co ban cua Parabola (dinh, truc
        doi xung)
C6 +12  xac dinh so gan dung voi do chinh xac cho truoc; xac dinh sai so tuong
        doi; may tinh cam tay voi so gan dung; phat hien so lieu khong chinh
        xac; hai cho "chi ra ket luan nho y nghia so dac trung"; moi lien he
        thong ke voi mon khac; dinh nghia co dien cua xac suat; nguyen li xac
        suat be; so do hinh cay cho thi nghiem lap; tinh chat co ban cua xac
        suat; xac suat cua bien co doi
C7 +8   do dai vecto tu toa do hai dau mut; giai tam giac bang toa do; toa do
        vecto vao bai toan thuc tien; MO TA phuong trinh tong quat va tham so;
        lien he do thi ham bac nhat va duong thang; duong tron vao bai toan
        thuc tien; nhan biet phuong trinh chinh tac ba duong conic; van de
        thuc tien gan voi conic
C8 +2   van dung quy tac cong/nhan trong tinh huong thuc tien; TINH SO HOAN VI,
        CHINH HOP, TO HOP BANG CONG THUC (truoc do chi co ban may tinh cam tay)

## Sua cho lech

- C7 hoc_phan: "Dai so va Mot so yeu to giai tich" -> "Hinh hoc va Do luong".
  Bo xep Phuong phap toa do trong mat phang vao HINH HOC VA DO LUONG (tr.83).
- C5 TH057: "bang bien thien" -> "bang gia tri" theo dung chu cua Bo, va them
  mot ban ghi rieng cho bang bien thien (la cach trinh bay cua SGK, van ra de).
- C2 VD028: lay lai chu "thuc tien"; scope sua thanh "cuc tri" (Bo noi cuc tri,
  truoc do thu hep con "gia tri lon nhat").
- C5 TH066/TH067: cong thuc viet lai bang LaTeX thay vi ta bang loi.
- C7 VD104A: scope bi chep nham tu VD104, da sua.

## Danh lai so C2-C8

C1 GIU NGUYEN 001-021 (dang co mapping va 46 ham Python tro vao - danh lai la
mo coi het). Tu C2 danh lai lien mach:

    C2 022-028   C3 029-036   C4 037-053   C5 054-073
    C6 074-111   C7 112-138   C8 139-155

Cac cap cung don vi kien thuc van giu chung mot so: 014, 021 (C1), 095 (C6),
121, 122 (C7).

Lam duoc vi C2-C8 chua co mapping va chua co ham Python nao tro vao. Sau nay
co roi thi khong danh lai duoc nua.

Bang doi chieu ma cu -> ma moi: 137 ma (khong luu vao kho, chi dung trong lan
sua nay vi khong co gi tro vao cac ma do).

## Kiem tra sau khi sua

Khong trung ID; du 15 truong; so lien mach va tang dan theo tung chuong; thu
tu bai tang dan; cac cap cung don vi kien thuc con nguyen; ba lop cua C1 van
khop; 142 test qua.

## CHUA lam mapping C2-C8 - ly do

/danh-sach-chuong tinh co_du_cau BANG CACH DEM SO DONG MAPPING. Neu them
mapping cho C2-C8 ma chua co ham Python thi web se bao voi hoc sinh la cac
chuong do DA SAN SANG, hoc sinh chon vao, va vi ra de that chay voi
cho_phep_thieu=False nen se VO CA DE chu khong phai thieu vai cau.

Phai sua co_du_cau thanh "co it nhat mot dang DA CO HAM PYTHON" truoc, roi moi
them mapping duoc. Xem version sau.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.76 - 2026-09-27

## Mapping lop 10 day du + sua cho co the lam vo de

    Truoc: mapping chi co C1 (34 dang)
    Sau  : ca 8 chuong, 259 dang cho 154 yeu cau can dat

C1 34 | C2 13 | C3 17 | C4 25 | C5 31 | C6 61 | C7 51 | C8 27

Moi yeu cau can dat deu co it nhat mot dang. Moi chuong deu co cau Dung/Sai.
Phan bo: 167 trac nghiem, 49 tra loi ngan, 27 tu luan, 16 dung/sai.

## SUA MOT CHO CO THE LAM VO DE THAT

/danh-sach-chuong tinh co_du_cau = "co dong mapping nao khong". Mapping la BAN
KE HOACH, co ca dang chua viet ham. Nen ngay khi them mapping cho C2-C8, web se
bao voi hoc sinh la 8 chuong deu da san sang - hoc sinh chon vao chuong 5, ra
de that chay voi cho_phep_thieu=False, va VO CA DE chu khong phai thieu vai cau.

Da them mapping_service.dem_dang_co_ham(lop, chuong): dem so dong mapping ma
THUC SU co ham sinh trong ngan hang Python. Doc thang tep .py bang van ban,
khong import module (khong keo theo sympy/numpy chi de dem).

/danh-sach-chuong gio tra ve:
    co_du_cau            = so_dang_co_cau_hoi > 0
    so_dang_co_cau_hoi   = so dang da co ham (truong moi, FE dung de hien
                           "da co 34/34 dang" neu muon)

Hien tai: C1 = 34 dang co ham; C2-C8 = 0. Dung su that.

## Y nghia cua thay doi nay

Gio ba lop co vai tro ro rang:
    curriculum  Bo yeu cau gi           154 dong
    mapping     can nhung dang nao      259 dong  <- ban ke hoach
    Python      dang nao da co that      46 ham   <- hang co that

Mapping tro thanh DANH SACH VIEC nhin thay duoc: con 225 dang chua co ham.
Co Lan viet ham den dau, chuong tu mo den do, khong phai sua code.

## Kiem thu

Them tests/test_mapping_curriculum.py (41 bai): moi dong mapping phai tro vao
mot yeu cau co that; content phai khop curriculum; khong trung id; moi yeu cau
co it nhat mot dang; moi chuong co cau Dung/Sai; va co_du_cau phai dem theo ham
Python chu khong phai dong mapping.

Tong 183 bai test qua (truoc: 142).

Bai test cuoi la bay chan hoi quy: neu sau nay ai do doi co_du_cau ve dem dong
mapping thi test do hong ngay.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.77 - 2026-09-27

## Bao THIEU thay vi bao loi

Theo y co Lan: cho nao chua co thi ghi ro THIEU O DAU va MA NAO, roi van ra de
tiep - khong dung ca de lai.

Dong bao trong de gio ghi:
    [THIEU O MAPPING --- ID: L10_C5_B11_TH069_SA_A]
    [THIEU O PYTHON  --- ID: L10_C5_B11_TH069_MC_A]

"Thieu o Mapping" = chua khai dang cau hoi nao cho yeu cau can dat do.
"Thieu o Python"  = da khai dang trong Mapping nhung chua viet ham sinh.

Ket qua chon cau cung mang them hai truong thieu_o va ma_thieu de man hinh
giao vien liet ke duoc danh sach can bo sung.

Mac dinh cho_phep_thieu doi tu False sang True o moi cho (selector, assembler,
blueprint, endpoint /exam) nen khong con truong hop vo ca de nua.

## Curriculum + Mapping lop 11 va lop 12

    Lop 11: 148 yeu cau can dat / 9 chuong / 33 bai | 238 dang mapping
    Lop 12:  58 yeu cau can dat / 6 chuong / 18 bai | 113 dang mapping

Doi chieu tung dong voi Thong tu 32/2018 (lop 11 tr.89-102, lop 12 tr.105-110).
Moi yeu cau deu co it nhat mot dang; moi chuong deu co cau Dung/Sai.

Tong ca ba khoi: 360 yeu cau can dat, 610 dang mapping, 46 ham Python.

## PHAT HIEN QUAN TRONG: PPCT va Curriculum danh so khac nhau

He thong noi PPCT voi Curriculum bang chuoi ma L{lop}_C{chuong}_B{bai}. Hai ben
dang danh so khac nhau nen ma VAN KHOP CHUOI nhung tro vao BAI KHAC - may khong
bao loi, chi lang le lay sai yeu cau can dat.

    L10_C5_B12  PPCT: So gan dung va sai so
                Curriculum: Phuong trinh quy ve phuong trinh bac hai
    L10_C6_B15  PPCT: Ham so
                Curriculum: Cac so dac trung do do phan tan

Hoc sinh chon on den bai "So gan dung" se nhan de "Phuong trinh bac hai".

Chua gay hau qua vi moi chuong 1 lop 10 co ham Python, ma chuong 1 thi hai ben
trung nhau. Nhung ngay khi viet ham cho chuong khac la loi hien ra.

Chua sua gi - can co Lan quyet ben nao la chuan. Phan tich day du:
docs/25_LECH_PPCT_CURRICULUM.md

## Sua bai test ly thuyet

test_moi_bai_trong_curriculum_deu_co_ly_thuyet truoc doi hoi MOI bai trong
curriculum phai co tep ly thuyet - them lop 11, 12 vao la hong ngay. Sua lai:
chi doi hoi voi KHOI DA BAT DAU co tep ly thuyet. Khoi chua co tep nao thi in
ra cho biet, khong bao loi. Dung tinh than "chua lam thi bao thieu".

259 bai test qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.78 - 2026-09-27

## Lenh xem con thieu gi: scripts/thieu.py

Theo y co Lan: cho nao chua co thi chi can bao thieu, ghi ro thieu o Mapping
hay thieu o Python va MA la gi, de bo sung dan.

    python3 scripts/thieu.py              tom tat ca ba khoi
    python3 scripts/thieu.py 10 2         chi tiet lop 10 chuong 2

In ra tung ma kem loai cau va ten dang, vi du:

    L10_C2_B3_TH024_MC_A    trac nghiem   Chon hinh ve dung cua mien nghiem
    L10_C2_B4_VD028_SA_A    tra loi ngan  Gia tri lon nhat cua F tren mien nghiem

Doc thang tep .py bang van ban de tim ham da co, khong import module, nen chay
nhanh va khong keo theo sympy.

Huong dan day du: docs/14_DEPLOYMENT.md

## Tinh trang ngan hang de

    Lop 10: 154 yeu cau can dat | 259 dang | 34 dang da co ham
    Lop 11: 148 yeu cau can dat | 238 dang | 0
    Lop 12:  58 yeu cau can dat | 113 dang | 0
    -------------------------------------------------------
    Tong  : 360 yeu cau can dat | 610 dang | 34 dang da co ham

Khong con cho nao thieu o Mapping. Con 576 dang cho viet ham Python.

Chuong nho nhat de lam truoc: lop 10 chuong 2 (13 dang), lop 12 chuong 2 (10),
lop 12 chuong 6 (12).

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.79 - 2026-09-27

## Curriculum da chay theo PPCT

Co Lan chot PPCT la chuan (PPCT la ke hoach day that, quyet dinh "den tuan nay
da day den bai nao"). Da dua toan bo Curriculum ba khoi ve dung so chuong/bai
cua PPCT.

    Lop 10: 27/27 bai khop PPCT | 8 chuong -> 9 chuong
    Lop 11: 18/34 bai khop PPCT (PPCT moi co het hoc ki I)
    Lop 12: 16/16 bai khop PPCT

Khong con bai nao lech ten. Khong con bai nao cua PPCT bi bo quen.

## Khong chi doi so - phai tach lai theo tung yeu cau

PPCT chia bai khac Curriculum nen phai dinh tuyen TUNG yeu cau can dat:

  L10 C4_B8  "Cac phep toan tren vecto" 14 yeu cau -> tach lam 3 bai:
             B8 tong/hieu, B9 tich voi mot so, B11 tich vo huong
  L10 C6_B16 "Bien co va xac suat" 14 yeu cau -> tach lam 2:
             C9_B26 bien co va dinh nghia, C9_B27 thuc hanh tinh xac suat
  L10 C7_B18 "Duong thang" 8 yeu cau -> tach lam 2:
             B19 phuong trinh, B20 vi tri tuong doi / goc / khoang cach
  L11 C1_B1  9 yeu cau -> tach lam 2: B1 Goc luong giac, B2 Gia tri luong giac
  L12 C2_B7 va C5_B15 -> gop vao B6 va B13

Hai cho doi han chuong: "Toa do cua vecto" tu C7 sang C4 (PPCT xep vao chuong
Vecto); lop 10 Thong ke va Ham so dao cho nhau (C5 <-> C6); lop 11 Gioi han va
Thong ke dao cho nhau (C3 <-> C5).

## Lop 10 chuong 1 khong bi dung den

Dang co 46 ham Python + 34 dong mapping tro vao, va PPCT cung ghi dung B1
Menh de, B2 Tap hop nen von da khop. Giu nguyen toan bo ma.

## Mot loi Claude tu gay ra va da sua

Lan dung lai mapping dau tien, Claude danh lai chu cai dang tu dau -> 
NB017_SA_C thanh NB017_SA_A, mat khop voi ham Python (34 xuong 33). Chu cai
A/B/C co nghia (SA_C di voi MC_C cung mot ho dang), khong duoc danh lai. Da
sua: giu nguyen chu cai cu, chi doi khi that su dung do. Ket qua 0 cho phai doi.

## Bang anh xa ly thuyet doi theo

data/ly_thuyet/anh_xa.json khoa theo ma bai: 23 bai -> 27 bai. Bai cu tach lam
nhieu bai moi thi moi bai moi nhan danh sach tep cua bai cu.

## PPCT con thieu hoc ki II lop 11

16 bai (C6_B19 den C9_B34) Curriculum da co ma PPCT chua co. So bai la Claude
danh noi tiep sau B18 - hop li nhung chua duoc PPCT xac nhan. Khi co Lan bo
sung PPCT hoc ki II, neu truong day thu tu khac thi bao de doi lai (luc do van
con re vi chua co ham Python nao tro vao).

## Canh khong cho lech lai

tests/test_ppct_curriculum.py (9 bai). Bai quan trong nhat: cung mot ma
chuong/bai thi PPCT va Curriculum phai la CUNG MOT BAI. Lech kieu nay nguy hiem
vi ma van khop chuoi nen may khong bao loi, chi lang le lay sai bai.

273 bai test qua (truoc: 264).

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.80 - 2026-09-27

## Dung lai PPCT tu KE HOACH DAY HOC THAT cua to

Co Lan gui "Ke hoach giang day toan chung nam hoc 2026-2027.docx" (kem quyet
dinh 97/QD-THPTCHV ngay 29/08/2026). Doi chieu thi PPCT trong kho SAI:

    data/ppct/toan11.json  chi co 18 bai (het HK I) va LECH MOT BAI:
        ghi B1 "Goc luong giac", B2 "Gia tri luong giac..."
        that ra B1 la "Gia tri luong giac cua goc luong giac" (mot bai)
    data/ppct/toan12.json  chi co 16 bai, thieu 3 bai va lech so tu B5 tro di

Da dung lai ca ba tep tu van ban that:

    toan10.json  27 bai / 9 chuong  (HK1 14 bai, HK2 13 bai)  - trung voi ban cu
    toan11.json  33 bai / 9 chuong  (HK1 17 bai, HK2 16 bai)  - truoc chi co 18
    toan12.json  19 bai / 6 chuong  (HK1 10 bai, HK2  9 bai)  - truoc chi co 16

Kem tuan bat dau / tuan ket thuc / tiet / hoc ky lay tu chinh ke hoach.
Keywords cua lop 10 giu nguyen tu ban cu.

## Hau qua: phai chinh lai curriculum lop 11 va 12

Version 2.79 da chinh curriculum theo PPCT SAI, nay chinh lai theo PPCT dung.

Lop 11: bo phan tach C1_B1 lam hai (PPCT that chi co MOT bai "Gia tri luong
giac cua goc luong giac"); Gioi han ve lai chuong V bai 15-17; Thong ke ve lai
chuong III bai 8-9. Ket qua bai 1-33 dung nhu SGK Ket noi tri thuc - tinh co
la trung voi ban Claude dung ban dau.

Lop 12: PPCT that co 19 bai chu khong phai 16. Ba bai truoc bi gop nham nay
tach ra dung:
    B5  Ung dung dao ham de giai quyet mot so van de lien quan den thuc tien
    B8  Bieu thuc toa do cua cac phep toan vecto
    B16 Cong thuc tinh goc trong khong gian

## Ket qua doi chieu

    Lop 10: PPCT 27 bai | Curriculum 154 yeu cau tren 27 bai | 261 dang
    Lop 11: PPCT 33 bai | Curriculum 148 yeu cau tren 33 bai | 238 dang
    Lop 12: PPCT 19 bai | Curriculum  58 yeu cau tren 19 bai | 113 dang

KHONG con bai nao cua PPCT thieu yeu cau can dat. Khong con bai nao lech ten.
Chu cai dang A/B/C giu nguyen het (0 cho phai doi).

## THIEU: chuyen de hoc tap

Ke hoach co ca chuyen de hoc tap ma he thong CHUA co gi:

    Lop 10  8 bai   CD1 He phuong trinh bac nhat ba an (b1-2)
                    CD2 Quy nap toan hoc, Nhi thuc Newton (b3-4)
                    CD3 Elip, Hypebol, Parabol, Su thong nhat ba duong conic (b5-8)
    Lop 11 12 bai   CD1 Phep bien hinh (b1-7)
                    CD2 Graph, Euler, Hamilton, duong di toi uu (b8-10)
                    CD3 Hinh chieu vuong goc, Ban ve ki thuat (b11-12)
    Lop 12  7 bai   CD1 Bien ngau nhien roi rac (b1-2)
                    CD2 He bat phuong trinh, dao ham toi uu (b3-4)
                    CD3 Tien te, tin dung, dau tu tai chinh (b5-7)

Da ghi lai o data/ppct/chuyen_de.json de biet con thieu gi. CHUA dua vao
curriculum/mapping - he thong chua ra de duoc phan chuyen de.

273 bai test qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.81 - 2026-09-27

## Khoi phuc moc ki thi trong PPCT (loi Claude tu gay ra)

Khi dung lai PPCT o v2.80, Claude de boundary_after = null cho MOI bai. Do la
moc de exam_scope_service biet de giua ki / cuoi ki dung o bai nao. Mat moc
thi moi loi goi load_scope_heso23 deu tra ve loi KHONG_TIM_THAY_MOC_DUNG -
tuc la KHONG RA DUOC de dinh ki nao ca.

Da suy lai moc tu chinh ke hoach day hoc: bai duoc day ngay TRUOC tuan "On
tap kiem tra giua ky / cuoi ky" chinh la moc.

    Lop 10  GK1 sau B8   CK1 sau B14  GK2 sau B22  CK2 sau B27
    Lop 11  GK1 sau B10  CK1 sau B17  GK2 sau B24  CK2 sau B33
    Lop 12  GK1 sau B5   CK1 sau B10  GK2 sau B13  CK2 sau B19

Lop 10 suy ra TRUNG KHIT ban cu trong git (B8, B14, B22, B27) - xac nhan cach
suy dung. Da thu ca 12 pham vi (3 khoi x 4 ki thi), chay dung het.

## scripts/thieu.py: loc theo ki thi

    python3 scripts/thieu.py 10 --giuaki1

Chi liet ke nhung dang nam trong pham vi ki thi do, lay tu PPCT. De biet phai
viet ham nao TRUOC cho kip ky kiem tra sap toi.

Cac tuy chon: --giuaki1  --cuoiki1  --giuaki2  --cuoiki2

## Can bao nhieu cho kiem tra giua ki I

    Lop 10  chuong 1-4, 8 bai   73 dang   da co 34   con thieu 39
    Lop 11  chuong 1-4, 10 bai  88 dang   da co  0   con thieu 88
    Lop 12  chuong 1, 5 bai     22 dang   da co  0   con thieu 22

273 bai test qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.82 - 2026-09-27

## Ngan hang cau hoi chuong 3 lop 10 (He thuc luong trong tam giac)

Co Lan chon lam chuong nay truoc vi can cho lop 10C9 lam de hoan thanh sang
kien kinh nghiem. Chuong 3 roi vao tuan 6-7 nen con khoang hai tuan.

    data/python_bank/toan10/L10_C3.py   18 ham sinh cau hoi
    18/18 dang trong Mapping da co ham -> chuong 3 mo cho hoc sinh chon

Truoc do chuong 3 chua co ham nao.

## Cac dang da viet

Bai 5 (4 dang)  gia tri luong giac goc dac biet; dung may tinh cam tay;
                quan he hai goc bu nhau (MC + SA rut gon bieu thuc)
Bai 6 (12 dang) dinh li cosin tinh canh (MC + SA); dinh li sin tinh canh (MC);
                ban kinh duong tron ngoai tiep (SA); chon cong thuc dien tich
                (MC); tinh dien tich (SA); giai tam giac c-g-c (MC) va g-c-g
                (MC); giai tam giac (SA); do khoang cach khi gap vat can
                (MC + SA); tinh chieu cao vat khong do truc tiep (TL 3 y)
Dung/Sai (2)    gia tri luong giac 0-180 do; he thuc luong trong tam giac

## Lam sao so lieu luon "dep"

Tinh san CAP_COSIN: cac cap canh (b,c) ma voi goc 60 hoac 120 do thi canh thu
ba ra SO NGUYEN (vi du 3-5 goc 120 -> 7; 7-8 goc 120 -> 13). Hoc sinh khong
phai bam may ra so le.

Dinh li sin: chon cap goc dac biet kem san he so k = sinB/sinA da rut gon
(vi du 45-60 -> can6/2) nen canh con lai luon la bieu thuc can rut gon duoc.

Dien tich: chon goc 30 hoac 150 do (sin = 1/2) va bc chia het 4 -> S nguyen.

Chieu cao vat: goc nang 30 roi 60 do, tam giac ABC can tai B nen BC = AB = d,
suy ra CH = d.can3/2 - chon d chan de ket qua gon.

## Da kiem chung the nao

1. 18/18 ham chay duoc, moi ham sinh dung so cau yeu cau.
2. Soat cau truc 51 cau: can ngoac {}, so dau $ chan, moi truong dong mo khop,
   khong co moi truong la, cau nao cung co loi giai.
3. Bien dich THAT ra PDF 5 trang, 0 loi (dich rieng phan toan bang XeLaTeX vi
   may ao thieu tabvar.sty, bclogo.sty, esvect.sty, vietnam.sty ma khung de
   cua co Lan can - VPS co du).
4. Doc lai PDF, doi chieu tung ket qua: 5^2+16^2+5.16 = 361 -> 19; 7^2+8^2+56
   = 169 -> 13; CH = 10.can3/2 = 5can3; cot150 = -can3; sin136 = 0,69. Dung het.
5. Chay CA DAY CHUYEN ra de 6 lan (blueprint -> chon cau -> sinh cau):
   24 cau, 0 loi, 0 cho thieu.

## Hai loi tu phat hien khi soat

- Ham TL viet "chieu cao CH cua mot TOA NHA" nhung cau sau lai ghi "chan THAP".
  Da gan danh tu di lien voi nhau (thap/chan thap, cot/chan cot, toa nha/chan
  toa nha).
- Ma tran doi mot cau TRA LOI NGAN muc van dung ma Mapping chua khai dang nao
  -> he thong bao "THIEU O MAPPING: L10_C3_B6_VD036_SA_A". Da them dang do va
  viet ham. Chinh co che bao thieu (v2.77) chi ra cho nay.

## Viet lai mot bai test

test_co_du_cau_dem_theo_ham_python... truoc ghim cung "moi chuong tru (10,1)
deu phai co 0 ham" - them ham cho chuong 3 la hong ngay. Viet lai theo QUAN HE
(so dang co ham khong vuot so dong Mapping; chuong khong co tep .py thi phai
dem ra 0) nen van dung khi co Lan them ham dan. Them mot bai test nua cho
truong hop chua co tep Python.

274 bai test qua.

## Con lai

    Lop 10: con 210 dang cho viet ham (chuong 1, 3 da xong)
    Lop 11: con 238
    Lop 12: con 113

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.83 - 2026-09-27

## Khoa loai cau ngay trong TEN HAM

Yeu cau cua co Lan: "TLN: khong co cac bai a,b duoc. chi co 1 cau hoi de ra 1
dap an tra loi ngan thoi. cau tu luan moi can 2 y. chot, khoa luon trong ten
ham cho toi."

Tu nay TEN HAM la loi hua, va he thong bat ham giu loi hua do. Khoa hai lop.

## Lop 1 - chan ngay luc viet ham (data/python_bank/math_type.py)

    _khoa_loai_cau_TLN(debai, dang)   dang 2/3 (tra loi ngan) ma de bai co
                                      listEX / item / SA[  -> bao loi ngay
    _khoa_loai_cau_TL(ds_abcd)        cau tu luan ma ds_abcd duoi 2 y

Goi ngay dong dau cua MC_SA_answer_const, MC_SA_answer_text, TL_answer_const,
TL_answer_text. Loi bao kem cau nhac nen doi sang loai nao.

## Lop 2 - chan theo ten ham (app/services/generator_service.py)

kiem_tra_dung_loai_cau(generator_id, latex_block) soi khoi LaTeX sinh ra so
voi ten ham, chay trong ca call_generator va call_locked_variant:

    _SA_   dung 1 shortans, khong duoc co listEX
    _TL_   tu 2 item tro len
    _TF_   phai co choiceTFt
    _MC_   phai co choice, khong duoc co shortans

Sai thi nem LoaiCauSaiError.

## Mot loai loi dung chung cho ca hai lop

LoaiCauSaiError dinh nghia MOT lan trong math_type.py (ke thua ValueError),
generator_service import lai dung lop do. Neu de hai lop khoa nem hai loai loi
khac nhau thi bo rap de chi bat duoc mot nua, nua con lai van lam vo ca de -
da thu that va gap dung loi nay truoc khi gop.

## De khong vo

exam_assembler_service bat LoaiCauSaiError giong nhu bat GeneratorNotFoundError
- cau sai loai KHONG vao de cua hoc sinh, thay vao do de in dong bao thieu kem
ID de sua. Dung nguyen tac "cu bao thieu, khong can bao loi".

## Vong quet tim ra 1 ham cu chua dung quy uoc

L10_C1_B2_VD021_TL_A_01 - ten la tu luan nhung ca 4 kieu deu chi sinh MOT y
("So gia tri nguyen cua tham so m de A hop B = A"). Theo quy uoc moi thi mot
cau hoi ra mot dap an la TRA LOI NGAN.

Hai cach sua, cho co Lan quyet:
  (1) Them y thu hai vao ca 4 kieu, giu nguyen ten _TL_ va Mapping.
  (2) Doi ham sang _SA_ , phai sua ca dong trong Mapping.

Trong luc cho: ham nay bi chan khi ra de va he thong bao thieu, nen khong co
cau sai loai nao den tay hoc sinh. Ten ham ghi trong CHUA_DUNG_QUY_UOC o
tests/test_loai_cau.py; sua xong thi xoa khoi do, bai test se tu doi hoi lai.

## Da kiem chung the nao

1. Thu that ca hai lop: TLN chia y -> bi chan; tu luan 1 y -> bi chan; trac
   nghiem co shortans -> bi chan; TLN dung quy uoc -> qua.
2. tests/test_loai_cau.py (23 test) trong do co vong quet chay THAT moi ham
   _SA_ / _TL_ dang co trong ngan hang va soi theo dung ten no.
3. Quet CA 3 KHOI qua duong ra de that (call_generator tren moi dong Mapping):
   51 ham chay dung loai, 1 ham bi chan (VD021), 561 dang chua co ham. Khong
   ham nao nem loi la lam vo de.
4. 296 bai test qua, 1 bo qua (dung ham VD021 dang cho quyet).

## Con lai

    Lop 10: con 210 dang cho viet ham (chuong 1, 3 da xong)
    Lop 11: con 238
    Lop 12: con 113

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.84 - 2026-09-27

## Dang VD021 lop 10: doi cau tu luan mot y thanh cau TRA LOI NGAN

Co Lan chot: "doi sang TLN".

    L10_C1_B2_VD021_TL_A   Tu luan       ->  L10_C1_B2_VD021_SA_A   Tra loi ngan
    (Mapping doi ca id lan cot Loai; Dang giu nguyen)

Ham L10_C1_B2_VD021_TL_A_01 doi ten thanh L10_C1_B2_VD021_SA_A_01 (dang=2).
Sau buoc nay khong con ham nao vi pham quy uoc loai cau; danh sach ngoai le
CHUA_DUNG_QUY_UOC trong tests/test_loai_cau.py da xoa han, moi ham _SA_/_TL_
deu bi soi that.

## Nhan tien phat hien SAI TOAN trong ca dang nay

Doc ky de sua loai cau thi thay dap so cua dang VD021 SAI o hai cho, dinh ca
cau trac nghiem L10_C1_B2_VD021_MC_A_01 chu khong rieng cau vua doi.

De cu: "Cho A = [a;b] va B = (n;m]. Co bao nhieu gia tri nguyen cua m de ...?"

  (1) De KHONG noi B khac rong. Ma voi m <= n thi B = rong, va tap rong la
      tap con cua moi tap, nen:
        - kieu 1 (A hop B = A): van dung -> co VO SO gia tri nguyen cua m
        - kieu 3 (A giao B = rong): cung van dung -> cung VO SO
      Dap so cu b - n va a - n - 1 la thieu truong hop.

  (2) Kieu 2 (A hop B = B) dan toi m >= b; kieu 4 (A giao B khac rong) dan
      toi m >= a. Deu co VO SO gia tri nguyen cua m. Loi giai cu viet "theo
      cach sinh du lieu ta co m <= 15" roi dem tu b (hoac a) den 15 - nhung
      DE BAI KHONG HE NOI m <= 15, hoc sinh khong the nao biet duoc.

Da chung minh bang may: giu nguyen de cu roi dem m trong cac khoang rong dan
[-33;42], [-63;72], [-123;132] thi so gia tri dem duoc la 46, 76, 136 - tang
theo khoang do, dung nghia VO SO.

## Cach sua

  - De bai them dieu kien: "trong do m la so nguyen sao cho B khac rong".
    Cai nay chan het truong hop B = rong, kieu 1 va kieu 3 tro lai dung.
  - Kieu 2 va kieu 4 doi cau hoi: khong hoi "co bao nhieu gia tri" nua ma hoi
    "TIM GIA TRI NGUYEN NHO NHAT cua m" - luon ton tai, duy nhat, va dung
    tinh than mot cau mot dap so cua tra loi ngan.
  - Gop chung phan sinh de/loi giai cua hai ham (_VD021_de_giai, _VD021_nhieu,
    _VD021_sinh) de cau trac nghiem va cau tra loi ngan khong bao gio lech
    nhau; hai ham cong khai chi con goi lai phan chung do.

## Hai loi trinh bay tu phat hien khi doc PDF

  - Phep tru ra hai dau tru lien nhau: "10 - -1 = 11". Da boc ngoac so am
    (_VD021_ngoac) -> "10 - (-1) = 11".
  - Khi dap so nho, dong liet ke thanh vo li: "m thuoc {-9; -8; ...; -8}".
    Da sua (_VD021_liet_ke): tu 4 gia tri tro xuong thi ghi ra het, nhieu hon
    moi dung dau ba cham.

## Da kiem chung the nao

1. Doi chieu DOC LAP: khong dung lai cong thuc trong ham, ma rai diem cach
   nhau 1/4 de xet that quan he tap hop, roi do m nguyen trong mot khoang
   rong. Quet 3000 bo so lieu ngau nhien va 1491 bo quet co he thong:
   0 truong hop lech.
2. Soi TOAN BO 11800 truong hop co the co cua dong liet ke: 0 dong vo li.
3. Bien dich THAT ra PDF 16 cau (8 trac nghiem + 8 tra loi ngan), 5 trang,
   0 loi; doc lai PDF doi chieu tung dong tinh.
4. Ra de that 8 lan cho chuong 1: 64 cau, 0 loi.
5. Quet ca 3 khoi qua duong ra de: 52 ham chay dung loai, 0 ham bi chan.
6. 297 bai test qua, khong con bai nao bi bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.85 - 2026-09-27

## Ba viec: bac do kho cau Dung/Sai, don vi met, va nhap tep 10-3.py

## 1. Cau Dung/Sai phai tang dan NB -> TH -> VD -> VDC

Co Lan bao: "cau d) ko dung chuan. vi theo dung cau dung sai thi a: NB,
b: TH, c: VD, d: VDC."

Dung vay - y d) cu cua L10_C3_TF_B_01 chi la PHAT BIEU dinh li sin
("BC/sin A = 2R"), tuc muc nhan biet, dat o cho van dung cao. Da viet lai
ca hai ham Dung/Sai cua chuong 3:

    L10_C3_TF_A_01 (gia tri luong giac)
      a) NB   sin cua hai goc bu nhau bang nhau
      b) TH   cos cua goc bu, thay so cu the
      c) VD   tinh P = sin(180-a) + cos(180-a) theo dung goc alpha cua de
      d) VDC  cho sin(beta) va beta tu -> tim cos(beta) (he thuc co ban +
              xet dau cosin cua goc tu)

    L10_C3_TF_B_01 (he thuc luong trong tam giac)
      a) NB   phat bieu dinh li cosin
      b) TH   thay so tinh BC
      c) VD   phai co BC cua y b) moi dung duoc dinh li sin de tinh R
      d) VDC  do dai duong phan giac trong AD - khong co cong thuc san
              trong sach, phai tu tach dien tich tam giac lam hai phan

Kiem chung hai y moi bang TOA DO (dung ban kinh ngoai tiep tu ba dinh, va
giao diem phan giac voi BC): 11 tam giac, 0 lech.

tests/test_cau_dung_sai.py (moi): soi moi ham _TF_ phai co DUNG BON y, va
than ham phai ghi ro bon moc "# a) NB", "# b) TH", "# c) VD", "# d) VDC"
theo thu tu.

CON LAI, cho co Lan quyet: L10_C1_TF_A_01 va L10_C1_TF_B_01 (ham cu cua co)
rut bon y tu cung mot kho menh de nen khong phan bac do kho. Chua sua vi do
la noi dung cua co. Ten ghi trong CHUA_XEP_BAC o tep test.

## 2. Loi don vi tren web

De hien tren web la "CA = 8\,m" - chu "\,m" hien nguyen xi. Ly do: don vi
dat NGOAI cap $...$, ma trinh render cua web chi dich phan trong $...$.
Da dua don vi vao trong cong thuc: "$CA = 8\,\text{m}$" - dung ca trong PDF
lan tren web. Sua 7 cho trong L10_C3.py.

## 3. Nhap 10 dang tu tep 10-3.py cua co Lan

Tep cu ghi thang ra latex\data\de.tex, de \loigiai{} RONG va goi
DefChung.UCLN / DefChung.check. Da chuyen sang chuan ngan hang: moi ham
TRA VE chuoi LaTeX, co loi giai day du, dung math_type.py.

    K10_2_3_1_1_NB   -> L10_C3_B5_NB029_MC_B_01   toa do M -> gia tri luong giac
    K10_2_3_1_2_NB   -> L10_C3_B5_NB029_MC_C_01   gia tri luong giac -> toa do M
    K10_2_3_1_3_NB   -> L10_C3_B5_NB029_MC_D_01   gia tri nao co the xay ra
    K10_2_3_1_4_NB   -> L10_C3_B5_TH031_MC_B_01   doi xung qua Oy (co hinh)
    K10_2_3_2_1_TH   -> L10_C3_B5_TH030_MC_A_02   may tinh cam tay (bien the)
    K10_2_3_3_1_TH   -> L10_C3_B6_TH032_MC_A_02   dinh li cosin gan dung (bien the)
    K10_2_3_3_2_TH   -> L10_C3_B6_TH033_MC_B_01   ban kinh duong tron ngoai tiep
    K10_2_3_4_1_VD   -> L10_C3_B6_VD036_MC_B_01   dam lay, dinh li sin (co hinh)
    K10_2_3_4_2_VD   -> L10_C3_B6_VD036_TL_B_01   cu lao, tu luan (co hinh)
    K10_2_3_4_3_VDC  -> L10_C3_B6_VD036_MC_C_01   tau chay hai chang

Them 8 dang vao Mapping. Chuong 3 lop 10: 26/26 dang da co ham.

## Cac loi trong tep cu, da va khi chuyen

1. K10_2_3_1_2_NB nhanh choice==2: DE BAI truyen sai thu tu tham so nen
   ghi "sin = can(p)/q, cos = -(q^2-p^2)/q", trong khi dap an lai theo
   cach doc dung. De va dap an khong khop.
2. 7/10 ham de \loigiai{} RONG. Tro giang AI chi duoc lay dap an tu day
   nen bat buoc phai co loi giai - da viet day du cho ca 10 dang.
3. Lay hai so ngau nhien roi chia cho UCLN: khi hai so BANG NHAU thi ra
   p = q = 1, diem M(1;0), can bang 0 - cau hoi vo nghia. Da ep p < q.
4. K10_2_3_2_1_TH nhanh cos: mang phuong an nhieu chua -sin HAI LAN, nen
   cau hoi co hai phuong an trung nhau. Da bat buoc bon phuong an phan biet.
5. K10_2_3_4_3_VDC goi input() de hoi tu luan hay trac nghiem, va GOI LUON
   ham o cuoi tep. Ca hai deu lam TREO ngan hang luc nap mo-dun. Da bo.
6. Can bac hai so chinh phuong van de nguyen dang "can 16" thay vi "4".
   Nay dung sympy nen tu rut gon.
7. Cau tu luan cu lao chi co MOT y - trai quy uoc da chot. Da tach dung
   theo hai buoc cua chinh loi giai cu: (a) tinh goc ACB, (b) tinh AC.

## Mot loi CHINH CLAUDE tu tao ra roi tu bat duoc

Khi viet lai dang "gia tri nao co the xay ra", Claude mo rong phuong an
nhieu sang \tan va \cot: "$\tan\alpha = 2$". Nhung tan cua goc khoang
63 do DUNG BANG 2 - thanh ra cau hoi co hai dap an dung. Ban cua co Lan
chi dung sin/cos nen khong vuong. Da tra lai dung nhu ban cua co va ghi
chu canh bao ngay trong ham.

## Da kiem chung the nao

1. Diem tren nua duong tron don vi: 1600 truong hop, deu that su nam tren
   duong tron (x^2 + y^2 = 1) va o nua tren.
2. Soi TUNG PHUONG AN cua hai dang de sai nhat: dang may tinh cam tay
   (1200 phuong an) va dang "gia tri co the xay ra" (1200 phuong an) -
   moi cau dung mot phuong an dung, 0 sai.
3. Doi chieu DOC LAP bang toa do / vecto: dinh li cosin (300 bo), ban kinh
   ngoai tiep (300 bo), dinh li sin (400 bo), va bai toan tau chay - dung
   VECTO HUONG DI THAT (N goc E roi S goc E) de kiem lai goc ABC = goc1 +
   goc2 (500 bo). Tat ca 0 lech.
4. Bien dich THAT 20 cau cua 10 dang moi ra PDF 7 trang, 0 loi; doc lai
   PDF va XEM ANH ba trang co hinh ve - ca ba hinh (nua duong tron, dam
   lay, cu lao) deu ve ra dung.
5. Ra de that 8 lan cho chuong 3: 36 cau, 0 cho thieu, 0 loi.
6. 304 bai test qua, 2 bo qua (hai ham Dung/Sai cua chuong 1 dang cho).

## Mot viec can co Lan quyet: HINH VE va WEB

answer_parser_service danh dau co_hinh_ve = True cho cau co tikzpicture,
va cau do KHONG duoc dua vao phan lam bai truc tiep tren web (chi ra PDF).
Trong 8 de chuong 3 vua ra thu co 7 cau co hinh. Nghia la them hinh thi de
PDF dep hon nhung cau do bien mat khoi trang lam bai cua hoc sinh. Ba huong:
  (a) giu nguyen - hinh chi phuc vu PDF;
  (b) bo hinh o nhung dang van du du kien de giai;
  (c) dung LaTeX dich TikZ ra anh SVG/PNG roi luu lai cho web hien - viec
      nay la tinh nang moi, phai co Lan dong y truoc.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.86 - 2026-09-27

## 1. Y d) cau Dung/Sai: bo cong thuc ngoai sach giao khoa

Co Lan bat duoc: "do dai duong phan giac phai qua bai hinh hoc... ko su dung
cac cai khong co trong sach giao khoa. Neu tach dien tich thanh 2 phan, hoc
sinh co the su dung cac cong thuc thuoc chuong tinh duoc ko. neu duoc thi de lai."

Co dung. Loi giai cu viet "Ma sin A = 2 sin(A/2) cos(A/2)" - do la CONG THUC
NHAN DOI, lop 11 moi hoc. Hoc sinh lop 10 khong theo duoc.

Nhung cach tach dien tich thi CUU DUOC, vi goc A o day chi la 60 hoac 120 do
nen ca sin A lan sin(A/2) deu TRA THANG BANG:

    A = 120 -> nua goc 60,  sin 60 = can3/2,  sin 120 = can3/2  -> AD = bc/(b+c)
    A = 60  -> nua goc 30,  sin 30 = 1/2,     sin 60  = can3/2  -> AD = can3.bc/(b+c)

Loi giai moi chi dung ba thu, deu trong tam tay hoc sinh:
  - S = 1/2 . canh . canh . sin(goc xen giua)   -> cong thuc dien tich, bai 6
  - bang gia tri luong giac goc dac biet         -> bai 5
  - phan giac chia goc A thanh hai goc bang nhau -> hinh hoc lop 7
KHONG con cong thuc nhan doi, KHONG con cong thuc do dai phan giac.

Phuong an sai doi lai cho co y nghia: lay nham sin cua NUA goc.
Da kiem chung lai bang toa do (tim giao diem phan giac voi BC): 11 tam giac,
0 lech. Dong thoi doi het \frac sang \dfrac trong hai ham Dung/Sai.

## 2. HINH VE HIEN DUOC TREN WEB

Co Lan: "phai co hinh ca tren web. ko the ko co hinh. se bi sai muc do cua
cau. co hinh muc do se de hon. hoac phuc tap hon (vi du bai ham bac 2 - ko co
hinh sao lam cac muc do nhin hinh ra dinh, truc doi xung)".

Truoc day cau co TikZ bi danh dau co_hinh_ve va BI LOAI khoi phan lam bai
truc tiep, chi con trong PDF. Trong 8 de chuong 3 ra thu co 7 cau nhu vay.

Nay dich hinh ra anh:

    app/services/hinh_ve_service.py   (moi)
      - tim moi doan \begin{tikzpicture}...\end{tikzpicture} trong de bai
      - ghep vao DUNG phan dau cua khung de (latex_template.tex) roi dich
        bang xelatex -> PDF -> anh, nen hinh tren web giong het trong PDF
      - may nao thieu goi (tabvar, bclogo, esvect...) thi tu lui ve mot
        phan dau RUT GON chi co tikz/tkz-euclide/pgfplots
      - dich ra moi dinh dang lam duoc roi GIU CAI NHE NHAT: hinh con song
        ve bang plot[smooth] cho ra SVG 2,2 MB tu pdftocairo nhung chi 20 KB
        tu dvisvgm; trang lam bai cua hoc sinh hay mo bang 3G nen chon nhe
      - luu theo ma bam sha1 cua doan TikZ: mot hinh chi dich mot lan

    answer_parser_service   giu lai hinh_tikz thay vi vut di
    exam_assembler_service  dich hinh NGAY LUC SINH DE (may dang chay LaTeX
                            san roi) nen hoc sinh mo trang khong phai cho
    exam.py                 duong moi GET /hinh/{ma} tra anh, cache 1 nam
    lam_bai.html            hien <img>, va cau co hinh nay DUOC LAM binh
                            thuong (truoc day bi bo qua khi thu bai lam)

Hinh hong thi khong lam vo de: cau van ra, chi la khong co anh, va luc do
web moi hien ghi chu "xem trong PDF" nhu cu.

    scripts/kiem_tra_hinh.sh (moi)  chay tren VPS de xem may co du do nghe
    data/hinh_cache/  da cho vao .gitignore (tu sinh lai duoc)

## Da kiem chung the nao

1. Dich that ba hinh cua chuong 3 (nua duong tron don vi, dam lay, cu lao):
   6 KB PNG / 5 KB SVG / 20 KB SVG, moi hinh 1,5s lan dau, 0,000s lan sau.
2. XEM ANH hinh cu lao sau khi dich - song, cu lao, cay, tam giac ABC va
   nhan 65 do, 85 do, 40 deu dung.
3. Chay CA DUONG DAY: sinh cau -> trich de bai -> dich hinh -> tra duong
   dan anh, ca ba dang deu ra anh va phan CHU cua de bai van con nguyen.
4. tests/test_hinh_ve.py (4 bai): tim dung doan TikZ, ma bam on dinh va
   phan biet, de bai giu chu nhung khong lot ma TikZ ra cho hoc sinh.
5. 308 bai test qua, 2 bo qua.

## Con phai lam tren VPS

Chay "bash scripts/kiem_tra_hinh.sh". Neu bao thieu cong cu doi PDF sang
anh thi cai: apt-get install -y poppler-utils (va texlive-extra-utils neu
muon co pdfcrop cat vien cho sat). Khong ssh duoc tu may ao cua Claude nen
chua tu kiem tra duoc cho nay.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.87 - 2026-09-27

## Va loi canh bao ky tu thoat, va sua lai script kiem tra

Co Lan chay scripts/kiem_tra_hinh.sh thi Python in ra giua man hinh:

    hinh_ve_service.py:10: SyntaxWarning: "\e" is an invalid escape sequence

Docstring co viet \end{tikzpicture} nhung khong phai chuoi tho (raw string)
nen Python hieu "\e" la ky tu thoat khong hop le. Python 3.12 tro len bao
SyntaxWarning; ban 3.10 tren may ao cua Claude chi bao DeprecationWarning
nen KHONG THAY - phai co may cua co Lan moi lo ra.

Da va 5 cho (1 trong hinh_ve_service.py, 4 trong L10_C3.py).

tests/test_ma_nguon_sach.py (moi): chay tren MOI tep .py cua du an, bat loi
nay ngay. Ngan hang de day chuoi LaTeX nen chuyen nay chac chan con lap lai.
64 tep, 0 canh bao.

## Script kiem tra: noi ro dang kiem tra MAY NAO

Co Lan chay tren may Mac chu khong phai VPS - ma web chay tren VPS. Script
cu khong noi gi nen khong biet. Nay script:
  - in ten may va thu muc, va noi thang neu khong phai VPS, kem san lenh
    ssh de chay lai cho dung cho
  - canh bao khi chi co MOT cong cu doi PDF sang anh: van chay duoc nhung
    khong co cai du phong, va khong chon duoc dinh dang nhe nhat
  - ket luan ro mot dong o cuoi: du do nghe hay chua

Ket qua tren may Mac cua co Lan: chi co dvisvgm (thieu pdftocairo, pdftoppm).
Van dich duoc hinh, nhung nen cai them: brew install poppler

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.88 - 2026-09-28

## Loi chi xay ra TREN VPS: hinh lot thom giua trang A4

Tim ra khi dung nghi vi sao may ao cua Claude khong gap loi nay duoc.

hinh_ve_service dich hinh bang chinh phan dau (preamble) cua khung de, de
hinh tren web giong het trong PDF. Nhung khung de la \documentclass{book}
kho A4 co goi geometry - dich MOT hinh ra se duoc ca mot trang giay A4 voi
hinh be ti o goc. Da do that:

    preamble nguyen goc (book + geometry) -> trang 595 x 842 pt  (A4)
    sau khi sua                           -> trang  65 x  69 pt  (vua hinh)

Vi sao truoc khong thay: may ao cua Claude THIEU tabvar, bclogo, esvect nen
duong "preamble day du" luon hong va tu lui ve preamble rut gon, ma preamble
rut gon dung \documentclass{standalone} - tu cat sat vien. VPS co du goi nen
se di duong day du, va do moi la duong bi loi. Da gia lap VPS bang cach tao
bon tep .sty rong roi cho vao TEXINPUTS de di dung duong do ma thu.

Cach sua: khi dung preamble day du thi doi \documentclass thanh
standalone[preview,border=4pt] va bo goi geometry. Khong phu thuoc pdfcrop
co hay khong (may ao thieu pdfcrop, may co Lan co).

Da do lai sau khi sua, di duong preamble DAY DU: SVG 166 x 143 pt,
PNG 350 x 238 px - vua khit hinh.

## TEXINPUTS: noi them chu khong de len

dich_hinh dat TEXINPUTS de tim ex_test.sty trong repo, nhung dat de len
TEXINPUTS san co cua may. Nay noi them vao sau.

## 'day web' tu kiem tra do nghe ve hinh

Co Lan chay kiem_tra_hinh.sh o /root nen bao "No such file or directory" -
phai cd vao /root/NganHangDe moi thay. Khong bat ai phai nho duong dan:
day.sh nay tu chay buoc kiem tra tren VPS sau khi cap nhat xong, va in mot
dong ket luan; neu thieu do nghe thi in luon lenh cai dat.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.89 - 2026-09-28

## Nhap chuong 9 lop 10 (Xac suat) tu tep LopXChuong9.py cua co Lan

Co Lan gui 9 tep chuong cua lop 10 (124 ham). Lam theo thu tu co chon:
chuong da theo form moi truoc. Dot nay la CHUONG 9.

    data/python_bank/toan10/L10_C9.py   13 ham
    data/python_bank/DefChung.py        dung lai mo-dun dem dung chung

13/13 dang chay duoc va DUNG LOAI cau. Chuong 9: 13/27 dang da co ham.

## Doi ten theo ID ngan hang

    K10_9_TN_1_H                    -> L10_C9_B27_TH154_MC_A_01
    K10_9_TN_2_VD                   -> L10_C9_B27_VD155_MC_A_01
    K10_9_TN_3_VD                   -> L10_C9_B27_VD155_MC_B_01  (dang moi)
    K10_9_TN_4_B                    -> L10_C9_B26_NB144_MC_A_01
    K10_C9_B26_XacSuatBienCo_MC_VD  -> L10_C9_B27_TH152_MC_A_01
    K10_9_Ngan_1_VD                 -> L10_C9_B27_VD155_SA_A_01  (dang moi)
    K10_9_Ngan_3_VD                 -> L10_C9_B27_TH151_SA_A_01
    K10_9_Ngan_4_VD                 -> L10_C9_B27_TH154_SA_A_01
    K10_9_DS_1_VD                   -> L10_C9_TF_A_01
    K10_9_DS_2_VD                   -> L10_C9_TF_B_01
    K10_9_DS_3_VDC                  -> L10_C9_TF_C_01            (dang moi)
    K10_9_DS_4_VD                   -> L10_C9_TF_D_01            (dang moi)
    K10_9_DS_5_VD                   -> L10_C9_TF_E_01            (dang moi)

Them 5 dang vao Mapping.

## Kiem chung noi dung KHONG bi lam sai lech

Chay ham goc cua co Lan va ham da doi ten voi CUNG MOT HAT NGAU NHIEN roi
so tung ky tu: 12/13 ham ra ket qua GIONG HET. Ham thu 13 khong so duoc vi
ban goc bi loi (xem duoi).

## Cac loi da va

1. K10_C9_B26_XacSuatBienCo_MC_VD goi np.random.randint(...) - nhung trong
   tep nay np CHINH LA numpy.random, nen np.random la ham random(), khong co
   .randint. Ham nem AttributeError, KHONG ra duoc cau nao. Doi thanh
   np.randint(...). Da do lai dap an: gieo 9 lan, xac suat co it nhat mot
   lan mat 2 cham = 1 - (5/6)^9 = 0,81 - dung.

2. K10_9_TN_4_B de \loigiai{} RONG. Tro giang AI chi duoc lay dap an tu day
   nen bat buoc phai co loi giai; da viet phan giai thich cho ca bon phuong
   an (hai bien co xung khac, hop hai bien co khac khong gian mau...).
   Dong thoi doi ID: de hoi ve QUAN HE GIUA HAI BIEN CO chu khong phai tinh
   xac suat, nen thuoc NB144 chu khong phai TH151.

3. Nam ham trac nghiem khai bao (socau, dang) KHONG co gia tri mac dinh.
   Ngan hang goi func(socau) va dua vao mac dinh nen nem TypeError. Da dat
   dang=1 theo dung quy uoc (MC -> 1, SA -> 2/3).

4. Loi goi ham o muc mo-dun (print(...)) - nap mo-dun la chay ngay. Da bo.

5. Nam canh bao ky tu thoat (\Omega, \dfrac). Sua bang cach nhan doi dau
   gach cheo, KHONG doi sang chuoi tho, vi trong cung chuoi con co "\\ \\"
   ma doi sang raw se lam doi ket qua in ra.

## Mot ham KHONG nhap

K11_9_TN_2_H - chinh co Lan ghi chu "danh cho lop 11". Ngoai ra ham nay con
hai loi: (a) v = [mat, xac_suat_mat] chi co HAI phan tu nhung dong sau lai
lay v[0] den v[3] -> IndexError; (b) de hoi "xac suat xuat hien mat a HOAC
mat b" thi phai CONG hai xac suat, nhung dap an lai lay TICH, con tong thi
de lam phuong an nhieu - tuc dap an va nhieu bi doi cho.

## Phu thuoc moi

num2words (viet so bang chu tieng Viet) - da them vao requirements.txt.
VPS phai cai: pip install num2words

## Sua hai bai test

- test_loai_cau goi ham bang hai tham so cung; nay goi qua chinh
  _call_generator_function nhu ngan hang goi that (soi chu ky ham), vi co
  ham cua co Lan chi nhan mot tham so socau.
- Nam ham Dung/Sai chuong 9 chua xep bon y theo bac NB -> TH -> VD -> VDC,
  da ghi vao CHUA_XEP_BAC cho co Lan xem lai.

## Da kiem chung the nao

1. So tung ky tu voi ban goc: 12/13 ham giong het.
2. 13/13 dang chay qua duong ra de that, dung loai cau, 0 loi.
3. Bien dich THAT 26 cau (13 dang x 2) ra PDF 10 trang, 0 loi.
4. Soi loi giai tung dang: sau khi va, ca 13 dang deu co loi giai.
5. 382 bai test qua, 7 bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.90 - 2026-09-28

## Chan mot loi TREO trong math_type (anh huong ca ngan hang)

Do thu ham K10_3_3_1_1_H cua co Lan thi thay no TREO 4/5 lan. Lan theo thi
loi nam trong chinh math_type.py:

    nhieuda = random.sample(dsnhieu, 3)
    while len(set([dapso, nhieuda[0], nhieuda[1], nhieuda[2]])) < 4:
        nhieuda = random.sample(dsnhieu, 3)      # KHONG CO LOI THOAT

Neu danh sach nhieu chi co dung ba phan tu ma trong do co hai phan tu trung
nhau (hoac trung dap so) thi random.sample luon tra ve dung ba phan tu ay -
vong lap quay mai khong dung, TREO ca lan ra de, khong bao gi het.

Nay thay bang _chon_ba_nhieu(dapso, dsnhieu): loc trung mot lan, du thi
lay, khong du thi nem NhieuTrungError kem danh sach nhieu de con sua.

Gom luon cac loi "cau hong nhung de van phai ra" ve mot lop CauHongError;
LoaiCauSaiError va NhieuTrungError deu ke thua no, bo rap de chi phai bat
mot loai - cau hong thi BAO THIEU chu khong lam vo de.

## Nhap 6 dang chuong 3 co Lan da tu chuyen form

Co Lan chot: ban cua co lam goc, bo ban Claude viet hom qua.

    K10_3_3_1_1_H   -> L10_C3_B5_NB029_MC_B_01   (thay ban Claude)
    K10_3_3_1_2_H   -> L10_C3_B5_NB029_MC_C_01   (thay ban Claude)
    K10_3_3_3_1_H   -> L10_C3_B6_TH032_MC_A_02   (thay ban Claude)
    K10_3_3_4_1_H   -> L10_C3_B6_VD036_MC_B_01   (thay ban Claude; hinh
                                                  dam lay cua co co nhan
                                                  canh va hai goc, dep hon)
    K10_3_3_4_3_H   -> L10_C3_B6_VD036_MC_C_01   (thay ban Claude)
    K10_3_3_4_3_TF  -> L10_C3_TF_C_01            (DANG MOI)

Chuong 3 lop 10: 27/27 dang da co ham, 0 loi.

## Cac loi da va khi nhap

1. K10_3_3_1_1_H: gom nhieu roi moi loc trung TRONG vong lap, nen neu danh
   sach da du ba phan tu ma co hai cai giong nhau thi vong lap khong chay,
   va math_type nhan [x, y, y] -> treo. Nay dung _ba_nhieu, bao dam ba
   phuong an doi mot khac nhau. Do lai: 40/40 lan chay tron.
   Loc luon phuong an co mau bang 1 (\dfrac{...}{1}) - nhin rat vo li.
2. Bo lenh goi ham o muc mo-dun.
3. Va 9 chuoi co ky tu thoat hong. Dung bo phan tich cu phap (tokenize) de
   CHI sua chuoi thuong, khong dung den chuoi tho fr"""...""" - neu sua bua
   bang regex ca tep se lam hong cac chuoi tho von da dung.
4. Dat mac dinh dang=1 cho cac ham trac nghiem.

## Con lai o chuong 3 (chua lam)

Hai ham Dung/Sai con o form cu - K10_3_3_3_2_TH_DS va K10_3_3_3_4_VD_DS.
Chua nhap vi ca hai deu goi dc.GiaiTamGiac_Goc() (hoac _Canh()) SAU LAN,
moi lan tra ve mot tam giac ngau nhien KHAC NHAU, nen sau so A, B, C, a, b,
c khong thuoc cung mot tam giac - de bai khong khop nhau. Muon nhap thi
phai goi mot lan roi lay ca sau so, va viet lai loi giai (ban cu de
\loigiai{} rong). De dot sau, lam cung luc voi cac ham can DefChung.

## Danh dau dang do Claude tu them vao Mapping

Theo yeu cau cua co Lan: moi dong Mapping do Claude dat ID deu co them
truong "ghi_chu" ghi ro. Da danh dau nguoc lai cho 15 dong da them truoc do
(chuong 3: 10 dong, chuong 9: 5 dong). Quy uoc ghi trong docs/04_ID_STANDARD.md.
Tim nhanh:  grep -rn "CLAUDE THEM" data/mapping/

## Da kiem chung the nao

1. Ham NB029_MC_B_01 sau khi va: 40/40 lan chay tron (truoc do treo 4/8).
2. 27/27 dang chuong 3 chay qua duong ra de that, dung loai cau, 0 loi.
3. Bien dich THAT 12 cau cua 6 dang moi nhap ra PDF 9 trang, 0 loi.
4. Soi lai: 0 phuong an co mau bang 1 trong 120 cau.
5. 383 bai test qua, 8 bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.91 - 2026-09-28

## Them 11 dang cho chuong 3, de ra de da dang hon

Co Lan: "moi dang can nhieu ID de... vao dang chon 1 bai, nhung moi lan vao
no ra khac de chu ko chi khac so. de se da dang hon."

Dung quy uoc: chu cai A, B, C sau loai cau la cac DANG DE KHAC NHAU cua
cung mot yeu cau can dat (hoi cai khac, cho du kien khac); con _01 _02 moi
la cung mot de doi so.

Truoc dot nay co yeu cau chi co mot dang duy nhat:

    TH030  1 dang  ->  3 dang
    TH032  2 dang  ->  4 dang
    TH034  2 dang  ->  4 dang

Chuong 3 lop 10: 27 -> 38 dang, ca 38 deu da co ham.

## Muoi mot dang moi

    Bai 5
      TH030_MC_B  biet mot gia tri luong giac + khoang cua goc -> gia tri con lai
      TH030_SA_A  biet cosin (so thap phan) -> tim sin
      TH031_SA_B  rut gon bieu thuc bang he thuc co ban va quan he hai goc bu
    Bai 6
      TH032_MC_B  biet BA CANH -> tinh cosin mot goc (dinh li cosin dung nguoc)
      TH032_SA_B  biet ba canh -> so do goc (60, 90 hoac 120 do)
      TH033_SA_B  dinh li sin: biet mot canh va hai goc -> canh con lai
      TH034_MC_B  cong thuc Heron -> dien tich
      TH034_SA_B  ban kinh duong tron noi tiep, dung S = p.r
      TH035_MC_C  nhan dang tam giac nhon / vuong / tu
      VD036_SA_B  thuc te: dien tich manh dat tam giac (Heron)
      VD036_TL_C  thuc te (tu luan 2 y): tinh canh con lai va dien tich

Moi dong Mapping deu co "ghi_chu" danh dau Claude dat ID.

## Lam sao so lieu luon dep

BANG_HERON: quet toan bo tam giac ba canh nguyen (canh <= 30) giu lai
nhung tam giac vua co DIEN TICH NGUYEN vua co BAN KINH NOI TIEP NGUYEN -
duoc 24 tam giac. Nho vay dang Heron va dang duong tron noi tiep khong bao
gio ra so le.

BO_BA_PYTAGO cho cac dang "biet sin tim cos": ket qua luon la phan so dep.
BO_BA_THAP_PHAN rieng cho dang tra loi ngan: chi lay bo ba ma thuong so co
so thap phan huu han (3-4-5 va 7-24-25), nen dap an go vao o tra loi duoc.

## Mot loi tu phat hien khi bien dich

TH033_SA_B ban dau tra dap an la can thuc: \shortans{ \dfrac{10\sqrt{3}}{3}}
- vua thieu dau $ (LaTeX bao 18 loi), vua SAI VE BAN CHAT: cau tra loi ngan
thi hoc sinh go MOT SO vao o tra loi, khong go duoc can thuc. Da doi sang
dap an lam tron hai chu so thap phan, va de bai noi ro "lam tron den hang
phan tram"; loi giai van giu ca gia tri dung lan gia tri gan dung.

## Da kiem chung the nao

1. BANG_HERON: do lai ca 24 tam giac bang cong thuc Heron va S = p.r, dung het.
2. BO_BA_PYTAGO va BO_BA_THAP_PHAN: kiem a^2 + b^2 = c^2, dung het.
3. Dang nhan dang tam giac: 200 cau, DOC LAP tinh lai cosin goc lon nhat roi
   doi chieu - 0 sai. Phan bo: 92 tu, 70 vuong, 38 nhon.
4. Dang cosin tu ba canh: 120 cau, doi chieu bang toa do - 0 lech.
5. Dang dinh li sin: 120 cau - 0 lech.
6. 38/38 dang chay qua duong ra de that, dung loai cau, 0 loi.
7. Bien dich THAT 22 cau cua 11 dang moi ra PDF 6 trang, 0 loi; doc lai
   doi chieu (5-12-13 -> p=15, S=30; 20-24-... -> S=96).
8. Ra de that 12 lan: 49 cau, dung 12 dang khac nhau.
9. 390 bai test qua, 8 bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.92 - 2026-09-29

## 'day web' mo ket noi ssh thu hai - bi hoi mat khau roi dut

Co Lan chay day web thi thay:

    Dang kiem tra do nghe ve hinh tren VPS...
    root@nganhangdechv.tech's password:
    Connection closed by 103.82.27.226 port 22

Buoc truoc do (git pull + restart) vao bang khoa binh thuong, chi buoc kiem
tra hinh moi bi hoi mat khau - vi no MO MOT KET NOI SSH THU HAI.

Da gop: mot ket noi ssh duy nhat lam het moi viec tren VPS (keo ma nguon,
khoi dong lai dich vu, kiem tra thu vien, kiem tra do nghe ve hinh), roi
doc ket qua o may cua co Lan. Vua nhanh vua khong dinh chuyen xac thuc lan hai.

Them mot buoc kiem tra nua trong cung ket noi do: VPS co thu vien num2words
khong (chuong 9 can). Thieu thi in ro lenh cai.

Dong ket luan cuoi khong con bao "XONG" khi VPS van con viec phai lam.

## Loi nap mo-dun lam VO CA DE - nay chi bao thieu

VPS da keo ma nguon chuong 9 nhung co the chua co num2words. Khi do
_load_chapter_module goi exec_module se nem ImportError, va loi nay BAY
THANG RA NGOAI, lam vo ca de - ke ca de cua chuong khac.

Nay bat lai va doi thanh GeneratorNotFoundError: he thong bao thieu dung
cho, con cac chuong khac van ra de binh thuong. Da thu that bang cach ep
import num2words that bai: bao thieu dung, khong vo de.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.93 - 2026-09-29

## Cai thu vien tren VPS: pip bi Ubuntu chan, va phai dung DUNG con python

Co Lan chay pip tren VPS thi gap:

    error: externally-managed-environment   (PEP 668)

Ubuntu 24.04 tro len khong cho pip cai thang vao Python he thong.

Nay day.sh tu tim con python ma dich vu dang chay:

    systemctl show -p ExecStart --value nganhangde

roi kiem num2words bang CHINH con python do (neu dich vu chay trong venv
thi python3 he thong va python cua dich vu la hai con khac han - kiem nham
con se ra ket luan sai), va in ra dung lenh can go:

    venv        -> <python cua venv> -m pip install -r requirements.txt
    he thong    -> python3 -m pip install --break-system-packages -r requirements.txt

Ghi them muc huong dan vao docs/14_DEPLOYMENT.md, kem luu y: "day" la lenh
tat tren MAY MAC, khong co tren VPS - dang trong ssh thi phai exit ra da.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.94 - 2026-09-29

## Nhap chuong 2 lop 10 (Bat phuong trinh bac nhat hai an)

    data/python_bank/toan10/L10_C2.py   8 ham / 6 dang
    Chuong 2: 6/14 dang da co ham.

    K10_2_3_1_1_H       -> L10_C2_B3_NB022_MC_A_01
    K10_2_3_1_1_NB      -> L10_C2_B3_NB022_MC_A_02   (bien the cung dang)
    K10_CheckDiemBPT_H  -> L10_C2_B3_NB023_MC_A_01
    K10_2_3_2_1_H       -> L10_C2_B3_TH024_MC_A_01   (co hinh)
    K10_2_3_2_1_TH      -> L10_C2_B3_TH024_MC_A_02   (co hinh, bien the)
    K10_2_3_2_2_TH      -> L10_C2_B4_TH027_MC_A_01   (co hinh)
    K10_2_3_3_2_VD      -> L10_C2_B4_TH027_MC_B_01   (DANG MOI)
    K10_2_3_3_1_H       -> L10_C2_B4_VD028_MC_A_01

## Bon loi da va

1. d0.is_integer() (5 cho) - int.is_integer() chi co tu Python 3.12, ma may
   co Lan dang chay Python 3.10 nen HAI HAM NEM LOI NGAY TREN MAY CO. Doi
   thanh (int(d0) == d0), chay duoc moi ban Python.
2. latex(bien_ngau_nhien ^ 3) - trong Python dau ^ la phep XOR chu khong
   phai luy thua, nen sympy Symbol nem TypeError. Doi thanh ** 3.
3. while N == M ... dung bien N khi N CHUA duoc gan -> UnboundLocalError.
   Da gan N truoc vong lap va rut gon dieu kien (hai ve cua dieu kien cu
   von la mot).
4. Bo lenh goi ham o muc mo-dun; va 2 chuoi ky tu thoat.

## Hai ham KHONG nhap

K10_2_3_1_2_NB - de hoi "Bat phuong trinh nao sau day LA bat phuong trinh
bac nhat hai an?" nhung CA BON PHUONG AN DEU KHONG PHAI. Vi du mot cau:

    dap an danh dau:  343(x-4)^2 y <= -3     (bac ba)
    cac phuong an:    -5xy + 6y >= -7        (co xy)
                      -5x^2 - 2y >= -3       (co x binh phuong)
                      4x - 9y - z <= 9       (ba an)

Loi giai con tu mau thuan: "Bien doi phuong an dung, ta thay cac an x va y
deu chi co bac lon nhat la 1" - sai hien nhien voi (x-4)^2 y. Soi 40 cau,
40 cau deu khong co phuong an nao dung. Can co Lan sua lai phan sinh dap an.

K10_2_4_1_1_VDC_TL - goi TL_answer(debai, giai, "0,5 diem", dang), nhung
math_type.py KHONG CO ham ten TL_answer. Ngoai ra day la cau tu luan chi co
MOT y, trai voi quy uoc da chot (tu luan phai tu hai y tro len). Muon nhap
thi phai tach thanh hai y, vi du: (a) lap he bat phuong trinh va tim toa do
cac dinh cua mien nghiem; (b) tim gia tri lon nhat cua F.

## Kiem chung noi dung KHONG bi lam sai lech

Chay ham goc va ham da doi ten voi CUNG hat ngau nhien (ca random lan
numpy.random) roi so tung ky tu: 8/8 ham GIONG HET.

## Kiem chung doc lap dang "mien nghiem la da giac gi"

Tu giai he bat phuong trinh bang phan so huu ti: lay giao diem tung cap
duong bien, giu lai diem nao thoa man CA HE, roi dem so dinh. Soi 120 cau:
0 lech. Ghi nhan them: phan bo chi ra "tam giac" (55) va "ngu giac" (65) -
khong bao gio ra tu giac hay luc giac, nen hai phuong an do khong bao gio
la dap an. Khong sai, nhung co Lan co the noi rong khoang tham so cho da dang.

## Da kiem chung the nao

1. So tung ky tu voi ban goc: 8/8 ham giong het.
2. 120 cau dang "da giac gi" doi chieu bang cach tu dem dinh: 0 lech.
3. Soi tay dang "nhan ra BPT bac nhat hai an": dap an luon dung.
4. 6/6 dang chay qua duong ra de that, dung loai cau, 0 loi.
5. Bien dich THAT 16 cau ra PDF 9 trang, 0 loi (co ca cau co hinh TikZ).
6. 391 bai test qua, 8 bo qua.

## Tong ket lop 10 sau dot nay

    chuong 1   34 dang,  34 co ham
    chuong 2   14 dang,   6 co ham
    chuong 3   38 dang,  38 co ham
    chuong 9   27 dang,  13 co ham
    con lai (4, 5, 6, 7, 8) chua co ham
    LOP 10: 288 dang, 91 da co ham (32%)

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.95 - 2026-09-29

## Chuong 3: them 9 dang, phu cac LOAI CAU con trong (38 -> 47 dang)

Co Lan: "cung 1 dang co the ra 3 den 4 loai, tu nhieu lua chon, dung sai,
tra loi ngan, tham chi ca tu luan... 1 ID mapping da co rat nhieu ID ham roi."

Soi lai bang loai cau cua chuong 3 thi thay lo ro:

    KHONG CO CAU TU LUAN NAO ngoai VD036, va NB029 chi toan trac nghiem.

Dot nay lap cac o trong do:

    NB029   MC A,B,C,D                     -> them SA_A
    TH030   MC A,B  SA A                   -> them TL_A
    TH032   MC A,B  SA A,B                 -> them TL_A
    TH033   MC A,B  SA A,B                 -> them TL_A
    TH034   MC A,B  SA A,B                 -> them TL_A
    TH035   MC A,B,C  SA A                 -> them SA_B, TL_A
    Dung/Sai theo chuong: A,B,C            -> them D, E

Chuong 3: 47/47 dang deu da co ham.

## Chin dang moi

    NB029_SA_A  doc sin / cosin tu toa do diem tren nua duong tron don vi
    TH030_TL_A  biet sin va khoang goc -> tinh cosin, roi tinh gia tri bieu thuc
    TH032_TL_A  dinh li cosin: tinh canh thu ba, roi tinh cosin mot goc khac
    TH033_TL_A  dinh li sin: tinh ban kinh ngoai tiep, roi tinh mot canh
    TH034_TL_A  Heron: tinh dien tich, roi tinh ban kinh duong tron noi tiep
    TH035_SA_B  giai tam giac c-g-c: so do goc con lai (lam tron)
    TH035_TL_A  giai tam giac khi biet mot canh va hai goc ke
    TF_D        gia tri luong giac doc tu toa do diem tren nua duong tron
    TF_E        dinh li sin, cong thuc dien tich va quan he giua chung

Hai ham Dung/Sai moi deu xep bon y theo bac NB -> TH -> VD -> VDC, nen qua
duoc tests/test_cau_dung_sai.py ma khong can ghi vao danh sach cho.

## De so lieu dep va dap an tra loi ngan la MOT SO

Cau tu luan TH030_TL_A: he so cua bieu thuc P duoc chon la boi cua mau so
(huyen cua bo ba Pythagore), nen P luon ra SO NGUYEN.
Cau tra loi ngan NB029_SA_A: chi lay bo ba co thuong so thap phan huu han.
Cau tra loi ngan TH035_SA_B: dap an la so do goc lam tron hai chu so.

## Da kiem chung the nao

1. TH033_TL_A: 72 truong hop, doi chieu DOC LAP bang toa do (dung ban kinh
   ngoai tiep tu ba dinh, va canh tu dinh li sin) - 0 lech.
2. Heron / r = S/p / R = abc/(4S): do lai ca 24 tam giac trong BANG_HERON - 0 lech.
3. TH035_SA_B: 80 cau, tu tinh lai goc B bang arccos - 0 lech.
4. TF_D: 60 cau, kiem diem co THUC SU nam tren duong tron don vi (x^2+y^2=1) - dung het.
5. Chin ham deu chay 15/15 lan, dung so cau yeu cau.
6. 47/47 dang chay qua duong ra de that, dung loai cau, 0 loi.
7. Bien dich THAT 18 cau ra PDF 7 trang, 0 loi; doc lai doi chieu
   (6-8-10 -> p=12, S=24, r=2).
8. 402 bai test qua, 8 bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.96 - 2026-09-29

## Chuong 2: viet ham cho 8 dang con trong + 1 dang moi (6 -> 15 dang co ham)

Truoc dot nay chuong 2 co 14 dang nhung chi 6 dang co ham, va TOAN LA trac
nghiem: khong co cau tra loi ngan, tu luan hay dung/sai nao. Nay 15/15 dang
deu da co ham.

    NB023   MC_A          -> them SA_A (dang moi)
    NB025   (chua co ham) -> MC_A
    TH024   MC_A, MC_B    -> them TL_A
    NB026   (chua co ham) -> MC_A
    TH027   MC_A, MC_B    -> them TL_A
    VD028   MC_A          -> them SA_A, TL_A
    TF      (chua co ham) -> TF_A, TF_B

## Chin dang moi

    NB023_SA_A  tinh gia tri ve trai cua bat phuong trinh tai mot diem
    NB025_MC_A  chon bat phuong trinh mo ta dung tinh huong thuc te
                (mua but, gio cong xuong may, khoi luong hang tren xe)
    TH024_TL_A  cac buoc ve mien nghiem: tim hai giao diem cua duong bo voi hai truc
    NB026_MC_A  nhan ra he bat phuong trinh bac nhat hai an
    TH027_TL_A  mien nghiem la tam giac vuong: tim ba dinh, tinh dien tich
    VD028_SA_A  gia tri lon nhat cua F = px + qy tren mien nghiem
    VD028_TL_A  bai toan toi uu thuc tien (xuong san xuat hai loai san pham)
    TF_A        bat phuong trinh bac nhat hai an
    TF_B        he bat phuong trinh va bai toan toi uu

Hai ham Dung/Sai deu xep bon y theo bac NB -> TH -> VD -> VDC.

## De so lieu luon dep: chon DINH truoc, viet bat phuong trinh sau

_mien_tu_giac() khong sinh bat phuong trinh roi moi giai tim dinh (lam nhu
the giao diem hay ra phan so xau). Nguoc lai: chon truoc ba dinh nguyen
P(m;0), Q(u;v), R(0;n) roi moi viet hai duong thang di qua chung, nen bon
dinh cua mien nghiem CHAC CHAN nguyen. Con loc them dieu kien Q nam ngoai
doan PR (de thanh tu giac loi) va F dat gia tri lon nhat tai DUY NHAT mot
dinh (de dap an khong nhap nhang).

TH024_TL_A: chon c = a.b.k nen hai giao diem voi hai truc deu nguyen.
TH027_TL_A: chon m.n chan nen dien tich m.n/2 la so nguyen.

## Da kiem chung the nao

1. Mien tu giac: 400 truong hop. TU TIM dinh bang cach lay giao tung cap
   trong bon duong bo (dung phan so huu ti) roi giu diem thoa CA HE -
   khop 100% voi bon dinh ham khai. 0 lech.
2. Gia tri lon nhat cua F: voi ca 400 mien do, QUET LUOI buoc 1/4 tren
   toan mien roi so voi gia tri lon nhat tinh tai cac dinh - 0 lech.
3. TF_A: 120 cau. Y d) dem cap so nguyen: tu dem lai - 0 sai. Y b) xet mot
   cap so co la nghiem khong: tu thay so - 0 sai.
4. Chin ham deu chay 15/15 lan, dung so cau yeu cau.
5. 15/15 dang chay qua duong ra de that, dung loai cau, 0 loi.
6. Bien dich THAT 18 cau ra PDF 8 trang, 0 loi; doc lai doi chieu
   (F(9;1) = 5.9 + 7.1 = 52 la gia tri lon nhat).
7. 411 bai test qua, 8 bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.97 - 2026-09-29

## Da ra duoc DE HE SO 1 tron ven cho bon chuong: 1, 2, 3, 9

Co Lan hoi: "lam sao de du so cau ra duoc de he so 1".

Cach do: chay CA DUONG RA DE that (blueprint -> chon cau -> goi ham sinh)
cho tung pham vi chuong, dem xem bao nhieu cho khong ra duoc cau va thieu o
dau. Luu y: chi nhin select_questions thoi thi KHONG DU, vi no mo i bao
thieu o Mapping; thieu HAM chi lo ra khi that su goi call_generator.

Truoc dot nay:

    chuong 1   6/8 cau   thieu 3 dong Mapping
    chuong 2   du cau
    chuong 3   du cau
    chuong 9   1/6 cau   thieu 9 ham

Sau dot nay, chay 20 de moi chuong:

    chuong 1   160/160 cau   DU CAU
    chuong 2   121/121 cau   DU CAU
    chuong 3    79/79  cau   DU CAU
    chuong 9   123/123 cau   DU CAU
    chuong 4, 5, 6, 7, 8: chua co ham (4 den 18 cho thieu moi chuong)

## Chuong 1: them ba dang ma tran doi nhung Mapping chua khai

    VD014_TL_A  tu luan: xet tinh dung sai cua menh de keo theo va menh de dao
    VD020_SA_A  tra loi ngan: dem phan tu tap hop trong bai toan thuc te
                (dung n(A hop B) = n(A) + n(B) - n(A giao B))
    VD021_TL_A  tu luan: phep toan tap hop chua tham so tren truc so

VD021_TL_A dung lai dung phan sinh de va loi giai da kiem chung cua dang
VD021 (_VD021_de_giai): y (a) dem so gia tri m de giao bang rong, y (b) tim
m nho nhat de giao khac rong - hai cau hoi bo sung cho nhau va cung can
n < a nen dung chung mot bo so lieu.

## Chuong 9: them tam cau NHAN BIET va mot cau tu luan

Ngan hang chuong 9 truoc do chi toan cau tinh toan muc TH/VD, khong co cau
nhan biet khai niem nao - ma ma tran de he so 1 lai doi nhung cau do.

    NB142_MC_A  nhan biet phep thu ngau nhien
    NB143_MC_A  khong gian mau (xuc xac / dong xu / rut the)
    NB145_MC_A  bien co khong the
    NB146_MC_A  bien co chac chan
    NB147_MC_A  bien co doi
    NB148_MC_A  nguyen li xac suat be
    NB149_MC_A  dinh nghia co dien cua xac suat
    NB153_MC_A  cac tinh chat co ban cua xac suat
    VD155_TL_A  tu luan: gieo hai xuc xac, mo ta khong gian mau va tinh xac suat

Cau NB148 co ghi ro trong loi giai hai cho hoc sinh hay nham: xac suat be
KHONG co nghia la "khong bao gio xay ra", va neu P(A) rat be thi
P(A ngang) = 1 - P(A) lai rat GAN 1 chu khong he be.

## Da kiem chung the nao

1. Chay 20 de he so 1 cho MOI chuong, goi ham sinh that tung cau:
   chuong 1, 2, 3, 9 ra du 100% so cau, 0 loi.
2. Quet ca lop 10 qua duong ra de: 121 dang chay dung loai cau, 0 loi.
3. Ra DE THAT cho ba chuong 1, 3, 9 roi bien dich: 17 cau, PDF 6 trang, 0 loi.
4. Muoi hai ham moi deu chay 12-15/15 lan, dung so cau yeu cau.
5. 415 bai test qua, 8 bo qua.

## Con lai de ra duoc de he so 1 cho ca lop 10

    chuong 4    4 cho thieu
    chuong 5   17 cho thieu
    chuong 6   13 cho thieu
    chuong 7   18 cho thieu
    chuong 8   11 cho thieu

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.98 - 2026-09-28

## De he so 1 ra THIEU CAU ma KHONG BAO GI - da sua

Co Lan hoi: "chuong 3 con it. co the lam them duoc khong". Do lai thi
KHONG phai do thieu dang: de he so 1 chuong 3 chi ra 5/12 cau, va nam cau
kia BIEN MAT lang le - khong ra cau, cung khong co dong
[THIEU O PYTHON --- ID: xxx] nao. Day la dieu trai voi nguyen tac "bao
thieu chu khong vo de" da chot tu truoc.

Hai nguyen nhan, deu nam o buoc CHIA CAU chu khong nam o ngan hang ham.

### 1. Chia cau cho bai KHONG CO yeu cau o muc do do

So cau duoc chia ve tung bai theo TI LE SO TIET, hoan toan khong kiem tra
bai ay trong Curriculum co yeu cau nao o muc do dang xet hay khong.
Chuong 3 chi co DUNG MOT yeu cau muc NB (bai 5) va DUNG MOT yeu cau muc VD
(bai 6), nhung bo chia van rai:

    trac nghiem NB    B5: 1, B6: 2    B6 khong co NB nao   -> mat 2 cau
    tra loi ngan VD   B5: 1           B5 khong co VD nao   -> mat 1 cau
    tu luan VD        B5: 2, B6: 1    B5 khong co VD nao   -> mat 2 cau

_chon_curriculum_id tra ve rong, va so cau ay roi mat khong dau vet.

Nay them hai ham _don_ve_bai_co_cau (muc NB/TH) va _don_vd_ve_bai_co_cau
(muc VD/VDC): phan cua bai khong co yeu cau duoc don sang bai co, uu tien
bai dang duoc chia nhieu cau nhat, van giu quy uoc moi bai toi da 1 cau
VDC. Neu trong phan bo khong con bai nao nhan duoc thi mo rong ra MOI BAI
thuoc pham vi de - bai co yeu cau nhung khong duoc chia cau nao van la cho
don hop le. (Thieu buoc mo rong nay thi chuong 3 van mat cau trac nghiem
muc VD, vi ca suat VD roi vao bai 5 trong khi yeu cau VD duy nhat o bai 6.)

Neu ca chuong that su khong co yeu cau nao o muc do do thi ghi vao
bao_cao_phan_bo["khong_du_yeu_cau"] de co Lan nhin thay, khong im lang nua.

### 2. Cau Dung/Sai an suat muc do cua cac phan khac

Thiet ke cu: moi cau Dung/Sai da chua san 4 y NB/TH/VD/VDC nen tru 1 suat
NB + 1 TH cua trac nghiem (_tru_phan_dung_sai) va 1 suat VD + 1 VDC cua
phan dung truoc (ngan_sach_ds). Voi chuong 3 dieu nay an sach ca cau trac
nghiem muc VD.

Co Lan chot 28/09/2026: "cu lam theo dung muc do la duoc. vi quan trong
muc do se anh huong diem so. muc do khac di se lam diem so ko phan anh dung
cai ma nguoi kiem tra mong muon."

Nay BO ca hai phep tru. Moi phan ra dung so cau tung muc do ma tran ghi,
khong bu tru cheo giua cac phan. Ham _tru_phan_dung_sai giu lai de tham
khao nhung khong con duoc goi.

### 3. Them ham con thieu: L10_C9_B27_TH151_MC_A_01

Mapping da co tu truoc nhung chua co ham. Gieo hai xuc xac, tinh xac suat
tong so cham bang mot so cho - thi nghiem don gian nhat ma hoc sinh lap
duoc khong gian mau day du (36 ket qua), dung muc Thong hieu. Ba phuong an
nhieu la ba loi hay gap: dem thua mot cap, dem thieu mot cap, va chia nham
cho 6 thay vi 36.
GHI CHU: ham nay CLAUDE THEM 28/09/2026 - co Lan kiem tra lai noi dung.

## Ket qua

Truoc:

    chuong 1    8/12 cau
    chuong 2    6/12 cau
    chuong 3    5/12 cau
    chuong 9    6/12 cau

Sau, chay 5 lan bat de moi chuong (ma tran he so 1 doi 12 cau:
trac nghiem 6, dung/sai 1, tra loi ngan 2, tu luan 3):

    chuong 1   5/5 de du ma tran   60/60 cau sinh duoc
    chuong 2   5/5 de du ma tran   60/60 cau sinh duoc
    chuong 3   5/5 de du ma tran   60/60 cau sinh duoc
    chuong 9   5/5 de du ma tran   60/60 cau sinh duoc

Muc do ra dung ma tran: NB 4, TH 1, VD 6, cong 1 cau Dung/Sai cau lon.

## Da kiem chung the nao

1. Chay 5 seed x 4 chuong, dem theo TUNG PHAN: du ca 4 phan, khong phan
   nao hut.
2. Goi ham sinh THAT cho tung cau (khong chi nhin select_questions):
   240/240 cau ra duoc, 0 loi.
3. Them tests/test_du_cau_he_so_1.py - 29 bai test khoa lai: de phai du
   cau, va neu co cau khong xep duoc vao bai nao thi PHAI bao, khong duoc
   bien mat.
4. 445 bai test qua, 8 bo qua (truoc dot nay la 415).

Luu y moi truong: khong bien dich duoc PDF tren may co Lan vi thieu
tabvar.sty; VPS co du bo TeX Live nen van dich binh thuong. Da kiem tra
khau SINH CAU rieng, khong qua PDF.

## Con lai de ra duoc de he so 1 cho ca lop 10

    chuong 4    4 cho thieu
    chuong 5   17 cho thieu
    chuong 6   13 cho thieu
    chuong 7   18 cho thieu
    chuong 8   11 cho thieu

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 2.99 - 2026-09-28

## Mot yeu cau NB co the co NHIEU DANG - them ba dang cho L10_C3_B5_NB029

Co Lan chi ra: khong can bo sung yeu cau vao Curriculum, vi MOT yeu cau
Nhan biet von da de ra duoc nhieu dang khac nhau. Co neu ba vi du cho bai
"Gia tri luong giac cua mot goc tu 0 do den 180 do":

    1. Xet dau: goc alpha tu 0 den 90 thi cos alpha > hay < 0; de tu sinh
       ra sin, tan, cot.
    2. Ve goc alpha tren he truc, diem M, hoi ve toa do x_M, y_M,
       x_M/y_M... la sin, cos, tan hay cot.
    3. Ve goc va he truc: voi cos > 0 thi goc tu dau den dau.

Da kiem chung truoc khi viet: bo chon cau CO xoay vong cac chu cai. Khi
NB029 duoc chon 4 lan trong mot de thi ra 4 dang KHAC NHAU, va thu tu doi
theo tung de. Nen them dang la co tac dung ngay, khong can sua gi them.

Ba dang moi (deu la CLAUDE THEM 28/09/2026, co Lan kiem tra lai):

    NB029_MC_E  Xet dau gia tri luong giac khi biet khoang cua goc
    NB029_MC_F  Doc gia tri luong giac theo toa do diem M TREN HINH VE
    NB029_MC_G  Biet dau gia tri luong giac, suy ra khoang cua goc

Truoc: 4 dang trac nghiem duoi NB029. Nay: 7 dang.

## Hai cho phai can than khi viet ba dang nay

### Hinh ve khong duoc mau thuan voi de

Ban dau dang MC_G ve san mot goc cu the. Nhung de cho dau
(vi du cos alpha < 0) roi hoi goc nam trong khoang nao - neu hinh ve san
goc thoa man gia thiet thi hoc sinh doc thang dap an tren hinh, cau hoi
mat het y nghia; tram trong hon, ban chay thu dau tien ra hinh goc NHON
trong khi de cho cos alpha < 0, tuc la hinh SAI so voi de.

Nay MC_G dung hinh rieng _hinh_nua_duong_tron_hai_phia(): ve HAI vi tri
mau cua M, mot ben phai va mot ben trai truc Oy, kem hoanh do x_M va x_N.
Hoc sinh thay duoc dau cua hoanh do doi ra sao ma van phai tu chon khoang.

### Hai dau mut cua khoang

Cac khoang ghi trong MC_G la khoang DUNG BANG tap nghiem, da xet ca hai
dau mut:

    cos alpha > 0   <=>   0 <= alpha < 90
    cos alpha < 0   <=>   90 < alpha <= 180   (vi cos 180 = -1 < 0)
    tan alpha > 0   <=>   0 < alpha < 90      (vi tan 0 = 0)
    tan alpha < 0   <=>   90 < alpha < 180    (vi tan 180 = 0)

Phuong an nhieu deu la khang dinh SAI, khong dung
"0 <= alpha <= 180" lam nhieu vi cai do gia thiet da cho, tuc la DUNG.

## Da kiem chung the nao

1. Chay 40 lan moi dang: khong loi, moi cau dung MOT dap an dung, bon
   phuong an doi mot khac nhau, ra 23-26 bo phuong an khac nhau.
2. Hai hinh moi dich qua duong ra hinh cho web (dich_hinh) deu ra anh,
   va da XEM TAN MAT anh de kiem tra. Lan dau nhan y_M cham vao cung tron
   khi goc lon nen da ha goc toi da xuong 60 do.
3. Chay 8 de chuong 3: ca bay dang NB029 deu duoc dung
   (MC_A 3, MC_B 3, MC_C 7, MC_D 4, MC_E 6, MC_F 5, MC_G 4).
4. 445 bai test qua, 8 bo qua.

## Ap dung tiep

Cach nay dung cho MOI chuong, khong rieng chuong 3: chuong nao it yeu cau
trong Curriculum thi them DANG duoi yeu cau san co, khong phai them yeu
cau moi.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.00 - 2026-09-28

## Van dung cung nhieu phien ban: them ba dang cho L10_C3_B6_VD036

Co Lan: "Van dung cung co the lam nhieu phien ban khac nhau: cac bai ve do
chieu cao, ngay ca bai do nui kinh dien cua luong giac, do ban kinh trai
dat... do cay, do toa nha, di chuyen tren bien. Kiem tra tren mang, cac
bai toan van dung cua sach giao khoa, sach bai tap. Rat nhieu."

Va co dan them: "luu y co nh cach giai, co cach giai su dung kien thuc lop
11, khong duoc dung. chi dung pp ma don vi kien thuc nam trong lop 10 dang
hoc."

Da tra cuu cac dang bai thuc te cua chuong nay truoc khi viet (do chieu
cao, do khoang cach khong toi duoc, tau thuyen doi huong, dien tich manh
dat). Truoc dot nay VD036 da co 8 dang; nay 11 dang.

    VD036_MC_D  Do chieu cao vat cao bang HAI GOC NANG bat ki
    VD036_TL_D  Tau doi huong tren bien: dinh li cosin roi dinh li sin
    VD036_TL_E  Do ban kinh Trai Dat bang goc ha toi duong chan troi

## Da giu dung rang buoc "khong dung kien thuc lop 11"

Bai do ban kinh Trai Dat quen thuoc nhat la cach cua Eratosthenes, dung
DO DAI CUNG TRON l = R.alpha voi alpha tinh bang radian - day la chuong
trinh LOP 11, da KHONG dung.

Cach dung o day chi can tam giac vuong, nam tron trong lop 10: tu dinh nui
M cao h, tia nhin toi duong chan troi tiep xuc mat bien tai T nen
OT vuong goc MT. Goi theta la goc ha so voi phuong nam ngang thi
goc OMT = 90 - theta, suy ra cos(theta) = R/(R+h) va
R = h.cos(theta)/(1 - cos(theta)).

Dang MC_D cung vay: chi dung dinh li sin trong tam giac ABD roi ti so
luong giac trong tam giac vuong BDH, khong dung cong thuc cong hay nhan
doi.

## Hai cho da phai sua giua chung

### Bai ban kinh Trai Dat KHONG lam trac nghiem duoc

Ban dau viet thanh trac nghiem. Nhung vi cos(theta) rat gan 1 nen phuong
an nhieu "quen nhan cos(theta)", tuc la h/(1 - cos theta), ra 6311 km
trong khi dap an dung la 6310 km - hai dap an deu dung, cau hoi hong.
Con moi bien the sai khac thi lai lech han ve co h (vai ki-lo-met), nhin
la loai duoc ngay, khong phai phuong an nhieu tu te.

Ket luan: bai nay khong co bo phuong an nhieu dung nghia. Da chuyen thanh
TU LUAN ba y - chung to tam giac OTM vuong, chung minh cos(theta) =
R/(R+h), roi tinh R. Cho phai danh gia la lap duoc he thuc, dung cho do.

### Phuong an trac nghiem phai cung dang so

Dang MC_D hoi "lam tron den hang phan muoi" nhung ham _xx cat duoi so 0,
nen co phuong an ra so nguyen (90 m, 61 m) ben canh phuong an co thap
phan (76,3 m). Hoc sinh nhin DANG SO cung doan duoc dap an. Nay ep moi
phuong an dung MOT chu so thap phan.

## Da kiem chung the nao

1. Dung TOA DO dung lai hinh de kiem cong thuc, khong tin cong thuc minh
   vua viet: chieu cao do bang hai goc nang lech 1e-14; AC va goc BAC cua
   bai tau bien khop tuyet doi; bai Trai Dat chay vong kin tu R = 6371 ra
   theta roi tu theta ra lai R, lech 0,2 den 1,0 phan tram do lam tron
   theta ve hai chu so.
2. Chay 30 lan moi dang: 30/30 ra cau, khong loi, cau trac nghiem luon
   dung MOT dap an dung.
3. Chay 10 de chuong 3: 120/120 cau sinh duoc, ca 11 dang VD036 deu duoc
   dung.
4. 447 bai test qua, 8 bo qua.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.01 - 2026-09-28

## Chuong 9 da du ham cho MOI dang trong Mapping (23/27 -> 27/27)

Bon dang con lai da duoc khai trong Mapping tu truoc nhung chua co ham:

    L10_C9_B26_NB143_SA_A  So phan tu cua khong gian mau
    L10_C9_B26_TH150_MC_A  Mo ta khong gian mau va bien co (dong xu, xuc xac)
    L10_C9_B26_TH150_SA_A  So phan tu cua bien co
    L10_C9_B27_TH152_SA_A  Xac suat cua bien co doi

Deu la CLAUDE THEM 28/09/2026 - co Lan kiem tra lai noi dung.

## Hai cho da phai sua

### Cau TRA LOI NGAN van phai truyen ba phuong an nhieu

Lan dau viet ba ham SA voi dsnhieu rong, chay 0/30 lan ra cau, bao
NhieuTrungError. Doc lai math_type.py thay MC_SA_answer_text va
MC_SA_answer_const goi _chon_ba_nhieu NGAY TU DAU, roi moi bo phan
\choice di khi dang=2. Tuc la du cau tra loi ngan khong in phuong an
nhieu, van phai truyen du ba cai. Da bo sung, dung _ba_nhieu9 de bao dam
ba phuong an doi mot khac nhau.

### Dap so cau tra loi ngan phai la so thap phan HUU HAN

Cau xac suat bien co doi neu lay "gieo mot con xuc xac" thi dap so hay
ra 5/6 = 0,8333... Cau tra loi ngan cham bang so khop dung chuoi nen hoc
sinh lam dung van co the go ra so khac. Da doi sang "chon mot so nguyen
duong khong vuot qua N, chia het cho k" va chi giu nhung cap (N; k) cho
ket qua thap phan huu han.

## Da kiem chung the nao

1. Chay 30 lan moi dang: 30/30 ra cau, khong loi; cau trac nghiem dung
   MOT dap an dung, cau tra loi ngan dung MOT \shortans.
2. 450 bai test qua, 8 bo qua.

## Hien trang toan lop 10 - so dang CO HAM tren tong so dang Mapping

    C1   37/37   xong
    C2   15/15   xong
    C3   53/53   xong
    C4    0/39
    C5    0/41
    C6    0/31
    C7    0/37
    C8    0/27
    C9   27/27   xong

Bon chuong 1, 2, 3, 9 deu ra duoc de he so 1 tron ven. Nam chuong
4, 5, 6, 7, 8 CHUA CO MOT HAM NAO - moi chi co Curriculum va Mapping.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.02 - 2026-09-28

## Chuong 8 (Dai so to hop): tu 0 len 30/30 dang co ham

Co Lan gui lai nam tep LopXChuong4/5/6/7/8.py. Rieng tep chuong 8 da viet
theo FORM MOI (goi MC_SA_answer_*, TF_baitoan_du cua math_type) nen chuyen
duoc; bon tep con lai van la form cu (tu mo tep de.tex roi de.write).

Co Lan dan: KHONG duoc sua math_type.py, chi viet lai HAM CUA TUNG CHUONG
cho dung khuon cua math_type. Da lam dung the - math_type.py giu nguyen,
khong mot dong nao thay doi.

Nay data/python_bank/toan10/L10_C8.py co 30 ham, phu kin 30 dong Mapping:

    Bai 23  quy tac dem          10 dang
    Bai 24  hoan vi, chinh hop, to hop  11 dang
    Bai 25  nhi thuc Newton       7 dang
    Dung/Sai                      2 dang

## Ba dang phai them de de he so 1 du cau

Lan chay thu dau tien: 5/5 de du ma tran nhung chi sinh duoc 48/60 cau.
Bo chon can TRA LOI NGAN cho VD130 va VD138, can TU LUAN cho VD141, ma
Mapping chua khai. Da them ba dang:

    L10_C8_B23_VD130_SA_A  dem thuc tien dung quy tac cong va nhan
    L10_C8_B24_VD138_SA_A  dem so cach chon nhom co dieu kien thanh phan
    L10_C8_B25_VD141_TL_A  khai trien nhi thuc Newton va cac he so

## Loi trong tep cua co - da sua khi chuyen

1. K10_8_25_1_B dinh nghia HAI LAN (dong 292 va 363), ban sau de ban
   truoc. Khi chuyen chi giu mot.
2. K10_8_DS_1_TH co vong "while l > n: k = np.randint([1, n-1])" - truyen
   mot LIST cho randint va khong cap nhat l, roi vao la treo may. Da bo.
3. K10_8_DS_1_TH co bon y ngang muc nhau. Da xep lai theo dung thang
   NB - TH - VD - VDC nhu quy uoc chot 27/09/2026 (nay la L10_C8_TF_B).
4. K10_8_23_2_Ngan_1_NB viet $C_{blue}^{2}$ bang f-string nen ra "C_9^2"
   khong co ngoac nhon; so hai chu so se hien sai (C_10^2 thanh C_1 roi
   0^2). Da viet lai co ngoac day du (nay la L10_C8_B23_TH127_SA_A).

## Da kiem chung the nao

1. Chay 10 lan moi dang cho ca 30 dang: 30/30 khong loi; cau trac nghiem
   dung MOT dap an dung, tra loi ngan dung MOT shortans, Dung/Sai dung
   BON y.
2. Doi chieu ket qua dem bang VET CAN chu khong tin cong thuc:
   - chon 2 vien bi cung mau: khop
   - so co d chu so tu tap 1..k: khop
   - xep n nguoi sao cho hai ban canh nhau / khong canh nhau: khop
   - chon 2 hoc sinh cung gioi tinh: khop
   - he so khai trien (a+bx)^n voi n = 4, 5: khop sympy o MOI truong hop
   - tong cac he so = (1+a)^n: khop
3. De he so 1 chuong 8: 5/5 de du ma tran, 60/60 cau sinh duoc.
4. Them chuong 8 vao tests/test_du_cau_he_so_1.py. 472 bai test qua,
   8 bo qua (truoc dot nay la 450).

## Hien trang toan lop 10

    C1   37/37   xong        C6    0/31
    C2   15/15   xong        C7    0/37  (chua co nguon)
    C3   53/53   xong        C8   30/30   xong
    C4    0/39               C9   27/27   xong
    C5    0/41

Nam chuong 1, 2, 3, 8, 9 deu ra duoc de he so 1 tron ven.

## Con lai

Tep LopXChuong7.py co Lan gui LAI LA NOI DUNG CHUONG 9 (toan ham
K10_9_*, xac suat), khong phai phuong phap toa do trong mat phang. Chuong
7 van chua co nguon.

Bon tep chuong 4, 5, 6 o form cu, phai viet lai ham cho dung khuon
math_type. Da doc va ghi nhan cac loi can sua khi chuyen - xem muc duoi.

## Loi da ghi nhan trong tep chuong 4, 5, 6 (chua sua, de doi chuyen)

    C6 K10_6_15_1_1   \True dat vao bang X1 - ma X1 chinh la bang co chu
                      thich "KHONG phai ham so" (co mot gia tri x lap
                      lai). DAP AN DUNG DANG DAT NHAM VAO PHUONG AN SAI.
    C5 K10_5_13_2_1   co input() nen treo khi sinh de tu dong; de hoi
                      TRUNG VI nhung lai tinh numpy.mean; loi giai dung
                      bien "median" chua he duoc gan -> NameError.
    C5 K10_5_14_1_1   de ghi can nang tre so sinh "don vi kg" nhung so
                      lieu la 2700-4200 (gam).
    C5 K10_5_14_1_3   numpy.delete(X, i) voi i la GIA TRI chu khong phai
                      chi so.
    C6 K10_6_18_1_1   nghiem_hq[1] se IndexError khi phuong trinh co it
                      hon hai nghiem; {$\True S = \varnothing$} dat \True
                      BEN TRONG $...$ nen LaTeX hong.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.03 - 2026-09-28

## Chuong 4 (Vecto): tu 0 len 40/40 dang co ham

Tep LopXChuong4.py cua co Lan o FORM CU (tu mo tep de.tex roi de.write),
chi co 6 ham. Da viet lai toan bo cho dung khuon math_type -
math_type.py GIU NGUYEN, khong sua mot dong nao, dung nhu co Lan dan.

Noi dung toan cua co duoc giu o cac dang:

    NB038_MC_A  hinh chu nhat, hai trung diem, hoi khang dinh nao SAI
                (tu K10_2_3_1_2_NB)
    TH041_MC_B  hinh vuong, tam O, tong hai vecto doi
                (tu K10_2_3_1_3_TH)
    TH048_MC_A  trong tam tam giac (tu K10_2_3_1_4_TH)
    VD060       ba luc can bang (tu K10_2_3_2_1_VD)
    VD061       phan tich mot vecto theo hai vecto khong cung phuong
                (y cua K10_2_3_3_1_VD)

Da kiem lai bang toa do: noi dung toan cua co o NB038, TH041, TH048 DUNG.
Rieng NB038 ban cu hong LaTeX - phuong an thu tu thua mot dau }, va khoi
tikzpicture dat sau \choice nen hinh roi ra ngoai o hinh; da sua.

Them dang TH041_MC_B (Mapping chua khai) de giu bai hinh vuong cua co.

## CO HINH VE - dung yeu cau co Lan chot

Sau dang co hinh, deu da dich thu qua duong ra hinh cho web:
NB037 (hinh binh hanh), NB038 (hinh chu nhat + hai trung diem),
TH040_MC_B (hinh binh hanh), TH041_MC_B (hinh vuong + hai duong cheo),
TH048 (tam giac + trong tam), NB057 (tam giac deu),
VD061 (tam giac + diem M tren canh), TF_A (hinh binh hanh + tam O).

## Ba loi da vap phai va da sua

### 1. Dau phay thap phan lam HONG toa do TikZ

Ham _xx4 doi dau cham thanh dau PHAY theo cach viet so cua Viet Nam. Lan
dau dung luon _xx4 de viet toa do TikZ, nen (4.4, 2.2) thanh (4,4, 2,2) -
TikZ doc thanh bon so, hinh ve meo hoan toan. Da XEM TAN MAT anh moi phat
hien. Nay them ham rieng _toa() luon dung dau CHAM cho toa do.

### 2. Bang cap luc go tay bi SAI mot dong

CAP_LUC_60 (cac cap p, q lam cho p^2 + pq + q^2 chinh phuong, dung cho
bai ba luc can bang goc 60 do) ban go tay co cap (16; 19; 31) - nhung
16^2 + 16*19 + 19^2 = 921 chu khong phai 31^2 = 961. De nguyen thi bai ba
luc ra DAP SO SAI. Nay tinh bang may thay vi go tay, duoc 26 cap, da kiem
lai tat ca deu dung.

### 3. Ba dang trung phuong an nhieu

TH053_MC_A, TH058_MC_A, VD061_MC_A co luc sinh ra hai phuong an nhieu
giong het nhau (vi du goc 90 do thi tich vo huong bang 0 va so doi cua no
cung bang 0; hoac k = 1/2 thi hai he so bang nhau). Da loc qua _ba_nhieu4.

## Da kiem chung the nao

1. Chay 25 lan moi dang cho ca 40 dang: 40/40 khong loi; trac nghiem dung
   MOT dap an dung, tra loi ngan dung MOT shortans, Dung/Sai dung BON y.
2. Dung TOA DO kiem lai toan, doc lap voi cong thuc trong ham:
   - hinh chu nhat: DA = -MN (nen "DA = MN" dung la khang dinh SAI), ba
     khang dinh con lai deu dung
   - hinh binh hanh: AB = DC, AD = BC
   - ba luc goc 60 do: moi cap deu cho |F3| nguyen
   - tam giac vuong can dung tu bo ba Pytago: AB.AC = 0 va |AB| = |AC|
   - AM = (1-k)AB + k.AC: khop voi toa do
   - dien tich |x1y2 - x2y1|/2: khop cong thuc Heron qua 300 bo so
3. 488 bai test qua, 8 bo qua (truoc dot nay la 472).

## CAN CO LAN QUYET: de he so 1 chuong 4 chi ra duoc 6 cau

Khong phai loi. load_scope_heso1 lay bai trong chuong cho den khi gap bai
co boundary_after, ma bai 8 CO boundary_after, nen de he so 1 chuong 4
chi gom BAI 7 va BAI 8 - dung PPCT cua co.

Nhung trong Curriculum, bai 7 va bai 8 KHONG co yeu cau nao muc VD (bai 7
co 2 NB + 1 TH, bai 8 co 3 TH). Ma ma tran he so 1 doi 6 cau muc VD. Nen
de chi ra duoc 6 cau: 5 trac nghiem + 1 Dung/Sai, va bao_cao_phan_bo ghi
ro mat 6 cau o muc VD/VDC.

Muon de chuong 4 du 12 cau thi phai bo sung yeu cau muc VD cho bai 7
hoac bai 8 trong data/curriculum/toan10/L10_C4.json - day la SUA CHUONG
TRINH nen khong tu lam, cho co Lan quyet.

(Cac bai 9, 10, 11 deu da co du ham va deu co yeu cau muc VD, nen khi ra
de giua ky / cuoi ky co pham vi rong hon thi dung duoc ngay.)

## Hien trang toan lop 10

    C1   37/37   xong        C6    0/31
    C2   15/15   xong        C7    0/37  (chua co nguon)
    C3   53/53   xong        C8   30/30   xong
    C4   40/40   xong*       C9   27/27   xong
    C5    0/41

(*) chuong 4 du ham cho MOI dang, nhung de he so 1 chi ra 6 cau vi ly do
o tren.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.04 - 2026-09-28

## SUA PHAM VI DE HE SO 1: chay HET CHUONG, khong dung o moc thi

Co Lan chot 28/09/2026: "he so 2 - de giua ky moi quan tam pham vi nay.
con he so 1 se chay theo chuong."

load_scope_heso1 truoc day lay bai trong chuong cho den khi gap bai co
boundary_after roi DUNG. Nhung boundary_after la moc cua cac KY THI
(GK1_EXAM, CK1_EXAM, GK2_EXAM, CK2_EXAM) - no danh cho de giua ky /
cuoi ky, khong danh cho bai kiem tra thuong xuyen.

Bon cho bi cat trong PPCT lop 10:

    L10_C4_B8  -> GK1_EXAM
    L10_C5_B14 -> CK1_EXAM
    L10_C7_B22 -> GK2_EXAM
    L10_C9_B27 -> CK2_EXAM

Hau qua do duoc: de he so 1 chuong 4 chi gom bai 7 va bai 8, ma hai bai
ay khong co yeu cau nao muc Van dung, nen de chi ra 6/12 cau. Chuong 5 va
chuong 7 cung bi cat tuong tu (chua lo ra vi hai chuong ay chua co ham).
Chuong 9 khong anh huong vi moc nam o bai cuoi cung.

Nay lay TOAN BO cac bai cua chuong. Pham vi moi:

    chuong 4  bai 7, 8, 9, 10, 11   (truoc: chi 7, 8)
    chuong 5  bai 12, 13, 14
    chuong 7  bai 19, 20, 21, 22
    cac chuong khac: khong doi

## Sau khi sua, chuong 4 thieu 6 dang nen da bo sung

Pham vi rong ra thi bo chon cau voi toi cac yeu cau muc Van dung o bai
10 va bai 11, nhung Mapping chua khai du loai cau, de mat 12/60 cau. Da
them:

    VD054_SA_A  do dai trung tuyen theo toa do
    VD055_SA_A  vi tri cua vat sau mot khoang thoi gian
    VD055_TL_A  toc do, vi tri va quang duong cua vat chuyen dong deu
    VD056_SA_A  dien tich tam giac theo toa do
    VD060_SA_A  do lon luc thu ba khi vat can bang
    VD061_SA_A  he so trong phan tich vecto theo trung diem, trong tam

Chuong 4 nay co 46 dang, deu co ham.

## Da kiem chung the nao

1. 46/46 dang chuong 4 chay tron 10/10 lan, khong loi.
2. De he so 1, chay 8 lan bat de moi chuong:

       chuong 1   8/8 du ma tran   96/96 cau sinh duoc
       chuong 2   8/8 du ma tran   96/96
       chuong 3   8/8 du ma tran   96/96
       chuong 4   8/8 du ma tran   96/96   (truoc dot nay: 0/5, 30/60)
       chuong 8   8/8 du ma tran   96/96
       chuong 9   8/8 du ma tran   96/96

3. Them chuong 4 vao tests/test_du_cau_he_so_1.py va ghi ro ly do sua
   pham vi ngay trong tep test. 500 bai test qua, 8 bo qua (truoc: 488).

## Hien trang toan lop 10

    C1   37/37   xong        C6    0/31
    C2   15/15   xong        C7    0/37  (chua co nguon)
    C3   53/53   xong        C8   30/30   xong
    C4   46/46   xong        C9   27/27   xong
    C5    0/41

Sau chuong 1, 2, 3, 4, 8, 9 deu ra duoc de he so 1 tron ven.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.05 - 2026-09-28

## Kiem tra duong ra DE HE SO 2 (giua ky) - bat duoc BON loi

Co Lan: "gio da xong chuong 1,2,3,4. da toi duoc he so 2. hay ra de he so
2. kiem tra hoat dong he so 2 truoc cho toi. de xem co loi gi ko de chinh
sua luon."

Pham vi de giua ky 1 lop 10 = chuong 1, 2, 3 va bai 7-8 cua chuong 4 -
dung phan da lam xong. Ma tran he so 2: trac nghiem 12, dung/sai 2,
tra loi ngan 4, tu luan 3 = 21 cau.

### Loi 1: de giua ky chi ra cau cua CHUONG 1 va CHUONG 2

Nang nhat. Pham vi 8 bai thuoc 4 chuong nhung 20 cau roi het vao chuong 1
va chuong 2; chuong 3 va chuong 4 KHONG co cau nao.

Nguyen nhan: _chia_theo_so_tiet lam tron xuong roi rai phan du theo thu
tu (-so tiet, ten) - lan nao cung DUNG MOT THU TU. De giua ky chia rieng
cho tung loai cau, nen hai bai nhieu tiet nhat thang o MOI loai cau, cac
bai con lai khong bao gio toi luot.

Da doi sang chia theo PHAN DU LON NHAT (largest remainder): bai bi lam
tron xuong nhieu nhat duoc uu tien, bai bang phan du thi boc ngau nhien
de cac loai cau khac nhau khong cung chon mot bai.

### Loi 2: buoc don cau lam chuong dau phinh ra

_don_ve_bai_co_cau don phan cua bai khong co yeu cau cho bai dang NHIEU
CAU NHAT - ma bai ay gan nhu luon la bai cua chuong dau. Do duoc: chuong
1 chiem 62% so cau du chi chiem 36% so tiet.

Da doi sang chia lai toan bo so cau cua muc do ay theo ti le so tiet,
chi tren nhung bai that su co yeu cau o muc do do.

### Loi 3: mat mot cau tra loi ngan

Khoi VD/VDC chi don trong dam bai DA CO trong phan bo. De giua ky 1 co
bon bai mang yeu cau muc VD (B1, B2, B4, B6) nhung phan bo ban dau chi
cham toi B1, nen ca bon cau tra loi ngan don het ve B1; quy uoc moi bai
toi da MOT cau VDC nen cau thu tu roi mat. Do duoc: 3/20 de chi ra 20 cau
thay vi 21.

Da doi sang chia lai tren MOI bai thuoc pham vi de co yeu cau muc VD.

### Loi 4: cau L10_C1_B1_TH014_MC_A co HAI DAP AN DUNG

Loi TOAN, nang. Ca hai bien the _01 va _02 deu lay
b = random.choice([u for u in range(1, a+1) if a % u == 0])
nen b CO THE BANG a.

Ham _01 (hoi "khang dinh nao DUNG"): khi b = a, dap so thanh
"a|n => a|n" va phuong an nhieu thu nhat cung the - trung nhau.
Rieng phuong an nhieu "ton tai n, a|n => b khong chia het n" la menh de
DUNG chu khong sai: chi can lay mot n khong chia het cho a thi gia thiet
sai nen phep keo theo dung, va menh de ton tai duoc thoa man. Nhu vay cau
hoi co HAI dap an dung. Da thay bang menh de sai that.

Ham _02 (hoi "khang dinh nao SAI"): khi b = a, dap so "a|n => a|n" la
menh de DUNG - dap an bi sai han. Ham nay chinh co Lan da ghi chu
"kiem tra lai noi dung cau hoi, cac phuong an".

Nay b la uoc THUC SU cua a, 1 < b < a, o ca hai ham.

## Ket qua sau khi sua

De giua ky 1, chay 20 lan bat de:

    truoc: 3/20 de thieu cau, 20 cau roi het vao chuong 1 va 2
    sau  : 20/20 de du ma tran (21 cau), 420/420 cau sinh duoc, 0 loi

Phan bo chuong sau khi sua (20 de, 420 cau):

    chuong 1   251 cau   (ti le so tiet 36%)
    chuong 2    85 cau   (23%)
    chuong 3    73 cau   (23%)
    chuong 4    11 cau   (18%)

Chuong 1 van cao hon ti le so tiet va chuong 4 van thap - day la chuyen
cua CURRICULUM chu khong phai cua bo chia: trong pham vi giua ky, bai 7
va bai 8 cua chuong 4 KHONG co yeu cau nao muc Van dung, ma ma tran doi
toi 9 cau muc VD; con bon yeu cau muc VD trong ca pham vi thi chuong 1
giu ba.

## Da kiem chung the nao

1. De giua ky 1: 20/20 de du ma tran, 420/420 cau sinh duoc, khong loi.
2. Kiem lai HE SO 1 sau khi sua bo chia - khong lam hong cai da chay:
   chuong 1, 2, 3, 4, 8, 9 deu 8/8 de du ma tran, 96/96 cau sinh duoc.
3. Ham L10_C1_B1_TH014_MC_A chay 1500 lan qua call_generator: 1500/1500
   ra cau, moi cau dung MOT dap an dung.
4. Them tests/test_du_cau_giua_ky.py - khoa lai ba dieu: de du cau, KHONG
   chuong nao trong pham vi bi bo trang, va cau khong xep duoc thi phai
   bao chu khong duoc bien mat. 511 bai test qua, 8 bo qua (truoc: 500).

## Chua kiem duoc

De cuoi ky 1 con thieu ham chuong 5 nen chua chay tron ven (172/210 cau).
Se xong khi lam chuong 5.

## Nguoi thuc hien

Mai Ha Lan (cung Claude)

# Version 3.06 - 2026-09-28

## Chuong 5 (Thong ke): tu 0 len 48/48 dang co ham

Tep LopXChuong5.py cua co Lan o FORM CU va chi co 3 ham. Da viet lai
toan bo cho dung khuon math_type - math_type.py GIU NGUYEN.

    Bai 12  so gan dung va sai so        16 dang
    Bai 13  do xu the trung tam          15 dang
    Bai 14  do do phan tan               15 dang
    Dung/Sai                              2 dang

Trong do 7 dang la bo sung vi bo chon cau can ma Mapping chua khai (de
he so 1 chuong 5 luc dau mat 26/96 cau): VD070_SA_A, VD077_SA_A,
VD078_SA_A, VD078_TL_A, VD083_SA_A, VD083_TL_A, VD084_SA_A.

## Ba loi trong tep cua co - da tranh khi viet lai

1. K10_5_13_2_1_TH co input() nen TREO khi sinh de tu dong; de hoi TRUNG
   VI nhung lai tinh numpy.mean (so trung binh); loi giai dung bien
   "median" chua he duoc gan -> NameError.
2. K10_5_14_1_1_TH ghi can nang tre so sinh "don vi kg" nhung so lieu la
   2700-4200, tuc la GAM.
3. K10_5_14_1_3_VD goi numpy.delete(X, i) voi i la GIA TRI chu khong
   phai chi so.

## Quy uoc SGK KNTT lop 10 da bam dung

    Tu phan vi   sap xep tang dan; Q2 la trung vi; Q1 la trung vi nua
                 ben trai, Q3 la trung vi nua ben phai; neu n LE thi Q2
                 KHONG thuoc nua nao.
    Phuong sai   s^2 = (1/n) * tong (x_i - x_tb)^2 - chia cho n, KHONG
                 phai n-1.
    Ngoai le     x < Q1 - 1,5*delta_Q hoac x > Q3 + 1,5*delta_Q.

## Cho phai can than: dap so cau TRA LOI NGAN

Cau tra loi ngan cham bang SO KHOP CHUOI nen dap so phai la so thap phan
HUU HAN. Thong ke rat de ra so le vo han:

  - so trung binh, trung vi, tu phan vi: loc bang _dep(x, 2);
  - DO LECH CHUAN la CAN cua phuong sai nen hau het bo so cho ket qua vo
    ti - phai loc rieng bang _mau_phuong_sai_dep(can_do_lech=True).

## Mot loi da vap phai

VD084 (tim gia tri ngoai le) tinh nguong tren MAU GOC roi moi them gia
tri la vao. Nhung them mot so lieu lam ba tu phan vi DICH DI, nen so vua
them co the khong con vuot nguong - danh sach ngoai le rong, lay
ngoai[0] thi IndexError. Hong 4/10 lan. Nay kiem tra lai SAU KHI them,
chi nhan mau co dung MOT ngoai le.

## Da kiem chung the nao

1. 48/48 dang chay tron 20/20 lan, khong loi; trac nghiem dung MOT dap
   an dung, tra loi ngan dung MOT shortans, Dung/Sai dung BON y.
2. Doi chieu voi thu vien chuan va vi du SGK:
   - so trung binh khop statistics.fmean
   - phuong sai khop statistics.pvariance (chia n)
   - trung vi khop statistics.median
   - tu phan vi khop bon vi du SGK, ca truong hop n chan va n le
   - 200 mau sinh ra deu co do lech chuan huu han
3. Bieu do hop ve bang TikZ, da dich thu qua duong ra hinh cho web va
   XEM TAN MAT anh - nam moc va diem ngoai le hien dung cho.
4. De he so 1 chuong 5: 8/8 de du ma tran, 96/96 cau sinh duoc.
5. 543 bai test qua, 8 bo qua (truoc: 511).

## DE CUOI KY 1 nay chay tron ven

Truoc dot nay cuoi ky 1 chi sinh duoc 172/210 cau vi thieu ham chuong 5.

    giua ky 1   10/10 de du ma tran   210/210 cau sinh duoc
    cuoi ky 1   10/10 de du ma tran   210/210 cau sinh duoc

Phan bo chuong cua de cuoi ky 1: C1 87, C2 21, C3 14, C4 41, C5 47 -
deu co mat.

## Hien trang toan lop 10

    C1   37/37   xong        C6    0/31
    C2   15/15   xong        C7    0/37  (chua co nguon)
    C3   53/53   xong        C8   30/30   xong
    C4   46/46   xong        C9   27/27   xong
    C5   48/48   xong

## Nguoi thuc hien

Mai Ha Lan (cung Claude)
