# -*- coding: utf-8 -*-
"""Bai 5 lop 10 muc VD (16/10/2026, co Lan duyet ke hoach ID): L10_C3_B5_VD030 D, E, F, G, H (luyen tap them).

Dap so TINH LAI DOC LAP bang so thuc: doc dieu kien trong de, TIM GOC alpha bang quet so tren (0; 180) do (khong dung
cong thuc cua ham sinh), roi tinh bieu thuc hoi bang math. Cau F (biet sin +- cos, tan + cot) kiem them: MOI goc thoa dieu
kien deu cho cung mot gia tri (de khong mo ho ve dau). Cau G: thu tren nhieu goc ngau nhien, bieu thuc phai la hang so.
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
from _tinh_tex import MOI_TRUONG, sang_python, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C3_b5_vd030", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_b5_vd030"] = M
_spec.loader.exec_module(M)

SO_LAN = 250
P = "L10_C3_B5_VD030_"


def _bat(ten, seed):
    cap = []
    goc = M.MC_SA_answer_const
    M.MC_SA_answer_const = lambda de, dap, nhieu, giai, *a, **k: cap.append((de, str(dap), list(nhieu), giai)) or ""
    try:
        random.seed(seed)
        getattr(M, P + ten)(1)
    finally:
        M.MC_SA_answer_const = goc
    assert len(cap) == 1
    return cap[0]


def _py(tex):
    """LaTeX luong giac -> bieu thuc cho tinh(): sin -> S, cos -> C, tan -> T, cot -> K."""
    for h, v in (("sin", "S"), ("cos", "C"), ("tan", "T"), ("cot", "K")):
        tex = re.sub(r"\\%s\^\{(\d)\}\\alpha" % h, r"%s^{\1}" % v, tex)
        tex = tex.replace("\\%s\\alpha" % h, v)
    return tex.replace(r"\left|", "(").replace(r"\right|", ")")


_BIEN_DICH = {}


def _gia_tri(tex, a_do):
    """Gia tri bieu thuc LaTeX tai goc a_do (do). Bien dich LaTeX -> Python mot lan (nhanh khi quet nhieu goc)."""
    if tex not in _BIEN_DICH:
        _BIEN_DICH[tex] = compile(sang_python(_py(tex)), "<bt>", "eval")
    a = math.radians(a_do)
    s, c = math.sin(a), math.cos(a)
    bien = dict(MOI_TRUONG, S=s, C=c, T=s / c if abs(c) > 1e-12 else float("nan"),
                K=c / s if abs(s) > 1e-12 else float("nan"))
    try:
        return eval(_BIEN_DICH[tex], {"__builtins__": {}}, bien)
    except ZeroDivisionError:
        return float("nan")


def _cac_goc(dieu_kien):
    """Moi goc alpha trong (0; 180) do thoa f(alpha) = 0: quet luoi rat min + chia doi."""
    ra = []
    n = 36000
    truoc = None
    for i in range(1, n):
        x = 180 * i / n
        if abs(x - 90) < 1e-6:
            truoc = None
            continue
        v = dieu_kien(x)
        if v == 0:
            ra.append(x)
        elif truoc is not None and truoc[1] * v < 0:
            lo, hi = truoc[0], x
            for _ in range(60):
                mid = (lo + hi) / 2
                if dieu_kien(lo) * dieu_kien(mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            ra.append((lo + hi) / 2)
        truoc = (x, v) if v == v else None
    # bo nghiem gia o tiem can (tan, cot doi dau qua 90 do)
    return [x for x in ra if abs(dieu_kien(x)) < 1e-6]


def _so(chuoi):
    return float(chuoi.replace(",", "."))


def _kiem_mc(dap, nhieu, dung):
    gia = [tinh(dap)] + [tinh(x) for x in nhieu]
    assert abs(gia[0] - dung) < 1e-9, (dap, dung)
    assert all(abs(g - dung) > 1e-9 for g in gia[1:]), (dap, nhieu)
    assert len({round(g, 9) for g in gia}) == 4


def _kiem_sa(de, dap, dung):
    if "làm tròn kết quả đến hàng phần trăm" in de:
        # lam tron den hang phan tram: sai so <= 0,005 (bang 0,005 khi lam tron len o chu so 5)
        assert abs(_so(dap) - dung) <= 0.005 + 1e-9 and abs(_so(dap) * 100 - round(_so(dap) * 100)) < 1e-9, (dap, dung)
    else:
        assert abs(_so(dap) - dung) < 1e-9, (dap, dung)
    assert len(dap) <= 4


# ---------------------------------------------------------------- D, E: cho mot gia tri, bieu thuc doi xung / thuan nhat
def _goc_tu_dieu_kien(de):
    m = re.search(r"(?:thoả mãn|180\^\\circ\$ và) \$([^$<]+?) = ([^$]+?)\$", de)
    trai, phai = m.group(1), tinh(m.group(2))
    return _cac_goc(lambda x: _gia_tri(trai, x) - phai)


def _bt_hoi(de):
    m = re.search(r"biểu thức \$(?:P = )?(.+?)\$", de)
    return m.group(1)


@pytest.mark.parametrize("ten", ["MC_D_01", "MC_D_02", "SA_D_01", "MC_E_01", "SA_E_01"])
def test_d_e_dap_so_doc_lap(ten):
    for s in range(SO_LAN // 5):
        de, dap, nhieu, giai = _bat(ten, s)
        goc = _goc_tu_dieu_kien(de)
        assert goc, de
        bt = _bt_hoi(de)
        gt = {round(_gia_tri(bt, a), 9) for a in goc}
        assert len(gt) == 1, (de, gt)                      # moi goc thoa dieu kien cho cung gia tri
        dung = gt.pop()
        if ten.startswith("MC"):
            _kiem_mc(dap, nhieu, dung)
        else:
            _kiem_sa(de, dap, dung)


# ---------------------------------------------------------------- F: biet sin +- cos / tan + cot, co xet dau
@pytest.mark.parametrize("ten", ["MC_F_01", "SA_F_01"])
def test_f_xet_dau_doc_lap(ten):
    for s in range(SO_LAN // 2):
        de, dap, nhieu, giai = _bat(ten, s)
        assert r"0^\circ < \alpha < 180^\circ" in de
        goc = _goc_tu_dieu_kien(de)
        assert goc, de
        hoi = re.search(r"(?:Giá trị của|Tính giá trị của) \$(.+?)\$", de).group(1)
        gt = {round(_gia_tri(hoi, a), 9) for a in goc}
        assert len(gt) == 1, ("de mo ho dau", de, goc, gt)
        dung = gt.pop()
        if ten.startswith("MC"):
            _kiem_mc(dap, nhieu, dung)
        else:
            _kiem_sa(de, dap, dung)


# ---------------------------------------------------------------- G: khong phu thuoc alpha / chua can
@pytest.mark.parametrize("ten", ["MC_G_01", "SA_G_01"])
def test_g_hang_so_doc_lap(ten):
    thay_can = thay_luy_thua = False
    for s in range(SO_LAN):
        de, dap, nhieu, giai = _bat(ten, s)
        bt = re.search(r"biểu thức \$M = (.+?)\$", de).group(1)
        thay_can |= r"\sqrt" in bt
        thay_luy_thua |= r"\sin^{6}" in bt
        gia = {round(_gia_tri(bt, random.uniform(0, 180)), 9) for _ in range(6)}
        assert len(gia) == 1, (bt, gia)
        dung = gia.pop()
        assert abs(dung - round(dung)) < 1e-9
        if ten.startswith("MC"):
            _kiem_mc(dap, nhieu, dung)
        else:
            assert int(dap) == round(dung) and dap not in nhieu
    assert thay_can and thay_luy_thua


def test_dung_loai_cau_va_da_dang():
    for ten in ["MC_D_01", "MC_D_02", "SA_D_01", "MC_E_01", "SA_E_01", "MC_F_01", "SA_F_01", "MC_G_01", "SA_G_01",
                "MC_H_01", "MC_H_02", "SA_H_01"]:
        de_khac = set()
        for s in range(60):
            random.seed(s)
            o = getattr(M, P + ten)(1)
            if ten.startswith("MC"):
                assert r"\choice" in o and r"\shortans" not in o
            else:
                assert r"\shortans" in o and r"\choice" not in o
            de_khac.add(o.split(r"\choice")[0].split(r"\shortans")[0])
        assert len(de_khac) >= 30, (ten, len(de_khac))      # python tu sinh, khong phai de chet


# ---------------------------------------------------------------- H (VD): biet cos (0 < a < 180) / sin + goc nhon, tu
@pytest.mark.parametrize("ten", ["MC_H_01", "MC_H_02", "SA_H_01"])
def test_h_dap_so_doc_lap(ten):
    for s in range(SO_LAN // 2):
        de, dap, nhieu, giai = _bat(ten, s)
        m = re.search(r"là góc (tù|nhọn) thoả mãn \$\\sin\\alpha = (.+?)\$", de)
        if m:
            v = tinh(m.group(2))
            goc = [a for a in _cac_goc(lambda x: _gia_tri(r"\sin\alpha", x) - v) if (a > 90) == (m.group(1) == "tù")]
        else:
            v = tinh(re.search(r"\$\\cos\\alpha = (.+?)\$", de).group(1))
            assert r"0^\circ < \alpha < 180^\circ" in de
            goc = _cac_goc(lambda x: _gia_tri(r"\cos\alpha", x) - v)
        assert len(goc) == 1, (de, goc)                    # dieu kien xac dinh duy nhat goc
        bt = re.search(r"biểu thức \$P = (.+?)\$", de).group(1)
        assert r"\tan\alpha" in bt or r"\cot\alpha" in bt
        dung = _gia_tri(bt, goc[0])
        if ten.startswith("MC"):
            _kiem_mc(dap, nhieu, dung)
        else:
            _kiem_sa(de, dap, dung)
