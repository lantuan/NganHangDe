# -*- coding: utf-8 -*-
"""Chuong 3 lop 10 - cac cau SA/MC bo sung 15/10/2026 (co Lan: "ghep cac dang da thay giong, cung dang; cac dang
thieu lam bo sung luon").

Moi dap so duoc TINH LAI DOC LAP tu chinh van ban de bai (doc LaTeX bang tests/_tinh_tex.py, dung tam giac dung bang
toa do rieng cua test), KHONG dung lai ham sinh de. Cau dem khang dinh: tinh chan tri tung khang dinh roi dem.
"""
import importlib.util
import math
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC / "tests"))
from _tinh_tex import bang, so, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C3_sa_bo_sung", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_sa_bo_sung"] = M
_spec.loader.exec_module(M)

SO_LAN = 200
P = "L10_C3_"
DAP_SO = re.compile(r"^-?\d+(,\d+)?$")


def _bat(ten, seed, dang=2):
    """Chay ham voi seed, bat (debai, dapso, dsnhieu, giai) truyen vao MC_SA_answer_const."""
    cap = []
    goc = M.MC_SA_answer_const
    M.MC_SA_answer_const = lambda debai, dap, nhieu, giai, *a, **k: cap.append((debai, str(dap), nhieu, giai)) or ""
    try:
        random.seed(seed)
        getattr(M, P + ten)(1, dang=dang)
    finally:
        M.MC_SA_answer_const = goc
    assert len(cap) == 1
    return cap[0]


def _muc(debai):
    """Cac muc '1. ...' cua cau dem (moi muc mot dong sau \\\\)."""
    return [m.group(1).strip() for m in re.finditer(r"\\\\ \d\. (.+?)(?=\\\\ \d\. |\\\\ Có bao|$)", debai)]


def _hoi_dung(debai):
    if r"\textbf{sai}" in debai:
        return False
    return True


# ---------------------------------------------------------------- tam giac dung bang toa do (doc lap voi ham sinh)
def _tam_giac(tu=None):
    """Tam giac ngau nhien tu ba diem; tu = 'A'/'B'/'C' de goc do tu, 'nhon' de ca ba goc nhon."""
    while True:
        Ax, Ay = 0.0, 0.0
        Bx, By = random.uniform(3, 9), 0.0
        Cx, Cy = random.uniform(-4, 12), random.uniform(1.5, 8)
        a, b, c = math.dist((Bx, By), (Cx, Cy)), math.dist((Ax, Ay), (Cx, Cy)), math.dist((Ax, Ay), (Bx, By))
        A = math.acos((b * b + c * c - a * a) / (2 * b * c))
        B = math.acos((a * a + c * c - b * b) / (2 * a * c))
        C = math.pi - A - B
        g = {"A": A, "B": B, "C": C}
        if min(g.values()) < 0.2 or min(abs(x - math.pi / 2) for x in g.values()) < 0.05:
            continue
        if tu == "nhon" and max(g.values()) >= math.pi / 2:
            continue
        if tu in ("A", "B", "C") and g[tu] <= math.pi / 2:
            continue
        S = abs((Bx - Ax) * (Cy - Ay) - (Cx - Ax) * (By - Ay)) / 2
        p = (a + b + c) / 2
        R = a * b * c / (4 * S)
        tb = lambda X, Y: ((X[0] + Y[0]) / 2, (X[1] + Y[1]) / 2)
        return dict(a=a, b=b, c=c, A=A, B=B, C=C, S=S, p=p, R=R, r=S / p, ha=2 * S / a, hb=2 * S / b, hc=2 * S / c,
                    ma=math.dist((Ax, Ay), tb((Bx, By), (Cx, Cy))), mb=math.dist((Bx, By), tb((Ax, Ay), (Cx, Cy))),
                    mc=math.dist((Cx, Cy), tb((Ax, Ay), (Bx, By))))


def _dung_tren_tam_giac(muc, so_lan=5, **kw):
    """Chan tri cua 've trai = ve phai' tren nhieu tam giac ngau nhien."""
    tex = muc.strip("$")
    l, r = tex.split(" = ")
    return all(bang(tinh(l, **T), tinh(r, **T)) for T in (_tam_giac(**kw) for _ in range(so_lan)))


def _dem_kiem(debai, dap, chan_tri):
    ds = _muc(debai)
    assert len(ds) == 4, debai
    assert len(set(ds)) == 4
    tri = [chan_tri(x) for x in ds]
    so_dung = sum(tri)
    assert 1 <= so_dung <= 3
    assert dap == str(so_dung if _hoi_dung(debai) else 4 - so_dung), (debai, tri)


# ---------------------------------------------------------------- moi ham moi: dung loai SA, dap so la so
TAT_CA_SA = ["B5_NB029_SA_A_01", "B5_NB029_SA_C_01", "B5_NB029_SA_D_01", "B5_NB029_SA_E_01", "B5_NB029_SA_H_01",
             "B5_NB029_SA_I_01", "B5_TH030_SA_A_01", "B5_TH030_SA_C_01", "B5_TH031_SA_A_01", "B5_TH031_SA_B_01",
             "B5_TH031_SA_D_01", "B5_TH031_SA_F_01", "B6_TH032_SA_D_01", "B6_TH032_SA_D_02", "B6_NB032_SA_A_01",
             "B6_NB032_SA_B_01", "B6_NB033_SA_A_01", "B6_TH034_SA_B_01", "B6_TH034_SA_C_01", "B6_TH034_SA_F_01",
             "B6_NB034_SA_A_01", "B6_TH035_SA_C_01", "B6_VD032_SA_A_01", "B6_VD036_SA_B_01",
             "B6_TH033_SA_C_01", "B6_NB034_SA_B_01"]


@pytest.mark.parametrize("ten", TAT_CA_SA)
def test_sa_moi_dung_loai(ten):
    for s in range(SO_LAN):
        random.seed(s)
        out = getattr(M, P + ten)(1)
        assert r"\shortans" in out and r"\choice" not in out
        debai, dap, nhieu, _ = _bat(ten, s)
        assert DAP_SO.match(dap), (ten, dap)
        assert "\\item" not in debai


# ---------------------------------------------------------------- MC goi lai SA: cung dap so
@pytest.mark.parametrize("mc,sa", [("B5_NB029_MC_J_01", "B5_NB029_SA_J_01"), ("B5_NB029_MC_J_02", "B5_NB029_SA_J_02"),
                                   ("B5_TH030_MC_N_01", "B5_TH030_SA_N_01"), ("B5_TH030_MC_N_02", "B5_TH030_SA_N_02"),
                                   ("B6_VD036_MC_Z_01", "B6_VD036_SA_Z_01"), ("B6_VD036_MC_Z_02", "B6_VD036_SA_Z_02"),
                                   ("B6_VD036_MC_Z_03", "B6_VD036_SA_Z_03"), ("B6_VD036_MC_X_01", "B6_VD036_SA_X_01"),
                                   ("B6_VD036_MC_X_02", "B6_VD036_SA_X_02")])
def test_mc_cung_dang_voi_sa(mc, sa):
    for s in range(60):
        random.seed(s)
        o_mc = getattr(M, P + mc)(1)
        random.seed(s)
        o_sa = getattr(M, P + sa)(1)
        assert r"\choice" in o_mc and r"\shortans" not in o_mc
        dung = re.search(r"\{\\True \$?\s*([^${}]*?)\s*\$?\}", o_mc).group(1)
        sa_dap = re.search(r"\\shortans\{\s*\$?\s*([^${}]*?)\s*\$?\}", o_sa).group(1)
        assert dung == sa_dap
        # cung de bai (bo phan dap an)
        assert o_mc.split(r"\choice")[0].strip() == o_sa.split(r"\shortans")[0].strip()


# ---------------------------------------------------------------- tung dang
def test_nb029_sa_a_bieu_thuc():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_NB029_SA_A_01", s)
        bt = re.search(r"\$A = (.+)\$", debai).group(1)
        assert bang(tinh(bt), so(dap))


def test_nb029_sa_c_toa_do():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_NB029_SA_C_01", s)
        sn = so(re.search(r"\\sin\\widehat\{xOM\} = (-?[\d,]+)", debai).group(1))
        cs = so(re.search(r"\\cos\\widehat\{xOM\} = (-?[\d,]+)", debai).group(1))
        assert abs(sn * sn + cs * cs - 1) < 1e-9 and sn > 0
        assert so(dap) == (cs if "hoành độ" in debai else sn)


def test_nb029_sa_d_co_the_xay_ra():
    def co_the(m):
        h, v = re.match(r"\$\\(sin|cos|tan|cot)\\alpha = (.+)\$", m).groups()
        x = tinh(v)
        return {"sin": 0 <= x <= 1, "cos": -1 <= x <= 1}.get(h, True)
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_NB029_SA_D_01", s)
        ds = _muc(debai)
        assert dap == str(sum(co_the(m) for m in ds))


def test_nb029_sa_e_dau():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_NB029_SA_E_01", s)
        lo, hi = map(int, re.search(r"\$(\d+)\^\{\\circ\} < \\alpha < (\d+)\^\{\\circ\}\$", debai).groups())
        al = math.radians((lo + hi) / 2 + 7)

        def tri(m):
            e, d = re.match(r"\$(.+) ([<>]) 0\$", m).groups()
            v = tinh(e, al=al)
            return v > 0 if d == ">" else v < 0
        _dem_kiem(debai, dap, tri)


def test_nb029_sa_h_goc_dac_biet():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_NB029_SA_H_01", s)
        _dem_kiem(debai, dap, lambda m: bang(*[tinh(x) for x in m.strip("$").split(" = ")]))


def test_nb029_sa_i_dau_trong_tam_giac():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_NB029_SA_I_01", s)
        mt = re.search(r"có góc \$([ABC])\$ tù", debai)
        kieu = mt.group(1) if mt else "nhon"
        assert mt or "nhọn" in debai

        def tri(m):
            e, d = re.match(r"\$(.+) ([<>]) 0\$", m).groups()
            T = _tam_giac(kieu)
            v = tinh(e, **T)
            return v > 0 if d == ">" else v < 0
        _dem_kiem(debai, dap, tri)


def test_th030_sa_a_may_tinh():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_TH030_SA_A_01", s)
        bt = re.search(r"tính \$(.+?)\$", debai).group(1)
        assert so(dap) == round(tinh(bt), 2)


def test_th030_sa_c_khang_dinh_may_tinh():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_TH030_SA_C_01", s)

        def tri(m):
            l, r = m.strip("$").split(r" \approx ")
            return abs(round(tinh(l), 2) - so(r)) < 1e-9
        _dem_kiem(debai, dap, tri)


def test_th031_sa_a_bu_phu():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_TH031_SA_A_01", s)
        if "tam giác" in debai:
            _dem_kiem(debai, dap, lambda m: _dung_tren_tam_giac(m))
        else:
            def tri(m):
                l, r = m.strip("$").split(" = ")
                return all(bang(tinh(l, al=a), tinh(r, al=a)) for a in (0.3, 0.7, 1.2))
            _dem_kiem(debai, dap, tri)


def test_th031_sa_b_doi_xung_oy():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_TH031_SA_B_01", s)
        x, y = map(so, re.search(r"M\\left\((-?[\d,]+); (-?[\d,]+)\\right\)", debai).groups())
        h = re.search(r"Tính \$\\(sin|cos|tan|cot)\\widehat\{xON\}", debai).group(1)
        nx, ny = -x, y                                         # N doi xung M qua Oy, nam tren nua duong tron
        v = {"sin": ny, "cos": nx, "tan": ny / nx, "cot": nx / ny}[h]
        assert abs(so(dap) - v) < 1e-9


def test_th031_sa_d_gia_tri_gan_dung():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_TH031_SA_D_01", s)
        cho, v = re.search(r"Biết \$(.+?) \\approx (-?[\d,]+)\$", debai).groups()
        hoi = re.search(r"của \$(.+?)\$", debai).group(1)
        assert so(v) == round(tinh(cho), 2)
        k = tinh(hoi) / tinh(cho)                             # quan he phu / bu: hai gia tri bang nhau hoac doi nhau
        assert abs(abs(k) - 1) < 1e-9
        assert abs(so(dap) - round(k) * so(v)) < 1e-9


def test_th031_sa_f_tam_giac_vuong():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B5_TH031_SA_F_01", s)
        assert "vuông tại $B$" in debai
        h, v = re.search(r"\$\\(sin|cos) C = ([\d,]+)\$", debai).groups()
        g = re.search(r"Tính \$\\(sin|cos) A\$", debai).group(1)
        C = math.asin(so(v)) if h == "sin" else math.acos(so(v))
        A = math.pi / 2 - C
        assert abs(so(dap) - (math.sin(A) if g == "sin" else math.cos(A))) < 1e-9


@pytest.mark.parametrize("ten", ["B6_TH032_SA_D_01", "B6_TH032_SA_D_02"])
def test_th032_sa_d_he_thuc_ra_goc(ten):
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat(ten, s)
        ht = re.search(r"thoả mãn \$(.+?)\$\.", debai).group(1)
        X = re.search(r"Số đo góc \$([ABC])\$", debai).group(1)
        doi, k1, k2 = {"A": ("a", "b", "c"), "B": ("b", "c", "a"), "C": ("c", "a", "b")}[X]
        l, r = ht.split(" = ")
        for _ in range(5):                                    # tam giac co goc X = dap: he thuc phai dung
            u, w = random.uniform(2, 9), random.uniform(2, 9)
            g = math.radians(int(dap))
            d = math.sqrt(u * u + w * w - 2 * u * w * math.cos(g))
            T = {doi: d, k1: u, k2: w}
            assert bang(tinh(l, **T), tinh(r, **T)), (debai, dap)


def test_th032_sa_e_dinh_li_cosin():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_NB032_SA_A_01", s)
        _dem_kiem(debai, dap, _dung_tren_tam_giac)


def test_th032_sa_f_trung_tuyen():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_NB032_SA_B_01", s)
        _dem_kiem(debai, dap, _dung_tren_tam_giac)


def test_th033_sa_c_dinh_li_sin():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_NB033_SA_A_01", s)
        _dem_kiem(debai, dap, _dung_tren_tam_giac)


def test_th034_sa_g_cong_thuc():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_NB034_SA_A_01", s)
        _dem_kiem(debai, dap, _dung_tren_tam_giac)


def _ba_canh(debai):
    return [int(x) for x in re.search(r"\$BC = (\d+)\$, \$CA = (\d+)\$, \$AB = (\d+)\$", debai).groups()]


def _heron(a, b, c):
    """Dien tich bang toa do (dat B, C tren truc hoanh) - doc lap voi cong thuc Heron cua ham sinh."""
    x = (c * c - b * b + a * a) / (2 * a)                     # A(x; y), B(0; 0), C(a; 0)
    y = math.sqrt(c * c - x * x)
    return a * y / 2


def test_th034_sa_b_heron():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_TH034_SA_B_01", s)
        assert abs(_heron(*_ba_canh(debai)) - int(dap)) < 1e-7


def test_th034_sa_c_goc_tu_dien_tich():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_TH034_SA_C_01", s)
        c, b = map(int, re.search(r"\$AB = (\d+)\$, \$AC = (\d+)\$", debai).groups())
        S = tinh(re.search(r"\$S = (.+?)\$", debai).group(1))
        sa = 2 * S / (b * c)
        g = math.degrees(math.asin(min(1.0, sa)))
        g = 180 - g if "tù" in debai else g
        assert abs(g - int(dap)) < 1e-6


def test_th034_sa_f_duong_cao():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_TH034_SA_F_01", s)
        if "$BC = " in debai:
            a, b, c = _ba_canh(debai)
            h = 2 * _heron(a, b, c) / a
        else:
            c, b = map(int, re.search(r"\$AB = (\d+)\$, \$AC = (\d+)\$", debai).groups())
            g = math.radians(int(re.search(r"widehat\{BAC\} = (\d+)\^", debai).group(1)))
            B, C = (c, 0.0), (b * math.cos(g), b * math.sin(g))          # A goc toa do
            h = abs(B[0] * C[1] - B[1] * C[0]) / math.dist(B, C)        # khoang cach tu A toi BC
        assert so(dap) == round(h, 2)


def test_th035_sa_c_nhan_dang():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_TH035_SA_C_01", s)
        bo = [tuple(map(int, m)) for m in re.findall(r"\d\. \$(\d+)\$, \$(\d+)\$, \$(\d+)\$", debai)]
        hoi = re.search(r"tam giác \\textbf\{(nhọn|vuông|tù)\}", debai).group(1)
        assert len(bo) == 4

        def loai(t):
            x, y, z = sorted(t)
            assert x + y > z
            gmax = math.degrees(math.acos((x * x + y * y - z * z) / (2 * x * y)))
            return "vuông" if abs(gmax - 90) < 1e-9 else ("tù" if gmax > 90 else "nhọn")
        assert dap == str(sum(loai(t) == hoi for t in bo))
        assert 1 <= int(dap) <= 3


def test_vd032_sa_a_hinh_binh_hanh():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_VD032_SA_A_01", s)
        ab, ac, bd = map(int, re.search(r"\$AB = (\d+)\$ và hai đường chéo \$AC = (\d+)\$, \$BD = (\d+)\$", debai).groups())
        oa, ob = ac / 2, bd / 2                                 # tam giac OAB -> goc AOB; tam giac OAD co goc bu
        cos_aob = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
        assert -1 < cos_aob < 1
        ad = math.sqrt(oa * oa + ob * ob + 2 * oa * ob * cos_aob)
        assert so(dap) == round(ad, 1)


def test_vd036_sa_b_dam_lay():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_VD036_SA_B_01", s)
        b = int(re.search(r"\$AC = (\d+)\\,", debai).group(1))
        A = math.radians(int(re.search(r"BAC\} = (\d+)\^", debai).group(1)))
        C = math.radians(int(re.search(r"BCA\} = (\d+)\^", debai).group(1)))
        # A(0;0), C(b;0); B la giao cua hai tia tu A (goc A) va tu C (goc C, phia tren)
        ua, uc = (math.cos(A), math.sin(A)), (-math.cos(C), math.sin(C))
        t = (b * uc[1]) / (ua[0] * uc[1] - ua[1] * uc[0])
        assert so(dap) == round(t, 2)


def test_th033_sa_c_ti_so():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_TH033_SA_C_01", s)
        A, B = (math.radians(int(x)) for x in re.search(r"widehat\{A\} = (\d+)\^.*widehat\{B\} = (\d+)\^", debai).groups())
        # tam giac dung bang toa do: A(0;0), B(1;0), C la giao hai tia -> BC/CA
        ua, ub = (math.cos(A), math.sin(A)), (-math.cos(B), math.sin(B))
        t = ub[1] / (ua[0] * ub[1] - ua[1] * ub[0])            # C = t.ua
        C = (t * ua[0], t * ua[1])
        assert so(dap) == round(math.dist((1, 0), C) / math.dist((0, 0), C), 2)


def test_nb034_sa_b_cong_thuc_va_du_kien():
    for s in range(SO_LAN):
        debai, dap, _, _ = _bat("B6_NB034_SA_B_01", s)

        def tri(m):
            dk, ct = re.match(r"Biết (.+) thì \$(.+)\$$", m).groups()
            biet = set()
            if "ba cạnh" in dk:
                biet |= set("abcp")                              # biet ba canh thi biet nua chu vi
            for ten, k in (("cạnh $a$", "a"), ("$b$", "b"), ("$c$", "c"), ("nửa chu vi $p$", "p"), ("bán kính $R$", "R"),
                           ("bán kính $r$", "r"), ("góc $A$", "A"), ("góc $C$", "C"), ("$h_a$", "ha"), ("$a$, $b$", "ab")):
                if ten in dk:
                    biet |= set(k) if k != "ha" else {"ha"}
            l, r = ct.split(" = ")
            sach = r.replace("h_a", "")
            for lenh in ("\\sin", "\\cos", "\\sqrt", "\\dfrac", "\\left", "\\right", "\\cdot"):
                sach = sach.replace(lenh, "")
            can = set(re.findall(r"[abcpRrAC]", sach)) | ({"ha"} if "h_a" in r else set())
            dung_ct = _dung_tren_tam_giac("$" + ct + "$")
            return dung_ct and can <= biet
        _dem_kiem(debai, dap, tri)
