# Nguồn SGK cũ — để dành cho ngân hàng đề CHUYÊN ĐỀ HỌC TẬP

Bốn tệp trong thư mục này là ngân hàng câu hỏi **lớp 11 theo SGK cũ** của
cô Lan, giữ lại NGUYÊN BẢN làm nguồn cho ngân hàng đề **Chuyên đề học tập**
sau này. **Chưa nối vào hệ thống** — không tệp nào được `import`, không có
dòng Mapping nào trỏ tới.

| Tệp | Số hàm | Nội dung | Dùng cho |
|---|---|---|---|
| `H11.py` | 13 | Phép tịnh tiến, đối xứng trục, đối xứng tâm, phép quay, phép vị tự, phép đồng dạng | **Chuyên đề 11.1 — Phép biến hình phẳng** |
| `D11.py` | 48 | Hàm số lượng giác; PT lượng giác cơ bản; **PT lượng giác thường gặp** | Phần PT thường gặp dùng cho chuyên đề / lớp chuyên |
| `D12.py` | 67 | Quy tắc đếm; hoán vị – chỉnh hợp – tổ hợp; nhị thức Newton; xác suất | Nay thuộc **lớp 10 chương 8** — đang rút dạng sang |
| `H12.py` | 4 | Tứ diện, hai đường thẳng song song, trọng tâm | Nay thuộc **lớp 11 chương 4** — đã rút dạng sang |

## Lưu ý kĩ thuật khi dùng lại

Bốn tệp này viết theo **thế hệ cũ**, khác hẳn chuẩn hiện tại:

- Ghi thẳng ra `latex\data\de.tex` bằng `open(...)` (đường dẫn Windows),
  không trả về chuỗi.
- Dùng `\choice` với `\loigiai{}` **để trống** — không có lời giải.
- Không đi qua `math_type.py`, không theo quy ước ID
  `L<lop>_C<chuong>_B<bai>_<MUC><so>_<LOAI>_<PHIENBAN>`.
- Dùng `numpy.random` thay cho `random`.

→ Khi làm ngân hàng chuyên đề, **viết lại theo chuẩn hiện tại**, chỉ lấy
lại Ý TƯỞNG DẠNG CÂU và số liệu.

## Lỗi có sẵn trong `D12.py`

Bốn cặp hàm **trùng tên** — hàm sau ghi đè hàm trước nên hàm trước không
bao giờ chạy được:

- `D12K2_10` (dòng 506 và 532)
- `D12K3_4` (dòng 742 và 753)
- `D12K3_13` (dòng 876 và 887)
- `D12B3_15` (dòng 937 và 1018)

Khi viết lại nhớ tách thành hai dạng riêng, kẻo mất câu.
