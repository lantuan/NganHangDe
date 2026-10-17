# -*- coding: utf-8 -*-
r"""L10_C4_B8_VD040_B (bai 4.9 SGK, muc VD) va VD040_C (bai Van dung keo phao len doc, muc VDC) - co Lan 17/10/2026.

Kiem chung DOC LAP:
- B: doc goc, do lon tu de; doc them HINH TikZ (goc cuc, do dai) de chac hinh khop so lieu; dung hai luc bang toa do
  roi tinh |F1 + F2| hoac |F1 - F2|.
- C: dung mat doc nghieng alpha bang toa do, trong luc P = (0; -P), phan luc w vuong goc mat doc sao cho P + w nam doc
  mat doc (tinh bang phep chieu), F = -(P + w); so nguoi = so nguyen nho nhat k voi k.f >= |F| (vet can).
"""
import importlib.util
import json
import math
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC / "tests"))
from _tinh_tex import V, so, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C4_vd040bc", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_vd040bc"] = M
_spec.loader.exec_module(M)


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, hinh, *a, **k: cap.append((de, str(dap), list(nhieu), giai, hinh)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, "L10_C4_B8_VD040_" + ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _kiem_tron(de, dap, d):
    m = re.search(r"làm tròn kết quả đến (hàng đơn vị|hàng phần mười|hàng phần trăm)", de)
    if m:
        e = {"hàng đơn vị": 0.5, "hàng phần mười": 0.05, "hàng phần trăm": 0.005}[m.group(1)]
        assert abs(so(dap) - d) <= e + 1e-9, (de, dap, d)
    else:
        assert abs(so(dap) - d) < 1e-9, (de, dap, d)


# ---------------------------------------------------------------- B
@pytest.mark.parametrize("ten", ["MC_B_01", "SA_B_01"])
def test_b_hai_luc_tren_hinh(ten):
    hoi_thay, goc_thay = set(), set()
    for s in range(300):
        de, dap, nhieu, giai, hinh = _bat(ten, s)
        g, p, q = map(int, re.search(r"góc giữa hai lực bằng \$(\d+)\^\\circ\$, \$\\left\|\\overrightarrow\{F_1\}\\right\| = "
                                     r"(\d+)\$ N, \$\\left\|\\overrightarrow\{F_2\}\\right\| = (\d+)\$ N", de).groups())
        # hình khớp số liệu: góc giữa hai mũi tên = g, tỉ lệ độ dài = p : q
        (a1, d1), (a2, d2) = [(float(x), float(y)) for x, y in re.findall(r"\\draw\[->\] \(0,0\) -- \(([-\d.]+):([\d.]+)\)", hinh)]
        assert abs((a2 - a1) - g) < 1e-6 and abs(d1 / d2 - p / q) < 1e-3, (hinh, p, q, g)
        F1 = V(p * math.cos(math.radians(a1)), p * math.sin(math.radians(a1)))
        F2 = V(q * math.cos(math.radians(a2)), q * math.sin(math.radians(a2)))
        if "vectơ $\\overrightarrow{F_1} - \\overrightarrow{F_2}$" in de:
            d, hoi = abs(F1 - F2), "hieu"
        else:
            d, hoi = abs(F1 + F2), ("can_bang" if "đứng yên" in de else "tong")
        hoi_thay.add(hoi)
        goc_thay.add(g)
        if ten.startswith("MC"):
            gia = lambda x: tinh(x.replace(" N", "").strip("$"))
            assert abs(gia(dap) - d) < 1e-9, (de, dap, d)
            assert all(abs(gia(x) - d) > 1e-9 for x in nhieu) and len(set([dap] + nhieu)) == 4, (de, nhieu)
        else:
            _kiem_tron(de, dap, d)
            assert len(dap) <= 4
    assert hoi_thay == {"tong", "can_bang", "hieu"}
    assert goc_thay >= ({60, 90, 120} if ten.startswith("MC") else {30, 45, 60, 90, 120, 135, 150})


# ---------------------------------------------------------------- C (VDC)
@pytest.mark.parametrize("ten", ["MC_C_01", "SA_C_01"])
def test_c_keo_len_doc(ten):
    bc, hoi_thay = set(), set()
    for s in range(300):
        de, dap, nhieu, giai, hinh = _bat(ten, s)
        Pm, a = re.search(r"trọng lượng \$([\d\\,]+)\$ N lên (?:một con|một mặt) dốc nghiêng \$(\d+)\^\\circ\$", de).groups()
        Pm, a = int(Pm.replace(r"\,", "")), int(a)
        assert r"arc (0:%d:1)" % a in hinh                   # hình đúng góc nghiêng
        r = math.radians(a)
        u, n = V(math.cos(r), math.sin(r)), V(-math.sin(r), math.cos(r))
        Pv = V(0, -Pm)
        w = n * (-(Pv * n))                                  # phản lực: vuông góc mặt dốc, khử thành phần pháp tuyến của P
        F = -(Pv + w)
        assert abs(F * n) < 1e-6 and F * u > 0              # F nằm dọc dốc, hướng lên
        dv = "kN" if "kN" in dap or "kilôniutơn" in giai else "N"
        k = 1000 if dv == "kN" else 1
        m = re.search(r"lực kéo của mỗi người bằng \$(\d+)\$ N", de)
        if m:
            f = int(m.group(1))
            dung = next(x for x in range(1, 10000) if x * f >= abs(F) - 1e-9)
            got = int(re.search(r"\d+", dap).group(0))
            assert got == dung, (de, dap, dung)
            hoi_thay.add("nguoi")
        else:
            d = (abs(F) if "lực kéo" in de.split(". ")[-1] else abs(w)) / k
            hoi_thay.add("luc" if "lực kéo" in de.split(". ")[-1] else "phan_luc")
            _kiem_tron(de, re.search(r"[\d,]+", dap).group(0), d)
        if ten.startswith("MC"):
            assert len(set([dap] + nhieu)) == 4 and dap not in nhieu
        else:
            assert len(dap) <= 4, dap
        bc.add(re.search(r"khẩu pháo|xe chở hàng|khúc gỗ", de).group(0))
    assert bc == {"khẩu pháo", "xe chở hàng", "khúc gỗ"} and hoi_thay == {"nguoi", "luc", "phan_luc"}


def test_mapping_vdc_va_luyen_tap_them():
    m = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C4.json", encoding="utf-8"))}
    for i in ("MC_B", "SA_B", "MC_C", "SA_C"):
        assert m["L10_C4_B8_VD040_" + i]["ngoai_yccd"] is True
    assert m["L10_C4_B8_VD040_MC_C"]["muc_do_dang"] == m["L10_C4_B8_VD040_SA_C"]["muc_do_dang"] == "VDC"
    assert "muc_do_dang" not in m["L10_C4_B8_VD040_MC_B"]
    assert m["L10_C4_B8_VD040_MC_B"]["Dang"] == m["L10_C4_B8_VD040_SA_B"]["Dang"]
    assert m["L10_C4_B8_VD040_MC_C"]["Dang"] == m["L10_C4_B8_VD040_SA_C"]["Dang"]
    khac = set()
    for f in (GOC / "data" / "mapping" / "toan10").glob("*.json"):
        for r in json.load(open(f, encoding="utf-8")):
            if not r["id"].startswith("L10_C4_B8_VD040_"):
                b = r.get("boi_canh")
                khac.update(b if isinstance(b, list) else [b] if b else [])
    assert not khac & set(m["L10_C4_B8_VD040_MC_C"]["boi_canh"])


def test_python_tu_sinh():
    for ten in ("MC_B_01", "SA_B_01", "MC_C_01", "SA_C_01"):
        de = set()
        for s in range(100):
            random.seed(s)
            o = getattr(M, "L10_C4_B8_VD040_" + ten)(1)
            de.add(o.split(r"\choice")[0].split(r"\shortans")[0])
        assert len(de) >= 80, (ten, len(de))
