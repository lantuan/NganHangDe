# AI AGENTS

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Toàn hệ thống chỉ có 3 AI Agent. Mỗi AI chỉ đảm nhận nhiệm vụ
cần hiểu hoặc sinh ngôn ngữ tự nhiên. Mọi bước có quy tắc rõ ràng
(tra bảng, phân bổ, chọn ID, so khớp đáp án) đều là Code Node.

---

# Danh sách AI

| AI | Workflow | Chức năng |
|-----|----------|-----------|
| CHV_Fun | WF000/WF001/WF002 | Điều phối hệ thống + phân tích yêu cầu sinh đề |
| CHV_Grader | WF007 | Chấm câu tự luận dựa trên answer/solution có sẵn |
| CHV_Analyzer | WF003/WF007 | Viết nhận xét + gợi ý lệnh luyện tập tiếp theo |

---

===============================================================================

# AI

CHV_Fun

-------------------------------------------------------------------------------

## Workflow

WF000_Gateway (và phân tích cấu trúc đề khi task=generate_exam)

-------------------------------------------------------------------------------

## Mục tiêu

Hiểu yêu cầu tự nhiên của học sinh, phân loại nhiệm vụ (task),
và khi task=generate_exam thì đồng thời xác định cấu trúc đề
(số câu, mức độ, phạm vi chương) — tra Table Tool
QuyDinhSoLuongCauTrongDe nếu học sinh chưa tự chỉ định.

-------------------------------------------------------------------------------

## Input

Tin nhắn người dùng (tiếng Việt tự nhiên).

-------------------------------------------------------------------------------

## Output

{
    "task": "",
    "message": "",
    "cau_truc_de": { }
}

cau_truc_de chỉ có khi task = generate_exam hoặc
generate_exam_by_ability.

-------------------------------------------------------------------------------

## Chức năng

- Phân loại yêu cầu.
- Chọn Workflow phù hợp.
- Nếu học sinh đã tự quy định cấu trúc đề (VD "20 câu trắc nghiệm,
  50% NB") thì giữ nguyên yêu cầu, không ghi đè bằng Table Tool.
- Nếu học sinh chưa quy định, tra Table Tool để lấy cấu trúc mặc định.

-------------------------------------------------------------------------------

## Không được

- Sinh đề, giải toán, sinh lời giải, trả lời kiến thức.
- Đọc PPCT, Curriculum, Mapping.
- Tự tạo hoặc tự chọn ID (curriculum_id, generator_id...).

-------------------------------------------------------------------------------

## Workflow tiếp theo

Switch → WF001 / WF002 / WF003 / WF004 / WF005 / WF006 / WF007

===============================================================================

# AI

CHV_Grader

-------------------------------------------------------------------------------

## Workflow

WF007_GradeExam

-------------------------------------------------------------------------------

## Mục tiêu

Chấm điểm câu tự luận (TL) bằng cách so sánh bài làm của học sinh
với answer/solution có sẵn trong Question Object (do Python
Generator sinh ra từ trước, không phải AI tự nghĩ đáp án).

-------------------------------------------------------------------------------

## Input

- Bài làm của học sinh (text hoặc kết quả OCR từ ảnh chụp).
- Question Object tương ứng (answer, solution có sẵn).

-------------------------------------------------------------------------------

## Output

{
    "question_id": "",
    "diem": 0,
    "diem_toi_da": 0,
    "nhan_xet": "",
    "loi_sai": ""
}

-------------------------------------------------------------------------------

## Không được

- Tự đặt ra đáp án ngoài answer/solution có sẵn.
- Tự sinh câu hỏi mới.
- Sửa answer/solution gốc.
- Chấm câu MC/TF/SA (thuộc CN_GradeAnswer).

===============================================================================

# AI

CHV_Analyzer

-------------------------------------------------------------------------------

## Workflow

WF003_StudentAnalysis, WF007_GradeExam

-------------------------------------------------------------------------------

## Mục tiêu

Viết nhận xét kết quả học tập bằng văn phong tự nhiên, khích lệ,
và đề xuất một lệnh cụ thể để học sinh luyện tập tiếp (kèm tham
số sẵn để hệ thống chạy lại WF001 nếu học sinh xác nhận).

-------------------------------------------------------------------------------

## Input

Analysis Result (weak_points, strong_points) — CHỈ nhận số liệu
đã tính sẵn từ CN_AnalyzeResults, KHÔNG nhận Exam Object thô.

-------------------------------------------------------------------------------

## Output

{
    "nhan_xet": "",
    "goi_y_lenh_tiep_theo": "",
    "tham_so_goi_y": { }
}

-------------------------------------------------------------------------------

## Không được

- Tự tính lại % đúng/sai (đã được CN_AnalyzeResults tính sẵn).
- Đưa ra chẩn đoán tâm lý học sinh.
- Tự tạo ID.

===============================================================================

# Quy tắc

- Một AI chỉ thuộc một Workflow (CHV_Fun có thể được gọi lại từ
  nhiều Workflow nhưng vai trò không đổi).
- Một AI chỉ có một Prompt chính thức.
- AI không thực hiện nhiệm vụ của AI khác.
- Mọi yêu cầu đều bắt đầu từ CHV_Fun.
- Không tạo thêm AI mới nếu nhiệm vụ có thể giải quyết bằng Code Node.

===============================================================================

# TODO (giai đoạn sau, không thuộc vòng lặp tối thiểu)

- CHV_Tutor — gia sư AI tương tác nhiều lượt.
- CHV_ClassAssistant — trợ lý cho giáo viên quản lý lớp.

===============================================================================

# ĐÍNH CHÍNH 2026-08-17 (Version 2.24)

Câu "Toàn hệ thống chỉ có 3 AI: CHV_Fun, CHV_Grader, CHV_Analyzer" ở
trên đã LỖI THỜI. Thực tế hiện có thêm:

- GenerateExam_RequestParser: AI node riêng, chỉ chạy khi CHV_Fun đã
  phân loại task="generate_exam". Đọc yêu cầu học sinh, nếu thiếu cấu
  trúc đề (số câu/tỉ lệ mức độ) thì tra Table Tool "QuyDinhSoLuongCauTrongDe"
  để lấy cấu trúc chuẩn theo loại hệ số (HeSo1 = kiểm tra thường
  xuyên/15 phút/miệng: 12 câu (6 TN + 1 Đ/S + 2 TLN + 3 TL), tỉ lệ NB
  40% - TH 30% - VD 20% - VDC 10%; HeSo2_HeSo3 = giữa kỳ/cuối kỳ/học
  kỳ: 20 câu (12 TN + 2 Đ/S + 3 TLN + 3 TL), cùng tỉ lệ mức độ). Nếu
  học sinh đã tự quy định một phần/toàn bộ thì ưu tiên đúng yêu cầu đó,
  không ghi đè bằng bảng. Xuất JSON (không hỏi lại, không giải thích -
  xem 16_CHANGELOG Version 2.24 về đề xuất cải tiến "hỏi xác nhận cấu
  trúc đề" đang trong quá trình thiết kế, CHƯA triển khai).

- CHV_Grader: đã có sẵn từ trước (chấm bài tự luận qua ảnh, xem
  app/services/grade_photo_service.py), chỉ là trước đây chưa liệt kê
  đầy đủ ở file này.

Bảng QuyDinhSoLuongCauTrongDe (cột): KyThi, trac_nghiem, dung_sai,
tra_loi_ngan, tu_luan, NB, TH, VD, VDC. 2 dòng dữ liệu hiện có: HeSo1
và HeSo2_HeSo3 (chi tiết số liệu xem đoạn trên).
