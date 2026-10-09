"""Dien tich mien nghiem la tam giac (VD028, ngoai_yccd) cua L10_C2: kiem lai DOC LAP.

Parse chinh he bat phuong trinh trong de, tu giao cac duong thang (phan so), tinh dien tich bang cong thuc
day gio, roi so voi dap an. Voi bien the co tham so: thay m dung -> dien tich dung, thay m sai -> mien rong.
(co Lan 09/10/2026)
"""
import importlib.util
import itertools
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C2_dt_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_dt_test"] = M
_spec.loader.exec_module(M)

_cap = {}


@pytest.fixture(autouse=True)
def _chup(monkeypatch):
    _cap.clear()
    monkeypatch.setattr(M, "MC_SA_answer_text", lambda d, dap, nh, g, *a: _cap.setdefault("mc", []).append((d, dap, list(nh), g)) or "")
    monkeypatch.setattr(M, "TL_answer_text", lambda d, ds, *a: _cap.setdefault("tl", []).append((d, ds)) or "")


def _hs(tok):
    tok = tok.strip()
    m = re.fullmatch(r"(-?)(\d*)", tok)
    return -1 if m.group(1) and not m.group(2) else (1 if not m.group(2) else int(m.group(2)) * (-1 if m.group(1) else 1))


def _doc_he(debai):
    """-> list (a, b, c, dau) tu \\heva{...}; m duoc thay bang chuoi 'm'."""
    he = re.search(r"\\heva\{(.*?)\}\$", debai).group(1)
    kq = []
    for dong in he.split(r"\\"):
        dong = dong.replace("&", "").strip()
        m = re.fullmatch(r"(.+?) (\\le|\\ge) (-?\d+|m)", dong)
        assert m, dong
        lhs, dau, c = m.groups()
        a = b = 0
        for dau_t, he_so, bien in re.findall(r"([+-]?)\s*(\d*)\s*([xy])", lhs.replace(" - ", " -").replace(" + ", " +")):
            v = int(he_so) if he_so else 1
            if dau_t == "-":
                v = -v
            if bien == "x":
                a = v
            else:
                b = v
        kq.append((a, b, c, dau))
    return kq


def _dien_tich(he, m=None):
    """Giao tung cap duong thang, giu cac diem thoa he; tra (cac dinh, dien tich)."""
    ds = [(a, b, Fraction(m if c == "m" else int(c)), dau) for a, b, c, dau in he]
    thoa = lambda X, Y: all((a * X + b * Y <= c) if dau == r"\le" else (a * X + b * Y >= c) for a, b, c, dau in ds)
    dinh = set()
    for (a1, b1, c1, _), (a2, b2, c2, _) in itertools.combinations(ds, 2):
        D = a1 * b2 - a2 * b1
        if D == 0:
            continue
        X, Y = (c1 * b2 - c2 * b1) / D, (a1 * c2 - a2 * c1) / D
        if thoa(X, Y):
            dinh.add((X, Y))
    dinh = sorted(dinh)
    if len(dinh) != 3:
        return dinh, Fraction(0)
    (x1, y1), (x2, y2), (x3, y3) = dinh
    return dinh, abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2


def _chay(ten, n=80):
    out = []
    for _ in range(n):
        _cap.clear()
        getattr(M, ten)(1)
        out.append(_cap["mc"][0] if "mc" in _cap else _cap["tl"][0])
    return out


def _so_dau(s):
    return int(re.sub(r"[^\d-]", "", s))


@pytest.mark.parametrize("ten,hoi", [("L10_C2_B4_VD028_MC_J_01", "dt"), ("L10_C2_B4_VD028_SA_J_01", "dt")])
def test_dien_tich_vd(ten, hoi):
    for debai, dap, nh, giai in _chay(ten):
        dinh, S = _dien_tich(_doc_he(debai))
        assert len(dinh) == 3
        assert S == int(dap) and S.denominator == 1 and S >= 3
        assert dap not in nh and len(set(nh)) == len(nh)


def test_mc_dinh_va_canh():
    for debai, dap, nh, giai in _chay("L10_C2_B4_VD028_MC_J_02"):
        he = _doc_he(debai)
        dinh, S = _dien_tich(he)
        k = int(re.search(r"đường thẳng \$([xy]) = (-?\d+)\$", debai).group(2))
        bien = re.search(r"đường thẳng \$([xy]) = (-?\d+)\$", debai).group(1)
        i = 0 if bien == "x" else 1
        A = [P for P in dinh if P[i] != k]
        assert len(A) == 1
        X, Y = map(int, re.findall(r"-?\d+", dap))
        assert (X, Y) == A[0]
    for debai, dap, nh, giai in _chay("L10_C2_B4_VD028_MC_J_03"):
        dinh, S = _dien_tich(_doc_he(debai))
        bien = re.search(r"đường thẳng \$([xy]) = (-?\d+)\$", debai).group(1)
        k = int(re.search(r"đường thẳng \$([xy]) = (-?\d+)\$", debai).group(2))
        i = 0 if bien == "x" else 1
        B = [P for P in dinh if P[i] == k]
        assert abs(B[0][1 - i] - B[1][1 - i]) == int(dap)


def test_sa_tong():
    for debai, dap, nh, giai in _chay("L10_C2_B4_VD028_SA_J_02"):
        dinh, S = _dien_tich(_doc_he(debai))
        assert sum(x + y for x, y in dinh) == int(dap)


@pytest.mark.parametrize("ten", ["L10_C2_B4_VD028_MC_K_01", "L10_C2_B4_VD028_SA_K_01"])
def test_tim_m(ten):
    for debai, dap, nh, giai in _chay(ten):
        he = _doc_he(debai)
        S = int(re.search(r"diện tích bằng \$(\d+)\$", debai).group(1))
        m = _so_dau(dap)
        dinh, dt = _dien_tich(he, m)
        assert len(dinh) == 3 and dt == S, (debai, m, dt)
        # nghiem doi xung qua dinh A con lai phai lam mien rong / khong con la tam giac dien tich S
        for o in nh:
            if "m =" in o or ten.endswith("SA_K_01"):
                mo = _so_dau(o)
                d2, t2 = _dien_tich(he, mo)
                assert not (len(d2) == 3 and t2 == S), (debai, o)


def test_tap_m():
    for debai, dap, nh, giai in _chay("L10_C2_B4_VD028_MC_K_02"):
        he = _doc_he(debai)
        S = int(re.search(r"diện tích bằng \$(\d+)\$", debai).group(1))
        tap = lambda s: {int(v) for v in re.findall(r"-?\d+", s)}
        dung = tap(dap)
        # tim moi m nguyen hop le bang vet can
        hop = {m for m in range(-60, 61) if (lambda r: len(r[0]) == 3 and r[1] == S)(_dien_tich(he, m))}
        assert dung == hop, (debai, dung, hop)
        assert dap not in nh


def test_sa_canh_tham_so():
    for debai, dap, nh, giai in _chay("L10_C2_B4_VD028_SA_K_02"):
        he = _doc_he(debai)
        S = int(re.search(r"diện tích bằng \$(\d+)\$", debai).group(1))
        hop = [m for m in range(-60, 61) if (lambda r: len(r[0]) == 3 and r[1] == S)(_dien_tich(he, m))]
        assert len(hop) == 1
        dinh, _ = _dien_tich(he, hop[0])
        bien = [t for t in he if t[2] == "m"][0]
        i = 0 if bien[0] else 1
        B = [P for P in dinh if P[i] == hop[0]]
        assert abs(B[0][1 - i] - B[1][1 - i]) == int(dap)


def test_tl_vd_va_tham_so():
    for debai, ds in _chay("L10_C2_B4_VD028_TL_F_01"):
        assert len(ds) == 2
        dinh, S = _dien_tich(_doc_he(debai))
        nums = list(map(int, re.findall(r"-?\d+", ds[0][1])))
        assert sorted(zip(nums[::2], nums[1::2])) == [(int(x), int(y)) for x, y in dinh]
        assert int(ds[1][1]) == S
    for debai, ds in _chay("L10_C2_B4_VD028_TL_G_01"):
        assert len(ds) == 2
        he = _doc_he(debai)
        S = int(re.search(r"bằng \$(\d+)\$", ds[1][0]).group(1))
        m = _so_dau(ds[1][1])
        dinh, dt = _dien_tich(he, m)
        assert len(dinh) == 3 and dt == S
