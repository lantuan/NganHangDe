# -*- coding: utf-8 -*-
r"""L10_C3_B5_NB029_MC_E_01 (co Lan 17/10/2026): bon phuong an phai du sin, cos, tan, cot - moi gia tri dung MOT phuong an;
khong de lo dap an qua dau (khong co phuong an duy nhat khac dau ba phuong an kia).

Kiem chung DOC LAP: tinh dau bang so voi mot goc tu bat ky (math.sin, math.cos), roi xet tung phuong an.
"""
import importlib.util
import math
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C3_nb029e", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_nb029e"] = M
_spec.loader.exec_module(M)

PA = re.compile(r"\{(\\True )?\$\\(sin|cos|tan|cot)\\alpha ([<>]) 0\$\}")


def _dau(ten, goc):
    r = math.radians(goc)
    v = {"sin": math.sin(r), "cos": math.cos(r), "tan": math.tan(r), "cot": math.cos(r) / math.sin(r)}[ten]
    return ">" if v > 0 else "<"


def test_du_bon_gia_tri_va_mot_dap_an():
    thay = set()
    for s in range(400):
        random.seed(s)
        o = M.L10_C3_B5_NB029_MC_E_01(1)
        lo, hi = map(int, re.search(r"thoả mãn \$(\d+)\^\{\\circ\} < \\alpha < (\d+)\^\{\\circ\}\$", o).groups())
        hoi_dung = r"\textbf{đúng}" in o
        assert hoi_dung or r"\textbf{sai}" in o
        pa = PA.findall(o)
        assert len(pa) == 4 and sorted(p[1] for p in pa) == ["cos", "cot", "sin", "tan"], o   # đủ bốn giá trị
        dap = [p for p in pa if p[0]]
        assert len(dap) == 1
        for goc in (lo + 1, (lo + hi) / 2, hi - 1):
            for t, ten, d in pa:
                assert (d == _dau(ten, goc)) == (bool(t) == hoi_dung), (o, goc)              # đúng một đáp án
        dau = [p[2] for p in pa]
        assert not (dau.count(dap[0][2]) == 1 and dau.count(dap[0][2] == ">" and "<" or ">") == 3), o  # không lộ qua dấu
        thay.add((dap[0][1], hoi_dung))
    assert len(thay) == 8


def test_python_tu_sinh():
    de = set()
    for s in range(100):
        random.seed(s)
        o = M.L10_C3_B5_NB029_MC_E_01(1)
        assert r"\choice" in o
        de.add(o)
    assert len(de) >= 8
