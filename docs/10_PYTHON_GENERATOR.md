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


===== FILE: docs/10_PYTHON_GENERATOR.md (thêm vào cuối file) =====

---

# GHI CHÚ CẬP NHẬT — Version 2.1

Trạng thái

🟢 Chuẩn chính thức (thay thế một phần Version 2.0)

---

## Mô hình thực tế của Generator Function

Khác với mô tả ban đầu (Version 1.0: "không nhận tham số, chỉ trả về 1 Question Object"),
thực tế Generator Function được thiết kế để phục vụ nhu cầu **sinh nhiều mã đề cùng
cấu trúc, khác số liệu** — phù hợp với việc giáo viên cần ra nhiều đề tương đương.

Generator Function ĐƯỢC PHÉP nhận tham số điều khiển số lượng:
def L10_C1_B2_VD020_TL_A_01(socau, dong=1):
...

Trong đó

`socau`

↓

Số lượng bộ số liệu (mã đề) cần sinh trong 1 lần gọi.

`socot` / `dong`

↓

Tham số định dạng trình bày LaTeX (số cột đáp án, số dòng...),
lấy từ các hàm phụ trợ trong `math_type.py`.

---

## Output của Generator Function

Không trả về object có field tách rời (`content`, `answer`, `solution` riêng).

Thay vào đó trả về **1 chuỗi string LaTeX hoàn chỉnh**, đã bao gồm:

- Đề bài
- Lựa chọn / đáp án
- Lời giải

được đóng gói sẵn bằng các hàm phụ trợ dùng chung trong `math_type.py`:

- `TF_baitoan_du` — câu Đúng/Sai
- `TL_answer_const` — câu tự luận, đáp số là hằng số
- `TL_answer_text` — câu tự luận, đáp số dạng kí tự
- `MC_SA_answer_const` — câu trắc nghiệm/trả lời ngắn, đáp số hằng số
- `MC_SA_answer_text` — câu trắc nghiệm/trả lời ngắn, đáp số dạng kí tự

Nếu `socau > 1`, chuỗi trả về chứa nhiều khối `\begin{ex}...\end{ex}` nối tiếp
(nhiều mã đề/câu cùng cấu trúc).

---

## Metadata

Metadata (lop, chuong, bai, muc_do, loai, dang) KHÔNG cần nhúng trong chuỗi trả về.

Toàn bộ metadata được suy ra trực tiếp từ Generator ID theo `04_ID_STANDARD.md`
(ID đã mã hoá đủ khối/chương/bài/mức độ/loại câu). Tầng gọi hàm (CN_CallPythonGenerator)
chịu trách nhiệm gắn ID + metadata bên ngoài chuỗi LaTeX trả về, không sửa vào bên trong.

---

## math_type.py

File `math_type.py` là thư viện dùng chung, chứa các hàm định dạng LaTeX
(KHÔNG phải Generator Function). Mọi file trong `python_bank/` đều import
từ file này để đảm bảo định dạng đề/lời giải đồng nhất.

Vị trí
data/python_bank/math_type.py

Không được sửa logic bên trong các hàm này khi viết Generator Function riêng lẻ.
Nếu cần định dạng mới, phải bổ sung hàm mới vào `math_type.py`, không viết trùng
logic định dạng bên trong từng chương.

---

## Số câu mặc định theo vai trò tài khoản

Tham số `socau` **không được** Generator Function tự quyết định.

Giá trị `socau` do tầng gọi (CN_CallPythonGenerator / API) truyền vào, theo quy tắc:
Tài khoản Học sinh (làm bài online, 1 học sinh làm 1 đề)
↓
socau = 1 (mặc định, không cho đổi)

Tài khoản Giáo viên (ra đề, cần nhiều mã đề tương đương)
↓
socau = theo yêu cầu trong Request (Blueprint)

Logic phân biệt vai trò này thuộc về Business Logic ở FastAPI/n8n
(theo `01_ARCHITECTURE.md`: *"Business Logic ↓ FastAPI"*),
**không** đặt cứng trong Generator Function.

---

## Nhiều biến thể cho cùng 1 Generator ID

Xem chi tiết tại `04_ID_STANDARD.md` (mục "Biến thể nội dung trong Python").

Tóm tắt
1 Generator ID  →  có thể có NHIỀU hàm Python (biến thể _01, _02, ...)
1 hàm Python    →  vẫn tuân thủ mô hình sinh nhiều mã đề (tham số socau)

Ví dụ đầy đủ

```python
def L10_C1_B1_VD014_MC_A_01(socau, socot):
    """Biến thể 1: bối cảnh mệnh đề chứa biến đại số."""
    ...

def L10_C1_B1_VD014_MC_A_02(socau, socot):
    """Biến thể 2: bối cảnh mệnh đề thực tiễn."""
    ...
```

Khi Request yêu cầu `generator_id = L10_C1_B1_VD014_MC_A` với `socau = 3`:

- Hệ thống thấy có 2 biến thể (`_01`, `_02`).
- Có thể chọn ngẫu nhiên 1 biến thể rồi gọi với `socau=3`,
  hoặc chia ra gọi nhiều biến thể khác nhau — quy tắc phân bổ cụ thể
  do CN_CallPythonGenerator quyết định, không thuộc phạm vi Generator Function.

---

## Không thay đổi

- Một chương vẫn chỉ có một file Python (`L10_C1.py`, `L10_C2.py`...).
- Generator Function không gọi AI, không đọc PPCT/Curriculum/Mapping,
  không sinh PDF/Web Test trực tiếp.