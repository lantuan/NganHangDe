# Rà soát 4 tệp cô vừa gửi (H11, H12, D11, D12)

*Claude — 29/09/2026*

## 1. Bốn tệp này là gì

Đọc nội dung thì thấy đây **không phải lớp 11 và lớp 12**, mà là **bốn tệp
của riêng lớp 11 theo SGK CŨ**:

| Tệp | Số hàm | Nội dung thực tế | Tương ứng SGK cũ |
|---|---|---|---|
| `D11.py` | 48 | Hàm số lượng giác; PT lượng giác cơ bản; PT lượng giác thường gặp | Đại số 11 — chương 1 |
| `D12.py` | 67 | Quy tắc đếm; hoán vị – chỉnh hợp – tổ hợp; nhị thức Newton; xác suất | Đại số 11 — chương 2, 3 |
| `H11.py` | 13 | Phép tịnh tiến, đối xứng trục, đối xứng tâm, phép quay, vị tự, đồng dạng | Hình học 11 — chương 1 |
| `H12.py` | 4 | Tứ diện, hai đường thẳng song song, trọng tâm | Hình học 11 — chương 2 |

Định dạng của chúng là **thế hệ cũ**: ghi thẳng vào `latex\data\de.tex`
(đường dẫn Windows), dùng `\choice` với `\loigiai{}` **để trống**, không đi
qua `math_type.py`. Vì vậy **không dùng lại code được**, nhưng **dùng lại
được Ý TƯỞNG DẠNG CÂU** — và đó chính là phần có giá trị.

## 2. Đối chiếu với chương trình 2018 (KNTT)

### 2.1. Phần KHÔNG còn trong chương trình lớp 11 hiện hành

- **Toàn bộ `H11.py`** (phép biến hình: tịnh tiến, đối xứng, quay, vị tự,
  đồng dạng). Chương trình 2018 đã **bỏ hẳn** phần này khỏi lớp 11.
- **`D11.py` phần PT lượng giác thường gặp**: phương trình bậc hai theo một
  hàm số lượng giác, phương trình $a\sin x + b\cos x = c$, tìm $m$ để
  phương trình có nghiệm. KNTT lớp 11 chỉ còn **PT lượng giác cơ bản**.
- **Tịnh tiến đồ thị hàm lượng giác** (`D11K1_7`) — không còn.

→ Em **không đưa** những dạng này vào ngân hàng lớp 11. Nếu cô muốn giữ
lại để dạy đội tuyển / lớp chuyên thì nói em, em sẽ để thành một nhóm
riêng (ví dụ `CHUYEN_*`) chứ không trộn vào đề chính khoá.

### 2.2. Phần đã CHUYỂN XUỐNG LỚP 10

`D12.py` chương 1, 2, 3 (quy tắc đếm, hoán vị – chỉnh hợp – tổ hợp, nhị
thức Newton) nay nằm ở **lớp 10 chương 8 (Đại số tổ hợp)**.

Đây là **nguồn rất tốt** vì lớp 10 chương 8 của mình mới có **30 dạng**.
Trong tệp có sẵn nhiều dạng hay chưa có trong ngân hàng:

- Đếm số tự nhiên thoả điều kiện (chẵn/lẻ, chia hết cho 5, chữ số đôi một
  khác nhau, nhỏ hơn một số cho trước) — `D12B1_6`, `D12K1_10`, `D12K1_13`
- Xếp chỗ quanh **bàn tròn** — `D12K2_3`
- Số **đường chéo** của đa giác lồi — `D12K2_4`
- Đếm giao điểm của đường thẳng và đường tròn — `D12K2_8`
- Đếm tam giác/vectơ từ tập điểm, có điểm thẳng hàng — `D12B2_6`,
  `D12K2_16`
- Giải phương trình/bất phương trình chứa $C_n^k$, $A_n^k$ — `D12B2_5`,
  `D12K2_15`
- Tìm hệ số của $x^k$ trong khai triển — `D12K3_5` → `D12K3_13`
- Tính tổng các $C_n^k$ có dấu và có luỹ thừa — `D12K3_2`, `D12K3_3`

→ **Xin ý kiến cô**: có bổ sung những dạng này cho **lớp 10 chương 8**
không? Em làm được, nhưng đó là mở rộng phạm vi nên em hỏi trước.

### 2.3. Phần CÓ THỂ BỔ SUNG NGAY cho lớp 11 (9 dạng)

Chín dạng dưới đây **nằm đúng trong yêu cầu cần đạt đã có** của chương
trình 2018, chỉ là ngân hàng mình chưa khai. Mỗi dạng gắn vào một
Curriculum ID **đã tồn tại**, nên không phải thêm yêu cầu cần đạt mới.

| Mã dạng mới | Nội dung | Lấy ý tưởng từ |
|---|---|---|
| `L11_C1_B3_TH020_MC_B` | Tập xác định của $y=\tan\frac{x}{m}$, $y=\frac{1}{\cos x}$, $y=\sin\sqrt{x}$ | `D11B1_2`, `D11Y1_10`, `D11Y1_11` |
| `L11_C1_B3_TH020_MC_C` | Khoảng đồng biến / nghịch biến của hàm lượng giác | `D11Y1_14`, `D11B1_13` |
| `L11_C1_B3_TH019_MC_B` | Nhận dạng đồ thị $y=a\sin x+b$ (có hình) | `D11B1_8`, `D11B1_18` |
| `L11_C1_B4_TH026_MC_B` | Giá trị nào là nghiệm của phương trình lượng giác | `D11Y2_3_1` … `D11B2_3_4` |
| `L11_C1_B4_TH026_SA_B` | Nghiệm thuộc một đoạn cho trước / tổng các nghiệm | `D11B3_9`, `D11K2_7` |
| `L11_C8_B29_TH133_MC_B` | Biến cố xung khắc và công thức cộng cho biến cố xung khắc | `D12Y4_2` |
| `L11_C8_B30_TH135_MC_B` | Xác suất rút bài tú lơ khơ, chọn số nguyên tố | `D12K4_5`, `D12B4_4` |
| `L11_C4_B11_TH056_MC_B` | Ba đường thẳng $a \parallel b$ — mệnh đề đúng | `H12Y2_1` |
| `L11_C4_B10_TH050_MC_B` | Giao tuyến qua trọng tâm hai mặt của tứ diện | `H12Y2_2` |

→ Em **sẽ làm 9 dạng này** ngay khi máy cô kết nối lại, vì chúng chỉ là
phiên bản B/C của yêu cầu cần đạt cô đã duyệt. Mọi dòng Mapping mới vẫn
có `ghi_chu` để cô duyệt lại.

## 3. Một điểm đáng chú ý trong tệp cũ

Trong `D12.py` có **bốn cặp hàm trùng tên** (hàm sau ghi đè hàm trước,
nên hàm trước không bao giờ chạy):

- `D12K2_10` (dòng 506 và 532)
- `D12K3_4` (dòng 742 và 753)
- `D12K3_13` (dòng 876 và 887)
- `D12B3_15` (dòng 937 và 1018)

Nếu cô còn dùng tệp này thì nên đổi tên một trong hai, kẻo mất câu.

## 4. Tóm lại

- **Bỏ**: toàn bộ `H11.py` và phần PT lượng giác thường gặp của `D11.py`
  (ngoài chương trình 2018).
- **Làm ngay**: 9 dạng ở mục 2.3 cho lớp 11.
- **Chờ cô quyết**: có bổ sung phần tổ hợp – nhị thức Newton của `D12.py`
  cho **lớp 10 chương 8** hay không.
