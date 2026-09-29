# 26. CHẠY NHÁP VÀ SỬA MỘT CÂU HỎI

Version: 1.0 — 2026-09-29

Sổ tay cho cô Lan: thấy một câu lạ trên web → tìm ra hàm Python → chạy
nháp ra LaTeX/PDF để soi → sửa → đẩy lên web. Làm tuần tự từ bước 1.

Mọi lệnh gõ trong **Terminal của VS Code**, đứng ở thư mục gốc dự án
(`/Users/mailan/Desktop/NganHangDe_Lan/web/NganHangDe`).

---

## Bước 1. Tìm hàm sinh ra câu đang thấy trên web

Web không hiện tên hàm. Copy **một cụm chữ đặc biệt** trong đề (khoảng
5–8 chữ, tránh chỗ có số vì số thay đổi mỗi lần sinh) rồi tìm:

```bash
grep -rn "phương án nào không đúng" data/python_bank
```

Kết quả dạng:

```
data/python_bank/toan10/L10_C1.py:5472:   Trong các phương án sau, ...
```

- Tệp: `toan10/L10_C1.py` (lớp 10, chương 1), dòng 5472.
- Mở tệp, kéo **lên trên** dòng đó tới dòng `def ...` gần nhất — đó là
  tên hàm, ví dụ `def L10_C1_B2_NB017_MC_A_01(...)`.

Không ra kết quả? Câu dẫn có thể bị ngắt giữa hai dòng code — thử cụm
chữ ngắn hơn, hoặc cụm chữ trong phương án / lời giải.

### Đọc tên hàm

```
L10_C1_B2_NB017_MC_A_01
 │   │  │  │  │   │  │ └ biến thể (01, 02 ... cùng một dạng, chỉ khác cách viết)
 │   │  │  │  │   │  └── chữ cái dạng (A, B, C ... trong cùng một yêu cầu cần đạt)
 │   │  │  │  │   └───── loại câu: MC trắc nghiệm | TF đúng/sai | SA trả lời ngắn | TL tự luận
 │   │  │  │  └───────── số thứ tự yêu cầu cần đạt trong curriculum
 │   │  │  └──────────── MỨC ĐỘ: NB | TH | VD
 │   │  └─────────────── bài
 │   └────────────────── chương
 └────────────────────── lớp
```

Chi tiết đầy đủ: `docs/04_ID_STANDARD.md`.

---

## Bước 2. Chạy nháp ra LaTeX và PDF

```bash
python3 scripts/nhap.py L10_C1_B2_NB017_MC_A_01            # 5 câu
python3 scripts/nhap.py L10_C1_B2_NB017_MC_A_01 -n 20      # 20 câu - soi nhiều bộ số
python3 scripts/nhap.py L10_C1_B2_NB017_MC_A_01 --seed 7   # cố định số: chạy lại ra y hệt
python3 scripts/nhap.py L10_C1_B2_NB017_MC_A               # bỏ _01: chạy mọi biến thể
python3 scripts/nhap.py L10_C1_B2_NB017_MC_A_01 --khong-pdf   # chỉ ra .tex, không biên dịch
```

Kết quả nằm trong thư mục **`nhap/`** (thư mục này không đẩy lên GitHub,
xoá thoải mái):

| Tệp | Nội dung |
|---|---|
| `nhap/<TÊN>_dethi.tex` / `.pdf` | bản đề, không lời giải |
| `nhap/<TÊN>_loigiai.tex` / `.pdf` | bản có đáp án (`\True`) và lời giải |
| `nhap/<TÊN>_*.log` | nhật ký LaTeX - xem khi PDF lỗi |

Câu sinh ra **giống hệt trên web**: cùng cách gọi hàm, cùng bộ lọc làm
đẹp biểu thức (bỏ `1x`, `+ -3`...), cùng khung
`data/config/latex_template.tex` và `ex_test.sty`.

Mẹo:

- Muốn so trước/sau khi sửa: chạy với cùng `--seed`, sửa code, chạy lại
  cùng `--seed` → hai bản cùng bộ số, chỉ khác chỗ đã sửa.
- Script in `!! Canh bao loai cau` nếu câu sinh ra sai loại (vd hàm MC mà
  không có `\choice`) - vẫn xuất nháp để soi.

### Khi PDF không ra

Script in ngay dòng lỗi LaTeX. Hay gặp:

| Lỗi in ra | Cách xử lý |
|---|---|
| `File 'xxx.sty' not found` | máy thiếu gói: `sudo tlmgr install xxx` (MacTeX có sẵn tlmgr) |
| `Khong tim thay pdflatex` | máy chưa cài LaTeX - cài MacTeX; tệp `.tex` vẫn mở được bằng TeXstudio |
| `Undefined control sequence` | lệnh LaTeX gõ sai trong hàm Python - mở `.log`, tìm dòng `l.<số>` để biết chỗ |
| `Missing $ inserted` | công thức thiếu/thừa dấu `$` trong chuỗi của hàm |

---

## Bước 3. Soi câu theo danh sách

- [ ] Câu dẫn khớp với phương án (hỏi "khẳng định" thì phương án phải là
      khẳng định; hỏi "ứng dụng" thì nhiễu cũng phải là ứng dụng).
- [ ] Đúng **mức độ** trong tên hàm (NB / TH / VD). Câu phải suy ngược
      tham số, nhiều bước biến đổi → không thể là NB.
- [ ] Mọi biến thể, mọi bộ số **cùng một dạng**: đề chữ thì chữ hết, đề
      số thì số hết; chỉ đổi con số.
- [ ] Không vượt khung chương trình của lớp/chương đó.
- [ ] Đáp án lấy từ Python (không tính tay, không để AI tính).
- [ ] Lời giải đúng toán, viết đúng kí hiệu: tập liệt kê dùng dấu `;`;
      số âm làm cơ số lũy thừa phải có ngoặc `\left(-3\right)^{2}`.
- [ ] Trả lời ngắn: đáp số là số thập phân hữu hạn, tối đa 4 kí tự.
- [ ] Câu cần hình thì phải có hình (TikZ) cả trên PDF lẫn web.

---

## Bước 4. Sửa

### 4a. Chỉ sửa nội dung (câu dẫn, nhiễu, lời giải)

Sửa thẳng trong hàm ở `data/python_bank/toan<lớp>/L<lớp>_C<chương>.py`.
**Không sửa `math_type.py`.** Ghi một dòng chú thích `# SUA <ngày>: ...`
ngay chỗ sửa để sau này biết vì sao. Chạy lại bước 2 để xem.

### 4b. Câu sai mức độ / sai yêu cầu cần đạt → đổi ID

Ví dụ thật (29/09/2026): `L10_C1_B2_NB017_SA_C_01` → `L10_C1_B2_VD021_SA_B_01`.

1. **Tìm ID đích trong curriculum** - mở
   `data/curriculum/toan<lớp>/L<lớp>_C<chương>.json`, tìm yêu cầu cần đạt
   đúng với câu (vd `L10_C1_B2_VD021` - khoảng, đoạn trên trục số).
2. **Chọn chữ cái dạng chưa dùng** - tìm trong mapping:
   ```bash
   grep -n '"id": "L10_C1_B2_VD021_SA' data/mapping/toan10/L10_C1.json
   ```
   Đã có `SA_A` → dùng `SA_B`.
3. **Đổi tên hàm** trong tệp `.py`: `def L10_C1_B2_VD021_SA_B_01(...)`.
   Đuôi `_01` bắt buộc - thiếu là hệ thống không thấy hàm.
4. **Sửa dòng mapping** trong `data/mapping/toan<lớp>/L<lớp>_C<chương>.json`:
   đổi `"id"` sang ID mới (bỏ `_01`), `"content"` chép từ dòng curriculum
   đích, giữ `"Loai"`, `"Dang"`.
5. **Kiểm tra** (bước 5) - có bài test so khớp tên hàm với mapping, sai
   là báo ngay.

Lưu ý: câu **trả lời ngắn** trong đề chỉ lấy mức VD/VDC
(`data/config/exam_rules.json`) - dòng SA mức NB/TH không bao giờ được
rút vào đề.

---

## Bước 5. Kiểm tra rồi đẩy lên web

```bash
python3 -m pytest tests -q --ignore=tests/test_supabase.py -p no:cacheprovider
```

Dòng cuối phải là `... passed` (không có `failed`). Rồi:

```bash
day          # đẩy lên GitHub
day web      # đẩy lên GitHub + cập nhật VPS + kiểm tra web còn sống
```

(`day` là lối tắt đã cài - xem `docs/14_DEPLOYMENT.md` nếu máy mới.)

---

## Lối tắt `nhap` (tuỳ chọn, cài một lần)

```bash
echo 'alias nhap="cd /Users/mailan/Desktop/NganHangDe_Lan/web/NganHangDe && python3 scripts/nhap.py"' >> ~/.zshrc
source ~/.zshrc
```

Sau đó gõ ở đâu cũng được: `nhap L10_C1_B2_VD021_SA_B_01 -n 10`.
