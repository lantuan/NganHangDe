# TÀI KHOẢN GIÁO VIÊN

Version: 1.0 — 2026-09-13

Trạng thái

🟢 ĐÃ TRIỂN KHAI (Version 2.46 — 2026-09-13). Tài liệu này giữ nguyên phần
thiết kế để tra cứu; phần "đã làm / chưa làm" ở cuối file.

---

# 1. Hiện trạng (đã kiểm tra trong mã nguồn ngày 13/09/2026)

| Nội dung | Hiện trạng | Tệp |
|---|---|---|
| Đăng ký | Chỉ có luồng học sinh (`/register/student`). `/register/teacher` chuyển sang `/teacher-coming-soon` | `app/routers/auth.py` |
| Phân quyền | KHÔNG có. Các route `/gv/*` chỉ kiểm tra ĐÃ ĐĂNG NHẬP (`get_current_user`), không kiểm tra vai trò | `app/routers/classroom.py` |
| Kết nối Classroom | Lưu vào bảng `classroom_oauth` **chỉ một dòng, id = 1** | `classroom_service.luu_refresh_token()` |
| Thống kê | `/gv/thong-ke` hiện thống kê theo khối/lớp, không lọc theo giáo viên | `app/routers/classroom.py` |
| `app/routers/teacher.py` | Tệp rỗng | — |

Hai hệ quả phải sửa, theo thứ tự nghiêm trọng:

1. **Bất kỳ học sinh nào biết đường dẫn `/gv/thong-ke` đều xem được điểm cả
   lớp.** Đây là lỗi lộ dữ liệu, phải sửa trước tiên.
2. **Hệ thống hiện chỉ phục vụ được ĐÚNG MỘT giáo viên.** Giáo viên thứ hai
   bấm kết nối Classroom sẽ GHI ĐÈ refresh_token của giáo viên thứ nhất, và
   từ đó bài của học sinh sẽ đăng nhầm sang Classroom của người kia.

---

# 2. Nguyên tắc thiết kế

Giữ đúng các nguyên tắc đã có trong docs/00, 01, 13:

- Mọi dữ liệu đi qua FastAPI. Frontend không gọi thẳng Supabase.
- Phân quyền kiểm tra ở TẦNG SERVER, không chỉ ẩn nút trên giao diện.
- Không dùng AI ở bất kỳ bước nào của phần này.
- Giáo viên chỉ thấy dữ liệu của lớp mình dạy.

---

# 3. Kế hoạch thi công — 5 bước

Làm đúng thứ tự. Mỗi bước chạy được và kiểm tra được trước khi sang bước sau.

## Bước 1 — Thêm cột vai trò và chặn cửa (ưu tiên cao nhất)

**Cơ sở dữ liệu.** Chạy trong Supabase > SQL Editor:

```sql
alter table profiles
  add column if not exists vai_tro text not null default 'hoc_sinh'
  check (vai_tro in ('hoc_sinh', 'giao_vien', 'quan_tri'));

-- Nâng tài khoản của mình lên giáo viên
update profiles set vai_tro = 'giao_vien' where email = 'lantuan2605@gmail.com';
```

**Mã nguồn.** Thêm vào `app/core/deps.py`:

```python
def lay_vai_tro(request) -> str:
    """Doc vai_tro tu bang profiles. Mac dinh 'hoc_sinh' neu khong doc duoc."""
    user = get_current_user(request)
    if user is None:
        return "khach"
    ...  # truy van profiles theo user.id, tra ve vai_tro


def yeu_cau_giao_vien(request):
    """Dung o dau moi route /gv/*. Tra ve RedirectResponse neu khong du quyen."""
    vai_tro = lay_vai_tro(request)
    if vai_tro == "khach":
        return RedirectResponse("/login", status_code=303)
    if vai_tro not in ("giao_vien", "quan_tri"):
        raise HTTPException(status_code=403, detail="Chuc nang danh cho giao vien.")
    return None
```

Rồi thêm hai dòng đầu MỌI route `/gv/*` trong `app/routers/classroom.py`:

```python
chan = yeu_cau_giao_vien(request)
if chan is not None:
    return chan
```

**Kiểm tra:** đăng nhập bằng một tài khoản học sinh, mở `/gv/thong-ke`, phải
nhận 403. Đây là bước quan trọng nhất của cả tài liệu này.

## Bước 2 — Đăng ký tài khoản giáo viên

- Bỏ trang `/teacher-coming-soon`, làm thật `/register/teacher`.
- Biểu mẫu: họ tên, email, mật khẩu, tên trường, tổ chuyên môn, **mã mời**.
- **Mã mời** (một chuỗi đặt trong `.env`, ví dụ `MA_MOI_GIAO_VIEN`) là cách
  đơn giản nhất để học sinh không tự đăng ký thành giáo viên. Không cần dựng
  luồng duyệt tài khoản phức tạp.
- Sau khi tạo tài khoản, đặt `vai_tro = 'giao_vien'`.

Nhớ cập nhật trigger `handle_new_user` (xem docs/12 và Version 2.15) để nó
nhận thêm khóa `vai_tro` từ metadata lúc đăng ký.

## Bước 3 — Mỗi giáo viên một kết nối Classroom riêng

Đây là bước sửa lỗi ghi đè ở Mục 1.

```sql
-- Bo bang classroom_oauth 1 dong, chuyen sang moi giao vien 1 dong
create table classroom_oauth_gv (
  user_id       uuid primary key references profiles(id) on delete cascade,
  refresh_token text not null,
  email_google  text,
  updated_at    timestamptz default now()
);

-- Chuyen du lieu cu sang (thay <user_id_cua_chi> bang id that)
insert into classroom_oauth_gv (user_id, refresh_token)
select '<user_id_cua_chi>', refresh_token from classroom_oauth where id = 1;
```

Sửa `classroom_service.py`:

- `luu_refresh_token(user_id, refresh_token)` — thêm tham số `user_id`.
- `lay_refresh_token(user_id)` — thêm tham số `user_id`.
- Mọi hàm gọi API Classroom nhận thêm `user_id` để lấy đúng token.
- Khi học sinh nộp bài: tra giáo viên phụ trách lớp của học sinh đó, lấy token
  của chính giáo viên ấy rồi mới đăng bài.

Cần thêm một bảng nối lớp với giáo viên:

```sql
create table lop_giao_vien (
  khoi     text not null,
  lop      text not null,
  user_id  uuid not null references profiles(id) on delete cascade,
  primary key (khoi, lop)
);
```

**Lưu ý bảo mật:** `refresh_token` là chìa khóa vào tài khoản Google của giáo
viên. Bảng này phải bật Row Level Security trong Supabase và chỉ cho đọc bằng
service key ở phía máy chủ, tuyệt đối không để lộ ra Frontend.

## Bước 4 — Khu làm việc của giáo viên

Dựng `app/routers/teacher.py` (đang rỗng) với các đường dẫn:

| Đường dẫn | Nội dung |
|---|---|
| `GET /gv` | Trang chính: các lớp đang dạy, số đề đã giao, lối tắt sang các mục dưới |
| `GET /gv/ra-de` | Biểu mẫu ra đề đầy đủ cho giáo viên: chọn lớp, phạm vi, loại bài, **số mã đề**, và tuỳ chọn ma trận chi tiết |
| `GET /gv/de-da-tao` | Danh sách đề đã tạo, tải lại PDF đề / lời giải / **tệp `.tex`** |
| `GET /gv/lop` | Danh sách lớp và học sinh, mã lớp Classroom |
| `GET /gv/thong-ke` | Giữ như hiện tại, thêm lọc theo lớp mà giáo viên đó dạy |

Phần ra đề dùng lại nguyên `generate_exam_pdf_auto` đang có, chỉ khác ở chỗ
truyền `role="teacher"` và `socau_ma_de` theo số giáo viên nhập.

## Bước 5 — Tải mã nguồn LaTeX của đề

Thêm `GET /api/exam/tai-tex/{de_id}`:

- Chỉ cho tài khoản có `vai_tro` là `giao_vien` hoặc `quan_tri`.
- Trả về tệp `.tex` của đề đó (hệ thống đã lưu sẵn, xem Version 2.4).
- Nếu tệp đã bị dọn (quá 1 ngày) thì sinh lại từ danh sách mã câu hỏi đã lưu.
- Nên trả kèm cả tệp `.tex` của lời giải trong một tệp nén.

---

# 4. Thứ tự làm và thời gian ước lượng

| Bước | Nội dung | Ước lượng | Ghi chú |
|---|---|---|---|
| 1 | Vai trò + chặn cửa `/gv/*` | 1 buổi | **Làm ngay**, đang là lỗ hổng dữ liệu |
| 2 | Đăng ký giáo viên có mã mời | 1 buổi | |
| 3 | Tách kết nối Classroom theo từng giáo viên | 1--2 buổi | Phải chuyển dữ liệu cũ, làm cẩn thận |
| 4 | Khu làm việc giáo viên | 2--3 buổi | Phần nhiều mã đề nằm ở đây |
| 5 | Tải tệp `.tex` | nửa buổi | |

Bước 1 nên làm trước cả việc sửa lỗi nhiều mã đề, vì đó là vấn đề lộ dữ liệu
chứ không phải vấn đề tiện dụng.

---

# 5. Những chỗ dễ sai

- **Chỉ ẩn nút trên giao diện mà không chặn ở server.** Người dùng gõ thẳng
  đường dẫn là vào được. Luôn kiểm tra ở route.
- **Quên `vai_tro` cho tài khoản đăng ký trước khi thêm cột.** Cột có
  `default 'hoc_sinh'` nên các tài khoản cũ đều thành học sinh — đúng ý, nhưng
  nhớ nâng tài khoản giáo viên lên bằng tay.
- **Đổi tên hàm trong `classroom_service.py` mà quên chỗ gọi.** Hàm này được
  gọi từ `chat.py` và `exam.py`; tìm hết trước khi đổi.
- **Chuyển dữ liệu `classroom_oauth` sang bảng mới mà chưa kiểm tra.** Kiểm tra
  đăng được bài lên Classroom bằng bảng mới rồi mới xoá bảng cũ.


===============================================================================

# 6. Tình trạng sau khi thi công (2026-09-13)

## Đã làm

| Bước | Nội dung | Tệp |
|---|---|---|
| 1 | Cột `vai_tro`, hàm `lay_vai_tro`/`yeu_cau_giao_vien`, chặn cả 6 route `/gv/*` | `app/services/profile_service.py`, `app/core/deps.py`, `app/routers/classroom.py` |
| 2 | Đăng ký giáo viên có mã mời; xoá route `/register/teacher` cũ | `app/routers/auth.py`, `app/templates/auth/register_teacher.html` |
| 3 | `classroom_oauth_gv` + `lop_giao_vien`, mọi hàm nhận `user_id` | `app/services/classroom_service.py` |
| 4 | Khu làm việc `/gv`, `/gv/ra-de`, `/gv/de-da-tao`, `/gv/lop` | `app/routers/teacher.py`, `app/templates/teacher/*` |
| 5 | `GET /api/exam/tai-tex/{de_id}` | `app/routers/exam.py` |

## Một chỗ suýt sai, ghi lại để nhớ

Route `GET /register/teacher` **cũ** (trả về trang "Coming soon") nằm ở đầu
`auth.py`. Nếu chỉ thêm route mới ở cuối file thì FastAPI vẫn dùng route
đăng ký TRƯỚC, và trang đăng ký mới không bao giờ hiện ra — không báo lỗi gì
cả. Phát hiện bằng cách liệt kê `router.routes` và thấy `/register/teacher`
xuất hiện hai lần. Khi thêm route trùng đường dẫn, luôn kiểm tra lại như vậy.

## Chưa làm (để lần sau)

- Màn hình tự gán lớp cho giáo viên — hiện gán bằng SQL trong bảng
  `lop_giao_vien`.
- Đặt ma trận chi tiết cho từng đề (hiện lấy theo bảng cấu hình chung của
  loại bài kiểm tra).
- Sinh một lượt nhiều mã đề thành **các đề riêng biệt**: ô "số mã đề" đã có
  và đã truyền xuống `socau_ma_de`, nhưng cách ghép hiện tại dồn nhiều khối
  `\begin{ex}` vào CÙNG một đề, nên ra một đề mà mỗi câu lặp lại N lần chứ
  chưa phải N đề riêng. Đây là việc tiếp theo.
- Bật Row Level Security cho `classroom_oauth_gv`.
