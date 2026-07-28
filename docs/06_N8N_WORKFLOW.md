# N8N WORKFLOW

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Toàn bộ nghiệp vụ triển khai bằng nhiều Workflow độc lập.
Mỗi Workflow chỉ thực hiện một nhiệm vụ.

---

# Danh sách Workflow

| Workflow | Chức năng |
|----------|-----------|
| WF000_Gateway | Điều phối toàn bộ hệ thống |
| WF001_GenerateExam | Sinh đề |
| WF002_GenerateExamByAbility | Sinh đề theo năng lực |
| WF003_StudentAnalysis | Phân tích học tập |
| WF004_DownloadFile | Tải file |
| WF005_Help | Hướng dẫn sử dụng |
| WF006_Reject | Từ chối yêu cầu |
| WF007_GradeExam | Chấm bài (MC/TF/SA tự động + TL bằng AI) |

---

# WF000_Gateway

Webhook → CHV_Fun → Switch → Execute Workflow

---

# Switch

generate_exam → WF001_GenerateExam
generate_exam_by_ability → WF002_GenerateExamByAbility
student_analysis → WF003_StudentAnalysis
download_file → WF004_DownloadFile
help → WF005_Help
reject_math_solution → WF006_Reject
reject_out_of_scope → WF006_Reject
grade_exam → WF007_GradeExam

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
Question Objects
↓
CN_QuestionValidator
↓
CN_ExamAssembler
↓
Exam Object
↓
Switch_OutputFormat
↓
CN_ResponseFormatter

---

# Switch_OutputFormat

latex → Generate LaTeX → Compile PDF
web_test → Generate Web Test
json → Generate JSON

---

# WF002_GenerateExamByAbility

Load Student History
↓
CN_AnalyzeResults (lấy weak_points từ lần làm bài trước)
↓
WF001_GenerateExam (ưu tiên bài/chương yếu)

---

# WF003_StudentAnalysis

Load Student History
↓
CN_AnalyzeResults
↓
CHV_Analyzer
↓
Learning Report + Gợi ý lệnh tiếp theo
↓
Dashboard

---

# WF004_DownloadFile

Find File → Download

---

# WF005_Help

CHV_Fun (task=help) → Response tĩnh

---

# WF006_Reject

CHV_Fun (task=reject_*) → Response tĩnh

---

# WF007_GradeExam

Đáp án học sinh + Exam Object
↓
CN_GradeAnswer (MC/TF/SA)
↓
CHV_Grader (TL — dùng answer/solution có sẵn)
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

# Execute Workflow

Các Workflow liên kết bằng Execute Workflow. Không gọi trực tiếp
Code Node giữa các Workflow.

---

# Quy tắc

- Một Workflow chỉ thực hiện một nhiệm vụ.
- Mỗi AI chỉ thuộc một Workflow.
- Mỗi Code Node chỉ thuộc một Workflow.
- WF000 là cổng vào duy nhất.
- Toàn hệ thống chỉ có 3 AI: CHV_Fun, CHV_Grader, CHV_Analyzer.
- Không tạo Workflow đa nhiệm.

---

# TODO

- WF008_AI_Tutor
- WF009_ExerciseRecommendation
- WF010_ClassDashboard
===============================================================================

# Hiện trạng triển khai (Version 2.3 — 2026-07-28)

Phần dưới đây mô tả ĐÚNG những gì đang chạy thật trên VPS, thay thế
cách hiểu ban đầu ở các mục phía trên cho WF001_GenerateExam.

## Thay đổi quan trọng

- CN_LoadCurriculum, CN_BuildBlueprint, CN_LoadMapping,
  CN_QuestionSelector, CN_CallPythonGenerator, CN_ExamAssembler
  KHÔNG còn là các Code Node riêng trong n8n. Toàn bộ đã được gộp
  thành 1 hàm Python duy nhất `generate_exam_pdf_auto()` trong
  `app/services/exam_assembler_service.py`, chạy trong tiến trình
  FastAPI. Lý do: giảm số điểm lỗi, debug bằng traceback Python
  trực tiếp thay vì dò từng Code Node, đã kiểm chứng chạy đúng qua
  Swagger UI (`/docs`) và test thật trên VPS.
- n8n giờ chỉ còn giữ đúng 2 việc trong WF001_GenerateExam:
  1. CHV_Fun — đọc tin nhắn tự nhiên của giáo viên/học sinh, suy ra
     tham số JSON đúng theo API bên dưới.
  2. HTTP Request — gọi thẳng 1 API duy nhất, nhận file trả về.
- CN_QuestionValidator (Giai đoạn 6, doc 09) CHƯA triển khai. Thay
  vào đó dùng cơ chế `cho_phep_thieu` (chế độ nháp) — xem doc 09
  bản cập nhật.
- Switch_OutputFormat hiện là 1 tham số `dinh_dang` trong cùng API
  (`pdf` | `tex` | `zip`), không tách 3 route latex/web_test/json
  riêng như dự kiến ban đầu. `web_test` và `json` CHƯA triển khai.
- WF000_Gateway, WF002–WF007 vẫn ở dạng dự kiến (TODO), chưa xây.

## API duy nhất mà n8n cần gọi cho WF001_GenerateExam

POST http://103.82.27.226:8000/api/exam/generate-pdf-auto

Body (JSON) — CHV_Fun phải suy ra đủ các trường sau từ tin nhắn:

```json
{
  "lop": 10,
  "tieu_de": "Đề kiểm tra Chương 1",
  "role": "teacher",
  "loai_he_so": "HeSo1",
  "ki_thi": null,
  "pham_vi_chuong": "chuong_1",
  "cau_truc_tu_hoc_sinh": null,
  "socau_ma_de": null,
  "cho_phep_thieu": true,
  "dinh_dang": "pdf"
}
```

Ghi chú tham số:
- `loai_he_so`: "HeSo1" (kiểm tra thường xuyên, cần `pham_vi_chuong`
  dạng "chuong_<số>") hoặc "HeSo2_HeSo3" (giữa kỳ/cuối kỳ, cần
  `ki_thi` là một trong: thuong_xuyen, giua_ky_1, cuoi_ky_1,
  giua_ky_2, cuoi_ky_2).
- `cho_phep_thieu`: true = chế độ nháp, câu nào ngân hàng đề còn
  thiếu sẽ hiện khung "[THIẾU CÂU HỎI: ...]" thay vì báo lỗi dừng
  cả đề. Đặt false khi ra đề thật cho học sinh.
- `dinh_dang`: "pdf" (mặc định), "tex" (mã LaTeX), hoặc "zip"
  (gồm cả PDF và TEX của cùng 1 đề, dùng khi giáo viên cần sửa tay).

Response: file nhị phân (PDF/TEX/ZIP), không phải JSON — n8n cần
đặt "Response Format: File" ở HTTP Request node.

## Đường đi đầy đủ hiện tại của luồng Chat

Frontend (`/chat`)
↓ POST form (message)
FastAPI `app/routers/chat.py` → `chat_post()`
↓ requests.post(...)
n8n Webhook (`https://fqrpl.n8npanel.com/webhook-test/chat`)
↓
CHV_Fun (AI node — phân tích tin nhắn → JSON tham số ở trên)
↓
HTTP Request → `/api/exam/generate-pdf-auto`
↓ (nhận file nhị phân)
Respond to Webhook (trả thẳng file nhị phân về FastAPI)
↓
FastAPI lưu file vào `app/static/downloads/`, trả JSON có link tải
↓
Frontend hiện nút tải file trong khung chat
