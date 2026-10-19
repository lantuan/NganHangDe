# -*- coding: utf-8 -*-
r"""L10_C2_B4_TH027_MC_D / SA_D (co Lan 19/10/2026): dem nghiem nguyen cua he ba bat phuong trinh nho hinh co luoi o vuong.

Kiem chung DOC LAP: doc he tu chinh van ban de (\heva), vet can moi diem nguyen trong khung [-10; 10]^2; doc hinh TikZ:
da giac trang (mien nghiem) phai co dinh thoa he va moi diem nut luoi trong da giac dung bang tap nghiem dem duoc.
"""
import importlib.util
import json
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C2_th027d", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_th027d"] = M
_spec.loader.exec_module(M)


def _he(de):
    he = []
    for vt, dau, c in re.findall(r"& ([^&\\]+?) (\\le|\\ge|<|>) (-?\d+)", re.search(r"\\heva\{(.+?)\}\$", de).group(1)):
        a = b = 0
        for dau_hs, hs, bien in re.findall(r"([+-]?)\s*(\d*)([xy])", vt.replace(" ", "")):
            v = int(hs or 1) * (-1 if dau_hs == "-" else 1)
            if bien == "x":
                a = v
            else:
                b = v
        he.append((a, b, int(c), dau))
    assert len(he) == 3
    return he


def _thoa(he, X, Y, dong=False):
    """dong=True: bao đóng (coi < như \\le)."""
    def mot(a, b, c, d):
        v = a * X + b * Y
        if d in (r"\le", "<"):
            return v <= c if (d == r"\le" or dong) else v < c
        return v >= c if (d == r"\ge" or dong) else v > c
    return all(mot(*t) for t in he)


def _trong_da_giac(P, X, Y):
    """Điểm (X, Y) trong hoặc trên tam giác P (toạ độ thực)."""
    s = []
    for i in range(3):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % 3]
        s.append((x2 - x1) * (Y - y1) - (y2 - y1) * (X - x1))
    return all(v >= -1e-3 for v in s) or all(v <= 1e-3 for v in s)


def _chay(ten, seed):
    random.seed(seed)
    return getattr(M, "L10_C2_B4_TH027_%s_D_01" % ten)(1)


def test_sa_dem_dung_va_hinh_khop():
    thay_n, truc, bay = set(), 0, 0
    for s in range(300):
        o = _chay("SA", s)
        de = o.split(r"\shortans")[0]
        he = _he(de)
        D = {(X, Y) for X in range(-10, 11) for Y in range(-10, 11) if _thoa(he, X, Y)}
        dap = int(re.search(r"\\shortans\{ ?\$?(\d+)", o).group(1))
        assert dap == len(D) and 3 <= dap <= 12, (de, dap, len(D))
        g = re.findall(r"\(([-\d.]+),([-\d.]+)\) -- \(([-\d.]+),([-\d.]+)\) -- \(([-\d.]+),([-\d.]+)\) -- cycle", o)[0]
        P = [(float(g[i]), float(g[i + 1])) for i in (0, 2, 4)]
        for X in range(-10, 11):
            for Y in range(-10, 11):
                if (X, Y) in D:
                    assert _trong_da_giac(P, X, Y), (o, X, Y)
        for X in range(-10, 11):                                  # ngược lại: điểm nút nằm trong tam giác vẽ là nghiệm
            for Y in range(-10, 11):
                if _trong_da_giac(P, X, Y):
                    assert _thoa(he, X, Y, True), (o, X, Y)
        for x_, y_ in P:                                          # đỉnh vẽ thoả hệ (sai số làm tròn 4 chữ số)
            assert all((a * x_ + b * y_ <= c + 1e-3) if d in (r"\le", "<") else (a * x_ + b * y_ >= c - 1e-3)
                       for a, b, c, d in he)
        net = re.findall(r"\\draw\[(thick|thick,dashed)\] \(", o)
        assert sorted(net) == sorted("thick,dashed" if d in "<>" else "thick" for *_, d in he), (o, net)   # nét đứt đúng bờ
        if any(d in "<>" for *_, d in he):
            bay += 1
            dong = {(X, Y) for X in range(-10, 11) for Y in range(-10, 11) if _thoa(he, X, Y, True)}
            assert len(dong) > dap and "sai thành $%d$" % len(dong) in o, o                           # bẫy có tác dụng
        assert r"\draw[gray!45,very thin]" in o and "pattern=north east lines" in o     # có lưới, có gạch
        assert "Vậy hệ có $%d$ nghiệm nguyên" % dap in o
        thay_n.add(dap)
        truc += any((a, b, c) in ((1, 0, 0), (0, 1, 0)) for a, b, c, _ in he)
    assert len(thay_n) >= 6 and truc > 100 and 120 < bay < 240


def test_mc_mot_dap_an():
    for s in range(200):
        o = _chay("MC", s)
        he = _he(o.split(r"\choice")[0])
        n = sum(1 for X in range(-10, 11) for Y in range(-10, 11) if _thoa(he, X, Y))
        pa = re.findall(r"\{(\\True )?\$(\d+)\$\}", o)
        assert len(pa) == 4 and len({v for _, v in pa}) == 4
        assert [int(v) for t, v in pa if t] == [n]


def test_mapping_va_tu_sinh():
    m = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C2.json", encoding="utf-8"))}
    assert m["L10_C2_B4_TH027_MC_D"]["Dang"] == m["L10_C2_B4_TH027_SA_D"]["Dang"]
    assert not m["L10_C2_B4_TH027_SA_D"].get("ngoai_yccd")
    de = {_chay("SA", s).split(r"\shortans")[0] for s in range(100)}
    assert len(de) >= 95
