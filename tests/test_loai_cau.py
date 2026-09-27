"""
Quy uoc loai cau (co Lan chot 27/09/2026):

    Tra loi ngan (_SA_) : MOT cau hoi -> MOT dap an. KHONG chia y a), b).
    Tu luan      (_TL_) : phai co TU HAI Y tro len.
    Trac nghiem  (_MC_) : co \\choice, khong duoc co \\shortans.
    Dung/Sai     (_TF_) : dung \\choiceTFt.

Khoa o hai tang:
  - math_type.py           chan ngay luc viet ham sinh cau hoi
  - generator_service.py   chan luc RA DE, theo chinh TEN HAM

Bai test nay canh ca hai tang, va chay lai toan bo cac ham _SA_ / _TL_ da co
trong ngan hang de bao dam khong ham nao lech quy uoc.
"""

import glob
import importlib.util
import re
import sys

import pytest

sys.path.insert(0, "data/python_bank")

from app.services.generator_service import kiem_tra_dung_loai_cau, LoaiCauSaiError

EX = "\\begin{ex}%s\\loigiai{x}\\end{ex}"
SA_MOT_Y = EX % "De hoi mot y\n\\shortans{$7$}\n"
SA_NHIEU_Y = EX % ("De\n\\begin{listEX}[1]\\item Hoi a \\SA[4]{$1$}"
                   "\\item Hoi b \\SA[4]{$2$}\\end{listEX}\n")
TL_HAI_Y = EX % ("De\n\\begin{listEX}[1]\\item Hoi a \\SA[4]{$1$}"
                 "\\item Hoi b \\SA[4]{$2$}\\end{listEX}\n")
TL_MOT_Y = EX % "De\n\\begin{listEX}[1]\\item Hoi a \\SA[4]{$1$}\\end{listEX}\n"
MC_TOT = EX % "De\n\\choice{\\True $1$}{$2$}{$3$}{$4$}\n"
MC_CO_SHORTANS = EX % "De\n\\choice{\\True $1$}{$2$}{$3$}{$4$}\n\\shortans{$1$}\n"
TF_TOT = EX % "De\n\\choiceTFt{\\True a}{b}{c}{d}\n"


# ------------------------------------------------ tang khoa luc RA DE

def test_tra_loi_ngan_mot_y_thi_cho_qua():
    kiem_tra_dung_loai_cau("L10_C3_B6_TH034_SA_A", SA_MOT_Y)


def test_tra_loi_ngan_chia_y_thi_bi_chan():
    with pytest.raises(LoaiCauSaiError):
        kiem_tra_dung_loai_cau("L10_C3_B6_TH034_SA_A", SA_NHIEU_Y)


def test_tu_luan_hai_y_thi_cho_qua():
    kiem_tra_dung_loai_cau("L10_C3_B6_VD036_TL_A", TL_HAI_Y)


def test_tu_luan_mot_y_thi_bi_chan():
    with pytest.raises(LoaiCauSaiError):
        kiem_tra_dung_loai_cau("L10_C3_B6_VD036_TL_A", TL_MOT_Y)


def test_trac_nghiem_co_shortans_thi_bi_chan():
    with pytest.raises(LoaiCauSaiError):
        kiem_tra_dung_loai_cau("L10_C3_B5_NB029_MC_A", MC_CO_SHORTANS)


def test_trac_nghiem_va_dung_sai_dung_chuan_thi_cho_qua():
    kiem_tra_dung_loai_cau("L10_C3_B5_NB029_MC_A", MC_TOT)
    kiem_tra_dung_loai_cau("L10_C3_TF_A", TF_TOT)


# ------------------------------------------------ tang khoa luc VIET HAM

def test_math_type_chan_tra_loi_ngan_chia_y():
    from math_type import MC_SA_answer_const
    with pytest.raises(ValueError):
        MC_SA_answer_const("De\\begin{listEX}[1]\\item Hoi a\\end{listEX}",
                           "5", ["1", "2", "3"], "giai", 0, 0, 2)


def test_math_type_chan_tu_luan_mot_y():
    from math_type import TL_answer_const
    with pytest.raises(ValueError):
        TL_answer_const("De", [("Hoi a", 1, "giai a")], 0, 0, 1)


def test_math_type_van_cho_qua_khi_dung_chuan():
    from math_type import MC_SA_answer_const, TL_answer_const
    assert "\\shortans" in MC_SA_answer_const("De hoi mot y", "5", ["1", "2", "3"],
                                              "giai", 0, 0, 2)
    assert "\\item" in TL_answer_const("De", [("Hoi a", 1, "giai a"),
                                              ("Hoi b", 2, "giai b")], 0, 0, 1)


# ------------------------------------------------ soat toan bo ngan hang

def _ham_sa_tl():
    ra = []
    for f in sorted(glob.glob("data/python_bank/toan*/L*_C*.py")):
        spec = importlib.util.spec_from_file_location("bank_" + f.replace("/", "_"), f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for ten in sorted(n for n in dir(m)
                          if re.match(r"^L\d+_C\d+.*_\d{2}$", n)
                          and ("_SA_" in n or "_TL_" in n)):
            ra.append((ten, getattr(m, ten)))
    return ra


# Ham da co san trong ngan hang nhung CHUA dung quy uoc, cho co Lan quyet.
# Khi nao sua xong thi xoa khoi danh sach nay - bai test se tu doi hoi lai.
CHUA_DUNG_QUY_UOC = {
    # Tu luan nhung chi co MOT y ("So gia tri nguyen cua m de A hop B = A").
    # Theo quy uoc thi mot cau mot dap an la TRA LOI NGAN. Hai cach sua:
    # them mot y thu hai, hoac doi sang dang _SA_ (phai sua ca Mapping).
    # Trong luc cho: khi ra de, ham nay bi chan va he thong bao thieu, khong
    # cho cau sai loai vao de cua hoc sinh.
    "L10_C1_B2_VD021_TL_A_01",
}


@pytest.mark.parametrize("ten,ham", _ham_sa_tl(), ids=lambda x: x if isinstance(x, str) else "")
def test_moi_ham_da_co_deu_dung_loai(ten, ham):
    """Chay that tung ham _SA_ / _TL_ trong ngan hang, soi theo dung ten no."""
    if ten in CHUA_DUNG_QUY_UOC:
        pytest.skip("cho co Lan sua: %s chua dung quy uoc loai cau" % ten)
    khoi = ham(1, 2 if "_SA_" in ten else 1)
    kiem_tra_dung_loai_cau(ten, khoi)
