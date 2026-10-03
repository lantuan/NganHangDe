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

## Còn lại (chưa làm)
- Thông báo từ AI / n8n (Chat) vẫn tiếng Việt: cần truyền `lang` cho n8n.
- Tên bài, yêu cầu cần đạt trong Curriculum (mới có tên chương).
- Đề PDF / Word tiếng Anh (khung đề: "PHẦN I", "Lời giải", "Đáp án"), thư mục `de_tieng_Anh/` song song.
- Ngân hàng câu hỏi: dịch chữ trong hàm sinh câu (thay literal khi chạy, cùng hạt giống thì ra cùng số liệu), từ Chương 1.
