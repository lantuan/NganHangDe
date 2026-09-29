# -*- coding: utf-8 -*-
"""Tap hop liet ke: cac phan tu cach nhau boi dau ";" (dau "," la dau
thap phan trong SGK Viet Nam). Cau NB017_MC_A: phuong an la TAP HOP tran
nen cau hoi phai hoi "khong la tap con", khong hoi "khang dinh nao sai".
"""
import pathlib
import random
import re
import sys

import numpy as np

GOC = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from toan10 import L10_C1 as m  # noqa: E402

PHAY = re.compile(r"\\left\\\{\s*-?[\w.]+\s*,\s*-?[\w.]+[^}]*\\right\\\}")


def _sinh(ten, seed):
    random.seed(seed)
    np.random.seed(seed)
    return getattr(m, ten)(2, 1)


def test_nb017_mc_a_hoi_dung_y():
    for sd in range(100):
        out = _sinh("L10_C1_B2_NB017_MC_A_01", sd)
        assert "khẳng định" not in out and "không đúng?" not in out
        assert "tập con của" in out


def test_tap_hop_dung_dau_cham_phay():
    for ten in ["L10_C1_B2_NB017_MC_A_01", "L10_C1_B2_NB017_MC_D_01",
                "L10_C1_B2_TH018_MC_B_01"]:
        for sd in range(100):
            assert not PHAY.search(_sinh(ten, sd)), ten
