# ==========================================================
# CHƯƠNG 6 (lớp 10): HÀM SỐ, ĐỒ THỊ VÀ ỨNG DỤNG
#   Bài 15. Hàm số
#   Bài 16. Hàm số bậc hai
#   Bài 17. Dấu của tam thức bậc hai
#   Bài 18. Phương trình quy về phương trình bậc hai
#
# Nguồn: tệp LopXChuong6.py của cô Lan. Tệp ấy ở FORM CŨ (tự mở tệp
# de.tex rồi de.write), nên viết lại cho đúng khuôn math_type -
# math_type.py GIỮ NGUYÊN, không sửa một dòng nào.
#
# HAI LỖI trong tệp của cô đã tránh khi viết lại:
#   1. K10_6_15_1_1 hỏi "đại lượng y nào LÀ hàm số của x" nhưng đặt
#      \True vào bảng X1 - chính là bảng cô chú thích "# KHÔNG phải hàm
#      số" (có một giá trị x lặp lại). Đáp án đặt nhầm vào phương án sai.
#   2. K10_6_18_1_1 lấy nghiem_hq[1] nên IndexError khi phương trình có
#      ít hơn hai nghiệm; và viết {$\True S = \varnothing$} - đặt \True
#      BÊN TRONG $...$ nên LaTeX hỏng.
#
# HÌNH VẼ: bảng xét dấu và bảng biến thiên vẽ bằng TikZ THUẦN, không
# dùng tkz-tab. Lý do: tkz-tab cần tabvar.sty, máy cô Lan không có gói
# này (đã gặp khi dịch PDF), còn TikZ thuần thì chạy ở mọi nơi.
# ==========================================================
import math
import random

from math_type import *

DAU_THAP_PHAN = ","


def _xx6(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết theo cách viết Việt Nam."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _toa6(x):
    """Số dùng LÀM TOẠ ĐỘ TikZ - luôn dấu CHẤM, không phải dấu phẩy."""
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _ba_nhieu6(dapso, ung_vien, buoc=None):
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


def _tam_thuc(a, b, c):
    r"""Viết $ax^2 + bx + c$ thành LaTeX gọn."""
    phan = []
    if a == 1:
        phan.append("x^2")
    elif a == -1:
        phan.append("-x^2")
    else:
        phan.append("%dx^2" % a)
    if b:
        if b == 1:
            phan.append("+ x")
        elif b == -1:
            phan.append("- x")
        elif b > 0:
            phan.append("+ %dx" % b)
        else:
            phan.append("- %dx" % (-b))
    if c:
        phan.append(("+ %d" % c) if c > 0 else ("- %d" % (-c)))
    return " ".join(phan)


def _nghiem_bac_hai(a, b, c):
    """Hai nghiệm của ax^2+bx+c=0 nếu delta > 0, ngược lại None."""
    delta = b * b - 4 * a * c
    if delta <= 0:
        return None
    can = math.isqrt(delta)
    if can * can != delta:
        return None
    x1 = (-b - can) / (2.0 * a)
    x2 = (-b + can) / (2.0 * a)
    return (min(x1, x2), max(x1, x2))


def _dinh(a, b, c):
    """Toạ độ đỉnh của parabol y = ax^2 + bx + c."""
    xi = -b / (2.0 * a)
    yi = a * xi * xi + b * xi + c
    return xi, yi


# ---------------------------------------------------------------------
# HÌNH VẼ - TikZ thuần
# ---------------------------------------------------------------------

def _hinh_parabola(a, b, c, x_tu=None, x_den=None):
    """Đồ thị parabol y = ax^2 + bx + c với trục toạ độ và đỉnh."""
    xi, yi = _dinh(a, b, c)
    if x_tu is None:
        x_tu, x_den = xi - 3, xi + 3
    # lấy biên y theo giá trị thực của hàm ở hai đầu và ở đỉnh
    cac_y = [a * t * t + b * t + c for t in (x_tu, x_den, xi)]
    y_tu, y_den = min(cac_y) - 1, max(cac_y) + 1
    return (
        "\\begin{tikzpicture}[>=stealth,x=0.8cm,y=0.55cm,thick,"
        "line join=round]\n"
        "\\draw[->] (%s,0) -- (%s,0) node[below right]{\\footnotesize $x$};\n"
        % (_toa6(x_tu - 0.5), _toa6(x_den + 0.5)) +
        "\\draw[->] (0,%s) -- (0,%s) node[left]{\\footnotesize $y$};\n"
        % (_toa6(y_tu - 0.5), _toa6(y_den + 0.5)) +
        "\\node[below left] at (0,0) {\\footnotesize $O$};\n"
        "\\clip (%s,%s) rectangle (%s,%s);\n"
        % (_toa6(x_tu - 0.5), _toa6(y_tu - 0.5),
           _toa6(x_den + 0.5), _toa6(y_den + 0.5)) +
        "\\draw[very thick,smooth,samples=120,domain=%s:%s] "
        "plot(\\x,{(%s)*(\\x)*(\\x) + (%s)*(\\x) + (%s)});\n"
        % (_toa6(x_tu), _toa6(x_den), _toa6(a), _toa6(b), _toa6(c)) +
        "\\fill[black] (%s,%s) circle[radius=2pt];\n"
        % (_toa6(xi), _toa6(yi)) +
        "\\end{tikzpicture}")


def _hinh_gap_khuc(diem):
    """Đồ thị gấp khúc qua danh sách điểm, có lưới và trục."""
    xs = [p[0] for p in diem]
    ys = [p[1] for p in diem]
    x_tu, x_den = min(xs) - 1, max(xs) + 1
    y_tu, y_den = min(ys) - 1, max(ys) + 1
    ra = ["\\begin{tikzpicture}[>=stealth,x=0.8cm,y=0.8cm,thick,"
          "line join=round]"]
    ra.append("\\draw[help lines,line width=0.2pt] (%s,%s) grid (%s,%s);"
              % (_toa6(x_tu), _toa6(y_tu), _toa6(x_den), _toa6(y_den)))
    ra.append("\\draw[->] (%s,0) -- (%s,0) node[below right]"
              "{\\footnotesize $x$};" % (_toa6(x_tu), _toa6(x_den)))
    ra.append("\\draw[->] (0,%s) -- (0,%s) node[left]{\\footnotesize $y$};"
              % (_toa6(y_tu), _toa6(y_den)))
    ra.append("\\node[below left] at (0,0) {\\footnotesize $O$};")
    duong = " -- ".join("(%s,%s)" % (_toa6(x), _toa6(y)) for x, y in diem)
    ra.append("\\draw[very thick] %s;" % duong)
    for x, y in diem:
        ra.append("\\fill[black] (%s,%s) circle[radius=2pt];"
                  % (_toa6(x), _toa6(y)))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


def _hinh_bang_xet_dau(ten_ham, moc, dau):
    r"""Bảng xét dấu vẽ bằng TikZ thuần (không dùng tkz-tab).

    moc: nhãn các mốc, đã gồm -\infty ở đầu và +\infty ở cuối.
    dau: dấu trên từng khoảng, đúng len(moc) - 1 phần tử.

    Bản đầu đặt mốc đầu và mốc cuối ĐÚNG TẠI viền nên $-\infty$ chồng
    lên khung, còn số $0$ tại nghiệm thì đè lên dấu. Nay chừa lề hai bên
    và tách hẳn hàng dấu ra khỏi vị trí nghiệm.
    """
    n = len(moc)
    rong = 2.6
    le = 0.7                      # lề hai bên để nhãn vô cực không tràn
    x_nhan = -1.5                 # cột nhãn bên trái
    tong = 2 * le + rong * (n - 1)

    def X(i):
        return le + rong * i

    ra = ["\\begin{tikzpicture}[x=1cm,y=1cm,thick]"]
    ra.append("\\draw (%s,0) rectangle (%s,1.7);" % (_toa6(x_nhan),
                                                     _toa6(tong)))
    ra.append("\\draw (%s,0.85) -- (%s,0.85);" % (_toa6(x_nhan),
                                                  _toa6(tong)))
    ra.append("\\draw (0,0) -- (0,1.7);")
    ra.append("\\node at (%s,1.28) {\\footnotesize $x$};"
              % _toa6(x_nhan / 2))
    ra.append("\\node at (%s,0.42) {\\footnotesize $%s$};"
              % (_toa6(x_nhan / 2), ten_ham))
    for i, m in enumerate(moc):
        ra.append("\\node at (%s,1.28) {\\footnotesize $%s$};"
                  % (_toa6(X(i)), m))
    for i, d in enumerate(dau):
        ra.append("\\node at (%s,0.42) {\\footnotesize $%s$};"
                  % (_toa6((X(i) + X(i + 1)) / 2), d))
    # tại mỗi nghiệm: vạch đứt và số 0
    for i in range(1, n - 1):
        ra.append("\\draw[dashed,line width=0.4pt] (%s,0) -- (%s,0.85);"
                  % (_toa6(X(i)), _toa6(X(i))))
        # nền trắng để đường nét đứt không gạch ngang qua số 0
        ra.append("\\node[fill=white,inner sep=1.5pt] at (%s,0.42) "
                  "{\\footnotesize $0$};" % _toa6(X(i)))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


def _hinh_bang_bien_thien(a, b, c):
    """Bảng biến thiên của hàm số bậc hai, vẽ bằng TikZ thuần."""
    xi, yi = _dinh(a, b, c)
    ra = ["\\begin{tikzpicture}[x=1cm,y=1cm,thick]"]
    ra.append("\\draw (-1.5,0) rectangle (7.5,2.6);")
    ra.append("\\draw (-1.5,1.9) -- (7.5,1.9);")
    ra.append("\\draw (0,0) -- (0,2.6);")
    ra.append("\\node at (-0.75,2.25) {\\footnotesize $x$};")
    ra.append("\\node at (-0.75,0.95) {\\footnotesize $y$};")
    ra.append("\\node at (0.7,2.25) {\\footnotesize $-\\infty$};")
    ra.append("\\node at (3.75,2.25) {\\footnotesize $%s$};" % _xx6(xi))
    ra.append("\\node at (6.8,2.25) {\\footnotesize $+\\infty$};")
    ra.append("\\draw[dashed,line width=0.4pt] (3.75,0) -- (3.75,1.9);")
    if a > 0:
        ra.append("\\node at (0.7,1.6) {\\footnotesize $+\\infty$};")
        ra.append("\\node at (6.8,1.6) {\\footnotesize $+\\infty$};")
        ra.append("\\node[fill=white,inner sep=1.5pt] at (3.75,0.5) {\\footnotesize $%s$};" % _xx6(yi))
        ra.append("\\draw[->] (1.25,1.5) -- (3.3,0.68);")
        ra.append("\\draw[->] (4.2,0.68) -- (6.25,1.5);")
    else:
        ra.append("\\node at (0.7,0.35) {\\footnotesize $-\\infty$};")
        ra.append("\\node at (6.8,0.35) {\\footnotesize $-\\infty$};")
        ra.append("\\node[fill=white,inner sep=1.5pt] at (3.75,1.45) {\\footnotesize $%s$};" % _xx6(yi))
        ra.append("\\draw[->] (1.25,0.55) -- (3.3,1.32);")
        ra.append("\\draw[->] (4.2,1.32) -- (6.25,0.55);")
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


# =====================================================================
# BÀI 15. HÀM SỐ
# =====================================================================

def L10_C6_B15_NB086_MC_A_01(socau, dang=1):
    """Nhận ra mô hình thực tế dẫn đến khái niệm hàm số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    LA_HAM = [
        (r"Quãng đường $s$ của một ô tô chạy đều phụ thuộc vào thời gian $t$",
         r"với mỗi thời điểm $t$ chỉ có \textbf{đúng một} quãng đường"),
        (r"Tiền cước taxi $y$ phụ thuộc vào số ki-lô-mét $x$ đã đi",
         r"với mỗi số ki-lô-mét $x$ chỉ có \textbf{đúng một} số tiền phải trả"),
        (r"Diện tích $S$ của hình vuông phụ thuộc vào độ dài cạnh $a$",
         r"với mỗi độ dài cạnh $a$ chỉ có \textbf{đúng một} diện tích"),
    ]
    KHONG_HAM = [
        r"Ứng với mỗi học sinh của lớp, ta ghi lại các môn học mà bạn ấy "
        r"thích (một bạn có thể thích nhiều môn)",
        r"Ứng với mỗi số thực $x$, ta ghi lại các số $y$ sao cho $y^2 = x$",
        r"Ứng với mỗi tháng trong năm, ta ghi lại các ngày có mưa",
        r"Ứng với mỗi lớp trong trường, ta ghi lại tên các bạn học sinh "
        r"của lớp",
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(LA_HAM))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(LA_HAM):
            break

    cauTN = ""
    for i in gt:
        mo_ta, ly_do = LA_HAM[i]
        debai = (r"Trong các tình huống sau, tình huống nào cho ta một "
                 r"\textbf{hàm số}?")
        giai = (r"Một quy tắc là hàm số khi ứng với \textbf{mỗi} giá trị của "
                r"đại lượng thứ nhất, ta được \textbf{đúng một} giá trị của "
                r"đại lượng thứ hai."
                "\\\\\n"
                r"``%s'' là hàm số vì %s." % (mo_ta, ly_do) +
                "\\\\\n"
                r"Các tình huống còn lại đều không phải hàm số vì có giá trị "
                r"của đại lượng thứ nhất ứng với \textbf{nhiều} giá trị của "
                r"đại lượng thứ hai (chẳng hạn $y^2 = x$ với $x > 0$ cho "
                r"\textbf{hai} giá trị $y$).")
        cauTN += MC_SA_answer_text(debai, "%s." % mo_ta,
                                   ["%s." % t for t in KHONG_HAM],
                                   giai, 0, 0, dang)
    return cauTN


def L10_C6_B15_NB087_MC_A_01(socau, dang=1):
    r"""Tìm tập xác định của hàm số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-5, 3)
        b = random.randint(a + 1, a + 6)
        if (a, b) not in gt:
            gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        dung = (r"$D = \left[%d;\ +\infty\right) \setminus \left\{%d\right\}$"
                % (a, b))
        nhieu = [r"$D = \left(%d;\ +\infty\right) \setminus \left\{%d\right\}$"
                 % (a, b),
                 r"$D = \left[%d;\ +\infty\right)$" % a,
                 r"$D = \mathbb{R} \setminus \left\{%d\right\}$" % b,
                 r"$D = \left[%d;\ %d\right)$" % (a, b)]
        debai = (r"Tìm tập xác định $D$ của hàm số "
                 r"$y = \dfrac{\sqrt{x %s %d}}{x %s %d}$."
                 % ("-" if a >= 0 else "+", abs(a),
                    "-" if b >= 0 else "+", abs(b)))
        giai = (r"Hàm số xác định khi đồng thời:"
                "\\\\\n"
                r"$\bullet$ biểu thức dưới căn không âm: "
                r"$x %s %d \ge 0 \Leftrightarrow x \ge %d$;"
                % ("-" if a >= 0 else "+", abs(a), a) +
                "\\\\\n"
                r"$\bullet$ mẫu khác $0$: "
                r"$x %s %d \ne 0 \Leftrightarrow x \ne %d$."
                % ("-" if b >= 0 else "+", abs(b), b) +
                "\\\\\n"
                r"Vì $%d > %d$ nên giá trị $x = %d$ nằm trong nửa khoảng "
                r"$\left[%d;\ +\infty\right)$ và phải loại ra."
                % (b, a, b, a) +
                "\\\\\n"
                r"Vậy $D = \left[%d;\ +\infty\right) \setminus "
                r"\left\{%d\right\}$." % (a, b))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B15_NB087_SA_A_01(socau):
    r"""Số phần tử nguyên của tập xác định.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Dùng hàm có tập xác định là ĐOẠN để số phần tử nguyên là hữu hạn.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-6, 0)
        b = random.randint(a + 3, a + 12)
        if (a, b) not in gt:
            gt.append((a, b))

    cau = ""
    for a, b in gt:
        kq = b - a + 1
        debai = (r"Cho hàm số $y = \sqrt{x %s %d} + \sqrt{%d - x}$. Tập xác "
                 r"định của hàm số có bao nhiêu phần tử là \textbf{số "
                 r"nguyên}?" % ("-" if a >= 0 else "+", abs(a), b))
        giai = (r"Hàm số xác định khi cả hai biểu thức dưới căn đều không âm:"
                "\\\\\n"
                r"$x %s %d \ge 0 \Leftrightarrow x \ge %d$ và "
                r"$%d - x \ge 0 \Leftrightarrow x \le %d$."
                % ("-" if a >= 0 else "+", abs(a), a, b, b) +
                "\\\\\n"
                r"Vậy $D = \left[%d;\ %d\right]$." % (a, b) +
                "\\\\\n"
                r"Các số nguyên thuộc $D$ là $%d;\ %d;\ \ldots;\ %d$, gồm "
                r"$%d - \left(%d\right) + 1 = %d$ số."
                % (a, a + 1, b, b, a, kq))
        nhieu = _ba_nhieu6(kq, [b - a, kq + 1, abs(a) + abs(b)],
                           buoc=lambda t: kq + 2 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C6_B15_NB089_MC_A_01(socau, dang=1):
    r"""Nhận ra đồ thị của một hàm số.

    Chính là bài K10_6_15_1_1 của cô Lan, nhưng SỬA LỖI: bản của cô hỏi
    "đại lượng $y$ nào LÀ hàm số của $x$" mà lại đặt \True vào bảng $X1$
    - đúng bảng cô chú thích "# KHÔNG phải hàm số" vì có một giá trị $x$
    lặp lại. Đáp án đặt nhầm vào phương án sai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    def _bang_xy(X, Y):
        cot = "|" + "c|" * (len(X) + 1)
        d1 = " & ".join("$%d$" % v for v in X)
        d2 = " & ".join("$%d$" % v for v in Y)
        return (r"\begin{tabular}{%s}\hline $x$ & %s \\\hline "
                r"$y$ & %s \\\hline\end{tabular}" % (cot, d1, d2))

    gt = []
    while len(gt) < socau:
        n = 5
        # bảng ĐÚNG là hàm số: x đôi một khác nhau (y được phép lặp)
        X_dung = sorted(random.sample(range(-6, 10), n))
        Y_dung = [random.randint(-8, 12) for _ in range(n)]
        v = (tuple(X_dung), tuple(Y_dung))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for X_dung, Y_dung in gt:
        X_dung, Y_dung = list(X_dung), list(Y_dung)
        dung = _bang_xy(X_dung, Y_dung)
        # ba bảng SAI: đều có một giá trị x lặp lại
        nhieu = []
        for _ in range(3):
            Xs = sorted(random.sample(range(-6, 10), 4))
            lap = random.choice(Xs)
            Xs = sorted(Xs + [lap])
            Ys = random.sample(range(-8, 12), 5)
            nhieu.append(_bang_xy(Xs, Ys))

        debai = (r"Cho các bảng giá trị tương ứng của hai đại lượng $x$ và "
                 r"$y$. Bảng nào cho ta $y$ là \textbf{hàm số} của $x$?")
        giai = (r"$y$ là hàm số của $x$ khi ứng với \textbf{mỗi} giá trị của "
                r"$x$ chỉ có \textbf{đúng một} giá trị của $y$."
                "\\\\\n"
                r"Trong bảng đúng, các giá trị của $x$ \textbf{đôi một khác "
                r"nhau} nên mỗi $x$ chỉ ứng với một $y$."
                "\\\\\n"
                r"Ba bảng còn lại đều có một giá trị $x$ \textbf{xuất hiện "
                r"hai lần} với hai giá trị $y$ khác nhau, nên $y$ không phải "
                r"là hàm số của $x$."
                "\\\\\n"
                r"Chú ý: giá trị của $y$ \textbf{được phép} lặp lại - điều "
                r"đó không ảnh hưởng gì.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B15_TH088_MC_A_01(socau, dang=1):
    r"""Cách cho hàm số bằng bảng, bằng biểu đồ, bằng công thức.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(2, 6)
        b = random.randint(-8, 8)
        x0 = random.randint(-4, 5)
        if (a, b, x0) not in gt:
            gt.append((a, b, x0))

    cauTN = ""
    for a, b, x0 in gt:
        kq = a * x0 * x0 + b
        dung = r"$%d$" % kq
        nhieu = [r"$%d$" % x for x in _ba_nhieu6(
            kq, [a * x0 + b, (a * x0) ** 2 + b, a * x0 * x0 - b, -kq],
            buoc=lambda t: kq + 3 * t)]
        debai = (r"Cho hàm số được cho bằng công thức "
                 r"$f(x) = %dx^2 %s %d$. Tính $f\left(%d\right)$."
                 % (a, "+" if b >= 0 else "-", abs(b), x0))
        giai = (r"Thay $x = %d$ vào công thức:" % x0 +
                "\\\\\n"
                r"$f\left(%d\right) = %d\cdot\left(%d\right)^2 %s %d = "
                r"%d\cdot %d %s %d = %d$."
                % (x0, a, x0, "+" if b >= 0 else "-", abs(b),
                   a, x0 * x0, "+" if b >= 0 else "-", abs(b), kq) +
                "\\\\\n"
                r"Chú ý phải bình phương \textbf{trước} rồi mới nhân với "
                r"hệ số.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _do_thi_gap_khuc_ngau_nhien():
    """Năm điểm của một đồ thị gấp khúc, các đoạn đổi chiều rõ ràng."""
    x = [-4, -2, 0, 2, 4]
    y = [random.randint(-3, -1), random.randint(1, 3),
         random.randint(-3, -1), random.randint(1, 3),
         random.randint(-3, -1)]
    return list(zip(x, y))


def L10_C6_B15_TH090_MC_A_01(socau, dang=1):
    r"""Đọc khoảng đồng biến, nghịch biến từ ĐỒ THỊ - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đồ thị gấp khúc được sinh sao cho các đoạn ĐỔI CHIỀU luân phiên, nên
    khoảng đồng biến/nghịch biến đọc được chắc chắn - khác bản của cô
    (K10_6_15_1_2) vốn ghi cứng kết luận theo dấu của một hệ số mà không
    đối chiếu với các điểm thật.
    """
    gt = []
    while len(gt) < socau:
        diem = _do_thi_gap_khuc_ngau_nhien()
        v = tuple(diem)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for diem in gt:
        diem = list(diem)
        hinh = _hinh_gap_khuc(diem)
        # chọn một đoạn và hỏi về nó
        i = random.randrange(len(diem) - 1)
        (x1, y1), (x2, y2) = diem[i], diem[i + 1]
        tang = y2 > y1
        chieu = "đồng biến" if tang else "nghịch biến"
        nguoc = "nghịch biến" if tang else "đồng biến"
        dung = (r"Hàm số %s trên khoảng $\left(%d;\ %d\right)$"
                % (chieu, x1, x2))
        nhieu = [r"Hàm số %s trên khoảng $\left(%d;\ %d\right)$"
                 % (nguoc, x1, x2)]
        for j in range(len(diem) - 1):
            if j == i:
                continue
            (u1, v1), (u2, v2) = diem[j], diem[j + 1]
            sai_chieu = "nghịch biến" if v2 > v1 else "đồng biến"
            nhieu.append(r"Hàm số %s trên khoảng $\left(%d;\ %d\right)$"
                         % (sai_chieu, u1, u2))

        debai = (r"Cho đồ thị hàm số $y = f(x)$ như hình vẽ. Khẳng định nào "
                 r"sau đây \textbf{đúng}?")
        giai = (r"Trên một khoảng, hàm số \textbf{đồng biến} nếu đồ thị đi "
                r"\textbf{lên} từ trái sang phải, \textbf{nghịch biến} nếu "
                r"đồ thị đi \textbf{xuống}."
                "\\\\\n"
                r"Trên khoảng $\left(%d;\ %d\right)$, đồ thị đi từ điểm "
                r"$\left(%d;\ %d\right)$ tới điểm $\left(%d;\ %d\right)$: "
                r"giá trị $y$ %s từ $%d$ lên $%d$."
                % (x1, x2, x1, y1, x2, y2,
                   "tăng" if tang else "giảm", y1, y2) +
                "\\\\\n"
                r"Vậy hàm số %s trên khoảng $\left(%d;\ %d\right)$."
                % (chieu, x1, x2))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B15_TH091_MC_A_01(socau, dang=1):
    r"""Đọc giá trị lớn nhất, nhỏ nhất từ ĐỒ THỊ - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        diem = _do_thi_gap_khuc_ngau_nhien()
        ys = [p[1] for p in diem]
        if len(set(ys)) < 4:
            continue
        v = tuple(diem)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for diem in gt:
        diem = list(diem)
        hinh = _hinh_gap_khuc(diem)
        ys = [p[1] for p in diem]
        xs = [p[0] for p in diem]
        lon = max(ys)
        x_lon = xs[ys.index(lon)]
        nho = min(ys)
        hoi_lon = random.choice([True, False])
        kq = lon if hoi_lon else nho
        dung = r"$%d$" % kq
        nhieu = [r"$%d$" % x for x in _ba_nhieu6(
            kq, [nho if hoi_lon else lon, x_lon, min(xs), max(xs)],
            buoc=lambda t: kq + t)]
        debai = (r"Cho đồ thị hàm số $y = f(x)$ xác định trên đoạn "
                 r"$\left[%d;\ %d\right]$ như hình vẽ. Giá trị %s nhất của "
                 r"hàm số trên đoạn đó bằng bao nhiêu?"
                 % (min(xs), max(xs), "lớn" if hoi_lon else "nhỏ"))
        giai = (r"Giá trị lớn nhất (nhỏ nhất) của hàm số trên một đoạn là "
                r"tung độ của điểm \textbf{cao nhất} (thấp nhất) trên đồ "
                r"thị ứng với đoạn ấy."
                "\\\\\n"
                r"Nhìn đồ thị, điểm cao nhất có tung độ $%d$, điểm thấp "
                r"nhất có tung độ $%d$." % (lon, nho) +
                "\\\\\n"
                r"Vậy giá trị %s nhất bằng $%d$. Chú ý câu hỏi đòi "
                r"\textbf{giá trị} của hàm số (tung độ), không phải vị trí "
                r"$x$ mà tại đó hàm số đạt giá trị ấy."
                % ("lớn" if hoi_lon else "nhỏ", kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B15_TH091_SA_A_01(socau):
    r"""Giá trị lớn nhất của hàm số trên một đoạn - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-6, 6)
        c = random.randint(-8, 8)
        xt = random.randint(-4, 0)
        xp = random.randint(1, 5)
        v = (a, b, c, xt, xp)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, c, xt, xp in gt:
        # giá trị lớn nhất của hàm bậc hai trên đoạn: xét đỉnh (nếu thuộc
        # đoạn) và hai đầu mút
        xi, _yi = _dinh(a, b, c)
        cac_x = [xt, xp] + ([xi] if xt <= xi <= xp else [])
        cac_y = [a * t * t + b * t + c for t in cac_x]
        kq = max(cac_y)
        debai = (r"Cho hàm số $y = %s$. Tìm giá trị lớn nhất của hàm số "
                 r"trên đoạn $\left[%d;\ %d\right]$."
                 % (_tam_thuc(a, b, c), xt, xp))
        dong = []
        for t, y in zip(cac_x, cac_y):
            dong.append(r"$f\left(%s\right) = %s$" % (_xx6(t), _xx6(y)))
        giai = (r"Đỉnh của parabol có hoành độ "
                r"$x_I = -\dfrac{b}{2a} = %s$." % _xx6(xi) +
                "\\\\\n" +
                (r"Hoành độ đỉnh \textbf{thuộc} đoạn nên phải xét cả đỉnh "
                 r"lẫn hai đầu mút."
                 if xt <= xi <= xp else
                 r"Hoành độ đỉnh \textbf{không thuộc} đoạn nên hàm số đơn "
                 r"điệu trên đoạn, chỉ cần xét hai đầu mút.") +
                "\\\\\n" + ", ".join(dong) + "." +
                "\\\\\n"
                r"Vậy giá trị lớn nhất bằng $%s$." % _xx6(kq))
        nhieu = _ba_nhieu6(_xx6(kq), [_xx6(min(cac_y)), _xx6(xi),
                                      _xx6(kq + 1)],
                           buoc=lambda t: _xx6(kq + 2 * t))
        cau += MC_SA_answer_text(debai, _xx6(kq), nhieu, giai, 0, 0, 2)
    return cau


def L10_C6_B15_VD092_MC_A_01(socau, dang=1):
    r"""Hàm số bậc nhất trên từng khoảng: bài toán cước điện thoại.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        tron = random.choice([20, 25, 30, 40])      # nghìn đồng
        bao = random.choice([100, 150, 200])        # phút trong gói
        them = random.choice([200, 250, 300, 400])  # đồng mỗi phút vượt
        vuot = random.choice([20, 30, 40, 50, 60])
        v = (tron, bao, them, vuot)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for tron, bao, them, vuot in gt:
        tong_phut = bao + vuot
        kq = tron * 1000 + vuot * them
        dung = r"$%s$ đồng" % "{:,}".format(kq).replace(",", "\\,")
        ung_vien = [tron * 1000 + tong_phut * them,
                    tron * 1000, vuot * them,
                    tron * 1000 + bao * them]
        nhieu = [r"$%s$ đồng" % "{:,}".format(x).replace(",", "\\,")
                 for x in _ba_nhieu6(kq, ung_vien,
                                     buoc=lambda t: kq + 1000 * t)]
        debai = (r"Một gói cước điện thoại có giá $%d$ nghìn đồng một tháng, "
                 r"được gọi miễn phí $%d$ phút; mỗi phút gọi vượt quá $%d$ "
                 r"phút phải trả thêm $%d$ đồng. Trong tháng, bạn An gọi hết "
                 r"$%d$ phút. Hỏi An phải trả bao nhiêu tiền cước?"
                 % (tron, bao, bao, them, tong_phut))
        giai = (r"Gọi $x$ là số phút gọi trong tháng, $y$ là số tiền cước "
                r"(đồng). Khi đó $y$ là hàm số bậc nhất trên từng khoảng:"
                "\\\\\n"
                r"$y = %d\,000$ nếu $0 \le x \le %d$;" % (tron, bao) +
                "\\\\\n"
                r"$y = %d\,000 + %d\left(x - %d\right)$ nếu $x > %d$."
                % (tron, them, bao, bao) +
                "\\\\\n"
                r"Vì $%d > %d$ nên dùng công thức thứ hai:" % (tong_phut, bao) +
                "\\\\\n"
                r"$y = %d\,000 + %d\cdot\left(%d - %d\right) = %d\,000 + "
                r"%d\cdot %d = %s$ (đồng)."
                % (tron, them, tong_phut, bao, tron, them, vuot,
                   "{:,}".format(kq).replace(",", "\\,")))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B15_VD092_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn giải bằng hàm số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        tron = random.choice([25, 30, 40])
        bao = random.choice([100, 150, 200])
        them = random.choice([200, 250, 300])
        vuot = random.choice([30, 40, 50, 60])
        v = (tron, bao, them, vuot)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for tron, bao, them, vuot in gt:
        tong_phut = bao + vuot
        tien = tron * 1000 + vuot * them

        debai = (r"Một gói cước điện thoại có giá $%d$ nghìn đồng một tháng "
                 r"và được gọi miễn phí $%d$ phút. Mỗi phút gọi vượt quá "
                 r"$%d$ phút phải trả thêm $%d$ đồng."
                 % (tron, bao, bao, them))

        hoi_a = (r"Gọi $x$ là số phút gọi trong tháng và $y$ là số tiền cước "
                 r"(đồng). Viết công thức của hàm số $y = f(x)$.")
        giai_a = (r"Nếu $0 \le x \le %d$ thì chỉ phải trả tiền gói: "
                  r"$y = %d\,000$." % (bao, tron) +
                  "\\\\\n"
                  r"Nếu $x > %d$ thì ngoài tiền gói còn phải trả cho $x - %d$ "
                  r"phút vượt: $y = %d\,000 + %d\left(x - %d\right)$."
                  % (bao, bao, tron, them, bao))

        hoi_b = r"Tính số tiền phải trả nếu tháng đó gọi $%d$ phút." % tong_phut
        giai_b = (r"Vì $%d > %d$ nên dùng công thức thứ hai:"
                  % (tong_phut, bao) +
                  "\\\\\n"
                  r"$y = %d\,000 + %d\left(%d - %d\right) = %s$ (đồng)."
                  % (tron, them, tong_phut, bao,
                     "{:,}".format(tien).replace(",", "\\,")))

        muc = tron * 1000 + 100 * them
        hoi_c = (r"Nếu tháng đó phải trả $%s$ đồng thì đã gọi bao nhiêu phút?"
                 % "{:,}".format(muc).replace(",", "\\,"))
        giai_c = (r"Số tiền lớn hơn $%d\,000$ đồng nên chắc chắn đã gọi quá "
                  r"$%d$ phút." % (tron, bao) +
                  "\\\\\n"
                  r"Giải $%d\,000 + %d\left(x - %d\right) = %s$:"
                  % (tron, them, bao,
                     "{:,}".format(muc).replace(",", "\\,")) +
                  "\\\\\n"
                  r"$%d\left(x - %d\right) = %s \Rightarrow x - %d = 100 "
                  r"\Rightarrow x = %d$ (phút)."
                  % (them, bao, "{:,}".format(100 * them).replace(",", "\\,"),
                     bao, bao + 100))

        ds_abcd = [(hoi_a, r"y = %d\,000 \text{ hoặc } %d\,000 + %d(x - %d)"
                    % (tron, tron, them, bao), giai_a),
                   (hoi_b, r"%s \text{ đồng}"
                    % "{:,}".format(tien).replace(",", "\\,"), giai_b),
                   (hoi_c, r"%d \text{ phút}" % (bao + 100), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 16. HÀM SỐ BẬC HAI
# =====================================================================

def _bo_bac_hai_dep(lan_thu=300):
    """Bộ (a, b, c) cho đỉnh có toạ độ đẹp và hai nghiệm nguyên."""
    for _ in range(lan_thu):
        a = random.choice([-2, -1, 1, 2])
        x1 = random.randint(-5, 3)
        x2 = x1 + random.choice([2, 4, 6])   # tổng chẵn -> đỉnh nguyên
        b = -a * (x1 + x2)
        c = a * x1 * x2
        if abs(b) > 12 or abs(c) > 30:
            continue
        return a, b, c, x1, x2
    return None


def L10_C6_B16_NB096_MC_A_01(socau, dang=1):
    r"""Toạ độ đỉnh và trục đối xứng của parabol.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTN = ""
    for a, b, c, _x1, _x2 in gt:
        xi, yi = _dinh(a, b, c)
        dung = (r"$I\left(%s;\ %s\right)$, trục đối xứng $x = %s$"
                % (_xx6(xi), _xx6(yi), _xx6(xi)))
        nhieu = [r"$I\left(%s;\ %s\right)$, trục đối xứng $x = %s$"
                 % (_xx6(-xi), _xx6(yi), _xx6(-xi)),
                 r"$I\left(%s;\ %s\right)$, trục đối xứng $x = %s$"
                 % (_xx6(yi), _xx6(xi), _xx6(yi)),
                 r"$I\left(%s;\ %s\right)$, trục đối xứng $y = %s$"
                 % (_xx6(xi), _xx6(yi), _xx6(yi)),
                 r"$I\left(%s;\ %s\right)$, trục đối xứng $x = %s$"
                 % (_xx6(xi), _xx6(-yi), _xx6(xi))]
        debai = (r"Cho hàm số $y = %s$. Toạ độ đỉnh $I$ và trục đối xứng của "
                 r"parabol là" % _tam_thuc(a, b, c))
        giai = (r"Parabol $y = ax^2 + bx + c$ có đỉnh "
                r"$I\left(-\dfrac{b}{2a};\ -\dfrac{\Delta}{4a}\right)$ và "
                r"trục đối xứng là đường thẳng $x = -\dfrac{b}{2a}$."
                "\\\\\n"
                r"$x_I = -\dfrac{%d}{2\cdot %d} = %s$."
                % (b, a, _xx6(xi)) +
                "\\\\\n"
                r"$y_I = f\left(%s\right) = %s$." % (_xx6(xi), _xx6(yi)) +
                "\\\\\n"
                r"Vậy $I\left(%s;\ %s\right)$ và trục đối xứng là "
                r"$x = %s$ - một đường thẳng \textbf{đứng}."
                % (_xx6(xi), _xx6(yi), _xx6(xi)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B16_NB096_SA_A_01(socau):
    r"""Hoành độ đỉnh của parabol - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cau = ""
    for a, b, c, _x1, _x2 in gt:
        xi, yi = _dinh(a, b, c)
        debai = (r"Cho hàm số $y = %s$. Tìm hoành độ đỉnh của parabol."
                 % _tam_thuc(a, b, c))
        giai = (r"$x_I = -\dfrac{b}{2a} = -\dfrac{%d}{2\cdot %d} = %s$."
                % (b, a, _xx6(xi)))
        nhieu = _ba_nhieu6(_xx6(xi), [_xx6(-xi), _xx6(yi), _xx6(xi + 1)],
                           buoc=lambda t: _xx6(xi + t))
        cau += MC_SA_answer_text(debai, _xx6(xi), nhieu, giai, 0, 0, 2)
    return cau


def L10_C6_B16_TH093_MC_A_01(socau, dang=1):
    r"""Lập bảng giá trị của hàm số bậc hai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTN = ""
    for a, b, c, _x1, _x2 in gt:
        xi, _yi = _dinh(a, b, c)
        cac_x = [int(xi) - 2, int(xi) - 1, int(xi), int(xi) + 1, int(xi) + 2]
        cac_y = [a * t * t + b * t + c for t in cac_x]

        def _bang(ys):
            cot = "|" + "c|" * (len(cac_x) + 1)
            d1 = " & ".join("$%d$" % v for v in cac_x)
            d2 = " & ".join("$%s$" % _xx6(v) for v in ys)
            return (r"\begin{tabular}{%s}\hline $x$ & %s \\\hline "
                    r"$y$ & %s \\\hline\end{tabular}" % (cot, d1, d2))

        dung = _bang(cac_y)
        nhieu = [_bang([-v for v in cac_y]),
                 _bang([a * t + b for t in cac_x]),
                 _bang([v + 1 for v in cac_y])]
        debai = (r"Cho hàm số $y = %s$. Bảng giá trị nào sau đây là "
                 r"\textbf{đúng}?" % _tam_thuc(a, b, c))
        dong = ["$f\\left(%d\\right) = %s$" % (t, _xx6(y))
                for t, y in zip(cac_x, cac_y)]
        giai = (r"Thay lần lượt từng giá trị của $x$ vào công thức "
                r"$y = %s$:" % _tam_thuc(a, b, c) +
                "\\\\\n" + "; ".join(dong) + ".")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B16_TH094_MC_A_01(socau, dang=1):
    r"""Lập bảng biến thiên của hàm số bậc hai - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTN = ""
    for a, b, c, _x1, _x2 in gt:
        xi, yi = _dinh(a, b, c)
        if a > 0:
            dung = (r"Hàm số nghịch biến trên $\left(-\infty;\ %s\right)$ và "
                    r"đồng biến trên $\left(%s;\ +\infty\right)$"
                    % (_xx6(xi), _xx6(xi)))
            nhieu = [r"Hàm số đồng biến trên $\left(-\infty;\ %s\right)$ và "
                     r"nghịch biến trên $\left(%s;\ +\infty\right)$"
                     % (_xx6(xi), _xx6(xi)),
                     r"Hàm số đồng biến trên toàn bộ $\mathbb{R}$",
                     r"Hàm số nghịch biến trên toàn bộ $\mathbb{R}$",
                     r"Hàm số đồng biến trên $\left(-\infty;\ %s\right)$ và "
                     r"nghịch biến trên $\left(%s;\ +\infty\right)$"
                     % (_xx6(yi), _xx6(yi))]
            ly_do = (r"Vì $a = %d > 0$ nên parabol quay bề lõm lên trên: hàm "
                     r"số nghịch biến trước đỉnh rồi đồng biến sau đỉnh." % a)
        else:
            dung = (r"Hàm số đồng biến trên $\left(-\infty;\ %s\right)$ và "
                    r"nghịch biến trên $\left(%s;\ +\infty\right)$"
                    % (_xx6(xi), _xx6(xi)))
            nhieu = [r"Hàm số nghịch biến trên $\left(-\infty;\ %s\right)$ và "
                     r"đồng biến trên $\left(%s;\ +\infty\right)$"
                     % (_xx6(xi), _xx6(xi)),
                     r"Hàm số đồng biến trên toàn bộ $\mathbb{R}$",
                     r"Hàm số nghịch biến trên toàn bộ $\mathbb{R}$",
                     r"Hàm số nghịch biến trên $\left(-\infty;\ %s\right)$ và "
                     r"đồng biến trên $\left(%s;\ +\infty\right)$"
                     % (_xx6(yi), _xx6(yi))]
            ly_do = (r"Vì $a = %d < 0$ nên parabol quay bề lõm xuống dưới: "
                     r"hàm số đồng biến trước đỉnh rồi nghịch biến sau đỉnh."
                     % a)

        hinh = _hinh_bang_bien_thien(a, b, c)
        debai = (r"Cho hàm số $y = %s$ có bảng biến thiên như hình bên. "
                 r"Khẳng định nào sau đây \textbf{đúng}?" % _tam_thuc(a, b, c))
        giai = (r"Hoành độ đỉnh $x_I = -\dfrac{b}{2a} = %s$." % _xx6(xi) +
                "\\\\\n" + ly_do +
                "\\\\\n"
                r"Bảng biến thiên cho thấy hàm số đạt giá trị %s nhất bằng "
                r"$%s$ tại $x = %s$."
                % ("nhỏ" if a > 0 else "lớn", _xx6(yi), _xx6(xi)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B16_TH095_MC_A_01(socau, dang=1):
    r"""Chọn ĐỒ THỊ đúng của hàm số bậc hai cho trước - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTN = ""
    for a, b, c, x1, x2 in gt:
        xi, yi = _dinh(a, b, c)
        hinh = _hinh_parabola(a, b, c)
        dung = r"$y = %s$" % _tam_thuc(a, b, c)
        nhieu = [r"$y = %s$" % _tam_thuc(-a, b, c),
                 r"$y = %s$" % _tam_thuc(a, -b, c),
                 r"$y = %s$" % _tam_thuc(-a, -b, -c),
                 r"$y = %s$" % _tam_thuc(a, b, -c)]
        debai = (r"Parabol trong hình bên là đồ thị của hàm số nào sau đây?")
        giai = (r"Nhìn hình: bề lõm quay %s nên $a %s 0$; parabol cắt trục "
                r"hoành tại hai điểm có hoành độ $%s$ và $%s$."
                % ("lên trên" if a > 0 else "xuống dưới",
                   ">" if a > 0 else "<", _xx6(x1), _xx6(x2)) +
                "\\\\\n"
                r"Đỉnh có hoành độ $x_I = \dfrac{%s + %s}{2} = %s$ - đúng là "
                r"trung điểm của hai nghiệm."
                % (_xx6(x1), _xx6(x2), _xx6(xi)) +
                "\\\\\n"
                r"Thử hàm số $y = %s$: $-\dfrac{b}{2a} = %s$ và "
                r"$f\left(%s\right) = %s$, khớp với đồ thị."
                % (_tam_thuc(a, b, c), _xx6(xi), _xx6(x1), _xx6(0)) +
                "\\\\\n"
                r"Vậy đồ thị là của hàm số $y = %s$." % _tam_thuc(a, b, c))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B16_TH097_MC_A_01(socau, dang=1):
    r"""Đọc tính chất của hàm số bậc hai từ ĐỒ THỊ - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTN = ""
    for a, b, c, x1, x2 in gt:
        xi, yi = _dinh(a, b, c)
        hinh = _hinh_parabola(a, b, c)
        cuc = "nhỏ" if a > 0 else "lớn"
        dung = (r"Hàm số đạt giá trị %s nhất bằng $%s$ tại $x = %s$"
                % (cuc, _xx6(yi), _xx6(xi)))
        nhieu = [r"Hàm số đạt giá trị %s nhất bằng $%s$ tại $x = %s$"
                 % ("lớn" if a > 0 else "nhỏ", _xx6(yi), _xx6(xi)),
                 r"Hàm số đạt giá trị %s nhất bằng $%s$ tại $x = %s$"
                 % (cuc, _xx6(xi), _xx6(yi)),
                 r"Hàm số không có giá trị %s nhất" % cuc,
                 r"Hàm số đạt giá trị %s nhất bằng $%s$ tại $x = %s$"
                 % (cuc, _xx6(yi), _xx6(x1))]
        debai = (r"Cho đồ thị hàm số $y = %s$ như hình bên. Khẳng định nào "
                 r"sau đây \textbf{đúng}?" % _tam_thuc(a, b, c))
        giai = (r"Hệ số $a = %d %s 0$ nên bề lõm quay %s, do đó hàm số đạt "
                r"giá trị %s nhất tại \textbf{đỉnh}."
                % (a, ">" if a > 0 else "<",
                   "lên trên" if a > 0 else "xuống dưới", cuc) +
                "\\\\\n"
                r"Đỉnh $I\left(%s;\ %s\right)$, trong đó $%s$ là "
                r"\textbf{vị trí} $x$ còn $%s$ là \textbf{giá trị} của hàm "
                r"số." % (_xx6(xi), _xx6(yi), _xx6(xi), _xx6(yi)) +
                "\\\\\n"
                r"Vậy hàm số đạt giá trị %s nhất bằng $%s$ tại $x = %s$."
                % (cuc, _xx6(yi), _xx6(xi)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B16_VD098_MC_A_01(socau, dang=1):
    r"""Bài toán cổng, cầu dạng parabol.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đặt gốc toạ độ tại chân cổng bên trái để parabol có dạng
    $y = ax(x - L)$ - cách làm trọn trong chương trình lớp 10.
    """
    gt = []
    while len(gt) < socau:
        L = random.choice([8, 10, 12, 16, 20])
        h = random.choice([4, 5, 6, 8, 9])
        x0 = random.choice([2, 3, 4])
        if x0 >= L / 2:
            continue
        # chiều cao tại x0 phải ra số đẹp
        y0 = 4.0 * h * x0 * (L - x0) / (L * L)
        if not (abs(y0 * 100 - round(y0 * 100)) < 1e-9):
            continue
        v = (L, h, x0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for L, h, x0 in gt:
        y0 = 4.0 * h * x0 * (L - x0) / (L * L)
        dung = r"$%s$ m" % _xx6(y0)
        nhieu = [r"$%s$ m" % x for x in _ba_nhieu6(
            _xx6(y0), [_xx6(h), _xx6(h - y0), _xx6(y0 * 2), _xx6(x0)],
            buoc=lambda t: _xx6(y0 + t / 2.0))]
        debai = (r"Một chiếc cổng có dạng parabol, chân cổng rộng $%d$ m và "
                 r"đỉnh cổng cao $%d$ m so với mặt đất. Tính chiều cao của "
                 r"cổng tại điểm cách chân cổng bên trái $%d$ m."
                 % (L, h, x0))
        giai = (r"Chọn hệ trục $Oxy$ với gốc $O$ tại chân cổng bên trái, "
                r"trục $Ox$ dọc mặt đất."
                "\\\\\n"
                r"Cổng đi qua $O\left(0;\ 0\right)$ và $A\left(%d;\ 0\right)$ "
                r"nên có dạng $y = ax\left(x - %d\right)$." % (L, L) +
                "\\\\\n"
                r"Đỉnh ở chính giữa, tại $x = %s$, và cao $%d$ m:"
                % (_xx6(L / 2.0), h) +
                "\\\\\n"
                r"$a\cdot %s\cdot\left(%s - %d\right) = %d \Rightarrow "
                r"a = %s$."
                % (_xx6(L / 2.0), _xx6(L / 2.0), L, h,
                   _xx6(-4.0 * h / (L * L), 4)) +
                "\\\\\n"
                r"Tại $x = %d$: $y = %s\cdot %d\cdot\left(%d - %d\right) "
                r"= %s$ (m)."
                % (x0, _xx6(-4.0 * h / (L * L), 4), x0, x0, L, _xx6(y0)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B16_VD098_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về hàm số bậc hai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        L = random.choice([8, 10, 12, 16, 20])
        h = random.choice([4, 5, 6, 8])
        x0 = random.choice([2, 4])
        if x0 >= L / 2:
            continue
        y0 = 4.0 * h * x0 * (L - x0) / (L * L)
        if abs(y0 * 100 - round(y0 * 100)) > 1e-9:
            continue
        v = (L, h, x0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for L, h, x0 in gt:
        a = -4.0 * h / (L * L)
        y0 = a * x0 * (x0 - L)

        debai = (r"Một chiếc cổng trường có dạng parabol, chân cổng rộng "
                 r"$%d$ m và đỉnh cổng cao $%d$ m so với mặt đất. Chọn hệ "
                 r"trục $Oxy$ với gốc $O$ tại chân cổng bên trái và trục "
                 r"$Ox$ nằm dọc mặt đất." % (L, h))

        hoi_a = r"Viết công thức hàm số biểu diễn hình dạng chiếc cổng."
        giai_a = (r"Cổng cắt trục hoành tại $x = 0$ và $x = %d$ nên có dạng "
                  r"$y = ax\left(x - %d\right)$." % (L, L) +
                  "\\\\\n"
                  r"Đỉnh ở giữa, tại $x = %s$, cao $%d$ m nên"
                  % (_xx6(L / 2.0), h) +
                  "\\\\\n"
                  r"$a\cdot %s\cdot\left(%s - %d\right) = %d "
                  r"\Rightarrow a = %s$."
                  % (_xx6(L / 2.0), _xx6(L / 2.0), L, h, _xx6(a, 4)) +
                  "\\\\\n"
                  r"Vậy $y = %s\,x\left(x - %d\right)$." % (_xx6(a, 4), L))

        hoi_b = (r"Tính chiều cao của cổng tại điểm cách chân cổng bên trái "
                 r"$%d$ m." % x0)
        giai_b = (r"Thay $x = %d$: $y = %s\cdot %d\cdot\left(%d - %d\right) "
                  r"= %s$ (m)." % (x0, _xx6(a, 4), x0, x0, L, _xx6(y0)))

        cao_xe = 3
        # nửa bề rộng nơi cổng còn cao hơn cao_xe
        delta = math.sqrt(max(h * h - h * cao_xe * 1.0, 0))
        hoi_c = (r"Một chiếc xe tải cao $%d$ m có thể đi qua cổng được "
                 r"không? Giải thích." % cao_xe)
        giai_c = (r"Đỉnh cổng cao $%d$ m $> %d$ m nên ở giữa cổng xe đi lọt."
                  % (h, cao_xe) +
                  "\\\\\n"
                  r"Giải $y = %d$ để tìm hai mép của phần cổng cao hơn "
                  r"$%d$ m:" % (cao_xe, cao_xe) +
                  "\\\\\n"
                  r"$%s\,x\left(x - %d\right) = %d$." % (_xx6(a, 4), L,
                                                         cao_xe) +
                  "\\\\\n"
                  r"Giải phương trình bậc hai này được hai nghiệm; khoảng "
                  r"giữa hai nghiệm chính là bề rộng mà xe cao $%d$ m đi "
                  r"lọt. Nếu bề rộng ấy lớn hơn bề ngang của xe thì xe qua "
                  r"được." % cao_xe +
                  "\\\\\n"
                  r"Vì đỉnh cổng cao $%d$ m nên với xe cao $%d$ m, câu trả "
                  r"lời là \textbf{có}, miễn là xe đi vào giữa cổng."
                  % (h, cao_xe))

        ds_abcd = [(hoi_a, r"y = %s\,x(x - %d)" % (_xx6(a, 4), L), giai_a),
                   (hoi_b, r"%s\ \text{m}" % _xx6(y0), giai_b),
                   (hoi_c, r"\text{Có}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 17. DẤU CỦA TAM THỨC BẬC HAI
# =====================================================================

def L10_C6_B17_NB099_MC_A_01(socau, dang=1):
    r"""Nhận ra tam thức bậc hai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-6, 6)
        c = random.randint(-9, 9)
        v = (a, b, c)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c in gt:
        dung = r"$f(x) = %s$" % _tam_thuc(a, b, c)
        nhieu = [r"$f(x) = %dx %s %d$" % (a, "+" if c >= 0 else "-", abs(c)),
                 r"$f(x) = %dx^3 %s %d$" % (a, "+" if c >= 0 else "-",
                                            abs(c)),
                 r"$f(x) = \dfrac{%d}{x} %s %d$"
                 % (a, "+" if c >= 0 else "-", abs(c)),
                 r"$f(x) = %s$" % (("%d" % c) if c else "5")]
        debai = (r"Trong các biểu thức sau, biểu thức nào là \textbf{tam "
                 r"thức bậc hai}?")
        giai = (r"Tam thức bậc hai (một ẩn) là biểu thức có dạng "
                r"$f(x) = ax^2 + bx + c$ với $a \ne 0$."
                "\\\\\n"
                r"Chỉ $f(x) = %s$ có đúng dạng ấy với $a = %d \ne 0$."
                % (_tam_thuc(a, b, c), a) +
                "\\\\\n"
                r"Các biểu thức còn lại: một cái bậc nhất, một cái bậc ba, "
                r"một cái có ẩn ở mẫu, một cái là hằng số - đều không phải "
                r"tam thức bậc hai.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B17_TH100_MC_A_01(socau, dang=1):
    r"""Xét dấu của tam thức bậc hai - CÓ HÌNH VẼ (bảng xét dấu).

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTN = ""
    for a, b, c, x1, x2 in gt:
        ngoai = "+" if a > 0 else "-"
        trong = "-" if a > 0 else "+"
        hinh = _hinh_bang_xet_dau(
            "f(x)", [r"-\infty", _xx6(x1), _xx6(x2), r"+\infty"],
            [ngoai, trong, ngoai])
        dung = (r"$f(x) %s 0$ khi $x \in \left(%s;\ %s\right)$ và "
                r"$f(x) %s 0$ khi $x$ ở ngoài đoạn $\left[%s;\ %s\right]$"
                % (trong, _xx6(x1), _xx6(x2), ngoai, _xx6(x1), _xx6(x2)))
        nhieu = [r"$f(x) %s 0$ khi $x \in \left(%s;\ %s\right)$ và "
                 r"$f(x) %s 0$ khi $x$ ở ngoài đoạn $\left[%s;\ %s\right]$"
                 % (ngoai, _xx6(x1), _xx6(x2), trong, _xx6(x1), _xx6(x2)),
                 r"$f(x) %s 0$ với mọi $x \in \mathbb{R}$" % ngoai,
                 r"$f(x) %s 0$ với mọi $x \in \mathbb{R}$" % trong,
                 r"$f(x) %s 0$ khi $x \in \left(%s;\ %s\right)$"
                 % (trong, _xx6(x2), _xx6(x1))]
        debai = (r"Cho tam thức bậc hai $f(x) = %s$ có bảng xét dấu như hình "
                 r"bên. Khẳng định nào sau đây \textbf{đúng}?"
                 % _tam_thuc(a, b, c))
        giai = (r"Giải $f(x) = 0$ được hai nghiệm phân biệt $x_1 = %s$ và "
                r"$x_2 = %s$." % (_xx6(x1), _xx6(x2)) +
                "\\\\\n"
                r"Quy tắc dấu tam thức bậc hai có hai nghiệm phân biệt: "
                r"$f(x)$ cùng dấu với hệ số $a$ ở \textbf{ngoài} khoảng hai "
                r"nghiệm, và trái dấu với $a$ ở \textbf{trong} khoảng hai "
                r"nghiệm."
                "\\\\\n"
                r"Ở đây $a = %d %s 0$ nên $f(x) %s 0$ khi "
                r"$x \in \left(%s;\ %s\right)$ và $f(x) %s 0$ khi "
                r"$x < %s$ hoặc $x > %s$."
                % (a, ">" if a > 0 else "<", trong, _xx6(x1), _xx6(x2),
                   ngoai, _xx6(x1), _xx6(x2)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B17_TH101_MC_A_01(socau, dang=1):
    r"""Giải bất phương trình bậc hai một ẩn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None:
            continue
        dau = random.choice(["<", r"\le", ">", r"\ge"])
        w = v + (dau,)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, c, x1, x2, dau in gt:
        mo = dau in ("<", ">")
        # f(x) trái dấu a trong khoảng, cùng dấu a ngoài khoảng
        trong_khoang = (dau in ("<", r"\le")) == (a > 0)
        if trong_khoang:
            if mo:
                S = r"S = \left(%s;\ %s\right)" % (_xx6(x1), _xx6(x2))
            else:
                S = r"S = \left[%s;\ %s\right]" % (_xx6(x1), _xx6(x2))
        else:
            if mo:
                S = (r"S = \left(-\infty;\ %s\right) \cup "
                     r"\left(%s;\ +\infty\right)" % (_xx6(x1), _xx6(x2)))
            else:
                S = (r"S = \left(-\infty;\ %s\right] \cup "
                     r"\left[%s;\ +\infty\right)" % (_xx6(x1), _xx6(x2)))
        dung = "$%s$" % S
        nhieu = [r"$S = \left(%s;\ %s\right)$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \left[%s;\ %s\right]$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \left(-\infty;\ %s\right) \cup "
                 r"\left(%s;\ +\infty\right)$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \left(-\infty;\ %s\right] \cup "
                 r"\left[%s;\ +\infty\right)$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \mathbb{R}$", r"$S = \varnothing$"]
        nhieu = [t for t in nhieu if t != dung]
        debai = (r"Tìm tập nghiệm $S$ của bất phương trình "
                 r"$%s %s 0$." % (_tam_thuc(a, b, c), dau))
        giai = (r"Tam thức $f(x) = %s$ có hai nghiệm $x_1 = %s$, "
                r"$x_2 = %s$ và $a = %d %s 0$."
                % (_tam_thuc(a, b, c), _xx6(x1), _xx6(x2), a,
                   ">" if a > 0 else "<") +
                "\\\\\n"
                r"$f(x)$ %s dấu với $a$ trong khoảng hai nghiệm, %s dấu với "
                r"$a$ ngoài khoảng hai nghiệm." % ("trái", "cùng") +
                "\\\\\n" +
                (r"Bất phương trình đòi $f(x) %s 0$, tức là lấy phần "
                 r"\textbf{trong} khoảng hai nghiệm." % dau
                 if trong_khoang else
                 r"Bất phương trình đòi $f(x) %s 0$, tức là lấy phần "
                 r"\textbf{ngoài} khoảng hai nghiệm." % dau) +
                "\\\\\n" +
                (r"Dấu %s là dấu \textbf{ngặt} nên hai nghiệm KHÔNG thuộc "
                 r"tập nghiệm." % dau if mo else
                 r"Dấu %s cho phép lấy dấu bằng nên hai nghiệm THUỘC tập "
                 r"nghiệm." % dau) +
                "\\\\\n"
                r"Vậy $%s$." % S)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B17_TH101_SA_A_01(socau):
    r"""Số nghiệm nguyên của bất phương trình bậc hai - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chỉ lấy trường hợp tập nghiệm là ĐOẠN/KHOẢNG hữu hạn, để số nghiệm
    nguyên là hữu hạn.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None:
            continue
        a, b, c, x1, x2 = v
        if a < 0:
            continue                    # để "$\le 0$" cho ra đoạn
        dau = random.choice(["<", r"\le"])
        w = (a, b, c, x1, x2, dau)
        if w not in gt:
            gt.append(w)

    cau = ""
    for a, b, c, x1, x2, dau in gt:
        if dau == "<":
            cac = [t for t in range(int(math.ceil(x1)), int(x2) + 1)
                   if x1 < t < x2]
            S = r"\left(%s;\ %s\right)" % (_xx6(x1), _xx6(x2))
        else:
            cac = [t for t in range(int(math.ceil(x1)), int(x2) + 1)
                   if x1 <= t <= x2]
            S = r"\left[%s;\ %s\right]" % (_xx6(x1), _xx6(x2))
        kq = len(cac)
        debai = (r"Bất phương trình $%s %s 0$ có bao nhiêu nghiệm "
                 r"\textbf{nguyên}?" % (_tam_thuc(a, b, c), dau))
        giai = (r"Tam thức có hai nghiệm $x_1 = %s$, $x_2 = %s$ và "
                r"$a = %d > 0$." % (_xx6(x1), _xx6(x2), a) +
                "\\\\\n"
                r"Vì $a > 0$ nên $f(x) %s 0$ ở \textbf{trong} khoảng hai "
                r"nghiệm: $S = %s$." % (dau, S) +
                "\\\\\n"
                r"Các số nguyên thuộc $S$ là: %s."
                % (", ".join("$%d$" % t for t in cac) if cac else "không có") +
                "\\\\\n"
                r"Vậy có $%d$ nghiệm nguyên." % kq)
        nhieu = _ba_nhieu6(kq, [kq + 2, kq - 1 if kq > 1 else kq + 1,
                                int(x2 - x1)],
                           buoc=lambda t: kq + 3 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C6_B17_TH102_MC_A_01(socau, dang=1):
    r"""Đọc tập nghiệm của bất phương trình bậc hai từ ĐỒ THỊ - CÓ HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None:
            continue
        w = v + (random.choice([">", "<"]),)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, c, x1, x2, dau in gt:
        hinh = _hinh_parabola(a, b, c)
        tren = (dau == ">")
        # f(x) > 0 <=> đồ thị nằm TRÊN trục hoành
        trong_khoang = (a < 0) == tren
        if trong_khoang:
            S = r"\left(%s;\ %s\right)" % (_xx6(x1), _xx6(x2))
        else:
            S = (r"\left(-\infty;\ %s\right) \cup \left(%s;\ +\infty\right)"
                 % (_xx6(x1), _xx6(x2)))
        dung = "$S = %s$" % S
        nhieu = [r"$S = \left(%s;\ %s\right)$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \left(-\infty;\ %s\right) \cup "
                 r"\left(%s;\ +\infty\right)$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \left[%s;\ %s\right]$" % (_xx6(x1), _xx6(x2)),
                 r"$S = \mathbb{R}$"]
        nhieu = [t for t in nhieu if t != dung]
        debai = (r"Cho đồ thị hàm số $y = f(x) = %s$ như hình bên. Tìm tập "
                 r"nghiệm của bất phương trình $f(x) %s 0$."
                 % (_tam_thuc(a, b, c), dau))
        giai = (r"$f(x) %s 0$ nghĩa là đồ thị nằm \textbf{phía %s} trục "
                r"hoành." % (dau, "trên" if tren else "dưới") +
                "\\\\\n"
                r"Đồ thị cắt trục hoành tại $x = %s$ và $x = %s$."
                % (_xx6(x1), _xx6(x2)) +
                "\\\\\n" +
                (r"Nhìn hình, phần đồ thị nằm phía %s trục hoành ứng với "
                 r"$x$ \textbf{trong} khoảng hai nghiệm."
                 % ("trên" if tren else "dưới") if trong_khoang else
                 r"Nhìn hình, phần đồ thị nằm phía %s trục hoành ứng với "
                 r"$x$ \textbf{ngoài} khoảng hai nghiệm."
                 % ("trên" if tren else "dưới")) +
                "\\\\\n"
                r"Dấu ngặt nên không lấy hai nghiệm. Vậy $S = %s$." % S)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C6_B17_VD103_MC_A_01(socau, dang=1):
    r"""Bài toán thực tiễn dẫn đến bất phương trình bậc hai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Vật ném lên: $h(t) = -5t^2 + v_0 t$. Hỏi khoảng thời gian vật cao
    hơn một mức cho trước - đúng dạng bất phương trình bậc hai.
    """
    gt = []
    while len(gt) < socau:
        v0 = random.choice([20, 25, 30, 40])
        # chọn mức h sao cho hai nghiệm đẹp
        t1 = random.choice([1, 2])
        t2 = v0 / 5.0 - t1
        if t2 <= t1 or abs(t2 - round(t2)) > 1e-9:
            continue
        h = -5.0 * t1 * t1 + v0 * t1
        if abs(h - round(h)) > 1e-9:
            continue
        v = (v0, t1, int(t2), int(h))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for v0, t1, t2, h in gt:
        khoang = t2 - t1
        dung = r"$%s$ giây" % _xx6(khoang)
        nhieu = [r"$%s$ giây" % x for x in _ba_nhieu6(
            _xx6(khoang), [_xx6(t1), _xx6(t2), _xx6(t1 + t2),
                           _xx6(v0 / 5.0)],
            buoc=lambda t: _xx6(khoang + t))]
        debai = (r"Một quả bóng được ném thẳng đứng lên cao với vận tốc ban "
                 r"đầu $%d$ m/s. Độ cao của bóng (tính bằng mét) sau $t$ "
                 r"giây là $h(t) = -5t^2 + %dt$. Hỏi bóng ở độ cao lớn hơn "
                 r"$%d$ m trong khoảng thời gian bao lâu?" % (v0, v0, h))
        giai = (r"Yêu cầu dẫn tới bất phương trình $h(t) > %d$:" % h +
                "\\\\\n"
                r"$-5t^2 + %dt > %d \Leftrightarrow -5t^2 + %dt - %d > 0$."
                % (v0, h, v0, h) +
                "\\\\\n"
                r"Tam thức $-5t^2 + %dt - %d$ có hai nghiệm $t_1 = %d$ và "
                r"$t_2 = %d$." % (v0, h, t1, t2) +
                "\\\\\n"
                r"Hệ số $a = -5 < 0$ nên tam thức \textbf{dương} ở trong "
                r"khoảng hai nghiệm:"
                "\\\\\n"
                r"$t \in \left(%d;\ %d\right)$." % (t1, t2) +
                "\\\\\n"
                r"Vậy bóng ở độ cao lớn hơn $%d$ m trong $%d - %d = %s$ giây."
                % (h, t2, t1, _xx6(khoang)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B17_VD103_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về chiều cao, khoảng cách.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v0 = random.choice([20, 30, 40])
        t1 = random.choice([1, 2])
        t2 = v0 / 5.0 - t1
        if t2 <= t1 or abs(t2 - round(t2)) > 1e-9:
            continue
        h = -5.0 * t1 * t1 + v0 * t1
        v = (v0, t1, int(t2), int(h))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for v0, t1, t2, h in gt:
        t_dinh = v0 / 10.0
        h_max = -5.0 * t_dinh * t_dinh + v0 * t_dinh

        debai = (r"Một quả bóng được ném thẳng đứng lên cao với vận tốc ban "
                 r"đầu $%d$ m/s. Độ cao của bóng (mét) sau $t$ giây là "
                 r"$h(t) = -5t^2 + %dt$." % (v0, v0))

        hoi_a = r"Tính độ cao lớn nhất mà bóng đạt được."
        giai_a = (r"$h(t)$ là hàm số bậc hai với $a = -5 < 0$ nên đạt giá "
                  r"trị lớn nhất tại đỉnh."
                  "\\\\\n"
                  r"$t = -\dfrac{b}{2a} = -\dfrac{%d}{2\cdot\left(-5\right)} "
                  r"= %s$ (giây)." % (v0, _xx6(t_dinh)) +
                  "\\\\\n"
                  r"$h\left(%s\right) = %s$ (m)."
                  % (_xx6(t_dinh), _xx6(h_max)))

        hoi_b = r"Sau bao lâu thì bóng chạm đất?"
        giai_b = (r"Bóng chạm đất khi $h(t) = 0$:"
                  "\\\\\n"
                  r"$-5t^2 + %dt = 0 \Leftrightarrow "
                  r"t\left(-5t + %d\right) = 0$." % (v0, v0) +
                  "\\\\\n"
                  r"$t = 0$ (lúc ném) hoặc $t = %s$ (giây)."
                  % _xx6(v0 / 5.0) +
                  "\\\\\n"
                  r"Vậy sau $%s$ giây thì bóng chạm đất."
                  % _xx6(v0 / 5.0))

        hoi_c = (r"Tìm khoảng thời gian bóng ở độ cao lớn hơn $%d$ m." % h)
        giai_c = (r"$h(t) > %d \Leftrightarrow -5t^2 + %dt - %d > 0$."
                  % (h, v0, h) +
                  "\\\\\n"
                  r"Tam thức có hai nghiệm $t = %d$ và $t = %d$; hệ số "
                  r"$a = -5 < 0$ nên tam thức dương ở \textbf{trong} khoảng "
                  r"hai nghiệm." % (t1, t2) +
                  "\\\\\n"
                  r"Vậy $t \in \left(%d;\ %d\right)$, tức là trong $%d$ giây."
                  % (t1, t2, t2 - t1))

        ds_abcd = [(hoi_a, r"%s\ \text{m}" % _xx6(h_max), giai_a),
                   (hoi_b, r"%s\ \text{giây}" % _xx6(v0 / 5.0), giai_b),
                   (hoi_c, r"t \in \left(%d;\ %d\right)" % (t1, t2), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 18. PHƯƠNG TRÌNH QUY VỀ PHƯƠNG TRÌNH BẬC HAI
# =====================================================================

def _pt_hai_can(lan_thu=300):
    r"""Bộ số cho phương trình $\sqrt{ax^2+bx+c} = \sqrt{dx+e}$.

    Sinh NGƯỢC từ nghiệm để nghiệm luôn đẹp, rồi kiểm tra điều kiện
    $dx + e \ge 0$ để biết nghiệm nào bị loại - tránh hẳn lỗi
    IndexError của bản cũ (K10_6_18_1_1 lấy nghiem_hq[1] khi phương
    trình hệ quả có ít hơn hai nghiệm).
    """
    for _ in range(lan_thu):
        x1 = random.randint(-6, 6)
        x2 = random.randint(-6, 6)
        if x1 == x2:
            continue
        d = random.choice([1, 2, -1, -2])
        e = random.randint(-6, 6)
        # ax^2+bx+c - (dx+e) = (x-x1)(x-x2)  =>  a=1
        a, b, c = 1, -(x1 + x2) + d, x1 * x2 + e
        nghiem = sorted({x for x in (x1, x2) if d * x + e >= 0})
        if not nghiem:
            continue
        return a, b, c, d, e, sorted({x1, x2}), nghiem
    return None


def L10_C6_B18_TH104_MC_A_01(socau, dang=1):
    r"""Giải phương trình dạng hai căn thức bằng nhau.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _pt_hai_can()
        if v is None:
            continue
        w = (v[0], v[1], v[2], v[3], v[4], tuple(v[5]), tuple(v[6]))
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, c, d, e, hq, nghiem in gt:
        hq, nghiem = list(hq), list(nghiem)
        dung = r"$S = \left\{%s\right\}$" % ";\\ ".join(
            "%d" % x for x in nghiem)
        nhieu = [r"$S = \left\{%s\right\}$" % ";\\ ".join("%d" % x
                                                          for x in hq),
                 r"$S = \varnothing$",
                 r"$S = \left\{%d\right\}$" % hq[-1],
                 r"$S = \left\{%d\right\}$" % hq[0]]
        nhieu = [t for t in nhieu if t != dung]
        ve_phai = "%dx %s %d" % (d, "+" if e >= 0 else "-", abs(e))
        debai = (r"Giải phương trình $\sqrt{%s} = \sqrt{%s}$."
                 % (_tam_thuc(a, b, c), ve_phai))
        giai = (r"Hai căn bậc hai bằng nhau khi và chỉ khi hai biểu thức "
                r"dưới căn bằng nhau \textbf{và} cùng không âm:"
                "\\\\\n"
                r"$\sqrt{f(x)} = \sqrt{g(x)} \Leftrightarrow "
                r"\begin{cases} g(x) \ge 0 \\ f(x) = g(x) \end{cases}$"
                "\\\\\n"
                r"Phương trình $f(x) = g(x)$:"
                "\\\\\n"
                r"$%s = %s \Leftrightarrow x^2 %s %dx %s %d = 0$."
                % (_tam_thuc(a, b, c), ve_phai,
                   "+" if (b - d) >= 0 else "-", abs(b - d),
                   "+" if (c - e) >= 0 else "-", abs(c - e)) +
                "\\\\\n"
                r"Nghiệm: %s." % ", ".join("$x = %d$" % x for x in hq) +
                "\\\\\n"
                r"Thử lại điều kiện $%s \ge 0$:" % ve_phai +
                "\\\\\n" +
                "; ".join(r"$x = %d$ cho $%d$ nên %s"
                          % (x, d * x + e,
                             "\\textbf{nhận}" if d * x + e >= 0
                             else "\\textbf{loại}")
                          for x in hq) + "." +
                "\\\\\n"
                r"Vậy $S = \left\{%s\right\}$."
                % ";\\ ".join("%d" % x for x in nghiem))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B18_TH104_SA_A_01(socau):
    r"""Tổng các nghiệm của phương trình - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _pt_hai_can()
        if v is None:
            continue
        w = (v[0], v[1], v[2], v[3], v[4], tuple(v[5]), tuple(v[6]))
        if w not in gt:
            gt.append(w)

    cau = ""
    for a, b, c, d, e, hq, nghiem in gt:
        hq, nghiem = list(hq), list(nghiem)
        kq = sum(nghiem)
        ve_phai = "%dx %s %d" % (d, "+" if e >= 0 else "-", abs(e))
        debai = (r"Tính tổng tất cả các nghiệm của phương trình "
                 r"$\sqrt{%s} = \sqrt{%s}$." % (_tam_thuc(a, b, c), ve_phai))
        giai = (r"Bình phương hai vế và giải phương trình bậc hai được "
                r"%s." % ", ".join("$x = %d$" % x for x in hq) +
                "\\\\\n"
                r"Thử lại điều kiện $%s \ge 0$ thì chỉ giữ được %s."
                % (ve_phai, ", ".join("$x = %d$" % x for x in nghiem)) +
                "\\\\\n"
                r"Vậy tổng các nghiệm bằng $%d$." % kq)
        nhieu = _ba_nhieu6(kq, [sum(hq), kq + 1, -kq],
                           buoc=lambda t: kq + 2 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def _pt_can_bang_nhi_thuc(lan_thu=400):
    r"""Bộ số cho $\sqrt{ax^2+bx+c} = dx + e$, sinh NGƯỢC từ nghiệm.

    Trả về (a,b,c,d,e, nghiem_he_qua, nghiem_that).
    """
    for _ in range(lan_thu):
        x1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        if x1 == x2:
            continue
        d = random.choice([1, 2])
        e = random.randint(-5, 5)
        # ax^2+bx+c = (dx+e)^2 + (x-x1)(x-x2) - (x-x1)(x-x2) ... dựng:
        # đặt f(x) - (dx+e)^2 = (x - x1)(x - x2)
        a = 1 + d * d
        b = -(x1 + x2) + 2 * d * e
        c = x1 * x2 + e * e
        nghiem = sorted({x for x in (x1, x2) if d * x + e >= 0})
        if not nghiem:
            continue
        return a, b, c, d, e, sorted({x1, x2}), nghiem
    return None


def L10_C6_B18_TH105_MC_A_01(socau, dang=1):
    r"""Giải phương trình dạng căn thức bằng nhị thức bậc nhất.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _pt_can_bang_nhi_thuc()
        if v is None:
            continue
        w = (v[0], v[1], v[2], v[3], v[4], tuple(v[5]), tuple(v[6]))
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, c, d, e, hq, nghiem in gt:
        hq, nghiem = list(hq), list(nghiem)
        dung = r"$S = \left\{%s\right\}$" % ";\\ ".join("%d" % x
                                                        for x in nghiem)
        nhieu = [r"$S = \left\{%s\right\}$" % ";\\ ".join("%d" % x
                                                          for x in hq),
                 r"$S = \varnothing$",
                 r"$S = \left\{%d\right\}$" % hq[-1],
                 r"$S = \left\{%d\right\}$" % hq[0]]
        nhieu = [t for t in nhieu if t != dung]
        ve_phai = "%dx %s %d" % (d, "+" if e >= 0 else "-", abs(e))
        debai = (r"Giải phương trình $\sqrt{%s} = %s$."
                 % (_tam_thuc(a, b, c), ve_phai))
        giai = (r"Căn bậc hai luôn không âm nên vế phải cũng phải không âm:"
                "\\\\\n"
                r"$\sqrt{f(x)} = g(x) \Leftrightarrow "
                r"\begin{cases} g(x) \ge 0 \\ f(x) = \left[g(x)\right]^2 "
                r"\end{cases}$"
                "\\\\\n"
                r"Bình phương hai vế: $%s = \left(%s\right)^2$, thu gọn "
                r"được phương trình bậc hai với nghiệm %s."
                % (_tam_thuc(a, b, c), ve_phai,
                   " và ".join("$x = %d$" % x for x in hq)) +
                "\\\\\n"
                r"Thử lại điều kiện $%s \ge 0$:" % ve_phai +
                "\\\\\n" +
                "; ".join(r"$x = %d$ cho vế phải bằng $%d$ nên %s"
                          % (x, d * x + e,
                             "\\textbf{nhận}" if d * x + e >= 0
                             else "\\textbf{loại}")
                          for x in hq) + "." +
                "\\\\\n"
                r"Vậy $S = \left\{%s\right\}$."
                % ";\\ ".join("%d" % x for x in nghiem))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C6_B18_TH105_SA_A_01(socau):
    r"""Số nghiệm của phương trình chứa căn - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _pt_can_bang_nhi_thuc()
        if v is None:
            continue
        w = (v[0], v[1], v[2], v[3], v[4], tuple(v[5]), tuple(v[6]))
        if w not in gt:
            gt.append(w)

    cau = ""
    for a, b, c, d, e, hq, nghiem in gt:
        hq, nghiem = list(hq), list(nghiem)
        kq = len(nghiem)
        ve_phai = "%dx %s %d" % (d, "+" if e >= 0 else "-", abs(e))
        debai = (r"Phương trình $\sqrt{%s} = %s$ có bao nhiêu nghiệm?"
                 % (_tam_thuc(a, b, c), ve_phai))
        giai = (r"Bình phương hai vế được phương trình hệ quả với nghiệm "
                r"%s." % " và ".join("$x = %d$" % x for x in hq) +
                "\\\\\n"
                r"Nhưng phải có $%s \ge 0$ thì căn mới bằng vế phải:"
                % ve_phai +
                "\\\\\n" +
                "; ".join(r"$x = %d \Rightarrow %d$ nên %s"
                          % (x, d * x + e,
                             "\\textbf{nhận}" if d * x + e >= 0
                             else "\\textbf{loại}")
                          for x in hq) + "." +
                "\\\\\n"
                r"Vậy phương trình có $%d$ nghiệm." % kq)
        nhieu = _ba_nhieu6(kq, [len(hq), 0, kq + 2],
                           buoc=lambda t: kq + t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


# =====================================================================
# CÂU ĐÚNG/SAI - bốn ý phải TĂNG DẦN mức độ NB, TH, VD, VDC
# =====================================================================

def L10_C6_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - hàm số; hàm số bậc hai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTF = ''
    for a, b, c, x1, x2 in gt:
        xi, yi = _dinh(a, b, c)
        cuc = "nhỏ" if a > 0 else "lớn"
        debai = (r"Cho hàm số $y = f(x) = %s$." % _tam_thuc(a, b, c))

        ds_abcd = (
            # a) NB - nhắc lại một tính chất
            [
                (r"{\True Tập xác định của hàm số là $\mathbb{R}$}",
                 r"Đúng. Hàm số bậc hai là đa thức nên xác định với mọi số "
                 r"thực $x$."),
                (r"{Tập xác định của hàm số là $\mathbb{R}\setminus"
                 r"\left\{0\right\}$}",
                 r"Sai. Không có mẫu và không có căn nên không phải loại "
                 r"giá trị nào; tập xác định là $\mathbb{R}$."),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True Đỉnh của parabol là $I\left(%s;\ %s\right)$}"
                 % (_xx6(xi), _xx6(yi)),
                 r"Đúng. $x_I = -\dfrac{b}{2a} = -\dfrac{%d}{2\cdot %d} = "
                 r"%s$ và $y_I = f\left(%s\right) = %s$."
                 % (b, a, _xx6(xi), _xx6(xi), _xx6(yi))),
                (r"{Đỉnh của parabol là $I\left(%s;\ %s\right)$}"
                 % (_xx6(yi), _xx6(xi)),
                 r"Sai. Hai toạ độ bị viết ngược: đỉnh là "
                 r"$I\left(%s;\ %s\right)$." % (_xx6(xi), _xx6(yi))),
            ],
            # c) VD - phải có đỉnh mới kết luận được
            [
                (r"{\True Hàm số đạt giá trị %s nhất bằng $%s$}"
                 % (cuc, _xx6(yi)),
                 r"Đúng. Vì $a = %d %s 0$ nên bề lõm quay %s, hàm số đạt "
                 r"giá trị %s nhất tại đỉnh, bằng $y_I = %s$."
                 % (a, ">" if a > 0 else "<",
                    "lên trên" if a > 0 else "xuống dưới", cuc, _xx6(yi))),
                (r"{Hàm số đạt giá trị %s nhất bằng $%s$}"
                 % ("lớn" if a > 0 else "nhỏ", _xx6(yi)),
                 r"Sai. Với $a = %d %s 0$ thì hàm số chỉ có giá trị %s "
                 r"nhất, KHÔNG có giá trị %s nhất."
                 % (a, ">" if a > 0 else "<", cuc,
                    "lớn" if a > 0 else "nhỏ")),
            ],
            # d) VDC - phải tự nghĩ ra cách, không có công thức sẵn
            [
                (r"{\True Đồ thị hàm số cắt trục hoành tại hai điểm có "
                 r"hoành độ $%s$ và $%s$}" % (_xx6(x1), _xx6(x2)),
                 r"Đúng. Hoành độ giao điểm với trục hoành là nghiệm của "
                 r"$f(x) = 0$."
                 "\\\\\n"
                 r"Giải $%s = 0$ được $x = %s$ và $x = %s$."
                 % (_tam_thuc(a, b, c), _xx6(x1), _xx6(x2)) +
                 "\\\\\n"
                 r"Kiểm lại: trung bình cộng hai nghiệm bằng $%s$, đúng "
                 r"bằng hoành độ đỉnh - phù hợp với tính đối xứng của "
                 r"parabol." % _xx6(xi)),
                (r"{Đồ thị hàm số không cắt trục hoành}",
                 r"Sai. $\Delta = %d^2 - 4\cdot %d\cdot %d = %d > 0$ nên "
                 r"phương trình $f(x) = 0$ có hai nghiệm phân biệt, đồ thị "
                 r"cắt trục hoành tại hai điểm."
                 % (b, a, c, b * b - 4 * a * c)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L10_C6_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - dấu tam thức bậc hai; phương trình quy về bậc hai.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_bac_hai_dep()
        if v is None or v in gt:
            continue
        gt.append(v)

    cauTF = ''
    for a, b, c, x1, x2 in gt:
        delta = b * b - 4 * a * c
        ngoai = "cùng dấu với $a$"
        trong = "trái dấu với $a$"
        if a > 0:
            S_am = r"\left(%s;\ %s\right)" % (_xx6(x1), _xx6(x2))
            dau_trong = "<"
        else:
            S_am = (r"\left(-\infty;\ %s\right) \cup \left(%s;\ +\infty"
                    r"\right)" % (_xx6(x1), _xx6(x2)))
            dau_trong = "<"

        debai = (r"Cho tam thức bậc hai $f(x) = %s$." % _tam_thuc(a, b, c))

        ds_abcd = (
            # a) NB - nhắc lại một công thức
            [
                (r"{\True Biệt thức của tam thức là $\Delta = %d$}" % delta,
                 r"Đúng. $\Delta = b^2 - 4ac = \left(%d\right)^2 - "
                 r"4\cdot %d\cdot\left(%d\right) = %d$."
                 % (b, a, c, delta)),
                (r"{Biệt thức của tam thức là $\Delta = %d$}"
                 % (b * b + 4 * a * c),
                 r"Sai. Công thức là $b^2 - 4ac$ chứ không phải "
                 r"$b^2 + 4ac$; giá trị đúng là $%d$." % delta),
            ],
            # b) TH - thay số vào đúng một quy tắc
            [
                (r"{\True Tam thức có hai nghiệm phân biệt $%s$ và $%s$}"
                 % (_xx6(x1), _xx6(x2)),
                 r"Đúng. Vì $\Delta = %d > 0$ nên có hai nghiệm phân biệt; "
                 r"giải ra được $x = %s$ và $x = %s$."
                 % (delta, _xx6(x1), _xx6(x2))),
                (r"{Tam thức vô nghiệm}",
                 r"Sai. $\Delta = %d > 0$ nên tam thức có hai nghiệm phân "
                 r"biệt." % delta),
            ],
            # c) VD - phải dùng quy tắc dấu, có kết quả ý trước
            [
                (r"{\True $f(x)$ %s khi $x$ nằm trong khoảng hai nghiệm}"
                 % trong,
                 r"Đúng. Khi tam thức có hai nghiệm phân biệt, $f(x)$ trái "
                 r"dấu với hệ số $a$ ở TRONG khoảng hai nghiệm và cùng dấu "
                 r"với $a$ ở NGOÀI khoảng hai nghiệm."
                 "\\\\\n"
                 r"Ở đây $a = %d$ nên trong khoảng "
                 r"$\left(%s;\ %s\right)$ thì $f(x)$ %s."
                 % (a, _xx6(x1), _xx6(x2), trong)),
                (r"{$f(x)$ %s khi $x$ nằm trong khoảng hai nghiệm}" % ngoai,
                 r"Sai. Trong khoảng hai nghiệm thì $f(x)$ %s, còn ngoài "
                 r"khoảng hai nghiệm mới %s." % (trong, ngoai)),
            ],
            # d) VDC - phải tự lập luận, không có công thức sẵn
            [
                (r"{\True Tập nghiệm của bất phương trình $f(x) %s 0$ là "
                 r"$%s$}" % (dau_trong, S_am),
                 r"Đúng. Ta xét dấu của $f(x)$ theo quy tắc dấu tam thức."
                 "\\\\\n"
                 r"Với $a = %d %s 0$, tam thức %s trong khoảng hai nghiệm "
                 r"và %s ngoài khoảng ấy."
                 % (a, ">" if a > 0 else "<",
                    "âm" if a > 0 else "dương",
                    "dương" if a > 0 else "âm") +
                 "\\\\\n"
                 r"Do đó $f(x) < 0$ khi $x \in %s$." % S_am),
                (r"{Bất phương trình $f(x) %s 0$ vô nghiệm}" % dau_trong,
                 r"Sai. Tam thức có hai nghiệm phân biệt nên nó đổi dấu, "
                 r"chắc chắn có khoảng làm $f(x) < 0$; tập nghiệm là $%s$."
                 % S_am),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


# ---------------------------------------------------------------------
# Ba dạng TRẢ LỜI NGẮN bổ sung cho các yêu cầu mức Vận dụng - bộ chọn
# câu cần mà Mapping chưa khai, đề hệ số 1 chương 6 vì thế mất 16/96 câu.
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
# ---------------------------------------------------------------------

def L10_C6_B15_VD092_SA_A_01(socau):
    """Trả lời ngắn: tiền cước theo hàm số bậc nhất trên từng khoảng."""
    gt = []
    while len(gt) < socau:
        tron = random.choice([20, 25, 30, 40])
        bao = random.choice([100, 150, 200])
        them = random.choice([200, 250, 300, 400])
        vuot = random.choice([20, 30, 40, 50, 60])
        v = (tron, bao, them, vuot)
        if v not in gt:
            gt.append(v)

    cau = ""
    for tron, bao, them, vuot in gt:
        tong_phut = bao + vuot
        kq = tron * 1000 + vuot * them
        debai = (r"Một gói cước điện thoại giá $%d$ nghìn đồng một tháng, "
                 r"được gọi miễn phí $%d$ phút; mỗi phút vượt quá $%d$ phút "
                 r"phải trả thêm $%d$ đồng. Tháng đó bạn An gọi $%d$ phút. "
                 r"Tính số tiền cước An phải trả (đơn vị: đồng)."
                 % (tron, bao, bao, them, tong_phut))
        giai = (r"Số phút vượt: $%d - %d = %d$ (phút)."
                % (tong_phut, bao, vuot) +
                "\\\\\n"
                r"Tiền cước $= %d\,000 + %d\cdot %d = %d$ (đồng)."
                % (tron, them, vuot, kq))
        nhieu = _ba_nhieu6(kq, [tron * 1000 + tong_phut * them, tron * 1000,
                                vuot * them],
                           buoc=lambda t: kq + 1000 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C6_B16_VD098_SA_A_01(socau):
    """Trả lời ngắn: chiều cao cổng parabol tại một vị trí."""
    gt = []
    while len(gt) < socau:
        L = random.choice([8, 10, 12, 16, 20])
        h = random.choice([4, 5, 6, 8, 9])
        x0 = random.choice([2, 3, 4])
        if x0 >= L / 2:
            continue
        y0 = 4.0 * h * x0 * (L - x0) / (L * L)
        if abs(y0 * 100 - round(y0 * 100)) > 1e-9:
            continue
        v = (L, h, x0)
        if v not in gt:
            gt.append(v)

    cau = ""
    for L, h, x0 in gt:
        a = -4.0 * h / (L * L)
        y0 = a * x0 * (x0 - L)
        debai = (r"Một chiếc cổng dạng parabol có chân cổng rộng $%d$ m và "
                 r"đỉnh cao $%d$ m. Tính chiều cao của cổng tại điểm cách "
                 r"chân cổng bên trái $%d$ m (đơn vị: mét)." % (L, h, x0))
        giai = (r"Chọn gốc toạ độ tại chân cổng bên trái, cổng có dạng "
                r"$y = ax\left(x - %d\right)$." % L +
                "\\\\\n"
                r"Đỉnh tại $x = %s$ cao $%d$ m nên $a = %s$."
                % (_xx6(L / 2.0), h, _xx6(a, 4)) +
                "\\\\\n"
                r"Tại $x = %d$: $y = %s\cdot %d\cdot\left(%d - %d\right) "
                r"= %s$ (m)." % (x0, _xx6(a, 4), x0, x0, L, _xx6(y0)))
        nhieu = _ba_nhieu6(_xx6(y0), [_xx6(h), _xx6(h - y0), _xx6(y0 * 2)],
                           buoc=lambda t: _xx6(y0 + t / 2.0))
        cau += MC_SA_answer_text(debai, _xx6(y0), nhieu, giai, 0, 0, 2)
    return cau


def L10_C6_B17_VD103_SA_A_01(socau):
    """Trả lời ngắn: khoảng thời gian vật cao hơn một mức cho trước."""
    gt = []
    while len(gt) < socau:
        v0 = random.choice([20, 25, 30, 40])
        t1 = random.choice([1, 2])
        t2 = v0 / 5.0 - t1
        if t2 <= t1 or abs(t2 - round(t2)) > 1e-9:
            continue
        h = -5.0 * t1 * t1 + v0 * t1
        if abs(h - round(h)) > 1e-9:
            continue
        w = (v0, t1, int(t2), int(h))
        if w not in gt:
            gt.append(w)

    cau = ""
    for v0, t1, t2, h in gt:
        kq = t2 - t1
        debai = (r"Một quả bóng được ném thẳng đứng lên cao, độ cao sau $t$ "
                 r"giây là $h(t) = -5t^2 + %dt$ (mét). Hỏi bóng ở độ cao "
                 r"lớn hơn $%d$ m trong bao nhiêu giây?" % (v0, h))
        giai = (r"$h(t) > %d \Leftrightarrow -5t^2 + %dt - %d > 0$."
                % (h, v0, h) +
                "\\\\\n"
                r"Tam thức có hai nghiệm $t = %d$, $t = %d$; hệ số "
                r"$a = -5 < 0$ nên tam thức dương ở TRONG khoảng hai nghiệm."
                % (t1, t2) +
                "\\\\\n"
                r"$t \in \left(%d;\ %d\right)$, dài $%d - %d = %d$ (giây)."
                % (t1, t2, t2, t1, kq))
        nhieu = _ba_nhieu6(kq, [t1, t2, t1 + t2, int(v0 / 5)],
                           buoc=lambda t: kq + t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau
