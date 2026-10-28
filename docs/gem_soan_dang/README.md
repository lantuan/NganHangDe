# Gem "Soạn dạng" - giáo viên đưa đề, Gemini viết hàm Python

Cô Lan 28/10/2026: giáo viên dùng một Gem Gemini do cô chia sẻ để biến bài toán bình thường thành hàm Python đúng
chuẩn ngân hàng; giáo viên dán code vào mục **Gửi dạng** trên web; cô tải về máy, chạy thử, duyệt rồi đưa vào
ngân hàng như mọi lần. Web không gọi AI (không tốn lượt), không chạy code giáo viên gửi.

## Các tệp trong thư mục này

| Tệp | Dùng làm gì |
|---|---|
| `chi_dan_gem.md` | Dán NGUYÊN VĂN vào ô "Hướng dẫn" (Instructions) khi tạo Gem |
| `chuan_ham_sinh.md` | Tải lên phần "Kiến thức" (Knowledge) của Gem |
| `ham_mau.py` | Tải lên Kiến thức: 4 hàm mẫu MC, SA, Đúng/Sai, Tự luận (chạy được) |
| `../../data/python_bank/math_type.py` | Tải lên Kiến thức (chỉ để Gem đọc tham số các hàm có sẵn) |
| `danh_muc_ID_lop10.md`, `_lop11.md`, `_lop12.md` | Tải lên Kiến thức: đơn vị kiến thức + dạng đang có |

Gem không nhận đuôi `.py` thì đổi tên thành `.txt` rồi tải lên.

## Tạo Gem (làm một lần)

1. Vào gemini.google.com → **Gems** (Khám phá Gem) → **Tạo Gem mới**.
2. Tên: "Soạn dạng - Ngân Hàng Đề AI".
3. Ô **Hướng dẫn**: dán toàn bộ `chi_dan_gem.md`.
4. Phần **Kiến thức**: tải lên các tệp ở bảng trên.
5. **Lưu**, rồi bấm **Chia sẻ** để lấy đường liên kết, gửi cho giáo viên.

## Cập nhật danh mục ID

Sau mỗi đợt thêm dạng vào ngân hàng, chạy `python3 scripts/xuat_tai_lieu_gem.py`, rồi trong Gem xoá ba tệp
`danh_muc_ID_lop*.md` cũ và tải bản mới lên (để Gem không đề xuất trùng chữ cái / số biến thể).

## Trên web

- Giáo viên: mục **Gửi dạng** (`/gv/gui-dang`) trên thanh điều hướng khu giáo viên. Dán PHIẾU + CODE, bấm **Gửi duyệt**.
  Web chỉ đọc cú pháp (ast), lấy tên hàm theo ID, báo chỗ đáng ngờ (`open(`, `os.`…) cho người duyệt; KHÔNG chạy code.
  Bảng cuối trang hiện trạng thái (Chờ duyệt / Đã duyệt / Trả lại) và lời nhắn. Mỗi giáo viên tối đa 30 bài/ngày.
- Người duyệt (email trong `EMAIL_DUYET_DANG`, mặc định nganhangdetoanchv@gmail.com - tài khoản liên hệ của web, phải đăng kí vai trò GIÁO VIÊN): **Duyệt dạng** (`/gv/duyet-dang`):
  lọc theo trạng thái, xem phiếu/đề gốc/code, **Tải .py** từng bài hoặc **Tải tất cả bài chờ duyệt (.zip)**,
  ghi lời nhắn rồi bấm **Đã duyệt** / **Trả lại** / **Đưa về chờ**.
- Bài gửi lưu trên VPS ở `data/gui_dang/<mã>.json` (không đẩy lên GitHub).
- Biến môi trường (tuỳ chọn, trong `.env` trên VPS): `GEM_SOAN_DANG_URL` = link Gem (trang Gửi dạng hiện nút
  "Mở Gem Soạn dạng"); `EMAIL_DUYET_DANG` = email người duyệt (nhiều email cách nhau dấu phẩy).

## Cô duyệt trên máy

1. Trang Duyệt dạng → **Tải .py** (hoặc tải .zip rồi giải nén) vào `nhap/gui_dang/`.
2. `python3 scripts/thu_dang_gui.py nhap/gui_dang/<mã>.py` - chạy 30 bộ số, kiểm loại câu, tham số, SA ≤ 4 kí tự,
   Đúng/Sai ≥ 3 đúng/≥ 3 sai mỗi ý + bốn mốc độ khó, đề có đổi số; ghi bản nháp `nhap/gui_dang/<mã>_dethi.pdf`,
   `_loigiai.pdf`.
3. Đạt thì đưa vào ngân hàng như mọi lần (chép hàm vào `data/python_bank/toanXX/LXX_CY.py`, thêm dòng Mapping nếu là
   dạng mới, chạy test), `day web`; rồi bấm **Đã duyệt** (ghi lời nhắn, ví dụ ID cuối cùng). Chưa đạt thì dán lỗi vào
   lời nhắn, bấm **Trả lại**.
