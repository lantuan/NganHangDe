# LATEX ENGINE

Version: 1.0

Trạng thái

🟡 Đang triển khai

---

# Mục tiêu

Chuẩn hóa toàn bộ quá trình sinh đề LaTeX.

LaTeX chỉ nhận dữ liệu đã được sinh hoàn chỉnh.

Không sinh câu hỏi.

Không sửa nội dung câu hỏi.

---

# Vai trò

Latex Engine chịu trách nhiệm

- Ghép câu hỏi
- Ghép đáp án
- Ghép lời giải
- Ghép hình
- Ghép bảng
- Xuất PDF

---

# Kiến trúc

Question Objects

↓

Exam JSON

↓

LaTeX Template

↓

.tex

↓

pdflatex

↓

PDF

---

# Input

Exam JSON

---

# Output

- tex
- pdf
- answer pdf
- solution pdf

---

# Template

Toàn bộ template lưu tại

```
templates/
```

---

Ví dụ

```
exam.tex

answer.tex

solution.tex
```

---

# Không được

Không random.

Không gọi Python.

Không gọi AI.

Không đọc PPCT.

Không đọc Curriculum.

---

# Được phép

- Chèn hình.
- Chèn bảng.
- Chèn TikZ.
- Chèn biểu đồ.
- Chèn watermark.
- Chèn QR Code.

---

# Hình vẽ

Hình sinh từ Python.

Latex chỉ include.

---

# Công thức

Toàn bộ công thức do Python sinh.

---

# Đáp án

Có thể xuất

- cuối đề
- file riêng

---

# Lời giải

Có thể xuất

- cuối đề
- file riêng

---

# Định dạng

A4

Portrait

Landscape (tương lai)

---

# Font

Mặc định

Times New Roman

(TODO)

---

# Header

TODO

---

# Footer

TODO

---

# Số trang

TODO

---

# Mã đề

TODO

---

# QR Code

TODO

---

# Watermark

TODO

---

# Logging

TODO

---

# Error Handling

Nếu pdflatex lỗi

↓

Trả lỗi cho Code Node

↓

Không trả PDF rỗng.

---

# Quan hệ

Python

↓

Question Objects

↓

Exam JSON

↓

Latex Engine

↓

PDF

---

# TODO

Thiết kế Exam JSON.

Thiết kế Template.

Thiết kế Header.

Thiết kế Footer.

Thiết kế Watermark.

Thiết kế QR Code.

Thiết kế nhiều mẫu đề.