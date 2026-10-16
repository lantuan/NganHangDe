# -*- coding: utf-8 -*-
"""L10_C4_B7_VD039 chu B (16/10/2026, theo Vi du 4 SGK co Lan gui: luc day Archimedes va trong luc tren luoi o vuong).

Kiem chung DOC LAP tu chinh hinh TikZ: doc toa do hai mui ten (F mau den, P mau xanh), tinh do dai, huong; ti so
d_A / d_l = |P| / |F| (vat chim hoan toan); cau chon hinh: dung MOT hinh co F thang dung len, P thang dung xuong va quan he
do dai khop tinh huong (chim: P > F; lo lung: P = F; noi len: F > P).
"""
import importlib.util
import math
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C4_vd039b", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_vd039b"] = M
_spec.loader.exec_module(M)

MUI = re.compile(r"\\draw\[->,thick(,blue)?\] \(([-\d.]+),([-\d.]+)\) -- \(([-\d.]+),([-\d.]+)\);")


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, hinh=0, *a, **k: cap.append((de, str(dap), list(nhieu), giai, hinh)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, "L10_C4_B7_VD039_" + ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _hai_luc(tikz):
    ra = {}
    for xanh, x1, y1, x2, y2 in MUI.findall(tikz):
        ra["P" if xanh else "F"] = (float(x2) - float(x1), float(y2) - float(y1))
    return ra["F"], ra["P"]


def _tinh_huong(de):
    if "nằm yên dưới đáy" in de:
        return "chim"
    if "lơ lửng" in de:
        return "lo_lung"
    assert "đang nổi lên" in de
    return "noi"


def _ps(tex):
    m = re.fullmatch(r"\$(?:(\d+)|\\dfrac\{(\d+)\}\{(\d+)\})\$", tex)
    return Fraction(int(m.group(1))) if m.group(1) else Fraction(int(m.group(2)), int(m.group(3)))


def _dai(v):
    return math.hypot(*v)


def test_mc_b_01_ti_so():
    for s in range(250):
        de, dap, nhieu, giai, hinh = _bat("MC_B_01", s)
        F, P = _hai_luc(hinh)
        assert abs(F[0]) < 1e-9 and F[1] > 0 and abs(P[0]) < 1e-9 and P[1] < 0
        fa, pa = Fraction(round(_dai(F))), Fraction(round(_dai(P)))
        th = _tinh_huong(de)
        assert {"chim": pa > fa, "lo_lung": pa == fa, "noi": pa < fa}[th], (de, fa, pa)
        dung = fa / pa if r"\dfrac{d_\ell}{d_A}" in de else pa / fa
        assert _ps(dap) == dung and all(_ps(x) != dung for x in nhieu) and len(set(nhieu)) == 3


def test_mc_b_02_chon_hinh():
    for s in range(250):
        de, dap, nhieu, giai, _ = _bat("MC_B_02", s)
        th = _tinh_huong(de)

        def dung(tikz):
            F, P = _hai_luc(tikz)
            if abs(F[0]) > 1e-9 or F[1] <= 0 or abs(P[0]) > 1e-9 or P[1] >= 0:
                return False
            return {"chim": _dai(P) > _dai(F) + 1e-9, "lo_lung": abs(_dai(P) - _dai(F)) < 1e-9,
                    "noi": _dai(F) > _dai(P) + 1e-9}[th]
        assert dung(dap) and not any(dung(x) for x in nhieu)


def test_sa_b_01():
    for s in range(250):
        de, dap, nhieu, giai, hinh = _bat("SA_B_01", s)
        F, P = _hai_luc(hinh)
        r = _dai(F) / _dai(P) if r"\dfrac{d_\ell}{d_A}" in de else _dai(P) / _dai(F)
        assert abs(float(dap.replace(",", ".")) - r) < 1e-9 and len(dap) <= 4, (de, dap, r)
