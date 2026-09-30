# 27. DẠNG (A, B, C…), BIẾN THỂ (_01, _02…) VÀ QUY TRÌNH NHẬP BÀI TỪ GIÁO ÁN

Chốt ngày 30/09/2026 (cô Lan). Đọc tệp này **trước** mỗi lần nhận bài, đề
hoặc giáo án cô gửi để thêm câu vào ngân hàng. Các quy ước chung về ID xem
`04_ID_STANDARD.md`; cách chạy nháp và sửa một câu xem
`26_CHAY_NHAP_VA_SUA_CAU.md`.

---

## 1. Ba tầng: đơn vị kiến thức → dạng → biến thể

```
L10_C3_B5_TH031                 đơn vị kiến thức (Curriculum ID, số + mức độ)
L10_C3_B5_TH031_MC_A            dạng A   (Generator ID, có trong Mapping)
L10_C3_B5_TH031_MC_B            dạng B   (dạng khác, CÙNG đơn vị kiến thức)
L10_C3_B5_TH031_MC_B_01         biến thể 01 của dạng B (chỉ có trong Python)
L10_C3_B5_TH031_MC_B_02         biến thể 02 của dạng B
```

| Tầng | Ở đâu | Khác nhau ở chỗ nào |
|---|---|---|
| Đơn vị kiến thức (`TH031`) | PPCT, Curriculum | Yêu cầu cần đạt của Bộ GD&ĐT. **Không tự thêm, không nâng mức.** |
| Dạng (`_A`, `_B`, `_C`…) | Mapping (mỗi chữ cái một dòng) | **Các dạng toán khác nhau**, nhưng cùng một đơn vị kiến thức. |
| Biến thể (`_01`, `_02`…) | Chỉ trong `data/python_bank/` | Cùng dạng đó nhưng **cách hỏi phải khác đi** (không chỉ đổi số). |

Trong mỗi hàm, số liệu vẫn ngẫu nhiên theo `socau`, nên một biến thể đã tự
có nhiều câu khác số. Biến thể `_02` vì vậy **không** được là bản sao của
`_01` chỉ đổi số — phải đổi CÁCH HỎI.

### Cách hỏi khác đi — các kiểu thường dùng

- **Hỏi ngược**: `_01` biết góc → tính toạ độ; `_02` biết toạ độ → tìm góc.
- **Đổi đại lượng cho / hỏi**: `_01` biết `sin + cos` → tính `sin·cos`;
  `_02` biết `sin·cos` → tính `(sin ± cos)²`.
- **Bỏ chỗ dựa**: `_01` góc đặc biệt (tra bảng được); `_02` góc lẻ (bắt buộc
  dùng quan hệ phụ/bù).
- **Đổi bối cảnh**: `_01` cho sẵn `α + β = 180°`; `_02` đặt trong tam giác,
  học sinh tự nhận ra `A` và `B + C` bù nhau.
- **Đổi hình thức câu hỏi**: `_01` chọn công thức đúng/sai; `_02` dùng công
  thức đó để rút gọn.

Mức độ của `_02` phải **bằng** `_01` (cùng ID nên cùng NB/TH/VD).

### Ví dụ thật (Bài 5, lớp 10, commit 3.58)

| ID | `_01` | `_02` |
|---|---|---|
| NB029_SA_B | Biết `xOM`, tính biểu thức toạ độ `M` | Biết hoành/tung độ `M`, tìm `xOM` |
| TH030_SA_B | Biết `cos xOM`, tính diện tích `AOM` | Biết diện tích `AOM`, tìm `cos xOM` |
| TH031_MC_C | Tích sin, cos của góc đặc biệt phụ/bù | Góc lẻ: `sin²20° + sin²70°` |
| TH031_MC_E | Chọn công thức góc phụ/bù đúng/sai | Rút gọn biểu thức bằng công thức đó |
| TF_F | Tam giác biết góc tù/nhọn: xét dấu | Tam giác cho số đo góc: tính giá trị |

### Khi nào là DẠNG MỚI (chữ cái mới), khi nào là BIẾN THỂ

- Câu mới là **một dạng toán khác** so với mọi dạng đang có của đơn vị kiến
  thức đó → **dạng mới**: thêm chữ cái kế tiếp (`_H` sau `_G`), thêm dòng
  Mapping.
- Câu mới là **cùng dạng toán**, chỉ khác cách hỏi → **biến thể** `_NN`
  kế tiếp của ID đó. Không thêm dòng Mapping.
- Câu giống hệt một hàm đang có (chỉ khác số) → **không thêm**; ghi trong
  báo cáo là "đã có sẵn".

### Khi có từ hai biến thể trở lên

`tests/test_mot_id_mot_dang.py` chặn mọi ID có nhiều hàm mà chưa được soát.
Mỗi lần thêm `_02` cho một ID phải:

1. Thêm ID vào `CHO_PHEP_NHIEU_HAM`, kèm chú thích ngắn `_01 / _02` hỏi gì.
2. Viết lại trường `"Dang"` trong Mapping sao cho bao được **cả** `_01` và
   `_02` (mô tả theo đơn vị kiến thức, không theo một cách hỏi).

---

## 2. Quy trình khi cô Lan gửi bài / đề / giáo án

1. **Đọc Curriculum và Mapping của bài đó** (`data/curriculum/`,
   `data/mapping/`) và liệt kê các hàm Python đang có của từng ID.
2. **Xếp từng câu** vào một trong ba loại ở mục 1 (đã có / biến thể / dạng
   mới). Lập bảng "Câu → ID" để báo cáo.
3. **Mức độ**: chỉ dùng các mức mà Curriculum của bài có. Câu trong giáo án
   ở mức cao hơn (ví dụ VD mà bài chỉ có đến TH) thì **hạ mức** (cho số cụ
   thể thay cho chữ, bớt bước) hoặc bỏ. Tuyệt đối không thêm dòng mức cao hơn.
4. **Dạng mới** → dòng Mapping có
   `"ghi_chu": "CLAUDE THEM <ngày> - ... co Lan duyet lai"`; docstring hàm
   ghi rõ lấy theo câu nào của giáo án.
5. **Viết hàm** (xem mục 3), chạy thử nhiều seed, chạy nháp ra PDF với câu
   có hình.
6. **Chạy toàn bộ test**:
   `python3 -m pytest tests -q --ignore=tests/test_supabase.py -p no:cacheprovider`
7. **Ghi `16_CHANGELOG.md`**, commit (cô Lan tự đẩy lên bằng `day` /
   `day web`).
8. **Báo cáo**: bảng Câu → ID, các hàm mới, và **lỗi trong giáo án** (đáp án
   đánh `\True` sai, gõ nhầm, thiếu lời giải, đề thiếu dữ kiện…).
9. Có ý tưởng gì mới (dạng mới, đổi quy ước…) → **báo ngay và hỏi** cô.

---

## 3. Quy ước khi viết hàm sinh câu

- Đáp án và lời giải **tính bằng Python** (sympy khi cần chính xác), không
  gõ tay.
- **Không viết lại `math_type.py`.** Cần xử lý thêm thì viết hàm bọc trong
  tệp chương.
- Mọi thứ **theo sách giáo khoa hiện hành**: kí hiệu, cách trình bày, miền
  nghiệm (phần **không bị gạch**, bờ nét liền khi có dấu bằng, nét đứt khi
  không), dấu phẩy thập phân (`DAU_THAP_PHAN = ","`, khung đề nạp `icomma`).
- Tập số thực dùng biến `x`, tập số tự nhiên dùng `n`.
- Câu VD dạng đếm hỏi **"có bao nhiêu"**, không hỏi "số nào".
- **Trả lời ngắn**: một câu hỏi – một đáp số, là số thập phân hữu hạn, tối đa
  4 kí tự (dùng `_so_thap_phan_gon` để lọc).
- **Phương án trắc nghiệm không tự chấm cuối câu**: gói `ex_test` tự thêm
  dấu "." sau mỗi phương án `\choice`. Phương án là câu văn thì gọi
  `_MC_khong_cham(...)` thay cho `MC_SA_answer_text(...)` (có sẵn ở cuối các
  tệp L10_C1, C4, C5, C6, C8, L11_C2, C3, C4, C6, C8; tệp khác thì chép sang).
  Test `test_phuong_an_trac_nghiem_khong_tu_cham_cuoi` quét mọi hàm `_MC_`.
- Bốn phương án phải khác nhau (dùng `_ba_nhieu`), nhiễu là lỗi học sinh
  hay mắc (sai dấu, nhầm sin/cos, quên nhân ½…).
- Câu Đúng/Sai: bốn ý có chú thích `# a) NB`, `# b) TH`, `# c) VD`,
  `# d) VDC`; mỗi ý có bản đúng và bản sai, lời giải cho cả hai.
- Kí hiệu mức độ trong tệp gốc của cô: `Y` = NB, `B` = TH, `K` = VD, `G` = VDC.

---

## 4. Hình vẽ

- Hình phải hiện **cả trên PDF lẫn trên web** (và trong Word).
- Hình của đề: truyền vào tham số `dothi_de` của `MC_SA_answer_text` /
  `MC_SA_answer_const` / `TF_baitoan_du` (ra `\immini{đề}{hình}`).
- **Hình nằm trong từng phương án / từng ý Đúng-Sai** (ví dụ TH024 chọn hình
  biểu diễn miền nghiệm) được xử lý riêng từ 3.55:
  - `answer_parser_service.trich_dap_an` tách thành `hinh_phuong_an_tikz`
    `{A..D}` và `hinh_phat_bieu_tikz` `{a..d}`; `hinh_tikz` của đề không chứa
    các hình này.
  - `exam_assembler_service` dịch ra ảnh → `dap_an["hinh_phuong_an"]`,
    `dap_an["hinh_phat_bieu"]`.
  - API làm bài (`app/routers/exam.py`) trả URL `/api/exam/hinh/<mã>`;
    `chat/lam_bai.html` hiện ảnh ngay trong ô phương án (`.hinh-o`).
  - `word_service` chèn ảnh vào đúng phương án.
- Đề đã tạo trước khi sửa hàm vẫn giữ hình cũ (hình lưu theo đề).

---

## 5. Xuất Word cho giáo viên (3.54 – 3.56)

Chi tiết cài đặt ở `14_DEPLOYMENT.md` và `21_TAI_KHOAN_GIAO_VIEN.md`
(Bước 6). Những điểm kĩ thuật cần nhớ:

- `app/services/word_service.py`: `.tex` đã lưu → pandoc → `.docx`; công
  thức thành Office Math (OMML), TikZ thành PNG; không gọi AI, không tốn
  token. Máy chủ phải có `pandoc`.
- Câu nào pandoc không đọc được thì chỉ câu đó hiện dòng "xem bản PDF", các
  câu khác vẫn ra (đánh dấu `% @@CAU@@`).
- pandoc 2.9 bỏ mất `\quad`, `\qquad`, `\;`, `\,` nằm **ngoài** công thức
  (mẫu số liệu `$5$\quad $8$` ra "58"). `_khoang_trang_ngoai_toan` đổi các
  lệnh đó thành khoảng trắng Unicode trước khi đưa cho pandoc.
- Phương án A–D được thêm dấu "." ở cuối cho giống PDF (ex_test).
- Lỗi gõ trong hàm sinh câu (`%d`, `%s` chưa điền số, `\%%`) làm hỏng cả PDF
  lẫn Word; test `test_khong_ham_nao_sot_ma_dinh_dang` quét mọi hàm.

---

## 6. Kiểm tra trước khi báo xong

- Chạy mỗi hàm mới với nhiều seed (≥ 200), không lỗi, đáp số SA đúng khuôn.
- Chạy nháp PDF cho câu có hình: `python3 scripts/nhap.py <hàm> -n 2 --seed 3`.
- Toàn bộ pytest đạt.
- Changelog, commit có dòng `Co-Authored-By` và `Claude-Session`.

---

## 7. Quy tắc chọn câu khi ra đề (chống đề na ná nhau)

Chốt 30/09/2026 (cô Lan). Ví dụ: mức TH của bài 1, ma trận có 5 MC, 1 SA, 1 TL.

1. **Đơn vị kiến thức** (`exam_blueprint_service._chon_curriculum_id`): lọc trong
   toàn bộ yêu cầu TH của bài 1. Tập "đã dùng" **chung cho MC, SA, TL**: MC đã
   lấy 014 thì SA, TL lấy đơn vị khác, trừ khi hết. Buộc phải lặp thì lấy đơn
   vị **đang dùng ít nhất**. Thứ tự chọn: MC → SA → TL.
2. **Dạng** (`question_selector_service._xoay_vong_bien_the`): các câu cùng
   đơn vị lấy chữ cái khác nhau (A, B, D…); hết chữ cái thì lấy dạng dùng ít
   nhất (chỉ có A, B mà cần 3 câu → 2 A + 1 B, không bao giờ 3 A). Đơn vị
   được chia chưa có dạng cho loại câu đó → đổi sang đơn vị khác cùng bài,
   cùng mức có dạng đó (`_thay_don_vi_khac`).
3. **Biến thể** (`generator_service._chon_bien_the`): cùng dạng A hai lần thì
   khác biến thể (A_01, A_04); hết biến thể thì lấy biến thể dùng ít nhất.
4. Ma trận có SA, TL ở mức NB, TH được chia như trắc nghiệm (trước 30/09/2026
   các câu này bị bỏ mất).

Test: `tests/test_chon_cau_khong_na_na.py`.
5. Hai dạng khác loại câu nhưng **cùng mô tả "Dang"** trong Mapping của cùng
   một đơn vị (vd VD014_MC_A và VD014_SA_A đều là "Mệnh đề chưa biến", ra gần
   như cùng một bài toán) thì không lấy cả hai nếu còn dạng khác
   (`_khoa_mo_ta` trong question_selector_service). Vì vậy khi viết dạng SA/TL
   cho một đơn vị đã có MC, nên làm **bài toán khác** chứ không chép dạng MC.

---

## 8. Kho bối cảnh cho bài toán thực tế (không trùng bối cảnh trong một đề)

Chốt 30/09/2026 (cô Lan): lời dẫn bài toán thực tế tự chọn ngẫu nhiên trong
nhiều lĩnh vực để đề không nhàm chán; **trong một đề các câu không trùng bối cảnh**.

- Kho `_BOI_CANH_HAI_TAP` trong `L10_C1.py` (bài toán hai tập hợp, VD020): 15 lĩnh
  vực - đọc sách, môn học yêu thích (Toán, Ngữ văn, Vật lí, Hoá học...), thể thao, câu lạc bộ, học lực, văn nghệ (một lớp của trường THPT
  chuyên Hùng Vương: 10C1A … 10C9, cố định 35 học sinh); hoa (phụ nữ trên phố đi bộ
  Gia Lai), tài chính cá nhân, mạng xã hội, du lịch Gia Lai, đồ uống, đặc sản, nông
  nghiệp (cà phê, hồ tiêu), ngoại ngữ, thể dục. Mỗi bối cảnh có tỉ lệ số liệu riêng
  cho HỢP LÍ (vd người đầu tư chứng chỉ quỹ phần lớn đã có tài khoản ngân hàng).
- Không trùng trong một mã đề: tệp chương khai báo `_DE_HIEN_TAI = threading.local()`;
  `generator_service.call_generator` gán `_DE_HIEN_TAI.da_dung` = tập bối cảnh đã
  dùng của mã đề (lưu trong `used_variants["__boi_canh__"]`). Hàm chọn bối cảnh qua
  `_bo_chon_boi_canh()`. Chạy nháp lẻ thì mỗi lần gọi hàm tự không lặp.
- Muốn thêm bối cảnh: thêm một phần tử vào `_BOI_CANH_HAI_TAP` (mo, dv, tap, cap =
  (A, B, động từ, động từ phủ định, loại), tỉ lệ tA, tB, giao; mo_an + hoi_tong nếu
  dùng được cho câu hỏi tổng số).
- **Chỉ HAI tập hợp** (cô Lan 30/09/2026): SGK dừng bài toán thực tế ở hai tập hợp.
  Câu ba tập hợp (MC_A_03, SA_A_02) đã bỏ bớt một tập cho thành hai tập; bản ba
  tập để dành ở `data/chuyen_de_hoc_tap/ba_tap_hop_L10_C1.py`. Riêng câu tự luận
  biểu đồ Ven ba tập TH019_TL_A_01 giữ nguyên trong ngân hàng.
- **Chọn đáp án trước** (`_vung_hai_tap`): chọn số phần tử từng vùng (chỉ A, chỉ B,
  cả hai, không thuộc tập nào) theo tỉ lệ của bối cảnh, rồi mới suy ra dữ kiện -
  đề không bao giờ vô lí.
- **Nội dung hỏi ngẫu nhiên** (`_hoi_hai_tap`, `_cau_hai_tap`): mỗi câu chọn ngẫu
  nhiên hỏi cả hai / không thuộc tập nào / ít nhất một / chỉ A / chỉ B (mỗi biến thể
  có một nhóm nội dung hỏi riêng); câu "cả hai" có thể cho "mỗi người đều thuộc ít
  nhất một tập".
