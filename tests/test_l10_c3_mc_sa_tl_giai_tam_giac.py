"""MC / SA / TL 'giai tam giac' chuong 3 (co Lan 10/10/2026): kiem lai DOC LAP bang TOA DO.

Voi MOI ham sinh boi `_ms_sinh` (cac ID duoc them theo bang co Lan duyet):
  1. doc so lieu trong de bai (AB, AC, cos A / hai goc + mot canh / ba canh / duong cao / trung tuyen / phan giac),
     dung lai tam giac tu TOA DO roi tu tinh dai luong duoc hoi (khong dung engine);
  2. MC: dung 4 phuong an khac nhau, dung 1 phuong an {\\True}, phuong an dung khop dai luong, 3 phuong an con lai SAI;
     SA: dap so khop; TL: dung 2 y, moi dap so khop;
  3. NB029 (xet dau / loai goc): phuong an dung la khang dinh DUNG, 3 phuong an con lai la khang dinh SAI;
  4. mapping / curriculum: co dong cho moi ID moi, dang luyen tap them danh dau dung.
"""
import importlib.util
import json
import math
import os
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C3_ms_test", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_ms_test"] = M
_spec.loader.exec_module(M)

_SRC = (GOC / "data" / "python_bank" / "toan10" / "L10_C3.py").read_text(encoding="utf-8")
_PHAN = _SRC[_SRC.index("# ===== MS_BEGIN"):_SRC.index("# ===== MS_END")]
HAM = re.findall(r"^def (L10_C3_\w+_\d\d)\(", _PHAN, flags=re.M)
KIEU = {n: re.search(r'_ms_sinh\("(\w+)", "(\w+)", "(\w)", (\d)', _PHAN[_PHAN.index("def %s(" % n):]).groups() for n in HAM}


# ---------------------------------------------------------------- doc LaTeX -> so
def tex_so(s):
    s = s.strip()
    s = s.replace("^{\\circ}", "").replace("\\approx", "").replace("\\left", "").replace("\\right", "").replace("{,}", ".").replace(",", ".")
    s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"(\d)\s+(sqrt)", r"\1*\2", s)
    while "\\dfrac" in s:
        s = re.sub(r"\\dfrac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"(\d|\))\s*(sqrt|\()", r"\1*\2", s)
    s = s.replace("$", "").strip()
    assert re.fullmatch(r"[0-9sqrt()+\-*/. ]+", s), s
    return float(eval(s, {"sqrt": math.sqrt}))


def so_chu_so_tp(s):
    m = re.search(r"[.,](\d+)", s.replace("^{\\circ}", ""))
    return len(m.group(1)) if m else None


def n_lam_tron(de):
    """So chu so lam tron neu de bai yeu cau ('hang phan muoi' -> 1); None neu khong yeu cau."""
    for n, ten in M._MS_MUC_HANG.items():
        if "làm tròn đến " + ten in de:
            return n
    return None


def khop(chuoi, dich, n_de=None):
    """chuoi (dap an dang LaTeX / so) co khop gia tri dich khong. Thap phan -> dung sai nua don vi lam tron
    (n_de: so chu so lam tron de bai yeu cau; SA bo duoi 0 nen '27' van la 27,0)."""
    v = tex_so(chuoi)
    n = n_de if n_de is not None else so_chu_so_tp(chuoi)
    tol = 1e-7 if n is None else 0.5 * 10 ** (-n) + 1e-9
    return abs(v - dich) <= tol


# ---------------------------------------------------------------- dung tam giac tu de bai
def tg_tu_ba_canh(a, b, c):
    B = (0.0, 0.0)
    C = (float(a), 0.0)
    x = (a * a + c * c - b * b) / (2 * a)
    A = (x, math.sqrt(max(c * c - x * x, 0.0)))
    return dict(A=A, B=B, C=C)


def d(P, Q):
    return math.hypot(P[0] - Q[0], P[1] - Q[1])


def goc(T, X):
    """So do (radian) cua goc tai dinh X."""
    O = T[X]
    P, Q = [T[y] for y in "ABC" if y != X]
    v1, v2 = (P[0] - O[0], P[1] - O[1]), (Q[0] - O[0], Q[1] - O[1])
    return math.acos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2)))))


def dien_tich(P, Q, R):
    return abs((Q[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q[1] - P[1])) / 2


def doc_so(s):
    """So (nguyen / phan so / thap phan) trong de bai: '25' hoac '\\dfrac{25}{2}'."""
    return tex_so(s)


def dung_tg(de):
    """Doc cau dan, dung tam giac tu toa do. Tra ve (T, loai)."""
    de = de.replace("\n", " ")
    m = re.search(r"có \$AB = (\d+)\$, \$AC = (\d+)\$ và (.*?)\.", de)
    if m and ("\\cos A" in m.group(3) or "\\sin A" in m.group(3) or "\\tan A" in m.group(3)):
        c, b, g = float(m.group(1)), float(m.group(2)), m.group(3)
        if "\\cos A" in g:
            cs = tex_so(re.search(r"\\cos A = (.*?)\$", g + "$").group(1))
        elif "\\sin A" in g:
            sn = tex_so(re.search(r"\\sin A = (.*?)\$", g).group(1))
            cs = math.sqrt(1 - sn * sn) * (1 if "nhọn" in g else -1)
        else:
            tg = tex_so(re.search(r"\\tan A = (.*?)\$", g + "$").group(1))
            cs = (1 if tg > 0 else -1) / math.sqrt(1 + tg * tg)
        sn = math.sqrt(1 - cs * cs)
        A, B, C = (0.0, 0.0), (c, 0.0), (b * cs, b * sn)
        return dict(A=A, B=B, C=C), "A"
    ang = re.findall(r"\\widehat\{([ABC])\} = (\d+)\^\{\\circ\}", de)
    if len(ang) == 2:
        goc_d = {x: float(v) for x, v in ang}
        x3 = [x for x in "ABC" if x not in goc_d][0]
        goc_d[x3] = 180 - sum(goc_d.values())
        cd = re.search(r"và \$(BC|CA|AB)\$? ?= (\d+)", de) or re.search(r"\$(BC|CA|AB) = (\d+)\$", de)
        ten, val = cd.group(1), float(cd.group(2))
        doi = {"BC": "A", "CA": "B", "AB": "C"}[ten]
        k = val / math.sin(math.radians(goc_d[doi]))
        s = {x: k * math.sin(math.radians(goc_d[x])) for x in "ABC"}  # canh doi dien dinh x
        return tg_tu_ba_canh(s["A"], s["B"], s["C"]), "B"
    m = re.search(r"\$BC = (\d+)\$, \$\\cos B = (.*?)\$ và đường cao \$AH = (.*?)\$", de)
    if m:
        a, cb, h = float(m.group(1)), tex_so(m.group(2)), tex_so(m.group(3))
        sb = math.sqrt(1 - cb * cb)
        c = h / sb
        return dict(A=(c * cb, c * sb), B=(0.0, 0.0), C=(a, 0.0)), "D"
    m = re.search(r"\$AB = (\d+)\$, \$\\cos B = (.*?)\$ và đường cao \$CK = (.*?)\$", de)
    if m:
        c, cb, h = float(m.group(1)), tex_so(m.group(2)), tex_so(m.group(3))
        sb = math.sqrt(1 - cb * cb)
        a = h / sb
        return dict(A=(c * cb, c * sb), B=(0.0, 0.0), C=(a, 0.0)), "D"
    m = re.search(r"\$BC = (\d+)\$, \$(AB|AC) = (\d+)\$ và đường trung tuyến \$AM = (.*?)\$ \(", de)
    if m:
        a, ten, x, mm = float(m.group(1)), m.group(2), float(m.group(3)), tex_so(m.group(4))
        if ten == "AB":
            px = (x * x - mm * mm + a * a / 4) / a
        else:
            px = (mm * mm - x * x + 3 * a * a / 4) / a
        py = math.sqrt(mm * mm - (px - a / 2) ** 2)
        return dict(A=(px, py), B=(0.0, 0.0), C=(a, 0.0)), "E"
    m = re.search(r"\$BC = (\d+)\$, \$CA = (\d+)\$, \$AB = (\d+)\$", de)
    if m:
        T = tg_tu_ba_canh(*[float(m.group(i)) for i in (1, 2, 3)])
        return T, ("F" if "phân giác" in de else "C")
    raise AssertionError("khong doc duoc de: " + de)


def chan_phan_giac(T):
    b, c = d(T["A"], T["C"]), d(T["A"], T["B"])
    t = c / (b + c)
    return (T["B"][0] + (T["C"][0] - T["B"][0]) * t, T["B"][1] + (T["C"][1] - T["B"][1]) * t)


def muc_tieu(hoi, T):
    """Tinh dai luong duoc hoi tu toa do. Tra ve gia tri (do voi goc)."""
    a, b, c = d(T["B"], T["C"]), d(T["A"], T["C"]), d(T["A"], T["B"])
    S = dien_tich(T["A"], T["B"], T["C"])
    ten_c = {"BC": a, "CA": b, "AC": b, "AB": c}
    gs = {x: goc(T, x) for x in "ABC"}
    D = chan_phan_giac(T)
    m = re.search(r"\\(sin|cos)\\left\(B \+ C\\right\)", hoi)
    if m:
        return (math.sin if m.group(1) == "sin" else math.cos)(gs["B"] + gs["C"])
    m = re.search(r"\\(sin|cos)\\left\(180\^\{\\circ\} - A\\right\)", hoi)
    if m:
        return (math.sin if m.group(1) == "sin" else math.cos)(math.pi - gs["A"])
    m = re.search(r"\\(sin|cos)\\left\(\\widehat\{([ABC])\} \+ \\widehat\{([ABC])\}\\right\)", hoi)
    if m:
        return (math.sin if m.group(1) == "sin" else math.cos)(gs[m.group(2)] + gs[m.group(3)])
    m = re.search(r"Tính \$\\(cos|sin|tan)\\widehat\{([ABC])\}\$", hoi)
    if m:
        return {"cos": math.cos, "sin": math.sin, "tan": math.tan}[m.group(1)](gs[m.group(2)])
    m = re.search(r"Tính \$\\(cos|sin|tan) ([ABC])\$", hoi)
    if m:
        return {"cos": math.cos, "sin": math.sin, "tan": math.tan}[m.group(1)](gs[m.group(2)])
    m = re.search(r"Tính số đo góc \$\\widehat\{([ABC])\}\$", hoi)
    if m:
        return math.degrees(gs[m.group(1)])
    m = re.search(r"độ dài cạnh \$(BC|CA|AC|AB)\$", hoi)
    if m:
        return ten_c[m.group(1)]
    m = re.search(r"diện tích tam giác \$(ABD|ACD)\$", hoi)
    if m:
        return dien_tich(T["A"], T["B"], D) if m.group(1) == "ABD" else dien_tich(T["A"], D, T["C"])
    if "diện tích $S$" in hoi:
        return S
    if "bán kính $R$" in hoi:
        return a * b * c / (4 * S)
    if "bán kính $r$" in hoi:
        return S / ((a + b + c) / 2)
    if "nửa chu vi" in hoi:
        return (a + b + c) / 2
    if "chu vi của tam giác" in hoi:
        return a + b + c
    m = re.search(r"đường cao \$h_([abc])\$", hoi)
    if m:
        return 2 * S / {"a": a, "b": b, "c": c}[m.group(1)]
    m = re.search(r"đường cao kẻ từ đỉnh \$([ABC])\$ của tam giác", hoi)
    if m:
        return 2 * S / {"A": a, "B": b, "C": c}[m.group(1)]
    if "đường phân giác $AD$" in hoi:
        # kiem tra AD thuc su la phan giac: hai goc BAD, DAC bang nhau
        v1 = (T["B"][0] - T["A"][0], T["B"][1] - T["A"][1]); v2 = (D[0] - T["A"][0], D[1] - T["A"][1]); v3 = (T["C"][0] - T["A"][0], T["C"][1] - T["A"][1])
        c1 = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))
        c2 = (v3[0] * v2[0] + v3[1] * v2[1]) / (math.hypot(*v3) * math.hypot(*v2))
        assert abs(c1 - c2) < 1e-9
        return d(T["A"], D)
    m = re.search(r"độ dài đoạn \$(BD|DC)\$", hoi)
    if m:
        return d(T["B"], D) if m.group(1) == "BD" else d(D, T["C"])
    raise AssertionError("khong hieu cau hoi: " + hoi)


# ---------------------------------------------------------------- tach ma LaTeX
def cac_cau(out):
    kq = re.findall(r"\\begin\{ex\}%%\[\?\]\n(.*?)\\end\{ex\}", out, flags=re.S)
    assert kq
    return kq


def lay_nhom(s, i):
    """s[i] == '{': tra ve (noi dung, vi tri sau dau '}' tuong ung)."""
    dem = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            dem += 1
        elif s[j] == "}":
            dem -= 1
            if dem == 0:
                return s[i + 1:j], j + 1
    raise AssertionError


def lay_phuong_an(khoi):
    i = khoi.index("\\choice") + len("\\choice")
    ds = []
    while i < len(khoi):
        while i < len(khoi) and khoi[i] in " \n":
            i += 1
        if i >= len(khoi) or khoi[i] != "{":
            break
        nd, i = lay_nhom(khoi, i)
        ds.append(nd)
    return ds


def lay_de(khoi):
    return khoi.split("\\choice")[0].split("\\shortans")[0].split("\\begin{listEX}")[0].split("\\loigiai")[0].strip()


SO_HAT = int(os.environ.get("MS_SEEDS", 3))  # chay kiem sau: MS_SEEDS=60 pytest ...
HAM_MC = [n for n in HAM if KIEU[n][0] == "MC" and KIEU[n][1] != "NB029"]
HAM_SA = [n for n in HAM if KIEU[n][0] == "SA"]
HAM_TL = [n for n in HAM if KIEU[n][0] == "TL"]
HAM_NB = [n for n in HAM if KIEU[n][1] == "NB029"]


def test_co_du_ham():
    assert len(HAM) == 177
    assert len(set(HAM)) == 177


@pytest.mark.parametrize("ten", HAM_MC)
def test_mc(ten):
    f = getattr(M, ten)
    for seed in range(SO_HAT):
        random.seed(seed)
        out = f(4)
        cac = cac_cau(out)
        assert len(cac) == 4
        de_da = set()
        for k in cac:
            pa = lay_phuong_an(k)
            assert len(pa) == 4, k
            assert len(set(pa)) == 4, pa
            assert sum("\\True" in x for x in pa) == 1
            de = lay_de(k)
            de_da.add(de)
            T, _ = dung_tg(de)
            dich = muc_tieu(de, T)
            dung = [x.replace("\\True", "") for x in pa if "\\True" in x][0]
            assert khop(dung, dich), (ten, de, dung, dich)
            for x in pa:
                if "\\True" not in x:
                    n = so_chu_so_tp(x)
                    tol = 1e-7 if n is None else 0.5 * 10 ** (-n) + 1e-9
                    assert abs(tex_so(x) - dich) > tol, (ten, de, x, dich)
        assert len(de_da) == 4  # bon cau khac nhau


@pytest.mark.parametrize("ten", HAM_SA)
def test_sa(ten):
    f = getattr(M, ten)
    for seed in range(SO_HAT):
        random.seed(seed)
        out = f(4)
        cac = cac_cau(out)
        assert len(cac) == 4
        de_da = set()
        for k in cac:
            assert "\\choice" not in k
            m = re.search(r"\\shortans\{ ?(.*?)\}\n", k)
            assert m, k
            de = lay_de(k)
            de_da.add(de)
            T, _ = dung_tg(de)
            dich = muc_tieu(de, T)
            dap = m.group(1)
            n_dap = so_chu_so_tp(dap)
            n_de = n_lam_tron(de)
            if n_dap is not None and n_de is None:  # khong yeu cau lam tron -> dap so phai la thap phan huu han DUNG (vd 7/25 = 0,28)
                assert abs(tex_so(dap) - dich) < 1e-7, (ten, de, dap, dich)
            else:
                assert n_dap is None or n_dap <= n_de, (de, dap)
                assert khop(dap, dich, n_de), (ten, de, dap, dich)
        assert len(de_da) == 4


@pytest.mark.parametrize("ten", HAM_TL)
def test_tl(ten):
    f = getattr(M, ten)
    for seed in range(SO_HAT):
        random.seed(seed)
        out = f(3)
        cac = cac_cau(out)
        assert len(cac) == 3
        for k in cac:
            de = lay_de(k)
            T, _ = dung_tg(de)
            ds = re.findall(r"\\item (.*?) \\SA\[4\]\{\$(.*?)\$\}", k)
            assert len(ds) == 2, k
            assert k.count("\\item") == 4  # 2 y de + 2 y loi giai
            assert ds[0][0] != ds[1][0]
            for hoi, dap in ds:
                dich = muc_tieu(hoi, T)
                assert khop(dap, dich), (ten, de, hoi, dap, dich)


def _menh_de_dung(ms, T):
    gs = {x: goc(T, x) for x in "ABC"}
    ms = ms.replace("\\True", "").strip()
    m = re.fullmatch(r"\$\\(cos|sin|tan) A (>|<|=) 0\$", ms)
    if m:
        v = {"cos": math.cos, "sin": math.sin, "tan": math.tan}[m.group(1)](gs["A"])
        return {">": v > 1e-9, "<": v < -1e-9, "=": abs(v) < 1e-9}[m.group(2)]
    m = re.fullmatch(r"Góc \$\\widehat\{A\}\$ là góc (nhọn|tù|vuông)", ms)
    if m:
        g = math.degrees(gs["A"])
        return {"nhọn": g < 90 - 1e-9, "tù": g > 90 + 1e-9, "vuông": abs(g - 90) < 1e-9}[m.group(1)]
    raise AssertionError(ms)


@pytest.mark.parametrize("ten", HAM_NB)
def test_nb029(ten):
    f = getattr(M, ten)
    for seed in range(6):
        random.seed(seed)
        for k in cac_cau(f(3)):
            pa = lay_phuong_an(k)
            assert len(set(pa)) == 4 and sum("\\True" in x for x in pa) == 1
            T, _ = dung_tg(lay_de(k))
            for x in pa:
                assert _menh_de_dung(x, T) == ("\\True" in x), (lay_de(k), x)


# ---------------------------------------------------------------- mapping / curriculum
def _mapping():
    return {r["id"]: r for r in json.loads((GOC / "data" / "mapping" / "toan10" / "L10_C3.json").read_text(encoding="utf-8"))}


def test_mapping_moi_co_dong_va_co_ham():
    mp = _mapping()
    moi = [i for i, r in mp.items() if "[MSTL_C3]" in r.get("ghi_chu", "")]
    assert len(moi) == 60
    ham_goc = {n[:-3] for n in HAM}
    for i in moi:
        assert any(h == i for h in ham_goc), i
        assert mp[i]["Loai"] in ("Trắc nghiệm nhiều lựa chọn", "Trả lời ngắn", "Tự luận")
    # ham thuoc ID cu (mo rong TH035) thi ID phai co san trong mapping
    for h in ham_goc:
        assert h in mp, h


def test_luyen_tap_them_dung_co():
    mp = _mapping()
    for i, r in mp.items():
        if "[MSTL_C3]" not in r.get("ghi_chu", ""):
            continue
        dv = i.split("_")[3]
        ltt = r.get("ngoai_yccd") is True
        co_ghi = r["ghi_chu"].startswith("LUYEN TAP THEM")
        assert ltt == co_ghi, i
    # E, F cua TH032 va VD032 la luyen tap them; VD032 E, F con la VDC
    cuoi = {"E", "F"}
    for i, r in mp.items():
        if "[MSTL_C3]" not in r.get("ghi_chu", ""):
            continue
        if "Dang" in r and ("luyện tập thêm" in r["Dang"]):
            assert r.get("ngoai_yccd") is True, i
            if "_VD032_" in i:
                assert r.get("muc_do_dang") == "VDC", i
        elif "_VD032_" in i:
            assert "muc_do_dang" not in r, i


def test_curriculum_co_nhom_luyen_tap_them():
    cur = json.loads((GOC / "data" / "curriculum" / "toan10" / "L10_C3.json").read_text(encoding="utf-8"))
    mp = _mapping()
    for e in cur:
        if e["id"] in ("L10_C3_B6_TH032", "L10_C3_B6_VD032"):
            ids = {i for g in e["dang_luyen_tap_them"] for i in g["mapping_id"]}
            for i, r in mp.items():
                if r.get("ngoai_yccd") and i.startswith(e["id"] + "_"):
                    assert i in ids, (e["id"], i)
