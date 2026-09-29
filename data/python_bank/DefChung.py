"""
Các hàm đếm dùng chung cho ngân hàng đề.

Dựng lại từ mô-đun DefChung mà các tệp gốc của cô Lan vẫn `import`. Chỉ
giữ những hàm ngân hàng thật sự cần; tên hàm giữ nguyên để mã cũ của cô
chuyển sang không phải sửa.
"""

import math


def calculate_coefficient(n, k):
    """Tổ hợp chập k của n phần tử: $C_n^k$ (chọn k, không kể thứ tự)."""
    n, k = int(n), int(k)
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def calculate_permutations(n, k):
    """Chỉnh hợp chập k của n phần tử: $A_n^k$ (chọn k, CÓ kể thứ tự)."""
    n, k = int(n), int(k)
    if k < 0 or k > n:
        return 0
    return math.perm(n, k)


def UCLN(a, b):
    """Ước chung lớn nhất."""
    return math.gcd(int(a), int(b))


# =====================================================================
# VIẾT BIỂU THỨC CHO ĐÚNG KIỂU SGK (thêm 29/09/2026)
#
# Cô Lan bắt được "1x + 2y <= 12". Quét cả ngân hàng thấy 56 hàm cùng một
# họ lỗi: in hệ số 1 ("1x", "-1y", "1x^3"), in hệ số 0 ("x^2 + 0x - 4"),
# cộng số âm ("5 + -3"), trừ số âm ("1 - -3"), nhân với số âm không có
# ngoặc ("3 \cdot -2"), và NGHIÊM TRỌNG NHẤT là lũy thừa của số âm không
# có ngoặc: "-3^{8}" nghĩa là -(3^8) chứ KHÔNG phải (-3)^8 - in sai như
# vậy là sai toán, không chỉ xấu.
#
# Mọi hàm dưới đây nhận số nguyên, Fraction, hoặc chuỗi LaTeX đã viết
# sẵn (ví dụ r"\dfrac{1}{2}", r"-\sqrt{3}"): chuỗi bắt đầu bằng "-" được
# coi là số âm.
# =====================================================================

from fractions import Fraction as _Fr


def _am(x):
    if isinstance(x, str):
        return x.strip().startswith("-")
    return x < 0


def _khong(x):
    if isinstance(x, str):
        return x.strip() in ("0", "-0", "+0")
    return x == 0


def _tri_tuyet_doi(x):
    """Chuỗi LaTeX của |x| (bỏ dấu trừ đầu)."""
    if isinstance(x, str):
        s = x.strip()
        return s[1:].strip() if s.startswith("-") else s.lstrip("+").strip()
    x = abs(x)
    if isinstance(x, _Fr):
        if x.denominator == 1:
            return str(x.numerator)
        return r"\dfrac{%d}{%d}" % (x.numerator, x.denominator)
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x).replace(".", ",")


def bt_hang(he, bien="", dau=False):
    r"""Viết MỘT hạng tử $he \cdot bien$ cho đúng kiểu SGK.

    dau=False: hạng tử đứng ĐẦU biểu thức  -> "3x", "-x", "x", "-5"
    dau=True : hạng tử đứng SAU, kèm dấu   -> " + 3x", " - x", " + 5"
    he = 0 thì trả về "" (bỏ hẳn hạng tử).
    Hệ số 1 và -1 đi với biến thì KHÔNG viết số 1.
    """
    if _khong(he):
        return ""
    am = _am(he)
    so = _tri_tuyet_doi(he)
    if bien and so == "1":
        so = ""
    than = so + bien
    if dau:
        return (" - " if am else " + ") + than
    return ("-" if am else "") + than


def bt(*hang):
    r"""Ghép nhiều hạng tử thành một biểu thức gọn.

    bt((2, "x"), (-1, "y"), (5, ""))  ->  "2x - y + 5"
    bt((1, "x^2"), (0, "x"), (-4, "")) ->  "x^2 - 4"
    Mọi hạng tử đều bằng 0 thì trả về "0".
    """
    ra = ""
    for he, bien in hang:
        if _khong(he):
            continue
        ra += bt_hang(he, bien, dau=bool(ra))
    return ra or "0"


def ngoac(x):
    r"""Số âm đứng sau dấu nhân, sau dấu trừ, hoặc làm cơ số lũy thừa thì
    phải có ngoặc: -3 -> "\left(-3\right)", 5 -> "5"."""
    s = _tri_tuyet_doi(x)
    return r"\left(-%s\right)" % s if _am(x) else s


def cong(x):
    r"""Số đứng SAU trong một tổng: 5 -> " + 5", -5 -> " - 5"."""
    return (" - " if _am(x) else " + ") + _tri_tuyet_doi(x)


def tru(x):
    r"""Trừ đi một số: tru(5) -> " - 5", tru(-5) -> " - \left(-5\right)".

    Dùng khi muốn GIỮ phép trừ trong lời giải (ví dụ công thức
    $x - x_0$ thay số). Muốn gọn thì dùng cong(-x) thay cho tru(x).
    """
    return " - " + ngoac(x)


def thay_so(*cap, hs=None):
    r"""Viết phép THAY SỐ vào một tổng các tích.

    thay_so((2, -3), (-1, 4), hs=5)
        -> "2\cdot\left(-3\right) - 1\cdot 4 + 5"
    Mỗi cặp là (hệ số, giá trị thay vào). Giá trị âm luôn có ngoặc; hệ
    số âm đứng sau thì chuyển thành dấu trừ.
    """
    ra = ""
    for he, gt in cap:
        tich = r"%s\cdot %s" % (_tri_tuyet_doi(he), ngoac(gt))
        if not ra:
            ra = ("-" if _am(he) else "") + tich
        else:
            ra += (" - " if _am(he) else " + ") + tich
    if hs is not None and not _khong(hs):
        ra += cong(hs) if ra else ("-" if _am(hs) else "") + _tri_tuyet_doi(hs)
    return ra or "0"


def luy_thua(co_so, mu):
    r"""Lũy thừa: cơ số âm PHẢI có ngoặc.

    luy_thua(-3, 8) -> "\left(-3\right)^{8}"   (= 6561)
    Viết "-3^{8}" là SAI: nó có nghĩa là -(3^8) = -6561.
    """
    return r"%s^{%s}" % (ngoac(co_so), mu)
