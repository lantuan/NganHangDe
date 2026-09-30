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
    "L10_C1_B2_VD020_SA_A",   # hai tap: khong thuoc tap nao / ba tap: dung hai mon -> ca ba
    "L10_C1_B2_VD020_MC_A",   # hai tiet muc / nhom khong thuoc tap nao / ba tap: tinh hop
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
    "L10_C3_B5_NB029_MC_A",   # mot gia tri goc dac biet / bieu thuc nhieu gia tri
    "L10_C3_B5_NB029_MC_E",   # dau mot gia tri / dau tich-thuong hai gia tri (goc tu)
    "L10_C3_B5_NB029_MC_G",   # dau mot gia tri -> khoang / dau mot tich -> loai goc
    "L10_C3_B5_TH031_MC_A",   # hai goc bu nhau / trong tam giac (B + C = 180 - A)
    "L10_C3_B5_TH031_SA_A",   # rut gon voi goc bu / tam giac biet hai goc
    "L10_C3_B5_TH031_SA_B",   # he thuc co ban + goc bu / tong binh phuong goc phu nhau
    "L10_C3_TF_A",            # alpha dac biet / sin alpha = bo ba Pythagore
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
    "L10_C3_B6_TH034_MC_A",   # chon cong thuc theo du kien / cong thuc nao dung-sai
    "L10_C3_TF_C",            # tau hai chang: van toc-thoi gian / quang duong + huong la ban
    "L10_C3_B6_VD036_MC_C",   # tau doi huong / hai phuong tien cung xuat phat
    "L10_C3_B6_VD036_TL_D",   # doi huong 60 do / hai huong la ban bat ki
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
