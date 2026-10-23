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

## Hai chỗ lệch giữa prompt và mã nguồn (ĐÃ SỬA cùng ngày — xem mục kế tiếp)

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

---

# Cập nhật 21/10/2026 (lần 2) — Đồng nhất các trường giữa prompt n8n và Python

Cô Lan: "đồng nhất các trường với nhau, không để mâu thuẫn xảy ra". Nguyên tắc chốt:
**trường nào Python tự biết thì Python đặt; từ AI chỉ lấy đúng phần AI đọc / chấm được, và
Python luôn chuẩn hoá phần đó.** Như vậy prompt có lệch chữ nào cũng không làm sai điểm, sai đề.
Mỗi chỗ đều có test đọc thẳng tệp prompt trong `data/prompts/` — sửa prompt mà Python chưa theo
thì test báo.

## Bảng đối chiếu

| AI | Trường | Prompt | Python | Trước | Nay |
|---|---|---|---|---|---|
| `DocPhieuTraLoi` | Phần III (trả lời ngắn) | ví dụ `"-12.5"` | đáp án ngân hàng `$-5,5$` | so nguyên chuỗi → thập phân đúng bị chấm sai | `chuan_hoa_dap_an_ngan` (chung với chấm trên web): bỏ `$`, `.` = `,`, `{,}` = `,`, `−` = `-`. Prompt đổi ví dụ thành `"-12,5"` |
| `DocPhieuTraLoi` | Phần II (`"D"`/`"S"`) | đọc từng ý | — | đọc xong bỏ đó, câu Đ/S luôn "cần chấm tay" | chấm theo số ý đúng, đúng cách tính của `/grade` (`diem_cau_tf`) |
| `DocPhieuTraLoi`, `CHV_Grader` | vỏ JSON | "chỉ JSON" | — | n8n trả `{"output": "..."}` hay có ```` ``` ```` là hỏng | `_boc_json` bóc được; JSON hỏng thật thì báo lỗi rõ |
| `CHV_Grader` | điểm | `diem:` trong QUY TẮC, `dung_sai_hoac_diem` trong schema | đọc `dung_sai_hoac_diem` | hai tên | prompt thống nhất `dung_sai_hoac_diem`; Python nhận cả `diem`, ép về số, chặn `[0; diem_toi_da]`, làm tròn 0,25; không đọc được → `loi_cham` (không cộng bừa) |
| `CHV_Grader` | `loai_cau`, `diem_toi_da`, `chuong`, `bai` | AI tự ghi (`"tu_luan"`) | `"TL"`, thang điểm `diem_service` | lấy nguyên của AI → AI ghi sai `diem_toi_da` là lệch tổng điểm | Python tự đặt cả bốn; prompt ghi `"TL"` cho khớp |
| `GenerateExam_RequestParser` | `ki_thi` | 9 slug, có `hoc_ky_1`, `hoc_ky_2` | chỉ nhận `giua_ky_1/2`, `cuoi_ky_1/2` | đề "học kỳ" hỏng (`KI_THI_KHONG_HOP_LE`) | `exam_scope_service.KI_THI_BI_DANH`: `hoc_ky_x` = `cuoi_ky_x`; kỳ thi lạ báo lỗi nói rõ phải chọn giữa kỳ hay cuối kỳ |
| `GenerateExam_RequestParser` | `pham_vi_chuong` | được trả `"chua_xac_dinh"` | đổi `chuong_x` sang số | lỗi 500 (`ValueError`) | lỗi 400 "Chưa rõ chương nào..." |

Test: `tests/test_cham_anh_dong_nhat.py`, `tests/test_dong_nhat_request_parser.py`.

## Việc cô Lan làm trên n8n (chỉ sửa đúng các dòng này)

- Node `DocPhieuTraLoi`, dòng cuối mục ĐỊNH DẠNG JSON: `(vd "75", "-12.5")` → `(vd "75", "-12,5")`.
- Node `CHV_Grader`, mục QUY TẮC CHẤM: `- diem: số thực, làm tròn 0.25.` →
  `- dung_sai_hoac_diem: số thực, làm tròn 0.25.`; trong schema: `"loai_cau": "tu_luan",` →
  `"loai_cau": "TL",`.

Chưa dán thì vẫn chấm đúng (Python đã tự chuẩn hoá) — dán để chữ trên n8n khớp bản ghi.

---

# Cập nhật 23/10/2026 — CHV_Fun v2.7 + ba prompt mới chạy qua webhook gia sư

Cô Lan: "tôi cần chat được bình thường như chatbox bình thường khác. Chỉ là các nội dung bên ngoài thì không giải
quyết mà hướng người dùng về tạo đề và nội dung toán. Nếu hỏi về kiến thức toán thì AI có thể đọc ngay phần lý thuyết
có sẵn để trả lời, chỉ trả lời trong đó."

## Bảng prompt sau ngày 23/10/2026

| Prompt | Chạy ở node / webhook | Bản ghi | Dùng khi |
|---|---|---|---|
| `CHV_Fun` **v2.7** | `CHV_Fun`, `/webhook/chat` | `data/prompts/CHV_Fun.md` | Mọi tin nhắn chat chưa được máy chủ tự xử lí |
| Gia sư **Mức A** | `CHV_GiaSu`, `/webhook/gia-su` | `LENH_HE_THONG` / `_EN` + `_QUY_TAC[(lang, "A")]` trong `app/services/gia_su_service.py` | Giảng lại một câu trong đề đã làm, chỉ theo lời giải mẫu |
| Gia sư **Mức B** | `CHV_GiaSu`, `/webhook/gia-su` | cùng tệp, `_QUY_TAC[(lang, "B")]` + khối "TÀI LIỆU LÍ THUYẾT CỦA THẦY/CÔ" | Hỏi tiếp về khái niệm mà lời giải mẫu không giải thích (đoạn tài liệu lấy từ `ly_thuyet_service.tim_doan`, chỉ các chương đã học) |
| **Hỏi kiến thức** | `CHV_GiaSu`, `/webhook/gia-su` (`muc = "kien_thuc"`) | `LENH_KIEN_THUC` / `_EN` trong `app/services/tro_chuyen_service.py` | Câu hỏi kiến thức gõ thẳng trong chat ("tập rỗng là gì") - chỉ trả lời theo đoạn tài liệu `tim_doan_tu_do` tìm được; không có đoạn nào thì không gọi mô hình |
| **Trò chuyện dự phòng** | `CHV_GiaSu`, `/webhook/gia-su` (`muc = "tro_chuyen"`) | `LENH_TRO_CHUYEN` / `_EN` trong `app/services/tro_chuyen_service.py` | CHV_Fun hỏng (n8n trả rỗng/hỏng) mà tin nhắn không phải yêu cầu tạo đề / hỏi cách dùng |

Ba prompt của gia sư / hỏi kiến thức / trò chuyện dự phòng nằm TRONG MÃ NGUỒN (Python dựng `lenh_he_thong`), có test
(`tests/test_gia_su.py`, `tests/test_gia_su_muc_b.py`, `tests/test_tro_chuyen.py`). Node `CHV_GiaSu` trên n8n không
phải sửa gì: System Message vẫn là `{{ $json.body.lenh_he_thong }}`.

## CHV_Fun v2.7 — đã sửa gì (chi tiết ở cuối `data/prompts/CHV_Fun.md`)

- Rule 7 thành **TRÒ CHUYỆN / NGOÀI PHẠM VI**: trò chuyện như người bạn (2-4 câu), chuyện ngoài Toán đáp vui một câu
  rồi hướng về tạo đề / ôn Toán. Bỏ "Không trả lời như chatbot".
- NHIỆM VỤ + Rule 6: câu hỏi kiến thức do máy chủ trả lời theo tài liệu trước khi tới CHV_Fun; câu nào vẫn tới là tài
  liệu chưa có -> nói rõ, gợi ý hỏi thầy/cô hoặc tạo đề.
- Rule 5 thêm tính năng thật: hỏi kiến thức, nút Đúng chương trình / Nâng cao thêm, ô hỏi tiếp, nút xem lời giải.
- JSON và tên `task` giữ nguyên -> `Switch`, `Code in JavaScript` không phải sửa.

## Việc cô Lan làm trên n8n

1. Node `CHV_Fun` → ô **System Message**: xoá hết, dán **chỉ phần lệnh** (từ "Bạn là CHV_Fun." đến hết mục QUY TẮC
   trong `data/prompts/CHV_Fun.md`; bản chép sẵn: `nhap/CHV_Fun_dan_vao_n8n.txt`). Trước đây ô này chứa cả phần ghi
   chú đầu/cuối tệp (khoảng 15 KB) - tốn token mỗi lượt và có đoạn `{{ ... }}` bị tính như biểu thức.
2. Node `Edit Fields` (mode JSON): thay `{{ JSON.parse($json.output) }}` bằng biểu thức đọc JSON chịu lỗi (bỏ đoạn
   `<think>...</think>`, bỏ ```json, lấy từ dấu `{` đầu đến `}` cuối; vẫn hỏng thì coi chữ mô hình viết là câu trả
   lời `task = "help"` thay vì làm hỏng cả luồng):
   ```
   {{ (() => { const s = String($json.output ?? '').replace(/<think>[\s\S]*?<\/think>/gi, '').replace(/```(json)?/gi, ''); const a = s.indexOf('{'), b = s.lastIndexOf('}'); for (const t of [s.slice(a, b + 1), s.slice(a, b + 1).replace(/\r?\n/g, ' ')]) { try { return JSON.parse(t); } catch (e) {} } return { task: 'help', message: $('Webhook').item.json.body.message, tra_loi: s.trim() || 'Mình chưa hiểu ý bạn, bạn nói rõ hơn giúp mình nhé!' }; })() }}
   ```
3. (Nên) Node `CHV_Fun` → bật **Enable Fallback Model**, nối thêm một OpenRouter Chat Model khác (vd
   `google/gemini-2.0-flash-001`) phòng khi mô hình chính (qwen/qwen3-8b) hết lượt / bị gỡ.

Sửa xong bấm **Save**. Chưa làm thì web vẫn chạy (máy chủ tự xử lí khi n8n hỏng), nhưng câu trò chuyện sẽ do AI dự
phòng trả lời thay vì CHV_Fun.

# Cập nhật 23/10/2026 (chiều) — CHV_Fun v2.8: chốt PHẠM VI

Cô Lan (ảnh): chat tự tính "7 x 7 bằng 49", rủ "tạo vài đề ôn bảng cửu chương"; học sinh đồng ý ("vâng. tạo cho tôi",
"bảng cửu chương mà", "mấy cũng được. miễn tôi rèn luyện được") thì AI hỏi lại số câu, phép nhân mấy đến mấy... mãi mà
không làm được. Cô chốt: **kiến thức ngoài tài liệu lí thuyết GV (người tạo) đưa thì AI không dạy; đề phải theo ngân
hàng đề GV đưa - đơn vị kiến thức Toán THPT lớp 10-12.**

| Chỗ | Sửa |
|---|---|
| Máy chủ, trước n8n (`app/services/pham_vi_service.py`, gọi ở `chat.py`) | Câu soạn sẵn, không gọi mô hình, không tính lượt: (1) ngoài phạm vi - bảng cửu chương, lớp 1-9 / tiểu học / THCS, môn khác, nhờ tính "7x7=?" -> nói rõ không làm được + danh sách chương lớp của học sinh; (2) muốn đề mà chưa nói chương / kỳ thi / chủ đề -> danh sách chương + cách gõ ("đề chương 3", "lớp 10 giữa kỳ 1"). Danh sách chương lấy từ `data/ppct/`, chỉ chương đã có tệp ngân hàng. Câu có chương, kỳ thi hay tên chủ đề ("đề hàm số bậc hai") vẫn đi n8n như cũ. |
| Hỏi kiến thức (`chat.py`) | Tài liệu lí thuyết không có đoạn nào -> câu soạn sẵn "Phần này chưa có trong tài liệu lí thuyết của thầy/cô..." thay vì để CHV_Fun tự trả lời. |
| Trò chuyện dự phòng (`LENH_TRO_CHUYEN` / `_EN`) | Thêm mục PHẠM VI kèm danh sách chương của lớp học sinh; không rủ đề ngoài danh sách; không tự tính (kể cả 7 x 7); không hỏi lại số câu / chủ đề, mà bảo gõ "đề chương <số>". |
| `CHV_Fun` v2.8 (`data/prompts/CHV_Fun.md`) | Mục PHẠM VI mới; Rule 6 thêm "nhờ tính một phép tính"; Rule 7 chỉ gợi ý đề trong phạm vi. JSON, tên `task` giữ nguyên. |

Việc cô Lan làm trên n8n: dán lại ô System Message của node `CHV_Fun` bằng `nhap/CHV_Fun_dan_vao_n8n.txt` (bản v2.8).
Chưa dán thì phần chặn ở máy chủ vẫn chạy; chỉ câu trò chuyện do CHV_Fun trả lời là chưa có quy tắc PHẠM VI.
