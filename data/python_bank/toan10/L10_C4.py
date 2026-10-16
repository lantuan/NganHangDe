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
        debai = (r"Cho %s như hình vẽ. Góc giữa hai vectơ $%s$ và $%s$ bằng"
                 % (ten_hinh, _vt(*v1), _vt(*v2)))
        giai = _loi_giai_goc(TD, v1, v2, g)
        if tra_loi_ngan:
            debai = (r"Cho %s như hình vẽ. Góc giữa hai vectơ $%s$ và $%s$ bằng bao nhiêu độ?"
                     % (ten_hinh, _vt(*v1), _vt(*v2)))
            cauTN += MC_SA_answer_const(debai, str(g), [str(x) for x in (uu_tien + con)[:3]], giai, hinh, 0, dang)
            continue
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
        ten_hinh = {"hbh": "hình bình hành", "hcn": "hình chữ nhật", "thoi": "hình thoi", "vuong": "hình vuông"}[kieu]
        return dict(kieu=kieu, P=P, canh=[(A, B), (B, C), (C, D), (D, A), (A, C), (B, D)], tam=o,
                    mo=r"Cho %s $%s$ có hai đường chéo cắt nhau tại $%s$ (xem hình vẽ)." % (ten_hinh, ten, o),
                    da_giac=list(ten))
    if kieu == "luc_giac":
        ten = "ABCDEF"
        P = {ten[i]: (2 * math.cos(math.pi / 3 * i), 2 * math.sin(math.pi / 3 * i)) for i in range(6)}
        P["O"] = (0.0, 0.0)
        canh = [(ten[i], ten[(i + 1) % 6]) for i in range(6)] + [("A", "D"), ("B", "E"), ("C", "F")]
        return dict(kieu=kieu, P=P, canh=canh, tam="O", da_giac=list(ten),
                    mo=r"Cho lục giác đều $ABCDEF$ có tâm $O$ (xem hình vẽ).")
    if kieu == "tg_trung_diem":
        A, B, C = "ABC"
        M, N, Q = random.choice([("M", "N", "P"), ("D", "E", "F"), ("I", "J", "K")])
        P = {A: (1.4, 3.0), B: (0.0, 0.0), C: (4.8, 0.0)}
        tb = lambda X, Y: ((P[X][0] + P[Y][0]) / 2, (P[X][1] + P[Y][1]) / 2)
        P[M], P[N], P[Q] = tb(B, C), tb(C, A), tb(A, B)
        return dict(kieu=kieu, P=P, canh=[(A, B), (B, C), (C, A), (M, N), (N, Q), (Q, M)], tam=None, da_giac=[A, B, C],
                    mo=r"Cho tam giác $ABC$ có $%s$, $%s$, $%s$ lần lượt là trung điểm của các cạnh $BC$, $CA$, $AB$ "
                       r"(xem hình vẽ)." % (M, N, Q))
    if kieu == "thang":
        ten = random.choice(["ABCD", "MNPQ"])
        A, B, C, D = ten
        E = "I" if ten == "ABCD" else "E"
        P = {A: (1.0, 2.2), B: (3.2, 2.2), C: (4.4, 0.0), D: (0.0, 0.0), E: (2.2, 0.0)}
        return dict(kieu=kieu, P=P, canh=[(A, B), (B, C), (C, D), (D, A), (A, E), (B, E)], tam=None, da_giac=[A, B, C, D],
                    mo=r"Cho hình thang $%s$ có hai đáy $%s$, $%s$ với $%s = 2%s$; $%s$ là trung điểm của $%s$ (xem hình vẽ)."
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


_C4_TEN_QH = {"cung_phuong": "cùng phương", "cung_huong": "cùng hướng", "nguoc_huong": "ngược hướng", "bang": "bằng"}


def _c4_ly_qh(H, v, qh, ds):
    """Lời giải liệt kê."""
    vv = _vt(*v)
    if qh == "bang":
        dau = r"Các vectơ bằng $%s$ phải cùng hướng và cùng độ dài với $%s$" % (vv, vv)
    elif qh == "cung_phuong":
        dau = (r"Các vectơ cùng phương với $%s$ có giá song song hoặc trùng với đường thẳng $%s$"
               % (vv, v[0] + v[1]))
    else:
        dau = (r"Các vectơ %s với $%s$ phải cùng phương với $%s$ (giá song song hoặc trùng với $%s$) và chỉ về %s phía"
               % (_C4_TEN_QH[qh], vv, vv, v[0] + v[1], "cùng" if qh == "cung_huong" else "ngược"))
    return dau + r": %s. Có $%d$ vectơ." % (_c4_ds_vt(ds) if ds else "không có", len(ds))


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
            for qh, gt in (("cùng hướng", ch), ("ngược hướng", cp and not ch), ("cùng phương", cp),
                           ("không cùng phương", not cp)):
                ra.append((r"$%s$ và $%s$ %s" % (_vt(*u), _vt(*w), qh), gt, u, w, cp, ch))
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
            mo_ta = ("cùng hướng" if p[5] else "ngược hướng") if p[4] else "không cùng phương (giá cắt nhau)"
            ly.append(r"$%s$ và $%s$ %s nên khẳng định ``%s'' %s." % (_vt(*u), _vt(*w), mo_ta, p[0], "đúng" if p[1] else "sai"))
        debai = H["mo"] + r" Khẳng định nào sau đây %s?" % (r"\textbf{đúng}" if hoi_dung else r"\textbf{sai}")
        giai = (r"Hai vectơ cùng phương khi giá của chúng song song hoặc trùng nhau; hai vectơ cùng phương thì cùng hướng "
                r"hoặc ngược hướng.\\ " + r"\\ ".join(ly))
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
        ten = {3: "tam giác $ABC$", 4: "tứ giác $ABCD$", 5: "ngũ giác $ABCDE$", 6: "lục giác $ABCDEF$"}[k]
        dinh = "ABCDEF"[:k]
        de = (r"Cho %s. Có bao nhiêu vectơ khác vectơ-không có điểm đầu và điểm cuối là các đỉnh của %s?"
              % (ten, "tam giác" if k == 3 else "tứ giác" if k == 4 else "ngũ giác" if k == 5 else "lục giác"))
        dap = k * (k - 1)
        ly = (r"Mỗi vectơ khác vectơ-không được xác định bởi một cặp điểm đầu, điểm cuối khác nhau (có thứ tự). Điểm đầu có "
              r"$%d$ cách chọn, điểm cuối có $%d$ cách chọn nên có $%d \cdot %d = %d$ vectơ" % (k, k - 1, k, k - 1, dap))
        if k <= 4:
            ly += ": " + _c4_ds_vt([(X, Y) for X in dinh for Y in dinh if X != Y])
        return de, dap, ly + ".", [k * (k - 1) // 2, k, k * k, 2 * k]
    if kieu == 1:
        k = random.choice([4, 5, 6, 7])
        ten = ", ".join("$%s$" % c for c in "ABCDEFG"[:k])
        X = random.choice("ABCDEFG"[:k])
        dau = random.random() < 0.5
        de = (r"Cho $%d$ điểm phân biệt %s. Có bao nhiêu vectơ khác vectơ-không có %s là $%s$ và điểm %s là một trong các "
              r"điểm đã cho?" % (k, ten, "điểm đầu" if dau else "điểm cuối", X, "cuối" if dau else "đầu"))
        dap = k - 1
        khac = [c for c in "ABCDEFG"[:k] if c != X]
        ly = (r"Điểm %s phải khác $%s$ (vectơ khác vectơ-không) nên có $%d$ vectơ: %s."
              % ("cuối" if dau else "đầu", X, dap, _c4_ds_vt([(X, Y) if dau else (Y, X) for Y in khac])))
        return de, dap, ly, [k, 2 * (k - 1), k * (k - 1)]
    k = random.choice([3, 4, 5])
    de = (r"Cho $%d$ điểm phân biệt, trong đó không có ba điểm nào thẳng hàng. Có bao nhiêu vectơ khác vectơ-không có "
          r"điểm đầu và điểm cuối thuộc các điểm đã cho?" % k)
    dap = k * (k - 1)
    ly = (r"Mỗi cặp hai điểm phân biệt $X$, $Y$ cho đúng hai vectơ $\overrightarrow{XY}$ và $\overrightarrow{YX}$. Có $%d$ "
          r"cặp điểm nên có $2 \cdot %d = %d$ vectơ." % (k * (k - 1) // 2, k * (k - 1) // 2, dap))
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
        hoi = random.choice(["cùng hướng", "ngược hướng"])
        kt = (lambda c: c[3]) if hoi == "cùng hướng" else (lambda c: c[2] and not c[3])
        cp = [c for c in ds if c[2]]
        kcp = [c for c in ds if not c[2]]
        for _lan in range(200):
            # ba cặp cùng phương (dễ nhầm hướng) và một cặp không cùng phương; đáp số từ 1 đến 3
            chon = random.sample(cp, 3) + random.sample(kcp, 1)
            random.shuffle(chon)
            if 1 <= sum(1 for c in chon if kt(c)) <= 3:
                break
        dap = sum(1 for c in chon if kt(c))
        dong = r"\\ ".join(r"%d) $%s$ và $%s$" % (i + 1, _vt(*c[0]), _vt(*c[1])) for i, c in enumerate(chon))
        de = H["mo"] + r" Cho bốn cặp vectơ: \\ " + dong + r"\\ Có bao nhiêu cặp vectơ %s?" % hoi
        ly = []
        for i, c in enumerate(chon):
            mo_ta = ("cùng hướng" if c[3] else "ngược hướng") if c[2] else "không cùng phương (giá cắt nhau)"
            ly.append(r"Cặp %d: $%s$ và $%s$ %s." % (i + 1, _vt(*c[0]), _vt(*c[1]), mo_ta))
        ly = r"\\ ".join(ly) + r"\\ Vậy có $%d$ cặp vectơ %s." % (dap, hoi)
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
    de = (H["mo"] + r" Có bao nhiêu vectơ khác vectơ $%s$, %s $%s$ và có điểm đầu, điểm cuối là hai trong các điểm %s?"
          % (_vt(*v), "bằng vectơ" if qh == "bang" else _C4_TEN_QH[qh] + " với", _vt(*v), ten_diem))
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
    (r"Vectơ là một đoạn thẳng có hướng", True, "đó là định nghĩa vectơ"),
    (r"Vectơ $\overrightarrow{AB}$ có điểm đầu là $A$, điểm cuối là $B$", True, "theo kí hiệu vectơ"),
    (r"Độ dài của vectơ $\overrightarrow{AB}$ bằng độ dài đoạn thẳng $AB$", True, "theo định nghĩa độ dài vectơ"),
    (r"Hai vectơ $\overrightarrow{AB}$ và $\overrightarrow{BA}$ có cùng độ dài", True, "cả hai đều bằng $AB$"),
    (r"Giá của vectơ $\overrightarrow{AB}$ là đường thẳng $AB$", True, "giá là đường thẳng đi qua điểm đầu và điểm cuối"),
    (r"Hai vectơ cùng phương thì cùng hướng hoặc ngược hướng", True, "đó là nhận xét trong SGK"),
    (r"Hai vectơ cùng hướng thì cùng phương", True, "cùng hướng được xét trong hai vectơ cùng phương"),
    (r"Hai vectơ $\overrightarrow{AB}$ và $\overrightarrow{BA}$ ngược hướng", True, "hai vectơ có cùng giá, chỉ về hai phía ngược nhau"),
    (r"Ba điểm phân biệt $A$, $B$, $C$ thẳng hàng khi và chỉ khi $\overrightarrow{AB}$ và $\overrightarrow{AC}$ cùng phương", True,
     "hai vectơ có chung điểm đầu $A$ nên cùng phương khi và chỉ khi có cùng giá"),
    (r"Nếu $\overrightarrow{a}$, $\overrightarrow{b}$ cùng hướng với $\overrightarrow{c}$ (đều khác $\overrightarrow{0}$) thì "
     r"$\overrightarrow{a}$ cùng hướng với $\overrightarrow{b}$", True, "quan hệ cùng hướng có tính bắc cầu đối với các vectơ khác vectơ-không"),
    (r"Hai vectơ cùng phương thì cùng hướng", False, "chúng có thể ngược hướng, chẳng hạn $\\overrightarrow{AB}$ và $\\overrightarrow{BA}$"),
    (r"Hai vectơ có cùng độ dài thì cùng phương", False, "độ dài không cho biết phương, chẳng hạn hai cạnh kề của hình vuông"),
    (r"Hai vectơ cùng phương thì có cùng giá", False, "giá của chúng có thể chỉ song song"),
    (r"Hai vectơ $\overrightarrow{AB}$ và $\overrightarrow{BA}$ cùng hướng", False, "chúng ngược hướng"),
    (r"Hai vectơ ngược hướng thì không cùng phương", False, "ngược hướng chỉ xét với hai vectơ cùng phương"),
    (r"Độ dài của vectơ $\overrightarrow{AB}$ khác độ dài của vectơ $\overrightarrow{BA}$", False, "cả hai đều bằng $AB$"),
    (r"Vectơ là một đoạn thẳng", False, "vectơ là đoạn thẳng CÓ HƯỚNG (phải chỉ rõ điểm đầu, điểm cuối)"),
    (r"Hai vectơ cùng phương với một vectơ thứ ba (khác $\overrightarrow{0}$) thì cùng hướng", False,
     "chúng chỉ cùng phương, có thể ngược hướng"),
    (r"Ba điểm $A$, $B$, $C$ phân biệt thẳng hàng khi và chỉ khi $\overrightarrow{AB}$ và $\overrightarrow{AC}$ cùng hướng", False,
     "nếu $A$ nằm giữa $B$ và $C$ thì hai vectơ ngược hướng mà ba điểm vẫn thẳng hàng"),
]


def _c4_mc_kho(kho, ten_kho, dang, debai_mo, giai_mo):
    cau = ""
    hoi = random.random() < 0.55
    idx = _c4_uu_tien(ten_kho, list(range(len(kho))))
    d = [i for i in idx if kho[i][1] == hoi][:1]
    s = [i for i in idx if kho[i][1] != hoi][:3]
    _c4_danh_dau(ten_kho, d + s)
    debai = debai_mo + r" Khẳng định nào sau đây %s?" % (r"\textbf{đúng}" if hoi else r"\textbf{sai}")
    giai = giai_mo + r"\\ ".join(r"``%s'' là khẳng định %s vì %s." % (kho[i][0], "đúng" if kho[i][1] else "sai", kho[i][2])
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
        de = (r"Cho các khẳng định sau: \\ " + r"\\ ".join(r"%d) %s;" % (k + 1, _C4_KN_NB037[i][0]) for k, i in enumerate(chon))
              + r"\\ Có bao nhiêu khẳng định đúng?")
        ly = r"\\ ".join(r"Khẳng định %d %s vì %s." % (k + 1, "đúng" if _C4_KN_NB037[i][1] else "sai", _C4_KN_NB037[i][2])
                           for k, i in enumerate(chon)) + r"\\ Vậy có $%d$ khẳng định đúng." % dap
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
        mo = r"Cho hình chữ nhật $%s$ tâm $%s$ có $%s = %s$, $%s = %s$." % ("".join(H["da_giac"]), O, A + B, _c4_tx(p), A + D, _c4_tx(q))
        v, L = random.choice([((A, C), cheo), ((B, D), cheo), ((O, A), cheo / 2), ((C, O), cheo / 2), ((D, B), cheo)])
        ly = (r"$%s = %s = \sqrt{%s^{2} + %s^{2}} = %s$ (định lí Pythagore)" % (A + C, B + D, _c4_ng(p), _c4_ng(q), _c4_tx(cheo))
              + ("" if O not in v else r", $%s$ là trung điểm của đường chéo nên $%s = \dfrac{%s}{2} = %s$" % (O, v[0] + v[1], A + C, _c4_tx(cheo / 2))))
        return mo, v, L, ly, [p + q, cheo / 2 if O not in v else cheo, abs(q - p) if p != q else 2 * p], H
    if kieu == "vuong":
        H = _c4_hinh("vuong")
        A, B, C, D = H["da_giac"]
        O = H["tam"]
        mo = r"Cho hình vuông $%s$ tâm $%s$ có cạnh bằng $%s$." % ("".join(H["da_giac"]), O, _c4_tx(a))
        cheo = a * _sq4(2)
        v, L = random.choice([((A, C), cheo), ((D, B), cheo), ((O, B), cheo / 2), ((A, O), cheo / 2), ((C, D), a)])
        ly = r"$%s = %s\sqrt{2}$ (đường chéo hình vuông)" % (A + C, _c4_tx(a))
        if O in v:
            ly += r", $%s$ là trung điểm của đường chéo nên $%s = \dfrac{%s}{2} = %s$" % (O, v[0] + v[1], A + C, _c4_tx(cheo / 2))
        elif v == (C, D):
            ly = r"$%s = %s$ (cạnh hình vuông)" % (C + D, _c4_tx(a))
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
            mo = r"Cho hình thoi $%s$ tâm $%s$ có $%s = %d$, $%s = %d$." % ("".join(H["da_giac"]), O, A + C, d1, B + D, d2)
            canh = _sq4((d1 / _R4(2)) ** 2 + (d2 / _R4(2)) ** 2)
            v, L = random.choice([((A, B), canh), ((C, D), canh), ((O, A), _R4(d1, 2)), ((B, O), _R4(d2, 2))])
            ly = (r"Hai đường chéo vuông góc tại trung điểm $%s$: $%s = %s$, $%s = %s$; $%s = \sqrt{%s^{2} + %s^{2}} = %s$"
                  % (O, O + A, _c4_tx(_R4(d1, 2)), O + B, _c4_tx(_R4(d2, 2)), A + B, _c4_tx(_R4(d1, 2)), _c4_tx(_R4(d2, 2)), _c4_tx(canh)))
            return mo, v, L, ly, [d1, d2, _R4(d1 + d2, 2)], H
        r3 = math.sqrt(3)
        H["P"].update({A: (0, 1.2), B: (1.2 * r3, 0), C: (2.4 * r3, 1.2), D: (1.2 * r3, 2.4), O: (1.2 * r3, 1.2)})
        mo = (r"Cho hình thoi $%s$ tâm $%s$ có cạnh bằng $%s$ và $\widehat{%s} = 60^{\circ}$."
              % ("".join(H["da_giac"]), O, _c4_tx(a), B + A + D))
        v, L = random.choice([((B, D), a), ((A, C), a * _sq4(3)), ((O, A), a * _sq4(3) / 2), ((D, O), a / 2)])
        ly = (r"Tam giác $%s$ cân tại $%s$ có góc $60^{\circ}$ nên đều: $%s = %s$. $%s$ là đường cao của tam giác đều cạnh $%s$ "
              r"nên $%s = \dfrac{%s\sqrt{3}}{2}$, $%s = 2%s = %s\sqrt{3}$" % (A + B + D, A, B + D, _c4_tx(a), A + O, _c4_tx(a), A + O,
                                                                              _c4_tx(a), A + C, A + O, _c4_tx(a)))
        return mo, v, L, ly, [a, a * _sq4(3), a * _sq4(3) / 2, a / 2, a * _sq4(2)], H
    if kieu == "luc_giac":
        H = _c4_hinh("luc_giac")
        mo = r"Cho lục giác đều $ABCDEF$ tâm $O$ có cạnh bằng $%s$." % _c4_tx(a)
        v, L = random.choice([(("A", "D"), 2 * a), (("B", "E"), 2 * a), (("O", "C"), a), (("A", "C"), a * _sq4(3)),
                              (("F", "B"), a * _sq4(3)), (("E", "O"), a)])
        ly = (r"Lục giác đều được chia thành sáu tam giác đều cạnh $%s$ chung đỉnh $O$ nên $OA = OB = \ldots = %s$, "
              r"$AD = BE = CF = 2 \cdot %s$; $AC = BD = \ldots = 2 \cdot \dfrac{%s\sqrt{3}}{2} = %s\sqrt{3}$ (gấp đôi đường cao tam "
              r"giác đều)" % (_c4_tx(a), _c4_tx(a), _c4_tx(a), _c4_tx(a), _c4_tx(a)))
        return mo, v, L, ly, [a, 2 * a, a * _sq4(3), a * _sq4(3) / 2, a * _sq4(2)], H
    H = _c4_hinh("tg_trung_diem")
    M, N, Q = [t for t in H["P"] if t not in "ABC"]
    r3 = math.sqrt(3)
    H["P"].update({"A": (2.2, 2.2 * r3), "B": (0, 0), "C": (4.4, 0), M: (2.2, 0), N: (3.3, 1.1 * r3), Q: (1.1, 1.1 * r3)})
    mo = (r"Cho tam giác đều $ABC$ có cạnh bằng $%s$; $%s$, $%s$, $%s$ lần lượt là trung điểm của $BC$, $CA$, $AB$."
          % (_c4_tx(a), M, N, Q))
    v, L = random.choice([(("A", M), a * _sq4(3) / 2), ((N, "B"), a * _sq4(3) / 2), ((M, N), a / 2), ((Q, "B"), a / 2)])
    ly = (r"Đường trung tuyến của tam giác đều cũng là đường cao, có độ dài $\dfrac{%s\sqrt{3}}{2}$; đoạn nối hai trung điểm "
          r"(đường trung bình) và nửa cạnh đều bằng $\dfrac{%s}{2}$" % (_c4_tx(a), _c4_tx(a)))
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
        debai = mo + r" Độ dài của vectơ $%s$ bằng" % _vt(*v)
        giai = ly.replace(r"\frac", r"\dfrac") + r".\\ Vậy $\left|%s\right| = %s = %s$." % (_vt(*v), v[0] + v[1], dap.strip("$"))
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
        debai = mo + r" Tính độ dài của vectơ $%s$%s." % (_vt(*v), "" if chinh_xac else " (làm tròn kết quả đến hàng phần mười)")
        giai = ly + r".\\ Vậy $\left|%s\right| = %s %s %s$." % (_vt(*v), _c4_tx(L), "=" if chinh_xac else r"\approx", s)
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
                    dung.append((u, w, "cùng hướng và cùng độ dài"))
                elif cung_do and _c4_cp(a, b):
                    sai.append((u, w, "ngược hướng"))
                elif _c4_ch(a, b):
                    sai.append((u, w, "cùng hướng nhưng khác độ dài"))
                elif cung_do and not _c4_cp(a, b):
                    sai.append((u, w, "cùng độ dài nhưng không cùng phương"))
        hoi = random.random() < 0.55
        A_, B_ = (dung, sai) if hoi else (sai, dung)
        if not A_ or len(B_) < 3:
            continue
        random.shuffle(A_)
        random.shuffle(B_)
        chon = [A_[0]] + B_[:3]
        so += 1
        tex = lambda c: r"$%s = %s$" % (_vt(*c[0]), _vt(*c[1]))
        debai = H["mo"] + r" Đẳng thức nào sau đây %s?" % (r"\textbf{đúng}" if hoi else r"\textbf{sai}")
        giai = (r"Hai vectơ bằng nhau khi chúng cùng hướng và có cùng độ dài.\\ "
                + r"\\ ".join(r"$%s$ và $%s$ %s nên %s %s." % (_vt(*c[0]), _vt(*c[1]), c[2], tex(c), "đúng" if c in dung else "sai")
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
    (r"Hai vectơ bằng nhau thì có cùng độ dài", True, "hai vectơ bằng nhau là hai vectơ cùng hướng và cùng độ dài"),
    (r"Hai vectơ bằng nhau thì cùng hướng", True, "theo định nghĩa hai vectơ bằng nhau"),
    (r"Hai vectơ bằng nhau thì cùng phương", True, "chúng cùng hướng nên cùng phương"),
    (r"Vectơ-không là vectơ có điểm đầu và điểm cuối trùng nhau", True, "đó là định nghĩa vectơ-không"),
    (r"Vectơ-không có độ dài bằng $0$", True, "$\\left|\\overrightarrow{AA}\\right| = 0$"),
    (r"Vectơ-không cùng phương, cùng hướng với mọi vectơ", True, "đó là quy ước trong SGK"),
    (r"$\overrightarrow{AA} = \overrightarrow{BB}$ với mọi điểm $A$, $B$", True, "mọi vectơ-không đều bằng nhau và kí hiệu là $\\overrightarrow{0}$"),
    (r"Nếu $\overrightarrow{a} = \overrightarrow{b}$ và $\overrightarrow{b} = \overrightarrow{c}$ thì $\overrightarrow{a} = \overrightarrow{c}$", True,
     "ba vectơ cùng hướng và cùng độ dài"),
    (r"Tứ giác $ABCD$ là hình bình hành khi và chỉ khi $\overrightarrow{AB} = \overrightarrow{DC}$ ($A$, $B$, $C$, $D$ không thẳng hàng)", True,
     "$\\overrightarrow{AB} = \\overrightarrow{DC}$ nghĩa là $AB \\parallel DC$, $AB = DC$ và cùng hướng"),
    (r"Hai vectơ có cùng độ dài thì bằng nhau", False, "chúng còn phải cùng hướng"),
    (r"Hai vectơ cùng phương và có cùng độ dài thì bằng nhau", False, "chúng có thể ngược hướng, chẳng hạn $\\overrightarrow{AB}$ và $\\overrightarrow{BA}$"),
    (r"Hai vectơ cùng hướng thì bằng nhau", False, "chúng còn phải có cùng độ dài"),
    (r"$\overrightarrow{AB} = \overrightarrow{BA}$ với mọi điểm $A$, $B$", False, "khi $A \\ne B$ hai vectơ ngược hướng"),
    (r"Vectơ-không không cùng phương với vectơ nào", False, "vectơ-không cùng phương với mọi vectơ"),
    (r"Độ dài của vectơ-không bằng $1$", False, "độ dài vectơ-không bằng $0$"),
    (r"$\overrightarrow{AB} = \overrightarrow{CD}$ khi và chỉ khi $AB = CD$", False, "$AB = CD$ chỉ cho biết hai vectơ cùng độ dài"),
    (r"Nếu $\overrightarrow{AB} = \overrightarrow{CD}$ thì $A$, $B$, $C$, $D$ là bốn đỉnh của hình bình hành $ABCD$", False,
     "khi đó $ABDC$ (hoặc bốn điểm thẳng hàng) mới đúng, không phải $ABCD$"),
    (r"Nếu $\overrightarrow{AB} = \overrightarrow{AC}$ thì $B$ khác $C$", False, "hai vectơ chung điểm đầu bằng nhau thì $B \\equiv C$"),
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
        pa_d = r"$%s$ là hình bình hành" % dung
        nhieu = [r"$%s$ là hình bình hành" % o for o in sai] + [r"$%s$ là trung điểm của $%s$" % (T, X + Z)]
        debai = (r"Cho ba điểm $%s$, $%s$, $%s$ không thẳng hàng và điểm $%s$ thoả mãn $%s = %s$. Khẳng định nào sau đây đúng?"
                 % (X, Y, Z, T, _vt(p1, p2), _vt(q1, q2)))
        giai = (r"$%s = %s$ nên hai đoạn $%s$, $%s$ song song (ba điểm không thẳng hàng), bằng nhau và hai vectơ cùng hướng. "
                r"Do đó tứ giác $%s$ (đi theo thứ tự $%s \to %s \to %s \to %s$) là hình bình hành: hai cạnh đối $%s$ và $%s$ song song, "
                r"bằng nhau." % (_vt(p1, p2), _vt(q1, q2), p1 + p2, q1 + q2, dung, *dung, dung[0] + dung[1], dung[3] + dung[2]))
        cau += _MC_khong_cham(debai, pa_d, nhieu, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH039: biểu diễn đại lượng thực tiễn bằng vectơ
# ---------------------------------------------------------------------
_C4_HUONG = {(1, 0): "đông", (-1, 0): "tây", (0, 1): "bắc", (0, -1): "nam",
             (1, 1): "đông bắc", (-1, 1): "tây bắc", (1, -1): "đông nam", (-1, -1): "tây nam"}


def _c4_luoi(ds, nhan, rong=10, cao=6, la_ban=False):
    """Lưới ô vuông với các mũi tên ds = [(x0, y0, dx, dy)] và nhãn."""
    out = ["\\begin{tikzpicture}[>=stealth,x=0.5cm,y=0.5cm,scale=1]",
           "\\draw[gray!50, very thin] (0,0) grid (%d,%d);" % (rong, cao)]
    for (x0, y0, dx, dy), t in zip(ds, nhan):
        out.append("\\draw[->, very thick] (%d,%d) -- (%d,%d) node[midway, %s]{\\footnotesize $%s$};"
                   % (x0, y0, x0 + dx, y0 + dy, "above" if dy == 0 else "right", t))
    if la_ban:
        out.append("\\draw[->] (%d,%d) -- (%d,%d) node[above]{\\scriptsize Bắc};" % (rong + 2, cao - 3, rong + 2, cao - 1))
        out.append("\\draw[->] (%d,%d) -- (%d,%d) node[right]{\\scriptsize Đông};" % (rong + 2, cao - 3, rong + 4, cao - 3))
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
        hoi = random.choice(["cùng hướng", "ngược hướng", "bằng nhau"])
        goc = random.choice([(1, 0), (0, 1), (1, 1), (1, -1)])
        k1 = random.randint(2, 3)
        k2 = k1 if hoi == "bằng nhau" else random.choice([k for k in (1, 2, 3) if k != k1] if hoi == "cùng hướng" else [1, 2, 3])
        s2 = -1 if hoi == "ngược hướng" else 1
        v1 = (goc[0] * k1, goc[1] * k1)
        v2 = (s2 * goc[0] * k2, s2 * goc[1] * k2)
        khac = [d for d in _C4_HUONG if d != goc and d != (-goc[0], -goc[1])]
        d3, d4 = random.sample(khac, 2)
        v3 = (d3[0] * random.randint(1, 3), d3[1] * random.randint(1, 3))
        v4 = (d4[0] * random.randint(1, 3), d4[1] * random.randint(1, 3))
        if hoi != "bằng nhau":
            v3 = (goc[0] * (-s2) * random.randint(1, 3), goc[1] * (-s2) * random.randint(1, 3)) if random.random() < .5 else v3
        V = [v1, v2, v3, v4]
        random.shuffle(V)
        ten = [r"\overrightarrow{F_{%d}}" % (i + 1) for i in range(4)]
        def qh(a, b):
            if _c4_bang(a, b):
                return "bằng nhau"
            if _c4_ch(a, b):
                return "cùng hướng"
            if _c4_cp(a, b):
                return "ngược hướng"
            return "không cùng phương"
        cap = list(itertools.combinations(range(4), 2))
        dung = [c for c in cap if qh(V[c[0]], V[c[1]]) == hoi or (hoi == "cùng hướng" and qh(V[c[0]], V[c[1]]) == "bằng nhau")]
        if len(dung) != 1:
            continue
        sai = [c for c in cap if c not in dung]
        random.shuffle(sai)
        try:
            ds = _c4_dat_mui_ten(V)
        except ValueError:
            continue
        so += 1
        tx = lambda c: r"$%s$ và $%s$" % (ten[c[0]], ten[c[1]])
        debai = (r"Các lực $%s$ tác dụng lên các vật được biểu diễn bằng các vectơ trên lưới ô vuông như hình vẽ. Cặp lực nào "
                 r"sau đây \textbf{%s}?" % ("$, $".join(ten), hoi))
        giai = r"\\ ".join(r"%s %s." % (tx(c), qh(V[c[0]], V[c[1]]) if qh(V[c[0]], V[c[1]]) != "không cùng phương" else
                                        "không cùng phương (giá cắt nhau)") for c in dung + sai[:3])
        giai = r"Đọc hướng và độ dài các vectơ trên lưới:\\ " + giai
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
        vat = random.choice(["một chiếc thuyền", "một cơn bão", "một chiếc ô tô", "một đàn chim", "một chiếc máy bay"])
        debai = (r"Trên lưới ô vuông (xem hình, phía trên là hướng bắc, bên phải là hướng đông), mỗi cạnh ô vuông ứng với "
                 r"$10$ km/h. Vectơ nào biểu diễn vận tốc của %s đang di chuyển theo hướng %s với tốc độ $%d$ km/h?"
                 % (vat, _C4_HUONG[huong], 10 * k))
        giai = (r"Vectơ cần tìm chỉ về hướng %s và có độ dài $%d$ cạnh ô (ứng với $%d$ km/h): đó là $%s$.\\ $%s$ đúng hướng nhưng "
                r"dài $%d$ ô; $%s$ dài $%d$ ô nhưng chỉ về hướng %s; $%s$ dài $%d$ ô nhưng chỉ về hướng %s."
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
        mo = (r"Một dòng sông chảy thẳng với vận tốc dòng nước là $\overrightarrow{v_n}$ ($%d$ km/h). Thuyền $A$ đi xuôi dòng, thuyền $B$ "
              r"đi ngược dòng, thuyền $C$ đi xuôi dòng; vận tốc của các thuyền lần lượt là $\overrightarrow{v_A}$, $\overrightarrow{v_B}$, "
              r"$\overrightarrow{v_C}$ với độ lớn $%d$ km/h, $%d$ km/h, $%d$ km/h." % (vn, a, a, b))
        X = [(r"$\overrightarrow{v_A}$ cùng hướng với $\overrightarrow{v_n}$", True, "thuyền $A$ đi xuôi dòng"),
             (r"$\overrightarrow{v_B}$ ngược hướng với $\overrightarrow{v_n}$", True, "thuyền $B$ đi ngược dòng"),
             (r"$\overrightarrow{v_A}$ và $\overrightarrow{v_B}$ cùng phương", True, "cả hai cùng chuyển động dọc theo dòng sông"),
             (r"$\overrightarrow{v_A}$ và $\overrightarrow{v_C}$ cùng hướng", True, "hai thuyền đều đi xuôi dòng"),
             (r"$\overrightarrow{v_A} = \overrightarrow{v_B}$", False, "hai vectơ có cùng độ lớn nhưng ngược hướng"),
             (r"$\overrightarrow{v_A} = \overrightarrow{v_C}$", False, "hai vectơ cùng hướng nhưng khác độ lớn ($%d \\ne %d$)" % (a, b)),
             (r"$\overrightarrow{v_B}$ cùng hướng với $\overrightarrow{v_n}$", False, "thuyền $B$ đi ngược dòng"),
             (r"$\overrightarrow{v_A}$ và $\overrightarrow{v_B}$ cùng hướng", False, "một thuyền xuôi dòng, một thuyền ngược dòng")]
        return mo, X
    mo = (r"Trên một đoạn đường thẳng theo hướng bắc - nam, xe $A$ chạy về phía bắc với tốc độ $%d$ km/h, xe $B$ chạy về phía nam "
          r"với tốc độ $%d$ km/h, xe $C$ chạy về phía bắc với tốc độ $%d$ km/h. Gọi $\overrightarrow{v_A}$, $\overrightarrow{v_B}$, "
          r"$\overrightarrow{v_C}$ là vectơ vận tốc của ba xe." % (a * 3, a * 3, b * 3))
    X = [(r"$\overrightarrow{v_A}$ và $\overrightarrow{v_B}$ ngược hướng", True, "hai xe chạy theo hai hướng ngược nhau trên cùng một đường"),
         (r"$\overrightarrow{v_A}$ và $\overrightarrow{v_C}$ cùng hướng", True, "hai xe cùng chạy về phía bắc"),
         (r"$\overrightarrow{v_B}$ và $\overrightarrow{v_C}$ cùng phương", True, "các xe chuyển động trên cùng một đường thẳng"),
         (r"$\left|\overrightarrow{v_A}\right| = \left|\overrightarrow{v_B}\right|$", True, "hai xe có cùng tốc độ $%d$ km/h" % (a * 3)),
         (r"$\overrightarrow{v_A} = \overrightarrow{v_B}$", False, "hai vectơ cùng độ lớn nhưng ngược hướng"),
         (r"$\overrightarrow{v_A} = \overrightarrow{v_C}$", False, "hai vectơ cùng hướng nhưng khác độ lớn"),
         (r"$\overrightarrow{v_B}$ và $\overrightarrow{v_C}$ cùng hướng", False, "xe $B$ chạy về phía nam, xe $C$ chạy về phía bắc"),
         (r"$\overrightarrow{v_A}$ và $\overrightarrow{v_B}$ không cùng phương", False, "hai xe chạy trên cùng một đường thẳng")]
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
        debai = mo + r" Khẳng định nào sau đây %s?" % (r"\textbf{đúng}" if hoi else r"\textbf{sai}")
        giai = r"\\ ".join(r"%s là khẳng định %s vì %s." % (x[0], "đúng" if x[1] else "sai", x[2]) for x in [d] + s)
        cau += _MC_khong_cham(debai, d[0], [x[0] for x in s], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TỰ LUẬN HAI ĐƠN VỊ
# ---------------------------------------------------------------------
def _c4_tl_ds(ds):
    return r",\ ".join(_vt(*w) for w in ds) if ds else r"\text{không có}"


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
        de = H["mo"] + r" Xét các vectơ khác vectơ $%s$ có điểm đầu, điểm cuối là hai trong các điểm %s." % (
            _vt(*v), ", ".join("$%s$" % t for t in H["P"]))
        ds = [(r"Tìm các vectơ cùng hướng với vectơ $%s$." % _vt(*v), _c4_tl_ds(ch), _c4_ly_qh(H, v, "cung_huong", ch)),
              (r"Tìm các vectơ bằng vectơ $%s$." % _vt(*v), _c4_tl_ds(bg),
               _c4_ly_qh(H, v, "bang", bg) + r" (Trong các vectơ cùng hướng ở câu a), chỉ giữ các vectơ có độ dài bằng $%s$.)" % (v[0] + v[1]))]
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
        de = (r"Bốn lực $%s$ được biểu diễn bằng các vectơ trên lưới ô vuông như hình bên (phía trên là hướng bắc, bên phải là "
              r"hướng đông); mỗi cạnh ô vuông ứng với $10$ N." % "$, $".join(ten))
        ys = [(r"Tìm các lực cùng hướng, các lực ngược hướng với $%s$." % ten[0],
               _c4_tl_dap4(r"cùng hướng: $%s$; ngược hướng: $%s$" % (r",\ ".join(ch) or r"\text{không có}", r",\ ".join(ng) or r"\text{không có}")),
               r"Các lực cùng phương với $%s$ là các lực có giá nằm ngang%s. Trong đó cùng hướng: $%s$; ngược hướng: $%s$."
               % (ten[0], "" if V[0][1] == 0 else "" , r",\ ".join(ch) or r"\text{không có}", r",\ ".join(ng) or r"\text{không có}")
               if V[0][1] == 0 else
               r"Các lực cùng phương với $%s$ là các lực có giá thẳng đứng. Trong đó cùng hướng: $%s$; ngược hướng: $%s$."
               % (ten[0], r",\ ".join(ch) or r"\text{không có}", r",\ ".join(ng) or r"\text{không có}")),
              (r"Tính độ lớn và nêu hướng của mỗi lực.",
               _c4_tl_dap4("; ".join(r"$\left|%s\right| = %d$ N (%s)" % (ten[i], 10 * do[i], hg[i]) for i in range(4))),
               r"Đếm số cạnh ô của mỗi vectơ rồi nhân với $10$ N: " +
               "; ".join(r"$%s$ dài $%d$ ô, hướng %s nên $\left|%s\right| = %d$ N" % (ten[i], do[i], hg[i], ten[i], 10 * do[i]) for i in range(4))
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
            return r"hai vế cùng bằng $%s$" % gl
        if gl != l.tex:
            return r"vế trái bằng $%s$, đúng bằng vế phải" % gl
        if gr != r.tex:
            return r"vế phải bằng $%s$, đúng bằng vế trái" % gr
        return r"$%s$ và $%s$ cùng hướng và cùng độ dài" % (l.tex, r.tex)
    trai = (r"vế trái bằng $%s$" % gl) if gl != l.tex else (r"vế trái là $%s$" % gl)
    phai = (r"vế phải bằng $%s$" % gr) if gr != r.tex else (r"vế phải là $%s$" % gr)
    return trai + ", còn " + phai + "; hai vectơ này khác nhau"


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
    tu = r"\textbf{đúng}" if hoi_dung else r"\textbf{sai}"
    debai = (mo + r" Trong các khẳng định sau, có bao nhiêu khẳng định %s?\\ " % tu
             + r"\\ ".join("%d. %s" % (i + 1, x[0]) for i, (x, _) in enumerate(ds)))
    giai = giai_mo + r"\\ ".join(r"%d. %s là khẳng định %s vì %s." % (i + 1, x[0], "đúng" if d else "sai", x[1])
                                for i, (x, d) in enumerate(ds))
    giai += r"\\ Vậy có $%d$ khẳng định %s." % (dap, tu)
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
        mo = r"Cho bốn điểm $%s$, $%s$, $%s$, $%s$ bất kì." % tuple(sorted([X, Y, Z, T]))
        giai_mo = (r"Quy tắc ba điểm: với ba điểm $%s$, $%s$, $%s$ bất kì, $%s + %s = %s$.\\ "
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
        giai_mo = (r"Quy tắc hình bình hành: nếu $%s$ là hình bình hành thì $%s + %s = %s$.\\ "
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
        mo = r"Cho ba điểm $%s$, $%s$, $%s$ bất kì." % tuple(sorted([X, Y, Z]))
        giai_mo = (r"Quy tắc trừ: với ba điểm $%s$, $%s$, $%s$ bất kì, $%s - %s = %s$.\\ "
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
                    ly = r"$%s$ và $%s$ là hai vectơ đối nhau (cùng độ dài, ngược hướng)" % (_vt(*u), _vt(*w))
                elif abs(a - b) < 1e-9:
                    ly = r"$%s$ và $%s$ cùng hướng nên không phải hai vectơ đối nhau" % (_vt(*u), _vt(*w))
                else:
                    ly = r"$%s$ và $%s$ không cùng phương nên không phải hai vectơ đối nhau" % (_vt(*u), _vt(*w))
                tex = random.choice([r"$%s + %s = \overrightarrow{0}$" % (_vt(*u), _vt(*w)),
                                     r"$%s = -%s$" % (_vt(*u), _vt(*w))])
                (dung if abs(a + b) < 1e-9 else sai).append((tex, ly))
        dung.append((r"$%s + %s + %s + %s = \overrightarrow{0}$" % tuple(_vt(O, X) for X in (A, B, C, D)),
                     r"$%s + %s = \overrightarrow{0}$ và $%s + %s = \overrightarrow{0}$ ($%s$ là trung điểm của mỗi "
                     r"đường chéo)" % (_vt(O, A), _vt(O, C), _vt(O, B), _vt(O, D), O)))
        giai_mo = (r"Hai vectơ đối nhau là hai vectơ cùng độ dài, ngược hướng; $\vec u + \vec w = \overrightarrow{0}$ "
                   r"khi và chỉ khi $\vec u = -\vec w$.\\ ")
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
        mo = r"Cho ba vectơ $%s$, $%s$, $%s$ tuỳ ý." % tuple(r"\overrightarrow{%s}" % t for t in tu)
        giai_mo = (r"Phép cộng vectơ có tính chất giao hoán, kết hợp; $\vec a + \overrightarrow{0} = \vec a$, "
                   r"$\vec a + \left(-\vec a\right) = \overrightarrow{0}$; nhóm các vectơ giống nhau để rút gọn mỗi vế.\\ ")
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
            debai = (r"Cho vectơ $%s$ có $\left|%s\right| = %d$. Độ dài của vectơ $%s%s$ bằng bao nhiêu?"
                     % (a, a, m, kt, a))
            giai = (r"$\left|%s%s\right| = \left|%s\right|\cdot\left|%s\right| = %s\cdot %d = %s$."
                    % (kt, a, kt, a, _xx4(float(abs(k)), 2), m, _xx4(float(n), 2)))
            ung = [m, float(k) * m, n + m, abs(n - m), 2 * n]
        else:
            dap = _Fr5(m)
            debai = (r"Cho hai vectơ $%s$, $%s$ thoả mãn $%s = %s%s$ và $\left|%s\right| = %s$. Tính $\left|%s\right|$."
                     % (a, b, b, kt, a, b, _xx4(float(n), 2), a))
            giai = (r"$\left|%s\right| = \left|%s\right|\cdot\left|%s\right| = %s\left|%s\right|$ nên "
                    r"$\left|%s\right| = %s : %s = %d$."
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
        mo = r"Cho hai vectơ $\overrightarrow{a}$, $\overrightarrow{b}$ tuỳ ý."
        giai_mo = (r"Với hai số $k$, $l$ và hai vectơ $\vec a$, $\vec b$: $k\left(\vec a + \vec b\right) = k\vec a + "
                   r"k\vec b$; $\left(k + l\right)\vec a = k\vec a + l\vec a$; $k\left(l\vec a\right) = \left(kl\right)\vec a$."
                   r"\\ ")
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho ba điểm $A%s$, $B%s$, $C%s$. Tìm số thực $k$ sao cho "
                 r"$\overrightarrow{AB} = k\overrightarrow{AC}$." % (_toado(xa, ya), _toado(xb, yb), _toado(xc, yc)))
        giai = (r"$\overrightarrow{AB} = %s$, $\overrightarrow{AC} = %s$. Vì $%s = %s\cdot\left(%d\right)$ và "
                r"$%s = %s\cdot\left(%d\right)$ nên $\overrightarrow{AB} = %s\overrightarrow{AC}$, tức là $k = %s$ (ba "
                r"điểm $A$, $B$, $C$ thẳng hàng)."
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
        mo = r"Cho $%s$ là trung điểm của đoạn thẳng $%s$ và $%s$ là một điểm bất kì." % (J, X + Y, N)
        giai_mo = (r"$%s$ là trung điểm của $%s$ nên $%s + %s = \overrightarrow{0}$ và với mọi điểm $%s$: $%s + %s = "
                   r"2%s$.\\ " % (J, X + Y, _vt(J, X), _vt(J, Y), N, _vt(N, X), _vt(N, Y), _vt(N, J)))
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
                    dung.append((tex, r"$%s$ và $%s$ cùng hướng và cùng độ dài" % (_vt(*u), _vt(*w))))
                elif cung_do and _c4_cp(a, b):
                    sai.append((tex, r"$%s$ và $%s$ ngược hướng" % (_vt(*u), _vt(*w))))
                elif _c4_ch(a, b):
                    sai.append((tex, r"$%s$ và $%s$ cùng hướng nhưng khác độ dài" % (_vt(*u), _vt(*w))))
                elif cung_do and not _c4_cp(a, b):
                    sai.append((tex, r"$%s$ và $%s$ cùng độ dài nhưng không cùng phương" % (_vt(*u), _vt(*w))))
        if len(dung) < 3 or len(sai) < 3:
            continue
        so += 1
        cau += _c4s_dem(H["mo"], dung, sai, dang, _c4_tikz(H),
                        r"Hai vectơ bằng nhau khi chúng cùng hướng và có cùng độ dài.\\ ")
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
         r"tích vô hướng có tính chất giao hoán"),
        (r"$%s\cdot\left(%s + %s\right) = %s\cdot %s + %s\cdot %s$" % (a, b, c, a, b, a, c),
         lambda A, B, C: (d(A, B + C), d(A, B) + d(A, C)), r"tích vô hướng có tính chất phân phối đối với phép cộng vectơ"),
        (r"$%s\cdot\left(%s - %s\right) = %s\cdot %s - %s\cdot %s$" % (a, b, c, a, b, a, c),
         lambda A, B, C: (d(A, B - C), d(A, B) - d(A, C)), r"tích vô hướng có tính chất phân phối đối với phép trừ vectơ"),
        (r"$\left(%d%s\right)\cdot %s = %d\left(%s\cdot %s\right)$" % (k, a, b, k, a, b),
         lambda A, B, C: (d(k * A, B), k * d(A, B)), r"$\left(k\vec a\right)\cdot\vec b = k\left(\vec a\cdot\vec b\right)$"),
        (r"$%s^{2} = \left|%s\right|^{2}$" % (a, a), lambda A, B, C: (d(A, A), abs(A) ** 2),
         r"bình phương vô hướng của một vectơ bằng bình phương độ dài của nó"),
        (r"$\left(%s + %s\right)\cdot\left(%s - %s\right) = \left|%s\right|^{2} - \left|%s\right|^{2}$" % (a, b, a, b, a, b),
         lambda A, B, C: (d(A + B, A - B), abs(A) ** 2 - abs(B) ** 2),
         r"khai triển vế trái được $\vec a^{2} - \vec a\cdot\vec b + \vec b\cdot\vec a - \vec b^{2} = \left|\vec a\right|^{2} - "
         r"\left|\vec b\right|^{2}$"),
        (r"$%s\cdot %s = -%s\cdot %s$" % (a, b, b, a), lambda A, B, C: (d(A, B), -d(B, A)),
         r"$\vec a\cdot\vec b = \vec b\cdot\vec a$, hai vế chỉ bằng nhau khi $\vec a\cdot\vec b = 0$"),
        (r"$%s\cdot\left(%s - %s\right) = %s\cdot %s + %s\cdot %s$" % (a, b, c, a, b, a, c),
         lambda A, B, C: (d(A, B - C), d(A, B) + d(A, C)), r"đúng ra $\vec a\cdot\left(\vec b - \vec c\right) = "
                                                            r"\vec a\cdot\vec b - \vec a\cdot\vec c$"),
        (r"$\left(%d%s\right)\cdot\left(%d%s\right) = %d\left(%s\cdot %s\right)$" % (k, a, k, b, k, a, b),
         lambda A, B, C: (d(k * A, k * B), k * d(A, B)), r"vế trái bằng $%d\left(\vec a\cdot\vec b\right)$" % (k * k)),
        (r"$%s^{2} = \left|%s\right|$" % (a, a), lambda A, B, C: (d(A, A), abs(A)),
         r"$\vec a^{2} = \left|\vec a\right|^{2}$ chứ không phải $\left|\vec a\right|$"),
        (r"$\left(%s + %s\right)\cdot\left(%s - %s\right) = \left|%s\right|^{2} + \left|%s\right|^{2}$" % (a, b, a, b, a, b),
         lambda A, B, C: (d(A + B, A - B), abs(A) ** 2 + abs(B) ** 2),
         r"vế trái bằng $\left|\vec a\right|^{2} - \left|\vec b\right|^{2}$"),
        (r"$%s\cdot %s = \left|%s\right|\cdot\left|%s\right|$" % (a, b, a, b), lambda A, B, C: (d(A, B), abs(A) * abs(B)),
         r"$\vec a\cdot\vec b = \left|\vec a\right|\cdot\left|\vec b\right|\cdot\cos\left(\vec a, \vec b\right)$, chỉ bằng "
         r"$\left|\vec a\right|\cdot\left|\vec b\right|$ khi hai vectơ cùng hướng"),
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
        mo = r"Cho ba vectơ $\overrightarrow{a}$, $\overrightarrow{b}$, $\overrightarrow{c}$ tuỳ ý."
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
            hoi = "hoành độ" if kieu == "ij_hd" else "tung độ"
            dap = x if kieu == "ij_hd" else y
            debai = (r"Trong mặt phẳng toạ độ $Oxy$ với hai vectơ đơn vị $\overrightarrow{i}$, $\overrightarrow{j}$, cho "
                     r"vectơ $%s = %s$. Tìm \textbf{%s} của vectơ $%s$." % (u, _bt_ij(x, y), hoi, u))
            giai = r"$%s = %s$ nên $%s = %s$, %s của $%s$ bằng $%d$." % (u, _bt_ij(x, y), u, _toado(x, y), hoi, u, dap)
        else:
            dap = x if kieu == "td_m" else y
            debai = (r"Trong mặt phẳng toạ độ $Oxy$ với hai vectơ đơn vị $\overrightarrow{i}$, $\overrightarrow{j}$, cho "
                     r"vectơ $%s = %s$. Biết $%s = m\overrightarrow{i} + n\overrightarrow{j}$. Tìm $%s$."
                     % (u, _toado(x, y), u, "m" if kieu == "td_m" else "n"))
            giai = (r"$%s = %s$ nghĩa là $%s = %s$, nên $m = %d$, $n = %d$." % (u, _toado(x, y), u, _bt_ij(x, y), x, y))
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
        w = tuple(random.randint(-6, 6) for _ in range(4)) + (random.choice(["hoành độ", "tung độ"]),)
        if w[:2] != w[2:4] and w not in gt:
            gt.append(w)
    cau = ""
    for xa, ya, xb, yb, hoi in gt:
        dx, dy = xb - xa, yb - ya
        dap = dx if hoi == "hoành độ" else dy
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai điểm $A%s$ và $B%s$. Tìm \textbf{%s} của vectơ "
                 r"$\overrightarrow{AB}$." % (_toado(xa, ya), _toado(xb, yb), hoi))
        giai = (r"$\overrightarrow{AB} = \left(x_B - x_A;\ y_B - y_A\right) = \left(%d - \left(%d\right);\ %d - \left(%d\right)"
                r"\right) = %s$. Vậy %s của $\overrightarrow{AB}$ bằng $%d$." % (xb, xa, yb, ya, _toado(dx, dy), hoi, dap))
        ung = [(xa - xb) if hoi == "hoành độ" else (ya - yb), (xa + xb) if hoi == "hoành độ" else (ya + yb),
               dy if hoi == "hoành độ" else dx, dap + 1, dap - 1, dap + 2]
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
        (r"Vectơ là một đoạn thẳng", "có hướng",
         ["có hướng dương và hướng âm", "có hai đầu mút", "có độ dài bằng $1$", "nằm ngang"],
         "Vectơ là một đoạn thẳng có hướng, nghĩa là trong hai điểm mút đã chỉ rõ điểm nào là điểm đầu, điểm nào là điểm cuối."),
        (r"Giá của vectơ $%s$ ($%s \ne %s$) là" % (xy, X, Y), r"đường thẳng $%s$" % (X + Y),
         [r"đoạn thẳng $%s$" % (X + Y), r"độ dài đoạn thẳng $%s$" % (X + Y), r"tia $%s$" % (X + Y), r"điểm $%s$" % Y],
         r"Đường thẳng đi qua điểm đầu và điểm cuối của một vectơ gọi là giá của vectơ đó; giá của $%s$ là đường thẳng $%s$." % (xy, X + Y)),
        (r"Độ dài của vectơ $%s$ là" % xy, r"độ dài đoạn thẳng $%s$" % (X + Y),
         [r"đường thẳng $%s$" % (X + Y), r"tia $%s$" % (Y + X), r"vectơ $%s$" % yx, r"số $1$"],
         r"Độ dài của vectơ là khoảng cách giữa điểm đầu và điểm cuối: $\left|%s\right| = %s$." % (xy, X + Y)),
        (r"Hai vectơ được gọi là cùng phương nếu", "giá của chúng song song hoặc trùng nhau",
         ["chúng có cùng độ dài", "giá của chúng vuông góc với nhau", "chúng có chung điểm đầu", "giá của chúng cắt nhau"],
         "Theo định nghĩa: hai vectơ cùng phương nếu giá của chúng song song hoặc trùng nhau."),
        (r"Hai vectơ cùng phương thì", "chúng cùng hướng hoặc ngược hướng",
         ["chúng luôn cùng hướng", "chúng có cùng độ dài", "chúng bằng nhau", "giá của chúng luôn trùng nhau"],
         "Nếu hai vectơ cùng phương thì chúng chỉ có thể cùng hướng hoặc ngược hướng."),
        (r"Hai vectơ cùng hướng thì", "chúng cùng phương",
         ["chúng bằng nhau", "chúng có cùng độ dài", "giá của chúng vuông góc", "chúng có chung điểm cuối"],
         "Hai vectơ cùng hướng trước hết phải cùng phương (giá song song hoặc trùng nhau)."),
        (r"Vectơ-không là vectơ", "có điểm đầu và điểm cuối trùng nhau",
         ["có độ dài bằng $1$", "không có giá", "có điểm đầu là gốc toạ độ", "không cùng phương với vectơ nào"],
         r"Vectơ có điểm đầu và điểm cuối trùng nhau gọi là vectơ-không, kí hiệu $\overrightarrow{0}$."),
        (r"Ba điểm phân biệt $%s$, $%s$, $%s$ thẳng hàng khi và chỉ khi hai vectơ $%s$ và $%s$" % (X, Y, Z, xy, _vt(X, Z)),
         "cùng phương",
         ["cùng hướng", "ngược hướng", "có cùng độ dài", "bằng nhau"],
         r"$%s$, $%s$, $%s$ thẳng hàng khi và chỉ khi $%s$ và $%s$ có giá trùng nhau, tức là cùng phương (có thể cùng hướng hoặc ngược hướng)."
         % (X, Y, Z, xy, _vt(X, Z))),
        (r"Hai vectơ $%s$ và $%s$" % (xy, yx), "có cùng độ dài và ngược hướng",
         ["bằng nhau", "cùng hướng", "có độ dài khác nhau", "không cùng phương"],
         r"$%s$ và $%s$ có chung giá $%s$, cùng độ dài $%s$ nhưng hướng ngược nhau." % (xy, yx, X + Y, X + Y)),
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
            de = r"Vectơ có điểm đầu $%s$ và điểm cuối $%s$ được kí hiệu là" % (X, Y)
            dung = "$%s$" % _vt(X, Y)
            sai = ["$%s$" % (X + Y), "$%s$" % _vt(Y, X), r"$\left|%s\right|$" % _vt(X, Y)]
            ly = r"Vectơ có điểm đầu $%s$, điểm cuối $%s$ được kí hiệu là $%s$." % (X, Y, _vt(X, Y))
        elif kieu in ("dau", "cuoi"):
            de = r"Điểm %s của vectơ $%s$ là" % ("đầu" if kieu == "dau" else "cuối", _vt(X, Y))
            dung = "điểm $%s$" % (X if kieu == "dau" else Y)
            sai = ["điểm $%s$" % (Y if kieu == "dau" else X), "trung điểm của đoạn thẳng $%s$" % (X + Y),
                   "đường thẳng $%s$" % (X + Y)]
            ly = r"Vectơ $%s$ có điểm đầu là $%s$, điểm cuối là $%s$." % (_vt(X, Y), X, Y)
        else:
            de = r"Độ dài của vectơ $%s$ được kí hiệu là" % _vt(X, Y)
            dung = r"$\left|%s\right|$" % _vt(X, Y)
            sai = ["$%s$" % _vt(X, Y), "$%s$" % _vt(Y, X), r"$-%s$" % _vt(X, Y)]
            ly = r"Độ dài của vectơ $%s$ kí hiệu là $\left|%s\right|$, và $\left|%s\right| = %s$." % (
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
        mo = r"Cho ba điểm $%s$, $%s$, $%s$ thẳng hàng theo thứ tự đó (điểm $%s$ nằm giữa $%s$ và $%s$)." % (
            ten[0], ten[1], ten[2], ten[1], ten[0], ten[2])
    else:
        mo = r"Cho bốn điểm $%s$, $%s$, $%s$, $%s$ phân biệt, thẳng hàng theo thứ tự đó." % tuple(ten)
    return ten, mo, cap


def _b7_ly_cap(u, w, cung, ten):
    huong = lambda v: "từ $%s$ đến $%s$" % v
    return (r"$%s$ và $%s$ cùng nằm trên đường thẳng chứa các điểm, $%s$ có hướng %s, $%s$ có hướng %s nên chúng %s."
            % (_vt(*u), _vt(*w), _vt(*u), huong(u), _vt(*w), huong(w), "cùng hướng" if cung else "ngược hướng"))


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
        fmt = lambda c: r"$%s$ và $%s$" % (_vt(*c[0]), _vt(*c[1]))
        de = mo + r" Cặp vectơ nào sau đây %s?" % ("cùng hướng" if hoi_cung else "ngược hướng")
        ly = r"Các vectơ đều có giá là đường thẳng chứa các điểm nên cùng phương; xét hướng: " + _b7_ly_cap(d[0], d[1], d[2], ten)
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
        hoi = "cùng hướng" if hoi_cung else "ngược hướng"
        dong = r"\\ ".join(r"%d) $%s$ và $%s$" % (i + 1, _vt(*c[0]), _vt(*c[1])) for i, c in enumerate(chon))
        de = mo + r" Cho bốn cặp vectơ: \\ " + dong + r"\\ Có bao nhiêu cặp vectơ %s?" % hoi
        ly = (r"Các vectơ đều cùng phương (giá là đường thẳng chứa các điểm); chỉ cần so hướng:\\ "
              + r"\\ ".join(r"Cặp %d: %s" % (i + 1, "cùng hướng" if c[2] else "ngược hướng") for i, c in enumerate(chon))
              + r".\\ Vậy có $%d$ cặp vectơ %s." % (k, hoi))
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
         r"$%s = %s$ khi và chỉ khi $%s$ cùng hướng với $%s$ và $%s = %s$: từ $%s$ chỉ có đúng một điểm $%s$ như vậy."
         % (ab, cd, cd, ab, C + D, A + B, C, D), False),
        (r"$%s = %s$" % (_vt(D, C), ab), 1,
         r"$%s = %s$ thì $%s = %s$, tức $%s$ là điểm duy nhất sao cho vectơ từ $%s$ đến $%s$ bằng $%s$: có đúng một điểm."
         % (_vt(D, C), ab, cd, ba, D, C, D, ba), False),
        (r"$\left|%s\right| = \left|%s\right|$" % (ab, cd), "vô số",
         r"$\left|%s\right| = \left|%s\right| \Leftrightarrow %s = %s$: tập hợp các điểm $%s$ là đường tròn tâm $%s$, bán kính $%s$, nên có vô số điểm."
         % (ab, cd, C + D, A + B, D, C, A + B), False),
        (r"$%s$ cùng phương với $%s$ ($%s \ne %s$)" % (cd, ab, D, C), "vô số",
         r"$%s$ cùng phương với $%s$ khi $%s$ thuộc đường thẳng qua $%s$ song song (hoặc trùng) với đường thẳng $%s$, khác $%s$: có vô số điểm."
         % (cd, ab, D, C, A + B, C), False),
        (r"$%s$ cùng phương với $%s$ và $\left|%s\right| = \left|%s\right|$" % (cd, ab, cd, ab), 2,
         r"$%s$ thuộc đường thẳng qua $%s$ cùng phương với $%s$ và $%s = %s$: có hai điểm, đối xứng nhau qua $%s$ (một điểm cho $%s$ cùng hướng, một điểm cho $%s$ ngược hướng với $%s$)."
         % (D, C, ab, C + D, A + B, C, cd, cd, ab), False),
        (r"$%s$ cùng phương với $%s$ và $\left|%s\right| = %d\left|%s\right|$" % (cd, ab, cd, k, ab), 2,
         r"$%s$ thuộc đường thẳng qua $%s$ cùng phương với $%s$ và $%s = %d%s$: có hai điểm, đối xứng nhau qua $%s$."
         % (D, C, ab, C + D, k, A + B, C), False),
        (r"$%s$ cùng hướng với $%s$ và $\left|%s\right| = %d\left|%s\right|$" % (cd, ab, cd, k, ab), 1,
         r"Trên đường thẳng qua $%s$ cùng phương với $%s$, chỉ có một điểm $%s$ để $%s$ cùng hướng với $%s$ và $%s = %d%s$."
         % (C, ab, D, cd, ab, C + D, k, A + B), False),
        (r"$%s$ ngược hướng với $%s$ và $\left|%s\right| = \left|%s\right|$" % (cd, ab, cd, ab), 1,
         r"Khi đó $%s = %s$: chỉ có đúng một điểm $%s$." % (cd, ba, D), False),
        (r"$%s$ cùng phương với $%s$ và $%s$ thuộc đường thẳng $%s$" % (cd, ab, D, A + B), 0,
         r"$%s$ cùng phương với $%s$ thì $%s$ thuộc đường thẳng qua $%s$ song song với $%s$; đường thẳng này không cắt đường thẳng $%s$ (vì $%s$ không thuộc $%s$). Vậy không có điểm nào."
         % (cd, ab, D, C, A + B, A + B, C, A + B), True),
        (r"$%s = %s$" % (_vt(D, A), _vt(D, B)), 0,
         r"$%s = %s$ thì $%s$ trùng $%s$, trái giả thiết $%s \ne %s$. Vậy không có điểm nào." % (_vt(D, A), _vt(D, B), A, B, A, B), False),
        (r"$%s = %s$" % (_vt(A, D), _vt(D, B)), 1,
         r"$%s = %s$ khi và chỉ khi $%s$ là trung điểm của đoạn thẳng $%s$: có đúng một điểm." % (_vt(A, D), _vt(D, B), D, A + B), False),
        (r"$\left|%s\right| = \left|%s\right|$" % (_vt(D, A), _vt(D, B)), "vô số",
         r"$%s = %s$: $%s$ thuộc đường trung trực của đoạn thẳng $%s$, có vô số điểm." % (D + A, D + B, D, A + B), False),
    ]
    dk, so, ly, can_ngoai = random.choice(ds)
    if can_ngoai:
        mo = (r"Cho hai điểm phân biệt $%s$, $%s$ và điểm $%s$ không thuộc đường thẳng $%s$. Có bao nhiêu điểm $%s$ thoả mãn %s?"
              % (A, B, C, A + B, D, dk))
    elif C in dk.replace(D, ""):
        mo = r"Cho hai điểm phân biệt $%s$, $%s$ và điểm $%s$. Có bao nhiêu điểm $%s$ thoả mãn %s?" % (A, B, C, D, dk)
    else:
        mo = r"Cho hai điểm phân biệt $%s$, $%s$. Có bao nhiêu điểm $%s$ thoả mãn %s?" % (A, B, D, dk)
    return mo, so, ly


def L10_C4_B7_NB037_MC_F_01(socau, dang=1):
    r"""Đếm số điểm $D$ thoả một điều kiện về vectơ: bằng nhau, cùng độ dài (đường tròn, trung trực), cùng phương,
    cùng phương và cùng độ dài, vectơ-không... Đáp án trong $\{$vô số; $0$; $1$; $2\}$. Theo câu mẫu cô Lan gửi
    ($\left|\overrightarrow{AB}\right| = \left|\overrightarrow{CD}\right|$: vô số).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        mo, so, ly = _b7_dieu_kien_D()
        tat_ca = ["Vô số", "$0$", "$1$", "$2$"]
        dung = "Vô số" if so == "vô số" else "$%d$" % so
        cau += MC_SA_answer_text(mo, dung, [x for x in tat_ca if x != dung], ly, 0, 0, dang)
    return cau


def L10_C4_B7_NB037_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn cùng dạng NB037_MC_F: chỉ dùng điều kiện có HỮU HẠN điểm $D$ ($0$, $1$ hoặc $2$).

    CLAUDE THEM 16/10/2026 - co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        while True:
            mo, so, ly = _b7_dieu_kien_D()
            if so != "vô số":
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
        H["mo"] = r"Cho lục giác đều $%s$ tâm $%s$, cạnh $a$ (xem hình vẽ)." % (doi, tam)
        H["ly_do"] = r"lục giác đều cạnh $a$ ghép từ sáu tam giác đều cạnh $a$ chung đỉnh $%s$" % tam
        H["ly_do_dai"] = (r"lục giác đều cạnh $a$: cạnh và đoạn nối tâm với đỉnh bằng $a$, đường chéo ngắn bằng $a\sqrt{3}$, "
                          r"đường chéo qua tâm bằng $2a$")
    elif kieu == "hbh":
        H["mo"] = r"Cho hình bình hành $%s$ tâm $%s$ (xem hình vẽ)." % ("".join(H["da_giac"]), H["tam"])
        H["ly_do"] = "các cạnh đối của hình bình hành song song và bằng nhau, tâm là trung điểm của hai đường chéo"
    else:
        H["ly_do"] = "tính chất trung điểm và đường trung bình của tam giác: đường trung bình song song và bằng nửa cạnh thứ ba"
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
        return (r"{\True %s}" % phat if dung else r"{%s}" % phat, ("Đúng. " if dung else "Sai. ") + ly)

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
                              r"$%s$ và $%s$ cùng hướng và cùng độ dài nên bằng nhau (%s)." % (vt(u), vt(w), H["ly_do"])))
            elif cung_do_dai or cung:
                a.append(dong(r"$%s = %s$" % (vt(u), vt(w)), False,
                              r"$%s$ và $%s$ %s nên không bằng nhau." % (vt(u), vt(w), "ngược hướng" if not cung else "có độ dài khác nhau")))
            if not set(u) & set(w):
                hoi = random.choice(["cùng hướng", "ngược hướng"])
                a.append(dong(r"$%s$ và $%s$ %s" % (vt(u), vt(w), hoi), cung == (hoi == "cùng hướng"),
                              r"$%s$ và $%s$ cùng phương và %s (%s)." % (vt(u), vt(w), "cùng hướng" if cung else "ngược hướng", H["ly_do"])))

    # ---------------- b) TH: cung phuong (khong tam thuong), vecto doi, ti so do dai
    b = []
    for i, u in enumerate(vts):
        for w in vts[i + 1:]:
            if set(u) & set(w):
                continue
            cp = _tfc_cp(V[u], V[w])
            b.append(dong(r"$%s$ và $%s$ cùng phương" % (vt(u), vt(w)), cp,
                          (r"Giá của $%s$ và $%s$ song song hoặc trùng nhau nên hai vectơ cùng phương." if cp else
                           r"Giá của $%s$ và $%s$ cắt nhau nên hai vectơ không cùng phương.") % (vt(u), vt(w))))
            if cp:
                doi = _tfc_bang(V[u], (-V[w][0], -V[w][1]))
                b.append(dong(r"$%s$ và $%s$ là hai vectơ đối nhau" % (vt(u), vt(w)), doi,
                              (r"$%s$ và $%s$ ngược hướng, cùng độ dài nên là hai vectơ đối nhau (%s)." if doi else
                               r"$%s$ và $%s$ không ngược hướng hoặc không cùng độ dài nên không phải hai vectơ đối nhau.")
                              % ((vt(u), vt(w), H["ly_do"]) if doi else (vt(u), vt(w)))))
                r = _tfc_dai(V[u]) / _tfc_dai(V[w])
                for k in (0.5, 2):
                    if abs(r - k) < 1e-9:
                        b.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (vt(u), _tfc_k(k), vt(w)), True,
                                      r"$%s = %s%s$ (%s)." % ("".join(u), _tfc_k(k), "".join(w), H["ly_do"])))
                        sai_k = 2 if k == 0.5 else 0.5
                        b.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (vt(u), _tfc_k(sai_k), vt(w)), False,
                                      r"Thực ra $%s = %s%s$ (%s)." % ("".join(u), _tfc_k(k), "".join(w), H["ly_do"])))
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
                buoc = (r"Vì $%s %s %s$ nên $%s = %s + %s = %s$ (quy tắc ba điểm)."
                        % (("-" + vt(v)) if phep == "-" else vt(v), "=", vt(t), bt, vt(u), vt(t),
                           vt(cuoi) if cuoi[0] != cuoi[1] else r"\overrightarrow{0}"))
                buoc_dung = buoc
                if ket != (vt(cuoi) if cuoi[0] != cuoi[1] else r"\overrightarrow{0}"):
                    buoc_dung += r" Mà $%s = %s$ (%s)." % (vt(cuoi), ket, H["ly_do"])
                c.append(dong(r"$%s = %s$" % (bt, ket), True, buoc_dung))
                # sai: nguoc chieu / doi phep tinh
                sai_z = (-z[0], -z[1])
                sai = ten_vt(sai_z) if _tfc_dai(z) > 1e-9 else None
                if sai:
                    c.append(dong(r"$%s = %s$" % (bt, sai), False, buoc + r" Không phải $%s$." % sai))
                z2 = (V[u][0] - V[v][0], V[u][1] - V[v][1]) if phep == "+" else (V[u][0] + V[v][0], V[u][1] + V[v][1])
                sai2 = ten_vt(z2)
                if sai2 and not _tfc_bang(z2, z):
                    c.append(dong(r"$%s = %s$" % (bt, sai2), False, buoc + r" Không phải $%s$." % sai2))
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
                                       buoc + r" Do đó $\left|%s\right| = %s = %s$ (%s)." % (bt, "".join(cuoi), that, H["ly_do_dai"])))
                else:
                    for w in vts:
                        if set(w) == set(cuoi) or not _tfc_cp(V[w], z):
                            continue
                        r = L / _tfc_dai(V[w])
                        for k in (0.5, 2):
                            if abs(r - k) < 1e-9:
                                ly = buoc + r" Do đó $\left|%s\right| = %s = %s%s$ (%s)." % (bt, "".join(cuoi), _tfc_k(k), "".join(w), H["ly_do"])
                                d_.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (bt, _tfc_k(k), vt(w)), True, ly))
                                d_.append(dong(r"$\left|%s\right| = %s\left|%s\right|$" % (bt, _tfc_k(2 if k == 0.5 else 0.5), vt(w)),
                                               False, ly))
                    # |u + v| = |w| voi w bang hoac doi z (khac ten): dung; voi w cung phuong khac do dai: sai
                    for w in vts:
                        if set(w) == set(cuoi) or not _tfc_cp(V[w], z):
                            continue
                        bang_dd = abs(_tfc_dai(V[w]) - L) < 1e-9
                        ly = buoc + r" Do đó $\left|%s\right| = %s$, %s $%s$ (%s)." % (
                            bt, "".join(cuoi), "bằng" if bang_dd else "khác", "".join(w), H["ly_do"])
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
        debai = H["mo"] + " Xét tính đúng sai của các khẳng định sau:"
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
    "tau_bien_dong": ("Trên biển Đông, một tàu chuyển động đều", "tàu", [15, 18, 20, 24, 25, 30]),
    "ca_no_tren_ho": ("Trên một hồ nước rộng, một ca nô chuyển động đều", "ca nô", [20, 24, 30, 36, 40]),
    "may_bay": ("Một máy bay bay thẳng đều", "máy bay", [600, 640, 720, 800, 840]),
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
        tg, doi = r"$%d$ giờ" % (t_ph // 60), ""
        t_tex = "%d" % (t_ph // 60)
    else:
        tg = (r"$%d$ giờ $%d$ phút" % (t_ph // 60, t_ph % 60)) if t_ph > 60 else r"$%d$ phút" % t_ph
        t_tex = _vd039_so(t_ph / 60)
        doi = r"Đổi %s $= %s$ giờ. " % (tg, t_tex)
    de = (r"%s từ vị trí $A$ theo hướng %s với vận tốc $%d$ km/h. Sau %s, %s đến được vị trí $B$."
          % (mo, _vd039_huong(d1, goc, d2), v, tg, ten))
    ve = (doi + r"Vectơ vận tốc có hướng %s và độ lớn $%d$ km/h, nên vectơ độ dời $\overrightarrow{AB}$ cùng hướng với "
          r"vectơ vận tốc và có độ dài $AB = %d\cdot %s = %s$ (km).\\ "
          r"Vectơ $\overrightarrow{BA}$ ngược hướng với $\overrightarrow{AB}$: đổi $\mathrm{%s}$ thành $\mathrm{%s}$, $\mathrm{%s}$ "
          r"thành $\mathrm{%s}$, giữ nguyên góc $%d^\circ$. Vậy $A$ ở hướng %s so với $B$."
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
        de += r" Hỏi $A$ cách $B$ bao nhiêu kilômét và ở hướng nào so với $B$?"
        p = lambda kc, hh: r"$%s$ km, hướng %s" % (_vd039_so(kc), _vd039_huong(*hh))
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
        de += r" Hỏi $A$ cách $B$ bao nhiêu kilômét?"
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
    "chim": r"Một vật $A$ được thả vào một cốc chất lỏng, chìm hoàn toàn và nằm yên dưới đáy cốc.",
    "lo_lung": r"Một vật $A$ được thả vào một cốc chất lỏng và nằm lơ lửng, chìm hoàn toàn trong chất lỏng.",
    "noi": r"Một vật $A$ đang chìm hoàn toàn trong một cốc chất lỏng và đang nổi lên.",
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
        de = (_VD039B_TINH_HUONG[th] + r" Hình bên biểu diễn lực đẩy Archimedes $\overrightarrow{F}$ và trọng lực "
              r"$\overrightarrow{P}$ tác động lên vật $A$ (độ dài vectơ tỉ lệ với độ lớn của lực). Gọi $d_A$, $d_\ell$ lần lượt là "
              r"trọng lượng riêng của vật $A$ và của chất lỏng. Tỉ số $\dfrac{%s}{%s}$ bằng"
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
        giai = (r"Vật $A$ chìm hoàn toàn nên thể tích chất lỏng bị chiếm chỗ bằng thể tích $V$ của vật: "
                r"$\left|\overrightarrow{F}\right| = d_\ell V$, $\left|\overrightarrow{P}\right| = d_A V$.\\ "
                r"Trên hình, $\overrightarrow{F}$ dài $%d$ ô, $\overrightarrow{P}$ dài $%d$ ô nên "
                r"$\dfrac{d_A}{d_\ell} = \dfrac{\left|\overrightarrow{P}\right|}{\left|\overrightarrow{F}\right|} = %s$"
                % (F, P, _vd039b_ps(P, F)))
        giai += (r", do đó $\dfrac{d_\ell}{d_A} = %s$." % _vd039b_ps(F, P)) if hoi_nguoc else "."
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
        de = (_VD039B_TINH_HUONG[th] + r" Hình nào sau đây biểu diễn đúng lực đẩy Archimedes $\overrightarrow{F}$ và trọng "
              r"lực $\overrightarrow{P}$ tác động lên vật $A$ (độ dài vectơ tỉ lệ với độ lớn của lực)?")
        ly = {"chim": r"vật chìm xuống đáy nên trọng lực lớn hơn lực đẩy: $\left|\overrightarrow{P}\right| > \left|\overrightarrow{F}\right|$",
              "lo_lung": r"vật lơ lửng nên hai lực cân bằng: $\left|\overrightarrow{P}\right| = \left|\overrightarrow{F}\right|$",
              "noi": r"vật đang nổi lên nên lực đẩy lớn hơn trọng lực: $\left|\overrightarrow{F}\right| > \left|\overrightarrow{P}\right|$"}[th]
        giai = (r"Trọng lực $\overrightarrow{P}$ hướng thẳng đứng xuống dưới, lực đẩy Archimedes $\overrightarrow{F}$ hướng thẳng "
                r"đứng lên trên (hai vectơ ngược hướng, cùng giá thẳng đứng); " + ly
                + r". Chỉ một hình thoả mãn cả hướng và quan hệ độ dài.")
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
        de = (_VD039B_TINH_HUONG[th] + r" Hình bên biểu diễn lực đẩy Archimedes $\overrightarrow{F}$ và trọng lực "
              r"$\overrightarrow{P}$ tác động lên vật $A$ (độ dài vectơ tỉ lệ với độ lớn của lực). Gọi $d_A$, $d_\ell$ lần lượt là "
              r"trọng lượng riêng của vật $A$ và của chất lỏng. Tính tỉ số $\dfrac{%s}{%s}$ (viết dưới dạng số thập phân)."
              % ((r"d_\ell", "d_A") if nguoc else ("d_A", r"d_\ell")))
        v = F / P if nguoc else P / F
        dap = ("%g" % v).replace(".", ",")
        giai = (r"Vật $A$ chìm hoàn toàn nên $\left|\overrightarrow{F}\right| = d_\ell V$, $\left|\overrightarrow{P}\right| = d_A V$ "
                r"($V$ là thể tích vật). Trên hình, $\overrightarrow{F}$ dài $%d$ ô, $\overrightarrow{P}$ dài $%d$ ô nên "
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
            ly = (r"Theo quy tắc ba điểm: $%s = %s$, đúng với \emph{mọi} vị trí của $%s$, $%s$, $%s$."
                  % (ve.tex, trai.tex, U, V, W))
        else:
            ly = (r"Theo quy tắc ba điểm: $%s + %s = %s$; phép cộng vectơ có tính chất giao hoán nên $%s = %s$, "
                  r"đúng với \emph{mọi} vị trí của $%s$, $%s$, $%s$."
                  % (_vt(U, W), _vt(W, V), trai.tex, ve.tex, trai.tex, U, V, W))
    else:
        ly = (r"Theo quy tắc trừ (hai vectơ chung điểm đầu $%s$): $%s = %s$, đúng với \emph{mọi} vị trí của "
              r"$%s$, $%s$, $%s$." % (a[0], ve.tex, trai.tex, U, V, W))
    ly += (r"\\ Các khẳng định còn lại sai vì: "
           + "; ".join(r"$%s = %s \ne %s$" % (n[1].tex, n[3], trai.tex) for n in nhieu) + ".")
    debai = (r"Cho ba điểm $%s$, $%s$, $%s$ phân biệt bất kì. Khẳng định nào sau đây luôn đúng?"
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
        giai = (r"Áp dụng quy tắc hình bình hành tại đỉnh $%s$: hai cạnh xuất phát từ $%s$ là $%s$, $%s$, đường chéo "
                r"xuất phát từ $%s$ là $%s$, nên $%s + %s = %s$."
                % (X, X, _vt(X, U), _vt(X, W), X, phai.tex, _vt(X, U), _vt(X, W), phai.tex))
        giai += (r"\\ Các khẳng định còn lại sai vì: "
                 + "; ".join(r"$%s = %s \ne %s$" % (l.tex, _b5_rut_diem(l, envs, _b5_cap_trong(l), ten), phai.tex)
                             for _, l in nhieu) + ".")
        debai = r"Cho hình bình hành $%s$. Khẳng định nào sau đây đúng?" % "".join(ten)
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
    muc, q = ("hàng phần trăm", "0.01") if x < 10 else ("hàng phần mười", "0.1")
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
            mo = r"Cho hình vuông $%s$ cạnh $%s$" % (ten, _b8_tex(p))
        elif kieu == "hcn":
            if not so:
                p, q = random.choice([(_A8, 2 * _A8), (2 * _A8, _A8), (_A8, _A8 * r3), (_A8 * r3, _A8), (3 * _A8, 4 * _A8),
                                      (4 * _A8, 3 * _A8)])
            else:
                p, q = random.choice([(3, 4), (4, 3), (6, 8), (8, 6), (5, 12)] + [tuple(random.sample(range(2, 10), 2))] * 3)
            P = {A: (0, 0), B: (p, 0), C: (p, q), D: (0, q)}
            mo = r"Cho hình chữ nhật $%s$ có $%s = %s$, $%s = %s$" % (ten, A + B, _b8_tex(p), A + D, _b8_tex(q))
        else:
            p = _A8 if not so else random.randint(2, 9)
            q = p
            P = {A: (0, 0), B: (p, 0), D: (p / _sp8.Integer(2), p * r3 / 2)}
            P[C] = (P[B][0] + P[D][0], P[B][1] + P[D][1])
            mo = r"Cho hình thoi $%s$ cạnh $%s$ có $\widehat{%s} = 60^\circ$" % (ten, _b8_tex(p), B + A + D)
        O = "O" if "O" not in ten else "I"
        P[O] = ((P[A][0] + P[C][0]) / 2, (P[A][1] + P[C][1]) / 2)
        H.update(dinh=list(ten), O=O, P=P,
                 mo=lambda co_O, mo=mo, O=O: mo + ((r" và hai đường chéo cắt nhau tại $%s$." % O) if co_O else "."))
        L = {}
        for X, Y, d in ((A, B, p), (B, C, q), (C, D, p), (D, A, q)):
            L[frozenset((X, Y))] = (d, None)
        if kieu in ("vuong", "hcn"):
            cheo = _sp8.sqrt(p ** 2 + q ** 2)
            for X, Y, Z in ((A, B, C), (B, C, D)):
                L[frozenset((X, Z))] = (cheo, r"$%s = \sqrt{%s^2 + %s^2} = \sqrt{%s + %s} = %s$ (định lí Pythagore trong "
                                               r"tam giác $%s$ vuông tại $%s$)"
                                        % (X + Z, X + Y, Y + Z, _b8_tex(_sp8.expand(L[frozenset((X, Y))][0] ** 2)),
                                           _b8_tex(_sp8.expand(L[frozenset((Y, Z))][0] ** 2)), _b8_tex(cheo), X + Y + Z, Y))
            for X in ten:
                L[frozenset((O, X))] = (cheo / 2, r"$%s$ là trung điểm của hai đường chéo nên $%s = \dfrac{1}{2}%s = %s$"
                                        % (O, O + X, A + C if X in (A, C) else B + D, _b8_tex(cheo / 2)))
        else:
            L[frozenset((B, D))] = (p, r"tam giác $%s$ có $%s = %s$ và $\widehat{%s} = 60^\circ$ nên là tam giác đều, "
                                       r"$%s = %s$" % (A + B + D, A + B, A + D, B + A + D, B + D, _b8_tex(p)))
            L[frozenset((A, C))] = (p * r3, r"$%s$ là trung điểm của $%s$ và $%s$ vuông góc $%s$ nên $%s = 2%s = "
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
        mo = r"Cho tam giác đều $%s$ cạnh $%s$." % (ten, _b8_tex(p))
    else:
        if not so:
            p, q = random.choice([(_A8, _A8 * r3), (_A8 * r3, _A8), (3 * _A8, 4 * _A8), (4 * _A8, 3 * _A8), (_A8, 2 * _A8),
                                  (2 * _A8, _A8)])
        else:
            p, q = random.choice([(6, 8), (8, 6), (3, 4), (5, 12), (12, 5)] + [tuple(random.sample(range(2, 10), 2))] * 3)
        P = {A: (0, 0), B: (p, 0), C: (0, q)}
        bc = _sp8.sqrt(p ** 2 + q ** 2)
        L = {frozenset((A, B)): (p, None), frozenset((A, C)): (q, None),
             frozenset((B, C)): (bc, r"$%s = \sqrt{%s^2 + %s^2} = \sqrt{%s + %s} = %s$ (định lí Pythagore)"
                                 % (B + C, A + B, A + C, _b8_tex(_sp8.expand(p ** 2)), _b8_tex(_sp8.expand(q ** 2)),
                                    _b8_tex(bc)))}
        mo = r"Cho tam giác $%s$ vuông tại $%s$ có $%s = %s$, $%s = %s$." % (ten, A, A + B, _b8_tex(p), A + C, _b8_tex(q))
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
                    ly = r"$%s + %s = %s$ (quy tắc ba điểm)" % (_vt(*u), _vt(*v), _vt(P_, S))
                elif P_ == R:
                    wv = _b8_vec(H, R, S)
                    T = _b8_tim(H, (Q, wv), diem)
                    if T and T != P_:
                        kq, nhom = (P_, T), "hbh"
                        ly = (r"$%s%s%s%s$ là hình bình hành nên $%s + %s = %s$ (quy tắc hình bình hành)"
                              % (P_, Q, T, S, _vt(*u), _vt(*v), _vt(P_, T)))
                if kq is None and Q != R and P_ != R:
                    T = _b8_tim(H, (Q, _b8_vec(H, R, S)), diem)
                    if T and T != P_:
                        kq, nhom = (P_, T), "thay"
                        ly = (r"$%s = %s$ nên $%s + %s = %s + %s = %s$"
                              % (_vt(*v), _vt(Q, T), _vt(*u), _vt(*v), _vt(*u), _vt(Q, T), _vt(P_, T)))
            else:
                if P_ == R and Q != S:
                    kq, nhom = (S, Q), "tru"
                    ly = r"$%s - %s = %s$ (quy tắc trừ)" % (_vt(*u), _vt(*v), _vt(S, Q))
                elif Q == S and P_ != R:
                    kq, nhom = (P_, R), "doi"
                    ly = (r"$%s - %s = %s + %s = %s$ (vectơ đối, quy tắc ba điểm)"
                          % (_vt(*u), _vt(*v), _vt(*u), _vt(S, R), _vt(P_, R)))
                elif P_ != R:
                    T = _b8_tim(H, (P_, _b8_vec(H, R, S)), diem)
                    if T and T != Q:
                        kq, nhom = (T, Q), "thay"
                        ly = (r"$%s = %s$ nên $%s - %s = %s - %s = %s$ (quy tắc trừ)"
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
                        ly = r"Ta có $%s = " % bt_goc
                        if phep == "-":
                            ly += r"%s + %s = " % (_vt(*d1), _vt(*e2))
                        ly += (r"\left(%s + %s\right) + \left(%s + %s\right) = %s + %s$ (vì $%s + %s = \overrightarrow{0}$). "
                               r"Hai vectơ $%s$, $%s$ bằng nhau (hai cạnh đối của hình bình hành) nên "
                               r"$\left|%s + %s\right| = 2%s$"
                               % (_vt(d1[0], Y), _vt(Y, d1[1]), _vt(e2[0], Z), _vt(Z, e2[1]), _vt(*w1), _vt(*w2),
                                  _vt(Y, d1[1]), _vt(Z, e2[1]), _vt(*w1), _vt(*w2), _vt(*w1), _vt(*w2),
                                  w1[0] + w1[1]))
                        dd, ly_dd = H["L"][frozenset(w1)]
                        ly = (ly[:-1] + r" = %s$" % _b8_tex(2 * dd)) if ly_dd is None else (ly + r", mà %s" % ly_dd)
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
                ly = (r"Gọi $%s$ là trung điểm của $%s$, dựng hình bình hành $%s%s%s%s$ thì $%s + %s = %s$ (quy tắc hình "
                      r"bình hành) và $%s$ là trung điểm của $%s$. Tam giác đều cạnh $%s$ có đường trung tuyến "
                      r"$%s = %s$ nên $%s = 2%s = %s$"
                      % (M, Y + Z, X, Y, T, Z, _vt(X, Y), _vt(X, Z), _vt(X, T), M, X + T, _b8_tex(H["canh"]), X + M,
                         _b8_tex(H["canh"] * _sp8.sqrt(3) / 2), X + T, X + M, _b8_tex(d)))
            else:
                d = H["L"][frozenset((B, C))][0]
                ly = (r"Dựng hình chữ nhật $%s%s%s%s$ thì $%s + %s = %s$ (quy tắc hình bình hành) và $%s = %s$ (hai "
                      r"đường chéo của hình chữ nhật bằng nhau). Mà %s"
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
    giai = (ly if not kq else r"Ta có %s" % ly) + "."
    if ly_dd:
        giai += r"\\ Mà %s." % ly_dd
    giai += r"\\ Do đó $\left|%s\right| = %s$." % (bt, _b8_tex(d))
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
        debai = mo + r" Độ dài của vectơ $%s$ bằng" % bt
        # nhiễu thứ nhất luôn là lỗi hay gặp |u| + |v| (nếu khác đáp số), hai nhiễu còn lại chọn ngẫu nhiên
        chon = nhieu[:1] + random.sample(nhieu[1:], 2)
        cau += MC_SA_answer_text(debai, "$%s$" % _b8_tex(d), ["$%s$" % _b8_tex(x) for x in chon], giai, 0, 0, dang)
    return cau


def _b8_sa_do_dai(phep, socau, dang):
    cau = ""
    for _ in range(socau):
        mo, bt, d, nhieu, giai = _b8_do_dai(phep, True)
        dap, muc = _b8_sa(d)
        debai = mo + r" Tính $\left|%s\right|$%s." % (bt, (r" (làm tròn kết quả đến %s)" % muc) if muc else "")
        if muc:
            giai += r" Vậy $\left|%s\right| \approx %s$." % (bt, dap)
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
        quan_he = r"hai lực $%s$, $%s$ cùng phương, cùng chiều" % (F1, F2)
    elif g == 180:
        quan_he = r"hai lực $%s$, $%s$ cùng phương, ngược chiều" % (F1, F2)
    else:
        quan_he = r"góc giữa hai vectơ $%s$, $%s$ bằng $%d^\circ$" % (F1, F2, g)
    dap, tron = _b8_luc_so(R)
    lam_tron = r" (làm tròn kết quả đến hàng phần mười)" if tron else ""
    if can_bang:
        debai = (r"Một vật đứng yên dưới tác dụng của ba lực $%s$, $%s$, $%s$, trong đó %s và %s. Tính độ lớn của lực "
                 r"$%s$%s." % (F1, F2, F3, so, quan_he, F3, lam_tron))
        giai = (r"Vật đứng yên (cân bằng) nên $%s + %s + %s = \overrightarrow{0}$, suy ra $%s = -\left(%s + %s\right)$, "
                r"do đó $%s = \left|%s + %s\right|$.\\ " % (F1, F2, F3, F3, F1, F2, do(F3), F1, F2))
        hoi = do(F3)
    else:
        debai = (r"Hai lực $%s$, $%s$ cùng tác dụng vào một vật, trong đó %s và %s. Tính độ lớn hợp lực "
                 r"$%s + %s$%s." % (F1, F2, so, quan_he, F1, F2, lam_tron))
        giai, hoi = "", r"\left|%s + %s\right|" % (F1, F2)
    tong = r"\left|%s + %s\right|" % (F1, F2)
    if g == 0:
        giai += r"Hai lực cùng hướng nên $%s = %d + %d = %d\ \text{N}$." % (tong, p, q, p + q)
    elif g == 180:
        giai += (r"Hai lực ngược hướng nên $%s = \left|%d - %d\right| = %d\ \text{N}$%s." % (tong, p, q, abs(p - q),
                 r" (hai lực đối nhau, hợp lực bằng $\overrightarrow{0}$)" if p == q else ""))
    else:
        R2 = _sp8.nsimplify(R ** 2)
        giai += (r"Đặt $\overrightarrow{OA} = %s$, $\overrightarrow{OB} = %s$ và dựng hình bình hành $OACB$ thì "
                 r"$%s + %s = \overrightarrow{OC}$ (quy tắc hình bình hành). Tam giác $OAC$ có $OA = %d$, $AC = OB = %d$, "
                 r"$\widehat{OAC} = 180^\circ - %d^\circ = %d^\circ$. Theo định lí côsin:\\ "
                 r"$OC^2 = OA^2 + AC^2 - 2\cdot OA\cdot AC\cdot\cos\widehat{OAC} = %d^2 + %d^2 - 2\cdot %d\cdot %d\cdot\cos %d^\circ "
                 r"= %s$.\\ " % (F1, F2, F1, F2, p, q, g, 180 - g, p, q, p, q, 180 - g, _b8_tex(R2)))
        if tron:
            giai += r"Vậy $%s = OC = \sqrt{%s} \approx %s\ \text{N}$." % (tong, _b8_tex(R2), dap)
        else:
            giai += r"Vậy $%s = OC = \sqrt{%s} = %s\ \text{N}$." % (tong, _b8_tex(R2), dap)
    if can_bang:
        giai += r"\\ Vậy $%s %s %s\ \text{N}$." % (hoi, r"\approx" if tron else "=", dap)
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
        debai = debai[:-1] + r" (đơn vị: N)."
        d = float(dap.replace(",", "."))
        du = [_xx4(d + k, 1) for k in (1, -1, 2, -2, 3, 5) if d + k > 0]
        cau += MC_SA_answer_const(debai, dap, ds + du, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# B11_VD060_B (vận tốc thực = tổng hai vectơ vận tốc) và VD060_C (hợp lực trong bối cảnh thực tế). Bài toán thực tế
# tách riêng chữ C với VD060_A (không thực tế) theo ý cô Lan 16/10/2026.
# ---------------------------------------------------------------------
_B8_MUC = {0: "hàng đơn vị", 1: "hàng phần mười", 2: "hàng phần trăm"}


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
        gi = (r"Vì $%s \perp %s$ nên hình bình hành dựng trên hai vectơ này là hình chữ nhật, do đó "
              r"$%s = \sqrt{%s^2 + %s^2} = \sqrt{%s}" % (u, w, tong, _b8_so(p), _b8_so(q), _b8_so(p * p + q * q)))
    else:
        R2 = _sp8.sympify(p ** 2 + q ** 2 + 2 * p * q * _sp8.cos(_sp8.pi * g / 180))
        gt = _b8_tex(R2) if R2.is_Rational or g in (30, 45, 60, 120, 135, 150) else r"\approx %s" % _b8_tron(R2, 2)
        gi = (r"Đặt $\overrightarrow{OA} = %s$, $\overrightarrow{OB} = %s$ và dựng hình bình hành $OACB$ thì "
              r"$%s + %s = \overrightarrow{OC}$ (quy tắc hình bình hành). Tam giác $OAC$ có $OA = %s$, $AC = OB = %s$, "
              r"$\widehat{OAC} = 180^\circ - %d^\circ = %d^\circ$. Theo định lí côsin:\\ "
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
            huong = r"mũi ca nô luôn hướng vuông góc với bờ"
        elif g < 90:
            huong = r"mũi ca nô luôn hướng chếch xuôi dòng, hợp với hướng dòng nước một góc $%d^\circ$" % g
        else:
            huong = r"mũi ca nô luôn hướng chếch ngược dòng, hợp với hướng dòng nước một góc $%d^\circ$" % g
        de = (r"Một ca nô chạy qua một khúc sông thẳng, %s. Vận tốc riêng của ca nô (so với dòng nước) có độ lớn $%d$ "
              r"km/h, dòng nước chảy song song với bờ với vận tốc $%d$ km/h." % (huong, p, q))
        dv, so_le = "km/h", 1
        hoi_qd = random.random() < 0.4
        ten = r"ca nô"
    elif bc == "nguoi_boi_qua_song":
        p = _sp8.Rational(random.choice([10, 12, 13, 14, 15, 16, 18, 20]), 10)
        q = _sp8.Rational(random.choice([4, 5, 6, 7, 8, 9]), 10)
        g = 90
        de = (r"Một người bơi qua một con sông, luôn bơi theo hướng vuông góc với bờ với vận tốc riêng (so với dòng "
              r"nước) có độ lớn $%s$ m/s; dòng nước chảy song song với bờ với vận tốc $%s$ m/s." % (_b8_so(p), _b8_so(q)))
        dv, so_le, ten = "m/s", 2, r"người đó"
    else:
        p, q = random.randint(8, 20), random.randint(2, 8)
        g, gio = random.choice([(90, "hướng Bắc"), (90, "hướng Nam"), (45, "hướng Đông Bắc"), (135, "hướng Tây Bắc"),
                                (45, "hướng Đông Nam"), (135, "hướng Tây Nam")])
        de = (r"Một flycam bay theo hướng Đông với vận tốc riêng (so với không khí) có độ lớn $%d$ m/s; gió thổi theo "
              r"%s với vận tốc $%d$ m/s." % (p, gio, q))
        dv, so_le, ten = "m/s", 1, r"flycam"
    R = _b8_tong_hai(p, q, g)
    giai = (r"Gọi $%s$ là vận tốc riêng, $%s$ là vận tốc của %s; vận tốc thực tế là $\vec v = %s + %s$, "
            r"góc giữa $%s$ và $%s$ bằng $%d^\circ$.\\ "
            % (v1, v2, "dòng nước" if bc != "flycam_gap_gio" else "gió", v1, v2, v1, v2, g))
    if hoi_qd:
        t = random.choice([(15, _sp8.Rational(1, 4)), (20, _sp8.Rational(1, 3)), (30, _sp8.Rational(1, 2)),
                           (45, _sp8.Rational(3, 4)), (90, _sp8.Rational(3, 2))])
        hoi = r"Tính quãng đường thực tế ca nô đi được sau $%d$ phút" % t[0]
        dap = _b8_tron(R * t[1], 1)
        giai += _b8_giai_tong(v1, v2, p, q, g, dv, _b8_tron(R, 3), _b8_can_tron(R, 3))
        giai += (r"\\ Ca nô chuyển động thẳng đều với tốc độ $\left|\vec v\right|$ nên sau $%d$ phút $= %s$ giờ đi được "
                 r"$s = \left|\vec v\right|\cdot %s \approx %s$ (km)." % (t[0], _b8_tex(t[1]), _b8_tex(t[1]), dap))
        giai = giai if _b8_can_tron(R * t[1], 1) else giai.replace(r"\approx %s$ (km)" % dap, r"= %s$ (km)" % dap)
        nhieu = _b8_nhieu_tong(p * t[1], q * t[1], g, 1, dap)
        return de, hoi, dap, 1, nhieu, giai, "km", _b8_can_tron(R * t[1], 1)
    hoi = r"Tính tốc độ thực tế của %s" % ten
    dap = _b8_tron(R, so_le)
    giai += _b8_giai_tong(v1, v2, p, q, g, dv, dap, _b8_can_tron(R, so_le))
    return de, hoi, dap, so_le, _b8_nhieu_tong(p, q, g, so_le, dap), giai, dv, _b8_can_tron(R, so_le)


def _b8_cau_thuc_te(sinh, dang, mc):
    cau = ""
    for _ in range(1):
        de, hoi, dap, so_le, nhieu, giai, dv, tron = sinh()
        lam_tron = (r"làm tròn kết quả đến %s" % _B8_MUC[so_le]) if tron else ""
        if mc:
            debai = de + " " + hoi + ((r" (%s)." % lam_tron) if tron else ".")
            fm = lambda t: r"$%s$ %s" % (t, dv)
            return MC_SA_answer_text(debai, fm(dap), [fm(t) for t in nhieu[:3]], giai, 0, 0, dang)
        debai = de + " " + hoi + r" (đơn vị: %s%s)." % (dv, ("; " + lam_tron) if tron else "")
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
        de = (r"Hai người đứng trên bờ cùng kéo một con thuyền bằng hai sợi dây với các lực $%s$, $%s$ có độ lớn lần lượt "
              r"là $%d$ N và $%d$ N, góc giữa hai lực bằng $%d^\circ$." % (F1, F2, p, q, g))
        can, vat = "lực cản của nước", "con thuyền"
    elif bc == "tau_keo_sa_lan":
        p, q, dv = random.randint(20, 90), random.randint(20, 90), "kN"
        de = (r"Hai tàu kéo cùng kéo một sà lan bằng hai dây cáp với các lực $%s$, $%s$ có độ lớn lần lượt là $%d$ kN và "
              r"$%d$ kN, góc giữa hai dây cáp bằng $%d^\circ$." % (F1, F2, p, q, g))
        can, vat = "lực cản của nước", "sà lan"
    else:
        p, q, dv = random.randint(50, 200), random.randint(50, 200), "N"
        de = (r"Hai công nhân kéo một kiện hàng trên mặt sàn nằm ngang bằng hai sợi dây với các lực $%s$, $%s$ (song "
              r"song với mặt sàn) có độ lớn lần lượt là $%d$ N và $%d$ N, góc giữa hai lực bằng $%d^\circ$." % (F1, F2, p, q, g))
        can, vat = "lực ma sát", "kiện hàng"
    R = _b8_tong_hai(p, q, g)
    dap = _b8_tron(R, 0)
    giai = _b8_giai_tong(F1, F2, p, q, g, dv, dap, _b8_can_tron(R, 0))
    if deu:
        de += (r" Biết %s chuyển động thẳng đều theo hướng của hợp lực và %s (ngược hướng chuyển động) cân bằng "
               r"với hợp lực hai lực kéo." % (vat, can))
        hoi = r"Tính độ lớn của %s" % can
        giai = (r"Vật chuyển động thẳng đều nên %s $\overrightarrow{F_c}$ cân bằng với hợp lực: "
                r"$\overrightarrow{F_c} = -\left(%s + %s\right)$, do đó $\left|\overrightarrow{F_c}\right| = "
                r"\left|%s + %s\right|$.\\ " % (can, F1, F2, F1, F2)) + giai
    else:
        hoi = r"Tính độ lớn hợp lực của hai lực kéo tác dụng lên %s" % vat
        giai = r"Hợp lực là $\vec F = %s + %s$.\\ " % (F1, F2) + giai
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
# B8_VD040 (LUYỆN TẬP THÊM, ngoài YCCĐ): tập hợp điểm M thoả một đẳng thức độ dài vectơ trong hình bình hành
# (câu tự luận cô Lan gửi: |MB + CD| = |MC + DA| -> trung trực AB). MC (không có SA: đáp án không phải số) và TL.
# ---------------------------------------------------------------------
def _b8_ban_sao(V, X, P):
    """Cạnh hình bình hành V (theo thứ tự đỉnh): vectơ bằng vectơ XP nằm ở cạnh ĐỐI (X, P kề nhau)."""
    i, j = V.index(X), V.index(P)
    if (j - i) % 4 == 1:
        return V[(i - 1) % 4], V[(i + 2) % 4]
    return V[(i + 1) % 4], V[(i - 2) % 4]


def _b8_hang_tu(V, X, P):
    """Biểu thức MX + (vectơ bằng XP) hoặc MX - (vectơ bằng PX). -> (tex, lời giải rút gọn về MP)."""
    if random.random() < 0.6:
        R, S = _b8_ban_sao(V, X, P)
        tex = r"%s + %s" % (_vt("M", X), _vt(R, S))
        ly = r"$%s = %s$ nên $%s = %s + %s = %s$" % (_vt(R, S), _vt(X, P), tex, _vt("M", X), _vt(X, P), _vt("M", P))
    else:
        R, S = _b8_ban_sao(V, P, X)
        tex = r"%s - %s" % (_vt("M", X), _vt(R, S))
        ly = (r"$%s = %s$ nên $%s = %s + %s = %s + %s = %s$"
              % (_vt(R, S), _vt(P, X), tex, _vt("M", X), _vt(S, R), _vt("M", X), _vt(X, P), _vt("M", P)))
    return tex, ly


def _b8_tap_hop():
    """-> (debai, dieu_kien_tex, dap (chuỗi), nhieu, giai_a (rút gọn), dap_a, giai_b, kieu)."""
    ten = random.choice(["ABCD", "EFGH", "PQRS"])
    V = list(ten)
    ke = [(V[i], V[(i + k) % 4]) for i in range(4) for k in (1, 3)]
    tt = lambda X, Y: r"đường trung trực của đoạn thẳng $%s$" % "".join(sorted((X, Y)))
    if random.random() < 0.6:
        while True:
            (X1, P), (X2, Q) = random.sample(ke, 2)
            if P != Q and X1 != X2:
                break
        t1, l1 = _b8_hang_tu(V, X1, P)
        t2, l2 = _b8_hang_tu(V, X2, Q)
        dk = r"\left|%s\right| = \left|%s\right|" % (t1, t2)
        dap = tt(P, Q)
        ung = [tt(X1, X2) if {X1, X2} != {P, Q} else None, r"đường thẳng $%s$" % "".join(sorted((P, Q))),
               r"đường tròn đường kính $%s$" % "".join(sorted((P, Q))),
               tt(X1, Q) if {X1, Q} != {P, Q} else None, tt(P, X2) if {P, X2} != {P, Q} else None]
        giai_a = l1 + r"; " + l2 + "."
        dap_a = r"%s = %s,\ %s = %s" % (t1, _vt("M", P), t2, _vt("M", Q))
        giai_b = (r"Điều kiện trở thành $\left|%s\right| = \left|%s\right|$, tức là $M%s = M%s$: $M$ cách đều hai điểm "
                  r"$%s$, $%s$. Vậy tập hợp các điểm $M$ là %s." % (_vt("M", P), _vt("M", Q), P, Q, P, Q, dap))
        kieu = "trung_truc"
    else:
        X, P = random.choice(ke)
        t1, l1 = _b8_hang_tu(V, X, P)
        Y, Z = random.sample([v for v in V], 2)
        doan = "".join(sorted((Y, Z)))
        if random.random() < 0.5:
            t2 = _vt(Y, Z)
            l2 = r"$\left|%s\right| = %s$" % (t2, Y + Z)
            dap_a = r"%s = %s" % (t1, _vt("M", P))
        else:
            t2 = r"%s - %s" % (_vt("M", Z), _vt("M", Y))
            l2 = r"$%s = %s$ (quy tắc trừ) nên $\left|%s\right| = %s$" % (t2, _vt(Y, Z), t2, Y + Z)
            dap_a = r"%s = %s,\ %s = %s" % (t1, _vt("M", P), t2, _vt(Y, Z))
        dk = r"\left|%s\right| = \left|%s\right|" % (t1, t2)
        dap = r"đường tròn tâm $%s$, bán kính bằng $%s$" % (P, doan)
        khac = [v for v in V if v not in (P, X)]
        ung = [r"đường tròn tâm $%s$, bán kính bằng $%s$" % (X, doan), tt(P, X),
               r"đường tròn đường kính $%s$" % doan,
               r"đường tròn tâm $%s$, bán kính bằng $%s$" % (khac[0], doan)]
        giai_a = l1 + r"; " + l2 + "."
        giai_b = (r"Điều kiện trở thành $M%s = %s$ ($%s$ là độ dài không đổi). Vậy tập hợp các điểm $M$ là %s."
                  % (P, doan, doan, dap))
        kieu = "duong_tron"
    nhieu = []
    for x in ung:
        if x and x != dap and x not in nhieu:
            nhieu.append(x)
    debai = r"Cho hình bình hành $%s$." % ten
    return debai, dk, dap, nhieu, giai_a, dap_a, giai_b, kieu


def L10_C4_B8_VD040_MC_A_01(socau, dang=1):
    r"""Tập hợp điểm $M$ thoả một đẳng thức độ dài vectơ trong hình bình hành: thay vectơ bằng vectơ bằng nó (cạnh
    đối), quy tắc ba điểm, quy tắc trừ để đưa về $MP = MQ$ (đường trung trực) hoặc $MP = $ độ dài không đổi (đường
    tròn). LUYỆN TẬP THÊM (mức VD cao hơn YCCĐ TH040). Theo câu tự luận cô Lan gửi. Không có bản SA (đáp án không phải
    số).

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; luyen tap them; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dk, dap, nhieu, ga, da, gb, kieu = _b8_tap_hop()
        debai += r" Tập hợp các điểm $M$ thoả mãn $%s$ là" % dk
        cau += MC_SA_answer_text(debai, dap, nhieu[:3], ga + r"\\ " + gb, 0, 0, dang)
    return cau


def L10_C4_B8_VD040_TL_A_01(socau, dong=1):
    r"""Tự luận - cùng Dang với VD040_MC_A: a) rút gọn các vectơ trong điều kiện; b) tìm tập hợp điểm $M$.

    CLAUDE THEM 16/10/2026 - co Lan duyet ke hoach; luyen tap them; co Lan duyet lai."""
    cau = ""
    for _ in range(socau):
        debai, dk, dap, nhieu, ga, da, gb, kieu = _b8_tap_hop()
        hoi_a = r"Rút gọn các biểu thức vectơ trong đẳng thức $%s$." % dk
        hoi_b = r"Tìm tập hợp các điểm $M$ thoả mãn $%s$." % dk
        dap_b = r"\text{%s}" % dap.replace("$", "")
        cau += TL_answer_text(debai, [(hoi_a, da, ga), (hoi_b, dap_b, gb)], 0, 0, dong)
    return cau
