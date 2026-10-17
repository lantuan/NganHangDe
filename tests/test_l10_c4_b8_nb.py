# -*- coding: utf-8 -*-
r"""Bai 8 lop 10 muc NHAN BIET (co Lan 17/10/2026, duyet ke hoach ID): NB040_MC_A, NB041_MC_A, NB042_MC_A (dien
khuyet / goi ten quy tac, tinh chat - chi MC), NB040_MC_B/SA_B, NB041_MC_B/SA_B (chon / dem khang dinh dung).

Kiem chung DOC LAP: moi phat bieu dang dang thuc vecto duoc tinh lai bang tests/_tinh_tex.py voi toa do ngau nhien
(diem bat ki, hinh binh hanh ngau nhien, vecto tu do ngau nhien); phat bieu bang loi doi chieu bang chan tri viet tay
trong test (khong lay tu file sinh de).
"""
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC / "tests"))
from _tinh_tex import V, bang, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C4_b8_nb", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_b8_nb"] = M
_spec.loader.exec_module(M)

P8 = "L10_C4_B8_"


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, *a, **k: cap.append((de, str(dap), list(nhieu), giai)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, P8 + ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _moi_truong(tex):
    """Toạ độ ngẫu nhiên cho mọi điểm và vectơ tự do xuất hiện; 'hình bình hành $XYZT$' thì Z = Y + T - X."""
    P = {t: V(random.uniform(-9, 9), random.uniform(-9, 9)) for t in set(re.findall(r"\\overrightarrow\{([A-Z])", tex) +
                                                                          re.findall(r"\\overrightarrow\{[A-Z]([A-Z])\}", tex))}
    for t in re.findall(r"\$([A-Z])\$", tex):
        P.setdefault(t, V(random.uniform(-9, 9), random.uniform(-9, 9)))
    m = re.search(r"hình bình hành \$([A-Z])([A-Z])([A-Z])([A-Z])\$", tex) or \
        re.search(r"\$([A-Z])([A-Z])([A-Z])([A-Z])\$ là hình bình hành", tex)
    if m:
        X, Y, Z, T = m.groups()
        for t in (X, Y, T):
            P.setdefault(t, V(random.uniform(-9, 9), random.uniform(-9, 9)))
        P[Z] = P[Y] + P[T] - P[X]
    W = {t: V(random.uniform(-9, 9), random.uniform(-9, 9)) for t in "abcuvwxyz"}
    return P, W


def _gia_tri(tex, P, W):
    return tinh(tex, P=P, W=W)


# ---------------------------------------------------------------- B: khang dinh dung / sai
LOI = {  # phát biểu bằng lời -> chân trị (viết tay, độc lập)
    "Tổng của hai vectơ là một vectơ": True, "Tổng của hai vectơ là một số": False,
    "Vectơ đối của vectơ-không là vectơ-không": True, "Vectơ-không không có vectơ đối": False,
    "Hai vectơ đối nhau thì có cùng độ dài": True, "Hai vectơ đối nhau thì cùng hướng": False,
    "Hai vectơ có cùng độ dài thì đối nhau": False,
}


def _chan_tri(kd):
    """Chân trị của một khẳng định, tính độc lập."""
    if kd in LOI:
        return LOI[kd]
    m = re.fullmatch(r"Vectơ đối của \$(\\overrightarrow\{\w\w\})\$ là \$(\\overrightarrow\{\w\w\})\$", kd)
    if m:
        P, W = _moi_truong(kd)
        return bang(-_gia_tri(m.group(1), P, W), _gia_tri(m.group(2), P, W))
    dt = re.findall(r"\$([^$]*=[^$]*)\$", kd)
    assert len(dt) == 1, kd
    ve = dt[0].split(":")[-1].split(" = ")                # chuỗi đẳng thức a = b = c: mọi vế bằng nhau
    kq = set()
    for _ in range(3):
        P, W = _moi_truong(kd)
        g = [_gia_tri(x.strip(), P, W) for x in ve]
        kq.add(all(bang(g[0], y) for y in g[1:]))
    return kq == {True}


@pytest.mark.parametrize("ten", ["NB040_MC_B_01", "NB041_MC_B_01"])
def test_b_mc_dung_mot_phuong_an(ten):
    for s in range(200):
        de, dap, nhieu, giai = _bat(ten, s)
        hoi = r"\textbf{đúng}" in de
        assert _chan_tri(dap) == hoi, (de, dap)
        assert all(_chan_tri(x) != hoi for x in nhieu), (de, nhieu)
        assert len(set([dap] + nhieu)) == 4


@pytest.mark.parametrize("ten", ["NB040_SA_B_01", "NB041_SA_B_01"])
def test_b_sa_dem_dung(ten):
    thay = set()
    for s in range(200):
        de, dap, nhieu, giai = _bat(ten, s)
        kd = re.findall(r"\d\) (.+?);(?:\\\\|$)", de)
        assert len(kd) == 4, de
        assert int(dap) == sum(_chan_tri(x) for x in kd), (de, dap)
        thay.add(int(dap))
    assert thay == {1, 2, 3}


# ---------------------------------------------------------------- A: dien khuyet, goi ten
QUY_TAC = {"quy tắc ba điểm", "quy tắc hình bình hành", "quy tắc trừ", "tính chất giao hoán của phép cộng vectơ",
           "tính chất kết hợp của phép cộng vectơ", "tính chất của vectơ-không", "tính chất giao hoán"}


def _ten_dung(de):
    """Tên quy tắc / tính chất đúng của đẳng thức trong đề, xác định độc lập từ dạng đẳng thức."""
    dt = re.search(r"[đĐ]ẳng thức \$([^$]+)\$", de).group(1)
    vt = re.findall(r"\\overrightarrow\{(\w+)\}", dt)
    if "hình bình hành" in de:
        return "quy tắc hình bình hành"
    if " - " in dt:
        return "quy tắc trừ"
    if all(len(x) == 2 and x.isupper() for x in vt):
        return "quy tắc ba điểm"
    if r"\overrightarrow{0}" in dt:
        return "tính chất của vectơ-không"
    if r"\left(" in dt:
        return "tính chất kết hợp của phép cộng vectơ"
    return "tính chất giao hoán của phép cộng vectơ"


@pytest.mark.parametrize("ten", ["NB040_MC_A_01", "NB041_MC_A_01", "NB042_MC_A_01"])
def test_a_dien_khuyet_doc_lap(ten):
    so_mau = set()
    for s in range(240):
        de, dap, nhieu, giai = _bat(ten, s)
        assert len(set([dap] + nhieu)) == 4
        so_mau.add(re.sub(r"\$[^$]*\$", "", de))
        if "được gọi là" in de or "thể hiện" in de:
            assert dap == _ten_dung(de) and dap in QUY_TAC, (de, dap)
            continue
        m = re.search(r"tính chất (giao hoán|kết hợp|cộng với vectơ-không) của phép cộng vectơ được viết là", de)
        if m:                                              # chọn đẳng thức: đúng là đồng nhất thức
            loai = lambda x: ("cộng với vectơ-không" if r"\overrightarrow{0}" in x else "kết hợp" if r"\left(" in x
                              else "giao hoán")
            assert _chan_tri("x: " + dap) and loai(dap) == m.group(1), (de, dap)
            for x in nhieu:                                # nhiễu: sai, hoặc đúng nhưng là tính chất khác
                assert not _chan_tri("x: " + x) or loai(x) != m.group(1), (de, x)
            continue
        # các câu mà phương án là vectơ: tính giá trị biểu thức trong đề
        P, W = _moi_truong(de)
        if "Vectơ đối của vectơ $" in de:
            u = re.search(r"Vectơ đối của vectơ \$([^$]+)\$", de).group(1)
            dung = -_gia_tri(u, P, W)
        elif "Lấy một điểm" in de:
            a, b = re.findall(r"vẽ \$(\\overrightarrow\{\w\w\}) = (\\overrightarrow\{\w\})\$", de)[0], \
                re.findall(r"và \$(\\overrightarrow\{\w\w\}) = (\\overrightarrow\{\w\})\$", de)[0]
            dung = _gia_tri(a[0], P, W) + _gia_tri(b[0], P, W)
        elif re.search(r"\$([^$]+)\$ bằng$", de):
            bt = re.search(r"\$([^$]+)\$ bằng$", de).group(1)
            dung = _gia_tri(bt, P, W)
        else:
            continue                                       # phương án bằng lời (vectơ-không, định nghĩa...)
        assert bang(_gia_tri(dap.strip("$"), P, W), dung), (de, dap)
        for x in nhieu:
            if x.startswith("$") and x.endswith("$") and "left(-" not in x:
                assert not bang(_gia_tri(x.strip("$"), P, W), dung), (de, x)
    assert len(so_mau) >= (4 if ten.startswith("NB042") else 5), so_mau


def test_mapping_curriculum_ngoai_le():
    m = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C4.json", encoding="utf-8"))}
    cur = {u["id"]: u for u in json.load(open(GOC / "data" / "curriculum" / "toan10" / "L10_C4.json", encoding="utf-8"))}
    nl = json.load(open(GOC / "data" / "mapping" / "id_mc_sa_ngoai_le.json", encoding="utf-8"))["L10_C4"]
    for u in ("NB040", "NB041", "NB042"):
        assert cur["L10_C4_B8_" + u]["MucDo"] == "NB" and "dang_luyen_tap_them" not in cur["L10_C4_B8_" + u]
        assert P8 + u + "_MC_A" in m and P8 + u + "_MC_A" in nl and not m[P8 + u + "_MC_A"].get("ngoai_yccd")
    for u in ("NB040", "NB041"):
        assert m[P8 + u + "_MC_B"]["Dang"] == m[P8 + u + "_SA_B"]["Dang"]


def test_python_tu_sinh():
    for ten in ("NB040_MC_A_01", "NB041_MC_A_01", "NB042_MC_A_01", "NB040_MC_B_01", "NB040_SA_B_01", "NB041_MC_B_01",
                "NB041_SA_B_01"):
        de = set()
        for s in range(100):
            random.seed(s)
            o = getattr(M, P8 + ten)(1)
            assert (r"\choice" in o) == ("_MC_" in ten) and (r"\shortans" in o) == ("_SA_" in ten)
            de.add(frozenset(o.split(r"\loigiai")[0].replace(r"\True ", "").split("\n")))
        assert len(de) >= (30 if ten.startswith("NB042") else 60), (ten, len(de))
