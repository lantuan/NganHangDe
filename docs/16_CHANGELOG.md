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
