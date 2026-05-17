# AGENT INSTRUCTIONS

## Quy trình bắt buộc khi sinh đề
Trước khi sinh bất kỳ nội dung nào, AI phải đọc theo thứ tự:
1. Đọc README.md
2. Đọc LATEX_RULES.md
3. Đọc TEMPLATE_RULES.md
4. Đọc TEMPLATE/de_mau.tex
5. Sau đó mới sinh nội dung

---

## Thứ tự ưu tiên
1. TEMPLATE/de_mau.tex
2. LATEX_RULES.md
3. TEMPLATE_RULES.md
4. Prompt người dùng

---

## Không được phép
- Không đổi môi trường LaTeX
- Không bỏ lời giải
- Không đổi encoding (luôn dùng UTF-8)
- Không tự ý sửa cấu trúc file
- Không sửa nội dung trong STATIC_EXAMS/
- Không tự bịa câu hỏi sai kiến thức

---

## Quy tắc sinh đề

### Đề 1 — Lấy từ STATIC_EXAMS
- Đọc file .tex trong STATIC_EXAMS/{Khoi}/
- Chọn đúng khối lớp theo yêu cầu
- KHÔNG sửa nội dung gốc
- Trả nguyên file hoặc trích đúng phần được yêu cầu

### Đề 2 — Tự sinh (DYNAMIC)
- Dựa trên TEMPLATE/de_mau.tex
- Tuân thủ LATEX_RULES.md
- Random dữ kiện số, giữ nguyên cấu trúc
- Lưu output vào DYNAMIC_EXAMS/{Khoi}/

### Mỗi đề phải có
- Mức độ rõ ràng: NB / TH / VD / VDC
- Lời giải đầy đủ
- Đáp án đúng đánh dấu \True
- Đúng môi trường LaTeX
- Đúng format theo TEMPLATE

---

## Cấu trúc câu hỏi chuẩn
Mỗi câu hỏi gồm:
- Đề bài
- 4 lựa chọn A, B, C, D
- Đánh dấu \True vào đáp án đúng
- Lời giải chi tiết

---

## Đặt tên file output
Quy tắc đặt tên file sinh ra:
DYNAMIC_EXAMS/{Khoi}/de_{loai}_{khoi}_{ddmmyy}_{variant}.tex

Ví dụ:
DYNAMIC_EXAMS/Khoi10/de_15p_Khoi10_170526_v1.tex
DYNAMIC_EXAMS/Khoi12/de_HK1_Khoi12_020626_v2.tex

---

## Xuất nội dung
Thứ tự ưu tiên:
1. LaTeX (.tex)
2. PDF (.pdf)
3. DOCX (.docx)

---

## Báo lỗi
Nếu không tìm thấy file TEMPLATE hoặc LATEX_RULES.md:
- Dừng lại
- Báo lỗi rõ ràng
- Không tự ý sinh đề theo cách khác
