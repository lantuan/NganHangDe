# EXAM GENERATION

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

WF001_GenerateExam chịu trách nhiệm sinh đề thi. Chỉ được gọi
từ WF000_Gateway. Không được gọi trực tiếp từ Frontend.

---

# Đầu vào

Request JSON (từ CHV_Fun) → Blueprint → Curriculum → Mapping

---

# Luồng tổng thể

CHV_Fun
↓
CN_LoadExamScope
↓
CN_LoadCurriculum
↓
CN_BuildBlueprint
↓
CN_LoadMapping
↓
CN_QuestionSelector
↓
Question IDs
↓
CN_CallPythonGenerator
↓
Question Objects
↓
CN_QuestionValidator
↓
Validated Questions
↓
CN_ExamAssembler
↓
Exam Object
↓
Switch_OutputFormat
↓
LaTeX / Web Test / JSON
↓
Response

---

===============================================================================

# Giai đoạn 1 — Phân tích yêu cầu (AI)

CHV_Fun

Input: Tin nhắn học sinh
Output: task, message, cau_truc_de

---

===============================================================================

# Giai đoạn 2 — Xác định phạm vi (Code)

CN_LoadExamScope

Input: cau_truc_de, PPCT
Output: pham_vi_chuong, pham_vi_bai

---

===============================================================================

# Giai đoạn 3 — Xây Blueprint (Code)

CN_BuildBlueprint

Input: cau_truc_de, pham_vi_bai, Curriculum
Output: Blueprint (không chứa Question ID)

---

===============================================================================

# Giai đoạn 4 — Chọn Question ID (Code)

CN_QuestionSelector

Input: Candidate Pool, Blueprint, Mapping
Output: Question IDs

Ví dụ: L10_C1_B1_TH014_MC_A, L10_C1_B2_VD020_TL_A, L10_C1_TF_A

Đây là bước quyết định gọi hàm Python nào.

---

===============================================================================

# Giai đoạn 5 — Python Generator

Input: Question IDs
Output: Question Objects (nội dung, đáp án, lời giải, metadata,
latex, hình ảnh nếu có)

---

===============================================================================

# Giai đoạn 6 — Question Validator

Kiểm tra: trùng ID, trùng nội dung, đúng Blueprint, đúng chương,
đúng bài, đúng mức độ, đúng loại câu.

Nếu lỗi → sinh lại Question ID → gọi lại Python.

---

===============================================================================

# Giai đoạn 7 — Exam Object

Input: Validated Questions
Output: Exam Object — dữ liệu chuẩn của toàn bộ hệ thống.

---

===============================================================================

# Giai đoạn 8 — Output

Switch_OutputFormat:
latex → Generate tex → Compile pdf
web_test → Generate Online Test
json → Generate JSON

---

===============================================================================

# Quy tắc

- Blueprint không chứa Question ID.
- Candidate Pool không chứa câu hỏi.
- Question Selector chỉ chọn ID, không dùng AI.
- Python chỉ sinh Question Object.
- Validator không sửa câu hỏi.
- Exam Object là trung tâm.
- PDF, Web Test, JSON đều sinh từ Exam Object.
- Toàn bộ Giai đoạn 2–8 là Code Node, không có AI nào can thiệp.

---

# TODO

- Sinh DOCX
- Sinh Moodle XML
- Sinh QTI
- Sinh SCORM