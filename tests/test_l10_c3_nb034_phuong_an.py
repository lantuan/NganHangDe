# -*- coding: utf-8 -*-
r"""L10_C3_B6_NB034_MC_A (co Lan 21/10/2026): "da khac thi khac het, da giong la giong het, hoi mot don vi kien thuc
duy nhat". Bon phuong an hoac thuoc bon ho cong thuc KHAC NHAU (khong co cap dung - sai cua cung mot cong thuc nhu
S = 1/2 a.h_a canh S = a.h_a), hoac cung MOT ho. NB034_MC_B_02 cu (cung hoi cong thuc dien tich dung/sai) da gop vao
MC_A nen mot de khong the co hai cau hoi cung mot dang.

Kiem chung DOC LAP bang so: cong thuc "dung" phai dung tren nhieu tam giac ngau nhien, cong thuc "sai" phai sai.
"""
import importlib.util
import math
import random
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C3_nb034", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_nb034"] = M
_spec.loader.exec_module(M)


def _tam_giac(rng):
    while True:
        a, b, c = (rng.uniform(2, 12) for _ in range(3))
        if a + b > c + 0.5 and b + c > a + 0.5 and c + a > b + 0.5:
            break
    A = math.acos((b * b + c * c - a * a) / (2 * b * c))
    B = math.acos((c * c + a * a - b * b) / (2 * c * a))
    C = math.pi - A - B
    p = (a + b + c) / 2
    S = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return dict(a=a, b=b, c=c, A=A, B=B, C=C, p=p, S=S, R=a * b * c / (4 * S), r=S / p,
                ha=2 * S / a, hb=2 * S / b, hc=2 * S / c)


def _dung(f, T):
    u, v = f(T)
    return math.isclose(u, v, rel_tol=1e-9)


@pytest.mark.parametrize("ho", list(M._C3_HO_CT))
def test_cong_thuc_dung_sai_kiem_bang_so(ho):
    rng = random.Random(7)
    tg = [_tam_giac(rng) for _ in range(40)]
    for tex, f in M._C3_HO_CT[ho]["dung"]:
        assert all(_dung(f, T) for T in tg), tex
    for tex, f in M._C3_HO_CT[ho]["sai"]:
        assert not all(_dung(f, T) for T in tg), tex
    assert len(M._C3_HO_CT[ho]["dung"]) >= 3 and len(M._C3_HO_CT[ho]["sai"]) >= 3


HO_CUA = {tex: (ho, loai) for ho, d in M._C3_HO_CT.items() for loai in ("dung", "sai") for tex, _f in d[loai]}


def _phuong_an(o):
    khoi = o.split("\\choice", 1)[1].split("\n\n", 1)[0]
    pa = [d[1:-1] for d in khoi.strip().split("\n")]
    assert len(pa) == 4, o
    return [(x.replace("\\True ", ""), x.startswith("\\True ")) for x in pa]


@pytest.mark.parametrize("ham, hoi_dung", [("L10_C3_B6_NB034_MC_A_01", True), ("L10_C3_B6_NB034_MC_A_02", False)])
def test_khac_het_hoac_giong_het(ham, hoi_dung):
    kieu = set()
    for s in range(300):
        random.seed(s)
        o = getattr(M, ham)(1)
        pa = _phuong_an(o)
        assert sum(d for _x, d in pa) == 1
        ho = [HO_CUA[x][0] for x, _d in pa]
        assert len(set(ho)) in (1, 4), (ho, o)          # khác hết hoặc giống hết
        kieu.add(len(set(ho)))
        for x, la_dap in pa:
            dung = HO_CUA[x][1] == "dung"
            assert dung == (la_dap == hoi_dung), (x, o)  # đáp án đúng kiểu hỏi, ba nhiễu ngược lại
        assert len({x for x, _d in pa}) == 4
    assert kieu == {1, 4}


def test_mc_b_chi_con_mot_ham():
    ham = [n for n in dir(M) if n.startswith("L10_C3_B6_NB034_MC_B_")]
    assert ham == ["L10_C3_B6_NB034_MC_B_01"]
