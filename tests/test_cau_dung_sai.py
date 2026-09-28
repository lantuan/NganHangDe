"""
Quy uoc cau DUNG/SAI (co Lan chot 27/09/2026):

    a) NB   nhan biet      - nhac lai mot cong thuc, mot tinh chat
    b) TH   thong hieu     - thay so vao dung mot cong thuc
    c) VD   van dung       - phai co ket qua y truoc moi lam duoc
    d) VDC  van dung cao   - phai tu nghi ra cach, khong co cong thuc san

Bai test nay soi hai thu:
  1. Cau truc: moi cau Dung/Sai phai co DUNG BON y.
  2. Bac do kho: than ham phai ghi ro bon moc "# a) NB", "# b) TH",
     "# c) VD", "# d) VDC" theo dung thu tu - de nguoi viet ham buoc phai
     nghi den bac do kho chu khong xep bua bon y ngang nhau.
"""

import glob
import importlib.util
import inspect
import random
import re
import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
BANK = BASE_DIR / "data" / "python_bank"
if str(BANK) not in sys.path:
    sys.path.insert(0, str(BANK))


def _nap(tep):
    spec = importlib.util.spec_from_file_location(tep.stem, tep)
    mo = importlib.util.module_from_spec(spec)
    sys.modules[tep.stem] = mo
    spec.loader.exec_module(mo)
    return mo


def _ham_TF():
    ra = []
    for tep in sorted(Path(BANK).glob("toan*/L*_C*.py")):
        mo = _nap(tep)
        for ten in dir(mo):
            if re.match(r"^L\d+_C\d+_TF_[A-Z]_\d{2}$", ten):
                ra.append((ten, getattr(mo, ten)))
    return ra


# Ham co san tu truoc, CHUA xep bon y theo bac do kho. Khong phai loi sai
# toan - chi la chua dung quy uoc moi. Sua xong thi xoa khoi day, bai test
# se tu doi hoi lai.
CHUA_XEP_BAC = {
    "L10_C1_TF_A_01",   # bon y deu rut tu cung mot kho menh de, khong phan bac
    "L10_C1_TF_B_01",
    # Chuong 9 nhap tu tep LopXChuong9.py cua co Lan 28/09/2026. Noi dung
    # toan dung, nhung bon y chua xep theo bac NB -> TH -> VD -> VDC.
    "L10_C9_TF_A_01",
    "L10_C9_TF_B_01",
    "L10_C9_TF_C_01",
    "L10_C9_TF_D_01",
    "L10_C9_TF_E_01",
}


@pytest.mark.parametrize("ten,ham", _ham_TF(), ids=lambda x: x if isinstance(x, str) else "")
def test_moi_cau_dung_sai_co_dung_bon_y(ten, ham):
    random.seed(12)
    khoi = ham(2, 1)
    assert khoi.count(r"\choiceTFt") == 2, "moi cau phai co dung mot khoi \\choiceTFt"
    # bon y hien ra thanh bon dong \itemch trong loi giai
    assert khoi.count(r"\itemch") == 8, (
        "%s: moi cau Dung/Sai phai co dung BON y (dem duoc %d y tren 2 cau)"
        % (ten, khoi.count(r"\itemch")))


@pytest.mark.parametrize("ten,ham", _ham_TF(), ids=lambda x: x if isinstance(x, str) else "")
def test_bon_y_duoc_xep_theo_bac_do_kho(ten, ham):
    if ten in CHUA_XEP_BAC:
        pytest.skip("cho co Lan xep lai bac do kho cho %s" % ten)
    than = inspect.getsource(ham)
    vi_tri = []
    for moc in ("# a) NB", "# b) TH", "# c) VD", "# d) VDC"):
        assert moc in than, (
            "%s: thieu moc %r. Bon y cua cau Dung/Sai phai tang dan "
            "NB -> TH -> VD -> VDC va ghi ro moc trong than ham." % (ten, moc))
        vi_tri.append(than.index(moc))
    assert vi_tri == sorted(vi_tri), "%s: bon moc do kho khong theo thu tu" % ten
