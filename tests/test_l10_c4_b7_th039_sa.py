# -*- coding: utf-8 -*-
r"""TH039 ban tra loi ngan (co Lan 17/10/2026: o SA TH Bai 7 trong khi chon "Chi theo YCCD"):
SA_B (dem cap luc tren luoi), SA_C (doc toc do theo huong tren luoi co la ban), SA_D (dem khang dinh dung - song / xe).

Kiem chung DOC LAP: doc toa do mui ten tu chinh hinh TikZ; bai song / xe dung vecto van toc tu cau dan (truc Ox theo dong
nuoc / truc Oy theo huong bac) roi xet tung khang dinh.
"""
import importlib.util
import itertools
import json
import math
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C4_th039sa", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_th039sa"] = M
_spec.loader.exec_module(M)


def _bat(ten, seed):
    cap = []
    g = M.MC_SA_answer_const
    M.MC_SA_answer_const = lambda de, dap, nhieu, giai, hinh, *a, **k: cap.append((de, str(dap), list(nhieu), giai, hinh)) or ""
    try:
        random.seed(seed)
        getattr(M, "L10_C4_B7_TH039_" + ten)(1)
    finally:
        M.MC_SA_answer_const = g
    assert len(cap) == 1
    return cap[0]


def _mui_ten(hinh):
    """{nhãn: (dx, dy)} đọc từ TikZ."""
    return {t: (int(x2) - int(x1), int(y2) - int(y1)) for x1, y1, x2, y2, t in re.findall(
        r"\\draw\[->, very thick\] \((-?\d+),(-?\d+)\) -- \((-?\d+),(-?\d+)\) node\[[^\]]*\]\{\\footnotesize \$([^$]+)\$\}", hinh)}


def _qh(u, v):
    if u == v:
        return "bằng nhau"
    if u[0] * v[1] - u[1] * v[0] != 0:
        return "không cùng phương"
    return "cùng hướng" if u[0] * v[0] + u[1] * v[1] > 0 else "ngược hướng"


def test_sa_b_dem_cap_luc():
    thay = set()
    for s in range(300):
        de, dap, nhieu, giai, hinh = _bat("SA_B_01", s)
        V = _mui_ten(hinh)
        assert len(V) == 4
        hoi = re.search(r"\\textbf\{([^}]+)\}", de).group(1)
        dem = 0
        for a, b in itertools.combinations(sorted(V), 2):
            q = _qh(V[a], V[b])
            dem += {"cùng hướng": q in ("cùng hướng", "bằng nhau"), "cùng phương": q != "không cùng phương"}.get(hoi, q == hoi)
        assert int(dap) == dem and 1 <= dem <= 4, (de, hinh, dap, dem)
        thay.add(hoi)
    assert thay == {"cùng hướng", "ngược hướng", "bằng nhau", "cùng phương"}


LA_BAN = {"đông": (1, 0), "tây": (-1, 0), "bắc": (0, 1), "nam": (0, -1)}


def test_sa_c_doc_toc_do():
    cheo = thang = 0
    for s in range(300):
        de, dap, nhieu, giai, hinh = _bat("SA_C_01", s)
        h = re.search(r"di chuyển theo hướng (\S+(?: \S+)?)\. ", de).group(1)
        x = sum(LA_BAN[t][0] for t in h.split())
        y = sum(LA_BAN[t][1] for t in h.split())
        V = _mui_ten(hinh)
        hop = [v for v in V.values() if v[0] * y - v[1] * x == 0 and v[0] * x + v[1] * y > 0]
        assert len(hop) == 1, (de, hinh)                     # đúng một vectơ theo hướng hỏi
        d = 10 * math.hypot(*hop[0])
        if "làm tròn kết quả đến hàng đơn vị" in de:
            assert abs(int(dap) - d) <= 0.5 and abs(d - round(d)) > 1e-9
            cheo += 1
        else:
            assert int(dap) == round(d) and abs(d - round(d)) < 1e-9
            thang += 1
        assert len(dap) <= 4
    assert cheo and thang


def _song_xe(de):
    m = re.search(r"Thuyền \$A\$ đi xuôi dòng, thuyền \$B\$ đi ngược dòng, thuyền \$C\$ đi xuôi dòng; .+ với độ lớn \$(\d+)\$ "
                  r"km/h, \$(\d+)\$ km/h, \$(\d+)\$ km/h", de)
    vn = re.search(r"vận tốc dòng nước là \$\\overrightarrow\{v_n\}\$ \(\$(\d+)\$ km/h\)", de)
    if m:
        a, b, c = map(int, m.groups())
        return {"v_n": (int(vn.group(1)), 0), "v_A": (a, 0), "v_B": (-b, 0), "v_C": (c, 0)}
    m = re.search(r"xe \$A\$ chạy về phía bắc với tốc độ \$(\d+)\$ km/h, xe \$B\$ chạy về phía nam với tốc độ \$(\d+)\$ km/h, "
                  r"xe \$C\$ chạy về phía bắc với tốc độ \$(\d+)\$ km/h", de)
    a, b, c = map(int, m.groups())
    return {"v_A": (0, a), "v_B": (0, -b), "v_C": (0, c)}


def _dung(kd, V):
    vt = re.findall(r"\\overrightarrow\{(v_\w)\}", kd)
    u, w = V[vt[0]], V[vt[1]]
    if r"\left|" in kd:
        return math.hypot(*u) == math.hypot(*w)
    if " = " in kd:
        return u == w
    q = _qh(u, w)
    if "không cùng phương" in kd:
        return q == "không cùng phương"
    if "cùng phương" in kd:
        return q != "không cùng phương"
    if "cùng hướng" in kd:
        return q in ("cùng hướng", "bằng nhau")
    assert "ngược hướng" in kd, kd
    return q == "ngược hướng"


def test_sa_d_dem_khang_dinh():
    thay = set()
    for s in range(300):
        de, dap, nhieu, giai, hinh = _bat("SA_D_01", s)
        V = _song_xe(de)
        kd = re.findall(r"\d\) (.+?);(?:\\\\|$)", de)
        assert len(kd) == 4
        assert int(dap) == sum(_dung(x, V) for x in kd), (de, dap)
        thay.add(int(dap))
    assert thay == {1, 2, 3}


def test_mapping_ngoai_le():
    m = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C4.json", encoding="utf-8"))}
    for L in "BCD":
        assert m["L10_C4_B7_TH039_SA_" + L]["Dang"] == m["L10_C4_B7_TH039_MC_" + L]["Dang"]
        assert not m["L10_C4_B7_TH039_SA_" + L].get("ngoai_yccd")
    nl = json.load(open(GOC / "data" / "mapping" / "id_mc_sa_ngoai_le.json", encoding="utf-8"))["L10_C4"]
    assert "L10_C4_B7_TH039_MC_A" in nl


def test_python_tu_sinh():
    for ten in ("SA_B_01", "SA_C_01", "SA_D_01"):
        de = set()
        for s in range(100):
            random.seed(s)
            o = getattr(M, "L10_C4_B7_TH039_" + ten)(1)
            assert r"\shortans" in o and r"\choice" not in o
            de.add(o.split(r"\shortans")[0])
        assert len(de) >= 60, (ten, len(de))
