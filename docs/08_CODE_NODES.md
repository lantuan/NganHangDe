# CODE NODES

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Code Node chỉ xử lý dữ liệu. Không thực hiện suy luận AI.
Không sinh câu hỏi, không sinh đề, không thay thế Python Generator.

---

# Quy tắc đặt tên

CN_<Tên>

---

# WF001_GenerateExam

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
CN_CallPythonGenerator
↓
CN_QuestionValidator
↓
CN_ExamAssembler
↓
Switch_OutputFormat
↓
CN_ResponseFormatter

---

===============================================================================

CN_LoadExamScope

-------------------------------------------------------------------------------

Input

Request JSON (lop, ki_thi, pham_vi_chuong, loai_he_so) từ CHV_Fun

Output

pham_vi_chuong, pham_vi_bai

Nhiệm vụ

- Đọc PPCT theo lớp.
- Nếu loai_he_so=HeSo1 và pham_vi_chuong="chuong_x": lọc toàn bộ
  bài có chuong_so == x.
- Nếu ki_thi là giữa kỳ: lọc từ đầu học kỳ đến bài có
  boundary_after == GK1_EXAM/GK2_EXAM (bao gồm bài đó).
- Nếu ki_thi là cuối kỳ: lọc đến bài có boundary_after ==
  CK1_EXAM/CK2_EXAM.
- Nếu ki_thi là ôn tập: lấy toàn bộ PPCT của lớp/học kỳ.

Không được

- Đọc Curriculum, Mapping.
- Tự tạo hoặc tự sửa ID.

Lỗi

Nếu không khớp dữ liệu → {"error":"PPCT_NOT_FOUND"}

===============================================================================

CN_LoadCurriculum

Input: pham_vi_bai
Output: Curriculum JSON (đã lọc theo pham_vi_bai)

Không được: Chọn câu.

===============================================================================

CN_BuildBlueprint

-------------------------------------------------------------------------------

Input

cau_truc_tong_quat, ty_le_muc_do_goc, pham_vi_bai, Curriculum
(đã lọc theo pham_vi_bai)

Output

Blueprint

Nhiệm vụ

1. Chọn N chương cho câu TF (N = dung_sai_cau_lon): sắp xếp các
   chương trong pham_vi_chuong theo số bài giảm dần, lấy N chương
   đầu. Nếu chỉ có 1 chương trong phạm vi, toàn bộ TF thuộc chương đó.
2. Tính chỉ tiêu còn lại cho NB/TH/VD/VDC = tổng - so_cau_dung_sai
   (mỗi câu TF trừ 1 vào mỗi mức, vì gồm 1 NB+1 TH+1 VD+1 VDC).
3. Lấy Curriculum entries thuộc pham_vi_bai, group theo MucDo.
4. Phân bổ câu MC/SA/TL: ưu tiên đều giữa các bài; không lặp
   competency cùng mức nếu còn lựa chọn khác; chỉ lặp khi hết;
   tối đa 2 câu SA/chương; tối đa 2 câu TL/chương.
5. Với mỗi curriculum_id mức VD dùng cho SA/TL: chia so_cau_VD
   và so_cau_VDC theo chỉ tiêu còn lại. curriculum_id giữ nguyên,
   không đổi thành VDC.

Không được

- Đọc PPCT, Mapping.
- Gọi Python.
- Sinh PDF.
- Tự tạo hoặc tự sửa curriculum_id.
- Tạo curriculum_id mức VDC (không tồn tại).

Lỗi

Nếu Curriculum rỗng → {"error":"CURRICULUM_NOT_FOUND"}

===============================================================================

CN_LoadMapping

Input: Blueprint
Output: Mapping JSON (theo chương liên quan)

Không được: Chọn câu.

===============================================================================

CN_QuestionSelector

-------------------------------------------------------------------------------

Input

Blueprint, Mapping

Output

Question IDs (Generator ID)

Nhiệm vụ

- Với item TF: tìm Mapping entry theo chuong_so, loại TF, chưa
  dùng trong đề hiện tại.
- Với item MC/SA/TL: tìm Mapping entry có ID bắt đầu bằng
  curriculum_id + đúng Loại câu, chưa dùng trong đề hiện tại; nếu
  có nhiều phiên bản A/B/C thì xoay vòng để tăng đa dạng.

Đây là node duy nhất chọn Generator ID cuối cùng. Không có AI
nào tham gia bước này.

Không được

- Sinh câu hỏi, sinh LaTeX.

===============================================================================

CN_CallPythonGenerator

Input: Question IDs
Output: Question Objects

Nhiệm vụ: Gọi đúng hàm Python theo Generator ID.

Không được: Chọn ID.

===============================================================================

CN_QuestionValidator

Input: Question Objects
Output: Validated Questions

Nhiệm vụ: Kiểm tra trùng câu, đúng chương, đúng bài, đúng
Blueprint, đúng mức độ.

===============================================================================

CN_ExamAssembler

Input: Validated Questions
Output: Exam Object

Không được: Sinh PDF, sinh Web Test.

===============================================================================

Switch_OutputFormat

latex → Generate LaTeX → Compile PDF
web_test → Generate Web Test
json → Generate JSON

===============================================================================

CN_ResponseFormatter

Input: PDF, Web Test, JSON
Output: Response chuẩn hoá cho Frontend (theo doc 05).

===============================================================================

# WF007_GradeExam

-------------------------------------------------------------------------------

CN_GradeAnswer

Input: Đáp án học sinh, Answer Key (Exam Object)
Output: Kết quả chấm MC/TF/SA

Nhiệm vụ: Chấm tự động MC/TF/SA bằng so khớp trực tiếp với
answer_key. Câu TL: chuyển nguyên bài làm + Question Object
tương ứng sang CHV_Grader, không tự chấm.

-------------------------------------------------------------------------------

CN_MergeGradeResult

Input: Kết quả MC/TF/SA (Code) + Kết quả TL (CHV_Grader)
Output: Kết quả chấm đầy đủ toàn bài (theo Grade Result — doc 03)

Nhiệm vụ: Gộp 2 nguồn kết quả thành một bảng điểm thống nhất.

===============================================================================

# WF003_StudentAnalysis / WF007_GradeExam

CN_AnalyzeResults

Input: Kết quả chấm (Grade Result)
Output: Analysis Result (weak_points, strong_points)

Nhiệm vụ: Group theo chương/bài/tag, tính % đúng mỗi nhóm.
weak_points = nhóm có % đúng dưới ngưỡng (mặc định 50%).

Không được: Sinh nhận xét bằng lời — chỉ xuất số liệu. Văn bản
nhận xét do CHV_Analyzer đảm nhiệm.

===============================================================================

# Quy tắc

- Một Code Node chỉ làm một việc.
- Không có AI trong Code Node.
- Không có Prompt trong Code Node.
- Không có Python trong Code Node (trừ CN_CallPythonGenerator).
- Không sinh đề trong Code Node.
- Mọi dữ liệu truyền giữa các Node đều là JSON.
- Mọi bước chọn/ghép ID đều thuộc Code Node, không thuộc AI.

===============================================================================

# TODO

- CN_SaveExamHistory
- CN_SaveQuestionHistory
- CN_SaveStudentLog
- CN_CacheQuestion
- CN_CacheBlueprint