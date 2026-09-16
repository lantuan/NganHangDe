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


===============================================================================

# Trạng thái triển khai thực tế (cập nhật 2026-08-06)

Xem chi tiết ở docs/16_CHANGELOG.md, Version 2.4.

- Thực tế hiện tại KHÔNG tách thành nhiều Workflow độc lập như trên.
  Chỉ có 1 Workflow gộp: Webhook → CHV_Fun → Edit Fields → Switch
  → (2 nhánh có nối) → Respond to Webhook.
- 2 nhánh đang hoạt động:
  - task == "generate_exam" → Ghep_Tham_So (Code) → Goi_API_Sinh_De
    (HTTP → /api/exam/generate-pdf-auto) → Respond to Webhook.
  - task == "download_file" (dùng cho "xuất đáp án") →
    Goi_API_XuatDapAn (HTTP → /api/exam/export-loigiai) →
    Respond to Webhook.
- Switch còn 4 rule cũ chưa dọn: analyze_result, study_advice,
  history, general_chat — không khớp giá trị task nào CHV_Fun thực
  tế trả về, không nối tới đâu cả. Cần dọn/khớp lại khi triển khai
  WF002 (generate_exam_by_ability), WF003 (student_analysis),
  WF005 (help), WF006 (reject_*), WF007 (grade_exam) — các task này
  CHV_Fun đã phân loại được nhưng chưa có nhánh xử lý thật.
- CN_LoadExamScope, CN_LoadCurriculum, CN_BuildBlueprint,
  CN_LoadMapping, CN_QuestionSelector, CN_CallPythonGenerator,
  CN_QuestionValidator, CN_ExamAssembler trong sơ đồ WF001 ở trên
  hiện được gộp chung trong 1 lệnh gọi API
  /api/exam/generate-pdf-auto (FastAPI xử lý nội bộ), chưa tách
  thành các Code Node riêng trong n8n.


===============================================================================

# Cập nhật 2026-08-17 — GenerateExam_RequestParser + node hỗ trợ (Version 2.24)

Thực tế trong n8n hiện có THÊM 1 AI node nữa ngoài CHV_Fun/CHV_Grader
(doc 07 lúc trước ghi "chỉ có 3 AI" đã lỗi thời — xem đính chính ở
doc 07). Chi tiết đầy đủ: xem 16_CHANGELOG.md, Version 2.24.

Tóm tắt luồng task=generate_exam (nhánh CHV_Fun -> Switch dẫn tới):

CHV_Fun (task=generate_exam)
  -> Switch
  -> GenerateExam_RequestParser (AI node, có Memory + Table Tool
     QuyDinhSoLuongCauTrongDe)
  -> Parse_RequestParserOutput (Code node, JSON.parse thô, throw nếu
     JSON hỏng)
  -> Ghep_Tham_So (Code node - xem doc 16 Version cũ nhất nhắc, đang
     là task tồn đọng #16 sửa tiêu đề PDF không dấu)
  -> Goi_API_Sinh_De (POST http://103.82.27.226:8xxx/... - gọi thẳng
     backend FastAPI, KHÔNG qua các CN_ tách rời như sơ đồ lý tưởng
     ở doc 08)
  -> Goi_API_XuatDapAn (song song, xuất file đáp án)
  -> Respond to Webhook

Nhánh CHV_Fun (task=help/reject_math_solution/reject_out_of_scope) hoặc
Switch không khớp nhánh nào (Fallback):
  -> Code in JavaScript (Code node, xem doc 08 mục "Code in JavaScript")
  -> Respond to Webhook1

Node "doc-phieu-tra-loi" (DocPhieuTraLoi) và "cham-tu-luan" (CHV_Grader)
là 2 webhook RIÊNG, không nằm trong luồng chat chính ở trên - được
app/services/grade_photo_service.py gọi trực tiếp khi học sinh nộp ảnh
bài làm ở trang /lam-bai.


===============================================================================

# Cập nhật 2026-09-16 — Ghi lại TỪNG NODE của workflow `NganHangDe` (Version 2.58)

> **Quy tắc từ nay**: mỗi lần động vào n8n, ghi lại vào chính mục này —
> tên node, loại node, vào gì ra gì, và **vì sao** nó tồn tại. Sơ đồ n8n nhìn
> thì đẹp nhưng 3 tháng sau mở ra không ai nhớ node `Sua_Lop_Bang_Regex`
> sửa cái gì. Ghi ngay lúc làm, không để dồn.
>
> **Nguồn của mục này**: phần giao tiếp (URL, payload gửi/nhận) đọc **chắc
> chắn từ mã nguồn** Python. Phần cấu hình bên trong từng node đọc từ **sơ đồ
> canvas** — chưa mở từng node xác nhận, chỗ nào chưa chắc đã ghi rõ `(?)`.

## Toàn cảnh: MỘT workflow, BỐN webhook

Workflow tên `NganHangDe` (Personal). Trong cùng một canvas có **4 webhook độc
lập**, không nối với nhau — đây là thiết kế cố ý, không phải làm dở:

| # | Webhook | Ai gọi (mã nguồn) | Việc |
|---|---|---|---|
| 1 | `/webhook/chat` | `app/routers/chat.py::_goi_n8n` | Chat AI — phân loại ý định rồi làm theo |
| 2 | `/webhook/doc-phieu-tra-loi` | `grade_photo_service.py` | Đọc ảnh Phiếu trả lời (MC/TF/SA) |
| 3 | `/webhook/cham-tu-luan` | `grade_photo_service.py` | Chấm ảnh bài tự luận viết tay |
| 4 | `/webhook/gia-su` | `gia_su_service.py::_goi_mo_hinh` | **Mới v2.58** — giảng lại 1 câu cho học sinh |

Chỉ webhook #1 có `CHV_Fun` + `Switch`. **Ba webhook còn lại đi thẳng**, vì
việc của chúng đã được Python xác định rõ từ trước, không có gì để AI đoán.

---

## Nhánh 1 — `/webhook/chat` (luồng Chat AI)

```
Webhook ──► CHV_Fun ──► Edit Fields ──► Switch ──┬─► (generate_exam)  ──► ... xem dưới
   │           │                                  ├─► (download_file) ──► Goi_API_XuatDapAn ──► Respond to Webhook
   │           └── OpenRouter Chat Model          └─► (Fallback)      ──► Code in JavaScript ──► Respond to Webhook1
```

| Node | Loại | Vào | Ra | Làm gì |
|---|---|---|---|---|
| `Webhook` | Webhook POST | `{message, user_id, conversation_id, vai_tro}` | nguyên văn body | Cửa vào luồng chat. `vai_tro` (thêm v2.55) chỉ để AI **xưng hô** cho đúng — việc quyết định xuất lời giải hay không do máy chủ tra `profiles.vai_tro`, không tin trường này |
| `CHV_Fun` | AI Agent | tin nhắn học sinh/giáo viên | `{task: "...", ...}` | Phân loại ý định. Có Chat Model + Memory + Tool |
| `OpenRouter Chat Model` | Model | — | — | Mô hình cho `CHV_Fun` |
| `Edit Fields` (raw) | Set | đầu ra `CHV_Fun` | JSON phẳng | Dọn đầu ra AI thành trường phẳng để `Switch` đọc được |
| `Switch` (mode: Rules) | Switch | `task` | 1 trong N nhánh | Chia việc theo `task`. **Còn 4 rule cũ chưa dọn** (`analyze_result`, `study_advice`, `history`, `general_chat`) — không khớp `task` nào `CHV_Fun` thực trả, không nối đi đâu |

### Nhánh con `task == "generate_exam"`

```
Switch ─► GenerateExam_RequestParser ─► Parse_RequestParser_Output ─► Sua_Lop_Bang_Regex ─► Can_Xac_Nhan_Cau_Truc
                                                                                                │
                                                          ┌──── true ──► Tra_Loi_Xac_Nhan ──────┤
                                                          │                                     │
                                                          └──── false ─► Ghep_Tham_So ─► Goi_API_Sinh_De
                                                                                                │
                                                                                     Respond to Webhook
```

| Node | Loại | Làm gì |
|---|---|---|
| `GenerateExam_RequestParser` | AI Agent | Bóc yêu cầu thành tham số (lớp, chương, kỳ thi, số mã đề…). Có Memory + **Table Tool `QuyDinhSoLuongCauTrongDe`** (tra bảng số câu, để AI không tự bịa) + ModelFallback |
| `Parse_RequestParser_Output` | Code | `JSON.parse` thô, **throw nếu JSON hỏng** — hỏng sớm còn hơn đưa rác xuống dưới |
| `Sua_Lop_Bang_Regex` | Code | Chuẩn hoá tên lớp AI trả về (`"lớp 10"`, `"10A1"`, `"K10"` → `10`) bằng regex, không hỏi lại mô hình (?) |
| `Can_Xac_Nhan_Cau_Truc` | If/Switch | Cấu trúc đề đã đủ rõ chưa: **chưa** → hỏi lại người dùng; **rồi** → sinh đề luôn |
| `Tra_Loi_Xac_Nhan` | Code | Dựng câu hỏi xác nhận cấu trúc gửi về giao diện |
| `Ghep_Tham_So` | Code | Ghép tham số thành body cho API. **Tồn đọng #16**: tiêu đề PDF bị mất dấu tiếng Việt |
| `Goi_API_Sinh_De` | HTTP POST | `http://103.82.27.226:8xxx/api/exam/generate-pdf-auto` — FastAPI làm toàn bộ việc chọn câu/sinh đề/biên dịch |
| `Respond to Webhook` | Respond | Trả kết quả (JSON hoặc tệp nhị phân PDF/TEX) về `chat.py` |

> **Vì sao chỉ một lệnh gọi API mà không tách thành nhiều Code Node** (`CN_LoadExamScope`,
> `CN_BuildBlueprint`, `CN_QuestionSelector`… như sơ đồ lý tưởng ở doc 08): nguyên tắc
> **"Ưu tiên Code hơn AI"** ở doc 00. Việc chọn câu và ghép đề là logic xác định — để
> trong Python thì kiểm thử được, sửa được, không tốn lượt gọi mô hình.

### Các nhánh khác của `Switch`

| Nhánh | Node | Làm gì |
|---|---|---|
| `download_file` | `Goi_API_XuatDapAn` (HTTP POST → `/api/exam/export-loigiai`) → `Respond to Webhook` | Xuất tệp đáp án cho đề đã có |
| Fallback | `Code in JavaScript` → `Respond to Webhook1` | `help`, `reject_math_solution`, `reject_out_of_scope`, hoặc không khớp rule nào. Trả câu trả lời soạn sẵn, **không gọi mô hình lần nữa** |

---

## Nhánh 2 — `/webhook/doc-phieu-tra-loi`

```
doc-phieu-tra-loi ─► Convert to File ─► DocPhieuTraLoi ─► Respond to Webhook Cham bai
                     (Move Base64 String to File)   └── OpenRouter Chat Model2
```

| Node | Loại | Chi tiết |
|---|---|---|
| `doc-phieu-tra-loi` | Webhook POST | Vào: `{anh_base64, so_luong}` (`grade_photo_service.py` dòng ~80) |
| `Convert to File` | Convert to File | Đổi chuỗi base64 thành tệp nhị phân để node ảnh đọc được |
| `DocPhieuTraLoi` | AI Agent | Đọc ảnh Phiếu trả lời của Bộ, trả về đáp án học sinh tô cho từng câu |
| `Respond to Webhook Cham bai` | Respond | Trả danh sách đáp án đã đọc |

**AI ở đây chỉ *đọc chữ trên ảnh*, không chấm.** Việc so đáp án và tính điểm do
`grade_photo_service.py` + `diem_service.py` làm bằng Python.

---

## Nhánh 3 — `/webhook/cham-tu-luan`

```
cham-tu-luan ─► Convert to File1 ─► CHV_Grader ─► Respond to Webhook Cham tu luan
                                     └── OpenRouter Chat Model4
```

| Node | Loại | Chi tiết |
|---|---|---|
| `cham-tu-luan` | Webhook POST | Vào: `{anh_base64, danh_sach_cau: [{question_id, bai, diem_toi_da, dap_an_mau, chuong}]}` |
| `Convert to File1` | Convert to File | Như trên |
| `CHV_Grader` | AI Agent | Chấm bài tự luận viết tay. **Nhận sẵn `dap_an_mau`** (lời giải Python sinh) — chấm theo đáp án mẫu, không tự giải lại |
| `Respond to Webhook Cham tu luan` | Respond | Trả mảng `[{question_id, ...}]`, Python ghép lại theo `question_id` |

---

## Nhánh 4 — `/webhook/gia-su` (MỚI v2.58)

```
gia-su ─► CHV_GiaSu ─► Respond to Webhook Gia su
            └── OpenRouter Chat Model (dùng chung được)
```

Ba node. Không `CHV_Fun`, không `Switch`, không Code node, không Tool.

| Node | Loại | Cấu hình |
|---|---|---|
| `gia-su` | Webhook POST | Đường dẫn `gia-su`. Respond: **Using Respond to Webhook** |
| `CHV_GiaSu` | AI Agent | Source for Prompt: **Define below**<br>Prompt = `{{ $json.body.cau_hoi }}`<br>Options → System Message = `{{ $json.body.lenh_he_thong }}`<br>**Không Memory, không Tool** — mỗi lượt độc lập, lịch sử do Python gửi trong `lich_su` |
| `Respond to Webhook Gia su` | Respond | Respond With: **First Incoming Item**. Không gõ JSON tay — AI Agent trả khoá `output`, `_goi_mo_hinh()` đọc được |

**Payload vào** (do `gia_su_service.dung_lenh()` dựng — đọc chắc từ mã nguồn):

```json
{
  "muc": "A",
  "lenh_he_thong": "<đã chứa sẵn đề bài + đáp án + lời giải chuẩn>",
  "cau_hoi": "em chưa hiểu bước 2",
  "lich_su": [{"vai": "hs", "noi": "..."}, {"vai": "ai", "noi": "..."}],
  "question_id": "L10_C1_B2_VD01_MC_v1",
  "dap_an_python": "B. $4$"
}
```

`question_id` và `dap_an_python` gửi kèm **chỉ để n8n ghi log đối chiếu** — không
phải để n8n đi tra cứu gì.

**Ra**: `{"tra_loi": "..."}`. `_goi_mo_hinh()` cũng nhận được nếu n8n trả
`output` / `text` / `message` / `answer`, hoặc một mảng bọc ngoài.

### Vì sao nhánh này KHÔNG đi qua `CHV_Fun` → `Switch`

| | Hậu quả |
|---|---|
| **Tốn gấp đôi lượt gọi mô hình** | `CHV_Fun` chạy để phân loại, rồi node sau mới trả lời. Hai lượt cho một câu hỏi, trong khi dùng tài khoản miễn phí |
| **Phá lớp khoá 1** | `CHV_Fun` có system prompt riêng, sẽ trộn với `lenh_he_thong`. Các câu "KHÔNG TỰ TÍNH TOÁN", "cấm ra số khác lời giải mẫu" không còn là lệnh duy nhất |
| **Không có gì để đoán** | `Switch` chia theo ý định `CHV_Fun` suy ra. Python đã biết chắc học sinh hỏi câu số mấy, đề nào |

Chi tiết ba lớp khoá: `docs/23_GIA_SU_AI.md`.

---

## Bốn quy tắc rút ra (áp dụng cho mọi nhánh sau này)

1. **Việc nào Python xác định được thì đừng để AI đoán.** `Sua_Lop_Bang_Regex` là
   ví dụ đúng: chuẩn hoá tên lớp bằng regex thay vì hỏi lại mô hình.
2. **AI nhận sẵn đáp án chuẩn, không tự tính.** `CHV_Grader` nhận `dap_an_mau`;
   `CHV_GiaSu` nhận `lenh_he_thong` đã chứa lời giải. Đây là cùng một nguyên tắc.
3. **Webhook nào việc đã rõ thì đi thẳng, đừng nhét vào `Switch`.** Ba trong bốn
   nhánh hiện tại đi thẳng. `Switch` chỉ dành cho luồng chat — nơi thật sự phải
   đoán ý người dùng.
4. **Toàn bộ câu lệnh dựng ở Python, n8n chỉ gọi mô hình.** Thêm node tra cứu dữ
   liệu vào n8n là chuyển một phần logic ra khỏi chỗ có kiểm thử.

## Việc còn tồn đọng ở n8n

| # | Việc |
|---|---|
| 1 | Dọn 4 rule chết trong `Switch` (`analyze_result`, `study_advice`, `history`, `general_chat`) |
| 2 | `Ghep_Tham_So` làm mất dấu tiếng Việt ở tiêu đề PDF (tồn đọng #16) |
| 3 | `CHV_Fun` chưa hiểu "cho tôi 4 mã đề" trong chat — giáo viên phải vào `/gv/ra-de` |
| 4 | Mở từng node xác nhận các chỗ đánh `(?)` ở mục này |
