# Chuẩn hàm sinh câu hỏi - Ngân Hàng Đề AI

Tài liệu cho Gem "Soạn dạng". Rút gọn từ docs/04_ID_STANDARD.md, docs/10_PYTHON_GENERATOR.md,
docs/27_DANG_BIEN_THE_VA_NHAP_BAI.md và các quy ước cô Lan đã chốt. Khi có mâu thuẫn, các tệp docs gốc là chuẩn.

## 1. ID

```
L10_C3_B6_TH032_MC_A_01
│   │  │  │  │   │  │ └─ biến thể _01, _02… (cùng dạng, CÁCH HỎI khác; chỉ có trong tên hàm Python)
│   │  │  │  │   │  └─── dạng A, B, C… (dạng toán khác nhau của cùng đơn vị kiến thức)
│   │  │  │  │   └────── loại câu: MC trắc nghiệm, SA trả lời ngắn, TL tự luận
│   │  │  │  └────────── số yêu cầu cần đạt (YCCĐ) của Bộ - lấy từ danh mục, KHÔNG tự đặt
│   │  │  └───────────── mức độ: NB Biết, TH Hiểu, VD Vận dụng (VDC dùng chung đơn vị VD)
│   │  └──────────────── bài
│   └─────────────────── chương
└─────────────────────── lớp
```

- Đơn vị kiến thức (Curriculum ID) = 4 phần đầu, ví dụ `L10_C3_B6_TH032`. Một đơn vị giữ MỘT số qua các mức độ
  (`L10_C1_B2_TH021` và `L10_C1_B2_VD021`); khác mức chỉ đổi phần NB/TH/VD.
- Thứ bậc: yêu cầu cần đạt > mức độ > dạng toán (chữ cái) > biến thể (_NN).
- **Dạng mới** (chữ cái mới): cách giải / thứ được hỏi khác hẳn các dạng đã có của đơn vị đó.
  Bài toán thực tế là dạng RIÊNG so với bản toán thuần cùng yêu cầu.
- **Biến thể** (_NN kế tiếp): cùng dạng nhưng CÁCH HỎI khác (hỏi ngược, đổi đại lượng cho/hỏi, đổi bối cảnh, bỏ chỗ dựa
  như góc đặc biệt → góc lẻ…). Không tạo biến thể chỉ đổi số - số đã ngẫu nhiên trong hàm.
- Bối cảnh KHÔNG phải dạng: cùng một việc toán ở nhiều bối cảnh thực tế là MỘT dạng, bối cảnh ghi ở dòng "Bối cảnh".
- MC và SA cùng dạng mang **cùng chữ cái** (MC_C ↔ SA_C) và cùng mô tả dạng.
- **Đúng/Sai** theo chương: `L10_C3_TF_A_01` (không có bài, mức độ).
- **Tự luận** hai đơn vị của cùng chương: `L10_C3_TH031_TH032_TL_A_01` (đơn vị ý a rồi ý b, không ghi bài).
  Tự luận một đơn vị mức VD: `L10_C3_B6_VD036_TL_A_01` (ý a VD, ý b VDC).
- Dạng mức NB/TH phải nằm dưới đơn vị NB/TH; dạng VD/VDC dưới đơn vị VD. Không xếp câu khó dưới đơn vị dễ.
- Vượt yêu cầu cần đạt của Bộ ("luyện tập thêm"): vẫn nhận, gắn vào đơn vị gần nhất cùng bài, ghi "Ngoài YCCĐ: có".
  Không nâng mức trên mức cao nhất của bài; nếu khó hơn thì làm đơn giản lại (ít bước hơn, số thay chữ).

## 2. Hàm Python

- Tên hàm = ID đầy đủ có `_NN`. Mỗi hàm một dạng/biến thể.
- Tham số (bắt buộc đúng tên):

| Loại | Khai báo | Gọi hàm có sẵn |
|---|---|---|
| MC | `def ..._MC_A_01(socau, dang=1):` | `MC_SA_answer_const(...)` hoặc `MC_SA_answer_text(...)` với `dang` |
| SA | `def ..._SA_A_01(socau, dang=2):` | như MC, `dang=2` (in ô trả lời ngắn) |
| TF | `def ..._TF_A_01(socau, socot=1):` | `TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], 0, 0, socot)` |
| TL | `def ..._TL_A_01(socau, dong=1):` | `TL_answer_text(debai, ds_y, 0, 0, dong)` |

- Hàm sinh `socau` câu KHÁC NHAU về số liệu (vòng `while len(da_co) < socau` loại trùng), nối các chuỗi trả về
  rồi `return` một chuỗi.
- Các hàm có sẵn (`MC_SA_answer_const`, `MC_SA_answer_text`, `TF_baitoan_du`, `TL_answer_text`, `TL_answer_const`)
  đã có trong tệp chương (`from math_type import *`), KHÔNG import lại, KHÔNG chép, KHÔNG sửa.
- Mọi `import` khác đặt TRONG thân hàm. Chỉ dùng: `random`, `math`, `fractions`, `sympy`, `numpy as np`.
- Hàm phụ (nếu cần) viết LỒNG trong hàm chính để không trùng tên với hàm khác trong tệp chương.
- Không `print`, không đọc/ghi tệp, không mạng, không `input`, không gọi AI, không đọc Curriculum/Mapping.
- Viết chuỗi LaTeX bằng chuỗi thô `r"..."` và định dạng `%` (tránh f-string vì ngoặc nhọn LaTeX).

### Tham số các hàm có sẵn

- `MC_SA_answer_const(debai, dapso, dsnhieu, giai, dothi_de, dothi_giai, dang)`: đáp số là SỐ / biểu thức toán;
  hàm tự bọc `$...$`. `dapso` là chuỗi LaTeX (ví dụ `"7"`, `r"\dfrac{1}{2}"`), `dsnhieu` là danh sách ≥ 3 phương án
  nhiễu KHÁC NHAU và khác đáp số (nên đưa 4–6 ứng viên). Không có hình thì `dothi_de = dothi_giai = 0`.
- `MC_SA_answer_text(...)`: cùng tham số, dùng khi phương án là CHỮ (câu văn, mệnh đề); tự viết `$...$` bên trong nếu cần.
- `TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], dothi_de, dothi_giai, socot)`: mỗi `y_*` là danh sách các cặp
  `(phát biểu, lời giải)`. Phát biểu ĐÚNG viết `r"{\True ...}"`, phát biểu SAI viết `r"{...}"`. Hàm tự chọn ngẫu nhiên
  một phát biểu cho mỗi ý.
- `TL_answer_text(debai, ds_y, dothi_de, dothi_giai, dong)`: `ds_y` là danh sách các bộ ba
  `(câu hỏi của ý, đáp số dạng chuỗi LaTeX, lời giải của ý)`, ít nhất HAI ý.

## 3. Quy tắc nội dung

Loại câu
- **SA**: MỘT câu hỏi, MỘT đáp số; đáp số tối đa **4 kí tự** (tính cả dấu "-" và dấu ","), là số. Số thập phân viết dấu
  phẩy; câu dẫn nói rõ cách làm tròn ("làm tròn đến hàng phần mười"). Cần nhiều ý thì là Tự luận.
- **TL**: từ HAI ý; tốt nhất ý a và ý b thuộc hai đơn vị kiến thức khác nhau của cùng chương.
- **TF**: đúng 4 ý, độ khó tăng dần, ghi chú đúng bốn mốc trong thân hàm:
  `# a) NB` (nhắc công thức/tính chất), `# b) TH` (một bước thay số đơn giản), `# c) VD` (nhiều bước),
  `# d) VDC` (phải tự nghĩ cách, nhiều bước). MỖI ý có **ít nhất 3 phát biểu đúng và 3 phát biểu sai**
  (sai theo những lỗi khác nhau học sinh hay mắc), để mỗi lần chạy ra đề khác.
- **MC**: một câu chỉ hỏi về MỘT chủ đề. Phương án nhiễu phải hợp lí (lỗi thường gặp: nhầm dấu, quên căn,
  nhầm công thức…) và nằm trong miền giá trị có thể của đại lượng (hỏi bình phương thì không có phương án âm).
  Phương án KHÔNG kết thúc bằng dấu chấm. Đáp án không được đoán ra mà không tính.

Đề bài
- Python TỰ SINH số liệu mỗi lần chạy; không chép cứng bài gốc ("không để đề chết"). Chọn số để kết quả đẹp,
  không suy biến (tam giác tồn tại, mẫu khác 0…), bài toán hợp lí với thực tế.
- Câu dẫn chỉ chứa dữ kiện DÙNG đến khi giải; không thêm dữ kiện thừa.
- Chỉ dùng kiến thức, công thức, phương pháp trong SGK Kết nối tri thức của lớp đó và các chương đã học;
  không dùng kiến thức lớp trên (ví dụ công thức nhân đôi ở lớp 10).
- Biến số thuộc ℕ đặt tên `n`, thuộc ℝ đặt tên `x`. Các mệnh đề liệt kê trong câu đánh số 1., 2., 3.;
  các ý tự luận là a), b) (hàm có sẵn tự đánh).
- Toán thực tế chỉ ở mức VD/VDC (MC, SA, TL). Mức Biết/Hiểu là toán thuần. (Riêng Đúng/Sai có thể có ý thực tế
  rất dễ ở mức Biết/Hiểu.)
- Bối cảnh lịch sử, di tích: thông tin thật chỉ ở câu dẫn và phải có nguồn; số liệu không có nguồn ghi "giả sử";
  câu cảm xúc (tự hào, biết ơn…) chỉ ở câu dẫn, học sinh chỉ làm toán. Câu dẫn ngắn gọn.

Lời giải
- Đầy đủ từng bước, đúng phương pháp SGK, khớp đáp số. Đây là căn cứ duy nhất để chấm và để gia sư AI giảng lại.

LaTeX
- Toán trong `$...$`; phân số `\dfrac`; độ `^{\circ}`; góc `\widehat{BAC}`.
- Số thập phân trong công thức viết `13{,}08` (ngoặc nhọn để LaTeX không chèn khoảng trắng).
- Hình vẽ: chỉ khi thật cần (bỏ hình làm đổi mức độ). Viết TikZ đơn giản vào `dothi_de` / `dothi_giai`; hình chỉ ghi
  đúng các chữ đã gọi tên trong đề.

## 4. Ví dụ đặt ID (GIẢ SỬ đơn vị L10_C3_B6_TH032 đang có MC_A … MC_G, SA_A … SA_G)

- Giáo viên đưa bài "biết hai cạnh và góc xen giữa, tính cạnh thứ ba" và danh mục đã có dạng này là `MC_B`
  với biến thể _01, _02 → biến thể: `L10_C3_B6_TH032_MC_B_03` và `L10_C3_B6_TH032_SA_B_03` (nếu SA_B có _01, _02).
- Bài "biết ba cạnh, tính côsin một góc" mà chưa có dạng nào như vậy → dạng mới `MC_H_01`, `SA_H_01`.
- Ví dụ trên là giả sử, chỉ minh hoạ cách nghĩ; luôn tra danh mục thật.
