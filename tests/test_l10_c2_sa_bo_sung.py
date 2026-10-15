"""Chuong 2 lop 10 - cac cau SA/MC bo sung 15/10/2026 (co Lan duyet cach lam).

Moi dap so duoc TINH LAI DOC LAP tu chinh van ban de bai sinh ra (regex + sympy / vet can), khong dung lai
ham sinh de.
"""
import importlib.util
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest
from sympy import Symbol
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, standard_transformations)

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C2_sa_bo_sung", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_sa_bo_sung"] = M
_spec.loader.exec_module(M)

X, Y = Symbol("x"), Symbol("y")
PHEP = re.compile(r"^(.+?) (\\le|\\ge|<|>) (-?\d+)$")
SO_LAN = 300


def _bat(ham, seed, **kw):
    """Chay ham voi seed, bat (debai, dapso, dsnhieu, giai) truyen vao MC_SA_answer_const."""
    cap = []
    goc = M.MC_SA_answer_const
    M.MC_SA_answer_const = lambda debai, dap, nhieu, giai, *a, **k: cap.append((debai, dap, nhieu, giai)) or ""
    try:
        M._rd.seed(seed)
        ham(1, **kw)
    finally:
        M.MC_SA_answer_const = goc
    assert len(cap) == 1
    return cap[0]


def _tach_bpt(tex):
    m = PHEP.match(tex)
    assert m, tex
    return m.group(1), m.group(2), int(m.group(3))


def _he_so(lhs):
    e = parse_expr(lhs.replace(" ", ""), transformations=standard_transformations + (implicit_multiplication_application,),
                   local_dict={"x": X, "y": Y})
    return int(e.coeff(X)), int(e.coeff(Y))


THOA = {r"\le": lambda v, c: v <= c, r"\ge": lambda v, c: v >= c, "<": lambda v, c: v < c, ">": lambda v, c: v > c}


def _kiem_nhieu(dap, nhieu, mien):
    assert dap not in nhieu and len(set(nhieu)) == len(nhieu) and set(nhieu) <= {str(j) for j in mien}


# ------------------------------------------------------------------ TH024_SA_B (truoc 15/10/2026 la NB023_SA_A): dem cap so la nghiem
def test_nb023_sa_a_dem_dung_so_cap_nghiem():
    thay = set()
    for seed in range(SO_LAN):
        debai, dap, nhieu, giai = _bat(M.L10_C2_B3_TH024_SA_B_01, seed)
        m = re.search(r"Cho bất phương trình \$(.+?)\$\. Trong các cặp số (.+?), có bao nhiêu cặp số là nghiệm", debai)
        assert m, debai
        lhs, dau, c = _tach_bpt(m.group(1))
        a, b = _he_so(lhs)
        diem = [(int(p), int(q)) for p, q in re.findall(r"\\left\((-?\d+); (-?\d+)\\right\)", m.group(2))]
        assert len(diem) == 5 and len(set(diem)) == 5
        k = sum(1 for p, q in diem if THOA[dau](a * p + b * q, c))
        assert int(dap) == k and 1 <= k <= 4, debai
        assert "có $%s$ cặp số là nghiệm" % dap in giai.replace("Vậy có", "có")
        _kiem_nhieu(dap, nhieu, range(0, 6))
        thay.add(k)
    assert thay == {1, 2, 3, 4}


def test_nb023_sa_a_dinh_dang_tl_ngan_va_mc():
    sa = M.L10_C2_B3_TH024_SA_B_01(2)
    assert sa.count(r"\shortans") == 2 and r"\choice" not in sa and r"\item" not in sa
    mc = M.L10_C2_B3_TH024_SA_B_01(2, 1)
    assert mc.count(r"\choice") == 2 and mc.count(r"\True") == 2


# ------------------------------------------------------------------ NB023_MC_B: ban trac nghiem cua SA_B
def test_nb023_mc_b_dap_an_la_gia_tri_f():
    for seed in range(100):
        M._rd.seed(seed)
        txt = M.L10_C2_B3_NB023_MC_B_01(1)
        assert txt.count(r"\choice") == 1 and txt.count(r"\True") == 1 and r"\shortans" not in txt
        m = re.search(r"Cho bất phương trình \$(.+?)\$\. Điểm \$M\\left\((-?\d+); (-?\d+)\\right\)", txt)
        f = re.search(r"F\\left\(x; y\\right\) = (.+?)\$ tại", txt).group(1)
        a, b = _he_so(f)
        x0, y0 = int(m.group(2)), int(m.group(3))
        dung = re.search(r"\{\\True (-?\d+)\}", txt).group(1)
        assert int(dung) == a * x0 + b * y0
        lhs, dau, c = _tach_bpt(m.group(1))
        assert _he_so(lhs) == (a, b) and THOA[dau](a * x0 + b * y0, c)


# ------------------------------------------------------------------ TH027_SA_C (truoc 15/10/2026 la TH027_SA_B): so dinh / canh cua mien nghiem
def _so_dinh_vet_can(fx, gx, hx, kx, a, b, c, dau):
    """Cac ung vien: 4 dinh hinh chu nhat + giao diem duong thang voi 4 canh; giu cac diem thoa du 5 bat phuong trinh."""
    ung = {(fx, hx), (fx, kx), (gx, hx), (gx, kx)}
    ung = {(Fraction(p), Fraction(q)) for p, q in ung}
    for X0 in (fx, gx):                                   # canh dung x = X0: a*X0 + b*y = c
        ung.add((Fraction(X0), Fraction(c - a * X0, b)))
    for Y0 in (hx, kx):                                   # canh ngang y = Y0
        ung.add((Fraction(c - b * Y0, a), Fraction(Y0)))
    ok = set()
    for p, q in ung:
        v = a * p + b * q
        if fx <= p <= gx and hx <= q <= kx and (v <= c if dau == r"\le" else v >= c):
            ok.add((p, q))
    return len(ok)


def test_th027_sa_b_dem_dinh_canh_vet_can():
    thay = set()
    for seed in range(SO_LAN):
        debai, dap, nhieu, giai = _bat(M.L10_C2_B4_TH027_SA_C_01, seed)
        m = re.search(r"\\heva\{& x \\ge (-?\d+) \\\\ & x \\le (-?\d+) \\\\ & y \\ge (-?\d+) \\\\ & y \\le (-?\d+) \\\\ & (.+?)\}\$\. "
                      r"Miền nghiệm của hệ là một đa giác\. Đa giác đó có bao nhiêu (đỉnh|cạnh)\?", debai)
        assert m, debai
        fx, gx, hx, kx = (int(m.group(i)) for i in (1, 2, 3, 4))
        assert fx < gx and hx < kx
        lhs, dau, c = _tach_bpt(m.group(5))
        a, b = _he_so(lhs)
        assert a != 0 and b != 0
        n = _so_dinh_vet_can(fx, gx, hx, kx, a, b, c, dau)
        assert int(dap) == n and n in (3, 4, 5), debai
        _kiem_nhieu(dap, nhieu, range(3, 8))
        assert "có $%s$ đỉnh và $%s$ cạnh" % (dap, dap) in giai
        thay.add(n)
    assert thay == {3, 4, 5}


def test_th027_vet_can_dung_tren_mau_biet():
    # hinh chu nhat [0,3]x[0,3]
    assert _so_dinh_vet_can(0, 3, 0, 3, 1, 1, 1, r"\le") == 3      # x + y <= 1: tam giac (0,0),(1,0),(0,1)
    assert _so_dinh_vet_can(0, 3, 0, 3, 1, 1, 4, r"\le") == 5      # x + y <= 4: ngu giac
    assert _so_dinh_vet_can(0, 3, 0, 3, 4, 1, 6, r"\le") == 4      # 4x + y <= 6: tu giac (0,0),(1.5,0),(0.75,3),(0,3)
    assert _so_dinh_vet_can(0, 3, 0, 3, 1, 1, 4, r"\ge") == 3      # x + y >= 4: tam giac (3,1),(3,3),(1,3)


@pytest.mark.parametrize("ten", ["TH024_SA_B_01", "TH027_SA_C_01"])
def test_sa_moi_khong_co_item_va_don_cau(ten):
    ham = [getattr(M, n) for n in dir(M) if n.endswith(ten)][0]
    for seed in range(30):
        M._rd.seed(seed)
        out = ham(3)
        assert out.count(r"\begin{ex}") == 3 and out.count(r"\shortans") == 3
        assert r"\item" not in out and "listEX" not in out
