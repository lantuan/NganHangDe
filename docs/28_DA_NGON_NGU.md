# 28. ĐA NGÔN NGỮ VIỆT / ANH

Cô Lan 03/10/2026: web và đề có bản tiếng Anh tương ứng; thuật ngữ Toán của MỸ (học sinh thi SAT).
Làm theo thứ tự: (1) web có nút Tiếng Việt | English ở góc phải trên; (2) ngân hàng đề dịch dần từ Chương 1 trở đi.

## Nguyên tắc
- Không sửa từng template / hàm. Mọi chữ Việt đi qua một BƯỚC DỊCH theo từ điển; chưa có trong từ điển thì giữ nguyên tiếng Việt (web vẫn chạy, đầy dần).
- Ngôn ngữ lưu trong cookie `lang` (vi | en). Nút chuyển chèn tự động vào mọi trang HTML (middleware ngon_ngu_viet_anh trong app/main.py).
- Từ điển Việt -> Anh trong `data/i18n/`: `en_ui.json` (giao diện), `en_curriculum.json` (tên chương, bài, yêu cầu cần đạt), sau này `en_bank_*.json` (chữ trong hàm sinh câu).
- Code: `app/services/i18n_service.py`. Chữ được cắt thành đoạn giống `scripts/i18n_trich_chuoi.py` (ngắt ở thẻ HTML, {}, nháy, xuống dòng).
- Test `tests/test_i18n.py` bắt buộc: mọi đoạn chữ Việt trong template phải có trong `en_ui.json`. Thêm chữ mới vào template thì chạy `python3 scripts/i18n_trich_chuoi.py --chua-dich` và dịch.
- Bản dịch không chứa nháy ' ", dấu ` < > { } \ $ (nằm trong chuỗi JS / thuộc tính HTML); dùng nháy cong ’.

## Thuật ngữ (Toán Mỹ)
Học sinh = student; giáo viên = teacher; lớp 10 = Grade 10; chương = chapter; mã đề = exam version (form);
NB / TH / VD / VDC = Recall / Comprehension / Application / Advanced (giữ ký hiệu NB, TH, VD, VDC kèm chú thích);
vectơ = vector; tập hợp = set; mệnh đề = statement; hình bình hành = parallelogram; hình chữ nhật = rectangle;
hình thoi = rhombus; tam giác đều = equilateral triangle; trung điểm = midpoint; cùng phương / cùng hướng / ngược hướng =
parallel (collinear) / same direction / opposite direction.

## Ngân hàng câu hỏi tiếng Anh (đã xong Lớp 10 Chương 1 và Chương 2, 03/10/2026)
- Thư mục riêng `data/python_bank_en/toan10/L10_C1.py`, `L10_C2.py`... (cùng tên hàm, tham số như bản Việt). KHÔNG sửa tay: sửa bản Việt (data/python_bank) rồi chạy lại
  `python3 scripts/dich_ngan_hang.py dich data/python_bank/toan10/L10_C1.py`.
- Cách dịch: tách chuỗi hiển thị (str, f-string) trong cây cú pháp thành đơn vị; từ điển `data/i18n/bank/en_<tệp>.json` {nguồn Việt: nguồn Anh | "__GIU__"} (giữ nguyên toán, %s %d, {biểu thức}, thứ tự placeholder); `__GIU__` cho chuỗi mà mã dùng làm khoá logic.
- Chỗ MÃ phụ thuộc chữ Việt không dấu (so sánh "sai", split("cho } "), "tham gia", dấu thập phân...) sửa bằng `data/i18n/bank/patch_<tệp>.json` và `patch_<tệp>_2.json`, `_3`...: [{"tim", "thay", "so_lan" | "tat_ca"}], áp dụng lần lượt lên bản Anh sau khi thay chuỗi.
- Quy tắc bắt buộc khi dịch: hai chỗ cùng một câu tiếng Việt mà mã gộp / bỏ trùng (so sánh, set) PHẢI ra cùng một câu tiếng Anh; từ khoá mã dùng ("true", "false", "recorded that"...) không đổi tuỳ tiện.
- Kiểm: `python3 scripts/kiem_tuong_duong.py L10_C1 8` so từng hàm bản Anh với bản Việt cùng hạt giống (cấu trúc, vị trí \True, mọi công thức). Phải 0 hàm lệch (ngoại lệ ghi trong tests/test_ngan_hang_anh.py). `python3 -m pytest tests/test_ngan_hang_anh.py`.
- Quy trình thêm chương tiếp theo: (1) trích đơn vị `python3 scripts/dich_ngan_hang.py trich <tệp>`; (2) dịch hàng loạt, tách nhóm ~200 đơn vị cho các nhóm dịch song song, mỗi nhóm đọc mã quanh dòng đó; (3) chạy dich, kiem_tuong_duong, sửa patch; (4) rà mẫu đầu ra (grammar, "there are 1 ...", từ Việt không dấu sót như Sai, Cho, Do); (5) test.

## Đề tiếng Anh ghép cùng đề tiếng Việt
- `generate_exam_pdf_auto(..., kem_tieng_anh=True)`: đề Việt rồi đề Anh CÙNG seed, cùng danh sách câu (cùng câu, số liệu, thứ tự đáp án). Chương chưa dịch: dòng [MISSING IN PYTHON].
- Thư mục tiếng Anh riêng: `data/temp_en/` (.tex, đáp án json), `data/exports_en/` (PDF). Khung `ex_test_en.sty` và `latex_template_en.tex` do `scripts/tao_ex_test_en.py` sinh từ bản Việt (bảng thay nhãn trong script; ex_test.sty đổi làm mục nào không khớp thì script báo).
- Giáo viên: form /gv/ra-de có ô "Tạo kèm đề tiếng Anh tương ứng"; /gv/de-da-tao có liên kết Tiếng Anh. API: /api/exam/tai-de-en, tai-loigiai-en, tai-tex-en (chỉ giáo viên).

## Trang làm bài trực tuyến của học sinh (03/10/2026)
- Nền là tiếng Việt: đề luôn được CHỌN và SINH trên bản Việt (cùng ID hàm, cùng hạt giống). `/api/exam/generate-pdf-auto` và `/api/exam/lam-de-khac` gọi `generate_exam_pdf_auto(..., dapan_tieng_anh=True)`: sinh thêm bản Anh của đúng đề đó (cùng ID + seed), CHỈ lấy tệp đáp án (không biên dịch PDF), đặt ở `data/temp_en/<cùng tên tệp đáp án Việt>` (không ghi vào cơ sở dữ liệu nên không dính ràng buộc `file_de_loai_file_check`).
- `GET /api/exam/quiz/{de_id}` và `POST /api/exam/grade`: cookie `lang=en` và có tệp đáp án Anh thì dùng bản Anh (đề, lời giải, tên phần "PART I..."), ngược lại dùng bản Việt (đề cũ, chương chưa dịch).
- PDF tải về: `generate_exam_pdf_auto(dapan_tieng_anh=True)` còn ghi `.tex` tiếng Anh (chưa biên dịch) vào `data/temp_en/` CÙNG TÊN với `.tex` tiếng Việt (`duong_tex_en`). `GET /api/exam/tai-de/{id}`, `/tai-loigiai/{id}`, `/export-loigiai` khi cookie `lang=en` và có `.tex` tiếng Anh thì biên dịch (lần đầu bấm tải; cache ở `data/exports_en/`) và trả PDF tiếng Anh (`_pdf_en_tu_tex`: đổi `[dethi]`/`[loigiai]` của `ex_test_en`); không có thì trả bản Việt.
- Word: `GET /api/exam/tai-word/{id}?ban=de|loigiai` (chỉ giáo viên) khi `lang=en` và có `.tex` tiếng Anh thì xuất Word TIẾNG ANH: `word_service.xuat_word(..., lang="en")`, bảng nhãn `_CHU` ("PART", "Exam code", "SCHOOL YEAR", Question/Problem, True/False, "Correct answer:", "Answer:", "Solution."). Thêm nhãn mới vào khung tiếng Anh (`tao_ex_test_en.py`) thì phải thêm vào `_CHU["en"]` tương ứng.
- Đề tạo TRƯỚC khi có tính năng này không có bản Anh -> vẫn tiếng Việt; cần tạo đề mới / bấm "Làm đề khác".
- Ô "Tạo kèm đề tiếng Anh tương ứng" (PDF cho giáo viên) giữ nguyên, giáo viên tự chọn.
- Lưu ý: bản Anh dùng dấu thập phân "." nên đáp án SA của đề Anh là "3.5" (đề Việt "3,5").

## Ô tick "Kèm bản tiếng Anh" lúc tạo đề (03/10/2026, thay cho cơ chế tick lúc tải)
- Nguyên tắc (cô Lan chốt): bản Anh chỉ sinh khi người dùng tick; không tick thì đề chỉ có bản Việt (đỡ tốn công sinh, n8n đỡ thêm bước). Ô tick luôn hiện ở nơi tạo đề, dù trang đang ở tiếng Việt hay tiếng Anh: hàng trên nút "Tạo đề mới" ở Chat AI, trong form "Tạo đề nhanh", trong thẻ "Đồng ý, tạo đề", và cạnh nút "Làm đề khác" ở trang làm bài (mặc định giữ như đề vừa làm). Giáo viên ở mục Ra đề có ô riêng (đã có từ trước).
- Chat AI: một trạng thái chung `kemAnh()` (localStorage `chv_kem_anh`), các ô `.chk-kem-anh` đồng bộ nhau. Form nhanh và thẻ xác nhận gửi `kem_tieng_anh` thẳng vào `/api/exam/generate-pdf-auto`.
- Chat tự do đi qua n8n: n8n tự gọi `/generate-pdf-auto` nên không nhận được ô tick. `/chat` nhận field `kem_tieng_anh` và ghi vào `app/services/tuy_chon_de_service.py` (tệp `data/temp/kem_tieng_anh_hoi_thoai.json`, theo conversation_id, hết hạn 6 giờ); `/generate-pdf-auto` đọc lại khi lời gọi không nói rõ (`kem_tieng_anh=None`). n8n không phải sửa gì.
- Tải về: đề của HỌC SINH có bản Anh thì `/tai-de`, `/tai-loigiai` mặc định trả `.zip` có `*_TiengViet.pdf` và `*_English.pdf` (dù trang ở ngôn ngữ nào); không có bản Anh thì PDF Việt thường. Link tải không gắn `download="…pdf"` (để tên `.zip` đúng); chỉ link blob mới gắn. `?ngon_ngu=vi|en|ca-hai` ép một thứ tiếng.
- Làm bài trực tiếp luôn theo ngôn ngữ trang; đề không có bản Anh thì hiện tiếng Việt kèm chú thích vàng (`thong_bao_ban_anh`), `/quiz` trả thêm `co_ban_tieng_anh`.
- Test: test_tick_kem_tieng_anh_luc_tao_de_quyet_dinh_co_ban_anh_hay_khong, test_tai_de_hoc_sinh_da_tick_anh_ra_zip_mac_dinh.

## Bản Anh KHÔNG ghi vào bảng file_de (lỗi 03/10/2026)
Cột `file_de.loai_file` có CHECK constraint chỉ nhận các loại cũ (de, loigiai, tex, dapan_json...). Các dòng `de_en`, `loigiai_en`, `tex_en` từng được ghi cho đề giáo viên tick tiếng Anh bị từ chối âm thầm, nên ba liên kết tiếng Anh ở bảng "Đề đã tạo" đều báo "Đề này không có bản tiếng Anh". Nay bản Anh nằm cạnh bản Việt, CÙNG TÊN: `.tex` ở `data/temp_en/`, PDF ở `data/exports_en/`. Bản Anh KHÔNG biên dịch PDF lúc tạo đề (mỗi PDF 30-60 giây; Việt + Anh = 4 lần biên dịch làm giáo viên chờ rất lâu, có lúc nginx cắt kết nối): `_sinh_kem_tieng_anh` chỉ ghi `.tex` + đáp án Anh (`chi_dap_an=True`). Giáo viên tick thì `teacher.py` mở một luồng nền gọi `bien_dich_nen_tieng_anh` biên dịch PDF đề rồi PDF lời giải bản Anh; bấm tải trước khi xong thì `bien_dich_pdf_tieng_anh` chờ khoá của đúng PDF đó rồi trả (không biên dịch đè hai lần). PDF có sẵn thì trả ngay, kể cả khi `.tex` đã bị dọn. Quy tắc tên: `.tex` Anh tên `exam_x_loigiai.tex` (giáo viên) -> PDF đề `exam_x.pdf`, PDF lời giải `exam_x_loigiai.pdf`; BỎ đuôi `_loigiai` trước khi ghép tên, nếu không PDF lời giải thực ra là PDF đề (lỗi 03/10/2026). Bảng giáo viên với đề tick tiếng Anh có 10 liên kết: 5 bản Việt (PDF đề, PDF lời giải, Word đề, Word lời giải, .tex) + 5 bản Anh (cùng loại; Word Anh qua `tai-word?ngon_ngu=en`). Tuyệt đối không thêm loại tệp mới vào `file_de` nếu chưa sửa CHECK constraint trên Supabase. Test: test_giao_vien_tick_tieng_anh_cac_lien_ket_tieng_anh_tai_duoc_dung_ban.

## Khi nào một đề có bản tiếng Anh (quan trọng với CHV_Fun)
Bản Anh của đề (tệp đáp án + .tex tiếng Anh cạnh tệp Việt, `data/temp_en/`, cùng tên) CHỈ có khi người dùng tick "Kèm bản tiếng Anh" lúc tạo đề (học sinh: Chat AI, form nhanh, thẻ xác nhận, "Làm đề khác"; giáo viên: Ra đề, ô "Tạo kèm đề tiếng Anh tương ứng") VÀ chương đó đã có ngân hàng tiếng Anh (hiện Lớp 10 Chương 1, 2). Đề cũ trước 03/10/2026 không có. Trang làm bài ở English mà đề không có bản Anh vẫn hiện tiếng Việt kèm chú thích vàng. Muốn có bản Anh phải TẠO ĐỀ MỚI có tick. Quy tắc này đã chép vào `data/prompts/CHV_Fun.md` (rule 5, task `help`): dán sang node CHV_Fun trên n8n thì CHV_Fun mới trả lời đúng khi người dùng hỏi.

## Tải kèm cả hai thứ tiếng cho giáo viên (03/10/2026)
- Ô tick "Tải kèm bản tiếng Anh" trên Trang chính và "Đề đã tạo" (`_base_gv.html` có script chung; liên kết có `data-ca-hai` chỉ khi đề có bản Anh). Tick thì PDF đề, PDF lời giải, Word đề/lời giải và `.tex` thêm `ngon_ngu=ca-hai` và trả `.zip` có `*_TiengViet` và `*_English`.
- `GET /api/exam/tai-word/{id}?ban=de|loigiai&ngon_ngu=ca-hai`, `/tai-tex/{id}?ngon_ngu=ca-hai`. Đề không có bản Anh thì Word vẫn ra zip chỉ có bản Việt, `.tex` ra tệp Việt như cũ.
- Test: test_giao_vien_tick_ca_hai_thu_tieng_word_va_tex_ra_zip.

## Lỗi hiển thị công thức trong câu trả lời của AI (03/10/2026)
Câu trả lời của AI là markdown nên qua `marked`; `marked` coi `\{` `\}` là ký tự thoát và bỏ dấu `\`, làm `\left\{ ... \right\}` thành `\left{ ... \right}` và MathJax báo "Missing or unrecognized delimiter for \left". Sửa: `markdownGiuCongThuc()` (chat.html, lam_bai.html) cắt công thức `$..$ $$..$$ \(..\) \[..\]` thành mốc trước khi qua marked rồi trả nguyên văn. Mọi chỗ hiển thị câu trả lời AI phải gọi `renderMarkdownAI`, không gọi `marked.parse` trực tiếp.

## Gia sư AI bằng tiếng Anh
Xem docs/23 mục 8b: cùng cách chọn tệp đáp án bản Anh (`data/temp_en/`), lệnh `LENH_HE_THONG_EN`, thông báo lỗi tiếng Anh.

## Bản đồ tệp
| Việc | Tệp |
|---|---|
| Nút Việt/Anh, dịch giao diện | `app/services/i18n_service.py` (nút ở khu giáo viên đặt dưới thanh menu: `data-chv-lang="duoi"` trong `_base_gv.html`) |
| Dịch ngân hàng (trích, dịch, kiểm) | `scripts/dich_ngan_hang.py`, từ điển `data/i18n/bank/en_<chương>.json`, vá `patch_<chương>*.json` |
| Kiểm tương đương Việt/Anh | `scripts/kiem_tuong_duong.py <chương> [số_seed]` |
| Khung LaTeX tiếng Anh | `scripts/tao_ex_test_en.py` -> `data/config/ex_test_en.sty`, `latex_template_en.tex` |
| Sinh đề Anh cùng seed | `app/services/exam_assembler_service.py` (`_sinh_kem_tieng_anh`, `duong_dapan_en`), `generator_service.py` (`lang`, `dat_hat_giong`, `chup/khoi_phuc_trang_thai_xoay`) |
| Trang làm bài, chấm bài | `app/routers/exam.py` (`/quiz`, `/grade` chọn bản Anh theo cookie) |
| Test | `tests/test_ngan_hang_anh.py`, `tests/test_i18n.py` |

## Những chỗ dễ sai về sau
| Chỗ | Vì sao dễ sai |
|---|---|
| Sửa tay `data/python_bank_en/...` | Lần sinh lại sẽ mất; test "bản Anh sinh ra từ bản Việt" đỏ. Sửa bản Việt hoặc từ điển/patch rồi chạy lại `dich`. |
| Sửa hàm bản Việt mà không dịch lại | Bản Anh lệch bản Việt (số liệu, đáp án). Chạy `dich` + `kiem_tuong_duong` + pytest. |
| Hai câu Việt giống nhau mà bản Anh khác nhau | Mã gộp/bỏ trùng bằng so sánh chuỗi -> số câu/ phương án lệch. Dịch CÙNG một câu Anh. |
| Chữ Việt không dấu làm khoá logic ("sai", "cho } ", "tham gia") | Không nằm trong từ điển nên không được dịch; vá bằng `patch_*`. |
| Dịch chương mới mà quên đưa vào test | Test duyệt mọi `python_bank_en/toan10/L10_C*.py` nên tự có; chỉ cần có tệp. |
| Đề cũ không có bản Anh | Trang English rơi về tiếng Việt, không lỗi. Muốn có bản Anh phải tạo đề mới. |
| Đáp án SA bản Anh dùng dấu chấm thập phân | "3.5" thay "3,5"; chấm bài theo đúng bản đang hiển thị. |

## Còn lại (chưa làm)
- Thông báo từ AI / n8n (Chat) vẫn tiếng Việt: cần truyền `lang` cho n8n.
- Tên bài, yêu cầu cần đạt trong Curriculum (mới có tên chương).
- Word tiếng Anh (word_service còn nhãn Việt).
- Dịch ngân hàng các chương khác (Lớp 10 chương 3..9, Lớp 11, 12).
