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

### Bước 2 — Tạo webhook n8n

Tạo một workflow n8n mới, đặt tên `CHV_GiaSu`:

1. **Webhook** (POST) — bật *Respond: Using Respond to Webhook*.
2. **AI node / HTTP Request** gọi mô hình. Nạp:
   - phần *system* = `{{ $json.body.lenh_he_thong }}`
   - phần *user* = `{{ $json.body.cau_hoi }}`
   - lịch sử (nếu muốn) = `{{ $json.body.lich_su }}`
3. **Respond to Webhook** trả JSON `{ "tra_loi": "<nội dung>" }`.

> ⚠️ **Không thêm bất kì nút nào để n8n tự đi tra cứu dữ liệu.** Toàn bộ đề bài, đáp án
> và lời giải đã nằm sẵn trong `lenh_he_thong` do Python dựng. n8n chỉ làm đúng một
> việc: gọi mô hình. Thêm nút tra cứu là phá lớp khoá 1.

Dùng tài khoản mô hình miễn phí được — hạn mức lượt ở bước 3 chính là để chặn trần.

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

## 8. Mức B — chưa làm

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
| Thêm nút tra cứu vào workflow n8n | Phá lớp khoá 1 (mục 6, bước 2). |
| Dọn `data/temp/*_dapan.json` sớm hơn | Đó là nguồn lời giải chuẩn số 1. Dọn sớm thì Mức A phải lùi về `exam_history` (không còn đề bài gốc). |
