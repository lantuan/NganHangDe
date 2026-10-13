"""Pac Bo - hanh trinh ve nuoc cua Bac, TU GIAC 4 trong 5 dia danh (co Lan 13/10/2026): kiem lai DOC LAP.

Doc ten bon dia danh va nam so do (AB, BC, CD, DA, AC) trong de, dung tu giac bang TOA DO roi tu tinh DIEN TICH va so voi SA / MC / TL
(Pac Bo la bien the _04 cua dang dien tich MC_J / SA_L / TL_I; de thuc te khong tinh goc). Kiem them: moi so do trong de lech toi da 15 m so voi khoang cach THAT giua dung
bon dia danh do (toa do tu Plus Code Google Maps co Lan gui, giai ma bang bo giai kiem voi vi du chuan cua dac ta Open Location Code;
hang Coc Bo: showcaves.com; suoi Le-nin: diem danh dau Google Maps), tu giac LOI, mapping.
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
_spec = importlib.util.spec_from_file_location("L10_C3_pb_test", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_pb_test"] = M
_spec.loader.exec_module(M)

_A = "23456789CFGHJMPQRVWX"


def _giai_ma_plus_code(ma):
    c = ma.replace("+", "")
    lat, lon, res = -90.0, -180.0, 20.0
    cap = c[:10]
    for k in range(0, len(cap), 2):
        lat += _A.index(cap[k]) * res
        lon += _A.index(cap[k + 1]) * res
        if k + 2 < len(cap):
            res /= 20
    dlat = dlon = res
    for ch in c[10:]:
        v = _A.index(ch)
        dlat /= 5
        dlon /= 4
        lat += (v // 4) * dlat
        lon += (v % 4) * dlon
    return lat + dlat / 2, lon + dlon / 2


def _hv(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (*p, *q))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


# toa do that, doc lap voi ma nguon (Plus Code day du; moc 675: ma 6 ky tu nen o ~14 m)
THAT = {
    "km0": _giai_ma_plus_code("7PJ8X3H2+4F8"),
    "lan": _giai_ma_plus_code("7PJ8X2MV+9PF"),
    "moc": _giai_ma_plus_code("7PJ8X3H3+P8"),
    "hang": (22.9872767, 106.0502709),
    "suoi": (22.9726677, 106.0467982),
}


def _khoa(ten):
    for k, w in (("Km", "km0"), ("hang", "hang"), ("lán", "lan"), ("675", "moc"), ("suối", "suoi")):
        if k in ten:
            return w
    raise AssertionError(ten)


def _num(t):
    return float(t.replace(",", "."))


def _khop(v, s, n):
    k = 10 ** n
    return abs(_num(s) - math.floor(v * k + 0.5) / k) < 1e-9


def _doc(txt):
    de = txt.split("\\loigiai")[0]
    names = re.findall(r"\$([ABCD])\$ \(([^()]*(?:\([^()]*\))?[^()]*)\)", de)
    assert [x[0] for x in names[:4]] == list("ABCD"), names
    ten = [_khoa(x[1]) for x in names[:4]]
    m = re.search(r"AB = (\d+)\$ m, \$BC = (\d+)\$ m, \$CD = (\d+)\$ m, \$DA = (\d+)\$ m và đường chéo \$(AC|BD) = (\d+)\$ m", de)
    ab, bc, cd, da = (int(m.group(i)) for i in (1, 2, 3, 4))
    cheo, dd = m.group(5), int(m.group(6))
    # dung tu giac bang toa do: duong cheo cho truoc nam tren truc x; X (tam giac chua AB) o tren, Y o duoi
    if cheo == "AC":
        l1, l2 = (ab, bc), (da, cd)
    else:
        l1, l2 = (ab, da), (bc, cd)
    xx = (l1[0] ** 2 + dd * dd - l1[1] ** 2) / (2 * dd)
    X = (xx, math.sqrt(l1[0] ** 2 - xx * xx))
    yy = (l2[0] ** 2 + dd * dd - l2[1] ** 2) / (2 * dd)
    Y = (yy, -math.sqrt(l2[0] ** 2 - yy * yy))
    E1, E2 = (0.0, 0.0), (float(dd), 0.0)
    A, B, C, D = (E1, X, E2, Y) if cheo == "AC" else (X, E1, Y, E2)
    P = [(q[0] - A[0], q[1] - A[1]) for q in (A, B, C, D)]            # dich de A la goc toa do
    A, B, C, D = P
    S = 0.5 * abs(sum(P[i][0] * P[(i + 1) % 4][1] - P[(i + 1) % 4][0] * P[i][1] for i in range(4)))
    cr = [(P[(i + 1) % 4][0] - P[i][0]) * (P[(i + 2) % 4][1] - P[(i + 1) % 4][1]) -
          (P[(i + 1) % 4][1] - P[i][1]) * (P[(i + 2) % 4][0] - P[(i + 1) % 4][0]) for i in range(4)]
    loi = all(x > 0 for x in cr) or all(x < 0 for x in cr)
    bd = math.hypot(B[0] - D[0], B[1] - D[1])
    u, v = (C[0] - B[0], C[1] - B[1]), (A[0] - B[0], A[1] - B[1])
    gB = math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))
    dAB = abs(B[0] * D[1] - B[1] * D[0]) / math.hypot(*B)                       # khoang cach D den duong thang AB
    sABD = 0.5 * abs(B[0] * D[1] - B[1] * D[0])                                   # dien tich tam giac ABD (A la goc toa do)
    gt = {"dt": (S / 1e4, 1), "goc": (gB, 0), "bd": (bd, 0), "kc": (dAB, 0), "dt3": (sABD / 1e4, 1)}
    return (ten, (ab, bc, cd, da, cheo, dd)), loi, gt


def _sa(txt):
    return re.search(r"\\shortans\{\s*\$([^$]*)\$\}", txt).group(1)


def _kiem_that(ten, so):
    """Do dai trong de = khoang cach that lam tron chuc met; rieng cap co diem suoi (dich toi da 30 m) cho phep lech them 30 m."""
    P = [THAT[k] for k in ten]
    ab, bc, cd, da, cheo, dd = so
    cap = [(0, 1, ab), (1, 2, bc), (2, 3, cd), (3, 0, da)] + [(0, 2, dd) if cheo == "AC" else (1, 3, dd)]
    for i, j, s in cap:
        sai = 5.01 + (30 if "suoi" in (ten[i], ten[j]) else 0)
        assert abs(_hv(P[i], P[j]) - s) <= sai, (ten, i, j, s, _hv(P[i], P[j]))
        if "suoi" not in (ten[i], ten[j]):
            assert s % 10 == 0 and abs(_hv(P[i], P[j]) - s) <= 5.01        # khong cong nhieu: dung lam tron that


def _mc_dung(txt):
    ds = re.findall(r"\{\s*(\\True\s*)?\$\s*([^$]*?)\s*\$\}", txt.split("\\choice", 1)[1].split("\\loigiai")[0])
    assert len(ds) == 4 and len({x[1] for x in ds}) == 4, ds
    dung = [x[1] for x in ds if x[0]]
    assert len(dung) == 1
    return dung[0]


def _khong_goc(txt):
    de = txt.split("\\loigiai")[0]
    assert "góc" not in de.replace("góc nhọn", "") and "widehat" not in de and "sin" not in de and "côsin" not in de


@pytest.mark.parametrize("ham", ["SA_L", "MC_J"])
def test_sa_mc_dap_so_khop_doc_lap(ham):
    gap = set()
    for sd in range(150):
        random.seed(sd)
        txt = getattr(M, "L10_C3_B6_VD036_%s_04" % ham)(1)
        (ten, so), loi, gt = _doc(txt)
        assert loi and len(set(ten)) == 4, (ten, so)
        _kiem_that(ten, so)
        _khong_goc(txt)
        got = _sa(txt) if ham.startswith("SA") else _mc_dung(txt)
        assert _khop(gt["dt"][0], got, gt["dt"][1]), (ham, sd, gt["dt"], got)
        assert len(got.replace(",", "")) <= 4
        gap.add(frozenset(ten))
    assert len(gap) == 3                      # ba bo tu giac loi trong nam dia danh, moi de chi dung 4 trong 5


def test_tl_hai_y_khop_doc_lap():
    for sd in range(150):
        random.seed(sd)
        txt = M.L10_C3_B6_VD036_TL_I_04(1)
        (ten, so), loi, gt = _doc(txt)
        assert loi
        _kiem_that(ten, so)
        _khong_goc(txt)
        ab, bc, cd, da, cheo, ac = so
        if cheo == "AC":
            n1, n2, S1, S2 = "ABC", "ACD", M._pb_heron(ab, bc, ac), M._pb_heron(ac, cd, da)
        else:
            n1, n2, S1, S2 = "ABD", "BCD", M._pb_heron(ab, da, ac), M._pb_heron(bc, cd, ac)
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", txt)
        assert len(ys) == 2
        tg = re.search(r"Tính diện tích tam giác \$(\w+)\$", txt).group(1)
        a1 = re.search(r"approx (\d+)", ys[0]).group(1)
        assert int(a1) == math.floor((S1 if tg == n1 else S2) + 0.5), (sd, ys, S1, S2)
        assert _khop(gt["dt"][0], re.search(r"approx (\d+(?:,\d+)?)", ys[1]).group(1), gt["dt"][1]), (sd, ys, gt["dt"])
        b = txt.split("\\loigiai")[1].split("\\item")[2]
        assert b.count("nửa chu vi") == 1 and ("Tam giác $%s$" % (n2 if tg == n1 else n1)) in b


def test_mapping_pac_bo_nam_trong_dang_dien_tich():
    rows = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C3.json", encoding="utf-8"))}
    ids = ["L10_C3_B6_VD036_MC_J", "L10_C3_B6_VD036_SA_L", "L10_C3_B6_VD036_TL_I"]
    dang = {rows[i]["Dang"] for i in ids}
    assert len(dang) == 1 and "Pác Bó" in dang.pop()
    # khong con ID rieng cho Pac Bo (cac chu cai W, Y, O da duoc dang trang Viet Bac dung lai - xem test_l10_c3_trang_viet_bac.py)
    assert not [r for r in rows.values() if r.get("boi_canh") == "pac_bo"]


def test_plus_code_giai_ma_dung():
    la, lo = _giai_ma_plus_code("8FVC9G8F+6W")        # vi du chuan cua dac ta: 47,365562; 8,524813
    assert abs(la - 47.365562) < 1e-5 and abs(lo - 8.524813) < 1e-5


def test_toa_do_trong_ma_nguon_khop_toa_do_that():
    for k, p in THAT.items():
        q = M._PB_TOA_DO[k]
        assert _hv(p, q) < 1.0, (k, p, q)


def test_dan_ngan_gon_khong_tho_khong_doan_hang_coc_bo():
    d = M._pb_dan()
    for must in ("28/1/1941", "Km $0$", "675", "$108$", "mở ra thời kỳ mới của cách mạng Việt Nam"):
        assert must in d, must
    for khong in ("Tức cảnh Pác Bó", "textit", "begin{center}", "Việt Minh", "Cốc Bó bên", "Hội nghị", "thất ngôn"):
        assert khong not in d, khong


def test_hinh_chi_ghi_ten_diem_A_B_C_D():
    random.seed(1)
    h = M._pb_hinh(M._pb_bo())
    nut = re.findall(r"node\[[a-z ]+\] \{([^}]*)\};\n", h)
    assert sorted(nut) == sorted("$%s$" % c for c in "ABCD")
    assert "(" not in "".join(nut)


def test_duong_cheo_cho_truoc_la_AC_hoac_BD_va_chi_suoi_duoc_dich():
    cheo = set()
    for sd in range(80):
        random.seed(sd)
        c = M._pb_cau()
        cheo.add(c["cheo"])
        assert c["t1"][0] + c["t2"][0] in ("ABCACD", "ABDBCD")
    assert cheo == {"AC", "BD"}
    assert "gần suối Lê-nin" in M._PB_TEN["suoi"][0] and "trên suối" not in M._PB_TEN["suoi"][0]
    for sd in range(40):                                             # toa do khong doi voi lan, hang, moc, Km 0
        random.seed(sd)
        for k in ("lan", "hang", "moc", "km0"):
            assert M._pb_toa_do(k) == M._PB_TOA_DO[k]
        p, q = M._pb_toa_do("suoi"), M._PB_TOA_DO["suoi"]
        assert 0 < _hv(p, q) <= 30.5
