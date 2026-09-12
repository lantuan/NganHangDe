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

Nhiệm vụ (cập nhật 2026-09-12 — mọi phân bổ làm ở cấp BÀI, không
phải cấp chương như bản cũ)

1. Chọn BÀI cho câu TF TRƯỚC TIÊN (N = dung_sai_cau_lon): sắp xếp các
   bài trong pham_vi_bai theo SỐ TIẾT giảm dần, lấy N bài đầu. Nếu
   N > số bài thì mới quay vòng lại. Mỗi câu TF lấy đủ 4 ý
   NB-TH-VD-VDC trong CÙNG một bài.
2. Tính chỉ tiêu còn lại cho NB/TH/VD/VDC = tổng - so_cau_dung_sai
   (mỗi câu TF trừ 1 vào mỗi mức, vì gồm 1 NB+1 TH+1 VD+1 VDC).
   CÁCH LÀM: trừ ngay tại BÀI mà TF đã chọn ("đơn vị kiến thức đó
   chia ra được 3 câu thì phải tính 1 ở đúng sai, chỉ còn 2"). Trừ ở
   cấp bài đã tự động làm tổng giảm đúng bằng so_cau_dung_sai —
   TUYỆT ĐỐI KHÔNG trừ thêm lần nữa ở cấp tổng (sẽ thành trừ 2 lần).
   Nếu bài đó vốn không được chia câu nào ở mức đang xét thì bỏ qua,
   KHÔNG đẩy phần trừ sang bài khác.
   Riêng mức VD/VDC có thể nằm ở cả 3 phần (MC/SA/TL) nên giữ một
   "ngân sách trừ" dùng chung, trừ theo thứ tự MC → SA → TL, mỗi câu
   TF chỉ được trừ MỘT LẦN. Đề đặt tỉ lệ VDC = 0 thì ý VDC của câu TF
   không trừ đi đâu cả (kẹp ở 0), câu TF vẫn giữ đủ 4 ý.
3. Lấy Curriculum entries thuộc pham_vi_bai, group theo (bài, MucDo).
4. Phân bổ câu MC/SA/TL mức NB/TH: chia về từng BÀI theo TỈ LỆ SỐ
   TIẾT của bài (số tiết lấy từ CN_LoadExamScope, trường
   so_tiet_theo_bai — blueprint KHÔNG được đọc PPCT). Làm tròn xuống,
   phần dư rải lần lượt cho bài nhiều tiết nhất trước. Không lặp
   competency cùng mức nếu còn lựa chọn khác; chỉ lặp khi hết;
   tối đa 2 câu SA/bài; tối đa 2 câu TL/bài.
5. Mức VD/VDC: chọn VDC TRƯỚC, mỗi BÀI tối đa 1 câu VDC (không dồn
   nhiều VDC vào cùng một đơn vị kiến thức). Sau đó rải VD, ưu tiên
   các bài CHƯA có VDC; hết bài trống mới quay lại bài đã có.
   Tỉ lệ VD:VDC lấy từ bảng exam_rules.json, KHÔNG ép cứng 2:1.
6. Với mỗi curriculum_id mức VD dùng cho SA/TL: chia so_cau_VD
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

===============================================================================

# Cập nhật 2026-08-17 — Code Node thực tế đang dùng trong nhánh chat (Version 2.24)

Khác với sơ đồ WF001 lý tưởng ở trên (CN_LoadExamScope...CN_ResponseFormatter,
đã gộp vào 1 API call như ghi chú Version cũ ở cuối file), nhánh CHAT
(webhook chính, không phải luồng sinh đề) hiện có 2 Code Node thật sau:

-------------------------------------------------------------------------------

Parse_RequestParserOutput

Input: output text thô của GenerateExam_RequestParser (field output/
text/content, tuỳ node AI trả về field nào).

Logic: JSON.parse() trực tiếp, throw Error nếu không phải JSON hợp lệ
(dừng luôn workflow tại đây, không có xử lý fallback - nếu AI trả sai
định dạng thì cả nhánh sinh đề sẽ lỗi ở bước này).

Output: JSON đã parse, giữ nguyên các field GenerateExam_RequestParser
trả ra (loai_he_so, lop, ki_thi, pham_vi_chuong, nguon_cau_truc,
cau_truc_tong_quat, ty_le_muc_do_goc...) để Ghep_Tham_So dùng tiếp.

-------------------------------------------------------------------------------

Code in JavaScript (nhánh trả lời chat thuần - help/reject_math_solution/
reject_out_of_scope/Fallback của Switch)

Input: field response_chv_fun (do node "Edit Fields" đặt tên) chứa
{task, message, tra_loi} là output gốc của CHV_Fun.

Logic:
- Lấy tra_loi từ response_chv_fun.
- Nếu có tra_loi (không rỗng) -> success=true, message=tra_loi.
- Nếu KHÔNG có tra_loi (rỗng/null) -> success=false, message = 1 câu
  ngẫu nhiên trong ngân hàng "cacCauChuaXong" (8 câu vui nhộn kiểu
  "Tính năng này đang được code cày cuốc, sắp ra lò rồi, chờ xíu nha!" -
  dùng cho các nhánh chưa triển khai, KHÔNG tốn AI token vì random.choice
  thuần JS, đúng nguyên tắc "Ưu tiên Code hơn AI" của doc 00).

Output: {"success": bool, "message": str, "data": null} - đúng định
dạng app/routers/chat.py mong đợi (content-type application/json, đọc
qua ket_qua.get("message")).
