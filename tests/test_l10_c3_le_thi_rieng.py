"""Cong vien Le Thi Rieng: kiem lai DOC LAP.

13/10/2026: hai bien the _02 (cong vien, dap so ha) va _03 (khu vuc ranh mo) cua CUNG dang voi Cong Troi o cac ID
MC_J / SA_J / TL_I, ve TikZ. 21/10/2026: cau tren ANH CHUP ban do that (luc giac MNPQRS khu vuc tim kiem mo rong, Heron
bon lan). 22/10/2026 co Lan: "TL_I ... van chi co anh ve TikZ", roi "MC_J van khong ra duoc map cua Le Thi Rieng" ->
bien the Le Thi Rieng cua CA BA ID (TL_I_02, MC_J_02, SA_J_02) la cau tren anh that; bo cac bien the ve TikZ (_03).

Moi cau: doc 9 so do trong de, tu tinh lai dien tich bang Heron (viet rieng, khong goi ham sinh), so voi dap so; tong
sat 5 800 m^2 (lech <= 2,5%); de KHONG lo con so 5 800; MC 4 phuong an khac nhau, dung 1; SA <= 4 ky tu.
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

CANH = ["MN", "NP", "PQ", "QR", "RS", "SM"]


def _heron(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def _de(txt):
    return txt.split("\\loigiai")[0]


def _tinh_lai(txt):
    """(tong dien tich, [4 dien tich tam giac]) tinh lai tu 9 so do trong de: quat tam giac tu dinh chung cua 3 cheo."""
    de = _de(txt)
    do = {t: int(v) for t, v in re.findall(r"\$([MNPQRS]{2}) = (\d+)\$ m", de)}
    assert len(do) == 9 and all(c in do for c in CANH), de
    cheo = [t for t in do if t not in CANH]
    dinh = {cheo[0][0]} & {cheo[1][0]} & {cheo[2][0]}
    assert len(dinh) == 1
    A = dinh.pop()
    vong = "MNPQRS"
    i = vong.index(A)
    thu = [vong[(i + j) % 6] for j in range(6)]
    dl = lambda u, v: do.get(u + v, do.get(v + u))
    S = [_heron(dl(A, thu[j]), dl(thu[j], thu[j + 1]), dl(thu[j + 1], A)) for j in range(1, 5)]
    return sum(S), S


def _chung(txt):
    de = _de(txt)
    assert r"\includegraphics[width=14cm]{ltr_ban_do.jpg}" in de and "- Diện tích: ?" in de
    assert "5.800" not in de and "5\\,800" not in de                        # de khong lo dap so tren ban do
    tong, S = _tinh_lai(txt)
    assert abs(tong - 5800) <= 0.025 * 5800
    return tong, S


def test_ba_id_deu_chi_con_bien_the_anh_that():
    for id_ in ("MC_J", "SA_J", "TL_I"):
        ten = sorted(n for n in dir(M) if n.startswith("L10_C3_B6_VD036_%s_" % id_))
        assert ten == ["L10_C3_B6_VD036_%s_%s" % (id_, b) for b in ("01", "02", "04")], ten
    assert not [n for n in dir(M) if n.startswith("L10_C3_B6_VD036_TL_P")]
    for f in (M.L10_C3_B6_VD036_MC_J_01, M.L10_C3_B6_VD036_MC_J_04, M.L10_C3_B6_VD036_SA_J_01,
              M.L10_C3_B6_VD036_TL_I_01, M.L10_C3_B6_VD036_TL_I_04):
        random.seed(0)
        assert "Lê Thị Riêng" not in f(1)


def test_mc_anh_that_dung_va_bon_phuong_an_khac_nhau():
    for sd in range(150):
        random.seed(sd)
        txt = M.L10_C3_B6_VD036_MC_J_02(1)
        tong, _S = _chung(txt)
        ds = re.findall(r"\{\s*(\\True\s*)?\$\s*([^$]*?)\s*\$\}", txt.split("\\choice", 1)[1].split("\\loigiai")[0])
        assert len(ds) == 4 and len({x[1] for x in ds}) == 4, (sd, ds)
        dung = [x[1] for x in ds if x[0]]
        assert len(dung) == 1 and int(dung[0]) == round(tong), (dung, tong)
        assert "làm tròn đến hàng đơn vị) là" in _de(txt)


def test_sa_anh_that_khop_doc_lap():
    for sd in range(150):
        random.seed(sd)
        txt = M.L10_C3_B6_VD036_SA_J_02(1)
        tong, _S = _chung(txt)
        dap = re.search(r"\\shortans\{\s*\$([^$]*)\$\}", txt).group(1).strip()
        assert len(dap) <= 4 and int(dap) == round(tong), (dap, tong)
        assert "\\choice" not in txt


def test_tl_anh_that_hai_y():
    for sd in range(60):
        random.seed(sd)
        txt = M.L10_C3_B6_VD036_TL_I_02(1)
        tong, S = _chung(txt)
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", txt)
        assert len(ys) == 2
        assert int(re.search(r"approx (\d+)", ys[1]).group(1)) == round(tong)
        assert min(abs(int(re.search(r"approx (\d+)", ys[0]).group(1)) - s) for s in S) <= 0.5


def test_loi_giai_cong_bon_tam_giac_ra_dung_dap_so():
    for f in (M.L10_C3_B6_VD036_MC_J_02, M.L10_C3_B6_VD036_SA_J_02):
        for sd in range(40):
            random.seed(sd)
            g = f(1).split("\\loigiai", 1)[1]
            m = re.search(r"\\approx (\d+) \+ (\d+) \+ (\d+) \+ (\d+) = (\d+)", g)
            assert m and sum(map(int, m.groups()[:4])) == int(m.group(5)), g


def test_mapping_cung_dang():
    rows = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C3.json", encoding="utf-8"))}
    ids = ["L10_C3_B6_VD036_MC_J", "L10_C3_B6_VD036_SA_J", "L10_C3_B6_VD036_TL_I"]
    dang = {rows[i]["Dang"] for i in ids}
    assert len(dang) == 1 and "Lê Thị Riêng" in dang.pop()
    assert all(rows[i]["boi_canh"] == "cong_troi" for i in ids)
    assert not any("le_thi_rieng" in i.lower() for i in rows) and "L10_C3_B6_VD036_TL_P" not in rows


def test_dan_co_nguon_va_khong_loi_thoai():
    random.seed(0)
    de = _de(M.L10_C3_B6_VD036_SA_J_02(1))
    for must in ("Tết Mậu Thân", "$731$", "$11/10/2026$", "$14/10/2026$", "giả định", "ông cha"):
        assert must in de, must


def test_trang_lam_bai_hien_anh_khong_in_ma_tikz():
    """MC/SA anh that: hinh nam NGAY TRONG de bai (giua phan dan va cau hoi) -> web lay ra thanh anh rieng, chu de bai
    khong con ma TikZ (de_bai_cho_web); gia su cung khong nhan ma TikZ."""
    from app.services.answer_parser_service import de_bai_cho_web, trich_de_bai
    for f in (M.L10_C3_B6_VD036_MC_J_02, M.L10_C3_B6_VD036_SA_J_02):
        random.seed(5)
        d = trich_de_bai(f(1))
        assert d["co_hinh_ve"] and len(d["hinh_tikz"]) == 1 and "ltr_ban_do.jpg" in d["hinh_tikz"][0]
        web = de_bai_cho_web(d["de_bai"])
        assert "tikzpicture" not in web and "\\begin{center}" not in web and "includegraphics" not in web
        assert "Lê Thị Riêng" in web and "MNPQRS" in web
