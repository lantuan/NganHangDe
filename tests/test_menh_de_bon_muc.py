# -*- coding: utf-8 -*-
r"""Mệnh đề chứa biến bốn mức NB / TH / VD / VDC (cô Lan 04/10/2026).

Kiểm: (1) các hàm chạy hàng trăm hạt giống, (2) đáp số TÍNH LẠI độc lập bằng vét cạn
hoặc sympy, (3) khoảng của k đi theo NĂM THỰC (giả lập năm khác), (4) mapping khớp.
"""
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[1]
BANK = GOC / "data" / "python_bank"
sys.path.insert(0, str(BANK))

_spec = importlib.util.spec_from_file_location("L10_C1_menh_de_bon_muc", BANK / "toan10" / "L10_C1.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C1_menh_de_bon_muc"] = M
_spec.loader.exec_module(M)

HAM_MOI = [n for n in dir(M) if n.startswith("L10_C1_B1_") and any(
    t in n for t in ("NB001_MC_C", "TH003_MC_D", "VD014_MC_E", "VD014_SA_C", "VD014_MC_F", "VD014_SA_D",
                     "VD014_MC_G", "VD014_SA_E", "VD014_MC_H", "VD014_SA_F", "VD014_MC_I", "VD014_SA_G",
                     "VD014_MC_J", "VD014_SA_H"))]


def test_du_21_ham():
    assert len(HAM_MOI) == 21, HAM_MOI


@pytest.mark.parametrize("ten", HAM_MOI)
def test_ham_chay_nhieu_hat_giong(ten):
    f = getattr(M, ten)
    for s in range(120):
        random.seed(s)
        out = f(3)
        assert r"\begin{ex}" in out and r"\loigiai" in out
        if "_MC_" in ten:
            assert out.count(r"\True") == 3


# ---------------------------------------------------------------- đáp số đếm k
def _khoang(nam, tr, ph):
    lo = -nam if tr == "[" else -nam + 1
    hi = nam + 1 if ph == "]" else nam
    return range(lo, hi + 1)


CA_TRI = {}


def _dem(pred, nam, tr, ph):
    return sum(1 for k in _khoang(nam, tr, ph) if pred(k))


def _kiem_abs(kieu, nam, tr, ph, ts):
    if kieu == "duong":
        a, c = ts
        pred = lambda k: 0 < k - c < a
    else:
        p, q, m, c = ts
        t = lambda k: m * k + c
        pred = {"co": lambda k: t(k) >= 0, "hai": lambda k: t(k) > 0, "vo": lambda k: t(k) < 0}[kieu]
    return _dem(pred, nam, tr, ph)


def _kiem_bac2(kieu, nam, tr, ph, ts):
    if kieu == "co":
        b, = ts
        pred = lambda k: b * b - 4 * k >= 0
    elif kieu == "vo":
        b, = ts
        pred = lambda k: b * b - 4 * k < 0
    elif kieu == "hesoa":
        a, c = ts
        pred = lambda k: k != 0 and a * a - k * c > 0
    else:
        c, dau = ts
        pred = (lambda k: k * k >= c) if dau == r"\geq" else (lambda k: k * k > c)
    return _dem(pred, nam, tr, ph)


@pytest.mark.parametrize("kieu", ["co", "hai", "vo", "duong"])
@pytest.mark.parametrize("nam", [2026, 2031, 2040])
def test_dem_k_abs_dung(kieu, nam):
    sinh, de_giai = M._sinh_abs(kieu), M._de_giai_abs(kieu)
    random.seed(7)
    for _ in range(300):
        ts = sinh()
        for tr in "([":
            for ph in ")]":
                _, dem, _ = de_giai(nam, tr, ph, *ts)
                assert dem == _kiem_abs(kieu, nam, tr, ph, ts), (kieu, nam, tr, ph, ts)


@pytest.mark.parametrize("kieu", ["co", "vo", "hesoa", "kep"])
@pytest.mark.parametrize("nam", [2026, 2031, 2040])
def test_dem_k_bac2_dung(kieu, nam):
    sinh, de_giai = M._sinh_bac2(kieu), M._de_giai_bac2(kieu)
    random.seed(11)
    for _ in range(300):
        ts = sinh()
        for tr in "([":
            for ph in ")]":
                _, dem, _ = de_giai(nam, tr, ph, *ts)
                assert dem == _kiem_bac2(kieu, nam, tr, ph, ts), (kieu, nam, tr, ph, ts)


class _GiaLapDatetime:
    """Thay module datetime trong ngân hàng: .datetime.now().year trả năm giả lập."""
    def __init__(self, nam):
        outer = self

        class _DT:
            @staticmethod
            def now():
                class _N:
                    year = nam
                return _N
        self.datetime = _DT


HAM_K = [n for n in HAM_MOI if "VD014" in n and not re.search(r"_(MC_E|SA_C)_", n)]


@pytest.mark.parametrize("nam", [2026, 2029, 2035])
@pytest.mark.parametrize("ten", HAM_K)
def test_khoang_cua_k_di_theo_nam_thuc(monkeypatch, ten, nam):
    monkeypatch.setattr(M, "datetime", _GiaLapDatetime(nam))
    random.seed(3)
    out = getattr(M, ten)(4)
    cac = re.findall(r"thuộc \$\\left[\[(](-?\d+);\\ (\d+)\\right[\])]\$", out)
    assert cac, out[:300]
    for lo, hi in cac:
        assert int(lo) == -nam and int(hi) == nam + 1


def test_ham_cu_VD014_A_cung_theo_nam_thuc(monkeypatch):
    monkeypatch.setattr(M, "datetime", _GiaLapDatetime(2033))
    random.seed(1)
    out = M.L10_C1_B1_VD014_MC_A_02(2)
    assert "-2033" in out and "2034" in out


# ------------------------------------------------- NB / TH: đúng một đáp án
def _doc_cau(out):
    """Tách các câu: (đề, danh sách phương án, chỉ số đáp án đúng)."""
    cac = []
    for blk in out.split(r"\begin{ex}")[1:]:
        de = blk.split("\n", 1)[1].split(r"\choice")[0]
        pa = re.findall(r"\{(\\True )?(\$[^$]*\$)\}", blk.split(r"\choice", 1)[1].split(r"\loigiai")[0])
        cac.append((de, [(bool(t), x) for t, x in pa]))
    return cac


def _gia_tri(x):
    return int(re.search(r"x = (-?\d+)", x).group(1))


@pytest.mark.parametrize("seed", range(150))
def test_NB_dung_mot_dap_an(seed):
    random.seed(seed)
    for de, pa in _doc_cau(M.L10_C1_B1_NB001_MC_C_01(3)):
        m = re.search(r"x (>|<|\\geq|\\leq|=|\\neq) (-?\d+)\$ là mệnh đề (đúng|\\textbf\{sai\})", de)
        dau, c, hoi = m.group(1), int(m.group(2)), m.group(3) == "đúng"
        ss = M._SO_SANH[dau]
        assert len(pa) == 4 and sum(t for t, _ in pa) == 1
        assert len({x for _, x in pa}) == 4
        for t, x in pa:
            assert t == (ss(_gia_tri(x), c) == hoi), (de, pa)


@pytest.mark.parametrize("seed", range(150))
def test_TH_dai_so_dung_mot_dap_an(seed):
    random.seed(seed)
    for de, pa in _doc_cau(M.L10_C1_B1_TH003_MC_D_01(3)):
        m = re.search(r"P\(x\)\\colon (.*?) (>|<|\\geq|\\leq|=) (-?\d+)\$ là mệnh đề (đúng|\\textbf\{sai\})", de)
        bt, dau, c, hoi = m.group(1), m.group(2), int(m.group(3)), m.group(4) == "đúng"
        py = bt.replace(r"\left|x\right|", "abs(x)").replace(r"\left(", "(").replace(r"\right)", ")")
        py = py.replace("^{2}", "**2").replace("^{3}", "**3")
        py = re.sub(r"\(x ([+-]) (\d+)\)", r"(x \1 \2)", py)
        ss = M._SO_SANH[dau]
        assert sum(t for t, _ in pa) == 1 and len({x for _, x in pa}) == 4
        for t, x in pa:
            v = _gia_tri(x)
            assert t == (ss(eval(py, {"x": v, "abs": abs}), c) == hoi), (de, x)


@pytest.mark.parametrize("seed", range(150))
def test_TH_luong_giac_dung_mot_dap_an(seed):
    import math
    random.seed(seed)
    gt = {r"\dfrac{1}{2}": 0.5, r"\dfrac{\sqrt{2}}{2}": math.sqrt(2) / 2, r"\dfrac{\sqrt{3}}{2}": math.sqrt(3) / 2,
          r"\dfrac{\sqrt{3}}{3}": math.sqrt(3) / 3, r"\sqrt{3}": math.sqrt(3), "1": 1.0, "0": 0.0}
    for de, pa in _doc_cau(M.L10_C1_B1_TH003_MC_D_02(3)):
        m = re.search(r"\\(sin|cos|tan) x (>|<|\\geq|\\leq|=) (.*?)\$ là mệnh đề (đúng|\\textbf\{sai\})", de)
        ham, dau, ct, hoi = m.group(1), m.group(2), m.group(3), m.group(4) == "đúng"
        c = gt[ct]
        f = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[ham]
        ss = M._LG_SS[dau]
        assert sum(t for t, _ in pa) == 1 and len({x for _, x in pa}) == 4
        for t, x in pa:
            g = int(re.search(r"x = (\d+)", x).group(1))
            assert t == (ss(f(math.radians(g)), c) == hoi), (de, x)


# ------------------------------------------------- VD: nghiệm tính độc lập bằng sympy
@pytest.mark.parametrize("seed", range(60))
def test_VD_nghiem_dung_voi_sympy(seed):
    import sympy as sp
    random.seed(seed)
    X = sp.Symbol("x", real=True)
    for _ in range(10):
        kieu, pt, nghiem, _ = M._vd_tao_pt()
        lhs, rhs = pt.split(" = ", 1)
        bien = lambda t: sp.sympify(
            re.sub(r"(\d)x", r"\1*x", t.replace(r"\left|", "Abs(").replace(r"\right|", ")")
                   .replace("^{2}", "**2").replace(r"\left(", "(").replace(r"\right)", ")")),
            locals={"x": X, "Abs": sp.Abs})
        sol = sp.solveset(sp.Eq(bien(lhs), bien(rhs)), X, sp.S.Reals)
        dung = sorted(sp.Rational(v.numerator, v.denominator) for v in nghiem)
        assert sorted(sol) == dung, (pt, sol, nghiem)


# ------------------------------------------------- mapping
def _mapping():
    return {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C1.json", encoding="utf-8"))}


def test_mapping_co_du_dong_moi_va_danh_dau_vdc():
    mp = _mapping()
    for i in ("NB001_MC_C", "TH003_MC_D", "VD014_MC_E", "VD014_SA_C"):
        assert "L10_C1_B1_" + i in mp
        assert "muc_do_dang" not in mp["L10_C1_B1_" + i]
    for i in ("VD014_MC_A", "VD014_SA_A", "VD014_MC_F", "VD014_SA_D", "VD014_MC_G", "VD014_SA_E",
              "VD014_MC_H", "VD014_SA_F", "VD014_MC_I", "VD014_SA_G", "VD014_MC_J", "VD014_SA_H"):
        assert mp["L10_C1_B1_" + i]["muc_do_dang"] == "VDC", i


def test_cap_mc_sa_cung_mo_ta_dang():
    """Cặp MC/SA cùng dạng có cùng chuỗi Dang (để một đề không ra cả hai)."""
    mp = _mapping()
    for mc, sa in [("E", "C"), ("F", "D"), ("G", "E"), ("H", "F"), ("I", "G"), ("J", "H")]:
        assert mp["L10_C1_B1_VD014_MC_" + mc]["Dang"] == mp["L10_C1_B1_VD014_SA_" + sa]["Dang"]
