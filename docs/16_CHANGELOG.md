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