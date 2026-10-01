"""Khoá quy tắc chống trùng của chương 1 (cô Lan 01/10/2026):
"chọn câu này rồi thì câu khác không chọn nữa, cùng lắm hết câu rồi mới quay lại chọn".

Mỗi mệnh đề (một phần tử của kho, ghi trong sổ xoay vòng _C1_XV.da_dung) chỉ được dùng lại khi cả
chủ đề đã dùng hết - kể cả giữa các LOẠI CÂU khác nhau (MC bốn mệnh đề, SA đếm, MC/TL một mệnh đề)
và giữa các lần gọi hàm (mỗi câu của đề là một lần gọi, socau = 1).
"""
import importlib.util
import random
import sys
from pathlib import Path

import pytest

BANK = Path(__file__).resolve().parent.parent / "data" / "python_bank"
if str(BANK) not in sys.path:
    sys.path.insert(0, str(BANK))


def _nap():
    tep = BANK / "toan10" / "L10_C1.py"
    spec = importlib.util.spec_from_file_location("L10_C1_xoay", tep)
    mo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mo)
    return mo


M = _nap()

THEO_CHU_DE = [  # (hàm, sổ, số mệnh đề mỗi câu)
    ("L10_C1_B1_TH014_MC_E_01", "c1_dl_tu_giac"), ("L10_C1_B1_TH014_SA_A_01", "c1_dl_tu_giac"),
    ("L10_C1_B1_TH014_MC_H_01", "c1_dl_tam_giac"), ("L10_C1_B1_TH014_SA_D_01", "c1_dl_tam_giac"),
    ("L10_C1_B1_TH014_MC_C_01", "c1_dl_chia_het"), ("L10_C1_B1_TH014_SA_E_01", "c1_dl_chia_het"),
    ("L10_C1_B1_TH014_MC_I_01", "c1_dl_so_thuc"), ("L10_C1_B1_TH014_SA_F_01", "c1_dl_so_thuc"),
    ("L10_C1_B1_TH014_MC_J_01", "c1_lt_chan_le"), ("L10_C1_B1_TH014_SA_B_01", "c1_lt_chan_le"),
    ("L10_C1_B1_TH014_MC_K_01", "c1_lt_bat_dang_thuc"), ("L10_C1_B1_TH014_SA_G_01", "c1_lt_bat_dang_thuc"),
    ("L10_C1_B1_TH014_MC_L_01", "c1_lt_phuong_trinh"), ("L10_C1_B1_TH014_SA_H_01", "c1_lt_phuong_trinh"),
]


def _so(ten):
    return set(M._C1_XV.da_dung.get(ten, set()))


@pytest.mark.parametrize("ham,so", THEO_CHU_DE)
@pytest.mark.parametrize("seed", range(8))
def test_bon_menh_de_khong_trung_cho_toi_khi_het(ham, so, seed):
    random.seed(seed)
    M._C1_XV.da_dung.clear()
    n = len(M._KHO_DL[so[6:]]) if so.startswith("c1_dl_") else len(M._KHO_LT[so[6:]]())
    # trong một vòng, mỗi câu lấy 4 mệnh đề MỚI; chỉ câu CUỐI vòng (phần còn lại không đủ để ghép
    # 1 đúng + 3 sai hoặc 1 sai + 3 đúng) mới được lấy lại mệnh đề đã dùng
    for _lan in range(n // 4):
        truoc = _so(so)
        getattr(M, ham)(1, 1)
        sau = _so(so)
        if _lan < n // 4 - 1:
            moi = sau - truoc
            assert len(moi) == 4 and truoc <= sau, (ham, _lan, truoc, sau)


@pytest.mark.parametrize("seed", range(8))
def test_mot_menh_de_va_bon_menh_de_dung_chung_so(seed):
    """MC_D / tự luận (một mệnh đề) và MC, SA theo chủ đề không lấy trùng mệnh đề của nhau trong một vòng."""
    random.seed(seed)
    M._C1_XV.da_dung.clear()
    tong = sum(len(v) for v in M._KHO_DL.values())
    da = set()
    ham = ["L10_C1_B1_TH014_MC_D_01", "L10_C1_NB010_TH014_TL_A_01", "L10_C1_B1_TH014_MC_E_01",
           "L10_C1_B1_TH014_SA_E_01", "L10_C1_B1_TH014_MC_D_02", "L10_C1_B1_TH014_MC_H_01"]
    for k in range(6):
        getattr(M, ham[k])(1, 1)
        hien = {(t, i) for t, s in M._C1_XV.da_dung.items() if t.startswith("c1_dl_") for i in s}
        assert da <= hien, "mot menh de da dung bi xoa so truoc khi het chu de"
        da = hien
    assert len(da) <= tong
