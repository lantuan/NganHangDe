# -*- coding: utf-8 -*-
r"""Kiem chung cac ham tra loi ngan (SA) bo sung cho chuong 1 lop 10 ngay 15/10/2026.

Quy tac cua co Lan: cai nao khong kiem chung duoc thi bo qua. Moi ham SA moi o day deu duoc kiem lai DOC LAP voi
code sinh de:
  * dung loai cau (co \shortans, khong co \choice, khong co \item);
  * dap so trong \shortans trung voi dap so tinh lai tu chinh noi dung de (doc ngược bang regex) hoac bang phep tinh
    doc lap (brute force, sympy).
"""
import itertools
import math
import pathlib
import random
import re
import sys

import numpy as np
import pytest
from sympy import N as sym_N, sqrt as sym_sqrt, pi as sym_pi, Rational, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

GOC = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from toan10 import L10_C1 as m  # noqa: E402

CAC_SA_MOI = [
    "L10_C1_B1_NB001_SA_B_01", "L10_C1_B1_NB001_SA_C_01",
    "L10_C1_B1_TH003_SA_B_01", "L10_C1_B1_TH003_SA_C_01", "L10_C1_B1_TH003_SA_D_01", "L10_C1_B1_TH003_SA_D_02",
    "L10_C1_B1_VD014_SA_C_01", "L10_C1_B1_VD014_SA_D_01", "L10_C1_B1_VD014_SA_D_02",
    "L10_C1_B2_NB017_SA_B_01", "L10_C1_B2_NB017_SA_C_01", "L10_C1_B2_NB017_SA_E_01", "L10_C1_B2_NB017_SA_G_01",
    "L10_C1_B2_NB017_SA_H_01", "L10_C1_B2_NB017_SA_H_02",
    "L10_C1_B2_TH018_SA_B_01", "L10_C1_B2_TH018_SA_B_02", "L10_C1_B2_TH018_SA_B_03", "L10_C1_B2_TH018_SA_B_04",
    "L10_C1_B2_TH018_SA_D_01",
    "L10_C1_B2_NB017_SA_I_01", "L10_C1_B2_VD021_SA_B_01", "L10_C1_B2_VD021_SA_C_01",
]


def _sinh(ten, seed, socau=1):
    random.seed(seed)
    np.random.seed(seed)
    return getattr(m, ten)(socau, 2)


def _dap(out):
    kq = re.search(r"\\shortans\{\s*\$?(-?\d+)\$?\s*\}", out)
    assert kq, out[:300]
    return int(kq.group(1))


@pytest.mark.parametrize("ten", CAC_SA_MOI)
def test_la_cau_tra_loi_ngan(ten):
    for sd in range(120):
        out = _sinh(ten, sd, 2)
        assert out.count("\\begin{ex}") == 2
        assert "\\shortans" in out and "\\choice" not in out and "\\item" not in out.split("\\loigiai")[0]


# Ham dung kho xoay vong (nho cau da ra trong sys.modules) thi cung seed KHONG cho cung de - do chu y, nen bo ra.
CO_XOAY_VONG = {"L10_C1_B2_NB017_SA_H_02"}


@pytest.mark.parametrize("ten", [t for t in CAC_SA_MOI if t not in CO_XOAY_VONG])
def test_cung_seed_cung_de(ten):
    assert _sinh(ten, 7, 2) == _sinh(ten, 7, 2)


# ---------------------------------------------------------------- NB001_SA_C, TH003_SA_D: dem gia tri x
def _so_sanh(dau, v, c):
    return {">": v > c, "<": v < c, r"\geq": v >= c, r"\leq": v <= c, "=": v == c}[dau]


def test_nb001_sa_c_dap_so():
    for sd in range(300):
        out = _sinh("L10_C1_B1_NB001_SA_C_01", sd)
        kq = re.search(r"P\(x\)\\colon x (>|<|\\geq|\\leq) (-?\d+)\$\. Trong các giá trị \$x \\in \\left\\\{([^}]*)\\right\\\}\$.*?làm cho \$P\(x\)\$ là mệnh đề (đúng|\\textbf\{sai\})\?", out)
        assert kq, out[:400]
        dau, c, tap, loai = kq.group(1), int(kq.group(2)), kq.group(3), kq.group(4)
        gt = [int(v) for v in tap.split(";")]
        so_dung = sum(1 for v in gt if _so_sanh(dau, v, c))
        mong_doi = so_dung if loai == "đúng" else len(gt) - so_dung
        assert 1 <= mong_doi <= len(gt) - 1
        assert _dap(out) == mong_doi


def test_th003_sa_d_01_dap_so():
    mau = re.compile(r"P\(x\)\\colon (.+?) (>|<|\\geq|\\leq|=) (-?\d+)\$\. Trong các giá trị \$x \\in \\left\\\{([^}]*)\\right\\\}\$.*?là mệnh đề (đúng|\\textbf\{sai\})\?")
    for sd in range(300):
        out = _sinh("L10_C1_B1_TH003_SA_D_01", sd)
        kq = mau.search(out)
        assert kq, out[:400]
        bt, dau, c, tap, loai = kq.group(1), kq.group(2), int(kq.group(3)), kq.group(4), kq.group(5)
        py = bt.replace(r"\left|x\right|", "abs(x)").replace(r"\left(", "(").replace(r"\right)", ")")
        py = py.replace("^{2}", "**2").replace("^{3}", "**3")
        py = re.sub(r"(\d|\))\s*(?=\()", r"\1*", py)
        gt = [int(v) for v in tap.split(";")]
        so_dung = sum(1 for x in gt if _so_sanh(dau, eval(py, {"abs": abs}, {"x": x}), c))
        mong_doi = so_dung if loai == "đúng" else len(gt) - so_dung
        assert _dap(out) == mong_doi, (bt, dau, c, gt, loai, _dap(out), mong_doi)


def test_th003_sa_d_02_dap_so():
    mau = re.compile(r"P\(x\)\\colon \\(sin|cos|tan) x (>|<|\\geq|\\leq|=) (.+?)\$ với.*?là mệnh đề (đúng|\\textbf\{sai\})\?")
    gtri = {"0": 0.0, r"\dfrac{1}{2}": 0.5, r"\dfrac{\sqrt{2}}{2}": math.sqrt(2) / 2, r"\dfrac{\sqrt{3}}{2}": math.sqrt(3) / 2,
            "1": 1.0, r"\dfrac{\sqrt{3}}{3}": math.sqrt(3) / 3, r"\sqrt{3}": math.sqrt(3)}
    ham = {"sin": math.sin, "cos": math.cos, "tan": math.tan}
    for sd in range(300):
        out = _sinh("L10_C1_B1_TH003_SA_D_02", sd)
        kq = mau.search(out)
        assert kq, out[:500]
        f, dau, c_tex, loai = kq.group(1), kq.group(2), kq.group(3), kq.group(4)
        c = gtri[c_tex]
        goc = [0, 30, 45, 60, 90] if f != "tan" else [0, 30, 45, 60]
        dung = {">": lambda v: v > c + 1e-9, "<": lambda v: v < c - 1e-9, r"\geq": lambda v: v >= c - 1e-9,
                r"\leq": lambda v: v <= c + 1e-9, "=": lambda v: abs(v - c) < 1e-9}[dau]
        so_dung = sum(1 for g in goc if dung(ham[f](math.radians(g))))
        mong_doi = so_dung if loai == "đúng" else len(goc) - so_dung
        assert _dap(out) == mong_doi, (f, dau, c_tex, loai)


# ---------------------------------------------------------------- TH003_SA_C: kho khang dinh bang sympy
def test_th003_kho_khang_dinh_dung_sai_theo_sympy():
    """Moi khang dinh trong kho `_th003_c_kho` duoc kiem bang sympy chinh xac (khong dung so thuc)."""
    for mm in [v for v in range(2, 40) if math.isqrt(v) ** 2 != v]:
        for k in range(1, 6):
            a, b = sym_sqrt(mm) + k, sym_sqrt(mm) - k
            dung, sai = m._th003_c_kho(mm, k)
            # thu tu cua kho: xem dinh nghia _th003_c_kho
            gt_dung = [simplify(a**2 + b**2 - 2 * (mm + k * k)) == 0, simplify(a * b - (mm - k * k)) == 0,
                       simplify(a - b - 2 * k) == 0, simplify((a + b)**2 - 4 * mm) == 0,
                       simplify(a**2 + b**2).is_integer and simplify(a**2 + b**2) >= 0]
            gt_sai = [simplify(a + b).is_rational is True, simplify(a * b - (mm + k * k)) == 0,
                      simplify(a**2 + b**2 - (mm + k * k)) == 0, simplify(a - b - 2 * sym_sqrt(mm)) == 0,
                      simplify((a - b)**2 - 4 * mm) == 0]
            assert all(gt_dung), (mm, k, gt_dung)
            assert not any(gt_sai), (mm, k, gt_sai)
            assert len(dung) == len(gt_dung) and len(sai) == len(gt_sai)


def test_th003_sa_c_dap_so_dem_lai():
    """Doc lai de: dem so 'dung' trong bon dong 'a) ...' bang cach tra ve kho."""
    for sd in range(200):
        out = _sinh("L10_C1_B1_TH003_SA_C_01", sd)
        kq = re.search(r"a = \\sqrt\{(\d+)\} \+ (\d+)\$", out)
        mm, k = int(kq.group(1)), int(kq.group(2))
        dung, sai = m._th003_c_kho(mm, k)
        tap_dung = {t for t, _ in dung}
        de = out.split("\\loigiai")[0]
        cac = re.findall(r"[a-d]\) (\$[^\n]*?\$)(?:\\\\|\n)", de.replace("\\\\ ", "\\\\\n"))
        assert len(cac) == 4, de
        so_dung = sum(1 for c in cac if c in tap_dung)
        hoi = "đúng" if re.search(r"có bao nhiêu khẳng định đúng", de) else "sai"
        assert _dap(out) == (so_dung if hoi == "đúng" else 4 - so_dung)


# ---------------------------------------------------------------- VD014_SA_C: kiem lai _md_bdt bang sympy
_TRANS = standard_transformations + (implicit_multiplication_application,)


def _vt(tex):
    s = tex.replace(r"\sqrt", "sqrt").replace(r"\pi", "pi").replace(r"\cdot", "*").replace("{", "(").replace("}", ")")
    s = s.replace("^", "**")
    return parse_expr(s, transformations=_TRANS, local_dict={"sqrt": sym_sqrt, "pi": sym_pi})


def _chan_tri_bdt(tex):
    r"""Tinh lai chan tri cua `P => Q` hoac `P <=> Q` (hai ve la bat dang thuc so) bang sympy, 30 chu so."""
    ki = r"\Leftrightarrow" if r"\Leftrightarrow" in tex else r"\Rightarrow"
    P, Q = [x.strip() for x in tex.split(ki)]

    def dung(bdt):
        mm = re.match(r"(.+?)\s*(<|>)\s*(.+)", bdt)
        l, dau, r = _vt(mm.group(1)), mm.group(2), _vt(mm.group(3))
        d = sym_N(l - r, 40)
        return d < 0 if dau == "<" else d > 0
    p, q = dung(P), dung(Q)
    return (p == q) if ki == r"\Leftrightarrow" else ((not p) or q)


def test_md_bdt_chan_tri_theo_sympy():
    for sd in range(600):
        random.seed(sd)
        tex, d_, _ly = m._md_bdt()
        assert _chan_tri_bdt(tex) == d_, tex


def test_vd014_sa_c_dap_so():
    for sd in range(150):
        out = _sinh("L10_C1_B1_VD014_SA_C_01", sd)
        de = out.split("\\loigiai")[0]
        cac = re.findall(r"[a-d]\) \$(.+?)\$", de)
        assert len(cac) == 4, de
        so_dung = sum(1 for c in cac if _chan_tri_bdt(c))
        hoi_dung = "Có bao nhiêu mệnh đề đúng" in de
        assert _dap(out) == (so_dung if hoi_dung else 4 - so_dung)


# ---------------------------------------------------------------- NB017_SA_C: tap con cua khoang
def _thuoc(K, p):
    lo, lc, hi, hc = K
    return (p > lo or (lc and p == lo)) and (p < hi or (hc and p == hi))


def test_khoang_con_cua_brute_force():
    """So sanh `_b2_khoang_con_cua` voi kiem tra tung diem tren luoi nua nguyen (du de phan biet dong/mo)."""
    random.seed(1)
    luoi = [i / 2 for i in range(-80, 81)]
    inf = math.inf
    for _ in range(4000):
        def rd():
            lo = random.randint(-8, 6)
            hi = lo + random.randint(1, 7)
            K = [lo, random.random() < .5, hi, random.random() < .5]
            u = random.random()
            if u < .15:
                K[0], K[1] = -inf, False
            elif u < .3:
                K[2], K[3] = inf, False
            return tuple(K)
        A, X = rd(), rd()
        con = all(_thuoc(A, p) for p in luoi if _thuoc(X, p))
        # voi A huu han thi X vo han khong the la tap con: luoi chi toi +-40 nen phai chan tay phan vo han
        if X[0] == -inf and A[0] != -inf or X[2] == inf and A[2] != inf:
            con = False
        assert m._b2_khoang_con_cua(X, A) == con, (A, X)


def test_nb017_sa_c_dap_so():
    for sd in range(200):
        out = _sinh("L10_C1_B2_NB017_SA_C_01", sd)
        de = out.split("\\loigiai")[0]
        A = re.search(r"A = ([\[(])(-?\d+);\\ (-?\d+)([\])])\$", de)
        assert A, de
        KA = (int(A.group(2)), A.group(1) == "[", int(A.group(3)), A.group(4) == "]")
        ds = re.findall(r"[a-d]\) \$([\[(])(-?\d+|-\\infty);\\ (-?\d+|\+\\infty)([\])])\$", de)
        assert len(ds) == 4, de
        so_con = 0
        for t, lo, hi, p in ds:
            lo = -math.inf if "infty" in lo else int(lo)
            hi = math.inf if "infty" in hi else int(hi)
            X = (lo, t == "[", hi, p == "]")
            luoi = [i / 2 for i in range(-80, 81)]
            con = all(_thuoc(KA, q) for q in luoi if _thuoc(X, q)) and not (lo == -math.inf or hi == math.inf)
            so_con += con
        hoi_con = "\\textbf{không phải} là tập con" not in de.split("Trong các tập hợp sau")[1]
        assert _dap(out) == (so_con if hoi_con else 4 - so_con)


# ---------------------------------------------------------------- NB017_SA_G: so tap con
def test_nb017_sa_g_dap_so():
    for sd in range(300):
        out = _sinh("L10_C1_B2_NB017_SA_G_01", sd)
        kq = re.search(r"A = \\left\\\{([^}]*)\\right\\\}\$\. Tập hợp \$A\$ (.*?)\?", out)
        A = [int(v) for v in kq.group(1).split(";")]
        hoi = kq.group(2)
        n = len(A)
        tat_ca = [c for r in range(n + 1) for c in itertools.combinations(A, r)]
        if "gồm đúng $" in hoi:
            k = int(re.search(r"gồm đúng \$(\d+)\$", hoi).group(1))
            mong_doi = sum(1 for c in tat_ca if len(c) == k)
        elif "khác tập rỗng" in hoi:
            mong_doi = sum(1 for c in tat_ca if c)
        else:
            assert hoi == "có bao nhiêu tập con"
            mong_doi = len(tat_ca)
        assert _dap(out) == mong_doi


# ---------------------------------------------------------------- NB017_SA_H_01: tap rong, brute force
def _rong_brute(de):
    r"""Tinh lai tap `\left\{x \in D \mid dieu_kien\right\}` co rong khong bang brute force."""
    kq = re.match(r"\\left\\\{x \\in \\mathbb\{(\w)\} \\mid (.+)\\right\\\}$", de)
    mien, dk = kq.group(1), kq.group(2)
    if mien == "Q":
        k = int(re.match(r"x\^2 = (\d+)$", dk).group(1))
        return math.isqrt(k) ** 2 != k           # x^2 = k co nghiem huu ti khi k chinh phuong
    if mien == "R":
        return False                              # khoang (a; a+1) cua R luon khac rong
    py = dk.replace("|x|", "abs(x)")
    py = re.sub(r"(\d)x", r"\1*x", py)
    py = py.replace(" = ", " == ")
    xs = range(-200, 201) if mien == "Z" else range(0, 401)
    return not any(eval(py, {"abs": abs}, {"x": x}) for x in xs)


def test_tap_rong_hay_khong_theo_brute_force():
    for sd in range(2000):
        random.seed(sd)
        de, rong, _ly = m._tap_rong_hay_khong()
        assert _rong_brute(de) == rong, de


def test_nb017_sa_h_01_dap_so():
    for sd in range(200):
        out = _sinh("L10_C1_B2_NB017_SA_H_01", sd)
        de = out.split("\\loigiai")[0]
        cac = re.findall(r"[a-d]\) \$(\\left\\\{x .*?\\right\\\})\$", de)
        assert len(cac) == 4, de
        so_rong = sum(1 for c in cac if _rong_brute(c))
        hoi_rong = "là tập hợp rỗng?" in de
        assert _dap(out) == (so_rong if hoi_rong else 4 - so_rong)


def test_nb017_sa_h_02_dap_so_theo_kho():
    kho = m._B2_RONG_LOI
    for sd in range(200):
        out = _sinh("L10_C1_B2_NB017_SA_H_02", sd)
        de = out.split("\\loigiai")[0]
        cac = re.findall(r"[a-d]\) (.*?)(?:\\\\|\n)", de.replace("\\\\ ", "\\\\\n"))[:4]
        tra = {k[0]: k[1] for k in kho}
        assert all(c in tra for c in cac), cac
        so_rong = sum(1 for c in cac if tra[c])
        hoi_rong = "là tập hợp rỗng?" in de
        assert _dap(out) == (so_rong if hoi_rong else 4 - so_rong)


# ---------------------------------------------------------------- TH018_SA_B_02..04: phep toan tap hop
def _doc_tap(s):
    return {int(v) for v in s.split(";")}


def test_th018_sa_b_02_dap_so():
    for sd in range(200):
        out = _sinh("L10_C1_B2_TH018_SA_B_02", sd)
        kq = re.search(r"A = \\left\\\{([^}]*)\\right\\\}\$ và \$B = \\left\\\{([^}]*)\\right\\\}\$", out)
        assert _dap(out) == len(_doc_tap(kq.group(1)) & _doc_tap(kq.group(2)))


def test_th018_sa_b_03_dap_so():
    for sd in range(300):
        out = _sinh("L10_C1_B2_TH018_SA_B_03", sd)
        kq = re.search(r"E = \\left\\\{([^}]*)\\right\\\}\$ và các tập con \$A = \\left\\\{([^}]*)\\right\\\}\$, "
                       r"\$B = \\left\\\{([^}]*)\\right\\\}\$ của \$E\$\. Tập hợp \$(.+?)\$ có bao nhiêu", out)
        E, A, B = _doc_tap(kq.group(1)), _doc_tap(kq.group(2)), _doc_tap(kq.group(3))
        ten = kq.group(4)
        bu = lambda S: E - S
        mong_doi = {r"C_EA": bu(A), r"C_EB": bu(B), r"C_E(A \cup B)": bu(A | B), r"C_E(A \cap B)": bu(A & B),
                    r"C_EA \cap C_EB": bu(A) & bu(B), r"C_EA \cup C_EB": bu(A) | bu(B)}[ten]
        assert _dap(out) == len(mong_doi)


def test_th018_sa_b_04_dap_so():
    for sd in range(300):
        out = _sinh("L10_C1_B2_TH018_SA_B_04", sd)
        kq = re.search(r"A \\setminus B = \\left\\\{([^}]*)\\right\\\}\$, \$B \\setminus A = \\left\\\{([^}]*)\\right\\\}\$ và "
                       r"\$A \\cap B = \\left\\\{([^}]*)\\right\\\}\$\. Tập hợp \$(.+?)\$ có bao nhiêu", out)
        AB, BA, G = _doc_tap(kq.group(1)), _doc_tap(kq.group(2)), _doc_tap(kq.group(3))
        hoi = kq.group(4)
        mong_doi = {"A": AB | G, "B": BA | G, r"A \cup B": AB | BA | G}[hoi]
        assert _dap(out) == len(mong_doi)


# ---------------------------------------------------------------- TH018_SA_D_01: doc bang
def test_th018_sa_d_01_dap_so_doc_bang():
    bang_theo_tc1 = {b[4]: b for b in m._B2_BANG}            # tên tiêu chí 1 (duy nhất mỗi bảng) -> (.., dat, khong, ..)
    for sd in range(300):
        out = _sinh("L10_C1_B2_TH018_SA_D_01", sd)
        tab = re.search(r"\\begin\{tabular\}\{\|c\|c+\|\}\\hline (.*?)\\end\{tabular\}", out, re.S).group(1)
        hang = [h.strip() for h in tab.split(r"\\ \hline") if h.strip()]
        o = [[c.strip() for c in h.split("&")] for h in hang]
        b = bang_theo_tc1[o[1][0]]
        dat = b[6]
        A = {i for i, c in enumerate(o[1][1:], 1) if c == dat}
        B = {i for i, c in enumerate(o[2][1:], 1) if c == dat}
        phep = re.search(r"Tập hợp \$(.+?)\$ có bao nhiêu phần tử\?", out).group(1)
        mong_doi = {r"A \cap B": A & B, r"A \cup B": A | B, r"A \setminus B": A - B, r"B \setminus A": B - A}[phep]
        assert mong_doi and _dap(out) == len(mong_doi)


# ---------------------------------------------------------------- khoang / doan / nua khoang: doc lai tu TeX
_KH = re.compile(r"\\left([\[(])\s*(-\\infty|-?\d+);\\ (\+\\infty|-?\d+)\\right([\])])")


def _doc_hop_khoang(tex):
    r"""'\left(a;\ b\right] \cup ...' -> danh sach (lo, lo_dong, hi, hi_dong)."""
    ra = []
    for t, lo, hi, p in _KH.findall(tex):
        lo = -math.inf if "infty" in lo else int(lo)
        hi = math.inf if "infty" in hi else int(hi)
        ra.append((lo, t == "[", hi, p == "]"))
    return ra


def _nguyen_trong(hop, tu=-60, den=60):
    return {v for v in range(tu, den + 1) if any(_thuoc(K, v) for K in hop)}


def test_vd021_sa_b_dap_so():
    ham = {r"(A \cap B) \cup (A \cap C)": lambda A, B, C: (A & B) | (A & C), r"A \cap B \cap C": lambda A, B, C: A & B & C,
           r"(A \cup B) \cap C": lambda A, B, C: (A | B) & C, r"(A \cap B) \setminus C": lambda A, B, C: (A & B) - C,
           r"A \cap (B \cup C)": lambda A, B, C: A & (B | C), r"(A \setminus B) \cup C": lambda A, B, C: (A - B) | C}
    for sd in range(300):
        out = _sinh("L10_C1_B2_VD021_SA_B_01", sd)
        de = out.split("\\loigiai")[0]
        kq = re.search(r"A = (.+?)\$, \$B = (.+?)\$ và \$C = (.+?)\$\. Tập hợp \$(.+?)\$ có bao nhiêu", de)
        A, B, C = (_nguyen_trong(_doc_hop_khoang(kq.group(i))) for i in (1, 2, 3))
        assert _dap(out) == len(ham[kq.group(4)](A, B, C))


def test_vd021_sa_c_dap_so():
    for sd in range(300):
        out = _sinh("L10_C1_B2_VD021_SA_C_01", sd)
        de = out.split("\\loigiai")[0]
        kq = re.search(r"C_\{\\mathbb\{R\}\}A = (.+?) và \$C_\{\\mathbb\{R\}\}B = (.+?)\$\. Tập hợp \$(.+?)\$ có bao", de)
        CA = _nguyen_trong(_doc_hop_khoang(kq.group(1).rstrip("$")), -80, 80)
        CB = _nguyen_trong(_doc_hop_khoang(kq.group(2)), -80, 80)
        U = set(range(-80, 81))
        A, B = U - CA, U - CB
        mong_doi = (A & B) if kq.group(3) == r"A \cap B" else (A | B)
        assert _dap(out) == len(mong_doi)


# ---------------------------------------------------------------- NB017_SA_I: bat dang thuc <-> khoang
def _doc_bdt(dk):
    """'2 \\le x < 5' / 'x \\le 3' / 'x > 1' -> (lo, lo_dong, hi, hi_dong)."""
    mm = re.fullmatch(r"(-?\d+) (\\le|<) x (\\le|<) (-?\d+)", dk)
    if mm:
        return (int(mm.group(1)), mm.group(2) == r"\le", int(mm.group(4)), mm.group(3) == r"\le")
    mm = re.fullmatch(r"x (\\le|<) (-?\d+)", dk)
    if mm:
        return (-math.inf, False, int(mm.group(2)), mm.group(1) == r"\le")
    mm = re.fullmatch(r"x (\\ge|>) (-?\d+)", dk)
    assert mm, dk
    return (int(mm.group(2)), mm.group(1) == r"\ge", math.inf, False)


def test_nb017_sa_i_dap_so():
    for sd in range(300):
        out = _sinh("L10_C1_B2_NB017_SA_I_01", sd)
        de = out.split("\\loigiai")[0]
        cac = re.findall(r"[a-d]\) \$\\left\\\{x \\in \\mathbb\{R\} \\mid (.+?)\\right\\\} = (.+?)\$", de)
        assert len(cac) == 4, de
        so_dung = 0
        for dk, khoang in cac:
            (K,) = _doc_hop_khoang(khoang)
            so_dung += (_doc_bdt(dk) == K)
        hoi_dung = "Có bao nhiêu đẳng thức đúng" in de
        assert _dap(out) == (so_dung if hoi_dung else 4 - so_dung)
