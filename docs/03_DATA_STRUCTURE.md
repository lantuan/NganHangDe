# DATA STRUCTURE

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Quy định cấu trúc dữ liệu của toàn bộ hệ thống.
Workflow chỉ được trao đổi dữ liệu theo các Object quy định ở đây.

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

Quy định chương trình giảng dạy: chương, bài, tuần, tiết, lesson_type,
boundary_after (đánh dấu ranh giới GK1_EXAM/CK1_EXAM/GK2_EXAM/CK2_EXAM).

Không chứa năng lực, Generator, câu hỏi.

---

===============================================================================

# Curriculum

Mô tả các năng lực cần đạt: mức độ NB/TH/VD, verb, content, tags.

Curriculum KHÔNG có mức VDC. Mọi câu VDC dùng chung curriculum_id
của một competency mức VD; việc quyết định VD hay VDC nằm ở
CN_QuestionSelector, không nằm ở Curriculum.

Không chứa Generator, Python, câu hỏi.

---

===============================================================================

# Mapping

Mô tả các dạng bài, gắn với curriculum_id (đối với MC/SA/TL) hoặc
chuong_so (đối với TF).

Ví dụ

ID: L10_C1_B2_VD020_TL_A
content: Giải quyết bài toán tập hợp thực tế
Loai: Tự luận
Dang: Tập hợp thực tế

Không chứa câu hỏi, Python code.

---

===============================================================================

# Blueprint

Được tạo bởi CN_BuildBlueprint.

Quy định cấu trúc đề: lớp, học kỳ, chương, bài, số câu, mức độ,
loại câu, tỉ lệ. Không chứa Generator ID hay Question Object.

Cấu trúc mẫu:

{
  "dung_sai": [
    {"chapter_id":"L10_C1", "chuong_so":1, "so_cau":1}
  ],
  "trac_nghiem": [
    {"curriculum_id":"L10_C1_B1_NB001", "muc_do":"NB"}
  ],
  "tra_loi_ngan": [
    {"curriculum_id":"L10_C1_B2_VD006", "tong_so_cau":2,
     "so_cau_VD":2, "so_cau_VDC":0}
  ],
  "tu_luan": [
    {"curriculum_id":"L10_C1_B3_VD008", "tong_so_cau":3,
     "so_cau_VD":2, "so_cau_VDC":1}
  ]
}

---

===============================================================================

# Candidate Pool

Được tạo bởi CN_BuildCandidatePool.

Danh sách Generator có thể sử dụng, chưa chọn câu.

Nhánh MC/SA/TL: ghép Blueprint + Curriculum + Mapping theo
curriculum_id.

Nhánh riêng cho TF: KHÔNG đi qua Curriculum. Chỉ ghép
Blueprint (chapter_id, so_cau) + Mapping (theo chuong_so).

---

===============================================================================

# Generator IDs

Được tạo bởi CN_QuestionSelector.

Ví dụ: L10_C1_B1_TH014_MC_A, L10_C1_B2_VD020_TL_A, L10_C1_TF_A

Dùng để gọi đúng Generator Function.

---

===============================================================================

# Question Object

Được tạo bởi CN_CallPythonGenerator.

Gồm: generator_id, question_type, content, options, answer,
solution, latex, metadata.

answer và solution là căn cứ DUY NHẤT để CHV_Grader chấm tự luận.

---

===============================================================================

# Exam Object

Được tạo bởi CN_ExamAssembler.

Gồm: exam_info, blueprint, questions, answer_key, metadata.

Là dữ liệu chuẩn của toàn bộ hệ thống.

---

===============================================================================

# Grade Result (mới)

Được tạo bởi CN_GradeAnswer + CHV_Grader, gộp bởi CN_MergeGradeResult.

Gồm với mỗi câu:

{
  "question_id": "",
  "loai_cau": "MC | TF | SA | TL",
  "dung_sai_hoac_diem": "",
  "diem_toi_da": 0,
  "nhan_xet": "",
  "chuong": "",
  "bai": "",
  "tags": []
}

Câu TL có thêm nhan_xet, loi_sai từ CHV_Grader.
Câu MC/TF/SA chỉ có đúng/sai, không có nhan_xet.

---

===============================================================================

# Analysis Result (mới)

Được tạo bởi CN_AnalyzeResults.

{
  "weak_points": [
    {"chuong":"", "bai":"", "ty_le_dung": 0}
  ],
  "strong_points": [
    {"chuong":"", "bai":"", "ty_le_dung": 0}
  ]
}

Chỉ chứa số liệu. Không chứa văn bản nhận xét — văn bản do
CHV_Analyzer sinh từ Object này.

---

===============================================================================

# Output

Exam Object có thể sinh ra PDF, LaTeX, Web Test, JSON. Các Output
đều lấy dữ liệu từ cùng một Exam Object.

---

===============================================================================

# Metadata

Mỗi Question Object phải có: generator_id, lop, chuong, bai,
muc_do, loai, dang, tags, version, created_at.

---

===============================================================================

# Quy tắc

- PPCT chỉ chứa chương trình học.
- Curriculum chỉ chứa năng lực, không có mức VDC riêng.
- Mapping chỉ chứa dạng bài.
- Blueprint chỉ chứa cấu trúc đề.
- Candidate Pool của TF không đi qua Curriculum.
- Generator chỉ sinh Question Object.
- Exam Object là trung tâm của toàn bộ hệ thống.
- Grade Result và Analysis Result chỉ chứa số liệu, không chứa
  văn bản nhận xét cuối cùng.
- Mọi Output đều sinh từ Exam Object.