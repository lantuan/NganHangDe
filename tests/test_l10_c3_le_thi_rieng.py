"""Cong vien Le Thi Rieng (co Lan 13/10/2026): kiem lai DOC LAP.

Hai bien the _02 (cong vien, dap so ha) va _03 (khu vuc ranh mo ngau nhien, dap so m2) cua CUNG dang voi Cong Troi:
cac ID MC_J / SA_L / TL_I. Moi cau: doc 5 so do trong de, tu tinh lai dien tich bang Heron (viet rieng, khong goi ham sinh),
so voi dap so in ra; dien tich phai sat so that (lech <= 3%); de KHONG lo dien tich cua chinh doi tuong duoc hoi;
MC co 4 phuong an khac nhau; SA <= 4 ky tu; hinh ghi don vi m (Cong Troi _01 van ghi km).
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
_spec = importlib.util.spec_from_file_location("L10_C3_ltr_test", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_ltr_test"] = M
_spec.loader.exec_module(M)

THAT = {"công viên Lê Thị Riêng": 75000, "Khu vực số $1$": 800, "Khu vực số $2$": 1200, "Khu vực số $3$": 500,
        "khu vực tìm kiếm mở rộng": 5800}


def _lt(x):
    return int(math.floor(x + 0.5))


def _num(t):
    return float(t.replace(",", "."))


def _heron(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def _de(txt):
    return txt.split("\\loigiai")[0]


def _doc(txt):
    """(ten doi tuong, S1 = BCD, S2 = ABD, S) tinh lai tu cac so do trong de."""
    de = _de(txt)
    ab, bc, cd, da, bd = (int(re.search(k + r" = (\d+)\$ m", de).group(1)) for k in ("AB", "BC", "CD", "DA", "BD"))
    # toa do: B = (0,0), D = (bd,0); C va A o hai phia khac nhau -> tu giac loi
    xc = (bc * bc + bd * bd - cd * cd) / (2 * bd)
    xa = (ab * ab + bd * bd - da * da) / (2 * bd)
    yc, ya = math.sqrt(bc * bc - xc * xc), math.sqrt(ab * ab - xa * xa)
    S1, S2 = bd * yc / 2, bd * ya / 2
    assert abs(S1 - _heron(bc, cd, bd)) < 1e-6 and abs(S2 - _heron(ab, da, bd)) < 1e-6
    ten = [k for k in THAT if re.search(r"(Tính diện tích của|Diện tích của) " + re.escape(k), de)]
    assert len(ten) == 1, ten
    return ten[0], S1, S2, S1 + S2, (ab, bc, cd, da, bd)


def _vi_du(txt, ten):
    """De khong duoc nhac dien tich cua chinh doi tuong duoc hoi."""
    de = _de(txt)
    if ten == "công viên Lê Thị Riêng":
        assert "7,5$ ha" not in de and "75\\,000" not in de and "75000" not in de
    else:
        assert str(THAT[ten]) not in de.replace("\\,", "").replace(" ", "")


def _khop_ha(S, chuoi):
    return abs(_num(chuoi) - math.floor(S / 1e4 * 10 + 0.5) / 10) < 1e-9


def _sa(txt):
    return re.search(r"\\shortans\{\s*\$([^$]*)\$\}", txt).group(1).strip()


def _mc(txt):
    return re.findall(r"\{\s*(\\True\s*)?\$\s*([^$]*?)\s*\$\}", txt.split("\\choice", 1)[1].split("\\loigiai")[0])


def _kiem(ten, S, chuoi):
    assert abs(S - THAT[ten]) <= 0.03 * THAT[ten] + 1e-9, (ten, S)
    if ten == "công viên Lê Thị Riêng":
        assert _khop_ha(S, chuoi), (S, chuoi)
    else:
        assert int(chuoi) == _lt(S), (S, chuoi)


@pytest.mark.parametrize("bt,ham", [(2, "SA_L"), (3, "SA_L")])
def test_sa_khop_doc_lap(bt, ham):
    f = getattr(M, "L10_C3_B6_VD036_%s_%02d" % (ham, bt))
    thay = set()
    for sd in range(150):
        random.seed(sd)
        txt = f(1)
        ten, S1, S2, S, _ = _doc(txt)
        thay.add(ten)
        assert (ten == "công viên Lê Thị Riêng") == (bt == 2)
        _kiem(ten, S, _sa(txt))
        assert len(_sa(txt).replace(",", "")) <= 4
        _vi_du(txt, ten)
    if bt == 3:
        assert len(thay) == 4, thay


@pytest.mark.parametrize("bt", [2, 3])
def test_mc_dung_va_bon_phuong_an_khac_nhau(bt):
    f = getattr(M, "L10_C3_B6_VD036_MC_J_%02d" % bt)
    for sd in range(150):
        random.seed(sd)
        txt = f(1)
        ten, S1, S2, S, _ = _doc(txt)
        ds = _mc(txt)
        assert len(ds) == 4 and len({x[1] for x in ds}) == 4, (sd, ds)
        dung = [x[1] for x in ds if x[0]]
        assert len(dung) == 1
        _kiem(ten, S, dung[0])
        _vi_du(txt, ten)


@pytest.mark.parametrize("bt", [2, 3])
def test_tl_hai_y(bt):
    f = getattr(M, "L10_C3_B6_VD036_TL_I_%02d" % bt)
    for sd in range(150):
        random.seed(sd)
        txt = f(1)
        de = _de(txt)
        ten = [k for k in THAT if re.search(r"Tính diện tích của " + re.escape(k), de)][0]
        ab, bc, cd, da, bd = (int(re.search(k + r" = (\d+)\$ m", de).group(1)) for k in ("AB", "BC", "CD", "DA", "BD"))
        S1, S2 = _heron(bc, cd, bd), _heron(ab, da, bd)
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", txt)
        assert len(ys) == 2
        so = [re.search(r"approx ([\d,]+)", y).group(1) for y in ys]
        tg = re.search(r"Tính diện tích tam giác \$(\w+)\$", de).group(1)
        assert int(so[0]) == _lt(S1 if tg == "BCD" else S2)
        _kiem(ten, S1 + S2, so[1])
        _vi_du(txt, ten)
        # loi giai y b) chi tinh tam giac CON LAI roi cong (khong lap lai tam giac y a))
        b = txt.split("\\loigiai")[1].split("\\item")[2]
        assert b.count("nửa chu vi") == 1 and ("Tam giác $%s$" % ("ABD" if tg == "BCD" else "BCD")) in b


def test_hinh_don_vi():
    random.seed(1)
    for f in (M.L10_C3_B6_VD036_MC_J_02, M.L10_C3_B6_VD036_MC_J_03):
        t = f(1)
        assert " m}" in t and " km}" not in t
    # Cong Troi _01 van ghi km
    for sd in range(5):
        random.seed(sd)
        assert " km}" in M.L10_C3_B6_VD036_MC_J_01(1)


def test_mapping_cung_dang():
    rows = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C3.json", encoding="utf-8"))}
    ids = ["L10_C3_B6_VD036_MC_J", "L10_C3_B6_VD036_SA_L", "L10_C3_B6_VD036_TL_I"]
    dang = {rows[i]["Dang"] for i in ids}
    assert len(dang) == 1 and "Lê Thị Riêng" in dang.pop()
    assert all(rows[i]["boi_canh"] == "cong_troi" for i in ids)
    assert not any("le_thi_rieng" in i.lower() for i in rows)


def test_dan_co_nguon_va_khong_loi_thoai():
    random.seed(0)
    de = _de(M.L10_C3_B6_VD036_SA_L_03(1))
    for must in ("Tết Mậu Thân", "$731$", "$11/10/2026$", "$14/10/2026$", "giả định", "ông cha"):
        assert must in de, must
