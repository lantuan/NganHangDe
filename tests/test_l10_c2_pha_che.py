"""Tinh huong 1 (pha che nuoc, boi_canh pha_che) cua L10_C2: kiem lai DOC LAP dap an tu so lieu trong de.

Doc cac so trong cau dan, tu giai bang giao cac duong bien (phan so), roi so voi dap an / nhan \\True
cua tung ham. (co Lan 09/10/2026)
"""
import importlib.util
import itertools
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))

_spec = importlib.util.spec_from_file_location("L10_C2_pc_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_pc_test"] = M
_spec.loader.exec_module(M)

_cap = {}


@pytest.fixture(autouse=True)
def _chup(monkeypatch):
    _cap.clear()

    def mcsa(debai, dap, nhieu, giai, *a):
        _cap.setdefault("mc", []).append((debai, dap, list(nhieu), giai))
        return ""

    def tl(debai, ds, *a):
        _cap.setdefault("tl", []).append((debai, ds))
        return ""

    def tf(debai, ys, *a, **k):
        _cap["tf"] = (debai, ys)
        return ""
    monkeypatch.setattr(M, "MC_SA_answer_text", mcsa)
    monkeypatch.setattr(M, "TL_answer_text", tl)
    monkeypatch.setattr(M, "TF_baitoan_du", tf)


def _so(s):
    return Fraction(s.replace("{,}", ".").strip())


def _doc(debai):
    """-> dict(H, N, D, ad, ah, bd, bh, p, q) tu cau dan."""
    n = r"(\d+(?:\{,\}\d+)?)"
    r = re.search(r"tối đa \$%s\$ g hương liệu, \$%s\$ lít nước và \$%s\$ g đường" % (n, n, n), debai)
    A = re.search(r"nước A cần \$%s\$ g đường, \$1\$ lít nước và \$%s\$ g hương liệu" % (n, n), debai)
    B = re.search(r"nước B cần \$%s\$ g đường, \$1\$ lít nước và \$%s\$ g hương liệu" % (n, n), debai)
    P = re.search(r"nước A nhận được \$(\d+)\$ điểm thưởng, mỗi lít nước B nhận được \$(\d+)\$ điểm", debai)
    assert r and A and B and P, debai
    return dict(H=_so(r.group(1)), N=_so(r.group(2)), D=_so(r.group(3)), ad=_so(A.group(1)), ah=_so(A.group(2)),
                bd=_so(B.group(1)), bh=_so(B.group(2)), p=int(P.group(1)), q=int(P.group(2)))


def _giai(d):
    """Giao cac duong bien -> (ham thoa, dinh theo thu tu quanh, F tai dinh)."""
    duong = [(Fraction(1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(1), Fraction(0)),
             (d["ah"], d["bh"], d["H"]), (Fraction(1), Fraction(1), d["N"]), (d["ad"], d["bd"], d["D"])]
    thoa = lambda X, Y: X >= 0 and Y >= 0 and all(a * X + b * Y <= c for a, b, c in duong[2:])
    dinh = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(duong, 2):
        D = a1 * b2 - a2 * b1
        if D == 0:
            continue
        X, Y = (c1 * b2 - c2 * b1) / D, (a1 * c2 - a2 * c1) / D
        if thoa(X, Y):
            dinh.add((X, Y))
    dinh = sorted(dinh)
    cx = sum(v[0] for v in dinh) / len(dinh)
    cy = sum(v[1] for v in dinh) / len(dinh)
    dinh.sort(key=lambda v: math.atan2(v[1] - cy, v[0] - cx))
    F = {v: d["p"] * v[0] + d["q"] * v[1] for v in dinh}
    return thoa, dinh, F


def _bpt(s):
    """'0{,}5x + 2y \\le 12' -> (a, b, dau, c)."""
    m = re.fullmatch(r"\s*([\d{},]*)x \+ ([\d{},]*)y (\\le|\\ge|<) ([\d{},]+)\s*", s)
    assert m, s
    he = lambda t: Fraction(1) if t == "" else _so(t)
    return he(m.group(1)), he(m.group(2)), m.group(3), _so(m.group(4))


def _chay(ten, n=60):
    f = getattr(M, ten)
    for _ in range(n):
        _cap.clear()
        f(1)
        yield


def test_nb025_mot_bpt():
    for ten, k in (("L10_C2_B3_NB025_MC_B_01", "đường"), ("L10_C2_B3_NB025_MC_B_02", "nước"), ("L10_C2_B3_NB025_MC_B_03", "hương liệu")):
        for _ in _chay(ten):
            debai, dap, nhieu, _g = _cap["mc"][0]
            d = _doc(debai)
            assert ("lượng %s" % k) in debai
            exp = {"đường": (d["ad"], d["bd"], d["D"]), "nước": (1, 1, d["N"]), "hương liệu": (d["ah"], d["bh"], d["H"])}[k]
            a, b, dau, c = _bpt(dap.strip("$"))
            assert (a, b, c) == tuple(Fraction(v) for v in exp) and dau == r"\le"
            assert len(set(nhieu + [dap])) == 4
            for x in nhieu:
                assert _bpt(x.strip("$")) != (a, b, dau, c)


def _he_tu_chuoi(s):
    m = re.fullmatch(r"\$\\heva\{& x \\ge 0 \\\\ & y \\ge 0 \\\\ & (.+?) \\\\ & (.+?) \\\\ & (.+?)\}\$", s)
    assert m, s
    return [_bpt(g) for g in m.groups()]


def test_mc_b_01_he():
    for _ in _chay("L10_C2_B4_VD028_MC_B_01"):
        debai, dap, nhieu, _g = _cap["mc"][0]
        d = _doc(debai)
        dung = {(d["ah"], d["bh"], r"\le", d["H"]), (Fraction(1), Fraction(1), r"\le", d["N"]), (d["ad"], d["bd"], r"\le", d["D"])}
        assert set(_he_tu_chuoi(dap)) == dung
        for x in nhieu:
            assert set(_he_tu_chuoi(x)) != dung


def test_mc_b_02_phuong_an_kha_thi():
    for _ in _chay("L10_C2_B4_VD028_MC_B_02"):
        debai, dap, nhieu, _g = _cap["mc"][0]
        d = _doc(debai)
        thoa, _, _ = _giai(d)
        P = lambda s: tuple(int(v) for v in re.findall(r"-?\d+", s))
        assert thoa(*P(dap))
        for x in nhieu:
            assert not thoa(*P(x))


def test_mc_b_03_diem_thuong():
    for _ in _chay("L10_C2_B4_VD028_MC_B_03"):
        debai, dap, nhieu, _g = _cap["mc"][0]
        d = _doc(debai)
        X, Y = (int(v) for v in re.search(r"pha chế \$(\d+)\$ lít nước A và \$(\d+)\$ lít nước B \(", debai).groups())
        thoa, _, _ = _giai(d)
        assert thoa(X, Y)
        assert int(dap.strip("$")) == d["p"] * X + d["q"] * Y
        assert all(int(x.strip("$")) != int(dap.strip("$")) for x in nhieu)


@pytest.mark.parametrize("ten,hoi", [("L10_C2_B4_VD028_MC_C_01", "diem"), ("L10_C2_B4_VD028_MC_C_02", "A"), ("L10_C2_B4_VD028_MC_C_03", "B"),
                                     ("L10_C2_B4_VD028_SA_C_01", "diem"), ("L10_C2_B4_VD028_SA_C_02", "A"), ("L10_C2_B4_VD028_SA_C_03", "B")])
def test_toi_uu(ten, hoi):
    for _ in _chay(ten):
        debai, dap, nhieu, _g = _cap["mc"][0]
        d = _doc(debai)
        _, dinh, F = _giai(d)
        lon = max(F.values())
        assert list(F.values()).count(lon) == 1
        opt = [v for v in dinh if F[v] == lon][0]
        exp = {"diem": lon, "A": opt[0], "B": opt[1]}[hoi]
        assert Fraction(int(dap.strip("$"))) == exp
        assert all(int(x.strip("$")) != exp for x in nhieu)


@pytest.mark.parametrize("ten,hoi", [("L10_C2_B4_VD028_SA_B_01", "dinh"), ("L10_C2_B4_VD028_SA_B_02", "x"), ("L10_C2_B4_VD028_SA_B_03", "y")])
def test_sa_b(ten, hoi):
    for _ in _chay(ten):
        debai, dap, nhieu, _g = _cap["mc"][0]
        d = _doc(debai)
        _, dinh, _F = _giai(d)
        exp = {"dinh": len(dinh), "x": max(v[0] for v in dinh), "y": max(v[1] for v in dinh)}[hoi]
        assert Fraction(int(dap)) == exp
        assert all(int(x) != int(dap) for x in nhieu)


def test_tl_b():
    for _ in _chay("L10_C2_B4_VD028_TL_B_01"):
        debai, ds = _cap["tl"][0]
        assert len(ds) == 2                               # tu luan chi 2 y
        d = _doc(debai)
        _, dinh, F = _giai(d)
        lon = max(F.values())
        opt = [v for v in dinh if F[v] == lon][0]
        he = ds[0][1]
        gs = re.fullmatch(r"\\heva\{& x \\ge 0 \\\\ & y \\ge 0 \\\\ & (.+?) \\\\ & (.+?) \\\\ & (.+?)\}", he)
        assert {_bpt(g) for g in gs.groups()} == {(d["ah"], d["bh"], r"\le", d["H"]), (Fraction(1), Fraction(1), r"\le", d["N"]), (d["ad"], d["bd"], r"\le", d["D"])}
        assert tuple(int(v) for v in re.findall(r"-?\d+", ds[1][1])) == (opt[0], opt[1])
        assert ("$%d$" % lon) in ds[1][2]


def test_tf_c_moi_y_it_nhat_3_dung_3_sai():
    for _ in _chay("L10_C2_TF_C_01", 200):
        ys = _cap["tf"][1]
        assert len(ys) == 4
        for i, y in enumerate(ys):
            dg = sum(1 for t, _ in y if "\\True" in t)
            assert dg >= 3 and len(y) - dg >= 3, ("abcd"[i], dg, len(y) - dg)


def test_tf_c_dung_sai_tinh_doc_lap():
    for _ in _chay("L10_C2_TF_C_01", 120):
        debai, ys = _cap["tf"]
        d = _doc(debai)
        thoa, dinh, F = _giai(d)
        lon = max(F.values())
        opt = [v for v in dinh if F[v] == lon][0]
        ten2k = {"hương liệu": (d["ah"], d["bh"], d["H"]), "nước": (Fraction(1), Fraction(1), d["N"]), "đường": (d["ad"], d["bd"], d["D"])}
        dinh_set = {(int(v[0]), int(v[1])) for v in dinh if v[0].denominator == 1 and v[1].denominator == 1}
        for k, y in enumerate(ys):
            for text, _ly in y:
                dung = "\\True" in text
                nd = text.replace("\\True ", "").strip("{}")
                if k == 0:
                    if nd.startswith("Hai điều kiện"):
                        kq = True
                    else:
                        mm = re.fullmatch(r"Điều kiện về lượng (.+?) được biểu thị bởi bất phương trình \$(.+)\$", nd)
                        assert mm, nd
                        a, b, dau, c = _bpt(mm.group(2))
                        kq = ((a, b, c) == tuple(Fraction(v) for v in ten2k[mm.group(1)])) and dau == r"\le"
                elif k == 1:
                    mm = re.fullmatch(r"Phương án pha chế \$(\d+)\$ lít nước A và \$(\d+)\$ lít nước B (không )?thoả mãn mọi điều kiện của bài toán", nd)
                    assert mm, nd
                    ok = thoa(int(mm.group(1)), int(mm.group(2)))
                    kq = (not ok) if mm.group(3) else ok
                elif k == 2:
                    if (mm := re.search(r"có \$(\d+)\$ đỉnh", nd)):
                        kq = int(mm.group(1)) == len(dinh)
                    elif "không bị chặn" in nd:
                        kq = False
                    elif "bị chặn" in nd:
                        kq = True
                    elif (mm := re.search(r"Điểm \$\\left\((\d+); (\d+)\\right\)\$ là một đỉnh", nd)):
                        kq = (int(mm.group(1)), int(mm.group(2))) in dinh_set
                    else:
                        raise AssertionError(nd)
                else:
                    if (mm := re.search(r"điểm thưởng cao nhất mà một đội có thể nhận được bằng \$(\d+)\$", nd)):
                        kq = int(mm.group(1)) == lon
                    elif (mm := re.search(r"cao nhất đạt được khi pha chế \$(\d+)\$ lít nước A và \$(\d+)\$ lít nước B", nd)):
                        kq = (int(mm.group(1)), int(mm.group(2))) == opt
                    elif (mm := re.search(r"tổng lượng nước đã dùng là \$(\d+)\$ lít", nd)):
                        kq = opt[0] + opt[1] == int(mm.group(1))
                    elif (mm := re.search(r"Pha chế \$(\d+)\$ lít nước A và không pha nước B thì nhận được \$(\d+)\$ điểm", nd)):
                        kq = d["p"] * int(mm.group(1)) == int(mm.group(2)) and thoa(int(mm.group(1)), 0)
                    elif (mm := re.search(r"Pha chế \$(\d+)\$ lít nước B và không pha nước A thì nhận được \$(\d+)\$ điểm", nd)):
                        kq = d["q"] * int(mm.group(1)) == int(mm.group(2)) and thoa(0, int(mm.group(1)))
                    elif (mm := re.search(r"Pha chế \$(\d+)\$ lít nước A và không pha nước B thì nhận được số điểm thưởng cao nhất", nd)):
                        kq = d["p"] * int(mm.group(1)) == lon
                    elif (mm := re.search(r"Pha chế \$(\d+)\$ lít nước B và không pha nước A thì nhận được số điểm thưởng cao nhất", nd)):
                        kq = d["q"] * int(mm.group(1)) == lon
                    else:
                        raise AssertionError(nd)
                assert dung == kq, (nd, dung, kq)
