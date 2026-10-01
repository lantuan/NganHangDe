# TIÊU CHUẨN ID TOÀN HỆ THỐNG

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

ID là xương sống của toàn bộ hệ thống. Mọi thành phần làm việc
bằng ID thay vì tên hiển thị. AI không được tự suy luận hoặc
tự tạo ID — chỉ Code Node được phép ghép/chọn ID theo quy tắc.

---

# Cấu trúc chung

L10_C1_B2_NB017_MC_A

L10 = Khối
C1 = Chương
B2 = Bài
NB = Mức độ
017 = Mã năng lực (lấy từ Curriculum, không tự sinh)
MC = Loại câu
A = Phiên bản

---

# Khối

L10, L11, L12

---

# Chương

C1, C2, C3, ...

---

# Bài

B1, B2, B3, ...

---

# Mức độ

NB — Nhận biết
TH — Thông hiểu
VD — Vận dụng
VDC — Vận dụng cao

---

# Mã năng lực

Lấy nguyên văn từ Curriculum. Không được tự sinh, không tự
thêm hậu tố chữ cái vào mã năng lực gốc.

---

# Loại câu

MC — Trắc nghiệm nhiều lựa chọn
TF — Đúng/Sai
SA — Trả lời ngắn
TL — Tự luận

Có thể mở rộng thêm trong tương lai.

---

# Phiên bản

A, B, C... Một năng lực có thể có nhiều câu hỏi khác nhau.

Ví dụ

L10_C1_B2_NB017_MC_A
L10_C1_B2_NB017_MC_B
L10_C1_B2_NB017_MC_C

---

# Ngoại lệ 1: Câu Đúng/Sai (TF) ra theo Chương

Câu TF không gắn với một Bài cụ thể, ra theo cả chương.

ID rút gọn:

L<khối>_C<chương>_TF_<phiên bản>

Ví dụ

L10_C1_TF_A
L10_C1_TF_B

Một câu TF lớn mặc định gồm 4 ý nhỏ mức độ: NB, TH, VD, VDC.

Candidate Pool của TF không đi qua Curriculum — chỉ ghép trực
tiếp Blueprint + Mapping theo chuong_so.

---

# Ngoại lệ 2: Mức VDC dùng chung Curriculum ID mức VD

Curriculum chỉ có 3 mức: NB, TH, VD. Không tồn tại curriculum_id
dạng VDC.

Toàn bộ câu VDC mượn curriculum_id của một competency mức VD
đã có sẵn. Quyết định một lượt sinh câu là VD hay VDC nằm ở
CN_QuestionSelector, không nằm ở Curriculum hay Blueprint.

Ví dụ

curriculum_id = L10_C1_B2_VD006

có thể phân bổ: tong_so_cau=3, so_cau_VD=2, so_cau_VDC=1.

curriculum_id không đổi, không thêm hậu tố VDC.

Đánh dấu DẠNG vận dụng cao (chốt 30/09/2026, cô Lan): ID dạng câu vẫn mang VD
(vì Curriculum không có VDC), nhưng dòng Mapping ghi thêm

"muc_do_dang": "VDC"

Ví dụ L10_C3_B6_VD036_MC_F (khinh khí cầu nhìn từ sườn đồi). Khi một mục
Blueprint mức VD có so_cau_VDC > 0 (MC, SA), CN_QuestionSelector lấy các suất
VDC trong các dạng đánh dấu VDC TRƯỚC, rồi mới lấy suất VD trong các dạng còn
lại; nhóm nào chưa có dạng thì lấy chung. Mỗi câu ra có "muc_do_cau" = VD/VDC.
Câu tự luận mức VD luôn là ý a) VD + ý b) VDC nên không cần đánh dấu.

Quy tắc khi tạo dạng MỚI (cô Lan, 01/10/2026): mỗi dạng MC/SA mức VD làm mới
phải được đánh giá VD hay VDC NGAY lúc tạo và ghi "muc_do_dang": "VDC" nếu là
VDC. Một hàm không được hỏi ngẫu nhiên lẫn câu VD và câu VDC: phải tách thành
hai dạng (hai chữ cái), ví dụ VD036_SA_F (tính AC, VD) và VD036_SA_O (tìm hướng,
VDC). Bối cảnh có câu tự luận a) VD, b) VDC thì MC/SA hỏi giống ý b) là VDC.
Các dạng cũ duyệt dần theo docs/bang_duyet_VD_VDC.xlsx.

Cùng một bối cảnh ra ở MC, SA, TL thì ghi CÙNG mô tả "Dang": bộ chọn câu tránh
hai dạng cùng mô tả trong một đề, trừ khi không còn dạng nào khác.

---

# Ngoại lệ 3: Câu Tự luận nhiều ý thuộc nhiều đơn vị kiến thức

Chốt 30/09/2026 (cô Lan): câu tự luận phải hỏi về HAI đơn vị kiến thức khác
nhau của cùng một chương, và ID phải thể hiện rõ hai đơn vị đó, để ma trận tính
đúng % mức độ và để tránh trùng với câu trắc nghiệm, trả lời ngắn.

ID (theo chương như câu TF, không ghi bài; đơn vị viết theo thứ tự ý a → ý b):

L<khối>_C<chương>_<ý a>_<ý b>_TL_<phiên bản>

Ví dụ

L10_C3_TH031_TH032_TL_A   ý a) TH031 (Bài 5), ý b) TH032 (Bài 6)
L10_C1_NB017_TH018_TL_A   ý a) NB017, ý b) TH018 (mức khác nhau)

Dòng Mapping có thêm trường cac_y:

"cac_y": [{"y": "a", "curriculum_id": "L10_C3_B5_TH031", "muc_do": "TH"},
          {"y": "b", "curriculum_id": "L10_C3_B6_TH032", "muc_do": "TH"}]

content = content các yêu cầu cần đạt nối bằng " | ".

Ma trận tính theo TỪNG Ý (như câu TF): mỗi ý chiếm một suất tự luận ở đúng
mức độ và đơn vị của nó. CN_QuestionSelector ghép các suất tự luận của Blueprint
(cùng chương, đúng mức độ) vào câu nhiều ý trước, suất còn thừa mới dùng câu tự
luận thường. Cả hai đơn vị phải nằm trong phạm vi bài của đề. Điểm phần Tự luận
chia theo suất (diem_service: câu hai ý = hai suất).

Mỗi câu tự luận gồm HAI ý (hai suất) - chốt 30/09/2026:
- câu hai đơn vị: mỗi ý một suất ở mức của đơn vị đó (như trên);
- câu một đơn vị mức VD: ý a) mức VD, ý b) mức VDC;
- câu một đơn vị mức NB/TH (loại cũ, chuyển dần sang hai đơn vị): hai ý cùng mức.
exam_rules.json: tu_luan.so_luong là số CÂU, so_y_moi_cau = 2, ty_le_muc_do chia
trên số ý (mặc định VD 50%, VDC 50%: 3 câu = 3 ý VD + 3 ý VDC).

Thứ tự chọn câu (cả Blueprint lẫn Selector): Đúng/Sai -> Tự luận -> Trắc
nghiệm nhiều lựa chọn -> Trả lời ngắn; phần sau tránh đơn vị kiến thức phần
trước đã dùng.

Mã nguồn: mapping_service.cac_y_tu_luan / so_suat_tu_luan,
question_selector_service._ghep_tu_luan_nhieu_y. Kiểm thử:
tests/test_tu_luan_nhieu_y.py, tests/test_mapping_curriculum.py.

# Ngoại lệ 4: Dạng "luyện tập thêm" - ngoài yêu cầu cần đạt (YCCĐ)

Chốt 01/10/2026 (cô Lan): bài toán hay nhưng YCCĐ của Bộ không có thì VẪN đưa
vào ngân hàng, nhưng phải đánh dấu để giáo viên biết và tự quyết định.

- KHÔNG tạo curriculum ID mới (số thứ tự NB/TH/VD nối liền giữa các chương, và
  Blueprint sẽ tự chia suất cho mục mới). Dạng mới gắn vào mục Curriculum gần
  nhất, giữ đúng mức độ của mục đó (thường là TH, số liệu đơn giản).
- Dòng Mapping ghi thêm "ngoai_yccd": true và ghi_chu bắt đầu bằng
  "LUYEN TAP THEM - khong co trong yeu cau can dat cua Bo ...".
- Mục Curriculum tương ứng ghi "dang_luyen_tap_them": [{"mo_ta", "mapping_id"}]
  và "ghi_chu_luyen_tap_them" (chỉ để tra cứu, Blueprint không đọc).
- Khi ra đề: dạng này được chọn như thường. Kết quả sinh đề có
  "canh_bao_ngoai_yccd": [{phan, cau, generator_id, dang}] (theo mã đề đầu),
  lưu vào blueprint của de_da_sinh; trang "Đề đã tạo" và khung chat (đề của giáo
  viên) hiện cảnh báo "câu luyện tập thêm"; file .tex bản giáo viên có dòng
  chú thích "% LUU Y GIAO VIEN ..." trước câu đó (bản học sinh không có).
- Hàm tra: mapping_service.la_ngoai_yccd(row), tim_dang_ngoai_yccd(lop, chuong, generator_id).
- Ví dụ: L10_C3_B5_TH030_MC_E (biểu thức đồng bậc biết tan/cot), TH030_MC_F,
  TH030_MC_G, TH031_MC_J và các bản SA tương ứng.

---

# PPCT

Dùng ID dạng L10_C1_B2. Không cần mức độ, không cần loại câu.

---

# Curriculum

Ví dụ: L10_C1_B2_TH014. Trong đó TH014 là năng lực.

---

# Mapping

Ví dụ: L10_C1_B2_VD020_TL_A. Mapping là cầu nối giữa Curriculum
và Python Generator (hoặc giữa Blueprint và Python Generator
đối với TF).

---

# Python

Tên file: L10_C1.py
Tên hàm: L10_C1_B2_NB017_MC_A()

Không đặt tên theo tiếng Việt. Tên hàm phải trùng Generator ID.

---

# API

Mọi API đều trả ID, không trả text trước.

Đúng: {"lesson_id":"L10_C1_B2"}
Sai: {"lesson":"Mệnh đề"}

---

# n8n

Toàn bộ Workflow làm việc bằng ID. Không dùng tên bài.

---

# AI

AI không được tự suy luận ID.
AI chỉ nhận ID có sẵn, hoặc sinh Request để Code đổi sang ID.
Không AI nào (kể cả CHV_Fun, CHV_Grader, CHV_Analyzer) được tự
tạo curriculum_id, generator_id, hay bất kỳ ID nào khác.

---

# Database

Các bảng chỉ lưu ID: lesson_id, question_id, curriculum_id,
mapping_id. Không lưu tên bài nếu không cần thiết.

---

# Quy tắc bất biến

ID là chuẩn duy nhất. Không sửa ID sau khi phát hành. Nếu thay
đổi nội dung chỉ tạo Version mới.

Ví dụ: L10_C1_B2_NB017_MC_B (đúng) — không sửa
L10_C1_B2_NB017_MC_A đã phát hành.

---

# Mục tiêu cuối cùng

FastAPI → n8n → Python → LaTeX → Dashboard → AI → Database
đều giao tiếp bằng ID. Tên hiển thị chỉ dùng ở giao diện người dùng.

===== FILE: docs/04_ID_STANDARD.md (thêm vào cuối file, TRƯỚC mục "Mục tiêu cuối cùng") =====

---

# GHI CHÚ CẬP NHẬT — Version 2.1

Trạng thái

🟢 Chuẩn chính thức (bổ sung)

---

## Biến thể nội dung trong Python (Content Variant)

Phân biệt rõ hai khái niệm:

```
Generator ID (ID chuẩn, dùng ở Mapping/Curriculum/Database/API)
    ↓
L10_C1_B1_VD014_MC_A
```

Content Variant (chỉ tồn tại trong Python file, KHÔNG xuất hiện ở nơi khác)
↓
L10_C1_B1_VD014_MC_A_01
L10_C1_B1_VD014_MC_A_02
L10_C1_B1_VD014_MC_A_03
...

Ý nghĩa

Một Generator ID có thể có NHIỀU hàm Python khác nhau, mỗi hàm là một
cách ra đề khác nhau (bối cảnh khác, dạng số liệu khác) cho cùng một
năng lực/dạng bài. Đây là cách bổ sung dần độ phong phú của ngân hàng đề
mà không cần tạo ID mới.

Chốt 30/09/2026 (cô Lan): biến thể `_02` phải có **cách hỏi khác** `_01`
(hỏi ngược, đổi đại lượng cho/hỏi, đổi bối cảnh…), cùng đơn vị kiến thức và
cùng mức độ; còn chữ cái `_A`, `_B` là các dạng toán khác nhau. Xem
`27_DANG_BIEN_THE_VA_NHAP_BAI.md`.

Quy tắc đặt tên hàm
{Generator_ID}_{số thứ tự 2 chữ số}

Ví dụ
def L10_C1_B1_VD014_MC_A_01(socau, socot):
...
def L10_C1_B1_VD014_MC_A_02(socau, socot):
...

---

## Nơi hậu tố _NN được phép xuất hiện

CHỈ trong
data/python_bank/

KHÔNG được xuất hiện ở

- Mapping
- Curriculum
- PPCT
- Database
- API Response
- Blueprint
- Candidate Pool

Mọi nơi khác chỉ làm việc với Generator ID gốc (không hậu tố).

---

## Cơ chế gọi hàm (Function Resolution)

Khi hệ thống cần sinh câu hỏi cho một Generator ID:
Input: generator_id (VD: L10_C1_B1_VD014_MC_A), socau
↓
Quét file Python tương ứng chương, tìm tất cả hàm khớp:
{generator_id}_01, {generator_id}_02, ...
↓
Nếu chỉ có 1 hàm → dùng hàm đó.
Nếu có nhiều hàm → chọn ngẫu nhiên 1 hoặc nhiều hàm trong số đó.
↓
Gọi hàm đã chọn với (socau, socot/dong) tương ứng.

Nếu Generator ID không có bất kỳ hàm nào khớp (`_01` trở lên không tồn tại)
→ báo lỗi thiếu Generator, không tự suy diễn.

---

## Không được

- Không đặt tên hàm chỉ bằng Generator ID gốc khi có từ 2 biến thể trở lên
  (tránh trùng tên hàm Python trong cùng 1 file).
- Không đổi số thứ tự biến thể đã phát hành (VD: đã có `_01` thì không xoá,
  chỉ được thêm `_02`, `_03`... về sau — giữ đúng nguyên tắc bất biến ID
  đã nêu ở phần trên của tài liệu).
---

# Quy uoc: CUNG don vi kien thuc thi CUNG so

Chot ngay 27/09/2026 (co Lan). Day la quy uoc de RA DE khong bi trung dang,
khong phai quy uoc danh so cho dep.

## Noi dung quy uoc

Mot don vi kien thuc co the duoc hoi o NHIEU MUC DO khac nhau. Khi do cac ban
ghi giu NGUYEN SO, chi doi phan muc do:

    L10_C1_B2_TH021    Xac dinh hop, giao, hieu... tren truc so   (thong hieu)
    L10_C1_B2_VD021    Xac dinh hop, giao, hieu... tren truc so   (van dung)

KHONG dung hau to chu cai (VD021A) cho truong hop nay.

## Vi sao

Neu mot de lay ca TH021 lan VD021 thi hai cau ay cung mot dang toan, chi khac
do kho -- hoc sinh nhin vao la thay trung. Cung mot so chinh la dau hieu de
may biet "hai ban ghi nay that ra la mot", tu do khong lay ca hai.

Thuat toan dung blueprint co ham _don_vi_kien_thuc() trong
app/services/exam_blueprint_service.py lam viec do: bo phan muc do khoi ma de
lay khoa.

    L10_C1_B2_TH021  ->  L10_C1_B2_021
    L10_C1_B2_VD021  ->  L10_C1_B2_021     cung khoa -> khong lay ca hai

Chi khi da het sach lua chon khac (vong 2) thi moi chap nhan lap, vi de van
phai du so cau theo ma tran.

## Khi nao thi dung so KHAC

Khi noi dung KHAC nhau, du cung bai va cung muc do. Vi du chuong 7:

    L10_C7_B19_VD104    Lap phuong trinh duong tron khi biet toa do ba diem
    L10_C7_B19_VD104A   Lap phuong trinh duong tron khi biet dieu kien khong
                        truc tiep cho truoc

Hai cai nay la HAI don vi kien thuc khac nhau nen PHAI khac so. Hien VD104A
dang dung hau to chu cai -- xem muc "Con ton dong" ben duoi.

## Con ton dong

L10_C7_B19_VD104A: noi dung khac VD104 nen dang la mot don vi rieng, phai cap
so rieng chu khong phai hau to A. Chua sua vi so chay lien tuc theo tung chuong
(C7 la 094-111), cap so moi o cuoi day (126) se pha tinh lien tuc do. Cho co Lan
quyet: hoac cap 126, hoac danh lai so cho ca C7 tro di (hien an toan vi tu C2
tro di chua co mapping hay ham Python nao tro vao).

Ngoai ra scope cua VD104A dang bi chep nham tu VD104 ("duong tron di qua ba
diem") trong khi noi dung la "dieu kien khong truc tiep cho truoc".


===============================================================================

DANG DO CLAUDE TU THEM VAO MAPPING

Khi nhap ham tu cac tep cua giao vien, co dang chua duoc khai trong Mapping.
Claude tu them dong Mapping cho dang do, va PHAI danh dau ngay tai dong ay:

    {
      "id": "L10_C9_TF_C",
      "content": "...",
      "Loai": "Dung sai",
      "Dang": "Tro choi quay banh xe nhieu lan (van dung cao)",
      "ghi_chu": "CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta"
    }

Truong "ghi_chu" chi de nguoi doc biet dong nay do Claude dat ID chu khong
phai giao vien; he thong ra de khong dung den no. Xoa truong nay khi giao
vien da soat va dong y voi ID.

Tim nhanh moi dong nhu vay:

    grep -rn "CLAUDE THEM" data/mapping/
