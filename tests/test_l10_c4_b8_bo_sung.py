# -*- coding: utf-8 -*-
r"""Bai 8 lop 10 bo sung 16/10/2026 theo cau mau co Lan gui (co Lan duyet ke hoach ID):
TH040_MC_A_02, TH041_MC_A_02, TH040_MC_B_02 (khang dinh nao dung), TH040_MC_C/SA_C, TH041_MC_C/SA_C (do dai vecto
tong/hieu trong hinh), B11_VD060_MC_A_02/SA_A_02 (hop luc, goc bat ki).

Kiem chung DOC LAP: doc tung phuong an / bieu thuc trong de bang tests/_tinh_tex.py roi tinh lai bang toa do tu dung
(diem ngau nhien, hinh dat o vi tri xoay + tinh tien ngau nhien, luc dat tren truc), khong dung ham cua file sinh de.
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

_spec = importlib.util.spec_from_file_location("L10_C4_b8_bo_sung", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_b8_bo_sung"] = M
_spec.loader.exec_module(M)


def _bat(ten, seed):
    cap = []
    g1, g2 = M.MC_SA_answer_text, M.MC_SA_answer_const
    ghi = lambda de, dap, nhieu, giai, *a, **k: cap.append((de, str(dap), list(nhieu), giai)) or ""
    M.MC_SA_answer_text = M.MC_SA_answer_const = ghi
    try:
        random.seed(seed)
        getattr(M, ten)(1)
    finally:
        M.MC_SA_answer_text, M.MC_SA_answer_const = g1, g2
    assert len(cap) == 1
    return cap[0]


def _dung(kd, P):
    """Khẳng định '$L = R$' (vectơ theo điểm) đúng với toạ độ P?"""
    l, r = kd.strip("$").split(" = ")
    return bang(tinh(l, P=P), tinh(r, P=P))


# ---------------------------------------------------------------- A_02: ba diem phan biet bat ki
@pytest.mark.parametrize("ten, phep", [("L10_C4_B8_TH040_MC_A_02", "+"), ("L10_C4_B8_TH041_MC_A_02", "-")])
def test_a02_dung_mot_phuong_an(ten, phep):
    for s in range(200):
        de, dap, nhieu, giai = _bat(ten, s)
        diem = re.findall(r"\$([A-Z])\$", de.split("Khẳng định")[0])
        assert len(diem) == 3 and "luôn đúng" in de
        for _ in range(3):
            P = {t: V(random.uniform(-9, 9), random.uniform(-9, 9)) for t in diem}
            assert _dung(dap, P), (de, dap)
            assert not any(_dung(x, P) for x in nhieu), (de, nhieu)
        assert len(set([dap] + nhieu)) == 4
        assert (" + " in dap.split(" = ")[1]) == (phep == "+")
        if phep == "-":                                    # quy tac tru: hai vecto chung diem dau
            u, w = re.findall(r"\\overrightarrow\{([A-Z])([A-Z])\}", dap.split(" = ")[1])
            assert u[0] == w[0]


def test_b02_hinh_binh_hanh():
    for s in range(200):
        de, dap, nhieu, giai = _bat("L10_C4_B8_TH040_MC_B_02", s)
        A, B, C, D = re.search(r"Cho hình bình hành \$([A-Z]{4})\$", de).group(1)
        for _ in range(3):
            P = {A: V(random.uniform(-9, 9), random.uniform(-9, 9)), B: V(random.uniform(-9, 9), random.uniform(-9, 9)),
                 D: V(random.uniform(-9, 9), random.uniform(-9, 9))}
            P[C] = P[B] + P[D] - P[A]
            assert _dung(dap, P) and not any(_dung(x, P) for x in nhieu), (de, dap, nhieu)
        # cac phuong an cung ve phai (nhu cau mau)
        assert len({x.split(" = ")[1] for x in [dap] + nhieu}) == 1


# ---------------------------------------------------------------- C: do dai vecto tong / hieu
def _xoay(P):
    g = random.uniform(0, 2 * math.pi)
    tx, ty = random.uniform(-5, 5), random.uniform(-5, 5)
    return {k: V(x * math.cos(g) - y * math.sin(g) + tx, x * math.sin(g) + y * math.cos(g) + ty) for k, (x, y) in P.items()}


def _hinh_tu_de(de, a):
    """Dung toa do cua hinh tu chinh van ban de bai (a: gia tri thay cho chu a)."""
    sv = lambda t: tinh(t, a=a)
    m = re.search(r"Cho hình vuông \$(\w)(\w)(\w)(\w)\$ cạnh \$([^$]+)\$", de)
    if m:
        A, B, C, D, c = m.groups()
        c = sv(c)
        P = {A: (0, 0), B: (c, 0), C: (c, c), D: (0, c)}
    m2 = re.search(r"Cho hình chữ nhật \$(\w)(\w)(\w)(\w)\$ có \$(\w\w) = ([^$]+)\$, \$(\w\w) = ([^$]+)\$", de)
    if m2:
        A, B, C, D = m2.groups()[:4]
        assert m2.group(5) == A + B and m2.group(7) == A + D
        p, q = sv(m2.group(6)), sv(m2.group(8))
        P = {A: (0, 0), B: (p, 0), C: (p, q), D: (0, q)}
    m3 = re.search(r"Cho hình thoi \$(\w)(\w)(\w)(\w)\$ cạnh \$([^$]+)\$ có \$\\widehat\{(\w)(\w)(\w)\} = 60\^\\circ\$", de)
    if m3:
        A, B, C, D, c = m3.groups()[:5]
        assert m3.group(6) + m3.group(7) + m3.group(8) == B + A + D
        c = sv(c)
        P = {A: (0, 0), B: (c, 0), D: (c * math.cos(math.pi / 3), c * math.sin(math.pi / 3))}
        P[C] = (P[B][0] + P[D][0], P[B][1] + P[D][1])
    if m or m2 or m3:
        o = re.search(r"hai đường chéo cắt nhau tại \$(\w)\$", de)
        if o:
            P[o.group(1)] = ((P[A][0] + P[C][0]) / 2, (P[A][1] + P[C][1]) / 2)
        return P
    m = re.search(r"Cho tam giác đều \$(\w)(\w)(\w)\$ cạnh \$([^$]+)\$", de)
    if m:
        A, B, C, c = m.groups()
        c = sv(c)
        return {A: (0, 0), B: (c, 0), C: (c / 2, c * math.sqrt(3) / 2)}
    m = re.search(r"Cho tam giác \$(\w)(\w)(\w)\$ vuông tại \$(\w)\$ có \$(\w\w) = ([^$]+)\$, \$(\w\w) = ([^$]+)\$", de)
    assert m, de
    A, B, C, vt = m.groups()[:4]
    assert vt == A and m.group(5) == A + B and m.group(7) == A + C
    return {A: (0, 0), B: (sv(m.group(6)), 0), C: (0, sv(m.group(8)))}


def _bieu_thuc(de):
    m = re.search(r"Độ dài của vectơ \$([^$]+)\$ bằng", de) or re.search(r"Tính \$\\left\|(.+?)\\right\|\$", de)
    return m.group(1)


@pytest.mark.parametrize("ten, phep", [("L10_C4_B8_TH040_MC_C_01", "+"), ("L10_C4_B8_TH041_MC_C_01", "-"),
                                       ("L10_C4_B8_TH040_SA_C_01", "+"), ("L10_C4_B8_TH041_SA_C_01", "-")])
def test_c_do_dai_doc_lap(ten, phep):
    thay = set()
    for s in range(150):
        de, dap, nhieu, giai = _bat(ten, s)
        bt = _bieu_thuc(de)
        assert (" %s " % phep) in bt and bt.count(r"\overrightarrow") == 2
        if "_MC_" in ten:
            a = random.uniform(1, 3)                       # MC theo a: dung voi MOI a
            P = _xoay(_hinh_tu_de(de, a))
            d = abs(tinh(bt, P=P))
            assert abs(tinh(dap.strip("$"), a=a) - d) < 1e-7, (de, dap, d)
            assert all(abs(tinh(x.strip("$"), a=a) - d) > 1e-7 for x in nhieu), (de, nhieu)
            assert len(set([dap] + nhieu)) == 4
            u, w = [abs(tinh(t, P=P)) for t in bt.split(" %s " % phep)]
            if abs(u + w - d) > 1e-7:                      # loi hay gap |u| + |v| luon co mat
                assert any(abs(tinh(x.strip("$"), a=a) - (u + w)) < 1e-7 for x in nhieu), (de, nhieu)
        else:
            P = _xoay(_hinh_tu_de(de, 1))
            d = abs(tinh(bt, P=P))
            assert len(dap) <= 4, dap
            if "hàng phần trăm" in de:
                assert abs(so(dap) - d) <= 0.005 + 1e-9 and d < 10, (de, dap, d)
            elif "hàng phần mười" in de:
                assert abs(so(dap) - d) <= 0.05 + 1e-9, (de, dap, d)
            else:
                assert abs(so(dap) - d) < 1e-7 and abs(d - round(d)) < 1e-7, (de, dap, d)
        thay.add(re.match(r"Cho (hình vuông|hình chữ nhật|hình thoi|tam giác đều|tam giác)", de).group(1))
    assert len(thay) == 5


# ---------------------------------------------------------------- VD060_A_02: hop luc
def _luc_tu_de(de):
    m = re.search(r"\\left\|\\overrightarrow\{F_1\}\\right\| = \\left\|\\overrightarrow\{F_2\}\\right\| = (\d+)", de)
    if m:
        p = q = int(m.group(1))
    else:
        p, q = map(int, re.search(r"\\left\|\\overrightarrow\{F_1\}\\right\| = (\d+)\\ \\text\{N\}\$, "
                                  r"\$\\left\|\\overrightarrow\{F_2\}\\right\| = (\d+)", de).groups())
    if "cùng phương, cùng chiều" in de:
        g = 0
    elif "cùng phương, ngược chiều" in de:
        g = 180
    else:
        g = int(re.search(r"bằng \$(\d+)\^\\circ\$", de).group(1))
    F1, F2 = V(p, 0), V(q * math.cos(math.radians(g)), q * math.sin(math.radians(g)))
    return abs(F1 + F2)                                  # can bang: |F3| = |-(F1 + F2)|


@pytest.mark.parametrize("ten", ["L10_C4_B11_VD060_MC_A_02", "L10_C4_B11_VD060_SA_A_02"])
def test_vd060_a02_hop_luc(ten):
    goc, loai = set(), set()
    for s in range(300):
        de, dap, nhieu, giai = _bat(ten, s)
        d = _luc_tu_de(de)
        dap_so = so(dap.replace(r"\ \text{N}", ""))
        if "làm tròn kết quả đến hàng phần mười" in de:
            assert abs(dap_so - d) <= 0.05 + 1e-9 and abs(d - round(d)) > 1e-9, (de, dap, d)
        else:
            assert abs(dap_so - d) < 1e-9, (de, dap, d)
        if "_MC_" in ten:
            assert len(set([dap] + nhieu)) == 4 and dap.endswith(r"\ \text{N}$")
        else:
            assert len(dap) <= 4 and "(đơn vị: N)" in de
        loai.add("ba lực" in de)
        goc.add(re.search(r"bằng \$(\d+)\^\\circ\$|cùng chiều|ngược chiều", de).group(0))
    assert loai == {True, False} and len(goc) >= 8


def test_python_tu_sinh_khong_de_chet():
    for ten, toi_thieu in (("L10_C4_B8_TH040_MC_A_02", 60), ("L10_C4_B8_TH041_MC_A_02", 60),
                           ("L10_C4_B8_TH040_MC_B_02", 30), ("L10_C4_B8_TH040_MC_C_01", 40),
                           ("L10_C4_B8_TH040_SA_C_01", 60), ("L10_C4_B8_TH041_MC_C_01", 40),
                           ("L10_C4_B8_TH041_SA_C_01", 60), ("L10_C4_B11_VD060_MC_A_02", 100),
                           ("L10_C4_B11_VD060_SA_A_02", 100), ("L10_C4_B11_VD060_MC_B_01", 100),
                           ("L10_C4_B11_VD060_SA_B_01", 100), ("L10_C4_B11_VD060_MC_C_01", 100),
                           ("L10_C4_B11_VD060_SA_C_01", 100), ("L10_C4_B8_VD040_MC_A_01", 100), ("L10_C4_B8_VD040_MC_A_02", 100)):
        de = set()
        for s in range(150):
            random.seed(s)
            o = getattr(M, ten)(1)
            assert (r"\choice" in o) == ("_MC_" in ten) and (r"\shortans" in o) == ("_SA_" in ten)
            than = o.split(r"\loigiai")[0].replace(r"\True ", "")
            de.add((than.split(r"\choice")[0], frozenset(than.split("\n"))))   # de + tap phuong an (bo thu tu)
        assert len(de) >= toi_thieu, (ten, len(de))


# ---------------------------------------------------------------- dot 2 (16/10/2026): VD060_B, VD060_C, VD040
_LA_BAN = {"Đông": (1, 0), "Tây": (-1, 0), "Bắc": (0, 1), "Nam": (0, -1)}


def _huong(ten):
    """'Đông Bắc' -> vectơ đơn vị."""
    x = y = 0
    for t in ten.split():
        x, y = x + _LA_BAN[t][0], y + _LA_BAN[t][1]
    n = math.hypot(x, y)
    return x / n, y / n


def _kiem_lam_tron(de, dap, d):
    muc = re.search(r"làm tròn kết quả đến (hàng đơn vị|hàng phần mười|hàng phần trăm)", de)
    if muc:
        sai_so = {"hàng đơn vị": 0.5, "hàng phần mười": 0.05, "hàng phần trăm": 0.005}[muc.group(1)]
        assert abs(so(dap) - d) <= sai_so + 1e-9, (de, dap, d)
        assert abs(d * (0.5 / sai_so) - round(d * (0.5 / sai_so))) > 1e-9, ("khong can lam tron", de, d)
    else:
        assert abs(so(dap) - d) < 1e-9, (de, dap, d)


def _van_toc_tu_de(de):
    m = re.search(r"Vận tốc riêng của ca nô \(so với dòng nước\) có độ lớn \$(\d+)\$ km/h, dòng nước chảy song song với bờ "
                  r"với vận tốc \$(\d+)\$ km/h", de)
    if m:
        p, q = map(int, m.groups())
        nuoc = (q, 0)                                     # dòng nước theo Ox, bờ song song Ox
        if "vuông góc với bờ" in de:
            g = 90
        else:
            g0 = int(re.search(r"một góc \$(\d+)\^\\circ\$", de).group(1))
            g = g0
            assert ("xuôi dòng" in de) == (g0 < 90)
        v1 = (p * math.cos(math.radians(g)), p * math.sin(math.radians(g)))
        v = math.hypot(v1[0] + nuoc[0], v1[1] + nuoc[1])
        t = re.search(r"sau \$(\d+)\$ phút", de)
        return ("thuyen_qua_song", v * int(t.group(1)) / 60 if t else v)
    m = re.search(r"vận tốc riêng \(so với dòng nước\) có độ lớn \$([\d,]+)\$ m/s; dòng nước chảy song song với bờ với vận "
                  r"tốc \$([\d,]+)\$ m/s", de)
    if m:
        p, q = so(m.group(1)), so(m.group(2))
        assert "vuông góc với bờ" in de
        return ("nguoi_boi_qua_song", math.hypot(p, q))
    m = re.search(r"flycam bay theo hướng (\S+) với vận tốc riêng \(so với không khí\) có độ lớn \$(\d+)\$ m/s; gió thổi "
                  r"theo hướng ([^$]+?) với vận tốc \$(\d+)\$ m/s", de)
    assert m, de
    a, b = _huong(m.group(1)), _huong(m.group(3))
    p, q = int(m.group(2)), int(m.group(4))
    return ("flycam_gap_gio", math.hypot(p * a[0] + q * b[0], p * a[1] + q * b[1]))


@pytest.mark.parametrize("ten", ["L10_C4_B11_VD060_MC_B_01", "L10_C4_B11_VD060_SA_B_01"])
def test_vd060_b_van_toc_doc_lap(ten):
    thay = set()
    for s in range(300):
        de, dap, nhieu, giai = _bat(ten, s)
        bc, d = _van_toc_tu_de(de)
        thay.add(bc)
        if "_MC_" in ten:
            gia = lambda x: so(re.search(r"\$([\d,]+)\$", x).group(1))
            _kiem_lam_tron(de, "%s" % gia(dap), d)
            assert len(set([dap] + nhieu)) == 4 and all(abs(gia(x) - gia(dap)) > 1e-9 for x in nhieu)
        else:
            _kiem_lam_tron(de, dap, d)
            assert len(dap) <= 4 and "(đơn vị:" in de
    assert thay == {"thuyen_qua_song", "nguoi_boi_qua_song", "flycam_gap_gio"}


@pytest.mark.parametrize("ten", ["L10_C4_B11_VD060_MC_C_01", "L10_C4_B11_VD060_SA_C_01"])
def test_vd060_c_luc_thuc_te_doc_lap(ten):
    thay, deu = set(), set()
    for s in range(300):
        de, dap, nhieu, giai = _bat(ten, s)
        p, q, g = map(int, re.search(r"độ lớn lần lượt là \$(\d+)\$ k?N và \$(\d+)\$ k?N, góc giữa hai (?:lực|dây cáp) bằng "
                                     r"\$(\d+)\^\\circ\$", de).groups())
        F = V(p, 0) + V(q * math.cos(math.radians(g)), q * math.sin(math.radians(g)))
        d = abs(F)                                        # lực cản (chuyển động đều) cũng bằng |F1 + F2|
        if "_MC_" in ten:
            gia = lambda x: so(re.search(r"\$([\d,]+)\$", x).group(1))
            _kiem_lam_tron(de, "%s" % gia(dap), d)
            assert len(set([dap] + nhieu)) == 4 and all(abs(gia(x) - gia(dap)) > 1e-9 for x in nhieu)
        else:
            _kiem_lam_tron(de, dap, d)
            assert len(dap) <= 4
        thay.add(re.search(r"con thuyền|sà lan|kiện hàng", de).group(0))
        deu.add("chuyển động thẳng đều" in de)
    assert len(thay) == 3 and deu == {True, False}


def _quy_tich(mo_ta, P):
    """Mô tả tập hợp -> hàm sinh một điểm trên tập hợp (tham số t)."""
    m = re.fullmatch(r"đường trung trực của đoạn thẳng \$(\w)(\w)\$", mo_ta)
    if m:
        A, B = P[m.group(1)], P[m.group(2)]
        I, u = (A + B) / 2, B - A
        return lambda t: I + V(-u.y, u.x) * t
    m = re.fullmatch(r"đường tròn tâm \$(\w)\$, bán kính bằng \$(\w)(\w)\$", mo_ta)
    if m:
        O, r = P[m.group(1)], abs(P[m.group(3)] - P[m.group(2)])
        return lambda t: O + V(math.cos(t), math.sin(t)) * r
    m = re.fullmatch(r"đường tròn đường kính \$(\w)(\w)\$", mo_ta)
    if m:
        A, B = P[m.group(1)], P[m.group(2)]
        return lambda t: (A + B) / 2 + V(math.cos(t), math.sin(t)) * (abs(B - A) / 2)
    m = re.fullmatch(r"đường thẳng \$(\w)(\w)\$", mo_ta)
    assert m, mo_ta
    A, B = P[m.group(1)], P[m.group(2)]
    return lambda t: A + (B - A) * t


def _hinh_vd040(de):
    """Toạ độ ngẫu nhiên của hình đọc từ câu dẫn: hình bình hành (tâm O) hoặc tam giác (trọng tâm G, trung điểm I)."""
    r = lambda: V(random.uniform(-5, 5), random.uniform(-5, 5))
    m = re.search(r"Cho hình bình hành \$(\w)(\w)(\w)(\w)\$", de)
    if m:
        A, B, C, D = m.groups()
        P = {A: r(), B: r(), D: r()}
        P[C] = P[B] + P[D] - P[A]
        if "hai đường chéo cắt nhau tại $O$" in de:
            P["O"] = (P[A] + P[C]) / 2
        return P
    A, B, C = re.search(r"Cho tam giác \$(\w)(\w)(\w)\$", de).groups()
    P = {A: r(), B: r(), C: r()}
    if "trọng tâm $G$" in de:
        P["G"] = (P[A] + P[B] + P[C]) / 3
    m = re.search(r"\$I\$ là trung điểm của cạnh \$(\w)(\w)\$", de)
    if m:
        P["I"] = (P[m.group(1)] + P[m.group(2)]) / 2
    return P


@pytest.mark.parametrize("ten, loai", [("L10_C4_B8_VD040_MC_A_01", "đường trung trực của đoạn thẳng "),
                                       ("L10_C4_B8_VD040_MC_A_02", "đường tròn tâm ")])
def test_vd040_tap_hop_diem_doc_lap(ten, loai):
    hinh, diem_phu = set(), set()
    for s in range(300):
        de, dap, nhieu, giai = _bat(ten, s)
        assert dap.startswith(loai), (de, dap)
        P = _hinh_vd040(de)
        trai, phai = re.search(r"thoả mãn \$\\left\|(.+?)\\right\| = \\left\|(.+?)\\right\|\$ là", de).groups()
        dung = set(re.findall(r"\\overrightarrow\{(\w)(\w)\}", trai + phai))
        for t in {x for c in dung for x in c} - {"M"}:
            assert t in P, ("điểm dùng mà câu dẫn không cho", de, t)
        for t in set(P) - {x for c in dung for x in c} - set(re.findall(r"\$(\w)\$", dap)):
            dinh = re.search(r"Cho (?:hình bình hành|tam giác) \$(\w+)\$", de).group(1)
            assert t in dinh, ("câu dẫn có điểm phụ không dùng", de, t)
        dk = lambda Mm: abs(tinh(trai, P=dict(P, M=Mm))) - abs(tinh(phai, P=dict(P, M=Mm)))
        f = _quy_tich(dap, P)
        assert all(abs(dk(f(t))) < 1e-7 for t in (-1.3, 0.2, 0.9, 2.5)), (de, dap)
        for x in nhieu:                                   # mỗi nhiễu có điểm không thoả điều kiện
            g = _quy_tich(x, P)
            assert any(abs(dk(g(t))) > 1e-6 for t in (-1.3, 0.2, 0.9, 2.5)), (de, x)
        assert len(set([dap] + nhieu)) == 4
        hinh.add(de.split("$")[0])
        diem_phu |= set(P) & {"O", "G", "I"}
    assert hinh == {"Cho hình bình hành ", "Cho tam giác "} and diem_phu == {"O", "G", "I"}


def test_vd040_tl_hai_y():
    for s in range(100):
        random.seed(s)
        o = M.L10_C4_B8_VD040_TL_A_01(1)
        assert o.count(r"\item") == 4 and r"\choice" not in o and r"\shortans" not in o


def test_c_co_truong_hop_hai_duong_cheo():
    thay = 0
    for s in range(300):
        de, dap, nhieu, giai = _bat("L10_C4_B8_TH041_SA_C_01", s)
        thay += "hai cạnh đối của hình bình hành" in giai
    assert thay >= 10
