# PYTHON GENERATOR

Version: 1.0

Trạng thái

🟡 Đang triển khai

---

# Mục tiêu

Python là thành phần duy nhất được phép sinh câu hỏi.

AI không sinh câu hỏi.

---

# Vai trò

Python chịu trách nhiệm

- Sinh câu hỏi
- Sinh đáp án
- Sinh lời giải
- Sinh LaTeX
- Sinh dữ liệu Web Test

---

# Kiến trúc

Code Node

↓

Import Python

↓

Gọi Function

↓

Question Object

---

# Cấu trúc thư mục

data/python_bank

```
toan10/
toan11/
toan12/
```

---

# Quy tắc

Một chương

=

Một file Python.

Ví dụ

```
L10_C1.py

L10_C2.py

L10_C3.py
```

---

# Không chia theo bài.

Không chia theo mức độ.

Không chia theo dạng.

---

# Mỗi file chứa

Toàn bộ hàm sinh câu hỏi của chương.

Ví dụ

```
L10_C1.py
```

gồm

```
L10_C1_B1...

L10_C1_B2...

L10_C1_B3...
```

---

# Import

Ví dụ

```python
from L10_C1 import *
```

---

# Hàm

Tên hàm

=

ID

Ví dụ

```python
def L10_C1_B2_VD020_TL_A():
```

---

Không đổi tên.

---

# Input

Không nhận Prompt.

Không nhận Text.

Chỉ nhận

```python
seed
```

hoặc

```python
config
```

khi cần.

---

# Output

Luôn trả Question Object.

Không trả String.

---

Ví dụ

```python
return {

}
```

---

# Question Object

TODO

---

# Random

Mỗi hàm

Tự random.

Không để AI random.

---

# Seed

Sau này

Cho phép

```python
seed
```

để sinh lại đúng câu.

---

# Đáp án

Python sinh.

Không AI.

---

# Lời giải

Python sinh.

Không AI.

---

# LaTeX

Python sinh.

Không AI.

---

# Hình vẽ

Python sinh.

Không AI.

---

# Đúng/Sai

Một hàm

Có thể sinh

4 ý.

---

# Tự luận

Một hàm

Sinh

01 bài.

---

# Trắc nghiệm

Một hàm

Sinh

01 câu.

---

# Không được

Không gọi AI.

Không đọc JSON.

Không ghi Database.

Không gọi API.

---

# Được phép

Random

Sympy

Numpy

Latex

Matplotlib

TikZ

---

# Quan hệ với Mapping

Mapping

↓

ID

↓

Python Function

---

# Quan hệ với Curriculum

Curriculum

↓

Định nghĩa năng lực.

Python không đọc Curriculum.

---

# Quan hệ với PPCT

Không đọc PPCT.

---

# Quan hệ với Code Node

Code Node

↓

Import Python

↓

Gọi Function

---

# TODO

Question Object.

Question Validator.

Seed.

Cache.

Performance.

Parallel Generator.