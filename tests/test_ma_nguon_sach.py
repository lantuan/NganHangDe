r"""
Ma nguon khong duoc de lai canh bao luc nap.

Chuyen that 27/09/2026: co Lan chay scripts/kiem_tra_hinh.sh tren may thi
Python in ra giua man hinh:

    hinh_ve_service.py:10: SyntaxWarning: "\e" is an invalid escape sequence

Nguyen nhan: docstring co viet \end{tikzpicture} nhung khong phai chuoi tho
(raw string), nen Python hieu "\e" la mot ky tu thoat khong hop le. Python
3.12 tro len bao SyntaxWarning, ban cu chi bao DeprecationWarning nen may ao
cua Claude khong thay - phai co may cua co Lan moi lo ra.

Ngan hang de day chuoi LaTeX nen chuyen nay se con lap lai. Bai test chay
tren MOI tep .py cua du an.
"""

import glob
import warnings
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent

TEP = sorted(
    glob.glob(str(BASE_DIR / "app" / "**" / "*.py"), recursive=True)
    + glob.glob(str(BASE_DIR / "data" / "python_bank" / "**" / "*.py"), recursive=True)
    + glob.glob(str(BASE_DIR / "scripts" / "*.py"))
    + glob.glob(str(BASE_DIR / "tests" / "*.py"))
)


@pytest.mark.parametrize("tep", TEP, ids=lambda t: Path(t).name)
def test_khong_co_ky_tu_thoat_hong(tep):
    van = Path(tep).read_text(encoding="utf-8")
    with warnings.catch_warnings(record=True) as ghi:
        warnings.simplefilter("always")
        compile(van, tep, "exec")
    hong = [w for w in ghi if "escape" in str(w.message)]
    assert not hong, (
        "%s: %s\nChuoi co dau \\ cua LaTeX phai viet la chuoi tho: r\"...\" "
        "hoac r\"\"\"...\"\"\"" % (
            Path(tep).name,
            "; ".join("dong %s: %s" % (w.lineno, w.message) for w in hong)))
