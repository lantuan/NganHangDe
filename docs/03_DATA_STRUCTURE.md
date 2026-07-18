# DATA STRUCTURE

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Quy định cấu trúc dữ liệu của toàn bộ hệ thống.

Workflow chỉ được trao đổi dữ liệu theo các Object được quy định trong tài liệu này.

---

# Luồng dữ liệu

PPCT

↓

Curriculum

↓

Mapping

↓

Blueprint

↓

Candidate Pool

↓

Generator IDs

↓

Question Objects

↓

Exam Object

↓

Output

---

===============================================================================

# PPCT

Mục đích

Quy định chương trình giảng dạy.

Ví dụ

- chương
- bài
- tuần
- tiết
- lesson_type

Không chứa

- năng lực
- Generator
- câu hỏi

---

===============================================================================

# Curriculum

Mục đích

Mô tả các năng lực cần đạt.

Ví dụ

- TH
- VD
- VDC

- verb

- content

- tags

Không chứa

- Generator
- Python
- câu hỏi

---

===============================================================================

# Mapping

Mục đích

Mô tả các dạng bài.

Ví dụ

ID

↓

L10_C1_B2_VD020_TL_A

Nội dung

↓

Giải quyết bài toán tập hợp thực tế

Loại

↓

Tự luận

Dạng

↓

Tập hợp thực tế

Không chứa

- câu hỏi
- Python code

---

===============================================================================

# Blueprint

Được tạo bởi

CHV_ExamPlanner

Mục đích

Quy định cấu trúc đề.

Bao gồm

- lớp
- học kỳ
- chương
- bài
- số câu
- mức độ
- loại câu
- tỉ lệ

Không chứa

- Generator IDs
- Question Objects

---

===============================================================================

# Candidate Pool

Được tạo bởi

CN_BuildCandidatePool

Mục đích

Danh sách Generator có thể sử dụng.

Ví dụ

L10_C1_B1_TH001_MC_A

L10_C1_B1_TH014_MC_A

L10_C1_B2_VD020_TL_A

...

Candidate Pool chưa chọn Generator.

---

===============================================================================

# Generator IDs

Được tạo bởi

CN_GeneratorSelector

Ví dụ

L10_C1_B1_TH014_MC_A

L10_C1_B2_VD020_TL_A

...

Generator ID dùng để gọi đúng Generator Function.

---

===============================================================================

# Question Object

Được tạo bởi

CN_CallGenerator

Một Question Object gồm

- generator_id
- question_type
- content
- options
- answer
- solution
- latex
- metadata

Question Object là đơn vị nhỏ nhất của đề.

---

===============================================================================

# Exam Object

Được tạo bởi

CN_ExamAssembler

Một Exam Object gồm

- exam_info
- blueprint
- questions
- answer_key
- metadata

Exam Object là dữ liệu chuẩn của toàn bộ hệ thống.

---

===============================================================================

# Output

Exam Object có thể sinh ra

- PDF
- LaTeX
- Web Test
- JSON

Các Output đều lấy dữ liệu từ cùng một Exam Object.

---

===============================================================================

# Metadata

Mỗi Question Object phải có Metadata.

Bao gồm

- generator_id
- lop
- chuong
- bai
- muc_do
- loai
- dang
- tags
- version
- created_at

---

===============================================================================

# Quy tắc

- PPCT chỉ chứa chương trình học.
- Curriculum chỉ chứa năng lực.
- Mapping chỉ chứa dạng bài.
- Blueprint chỉ chứa cấu trúc đề.
- Candidate Pool chỉ chứa Generator.
- Generator chỉ sinh Question Object.
- Exam Object là trung tâm của toàn bộ hệ thống.
- Mọi Output đều sinh từ Exam Object.