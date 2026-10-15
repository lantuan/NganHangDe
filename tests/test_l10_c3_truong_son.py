"""Bai toan thuc tien gan voi duong Truong Son (co Lan 13/10/2026): kiem lai DOC LAP.

5 boi canh la 5 bien the _01.._05 cua CUNG mot dang (MC_U / MC_V / SA_U / SA_V / TL_N).
Moi cau: doc so lieu trong de bai, tu tinh lai dap so bang cong thuc rieng (khong goi lai ham sinh) roi so voi
dap so in ra (SA: \\shortans; MC: phuong an {\\True}; TL: hai y). Kiem them mapping (boi_canh chung "truong_son",
muc_do_dang VDC cho MC_V / SA_V) va moi bien the dung 4 phuong an khac nhau.
"""
import importlib.util
import json
import math
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C3_ts_test", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_ts_test"] = M
_spec.loader.exec_module(M)

S = lambda d: math.sin(math.radians(d))
C = lambda d: math.cos(math.radians(d))


def _lt(x):
    return int(math.floor(x + 0.5))


def _num(t):
    return float(t.replace(",", "."))


def _de(txt):
    """Phan de bai (truoc dap an / loi giai)."""
    return txt.split("\\loigiai")[0]


def _doc(bien, txt):
    """Doc so lieu trong de, tra ve (dap so y a, dap so y b) tinh lai doc lap."""
    de = _de(txt)
    if bien == 1:
        h = int(re.search(r"tối đa \$(\d+)\$ m", de).group(1))
        H = int(re.search(r"núi cao \$(\d+)\$ m", de).group(1))
        al = int(re.search(r"nghiêng \$(\d+)\^\{\\circ\}\$", de).group(1))
        return -(-H // h), H / S(al), (0, 0)
    if bien == 2:
        d = int(re.search(r"OK = (\d+)\$ km", de).group(1))
        th = int(re.search(r"OKK'\} = (\d+)\^", de).group(1))
        ok = math.sqrt(d * d + 100 - 20 * d * C(th))
        # goc KOK' tu toa do: O = (0,0), K = (d, 0), K' = K + 10*(cos(180-th), sin(180-th))
        kp = (d - 10 * C(th), 10 * S(th))
        return ok, math.degrees(math.atan2(kp[1], kp[0])), (1, 0)
    if bien == 3:
        m1 = re.search(r"đi \$(\d+)\$ km theo phương vị \$(\d+)\^\{\\circ\}\$ đến \$B\$", de)
        m2 = re.search(r"đi tiếp \$(\d+)\$ km theo phương vị \$(\d+)\^\{\\circ\}\$ đến \$C\$", de)
        d1, a1, d2, a2 = int(m1.group(1)), int(m1.group(2)), int(m2.group(1)), int(m2.group(2))
        bx, by = d1 * S(a1), d1 * C(a1)
        cx, cy = bx + d2 * S(a2), by + d2 * C(a2)
        return math.hypot(cx, cy), math.degrees(math.atan2(cx, cy)) % 360, (1, 0)
    if bien == 4:
        AC = int(re.search(r"AC = (\d+)\$ m", de).group(1))
        CB = int(re.search(r"CB = (\d+)\$ m", de).group(1))
        g = int(re.search(r"ACB\} = (\d+)\^", de).group(1))
        AB = math.sqrt((AC - CB * C(g)) ** 2 + (CB * S(g)) ** 2)
        return AB, AC + CB - _lt(AB), (0, 0)
    c = _num(re.search(r"AB = ([\d,]+)\$ km", de).group(1))
    a = _num(re.search(r"BC = ([\d,]+)\$ km", de).group(1))
    b = _num(re.search(r"CA = ([\d,]+)\$ km", de).group(1))
    # dien tich bang toa do: B = (0,0), C = (a,0), A = (x, y)
    x = (a * a + c * c - b * b) / (2 * a)
    y = math.sqrt(c * c - x * x)
    return a * y / 2, y, (2, 2)


def _khop(v, chuoi, n):
    k = 10 ** n
    return abs(_num(chuoi) - math.floor(v * k + 0.5) / k) < 1e-9


def _sa(txt):
    return re.search(r"\\shortans\{\s*\$([^$]*)\$\}", txt).group(1)


def _mc(txt):
    ds = re.findall(r"\{\s*(\\True\s*)?\$\s*([^$]*?)\s*\$\}", txt.split("\\choice", 1)[1].split("\\loigiai")[0])
    return ds


@pytest.mark.parametrize("bien", [1, 2, 3, 4, 5])
def test_sa_dap_so_khop_doc_lap(bien):
    for ham, ph in (("SA_U", 0), ("SA_V", 1)):
        f = getattr(M, "L10_C3_B6_VD036_%s_%02d" % (ham, bien))
        for sd in range(60):
            random.seed(sd)
            txt = f(1)
            a, b, nd = _doc(bien, txt)
            v, n = ((a, nd[0]) if ph == 0 else (b, nd[1]))
            assert _khop(v, _sa(txt), n), (ham, bien, sd, v, _sa(txt))
            assert len(_sa(txt).replace(",", "")) <= 4


@pytest.mark.parametrize("bien", [1, 2, 3, 4, 5])
def test_mc_dap_an_dung_va_bon_phuong_an_khac_nhau(bien):
    for ham, ph in (("MC_U", 0), ("MC_V", 1)):
        f = getattr(M, "L10_C3_B6_VD036_%s_%02d" % (ham, bien))
        for sd in range(60):
            random.seed(sd)
            txt = f(1)
            a, b, nd = _doc(bien, txt)
            v, n = ((a, nd[0]) if ph == 0 else (b, nd[1]))
            ds = _mc(txt)
            assert len(ds) == 4 and len({x[1] for x in ds}) == 4, (ham, bien, sd, ds)
            dung = [x[1] for x in ds if x[0]]
            assert len(dung) == 1 and _khop(v, dung[0], n), (ham, bien, sd, v, dung)


@pytest.mark.parametrize("bien", [1, 2, 3, 4, 5])
def test_tl_hai_y_dap_so_khop(bien):
    f = getattr(M, "L10_C3_B6_VD036_TL_N_%02d" % bien)
    for sd in range(60):
        random.seed(sd)
        txt = f(1)
        a, b, nd = _doc(bien, txt)
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", txt)
        assert len(ys) == 2, (bien, sd, ys)
        for y, v, n in zip(ys, (a, b), nd):
            so = re.search(r"([\d]+(?:,\d+)?)", y.split("approx")[-1] if "approx" in y else y).group(1)
            if bien == 4 and v is b:
                pass
            assert _khop(v, so, n), (bien, sd, y, v)


def test_mapping_truong_son():
    rows = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C3.json", encoding="utf-8"))}
    ids = ["L10_C3_B6_VD036_MC_U", "L10_C3_B6_VD036_MC_V", "L10_C3_B6_VD036_SA_U", "L10_C3_B6_VD036_SA_V", "L10_C3_B6_VD036_TL_N"]
    assert len({rows[i]["Dang"] for i in ids}) == 1
    for i in ids:
        assert rows[i]["boi_canh"] == "truong_son"
        assert (rows[i].get("muc_do_dang") == "VDC") == i.endswith(("_V", "_X"))
    src = (GOC / "data" / "python_bank" / "toan10" / "L10_C3.py").read_text(encoding="utf-8")
    for i in ids:
        for b in range(1, 6):
            assert "def %s_%02d(" % (i, b) in src


def test_moi_de_chi_mot_bai_truong_son():
    """Chon de nhieu lan: khong de nao co hai cau cung boi canh truong_son."""
    import collections
    from app.services.exam_blueprint_service import build_blueprint
    from app.services.mapping_service import load_mapping
    from app.services.question_selector_service import select_questions
    dong = {r["id"]: r for r in load_mapping(10, 3)}
    for sd in range(40):
        random.seed(sd)
        ds = select_questions(10, build_blueprint(10, "HeSo1", pham_vi_chuong="3"))
        dem = collections.Counter()
        for c in ds:                                   # boi_canh co the la chuoi hoac danh sach (vd VD036_MC_C, SA_C)
            bc = dong.get(c.get("generator_id"), {}).get("boi_canh")
            dem.update(bc if isinstance(bc, list) else [bc])
        assert dem.get("truong_son", 0) <= 1, (sd, [c.get("generator_id") for c in ds])
