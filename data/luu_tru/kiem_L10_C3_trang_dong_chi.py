"""LUU TRU 21/10/2026 (co Lan: bai tho Dong chi thay khong hay, de nhap, chinh li lay lai sau). Test doc lap cua dang
nay, chuyen tu tests/test_l10_c3_trang_viet_bac.py; ten khong bat dau bang test_ va nam ngoai tests/ nen bo test chung
KHONG chay. Chay rieng:  python3 -m pytest data/luu_tru/kiem_L10_C3_trang_dong_chi.py
Dua dang tro lai ngan hang thi chuyen tep ve tests/ (doi lai duong dan L10_C3.py va Mapping).

Vang trang cua nguoi linh - bai tho Dong chi cua Chinh Huu (co Lan 13/10/2026): kiem lai DOC LAP.

_01: duong kinh Mat Trang tu khoang cach d va goc nhin theta (tam giac can; kiem bang dinh li cosin, KHONG dung cong thuc 2d.sin(theta/2) cua ham sinh).
     Du lieu thuc: d trong khoang can diem 363 300 - vien diem 405 500 km, duong kinh thu duoc gan 3 474-3 476 km (NASA).
_02: chieu cao cay co thu AB va khoang cach BC (suon doi dock): dung toa do - giao cua tia sang voi mat doc - roi tinh lai.
"""
import importlib.util
import json
import math
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C3_trang_test", GOC / "data" / "luu_tru" / "L10_C3_luu_tru.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_trang_test"] = M
_spec.loader.exec_module(M)

IDS = {"MC": "L10_C3_B6_VD036_MC_W", "SA": "L10_C3_B6_VD036_SA_W", "TL": "L10_C3_B6_VD036_TL_O"}


def _lt(x):
    return int(math.floor(x + 0.5))


def _num(t):
    return float(t.replace("\\,", "").replace(",", "."))


def _de(txt):
    return txt.split("\\loigiai")[0]


def _doc1(txt):
    de = _de(txt)
    d = int(re.search(r"khoảng \$([\d\\,]+)\$ km \(khoảng cách", de).group(1).replace("\\,", ""))
    th = _num(re.search(r"dưới góc khoảng \$([\d,]+)\^\{\\circ\}\$", de).group(1))
    D = math.sqrt(2 * d * d * (1 - math.cos(math.radians(th))))        # dinh li cosin: AB^2 = 2d^2(1 - cos theta)
    assert 363300 <= d <= 405500 and d % 100 == 0
    assert abs(D - 3475) <= 45, (d, th, D)                          # du lieu thuc: duong kinh that ~3 474-3 476 km
    return d, th, D


def _doc2(txt):
    de = _de(txt)
    be = int(re.search(r"nghiêng \$(\d+)\^\{\\circ\}\$", de).group(1))
    al = int(re.search(r"một góc \$(\d+)\^\{\\circ\}\$ và bóng", de).group(1))
    s = int(re.search(r"dài \$(\d+)\$ m", de).group(1))
    # A = (0,0) goc cay, C = A + s(cos be, sin be) dau bong tren doc, B = (0, h): tia sang B -> C huong (cos al, -sin al)
    C = (s * math.cos(math.radians(be)), s * math.sin(math.radians(be)))
    # B nam tren truc Oy sao cho tia tu B theo huong (cos al, -sin al) di qua C: t = C.x / cos al ; h = C.y + t sin al
    t = C[0] / math.cos(math.radians(al))
    h = C[1] + t * math.sin(math.radians(al))
    bc = t
    return al, be, s, h, bc


def _sa(txt):
    return re.search(r"\\shortans\{\s*\$([^$]*)\$\}", txt).group(1).strip()


def _mc(txt):
    ds = re.findall(r"\{\s*(\\True\s*)?\$\s*([^$]*?)\s*\$\}", txt.split("\\choice", 1)[1].split("\\loigiai")[0])
    assert len(ds) == 4 and len({x[1] for x in ds}) == 4, ds
    dung = [x[1] for x in ds if x[0]]
    assert len(dung) == 1
    return dung[0]


def _khop(v, s, n):
    k = 10 ** n
    return abs(_num(s) - math.floor(v * k + 0.5) / k) < 1e-9


@pytest.mark.parametrize("loai", ["SA", "MC"])
def test_bien_the_1_duong_kinh_mat_trang(loai):
    f = getattr(M, IDS[loai] + "_01")
    for sd in range(120):
        random.seed(sd)
        txt = f(1)
        d, th, D = _doc1(txt)
        got = _sa(txt) if loai == "SA" else _mc(txt)
        assert int(got) == _lt(D / 10) * 10, (sd, D, got)
        assert len(got) <= 4


@pytest.mark.parametrize("loai", ["SA", "MC"])
def test_bien_the_2_chieu_cao_cay(loai):
    f = getattr(M, IDS[loai] + "_02")
    for sd in range(120):
        random.seed(sd)
        txt = f(1)
        al, be, s, h, bc = _doc2(txt)
        got = _sa(txt) if loai == "SA" else _mc(txt)
        assert _khop(h, got, 1), (sd, h, got)
        assert 7 <= h <= 32 and al + be < 90


def test_tl_bien_the_1_hai_y():
    for sd in range(120):
        random.seed(sd)
        txt = M.L10_C3_B6_VD036_TL_O_01(1)
        d, th, D = _doc1(txt)
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", txt)
        assert len(ys) == 2
        chuc = _lt(D / 10) * 10
        assert int(re.search(r"approx (\d+(?:\\,\d{3})*)", ys[0]).group(1).replace("\\,", "")) == chuc
        d2 = int(re.search(r"cách Trái Đất \$([\d\\,]+)\$ km, đường kính", _de(txt)).group(1).replace("\\,", ""))
        # goc nhin o khoang cach d2 tu chinh duong kinh lam tron (cach tinh khac: dinh li cosin)
        cos_t = 1 - chuc ** 2 / (2.0 * d2 * d2)
        th2 = math.degrees(math.acos(cos_t))
        assert _khop(th2, re.search(r"approx ([\d,]+)\^", ys[1]).group(1), 2), (sd, th2, ys[1])


def test_tl_bien_the_2_hai_y():
    for sd in range(120):
        random.seed(sd)
        txt = M.L10_C3_B6_VD036_TL_O_02(1)
        al, be, s, h, bc = _doc2(txt)
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", txt)
        assert len(ys) == 2
        assert _khop(h, re.search(r"approx ([\d,]+)", ys[0]).group(1), 1)
        assert _khop(bc, re.search(r"approx ([\d,]+)", ys[1]).group(1), 1)


def test_ca_hai_bien_the_xuat_hien_va_dan_dung_su_that():
    random.seed(0)
    for ham in ("MC_W_01", "MC_W_02", "TL_O_01", "TL_O_02"):
        de = _de(getattr(M, "L10_C3_B6_VD036_" + ham)(1))
        # su that da kiem chung (hoatieu.vn, luatminhkhue.vn): Dong chi - Chinh Huu, dau nam 1948, sau chien dich Viet Bac thu dong 1947
        assert "Đồng chí" in de and "Chính Hữu" in de and "$1948$" in de and "$1947$" in de and "kháng chiến chống thực dân Pháp" in de
        assert "yêu đời" in de and "yêu thiên nhiên" in de and "Cụ Hồ" in de
        assert "Cảnh khuya" not in de and "Rằm tháng Giêng" not in de
        assert "\\begin{center}" not in de.split("\\begin{tikzpicture}")[0]      # khong co khoi tho (co Lan bo tho 13/10/2026)
    # de khong lo duong kinh that cua Mat Trang (dap so)
    de = _de(M.L10_C3_B6_VD036_SA_W_01(1))
    assert "3 474" not in de and "3474" not in de and "3\\,47" not in de


def test_khong_co_khoi_tho_va_hinh_chi_ghi_ten_diem():
    random.seed(2)
    assert not hasattr(M, "_tho_khoi") and not hasattr(M, "_TR_THO")
    h = M._tr_hinh1(384400, 0.52)
    assert "{$E$}" in h and "Trái Đất" not in h
    assert "{$A$}" in h and "{$B$}" in h


def test_mapping_mot_dang_mot_boi_canh():
    rows = {r["id"]: r for r in json.load(open(GOC / "data" / "luu_tru" / "L10_C3_mapping_luu_tru.json", encoding="utf-8"))}
    dang = {rows[i]["Dang"] for i in IDS.values()}
    assert len(dang) == 1
    assert all(rows[i]["boi_canh"] == "trang_dong_chi" for i in IDS.values())
    assert rows[IDS["MC"]]["Loai"].startswith("Trắc") and rows[IDS["SA"]]["Loai"] == "Trả lời ngắn" and rows[IDS["TL"]]["Loai"] == "Tự luận"
