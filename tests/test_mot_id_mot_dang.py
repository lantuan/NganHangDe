# -*- coding: utf-8 -*-
r"""Moi ID mapping chi duoc ung voi MOT dang cau hoi.

Co Lan 29/09/2026, sau khi soi de that: "da liet ke thi liet ke het. da
tap nay la con tap kia, co phan tu thuoc tap con... thi tat ca cung deu
giong nhau. chi cho chay chu so khac chu."

Boi canh: mot ID mapping co the co nhieu ham Python `_01`, `_02`, `_03`.
exam_assembler_service.py cap cho MOI MA DE mot bo used_variants rieng,
nen hai ma de cua cung mot bai thi co the roi vao hai ham khac nhau -
dieu do CHI chap nhan duoc neu cac ham ay ra CUNG MOT DANG, khac nhau
moi con so.

Truoc khi sua, ID L10_C1_B2_NB017_MC_B co ba ham ba dang khac han:
  _01 dem khang dinh sai tren tap SO,
  _02 dem khang dinh sai nhung viet bang CHU chua he dinh nghia trong de
      (hoc sinh khong the lam duoc),
  _03 hoi quan he phan tu - tap con giua hai tap long nhau.
Sau ma de cua cung mot bai thi ra ba kieu cau 3, lech han muc do.

Bai kiem tra nay KHONG cam co nhieu ham. No chi giu mot DANH SACH TRANG
cac ID duoc phep co nhieu ham - nhung ID ma ca hai ham deu ra dung mot
dang. Them ham thu hai cho mot ID khac la bai kiem tra do ngay, buoc
nguoi sua phai dung lai ma can nhac: tach ID rieng hay la giu chung.
"""
import collections
import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]

# ID duoc phep co nhieu ham - da soi tay, cac ham deu CUNG dang, chi khac
# ngu lieu/con so (co Lan xem lai 29/09/2026).
CHO_PHEP_NHIEU_HAM = {
    "L10_C1_B1_NB010_MC_A",   # ca hai deu: phat bieu menh de dao
    "L10_C1_B1_NB015_MC_A",   # ca hai deu: dieu kien can va du
    # tu giao an Bai 1 (Menh de):
    "L10_C1_B1_NB001_MC_A",   # danh sach co dinh / co menh de chua bien va menh de so
    "L10_C1_B1_TH003_MC_A",   # menh de hinh hoc co dinh / menh de so / thay gia tri vao P(x)
    "L10_C1_B1_TH003_TL_A",   # menh de dao voi |x| / viet bang ki hieu roi xet dung sai
    "L10_C1_B1_TH003_TL_B",   # phu dinh menh de luong tu / phu dinh menh de ve so
    "L10_C1_B1_VD014_MC_B",   # thay gia tri vao P(x) / dem n de 2^n + k nguyen to
    "L10_C1_TF_A",            # day so n / menh de voi moi x, x^2 + 2px + q > 0
    # tu giao an Bai 2 (Tap hop):
    "L10_C1_B2_TH018_MC_B",   # phep toan liet ke / M nhieu phan tu nhat, M con A va M con B
    "L10_C1_B2_VD021_SA_A",   # tham so de hop, giao thoa dieu kien / dem m de A giao B = A
    "L10_C1_TF_B",            # khoang va tap liet ke / A = {x | (x + k)/(x - c) nguyen}
    # tu giao an Bai 3 (Cac phep toan tren tap hop):
    "L10_C1_B2_TH021_MC_A",   # phan bu cua mot khoang / giao-hop-hieu-bu hai khoang (co dang {x | ...})
    "L10_C1_B2_VD021_MC_A",   # dem m nguyen / dieu kien cua m (hop = R, giao rong, giao khac rong)
    "L10_C1_B2_VD020_SA_A",   # khong thuoc nao / moi nguoi thuoc it nhat mot -> ca hai / chi thuoc A (kho boi canh)
    "L10_C1_B2_VD020_MC_A",   # khong thuoc nao / tim tong so / it nhat mot / tim so thuoc ca hai (kho boi canh)
    # tu de on tap cuoi chuong 1:
    "L10_C1_B1_TH014_MC_A",   # 17 nhom co dinh / menh de luong tu tham so do Python chon
    # tu bai tap trac nghiem Bai 3 chuong 2 (BPT bac nhat hai an):
    "L10_C2_B3_NB023_MC_A",   # chon diem thuoc mien nghiem / cho diem, chon bat phuong trinh
    "L10_C2_B3_NB025_MC_A",   # tien - gio cong - khoi luong / protein, cuoc goi, lam them, thue xe
    "L10_C2_TF_A",            # ax + by <= c dem diem nguyen / diem tren bo / mien nghiem mo ta bang loi
    "L10_C2_B3_NB022_MC_A",   # ca hai deu: nhan biet bat phuong trinh bac nhat hai an
    "L10_C2_B3_TH024_MC_A",   # ca hai deu: hinh nao bieu dien mien nghiem
    "L10_C3_B6_TH032_MC_A",   # ca hai deu: dinh li cosin tinh canh con lai
    # Bien the _02, _03 (co Lan yeu cau 29/09/2026: cung dang theo mapping,
    # khac loi dan / kieu cau):
    "L10_C2_B4_NB026_MC_A",   # he nao LA / he nao KHONG PHAI / ghep bpt khuyet an
    "L10_C4_B10_NB049_MC_A",  # xi+yj -> toa do / toa do -> xi+yj / thieu, dao hang tu
    "L10_C4_B11_NB057_MC_A",  # chung diem dau: tam giac deu / hinh vuong / cung-nguoc huong
    "L10_C4_B11_TH057_MC_A",  # khong chung diem dau: tam giac deu / hinh vuong
    "L10_C4_B11_TH057_MC_B",  # chung diem cuoi: tam giac deu / hinh vuong
    "L10_C5_B14_NB085_MC_A",  # khang dinh dung / khang dinh sai / tinh huong can thong ke
    "L10_C1_B1_VD014_MC_A",   # tham so k: voi moi x dung / ton tai x dung / voi moi x sai
    "L10_C1_B1_VD014_SA_A",   # nhu MC_A, tra loi ngan
    "L10_C1_B1_VD014_TL_A",   # keo theo + menh de dao: chia het / hinh hoc / so thuc
    "L10_C2_B4_VD028_MC_A",   # GTLN-NN tu he / diem dat GTLN / mien cho bang hinh
    "L10_C2_B4_VD028_SA_A",   # GTLN tu he / tu hinh / GTNN mien khong bi chan
    "L10_C2_B4_VD028_TL_A",   # cho san he / tu lap he (lai lon nhat) / chi phi nho nhat
    "L10_C3_B6_VD036_SA_A",   # vat can: dam lay / duong ham-ho-nha (cosin) / ben kia song (sin)
    "L10_C3_B6_VD036_SA_B",   # dien tich manh dat: Heron / hai canh-goc xen giua / tu giac = 2 Heron
    # tu giao an Bai 5 cua co Lan (29/09/2026):
    "L10_C3_B5_NB029_MC_A",   # mot gia tri goc dac biet / bieu thuc nhieu gia tri / tong-hieu hai gia tri co can
    "L10_C3_B5_NB029_MC_E",   # dau mot gia tri / dau tich-thuong hai gia tri (goc tu)
    "L10_C3_B5_NB029_MC_G",   # dau mot gia tri -> khoang / dau mot tich -> loai goc
    "L10_C3_B5_TH031_MC_A",   # hai goc bu nhau / trong tam giac (B + C = 180 - A)
    "L10_C3_B5_TH031_SA_A",   # rut gon voi goc bu / tam giac biet hai goc
    "L10_C3_B5_TH031_SA_B",   # he thuc co ban + goc bu / tong binh phuong goc phu nhau
    "L10_C3_TF_A",            # alpha dac biet / sin alpha = bo ba Pythagore / sin hoac cos co can thuc
    # tu bai tap trac nghiem Bai 5 (30/09/2026):
    "L10_C3_B5_TH031_MC_B",   # M doi xung N qua Oy: toa do bang chu / so do goc xOM
    "L10_C3_TF_D",            # M cho bang toa do thap phan / cho bang so do goc (co hinh, dien tich MAN)
    # 10 dang moi Bai 5, _02 hoi theo cach khac cung don vi kien thuc (co Lan 30/09/2026):
    "L10_C3_B5_NB029_MC_H",   # dang thuc dung/sai cua mot goc / gia tri nao bang so cho truoc
    "L10_C3_B5_NB029_SA_B",   # biet goc tinh toa do / biet toa do tim goc
    "L10_C3_B5_TH030_MC_D",   # sin + cos -> sin.cos / sin.cos -> (sin +- cos)^2, sin^4 + cos^4
    "L10_C3_B5_TH030_SA_B",   # cos -> dien tich AOM / dien tich AOM -> cos
    "L10_C3_B5_TH031_MC_C",   # tich sin cos goc dac biet / goc le phai dung phu-bu
    "L10_C3_B5_TH031_SA_C",   # cho alpha + beta / trong tam giac
    "L10_C3_B5_TH031_MC_D",   # dang thuc giua hai goc dac biet / suy ra gia tri gan dung
    "L10_C3_B5_TH031_MC_E",   # chon cong thuc dung-sai / rut gon bieu thuc
    "L10_C3_B5_TH031_MC_F",   # biet so do goc / biet sin-cos phan so
    "L10_C3_B5_TH031_MC_G",   # cho alpha tim 180 - alpha / cho 180 - alpha tim alpha
    "L10_C3_B5_TH031_MC_H",   # cho alpha tim 90 - alpha / nguoc lai
    "L10_C3_B5_TH031_MC_I",   # hinh goc bet / hinh goc vuong
    "L10_C3_B5_TH031_SA_D",   # goc bu so thap phan: xuoi / nguoc
    "L10_C3_B5_TH031_SA_E",   # goc phu so thap phan: xuoi / nguoc
    "L10_C3_B5_TH031_SA_F",   # hinh goc bet / goc vuong, so thap phan
    "L10_C3_TH031_TH033_TL_A",   # tam giac sin(A + B) -> R / tam giac vuong -> canh
    "L10_C3_TF_F",            # goc tu-nhon (dau) / so do goc (tinh gia tri)
    "L10_C1_B2_VD020_TL_A",   # it nhat mot / khong thuoc nao  -  biet so khong thuoc, tinh ca hai, chi A (kho boi canh)
    # VD cua bai 1 chuong 1 (chi co mot don vi VD014), 30/09/2026:
    "L10_C1_B1_VD014_SA_B",   # dem so menh de dung / dem n lam keo theo sai
    "L10_C1_B2_NB017_MC_G",   # tinh chat -> liet ke / liet ke -> tinh chat / a thuoc A khong
    "L10_C1_B2_NB017_SA_A",   # dem so phan tu / tong cac phan tu
    "L10_C1_B1_VD014_MC_D",   # keo theo tren R co tham so / keo theo chia het
    "L10_C1_B1_VD014_TL_B",   # phu dinh menh de voi moi (bat dang thuc) / ton tai (chia het)
    # tu bai tap trac nghiem Bai 6 (30/09/2026), _02 hoi theo cach khac:
    "L10_C3_B6_VD036_MC_B",   # qua dam lay (canh doi dien goc) / ve tinh (canh ke)
    "L10_C3_B6_TH032_MC_E",   # he thuc bang chu / he thuc da thay so
    "L10_C3_B6_TH033_MC_C",   # chon he thuc dinh li sin / ti so hai canh
    "L10_C3_B6_TH034_MC_D",   # cho so do goc / cho cos goc
    "L10_C3_B6_TH034_MC_E",   # Heron roi r / Heron roi R
    "L10_C3_B6_TH034_MC_F",   # hai canh + goc xen / ba canh
    "L10_C3_B6_VD036_SA_C",   # biet thoi gian tinh khoang cach / nguoc lai
    "L10_C3_B6_VD036_SA_D",   # hai dang / cay (AH, HB) / ang-ten tren noc nha
    "L10_C3_B6_VD036_SA_E",   # quang duong con lai / dien tich tu giac
    "L10_C3_TF_G",            # cho doan len doc / cho do cao doc
    "L10_C3_TF_H",            # BC = CD, hai goc / goc A va bon canh
    # tu giao an Bai 6:
    "L10_C3_B6_TH032_MC_A",   # (da co 2) + cos A cho bang phan so
    "L10_C3_B6_TH033_MC_A",   # biet mot canh hai goc / noi tiep duong tron R, tinh canh goc thu ba
    "L10_C3_B6_TH033_SA_A",   # R tu mot canh va goc doi / R cua tam giac vuong (bo Pythagore)
    "L10_C3_B6_TH034_TL_A",   # Heron roi r / Heron roi R va h_a
    "L10_C3_B6_TH035_MC_C",   # nhon-vuong-tu / vuong tai dinh nao
    "L10_C3_TF_B",            # goc dac biet / cos A phan so
    "L10_C3_TF_E",            # Heron S-R-r / tam giac vuong co goc 30-60
    "L10_C3_B6_VD036_TL_C",   # canh con lai + dien tich / rao dat: chu vi, chi phi, dien tich
    "L10_C3_B6_TH032_TL_A",   # canh thu ba + cos: goc dac biet / cos A phan so
    "L10_C3_B6_TH032_MC_B",   # biet ba canh tinh cos mot goc / cos goc lon nhat
    "L10_C3_B6_TH032_MC_D",   # he thuc canh -> goc: dang khai trien / dang tich
    "L10_C3_B6_TH033_TL_A",   # cho A, B / cho B, C (tu tinh A) roi dinh li sin
    "L10_C1_B1_TH014_MC_D",   # _01 menh de va menh de dao, _02 menh de tuong duong
    "L10_C1_B1_TH014_MC_F",   # _01 dung sai cua P va phu dinh, _02 chon menh de dung/sai
    "L10_C1_B1_TH014_MC_G",   # _01 cho san dung/sai, _02 menh de cu the
    "L10_C1_B1_TH014_SA_C",   # _01 cho san dung/sai, _02 menh de cu the
    "L10_C3_B6_TH034_MC_A",   # chon cong thuc theo du kien / cong thuc nao dung-sai
    "L10_C3_TF_C",            # tau hai chang: van toc-thoi gian / quang duong + huong la ban
    "L10_C3_B6_TH032_MC_F",   # cong thuc trung tuyen: chon dung / chon sai
    "L10_C3_B6_TH034_MC_G",   # cong thuc R, r, Heron: chon dung / chon sai
    "L10_C3_B6_TH035_MC_D",   # tam giac nho: trung tuyen / phan giac
    "L10_C3_B6_TH035_SA_C",   # tam giac nho: trung tuyen / phan giac
    "L10_C3_B5_TH030_MC_E",   # luyen tap them: bieu thuc dong bac, _01 cho tan, _02 cho cot
    "L10_C3_B5_TH030_MC_F",   # luyen tap them: _01 tan +- cot -> tan^2 + cot^2, _02 hoi nguoc
    "L10_C3_B5_TH031_MC_J",   # luyen tap them: _01 tich tan ghep phu, _02 tong cos ghep bu
    "L10_C3_B6_TH033_MC_D",   # hoi nguoc dinh li sin: _01 biet a va R, _02 he thuc k.a.sinB = b.can n
    "L10_C3_B6_TH033_MC_E",   # ti le canh = ti le sin: _01 chu vi, _02 ti so duong cao
    "L10_C3_B6_VD036_MC_P",   # duong tron qua 3 diem (VD): _01 dia co, _02 ho nuoc
    "L10_C3_B6_VD036_MC_Q",   # duong tron qua 3 diem (VDC): _01 dia co, _02 ho nuoc
    "L10_C3_B6_VD036_TL_K",   # duong tron qua 3 diem: _01 dia co, _02 ho nuoc
    "L10_C3_TF_O",            # duong tron qua 3 diem: _01 dia co, _02 ho nuoc
    "L10_C6_B15_VD092_MC_B",  # cuoc dien thoai VDC: biet tien tim phut / hai goi / bac thang 3 muc
    "L10_C6_B15_VD092_SA_B",  # nhu MC_B (ban tra loi ngan)
    "L10_C6_B15_VD092_TL_B",  # a) ham tren mot khoang, b) dung ham tren tung khoang: hai goi / bac thang
    "L10_C3_B6_VD036_MC_C",   # tau doi huong / hai phuong tien cung xuat phat / cho quang duong, hoi AC (cau hoi huong VDC tach sang MC_M 01/10/2026)
    "L10_C3_B6_VD036_TL_D",   # doi huong 60 do / hai huong la ban bat ki / phuong dong roi E30S (cho quang duong)
    "L10_C3_B6_VD036_TL_A",   # hai goc nang 30-60 / ang-ten tren noc nha
    "L10_C3_B6_VD036_MC_D",   # hai goc nang tren mat dat / thap tren doi / dieu
}


def _dem_ham_theo_id():
    dem = collections.Counter()
    for p in sorted((GOC / "data" / "python_bank").rglob("L1*_C*.py")):
        txt = p.read_text(encoding="utf-8")
        for m in re.finditer(r"^def (L\d+_C\d+\w*?)_\d\d\(", txt, re.M):
            dem[m.group(1)] += 1
    return dem


def test_khong_co_id_la_nao_gom_nhieu_ham():
    dem = _dem_ham_theo_id()
    nhieu = {k: v for k, v in dem.items() if v > 1}
    la = {k: v for k, v in nhieu.items() if k not in CHO_PHEP_NHIEU_HAM}
    assert not la, (
        "Cac ID sau dang co nhieu hon mot ham Python: %s.\n"
        "Cac ham duoi cung mot ID phai ra CUNG MOT DANG, chi khac con so. "
        "Neu chung khac dang thi phai tach ra ID rieng (them chu cai moi "
        "va them dong mapping). Neu da soi va chung that su cung dang thi "
        "them ID do vao CHO_PHEP_NHIEU_HAM trong tep nay." % sorted(la)
    )


def test_danh_sach_cho_phep_khong_bi_bo_quen():
    """ID trong danh sach trang ma khong con nhieu ham thi go bot di."""
    dem = _dem_ham_theo_id()
    thua = [k for k in CHO_PHEP_NHIEU_HAM if dem.get(k, 0) <= 1]
    assert not thua, (
        "Cac ID sau nam trong CHO_PHEP_NHIEU_HAM nhung khong con nhieu "
        "ham nua, nen go khoi danh sach: %s" % sorted(thua)
    )


def test_mapping_va_ham_khop_nhau():
    """Moi dong mapping phai co ham, va moi ham phai co dong mapping."""
    dem = _dem_ham_theo_id()
    thieu_ham, thieu_mapping = [], []
    for lop in (10, 11):
        thu_muc = GOC / "data" / "mapping" / ("toan%d" % lop)
        if not thu_muc.exists():
            continue
        for f in sorted(thu_muc.glob("L%d_C*.json" % lop)):
            py = GOC / "data" / "python_bank" / ("toan%d" % lop) / (f.stem + ".py")
            if not py.exists():
                continue
            ids = {r["id"] for r in json.loads(f.read_text(encoding="utf-8"))}
            ham_cua_chuong = {
                k for k in dem
                if k.startswith(f.stem.split("_C")[0] + "_C" + f.stem.split("_C")[1] + "_")
                or k == f.stem
            }
            thieu_ham += [i for i in ids if i not in dem]
            thieu_mapping += [k for k in ham_cua_chuong if k not in ids]
    assert not thieu_ham, "Dong mapping khong co ham Python: %s" % sorted(thieu_ham)
    assert not thieu_mapping, "Ham Python khong co dong mapping: %s" % sorted(thieu_mapping)


def test_cau_tu_luan_khong_con_o_dien_dap_an():
    r"""Cau tu luan khong duoc ve ra o vuong "KQ: []" nhu cau tra loi ngan.

    math_type.py gan \SA[4]{...} vao sau moi y cua cau tu luan. ex_test.sty
    dinh nghia \SA = \shortans nen no ve ra o dien. Quy tac cua co Lan la
    khong sua math_type.py, nen latex_template.tex phai nuot lenh \SA di.
    """
    tex = (GOC / "data" / "config" / "latex_template.tex").read_text(encoding="utf-8")
    assert r"\renewcommand{\SA}[2][]{}" in tex, (
        "latex_template.tex thieu dong nuot lenh \\SA - cau tu luan se lai "
        "moc ra o dien dap an."
    )
    assert r"\renewcommand{\shortans}" not in tex, (
        "Khong duoc dong vao \\shortans: PHAN III (tra loi ngan) van phai "
        "co o dien."
    )
