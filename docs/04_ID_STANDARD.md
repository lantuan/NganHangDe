# TIÊU CHUẨN ID TOÀN HỆ THỐNG

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

ID là xương sống của toàn bộ hệ thống. Mọi thành phần làm việc
bằng ID thay vì tên hiển thị. AI không được tự suy luận hoặc
tự tạo ID — chỉ Code Node được phép ghép/chọn ID theo quy tắc.

---

# Cấu trúc chung

L10_C1_B2_NB017_MC_A

L10 = Khối
C1 = Chương
B2 = Bài
NB = Mức độ
017 = Mã năng lực (lấy từ Curriculum, không tự sinh)
MC = Loại câu
A = Phiên bản

---

# Khối

L10, L11, L12

---

# Chương

C1, C2, C3, ...

---

# Bài

B1, B2, B3, ...

---

# Mức độ

NB — Nhận biết
TH — Thông hiểu
VD — Vận dụng
VDC — Vận dụng cao

---

# Mã năng lực

Lấy nguyên văn từ Curriculum. Không được tự sinh, không tự
thêm hậu tố chữ cái vào mã năng lực gốc.

---

# Loại câu

MC — Trắc nghiệm nhiều lựa chọn
TF — Đúng/Sai
SA — Trả lời ngắn
TL — Tự luận

Có thể mở rộng thêm trong tương lai.

---

# Phiên bản

A, B, C... Một năng lực có thể có nhiều câu hỏi khác nhau.

Ví dụ

L10_C1_B2_NB017_MC_A
L10_C1_B2_NB017_MC_B
L10_C1_B2_NB017_MC_C

---

# Ngoại lệ 1: Câu Đúng/Sai (TF) ra theo Chương

Câu TF không gắn với một Bài cụ thể, ra theo cả chương.

ID rút gọn:

L<khối>_C<chương>_TF_<phiên bản>

Ví dụ

L10_C1_TF_A
L10_C1_TF_B

Một câu TF lớn mặc định gồm 4 ý nhỏ mức độ: NB, TH, VD, VDC.

Candidate Pool của TF không đi qua Curriculum — chỉ ghép trực
tiếp Blueprint + Mapping theo chuong_so.

---

# Ngoại lệ 2: Mức VDC dùng chung Curriculum ID mức VD

Curriculum chỉ có 3 mức: NB, TH, VD. Không tồn tại curriculum_id
dạng VDC.

Toàn bộ câu VDC mượn curriculum_id của một competency mức VD
đã có sẵn. Quyết định một lượt sinh câu là VD hay VDC nằm ở
CN_QuestionSelector, không nằm ở Curriculum hay Blueprint.

Ví dụ

curriculum_id = L10_C1_B2_VD006

có thể phân bổ: tong_so_cau=3, so_cau_VD=2, so_cau_VDC=1.

curriculum_id không đổi, không thêm hậu tố VDC.

---

# PPCT

Dùng ID dạng L10_C1_B2. Không cần mức độ, không cần loại câu.

---

# Curriculum

Ví dụ: L10_C1_B2_TH014. Trong đó TH014 là năng lực.

---

# Mapping

Ví dụ: L10_C1_B2_VD020_TL_A. Mapping là cầu nối giữa Curriculum
và Python Generator (hoặc giữa Blueprint và Python Generator
đối với TF).

---

# Python

Tên file: L10_C1.py
Tên hàm: L10_C1_B2_NB017_MC_A()

Không đặt tên theo tiếng Việt. Tên hàm phải trùng Generator ID.

---

# API

Mọi API đều trả ID, không trả text trước.

Đúng: {"lesson_id":"L10_C1_B2"}
Sai: {"lesson":"Mệnh đề"}

---

# n8n

Toàn bộ Workflow làm việc bằng ID. Không dùng tên bài.

---

# AI

AI không được tự suy luận ID.
AI chỉ nhận ID có sẵn, hoặc sinh Request để Code đổi sang ID.
Không AI nào (kể cả CHV_Fun, CHV_Grader, CHV_Analyzer) được tự
tạo curriculum_id, generator_id, hay bất kỳ ID nào khác.

---

# Database

Các bảng chỉ lưu ID: lesson_id, question_id, curriculum_id,
mapping_id. Không lưu tên bài nếu không cần thiết.

---

# Quy tắc bất biến

ID là chuẩn duy nhất. Không sửa ID sau khi phát hành. Nếu thay
đổi nội dung chỉ tạo Version mới.

Ví dụ: L10_C1_B2_NB017_MC_B (đúng) — không sửa
L10_C1_B2_NB017_MC_A đã phát hành.

---

# Mục tiêu cuối cùng

FastAPI → n8n → Python → LaTeX → Dashboard → AI → Database
đều giao tiếp bằng ID. Tên hiển thị chỉ dùng ở giao diện người dùng.

===== FILE: docs/04_ID_STANDARD.md (thêm vào cuối file, TRƯỚC mục "Mục tiêu cuối cùng") =====

---

# GHI CHÚ CẬP NHẬT — Version 2.1

Trạng thái

🟢 Chuẩn chính thức (bổ sung)

---

## Biến thể nội dung trong Python (Content Variant)

Phân biệt rõ hai khái niệm:

```
Generator ID (ID chuẩn, dùng ở Mapping/Curriculum/Database/API)
    ↓
L10_C1_B1_VD014_MC_A
```

Content Variant (chỉ tồn tại trong Python file, KHÔNG xuất hiện ở nơi khác)
↓
L10_C1_B1_VD014_MC_A_01
L10_C1_B1_VD014_MC_A_02
L10_C1_B1_VD014_MC_A_03
...

Ý nghĩa

Một Generator ID có thể có NHIỀU hàm Python khác nhau, mỗi hàm là một
cách ra đề khác nhau (bối cảnh khác, dạng số liệu khác) cho cùng một
năng lực/dạng bài. Đây là cách bổ sung dần độ phong phú của ngân hàng đề
mà không cần tạo ID mới.

Quy tắc đặt tên hàm
{Generator_ID}_{số thứ tự 2 chữ số}

Ví dụ
def L10_C1_B1_VD014_MC_A_01(socau, socot):
...
def L10_C1_B1_VD014_MC_A_02(socau, socot):
...

---

## Nơi hậu tố _NN được phép xuất hiện

CHỈ trong
data/python_bank/

KHÔNG được xuất hiện ở

- Mapping
- Curriculum
- PPCT
- Database
- API Response
- Blueprint
- Candidate Pool

Mọi nơi khác chỉ làm việc với Generator ID gốc (không hậu tố).

---

## Cơ chế gọi hàm (Function Resolution)

Khi hệ thống cần sinh câu hỏi cho một Generator ID:
Input: generator_id (VD: L10_C1_B1_VD014_MC_A), socau
↓
Quét file Python tương ứng chương, tìm tất cả hàm khớp:
{generator_id}_01, {generator_id}_02, ...
↓
Nếu chỉ có 1 hàm → dùng hàm đó.
Nếu có nhiều hàm → chọn ngẫu nhiên 1 hoặc nhiều hàm trong số đó.
↓
Gọi hàm đã chọn với (socau, socot/dong) tương ứng.

Nếu Generator ID không có bất kỳ hàm nào khớp (`_01` trở lên không tồn tại)
→ báo lỗi thiếu Generator, không tự suy diễn.

---

## Không được

- Không đặt tên hàm chỉ bằng Generator ID gốc khi có từ 2 biến thể trở lên
  (tránh trùng tên hàm Python trong cùng 1 file).
- Không đổi số thứ tự biến thể đã phát hành (VD: đã có `_01` thì không xoá,
  chỉ được thêm `_02`, `_03`... về sau — giữ đúng nguyên tắc bất biến ID
  đã nêu ở phần trên của tài liệu).