# -*- coding: utf-8 -*-
"""L10_C4_B7_VD039 (16/10/2026, cau mau co Lan: tau tren bien Dong theo huong N20 do E): kiem chung DOC LAP.

Doc huong, van toc, thoi gian tu de; dung vecto do doi bang toa do (Bac = truc y, Dong = truc x), tinh |AB| va huong cua
vecto BA roi viet lai dang N/S x do E/W de so voi dap an. Moi phuong an nhieu phai sai.
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
_spec = importlib.util.spec_from_file_location("L10_C4_vd039", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_vd039"] = M
_spec.loader.exec_module(M)

HUONG = re.compile(r"\$\\mathrm\{([NS])\}(\d+)\^\\circ\\mathrm\{([EW])\}\$")


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, *a, **k: cap.append((de, str(dap), list(nhieu), giai)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, "L10_C4_B7_VD039_" + ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _vecto(ns, goc, ew, r):
    a = math.radians(goc)
    return (r * math.sin(a) * (1 if ew == "E" else -1), r * math.cos(a) * (1 if ns == "N" else -1))


def _ve_huong(x, y):
    ns = "N" if y > 0 else "S"
    ew = "E" if x > 0 else "W"
    return ns, round(math.degrees(math.atan2(abs(x), abs(y)))), ew


def _doc(de):
    ns, goc, ew = HUONG.search(de).groups()
    v = int(re.search(r"vận tốc \$(\d+)\$ km/h", de).group(1))
    m = re.search(r"Sau \$(\d+)\$ giờ(?: \$(\d+)\$ phút)?|Sau \$(\d+)\$ phút", de)
    gio = int(m.group(1)) + int(m.group(2) or 0) / 60 if m.group(1) else int(m.group(3)) / 60
    x, y = _vecto(ns, int(goc), ew, v * gio)
    return math.hypot(x, y), _ve_huong(-x, -y)


def _so(s):
    return float(s.replace("{,}", ".").replace(",", "."))


def test_mc():
    loai = set()
    for s in range(300):
        de, dap, nhieu, giai = _bat("MC_A_01", s)
        loai.add(de.split(",")[0][:12])
        kc, huong = _doc(de)

        def dung(pa):
            m = re.match(r"\$([\d{},]+)\$ km, hướng (.+)$", pa)
            h = HUONG.search(m.group(2)).groups()
            return abs(_so(m.group(1)) - kc) < 1e-9 and (h[0], int(h[1]), h[2]) == huong
        assert dung(dap), (de, dap, kc, huong)
        assert not any(dung(x) for x in nhieu) and len(set([dap] + nhieu)) == 4
    assert len(loai) == 3


def test_sa():
    for s in range(300):
        de, dap, nhieu, giai = _bat("SA_A_01", s)
        kc, _ = _doc(de)
        assert abs(_so(dap) - kc) < 1e-9 and len(dap) <= 4 and "hướng nào" not in de
