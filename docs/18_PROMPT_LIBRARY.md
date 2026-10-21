# PROMPT LIBRARY

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Lưu trữ Prompt chính thức của toàn bộ AI trong hệ thống. Mỗi AI
chỉ có một Prompt chính thức, quản lý theo phiên bản. Toàn hệ
thống chỉ có 3 AI.

---

# Danh sách Prompt

| AI | Prompt |
|-----|--------|
| CHV_Fun | Điều phối hệ thống + phân tích yêu cầu sinh đề |
| CHV_Grader | Chấm câu tự luận |
| CHV_Analyzer | Phân tích học tập + gợi ý luyện tập |

> **Bảng trên đã cũ — xem bảng đầy đủ ở mục "Cập nhật 21/10/2026" cuối tệp**
> (5 AI đang chạy trên n8n; `CHV_Analyzer` chưa có node).

---

===============================================================================

CHV_Fun

-------------------------------------------------------------------------------

Workflow

WF000_Gateway (+ WF001/WF002 khi task=generate_exam)

-------------------------------------------------------------------------------

Prompt

Điều phối toàn bộ hệ thống. Phân loại yêu cầu. Khi task=
generate_exam, đồng thời xác định cấu trúc đề (tra Table Tool
nếu học sinh chưa tự quy định).

Trả về:

{
    "task":"",
    "message":"",
    "cau_truc_de": {}
}

Không sinh đề. Không giải toán. Không trả lời kiến thức.
Không tự tạo ID.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Fun.md

---

===============================================================================

CHV_Grader

-------------------------------------------------------------------------------

Workflow

WF007_GradeExam

-------------------------------------------------------------------------------

Prompt

Chấm câu tự luận bằng cách so sánh bài làm học sinh với
answer/solution có sẵn trong Question Object. Không tự đặt đáp án.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Grader.md

---

===============================================================================

CHV_Analyzer

-------------------------------------------------------------------------------

Workflow

WF003_StudentAnalysis, WF007_GradeExam

-------------------------------------------------------------------------------

Prompt

Nhận Analysis Result (số liệu weak_points/strong_points đã tính
sẵn). Viết nhận xét khích lệ và đề xuất một lệnh luyện tập cụ thể
kèm tham số sẵn.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Analyzer.md

---

# Cập nhật 17/09/2026 — CHV_Fun phải chỉ đường khi từ chối (Version 2.60)

## Việc đã xảy ra

Học sinh gõ "giải cho tôi bài 3" trong Chat AI. CHV_Fun trả lời đại ý
"mình không có chức năng giải đâu nha" rồi dừng. Từ chối là ĐÚNG — bài
lẻ ngoài web không có đáp án Python nào để bám, giảng là phải tự tính,
mà mô hình tính số học rất hay sai.

Nhưng từ chối XONG THÌ BỎ EM ẤY GIỮA ĐƯỜNG. Hệ thống giờ ĐÃ CÓ gia sư
AI (v2.58) giảng lại từng bước — chỉ là em ấy không biết lối vào.

## Đã sửa

`data/prompts/CHV_Fun.md` thêm mục "Cách từ chối". Từ nay `message` của
task `reject_math_solution` phải có đủ 3 ý:

1. Từ chối giải bài lẻ (giữ giọng vui — cô Lan cố ý làm vui, giữ nguyên).
2. Nói rõ MÌNH GIẢNG ĐƯỢC, với câu trong đề em vừa làm trên web.
3. Chỉ đúng 3 bước: tạo đề → làm bài, nộp → bấm nút
   "💬 Hỏi thầy/cô AI về câu này" dưới câu chưa hiểu.

`reject_out_of_scope`: từ chối + chỉ lại 2 việc làm được.

Sửa kèm ở giao diện (không phụ thuộc AI, luôn chạy):
- `chat.html` lời chào mở đầu: thêm dòng "Chưa hiểu bài? Làm xong đề rồi
  bấm Hỏi thầy/cô AI về câu này".
- `chat.html` `addAIMessageLoi()`: mọi tin nhắn lỗi giờ chỉ CẢ HAI đường
  — nút "Tạo đề nhanh" và cách hỏi bài.
- `chat.py`: thông báo khi n8n trả JSON hỏng cũng chỉ đường tương tự.

## CẢNH BÁO — prompt trong repo đang LỆCH với n8n

`data/prompts/*.md` là BẢN GHI, không phải bản đang chạy. Prompt thật
nằm trong node AI trên n8n. Sửa tệp trong repo rồi thì PHẢI dán sang n8n
mới có tác dụng.

Hiện `CHV_Fun.md` NGẮN HƠN bản chạy thật (bản thật có thêm phần giọng
điệu, cách xưng hô — nhìn câu trả lời trên web là thấy). Lần tới mở n8n,
chép nguyên bản thật về đây để hết lệch. Đây là việc tồn đọng.

---

===============================================================================

# Quy tắc

- Một AI chỉ có một Prompt chính thức.
- Prompt lưu dưới dạng Markdown trong data/prompts.
- data/prompts là BẢN GHI; bản chạy thật nằm trên n8n. Sửa bên nào cũng
  phải đồng bộ sang bên kia ngay, không để lệch.
- Không sửa Prompt trực tiếp trong n8n.
- Ưu tiên đưa dữ liệu liệt kê (bảng tra cứu, ví dụ lặp lại) vào
  Table Tool thay vì viết cứng trong Prompt, để giảm token.
- Phần rule định dạng output (chỉ JSON, không markdown, không
  backtick, ký tự đầu {, ký tự cuối }) dùng chung 1 System Prompt
  cho cả 3 AI, không lặp lại trong từng Prompt riêng.
- Khi thay đổi Prompt phải cập nhật CHANGELOG.
---

# Cập nhật 03/10/2026 — CHV_Fun biết về bản tiếng Anh

`data/prompts/CHV_Fun.md` rule 5 (task `help`) thêm: nút Tiếng Việt | English, đề song sinh cùng ID/số liệu, KHI NÀO đề có bản Anh (chỉ khi người dùng tick "Kèm bản tiếng Anh" lúc tạo đề, và chương đã dịch; ô tick luôn hiện ở nơi tạo đề), vì sao bấm English mà đề vẫn tiếng Việt, tải cả hai thứ tiếng (.zip), mục tiêu Quyết định 2371/QĐ-TTg. Sửa tệp rồi thì PHẢI dán sang node CHV_Fun trên n8n. Việc còn lại: CHV_Fun vẫn chỉ viết tiếng Việt; trả lời bằng tiếng Anh khi trang ở English chưa làm.

---

# Cập nhật 21/10/2026 — Chép prompt thật của các AI còn lại + kiểm tính ngẫu nhiên của đề

Cô Lan chụp toàn bộ workflow `NganHangDe` trên n8n và gửi prompt của các node AI,
hỏi: **các prompt này có làm đề bớt ngẫu nhiên không?** Kết luận: **không**. Đã chép
prompt về `data/prompts/` (xong tồn đọng #6 ở `docs/06_N8N_WORKFLOW.md`).

## Năm AI đang chạy trên n8n

| AI (node) | Webhook | Bản ghi prompt | Ghi chú |
|---|---|---|---|
| `CHV_Fun` | `/webhook/chat` | `data/prompts/CHV_Fun.md` | Phân loại ý định (`task`) |
| `GenerateExam_RequestParser` | `/webhook/chat` (sau `Switch`, task `generate_exam`) | `data/prompts/GenerateExam_RequestParser.md` | Bóc yêu cầu thành cấu trúc đề; Memory + Table Tool `QuyDinhSoLuongCauTrongDe` |
| `DocPhieuTraLoi` | `/webhook/doc-phieu-tra-loi` | `data/prompts/DocPhieuTraLoi.md` | Chỉ đọc ô tô trên ảnh Phiếu trả lời |
| `CHV_Grader` | `/webhook/cham-tu-luan` | `data/prompts/CHV_Grader.md` | Chấm ảnh bài tự luận theo `dap_an_mau` |
| `CHV_GiaSu` | `/webhook/gia-su` | **Không có tệp riêng** — System Message là `{{ $json.body.lenh_he_thong }}`, do Python dựng: `LENH_HE_THONG` / `LENH_HE_THONG_EN` trong `app/services/gia_su_service.py` (`dung_lenh`) | Vì vậy trên n8n "không thấy prompt": prompt nằm trong mã nguồn, có test (`tests/test_gia_su.py`), xem `docs/23_GIA_SU_AI.md` |

`CHV_Analyzer` (bảng đầu tệp) chưa có node trên n8n.

## Vì sao prompt không ảnh hưởng tính ngẫu nhiên

Tính ngẫu nhiên của đề nằm ở ba chỗ, **cả ba đều là Python trên máy chủ**:

1. **Ma trận** (`exam_blueprint_service.build_blueprint`): chia số câu theo bài, làm tròn
   ngẫu nhiên.
2. **Chọn dạng / ID** (`question_selector_service.select_questions`): rút ngẫu nhiên, xoay
   vòng để không lặp dạng vừa dùng.
3. **Số liệu** (các hàm trong `data/python_bank`): mỗi đề một hạt giống
   `secrets.randbelow(2**31)` rút ngay trên máy chủ (`exam_assembler_service`), mỗi mã đề
   `seed + chi_so * 104729`.

`GenerateExam_RequestParser` chỉ xuất **cấu trúc**: `lop`, `ki_thi`, `pham_vi_chuong`,
`loai_he_so`, `cau_truc_tong_quat` (số câu mỗi loại), `ty_le_muc_do_goc`. Không xuất ID câu,
không xuất số liệu, không xuất hạt giống. Request `GenerateExamAutoRequest` của
`/api/exam/generate-pdf-auto` **không có trường hạt giống**; gửi thừa `seed` thì Pydantic bỏ qua.
Nút "Đồng ý, tạo đề" (`chat.html` → `xacNhanTaoDe`) và nút "Làm đề khác" gọi thẳng API, không
qua AI. `DocPhieuTraLoi`, `CHV_Grader`, `CHV_GiaSu` chạy **sau** khi đề đã sinh.

Việc duy nhất prompt quyết định là **cấu trúc** (bao nhiêu câu mỗi loại, tỉ lệ mức độ) — đúng
vai trò của nó. Mô hình có trả y hệt một JSON cho cùng một câu hỏi thì đề vẫn khác nhau.

**Đã kiểm (21/10/2026)**: gửi 6 lần cùng một JSON (lớp 10, HeSo1, 6 TN + 1 Đ/S + 2 TLN + 3 TL,
40/30/20/10) cho chương 1 và chương 3: 6/6 bộ ID khác nhau, 6/6 bộ số liệu khác nhau.
Test giữ lại: `tests/test_ngau_nhien_khong_qua_ai.py`.

## Quy tắc thêm (áp dụng cho mọi prompt sau này)

- **Prompt không bao giờ được xuất hạt giống, ID câu hay số liệu của câu.** AI chỉ nói *cần
  đề gì* (cấu trúc); *đề cụ thể* do Python rút. Nếu một ngày thêm trường như vậy vào JSON, test
  `test_api_sinh_de_khong_nhan_hat_giong_tu_ngoai` sẽ nhắc.
- Mỗi AI trên n8n phải có bản ghi trong `data/prompts/<TenNode>.md`, mở đầu bằng khối
  "ĐÂY LÀ BẢN CHÍNH THỨC" (ngày chép, node, webhook, ai gọi). Riêng prompt dựng trong Python
  (như `CHV_GiaSu`) thì ghi chỗ đặt ở bảng trên, không chép ra tệp riêng.

## Hai chỗ lệch giữa prompt và mã nguồn (ghi lại, CHƯA sửa)

Không liên quan đến tính ngẫu nhiên, nhưng thấy khi đối chiếu:

1. **`DocPhieuTraLoi` — số thập phân Phần III.** Prompt ví dụ `"-12.5"` (dấu chấm). Đáp án trả
   lời ngắn trong ngân hàng dùng dấu phẩy, nhiều câu bọc `$...$` (kiểm chương 2, 3 lớp 10: 55/130
   dạng SA có dấu phẩy, ví dụ `$-5,5$`). `grade_photo_service.py` chỉ bỏ khoảng trắng và đổi chữ
   thường trước khi so (không bỏ `$`, không coi `,` và `.` như nhau) → khi chấm bằng ảnh phiếu,
   đáp án thập phân đúng vẫn bị tính sai. Cách sửa gọn nhất là ở Python: so bằng
   `chuan_hoa_dap_an_ngan` (đã bỏ `$`) và đổi `.` thành `,` ở cả hai vế — không phụ thuộc mô hình
   đọc ra dấu gì.
2. **`CHV_Grader` — tên khoá điểm.** Mục QUY TẮC CHẤM viết `diem: số thực, làm tròn 0.25`, còn
   schema đầu ra và Python dùng `dung_sai_hoac_diem`. Hiện vẫn chạy vì mô hình theo schema; lần
   tới sửa prompt thì đổi chữ `diem` cho khớp.
