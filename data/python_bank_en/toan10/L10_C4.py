# ==========================================================
# CHƯƠNG 4 (lớp 10): VECTƠ
#   Bài 7.  Các khái niệm mở đầu
#   Bài 8.  Tổng và hiệu của hai vectơ
#   Bài 9.  Tích của một vectơ với một số
#   Bài 10. Vectơ trong mặt phẳng toạ độ
#   Bài 11. Tích vô hướng của hai vectơ
#
# Nguồn: tệp LopXChuong4.py của cô Lan. Tệp ấy viết theo FORM CŨ (tự mở
# tệp de.tex rồi de.write), nên ở đây viết lại cho đúng khuôn math_type -
# math_type.py GIỮ NGUYÊN, không sửa một dòng nào.
#
# Nội dung toán của cô được giữ ở các dạng NB038, TH042, TH048, VD060,
# VD061; phần còn lại viết mới, đều ghi rõ CLAUDE THEM.
# ==========================================================
import math
import random

from math_type import *

DAU_THAP_PHAN = ","


def _xx4(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết thành chuỗi (bỏ đuôi 0 thừa)."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu4(dapso, ung_vien, buoc=None):
    """Ba phương án nhiễu đôi một khác nhau và khác đáp số."""
    ds = []
    for v in ung_vien:
        if v != dapso and v not in ds:
            ds.append(v)
        if len(ds) == 3:
            return ds
    k = 1
    while len(ds) < 3:
        v = buoc(k) if buoc else str(k)
        if v != dapso and v not in ds:
            ds.append(v)
        k += 1
    return ds


def _toa(x):
    """Số dùng LÀM TOẠ ĐỘ TikZ - luôn dùng dấu CHẤM.

    Không được dùng _xx4 ở đây: _xx4 đổi dấu chấm thành dấu phẩy theo
    cách viết số của Việt Nam, nên toạ độ (4.4, 2.2) sẽ thành
    (4,4, 2,2) và TikZ đọc thành bốn số - hình vẽ méo hoàn toàn.
    Đã vấp đúng lỗi này khi dựng hình bài 7.
    """
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _vt(dau, cuoi):
    r"""Vectơ $\overrightarrow{AB}$."""
    return r"\overrightarrow{%s%s}" % (dau, cuoi)


def _toado(x, y):
    return r"\left(%s;\ %s\right)" % (_xx4(x), _xx4(y))


def _bt_ij(x, y, i=r"\overrightarrow{i}", j=r"\overrightarrow{j}"):
    r"""Viết x.i + y.j cho đẹp: bỏ hệ số 1, bỏ hạng tử 0, dấu trừ gọn.

    CLAUDE THEM 29/09/2026. _bt_ij(-5, -1) -> "-5\overrightarrow{i} - \overrightarrow{j}";
    _bt_ij(0, 3) -> "3\overrightarrow{j}"; _bt_ij(0, 0) -> "\overrightarrow{0}".
    """
    def hang(h, vt):
        if h == 1:
            return vt
        if h == -1:
            return "-" + vt
        return "%s%s" % (_xx4(h), vt)
    phan = [(h, vt) for h, vt in ((x, i), (y, j)) if h != 0]
    if not phan:
        return r"\overrightarrow{0}"
    kq = hang(*phan[0])
    for h, vt in phan[1:]:
        kq += (" - " if h < 0 else " + ") + hang(abs(h), vt)
    return kq


# ---------------------------------------------------------------------
# HÌNH VẼ. Mọi hình đều là TikZ thuần để đường ra hình cho web dịch được.
# ---------------------------------------------------------------------

def _hinh_tu_giac(ten, toado, them=""):
    """Tứ giác ABCD (hoặc MNPQ) với nhãn đỉnh đặt ra phía ngoài."""
    A, B, C, D = ten
    xa, ya = toado[0]
    xb, yb = toado[1]
    xc, yc = toado[2]
    xd, yd = toado[3]
    return (
        "\\begin{tikzpicture}[>=stealth,x=1cm,y=1cm,thick,scale=0.9]\n"
        "\\coordinate (%s) at (%s,%s);\n" % (A, _toa(xa), _toa(ya)) +
        "\\coordinate (%s) at (%s,%s);\n" % (B, _toa(xb), _toa(yb)) +
        "\\coordinate (%s) at (%s,%s);\n" % (C, _toa(xc), _toa(yc)) +
        "\\coordinate (%s) at (%s,%s);\n" % (D, _toa(xd), _toa(yd)) +
        "\\draw (%s) -- (%s) -- (%s) -- (%s) -- cycle;\n" % (A, B, C, D) +
        them +
        "\\foreach \\p/\\n in {%s/above left, %s/above right, "
        "%s/below right, %s/below left}\n" % (A, B, C, D) +
        "  \\fill[black] (\\p) circle[radius=1.4pt] node[\\n]"
        "{\\footnotesize $\\p$};\n"
        "\\end{tikzpicture}")


def _hinh_tam_giac_trong_tam(ten="ABC", trong_tam="G", trung_diem="I"):
    """Tam giác với trung tuyến AI và trọng tâm G."""
    A, B, C = ten
    return (
        "\\begin{tikzpicture}[>=stealth,x=1cm,y=1cm,thick,scale=0.9]\n"
        "\\coordinate (%s) at (1.2,3.2);\n" % A +
        "\\coordinate (%s) at (0,0);\n" % B +
        "\\coordinate (%s) at (4.4,0);\n" % C +
        "\\coordinate (%s) at (2.2,0);\n" % trung_diem +
        "\\coordinate (%s) at (1.8667,1.0667);\n" % trong_tam +
        "\\draw (%s) -- (%s) -- (%s) -- cycle;\n" % (A, B, C) +
        "\\draw (%s) -- (%s);\n" % (A, trung_diem) +
        "\\fill[black] (%s) circle[radius=1.4pt] node[above]"
        "{\\footnotesize $%s$};\n" % (A, A) +
        "\\fill[black] (%s) circle[radius=1.4pt] node[below left]"
        "{\\footnotesize $%s$};\n" % (B, B) +
        "\\fill[black] (%s) circle[radius=1.4pt] node[below right]"
        "{\\footnotesize $%s$};\n" % (C, C) +
        "\\fill[black] (%s) circle[radius=1.4pt] node[below]"
        "{\\footnotesize $%s$};\n" % (trung_diem, trung_diem) +
        "\\fill[black] (%s) circle[radius=1.4pt] node[right]"
        "{\\footnotesize $%s$};\n" % (trong_tam, trong_tam) +
        "\\end{tikzpicture}")


# =====================================================================
# BÀI 7. CÁC KHÁI NIỆM MỞ ĐẦU
# =====================================================================

def L10_C4_B7_NB037_MC_A_01(socau, dang=1):
    r"""Nhận ra hai vectơ cùng phương, cùng hướng trong hình cho trước.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Có HÌNH VẼ: cô Lan đã chốt câu hình phải có hình cả trên web, vì
    không có hình thì mức độ của câu bị lệch.
    """
    BO_TEN = ["ABCD", "MNPQ"]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_TEN))
        cap = random.choice([0, 1])
        if (i, cap) not in gt:
            gt.append((i, cap))
        if len(gt) >= 2 * len(BO_TEN):
            break

    cauTN = ""
    for i, cap in gt:
        ten = BO_TEN[i]
        A, B, C, D = ten
        # hình bình hành: A(0;0), B(3.6;0), C(4.6;2.2), D(1;2.2)
        # nhãn đỉnh theo thứ tự A dưới trái, B dưới phải, C trên phải,
        # D trên trái nên dùng toạ độ đi theo chiều đó.
        hinh = _hinh_tu_giac(
            ten, [(1, 2.2), (4.6, 2.2), (3.6, 0), (0, 0)])
        # ở hình trên: A trên trái, B trên phải, C dưới phải, D dưới trái
        # => AB cùng hướng DC ; AD cùng hướng BC
        if cap == 0:
            dung = r"$%s$ and $%s$ have the same direction" % (_vt(A, B), _vt(D, C))
            nhieu = [r"$%s$ and $%s$ have the same direction" % (_vt(A, B), _vt(C, D)),
                     r"$%s$ and $%s$ are collinear" % (_vt(A, B), _vt(A, D)),
                     r"$%s$ and $%s$ are collinear" % (_vt(A, C), _vt(B, D)),
                     r"$%s$ and $%s$ have the same direction" % (_vt(B, A), _vt(D, C))]
            ly_do = (r"Since $%s%s%s%s$ is a parallelogram, $%s$ is parallel and "
                     r"equal to $%s$; moreover, the two vectors $%s$ and $%s$ point to the same "
                     r"side, so they have the \textbf{same direction}."
                     % (A, B, C, D, A + B, D + C, _vt(A, B), _vt(D, C)))
        else:
            dung = r"$%s$ and $%s$ have the same direction" % (_vt(A, D), _vt(B, C))
            nhieu = [r"$%s$ and $%s$ have the same direction" % (_vt(A, D), _vt(C, B)),
                     r"$%s$ and $%s$ are collinear" % (_vt(A, D), _vt(A, B)),
                     r"$%s$ and $%s$ are collinear" % (_vt(A, C), _vt(B, D)),
                     r"$%s$ and $%s$ have the same direction" % (_vt(D, A), _vt(B, C))]
            ly_do = (r"Since $%s%s%s%s$ is a parallelogram, $%s$ is parallel and equal "
                     r"to $%s$; the two vectors $%s$ and $%s$ point to the same side, so "
                     r"they have the \textbf{same direction}."
                     % (A, B, C, D, A + D, B + C, _vt(A, D), _vt(B, C)))

        debai = (r"Given parallelogram $%s$ as shown in the figure. Which of the following statements is "
                 r"\textbf{true}?" % ten)
        giai = (r"Two vectors are \textbf{collinear} if their lines of action are parallel "
                r"or coincide; among collinear vectors, two vectors have the "
                r"\textbf{same direction} when they point to the same side."
                "\\\\\n" + ly_do +
                "\\\\\n"
                r"The two diagonals $%s$ and $%s$ intersect, so $%s$ and $%s$ "
                r"are not collinear." % (A + C, B + D, _vt(A, C), _vt(B, D)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B7_NB038_MC_A_01(socau, dang=1):
    r"""Nhận ra hai vectơ bằng nhau trong hình cho trước.

    Giữ nguyên bài của cô Lan (K10_2_3_1_2_NB): hình chữ nhật với hai
    trung điểm của hai cạnh đối, hỏi khẳng định nào SAI.

    Bản cũ của cô có hai lỗi LaTeX đã sửa ở đây:
      - phương án thứ tư thừa một dấu } làm hỏng khối \immini;
      - khối tikzpicture đặt sau \choice nên hình rơi ra ngoài ô hình.
    Nội dung toán của cô ĐÚNG, đã kiểm lại bằng toạ độ:
    với $M$, $N$ là trung điểm $AB$, $CD$ thì
    $\overrightarrow{DA} = -\overrightarrow{MN}$ nên khẳng định
    $\overrightarrow{DA} = \overrightarrow{MN}$ là SAI.
    """
    BO = [("ABCD", "M", "N"), ("MNPQ", "R", "S")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO):
            break

    cauTN = ""
    for i in gt:
        ten, M, N = BO[i]
        A, B, C, D = ten
        # A trên trái, B trên phải, C dưới phải, D dưới trái
        them = ("\\coordinate (%s) at (2.2,2.2);\n" % M +
                "\\coordinate (%s) at (2.2,0);\n" % N +
                "\\draw (%s) -- (%s);\n" % (M, N) +
                "\\fill[black] (%s) circle[radius=1.4pt] node[above]"
                "{\\footnotesize $%s$};\n" % (M, M) +
                "\\fill[black] (%s) circle[radius=1.4pt] node[below]"
                "{\\footnotesize $%s$};\n" % (N, N))
        hinh = _hinh_tu_giac(ten, [(0, 2.2), (4.4, 2.2), (4.4, 0), (0, 0)],
                             them)

        dung = r"$%s = %s$" % (_vt(D, A), _vt(M, N))
        nhieu = [r"$%s = %s$" % (_vt(M, B), _vt(N, C)),
                 r"$%s = %s$" % (_vt(A, B), _vt(D, C)),
                 r"$%s = %s$" % (_vt(M, A), _vt(C, N))]

        debai = (r"Let $%s$ be a rectangle, with $%s$ and $%s$ the midpoints of "
                 r"sides $%s$ and $%s$, respectively (see figure). Which of the "
                 r"following statements is \textbf{false}?"
                 % (ten, M, N, A + B, C + D))
        giai = (r"Two vectors are equal when they have the \textbf{same direction} and "
                r"the \textbf{same magnitude}."
                "\\\\\n"
                r"$%s$ points upward, while $%s$ points downward: these two "
                r"vectors have \textbf{opposite directions} (they are opposite "
                r"vectors), so $%s = %s$ is a false statement."
                % (_vt(D, A), _vt(M, N), _vt(D, A), _vt(M, N)) +
                "\\\\\n"
                r"The other three statements are all true: $%s$ and $%s$ have the same direction and "
                r"the same length (both equal to half of side $%s$); $%s$ and $%s$ have the "
                r"same direction and the same length; $%s$ and $%s$ have the same direction and the same length."
                % (_vt(M, B), _vt(N, C), A + B, _vt(A, B), _vt(D, C),
                   _vt(M, A), _vt(C, N)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B7_TH039_MC_A_01(socau, dang=1):
    """Biểu thị một đại lượng thực tiễn bằng vectơ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    LA_VECTO = [
        "The velocity of a moving boat",
        "The pulling force acting on a crate",
        "The displacement of an object from one position to another",
        "The acceleration of a moving object",
    ]
    KHONG_VECTO = [
        "The air temperature in a room",
        "The mass of a bag of rice",
        "The time taken to cover the distance",
        "The area of a garden",
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(LA_VECTO))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(LA_VECTO):
            break

    cauTN = ""
    for i in gt:
        dung = "%s." % LA_VECTO[i]
        nhieu = ["%s." % t for t in KHONG_VECTO]
        debai = (r"Which of the following quantities is a "
                 r"\textbf{vector} quantity, that is, one that needs both magnitude and direction to describe it?")
        giai = (r"A vector quantity is a quantity that must be described by \textbf{both magnitude "
                r"and direction}; a scalar quantity needs only magnitude."
                "\\\\\n"
                r"``%s'' requires a specified direction to be fully determined, so it is a vector "
                r"quantity." % LA_VECTO[i] +
                "\\\\\n"
                r"Temperature, mass, time, and area need only one number to "
                r"measure, so they are scalar quantities.")
        cauTN += _MC_khong_cham(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# =====================================================================
# BÀI 8. TỔNG VÀ HIỆU CỦA HAI VECTƠ
# =====================================================================

def L10_C4_B8_TH040_MC_A_01(socau, dang=1):
    """Tổng hai vectơ theo quy tắc ba điểm.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO_DIEM = [("M", "N", "P"), ("A", "B", "C"), ("X", "Y", "Z"),
               ("D", "E", "F")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_DIEM))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO_DIEM):
            break

    cauTN = ""
    for i in gt:
        X, Y, Z = BO_DIEM[i]
        dung = r"$%s + %s = %s$" % (_vt(X, Y), _vt(Y, Z), _vt(X, Z))
        nhieu = [r"$%s + %s = %s$" % (_vt(X, Y), _vt(Y, Z), _vt(Z, X)),
                 r"$%s + %s = %s$" % (_vt(X, Y), _vt(X, Z), _vt(Y, Z)),
                 r"$%s + %s = %s$" % (_vt(Y, X), _vt(Y, Z), _vt(X, Z)),
                 r"$%s + %s = %s$" % (_vt(X, Y), _vt(Z, Y), _vt(X, Z))]
        debai = (r"For any three points $%s$, $%s$, $%s$, which of the following "
                 r"statements is \textbf{true}?" % (X, Y, Z))
        giai = (r"Triangle rule (Chasles' rule): for any three points, the vector whose initial point is "
                r"the first point and whose terminal point is the third point equals the sum of the two "
                r"vectors passing through the middle point:"
                "\\\\\n"
                r"$%s + %s = %s$." % (_vt(X, Y), _vt(Y, Z), _vt(X, Z)) +
                "\\\\\n"
                r"The key point is that the terminal point of the first vector must "
                r"coincide with the initial point of the second vector (here, point "
                r"$%s$)." % Y)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B8_TH040_MC_B_01(socau, dang=1):
    """Tổng hai vectơ theo quy tắc hình bình hành - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO_TEN = ["ABCD", "MNPQ"]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_TEN))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO_TEN):
            break

    cauTN = ""
    for i in gt:
        ten = BO_TEN[i]
        A, B, C, D = ten
        hinh = _hinh_tu_giac(ten, [(1, 2.2), (4.6, 2.2), (3.6, 0), (0, 0)])
        dung = r"$%s$" % _vt(A, C)
        nhieu = [r"$%s$" % _vt(B, D), r"$%s$" % _vt(C, A),
                 r"$%s$" % _vt(D, B), r"$%s$" % _vt(A, B)]
        debai = (r"Given parallelogram $%s$ as shown in the figure. The sum "
                 r"$%s + %s$ equals which of the following vectors?"
                 % (ten, _vt(A, B), _vt(A, D)))
        giai = (r"Parallelogram rule: if $%s%s%s%s$ is a parallelogram, "
                r"then the sum of two vectors starting from the same vertex $%s$ is the "
                r"diagonal vector also starting from $%s$:" % (A, B, C, D, A, A) +
                "\\\\\n"
                r"$%s + %s = %s$." % (_vt(A, B), _vt(A, D), _vt(A, C)) +
                "\\\\\n"
                r"This can be checked with the triangle rule: $%s = %s$, so "
                r"$%s + %s = %s + %s = %s$."
                % (_vt(A, D), _vt(B, C), _vt(A, B), _vt(A, D),
                   _vt(A, B), _vt(B, C), _vt(A, C)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B8_TH041_MC_A_01(socau, dang=1):
    """Hiệu hai vectơ, quy tắc trừ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO_DIEM = [("M", "A", "B"), ("O", "A", "B"), ("I", "X", "Y"),
               ("O", "M", "N")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_DIEM))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO_DIEM):
            break

    cauTN = ""
    for i in gt:
        O, X, Y = BO_DIEM[i]
        dung = r"$%s$" % _vt(Y, X)
        nhieu = [r"$%s$" % _vt(X, Y), r"$%s$" % _vt(O, X),
                 r"$%s$" % _vt(O, Y), r"$\overrightarrow{0}$"]
        debai = (r"For any three points $%s$, $%s$, $%s$, the difference $%s - %s$ "
                 r"equals which of the following vectors?" % (O, X, Y, _vt(O, X), _vt(O, Y)))
        giai = (r"Subtraction rule (difference rule): if two vectors have a \textbf{common "
                r"initial point}, then their difference is the vector joining the two terminal points, "
                r"directed from the terminal point of the subtrahend to the terminal point of the "
                r"minuend:"
                "\\\\\n"
                r"$%s - %s = %s$." % (_vt(O, X), _vt(O, Y), _vt(Y, X)) +
                "\\\\\n"
                r"Check with the triangle rule: "
                r"$%s + %s = %s$, so $%s = %s - %s$."
                % (_vt(O, Y), _vt(Y, X), _vt(O, X), _vt(Y, X),
                   _vt(O, X), _vt(O, Y)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B8_TH041_MC_B_01(socau, dang=1):
    r"""Vectơ đối trong hình vuông - CÓ HÌNH VẼ.

    Giữ bài của cô Lan (K10_2_3_1_3_TH): hình vuông, $O$ là giao điểm hai
    đường chéo, hỏi khẳng định nào đúng. Đã kiểm lại: $O$ là trung điểm
    của $AC$ nên $\overrightarrow{OA} + \overrightarrow{OC} =
    \overrightarrow{0}$ - nội dung toán của cô đúng.

    CLAUDE THEM 28/09/2026 (chuyen sang khuon math_type, them hinh va loi
    giai) - co Lan kiem tra lai ID va mo ta.
    """
    BO_TEN = ["ABCD", "MNPQ"]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_TEN))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO_TEN):
            break

    cauTN = ""
    for i in gt:
        ten = BO_TEN[i]
        A, B, C, D = ten
        O = "O"
        them = ("\\coordinate (%s) at (1.6,1.6);\n" % O +
                "\\draw (%s) -- (%s);\n" % (A, C) +
                "\\draw (%s) -- (%s);\n" % (B, D) +
                "\\fill[black] (%s) circle[radius=1.4pt] node[below right]"
                "{\\footnotesize $%s$};\n" % (O, O))
        hinh = _hinh_tu_giac(ten, [(0, 3.2), (3.2, 3.2), (3.2, 0), (0, 0)],
                             them)

        dung = r"$%s + %s = \overrightarrow{0}$" % (_vt(O, A), _vt(O, C))
        nhieu = [r"$%s + %s = \overrightarrow{0}$" % (_vt(O, A), _vt(O, B)),
                 r"$%s + %s = \overrightarrow{0}$" % (_vt(A, O), _vt(O, C)),
                 r"$%s + %s + %s = \overrightarrow{0}$"
                 % (_vt(O, A), _vt(O, B), _vt(A, B))]
        debai = (r"Let $%s$ be a square and let $%s$ be the intersection of its two "
                 r"diagonals (see figure). Which of the following statements is "
                 r"\textbf{true}?" % (ten, O))
        giai = (r"The two diagonals of a square intersect at the midpoint of each "
                r"diagonal, so $%s$ is the midpoint of $%s$." % (O, A + C) +
                "\\\\\n"
                r"Hence $%s$ and $%s$ are \textbf{opposite} vectors (same length, opposite "
                r"direction), so $%s + %s = \overrightarrow{0}$."
                % (_vt(O, A), _vt(O, C), _vt(O, A), _vt(O, C)) +
                "\\\\\n"
                r"The remaining statements are all false: $%s$ and $%s$ are not "
                r"collinear; $%s + %s = %s \ne \overrightarrow{0}$; and "
                r"$%s + %s + %s = 2%s \ne \overrightarrow{0}$ because "
                r"$%s = %s - %s$."
                % (_vt(O, A), _vt(O, B), _vt(A, O), _vt(O, C), _vt(A, C),
                   _vt(O, A), _vt(O, B), _vt(A, B), _vt(O, B),
                   _vt(A, B), _vt(O, B), _vt(O, A)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B8_TH042_MC_A_01(socau, dang=1):
    """Tính chất giao hoán, kết hợp của phép cộng vectơ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    c = r"\overrightarrow{c}"
    kh = r"\overrightarrow{0}"
    DUNG = [
        (r"$%s + %s = %s + %s$" % (a, b, b, a),
         r"the \textbf{commutative} property of vector addition"),
        (r"$\left(%s + %s\right) + %s = %s + \left(%s + %s\right)$"
         % (a, b, c, a, b, c),
         r"the \textbf{associative} property of vector addition"),
        (r"$%s + %s = %s$" % (a, kh, a),
         r"the zero vector is the \textbf{identity} element of vector addition"),
    ]
    SAI = [
        r"$%s + %s = %s - %s$" % (a, b, b, a),
        r"$\left(%s + %s\right) + %s = %s + \left(%s - %s\right)$"
        % (a, b, c, a, b, c),
        r"$%s + %s = %s$" % (a, kh, kh),
        r"$%s - %s = %s - %s$" % (a, b, b, a),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(DUNG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(DUNG):
            break

    cauTN = ""
    for i in gt:
        dung, ten_tc = DUNG[i]
        nhieu = list(SAI)
        debai = (r"Given three arbitrary vectors $%s$, $%s$, $%s$. Which of the following statements is "
                 r"\textbf{true}?" % (a, b, c))
        giai = (r"Statement $%s$ is exactly %s."
                % (dung.strip("$"), ten_tc) +
                "\\\\\n"
                r"The remaining statements are all false. Note that $%s - %s$ and "
                r"$%s - %s$ are \textbf{opposite} vectors, not equal vectors, and "
                r"$%s + %s = %s$, not $%s$."
                % (a, b, b, a, a, kh, a, kh))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# =====================================================================
# BÀI 9. TÍCH CỦA MỘT VECTƠ VỚI MỘT SỐ
# =====================================================================

def L10_C4_B9_TH043_MC_A_01(socau, dang=1):
    r"""Tích của một số với một vectơ - độ dài và hướng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    gt = []
    while len(gt) < socau:
        k = random.choice([-4, -3, -2, 2, 3, 4])
        if k not in gt:
            gt.append(k)
        if len(gt) >= 6:
            break

    cauTN = ""
    for k in gt:
        huong = "same direction" if k > 0 else "opposite direction"
        huong_sai = "opposite direction" if k > 0 else "same direction"
        dung = (r"$%d%s$ is in the %s relative to $%s$ and has magnitude $%d\left|%s\right|$"
                % (k, a, huong, a, abs(k), a))
        nhieu = [
            r"$%d%s$ is in the %s relative to $%s$ and has magnitude $%d\left|%s\right|$"
            % (k, a, huong_sai, a, abs(k), a),
            r"$%d%s$ is in the %s relative to $%s$ and has magnitude $%d\left|%s\right|$"
            % (k, a, huong, a, abs(k) + 1, a),
            r"$%d%s$ is in the %s relative to $%s$ and has length equal to $\left|%s\right|$"
            % (k, a, huong_sai, a, a),
        ]
        debai = (r"Given a vector $%s \ne \overrightarrow{0}$. Which of the following statements "
                 r"is \textbf{true}?" % a)
        giai = (r"For a real number $k \ne 0$ and a vector $%s \ne \overrightarrow{0}$, "
                r"the vector $k%s$ has:" % (a, a) +
                "\\\\\n"
                r"$\bullet$ \textbf{direction}: same direction as $%s$ if $k > 0$, "
                r"opposite direction to $%s$ if $k < 0$;" % (a, a) +
                "\\\\\n"
                r"$\bullet$ \textbf{magnitude}: "
                r"$\left|k%s\right| = \left|k\right|\cdot\left|%s\right|$."
                % (a, a) +
                "\\\\\n"
                r"Here $k = %d$, so $%d%s$ points in the %s relative to $%s$ and has magnitude "
                r"$\left|%d\right|\cdot\left|%s\right| = %d\left|%s\right|$."
                % (k, k, a, huong, a, k, a, abs(k), a))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B9_TH044_MC_A_01(socau, dang=1):
    """Tính chất của phép nhân một số với một vectơ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    DUNG = [
        (r"$k\left(%s + %s\right) = k%s + k%s$" % (a, b, a, b),
         r"the fact that multiplying a number by a vector is "
         r"\textbf{distributive} over vector addition"),
        (r"$\left(k + l\right)%s = k%s + l%s$" % (a, a, a),
         r"multiplying a number by a vector is \textbf{distributive} over "
         r"addition of numbers"),
        (r"$k\left(l%s\right) = \left(kl\right)%s$" % (a, a),
         r"the \textbf{associative} property of multiplying a number by a " r"vector"),
    ]
    SAI = [
        r"$k\left(%s + %s\right) = k%s + %s$" % (a, b, a, b),
        r"$\left(k + l\right)%s = kl%s$" % (a, a),
        r"$k\left(l%s\right) = \left(k + l\right)%s$" % (a, a),
        r"$k\left(%s - %s\right) = k%s + k%s$" % (a, b, a, b),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(DUNG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(DUNG):
            break

    cauTN = ""
    for i in gt:
        dung, ten_tc = DUNG[i]
        debai = (r"Given two vectors $%s$, $%s$ and two real numbers $k$, $l$. Which of the following "
                 r"statements is \textbf{true}?" % (a, b))
        giai = (r"Statement $%s$ is exactly %s." % (dung.strip("$"), ten_tc) +
                "\\\\\n"
                r"The other statements are false because they omit the factor $k$ in some "
                r"terms, or confuse addition of numbers with multiplication of numbers, or "
                r"do not change the sign when distributing over a difference.")
        cauTN += MC_SA_answer_text(debai, dung, list(SAI), giai, 0, 0, dang)
    return cauTN


def L10_C4_B9_TH045_MC_A_01(socau, dang=1):
    """Điều kiện để hai vectơ cùng phương.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    kh = r"\overrightarrow{0}"
    dung = (r"There exists a real number $k$ such that $%s = k%s$" % (b, a))
    nhieu = [r"There exists a real number $k > 0$ such that $%s = k%s$" % (b, a),
             r"$\left|%s\right| = \left|%s\right|$" % (a, b),
             r"$%s + %s = %s$" % (a, b, kh),
             r"There exists a real number $k$ such that $%s = k%s$ and $k > 1$" % (b, a)]

    cauTN = ""
    for _ in range(socau):
        debai = (r"Given a vector $%s \ne %s$ and an arbitrary vector $%s$. Vectors $%s$ "
                 r"and $%s$ are collinear if and only if which of the following conditions "
                 r"holds?" % (a, kh, b, a, b))
        giai = (r"Collinearity condition: for $%s \ne %s$, two vectors $%s$ and "
                r"$%s$ are collinear if and only if there exists a real number $k$ such that "
                r"$%s = k%s$." % (a, kh, a, b, b, a) +
                "\\\\\n"
                r"We cannot require $k > 0$: when $k < 0$ the two vectors have the "
                r"opposite direction but are \textbf{still collinear}. We also "
                r"cannot require $k > 1$."
                "\\\\\n"
                r"The condition $\left|%s\right| = \left|%s\right|$ only concerns "
                r"length and says nothing about direction; whereas $%s + %s = %s$ "
                r"is the condition for two vectors to be \textbf{opposite}, which "
                r"is much stronger."
                % (a, b, a, b, kh))
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), giai, 0, 0, dang)
    return cauTN


def L10_C4_B9_TH046_MC_A_01(socau, dang=1):
    """Chứng minh ba điểm thẳng hàng bằng vectơ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        # A, B, C với AB = k*AC, chọn k hữu tỉ đẹp
        xa, ya = random.randint(-4, 2), random.randint(-4, 2)
        u, v = random.randint(1, 3), random.randint(1, 3)
        k = random.choice([2, 3, -2])
        v0 = (xa, ya, u, v, k)
        if v0 not in gt:
            gt.append(v0)

    cauTN = ""
    for xa, ya, u, v, k in gt:
        # AC = (u; v), AB = k * AC
        xc, yc = xa + u, ya + v
        xb, yb = xa + k * u, ya + k * v
        dung = r"$%s = %d\,%s$" % (_vt("A", "B"), k, _vt("A", "C"))
        nhieu = [r"$%s = %d\,%s$" % (_vt("A", "B"), k + 1, _vt("A", "C")),
                 r"$%s = %d\,%s$" % (_vt("A", "B"), -k, _vt("A", "C")),
                 r"$%s = %d\,%s$" % (_vt("A", "C"), k, _vt("A", "B")),
                 r"$%s = %d\,%s$" % (_vt("B", "C"), k, _vt("A", "C"))]
        debai = (r"In the coordinate plane $Oxy$, given three points "
                 r"$A%s$, $B%s$, $C%s$. Which of the following statements is \textbf{true}, "
                 r"from which we conclude that $A$, $B$, $C$ are collinear?"
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$ and $%s = %s$."
                % (_vt("A", "B"), _toado(xb - xa, yb - ya),
                   _vt("A", "C"), _toado(xc - xa, yc - ya)) +
                "\\\\\n"
                r"Note that $%s = %d\cdot %s$ and $%s = %d\cdot %s$, so "
                r"$%s = %d\,%s$."
                % (_xx4(xb - xa), k, _xx4(xc - xa),
                   _xx4(yb - ya), k, _xx4(yc - ya),
                   _vt("A", "B"), k, _vt("A", "C")) +
                "\\\\\n"
                r"The vectors $%s$, $%s$ are collinear and share the initial point $A$, "
                r"so the three points $A$, $B$, $C$ are collinear."
                % (_vt("A", "B"), _vt("A", "C")))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B9_TH046_TL_A_01(socau, dong=1):
    """Tự luận: chứng minh ba điểm thẳng hàng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa, ya = random.randint(-3, 2), random.randint(-3, 2)
        u, v = random.randint(1, 3), random.randint(1, 3)
        k = random.choice([2, 3, -2])
        v0 = (xa, ya, u, v, k)
        if v0 not in gt:
            gt.append(v0)

    cauTN = ""
    for xa, ya, u, v, k in gt:
        xc, yc = xa + u, ya + v
        xb, yb = xa + k * u, ya + k * v

        debai = (r"In the coordinate plane $Oxy$, given three points "
                 r"$A%s$, $B%s$, $C%s$."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))

        hoi_a = r"Find the coordinates of the two vectors $%s$ and $%s$." % (
            _vt("A", "B"), _vt("A", "C"))
        giai_a = (r"The coordinates of a vector equal the coordinates of the terminal point minus those of the initial point:"
                  "\\\\\n"
                  r"$%s = %s$; $%s = %s$."
                  % (_vt("A", "B"), _toado(xb - xa, yb - ya),
                     _vt("A", "C"), _toado(xc - xa, yc - ya)))

        hoi_b = r"Prove that the three points $A$, $B$, $C$ are collinear."
        giai_b = (r"We see that $%s = %d\,%s$ because $%s = %d\cdot %s$ and "
                  r"$%s = %d\cdot %s$."
                  % (_vt("A", "B"), k, _vt("A", "C"),
                     _xx4(xb - xa), k, _xx4(xc - xa),
                     _xx4(yb - ya), k, _xx4(yc - ya)) +
                  "\\\\\n"
                  r"Hence $%s$ and $%s$ are collinear and share the initial point $A$, "
                  r"so the three points $A$, $B$, $C$ are collinear."
                  % (_vt("A", "B"), _vt("A", "C")))

        ds_abcd = [(hoi_a, r"%s = %s,\ %s = %s"
                    % (_vt("A", "B"), _toado(xb - xa, yb - ya).replace("\\left", "").replace("\\right", ""),
                       _vt("A", "C"), _toado(xc - xa, yc - ya).replace("\\left", "").replace("\\right", "")),
                    giai_a),
                   (hoi_b, r"%s = %d\,%s" % (_vt("A", "B"), k, _vt("A", "C")),
                    giai_b)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C4_B9_TH047_MC_A_01(socau, dang=1):
    """Đẳng thức vectơ về trung điểm đoạn thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO = [("I", "A", "B", "M"), ("J", "X", "Y", "N"), ("K", "P", "Q", "O")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        kieu = random.choice([0, 1])
        if (i, kieu) not in gt:
            gt.append((i, kieu))
        if len(gt) >= 2 * len(BO):
            break

    cauTN = ""
    for i, kieu in gt:
        I, A, B, M = BO[i]
        kh = r"\overrightarrow{0}"
        if kieu == 0:
            dung = r"$%s + %s = %s$" % (_vt(I, A), _vt(I, B), kh)
            nhieu = [r"$%s + %s = %s$" % (_vt(A, I), _vt(I, B), kh),
                     r"$%s - %s = %s$" % (_vt(I, A), _vt(I, B), kh),
                     r"$%s + %s = 2%s$" % (_vt(I, A), _vt(I, B), _vt(I, A))]
            them = (r"Since $%s$ is the midpoint of $%s$, $%s$ and $%s$ are opposite "
                    r"vectors, so $%s + %s = %s$."
                    % (I, A + B, _vt(I, A), _vt(I, B),
                       _vt(I, A), _vt(I, B), kh))
        else:
            dung = r"$%s + %s = 2%s$" % (_vt(M, A), _vt(M, B), _vt(M, I))
            nhieu = [r"$%s + %s = %s$" % (_vt(M, A), _vt(M, B), _vt(M, I)),
                     r"$%s + %s = 3%s$" % (_vt(M, A), _vt(M, B), _vt(M, I)),
                     r"$%s + %s = 2%s$" % (_vt(M, A), _vt(M, B), _vt(A, B))]
            them = (r"For any point $%s$: $%s = %s + %s$ and "
                    r"$%s = %s + %s$." % (M, _vt(M, A), _vt(M, I), _vt(I, A),
                                          _vt(M, B), _vt(M, I), _vt(I, B)) +
                    "\\\\\n"
                    r"Adding: $%s + %s = 2%s + \left(%s + %s\right) "
                    r"= 2%s + %s = 2%s$."
                    % (_vt(M, A), _vt(M, B), _vt(M, I), _vt(I, A), _vt(I, B),
                       _vt(M, I), kh, _vt(M, I)))

        debai = (r"Let $%s$ be the midpoint of segment $%s$ and let $%s$ be any "
                 r"point. Which of the following statements is \textbf{true}?"
                 % (I, A + B, M))
        giai = them
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B9_TH048_MC_A_01(socau, dang=1):
    r"""Đẳng thức vectơ về trọng tâm tam giác - CÓ HÌNH VẼ.

    Giữ ý bài của cô Lan (K10_2_3_1_4_TH): tam giác với trọng tâm $G$ và
    trung điểm $I$ của cạnh đối. Đã kiểm lại bằng toạ độ:
    $AG = 2GI$ nên $\left|\overrightarrow{AG}\right| =
    2\left|\overrightarrow{IG}\right|$ - nội dung của cô đúng.

    CLAUDE THEM 28/09/2026 (chuyen sang khuon math_type, them hinh va loi
    giai) - co Lan kiem tra lai ID va mo ta.
    """
    BO = [("ABC", "G", "I"), ("XYZ", "G", "I"), ("MNP", "G", "I")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        kieu = random.choice([0, 1])
        if (i, kieu) not in gt:
            gt.append((i, kieu))
        if len(gt) >= 2 * len(BO):
            break

    cauTN = ""
    for i, kieu in gt:
        ten, G, I = BO[i]
        A, B, C = ten
        kh = r"\overrightarrow{0}"
        hinh = _hinh_tam_giac_trong_tam(ten, G, I)

        if kieu == 0:
            dung = r"$%s + %s + %s = %s$" % (_vt(G, A), _vt(G, B),
                                             _vt(G, C), kh)
            nhieu = [r"$%s + %s + %s = %s$" % (_vt(A, G), _vt(G, B),
                                               _vt(G, C), kh),
                     r"$%s + %s + %s = 3%s$" % (_vt(G, A), _vt(G, B),
                                                _vt(G, C), _vt(G, A)),
                     r"$%s + %s = %s$" % (_vt(G, B), _vt(G, C), kh)]
            giai = (r"Centroid property: $%s$ is the centroid of triangle $%s$ "
                    r"if and only if $%s + %s + %s = %s$."
                    % (G, ten, _vt(G, A), _vt(G, B), _vt(G, C), kh) +
                    "\\\\\n"
                    r"Indeed, let $%s$ be the midpoint of $%s$; then $%s + %s = 2%s$, "
                    r"while $%s = -2%s$ (since $%s$ lies on $%s$ with $%s = 2%s$), so "
                    r"the sum of the three vectors equals $%s$."
                    % (I, B + C, _vt(G, B), _vt(G, C), _vt(G, I),
                       _vt(G, A), _vt(G, I), G, A + I,
                       _vt(A, G), _vt(G, I), kh))
        else:
            dung = (r"$\left|%s\right| = 2\left|%s\right|$"
                    % (_vt(A, G), _vt(I, G)))
            nhieu = [r"$\left|%s\right| = 3\left|%s\right|$"
                     % (_vt(A, I), _vt(A, G)),
                     r"$\left|%s\right| = \left|%s\right|$"
                     % (_vt(G, A), _vt(G, I)),
                     r"$\left|%s\right| = 2\left|%s\right|$"
                     % (_vt(I, A), _vt(I, G))]
            giai = (r"The centroid $%s$ lies on the median $%s$ and divides the "
                    r"median in the ratio $%s = \dfrac{2}{3}%s$, "
                    r"$%s = \dfrac{1}{3}%s$." % (G, A + I, _vt(A, G),
                                                 _vt(A, I), _vt(G, I),
                                                 _vt(A, I)) +
                    "\\\\\n"
                    r"Therefore $\left|%s\right| = 2\left|%s\right| = "
                    r"2\left|%s\right|$."
                    % (_vt(A, G), _vt(G, I), _vt(I, G)) +
                    "\\\\\n"
                    r"The other statements are false: $\left|%s\right| = "
                    r"\dfrac{3}{2}\left|%s\right|$ rather than $3$ times; "
                    r"$\left|%s\right| = 2\left|%s\right|$ rather than being "
                    r"equal; and $\left|%s\right| = 3\left|%s\right|$."
                    % (_vt(A, I), _vt(A, G), _vt(G, A), _vt(G, I),
                       _vt(I, A), _vt(I, G)))

        debai = (r"Given triangle $%s$ with centroid $%s$; let $%s$ be the "
                 r"midpoint of side $%s$ (see the figure). Which of the following statements is "
                 r"\textbf{true}?" % (ten, G, I, B + C))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B9_TH048_SA_A_01(socau):
    r"""Phân tích vectơ theo trọng tâm - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đáp số là SỐ NGUYÊN để câu trả lời ngắn chấm được bằng so khớp chuỗi.
    """
    BO = [("ABC", "G", "M"), ("XYZ", "G", "M"), ("MNP", "G", "O")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO):
            break

    cau = ""
    for i in gt:
        ten, G, M = BO[i]
        A, B, C = ten
        kq = 3
        debai = (r"Given triangle $%s$ with centroid $%s$ and an arbitrary point "
                 r"$%s$. Suppose that $%s + %s + %s = k\,%s$ for every position of "
                 r"point $%s$. Find the number $k$."
                 % (ten, G, M, _vt(M, A), _vt(M, B), _vt(M, C),
                    _vt(M, G), M))
        giai = (r"Using the triangle rule, insert point $%s$ into each vector:" % G +
                "\\\\\n"
                r"$%s = %s + %s$; $%s = %s + %s$; $%s = %s + %s$."
                % (_vt(M, A), _vt(M, G), _vt(G, A),
                   _vt(M, B), _vt(M, G), _vt(G, B),
                   _vt(M, C), _vt(M, G), _vt(G, C)) +
                "\\\\\n"
                r"Adding the three equalities: $%s + %s + %s = 3%s + \left(%s + %s + "
                r"%s\right)$."
                % (_vt(M, A), _vt(M, B), _vt(M, C), _vt(M, G),
                   _vt(G, A), _vt(G, B), _vt(G, C)) +
                "\\\\\n"
                r"Since $%s$ is the centroid, $%s + %s + %s = "
                r"\overrightarrow{0}$."
                % (G, _vt(G, A), _vt(G, B), _vt(G, C)) +
                "\\\\\n"
                r"Hence $%s + %s + %s = 3%s$, that is, $k = 3$."
                % (_vt(M, A), _vt(M, B), _vt(M, C), _vt(M, G)))
        nhieu = _ba_nhieu4(kq, [2, 1, -3, 6], buoc=lambda t: kq + 3 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


# =====================================================================
# BÀI 10. VECTƠ TRONG MẶT PHẲNG TOẠ ĐỘ
# =====================================================================

# Bộ ba Pytago, dùng khi cần ĐỘ DÀI RA SỐ NGUYÊN (câu trả lời ngắn chấm
# bằng so khớp chuỗi nên không để đáp số là căn thức hay số vô hạn).
BO_BA_PYTAGO4 = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17),
                 (9, 12, 15), (7, 24, 25), (20, 21, 29)]


def L10_C4_B10_NB049_MC_A_01(socau, dang=1):
    r"""Nhận ra toạ độ của vectơ trong hệ trục toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    i = r"\overrightarrow{i}"
    j = r"\overrightarrow{j}"
    u = r"\overrightarrow{u}"
    gt = []
    while len(gt) < socau:
        p = random.randint(-5, 5)
        q = random.randint(-5, 5)
        if p == 0 or q == 0 or p == q or (p, q) in gt:
            continue
        gt.append((p, q))

    cauTN = ""
    for p, q in gt:
        dung = r"$%s = %s$" % (u, _toado(p, q))
        nhieu = [r"$%s = %s$" % (u, _toado(q, p)),
                 r"$%s = %s$" % (u, _toado(-p, q)),
                 r"$%s = %s$" % (u, _toado(p, -q)),
                 r"$%s = %s$" % (u, _toado(-p, -q))]
        # SUA 29/09/2026: truoc in "-5\vec i - 1\vec j" (he so 1) -> dung _bt_ij
        debai = (r"In the coordinate plane $Oxy$ with two unit vectors $%s$, $%s$, "
                 r"let vector $%s = %s$. Which of the following statements is "
                 r"\textbf{true}?" % (i, j, u, _bt_ij(p, q)))
        giai = (r"If $%s = x%s + y%s$, then the ordered pair $\left(x;\ y\right)$ is called "
                r"the \textbf{coordinates} of $%s$, written $%s = \left(x;\ y\right)$."
                % (u, i, j, u, u) +
                "\\\\\n"
                r"Here the coefficient of $%s$ is $%d$ and the coefficient of $%s$ is $%d$, so "
                r"$%s = %s$." % (i, p, j, q, u, _toado(p, q)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN



def L10_C4_B10_NB049_MC_A_02(socau, dang=1):
    r"""Nhận ra toạ độ của vectơ - HỎI NGƯỢC: cho toạ độ, chọn cách biểu
    diễn qua hai vectơ đơn vị.

    CLAUDE THEM 29/09/2026 - bien the 02, cung dang voi _01 (mapping:
    "Nhan ra toa do cua vecto trong he truc toa do"), khac loi dan: _01
    cho u = xi + yj hoi toa do; _02 cho toa do hoi bieu dien. Co Lan duyet.
    """
    i = r"\overrightarrow{i}"
    j = r"\overrightarrow{j}"
    gt = []
    while len(gt) < socau:
        p = random.randint(-6, 6)
        q = random.randint(-6, 6)
        if 0 in (p, q) or abs(p) == abs(q) or (p, q) in gt:
            continue
        gt.append((p, q))

    cauTN = ""
    for p, q in gt:
        ten = random.choice(["a", "u", "v", "m"])
        vt = r"\overrightarrow{%s}" % ten
        dung = r"$%s = %s$" % (vt, _bt_ij(p, q))
        nhieu = _ba_nhieu4(dung, [
            r"$%s = %s$" % (vt, _bt_ij(q, p)),      # dao thu tu hoanh/tung
            r"$%s = %s$" % (vt, _bt_ij(p, -q)),
            r"$%s = %s$" % (vt, _bt_ij(-p, q)),
            r"$%s = %s$" % (vt, _bt_ij(-p, -q))])
        debai = (r"In the coordinate plane $Oxy$ with two unit vectors $%s$, $%s$, "
                 r"given the vector $%s = %s$. Which of the following statements is \textbf{true}?"
                 % (i, j, vt, _toado(p, q)))
        giai = (r"By definition, $%s = \left(x;\ y\right)$ if and only if "
                r"$%s = x%s + y%s$: the x-coordinate is the coefficient of $%s$, the y-coordinate is the "
                r"coefficient of $%s$." % (vt, vt, i, j, i, j) +
                "\\\\\n"
                r"Since $%s = %s$, we have $%s = %s$." % (vt, _toado(p, q), vt, _bt_ij(p, q)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_NB049_MC_A_03(socau, dang=1):
    r"""Nhận ra toạ độ của vectơ - vectơ viết thiếu một thành phần hoặc viết
    đảo thứ tự ($3\vec{j}$, $-2\vec{i}$, $4\vec{j} - \vec{i}$...).

    CLAUDE THEM 29/09/2026 - bien the 03, cung dang voi _01. Kiem tra dung
    y "hoanh do la he so cua i, tung do la he so cua j" o cac cach viet de
    nham. Co Lan duyet.
    """
    i = r"\overrightarrow{i}"
    j = r"\overrightarrow{j}"
    gt = []
    while len(gt) < socau:
        kieu = random.choice(["chi_i", "chi_j", "dao"])
        p = random.choice([k for k in range(-6, 7) if k not in (0, 1)])
        q = random.choice([k for k in range(-6, 7) if k not in (0,)])
        if kieu == "chi_i":
            x, y = p, 0
        elif kieu == "chi_j":
            x, y = 0, p
        else:
            x, y = p, q
            if abs(x) == abs(y):
                continue
        if (kieu, x, y) not in gt:
            gt.append((kieu, x, y))

    cauTN = ""
    for kieu, x, y in gt:
        ten = random.choice(["a", "b", "u", "w"])
        vt = r"\overrightarrow{%s}" % ten
        if kieu == "dao":
            # viet hang tu j TRUOC: y.j + x.i
            bieu_dien = _bt_ij(y, x, i=j, j=i)
        else:
            bieu_dien = _bt_ij(x, y)
        dung = "$%s$" % _toado(x, y)
        ung_vien = ["$%s$" % _toado(y, x)]
        if kieu == "dao":
            ung_vien += ["$%s$" % _toado(-x, y), "$%s$" % _toado(x, -y)]
        else:
            k = x if y == 0 else y
            ung_vien += ["$%s$" % _toado(k, k), "$%s$" % _toado(1, k),
                         "$%s$" % _toado(k, 1)]
        nhieu = _ba_nhieu4(dung, ung_vien)
        debai = (r"In the coordinate plane $Oxy$ with unit vectors $%s$, $%s$, "
                 r"the coordinate pair of the vector $%s = %s$ is" % (i, j, vt, bieu_dien))
        if kieu == "dao":
            them = (r"Rewrite in the correct order: $%s = %s$ (the order of the terms "
                    r"in the sum does not matter)." % (vt, _bt_ij(x, y)))
        elif kieu == "chi_i":
            them = (r"There is no term containing $%s$, that is, the coefficient of $%s$ equals "
                    r"$0$: $%s = %s$." % (j, j, vt, _bt_ij(x, 0) + " + 0" + j))
        else:
            them = (r"There is no term containing $%s$, so the coefficient of $%s$ equals "
                    r"$0$: $%s = 0%s + %s$." % (i, i, vt, i, _bt_ij(0, y)))
        giai = (r"Coordinates of a vector: the x-coordinate is the coefficient of $%s$, "
                r"and the y-coordinate is the coefficient of $%s$." % (i, j) +
                "\\\\\n" + them +
                "\\\\\n"
                r"Therefore, $%s = %s$." % (vt, _toado(x, y)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN

def L10_C4_B10_TH050_MC_A_01(socau, dang=1):
    """Tìm toạ độ vectơ, toạ độ điểm trong hệ trục.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa, ya = random.randint(-5, 5), random.randint(-5, 5)
        xb, yb = random.randint(-5, 5), random.randint(-5, 5)
        if (xa, ya) == (xb, yb) or (xa, ya, xb, yb) in gt:
            continue
        gt.append((xa, ya, xb, yb))

    cauTN = ""
    for xa, ya, xb, yb in gt:
        u, v = xb - xa, yb - ya
        dung = r"$%s$" % _toado(u, v)
        # Qua _ba_nhieu4: bo so suy bien (u = v, hai diem doi xung qua goc...)
        # lam hai phuong an trung nhau -> NhieuTrungError, cau bien thanh
        # o "[THIEU O PYTHON]" trong de. Do duoc 29/09/2026.
        nhieu = _ba_nhieu4(
            dung,
            [r"$%s$" % _toado(-u, -v), r"$%s$" % _toado(xa + xb, ya + yb),
             r"$%s$" % _toado(v, u), r"$%s$" % _toado(xb, yb)],
            buoc=lambda t: r"$%s$" % _toado(u + t, v))
        debai = (r"In the coordinate plane $Oxy$, given two points $A%s$ and $B%s$. "
                 r"The coordinates of vector $%s$ are"
                 % (_toado(xa, ya), _toado(xb, yb), _vt("A", "B")))
        giai = (r"The coordinates of the vector equal the coordinates of the terminal point minus those of the initial point:"
                "\\\\\n"
                r"$%s = \left(x_B - x_A;\ y_B - y_A\right) = "
                r"\left(%d - \left(%d\right);\ %d - \left(%d\right)\right) "
                r"= %s$."
                % (_vt("A", "B"), xb, xa, yb, ya, _toado(u, v)) +
                "\\\\\n"
                r"Note that $%s = %s$ is the \textbf{opposite} vector; do not mix them up."
                % (_vt("B", "A"), _toado(-u, -v)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_TH050_SA_B_01(socau, dang=2):
    """Toạ độ của điểm thoả điều kiện - đỉnh thứ tư của hình bình hành.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chỉ hỏi MỘT số (hoành độ) để câu trả lời ngắn có đúng một đáp án.
    """
    gt = []
    while len(gt) < socau:
        xa, ya = random.randint(-4, 4), random.randint(-4, 4)
        xb, yb = random.randint(-4, 4), random.randint(-4, 4)
        xc, yc = random.randint(-4, 4), random.randint(-4, 4)
        if len({(xa, ya), (xb, yb), (xc, yc)}) < 3:
            continue
        # ba điểm không thẳng hàng
        if (xb - xa) * (yc - ya) - (yb - ya) * (xc - xa) == 0:
            continue
        if (xa, ya, xb, yb, xc, yc) in gt:
            continue
        gt.append((xa, ya, xb, yb, xc, yc))

    cau = ""
    for xa, ya, xb, yb, xc, yc in gt:
        # ABCD là hình bình hành  <=>  AB = DC  <=>  D = A + C - B
        xd, yd = xa + xc - xb, ya + yc - yb
        debai = (r"In the coordinate plane $Oxy$, given three points $A%s$, $B%s$, "
                 r"$C%s$. Find the \textbf{x-coordinate} of point $D$ such that $ABCD$ "
                 r"is a parallelogram."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$ABCD$ is a parallelogram if and only if $%s = %s$."
                % (_vt("A", "B"), _vt("D", "C")) +
                "\\\\\n"
                r"$%s = %s$; $%s = \left(%d - x_D;\ %d - y_D\right)$."
                % (_vt("A", "B"), _toado(xb - xa, yb - ya),
                   _vt("D", "C"), xc, yc) +
                "\\\\\n"
                r"Setting the coordinates equal: $%d - x_D = %d$, so "
                r"$x_D = %d$; similarly $y_D = %d$."
                % (xc, xb - xa, xd, yd) +
                "\\\\\n"
                r"Thus $D%s$, and the x-coordinate of $D$ equals $%d$."
                % (_toado(xd, yd), xd))
        nhieu = _ba_nhieu4(xd, [xa + xb - xc, xb + xc - xa, -xd, xd + 1],
                           buoc=lambda t: xd + 2 * t)
        cau += MC_SA_answer_const(debai, xd, nhieu, giai, 0, 0, dang)
    return cau


def L10_C4_B10_TH051_MC_A_01(socau, dang=1):
    """Tính độ dài vectơ từ toạ độ hai đầu mút.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4)
        if random.choice([True, False]):
            p, q = q, p
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        xa, ya = random.randint(-4, 4), random.randint(-4, 4)
        v = (xa, ya, sx * p, sy * q, r)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for xa, ya, u, v, r in gt:
        xb, yb = xa + u, ya + v
        dung = r"$%d$" % r
        nhieu = [r"$%d$" % (abs(u) + abs(v)), r"$%d$" % (u * u + v * v),
                 r"$%d$" % abs(abs(u) - abs(v)), r"$%d$" % (r + 1)]
        debai = (r"In the coordinate plane $Oxy$, given two points $A%s$ and $B%s$. "
                 r"The length of vector $%s$ equals"
                 % (_toado(xa, ya), _toado(xb, yb), _vt("A", "B")))
        giai = (r"$%s = %s$." % (_vt("A", "B"), _toado(u, v)) +
                "\\\\\n"
                r"If $%s = \left(x;\ y\right)$ then "
                r"$\left|%s\right| = \sqrt{x^2 + y^2}$."
                % (r"\overrightarrow{u}", r"\overrightarrow{u}") +
                "\\\\\n"
                r"Therefore $\left|%s\right| = \sqrt{\left(%d\right)^2 + "
                r"\left(%d\right)^2} = \sqrt{%d} = %d$."
                % (_vt("A", "B"), u, v, u * u + v * v, r))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_TH051_SA_A_01(socau):
    """Độ dài đoạn thẳng theo toạ độ - đáp số nguyên.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4)
        if random.choice([True, False]):
            p, q = q, p
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        xa, ya = random.randint(-5, 5), random.randint(-5, 5)
        v = (xa, ya, sx * p, sy * q, r)
        if v not in gt:
            gt.append(v)

    cau = ""
    for xa, ya, u, v, r in gt:
        xb, yb = xa + u, ya + v
        debai = (r"In the coordinate plane $Oxy$, given two points $A%s$ and $B%s$. "
                 r"Find the length of segment $AB$."
                 % (_toado(xa, ya), _toado(xb, yb)))
        giai = (r"$AB = \left|%s\right|$ where $%s = %s$."
                % (_vt("A", "B"), _vt("A", "B"), _toado(u, v)) +
                "\\\\\n"
                r"$AB = \sqrt{\left(x_B - x_A\right)^2 + "
                r"\left(y_B - y_A\right)^2} = "
                r"\sqrt{\left(%d\right)^2 + \left(%d\right)^2} "
                r"= \sqrt{%d} = %d$."
                % (u, v, u * u + v * v, r))
        nhieu = _ba_nhieu4(r, [abs(u) + abs(v), u * u + v * v,
                               abs(abs(u) - abs(v)), r + 2],
                           buoc=lambda t: r + 3 * t)
        cau += MC_SA_answer_const(debai, r, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B10_TH052_MC_A_01(socau, dang=1):
    """Toạ độ vectơ tổng, hiệu, tích với một số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    u = r"\overrightarrow{u}"
    v = r"\overrightarrow{v}"
    gt = []
    while len(gt) < socau:
        a1, a2 = random.randint(-5, 5), random.randint(-5, 5)
        b1, b2 = random.randint(-5, 5), random.randint(-5, 5)
        m = random.choice([2, 3, -2])
        n = random.choice([1, 2, -1])
        w = (a1, a2, b1, b2, m, n)
        if (a1, a2) == (0, 0) or (b1, b2) == (0, 0) or w in gt:
            continue
        gt.append(w)

    cauTN = ""
    for a1, a2, b1, b2, m, n in gt:
        c1, c2 = m * a1 + n * b1, m * a2 + n * b2
        dung = r"$%s$" % _toado(c1, c2)
        nhieu = _ba_nhieu4(
            dung,
            [r"$%s$" % _toado(m * a1 + n * b1, m * a2 - n * b2),
             r"$%s$" % _toado(m * a1 * n * b1, m * a2 * n * b2),
             r"$%s$" % _toado(a1 + b1, a2 + b2),
             r"$%s$" % _toado(c2, c1)],
            buoc=lambda t: r"$%s$" % _toado(c1 + t, c2))
        dau = "+" if n > 0 else "-"
        he_so_n = "" if abs(n) == 1 else "%d" % abs(n)
        debai = (r"In the coordinate plane $Oxy$, given two vectors $%s = %s$ and "
                 r"$%s = %s$. The coordinates of vector $%d%s %s %s%s$ are"
                 % (u, _toado(a1, a2), v, _toado(b1, b2), m, u, dau,
                    he_so_n, v))
        giai = (r"To multiply a number by a vector, multiply \textbf{each} coordinate; "
                r"to add two vectors, add the corresponding coordinates \textbf{one by one}."
                "\\\\\n"
                r"$%d%s = %s$; $%s%s%s = %s$."
                % (m, u, _toado(m * a1, m * a2), dau, he_so_n, v,
                   _toado(n * b1, n * b2)) +
                "\\\\\n"
                r"Add coordinate by coordinate: $%s$." % _toado(c1, c2))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_TH052_SA_A_01(socau):
    """Toạ độ vectơ sau phép toán - hỏi MỘT thành phần.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    u = r"\overrightarrow{u}"
    v = r"\overrightarrow{v}"
    gt = []
    while len(gt) < socau:
        a1, a2 = random.randint(-5, 5), random.randint(-5, 5)
        b1, b2 = random.randint(-5, 5), random.randint(-5, 5)
        m = random.choice([2, 3, -2])
        w = (a1, a2, b1, b2, m)
        if w in gt:
            continue
        gt.append(w)

    cau = ""
    for a1, a2, b1, b2, m in gt:
        c1 = m * a1 - b1
        debai = (r"In the coordinate plane $Oxy$, given two vectors $%s = %s$ and "
                 r"$%s = %s$. Find the \textbf{x-coordinate} of the vector $%d%s - %s$."
                 % (u, _toado(a1, a2), v, _toado(b1, b2), m, u, v))
        giai = (r"$%d%s = %s$." % (m, u, _toado(m * a1, m * a2)) +
                "\\\\\n"
                r"$%d%s - %s = \left(%d - \left(%d\right);\ "
                r"%d - \left(%d\right)\right) = %s$."
                % (m, u, v, m * a1, b1, m * a2, b2,
                   _toado(c1, m * a2 - b2)) +
                "\\\\\n"
                r"Therefore, the required x-coordinate is $%d$." % c1)
        nhieu = _ba_nhieu4(c1, [m * a1 + b1, a1 - b1, m * a2 - b2, -c1],
                           buoc=lambda t: c1 + 2 * t)
        cau += MC_SA_answer_const(debai, c1, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B10_TH053_MC_A_01(socau, dang=1):
    """Tính tích vô hướng hai vectơ bằng toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    u = r"\overrightarrow{u}"
    v = r"\overrightarrow{v}"
    gt = []
    while len(gt) < socau:
        a1, a2 = random.randint(-5, 5), random.randint(-5, 5)
        b1, b2 = random.randint(-5, 5), random.randint(-5, 5)
        w = (a1, a2, b1, b2)
        if (a1, a2) == (0, 0) or (b1, b2) == (0, 0) or w in gt:
            continue
        gt.append(w)

    cauTN = ""
    for a1, a2, b1, b2 in gt:
        kq = a1 * b1 + a2 * b2
        dung = r"$%d$" % kq
        # phải lọc qua _ba_nhieu4: với một số bộ toạ độ, mấy biểu thức
        # nhiễu dưới đây cho ra CÙNG một số (ví dụ khi a2 = 0) nên nếu
        # truyền thẳng thì math_type báo NhieuTrungError, câu hỏng.
        nhieu = [r"$%d$" % x for x in _ba_nhieu4(
            kq, [a1 * b1 - a2 * b2, a1 * b2 + a2 * b1, a1 * b2 - a2 * b1,
                 kq + 2, kq - 3],
            buoc=lambda t: kq + 5 * t)]
        debai = (r"In the coordinate plane $Oxy$, given two vectors $%s = %s$ and "
                 r"$%s = %s$. The dot product $%s \cdot %s$ equals"
                 % (u, _toado(a1, a2), v, _toado(b1, b2), u, v))
        giai = (r"If $%s = \left(x_1;\ y_1\right)$ and "
                r"$%s = \left(x_2;\ y_2\right)$, then "
                r"$%s \cdot %s = x_1x_2 + y_1y_2$." % (u, v, u, v) +
                "\\\\\n"
                r"$%s \cdot %s = \left(%d\right)\cdot\left(%d\right) + "
                r"\left(%d\right)\cdot\left(%d\right) = %d + %d = %d$."
                % (u, v, a1, b1, a2, b2, a1 * b1, a2 * b2, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_TH053_SA_A_01(socau):
    """Tích vô hướng theo toạ độ - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa, ya = random.randint(-5, 5), random.randint(-5, 5)
        xb, yb = random.randint(-5, 5), random.randint(-5, 5)
        xc, yc = random.randint(-5, 5), random.randint(-5, 5)
        if len({(xa, ya), (xb, yb), (xc, yc)}) < 3:
            continue
        w = (xa, ya, xb, yb, xc, yc)
        if w in gt:
            continue
        gt.append(w)

    cau = ""
    for xa, ya, xb, yb, xc, yc in gt:
        u1, u2 = xb - xa, yb - ya
        v1, v2 = xc - xa, yc - ya
        kq = u1 * v1 + u2 * v2
        debai = (r"In the coordinate plane $Oxy$, given three points $A%s$, $B%s$, "
                 r"$C%s$. Calculate the dot product $%s \cdot %s$."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc),
                    _vt("A", "B"), _vt("A", "C")))
        giai = (r"$%s = %s$; $%s = %s$."
                % (_vt("A", "B"), _toado(u1, u2),
                   _vt("A", "C"), _toado(v1, v2)) +
                "\\\\\n"
                r"$%s \cdot %s = \left(%d\right)\cdot\left(%d\right) + "
                r"\left(%d\right)\cdot\left(%d\right) = %d$."
                % (_vt("A", "B"), _vt("A", "C"), u1, v1, u2, v2, kq))
        nhieu = _ba_nhieu4(kq, [u1 * v1 - u2 * v2, u1 * v2 - u2 * v1,
                                u1 * v2 + u2 * v1, kq + 3],
                           buoc=lambda t: kq + 4 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B10_VD054_MC_A_01(socau, dang=1):
    r"""Bài toán hình học phẳng giải bằng toạ độ - nhận dạng tam giác.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Số liệu dựng từ bộ ba Pytago nên tam giác VUÔNG thật sự, không phải
    vuông "gần đúng" do làm tròn.
    """
    gt = []
    while len(gt) < socau:
        p, q, _r = random.choice(BO_BA_PYTAGO4[:4])
        xa, ya = random.randint(-3, 3), random.randint(-3, 3)
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        w = (xa, ya, sx * p, sy * q)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for xa, ya, u, v in gt:
        # AB = (u; v), AC vuông góc với AB: AC = (-v; u)
        xb, yb = xa + u, ya + v
        xc, yc = xa - v, ya + u
        dung = r"Right isosceles triangle at $A$"
        nhieu = [r"Right triangle at $A$, but not isosceles",
                 r"Triangle isosceles at $A$ but not right",
                 r"Equilateral triangle", r"Triangle with an obtuse angle at $A$"]
        # AB va AC cung do dai nen vuong can
        debai = (r"In the coordinate plane $Oxy$, given three points $A%s$, $B%s$, "
                 r"$C%s$. What type of triangle is $ABC$?"
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$; $%s = %s$."
                % (_vt("A", "B"), _toado(u, v),
                   _vt("A", "C"), _toado(-v, u)) +
                "\\\\\n"
                r"Dot product: $%s \cdot %s = \left(%d\right)\cdot\left(%d\right) + "
                r"\left(%d\right)\cdot\left(%d\right) = 0$ so $%s \perp %s$, and "
                r"the triangle is right-angled at $A$."
                % (_vt("A", "B"), _vt("A", "C"), u, -v, v, u,
                   _vt("A", "B"), _vt("A", "C")) +
                "\\\\\n"
                r"Lengths: $AB = \sqrt{%d} = AC$, so the triangle is also isosceles at $A$."
                % (u * u + v * v) +
                "\\\\\n"
                r"Therefore, triangle $ABC$ is an isosceles right triangle with the right angle at $A$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_VD054_TL_A_01(socau, dong=1):
    """Tự luận: chứng minh tính chất hình học bằng toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4[:4])
        xa, ya = random.randint(-3, 3), random.randint(-3, 3)
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        w = (xa, ya, sx * p, sy * q, r)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for xa, ya, u, v, r in gt:
        xb, yb = xa + u, ya + v
        xc, yc = xa - v, ya + u
        dt = (u * u + v * v) / 2.0

        debai = (r"In the coordinate plane $Oxy$, given three points $A%s$, $B%s$, "
                 r"$C%s$." % (_toado(xa, ya), _toado(xb, yb),
                              _toado(xc, yc)))

        hoi_a = r"Find the coordinates of the two vectors $%s$ and $%s$." % (
            _vt("A", "B"), _vt("A", "C"))
        giai_a = (r"$%s = %s$; $%s = %s$."
                  % (_vt("A", "B"), _toado(u, v),
                     _vt("A", "C"), _toado(-v, u)))

        hoi_b = r"Prove that triangle $ABC$ is right-angled at $A$."
        giai_b = (r"$%s \cdot %s = \left(%d\right)\left(%d\right) + "
                  r"\left(%d\right)\left(%d\right) = 0$."
                  % (_vt("A", "B"), _vt("A", "C"), u, -v, v, u) +
                  "\\\\\n"
                  r"The dot product equals $0$, so $%s \perp %s$, that is, triangle "
                  r"$ABC$ has a right angle at $A$."
                  % (_vt("A", "B"), _vt("A", "C")))

        hoi_c = r"Calculate the area of triangle $ABC$."
        giai_c = (r"$AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} = %d$ "
                  r"and $AC = %d$ (computed similarly)." % (u, v, r, r) +
                  "\\\\\n"
                  r"Since the triangle has a right angle at $A$, "
                  r"$S = \dfrac{1}{2}\cdot AB \cdot AC = "
                  r"\dfrac{1}{2}\cdot %d \cdot %d = %s$ (square units)."
                  % (r, r, _xx4(dt)))

        ds_abcd = [(hoi_a, r"%s = \left(%d;\ %d\right)"
                    % (_vt("A", "B"), u, v), giai_a),
                   (hoi_b, r"%s \cdot %s = 0"
                    % (_vt("A", "B"), _vt("A", "C")), giai_b),
                   (hoi_c, r"S = %s" % _xx4(dt), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C4_B10_VD055_MC_A_01(socau, dang=1):
    """Vị trí của vật trên mặt phẳng toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        x0, y0 = random.randint(-6, 6), random.randint(-6, 6)
        vx, vy = random.randint(-5, 5), random.randint(-5, 5)
        t = random.randint(2, 5)
        if (vx, vy) == (0, 0):
            continue
        w = (x0, y0, vx, vy, t)
        if w in gt:
            continue
        gt.append(w)

    cauTN = ""
    for x0, y0, vx, vy, t in gt:
        x1, y1 = x0 + t * vx, y0 + t * vy
        dung = r"$%s$" % _toado(x1, y1)
        nhieu = [r"$%s$" % _toado(x0 + vx, y0 + vy),
                 r"$%s$" % _toado(t * vx, t * vy),
                 r"$%s$" % _toado(x0 - t * vx, y0 - t * vy),
                 r"$%s$" % _toado(y1, x1)]
        debai = (r"A motorboat starts from position $A%s$ in the coordinate plane "
                 r"$Oxy$ (the unit on each axis is a kilometer) and moves in a "
                 r"straight line at constant velocity $\overrightarrow{v} = %s$ "
                 r"(unit: km/h). After $%d$ h, where is the motorboat?"
                 % (_toado(x0, y0), _toado(vx, vy), t))
        giai = (r"For uniform straight-line motion, the displacement after $%d$ hours is "
                r"$%d\overrightarrow{v} = %s$."
                % (t, t, _toado(t * vx, t * vy)) +
                "\\\\\n"
                r"Let $B$ be the position after $%d$ hours; then $%s = %d\overrightarrow{v}$, "
                r"so the coordinates of $B$ equal the coordinates of $A$ plus the "
                r"displacement:" % (t, _vt("A", "B"), t) +
                "\\\\\n"
                r"$B\left(%d + %d;\ %d + %d\right) = B%s$."
                % (x0, t * vx, y0, t * vy, _toado(x1, y1)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_VD056_MC_A_01(socau, dang=1):
    """Giải tam giác bằng phương pháp toạ độ - tính diện tích.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa, ya = random.randint(-4, 4), random.randint(-4, 4)
        u1, u2 = random.randint(-5, 5), random.randint(-5, 5)
        v1, v2 = random.randint(-5, 5), random.randint(-5, 5)
        d = u1 * v2 - u2 * v1
        if d == 0 or abs(d) % 2 != 0:
            continue
        w = (xa, ya, u1, u2, v1, v2)
        if w in gt:
            continue
        gt.append(w)

    cauTN = ""
    for xa, ya, u1, u2, v1, v2 in gt:
        xb, yb = xa + u1, ya + u2
        xc, yc = xa + v1, ya + v2
        d = u1 * v2 - u2 * v1
        S = abs(d) // 2
        dung = r"$%d$" % S
        nhieu = _ba_nhieu4(
            dung,
            [r"$%d$" % abs(d), r"$%d$" % (abs(u1 * v1 + u2 * v2) // 2 + 1),
             r"$%d$" % (S + 1), r"$%d$" % (S * 2 + 1)],
            buoc=lambda t: r"$%d$" % (S + 1 + t))
        debai = (r"In the coordinate plane $Oxy$, given triangle $ABC$ with "
                 r"$A%s$, $B%s$, $C%s$. The area of triangle $ABC$ equals"
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$; $%s = %s$."
                % (_vt("A", "B"), _toado(u1, u2),
                   _vt("A", "C"), _toado(v1, v2)) +
                "\\\\\n"
                r"For $%s = \left(x_1;\ y_1\right)$, $%s = "
                r"\left(x_2;\ y_2\right)$, the area of the triangle equals"
                % (_vt("A", "B"), _vt("A", "C")) +
                "\\\\\n"
                r"$S = \dfrac{1}{2}\left|x_1y_2 - x_2y_1\right| = "
                r"\dfrac{1}{2}\left|\left(%d\right)\left(%d\right) - "
                r"\left(%d\right)\left(%d\right)\right| = "
                r"\dfrac{1}{2}\cdot %d = %d$."
                % (u1, v2, v1, u2, abs(d), S))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_VD056_TL_A_01(socau, dong=1):
    """Tự luận: tính cạnh, góc, diện tích tam giác bằng toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4[:4])
        xa, ya = random.randint(-3, 3), random.randint(-3, 3)
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        w = (xa, ya, sx * p, sy * q, r)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for xa, ya, u, v, r in gt:
        xb, yb = xa + u, ya + v
        xc, yc = xa - v, ya + u
        dt = (u * u + v * v) / 2.0

        debai = (r"In the coordinate plane $Oxy$, given triangle $ABC$ with "
                 r"$A%s$, $B%s$, $C%s$."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))

        hoi_a = r"Calculate the lengths of the two sides $AB$ and $AC$."
        giai_a = (r"$%s = %s$, so $AB = \sqrt{\left(%d\right)^2 + "
                  r"\left(%d\right)^2} = %d$."
                  % (_vt("A", "B"), _toado(u, v), u, v, r) +
                  "\\\\\n"
                  r"$%s = %s$ so $AC = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} = "
                  r"%d$."
                  % (_vt("A", "C"), _toado(-v, u), -v, u, r))

        hoi_b = r"Calculate the measure of angle $\widehat{BAC}$."
        giai_b = (r"$\cos\widehat{BAC} = \dfrac{%s \cdot %s}"
                  r"{\left|%s\right|\cdot\left|%s\right|} = "
                  r"\dfrac{0}{%d\cdot %d} = 0$."
                  % (_vt("A", "B"), _vt("A", "C"), _vt("A", "B"),
                     _vt("A", "C"), r, r) +
                  "\\\\\n"
                  r"Hence $\widehat{BAC} = 90^{\circ}$.")

        hoi_c = r"Calculate the area of triangle $ABC$."
        giai_c = (r"Since the triangle is right-angled at $A$, "
                  r"$S = \dfrac{1}{2}\cdot AB \cdot AC = "
                  r"\dfrac{1}{2}\cdot %d\cdot %d = %s$." % (r, r, _xx4(dt)))

        ds_abcd = [(hoi_a, r"AB = AC = %d" % r, giai_a),
                   (hoi_b, r"\widehat{BAC} = 90^{\circ}", giai_b),
                   (hoi_c, r"S = %s" % _xx4(dt), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 11. TÍCH VÔ HƯỚNG CỦA HAI VECTƠ
# =====================================================================

# ---------------------------------------------------------------------
# GÓC GIỮA HAI VECTƠ - SỬA 29/09/2026 theo cô Lan: tách theo MỨC ĐỘ
#   NB057_MC_A : hai vectơ CHUNG ĐIỂM ĐẦU (đọc thẳng góc trên hình)
#   TH057_MC_A : hai vectơ KHÔNG chung điểm đầu, không chung điểm cuối
#                (phải dời vectơ / đổi hướng)
#   TH057_MC_B : hai vectơ CHUNG ĐIỂM CUỐI (đổi hướng cả hai vectơ)
# Góc luôn TÍNH TỪ TOẠ ĐỘ (không gõ tay), lời giải sinh theo loại cặp.
# ---------------------------------------------------------------------

_TG_DEU = {"A": (1.5, 2.598076), "B": (0.0, 0.0), "C": (3.0, 0.0), "H": (1.5, 0.0)}
_HV = {"A": (0.0, 3.0), "B": (3.0, 3.0), "C": (3.0, 0.0), "D": (0.0, 0.0),
       "O": (1.5, 1.5)}
_GOC_TG = (0, 30, 60, 90, 120, 150, 180)
_GOC_HV = (0, 45, 90, 135, 180)


def _hinh_tg_deu_H():
    """Tam giác đều ABC, H là trung điểm BC, có đoạn AH."""
    return (
        "\\begin{tikzpicture}[>=stealth,x=1cm,y=1cm,thick,scale=0.95]\n"
        "\\coordinate (A) at (1.5,2.598);\n\\coordinate (B) at (0,0);\n"
        "\\coordinate (C) at (3,0);\n\\coordinate (H) at (1.5,0);\n"
        "\\draw (A) -- (B) -- (C) -- cycle;\n\\draw[dashed] (A) -- (H);\n"
        "\\fill[black] (A) circle[radius=1.4pt] node[above]{\\footnotesize $A$};\n"
        "\\fill[black] (B) circle[radius=1.4pt] node[below left]{\\footnotesize $B$};\n"
        "\\fill[black] (C) circle[radius=1.4pt] node[below right]{\\footnotesize $C$};\n"
        "\\fill[black] (H) circle[radius=1.4pt] node[below]{\\footnotesize $H$};\n"
        "\\end{tikzpicture}")


def _hinh_hv_O():
    """Hình vuông ABCD, O là giao điểm hai đường chéo."""
    them = ("\\draw[thin] (A) -- (C);\n\\draw[thin] (B) -- (D);\n"
            "\\fill[black] (1.5,1.5) circle[radius=1.4pt] node[right=2pt]"
            "{\\footnotesize $O$};\n")
    return _hinh_tu_giac("ABCD", [_HV["A"], _HV["B"], _HV["C"], _HV["D"]], them)


def _goc2(TD, v1, v2):
    x1, y1 = TD[v1[1]][0] - TD[v1[0]][0], TD[v1[1]][1] - TD[v1[0]][1]
    x2, y2 = TD[v2[1]][0] - TD[v2[0]][0], TD[v2[1]][1] - TD[v2[0]][1]
    c = (x1 * x2 + y1 * y2) / math.hypot(x1, y1) / math.hypot(x2, y2)
    return int(round(math.degrees(math.acos(max(-1.0, min(1.0, c))))))


def _goc_ten(P, Q, R, g):
    r"""Tên góc $\widehat{PQR}$ (đỉnh Q) hoặc mô tả khi thẳng hàng."""
    if g == 180:
        return r"$%s$, $%s$, $%s$ are collinear and $%s$ lies between the other two, so the angle equals $180^{\circ}$" % (P, Q, R, Q)
    if g == 0:
        return r"the two vectors have the same direction, so the angle equals $0^{\circ}$"
    return r"$\widehat{%s%s%s} = %d^{\circ}$" % (P, Q, R, g)


def _loi_giai_goc(TD, v1, v2, g, _sau=True):
    """Lời giải theo loại cặp vectơ (chung gốc / chung ngọn / nối đuôi /
    dời vectơ cùng phương / vuông góc). Góc g đã tính từ toạ độ."""
    u, v = _vt(*v1), _vt(*v2)
    diem = list(TD)

    def cung_phuong_tu(goc_diem, mau):
        """Vectơ (goc_diem -> Y) cùng hướng (0) hoặc ngược hướng (180) với mau."""
        for Y in diem:
            if Y == goc_diem:
                continue
            w = (goc_diem, Y)
            gg = _goc2(TD, mau, w)
            if gg in (0, 180):
                return w, gg
        return None, None

    if v1[0] == v2[0]:
        return (r"The two vectors $%s$ and $%s$ share the initial point $%s$, so "
                r"the angle between them is the angle formed by the two rays "
                r"$%s%s$, $%s%s$: %s."
                % (u, v, v1[0], v1[0], v1[1], v2[0], v2[1],
                   _goc_ten(v1[1], v1[0], v2[1], g)))
    if g in (0, 180):
        return (r"The vectors $%s$ and $%s$ point in the %s, so the angle between them equals $%d^{\circ}$."
                % (u, v, r"\textbf{same direction}" if g == 0 else r"\textbf{opposite direction}", g))
    if v1[1] == v2[1]:
        X = v1[1]
        return (r"The two vectors share the \textbf{terminal point} $%s$. Reversing both vectors "
                r"does not change the angle between them: the angle between $%s$, $%s$ equals the angle "
                r"between $%s$, $%s$ - these two vectors share the initial point $%s$."
                % (X, u, v, _vt(X, v1[0]), _vt(X, v2[0]), X) +
                "\\\\\n" + r"Therefore the required angle is %s." % _goc_ten(v1[0], X, v2[0], g))
    if v1[1] == v2[0] or v2[1] == v1[0]:
        # noi duoi: doi huong vecto ket thuc tai diem chung
        if v1[1] == v2[0]:
            X, w1, w2 = v1[1], (v1[1], v1[0]), v2
        else:
            X, w1, w2 = v1[0], v1, (v2[1], v2[0])
        g2 = 180 - g
        doi = u if w1 != v1 else v
        return (r"The two vectors do not yet share an initial point. Reversing $%s$ (to get a vector "
                r"with initial point $%s$) changes the angle between the two vectors to its supplement."
                % (doi, X) + "\\\\\n" +
                r"The angle between $%s$ and $%s$ is %s, so the required angle equals "
                r"$180^{\circ} - %d^{\circ} = %d^{\circ}$."
                % (_vt(*w1), _vt(*w2), _goc_ten(w1[1], X, w2[1], g2), g2, g))
    w, gg = cung_phuong_tu(v1[0], v2)
    if w:
        gw = _goc2(TD, v1, w)
        return (r"The two vectors do not yet share an initial point. Vector $%s$ "
                r"has the %s relative to $%s$ (same initial point $%s$ as $%s$)" % (v, "same direction" if gg == 0 else "opposite direction",
                                              _vt(*w), v1[0], u) +
                (r" so the required angle equals the angle between $%s$ and $%s$: %s."
                 % (u, _vt(*w), _goc_ten(v1[1], v1[0], w[1], g)) if gg == 0 else
                 r" so the required angle equals $180^{\circ}$ minus the angle "
                 r"between $%s$, $%s$, that is, $180^{\circ} - %d^{\circ} = "
                 r"%d^{\circ}$." % (u, _vt(*w), gw, g)))
    w, gg = cung_phuong_tu(v2[0], v1)
    if w:
        gw = _goc2(TD, w, v2)
        return (r"The two vectors do not yet share an initial point. Vector $%s$ "
                r"has the %s relative to $%s$ (same initial point $%s$ as $%s$)" % (u, "same direction" if gg == 0 else "opposite direction",
                                              _vt(*w), v2[0], v) +
                (r" so the required angle equals the angle between $%s$ and $%s$: %s."
                 % (_vt(*w), v, _goc_ten(w[1], v2[0], v2[1], g)) if gg == 0 else
                 r" so the required angle equals $180^{\circ}$ minus the angle "
                 r"between $%s$, $%s$, that is, $180^{\circ} - %d^{\circ} = "
                 r"%d^{\circ}$." % (_vt(*w), v, gw, g)))
    if g == 90:
        return (r"Lines $%s%s$ and $%s%s$ are perpendicular, so the angle between "
                r"the vectors $%s$, $%s$ equals $90^{\circ}$." % (v1[0], v1[1], v2[0], v2[1], u, v))
    if _sau:
        # thay v2 bang vecto cung huong co ten khac roi giai lai
        for Y in diem:
            for Z in diem:
                w = (Y, Z)
                if Y == Z or w == v2 or _goc2(TD, v2, w) != 0:
                    continue
                phu = _loi_giai_goc(TD, v1, w, g, _sau=False)
                if "move" not in phu:
                    return (r"Vector $%s$ has the same direction as $%s$, so the angle between $%s$ and $%s$ "
                            r"equals the angle between $%s$ and $%s$." % (v, _vt(*w), u, v, u, _vt(*w)) +
                            "\\\\\n" + phu)
    return (r"The two vectors do not share an initial point: move $%s$ to the initial point $%s$, then read "
            r"the angle formed, which is $%d^{\circ}$." % (v, v1[0], g))


def _cau_goc_vecto(socau, dang, TD, hinh, ten_hinh, CAP, GOC, tra_loi_ngan=False):
    """tra_loi_ngan=True (CLAUDE THEM 15/10/2026): ban tra loi ngan cung dang - hoi "bang bao nhieu do", dap so la so
    nguyen (khong kem dau do); phan con lai (thu tu ngau nhien, loi giai) giu nguyen nhu ban trac nghiem."""
    ds = list(range(len(CAP)))
    random.shuffle(ds)
    cauTN = ""
    for i in ds[:min(socau, len(CAP))]:
        v1, v2 = CAP[i]
        g = _goc2(TD, v1, v2)
        dung = r"$%d^{\circ}$" % g
        uu_tien = [x for x in (180 - g,) if x != g and x in GOC]
        con = [x for x in GOC if x != g and x not in uu_tien]
        random.shuffle(con)
        nhieu = [r"$%d^{\circ}$" % x for x in (uu_tien + con)[:3]]
        debai = (r"Given %s as shown in the figure. The angle between the vectors $%s$ and $%s$ equals"
                 % (ten_hinh, _vt(*v1), _vt(*v2)))
        giai = _loi_giai_goc(TD, v1, v2, g)
        if tra_loi_ngan:
            debai = (r"Given %s as shown in the figure. What is the angle between the two vectors $%s$ and $%s$ in degrees?"
                     % (ten_hinh, _vt(*v1), _vt(*v2)))
            cauTN += MC_SA_answer_const(debai, str(g), [str(x) for x in (uu_tien + con)[:3]], giai, hinh, 0, dang)
            continue
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


_TEN_TG = r"equilateral triangle $ABC$ in which $H$ is the midpoint of $BC$"
_TEN_HV = r"square $ABCD$ with $O$ the intersection of its two diagonals"


def L10_C4_B11_NB057_MC_A_01(socau, dang=1):
    r"""Góc giữa hai vectơ CHUNG ĐIỂM ĐẦU - tam giác đều (mức NB).

    CLAUDE SUA 29/09/2026 (co Lan: tach theo muc do): chi con cac cap chung
    diem dau, doc thang goc tren hinh. Cap khac diem dau chuyen sang
    L10_C4_B11_TH057_MC_A, cap chung diem cuoi sang TH057_MC_B.
    """
    CAP = [("AB", "AC"), ("BA", "BC"), ("CA", "CB"), ("HB", "HC"),
           ("HA", "HB"), ("HC", "HA"), ("BC", "BA"), ("AC", "AB")]
    return _cau_goc_vecto(socau, dang, _TG_DEU, _hinh_tg_deu_H(), _TEN_TG, CAP, _GOC_TG)


def L10_C4_B11_NB057_MC_A_02(socau, dang=1):
    r"""Góc giữa hai vectơ CHUNG ĐIỂM ĐẦU - hình vuông (mức NB).

    CLAUDE THEM 29/09/2026, sua cung ngay: chi cap chung diem dau.
    """
    CAP = [("AB", "AD"), ("AB", "AC"), ("DA", "DB"), ("BA", "BD"),
           ("CB", "CD"), ("OA", "OB"), ("OA", "OC"), ("CA", "CD")]
    return _cau_goc_vecto(socau, dang, _HV, _hinh_hv_O(), _TEN_HV, CAP, _GOC_HV)


def L10_C4_B11_NB057_MC_A_03(socau, dang=1):
    r"""Góc giữa hai vectơ cùng hướng / ngược hướng (0 hoặc 180 độ) - cho
    bằng hệ thức $\vec a = k\vec b$ hoặc trung điểm, CHUNG ĐIỂM ĐẦU.

    CLAUDE THEM 29/09/2026, sua cung ngay: trung diem chi con cap chung
    diem dau.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    VI_TRI = {"A": 0, "M": 1, "B": 2}
    CAP_TD = [("MA", "MB"), ("AM", "AB"), ("BM", "BA"), ("MB", "MA")]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        if random.random() < 0.5:
            muc = ("he_thuc", random.choice([-5, -4, -3, -2, 2, 3, 4, 5]))
        else:
            muc = ("trung_diem", random.randrange(len(CAP_TD)))
        if muc not in gt:
            gt.append(muc)

    cauTN = ""
    for kieu, t in gt:
        if kieu == "he_thuc":
            g = 0 if t > 0 else 180
            debai = (r"Given two vectors $%s$, $%s$ different from the vector $\overrightarrow{0}$ "
                     r"satisfying $%s = %d%s$. The angle between the two vectors $%s$ and $%s$ equals"
                     % (a, b, a, t, b, a, b))
            giai = (r"Since $%s = %d%s$ with $%d %s 0$, $%s$ and $%s$ have the "
                    % (a, t, b, t, ">" if t > 0 else "<", a, b) +
                    (r"\textbf{same direction}" if t > 0 else r"\textbf{opposite direction}") +
                    r", so the angle between them equals $%d^{\circ}$." % g)
        else:
            v1, v2 = CAP_TD[t]
            h1 = VI_TRI[v1[1]] - VI_TRI[v1[0]]
            h2 = VI_TRI[v2[1]] - VI_TRI[v2[0]]
            g = 0 if h1 * h2 > 0 else 180
            debai = (r"Given segment $AB$ with midpoint $M$. The angle between the two vectors "
                     r"$%s$ and $%s$ equals" % (_vt(*v1), _vt(*v2)))
            giai = (r"The two vectors share the initial point $%s$; the three points "
                    r"$A$, $M$, $B$ are collinear, so $%s$ and $%s$ have the " % (v1[0], _vt(*v1), _vt(*v2)) +
                    (r"\textbf{same direction}" if g == 0 else r"\textbf{opposite direction}") +
                    r", so the angle between them equals $%d^{\circ}$." % g)
        dung = r"$%d^{\circ}$" % g
        nhieu = [r"$%d^{\circ}$" % x for x in (0, 90, 180, 45) if x != g][:3]
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B11_TH057_MC_A_01(socau, dang=1):
    r"""Góc giữa hai vectơ KHÔNG chung điểm đầu - tam giác đều (mức TH).

    CLAUDE THEM 29/09/2026 (co Lan: "chi xet nhung vecto luon khac dinh
    (TH)"). Phai doi vecto / doi huong moi doc duoc goc. Co Lan duyet.
    """
    CAP = [("AB", "BC"), ("AB", "CA"), ("BC", "CA"), ("AH", "BC"),
           ("AB", "HC"), ("HA", "BC"), ("BH", "CA"), ("AC", "HB")]
    return _cau_goc_vecto(socau, dang, _TG_DEU, _hinh_tg_deu_H(), _TEN_TG, CAP, _GOC_TG)


def L10_C4_B11_TH057_MC_A_02(socau, dang=1):
    r"""Góc giữa hai vectơ KHÔNG chung điểm đầu - hình vuông (mức TH).

    CLAUDE THEM 29/09/2026. Co Lan duyet.
    """
    CAP = [("AB", "CD"), ("AB", "DC"), ("AC", "BD"), ("AB", "CA"),
           ("AD", "CB"), ("AB", "BD"), ("AO", "BC"), ("DO", "AB")]
    return _cau_goc_vecto(socau, dang, _HV, _hinh_hv_O(), _TEN_HV, CAP, _GOC_HV)


def L10_C4_B11_TH057_MC_B_01(socau, dang=1):
    r"""Góc giữa hai vectơ CHUNG ĐIỂM CUỐI - tam giác đều (mức TH).

    CLAUDE THEM 29/09/2026 (co Lan: "chi lay nhung vecto luon cung ngon").
    Doi huong ca hai vecto de ve chung diem dau. Co Lan duyet muc do.
    """
    CAP = [("AB", "CB"), ("BA", "CA"), ("AC", "BC"), ("AH", "BH"),
           ("BH", "CH"), ("AB", "HB"), ("HC", "AC"), ("CH", "AH")]
    return _cau_goc_vecto(socau, dang, _TG_DEU, _hinh_tg_deu_H(), _TEN_TG, CAP, _GOC_TG)


def L10_C4_B11_TH057_MC_B_02(socau, dang=1):
    r"""Góc giữa hai vectơ CHUNG ĐIỂM CUỐI - hình vuông (mức TH).

    CLAUDE THEM 29/09/2026. Co Lan duyet muc do.
    """
    CAP = [("AB", "CB"), ("AC", "BC"), ("AC", "DC"), ("BD", "AD"),
           ("AB", "DB"), ("AO", "CO"), ("AO", "BO"), ("DC", "BC")]
    return _cau_goc_vecto(socau, dang, _HV, _hinh_hv_O(), _TEN_HV, CAP, _GOC_HV)


def L10_C4_B11_TH058_MC_A_01(socau, dang=1):
    r"""Tính tích vô hướng của hai vectơ theo định nghĩa.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chỉ dùng góc đặc biệt để $\cos$ ra số hữu tỉ, đáp số đẹp.
    """
    COS_DEP = {0: (1, "1"), 60: (0.5, r"\dfrac{1}{2}"),
               90: (0, "0"), 120: (-0.5, r"-\dfrac{1}{2}"),
               180: (-1, "-1")}
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    gt = []
    while len(gt) < socau:
        goc = random.choice(list(COS_DEP.keys()))
        p = random.choice([2, 4, 6, 8])
        q = random.choice([3, 5, 7, 9])
        w = (goc, p, q)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for goc, p, q in gt:
        c, c_tex = COS_DEP[goc]
        kq = p * q * c
        dung = r"$%s$" % _xx4(kq)
        # khi góc bằng 90 độ thì kq = 0 và -kq cũng bằng 0, hai phương án
        # trùng nhau; lọc qua _ba_nhieu4 cho chắc.
        nhieu = [r"$%s$" % x for x in _ba_nhieu4(
            _xx4(kq), [_xx4(-kq), _xx4(p * q), _xx4(-p * q),
                       _xx4(p + q), _xx4(p * q / 2.0)],
            buoc=lambda t: _xx4(kq + 2 * t))]
        debai = (r"Given two vectors $%s$, $%s$ with $\left|%s\right| = %d$, "
                 r"$\left|%s\right| = %d$ and the angle between them equal to "
                 r"$%d^{\circ}$. Find $%s \cdot %s$."
                 % (a, b, a, p, b, q, goc, a, b))
        giai = (r"Definition of the dot product:"
                "\\\\\n"
                r"$%s \cdot %s = \left|%s\right|\cdot\left|%s\right|\cdot"
                r"\cos\left(%s,\ %s\right)$." % (a, b, a, b, a, b) +
                "\\\\\n"
                r"$%s \cdot %s = %d \cdot %d \cdot \cos %d^{\circ} = "
                r"%d \cdot %s = %s$."
                % (a, b, p, q, goc, p * q, c_tex, _xx4(kq)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B11_TH058_SA_A_01(socau):
    """Tính tích vô hướng - trả lời ngắn, đáp số nguyên.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    gt = []
    while len(gt) < socau:
        goc = random.choice([60, 120])
        p = random.choice([2, 4, 6, 8, 10])
        q = random.choice([3, 5, 7, 9])
        w = (goc, p, q)
        if w not in gt:
            gt.append(w)

    cau = ""
    for goc, p, q in gt:
        c = 0.5 if goc == 60 else -0.5
        c_tex = r"\dfrac{1}{2}" if goc == 60 else r"-\dfrac{1}{2}"
        kq = int(p * q * c)
        debai = (r"Given two vectors $%s$, $%s$ with $\left|%s\right| = %d$, "
                 r"$\left|%s\right| = %d$ and the angle between them equal to "
                 r"$%d^{\circ}$. Find $%s \cdot %s$."
                 % (a, b, a, p, b, q, goc, a, b))
        giai = (r"$%s \cdot %s = \left|%s\right|\cdot\left|%s\right|\cdot"
                r"\cos %d^{\circ} = %d \cdot %d \cdot %s = %d$."
                % (a, b, a, b, goc, p, q, c_tex, kq))
        nhieu = _ba_nhieu4(kq, [-kq, p * q, p + q, kq + 2],
                           buoc=lambda t: kq + 3 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B11_TH059_MC_A_01(socau, dang=1):
    """Tính chất của tích vô hướng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    c = r"\overrightarrow{c}"
    DUNG = [
        (r"$%s \cdot %s = %s \cdot %s$" % (a, b, b, a),
         r"the dot product is \textbf{commutative}"),
        (r"$%s \cdot \left(%s + %s\right) = %s \cdot %s + %s \cdot %s$"
         % (a, b, c, a, b, a, c),
         r"the fact that the dot product is \textbf{distributive} over " r"vector addition"),
        (r"$%s \cdot %s = \left|%s\right|^{2}$" % (a, a, a),
         r"the scalar square of a vector equals the square of its length"),
    ]
    SAI = [
        r"$%s \cdot %s = -\,%s \cdot %s$" % (a, b, b, a),
        r"$%s \cdot \left(%s + %s\right) = %s \cdot %s \cdot %s$"
        % (a, b, c, a, b, c),
        r"$%s \cdot %s = \left|%s\right|$" % (a, a, a),
        r"If $%s \cdot %s = 0$, then $%s = \overrightarrow{0}$ or $%s = "
        r"\overrightarrow{0}$" % (a, b, a, b),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(DUNG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(DUNG):
            break

    cauTN = ""
    for i in gt:
        dung, ten_tc = DUNG[i]
        debai = (r"Given three arbitrary vectors $%s$, $%s$, $%s$. Which of the following statements is "
                 r"\textbf{true}?" % (a, b, c))
        giai = (r"Statement $%s$ is exactly %s." % (dung.strip("$"), ten_tc) +
                "\\\\\n"
                r"Note in particular that the statement ``$%s \cdot %s = 0$ implies $%s$ or "
                r"$%s$ is $\overrightarrow{0}$'' is \textbf{false}: the dot "
                r"product is also $0$ when the two vectors are \textbf{perpendicular} "
                r"to each other." % (a, b, a, b))
        cauTN += MC_SA_answer_text(debai, dung, list(SAI), giai, 0, 0, dang)
    return cauTN


# Các cặp (p; q) làm cho p^2 + pq + q^2 là số chính phương - dùng cho bài
# ba lực cân bằng với góc giữa hai lực bằng 60 độ, để độ lớn lực thứ ba
# ra SỐ NGUYÊN.
# TÍNH BẰNG MÁY, không gõ tay: bản gõ tay đầu tiên có cặp (16; 19; 31)
# sai - 16^2 + 16*19 + 19^2 = 921 chứ không phải 31^2 = 961, để nguyên thì
# bài ba lực ra đáp số sai.
CAP_LUC_60 = []
for _p in range(3, 40):
    for _q in range(_p + 1, 60):
        _k2 = _p * _p + _p * _q + _q * _q
        _k = math.isqrt(_k2)
        if _k * _k == _k2:
            CAP_LUC_60.append((_p, _q, _k))


def L10_C4_B11_VD060_MC_A_01(socau, dang=1):
    r"""Tổng hợp lực tác dụng lên vật bằng vectơ.

    Giữ ý bài của cô Lan (K10_2_3_2_1_VD): chất điểm chịu ba lực và ở
    trạng thái cân bằng, biết góc giữa hai lực, tính độ lớn lực thứ ba.

    Bản của cô cho góc chạy qua nhiều giá trị nên $\left|F_3\right|$ hay
    ra căn thức lẻ; ở đây cố định góc $60^{\circ}$ và chỉ lấy những cặp
    độ lớn làm cho kết quả ra SỐ NGUYÊN.

    CLAUDE THEM 28/09/2026 (chuyen sang khuon math_type) - co Lan kiem
    tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(CAP_LUC_60))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(CAP_LUC_60):
            break

    cauTN = ""
    for i in gt:
        p, q, k = CAP_LUC_60[i]
        dung = r"$%d\ \text{N}$" % k
        nhieu = [r"$%d\ \text{N}$" % (p + q), r"$%d\ \text{N}$" % abs(p - q),
                 r"$%d\ \text{N}$" % (k * k), r"$%d\ \text{N}$" % (k + 1)]
        debai = (r"In the plane, particle $A$ is acted on by three forces "
                 r"$\overrightarrow{F_1}$, $\overrightarrow{F_2}$, "
                 r"$\overrightarrow{F_3}$ and is in equilibrium. Given that "
                 r"$\left|\overrightarrow{F_1}\right| = %d\ \text{N}$, "
                 r"$\left|\overrightarrow{F_2}\right| = %d\ \text{N}$ and the angle "
                 r"between the two vectors $\overrightarrow{F_1}$, "
                 r"$\overrightarrow{F_2}$ equals $60^{\circ}$. Find the magnitude of "
                 r"force $\overrightarrow{F_3}$." % (p, q))
        giai = (r"The particle is in equilibrium, so $\overrightarrow{F_1} + "
                r"\overrightarrow{F_2} + \overrightarrow{F_3} = "
                r"\overrightarrow{0}$, which gives $\overrightarrow{F_3} = "
                r"-\left(\overrightarrow{F_1} + \overrightarrow{F_2}\right)$ "
                r"and therefore $\left|\overrightarrow{F_3}\right| = "
                r"\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|$."
                "\\\\\n"
                r"Squaring both sides (dot product):"
                "\\\\\n"
                r"$\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|^2 "
                r"= \left|\overrightarrow{F_1}\right|^2 + "
                r"\left|\overrightarrow{F_2}\right|^2 + "
                r"2\left|\overrightarrow{F_1}\right|\left|"
                r"\overrightarrow{F_2}\right|\cos 60^{\circ}$."
                "\\\\\n"
                r"$= %d^2 + %d^2 + 2\cdot %d\cdot %d\cdot\dfrac{1}{2} = %d$."
                % (p, q, p, q, p * p + q * q + p * q) +
                "\\\\\n"
                r"Hence $\left|\overrightarrow{F_3}\right| = \sqrt{%d} = %d\ "
                r"\text{N}$." % (k * k, k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B11_VD060_TL_A_01(socau, dong=1):
    """Tự luận: bài toán về lực dùng vectơ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(CAP_LUC_60))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(CAP_LUC_60):
            break

    cauTN = ""
    for i in gt:
        p, q, k = CAP_LUC_60[i]
        tich = p * q // 2 if (p * q) % 2 == 0 else None
        tich_tex = (r"%d" % (p * q // 2)) if tich is not None \
            else r"\dfrac{%d}{2}" % (p * q)
        tich_val = p * q / 2.0

        debai = (r"A particle $A$ is acted on by three forces "
                 r"$\overrightarrow{F_1}$, $\overrightarrow{F_2}$, "
                 r"$\overrightarrow{F_3}$ and is in equilibrium. Given "
                 r"$\left|\overrightarrow{F_1}\right| = %d\ \text{N}$, "
                 r"$\left|\overrightarrow{F_2}\right| = %d\ \text{N}$ and the angle "
                 r"between $\overrightarrow{F_1}$, $\overrightarrow{F_2}$ equals "
                 r"$60^{\circ}$." % (p, q))

        hoi_a = (r"Find the dot product $\overrightarrow{F_1} \cdot "
                 r"\overrightarrow{F_2}$.")
        giai_a = (r"$\overrightarrow{F_1} \cdot \overrightarrow{F_2} = "
                  r"\left|\overrightarrow{F_1}\right|\cdot"
                  r"\left|\overrightarrow{F_2}\right|\cdot\cos 60^{\circ} = "
                  r"%d\cdot %d\cdot\dfrac{1}{2} = %s$." % (p, q, tich_tex))

        hoi_b = (r"Show that $\overrightarrow{F_3} = "
                 r"-\left(\overrightarrow{F_1} + "
                 r"\overrightarrow{F_2}\right)$.")
        giai_b = (r"A particle in equilibrium means that the sum of the forces "
                  r"acting on it equals the zero vector:"
                  "\\\\\n"
                  r"$\overrightarrow{F_1} + \overrightarrow{F_2} + "
                  r"\overrightarrow{F_3} = \overrightarrow{0}$."
                  "\\\\\n"
                  r"Rearranging: $\overrightarrow{F_3} = "
                  r"-\left(\overrightarrow{F_1} + "
                  r"\overrightarrow{F_2}\right)$.")

        hoi_c = (r"Find the magnitude of force $\overrightarrow{F_3}$.")
        giai_c = (r"$\left|\overrightarrow{F_3}\right|^2 = "
                  r"\left|\overrightarrow{F_1} + "
                  r"\overrightarrow{F_2}\right|^2 = "
                  r"\left|\overrightarrow{F_1}\right|^2 + "
                  r"\left|\overrightarrow{F_2}\right|^2 + "
                  r"2\,\overrightarrow{F_1}\cdot\overrightarrow{F_2}$."
                  "\\\\\n"
                  r"$= %d^2 + %d^2 + 2\cdot %s = %d$."
                  % (p, q, tich_tex, p * p + q * q + p * q) +
                  "\\\\\n"
                  r"Hence $\left|\overrightarrow{F_3}\right| = \sqrt{%d} = "
                  r"%d\ \text{N}$." % (k * k, k))

        ds_abcd = [(hoi_a, tich_tex, giai_a),
                   (hoi_b, r"\overrightarrow{F_3} = -\left("
                           r"\overrightarrow{F_1} + "
                           r"\overrightarrow{F_2}\right)", giai_b),
                   (hoi_c, r"%d\ \text{N}" % k, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C4_B11_VD061_MC_A_01(socau, dang=1):
    r"""Phân tích một vectơ theo hai vectơ không cùng phương - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Điểm $M$ nằm trên cạnh $BC$ với $\overrightarrow{BM} =
    k\,\overrightarrow{BC}$, khi đó
    $\overrightarrow{AM} = (1-k)\overrightarrow{AB} +
    k\,\overrightarrow{AC}$.
    """
    # (tử, mẫu) của k, chọn để hệ số ra phân số đẹp
    BO_K = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)]

    def _ps(tu, mau):
        from math import gcd
        g = gcd(abs(tu), mau)
        tu, mau = tu // g, mau // g
        if mau == 1:
            return "%d" % tu
        return r"\dfrac{%d}{%d}" % (tu, mau)

    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_K))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO_K):
            break

    cauTN = ""
    for i in gt:
        tu, mau = BO_K[i]
        # hình: tam giác ABC với M trên BC, BM = (tu/mau) BC
        t = tu / mau
        xm = 0 + t * (4.4 - 0)
        ym = 0.0
        hinh = (
            "\\begin{tikzpicture}[>=stealth,x=1cm,y=1cm,thick,scale=0.95]\n"
            "\\coordinate (A) at (1.2,3.0);\n"
            "\\coordinate (B) at (0,0);\n"
            "\\coordinate (C) at (4.4,0);\n"
            "\\coordinate (M) at (%s,%s);\n" % (_toa(xm), _toa(ym)) +
            "\\draw (A) -- (B) -- (C) -- cycle;\n"
            "\\draw (A) -- (M);\n"
            "\\fill[black] (A) circle[radius=1.4pt] node[above]"
            "{\\footnotesize $A$};\n"
            "\\fill[black] (B) circle[radius=1.4pt] node[below left]"
            "{\\footnotesize $B$};\n"
            "\\fill[black] (C) circle[radius=1.4pt] node[below right]"
            "{\\footnotesize $C$};\n"
            "\\fill[black] (M) circle[radius=1.4pt] node[below]"
            "{\\footnotesize $M$};\n"
            "\\end{tikzpicture}")

        hs_ab = _ps(mau - tu, mau)
        hs_ac = _ps(tu, mau)
        dung = r"$%s = %s\,%s + %s\,%s$" % (
            _vt("A", "M"), hs_ab, _vt("A", "B"), hs_ac, _vt("A", "C"))
        # khi k = 1/2 thì hs_ab = hs_ac, mấy phương án dưới đây trùng
        # nhau, nên phải lọc qua _ba_nhieu4.
        def _pa(h1, h2, dau="+"):
            return r"$%s = %s\,%s %s %s\,%s$" % (
                _vt("A", "M"), h1, _vt("A", "B"), dau, h2, _vt("A", "C"))

        nhieu = _ba_nhieu4(
            dung, [_pa(hs_ac, hs_ab), _pa(hs_ab, hs_ac, "-"),
                   _pa(hs_ac, hs_ac), _pa(hs_ab, hs_ab),
                   _pa(hs_ac, hs_ab, "-")],
            buoc=lambda t: _pa(_ps(tu + t, mau), _ps(tu, mau)))

        debai = (r"Given triangle $ABC$ and a point $M$ on side $BC$ such that $%s = "
                 r"%s\,%s$ (see figure). Express $%s$ in terms of the two vectors "
                 r"$%s$ and $%s$."
                 % (_vt("B", "M"), _ps(tu, mau), _vt("B", "C"),
                    _vt("A", "M"), _vt("A", "B"), _vt("A", "C")))
        giai = (r"By the triangle rule: $%s = %s + %s$."
                % (_vt("A", "M"), _vt("A", "B"), _vt("B", "M")) +
                "\\\\\n"
                r"Since $%s = %s\,%s$ and $%s = %s - %s$, we get"
                % (_vt("B", "M"), _ps(tu, mau), _vt("B", "C"),
                   _vt("B", "C"), _vt("A", "C"), _vt("A", "B")) +
                "\\\\\n"
                r"$%s = %s + %s\left(%s - %s\right) = "
                r"\left(1 - %s\right)%s + %s\,%s$."
                % (_vt("A", "M"), _vt("A", "B"), _ps(tu, mau),
                   _vt("A", "C"), _vt("A", "B"), _ps(tu, mau),
                   _vt("A", "B"), _ps(tu, mau), _vt("A", "C")) +
                "\\\\\n"
                r"Therefore $%s = %s\,%s + %s\,%s$."
                % (_vt("A", "M"), hs_ab, _vt("A", "B"),
                   hs_ac, _vt("A", "C")) +
                "\\\\\n"
                r"Note that the sum of the two coefficients is always $1$ because $M$ lies on line "
                r"$BC$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B11_VD061_TL_A_01(socau, dong=1):
    """Tự luận: chứng minh đẳng thức vectơ trong tam giác.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO = [("ABC", "G", "I"), ("MNP", "G", "I"), ("XYZ", "G", "I")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO):
            break

    cauTN = ""
    for i in gt:
        ten, G, I = BO[i]
        A, B, C = ten
        kh = r"\overrightarrow{0}"
        hinh = _hinh_tam_giac_trong_tam(ten, G, I)

        debai = (r"Given triangle $%s$ with centroid $%s$; let $%s$ be the midpoint "
                 r"of side $%s$ (see figure)." % (ten, G, I, B + C))

        hoi_a = r"Prove that $%s + %s = 2%s$." % (_vt(A, B), _vt(A, C),
                                                  _vt(A, I))
        giai_a = (r"Since $%s$ is the midpoint of $%s$, $%s + %s = %s$." %
                  (I, B + C, _vt(I, B), _vt(I, C), kh) +
                  "\\\\\n"
                  r"By the triangle rule: $%s = %s + %s$ and $%s = %s + %s$."
                  % (_vt(A, B), _vt(A, I), _vt(I, B),
                     _vt(A, C), _vt(A, I), _vt(I, C)) +
                  "\\\\\n"
                  r"Adding them: $%s + %s = 2%s + \left(%s + %s\right) = 2%s$."
                  % (_vt(A, B), _vt(A, C), _vt(A, I), _vt(I, B),
                     _vt(I, C), _vt(A, I)))

        hoi_b = r"Prove that $%s = \dfrac{1}{3}\left(%s + %s\right)$." % (
            _vt(A, G), _vt(A, B), _vt(A, C))
        giai_b = (r"The centroid $%s$ lies on the median $%s$ with "
                  r"$%s = \dfrac{2}{3}%s$." % (G, A + I, _vt(A, G), _vt(A, I)) +
                  "\\\\\n"
                  r"By the previous part, $%s = \dfrac{1}{2}\left(%s + %s\right)$, so"
                  % (_vt(A, I), _vt(A, B), _vt(A, C)) +
                  "\\\\\n"
                  r"$%s = \dfrac{2}{3}\cdot\dfrac{1}{2}\left(%s + %s\right) "
                  r"= \dfrac{1}{3}\left(%s + %s\right)$."
                  % (_vt(A, G), _vt(A, B), _vt(A, C),
                     _vt(A, B), _vt(A, C)))

        hoi_c = r"Prove that $%s + %s + %s = %s$." % (
            _vt(G, A), _vt(G, B), _vt(G, C), kh)
        giai_c = (r"From part b) we have $%s = \dfrac{1}{3}\left(%s + %s\right)$, "
                  r"that is, $3%s = %s + %s$."
                  % (_vt(A, G), _vt(A, B), _vt(A, C),
                     _vt(A, G), _vt(A, B), _vt(A, C)) +
                  "\\\\\n"
                  r"Also $%s = %s + %s$ and $%s = %s + %s$."
                  % (_vt(A, B), _vt(A, G), _vt(G, B),
                     _vt(A, C), _vt(A, G), _vt(G, C)) +
                  "\\\\\n"
                  r"Substituting: $3%s = 2%s + %s + %s$, so "
                  r"$%s = %s + %s$."
                  % (_vt(A, G), _vt(A, G), _vt(G, B), _vt(G, C),
                     _vt(A, G), _vt(G, B), _vt(G, C)) +
                  "\\\\\n"
                  r"Since $%s = -%s$, we have $%s + %s + %s = %s$."
                  % (_vt(A, G), _vt(G, A), _vt(G, A), _vt(G, B),
                     _vt(G, C), kh))

        ds_abcd = [(hoi_a, r"%s + %s = 2%s" % (_vt(A, B), _vt(A, C),
                                               _vt(A, I)), giai_a),
                   (hoi_b, r"%s = \dfrac{1}{3}\left(%s + %s\right)"
                    % (_vt(A, G), _vt(A, B), _vt(A, C)), giai_b),
                   (hoi_c, r"%s + %s + %s = %s"
                    % (_vt(G, A), _vt(G, B), _vt(G, C), kh), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI - bốn ý phải TĂNG DẦN mức độ NB, TH, VD, VDC
# =====================================================================

def L10_C4_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - khái niệm mở đầu; tổng, hiệu; tích với một số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO_TEN = ["ABCD", "MNPQ"]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO_TEN))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO_TEN):
            break

    cauTF = ''
    for i in gt:
        ten = BO_TEN[i]
        A, B, C, D = ten
        O = "O"
        kh = r"\overrightarrow{0}"
        them = ("\\coordinate (%s) at (2.3,1.1);\n" % O +
                "\\draw (%s) -- (%s);\n" % (A, C) +
                "\\draw (%s) -- (%s);\n" % (B, D) +
                "\\fill[black] (%s) circle[radius=1.4pt] node[below right]"
                "{\\footnotesize $%s$};\n" % (O, O))
        hinh = _hinh_tu_giac(ten, [(1, 2.2), (4.6, 2.2), (3.6, 0), (0, 0)],
                             them)

        debai = (r"Given parallelogram $%s$ whose two diagonals intersect at "
                 r"$%s$ (see the figure)." % (ten, O))

        ds_abcd = (
            # a) NB - nhắc lại một tính chất
            [
                (r"{\True $%s = %s$}" % (_vt(A, B), _vt(D, C)),
                 r"True. In a parallelogram, $%s$ is parallel and equal to $%s$, and "
                 r"they also have the same direction, so the two vectors are equal."
                 % (A + B, D + C)),
                (r"{$%s = %s$}" % (_vt(A, B), _vt(C, D)),
                 r"False. $%s$ and $%s$ have the same magnitude but \textbf{opposite directions}, "
                 r"so they are opposite vectors." % (_vt(A, B), _vt(C, D))),
            ],
            # b) TH - thay vào đúng một quy tắc
            [
                (r"{\True $%s + %s = %s$}" % (_vt(A, B), _vt(A, D), _vt(A, C)),
                 r"True. This is exactly the parallelogram rule: the sum of two vectors "
                 r"starting from $%s$ is the diagonal vector starting from "
                 r"$%s$." % (A, A)),
                (r"{$%s + %s = %s$}" % (_vt(A, B), _vt(A, D), _vt(B, D)),
                 r"False. $%s$ is the \textbf{difference} vector $%s - %s$, not the "
                 r"sum." % (_vt(B, D), _vt(A, D), _vt(A, B))),
            ],
            # c) VD - phải dùng được tính chất giao điểm hai đường chéo
            [
                (r"{\True $%s + %s = %s$}" % (_vt(O, A), _vt(O, C), kh),
                 r"True. The two diagonals of a parallelogram intersect at the "
                 r"midpoint of each diagonal, so $%s$ is the midpoint of $%s$; hence "
                 r"$%s$ and $%s$ are opposite vectors."
                 % (O, A + C, _vt(O, A), _vt(O, C))),
                (r"{$%s + %s = %s$}" % (_vt(O, A), _vt(O, B), kh),
                 r"False. $%s$ is the midpoint of $%s$, not of $%s$, "
                 r"so $%s$ and $%s$ are not opposite vectors."
                 % (O, A + C, A + B, _vt(O, A), _vt(O, B))),
            ],
            # d) VDC - phải tự ghép hai quy tắc, không có công thức sẵn
            [
                (r"{\True $%s + %s + %s + %s = %s$}"
                 % (_vt(A, B), _vt(A, D), _vt(C, B), _vt(C, D), kh),
                 r"True. By the parallelogram rule, $%s + %s = %s$ and "
                 r"$%s + %s = %s$."
                 % (_vt(A, B), _vt(A, D), _vt(A, C),
                    _vt(C, B), _vt(C, D), _vt(C, A)) +
                 "\\\\\n"
                 r"Since $%s$ and $%s$ are opposite vectors, their sum equals $%s$."
                 % (_vt(A, C), _vt(C, A), kh)),
                (r"{$%s + %s + %s + %s = 2%s$}"
                 % (_vt(A, B), _vt(A, D), _vt(C, B), _vt(C, D), _vt(A, C)),
                 r"False. The sum equals $%s + %s = %s$, not $2%s$."
                 % (_vt(A, C), _vt(C, A), kh, _vt(A, C))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF


def L10_C4_TF_B_01(socau, socot=1):
    """Đúng/Sai - vectơ trong mặt phẳng toạ độ; tích vô hướng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4[:4])
        xa, ya = random.randint(-3, 3), random.randint(-3, 3)
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        w = (xa, ya, sx * p, sy * q, r)
        if w not in gt:
            gt.append(w)

    cauTF = ''
    for xa, ya, u, v, r in gt:
        xb, yb = xa + u, ya + v
        xc, yc = xa - v, ya + u          # AC vuông góc AB, cùng độ dài
        S = (u * u + v * v) / 2.0

        debai = (r"In the coordinate plane $Oxy$, given three points $A%s$, $B%s$, "
                 r"$C%s$." % (_toado(xa, ya), _toado(xb, yb),
                              _toado(xc, yc)))

        ds_abcd = (
            # a) NB - nhắc lại một công thức
            [
                (r"{\True $%s = %s$}" % (_vt("A", "B"), _toado(u, v)),
                 r"True. The coordinates of a vector equal the coordinates of the terminal point minus those of the initial "
                 r"point: $%s = \left(%d - \left(%d\right);\ %d - "
                 r"\left(%d\right)\right) = %s$."
                 % (_vt("A", "B"), xb, xa, yb, ya, _toado(u, v))),
                (r"{$%s = %s$}" % (_vt("A", "B"), _toado(-u, -v)),
                 r"False. It is $%s$ that is the vector $%s$; taking the initial point minus the terminal point "
                 r"gives the opposite vector." % (_toado(-u, -v), _vt("B", "A"))),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True $AB = %d$}" % r,
                 r"True. $AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} "
                 r"= \sqrt{%d} = %d$." % (u, v, u * u + v * v, r)),
                (r"{$AB = %d$}" % (abs(u) + abs(v)),
                 r"False. $%d$ is the sum of the two coordinates, not the length; "
                 r"$AB = \sqrt{%d} = %d$."
                 % (abs(u) + abs(v), u * u + v * v, r)),
            ],
            # c) VD - phải tính được tích vô hướng mới kết luận được
            [
                (r"{\True Triangle $ABC$ has a right angle at $A$}",
                 r"True. $%s = %s$, $%s = %s$, so "
                 r"$%s \cdot %s = \left(%d\right)\left(%d\right) + "
                 r"\left(%d\right)\left(%d\right) = 0$."
                 % (_vt("A", "B"), _toado(u, v), _vt("A", "C"),
                    _toado(-v, u), _vt("A", "B"), _vt("A", "C"),
                    u, -v, v, u) +
                 "\\\\\n"
                 r"The dot product equals $0$, so the two vectors are perpendicular."),
                (r"{Triangle $ABC$ has a right angle at $B$}",
                 r"False. Computing $%s \cdot %s$ gives $0$, so the right angle is at "
                 r"vertex $A$, not vertex $B$."
                 % (_vt("A", "B"), _vt("A", "C"))),
            ],
            # d) VDC - phải tự nghĩ ra cách, không có công thức sẵn
            [
                (r"{\True The area of triangle $ABC$ equals $%s$}" % _xx4(S),
                 r"True. The triangle is right-angled at $A$ and $AB = AC = %d$, so"
                 "\\\\\n"
                 r"$S = \dfrac{1}{2}\cdot AB\cdot AC = "
                 r"\dfrac{1}{2}\cdot %d\cdot %d = %s$." % (r, r, r, _xx4(S))),
                (r"{The area of triangle $ABC$ equals $%d$}" % (r * r),
                 r"False. $%d$ is the product $AB \cdot AC$; the area of a right triangle "
                 r"equals \textbf{half} the product of the two legs, that is "
                 r"$%s$." % (r * r, _xx4(S))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


# ---------------------------------------------------------------------
# Năm dạng TRẢ LỜI NGẮN bổ sung cho các yêu cầu mức Vận dụng.
# Sau khi sửa phạm vi đề hệ số 1 (chạy hết chương, không dừng ở mốc thi
# giữa kỳ), bộ chọn câu cần trả lời ngắn cho VD054, VD055, VD056, VD060,
# VD061 mà Mapping chưa khai, nên đề mất 12/60 câu.
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
# ---------------------------------------------------------------------

def L10_C4_B10_VD054_SA_B_01(socau, dang=2):
    """Bài toán hình học bằng toạ độ - độ dài trung tuyến, đáp số nguyên.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4[:5])
        xa, ya = random.randint(-4, 4), random.randint(-4, 4)
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        w = (xa, ya, sx * p, sy * q, r)
        if w not in gt:
            gt.append(w)

    cau = ""
    for xa, ya, u, v, r in gt:
        # B và C đối xứng nhau qua A theo hướng (u; v): trung điểm BC là A
        xb, yb = xa + u, ya + v
        xc, yc = xa - u, ya - v
        # lấy điểm D để trung tuyến từ D tới trung điểm BC (chính là A)
        xd, yd = xa + 2 * (-v), ya + 2 * u
        kq = 2 * r
        debai = (r"In the coordinate plane $Oxy$, given triangle $DBC$ with "
                 r"$D%s$, $B%s$, $C%s$. Let $A$ be the midpoint of $BC$. "
                 r"Find the length of median $DA$."
                 % (_toado(xd, yd), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"The midpoint $A$ of $BC$ has coordinates "
                r"$\left(\dfrac{x_B + x_C}{2};\ \dfrac{y_B + y_C}{2}\right) "
                r"= %s$." % _toado(xa, ya) +
                "\\\\\n"
                r"$%s = %s$." % (_vt("D", "A"), _toado(xa - xd, ya - yd)) +
                "\\\\\n"
                r"$DA = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} = "
                r"\sqrt{%d} = %d$."
                % (xa - xd, ya - yd, (xa - xd) ** 2 + (ya - yd) ** 2, kq))
        nhieu = _ba_nhieu4(kq, [r, kq * kq, kq + 1, abs(u) + abs(v)],
                           buoc=lambda t: kq + 3 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, dang)
    return cau


def L10_C4_B10_VD055_SA_A_01(socau):
    """Vị trí của vật trên mặt phẳng toạ độ - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        x0, y0 = random.randint(-6, 6), random.randint(-6, 6)
        vx, vy = random.randint(-5, 5), random.randint(-5, 5)
        t = random.randint(2, 5)
        if (vx, vy) == (0, 0):
            continue
        w = (x0, y0, vx, vy, t)
        if w not in gt:
            gt.append(w)

    cau = ""
    for x0, y0, vx, vy, t in gt:
        x1 = x0 + t * vx
        debai = (r"A motorboat starts from position $A%s$ in the coordinate plane "
                 r"$Oxy$ (the unit on each axis is a kilometer) and moves in a "
                 r"straight line at constant velocity $\overrightarrow{v} = %s$ "
                 r"(unit: km/h). Find the \textbf{x-coordinate} of the motorboat's "
                 r"position after $%d$ h." % (_toado(x0, y0), _toado(vx, vy), t))
        giai = (r"After $%d$ h, the displacement is $%d\overrightarrow{v} = %s$."
                % (t, t, _toado(t * vx, t * vy)) +
                "\\\\\n"
                r"New x-coordinate of the position: $%d + %d\cdot\left(%d\right) = %d$."
                % (x0, t, vx, x1))
        nhieu = _ba_nhieu4(x1, [x0 + vx, t * vx, x0 - t * vx, y0 + t * vy],
                           buoc=lambda k: x1 + 2 * k)
        cau += MC_SA_answer_const(debai, x1, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B10_VD056_SA_A_01(socau):
    """Diện tích tam giác bằng toạ độ - trả lời ngắn, đáp số nguyên.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa, ya = random.randint(-4, 4), random.randint(-4, 4)
        u1, u2 = random.randint(-5, 5), random.randint(-5, 5)
        v1, v2 = random.randint(-5, 5), random.randint(-5, 5)
        d = u1 * v2 - u2 * v1
        if d == 0 or abs(d) % 2 != 0:
            continue
        w = (xa, ya, u1, u2, v1, v2)
        if w not in gt:
            gt.append(w)

    cau = ""
    for xa, ya, u1, u2, v1, v2 in gt:
        xb, yb = xa + u1, ya + u2
        xc, yc = xa + v1, ya + v2
        d = u1 * v2 - u2 * v1
        S = abs(d) // 2
        debai = (r"In the coordinate plane $Oxy$, given triangle $ABC$ with "
                 r"$A%s$, $B%s$, $C%s$. Calculate the area of triangle $ABC$."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$; $%s = %s$."
                % (_vt("A", "B"), _toado(u1, u2),
                   _vt("A", "C"), _toado(v1, v2)) +
                "\\\\\n"
                r"$S = \dfrac{1}{2}\left|x_1y_2 - x_2y_1\right| = "
                r"\dfrac{1}{2}\left|\left(%d\right)\left(%d\right) - "
                r"\left(%d\right)\left(%d\right)\right| = "
                r"\dfrac{1}{2}\cdot %d = %d$."
                % (u1, v2, v1, u2, abs(d), S))
        nhieu = _ba_nhieu4(S, [abs(d), S + 1, 2 * S + 1,
                               abs(u1 * v1 + u2 * v2)],
                           buoc=lambda t: S + 3 * t)
        cau += MC_SA_answer_const(debai, S, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B11_VD060_SA_A_01(socau):
    """Tổng hợp lực - trả lời ngắn, độ lớn lực thứ ba ra số nguyên.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(CAP_LUC_60))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(CAP_LUC_60):
            break

    cau = ""
    for i in gt:
        p, q, k = CAP_LUC_60[i]
        debai = (r"Particle $A$ is acted on by three forces "
                 r"$\overrightarrow{F_1}$, $\overrightarrow{F_2}$, "
                 r"$\overrightarrow{F_3}$ and is in equilibrium. Given "
                 r"$\left|\overrightarrow{F_1}\right| = %d\ \text{N}$, "
                 r"$\left|\overrightarrow{F_2}\right| = %d\ \text{N}$, and the angle "
                 r"between $\overrightarrow{F_1}$ and $\overrightarrow{F_2}$ "
                 r"equals $60^{\circ}$. Find $\left|\overrightarrow{F_3}\right|$ "
                 r"(unit: N)." % (p, q))
        giai = (r"Since the particle is in equilibrium, $\overrightarrow{F_3} = "
                r"-\left(\overrightarrow{F_1} + \overrightarrow{F_2}\right)$, "
                r"hence $\left|\overrightarrow{F_3}\right| = "
                r"\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|$."
                "\\\\\n"
                r"$\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|^2 "
                r"= %d^2 + %d^2 + 2\cdot %d\cdot %d\cdot\cos 60^{\circ} = %d$."
                % (p, q, p, q, p * p + q * q + p * q) +
                "\\\\\n"
                r"Hence $\left|\overrightarrow{F_3}\right| = \sqrt{%d} = %d$."
                % (k * k, k))
        nhieu = _ba_nhieu4(k, [p + q, abs(p - q), k * k, k + 2],
                           buoc=lambda t: k + 3 * t)
        cau += MC_SA_answer_const(debai, k, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B11_VD061_SA_A_01(socau):
    r"""Phân tích vectơ - trả lời ngắn, hỏi MỘT số nguyên.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Hỏi mẫu số $n$ trong $\overrightarrow{AM} =
    \dfrac{1}{n}\left(\overrightarrow{AB} + \overrightarrow{AC}\right)$
    để đáp số là số nguyên.
    """
    BO = [("the midpoint of side $BC$", "M", 2,
           r"Since $M$ is the midpoint of $BC$, $\overrightarrow{AM} = "
           r"\dfrac{1}{2}\left(\overrightarrow{AB} + "
           r"\overrightarrow{AC}\right)$."),
          ("the centroid of triangle $ABC$", "G", 3,
           r"Since $G$ is the centroid, $\overrightarrow{AG} = "
           r"\dfrac{2}{3}\overrightarrow{AI}$ where $I$ is the midpoint of "
           r"$BC$; and $\overrightarrow{AI} = "
           r"\dfrac{1}{2}\left(\overrightarrow{AB} + "
           r"\overrightarrow{AC}\right)$, so $\overrightarrow{AG} = "
           r"\dfrac{1}{3}\left(\overrightarrow{AB} + "
           r"\overrightarrow{AC}\right)$.")]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BO):
            break

    cau = ""
    for i in gt:
        mo_ta, ten, kq, ly_do = BO[i]
        debai = (r"In triangle $ABC$, point $%s$ is %s. It is given that "
                 r"$\overrightarrow{A%s} = \dfrac{1}{n}\left("
                 r"\overrightarrow{AB} + \overrightarrow{AC}\right)$. "
                 r"Find the positive integer $n$." % (ten, mo_ta, ten))
        giai = ly_do + "\\\\\n" + r"Therefore $n = %d$." % kq
        nhieu = _ba_nhieu4(kq, [1, 4, 6, 2 if kq != 2 else 5],
                           buoc=lambda t: kq + 3 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C4_B10_VD055_TL_A_01(socau, dong=1):
    """Tự luận: vị trí của vật trên mặt phẳng toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Vectơ vận tốc lấy từ bộ ba Pytago nên tốc độ và quãng đường ra SỐ
    NGUYÊN, học sinh không phải làm tròn giữa chừng.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(BO_BA_PYTAGO4[:5])
        sx, sy = random.choice([1, -1]), random.choice([1, -1])
        x0, y0 = random.randint(-6, 6), random.randint(-6, 6)
        t = random.randint(2, 4)
        w = (x0, y0, sx * p, sy * q, r, t)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for x0, y0, vx, vy, r, t in gt:
        x1, y1 = x0 + t * vx, y0 + t * vy

        debai = (r"In the coordinate plane $Oxy$ (the unit on each axis is "
                 r"one kilometer), a motorboat starts from position $A%s$ and moves "
                 r"in uniform straight-line motion with velocity vector $\overrightarrow{v} = %s$ "
                 r"(unit: km/h)." % (_toado(x0, y0), _toado(vx, vy)))

        hoi_a = r"Find the speed of the motorboat."
        giai_a = (r"Speed is the magnitude of the velocity vector:"
                  "\\\\\n"
                  r"$\left|\overrightarrow{v}\right| = "
                  r"\sqrt{\left(%d\right)^2 + \left(%d\right)^2} = "
                  r"\sqrt{%d} = %d$ (km/h)."
                  % (vx, vy, vx * vx + vy * vy, r))

        hoi_b = r"Find the coordinates of the position $B$ of the boat after $%d$ hours." % t
        giai_b = (r"For uniform straight-line motion, the displacement after $%d$ hours is "
                  r"$%s = %d\overrightarrow{v} = %s$."
                  % (t, _vt("A", "B"), t, _toado(t * vx, t * vy)) +
                  "\\\\\n"
                  r"The coordinates of $B$ equal the coordinates of $A$ plus the "
                  r"displacement:"
                  "\\\\\n"
                  r"$B\left(%d + %d;\ %d + %d\right) = B%s$."
                  % (x0, t * vx, y0, t * vy, _toado(x1, y1)))

        hoi_c = r"Calculate the distance the motorboat travels after $%d$ hours." % t
        giai_c = (r"The boat moves in a straight line at constant speed, so distance equals speed times "
                  r"time:"
                  "\\\\\n"
                  r"$s = %d \cdot %d = %d$ (km)." % (r, t, r * t) +
                  "\\\\\n"
                  r"Check using the length $AB$: "
                  r"$AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} = %d$ "
                  r"(km), which matches the result above."
                  % (t * vx, t * vy, r * t))

        ds_abcd = [(hoi_a, r"%d\ \text{km/h}" % r, giai_a),
                   (hoi_b, r"B\left(%d;\ %d\right)" % (x1, y1), giai_b),
                   (hoi_c, r"%d\ \text{km}" % (r * t), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# ----------------------------------------------------------------------
# CLAUDE THEM 30/09/2026 - goi ex_test TU THEM dau "." sau moi phuong an
# \choice, nen phuong an KHONG duoc tu cham cuoi (neu co se ra ".." tren PDF).
# Cac ham trac nghiem co phuong an la cau van (vd "Mot tuan co $7$ ngay.")
# goi _MC_khong_cham thay cho MC_SA_answer_text; math_type giu nguyen.
# ----------------------------------------------------------------------
def _bo_cham_cuoi(s):
    """Bo dau "." o cuoi phuong an (giu "\\right." cua he/tuyen va "...")."""
    s = str(s).rstrip()
    while s.endswith(".") and not s.endswith(r"\right.") and not s.endswith("..."):
        s = s[:-1].rstrip()
    return s


def _MC_khong_cham(debai, dung, nhieu, *con_lai):
    """Nhu MC_SA_answer_text nhung bo dau "." cuoi cua 4 phuong an."""
    return MC_SA_answer_text(debai, _bo_cham_cuoi(dung),
                             [_bo_cham_cuoi(x) for x in nhieu], *con_lai)


# =====================================================================
# BÀI 7 - BỔ SUNG TỪ TÀI LIỆU CĐ DẠY THÊM TOÁN 10 "KHÁI NIỆM VECTƠ" (file docx cô Lan gửi 01/10/2026)
# CLAUDE THEM 01/10/2026 - co Lan duyet lai. Chỉ ba đơn vị NB037, NB038, TH039 (YCCĐ của Bộ):
# không dùng tổng, hiệu, tích với số, vectơ đối (Bài 8). Mọi quan hệ cùng phương, cùng hướng, bằng nhau,
# mọi số đếm đều do Python tính từ toạ độ của hình; hình là TikZ thuần (hiện cả trên web).
# Kho hình lấy xoay vòng: hình đã ra thì chỉ ra lại khi đã dùng hết kho.
# =====================================================================
import sys as _sys4
import types as _types4
from sympy import sqrt as _sq4, nsimplify as _ns4, latex as _lx4, Symbol as _Sym4, Rational as _R4

_C4_XV = _sys4.modules.setdefault("_ngan_hang_xoay_vong", _types4.ModuleType("_ngan_hang_xoay_vong"))
if not hasattr(_C4_XV, "da_dung"):
    _C4_XV.da_dung = {}


def _c4_uu_tien(ten, ung):
    """Thứ tự lấy các phần tử của kho 'ten' (danh sách khoá): CHƯA dùng trước, đã dùng sau; hết thì vòng mới."""
    da = _C4_XV.da_dung.setdefault(ten, set())
    if all(k in da for k in ung):
        da.difference_update(ung)
    chua = [k for k in ung if k not in da]
    roi = [k for k in ung if k in da]
    random.shuffle(chua)
    random.shuffle(roi)
    return chua + roi


def _c4_danh_dau(ten, ds):
    _C4_XV.da_dung.setdefault(ten, set()).update(ds)


# ---------------------------------------------------------------------
# KHO HÌNH: toạ độ vẽ (dùng luôn để xét phương, hướng, bằng nhau), đoạn cần vẽ, lời mô tả
# ---------------------------------------------------------------------
_C4_TU_GIAC_TEN = [("ABCD", "O"), ("MNPQ", "O"), ("ABCD", "I"), ("EFGH", "O")]


def _c4_hinh(kieu):
    """Một hình của kho. Trả về dict: P (tên -> (x, y)), canh (đoạn vẽ), mo (lời mô tả), kieu, tam (điểm giữa hình)."""
    if kieu in ("hbh", "hcn", "thoi", "vuong"):
        ten, o = random.choice(_C4_TU_GIAC_TEN)
        A, B, C, D = ten
        toa = {"hbh": [(0, 0), (4, 0), (5.2, 2.4), (1.2, 2.4)],
               "hcn": [(0, 0), (4.4, 0), (4.4, 2.4), (0, 2.4)],
               "thoi": [(0, 1.5), (2.4, 0), (4.8, 1.5), (2.4, 3)],
               "vuong": [(0, 0), (3, 0), (3, 3), (0, 3)]}[kieu]
        P = dict(zip(ten, toa))
        P[o] = ((toa[0][0] + toa[2][0]) / 2, (toa[0][1] + toa[2][1]) / 2)
        ten_hinh = {"hbh": "parallelogram", "hcn": "rectangle", "thoi": "rhombus", "vuong": "square"}[kieu]
        return dict(kieu=kieu, P=P, canh=[(A, B), (B, C), (C, D), (D, A), (A, C), (B, D)], tam=o,
                    mo=r"Given %s $%s$ whose two diagonals intersect at $%s$ (see figure)." % (ten_hinh, ten, o),
                    da_giac=list(ten))
    if kieu == "luc_giac":
        ten = "ABCDEF"
        P = {ten[i]: (2 * math.cos(math.pi / 3 * i), 2 * math.sin(math.pi / 3 * i)) for i in range(6)}
        P["O"] = (0.0, 0.0)
        canh = [(ten[i], ten[(i + 1) % 6]) for i in range(6)] + [("A", "D"), ("B", "E"), ("C", "F")]
        return dict(kieu=kieu, P=P, canh=canh, tam="O", da_giac=list(ten),
                    mo=r"Given a regular hexagon $ABCDEF$ with center $O$ (see the figure).")
    if kieu == "tg_trung_diem":
        A, B, C = "ABC"
        M, N, Q = random.choice([("M", "N", "P"), ("D", "E", "F"), ("I", "J", "K")])
        P = {A: (1.4, 3.0), B: (0.0, 0.0), C: (4.8, 0.0)}
        tb = lambda X, Y: ((P[X][0] + P[Y][0]) / 2, (P[X][1] + P[Y][1]) / 2)
        P[M], P[N], P[Q] = tb(B, C), tb(C, A), tb(A, B)
        return dict(kieu=kieu, P=P, canh=[(A, B), (B, C), (C, A), (M, N), (N, Q), (Q, M)], tam=None, da_giac=[A, B, C],
                    mo=r"Given triangle $ABC$ where $%s$, $%s$, $%s$ are the midpoints of sides $BC$, $CA$, $AB$, respectively "
                       r"(see the figure)." % (M, N, Q))
    if kieu == "thang":
        ten = random.choice(["ABCD", "MNPQ"])
        A, B, C, D = ten
        E = "I" if ten == "ABCD" else "E"
        P = {A: (1.0, 2.2), B: (3.2, 2.2), C: (4.4, 0.0), D: (0.0, 0.0), E: (2.2, 0.0)}
        return dict(kieu=kieu, P=P, canh=[(A, B), (B, C), (C, D), (D, A), (A, E), (B, E)], tam=None, da_giac=[A, B, C, D],
                    mo=r"Given trapezoid $%s$ with two bases $%s$, $%s$ where $%s = 2%s$; " r"$%s$ is the midpoint of $%s$ (see figure)."
                       % (ten, A + B, D + C, D + C, A + B, E, D + C))
    raise ValueError(kieu)


_C4_KIEU_HINH = ["hbh", "hcn", "thoi", "vuong", "luc_giac", "tg_trung_diem", "thang"]


def _c4_chon_hinh(ten_kho, cho_phep=None):
    """Chọn một kiểu hình theo xoay vòng (chung cho cả Bài 7 nên trong một đề ít lặp hình)."""
    ung = [k for k in _C4_KIEU_HINH if cho_phep is None or k in cho_phep]
    k = _c4_uu_tien("c4_b7_hinh", ung)[0]
    _c4_danh_dau("c4_b7_hinh", [k])
    return _c4_hinh(k)


def _c4_tikz(H, ve_vt=None):
    """TikZ của hình H; nhãn đặt ra phía ngoài (theo hướng từ trọng tâm hình tới điểm)."""
    P = H["P"]
    cx = sum(x for x, _ in P.values()) / len(P)
    cy = sum(y for _, y in P.values()) / len(P)
    out = ["\\begin{tikzpicture}[>=stealth,x=1cm,y=1cm,thick,scale=0.85]"]
    for t, (x, y) in P.items():
        out.append("\\coordinate (%s) at (%s,%s);" % (t, _toa(x), _toa(y)))
    out.append("\\draw " + " ".join("(%s) -- (%s)" % c for c in H["canh"]) + ";")
    for t, (x, y) in P.items():
        dx, dy = x - cx, y - cy
        if abs(dx) < 1e-6 and abs(dy) < 1e-6 or t == H.get("tam"):
            neo = "below"
        else:
            g = math.degrees(math.atan2(dy, dx)) % 360
            neo = ["right", "above right", "above", "above left", "left", "below left", "below", "below right"][
                int(((g + 22.5) % 360) // 45)]
        out.append("\\fill[black] (%s) circle[radius=1.4pt] node[%s]{\\footnotesize $%s$};" % (t, neo, t))
    out.append("\\end{tikzpicture}")
    return "\n".join(out)


def _c4_v(H, X, Y):
    return (H["P"][Y][0] - H["P"][X][0], H["P"][Y][1] - H["P"][X][1])


def _c4_cp(u, v):
    return abs(u[0] * v[1] - u[1] * v[0]) < 1e-7


def _c4_ch(u, v):
    return _c4_cp(u, v) and u[0] * v[0] + u[1] * v[1] > 0


def _c4_bang(u, v):
    return abs(u[0] - v[0]) < 1e-7 and abs(u[1] - v[1]) < 1e-7


def _c4_tat_ca_vt(H):
    ds = list(H["P"])
    return [(X, Y) for X in ds for Y in ds if X != Y]


def _c4_loc(H, v, quan_he):
    """Các vectơ (điểm đầu, cuối thuộc hình, khác v) có quan hệ quan_he với v."""
    vv = _c4_v(H, *v)
    f = {"cung_phuong": _c4_cp, "cung_huong": _c4_ch, "nguoc_huong": lambda a, b: _c4_cp(a, b) and not _c4_ch(a, b),
         "bang": _c4_bang}[quan_he]
    return [w for w in _c4_tat_ca_vt(H) if w != v and f(_c4_v(H, *w), vv)]


def _c4_ds_vt(ds):
    return ", ".join("$%s$" % _vt(*w) for w in ds)


_C4_TEN_QH = {"cung_phuong": "collinear", "cung_huong": "same direction", "nguoc_huong": "opposite direction", "bang": "equal to"}


def _c4_ly_qh(H, v, qh, ds):
    """Lời giải liệt kê."""
    vv = _vt(*v)
    if qh == "bang":
        dau = r"Vectors equal to $%s$ must have the same direction and the same length as $%s$" % (vv, vv)
    elif qh == "cung_phuong":
        dau = (r"The vectors collinear with $%s$ have lines of action parallel or identical to the line $%s$"
               % (vv, v[0] + v[1]))
    else:
        dau = (r"Vectors in the %s relative to $%s$ must be collinear with $%s$ (their line of support is parallel to or coincides with $%s$) and point to %s side"
               % (_C4_TEN_QH[qh], vv, vv, v[0] + v[1], "the same" if qh == "cung_huong" else "the opposite"))
    return dau + r": %s. The number of vectors is $%d$." % (_c4_ds_vt(ds) if ds else "does not include", len(ds))


def _c4_chon_vt(H, qh, lo=1, hi=12):
    """Chọn vectơ v (cạnh, đường chéo, nửa đường chéo) sao cho số vectơ có quan hệ qh nằm trong [lo; hi]."""
    ung = [c for c in H["canh"]] + [(c[1], c[0]) for c in H["canh"]]
    if H.get("tam"):
        ung += [(X, H["tam"]) for X in H["da_giac"]] + [(H["tam"], X) for X in H["da_giac"]]
    random.shuffle(ung)
    for v in ung:
        if lo <= len(_c4_loc(H, v, qh)) <= hi:
            return v
    return None


def _c4_nhieu_so(dap, ung):
    ra = []
    for x in list(ung) + [dap + 1, dap - 1, dap + 2, dap - 2, dap + 3, 2 * dap]:
        if isinstance(x, int) and x >= 0 and x != dap and x not in ra:
            ra.append(x)
    return ra[:3]


# ---------------------------------------------------------------------
# NB037_MC_A_02: khẳng định đúng (sai) về cùng phương, cùng hướng, ngược hướng trong hình
# ---------------------------------------------------------------------
def _c4_pb_huong(H):
    """Các phát biểu ``u và w <quan hệ>'' kèm chân trị, u, w có điểm mút thuộc hình."""
    vts = [c for c in H["canh"]] + [(c[1], c[0]) for c in H["canh"]]
    if H.get("tam"):
        vts += [(X, H["tam"]) for X in H["da_giac"]]
    ra = []
    for u in vts:
        for w in vts:
            if u == w or set(u) == set(w):
                continue
            a, b = _c4_v(H, *u), _c4_v(H, *w)
            cp, ch = _c4_cp(a, b), _c4_ch(a, b)
            for qh, gt in (("same direction", ch), ("opposite direction", cp and not ch), ("collinear", cp),
                           ("not collinear", not cp)):
                ra.append((r"$%s$ and $%s$: %s" % (_vt(*u), _vt(*w), qh), gt, u, w, cp, ch))
    return ra


def L10_C4_B7_NB037_MC_A_02(socau, dang=1):
    r"""Cách hỏi khác của NB037_MC_A_01 với KHO HÌNH xoay vòng (hình bình hành, hình chữ nhật, hình thoi, hình vuông
    có tâm; lục giác đều có tâm; tam giác có ba trung điểm; hình thang có trung điểm đáy lớn): chọn khẳng định đúng
    (hoặc sai) về hai vectơ cùng phương, cùng hướng, ngược hướng. Chân trị do Python tính từ toạ độ.

    CLAUDE THEM 01/10/2026 - theo phan dang 2, MC 4, 6, 8, 9 tai lieu CĐ day them "Khai niem vecto". Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        H = _c4_chon_hinh("nb037_a")
        pb = _c4_pb_huong(H)
        hoi_dung = random.random() < 0.6
        # ưu tiên các cặp cùng phương (dễ nhầm hướng)
        dung = [p for p in pb if p[1] == hoi_dung and (p[4] or random.random() < 0.3)]
        sai = [p for p in pb if p[1] != hoi_dung and p[4]]
        random.shuffle(dung)
        random.shuffle(sai)
        chon = [dung[0]]
        sai2 = [p for p in pb if p[1] != hoi_dung and not p[4]]
        random.shuffle(sai2)
        for p in sai + sai2:
            khoa = lambda q: frozenset([q[2], q[3]])
            if all(khoa(p) != khoa(q) for q in chon) and len(chon) < 4:
                chon.append(p)
        ly = []
        for p in chon:
            u, w = p[2], p[3]
            mo_ta = ("same direction" if p[5] else "opposite direction") if p[4] else "not collinear (the support lines intersect)"
            ly.append(r"$%s$ and $%s$: %s, so the statement ``%s'' is %s." % (_vt(*u), _vt(*w), mo_ta, p[0], "true" if p[1] else "false"))
        debai = H["mo"] + r" Which of the following statements is %s?" % (r"\textbf{true}" if hoi_dung else r"\textbf{false}")
        giai = (r"Two vectors are collinear when their support lines are parallel or coincide; collinear vectors have the same direction "
                r"or opposite direction.\\ " + r"\\ ".join(ly))
        cau += MC_SA_answer_text(debai, chon[0][0], [p[0] for p in chon[1:4]], giai, _c4_tikz(H), 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB037_MC_B / SA_A: đếm số vectơ khác vectơ-không tạo từ n điểm
# ---------------------------------------------------------------------
def _c4_dem_diem():
    """(đề, đáp số, lời giải, nhiễu): n điểm phân biệt -> n(n - 1) vectơ; có điểm đầu cố định -> n - 1."""
    kieu = random.randint(0, 2)
    if kieu == 0:
        k = random.choice([3, 4, 5, 6])
        ten = {3: "triangle $ABC$", 4: "quadrilateral $ABCD$", 5: "pentagon $ABCDE$", 6: "hexagon $ABCDEF$"}[k]
        dinh = "ABCDEF"[:k]
        de = (r"Given %s. How many nonzero vectors have their initial and " r"terminal points at the vertices of such %s?"
              % (ten, "triangles" if k == 3 else "quadrilaterals" if k == 4 else "pentagon" if k == 5 else "hexagon"))
        dap = k * (k - 1)
        ly = (r"Each nonzero vector is determined by an ordered pair of different initial and terminal points. There are "
              r"$%d$ choices for the initial point and $%d$ choices for the terminal point, so there are $%d \cdot %d = %d$ vectors" % (k, k - 1, k, k - 1, dap))
        if k <= 4:
            ly += ": " + _c4_ds_vt([(X, Y) for X in dinh for Y in dinh if X != Y])
        return de, dap, ly + ".", [k * (k - 1) // 2, k, k * k, 2 * k]
    if kieu == 1:
        k = random.choice([4, 5, 6, 7])
        ten = ", ".join("$%s$" % c for c in "ABCDEFG"[:k])
        X = random.choice("ABCDEFG"[:k])
        dau = random.random() < 0.5
        de = (r"Given $%d$ distinct points %s. How many nonzero vectors have %s $%s$ and have their %s point among the "
              r"given points?" % (k, ten, "initial point" if dau else "terminal point", X, "terminal" if dau else "initial"))
        dap = k - 1
        khac = [c for c in "ABCDEFG"[:k] if c != X]
        ly = (r"The %s point must differ from $%s$ (the vector must be nonzero), " r"so there are $%d$ vectors: %s."
              % ("terminal" if dau else "initial", X, dap, _c4_ds_vt([(X, Y) if dau else (Y, X) for Y in khac])))
        return de, dap, ly, [k, 2 * (k - 1), k * (k - 1)]
    k = random.choice([3, 4, 5])
    de = (r"Given $%d$ distinct points, no three of which are collinear. How many nonzero vectors have "
          r"their initial point and terminal point among the given points?" % k)
    dap = k * (k - 1)
    ly = (r"Each pair of distinct points $X$, $Y$ gives exactly two vectors $\overrightarrow{XY}$ and $\overrightarrow{YX}$. There are $%d$ "
          r"pairs of points, so there are $2 \cdot %d = %d$ vectors." % (k * (k - 1) // 2, k * (k - 1) // 2, dap))
    return de, dap, ly, [k * (k - 1) // 2, k * k, 2 * k]


def L10_C4_B7_NB037_MC_B_01(socau, dang=1):
    r"""Đếm số vectơ khác vectơ-không có điểm đầu, điểm cuối thuộc $n$ điểm cho trước (các đỉnh của đa giác, $n$ điểm
    không có ba điểm thẳng hàng; hoặc cố định điểm đầu / điểm cuối). Lời giải liệt kê khi $n \le 4$.

    CLAUDE THEM 01/10/2026 - theo phan dang 1, MC 12, 14, 15, TL 4 tai lieu CĐ day them "Khai niem vecto". Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dap, ly, ung = _c4_dem_diem()
        cau += MC_SA_answer_text(de, "$%d$" % dap, ["$%d$" % x for x in _c4_nhieu_so(dap, ung)], ly, 0, 0, dang)
    return cau


def L10_C4_B7_NB037_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB037_MC_A (cùng kiểu, cùng Dang): cho hình, xét bốn cặp vectơ có điểm
    mút thuộc hình, hỏi có bao nhiêu cặp cùng hướng (hoặc ngược hướng). Quan hệ do Python tính từ toạ độ.

    CLAUDE THEM 14/10/2026 theo quy uoc cua co Lan (MC_x va SA_x cung kieu, cung chu cai). Co Lan duyet.
    """
    cau = ""
    for _ in range(socau):
        H = _c4_chon_hinh("nb037_a")
        pb = _c4_pb_huong(H)
        cap = {}  # khoá = tập hai vectơ -> (u, w, cùng phương, cùng hướng)
        for p in pb:
            cap.setdefault(frozenset([p[2], p[3]]), (p[2], p[3], p[4], p[5]))
        ds = list(cap.values())
        hoi = random.choice(["same direction", "opposite direction"])
        kt = (lambda c: c[3]) if hoi == "same direction" else (lambda c: c[2] and not c[3])
        cp = [c for c in ds if c[2]]
        kcp = [c for c in ds if not c[2]]
        for _lan in range(200):
            # ba cặp cùng phương (dễ nhầm hướng) và một cặp không cùng phương; đáp số từ 1 đến 3
            chon = random.sample(cp, 3) + random.sample(kcp, 1)
            random.shuffle(chon)
            if 1 <= sum(1 for c in chon if kt(c)) <= 3:
                break
        dap = sum(1 for c in chon if kt(c))
        dong = r"\\ ".join(r"%d) $%s$ and $%s$" % (i + 1, _vt(*c[0]), _vt(*c[1])) for i, c in enumerate(chon))
        de = H["mo"] + r" Consider four pairs of vectors: \\ " + dong + r"\\ How many pairs of vectors have the %s?" % hoi
        ly = []
        for i, c in enumerate(chon):
            mo_ta = ("same direction" if c[3] else "opposite direction") if c[2] else "not collinear (the support lines intersect)"
            ly.append(r"Pair %d: $%s$ and $%s$: %s." % (i + 1, _vt(*c[0]), _vt(*c[1]), mo_ta))
        ly = r"\\ ".join(ly) + r"\\ So there are $%d$ pairs of vectors with the %s." % (dap, hoi)
        ung = [4 - dap, dap + 1, dap - 1, 3, 2]
        cau += MC_SA_answer_const(de, str(dap), [str(x) for x in _c4_nhieu_so(dap, ung)], ly, _c4_tikz(H), 0, dang)
    return cau


def L10_C4_B7_NB037_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB037_MC_B (cùng Dang).

    CLAUDE THEM 01/10/2026. DOI ID 14/10/2026: NB037_SA_A -> NB037_SA_B (cung dang voi MC_B, cung chu cai); co Lan duyet.
    """
    cau = ""
    for _ in range(socau):
        de, dap, ly, ung = _c4_dem_diem()
        cau += MC_SA_answer_const(de, str(dap), [str(x) for x in _c4_nhieu_so(dap, ung)], ly, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB037_MC_C / SA_B: đếm vectơ cùng phương, cùng hướng, ngược hướng với một vectơ trong hình
# ---------------------------------------------------------------------
def _c4_cau_dem(qh_ds, ten_kho):
    for _ in range(50):
        H = _c4_chon_hinh(ten_kho)
        qh = random.choice(qh_ds)
        v = _c4_chon_vt(H, qh, 1, 12)
        if v:
            break
    ds = _c4_loc(H, v, qh)
    ten_diem = ", ".join("$%s$" % t for t in H["P"])
    de = (H["mo"] + r" How many vectors other than vector $%s$ are %s $%s$ and have " r"their initial and terminal points among the points %s?"
          % (_vt(*v), "equal to vector" if qh == "bang" else _C4_TEN_QH[qh] + " with", _vt(*v), ten_diem))
    ly = _c4_ly_qh(H, v, qh, ds)
    khac = [len(_c4_loc(H, v, q)) for q in ("cung_phuong", "cung_huong", "nguoc_huong", "bang") if q != qh]
    return H, de, len(ds), ly, khac + [len(ds) + 1]


def L10_C4_B7_NB037_MC_C_01(socau, dang=1):
    r"""Đếm số vectơ (điểm đầu, điểm cuối thuộc các điểm của hình, khác vectơ đã cho) cùng phương, cùng hướng hoặc
    ngược hướng với một vectơ cho trước; kho hình xoay vòng; lời giải liệt kê các vectơ.

    CLAUDE THEM 01/10/2026 - theo phan dang 2, MC 20, 21, 27, TF 1, 6, 7 tai lieu CĐ day them "Khai niem vecto"
    (tai lieu khi tinh ca vecto da cho, khi khong - o day luon ghi ro "khac vecto da cho"). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        H, de, dap, ly, ung = _c4_cau_dem(["cung_phuong", "cung_huong", "nguoc_huong"], "nb037_c")
        cau += MC_SA_answer_text(de, "$%d$" % dap, ["$%d$" % x for x in _c4_nhieu_so(dap, ung)], ly, _c4_tikz(H), 0, dang)
    return cau


def L10_C4_B7_NB037_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB037_MC_C (cùng Dang).

    CLAUDE THEM 01/10/2026. DOI ID 14/10/2026: NB037_SA_B -> NB037_SA_C (cung dang voi MC_C, cung chu cai); co Lan duyet.
    """
    cau = ""
    for _ in range(socau):
        H, de, dap, ly, ung = _c4_cau_dem(["cung_phuong", "cung_huong", "nguoc_huong"], "nb037_c")
        cau += MC_SA_answer_const(de, str(dap), [str(x) for x in _c4_nhieu_so(dap, ung)], ly, _c4_tikz(H), 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB037_MC_D: khẳng định đúng / sai về khái niệm vectơ, cùng phương, cùng hướng (kho xoay vòng)
# ---------------------------------------------------------------------
_C4_KN_NB037 = [  # (phát biểu, đúng?, lí do)
    (r"A vector is a directed line segment", True, "that is the definition of a vector"),
    (r"Vector $\overrightarrow{AB}$ has initial point $A$ and terminal point $B$", True, "it follows from the vector notation"),
    (r"The magnitude of vector $\overrightarrow{AB}$ equals the length of segment $AB$", True, "it follows from the definition of vector length"),
    (r"The vectors $\overrightarrow{AB}$ and $\overrightarrow{BA}$ have the same length", True, "both are equal to $AB$"),
    (r"The support line of vector $\overrightarrow{AB}$ is line $AB$", True, "the supporting line is the line passing through the initial point " "and the terminal point"),
    (r"Two collinear vectors have the same direction or opposite directions", True, "this is a remark in the textbook"),
    (r"If two vectors have the same direction, then they are collinear", True, "same direction is only considered for two collinear vectors"),
    (r"The vectors $\overrightarrow{AB}$ and $\overrightarrow{BA}$ have opposite directions", True, "two vectors with the same line of action pointing in opposite directions"),
    (r"Three distinct points $A$, $B$, $C$ are collinear if and only if " r"$\overrightarrow{AB}$ and $\overrightarrow{AC}$ are collinear", True,
     "two vectors with a common initial point $A$ are collinear if and only if they have the same support line"),
    (r"If $\overrightarrow{a}$, $\overrightarrow{b}$ have the same direction as $\overrightarrow{c}$ (all different from $\overrightarrow{0}$), then "
     r"$\overrightarrow{a}$ has the same direction as $\overrightarrow{b}$", True, "the same-direction relation is transitive for nonzero vectors"),
    (r"Two collinear vectors have the same direction", False, "they can have opposite directions, for example $\\overrightarrow{AB}$ and $\\overrightarrow{BA}$"),
    (r"If two vectors have the same length, then they are collinear", False, "magnitude does not determine direction, for example two adjacent sides of a square"),
    (r"If two vectors are collinear, then they have the same supporting " r"line", False, "their support lines may only be parallel"),
    (r"The vectors $\overrightarrow{AB}$ and $\overrightarrow{BA}$ have the same direction", False, "they have the opposite direction"),
    (r"Two vectors in opposite direction are not collinear", False, "the opposite direction is only considered for two collinear " "vectors"),
    (r"The magnitude of vector $\overrightarrow{AB}$ differs from the magnitude of vector $\overrightarrow{BA}$", False, "both are equal to $AB$"),
    (r"A vector is a line segment", False, "a vector is a DIRECTED line segment (its initial point and " "terminal point must be specified)"),
    (r"Two vectors collinear with a third vector (different from $\overrightarrow{0}$) have the same direction", False,
     "they are only collinear and may have opposite direction"),
    (r"Three distinct points $A$, $B$, $C$ are collinear if and only if $\overrightarrow{AB}$ and $\overrightarrow{AC}$ have the same direction", False,
     "if $A$ lies between $B$ and $C$, then the two vectors have the " "opposite direction while the three points are still collinear"),
]


def _c4_mc_kho(kho, ten_kho, dang, debai_mo, giai_mo):
    cau = ""
    hoi = random.random() < 0.55
    idx = _c4_uu_tien(ten_kho, list(range(len(kho))))
    d = [i for i in idx if kho[i][1] == hoi][:1]
    s = [i for i in idx if kho[i][1] != hoi][:3]
    _c4_danh_dau(ten_kho, d + s)
    debai = debai_mo + r" Which of the following statements is %s?" % (r"\textbf{true}" if hoi else r"\textbf{false}")
    giai = giai_mo + r"\\ ".join(r"``%s'' is a %s statement because %s." % (kho[i][0], "true" if kho[i][1] else "false", kho[i][2])
                                 for i in d + s)
    return _MC_khong_cham(debai, kho[d[0]][0], [kho[i][0] for i in s], giai, 0, 0, dang)


def L10_C4_B7_NB037_MC_D_01(socau, dang=1):
    r"""Khẳng định đúng (sai) về khái niệm vectơ, giá, độ dài, cùng phương, cùng hướng, ngược hướng; kho 19 khẳng
    định lấy xoay vòng.

    CLAUDE THEM 01/10/2026 - theo MC 1, 2, 5, 11, TL 13 tai lieu CĐ day them "Khai niem vecto" (MC 1 tai lieu co hai
    phuong an dung). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        cau += _c4_mc_kho(_C4_KN_NB037, "c4_kn_nb037", dang, "", "")
    return cau


def L10_C4_B7_NB037_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB037_MC_D (cùng kiểu, cùng Dang): cho bốn khẳng định về khái niệm vectơ,
    giá, độ dài, cùng phương, cùng hướng, ngược hướng (lấy từ kho 19 khẳng định của MC_D); hỏi có bao nhiêu khẳng
    định đúng. Kho lấy xoay vòng riêng.

    CLAUDE THEM 14/10/2026 theo quy uoc cua co Lan (MC_x va SA_x cung kieu, cung chu cai). Co Lan duyet.
    """
    cau = ""
    for _ in range(socau):
        ten = "c4_kn_nb037_sa"
        so_dung = random.choice([1, 2, 2, 3])
        idx = _c4_uu_tien(ten, list(range(len(_C4_KN_NB037))))
        d = [i for i in idx if _C4_KN_NB037[i][1]][:so_dung]
        sai = [i for i in idx if not _C4_KN_NB037[i][1]][:4 - so_dung]
        chon = d + sai
        _c4_danh_dau(ten, chon)
        random.shuffle(chon)
        dap = so_dung
        de = (r"Consider the following statements: \\ " + r"\\ ".join(r"%d) %s;" % (k + 1, _C4_KN_NB037[i][0]) for k, i in enumerate(chon))
              + r"\\ How many of these statements are true?")
        ly = r"\\ ".join(r"Statement %d is %s because %s." % (k + 1, "true" if _C4_KN_NB037[i][1] else "false", _C4_KN_NB037[i][2])
                           for k, i in enumerate(chon)) + r"\\ So there are $%d$ true statements." % dap
        ung = [4 - dap, dap + 1, dap - 1, 0, 4]
        cau += MC_SA_answer_const(de, str(dap), [str(x) for x in _c4_nhieu_so(dap, ung)], ly, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB037_MC_E / SA_C: độ dài vectơ trong hình đơn giản
# ---------------------------------------------------------------------
def _c4_do_dai(so):
    """Một câu độ dài vectơ. so=True: số liệu bằng số (trả lời ngắn, làm tròn hàng phần mười); False: theo a.
    Trả về (mô tả, vectơ, độ dài sympy, lời giải, các độ dài nhiễu, hình H)."""
    a = random.choice([2, 3, 4, 5, 6, 8, 10]) if so else _Sym4("a", positive=True)
    kieu = random.choice(["hcn", "vuong", "thoi", "luc_giac", "tg_deu"] if not so else ["hcn", "vuong", "thoi", "luc_giac", "tg_deu"])
    if kieu == "hcn":
        p, q = random.choice([(3, 4), (6, 8), (5, 12), (8, 6), (4, 3), (12, 5), (8, 15), (9, 12)])
        if not so:
            p, q = random.choice([(1, 2), (2, 1), (1, 3), (3, 1)])
            p, q = p * a, q * a
            if random.random() < 0.5:
                p, q = a, a * _sq4(3)
        H = _c4_hinh("hcn")
        A, B, C, D = H["da_giac"]
        tl = 4.4 / float(max(p, q) if so else max(p / a, q / a))
        pp, qq = (float(p) * tl, float(q) * tl) if so else (float(p / a) * tl, float(q / a) * tl)
        H["P"].update({A: (0, 0), B: (pp, 0), C: (pp, qq), D: (0, qq), H["tam"]: (pp / 2, qq / 2)})
        O = H["tam"]
        cheo = _sq4(p ** 2 + q ** 2)
        mo = r"Given rectangle $%s$ with center $%s$ and $%s = %s$, $%s = %s$." % ("".join(H["da_giac"]), O, A + B, _c4_tx(p), A + D, _c4_tx(q))
        v, L = random.choice([((A, C), cheo), ((B, D), cheo), ((O, A), cheo / 2), ((C, O), cheo / 2), ((D, B), cheo)])
        ly = (r"$%s = %s = \sqrt{%s^{2} + %s^{2}} = %s$ (Pythagorean theorem)" % (A + C, B + D, _c4_ng(p), _c4_ng(q), _c4_tx(cheo))
              + ("" if O not in v else r", $%s$ is the midpoint of the diagonal, so $%s = \dfrac{%s}{2} = " r"%s$" % (O, v[0] + v[1], A + C, _c4_tx(cheo / 2))))
        return mo, v, L, ly, [p + q, cheo / 2 if O not in v else cheo, abs(q - p) if p != q else 2 * p], H
    if kieu == "vuong":
        H = _c4_hinh("vuong")
        A, B, C, D = H["da_giac"]
        O = H["tam"]
        mo = r"Given square $%s$ with center $%s$ and side length $%s$." % ("".join(H["da_giac"]), O, _c4_tx(a))
        cheo = a * _sq4(2)
        v, L = random.choice([((A, C), cheo), ((D, B), cheo), ((O, B), cheo / 2), ((A, O), cheo / 2), ((C, D), a)])
        ly = r"$%s = %s\sqrt{2}$ (diagonal of a square)" % (A + C, _c4_tx(a))
        if O in v:
            ly += r", $%s$ is the midpoint of the diagonal, so $%s = \dfrac{%s}{2} = " r"%s$" % (O, v[0] + v[1], A + C, _c4_tx(cheo / 2))
        elif v == (C, D):
            ly = r"$%s = %s$ (side of the square)" % (C + D, _c4_tx(a))
        return mo, v, L, ly, [a, 2 * a, cheo / 2 if O not in v else cheo, a * _sq4(3)], H
    if kieu == "thoi":
        H = _c4_hinh("thoi")
        A, B, C, D = H["da_giac"]
        O = H["tam"]
        if so:
            d1, d2 = random.choice([(6, 8), (8, 6), (10, 24), (12, 16), (16, 12), (24, 10)])
            tl = 4.8 / max(d1, d2)
            H["P"].update({A: (0, d2 * tl / 2), B: (d1 * tl / 2, 0), C: (d1 * tl, d2 * tl / 2), D: (d1 * tl / 2, d2 * tl),
                           O: (d1 * tl / 2, d2 * tl / 2)})
            mo = r"Given rhombus $%s$ with center $%s$, where $%s = %d$, $%s = %d$." % ("".join(H["da_giac"]), O, A + C, d1, B + D, d2)
            canh = _sq4((d1 / _R4(2)) ** 2 + (d2 / _R4(2)) ** 2)
            v, L = random.choice([((A, B), canh), ((C, D), canh), ((O, A), _R4(d1, 2)), ((B, O), _R4(d2, 2))])
            ly = (r"The two diagonals are perpendicular at the midpoint $%s$: $%s = %s$, $%s = %s$; $%s = \sqrt{%s^{2} + %s^{2}} = %s$"
                  % (O, O + A, _c4_tx(_R4(d1, 2)), O + B, _c4_tx(_R4(d2, 2)), A + B, _c4_tx(_R4(d1, 2)), _c4_tx(_R4(d2, 2)), _c4_tx(canh)))
            return mo, v, L, ly, [d1, d2, _R4(d1 + d2, 2)], H
        r3 = math.sqrt(3)
        H["P"].update({A: (0, 1.2), B: (1.2 * r3, 0), C: (2.4 * r3, 1.2), D: (1.2 * r3, 2.4), O: (1.2 * r3, 1.2)})
        mo = (r"Given rhombus $%s$ with center $%s$, side length $%s$ and $\widehat{%s} = 60^{\circ}$."
              % ("".join(H["da_giac"]), O, _c4_tx(a), B + A + D))
        v, L = random.choice([((B, D), a), ((A, C), a * _sq4(3)), ((O, A), a * _sq4(3) / 2), ((D, O), a / 2)])
        ly = (r"Triangle $%s$ is isosceles at $%s$ with a $60^{\circ}$ angle, so "
              r"it is equilateral: $%s = %s$. $%s$ is the altitude of an "
              r"equilateral triangle with side $%s$ so $%s = "
              r"\dfrac{%s\sqrt{3}}{2}$, $%s = 2%s = %s\sqrt{3}$" % (A + B + D, A, B + D, _c4_tx(a), A + O, _c4_tx(a), A + O,
                                                                              _c4_tx(a), A + C, A + O, _c4_tx(a)))
        return mo, v, L, ly, [a, a * _sq4(3), a * _sq4(3) / 2, a / 2, a * _sq4(2)], H
    if kieu == "luc_giac":
        H = _c4_hinh("luc_giac")
        mo = r"Given a regular hexagon $ABCDEF$ with center $O$ and side length $%s$." % _c4_tx(a)
        v, L = random.choice([(("A", "D"), 2 * a), (("B", "E"), 2 * a), (("O", "C"), a), (("A", "C"), a * _sq4(3)),
                              (("F", "B"), a * _sq4(3)), (("E", "O"), a)])
        ly = (r"The regular hexagon is divided into six equilateral triangles of side $%s$ sharing vertex $O$, so $OA = OB = \ldots = %s$, "
              r"$AD = BE = CF = 2 \cdot %s$; $AC = BD = \ldots = 2 \cdot \dfrac{%s\sqrt{3}}{2} = %s\sqrt{3}$ (twice the altitude of an "
              r"equilateral triangle)" % (_c4_tx(a), _c4_tx(a), _c4_tx(a), _c4_tx(a), _c4_tx(a)))
        return mo, v, L, ly, [a, 2 * a, a * _sq4(3), a * _sq4(3) / 2, a * _sq4(2)], H
    H = _c4_hinh("tg_trung_diem")
    M, N, Q = [t for t in H["P"] if t not in "ABC"]
    r3 = math.sqrt(3)
    H["P"].update({"A": (2.2, 2.2 * r3), "B": (0, 0), "C": (4.4, 0), M: (2.2, 0), N: (3.3, 1.1 * r3), Q: (1.1, 1.1 * r3)})
    mo = (r"Given equilateral triangle $ABC$ with side length $%s$; $%s$, $%s$, $%s$ are the midpoints of $BC$, $CA$, $AB$ respectively."
          % (_c4_tx(a), M, N, Q))
    v, L = random.choice([(("A", M), a * _sq4(3) / 2), ((N, "B"), a * _sq4(3) / 2), ((M, N), a / 2), ((Q, "B"), a / 2)])
    ly = (r"The median of an equilateral triangle is also an altitude, with length $\dfrac{%s\sqrt{3}}{2}$; the segment joining two midpoints "
          r"(the midsegment) and half a side are both equal to $\dfrac{%s}{2}$" % (_c4_tx(a), _c4_tx(a)))
    return mo, v, L, ly, [a, a * _sq4(3), a * _sq4(3) / 2, a / 2, a * _sq4(2) / 2], H


def _c4_tx(x):
    """Viết độ dài kiểu đề thi: a\\sqrt{3}, \\dfrac{a\\sqrt{3}}{2}, 2a, 10, 5\\sqrt{2}..."""
    x = _ns4(x)
    a = [t for t in x.free_symbols]
    he = _ns4(x / a[0]) if a else x
    c, r = he.as_coeff_Mul()
    c = _R4(c)
    can = "" if r == 1 else r"\sqrt{%s}" % _lx4(r ** 2)
    if r != 1 and not (r ** 2).is_Integer:
        return _lx4(x).replace(r"\frac", r"\dfrac")
    chu = "a" if a else ""
    tu = ("" if (c.p == 1 and (chu or can)) else "%d" % c.p) + chu + can
    if c.p == 1 and not chu and not can:
        tu = "1"
    return tu if c.q == 1 else r"\dfrac{%s}{%d}" % (tu, c.q)


def _c4_ng(x):
    x = _ns4(x)
    s = _c4_tx(x)
    return s if x.is_Atom else r"\left(%s\right)" % s


def L10_C4_B7_TH037_MC_A_01(socau, dang=1):
    r"""Độ dài vectơ trong hình đơn giản (hình chữ nhật, hình vuông, hình thoi góc $60^{\circ}$, lục giác đều, tam giác
    đều có trung điểm), độ dài theo $a$; một bước Pythagore hoặc đường cao tam giác đều.

    CLAUDE THEM 01/10/2026 - theo phan dang 3, MC 29 - 36, TL 5, 6 tai lieu CĐ day them "Khai niem vecto" (chi lay cac
    cau mot buoc tinh; cau trong tam, trung diem AG, phan giac... vuot muc NB037 nen khong lay). Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        mo, v, L, ly, ung, H = _c4_do_dai(False)
        dap = "$%s$" % _c4_tx(L)
        nh = [u for u in dict.fromkeys("$%s$" % _c4_tx(x) for x in ung) if u != dap]
        if len(nh) < 3:
            continue
        so += 1
        debai = mo + r" The length of vector $%s$ equals" % _vt(*v)
        giai = ly.replace(r"\frac", r"\dfrac") + r".\\ Hence $\left|%s\right| = %s = %s$." % (_vt(*v), v[0] + v[1], dap.strip("$"))
        cau += MC_SA_answer_text(debai, dap, nh[:3], giai, _c4_tikz(H), 0, dang)
    return cau


def L10_C4_B7_TH037_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - độ dài vectơ trong hình đơn giản với số liệu bằng số; kết quả làm tròn đến hàng phần mười
    (bản trả lời ngắn của NB037_MC_E, cùng Dang).

    CLAUDE THEM 01/10/2026. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        mo, v, L, ly, ung, H = _c4_do_dai(True)
        gt = float(L)
        s = _xx4(round(gt, 1), 1)
        if len(s) > 4:
            continue
        so += 1
        chinh_xac = abs(gt - round(gt, 1)) < 1e-9
        debai = mo + r" Find the length of vector $%s$%s." % (_vt(*v), "" if chinh_xac else " (round the result to the nearest tenth)")
        giai = ly + r".\\ Hence $\left|%s\right| = %s %s %s$." % (_vt(*v), _c4_tx(L), "=" if chinh_xac else r"\approx", s)
        nh = [_xx4(round(float(x), 1), 1) for x in ung]
        nh = [x for x in dict.fromkeys(nh) if x != s and len(x) <= 4]
        cau += MC_SA_answer_const(debai, s, (nh + ["1", "2", "3"])[:3] if len(nh) < 3 else nh[:3], giai, _c4_tikz(H), 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB038_MC_A_02: đẳng thức vectơ bằng nhau đúng / sai trong hình (kho hình)
# ---------------------------------------------------------------------
def L10_C4_B7_NB038_MC_A_02(socau, dang=1):
    r"""Cách hỏi khác của NB038_MC_A_01 với KHO HÌNH xoay vòng: trong bốn đẳng thức $\overrightarrow{XY} =
    \overrightarrow{ZT}$, chọn đẳng thức đúng (hoặc sai). Các đẳng thức sai đều là cặp dễ nhầm: cùng độ dài nhưng
    ngược hướng, cùng hướng nhưng khác độ dài, cùng độ dài nhưng không cùng phương.

    CLAUDE THEM 01/10/2026 - theo phan dang 2, MC 22 - 26, 41, TF 5, 8, 9 tai lieu CĐ day them "Khai niem vecto". Co Lan
    duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        H = _c4_chon_hinh("nb038_a")
        vts = _c4_tat_ca_vt(H)
        do = lambda w: math.hypot(*_c4_v(H, *w))
        dung, sai = [], []
        for i, u in enumerate(vts):
            for w in vts[i + 1:]:
                if set(u) == set(w):
                    continue
                a, b = _c4_v(H, *u), _c4_v(H, *w)
                cung_do = abs(do(u) - do(w)) < 1e-7
                if _c4_bang(a, b):
                    dung.append((u, w, "have the same direction and the same length"))
                elif cung_do and _c4_cp(a, b):
                    sai.append((u, w, "opposite direction"))
                elif _c4_ch(a, b):
                    sai.append((u, w, "same direction but different magnitudes"))
                elif cung_do and not _c4_cp(a, b):
                    sai.append((u, w, "have the same length but are not collinear"))
        hoi = random.random() < 0.55
        A_, B_ = (dung, sai) if hoi else (sai, dung)
        if not A_ or len(B_) < 3:
            continue
        random.shuffle(A_)
        random.shuffle(B_)
        chon = [A_[0]] + B_[:3]
        so += 1
        tex = lambda c: r"$%s = %s$" % (_vt(*c[0]), _vt(*c[1]))
        debai = H["mo"] + r" Which of the following equalities is %s?" % (r"\textbf{true}" if hoi else r"\textbf{false}")
        giai = (r"Two vectors are equal when they have the same direction and the same magnitude.\\ "
                + r"\\ ".join(r"$%s$ and $%s$ %s, so %s is %s." % (_vt(*c[0]), _vt(*c[1]), c[2], tex(c), "true" if c in dung else "false")
                              for c in chon))
        cau += MC_SA_answer_text(debai, tex(chon[0]), [tex(c) for c in chon[1:]], giai, _c4_tikz(H), 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB038_MC_B / SA_A: đếm số vectơ bằng một vectơ cho trước
# ---------------------------------------------------------------------
def L10_C4_B7_NB038_MC_B_01(socau, dang=1):
    r"""Đếm số vectơ (điểm đầu, điểm cuối thuộc các điểm của hình, khác vectơ đã cho) bằng một vectơ cho trước;
    kho hình xoay vòng; lời giải liệt kê.

    CLAUDE THEM 01/10/2026 - theo MC 20, 21, 37, 39, TF 7, 10, TL 18 tai lieu CĐ day them "Khai niem vecto". Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        H, de, dap, ly, ung = _c4_cau_dem(["bang"], "nb038_b")
        cau += MC_SA_answer_text(de, "$%d$" % dap, ["$%d$" % x for x in _c4_nhieu_so(dap, ung)], ly, _c4_tikz(H), 0, dang)
    return cau


def L10_C4_B7_NB038_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB038_MC_B (cùng Dang).

    CLAUDE THEM 01/10/2026. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        H, de, dap, ly, ung = _c4_cau_dem(["bang"], "nb038_b")
        cau += MC_SA_answer_const(de, str(dap), [str(x) for x in _c4_nhieu_so(dap, ung)], ly, _c4_tikz(H), 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB038_MC_C: khẳng định về hai vectơ bằng nhau, vectơ-không (kho xoay vòng)
# ---------------------------------------------------------------------
_C4_KN_NB038 = [
    (r"Equal vectors have the same length", True, "two equal vectors are two vectors with the same direction and the same magnitude"),
    (r"If two vectors are equal, then they have the same direction", True, "by the definition of equal vectors"),
    (r"Two equal vectors are collinear", True, "they have the same direction, so they are collinear"),
    (r"The zero vector is a vector whose initial point and terminal " r"point coincide", True, "that is the definition of the zero vector"),
    (r"The zero vector has magnitude $0$", True, "$\\left|\\overrightarrow{AA}\\right| = 0$"),
    (r"The zero vector is collinear with every vector and has the same direction as every vector", True, "that is the convention in the textbook"),
    (r"$\overrightarrow{AA} = \overrightarrow{BB}$ for all points $A$, $B$", True, "all zero vectors are equal and are denoted by " "$\\overrightarrow{0}$"),
    (r"If $\overrightarrow{a} = \overrightarrow{b}$ and $\overrightarrow{b} = \overrightarrow{c}$ then $\overrightarrow{a} = \overrightarrow{c}$", True,
     "three vectors with the same direction and the same magnitude"),
    (r"Quadrilateral $ABCD$ is a parallelogram if and only if $\overrightarrow{AB} = \overrightarrow{DC}$ ($A$, $B$, $C$, $D$ not collinear)", True,
     "$\\overrightarrow{AB} = \\overrightarrow{DC}$ means $AB \\parallel DC$, $AB = DC$ and the same direction"),
    (r"If two vectors have the same length, then they are equal", False, "they must also have the same direction"),
    (r"If two vectors are collinear and have the same length, then they " r"are equal", False, "they can have opposite directions, for example $\\overrightarrow{AB}$ and $\\overrightarrow{BA}$"),
    (r"Two vectors with the same direction are equal", False, "they must also have the same length"),
    (r"$\overrightarrow{AB} = \overrightarrow{BA}$ for all points $A$, $B$", False, "when $A \\ne B$ the two vectors have opposite directions"),
    (r"The zero vector is not collinear with any vector", False, "the zero vector is collinear with every vector"),
    (r"The magnitude of the zero vector equals $1$", False, "the magnitude of the zero vector equals $0$"),
    (r"$\overrightarrow{AB} = \overrightarrow{CD}$ if and only if $AB = " r"CD$", False, "$AB = CD$ only says that the two vectors have the same length"),
    (r"If $\overrightarrow{AB} = \overrightarrow{CD}$, then $A$, $B$, $C$, $D$ are the four vertices of parallelogram $ABCD$", False,
     "in that case $ABDC$ (or four collinear points) is the correct statement, not $ABCD$"),
    (r"If $\overrightarrow{AB} = \overrightarrow{AC}$ then $B$ is different from $C$", False, "if two vectors with the same initial point are equal, then $B " "\\equiv C$"),
]


def L10_C4_B7_NB038_MC_C_01(socau, dang=1):
    r"""Khẳng định đúng (sai) về hai vectơ bằng nhau, vectơ-không; kho 18 khẳng định lấy xoay vòng.

    CLAUDE THEM 01/10/2026 - theo MC 3, 7, 13, 16, 40 tai lieu CĐ day them "Khai niem vecto" (bo cac khang dinh ve vecto doi
    nhau - thuoc Bai 8). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        cau += _c4_mc_kho(_C4_KN_NB038, "c4_kn_nb038", dang, "", "")
    return cau


# ---------------------------------------------------------------------
# NB038_MC_D: dựng điểm từ hai vectơ bằng nhau -> hình bình hành
# ---------------------------------------------------------------------
def L10_C4_B7_NB038_MC_D_01(socau, dang=1):
    r"""Ba điểm $A$, $B$, $C$ không thẳng hàng và điểm $D$ thoả mãn một đẳng thức vectơ bằng nhau
    ($\overrightarrow{AB} = \overrightarrow{DC}$, $\overrightarrow{AB} = \overrightarrow{CD}$, $\overrightarrow{AD} =
    \overrightarrow{BC}$...): tứ giác nào là hình bình hành. Python kiểm tra bằng toạ độ.

    CLAUDE THEM 01/10/2026 - theo MC 25, TF 9, 10, 19, TL 12, 15 tai lieu CĐ day them "Khai niem vecto". Co Lan duyet lai.
    """
    import itertools
    cau = ""
    for _ in range(socau):
        ten = random.choice(["ABC", "MNP", "EFG"])
        X, Y, Z = ten
        T = {"ABC": "D", "MNP": "Q", "EFG": "H"}[ten]
        P = {X: (0, 0), Y: (random.randint(3, 5), 0), Z: (random.randint(1, 4), random.randint(2, 4))}
        cap = random.choice([((X, Y), (T, Z)), ((X, Y), (Z, T)), ((X, T), (Y, Z)), ((Y, X), (Z, T)), ((T, X), (Z, Y)),
                             ((X, Z), (T, Y)), ((X, Z), (Y, T)), ((Z, Y), (T, X))])
        (p1, p2), (q1, q2) = cap
        # q2 - q1 = p2 - p1, T là q1 hoặc q2 hoặc p1, p2
        ve = lambda a, b: (P[b][0] - P[a][0], P[b][1] - P[a][1])
        if T in (q1, q2):
            k = ve(p1, p2)
            P[T] = (P[q2][0] - k[0], P[q2][1] - k[1]) if T == q1 else (P[q1][0] + k[0], P[q1][1] + k[1])
        else:
            k = ve(q1, q2)
            P[T] = (P[p2][0] - k[0], P[p2][1] - k[1]) if T == p1 else (P[p1][0] + k[0], P[p1][1] + k[1])

        def la_hbh(o):
            a, b, c, d = (P[t] for t in o)
            return abs(a[0] + c[0] - b[0] - d[0]) < 1e-9 and abs(a[1] + c[1] - b[1] - d[1]) < 1e-9
        tu = [X + Y + Z + T, X + Y + T + Z, X + Z + Y + T]
        dung = [o for o in tu if la_hbh(o)][0]
        sai = [o for o in tu if o != dung]
        pa_d = r"$%s$ is a parallelogram" % dung
        nhieu = [r"$%s$ is a parallelogram" % o for o in sai] + [r"$%s$ is the midpoint of $%s$" % (T, X + Z)]
        debai = (r"Given three non-collinear points $%s$, $%s$, $%s$ and a point " r"$%s$ satisfying $%s = %s$. Which of the following statements is " r"true?"
                 % (X, Y, Z, T, _vt(p1, p2), _vt(q1, q2)))
        giai = (r"$%s = %s$, so the segments $%s$ and $%s$ are parallel (the three points are not collinear), equal in length, and the two vectors have the same direction. "
                r"Therefore quadrilateral $%s$ (taken in the order $%s \to %s \to %s \to %s$) is a parallelogram: the two opposite sides $%s$ and $%s$ are parallel and "
                r"equal." % (_vt(p1, p2), _vt(q1, q2), p1 + p2, q1 + q2, dung, *dung, dung[0] + dung[1], dung[3] + dung[2]))
        cau += _MC_khong_cham(debai, pa_d, nhieu, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH039: biểu diễn đại lượng thực tiễn bằng vectơ
# ---------------------------------------------------------------------
_C4_HUONG = {(1, 0): "east", (-1, 0): "west", (0, 1): "north", (0, -1): "south",
             (1, 1): "northeast", (-1, 1): "northwest", (1, -1): "southeast", (-1, -1): "southwest"}


def _c4_luoi(ds, nhan, rong=10, cao=6, la_ban=False):
    """Lưới ô vuông với các mũi tên ds = [(x0, y0, dx, dy)] và nhãn."""
    out = ["\\begin{tikzpicture}[>=stealth,x=0.5cm,y=0.5cm,scale=1]",
           "\\draw[gray!50, very thin] (0,0) grid (%d,%d);" % (rong, cao)]
    for (x0, y0, dx, dy), t in zip(ds, nhan):
        out.append("\\draw[->, very thick] (%d,%d) -- (%d,%d) node[midway, %s]{\\footnotesize $%s$};"
                   % (x0, y0, x0 + dx, y0 + dy, "above" if dy == 0 else "right", t))
    if la_ban:
        out.append("\\draw[->] (%d,%d) -- (%d,%d) node[above]{\\scriptsize North};" % (rong + 2, cao - 3, rong + 2, cao - 1))
        out.append("\\draw[->] (%d,%d) -- (%d,%d) node[right]{\\scriptsize East};" % (rong + 2, cao - 3, rong + 4, cao - 3))
    out.append("\\end{tikzpicture}")
    return "\n".join(out)


def _c4_dat_mui_ten(vec, rong=10, cao=6):
    """Đặt các mũi tên (dx, dy) không chồng nhau trên lưới."""
    for _ in range(500):
        ds, chiem = [], set()
        ok = True
        for dx, dy in vec:
            for _t in range(200):
                x0 = random.randint(max(0, -dx), min(rong, rong - dx))
                y0 = random.randint(max(0, -dy), min(cao, cao - dy))
                o = {(x0 + round(dx * t / 4), y0 + round(dy * t / 4)) for t in range(5)}
                vung = {(a + i, b + j) for a, b in o for i in (-1, 0, 1) for j in (-1, 0, 1)}
                if not (vung & chiem):
                    chiem |= o
                    ds.append((x0, y0, dx, dy))
                    break
            else:
                ok = False
                break
        if ok:
            return ds
    raise ValueError("khong dat duoc")


def L10_C4_B7_TH039_MC_B_01(socau, dang=1):
    r"""Các lực $\overrightarrow{F_1}, \ldots, \overrightarrow{F_4}$ được biểu diễn trên lưới ô vuông (mỗi cạnh ô ứng với
    $10$ N): chọn cặp lực cùng hướng / ngược hướng / bằng nhau. Python xét bằng toạ độ.

    CLAUDE THEM 01/10/2026 - theo TL 19 (Hinh 18), TL 14, 17 tai lieu CĐ day them "Khai niem vecto". Co Lan duyet lai.
    """
    import itertools
    cau = ""
    so = 0
    while so < socau:
        hoi = random.choice(["same direction", "opposite direction", "are equal"])
        goc = random.choice([(1, 0), (0, 1), (1, 1), (1, -1)])
        k1 = random.randint(2, 3)
        k2 = k1 if hoi == "are equal" else random.choice([k for k in (1, 2, 3) if k != k1] if hoi == "same direction" else [1, 2, 3])
        s2 = -1 if hoi == "opposite direction" else 1
        v1 = (goc[0] * k1, goc[1] * k1)
        v2 = (s2 * goc[0] * k2, s2 * goc[1] * k2)
        khac = [d for d in _C4_HUONG if d != goc and d != (-goc[0], -goc[1])]
        d3, d4 = random.sample(khac, 2)
        v3 = (d3[0] * random.randint(1, 3), d3[1] * random.randint(1, 3))
        v4 = (d4[0] * random.randint(1, 3), d4[1] * random.randint(1, 3))
        if hoi != "are equal":
            v3 = (goc[0] * (-s2) * random.randint(1, 3), goc[1] * (-s2) * random.randint(1, 3)) if random.random() < .5 else v3
        V = [v1, v2, v3, v4]
        random.shuffle(V)
        ten = [r"\overrightarrow{F_{%d}}" % (i + 1) for i in range(4)]
        def qh(a, b):
            if _c4_bang(a, b):
                return "are equal"
            if _c4_ch(a, b):
                return "same direction"
            if _c4_cp(a, b):
                return "opposite direction"
            return "not collinear"
        cap = list(itertools.combinations(range(4), 2))
        dung = [c for c in cap if qh(V[c[0]], V[c[1]]) == hoi or (hoi == "same direction" and qh(V[c[0]], V[c[1]]) == "are equal")]
        if len(dung) != 1:
            continue
        sai = [c for c in cap if c not in dung]
        random.shuffle(sai)
        try:
            ds = _c4_dat_mui_ten(V)
        except ValueError:
            continue
        so += 1
        tx = lambda c: r"$%s$ and $%s$" % (ten[c[0]], ten[c[1]])
        debai = (r"The forces $%s$ acting on objects are represented by vectors on a square grid as shown in the figure. Which pair of forces "
                 r"below is \textbf{%s}?" % ("$, $".join(ten), hoi))
        giai = r"\\ ".join(r"%s %s." % (tx(c), qh(V[c[0]], V[c[1]]) if qh(V[c[0]], V[c[1]]) != "not collinear" else
                                        "not collinear (the support lines intersect)") for c in dung + sai[:3])
        giai = r"Read the direction and length of each vector on the grid:\\ " + giai
        cau += MC_SA_answer_text(debai, tx(dung[0]), [tx(c) for c in sai[:3]], giai, _c4_luoi(ds, ten), 0, dang)
    return cau


def L10_C4_B7_TH039_MC_C_01(socau, dang=1):
    r"""Vận tốc trên lưới ô vuông có la bàn (mỗi cạnh ô ứng với $10$ km/h): vectơ nào biểu diễn vận tốc ``$v$ km/h theo
    hướng đông / tây / nam / bắc''. Nhiễu: đúng hướng sai độ lớn, đúng độ lớn ngược hướng, đúng độ lớn vuông góc.

    CLAUDE THEM 01/10/2026 - theo TL 9 (con bao di chuyen theo huong dong bac), TL 1 tai lieu CĐ day them "Khai niem vecto".
    Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        huong = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        k = random.randint(2, 4)
        k2 = random.choice([x for x in (1, 2, 3, 4, 5) if x != k])
        vuong = (huong[1], huong[0])
        V = [(huong[0] * k, huong[1] * k), (huong[0] * k2, huong[1] * k2), (-huong[0] * k, -huong[1] * k),
             (vuong[0] * k, vuong[1] * k)]
        thu_tu = list(range(4))
        random.shuffle(thu_tu)
        ten = [r"\overrightarrow{%s}" % c for c in "abcd"]
        try:
            ds = _c4_dat_mui_ten([V[i] for i in thu_tu], 10, 6)
        except ValueError:
            continue
        so += 1
        vi = {i: ten[thu_tu.index(i)] for i in range(4)}
        vat = random.choice(["a boat", "a storm", "a car", "a flock of birds", "an airplane"])
        debai = (r"On the square grid (see figure; up is north, right is east), each "
                 r"side of a grid square corresponds to $10$ km/h. Which vector "
                 r"represents the velocity of %s heading %s at a speed of $%d$ km/h?"
                 % (vat, _C4_HUONG[huong], 10 * k))
        giai = (r"The required vector points %s and has length $%d$ grid squares (corresponding to $%d$ km/h): it is $%s$.\\ $%s$ has the correct direction but "
                r"is $%d$ squares long; $%s$ is $%d$ squares long but points %s; $%s$ is $%d$ squares long but points %s."
                % (_C4_HUONG[huong], k, 10 * k, vi[0], vi[1], k2, vi[2], k, _C4_HUONG[(-huong[0], -huong[1])], vi[3], k,
                   _C4_HUONG[vuong]))
        cau += MC_SA_answer_text(debai, "$%s$" % vi[0], ["$%s$" % vi[i] for i in (1, 2, 3)], giai,
                                 _c4_luoi(ds, ten, la_ban=True), 0, dang)
    return cau


def _c4_kho_song():
    """Khẳng định về vận tốc trên dòng sông / đường thẳng: [(phát biểu, đúng?, lí do)]."""
    vn = random.randint(3, 6)
    a = random.choice([12, 15, 18, 20])
    b = random.choice([v for v in (12, 15, 18, 20) if v != a])
    if random.random() < 0.5:
        mo = (r"A river flows in a straight line with current velocity $\overrightarrow{v_n}$ ($%d$ km/h). Boat $A$ travels downstream, boat $B$ "
              r"travels upstream, boat $C$ travels downstream; the velocities of the boats are $\overrightarrow{v_A}$, $\overrightarrow{v_B}$, "
              r"$\overrightarrow{v_C}$ with magnitudes $%d$ km/h, $%d$ km/h, $%d$ km/h, respectively." % (vn, a, a, b))
        X = [(r"$\overrightarrow{v_A}$ has the same direction as $\overrightarrow{v_n}$", True, "boat $A$ travels downstream"),
             (r"$\overrightarrow{v_B}$ has the opposite direction to $\overrightarrow{v_n}$", True, "boat $B$ is going upstream"),
             (r"$\overrightarrow{v_A}$ and $\overrightarrow{v_B}$ are collinear", True, "both move along the river"),
             (r"$\overrightarrow{v_A}$ and $\overrightarrow{v_C}$ have the same direction", True, "both boats are going downstream"),
             (r"$\overrightarrow{v_A} = \overrightarrow{v_B}$", False, "the two vectors have the same magnitude but opposite directions"),
             (r"$\overrightarrow{v_A} = \overrightarrow{v_C}$", False, "the two vectors have the same direction but different magnitudes " "($%d \\ne %d$)" % (a, b)),
             (r"$\overrightarrow{v_B}$ has the same direction as $\overrightarrow{v_n}$", False, "boat $B$ is going upstream"),
             (r"$\overrightarrow{v_A}$ and $\overrightarrow{v_B}$ have the same direction", False, "one boat goes downstream and the other goes upstream")]
        return mo, X
    mo = (r"On a straight stretch of road running in the north-south direction, car $A$ travels north at a speed of $%d$ km/h, car $B$ travels south "
          r"at a speed of $%d$ km/h, and car $C$ travels north at a speed of $%d$ km/h. Let $\overrightarrow{v_A}$, $\overrightarrow{v_B}$, "
          r"$\overrightarrow{v_C}$ be the velocity vectors of the three cars." % (a * 3, a * 3, b * 3))
    X = [(r"$\overrightarrow{v_A}$ and $\overrightarrow{v_B}$ have opposite directions", True, "the two cars travel in opposite directions on the same road"),
         (r"$\overrightarrow{v_A}$ and $\overrightarrow{v_C}$ have the same direction", True, "two cars both traveling north"),
         (r"$\overrightarrow{v_B}$ and $\overrightarrow{v_C}$ are collinear", True, "the vehicles move along the same straight line"),
         (r"$\left|\overrightarrow{v_A}\right| = \left|\overrightarrow{v_B}\right|$", True, "the two cars have the same speed of $%d$ km/h" % (a * 3)),
         (r"$\overrightarrow{v_A} = \overrightarrow{v_B}$", False, "the two vectors have the same magnitude but opposite directions"),
         (r"$\overrightarrow{v_A} = \overrightarrow{v_C}$", False, "the two vectors have the same direction but different magnitudes"),
         (r"$\overrightarrow{v_B}$ and $\overrightarrow{v_C}$ have the same direction", False, "car $B$ heads south, car $C$ heads north"),
         (r"$\overrightarrow{v_A}$ and $\overrightarrow{v_B}$ are not " r"collinear", False, "the two cars travel on the same straight line")]
    return mo, X


def L10_C4_B7_TH039_MC_D_01(socau, dang=1):
    r"""Biểu diễn vận tốc bằng vectơ trong bối cảnh dòng sông (thuyền xuôi, ngược dòng) hoặc ba xe trên đường thẳng: chọn
    khẳng định đúng (sai) về cùng hướng, ngược hướng, bằng nhau, độ lớn.

    CLAUDE THEM 01/10/2026 - theo TL 1 (hai thuyen nguoc dong) tai lieu CĐ day them "Khai niem vecto". Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        mo, X = _c4_kho_song()
        hoi = random.random() < 0.55
        d = random.choice([x for x in X if x[1] == hoi])
        s = random.sample([x for x in X if x[1] != hoi], 3)
        debai = mo + r" Which of the following statements is %s?" % (r"\textbf{true}" if hoi else r"\textbf{false}")
        giai = r"\\ ".join(r"%s is a %s statement because %s." % (x[0], "true" if x[1] else "false", x[2]) for x in [d] + s)
        cau += _MC_khong_cham(debai, d[0], [x[0] for x in s], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TỰ LUẬN HAI ĐƠN VỊ
# ---------------------------------------------------------------------
def _c4_tl_ds(ds):
    return r",\ ".join(_vt(*w) for w in ds) if ds else r"\text{none}"


def L10_C4_NB037_NB038_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý trong một hình (kho hình xoay vòng):
    a) (NB037) Tìm các vectơ cùng hướng với $\overrightarrow{v}$ (khác $\overrightarrow{v}$, điểm mút thuộc hình);
    b) (NB038) Tìm các vectơ bằng $\overrightarrow{v}$.

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi theo co Lan; theo TL 7, 10, 11, 18 tai lieu CĐ day them "Khai niem
    vecto". Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        H = _c4_chon_hinh("tl_b7")
        v = _c4_chon_vt(H, "bang", 1, 4)
        if not v:
            continue
        ch = _c4_loc(H, v, "cung_huong")
        bg = _c4_loc(H, v, "bang")
        if len(ch) > 8 or len(ch) == len(bg):
            continue
        so += 1
        de = H["mo"] + r" Consider the vectors other than vector $%s$ whose initial and " r"terminal points are two of the points %s." % (
            _vt(*v), ", ".join("$%s$" % t for t in H["P"]))
        ds = [(r"Find the vectors with the same direction as the vector $%s$." % _vt(*v), _c4_tl_ds(ch), _c4_ly_qh(H, v, "cung_huong", ch)),
              (r"Find the vectors equal to vector $%s$." % _vt(*v), _c4_tl_ds(bg),
               _c4_ly_qh(H, v, "bang", bg) + r" (Among the vectors with the same direction in part a), keep only those with magnitude $%s$.)" % (v[0] + v[1]))]
        cau += TL_answer_text(de, ds, _c4_tikz(H), 0, dong)
    return cau


def L10_C4_NB037_TH039_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý - các lực biểu diễn trên lưới ô vuông (mỗi cạnh ô ứng với $10$ N, các lực theo phương ngang hoặc dọc):
    a) (NB037) Tìm các lực cùng hướng, ngược hướng với $\overrightarrow{F_1}$;
    b) (TH039) Tính độ lớn và nêu hướng (đông, tây, nam, bắc) của từng lực.

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi theo co Lan; theo TL 9, 19 tai lieu CĐ day them "Khai niem vecto".
    Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        H4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        h1 = random.choice(H4)
        dirs = [h1, h1, (-h1[0], -h1[1]), random.choice([d for d in H4 if d not in (h1, (-h1[0], -h1[1]))])]
        V = [(d[0] * random.randint(1, 4), d[1] * random.randint(1, 4)) for d in dirs]
        thu = [0] + random.sample([1, 2, 3], 3)
        V = [V[i] for i in thu]
        try:
            ds = _c4_dat_mui_ten(V)
        except ValueError:
            continue
        so += 1
        ten = [r"\overrightarrow{F_{%d}}" % (i + 1) for i in range(4)]
        ch = [ten[i] for i in range(1, 4) if _c4_ch(V[i], V[0])]
        ng = [ten[i] for i in range(1, 4) if _c4_cp(V[i], V[0]) and not _c4_ch(V[i], V[0])]
        do = [abs(v[0]) + abs(v[1]) for v in V]
        hg = [_C4_HUONG[(int(math.copysign(1, v[0])) if v[0] else 0, int(math.copysign(1, v[1])) if v[1] else 0)] for v in V]
        de = (r"The four forces $%s$ are represented by vectors on a square grid as shown (up is north, right is "
              r"east); each grid square side corresponds to $10$ N." % "$, $".join(ten))
        ys = [(r"Find the forces with the same direction as $%s$ and the forces " r"with the opposite direction." % ten[0],
               _c4_tl_dap4(r"same direction: $%s$; opposite direction: $%s$" % (r",\ ".join(ch) or r"\text{none}", r",\ ".join(ng) or r"\text{none}")),
               r"The forces collinear with $%s$ are those whose lines of action are horizontal%s. Among them, same direction: $%s$; opposite direction: $%s$."
               % (ten[0], "" if V[0][1] == 0 else "" , r",\ ".join(ch) or r"\text{none}", r",\ ".join(ng) or r"\text{none}")
               if V[0][1] == 0 else
               r"The forces collinear with $%s$ are the forces whose lines of support are vertical. Among them, same direction: $%s$; opposite direction: $%s$."
               % (ten[0], r",\ ".join(ch) or r"\text{none}", r",\ ".join(ng) or r"\text{none}")),
              (r"Find the magnitude and state the direction of each force.",
               _c4_tl_dap4("; ".join(r"$\left|%s\right| = %d$ N (%s)" % (ten[i], 10 * do[i], hg[i]) for i in range(4))),
               r"Count the grid-square sides of each vector, then multiply by $10$ " r"N: " +
               "; ".join(r"$%s$ has length $%d$ (grid squares) and points %s, so $\left|%s\right| = %d$ N" % (ten[i], do[i], hg[i], ten[i], 10 * do[i]) for i in range(4))
               + ".")]
        cau += TL_answer_text(de, ys, _c4_luoi(ds, ten, la_ban=True), 0, dong)
    return cau


def _c4_tl_dap4(s):
    """Đáp án tự luận đặt trong $...$: phần chữ bọc \\text{}."""
    ra = []
    for i, phan in enumerate(s.split("$")):
        if i % 2 == 0:
            if phan:
                ra.append(r"\text{%s}" % phan)
        else:
            ra.append(phan)
    return "".join(ra)


# =====================================================================
# BỔ SUNG 15/10/2026 (cô Lan: "ghép các dạng đã thấy giống, cùng dạng; các dạng thiếu làm bổ sung luôn")
# Bản TRẢ LỜI NGẮN (SA) / TRẮC NGHIỆM (MC) cùng chữ, cùng "Dang" với câu đã có.
# MC "chọn khẳng định đúng" -> SA "có bao nhiêu khẳng định đúng (sai)". Chân trị của MỌI khẳng định do Python
# TÍNH bằng toạ độ (điểm bất kì: thử ba bộ toạ độ ngẫu nhiên; có hình: toạ độ của hình), không gõ tay.
# CLAUDE THEM 15/10/2026 - co Lan duyet lai.
# =====================================================================
import re as _re5
from fractions import Fraction as _Fr5


class _Bt5:
    # Biểu thức vectơ: tex (LaTeX), f (môi trường -> số phức: vectơ (x; y) viết thành x + yi), loai: 'don' (một
    # vectơ), 'tich' (số nhân vectơ), 'tong' (tổng, hiệu).

    def __init__(self, tex, f, loai="don"):
        self.tex, self.f, self.loai = tex, f, loai


def _b5_vt(X, Y):
    return _Bt5(_vt(X, Y), lambda E: E[Y] - E[X])


def _b5_tu(t):
    return _Bt5(r"\overrightarrow{%s}" % t, lambda E: E[t])


_B5_0 = _Bt5(r"\overrightarrow{0}", lambda E: 0)


def _he5(k):
    k = _Fr5(k)
    if k == 1:
        return ""
    if k == -1:
        return "-"
    if k.denominator == 1:
        return str(k.numerator)
    return ("-" if k < 0 else "") + r"\dfrac{%d}{%d}" % (abs(k.numerator), k.denominator)


def _b5_nhan(k, x, ktex=None):
    """k.x; ktex: cách viết riêng của hệ số (vd \\left(2 + 3\\right))."""
    gt = float(_Fr5(k))
    vt = x.tex if x.loai == "don" else r"\left(%s\right)" % x.tex
    return _Bt5((_he5(k) if ktex is None else ktex) + vt, lambda E: gt * x.f(E), "tich")


def _b5_cong(*ds):
    """Tổng; số hạng là tổng (hiệu) thì đặt trong ngoặc để giữ đúng cách nhóm (tính kết hợp)."""
    def boc(d):
        return r"\left(%s\right)" % d.tex if d.loai == "tong" else d.tex
    tex = boc(ds[0])
    for d in ds[1:]:
        tex += (" - " + d.tex[1:]) if (d.loai != "tong" and d.tex.startswith("-")) else (" + " + boc(d))
    return _Bt5(tex, lambda E: sum(d.f(E) for d in ds), "tong")


def _b5_tru(x, y):
    vt = r"\left(%s\right)" % y.tex if (y.loai == "tong" or y.tex.startswith("-")) else y.tex
    return _Bt5(x.tex + " - " + vt, lambda E: x.f(E) - y.f(E), "tong")


def _b5_bang(l, r, envs):
    return all(abs(l.f(E) - r.f(E)) < 1e-9 for E in envs)


def _b5_env_diem(ten, rang_buoc=None, so=3):
    """Ba bộ toạ độ ngẫu nhiên cho các điểm 'bất kì'; rang_buoc(E) bổ sung điểm phụ thuộc (vd trung điểm)."""
    ra = []
    for _ in range(so):
        E = {t: complex(random.uniform(-9, 9), random.uniform(-9, 9)) for t in ten}
        if rang_buoc:
            rang_buoc(E)
        ra.append(E)
    return ra


def _b5_rut_diem(x, envs, uu_tien, ten_diem):
    """Viết gọn một biểu thức vectơ (điểm): vectơ-không, một vectơ, hai lần hoặc nửa một vectơ có tên trong hình.
    uu_tien: các cặp điểm ưu tiên (đã có trong khẳng định). Không gọn được thì giữ nguyên."""
    if x.loai == "don":
        return x.tex
    if _b5_bang(x, _B5_0, envs):
        return _B5_0.tex
    cap = list(uu_tien) + [(U, V) for U in ten_diem for V in ten_diem if U != V and (U, V) not in uu_tien]
    for k in ((1,) if x.loai == "tich" else (1, 2, _Fr5(1, 2))):
        for U, V in cap:
            w = _b5_nhan(k, _b5_vt(U, V)) if k != 1 else _b5_vt(U, V)
            if _b5_bang(x, w, envs):
                return w.tex
    return x.tex


def _b5_cap_trong(*ds):
    """Các cặp điểm (điểm đầu, điểm cuối) xuất hiện trong các biểu thức (đọc từ LaTeX)."""
    ra = []
    for d in ds:
        for m in _re5.finditer(r"\\overrightarrow\{([A-Z])([A-Z])\}", d.tex):
            if (m.group(1), m.group(2)) not in ra:
                ra.append((m.group(1), m.group(2)))
    return ra


def _b5_ly_so_sanh(l, r, gl, gr, bang):
    """Lí do đúng / sai sau khi đã viết gọn hai vế (gl, gr là LaTeX dạng gọn; trùng tex gốc nghĩa là không gọn hơn)."""
    if bang:
        if gl != l.tex and gr != r.tex:
            return r"both sides equal $%s$" % gl
        if gl != l.tex:
            return r"the left-hand side equals $%s$, which is exactly the right-hand side" % gl
        if gr != r.tex:
            return r"the right-hand side equals $%s$, which is exactly the left-hand side" % gr
        return r"$%s$ and $%s$ have the same direction and the same length" % (l.tex, r.tex)
    trai = (r"the left-hand side equals $%s$" % gl) if gl != l.tex else (r"the left-hand side is $%s$" % gl)
    phai = (r"the right-hand side equals $%s$" % gr) if gr != r.tex else (r"the right-hand side is $%s$" % gr)
    return trai + ", while " + phai + "; these two vectors are different"


def _b5_ly_diem(l, r, envs, ten_diem):
    """Lí do đúng / sai của khẳng định l = r (vectơ theo điểm): rút gọn hai vế rồi so sánh."""
    uu = _b5_cap_trong(l, r)
    gl, gr = _b5_rut_diem(l, envs, uu, ten_diem), _b5_rut_diem(r, envs, uu, ten_diem)
    return _b5_ly_so_sanh(l, r, gl, gr, _b5_bang(l, r, envs))


def _b5_to_hop(x, tu):
    """Viết x thành tổ hợp a.u + b.v + ... của các vectơ tự do (x tuyến tính)."""
    he = []
    for t in tu:
        E = {s: (1 if s == t else 0) for s in tu}
        he.append(_Fr5(x.f(E).real).limit_denominator(100))
    hang = [_b5_nhan(k, _b5_tu(t)) if k != 1 else _b5_tu(t) for k, t in zip(he, tu) if k != 0]
    if not hang:
        return _B5_0.tex
    return _b5_cong(*hang).tex if len(hang) > 1 else hang[0].tex


def _b5_ly_tu(l, r, envs, tu):
    gl, gr = _b5_to_hop(l, tu), _b5_to_hop(r, tu)
    return _b5_ly_so_sanh(l, r, gl, gr, _b5_bang(l, r, envs))


def _c4s_chon_bon(dung_ds, sai_ds):
    """Chọn bốn mục (số mục đúng t trong {1; 2; 3}); mục (tex, lí do) hoặc (tex, lí do, khoá): hai mục cùng khoá (vd
    cùng vế trái) không cùng xuất hiện, để khẳng định này không làm lộ khẳng định kia."""
    chuan = lambda ds: list({x[0]: (x[0], x[1], x[2] if len(x) > 2 else x[0]) for x in ds}.values())
    dung_ds, sai_ds = chuan(dung_ds), chuan(sai_ds)
    for _ in range(200):
        t = random.choice([x for x in (1, 2, 3) if x <= len(dung_ds) and 4 - x <= len(sai_ds)])
        random.shuffle(dung_ds)
        random.shuffle(sai_ds)
        khoa, ds = set(), []
        for nguon, can, la_dung in ((dung_ds, t, True), (sai_ds, 4 - t, False)):
            lay = 0
            for x in nguon:
                if lay < can and x[2] not in khoa:
                    ds.append(((x[0], x[1]), la_dung))
                    khoa.add(x[2])
                    lay += 1
        if len(ds) == 4:
            random.shuffle(ds)
            return ds
    raise ValueError("khong du khang dinh khac khoa")


def _c4s_dem(mo, dung_ds, sai_ds, dang, hinh=0, giai_mo=""):
    r"""Câu ĐẾM: bốn khẳng định (đúng có lí do, sai có lí do) lấy từ dung_ds / sai_ds: [(tex có $...$, lí do)].
    Số khẳng định đúng chọn trong {1; 2; 3}; hỏi số khẳng định đúng hoặc số khẳng định sai."""
    ds = _c4s_chon_bon(dung_ds, sai_ds)
    t = sum(1 for _, d in ds if d)
    hoi_dung = random.random() < 0.6
    dap = t if hoi_dung else 4 - t
    tu = r"\textbf{true}" if hoi_dung else r"\textbf{false}"
    debai = (mo + r" How many of the following statements are %s?\\ " % tu
             + r"\\ ".join("%d. %s" % (i + 1, x[0]) for i, (x, _) in enumerate(ds)))
    giai = giai_mo + r"\\ ".join(r"%d. %s is %s because %s." % (i + 1, x[0], "true" if d else "false", x[1])
                                for i, (x, d) in enumerate(ds))
    giai += r"\\ So $%d$ statements are %s." % (dap, tu)
    nhieu = [str(x) for x in (4 - dap, dap + 1, dap - 1, 0, 4, 1, 2, 3) if x != dap and 0 <= x <= 4]
    return MC_SA_answer_const(debai, str(dap), nhieu, giai, hinh, 0, dang)


def _c4s_phan_loai(cap, envs, ten_diem):
    """[(l, r)] -> (đúng, sai) dạng [(tex $l = r$, lí do)]."""
    dung, sai = [], []
    for l, r in cap:
        tex = r"$%s = %s$" % (l.tex, r.tex)
        (dung if _b5_bang(l, r, envs) else sai).append((tex, _b5_ly_diem(l, r, envs, ten_diem), l.tex))
    return dung, sai


_C4S_BO_DIEM = [("A", "B", "C", "D"), ("M", "N", "P", "Q"), ("D", "E", "F", "G"), ("I", "J", "K", "L"), ("X", "Y", "Z", "T")]


# ---------------------------------------------------------------------
# TH040_SA_A: quy tắc ba điểm (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def L10_C4_B8_TH040_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH040_MC_A (cùng Dang): với bốn điểm bất kì, cho bốn đẳng thức về tổng
    các vectơ (quy tắc ba điểm), hỏi có bao nhiêu đẳng thức đúng (sai). Chân trị tính bằng toạ độ ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, Z, T = random.sample(random.choice(_C4S_BO_DIEM), 4)
        v = _b5_vt
        cap = [(_b5_cong(v(X, Y), v(Y, Z)), v(X, Z)), (_b5_cong(v(Y, X), v(X, Z)), v(Y, Z)),
               (_b5_cong(v(X, Y), v(Y, Z), v(Z, X)), _B5_0), (_b5_cong(v(X, Y), v(Y, Z), v(Z, T)), v(X, T)),
               (_b5_cong(v(Z, X), v(X, Y)), v(Z, Y)), (_b5_cong(v(X, Y), v(Y, T), v(T, Z)), v(X, Z)),
               (_b5_cong(v(X, Y), v(Y, Z)), v(Z, X)), (_b5_cong(v(Y, X), v(X, Z)), v(Z, Y)),
               (_b5_cong(v(X, Y), v(Y, Z), v(Z, T)), v(T, X)), (_b5_cong(v(X, Y), v(Y, Z), v(Z, X)), v(X, Z)),
               (_b5_cong(v(Z, X), v(X, Y)), v(Y, Z)), (_b5_cong(v(T, X), v(X, Y)), v(Y, T))]
        envs = _b5_env_diem([X, Y, Z, T])
        dung, sai = _c4s_phan_loai(cap, envs, [X, Y, Z, T])
        mo = r"Given four arbitrary points $%s$, $%s$, $%s$, $%s$." % tuple(sorted([X, Y, Z, T]))
        giai_mo = (r"Triangle rule: for any three points $%s$, $%s$, $%s$, $%s + %s = %s$.\\ "
                   % (X, Y, Z, _vt(X, Y), _vt(Y, Z), _vt(X, Z)))
        cau += _c4s_dem(mo, dung, sai, dang, 0, giai_mo)
    return cau


# ---------------------------------------------------------------------
# TH040_SA_B: quy tắc hình bình hành, có hình (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def L10_C4_B8_TH040_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH040_MC_B (cùng Dang): cho hình bình hành (hình chữ nhật, hình thoi, hình
    vuông) có hình vẽ; bốn đẳng thức dạng $\overrightarrow{XY} + \overrightarrow{XZ} = \ldots$; hỏi có bao nhiêu đẳng
    thức đúng (sai). Chân trị tính bằng toạ độ của hình.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        H = _c4_chon_hinh("th040_sa_b", ["hbh", "hcn", "thoi", "vuong"])
        A, B, C, D = H["da_giac"]
        O = H["tam"]
        v = _b5_vt
        cap = []
        for X, U, W, T in ((A, B, D, C), (B, C, A, D), (C, D, B, A), (D, A, C, B)):
            l = _b5_cong(v(X, U), v(X, W))
            cap += [(l, v(X, T)), (l, v(U, W)), (l, v(W, U)), (l, v(T, X)), (l, _b5_nhan(2, v(X, O))),
                    (l, v(X, O)), (_b5_cong(v(X, U), v(X, T)), v(X, W))]
        envs = [{k: complex(*p) for k, p in H["P"].items()}]
        dung, sai = _c4s_phan_loai(cap, envs, list(H["P"]))
        giai_mo = (r"Parallelogram rule: if $%s$ is a parallelogram then $%s + %s = %s$.\\ "
                   % (A + B + C + D, _vt(A, B), _vt(A, D), _vt(A, C)))
        cau += _c4s_dem(H["mo"], dung, sai, dang, _c4_tikz(H), giai_mo)
    return cau


# ---------------------------------------------------------------------
# TH041_SA_A: hiệu hai vectơ, quy tắc trừ (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def L10_C4_B8_TH041_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH041_MC_A (cùng Dang): với ba điểm bất kì, bốn đẳng thức về hiệu hai
    vectơ (quy tắc trừ); hỏi có bao nhiêu đẳng thức đúng (sai). Chân trị tính bằng toạ độ ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, Z = random.sample(random.choice(_C4S_BO_DIEM), 3)
        v = _b5_vt
        cap = [(_b5_tru(v(X, Y), v(X, Z)), v(Z, Y)), (_b5_tru(v(X, Y), v(X, Z)), v(Y, Z)),
               (_b5_tru(v(X, Y), v(Z, Y)), v(X, Z)), (_b5_tru(v(X, Y), v(Z, Y)), v(Z, X)),
               (_b5_tru(v(X, Z), v(Y, Z)), v(X, Y)), (_b5_tru(v(X, Z), v(Y, Z)), v(Y, X)),
               (_b5_tru(v(Y, X), v(Z, X)), v(Y, Z)), (_b5_tru(v(Y, X), v(Z, X)), v(Z, Y)),
               (_b5_tru(v(X, Y), v(X, Z)), _b5_cong(v(Z, X), v(X, Y))),
               (_b5_tru(v(X, Y), v(X, Z)), _b5_cong(v(X, Z), v(Y, X))),
               (_b5_tru(v(Z, X), v(Z, Y)), v(Y, X)), (_b5_tru(v(Z, X), v(Z, Y)), v(X, Y))]
        envs = _b5_env_diem([X, Y, Z])
        dung, sai = _c4s_phan_loai(cap, envs, [X, Y, Z])
        mo = r"Given three arbitrary points $%s$, $%s$, $%s$." % tuple(sorted([X, Y, Z]))
        giai_mo = (r"Subtraction rule: for any three points $%s$, $%s$, $%s$, $%s - %s = %s$.\\ "
                   % (X, Y, Z, _vt(X, Y), _vt(X, Z), _vt(Z, Y)))
        cau += _c4s_dem(mo, dung, sai, dang, 0, giai_mo)
    return cau


# ---------------------------------------------------------------------
# TH041_SA_B: vectơ đối trong hình bình hành / hình chữ nhật / hình thoi / hình vuông (có hình)
# ---------------------------------------------------------------------
def L10_C4_B8_TH041_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH041_MC_B (cùng Dang): hình có tâm $O$ (hai đường chéo cắt nhau tại $O$),
    bốn khẳng định ``$\vec u + \vec w = \vec 0$'' hoặc ``$\vec u = -\vec w$''; hỏi có bao nhiêu khẳng định đúng (sai).
    Các cặp đưa ra đều có cùng độ dài (dễ nhầm); chân trị tính bằng toạ độ của hình.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        H = _c4_chon_hinh("th041_sa_b", ["hbh", "hcn", "thoi", "vuong"])
        A, B, C, D = H["da_giac"]
        O = H["tam"]
        E = {k: complex(*p) for k, p in H["P"].items()}
        vts = [(A, B), (B, C), (C, D), (D, A), (B, A), (C, B), (D, C), (A, D)] + [(O, X) for X in (A, B, C, D)] + \
              [(X, O) for X in (A, B, C, D)]
        dung, sai = [], []
        for i, u in enumerate(vts):
            for w in vts[i + 1:]:
                a, b = E[u[1]] - E[u[0]], E[w[1]] - E[w[0]]
                if set(u) == set(w) or abs(abs(a) - abs(b)) > 1e-9:
                    continue
                if abs(a + b) < 1e-9:
                    ly = r"$%s$ and $%s$ are opposite vectors (same length, opposite directions)" % (_vt(*u), _vt(*w))
                elif abs(a - b) < 1e-9:
                    ly = r"$%s$ and $%s$ have the same direction, so they are not opposite vectors" % (_vt(*u), _vt(*w))
                else:
                    ly = r"$%s$ and $%s$ are not parallel, so they are not opposite vectors" % (_vt(*u), _vt(*w))
                tex = random.choice([r"$%s + %s = \overrightarrow{0}$" % (_vt(*u), _vt(*w)),
                                     r"$%s = -%s$" % (_vt(*u), _vt(*w))])
                (dung if abs(a + b) < 1e-9 else sai).append((tex, ly))
        dung.append((r"$%s + %s + %s + %s = \overrightarrow{0}$" % tuple(_vt(O, X) for X in (A, B, C, D)),
                     r"$%s + %s = \overrightarrow{0}$ and $%s + %s = \overrightarrow{0}$ ($%s$ is the midpoint of each diagonal)" % (_vt(O, A), _vt(O, C), _vt(O, B), _vt(O, D), O)))
        giai_mo = (r"Two opposite vectors have the same length and opposite directions; $\vec u + \vec w = \overrightarrow{0}$ if and only if $\vec u = -\vec w$.\\ ")
        cau += _c4s_dem(H["mo"], dung, sai, dang, _c4_tikz(H), giai_mo)
    return cau


# ---------------------------------------------------------------------
# TH042_SA_A: tính chất của phép cộng vectơ (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def L10_C4_B8_TH042_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH042_MC_A (cùng Dang): ba vectơ tuỳ ý, bốn đẳng thức (giao hoán, kết
    hợp, cộng với vectơ-không, cộng với vectơ đối; các đẳng thức sai là lỗi dấu, nhầm vectơ-không); hỏi có bao nhiêu
    đẳng thức đúng (sai). Chân trị tính bằng ba bộ vectơ ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        tu = random.choice([("a", "b", "c"), ("u", "v", "w"), ("x", "y", "z")])
        a, b, c = (_b5_tu(t) for t in tu)
        cap = [(_b5_cong(a, b), _b5_cong(b, a)), (_b5_cong(_b5_cong(a, b), c), _b5_cong(a, _b5_cong(b, c))),
               (_b5_cong(a, _B5_0), a), (_b5_cong(_b5_cong(a, b), c), _b5_cong(_b5_cong(a, c), b)),
               (_b5_tru(a, b), _b5_nhan(-1, _b5_tru(b, a))), (_b5_cong(a, _b5_tru(b, a)), b),
               (_b5_cong(a, _b5_nhan(-1, a)), _B5_0),
               (_b5_cong(a, b), _b5_tru(b, a)), (_b5_tru(a, b), _b5_tru(b, a)), (_b5_cong(a, _B5_0), _B5_0),
               (_b5_cong(_b5_cong(a, b), c), _b5_cong(a, _b5_tru(b, c))), (_b5_tru(a, _b5_cong(b, c)), _b5_cong(_b5_tru(a, b), c)),
               (_b5_cong(a, _b5_tru(b, a)), a), (_b5_tru(a, b), _b5_tru(a, _b5_nhan(-1, b)))]
        envs = [{t: complex(random.uniform(-9, 9), random.uniform(-9, 9)) for t in tu} for _ in range(3)]
        dung, sai = [], []
        for l, r in cap:
            (dung if _b5_bang(l, r, envs) else sai).append((r"$%s = %s$" % (l.tex, r.tex), _b5_ly_tu(l, r, envs, tu), l.tex))
        mo = r"Given three arbitrary vectors $%s$, $%s$, $%s$." % tuple(r"\overrightarrow{%s}" % t for t in tu)
        giai_mo = (r"Vector addition is commutative and associative; $\vec a + \overrightarrow{0} = \vec a$, $\vec a + \left(-\vec a\right) = \overrightarrow{0}$; group like vectors to simplify each side.\\ ")
        cau += _c4s_dem(mo, dung, sai, dang, 0, giai_mo)
    return cau


# ---------------------------------------------------------------------
# TH043_SA_A: độ dài của vectơ k.a
# ---------------------------------------------------------------------
def L10_C4_B9_TH043_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH043_MC_A (cùng Dang: tích của một số với một vectơ, độ dài
    $\left|k\vec a\right| = \left|k\right|\cdot\left|\vec a\right|$): biết $\left|\vec a\right|$ tính độ dài $k\vec a$,
    hoặc biết $\vec b = k\vec a$ và $\left|\vec b\right|$ tính $\left|\vec a\right|$.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    a, b = r"\overrightarrow{a}", r"\overrightarrow{b}"
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        k = random.choice([-5, -4, -3, -2, 2, 3, 4, 5, _Fr5(1, 2), _Fr5(-1, 2), _Fr5(3, 2), _Fr5(-3, 2)])
        m = random.randint(2, 12)
        kieu = random.choice(["xuoi", "nguoc"])
        if kieu == "nguoc" and (abs(k) * m).denominator != 1:
            continue
        if (k, m, kieu) not in gt:
            gt.append((k, m, kieu))
    cau = ""
    for k, m, kieu in gt:
        n = abs(k) * m
        kt = _he5(k)
        if kieu == "xuoi":
            dap = n
            debai = (r"Given a vector $%s$ with $\left|%s\right| = %d$. What is the length of the vector $%s%s$?"
                     % (a, a, m, kt, a))
            giai = (r"$\left|%s%s\right| = \left|%s\right|\cdot\left|%s\right| = %s\cdot %d = %s$."
                    % (kt, a, kt, a, _xx4(float(abs(k)), 2), m, _xx4(float(n), 2)))
            ung = [m, float(k) * m, n + m, abs(n - m), 2 * n]
        else:
            dap = _Fr5(m)
            debai = (r"Given two vectors $%s$, $%s$ such that $%s = %s%s$ and $\left|%s\right| = %s$. Find $\left|%s\right|$."
                     % (a, b, b, kt, a, b, _xx4(float(n), 2), a))
            giai = (r"$\left|%s\right| = \left|%s\right|\cdot\left|%s\right| = %s\left|%s\right|$, so $\left|%s\right| = %s : %s = %d$."
                    % (b, kt, a, _xx4(float(abs(k)), 2), a, a, _xx4(float(n), 2), _xx4(float(abs(k)), 2), m))
            ung = [n, float(n) * float(abs(k)), m + 1, m - 1, 2 * m]
        ds = _xx4(float(dap), 2)
        nhieu = [_xx4(float(x), 2) for x in ung if _xx4(float(x), 2) != ds and float(x) > 0]
        cau += MC_SA_answer_const(debai, ds, nhieu + ["%d" % (int(float(dap)) + j) for j in (1, 2, 3)], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH044_SA_A: tính chất phép nhân số với vectơ (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def L10_C4_B9_TH044_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH044_MC_A (cùng Dang): với hai số cụ thể $k$, $l$ và hai vectơ tuỳ ý,
    bốn đẳng thức (phân phối với cộng vectơ, với cộng số, kết hợp; các đẳng thức sai bỏ sót hệ số, sai dấu, nhầm
    cộng số thành nhân số); hỏi có bao nhiêu đẳng thức đúng (sai). Chân trị tính bằng ba bộ vectơ ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        k, l = random.sample([2, 3, 4, 5, -2, -3], 2)
        while k + l == 0:
            k, l = random.sample([2, 3, 4, 5, -2, -3], 2)
        a, b = _b5_tu("a"), _b5_tu("b")
        n = _b5_nhan
        kl_tex = r"\left(%d %s %d\right)" % (k, "+" if l > 0 else "-", abs(l))
        cap = [(n(k, _b5_cong(a, b)), _b5_cong(n(k, a), n(k, b))), (n(k, _b5_tru(a, b)), _b5_cong(n(k, a), n(-k, b))),
               (n(k + l, a, kl_tex), _b5_cong(n(k, a), n(l, a))), (n(k, n(l, a)), n(k * l, a)),
               (n(-k, _b5_tru(a, b)), _b5_cong(n(-k, a), n(k, b))),
               (n(k, _b5_cong(a, b)), _b5_cong(n(k, a), b)), (n(k, _b5_tru(a, b)), _b5_cong(n(k, a), n(k, b))),
               (n(k, _b5_tru(a, b)), _b5_tru(n(k, a), b)), (n(k, n(l, a)), n(k + l, a)),
               (n(k + l, a, kl_tex), n(k * l, a)), (n(-k, _b5_tru(a, b)), _b5_tru(n(-k, a), n(k, b)))]
        envs = [{t: complex(random.uniform(-9, 9), random.uniform(-9, 9)) for t in "ab"} for _ in range(3)]
        dung, sai = [], []
        for x, y in cap:
            (dung if _b5_bang(x, y, envs) else sai).append((r"$%s = %s$" % (x.tex, y.tex), _b5_ly_tu(x, y, envs, "ab"), x.tex))
        mo = r"Given two arbitrary vectors $\overrightarrow{a}$, $\overrightarrow{b}$."
        giai_mo = (r"For two numbers $k$, $l$ and two vectors $\vec a$, $\vec b$: $k\left(\vec a + \vec b\right) = k\vec a + k\vec b$; $\left(k + l\right)\vec a = k\vec a + l\vec a$; $k\left(l\vec a\right) = \left(kl\right)\vec a$.\\ ")
        cau += _c4s_dem(mo, dung, sai, dang, 0, giai_mo)
    return cau


# ---------------------------------------------------------------------
# TH046_SA_A: ba điểm thẳng hàng - tìm k để AB = k.AC (toạ độ)
# ---------------------------------------------------------------------
def L10_C4_B9_TH046_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH046_MC_A (cùng Dang): cho toạ độ ba điểm thẳng hàng, tìm số $k$ sao
    cho $\overrightarrow{AB} = k\overrightarrow{AC}$ (từ đó suy ra ba điểm thẳng hàng). $k$ nguyên hoặc nửa nguyên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 2000:
        lan += 1
        k = random.choice([2, 3, -2, -3, 4, -1, _Fr5(1, 2), _Fr5(-1, 2), _Fr5(3, 2), _Fr5(-3, 2)])
        xa, ya = random.randint(-5, 5), random.randint(-5, 5)
        q = _Fr5(k).denominator
        ux, uy = q * random.randint(-3, 3), q * random.randint(-3, 3)
        if (ux, uy) == (0, 0):
            continue
        xc, yc = xa + ux, ya + uy
        xb, yb = xa + int(k * ux), ya + int(k * uy)
        if max(abs(xb), abs(yb), abs(xc), abs(yc)) > 12:
            continue
        w = (xa, ya, xb, yb, xc, yc)
        if w not in gt:
            gt.append(w)
    cau = ""
    for xa, ya, xb, yb, xc, yc in gt:
        ab, ac = (xb - xa, yb - ya), (xc - xa, yc - ya)
        k = _Fr5(ab[0], ac[0]) if ac[0] else _Fr5(ab[1], ac[1])
        debai = (r"In the coordinate plane $Oxy$, given three points $A%s$, $B%s$, $C%s$. Find the real number $k$ such that $\overrightarrow{AB} = k\overrightarrow{AC}$." % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$\overrightarrow{AB} = %s$, $\overrightarrow{AC} = %s$. Since $%s = %s\cdot\left(%d\right)$ and $%s = %s\cdot\left(%d\right)$, $\overrightarrow{AB} = %s\overrightarrow{AC}$, i.e. $k = %s$ (the points $A$, $B$, $C$ are collinear)."
                % (_toado(*ab), _toado(*ac), ab[0], _xx4(float(k), 2), ac[0], ab[1], _xx4(float(k), 2), ac[1],
                   _he5(k) if k not in (1, -1) else str(k), _xx4(float(k), 2)))
        dap = _xx4(float(k), 2)
        ung = [_xx4(float(1 / k), 2), _xx4(-float(k), 2), _xx4(float(k) + 1, 2), _xx4(float(k) - 1, 2)]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH047_SA_A: đẳng thức vectơ về trung điểm (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def L10_C4_B9_TH047_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH047_MC_A (cùng Dang): $J$ là trung điểm của $XY$, $N$ là điểm bất kì;
    bốn đẳng thức vectơ; hỏi có bao nhiêu đẳng thức đúng (sai). Chân trị tính bằng toạ độ ngẫu nhiên ($J$ là trung
    điểm).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, J, N = random.choice([("A", "B", "I", "M"), ("M", "N", "I", "O"), ("X", "Y", "J", "N"), ("P", "Q", "K", "M"),
                                    ("E", "F", "I", "S")])
        v = _b5_vt
        cap = [(_b5_cong(v(N, X), v(N, Y)), _b5_nhan(2, v(N, J))), (_b5_cong(v(J, X), v(J, Y)), _B5_0),
               (v(X, J), v(J, Y)), (v(X, Y), _b5_nhan(2, v(X, J))), (v(X, Y), _b5_nhan(2, v(J, Y))),
               (v(J, X), _b5_nhan(_Fr5(-1, 2), v(X, Y))),
               (_b5_cong(v(N, X), v(N, Y)), v(N, J)), (_b5_cong(v(N, X), v(N, Y)), _b5_nhan(2, v(J, N))),
               (v(J, X), v(J, Y)), (v(X, Y), _b5_nhan(2, v(J, X))), (_b5_cong(v(J, X), v(J, Y)), v(X, Y)),
               (_b5_tru(v(N, X), v(N, Y)), _b5_nhan(2, v(N, J))), (v(J, X), _b5_nhan(_Fr5(1, 2), v(X, Y)))]

        def rb(E):
            E[J] = (E[X] + E[Y]) / 2
        envs = _b5_env_diem([X, Y, N], rb)
        dung, sai = _c4s_phan_loai(cap, envs, [X, Y, J, N])
        mo = r"Let $%s$ be the midpoint of segment $%s$ and $%s$ an arbitrary point." % (J, X + Y, N)
        giai_mo = (r"$%s$ is the midpoint of $%s$, so $%s + %s = \overrightarrow{0}$ and for every point $%s$: $%s + %s = 2%s$.\\ " % (J, X + Y, _vt(J, X), _vt(J, Y), N, _vt(N, X), _vt(N, Y), _vt(N, J)))
        cau += _c4s_dem(mo, dung, sai, dang, 0, giai_mo)
    return cau


# ---------------------------------------------------------------------
# NB038_SA_A: vectơ bằng nhau trong hình (đếm đẳng thức đúng)
# ---------------------------------------------------------------------
def L10_C4_B7_NB038_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB038_MC_A (cùng Dang: nhận ra hai vectơ bằng nhau trong hình): bốn đẳng
    thức $\overrightarrow{XY} = \overrightarrow{ZT}$ theo hình (kho hình xoay vòng như NB038_MC_A_02); hỏi có bao nhiêu
    đẳng thức đúng (sai). Các đẳng thức sai là cặp dễ nhầm: cùng độ dài nhưng ngược hướng, cùng hướng nhưng khác độ
    dài, cùng độ dài nhưng không cùng phương.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        H = _c4_chon_hinh("nb038_sa_a")
        vts = _c4_tat_ca_vt(H)
        do = lambda w: math.hypot(*_c4_v(H, *w))
        dung, sai = [], []
        for i, u in enumerate(vts):
            for w in vts[i + 1:]:
                if set(u) == set(w):
                    continue
                a, b = _c4_v(H, *u), _c4_v(H, *w)
                cung_do = abs(do(u) - do(w)) < 1e-7
                tex = r"$%s = %s$" % (_vt(*u), _vt(*w))
                if _c4_bang(a, b):
                    dung.append((tex, r"$%s$ and $%s$ have the same direction and the same length" % (_vt(*u), _vt(*w))))
                elif cung_do and _c4_cp(a, b):
                    sai.append((tex, r"$%s$ and $%s$ have opposite directions" % (_vt(*u), _vt(*w))))
                elif _c4_ch(a, b):
                    sai.append((tex, r"$%s$ and $%s$ have the same direction but different lengths" % (_vt(*u), _vt(*w))))
                elif cung_do and not _c4_cp(a, b):
                    sai.append((tex, r"$%s$ and $%s$ have the same length but are not parallel" % (_vt(*u), _vt(*w))))
        if len(dung) < 3 or len(sai) < 3:
            continue
        so += 1
        cau += _c4s_dem(H["mo"], dung, sai, dang, _c4_tikz(H),
                        r"Two vectors are equal when they have the same direction and the same magnitude.\\ ")
    return cau


# ---------------------------------------------------------------------
# TH059_SA_A: tính chất của tích vô hướng (đếm khẳng định đúng)
# ---------------------------------------------------------------------
def _c4s_tvh_kho(k):
    """Kho khẳng định về tích vô hướng: (tex, hàm kiểm tra trên ba vectơ (số phức), lí do)."""
    a, b, c = r"\overrightarrow{a}", r"\overrightarrow{b}", r"\overrightarrow{c}"
    d = lambda u, v: (u.conjugate() * v).real
    return [
        (r"$%s\cdot %s = %s\cdot %s$" % (a, b, b, a), lambda A, B, C: (d(A, B), d(B, A)),
         r"the dot product is commutative"),
        (r"$%s\cdot\left(%s + %s\right) = %s\cdot %s + %s\cdot %s$" % (a, b, c, a, b, a, c),
         lambda A, B, C: (d(A, B + C), d(A, B) + d(A, C)), r"the dot product is distributive over vector addition"),
        (r"$%s\cdot\left(%s - %s\right) = %s\cdot %s - %s\cdot %s$" % (a, b, c, a, b, a, c),
         lambda A, B, C: (d(A, B - C), d(A, B) - d(A, C)), r"the dot product is distributive over vector subtraction"),
        (r"$\left(%d%s\right)\cdot %s = %d\left(%s\cdot %s\right)$" % (k, a, b, k, a, b),
         lambda A, B, C: (d(k * A, B), k * d(A, B)), r"$\left(k\vec a\right)\cdot\vec b = k\left(\vec a\cdot\vec b\right)$"),
        (r"$%s^{2} = \left|%s\right|^{2}$" % (a, a), lambda A, B, C: (d(A, A), abs(A) ** 2),
         r"the scalar square of a vector equals the square of its length"),
        (r"$\left(%s + %s\right)\cdot\left(%s - %s\right) = \left|%s\right|^{2} - \left|%s\right|^{2}$" % (a, b, a, b, a, b),
         lambda A, B, C: (d(A + B, A - B), abs(A) ** 2 - abs(B) ** 2),
         r"expanding the left-hand side gives $\vec a^{2} - \vec a\cdot\vec b + \vec b\cdot\vec a - \vec b^{2} = \left|\vec a\right|^{2} - \left|\vec b\right|^{2}$"),
        (r"$%s\cdot %s = -%s\cdot %s$" % (a, b, b, a), lambda A, B, C: (d(A, B), -d(B, A)),
         r"$\vec a\cdot\vec b = \vec b\cdot\vec a$, so the two sides are equal only when $\vec a\cdot\vec b = 0$"),
        (r"$%s\cdot\left(%s - %s\right) = %s\cdot %s + %s\cdot %s$" % (a, b, c, a, b, a, c),
         lambda A, B, C: (d(A, B - C), d(A, B) + d(A, C)), r"in fact $\vec a\cdot\left(\vec b - \vec c\right) = \vec a\cdot\vec b - \vec a\cdot\vec c$"),
        (r"$\left(%d%s\right)\cdot\left(%d%s\right) = %d\left(%s\cdot %s\right)$" % (k, a, k, b, k, a, b),
         lambda A, B, C: (d(k * A, k * B), k * d(A, B)), r"the left-hand side equals $%d\left(\vec a\cdot\vec b\right)$" % (k * k)),
        (r"$%s^{2} = \left|%s\right|$" % (a, a), lambda A, B, C: (d(A, A), abs(A)),
         r"$\vec a^{2} = \left|\vec a\right|^{2}$, not $\left|\vec a\right|$"),
        (r"$\left(%s + %s\right)\cdot\left(%s - %s\right) = \left|%s\right|^{2} + \left|%s\right|^{2}$" % (a, b, a, b, a, b),
         lambda A, B, C: (d(A + B, A - B), abs(A) ** 2 + abs(B) ** 2),
         r"the left-hand side equals $\left|\vec a\right|^{2} - \left|\vec b\right|^{2}$"),
        (r"$%s\cdot %s = \left|%s\right|\cdot\left|%s\right|$" % (a, b, a, b), lambda A, B, C: (d(A, B), abs(A) * abs(B)),
         r"$\vec a\cdot\vec b = \left|\vec a\right|\cdot\left|\vec b\right|\cdot\cos\left(\vec a, \vec b\right)$, which equals $\left|\vec a\right|\cdot\left|\vec b\right|$ only when the two vectors have the same direction"),
        (r"$\left(%s + %s\right)^{2} = \left|%s\right|^{2} + \left|%s\right|^{2}$" % (a, b, a, b),
         lambda A, B, C: (d(A + B, A + B), abs(A) ** 2 + abs(B) ** 2),
         r"$\left(\vec a + \vec b\right)^{2} = \left|\vec a\right|^{2} + 2\vec a\cdot\vec b + \left|\vec b\right|^{2}$"),
    ]


def L10_C4_B11_TH059_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH059_MC_A (cùng Dang: tính chất của tích vô hướng): bốn đẳng thức với ba
    vectơ tuỳ ý; hỏi có bao nhiêu đẳng thức đúng (sai). Chân trị tính bằng ba bộ vectơ ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        k = random.choice([2, 3, 4, 5, -2, -3])
        envs = [tuple(complex(random.uniform(-9, 9), random.uniform(-9, 9)) for _ in range(3)) for _ in range(3)]
        dung, sai = [], []
        for tex, f, ly in _c4s_tvh_kho(k):
            ok = all(abs(f(*E)[0] - f(*E)[1]) < 1e-7 for E in envs)
            (dung if ok else sai).append((tex, ly))
        mo = r"Given three arbitrary vectors $\overrightarrow{a}$, $\overrightarrow{b}$, $\overrightarrow{c}$."
        cau += _c4s_dem(mo, dung, sai, dang)
    return cau


# ---------------------------------------------------------------------
# NB049_SA_A, TH050_SA_A: toạ độ của vectơ
# ---------------------------------------------------------------------
def L10_C4_B10_NB049_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB049_MC_A (cùng Dang: nhận ra toạ độ của vectơ trong hệ trục): cho
    $\vec u = x\vec i + y\vec j$ hỏi hoành độ (tung độ) của $\vec u$, hoặc cho $\vec u = \left(x; y\right)$ viết
    $\vec u = m\vec i + n\vec j$ hỏi $m$ (hoặc $n$).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        x, y = random.randint(-9, 9), random.randint(-9, 9)
        if x == 0 and y == 0:
            continue
        w = (x, y, random.choice(["ij_hd", "ij_td", "td_m", "td_n"]))
        if w not in gt:
            gt.append(w)
    cau = ""
    for x, y, kieu in gt:
        u = r"\overrightarrow{u}"
        if kieu.startswith("ij"):
            hoi = "x-coordinate" if kieu == "ij_hd" else "y-coordinate"
            dap = x if kieu == "ij_hd" else y
            debai = (r"In the coordinate plane $Oxy$ with unit vectors $\overrightarrow{i}$, $\overrightarrow{j}$, given the vector $%s = %s$. Find the \textbf{%s} of the vector $%s$." % (u, _bt_ij(x, y), hoi, u))
            giai = r"$%s = %s$ so $%s = %s$, and the %s of $%s$ is $%d$." % (u, _bt_ij(x, y), u, _toado(x, y), hoi, u, dap)
        else:
            dap = x if kieu == "td_m" else y
            debai = (r"In the coordinate plane $Oxy$ with unit vectors $\overrightarrow{i}$, $\overrightarrow{j}$, given the vector $%s = %s$. Suppose $%s = m\overrightarrow{i} + n\overrightarrow{j}$. Find $%s$."
                     % (u, _toado(x, y), u, "m" if kieu == "td_m" else "n"))
            giai = (r"$%s = %s$ means $%s = %s$, so $m = %d$, $n = %d$." % (u, _toado(x, y), u, _bt_ij(x, y), x, y))
        ung = [y if dap == x else x, -dap, dap + 1, dap - 1, dap + 2, dap - 2]
        cau += MC_SA_answer_const(debai, str(dap), [str(t) for t in ung], giai, 0, 0, dang)
    return cau


def L10_C4_B10_TH050_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH050_MC_A (cùng Dang: toạ độ vectơ $\overrightarrow{AB}$ từ toạ độ hai
    điểm): hỏi hoành độ hoặc tung độ của $\overrightarrow{AB}$.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        w = tuple(random.randint(-6, 6) for _ in range(4)) + (random.choice(["x-coordinate", "y-coordinate"]),)
        if w[:2] != w[2:4] and w not in gt:
            gt.append(w)
    cau = ""
    for xa, ya, xb, yb, hoi in gt:
        dx, dy = xb - xa, yb - ya
        dap = dx if hoi == "x-coordinate" else dy
        debai = (r"In the coordinate plane $Oxy$, given two points $A%s$ and $B%s$. Find the \textbf{%s} of the vector $\overrightarrow{AB}$." % (_toado(xa, ya), _toado(xb, yb), hoi))
        giai = (r"$\overrightarrow{AB} = \left(x_B - x_A;\ y_B - y_A\right) = \left(%d - \left(%d\right);\ %d - \left(%d\right)\right) = %s$. So the %s of $\overrightarrow{AB}$ is $%d$." % (xb, xa, yb, ya, _toado(dx, dy), hoi, dap))
        ung = [(xa - xb) if hoi == "x-coordinate" else (ya - yb), (xa + xb) if hoi == "x-coordinate" else (ya + yb),
               dy if hoi == "x-coordinate" else dx, dap + 1, dap - 1, dap + 2]
        cau += MC_SA_answer_const(debai, str(dap), [str(t) for t in ung], giai, 0, 0, dang)
    return cau


def L10_C4_B10_TH050_MC_B_01(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với TH050_SA_B_01 (toạ độ đỉnh thứ tư của hình bình hành, hỏi hoành độ): gọi lại hàm SA
    với dang=1.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    return L10_C4_B10_TH050_SA_B_01(socau, dang)


def L10_C4_B10_VD054_MC_B_01(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với VD054_SA_B_01 (độ dài trung tuyến theo toạ độ): gọi lại hàm SA với dang=1.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    return L10_C4_B10_VD054_SA_B_01(socau, dang)


# ---------------------------------------------------------------------
# NB057_SA_A, TH057_SA_A, TH057_SA_B: góc giữa hai vectơ trên hình (đáp số là số đo độ)
# ---------------------------------------------------------------------
def L10_C4_B11_NB057_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB057_MC_A_01 (cùng cặp vectơ chung điểm đầu, tam giác đều).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    CAP = [("AB", "AC"), ("BA", "BC"), ("CA", "CB"), ("HB", "HC"),
           ("HA", "HB"), ("HC", "HA"), ("BC", "BA"), ("AC", "AB")]
    return _cau_goc_vecto(socau, dang, _TG_DEU, _hinh_tg_deu_H(), _TEN_TG, CAP, _GOC_TG, tra_loi_ngan=True)


def L10_C4_B11_NB057_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB057_MC_A_02 (chung điểm đầu, hình vuông).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    CAP = [("AB", "AD"), ("AB", "AC"), ("DA", "DB"), ("BA", "BD"),
           ("CB", "CD"), ("OA", "OB"), ("OA", "OC"), ("CA", "CD")]
    return _cau_goc_vecto(socau, dang, _HV, _hinh_hv_O(), _TEN_HV, CAP, _GOC_HV, tra_loi_ngan=True)


def L10_C4_B11_TH057_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH057_MC_A_01 (không chung điểm đầu, tam giác đều).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    CAP = [("AB", "BC"), ("AB", "CA"), ("BC", "CA"), ("AH", "BC"),
           ("AB", "HC"), ("HA", "BC"), ("BH", "CA"), ("AC", "HB")]
    return _cau_goc_vecto(socau, dang, _TG_DEU, _hinh_tg_deu_H(), _TEN_TG, CAP, _GOC_TG, tra_loi_ngan=True)


def L10_C4_B11_TH057_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH057_MC_A_02 (không chung điểm đầu, hình vuông).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    CAP = [("AB", "CD"), ("AB", "DC"), ("AC", "BD"), ("AB", "CA"),
           ("AD", "CB"), ("AB", "BD"), ("AO", "BC"), ("DO", "AB")]
    return _cau_goc_vecto(socau, dang, _HV, _hinh_hv_O(), _TEN_HV, CAP, _GOC_HV, tra_loi_ngan=True)


def L10_C4_B11_TH057_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH057_MC_B_01 (chung điểm cuối, tam giác đều).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    CAP = [("AB", "CB"), ("BA", "CA"), ("AC", "BC"), ("AH", "BH"),
           ("BH", "CH"), ("AB", "HB"), ("HC", "AC"), ("CH", "AH")]
    return _cau_goc_vecto(socau, dang, _TG_DEU, _hinh_tg_deu_H(), _TEN_TG, CAP, _GOC_TG, tra_loi_ngan=True)


def L10_C4_B11_TH057_SA_B_02(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH057_MC_B_02 (chung điểm cuối, hình vuông).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    CAP = [("AB", "CB"), ("AC", "BC"), ("AC", "DC"), ("BD", "AD"),
           ("AB", "DB"), ("AO", "CO"), ("AO", "BO"), ("DC", "BC")]
    return _cau_goc_vecto(socau, dang, _HV, _hinh_hv_O(), _TEN_HV, CAP, _GOC_HV, tra_loi_ngan=True)


# =====================================================================
# 16/10/2026 - BAI 7 BO SUNG theo cau mau co Lan gui (co Lan duyet ke hoach):
#   NB037_MC_E_01/_02 (chi MC - ngoai le): dien khuyet dinh nghia / ki hieu, diem dau, diem cuoi cua vecto.
#   NB037_MC_A_03, NB037_SA_A_02: ba, bon diem thang hang THEO THU TU -> cap vecto cung huong / nguoc huong.
#   NB037_MC_F / SA_F: dem so diem D thoa mot dieu kien ve vecto (vo so / 0 / 1 / 2); SA chi dung truong hop huu han.
# Moi de: ten diem, menh de, dieu kien chon ngau nhien.
# =====================================================================

_B7_TEN_DIEM = ["ABCD", "MNPQ", "EFGH", "IJKL", "ABCE", "DEFG", "MNPK", "XYZT"]


def _b7_hai_ten():
    return random.sample(list("ABCDEFGHIKMNPQ"), 2)


# ---------------------------------------------------------------- E: dien khuyet dinh nghia, ki hieu
def _b7_dinh_nghia():
    """Kho mệnh đề điền khuyết; tên điểm ngẫu nhiên. Mỗi phần tử: (câu dẫn, đáp án, [nhiễu], lời giải)."""
    X, Y, Z = random.sample(list("ABCDEFGHIKMNPQ"), 3)
    xy, yx = _vt(X, Y), _vt(Y, X)
    return [
        (r"A vector is a line segment", "that has a direction",
         ["that has a positive and a negative direction", "that has two endpoints", "of length $1$", "that is horizontal"],
         "A vector is a directed line segment, that is, of its two endpoints it is specified which is the initial point and which is the terminal point."),
        (r"The line of action of the vector $%s$ ($%s \ne %s$) is" % (xy, X, Y), r"the line $%s$" % (X + Y),
         [r"the segment $%s$" % (X + Y), r"the length of the segment $%s$" % (X + Y), r"tia $%s$" % (X + Y), r"the point $%s$" % Y],
         r"The line through the initial point and the terminal point of a vector is called its line of action; the line of action of $%s$ is the line $%s$." % (xy, X + Y)),
        (r"The length of the vector $%s$ is" % xy, r"the length of the segment $%s$" % (X + Y),
         [r"the line $%s$" % (X + Y), r"tia $%s$" % (Y + X), r"the vector $%s$" % yx, r"the number $1$"],
         r"The length of a vector is the distance between its initial point and its terminal point: $\left|%s\right| = %s$." % (xy, X + Y)),
        (r"Two vectors are called parallel (collinear) if", "their lines of action are parallel or coincide",
         ["they have the same length", "their lines of action are perpendicular", "they have the same initial point", "their lines of action intersect"],
         "By definition, two vectors are parallel if their lines of action are parallel or coincide."),
        (r"If two vectors are parallel, then", "they have the same direction or opposite directions",
         ["they always have the same direction", "they have the same length", "they are equal", "their lines of action always coincide"],
         "If two vectors are parallel, they can only have the same direction or opposite directions."),
        (r"If two vectors have the same direction, then", "they are parallel",
         ["they are equal", "they have the same length", "their lines of action are perpendicular", "they have the same terminal point"],
         "Two vectors with the same direction must first be parallel (their lines of action are parallel or coincide)."),
        (r"The zero vector is the vector", "whose initial point and terminal point coincide",
         ["of length $1$", "that has no line of action", "whose initial point is the origin", "that is not parallel to any vector"],
         r"The vector whose initial point and terminal point coincide is called the zero vector, denoted $\overrightarrow{0}$."),
        (r"Three distinct points $%s$, $%s$, $%s$ are collinear if and only if the vectors $%s$ and $%s$ are" % (X, Y, Z, xy, _vt(X, Z)),
         "collinear",
         ["same direction", "opposite direction", "of the same length", "are equal"],
         r"$%s$, $%s$, $%s$ are collinear if and only if $%s$ and $%s$ have the same line of action, that is, they are parallel (with the same direction or opposite directions)."
         % (X, Y, Z, xy, _vt(X, Z))),
        (r"The two vectors $%s$ and $%s$" % (xy, yx), "have the same length and opposite directions",
         ["are equal", "same direction", "have different lengths", "not collinear"],
         r"$%s$ and $%s$ have the same line of action $%s$ and the same length $%s$ but opposite directions." % (xy, yx, X + Y, X + Y)),
    ]


def L10_C4_B7_NB037_MC_E_01(socau, dang=1):
    r"""Điền khuyết định nghĩa: vectơ là đoạn thẳng có hướng; giá, độ dài, cùng phương, vectơ-không. Mệnh đề và ba
    phương án nhiễu chọn ngẫu nhiên từ kho (theo câu mẫu cô Lan gửi 16/10/2026: "Véc-tơ là một đoạn thẳng ...").

    CLAUDE THEM 16/10/2026 - chi co MC (ban SA dap so luon 1, vo ly); co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for mo, dung, sai, ly in random.sample(_b7_dinh_nghia(), min(socau, 9)):
        cau += MC_SA_answer_text(mo, dung, random.sample(sai, 3), ly, 0, 0, dang)
    return cau


def L10_C4_B7_NB037_MC_E_02(socau, dang=1):
    r"""Kí hiệu vectơ: vectơ có điểm đầu $X$, điểm cuối $Y$ kí hiệu thế nào; hoặc cho $\overrightarrow{XY}$, hỏi điểm đầu /
    điểm cuối / độ dài kí hiệu thế nào. Tên điểm ngẫu nhiên (theo câu mẫu cô Lan gửi).

    CLAUDE THEM 16/10/2026 - chi co MC; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        X, Y = _b7_hai_ten()
        kieu = random.choice(["ki_hieu", "dau", "cuoi", "do_dai"])
        if kieu == "ki_hieu":
            de = r"The vector with initial point $%s$ and terminal point $%s$ is denoted by" % (X, Y)
            dung = "$%s$" % _vt(X, Y)
            sai = ["$%s$" % (X + Y), "$%s$" % _vt(Y, X), r"$\left|%s\right|$" % _vt(X, Y)]
            ly = r"The vector with initial point $%s$ and terminal point $%s$ is denoted by $%s$." % (X, Y, _vt(X, Y))
        elif kieu in ("dau", "cuoi"):
            de = r"The %s point of the vector $%s$ is" % ("initial" if kieu == "dau" else "terminal", _vt(X, Y))
            dung = "the point $%s$" % (X if kieu == "dau" else Y)
            sai = ["the point $%s$" % (Y if kieu == "dau" else X), "the midpoint of the segment $%s$" % (X + Y),
                   "the line $%s$" % (X + Y)]
            ly = r"The vector $%s$ has initial point $%s$ and terminal point $%s$." % (_vt(X, Y), X, Y)
        else:
            de = r"The length of the vector $%s$ is denoted by" % _vt(X, Y)
            dung = r"$\left|%s\right|$" % _vt(X, Y)
            sai = ["$%s$" % _vt(X, Y), "$%s$" % _vt(Y, X), r"$-%s$" % _vt(X, Y)]
            ly = r"The length of the vector $%s$ is denoted by $\left|%s\right|$, and $\left|%s\right| = %s$." % (
                _vt(X, Y), _vt(X, Y), _vt(X, Y), X + Y)
        cau += MC_SA_answer_text(de, dung, sai, ly, 0, 0, dang)
    return cau


# ---------------------------------------------------------------- A: diem thang hang theo thu tu
def _b7_thang_hang():
    """n điểm thẳng hàng theo thứ tự trên đường thẳng: trả về (tên các điểm, mô tả, danh sách cặp (u, w, cùng hướng))."""
    n = random.choice([3, 3, 4])
    ten = list(random.choice(_B7_TEN_DIEM))[:n]
    if random.random() < 0.3:
        ten = ten[::-1] if n == 3 else ten
    vi_tri = {t: i for i, t in enumerate(ten)}
    vts = [(p, q) for p in ten for q in ten if p != q]
    cap = []
    for i, u in enumerate(vts):
        for w in vts[i + 1:]:
            if set(u) == set(w):              # cung mot doan (AB va BA): qua de
                continue
            hu = vi_tri[u[1]] > vi_tri[u[0]]
            hw = vi_tri[w[1]] > vi_tri[w[0]]
            cap.append((u, w, hu == hw))
    if n == 3:
        mo = r"Given three points $%s$, $%s$, $%s$ that are collinear in that order (point $%s$ lies between $%s$ and $%s$)." % (
            ten[0], ten[1], ten[2], ten[1], ten[0], ten[2])
    else:
        mo = r"Given four distinct points $%s$, $%s$, $%s$, $%s$ that are collinear in that order." % tuple(ten)
    return ten, mo, cap


def _b7_ly_cap(u, w, cung, ten):
    huong = lambda v: "from $%s$ to $%s$" % v
    return (r"$%s$ and $%s$ both lie on the line containing the points; $%s$ points %s and $%s$ points %s, so they have %s."
            % (_vt(*u), _vt(*w), _vt(*u), huong(u), _vt(*w), huong(w), "same direction" if cung else "opposite direction"))


def L10_C4_B7_NB037_MC_A_03(socau, dang=1):
    r"""Ba hoặc bốn điểm thẳng hàng THEO THỨ TỰ (không hình vẽ): cặp vectơ nào cùng hướng (ngược hướng). Ba phương án
    nhiễu là các cặp ngược (cùng) hướng - đều cùng phương nên phải xét hướng.

    CLAUDE THEM 16/10/2026 - theo cau mau co Lan gui; bien the cua NB037_MC_A (nhan ra cung phuong, cung huong); co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        ten, mo, cap = _b7_thang_hang()
        hoi_cung = random.random() < 0.6
        dung_ds = [c for c in cap if c[2] == hoi_cung]
        sai_ds = [c for c in cap if c[2] != hoi_cung]
        d = random.choice(dung_ds)
        sai = random.sample(sai_ds, 3)
        fmt = lambda c: r"$%s$ and $%s$" % (_vt(*c[0]), _vt(*c[1]))
        de = mo + r" Which of the following pairs of vectors have %s?" % ("same direction" if hoi_cung else "opposite direction")
        ly = r"All the vectors lie on the line containing the points, so they are parallel; compare directions: " + _b7_ly_cap(d[0], d[1], d[2], ten)
        cau += MC_SA_answer_text(de, fmt(d), [fmt(c) for c in sai], ly, 0, 0, dang)
    return cau


def L10_C4_B7_NB037_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn cùng dạng NB037_MC_A_03: ba/bốn điểm thẳng hàng theo thứ tự, cho bốn cặp vectơ, đếm số cặp cùng
    hướng (ngược hướng). Đáp số từ $1$ đến $3$.

    CLAUDE THEM 16/10/2026 - co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        ten, mo, cap = _b7_thang_hang()
        hoi_cung = random.random() < 0.5
        for _lan in range(200):
            chon = random.sample(cap, 4)
            k = sum(1 for c in chon if c[2] == hoi_cung)
            if 1 <= k <= 3:
                break
        hoi = "same direction" if hoi_cung else "opposite direction"
        dong = r"\\ ".join(r"%d) $%s$ and $%s$" % (i + 1, _vt(*c[0]), _vt(*c[1])) for i, c in enumerate(chon))
        de = mo + r" Consider four pairs of vectors: \\ " + dong + r"\\ How many pairs of vectors have the %s?" % hoi
        ly = (r"All the vectors are parallel (they lie on the line containing the points); we only compare directions:\\ "
              + r"\\ ".join(r"Pair %d: %s" % (i + 1, "same direction" if c[2] else "opposite direction") for i, c in enumerate(chon))
              + r".\\ Hence there are $%d$ pairs of vectors that have %s." % (k, hoi))
        cau += MC_SA_answer_const(de, str(k), [str(x) for x in _c4_nhieu_so(k, [4 - k, k + 1, k - 1, 4, 0])], ly, 0, 0, dang)
    return cau


# ---------------------------------------------------------------- F: dem so diem D thoa dieu kien vecto
def _b7_dieu_kien_D():
    """(câu dẫn, số điểm D: 'vô số' hoặc số nguyên, lời giải). Câu dẫn chỉ nêu các điểm mà điều kiện dùng đến."""
    A, B, C, D = random.choice(["ABCD", "MNPQ", "EFGH", "ABCM", "MNPK", "IJKL"])
    ab, cd, ba = _vt(A, B), _vt(C, D), _vt(B, A)
    k = random.choice([2, 3])
    ds = [
        # (dieu kien, so diem, loi giai, can C ngoai duong thang AB)
        (r"$%s = %s$" % (ab, cd), 1,
         r"$%s = %s$ if and only if $%s$ has the same direction as $%s$ and $%s = %s$: from $%s$ there is exactly one such point $%s$."
         % (ab, cd, cd, ab, C + D, A + B, C, D), False),
        (r"$%s = %s$" % (_vt(D, C), ab), 1,
         r"$%s = %s$ means $%s = %s$, so $%s$ is the unique point such that the vector from $%s$ to $%s$ equals $%s$: there is exactly one point."
         % (_vt(D, C), ab, cd, ba, D, C, D, ba), False),
        (r"$\left|%s\right| = \left|%s\right|$" % (ab, cd), "infinitely many",
         r"$\left|%s\right| = \left|%s\right| \Leftrightarrow %s = %s$: the points $%s$ form the circle with center $%s$ and radius $%s$, so there are infinitely many points."
         % (ab, cd, C + D, A + B, D, C, A + B), False),
        (r"$%s$ is parallel to $%s$ ($%s \ne %s$)" % (cd, ab, D, C), "infinitely many",
         r"$%s$ is parallel to $%s$ when $%s$ lies on the line through $%s$ parallel to (or coinciding with) the line $%s$, other than $%s$: there are infinitely many points."
         % (cd, ab, D, C, A + B, C), False),
        (r"$%s$ is parallel to $%s$ and $\left|%s\right| = \left|%s\right|$" % (cd, ab, cd, ab), 2,
         r"$%s$ lies on the line through $%s$ parallel to $%s$ and $%s = %s$: there are two points, symmetric about $%s$ (one gives $%s$ the same direction, the other gives $%s$ the opposite direction to $%s$)."
         % (D, C, ab, C + D, A + B, C, cd, cd, ab), False),
        (r"$%s$ is parallel to $%s$ and $\left|%s\right| = %d\left|%s\right|$" % (cd, ab, cd, k, ab), 2,
         r"$%s$ lies on the line through $%s$ parallel to $%s$ and $%s = %d%s$: there are two points, symmetric about $%s$."
         % (D, C, ab, C + D, k, A + B, C), False),
        (r"$%s$ has the same direction as $%s$ and $\left|%s\right| = %d\left|%s\right|$" % (cd, ab, cd, k, ab), 1,
         r"On the line through $%s$ parallel to $%s$, there is only one point $%s$ such that $%s$ has the same direction as $%s$ and $%s = %d%s$."
         % (C, ab, D, cd, ab, C + D, k, A + B), False),
        (r"$%s$ has the opposite direction to $%s$ and $\left|%s\right| = \left|%s\right|$" % (cd, ab, cd, ab), 1,
         r"Then $%s = %s$: there is exactly one point $%s$." % (cd, ba, D), False),
        (r"$%s$ is parallel to $%s$ and $%s$ lies on the line $%s$" % (cd, ab, D, A + B), 0,
         r"If $%s$ is parallel to $%s$, then $%s$ lies on the line through $%s$ parallel to $%s$; this line does not meet the line $%s$ (since $%s$ is not on $%s$). So there is no such point."
         % (cd, ab, D, C, A + B, A + B, C, A + B), True),
        (r"$%s = %s$" % (_vt(D, A), _vt(D, B)), 0,
         r"$%s = %s$ implies that $%s$ coincides with $%s$, contradicting $%s \ne %s$. So there is no such point." % (_vt(D, A), _vt(D, B), A, B, A, B), False),
        (r"$%s = %s$" % (_vt(A, D), _vt(D, B)), 1,
         r"$%s = %s$ if and only if $%s$ is the midpoint of the segment $%s$: there is exactly one point." % (_vt(A, D), _vt(D, B), D, A + B), False),
        (r"$\left|%s\right| = \left|%s\right|$" % (_vt(D, A), _vt(D, B)), "infinitely many",
         r"$%s = %s$: $%s$ lies on the perpendicular bisector of the segment $%s$, so there are infinitely many points." % (D + A, D + B, D, A + B), False),
    ]
    dk, so, ly, can_ngoai = random.choice(ds)
    if can_ngoai:
        mo = (r"Given two distinct points $%s$, $%s$ and a point $%s$ not on the line $%s$. How many points $%s$ satisfy %s?"
              % (A, B, C, A + B, D, dk))
    elif C in dk.replace(D, ""):
        mo = r"Given two distinct points $%s$, $%s$ and a point $%s$. How many points $%s$ satisfy %s?" % (A, B, C, D, dk)
    else:
        mo = r"Given two distinct points $%s$, $%s$. How many points $%s$ satisfy %s?" % (A, B, D, dk)
    return mo, so, ly


def L10_C4_B7_NB037_MC_F_01(socau, dang=1):
    r"""Đếm số điểm $D$ thoả một điều kiện về vectơ: bằng nhau, cùng độ dài (đường tròn, trung trực), cùng phương,
    cùng phương và cùng độ dài, vectơ-không... Đáp án trong $\{$vô số; $0$; $1$; $2\}$. Theo câu mẫu cô Lan gửi
    ($\left|\overrightarrow{AB}\right| = \left|\overrightarrow{CD}\right|$: vô số).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        mo, so, ly = _b7_dieu_kien_D()
        tat_ca = ["Infinitely many", "$0$", "$1$", "$2$"]
        dung = "Infinitely many" if so == "infinitely many" else "$%d$" % so
        cau += MC_SA_answer_text(mo, dung, [x for x in tat_ca if x != dung], ly, 0, 0, dang)
    return cau


def L10_C4_B7_NB037_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn cùng dạng NB037_MC_F: chỉ dùng điều kiện có HỮU HẠN điểm $D$ ($0$, $1$ hoặc $2$).

    CLAUDE THEM 16/10/2026 - co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        while True:
            mo, so, ly = _b7_dieu_kien_D()
            if so != "infinitely many":
                break
        cau += MC_SA_answer_const(mo, str(so), [str(x) for x in (0, 1, 2, 3, 4) if x != so], ly, 0, 0, dang)
    return cau


# =====================================================================
# 16/10/2026 - L10_C4_TF_C: DUNG/SAI theo cau mau co Lan gui (hinh binh hanh tam O; luc giac deu tam O canh a; tam giac
# co ba trung diem). Bon y TANG DAN: a) NB vecto bang nhau, cung huong / nguoc huong (Bai 7); b) TH cung phuong, vecto doi,
# ti so do dai (Bai 7); c) VD tong / hieu phai thay mot vecto bang vecto bang no roi dung quy tac ba diem (Bai 8);
# d) VDC do dai cua tong / hieu (Bai 8). MOI y co kho >= 3 phat bieu dung, >= 3 phat bieu sai; chan tri do Python tinh tu
# toa do hinh (chi dung quan he bat bien voi moi hinh binh hanh / tam giac: bang nhau, cung phuong, ti so do dai cung phuong).
# CLAUDE THEM 16/10/2026 - co Lan gui mau; co Lan duyet lai.
# =====================================================================

def _tfc_vec(P, X, Y):
    return (P[Y][0] - P[X][0], P[Y][1] - P[X][1])


def _tfc_bang(u, w, e=1e-9):
    return abs(u[0] - w[0]) < e and abs(u[1] - w[1]) < e


def _tfc_cp(u, w):
    return abs(u[0] * w[1] - u[1] * w[0]) < 1e-9


def _tfc_dai(u):
    return math.hypot(*u)


def _tfc_k(k):
    """Hệ số tỉ lệ hiển thị: 1 -> '', 2 -> '2', 1/2 -> '\\dfrac{1}{2}'."""
    return {1: "", 2: "2", 0.5: r"\dfrac{1}{2}", 3: "3"}[k]


def _tfc_hinh():
    kieu = random.choice(["hbh", "luc_giac", "tg_trung_diem"])
    H = _c4_hinh(kieu)
    if kieu == "luc_giac":
        doi = random.choice(["ABCDEF", "MNPQRS", "ABCDEF"])
        tam = random.choice(["O", "O", "I"])
        mp = dict(zip("ABCDEF", doi))
        mp["O"] = tam
        H["P"] = {mp[t]: v for t, v in H["P"].items()}
        H["canh"] = [(mp[a], mp[b]) for a, b in H["canh"]]
        H["tam"] = tam
        H["mo"] = r"Given a regular hexagon $%s$ with center $%s$ and side $a$ (see the figure)." % (doi, tam)
        H["ly_do"] = r"a regular hexagon with side $a$ is made of six equilateral triangles with side $a$ sharing the vertex $%s$" % tam
        H["ly_do_dai"] = (r"regular hexagon with side $a$: each side and each segment from the center to a vertex equals $a$, a short diagonal equals $a\sqrt{3}$, "
                          r"a diagonal through the center equals $2a$")
    elif kieu == "hbh":
        H["mo"] = r"Given a parallelogram $%s$ with center $%s$ (see the figure)." % ("".join(H["da_giac"]), H["tam"])
        H["ly_do"] = "opposite sides of a parallelogram are parallel and equal, and the center is the midpoint of both diagonals"
    else:
        H["ly_do"] = "properties of midpoints and midlines of a triangle: a midline is parallel to the third side and equal to half of it"
    return H


def _tfc_y(H):
    """Bốn kho phát biểu (a, b, c, d): mỗi phần tử (chuỗi \\choiceTFt, lời giải)."""
    P = H["P"]
    ten = list(P)
    lg = H["kieu"] == "luc_giac"
    vts = [(X, Y) for X in ten for Y in ten if X != Y]
    V = {v: _tfc_vec(P, *v) for v in vts}
    vt = lambda v: _vt(*v)
    don_vi = 2.0                                   # canh luc giac ve dai 2 = a

    def dong(phat, dung, ly):
        """phat: phát biểu đã có $...$ (chữ ở ngoài $)."""
        return (r"{\True %s}" % phat if dung else r"{%s}" % phat, ("True. " if dung else "False. ") + ly)

    # ---------------- a) NB: bang nhau, cung huong / nguoc huong (cac cap cung phuong, khac doan)
    a = []
    for i, u in enumerate(vts):
        for w in vts[i + 1:]:
            if set(u) == set(w) or not _tfc_cp(V[u], V[w]):
                continue
            bang = _tfc_bang(V[u], V[w])
            cung = V[u][0] * V[w][0] + V[u][1] * V[w][1] > 0
            cung_do_dai = abs(_tfc_dai(V[u]) - _tfc_dai(V[w])) < 1e-9
            if bang:
                a.append(dong(r"$%s = %s$" % (vt(u), vt(w)), True,
                              r"$%s$ and $%s$ have the same direction and the same length, so they are equal (%s)." % (vt(u), vt(w), H["ly_do"])))
            elif cung_do_dai or cung:
                a.append(dong(r"$%s = %s$" % (vt(u), vt(w)), False,
                              r"$%s$ and $%s$: %s, so they are not equal." % (vt(u), vt(w), "opposite direction" if not cung else "have different lengths")))
            if not set(u) & set(w):
                hoi = random.choice(["same direction", "opposite direction"])
                a.append(dong(r"$%s$ and $%s$: %s" % (vt(u), vt(w), hoi), cung == (hoi == "same direction"),
                              r"$%s$ and $%s$ are collinear and have the %s (%s)." % (vt(u), vt(w), "same direction" if cung else "opposite direction", H["ly_do"])))

    # ---------------- b) TH: cung phuong (khong tam thuong), vecto doi, ti so do dai
    b = []
    for i, u in enumerate(vts):
        for w in vts[i + 1:]:
            if set(u) & set(w):
                continue
            cp = _tfc_cp(V[u], V[w])
            b.append(dong(r"$%s$ and $%s$ are collinear" % (vt(u), vt(w)), cp,
                          (r"The lines containing $%s$ and $%s$ are parallel or coincide, so the two vectors are collinear." if cp else
                           r"The lines containing $%s$ and $%s$ intersect, so the two vectors are not collinear.") % (vt(u), vt(w))))
            if cp:
                doi = _tfc_bang(V[u], (-V[w][0], -V[w][1]))
                b.append(dong(r"$%s$ and $%s$ are opposite vectors" % (vt(u), vt(w)), doi,
                              (r"$%s$ and $%s$ have opposite directions and the same length, so they are opposite vectors (%s)." if doi else
                               r"$%s$ and $%s$ do not have opposite directions or do not have the same length, so they are not opposite vectors.")
                              % ((vt(u), vt(w), H["ly_do"]) if doi else (vt(u), vt(w)))))
                r = _tfc_dai(V[u]) / _tfc_dai(V[w])
                for k in (0.5, 2):
                    if abs(r - k) < 1e-9:
                        b.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (vt(u), _tfc_k(k), vt(w)), True,
                                      r"$%s = %s%s$ (%s)." % ("".join(u), _tfc_k(k), "".join(w), H["ly_do"])))
                        sai_k = 2 if k == 0.5 else 0.5
                        b.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (vt(u), _tfc_k(sai_k), vt(w)), False,
                                      r"In fact $%s = %s%s$ (%s)." % ("".join(u), _tfc_k(k), "".join(w), H["ly_do"])))
    if lg:
        for u in vts:
            d = _tfc_dai(V[u]) / don_vi
            that = "a" if abs(d - 1) < 1e-9 else (r"a\sqrt{3}" if abs(d - math.sqrt(3)) < 1e-9 else "2a")
            for c in ("a", r"a\sqrt{3}", "2a"):
                b.append(dong(r"$\left|%s\right| = %s$" % (vt(u), c), c == that,
                              r"$\left|%s\right| = %s = %s$ (%s)." % (vt(u), "".join(u), that, H["ly_do_dai"])))

    # ---------------- c) VD: tong / hieu, phai thay mot vecto bang vecto bang no (khong phai quy tac 3 diem / hbh truc tiep)
    def ten_vt(z):
        if _tfc_dai(z) < 1e-9:
            return r"\overrightarrow{0}"
        for v in vts:
            if _tfc_bang(V[v], z):
                return vt(v)
        return None

    c, d_ = [], []
    for u in vts:
        for v in vts:
            if u == v or set(u) == set(v):
                continue
            for phep in ("+", "-"):
                if phep == "+" and (u[1] == v[0] or u[0] == v[0]):
                    continue               # quy tac ba diem / hbh: qua de cho muc VD
                if phep == "-" and u[0] == v[0]:
                    continue               # quy tac hieu truc tiep
                z = (V[u][0] + V[v][0], V[u][1] + V[v][1]) if phep == "+" else (V[u][0] - V[v][0], V[u][1] - V[v][1])
                # vecto thay the bat dau tai diem cuoi cua u
                can = V[v] if phep == "+" else (-V[v][0], -V[v][1])
                thay = [x for x in vts if x[0] == u[1] and _tfc_bang(V[x], can)]
                if not thay:
                    continue
                t = thay[0]
                ket = ten_vt(z)
                if ket is None:
                    continue
                cuoi = (u[0], t[1])
                bt = r"%s %s %s" % (vt(u), phep, vt(v))
                buoc = (r"Since $%s %s %s$, we have $%s = %s + %s = %s$ (triangle rule)."
                        % (("-" + vt(v)) if phep == "-" else vt(v), "=", vt(t), bt, vt(u), vt(t),
                           vt(cuoi) if cuoi[0] != cuoi[1] else r"\overrightarrow{0}"))
                buoc_dung = buoc
                if ket != (vt(cuoi) if cuoi[0] != cuoi[1] else r"\overrightarrow{0}"):
                    buoc_dung += r" Moreover $%s = %s$ (%s)." % (vt(cuoi), ket, H["ly_do"])
                c.append(dong(r"$%s = %s$" % (bt, ket), True, buoc_dung))
                # sai: nguoc chieu / doi phep tinh
                sai_z = (-z[0], -z[1])
                sai = ten_vt(sai_z) if _tfc_dai(z) > 1e-9 else None
                if sai:
                    c.append(dong(r"$%s = %s$" % (bt, sai), False, buoc + r" It is not $%s$." % sai))
                z2 = (V[u][0] - V[v][0], V[u][1] - V[v][1]) if phep == "+" else (V[u][0] + V[v][0], V[u][1] + V[v][1])
                sai2 = ten_vt(z2)
                if sai2 and not _tfc_bang(z2, z):
                    c.append(dong(r"$%s = %s$" % (bt, sai2), False, buoc + r" It is not $%s$." % sai2))
                # ---------------- d) VDC: do dai cua tong / hieu
                L = _tfc_dai(z)
                if L < 1e-9:
                    continue
                if lg:
                    dd = L / don_vi
                    that = "a" if abs(dd - 1) < 1e-9 else (r"a\sqrt{3}" if abs(dd - math.sqrt(3)) < 1e-9 else
                                                            ("2a" if abs(dd - 2) < 1e-9 else None))
                    if that is None:
                        continue
                    for cc in ("a", r"a\sqrt{3}", "2a"):
                        d_.append(dong(r"$\left|%s\right| = %s$" % (bt, cc), cc == that,
                                       buoc + r" Hence $\left|%s\right| = %s = %s$ (%s)." % (bt, "".join(cuoi), that, H["ly_do_dai"])))
                else:
                    for w in vts:
                        if set(w) == set(cuoi) or not _tfc_cp(V[w], z):
                            continue
                        r = L / _tfc_dai(V[w])
                        for k in (0.5, 2):
                            if abs(r - k) < 1e-9:
                                ly = buoc + r" Hence $\left|%s\right| = %s = %s%s$ (%s)." % (bt, "".join(cuoi), _tfc_k(k), "".join(w), H["ly_do"])
                                d_.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (bt, _tfc_k(k), vt(w)), True, ly))
                                d_.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (bt, _tfc_k(2 if k == 0.5 else 0.5), vt(w)),
                                               False, ly))
                    # |u + v| = |w| voi w bang hoac doi z (khac ten): dung; voi w cung phuong khac do dai: sai
                    for w in vts:
                        if set(w) == set(cuoi) or not _tfc_cp(V[w], z):
                            continue
                        bang_dd = abs(_tfc_dai(V[w]) - L) < 1e-9
                        ly = buoc + r" Hence $\left|%s\right| = %s$, which is %s $%s$ (%s)." % (
                            bt, "".join(cuoi), "equal to" if bang_dd else "different from", "".join(w), H["ly_do"])
                        d_.append(dong(r"$\left|%s\right| = \left|%s\right|$" % (bt, vt(w)), bang_dd, ly))
    return a, b, c, d_


def _tfc_loc(ds, n=4):
    """Giữ tối đa n đúng + n sai khác nhau, chọn ngẫu nhiên (đủ đa dạng mà lời giải gọn)."""
    dung = list({t: (t, l) for t, l in ds if r"\True" in t}.values())
    sai = list({t: (t, l) for t, l in ds if r"\True" not in t}.values())
    random.shuffle(dung)
    random.shuffle(sai)
    return dung[:n] + sai[:n]


def L10_C4_TF_C_01(socau, socot=1):
    r"""Đúng/Sai theo câu mẫu cô Lan gửi: hình bình hành tâm $O$, lục giác đều tâm $O$ cạnh $a$, tam giác có ba trung điểm.
    a) NB bằng nhau, cùng/ngược hướng; b) TH cùng phương, vectơ đối, tỉ số độ dài (độ dài theo $a$ với lục giác);
    c) VD tổng, hiệu (thay một vectơ bằng vectơ bằng nó rồi dùng quy tắc ba điểm); d) VDC độ dài của tổng, hiệu.

    CLAUDE THEM 16/10/2026 - co Lan gui mau; co Lan duyet lai."""
    cauTF = ""
    da = 0
    while da < socau:
        H = _tfc_hinh()
        # Bon kho do _tfc_y tra ve, dung thu tu:
        # a) NB  - hai vecto bang nhau, cung huong / nguoc huong (Bai 7)
        # b) TH  - cung phuong, hai vecto doi nhau, ti so do dai / do dai theo a (Bai 7)
        # c) VD  - tong, hieu: thay mot vecto bang vecto bang no roi dung quy tac ba diem (Bai 8)
        # d) VDC - do dai cua tong, hieu (Bai 8)
        kho = [_tfc_loc(y) for y in _tfc_y(H)]
        if any(sum(1 for t, _ in y if r"\True" in t) < 3 or sum(1 for t, _ in y if r"\True" not in t) < 3 for y in kho):
            continue
        debai = H["mo"] + " Determine whether each of the following statements is true or false:"
        cauTF += TF_baitoan_du(debai, kho, _c4_tikz(H), 0, socot)
        da += 1
    return cauTF


# =====================================================================
# 16/10/2026 - L10_C4_B7_VD039 (co Lan: "day la cau VD cua bai 7. Lam cho ca MC va SA"):
# vat chuyen dong deu tu A theo huong (vd N20 do E) voi van toc v trong t gio den B -> AB = v.t va A o huong NGUOC lai so
# voi B (N <-> S, E <-> W, giu nguyen goc). Muc VD cao hon YCCD TH039 cua Bo (bieu dien dai luong thuc tien bang vecto)
# -> LUYEN TAP THEM. Boi canh: tau tren bien Dong, ca no tren ho, may bay (khong trung boi canh co san).
# =====================================================================

_VD039_PT = {
    "tau_bien_dong": ("In the East Sea, a ship moves uniformly", "the ship", [15, 18, 20, 24, 25, 30]),
    "ca_no_tren_ho": ("On a large lake, a motorboat moves uniformly", "the motorboat", [20, 24, 30, 36, 40]),
    "may_bay": ("An airplane flies uniformly in a straight line", "the airplane", [600, 640, 720, 800, 840]),
}


def _vd039_huong(dau1, goc, dau2):
    return r"$\mathrm{%s}%d^\circ\mathrm{%s}$" % (dau1, goc, dau2)


def _vd039_so(x):
    """Số km gọn: 48 -> '48', 22.5 -> '22{,}5'."""
    return ("%d" % x) if abs(x - round(x)) < 1e-9 else ("%g" % x).replace(".", "{,}")


def _vd039_sinh():
    """Thời gian cho bằng giờ hoặc phút (đổi ra giờ); quãng đường là số nguyên hoặc thập phân một chữ số."""
    while True:
        bc = random.choice(list(_VD039_PT))
        mo, ten, ds_v = _VD039_PT[bc]
        v = random.choice(ds_v)
        if random.random() < 0.5:
            t_ph = random.choice([60, 120, 180] if bc != "may_bay" else [60, 120])
        else:
            t_ph = random.choice([30, 45, 90, 150] if bc != "may_bay" else [15, 30, 45, 90])
        d = v * t_ph / 60
        if abs(d * 10 - round(d * 10)) > 1e-9 or len(_vd039_so(d).replace("{,}", ",")) > 4:
            continue
        break
    goc = random.choice(range(10, 85, 5))
    d1, d2 = random.choice("NS"), random.choice("EW")
    n1, n2 = {"N": "S", "S": "N"}[d1], {"E": "W", "W": "E"}[d2]
    if t_ph % 60 == 0:
        tg, doi = r"$%d$ hours" % (t_ph // 60), ""
        t_tex = "%d" % (t_ph // 60)
    else:
        tg = (r"$%d$ hours $%d$ minutes" % (t_ph // 60, t_ph % 60)) if t_ph > 60 else r"$%d$ minutes" % t_ph
        t_tex = _vd039_so(t_ph / 60)
        doi = r"Convert %s $= %s$ hours. " % (tg, t_tex)
    de = (r"%s from position $A$ in the direction %s at a speed of $%d$ km/h. After %s, %s reaches position $B$."
          % (mo, _vd039_huong(d1, goc, d2), v, tg, ten))
    ve = (doi + r"The velocity vector has direction %s and magnitude $%d$ km/h, so the displacement vector $\overrightarrow{AB}$ has the same direction as "
          r"the velocity vector and length $AB = %d\cdot %s = %s$ (km).\\ "
          r"The vector $\overrightarrow{BA}$ has the opposite direction to $\overrightarrow{AB}$: change $\mathrm{%s}$ to $\mathrm{%s}$ and $\mathrm{%s}$ "
          r"to $\mathrm{%s}$, keeping the angle $%d^\circ$. So $A$ is in the direction %s from $B$."
          % (_vd039_huong(d1, goc, d2), v, v, t_tex, _vd039_so(d), d1, n1, d2, n2, goc, _vd039_huong(n1, goc, n2)))
    return bc, de, d, (d1, goc, d2), (n1, goc, n2), v, t_ph, ve


def L10_C4_B7_VD039_MC_A_01(socau, dang=1):
    r"""Toán thực tế (VD): vật chuyển động đều từ $A$ theo hướng $\mathrm{N}\alpha^\circ\mathrm{E}$ (hoặc S, W) với vận tốc $v$
    trong $t$ giờ đến $B$; hỏi $A$ cách $B$ bao nhiêu km và ở hướng nào so với $B$. Nhiễu: giữ nguyên hướng
    $\overrightarrow{AB}$, đổi một chữ, lấy góc phụ, quãng đường sai ($v$, $v + t$).

    CLAUDE THEM 16/10/2026 - theo cau mau co Lan gui (tau tren bien Dong N20 do E, 20 km/h, 2 gio); luyen tap them."""
    cau = ""
    for _ in range(socau):
        bc, de, d, h, n, v, t, ve = _vd039_sinh()
        de += r" How many kilometers is $A$ from $B$, and in which direction is it from $B$?"
        p = lambda kc, hh: r"$%s$ km, direction %s" % (_vd039_so(kc), _vd039_huong(*hh))
        dung = p(d, n)
        kc_sai = v                               # lay van toc lam quang duong
        ung = [p(d, h), p(d, (n[0], n[1], h[2])), p(d, (n[0], 90 - n[1], n[2])) if n[1] != 45 else p(d, (h[0], n[1], n[2])),
               p(kc_sai, n), p(2 * d, n)]
        sai = []
        for x in ung:
            if x != dung and x not in sai:
                sai.append(x)
        cau += MC_SA_answer_text(de, dung, random.sample(sai[:4], 3), ve, 0, 0, dang)
    return cau


def L10_C4_B7_VD039_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn cùng dạng VD039_MC_A: hỏi $A$ cách $B$ bao nhiêu kilômét (thời gian có thể cho bằng phút, phải đổi
    ra giờ). Không hỏi góc vì góc chép lại được từ đề.

    CLAUDE THEM 16/10/2026 - co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        bc, de, d, h, n, v, t, ve = _vd039_sinh()
        de += r" How many kilometers is $A$ from $B$?"
        dap = _vd039_so(d).replace("{,}", ",")
        ung = [_vd039_so(x).replace("{,}", ",") for x in (v, 2 * d, d + v, d / 2)]
        cau += MC_SA_answer_const(de, dap, [x for x in ung if x != dap] + ["1", "2", "3"], ve, 0, 0, dang)
    return cau


# =====================================================================
# 16/10/2026 - L10_C4_B7_VD039 chu B (co Lan: "ra bai ve ung dung nay, la bai VD. ra bai MC va SA thoi" - theo Vi du 4
# SGK: luc day Archimedes F va trong luc P tac dong len vat A chim hoan toan trong chat long, ve tren luoi o vuong).
# Vat chim hoan toan: |F| = d_long.V, |P| = d_vat.V -> d_vat / d_long = |P| / |F| (doc so o tren hinh).
#   chim xuong / nam yen o day: |P| > |F|;  lo lung: |P| = |F|;  dang noi len: |P| < |F|.
# LUYEN TAP THEM nhu VD039_A (YCCD cua Bo chi TH039).
# =====================================================================

_VD039B_TINH_HUONG = {
    "chim": r"An object $A$ is dropped into a cup of liquid; it is completely submerged and rests at the bottom of the cup.",
    "lo_lung": r"An object $A$ is dropped into a cup of liquid and stays suspended, completely submerged in the liquid.",
    "noi": r"An object $A$ is completely submerged in a cup of liquid and is rising.",
}


def _vd039b_hinh(F, P, goc_F=90, chieu_P=-1, tinh_huong="chim", nhan=True, kich=None):
    r"""TikZ cốc chất lỏng trên lưới ô vuông: điểm đặt $A$, vectơ $\overrightarrow{F}$ dài F ô theo góc goc_F (độ),
    vectơ $\overrightarrow{P}$ dài P ô hướng xuống (chieu_P = -1) hoặc lên (+1)."""
    xA = 3
    duoi = (kich if kich else max(P if chieu_P < 0 else 0, F if goc_F > 180 else 0)) + 1   # cho mui ten huong xuong
    yA = duoi + (0.5 if tinh_huong == "chim" else 1.5)
    tren = yA + (kich if kich else max(F if goc_F < 180 else 0, P if chieu_P > 0 else 0)) + 1   # kich: cung khung cho moi phuong an
    H = int(math.ceil(tren)) + 1
    day = yA - 0.5 if tinh_huong == "chim" else duoi
    mat = tren - 0.4
    s = [r"\begin{tikzpicture}[scale=0.45,>=stealth]",
         r"\draw[gray!50,very thin] (0,0) grid (6,%d);" % H,
         r"\fill[cyan!10] (0.8,%s) -- (5.2,%s) -- (5.6,%s) -- (0.4,%s) -- cycle;" % (_toa(day), _toa(day), _toa(mat), _toa(mat)),
         r"\draw[thick] (0.2,%s) -- (0.8,%s) -- (5.2,%s) -- (5.8,%s);" % (_toa(mat + 0.6), _toa(day), _toa(day), _toa(mat + 0.6)),
         r"\draw[dashed,gray] (0.4,%s) -- (5.6,%s);" % (_toa(mat), _toa(mat)),
         r"\fill[gray!55] (2,%s) rectangle (4,%s);" % (_toa(yA - 0.5), _toa(yA + 0.5)),
         r"\node at (2.4,%s) {$A$};" % _toa(yA)]
    gx, gy = math.cos(math.radians(goc_F)) * F, math.sin(math.radians(goc_F)) * F
    s.append(r"\draw[->,thick] (%d,%s) -- (%s,%s);" % (xA, _toa(yA), _toa(xA + gx), _toa(yA + gy)))
    s.append(r"\draw[->,thick,blue] (%d,%s) -- (%d,%s);" % (xA, _toa(yA), xA, _toa(yA + chieu_P * P)))
    if nhan:
        s.append(r"\node[left] at (%s,%s) {$\overrightarrow{F}$};" % (_toa(xA + gx / 2), _toa(yA + gy / 2 + 0.3)))
        s.append(r"\node[right,blue] at (%d,%s) {$\overrightarrow{P}$};" % (xA, _toa(yA + chieu_P * P / 2)))
    s.append(r"\fill[red] (%d,%s) circle (2.5pt);" % (xA, _toa(yA)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def _vd039b_ps(p, q):
    from fractions import Fraction as _Fr
    r = _Fr(p, q)
    return ("%d" % r.numerator) if r.denominator == 1 else r"\dfrac{%d}{%d}" % (r.numerator, r.denominator)


def _vd039b_so_lieu(can_sa):
    while True:
        F, P = random.randint(1, 6), random.randint(1, 6)
        th = "chim" if P > F else ("lo_lung" if P == F else "noi")
        if th == "lo_lung" and random.random() < 0.6:          # it lo lung hon
            continue
        if can_sa:
            from fractions import Fraction as _Fr
            r = _Fr(P, F)
            if r.denominator not in (1, 2, 4, 5) or len(("%g" % float(r))) > 4:
                continue
        return F, P, th


def L10_C4_B7_VD039_MC_B_01(socau, dang=1):
    r"""Hình trên lưới ô vuông biểu diễn lực đẩy Archimedes $\overrightarrow{F}$ và trọng lực $\overrightarrow{P}$ tác động lên
    vật $A$ chìm hoàn toàn (độ dài vectơ tỉ lệ với độ lớn lực): tìm tỉ số trọng lượng riêng của vật và của chất lỏng
    ($d_A : d_\ell = \left|\overrightarrow{P}\right| : \left|\overrightarrow{F}\right|$). Theo Ví dụ 4 SGK.

    CLAUDE THEM 16/10/2026 - co Lan gui mau; luyen tap them; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        F, P, th = _vd039b_so_lieu(False)
        hoi_nguoc = random.random() < 0.4
        de = (_VD039B_TINH_HUONG[th] + r" The figure shows the buoyant (Archimedes) force $\overrightarrow{F}$ and the weight "
              r"$\overrightarrow{P}$ acting on the object $A$ (the length of each vector is proportional to the magnitude of the force). Let $d_A$, $d_\ell$ be "
              r"the specific weights of the object $A$ and of the liquid. The ratio $\dfrac{%s}{%s}$ equals"
              % (("d_\\ell", "d_A") if hoi_nguoc else ("d_A", "d_\\ell")))
        tu, mau = (F, P) if hoi_nguoc else (P, F)
        dap = "$%s$" % _vd039b_ps(tu, mau)
        ung = ["$%s$" % _vd039b_ps(mau, tu), "$%s$" % _vd039b_ps(tu + mau, mau), "$%s$" % _vd039b_ps(abs(tu - mau) or 2, mau),
               "$%s$" % _vd039b_ps(tu, tu + mau), "$%s$" % _vd039b_ps(tu + 1, mau),
               "$2$", r"$\dfrac{1}{2}$", r"$\dfrac{3}{2}$", "$3$"]
        sai = []
        for x in ung:
            if x != dap and x not in sai:
                sai.append(x)
        giai = (r"Since $A$ is completely submerged, the volume of liquid displaced equals the volume $V$ of the object: "
                r"$\left|\overrightarrow{F}\right| = d_\ell V$, $\left|\overrightarrow{P}\right| = d_A V$.\\ "
                r"In the figure, $\overrightarrow{F}$ is $%d$ squares long and $\overrightarrow{P}$ is $%d$ squares long, so "
                r"$\dfrac{d_A}{d_\ell} = \dfrac{\left|\overrightarrow{P}\right|}{\left|\overrightarrow{F}\right|} = %s$"
                % (F, P, _vd039b_ps(P, F)))
        giai += (r", hence $\dfrac{d_\ell}{d_A} = %s$." % _vd039b_ps(F, P)) if hoi_nguoc else "."
        cau += MC_SA_answer_text(de, dap, sai[:3], giai, _vd039b_hinh(F, P, tinh_huong=th), 0, dang)
    return cau


def L10_C4_B7_VD039_MC_B_02(socau, dang=1):
    r"""Cho tình huống (vật chìm nằm yên ở đáy / lơ lửng / đang nổi lên), chọn hình biểu diễn đúng lực đẩy Archimedes
    $\overrightarrow{F}$ và trọng lực $\overrightarrow{P}$ (Ví dụ 4 SGK hỏi ngược). Nhiễu: $\overrightarrow{F}$ xiên,
    sai quan hệ độ dài, $\overrightarrow{F}$ cùng hướng $\overrightarrow{P}$.

    CLAUDE THEM 16/10/2026 - co Lan gui mau; luyen tap them; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        th = random.choice(["chim", "chim", "lo_lung", "noi"])
        a, b = sorted(random.sample(range(1, 5), 2))       # a < b
        dung = {"chim": (a, b), "lo_lung": (b, b), "noi": (b, a)}[th]
        sai_dai = [x for x in ((a, b), (b, b), (b, a)) if x != dung]
        hinh = [_vd039b_hinh(*dung, tinh_huong=th, kich=b)]
        hinh += [_vd039b_hinh(F, P, tinh_huong=th, kich=b) for F, P in sai_dai]
        hinh.append(_vd039b_hinh(dung[0], dung[1], goc_F=random.choice([60, 120]), tinh_huong=th, kich=b))
        de = (_VD039B_TINH_HUONG[th] + r" Which of the following figures correctly shows the buoyant (Archimedes) force $\overrightarrow{F}$ and the "
              r"weight $\overrightarrow{P}$ acting on the object $A$ (the length of each vector is proportional to the magnitude of the force)?")
        ly = {"chim": r"the object sinks to the bottom, so the weight is greater than the buoyant force: $\left|\overrightarrow{P}\right| > \left|\overrightarrow{F}\right|$",
              "lo_lung": r"the object is suspended, so the two forces balance: $\left|\overrightarrow{P}\right| = \left|\overrightarrow{F}\right|$",
              "noi": r"the object is rising, so the buoyant force is greater than the weight: $\left|\overrightarrow{F}\right| > \left|\overrightarrow{P}\right|$"}[th]
        giai = (r"The weight $\overrightarrow{P}$ points vertically downward and the buoyant force $\overrightarrow{F}$ points vertically "
                r"upward (the two vectors have opposite directions on the same vertical line); " + ly
                + r". Only one figure satisfies both the directions and the relation between the lengths.")
        cau += MC_SA_answer_text(de, hinh[0], random.sample(hinh[1:], 3), giai, 0, 0, dang)
    return cau


def L10_C4_B7_VD039_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn cùng dạng VD039_MC_B: đọc hình, tính tỉ số $\dfrac{d_A}{d_\ell}$ (hoặc $\dfrac{d_\ell}{d_A}$), viết dạng
    số thập phân.

    CLAUDE THEM 16/10/2026 - co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        F, P, th = _vd039b_so_lieu(True)
        nguoc = random.random() < 0.4 and (P / F) != 1 and len("%g" % (F / P)) <= 4 and (F * 1000 % P == 0)
        de = (_VD039B_TINH_HUONG[th] + r" The figure shows the buoyant (Archimedes) force $\overrightarrow{F}$ and the weight "
              r"$\overrightarrow{P}$ acting on the object $A$ (the length of each vector is proportional to the magnitude of the force). Let $d_A$, $d_\ell$ be "
              r"the specific weights of the object $A$ and of the liquid. Compute the ratio $\dfrac{%s}{%s}$ (as a decimal)."
              % ((r"d_\ell", "d_A") if nguoc else ("d_A", r"d_\ell")))
        v = F / P if nguoc else P / F
        dap = ("%g" % v).replace(".", ",")
        giai = (r"Since $A$ is completely submerged, $\left|\overrightarrow{F}\right| = d_\ell V$, $\left|\overrightarrow{P}\right| = d_A V$ "
                r"($V$ is the volume of the object). In the figure, $\overrightarrow{F}$ is $%d$ squares long and $\overrightarrow{P}$ is $%d$ squares long, so "
                r"$\dfrac{%s}{%s} = \dfrac{%d}{%d} = %s$." % ((F, P) + ((r"d_\ell", "d_A", F, P) if nguoc else ("d_A", r"d_\ell", P, F)) + (dap,)))
        ung = [("%g" % x).replace(".", ",") for x in (F / P, P + F, (P + F) / F, P / F + 1) if len("%g" % x) <= 4]
        cau += MC_SA_answer_const(de, dap, [x for x in ung if x != dap] + ["1", "2", "0,5", "1,5", "3", "2,5"], giai,
                                  _vd039b_hinh(F, P, tinh_huong=th), 0, dang)
    return cau


# =====================================================================
# BÀI 8 BỔ SUNG 16/10/2026 (cô Lan gửi câu mẫu, đã duyệt kế hoạch ID):
#   TH040_MC_A_02, TH041_MC_A_02, TH040_MC_B_02 (biến thể "khẳng định nào đúng");
#   TH040_MC_C, SA_C (độ dài vectơ tổng), TH041_MC_C, SA_C (độ dài vectơ hiệu) - dạng mới;
#   B11_VD060_MC_A_02, SA_A_02 (hợp lực hai lực, góc bất kì).
# Mọi chân trị kiểm bằng toạ độ (ngẫu nhiên hoặc chính xác bằng sympy), không viết tay.
# =====================================================================
import sympy as _sp8
from decimal import Decimal as _Dec8, ROUND_HALF_UP as _HU8

_B8_BO_DIEM = [("A", "B", "C"), ("M", "N", "P"), ("D", "E", "F"), ("I", "J", "K"), ("X", "Y", "Z"), ("O", "A", "B")]


def _b8_ba_diem(loai):
    r"""Câu ``khẳng định nào luôn đúng'' về $\overrightarrow{UV}$ phân tích qua điểm thứ ba $W$.
    loai 'tong': đáp án là tổng theo quy tắc ba điểm; 'hieu': đáp án là hiệu hai vectơ chung điểm đầu (quy tắc trừ).
    Nhiễu chỉ lấy các khẳng định SAI mà vế phải rút gọn được (về $\overrightarrow{VU}$, hai lần một vectơ, ...) để lời
    giải chỉ rõ vì sao sai."""
    ten = list(random.choice(_B8_BO_DIEM))
    U, V, W = random.sample(ten, 3)
    envs = _b5_env_diem(ten)
    trai = _b5_vt(U, V)
    vts = [(X, Y) for X in ten for Y in ten if X != Y and {X, Y} != {U, V}]
    dung, sai = [], []
    for a in vts:
        for b in vts:
            for phep in "+-":
                if a == b or (phep == "+" and a == (b[1], b[0])):
                    continue
                x, y = _b5_vt(*a), _b5_vt(*b)
                ve = _b5_cong(x, y) if phep == "+" else _b5_tru(x, y)
                kd = (r"$%s = %s$" % (trai.tex, ve.tex), ve, a)
                if not _b5_bang(trai, ve, envs):
                    gon = _b5_rut_diem(ve, envs, _b5_cap_trong(ve), ten)
                    if gon != ve.tex:
                        sai.append(kd + (gon,))
                elif loai == "tong" and phep == "+":
                    dung.append(kd)
                elif loai == "hieu" and phep == "-" and a[0] == b[0]:
                    dung.append(kd)
    dap = random.choice(dung)
    random.shuffle(sai)
    # hai nhiễu rút gọn về một vectơ (thường là vectơ đối $\overrightarrow{VU}$, viết dưới hai dạng khác nhau) và một
    # nhiễu dạng hai lần một vectơ (trừ hai vectơ đối nhau)
    mot = [x for x in sai if not x[3].startswith("2")]
    hai = [x for x in sai if x[3].startswith("2")]
    nhieu = mot[:2] + hai[:1]
    for x in sai:
        if len(nhieu) < 3 and x not in nhieu:
            nhieu.append(x)
    ve = dap[1]
    a = dap[2]
    if loai == "tong":
        if a[0] == U:
            ly = (r"By the three-point rule: $%s = %s$, which holds for \emph{every} position of $%s$, $%s$, $%s$."
                  % (ve.tex, trai.tex, U, V, W))
        else:
            ly = (r"By the three-point rule: $%s + %s = %s$; vector addition is commutative, so $%s = %s$, "
                  r"which holds for \emph{every} position of $%s$, $%s$, $%s$."
                  % (_vt(U, W), _vt(W, V), trai.tex, ve.tex, trai.tex, U, V, W))
    else:
        ly = (r"By the subtraction rule (two vectors with the common initial point $%s$): $%s = %s$, which holds for \emph{every} position of "
              r"$%s$, $%s$, $%s$." % (a[0], ve.tex, trai.tex, U, V, W))
    ly += (r"\\ The other statements are false because: "
           + "; ".join(r"$%s = %s \ne %s$" % (n[1].tex, n[3], trai.tex) for n in nhieu) + ".")
    debai = (r"Given three distinct arbitrary points $%s$, $%s$, $%s$. Which of the following statements is always true?"
             % tuple(sorted(ten)))
    return debai, dap[0], [n[0] for n in nhieu], ly


def L10_C4_B8_TH040_MC_A_02(socau, dang=1):
    r"""Tổng hai vectơ theo quy tắc ba điểm: cho ba điểm phân biệt bất kì, chọn khẳng định luôn đúng
    $\overrightarrow{UV} = \overrightarrow{UW} + \overrightarrow{WV}$ (nhiễu trộn tổng, hiệu, đổi chiều). Theo câu mẫu
    cô Lan gửi. Chân trị kiểm bằng ba bộ toạ độ ngẫu nhiên.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, nhieu, giai = _b8_ba_diem("tong")
        cau += MC_SA_answer_text(debai, dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C4_B8_TH041_MC_A_02(socau, dang=1):
    r"""Hiệu hai vectơ, quy tắc trừ: cho ba điểm phân biệt bất kì, chọn khẳng định luôn đúng
    $\overrightarrow{UV} = \overrightarrow{WV} - \overrightarrow{WU}$ (nhiễu trộn tổng, hiệu, đổi chiều). Theo câu mẫu
    cô Lan gửi. Chân trị kiểm bằng ba bộ toạ độ ngẫu nhiên.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, nhieu, giai = _b8_ba_diem("hieu")
        cau += MC_SA_answer_text(debai, dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C4_B8_TH040_MC_B_02(socau, dang=1):
    r"""Tổng hai vectơ theo quy tắc hình bình hành tại một đỉnh ngẫu nhiên: các phương án cùng vế phải là vectơ
    đường chéo $\overrightarrow{XT}$, khác vế trái (cạnh ở đỉnh khác, hai vectơ đối nhau, ra vectơ ngược hướng).
    Theo câu mẫu cô Lan gửi. Chân trị kiểm bằng ba hình bình hành ngẫu nhiên.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        ten = list(random.choice(["ABCD", "MNPQ", "EFGH"]))
        envs = []
        for _k in range(3):
            E = {t: complex(random.uniform(-9, 9), random.uniform(-9, 9)) for t in ten[:2] + ten[3:]}
            E[ten[2]] = E[ten[1]] + E[ten[3]] - E[ten[0]]
            envs.append(E)
        k = random.randrange(4)
        X, U, T, W = (ten[(k + i) % 4] for i in range(4))
        phai = _b5_vt(X, T)
        canh = [(ten[i], ten[(i + 1) % 4]) for i in range(4)]
        canh += [(q, p) for p, q in canh]
        dung = [r"$%s + %s = %s$" % (_vt(X, U), _vt(X, W), phai.tex), r"$%s + %s = %s$" % (_vt(X, W), _vt(X, U), phai.tex)]
        dap = random.choice(dung)
        nhom = {"nguoc": [], "khong": [], "cheo_khac": [], "khac": []}
        for a in canh:
            for b in canh:
                if a == b or a == (b[1], b[0]):
                    continue
                l = _b5_cong(_b5_vt(*a), _b5_vt(*b))
                if _b5_bang(l, phai, envs):
                    continue
                kd = (r"$%s = %s$" % (l.tex, phai.tex), l)
                if _b5_bang(l, _b5_nhan(-1, phai), envs):
                    nhom["nguoc"].append(kd)
                elif _b5_bang(l, _B5_0, envs):
                    nhom["khong"].append(kd)
                elif any(_b5_bang(l, _b5_vt(p, q), envs) for p, q in ((U, W), (W, U))):
                    nhom["cheo_khac"].append(kd)
                else:
                    nhom["khac"].append(kd)
        nhieu = []
        for g in ("nguoc", "khong", "cheo_khac", "khac"):
            if nhom[g] and len(nhieu) < 3:
                nhieu.append(random.choice(nhom[g]))
        giai = (r"Apply the parallelogram rule at vertex $%s$: the two sides starting from $%s$ are $%s$, $%s$, and the diagonal "
                r"starting from $%s$ is $%s$, so $%s + %s = %s$."
                % (X, X, _vt(X, U), _vt(X, W), X, phai.tex, _vt(X, U), _vt(X, W), phai.tex))
        giai += (r"\\ The other statements are false because: "
                 + "; ".join(r"$%s = %s \ne %s$" % (l.tex, _b5_rut_diem(l, envs, _b5_cap_trong(l), ten), phai.tex)
                             for _, l in nhieu) + ".")
        debai = r"Given a parallelogram $%s$. Which of the following statements is true?" % "".join(ten)
        cau += MC_SA_answer_text(debai, dap, [n[0] for n in nhieu], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH040_C, TH041_C: độ dài vectơ tổng / hiệu trong hình (hình vuông, hình chữ nhật, hình thoi góc 60 độ, tam giác
# đều, tam giác vuông). Toạ độ CHÍNH XÁC bằng sympy; MC theo cạnh a, SA cho số cụ thể.
# ---------------------------------------------------------------------
_A8 = _sp8.Symbol("a", positive=True)


def _b8_tex(x):
    """LaTeX gọn của một độ dài (có thể chứa a): a\\sqrt{2}, \\dfrac{a\\sqrt{3}}{2}, 2a, a + a\\sqrt{2}, ..."""
    x = _sp8.expand(_sp8.radsimp(_sp8.nsimplify(x)))
    if x == 0:
        return "0"
    phan = []
    for t in sorted(_sp8.Add.make_args(x), key=lambda t: (float(t.subs(_A8, 1)) < 0, t.subs(_A8, 1).is_Rational is False,
                                                          str(t))):
        c, con = t.as_coeff_Mul()
        c = _sp8.Rational(c)
        bac = _sp8.degree(con, _A8) if con.has(_A8) else 0
        can = _sp8.nsimplify(con.subs(_A8, 1))
        than = ""
        if abs(c.p) != 1 or (not bac and can == 1):
            than = str(abs(c.p))
        if bac:
            than += "a" if bac == 1 else "a^%d" % bac
        if can != 1:
            than += r"\sqrt{%s}" % _sp8.nsimplify(can ** 2)
        if c.q != 1:
            than = r"\dfrac{%s}{%d}" % (than, c.q)
        phan.append(("-" if c < 0 else "+", than))
    s = ("-" if phan[0][0] == "-" else "") + phan[0][1]
    for d, t in phan[1:]:
        s += " %s %s" % (d, t)
    return s


def _b8_sa(v):
    """Đáp số SA (<= 4 kí tự): số nguyên giữ nguyên; không thì làm tròn hàng phần trăm (< 10) hoặc hàng phần mười.
    Làm tròn từ giá trị CHÍNH XÁC (sympy, 40 chữ số). -> (chuỗi, 'hàng phần trăm' / 'hàng phần mười' / None)."""
    v = _sp8.nsimplify(v)
    if v.is_Integer:
        return str(int(v)), None
    x = _Dec8(str(v.evalf(40)))
    muc, q = ("nearest hundredth", "0.01") if x < 10 else ("nearest tenth", "0.1")
    t = str(x.quantize(_Dec8(q), rounding=_HU8))
    t = t.rstrip("0").rstrip(".").replace(".", DAU_THAP_PHAN)
    return t, muc


def _b8_ten_moi(da, so=2):
    return [t for t in "MNPQTKHEFGIJ" if t not in da][:so]


def _b8_hinh(kieu, so):
    """Hình cho câu độ dài. so=False: theo cạnh a (MC); so=True: số cụ thể (SA).
    Trả về dict: kieu, dinh (tên đỉnh), O (tên tâm hoặc None), P (toạ độ sympy), L ({frozenset: (độ dài, lí do)}),
    mo(co_O) (câu dẫn)."""
    r3 = _sp8.sqrt(3)
    H = dict(kieu=kieu, O=None)
    if kieu in ("vuong", "hcn", "thoi"):
        ten = random.choice(["ABCD", "MNPQ", "EFGH"])
        A, B, C, D = ten
        if kieu == "vuong":
            p = _A8 if not so else random.randint(2, 9)
            q = p
            P = {A: (0, 0), B: (p, 0), C: (p, p), D: (0, p)}
            mo = r"Given a square $%s$ with side $%s$" % (ten, _b8_tex(p))
        elif kieu == "hcn":
            if not so:
                p, q = random.choice([(_A8, 2 * _A8), (2 * _A8, _A8), (_A8, _A8 * r3), (_A8 * r3, _A8), (3 * _A8, 4 * _A8),
                                      (4 * _A8, 3 * _A8)])
            else:
                p, q = random.choice([(3, 4), (4, 3), (6, 8), (8, 6), (5, 12)] + [tuple(random.sample(range(2, 10), 2))] * 3)
            P = {A: (0, 0), B: (p, 0), C: (p, q), D: (0, q)}
            mo = r"Given a rectangle $%s$ with $%s = %s$, $%s = %s$" % (ten, A + B, _b8_tex(p), A + D, _b8_tex(q))
        else:
            p = _A8 if not so else random.randint(2, 9)
            q = p
            P = {A: (0, 0), B: (p, 0), D: (p / _sp8.Integer(2), p * r3 / 2)}
            P[C] = (P[B][0] + P[D][0], P[B][1] + P[D][1])
            mo = r"Given a rhombus $%s$ with side $%s$ and $\widehat{%s} = 60^\circ$" % (ten, _b8_tex(p), B + A + D)
        O = "O" if "O" not in ten else "I"
        P[O] = ((P[A][0] + P[C][0]) / 2, (P[A][1] + P[C][1]) / 2)
        H.update(dinh=list(ten), O=O, P=P,
                 mo=lambda co_O, mo=mo, O=O: mo + ((r" whose two diagonals intersect at $%s$." % O) if co_O else "."))
        L = {}
        for X, Y, d in ((A, B, p), (B, C, q), (C, D, p), (D, A, q)):
            L[frozenset((X, Y))] = (d, None)
        if kieu in ("vuong", "hcn"):
            cheo = _sp8.sqrt(p ** 2 + q ** 2)
            for X, Y, Z in ((A, B, C), (B, C, D)):
                L[frozenset((X, Z))] = (cheo, r"$%s = \sqrt{%s^2 + %s^2} = \sqrt{%s + %s} = %s$ (Pythagorean theorem in "
                                               r"the triangle $%s$ right-angled at $%s$)"
                                        % (X + Z, X + Y, Y + Z, _b8_tex(_sp8.expand(L[frozenset((X, Y))][0] ** 2)),
                                           _b8_tex(_sp8.expand(L[frozenset((Y, Z))][0] ** 2)), _b8_tex(cheo), X + Y + Z, Y))
            for X in ten:
                L[frozenset((O, X))] = (cheo / 2, r"$%s$ is the midpoint of both diagonals, so $%s = \dfrac{1}{2}%s = %s$"
                                        % (O, O + X, A + C if X in (A, C) else B + D, _b8_tex(cheo / 2)))
        else:
            L[frozenset((B, D))] = (p, r"the triangle $%s$ has $%s = %s$ and $\widehat{%s} = 60^\circ$, so it is equilateral, "
                                       r"$%s = %s$" % (A + B + D, A + B, A + D, B + A + D, B + D, _b8_tex(p)))
            L[frozenset((A, C))] = (p * r3, r"$%s$ is the midpoint of $%s$ and $%s$ is perpendicular to $%s$, so $%s = 2%s = "
                                            r"2\sqrt{%s^2 - %s^2} = 2\sqrt{%s - %s} = %s$"
                                    % (O, A + C, A + C, B + D, A + C, A + O, A + B, B + O, _b8_tex(p ** 2),
                                       _b8_tex(p ** 2 / 4), _b8_tex(p * r3)))
            for X in (B, D):
                L[frozenset((O, X))] = (p / 2, r"$%s = \dfrac{1}{2}%s = %s$" % (O + X, B + D, _b8_tex(p / 2)))
            for X in (A, C):
                L[frozenset((O, X))] = (p * r3 / 2, r"$%s = \dfrac{1}{2}%s = %s$" % (O + X, A + C, _b8_tex(p * r3 / 2)))
        H["L"] = L
        return H
    ten = random.choice(["ABC", "MNP", "DEF"])
    A, B, C = ten
    if kieu == "tg_deu":
        p = _A8 if not so else random.randint(2, 9)
        P = {B: (0, 0), C: (p, 0), A: (p / _sp8.Integer(2), p * r3 / 2)}
        L = {frozenset(c): (p, None) for c in ((A, B), (B, C), (C, A))}
        mo = r"Given an equilateral triangle $%s$ with side $%s$." % (ten, _b8_tex(p))
    else:
        if not so:
            p, q = random.choice([(_A8, _A8 * r3), (_A8 * r3, _A8), (3 * _A8, 4 * _A8), (4 * _A8, 3 * _A8), (_A8, 2 * _A8),
                                  (2 * _A8, _A8)])
        else:
            p, q = random.choice([(6, 8), (8, 6), (3, 4), (5, 12), (12, 5)] + [tuple(random.sample(range(2, 10), 2))] * 3)
        P = {A: (0, 0), B: (p, 0), C: (0, q)}
        bc = _sp8.sqrt(p ** 2 + q ** 2)
        L = {frozenset((A, B)): (p, None), frozenset((A, C)): (q, None),
             frozenset((B, C)): (bc, r"$%s = \sqrt{%s^2 + %s^2} = \sqrt{%s + %s} = %s$ (Pythagorean theorem)"
                                 % (B + C, A + B, A + C, _b8_tex(_sp8.expand(p ** 2)), _b8_tex(_sp8.expand(q ** 2)),
                                    _b8_tex(bc)))}
        mo = r"Given a triangle $%s$ right-angled at $%s$ with $%s = %s$, $%s = %s$." % (ten, A, A + B, _b8_tex(p), A + C, _b8_tex(q))
    H.update(dinh=list(ten), P=P, L=L, mo=lambda co_O, mo=mo: mo, canh=p)
    return H


def _b8_vec(H, X, Y):
    """Vectơ XY bằng số thực (a = 1) - chỉ dùng để so sánh bằng nhau, nhanh hơn sympy."""
    if "Pf" not in H:
        H["Pf"] = {k: (float(_sp8.sympify(x).subs(_A8, 1)), float(_sp8.sympify(y).subs(_A8, 1)))
                   for k, (x, y) in H["P"].items()}
    return (H["Pf"][Y][0] - H["Pf"][X][0], H["Pf"][Y][1] - H["Pf"][X][1])


def _b8_bang_v(u, v):
    return abs(u[0] - v[0]) < 1e-9 and abs(u[1] - v[1]) < 1e-9


def _b8_tim(H, v, diem):
    """Điểm T trong 'diem' với vectơ (Q -> T) = w, v = (Q, w); trả về T hoặc None."""
    Q, w = v
    for T in diem:
        if T != Q and _b8_bang_v(_b8_vec(H, Q, T), w):
            return T
    return None


def _b8_bieu_thuc(H, phep):
    """Liệt kê các biểu thức u + v (phep '+') hoặc u - v ('-') rút được về MỘT đoạn thẳng đã biết độ dài, kèm quy tắc.
    Trả về [(u, v, (X, Y) kết quả, lí do biến đổi, nhóm quy tắc)]."""
    diem = H["dinh"] + ([H["O"]] if H["O"] else [])
    vts = [(X, Y) for X in diem for Y in diem if X != Y]
    ra = []
    for u in vts:
        for v in vts:
            if u == v or u == (v[1], v[0]):
                continue
            P_, Q = u
            R, S = v
            kq, ly, nhom = None, None, None
            if phep == "+":
                if Q == R and P_ != S:
                    kq, nhom = (P_, S), "ba_diem"
                    ly = r"$%s + %s = %s$ (three-point rule)" % (_vt(*u), _vt(*v), _vt(P_, S))
                elif P_ == R:
                    wv = _b8_vec(H, R, S)
                    T = _b8_tim(H, (Q, wv), diem)
                    if T and T != P_:
                        kq, nhom = (P_, T), "hbh"
                        ly = (r"$%s%s%s%s$ is a parallelogram, so $%s + %s = %s$ (parallelogram rule)"
                              % (P_, Q, T, S, _vt(*u), _vt(*v), _vt(P_, T)))
                if kq is None and Q != R and P_ != R:
                    T = _b8_tim(H, (Q, _b8_vec(H, R, S)), diem)
                    if T and T != P_:
                        kq, nhom = (P_, T), "thay"
                        ly = (r"$%s = %s$, so $%s + %s = %s + %s = %s$"
                              % (_vt(*v), _vt(Q, T), _vt(*u), _vt(*v), _vt(*u), _vt(Q, T), _vt(P_, T)))
            else:
                if P_ == R and Q != S:
                    kq, nhom = (S, Q), "tru"
                    ly = r"$%s - %s = %s$ (subtraction rule)" % (_vt(*u), _vt(*v), _vt(S, Q))
                elif Q == S and P_ != R:
                    kq, nhom = (P_, R), "doi"
                    ly = (r"$%s - %s = %s + %s = %s$ (opposite vector, three-point rule)"
                          % (_vt(*u), _vt(*v), _vt(*u), _vt(S, R), _vt(P_, R)))
                elif P_ != R:
                    T = _b8_tim(H, (P_, _b8_vec(H, R, S)), diem)
                    if T and T != Q:
                        kq, nhom = (T, Q), "thay"
                        ly = (r"$%s = %s$, so $%s - %s = %s - %s = %s$ (subtraction rule)"
                              % (_vt(*v), _vt(P_, T), _vt(*u), _vt(*v), _vt(*u), _vt(P_, T), _vt(T, Q)))
            if kq and frozenset(kq) in H["L"]:
                ra.append((u, v, kq, ly, nhom))
    # tứ giác: tổng / hiệu HAI ĐƯỜNG CHÉO (câu mẫu |AC - BD| = 2AB): tách mỗi đường chéo qua một đỉnh để hai vectơ đối
    # nhau triệt tiêu, còn lại hai vectơ cạnh bằng nhau
    if H["kieu"] in ("vuong", "hcn", "thoi"):
        A, B, C, D = H["dinh"]
        for d1 in ((A, C), (C, A)):
            for d2 in ((B, D), (D, B)):
                e2 = d2 if phep == "+" else (d2[1], d2[0])           # u - v = u + (-v)
                xong = False
                for Y in H["dinh"]:
                    for Z in H["dinh"]:
                        if xong or Y in d1 or Z in e2:
                            continue
                        if not _b8_bang_v(_b8_vec(H, Y, d1[1]), _b8_vec(H, e2[1], Z)):
                            continue                              # Y d1[1] và Z e2[1] phải đối nhau
                        w1, w2 = (d1[0], Y), (e2[0], Z)
                        if not _b8_bang_v(_b8_vec(H, *w1), _b8_vec(H, *w2)):
                            continue
                        bt_goc = r"%s %s %s" % (_vt(*d1), phep, _vt(*d2))
                        ly = r"We have $%s = " % bt_goc
                        if phep == "-":
                            ly += r"%s + %s = " % (_vt(*d1), _vt(*e2))
                        ly += (r"\left(%s + %s\right) + \left(%s + %s\right) = %s + %s$ (since $%s + %s = \overrightarrow{0}$). "
                               r"The two vectors $%s$, $%s$ are equal (opposite sides of a parallelogram), so "
                               r"$\left|%s + %s\right| = 2%s$"
                               % (_vt(d1[0], Y), _vt(Y, d1[1]), _vt(e2[0], Z), _vt(Z, e2[1]), _vt(*w1), _vt(*w2),
                                  _vt(Y, d1[1]), _vt(Z, e2[1]), _vt(*w1), _vt(*w2), _vt(*w1), _vt(*w2),
                                  w1[0] + w1[1]))
                        dd, ly_dd = H["L"][frozenset(w1)]
                        ly = (ly[:-1] + r" = %s$" % _b8_tex(2 * dd)) if ly_dd is None else (ly + r", where %s" % ly_dd)
                        ra.append((d1, d2, None, ly, ("hai_cheo", 2 * dd)))
                        xong = True
    # tam giác: tổng hai cạnh chung đỉnh (dựng hình bình hành ngoài hình)
    if phep == "+" and H["kieu"] in ("tg_deu", "tg_vuong"):
        A, B, C = H["dinh"]
        goc = [A, B, C] if H["kieu"] == "tg_deu" else [A]
        for X in goc:
            Y, Z = [t for t in H["dinh"] if t != X]
            if random.random() < 0.5:
                Y, Z = Z, Y
            M, T = _b8_ten_moi(H["dinh"])
            if H["kieu"] == "tg_deu":
                d = H["canh"] * _sp8.sqrt(3)
                ly = (r"Let $%s$ be the midpoint of $%s$ and construct the parallelogram $%s%s%s%s$; then $%s + %s = %s$ (parallelogram "
                      r"rule) and $%s$ is the midpoint of $%s$. An equilateral triangle with side $%s$ has median "
                      r"$%s = %s$, so $%s = 2%s = %s$"
                      % (M, Y + Z, X, Y, T, Z, _vt(X, Y), _vt(X, Z), _vt(X, T), M, X + T, _b8_tex(H["canh"]), X + M,
                         _b8_tex(H["canh"] * _sp8.sqrt(3) / 2), X + T, X + M, _b8_tex(d)))
            else:
                d = H["L"][frozenset((B, C))][0]
                ly = (r"Construct the rectangle $%s%s%s%s$; then $%s + %s = %s$ (parallelogram rule) and $%s = %s$ (the two "
                      r"diagonals of a rectangle are equal). Moreover, %s"
                      % (X, Y, T, Z, _vt(X, Y), _vt(X, Z), _vt(X, T), X + T, B + C, H["L"][frozenset((B, C))][1]))
            ra.append(((X, Y), (X, Z), None, ly, ("tg", d)))
    return ra


def _b8_do_dai(phep, so):
    """Một câu độ dài |u + v| hoặc |u - v|. -> (debai_than, bieu thuc tex, do dai dung, nhieu (do dai), giai)."""
    kieu = _c4_uu_tien("b8_do_dai", ["vuong", "hcn", "thoi", "tg_deu", "tg_vuong"])[0]
    _c4_danh_dau("b8_do_dai", [kieu])
    H = _b8_hinh(kieu, so)
    ds = _b8_bieu_thuc(H, phep)
    nhom = {}
    for x in ds:
        k = x[4][0] if isinstance(x[4], tuple) else x[4]
        nhom.setdefault(k, []).append(x)
    # ưu tiên quy tắc hình bình hành / tam giác (như câu mẫu), rồi các quy tắc khác
    uu = [g for g in nhom if g != "ba_diem"]
    k = random.choice(uu if uu and random.random() < 0.8 else list(nhom))
    # ưu tiên kết quả là đoạn phải tính (đường chéo, nửa đường chéo...) hơn là cạnh đã cho
    kho = [x for x in nhom[k] if not x[2] or H["L"][frozenset(x[2])][1]]
    u, v, kq, ly, nh = random.choice(kho if kho and random.random() < 0.7 else nhom[k])
    if isinstance(nh, tuple):
        d, ly_dd = nh[1], None
    else:
        d, ly_dd = H["L"][frozenset(kq)]
    co_O = H["O"] is not None and H["O"] in u + v
    bt = r"%s %s %s" % (_vt(*u), phep, _vt(*v))
    giai = (ly if not kq else r"Note that %s" % ly) + "."
    if ly_dd:
        giai += r"\\ Moreover, %s." % ly_dd
    giai += r"\\ Therefore $\left|%s\right| = %s$." % (bt, _b8_tex(d))
    du, dv = H["L"][frozenset(u)][0], H["L"][frozenset(v)][0]
    hieu_dd = du - dv if float(_sp8.sympify(du - dv).subs(_A8, 1)) >= 0 else dv - du
    ung = [du + dv, hieu_dd, 2 * d, d / 2] + [x[0] for x in H["L"].values()] + \
          [d * _sp8.sqrt(2), d * _sp8.sqrt(3), d * _sp8.sqrt(3) / 2, d * _sp8.sqrt(2) / 2, 3 * d]
    so_f = lambda x: float(_sp8.sympify(x).subs(_A8, 1))
    nhieu, da = [], [so_f(d)]
    for i, x in enumerate(ung):
        f = so_f(x)
        if f > 1e-9 and all(abs(f - y) > 1e-9 for y in da):
            x = _sp8.radsimp(_sp8.sympify(x))
            if i < 2 or len(_sp8.Add.make_args(_sp8.expand(x))) == 1:     # |u| + |v|, |u| - |v| được hai số hạng
                nhieu.append(x)
                da.append(f)
    return H["mo"](co_O), bt, d, nhieu, giai


def _b8_mc_do_dai(phep, socau, dang):
    cau = ""
    for _ in range(socau):
        mo, bt, d, nhieu, giai = _b8_do_dai(phep, False)
        debai = mo + r" The length of vector $%s$ equals" % bt
        # nhiễu thứ nhất luôn là lỗi hay gặp |u| + |v| (nếu khác đáp số), hai nhiễu còn lại chọn ngẫu nhiên
        chon = nhieu[:1] + random.sample(nhieu[1:], 2)
        cau += MC_SA_answer_text(debai, "$%s$" % _b8_tex(d), ["$%s$" % _b8_tex(x) for x in chon], giai, 0, 0, dang)
    return cau


def _b8_sa_do_dai(phep, socau, dang):
    cau = ""
    for _ in range(socau):
        mo, bt, d, nhieu, giai = _b8_do_dai(phep, True)
        dap, muc = _b8_sa(d)
        debai = mo + r" Compute $\left|%s\right|$%s." % (bt, (r" (round the result to the %s)" % muc) if muc else "")
        if muc:
            giai += r" Hence $\left|%s\right| \approx %s$." % (bt, dap)
        ung = [_b8_sa(x)[0] for x in nhieu]
        cau += MC_SA_answer_const(debai, dap, [x for x in ung if x != dap] + [str(i) for i in range(1, 20)], giai, 0, 0,
                                  dang)
    return cau


def L10_C4_B8_TH040_MC_C_01(socau, dang=1):
    r"""Độ dài vectơ tổng trong hình (hình vuông, hình chữ nhật, hình thoi góc $60^\circ$, tam giác đều, tam giác vuông):
    đưa tổng về một vectơ (quy tắc ba điểm, hình bình hành, thay vectơ bằng nhau) rồi tính độ dài theo $a$. Nhiễu:
    $\left|\vec u\right| + \left|\vec v\right|$, hiệu hai độ dài, các đoạn khác trong hình. Theo câu mẫu cô Lan gửi.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8_mc_do_dai("+", socau, dang)


def L10_C4_B8_TH040_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với TH040_MC_C: độ dài vectơ tổng trong hình với số đo cụ thể; đáp số nguyên hoặc làm
    tròn (<= 4 kí tự).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8_sa_do_dai("+", socau, dang)


def L10_C4_B8_TH041_MC_C_01(socau, dang=1):
    r"""Độ dài vectơ hiệu trong hình (hình vuông, hình chữ nhật, hình thoi góc $60^\circ$, tam giác đều, tam giác vuông):
    đưa hiệu về một vectơ (quy tắc trừ, vectơ đối, thay vectơ bằng nhau) rồi tính độ dài theo $a$.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8_mc_do_dai("-", socau, dang)


def L10_C4_B8_TH041_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với TH041_MC_C: độ dài vectơ hiệu trong hình với số đo cụ thể; đáp số nguyên hoặc làm
    tròn (<= 4 kí tự).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8_sa_do_dai("-", socau, dang)


# ---------------------------------------------------------------------
# B11_VD060_A_02: hợp lực của hai lực với góc bất kì (0 độ đến 180 độ), hoặc lực thứ ba giữ vật cân bằng.
# ---------------------------------------------------------------------
_B8_COS = {30: (0, 1, 3), 45: (0, 1, 2), 60: (_Fr5(1, 2), 0, 1), 90: (0, 0, 1), 120: (_Fr5(-1, 2), 0, 1),
           135: (0, -1, 2), 150: (0, -1, 3)}         # cos = r + s*sqrt(m)/2


def _b8_luc_so(v):
    """Độ lớn lực (sympy) -> (chuỗi, có làm tròn): số nguyên giữ nguyên, không thì làm tròn hàng phần mười."""
    v = _sp8.nsimplify(v)
    if v.is_Integer:
        return str(int(v)), False
    t = str(_Dec8(str(v.evalf(40))).quantize(_Dec8("0.1"), rounding=_HU8))
    return t.rstrip("0").rstrip(".").replace(".", DAU_THAP_PHAN), True


def _b8_luc_sinh():
    can_bang = random.random() < 0.5
    while True:
        g = random.choice([0, 180, 90, 60, 120, 45, 135, 30, 150, 60, 120, 135])
        p = random.randint(2, 40)
        q = p if random.random() < 0.3 else random.randint(2, 40)
        if can_bang and (g == 180 and p == q):
            continue
        if not can_bang and g == 0 and random.random() < 0.7:
            continue
        break
    cos = _sp8.cos(_sp8.pi * g / 180)
    R = _sp8.sqrt(_sp8.nsimplify(p * p + q * q + 2 * p * q * cos))
    return can_bang, g, p, q, R


def _b8_luc_cau(dang):
    can_bang, g, p, q, R = _b8_luc_sinh()
    F1, F2, F3 = (r"\overrightarrow{F_%d}" % i for i in (1, 2, 3))
    do = lambda F: r"\left|%s\right|" % F
    if p == q:
        so = r"$%s = %s = %d\ \text{N}$" % (do(F1), do(F2), p)
    else:
        so = r"$%s = %d\ \text{N}$, $%s = %d\ \text{N}$" % (do(F1), p, do(F2), q)
    if g == 0:
        quan_he = r"the two forces $%s$, $%s$ are parallel and point in the same direction" % (F1, F2)
    elif g == 180:
        quan_he = r"the two forces $%s$, $%s$ are parallel and point in opposite directions" % (F1, F2)
    else:
        quan_he = r"the angle between the two vectors $%s$, $%s$ is $%d^\circ$" % (F1, F2, g)
    dap, tron = _b8_luc_so(R)
    lam_tron = r" (round the result to the nearest tenth)" if tron else ""
    if can_bang:
        debai = (r"An object is at rest under the action of three forces $%s$, $%s$, $%s$, where %s and %s. Find the magnitude of the force "
                 r"$%s$%s." % (F1, F2, F3, so, quan_he, F3, lam_tron))
        giai = (r"The object is at rest (in equilibrium), so $%s + %s + %s = \overrightarrow{0}$, hence $%s = -\left(%s + %s\right)$, "
                r"and therefore $%s = \left|%s + %s\right|$.\\ " % (F1, F2, F3, F3, F1, F2, do(F3), F1, F2))
        hoi = do(F3)
    else:
        debai = (r"Two forces $%s$, $%s$ act on the same object, where %s and %s. Find the magnitude of the resultant force "
                 r"$%s + %s$%s." % (F1, F2, so, quan_he, F1, F2, lam_tron))
        giai, hoi = "", r"\left|%s + %s\right|" % (F1, F2)
    tong = r"\left|%s + %s\right|" % (F1, F2)
    if g == 0:
        giai += r"The two forces point in the same direction, so $%s = %d + %d = %d\ \text{N}$." % (tong, p, q, p + q)
    elif g == 180:
        giai += (r"The two forces point in opposite directions, so $%s = \left|%d - %d\right| = %d\ \text{N}$%s." % (tong, p, q, abs(p - q),
                 r" (the two forces are opposite, the resultant force is $\overrightarrow{0}$)" if p == q else ""))
    else:
        R2 = _sp8.nsimplify(R ** 2)
        giai += (r"Let $\overrightarrow{OA} = %s$, $\overrightarrow{OB} = %s$ and construct the parallelogram $OACB$; then "
                 r"$%s + %s = \overrightarrow{OC}$ (parallelogram rule). The triangle $OAC$ has $OA = %d$, $AC = OB = %d$, "
                 r"$\widehat{OAC} = 180^\circ - %d^\circ = %d^\circ$. By the law of cosines:\\ "
                 r"$OC^2 = OA^2 + AC^2 - 2\cdot OA\cdot AC\cdot\cos\widehat{OAC} = %d^2 + %d^2 - 2\cdot %d\cdot %d\cdot\cos %d^\circ "
                 r"= %s$.\\ " % (F1, F2, F1, F2, p, q, g, 180 - g, p, q, p, q, 180 - g, _b8_tex(R2)))
        if tron:
            giai += r"Hence $%s = OC = \sqrt{%s} \approx %s\ \text{N}$." % (tong, _b8_tex(R2), dap)
        else:
            giai += r"Hence $%s = OC = \sqrt{%s} = %s\ \text{N}$." % (tong, _b8_tex(R2), dap)
    if can_bang:
        giai += r"\\ Hence $%s %s %s\ \text{N}$." % (hoi, r"\approx" if tron else "=", dap)
    cos = _sp8.cos(_sp8.pi * g / 180)
    ung = [p + q, abs(p - q), _sp8.sqrt(_sp8.nsimplify(p * p + q * q - 2 * p * q * cos)), _sp8.sqrt(p * p + q * q)]
    ds = []
    for x in ung:
        t = _b8_luc_so(x)[0]
        if t != dap and t not in ds and (len(t) <= 4 or dang == 1):
            ds.append(t)
    return debai, dap, ds, giai


def L10_C4_B11_VD060_MC_A_02(socau, dang=1):
    r"""Tổng hợp lực: hai lực có góc bất kì ($0^\circ$, $30^\circ$, ..., $180^\circ$), hỏi độ lớn hợp lực hoặc lực thứ ba
    giữ vật đứng yên (cân bằng). Quy tắc hình bình hành + định lí côsin; kết quả nguyên hoặc làm tròn hàng phần mười.
    Nhiễu: cộng độ lớn, hiệu độ lớn, nhầm dấu côsin, bỏ góc. Theo câu mẫu cô Lan gửi (hai lực ngược chiều cùng độ
    lớn; ba lực, $F_1 = F_2 = 25$ N, góc $135^\circ$).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, ds, giai = _b8_luc_cau(dang)
        d = float(dap.replace(",", "."))
        du = [_xx4(d + k, 1) for k in (1, -1, 2, -2, 3, 5) if d + k > 0]
        nhieu = [r"$%s\ \text{N}$" % t for t in (ds + [x for x in du if x != dap and x not in ds])[:3]]
        cau += MC_SA_answer_text(debai, r"$%s\ \text{N}$" % dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C4_B11_VD060_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với VD060_MC_A: như VD060_MC_A_02, đáp số (đơn vị N) nguyên hoặc làm tròn hàng phần
    mười, <= 4 kí tự.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, ds, giai = _b8_luc_cau(dang)
        debai = debai[:-1] + r" (unit: N)."
        d = float(dap.replace(",", "."))
        du = [_xx4(d + k, 1) for k in (1, -1, 2, -2, 3, 5) if d + k > 0]
        cau += MC_SA_answer_const(debai, dap, ds + du, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# B11_VD060_B (vận tốc thực = tổng hai vectơ vận tốc) và VD060_C (hợp lực trong bối cảnh thực tế). Bài toán thực tế
# tách riêng chữ C với VD060_A (không thực tế) theo ý cô Lan 16/10/2026.
# ---------------------------------------------------------------------
_B8_MUC = {0: "nearest whole number", 1: "nearest tenth", 2: "nearest hundredth"}


def _b8_tron(v, so_le):
    """Làm tròn giá trị CHÍNH XÁC (sympy) đến so_le chữ số thập phân -> chuỗi dấu phẩy (bỏ 0 thừa)."""
    v = _sp8.sympify(v)
    if v.is_Rational and (v * 10 ** so_le).is_Integer:
        t = str(_Dec8(str(_sp8.N(v, 40))).quantize(_Dec8(1).scaleb(-so_le), rounding=_HU8))
    else:
        t = str(_Dec8(str(v.evalf(40))).quantize(_Dec8(1).scaleb(-so_le), rounding=_HU8))
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t.replace(".", DAU_THAP_PHAN)


def _b8_can_tron(v, so_le):
    """True nếu giá trị chính xác v KHÔNG viết được đúng với so_le chữ số thập phân (phải làm tròn)."""
    v = _sp8.sympify(v)
    return not (v.is_Rational and (v * 10 ** so_le).is_Integer)


def _b8_so(x):
    """Số liệu trong đề (sympy Rational) -> chuỗi dấu phẩy."""
    x = _sp8.sympify(x)
    return str(x) if x.is_Integer else _xx4(float(x), 2)


def _b8_tong_hai(p, q, g):
    """Độ lớn tổng hai vectơ độ lớn p, q, góc g độ (chính xác, sympy)."""
    return _sp8.sqrt(_sp8.sympify(p ** 2 + q ** 2 + 2 * p * q * _sp8.cos(_sp8.pi * g / 180)))


def _b8_giai_tong(u, w, p, q, g, dv, dap, tron):
    """Lời giải |u + w| với |u| = p, |w| = q, góc g: cùng hướng / vuông góc / định lí côsin."""
    tong = r"\left|%s + %s\right|" % (u, w)
    if g == 90:
        gi = (r"Since $%s \perp %s$, the parallelogram constructed on these two vectors is a rectangle, so "
              r"$%s = \sqrt{%s^2 + %s^2} = \sqrt{%s}" % (u, w, tong, _b8_so(p), _b8_so(q), _b8_so(p * p + q * q)))
    else:
        R2 = _sp8.sympify(p ** 2 + q ** 2 + 2 * p * q * _sp8.cos(_sp8.pi * g / 180))
        gt = _b8_tex(R2) if R2.is_Rational or g in (30, 45, 60, 120, 135, 150) else r"\approx %s" % _b8_tron(R2, 2)
        gi = (r"Let $\overrightarrow{OA} = %s$, $\overrightarrow{OB} = %s$ and construct the parallelogram $OACB$; then "
              r"$%s + %s = \overrightarrow{OC}$ (parallelogram rule). The triangle $OAC$ has $OA = %s$, $AC = OB = %s$, "
              r"$\widehat{OAC} = 180^\circ - %d^\circ = %d^\circ$. By the law of cosines:\\ "
              r"$OC^2 = %s^2 + %s^2 - 2\cdot %s\cdot %s\cdot\cos %d^\circ %s%s$.\\ $%s = OC"
              % (u, w, u, w, _b8_so(p), _b8_so(q), g, 180 - g, _b8_so(p), _b8_so(q), _b8_so(p), _b8_so(q), 180 - g,
                 "" if gt.startswith(r"\approx") else "= ", gt, tong))
    return gi + (r" \approx %s$ (%s)." % (dap, dv) if tron else r" = %s$ (%s)." % (dap, dv))


def _b8_nhieu_tong(p, q, g, so_le, dap, them=()):
    """Nhiễu: cộng độ lớn, hiệu độ lớn, nhầm dấu côsin, bỏ góc (định lí Pythagore), rồi số lân cận."""
    cos = _sp8.cos(_sp8.pi * g / 180)
    ung = [p + q, abs(p - q), _sp8.sqrt(_sp8.sympify(p * p + q * q - 2 * p * q * cos)), _sp8.sqrt(p * p + q * q)]
    ung = [x * k for x in ung for k in ([1] + list(them))]
    ds = []
    for x in ung:
        t = _b8_tron(x, so_le)
        if t != dap and t not in ds and float(t.replace(",", ".")) > 0:
            ds.append(t)
    d = float(dap.replace(",", "."))
    buoc = 10 ** (-so_le) * random.choice([1, 2, 3])
    for k in (1, -1, 2, -2, 3, 5):
        t = _b8_tron(_sp8.sympify(round(d + k * buoc, so_le)), so_le)
        if t != dap and t not in ds and d + k * buoc > 0:
            ds.append(t)
    return ds


def _b8_van_toc():
    """Một câu vận tốc thực. -> (debai không có câu hỏi làm tròn, câu hỏi, đáp số, độ chính xác, nhiễu, lời giải)."""
    bc = _c4_uu_tien("b8_van_toc", ["thuyen_qua_song", "nguoi_boi_qua_song", "flycam_gap_gio"])[0]
    _c4_danh_dau("b8_van_toc", [bc])
    v1, v2 = r"\overrightarrow{v_1}", r"\overrightarrow{v_2}"
    hoi_qd = False
    if bc == "thuyen_qua_song":
        p, q = random.randint(10, 40), random.randint(2, 8)
        g = random.choice([90, 90, 90, random.choice([60, 70, 75, 80, 100, 105, 110, 120])])
        if g == 90:
            huong = r"its bow always points perpendicular to the bank"
        elif g < 90:
            huong = r"its bow always points obliquely downstream, making an angle of $%d^\circ$ with the direction of the current" % g
        else:
            huong = r"its bow always points obliquely upstream, making an angle of $%d^\circ$ with the direction of the current" % g
        de = (r"A motorboat crosses a straight section of a river; %s. The velocity of the boat relative to the water has magnitude $%d$ "
              r"km/h, and the current flows parallel to the bank with speed $%d$ km/h." % (huong, p, q))
        dv, so_le = "km/h", 1
        hoi_qd = random.random() < 0.4
        ten = r"the motorboat"
    elif bc == "nguoi_boi_qua_song":
        p = _sp8.Rational(random.choice([10, 12, 13, 14, 15, 16, 18, 20]), 10)
        q = _sp8.Rational(random.choice([4, 5, 6, 7, 8, 9]), 10)
        g = 90
        de = (r"A person swims across a river, always swimming perpendicular to the bank with a velocity (relative to the "
              r"water) of magnitude $%s$ m/s; the current flows parallel to the bank with speed $%s$ m/s." % (_b8_so(p), _b8_so(q)))
        dv, so_le, ten = "m/s", 2, r"the swimmer"
    else:
        p, q = random.randint(8, 20), random.randint(2, 8)
        g, gio = random.choice([(90, "the north"), (90, "the south"), (45, "the northeast"), (135, "the northwest"),
                                (45, "the southeast"), (135, "the southwest")])
        de = (r"A drone flies east with a velocity (relative to the air) of magnitude $%d$ m/s; the wind blows toward "
              r"%s with speed $%d$ m/s." % (p, gio, q))
        dv, so_le, ten = "m/s", 1, r"flycam"
    R = _b8_tong_hai(p, q, g)
    giai = (r"Let $%s$ be the own velocity and $%s$ the velocity of the %s; the actual velocity is $\vec v = %s + %s$, "
            r"the angle between $%s$ and $%s$ is $%d^\circ$.\\ "
            % (v1, v2, "current" if bc != "flycam_gap_gio" else "wind", v1, v2, v1, v2, g))
    if hoi_qd:
        t = random.choice([(15, _sp8.Rational(1, 4)), (20, _sp8.Rational(1, 3)), (30, _sp8.Rational(1, 2)),
                           (45, _sp8.Rational(3, 4)), (90, _sp8.Rational(3, 2))])
        hoi = r"Find the actual distance travelled by the motorboat after $%d$ minutes" % t[0]
        dap = _b8_tron(R * t[1], 1)
        giai += _b8_giai_tong(v1, v2, p, q, g, dv, _b8_tron(R, 3), _b8_can_tron(R, 3))
        giai += (r"\\ The motorboat moves uniformly in a straight line with speed $\left|\vec v\right|$, so after $%d$ minutes $= %s$ hours it travels "
                 r"$s = \left|\vec v\right|\cdot %s \approx %s$ (km)." % (t[0], _b8_tex(t[1]), _b8_tex(t[1]), dap))
        giai = giai if _b8_can_tron(R * t[1], 1) else giai.replace(r"\approx %s$ (km)" % dap, r"= %s$ (km)" % dap)
        nhieu = _b8_nhieu_tong(p * t[1], q * t[1], g, 1, dap)
        return de, hoi, dap, 1, nhieu, giai, "km", _b8_can_tron(R * t[1], 1)
    hoi = r"Find the actual speed of %s" % ten
    dap = _b8_tron(R, so_le)
    giai += _b8_giai_tong(v1, v2, p, q, g, dv, dap, _b8_can_tron(R, so_le))
    return de, hoi, dap, so_le, _b8_nhieu_tong(p, q, g, so_le, dap), giai, dv, _b8_can_tron(R, so_le)


def _b8_cau_thuc_te(sinh, dang, mc):
    cau = ""
    for _ in range(1):
        de, hoi, dap, so_le, nhieu, giai, dv, tron = sinh()
        lam_tron = (r"round the result to the %s" % _B8_MUC[so_le]) if tron else ""
        if mc:
            debai = de + " " + hoi + ((r" (%s)." % lam_tron) if tron else ".")
            fm = lambda t: r"$%s$ %s" % (t, dv)
            return MC_SA_answer_text(debai, fm(dap), [fm(t) for t in nhieu[:3]], giai, 0, 0, dang)
        debai = de + " " + hoi + r" (unit: %s%s)." % (dv, ("; " + lam_tron) if tron else "")
        return MC_SA_answer_const(debai, dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C4_B11_VD060_MC_B_01(socau, dang=1):
    r"""Vận tốc thực = tổng hai vectơ vận tốc (bối cảnh thực tế ngẫu nhiên): ca nô qua sông (mũi vuông góc bờ hoặc chếch
    xuôi/ngược dòng; có câu hỏi quãng đường sau t phút), người bơi qua sông, flycam gặp gió (Bắc/Nam, Đông Bắc...).
    Quy tắc hình bình hành (hình chữ nhật khi vuông góc) + định lí côsin; làm tròn. Theo câu mẫu cô Lan gửi (tàu
    $40$ km/h vuông góc dòng nước $5$ km/h).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return "".join(_b8_cau_thuc_te(_b8_van_toc, dang, True) for _ in range(socau))


def L10_C4_B11_VD060_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với VD060_MC_B: vận tốc thực (hoặc quãng đường thực) khi tổng hợp hai vận tốc;
    đáp số <= 4 kí tự.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return "".join(_b8_cau_thuc_te(_b8_van_toc, dang, False) for _ in range(socau))


def _b8_luc_thuc_te():
    bc = _c4_uu_tien("b8_luc_thuc_te", ["keo_thuyen", "tau_keo_sa_lan", "keo_kien_hang"])[0]
    _c4_danh_dau("b8_luc_thuc_te", [bc])
    F1, F2 = r"\overrightarrow{F_1}", r"\overrightarrow{F_2}"
    g = random.choice([x for x in range(20, 141, 5) if x not in (90,)] + [random.randint(21, 139)])
    deu = random.random() < 0.35
    if bc == "keo_thuyen":
        p, q, dv = random.randint(40, 150), random.randint(40, 150), "N"
        de = (r"Two people standing on the bank pull a boat with two ropes, with forces $%s$, $%s$ of magnitudes "
              r"$%d$ N and $%d$ N respectively; the angle between the two forces is $%d^\circ$." % (F1, F2, p, q, g))
        can, vat = "the water resistance", "the boat"
    elif bc == "tau_keo_sa_lan":
        p, q, dv = random.randint(20, 90), random.randint(20, 90), "kN"
        de = (r"Two tugboats pull a barge with two cables, with forces $%s$, $%s$ of magnitudes $%d$ kN and "
              r"$%d$ kN respectively; the angle between the two cables is $%d^\circ$." % (F1, F2, p, q, g))
        can, vat = "the water resistance", "the barge"
    else:
        p, q, dv = random.randint(50, 200), random.randint(50, 200), "N"
        de = (r"Two workers pull a crate on a horizontal floor with two ropes, with forces $%s$, $%s$ (parallel "
              r"to the floor) of magnitudes $%d$ N and $%d$ N respectively; the angle between the two forces is $%d^\circ$." % (F1, F2, p, q, g))
        can, vat = "the friction force", "the crate"
    R = _b8_tong_hai(p, q, g)
    dap = _b8_tron(R, 0)
    giai = _b8_giai_tong(F1, F2, p, q, g, dv, dap, _b8_can_tron(R, 0))
    if deu:
        de += (r" It is known that %s moves uniformly in a straight line in the direction of the resultant force and %s (opposite to the motion) balances "
               r"the resultant of the two pulling forces." % (vat, can))
        hoi = r"Find the magnitude of %s" % can
        giai = (r"The object moves uniformly in a straight line, so %s $\overrightarrow{F_c}$ balances the resultant force: "
                r"$\overrightarrow{F_c} = -\left(%s + %s\right)$, hence $\left|\overrightarrow{F_c}\right| = "
                r"\left|%s + %s\right|$.\\ " % (can, F1, F2, F1, F2)) + giai
    else:
        hoi = r"Find the magnitude of the resultant of the two pulling forces acting on %s" % vat
        giai = r"The resultant force is $\vec F = %s + %s$.\\ " % (F1, F2) + giai
    return de, hoi, dap, 0, _b8_nhieu_tong(p, q, g, 0, dap), giai, dv, _b8_can_tron(R, 0)


def L10_C4_B11_VD060_MC_C_01(socau, dang=1):
    r"""Hợp lực trong bối cảnh thực tế ngẫu nhiên: hai người kéo thuyền, hai tàu kéo sà lan, hai công nhân kéo kiện hàng;
    góc bất kì (dùng máy tính cầm tay); hỏi hợp lực hoặc lực cản/ma sát khi vật chuyển động thẳng đều; làm tròn hàng đơn
    vị. Theo câu mẫu cô Lan gửi (kéo thuyền $55$ N, $60$ N, góc $50^\circ$). Tách riêng VD060_A (không thực tế).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return "".join(_b8_cau_thuc_te(_b8_luc_thuc_te, dang, True) for _ in range(socau))


def L10_C4_B11_VD060_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với VD060_MC_C: hợp lực (hoặc lực cản) trong bối cảnh thực tế, làm tròn hàng đơn vị.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return "".join(_b8_cau_thuc_te(_b8_luc_thuc_te, dang, False) for _ in range(socau))


# ---------------------------------------------------------------------
# B8_VD040 (LUYỆN TẬP THÊM, ngoài YCCĐ): tập hợp điểm M thoả một đẳng thức độ dài vectơ.
# Cô Lan 16/10/2026: dạng A, _01 ra ĐƯỜNG TRUNG TRỰC (|MP| = |MQ|), _02 ra ĐƯỜNG TRÒN (|MP| = độ dài cố định).
# Cách sinh: đi từ kết quả (MP, MQ, vectơ cố định ZW) rồi "che" bằng các phép biến đổi vectơ của Bài 8: tách theo
# quy tắc ba điểm, thay bằng vectơ bằng nó (cạnh đối hình bình hành, trung điểm), vectơ đối, tính chất trọng tâm
# (GB + GC = AG). Lời giải là các bước ngược lại. Hình: hình bình hành (có thể có tâm O), tam giác có trọng tâm G
# và trung điểm I của một cạnh.
# ---------------------------------------------------------------------
def _b8h_hinh():
    """Hình cho câu tập hợp điểm: dict ten (tên đỉnh), diem (mọi điểm có tên), E (vài bộ toạ độ phức), mo(dung) (câu
    dẫn theo các điểm phụ có dùng), kieu, ly_bang(u, w) (lí do hai vectơ bằng nhau)."""
    if random.random() < 0.5:
        ten = random.choice(["ABCD", "EFGH", "PQRS"])
        A, B, C, D = ten
        envs = []
        for _ in range(3):
            E = {t: complex(random.uniform(-9, 9), random.uniform(-9, 9)) for t in (A, B, D)}
            E[C] = E[B] + E[D] - E[A]
            E["O"] = (E[A] + E[C]) / 2
            envs.append(E)
        phu = {"O": r"whose two diagonals intersect at $O$"}
        trung = {"O": [(A, C), (B, D)]}
        return dict(kieu="hbh", ten=ten, dinh=list(ten), diem=list(ten) + ["O"], E=envs, phu=phu, trung=trung,
                    mo=lambda dung: r"Given a parallelogram $%s$%s." % (ten, (" with " + phu["O"]) if "O" in dung else ""))
    ten = random.choice(["ABC", "DEF", "PQR"])
    A, B, C = ten
    _, Y, Z = random.sample(ten, 3) if False else (None,) + tuple(random.sample([B, C, A], 2))
    envs = []
    for _ in range(3):
        E = {t: complex(random.uniform(-9, 9), random.uniform(-9, 9)) for t in ten}
        E["G"] = (E[A] + E[B] + E[C]) / 3
        E["I"] = (E[Y] + E[Z]) / 2
        envs.append(E)
    phu = {"G": r"the centroid $G$", "I": r"$I$ is the midpoint of the side $%s$" % "".join(sorted(Y + Z))}
    trung = {"I": [(Y, Z)]}

    def mo(dung):
        k = [x for x in ("G", "I") if x in dung]
        if not k:
            return r"Given a triangle $%s$." % ten
        if k[0] == "G":
            return r"Given a triangle $%s$ with %s%s." % (ten, phu["G"], (", " + phu["I"]) if len(k) > 1 else "")
        return r"Given a triangle $%s$, %s." % (ten, phu["I"])
    return dict(kieu="tg", ten=ten, dinh=list(ten), diem=list(ten) + ["G", "I"], E=envs, phu=phu, trung=trung, mo=mo)


def _b8h_v(H, U, V, k=0):
    return H["E"][k][V] - H["E"][k][U]


def _b8h_bang(H, u, w):
    return all(abs(_b8h_v(H, *u, k) - _b8h_v(H, *w, k)) < 1e-9 for k in range(len(H["E"])))


def _b8h_ly_bang(H, u, w):
    """Lí do vectơ u = w (u, w là cặp điểm)."""
    for c, ds in H["trung"].items():
        if c in u + w:
            for X, Y in ds:
                if set(u + w) <= {c, X, Y}:
                    return r"$%s$ is the midpoint of $%s$" % (c, X + Y)
    return r"$%s$ is a parallelogram" % H["ten"]


def _b8h_che(H, u):
    """Che một vectơ u = (U, V) của hình. -> (danh sách hạng tử [(dấu, U, V)], câu giải thích ngược hoặc None)."""
    U, V = u
    lua = []
    bang = [(X, Y) for X in H["diem"] for Y in H["diem"] if X != Y and (X, Y) != u and _b8h_bang(H, (X, Y), u)]
    if bang:
        lua.append("bang")
    if H["kieu"] == "tg" and "G" in u and (set(u) - {"G"}) <= set(H["dinh"]):
        lua += ["trong_tam", "trong_tam"]
    lua.append("doi")
    k = random.choice(lua)
    if k == "bang":
        w = random.choice(bang)
        return [(1,) + w], r"$%s = %s$ (since %s)" % (_vt(*w), _vt(U, V), _b8h_ly_bang(H, w, u))
    if k == "doi":
        return [(-1, V, U)], None
    dinh = [t for t in H["dinh"] if t not in u]                    # hai đỉnh còn lại
    if U == "G":                                                   # GA = BG + CG
        hang = [(1, dinh[0], "G"), (1, dinh[1], "G")]
    else:                                                          # AG = GB + GC
        hang = [(1, "G", dinh[0]), (1, "G", dinh[1])]
    return hang, (r"$%s + %s = %s$ (since $G$ is the centroid, $\overrightarrow{G%s} + \overrightarrow{G%s} + "
                  r"\overrightarrow{G%s} = \overrightarrow{0}$)" % (_vt(*hang[0][1:]), _vt(*hang[1][1:]), _vt(U, V),
                                                                   *H["dinh"]))


def _b8h_tex(hang):
    s = ""
    for i, (d, U, V) in enumerate(hang):
        s += ("" if i == 0 and d > 0 else (" - " if d < 0 else " + ")) + _vt(U, V)
    return s.lstrip()


def _b8h_bieu_thuc(H, dau, cuoi, co_M):
    """Biểu thức che của vectơ dau -> cuoi (đi qua 1-2 điểm trung gian). co_M: dau là 'M' (hạng tử MX giữ nguyên).
    -> (tex, các bước giải thích, tex dạng chuỗi ba điểm)."""
    while True:
        so_buoc = random.choice([1, 2]) if co_M else random.choice([2, 2, 3])
        chuoi = [dau]
        trung_gian = [p for p in H["diem"] if p not in (dau, cuoi)]
        random.shuffle(trung_gian)
        chuoi += trung_gian[:so_buoc - 1] + [cuoi] if not co_M else [trung_gian[0]] + trung_gian[1:so_buoc] + [cuoi]
        hop = list(zip(chuoi, chuoi[1:]))
        hang, buoc, so_che = [], [], 0
        for i, u in enumerate(hop):
            if co_M and i == 0:
                hang.append((1,) + u)
                continue
            h, ly = _b8h_che(H, u) if random.random() < 0.85 else ([(1,) + u], None)
            so_che += h != [(1,) + u]
            hang += h
            if ly:
                buoc.append(ly)
        if so_che >= 1 and len(hang) >= 3 - (0 if co_M else 1) and len(hang) <= 4 and any(h[0] > 0 for h in hang):
            break
    dau_hang = hang[:1] if co_M else []
    con = hang[1:] if co_M else hang
    random.shuffle(con)
    hang = dau_hang + con
    if not co_M and hang[0][0] < 0:
        hang = sorted(hang, key=lambda h: h[0] < 0)
    return _b8h_tex(hang), buoc, " + ".join(_vt(*u) for u in hop), hop


def _b8h_giai(tex, buoc, chuoi, kq):
    gi = r"$%s = %s = %s$." % (tex, chuoi, kq)
    if buoc:
        return r"We have " + "; ".join(buoc) + r". Hence " + gi
    return r"Rewrite the subtracted vectors as opposite vectors and use the three-point rule: " + gi


def _b8_tap_hop(kieu):
    """kieu 'trung_truc' (dạng A_01) hoặc 'duong_tron' (A_02). -> (debai đầu, dk tex, dap, nhieu, giai_a, dap_a, giai_b)."""
    H = _b8h_hinh()
    tt = lambda X, Y: r"the perpendicular bisector of the segment $%s$" % "".join(sorted((X, Y))) if X != Y else None
    tron = lambda T, r: r"the circle with center $%s$ and radius $%s$" % (T, r)
    diem = H["diem"]
    if kieu == "trung_truc":
        while True:
            P, Q = random.sample(diem, 2)
            t1, b1, c1, h1 = _b8h_bieu_thuc(H, "M", P, True)
            t2, b2, c2, h2 = _b8h_bieu_thuc(H, "M", Q, True)
            X1, X2 = h1[0][1], h2[0][1]
            if X1 != X2 and {X1, X2} != {P, Q} and t1 != t2 and (b1 or b2):
                break
        dk = r"\left|%s\right| = \left|%s\right|" % (t1, t2)
        dap = tt(P, Q)
        ung = [tt(X1, X2), tt(P, X2) if X2 != Q else tt(X1, Q), r"the line $%s$" % "".join(sorted((P, Q))),
               r"the circle with diameter $%s$" % "".join(sorted((P, Q)))]
        giai_a = _b8h_giai(t1, b1, c1, _vt("M", P)) + r"\\ " + _b8h_giai(t2, b2, c2, _vt("M", Q))
        dap_a = r"%s = %s,\ %s = %s" % (t1, _vt("M", P), t2, _vt("M", Q))
        giai_b = (r"The condition becomes $\left|%s\right| = \left|%s\right|$, that is $M%s = M%s$: $M$ is equidistant from the two points "
                  r"$%s$, $%s$. Hence the set of points $M$ is %s." % (_vt("M", P), _vt("M", Q), P, Q, P, Q, dap))
        dung = set(t1 + t2)
    else:
        while True:
            P = random.choice(diem)
            Z, W = random.sample(H["dinh"], 2)                    # bán kính là một cạnh / đường chéo của hình
            t1, b1, c1, h1 = _b8h_bieu_thuc(H, "M", P, True)
            X1 = h1[0][1]
            if random.random() < 0.4:                              # |MW - MZ| = ZW (quy tắc trừ)
                t2 = r"%s - %s" % (_vt("M", W), _vt("M", Z))
                g2 = r"$%s = %s$ (subtraction rule)" % (t2, _vt(Z, W))
                ban_kinh_sai = None
            else:
                t2, b2, c2, h2 = _b8h_bieu_thuc(H, Z, W, False)
                g2 = _b8h_giai(t2, b2, c2, _vt(Z, W))[:-1]
                ban_kinh_sai = "".join(h2[0])
            if X1 != P and (b1 or (ban_kinh_sai and b2)):
                break
        r = "".join(sorted(Z + W))
        dk = r"\left|%s\right| = \left|%s\right|" % (t1, t2)
        dap = tron(P, r)
        ung = [tron(X1, r), r"the circle with diameter $%s$" % r, tt(P, X1),
               tron(P, ban_kinh_sai) if ban_kinh_sai and set(ban_kinh_sai) != set(r) else tron(P, r[0] + P)
               if r[0] != P else None]
        giai_a = _b8h_giai(t1, b1, c1, _vt("M", P)) + r"\\ " + g2 + r", so $\left|%s\right| = %s$." % (t2, r)
        dap_a = r"%s = %s,\ \left|%s\right| = %s" % (t1, _vt("M", P), t2, r)
        giai_b = (r"The condition becomes $M%s = %s$ ($%s$ is a fixed length). Hence the set of points $M$ is %s."
                  % (P, r, r, dap))
        dung = set(t1 + t2 + P)
    nhieu = []
    for x in ung:
        if x and x != dap and x not in nhieu:
            nhieu.append(x)
    return H["mo"](dung), dk, dap, nhieu, giai_a, dap_a, giai_b


def _b8_vd040_mc(kieu, socau, dang):
    cau = ""
    for _ in range(socau):
        mo, dk, dap, nhieu, ga, da, gb = _b8_tap_hop(kieu)
        debai = mo + r" The set of points $M$ satisfying $%s$ is" % dk
        cau += MC_SA_answer_text(debai, dap, nhieu[:3], ga + r"\\ " + gb, 0, 0, dang)
    return cau


def L10_C4_B8_VD040_MC_A_01(socau, dang=1):
    r"""Tập hợp điểm $M$ là ĐƯỜNG TRUNG TRỰC: điều kiện $\left|\ldots\right| = \left|\ldots\right|$ mỗi vế rút gọn về
    $\overrightarrow{MP}$, $\overrightarrow{MQ}$ (quy tắc ba điểm, vectơ bằng nhau trong hình bình hành / trung điểm,
    vectơ đối, tính chất trọng tâm). Hình bình hành (có thể có tâm $O$) hoặc tam giác có trọng tâm $G$, trung điểm $I$.
    LUYỆN TẬP THÊM. Theo câu tự luận cô Lan gửi.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach (dang A: _01 trung truc, _02 duong tron); luyen tap them."""
    return _b8_vd040_mc("trung_truc", socau, dang)


def L10_C4_B8_VD040_MC_A_02(socau, dang=1):
    r"""Tập hợp điểm $M$ là ĐƯỜNG TRÒN: vế chứa $M$ rút gọn về $\overrightarrow{MP}$, vế kia là độ dài không đổi (vectơ
    của hình viết dưới dạng phức tạp hoặc $\overrightarrow{MW} - \overrightarrow{MZ}$) -> đường tròn tâm $P$, bán kính
    $ZW$. Tâm, bán kính thay đổi (đỉnh, tâm $O$, trọng tâm $G$, trung điểm $I$).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach (dang A: _01 trung truc, _02 duong tron); luyen tap them."""
    return _b8_vd040_mc("duong_tron", socau, dang)


def L10_C4_B8_VD040_TL_A_01(socau, dong=1):
    r"""Tự luận - cùng Dang với VD040_MC_A: a) rút gọn các vectơ trong điều kiện; b) tìm tập hợp điểm $M$ (đường trung
    trực hoặc đường tròn).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; luyen tap them; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        mo, dk, dap, nhieu, ga, da, gb = _b8_tap_hop(random.choice(["trung_truc", "duong_tron"]))
        hoi_a = r"Simplify the vector expressions in the equality $%s$." % dk
        hoi_b = r"Find the set of points $M$ satisfying $%s$." % dk
        dap_b = r"\text{%s}" % dap.replace("$", "")
        cau += TL_answer_text(mo, [(hoi_a, da, ga), (hoi_b, dap_b, gb)], 0, 0, dong)
    return cau


# =====================================================================
# BÀI 8 MỨC NHẬN BIẾT (cô Lan 17/10/2026: "NB tổng hiệu bài 8 chưa có - nhận biết các khái niệm tổng hiệu vectơ cơ
# bản"; cô duyệt kế hoạch ID). Đơn vị NB040, NB041, NB042 DƯỚI YCCĐ TH của Bộ (không phải ngoài YCCĐ).
#   NB040_MC_A, NB041_MC_A, NB042_MC_A: điền khuyết / gọi tên quy tắc, tính chất (chỉ MC: bản SA vô lý);
#   NB040_MC_B + SA_B, NB041_MC_B + SA_B: chọn / đếm khẳng định đúng về khái niệm.
# Tên điểm, tên vectơ ngẫu nhiên mỗi lần sinh.
# =====================================================================
_B8NB_TEN = list("ABCDEFHIKNPQ")
_B8NB_TU = [("a", "b", "c"), ("u", "v", "w"), ("x", "y", "z")]


def _b8nb_ten():
    X, Y, Z, T = random.sample(_B8NB_TEN, 4)
    a, b, c = (r"\overrightarrow{%s}" % t for t in random.choice(_B8NB_TU))
    return X, Y, Z, T, a, b, c


_B8NB_QT = ["the three-point rule", "the parallelogram rule", "the subtraction rule", "the commutative property of vector addition"]


def _b8nb_dien_tong():
    """Kho điền khuyết về tổng hai vectơ. -> [(câu dẫn, đáp án, [nhiễu], lời giải)]."""
    X, Y, Z, T, a, b, c = _b8nb_ten()
    v = _vt
    return [
        (r"Given two vectors $%s$, $%s$. Take an arbitrary point $%s$ and draw $%s = %s$ and $%s = %s$. Then the vector $%s + %s$ is"
         % (a, b, X, v(X, Y), a, v(Y, Z), b, a, b), "$%s$" % v(X, Z), ["$%s$" % v(Z, X), "$%s$" % v(Y, X), "$%s$" % v(Z, Y)],
         r"By the definition of the sum of two vectors: draw $%s = %s$, $%s = %s$, then $%s + %s = %s$." % (v(X, Y), a, v(Y, Z), b, a, b,
                                                                                    v(X, Z))),
        (r"For any three points $%s$, $%s$, $%s$, the equality $%s + %s = %s$ is called" % (X, Y, Z, v(X, Y), v(Y, Z), v(X, Z)),
         _B8NB_QT[0], _B8NB_QT[1:], r"The equality $%s + %s = %s$ is the three-point rule." % (v(X, Y), v(Y, Z), v(X, Z))),
        (r"Given a parallelogram $%s$. The equality $%s + %s = %s$ is called" % (X + Y + Z + T, v(X, Y), v(X, T), v(X, Z)),
         _B8NB_QT[1], [_B8NB_QT[0], _B8NB_QT[2], _B8NB_QT[3]],
         r"For the parallelogram $%s$: $%s + %s = %s$ is the parallelogram rule." % (X + Y + Z + T, v(X, Y), v(X, T), v(X, Z))),
        (r"Given a parallelogram $%s$. By the parallelogram rule, $%s + %s$ equals" % (X + Y + Z + T, v(X, Y), v(X, T)),
         "$%s$" % v(X, Z), ["$%s$" % v(Y, T), "$%s$" % v(T, Y), "$%s$" % v(Z, X)],
         r"Parallelogram rule: the sum of the two side vectors starting from vertex $%s$ is the diagonal vector starting from $%s$: "
         r"$%s + %s = %s$." % (X, X, v(X, Y), v(X, T), v(X, Z))),
        (r"By the three-point rule, for any three points $%s$, $%s$, $%s$, $%s + %s$ equals" % (X, Y, Z, v(X, Y), v(Y, Z)),
         "$%s$" % v(X, Z), ["$%s$" % v(Z, X), "$%s$" % v(Y, Y), "$%s$" % v(X, Y)],
         r"Three-point rule: $%s + %s = %s$." % (v(X, Y), v(Y, Z), v(X, Z))),
        (r"For every vector $%s$, the sum $%s + \overrightarrow{0}$ equals" % (a, a), "$%s$" % a,
         [r"$\overrightarrow{0}$", "$-%s$" % a, "$%s + %s$" % (a, a)],
         r"Adding the zero vector to any vector gives that vector: $%s + \overrightarrow{0} = %s$." % (a, a)),
        (r"For any point $%s$, the vector $%s$ is" % (X, v(X, X)), r"the zero vector",
         [r"the opposite vector of $%s$" % v(X, Y), r"the vector of length $1$", r"not a vector"],
         r"A vector whose initial and terminal points coincide is the zero vector: $%s = \overrightarrow{0}$." % v(X, X)),
    ]


def _b8nb_dien_hieu():
    X, Y, Z, T, a, b, c = _b8nb_ten()
    v = _vt
    return [
        (r"The opposite vector of the vector $%s$ is" % v(X, Y), "$%s$" % v(Y, X),
         ["$%s$" % v(X, Y), r"$\overrightarrow{0}$", "$-%s$" % v(Y, X)],
         r"The opposite vector of $%s$ is the vector with the same length and opposite direction, that is $%s$: $-%s = %s$." % (v(X, Y), v(Y, X), v(X, Y),
                                                                                        v(Y, X))),
        (r"The opposite vector of the zero vector is", "the zero vector",
         ["does not exist", r"every vector different from $\overrightarrow{0}$", r"the vector of length $1$"],
         r"The opposite vector of $\overrightarrow{0}$ is $\overrightarrow{0}$."),
        (r"Two opposite vectors are two vectors that", "have the same length and opposite directions",
         ["have the same length and the same direction", "opposite direction", "of the same length"],
         r"The opposite vector of $\vec a$ is the vector with the same length as and opposite direction to $\vec a$."),
        (r"Given two vectors $%s$, $%s$. The difference $%s - %s$ is" % (a, b, a, b), r"$%s + \left(-%s\right)$" % (a, b),
         [r"$%s + \left(-%s\right)$" % (b, a), r"$-%s - %s$" % (a, b), r"$%s + %s$" % (a, b)],
         r"By definition: $%s - %s = %s + \left(-%s\right)$ (add the opposite vector of $%s$)." % (a, b, a, b, b)),
        (r"For any three points $%s$, $%s$, $%s$, the equality $%s - %s = %s$ is called" % (Z, X, Y, v(Z, Y), v(Z, X), v(X, Y)),
         _B8NB_QT[2], [_B8NB_QT[0], _B8NB_QT[1], _B8NB_QT[3]],
         r"Two vectors with the common initial point $%s$: $%s - %s = %s$ is the subtraction rule." % (Z, v(Z, Y), v(Z, X), v(X, Y))),
        (r"For every vector $%s$, the sum $%s + \left(-%s\right)$ equals" % (a, a, a), r"$\overrightarrow{0}$",
         ["$%s$" % a, "$-%s$" % a, "$%s + %s$" % (a, a)],
         r"The sum of a vector and its opposite vector is the zero vector: $%s + \left(-%s\right) = \overrightarrow{0}$." % (a, a)),
        (r"If $%s + %s = \overrightarrow{0}$, then" % (a, b), r"$%s$ is the opposite vector of $%s$" % (b, a),
         [r"$%s = %s$" % (a, b), r"$%s$ and $%s$ have the same direction" % (a, b), r"$%s = \overrightarrow{0}$" % a],
         r"$%s + %s = \overrightarrow{0}$ if and only if $%s = -%s$, that is $%s$ is the opposite vector of $%s$." % (a, b, b, a, b, a)),
    ]


def _b8nb_dien_tinh_chat():
    X, Y, Z, T, a, b, c = _b8nb_ten()
    TEN = ["the commutative property", "the associative property", "the zero-vector property", "the three-point rule"]
    dang_thuc = [r"$%s + %s = %s + %s$" % (a, b, b, a),
                 r"$\left(%s + %s\right) + %s = %s + \left(%s + %s\right)$" % (a, b, c, a, b, c),
                 r"$%s + \overrightarrow{0} = \overrightarrow{0} + %s = %s$" % (a, a, a)]
    ra = []
    for i in range(3):
        ra.append((r"For any vectors $%s$, $%s$, $%s$, the equality %s expresses" % (a, b, c, dang_thuc[i]),
                   TEN[i] + " of vector addition" if i < 2 else TEN[i],
                   [t + (" of vector addition" if j < 2 else "") for j, t in enumerate(TEN) if j != i],
                   r"%s is %s." % (dang_thuc[i], TEN[i] + (" of vector addition" if i < 2 else ""))))
        sai = [dang_thuc[j] for j in range(3) if j != i] + [
            [r"$%s + %s = %s - %s$" % (a, b, b, a), r"$\left(%s + %s\right) + %s = %s + \left(%s - %s\right)$" % (a, b, c, a, b, c),
             r"$%s + \overrightarrow{0} = \overrightarrow{0}$" % a][i]]
        ra.append((r"For any vectors $%s$, $%s$, $%s$, %s of vector addition is written as"
                   % (a, b, c, TEN[i] if i < 2 else "the zero-vector property"), dang_thuc[i], sai,
                   r"%s is %s." % (dang_thuc[i], TEN[i] + (" of vector addition" if i < 2 else ""))))
    return ra


def _b8nb_mc_dien(kho, ten_kho, socau, dang):
    cau = ""
    for _ in range(socau):
        ds = kho()
        i = _c4_uu_tien(ten_kho, list(range(len(ds))))[0]
        _c4_danh_dau(ten_kho, [i])
        mo, dung, sai, ly = ds[i]
        cau += MC_SA_answer_text(mo, dung, random.sample(sai, 3), ly, 0, 0, dang)
    return cau


def L10_C4_B8_NB040_MC_A_01(socau, dang=1):
    r"""Nhận biết tổng hai vectơ: điền khuyết định nghĩa tổng, quy tắc ba điểm, quy tắc hình bình hành, cộng với
    vectơ-không; gọi tên quy tắc từ đẳng thức. Tên điểm, tên vectơ ngẫu nhiên; kho xoay vòng.

    CLAUDE THEM 17/10/2026 - chi MC (ban SA vo ly); co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_mc_dien(_b8nb_dien_tong, "b8nb_dien_tong", socau, dang)


def L10_C4_B8_NB041_MC_A_01(socau, dang=1):
    r"""Nhận biết vectơ đối, hiệu hai vectơ: vectơ đối của $\overrightarrow{XY}$, của vectơ-không, định nghĩa hai vectơ
    đối nhau, định nghĩa hiệu, gọi tên quy tắc trừ, $\vec a + (-\vec a)$. Tên điểm, tên vectơ ngẫu nhiên.

    CLAUDE THEM 17/10/2026 - chi MC (ban SA vo ly); co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_mc_dien(_b8nb_dien_hieu, "b8nb_dien_hieu", socau, dang)


def L10_C4_B8_NB042_MC_A_01(socau, dang=1):
    r"""Nhận biết tính chất của phép cộng vectơ: cho đẳng thức, gọi tên tính chất (giao hoán, kết hợp, vectơ-không);
    hoặc cho tên tính chất, chọn đẳng thức đúng. Tên vectơ ngẫu nhiên.

    CLAUDE THEM 17/10/2026 - chi MC (ban SA vo ly); co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_mc_dien(_b8nb_dien_tinh_chat, "b8nb_dien_tinh_chat", socau, dang)


# ---------------------------------------------------------------- B: khẳng định đúng / sai về khái niệm
def _b8nb_kd_tong():
    """[(phát biểu (có $...$), đúng?, lí do)] về tổng hai vectơ."""
    X, Y, Z, T, a, b, c = _b8nb_ten()
    v = _vt
    h = X + Y + Z + T
    return [
        (r"For any three points $%s$, $%s$, $%s$, $%s + %s = %s$" % (X, Y, Z, v(X, Y), v(Y, Z), v(X, Z)), True, "that is the three-point rule"),
        (r"If $%s$ is a parallelogram, then $%s + %s = %s$" % (h, v(X, Y), v(X, T), v(X, Z)), True, "that is the parallelogram rule"),
        (r"For every vector $%s$, $%s + \overrightarrow{0} = %s$" % (a, a, a), True, "adding the zero vector does not change a vector"),
        (r"For all vectors $%s$, $%s$: $%s + %s = %s + %s$" % (a, b, a, b, b, a), True, "vector addition is commutative"),
        (r"The sum of two vectors is a vector", True, "by definition, the sum of two vectors is a vector"),
        (r"For any two points $%s$, $%s$, $%s + %s = \overrightarrow{0}$" % (X, Y, v(X, Y), v(Y, X)), True,
         r"by the three-point rule $%s + %s = %s = \overrightarrow{0}$" % (v(X, Y), v(Y, X), v(X, X))),
        (r"For any three points $%s$, $%s$, $%s$, $%s + %s = %s$" % (X, Y, Z, v(X, Y), v(Y, Z), v(Z, X)), False,
         r"by the three-point rule $%s + %s = %s$, not $%s$" % (v(X, Y), v(Y, Z), v(X, Z), v(Z, X))),
        (r"For any three points $%s$, $%s$, $%s$, $%s + %s = %s$" % (X, Y, Z, v(X, Y), v(X, Z), v(Y, Z)), False,
         "the three-point rule needs the terminal point of the first vector to coincide with the initial point of the second"),
        (r"If $%s$ is a parallelogram, then $%s + %s = %s$" % (h, v(X, Y), v(X, T), v(Y, T)), False,
         r"by the parallelogram rule $%s + %s = %s$" % (v(X, Y), v(X, T), v(X, Z))),
        (r"For every vector $%s$, $%s + \overrightarrow{0} = \overrightarrow{0}$" % (a, a), False,
         r"$%s + \overrightarrow{0} = %s$" % (a, a)),
        (r"For all vectors $%s$, $%s$: $\left|%s + %s\right| = \left|%s\right| + \left|%s\right|$" % (a, b, a, b, a, b), False,
         "it holds only when the two vectors have the same direction (or one of them is the zero vector)"),
        (r"The sum of two vectors is a number", False, "the sum of two vectors is a vector"),
    ]


def _b8nb_kd_hieu():
    X, Y, Z, T, a, b, c = _b8nb_ten()
    v = _vt
    return [
        (r"The opposite vector of $%s$ is $%s$" % (v(X, Y), v(Y, X)), True, "these two vectors have the same length and opposite directions"),
        (r"The opposite vector of the zero vector is the zero vector", True, r"$-\overrightarrow{0} = \overrightarrow{0}$"),
        (r"For all vectors $%s$, $%s$: $%s - %s = %s + \left(-%s\right)$" % (a, b, a, b, a, b), True, "that is the definition of the difference of two vectors"),
        (r"For any three points $%s$, $%s$, $%s$, $%s - %s = %s$" % (Z, X, Y, v(Z, Y), v(Z, X), v(X, Y)), True, "that is the subtraction rule"),
        (r"Two opposite vectors have the same length", True, "the opposite vector has the same length as and the opposite direction to the given vector"),
        (r"For every vector $%s$, $%s + \left(-%s\right) = \overrightarrow{0}$" % (a, a, a), True, "the sum of a vector and its opposite vector is the zero vector"),
        (r"The opposite vector of $%s$ is $%s$" % (v(X, Y), v(X, Y)), False, r"the opposite vector of $%s$ is $%s$" % (v(X, Y), v(Y, X))),
        (r"Two opposite vectors have the same direction", False, "two opposite vectors have opposite directions"),
        (r"For all vectors $%s$, $%s$: $%s - %s = %s - %s$" % (a, b, a, b, b, a), False,
         r"$%s - %s$ and $%s - %s$ are opposite vectors" % (a, b, b, a)),
        (r"For any three points $%s$, $%s$, $%s$, $%s - %s = %s$" % (Z, X, Y, v(Z, Y), v(Z, X), v(Y, X)), False,
         r"by the subtraction rule $%s - %s = %s$" % (v(Z, Y), v(Z, X), v(X, Y))),
        (r"The zero vector has no opposite vector", False, "the opposite vector of the zero vector is the zero vector"),
        (r"Two vectors with the same length are opposite", False, "they must also have opposite directions"),
    ]


def _b8nb_mc_kd(kho, socau, dang):
    cau = ""
    for _ in range(socau):
        ds = kho()
        hoi = random.random() < 0.55
        d = random.choice([x for x in ds if x[1] == hoi])
        s = random.sample([x for x in ds if x[1] != hoi], 3)
        debai = r"Which of the following statements is %s?" % (r"\textbf{true}" if hoi else r"\textbf{false}")
        giai = r"\\ ".join(r"``%s'' is a %s statement because %s." % (x[0], "true" if x[1] else "false", x[2]) for x in [d] + s)
        cau += MC_SA_answer_text(debai, d[0], [x[0] for x in s], giai, 0, 0, dang)
    return cau


def _b8nb_sa_kd(kho, socau, dang):
    cau = ""
    for _ in range(socau):
        ds = kho()
        so_dung = random.choice([1, 2, 2, 3])
        chon = random.sample([x for x in ds if x[1]], so_dung) + random.sample([x for x in ds if not x[1]], 4 - so_dung)
        random.shuffle(chon)
        de = (r"Consider the following statements: \\ " + r"\\ ".join(r"%d) %s;" % (k + 1, x[0]) for k, x in enumerate(chon))
              + r"\\ How many of these statements are true?")
        ly = r"\\ ".join(r"Statement %d is %s because %s." % (k + 1, "true" if x[1] else "false", x[2]) for k, x in enumerate(chon))
        ly += r"\\ So there are $%d$ true statements." % so_dung
        cau += MC_SA_answer_const(de, str(so_dung), [str(x) for x in (0, 1, 2, 3, 4) if x != so_dung], ly, 0, 0, dang)
    return cau


def L10_C4_B8_NB040_MC_B_01(socau, dang=1):
    r"""Chọn khẳng định đúng (sai) về khái niệm tổng hai vectơ: quy tắc ba điểm, quy tắc hình bình hành, cộng với
    vectơ-không, giao hoán (kho 12 khẳng định, tên điểm/vectơ ngẫu nhiên).

    CLAUDE THEM 17/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_mc_kd(_b8nb_kd_tong, socau, dang)


def L10_C4_B8_NB040_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với NB040_MC_B: bốn khẳng định về tổng hai vectơ, đếm số khẳng định đúng.

    CLAUDE THEM 17/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_sa_kd(_b8nb_kd_tong, socau, dang)


def L10_C4_B8_NB041_MC_B_01(socau, dang=1):
    r"""Chọn khẳng định đúng (sai) về vectơ đối, hiệu hai vectơ, quy tắc trừ (kho 12 khẳng định, tên ngẫu nhiên).

    CLAUDE THEM 17/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_mc_kd(_b8nb_kd_hieu, socau, dang)


def L10_C4_B8_NB041_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với NB041_MC_B: bốn khẳng định về vectơ đối, hiệu, đếm số khẳng định đúng.

    CLAUDE THEM 17/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    return _b8nb_sa_kd(_b8nb_kd_hieu, socau, dang)


# =====================================================================
# BÀI 8 - LUYỆN TẬP THÊM VD040 (cô Lan 17/10/2026, ảnh SGK): bài 4.9 (hai lực trên hình, góc 120 độ) là mức VẬN DỤNG
# -> VD040_MC_B, SA_B; bài Vận dụng kéo pháo lên dốc nghiêng 30 độ là mức VẬN DỤNG CAO -> VD040_MC_C, SA_C
# (Mapping "muc_do_dang": "VDC" - quy ước docs/04_ID_STANDARD.md). Cùng đơn vị luyện tập thêm L10_C4_B8_VD040.
# =====================================================================
def _b8_hinh_hai_luc(p, q, g, goc0):
    """TikZ: hai vectơ lực chung gốc O, độ dài tỉ lệ độ lớn, cung góc g."""
    s = 3.2 / max(p, q)
    a1, a2 = goc0, goc0 + g
    out = [r"\begin{tikzpicture}[>=stealth,thick,scale=0.85]"]
    for a, d, ten in ((a1, p * s, r"\overrightarrow{F_1}"), (a2, q * s, r"\overrightarrow{F_2}")):
        out.append(r"\draw[->] (0,0) -- (%s:%s);" % (_toa(a), _toa(d)))
        out.append(r"\node at (%s:%s) {$%s$};" % (_toa(a), _toa(d + 0.55), ten))
    r0 = min(0.7, 0.35 * min(p, q) * s)
    if g == 90:
        # Góc vuông: kí hiệu ô vuông nhỏ ở O, không vẽ cung + "90°" (cô Lan 23/10/2026: "góc vuông vẽ sai kí hiệu")
        k = min(0.35, max(0.22, 0.6 * r0))
        u = (k * math.cos(math.radians(a1)), k * math.sin(math.radians(a1)))
        v = (k * math.cos(math.radians(a2)), k * math.sin(math.radians(a2)))
        out.append(r"\draw[thin] (%s,%s) -- (%s,%s) -- (%s,%s);" % (
            _toa(u[0]), _toa(u[1]), _toa(u[0] + v[0]), _toa(u[1] + v[1]), _toa(v[0]), _toa(v[1])))
    else:
        out.append(r"\draw[thin] (%s:%s) arc (%s:%s:%s);" % (_toa(a1), _toa(r0), _toa(a1), _toa(a2), _toa(r0)))
        out.append(r"\node at (%s:%s) {\footnotesize $%d^\circ$};" % (_toa((a1 + a2) / 2), _toa(r0 + 0.5), g))
    out.append(r"\fill (0,0) circle[radius=1.5pt] node[below]{\footnotesize $O$};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def _b8_vd040b(mc):
    """Bài 4.9: hai lực trên hình. -> (debai, dap, nhieu, giai, hinh)."""
    g = random.choice([60, 90, 120, 120]) if mc else random.choice([30, 45, 60, 90, 120, 135, 150])
    while True:
        p, q = random.randint(1, 8), random.randint(1, 8)
        if p != q or random.random() < 0.2:
            break
    hoi = random.choice(["tong", "tong", "can_bang", "hieu"])
    F1, F2, F3 = (r"\overrightarrow{F_%d}" % i for i in (1, 2, 3))
    cos = _sp8.cos(_sp8.pi * g / 180)
    dau = -1 if hoi == "hieu" else 1
    R2 = _sp8.sympify(p * p + q * q + 2 * dau * p * q * cos)
    R = _sp8.sqrt(R2)
    mo = (r"The figure shows two forces $%s$, $%s$ acting on an object (placed at $O$); the angle between the two forces is "
          r"$%d^\circ$, $\left|%s\right| = %d$ N, $\left|%s\right| = %d$ N." % (F1, F2, g, F1, p, F2, q))
    if hoi == "tong":
        cau_hoi = r"Find the magnitude of the resultant force $%s + %s$" % (F1, F2)
    elif hoi == "can_bang":
        cau_hoi = r"What magnitude must an additional force $%s$ have so that the object stays at rest" % F3
    else:
        cau_hoi = r"Find the magnitude of the vector $%s - %s$" % (F1, F2)
    if hoi == "hieu":
        giai = (r"Let $\overrightarrow{OA} = %s$, $\overrightarrow{OB} = %s$; then $%s - %s = \overrightarrow{OA} - "
                r"\overrightarrow{OB} = \overrightarrow{BA}$ (subtraction rule). The triangle $OAB$ has $OA = %d$, $OB = %d$, "
                r"$\widehat{AOB} = %d^\circ$. By the law of cosines:\\ $AB^2 = %d^2 + %d^2 - 2\cdot %d\cdot %d\cdot\cos %d^\circ = %s$."
                % (F1, F2, F1, F2, p, q, g, p, q, p, q, g, _b8_tex(R2)))
        tong = r"\left|%s - %s\right| = AB" % (F1, F2)
    else:
        giai = (r"Let $\overrightarrow{OA} = %s$, $\overrightarrow{OB} = %s$ and construct the parallelogram $OACB$; then "
                r"$%s + %s = \overrightarrow{OC}$ (parallelogram rule). The triangle $OAC$ has $OA = %d$, $AC = OB = %d$, "
                r"$\widehat{OAC} = 180^\circ - %d^\circ = %d^\circ$. By the law of cosines:\\ "
                r"$OC^2 = %d^2 + %d^2 - 2\cdot %d\cdot %d\cdot\cos %d^\circ = %s$."
                % (F1, F2, F1, F2, p, q, g, 180 - g, p, q, p, q, 180 - g, _b8_tex(R2)))
        tong = r"\left|%s + %s\right| = OC" % (F1, F2)
        if hoi == "can_bang":
            giai = (r"The object is at rest when $%s + %s + %s = \overrightarrow{0}$, that is $%s = -\left(%s + %s\right)$, so "
                    r"$\left|%s\right| = \left|%s + %s\right|$.\\ " % (F1, F2, F3, F3, F1, F2, F3, F1, F2)) + giai
    hinh = _b8_hinh_hai_luc(p, q, g, random.choice([0, 0, 10, 20, -15]))
    sai_dau = _sp8.sqrt(_sp8.sympify(p * p + q * q - 2 * dau * p * q * cos))
    ung = [sai_dau, p + q, abs(p - q), _sp8.sqrt(p * p + q * q), R2] + [_sp8.sqrt(R2 + k) for k in (2, -2, 4, 1, 3) if R2 + k > 0]
    cham = "?" if hoi == "can_bang" else "."
    if mc:
        dap = _b8_tex(R)
        giai += r"\\ Hence the required magnitude is $%s = \sqrt{%s}%s$ N." % (tong, _b8_tex(R2),
                                                                     "" if _b8_tex(R) == r"\sqrt{%s}" % _b8_tex(R2)
                                                                     else " = " + _b8_tex(R))
        nhieu = []
        for x in ung:
            x = _sp8.sympify(x)
            if x > 0 and abs(float(x) - float(R)) > 1e-9 and all(abs(float(x) - float(y)) > 1e-9 for y in nhieu):
                nhieu.append(x)
        return mo + " " + cau_hoi + cham, r"$%s$ N" % dap, [r"$%s$ N" % _b8_tex(x) for x in nhieu[:3]], giai, hinh
    dap, muc = _b8_sa(R)
    giai += r"\\ Hence the required magnitude is $%s = \sqrt{%s} %s %s$ (N)." % (tong, _b8_tex(R2), r"\approx" if muc else "=", dap)
    lam = (r" (unit: N; round the result to the %s)" % muc) if muc else r" (unit: N)"
    nhieu = [_b8_sa(x)[0] for x in ung]
    return mo + " " + cau_hoi + lam + cham, dap, [x for x in nhieu if x != dap] + ["1", "2", "3", "4"], giai, hinh


def L10_C4_B8_VD040_MC_B_01(socau, dang=1):
    r"""Hai lực $\overrightarrow{F_1}$, $\overrightarrow{F_2}$ biểu diễn trên hình (góc $60^\circ$, $90^\circ$, $120^\circ$):
    độ lớn hợp lực, lực $\overrightarrow{F_3}$ để vật đứng yên, hoặc độ lớn $\overrightarrow{F_1} - \overrightarrow{F_2}$
    (quy tắc trừ); đáp số dạng căn chính xác. Theo bài 4.9 SGK cô Lan gửi (mức VD). LUYỆN TẬP THÊM.

    CLAUDE THEM 17/10/2026 - co Lan xep muc VD; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, nhieu, giai, hinh = _b8_vd040b(True)
        cau += MC_SA_answer_text(debai, dap, nhieu, giai, hinh, 0, dang)
    return cau


def L10_C4_B8_VD040_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với VD040_MC_B: góc $30^\circ$ đến $150^\circ$, đáp số nguyên hoặc làm tròn (<= 4 kí tự).

    CLAUDE THEM 17/10/2026 - co Lan xep muc VD; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, nhieu, giai, hinh = _b8_vd040b(False)
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, hinh, 0, dang)
    return cau


# ---------------------------------------------------------------- C (VDC): kéo vật lên dốc nghiêng
def _b8_hinh_doc(a):
    """TikZ mặt dốc nghiêng góc a độ, vật (hình chữ nhật) có TÂM O, trọng lực P, phản lực w, lực kéo F đặt tại O
    (như Hình 4.18 SGK). Sửa 21/10/2026 (cô Lan): "toạ độ điểm O phải là tâm của hình chữ nhật" - trước đây O là
    trung điểm cạnh đáy (chỗ vật chạm mặt dốc)."""
    r = math.radians(a)
    L = 6.0
    # dốc thoải (dưới 20 độ): đẩy vật lên cao hơn trên dốc để nhãn góc đặt xa đỉnh góc mà không chạm trọng lực P
    u = (math.cos(r), math.sin(r))                       # dọc dốc, hướng lên
    n = (-math.sin(r), math.cos(r))                      # pháp tuyến hướng lên
    rong, cao = 0.9, 0.5                                 # vật: dài 0.9 dọc dốc, cao 0.5
    d = 4.3 if a < 20 else 3.6
    S0 = (d * math.cos(r), d * math.sin(r))              # trung điểm cạnh đáy (chỗ vật chạm mặt dốc)
    O = (S0[0] + n[0] * cao / 2, S0[1] + n[1] * cao / 2)  # TÂM hình chữ nhật: điểm đặt ba lực
    # độ dài vẽ trọng lực: ngọn mũi tên P xuống hẳn dưới mặt đất (không để chữ P đè lên đường nằm ngang);
    # w, F vẽ theo cùng tỉ lệ lp nên tam giác lực vẫn đúng hình dạng
    lp = max(2.2, O[1] + 0.55)
    P = (O[0], O[1] - lp)
    W = (O[0] + n[0] * lp * math.cos(r), O[1] + n[1] * lp * math.cos(r))
    lf = max(lp * math.sin(r), 1.0)                      # dốc thoải: F theo tỉ lệ sẽ nằm lọt trong vật, nên tối thiểu 1
    F = (O[0] + u[0] * lf, O[1] + u[1] * lf)
    goc = [(O[0] + i * rong / 2 * u[0] + j * cao / 2 * n[0], O[1] + i * rong / 2 * u[1] + j * cao / 2 * n[1])
           for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    nhan_O = (O[0] - 0.24 * u[0], O[1] - 0.24 * u[1])    # chữ O trong vật, bên trái tâm (không đè ba mũi tên)
    T = lambda p: "(%s,%s)" % (_toa(p[0]), _toa(p[1]))
    out = [r"\begin{tikzpicture}[>=stealth,thick,scale=0.8]",
           r"\draw (0,0) -- (%s,0);" % _toa(L * math.cos(r) + 0.5),
           r"\draw (0,0) -- %s;" % T((L * math.cos(r), L * math.sin(r))),
           r"\draw[fill=cyan!30] " + " -- ".join(T(p) for p in goc) + " -- cycle;",
           r"\draw[->] %s -- %s node[right]{$\overrightarrow{P}$};" % (T(O), T(P)),
           r"\draw[->] %s -- %s node[above left]{$\overrightarrow{w}$};" % (T(O), T(W)),
           r"\draw[->,blue] %s -- %s node[above]{$\overrightarrow{F}$};" % (T(O), T(F)),
           r"\fill %s circle[radius=1.5pt];" % T(O),
           r"\node at %s {\scriptsize $O$};" % T(nhan_O),
           r"\draw[thin] (1,0) arc (0:%s:1);" % _toa(a),
           # nhãn góc: dốc càng thoải đặt càng xa đỉnh (khe giữa hai cạnh đủ rộng cho chữ)
           r"\node at (%s:%s) {\footnotesize $%d^\circ$};" % (_toa(a / 2), _toa(min(2.9, max(1.45, 0.5 / math.tan(r)))), a),
           r"\end{tikzpicture}"]
    return "\n".join(out)


_B8_DOC_NGHIENG = {"keo_xe_hang_len_doc": (8, 15), "keo_phao_len_doc": (15, 30), "toi_keo_go_len_doc": (10, 30)}


def _b8_vd040c(mc):
    """Kéo vật lên dốc nghiêng (VDC). -> (debai, dap, nhieu, giai, hinh)."""
    bc = _c4_uu_tien("b8_vd040c", ["keo_phao_len_doc", "keo_xe_hang_len_doc", "toi_keo_go_len_doc"])[0]
    _c4_danh_dau("b8_vd040c", [bc])
    # Góc nghiêng KHOÁ theo thực tế từng bối cảnh (cô Lan 21/10/2026: "độ nghiêng không hợp lý ... khoá độ dốc cho hợp
    # lý"; trước đây rút 10-45 độ cho mọi bối cảnh, ra cả "xe chở hàng lên dốc 40 độ"). Mốc: đường ô tô miền núi theo
    # TCVN 4054 dốc dọc chỉ khoảng 10 % (~6 độ); con phố dốc nhất thế giới khoảng 35 % (~19 độ). Người kéo xe chở hàng
    # trên dốc 8-15 độ là đã rất dốc; kéo pháo qua đường núi 15-30 độ (bài SGK dùng 30 độ); tời kéo gỗ trên sườn /
    # máng 10-30 độ. Dưới 8 độ lực kéo quá nhỏ, mũi tên F trên hình gần như không thấy.
    a = random.randint(*_B8_DOC_NGHIENG[bc])
    r = _sp8.pi * a / 180
    if bc == "keo_phao_len_doc":
        P = random.randint(150, 260) * 100 + random.randint(0, 99)        # N
        vat, nguoi = "the cannon", random.choice([80, 90, 100, 120, 150])
        mo = (r"Soldiers pull a cannon of weight $%s$ N up a slope inclined at $%d^\circ$ to the horizontal "
              r"(see the figure). Assume the cannon is subject to three forces: the weight $\overrightarrow{P}$, the normal force $\overrightarrow{w}$ of "
              r"the slope (perpendicular to the slope) and the pulling force $\overrightarrow{F}$ (along the slope, toward the top of the slope); "
              r"the cannon can be pulled when $\left|\overrightarrow{F}\right|$ is not less than the magnitude needed for "
              r"$\overrightarrow{F} + \overrightarrow{P} + \overrightarrow{w} = \overrightarrow{0}$."
              % (_b8_ngan_cach(P), a))
        hoi = random.choice(["nguoi", "nguoi", "luc_kn", "phan_luc_kn"])
    elif bc == "keo_xe_hang_len_doc":
        P = random.randint(30, 90) * 100                                     # N
        vat, nguoi = "the cargo cart", random.choice([150, 180, 200, 250])
        mo = (r"A group of workers pull a cargo cart of weight $%s$ N up a slope inclined at $%d^\circ$ to the "
              r"horizontal (see the figure). Assume the cart is subject to three forces: the weight $\overrightarrow{P}$, the normal force "
              r"$\overrightarrow{w}$ of the slope (perpendicular to the slope) and the pulling force $\overrightarrow{F}$ (along the "
              r"slope, toward the top of the slope); the cart can be pulled when $\left|\overrightarrow{F}\right|$ is not less than the magnitude needed "
              r"for $\overrightarrow{F} + \overrightarrow{P} + \overrightarrow{w} = \overrightarrow{0}$." % (_b8_ngan_cach(P), a))
        hoi = random.choice(["nguoi", "nguoi", "luc_n", "phan_luc_n"])
    else:
        P = random.randint(20, 95) * 100
        vat, nguoi = "the log", None
        mo = (r"A winch pulls a log of weight $%s$ N up a slope inclined at $%d^\circ$ to the horizontal "
              r"(see the figure). Assume the log is subject to three forces: the weight $\overrightarrow{P}$, the normal force $\overrightarrow{w}$ of the "
              r"slope (perpendicular to the slope) and the pulling force $\overrightarrow{F}$ of the winch cable (along the slope, toward the top of the "
              r"slope); the log moves uniformly, so $\overrightarrow{F} + \overrightarrow{P} + \overrightarrow{w} = "
              r"\overrightarrow{0}$." % (_b8_ngan_cach(P), a))
        hoi = random.choice(["luc_n", "phan_luc_n"])
    Fk = P * _sp8.sin(r)
    Wk = P * _sp8.cos(r)
    giai = (r"Let $\overrightarrow{OA} = \overrightarrow{P}$ (vertical, pointing down) and draw $\overrightarrow{AC} = "
            r"\overrightarrow{w}$; then $\overrightarrow{P} + \overrightarrow{w} = \overrightarrow{OC}$ (three-point rule), "
            r"$\overrightarrow{OC}$ lies along the slope, pointing down. The triangle $OAC$ right-angled at $C$ has $OA = %s$, "
            r"$\widehat{OAC} = %d^\circ$ (its sides are perpendicular to the sides of the slope angle), so "
            r"$OC = OA\sin %d^\circ$, $AC = OA\cos %d^\circ$.\\ "
            r"From $\overrightarrow{F} + \overrightarrow{P} + \overrightarrow{w} = \overrightarrow{0}$ we get "
            r"$\overrightarrow{F} = -\overrightarrow{OC}$, hence $\left|\overrightarrow{F}\right| = %s\sin %d^\circ "
            r"\approx %s$ (N) and $\left|\overrightarrow{w}\right| = %s\cos %d^\circ \approx %s$ (N)."
            % (_b8_ngan_cach(P), a, a, a, _b8_ngan_cach(P), a, _b8_tron(Fk, 1), _b8_ngan_cach(P), a, _b8_tron(Wk, 1)))
    if hoi == "nguoi":
        n = int(_sp8.ceiling(Fk / nguoi))
        cau_hoi = (r"If each person pulls with a force of $%d$ N, at least how many people are needed to pull %s up the slope"
                   % (nguoi, vat))
        giai += (r"\\ We need $k$ people with $%d k \ge %s$, that is $k \ge %s$. Hence at least $%d$ people are needed."
                 % (nguoi, _b8_tron(Fk, 1), _b8_tron(Fk / nguoi, 2), n))
        dap = str(n)
        ung = [int(_sp8.ceiling(Wk / nguoi)), n - 1, int(_sp8.ceiling(P / nguoi)), int(_sp8.ceiling(P * _sp8.tan(r) / nguoi)),
               n + 1, int(_sp8.ceiling(Fk / nguoi / 2))]
        nhieu = [str(x) for x in ung]
        don_vi, lam = "people", ""
    else:
        kn = hoi.endswith("kn")
        v = (Fk if hoi.startswith("luc") else Wk) / (1000 if kn else 1)
        so_le = 1 if kn else 0
        dap = _b8_tron(v, so_le)
        doi = (Wk if hoi.startswith("luc") else Fk) / (1000 if kn else 1)
        ung = [doi, _sp8.sympify(P) / (1000 if kn else 1), v * 2, P * _sp8.tan(r) / (1000 if kn else 1), v / 2]
        nhieu = [_b8_tron(x, so_le) for x in ung]
        don_vi = "kN" if kn else "N"
        if hoi.startswith("luc"):
            cau_hoi = r"Find the minimum magnitude of the pulling force $\overrightarrow{F}$"
        else:
            cau_hoi = r"Find the magnitude of the normal force $\overrightarrow{w}$ of the slope"
        if kn:
            giai += r"\\ In kilonewtons: $%s$ kN." % dap
        lam = r"round the result to the %s" % _B8_MUC[so_le]
    hinh = _b8_hinh_doc(a)
    nhieu = [x for x in dict.fromkeys(nhieu) if x != dap and float(x.replace(",", ".")) > 0]
    if mc:
        fm = lambda t: r"$%s$ %s" % (t, don_vi)
        return (mo + " " + cau_hoi + ((r" (%s)" % lam) if lam else "") + ("?" if hoi == "nguoi" else "."), fm(dap),
                [fm(t) for t in nhieu[:3]],
                giai, hinh)
    if don_vi == "people":
        de = mo + " " + cau_hoi + "?"
    else:
        de = mo + " " + cau_hoi + r" (unit: %s; %s)." % (don_vi, lam)
    return de, dap, nhieu + [str(i) for i in range(1, 10)], giai, hinh


def _b8_ngan_cach(n):
    """Số nguyên >= 10000 viết có dấu cách nghìn như SGK: 22\\,148."""
    s = str(int(n))
    return s if len(s) <= 4 else s[:-3] + r"\," + s[-3:]


def L10_C4_B8_VD040_MC_C_01(socau, dang=1):
    r"""VẬN DỤNG CAO: kéo vật lên dốc nghiêng (khẩu pháo, xe chở hàng, khúc gỗ kéo bằng tời) - ba lực
    $\overrightarrow{F} + \overrightarrow{P} + \overrightarrow{w} = \overrightarrow{0}$: số người tối thiểu, lực kéo tối
    thiểu hoặc phản lực mặt dốc ($\left|\overrightarrow{P}\right|\sin\alpha$, $\left|\overrightarrow{P}\right|\cos\alpha$).
    Theo bài Vận dụng SGK (kéo pháo $22\,148$ N lên dốc $30^\circ$) cô Lan gửi. LUYỆN TẬP THÊM.

    CLAUDE THEM 17/10/2026 - co Lan xep muc VDC (Mapping muc_do_dang VDC); co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, nhieu, giai, hinh = _b8_vd040c(True)
        cau += MC_SA_answer_text(debai, dap, nhieu, giai, hinh, 0, dang)
    return cau


def L10_C4_B8_VD040_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với VD040_MC_C (VẬN DỤNG CAO): số người tối thiểu / lực kéo / phản lực, <= 4 kí tự.

    CLAUDE THEM 17/10/2026 - co Lan xep muc VDC; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dap, nhieu, giai, hinh = _b8_vd040c(False)
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, hinh, 0, dang)
    return cau


# =====================================================================
# TH039 bản TRẢ LỜI NGẮN (cô Lan 17/10/2026: ô SA TH của Bài 7 trống khi chọn "Chỉ theo YCCĐ" vì TH039 chỉ có MC).
# SA_B, SA_C, SA_D cùng Dang với MC_B, MC_C, MC_D; TH039_MC_A (chọn đại lượng là vectơ) chỉ MC.
# =====================================================================
def _c4_qh_luc(a, b):
    if _c4_bang(a, b):
        return "are equal"
    if _c4_ch(a, b):
        return "same direction"
    if _c4_cp(a, b):
        return "opposite direction"
    return "not collinear"


def L10_C4_B7_TH039_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với TH039_MC_B: bốn lực $\overrightarrow{F_1}, \ldots, \overrightarrow{F_4}$ trên lưới ô
    vuông; đếm số cặp lực cùng hướng / ngược hướng / bằng nhau / cùng phương. Python xét bằng toạ độ.

    CLAUDE THEM 17/10/2026 - co Lan duyet; co Lan duyet lai."""
    import itertools
    cau = ""
    so = 0
    while so < socau:
        hoi = random.choice(["same direction", "opposite direction", "are equal", "collinear"])
        goc = random.sample([(1, 0), (0, 1), (1, 1), (1, -1)], 2)
        V = []
        for _ in range(4):
            g = random.choice(goc + [random.choice(list(_C4_HUONG))])
            s = random.choice([1, -1])
            k = random.randint(1, 3)
            V.append((s * g[0] * k, s * g[1] * k))
        cap = list(itertools.combinations(range(4), 2))
        qh = {c: _c4_qh_luc(V[c[0]], V[c[1]]) for c in cap}
        if hoi == "same direction":
            dem = [c for c in cap if qh[c] in ("same direction", "are equal")]
        elif hoi == "collinear":
            dem = [c for c in cap if qh[c] != "not collinear"]
        else:
            dem = [c for c in cap if qh[c] == hoi]
        if not 1 <= len(dem) <= 4 or len(set(V)) < 3:
            continue
        try:
            ds = _c4_dat_mui_ten(V)
        except ValueError:
            continue
        so += 1
        ten = [r"\overrightarrow{F_{%d}}" % (i + 1) for i in range(4)]
        tx = lambda c: r"$%s$ and $%s$" % (ten[c[0]], ten[c[1]])
        cau_hoi = {"same direction": r"How many pairs of forces (unordered) \textbf{have the same direction}?",
                   "opposite direction": r"How many pairs of forces (unordered) \textbf{have opposite directions}?",
                   "are equal": r"How many pairs of forces (unordered) \textbf{are equal}?",
                   "collinear": r"How many pairs of forces (unordered) \textbf{are collinear}?"}[hoi]
        ket = {"same direction": r"\\ Hence there are $%d$ pairs of forces with the same direction (including equal pairs).",
               "opposite direction": r"\\ Hence there are $%d$ pairs of forces with opposite directions.",
               "are equal": r"\\ Hence there are $%d$ pairs of equal forces.",
               "collinear": r"\\ Hence there are $%d$ pairs of collinear forces (same or opposite direction)."}[hoi]
        debai = (r"The forces $%s$ acting on objects are represented by the vectors on the square grid in the figure. "
                 % "$, $".join(ten)) + cau_hoi
        giai = (r"Read the directions and lengths of the vectors on the grid and check all $6$ pairs:\\ "
                + r"\\ ".join(r"%s %s." % (tx(c), qh[c]) for c in cap) + ket % len(dem))
        nhieu = [str(x) for x in (len(dem) + 1, len(dem) - 1, 6, 0, len(dem) + 2) if x != len(dem) and x >= 0]
        cau += MC_SA_answer_const(debai, str(len(dem)), nhieu, giai, _c4_luoi(ds, ten), 0, dang)
    return cau


def L10_C4_B7_TH039_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với TH039_MC_C: bốn vectơ vận tốc trên lưới ô vuông có la bàn (mỗi cạnh ô ứng với
    $10$ km/h); đọc tốc độ của vật đi theo một hướng cho trước (kể cả hướng đông bắc, tây nam... - đường chéo ô:
    $10k\sqrt{2}$, làm tròn hàng đơn vị).

    CLAUDE THEM 17/10/2026 - co Lan duyet; co Lan duyet lai."""
    cau = ""
    so = 0
    while so < socau:
        huong = random.choice(list(_C4_HUONG))
        cheo = huong[0] != 0 and huong[1] != 0
        k = random.randint(1, 3) if cheo else random.randint(2, 4)
        khac = [h for h in _C4_HUONG if h != huong]
        V = [(huong[0] * k, huong[1] * k)]
        for h in random.sample([(-huong[0], -huong[1])] + random.sample([x for x in khac if x != (-huong[0], -huong[1])], 3), 3):
            kk = random.randint(1, 3) if h[0] and h[1] else random.randint(1, 4)
            V.append((h[0] * kk, h[1] * kk))
        thu_tu = list(range(4))
        random.shuffle(thu_tu)
        ten = [r"\overrightarrow{%s}" % c for c in "abcd"]
        try:
            ds = _c4_dat_mui_ten([V[i] for i in thu_tu], 10, 6)
        except ValueError:
            continue
        so += 1
        vi = ten[thu_tu.index(0)]
        vat, vat_ngan = random.choice([("a boat", "the boat"), ("a storm", "the storm"),
                                       ("a car", "the car"), ("a flock of birds", "the flock of birds"),
                                       ("an airplane", "the airplane")])
        if cheo:
            gt = 10 * k * math.sqrt(2)
            dap = str(int(_Dec8(str(gt)).quantize(_Dec8(1), rounding=_HU8)))
            ly = (r"The vector pointing %s is $%s$; it is the diagonal of a square of side $%d$ cells, so its length is $%d\sqrt{2}$ cells. "
                  r"The speed is $%d\sqrt{2}\cdot 10 = %d\sqrt{2} \approx %s$ (km/h)." % (_C4_HUONG[huong], vi, k, k, k, 10 * k, dap))
            lam = r" (round the result to the nearest whole number)"
        else:
            dap = str(10 * k)
            ly = r"The vector pointing %s is $%s$, of length $%d$ cells, so the speed is $%d\cdot 10 = %s$ (km/h)." % (
                _C4_HUONG[huong], vi, k, k, dap)
            lam = ""
        debai = (r"On the square grid (see the figure, up is north, right is east), each side of a cell corresponds to "
                 r"$10$ km/h. One of the vectors in the figure represents the velocity of %s moving %s. What is the speed "
                 r"of %s in kilometres per hour%s?" % (vat, _C4_HUONG[huong], vat_ngan, lam))
        nhieu = [str(10 * k), str(k), str(10 * (k + 1)), str(int(10 * k * 1.5)), str(10 * (k + 2)), str(10 * k + 5),
                 str(20 * k)]
        cau += MC_SA_answer_const(debai, dap, [x for x in nhieu if x != dap], ly, _c4_luoi(ds, ten, la_ban=True), 0, dang)
    return cau


def L10_C4_B7_TH039_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - cùng Dang với TH039_MC_D: bối cảnh dòng sông (thuyền xuôi, ngược dòng) hoặc ba xe trên đường
    thẳng; bốn khẳng định về cùng hướng, ngược hướng, bằng nhau, độ lớn; đếm số khẳng định đúng.

    CLAUDE THEM 17/10/2026 - co Lan duyet; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        mo, X = _c4_kho_song()
        so_dung = random.choice([1, 2, 2, 3])
        chon = random.sample([x for x in X if x[1]], so_dung) + random.sample([x for x in X if not x[1]], 4 - so_dung)
        random.shuffle(chon)
        de = (mo + r" Consider the following statements: \\ " + r"\\ ".join(r"%d) %s;" % (k + 1, x[0]) for k, x in enumerate(chon))
              + r"\\ How many of these statements are true?")
        ly = r"\\ ".join(r"Statement %d is %s because %s." % (k + 1, "true" if x[1] else "false", x[2]) for k, x in enumerate(chon))
        ly += r"\\ So there are $%d$ true statements." % so_dung
        cau += MC_SA_answer_const(de, str(so_dung), [str(x) for x in (0, 1, 2, 3, 4) if x != so_dung], ly, 0, 0, dang)
    return cau
