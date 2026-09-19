# 23. GIA SƯ AI — MỨC A

> Trạng thái: **Mức A đã xong** (16/09/2026). **Mức B chưa làm** — xem mục 8.
> Liên quan: `docs/00_*` (nguyên tắc "Ưu tiên Code hơn AI"), `docs/21_TAI_KHOAN_GIAO_VIEN.md`,
> `docs/22_BAO_MAT_RLS.md`.

---

## 1. Yêu cầu gốc

> "Tôi cần giảng lại ngay đề bài vừa ra cho HS — ở **mức A**. Và nếu HS vẫn không hiểu
> thì có thể lấy tài liệu lí thuyết tôi đã chuẩn bị ra chỉ đúng chỗ HS cần học lại —
> đây là **mức B**. **Không ra ngoài bất kì cái nào. Đáp án thì phải lấy ngay đáp án
> Python tôi đã chuẩn bị theo đề. Không được để AI tự tính toán.**"

Câu cuối là ràng buộc cứng của toàn bộ tính năng. Mọi thiết kế dưới đây đều phục vụ nó.

## 2. Vì sao phải khoá chặt đến thế

Mô hình ngôn ngữ **tính số học rất hay sai**, và sai một cách tự tin. Nếu để AI tự giải
lại câu hỏi rồi giảng cho học sinh, sẽ có ngày nó giảng ra một đáp án khác với đáp án
in trong đề — học sinh tin AI, chép vào bài, và cô là người phải sửa hậu quả.

Ngân hàng đề này có một lợi thế mà các web đề khác không có: **mọi câu đều do Python
sinh ra, nên đáp án và lời giải đã có sẵn, chính xác tuyệt đối, từ trước khi AI được
gọi.** Việc của AI vì thế không phải là *giải*, mà là *diễn đạt lại cho dễ hiểu*.

## 3. Ba lớp khoá

Ba lớp độc lập nhau. Hỏng một lớp thì hai lớp còn lại vẫn đứng.

| Lớp | Đặt ở đâu | Làm gì |
|---|---|---|
| **1. Câu lệnh** | `gia_su_service.LENH_HE_THONG` | Đưa sẵn đề bài + đáp án + lời giải chuẩn vào câu lệnh. Cấm tính toán, cấm ra số khác lời giải mẫu, cấm nói sang câu khác. Có sẵn một câu từ chối để mô hình dùng khi bị hỏi ra ngoài. |
| **2. Hiển thị** | `lam_bai.html` → `veLoiGiaiChuan()` | API **luôn** trả về `dap_an_python` + `loi_giai_python` nguyên văn, và giao diện vẽ chúng **ngay cạnh** câu trả lời của AI. Học sinh nhìn hai khối là thấy ngay nếu lệch. |
| **3. Nhật kí** | bảng `gia_su_hoi_dap`, trang `/gv/gia-su` | Mỗi lượt hỏi lưu cả câu trả lời của AI lẫn đáp án Python đã đưa vào lệnh. Cô đọc lại, đối chiếu hai cột. |

Và một quy tắc bao trùm, quan trọng hơn cả ba lớp trên:

> **Không có lời giải chuẩn thì KHÔNG gọi mô hình.**

Nếu thiếu dữ liệu (đề quá cũ, câu chưa có lời giải mẫu), hệ thống **báo lỗi và dừng**,
chứ không gọi AI — vì lúc đó AI bắt buộc phải tự nghĩ ra, đúng cái bị cấm.
Bài kiểm tra `test_hoi_khong_goi_mo_hinh_khi_thieu_ngu_canh` canh đúng điểm này.

## 4. Luồng dữ liệu

```
Học sinh nộp bài → trang kết quả
        │
        │ bấm "💬 Hỏi thầy/cô AI về câu này" ở câu số N
        ▼
POST /api/giasu/hoi  {de_id, so_thu_tu: N, cau_hoi, lich_su}
        │  user_id lấy từ COOKIE (không lấy từ body)
        ▼
gia_su_service.hoi()
        │
        ├─1─ lay_ngu_canh_cau()  ──► file dapan_json (Python sinh)
        │        │                        └─ hết hạn ──► exam_history.chi_tiet_bai_lam
        │        └─ không có ──► GiaSuError, DỪNG, không gọi AI
        │
        ├─2─ lay_luot()          ──► hết lượt ──► GiaSuError, DỪNG, không gọi AI
        │
        ├─3─ dung_lenh()         ──► ghép đề bài + đáp án + lời giải vào LENH_HE_THONG
        │
        ├─4─ n8n webhook         ──► n8n CHỈ gọi mô hình, không tự lấy dữ liệu ở đâu
        │
        ├─5─ tru_luot()          ──► chỉ trừ khi đã có câu trả lời
        │
        └─6─ ghi_nhat_ki()       ──► gia_su_hoi_dap
                 │
                 ▼
        trả về {tra_loi, dap_an_python, loi_giai_python, luot}
                 │
                 ▼
        Giao diện vẽ câu trả lời AI  +  khối "Lời giải chuẩn của thầy/cô"
```

## 5. Tệp đã thêm / sửa

| Tệp | Việc |
|---|---|
| `sql/24_gia_su.sql` | **mới** — 2 bảng `gia_su_luot`, `gia_su_hoi_dap` + bật RLS |
| `app/services/gia_su_service.py` | **mới** — toàn bộ nghiệp vụ, 3 lớp khoá |
| `app/routers/gia_su.py` | **mới** — `POST /api/giasu/hoi`, `GET /api/giasu/luot` |
| `app/templates/teacher/gia_su.html` | **mới** — trang nhật kí cho cô |
| `tests/test_gia_su.py` | **mới** — 27 bài kiểm tra |
| `app/core/config.py` | thêm `N8N_WEBHOOK_GIA_SU`, `GIA_SU_LUOT_MOI_NGAY`, `GIA_SU_DO_DAI_CAU_HOI` |
| `app/main.py` | đăng kí router `gia_su` |
| `app/routers/teacher.py` | thêm `GET /gv/gia-su`, `POST /gv/gia-su/luot` |
| `app/templates/teacher/_base_gv.html` | thêm mục "Gia sư AI" vào thanh điều hướng |
| `app/templates/chat/lam_bai.html` | nút hỏi + khung hội thoại + khối lời giải chuẩn |

## 6. Cách bật (3 bước)

### Bước 1 — Chạy SQL

Supabase → **SQL Editor** → dán toàn bộ `sql/24_gia_su.sql` → **Run**.
Chưa chạy bước này thì học sinh vẫn hỏi được (không vỡ trang), nhưng log VPS sẽ in
`LOI DOC gia_su_luot` và hạn mức lượt không đếm được.

### Bước 2 — Thêm webhook `gia-su` vào workflow `NganHangDe`

**Không tạo workflow mới.** Thêm một nhánh thứ tư vào chính workflow `NganHangDe`
đang có, đúng kiểu `doc-phieu-tra-loi` và `cham-tu-luan` — ba nút, đi thẳng, không
qua Switch:

```
[Webhook: gia-su]  →  [AI node: CHV_GiaSu]  →  [Respond to Webhook]
```

**Node 1 — Webhook**
- HTTP Method: `POST` · Path: `gia-su`
- Respond: **Using 'Respond to Webhook' Node**

**Node 2 — AI Agent**, đổi tên thành `CHV_GiaSu`
- Source for Prompt: **Define below**
- Prompt (User Message): `{{ $json.body.cau_hoi }}`
- Options → Add Option → **System Message**: `{{ $json.body.lenh_he_thong }}`
- Chat Model: nối `OpenRouter Chat Model` (dùng lại credential có sẵn)
- **Không gắn Memory, không gắn Tool.** Mỗi câu hỏi là một lượt độc lập; lịch sử
  hội thoại đã do Python gửi sang trong `lich_su`, và câu lệnh khoá chặt phải là
  thứ duy nhất mô hình đọc.

**Node 3 — Respond to Webhook**
- Respond With: **First Incoming Item**
- Không cần gõ JSON tay: AI Agent trả về khoá `output`, mà `_goi_mo_hinh()` đã
  nhận được (`tra_loi` / `output` / `text` / `message` / `answer`, kể cả khi bị
  bọc trong một mảng).

Bấm **Save**. Workflow đang *Published* nên node mới phải lưu lại thì Production
URL mới sống. URL lấy ở node Webhook, tab **Production URL**.

### Vì sao KHÔNG cho gia sư đi qua `CHV_Fun` → Switch

Switch nằm **sau** `CHV_Fun`, nên mọi thứ qua Switch đều đã bị `CHV_Fun` đọc và đoán ý
định trước. Với gia sư, việc đó hỏng cả ba mặt:

| | Hậu quả |
|---|---|
| **Tốn gấp đôi lượt gọi mô hình** | `CHV_Fun` chạy để phân loại, rồi node sau mới trả lời. Hai lượt cho một câu hỏi, trong khi đang dùng tài khoản miễn phí. |
| **Phá lớp khoá 1** | `CHV_Fun` có system prompt riêng, sẽ trộn với `lenh_he_thong` do Python dựng. Các câu "KHÔNG TỰ TÍNH TOÁN", "cấm ra số khác lời giải mẫu" không còn là lệnh duy nhất nữa. |
| **Không có gì để đoán** | Switch chia theo ý định `CHV_Fun` suy ra. Python đã biết chắc học sinh hỏi câu số mấy, đề nào — không cần đoán. |

> ⚠️ **Không thêm bất kì nút nào để n8n tự đi tra cứu dữ liệu.** Toàn bộ đề bài, đáp án
> và lời giải đã nằm sẵn trong `lenh_he_thong`. Nhánh này chỉ làm đúng một việc: gọi mô
> hình. Thêm nút tra cứu — hay nối vào `CHV_Fun` — đều là phá lớp khoá 1.

Dùng tài khoản mô hình miễn phí được — hạn mức lượt ở bước 3 chính là để chặn trần.

> Sơ đồ đầy đủ cả 4 webhook của workflow `NganHangDe`, ghi rõ từng node làm gì: **`docs/06_N8N_WORKFLOW.md`**, mục *Cập nhật 2026-09-16*.

### Bước 3 — Đặt biến môi trường trên VPS

```bash
ssh root@103.82.27.226
nano /root/NganHangDe/.env
```

Thêm 2 dòng (dán URL thật của webhook vừa tạo ở bước 2):

```
N8N_WEBHOOK_GIA_SU=https://fqrpl.n8npanel.com/webhook/giasu
GIA_SU_LUOT_MOI_NGAY=20
```

Rồi:

```bash
systemctl restart nganhangde
```

**Chưa làm bước 2–3 vẫn dùng được**: khi `N8N_WEBHOOK_GIA_SU` để trống, nút "Hỏi
thầy/cô AI" chạy ở **chế độ không AI** — bấm vào là hiện lời giải chuẩn của cô. Không
bao giờ vỡ trang học sinh.

## 7. Hạn mức lượt hỏi

- Mặc định **20 lượt/em/ngày** (`GIA_SU_LUOT_MOI_NGAY` trong `.env`).
- Ngày chốt theo **giờ Việt Nam**, không theo UTC — nếu theo UTC thì từ 7h sáng
  đã bị tính sang ngày hôm sau và học sinh mất lượt giữa buổi học.
- **Chỉ trừ lượt khi đã có câu trả lời.** Mất mạng, n8n hỏng, hết dữ liệu — đều
  không trừ.
- Cô nâng riêng cho một em ở `/gv/gia-su`, cột cuối. Giá trị đó ghi vào
  `gia_su_luot.gioi_han` và **chỉ có hiệu lực trong ngày hôm đó**.

## 7b. Hai đường vào gia sư (cập nhật 17/09/2026, v2.61)

| Đường | Ở đâu | Dùng khi |
|---|---|---|
| Nút **"💬 Hỏi thầy/cô AI về câu này"** | trang kết quả sau khi nộp bài, dưới mỗi câu | đang xem điểm, thấy câu nào sai thì hỏi ngay |
| Nút **"💬 Hỏi lại đề cũ"** | cố định dưới ô nhập ở Chat AI | đã rời trang kết quả, quay lại chat muốn hỏi |

### Vì sao làm bằng NÚT, không để AI đoán

Học sinh vừa tạo đề xong thì trong đầu đã có ngữ cảnh rồi — gõ "giải bài 3"
là đủ với các em. Bắt mô hình đoán "bài 3 của đề nào" là **sai từ gốc**:
nó không có cách nào biết, và đoán sai thì đi giải một bài tưởng tượng.

Bấm nút thì máy chủ **biết chắc** `de_id` và `so_thu_tu` — không phải đoán,
không tốn một lượt gọi mô hình nào để phân loại. Đúng nguyên tắc
**"Ưu tiên Code hơn AI"** (docs/00).

### Luồng

```
Bấm "💬 Hỏi lại đề cũ"
   └─► GET /api/giasu/de-gan-nhat?conversation_id=...
          └─► history_service.lay_de_gan_nhat()  →  đọc dapan_json
              chia 4 phần theo loai_cau (MC/TF/SA/TL)
              mỗi câu kèm: da_lam, co_loi_giai, hoi_duoc
   └─► vẽ PHẦN I/II/III/IV, mỗi phần một hàng nút số câu
          └─► bấm số câu ─► POST /api/giasu/hoi (như cũ)
```

### PHẢI NỘP BÀI RỒI MỚI HỎI ĐƯỢC

Câu chưa nộp bài thì nút **mờ, không bấm được**. Lý do (cô Lan chốt): giảng
lại luôn kèm đáp án chuẩn, nên nếu cho hỏi tự do thì học sinh bấm lướt cả đề
để lấy lời giải mà không chịu nghĩ.

**Chặn ở HAI tầng**, không chỉ làm mờ nút:

| Tầng | Ở đâu |
|---|---|
| Giao diện | `chat.html::veBangHoiDeCu()` — `hoi_duoc = false` thì `disabled` |
| Máy chủ | `gia_su_service.hoi()` — gọi `_cac_cau_da_lam()`, chưa làm thì `GiaSuError` |

Chặn ở giao diện thôi là vô nghĩa: ai cũng gọi thẳng API được.
`tests/test_gia_su.py::test_chua_nop_bai_thi_khong_hoi_duoc_va_khong_goi_mo_hinh`
canh đúng điểm này.

Câu **đã làm nhưng không có lời giải mẫu** (ví dụ câu tự luận) cũng mờ —
không có gì chuẩn để giảng thì không giảng.

---

## 7c. Gõ hỏi bài trong chat (18/09/2026, v2.62)

Học sinh vừa nộp bài xong, gõ **"tôi không hiểu bài 1"** ngay trong chat.
`CHV_Fun` không có cách nào biết hội thoại này đã có đề — nó chỉ đọc mỗi câu
chữ — nên từ chối và bảo em ấy đi *tạo đề rồi làm bài*, trong khi em ấy vừa
làm xong. Vô lí với người dùng, và là lỗi của ta chứ không phải của prompt.

Máy chủ thì **biết chắc**: `conversation_id` → đề gần nhất → đã nộp bài chưa.

```
POST /chat  "tôi không hiểu bài 1"
   │
   ├─ gia_su_service.la_y_dinh_hoi_bai(message)   ── regex, không tốn lượt AI
   │     └─ False ──────────────────────────────────► đi tiếp sang n8n như cũ
   │
   ├─ gia_su_service.co_de_da_nop_bai(user, conv)
   │     └─ False ──────────────────────────────────► đi tiếp sang n8n như cũ
   │
   └─ cả hai True ──► trả {"type": "mo_bang_gia_su"}, KHÔNG gọi n8n
                       └─ Frontend mở bảng PHẦN I–IV để học sinh bấm câu
```

### CỐ Ý KHÔNG ĐOÁN SỐ CÂU

Cô Lan chốt. "Bài 1" có thể là câu 1 của đề, cũng có thể là bài 1 trong sách.
Đoán sai thì **giảng nhầm câu** — tệ hơn nhiều so với bắt học sinh bấm thêm
một nút. Nhận ra ý định thì mở bảng chọn câu, để chính em ấy chỉ đúng câu.

### Hai điều kiện, phải đủ cả hai

Chỉ một điều kiện là chặn nhầm. `la_y_dinh_hoi_bai` loại sẵn "hướng dẫn **sử
dụng**", "cách **tạo đề**", "**tính năng**" — những câu đó thuộc Rule 5 (help)
của `CHV_Fun`, không được cướp. Và nếu hội thoại chưa có đề nào thì vẫn để
`CHV_Fun` trả lời như cũ — lúc đó từ chối mới đúng.

`co_de_da_nop_bai` **nuốt mọi lỗi**: Supabase hỏng thì trả `False` để đi
đường cũ, không bao giờ chặn nhầm vì một lỗi đọc dữ liệu.

---

## 8. Mức B — tài liệu lí thuyết đã có, bảng ánh xạ đã xong (19/09/2026)

Cô Lan đã đưa **87 tệp `.tex` lí thuyết** vào `data/ly_thuyet/` (3,1 MB).

### Vì sao phải có bảng ánh xạ viết tay

Khớp tự động theo tên bài chỉ được **11/28** tệp lớp 10. Không phải tệp đặt
sai — mà **cách chia bài của tài liệu khác cách chia của chương trình**, và
quan hệ là **nhiều–nhiều**:

| Bài trong chương trình | Tệp lí thuyết |
|---|---|
| `L10_C1_B2` Tập hợp và các phép toán trên tập hợp | `0D1-CD2.tex` + `0D1-CD3.tex` |
| `L10_C4_B8` Các phép toán trên vectơ | `0H4-B2.tex` + `0H4-B3.tex` + `0H4-B5.tex` |
| `L10_C7_B18` Đường thẳng trong mặt phẳng toạ độ | `0H7-B1.tex` + `0H7-B2.tex` |

Và vài chỗ chỉ khác chữ: *NHỊ THỨC NIU-TƠN* ↔ *Nhị thức Newton*;
*DẤU TAM THỨC BẬC HAI* ↔ *Dấu **của** tam thức bậc hai*.

Không có cách nào tự động hoá việc này cho đúng. Nên: **`data/ly_thuyet/anh_xa.json`**
— viết một lần, canh bằng `tests/test_anh_xa_ly_thuyet.py` (7 bài).

### Phủ sóng

| Khối | Tệp lí thuyết | Curriculum | Ánh xạ |
|---|---|---|---|
| 10 | 28 | 23 bài | **đủ cả 23 bài** |
| 11 | 33 | **rỗng** | chưa làm được |
| 12 | 26 | **rỗng** | chưa làm được |

`data/curriculum/toan11/` và `toan12/` chưa có tệp nào, nên 59 tệp lí thuyết
lớp 11–12 **chưa gắn vào đâu được** — không phải tệp sai, mà chưa có câu hỏi
nào để gắn. Làm ngân hàng 11/12 xong thì bổ sung vào `anh_xa.json` là dùng ngay.

### Cắt phần nào của tệp — đã đo, không đoán

Mỗi tệp gồm: `\section{TÊN BÀI}` → `\subsection{LÝ THUYẾT CẦN NHỚ}` (hoặc
*TÓM TẮT LÝ THUYẾT* / *KIẾN THỨC CẦN NHỚ*) → *PHÂN LOẠI VÀ PHƯƠNG PHÁP GIẢI
TOÁN* → *BÀI TẬP TỰ LUYỆN*.

Đo thật trên 23 bài lớp 10:

| | Ký tự | ≈ token |
|---|---|---|
| Cả tệp (trung bình) | 34 079 | ~8 500 |
| **Chỉ mục lí thuyết** (trung bình) | **4 534** | **~1 130** |
| Chỉ lí thuyết, dài nhất (`L10_C4_B8`) | 14 576 | ~3 600 |
| Chỉ lí thuyết, ngắn nhất (`L10_C2_B4`) | 914 | ~230 |

→ **Nạp cả tệp là không được** (8 500 token mỗi lượt, tài khoản miễn phí chịu
không nổi). **Cắt lấy đúng mục lí thuyết thì được** — trung bình ~1 130 token,
và chỉ nạp khi học sinh bấm *"Em vẫn chưa hiểu"*, không nạp ở Mức A.

Riêng `L10_C4_B8` (gộp 3 tệp) vượt trần → cắt tiếp theo `\subsubsection`,
giữ các tiểu mục khớp từ khoá của câu hỏi.

## 8b. Mức B — phần còn lại chưa làm

Mức B là bước tiếp theo: học sinh đọc lời giảng mà **vẫn** chưa hiểu → chỉ đúng chỗ
trong tài liệu lí thuyết `.tex` của cô để em học lại.

Hướng đã chốt: **tra theo ID trước, vectơ tính sau.**

Mỗi câu trong ngân hàng đã mang sẵn ID dạng `L10_C1_B2_VD01_MC_v1`, tức là đã biết
chính xác **lớp – chương – bài**. Nếu tài liệu lí thuyết được đánh dấu theo cùng
`L{lớp}_C{chương}_B{bài}`, thì việc "chỉ đúng chỗ cần học lại" chỉ là một phép tra bảng
— không cần nhúng vectơ, không cần cơ sở dữ liệu vectơ, không tốn thêm một lượt gọi mô
hình nào (xem `docs/20_TIM_KIEM_VECTO.md`: kết luận là **chưa cần làm vectơ**).

Việc còn thiếu để làm Mức B: **một tệp `.tex` mẫu của tài liệu lí thuyết** để xem cấu
trúc hiện tại (đánh mục bằng `\section`? `\subsection`? có nhãn `\label` chưa?). Có tệp
mẫu rồi mới chốt được cách đánh dấu sao cho cô ít phải sửa tay nhất.

## 9. Những chỗ dễ sai về sau

| Chỗ | Vì sao dễ sai |
|---|---|
| Sửa `LENH_HE_THONG` | Mỗi câu trong đó là một lớp khoá. Bỏ câu "KHÔNG TỰ TÍNH TOÁN" là mở cửa cho AI giải lại. `tests/test_gia_su.py` canh từng câu một — test đỏ nghĩa là vừa gỡ mất một lớp khoá. |
| Bỏ khối "Lời giải chuẩn" ở giao diện | Đó là lớp khoá 2, không phải trang trí. |
| Đổi `def` thành `async def` ở `app/routers/gia_su.py` | Bên trong gọi `httpx` đồng bộ tới 60 giây — sẽ chặn event loop y hệt lỗi `/gv/ra-de` (v2.56). |
| Nhận `user_id` từ body | Ai cũng tiêu hết lượt của người khác. Luôn lấy từ cookie. |
| Nối gia sư vào `CHV_Fun` → Switch | Tốn gấp đôi lượt gọi mô hình, và system prompt của `CHV_Fun` trộn với `lenh_he_thong` → phá lớp khoá 1. Gia sư phải là webhook riêng, đi thẳng (mục 6, bước 2). |
| Thêm nút tra cứu vào nhánh n8n | Phá lớp khoá 1 (mục 6, bước 2). |
| Dọn `data/temp/*_dapan.json` sớm hơn | Đó là nguồn lời giải chuẩn số 1. Dọn sớm thì Mức A phải lùi về `exam_history` (không còn đề bài gốc). |
