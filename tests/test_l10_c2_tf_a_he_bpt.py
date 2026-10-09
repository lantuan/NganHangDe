"""L10_C2_TF_A_01 / _03 / _04: y d) la HE bat phuong trinh; moi y it nhat 3 dung + 3 sai.

Dung/sai cua y d) duoc kiem lai DOC LAP: doc he bat phuong trinh ngay trong cau (\\heva{...}),
vet can tren luoi so nguyen roi so voi nhan \\True. (cô Lan 09/10/2026)
"""
import importlib.util
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))

_spec = importlib.util.spec_from_file_location("L10_C2_tfa_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_tfa_test"] = M
_spec.loader.exec_module(M)

HAM = ["L10_C2_TF_A_01", "L10_C2_TF_A_03", "L10_C2_TF_A_04"]
_cap = {}


def _fake(debai, ys, *a, **k):
    _cap["debai"], _cap["ys"] = debai, ys
    return ""


@pytest.fixture(autouse=True)
def _chup(monkeypatch):
    monkeypatch.setattr(M, "TF_baitoan_du", _fake)


def test_khong_con_a_02():
    assert not hasattr(M, "L10_C2_TF_A_02")


@pytest.mark.parametrize("ten", HAM)
def test_moi_y_it_nhat_3_dung_3_sai(ten):
    f = getattr(M, ten)
    for _ in range(150):
        f(1)
        assert len(_cap["ys"]) == 4
        for i, y in enumerate(_cap["ys"]):
            d = sum(1 for t, _ in y if "\\True" in t)
            assert d >= 3 and len(y) - d >= 3, (ten, "abcd"[i], d, len(y) - d)


_HE = re.compile(r"\\heva\{& (?P<vt>.+?) (?P<ky>\\le|\\ge|<|>) (?P<c>-?\d+) \\\\& x (?P<ox>\\le|\\ge|<|>) 0 \\\\& y (?P<oy>\\le|\\ge|<|>) 0\}")


def _so_sanh(v, op, w):
    return {"\\le": v <= w, "\\ge": v >= w, "<": v < w, ">": v > w}[op]


def _he_tu_cau(text):
    m = _HE.search(text)
    assert m, text
    vt = m.group("vt").replace(" ", "")
    mm = re.fullmatch(r"(-?\d*)x([+-]\d*)y", vt)
    assert mm, vt
    hx = {"": 1, "-": -1}.get(mm.group(1), None)
    a = hx if hx is not None else int(mm.group(1))
    hy = {"+": 1, "-": -1}.get(mm.group(2), None)
    b = hy if hy is not None else int(mm.group(2))
    return a, b, int(m.group("c")), m.group("ky"), m.group("ox"), m.group("oy")


@pytest.mark.parametrize("ten", HAM)
def test_y_d_dung_sai_tinh_doc_lap(ten):
    f = getattr(M, ten)
    for _ in range(120):
        f(1)
        for text, _ly in _cap["ys"][3]:
            dung = "\\True" in text
            a, b, c, ky, ox, oy = _he_tu_cau(text)

            def thuoc(X, Y):
                return _so_sanh(a * X + b * Y, ky, c) and _so_sanh(X, ox, 0) and _so_sanh(Y, oy, 0)

            def dem(R):
                return sum(1 for X in range(-R, R + 1) for Y in range(-R, R + 1) if thuoc(X, Y))

            n20, n40 = dem(20), dem(40)
            vo_han = n40 > n20                              # miền không bị chặn
            pred = text.split("$ ", 1)[1].rstrip("}") if "$ " in text else text
            if "nhận cặp số" in pred:
                X, Y = map(int, re.search(r"\\left\((-?\d+); (-?\d+)\\right\)", pred).groups())
                truth = thuoc(X, Y) if not pred.startswith("không") else not thuoc(X, Y)
            elif "góc phần tư" in pred:
                goc = pred.split("thứ ")[1].strip()
                dau = {"I": (1, 1), "II": (-1, 1), "III": (-1, -1), "IV": (1, -1)}[goc]
                pts = [(X, Y) for X in range(-12, 13) for Y in range(-12, 13) if thuoc(X, Y)]
                truth = all(X * dau[0] >= 0 and Y * dau[1] >= 0 for X, Y in pts)
            elif "tam giác" in pred or "tứ giác" in pred or "bị chặn" in pred:
                if "không bị chặn" in pred:
                    truth = vo_han
                elif "tứ giác" in pred:
                    truth = False
                else:
                    truth = not vo_han
            elif "diện tích" in pred:
                s_txt = re.search(r"bằng \$(.+?)\$", pred).group(1)
                mm = re.fullmatch(r"\\dfrac\{(\d+)\}\{(\d+)\}", s_txt)
                val = Fraction(int(mm.group(1)), int(mm.group(2))) if mm else Fraction(int(s_txt))
                truth = (not vo_han) and val == Fraction(abs(c * c), 2 * abs(a * b))
            elif "vô số nghiệm nguyên" in pred:
                truth = vo_han
            elif "không có nghiệm nguyên nào" in pred:
                truth = n40 == 0
            elif "nghiệm nguyên" in pred:
                N = int(re.search(r"đúng \$(\d+)\$", pred).group(1))
                truth = (not vo_han) and n40 == N
            elif "vô số nghiệm" in pred:
                truth = n40 > 0
            elif "vô nghiệm" in pred:
                truth = n40 == 0
            elif "đúng một nghiệm" in pred:
                truth = False                                # miền 2 chiều nên không thể có đúng 1 nghiệm
            else:
                raise AssertionError("khong nhan ra phat bieu: " + pred)
            assert truth == dung, (ten, text)


def test_a03_y_a_b_c_dung_sai_tinh_doc_lap():
    """A_03: doc p, q, chua O, ke bo ngay trong cau dan, tu tinh lai moi phat bieu cua y a), b), c)."""
    for _ in range(150):
        M.L10_C2_TF_A_03(1)
        db = _cap["debai"]
        p, q = map(int, re.search(r"A\\left\((-?\d+); 0\\right\).*?B\\left\(0; (-?\d+)\\right\)", db).groups())
        chua_O = "nửa mặt phẳng chứa" in db
        ke = "kể cả bờ" in db
        f = lambda X, Y: q * X + p * Y - p * q
        sO = -p * q                                             # f(O)

        def trong_mien(X, Y):
            v = f(X, Y)
            if v == 0:
                return ke
            return (v * sO > 0) == chua_O

        for text, _ly in _cap["ys"][0]:
            dung = "\\True" in text
            if "ngặt" in text:
                truth = (not ke) if "không ngặt" not in text else ke
            else:
                X, Y = map(int, re.search(r"\\left\((-?\d+); (-?\d+)\\right\)", text).groups())
                truth = trong_mien(X, Y) if "không thuộc" not in text else not trong_mien(X, Y)
            assert truth == dung, text
        for text, _ly in _cap["ys"][1]:
            dung = "\\True" in text
            if "phương trình $" in text and "dfrac" in text:
                truth = True
            elif "phương trình" in text:
                mm = re.search(r"phương trình \$(.+?) = (-?\d+)\$", text)
                vt = mm.group(1).replace(" ", "")
                m2 = re.fullmatch(r"(-?\d*)x([+-]\d*)y", vt)
                al = {"": 1, "-": -1}.get(m2.group(1), None); al = al if al is not None else int(m2.group(1))
                be = {"+": 1, "-": -1}.get(m2.group(2), None); be = be if be is not None else int(m2.group(2))
                ga = int(mm.group(2))
                truth = all(al * X + be * Y == ga for X, Y in ((p, 0), (0, q)))
            else:
                X, Y = map(int, re.search(r"điểm \$\\left\((-?\d+); (-?\d+)\\right\)\$", text).groups())
                truth = f(X, Y) == 0
            assert truth == dung, text
        for text, _ly in _cap["ys"][2]:
            dung = "\\True" in text
            mm = re.search(r"bất phương trình \$(.+?) (\\le|\\ge|<|>) (-?\d+)\$", text)
            vt = mm.group(1).replace(" ", "")
            m2 = re.fullmatch(r"(-?\d*)x([+-]\d*)y", vt)
            al = {"": 1, "-": -1}.get(m2.group(1), None); al = al if al is not None else int(m2.group(1))
            be = {"+": 1, "-": -1}.get(m2.group(2), None); be = be if be is not None else int(m2.group(2))
            truth = all(_so_sanh(al * X + be * Y, mm.group(2), int(mm.group(3))) == trong_mien(X, Y)
                        for X in range(-12, 13) for Y in range(-12, 13))
            assert truth == dung, text
