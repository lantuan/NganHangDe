# -*- coding: utf-8 -*-
r"""Bai 8 lop 10 bo sung 16/10/2026 theo cau mau co Lan gui (co Lan duyet ke hoach ID):
TH040_MC_A_02, TH041_MC_A_02, TH040_MC_B_02 (khang dinh nao dung), TH040_MC_C/SA_C, TH041_MC_C/SA_C (do dai vecto
tong/hieu trong hinh), B11_VD060_MC_A_02/SA_A_02 (hop luc, goc bat ki).

Kiem chung DOC LAP: doc tung phuong an / bieu thuc trong de bang tests/_tinh_tex.py roi tinh lai bang toa do tu dung
(diem ngau nhien, hinh dat o vi tri xoay + tinh tien ngau nhien, luc dat tren truc), khong dung ham cua file sinh de.
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
from _tinh_tex import V, bang, so, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C4_b8_bo_sung", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_b8_bo_sung"] = M
_spec.loader.exec_module(M)


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, *a, **k: cap.append((de, str(dap), list(nhieu), giai)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _dung(kd, P):
    """Khẳng định '$L = R$' (vectơ theo điểm) đúng với toạ độ P?"""
    l, r = kd.strip("$").split(" = ")
    return bang(tinh(l, P=P), tinh(r, P=P))


# ---------------------------------------------------------------- A_02: ba diem phan biet bat ki
@pytest.mark.parametrize("ten, phep", [("L10_C4_B8_TH040_MC_A_02", "+"), ("L10_C4_B8_TH041_MC_A_02", "-")])
def test_a02_dung_mot_phuong_an(ten, phep):
    for s in range(200):
        de, dap, nhieu, giai = _bat(ten, s)
        diem = re.findall(r"\$([A-Z])\$", de.split("Khẳng định")[0])
        assert len(diem) == 3 and "luôn đúng" in de
        for _ in range(3):
            P = {t: V(random.uniform(-9, 9), random.uniform(-9, 9)) for t in diem}
            assert _dung(dap, P), (de, dap)
            assert not any(_dung(x, P) for x in nhieu), (de, nhieu)
        assert len(set([dap] + nhieu)) == 4
        assert (" + " in dap.split(" = ")[1]) == (phep == "+")
        if phep == "-":                                    # quy tac tru: hai vecto chung diem dau
            u, w = re.findall(r"\\overrightarrow\{([A-Z])([A-Z])\}", dap.split(" = ")[1])
            assert u[0] == w[0]


def test_b02_hinh_binh_hanh():
    for s in range(200):
        de, dap, nhieu, giai = _bat("L10_C4_B8_TH040_MC_B_02", s)
        A, B, C, D = re.search(r"Cho hình bình hành \$([A-Z]{4})\$", de).group(1)
        for _ in range(3):
            P = {A: V(random.uniform(-9, 9), random.uniform(-9, 9)), B: V(random.uniform(-9, 9), random.uniform(-9, 9)),
                 D: V(random.uniform(-9, 9), random.uniform(-9, 9))}
            P[C] = P[B] + P[D] - P[A]
            assert _dung(dap, P) and not any(_dung(x, P) for x in nhieu), (de, dap, nhieu)
        # cac phuong an cung ve phai (nhu cau mau)
        assert len({x.split(" = ")[1] for x in [dap] + nhieu}) == 1


# ---------------------------------------------------------------- C: do dai vecto tong / hieu
def _xoay(P):
    g = random.uniform(0, 2 * math.pi)
    tx, ty = random.uniform(-5, 5), random.uniform(-5, 5)
    return {k: V(x * math.cos(g) - y * math.sin(g) + tx, x * math.sin(g) + y * math.cos(g) + ty) for k, (x, y) in P.items()}


def _hinh_tu_de(de, a):
    """Dung toa do cua hinh tu chinh van ban de bai (a: gia tri thay cho chu a)."""
    sv = lambda t: tinh(t, a=a)
    m = re.search(r"Cho hình vuông \$(\w)(\w)(\w)(\w)\$ cạnh \$([^$]+)\$", de)
    if m:
        A, B, C, D, c = m.groups()
        c = sv(c)
        P = {A: (0, 0), B: (c, 0), C: (c, c), D: (0, c)}
    m2 = re.search(r"Cho hình chữ nhật \$(\w)(\w)(\w)(\w)\$ có \$(\w\w) = ([^$]+)\$, \$(\w\w) = ([^$]+)\$", de)
    if m2:
        A, B, C, D = m2.groups()[:4]
        assert m2.group(5) == A + B and m2.group(7) == A + D
        p, q = sv(m2.group(6)), sv(m2.group(8))
        P = {A: (0, 0), B: (p, 0), C: (p, q), D: (0, q)}
    m3 = re.search(r"Cho hình thoi \$(\w)(\w)(\w)(\w)\$ cạnh \$([^$]+)\$ có \$\\widehat\{(\w)(\w)(\w)\} = 60\^\\circ\$", de)
    if m3:
        A, B, C, D, c = m3.groups()[:5]
        assert m3.group(6) + m3.group(7) + m3.group(8) == B + A + D
        c = sv(c)
        P = {A: (0, 0), B: (c, 0), D: (c * math.cos(math.pi / 3), c * math.sin(math.pi / 3))}
        P[C] = (P[B][0] + P[D][0], P[B][1] + P[D][1])
    if m or m2 or m3:
        o = re.search(r"hai đường chéo cắt nhau tại \$(\w)\$", de)
        if o:
            P[o.group(1)] = ((P[A][0] + P[C][0]) / 2, (P[A][1] + P[C][1]) / 2)
        return P
    m = re.search(r"Cho tam giác đều \$(\w)(\w)(\w)\$ cạnh \$([^$]+)\$", de)
    if m:
        A, B, C, c = m.groups()
        c = sv(c)
        return {A: (0, 0), B: (c, 0), C: (c / 2, c * math.sqrt(3) / 2)}
    m = re.search(r"Cho tam giác \$(\w)(\w)(\w)\$ vuông tại \$(\w)\$ có \$(\w\w) = ([^$]+)\$, \$(\w\w) = ([^$]+)\$", de)
    assert m, de
    A, B, C, vt = m.groups()[:4]
    assert vt == A and m.group(5) == A + B and m.group(7) == A + C
    return {A: (0, 0), B: (sv(m.group(6)), 0), C: (0, sv(m.group(8)))}


def _bieu_thuc(de):
    m = re.search(r"Độ dài của vectơ \$([^$]+)\$ bằng", de) or re.search(r"Tính \$\\left\|(.+?)\\right\|\$", de)
    return m.group(1)


@pytest.mark.parametrize("ten, phep", [("L10_C4_B8_TH040_MC_C_01", "+"), ("L10_C4_B8_TH041_MC_C_01", "-"),
                                       ("L10_C4_B8_TH040_SA_C_01", "+"), ("L10_C4_B8_TH041_SA_C_01", "-")])
def test_c_do_dai_doc_lap(ten, phep):
    thay = set()
    for s in range(150):
        de, dap, nhieu, giai = _bat(ten, s)
        bt = _bieu_thuc(de)
        assert (" %s " % phep) in bt and bt.count(r"\overrightarrow") == 2
        if "_MC_" in ten:
            a = random.uniform(1, 3)                       # MC theo a: dung voi MOI a
            P = _xoay(_hinh_tu_de(de, a))
            d = abs(tinh(bt, P=P))
            assert abs(tinh(dap.strip("$"), a=a) - d) < 1e-7, (de, dap, d)
            assert all(abs(tinh(x.strip("$"), a=a) - d) > 1e-7 for x in nhieu), (de, nhieu)
            assert len(set([dap] + nhieu)) == 4
            u, w = [abs(tinh(t, P=P)) for t in bt.split(" %s " % phep)]
            if abs(u + w - d) > 1e-7:                      # loi hay gap |u| + |v| luon co mat
                assert any(abs(tinh(x.strip("$"), a=a) - (u + w)) < 1e-7 for x in nhieu), (de, nhieu)
        else:
            P = _xoay(_hinh_tu_de(de, 1))
            d = abs(tinh(bt, P=P))
            assert len(dap) <= 4, dap
            if "hàng phần trăm" in de:
                assert abs(so(dap) - d) <= 0.005 + 1e-9 and d < 10, (de, dap, d)
            elif "hàng phần mười" in de:
                assert abs(so(dap) - d) <= 0.05 + 1e-9, (de, dap, d)
            else:
                assert abs(so(dap) - d) < 1e-7 and abs(d - round(d)) < 1e-7, (de, dap, d)
        thay.add(re.match(r"Cho (hình vuông|hình chữ nhật|hình thoi|tam giác đều|tam giác)", de).group(1))
    assert len(thay) == 5


# ---------------------------------------------------------------- VD060_A_02: hop luc
def _luc_tu_de(de):
    m = re.search(r"\\left\|\\overrightarrow\{F_1\}\\right\| = \\left\|\\overrightarrow\{F_2\}\\right\| = (\d+)", de)
    if m:
        p = q = int(m.group(1))
    else:
        p, q = map(int, re.search(r"\\left\|\\overrightarrow\{F_1\}\\right\| = (\d+)\\ \\text\{N\}\$, "
                                  r"\$\\left\|\\overrightarrow\{F_2\}\\right\| = (\d+)", de).groups())
    if "cùng phương, cùng chiều" in de:
        g = 0
    elif "cùng phương, ngược chiều" in de:
        g = 180
    else:
        g = int(re.search(r"bằng \$(\d+)\^\\circ\$", de).group(1))
    F1, F2 = V(p, 0), V(q * math.cos(math.radians(g)), q * math.sin(math.radians(g)))
    return abs(F1 + F2)                                  # can bang: |F3| = |-(F1 + F2)|


@pytest.mark.parametrize("ten", ["L10_C4_B11_VD060_MC_A_02", "L10_C4_B11_VD060_SA_A_02"])
def test_vd060_a02_hop_luc(ten):
    goc, loai = set(), set()
    for s in range(300):
        de, dap, nhieu, giai = _bat(ten, s)
        d = _luc_tu_de(de)
        dap_so = so(dap.replace(r"\ \text{N}", ""))
        if "làm tròn kết quả đến hàng phần mười" in de:
            assert abs(dap_so - d) <= 0.05 + 1e-9 and abs(d - round(d)) > 1e-9, (de, dap, d)
        else:
            assert abs(dap_so - d) < 1e-9, (de, dap, d)
        if "_MC_" in ten:
            assert len(set([dap] + nhieu)) == 4 and dap.endswith(r"\ \text{N}$")
        else:
            assert len(dap) <= 4 and "(đơn vị: N)" in de
        loai.add("ba lực" in de)
        goc.add(re.search(r"bằng \$(\d+)\^\\circ\$|cùng chiều|ngược chiều", de).group(0))
    assert loai == {True, False} and len(goc) >= 8


def test_python_tu_sinh_khong_de_chet():
    for ten, toi_thieu in (("L10_C4_B8_TH040_MC_A_02", 60), ("L10_C4_B8_TH041_MC_A_02", 60),
                           ("L10_C4_B8_TH040_MC_B_02", 30), ("L10_C4_B8_TH040_MC_C_01", 40),
                           ("L10_C4_B8_TH040_SA_C_01", 60), ("L10_C4_B8_TH041_MC_C_01", 40),
                           ("L10_C4_B8_TH041_SA_C_01", 60), ("L10_C4_B11_VD060_MC_A_02", 100),
                           ("L10_C4_B11_VD060_SA_A_02", 100)):
        de = set()
        for s in range(150):
            random.seed(s)
            o = getattr(M, ten)(1)
            assert (r"\choice" in o) == ("_MC_" in ten) and (r"\shortans" in o) == ("_SA_" in ten)
            than = o.split(r"\loigiai")[0].replace(r"\True ", "")
            de.add((than.split(r"\choice")[0], frozenset(than.split("\n"))))   # de + tap phuong an (bo thu tu)
        assert len(de) >= toi_thieu, (ten, len(de))
