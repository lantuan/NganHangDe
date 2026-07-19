# KIẾN TRÚC HỆ THỐNG

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# 1. Mục tiêu

Kiến trúc được thiết kế theo hướng:

- Module hóa.
- Dễ mở rộng.
- Tách biệt dữ liệu.
- Giảm phụ thuộc vào AI tối đa (chỉ 3 AI cho toàn hệ thống).
- Có thể thay đổi từng thành phần mà không ảnh hưởng toàn hệ thống.

---

# 2. Kiến trúc tổng thể

User
↓
Frontend
↓
FastAPI
↓
WF000_Gateway
↓
CHV_Fun
↓
Switch
├── WF001_GenerateExam
│
├── WF002_GenerateExamByAbility
│
├── WF003_StudentAnalysis
│
├── WF004_DownloadFile
│
├── WF005_Help
│
├── WF006_Reject
│
├── WF007_GradeExam
│
└── Các Workflow mở rộng trong tương lai

---

# WF000_Gateway

Workflow điều phối trung tâm. Không xử lý nghiệp vụ.

- Nhận yêu cầu từ Frontend.
- Gọi CHV_Fun.
- Phân loại yêu cầu.
- Điều hướng sang Workflow phù hợp.

---

# CHV_Fun

AI điều phối trung tâm, đồng thời đảm nhận luôn việc phân tích cấu
trúc đề khi task = generate_exam (không cần AI RequestParser riêng).

CHV_Fun không:

- sinh đề;
- giải toán;
- sinh lời giải;
- trả lời kiến thức;
- đọc PPCT, Curriculum, Mapping;
- tự tạo hoặc tự chọn ID.

Output:

{
    "task": "...",
    "message": "...",
    "cau_truc_de": { ... }
}

`cau_truc_de` chỉ có khi task = generate_exam hoặc
generate_exam_by_ability.

---

# WF001_GenerateExam (không còn AI ở giữa)

CHV_Fun
↓
CN_LoadExamScope        (tra PPCT theo boundary_after)
↓
CN_LoadCurriculum
↓
CN_BuildBlueprint       (thuật toán phân bổ competency)
↓
CN_LoadMapping
↓
CN_QuestionSelector     (chọn Generator ID)
↓
CN_CallPythonGenerator
↓
Question Objects
↓
CN_QuestionValidator
↓
CN_ExamAssembler
↓
Exam Object
↓
Switch_OutputFormat
├── Generate LaTeX → Compile PDF
├── Generate Web Test
└── Generate JSON
↓
CN_ResponseFormatter
↓
Respond

---

# WF002_GenerateExamByAbility

Student History
↓
Weak Knowledge (lấy từ CN_AnalyzeResults của lần làm bài trước)
↓
WF001_GenerateExam (dùng weak_points để ưu tiên chọn bài/chương)

---

# WF003_StudentAnalysis

Student History
↓
CN_AnalyzeResults
↓
CHV_Analyzer
↓
Learning Report + Gợi ý lệnh luyện tập tiếp theo
↓
Dashboard

---

# WF004_DownloadFile

Find File
↓
Download

---

# WF005_Help

CHV_Fun (task=help) → Response tĩnh, không cần AI riêng.

---

# WF006_Reject

CHV_Fun (task=reject_*) → Response tĩnh, không cần AI riêng.

---

# WF007_GradeExam

Đáp án học sinh + Exam Object
↓
CN_GradeAnswer (chấm MC/TF/SA bằng so khớp trực tiếp)
↓
CHV_Grader (chấm TL, dựa trên answer/solution có sẵn)
↓
CN_MergeGradeResult
↓
Kết quả chấm đầy đủ
↓
CN_AnalyzeResults
↓
CHV_Analyzer
↓
Learning Report + Gợi ý lệnh tiếp theo

---

# Kiến trúc dữ liệu

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
Question IDs
↓
Question Objects
↓
Exam Object
↓
Output

Nhánh riêng: câu TF không đi qua Curriculum, chỉ ghép
Blueprint + Mapping theo chuong_so.

---

# Các Output chuẩn

PDF, LaTeX, Web Test, JSON — đều sinh từ cùng một Exam Object.
Tương lai có thể bổ sung DOCX, Moodle XML, QTI, SCORM mà không
cần đổi quy trình sinh đề.

---

# Nguyên tắc kiến trúc

- WF000 là cổng vào duy nhất.
- CHV_Fun luôn là AI đầu tiên.
- Toàn hệ thống chỉ có 3 AI: CHV_Fun, CHV_Grader, CHV_Analyzer.
- Mọi bước có quy tắc rõ ràng (tra bảng, phân bổ, chọn ID, so khớp
  đáp án) đều là Code Node, không dùng AI.
- Python chỉ sinh Question Object (gồm answer, solution).
- Exam Object là trung tâm của quy trình sinh đề.
- CHV_Grader chỉ được dùng answer/solution có sẵn, không tự đặt đáp án.

---

# 3. Thành phần

## Frontend

Đăng nhập, Chat AI, Sinh đề, Làm bài, Dashboard, Nút gợi ý luyện tập
(gửi thẳng tham số, không cần gõ lại lệnh mỗi vòng lặp).

## FastAPI

Trung tâm hệ thống: API, Authentication, đọc dữ liệu, gọi Python,
gọi n8n, trả kết quả. Tầng duy nhất được phép truy cập dữ liệu.

## n8n

Workflow Orchestrator. Không xử lý nghiệp vụ ngoài việc điều phối
Code Node và gọi đúng 3 AI khi cần.

## Python Generator

Sinh câu hỏi, đáp án, lời giải chuẩn. Không dùng AI.

## AI Agent (chỉ 3 AI)

CHV_Fun — hiểu yêu cầu.
CHV_Grader — chấm tự luận.
CHV_Analyzer — nhận xét + gợi ý.

## Database

Supabase: User, History, Exam, Result, Dashboard.

---

# 4. Nguyên tắc

Business Logic → FastAPI
Workflow → n8n
Mathematics → Python
Reasoning cần ngôn ngữ tự nhiên → AI (CHV_Fun / CHV_Grader / CHV_Analyzer)
Presentation → Frontend

---

# 5. Nguyên tắc phát triển

Không để Business Logic nằm trong Prompt.
Không để Business Logic nằm trong n8n.
Không để AI đọc dữ liệu thô nếu Code Node có thể xử lý trước.
Mọi dữ liệu đều phải đi qua API.
Code phải quyết định. AI chỉ hỗ trợ quyết định khi cần ngôn ngữ tự nhiên.

---

# 6. Luồng sinh đề

User → FastAPI → n8n → Code Node → Business API
→ Python Generator → LaTeX → PDF → Web

---

# 7. Luồng học sinh (vòng lặp đầy đủ)

Nhập lệnh (VD: "tạo đề chương 5")
↓
CHV_Fun (AI #1)
↓
WF001_GenerateExam (toàn Code Node)
↓
Học sinh làm bài (Web Test)
↓
Nộp bài
↓
WF007_GradeExam
  - CN_GradeAnswer (MC/TF/SA)
  - CHV_Grader (AI #2 — chấm TL)
↓
CN_AnalyzeResults
↓
CHV_Analyzer (AI #3 — nhận xét + gợi ý)
↓
Học sinh bấm nút gợi ý hoặc gõ lệnh mới
↓
Quay lại CHV_Fun

Nếu học sinh bấm nút gợi ý có sẵn tham số, vòng lặp tiếp theo
không cần gọi lại CHV_Fun để phân tích ngôn ngữ tự nhiên.

---

# 8. Luồng giáo viên

Đăng nhập → Tạo đề → Quản lý đề → Theo dõi học sinh
→ Phân tích lớp → Điều chỉnh lộ trình