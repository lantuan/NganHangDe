# -*- coding: utf-8 -*-
r"""Làm đẹp biểu thức toán trong câu hỏi vừa sinh (cô Lan chốt 29/09/2026).

VÌ SAO CÓ BỘ LỌC NÀY
    Cô Lan chụp màn hình đề thật: "Cho bất phương trình 1x + 2y <= 12".
    Quét cả ngân hàng thấy 56 hàm cùng một họ lỗi trình bày: in hệ số 1
    ("1x", "-1y"), in hạng tử hệ số 0 ("x^2 + 0x - 4"), cộng số âm
    ("5 + -3"), trừ số âm ("1 - -3"), nhân với số âm không có ngoặc
    ("3 \cdot -2"). Cô chọn: MỘT BỘ LỌC CHUNG chạy ngay sau khi hàm sinh
    câu, thay vì sửa tay từng hàm - sửa được cả hàm viết sau này.

NGUYÊN TẮC: CHỈ SỬA CHỖ CHẮC CHẮN KHÔNG ĐỔI NGHĨA
    1x -> x, -1y -> -y, 1\left( -> \left(, 1\sqrt -> \sqrt
    ... + 0x ... -> bỏ hạng tử
    + -5 -> - 5,  - -5 -> + 5,  \cdot -5 -> \cdot \left(-5\right)
    Mọi chỗ mà số âm là CƠ SỐ LŨY THỪA ("+ -3^{8}", "\cdot -2^{7}") thì
    KHÔNG đụng vào: "-3^{8}" nghĩa là -(3^8), còn người viết thường muốn
    (-3)^8 - hai số khác nhau. Đoán hộ là có thể làm SAI đáp án, nên phải
    sửa tận gốc trong hàm (xem tests/test_lam_dep_bieu_thuc.py - bài kiểm
    tra quét cả ngân hàng tìm những chỗ đó).

    "1\dfrac{1}{2}" cũng KHÔNG đụng: đó có thể là HỖN SỐ.
    "1\cdot x" cũng giữ nguyên: đó là bước thay số trong lời giải.

    Chỉ sửa BÊN TRONG vùng toán $...$; không đụng chữ thường, không đụng
    hình TikZ.
"""
import re

_TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)
_VUNG_TOAN = re.compile(r"\$\$.*?\$\$|\$[^$]*\$", re.S)

# Hệ số 1 đứng trước MỘT chữ cái biến (không phải đầu một từ dài hơn),
# trước \left( hoặc \sqrt. Đứng trước nó KHÔNG được là chữ số (21x),
# dấu phẩy thập phân (0,1x), chỉ số/số mũ (x_1y, x^1y), ngoặc nhọn đóng
# hay dấu gạch chéo ngược.
_HE_SO_1 = re.compile(
    r"(?<![0-9.,_^}\\a-zA-Z])1(?=(?:[a-zA-Z](?![a-zA-Z])|\\left\(|\\sqrt\b))")
# Cho phép MỘT khoảng trắng ("1 n + 4") khi sau đó là đúng một chữ cái
# rồi tới dấu phép toán / hết biểu thức.
_HE_SO_1_CACH = re.compile(
    r"(?<![0-9.,_^}\\a-zA-Z])1 (?=[a-zA-Z](?:\s*[-+=<>)^$]|\s*\\(?:le|ge|right)\b|\s*$))")

# Hạng tử có hệ số 0 ở GIỮA biểu thức: " + 0x", " - 0 x", " + 0x^{2}".
_HE_SO_0 = re.compile(
    r"\s[-+]\s*0\s?[a-zA-Z](?:\^\{[^{}]*\}|\^\d)?(?=\s*(?:[-+=<>)}]|\\(?:le|ge|right)\b|$))")

# Một "số" đứng sau dấu âm: số nguyên/thập phân, phân số, căn.
_SO = r"(?:\d+(?:[.,]\d+)?|\\d?frac\{[^{}]*\}\{[^{}]*\}|\\sqrt\{[^{}]*\})"
_CONG_AM = re.compile(r"\+\s*-\s*(" + _SO + r")")
# Truoc "- -" phai la mot TOAN HANG (chu, so, ngoac dong) - khong thi
# do la dau am dung dau, vi du "(- -3)" hiem gap, de nguyen.
_TRU_AM = re.compile(r"([\w})\]])\s*-\s*-\s*(" + _SO + r")")
_NHAN_AM = re.compile(r"\\cdot\s*-\s*(" + _SO + r")")


def _khong_phai_co_so(chuoi, het):
    """Sau con số không có dấu mũ ^ (tức nó không phải cơ số lũy thừa)."""
    sau = chuoi[het:het + 3].lstrip()
    return not sau.startswith("^")


def _sua_vung_toan(t):
    cu = None
    while cu != t:
        cu = t
        t = _HE_SO_1.sub("", t)
        t = _HE_SO_1_CACH.sub("", t)
        t = _HE_SO_0.sub("", t)
        t = _CONG_AM.sub(lambda m: ("- " + m.group(1)) if _khong_phai_co_so(t, m.end()) else m.group(0), t)
        t = _TRU_AM.sub(lambda m: (m.group(1) + " + " + m.group(2)) if _khong_phai_co_so(t, m.end()) else m.group(0), t)
        t = _NHAN_AM.sub(lambda m: (r"\cdot \left(-" + m.group(1) + r"\right)") if _khong_phai_co_so(t, m.end()) else m.group(0), t)
    return t


def lam_dep(latex):
    """Làm đẹp mọi vùng toán trong một khối LaTeX (bỏ qua hình TikZ)."""
    if not latex:
        return latex
    ra, i = [], 0
    for m in _TIKZ.finditer(latex):
        ra.append(_VUNG_TOAN.sub(lambda v: _sua_vung_toan(v.group(0)), latex[i:m.start()]))
        ra.append(m.group(0))
        i = m.end()
    ra.append(_VUNG_TOAN.sub(lambda v: _sua_vung_toan(v.group(0)), latex[i:]))
    return "".join(ra)
