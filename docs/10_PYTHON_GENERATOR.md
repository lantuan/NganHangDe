# PYTHON GENERATOR

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Python Generator chịu trách nhiệm sinh Question Object.

Không sinh PDF.

Không sinh Web Test.

Không sinh JSON.

---

# Cấu trúc

python_bank/

↓

toan10/

↓

L10_C1.py

L10_C2.py

...

---

# Quy tắc

Mỗi chương

↓

Một file Python.

Ví dụ

L10_C1.py

L10_C2.py

L10_C3.py

...

---

# Cấu trúc trong file

Một file gồm nhiều Generator Function.

Ví dụ

L10_C1.py

↓

L10_C1_B1_TH001_MC_A()

L10_C1_B1_TH002_MC_A()

L10_C1_B2_VD020_TL_A()

...

---

# Generator Function

Tên hàm phải trùng Generator ID.

Ví dụ

Generator ID

L10_C1_B2_VD020_TL_A

↓

Python

def L10_C1_B2_VD020_TL_A():

---

# Input

Generator Function không nhận tham số.

Random được xử lý bên trong hàm.

---

# Output

Mỗi Generator Function trả về đúng một Question Object.

---

# Question Object

Question Object gồm

- generator_id
- content
- answer
- solution
- latex
- metadata

---

# Random

Một Generator Function có thể sinh nhiều câu hỏi khác nhau.

Generator ID không đổi.

Question Object thay đổi.

---

# Không được

- Gọi AI.
- Đọc PPCT.
- Đọc Curriculum.
- Đọc Mapping.
- Sinh PDF.
- Sinh Web Test.

---

# Quy tắc

- Một Generator ID chỉ có một Generator Function.
- Một Generator Function chỉ sinh một Question Object.
- Mỗi chương chỉ có một file Python.
- Không tạo nhiều file Python cho cùng một chương.
- Tên hàm phải trùng Generator ID.