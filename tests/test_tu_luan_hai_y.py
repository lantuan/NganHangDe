# -*- coding: utf-8 -*-
r"""Câu tự luận chỉ đưa ra HAI ý (cô Lan 01/10/2026) - app/services/tu_luan_hai_y.py.

Mọi hàm sinh câu tự luận trong ngân hàng, sau khi qua giu_hai_y, có đúng hai \item ở đề
và hai \item ở lời giải; câu mức VD luôn giữ ý cuối (ý khó nhất, VDC).
"""
import contextlib
import glob
import importlib
import io
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from app.services.tu_luan_hai_y import giu_hai_y, _tim_listex, _tach_item  # noqa: E402


def _cac_ham_tl():
    ra = []
    for p in sorted(glob.glob(str(GOC / "data/python_bank/toan1*/L1*_C*.py"))):
        lop = re.search(r"toan(\d+)", p).group(1)
        sys.path.insert(0, str(GOC / ("data/python_bank/toan%s" % lop)))
        with contextlib.redirect_stdout(io.StringIO()):
            m = importlib.import_module(Path(p).stem)
        ra += [(m, n) for n in sorted(dir(m)) if re.match(r"^L\d+_C\d+_.*_TL_[A-Z]+_\d\d$", n)]
    return ra


HAM = _cac_ham_tl()


def _dem(ex):
    lg = ex.find("\\loigiai")
    q, s = _tim_listex(ex, 0), _tim_listex(ex, lg)
    return len(_tach_item(ex[q[0]:q[1]])[1]), len(_tach_item(ex[s[0]:s[1]])[1])


@pytest.mark.parametrize("m,ten", HAM, ids=[t for _, t in HAM])
def test_moi_cau_tu_luan_chi_con_hai_y(m, ten):
    for sd in range(4):
        random.seed(sd)
        with contextlib.redirect_stdout(io.StringIO()):
            goc = getattr(m, ten)(1)
        ra = giu_hai_y(goc, ten)
        assert _dem(ra) == (2, 2), ten
        if re.search(r"_VD\d+[A-Z]?_TL_", ten) and _dem(goc)[0] > 2:
            # mức VD: luôn giữ ý cuối (ý khó nhất)
            lg = goc.find("\\loigiai")
            q = _tim_listex(goc, 0)
            cuoi = _tach_item(goc[q[0]:q[1]])[1][-1]
            dap_cuoi = cuoi[cuoi.find("\\SA"):].strip()        # đáp số của ý cuối
            assert dap_cuoi in ra, (ten, dap_cuoi)
