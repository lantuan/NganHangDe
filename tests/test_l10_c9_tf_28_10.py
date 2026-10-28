"""Năm câu Đúng/Sai chương 9 lớp 10 viết lại (cô Lan 28/10/2026): bốn ý NB -> TH -> VD -> VDC, mỗi ý >= 3 phát biểu
đúng và >= 3 phát biểu sai, phát biểu không trùng nhau; kiểm ĐỘC LẬP các xác suất bằng cách liệt kê không gian mẫu."""
import random
import re
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
from app.services.generator_service import _load_chapter_module  # noqa: E402

M = _load_chapter_module(10, 9)
TEN = ["L10_C9_TF_A_01", "L10_C9_TF_B_01", "L10_C9_TF_C_01", "L10_C9_TF_D_01", "L10_C9_TF_E_01"]


def _bat(ten, seed):
    bat = []
    goc = M.TF_baitoan_du

    def _tf(debai, ds, *a, **k):
        bat.append((debai, ds))
        return goc(debai, ds, *a, **k)
    M.TF_baitoan_du = _tf
    try:
        random.seed(seed)
        getattr(M, ten)(1, 1)
    finally:
        M.TF_baitoan_du = goc
    return bat[0]


@pytest.mark.parametrize("ten", TEN)
def test_moi_y_ba_dung_ba_sai(ten):
    for s in range(25):
        _, ds = _bat(ten, s)
        assert len(ds) == 4
        for y in ds:
            dung = [p for p, _ in y if p.startswith(r"{\True")]
            sai = [p for p, _ in y if not p.startswith(r"{\True")]
            assert len(dung) >= 3 and len(sai) >= 3 and len({p.replace(r"\True ", "") for p, _ in y}) == len(y)


def _ps(t):
    m = re.search(r"bằng \$(?:\\dfrac\{(\d+)\}\{(\d+)\}|(\d+))\$\}$", t)
    return Fraction(int(m.group(1)), int(m.group(2))) if m.group(1) else Fraction(int(m.group(3)))


def test_banh_xe_va_lo_dung_dich_dung_xac_suat():
    """Mọi phát biểu "Xác suất để ... bằng X" đúng/sai đúng như liệt kê không gian mẫu."""
    for ten, k in (("L10_C9_TF_C_01", 3), ("L10_C9_TF_D_01", 2)):
        for s in range(15):
            debai, ds = _bat(ten, s)
            n, m, t = map(int, re.search(r"một trong \$(\d+)\$ vị trí.*?\$(\d+)\$ vị trí được cộng.*?\$(\d+)\$ vị trí bị",
                                         debai).groups())
            om = list(product(range(n), repeat=k))
            su_kien = {
                "cả %s lần đều được cộng điểm" % ("ba" if k == 3 else "hai"): lambda o: all(v < m for v in o),
                "có ít nhất một lần bị trừ điểm": lambda o: any(v >= m for v in o),
                "có đúng một lần bị trừ điểm": lambda o: sum(v >= m for v in o) == 1,
            }
            for y in ds:
                for p, _ in y:
                    for mo_ta, f in su_kien.items():
                        if ("Xác suất để %s bằng" % mo_ta) in p:
                            thuc = Fraction(sum(1 for o in om if f(o)), len(om))
                            assert (thuc == _ps(p)) == p.startswith(r"{\True"), (ten, s, p)
    for s in range(15):
        debai, ds = _bat("L10_C9_TF_E_01", s)
        a, b, c = map(int, re.search(r"Có \$(\d+)\$ lọ.*?axit, \$(\d+)\$ lọ.*?bazơ và \$(\d+)\$ lọ", debai).groups())
        lo = ["a"] * a + ["b"] * b + ["c"] * c
        om = list(combinations(range(len(lo)), 2))
        su_kien = {"cả hai mảnh giấy quỳ đều hoá đỏ": lambda p, q: p == q == "a",
                   "hai mảnh giấy quỳ có cùng màu": lambda p, q: p == q,
                   "có ít nhất một mảnh giấy quỳ hoá đỏ": lambda p, q: "a" in (p, q),
                   "một mảnh hoá đỏ và một mảnh hoá xanh": lambda p, q: {p, q} == {"a", "b"}}
        for y in ds:
            for p, _ in y:
                for mo_ta, f in su_kien.items():
                    if ("Xác suất để %s bằng" % mo_ta) in p:
                        thuc = Fraction(sum(1 for i, j in om if f(lo[i], lo[j])), len(om))
                        assert (thuc == _ps(p)) == p.startswith(r"{\True"), (s, p)
