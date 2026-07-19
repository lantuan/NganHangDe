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