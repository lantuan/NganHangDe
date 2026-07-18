# LATEX ENGINE

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

LaTeX Engine chịu trách nhiệm tạo file .tex và biên dịch PDF từ Exam Object.

Không sinh câu hỏi.

Không chọn Generator.

Không xử lý AI.

---

# Input

Exam Object

---

# Output

- .tex
- .pdf

---

# Luồng xử lý

Exam Object

↓

Generate LaTeX

↓

Compile PDF

↓

PDF

---

# Templates

Toàn bộ Template lưu tại

```
templates/
```

Ví dụ

```
exam.tex

answer.tex

header.tex

footer.tex
```

---

# Generate LaTeX

Input

Exam Object

↓

Sinh file

```
exam.tex
```

---

# Compile

Sử dụng

```
pdflatex
```

↓

Sinh

```
exam.pdf
```

---

# Output

Lưu tại

```
output/pdf/
```

và

```
output/latex/
```

---

# Không được

- Sinh câu hỏi.
- Chọn Generator.
- Gọi AI.
- Đọc PPCT.
- Đọc Curriculum.
- Đọc Mapping.

---

# Quy tắc

- Chỉ nhận Exam Object.
- Một Exam Object sinh một file .tex.
- Một file .tex sinh một file PDF.
- Template không chứa dữ liệu.
- Dữ liệu chỉ lấy từ Exam Object.
- Không chỉnh sửa Question Object trong quá trình sinh PDF.