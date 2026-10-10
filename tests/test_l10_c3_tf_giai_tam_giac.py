"""Dung/Sai 'giai tam giac' (L10_C3_TF_T (15 bien the), co Lan 10/10/2026): kiem lai DOC LAP bang TOA DO.

Moi tam giac duoc dung lai tu toa do (B = (0,0), C = (a,0), A suy ra tu hai canh), roi so voi:
  1. cac dai luong trong engine (_gt_dung, _gt_q, _gt_q2, _gu_dung);
  2. cac phat bieu DUNG sinh ra: doc so lieu trong de bai, dung lai tam giac, kiem cac phat bieu "canh = so nguyen";
  3. moi y co it nhat 3 phat bieu dung va 3 phat bieu sai.
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
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C3_gt_test", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_gt_test"] = M
_spec.loader.exec_module(M)

_cap = {}


@pytest.fixture(autouse=True)
def _chup(monkeypatch):
    _cap.clear()
    monkeypatch.setattr(M, "TF_baitoan_du", lambda d, ys, *a, **k: _cap.update(d=d, ys=ys) or "")


def _toa_do(a, b, c):
    """B = (0,0), C = (a,0); A = (x, y) voi AB = c, AC = b."""
    x = (a * a + c * c - b * b) / (2 * a)
    y = math.sqrt(max(c * c - x * x, 0))
    return (x, y), (0.0, 0.0), (float(a), 0.0)


def _d(P, Q):
    return math.hypot(P[0] - Q[0], P[1] - Q[1])


def _goc(P, O, Q):
    """Cos cua goc POQ."""
    v1 = (P[0] - O[0], P[1] - O[1])
    v2 = (Q[0] - O[0], Q[1] - O[1])
    return (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))


def _co_tam_giac(a, b, c):
    A, B, C = _toa_do(a, b, c)
    S = abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])) / 2
    p = (a + b + c) / 2
    mid = lambda P, Q: ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
    D = (a * c / (b + c), 0.0)  # chan phan giac: BD = ac/(b+c)
    return dict(A=A, B=B, C=C, S=S, p=p, R=a * b * c / (4 * S), r=S / p,
                cos={"A": _goc(B, A, C), "B": _goc(A, B, C), "C": _goc(A, C, B)},
                h={"a": 2 * S / a, "b": 2 * S / b, "c": 2 * S / c}, ma=_d(A, mid(B, C)), mb=_d(B, mid(A, C)), mc=_d(C, mid(A, B)),
                BD=_d(B, D), DC=_d(D, C), AD=_d(A, D), D=D, M=mid(B, C))


def _nhan():
    return [p for tri in M._gt_heron_ds() for p in {(tri[0], tri[1], tri[2]), (tri[1], tri[0], tri[2]), (tri[2], tri[1], tri[0]), (tri[0], tri[2], tri[1])}]


TAM_GIAC = _nhan()


@pytest.mark.parametrize("a,b,c", random.Random(7).sample(TAM_GIAC, 60))
def test_engine_khop_toa_do(a, b, c):
    t = M._gt_dung(a, b, c)
    g = _co_tam_giac(a, b, c)
    assert float(t["S"]) == pytest.approx(g["S"])
    assert float(t["R"]) == pytest.approx(g["R"])
    assert float(t["r"]) == pytest.approx(g["r"])
    for X in "ABC":
        assert float(t["cos"][X]) == pytest.approx(g["cos"][X])
        assert float(t["sin"][X]) == pytest.approx(math.sqrt(1 - g["cos"][X] ** 2))
    for k in "abc":
        assert float(t["h"][k]) == pytest.approx(g["h"][k])
    assert float(M.sqrt(t["m2"]["a"])) == pytest.approx(g["ma"])
    assert float(M.sqrt(t["m2"]["b"])) == pytest.approx(g["mb"])
    assert float(M.sqrt(t["m2"]["c"])) == pytest.approx(g["mc"])
    assert float(t["BD"]) == pytest.approx(g["BD"])
    assert float(t["DC"]) == pytest.approx(g["DC"])
    assert float(M.sqrt(t["l2"])) == pytest.approx(g["AD"])
    # AD that su la phan giac: hai goc BAD, DAC bang nhau
    assert _goc(g["B"], g["A"], g["D"]) == pytest.approx(_goc(g["D"], g["A"], g["C"]))


@pytest.mark.parametrize("a,b,c", random.Random(8).sample(TAM_GIAC, 40))
def test_gt_q_khop_toa_do(a, b, c):
    t = M._gt_dung(a, b, c)
    g = _co_tam_giac(a, b, c)
    kiem = {"cosA": g["cos"]["A"], "cosB": g["cos"]["B"], "cosC": g["cos"]["C"],
            "sinA": math.sqrt(1 - g["cos"]["A"] ** 2), "sinB": math.sqrt(1 - g["cos"]["B"] ** 2), "sinC": math.sqrt(1 - g["cos"]["C"] ** 2),
            "tanA": math.sqrt(1 - g["cos"]["A"] ** 2) / g["cos"]["A"], "a": a, "b": b, "c": c, "S": g["S"], "Sheron": g["S"], "p": g["p"],
            "R": g["R"], "r": g["r"], "ha": g["h"]["a"], "hb": g["h"]["b"], "hc": g["h"]["c"], "ma": g["ma"], "mb": g["mb"], "mc": g["mc"],
            "BD": g["BD"], "DC": g["DC"], "la": g["AD"], "Sha": g["S"], "Shc": g["S"]}
    for ten, mong in kiem.items():
        mau, v, ly, sai = M._gt_q(t, ten)
        assert float(v) == pytest.approx(mong, rel=1e-9), ten
        for w, _ in sai:  # gia tri sai phai khac gia tri dung (tam giac can: BD = a/2 trung gia tri 'sai', engine Y/X loai can)
            if b == c and ten in ("BD", "DC"):
                continue
            assert abs(float(w) - float(v)) > 1e-9, (ten, w)
    # laC (dung tam giac ACD) va c_cao / a_cao (dung duong cao)
    assert float(M._gt_q(t, "laC")[1]) == pytest.approx(g["AD"])
    assert float(M._gt_q(t, "c_cao")[1]) == pytest.approx(c)
    assert float(M._gt_q(t, "a_cao")[1]) == pytest.approx(a)


@pytest.mark.parametrize("dau", ["b", "c"])
def test_trung_tuyen_khop_toa_do(dau):
    M._GT_MED = None
    random.seed(3)
    for _ in range(25):
        t = M._gt_chon_med(dau)
        a, b, c = t["a"], t["b"], t["c"]
        g = _co_tam_giac(a, b, c)
        assert float(t["m"]) == pytest.approx(g["ma"])
        Mi = g["M"]
        cAMB, cAMC = _goc(g["A"], Mi, g["B"]), _goc(g["A"], Mi, g["C"])
        assert cAMB == pytest.approx(-cAMC)
        assert float(M._gt_q(t, "cosAMB")[1]) == pytest.approx(cAMB)
        assert float(M._gt_q(t, "cosAMC")[1]) == pytest.approx(cAMC)
        assert float(M._gt_q(t, "sinAMB")[1]) == pytest.approx(math.sqrt(1 - cAMB ** 2))
        assert float(M._gt_q(t, "b_med" if dau == "c" else "c_med")[1]) == pytest.approx(b if dau == "c" else c)


@pytest.mark.parametrize("hai,cg", [("AB", "a"), ("BC", "a"), ("AC", "c")])
def test_goc_khop_toa_do(hai, cg):
    rng = random.Random(11)
    for _ in range(40):
        g1, g2 = rng.choice(range(35, 85, 5)), rng.choice(range(35, 85, 5))
        ten3 = [x for x in "ABC" if x not in hai][0]
        ang = {hai[0]: g1, hai[1]: g2, ten3: 180 - g1 - g2}
        u = M._gu_dung(ang, cg, rng.randint(10, 40))
        a, b, c = u["canh"]["a"], u["canh"]["b"], u["canh"]["c"]
        gg = _co_tam_giac(a, b, c)  # dung lai tu ba canh roi doi chieu voi cac goc da cho
        for X in "ABC":
            assert gg["cos"][X] == pytest.approx(math.cos(math.radians(ang[X])), abs=1e-9)
        assert u["S"] == pytest.approx(gg["S"])
        assert u["R"] == pytest.approx(gg["R"])
        assert u["h"][cg] == pytest.approx(gg["h"][cg])


TEN = ["L10_C3_TF_T_%02d" % k for k in range(1, 16)]  # MOT ID, 15 bien the


@pytest.mark.parametrize("ten", TEN)
def test_moi_y_du_3_dung_3_sai(ten):
    mn = [[99, 99] for _ in range(4)]
    for s in range(30):
        random.seed(s)
        getattr(M, ten)(1, 1)
        ys = _cap["ys"]
        assert len(ys) == 4
        for i, y in enumerate(ys):
            T = {t for t, _ in y if "\\True" in t}
            F = {t for t, _ in y if "\\True" not in t}
            mn[i][0] = min(mn[i][0], len(T))
            mn[i][1] = min(mn[i][1], len(F))
    assert all(a >= 3 and b >= 3 for a, b in mn), mn


def _so(s):
    return float(s.replace(",", "."))


def _doc_canh(debai):
    kq = {}
    for ten, giatri in re.findall(r"\$(BC|CA|AC|AB) = (\d+)\$", debai):
        kq["CA" if ten in ("CA", "AC") else ten] = int(giatri)
    return kq


def _gia_tri_canh_dung(y, ten):
    """Cac phat bieu DUNG dang $BC = 17$ trong mot y."""
    kq = set()
    for t, _ in y:
        if "\\True" in t:
            m = re.search(r"\$%s = (\d+)\$" % ten, t)
            if m:
                kq.add(int(m.group(1)))
    return kq


@pytest.mark.parametrize("ten,loai", [("L10_C3_TF_T_01", "cos"), ("L10_C3_TF_T_02", "sin"), ("L10_C3_TF_T_03", "tan")])
def test_T_canh_BC_dung(ten, loai):
    for s in range(40):
        random.seed(s)
        getattr(M, ten)(1, 1)
        d = _cap["d"]
        c = int(re.search(r"AB = (\d+)", d).group(1))
        b = int(re.search(r"AC = (\d+)", d).group(1))
        if loai == "cos":
            m = re.search(r"\\cos A = (-?) ?\\dfrac\{(\d+)\}\{(\d+)\}", d)
            cosA = (-1 if m.group(1) else 1) * int(m.group(2)) / int(m.group(3))
        elif loai == "sin":
            m = re.search(r"\\sin A = \\dfrac\{(\d+)\}\{(\d+)\}.*góc \$A\$ là góc (nhọn|tù)", d)
            sinA = int(m.group(1)) / int(m.group(2))
            cosA = math.sqrt(1 - sinA ** 2) * (1 if m.group(3) == "nhọn" else -1)
        else:
            m = re.search(r"\\tan A = (-?) ?\\dfrac\{(\d+)\}\{(\d+)\}", d)
            tanA = (-1 if m.group(1) else 1) * int(m.group(2)) / int(m.group(3))
            cosA = (1 if tanA > 0 else -1) / math.sqrt(1 + tanA ** 2)
        bc = math.sqrt(c * c + b * b - 2 * b * c * cosA)
        dung = _gia_tri_canh_dung(_cap["ys"][2], "BC")
        assert dung, d
        assert all(abs(v - bc) < 1e-9 for v in dung), (d, bc, dung)


def test_X_canh_con_lai_dung():
    for dau, ten, cl in (("c", "L10_C3_TF_T_12", "AC"), ("b", "L10_C3_TF_T_13", "AB")):
        for s in range(40):
            random.seed(s)
            getattr(M, ten)(1, 1)
            d = _cap["d"]
            a = int(re.search(r"BC = (\d+)", d).group(1))
            ben = int(re.search(r"\$(?:AB|AC) = (\d+)\$", d).group(1))
            m = re.search(r"AM = \\dfrac\{(\d+)\}\{(\d+)\}|AM = (\d+)", d)
            mm = int(m.group(1)) / int(m.group(2)) if m.group(1) else int(m.group(3))
            # cong thuc trung tuyen: b^2 + c^2 = 2 m^2 + a^2 / 2
            kia = math.sqrt(2 * mm * mm + a * a / 2 - ben * ben)
            dung = _gia_tri_canh_dung(_cap["ys"][2], cl)
            assert dung and all(abs(v - kia) < 1e-9 for v in dung), (d, kia, dung)


def test_W_canh_con_lai_dung():
    for s in range(40):
        random.seed(s)
        M.L10_C3_TF_T_10(1, 1)
        d = _cap["d"]
        a = int(re.search(r"BC = (\d+)", d).group(1))
        mc = re.search(r"\\cos B = (-?) ?\\dfrac\{(\d+)\}\{(\d+)\}", d)
        cosB = (-1 if mc.group(1) else 1) * int(mc.group(2)) / int(mc.group(3))
        h = _so(re.search(r"AH = (\d+)", d).group(1))
        c = h / math.sqrt(1 - cosB ** 2)
        b = math.sqrt(a * a + c * c - 2 * a * c * cosB)
        assert all(abs(v - c) < 1e-9 for v in _gia_tri_canh_dung(_cap["ys"][2], "AB"))
        assert all(abs(v - b) < 1e-9 for v in _gia_tri_canh_dung(_cap["ys"][3], "CA"))
    for s in range(40):
        random.seed(s)
        M.L10_C3_TF_T_11(1, 1)
        d = _cap["d"]
        c = int(re.search(r"AB = (\d+)", d).group(1))
        mc = re.search(r"\\cos B = (-?) ?\\dfrac\{(\d+)\}\{(\d+)\}", d)
        cosB = (-1 if mc.group(1) else 1) * int(mc.group(2)) / int(mc.group(3))
        h = _so(re.search(r"CK = (\d+)", d).group(1))
        a = h / math.sqrt(1 - cosB ** 2)
        b = math.sqrt(a * a + c * c - 2 * a * c * cosB)
        assert all(abs(v - a) < 1e-9 for v in _gia_tri_canh_dung(_cap["ys"][2], "BC"))
        assert all(abs(v - b) < 1e-9 for v in _gia_tri_canh_dung(_cap["ys"][3], "CA"))
