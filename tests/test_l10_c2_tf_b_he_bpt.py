"""L10_C2_TF_B_01: moi y it nhat 3 dung + 3 sai; dung/sai kiem lai DOC LAP tu he trong cau.

Doc he \\heva{...} va F ngay trong de, tinh dinh (giao cac duong bo), dien tich (shoelace), F tai
cac dinh, roi so voi nhan \\True cua tung phat bieu. (co Lan 09/10/2026)
"""
import importlib.util
import itertools
import re
import sys
from fractions import Fraction
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))

_spec = importlib.util.spec_from_file_location("L10_C2_tfb_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_tfb_test"] = M
_spec.loader.exec_module(M)

_cap = {}


def _chup(monkeypatch):
    def _fake(debai, ys, *a, **k):
        _cap["debai"], _cap["ys"] = debai, ys
        return ""
    monkeypatch.setattr(M, "TF_baitoan_du", _fake)


def _he_so(s):
    s = s.replace(" ", "")
    mm = re.fullmatch(r"(-?\d*)x([+-]\d*)y", s)
    assert mm, s
    f = lambda t: {"": 1, "-": -1, "+": 1}.get(t, None) if t in ("", "-", "+") else int(t)
    return f(mm.group(1)), f(mm.group(2))


def _bpt(s):
    mm = re.fullmatch(r"(.+?) \\le (-?\d+)", s.strip())
    assert mm, s
    a, b = _he_so(mm.group(1))
    return a, b, int(mm.group(2))


def _doc_de(debai):
    mm = re.search(r"\\heva\{& x \\ge 0 \\\\ & y \\ge 0 \\\\ & (.+?) \\\\ & (.+?)\}\$ và biểu thức "
                   r"\$F\\left\(x; y\\right\) = (.+?)\$", debai)
    assert mm, debai
    l1, l2 = _bpt(mm.group(1)), _bpt(mm.group(2))
    ff = mm.group(3).replace(" ", "")
    m2 = re.fullmatch(r"(\d*)x\+(\d*)y", ff)
    assert m2, ff
    p, q = int(m2.group(1) or 1), int(m2.group(2) or 1)
    return l1, l2, p, q


def _hinh(l1, l2):
    duong = [(1, 0, 0), (0, 1, 0), l1, l2]               # a x + b y = c
    thuoc = lambda X, Y: X >= 0 and Y >= 0 and l1[0] * X + l1[1] * Y <= l1[2] and l2[0] * X + l2[1] * Y <= l2[2]
    dinh = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(duong, 2):
        D = a1 * b2 - a2 * b1
        if D == 0:
            continue
        X = Fraction(c1 * b2 - c2 * b1, D)
        Y = Fraction(a1 * c2 - a2 * c1, D)
        if thuoc(X, Y):
            dinh.add((X, Y))
    dinh = sorted(dinh)
    cx = sum(d[0] for d in dinh) / len(dinh)
    cy = sum(d[1] for d in dinh) / len(dinh)
    import math
    dinh.sort(key=lambda d: math.atan2(d[1] - cy, d[0] - cx))
    S = abs(sum(dinh[i][0] * dinh[(i + 1) % len(dinh)][1] - dinh[(i + 1) % len(dinh)][0] * dinh[i][1]
                for i in range(len(dinh)))) / 2
    return thuoc, dinh, S


def _so(t):
    t = t.strip()
    mm = re.fullmatch(r"\\dfrac\{(\d+)\}\{(\d+)\}", t)
    return Fraction(int(mm.group(1)), int(mm.group(2))) if mm else Fraction(int(t))


def test_moi_y_it_nhat_3_dung_3_sai(monkeypatch):
    _chup(monkeypatch)
    for _ in range(200):
        M.L10_C2_TF_B_01(1)
        assert len(_cap["ys"]) == 4
        for i, y in enumerate(_cap["ys"]):
            d = sum(1 for t, _ in y if "\\True" in t)
            assert d >= 3 and len(y) - d >= 3, ("abcd"[i], d, len(y) - d)


def test_dung_sai_tinh_doc_lap(monkeypatch):
    _chup(monkeypatch)
    for _ in range(150):
        M.L10_C2_TF_B_01(1)
        l1, l2, p, q = _doc_de(_cap["debai"])
        thuoc, dinh, S = _hinh(l1, l2)
        Fv = {d: p * d[0] + q * d[1] for d in dinh}
        lon, nho = max(Fv.values()), min(Fv.values())
        da_gap = [0, 0, 0, 0]
        for k, y in enumerate(_cap["ys"]):
            for text, _ly in y:
                dung = "\\True" in text
                nd = text.replace("\\True ", "").strip("{}")
                da_gap[k] += 1
                if k == 0:
                    if "không phải là hệ" in nd:
                        kq = False
                    elif "là hệ bất phương trình bậc nhất" in nd:
                        kq = True
                    elif (mm := re.search(r"gồm \$(\d+)\$ bất phương trình", nd)):
                        kq = int(mm.group(1)) == 4
                    elif "một bất phương trình không phải" in nd:
                        kq = False
                    elif nd.startswith("Mỗi bất phương trình"):
                        kq = True
                    elif (mm := re.search(r"Bất phương trình \$(.+?)\$ có hệ số của \$(x|y)\$ bằng \$(-?\d+)\$", nd)):
                        a, b, _c = _bpt(mm.group(1))
                        kq = (a if mm.group(2) == "x" else b) == int(mm.group(3))
                    else:
                        raise AssertionError(nd)
                elif k == 1:
                    mm = re.fullmatch(r"Điểm \$\\left\((-?\d+); (-?\d+)\\right\)\$ (không thuộc|thuộc) miền nghiệm của hệ", nd)
                    assert mm, nd
                    ok = thuoc(int(mm.group(1)), int(mm.group(2)))
                    kq = ok if mm.group(3) == "thuộc" else not ok
                elif k == 2:
                    if "miền tứ giác" in nd:
                        kq = len(dinh) == 4
                    elif "miền tam giác" in nd:
                        kq = len(dinh) == 3
                    elif "không bị chặn" in nd:
                        kq = False                      # co x,y >= 0 va hai bpt ... luon bi chan o tu giac nay
                    elif "miền bị chặn" in nd:
                        kq = True
                    elif (mm := re.search(r"có đúng \$(\d+)\$ đỉnh", nd)):
                        kq = int(mm.group(1)) == len(dinh)
                    elif (mm := re.search(r"Điểm \$\\left\((-?\d+); (-?\d+)\\right\)\$ là một đỉnh", nd)):
                        kq = (Fraction(int(mm.group(1))), Fraction(int(mm.group(2)))) in dinh
                    elif (mm := re.search(r"diện tích bằng \$(.+?)\$ \(đơn vị", nd)):
                        kq = _so(mm.group(1)) == S
                    else:
                        raise AssertionError(nd)
                else:
                    if (mm := re.search(r"Giá trị lớn nhất của \$F\$ trên miền nghiệm bằng \$(-?\d+)\$", nd)):
                        kq = int(mm.group(1)) == lon
                    elif (mm := re.search(r"đạt giá trị lớn nhất tại điểm \$\\left\((-?\d+); (-?\d+)\\right\)\$", nd)):
                        kq = Fv.get((Fraction(int(mm.group(1))), Fraction(int(mm.group(2))))) == lon
                    elif (mm := re.search(r"Giá trị nhỏ nhất của \$F\$ trên miền nghiệm bằng \$(-?\d+)\$", nd)):
                        kq = int(mm.group(1)) == nho
                    elif "đạt giá trị nhỏ nhất tại gốc toạ độ" in nd:
                        kq = Fv[(Fraction(0), Fraction(0))] == nho
                    elif (mm := re.search(r"Tại đỉnh \$\\left\((-?\d+); (-?\d+)\\right\)\$, biểu thức \$F\$ nhận giá trị \$(-?\d+)\$", nd)):
                        kq = Fv.get((Fraction(int(mm.group(1))), Fraction(int(mm.group(2))))) == int(mm.group(3))
                    elif "không có giá trị lớn nhất" in nd:
                        kq = False
                    else:
                        raise AssertionError(nd)
                assert dung == kq, (nd, dung, kq, l1, l2, p, q)
        assert all(da_gap)
