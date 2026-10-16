# -*- coding: utf-8 -*-
"""Bai 7 lop 10 bo sung 16/10/2026 theo cau mau co Lan gui (co Lan duyet ke hoach):
NB037_MC_E (dien khuyet dinh nghia / ki hieu - chi MC), NB037_MC_A_03 + SA_A_02 (diem thang hang theo thu tu),
NB037_MC_F + SA_F (dem so diem D thoa dieu kien vecto).

Kiem chung DOC LAP: diem thang hang dat tren truc so theo thu tu doc tu de roi so huong; cau dem diem D dich dieu kien
trong de thanh he phuong trinh / bat phuong trinh voi D = (x; y) va giai bang sympy (A, B, C toa do ngau nhien).
"""
import importlib.util
import random
import re
import sys
from pathlib import Path

import pytest
import sympy as sp

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C4_b7_bo_sung", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_b7_bo_sung"] = M
_spec.loader.exec_module(M)

P = "L10_C4_B7_NB037_"
VT = re.compile(r"\\overrightarrow\{([A-Z])([A-Z])\}")


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, *a, **k: cap.append((de, str(dap), list(nhieu), giai)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, P + ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


# ---------------------------------------------------------------- A: thang hang theo thu tu
def _vi_tri(de):
    m = re.search(r"Cho (?:ba|bốn) điểm ((?:\$[A-Z]\$(?:, )?)+) (?:phân biệt, )?thẳng hàng theo thứ tự đó", de)
    return {t: i for i, t in enumerate(re.findall(r"\$([A-Z])\$", m.group(1)))}


def _cung_huong(vt, u, w):
    return (vt[u[1]] - vt[u[0]]) * (vt[w[1]] - vt[w[0]]) > 0


def test_mc_a_03_thang_hang():
    for s in range(300):
        de, dap, nhieu, giai = _bat("MC_A_03", s)
        vt = _vi_tri(de)
        hoi_cung = "cùng hướng?" in de
        for i, lc in enumerate([dap] + nhieu):
            u, w = VT.findall(lc)
            assert _cung_huong(vt, u, w) == (hoi_cung if i == 0 else not hoi_cung), (de, lc)
        assert len(set([dap] + nhieu)) == 4


def test_sa_a_02_dem_cap():
    thay = set()
    for s in range(300):
        de, dap, nhieu, giai = _bat("SA_A_02", s)
        vt = _vi_tri(de)
        cap = re.findall(r"\d\) \$\\overrightarrow\{([A-Z]{2})\}\$ và \$\\overrightarrow\{([A-Z]{2})\}\$", de)
        assert len(cap) == 4
        hoi_cung = "cùng hướng?" in de
        k = sum(1 for u, w in cap if _cung_huong(vt, u, w) == hoi_cung)
        assert int(dap) == k and 1 <= k <= 3
        thay.add(k)
    assert thay == {1, 2, 3}


# ---------------------------------------------------------------- F: dem diem D
X, Y = sp.symbols("x y", real=True)


def _dem_D(de):
    """Số điểm D (sympy) hoặc 'vô số'."""
    diem = re.search(r"Cho hai điểm phân biệt \$([A-Z])\$, \$([A-Z])\$(?: và điểm \$([A-Z])\$)?", de)
    A, B, C = diem.groups()
    D = re.search(r"Có bao nhiêu điểm \$([A-Z])\$", de).group(1)
    T = {A: sp.Matrix([0, 0]), B: sp.Matrix([random.randint(2, 6), random.randint(-3, 3)])}
    if C:
        while True:
            T[C] = sp.Matrix([random.randint(-5, 5), random.randint(-5, 5)])
            ab, ac = T[B] - T[A], T[C] - T[A]
            if ab[0] * ac[1] - ab[1] * ac[0] != 0:
                break
    T[D] = sp.Matrix([X, Y])
    v = lambda p, q: T[q] - T[p]
    dk = de.split("thoả mãn ")[1].rstrip("?")
    pt, bdt, khac = [], [], []
    for phan in dk.split(" và "):
        phan = phan.strip()
        m = re.fullmatch(r"\$\\overrightarrow\{(\w)(\w)\} = \\overrightarrow\{(\w)(\w)\}\$", phan)
        if m:
            d = v(m.group(1), m.group(2)) - v(m.group(3), m.group(4))
            pt += [d[0], d[1]]
            continue
        m = re.fullmatch(r"\$\\left\|\\overrightarrow\{(\w)(\w)\}\\right\| = (\d?)\\left\|\\overrightarrow\{(\w)(\w)\}\\right\|\$", phan)
        if m:
            k = int(m.group(3) or 1)
            u, w = v(m.group(1), m.group(2)), v(m.group(4), m.group(5))
            pt.append(u.dot(u) - k * k * w.dot(w))
            continue
        m = re.fullmatch(r"\$\\overrightarrow\{(\w)(\w)\}\$ (cùng phương|cùng hướng|ngược hướng) với \$\\overrightarrow\{(\w)(\w)\}\$"
                         r"(?: \(\$(\w) \\ne (\w)\$\))?", phan)
        if m:
            u, w = v(m.group(1), m.group(2)), v(m.group(4), m.group(5))
            pt.append(u[0] * w[1] - u[1] * w[0])
            khac.append((m.group(1), m.group(2)))           # vecto khac vecto-khong
            if m.group(3) == "cùng hướng":
                bdt.append(lambda s, u=u, w=w: u.dot(w).subs(s) > 0)
            elif m.group(3) == "ngược hướng":
                bdt.append(lambda s, u=u, w=w: u.dot(w).subs(s) < 0)
            continue
        m = re.fullmatch(r"\$(\w)\$ thuộc đường thẳng \$(\w)(\w)\$", phan)
        if m:
            u, w = v(m.group(2), m.group(1)), v(m.group(2), m.group(3))
            pt.append(u[0] * w[1] - u[1] * w[0])
            continue
        raise AssertionError(phan)
    nghiem = sp.solve(pt, [X, Y], dict=True)
    if any(len(n) < 2 for n in nghiem):                      # con an tu do -> vo so
        return "vô số"
    dem = 0
    for n in nghiem:
        if not all(n[k].is_real for k in n):
            continue
        if any(T[p].subs(n) == T[q].subs(n) for p, q in khac):
            continue
        if all(f(n) for f in bdt):
            dem += 1
    return dem


@pytest.mark.parametrize("ten", ["MC_F_01", "SA_F_01"])
def test_f_dem_diem_doc_lap(ten):
    thay = set()
    for s in range(250):
        de, dap, nhieu, giai = _bat(ten, s)
        so = _dem_D(de)
        if ten.startswith("MC"):
            assert dap == ("Vô số" if so == "vô số" else "$%d$" % so), (de, so)
            assert sorted([dap] + nhieu) == sorted(["Vô số", "$0$", "$1$", "$2$"])
        else:
            assert so != "vô số" and int(dap) == so, (de, so)
        thay.add(so)
        # cau dan khong co du kien thua: moi diem neu ra deu duoc dung trong dieu kien
        dk = de.split("thoả mãn ")[1]
        for t in re.findall(r"điểm \$([A-Z])\$ không thuộc|và điểm \$([A-Z])\$", de):
            t = [x for x in t if x][0]
            assert t in dk, de
    assert len(thay) >= 3


# ---------------------------------------------------------------- E: dien khuyet / ki hieu (chi MC)
def test_e_dap_an_dung_dinh_nghia():
    for s in range(200):
        de, dap, nhieu, giai = _bat("MC_E_01", s)
        assert len(set([dap] + nhieu)) == 4 and not dap.endswith(".")
        if de.startswith("Vectơ là một đoạn thẳng"):
            assert dap == "có hướng"
        m = re.match(r"Giá của vectơ \$\\overrightarrow\{(\w)(\w)\}\$", de)
        if m:
            assert dap == r"đường thẳng $%s%s$" % m.groups()
        m = re.match(r"Độ dài của vectơ \$\\overrightarrow\{(\w)(\w)\}\$", de)
        if m:
            assert dap == r"độ dài đoạn thẳng $%s%s$" % m.groups()
    for s in range(200):
        de, dap, nhieu, giai = _bat("MC_E_02", s)
        assert len(set([dap] + nhieu)) == 4
        m = re.match(r"Vectơ có điểm đầu \$(\w)\$ và điểm cuối \$(\w)\$", de)
        if m:
            assert dap == r"$\overrightarrow{%s%s}$" % m.groups()
        m = re.match(r"Điểm (đầu|cuối) của vectơ \$\\overrightarrow\{(\w)(\w)\}\$", de)
        if m:
            assert dap == "điểm $%s$" % (m.group(2) if m.group(1) == "đầu" else m.group(3))
        m = re.match(r"Độ dài của vectơ \$\\overrightarrow\{(\w)(\w)\}\$ được kí hiệu", de)
        if m:
            assert dap == r"$\left|\overrightarrow{%s%s}\right|$" % m.groups()


def test_da_dang_python_tu_sinh():
    for ten, toi_thieu in (("MC_E_01", 100), ("MC_E_02", 100), ("MC_A_03", 100), ("SA_A_02", 100), ("MC_F_01", 100),
                           ("SA_F_01", 40)):
        de = set()
        for s in range(200):
            random.seed(s)
            de.add(getattr(M, P + ten)(1).split(r"\loigiai")[0])
        assert len(de) >= toi_thieu, (ten, len(de))
