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

## Ngân hàng câu hỏi tiếng Anh (làm xong Chương 1 Lớp 10, 03/10/2026)
- Thư mục riêng `data/python_bank_en/toan10/L10_C1.py` (cùng tên hàm, tham số như bản Việt). KHÔNG sửa tay: sửa bản Việt (data/python_bank) rồi chạy lại
  `python3 scripts/dich_ngan_hang.py dich data/python_bank/toan10/L10_C1.py`.
- Cách dịch: tách chuỗi hiển thị (str, f-string) trong cây cú pháp thành đơn vị; từ điển `data/i18n/bank/en_<tệp>.json` {nguồn Việt: nguồn Anh | "__GIU__"} (giữ nguyên toán, %s %d, {biểu thức}, thứ tự placeholder); `__GIU__` cho chuỗi mà mã dùng làm khoá logic.
- Chỗ MÃ phụ thuộc chữ Việt không dấu (so sánh "sai", split("cho } "), "tham gia", dấu thập phân...) sửa bằng `data/i18n/bank/patch_<tệp>*.json`: [{"tim", "thay", "so_lan" | "tat_ca"}], áp dụng lần lượt lên bản Anh sau khi thay chuỗi.
- Quy tắc bắt buộc khi dịch: hai chỗ cùng một câu tiếng Việt mà mã gộp / bỏ trùng (so sánh, set) PHẢI ra cùng một câu tiếng Anh; từ khoá mã dùng ("true", "false", "recorded that"...) không đổi tuỳ tiện.
- Kiểm: `python3 scripts/kiem_tuong_duong.py L10_C1 8` so từng hàm bản Anh với bản Việt cùng hạt giống (cấu trúc, vị trí \True, mọi công thức). Phải 0 hàm lệch (ngoại lệ ghi trong tests/test_ngan_hang_anh.py). `python3 -m pytest tests/test_ngan_hang_anh.py`.
- Quy trình thêm chương tiếp theo: (1) trích đơn vị `python3 scripts/dich_ngan_hang.py trich <tệp>`; (2) dịch hàng loạt, tách nhóm ~200 đơn vị cho các nhóm dịch song song, mỗi nhóm đọc mã quanh dòng đó; (3) chạy dich, kiem_tuong_duong, sửa patch; (4) rà mẫu đầu ra (grammar, "there are 1 ...", từ Việt không dấu sót như Sai, Cho, Do); (5) test.

## Đề tiếng Anh ghép cùng đề tiếng Việt
- `generate_exam_pdf_auto(..., kem_tieng_anh=True)`: đề Việt rồi đề Anh CÙNG seed, cùng danh sách câu (cùng câu, số liệu, thứ tự đáp án). Chương chưa dịch: dòng [MISSING IN PYTHON].
- Thư mục tiếng Anh riêng: `data/temp_en/` (.tex, đáp án json), `data/exports_en/` (PDF). Khung `ex_test_en.sty` và `latex_template_en.tex` do `scripts/tao_ex_test_en.py` sinh từ bản Việt (bảng thay nhãn trong script; ex_test.sty đổi làm mục nào không khớp thì script báo).
- Giáo viên: form /gv/ra-de có ô "Tạo kèm đề tiếng Anh tương ứng"; /gv/de-da-tao có liên kết Tiếng Anh. API: /api/exam/tai-de-en, tai-loigiai-en, tai-tex-en (chỉ giáo viên).

## Còn lại (chưa làm)
- Thông báo từ AI / n8n (Chat) vẫn tiếng Việt: cần truyền `lang` cho n8n.
- Tên bài, yêu cầu cần đạt trong Curriculum (mới có tên chương).
- Word tiếng Anh (word_service còn nhãn Việt).
- Dịch ngân hàng các chương khác (Lớp 10 chương 2..9, Lớp 11, 12).
- Làm bài trực tuyến của học sinh bằng tiếng Anh (trang làm bài, chấm bài).
