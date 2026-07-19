# PYTHON GENERATOR

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Python Generator chịu trách nhiệm sinh Question Object. Không
sinh PDF, không sinh Web Test, không sinh JSON đề thi.

---

# Cấu trúc

python_bank/
├── toan10/
│     L10_C1.py
│     L10_C2.py
├── toan11/
└── toan12/

---

# Quy tắc

Mỗi chương = một file Python.

---

# Cấu trúc trong file

Một file gồm nhiều Generator Function.

Ví dụ (L10_C1.py):
L10_C1_B1_TH001_MC_A()
L10_C1_B1_TH002_MC_A()
L10_C1_B2_VD020_TL_A()

---

# Generator Function

Tên hàm phải trùng Generator ID.

Generator ID: L10_C1_B2_VD020_TL_A
Python: def L10_C1_B2_VD020_TL_A():

---

# Input

Generator Function không nhận tham số. Random xử lý bên trong hàm.

---

# Output

Mỗi Generator Function trả về đúng một Question Object.

---

# Question Object

- generator_id
- content
- answer
- solution
- latex
- metadata

---

# Random

Một Generator Function có thể sinh nhiều câu hỏi khác nhau.
Generator ID không đổi. Question Object thay đổi.

---

# Ghi chú quan trọng — dùng cho CHV_Grader

Trường answer và solution của mỗi Question Object là căn cứ
DUY NHẤT để CHV_Grader chấm câu tự luận. Generator Function phải
đảm bảo answer/solution đầy đủ, chính xác, vì AI chấm bài sẽ
không tự nghĩ ra đáp án nào khác ngoài dữ liệu này.

---

# Không được

- Gọi AI.
- Đọc PPCT, Curriculum, Mapping.
- Sinh PDF, sinh Web Test.

---

# Quy tắc

- Một Generator ID chỉ có một Generator Function.
- Một Generator Function chỉ sinh một Question Object.
- Mỗi chương chỉ có một file Python.
- Không tạo nhiều file Python cho cùng một chương.
- Tên hàm phải trùng Generator ID.
- answer/solution bắt buộc phải có, đầy đủ, chính xác.