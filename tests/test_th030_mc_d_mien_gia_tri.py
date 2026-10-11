"""TH030_MC_D_01/_02 (sin±cos <-> sin.cos): moi phuong an (ke ca nhieu) phai nam trong MIEN GIA TRI co the
cua dai luong duoc hoi. Co Lan 11/10/2026: hoi (sin a - cos a)^2 ma co phuong an am thi hoc sinh loai ngay."""
import importlib.util
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C3_mcd_test", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_mcd_test"] = M
_spec.loader.exec_module(M)


def _gia_tri(t):
    t = t.strip()
    am = t.startswith("-")
    t = t.lstrip("- ").strip()
    m = re.fullmatch(r"\\dfrac\{(\d+)\}\{(\d+)\}", t)
    v = Fraction(int(m.group(1)), int(m.group(2))) if m else Fraction(int(t))
    return -v if am else v


def _phuong_an(ex):
    phan = ex.split("\\choice", 1)[1].split("\\loigiai", 1)[0]
    return re.findall(r"\{(?:\\True)?\s*\$(.*?)\$\}", phan)


def _mien(de):
    hoi = de.split("\\choice")[0]
    if "Tính giá trị của $\\sin\\alpha\\cos\\alpha$" in hoi:
        return Fraction(-1, 2), Fraction(1, 2)          # sin.cos = sin(2a)/2
    if "sin^{4}" in hoi:
        return Fraction(1, 2), Fraction(1)               # sin^4 + cos^4 = 1 - 2(sin.cos)^2
    return Fraction(0), Fraction(2)                      # (sin ± cos)^2


@pytest.mark.parametrize("ten", ["L10_C3_B5_TH030_MC_D_01", "L10_C3_B5_TH030_MC_D_02"])
def test_phuong_an_trong_mien_gia_tri(ten):
    ham = getattr(M, ten)
    dem = 0
    for seed in range(300):
        random.seed(seed)
        for dang in (1, 2, 3):
            try:
                out = ham(1, dang)
            except TypeError:
                out = ham(1)
            for ex in out.split("\\end{ex}"):
                if "\\choice" not in ex:
                    continue
                pa = _phuong_an(ex)
                assert len(pa) == 4 and len(set(pa)) == 4, (ten, pa)
                assert sum("\\True" in x for x in re.findall(r"\{[^{}]*\$", ex.split("\\choice", 1)[1].split("\\loigiai")[0])) == 1
                thap, cao = _mien(ex)
                for o in pa:
                    dem += 1
                    assert thap <= _gia_tri(o) <= cao, (ten, ex.split("\\choice")[0][-120:], o)
    assert dem > 0


# ---------------------------------------------------------------- SA / TL cung dang (11/10/2026)
import math


def _so(t):
    """'0,8' / '-0,4' / '\\dfrac{7}{13}' / '- \\dfrac{60}{169}' -> float."""
    t = t.strip().replace(",", ".").replace("\\left", "").replace("\\right", "")
    am = t.startswith("-")
    t = t.lstrip("- ").strip()
    m = re.fullmatch(r"\\dfrac\{(\d+)\}\{(\d+)\}", t)
    v = int(m.group(1)) / int(m.group(2)) if m else float(t)
    return -v if am else v


def _cac_goc(f, dich):
    """Moi alpha trong [0; pi] de f(alpha) = dich (do bang do doi dau tren luoi min)."""
    n, kq = 7200, []
    xs = [math.pi * i / n for i in range(n + 1)]
    for a, b in zip(xs, xs[1:]):
        fa, fb = f(a) - dich, f(b) - dich
        if fa == 0:
            kq.append(a)
        elif fa * fb < 0:
            for _ in range(60):
                m = (a + b) / 2
                if (f(a) - dich) * (f(m) - dich) <= 0:
                    b = m
                else:
                    a = m
            kq.append((a + b) / 2)
    return kq


def _bt(s):
    """Bieu thuc ve sin/cos cua alpha trong de -> ham so."""
    s = s.replace("\\left", "").replace("\\right", "").replace(" ", "")
    return {
        "\\sin\\alpha+\\cos\\alpha": lambda x: math.sin(x) + math.cos(x),
        "\\sin\\alpha-\\cos\\alpha": lambda x: math.sin(x) - math.cos(x),
        "\\sin\\alpha\\cos\\alpha": lambda x: math.sin(x) * math.cos(x),
        "(\\sin\\alpha+\\cos\\alpha)^{2}": lambda x: (math.sin(x) + math.cos(x)) ** 2,
        "(\\sin\\alpha-\\cos\\alpha)^{2}": lambda x: (math.sin(x) - math.cos(x)) ** 2,
        "|\\sin\\alpha+\\cos\\alpha|": lambda x: abs(math.sin(x) + math.cos(x)),
        "|\\sin\\alpha-\\cos\\alpha|": lambda x: abs(math.sin(x) - math.cos(x)),
        "\\sin^{4}\\alpha+\\cos^{4}\\alpha": lambda x: math.sin(x) ** 4 + math.cos(x) ** 4,
    }[s]


def _kiem_cau(de, hoi_dap):
    """de co 'thoa man $<bt> = <so>$'; hoi_dap: [(bieu thuc hoi, dap so)]. Moi goc thoa gia thiet phai cho dap so do."""
    m = re.search(r"thoả mãn \$(.+?) = (.+?)\$", de)
    f, v = _bt(m.group(1)), _so(m.group(2))
    cac = _cac_goc(f, v)
    assert cac, de
    for hoi, dap in hoi_dap:
        g = _bt(hoi)
        for al in cac:
            assert abs(g(al) - _so(dap)) < 1e-6, (de, hoi, dap, math.degrees(al), g(al))


@pytest.mark.parametrize("ten", ["SA_L_01", "SA_M_01", "SA_M_02", "SA_M_03"])
def test_sa_dung_so_va_gon(ten):
    ham = getattr(M, "L10_C3_B5_TH030_" + ten)
    hoi_cua = {"SA_L_01": None, "SA_M_01": "(\\sin\\alpha+\\cos\\alpha)^{2}", "SA_M_02": "(\\sin\\alpha-\\cos\\alpha)^{2}",
               "SA_M_03": "\\sin^{4}\\alpha+\\cos^{4}\\alpha"}[ten]
    dem = 0
    for seed in range(120):
        random.seed(seed)
        out = ham(3)
        for ex in out.split("\\end{ex}")[:-1]:
            de = next(l for l in ex.split("\n") if "thoả mãn" in l)
            dap = re.search(r"\\shortans\{\s*(.*?)\}", ex).group(1)
            assert len(dap) <= 4, (ten, dap)                   # o dap an toi da 4 ky tu
            assert "\\choice" not in ex
            hoi = hoi_cua or "\\sin\\alpha\\cos\\alpha"
            _kiem_cau(de, [(hoi, dap)])
            dem += 1
    assert dem > 0


@pytest.mark.parametrize("ten", ["TL_F_01", "TL_G_01"])
def test_tl_dung_so_hai_y(ten):
    ham = getattr(M, "L10_C3_B5_TH030_" + ten)
    dem = 0
    for seed in range(120):
        random.seed(seed)
        out = ham(2)
        for ex in out.split("\\end{ex}")[:-1]:
            hoi = re.findall(r"\\item Tính \$(.+?)\$\. \\SA\[4\]\{\$(.+?)\$\}", ex.split("\\loigiai")[0])
            assert len(hoi) == 2, ex
            de = next(l for l in ex.split("\n") if "thoả mãn" in l)
            if ten == "TL_G_01":                              # a) bat dau tu sin.cos = P  (de la 'sinacosa = P')
                m = re.search(r"thoả mãn \$\\sin\\alpha\\cos\\alpha = (.+?)\$", de)
                cac = _cac_goc(lambda x: math.sin(x) * math.cos(x), _so(m.group(1)))
                assert cac, de
                for al in cac:
                    for bt, dap in hoi:
                        # y b) 'sin a - cos a' khong co dau tuyet doi: phai dung o MOI goc thoa gia thiet
                        assert abs(_bt(bt)(al) - _so(dap)) < 1e-6, (de, bt, dap)
            else:
                _kiem_cau(de, [(bt, dap) for bt, dap in hoi])
            assert "Ở câu a)" in ex or ten == "TL_G_01"
            dem += 1
    assert dem > 0
