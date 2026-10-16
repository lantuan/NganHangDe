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
