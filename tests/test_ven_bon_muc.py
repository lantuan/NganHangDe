# -*- coding: utf-8 -*-
r"""Biểu đồ Ven NB / VD / VDC (cô Lan 04/10/2026), ID đúng mức: NB019_MC_A (NB), VD019_MC_B/SA_B (VD), VD019_MC_C/SA_C (VDC).

Đọc lại HÌNH TikZ do hàm sinh (các scope gạch sọc, các đường tròn, số ghi trong vùng) và TÍNH ĐỘC LẬP:
- đúng một phương án có tập vùng bằng vùng gạch sọc, và đó là phương án \True;
- câu SA: đáp số = tổng số phần tử các vùng của biểu thức.
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
_spec = importlib.util.spec_from_file_location("L10_C1_ven_bon_muc", BANK / "toan10" / "L10_C1.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C1_ven_bon_muc"] = M
_spec.loader.exec_module(M)

P = "L10_C1_B2_"


def _cau(out):
    return [b for b in out.split(r"\begin{ex}")[1:]]


def _hinh(blk):
    return re.search(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", blk, flags=re.S).group(0)


def _vong(tikz):
    return [(float(a), float(b), float(r)) for a, b, r in
            re.findall(r"\\def\\vong[A-F]\{\(([-\d.]+),([-\d.]+)\) circle \(([-\d.]+)\)\}", tikz)]


# 10/10/2026: [even odd rule] chuyen len muc scope (TikZ cu khong cho tuy chon tren \clip) -> doc lai theo cach moi.
def _mask_gach(tikz):
    vong = _vong(tikz)
    masks = set()
    for sc in re.findall(r"\\begin\{scope\}(?:\[even odd rule\])?(.*?)\\end\{scope\}", tikz, flags=re.S):
        if r"\fill[pattern" not in sc:
            continue
        m = [None] * len(vong)
        for i, ch in enumerate("ABCDEF"[:len(vong)]):
            if r"\clip \vong%s;" % ch in sc:
                m[i] = 1
        for cx, cy, r in re.findall(r"\\clip \(-8,-8\) rectangle \(9,9\) \(([-\d.]+),([-\d.]+)\) circle \(([-\d.]+)\);", sc):
            i = vong.index((float(cx), float(cy), float(r)))
            assert m[i] is None
            m[i] = 0
        assert None not in m, sc
        masks.add(tuple(m))
    return masks


def _vu_tru(vong):
    n = len(vong)
    import itertools
    return {m for m in itertools.product((0, 1), repeat=n)}


def _tinh(bt, ten, vu_tru, E=None):
    """Tính biểu thức LaTeX thành tập các vùng. ten: danh sách chữ theo thứ tự đường tròn."""
    env = {}
    for i, t in enumerate(ten):
        env[t] = {m for m in vu_tru if m[i]}
    env["E"] = set(vu_tru) if E is None else E
    s = bt.strip()
    s = re.sub(r"C_E\s*\(", "(E - (", s)
    if s.startswith("(E - ("):
        s += ")"
    s = re.sub(r"C_([A-Z])\s+([A-Z])", r"(\1 - \2)", s)
    s = s.replace(r"\cap", "&").replace(r"\cup", "|").replace(r"\setminus", "-")
    return set(eval(s, {}, env))


def _phuong_an(blk):
    ds = blk.split(r"\choice", 1)[1].split(r"\loigiai")[0]
    pa = re.findall(r"\{(\\True )?\$([^$]*)\$\}", ds)
    return [(bool(t), x) for t, x in pa]


@pytest.mark.parametrize("ten_ham", ["NB019_MC_A_01", "VD019_MC_B_01", "VD019_MC_C_01", "VD019_SA_A_01", "VD019_SA_B_01"])
def test_chay_nhieu_hat_giong(ten_ham):
    f = getattr(M, P + ten_ham)
    for s in range(150):
        random.seed(s)
        out = f(4)
        assert out.count(r"\begin{ex}") == 4 and r"\loigiai" in out


@pytest.mark.parametrize("seed", range(150))
@pytest.mark.parametrize("ten_ham", ["VD019_MC_B_01", "VD019_MC_C_01"])
def test_ba_tap_dung_mot_phuong_an(ten_ham, seed):
    random.seed(seed)
    for blk in _cau(getattr(M, P + ten_ham)(4)):
        tikz = _hinh(blk)
        ten = re.search(r"tập hợp \$(\w)\$, \$(\w)\$, \$(\w)\$ là", blk).groups()
        gach = _mask_gach(tikz)
        vu_tru = _vu_tru(_vong(tikz))
        pa = _phuong_an(blk)
        assert len(pa) == 4 and sum(t for t, _ in pa) == 1
        kq = [(t, _tinh(x, ten, vu_tru) == gach) for t, x in pa]
        assert [t for t, _ in kq] == [d for _, d in kq], (blk[:200], pa)
        assert len({x for _, x in pa}) == 4


@pytest.mark.parametrize("seed", range(150))
def test_hai_tap_nb_dung_mot_phuong_an(seed):
    random.seed(seed)
    for blk in _cau(getattr(M, P + "NB019_MC_A_01")(4)):
        tikz = _hinh(blk)
        gach = _mask_gach(tikz)
        vong = _vong(tikz)
        pa = _phuong_an(blk)
        assert len(pa) == 4 and sum(t for t, _ in pa) == 1
        ten = re.findall(r"\$(\w)\$", blk.split(r"\choice")[0])
        if len(vong) == 2 and "\\subset" in blk:                 # A nằm trong B
            p, q = re.search(r"\$(\w) \\subset (\w)\$", blk).groups()
            vu = {(0, 1), (1, 1)}
            env = {p: {(1, 1)}, q: {(0, 1), (1, 1)}}
            for t, x in pa:
                s = x
                s = re.sub(r"C_(\w) (\w)", r"(\1 - \2)", s)
                kq = set(eval(s, {}, env))
                assert t == (kq == gach), (blk[:300], x)
        elif len(vong) == 1:                                     # A nằm trong E
            p = re.search(r"Cho \$(\w)\$ là tập con", blk).group(1)
            env = {p: {(1,)}, "E": {(0,), (1,)}}
            for t, x in pa:
                s = re.sub(r"C_E (\w)", r"(E - \1)", x)
                s = re.sub(r"C_(\w) E", r"(\1 - E)", s)
                kq = set(eval(s, {}, env))
                assert t == (kq == gach), (blk[:300], x)
        else:                                                    # hai đường tròn cắt nhau
            p, q = ten[0], ten[1]
            vu = _vu_tru(vong)
            for t, x in pa:
                assert t == (_tinh(x, (p, q), vu) == gach), (blk[:300], x)


@pytest.mark.parametrize("seed", range(150))
@pytest.mark.parametrize("ten_ham", ["VD019_SA_A_01", "VD019_SA_B_01"])
def test_sa_dem_dung_tong_cac_vung(ten_ham, seed):
    random.seed(seed)
    for blk in _cau(getattr(M, P + ten_ham)(4)):
        tikz = _hinh(blk)
        vong = _vong(tikz)
        ten = re.search(r"tập hợp \$(\w)\$, \$(\w)\$, \$(\w)\$ là", blk).groups()
        bt = re.search(r"Tính số phần tử \$n\((.*?)\)\$ của tập hợp", blk).group(1)
        dem = {}
        for x, y, so in re.findall(r"\\node\[fill=white, inner sep=0.5pt\] at \(([-\d.]+),([-\d.]+)\) \{\$(\d+)\$\};", tikz):
            m = tuple(1 if (float(x) - cx) ** 2 + (float(y) - cy) ** 2 < r * r else 0 for cx, cy, r in vong)
            assert m not in dem
            dem[m] = int(so)
        assert len(dem) == 8
        vung = _tinh(bt, ten, _vu_tru(vong))
        dap = int(re.search(r"\\shortans\{\s*\$(\d+)\$\}", blk).group(1))
        assert dap == sum(dem[m] for m in vung), blk[:300]


def test_vung_so_cua_vd_va_vdc_khac_nhau_va_du_dang():
    vd = {M._bt_vung(e) for e in M._ven_muc_tieu("VD")}
    vdc = {M._bt_vung(e) for e in M._ven_muc_tieu("VDC")}
    assert len(vd) == 6 and not (vd & vdc) and len(vdc) == 13


def test_ba_tap_ten_khac_a_b_c_van_dung():
    random.seed(2)
    thay = set()
    for _ in range(40):
        out = M.L10_C1_B2_VD019_MC_C_01(2)
        thay.add(re.search(r"tập hợp \$(\w)\$", out).group(1))
    assert thay == {"A", "M", "X"}


# ----------------------------------------------------------- mapping / curriculum
def _mapping():
    return {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C1.json", encoding="utf-8"))}


def test_mapping_ven_id_dung_muc_va_danh_dau():
    mp = _mapping()
    cur = {r["id"]: r for r in json.load(open(GOC / "data" / "curriculum" / "toan10" / "L10_C1.json", encoding="utf-8"))}
    # cùng đơn vị 019: mỗi mức một mục Curriculum, cùng nội dung YCCĐ
    for muc in ("NB", "TH", "VD"):
        assert cur["L10_C1_B2_%s019" % muc]["MucDo"] == muc
    assert cur["L10_C1_B2_NB019"]["content"] == cur["L10_C1_B2_TH019"]["content"] == cur["L10_C1_B2_VD019"]["content"]
    nb = mp[P + "NB019_MC_A"]                                       # NB thấp hơn YCCĐ TH019: không ghi chú
    assert "ngoai_yccd" not in nb and "muc_do_dang" not in nb
    moi = ("VD019_MC_A", "VD019_MC_B", "VD019_SA_A", "VD019_MC_C", "VD019_SA_B")
    for i in moi:                                                   # VD/VDC cao hơn YCCĐ: ghi chú
        r = mp[P + i]
        assert r["ngoai_yccd"] is True and r["ghi_chu"].startswith("LUYEN TAP THEM")
        assert (r.get("muc_do_dang") == "VDC") == i.endswith(("MC_C", "SA_B")), i
    dang = [g for d in cur["L10_C1_B2_VD019"]["dang_luyen_tap_them"] for g in d["mapping_id"]]
    assert set(dang) == {P + i for i in moi}
    assert "L10_C1_B2_TH019_MC_A" not in mp and "dang_luyen_tap_them" not in cur["L10_C1_B2_VD020"]
