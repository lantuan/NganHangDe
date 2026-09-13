# BẢO MẬT: KHOÁ SUPABASE VÀ ROW LEVEL SECURITY

Version: 1.0 — 2026-09-13 (Version 2.47)

Trạng thái

🟢 Chuẩn chính thức

---

# 1. Lỗ hổng đã phát hiện

Phát hiện ngày 13/09/2026 khi rà lại trigger `handle_new_user`. Hai điểm
riêng lẻ, ghép lại thành một lỗ hổng nghiêm trọng.

**Điểm 1 — máy chủ dùng đúng cái khoá nó đưa cho trình duyệt.**
`app/core/supabase.py` tạo client bằng `SUPABASE_KEY`, mà chính biến đó
được nhét vào trang đăng nhập/đăng ký dưới tên `supabase_anon_key`
(`app/routers/auth.py`). Ai bấm "Xem mã nguồn trang" cũng lấy được.

**Điểm 2 — mọi bảng đều tắt Row Level Security.** Bảng tắt RLS thì bất kỳ
ai cầm khoá anon đều đọc và ghi được mọi dòng qua PostgREST.

**Hậu quả:**

| Bảng | Ai đó có thể làm gì |
|---|---|
| `profiles` | Tự đặt `vai_tro = 'giao_vien'` cho chính mình → đi vòng qua mã mời, vào được toàn bộ `/gv/*` |
| `classroom_oauth`, `classroom_oauth_gv` | **Đọc `refresh_token` Google Classroom của giáo viên** — chìa khoá vào tài khoản Google trong phạm vi quyền Classroom + Drive đã cấp |
| `exam_history` | Đọc điểm của mọi học sinh, sửa điểm của chính mình |
| `de_da_sinh`, `file_de` | Lấy đường dẫn file đáp án của mọi đề |
| `classroom_roster` | Đọc email toàn bộ học sinh |

Lỗ hổng này có từ Version 2.4 (khi tắt RLS để cho nhanh), nhưng chỉ thành
vấn đề rõ ràng khi có phân quyền giáo viên (Version 2.46).

---

# 2. Cách vá

## 2.1. Tách hai khoá

| Client | Khoá | Dùng cho |
|---|---|---|
| `supabase` | anon | **Chỉ xác thực**: đăng nhập, đăng ký, đọc user từ token, đổi mật khẩu |
| `supabase_admin` | service_role | **Mọi thao tác đọc/ghi bảng** |

Khoá `service_role` bỏ qua RLS, nên **tuyệt đối không được** gửi ra trình
duyệt, không commit vào git, không ghi vào tài liệu.

Các tệp đã đổi sang `supabase_admin`:

- `app/services/profile_service.py`
- `app/services/history_service.py`
- `app/services/classroom_service.py`
- `app/services/supabase_service.py` (chỉ hai hàm đọc/ghi `profiles`;
  phần `sign_in`/`sign_up`/`get_user` vẫn dùng khoá anon)

`app/routers/auth.py` và `app/core/deps.py` giữ nguyên khoá anon vì chỉ
gọi `supabase.auth.*`.

## 2.2. Bật RLS, không tạo policy nào

Chạy `sql/22_bat_rls.sql`.

Bật RLS mà không tạo policy = khoá anon không đọc/ghi được bảng nào.
Không cần viết policy chi tiết cho từng bảng vì **trình duyệt không truy
vấn bảng nào cả** — đã kiểm tra toàn bộ `app/templates/`, không có một
lệnh `.from()` hay `.rpc()` nào; supabase-js ở phía trình duyệt chỉ dùng
để xác thực.

Đây cũng là lý do cách vá này đơn giản và ít rủi ro: toàn bộ nghiệp vụ đã
đi qua FastAPI từ đầu, đúng quy tắc trong docs/13 (*"Mọi dữ liệu đều đi
qua FastAPI"*). Quy tắc kiến trúc đặt ra từ sớm giờ trả công.

---

# 3. THỨ TỰ THỰC HIỆN — làm sai thứ tự là web chết

1. **Lấy khoá service_role**: Supabase → Project Settings → API Keys →
   `service_role` → Copy.
2. **Thêm vào `.env` trên VPS** (không qua git):
   `SUPABASE_SERVICE_KEY=<khoá vừa copy>`
3. **Deploy code mới** (`git pull` + `systemctl restart nganhangde`).
4. **Thử lại web**: đăng nhập, tạo một đề, mở `/gv/thong-ke`. Phải chạy
   bình thường. Nếu trong log thấy dòng `CANH BAO BAO MAT: chua co
   SUPABASE_SERVICE_KEY` nghĩa là bước 2 chưa vào — dừng lại, sửa xong
   mới đi tiếp.
5. **Chạy `sql/22_bat_rls.sql`** trong Supabase SQL Editor.
6. **Thử lại web một lần nữa** y như bước 4.
7. **Đổi refresh_token Google Classroom** (xem mục 4).

Chạy bước 5 trước bước 2–3 thì mọi truy vấn trả về rỗng: đăng nhập được
nhưng không thấy lịch sử, không tạo được đề, thống kê trống. Cách chữa:
làm bước 2–3 rồi khởi động lại, không phải tắt RLS đi.

---

# 4. Đổi refresh_token Classroom sau khi vá

Khoá anon đã công khai suốt thời gian qua, nên phải coi như
`refresh_token` Google Classroom **đã lộ**. Vá xong phải đổi:

1. Vào <https://myaccount.google.com/connections> (Tài khoản Google →
   Bảo mật → Ứng dụng bên thứ ba).
2. Tìm ứng dụng "NganHangDe Classroom Sync", chọn **Xoá quyền truy cập**.
   Thao tác này làm refresh_token cũ hết hiệu lực ngay.
3. Vào lại `https://nganhangdechv.tech/gv/classroom/connect` để cấp quyền
   lại và nhận token mới — token mới nằm trong bảng đã khoá RLS.

Không làm bước này thì dù đã vá, token cũ vẫn dùng được nếu ai đó đã lấy.

---

# 5. Quy tắc từ nay

- **Không bao giờ** dùng chung một khoá cho máy chủ và trình duyệt.
- Khoá `service_role` chỉ nằm trong `.env` trên VPS. Không commit, không
  dán vào chat, không đưa vào tài liệu.
- Bảng mới tạo ra: **bật RLS ngay khi tạo**, đừng để "lát nữa làm".
- Trình duyệt chỉ được dùng supabase-js cho xác thực. Mọi truy vấn dữ
  liệu đi qua FastAPI — đúng quy tắc docs/13.
- Nếu sau này thật sự cần cho trình duyệt đọc thẳng một bảng, phải viết
  policy cụ thể cho bảng đó, không được tắt RLS.
