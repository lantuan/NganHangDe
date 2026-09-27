# Lech giua PPCT va Curriculum - viec phai quyet

Phat hien ngay 27/09/2026 khi dung curriculum lop 11 va 12.

## Van de

He thong noi PPCT voi Curriculum bang CHUOI MA `L{lop}_C{chuong}_B{bai}`:

    exam_scope_service   doc PPCT  -> ra pham_vi_bai, vi du ["L10_C5_B12", ...]
    curriculum_service.load_curriculum_for_scope  lay dung cac ban ghi co
                         id bat dau bang chuoi do

Nhung PPCT va Curriculum dang danh so chuong/bai KHAC NHAU. Ma van khop chuoi,
nen may KHONG bao loi - no lang le lay ra cac yeu cau can dat cua BAI KHAC.

## Vi du that o lop 10

| Ma | PPCT ghi | Curriculum ghi |
|---|---|---|
| L10_C5_B12 | Số gần đúng và sai số | Phương trình quy về phương trình bậc hai |
| L10_C6_B15 | Hàm số | Các số đặc trưng đo độ phân tán |
| L10_C6_B16 | Hàm số bậc hai | Biến cố và định nghĩa cổ điển của xác suất |
| L10_C7_B19 | Phương trình đường thẳng | Đường tròn trong mặt phẳng toạ độ |
| L10_C8_B23 | Quy tắc đếm | Nhị thức Newton |

Hoc sinh chon "on tap den bai So gan dung va sai so" -> he thong lay yeu cau
can dat cua bai "Phuong trinh quy ve phuong trinh bac hai" -> ra de sai hoan
toan pham vi, ma khong co dau hieu gi bao la sai.

Hien CHUA gay hau qua vi moi chuong 1 co ham Python (chuong 1 thi PPCT va
Curriculum trung nhau: B1 Menh de, B2 Tap hop). Nhung ngay khi co Lan viet ham
cho chuong khac la loi nay hien ra.

## Goc re

PPCT lop 10 co 9 chuong (tach Thong ke o C5 va Xac suat o C9, bai 1-27).
Curriculum lop 10 co 8 chuong (gop Thong ke va Xac suat vao C6, bai 1-23).
C5 va C6 bi DAO CHO nhau giua hai ben.

Lop 11 va 12 cung lech, do Curriculum (Claude vua dung) danh so theo SGK Ket
noi tri thuc, con PPCT lai theo thu tu day that cua truong:

| | PPCT | Curriculum |
|---|---|---|
| L11_C1_B1 | Góc lượng giác | Giá trị lượng giác của góc lượng giác |
| L11_C3 | Giới hạn. Hàm số liên tục | Các số đặc trưng của mẫu ghép nhóm |
| L12_C4_B10 | Tích phân | Nguyên hàm |
| L12_C5_B13 | Phương trình đường thẳng | Phương trình mặt phẳng |

## PPCT con THIEU

PPCT lop 11 moi co 5 chuong / 18 bai - het hoc ki I. Thieu han hoc ki II:
ham so mu va logarit, quan he vuong goc trong khong gian, cac quy tac tinh
xac suat, dao ham.

PPCT lop 12 co 6 chuong / 16 bai - du chuong nhung it bai hon Curriculum
(Curriculum tach rieng mot so bai ma PPCT gop lai).

## Phai quyet: ben nao la chuan?

**Cach 1 - Curriculum chay theo PPCT (nen chon).** PPCT la ke hoach day that,
la thu quyet dinh "den tuan nay da day den bai nao" nen no phai la chuan. Doi
lai so chuong/bai cua Curriculum cho khop PPCT.
  - Lop 11, 12: lam duoc ngay, khong pha gi (chua co mapping cu, chua co ham).
  - Lop 10: phai danh lai C2-C9 va dich so bai. C1 giu nguyen (dang co 46 ham).
    Bay gio van con re; khi da viet ham cho cac chuong khac thi khong lam duoc
    nua.
  - Vuong: PPCT lop 11 chua co hoc ki II, nen 4 chuong cuoi chua biet danh so
    bao nhieu. Phai bo sung PPCT truoc.

**Cach 2 - PPCT chay theo Curriculum.** Sua lai tep PPCT. Nhung PPCT gan voi
tuan/tiet thuc te cua truong nen sua se lech ke hoach day.

**Cach 3 - Them bang doi chieu.** Giu ca hai, viet mot bang noi ma PPCT voi ma
Curriculum. Them mot lop du lieu nua phai bao tri - Claude khong khuyen nghi.

## Truoc mat da lam gi

Chua doi gi ca. Curriculum lop 11, 12 dang danh so theo SGK Ket noi tri thuc
va TU NHAT QUAN ben trong (mapping tro dung vao curriculum, 259+238+113 dang
deu khop). Cho co Lan chon roi moi doi.

Bai test tests/test_mapping_curriculum.py canh tinh nhat quan trong noi bo ba
lop du lieu. Chua co bai test nao canh cho lech PPCT nay - se them sau khi co
Lan chon cach.

---

# DA XU LI (27/09/2026)

Co Lan chot: **Curriculum chay theo PPCT**. Da lam xong.

## Cach lam

Khong phai doi so la xong, vi PPCT chia bai KHAC Curriculum. Phai dinh tuyen
TUNG YEU CAU CAN DAT ve dung bai cua PPCT. Bon cho phai tach/gop:

| Cho | Truoc | Sau (theo PPCT) |
|---|---|---|
| L10 C4_B8 "Cac phep toan tren vecto" | 1 bai, 14 yeu cau | tach lam 3: B8 tong/hieu, B9 tich voi mot so, B11 tich vo huong |
| L10 C6_B16 "Bien co va xac suat" | 1 bai, 14 yeu cau | tach lam 2: C9_B26 bien co va dinh nghia, C9_B27 thuc hanh tinh |
| L10 C7_B18 "Duong thang" | 1 bai, 8 yeu cau | tach lam 2: B19 phuong trinh, B20 vi tri tuong doi/goc/khoang cach |
| L11 C1_B1 | 1 bai, 9 yeu cau | tach lam 2: B1 Goc luong giac, B2 Gia tri luong giac |
| L12 C2_B7, C5_B15 | 2 bai rieng | gop vao B6 va B13 theo PPCT |

Va hai cho doi han chuong:

    L10 "Toa do cua vecto"  C7_B17 -> C4_B10   (PPCT xep vao chuong Vecto)
    L10 Thong ke <-> Ham so  C5 va C6 dao cho nhau
    L11 Gioi han <-> Thong ke  C3 va C5 dao cho nhau

## Ket qua

    Lop 10: 27/27 bai khop PPCT, 9 chuong (truoc la 8)
    Lop 11: 18/34 bai khop PPCT
    Lop 12: 16/16 bai khop PPCT

Khong con bai nao lech ten. Khong con bai nao cua PPCT bi bo quen.

## Lop 10 chuong 1 khong bi dung den

C1 dang co 46 ham Python va 34 dong mapping tro vao. PPCT cung ghi dung
B1 Menh de, B2 Tap hop nen von da khop - giu nguyen toan bo ma, ke ca cac lo
so 002, 004, 006, 009, 012, 016.

## Chu cai dang (A, B, C) duoc giu nguyen

Lan dung lai mapping dau tien Claude danh lai chu cai tu dau, lam
NB017_SA_C thanh NB017_SA_A va mat khop voi ham Python. Da sua: giu nguyen
chu cai cu, chi doi khi that su dung do (hai bai cu gop lam mot bai moi).
Ket qua: 0 cho phai doi chu cai.

## Bang anh xa ly thuyet cung doi theo

data/ly_thuyet/anh_xa.json khoa theo ma bai nen phai doi theo: 23 bai -> 27
bai. Bai cu tach lam nhieu bai moi thi moi bai moi nhan danh sach tep cua bai
cu do (vd 0H1-CD2.tex phuc vu ca B8, B9, B11 cua chuong Vecto).

## PPCT con thieu - can co Lan bo sung

PPCT lop 11 moi co het hoc ki I (5 chuong, 18 bai). Curriculum da co ca nam
nen 16 bai sau chua co trong PPCT:

    C6 B19-B22  Ham so mu va ham so logarit
    C7 B23-B28  Quan he vuong goc trong khong gian
    C8 B29-B31  Cac quy tac tinh xac suat
    C9 B32-B34  Dao ham

So bai B19-B34 hien la Claude danh noi tiep sau B18 - HOP LI nhung chua duoc
PPCT xac nhan. Khi co Lan bo sung PPCT hoc ki II, neu truong day thu tu khac
thi bao de doi lai (luc do van con re vi chua co ham Python nao).

## Canh khong cho lech lai

tests/test_ppct_curriculum.py (9 bai):
  - cung ma chuong/bai thi hai ben phai la cung mot bai
  - bai nao PPCT co day ma Curriculum khong co yeu cau nao -> bao loi
  - bai nao Curriculum co ma PPCT chua co -> chi in ra cho biet, khong bao loi
