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
            dung = r"$%s$ và $%s$ cùng hướng" % (_vt(A, B), _vt(D, C))
            nhieu = [r"$%s$ và $%s$ cùng hướng" % (_vt(A, B), _vt(C, D)),
                     r"$%s$ và $%s$ cùng phương" % (_vt(A, B), _vt(A, D)),
                     r"$%s$ và $%s$ cùng phương" % (_vt(A, C), _vt(B, D)),
                     r"$%s$ và $%s$ cùng hướng" % (_vt(B, A), _vt(D, C))]
            ly_do = (r"Vì $%s%s%s%s$ là hình bình hành nên $%s$ song song và "
                     r"bằng $%s$, hơn nữa hai vectơ $%s$ và $%s$ chỉ về cùng "
                     r"một phía nên chúng \textbf{cùng hướng}."
                     % (A, B, C, D, A + B, D + C, _vt(A, B), _vt(D, C)))
        else:
            dung = r"$%s$ và $%s$ cùng hướng" % (_vt(A, D), _vt(B, C))
            nhieu = [r"$%s$ và $%s$ cùng hướng" % (_vt(A, D), _vt(C, B)),
                     r"$%s$ và $%s$ cùng phương" % (_vt(A, D), _vt(A, B)),
                     r"$%s$ và $%s$ cùng phương" % (_vt(A, C), _vt(B, D)),
                     r"$%s$ và $%s$ cùng hướng" % (_vt(D, A), _vt(B, C))]
            ly_do = (r"Vì $%s%s%s%s$ là hình bình hành nên $%s$ song song và "
                     r"bằng $%s$; hai vectơ $%s$ và $%s$ chỉ về cùng một phía "
                     r"nên chúng \textbf{cùng hướng}."
                     % (A, B, C, D, A + D, B + C, _vt(A, D), _vt(B, C)))

        debai = (r"Cho hình bình hành $%s$ như hình vẽ. Khẳng định nào sau "
                 r"đây \textbf{đúng}?" % ten)
        giai = (r"Hai vectơ \textbf{cùng phương} khi giá của chúng song song "
                r"hoặc trùng nhau; trong các vectơ cùng phương, hai vectơ "
                r"\textbf{cùng hướng} khi chúng chỉ về cùng một phía."
                "\\\\\n" + ly_do +
                "\\\\\n"
                r"Hai đường chéo $%s$ và $%s$ cắt nhau nên $%s$ và $%s$ "
                r"không cùng phương." % (A + C, B + D, _vt(A, C), _vt(B, D)))
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

        debai = (r"Cho hình chữ nhật $%s$, với $%s$, $%s$ lần lượt là trung "
                 r"điểm của cạnh $%s$ và $%s$ (xem hình vẽ). Trong các khẳng "
                 r"định sau, khẳng định nào \textbf{sai}?"
                 % (ten, M, N, A + B, C + D))
        giai = (r"Hai vectơ bằng nhau khi chúng \textbf{cùng hướng} và "
                r"\textbf{cùng độ dài}."
                "\\\\\n"
                r"$%s$ hướng từ dưới lên, còn $%s$ hướng từ trên xuống: hai "
                r"vectơ này \textbf{ngược hướng} (chúng là hai vectơ đối "
                r"nhau), nên $%s = %s$ là khẳng định sai."
                % (_vt(D, A), _vt(M, N), _vt(D, A), _vt(M, N)) +
                "\\\\\n"
                r"Ba khẳng định còn lại đều đúng: $%s$ và $%s$ cùng hướng và "
                r"cùng độ dài (đều bằng nửa cạnh $%s$); $%s$ và $%s$ cùng "
                r"hướng, cùng độ dài; $%s$ và $%s$ cùng hướng, cùng độ dài."
                % (_vt(M, B), _vt(N, C), A + B, _vt(A, B), _vt(D, C),
                   _vt(M, A), _vt(C, N)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C4_B7_TH039_MC_A_01(socau, dang=1):
    """Biểu thị một đại lượng thực tiễn bằng vectơ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    LA_VECTO = [
        "Vận tốc của một chiếc thuyền đang chạy",
        "Lực kéo tác dụng lên một thùng hàng",
        "Độ dịch chuyển của một vật từ vị trí này sang vị trí khác",
        "Gia tốc của một vật đang chuyển động",
    ]
    KHONG_VECTO = [
        "Nhiệt độ của không khí trong phòng",
        "Khối lượng của một bao gạo",
        "Thời gian chạy hết quãng đường",
        "Diện tích của một mảnh vườn",
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
        debai = (r"Trong các đại lượng sau, đại lượng nào là đại lượng "
                 r"\textbf{vectơ}, tức là cần cả độ lớn lẫn hướng để mô tả?")
        giai = (r"Đại lượng vectơ là đại lượng phải mô tả bằng \textbf{cả độ "
                r"lớn và hướng}; đại lượng vô hướng chỉ cần độ lớn."
                "\\\\\n"
                r"``%s'' cần chỉ rõ hướng mới xác định được nên là đại lượng "
                r"vectơ." % LA_VECTO[i] +
                "\\\\\n"
                r"Nhiệt độ, khối lượng, thời gian, diện tích chỉ cần một số "
                r"đo nên là các đại lượng vô hướng.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
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
        debai = (r"Với ba điểm $%s$, $%s$, $%s$ bất kì, khẳng định nào sau "
                 r"đây \textbf{đúng}?" % (X, Y, Z))
        giai = (r"Quy tắc ba điểm: với ba điểm bất kì, vectơ có điểm đầu là "
                r"điểm thứ nhất và điểm cuối là điểm thứ ba bằng tổng hai "
                r"vectơ nối qua điểm ở giữa:"
                "\\\\\n"
                r"$%s + %s = %s$." % (_vt(X, Y), _vt(Y, Z), _vt(X, Z)) +
                "\\\\\n"
                r"Điều cốt lõi là điểm cuối của vectơ thứ nhất phải trùng "
                r"điểm đầu của vectơ thứ hai (ở đây là điểm $%s$)." % Y)
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
        debai = (r"Cho hình bình hành $%s$ như hình vẽ. Tổng "
                 r"$%s + %s$ bằng vectơ nào sau đây?"
                 % (ten, _vt(A, B), _vt(A, D)))
        giai = (r"Quy tắc hình bình hành: nếu $%s%s%s%s$ là hình bình hành "
                r"thì tổng hai vectơ xuất phát từ cùng đỉnh $%s$ là vectơ "
                r"đường chéo cũng xuất phát từ $%s$:" % (A, B, C, D, A, A) +
                "\\\\\n"
                r"$%s + %s = %s$." % (_vt(A, B), _vt(A, D), _vt(A, C)) +
                "\\\\\n"
                r"Có thể kiểm lại bằng quy tắc ba điểm: $%s = %s$ nên "
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
        debai = (r"Với ba điểm $%s$, $%s$, $%s$ bất kì, hiệu $%s - %s$ bằng "
                 r"vectơ nào sau đây?" % (O, X, Y, _vt(O, X), _vt(O, Y)))
        giai = (r"Quy tắc trừ (quy tắc hiệu): hai vectơ có \textbf{chung "
                r"điểm đầu} thì hiệu của chúng là vectơ nối hai điểm cuối, "
                r"hướng từ điểm cuối của vectơ bị trừ về điểm cuối của vectơ "
                r"đứng trước:"
                "\\\\\n"
                r"$%s - %s = %s$." % (_vt(O, X), _vt(O, Y), _vt(Y, X)) +
                "\\\\\n"
                r"Kiểm lại bằng quy tắc ba điểm: "
                r"$%s + %s = %s$ nên $%s = %s - %s$."
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
        debai = (r"Cho hình vuông $%s$, gọi $%s$ là giao điểm của hai đường "
                 r"chéo (xem hình vẽ). Trong các khẳng định sau, khẳng định "
                 r"nào \textbf{đúng}?" % (ten, O))
        giai = (r"Hai đường chéo của hình vuông cắt nhau tại trung điểm mỗi "
                r"đường, nên $%s$ là trung điểm của $%s$." % (O, A + C) +
                "\\\\\n"
                r"Suy ra $%s$ và $%s$ là hai vectơ \textbf{đối nhau} (cùng độ "
                r"dài, ngược hướng), do đó $%s + %s = \overrightarrow{0}$."
                % (_vt(O, A), _vt(O, C), _vt(O, A), _vt(O, C)) +
                "\\\\\n"
                r"Các khẳng định còn lại đều sai: $%s$ và $%s$ không cùng "
                r"phương; $%s + %s = %s \ne \overrightarrow{0}$; còn "
                r"$%s + %s + %s = 2%s \ne \overrightarrow{0}$ vì "
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
         r"tính chất \textbf{giao hoán} của phép cộng vectơ"),
        (r"$\left(%s + %s\right) + %s = %s + \left(%s + %s\right)$"
         % (a, b, c, a, b, c),
         r"tính chất \textbf{kết hợp} của phép cộng vectơ"),
        (r"$%s + %s = %s$" % (a, kh, a),
         r"vectơ-không là phần tử \textbf{trung hoà} của phép cộng vectơ"),
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
        debai = (r"Cho ba vectơ $%s$, $%s$, $%s$ tuỳ ý. Khẳng định nào sau "
                 r"đây \textbf{đúng}?" % (a, b, c))
        giai = (r"Khẳng định $%s$ chính là %s."
                % (dung.strip("$"), ten_tc) +
                "\\\\\n"
                r"Các khẳng định còn lại đều sai. Chú ý $%s - %s$ và "
                r"$%s - %s$ là hai vectơ \textbf{đối nhau} chứ không bằng "
                r"nhau, và $%s + %s = %s$ chứ không phải $%s$."
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
        huong = "cùng hướng" if k > 0 else "ngược hướng"
        huong_sai = "ngược hướng" if k > 0 else "cùng hướng"
        dung = (r"$%d%s$ %s với $%s$ và có độ dài bằng $%d\left|%s\right|$"
                % (k, a, huong, a, abs(k), a))
        nhieu = [
            r"$%d%s$ %s với $%s$ và có độ dài bằng $%d\left|%s\right|$"
            % (k, a, huong_sai, a, abs(k), a),
            r"$%d%s$ %s với $%s$ và có độ dài bằng $%d\left|%s\right|$"
            % (k, a, huong, a, abs(k) + 1, a),
            r"$%d%s$ %s với $%s$ và có độ dài bằng $\left|%s\right|$"
            % (k, a, huong_sai, a, a),
        ]
        debai = (r"Cho vectơ $%s \ne \overrightarrow{0}$. Khẳng định nào sau "
                 r"đây \textbf{đúng}?" % a)
        giai = (r"Với số thực $k \ne 0$ và vectơ $%s \ne \overrightarrow{0}$, "
                r"vectơ $k%s$ có:" % (a, a) +
                "\\\\\n"
                r"$\bullet$ \textbf{hướng}: cùng hướng với $%s$ nếu $k > 0$, "
                r"ngược hướng với $%s$ nếu $k < 0$;" % (a, a) +
                "\\\\\n"
                r"$\bullet$ \textbf{độ dài}: "
                r"$\left|k%s\right| = \left|k\right|\cdot\left|%s\right|$."
                % (a, a) +
                "\\\\\n"
                r"Ở đây $k = %d$ nên $%d%s$ %s với $%s$ và có độ dài "
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
         r"phép nhân một số với một vectơ \textbf{phân phối} đối với phép "
         r"cộng vectơ"),
        (r"$\left(k + l\right)%s = k%s + l%s$" % (a, a, a),
         r"phép nhân một số với một vectơ \textbf{phân phối} đối với phép "
         r"cộng số"),
        (r"$k\left(l%s\right) = \left(kl\right)%s$" % (a, a),
         r"tính chất \textbf{kết hợp} của phép nhân số với vectơ"),
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
        debai = (r"Cho hai vectơ $%s$, $%s$ và hai số thực $k$, $l$. Khẳng "
                 r"định nào sau đây \textbf{đúng}?" % (a, b))
        giai = (r"Khẳng định $%s$ chính là %s." % (dung.strip("$"), ten_tc) +
                "\\\\\n"
                r"Các khẳng định còn lại sai vì bỏ sót thừa số $k$ ở một số "
                r"hạng, hoặc nhầm phép cộng số thành phép nhân số, hoặc "
                r"không đổi dấu khi nhân vào hiệu.")
        cauTN += MC_SA_answer_text(debai, dung, list(SAI), giai, 0, 0, dang)
    return cauTN


def L10_C4_B9_TH045_MC_A_01(socau, dang=1):
    """Điều kiện để hai vectơ cùng phương.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"\overrightarrow{a}"
    b = r"\overrightarrow{b}"
    kh = r"\overrightarrow{0}"
    dung = (r"Tồn tại số thực $k$ sao cho $%s = k%s$" % (b, a))
    nhieu = [r"Tồn tại số thực $k > 0$ sao cho $%s = k%s$" % (b, a),
             r"$\left|%s\right| = \left|%s\right|$" % (a, b),
             r"$%s + %s = %s$" % (a, b, kh),
             r"Tồn tại số thực $k$ sao cho $%s = k%s$ và $k > 1$" % (b, a)]

    cauTN = ""
    for _ in range(socau):
        debai = (r"Cho vectơ $%s \ne %s$ và vectơ $%s$ tuỳ ý. Hai vectơ $%s$ "
                 r"và $%s$ cùng phương khi và chỉ khi điều kiện nào sau đây "
                 r"được thoả mãn?" % (a, kh, b, a, b))
        giai = (r"Điều kiện cùng phương: với $%s \ne %s$, hai vectơ $%s$ và "
                r"$%s$ cùng phương khi và chỉ khi tồn tại số thực $k$ sao cho "
                r"$%s = k%s$." % (a, kh, a, b, b, a) +
                "\\\\\n"
                r"Không được đòi $k > 0$: khi $k < 0$ hai vectơ ngược hướng "
                r"nhưng \textbf{vẫn cùng phương}. Cũng không được đòi $k > 1$."
                "\\\\\n"
                r"Điều kiện $\left|%s\right| = \left|%s\right|$ chỉ nói về độ "
                r"dài, không nói gì về phương; còn $%s + %s = %s$ là điều "
                r"kiện để hai vectơ \textbf{đối nhau}, chặt hơn hẳn."
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm "
                 r"$A%s$, $B%s$, $C%s$. Khẳng định nào sau đây \textbf{đúng}, "
                 r"từ đó suy ra ba điểm $A$, $B$, $C$ thẳng hàng?"
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$ và $%s = %s$."
                % (_vt("A", "B"), _toado(xb - xa, yb - ya),
                   _vt("A", "C"), _toado(xc - xa, yc - ya)) +
                "\\\\\n"
                r"Nhận thấy $%s = %d\cdot %s$ và $%s = %d\cdot %s$ nên "
                r"$%s = %d\,%s$."
                % (_xx4(xb - xa), k, _xx4(xc - xa),
                   _xx4(yb - ya), k, _xx4(yc - ya),
                   _vt("A", "B"), k, _vt("A", "C")) +
                "\\\\\n"
                r"Hai vectơ $%s$, $%s$ cùng phương và có chung điểm đầu $A$ "
                r"nên ba điểm $A$, $B$, $C$ thẳng hàng."
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

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm "
                 r"$A%s$, $B%s$, $C%s$."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))

        hoi_a = r"Tìm toạ độ của hai vectơ $%s$ và $%s$." % (
            _vt("A", "B"), _vt("A", "C"))
        giai_a = (r"Toạ độ vectơ bằng toạ độ điểm cuối trừ toạ độ điểm đầu:"
                  "\\\\\n"
                  r"$%s = %s$; $%s = %s$."
                  % (_vt("A", "B"), _toado(xb - xa, yb - ya),
                     _vt("A", "C"), _toado(xc - xa, yc - ya)))

        hoi_b = r"Chứng minh ba điểm $A$, $B$, $C$ thẳng hàng."
        giai_b = (r"Ta thấy $%s = %d\,%s$ vì $%s = %d\cdot %s$ và "
                  r"$%s = %d\cdot %s$."
                  % (_vt("A", "B"), k, _vt("A", "C"),
                     _xx4(xb - xa), k, _xx4(xc - xa),
                     _xx4(yb - ya), k, _xx4(yc - ya)) +
                  "\\\\\n"
                  r"Vậy $%s$ và $%s$ cùng phương, lại có chung điểm đầu $A$, "
                  r"nên ba điểm $A$, $B$, $C$ thẳng hàng."
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
            them = (r"Vì $%s$ là trung điểm $%s$ nên $%s$ và $%s$ là hai "
                    r"vectơ đối nhau, do đó $%s + %s = %s$."
                    % (I, A + B, _vt(I, A), _vt(I, B),
                       _vt(I, A), _vt(I, B), kh))
        else:
            dung = r"$%s + %s = 2%s$" % (_vt(M, A), _vt(M, B), _vt(M, I))
            nhieu = [r"$%s + %s = %s$" % (_vt(M, A), _vt(M, B), _vt(M, I)),
                     r"$%s + %s = 3%s$" % (_vt(M, A), _vt(M, B), _vt(M, I)),
                     r"$%s + %s = 2%s$" % (_vt(M, A), _vt(M, B), _vt(A, B))]
            them = (r"Với điểm $%s$ bất kì: $%s = %s + %s$ và "
                    r"$%s = %s + %s$." % (M, _vt(M, A), _vt(M, I), _vt(I, A),
                                          _vt(M, B), _vt(M, I), _vt(I, B)) +
                    "\\\\\n"
                    r"Cộng lại: $%s + %s = 2%s + \left(%s + %s\right) "
                    r"= 2%s + %s = 2%s$."
                    % (_vt(M, A), _vt(M, B), _vt(M, I), _vt(I, A), _vt(I, B),
                       _vt(M, I), kh, _vt(M, I)))

        debai = (r"Cho $%s$ là trung điểm của đoạn thẳng $%s$ và $%s$ là một "
                 r"điểm bất kì. Khẳng định nào sau đây \textbf{đúng}?"
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
            giai = (r"Tính chất trọng tâm: $%s$ là trọng tâm tam giác $%s$ "
                    r"khi và chỉ khi $%s + %s + %s = %s$."
                    % (G, ten, _vt(G, A), _vt(G, B), _vt(G, C), kh) +
                    "\\\\\n"
                    r"Thật vậy, gọi $%s$ là trung điểm $%s$ thì "
                    r"$%s + %s = 2%s$, mà $%s = -2%s$ (vì $%s$ nằm trên "
                    r"$%s$ với $%s = 2%s$), nên tổng ba vectơ bằng $%s$."
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
            giai = (r"Trọng tâm $%s$ nằm trên trung tuyến $%s$ và chia trung "
                    r"tuyến theo tỉ lệ $%s = \dfrac{2}{3}%s$, "
                    r"$%s = \dfrac{1}{3}%s$." % (G, A + I, _vt(A, G),
                                                 _vt(A, I), _vt(G, I),
                                                 _vt(A, I)) +
                    "\\\\\n"
                    r"Do đó $\left|%s\right| = 2\left|%s\right| = "
                    r"2\left|%s\right|$."
                    % (_vt(A, G), _vt(G, I), _vt(I, G)) +
                    "\\\\\n"
                    r"Các khẳng định còn lại sai: $\left|%s\right| = "
                    r"\dfrac{3}{2}\left|%s\right|$ chứ không phải gấp $3$; "
                    r"$\left|%s\right| = 2\left|%s\right|$ chứ không bằng "
                    r"nhau; và $\left|%s\right| = 3\left|%s\right|$."
                    % (_vt(A, I), _vt(A, G), _vt(G, A), _vt(G, I),
                       _vt(I, A), _vt(I, G)))

        debai = (r"Cho tam giác $%s$ có trọng tâm $%s$; gọi $%s$ là trung "
                 r"điểm của cạnh $%s$ (xem hình vẽ). Khẳng định nào sau đây "
                 r"\textbf{đúng}?" % (ten, G, I, B + C))
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
        debai = (r"Cho tam giác $%s$ có trọng tâm $%s$ và $%s$ là một điểm "
                 r"bất kì. Biết rằng $%s + %s + %s = k\,%s$ với mọi vị trí "
                 r"của điểm $%s$. Tìm số $k$."
                 % (ten, G, M, _vt(M, A), _vt(M, B), _vt(M, C),
                    _vt(M, G), M))
        giai = (r"Dùng quy tắc ba điểm, chen điểm $%s$ vào từng vectơ:" % G +
                "\\\\\n"
                r"$%s = %s + %s$; $%s = %s + %s$; $%s = %s + %s$."
                % (_vt(M, A), _vt(M, G), _vt(G, A),
                   _vt(M, B), _vt(M, G), _vt(G, B),
                   _vt(M, C), _vt(M, G), _vt(G, C)) +
                "\\\\\n"
                r"Cộng ba đẳng thức: $%s + %s + %s = 3%s + \left(%s + %s + "
                r"%s\right)$."
                % (_vt(M, A), _vt(M, B), _vt(M, C), _vt(M, G),
                   _vt(G, A), _vt(G, B), _vt(G, C)) +
                "\\\\\n"
                r"Vì $%s$ là trọng tâm nên $%s + %s + %s = "
                r"\overrightarrow{0}$."
                % (G, _vt(G, A), _vt(G, B), _vt(G, C)) +
                "\\\\\n"
                r"Vậy $%s + %s + %s = 3%s$, tức là $k = 3$."
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$ với hai vectơ đơn vị $%s$, "
                 r"$%s$, cho vectơ $%s = %s$. Khẳng định nào sau "
                 r"đây \textbf{đúng}?" % (i, j, u, _bt_ij(p, q)))
        giai = (r"Nếu $%s = x%s + y%s$ thì cặp số $\left(x;\ y\right)$ gọi "
                r"là \textbf{toạ độ} của $%s$, viết $%s = \left(x;\ y\right)$."
                % (u, i, j, u, u) +
                "\\\\\n"
                r"Ở đây hệ số của $%s$ là $%d$ và hệ số của $%s$ là $%d$, nên "
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$ với hai vectơ đơn vị $%s$, $%s$, "
                 r"cho vectơ $%s = %s$. Khẳng định nào sau đây \textbf{đúng}?"
                 % (i, j, vt, _toado(p, q)))
        giai = (r"Theo định nghĩa, $%s = \left(x;\ y\right)$ khi và chỉ khi "
                r"$%s = x%s + y%s$: hoành độ là hệ số của $%s$, tung độ là "
                r"hệ số của $%s$." % (vt, vt, i, j, i, j) +
                "\\\\\n"
                r"Vì $%s = %s$ nên $%s = %s$." % (vt, _toado(p, q), vt, _bt_ij(p, q)))
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$ với hai vectơ đơn vị $%s$, $%s$, "
                 r"toạ độ của vectơ $%s = %s$ là" % (i, j, vt, bieu_dien))
        if kieu == "dao":
            them = (r"Viết lại theo đúng thứ tự: $%s = %s$ (thứ tự các hạng tử "
                    r"trong tổng không quan trọng)." % (vt, _bt_ij(x, y)))
        elif kieu == "chi_i":
            them = (r"Không có hạng tử chứa $%s$, tức là hệ số của $%s$ bằng "
                    r"$0$: $%s = %s$." % (j, j, vt, _bt_ij(x, 0) + " + 0" + j))
        else:
            them = (r"Không có hạng tử chứa $%s$, tức là hệ số của $%s$ bằng "
                    r"$0$: $%s = 0%s + %s$." % (i, i, vt, i, _bt_ij(0, y)))
        giai = (r"Toạ độ của vectơ: hoành độ là hệ số của $%s$, tung độ là hệ "
                r"số của $%s$." % (i, j) +
                "\\\\\n" + them +
                "\\\\\n"
                r"Vậy $%s = %s$." % (vt, _toado(x, y)))
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai điểm $A%s$ và $B%s$. "
                 r"Toạ độ của vectơ $%s$ là"
                 % (_toado(xa, ya), _toado(xb, yb), _vt("A", "B")))
        giai = (r"Toạ độ của vectơ bằng toạ độ điểm cuối trừ toạ độ điểm đầu:"
                "\\\\\n"
                r"$%s = \left(x_B - x_A;\ y_B - y_A\right) = "
                r"\left(%d - \left(%d\right);\ %d - \left(%d\right)\right) "
                r"= %s$."
                % (_vt("A", "B"), xb, xa, yb, ya, _toado(u, v)) +
                "\\\\\n"
                r"Chú ý $%s = %s$ là vectơ \textbf{đối}, không được nhầm."
                % (_vt("B", "A"), _toado(-u, -v)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C4_B10_TH050_SA_A_01(socau):
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm $A%s$, $B%s$, "
                 r"$C%s$. Tìm \textbf{hoành độ} của điểm $D$ sao cho $ABCD$ "
                 r"là hình bình hành."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$ABCD$ là hình bình hành khi và chỉ khi $%s = %s$."
                % (_vt("A", "B"), _vt("D", "C")) +
                "\\\\\n"
                r"$%s = %s$; $%s = \left(%d - x_D;\ %d - y_D\right)$."
                % (_vt("A", "B"), _toado(xb - xa, yb - ya),
                   _vt("D", "C"), xc, yc) +
                "\\\\\n"
                r"Cho hai toạ độ bằng nhau: $%d - x_D = %d$ nên "
                r"$x_D = %d$; tương tự $y_D = %d$."
                % (xc, xb - xa, xd, yd) +
                "\\\\\n"
                r"Vậy $D%s$, hoành độ của $D$ bằng $%d$."
                % (_toado(xd, yd), xd))
        nhieu = _ba_nhieu4(xd, [xa + xb - xc, xb + xc - xa, -xd, xd + 1],
                           buoc=lambda t: xd + 2 * t)
        cau += MC_SA_answer_const(debai, xd, nhieu, giai, 0, 0, 2)
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai điểm $A%s$ và $B%s$. "
                 r"Độ dài của vectơ $%s$ bằng"
                 % (_toado(xa, ya), _toado(xb, yb), _vt("A", "B")))
        giai = (r"$%s = %s$." % (_vt("A", "B"), _toado(u, v)) +
                "\\\\\n"
                r"Nếu $%s = \left(x;\ y\right)$ thì "
                r"$\left|%s\right| = \sqrt{x^2 + y^2}$."
                % (r"\overrightarrow{u}", r"\overrightarrow{u}") +
                "\\\\\n"
                r"Do đó $\left|%s\right| = \sqrt{\left(%d\right)^2 + "
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai điểm $A%s$ và $B%s$. "
                 r"Tính độ dài đoạn thẳng $AB$."
                 % (_toado(xa, ya), _toado(xb, yb)))
        giai = (r"$AB = \left|%s\right|$ với $%s = %s$."
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai vectơ $%s = %s$ và "
                 r"$%s = %s$. Toạ độ của vectơ $%d%s %s %s%s$ là"
                 % (u, _toado(a1, a2), v, _toado(b1, b2), m, u, dau,
                    he_so_n, v))
        giai = (r"Nhân một số với vectơ thì nhân vào \textbf{từng} toạ độ; "
                r"cộng hai vectơ thì cộng \textbf{từng} toạ độ tương ứng."
                "\\\\\n"
                r"$%d%s = %s$; $%s%s%s = %s$."
                % (m, u, _toado(m * a1, m * a2), dau, he_so_n, v,
                   _toado(n * b1, n * b2)) +
                "\\\\\n"
                r"Cộng theo từng toạ độ: $%s$." % _toado(c1, c2))
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai vectơ $%s = %s$ và "
                 r"$%s = %s$. Tìm \textbf{hoành độ} của vectơ $%d%s - %s$."
                 % (u, _toado(a1, a2), v, _toado(b1, b2), m, u, v))
        giai = (r"$%d%s = %s$." % (m, u, _toado(m * a1, m * a2)) +
                "\\\\\n"
                r"$%d%s - %s = \left(%d - \left(%d\right);\ "
                r"%d - \left(%d\right)\right) = %s$."
                % (m, u, v, m * a1, b1, m * a2, b2,
                   _toado(c1, m * a2 - b2)) +
                "\\\\\n"
                r"Vậy hoành độ cần tìm là $%d$." % c1)
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai vectơ $%s = %s$ và "
                 r"$%s = %s$. Tích vô hướng $%s \cdot %s$ bằng"
                 % (u, _toado(a1, a2), v, _toado(b1, b2), u, v))
        giai = (r"Nếu $%s = \left(x_1;\ y_1\right)$ và "
                r"$%s = \left(x_2;\ y_2\right)$ thì "
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm $A%s$, $B%s$, "
                 r"$C%s$. Tính tích vô hướng $%s \cdot %s$."
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
        dung = r"Tam giác vuông cân tại $A$"
        nhieu = [r"Tam giác vuông tại $A$ nhưng không cân",
                 r"Tam giác cân tại $A$ nhưng không vuông",
                 r"Tam giác đều", r"Tam giác tù tại $A$"]
        # AB va AC cung do dai nen vuong can
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm $A%s$, $B%s$, "
                 r"$C%s$. Tam giác $ABC$ là tam giác gì?"
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$; $%s = %s$."
                % (_vt("A", "B"), _toado(u, v),
                   _vt("A", "C"), _toado(-v, u)) +
                "\\\\\n"
                r"Tích vô hướng: $%s \cdot %s = \left(%d\right)\cdot"
                r"\left(%d\right) + \left(%d\right)\cdot\left(%d\right) = 0$ "
                r"nên $%s \perp %s$, tam giác vuông tại $A$."
                % (_vt("A", "B"), _vt("A", "C"), u, -v, v, u,
                   _vt("A", "B"), _vt("A", "C")) +
                "\\\\\n"
                r"Độ dài: $AB = \sqrt{%d} = AC$ nên tam giác còn cân tại $A$."
                % (u * u + v * v) +
                "\\\\\n"
                r"Vậy tam giác $ABC$ vuông cân tại $A$.")
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

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm $A%s$, $B%s$, "
                 r"$C%s$." % (_toado(xa, ya), _toado(xb, yb),
                              _toado(xc, yc)))

        hoi_a = r"Tìm toạ độ của hai vectơ $%s$ và $%s$." % (
            _vt("A", "B"), _vt("A", "C"))
        giai_a = (r"$%s = %s$; $%s = %s$."
                  % (_vt("A", "B"), _toado(u, v),
                     _vt("A", "C"), _toado(-v, u)))

        hoi_b = r"Chứng minh tam giác $ABC$ vuông tại $A$."
        giai_b = (r"$%s \cdot %s = \left(%d\right)\left(%d\right) + "
                  r"\left(%d\right)\left(%d\right) = 0$."
                  % (_vt("A", "B"), _vt("A", "C"), u, -v, v, u) +
                  "\\\\\n"
                  r"Tích vô hướng bằng $0$ nên $%s \perp %s$, tức là tam "
                  r"giác $ABC$ vuông tại $A$."
                  % (_vt("A", "B"), _vt("A", "C")))

        hoi_c = r"Tính diện tích tam giác $ABC$."
        giai_c = (r"$AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} = %d$ "
                  r"và $AC = %d$ (tính tương tự)." % (u, v, r, r) +
                  "\\\\\n"
                  r"Tam giác vuông tại $A$ nên "
                  r"$S = \dfrac{1}{2}\cdot AB \cdot AC = "
                  r"\dfrac{1}{2}\cdot %d \cdot %d = %s$ (đơn vị diện tích)."
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
        debai = (r"Một ca nô xuất phát từ vị trí $A%s$ trên mặt phẳng toạ độ "
                 r"$Oxy$ (đơn vị trên mỗi trục là ki-lô-mét) và chuyển động "
                 r"thẳng đều với vectơ vận tốc $\overrightarrow{v} = %s$ "
                 r"(đơn vị: km/h). Sau $%d$ giờ, ca nô ở vị trí nào?"
                 % (_toado(x0, y0), _toado(vx, vy), t))
        giai = (r"Chuyển động thẳng đều nên độ dịch chuyển sau $%d$ giờ là "
                r"$%d\overrightarrow{v} = %s$."
                % (t, t, _toado(t * vx, t * vy)) +
                "\\\\\n"
                r"Gọi $B$ là vị trí sau $%d$ giờ thì $%s = %d\overrightarrow{v}$, "
                r"nên toạ độ của $B$ bằng toạ độ của $A$ cộng với độ dịch "
                r"chuyển:" % (t, _vt("A", "B"), t) +
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho tam giác $ABC$ với "
                 r"$A%s$, $B%s$, $C%s$. Diện tích tam giác $ABC$ bằng"
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$%s = %s$; $%s = %s$."
                % (_vt("A", "B"), _toado(u1, u2),
                   _vt("A", "C"), _toado(v1, v2)) +
                "\\\\\n"
                r"Với $%s = \left(x_1;\ y_1\right)$, $%s = "
                r"\left(x_2;\ y_2\right)$ thì diện tích tam giác bằng"
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

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho tam giác $ABC$ với "
                 r"$A%s$, $B%s$, $C%s$."
                 % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))

        hoi_a = r"Tính độ dài hai cạnh $AB$ và $AC$."
        giai_a = (r"$%s = %s$ nên $AB = \sqrt{\left(%d\right)^2 + "
                  r"\left(%d\right)^2} = %d$."
                  % (_vt("A", "B"), _toado(u, v), u, v, r) +
                  "\\\\\n"
                  r"$%s = %s$ nên $AC = \sqrt{\left(%d\right)^2 + "
                  r"\left(%d\right)^2} = %d$."
                  % (_vt("A", "C"), _toado(-v, u), -v, u, r))

        hoi_b = r"Tính số đo góc $\widehat{BAC}$."
        giai_b = (r"$\cos\widehat{BAC} = \dfrac{%s \cdot %s}"
                  r"{\left|%s\right|\cdot\left|%s\right|} = "
                  r"\dfrac{0}{%d\cdot %d} = 0$."
                  % (_vt("A", "B"), _vt("A", "C"), _vt("A", "B"),
                     _vt("A", "C"), r, r) +
                  "\\\\\n"
                  r"Vậy $\widehat{BAC} = 90^{\circ}$.")

        hoi_c = r"Tính diện tích tam giác $ABC$."
        giai_c = (r"Tam giác vuông tại $A$ nên "
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
        return r"$%s$, $%s$, $%s$ thẳng hàng và $%s$ nằm giữa nên góc bằng $180^{\circ}$" % (P, Q, R, Q)
    if g == 0:
        return r"hai vectơ cùng hướng nên góc bằng $0^{\circ}$"
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
        return (r"Hai vectơ $%s$ và $%s$ có chung điểm đầu $%s$ nên góc giữa "
                r"chúng là góc tạo bởi hai tia $%s%s$, $%s%s$: %s."
                % (u, v, v1[0], v1[0], v1[1], v2[0], v2[1],
                   _goc_ten(v1[1], v1[0], v2[1], g)))
    if g in (0, 180):
        return (r"Hai vectơ $%s$ và $%s$ %s nên góc giữa chúng bằng $%d^{\circ}$."
                % (u, v, r"\textbf{cùng hướng}" if g == 0 else r"\textbf{ngược hướng}", g))
    if v1[1] == v2[1]:
        X = v1[1]
        return (r"Hai vectơ chung \textbf{điểm cuối} $%s$. Đổi hướng cả hai vectơ "
                r"thì góc giữa chúng không đổi: góc giữa $%s$, $%s$ bằng góc "
                r"giữa $%s$, $%s$ - hai vectơ này chung điểm đầu $%s$."
                % (X, u, v, _vt(X, v1[0]), _vt(X, v2[0]), X) +
                "\\\\\n" + r"Do đó góc cần tìm: %s." % _goc_ten(v1[0], X, v2[0], g))
    if v1[1] == v2[0] or v2[1] == v1[0]:
        # noi duoi: doi huong vecto ket thuc tai diem chung
        if v1[1] == v2[0]:
            X, w1, w2 = v1[1], (v1[1], v1[0]), v2
        else:
            X, w1, w2 = v1[0], v1, (v2[1], v2[0])
        g2 = 180 - g
        doi = u if w1 != v1 else v
        return (r"Hai vectơ chưa chung điểm đầu. Đổi hướng $%s$ (được một vectơ "
                r"có điểm đầu $%s$) thì góc giữa hai vectơ đổi thành phần bù của nó."
                % (doi, X) + "\\\\\n" +
                r"Góc giữa $%s$ và $%s$ là %s, nên góc cần tìm bằng "
                r"$180^{\circ} - %d^{\circ} = %d^{\circ}$."
                % (_vt(*w1), _vt(*w2), _goc_ten(w1[1], X, w2[1], g2), g2, g))
    w, gg = cung_phuong_tu(v1[0], v2)
    if w:
        gw = _goc2(TD, v1, w)
        return (r"Hai vectơ chưa chung điểm đầu. Vectơ $%s$ %s với $%s$ (chung "
                r"điểm đầu $%s$ với $%s$)" % (v, "cùng hướng" if gg == 0 else "ngược hướng",
                                              _vt(*w), v1[0], u) +
                (r" nên góc cần tìm bằng góc giữa $%s$, $%s$: %s."
                 % (u, _vt(*w), _goc_ten(v1[1], v1[0], w[1], g)) if gg == 0 else
                 r" nên góc cần tìm bằng $180^{\circ}$ trừ góc giữa $%s$, $%s$, "
                 r"tức là $180^{\circ} - %d^{\circ} = %d^{\circ}$." % (u, _vt(*w), gw, g)))
    w, gg = cung_phuong_tu(v2[0], v1)
    if w:
        gw = _goc2(TD, w, v2)
        return (r"Hai vectơ chưa chung điểm đầu. Vectơ $%s$ %s với $%s$ (chung "
                r"điểm đầu $%s$ với $%s$)" % (u, "cùng hướng" if gg == 0 else "ngược hướng",
                                              _vt(*w), v2[0], v) +
                (r" nên góc cần tìm bằng góc giữa $%s$, $%s$: %s."
                 % (_vt(*w), v, _goc_ten(w[1], v2[0], v2[1], g)) if gg == 0 else
                 r" nên góc cần tìm bằng $180^{\circ}$ trừ góc giữa $%s$, $%s$, "
                 r"tức là $180^{\circ} - %d^{\circ} = %d^{\circ}$." % (_vt(*w), v, gw, g)))
    if g == 90:
        return (r"Hai đường thẳng $%s%s$ và $%s%s$ vuông góc với nhau nên góc giữa "
                r"hai vectơ $%s$, $%s$ bằng $90^{\circ}$." % (v1[0], v1[1], v2[0], v2[1], u, v))
    if _sau:
        # thay v2 bang vecto cung huong co ten khac roi giai lai
        for Y in diem:
            for Z in diem:
                w = (Y, Z)
                if Y == Z or w == v2 or _goc2(TD, v2, w) != 0:
                    continue
                phu = _loi_giai_goc(TD, v1, w, g, _sau=False)
                if "dời" not in phu:
                    return (r"Vectơ $%s$ cùng hướng với $%s$ nên góc giữa $%s$, $%s$ "
                            r"bằng góc giữa $%s$, $%s$." % (v, _vt(*w), u, v, u, _vt(*w)) +
                            "\\\\\n" + phu)
    return (r"Hai vectơ chưa chung điểm đầu: dời $%s$ về điểm đầu $%s$ rồi đọc "
            r"góc tạo thành, được $%d^{\circ}$." % (v, v1[0], g))


def _cau_goc_vecto(socau, dang, TD, hinh, ten_hinh, CAP, GOC):
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
        debai = (r"Cho %s như hình vẽ. Góc giữa hai vectơ $%s$ và $%s$ bằng"
                 % (ten_hinh, _vt(*v1), _vt(*v2)))
        giai = _loi_giai_goc(TD, v1, v2, g)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


_TEN_TG = r"tam giác đều $ABC$ có $H$ là trung điểm của $BC$"
_TEN_HV = r"hình vuông $ABCD$ có $O$ là giao điểm hai đường chéo"


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
            debai = (r"Cho hai vectơ $%s$, $%s$ khác vectơ $\overrightarrow{0}$ "
                     r"thoả mãn $%s = %d%s$. Góc giữa hai vectơ $%s$ và $%s$ bằng"
                     % (a, b, a, t, b, a, b))
            giai = (r"Vì $%s = %d%s$ với $%d %s 0$ nên $%s$ và $%s$ "
                    % (a, t, b, t, ">" if t > 0 else "<", a, b) +
                    (r"\textbf{cùng hướng}" if t > 0 else r"\textbf{ngược hướng}") +
                    r", do đó góc giữa chúng bằng $%d^{\circ}$." % g)
        else:
            v1, v2 = CAP_TD[t]
            h1 = VI_TRI[v1[1]] - VI_TRI[v1[0]]
            h2 = VI_TRI[v2[1]] - VI_TRI[v2[0]]
            g = 0 if h1 * h2 > 0 else 180
            debai = (r"Cho đoạn thẳng $AB$ có trung điểm $M$. Góc giữa hai vectơ "
                     r"$%s$ và $%s$ bằng" % (_vt(*v1), _vt(*v2)))
            giai = (r"Hai vectơ chung điểm đầu $%s$; ba điểm $A$, $M$, $B$ thẳng "
                    r"hàng nên $%s$ và $%s$ " % (v1[0], _vt(*v1), _vt(*v2)) +
                    (r"\textbf{cùng hướng}" if g == 0 else r"\textbf{ngược hướng}") +
                    r", do đó góc giữa chúng bằng $%d^{\circ}$." % g)
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
        debai = (r"Cho hai vectơ $%s$, $%s$ có $\left|%s\right| = %d$, "
                 r"$\left|%s\right| = %d$ và góc giữa chúng bằng "
                 r"$%d^{\circ}$. Tính $%s \cdot %s$."
                 % (a, b, a, p, b, q, goc, a, b))
        giai = (r"Định nghĩa tích vô hướng:"
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
        debai = (r"Cho hai vectơ $%s$, $%s$ có $\left|%s\right| = %d$, "
                 r"$\left|%s\right| = %d$ và góc giữa chúng bằng "
                 r"$%d^{\circ}$. Tính $%s \cdot %s$."
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
         r"tích vô hướng có tính \textbf{giao hoán}"),
        (r"$%s \cdot \left(%s + %s\right) = %s \cdot %s + %s \cdot %s$"
         % (a, b, c, a, b, a, c),
         r"tích vô hướng \textbf{phân phối} đối với phép cộng vectơ"),
        (r"$%s \cdot %s = \left|%s\right|^{2}$" % (a, a, a),
         r"bình phương vô hướng của một vectơ bằng bình phương độ dài của nó"),
    ]
    SAI = [
        r"$%s \cdot %s = -\,%s \cdot %s$" % (a, b, b, a),
        r"$%s \cdot \left(%s + %s\right) = %s \cdot %s \cdot %s$"
        % (a, b, c, a, b, c),
        r"$%s \cdot %s = \left|%s\right|$" % (a, a, a),
        r"$%s \cdot %s = 0$ thì $%s = \overrightarrow{0}$ hoặc "
        r"$%s = \overrightarrow{0}$" % (a, b, a, b),
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
        debai = (r"Cho ba vectơ $%s$, $%s$, $%s$ tuỳ ý. Khẳng định nào sau "
                 r"đây \textbf{đúng}?" % (a, b, c))
        giai = (r"Khẳng định $%s$ chính là %s." % (dung.strip("$"), ten_tc) +
                "\\\\\n"
                r"Đặc biệt lưu ý khẳng định ``$%s \cdot %s = 0$ thì $%s$ hoặc "
                r"$%s$ bằng $\overrightarrow{0}$'' là \textbf{sai}: tích vô "
                r"hướng bằng $0$ còn xảy ra khi hai vectơ \textbf{vuông góc} "
                r"với nhau." % (a, b, a, b))
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
        debai = (r"Trên mặt phẳng, chất điểm $A$ chịu tác dụng của ba lực "
                 r"$\overrightarrow{F_1}$, $\overrightarrow{F_2}$, "
                 r"$\overrightarrow{F_3}$ và ở trạng thái cân bằng. Biết "
                 r"$\left|\overrightarrow{F_1}\right| = %d\ \text{N}$, "
                 r"$\left|\overrightarrow{F_2}\right| = %d\ \text{N}$ và góc "
                 r"giữa hai vectơ $\overrightarrow{F_1}$, "
                 r"$\overrightarrow{F_2}$ bằng $60^{\circ}$. Tính độ lớn của "
                 r"lực $\overrightarrow{F_3}$." % (p, q))
        giai = (r"Chất điểm cân bằng nên $\overrightarrow{F_1} + "
                r"\overrightarrow{F_2} + \overrightarrow{F_3} = "
                r"\overrightarrow{0}$, suy ra $\overrightarrow{F_3} = "
                r"-\left(\overrightarrow{F_1} + \overrightarrow{F_2}\right)$ "
                r"và do đó $\left|\overrightarrow{F_3}\right| = "
                r"\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|$."
                "\\\\\n"
                r"Bình phương vô hướng:"
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
                r"Vậy $\left|\overrightarrow{F_3}\right| = \sqrt{%d} = "
                r"%d\ \text{N}$." % (k * k, k))
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

        debai = (r"Một chất điểm $A$ chịu tác dụng của ba lực "
                 r"$\overrightarrow{F_1}$, $\overrightarrow{F_2}$, "
                 r"$\overrightarrow{F_3}$ và ở trạng thái cân bằng. Biết "
                 r"$\left|\overrightarrow{F_1}\right| = %d\ \text{N}$, "
                 r"$\left|\overrightarrow{F_2}\right| = %d\ \text{N}$ và góc "
                 r"giữa $\overrightarrow{F_1}$, $\overrightarrow{F_2}$ bằng "
                 r"$60^{\circ}$." % (p, q))

        hoi_a = (r"Tính tích vô hướng $\overrightarrow{F_1} \cdot "
                 r"\overrightarrow{F_2}$.")
        giai_a = (r"$\overrightarrow{F_1} \cdot \overrightarrow{F_2} = "
                  r"\left|\overrightarrow{F_1}\right|\cdot"
                  r"\left|\overrightarrow{F_2}\right|\cdot\cos 60^{\circ} = "
                  r"%d\cdot %d\cdot\dfrac{1}{2} = %s$." % (p, q, tich_tex))

        hoi_b = (r"Chứng tỏ rằng $\overrightarrow{F_3} = "
                 r"-\left(\overrightarrow{F_1} + "
                 r"\overrightarrow{F_2}\right)$.")
        giai_b = (r"Chất điểm ở trạng thái cân bằng nghĩa là tổng các lực "
                  r"tác dụng lên nó bằng vectơ-không:"
                  "\\\\\n"
                  r"$\overrightarrow{F_1} + \overrightarrow{F_2} + "
                  r"\overrightarrow{F_3} = \overrightarrow{0}$."
                  "\\\\\n"
                  r"Chuyển vế: $\overrightarrow{F_3} = "
                  r"-\left(\overrightarrow{F_1} + "
                  r"\overrightarrow{F_2}\right)$.")

        hoi_c = (r"Tính độ lớn của lực $\overrightarrow{F_3}$.")
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
                  r"Vậy $\left|\overrightarrow{F_3}\right| = \sqrt{%d} = "
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

        debai = (r"Cho tam giác $ABC$ và điểm $M$ nằm trên cạnh $BC$ sao cho "
                 r"$%s = %s\,%s$ (xem hình vẽ). Hãy phân tích $%s$ theo hai "
                 r"vectơ $%s$ và $%s$."
                 % (_vt("B", "M"), _ps(tu, mau), _vt("B", "C"),
                    _vt("A", "M"), _vt("A", "B"), _vt("A", "C")))
        giai = (r"Dùng quy tắc ba điểm: $%s = %s + %s$."
                % (_vt("A", "M"), _vt("A", "B"), _vt("B", "M")) +
                "\\\\\n"
                r"Mà $%s = %s\,%s$ và $%s = %s - %s$, nên"
                % (_vt("B", "M"), _ps(tu, mau), _vt("B", "C"),
                   _vt("B", "C"), _vt("A", "C"), _vt("A", "B")) +
                "\\\\\n"
                r"$%s = %s + %s\left(%s - %s\right) = "
                r"\left(1 - %s\right)%s + %s\,%s$."
                % (_vt("A", "M"), _vt("A", "B"), _ps(tu, mau),
                   _vt("A", "C"), _vt("A", "B"), _ps(tu, mau),
                   _vt("A", "B"), _ps(tu, mau), _vt("A", "C")) +
                "\\\\\n"
                r"Vậy $%s = %s\,%s + %s\,%s$."
                % (_vt("A", "M"), hs_ab, _vt("A", "B"),
                   hs_ac, _vt("A", "C")) +
                "\\\\\n"
                r"Chú ý tổng hai hệ số luôn bằng $1$ vì $M$ nằm trên đường "
                r"thẳng $BC$.")
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

        debai = (r"Cho tam giác $%s$ có trọng tâm $%s$; gọi $%s$ là trung "
                 r"điểm của cạnh $%s$ (xem hình vẽ)." % (ten, G, I, B + C))

        hoi_a = r"Chứng minh $%s + %s = 2%s$." % (_vt(A, B), _vt(A, C),
                                                  _vt(A, I))
        giai_a = (r"Vì $%s$ là trung điểm $%s$ nên $%s + %s = %s$." %
                  (I, B + C, _vt(I, B), _vt(I, C), kh) +
                  "\\\\\n"
                  r"Dùng quy tắc ba điểm: $%s = %s + %s$ và $%s = %s + %s$."
                  % (_vt(A, B), _vt(A, I), _vt(I, B),
                     _vt(A, C), _vt(A, I), _vt(I, C)) +
                  "\\\\\n"
                  r"Cộng lại: $%s + %s = 2%s + \left(%s + %s\right) = 2%s$."
                  % (_vt(A, B), _vt(A, C), _vt(A, I), _vt(I, B),
                     _vt(I, C), _vt(A, I)))

        hoi_b = r"Chứng minh $%s = \dfrac{1}{3}\left(%s + %s\right)$." % (
            _vt(A, G), _vt(A, B), _vt(A, C))
        giai_b = (r"Trọng tâm $%s$ nằm trên trung tuyến $%s$ với "
                  r"$%s = \dfrac{2}{3}%s$." % (G, A + I, _vt(A, G), _vt(A, I)) +
                  "\\\\\n"
                  r"Theo ý trên $%s = \dfrac{1}{2}\left(%s + %s\right)$, nên"
                  % (_vt(A, I), _vt(A, B), _vt(A, C)) +
                  "\\\\\n"
                  r"$%s = \dfrac{2}{3}\cdot\dfrac{1}{2}\left(%s + %s\right) "
                  r"= \dfrac{1}{3}\left(%s + %s\right)$."
                  % (_vt(A, G), _vt(A, B), _vt(A, C),
                     _vt(A, B), _vt(A, C)))

        hoi_c = r"Chứng minh $%s + %s + %s = %s$." % (
            _vt(G, A), _vt(G, B), _vt(G, C), kh)
        giai_c = (r"Từ ý b) ta có $%s = \dfrac{1}{3}\left(%s + %s\right)$, "
                  r"tức là $3%s = %s + %s$."
                  % (_vt(A, G), _vt(A, B), _vt(A, C),
                     _vt(A, G), _vt(A, B), _vt(A, C)) +
                  "\\\\\n"
                  r"Mặt khác $%s = %s + %s$ và $%s = %s + %s$."
                  % (_vt(A, B), _vt(A, G), _vt(G, B),
                     _vt(A, C), _vt(A, G), _vt(G, C)) +
                  "\\\\\n"
                  r"Thay vào: $3%s = 2%s + %s + %s$, suy ra "
                  r"$%s = %s + %s$."
                  % (_vt(A, G), _vt(A, G), _vt(G, B), _vt(G, C),
                     _vt(A, G), _vt(G, B), _vt(G, C)) +
                  "\\\\\n"
                  r"Mà $%s = -%s$, nên $%s + %s + %s = %s$."
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

        debai = (r"Cho hình bình hành $%s$ có hai đường chéo cắt nhau tại "
                 r"$%s$ (xem hình vẽ)." % (ten, O))

        ds_abcd = (
            # a) NB - nhắc lại một tính chất
            [
                (r"{\True $%s = %s$}" % (_vt(A, B), _vt(D, C)),
                 r"Đúng. Trong hình bình hành, $%s$ song song và bằng $%s$, "
                 r"lại cùng hướng, nên hai vectơ bằng nhau."
                 % (A + B, D + C)),
                (r"{$%s = %s$}" % (_vt(A, B), _vt(C, D)),
                 r"Sai. $%s$ và $%s$ cùng độ dài nhưng \textbf{ngược hướng}, "
                 r"chúng là hai vectơ đối nhau." % (_vt(A, B), _vt(C, D))),
            ],
            # b) TH - thay vào đúng một quy tắc
            [
                (r"{\True $%s + %s = %s$}" % (_vt(A, B), _vt(A, D), _vt(A, C)),
                 r"Đúng. Đây chính là quy tắc hình bình hành: tổng hai vectơ "
                 r"cùng xuất phát từ $%s$ là vectơ đường chéo xuất phát từ "
                 r"$%s$." % (A, A)),
                (r"{$%s + %s = %s$}" % (_vt(A, B), _vt(A, D), _vt(B, D)),
                 r"Sai. $%s$ là vectơ \textbf{hiệu} $%s - %s$, không phải "
                 r"tổng." % (_vt(B, D), _vt(A, D), _vt(A, B))),
            ],
            # c) VD - phải dùng được tính chất giao điểm hai đường chéo
            [
                (r"{\True $%s + %s = %s$}" % (_vt(O, A), _vt(O, C), kh),
                 r"Đúng. Hai đường chéo của hình bình hành cắt nhau tại "
                 r"trung điểm mỗi đường nên $%s$ là trung điểm $%s$; do đó "
                 r"$%s$ và $%s$ là hai vectơ đối nhau."
                 % (O, A + C, _vt(O, A), _vt(O, C))),
                (r"{$%s + %s = %s$}" % (_vt(O, A), _vt(O, B), kh),
                 r"Sai. $%s$ là trung điểm của $%s$ chứ không phải của $%s$, "
                 r"nên $%s$ và $%s$ không đối nhau."
                 % (O, A + C, A + B, _vt(O, A), _vt(O, B))),
            ],
            # d) VDC - phải tự ghép hai quy tắc, không có công thức sẵn
            [
                (r"{\True $%s + %s + %s + %s = %s$}"
                 % (_vt(A, B), _vt(A, D), _vt(C, B), _vt(C, D), kh),
                 r"Đúng. Theo quy tắc hình bình hành, $%s + %s = %s$ và "
                 r"$%s + %s = %s$."
                 % (_vt(A, B), _vt(A, D), _vt(A, C),
                    _vt(C, B), _vt(C, D), _vt(C, A)) +
                 "\\\\\n"
                 r"Mà $%s$ và $%s$ là hai vectơ đối nhau nên tổng bằng $%s$."
                 % (_vt(A, C), _vt(C, A), kh)),
                (r"{$%s + %s + %s + %s = 2%s$}"
                 % (_vt(A, B), _vt(A, D), _vt(C, B), _vt(C, D), _vt(A, C)),
                 r"Sai. Tổng bằng $%s + %s = %s$, không phải $2%s$."
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

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm $A%s$, $B%s$, "
                 r"$C%s$." % (_toado(xa, ya), _toado(xb, yb),
                              _toado(xc, yc)))

        ds_abcd = (
            # a) NB - nhắc lại một công thức
            [
                (r"{\True $%s = %s$}" % (_vt("A", "B"), _toado(u, v)),
                 r"Đúng. Toạ độ vectơ bằng toạ độ điểm cuối trừ toạ độ điểm "
                 r"đầu: $%s = \left(%d - \left(%d\right);\ %d - "
                 r"\left(%d\right)\right) = %s$."
                 % (_vt("A", "B"), xb, xa, yb, ya, _toado(u, v))),
                (r"{$%s = %s$}" % (_vt("A", "B"), _toado(-u, -v)),
                 r"Sai. $%s$ mới là vectơ $%s$; lấy điểm đầu trừ điểm cuối "
                 r"là ngược." % (_toado(-u, -v), _vt("B", "A"))),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True $AB = %d$}" % r,
                 r"Đúng. $AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} "
                 r"= \sqrt{%d} = %d$." % (u, v, u * u + v * v, r)),
                (r"{$AB = %d$}" % (abs(u) + abs(v)),
                 r"Sai. $%d$ là tổng hai toạ độ chứ không phải độ dài; "
                 r"$AB = \sqrt{%d} = %d$."
                 % (abs(u) + abs(v), u * u + v * v, r)),
            ],
            # c) VD - phải tính được tích vô hướng mới kết luận được
            [
                (r"{\True Tam giác $ABC$ vuông tại $A$}",
                 r"Đúng. $%s = %s$, $%s = %s$ nên "
                 r"$%s \cdot %s = \left(%d\right)\left(%d\right) + "
                 r"\left(%d\right)\left(%d\right) = 0$."
                 % (_vt("A", "B"), _toado(u, v), _vt("A", "C"),
                    _toado(-v, u), _vt("A", "B"), _vt("A", "C"),
                    u, -v, v, u) +
                 "\\\\\n"
                 r"Tích vô hướng bằng $0$ nên hai vectơ vuông góc."),
                (r"{Tam giác $ABC$ vuông tại $B$}",
                 r"Sai. Tính $%s \cdot %s$ thì được $0$, nên góc vuông ở "
                 r"đỉnh $A$ chứ không phải đỉnh $B$."
                 % (_vt("A", "B"), _vt("A", "C"))),
            ],
            # d) VDC - phải tự nghĩ ra cách, không có công thức sẵn
            [
                (r"{\True Diện tích tam giác $ABC$ bằng $%s$}" % _xx4(S),
                 r"Đúng. Tam giác vuông tại $A$ và $AB = AC = %d$ nên"
                 "\\\\\n"
                 r"$S = \dfrac{1}{2}\cdot AB\cdot AC = "
                 r"\dfrac{1}{2}\cdot %d\cdot %d = %s$." % (r, r, r, _xx4(S))),
                (r"{Diện tích tam giác $ABC$ bằng $%d$}" % (r * r),
                 r"Sai. $%d$ là tích $AB \cdot AC$; diện tích tam giác vuông "
                 r"bằng \textbf{một nửa} tích hai cạnh góc vuông, tức là "
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

def L10_C4_B10_VD054_SA_A_01(socau):
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho tam giác $DBC$ với "
                 r"$D%s$, $B%s$, $C%s$. Gọi $A$ là trung điểm của $BC$. "
                 r"Tính độ dài trung tuyến $DA$."
                 % (_toado(xd, yd), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"Trung điểm $A$ của $BC$ có toạ độ "
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
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
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
        debai = (r"Một ca nô xuất phát từ vị trí $A%s$ trên mặt phẳng toạ độ "
                 r"$Oxy$ (đơn vị trên mỗi trục là ki-lô-mét) và chuyển động "
                 r"thẳng đều với vectơ vận tốc $\overrightarrow{v} = %s$ "
                 r"(đơn vị: km/h). Tìm \textbf{hoành độ} vị trí của ca nô "
                 r"sau $%d$ giờ." % (_toado(x0, y0), _toado(vx, vy), t))
        giai = (r"Độ dịch chuyển sau $%d$ giờ là $%d\overrightarrow{v} = %s$."
                % (t, t, _toado(t * vx, t * vy)) +
                "\\\\\n"
                r"Hoành độ vị trí mới: $%d + %d\cdot\left(%d\right) = %d$."
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho tam giác $ABC$ với "
                 r"$A%s$, $B%s$, $C%s$. Tính diện tích tam giác $ABC$."
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
        debai = (r"Chất điểm $A$ chịu tác dụng của ba lực "
                 r"$\overrightarrow{F_1}$, $\overrightarrow{F_2}$, "
                 r"$\overrightarrow{F_3}$ và ở trạng thái cân bằng. Biết "
                 r"$\left|\overrightarrow{F_1}\right| = %d\ \text{N}$, "
                 r"$\left|\overrightarrow{F_2}\right| = %d\ \text{N}$, góc "
                 r"giữa $\overrightarrow{F_1}$ và $\overrightarrow{F_2}$ "
                 r"bằng $60^{\circ}$. Tính $\left|\overrightarrow{F_3}\right|$ "
                 r"(đơn vị: N)." % (p, q))
        giai = (r"Cân bằng nên $\overrightarrow{F_3} = "
                r"-\left(\overrightarrow{F_1} + \overrightarrow{F_2}\right)$, "
                r"do đó $\left|\overrightarrow{F_3}\right| = "
                r"\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|$."
                "\\\\\n"
                r"$\left|\overrightarrow{F_1} + \overrightarrow{F_2}\right|^2 "
                r"= %d^2 + %d^2 + 2\cdot %d\cdot %d\cdot\cos 60^{\circ} = %d$."
                % (p, q, p, q, p * p + q * q + p * q) +
                "\\\\\n"
                r"Vậy $\left|\overrightarrow{F_3}\right| = \sqrt{%d} = %d$."
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
    BO = [("trung điểm của cạnh $BC$", "M", 2,
           r"$M$ là trung điểm $BC$ nên $\overrightarrow{AM} = "
           r"\dfrac{1}{2}\left(\overrightarrow{AB} + "
           r"\overrightarrow{AC}\right)$."),
          ("trọng tâm của tam giác $ABC$", "G", 3,
           r"$G$ là trọng tâm nên $\overrightarrow{AG} = "
           r"\dfrac{2}{3}\overrightarrow{AI}$ với $I$ là trung điểm $BC$; "
           r"mà $\overrightarrow{AI} = \dfrac{1}{2}\left(\overrightarrow{AB} "
           r"+ \overrightarrow{AC}\right)$, nên $\overrightarrow{AG} = "
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
        debai = (r"Cho tam giác $ABC$ và điểm $%s$ là %s. Biết "
                 r"$\overrightarrow{A%s} = \dfrac{1}{n}\left("
                 r"\overrightarrow{AB} + \overrightarrow{AC}\right)$. "
                 r"Tìm số nguyên dương $n$." % (ten, mo_ta, ten))
        giai = ly_do + "\\\\\n" + r"Vậy $n = %d$." % kq
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

        debai = (r"Trên mặt phẳng toạ độ $Oxy$ (đơn vị trên mỗi trục là "
                 r"ki-lô-mét), một ca nô xuất phát từ vị trí $A%s$ và chuyển "
                 r"động thẳng đều với vectơ vận tốc $\overrightarrow{v} = %s$ "
                 r"(đơn vị: km/h)." % (_toado(x0, y0), _toado(vx, vy)))

        hoi_a = r"Tính tốc độ của ca nô."
        giai_a = (r"Tốc độ là độ lớn của vectơ vận tốc:"
                  "\\\\\n"
                  r"$\left|\overrightarrow{v}\right| = "
                  r"\sqrt{\left(%d\right)^2 + \left(%d\right)^2} = "
                  r"\sqrt{%d} = %d$ (km/h)."
                  % (vx, vy, vx * vx + vy * vy, r))

        hoi_b = r"Tìm toạ độ vị trí $B$ của ca nô sau $%d$ giờ." % t
        giai_b = (r"Chuyển động thẳng đều nên độ dịch chuyển sau $%d$ giờ là "
                  r"$%s = %d\overrightarrow{v} = %s$."
                  % (t, _vt("A", "B"), t, _toado(t * vx, t * vy)) +
                  "\\\\\n"
                  r"Toạ độ $B$ bằng toạ độ $A$ cộng độ dịch chuyển:"
                  "\\\\\n"
                  r"$B\left(%d + %d;\ %d + %d\right) = B%s$."
                  % (x0, t * vx, y0, t * vy, _toado(x1, y1)))

        hoi_c = r"Tính quãng đường ca nô đi được sau $%d$ giờ." % t
        giai_c = (r"Ca nô chạy thẳng đều nên quãng đường bằng tốc độ nhân "
                  r"thời gian:"
                  "\\\\\n"
                  r"$s = %d \cdot %d = %d$ (km)." % (r, t, r * t) +
                  "\\\\\n"
                  r"Kiểm tra lại bằng độ dài $AB$: "
                  r"$AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2} = %d$ "
                  r"(km), đúng bằng kết quả trên."
                  % (t * vx, t * vy, r * t))

        ds_abcd = [(hoi_a, r"%d\ \text{km/h}" % r, giai_a),
                   (hoi_b, r"B\left(%d;\ %d\right)" % (x1, y1), giai_b),
                   (hoi_c, r"%d\ \text{km}" % (r * t), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN
