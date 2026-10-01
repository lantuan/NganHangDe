"""Câu Đúng/Sai chương 3 lớp 10: MỖI Ý phải có NHIỀU phát biểu đúng và NHIỀU phát biểu sai.

Cô Lan 01/10/2026: "để tránh học sinh học thuộc thì nhất định các câu a, b, c, d phải có nhiều đáp
án đúng và nhiều đáp án sai trong chính câu đấy" - TF_baitoan_du (math_type.py) chọn ngẫu nhiên một
phát biểu trong danh sách của mỗi ý, nên mỗi ý phải liệt kê được ít nhất 3 phát biểu đúng và 3 phát
biểu sai KHÁC NHAU ở mỗi lần chạy.
"""
import importlib.util
import random
import re
import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
BANK = BASE_DIR / "data" / "python_bank"
if str(BANK) not in sys.path:
    sys.path.insert(0, str(BANK))

TOI_THIEU = 3          # số phát biểu đúng / sai tối thiểu của mỗi ý
SO_LAN = 25            # số lần chạy (seed) mỗi hàm


def _nap(tep):
    spec = importlib.util.spec_from_file_location(tep.stem, tep)
    mo = importlib.util.module_from_spec(spec)
    sys.modules[tep.stem] = mo
    spec.loader.exec_module(mo)
    return mo


MO = _nap(BANK / "toan10" / "L10_C3.py")
HAM = sorted(t for t in dir(MO) if re.match(r"^L10_C3_TF_[A-Z]_\d{2}$", t))


@pytest.mark.parametrize("ten", HAM)
def test_moi_y_nhieu_dung_nhieu_sai(ten, monkeypatch):
    bat = []
    goc = MO.TF_baitoan_du

    def _bat(debai, ds, d1, d2, socot):
        bat.append(ds)
        return goc(debai, ds, d1, d2, socot)

    monkeypatch.setattr(MO, "TF_baitoan_du", _bat)
    for seed in range(SO_LAN):
        random.seed(seed)
        bat.clear()
        getattr(MO, ten)(1, 1)
        assert len(bat) == 1 and len(bat[0]) == 4, ten
        for k, y in enumerate(bat[0]):
            dung = {t for t, _ in y if "\\True" in t}
            sai = {t for t, _ in y if "\\True" not in t}
            assert len(dung) >= TOI_THIEU and len(sai) >= TOI_THIEU, (
                "%s (seed %d) y %s: %d dung, %d sai - can it nhat %d moi loai"
                % (ten, seed, "abcd"[k], len(dung), len(sai), TOI_THIEU))
            assert not ({t.replace("{\\True ", "{") for t in dung} & sai), "%s y %s: phat bieu vua dung vua sai" % (ten, "abcd"[k])
