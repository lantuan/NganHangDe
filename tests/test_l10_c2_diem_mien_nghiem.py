"""Chuong 2 lop 10 - dang "diem thuoc mien nghiem" them 15/10/2026 (co Lan chot muc do: hinh -> NB, bat phuong trinh
-> TH, he -> VD; hinh cua he -> TH).

  NB024_MC_B / SA_B: cho HINH mien nghiem cua mot bat phuong trinh -> diem nao thuoc / co bao nhieu diem thuoc.
  TH027_MC_B / SA_B: cho HINH mien nghiem cua HE hai bat phuong trinh -> diem nao thuoc / co bao nhieu diem thuoc.
  VD027_MC_B / SA_B: cho HE bat phuong trinh -> diem nao thuoc / co bao nhieu diem thuoc.
  (TH024_MC_B / SA_B = NB023_MC_A / SA_A cu, da co test rieng.)

Dap so duoc TINH LAI DOC LAP: cau hinh thi doc thang HINH TikZ (da giac bi gach, bo net lien/dut) roi xet tung diem;
cau he thi doc he trong de bai (sympy) roi thay toa do. Khong dung lai ham sinh de.
"""
import importlib.util
import re
import sys
from pathlib import Path

from sympy import Symbol
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, standard_transformations)

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C2_diem_mien_nghiem", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_diem_mien_nghiem"] = M
_spec.loader.exec_module(M)

SO_LAN = 300
X, Y = Symbol("x"), Symbol("y")
DIEM = re.compile(r"\\left\((-?\d+); (-?\d+)\\right\)")
THOA = {r"\le": lambda v, c: v <= c, r"\ge": lambda v, c: v >= c, "<": lambda v, c: v < c, ">": lambda v, c: v > c}


def _bat(ham, seed, dang):
    """(debai, dapso, dsnhieu, giai, hinh) truyen vao MC_SA_answer_text / MC_SA_answer_const."""
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda debai, dap, nhieu, giai, hinh=0, *a, **k: cap.append((debai, str(dap), list(nhieu), giai, hinh)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        M._rd.seed(seed)
        ham(1, dang=dang)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _diem(tex):
    return [(int(a), int(b)) for a, b in DIEM.findall(tex)]


# ------------------------------------------------------------------ doc hinh TikZ
def _doc_hinh(tikz):
    """(da giac bi gach, hai dau mut cua bo, bo net lien?)."""
    m = re.search(r"\\fill\[pattern=north east lines\] (.+?) -- cycle;", tikz)
    gach = [tuple(map(float, p)) for p in re.findall(r"\((-?[\d.]+),(-?[\d.]+)\)", m.group(1))]
    b = re.search(r"\\draw\[(dashed,)?thick\] \((-?[\d.]+),(-?[\d.]+)\)--\((-?[\d.]+),(-?[\d.]+)\);", tikz)
    bo = ((float(b.group(2)), float(b.group(3))), (float(b.group(4)), float(b.group(5))))
    return gach, bo, b.group(1) is None


def _cheo(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


EPS = 0.05     # TikZ lam tron toa do 3 chu so thap phan; diem nguyen khong nam tren bo thi |cheo| >= 1


def _tren_bo(p, bo):
    return abs(_cheo(bo[0], bo[1], p)) < EPS


def _thuoc_hinh(p, gach, bo, lien):
    """Diem p thuoc mien nghiem (phan KHONG bi gach, ke ca bo neu net lien) - xet bang hinh hoc thuan tuy."""
    if _tren_bo(p, bo):
        return lien
    n = len(gach)
    dau = [_cheo(gach[i], gach[(i + 1) % n], p) for i in range(n)]
    trong_gach = all(d >= -1e-9 for d in dau) or all(d <= 1e-9 for d in dau)
    return not trong_gach


def _trong_khung(p, tikz):
    x1 = float(re.search(r"\\draw\[->\] \(-?\d+,0\)--\((-?[\d.]+),0\)", tikz).group(1)) - 0.6
    x0 = int(re.search(r"\\draw\[->\] \((-?\d+),0\)--", tikz).group(1))
    y0, y1 = re.search(r"\\draw\[->\] \(0,(-?\d+)\)--\(0,(-?[\d.]+)\)", tikz).groups()
    return x0 < p[0] < x1 and int(y0) < p[1] < float(y1) - 0.6


def test_th024_mc_b_doc_hinh():
    bay_tren_bo = 0
    for s in range(SO_LAN):
        debai, dap, nhieu, giai, hinh = _bat(M.L10_C2_B3_NB024_MC_B_01, s, 1)
        assert "Điểm nào sau đây thuộc miền nghiệm đó?" in debai and not DIEM.search(debai)
        gach, bo, lien = _doc_hinh(hinh)
        lc = [_diem(dap)[0]] + [_diem(t)[0] for t in nhieu]
        assert len(nhieu) == 3 and len(set(lc)) == 4
        assert [_thuoc_hinh(p, gach, bo, lien) for p in lc] == [True, False, False, False], (s, lc)
        assert all(_trong_khung(p, hinh) for p in lc)
        bay_tren_bo += any(_tren_bo(p, bo) for p in lc)
    assert bay_tren_bo > SO_LAN // 10


def test_th024_sa_b_dem_theo_hinh():
    thay = set()
    for s in range(SO_LAN):
        debai, dap, nhieu, giai, hinh = _bat(M.L10_C2_B3_NB024_SA_B_01, s, 2)
        ds = _diem(debai)
        assert len(ds) == 5 and len(set(ds)) == 5 and "có bao nhiêu điểm thuộc miền nghiệm đó?" in debai
        gach, bo, lien = _doc_hinh(hinh)
        k = sum(_thuoc_hinh(p, gach, bo, lien) for p in ds)
        assert int(dap) == k and 1 <= k <= 4, (s, debai)
        assert dap not in nhieu and "Vậy có $%d$ điểm." % k in giai
        thay.add(k)
    assert thay == {1, 2, 3, 4}


def test_th024_hinh_dung_voi_loi_giai():
    """Bat phuong trinh ket luan trong loi giai dung voi hinh (kiem them, doc lap voi dap so)."""
    for s in range(100):
        for ham, dang in ((M.L10_C2_B3_NB024_MC_B_01, 1), (M.L10_C2_B3_NB024_SA_B_01, 2)):
            debai, dap, nhieu, giai, hinh = _bat(ham, s, dang)
            gach, bo, lien = _doc_hinh(hinh)
            lhs, dau, c = re.search(r"bất phương trình \$(.+?) (\\le|\\ge|<|>) (-?\d+)\$\.", giai).groups()
            a, b = _he_so(lhs)
            assert lien == (dau in (r"\le", r"\ge"))
            for p in [(i, j) for i in range(-7, 8) for j in range(-7, 8)]:
                if not _trong_khung(p, hinh):
                    continue
                assert _thuoc_hinh(p, gach, bo, lien) == THOA[dau](a * p[0] + b * p[1], int(c)), (s, p)


# ------------------------------------------------------------------ he bat phuong trinh
def _he_so(lhs):
    e = parse_expr(lhs.replace(" ", ""), transformations=standard_transformations + (implicit_multiplication_application,),
                   local_dict={"x": X, "y": Y})
    return int(e.coeff(X)), int(e.coeff(Y))


def _doc_he(debai):
    he = re.search(r"\\heva\{(.+?)\}\$", debai).group(1)
    ra = []
    for dong in he.split(r"\\"):
        lhs, dau, c = re.match(r"\s*& (.+?) (\\le|\\ge|<|>) (-?\d+)\s*$", dong).groups()
        a, b = _he_so(lhs)
        assert (a, b) != (0, 0)
        ra.append((a, b, int(c), dau))
    assert len(ra) in (2, 3)
    return ra


def _thuoc_he(he, p):
    return all(THOA[d](a * p[0] + b * p[1], c) for a, b, c, d in he)


def test_th027_mc_c_diem_thuoc_he():
    for s in range(SO_LAN):
        debai, dap, nhieu, giai, hinh = _bat(M.L10_C2_B4_VD027_MC_B_01, s, 1)
        assert debai.startswith("Điểm nào sau đây thuộc miền nghiệm của hệ bất phương trình") and hinh == 0
        he = _doc_he(debai)
        lc = [_diem(dap)[0]] + [_diem(t)[0] for t in nhieu]
        assert len(set(lc)) == 4
        assert [_thuoc_he(he, p) for p in lc] == [True, False, False, False], (s, debai)
        # khong co hai bo song song / trung nhau
        assert all(a1 * b2 - b1 * a2 for i, (a1, b1, _c1, _d1) in enumerate(he) for a2, b2, _c2, _d2 in he[i + 1:])


def test_th027_sa_c_dem_diem_thuoc_he():
    thay = set()
    for s in range(SO_LAN):
        debai, dap, nhieu, giai, hinh = _bat(M.L10_C2_B4_VD027_SA_B_01, s, 2)
        he = _doc_he(debai)
        ds = _diem(debai.split(r"\heva")[1])
        assert len(ds) == 5 and len(set(ds)) == 5
        k = sum(_thuoc_he(he, p) for p in ds)
        assert int(dap) == k and 1 <= k <= 4 and dap not in nhieu
        thay.add(k)
    assert thay == {1, 2, 3, 4}


def test_dung_loai_cau():
    for s in range(30):
        for ham in (M.L10_C2_B3_NB024_MC_B_01, M.L10_C2_B4_VD027_MC_B_01, M.L10_C2_B4_TH027_MC_B_01):
            M._rd.seed(s)
            o = ham(1)
            assert r"\choice" in o and r"\shortans" not in o and o.count(r"\True") == 1
        for ham in (M.L10_C2_B3_NB024_SA_B_01, M.L10_C2_B4_VD027_SA_B_01, M.L10_C2_B4_TH027_SA_B_01):
            M._rd.seed(s)
            o = ham(1)
            assert r"\shortans" in o and r"\choice" not in o
        M._rd.seed(s)
        assert M.L10_C2_B3_NB024_MC_B_01(3).count(r"\begin{ex}") == 3


# ------------------------------------------------------------------ hinh mien nghiem cua HE (TH027_MC_B / SA_B)
def _doc_hinh_he(tikz):
    """[(da giac bi gach, bo, net lien?)] theo thu tu trong hinh (moi \\fill di lien voi \\draw bo ngay sau)."""
    fills = re.findall(r"\\fill\[pattern=north east lines\] (.+?) -- cycle;", tikz)
    bos = re.findall(r"\\draw\[(dashed,)?thick\] \((-?[\d.]+),(-?[\d.]+)\)--\((-?[\d.]+),(-?[\d.]+)\);", tikz)
    assert len(fills) == len(bos) == 2
    ra = []
    for f, b in zip(fills, bos):
        gach = [tuple(map(float, p)) for p in re.findall(r"\((-?[\d.]+),(-?[\d.]+)\)", f)]
        ra.append((gach, ((float(b[1]), float(b[2])), (float(b[3]), float(b[4]))), b[0] == ""))
    return ra


def _thuoc_hinh_he(p, cac):
    return all(_thuoc_hinh(p, g, bo, lien) for g, bo, lien in cac)


def test_th027_mc_b_doc_hinh_he():
    for s in range(SO_LAN):
        debai, dap, nhieu, giai, hinh = _bat(M.L10_C2_B4_TH027_MC_B_01, s, 1)
        assert "miền nghiệm của một hệ bất phương trình" in debai and not DIEM.search(debai)
        cac = _doc_hinh_he(hinh)
        lc = [_diem(dap)[0]] + [_diem(t)[0] for t in nhieu]
        assert len(set(lc)) == 4 and all(_trong_khung(p, hinh) for p in lc)
        assert [_thuoc_hinh_he(p, cac) for p in lc] == [True, False, False, False], (s, lc)


def test_th027_sa_b_dem_theo_hinh_he():
    thay = set()
    for s in range(SO_LAN):
        debai, dap, nhieu, giai, hinh = _bat(M.L10_C2_B4_TH027_SA_B_01, s, 2)
        ds = _diem(debai)
        assert len(ds) == 5 and len(set(ds)) == 5
        k = sum(_thuoc_hinh_he(p, _doc_hinh_he(hinh)) for p in ds)
        assert int(dap) == k and 1 <= k <= 4 and dap not in nhieu, (s, debai)
        thay.add(k)
    assert thay == {1, 2, 3, 4}


def test_th027_hinh_he_dung_voi_loi_giai():
    for s in range(100):
        for ham, dang in ((M.L10_C2_B4_TH027_MC_B_01, 1), (M.L10_C2_B4_TH027_SA_B_01, 2)):
            debai, dap, nhieu, giai, hinh = _bat(ham, s, dang)
            he = _doc_he(re.search(r"miền nghiệm của hệ (\$\\heva\{.+?\}\$)", giai).group(1))
            cac = _doc_hinh_he(hinh)
            for p in [(i, j) for i in range(-8, 9) for j in range(-8, 9)]:
                if _trong_khung(p, hinh):
                    assert _thuoc_hinh_he(p, cac) == _thuoc_he(he, p), (s, p)
