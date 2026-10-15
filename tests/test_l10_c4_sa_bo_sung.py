# -*- coding: utf-8 -*-
"""Chuong 4 lop 10 - cac cau SA/MC bo sung 15/10/2026 (co Lan: "ghep cac dang da thay giong, cung dang; cac dang
thieu lam bo sung luon").

Moi dap so duoc TINH LAI DOC LAP tu chinh van ban de bai: doc dang thuc vecto bang tests/_tinh_tex.py roi thu tren toa
do NGAU NHIEN cua test (diem bat ki, trung diem dung tu de) hoac toa do doc tu hinh TikZ trong de. Khong dung lai ham
sinh de.
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
sys.path.insert(0, str(GOC / "tests"))
from _tinh_tex import V, bang, so, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C4_sa_bo_sung", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_sa_bo_sung"] = M
_spec.loader.exec_module(M)

SO_LAN = 200
P = "L10_C4_"
DAP_SO = re.compile(r"^-?\d+(,\d+)?$")


def _bat(ten, seed, dang=2):
    """(debai, dapso, dsnhieu, giai, hinh) truyen vao MC_SA_answer_const."""
    cap = []
    goc = M.MC_SA_answer_const
    M.MC_SA_answer_const = lambda debai, dap, nhieu, giai, hinh=0, *a, **k: cap.append((debai, str(dap), nhieu, giai, hinh)) or ""
    try:
        random.seed(seed)
        getattr(M, P + ten)(1, dang=dang)
    finally:
        M.MC_SA_answer_const = goc
    assert len(cap) == 1
    return cap[0]


def _muc(debai):
    return [m.group(1).strip() for m in re.finditer(r"\\\\ \d\. (.+?)(?=\\\\ \d\. |$)", debai)]


def _toa_do_hinh(tikz):
    """Toa do cac diem co ten trong hinh TikZ (\\coordinate hoac \\fill ... node {$X$})."""
    td = {t: V(float(x), float(y)) for t, x, y in re.findall(r"\\coordinate \((\w)\) at \(([-\d.]+),([-\d.]+)\)", tikz)}
    for x, y, t in re.findall(r"\\fill\[black\] \(([-\d.]+),([-\d.]+)\) circle[^\n]*?\$(\w)\$", tikz):
        td[t] = V(float(x), float(y))
    return td


def _ngau_nhien(ten):
    return {t: V(random.uniform(-9, 9), random.uniform(-9, 9)) for t in ten}


def _dang_thuc_dung(muc, cac_moi_truong):
    l, r = muc.strip("$").split(" = ")
    return all(bang(tinh(l, P=E.get("P", {}), W=E.get("W", {})), tinh(r, P=E.get("P", {}), W=E.get("W", {})))
               for E in cac_moi_truong)


def _dem_kiem(debai, dap, chan_tri):
    ds = _muc(debai)
    assert len(ds) == 4 and len(set(ds)) == 4, debai
    tri = [chan_tri(x) for x in ds]
    so_dung = sum(tri)
    assert 1 <= so_dung <= 3
    hoi_dung = r"\textbf{sai}" not in debai
    assert dap == str(so_dung if hoi_dung else 4 - so_dung), (debai, tri)


TAT_CA_SA = ["B7_NB038_SA_A_01", "B8_TH040_SA_A_01", "B8_TH040_SA_B_01", "B8_TH041_SA_A_01", "B8_TH041_SA_B_01",
             "B8_TH042_SA_A_01", "B9_TH043_SA_A_01", "B9_TH044_SA_A_01", "B9_TH046_SA_A_01", "B9_TH047_SA_A_01",
             "B10_NB049_SA_A_01", "B10_TH050_SA_A_01", "B11_NB057_SA_A_01", "B11_NB057_SA_A_02", "B11_TH057_SA_A_01",
             "B11_TH057_SA_A_02", "B11_TH057_SA_B_01", "B11_TH057_SA_B_02", "B11_TH059_SA_A_01"]


@pytest.mark.parametrize("ten", TAT_CA_SA)
def test_sa_moi_dung_loai(ten):
    for s in range(SO_LAN):
        random.seed(s)
        out = getattr(M, P + ten)(1)
        assert r"\shortans" in out and r"\choice" not in out
        debai, dap, _, _, _ = _bat(ten, s)
        assert DAP_SO.match(dap), (ten, dap)


@pytest.mark.parametrize("mc,sa", [("B10_TH050_MC_B_01", "B10_TH050_SA_B_01"), ("B10_VD054_MC_B_01", "B10_VD054_SA_B_01")])
def test_mc_cung_dang_voi_sa(mc, sa):
    for s in range(60):
        random.seed(s)
        o_mc = getattr(M, P + mc)(1)
        random.seed(s)
        o_sa = getattr(M, P + sa)(1)
        assert r"\choice" in o_mc and r"\shortans" not in o_mc
        dung = re.search(r"\{\\True \$?\s*([^${}]*?)\s*\$?\}", o_mc).group(1)
        assert dung == re.search(r"\\shortans\{\s*\$?\s*([^${}]*?)\s*\$?\}", o_sa).group(1)
        assert o_mc.split(r"\choice")[0].strip() == o_sa.split(r"\shortans")[0].strip()


# ---------------------------------------------------------------- cau dem dang thuc vecto
def _diem_bat_ki(debai):
    m = re.match(r"Cho (?:bốn|ba) điểm ((?:\$[A-Z]\$(?:, )?)+) bất kì\.", debai)
    return re.findall(r"\$([A-Z])\$", m.group(1))


@pytest.mark.parametrize("ten", ["B8_TH040_SA_A_01", "B8_TH041_SA_A_01"])
def test_dem_diem_bat_ki(ten):
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat(ten, s)
        ten_diem = _diem_bat_ki(debai)
        mt = [{"P": _ngau_nhien(ten_diem)} for _ in range(4)]
        _dem_kiem(debai, dap, lambda m: _dang_thuc_dung(m, mt))


@pytest.mark.parametrize("ten", ["B7_NB038_SA_A_01", "B8_TH040_SA_B_01", "B8_TH041_SA_B_01"])
def test_dem_theo_hinh(ten):
    for s in range(SO_LAN):
        debai, dap, _, _, hinh = _bat(ten, s)
        mt = [{"P": _toa_do_hinh(hinh)}]
        _dem_kiem(debai, dap, lambda m: _dang_thuc_dung(m, mt))


@pytest.mark.parametrize("ten,so_vt", [("B8_TH042_SA_A_01", 3), ("B9_TH044_SA_A_01", 2), ("B11_TH059_SA_A_01", 3)])
def test_dem_vecto_tuy_y(ten, so_vt):
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat(ten, s)
        tu = re.findall(r"\\overrightarrow\{([a-z])\}", debai.split(r"\\")[0])[:so_vt]
        assert len(tu) == so_vt
        mt = [{"W": {t: V(random.uniform(-9, 9), random.uniform(-9, 9)) for t in tu}} for _ in range(4)]
        _dem_kiem(debai, dap, lambda m: _dang_thuc_dung(m, mt))


def test_th047_trung_diem():
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat("B9_TH047_SA_A_01", s)
        J, X, Y, N = re.match(r"Cho \$([A-Z])\$ là trung điểm của đoạn thẳng \$([A-Z])([A-Z])\$ và \$([A-Z])\$", debai).groups()
        mt = []
        for _ in range(4):
            E = _ngau_nhien([X, Y, N])
            E[J] = (E[X] + E[Y]) * 0.5
            mt.append({"P": E})
        _dem_kiem(debai, dap, lambda m: _dang_thuc_dung(m, mt))


# ---------------------------------------------------------------- cau tinh so
def test_th043_do_dai():
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat("B9_TH043_SA_A_01", s)
        m = re.search(r"\\left\|\\overrightarrow\{a\}\\right\| = (\d+)\$\. Độ dài của vectơ \$(.+?)\\overrightarrow\{a\}\$", debai)
        if m:
            k = tinh(m.group(2) + " 1")
            assert abs(so(dap) - abs(k) * int(m.group(1))) < 1e-9
        else:
            k, n = re.search(r"\\overrightarrow\{b\} = (.+?)\\overrightarrow\{a\}\$ và \$\\left\|\\overrightarrow\{b\}\\right\| = "
                             r"([\d,]+)\$", debai).groups()
            assert abs(so(dap) - so(n) / abs(tinh(k + " 1"))) < 1e-9


def _diem(debai, t):
    x, y = re.search(r"\$%s\\left\((-?\d+);\\ (-?\d+)\\right\)\$" % t, debai).groups()
    return int(x), int(y)


def test_th046_thang_hang():
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat("B9_TH046_SA_A_01", s)
        A, B, C = (_diem(debai, t) for t in "ABC")
        ab, ac = (B[0] - A[0], B[1] - A[1]), (C[0] - A[0], C[1] - A[1])
        k = so(dap)
        assert ab[0] * ac[1] - ab[1] * ac[0] == 0
        assert abs(ab[0] - k * ac[0]) < 1e-9 and abs(ab[1] - k * ac[1]) < 1e-9


def test_nb049_toa_do():
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat("B10_NB049_SA_A_01", s)
        m = re.search(r"vectơ \$\\overrightarrow\{u\} = \\left\((-?\d+);\\ (-?\d+)\\right\)\$", debai)
        if m:
            x, y = map(int, m.groups())
            assert int(dap) == (x if "Tìm $m$" in debai else y)
        else:
            bt = re.search(r"vectơ \$\\overrightarrow\{u\} = (.+?)\$", debai).group(1)
            u = tinh(bt.replace(r"\overrightarrow{i}", r"\overrightarrow{x}").replace(r"\overrightarrow{j}", r"\overrightarrow{y}"),
                     W={"x": V(1, 0), "y": V(0, 1)})
            assert int(dap) == round(u.x if "hoành độ" in debai else u.y)


def test_th050_sa_a_toa_do_vecto():
    for s in range(SO_LAN):
        debai, dap, _, _, _ = _bat("B10_TH050_SA_A_01", s)
        A, B = _diem(debai, "A"), _diem(debai, "B")
        assert int(dap) == (B[0] - A[0] if "hoành độ" in debai else B[1] - A[1])


@pytest.mark.parametrize("ten", ["B11_NB057_SA_A_01", "B11_NB057_SA_A_02", "B11_TH057_SA_A_01", "B11_TH057_SA_A_02",
                                 "B11_TH057_SA_B_01", "B11_TH057_SA_B_02"])
def test_goc_giua_hai_vecto(ten):
    for s in range(SO_LAN):
        debai, dap, _, _, hinh = _bat(ten, s)
        u, v = re.search(r"hai vectơ \$\\overrightarrow\{(\w\w)\}\$ và \$\\overrightarrow\{(\w\w)\}\$", debai).groups()
        T = _toa_do_hinh(hinh)
        a, b = T[u[1]] - T[u[0]], T[v[1]] - T[v[0]]
        g = math.degrees(math.acos(max(-1.0, min(1.0, (a * b) / abs(a) / abs(b)))))
        assert abs(g - int(dap)) < 0.05, (debai, g)
