# ==========================================
# CHƯƠNG 3 (lớp 10): HỆ THỨC LƯỢNG TRONG TAM GIÁC
#   Bài 5. Giá trị lượng giác của một góc từ 0° đến 180°
#   Bài 6. Hệ thức lượng trong tam giác
#
# Quy ước chung của ngân hàng (xem docs/10_PYTHON_GENERATOR.md):
#   - Mỗi hàm sinh ra "socau" câu KHÁC NHAU về số liệu, cùng một dạng toán.
#   - Đáp án và lời giải được tính ngay trong hàm, không để nơi khác tính lại.
#   - Số liệu bị ràng buộc để kết quả luôn "đẹp": góc đặc biệt, cạnh nguyên,
#     căn thức rút gọn được. Không để rơi vào trường hợp suy biến.
# ==========================================
import math
import random
import numpy as np
from sympy import (Rational, sqrt, simplify, latex, nsimplify, Integer,
                   together, fraction)

from math_type import *


# =====================================================================
# TIỆN ÍCH DÙNG CHUNG CHO CÁC DẠNG DÙNG SỐ GẦN ĐÚNG (máy tính cầm tay)
# ---------------------------------------------------------------------
# Các dạng dưới đây chuyển từ tệp 10-3.py của cô Lan. Bản cũ dùng
# DefChung.UCLN và DefChung.check; ở đây thay bằng math.gcd và hàm
# _ba_nhieu (vừa trộn vừa BẢO ĐẢM bốn phương án khác nhau - bản cũ có
# chỗ sinh ra hai phương án trùng nhau).
# =====================================================================
# Dấu thập phân dùng trong đề. Sách giáo khoa Việt Nam dùng DẤU PHẨY
# ("12,35"); tệp cũ của cô viết dấu chấm. Muốn đổi lại chỉ cần sửa đúng
# một dòng này.
DAU_THAP_PHAN = "."


def _xx(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết thành chuỗi (bỏ đuôi 0 thừa)."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu(dapso, ung_vien, buoc=None):
    """Lấy đúng BA phương án nhiễu, khác nhau và khác đáp số.

    math_type.MC_SA_answer_* đòi bốn phương án phân biệt, nếu không nó
    quay vòng mãi. Bản cũ có chỗ đưa cùng một giá trị vào hai lần
    (ví dụ dạng máy tính cầm tay, nhánh cos) nên phải chặn ở đây.
    """
    ds = []
    for v in ung_vien:
        if v != dapso and v not in ds:
            ds.append(v)
        if len(ds) == 3:
            return ds
    # vẫn thiếu thì đẻ thêm cho đủ, dựa trên một bước nhảy do hàm gọi đưa vào
    k = 1
    while len(ds) < 3:
        v = buoc(k) if buoc else str(k)
        if v != dapso and v not in ds:
            ds.append(v)
        k += 1
    return ds


def _cap_nguyen_to_cung_nhau(lo=2, hi=20):
    """Sinh cặp p < q nguyên tố cùng nhau, dùng cho điểm trên nửa đường tròn đơn vị.

    Bản cũ lấy hai số ngẫu nhiên rồi chia cho ƯCLN, nên KHI HAI SỐ BẰNG
    NHAU sẽ ra p = q = 1, điểm $M(1;0)$ và căn bằng 0 - câu hỏi vô nghĩa.
    Ở đây ép p < q ngay từ đầu.
    """
    while True:
        q = random.randint(lo, hi)
        p = random.randint(1, q - 1)
        if math.gcd(p, q) == 1:
            return p, q

def _gon(x):
    r"""Viết một biểu thức thành MỘT phân số, số hạng dương đứng trước.

    sympy để nguyên sẽ ra $\frac{-1 + \sqrt{3}}{2}$; giáo viên viết
    $\dfrac{\sqrt{3} - 1}{2}$. Hàm này lo đúng việc đó.
    """
    t = together(simplify(x))
    tu, mau = fraction(t)
    if tu.is_Add and len(tu.args) == 2:
        duong = [h for h in tu.args if not h.could_extract_minus_sign()]
        am = [h for h in tu.args if h.could_extract_minus_sign()]
        if len(duong) == 1 and len(am) == 1:
            tu_chu = r"%s - %s" % (latex(duong[0]), latex(-am[0]))
            return tu_chu if mau == 1 else r"\dfrac{%s}{%s}" % (tu_chu, latex(mau))
    return latex(t).replace(r"\frac", r"\dfrac")


# ---- Bảng giá trị lượng giác của các góc đặc biệt từ 0° đến 180° ----
# (độ, sin, cos, tan hoặc None nếu không xác định, cot hoặc None)
BANG_GTLG = [
    (0,   Integer(0),        Integer(1),         Integer(0),        None),
    (30,  Rational(1, 2),    sqrt(3) / 2,        sqrt(3) / 3,       sqrt(3)),
    (45,  sqrt(2) / 2,       sqrt(2) / 2,        Integer(1),        Integer(1)),
    (60,  sqrt(3) / 2,       Rational(1, 2),     sqrt(3),           sqrt(3) / 3),
    (90,  Integer(1),        Integer(0),         None,              Integer(0)),
    (120, sqrt(3) / 2,       Rational(-1, 2),    -sqrt(3),          -sqrt(3) / 3),
    (135, sqrt(2) / 2,       -sqrt(2) / 2,       Integer(-1),       Integer(-1)),
    (150, Rational(1, 2),    -sqrt(3) / 2,       -sqrt(3) / 3,      -sqrt(3)),
    (180, Integer(0),        Integer(-1),        Integer(0),        None),
]
TEN_HAM = {1: ("sin", 1), 2: ("cos", 2), 3: ("tan", 3), 4: ("cot", 4)}


def _goc(d):
    """Ghi một số đo góc theo kiểu đề thi: 120^\\circ"""
    return r"%d^{\circ}" % d


def _tam_giac_tikz(nhan_a="A", nhan_b="B", nhan_c="C"):
    """Hình tam giác thường, dùng minh hoạ cho các câu hệ thức lượng."""
    return (
        "\\begin{tikzpicture}[scale=0.85,line join=round]\n"
        "\\coordinate (A) at (0,0);\n"
        "\\coordinate (B) at (5,0);\n"
        "\\coordinate (C) at (1.6,2.7);\n"
        "\\draw[thick] (A)--(B)--(C)--cycle;\n"
        "\\node[below left] at (A) {$%s$};\n"
        "\\node[below right] at (B) {$%s$};\n"
        "\\node[above] at (C) {$%s$};\n"
        "\\end{tikzpicture}" % (nhan_a, nhan_b, nhan_c)
    )


# ==========================================================
# Bài 5 — Giá trị lượng giác của một góc từ 0° đến 180°
# ==========================================================

def L10_C3_B5_NB029_MC_A_01(socau, dang=1):
    """Nhận biết giá trị lượng giác của một góc đặc biệt."""
    gt = []
    while len(gt) < socau:
        # bỏ các góc mà tan/cot không xác định để đề luôn có nghĩa
        d, s, c, t, ct = random.choice([r for r in BANG_GTLG if r[3] is not None and r[4] is not None])
        ki, cot_gt = random.choice([("\\sin", s), ("\\cos", c), ("\\tan", t), ("\\cot", ct)])
        v = (d, ki)
        if v in [(x[0], x[1]) for x in gt]:
            continue
        gt.append((d, ki, cot_gt))

    cauTN = ''
    for d, ki, dung in gt:
        # nhiễu: lấy đúng giá trị của các hàm khác tại chính góc đó và giá trị đối
        ds = set()
        for _, s2, c2, t2, ct2 in [r for r in BANG_GTLG if r[0] == d]:
            for x in (s2, c2, t2, ct2):
                if x is not None and simplify(x - dung) != 0:
                    ds.add(latex(x))
        for x in (-dung, dung * 2 if dung != 0 else Integer(1)):
            if simplify(x - dung) != 0:
                ds.add(latex(x))
        ds = list(ds)
        while len(ds) < 3:
            ds.append(latex(Rational(random.randint(1, 3), random.randint(2, 4))))

        debai = r"The value of $%s %s$ is" % (ki, _goc(d))
        giai = (r"Using the table of trigonometric values of special angles: $%s %s = %s$."
                % (ki, _goc(d), latex(dung)))
        cauTN += MC_SA_answer_const(debai, latex(dung), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH030_MC_A_01(socau, dang=1):
    """Dùng máy tính cầm tay tính giá trị lượng giác (làm tròn 2 chữ số thập phân)."""
    gt = []
    while len(gt) < socau:
        d = random.choice([x for x in range(10, 171) if x % 10 != 0 or x % 30 != 0])
        ki = random.choice(["sin", "cos"])
        if (d, ki) in gt:
            continue
        gt.append((d, ki))

    cauTN = ''
    for d, ki in gt:
        thuc = np.sin(np.radians(d)) if ki == "sin" else np.cos(np.radians(d))
        dung = round(float(thuc), 2)
        ds = set()
        while len(ds) < 3:
            lech = round(dung + random.choice([-0.2, -0.1, -0.05, 0.05, 0.1, 0.2]), 2)
            if abs(lech) <= 1 and abs(lech - dung) > 1e-9:
                ds.add(("%.2f" % lech).replace(".", DAU_THAP_PHAN))
        debai = (r"Using a scientific calculator, the value of $\%s %s$ (rounded to the nearest hundredth) is"
                 % (ki, _goc(d)))
        giai = (r"Set the calculator to \textbf{DEG} mode and press $\%s %s$ to get $%s$."
                % (ki, _goc(d), ("%.2f" % dung).replace(".", DAU_THAP_PHAN)))
        cauTN += MC_SA_answer_const(debai, ("%.2f" % dung).replace(".", DAU_THAP_PHAN), list(ds), giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_MC_A_01(socau, dang=1):
    """Quan hệ giữa giá trị lượng giác của hai góc bù nhau."""
    gt = []
    while len(gt) < socau:
        d = random.choice([30, 45, 60, 120, 135, 150])
        ki = random.choice(["sin", "cos", "tan"])
        if (d, ki) in gt:
            continue
        gt.append((d, ki))

    cauTN = ''
    for d, ki in gt:
        bu = 180 - d
        hang = [r for r in BANG_GTLG if r[0] == d][0]
        hang_bu = [r for r in BANG_GTLG if r[0] == bu][0]
        chi = {"sin": 1, "cos": 2, "tan": 3}[ki]
        gia_tri_bu = hang_bu[chi]

        if ki == "sin":
            he_thuc = r"\sin(180^{\circ}-\alpha)=\sin\alpha"
        elif ki == "cos":
            he_thuc = r"\cos(180^{\circ}-\alpha)=-\cos\alpha"
        else:
            he_thuc = r"\tan(180^{\circ}-\alpha)=-\tan\alpha"

        # Truoc day dung set() roi bu them Rational ngau nhien ma KHONG
        # so lai voi dap so -> co luc bu trung dap so, con lai 2 phuong an
        # -> NhieuTrungError. Va set() khong giu thu tu nen de khong tai
        # lap lai duoc. Do duoc 29/09/2026.
        ds = _ba_nhieu(
            latex(gia_tri_bu),
            [latex(x) for x in (-gia_tri_bu, hang[1], hang[2]) if x is not None],
            buoc=lambda t: latex(Rational(t, t + 2)))

        debai = r"Given $\%s %s = %s$. The value of $\%s %s$ is" % (
            ki, _goc(d), latex(hang[chi]), ki, _goc(bu))
        giai = (r"The angles $%s$ and $%s$ are supplementary, so $%s$. Hence $\%s %s = %s$."
                % (_goc(d), _goc(bu), he_thuc, ki, _goc(bu), latex(gia_tri_bu)))
        cauTN += MC_SA_answer_const(debai, latex(gia_tri_bu), list(ds), giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_SA_C_03(socau, dang=2):
    """Rút gọn biểu thức lượng giác dùng quan hệ hai góc bù nhau (đáp số nguyên)."""
    gt = []
    while len(gt) < socau:
        d = random.choice([30, 45, 60])
        he_so = random.randint(2, 5)
        if (d, he_so) in gt:
            continue
        gt.append((d, he_so))

    cauTN = ''
    for d, he_so in gt:
        bu = 180 - d
        # P = k*(sin a + sin(180-a)) - k*(cos a + cos(180-a))  = 2k*sin a  (phần cos triệt tiêu)
        # chọn dạng cho đáp số luôn bằng 0 thì tầm thường -> dùng dạng cos triệt tiêu, sin nhân đôi
        hang = [r for r in BANG_GTLG if r[0] == d][0]
        dapso = simplify(he_so * (hang[2] + (-hang[2])))   # = 0 phần cos
        # biểu thức: k*(cos a + cos(180-a)) + (sin a)^2 + (cos a)^2
        dapso = Integer(1)
        debai = (r"Simplify the expression $P = %d\left(\cos %s + \cos %s\right) + \sin^{2} %s + \cos^{2} %s$."
                 % (he_so, _goc(d), _goc(bu), _goc(d), _goc(d)))
        giai = (r"Since $%s$ and $%s$ are supplementary, $\cos %s = -\cos %s$, so "
                r"$\cos %s + \cos %s = 0$.\\ "
                r"Also, $\sin^{2}\alpha + \cos^{2}\alpha = 1$, so $P = %d \cdot 0 + 1 = 1$."
                % (_goc(d), _goc(bu), _goc(bu), _goc(d), _goc(d), _goc(bu), he_so))
        ds = ["0", str(he_so), str(2 * he_so), "-1"]
        cauTN += MC_SA_answer_const(debai, latex(dapso), ds, giai, 0, 0, dang)
    return cauTN


# ==========================================================
# Bài 6 — Hệ thức lượng trong tam giác
# ==========================================================

def _la_chinh_phuong(n):
    if n <= 0:
        return False
    r = int(round(n ** 0.5))
    return r * r == n


# Các cặp cạnh cho ra cạnh thứ ba NGUYÊN khi dùng định lí côsin với góc 60° / 120°.
# Tính sẵn một lần để đề luôn ra số đẹp, học sinh không phải bấm máy ra số lẻ.
CAP_COSIN = {
    60:  [(b, c) for b in range(3, 21) for c in range(b + 1, 21)
          if _la_chinh_phuong(b * b + c * c - b * c)],
    120: [(b, c) for b in range(3, 21) for c in range(b + 1, 21)
          if _la_chinh_phuong(b * b + c * c + b * c)],
}


def L10_C3_B6_TH032_MC_A_01(socau, dang=1):
    """Định lí côsin: biết hai cạnh và góc xen giữa, tính cạnh thứ ba."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        if (A, b, c) in gt:
            continue
        gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)

        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$ and $\widehat{A} = %s$. "
                 r"The length of side $BC$ is" % (b, c, _goc(A)))
        giai = (r"By the law of cosines in triangle $ABC$:\\ "
                r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
                r"Hence $BC = %d$."
                % (b, c, b, c, latex(cos_A), a2, a))
        ds = [str(a + 1), str(a - 1), str(b + c), str(abs(b - c)) if b != c else str(a + 2)]
        ds = [x for x in dict.fromkeys(ds) if x != str(a)][:3]
        while len(ds) < 3:
            ds.append(str(a + len(ds) + 3))
        cauTN += MC_SA_answer_const(debai, str(a), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH032_SA_A_01(socau, dang=2):
    """Định lí côsin (trả lời ngắn): tính độ dài cạnh, đáp số nguyên."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        if (A, b, c) in gt:
            continue
        gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)
        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$ and $\widehat{A} = %s$. "
                 r"Calculate the length of side $BC$." % (b, c, _goc(A)))
        giai = (r"Law of cosines: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, "
                r"so $BC = %d$." % (b, c, b, c, latex(cos_A), a2, a))
        ds = [str(a + 1), str(a - 1), str(b + c)]
        ds = [x for x in dict.fromkeys(ds) if x != str(a)][:3]
        while len(ds) < 3:
            ds.append(str(a + len(ds) + 3))
        cauTN += MC_SA_answer_const(debai, str(a), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_MC_A_01(socau, dang=1):
    """Định lí sin: biết một cạnh và hai góc, tính cạnh còn lại."""
    # (A, B, hệ số k sao cho b = k*a)  với b = a*sinB/sinA
    BO_GOC = [(30, 45, sqrt(2)), (30, 60, sqrt(3)), (30, 90, Integer(2)),
              (45, 60, sqrt(6) / 2), (45, 90, sqrt(2)), (60, 90, 2 * sqrt(3) / 3)]
    gt = []
    while len(gt) < socau:
        A, B, k = random.choice(BO_GOC)
        a = random.randint(3, 12)
        if (A, B, a) in gt:
            continue
        gt.append((A, B, a))

    cauTN = ''
    for A, B, a in gt:
        k = [x[2] for x in BO_GOC if x[0] == A and x[1] == B][0]
        b = simplify(a * k)
        hang_A = [r for r in BANG_GTLG if r[0] == A][0]
        hang_B = [r for r in BANG_GTLG if r[0] == B][0]

        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$. "
                 r"The length of side $AC$ is" % (a, _goc(A), _goc(B)))
        giai = (r"By the law of sines: $\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B}$.\\ "
                r"Hence $AC = \dfrac{BC\cdot\sin B}{\sin A} "
                r"= \dfrac{%d\cdot %s}{%s} = %s$."
                % (a, latex(hang_B[1]), latex(hang_A[1]), latex(b)))
        ds = _ba_nhieu(
            latex(b),
            [latex(simplify(a / k)), latex(a * 2), latex(simplify(b + a))],
            buoc=lambda t: latex(a + t + 2))
        cauTN += MC_SA_answer_const(debai, latex(b), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_SA_B_01(socau, dang=2):
    """Bán kính đường tròn ngoại tiếp: R = a/(2 sin A), chọn A = 30° để R nguyên."""
    gt = []
    while len(gt) < socau:
        a = random.randint(4, 20)
        if a in gt:
            continue
        gt.append(a)

    cauTN = ''
    for a in gt:
        R = a                      # A = 30° => sin A = 1/2 => R = a
        debai = (r"Given triangle $ABC$ with $BC = %d$ and $\widehat{A} = 30^{\circ}$. "
                 r"What is the circumradius $R$ of triangle $ABC$?" % a)
        giai = (r"By the law of sines: $\dfrac{BC}{\sin A} = 2R$.\\ "
                r"Hence $R = \dfrac{BC}{2\sin A} = \dfrac{%d}{2\cdot\frac{1}{2}} = %d$."
                % (a, R))
        ds = [str(2 * a), str(a // 2 if a % 2 == 0 else a + 1), str(a + 3)]
        cauTN += MC_SA_answer_const(debai, str(R), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_NB034_MC_B_01(socau, dang=1):
    """Chọn công thức tính diện tích tam giác phù hợp với dữ kiện cho trước."""
    BO = [
        ("two sides $b$, $c$ and the included angle $A$",
         r"$S = \dfrac{1}{2}bc\sin A$"),
        ("three sides $a$, $b$, $c$",
         r"$S = \sqrt{p(p-a)(p-b)(p-c)}$"),
        ("three sides $a$, $b$, $c$ and the circumradius $R$",
         r"$S = \dfrac{abc}{4R}$"),
        ("three sides $a$, $b$, $c$ and the inradius $r$",
         r"$S = pr$"),
        ("side $a$ and the altitude $h_a$ to that side",
         r"$S = \dfrac{1}{2}a h_a$"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        if i in gt:
            continue
        gt.append(i)

    cauTN = ''
    for i in gt:
        du_kien, ct = BO[i]
        ds = [x[1] for j, x in enumerate(BO) if j != i]
        random.shuffle(ds)
        debai = (r"Triangle $ABC$ has area $S$ and semiperimeter $p$. "
                 r"When %s are given, the formula for the area of the triangle is" % du_kien)
        giai = r"Since %s are given, we use the formula %s." % (du_kien, ct)
        cauTN += MC_SA_answer_text(debai, ct, ds[:3], giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_SA_D_01(socau, dang=2):
    """Diện tích tam giác S = (1/2)bc sinA, chọn A = 30° hoặc 150° và bc chia hết 4."""
    gt = []
    while len(gt) < socau:
        A = random.choice([30, 150])
        b = random.randint(4, 16)
        c = random.randint(4, 16)
        if (b * c) % 4 != 0 or (A, b, c) in gt:
            continue
        gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        S = b * c // 4            # sin30 = sin150 = 1/2  => S = bc/4
        debai = (r"Given triangle $ABC$ with $AB = %d$, $AC = %d$ and $\widehat{A} = %s$. "
                 r"What is the area of triangle $ABC$?" % (c, b, _goc(A)))
        giai = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A "
                r"= \dfrac{1}{2}\cdot %d\cdot %d\cdot\dfrac{1}{2} = %d$." % (c, b, S))
        # 2*S va b*c//2 LUON bang nhau (S = bc/4) nen danh sach cu thuc
        # chat chi co 2 gia tri khac nhau. Do duoc 29/09/2026.
        ds = _ba_nhieu(str(S), [str(2 * S), str(S + 2), str(b * c // 2)],
                       buoc=lambda t: str(S + t + 5))
        cauTN += MC_SA_answer_const(debai, str(S), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH035_MC_A_01(socau, dang=1):
    """Giải tam giác khi biết hai cạnh và góc xen giữa (c-g-c): hỏi góc còn lại."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        if (A, b, c) in gt:
            continue
        gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        # cos B = (a^2 + c^2 - b^2) / (2ac)
        cos_B = Rational(a * a + c * c - b * b, 2 * a * c)
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)

        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$, $\widehat{A} = %s$. "
                 r"The value of $\cos B$ is" % (b, c, _goc(A)))
        giai = (r"The law of cosines gives $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, "
                r"so $BC = %d$.\\ "
                r"Applying the law of cosines again: $\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} "
                r"= \dfrac{%d + %d - %d}{2\cdot %d\cdot %d} = %s$."
                % (b, c, b, c, latex(cos_A), a2, a,
                   a * a, c * c, b * b, a, c, latex(cos_B)))
        ds = list(dict.fromkeys([latex(-cos_B), latex(Rational(a * a + b * b - c * c, 2 * a * b)),
                                 latex(cos_A)]))
        ds = [x for x in ds if x != latex(cos_B)][:3]
        while len(ds) < 3:
            ds.append(latex(Rational(random.randint(1, 5), random.randint(6, 9))))
        cauTN += MC_SA_answer_const(debai, latex(cos_B), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH035_MC_B_01(socau, dang=1):
    """Giải tam giác khi biết một cạnh và hai góc kề (g-c-g): hỏi góc thứ ba."""
    gt = []
    while len(gt) < socau:
        A, B = random.choice([(30, 45), (30, 60), (45, 60), (45, 45), (60, 60), (30, 90)])
        a = random.randint(4, 14)
        if (A, B, a) in gt:
            continue
        gt.append((A, B, a))

    cauTN = ''
    for A, B, a in gt:
        C = 180 - A - B
        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{B} = %s$, $\widehat{C} = %s$. "
                 r"The measure of angle $\widehat{A}$ is" % (a, _goc(A), _goc(B)))
        giai = (r"Since the sum of the three angles of a triangle is $180^{\circ}$, "
                r"$\widehat{A} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C)))
        ds = list(dict.fromkeys([_goc(C + 15), _goc(abs(C - 15)), _goc(180 - C)]))
        ds = [x for x in ds if x != _goc(C)][:3]
        while len(ds) < 3:
            ds.append(_goc(C + 10 * (len(ds) + 2)))
        cauTN += MC_SA_answer_const(debai, _goc(C), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH035_SA_B_01(socau, dang=2):
    """Giải tam giác (trả lời ngắn): biết cạnh và hai góc, tính số đo góc còn lại."""
    gt = []
    while len(gt) < socau:
        A, B = random.choice([(30, 45), (30, 60), (45, 60), (45, 45), (60, 60), (30, 90)])
        a = random.randint(4, 14)
        if (A, B, a) in gt:
            continue
        gt.append((A, B, a))

    cauTN = ''
    for A, B, a in gt:
        C = 180 - A - B
        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{B} = %s$, $\widehat{C} = %s$. "
                 r"Find the measure of angle $\widehat{A}$ (in degrees)." % (a, _goc(A), _goc(B)))
        giai = (r"$\widehat{A} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C)))
        ds = list(dict.fromkeys([str(C + 15), str(abs(C - 15)), str(180 - C)]))
        ds = [x for x in ds if x != str(C)][:3]
        while len(ds) < 3:
            ds.append(str(C + 10 * (len(ds) + 2)))
        cauTN += MC_SA_answer_const(debai, str(C), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_MC_A_01(socau, dang=1):
    """Đo khoảng cách giữa hai địa điểm khi gặp vật cản (định lí côsin)."""
    DIA_DIEM = [("opposite banks of a lake", "lake"), ("opposite sides of a forest", "forest"),
                ("opposite sides of a building", "building")]
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        if b < 6 or c < 6 or (A, b, c) in gt:
            continue
        gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        canh, _ = random.choice(DIA_DIEM)
        dau = -1 if A == 60 else 1
        d2 = b * b + c * c + dau * b * c
        d = int(round(d2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)

        debai = (r"To measure the distance between two points $A$ and $B$ located on %s (it cannot be measured directly), "
                 r"a point $C$ is chosen and one measures $CA = %d\,\text{m}$, $CB = %d\,\text{m}$ and "
                 r"$\widehat{ACB} = %s$. The distance $AB$ is"
                 % (canh, b, c, _goc(A)))
        giai = (r"By the law of cosines in triangle $ABC$:\\ "
                r"$AB^{2} = CA^{2} + CB^{2} - 2\cdot CA\cdot CB\cdot\cos\widehat{ACB} "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
                r"Hence $AB = %d\,\text{m}$."
                % (b, c, b, c, latex(cos_A), d2, d))
        ds = [str(b + c), str(d + 2), str(abs(b - c)) if b != c else str(d - 3)]
        ds = [x for x in dict.fromkeys(ds) if x != str(d)][:3]
        while len(ds) < 3:
            ds.append(str(d + len(ds) + 4))
        cauTN += MC_SA_answer_const(debai, str(d), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_TL_A_01(socau, dong=1):
    """Tính chiều cao của vật khi không đo trực tiếp được (hai góc nâng)."""
    gt = []
    while len(gt) < socau:
        d = random.choice([x for x in range(10, 61) if x % 2 == 0])
        if d in gt:
            continue
        gt.append(d)

    cauTN = ''
    for d in gt:
        # đo góc nâng 30° tại A, tiến lại gần d mét tới B đo được 60°
        # h = d / (cot30 - cot60) = d / (2√3/3) = d√3/2
        h = simplify(d * sqrt(3) / 2)
        AH = simplify(h * sqrt(3))          # = 3d/2, hình chiếu khi góc 30°
        # giữ một danh từ duy nhất cho cả đề và câu hỏi, tránh chỗ ghi "toà nhà"
        # chỗ lại ghi "chân tháp"
        vat, chan = random.choice([("a tower", "the base of the tower"),
                                   ("an antenna mast", "the base of the mast"),
                                   ("a high-rise building", "the base of the building")])

        debai = (r"To measure the height $CH$ of %s without climbing to its top, a person stands at point $A$ "
                 r"on the ground and measures the angle of elevation to the top $C$ as $30^{\circ}$, then walks straight toward "
                 r"%s for another $%d\,\text{m}$ to point $B$, where the angle of elevation is measured as $60^{\circ}$ "
                 r"(the three points $A$, $B$, $H$ are collinear)." % (vat, chan, d))

        hoi_a = r"Find the measure of angle $\widehat{ACB}$."
        giai_a = (r"Angle $\widehat{CBH} = 60^{\circ}$ is the exterior angle at $B$ of triangle $ABC$, so "
                  r"$\widehat{ACB} = 60^{\circ} - 30^{\circ} = 30^{\circ}$.")

        hoi_b = r"Find the length $BC$."
        BC = d
        giai_b = (r"Triangle $ABC$ has $\widehat{A} = \widehat{ACB} = 30^{\circ}$, so it is isosceles at $B$, "
                  r"hence $BC = AB = %d\,\text{m}$." % d)

        hoi_c = r"Find the height $CH$."
        giai_c = (r"Triangle $BCH$ is right-angled at $H$ with $\widehat{CBH} = 60^{\circ}$, so\\ "
                  r"$CH = BC\cdot\sin 60^{\circ} = %d\cdot\dfrac{\sqrt{3}}{2} = %s\,\text{(m)}$."
                  % (d, latex(h)))

        ds_abcd = [(hoi_a, r"30^{\circ}", giai_a),
                   (hoi_b, latex(BC), giai_b),
                   (hoi_c, latex(h), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI - bốn ý phải TĂNG DẦN mức độ:
#     a) NB   nhận biết  - nhắc lại một công thức, một tính chất
#     b) TH   thông hiểu - thay số vào đúng một công thức
#     c) VD   vận dụng   - phải có kết quả của ý trước mới làm được
#     d) VDC  vận dụng cao - phải tự nghĩ ra cách, không có công thức sẵn
# Quy ước này áp cho MỌI hàm _TF_; tests/test_cau_dung_sai.py soi các mốc
# "# a) NB", "# b) TH", "# c) VD", "# d) VDC" trong thân hàm.
# =====================================================================
def L10_C3_TF_A_01(socau, socot=1):
    """Đúng/Sai - giá trị lượng giác của một góc từ 0 độ đến 180 độ."""
    BO_BA_PYTHAGORE = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
    cauTF = ''
    for _ in range(socau):
        d = random.choice([30, 45, 60])
        bu = 180 - d
        hang = [r for r in BANG_GTLG if r[0] == d][0]
        cos_d = hang[2]
        doi, ke, huyen = random.choice(BO_BA_PYTHAGORE)

        debai = r"Given the angle $\alpha = %s$. Determine whether each of the following statements is true or false:" % _goc(d)

        # a) NB - nhắc lại quan hệ giữa hai góc bù nhau
        y1 = [(r"{\True $\sin %s = \sin %s$}" % (_goc(bu), _goc(d)),
               r"True. Supplementary angles have equal sines."),
              (r"{$\sin %s = -\sin %s$}" % (_goc(bu), _goc(d)),
               r"False. Supplementary angles have \textbf{equal} sines, not opposite ones.")]

        # b) TH - thay số: dùng quan hệ bù nhau rồi tra bảng
        y2 = [(r"{\True $\cos %s = %s$}" % (_goc(bu), _L(simplify(-cos_d))),
               r"Supplementary angles have opposite cosines, so $\cos %s = -\cos %s = %s$."
               % (_goc(bu), _goc(d), _L(simplify(-cos_d)))),
              (r"{$\cos %s = %s$}" % (_goc(bu), _L(cos_d)),
               r"False. That is $\cos %s$; the cosines of supplementary angles are \textbf{opposite}, so $\cos %s = %s$."
               % (_goc(d), _goc(bu), _L(simplify(-cos_d))))]

        # c) VD - phải dùng CẢ hai quan hệ ở trên, RỒI tra bảng giá trị
        #         của chính góc alpha đã cho mới ra được số
        # together: gộp thành MỘT phân số cho gọn, ví dụ
        # 1/2 - căn3/2  ->  (1 - căn3)/2  chứ không để rời hai phân số
        P = together(simplify(hang[1] - cos_d))     # sin(alpha) - cos(alpha)
        P_sai = together(simplify(hang[1] + cos_d))
        y3 = [(r"{\True The value of the expression $P = \sin\left(180^{\circ} - \alpha\right) "
               r"+ \cos\left(180^{\circ} - \alpha\right)$ equals $%s$}" % _gon(P),
               r"We have $\sin\left(180^{\circ}-\alpha\right) = \sin\alpha$ and "
               r"$\cos\left(180^{\circ}-\alpha\right) = -\cos\alpha$, so "
               r"$P = \sin\alpha - \cos\alpha$.\\ "
               r"For $\alpha = %s$, $P = %s - %s = %s$."
               % (_goc(d), _L(hang[1]), _L(cos_d), _gon(P))),
              (r"{The value of the expression $P = \sin\left(180^{\circ} - \alpha\right) "
               r"+ \cos\left(180^{\circ} - \alpha\right)$ equals $%s$}" % _gon(P_sai),
               r"False. That is $\sin\alpha + \cos\alpha$; it forgets that "
               r"$\cos\left(180^{\circ}-\alpha\right) = \textbf{--}\cos\alpha$, "
               r"so $P = \sin\alpha - \cos\alpha = %s$." % _gon(P))]

        # d) VDC - đổi sang một góc tù chưa biết: phải dùng hệ thức cơ bản
        #          VÀ xét dấu của côsin trên khoảng góc tù
        y4 = [(r"{\True If $90^{\circ} < \beta < 180^{\circ}$ and $\sin\beta = \dfrac{%d}{%d}$ "
               r"then $\cos\beta = -\dfrac{%d}{%d}$}" % (doi, huyen, ke, huyen),
               r"From $\sin^{2}\beta + \cos^{2}\beta = 1$ we get "
               r"$\cos^{2}\beta = 1 - \left(\dfrac{%d}{%d}\right)^{2} = \dfrac{%d}{%d}$, "
               r"so $\cos\beta = \pm\dfrac{%d}{%d}$.\\ "
               r"Since $90^{\circ} < \beta < 180^{\circ}$, $\beta$ is an obtuse angle and its cosine is \textbf{negative}, "
               r"hence $\cos\beta = -\dfrac{%d}{%d}$."
               % (doi, huyen, ke * ke, huyen * huyen, ke, huyen, ke, huyen)),
              (r"{If $90^{\circ} < \beta < 180^{\circ}$ and $\sin\beta = \dfrac{%d}{%d}$ "
               r"then $\cos\beta = \dfrac{%d}{%d}$}" % (doi, huyen, ke, huyen),
               r"False. The error is in the \textbf{sign}. The fundamental identity gives $\cos\beta = \pm\dfrac{%d}{%d}$, "
               r"but an obtuse angle has a negative cosine, so $\cos\beta = -\dfrac{%d}{%d}$."
               % (ke, huyen, ke, huyen))]

        # --- Bổ sung 01/10/2026 (cô Lan): mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai ---
        s_d, t_d, k_d = hang[1], hang[3], hang[4]
        B_, D_ = _goc(bu), _goc(d)
        ly1 = r"Supplementary angles have equal sines; their cosines, tangents and cotangents are opposite."
        _tf_them(y1, [(r"$\cos %s = -\cos %s$" % (B_, D_), ly1), (r"$\tan %s = -\tan %s$" % (B_, D_), ly1),
                      (r"$\cot %s = -\cot %s$" % (B_, D_), ly1)],
                 [(r"$\cos %s = \cos %s$" % (B_, D_), ly1), (r"$\tan %s = \tan %s$" % (B_, D_), ly1),
                  (r"$\sin %s = \cos %s$" % (B_, D_), ly1), (r"$\cot %s = \cot %s$" % (B_, D_), ly1)])
        ly2 = (r"Supplementary angles: $\sin %s = \sin %s = %s$, $\cos %s = -\cos %s = %s$, $\tan %s = -\tan %s = %s$."
               % (B_, D_, _L(s_d), B_, D_, _L(-cos_d), B_, D_, _L(-t_d)))
        d_, s_ = _tf_ct(r"$\sin %s = %s$" % (B_, "%s"), s_d, ly2, [(-s_d, "Sign error"), (cos_d, "Confused $\\sin$ with $\\cos$")])
        d2, s2 = _tf_ct(r"$\tan %s = %s$" % (B_, "%s"), -t_d, ly2, [(t_d, "Forgot to change the sign"), (-k_d, "Confused $\\tan$ with $\\cot$")])
        _tf_them(y2, d_ + d2, s_ + s2)
        ly3 = (r"$\sin\left(180^{\circ}-\alpha\right) = \sin\alpha$, $\cos\left(180^{\circ}-\alpha\right) = -\cos\alpha$, "
               r"$\tan\left(180^{\circ}-\alpha\right) = -\tan\alpha$, $\cot\left(180^{\circ}-\alpha\right) = -\cot\alpha$; for "
               r"$\alpha = %s$: $\sin\alpha = %s$, $\cos\alpha = %s$, $\tan\alpha = %s$, $\cot\alpha = %s$."
               % (D_, _L(s_d), _L(cos_d), _L(t_d), _L(k_d)))
        Q = together(simplify(s_d + cos_d))
        T = together(simplify(-t_d - k_d))
        d1, s1 = _tf_ct(r"The value of the expression $Q = \sin\left(180^{\circ} - \alpha\right) - \cos\left(180^{\circ} - \alpha\right)$ equals $%s$",
                        Q, ly3, [(together(simplify(s_d - cos_d)), "Forgot to change the sign of the cosine"), (together(simplify(-s_d - cos_d)), "Changed the sign of the sine by mistake")])
        d2, s2 = _tf_ct(r"The value of the expression $T = \tan\left(180^{\circ} - \alpha\right) + \cot\left(180^{\circ} - \alpha\right)$ equals $%s$",
                        T, ly3, [(together(simplify(t_d + k_d)), "Forgot to change the sign"), (together(simplify(-t_d + k_d)), "Forgot to change the sign of the cotangent")])
        _tf_them(y3, d1 + d2, s1 + s2)
        ly4 = (r"Since $90^{\circ} < \beta < 180^{\circ}$, $\cos\beta = -\dfrac{%d}{%d}$, so "
               r"$\tan\beta = \dfrac{\sin\beta}{\cos\beta} = -\dfrac{%d}{%d}$, $\cot\beta = -\dfrac{%d}{%d}$."
               % (ke, huyen, doi, ke, ke, doi))
        nd = r"If $90^{\circ} < \beta < 180^{\circ}$ and $\sin\beta = \dfrac{%d}{%d}$ then $%s = %s$"
        tb, cb = Rational(-doi, ke), Rational(-ke, doi)
        _tf_them(y4, [(nd % (doi, huyen, r"\tan\beta", _L(tb)), ly4), (nd % (doi, huyen, r"\cot\beta", _L(cb)), ly4)],
                 [(nd % (doi, huyen, r"\tan\beta", _L(-tb)), "Sign error. " + ly4), (nd % (doi, huyen, r"\tan\beta", _L(cb)), "Numerator and denominator swapped. " + ly4),
                  (nd % (doi, huyen, r"\cos\beta", _L(Rational(-doi, huyen))), "Confused $\\sin$ with $\\cos$. " + ly4)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_B_01(socau, socot=1):
    """Đúng/Sai - hệ thức lượng trong tam giác."""
    cauTF = ''
    for _ in range(socau):
        A = random.choice([60, 120])
        b, c = random.choice([x for x in CAP_COSIN[A] if x[0] >= 5])
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)
        # sin 60 = sin 120 = căn3/2 nên hai trường hợp dùng chung
        R = simplify(Rational(a, 2) / (sqrt(3) / 2))
        # Phân giác trong góc A: AD = 2bc.cos(A/2)/(b+c)
        cos_nua_A = sqrt(3) / 2 if A == 60 else Rational(1, 2)
        AD = simplify(2 * b * c * cos_nua_A / (b + c))

        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$, $\widehat{A} = %s$. "
                 r"Determine whether each of the following statements is true or false:" % (b, c, _goc(A)))

        # a) NB - nhắc lại định lí côsin
        y1 = [(r"{\True $BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A$}",
               r"True. This is exactly the law of cosines."),
              (r"{$BC^{2} = AC^{2} + AB^{2} + 2\cdot AC\cdot AB\cdot\cos A$}",
               r"False. The law of cosines has a \textbf{minus} sign before the last term.")]

        # b) TH - thay số vào đúng công thức vừa nhắc ở ý a)
        y2 = [(r"{\True $BC = %d$}" % a,
               r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, so $BC = %d$."
               % (b, c, b, c, _L(cos_A), a2, a)),
              (r"{$BC = %d$}" % (b + c),
               r"False. $BC = %d$, not the sum of the other two sides." % a)]

        # c) VD - phải có BC của ý b) rồi mới dùng được định lí sin
        y3 = [(r"{\True The circumradius of triangle $ABC$ is $R = %s$}" % _L(R),
               r"Law of sines: $\dfrac{BC}{\sin A} = 2R$, so $R = \dfrac{BC}{2\sin A}$.\\ "
               r"With $\sin %s = \dfrac{\sqrt{3}}{2}$ and $BC = %d$, "
               r"$R = \dfrac{%d}{2\cdot\dfrac{\sqrt{3}}{2}} = %s$."
               % (_goc(A), a, a, _L(R))),
              (r"{The circumradius of triangle $ABC$ is $R = %s$}"
               % _L(simplify(R / 2)),
               r"False. That is $\dfrac{BC}{4\sin A}$; the law of sines gives $\dfrac{BC}{\sin A} = 2R$, "
               r"so $R = \dfrac{BC}{2\sin A} = %s$." % _L(R))]

        # d) VDC - tách diện tích tam giác làm hai phần để tính đường phân giác.
        #    CHỈ dùng công thức TRONG CHƯƠNG:
        #      - S = 1/2 . AB . AC . sin A          (công thức diện tích, bài 6)
        #      - bảng giá trị lượng giác góc đặc biệt (bài 5)
        #      - phân giác chia góc A thành hai góc bằng nhau (hình học lớp 7)
        #    KHÔNG dùng sin A = 2 sin(A/2) cos(A/2): đó là công thức nhân đôi
        #    của lớp 11, học sinh lớp 10 chưa học. Ở đây không cần, vì góc A
        #    chỉ là 60 hoặc 120 độ nên sin A và sin(A/2) đều tra thẳng bảng.
        nua = A // 2
        sin_nua = sqrt(3) / 2 if nua == 60 else Rational(1, 2)
        sin_A = sqrt(3) / 2                      # đúng cho cả 60 và 120 độ
        sin_nua_lan = Rational(1, 2) if nua == 60 else sqrt(3) / 2   # lấy nhầm
        AD = simplify(b * c * sin_A / ((b + c) * sin_nua))
        AD_sai = simplify(b * c * sin_A / ((b + c) * sin_nua_lan))
        y4 = [(r"{\True Let $AD$ be the interior angle bisector of angle $A$ $\left(D \in BC\right)$, "
               r"then $AD = %s$}" % _L(AD),
               r"$AD$ is the bisector of angle $A$, so it divides the angle $%s$ into two equal angles: "
               r"$\widehat{BAD} = \widehat{CAD} = %s$.\\ "
               r"Since $D$ lies on side $BC$, triangle $ABC$ is divided into two triangles "
               r"$ABD$ and $ACD$, so $S_{ABD} + S_{ACD} = S_{ABC}$.\\ "
               r"Using the area formula $S = \dfrac{1}{2}\cdot\text{side}\cdot\text{side}\cdot\sin(\text{included angle})$:\\ "
               r"$\dfrac{1}{2}\cdot %d\cdot AD\cdot\sin %s + \dfrac{1}{2}\cdot %d\cdot AD\cdot\sin %s "
               r"= \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s$.\\ "
               r"From the table: $\sin %s = %s$ and $\sin %s = %s$; substituting:\\ "
               r"$\dfrac{1}{2}\cdot %s\cdot AD\cdot\left(%d + %d\right) "
               r"= \dfrac{1}{2}\cdot %s\cdot %d$.\\ "
               r"Simplifying gives $AD = %s$."
               % (_goc(A), _goc(nua),
                  c, _goc(nua), b, _goc(nua), b, c, _goc(A),
                  _goc(nua), _L(sin_nua), _goc(A), _L(sin_A),
                  _L(sin_nua), c, b, _L(sin_A), b * c,
                  _L(AD))),
              (r"{Let $AD$ be the interior angle bisector of angle $A$ $\left(D \in BC\right)$, "
               r"then $AD = %s$}" % _L(AD_sai),
               r"False, because the sine of \textbf{half of angle} $A$ was used by mistake. "
               r"The bisector divides the angle $%s$ into two angles $%s$, and $\sin %s = %s$ "
               r"(not $%s$).\\ "
               r"Substituting correctly into $S_{ABD} + S_{ACD} = S_{ABC}$ gives $AD = %s$."
               % (_goc(A), _goc(nua), _goc(nua), _L(sin_nua),
                  _L(sin_nua_lan), _L(AD)))]

        # --- Bổ sung 01/10/2026 (cô Lan): mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai ---
        ly1 = r"The law of cosines, its corollary, the law of sines and the area formulas of triangle $ABC$."
        _tf_them(y1, [(r"$\cos A = \dfrac{AB^{2} + AC^{2} - BC^{2}}{2\cdot AB\cdot AC}$", ly1), (r"$\dfrac{BC}{\sin A} = 2R$", ly1),
                      (r"$S_{ABC} = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A$", ly1)],
                 [(r"$\cos A = \dfrac{AB^{2} + AC^{2} - BC^{2}}{AB\cdot AC}$", ly1), (r"$\dfrac{BC}{\sin A} = R$", ly1),
                  (r"$S_{ABC} = AB\cdot AC\cdot\sin A$", ly1), (r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\sin A$", ly1)])
        ly2 = (r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, so $BC = %d$."
               % (b, c, b, c, _L(cos_A), a2, a))
        d_, s_ = _tf_ct(r"$BC = %s$", Integer(a), ly2,
                        [(sqrt(Integer(b * b + c * c - dau * b * c)), "Wrong sign of $\\cos A$"), (sqrt(Integer(b * b + c * c)), "Omitted the term containing $\\cos A$"),
                         (Integer(abs(b - c)), "Took the difference of two sides")], them=[r"$BC^{2} = %d$" % a2])
        _tf_them(y2, d_, s_)
        ly3 = r"Law of sines: $\dfrac{BC}{\sin A} = 2R$, so $R = \dfrac{BC}{2\sin A} = %s$, and the diameter is $2R = %s$." % (_L(R), _L(simplify(2 * R)))
        d_, s_ = _tf_ct(r"The circumradius of triangle $ABC$ is $R = %s$", R, ly3,
                        [(simplify(2 * R), "That is $2R$"), (simplify(Rational(a, 2) / abs(cos_A)), "Confused $\\sin A$ with $\\cos A$")])
        d2, s2 = _tf_ct(r"The diameter of the circumscribed circle of triangle $ABC$ equals $%s$", simplify(2 * R), ly3, [(R, "That is the radius")])
        _tf_them(y3, d_ + d2, s_ + s2)
        ly4 = r"From $S_{ABD} + S_{ACD} = S_{ABC}$ (part d) we get $AD = %s$." % _L(AD)
        d_, s_ = _tf_ct(r"The length of the interior angle bisector $AD$ of angle $A$ equals $%s$", AD, ly4,
                        [(AD_sai, "Used the sine of half of angle $A$ by mistake"), (simplify(2 * AD), "Forgot the factor $\\dfrac{1}{2}$"),
                         (Rational(b * c, b + c), "Omitted the sine values")])
        _tf_them(y4, d_, s_)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_B6_VD036_SA_A_01(socau, dang=2):
    """Đo khoảng cách khi gặp vật cản (trả lời ngắn): đáp số nguyên, đơn vị mét."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        if b < 6 or c < 6 or (A, b, c) in gt:
            continue
        gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        d2 = b * b + c * c + dau * b * c
        d = int(round(d2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)

        debai = (r"To measure the distance between two points $A$ and $B$ separated by a swamp, a point "
                 r"$C$ that can be reached directly is chosen and one measures $CA = %d\,\text{m}$, $CB = %d\,\text{m}$, "
                 r"$\widehat{ACB} = %s$. Find the distance $AB$ (in meters)."
                 % (b, c, _goc(A)))
        giai = (r"Law of cosines: $AB^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, "
                r"so $AB = %d\,\text{m}$." % (b, c, b, c, latex(cos_A), d2, d))
        ds = [str(b + c), str(d + 2), str(d - 2)]
        ds = [x for x in dict.fromkeys(ds) if x != str(d)][:3]
        while len(ds) < 3:
            ds.append(str(d + len(ds) + 5))
        cauTN += MC_SA_answer_const(debai, str(d), ds, giai, 0, 0, dang)
    return cauTN



_BOI_CANH_VAT_CAN = [
    (r"The two ends $A$, $B$ of a tunnel through a mountain cannot be measured "
     r"directly. From a point $C$ at the foot of the mountain, one measures", r"the length of tunnel $AB$"),
    (r"Two points $A$, $B$ lie on opposite banks of a lake. From a point $C$ on the shore, "
     r"one measures", r"the distance $AB$"),
    (r"A house blocks the line of sight between two utility poles $A$ and $B$. From position $C$, "
     r"an engineer measures", r"the distance between the two utility poles"),
]


def L10_C3_B6_VD036_SA_A_02(socau, dang=2):
    r"""Khoảng cách giữa hai địa điểm khi gặp vật cản (định lí côsin) - bối
    cảnh đường hầm / hồ nước / nhà che khuất, đáp số nguyên (mét).

    CLAUDE THEM 29/09/2026 - bien the 02, cung dang voi _01 (dam lay).
    Co Lan duyet.
    """
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        k = random.choice([10, 20, 30])            # phong to cho thuc te hon
        if (A, b, c, k) in gt or (b + c) * k > 900:
            continue
        gt.append((A, b, c, k))
    cau = ''
    for A, b, c, k in gt:
        B_, C_ = b * k, c * k
        d2 = B_ * B_ + C_ * C_ + (-1 if A == 60 else 1) * B_ * C_
        d = int(round(d2 ** 0.5))
        mo, hoi = random.choice(_BOI_CANH_VAT_CAN)
        debai = (mo + r" $CA = %d\,\text{m}$, $CB = %d\,\text{m}$ and $\widehat{ACB} = %s$. "
                 r"Find %s (in meters)." % (B_, C_, _goc(A), hoi))
        giai = (r"In triangle $ABC$, by the law of cosines:\\ "
                r"$AB^{2} = CA^{2} + CB^{2} - 2\cdot CA\cdot CB\cdot\cos %s "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
                r"Hence $AB = %d\,\text{m}$."
                % (_goc(A), B_, C_, B_, C_, r"\dfrac{1}{2}" if A == 60 else r"-\dfrac{1}{2}", d2, d))
        ds = _ba_nhieu(str(d), [str(B_ + C_), str(abs(C_ - B_)),
                                str(int(round((B_ * B_ + C_ * C_) ** 0.5)))],
                       buoc=lambda t: str(d + 10 * t))
        cau += MC_SA_answer_text(debai, str(d), ds, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_A_03(socau, dang=2):
    r"""Khoảng cách tới một điểm KHÔNG TỚI ĐƯỢC (bên kia sông) bằng định lí
    sin: biết đoạn $AC$ đo được và hai góc tại $A$, $C$; làm tròn đến hàng
    phần mười.

    CLAUDE THEM 29/09/2026 - bien the 03 (cung dang: khoang cach giua hai
    dia diem khi gap vat can). Dap so toi da 4 ki tu. Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        d = random.randrange(20, 91, 5)
        al = random.randrange(40, 86, 5)
        ga = random.randrange(40, 86, 5)
        if al + ga >= 150:
            continue
        ab = d * math.sin(math.radians(ga)) / math.sin(math.radians(al + ga))
        kq = round(ab, 1)
        if not 10 <= kq < 100 or (d, al, ga) in [g[:3] for g in gt]:
            continue
        gt.append((d, al, ga, kq))
    cau = ''
    for d, al, ga, kq in gt:
        be = 180 - al - ga
        dap = _xx(kq, 1)
        debai = (r"To measure the distance from point $A$ on a riverbank to a tree $B$ on the opposite bank, "
                 r"a point $C$ on the same bank as $A$ is chosen and one measures $AC = %d\,\text{m}$, "
                 r"$\widehat{BAC} = %s$, $\widehat{BCA} = %s$. Find the distance $AB$ (in "
                 r"meters, rounded to the nearest tenth)." % (d, _goc(al), _goc(ga)))
        giai = (r"In triangle $ABC$: $\widehat{ABC} = 180^{\circ} - %s - %s = %s$.\\ "
                r"By the law of sines: $\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B}$, so\\ "
                r"$AB = \dfrac{AC\cdot\sin C}{\sin B} = \dfrac{%d\cdot\sin %s}{\sin %s} "
                r"\approx %s\,\text{m}$." % (_goc(al), _goc(ga), _goc(be), d, _goc(ga), _goc(be), dap))
        sai1 = _xx(round(d * math.sin(math.radians(al)) / math.sin(math.radians(al + ga)), 1), 1)
        sai2 = _xx(round(d * math.sin(math.radians(ga)) / math.sin(math.radians(al)), 1), 1)
        ds = _ba_nhieu(dap, [sai1, sai2], buoc=lambda t: _xx(kq + t, 1))
        cau += MC_SA_answer_text(debai, dap, ds, giai, 0, 0, dang)
    return cau


# =====================================================================
# CÁC DẠNG CHUYỂN TỪ TỆP 10-3.py CỦA CÔ LAN (27/09/2026)
# ---------------------------------------------------------------------
# Bản cũ ghi thẳng ra latex\data\de.tex và để \loigiai{} RỖNG. Ở ngân
# hàng này mỗi hàm phải TRẢ VỀ chuỗi LaTeX và phải có lời giải đầy đủ
# (trợ giảng AI chỉ được lấy đáp án từ đây, không tự tính).
# =====================================================================

def _L(x):
    r"""latex() nhưng dùng \dfrac cho phân số, đúng kiểu cô Lan vẫn viết."""
    return latex(x).replace(r"\frac", r"\dfrac")


def _toa_do_nua_duong_tron(p, q, doi, ben_trai):
    r"""Toạ độ một điểm trên nửa đường tròn đơn vị, sinh từ cặp p < q.

    Vì $\left(\dfrac{p}{q}\right)^2 + \left(\dfrac{\sqrt{q^2-p^2}}{q}\right)^2 = 1$
    nên điểm luôn nằm ĐÚNG trên đường tròn đơn vị; lấy tung độ dương để
    ở nửa trên.
    """
    can = sqrt(Integer(q * q - p * p)) / q
    hoanh, tung = (can, Rational(p, q)) if doi else (Rational(p, q), can)
    if ben_trai:
        hoanh = -hoanh
    return simplify(hoanh), simplify(tung)




def L10_C3_B5_NB029_MC_D_01(socau, dang=1):
    r"""Nhận biết giá trị lượng giác nào CÓ THỂ xảy ra với góc từ 0 độ đến 180 độ.

    LƯU Ý khi làm phương án nhiễu: chỉ được dùng $\sin$ hoặc $\cos$ cho
    phương án "giá trị vượt quá 1". KHÔNG dùng $\tan$ hay $\cot$ vì
    $\tan\alpha = 2$ là chuyện có thật (góc khoảng $63^{\circ}$) - khi đó
    câu hỏi sẽ có HAI đáp án đúng.
    """
    gt = []
    while len(gt) < socau:
        p, q = _cap_nguyen_to_cung_nhau()
        r1, r2 = _cap_nguyen_to_cung_nhau()
        v = (p, q, r1, r2, random.choice([r"\sin", r"\cos"]),
             random.choice([2, 3, 4, -2, -3, -4]))
        if v not in gt:
            gt.append(v)

    debai = (r"Given an angle $\alpha$ with $0^{\circ} \le \alpha \le 180^{\circ}$. "
             r"Which of the following statements \textbf{can} occur?")

    cauTN = ''
    for p, q, r1, r2, ten, nguyen in gt:
        dung = r"$\cos\alpha = -\dfrac{%d}{%d}$" % (p, q)
        giai = (r"For $0^{\circ} \le \alpha \le 180^{\circ}$, the point $M$ moves on the unit semicircle "
                r"lying \textbf{above} the horizontal axis, so\\ "
                r"$\sin\alpha = y_{0} \ge 0$ and $-1 \le \cos\alpha = x_{0} \le 1$.\\ "
                r"$\bullet$ $\sin\alpha = -\dfrac{%d}{%d} < 0$: rejected, because the sine of an angle from "
                r"$0^{\circ}$ to $180^{\circ}$ is non-negative.\\ "
                r"$\bullet$ $%s\alpha = %d$: rejected, because $\left| %d \right| > 1$.\\ "
                r"$\bullet$ $\cos\alpha = \dfrac{%d}{%d} > 1$: rejected.\\ "
                r"$\bullet$ $\cos\alpha = -\dfrac{%d}{%d}$: accepted, because the cosine of an obtuse angle is negative "
                r"and $\dfrac{%d}{%d} \le 1$."
                % (r1, r2, ten, nguyen, nguyen, q, p, p, q, p, q))
        ds = _ba_nhieu(dung,
                       [r"$\sin\alpha = -\dfrac{%d}{%d}$" % (r1, r2),
                        r"$%s\alpha = %d$" % (ten, nguyen),
                        r"$\cos\alpha = \dfrac{%d}{%d}$" % (q, p)],
                       buoc=lambda k: r"$\sin\alpha = -\dfrac{%d}{%d}$" % (k, k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


# ---- Hình vẽ (giữ nguyên TikZ cô Lan đã dựng trong tệp 10-3.py) ------
HINH_DOI_XUNG_OY = r"""\begin{tikzpicture}[>=stealth,x=1.0cm,y=1.0cm,thick,scale=1.2]
\def \r {1.5}   \def \goc {50}
\draw[->] (-\r - 0.7,0) -- (\r + 0.7,0) node[below] {$x$};
\draw[->] (0,-0.7) -- (0,\r + 0.7) node[left] {$y$};
\draw (\r,0) arc (0:180:\r);
\tkzDefPoint(\goc:\r){M}
\tkzDefPoint(180 - \goc:\r){N}
\fill[black] (M) circle[radius=1.4pt] node[above right]{\footnotesize $M$};
\fill[black] (N) circle[radius=1.4pt] node[above left]{\footnotesize $N$};
\fill[black] (0,0) circle[radius=0.4pt] node[below left]{\footnotesize $O$};
\draw (N)--(0,0)--(M);
\draw[dashed] (N)--(M);
\end{tikzpicture}"""

HINH_DAM_LAY = r"""\begin{tikzpicture}[scale=1, font=\footnotesize, line join=round, line cap=round,>=stealth]
\path
(2,2) coordinate (A) (7,2) coordinate (B) (1.6,4.5) coordinate (C)
(2.5,2) coordinate (D) (3.5,3.1) coordinate (E) (5.5,2.9) coordinate (F)
(6.4,1.5) coordinate (G) (5.2,0.7) coordinate (H) (3.5,0.7) coordinate (I)
(2.6,1.3) coordinate (J) ;
\draw[fill=gray!40]
(D) .. controls ++(65:0.1) and ++(200: 1) .. (E)
.. controls ++(200:-0.5) and ++(170: 0.3) .. (F)
.. controls ++(170:-0.5) and ++(100: 0.3) .. (G)
.. controls ++(100:-0.3) and ++(30: 0.3) .. (H)
.. controls ++(30:-0.3) and ++(150: -0.3) .. (I)
.. controls ++(150:0.3) and ++(130: -0.3) .. (J)
.. controls ++(130:0.3) and ++(65: -0.1) .. (D) ;
\draw[dashed] (A)--(B)--(C) ;
\draw (A)--(C) ;
\foreach \x/\g in {A/-120,B/-60,C/90}
\fill[black] (\x) circle (1pt)+(\g:3mm) node {$\x$};
\end{tikzpicture}"""


def _tam_giac_cu_lao(c, A, B):
    """Phần tam giác ABC của hình cù lao (cô Lan 01/10/2026: số đo góc phải nằm giữa góc
    khi đổi số liệu). C cố định ở gốc cây, A và B trên bờ y = -3; nhãn góc đặt trên
    đường phân giác, nhãn cạnh ở dưới trung điểm AB.
    Góc thật (60-85 độ) vẽ đúng thì tam giác quá hẹp, không đặt được nhãn, nên vẽ góc
    "thu nhỏ" g = 47 + 0.5(góc - 60): vẫn giữ góc lớn hơn thì vẽ lớn hơn (hình minh hoạ)."""
    Cx, Cy, y0 = -1.38, -0.13, -3.0
    h = Cy - y0
    gA, gB = 47 + 0.5 * (A - 60), 47 + 0.5 * (B - 60)
    Bx = Cx - h / math.tan(math.radians(gB))
    Ax = Cx + h / math.tan(math.radians(gA))

    def _nhan(Px, Py, Qx, Qy, Rx, Ry, r):
        # điểm cách đỉnh P một đoạn r trên phân giác góc QPR
        u = [Qx - Px, Qy - Py]
        v = [Rx - Px, Ry - Py]
        lu, lv = math.hypot(*u), math.hypot(*v)
        w = [u[0] / lu + v[0] / lv, u[1] / lu + v[1] / lv]
        lw = math.hypot(*w)
        return Px + r * w[0] / lw, Py + r * w[1] / lw

    xa, ya = _nhan(Ax, y0, Cx, Cy, Bx, y0, 1.55)
    xb, yb = _nhan(Bx, y0, Ax, y0, Cx, Cy, 1.4)
    return ("\\tkzDefPoints{%.3f/%.3f/C,%.3f/%.3f/B,%.3f/%.3f/A}\n" % (Cx, Cy, Bx, y0, Ax, y0)
            + "\\tkzDrawPoints[fill=black](A,B,C)\n\\tkzDrawPolygon[very thick](A,B,C)\n"
            + "\\node[below] at (%.3f,%.3f) {$%d$};\n" % ((Ax + Bx) / 2, y0, c)
            + "\\tkzLabelPoints[below](A,B)\n\\tkzLabelPoints[above right](C)\n"
            + "\\tkzMarkAngles[size=.7cm,arc=l,mark=|](C,A,B)\n"
            + "\\tkzMarkAngles[size=.6cm,arc=l,mark=||](A,B,C)\n"
            + "\\node at (%.3f,%.3f) {$%d^{\\circ}$};\n" % (xa, ya, A)
            + "\\node at (%.3f,%.3f) {$%d^{\\circ}$};\n" % (xb, yb, B))


def _hinh_cu_lao(c, A, B):
    """Hình con sông và cù lao; nhãn cạnh AB và hai góc lấy theo số liệu đề."""
    return r"""\begin{tikzpicture}[scale=.7, font=\footnotesize, line join = round, line cap = round,>=stealth]
\clip (-4.39,3.2) rectangle (4,-4);
\draw[pattern=north east lines,opacity=0.3] plot[smooth] coordinates{(-4.39,1.43)(-2.43,1.46) (-1.48,1.67)(1.43,2.12)(2.01,2.09)(4,1.64) (4.1,-1.06)(3.02,-0.77)(1.85,-1.38)(0.95,-1.48)(0.13,-1.72)(-1.48,-1.67)(-2.46,-1.51)(-3.57,-0.98)(-4.37,-1.08)};
\draw[opacity=3] plot[smooth] coordinates{(-4.39,1.43)(-2.43,1.46) (-1.48,1.67)(1.43,2.12)(2.01,2.09)(4,1.64) (4.1,-1.06)(3.02,-0.77)(1.85,-1.38)(0.95,-1.48)(0.13,-1.72)(-1.48,-1.67)(-2.46,-1.51)(-3.57,-0.98)(-4.37,-1.08)};
\draw[fill=white] plot[smooth  cycle] coordinates{(-2.75,-0.08)(-1.83,0.32) (-0.03,0.42) (1,0) (0.24,-0.48)(-0.58,-0.79)(-1.38,-0.77)(-1.91,-0.71)};
\draw[fill=black!70]  plot[smooth  cycle] coordinates{(-2.14,0.58)(-2.09,0.24)(-2.33,-0.13) (-1.19,-0.13) (-1.38,-0.13) (-1.69,0.21)(-1.75,0.53)};
\draw[fill=blue!30]  plot[smooth  cycle] coordinates{(-1.75,0.53)(-1.46,0.79) (-1.01,0.58) (-1.08,1.06) (-0.64,1.08)(-0.93,1.59)(-0.53,1.85)(-0.93,2.2)(-1.38,2.7)(-2.04,3.18)(-2.49,2.91)(-3.07,2.91)(-3.2,2.22)(-3.73,1.96)(-3.1,1.3)(-3.31,1.01)(-2.83,1.01)(-2.99,0.69)(-2.14,0.58)};
%s\end{tikzpicture}""" % _tam_giac_cu_lao(c, A, B)


def L10_C3_B5_TH031_MC_B_01(socau, dang=1):
    """Hai điểm đối xứng qua Oy trên nửa đường tròn đơn vị: quan hệ hai góc bù nhau."""
    GIA_TRI = {r"\sin": "y_{0}", r"\cos": "- x_{0}",
               r"\tan": r"- \dfrac{y_{0}}{x_{0}}", r"\cot": r"- \dfrac{x_{0}}{y_{0}}"}
    gt = []
    while len(gt) < socau:
        ten = random.choice(list(GIA_TRI))
        if ten not in gt:
            gt.append(ten)

    cauTN = ''
    for ten in gt:
        debai = (r"In the coordinate plane $Oxy$, take a point $M\left( x_{0}; y_{0} \right)$ on the unit "
                 r"semicircle as shown in the figure. Let $N$ be the reflection of $M$ across the $Oy$ axis. "
                 r"Determine $%s\widehat{xON}$." % ten)
        giai = (r"Since $N$ is the reflection of $M$ across the $Oy$ axis, $N\left( -x_{0}; y_{0} \right)$, "
                r"that is, $\widehat{xON} = 180^{\circ} - \widehat{xOM}$.\\ "
                r"By the definition of trigonometric values of an angle from $0^{\circ}$ to $180^{\circ}$:\\ "
                r"$\sin\widehat{xON} = y_{0}$, $\cos\widehat{xON} = -x_{0}$, "
                r"$\tan\widehat{xON} = \dfrac{y_{0}}{-x_{0}} = -\dfrac{y_{0}}{x_{0}}$, "
                r"$\cot\widehat{xON} = \dfrac{-x_{0}}{y_{0}} = -\dfrac{x_{0}}{y_{0}}$.\\ "
                r"Hence $%s\widehat{xON} = %s$." % (ten, GIA_TRI[ten]))
        dung = r"$%s\widehat{xON} = %s$" % (ten, GIA_TRI[ten])
        ds = _ba_nhieu(dung, [r"$%s\widehat{xON} = %s$" % (ten, v)
                              for k, v in GIA_TRI.items() if k != ten])
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, HINH_DOI_XUNG_OY, 0, dang)
    return cauTN


def L10_C3_B5_TH030_MC_C_01(socau, dang=1):
    """Dùng máy tính cầm tay tính giá trị lượng giác của một góc bất kì.

    Bản cũ (nhánh cos) đưa cùng một giá trị vào HAI phương án nhiễu nên
    câu hỏi có hai đáp án giống nhau; ở đây bắt buộc bốn phương án phân
    biệt, và phải kiểm tra ba khẳng định nhiễu đều SAI thật.
    """
    TEN = [r"\sin", r"\cos", r"\tan", r"\cot"]
    DAC_BIET = (30, 45, 60, 90, 120, 135, 150)
    gt = []
    while len(gt) < socau:
        goc = random.choice(list(range(20, 70)) + list(range(110, 160)))
        if goc in DAC_BIET:
            continue
        ten = random.choice(TEN)
        rad = math.radians(goc)
        val = {r"\sin": math.sin(rad), r"\cos": math.cos(rad),
               r"\tan": math.tan(rad), r"\cot": 1 / math.tan(rad)}
        v = val[ten]
        # ba khẳng định nhiễu dùng TÊN KHÁC nhưng cùng con số: phải bảo đảm
        # chúng SAI thật, tức giá trị đúng của tên đó lệch hẳn con số này
        if any(abs(val[k] - v) < 0.005 for k in TEN if k != ten):
            continue
        if abs(v) > 20:
            continue
        if (goc, ten) not in gt:
            gt.append((goc, ten))

    cauTN = ''
    for goc, ten in gt:
        rad = math.radians(goc)
        val = {r"\sin": math.sin(rad), r"\cos": math.cos(rad),
               r"\tan": math.tan(rad), r"\cot": 1 / math.tan(rad)}
        so = _xx(val[ten])
        dung = r"$%s %d^{\circ} \approx %s$" % (ten, goc, so)
        giai = (r"Using a scientific calculator ($\mathrm{DEG}$ mode):\\ "
                r"$\sin %d^{\circ} \approx %s$, $\cos %d^{\circ} \approx %s$, "
                r"$\tan %d^{\circ} \approx %s$, $\cot %d^{\circ} \approx %s$.\\ "
                r"Hence only $%s %d^{\circ} \approx %s$ is correct."
                % (goc, _xx(val[r"\sin"]), goc, _xx(val[r"\cos"]),
                   goc, _xx(val[r"\tan"]), goc, _xx(val[r"\cot"]), ten, goc, so))
        ds = _ba_nhieu(dung, [r"$%s %d^{\circ} \approx %s$" % (k, goc, so)
                              for k in TEN if k != ten])
        cauTN += MC_SA_answer_text(debai_MTCT(), dung, ds, giai, 0, 0, dang)
    return cauTN


def debai_MTCT():
    return r"Which of the following statements is \textbf{true}?"



def L10_C3_B6_TH033_MC_B_01(socau, dang=1):
    """Định lí sin: tính bán kính đường tròn ngoại tiếp, góc bất kì (bấm máy)."""
    DAC_BIET = (30, 45, 60, 90, 120, 135, 150)
    gt = []
    while len(gt) < socau:
        a = random.randint(3, 19)
        A = random.randint(20, 160)
        if A in DAC_BIET or (a, A) in gt:
            continue
        gt.append((a, A))

    cauTN = ''
    for a, A in gt:
        sinA = math.sin(math.radians(A))
        R = a / (2 * sinA)
        dung = r"$R \approx %s$" % _xx(R)
        giai = (r"Law of sines in triangle $ABC$: $\dfrac{BC}{\sin A} = 2R$, "
                r"so $R = \dfrac{BC}{2\sin A}$.\\ "
                r"With $BC = %d$ and $\sin %d^{\circ} \approx %s$, "
                r"$R \approx \dfrac{%d}{2\cdot %s} \approx %s$."
                % (a, A, _xx(sinA, 4), a, _xx(sinA, 4), _xx(R)))
        ds = _ba_nhieu(
            dung,
            [r"$R \approx %s$" % _xx(a / sinA),          # quên chia 2
             r"$R \approx %s$" % _xx(a * sinA / 2),      # nhân thay vì chia
             r"$R \approx %s$" % _xx(2 * sinA / a)],     # lộn ngược phân số
            buoc=lambda k: r"$R \approx %s$" % _xx(R + k))
        debai = (r"Given triangle $ABC$ with $\widehat{A} = %d^{\circ}$ and $BC = %d$. "
                 r"Calculate the circumradius $R$ of triangle $ABC$ "
                 r"(rounded to the nearest hundredth)." % (A, a))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN



def L10_C3_B6_VD036_TL_B_01(socau, dong=1):
    """Tự luận: đo khoảng cách từ bờ sông tới gốc cây trên cù lao (định lí sin).

    Bản cũ chỉ hỏi MỘT ý; theo quy ước đã chốt, câu tự luận phải có từ
    HAI ý trở lên - nên tách đúng theo hai bước của lời giải cũ: tìm góc
    thứ ba, rồi mới tính khoảng cách.
    """
    gt = []
    while len(gt) < socau:
        A = random.randint(12, 17) * 5
        B = random.randint(12, 17) * 5
        c = random.choice([30, 40, 50, 60])
        if A == B or A + B > 150 or (A, B, c) in gt:
            continue
        gt.append((A, B, c))

    cauTN = ''
    for A, B, c in gt:
        C = 180 - A - B
        sinB, sinC = math.sin(math.radians(B)), math.sin(math.radians(C))
        AC = c * sinB / sinC

        debai = (r"To measure the distance from a point $A$ on a riverbank to a tree $C$ on an islet "
                 r"in the middle of the river, a point $B$ on the same bank as $A$ is chosen so that both $A$ "
                 r"and $B$ can see point $C$. One measures $AB = %d\,\text{m}$, "
                 r"$\widehat{CAB} = %d^{\circ}$ and $\widehat{CBA} = %d^{\circ}$." % (c, A, B))
        ds_abcd = [
            (r"Find the measure of angle $\widehat{ACB}$.",
             r"%d^{\circ}" % C,
             r"Since the sum of the three angles of triangle $ABC$ is $180^{\circ}$,\\ "
             r"$\widehat{ACB} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$."
             % (A, B, C)),
            (r"Find the distance from $A$ to the tree $C$ (rounded to the nearest hundredth).",
             r"%s\,\text{m}" % _xx(AC),
             r"By the law of sines in triangle $ABC$:\\ "
             r"$\dfrac{AC}{\sin \widehat{B}} = \dfrac{AB}{\sin \widehat{C}} "
             r"\Rightarrow AC = \dfrac{AB\cdot\sin \widehat{B}}{\sin \widehat{C}} "
             r"= \dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} \approx %s\,\text{(m)}$."
             % (c, B, C, _xx(AC))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, _hinh_cu_lao(c, A, B), 0, dong)
    return cauTN


# =====================================================================
# CAC DANG CO LAN DA TU CHUYEN SANG FORM MOI (tep LopXChuong3.py)
# Nhap 28/09/2026. Noi dung toan va loi giai giu NGUYEN nhu co viet;
# chi doi ten ham theo ID ngan hang va va cac loi neu co.
# =====================================================================

# ---- Toa do M tren nua duong tron don vi -> gia tri luong giac ----
# (ten cu cua co: K10_3_3_1_1_H)
def L10_C3_B5_NB029_MC_B_01(socau, dang=1):
    gt = []
    dem = len(gt)
    while dem < socau:
        # Sinh dữ liệu ngẫu nhiên
        a = []
        while len(a) < 2:
            k = random.randint(1, 10)  # Giảm giới hạn để đảm bảo sqrt(b^2 - a^2) là số đẹp hơn
            if k not in a:
                a.append(k)

        a.sort()
        # Đảm bảo b > a để căn bậc hai dương (với b là mẫu số/bán kính)
        if a[0] == a[1]:
            a[1] += random.randint(1, 5)
            a.sort()

        d1 = math.gcd(a[0], a[1])
        A = int(a[0] / d1)
        B = int(a[1] / d1)
        C_square = B ** 2 - A ** 2

        # Đảm bảo C_square dương
        if C_square <= 0:
            continue

        gtlg = random.choice(['\\sin', '\\cos'])
        choice = random.choice([0, 1, 2, 3])  # Chọn 1 trong 4 dạng tọa độ

        # choice: 0: (A/B, sqrt(C)/B), 1: (sqrt(C)/B, A/B), 2: (-A/B, sqrt(C)/B), 3: (-sqrt(C)/B, A/B)
        v = [A, B, C_square, gtlg, choice]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        A, B, C_square, gtlg, choice = v

        if choice == 0:
            # M(A/B, sqrt(C)/B). sin = sqrt(C)/B, cos = A/B
            M_toa_do = f"\\left( \\dfrac{{{A}}}{{{B}}}; \\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}} \\right)"
            dapso_sin = f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"
            dapso_cos = f"\\dfrac{{{A}}}{{{B}}}"

        elif choice == 1:
            # M(sqrt(C)/B, A/B). sin = A/B, cos = sqrt(C)/B
            M_toa_do = f"\\left( \\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}; \\dfrac{{{A}}}{{{B}}} \\right)"
            dapso_sin = f"\\dfrac{{{A}}}{{{B}}}"
            dapso_cos = f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"

        elif choice == 2:
            # M(-A/B, sqrt(C)/B). sin = sqrt(C)/B, cos = -A/B
            M_toa_do = f"\\left( -\\dfrac{{{A}}}{{{B}}}; \\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}} \\right)"
            dapso_sin = f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"
            dapso_cos = f"-\\dfrac{{{A}}}{{{B}}}"

        elif choice == 3:
            # M(-sqrt(C)/B, A/B). sin = A/B, cos = -sqrt(C)/B
            M_toa_do = f"\\left( -\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}; \\dfrac{{{A}}}{{{B}}} \\right)"
            dapso_sin = f"\\dfrac{{{A}}}{{{B}}}"
            dapso_cos = f"-\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"

        debai = f"""In the coordinate plane $Oxy$, take a point $M {M_toa_do}$ on the unit semicircle. Find ${gtlg} \\widehat{{ xOM }}$.
        """

        # Tính đáp số đúng và các nhiễu
        if gtlg == '\\sin':
            dapso = dapso_sin
            nhieu_val = [dapso_cos, f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{A}}}",
                         f"-\\dfrac{{{A}}}{{{B}}}" if B != A else f"-\\dfrac{{{B}}}{{{A}}}"]
        else:  # gtlg == 'cos'
            dapso = dapso_cos
            nhieu_val = [dapso_sin, f"\\dfrac{{{A}}}{{\\sqrt{{{C_square}}}}}",
                         f"-\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}" if C_square > 0 else f"\\dfrac{{{A}}}{{{B}}}"]

        # SỬA 28/09/2026: bản gốc gom nhiễu rồi mới lọc trùng TRONG vòng lặp,
        # nên nếu danh sách đã đủ ba phần tử mà trong đó có hai phần tử giống
        # nhau thì vòng lặp không chạy, và MC_SA_answer_const nhận [x, y, y]
        # -> quay mãi không dừng (đo được: treo 4/8 lần). Nay dùng _ba_nhieu:
        # bảo đảm đúng ba phương án đôi một khác nhau và khác đáp số.
        du_tru = [
            f"-\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}",
            f"-\\dfrac{{{A}}}{{{B}}}",
            f"\\dfrac{{{A}}}{{\\sqrt{{{C_square}}}}}",
            f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{A}}}",
            f"\\dfrac{{{B}}}{{{A}}}",
        ]
        dsnhieu = _ba_nhieu(dapso, list(nhieu_val) + du_tru,
                            buoc=lambda k: f"\\dfrac{{{k}}}{{{B + k}}}")
        nhieu1, nhieu2, nhieu3 = dsnhieu[0], dsnhieu[1], dsnhieu[2]

        # Lời giải
        xM = f"\\dfrac{{{A}}}{{{B}}}" if choice == 0 or choice == 1 else f"-\\dfrac{{{A}}}{{{B}}}" if choice == 2 else f"-\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"
        yM = f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}" if choice == 0 or choice == 2 else f"\\dfrac{{{A}}}{{{B}}}"

        x_coord = f"\\dfrac{{{A}}}{{{B}}}"
        y_coord = f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"

        if choice == 1:
            x_coord, y_coord = y_coord, x_coord
        elif choice == 2:
            x_coord = f"-\\dfrac{{{A}}}{{{B}}}"
        elif choice == 3:
            x_coord = f"-\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"
            y_coord = f"\\dfrac{{{A}}}{{{B}}}"

        giai = f"""
            Point $M(x_M; y_M)$ lies on the unit semicircle (radius $R=1$), so we have:
            \\[\\cos \\widehat{{ xOM }} = x_M \\quad \\text{{and}} \\quad \\sin \\widehat{{ xOM }} = y_M\\]
            From the coordinates of point $M {M_toa_do}$, we have:
            \\begin{{itemize}}
                \\item $x_M = {x_coord}$
                \\item $y_M = {y_coord}$
            \\end{{itemize}}
            The required value is ${gtlg} \\widehat{{ xOM }}$.
            \\begin{{itemize}}
                \\item If we need $\\cos \\widehat{{ xOM }}$, we take $x_M = {dapso_cos}$.
                \\item If we need $\\sin \\widehat{{ xOM }}$, we take $y_M = {dapso_sin}$.
            \\end{{itemize}}
            Therefore, ${gtlg} \\widehat{{ xOM }} = {dapso}$.
        """

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)
    return cauTN



# ---- Gia tri luong giac -> toa do M ----
# (ten cu cua co: K10_3_3_1_2_H)
def L10_C3_B5_NB029_MC_C_01(socau, dang=1):
    gt = []
    dem = len(gt)
    while dem < socau:
        # Sinh dữ liệu ngẫu nhiên
        a = []
        while len(a) < 2:
            k = random.randint(1, 10)
            if k not in a:
                a.append(k)

        a.sort()
        if a[0] == a[1]:
            a[1] += random.randint(1, 5)
            a.sort()

        d1 = math.gcd(a[0], a[1])
        A = int(a[0] / d1)
        B = int(a[1] / d1)
        C_square = B ** 2 - A ** 2

        if C_square <= 0:
            continue

        choice = random.choice([0, 1, 2, 3])

        v = [A, B, C_square, choice]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        A, B, C_square, choice = v

        # 1. Định nghĩa các giá trị lượng giác và tọa độ
        val_A = f"\\dfrac{{{A}}}{{{B}}}"
        val_C = f"\\dfrac{{\\sqrt{{{C_square}}}}}{{{B}}}"

        if choice == 0:
            cos_val = val_A
            sin_val = val_C
            dapso = f"M \\left( {cos_val}; {sin_val} \\right)"
        elif choice == 1:
            cos_val = val_C
            sin_val = val_A
            dapso = f"M \\left( {cos_val}; {sin_val} \\right)"
        elif choice == 2:
            cos_val = f"-{val_A}"
            sin_val = val_C
            dapso = f"M \\left( {cos_val}; {sin_val} \\right)"
        elif choice == 3:
            cos_val = f"-{val_C}"
            sin_val = val_A
            dapso = f"M \\left( {cos_val}; {sin_val} \\right)"

        # 2. Xây dựng đề bài
        debai = f"""In the coordinate plane $Oxy$, take a point $M$ on the unit semicircle.
        Given that $\\sin \\widehat{{ xOM }} = {sin_val}$ and $\\cos \\widehat{{ xOM }} = {cos_val}$. Find the coordinates of point $M$.
        """

        # 3. Xây dựng **tất cả** phương án nhiễu tiềm năng (chỉ góc I và II)

        potential_nhieu = set()

        # Nhiễu 1: Hoán đổi x, y (dấu giữ nguyên)
        nhieu1_x = cos_val if sin_val == val_A else sin_val
        nhieu1_y = sin_val if sin_val == val_A else cos_val

        # Điều chỉnh dấu cho đúng cặp (x, y) hoán đổi
        if cos_val[0] == '-' and nhieu1_x[0] != '-':
            nhieu1_x = f"-{nhieu1_x}"
        if sin_val == val_C and nhieu1_y == val_A and cos_val[
            0] == '-':  # Ví dụ: cos=-A/B, sin=C/B. Hoán đổi: x=C/B, y=-A/B (SAI, y phải dương)
            # Cần đảm bảo y_nhiễu >= 0
            nhieu1_y = nhieu1_y.replace('-', '', 1)
            nhieu1 = f"M \\left( {nhieu1_x}; {nhieu1_y} \\right)"
        else:
            nhieu1 = f"M \\left( {nhieu1_x}; {nhieu1_y.replace('-', '', 1)} \\right)"
        potential_nhieu.add(nhieu1)

        # Nhiễu 2: Đảo dấu cos (thay đổi góc phần tư)
        nhieu2_x = f"-{cos_val}" if cos_val[0] != '-' else cos_val.replace('-', '', 1)
        nhieu2_y = sin_val
        potential_nhieu.add(f"M \\left( {nhieu2_x}; {nhieu2_y} \\right)")

        # Nhiễu 3: Đáp án đúng nhưng sin, cos bị viết ngược (thay sin bằng cos và ngược lại trong M(cos; sin))
        potential_nhieu.add(f"M \\left( {sin_val.replace('-', '', 1)}; {cos_val} \\right)")

        # Nhiễu 4: Giữ nguyên cos, đảo dấu sin (SAI với nửa đường tròn) - Vẫn thêm vào để có đủ nhiễu
        potential_nhieu.add(f"M \\left( {cos_val}; -{sin_val} \\right)")

        # Nhiễu 5: Các cặp tọa độ cơ bản khác
        potential_nhieu.add(f"M \\left( {val_A}; {val_C} \\right)")
        potential_nhieu.add(f"M \\left( -{val_A}; {val_C} \\right)")
        potential_nhieu.add(f"M \\left( {val_C}; {val_A} \\right)")
        potential_nhieu.add(f"M \\left( -{val_C}; {val_A} \\right)")

        # Loại bỏ đáp án đúng khỏi tập hợp nhiễu
        final_nhieu_list = list(potential_nhieu - {dapso})

        # Chọn ngẫu nhiên 3 nhiễu từ danh sách đã lọc. Đảm bảo luôn có ít nhất 3 nhiễu.
        if len(final_nhieu_list) < 3:
            # Trường hợp cực hiếm, cần thêm nhiễu khác hẳn
            if A != B:
                final_nhieu_list.append(f"M \\left( \\dfrac{{{B}}}{{{A}}}; \\dfrac{{{A}}}{{{B}}} \\right)")
            else:
                final_nhieu_list.append(f"M \\left( 1; 0 \\right)")

        dsnhieu = random.sample(final_nhieu_list, 3)

        nhieu1, nhieu2, nhieu3 = dsnhieu[0], dsnhieu[1], dsnhieu[2]
        dsnhieu = [nhieu1, nhieu2, nhieu3]

        # 4. Lời giải
        giai = f"""
            Point $M(x_M; y_M)$ lies on the unit semicircle (radius $R=1$).
            By definition, the coordinates of point $M$ on the unit semicircle are:
            \\[x_M = \\cos \\widehat{{ xOM }} \\quad \\text{{and}} \\quad y_M = \\sin \\widehat{{ xOM }}\\]
            By the given conditions, we have:
            \\begin{{itemize}}
                \\item $x_M = \\cos \\widehat{{ xOM }} = {cos_val}$
                \\item $y_M = \\sin \\widehat{{ xOM }} = {sin_val}$
            \\end{{itemize}}
            Thus the coordinates of point $M$ are $M \\left( {cos_val}; {sin_val} \\right)$, that is, ${dapso}$.
            (Since $M$ lies on the unit semicircle, $\\sin \\widehat{{ xOM }} = y_M$ is always positive.)
        """

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)
    return cauTN



# ---- Dinh li cosin, goc bat ki (bam may) ----
# (ten cu cua co: K10_3_3_3_1_H)
def L10_C3_B6_TH032_MC_A_02(socau, dang=1):
    gt = []
    dem = len(gt)
    while dem < socau:
        # Sinh dữ liệu ngẫu nhiên
        # Dùng random.randint() để tránh xung đột với numpy import
        a = random.randint(3, 20)
        b = a + random.randint(1, 5)

        # Chọn góc C không phải các góc đặc biệt
        C = random.randint(20, 160)
        while C in [150, 135, 120, 90, 60, 45, 30]:
            C = random.randint(20, 160)

        # Tính toán kết quả chính xác (cạnh c = AB)
        C_rad = C * math.pi / 180
        c_square = b ** 2 + a ** 2 - 2 * a * b * math.cos(C_rad)

        if c_square <= 0:  # Đảm bảo tam giác hợp lệ
            continue

        c = round(math.sqrt(c_square), 2)

        # Tính các nhiễu
        # Nhiễu 1: Dùng dấu + thay vì - trong định lý cos
        c_sai1 = round(math.sqrt(b ** 2 + a ** 2 + 2 * a * b * math.cos(C_rad)), 2)

        # Nhiễu 2: Không đổi góc sang radian
        try:
            # math.cos(C) với C là độ sẽ ra kết quả sai (cần là radian), nhưng là nhiễu hợp lý
            c_sai2 = round(math.sqrt(b ** 2 + a ** 2 - 2 * a * b * math.cos(C)), 2)
        except ValueError:
            # Đảm bảo c_sai2 hợp lệ (nếu phép căn bị âm)
            c_sai2 = round(math.sqrt(b ** 2 + a ** 2 + a * b), 2)

        # Nhiễu 3: Dùng sin thay vì cos
        try:
            c_sai3 = round(math.sqrt(b ** 2 + a ** 2 - 2 * a * b * math.sin(C_rad)), 2)
        except ValueError:
            # Đảm bảo c_sai3 hợp lệ (nếu phép căn bị âm)
            c_sai3 = round(math.sqrt(b ** 2 + a ** 2 + a * b), 2)

        # Tạo tập hợp các giá trị
        v = [a, b, C, c, c_sai1, c_sai2, c_sai3]

        # Kiểm tra xem đáp án và các nhiễu có đủ 4 giá trị khác nhau không
        if v not in gt and len(set([c, c_sai1, c_sai2, c_sai3])) == 4:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        a, b, C, c, c_sai1, c_sai2, c_sai3 = v

        # Định dạng đề bài
        debai = f"""
        Given triangle $ABC$ with $\\widehat{{ C }} = {C} ^\\circ$ and sides $AC = {a}$, $BC = {b}$. Find the length of side $AB$.
        """

        # Định dạng đáp án và các nhiễu (dạng chuỗi đầy đủ)
        dapso = f"AB \\approx {c}"
        nhieu1 = f"AB \\approx {c_sai1}"
        nhieu2 = f"AB \\approx {c_sai2}"
        nhieu3 = f"AB \\approx {c_sai3}"

        # Chuẩn bị dsnhieu cho hàm gọi
        dsnhieu = [nhieu1, nhieu2, nhieu3]

        # Lời giải
        cos_C_giai = round(math.cos(C * math.pi / 180), 4)
        c_square_giai = round(c ** 2, 2)

        giai = f"""
        Apply the law of cosines to triangle $ABC$ to find the length of side $AB$ (that is, side $c$) with angle $\\widehat{{ C }}$ and the two sides $AC=b={a}$, $BC=a={b}$.
        Formula: $c^2 = a^2 + b^2 - 2ab \\cos C$.
        With $a={b}$, $b={a}$, $C = {C}^\\circ$, we have:
        \\[AB^2 = {b}^2 + {a}^2 - 2 \\cdot {b} \\cdot {a} \\cdot \\cos({C}^\\circ)\\]
        \\[AB^2 = {b ** 2 + a ** 2} - {2 * a * b} \\cdot \\cos({C}^\\circ)\\]
        Using $\\cos({C}^\\circ) \\approx {cos_C_giai}$, we obtain:
        \\[AB^2 \\approx {c_square_giai}\\]
        \\[AB = \\sqrt{{AB^2}} \\approx {c}\\]
        Therefore the length of side $AB$ is approximately ${c}$.
        """

        # Chuyển đáp số và nhiễu thành giá trị số đơn thuần (String) để hàm MC_SA_answer_const xử lý.
        # Ở đây tôi dùng hàm MC_SA_answer_text vì đáp án bao gồm cả chữ "AB \approx"
        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN



# ---- Do khoang cach qua dam lay bang dinh li sin (co hinh) ----
# (ten cu cua co: K10_3_3_4_1_H)
def L10_C3_B6_VD036_MC_B_01(socau, dang=1):
    gt = []
    dem = len(gt)
    while dem < socau:
        # 1. Sinh dữ liệu đảm bảo tam giác hợp lệ
        b = random.randint(3, 20)  # AC
        A = random.randint(92, 118)
        C = random.randint(35, 70)

        # Đảm bảo tổng A + C < 180 và B > 0
        while A + C >= 170:  # Giới hạn 170 để góc B không quá nhỏ
            A = random.randint(92, 118)
            C = random.randint(35, 70)

        B = 180 - A - C

        # 2. Tính toán kết quả chính xác (cạnh c = AB)
        # Định lý Sin: c/sinC = b/sinB => c = b * sinC / sinB

        C_rad = C * math.pi / 180
        B_rad = B * math.pi / 180

        c = round(b * math.sin(C_rad) / math.sin(B_rad), 2)

        # 3. Tính các nhiễu
        # Lấy giá trị đã được làm tròn
        c_val = round(b * math.sin(C_rad) / math.sin(B_rad), 2)
        c_sai1_val = round(b * math.sin(B_rad) / math.sin(C_rad), 2)
        c_sai2_val = round(b * math.sin(C_rad), 2)
        c_sai3_val = round(b * math.sin(C_rad) + b, 2)

        # Chuyển sang chuỗi và thay thế dấu thập phân
        c = str(c_val).replace('.', DAU_THAP_PHAN)
        c_sai1 = str(c_sai1_val).replace('.', DAU_THAP_PHAN)
        c_sai2 = str(c_sai2_val).replace('.', DAU_THAP_PHAN)
        c_sai3 = str(c_sai3_val).replace('.', DAU_THAP_PHAN)

        v = [b, A, C, B, c, c_sai1, c_sai2, c_sai3]

        # Kiểm tra tính duy nhất và tính hợp lệ của nhiễu
        if v not in gt and len(set([c, c_sai1, c_sai2, c_sai3])) == 4:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        b, A, C, B, c, c_sai1, c_sai2, c_sai3 = v

        # 4. Tạo mã TikZ cho đồ thị (Dùng code mẫu đã cho)
        dothi_de = f"""
        \\begin{{tikzpicture}}[scale=1, font=\\footnotesize, line join=round, line cap=round,>=stealth]
        \\path
        (2,2) coordinate (A)
        (7,2) coordinate (B)
        (1.6,4.5) coordinate (C)
        (2.5,2) coordinate (D)
        (3.5,3.1) coordinate (E)
        (5.5,2.9) coordinate (F)
        (6.4,1.5) coordinate (G)
        (5.2,0.7) coordinate (H)
        (3.5,0.7) coordinate (I)
        (2.6,1.3) coordinate (J) ; 
        \\draw[fill=gray!40]
        (D)
        .. controls ++(65:0.1) and ++(200: 1) .. (E)
        .. controls ++(200:-0.5) and ++(170: 0.3) .. (F)
        .. controls ++(170:-0.5) and ++(100: 0.3) .. (G)
        .. controls ++(100:-0.3) and ++(30: 0.3) .. (H)
        .. controls ++(30:-0.3) and ++(150: -0.3) .. (I)
        .. controls ++(150:0.3) and ++(130: -0.3) .. (J)
        .. controls ++(130:0.3) and ++(65: -0.1) .. (D) ; 
        \\draw[dashed] (A)--(B)--(C) ;
        \\draw (A)--(C)   ;
        \\foreach \\x/\\g in {{A/-120,B/-60,C/90}}
        \\fill[black] (\\x) circle (1pt)+(\\g:3mm) node {{$\\x$}};
        \\node at ($(A)!0.5!(C)$) [left] {{$ {b} $}};
        \\draw (A) ++(0:{.5}) arc (0:100:{.5}) node at ($(A)+(50:0.8)$) {{${A}^\\circ$}};
        \\draw (C) ++(-80:{.5}) arc (-80:-23:{.5}) node at ($(C)+(-50:0.8)$) {{${C}^\\circ$}};
        \\draw (C) ++(-80:{.55}) arc (-80:-23:{.55}) node at ($(C)+(-50:0.8)$) {{${C}^\\circ$}};
        \\end{{tikzpicture}}
        """

        # 5. Định dạng đề bài
        debai = f"""
        To measure the distance from $A$ to $B$ across a swamp, a point $C$ is chosen as shown in the figure. The distance from $A$ to $C$ is measured to be ${b}$ m. It is also known that points $B$ and $C$ are seen from point $A$ at an angle of $ {A} ^\\circ$, and points $A$ and $B$ are seen from point $C$ at an angle of $ {C} ^\\circ$. Find the distance from $A$ to $B$.
        """

        # 6. Định dạng đáp án và nhiễu (chỉ là giá trị số xấp xỉ)
        dapso = str(c)
        dsnhieu = [str(c_sai1), str(c_sai2), str(c_sai3)]

        # 7. Lời giải
        giai = f"""
        In triangle $ABC$, we know the two angles $\\widehat{{A}} = {A}^\\circ$, $\\widehat{{C}} = {C}^\\circ$ and side $b = AC = {b}$ m.
        The distance from $A$ to $B$ is the length of side $c=AB$.

        \\textbf{{Step 1: Compute angle $\\widehat{{B}}$}}
        The sum of the three angles in a triangle is $180^\\circ$, so:
        \\[\\widehat{{B}} = 180^\\circ - \\widehat{{A}} - \\widehat{{C}} = 180^\\circ - {A}^\\circ - {C}^\\circ = {B}^\\circ\\]

        \\textbf{{Step 2: Apply the law of sines}}
        We have the ratio:
        \\[\\dfrac{{AB}}{{\\sin C}} = \\dfrac{{AC}}{{\\sin B}}\\]
        Substituting the known values ($AC=b={b}$, $\\widehat{{B}}={B}^\\circ$, $\\widehat{{C}}={C}^\\circ$):
        \\[AB = \\dfrac{{AC \\cdot \\sin C}}{{\\sin B}} = \\dfrac{{{b} \\cdot \\sin({C}^\\circ)}}{{\\sin({B}^\\circ)}}\\]

        \\textbf{{Step 3: Calculation}}
        \\[AB \\approx \\dfrac{{{b} \\cdot {round(math.sin(C_rad), 4)}}}{{{round(math.sin(B_rad), 4)}}} \\approx {c} \\mathrm{{~m}}\\]
        Therefore the distance from $A$ to $B$ is approximately ${c}$ m.
        """

        # Sử dụng MC_SA_answer_const với tham số dothi_de
        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, dothi_de, 0, dang)

    return cauTN



# ---- Tau chay hai chang, tinh khoang cach ----
# (ten cu cua co: K10_3_3_4_3_H)
def L10_C3_B6_VD036_MC_C_01(socau, dang=1):
    gt = []
    dem = 0
    while dem < socau:
        goc1 = random.choice([40, 50, 70, 80])
        goc2 = random.choice([10, 20, 40, 50, 70, 80])
        vt1 = random.choice([20, 30, 40, 50, 60])
        vt2 = random.choice([20, 30, 40, 50, 60])
        t1 = random.choice([30, 35, 40, 45, 50, 55])
        t2 = random.randint(20, 50)

        # ---- Bước 1: Chuyển thời gian sang giờ ----
        t1_h = t1 / 60
        t2_h = t2 / 60

        # ---- Bước 2: Tính chiều dài cạnh ----
        a_val = vt2 * t2_h
        c_val = vt1 * t1_h
        Goc_B_deg = goc1 + goc2
        Goc_B_rad = math.radians(Goc_B_deg)

        b_square_val = a_val ** 2 + c_val ** 2 - 2 * a_val * c_val * math.cos(Goc_B_rad)
        if b_square_val <= 0:
            continue
        b_val = round(math.sqrt(b_square_val), 2)

        # ---- Sinh đáp án nhiễu ----
        z_sai1_val = round(math.sqrt(a_val ** 2 + c_val ** 2), 2)
        z_sai2_val = round(math.sqrt(a_val ** 2 + c_val ** 2 + 2 * a_val * c_val * math.cos(Goc_B_rad)), 2)
        z_sai3_val = round(math.sqrt(a_val ** 2 + c_val ** 2 - a_val * c_val * math.cos(Goc_B_rad)), 2)

        if len(set([b_val, z_sai1_val, z_sai2_val, z_sai3_val])) < 4:
            continue

        gt.append((goc1, goc2, vt1, vt2, t1, t2))
        dem += 1

    cauTN = ''
    for (goc1, goc2, vt1, vt2, t1, t2) in gt:
        # ---- Tính toán lại chính xác ----
        t1_h = t1 / 60
        t2_h = t2 / 60
        a_val = vt2 * t2_h
        c_val = vt1 * t1_h
        Goc_B_deg = goc1 + goc2
        Goc_B_rad = math.radians(Goc_B_deg)
        cos_B = math.cos(Goc_B_rad)

        b_square_val = a_val ** 2 + c_val ** 2 - 2 * a_val * c_val * cos_B
        b_val = round(math.sqrt(b_square_val), 2)

        # ---- Format giá trị ----
        def f(x):
            return str(round(x, 2)).replace('.', DAU_THAP_PHAN)

        a, b, c = f(a_val), f(b_val), f(c_val)
        b_square = f(b_square_val)
        cos_B_str = f(cos_B)
        t1_h_str, t2_h_str = f(t1_h), f(t2_h)

        z_sai1 = f(math.sqrt(a_val ** 2 + c_val ** 2))
        z_sai2 = f(math.sqrt(a_val ** 2 + c_val ** 2 + 2 * a_val * c_val * cos_B))
        z_sai3 = f(math.sqrt(a_val ** 2 + c_val ** 2 - a_val * c_val * cos_B))

        debai = f"""
        A ship departs from beach $A$ and sails in the direction $N {goc1}^\\circ E$ at a speed of ${vt1}$ km/h. 
        After traveling for ${t1}$ minutes to position $B$, the ship turns to the direction $S {goc2}^\\circ E$ 
        and continues at a speed of ${vt2}$ km/h for ${t2}$ more minutes, arriving at island $C$. 
        Approximately how many kilometers is the ship from its starting position?
        """

        giai = f"""
        The ship's path forms triangle $ABC$, where:
        $A$ is the starting position, $B$ is the position where the direction changes, and $C$ is the island.
        The distance to find is $AC$ (side $b$).

        \\textbf{{Step 1. Compute the side lengths}}
        \\begin{{itemize}}
        \\item $AB = c = {vt1} \\cdot {t1_h_str} = {c} \\mathrm{{~(km)}}$
        \\item $BC = a = {vt2} \\cdot {t2_h_str} = {a} \\mathrm{{~(km)}}$
        \\end{{itemize}}

        \\textbf{{Step 2. Determine angle $\\widehat{{ABC}}$}}
        The two directions $N{goc1}^\\circ E$ and $S{goc2}^\\circ E$ both lean toward the east,
        so the angle between the two directions equals the sum of the two bearing angles:
        \\[\\widehat{{ABC}} = {goc1}^\\circ + {goc2}^\\circ = {Goc_B_deg}^\\circ\\]

        \\textbf{{Step 3. Apply the law of cosines}}
        \\[AC^2 = AB^2 + BC^2 - 2AB \\cdot BC \\cdot \\cos(\\widehat{{ABC}})\\]
        Substituting the numbers:
        \\[AC^2 = {c}^2 + {a}^2 - 2 \\cdot {c} \\cdot {a} \\cdot \\cos({Goc_B_deg}^\\circ)\\]
        With $\\cos({Goc_B_deg}^\\circ) \\approx {cos_B_str}$, we get:
        \\[AC^2 \\approx {b_square}\\]
        \\[AC = \\sqrt{{AC^2}} \\approx {b} \\mathrm{{~(km)}}\\]

        Therefore the ship is approximately ${b}$ km from its starting position.
        """

        dapso = b
        dsnhieu = [z_sai1, z_sai2, z_sai3]

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


# bài toán đúng sai của dạng trên


# ---- Tau chay hai chang (dung/sai) ----
# (ten cu cua co: K10_3_3_4_3_TF)
def L10_C3_TF_C_01(socau, socot):
    gt = []
    dem = len(gt)

    # Hàm format ĐÚNG: Dùng dấu phẩy (,), bỏ số 0 thừa. max_decimals = 1 cho góc, 2 cho cạnh
    def f(x, max_decimals=2):
        # Làm tròn theo số chữ số thập phân tối đa cho phép
        x_round = round(x, max_decimals)

        # Định dạng thành chuỗi với dấu chấm
        s = f"{x_round:.{max_decimals}f}"

        # Bỏ các số 0 thừa ở cuối
        while s.endswith('0') and '.' in s:
            s = s[:-1]
        if s.endswith('.'):
            s = s[:-1]

        # Cuối cùng, thay dấu chấm thành dấu phẩy
        return s.replace('.', DAU_THAP_PHAN)

    def calculate_huong_ac(goc1, Goc_A_deg_high_precision):
        """
        Tính hướng AC (từ Bắc, chiều kim đồng hồ) và chuyển sang dạng Lat-Goc-Long.
        Quy tắc: Goc_AC = goc1 + Goc_A_deg
        """
        # Góc từ Bắc (chiều kim đồng hồ) đến AC (giữ độ chính xác cao)
        Goc_AC_raw = goc1 + Goc_A_deg_high_precision

        # Chỉ làm tròn ở BƯỚC CUỐI CÙNG (1 chữ số thập phân)
        Goc_AC_round = round(Goc_AC_raw, 1)

        if Goc_AC_round < 90:
            # Dạng N alpha E
            huong_val = Goc_AC_round
            huong_str = f"N {f(huong_val, 1)}^\\circ E"
        elif Goc_AC_round == 90:
            huong_str = "E"
            huong_val = 90.0
        elif Goc_AC_round < 180:
            # Dạng S alpha E (Goc = 180 - Goc_AC)
            Goc_SE = 180 - Goc_AC_round
            huong_val = Goc_SE
            huong_str = f"S {f(huong_val, 1)}^\\circ E"
        elif Goc_AC_round == 180:
            huong_str = "S"
            huong_val = 0.0
        else:
            return None, None

            # huong_val là góc dùng để sinh nhiễu
        return huong_str, huong_val

    while dem < socau:
        # 1. Chọn góc B
        goc1_list = [10, 20, 30, 40, 50, 70]
        goc2_list = [10, 20, 40, 50, 70, 80]
        goc1 = np.random.choice(goc1_list)
        goc2 = np.random.choice(goc2_list)
        Goc_B_deg = goc1 + goc2
        Goc_B_rad = math.radians(Goc_B_deg)
        cos_B = math.cos(Goc_B_rad)

        # 2. Chọn vận tốc và thời gian để tích ra số không phải làm tròn
        v_t_pairs = [
            (30, 40), (40, 30), (60, 20), (50, 30), (45, 40), (40, 45),
            (25, 36), (40, 75), (50, 54), (70, 36), (60, 25), (75, 20)
        ]

        vt1, t1 = random.choice(v_t_pairs)
        vt2, t2 = random.choice(v_t_pairs)
        while (vt2 == vt1 and t2 == t1):
            vt2, t2 = random.choice(v_t_pairs)

        # ---- Tính toán chính xác $AB$ và $BC$ ----
        a_val = vt2 * t2 / 60
        c_val = vt1 * t1 / 60

        if round(a_val, 2) == round(c_val, 2):
            continue

        # ---- Tính AC (Độ chính xác cao - KHÔNG LÀM TRÒN) ----
        b_square_val = a_val ** 2 + c_val ** 2 - 2 * a_val * c_val * cos_B
        if b_square_val <= 0:
            continue
        b_val_high_precision = math.sqrt(b_square_val)

        # Kết quả làm tròn cuối cùng cho cạnh b (AC)
        b_val = round(b_val_high_precision, 2)

        # Tính toán góc A (Độ chính xác cao - KHÔNG LÀM TRÒN)
        # Sử dụng giá trị b_val_high_precision cho độ chính xác cao nhất
        cos_A = (b_val_high_precision ** 2 + c_val ** 2 - a_val ** 2) / (2 * b_val_high_precision * c_val)

        # Kiểm tra điều kiện cosA
        if -1.000000001 <= cos_A <= 1.000000001:
            # Góc A độ chính xác cao (KHÔNG LÀM TRÒN)
            Goc_A_deg_high_precision = math.degrees(math.acos(np.clip(cos_A, -1.0, 1.0)))
        else:
            continue

        # TÍNH HƯỚNG AC CHÍNH XÁC (Dùng Goc_A_deg_high_precision)
        Huong_AC_str, Huong_AC_deg_val = calculate_huong_ac(goc1, Goc_A_deg_high_precision)
        if Huong_AC_str is None:
            continue

        # ---- Sinh đáp án nhiễu ----
        Goc_B_deg_sai = Goc_B_deg + np.random.choice([-5, 5, 10, -10])
        Huong_AC_deg_sai_val = round(Huong_AC_deg_val + np.random.choice([-2, 2, 5, -5]), 1)

        # Sinh chuỗi nhiễu
        Huong_AC_str_sai = f"N {f(Huong_AC_deg_sai_val, 1)}^\\circ E"

        # Đảm bảo nhiễu khác hẳn đáp án đúng
        if Huong_AC_str_sai == Huong_AC_str:
            Huong_AC_str_sai = f"S {f(Huong_AC_deg_sai_val, 1)}^\\circ E"

        v = [goc1, goc2, vt1, vt2, t1, t2, a_val, c_val, b_val, Goc_B_deg, Goc_A_deg_high_precision, Huong_AC_str,
             Huong_AC_str_sai, Goc_B_deg_sai]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTF = ''
    for v in gt:
        goc1, goc2, vt1, vt2, t1, t2, a_val, c_val, b_val, Goc_B_deg, Goc_A_deg_high_precision, Huong_AC_str, Huong_AC_str_sai, Goc_B_deg_sai = v

        # Áp dụng hàm f(x)
        a, c, b = f(a_val), f(c_val), f(b_val)
        goc_B_dung = f(Goc_B_deg)
        goc_B_sai = f(Goc_B_deg_sai)
        goc1_f = f(goc1)
        goc2_f = f(goc2)

        # Khai báo đề bài chung
        debai = f"""
        A ship departs from beach $A$ and sails in the direction $N {goc1_f}^\\circ E$ at a speed of ${vt1}$ km/h. 
        After traveling for ${t1}$ minutes to position $B$, the ship turns to the direction $S {goc2_f}^\\circ E$ 
        and continues at a speed of ${vt2}$ km/h for ${t2}$ more minutes, arriving at island $C$. 
        Determine whether each of the following statements is true or false:
        """

        # Lời giải chi tiết (không có dấu chấm cuối)
        giai_chung = f"""
        \\textbf{{Problem analysis:}} The ship's path forms triangle $ABC$.
        $AB = c = {vt1} \\cdot \\frac{{{t1}}}{{60}} = {c}$ km 
        $BC = a = {vt2} \\cdot \\frac{{{t2}}}{{60}} = {a}$ km
        Angle $\\widehat{{ABC}} = {goc1_f}^\\circ + {goc2_f}^\\circ = {goc_B_dung}^\\circ$
        By the law of cosines: $AC = b \\approx {b}$ km
        The direction from $A$ to $C$ is ${Huong_AC_str}$
        """

        # a) Độ dài AB hoặc BC
        ds_a = [
            (f"{{\\True The length of segment $AB$ is ${c}$ km}}", f"The length $AB = {c}$ km. The statement is \\textbf{{true}}. {giai_chung}"),
            (f"{{The length of segment $AB$ is ${a}$ km}}",
             f"The length $AB = {c}$ km $\\ne {a}$ km. The statement is \\textbf{{false}}. {giai_chung}"),
            (f"{{\\True The length of segment $BC$ is ${a}$ km}}", f"The length $BC = {a}$ km. The statement is \\textbf{{true}}. {giai_chung}"),
            (f"{{The length of segment $BC$ is ${b}$ km}}",
             f"The length $BC = {a}$ km $\\ne {b}$ km. The statement is \\textbf{{false}}. {giai_chung}"),
        ]

        # b) Góc ABC
        ds_b = [
            (f"{{\\True Angle $\\widehat{{ABC}}$ equals ${goc_B_dung}^\\circ$}}",
             f"Angle $\\widehat{{ABC}} = {goc_B_dung}^\\circ$. The statement is \\textbf{{true}}. {giai_chung}"),
            (f"{{Angle $\\widehat{{ABC}}$ equals ${goc_B_sai}^\\circ$}}",
             f"Angle $\\widehat{{ABC}} = {goc_B_dung}^\\circ \\ne {goc_B_sai}^\\circ$. The statement is \\textbf{{false}}. {giai_chung}"),
            (f"{{Angle $\\widehat{{ABC}}$ equals ${goc1_f}^\\circ$}}",
             f"Angle $\\widehat{{ABC}} = {goc_B_dung}^\\circ \\ne {goc1_f}^\\circ$. The statement is \\textbf{{false}}. {giai_chung}"),
        ]

        # CÂU C: Khoảng cách từ A đến C
        ds_c = [
            (f"{{\\True The distance from $A$ to $C$ is approximately ${b}$ km}}",
             f"By the law of cosines, $AC = b \\approx {b}$ km. The statement is \\textbf{{true}}. {giai_chung}"),
            (f"{{The distance from $A$ to $C$ is approximately ${a}$ km}}",
             f"By the law of cosines, $AC = b \\approx {b}$ km $\\ne {a}$ km. The statement is \\textbf{{false}}. {giai_chung}"),
            (f"{{The distance from $A$ to $C$ is approximately ${c}$ km}}",
             f"By the law of cosines, $AC = b \\approx {b}$ km $\\ne {c}$ km. The statement is \\textbf{{false}}. {giai_chung}"),
        ]

        # CÂU D: Hướng đi từ A đến C
        ds_d = [
            (f"{{\\True To go straight from $A$ to $C$, one should head in the direction ${Huong_AC_str}$}}",
             f"The direction of $AC$ is ${Huong_AC_str}$. The statement is \\textbf{{true}}. {giai_chung}"),
            (f"{{To go straight from $A$ to $C$, one should head in the direction ${Huong_AC_str_sai}$}}",
             f"The direction of $AC$ is ${Huong_AC_str} \\ne {Huong_AC_str_sai}$. The statement is \\textbf{{false}}. {giai_chung}"),
            (f"{{To go straight from $A$ to $C$, one should head in the direction $N {goc1_f}^\\circ E$}}",
             f"The direction of $AC$ is ${Huong_AC_str} \\ne N {goc1_f}^\\circ E$. The statement is \\textbf{{false}}. {giai_chung}"),
        ]

        # --- Bổ sung 01/10/2026 (cô Lan): mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai ---
        _tf_them(ds_a, [(r"The total distance traveled by the ship is $%s$ km" % f(a_val + c_val), giai_chung)],
                 [(r"The length of segment $AB$ is $%s$ km" % f(vt1 * t1), "Forgot to convert minutes to hours. " + giai_chung),
                  (r"The total distance traveled by the ship is $%s$ km" % f(abs(a_val - c_val)), giai_chung)])
        loai_B = "acute" if Goc_B_deg < 90 else ("right" if Goc_B_deg == 90 else "obtuse")
        _tf_them(ds_b, [(r"$\widehat{ABC} = %s^\circ + %s^\circ$" % (goc1_f, goc2_f), giai_chung), (r"Angle $\widehat{ABC}$ is %s" % loai_B, giai_chung)],
                 [(r"Angle $\widehat{ABC}$ is %s" % w, giai_chung) for w in ("acute", "right", "obtuse") if w != loai_B] +
                 ([(r"Angle $\widehat{ABC}$ equals $%s^\circ$" % f(180 - Goc_B_deg), giai_chung)] if Goc_B_deg != 90 else []))
        bt = b_val_high_precision
        nb = 2 if _xa_bien(bt, 2) else 1
        d_, s_ = _tf_so(r"The distance from $A$ to $C$ is approximately $%s$", bt, nb, giai_chung,
                        [(math.sqrt(a_val ** 2 + c_val ** 2), "Forgot the term containing $\\cos B$"),
                         (math.sqrt(a_val ** 2 + c_val ** 2 + 2 * a_val * c_val * cos_B), "Sign error"), (a_val + c_val, "Added the two distances")],
                        dv=r"\,\text{km}")
        _tf_them(ds_c, d_, s_)
        az = round(goc1 + Goc_A_deg_high_precision, 1)
        _tf_them(ds_d, [(r"Island $C$ lies to the east of beach $A$", giai_chung),
                        (r"The direction from $A$ to $C$ makes an angle of $%s^\circ$ with north, measured clockwise" % f(az, 1), giai_chung)],
                 [(r"Island $C$ lies to the west of beach $A$", giai_chung),
                  (r"To go straight from $A$ to $C$, one should head in the direction $S %s^\circ E$" % goc2_f, "That is the direction of the second leg. " + giai_chung),
                  (r"The direction from $A$ to $C$ makes an angle of $%s^\circ$ with north, measured clockwise" % f(round(360 - az, 1), 1), giai_chung)])
        # Sắp xếp lại theo thứ tự: a, b, c (khoảng cách), d (hướng)
        ds_abcd = [ds_a, ds_b, ds_c, ds_d]

        # Gọi hàm TF_baitoan_du để sinh câu hỏi Đúng/Sai
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)

    return cauTF


# =====================================================================
# BỔ SUNG DẠNG CHO CHƯƠNG 3 (28/09/2026)
# ---------------------------------------------------------------------
# Cô Lan: "mỗi dạng cần nhiều ID đề... vào dạng chọn 1 bài, nhưng mỗi
# lần vào nó ra khác đề chứ không chỉ khác số".
#
# Nên chữ cái A, B, C sau loại câu là các DẠNG ĐỀ KHÁC NHAU của cùng một
# yêu cầu cần đạt (hỏi cái khác, cho dữ kiện khác), còn _01 _02 mới là
# cùng một đề đổi số. Khối dưới đây thêm chữ cái mới cho các yêu cầu
# đang mỏng: TH030 (mới có 1 dạng), TH032, TH034 (mới có 2 dạng).
# =====================================================================

# Bộ ba Pythagore: dùng cho các dạng "biết một giá trị lượng giác, tìm
# giá trị còn lại" - luôn ra phân số đẹp.
BO_BA_PYTAGO = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]

# Bộ ba cho ĐÁP SỐ THẬP PHÂN hữu hạn (mẫu chỉ có ước 2 và 5).
BO_BA_THAP_PHAN = [(3, 4, 5), (4, 3, 5), (7, 24, 25), (24, 7, 25),
                   (15, 20, 25), (20, 15, 25)]


def _bang_heron(gioi_han=30):
    """Tam giác ba cạnh nguyên, diện tích nguyên VÀ bán kính nội tiếp nguyên.

    Trả về danh sách (a, b, c, S, p, r). Dùng cho các dạng Heron và đường
    tròn nội tiếp để số liệu luôn đẹp, học sinh không phải bấm máy ra số lẻ.
    """
    ra = []
    for a in range(3, gioi_han + 1):
        for b in range(a, gioi_han + 1):
            for c in range(b, gioi_han + 1):
                if a + b <= c:
                    continue
                if (a + b + c) % 2:
                    continue
                p = (a + b + c) // 2
                t = p * (p - a) * (p - b) * (p - c)
                s = math.isqrt(t)
                if s * s != t or s == 0 or s % p:
                    continue
                ra.append((a, b, c, s, p, s // p))
    return ra


BANG_HERON = _bang_heron()


def _goc_tu_ba_canh(a, b, c):
    """Số đo (độ) của góc đối cạnh a, làm tròn - dùng để nhận dạng tam giác."""
    cos_a = (b * b + c * c - a * a) / (2.0 * b * c)
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_a))))


# ---------------------------------------------------------------------
# BÀI 5 - giá trị lượng giác của một góc từ 0 độ đến 180 độ
# ---------------------------------------------------------------------

def L10_C3_B5_TH030_MC_B_01(socau, dang=1):
    """Biết một giá trị lượng giác và khoảng của góc, tìm giá trị còn lại."""
    gt = []
    while len(gt) < socau:
        doi, ke, huyen = random.choice(BO_BA_PYTAGO)
        tu = random.choice([True, False])        # góc tù hay góc nhọn
        cho_sin = random.choice([True, False])   # đề cho sin hay cho cos
        v = (doi, ke, huyen, tu, cho_sin)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for doi, ke, huyen, tu, cho_sin in gt:
        khoang = (r"$90^{\circ} < \alpha < 180^{\circ}$" if tu
                  else r"$0^{\circ} < \alpha < 90^{\circ}$")
        dau = "-" if tu else ""
        if cho_sin:
            # sin luôn dương trên (0; 180); cos mang dấu theo khoảng
            cho = r"\sin\alpha = \dfrac{%d}{%d}" % (doi, huyen)
            hoi, dapso = r"\cos\alpha", r"%s\dfrac{%d}{%d}" % (dau, ke, huyen)
            giai = (r"From $\sin^{2}\alpha + \cos^{2}\alpha = 1$ we get "
                    r"$\cos^{2}\alpha = 1 - \left(\dfrac{%d}{%d}\right)^{2} "
                    r"= \dfrac{%d}{%d}$, so $\cos\alpha = \pm\dfrac{%d}{%d}$.\\ "
                    r"Since %s, $\alpha$ is %s, so its cosine is %s. "
                    r"Hence $\cos\alpha = %s\dfrac{%d}{%d}$."
                    % (doi, huyen, ke * ke, huyen * huyen, ke, huyen,
                       khoang, "obtuse" if tu else "acute",
                       "negative" if tu else "positive", dau, ke, huyen))
            nhieu = [r"%s\dfrac{%d}{%d}" % ("" if tu else "-", ke, huyen),
                     r"\dfrac{%d}{%d}" % (doi, huyen),
                     r"%s\dfrac{%d}{%d}" % (dau, doi, ke),
                     r"\dfrac{%d}{%d}" % (ke, doi)]
        else:
            cho = r"\cos\alpha = %s\dfrac{%d}{%d}" % (dau, ke, huyen)
            hoi, dapso = r"\sin\alpha", r"\dfrac{%d}{%d}" % (doi, huyen)
            giai = (r"From $\sin^{2}\alpha + \cos^{2}\alpha = 1$ we get "
                    r"$\sin^{2}\alpha = 1 - \left(\dfrac{%d}{%d}\right)^{2} "
                    r"= \dfrac{%d}{%d}$, so $\sin\alpha = \pm\dfrac{%d}{%d}$.\\ "
                    r"For $0^{\circ} < \alpha < 180^{\circ}$, $\sin\alpha$ is always "
                    r"\textbf{positive}. Hence $\sin\alpha = \dfrac{%d}{%d}$."
                    % (ke, huyen, doi * doi, huyen * huyen, doi, huyen, doi, huyen))
            nhieu = [r"-\dfrac{%d}{%d}" % (doi, huyen),
                     r"%s\dfrac{%d}{%d}" % (dau, ke, huyen),
                     r"\dfrac{%d}{%d}" % (doi, ke),
                     r"\dfrac{%d}{%d}" % (ke, doi)]

        debai = (r"Given an angle $\alpha$ satisfying $%s$ and %s. Calculate $%s$."
                 % (cho, khoang, hoi))
        dung = "$%s$" % dapso
        ds = _ba_nhieu(dung, ["$%s$" % x for x in nhieu],
                       buoc=lambda k: r"$\dfrac{%d}{%d}$" % (k, huyen + k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH030_SA_B_01(socau, dang=2):
    """Trả lời ngắn: biết côsin (số thập phân), tìm sin. MỘT câu hỏi, MỘT đáp số."""
    gt = []
    while len(gt) < socau:
        doi, ke, huyen = random.choice(BO_BA_THAP_PHAN)
        tu = random.choice([True, False])
        if (doi, ke, huyen, tu) not in gt:
            gt.append((doi, ke, huyen, tu))

    cauTN = ''
    for doi, ke, huyen, tu in gt:
        cos_val = (-1 if tu else 1) * ke / huyen
        sin_val = doi / huyen
        khoang = (r"$90^{\circ} < \alpha < 180^{\circ}$" if tu
                  else r"$0^{\circ} < \alpha < 90^{\circ}$")
        debai = (r"Given an angle $\alpha$ with $\cos\alpha = %s$ and %s. "
                 r"Calculate $\sin\alpha$." % (_xx(cos_val), khoang))
        giai = (r"Apply $\sin^{2}\alpha + \cos^{2}\alpha = 1$:\\ "
                r"$\sin^{2}\alpha = 1 - \left(%s\right)^{2} = %s$, "
                r"so $\sin\alpha = \pm %s$.\\ "
                r"Since $0^{\circ} < \alpha < 180^{\circ}$, $\sin\alpha$ is always positive, "
                r"we get $\sin\alpha = %s$."
                % (_xx(cos_val), _xx(sin_val * sin_val, 4), _xx(sin_val), _xx(sin_val)))
        dung = _xx(sin_val)
        ds = _ba_nhieu(dung, [_xx(-sin_val), _xx(cos_val), _xx(abs(cos_val))],
                       buoc=lambda k: _xx(sin_val + k / 10.0))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_SA_E_01(socau, dang=2):
    """Trả lời ngắn: rút gọn biểu thức bằng hệ thức cơ bản và quan hệ hai góc bù."""
    gt = []
    while len(gt) < socau:
        v = (random.randint(2, 9), random.randint(2, 9))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for m, n in gt:
        dapso = m + n
        debai = (r"Given an angle $\alpha$ with $0^{\circ} < \alpha < 90^{\circ}$. "
                 r"Calculate the value of the expression\\ "
                 r"$P = %d\left[\sin^{2}\left(180^{\circ} - \alpha\right) "
                 r"+ \cos^{2}\left(180^{\circ} - \alpha\right)\right] "
                 r"+ %d\cdot\tan\alpha\cdot\cot\alpha$." % (m, n))
        giai = (r"Let $\beta = 180^{\circ} - \alpha$. The fundamental trigonometric identity holds for "
                r"every angle, so\\ "
                r"$\sin^{2}\beta + \cos^{2}\beta = 1$, that is, the expression in the square brackets equals $1$.\\ "
                r"Moreover, $\tan\alpha\cdot\cot\alpha = 1$ for every $\alpha$ for which these two values "
                r"are defined.\\ "
                r"Hence $P = %d\cdot 1 + %d\cdot 1 = %d$." % (m, n, dapso))
        dung = str(dapso)
        ds = _ba_nhieu(dung, [str(m * n), str(abs(m - n)), str(m + n + 1)],
                       buoc=lambda k: str(dapso + k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


# ---------------------------------------------------------------------
# BÀI 6 - hệ thức lượng trong tam giác
# ---------------------------------------------------------------------

def L10_C3_B6_TH032_MC_B_01(socau, dang=1):
    """Định lí côsin dùng ngược: biết BA CẠNH, tính côsin của một góc."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        dinh = random.choice(["B", "C"])   # hỏi góc B hoặc góc C cho đa dạng
        if (A, b, c, dinh) not in gt:
            gt.append((A, b, c, dinh))

    cauTN = ''
    for A, b, c, dinh in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        if dinh == "B":
            cos_x = Rational(a * a + c * c - b * b, 2 * a * c)
            ct = (r"\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB}", a, c, b, a, c)
        else:
            cos_x = Rational(a * a + b * b - c * c, 2 * a * b)
            ct = (r"\cos C = \dfrac{BC^{2} + AC^{2} - AB^{2}}{2\cdot BC\cdot AC}", a, b, c, a, b)
        debai = (r"Given triangle $ABC$ with $BC = %d$, $AC = %d$, $AB = %d$. "
                 r"Calculate $\cos %s$." % (a, b, c, dinh))
        giai = (r"The law of cosines for angle $%s$ gives:\\ "
                r"$%s = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$."
                % (dinh, ct[0], ct[1], ct[2], ct[3], ct[4], ct[5], _L(cos_x)))
        dung = "$%s$" % _L(cos_x)
        ds = _ba_nhieu(dung, ["$%s$" % _L(simplify(-cos_x)),
                              "$%s$" % _L(Rational(1, 2) if A == 60 else Rational(-1, 2)),
                              "$%s$" % _L(simplify(cos_x / 2))],
                       buoc=lambda k: "$%s$" % _L(Rational(k, 2 * (k + 2))))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH032_SA_B_01(socau, dang=2):
    """Trả lời ngắn: biết ba cạnh, tính SỐ ĐO (độ) của một góc đặc biệt."""
    gt = []
    while len(gt) < socau:
        loai = random.choice([60, 90, 120])
        if loai == 90:
            doi, ke, huyen = random.choice(BO_BA_PYTAGO)
            v = (90, ke, doi, huyen)          # góc vuông đối cạnh huyền
        else:
            b, c = random.choice(CAP_COSIN[loai])
            dau = -1 if loai == 60 else 1
            a = int(round((b * b + c * c + dau * b * c) ** 0.5))
            v = (loai, b, c, a)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for goc, b, c, a in gt:
        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$, $BC = %d$. "
                 r"Calculate the measure of angle $A$ (in degrees)." % (b, c, a))
        cos_A = Rational(b * b + c * c - a * a, 2 * b * c)
        giai = (r"Law of cosines: $\cos A = \dfrac{AC^{2} + AB^{2} - BC^{2}}{2\cdot AC\cdot AB} "
                r"= \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$.\\ "
                r"Using the table of trigonometric values, the angle whose cosine equals $%s$ is $%s$."
                % (b, c, a, b, c, _L(cos_A), _L(cos_A), _goc(goc)))
        dung = str(goc)
        ds = _ba_nhieu(dung, [str(180 - goc), str(goc // 2), str(goc + 30)],
                       buoc=lambda k: str(goc + 10 * (k + 1)))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_SA_A_01(socau, dang=2):
    """Trả lời ngắn: định lí sin - biết một cạnh và hai góc, tính cạnh còn lại."""
    gt = []
    while len(gt) < socau:
        A, B = random.choice([(30, 90), (90, 30), (30, 60), (45, 90), (90, 45), (60, 90)])
        a = random.randint(3, 14)
        if (A, B, a) not in gt:
            gt.append((A, B, a))

    cauTN = ''
    for A, B, a in gt:
        sin_A = [r[1] for r in BANG_GTLG if r[0] == A][0]
        sin_B = [r[1] for r in BANG_GTLG if r[0] == B][0]
        b = simplify(a * sin_B / sin_A)
        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$. "
                 r"Calculate the length of side $AC$ (rounded to the nearest hundredth)."
                 % (a, _goc(A), _goc(B)))
        giai = (r"Law of sines: $\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B}$, "
                r"so $AC = \dfrac{BC\cdot\sin B}{\sin A}$.\\ "
                r"For $\sin %s = %s$ and $\sin %s = %s$ we have "
                r"$AC = \dfrac{%d\cdot %s}{%s} = %s \approx %s$."
                % (_goc(B), _L(sin_B), _goc(A), _L(sin_A), a, _L(sin_B), _L(sin_A),
                   _L(b), _xx(float(b))))
        # Dap an cua cau TRA LOI NGAN phai la mot SO (hoc sinh go vao o
        # tra loi), khong the la can thuc \dfrac{10\sqrt{3}}{3}. Nen lam
        # tron hai chu so thap phan, va de bai noi ro yeu cau lam tron.
        dung = _xx(float(b))
        ds = _ba_nhieu(dung, [_xx(float(simplify(a * sin_A / sin_B))), str(a),
                              _xx(float(2 * b))],
                       buoc=lambda k: _xx(float(b) + k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_MC_B_01(socau, dang=1):
    """Công thức Heron: biết ba cạnh, tính diện tích tam giác."""
    gt = []
    while len(gt) < socau:
        v = random.choice(BANG_HERON)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a, b, c, S, p, r in gt:
        debai = (r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Calculate the area of triangle $ABC$." % (a, b, c))
        giai = (r"Semiperimeter $p = \dfrac{%d + %d + %d}{2} = %d$.\\ "
                r"Heron's formula:\\ "
                r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} "
                r"= \sqrt{%d\cdot %d\cdot %d\cdot %d} = \sqrt{%d} = %d$."
                % (a, b, c, p, p, p - a, p - b, p - c, S * S, S))
        dung = "$%d$" % S
        ds = _ba_nhieu(dung, ["$%d$" % (2 * S), "$%d$" % p, "$%d$" % (S + p)],
                       buoc=lambda k: "$%d$" % (S + 2 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_SA_E_01(socau, dang=2):
    """Trả lời ngắn: bán kính đường tròn nội tiếp, dùng S = p.r."""
    gt = []
    while len(gt) < socau:
        v = random.choice(BANG_HERON)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a, b, c, S, p, r in gt:
        debai = (r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Calculate the inradius $r$ of triangle $ABC$."
                 % (a, b, c))
        giai = (r"Semiperimeter $p = \dfrac{%d + %d + %d}{2} = %d$.\\ "
                r"Heron's formula: $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$.\\ "
                r"Since $S = p\cdot r$, we have $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$."
                % (a, b, c, p, p, p - a, p - b, p - c, S, S, p, r))
        dung = str(r)
        ds = _ba_nhieu(dung, [str(r + 1), str(S), str(p)],
                       buoc=lambda k: str(r + k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH035_MC_C_01(socau, dang=1):
    """Nhận dạng tam giác nhọn / vuông / tù bằng định lí côsin."""
    gt = []
    while len(gt) < socau:
        kieu = random.choice(["nhon", "vuong", "tu"])
        if kieu == "vuong":
            doi, ke, huyen = random.choice(BO_BA_PYTAGO)
            v = (kieu, ke, doi, huyen)
        elif kieu == "tu":
            b, c = random.choice(CAP_COSIN[120])
            a = int(round((b * b + c * c + b * c) ** 0.5))
            v = (kieu, b, c, a)
        else:
            b, c = random.choice(CAP_COSIN[60])
            a = int(round((b * b + c * c - b * c) ** 0.5))
            v = (kieu, b, c, a)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for kieu, b, c, a in gt:
        # kiem lai bang so: goc lon nhat doi canh lon nhat
        canh = sorted([a, b, c])
        lon = _goc_tu_ba_canh(canh[2], canh[0], canh[1])
        that = "right" if abs(lon - 90) < 1e-9 else ("obtuse" if lon > 90 else "acute")
        debai = (r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"What type of triangle is triangle $ABC$?" % (a, b, c))
        giai = (r"The longest side is $%d$, so the largest angle is the angle opposite that side. "
                r"Let that angle be $\varphi$; the law of cosines gives\\ "
                r"$\cos\varphi = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$.\\ "
                r"The cosine of the largest angle is %s, so the classification of the triangle is as follows: %s."
                % (canh[2], canh[0], canh[1], canh[2], canh[0], canh[1],
                   _L(Rational(canh[0] ** 2 + canh[1] ** 2 - canh[2] ** 2,
                               2 * canh[0] * canh[1])),
                   {"acute": "positive", "right": "equal to $0$", "obtuse": "negative"}[that],
                   {"acute": "has three acute angles", "right": "right", "obtuse": "obtuse"}[that]))
        dung = "%s triangle" % that
        ds = _ba_nhieu(dung, ["%s triangle" % x for x in ("acute", "right", "obtuse", "equilateral")
                              if x != that],
                       buoc=lambda k: "isosceles triangle")
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_SA_Z_01(socau, dang=2):
    """Trả lời ngắn (thực tế): tính diện tích mảnh đất tam giác bằng Heron."""
    NOI = [("a garden plot", "garden plot"), ("a field", "field"),
           ("a plot of land", "plot of land")]
    gt = []
    while len(gt) < socau:
        v = random.choice(BANG_HERON)
        if v[3] >= 20 and v not in gt:      # dien tich du lon cho hop ly thuc te
            gt.append(v)

    cauTN = ''
    for a, b, c, S, p, r in gt:
        ten, goi = random.choice(NOI)
        debai = (r"A surveyor measures %s in the shape of a triangle and finds its three sides to be "
                 r"$%d\,\text{m}$, $%d\,\text{m}$ and $%d\,\text{m}$, respectively. "
                 r"Calculate the area of the %s (in $\text{m}^{2}$)."
                 % (ten, a, b, c, goi))
        giai = (r"Semiperimeter $p = \dfrac{%d + %d + %d}{2} = %d\,\text{(m)}$.\\ "
                r"By Heron's formula:\\ "
                r"$S = \sqrt{p\left(p-a\right)\left(p-b\right)\left(p-c\right)} "
                r"= \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d\,\text{(m}^{2}\text{)}$."
                % (a, b, c, p, p, p - a, p - b, p - c, S))
        dung = str(S)
        ds = _ba_nhieu(dung, [str(2 * S), str(p), str(a + b + c)],
                       buoc=lambda k: str(S + 3 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN



def L10_C3_B6_VD036_SA_Z_02(socau, dang=2):
    r"""Diện tích mảnh đất tam giác khi đo được HAI CẠNH và GÓC XEN GIỮA
    ($S = \dfrac{1}{2}ab\sin C$).

    CLAUDE THEM 29/09/2026 - bien the 02 (cung dang: dien tich manh dat tam
    giac; _01 dung Heron). Goc 30 / 150 do cho dap so nguyen; goc 45, 60,
    120, 135 do lam tron den hang phan muoi. Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        C = random.choice([30, 150, 45, 60, 120, 135])
        a, b = random.randint(5, 40), random.randint(5, 40)
        S = 0.5 * a * b * math.sin(math.radians(C))
        if C in (30, 150):
            if (a * b) % 4 or S > 9999:
                continue
            dap = str(int(round(S)))
            lam_tron = ""
        else:
            S = round(S, 1)
            if S >= 100 or S < 10:
                continue
            dap = _xx(S, 1)
            lam_tron = ", rounded to the nearest tenth"
        if (a, b, C) in [g[:3] for g in gt]:
            continue
        gt.append((a, b, C, dap, lam_tron))
    ten = [("garden plot", "garden plot"), ("field", "field"), ("plot of land", "plot of land")]
    cau = ''
    for a, b, C, dap, lam_tron in gt:
        t1, t2 = random.choice(ten)
        sin_tex = {30: r"\dfrac{1}{2}", 150: r"\dfrac{1}{2}", 45: r"\dfrac{\sqrt{2}}{2}",
                   135: r"\dfrac{\sqrt{2}}{2}", 60: r"\dfrac{\sqrt{3}}{2}",
                   120: r"\dfrac{\sqrt{3}}{2}"}[C]
        debai = (r"A triangular %s $ABC$ has $CA = %d\,\text{m}$, $CB = %d\,\text{m}$ and "
                 r"$\widehat{ACB} = %s$. Calculate the area of the %s (in $\text{m}^{2}$%s)."
                 % (t1, a, b, _goc(C), t2, lam_tron))
        giai = (r"$S = \dfrac{1}{2}\cdot CA\cdot CB\cdot\sin\widehat{ACB} = \dfrac{1}{2}\cdot %d\cdot %d"
                r"\cdot %s %s %s\,\text{(m}^{2}\text{)}$."
                % (a, b, sin_tex, "=" if not lam_tron else r"\approx", dap))
        ds = _ba_nhieu(dap, [str(a * b // 2) if (a * b) % 2 == 0 else str(a * b), str(a * b)],
                       buoc=lambda t: str(int(float(dap.replace(",", "."))) + 2 * t + 1))
        cau += MC_SA_answer_text(debai, dap, ds, giai, 0, 0, dang)
    return cau


def _cap_heron_chung_canh():
    """Hai tam giác Heron có chung một cạnh (làm đường chéo tứ giác)."""
    theo_canh = {}
    for t in BANG_HERON:
        for k in range(3):
            theo_canh.setdefault(t[k], []).append(t)
    ung = [(c, ds) for c, ds in theo_canh.items() if len(ds) >= 2]
    c, ds = random.choice(ung)
    t1, t2 = random.sample(ds, 2)
    return c, t1, t2


def L10_C3_B6_VD036_SA_Z_03(socau, dang=2):
    r"""Diện tích mảnh đất hình TỨ GIÁC khi đo được bốn cạnh và một đường chéo:
    chia thành hai tam giác, dùng Heron hai lần rồi cộng lại.

    CLAUDE THEM 29/09/2026 - bien the 03 (cung dang Heron gives manh dat).
    Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        c, t1, t2 = _cap_heron_chung_canh()
        if t1[3] + t2[3] > 9999 or (c, t1, t2) in gt:
            continue
        gt.append((c, t1, t2))
    cau = ''
    for c, t1, t2 in gt:
        a1 = [x for x in t1[:3]]
        a1.remove(c)
        a2 = [x for x in t2[:3]]
        a2.remove(c)
        AB, BC = a1
        CD, DA = a2
        S = t1[3] + t2[3]
        debai = (r"A plot of land in the shape of quadrilateral $ABCD$ has $AB = %d\,\text{m}$, $BC = %d\,\text{m}$, "
                 r"$CD = %d\,\text{m}$, $DA = %d\,\text{m}$ and diagonal $AC = %d\,\text{m}$ "
                 r"(points $B$ and $D$ lie on opposite sides of $AC$). Calculate the area of the plot "
                 r"(in $\text{m}^{2}$)." % (AB, BC, CD, DA, c))
        giai = (r"The diagonal $AC$ divides the plot into two triangles $ABC$ and $ACD$.\\ "
                r"Triangle $ABC$: $p = \dfrac{%d + %d + %d}{2} = %d$, "
                r"$S_1 = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$.\\ "
                r"Triangle $ACD$: $p = \dfrac{%d + %d + %d}{2} = %d$, "
                r"$S_2 = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$.\\ "
                r"Area of the plot: $S = S_1 + S_2 = %d + %d = %d\,\text{(m}^{2}\text{)}$."
                % (AB, BC, c, t1[4], t1[4], t1[4] - AB, t1[4] - BC, t1[4] - c, t1[3],
                   CD, DA, c, t2[4], t2[4], t2[4] - CD, t2[4] - DA, t2[4] - c, t2[3],
                   t1[3], t2[3], S))
        ds = _ba_nhieu(str(S), [str(t1[3]), str(t2[3]), str(2 * S)],
                       buoc=lambda t: str(S + 3 * t + 1))
        cau += MC_SA_answer_text(debai, str(S), ds, giai, 0, 0, dang)
    return cau

def L10_C3_B6_VD036_TL_C_01(socau, dong=1):
    """Tự luận thực tế: đo hai cạnh và góc xen giữa của một khu đất."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice([x for x in CAP_COSIN[A] if x[0] >= 8])
        if (A, b, c) not in gt:
            gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)
        S = simplify(Rational(1, 2) * b * c * sqrt(3) / 2)

        debai = (r"A triangular plot of land $ABC$ has two sides $AB = %d\,\text{m}$, "
                 r"$AC = %d\,\text{m}$ and the angle between them is "
                 r"$\widehat{A} = %s$." % (c, b, _goc(A)))
        ds_abcd = [
            (r"Calculate the length of side $BC$ (in meters).",
             r"%d\,\text{m}" % a,
             r"The law of cosines in triangle $ABC$:\\ "
             r"$BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos A "
             r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
             r"Hence $BC = %d\,\text{(m)}$."
             % (c, b, c, b, _L(cos_A), a2, a)),
            (r"Calculate the area of the plot (in $\text{m}^{2}$).",
             r"%s\,\text{m}^{2}" % _L(S),
             r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A "
             r"= \dfrac{1}{2}\cdot %d\cdot %d\cdot\dfrac{\sqrt{3}}{2} "
             r"= %s\,\text{(m}^{2}\text{)}$." % (c, b, _L(S))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BỔ SUNG LOẠI CÂU CHO CHƯƠNG 3 (29/09/2026)
# ---------------------------------------------------------------------
# Cô Lan: "cùng 1 dạng có thể ra 3 đến 4 loại, từ nhiều lựa chọn, đúng
# sai, trả lời ngắn, thậm chí cả tự luận."
#
# Trước khối này chương 3 chỉ có câu tự luận ở VD036, và NB029 chỉ toàn
# trắc nghiệm. Khối này lấp các ô còn trống của bảng loại câu.
# =====================================================================

def L10_C3_B5_NB029_SA_B_01(socau, dang=2):
    """Trả lời ngắn: biết toạ độ điểm trên nửa đường tròn đơn vị, đọc ra sin hoặc côsin."""
    gt = []
    while len(gt) < socau:
        doi, ke, huyen = random.choice(BO_BA_THAP_PHAN)
        v = (doi, ke, huyen, random.choice([True, False]), random.choice(["sin", "cos"]))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for doi, ke, huyen, trai, ham in gt:
        x0 = (-1 if trai else 1) * ke / huyen
        y0 = doi / huyen
        dapso = y0 if ham == "sin" else x0
        ten = r"\sin" if ham == "sin" else r"\cos"
        debai = (r"In the coordinate plane $Oxy$, the point $M\left(%s; %s\right)$ lies on the unit "
                 r"semicircle. Calculate $%s\widehat{xOM}$." % (_xx(x0), _xx(y0), ten))
        giai = (r"For a point $M\left(x_{0}; y_{0}\right)$ on the unit semicircle, "
                r"$\cos\widehat{xOM} = x_{0}$ and $\sin\widehat{xOM} = y_{0}$.\\ "
                r"Check: $\left(%s\right)^{2} + \left(%s\right)^{2} = 1$, so $M$ is indeed "
                r"a point on the unit semicircle.\\ "
                r"Hence $%s\widehat{xOM} = %s$." % (_xx(x0), _xx(y0), ten, _xx(dapso)))
        dung = _xx(dapso)
        ds = _ba_nhieu(dung, [_xx(-dapso), _xx(y0 if ham == "cos" else x0),
                              _xx(-(y0 if ham == "cos" else x0))],
                       buoc=lambda k: _xx(dapso + k / 10.0))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH030_TL_A_01(socau, dong=1):
    """Tự luận: biết một giá trị lượng giác và khoảng của góc, tính tiếp."""
    gt = []
    while len(gt) < socau:
        doi, ke, huyen = random.choice(BO_BA_PYTAGO)
        k1, k2 = random.randint(1, 5), random.randint(1, 5)
        v = (doi, ke, huyen, k1, k2)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for doi, ke, huyen, k1, k2 in gt:
        # He so chon boi huyen de P luon nguyen
        m, n = k1 * huyen, k2 * huyen
        P = k1 * doi - k2 * ke          # m.sin + n.cos voi cos am
        debai = (r"Given an angle $\alpha$ satisfying $\sin\alpha = \dfrac{%d}{%d}$ and "
                 r"$90^{\circ} < \alpha < 180^{\circ}$." % (doi, huyen))
        ds_abcd = [
            (r"Calculate $\cos\alpha$.",
             r"-\dfrac{%d}{%d}" % (ke, huyen),
             r"From $\sin^{2}\alpha + \cos^{2}\alpha = 1$ we have "
             r"$\cos^{2}\alpha = 1 - \left(\dfrac{%d}{%d}\right)^{2} = \dfrac{%d}{%d}$, "
             r"so $\cos\alpha = \pm\dfrac{%d}{%d}$.\\ "
             r"Since $90^{\circ} < \alpha < 180^{\circ}$, $\alpha$ is an obtuse angle, so the cosine is negative. "
             r"Hence $\cos\alpha = -\dfrac{%d}{%d}$."
             % (doi, huyen, ke * ke, huyen * huyen, ke, huyen, ke, huyen)),
            (r"Calculate the value of the expression $P = %d\sin\alpha + %d\cos\alpha$." % (m, n),
             r"%d" % P,
             r"Substitute the two values just found:\\ "
             r"$P = %d\cdot\dfrac{%d}{%d} + %d\cdot\left(-\dfrac{%d}{%d}\right) "
             r"= %d - %d = %d$."
             % (m, doi, huyen, n, ke, huyen, k1 * doi, k2 * ke, P)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH032_TL_A_01(socau, dong=1):
    """Tự luận: định lí côsin - tính cạnh thứ ba rồi tính côsin một góc khác."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice(CAP_COSIN[A])
        if (A, b, c) not in gt:
            gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        cos_A = Rational(1, 2) if A == 60 else Rational(-1, 2)
        cos_B = Rational(a * a + c * c - b * b, 2 * a * c)
        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$ and $\widehat{A} = %s$."
                 % (b, c, _goc(A)))
        ds_abcd = [
            (r"Calculate the length of side $BC$.", r"%d" % a,
             r"Law of cosines:\\ "
             r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A "
             r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
             r"Hence $BC = %d$." % (b, c, b, c, _L(cos_A), a2, a)),
            (r"Calculate $\cos B$.", _L(cos_B),
             r"Using the law of cosines again, this time for angle $B$:\\ "
             r"$\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} "
             r"= \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$."
             % (a, c, b, a, c, _L(cos_B))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH033_TL_A_01(socau, dong=1):
    """Tự luận: định lí sin - tính bán kính ngoại tiếp rồi tính một cạnh."""
    gt = []
    while len(gt) < socau:
        A, B = random.choice([(30, 45), (30, 60), (45, 60), (60, 45), (45, 30), (60, 30)])
        a = random.randint(4, 15)
        if (A, B, a) not in gt:
            gt.append((A, B, a))

    cauTN = ''
    for A, B, a in gt:
        sin_A = [r[1] for r in BANG_GTLG if r[0] == A][0]
        sin_B = [r[1] for r in BANG_GTLG if r[0] == B][0]
        R = simplify(a / (2 * sin_A))
        b = simplify(2 * R * sin_B)
        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$."
                 % (a, _goc(A), _goc(B)))
        ds_abcd = [
            (r"Calculate the circumradius $R$ of triangle $ABC$.", _L(R),
             r"Law of sines: $\dfrac{BC}{\sin A} = 2R$, so $R = \dfrac{BC}{2\sin A}$.\\ "
             r"For $\sin %s = %s$ we get $R = \dfrac{%d}{2\cdot %s} = %s$."
             % (_goc(A), _L(sin_A), a, _L(sin_A), _L(R))),
            (r"Calculate the length of side $AC$.", _L(b),
             r"Again by the law of sines: $\dfrac{AC}{\sin B} = 2R$, so $AC = 2R\sin B$.\\ "
             r"$AC = 2\cdot %s\cdot %s = %s$." % (_L(R), _L(sin_B), _L(b))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH034_TL_A_01(socau, dong=1):
    """Tự luận: Heron - tính diện tích rồi tính bán kính đường tròn nội tiếp."""
    gt = []
    while len(gt) < socau:
        v = random.choice(BANG_HERON)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a, b, c, S, p, r in gt:
        debai = r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$." % (a, b, c)
        ds_abcd = [
            (r"Calculate the area of triangle $ABC$.", r"%d" % S,
             r"Semiperimeter $p = \dfrac{%d + %d + %d}{2} = %d$.\\ "
             r"Heron's formula:\\ "
             r"$S = \sqrt{p\left(p-a\right)\left(p-b\right)\left(p-c\right)} "
             r"= \sqrt{%d\cdot %d\cdot %d\cdot %d} = \sqrt{%d} = %d$."
             % (a, b, c, p, p, p - a, p - b, p - c, S * S, S)),
            (r"Calculate the inradius $r$ of triangle $ABC$.", r"%d" % r,
             r"The area of the triangle can also be computed as $S = p\cdot r$, so\\ "
             r"$r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH035_SA_A_01(socau, dang=2):
    """Trả lời ngắn: giải tam giác c-g-c, tính số đo góc còn lại (làm tròn độ)."""
    gt = []
    while len(gt) < socau:
        A = random.choice([60, 120])
        b, c = random.choice([x for x in CAP_COSIN[A] if x[0] != x[1]])
        if (A, b, c) not in gt:
            gt.append((A, b, c))

    cauTN = ''
    for A, b, c in gt:
        dau = -1 if A == 60 else 1
        a2 = b * b + c * c + dau * b * c
        a = int(round(a2 ** 0.5))
        cos_B = (a * a + c * c - b * b) / (2.0 * a * c)
        gocB = math.degrees(math.acos(max(-1.0, min(1.0, cos_B))))
        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$, $\widehat{A} = %s$. "
                 r"Calculate the measure of angle $B$ (in degrees, rounded to the nearest hundredth)."
                 % (b, c, _goc(A)))
        giai = (r"The law of cosines gives $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot"
                r"\left(%s\right) = %d$, so $BC = %d$.\\ "
                r"By the law of cosines again:\\ "
                r"$\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} "
                r"= \dfrac{%d + %d - %d}{2\cdot %d\cdot %d} = %s$.\\ "
                r"Hence $\widehat{B} \approx %s^{\circ}$."
                % (b, c, b, c, _L(Rational(1, 2) if A == 60 else Rational(-1, 2)), a2, a,
                   a * a, c * c, b * b, a, c, _xx(cos_B, 4), _xx(gocB)))
        dung = _xx(gocB)
        ds = _ba_nhieu(dung, [_xx(180 - gocB - A), _xx(A), _xx(gocB + 10)],
                       buoc=lambda k: _xx(gocB + 5 * (k + 1)))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH035_TL_A_01(socau, dong=1):
    """Tự luận: giải tam giác khi biết một cạnh và hai góc kề."""
    gt = []
    while len(gt) < socau:
        A, B = random.choice([(30, 45), (45, 60), (30, 60), (60, 45), (45, 30)])
        a = random.randint(4, 15)
        if (A, B, a) not in gt:
            gt.append((A, B, a))

    cauTN = ''
    for A, B, a in gt:
        C = 180 - A - B
        sin_A = [r[1] for r in BANG_GTLG if r[0] == A][0]
        sin_B = [r[1] for r in BANG_GTLG if r[0] == B][0]
        b = simplify(a * sin_B / sin_A)
        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$."
                 % (a, _goc(A), _goc(B)))
        ds_abcd = [
            (r"Calculate the measure of angle $C$.", r"%s" % _goc(C),
             r"The sum of the three angles of a triangle equals $180^{\circ}$, so\\ "
             r"$\widehat{C} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C))),
            (r"Calculate the length of side $AC$.", _L(b),
             r"Law of sines: $\dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$, so "
             r"$AC = \dfrac{BC\cdot\sin B}{\sin A}$.\\ "
             r"$AC = \dfrac{%d\cdot %s}{%s} = %s$." % (a, _L(sin_B), _L(sin_A), _L(b))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_TF_D_01(socau, socot=1):
    """Đúng/Sai - giá trị lượng giác đọc từ toạ độ điểm trên nửa đường tròn đơn vị."""
    cauTF = ''
    for _ in range(socau):
        doi, ke, huyen = random.choice(BO_BA_THAP_PHAN)
        x0, y0 = -ke / huyen, doi / huyen          # lay diem o goc phan tu thu hai
        tan0 = y0 / x0

        debai = (r"In the coordinate plane $Oxy$, the point $M\left(x_{0}; y_{0}\right)$ lies on the unit "
                 r"semicircle, with $x_{0} = %s$ and $y_{0} = %s$. "
                 r"Determine whether each of the following statements is true or false:" % (_xx(x0), _xx(y0)))

        # a) NB - nhac lai dinh nghia
        y1 = [(r"{\True $\cos\widehat{xOM} = x_{0}$}",
               r"True. By definition, the x-coordinate of $M$ is exactly the cosine of angle $\widehat{xOM}$."),
              (r"{$\cos\widehat{xOM} = y_{0}$}",
               r"False. $y_{0}$ is the \textbf{sine}, while the cosine is $x_{0}$.")]

        # b) TH - thay so cu the
        y2 = [(r"{\True $\sin\widehat{xOM} = %s$}" % _xx(y0),
               r"The sine of the angle equals the y-coordinate of $M$, that is, $\sin\widehat{xOM} = y_{0} = %s$." % _xx(y0)),
              (r"{$\sin\widehat{xOM} = %s$}" % _xx(x0),
               r"False. That is the x-coordinate, i.e., the cosine. The sine equals $%s$." % _xx(y0))]

        # c) VD - phai lap ti so tu hai toa do
        y3 = [(r"{\True $\tan\widehat{xOM} = %s$}" % _xx(tan0),
               r"$\tan\widehat{xOM} = \dfrac{\sin\widehat{xOM}}{\cos\widehat{xOM}} "
               r"= \dfrac{y_{0}}{x_{0}} = \dfrac{%s}{%s} = %s$."
               % (_xx(y0), _xx(x0), _xx(tan0))),
              (r"{$\tan\widehat{xOM} = %s$}" % _xx(-tan0),
               r"False, because of the sign. Since $x_{0} < 0$ and $y_{0} > 0$, $\tan\widehat{xOM}$ is \textbf{negative}, "
               r"equal to $%s$." % _xx(tan0))]

        # d) VDC - diem doi xung, phai suy ra quan he hai goc bu nhau
        y4 = [(r"{\True Let $N$ be the reflection of $M$ across the $Oy$-axis. "
               r"Then $\cos\widehat{xON} + \cos\widehat{xOM} = 0$}",
               r"Since $N$ is the reflection of $M$ across $Oy$, we have $N\left(-x_{0}; y_{0}\right)$, "
               r"hence $\cos\widehat{xON} = -x_{0}$.\\ "
               r"Therefore $\cos\widehat{xON} + \cos\widehat{xOM} = -x_{0} + x_{0} = 0$ "
               r"(the angles $\widehat{xOM}$ and $\widehat{xON}$ are supplementary)."),
              (r"{Let $N$ be the reflection of $M$ across the $Oy$-axis. "
               r"Then $\sin\widehat{xON} + \sin\widehat{xOM} = 0$}",
               r"False. Two points symmetric about $Oy$ have the \textbf{same} y-coordinate, so the two sines "
               r"are \textbf{equal}, not opposite; their sum equals $2y_{0} = %s$."
               % _xx(2 * y0))]

        # --- Bổ sung 01/10/2026 (cô Lan): mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai ---
        ly1 = (r"By definition: $\sin\widehat{xOM} = y_{0}$, $\cos\widehat{xOM} = x_{0}$, $\tan\widehat{xOM} = \dfrac{y_{0}}{x_{0}}$; "
               r"$M$ lies on the unit circle, so $x_{0}^{2} + y_{0}^{2} = 1$; $x_{0} < 0$, so angle $\widehat{xOM}$ is obtuse.")
        _tf_them(y1, [(r"$\sin\widehat{xOM} = y_{0}$", ly1), (r"$\tan\widehat{xOM} = \dfrac{y_{0}}{x_{0}}$", ly1),
                      (r"$x_{0}^{2} + y_{0}^{2} = 1$", ly1), (r"Angle $\widehat{xOM}$ is obtuse", ly1)],
                 [(r"$\sin\widehat{xOM} = x_{0}$", ly1), (r"$\tan\widehat{xOM} = \dfrac{x_{0}}{y_{0}}$", ly1),
                  (r"$x_{0} + y_{0} = 1$", ly1), (r"Angle $\widehat{xOM}$ is acute", ly1)])
        ly2 = r"$\cos\widehat{xOM} = x_{0} = %s$, $\sin\widehat{xOM} = y_{0} = %s$." % (_xx(x0), _xx(y0))
        _tf_them(y2, [(r"$\cos\widehat{xOM} = %s$" % _xx(x0), ly2), (r"$\sin^{2}\widehat{xOM} = %s$" % _xx(y0 * y0, 4), ly2)],
                 [(r"$\cos\widehat{xOM} = %s$" % _xx(-x0), "Sign error. " + ly2), (r"$\sin\widehat{xOM} = %s$" % _xx(-y0), "Sign error. " + ly2),
                  (r"$\cos\widehat{xOM} = %s$" % _xx(y0), "Confused the x-coordinate with the y-coordinate. " + ly2)])
        cot0 = x0 / y0
        ly3 = (r"$\tan\widehat{xOM} = \dfrac{y_{0}}{x_{0}} \approx %s$, $\cot\widehat{xOM} = \dfrac{x_{0}}{y_{0}} \approx %s$."
               % (_xx(tan0, 4), _xx(cot0, 4)))
        _tf_them(y3, [(r"$\cot\widehat{xOM} = %s$" % _xx(cot0), ly3), (r"$\tan\widehat{xOM} < 0$", ly3)],
                 [(r"$\cot\widehat{xOM} = %s$" % _xx(tan0), "Confused $\\cot$ with $\\tan$. " + ly3), (r"$\cot\widehat{xOM} = %s$" % _xx(-cot0), "Sign error. " + ly3),
                  (r"$\tan\widehat{xOM} = %s$" % _xx(cot0), "Numerator and denominator swapped. " + ly3), (r"$\tan\widehat{xOM} > 0$", ly3)])
        ly4 = (r"Since $N$ is the reflection of $M$ across $Oy$, we have $N\left(-x_{0}; y_{0}\right)$: $\sin\widehat{xON} = \sin\widehat{xOM}$, "
               r"$\cos\widehat{xON} = -x_{0} = %s$, $\tan\widehat{xON} = -\tan\widehat{xOM}$; the angles $\widehat{xOM}$ and $\widehat{xON}$ are supplementary." % _xx(-x0))
        nd = r"Let $N$ be the reflection of $M$ across the $Oy$-axis. Then %s"
        _tf_them(y4, [(nd % r"$\sin\widehat{xON} = \sin\widehat{xOM}$", ly4), (nd % (r"$\cos\widehat{xON} = %s$" % _xx(-x0)), ly4),
                      (nd % r"$\widehat{xON} + \widehat{xOM} = 180^{\circ}$", ly4), (nd % r"$\tan\widehat{xON} + \tan\widehat{xOM} = 0$", ly4)],
                 [(nd % (r"$\cos\widehat{xON} = %s$" % _xx(x0)), ly4), (nd % r"$\tan\widehat{xON} = \tan\widehat{xOM}$", ly4),
                  (nd % r"$\widehat{xON} = \widehat{xOM}$", ly4), (nd % r"$\widehat{xON} + \widehat{xOM} = 90^{\circ}$", ly4)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_E_01(socau, socot=1):
    """Đúng/Sai - định lí sin, công thức diện tích và quan hệ giữa chúng."""
    cauTF = ''
    for _ in range(socau):
        a, b, c, S, p, r = random.choice([t for t in BANG_HERON if t[3] >= 20])
        R = Rational(a * b * c, 4 * S)

        debai = (r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Let $S$, $p$, $R$, $r$ denote, respectively, the area, the semiperimeter, the circumradius "
                 r"and the inradius of the triangle. "
                 r"Determine whether each of the following statements is true or false:" % (a, b, c))

        # a) NB - nhac lai cong thuc
        y1 = [(r"{\True $S = p\cdot r$}",
               r"True. This is one of the formulas for the area of a triangle."),
              (r"{$S = 2p\cdot r$}",
               r"False. The correct formula is $S = p\cdot r$, with no factor of $2$.")]

        # b) TH - thay so vao cong thuc Heron
        y2 = [(r"{\True $p = %d$ and $S = %d$}" % (p, S),
               r"$p = \dfrac{%d + %d + %d}{2} = %d$; Heron gives "
               r"$S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
               % (a, b, c, p, p, p - a, p - b, p - c, S)),
              (r"{$p = %d$ and $S = %d$}" % (p, S + 2),
               r"False. Heron's formula gives $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$, not $%d$."
               % (p, p - a, p - b, p - c, S, S + 2))]

        # c) VD - phai co S cua y b) moi tinh duoc r
        y3 = [(r"{\True $r = %d$}" % r,
               r"From $S = p\cdot r$ we get $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r)),
              (r"{$r = %s$}" % _L(simplify(Rational(S, p) + 1)),
               r"False. $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r))]

        # d) VDC - noi hai cong thuc dien tich khac nhau lai voi nhau
        y4 = [(r"{\True $R = %s$}" % _L(R),
               r"The area of the triangle can also be computed as $S = \dfrac{abc}{4R}$, "
               r"so $R = \dfrac{abc}{4S}$.\\ "
               r"$R = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$."
               % (a, b, c, S, _L(R))),
              (r"{$R = %s$}" % _L(simplify(R * 2)),
               r"False. From $S = \dfrac{abc}{4R}$ we get $R = \dfrac{abc}{4S} = %s$." % _L(R))]

        # --- Bổ sung 01/10/2026 (cô Lan): mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai ---
        ly1 = r"Area formulas for a triangle: $S = pr = \dfrac{abc}{4R} = \dfrac{1}{2}a\cdot h_a = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$."
        _tf_them(y1, [(r"$S = \dfrac{abc}{4R}$", ly1), (r"$S = \dfrac{1}{2}BC\cdot h_a$", ly1),
                      (r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$", ly1)],
                 [(r"$S = \dfrac{abc}{2R}$", ly1), (r"$S = BC\cdot h_a$", ly1), (r"$S = \dfrac{r}{p}$", ly1),
                  (r"$S = \sqrt{\left(p - a\right)\left(p - b\right)\left(p - c\right)}$", ly1)])
        ly2 = (r"$p = \dfrac{%d + %d + %d}{2} = %d$; Heron gives $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
               % (a, b, c, p, p, p - a, p - b, p - c, S))
        _tf_them(y2, [(r"$p = %d$" % p, ly2), (r"$S = %d$" % S, ly2), (r"The perimeter of triangle $ABC$ equals $%d$" % (2 * p), ly2)],
                 [(r"$p = %d$" % (2 * p), "That is the perimeter. " + ly2), (r"$S = %d$" % (2 * S), ly2),
                  (r"The perimeter of triangle $ABC$ equals $%d$" % p, "That is the semiperimeter. " + ly2)])
        ly3 = r"From $S = p\cdot r$ we get $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r)
        d_, s_ = _tf_ct(r"$r = %s$", Integer(r), ly3, [(Rational(S, 2 * p), "Divided by the perimeter"), (Rational(2 * S, p), "Mistakenly used $S = \\dfrac{1}{2}pr$"), (R, "Confused with $R$")])
        _tf_them(y3, d_, s_)
        ly4 = r"$S = \dfrac{abc}{4R}$, so $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$." % (a, b, c, S, _L(R))
        d_, s_ = _tf_ct(r"$R = %s$", R, ly4, [(simplify(4 * R), "Forgot to divide by 4"), (Integer(r), "Confused with $r$"), (simplify(R / 2), "Divided by an extra factor of 2")],
                        them=[r"$2R = %s$" % _L(simplify(2 * R))])
        _tf_them(y4, d_, s_)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


# ==========================================================
# Ba dạng NHẬN BIẾT bổ sung cho yêu cầu L10_C3_B5_NB029
# (giá trị lượng giác của một góc từ 0 độ đến 180 độ).
#
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
# Ba dạng này theo đúng ba ví dụ cô Lan đưa ra:
#   MC_E  xét dấu giá trị lượng giác khi biết khoảng của góc
#   MC_F  đọc sin/cos/tan/cot theo toạ độ điểm M TRÊN HÌNH VẼ
#   MC_G  biết dấu một giá trị lượng giác, suy ra khoảng của góc
# ==========================================================

# Bảng dấu trên nửa đường tròn đơn vị, dùng chung cho MC_E.
#   0  < alpha < 90 : M nằm bên phải Oy nên x_M > 0, y_M > 0
#   90 < alpha < 180: M nằm bên trái  Oy nên x_M < 0, y_M > 0
DAU_GTLG = {
    "nhon": {r"\sin": 1, r"\cos": 1, r"\tan": 1, r"\cot": 1},
    "tu":   {r"\sin": 1, r"\cos": -1, r"\tan": -1, r"\cot": -1},
}

MO_TA_KHOANG = {
    "nhon": r"$0^{\circ} < \alpha < 90^{\circ}$",
    "tu": r"$90^{\circ} < \alpha < 180^{\circ}$",
}

LY_DO_KHOANG = {
    "nhon": (r"For $0^{\circ} < \alpha < 90^{\circ}$, the point $M$ lies on the part of "
             r"the unit semicircle \textbf{to the right of} the $Oy$ axis, so "
             r"$x_M > 0$ and $y_M > 0$."),
    "tu": (r"For $90^{\circ} < \alpha < 180^{\circ}$, the point $M$ lies on the part of "
           r"the unit semicircle \textbf{to the left of} the $Oy$ axis, so "
           r"$x_M < 0$ while $y_M > 0$."),
}


def _hinh_nua_duong_tron(goc, ten_diem="M", ve_hinh_chieu=True):
    r"""Nửa đường tròn đơn vị, góc $\alpha$ và điểm $M$ trên đó.

    Có vẽ hình chiếu của $M$ xuống hai trục để học sinh ĐỌC ĐƯỢC
    $x_M$, $y_M$ ngay trên hình - đây chính là chỗ làm câu hỏi nhẹ đi
    một mức so với việc chỉ cho toạ độ bằng chữ.
    """
    chieu = ""
    if ve_hinh_chieu:
        chieu = (
            "\\draw[dashed] (M) -- ({cos(%d)*1.6},0) node[below]"
              "{\\footnotesize $x_M$};\n" % goc
            + "\\draw[dashed] (M) -- (0,{sin(%d)*1.6}) node[left]"
              "{\\footnotesize $y_M$};\n" % goc
        )
    return (
        "\\begin{tikzpicture}[>=stealth,x=1.0cm,y=1.0cm,thick,scale=1.2]\n"
        "\\def\\r{1.6}\n"
        "\\draw[->] (-\\r - 0.6,0) -- (\\r + 0.6,0) node[below] {$x$};\n"
        "\\draw[->] (0,-0.5) -- (0,\\r + 0.6) node[left] {$y$};\n"
        "\\draw (\\r,0) arc (0:180:\\r);\n"
        "\\fill[black] (\\r,0) circle[radius=1.2pt] node[below right]"
        "{\\footnotesize $1$};\n"
        "\\fill[black] (-\\r,0) circle[radius=1.2pt] node[below left]"
        "{\\footnotesize $-1$};\n"
        "\\coordinate (M) at (%d:\\r);\n" % goc
        + "\\draw (0,0) -- (M);\n"
        "\\draw[->] (0.45,0) arc (0:%d:0.45);\n" % goc
        + "\\node at (%d:0.68) {\\footnotesize $\\alpha$};\n" % (goc // 2)
        + chieu
        + "\\fill[black] (M) circle[radius=1.5pt] node[above right]"
          "{\\footnotesize $%s$};\n" % ten_diem
        + "\\fill[black] (0,0) circle[radius=1.0pt] node[below left]"
          "{\\footnotesize $O$};\n"
        "\\end{tikzpicture}"
    )


def _hinh_nua_duong_tron_hai_phia():
    r"""Nửa đường tròn đơn vị với HAI vị trí mẫu của điểm $M$.

    Dùng cho dạng MC_G. Không được vẽ đúng MỘT góc ở đây: đề cho dấu của
    một giá trị lượng giác rồi hỏi góc nằm trong khoảng nào, nên nếu hình
    vẽ sẵn góc thoả mãn giả thiết thì học sinh đọc thẳng đáp án trên hình,
    câu hỏi mất hết ý nghĩa. Vẽ hai vị trí - một bên phải, một bên trái
    trục $Oy$ - để học sinh thấy được dấu của hoành độ đổi ra sao mà vẫn
    phải tự chọn khoảng.
    """
    return (
        "\\begin{tikzpicture}[>=stealth,x=1.0cm,y=1.0cm,thick,scale=1.2]\n"
        "\\def\\r{1.6}\n"
        "\\draw[->] (-\\r - 0.6,0) -- (\\r + 0.6,0) node[below] {$x$};\n"
        "\\draw[->] (0,-0.5) -- (0,\\r + 0.7) node[left] {$y$};\n"
        "\\draw (\\r,0) arc (0:180:\\r);\n"
        "\\fill[black] (\\r,0) circle[radius=1.2pt] node[below right]"
        "{\\footnotesize $1$};\n"
        "\\fill[black] (-\\r,0) circle[radius=1.2pt] node[below left]"
        "{\\footnotesize $-1$};\n"
        "\\coordinate (M) at (55:\\r);\n"
        "\\coordinate (N) at (130:\\r);\n"
        "\\draw (0,0) -- (M);\n"
        "\\draw (0,0) -- (N);\n"
        "\\draw[dashed] (M) -- ({cos(55)*1.6},0);\n"
        "\\draw[dashed] (N) -- ({cos(130)*1.6},0);\n"
        "\\fill[black] (M) circle[radius=1.5pt] node[above right]"
        "{\\footnotesize $M_1$};\n"
        "\\fill[black] (N) circle[radius=1.5pt] node[above left]"
        "{\\footnotesize $M_2$};\n"
        "\\node[below] at ({cos(55)*1.6},0) {\\footnotesize $x_{M_1}$};\n"
        "\\node[below] at ({cos(130)*1.6},0) {\\footnotesize $x_{M_2}$};\n"
        "\\fill[black] (0,0) circle[radius=1.0pt] node[below left]"
        "{\\footnotesize $O$};\n"
        "\\end{tikzpicture}"
    )


def L10_C3_B5_NB029_MC_E_01(socau, dang=1):
    r"""Xét dấu giá trị lượng giác khi đã biết khoảng của góc.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Mỗi phương án là một khẳng định dạng "$\sin\alpha > 0$". Đáp án đúng
    lấy từ bảng dấu, ba phương án nhiễu lấy từ các khẳng định SAI của
    chính khoảng góc ấy - luôn có đúng 4 khẳng định sai nên không bao giờ
    thiếu nhiễu, và không bao giờ có hai đáp án đúng.
    """
    def _viet(ten, dau):
        return r"$%s\alpha %s 0$" % (ten, ">" if dau > 0 else "<")

    gt = []
    while len(gt) < socau:
        khoang = random.choice(["nhon", "tu"])
        ten_dung = random.choice(list(DAU_GTLG[khoang].keys()))
        v = (khoang, ten_dung)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for khoang, ten_dung in gt:
        bang = DAU_GTLG[khoang]
        dung = _viet(ten_dung, bang[ten_dung])
        # mọi khẳng định SAI của khoảng này
        sai = [_viet(ten, -dau) for ten, dau in bang.items()]

        debai = (r"Given an angle $\alpha$ satisfying %s. Which of the following statements "
                 r"is \textbf{true}?" % MO_TA_KHOANG[khoang])

        dau_chu = "positive" if bang[ten_dung] > 0 else "negative"
        if ten_dung == r"\sin":
            cach = r"$\sin\alpha = y_M$"
        elif ten_dung == r"\cos":
            cach = r"$\cos\alpha = x_M$"
        elif ten_dung == r"\tan":
            cach = r"$\tan\alpha = \dfrac{y_M}{x_M}$"
        else:
            cach = r"$\cot\alpha = \dfrac{x_M}{y_M}$"

        giai = (LY_DO_KHOANG[khoang] + "\\\\\n"
                + r"Since %s, $%s\alpha$ is %s, that is, %s."
                % (cach, ten_dung, dau_chu, dung))

        cauTN += MC_SA_answer_text(debai, dung, sai, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_NB029_MC_F_01(socau, dang=1):
    r"""Đọc sin/cos/tan/cot theo toạ độ điểm $M$ TRÊN HÌNH VẼ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Khác dạng MC_B ở chỗ MC_B cho toạ độ bằng số, còn dạng này cho HÌNH
    và hỏi công thức theo $x_M$, $y_M$ - đúng ví dụ cô Lan nêu
    ("hỏi về toạ độ $x_M$, $y_M$, $x_M/y_M$... là sin, cos, tan, cot").
    """
    CT = {
        r"\sin": r"$\sin\alpha = y_M$",
        r"\cos": r"$\cos\alpha = x_M$",
        r"\tan": r"$\tan\alpha = \dfrac{y_M}{x_M}$",
        r"\cot": r"$\cot\alpha = \dfrac{x_M}{y_M}$",
    }
    # các khẳng định SAI: đổi chỗ hoành độ với tung độ
    SAI = {
        r"\sin": r"$\sin\alpha = x_M$",
        r"\cos": r"$\cos\alpha = y_M$",
        r"\tan": r"$\tan\alpha = \dfrac{x_M}{y_M}$",
        r"\cot": r"$\cot\alpha = \dfrac{y_M}{x_M}$",
    }

    gt = []
    while len(gt) < socau:
        # tránh 40-50 độ để trên hình thấy rõ x_M khác y_M
        # Không lấy góc lớn hơn 60 độ: khi đó $y_M$ nằm cao, nhãn của nó
        # chạm vào cung tròn, hình nhìn rối.
        v = (random.choice([25, 30, 35, 40, 55, 60]),
             random.choice(list(CT.keys())))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for goc, ten in gt:
        debai = (r"Given an angle $\alpha$ with $0^{\circ} < \alpha < 90^{\circ}$ and "
                 r"a point $M$ on the unit semicircle as shown in the figure, "
                 r"where $x_M$ and $y_M$ are, respectively, the x-coordinate and the y-coordinate "
                 r"of $M$. Which of the following statements is \textbf{true}?")

        giai = (r"By the definition of the trigonometric values of an angle $\alpha$ with "
                r"$0^{\circ} \le \alpha \le 180^{\circ}$, if $M(x_M; y_M)$ "
                r"is the point on the unit semicircle corresponding to the angle $\alpha$, then"
                "\\\\\n"
                r"$\sin\alpha = y_M$, \quad $\cos\alpha = x_M$, \quad "
                r"$\tan\alpha = \dfrac{y_M}{x_M}$ \ $(\alpha \ne 90^{\circ})$, "
                r"\quad $\cot\alpha = \dfrac{x_M}{y_M}$ \ "
                r"$(\alpha \ne 0^{\circ},\ \alpha \ne 180^{\circ})$."
                "\\\\\n"
                r"Hence the true statement is %s." % CT[ten])

        nhieu = [SAI[t] for t in CT if t != ten] + [SAI[ten]]
        hinh = _hinh_nua_duong_tron(goc)
        cauTN += MC_SA_answer_text(debai, CT[ten], nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C3_B5_NB029_MC_G_01(socau, dang=1):
    r"""Biết dấu một giá trị lượng giác, suy ra khoảng của góc.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đây là chiều NGƯỢC của dạng MC_E, đúng ví dụ cô Lan nêu
    ("với $\cos > 0$ thì góc từ đâu đến đâu").

    Các khoảng ghi ở đây là khoảng ĐÚNG BẰNG tập nghiệm, đã xét cả hai
    đầu mút: $\cos 180^{\circ} = -1 < 0$ nên lấy $\alpha \le 180^{\circ}$,
    còn $\tan 180^{\circ} = 0$ nên KHÔNG lấy $\alpha = 180^{\circ}$.
    """
    TRUONG_HOP = [
        (r"\cos\alpha > 0", r"$0^{\circ} \le \alpha < 90^{\circ}$",
         [r"$90^{\circ} < \alpha \le 180^{\circ}$",
          r"$90^{\circ} \le \alpha \le 180^{\circ}$",
          r"$0^{\circ} < \alpha \le 90^{\circ}$",
          r"$\alpha = 90^{\circ}$"],
         r"$\cos\alpha = x_M$, so $\cos\alpha > 0$ if and only if $x_M > 0$, "
         r"that is, $M$ lies to the right of the $Oy$ axis."),
        (r"\cos\alpha < 0", r"$90^{\circ} < \alpha \le 180^{\circ}$",
         [r"$0^{\circ} \le \alpha < 90^{\circ}$",
          r"$0^{\circ} < \alpha < 90^{\circ}$",
          r"$0^{\circ} \le \alpha \le 90^{\circ}$",
          r"$\alpha = 90^{\circ}$"],
         r"$\cos\alpha = x_M$, so $\cos\alpha < 0$ if and only if $x_M < 0$, "
         r"that is, $M$ lies to the left of the $Oy$ axis. Note that $\cos 180^{\circ} = -1 < 0$ "
         r"so $\alpha = 180^{\circ}$ still satisfies the condition."),
        (r"\tan\alpha > 0", r"$0^{\circ} < \alpha < 90^{\circ}$",
         [r"$90^{\circ} < \alpha < 180^{\circ}$",
          r"$0^{\circ} \le \alpha < 90^{\circ}$",
          r"$90^{\circ} < \alpha \le 180^{\circ}$",
          r"$0^{\circ} < \alpha \le 90^{\circ}$"],
         r"$\tan\alpha = \dfrac{y_M}{x_M}$ with $y_M > 0$, so $\tan\alpha > 0$ "
         r"if and only if $x_M > 0$. Note that $\tan 0^{\circ} = 0$, so we exclude "
         r"$\alpha = 0^{\circ}$, and $\tan 90^{\circ}$ is undefined."),
        (r"\tan\alpha < 0", r"$90^{\circ} < \alpha < 180^{\circ}$",
         [r"$0^{\circ} < \alpha < 90^{\circ}$",
          r"$90^{\circ} \le \alpha \le 180^{\circ}$",
          r"$90^{\circ} < \alpha \le 180^{\circ}$",
          r"$0^{\circ} \le \alpha < 90^{\circ}$"],
         r"$\tan\alpha = \dfrac{y_M}{x_M}$ with $y_M > 0$, so $\tan\alpha < 0$ "
         r"if and only if $x_M < 0$. Note that $\tan 180^{\circ} = 0$, so we exclude "
         r"$\alpha = 180^{\circ}$."),
    ]

    gt = []
    while len(gt) < socau:
        v = random.randrange(len(TRUONG_HOP))
        if v not in gt:
            gt.append(v)
        if len(gt) >= len(TRUONG_HOP):
            break

    cauTN = ""
    for chi_so in gt:
        gia_thiet, dung, nhieu, ly_do = TRUONG_HOP[chi_so]
        debai = (r"Given an angle $\alpha$ with $0^{\circ} \le \alpha \le 180^{\circ}$ "
                 r"and $M$ the point on the unit semicircle corresponding to the angle "
                 r"$\alpha$. The figure shows the two possible positions of $M$, namely $M_1$ and $M_2$. "
                 r"Given that $%s$. Which of the following statements is \textbf{true}?"
                 % gia_thiet)
        giai = ly_do + "\\\\\n" + r"Hence %s." % dung
        hinh = _hinh_nua_duong_tron_hai_phia()
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


# =====================================================================
# Ba dạng VẬN DỤNG bổ sung cho yêu cầu L10_C3_B6_VD036
# (vận dụng hệ thức lượng để giải bài toán có nội dung thực tiễn).
#
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
#
# RÀNG BUỘC đã bám theo: chỉ dùng kiến thức nằm trong chương 3 lớp 10 -
# định lí sin, định lí côsin, công thức diện tích, và tỉ số lượng giác
# trong tam giác vuông (lớp 9). KHÔNG dùng công thức cộng, công thức
# nhân đôi, độ dài cung tròn - đó là chương trình lớp 11.
# =====================================================================


def L10_C3_B6_VD036_MC_D_01(socau, dang=1):
    r"""Đo chiều cao vật cao (núi, toà nhà, cây) bằng HAI GÓC NÂNG bất kì.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Khác dạng TL_A ở chỗ TL_A dùng cặp góc đặc biệt $30^{\circ}$ và
    $60^{\circ}$ nên tam giác cân, ra kết quả căn thức đẹp. Dạng này dùng
    góc BẤT KÌ nên phải đi đúng đường định lí sin:

        tam giác $ABD$ có $\widehat{DAB} = \alpha$,
        $\widehat{DBA} = 180^{\circ} - \beta$ nên
        $\widehat{ADB} = \beta - \alpha$;
        định lí sin cho $BD = \dfrac{a\sin\alpha}{\sin(\beta - \alpha)}$;
        tam giác $BDH$ vuông tại $H$ cho
        $h = BD\sin\beta = \dfrac{a\sin\alpha\sin\beta}{\sin(\beta-\alpha)}$.

    Cả hai bước đều nằm trong chương 3 lớp 10.
    """
    BOI_CANH = [
        ("a mountain", "the foot of the mountain", "the summit of the mountain"),
        ("a high-rise building", "the base of the building", "the top of the building"),
        ("an old tree", "the base of the tree", "the top of the tree"),
        ("a lighthouse", "the base of the lighthouse", "the top of the lighthouse"),
    ]

    gt = []
    thu = 0
    while len(gt) < socau and thu < 200:
        thu += 1
        alpha = random.choice([25, 30, 32, 35, 38, 40])
        beta = alpha + random.choice([10, 12, 15, 18, 20])
        a = random.choice([40, 50, 60, 80, 100, 120])
        if beta >= 75:
            continue
        v = (alpha, beta, a, random.randrange(len(BOI_CANH)))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for alpha, beta, a, i_bc in gt:
        vat, chan, dinh = BOI_CANH[i_bc]
        ra = math.radians(alpha)
        rb = math.radians(beta)
        hieu = math.sin(math.radians(beta - alpha))

        # GIỮ ĐÚNG MỘT chữ số thập phân cho MỌI phương án: đề yêu cầu làm
        # tròn đến hàng phần mười, nếu để _xx cắt đuôi số 0 thì có phương
        # án ra số nguyên, học sinh nhìn dạng số cũng đoán được đáp án.
        def _mot_le(x):
            return "$%s\\,\\text{m}$" % ("%.1f" % float(x)).replace(".", DAU_THAP_PHAN)

        h = a * math.sin(ra) * math.sin(rb) / hieu
        dapso = _mot_le(h)

        # Các phương án nhiễu là LỖI THẬT của học sinh:
        ung_vien = [
            # dừng lại ở BD, quên bước tam giác vuông
            a * math.sin(ra) / hieu,
            # nhầm góc ADB thành beta + alpha
            a * math.sin(ra) * math.sin(rb) / math.sin(math.radians(beta + alpha)),
            # dùng côsin thay vì sin ở hai góc nâng
            a * math.cos(ra) * math.cos(rb) / hieu,
            # nhân sin alpha hai lần
            a * math.sin(ra) * math.sin(ra) / hieu,
        ]
        nhieu = []
        for x in ung_vien:
            s = _mot_le(x)
            if s != dapso and s not in nhieu:
                nhieu.append(s)
        if len(nhieu) < 3:
            continue

        debai = (r"To measure the height $DH$ of %s without being able to reach %s, "
                 r"two points $A$ and $B$ are chosen on the ground on a straight line "
                 r"through $H$ (point $B$ lies between $A$ and $H$) with "
                 r"$AB = %d\,\text{m}$. From $A$, looking up at %s, the angle of elevation is "
                 r"$%d^{\circ}$; from $B$, looking up at %s, the angle of elevation is $%d^{\circ}$. "
                 r"Which of the following values is closest to the height $DH$ "
                 r"(rounded to the nearest tenth)?"
                 % (vat, chan, a, dinh, alpha, dinh, beta))

        giai = (r"In triangle $ABD$: $\widehat{DAB} = %d^{\circ}$, and "
                r"$\widehat{DBA} = 180^{\circ} - %d^{\circ}$ (it forms a linear pair with "
                r"the angle of elevation at $B$), so"
                "\\\\\n"
                r"$\widehat{ADB} = 180^{\circ} - %d^{\circ} - "
                r"\left(180^{\circ} - %d^{\circ}\right) = %d^{\circ}$."
                "\\\\\n"
                r"Applying the law of sines in triangle $ABD$:"
                "\\\\\n"
                r"$\dfrac{BD}{\sin\widehat{DAB}} = "
                r"\dfrac{AB}{\sin\widehat{ADB}} \Rightarrow "
                r"BD = \dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} "
                r"\approx %s\,\text{(m)}$."
                "\\\\\n"
                r"Triangle $BDH$ is right-angled at $H$ and $\widehat{DBH} = %d^{\circ}$, so"
                "\\\\\n"
                r"$DH = BD\cdot\sin %d^{\circ} \approx %s\,\text{(m)}$."
                % (alpha, beta, alpha, beta, beta - alpha,
                   a, alpha, beta - alpha, _xx(a * math.sin(ra) / hieu, 2),
                   beta, beta, _xx(h, 1)))

        cauTN += MC_SA_answer_text(debai, dapso, nhieu, giai, 0, 0, dang)
    return cauTN


def _hinh_trai_dat():
    """Hình minh hoạ (KHÔNG đúng tỉ lệ - góc hạ thật chỉ khoảng 1-2 độ): Trái Đất tâm O, núi
    tại M, tia nhìn MT tiếp xúc mặt biển tại T, góc hạ theta so với phương nằm ngang tại M
    (cô Lan 01/10/2026: không có hình học sinh rất khó làm bài)."""
    R, h = 2.0, 0.7
    goc_T = math.degrees(math.acos(R / (R + h)))      # góc TOM
    Tx, Ty = R * math.sin(math.radians(goc_T)), R * math.cos(math.radians(goc_T))
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
        "\\fill[blue!8] (0,0) circle (%.2f);\n\\draw[thick] (0,0) circle (%.2f);\n" % (R, R)
        + "\\fill[brown!60] (-0.25,%.2f) -- (0,%.2f) -- (0.25,%.2f) -- cycle;\n" % (R - 0.02, R + h, R - 0.02)
        + "\\draw[dashed] (0,0) -- (0,%.2f);\n" % (R + h)
        + "\\draw (0,0) -- (%.3f,%.3f);\n" % (Tx, Ty)
        + "\\draw[thick,red] (0,%.2f) -- (%.3f,%.3f);\n" % (
            R + h, Tx + 0.35 * Tx / math.hypot(Tx, R + h - Ty), Ty - 0.35 * (R + h - Ty) / math.hypot(Tx, R + h - Ty))
        + "\\draw[dashed] (-1.2,%.2f) -- (2.4,%.2f);\n" % (R + h, R + h)
        + "\\draw (0.9,%.2f) arc (0:%.1f:0.9);\n" % (R + h, -(90 - goc_T))
        + "\\node at (%.2f,%.2f) {$\\theta$};\n" % (1.15, R + h - 0.25)
        + "\\fill (0,0) circle (0.03) node[below] {$O$};\n"
        "\\fill (0,%.2f) circle (0.03) node[above] {$M$};\n" % (R + h)
        + "\\fill (%.3f,%.3f) circle (0.03) node[right] {$T$};\n" % (Tx, Ty)
        + "\\node[left] at (0,%.2f) {$h$};\n" % (R + h / 2)
        + "\\node[left] at (0,%.2f) {$R$};\n" % (R / 2)
        + "\\node[below right] at (%.3f,%.3f) {$R$};\n" % (Tx / 2, Ty / 2)
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_TL_E_01(socau, dong=1):
    r"""Đo bán kính Trái Đất bằng góc hạ tới đường chân trời.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    CHÚ Ý VỀ PHƯƠNG PHÁP (cô Lan dặn: không dùng kiến thức lớp 11).
    Cách đo bán kính Trái Đất quen thuộc nhất - cách của Eratosthenes -
    dùng ĐỘ DÀI CUNG TRÒN $\ell = R\alpha$ với $\alpha$ tính bằng radian.
    Đó là chương trình LỚP 11 nên KHÔNG dùng ở đây.

    Cách dùng trong dạng này chỉ cần tam giác vuông: từ đỉnh núi $M$ cao
    $h$, tia nhìn tới đường chân trời tiếp xúc mặt đất tại $T$ nên
    $OT \perp MT$. Tam giác $OTM$ vuông tại $T$, gọi $\theta$ là góc hạ
    của tia nhìn so với phương nằm ngang thì $\widehat{OMT} =
    90^{\circ} - \theta$, do đó $\cos\theta = \dfrac{R}{R+h}$ và
    $R = \dfrac{h\cos\theta}{1 - \cos\theta}$.

    VÌ SAO LÀ TỰ LUẬN CHỨ KHÔNG PHẢI TRẮC NGHIỆM: vì $\cos\theta$ rất
    gần $1$ nên $\dfrac{h\cos\theta}{1-\cos\theta}$ và $\dfrac{h}{1-\cos\theta}$
    cho kết quả lệch nhau chưa tới $1\,\text{km}$ - phương án nhiễu
    "quên nhân $\cos\theta$" hoá ra CŨNG ĐÚNG, câu hỏi có hai đáp án.
    Mọi biến thể sai khác thì lại lệch hẳn về cỡ $h$, nhìn là loại được
    ngay. Nói cách khác bài này không có bộ phương án nhiễu tử tế. Để tự
    luận thì học sinh phải lập được hệ thức, đúng chỗ cần đánh giá.
    """
    NUI = [("Fansipan", 3.1), ("Ngoc Linh", 2.6), ("Ba Den", 1.0),
           ("Tay Con Linh", 2.4), ("Pu Ta Leng", 3.0)]

    gt = []
    thu = 0
    while len(gt) < socau and thu < 200:
        thu += 1
        i = random.randrange(len(NUI))
        # chọn theta từ bán kính thật 6371 km rồi làm tròn hai chữ số,
        # để số liệu đề bài là con số đo được hợp lí
        h = NUI[i][1]
        theta = round(math.degrees(math.acos(6371.0 / (6371.0 + h))), 2)
        if (i, theta) not in gt:
            gt.append((i, theta))

    cauTN = ''
    for i, theta in gt:
        ten, h = NUI[i]
        c = math.cos(math.radians(theta))
        R = h * c / (1 - c)

        debai = (r"Standing on the summit of Mount %s, at an elevation of $h = %s\,\text{km}$ above "
                 r"sea level, a person looks toward the sea and sees the "
                 r"horizon. The line of sight to the horizon makes with the horizontal "
                 r"an angle of depression $\theta = %s^{\circ}$. Treat the Earth as "
                 r"a sphere with center $O$ and radius $R$; let $M$ be the position of the "
                 r"observer and $T$ the point where the line of sight touches the sea surface (illustration, "
                 r"not to scale)."
                 % (ten, _xx(h, 1), _xx(theta, 2)))

        hoi_a = (r"Show that triangle $OTM$ is right-angled at $T$ and calculate "
                 r"$\widehat{OMT}$ in terms of $\theta$.")
        giai_a = (r"The line of sight touches the sea exactly at the horizon, so $MT$ "
                  r"is tangent to the circle with center $O$ at $T$, hence "
                  r"$OT \perp MT$: triangle $OTM$ is right-angled at $T$."
                  "\\\\\n"
                  r"The horizontal line at $M$ is perpendicular to the radius $OM$. "
                  r"The line of sight $MT$ points below that line by an angle $\theta$, "
                  r"so the angle between $MT$ and $MO$ is"
                  "\\\\\n"
                  r"$\widehat{OMT} = 90^{\circ} - \theta = %s^{\circ}$."
                  % _xx(90 - theta, 2))

        hoi_b = r"Prove that $\cos\theta = \dfrac{R}{R + h}$."
        giai_b = (r"Triangle $OTM$ is right-angled at $T$, with $OT = R$ the side opposite "
                  r"angle $\widehat{OMT}$ and $OM = R + h$ the hypotenuse, so"
                  "\\\\\n"
                  r"$\sin\widehat{OMT} = \dfrac{OT}{OM} = \dfrac{R}{R + h}$."
                  "\\\\\n"
                  r"Also $\widehat{OMT} = 90^{\circ} - \theta$, and for two complementary "
                  r"angles the sine of one equals the cosine of the other, so "
                  r"$\sin\left(90^{\circ} - \theta\right) = \cos\theta$."
                  "\\\\\n"
                  r"Hence $\cos\theta = \dfrac{R}{R + h}$.")

        hoi_c = (r"From this, calculate the radius $R$ of the Earth (rounded to the nearest "
                 r"whole number, in kilometers).")
        giai_c = (r"From $\cos\theta = \dfrac{R}{R+h}$ we get "
                  r"$\left(R + h\right)\cos\theta = R$, that is,"
                  "\\\\\n"
                  r"$R\left(1 - \cos\theta\right) = h\cos\theta "
                  r"\Rightarrow R = \dfrac{h\cos\theta}{1 - \cos\theta}$."
                  "\\\\\n"
                  r"Substituting $h = %s\,\text{km}$ and $\theta = %s^{\circ}$:"
                  "\\\\\n"
                  r"$R = \dfrac{%s\cdot\cos %s^{\circ}}{1 - \cos %s^{\circ}} "
                  r"\approx %s\,\text{(km)}$."
                  "\\\\\n"
                  r"This result is close to the commonly used Earth radius of "
                  r"$6371\,\text{km}$. Note that $1 - \cos\theta$ is a very "
                  r"small number, so when using a calculator you must keep enough decimal places; "
                  r"rounding too early will give a result that is far off."
                  % (_xx(h, 1), _xx(theta, 2), _xx(h, 1),
                     _xx(theta, 2), _xx(theta, 2), _xx(R, 0)))

        ds_abcd = [(hoi_a, r"90^{\circ} - \theta", giai_a),
                   (hoi_b, r"\cos\theta = \dfrac{R}{R + h}", giai_b),
                   (hoi_c, r"R \approx %s\,\text{km}" % _xx(R, 0), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, _hinh_trai_dat(), 0, dong)
    return cauTN


# ---- Bán kính Trái Đất / đường chân trời: MC + SA tách VD và VDC ----
# CLAUDE THEM 01/10/2026 - co Lan duyet cach hoi (VD: cho R, tinh goc ha / khoang cach
# toi chan troi; VDC: cho h va goc ha, tinh R). Cung mo ta "Dang" voi TL_E de khong ra
# chung mot de. Do cao lay xap xi so lieu thuc te (km).
_NUI_CHAN_TROI = [("Fansipan", 3.14), ("Pu Si Lung", 3.08), ("Pu Ta Leng", 3.05),
                  ("Ngoc Linh", 2.6), ("Chu Yang Sin", 2.44), ("Tay Con Linh", 2.42),
                  ("Lang Biang", 2.17), ("Mau Son", 1.54), ("Bach Ma", 1.45), ("Ba Den", 0.99)]
_R_TRAI_DAT = 6371


def _chon_nui(socau):
    """Chọn socau ngọn núi, không lặp khi còn đủ núi."""
    ds = random.sample(range(len(_NUI_CHAN_TROI)), min(socau, len(_NUI_CHAN_TROI)))
    while len(ds) < socau:
        ds.append(random.randrange(len(_NUI_CHAN_TROI)))
    return [_NUI_CHAN_TROI[i] for i in ds]


def _mo_dau_chan_troi(ten, h):
    return (r"Standing on the summit of Mount %s at an elevation of $h = %s\,\text{km}$ above sea level, a person "
            r"looks toward the sea and sees the horizon. Treat the Earth as a sphere with center $O$ and radius "
            r"$R$; let $M$ be the position of the observer and $T$ the point where the line of sight touches the sea surface, "
            r"and let $\theta$ be the angle of depression of the line of sight $MT$ below the horizontal (illustration, "
            r"not to scale)." % (ten, _xx(h, 2)))


_GIAI_VUONG_T = (r"The line of sight touches the sea exactly at the horizon, so $MT$ is tangent to the "
                 r"circle with center $O$ at $T$; hence triangle $OTM$ is right-angled at $T$, with "
                 r"$OT = R$, $OM = R + h$.")


def L10_C3_B6_VD036_MC_K_01(socau, dang=1):
    r"""Đường chân trời (mức VD): biết $R = 6371\,\text{km}$ và độ cao $h$, tính góc hạ $\theta$.

    Phương nằm ngang tại $M$ vuông góc với $OM$ nên $\widehat{OMT} = 90^{\circ} - \theta$,
    suy ra $\widehat{TOM} = \theta$ và $\cos\theta = \dfrac{R}{R + h}$.
    Nhiễu: $90^{\circ} - \theta$ (nhầm với $\widehat{OMT}$), $\tan\theta = \dfrac{h}{R}$,
    $\cos\theta = \dfrac{h}{R + h}$.

    CLAUDE THEM 01/10/2026 - co Lan duyet lai.
    """
    R = _R_TRAI_DAT
    cau = ""
    for ten, h in _chon_nui(socau):
        t = math.degrees(math.acos(R / (R + h)))
        dap = _xx(t, 2) + r"^{\circ}"
        ung = [_xx(90 - t, 2) + r"^{\circ}",
               _xx(math.degrees(math.atan(h / R)), 2) + r"^{\circ}",
               _xx(math.degrees(math.acos(h / (R + h))), 2) + r"^{\circ}"]
        nhieu = _ba_nhieu(dap, ung, buoc=lambda k: _xx(t + 0.1 * k, 2) + r"^{\circ}")
        debai = (_mo_dau_chan_troi(ten, h) + r" Given $R = %d\,\text{km}$. The angle of depression $\theta$ (rounded "
                 r"to the nearest hundredth of a degree) is" % R)
        giai = (_GIAI_VUONG_T + "\\\\\n"
                r"The horizontal at $M$ is perpendicular to $OM$, so "
                r"$\widehat{OMT} = 90^{\circ} - \theta$, hence "
                r"$\widehat{TOM} = 90^{\circ} - \widehat{OMT} = \theta$."
                "\\\\\n"
                r"Therefore $\cos\theta = \dfrac{OT}{OM} = \dfrac{R}{R + h} = \dfrac{%d}{%s}"
                r"\Rightarrow \theta \approx %s$." % (R, _xx(R + h, 2), dap))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_K_01(socau, dang=2):
    r"""Đường chân trời (mức VD): biết $R = 6371\,\text{km}$ và $h$, tính khoảng cách $MT$
    từ người quan sát tới đường chân trời (định lí Pythagore trong tam giác $OTM$ vuông tại $T$).

    CLAUDE THEM 01/10/2026 - co Lan duyet lai.
    """
    R = _R_TRAI_DAT
    cau = ""
    for ten, h in _chon_nui(socau):
        MT = math.sqrt((R + h) ** 2 - R ** 2)
        dap = str(_lt(MT))
        debai = (_mo_dau_chan_troi(ten, h) + r" Given $R = %d\,\text{km}$. Find the distance $MT$ "
                 r"from the observer to the horizon (in km, rounded to the nearest whole number)." % R)
        giai = (_GIAI_VUONG_T + "\\\\\n"
                r"By the Pythagorean theorem: $MT = \sqrt{OM^{2} - OT^{2}} = "
                r"\sqrt{%s^{2} - %d^{2}} \approx %s\,\text{(km)}$." % (_xx(R + h, 2), R, dap))
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai,
                                  _hinh_trai_dat(), 0, dang)
    return cau


# Công thức đúng và các công thức nhiễu cho dạng VDC tìm R theo h, theta
_CT_R_DUNG = r"R = \dfrac{h\cos\theta}{1 - \cos\theta}"
_CT_R_NHIEU = [r"R = \dfrac{h}{1 - \cos\theta}",
               r"R = \dfrac{h\sin\theta}{1 - \sin\theta}",
               r"R = \dfrac{h\left(1 - \cos\theta\right)}{\cos\theta}",
               r"R = \dfrac{h\cos\theta}{1 + \cos\theta}"]


def _giai_tim_R(h=None, theta=None, R=None):
    """Lời giải lập công thức R theo h, theta (VDC); có số thì thay số ở cuối."""
    s = (_GIAI_VUONG_T + "\\\\\n"
         r"The horizontal at $M$ is perpendicular to $OM$, so $\widehat{OMT} = 90^{\circ} - \theta$, "
         r"hence $\widehat{TOM} = \theta$."
         "\\\\\n"
         r"Therefore $\cos\theta = \dfrac{OT}{OM} = \dfrac{R}{R + h} \Rightarrow "
         r"\left(R + h\right)\cos\theta = R \Rightarrow R\left(1 - \cos\theta\right) = h\cos\theta$,"
         "\\\\\n"
         r"that is, $" + _CT_R_DUNG + r"$.")
    if R is not None:
        s += ("\\\\\n"
              r"Substituting: $R = \dfrac{%s\cdot\cos %s^{\circ}}{1 - \cos %s^{\circ}} \approx %s\,\text{(km)}$. "
              r"Since $1 - \cos\theta$ is very small, keep enough digits on the calculator and do not round early."
              % (_xx(h, 2), _xx(theta, 2), _xx(theta, 2), _xx(R, 0)))
    return s


def L10_C3_B6_VD036_MC_L_01(socau, dang=1):
    r"""Đường chân trời (mức VDC): biết $h$ và góc hạ $\theta$, chọn công thức tính bán kính $R$.

    Không hỏi ra số vì nhiễu "quên nhân $\cos\theta$" chỉ lệch khoảng $h$ (2-3 km) so với
    đáp số, dễ gây tranh cãi; hỏi công thức thì các phương án tách bạch.

    CLAUDE THEM 01/10/2026 - co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for ten, h in _chon_nui(socau):
        theta = round(math.degrees(math.acos(_R_TRAI_DAT / (_R_TRAI_DAT + h))), 2)
        debai = (_mo_dau_chan_troi(ten, h) + r" The person measures $\theta = %s^{\circ}$. The radius "
                 r"$R$ of the Earth is given in terms of $h$ and $\theta$ by which of the following formulas?"
                 % _xx(theta, 2))
        nhieu = random.sample(_CT_R_NHIEU, 3)
        cau += MC_SA_answer_const(debai, _CT_R_DUNG, nhieu, _giai_tim_R(), _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_L_01(socau, dang=2):
    r"""Đường chân trời (mức VDC): biết $h$ và góc hạ $\theta$, tính bán kính $R$ của Trái Đất.

    $\theta$ được tính từ bán kính thật $6371\,\text{km}$ rồi làm tròn hai chữ số thập phân
    (số đo hợp lí); đáp số làm tròn đến hàng đơn vị (4 chữ số).

    CLAUDE THEM 01/10/2026 - co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for ten, h in _chon_nui(socau):
        theta = round(math.degrees(math.acos(_R_TRAI_DAT / (_R_TRAI_DAT + h))), 2)
        c = math.cos(math.radians(theta))
        R = h * c / (1 - c)
        dap = str(_lt(R))
        debai = (_mo_dau_chan_troi(ten, h) + r" The person measures $\theta = %s^{\circ}$. Calculate the radius "
                 r"$R$ of the Earth (in km, rounded to the nearest whole number)." % _xx(theta, 2))
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)],
                                  _giai_tim_R(h, theta, R), _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_D_01(socau, dong=1):
    r"""Tàu đổi hướng trên biển: định lí côsin rồi định lí sin.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Số liệu chọn sao cho $AC$ ra SỐ NGUYÊN: tàu đổi hướng $60^{\circ}$
    nên $\widehat{ABC} = 120^{\circ}$, $\cos 120^{\circ} = -\dfrac{1}{2}$,
    do đó $AC^2 = a^2 + b^2 + ab$. Chỉ lấy những cặp $(a; b)$ làm cho
    $a^2 + ab + b^2$ là số chính phương, ví dụ $(3;5)$ cho $AC = 7$.
    """
    # các cặp (a, b) cho a^2 + ab + b^2 chính phương
    CAP = []
    for a in range(3, 41):
        for b in range(a + 1, 61):
            k2 = a * a + a * b + b * b
            k = math.isqrt(k2)
            if k * k == k2:
                CAP.append((a, b, k))

    PHUONG_TIEN = [("A ship", "ship"), ("A motorboat", "motorboat"),
                   ("A sailboat", "sailboat")]

    gt = []
    thu = 0
    while len(gt) < socau and thu < 200:
        thu += 1
        v = (random.randrange(len(CAP)), random.randrange(len(PHUONG_TIEN)))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for i_cap, i_pt in gt:
        a, b, k = CAP[i_cap]
        ten_hoa, ten = PHUONG_TIEN[i_pt]

        # góc BAC: định lí sin, sin(BAC) = b*sin(120)/k
        sin_A = b * math.sin(math.radians(120)) / k
        goc_A = math.degrees(math.asin(sin_A))

        debai = (r"%s departs from port $A$ and travels $%d\,\text{km}$ straight in "
                 r"a fixed direction to position $B$. At $B$, the %s changes direction "
                 r"by an angle of $60^{\circ}$ and then travels a further $%d\,\text{km}$ "
                 r"in a straight line to reach island $C$."
                 % (ten_hoa, a, ten, b))

        hoi_a = r"Find the measure of angle $\widehat{ABC}$."
        giai_a = (r"The original direction of the %s is the ray opposite to ray $BA$. Changing direction by an angle of "
                  r"$60^{\circ}$ means that ray $BC$ makes an angle of "
                  r"$60^{\circ}$ with that original direction, so $\widehat{ABC}$ forms a linear pair with the $60^{\circ}$ angle:"
                  "\\\\\n"
                  r"$\widehat{ABC} = 180^{\circ} - 60^{\circ} = 120^{\circ}$."
                  % ten)

        hoi_b = r"Find the distance $AC$ from port $A$ to island $C$."
        giai_b = (r"Apply the law of cosines in triangle $ABC$:"
                  "\\\\\n"
                  r"$AC^2 = AB^2 + BC^2 - 2\cdot AB\cdot BC\cdot"
                  r"\cos\widehat{ABC}$"
                  "\\\\\n"
                  r"$AC^2 = %d^2 + %d^2 - 2\cdot %d\cdot %d\cdot"
                  r"\left(-\dfrac{1}{2}\right) = %d$."
                  "\\\\\n"
                  r"Hence $AC = %d\,\text{(km)}$."
                  % (a, b, a, b, k * k, k))

        hoi_c = (r"From island $C$, the %s wants to head straight back to port $A$. Find the measure of angle "
                 r"$\widehat{BAC}$ (rounded to the nearest tenth of a degree)." % ten)
        giai_c = (r"Apply the law of sines in triangle $ABC$:"
                  "\\\\\n"
                  r"$\dfrac{BC}{\sin\widehat{BAC}} = "
                  r"\dfrac{AC}{\sin\widehat{ABC}} \Rightarrow "
                  r"\sin\widehat{BAC} = \dfrac{BC\cdot\sin\widehat{ABC}}{AC} "
                  r"= \dfrac{%d\cdot\sin 120^{\circ}}{%d} \approx %s$."
                  "\\\\\n"
                  r"Since triangle $ABC$ already has the obtuse angle $\widehat{ABC} = "
                  r"120^{\circ}$, $\widehat{BAC}$ is acute, so"
                  "\\\\\n"
                  r"$\widehat{BAC} \approx %s^{\circ}$."
                  % (b, k, _xx(sin_A, 4), _xx(goc_A, 1)))

        ds_abcd = [(hoi_a, r"120^{\circ}", giai_a),
                   (hoi_b, "%d\\,\\text{km}" % k, giai_b),
                   (hoi_c, "%s^{\\circ}" % _xx(goc_A, 1), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BIẾN THỂ LẤY TỪ GIÁO ÁN BÀI 5 CỦA CÔ LAN (29/09/2026)
# Nguồn: giáo án "Bài 5. Giá trị lượng giác của một góc từ 0 đến 180 độ"
# (dự án giáo án). Mỗi hàm là một biến thể CÙNG DẠNG với ID đã có trong
# mapping, số liệu sinh tự động, đáp án tính bằng sympy (chính xác).
# =====================================================================

def _gtlg(ham, d):
    """Giá trị lượng giác (sympy) của góc đặc biệt d; None nếu không xác định."""
    hang = [r for r in BANG_GTLG if r[0] == d][0]
    return hang[{"sin": 1, "cos": 2, "tan": 3, "cot": 4}[ham]]


def _so_thap_phan_gon(v, toi_da=4):
    """Chuỗi số thập phân hữu hạn (dấu phẩy) nếu v hữu tỉ viết được gọn
    trong toi_da kí tự; không được thì None."""
    v = nsimplify(v)
    if not v.is_Rational:
        return None
    q = int(v.q)
    while q % 2 == 0:
        q //= 2
    while q % 5 == 0:
        q //= 5
    if q != 1:
        return None
    x = float(v)
    t = ("%.4f" % x).rstrip("0").rstrip(".")
    if t in ("-0", ""):
        t = "0"
    t = t.replace(".", DAU_THAP_PHAN)
    return t if len(t) <= toi_da else None


def L10_C3_B5_NB029_MC_A_02(socau, dang=1):
    r"""Giá trị lượng giác của góc đặc biệt - tính BIỂU THỨC gồm ba, bốn giá
    trị lượng giác của các góc đặc biệt (kể cả góc tù).

    CLAUDE THEM 29/09/2026 - bien the 02 cua NB029_MC_A, lay theo bai tap
    [NB] trong giao an Bai 5 cua co Lan ("A = 2sin30 + 3tan45 - 4cos60 +
    cot135"). Chi dung cac gia tri HUU TI de ket qua gon. Co Lan duyet.
    """
    HUU_TI = [(h, d) for d in (0, 30, 45, 60, 90, 120, 135, 150, 180)
              for h in ("sin", "cos", "tan", "cot")
              if _gtlg(h, d) is not None and _gtlg(h, d).is_Rational]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        hang = random.sample(HUU_TI, random.choice([3, 4]))
        he = [random.choice([1, 2, 3, 4, -1, -2, -3]) for _ in hang]
        if any(_gtlg(h, d) == 0 for h, d in hang):
            continue
        key = tuple(sorted(zip(he, hang)))
        if key in gt:
            continue
        gt.append(key)
    cauTN = ""
    for key in gt:
        key = list(key)
        random.shuffle(key)
        tong = sum(k * _gtlg(h, d) for k, (h, d) in key)
        bt = ""
        thay = ""
        for i, (k, (h, d)) in enumerate(key):
            dau = ("-" if k < 0 else "") if i == 0 else (" - " if k < 0 else " + ")
            so = "" if abs(k) == 1 else str(abs(k))
            bt += r"%s%s\%s %s" % (dau, so, h, _goc(d))
            v = _gtlg(h, d)
            thay += r"%s%s%s" % (dau, (so + r"\cdot ") if so else "",
                                  (r"\left(%s\right)" % _L(v)) if v < 0 else _L(v))
        # nhieu: quen doi dau o goc tu / nham sin-cos / cong sai dau
        sai1 = sum(k * abs(_gtlg(h, d)) for k, (h, d) in key)
        sai2 = sum(k * (_gtlg({"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan"}[h], d)
                        if _gtlg({"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan"}[h], d)
                        is not None else 0) for k, (h, d) in key)
        dung = "$%s$" % _L(tong)
        nhieu = _ba_nhieu(dung, ["$%s$" % _L(simplify(x)) for x in (sai1, sai2, -tong, tong + 1)],
                          buoc=lambda t: "$%s$" % _L(tong + t + 1))
        debai = r"The value of the expression $A = %s$ is" % bt
        giai = (r"Use the table of trigonometric values of special angles (for an obtuse angle use the relation between "
                r"supplementary angles):\\ $A = %s = %s$." % (thay, _L(tong)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_NB029_MC_E_02(socau, dang=1):
    r"""Xét dấu - biết $\alpha$ là góc tù, chọn BIỂU THỨC (tích hoặc thương hai
    giá trị lượng giác) luôn âm / luôn dương.

    CLAUDE THEM 29/09/2026 - bien the 02 cua NB029_MC_E, theo vi du trong
    giao an Bai 5 ("phi tu, xet dau T = sin phi . cot phi"). Co Lan duyet.
    """
    DAU = DAU_GTLG["tu"]
    ten = [r"\sin", r"\cos", r"\tan", r"\cot"]
    cap = [(a, b, phep) for i, a in enumerate(ten) for b in ten[i + 1:]
           for phep in ("nhan", "chia")]
    def viet(a, b, phep):
        return (r"%s\alpha\cdot %s\alpha" % (a, b)) if phep == "nhan" else \
            (r"\dfrac{%s\alpha}{%s\alpha}" % (a, b))
    def dau(a, b, phep):
        return DAU[a] * DAU[b]
    cauTN = ""
    for _ in range(socau):
        hoi_am = random.random() < 0.5
        muc = -1 if hoi_am else 1
        dung_ds = [c for c in cap if dau(*c) == muc]
        sai_ds = [c for c in cap if dau(*c) != muc]
        d = random.choice(dung_ds)
        sai = random.sample(sai_ds, 3)
        dung = "$%s$" % viet(*d)
        nhieu = ["$%s$" % viet(*c) for c in sai]
        debai = (r"Given an angle $\alpha$ satisfying $90^{\circ} < \alpha < 180^{\circ}$. Which expression "
                 r"below is always \textbf{%s}?" % ("negative" if hoi_am else "positive"))
        giai = (r"Angle $\alpha$ is obtuse, so $\sin\alpha > 0$, while $\cos\alpha < 0$, $\tan\alpha < 0$, "
                r"$\cot\alpha < 0$." + "\\\\\n" +
                r"The product (quotient) of two numbers of the same sign is positive, and of opposite signs is negative. Hence "
                r"$%s$ is %s." % (viet(*d), "negative" if hoi_am else "positive") + "\\\\\n" +
                r"The other three expressions are all %s." % ("positive" if hoi_am else "negative"))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_NB029_MC_G_02(socau, dang=1):
    r"""Biết dấu của một TÍCH hai giá trị lượng giác, suy ra loại góc.

    CLAUDE THEM 29/09/2026 - bien the 02 cua NB029_MC_G, theo vi du trong
    giao an Bai 5 ("sin alpha . cos alpha < 0 thi alpha nhon, vuong hay
    tu?"). Co Lan duyet.
    """
    TH = [(r"\sin\alpha\cdot\cos\alpha < 0", "tu", r"\cos\alpha < 0"),
          (r"\sin\alpha\cdot\cos\alpha > 0", "nhon", r"\cos\alpha > 0"),
          (r"\sin\alpha\cdot\tan\alpha < 0", "tu", r"\tan\alpha < 0"),
          (r"\sin\alpha\cdot\tan\alpha > 0", "nhon", r"\tan\alpha > 0"),
          (r"\sin\alpha\cdot\cot\alpha < 0", "tu", r"\cot\alpha < 0"),
          (r"\sin\alpha\cdot\cot\alpha > 0", "nhon", r"\cot\alpha > 0")]
    PA = {"nhon": r"$\alpha$ is an acute angle", "tu": r"$\alpha$ is an obtuse angle",
          "vuong": r"$\alpha = 90^{\circ}$", "bet": r"$\alpha = 0^{\circ}$ or $\alpha = 180^{\circ}$"}
    ds = list(range(len(TH)))
    random.shuffle(ds)
    cauTN = ""
    for i in ds[:min(socau, len(ds))]:
        dk, loai, suy = TH[i]
        dung = PA[loai]
        nhieu = [PA[k] for k in PA if k != loai]
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ satisfying "
                 r"$%s$. Which of the following statements is \textbf{true}?" % dk)
        giai = (r"Since $0^{\circ} \le \alpha \le 180^{\circ}$, we have $\sin\alpha \ge 0$. The product is not $0$, so "
                r"$\sin\alpha > 0$, i.e. $\alpha \ne 0^{\circ}$, $\alpha \ne 180^{\circ}$ (and since the values "
                r"in the product are defined, $\alpha \ne 90^{\circ}$)." + "\\\\\n" +
                r"Hence $%s$, so %s." % (suy, dung))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_MC_A_02(socau, dang=1):
    r"""Quan hệ giữa giá trị lượng giác của hai góc bù nhau - TRONG TAM GIÁC
    ($B + C = 180^{\circ} - A$).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH031_MC_A, theo giao an Bai 5
    ("cos A + cos(B + C) = 0", "sin A = sin(B + C)"). Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        X, Y, Z = random.sample("ABC", 3)
        tong = r"%s + %s" % tuple(sorted([Y, Z]))
        DUNG = [r"\sin\left(%s\right) = \sin %s" % (tong, X),
                r"\cos\left(%s\right) = -\cos %s" % (tong, X),
                r"\tan\left(%s\right) = -\tan %s" % (tong, X),
                r"\cos %s + \cos\left(%s\right) = 0" % (X, tong)]
        SAI = [r"\sin\left(%s\right) = -\sin %s" % (tong, X),
               r"\cos\left(%s\right) = \cos %s" % (tong, X),
               r"\tan\left(%s\right) = \tan %s" % (tong, X),
               r"\sin %s + \sin\left(%s\right) = 0" % (X, tong),
               r"\cos\left(%s\right) = \sin %s" % (tong, X)]
        k = random.randrange(len(DUNG))
        dung = "$%s$" % DUNG[k]
        nhieu = ["$%s$" % t for t in random.sample(SAI, 3)]
        debai = r"Given triangle $ABC$. Which of the following statements is \textbf{true}?"
        giai = (r"Since $A + B + C = 180^{\circ}$, we have $%s = 180^{\circ} - %s$: the angles $%s$ and $%s$ "
                r"are supplementary." % (tong, X, tong, X) + "\\\\\n" +
                r"Supplementary angles have equal sines; their cosines and tangents are opposite. Hence "
                r"$\sin\left(%s\right) = \sin %s$, $\cos\left(%s\right) = -\cos %s$, "
                r"$\tan\left(%s\right) = -\tan %s$." % (tong, X, tong, X, tong, X) + "\\\\\n" +
                r"So the true statement is %s." % dung)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_SA_C_04(socau, dang=2):
    r"""Trả lời ngắn: tam giác biết hai góc; tính biểu thức dùng quan hệ hai
    góc bù nhau (vd $T = \cos C\cdot\tan\left(A + B\right)$).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH031_SA_A, theo bai tap trong
    giao an Bai 5. Chi giu bo so cho dap so thap phan huu han, toi da 4 ki
    tu. Co Lan duyet.
    """
    GOC = [30, 45, 60, 90, 120, 135, 150]
    MAU = [("cos", "tan"), ("sin", "cot"), ("tan", "cos"), ("cot", "sin"),
           ("sin", "sin"), ("cos", "cos"), ("tan", "tan")]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 2000:
        lan += 1
        C = random.choice([30, 45, 60, 90, 120])
        A = random.choice([g for g in range(15, 180 - C, 15)])
        B = 180 - A - C
        if B <= 0 or 180 - C not in GOC:
            continue
        h1, h2 = random.choice(MAU)
        v1, v2 = _gtlg(h1, C), _gtlg(h2, 180 - C)
        if v1 is None or v2 is None:
            continue
        T = simplify(v1 * v2)
        dap = _so_thap_phan_gon(T)
        if dap is None or T == 0 or (A, B, h1, h2) in gt:
            continue
        gt.append((A, B, h1, h2))
    cau = ""
    for A, B, h1, h2 in gt:
        C = 180 - A - B
        v1, v2 = _gtlg(h1, C), _gtlg(h2, 180 - C)
        T = simplify(v1 * v2)
        dap = _so_thap_phan_gon(T)
        debai = (r"Given triangle $ABC$ with $\widehat{A} = %s$, $\widehat{B} = %s$. Find the value "
                 r"of the expression $T = \%s C\cdot\%s\left(A + B\right)$."
                 % (_goc(A), _goc(B), h1, h2))
        giai = (r"$\widehat{C} = 180^{\circ} - %s - %s = %s$, so $\%s C = \%s %s = %s$.\\ "
                r"$A + B = 180^{\circ} - C = %s$, so $\%s\left(A + B\right) = \%s %s = %s$.\\ "
                r"Hence $T = %s\cdot %s = %s$."
                % (_goc(A), _goc(B), _goc(C), h1, h1, _goc(C), _L(v1),
                   _goc(180 - C), h2, h2, _goc(180 - C), _L(v2),
                   (r"\left(%s\right)" % _L(v1)) if v1 < 0 else _L(v1),
                   (r"\left(%s\right)" % _L(v2)) if v2 < 0 else _L(v2), dap))
        nguoc = _so_thap_phan_gon(-T) or "0"
        ds = _ba_nhieu(dap, [nguoc, "1", "-1", "0"], buoc=lambda t: str(t + 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_E_02(socau, dang=2):
    r"""Trả lời ngắn: tổng bình phương sin (hoặc côsin) của các góc cách đều,
    ghép cặp hai góc PHỤ nhau ($\cos(90^{\circ} - x) = \sin x$) rồi dùng
    $\sin^2 x + \cos^2 x = 1$.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH031_SA_B, theo bai
    "S = cos^2 5 + cos^2 10 + ... + cos^2 85" trong giao an Bai 5 (nguon: de
    on theo bai). Buoc goc va goc dau thay doi. Co Lan duyet.
    """
    BO = [(b, d) for d in (5, 10, 15, 18, 30) for b in range(d, 45, d)
          if (90 - b) % d == 0 and b < 45 and len(range(b, 90 - b + 1, d)) >= 5]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        b, d = random.choice(BO)
        ham = random.choice(["sin", "cos"])
        k = random.choice([1, 1, 2, 4])
        if (b, d, ham, k) in gt:
            continue
        gt.append((b, d, ham, k))
    cau = ""
    for b, d, ham, k in gt:
        goc = list(range(b, 90 - b + 1, d))
        n = len(goc)
        co45 = 45 in goc
        so_cap = (n - 1) // 2 if co45 else n // 2
        S = Rational(so_cap) + (Rational(1, 2) if co45 else 0)
        S = S * k
        dap = _so_thap_phan_gon(S)
        if dap is None:
            dap = str(S)
        he = "" if k == 1 else "%d" % k
        day = r"\%s^{2}%s + \%s^{2}%s + \%s^{2}%s + \cdots + \%s^{2}%s" % (
            ham, _goc(goc[0]), ham, _goc(goc[1]), ham, _goc(goc[2]), ham, _goc(goc[-1]))
        gom = (r", where the sum consists of the squares of the %s values of the angles $%s, %s, \ldots, %s$ "
               r"(consecutive angles differ by $%s$). Find the value of $S$."
               % ("sin" if ham == "sin" else "cos", _goc(goc[0]), _goc(goc[1]), _goc(goc[-1]), _goc(d)))
        debai = (r"Given the expression $S = %s\left(%s\right)$" % (he, day) + gom) if k != 1 else \
            (r"Given the expression $S = %s$" % day + gom)
        phu = "sin" if ham == "cos" else "cos"
        giai = (r"The sequence of angles $%s, %s, \ldots, %s$ has $\dfrac{%d - %d}{%d} + 1 = %d$ angles."
                % (_goc(goc[0]), _goc(goc[1]), _goc(goc[-1]), goc[-1], goc[0], d, n) + "\\\\\n" +
                r"Pair complementary angles $x$ and $90^{\circ} - x$: $\%s^{2}\left(90^{\circ} - x\right) = "
                r"\%s^{2}x$, so each pair gives $\%s^{2}x + \%s^{2}\left(90^{\circ} - x\right) = 1$."
                % (ham, phu, ham, ham) + "\\\\\n" +
                (r"There are $%d$ pairs, and the angle $45^{\circ}$ is left over, with $\%s^{2}45^{\circ} = \dfrac{1}{2}$."
                 % (so_cap, ham) if co45 else r"There are $%d$ pairs." % so_cap) + "\\\\\n" +
                r"Therefore $S = %s%s$." % (("%d\\cdot " % k) if k != 1 else "",
                                       (r"\left(%d + \dfrac{1}{2}\right) = %s" % (so_cap, dap)) if co45
                                       else (r"%d = %s" % (so_cap, dap)) if k != 1 else dap))
        ds = _ba_nhieu(dap, [str(n), str(so_cap * k), _so_thap_phan_gon(S + k) or str(S + k)],
                       buoc=lambda t: str(n + t))
        cau += MC_SA_answer_const(debai, dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_TF_A_02(socau, socot=1):
    r"""Đúng/Sai - biết $\sin\alpha$ (bộ ba Pythagore) và loại góc (nhọn/tù):
    tính $\cos$, $\tan$, $\cot$ và $\sin\left(180^{\circ} - \alpha\right)$.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C3_TF_A, theo cau Dung/Sai
    trong giao an Bai 5 ("sin alpha = 3/5, 0 < alpha < 90"). Moi y co ban
    dung va ban sai (sai dau / dao tu mau). Co Lan duyet.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    BO = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (4, 3, 5), (12, 5, 13)]
    cauTF = ""
    so = 0
    while so < socau:
        a, b, c = random.choice(BO)
        tu = random.random() < 0.5
        sn = Rational(a, c)
        cs = Rational(-b, c) if tu else Rational(b, c)
        tn, ct = sn / cs, cs / sn
        bts = [_n1_phan_thuc(sn, cs) for _ in range(2)]
        if None in bts:
            continue
        so += 1
        khoang = r"90^{\circ} < \alpha < 180^{\circ}" if tu else r"0^{\circ} < \alpha < 90^{\circ}"
        debai = (r"Given an angle $\alpha$ satisfying $\sin\alpha = %s$ and $%s$. Determine whether each of "
                 r"the following statements is true or false:" % (_L(sn), khoang))
        # a) NB - quan he hai goc bu nhau, phu nhau
        ly_a = (r"Supplementary angles have equal sines: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha = %s$; "
                r"for complementary angles: $\cos\left(90^{\circ} - \alpha\right) = \sin\alpha = %s$." % (_L(sn), _L(sn)))
        y1 = _phat_bieu(
            [(r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a), (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a)],
            [(r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a), (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a),
             (r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(1 - sn), ly_a), (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(1 - sn), ly_a)])
        # b) TH - he thuc co ban va xet dau cos theo loai goc
        ly_cos = (r"$\cos^{2}\alpha = 1 - \left(%s\right)^{2} = %s$, and since $\alpha$ is %s, "
                  r"$\cos\alpha %s 0$, so $\cos\alpha = %s$."
                  % (_L(sn), _L(1 - sn ** 2), "obtuse" if tu else "acute", "<" if tu else ">", _L(cs)))
        y2 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", cs, ly_cos,
                            [(-cs, "Sign error"), ((-1 if tu else 1) * (1 - sn), "Forgot to square"),
                             ((-1 if tu else 1) * cs ** 2, "Forgot to take the square root")]),
                     _tf_ct(r"$\cos^{2}\alpha = %s$", cs ** 2, ly_cos, [(1 + sn ** 2, "Sign error in $1 - \\sin^{2}\\alpha$"), (sn ** 2, "Mistakenly using $\\cos^{2}\\alpha = \\sin^{2}\\alpha$")]))
        # c) VD - dung ket qua cua b) de tinh tan, cot
        ly_c = ly_cos + r" $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$, $\cot\alpha = \dfrac{1}{\tan\alpha} = %s$." % (_L(tn), _L(ct))
        y3 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", tn, ly_c, [(1 / tn, "Numerator and denominator swapped"), (-tn, "Sign error"), (sn * cs, "Mistakenly using $\\tan\\alpha = \\sin\\alpha\\cdot\\cos\\alpha$")]),
                     _tf_ct(r"$\cot\alpha = %s$", ct, ly_c, [(tn, "Mistakenly using $\\cot\\alpha = \\tan\\alpha$"), (-ct, "Sign error")]))
        # d) VDC - thay ca sin va cos vao bieu thuc phan thuc (2 bieu thuc)
        dung, sai = [], []
        for bt, P, Ps in bts:
            ly = r"Substituting $\sin\alpha = %s$, $\cos\alpha = %s$ (part b) into the expression gives $%s$." % (_L(sn), _L(cs), _L(P))
            d_, s_ = _tf_ct("$" + bt + " = %s$", P, ly, Ps)
            dung += d_
            sai += s_
        y4 = _phat_bieu(dung, sai)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _lyq = r"Supplementary angles have equal sines and opposite cosines; for complementary angles, the sine of one equals the cosine of the other."
        _tf_them(y1, [(r"$\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha$", _lyq), (r"$\sin\left(90^{\circ} - \alpha\right) = \cos\alpha$", _lyq),
                      (r"$\tan\left(180^{\circ} - \alpha\right) = -\tan\alpha$", _lyq)],
                 [(r"$\cos\left(180^{\circ} - \alpha\right) = \cos\alpha$", _lyq), (r"$\sin\left(90^{\circ} - \alpha\right) = \sin\alpha$", _lyq),
                  (r"$\tan\left(180^{\circ} - \alpha\right) = \tan\alpha$", _lyq)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


# =====================================================================
# BIẾN THỂ LẤY TỪ GIÁO ÁN BÀI 6 CỦA CÔ LAN (29/09/2026)
# Nguồn: giáo án "Bài 6. Hệ thức lượng trong tam giác" (dự án giáo án).
# Curriculum Bài 6: TH032-TH035 (mức TH) và VD036 (thực tiễn). Theo cô Lan:
# được hạ mức độ nhưng KHÔNG được nâng - câu tính toán thuần tuý chỉ đưa vào
# ID mức TH khi đúng là một, hai bước áp dụng công thức.
# =====================================================================

_COS_PHAN_SO = [Rational(3, 5), Rational(4, 5), Rational(-3, 5), Rational(-4, 5),
                Rational(5, 13), Rational(12, 13), Rational(-5, 13), Rational(1, 3),
                Rational(-1, 3), Rational(1, 4), Rational(-1, 4)]


def _sin_tu_cos(c):
    return sqrt(1 - c ** 2)


def L10_C3_B6_TH032_MC_A_03(socau, dang=1):
    r"""Tính cạnh còn lại bằng định lí côsin khi góc cho bằng $\cos A$ là một
    PHÂN SỐ (không phải góc đặc biệt); đáp số có thể là căn thức.

    CLAUDE THEM 29/09/2026 - bien the 03 cua TH032_MC_A, theo vi du trong
    giao an Bai 6 ("AB = 4, AC = 5, cos A = 3/5"). Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        cA = random.choice(_COS_PHAN_SO)
        q = cA.q
        b = q * random.randint(1, 3) if q > 3 else random.randint(2, 9)
        c = random.randint(2, 12)
        a2 = b * b + c * c - 2 * b * c * cA
        if not a2.is_Integer or a2 <= 0 or b == c or (b, c, cA) in gt:
            continue
        gt.append((b, c, cA))
    cauTN = ""
    for b, c, cA in gt:
        a2 = Integer(b * b + c * c - 2 * b * c * cA)
        dung = "$%s$" % _L(sqrt(a2))
        nhieu = _ba_nhieu(dung, ["$%s$" % _L(a2),
                                 "$%s$" % _L(sqrt(Integer(b * b + c * c + 2 * b * c * cA))),
                                 "$%s$" % _L(sqrt(Integer(b * b + c * c)))],
                          buoc=lambda t: "$%s$" % _L(sqrt(a2 + t)))
        debai = (r"Given triangle $ABC$ with $AB = %d$, $AC = %d$ and $\cos A = %s$. The length of side "
                 r"$BC$ is" % (c, b, _L(cA)))
        giai = (r"By the law of cosines: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos A$\\ "
                r"$= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %d$.\\ Hence $BC = %s$."
                % (c, b, c, b, (r"\left(%s\right)" % _L(cA)) if cA < 0 else _L(cA), a2, _L(sqrt(a2))))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _bo_trung_tuyen(so_nguyen=False, lan_thu=3000):
    """Ba cạnh (a, b, c) nguyên, tam giác hợp lệ; m_a^2 = (2b^2 + 2c^2 - a^2)/4.
    so_nguyen=True: chỉ lấy bộ có m_a nguyên (cho câu trả lời ngắn)."""
    for _ in range(lan_thu):
        a, b, c = (random.randint(3, 20) for _ in range(3))
        if not (a + b > c and b + c > a and a + c > b) or b == c:
            continue
        m2 = Rational(2 * b * b + 2 * c * c - a * a, 4)
        if so_nguyen:
            k = math.isqrt(int(m2)) if m2.is_Integer else -1
            if k < 1 or k * k != m2:
                continue
        return a, b, c, m2
    return None


_DINH_CANH = [("A", "BC", "CA", "AB"), ("B", "CA", "AB", "BC"), ("C", "AB", "BC", "CA")]


def L10_C3_B6_TH032_MC_C_01(socau, dang=1):
    r"""Tính độ dài ĐƯỜNG TRUNG TUYẾN khi biết ba cạnh (công thức suy từ định lí
    côsin).

    CLAUDE THEM 29/09/2026 - dang moi TH032_MC_C, theo giao an Bai 6. Co Lan
    duyet (muc TH: mot lan ap dung cong thuc).
    """
    cauTN = ""
    for _ in range(socau):
        a, b, c, m2 = _bo_trung_tuyen()
        dinh, doi, k1, k2 = random.choice(_DINH_CANH)
        m = sqrt(m2)
        dung = "$%s$" % _L(m)
        sai = sqrt(Rational(b * b + c * c, 2) + Rational(a * a, 4))
        nhieu = _ba_nhieu(dung, ["$%s$" % _L(m2), "$%s$" % _L(sai),
                                 "$%s$" % _L(sqrt(Rational(b * b + c * c, 2)))],
                          buoc=lambda t: "$%s$" % _L(sqrt(m2 + t)))
        debai = (r"Given triangle $ABC$ with $%s = %d$, $%s = %d$, $%s = %d$. The length of the median "
                 r"from vertex $%s$ is" % (doi, a, k1, b, k2, c, dinh))
        giai = (r"The median from $%s$ to the opposite side $%s = %d$:\\ "
                r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4} = \dfrac{%d + %d}{2} - "
                r"\dfrac{%d}{4} = %s$.\\ Hence the length of the median is $%s$."
                % (dinh, doi, a, dinh.lower(), k1, k2, doi, b * b, c * c, a * a, _L(m2), _L(m)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH032_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn: độ dài đường trung tuyến (đáp số nguyên).

    CLAUDE THEM 29/09/2026 - dang moi TH032_SA_C. Co Lan duyet.
    """
    cau = ""
    for _ in range(socau):
        a, b, c, m2 = _bo_trung_tuyen(so_nguyen=True)
        dinh, doi, k1, k2 = random.choice(_DINH_CANH)
        m = int(math.isqrt(int(m2)))
        debai = (r"Given triangle $ABC$ with $%s = %d$, $%s = %d$, $%s = %d$. Find the length of the median "
                 r"from vertex $%s$." % (doi, a, k1, b, k2, c, dinh))
        giai = (r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4} = \dfrac{%d + %d}{2} - "
                r"\dfrac{%d}{4} = %d$, so $m_{%s} = %d$."
                % (dinh.lower(), k1, k2, doi, b * b, c * c, a * a, m * m, dinh.lower(), m))
        cau += MC_SA_answer_const(debai, str(m), [str(m * m), str(m + 1), str(m - 1)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_MC_A_02(socau, dang=1):
    r"""Định lí sin: tam giác nội tiếp đường tròn bán kính $R$, biết hai góc,
    tính cạnh đối diện góc THỨ BA ($c = 2R\sin C$).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH033_MC_A, theo giao an Bai 6
    ("R = 6, A = 45, B = 75, tinh AB"). Co Lan duyet.
    """
    GOC_C = [30, 45, 60, 90, 120, 135, 150]
    cauTN = ""
    for _ in range(socau):
        C = random.choice(GOC_C)
        A = random.choice([g for g in range(15, 180 - C, 15)])
        B = 180 - A - C
        if B <= 0:
            B, A = 15, 180 - C - 15
        R = random.randint(2, 12)
        sC = _gtlg("sin", C)
        c = simplify(2 * R * sC)
        dung = "$%s$" % _L(c)
        nhieu = _ba_nhieu(dung, ["$%s$" % _L(simplify(R * sC)),
                                 "$%s$" % _L(simplify(2 * R * _gtlg("cos", C))) if C != 90 else "$0$",
                                 "$%s$" % _L(simplify(2 * R / sC))],
                          buoc=lambda t: "$%s$" % _L(c + t))
        debai = (r"Triangle $ABC$ is inscribed in a circle of radius $R = %d$ and has $\widehat{A} = %s$, "
                 r"$\widehat{B} = %s$. The length of side $AB$ is" % (R, _goc(A), _goc(B)))
        giai = (r"$\widehat{C} = 180^{\circ} - %s - %s = %s$. Side $AB = c$ is opposite angle $C$.\\ "
                r"By the law of sines: $c = 2R\sin C = 2\cdot %d\cdot\sin %s = %s$."
                % (_goc(A), _goc(B), _goc(C), R, _goc(C), _L(c)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_SA_B_02(socau, dang=2):
    r"""Trả lời ngắn: bán kính đường tròn ngoại tiếp tam giác có ba cạnh là bộ
    Pythagore (nhận ra tam giác vuông -> cạnh huyền là đường kính).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH033_SA_A, theo giao an Bai 6
    ("a = 6, b = 8, c = 10, tinh R"). Co Lan duyet.
    """
    BO = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20)]
    cau = ""
    for _ in range(socau):
        x, y, z = random.choice(BO)
        k = random.choice([1, 1, 2, 3])
        x, y, z = x * k, y * k, z * k
        canh = [("BC", x), ("CA", y), ("AB", z)]
        random.shuffle(canh)
        huyen = [t for t, v in canh if v == z][0]
        R = Rational(z, 2)
        dap = _so_thap_phan_gon(R)
        debai = (r"Given triangle $ABC$ with $%s = %d$, $%s = %d$, $%s = %d$. Find the circumradius $R$ of "
                 r"the triangle." % (canh[0][0], canh[0][1], canh[1][0], canh[1][1],
                                                      canh[2][0], canh[2][1]))
        giai = (r"We have $%d^{2} + %d^{2} = %d = %d^{2}$, so the triangle is right-angled and its hypotenuse is $%s = %d$.\\ "
                r"A right triangle inscribed in a circle has its hypotenuse as a diameter, so "
                r"$R = \dfrac{%d}{2} = %s$." % (x, y, z * z, z, huyen, z, z, dap))
        cau += MC_SA_answer_const(debai, dap, [str(z), _so_thap_phan_gon(Rational(x * y, 2 * z)) or "1",
                                               _so_thap_phan_gon(Rational(x + y + z, 2)) or "2"],
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_C_01(socau, dang=1):
    r"""Biết DIỆN TÍCH và hai cạnh, tìm góc xen giữa ($S = \dfrac12 bc\sin A$),
    có điều kiện góc nhọn / tù để chọn nghiệm.

    CLAUDE THEM 29/09/2026 - dang moi TH034_MC_C, theo giao an Bai 6 ("S =
    15 can 3, AB = 6, AC = 10, A tu"). Co Lan duyet.
    """
    SIN = {30: (Rational(1, 2), 150), 45: (sqrt(2) / 2, 135), 60: (sqrt(3) / 2, 120)}
    cauTN = ""
    for _ in range(socau):
        g, (sg, bu) = random.choice(list(SIN.items()))
        b, c = random.randint(3, 12), random.randint(3, 12)
        S = simplify(Rational(1, 2) * b * c * sg)
        tu = random.random() < 0.5
        A = bu if tu else g
        dung = "$%s$" % _goc(A)
        nhieu = ["$%s$" % _goc(x) for x in (bu if not tu else g, 90, 180 - 90 + (g if tu else bu) - 90)
                 if x != A]
        nhieu = _ba_nhieu(dung, nhieu + ["$%s$" % _goc(x) for x in (30, 45, 60, 120, 135, 150)])
        debai = (r"Triangle $ABC$ has $AB = %d$, $AC = %d$ and area $S = %s$. Given that angle $A$ is %s, "
                 r"the measure of angle $A$ is" % (c, b, _L(S), "obtuse" if tu else "acute"))
        giai = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A \Rightarrow %s = %s\sin A \Rightarrow "
                r"\sin A = %s$.\\ So $\widehat{A} = %s$ or $\widehat{A} = %s$. Since $A$ is %s, "
                r"$\widehat{A} = %s$."
                % (_L(S), _L(Rational(b * c, 2)), _L(sg), _goc(g), _goc(bu), "obtuse" if tu else "acute",
                   _goc(A)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_TL_A_02(socau, dong=1):
    r"""Tự luận: biết ba cạnh (Heron) - tính diện tích, bán kính đường tròn
    NGOẠI tiếp và đường cao.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH034_TL_A (_01: S roi r), theo
    vi du "a = 13, b = 14, c = 15" trong giao an Bai 6. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        a, b, c, S, p, r = random.choice([t for t in BANG_HERON if t[3] >= 12])
        ds3 = [a, b, c]
        random.shuffle(ds3)
        a, b, c = ds3
        R = Rational(a * b * c, 4 * S)
        ha = Rational(2 * S, a)
        debai = r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$." % (a, b, c)
        ds_abcd = [
            (r"Calculate the area of triangle $ABC$.", "%d" % S,
             r"$p = \dfrac{%d + %d + %d}{2} = %d$, $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
             % (a, b, c, p, p, p - a, p - b, p - c, S)),
            (r"Find the radius $R$ of the circumscribed circle of the triangle.", _L(R),
             r"$R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$." % (a, b, c, S, _L(R))),
            (r"Find the length of the altitude from vertex $A$.", _L(ha),
             r"$S = \dfrac{1}{2}\cdot BC\cdot h_a \Rightarrow h_a = \dfrac{2S}{BC} = \dfrac{%d}{%d} = %s$."
             % (2 * S, a, _L(ha))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH035_MC_C_02(socau, dang=1):
    r"""Nhận dạng tam giác: ba cạnh là bộ Pythagore - tam giác VUÔNG TẠI ĐỈNH
    NÀO (đỉnh đối diện cạnh lớn nhất).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH035_MC_C, theo giao an Bai 6
    ("a = 8, b = 15, c = 17"). Co Lan duyet.
    """
    BO = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29)]
    cauTN = ""
    for _ in range(socau):
        ba = list(random.choice(BO))
        random.shuffle(ba)
        a, b, c = ba
        z = max(ba)
        dinh = "ABC"[ba.index(z)]
        dung = r"The triangle has a right angle at $%s$" % dinh
        nhieu = [r"The triangle has a right angle at $%s$" % d for d in "ABC" if d != dinh] + [r"The triangle is obtuse"]
        debai = (r"Triangle $ABC$ has $a = %d$, $b = %d$, $c = %d$. Which of the following statements is "
                 r"\textbf{true}?" % (a, b, c))
        x, y = [v for v in ba if v != z]
        giai = (r"The longest side is $%s = %d$. We have $%d^{2} + %d^{2} = %d = %d^{2}$.\\ "
                r"By the law of cosines, $\cos %s = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = 0$ "
                r"so $\widehat{%s} = 90^{\circ}$: the triangle has a right angle at $%s$ (the vertex opposite the longest side)."
                % ("abc"[ba.index(z)], z, x, y, z * z, z, dinh, x, y, z, x, y, dinh, dinh))
        cauTN += MC_SA_answer_text(debai, dung, nhieu[:3], giai, 0, 0, dang)
    return cauTN


def L10_C3_TF_B_02(socau, socot=1):
    r"""Đúng/Sai - hệ thức lượng: biết $b$, $c$ và $\cos A$ (phân số): cạnh $a$,
    $\sin A$, diện tích, bán kính ngoại tiếp.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C3_TF_B, theo cau Dung/Sai
    "b = 5, c = 7, cos A = 3/5" trong giao an Bai 6. Co Lan duyet.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        while True:
            cA = random.choice([Rational(3, 5), Rational(-3, 5), Rational(4, 5), Rational(-4, 5)])
            b, c = random.randint(2, 9), random.randint(2, 9) * 5
            a2 = b * b + c * c - 2 * b * c * cA
            if a2.is_Integer and a2 > 0 and b != c:
                break
        sA = _sin_tu_cos(cA)
        a = sqrt(Integer(a2))
        S = simplify(Rational(1, 2) * b * c * sA)
        R = simplify(a / (2 * sA))
        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$ and $\cos A = %s$. Determine whether each "
                 r"of the following statements is true or false:" % (b, c, _L(cA)))
        # a) NB - sin A tu he thuc co ban (sin A > 0)
        ly_a = r"$\sin A = \sqrt{1 - \cos^{2}A} = %s$ (since $0^{\circ} < A < 180^{\circ}$, we have $\sin A > 0$)." % _L(sA)
        y1 = _tf_gop(_tf_ct(r"$\sin A = %s$", sA, ly_a, [(-sA, "$\\sin A$ is always positive"), (1 - abs(cA), "Forgot to square"), (sA ** 2, "Forgot to take the square root")]),
                     _tf_ct(r"$\sin^{2}A = %s$", sA ** 2, ly_a, [(1 + cA ** 2, "Sign error")]))
        # b) TH - dinh li cosin
        ly_b = r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %d$." % (
            b, c, b, c, (r"\left(%s\right)" % _L(cA)) if cA < 0 else _L(cA), a2)
        y2 = _tf_gop(_tf_ct(r"$BC = %s$", a, ly_b,
                            [(sqrt(Integer(b * b + c * c + 2 * b * c * cA)), "Sign error"), (sqrt(Integer(b * b + c * c)), "Omitted the term containing $\\cos A$"),
                             (sqrt(b * b + c * c - b * c * cA), "Forgot the factor 2")],
                            them=[r"$BC^{2} = %d$" % a2]))
        # c) VD - dien tich, khoang cach
        ly_c = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$; the distance from $B$ to $AC$ is "
                r"$\dfrac{2S}{AC} = AB\cdot\sin A = %s$." % (c, b, _L(sA), _L(S), _L(c * sA)))
        d1, s1 = _tf_ct(r"The area of triangle $ABC$ equals $%s$", S, ly_c,
                        [(2 * S, "Forgot the factor $\\dfrac{1}{2}$"), (abs(Rational(1, 2) * b * c * cA), "Confused $\\sin A$ with $\\cos A$"),
                         (Rational(1, 2) * b * c * sA ** 2, "Mistakenly using $\\sin^{2}A$")])
        d2, s2 = _tf_ct(r"The distance from $B$ to line $AC$ equals $%s$", c * sA, ly_c,
                        [(b * sA, "Used the wrong side"), (c * abs(cA), "Confused $\\sin A$ with $\\cos A$")])
        y3 = _phat_bieu(d1 + d2, s1 + s2)
        # d) VDC - ban kinh ngoai tiep (can BC tu y b)
        ly_d = ly_b + r" $R = \dfrac{BC}{2\sin A} = \dfrac{%s}{2\cdot %s} = %s$." % (_L(a), _L(sA), _L(R))
        d1, s1 = _tf_ct(r"The circumradius of the triangle equals $%s$", R, ly_d,
                        [(simplify(2 * R), "Forgot to divide by 2"), (simplify(a / (2 * abs(cA))), "Confused $\\sin A$ with $\\cos A$"),
                         (simplify(sqrt(Integer(b * b + c * c + 2 * b * c * cA)) / (2 * sA)), "Miscalculated $BC$ (sign error)")])
        d2, s2 = _tf_ct(r"The diameter of the circumcircle of the triangle equals $%s$", simplify(2 * R), ly_d,
                        [(R, "That is the radius"), (simplify(a / abs(cA)), "Confused $\\sin A$ with $\\cos A$")])
        y4 = _phat_bieu(d1 + d2, s1 + s2)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_E_02(socau, socot=1):
    r"""Đúng/Sai - định lí sin và diện tích trong tam giác VUÔNG có góc
    $30^{\circ}$ hoặc $60^{\circ}$.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C3_TF_E, theo cau "vuong tai
    B, A = 30, a = 5" trong giao an Bai 6. Co Lan duyet.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        A = random.choice([30, 60])
        a = random.randint(2, 12)
        sA = _gtlg("sin", A)
        R = simplify(a / (2 * sA))
        b = 2 * R                           # canh huyen AC
        C = 90 - A
        c = simplify(b * _gtlg("sin", C))
        S = simplify(Rational(1, 2) * a * c)
        debai = (r"Given triangle $ABC$ with a right angle at $B$, $\widehat{A} = %s$ and $BC = %d$. Determine "
                 r"whether each of the following statements is true or false:" % (_goc(A), a))
        # a) NB - tổng ba góc, cạnh huyền
        ly_a = r"$\widehat{C} = 180^{\circ} - 90^{\circ} - %s = %s$; the side opposite the right angle $B$ is the hypotenuse $AC$." % (_goc(A), _goc(C))
        y1 = _phat_bieu(
            [(r"$\widehat{C} = %s$" % _goc(C), ly_a), (r"$\widehat{A} + \widehat{C} = 90^{\circ}$", ly_a), (r"$AC$ is the hypotenuse", ly_a)],
            [(r"$\widehat{C} = %s$" % _goc(A), ly_a), (r"$\widehat{C} = %s$" % _goc(180 - A), ly_a), (r"$AB$ is the hypotenuse", ly_a),
             (r"$\widehat{A} + \widehat{C} = 180^{\circ}$", ly_a)])
        # b) TH - định lí sin
        ly_b = r"$R = \dfrac{BC}{2\sin A} = \dfrac{%d}{2\cdot %s} = %s$, $AC = 2R = %s$ (the hypotenuse is the diameter)." % (a, _L(sA), _L(R), _L(b))
        y2 = _tf_gop(_tf_ct(r"The circumradius $R = %s$", R, ly_b,
                            [(2 * R, "That is $2R$"), (simplify(a / (2 * _gtlg("cos", A))), "Confused $\\sin A$ with $\\cos A$"),
                             (simplify(a * sA / 2), "Mistakenly using $R = \\dfrac{BC\\cdot\\sin A}{2}$")]),
                     _tf_ct(r"$AC = %s$", b, ly_b, [(R, "Forgot to multiply by 2"), (Integer(a), "Used the wrong side")]))
        # c) VD - cạnh AB
        ly_c = r"$AC = 2R = %s$ (the hypotenuse is the diameter), $AB = 2R\sin C = %s$." % (_L(b), _L(c))
        y3 = _tf_gop(_tf_ct(r"$AB = %s$", c, ly_c,
                            [(simplify(b * _gtlg("sin", A)), "Mistakenly used angle $A$ (that gives $BC$)"), (b, "Took the hypotenuse"),
                             (simplify(a * _gtlg("tan", A)), "Mistakenly using $AB = BC\\cdot\\tan A$")],
                            them=[r"$AB^{2} = %s$" % _L(simplify(c ** 2))]))
        # d) VDC - diện tích, đường cao ứng với cạnh huyền
        hB = simplify(2 * S / b)
        ly_d = (r"The two legs are $BC$ and $AB$: $S = \dfrac{1}{2}\cdot %d\cdot %s = %s$; the altitude from $B$ is "
                r"$h = \dfrac{2S}{AC} = %s$." % (a, _L(c), _L(S), _L(hB)))
        y4 = _tf_gop(_tf_ct(r"The area of triangle $ABC$ equals $%s$", S, ly_d,
                            [(2 * S, "Forgot the factor $\\dfrac{1}{2}$"), (simplify(Rational(1, 2) * a * b), "Mistakenly used the hypotenuse"), (S / 2, "Divided by an extra factor of 2")]),
                     _tf_ct(r"The altitude from $B$ of triangle $ABC$ equals $%s$", hB, ly_d,
                            [(hB / 2, "Forgot to multiply by 2"), (simplify(2 * S / a), "Divided by the wrong side")]))
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_B6_VD036_TL_C_02(socau, dong=1):
    r"""Tự luận thực tế: rào mảnh đất tam giác biết hai cạnh và góc xen giữa -
    tính cạnh còn lại, chu vi và chi phí làm hàng rào, diện tích.

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD036_TL_C, theo bai "manh dat
    AB = 120 m, AC = 150 m, A = 70, rao 85 nghin/m" trong giao an Bai 6.
    Goc bat ki (may tinh cam tay), lam tron theo de. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        AB, AC = random.randrange(80, 201, 10), random.randrange(80, 201, 10)
        A = random.choice([50, 55, 65, 70, 75, 80, 100, 110])
        gia = random.choice([60, 75, 85, 90, 120])
        BC = math.sqrt(AB * AB + AC * AC - 2 * AB * AC * math.cos(math.radians(A)))
        BC1 = round(BC, 1)
        P = round(AB + AC + BC1, 1)
        tien = P * gia * 1000
        trieu = int(round(tien / 1e6))
        S = 0.5 * AB * AC * math.sin(math.radians(A))
        debai = (r"A triangular plot of land $ABC$ has $AB = %d\,\text{m}$, $AC = %d\,\text{m}$, "
                 r"$\widehat{A} = %s$. The entire plot is fenced along its three sides, and the cost of the "
                 r"fence is $%d$ thousand VND per meter." % (AB, AC, _goc(A), gia))
        ds_abcd = [
            (r"Calculate the length of side $BC$ (rounded to the nearest tenth of a meter).", r"%s\,\text{m}" % _xx(BC1, 1),
             r"By the law of cosines: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s \approx %s$, "
             r"so $BC \approx %s\,\text{m}$." % (AB, AC, AB, AC, _goc(A), _xx(BC * BC, 1), _xx(BC1, 1))),
            (r"Calculate the cost of the fence (rounded to the nearest million VND).", r"%d\ \text{million VND}" % trieu,
             r"Perimeter $P \approx %d + %d + %s = %s\,\text{m}$.\\ Cost $\approx %s\cdot %d\,000 "
             r"\approx %d$ million VND." % (AB, AC, _xx(BC1, 1), _xx(P, 1), _xx(P, 1), gia, trieu)),
            (r"Calculate the area of the plot (rounded to the nearest square meter).",
             r"%d\,\text{m}^{2}" % int(round(S)),
             r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s "
             r"\approx %d\,\text{m}^{2}$." % (AB, AC, _goc(A), int(round(S)))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN



# ---------------------------------------------------------------------
# BÀI 6 - ĐỢT 2 (giáo án "Hệ thức lượng trong tam giác. Giải tam giác")
# CLAUDE THEM 29/09/2026 - co Lan duyet lai. Cau chung minh / bien doi he
# thuc (muc VD, VDC) KHONG dua vao vi curriculum Bai 6 chi co TH va VD thuc
# tien; rieng cau "he thuc giua cac canh -> goc" duoc HA xuong TH (TH032_MC_D).
# ---------------------------------------------------------------------

def _huong_sang_phuong_vi(huong):
    r"""Góc (độ) tính từ hướng bắc theo chiều kim đồng hồ -> (chữ trong đề,
    chữ giải thích cách đổi). Góc là bội của 5, nằm trong [0; 360)."""
    huong %= 360
    ten = {0: "north", 90: "east", 180: "south", 270: "west"}
    if huong in ten:
        return (r"heading %s" % ten[huong],
                r"heading %s corresponds to $%d^{\circ}$" % (ten[huong], huong))
    if huong < 90:
        x, kh, doi = huong, r"\mathrm{N}\,%d^{\circ}\,\mathrm{E}", r"%d^{\circ}"
        doi = doi % x
    elif huong < 180:
        x, kh = 180 - huong, r"\mathrm{S}\,%d^{\circ}\,\mathrm{E}"
        doi = r"180^{\circ} - %d^{\circ} = %d^{\circ}" % (x, huong)
    elif huong < 270:
        x, kh = huong - 180, r"\mathrm{S}\,%d^{\circ}\,\mathrm{W}"
        doi = r"180^{\circ} + %d^{\circ} = %d^{\circ}" % (x, huong)
    else:
        x, kh = 360 - huong, r"\mathrm{N}\,%d^{\circ}\,\mathrm{W}"
        doi = r"360^{\circ} - %d^{\circ} = %d^{\circ}" % (x, huong)
    kh = kh % x
    return r"heading $%s$" % kh, r"$%s$ corresponds to $%s$" % (kh, doi)


def _hai_chang(h1, d1, h2, d2):
    r"""Tàu đi $d_1$ theo hướng h1 (A -> B) rồi $d_2$ theo hướng h2 (B -> C).
    Trả về (Delta, goc B, AC, goc BAC, huong AC, re_phai). Delta là góc đổi
    hướng (0 < Delta < 180); $\widehat{ABC} = 180^{\circ} - \Delta$."""
    u = lambda h: (math.sin(math.radians(h)), math.cos(math.radians(h)))
    Bx, By = d1 * u(h1)[0], d1 * u(h1)[1]
    Cx, Cy = Bx + d2 * u(h2)[0], By + d2 * u(h2)[1]
    lech = (h2 - h1) % 360
    re_phai = lech < 180
    delta = lech if re_phai else 360 - lech
    AC = math.hypot(Cx, Cy)
    cos_A = (d1 * d1 + AC * AC - d2 * d2) / (2 * d1 * AC)
    gA = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
    hAC = math.degrees(math.atan2(Cx, Cy)) % 360
    return delta, 180 - delta, AC, gA, hAC, re_phai


def _giai_goc_doi_huong(h1, h2, delta):
    """Đoạn lời giải: đổi hai hướng ra góc từ hướng bắc rồi suy ra góc B."""
    _, g1 = _huong_sang_phuong_vi(h1)
    _, g2 = _huong_sang_phuong_vi(h2)
    a1, a2 = h1 % 360, h2 % 360
    lon, nho = max(a1, a2), min(a1, a2)
    if lon - nho <= 180:
        tinh = r"%d^{\circ} - %d^{\circ} = %d^{\circ}" % (lon, nho, delta)
    else:
        tinh = r"360^{\circ} - (%d^{\circ} - %d^{\circ}) = %d^{\circ}" % (lon, nho, delta)
    return (r"Convert the headings to angles measured clockwise from north: %s; %s. "
            r"At $B$ the ship changed direction by an angle of $%s$, so "
            r"$\widehat{ABC} = 180^{\circ} - %d^{\circ} = %d^{\circ}$."
            % (g1, g2, tinh, delta, 180 - delta))


def _cong_goc(h, g):
    """Chuỗi phép tính h + g (g có thể âm) quy về [0; 360) độ."""
    kq = h + g
    s = r"%d^{\circ} %s %d^{\circ}" % (h, "+" if g >= 0 else "-", abs(g))
    if kq < 0:
        s += r" + 360^{\circ}"
    elif kq >= 360:
        s += r" - 360^{\circ}"
    return s + r" = %d^{\circ}" % (kq % 360)


def _chon_hai_chang():
    """Chọn h1, h2 (bội của 5) với góc đổi hướng 30..90 độ -> B tù hoặc vuông,
    hai góc A, C chắc chắn nhọn (dùng định lí sin không phải xét hai nghiệm)."""
    while True:
        h1 = random.choice([x for x in range(5, 360, 5) if x % 90])
        delta = random.choice([30, 40, 45, 50, 60, 70, 80])
        h2 = (h1 + random.choice([1, -1]) * delta) % 360
        return h1, h2


def L10_C3_B6_TH032_TL_A_02(socau, dong=1):
    r"""Tự luận: định lí côsin - biết $b$, $c$ và $\cos A$ là PHÂN SỐ, tính
    cạnh $a$ rồi côsin hai góc còn lại.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH032_TL_A, theo vi du "b = 5,
    c = 7, cos A = 3/5" trong giao an Bai 6. Co Lan duyet.
    """
    from sympy import radsimp
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        cA = random.choice(_COS_PHAN_SO)
        b = cA.q * random.randint(1, 2) if cA.q > 3 else random.randint(2, 9)
        c = random.randint(2, 12)
        a2 = b * b + c * c - 2 * b * c * cA
        if not a2.is_Integer or a2 <= 0 or b == c or (b, c, cA) in gt:
            continue
        gt.append((b, c, cA))
    cauTN = ""
    for b, c, cA in gt:
        a2 = Integer(b * b + c * c - 2 * b * c * cA)
        a = sqrt(a2)
        cB = radsimp((a2 + c * c - b * b) / (2 * c * a))
        cC = radsimp((a2 + b * b - c * c) / (2 * b * a))
        cA_ = (r"\left(%s\right)" % _L(cA)) if cA < 0 else _L(cA)
        debai = (r"Given triangle $ABC$ with $AC = %d$, $AB = %d$ and $\cos A = %s$." % (b, c, _L(cA)))
        ds_abcd = [
            (r"Calculate the length of side $BC$.", _L(a),
             r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A = %d^{2} + %d^{2} - "
             r"2\cdot %d\cdot %d\cdot %s = %d$, so $BC = %s$." % (b, c, b, c, cA_, a2, _L(a))),
            (r"Calculate $\cos B$.", _L(cB),
             r"$\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} = "
             r"\dfrac{%d + %d - %d}{2\cdot %s\cdot %d} = %s$." % (a2, c * c, b * b, _L(a), c, _L(cB))),
            (r"Find $\cos C$.", _L(cC),
             r"$\cos C = \dfrac{BC^{2} + AC^{2} - AB^{2}}{2\cdot BC\cdot AC} = "
             r"\dfrac{%d + %d - %d}{2\cdot %s\cdot %d} = %s$." % (a2, b * b, c * c, _L(a), b, _L(cC))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH032_MC_B_02(socau, dang=1):
    r"""Biết ba cạnh, tính côsin của góc có số đo LỚN NHẤT (phải nhận ra góc
    đối diện cạnh dài nhất rồi dùng định lí côsin).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH032_MC_B, theo vi du "BC = 3,
    CA = 4, AB = 6" trong giao an Bai 6. Co Lan duyet.
    """
    cauTN = ""
    lan = 0
    so = 0
    while so < socau and lan < 500:
        lan += 1
        x, y, z = sorted(random.sample(range(3, 16), 3))
        if x + y <= z:
            continue
        dinh = random.sample("ABC", 3)            # dinh[2] đối diện cạnh dài nhất
        canh = {dinh[0]: x, dinh[1]: y, dinh[2]: z}
        ten = {"A": "BC", "B": "CA", "C": "AB"}
        cos_lon = Rational(x * x + y * y - z * z, 2 * x * y)
        cos_nho = Rational(y * y + z * z - x * x, 2 * y * z)
        dung = "$%s$" % _L(cos_lon)
        nhieu = _ba_nhieu(dung, ["$%s$" % _L(cos_nho), "$%s$" % _L(-cos_lon),
                                 "$%s$" % _L(Rational(x * x + y * y + z * z, 2 * x * y))],
                          buoc=lambda t: "$%s$" % _L(cos_lon + Rational(t, 2 * x * y)))
        debai = (r"Given triangle $ABC$ with $BC = %d$, $CA = %d$ and $AB = %d$. The cosine of the largest "
                 r"angle of the triangle is" % (canh["A"], canh["B"], canh["C"]))
        giai = (r"The longest side is $%s = %d$, so the largest angle is angle $%s$ (opposite that side).\\ "
                r"$\cos %s = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$."
                % (ten[dinh[2]], z, dinh[2], dinh[2], x, y, z, x, y, _L(cos_lon)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
        so += 1
    return cauTN


# (k, số đo góc) với b^2 + c^2 - a^2 = k.bc  <=>  cos A = k/2
_HE_SO_GOC = [(Integer(1), 60), (Integer(-1), 120), (sqrt(2), 45), (-sqrt(2), 135),
              (sqrt(3), 30), (-sqrt(3), 150), (Integer(0), 90)]
_BA_DINH = {"A": ("a", "b", "c"), "B": ("b", "c", "a"), "C": ("c", "a", "b")}


def _he_so_tex(k, hai_canh):
    """k.xy viết gọn: 1 -> 'bc', -1 -> '-bc', sqrt(2) -> '\\sqrt{2}bc'."""
    if k == 1:
        return hai_canh
    if k == -1:
        return "-" + hai_canh
    if k.is_Add:
        return r"\left(%s\right)%s" % (_L(k), hai_canh)
    return _L(k) + hai_canh


def _cau_he_thuc_goc(socau, dang, dang_nhan_tu, tra_loi_ngan=False):
    """tra_loi_ngan=True (CLAUDE THEM 15/10/2026): ban tra loi ngan cung dang (TH032_SA_D) - hoi so do goc bang bao
    nhieu do, dap so la so nguyen; phan sinh so lieu va loi giai giu nguyen nhu ban trac nghiem."""
    cauTN = ""
    for _ in range(socau):
        k, g = random.choice(_HE_SO_GOC)
        X = random.choice("ABC")
        duoi = (r" What is the measure of angle $%s$ in degrees?" % X) if tra_loi_ngan else (r" The measure of angle $%s$ is" % X)
        d, u, v = _BA_DINH[X]                     # d đối diện góc X
        uv = u + v if u < v else v + u
        u, v = sorted([u, v])
        if dang_nhan_tu:
            he = simplify(2 + k)
            ve = _he_so_tex(he, uv) if he != 0 else "0"
            debai = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$ satisfying $(%s + %s + %s)(%s + %s - %s) = %s$." % (u, v, d, u, v, d, ve)) + duoi
            buoc1 = (r"The left side equals $(%s + %s)^{2} - %s^{2} = %s^{2} + %s^{2} + 2%s - %s^{2}$, so "
                     r"$%s^{2} + %s^{2} - %s^{2} = %s$.\\ "
                     % (u, v, d, u, v, uv, d, u, v, d, _he_so_tex(k, uv) if k != 0 else "0"))
        else:
            dang_viet = random.choice([0, 1])
            if dang_viet == 0 and k != 0:
                ve = _he_so_tex(-k, uv)
                ve = ("+ " + ve) if not ve.startswith("-") else ("- " + ve[1:])
                debai = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$ satisfying $%s^{2} = %s^{2} + %s^{2} %s$." % (d, u, v, ve)) + duoi
            else:
                ve = _he_so_tex(k, uv) if k != 0 else "0"
                debai = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$ satisfying $%s^{2} + %s^{2} - %s^{2} = %s$." % (u, v, d, ve)) + duoi
            buoc1 = (r"From the given condition: $%s^{2} + %s^{2} - %s^{2} = %s$.\\ "
                     % (u, v, d, _he_so_tex(k, uv) if k != 0 else "0"))
        giai = (buoc1 + r"By the corollary of the law of cosines: $\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s} "
                r"= %s$, so $\widehat{%s} = %s$." % (X, u, v, d, uv, _L(k / 2), X, _goc(g)))
        dung = "$%s$" % _goc(g)
        khac = [x for _, x in _HE_SO_GOC if x not in (g, 180 - g)]
        random.shuffle(khac)
        ung = ([] if g == 90 else ["$%s$" % _goc(180 - g)]) + ["$%s$" % _goc(x) for x in khac]
        if tra_loi_ngan:
            ung_so = ([] if g == 90 else [str(180 - g)]) + [str(x) for x in khac]
            cauTN += MC_SA_answer_const(debai, str(g), _ba_nhieu(str(g), ung_so), giai, 0, 0, dang)
            continue
        cauTN += MC_SA_answer_text(debai, dung, _ba_nhieu(dung, ung), giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH032_MC_D_01(socau, dang=1):
    r"""Từ hệ thức giữa các cạnh ($a^2 = b^2 + c^2 - k\,bc$...) suy ra số đo
    một góc bằng hệ quả định lí côsin.

    CLAUDE THEM 29/09/2026 - dang MOI, ha muc tu cac cau "a^2 = (a^3 - b^3 -
    c^3)/(a - b - c)" trong giao an Bai 6 (ban goc la VD, curriculum Bai 6
    khong co VD thuan tuy nen chi giu buoc mot, hai buoc). Co Lan duyet.
    """
    return _cau_he_thuc_goc(socau, dang, dang_nhan_tu=False)


def L10_C3_B6_TH032_MC_D_02(socau, dang=1):
    r"""Như _01 nhưng hệ thức cho dưới dạng tích $(b + c + a)(b + c - a) = k\,bc$
    (theo ví dụ "$(a + b + c)(a + b - c) = (2 + \sqrt{2})ab$" trong giáo án).

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH032_MC_D. Co Lan duyet.
    """
    return _cau_he_thuc_goc(socau, dang, dang_nhan_tu=True)


def L10_C3_B6_TH033_TL_A_02(socau, dong=1):
    r"""Tự luận: biết một cạnh và HAI GÓC KỀ cạnh đó (góc $A$ phải tự tính),
    dùng định lí sin tính một cạnh khác và bán kính $R$.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH033_TL_A, theo vi du "B = 45,
    C = 75, BC = 5" trong giao an Bai 6. Co Lan duyet.
    """
    BO = [(60, 45), (45, 60), (120, 30), (30, 45), (45, 30), (135, 30), (30, 60), (60, 30),
          (30, 120), (45, 105)]
    cauTN = ""
    for _ in range(socau):
        A, B = random.choice([x for x in BO if x[1] in (30, 45, 60)])
        C = 180 - A - B
        a = random.randint(3, 12)
        sA, sB = _gtlg("sin", A), _gtlg("sin", B)
        b = simplify(a * sB / sA)
        R = simplify(a / (2 * sA))
        debai = (r"Given triangle $ABC$ with $BC = %d$, $\widehat{B} = %s$ and $\widehat{C} = %s$."
                 % (a, _goc(B), _goc(C)))
        ds_abcd = [
            (r"Find the measure of angle $A$.", _goc(A),
             r"$\widehat{A} = 180^{\circ} - \left(%s + %s\right) = %s$." % (_goc(B), _goc(C), _goc(A))),
            (r"Calculate the length of side $AC$.", _L(b),
             r"Law of sines: $\dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$, so "
             r"$AC = \dfrac{BC\cdot\sin B}{\sin A} = \dfrac{%d\cdot %s}{%s} = %s$."
             % (a, _L(sB), _L(sA), _L(b))),
            (r"Calculate the circumradius $R$ of triangle $ABC$.", _L(R),
             r"$\dfrac{BC}{\sin A} = 2R$, so $R = \dfrac{%d}{2\cdot %s} = %s$." % (a, _L(sA), _L(R))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_NB034_MC_B_02(socau, dang=1):
    r"""Chọn công thức diện tích ĐÚNG (hoặc SAI) trong bốn công thức.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH034_MC_A, theo cac cau nhan
    dang cong thuc trong phan trac nghiem giao an Bai 6. Co Lan duyet.
    """
    DUNG = [r"$S = \dfrac{1}{2}ab\sin C$", r"$S = \dfrac{1}{2}bc\sin A$", r"$S = \dfrac{1}{2}ca\sin B$",
            r"$S = \dfrac{abc}{4R}$", r"$S = pr$", r"$S = \sqrt{p(p-a)(p-b)(p-c)}$",
            r"$S = \dfrac{1}{2}a\cdot h_a$", r"$S = \dfrac{1}{2}b\cdot h_b$"]
    SAI = [(r"$S = \dfrac{1}{2}ab\sin A$", r"the angle in the formula must be the angle INCLUDED between sides $a$ and $b$, that is, angle $C$"),
           (r"$S = \dfrac{1}{2}bc\cos A$", r"it must be $\sin A$, not $\cos A$"),
           (r"$S = \dfrac{abc}{2R}$", r"the correct formula is $\dfrac{abc}{4R}$"),
           (r"$S = \dfrac{abc}{R}$", r"the correct formula is $\dfrac{abc}{4R}$"),
           (r"$S = 2pr$", r"$p$ is HALF the perimeter, so $S = pr$"),
           (r"$S = \sqrt{p(p+a)(p+b)(p+c)}$", r"Heron's formula is $\sqrt{p(p-a)(p-b)(p-c)}$"),
           (r"$S = a\cdot h_a$", r"the factor $\dfrac{1}{2}$ is missing"),
           (r"$S = \dfrac{1}{2}ab\sin B$", r"the angle included between sides $a$ and $b$ is angle $C$")]
    cauTN = ""
    for _ in range(socau):
        hoi_sai = random.choice([True, False])
        if hoi_sai:
            sai, ly_do = random.choice(SAI)
            dung, nhieu = sai, random.sample(DUNG, 3)
            debai = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$, area $S$, semiperimeter $p$, "
                     r"and circumradius and inradius $R$ and $r$, respectively. Which of the following "
                     r"formulas is \textbf{false}?")
            giai = r"Formula %s is false because %s. The other three formulas are all true." % (sai, ly_do)
        else:
            dung = random.choice(DUNG)
            ba = random.sample(SAI, 3)
            nhieu = [x[0] for x in ba]
            debai = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$, area $S$, semiperimeter $p$, "
                     r"and circumradius and inradius $R$ and $r$, respectively. Which of the following "
                     r"formulas is true?")
            giai = (r"%s is a true formula. The other formulas are false: " % dung
                    + "; ".join(r"%s: %s" % x for x in ba) + ".")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_TF_E_03(socau, socot=1):
    r"""Đúng/Sai - biết hai cạnh và góc xen giữa: diện tích, đường cao, cạnh
    thứ ba, bán kính ngoại tiếp.

    CLAUDE THEM 29/09/2026 - bien the 03 cua L10_C3_TF_E, theo vi du "a = 2can3,
    b = 2, C = 30" trong giao an Bai 6. Co Lan duyet.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        C = random.choice([30, 60, 120, 150])
        m = random.randint(2, 8)
        if C in (30, 150):
            k = random.randint(1, 5)
            a = k * sqrt(3)
        else:
            a = Integer(random.randint(2, 9))
            while a == m:
                a = Integer(random.randint(2, 9))
        b = Integer(m)
        sC, cC = _gtlg("sin", C), _gtlg("cos", C)
        S = simplify(a * b * sC / 2)
        ha = simplify(2 * S / a)
        c2 = simplify(a ** 2 + b ** 2 - 2 * a * b * cC)
        c = sqrt(c2)
        c2_sai = simplify(a ** 2 + b ** 2 + 2 * a * b * cC)
        R = simplify(c / (2 * sC))
        debai = (r"Given triangle $ABC$ with $BC = %s$, $CA = %d$ and $\widehat{C} = %s$. Determine whether each "
                 r"of the following statements is true or false:" % (_L(a), m, _goc(C)))
        cC_ = (r"\left(%s\right)" % _L(cC)) if cC < 0 else _L(cC)
        # a) NB - công thức diện tích hai cạnh, góc xen giữa
        ly_a = r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\sin C = \dfrac{1}{2}\cdot %s\cdot %d\cdot %s = %s$." % (_L(a), m, _L(sC), _L(S))
        d1, s1 = _tf_ct(r"The area of triangle $ABC$ equals $%s$", S, ly_a,
                        [(2 * S, "Forgot the factor $\\dfrac{1}{2}$"), (simplify(abs(a * b * cC) / 2), "Confused $\\sin C$ with $\\cos C$")],
                        them=[r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\sin C$"])
        s1.append((r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\cos C$", ly_a))
        s1.append((r"$S = BC\cdot CA\cdot\sin C$", ly_a))
        y1 = _phat_bieu(d1, s1)
        # b) TH - đường cao
        ly_b = r"$h_a = \dfrac{2S}{BC} = \dfrac{2\cdot %s}{%s} = %s$ (also equal to $CA\cdot\sin C$)." % (_L(S), _L(a), _L(ha))
        y2 = _tf_gop(_tf_ct(r"The altitude from $A$ has length $h_a = %s$", ha, ly_b,
                            [(simplify(S / a), "Forgot to multiply by 2"), (simplify(2 * S / b), "Divided by the wrong side $CA$"), (simplify(b * abs(cC)), "Confused $\\sin$ with $\\cos$")],
                            them=[r"$h_a = CA\cdot\sin C$"]))
        # c) VD - định lí côsin
        ly_c = (r"$AB^{2} = BC^{2} + CA^{2} - 2\cdot BC\cdot CA\cdot\cos C = %s + %d - 2\cdot %s\cdot %d"
                r"\cdot %s = %s$, so $AB = %s$." % (_L(a ** 2), m * m, _L(a), m, cC_, _L(c2), _L(c)))
        y3 = _tf_gop(_tf_ct(r"$AB = %s$", c, ly_c,
                            [(sqrt(c2_sai), "Sign mistake"), (sqrt(simplify(a ** 2 + b ** 2)), "Omitted the term containing $\\cos C$"),
                             (sqrt(simplify(a ** 2 + b ** 2 - a * b * cC)), "Forgot the factor 2")],
                            them=[r"$AB^{2} = %s$" % _L(c2)]))
        # d) VDC - bán kính ngoại tiếp
        ly_d = ly_c + r" Law of sines: $\dfrac{AB}{\sin C} = 2R$, so $R = \dfrac{%s}{2\cdot %s} = %s$." % (_L(c), _L(sC), _L(R))
        y4 = _tf_gop(_tf_ct(r"The circumradius of triangle $ABC$ equals $%s$", R, ly_d,
                            [(simplify(2 * R), "Forgot to divide by 2"), (simplify(c / (2 * abs(cC))), "Confused $\\sin C$ with $\\cos C$"),
                             (simplify(sqrt(c2_sai) / (2 * sC)), "Miscalculated $AB$ (sign error)")]),
                     _tf_ct(r"The diameter of the circumscribed circle of triangle $ABC$ equals $%s$", simplify(2 * R), ly_d, [(R, "That is the radius")]))
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_C_02(socau, socot=1):
    r"""Đúng/Sai - tàu chạy hai chặng theo hướng la bàn (N..E, S..W...):
    góc tại điểm đổi hướng, khoảng cách, góc $\widehat{BAC}$, hướng từ $A$ tới $C$.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C3_TF_C, theo bai "N24E 50 km
    roi N36W 130 km" trong giao an Bai 6. Khac _01: cho quang duong (khong cho
    van toc) va hai huong bat ki. Co Lan duyet.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    so = 0
    while so < socau:
        h1, h2 = _chon_hai_chang()
        d1, d2 = random.randrange(20, 101, 5), random.randrange(30, 151, 10)
        delta, B, AC, gA, _, re_phai = _hai_chang(h1, d1, h2, d2)
        gA_n = int(round(gA))
        if abs(gA - gA_n) > 0.4 or gA_n == 0:
            continue
        hAC = (h1 + gA_n) % 360 if re_phai else (h1 - gA_n) % 360
        if hAC % 90 == 0:
            continue
        so += 1
        t1, _ = _huong_sang_phuong_vi(h1)
        t2, _ = _huong_sang_phuong_vi(h2)
        tAC, _ = _huong_sang_phuong_vi(hAC)
        debai = (r"A fishing boat departs from island $A$, travels $%d\,\text{km}$ %s to island $B$, then switches "
                 r"to %s and continues for $%d\,\text{km}$ to fishing ground $C$. Determine whether each of the "
                 r"following statements is true or false:" % (d1, t1, t2, d2))
        g_B = _giai_goc_doi_huong(h1, h2, delta)
        cB = math.cos(math.radians(B))
        sinA = d2 * math.sin(math.radians(B)) / AC
        # a) NB - đọc góc đổi hướng, góc ABC
        x1, x2 = _n2_lech_truc(h1), _n2_lech_truc(h2)
        sai = [(r"$\widehat{ABC} = %s$" % _goc(delta), "That is the turning angle. " + g_B)]
        for g in (x1 + x2, abs(x1 - x2), 180 - x1 - x2):
            if 0 < g < 180 and g != B:
                sai.append((r"$\widehat{ABC} = %s$" % _goc(g), g_B))
        if delta != 180 - delta:
            sai.append((r"At $B$ the ship changes direction by an angle of $%s$" % _goc(180 - delta), g_B))
        y1 = _phat_bieu([(r"$\widehat{ABC} = %s$" % _goc(B), g_B), (r"At $B$ the ship changes direction by an angle of $%s$" % _goc(delta), g_B)], sai)
        # b) TH - định lí côsin
        giai_AC = r"Law of cosines: $AC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s$." % (d1, d2, d1, d2, _goc(B))
        y2 = _tf_gop(_tf_so(r"The distance $AC \approx %s$", AC, 1, giai_AC,
                            [(math.sqrt(d1 * d1 + d2 * d2 + 2 * d1 * d2 * cB), "Sign error"), (math.sqrt(d1 * d1 + d2 * d2), "Forgot the term containing $\\cos B$"),
                             (math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * math.cos(math.radians(delta))), "Mistakenly used the turning angle")],
                            dv=r"\,\text{km}", bdt=r"The distance $AC$ is %s $%s$"))
        # c) VD - định lí sin tìm góc BAC
        giai_A = (giai_AC + r" Law of sines: $\sin\widehat{BAC} = \dfrac{BC\cdot\sin B}{AC} \approx %s$; since angle $B$ is not acute, "
                  r"$\widehat{BAC}$ is acute." % _xx(sinA, 4))
        y3 = _tf_gop(_tf_so(r"$\widehat{BAC} \approx %s$", gA, 0, giai_A,
                            [(180 - B - gA, "That is angle $C$"), (180 - gA, "Mistakenly took the obtuse-angle solution"),
                             (90 - gA, "Confused $\\sin$ with $\\cos$ on the calculator")],
                            dv=r"^{\circ}", bdt=r"$\widehat{BAC}$ %s $%s$"))
        # d) VDC - hướng từ A đến C
        phia = "right" if re_phai else "left"
        giai_h = (r"The ship turns %s at $B$, so $C$ lies off to the %s side of ray $AB$: the heading of $AC$ corresponds to "
                  r"$%s$ (measured clockwise from north), that is, %s."
                  % (phia, phia, _cong_goc(h1, gA_n if re_phai else -gA_n), tAC))
        dung = [(r"The heading from $A$ to $C$ is %s" % tAC[8:], giai_h),
                (r"The heading from $A$ to $C$ makes an angle of $%s$ with north (measured clockwise)" % _goc(hAC), giai_h)]
        sai = []
        for hs, ghi in (((h1 - gA_n) % 360 if re_phai else (h1 + gA_n) % 360, "Deviated to the wrong side"), (h2 % 360, "That is the heading of the second leg"),
                        (h1 % 360, "That is the heading of the first leg"), ((hAC + 180) % 360, "That is the heading from $C$ back to $A$")):
            if hs % 90 and hs != hAC:
                ts, _ = _huong_sang_phuong_vi(hs)
                sai.append((r"The heading from $A$ to $C$ is %s" % ts[8:], ghi + ". " + giai_h))
        sai.append((r"The heading from $A$ to $C$ makes an angle of $%s$ with north (measured clockwise)" % _goc((360 - hAC) % 360),
                    "Measured counterclockwise. " + giai_h))
        y4 = _phat_bieu(dung, sai)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(r"Angle $\widehat{ABC}$ is an obtuse angle", g_B), (r"$\widehat{ABC} + %s = 180^{\circ}$" % _goc(delta), g_B)],
                 [(r"Angle $\widehat{ABC}$ is an acute angle", g_B), (r"$\widehat{ABC} + %s = 90^{\circ}$" % _goc(delta), g_B)])
        _bac = hAC < 90 or hAC > 270
        _dong = hAC < 180
        _tf_them(y4, [(r"Fishing ground $C$ lies to the %s of island $A$" % ("north" if _bac else "south"), giai_h),
                      (r"Fishing ground $C$ lies to the %s of island $A$" % ("east" if _dong else "west"), giai_h)],
                 [(r"Fishing ground $C$ lies to the %s of island $A$" % ("south" if _bac else "north"), giai_h),
                  (r"Fishing ground $C$ lies to the %s of island $A$" % ("west" if _dong else "east"), giai_h)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_B6_VD036_MC_C_02(socau, dang=1):
    r"""Hai phương tiện cùng xuất phát từ một điểm, đi theo HAI HƯỚNG LA BÀN
    khác nhau; sau một thời gian cách nhau bao xa (định lí côsin).

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD036_MC_C, theo bai "hai may bay:
    450 km/h huong tay, 630 km/h huong N25W, sau 90 phut" trong giao an Bai 6.
    Co Lan duyet.
    """
    BOI_CANH = [("Two airplanes take off from the same airport $O$", "airplane", "km/h", "km",
                 list(range(300, 901, 50)), [30, 45, 60, 90, 120]),
                ("Two ships leave port $O$ at the same time", "ship", "km/h", "km",
                 list(range(20, 61, 5)), [60, 90, 120, 150, 180])]
    cauTN = ""
    so = 0
    while so < socau:
        mo, ten, dv_v, dv, V, T = random.choice(BOI_CANH)
        h1 = random.choice([x for x in range(0, 360, 5)])
        goc = random.choice([35, 40, 50, 55, 65, 70, 75, 80, 100, 110, 115, 125])
        h2 = (h1 + random.choice([1, -1]) * goc) % 360
        v1, v2 = random.sample(V, 2)
        t = random.choice(T)
        d1, d2 = v1 * t / 60, v2 * t / 60
        cg = math.cos(math.radians(goc))
        kc = math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * cg)
        dung = "$%d\\,\\text{%s}$" % (int(round(kc)), dv)
        ung = [math.sqrt(v1 * v1 + v2 * v2 - 2 * v1 * v2 * cg),       # quên nhân thời gian
               math.sqrt(d1 * d1 + d2 * d2 + 2 * d1 * d2 * cg),       # nhầm dấu
               math.sqrt(d1 * d1 + d2 * d2)]                          # coi như vuông
        nhieu = _ba_nhieu(dung, ["$%d\\,\\text{%s}$" % (int(round(x)), dv) for x in ung],
                          buoc=lambda k: "$%d\\,\\text{%s}$" % (int(round(kc)) + 7 * k, dv))
        so += 1
        t1, g1 = _huong_sang_phuong_vi(h1)
        t2, g2 = _huong_sang_phuong_vi(h2)
        tg = ("%d min" % t) if t < 60 or t % 60 else ("%d h" % (t // 60))
        debai = (r"%s. The first one travels %s at a speed of $%d$ %s, and the second travels %s at a speed "
                 r"of $%d$ %s. After %s, about how many kilometers apart are the two %ss (rounded to the nearest "
                 r"whole number)? Assume the two %ss move in straight lines at constant speed, at the same altitude."
                 % (mo, t1, v1, dv_v, t2, v2, dv_v, tg, ten, ten))
        a1, a2 = h1 % 360, h2 % 360
        lon, nho = max(a1, a2), min(a1, a2)
        tinh = (r"%d^{\circ} - %d^{\circ} = %d^{\circ}" % (lon, nho, goc) if lon - nho <= 180 else
                r"360^{\circ} - (%d^{\circ} - %d^{\circ}) = %d^{\circ}" % (lon, nho, goc))
        giai = (r"After %s: $OA = %d\cdot\dfrac{%d}{60} = %s\,\text{km}$, $OB = %d\cdot\dfrac{%d}{60} = "
                r"%s\,\text{km}$.\\ Convert the headings to angles measured clockwise from north: %s; %s, "
                r"so $\widehat{AOB} = %s$.\\ Law of cosines: $AB^{2} = OA^{2} + OB^{2} - 2\cdot OA\cdot OB\cdot"
                r"\cos %s \approx %s$, hence $AB \approx %s\,\text{km}$."
                % (tg, v1, t, _xx(d1, 2), v2, t, _xx(d2, 2), g1, g2, tinh, _goc(goc),
                   _xx(kc * kc, 1), _xx(kc, 1)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_TL_D_02(socau, dong=1):
    r"""Tự luận: tàu chạy hai chặng theo HƯỚNG LA BÀN (cho vận tốc, thời gian):
    góc tại điểm đổi hướng, khoảng cách tới đích, hướng từ cảng tới đích.

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD036_TL_D, theo bai "tau ca S60E
    80 km/h trong 2 gio, hong may troi huong nam 7 km/h trong 90 phut" va "tau
    du lich N80E roi E20S" trong giao an Bai 6. Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        h1, h2 = _chon_hai_chang()
        v1, t1 = random.choice([(20, 30), (30, 40), (40, 90), (60, 30), (80, 120), (50, 60), (45, 40)])
        v2, t2 = random.choice([(20, 36), (7, 90), (10, 60), (30, 30), (24, 45), (40, 45), (15, 120)])
        d1, d2 = v1 * t1 / 60, v2 * t2 / 60
        delta, B, AC, gA, _, re_phai = _hai_chang(h1, d1, h2, d2)
        gA_n = int(round(gA))
        if abs(gA - gA_n) > 0.4 or gA_n == 0:
            continue
        hAC = (h1 + gA_n) % 360 if re_phai else (h1 - gA_n) % 360
        if hAC % 90 == 0:
            continue
        so += 1
        tt1, _ = _huong_sang_phuong_vi(h1)
        tt2, _ = _huong_sang_phuong_vi(h2)
        tAC, _ = _huong_sang_phuong_vi(hAC)
        sinA = d2 * math.sin(math.radians(B)) / AC
        phia = "right" if re_phai else "left"
        debai = (r"A ship departs from port $A$ and travels %s at a speed of $%d\,\text{km/h}$. After $%d$ minutes "
                 r"the ship reaches $B$ and switches to %s, traveling at a speed of $%d\,\text{km/h}$ for a further $%d$ minutes "
                 r"to reach island $C$." % (tt1, v1, t1, tt2, v2, t2))
        ds_abcd = [
            (r"Find the distances $AB$, $BC$ and the measure of angle $\widehat{ABC}$.",
             r"AB = %s\,\text{km},\ BC = %s\,\text{km},\ \widehat{ABC} = %s" % (_xx(d1, 2), _xx(d2, 2), _goc(B)),
             r"$AB = %d\cdot\dfrac{%d}{60} = %s\,\text{km}$, $BC = %d\cdot\dfrac{%d}{60} = %s\,\text{km}$.\\ "
             % (v1, t1, _xx(d1, 2), v2, t2, _xx(d2, 2)) + _giai_goc_doi_huong(h1, h2, delta)),
            (r"Find the distance from port $A$ to island $C$ (rounded to the nearest tenth).",
             r"AC \approx %s\,\text{km}" % _xx(AC, 1),
             r"Law of cosines: $AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos %s \approx %s$, "
             r"so $AC \approx %s\,\text{km}$." % (_goc(B), _xx(AC * AC, 2), _xx(AC, 1))),
            (r"Determine the heading from port $A$ to island $C$ (round the angle measure to the nearest whole number).",
             tAC[8:].strip("$") if "$" in tAC else tAC,
             r"Law of sines: $\sin\widehat{BAC} = \dfrac{BC\cdot\sin B}{AC} \approx %s$; angle $B$ is not acute, "
             r"so $\widehat{BAC} \approx %d^{\circ}$.\\ The ship turns %s at $B$, so the heading of $AC$ corresponds to $%s$ "
             r"(measured clockwise from north), that is, %s." % (_xx(sinA, 4), gA_n, phia,
                                                   _cong_goc(h1, gA_n if re_phai else -gA_n), tAC)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_VD036_TL_A_02(socau, dong=1):
    r"""Tự luận: cột ăng-ten trên nóc toà nhà. Từ điểm quan sát $A$ ở độ cao
    $h_0$ nhìn đỉnh $B$ và chân $C$ của cột với hai góc nâng $\alpha > \beta$;
    tính các góc tam giác $ABC$, đoạn $AC$ và chiều cao toà nhà.

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD036_TL_A, theo bai "cot ang-ten
    7 m, vi tri quan sat cao 10 m, goc 75 va 45" trong giao an Bai 6.
    Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        d = random.randint(5, 15)
        h0 = random.randint(6, 20)
        al = random.choice([60, 65, 70, 75, 80])
        be = random.choice([x for x in (20, 25, 30, 35, 40, 45) if al - x >= 25])
        A, B, C = al - be, 90 - al, 90 + be
        AC = d * math.sin(math.radians(B)) / math.sin(math.radians(A))
        CH = AC * math.sin(math.radians(be))
        cao = h0 + CH
        debai = (r"On the roof of a building stands an antenna mast $BC$ of height $%d\,\text{m}$ ($C$ is the base of the mast, located on "
                 r"the roof). From an observation point $A$ at a height of $%d\,\text{m}$ above the ground, the top $B$ and the base $C$ "
                 r"of the mast are seen at angles of elevation of $%s$ and $%s$, respectively, above the "
                 r"horizontal." % (d, h0, _goc(al), _goc(be)))
        ds_abcd = [
            (r"Find the angles of triangle $ABC$.",
             r"\widehat{A} = %s,\ \widehat{B} = %s,\ \widehat{C} = %s" % (_goc(A), _goc(B), _goc(C)),
             r"Let $H$ be the projection of $A$ onto line $BC$ (vertical), so $AH$ is horizontal.\\ "
             r"$\widehat{BAC} = %s - %s = %s$; triangle $ABH$ is right-angled at $H$, so "
             r"$\widehat{ABC} = 90^{\circ} - %s = %s$;\\ $\widehat{ACB} = 180^{\circ} - %s - %s = %s$."
             % (_goc(al), _goc(be), _goc(A), _goc(al), _goc(B), _goc(A), _goc(B), _goc(C))),
            (r"Find the length $AC$ (rounded to the nearest hundredth).", r"AC \approx %s\,\text{m}" % _xx(AC, 2),
             r"Law of sines in triangle $ABC$: $\dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$, so "
             r"$AC = \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (d, _goc(B), _goc(A), _xx(AC, 2))),
            (r"Find the height of the building (rounded to the nearest tenth).", r"\approx %s\,\text{m}" % _xx(cao, 1),
             r"Triangle $ACH$ is right-angled at $H$: $CH = AC\cdot\sin %s \approx %s\,\text{m}$.\\ The height of the building "
             r"(from the ground to $C$) is $%d + CH \approx %s\,\text{m}$." % (_goc(be), _xx(CH, 2), h0, _xx(cao, 1))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def _mot_le_m(x):
    """Một chữ số thập phân CỐ ĐỊNH (kể cả ,0) + đơn vị mét, để phương án không lộ đáp án."""
    return "$%s\\,\\text{m}$" % ("%.1f" % float(x)).replace(".", DAU_THAP_PHAN)


def L10_C3_B6_VD036_MC_D_02(socau, dang=1):
    r"""Tháp trên đỉnh đồi: biết chiều cao tháp và hai góc nhìn từ chân đồi,
    tính chiều cao ngọn đồi (định lí sin rồi tam giác vuông).

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD036_MC_D, theo bai "thap cao
    120 m tren ngon doi, goc 35 va 60 so voi phuong thang dung" trong giao an
    Bai 6. Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        h = random.choice(range(20, 131, 10))
        be = random.choice([15, 20, 25, 30])          # sườn đồi dốc không quá 30 độ (01/10/2026: đề phải hợp lí)
        al = be + random.choice([10, 15, 20, 25, 30])
        if al > 70:
            continue
        AC = h * math.cos(math.radians(al)) / math.sin(math.radians(al - be))
        cao = AC * math.sin(math.radians(be))
        if cao < h / 2 or AC * math.cos(math.radians(be)) < 50:   # đồi cao ít nhất nửa tháp, chân đồi đủ xa
            continue
        dung = _mot_le_m(cao)
        ung = [_mot_le_m(AC), _mot_le_m(cao + h), _mot_le_m(AC * math.cos(math.radians(be))),
               _mot_le_m(h * math.sin(math.radians(al)) / math.sin(math.radians(al - be)) * math.sin(math.radians(be)))]
        nhieu = _ba_nhieu(dung, ung, buoc=lambda k: _mot_le_m(cao + 3.7 * k))
        so += 1
        if random.random() < 0.5:
            mo = (r"From point $A$ at the foot of the hill, the top $B$ and the base $C$ of the tower are seen at angles of elevation of "
                  r"$%s$ and $%s$, respectively." % (_goc(al), _goc(be)))
            doi = r""
        else:
            mo = (r"The top $B$ and the base $C$ of the tower are seen from point $A$ at the foot of the hill at angles of "
                  r"$%s$ and $%s$ from the vertical, respectively." % (_goc(90 - al), _goc(90 - be)))
            doi = (r"The angles from the vertical are $%s$ and $%s$, so the angles of elevation from $A$ are "
                   r"$\alpha = 90^{\circ} - %s = %s$, $\beta = 90^{\circ} - %s = %s$.\\ "
                   % (_goc(90 - al), _goc(90 - be), _goc(90 - al), _goc(al), _goc(90 - be), _goc(be)))
        debai = (r"On top of a hill stands a tower $BC$ of height $%d\,\text{m}$ ($C$ is the base of the tower). %s Let $H$ "
                 r"be the projection of $C$ onto the horizontal plane through $A$. The height $CH$ of the hill is closest "
                 r"to which value (rounded to the nearest tenth)?" % (h, mo))
        giai = (doi + r"In triangle $ABC$: $\widehat{BAC} = %s - %s = %s$, $\widehat{ABC} = 90^{\circ} - %s "
                r"= %s$.\\ Law of sines: $AC = \dfrac{BC\cdot\sin\widehat{ABC}}{\sin\widehat{BAC}} = "
                r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$.\\ Triangle $ACH$ is right-angled at $H$: "
                r"$CH = AC\cdot\sin %s \approx %s\,\text{m}$."
                % (_goc(al), _goc(be), _goc(al - be), _goc(al), _goc(90 - al), h, _goc(90 - al),
                   _goc(al - be), _xx(AC, 2), _goc(be), _xx(cao, 1)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_MC_D_03(socau, dang=1):
    r"""Chiếc diều: một bạn đứng trên nóc toà nhà, một bạn đứng dưới chân toà
    nhà cùng nhìn chiếc diều với hai góc nâng; tính độ cao của diều so với
    mặt đất (định lí sin, rồi cộng chiều cao tầm mắt).

    CLAUDE THEM 29/09/2026 - bien the 03 cua VD036_MC_D, theo bai "dieu, goc
    35 va 75, toa nha 20 m, mat 1,5 m" trong giao an Bai 6. Luu y: dap so
    trong giao an (24,6 m) moi la do cao so voi TAM MAT ban B, con phai cong
    1,5 m nua. Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        h = random.choice(range(15, 41, 5))
        e = random.choice([1.5, 1.6])
        al = random.choice([20, 25, 30, 35, 40])
        be = random.choice([60, 65, 70, 75, 80])
        if be - al < 25:
            continue
        BC = h * math.cos(math.radians(al)) / math.sin(math.radians(be - al))
        CK = BC * math.sin(math.radians(be))
        if CK <= h + 2:
            continue
        cao = CK + e
        dung = _mot_le_m(cao)
        nhieu = _ba_nhieu(dung, [_mot_le_m(CK), _mot_le_m(BC + e), _mot_le_m(CK + h)],
                          buoc=lambda k: _mot_le_m(cao + 2.3 * k))
        so += 1
        e_s = _xx(e, 1)
        debai = (r"An is standing on the roof of a building of height $%d\,\text{m}$, and Binh is standing at the foot of the building; each "
                 r"person's eye level is $%s\,\text{m}$ above where they stand, and the two stand on the same vertical line. An looks "
                 r"at a kite at an angle of elevation of $%s$, and Binh looks at the kite at an angle of elevation of $%s$. How high "
                 r"is the kite above the ground (rounded to the nearest tenth of a meter)?" % (h, e_s, _goc(al), _goc(be)))
        giai = (r"Let $A$, $B$ be the eyes of An and Binh and $C$ the kite. Then $AB = %d\,\text{m}$ (both eye levels "
                r"are $%s\,\text{m}$ above where they stand). Draw $CK$ perpendicular to the horizontal line through $B$.\\ "
                r"$\widehat{CAB} = 90^{\circ} + %s = %s$, $\widehat{CBA} = 90^{\circ} - %s = %s$, so "
                r"$\widehat{ACB} = %s$.\\ Law of sines: $BC = \dfrac{AB\cdot\sin\widehat{CAB}}{\sin\widehat{ACB}} "
                r"= \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$.\\ $CK = BC\cdot\sin %s \approx "
                r"%s\,\text{m}$. Height of the kite above the ground: $%s + %s \approx %s\,\text{m}$."
                % (h, e_s, _goc(al), _goc(90 + al), _goc(be), _goc(90 - be), _goc(be - al), h, _goc(90 + al),
                   _goc(be - al), _xx(BC, 2), _goc(be), _xx(CK, 2), _xx(CK, 2), e_s, _xx(cao, 1)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_SA_A_04(socau, dang=2):
    r"""Đường hầm xuyên núi: đường cũ đi vòng $A \to B \to C \to D$ (biết ba
    đoạn và hai góc), đường mới nối thẳng $AD$. Đường mới ngắn hơn bao nhiêu
    ki-lô-mét? (định lí côsin hai lần).

    CLAUDE THEM 29/09/2026 - bien the 04 cua VD036_SA_A, theo bai "duong ham
    6 km, 5 km, 10 km, goc 100 va 145" trong giao an Bai 6. Co Lan duyet.
    """
    cau = ""
    so = 0
    while so < socau:
        AB, BC, CD = random.randint(4, 9), random.randint(3, 7), random.randint(7, 12)
        gB = random.choice(range(95, 141, 5))
        gC = random.choice(range(115, 156, 5))
        # B(0;0), C(BC;0), A và D cùng nằm phía trên BC
        Ax, Ay = AB * math.cos(math.radians(gB)), AB * math.sin(math.radians(gB))
        Dx = BC + CD * math.cos(math.radians(180 - gC))
        Dy = CD * math.sin(math.radians(180 - gC))
        P = [(Ax, Ay), (0, 0), (BC, 0), (Dx, Dy)]
        cr = [(P[(i + 1) % 4][0] - P[i][0]) * (P[(i + 2) % 4][1] - P[(i + 1) % 4][1])
              - (P[(i + 1) % 4][1] - P[i][1]) * (P[(i + 2) % 4][0] - P[(i + 1) % 4][0]) for i in range(4)]
        if not (all(x > 0 for x in cr) or all(x < 0 for x in cr)):
            continue
        AD = math.hypot(Dx - Ax, Dy - Ay)
        giam = AB + BC + CD - AD
        ds = _xx(giam, 1)
        if len(ds) > 4 or giam < 1:
            continue
        so += 1
        AC2 = AB * AB + BC * BC - 2 * AB * BC * math.cos(math.radians(gB))
        AC = math.sqrt(AC2)
        gBCA = math.degrees(math.acos((BC * BC + AC2 - AB * AB) / (2 * BC * AC)))
        gACD = gC - gBCA
        debai = (r"To avoid the mountain, the current road has to detour along $A \to B \to C \to D$ with "
                 r"$AB = %d\,\text{km}$, $BC = %d\,\text{km}$, $CD = %d\,\text{km}$, $\widehat{ABC} = %s$, "
                 r"$\widehat{BCD} = %s$ (convex quadrilateral $ABCD$). A tunnel through the mountain is planned to connect "
                 r"$A$ directly to $D$. By how many kilometers is the new road shorter than the old road "
                 r"(round to the nearest tenth)?" % (AB, BC, CD, _goc(gB), _goc(gC)))
        giai = (r"Triangle $ABC$: $AC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s \approx %s$, "
                r"$AC \approx %s\,\text{km}$.\\ $\cos\widehat{BCA} = \dfrac{BC^{2} + AC^{2} - AB^{2}}{2\cdot BC"
                r"\cdot AC} \approx %s$, so $\widehat{BCA} \approx %s^{\circ}$, hence "
                r"$\widehat{ACD} = %s - \widehat{BCA} \approx %s^{\circ}$.\\ Triangle $ACD$: $AD^{2} = AC^{2} + "
                r"CD^{2} - 2\cdot AC\cdot CD\cdot\cos\widehat{ACD} \approx %s$, $AD \approx %s\,\text{km}$.\\ "
                r"The old road has length $%d + %d + %d = %d\,\text{km}$, so the new road is shorter by about "
                r"$%d - %s \approx %s\,\text{km}$."
                % (AB, BC, AB, BC, _goc(gB), _xx(AC2, 2), _xx(AC, 2),
                   _xx((BC * BC + AC2 - AB * AB) / (2 * BC * AC), 4), _xx(gBCA, 2), _goc(gC), _xx(gACD, 2),
                   _xx(AD * AD, 2), _xx(AD, 2), AB, BC, CD, AB + BC + CD, AB + BC + CD, _xx(AD, 2), ds))
        nhieu = _ba_nhieu(ds, [_xx(AD, 1), _xx(AB + BC + CD - AC, 1), _xx(giam + 1, 1)],
                          buoc=lambda k: _xx(giam + 0.3 * k, 1))
        cau += MC_SA_answer_text(debai, ds, nhieu, giai, 0, 0, dang)
    return cau



# =====================================================================
# BIẾN THỂ TỪ "BÀI TẬP TRẮC NGHIỆM" BÀI 5 CỦA CÔ LAN (30/09/2026)
# ---------------------------------------------------------------------
# Nguồn: \subsection{BÀI TẬP TRẮC NGHIỆM} Bài 5 (Phần I, II, III) cô gửi.
# Mỗi hàm hoặc là biến thể (_02, _03...) CÙNG DẠNG với ID đã có, hoặc là
# dạng mới (dòng mapping mới, ghi chú "CLAUDE THEM 30/09/2026 ... co Lan
# duyet lai"). Bài 5 chỉ có NB029, TH030, TH031 nên không có câu nào vượt
# quá mức Thông hiểu (câu "sin + cos = a" hạ xuống TH bằng cách cho a là số).
# Đáp án tính bằng sympy (chính xác), không gõ tay.
# =====================================================================

_GOC_DB = [30, 45, 60, 120, 135, 150]      # góc đặc biệt có đủ sin, cos, tan, cot
_HAM4 = ["sin", "cos", "tan", "cot"]
_DOI_HAM = {"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan"}


def _ngoac(v):
    """Giá trị âm đặt trong ngoặc khi thay vào biểu thức."""
    return (r"\left(%s\right)" % _L(v)) if v < 0 else _L(v)


def _tri(v):
    """Giá trị lượng giác viết gọn thành một phân số (\\dfrac); số âm đưa dấu
    trừ ra trước phân số ($-\\dfrac{\\sqrt{2} + 1}{2}$)."""
    v = simplify(v)
    if v == 0:
        return "0"
    if float(v) < 0:
        return "-" + _gon(-v)
    return _gon(v)


def L10_C3_B5_NB029_MC_A_03(socau, dang=1):
    r"""Giá trị lượng giác của góc đặc biệt - tính TỔNG / HIỆU hai giá trị
    lượng giác, có ít nhất một giá trị vô tỉ (vd $\cos 45^\circ + \sin 45^\circ$,
    $\tan 30^\circ + \cot 30^\circ$).

    CLAUDE THEM 30/09/2026 - bien the 03 cua NB029_MC_A, theo cau 1, cau 2
    Phan I bai tap trac nghiem Bai 5 cua co Lan. Cung dang voi _02 (bieu
    thuc gom cac gia tri luong giac goc dac biet), _02 chi dung gia tri huu
    ti, _03 co can thuc. Co Lan duyet lai.
    """
    CAP = [(h, d) for d in (0, 30, 45, 60, 90, 120, 135, 150, 180)
           for h in _HAM4 if _gtlg(h, d) is not None and _gtlg(h, d) != 0]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        (h1, d1), (h2, d2) = random.sample(CAP, 2)
        v1, v2 = _gtlg(h1, d1), _gtlg(h2, d2)
        if v1.is_Rational and v2.is_Rational:
            continue
        dau = random.choice([1, -1])
        if (h1, d1, h2, d2, dau) in gt:
            continue
        gt.append((h1, d1, h2, d2, dau))
    cau = ""
    for h1, d1, h2, d2, dau in gt:
        v1, v2 = _gtlg(h1, d1), _gtlg(h2, d2)
        tong = simplify(v1 + dau * v2)
        phep = "+" if dau > 0 else "-"
        bt = r"\%s %s %s \%s %s" % (h1, _goc(d1), phep, h2, _goc(d2))
        thay = r"%s %s %s" % (_L(v1), phep, _ngoac(v2))
        ung = [simplify(abs(v1) + dau * abs(v2)), simplify(v1 - dau * v2), -tong]
        w1, w2 = _gtlg(_DOI_HAM[h1], d1), _gtlg(_DOI_HAM[h2], d2)
        if w1 is not None and w2 is not None:
            ung.append(simplify(w1 + dau * w2))
        dung = _tri(tong)
        nhieu = _ba_nhieu(dung, [_tri(x) for x in ung],
                          buoc=lambda t: _tri(tong + t))
        debai = r"The value of $%s$ is" % bt
        giai = (r"Using the table of trigonometric values of special angles (or a calculator):"
                r" $\%s %s = %s$, $\%s %s = %s$." % (h1, _goc(d1), _L(v1), h2, _goc(d2), _L(v2))
                + "\\\\\n" + r"Hence $%s = %s = %s$." % (bt, thay, dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_NB029_MC_H_01(socau, dang=1):
    r"""Chọn đẳng thức ĐÚNG (hoặc SAI) trong bốn đẳng thức về sin, côsin,
    tang, côtang của CÙNG một góc đặc biệt.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 3 Phan I bai tap trac nghiem
    Bai 5 ("sin 150 = ..., cos 150 = ..., tan 150 = ..., cot 150 = ...,
    dang thuc nao dung?"). Dang thuc sai: sai dau hoac nham gia tri cua ham
    khac. Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (random.choice(_GOC_DB), random.random() < 0.5)
        if v not in gt:
            gt.append(v)
    cau = ""
    for d, hoi_dung in gt:
        that = {h: _gtlg(h, d) for h in _HAM4}
        dung_ds, sai_ds = [], []
        for h in _HAM4:
            v = that[h]
            w = that[_DOI_HAM[h]]
            ung = [x for x in (-v, w, -w) if simplify(x - v) != 0]
            dung_ds.append(r"$\%s %s = %s$" % (h, _goc(d), _L(v)))
            sai_ds.append(r"$\%s %s = %s$" % (h, _goc(d), _L(random.choice(ung))))
        k = random.randrange(4)
        if hoi_dung:
            dung, nhieu = dung_ds[k], [sai_ds[i] for i in range(4) if i != k]
        else:
            dung, nhieu = sai_ds[k], [dung_ds[i] for i in range(4) if i != k]
        debai = (r"Which of the following equalities is \textbf{%s}?"
                 % ("true" if hoi_dung else "false"))
        giai = (r"Using the table of trigonometric values of special angles (or a calculator):"
                + "\\\\\n" + ", ".join(r"$\%s %s = %s$" % (h, _goc(d), _L(that[h])) for h in _HAM4)
                + ".\\\\\n" + r"Hence the %s equality is %s." % ("true" if hoi_dung else "false", dung))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


# ---- TH031: hai góc phụ nhau, bù nhau ----
_TICH = [
    (r"\cos AA\cos BB - \sin AA\sin BB", lambda sa, ca, sb, cb: ca * cb - sa * sb),
    (r"\sin AA\cos BB + \cos AA\sin BB", lambda sa, ca, sb, cb: sa * cb + ca * sb),
    (r"\cos AA\cos BB + \sin AA\sin BB", lambda sa, ca, sb, cb: ca * cb + sa * sb),
    (r"\sin AA\cos BB - \cos AA\sin BB", lambda sa, ca, sb, cb: sa * cb - ca * sb),
]


def L10_C3_B5_TH031_MC_C_01(socau, dang=1):
    r"""Tính biểu thức dạng $\cos a\cos b \pm \sin a\sin b$ (hoặc
    $\sin a\cos b \pm \cos a\sin b$) với $a$, $b$ là hai góc đặc biệt PHỤ
    nhau hoặc BÙ nhau: đổi giá trị lượng giác của $b$ theo $a$ rồi tính.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 4 Phan I bai tap trac nghiem
    Bai 5 ("P = cos30 cos60 - sin30 sin60"). Co Lan duyet lai.
    """
    CAP = [(a, 90 - a, "phu") for a in (30, 60)] + \
          [(a, 180 - a, "bu") for a in (30, 45, 60, 120, 135, 150)]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (random.choice(CAP), random.randrange(len(_TICH)))
        if v not in gt:
            gt.append(v)
    cau = ""
    for (a, b, quan_he), k in gt:
        mau, f = _TICH[k]
        sa, ca, sb, cb = _gtlg("sin", a), _gtlg("cos", a), _gtlg("sin", b), _gtlg("cos", b)
        P = simplify(f(sa, ca, sb, cb))
        bt = mau.replace("AA", _goc(a)).replace("BB", _goc(b))
        mau_nhan = mau.replace("AA\\", "AA\\cdot \\")     # \cos AA\cdot \cos BB
        if quan_he == "phu":
            doi = mau_nhan.replace(r"\cos BB", r"\sin AA").replace(r"\sin BB", r"\cos AA")
            ly = (r"Since $%s + %s = 90^{\circ}$, the two angles are complementary: $\sin %s = \cos %s$, "
                  r"$\cos %s = \sin %s$." % (_goc(a), _goc(b), _goc(b), _goc(a), _goc(b), _goc(a)))
        else:
            doi = mau_nhan.replace(r"\cos BB", r"\left(-\cos AA\right)").replace(r"\sin BB", r"\sin AA")
            ly = (r"Since $%s + %s = 180^{\circ}$, the two angles are supplementary: $\sin %s = \sin %s$, "
                  r"$\cos %s = -\cos %s$." % (_goc(a), _goc(b), _goc(b), _goc(a), _goc(b), _goc(a)))
        so = doi.replace(r"\left(-\cos AA\right)", _ngoac(simplify(-ca)))
        so = so.replace(r"\sin AA", _ngoac(sa)).replace(r"\cos AA", _ngoac(ca))
        doi = doi.replace("AA", _goc(a))
        dung = "$P = %s$" % _tri(P)
        khac = [simplify(g(sa, ca, sb, cb)) for i, (_, g) in enumerate(_TICH) if i != k]
        nhieu = _ba_nhieu(dung, ["$P = %s$" % _tri(x) for x in khac + [-P, Integer(1), Integer(0)]],
                          buoc=lambda t: "$P = %s$" % _tri(P + t))
        debai = r"Find the value of the expression $P = %s$." % bt
        giai = (ly + "\\\\\n" + r"Hence $P = %s$." % doi + "\\\\\n" +
                r"Since $\sin %s = %s$ and $\cos %s = %s$, we have $P = %s = %s$."
                % (_goc(a), _L(sa), _goc(a), _L(ca), so, _tri(P)))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


# (biểu thức, giá trị, cách biến đổi) - alpha + beta = 90 độ (hai góc nhọn)
_BT_PHU = [
    (r"\sin\alpha\cos\beta + \sin\beta\cos\alpha", 1,
     r"\sin\alpha\cdot\sin\alpha + \cos\alpha\cdot\cos\alpha = \sin^{2}\alpha + \cos^{2}\alpha = 1"),
    (r"\cos\alpha\cos\beta - \sin\alpha\sin\beta", 0,
     r"\cos\alpha\sin\alpha - \sin\alpha\cos\alpha = 0"),
    (r"\sin^{2}\alpha + \sin^{2}\beta", 1, r"\sin^{2}\alpha + \cos^{2}\alpha = 1"),
    (r"\cos^{2}\alpha + \cos^{2}\beta", 1, r"\cos^{2}\alpha + \sin^{2}\alpha = 1"),
    (r"\tan\alpha\tan\beta", 1, r"\tan\alpha\cot\alpha = 1"),
    (r"\sin\alpha - \cos\beta", 0, r"\sin\alpha - \sin\alpha = 0"),
]
# alpha + beta = 180 độ
_BT_BU = [
    (r"\sin\alpha\cos\beta + \sin\beta\cos\alpha", 0,
     r"-\sin\alpha\cos\alpha + \sin\alpha\cos\alpha = 0"),
    (r"\cos\alpha\cos\beta - \sin\beta\sin\alpha", -1,
     r"-\cos^{2}\alpha - \sin^{2}\alpha = -\left(\sin^{2}\alpha + \cos^{2}\alpha\right) = -1"),
    (r"\sin^{2}\alpha + \cos^{2}\beta", 1, r"\sin^{2}\alpha + \cos^{2}\alpha = 1"),
    (r"\cos\alpha + \cos\beta", 0, r"\cos\alpha - \cos\alpha = 0"),
    (r"\sin\alpha - \sin\beta", 0, r"\sin\alpha - \sin\alpha = 0"),
    (r"\sin\alpha\sin\beta - \cos\alpha\cos\beta", 1,
     r"\sin^{2}\alpha + \cos^{2}\alpha = 1"),
]


def L10_C3_B5_TH031_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn: cho $\alpha + \beta = 90^{\circ}$ (hoặc $180^{\circ}$),
    tính biểu thức theo $\alpha$, $\beta$ - đổi giá trị lượng giác của
    $\beta$ theo $\alpha$ rồi dùng $\sin^{2}\alpha + \cos^{2}\alpha = 1$.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 1, cau 2 Phan III bai tap
    trac nghiem Bai 5 ("alpha + beta = 90, P = sin a cos b + sin b cos a";
    "alpha + beta = 180, P = cos a cos b - sin b sin a"). Dap so nguyen.
    Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        phu = random.random() < 0.5
        BT = _BT_PHU if phu else _BT_BU
        i = random.choice([j for j, e in enumerate(BT) if e[1] != 0])
        k1 = random.choice([1, 1, 2, 3, 4])
        if random.random() < 0.5:
            j = random.choice([t for t in range(len(BT)) if t != i])
            k2 = random.choice([1, 2, 3]) * random.choice([1, -1])
        else:
            j, k2 = None, 0
        tri = k1 * BT[i][1] + (k2 * BT[j][1] if j is not None else 0)
        if tri == 0 or (phu, i, k1, j, k2) in gt:
            continue
        gt.append((phu, i, k1, j, k2))
    cau = ""
    for phu, i, k1, j, k2 in gt:
        BT = _BT_PHU if phu else _BT_BU

        def hang(k, e, dau_dau):
            so = "" if abs(k) == 1 else "%d" % abs(k)
            than = (r"%s\left(%s\right)" % (so, e[0])) if so else e[0]
            if not so and not dau_dau and k < 0 and (" + " in e[0] or " - " in e[0]):
                than = r"\left(%s\right)" % e[0]
            if dau_dau:
                return ("-" if k < 0 else "") + than
            return (" - " if k < 0 else " + ") + than

        bt = hang(k1, BT[i], True) + (hang(k2, BT[j], False) if j is not None else "")
        tri = k1 * BT[i][1] + (k2 * BT[j][1] if j is not None else 0)
        dap = str(tri)
        if phu:
            dk = r"Given two acute angles $\alpha$ and $\beta$ with $\alpha + \beta = 90^{\circ}$."
            ly = (r"Since the angles $\alpha$ and $\beta$ are complementary, $\sin\beta = \cos\alpha$, "
                  r"$\cos\beta = \sin\alpha$, $\tan\beta = \cot\alpha$.")
        else:
            dk = r"Given two angles $\alpha$ and $\beta$ with $\alpha + \beta = 180^{\circ}$."
            ly = (r"Since the angles $\alpha$ and $\beta$ are supplementary, $\sin\beta = \sin\alpha$, "
                  r"$\cos\beta = -\cos\alpha$.")
        dong = [r"$%s = %s$." % (BT[i][0], BT[i][2])]
        if j is not None:
            dong.append(r"$%s = %s$." % (BT[j][0], BT[j][2]))
        tinh = ("%d\\cdot %s" % (k1, _ngoac(Integer(BT[i][1])))) if k1 != 1 else "%d" % BT[i][1]
        if j is not None:
            tinh += " %s %d\\cdot %s" % ("-" if k2 < 0 else "+", abs(k2), _ngoac(Integer(BT[j][1])))
        debai = dk + r" Find the value of the expression $P = %s$." % bt
        giai = (ly + "\\\\\n" + "\\\\\n".join(dong) + "\\\\\n" +
                r"Hence $P = %s = %s$." % (tinh, dap))
        ds = _ba_nhieu(dap, [str(-tri), str(tri + 1), "0", str(k1 + abs(k2))],
                       buoc=lambda t: str(tri + t + 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_D_01(socau, dang=1):
    r"""Chọn đẳng thức ĐÚNG (hoặc SAI) giữa giá trị lượng giác của hai góc
    đặc biệt phụ nhau hoặc bù nhau (vd $\cos 45^\circ = \sin 135^\circ$,
    $\cos 30^\circ = \sin 120^\circ$).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 5 Phan I bai tap trac nghiem
    Bai 5. Chi lay cac cap co gia tri tuyet doi bang nhau, nen dang thuc sai
    la sai DAU hoac nham quan he phu/bu - dung cho de nham. Co Lan duyet lai.
    """
    MD = []
    for d1 in _GOC_DB:
        for d2 in (90 - d1, 180 - d1):
            if d2 not in _GOC_DB:
                continue
            for h1 in _HAM4:
                for h2 in _HAM4:
                    if d2 == d1 and h1 == h2:
                        continue
                    v1, v2 = _gtlg(h1, d1), _gtlg(h2, d2)
                    if simplify(abs(v1) - abs(v2)) != 0:
                        continue
                    for dau in (1, -1):
                        tex = r"$\%s %s = %s\%s %s$" % (h1, _goc(d1), "" if dau > 0 else "-",
                                                        h2, _goc(d2))
                        MD.append((tex, simplify(v1 - dau * v2) == 0, h1, d1, h2, d2, dau))
    cau = ""
    for _ in range(socau):
        hoi_dung = random.random() < 0.5
        dung_ds = [m for m in MD if m[1] == hoi_dung]
        sai_ds = [m for m in MD if m[1] != hoi_dung]
        m0 = random.choice(dung_ds)
        chon, trai = [], {(m0[2], m0[3])}
        random.shuffle(sai_ds)
        for m in sai_ds:
            if (m[2], m[3]) not in trai:
                chon.append(m)
                trai.add((m[2], m[3]))
            if len(chon) == 3:
                break
        dong = []
        for m in [m0] + chon:
            tex, dung_that, h1, d1, h2, d2, dau = m
            v1, v2 = _gtlg(h1, d1), _gtlg(h2, d2)
            dong.append(r"%s: \textbf{%s}, since $\%s %s = %s$ while $%s\%s %s = %s$."
                        % (tex, "true" if dung_that else "false", h1, _goc(d1), _L(v1),
                           "" if dau > 0 else "-", h2, _goc(d2), _L(simplify(dau * v2))))
        random.shuffle(dong)
        debai = (r"Which of the following statements is \textbf{%s}?"
                 % ("true" if hoi_dung else "false"))
        giai = (r"Using the table of trigonometric values of special angles (supplementary angles have equal sines and "
                r"opposite cosines; for complementary angles, the sine of one equals the cosine of the other):"
                + "\\\\\n" + "\\\\\n".join(dong))
        cau += MC_SA_answer_text(debai, m0[0], [m[0] for m in chon], giai, 0, 0, dang)
    return cau


# công thức TỔNG QUÁT: (vế phải đúng, [vế phải sai]) cho từng vế trái
_CT_BU = {
    r"\sin\left(180^{\circ} - \alpha\right)": (r"\sin\alpha", [r"-\sin\alpha", r"\cos\alpha", r"-\cos\alpha"]),
    r"\cos\left(180^{\circ} - \alpha\right)": (r"-\cos\alpha", [r"\cos\alpha", r"\sin\alpha", r"-\sin\alpha"]),
    r"\tan\left(180^{\circ} - \alpha\right)": (r"-\tan\alpha", [r"\tan\alpha", r"\cot\alpha", r"-\cot\alpha"]),
    r"\cot\left(180^{\circ} - \alpha\right)": (r"-\cot\alpha", [r"\cot\alpha", r"\tan\alpha", r"-\tan\alpha"]),
}
_CT_PHU = {
    r"\sin\alpha": (r"\cos\beta", [r"-\cos\beta", r"\sin\beta", r"-\sin\beta"]),
    r"\cos\alpha": (r"\sin\beta", [r"-\sin\beta", r"\cos\beta", r"-\cos\beta"]),
    r"\tan\alpha": (r"\cot\beta", [r"-\cot\beta", r"\tan\beta", r"-\tan\beta"]),
    r"\cot\alpha": (r"\tan\beta", [r"-\tan\beta", r"\cot\beta", r"-\cot\beta"]),
}


def L10_C3_B5_TH031_MC_E_01(socau, dang=1):
    r"""Chọn công thức ĐÚNG (hoặc SAI) về giá trị lượng giác của hai góc bù
    nhau ($\alpha$ và $180^{\circ} - \alpha$) hoặc hai góc nhọn phụ nhau
    ($\alpha$ và $\beta$) - dạng TỔNG QUÁT, không có số.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 7 ("sin(180 - a) = ?") va
    cau 8 ("alpha, beta phu nhau, he thuc nao sai?") Phan I bai tap trac
    nghiem Bai 5. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        loai, hoi_dung = random.choice(["bu", "phu"]), random.random() < 0.5
        CT = _CT_BU if loai == "bu" else _CT_PHU
        trai = list(CT)
        t = random.choice(trai)
        if hoi_dung:
            dung = "$%s = %s$" % (t, CT[t][0])
            nhieu = ["$%s = %s$" % (t, p) for p in CT[t][1]]
        else:
            dung = "$%s = %s$" % (t, random.choice(CT[t][1]))
            nhieu = ["$%s = %s$" % (x, CT[x][0]) for x in trai if x != t]
        if loai == "bu":
            debai = (r"Given an angle $\alpha$ with $0^{\circ} < \alpha < 180^{\circ}$, $\alpha \ne 90^{\circ}$. "
                     r"Which of the following equalities is \textbf{%s}?"
                     % ("true" if hoi_dung else "false"))
            ly = (r"The supplementary angles $\alpha$ and $180^{\circ} - \alpha$ have equal sines; their cosines, tangents and "
                  r"cotangents are opposites:" + "\\\\\n" +
                  ", ".join("$%s = %s$" % (x, CT[x][0]) for x in trai) + ".")
        else:
            debai = (r"Given two complementary acute angles $\alpha$ and $\beta$. Which of the following relations is "
                     r"\textbf{%s}?" % ("true" if hoi_dung else "false"))
            ly = (r"For two complementary acute angles, the sine of one equals the cosine of the other, and the tangent of one equals "
                  r"the cotangent of the other:" + "\\\\\n" +
                  ", ".join("$%s = %s$" % (x, CT[x][0]) for x in trai) + ".")
        giai = ly + "\\\\\n" + r"Hence the %s relation is %s." % ("true" if hoi_dung else "false", dung)
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_F_01(socau, dang=1):
    r"""Tam giác vuông biết một góc nhọn đặc biệt: suy ra góc nhọn còn lại
    (hai góc PHỤ nhau) rồi chọn khẳng định đúng / sai về sin, côsin, tang
    của hai góc nhọn.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 9 Phan I bai tap trac nghiem
    Bai 5 ("tam giac ABC vuong o A, B = 30 do, khang dinh nao sai?").
    Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (tuple(random.sample("ABC", 3)), random.choice([30, 45, 60]), random.random() < 0.5)
        if v not in gt:
            gt.append(v)
    cau = ""
    for (X, Y, Z), g, hoi_dung in gt:
        z = 90 - g
        DS = []
        for dinh, goc in ((Y, g), (Z, z)):
            for h in ("sin", "cos", "tan"):
                v = _gtlg(h, goc)
                ung = [x for x in (_gtlg(_DOI_HAM[h], goc), 1 / v, -v) if simplify(x - v) != 0]
                DS.append((r"$\%s %s = %s$" % (h, dinh, _L(v)),
                           r"$\%s %s = %s$" % (h, dinh, _L(simplify(ung[0])))))
        random.shuffle(DS)
        if hoi_dung:
            dung, nhieu = DS[0][0], [d[1] for d in DS[1:4]]
        else:
            dung, nhieu = DS[0][1], [d[0] for d in DS[1:4]]
        debai = (r"In right triangle $ABC$ with the right angle at $%s$, we have $\widehat{%s} = %s$. Which of the following "
                 r"statements is \textbf{%s}?" % (X, Y, _goc(g), "true" if hoi_dung else "false"))
        giai = (r"The two acute angles of a right triangle are complementary, so $\widehat{%s} = 90^{\circ} - %s = %s$."
                % (Z, _goc(g), _goc(z)) + "\\\\\n" +
                r"Using the table of trigonometric values of special angles: " +
                ", ".join(r"$\%s %s = %s$" % (h, dinh, _L(_gtlg(h, goc)))
                          for dinh, goc in ((Y, g), (Z, z)) for h in ("sin", "cos", "tan")) + ".\\\\\n" +
                r"Hence the %s statement is %s." % ("true" if hoi_dung else "false", dung))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_B_02(socau, dang=1):
    r"""Hai điểm đối xứng qua trục tung trên nửa đường tròn đơn vị - cho SỐ
    ĐO góc $\widehat{xOM}$, tính một giá trị lượng giác của $\widehat{xON}$
    ($\widehat{xON} = 180^{\circ} - \widehat{xOM}$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_B (cung dang voi _01:
    quan he hai goc bu qua hai diem doi xung), _01 cho toa do bang chu
    $x_0$, $y_0$, _02 cho so do goc. Theo cau 11 Phan I bai tap trac nghiem
    Bai 5 ("xOM = 150, N doi xung M qua truc tung, tan xON = ?"). Co Lan
    duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (random.choice(_GOC_DB), random.choice(_HAM4))
        if v not in gt:
            gt.append(v)
    cau = ""
    for a, h in gt:
        b = 180 - a
        v = _gtlg(h, b)
        dung = _L(v)
        ung = [_gtlg(h, a), -v, _gtlg(_DOI_HAM[h], b), -_gtlg(_DOI_HAM[h], b)]
        ung += [_gtlg(h, d) for d in random.sample(_GOC_DB, len(_GOC_DB))]
        nhieu = _ba_nhieu(dung, [_L(x) for x in ung], buoc=lambda t: _L(v + t))
        debai = (r"In the coordinate plane $Oxy$, take a point $M$ on the unit semicircle such that "
                 r"$\widehat{xOM} = %s$. Let $N$ be the reflection of $M$ across the y-axis. The value "
                 r"of $\%s\widehat{xON}$ is" % (_goc(a), h))
        giai = (r"Since $N$ is the reflection of $M$ across the y-axis, $\widehat{xON} = 180^{\circ} - "
                r"\widehat{xOM} = 180^{\circ} - %s = %s$." % (_goc(a), _goc(b)) + "\\\\\n" +
                r"Hence $\%s\widehat{xON} = \%s %s = %s$." % (h, h, _goc(b), dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_MC_D_01(socau, dang=1):
    r"""Biết $\sin\alpha + \cos\alpha$ (hoặc $\sin\alpha - \cos\alpha$) bằng một
    SỐ cho trước, tính $\sin\alpha\cos\alpha$ - bình phương hai vế rồi dùng
    $\sin^{2}\alpha + \cos^{2}\alpha = 1$.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 12 Phan I bai tap trac
    nghiem Bai 5 ("sin a + cos a = a, tinh sin a cos a"). Giao an cho $a$ la
    chu (muc Van dung); Bai 5 chi co den Thong hieu nen HA MUC: cho $a$ la so
    (sinh tu bo ba Pythagore nen goc alpha luon ton tai trong [0; 180]).
    Co Lan duyet lai.
    """
    BO = BO_BA_PYTAGO + [(b, a, c) for a, b, c in BO_BA_PYTAGO]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        p, q, r = random.choice(BO)
        s = random.choice([1, -1])
        tong = random.random() < 0.5
        a = Rational(p, r) + (1 if tong else -1) * s * Rational(q, r)
        if a == 0 or (a, tong) in gt:
            continue
        gt.append((a, tong))
    cau = ""
    for a, tong in gt:
        if tong:
            P = (a ** 2 - 1) / 2
            ung = [(a ** 2 + 1) / 2, a ** 2 - 1, (1 - a ** 2) / 2, a ** 2 / 2]
            bt, bien = r"\sin\alpha + \cos\alpha", r"1 + 2\sin\alpha\cos\alpha"
            ket = r"\dfrac{%s^{2} - 1}{2}" % _ngoac_mu(a)
        else:
            P = (1 - a ** 2) / 2
            ung = [(a ** 2 - 1) / 2, 1 - a ** 2, (a ** 2 + 1) / 2, a ** 2 / 2]
            bt, bien = r"\sin\alpha - \cos\alpha", r"1 - 2\sin\alpha\cos\alpha"
            ket = r"\dfrac{1 - %s^{2}}{2}" % _ngoac_mu(a)
        dung = _L(P)
        # sin.cos = sin(2α)/2 nằm trong [-1/2; 1/2]: phương án nhiễu ngoài miền này bị loại ngay
        nhieu = _nhieu_trong_mien(P, ung, Rational(-1, 2), Rational(1, 2), Rational(1, 100))
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ satisfying "
                 r"$%s = %s$. Find the value of $\sin\alpha\cos\alpha$." % (bt, _L(a)))
        giai = (r"Squaring both sides: $\left(%s\right)^{2} = %s^{2}$" % (bt, _ngoac_mu(a))
                + "\\\\\n" +
                r"$\Leftrightarrow \sin^{2}\alpha + \cos^{2}\alpha %s 2\sin\alpha\cos\alpha = %s$"
                % ("+" if tong else "-", _L(a ** 2)) + "\\\\\n" +
                r"$\Leftrightarrow %s = %s$ (since $\sin^{2}\alpha + \cos^{2}\alpha = 1$)" % (bien, _L(a ** 2))
                + "\\\\\n" + r"$\Leftrightarrow \sin\alpha\cos\alpha = %s = %s$." % (ket, dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def _nhieu_trong_mien(dung, ung, thap, cao, buoc=Rational(1, 50), fmt=None):
    """Ba phương án nhiễu (chuỗi LaTeX) mà giá trị PHẢI NẰM TRONG MIỀN GIÁ TRỊ CÓ THỂ của đại lượng được hỏi.

    Cô Lan 11/10/2026: câu hỏi $(\\sin\\alpha - \\cos\\alpha)^{2}$ mà có phương án âm (hoặc $\\sin^{4}\\alpha + \\cos^{4}\\alpha > 1$)
    thì học sinh loại ngay không cần tính. thap, cao: miền giá trị của đại lượng; ung: các giá trị sai hay gặp
    (quên hệ số 2, nhầm dấu, ...); thiếu thì thêm các giá trị lệch nhỏ quanh đáp số nhưng vẫn trong miền."""
    ds = []
    for x in ung:
        if thap <= x <= cao and x != dung and x not in ds:
            ds.append(x)
    t = 1
    while len(ds) < 3 and t < 400:
        for dau in (1, -1):
            x = dung + dau * t * buoc
            if thap <= x <= cao and x != dung and x not in ds and len(ds) < 3:
                ds.append(x)
        t += 1
    return [(fmt or _L)(x) for x in ds[:3]]


def _ngoac_mu(v):
    """Số đặt trong ngoặc khi nâng lên luỹ thừa (phân số hoặc số âm)."""
    return (r"\left(%s\right)" % _L(v)) if (v < 0 or not v.is_Integer) else _L(v)


def L10_C3_TF_A_03(socau, socot=1):
    r"""Đúng/Sai - biết $\sin\alpha$ hoặc $\cos\alpha$ (phân số, giá trị còn
    lại có CĂN THỨC) và khoảng của góc: góc phụ, giá trị còn lại, tang,
    góc bù.

    CLAUDE THEM 30/09/2026 - bien the 03 cua L10_C3_TF_A (cung dang voi _02:
    biet mot gia tri luong giac va loai goc), theo cau 1 ("sin a = 2/7,
    0 < a < 90") va cau 2 ("cos x = -5/13, 90 < x < 180") Phan II bai tap
    trac nghiem Bai 5. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    CAP = [(p, q) for q in range(3, 10) for p in range(1, q)
           if math.gcd(p, q) == 1 and math.isqrt(q * q - p * p) ** 2 != q * q - p * p]
    cauTF = ""
    for _ in range(socau):
        p, q = random.choice(CAP)
        cho_sin = random.random() < 0.5
        tu = random.random() < 0.5
        dau = -1 if tu else 1
        can = sqrt(Integer(q * q - p * p)) / q
        if cho_sin:
            sn, cs = Rational(p, q), (-can if tu else can)
        else:
            cs, sn = (Rational(-p, q) if tu else Rational(p, q)), can
        tn = simplify(sn / cs)
        ct = simplify(cs / sn)
        khoang = r"90^{\circ} < \alpha < 180^{\circ}" if tu else r"0^{\circ} < \alpha < 90^{\circ}"
        cho = (r"\sin\alpha = %s" % _L(sn)) if cho_sin else (r"\cos\alpha = %s" % _L(cs))
        debai = (r"Given $%s$ and $%s$. Determine whether each of the following statements is true or false:" % (cho, khoang))
        # a) NB - goc phu nhau, goc bu nhau (cua gia tri da cho)
        if cho_sin:
            ly_a = (r"Complementary angles: $\cos\left(90^{\circ} - \alpha\right) = \sin\alpha$; supplementary angles: "
                    r"$\sin\left(180^{\circ} - \alpha\right) = \sin\alpha = %s$." % _L(sn))
            dung = [(r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a), (r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a)]
            sai = [(r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a), (r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a),
                   (r"$\sin\left(90^{\circ} - \alpha\right) = %s$" % _L(sn), "That is $\\cos\\alpha$. " + ly_a)]
        else:
            ly_a = (r"Complementary angles: $\sin\left(90^{\circ} - \alpha\right) = \cos\alpha$; supplementary angles: "
                    r"$\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha = %s$." % _L(-cs))
            dung = [(r"$\sin\left(90^{\circ} - \alpha\right) = %s$" % _L(cs), ly_a), (r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(-cs), ly_a)]
            sai = [(r"$\sin\left(90^{\circ} - \alpha\right) = %s$" % _L(-cs), ly_a), (r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(cs), ly_a),
                   (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(cs), "That is $\\sin\\alpha$. " + ly_a)]
        y1 = _phat_bieu(dung, sai)
        # b) TH - tinh gia tri con lai, xet dau theo khoang
        if cho_sin:
            ly_b = (r"Since $%s$, we have $\cos\alpha %s 0$. Hence $\cos\alpha = %s\sqrt{1 - \sin^{2}\alpha} = "
                    r"%s\sqrt{1 - %s} = %s$." % (khoang, "<" if tu else ">", "-" if tu else "",
                                                 "-" if tu else "", _L(sn ** 2), _L(cs)))
            y2 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", cs, ly_b, [(-cs, "Sign error"), (dau * (1 - sn), "Forgot to square"),
                                                                 (dau * cs ** 2, "Forgot to take the square root")]),
                         _tf_ct(r"$\cos^{2}\alpha = %s$", cs ** 2, ly_b, [(1 + sn ** 2, "Sign error in $1 - \\sin^{2}\\alpha$"), (sn ** 2, "Mistakenly using $\\cos^{2}\\alpha = \\sin^{2}\\alpha$")]))
        else:
            ly_b = (r"Since $%s$, we have $\sin\alpha > 0$. Hence $\sin\alpha = \sqrt{1 - \cos^{2}\alpha} = "
                    r"\sqrt{1 - %s} = %s$." % (khoang, _L(cs ** 2), _L(sn)))
            y2 = _tf_gop(_tf_ct(r"$\sin\alpha = %s$", sn, ly_b, [(-sn, "$\\sin\\alpha$ is always positive"), (1 - abs(cs), "Forgot to square"),
                                                                 (sn ** 2, "Forgot to take the square root")]),
                         _tf_ct(r"$\sin^{2}\alpha = %s$", sn ** 2, ly_b, [(1 + cs ** 2, "Wrong sign in $1 - \\cos^{2}\\alpha$"), (cs ** 2, "Mistakenly using $\\sin^{2}\\alpha = \\cos^{2}\\alpha$")]))
        # c) VD - tang, cotang tu hai gia tri
        ly_c = ly_b + r" $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$, $\cot\alpha = \dfrac{\cos\alpha}{\sin\alpha} = %s$." % (_L(tn), _L(ct))
        y3 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", tn, ly_c, [(1 / tn, "Numerator and denominator swapped"), (-tn, "Sign error"), (sn * cs, "Mistakenly using $\\tan\\alpha = \\sin\\alpha\\cdot\\cos\\alpha$")]),
                     _tf_ct(r"$\cot\alpha = %s$", ct, ly_c, [(tn, "Mistakenly using $\\cot\\alpha = \\tan\\alpha$"), (-ct, "Sign error")]))
        # d) VDC - goc bu nhau, dung gia tri vua tinh (nhieu bieu thuc)
        ly_d = ly_c + (r" Supplementary angles: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha$, $\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha$, "
                       r"$\tan\left(180^{\circ} - \alpha\right) = -\tan\alpha$, $\cot\left(180^{\circ} - \alpha\right) = -\cot\alpha$.")
        BT = [(r"\tan\left(180^{\circ} - \alpha\right)", -tn, [tn, -ct]),
              (r"\cot\left(180^{\circ} - \alpha\right)", -ct, [ct, -tn]),
              (r"\sin\left(180^{\circ} - \alpha\right) + \cos\left(180^{\circ} - \alpha\right)", sn - cs, [sn + cs, -sn - cs]),
              (r"\sin\left(180^{\circ} - \alpha\right)\cdot\tan\left(180^{\circ} - \alpha\right)", -sn * tn, [sn * tn, -cs * tn]),
              (r"\cos\left(180^{\circ} - \alpha\right) - 2\sin\left(90^{\circ} - \alpha\right)", -3 * cs, [cs, -cs - 2 * sn])]
        dung, sai = [], []
        for bt, P, Ps in random.sample(BT, 3):
            d_, s_ = _tf_ct("$" + bt + " = %s$", simplify(P), ly_d, [(simplify(Q), "Mixing up the supplementary-angle and complementary-angle relations") for Q in Ps])
            dung += d_
            sai += s_
        y4 = _phat_bieu(dung, sai)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _lyq = r"Supplementary angles have equal sines and opposite cosines; for complementary angles, the sine of one equals the cosine of the other."
        _tf_them(y1, [(r"$\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha$", _lyq), (r"$\sin\left(90^{\circ} - \alpha\right) = \cos\alpha$", _lyq),
                      (r"$\tan\left(180^{\circ} - \alpha\right) = -\tan\alpha$", _lyq)],
                 [(r"$\cos\left(180^{\circ} - \alpha\right) = \cos\alpha$", _lyq), (r"$\sin\left(90^{\circ} - \alpha\right) = \sin\alpha$", _lyq),
                  (r"$\tan\left(180^{\circ} - \alpha\right) = \tan\alpha$", _lyq)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_F_01(socau, socot=1):
    r"""Đúng/Sai - giá trị lượng giác các góc của tam giác biết một góc tù
    (hoặc nhọn): dấu, $\sin\left(B + C\right) = \sin A$,
    $\cos\left(A + B\right) = -\cos C$...

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 3 Phan II bai tap trac nghiem
    Bai 5 ("tam giac ABC, A tu: cos A < 0, cos(A + B) = cos C, sin(A + B) =
    sin C"). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        X, Y, Z = random.sample("ABC", 3)
        tu = random.random() < 0.6
        loai = "obtuse" if tu else "acute"
        debai = (r"Given triangle $ABC$ in which $\widehat{%s}$ is %s. Determine whether each of the "
                 r"following statements is true or false:" % (X, loai))
        yz = "%s + %s" % tuple(sorted([Y, Z]))
        am, duong = ("<", ">") if tu else (">", "<")
        # a) NB - dau cua gia tri luong giac cua goc X
        ly_a = (r"Since $\widehat{%s}$ is %s, $\sin %s > 0$, while $\cos %s$, $\tan %s$, $\cot %s$ are %s."
                % (X, loai, X, X, X, X, "negative" if tu else "positive"))
        y1 = _phat_bieu(
            [(r"$\sin %s > 0$" % X, ly_a)] + [(r"$\%s %s %s 0$" % (h, X, am), ly_a) for h in ("cos", "tan", "cot")],
            [(r"$\sin %s < 0$" % X, ly_a)] + [(r"$\%s %s %s 0$" % (h, X, duong), ly_a) for h in ("cos", "tan", "cot")])
        # b) TH - Y + Z = 180 - X (mot buoc: goc bu)
        ly_b = (r"Since $\widehat{A} + \widehat{B} + \widehat{C} = 180^{\circ}$, we have $%s = 180^{\circ} - %s$; "
                r"supplementary angles have equal sines and opposite cosines, tangents and cotangents." % (yz, X))
        y2 = _phat_bieu(
            [(r"$\sin\left(%s\right) = \sin %s$" % (yz, X), ly_b), (r"$\cos\left(%s\right) = -\cos %s$" % (yz, X), ly_b),
             (r"$\tan\left(%s\right) = -\tan %s$" % (yz, X), ly_b), (r"$\cot\left(%s\right) = -\cot %s$" % (yz, X), ly_b)],
            [(r"$\sin\left(%s\right) = -\sin %s$" % (yz, X), ly_b), (r"$\cos\left(%s\right) = \cos %s$" % (yz, X), ly_b),
             (r"$\tan\left(%s\right) = \tan %s$" % (yz, X), ly_b), (r"$\sin\left(%s\right) = \cos %s$" % (yz, X), ly_b)])
        # c) VD - voi mot cap khac: (X + Y) va Z
        xy = "%s + %s" % tuple(sorted([X, Y]))
        ly_c = (r"$%s = 180^{\circ} - %s$, so $\cos\left(%s\right) = -\cos %s$, $\sin\left(%s\right) = \sin %s$." % (xy, Z, xy, Z, xy, Z))
        dung = [(r"$\cos\left(%s\right) + \cos %s = 0$" % (xy, Z), ly_c), (r"$\sin\left(%s\right) - \sin %s = 0$" % (xy, Z), ly_c)]
        sai = [(r"$\sin\left(%s\right) + \sin %s = 0$" % (xy, Z), ly_c + r" But $\sin %s > 0$." % Z)]
        if tu:      # khi X tù thì Z nhọn (khác 90 độ) nên các khẳng định dưới đây luôn sai / luôn đúng
            dung.append((r"$\tan\left(%s\right) + \tan %s = 0$" % (xy, Z), ly_c))
            sai += [(r"$\cos\left(%s\right) = \cos %s$" % (xy, Z), ly_c + r" But $\widehat{%s}$ is acute, so $\cos %s \ne 0$." % (Z, Z)),
                    (r"$\cos\left(%s\right) - \cos %s = 0$" % (xy, Z), ly_c + r" But $\widehat{%s}$ is acute, so $\cos %s \ne 0$." % (Z, Z))]
        else:
            sai.append((r"$\sin\left(%s\right) = -\sin %s$" % (xy, Z), ly_c + r" But $\sin %s > 0$." % Z))
        y3 = _phat_bieu(dung, sai)
        # d) VDC - ket hop quan he bu va dau
        ly_d = (r"$\cos\left(%s\right) = -\cos %s$, $\sin\left(%s\right) = \sin %s$, $\tan\left(%s\right) = -\tan %s$, so "
                r"$\cos %s\cdot\cos\left(%s\right) = -\cos^{2} %s < 0$, $\tan %s\cdot\tan\left(%s\right) = -\tan^{2} %s < 0$ "
                r"(since $\widehat{%s} \ne 90^{\circ}$), $\sin %s\cdot\sin\left(%s\right) = \sin^{2} %s > 0$; "
                r"$\sin\left(%s\right)\cdot\cos\left(%s\right) = -\sin %s\cos %s %s 0$."
                % (yz, X, yz, X, yz, X, X, yz, X, X, yz, X, X, X, yz, X, yz, yz, X, X, duong))
        y4 = _phat_bieu(
            [(r"$\cos %s\cdot\cos\left(%s\right) < 0$" % (X, yz), ly_d), (r"$\tan %s\cdot\tan\left(%s\right) < 0$" % (X, yz), ly_d),
             (r"$\sin %s\cdot\sin\left(%s\right) > 0$" % (X, yz), ly_d),
             (r"$\sin\left(%s\right)\cdot\cos\left(%s\right) %s 0$" % (yz, yz, duong), ly_d)],
            [(r"$\cos %s\cdot\cos\left(%s\right) > 0$" % (X, yz), ly_d), (r"$\tan %s\cdot\tan\left(%s\right) > 0$" % (X, yz), ly_d),
             (r"$\sin %s\cdot\sin\left(%s\right) < 0$" % (X, yz), ly_d),
             (r"$\sin\left(%s\right)\cdot\cos\left(%s\right) %s 0$" % (yz, yz, am), ly_d)])
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y3, [(r"$\cos\left(%s\right) = -\cos %s$" % (xy, Z), ly_c), (r"$\sin\left(%s\right) = \sin %s$" % (xy, Z), ly_c)],
                 [(r"$\sin\left(%s\right) = -\sin %s$" % (xy, Z), ly_c + r" But $\sin %s > 0$." % Z),
                  (r"$\cos\left(%s\right)\cdot\cos %s > 0$" % (xy, Z), ly_c + r" Hence $\cos\left(%s\right)\cdot\cos %s = -\cos^{2} %s \le 0$." % (xy, Z, Z))])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def _hinh_MAN(a):
    """Nửa đường tròn đơn vị, M (góc a), N đối xứng M qua Oy, A(1;0), tam giác MAN."""
    return (
        "\\begin{tikzpicture}[>=stealth,scale=1.7,font=\\footnotesize]\n"
        "\\draw[->] (-1.5,0) -- (1.5,0) node[below] {$x$};\n"
        "\\draw[->] (0,-0.3) -- (0,1.4) node[right] {$y$};\n"
        "\\draw (1,0) arc (0:180:1);\n"
        "\\coordinate (O) at (0,0);\n\\coordinate (A) at (1,0);\n"
        "\\coordinate (M) at (%d:1);\n\\coordinate (N) at (%d:1);\n" % (a, 180 - a)
        + "\\fill[gray!25] (M) -- (A) -- (N) -- cycle;\n"
        "\\draw (A) -- (M) -- (N) -- cycle;\n\\draw (O) -- (M);\n"
        "\\node[below] at (-1,0) {$-1$};\n"
        "\\fill (O) circle (0.02) node[below left] {$O$};\n"
        "\\fill (A) circle (0.02) node[below right] {$A$};\n"
        "\\fill (M) circle (0.02) node[above left] {$M$};\n"
        "\\fill (N) circle (0.02) node[above right] {$N$};\n"
        "\\end{tikzpicture}"
    )


def L10_C3_TF_D_02(socau, socot=1):
    r"""Đúng/Sai - điểm $M$ trên nửa đường tròn đơn vị cho bằng SỐ ĐO góc
    $\widehat{xOM}$ (góc tù), $N$ đối xứng với $M$ qua trục tung: góc
    $\widehat{xON}$, toạ độ $M$, $N$ và diện tích tam giác $MAN$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua L10_C3_TF_D (cung dang: gia tri
    luong giac doc tu toa do diem tren nua duong tron don vi), theo cau 4
    Phan II bai tap trac nghiem Bai 5 ("xOM = 150, N doi xung M qua truc
    tung, S tam giac MAN"). Co hinh. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        a = random.choice([120, 135, 150])
        b = 180 - a
        c, s = _gtlg("cos", a), _gtlg("sin", a)
        S = simplify(-c * s)
        debai = (r"In the coordinate plane $Oxy$, take a point $M$ on the unit semicircle such that "
                 r"$\widehat{xOM} = %s$ and the point $A\left(1; 0\right)$. Let $N$ be the reflection of $M$ across "
                 r"the y-axis. Determine whether each of the following statements is true or false:" % _goc(a))
        # a) NB - đối xứng qua trục tung
        ly_a = (r"Since $N$ is the reflection of $M$ across the y-axis, $\widehat{xON} = 180^{\circ} - %s = %s$ (the angles $\widehat{xOM}$, "
                r"$\widehat{xON}$ are supplementary)." % (_goc(a), _goc(b)))
        y1 = _phat_bieu(
            [(r"$\widehat{xON} = %s$" % _goc(b), ly_a), (r"$\widehat{xOM} + \widehat{xON} = 180^{\circ}$", ly_a)],
            [(r"$\widehat{xON} = %s$" % _goc(g), ly_a) for g in (a - 90, 2 * b, 90, a) if g != b] +
            [(r"$\widehat{xOM} + \widehat{xON} = 90^{\circ}$", ly_a)])
        # b) TH - toạ độ M (một bước: góc -> sin, cos)
        ly_b = (r"$x_M = \cos %s = %s$, $y_M = \sin %s = %s$." % (_goc(a), _L(c), _goc(a), _L(s)))
        y2 = _phat_bieu(
            [(r"$M\left(%s; %s\right)$" % (_L(c), _L(s)), ly_b), (r"$x_M = %s$" % _L(c), ly_b), (r"$y_M = %s$" % _L(s), ly_b)],
            [(r"$M\left(%s; %s\right)$" % (_L(-c), _L(s)), ly_b), (r"$M\left(%s; %s\right)$" % (_L(s), _L(c)), ly_b),
             (r"$M\left(%s; %s\right)$" % (_L(c), _L(-s)), ly_b), (r"$y_M = %s$" % _L(c), ly_b), (r"$x_M = %s$" % _L(-c), ly_b)])
        # c) VD - toạ độ N
        ly_c = (r"$x_N = \cos %s = %s$, $y_N = \sin %s = %s$ (same y-coordinate as $M$, opposite x-coordinate)."
                % (_goc(b), _L(-c), _goc(b), _L(s)))
        y3 = _phat_bieu(
            [(r"$N\left(%s; %s\right)$" % (_L(-c), _L(s)), ly_c), (r"$x_N = %s$" % _L(-c), ly_c),
             (r"$MN = %s$" % _L(-2 * c), ly_c + r" $MN = x_N - x_M = %s$." % _L(-2 * c))],
            [(r"$N\left(%s; %s\right)$" % (_L(-c), _L(-s)), ly_c), (r"$N\left(%s; %s\right)$" % (_L(c), _L(-s)), ly_c),
             (r"$N\left(%s; %s\right)$" % (_L(s), _L(-c)), ly_c), (r"$x_N = %s$" % _L(c), ly_c),
             (r"$MN = %s$" % _L(-c), ly_c + r" $MN = x_N - x_M = %s$." % _L(-2 * c))])
        # d) VDC - tam giác MAN
        ly_d = (r"$MN$ is parallel to $Ox$ and $MN = 2x_N = %s$; the distance from $A$ (and from $O$) to $MN$ equals "
                r"$y_N = %s$. Hence $S_{\triangle MAN} = S_{\triangle MON} = \dfrac{1}{2}\cdot %s\cdot %s = %s$; "
                r"$AM^{2} = \left(%s - 1\right)^{2} + %s = %s$, $AN^{2} = \left(%s - 1\right)^{2} + %s = %s$."
                % (_L(-2 * c), _L(s), _L(-2 * c), _L(s), _L(S), _L(c), _L(s ** 2), _L(simplify(2 - 2 * c)),
                   _L(-c), _L(s ** 2), _L(simplify(2 + 2 * c))))
        y4 = _tf_gop(_tf_ct(r"$S_{\triangle MAN} = %s$", S, ly_d,
                            [(2 * S, "Forgetting to multiply by $\\dfrac{1}{2}$"), (S / 2, "Mistakenly taking $MN = x_N$"), (s / 2, "Mistakenly taking $MN = 1$")],
                            them=[r"$S_{\triangle MAN} = S_{\triangle MON}$"]),
                     _tf_ct(r"$AM = %s$", sqrt(simplify(2 - 2 * c)), ly_d,
                            [(sqrt(simplify(2 + 2 * c)), "That is $AN$"), (simplify(1 - c), "Forgetting the y-coordinate of $M$")]))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(r"The angle $\widehat{xON}$ is acute", ly_a), (r"$\widehat{xON} = 180^{\circ} - \widehat{xOM}$", ly_a)],
                 [(r"The angle $\widehat{xON}$ is obtuse", ly_a), (r"$\widehat{xON} = \widehat{xOM}$", ly_a)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_MAN(a), 0, socot)
    return cauTF


# (lời, kí hiệu, hàm tính, cách thay số)
_TOA_DO_BT = [
    ("what is the product of the x-coordinate and the y-coordinate", r"x_M\cdot y_M", lambda x, y: x * y,
     lambda x, y: r"%s\cdot %s" % (_ngoac(x), _ngoac(y))),
    ("what is the difference between the square of the x-coordinate and the square of the y-coordinate", r"x_M^{2} - y_M^{2}",
     lambda x, y: x ** 2 - y ** 2,
     lambda x, y: r"\left(%s\right)^{2} - \left(%s\right)^{2}" % (_L(x), _L(y))),
    ("what is the square of the y-coordinate", r"y_M^{2}", lambda x, y: y ** 2,
     lambda x, y: r"\left(%s\right)^{2}" % _L(y)),
    ("what is the square of the x-coordinate", r"x_M^{2}", lambda x, y: x ** 2,
     lambda x, y: r"\left(%s\right)^{2}" % _L(x)),
]


def L10_C3_B5_NB029_SA_J_01(socau, dang=2):
    r"""Trả lời ngắn: biết số đo góc $\widehat{xOM}$ (góc đặc biệt), đọc toạ độ
    $M\left(\cos; \sin\right)$ rồi tính một biểu thức của toạ độ.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 3 Phan III bai tap trac
    nghiem Bai 5 ("xOM = 135, tich hoanh do va tung do cua M"). Chi giu bo
    so cho dap so thap phan huu han, toi da 4 ki tu, khac 0. Co Lan duyet lai.
    """
    BO = []
    for a in _GOC_DB:
        x, y = _gtlg("cos", a), _gtlg("sin", a)
        for k, e in enumerate(_TOA_DO_BT):
            v = simplify(e[2](x, y))
            if v != 0 and _so_thap_phan_gon(v):
                BO.append((a, k))
    random.shuffle(BO)
    cau = ""
    for a, k in BO[:socau]:
        chu, ki, f, thay_so = _TOA_DO_BT[k]
        x, y = _gtlg("cos", a), _gtlg("sin", a)
        v = simplify(f(x, y))
        dap = _so_thap_phan_gon(v)
        debai = (r"In the coordinate plane $Oxy$, take a point $M$ on the unit semicircle such that "
                 r"$\widehat{xOM} = %s$. %s of point $M$?"
                 % (_goc(a), chu[0].upper() + chu[1:]))
        giai = (r"Since $M$ lies on the unit semicircle and $\widehat{xOM} = %s$, "
                r"$x_M = \cos %s = %s$, $y_M = \sin %s = %s$."
                % (_goc(a), _goc(a), _L(x), _goc(a), _L(y))
                + "\\\\\n" + r"Hence $%s = %s = %s = %s$." % (ki, thay_so(x, y), _L(v), dap))
        ds = _ba_nhieu(dap, [_so_thap_phan_gon(-v) or "0", "1", "0", "0.5"],
                       buoc=lambda t: str(t + 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, 0, 0, dang)
    return cau


def _hinh_AOM(goc):
    """Nửa đường tròn đơn vị, A(1;0), điểm M ứng với góc goc (độ), tam giác AOM."""
    return (
        "\\begin{tikzpicture}[>=stealth,scale=1.7,font=\\footnotesize]\n"
        "\\draw[->] (-1.5,0) -- (1.5,0) node[below] {$x$};\n"
        "\\draw[->] (0,-0.3) -- (0,1.4) node[right] {$y$};\n"
        "\\draw (1,0) arc (0:180:1);\n"
        "\\coordinate (O) at (0,0);\n\\coordinate (A) at (1,0);\n"
        "\\coordinate (M) at (%.1f:1);\n" % goc
        + "\\fill[gray!25] (O) -- (A) -- (M) -- cycle;\n"
        "\\draw (O) -- (M) -- (A);\n"
        "\\node[below] at (-1,0) {$-1$};\n"
        "\\fill (O) circle (0.02) node[below left] {$O$};\n"
        "\\fill (A) circle (0.02) node[below right] {$A$};\n"
        "\\fill (M) circle (0.02) node[%s] {$M$};\n" % ("above left" if goc > 90 else "above right")
        + "\\end{tikzpicture}"
    )


def L10_C3_B5_TH030_SA_N_01(socau, dang=2):
    r"""Trả lời ngắn: biết $\cos\widehat{xOM}$ của điểm $M$ trên nửa đường
    tròn đơn vị, tính $\sin\widehat{xOM}$ rồi diện tích tam giác $AOM$ với
    $A\left(1; 0\right)$ (có hình).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 4 Phan III bai tap trac
    nghiem Bai 5 ("cos xOM = -3/5, dien tich tam giac AOM"). Dap so thap
    phan huu han. Co Lan duyet lai.
    """
    BO = [(3, 4, 5), (4, 3, 5), (7, 24, 25), (24, 7, 25)]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 200:
        lan += 1
        v = (random.choice(BO), random.choice([1, -1]))
        if v not in gt:
            gt.append(v)
    cau = ""
    for (doi, ke, huyen), dau in gt:
        cs, sn = Rational(dau * ke, huyen), Rational(doi, huyen)
        S = sn / 2
        dap = _so_thap_phan_gon(S)
        goc = math.degrees(math.acos(float(cs)))
        debai = (r"In the coordinate plane $Oxy$, take a point $M$ on the unit semicircle such that "
                 r"$\cos\widehat{xOM} = %s$ and the point $A\left(1; 0\right)$. What is the area of triangle $AOM$?" % _L(cs))
        giai = (r"Since $M$ lies on the unit semicircle, $y_M \ge 0$, that is, $\sin\widehat{xOM} \ge 0$."
                + "\\\\\n" +
                r"$\sin^{2}\widehat{xOM} = 1 - \cos^{2}\widehat{xOM} = 1 - %s = %s$, so "
                r"$\sin\widehat{xOM} = %s$." % (_L(cs ** 2), _L(sn ** 2), _L(sn)) + "\\\\\n" +
                r"The altitude from $M$ to $OA$ is $h = y_M = \sin\widehat{xOM} = %s$, and $OA = 1$."
                % _L(sn) + "\\\\\n" +
                r"Hence $S_{\triangle AOM} = \dfrac{1}{2}\cdot OA\cdot h = \dfrac{1}{2}\cdot 1\cdot %s = %s$."
                % (_L(sn), dap))
        ds = _ba_nhieu(dap, [_so_thap_phan_gon(sn), _so_thap_phan_gon(abs(cs) / 2),
                             _so_thap_phan_gon(abs(cs))], buoc=lambda t: str(t))
        cau += MC_SA_answer_const(debai, dap, ds, giai, _hinh_AOM(goc), 0, dang)
    return cau



# =====================================================================
# BÀI 5 - DẠNG "LUYỆN TẬP THÊM" (ngoai_yccd, docs/04 Ngoại lệ 4)
# ---------------------------------------------------------------------
# CLAUDE THEM 01/10/2026 theo tai lieu C3-B1 co Lan gui. Co Lan: "cac dang
# nay la bai toan hay nhung trong yeu cau cua Bo khong co" -> van dua vao
# ngan hang, Mapping ghi "ngoai_yccd": true, de sinh ra bao cho giao vien.
# Moi dang deu GIU MUC THONG HIEU: so lieu nho, mot buoc bien doi.
# =====================================================================

def _he_so_dong_bac():
    """Bốn hệ số nguyên a, b, c, d (khác 0) cho P = (a sin + b cos)/(c sin + d cos)."""
    return [random.choice([1, 2, 3, 4, 5, -1, -2, -3]) for _ in range(4)]


def _bt_bac_nhat(a, b, u, v):
    """Viết a.u + b.v gọn: '2\\sin\\alpha - 3\\cos\\alpha'."""
    def hang(k, x, dau):
        if k == 1:
            s = x
        elif k == -1:
            s = "-" + x
        else:
            s = "%d%s" % (k, x)
        if dau and not s.startswith("-"):
            s = "+ " + s
        elif dau:
            s = "- " + s[1:]
        return s
    return hang(a, u, False) + " " + hang(b, v, True)


def _bo_dong_bac(cho_tan, can_sa):
    """Chọn (giá trị tan hoặc cot = t, a, b, c, d, P). P = (a t + b)/(c t + d) khi cho tan,
    = (a + b t)/(c + d t) khi cho cot. Tránh mẫu bằng 0, tránh P = 0."""
    T = [Rational(1, 2), Rational(1, 3), Rational(2, 3), Rational(3, 2), Integer(2), Integer(3),
         Integer(-2), Integer(-3), Rational(-1, 2), Rational(-1, 3), Rational(3, 4), Rational(-3, 4)]
    while True:
        t = random.choice(T)
        a, b, c, d = _he_so_dong_bac()
        if cho_tan:
            tu, mau = a * t + b, c * t + d
        else:
            tu, mau = a + b * t, c + d * t
        if mau == 0 or tu == 0:
            continue
        P = tu / mau
        if abs(P) == 1:
            continue
        if can_sa:
            s = _so_thap_phan_gon(P)
            if s is None or len(s) > 4:
                continue
        return t, a, b, c, d, P


def _bt_mot_bien(a, x, b, x_truoc=True):
    """a.x + b (x_truoc) hoặc a + b.x, hệ số nguyên, viết gọn."""
    def he(k, x):
        return x if k == 1 else ("-" + x if k == -1 else "%d%s" % (k, x))
    dau = "+" if b > 0 else "-"
    if x_truoc:
        return "%s %s %d" % (he(a, x), dau, abs(b))
    return "%d %s %s" % (a, dau, he(abs(b), x))


def _de_giai_dong_bac(t, a, b, c, d, P, cho_tan):
    ham = r"\tan" if cho_tan else r"\cot"
    tu = _bt_bac_nhat(a, b, r"\sin\alpha", r"\cos\alpha")
    mau = _bt_bac_nhat(c, d, r"\sin\alpha", r"\cos\alpha")
    de = (r"Given an angle $\alpha$ satisfying $%s\alpha = %s$. The value of the expression "
          r"$P = \dfrac{%s}{%s}$ is" % (ham, _L(t), tu, mau))
    if cho_tan:
        giai = (r"Since $\tan\alpha = %s$, we have $\cos\alpha \ne 0$. Dividing the numerator and denominator of $P$ by "
                r"$\cos\alpha$ and using $\dfrac{\sin\alpha}{\cos\alpha} = \tan\alpha$:" "\\\\\n"
                r"$P = \dfrac{%s}{%s} = \dfrac{%s}{%s} = %s$."
                % (_L(t), _bt_mot_bien(a, r"\tan\alpha", b), _bt_mot_bien(c, r"\tan\alpha", d),
                   _L(a * t + b), _L(c * t + d), _L(P)))
    else:
        giai = (r"Since $\cot\alpha = %s$, we have $\sin\alpha \ne 0$. Dividing the numerator and denominator of $P$ by "
                r"$\sin\alpha$ and using $\dfrac{\cos\alpha}{\sin\alpha} = \cot\alpha$:" "\\\\\n"
                r"$P = \dfrac{%s}{%s} = \dfrac{%s}{%s} = %s$."
                % (_L(t), _bt_mot_bien(a, r"\cot\alpha", b, False), _bt_mot_bien(c, r"\cot\alpha", d, False),
                   _L(a + b * t), _L(c + d * t), _L(P)))
    return de, giai


def _nhieu_dong_bac(t, a, b, c, d, P, cho_tan):
    if cho_tan:
        ds = [(b * t + a) / (d * t + c) if d * t + c != 0 else None,
              (a * t - b) / (c * t - d) if c * t - d != 0 else None,
              (a + b * t) / (c + d * t) if c + d * t != 0 else None, -P, 1 / P]
    else:
        ds = [(a * t + b) / (c * t + d) if c * t + d != 0 else None,
              (a - b * t) / (c - d * t) if c - d * t != 0 else None, -P, 1 / P]
    return [x for x in ds if x is not None]


def L10_C3_B5_VD030_MC_A_01(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Biết $\tan\alpha$, tính
    $P = \dfrac{a\sin\alpha + b\cos\alpha}{c\sin\alpha + d\cos\alpha}$: chia tử, mẫu cho $\cos\alpha$.

    CLAUDE THEM 01/10/2026 - theo cau 4, cau 44 tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_dong_bac(True, False)
        if v[:5] in [g[:5] for g in gt]:
            continue
        gt.append(v)
    for t, a, b, c, d, P in gt:
        de, giai = _de_giai_dong_bac(t, a, b, c, d, P, True)
        dap = _L(P)
        nh = _ba_nhieu(dap, [_L(x) for x in _nhieu_dong_bac(t, a, b, c, d, P, True)],
                       buoc=lambda k: _L(P + k))
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD030_MC_A_02(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Như _01 nhưng cho $\cot\alpha$: chia tử, mẫu cho $\sin\alpha$.

    CLAUDE THEM 01/10/2026 - theo cau 44, phan III tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_dong_bac(False, False)
        if v[:5] in [g[:5] for g in gt]:
            continue
        gt.append(v)
    for t, a, b, c, d, P in gt:
        de, giai = _de_giai_dong_bac(t, a, b, c, d, P, False)
        dap = _L(P)
        nh = _ba_nhieu(dap, [_L(x) for x in _nhieu_dong_bac(t, a, b, c, d, P, False)],
                       buoc=lambda k: _L(P + k))
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD030_SA_A_01(socau, dang=2):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ) - trả lời ngắn: biết $\tan\alpha$ (hoặc $\cot\alpha$), tính
    biểu thức đồng bậc bậc nhất của $\sin\alpha$, $\cos\alpha$. Đáp số thập phân hữu hạn.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        cho_tan = random.random() < 0.5
        v = _bo_dong_bac(cho_tan, True)
        if v[:5] in [g[0][:5] for g in gt]:
            continue
        gt.append((v, cho_tan))
    for (t, a, b, c, d, P), cho_tan in gt:
        de, giai = _de_giai_dong_bac(t, a, b, c, d, P, cho_tan)
        de = de[:-len("is")].rstrip() + r". Find the value of $P$."
        dap = _so_thap_phan_gon(P)
        cau += MC_SA_answer_const(de, dap, [_so_thap_phan_gon(P + k) or str(k) for k in (1, -1, 2)],
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD030_MC_B_01(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Biết $\tan\alpha - \cot\alpha = m$ (hoặc
    $\tan\alpha + \cot\alpha = m$, $|m| \ge 2$), tính $\tan^{2}\alpha + \cot^{2}\alpha = m^{2} \pm 2$
    nhờ $\tan\alpha\cdot\cot\alpha = 1$.

    CLAUDE THEM 01/10/2026 - theo cau 54, cau 62 tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        cong = random.random() < 0.5
        m = random.choice([2, 3, 4, 5, -2, -3, -4]) if cong else random.choice([1, 2, 3, 4, -1, -2, -3])
        if (cong, m) not in gt:
            gt.append((cong, m))
    for cong, m in gt:
        k = m * m - 2 if cong else m * m + 2
        dau = "+" if cong else "-"
        de = (r"Given an angle $\alpha$ satisfying $\tan\alpha %s \cot\alpha = %d$. The value of the expression "
              r"$A = \tan^{2}\alpha + \cot^{2}\alpha$ is" % (dau, m))
        giai = (r"We have $\tan\alpha\cdot\cot\alpha = 1$. Squaring both sides of the given condition:" "\\\\\n"
                r"$\left(\tan\alpha %s \cot\alpha\right)^{2} = \tan^{2}\alpha + \cot^{2}\alpha %s "
                r"2\tan\alpha\cot\alpha = A %s 2 = %d$." "\\\\\n"
                r"Hence $A = %d$." % (dau, dau, dau, m * m, k))
        nh = _ba_nhieu(str(k), [str(m * m + (2 if cong else -2)), str(m * m), str(m * m + (-1 if cong else 1))],
                       buoc=lambda t: str(k + 3 * t))
        cau += MC_SA_answer_const(de, str(k), nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD030_MC_B_02(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Hỏi ngược của _01: biết $\tan^{2}\alpha + \cot^{2}\alpha = k$,
    tính $\left(\tan\alpha - \cot\alpha\right)^{2}$ hoặc $\left(\tan\alpha + \cot\alpha\right)^{2}$.

    CLAUDE THEM 01/10/2026 - bien the 02 cua TH030_MC_F. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = (random.random() < 0.5, random.choice([2, 3, 5, 7, 11, 14, 18, 23]))
        if v not in gt:
            gt.append(v)
    for cong, k in gt:
        dau = "+" if cong else "-"
        kq = k + 2 if cong else k - 2
        de = (r"Given an angle $\alpha$ satisfying $\tan^{2}\alpha + \cot^{2}\alpha = %d$. The value of "
              r"$\left(\tan\alpha %s \cot\alpha\right)^{2}$ is" % (k, dau))
        giai = (r"Since $\tan\alpha\cdot\cot\alpha = 1$," "\\\\\n"
                r"$\left(\tan\alpha %s \cot\alpha\right)^{2} = \tan^{2}\alpha + \cot^{2}\alpha %s 2 = %d %s 2 = %d$."
                % (dau, dau, k, dau, kq))
        nh = _ba_nhieu(str(kq), [str(k - 2 if cong else k + 2), str(k), str(k + (1 if cong else -1))],
                       buoc=lambda t: str(kq + 3 * t))
        cau += MC_SA_answer_const(de, str(kq), nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD030_SA_B_01(socau, dang=2):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ) - trả lời ngắn: biết $\tan\alpha \pm \cot\alpha = m$, tính
    $\tan^{2}\alpha + \cot^{2}\alpha$.

    CLAUDE THEM 01/10/2026 - theo cau 54 tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        cong = random.random() < 0.5
        m = random.choice([2, 3, 4, 5, 6]) * random.choice([1, -1]) if cong else random.choice([1, 2, 3, 4, 5, 6, -1, -2, -3])
        if (cong, m) not in gt:
            gt.append((cong, m))
    for cong, m in gt:
        k = m * m - 2 if cong else m * m + 2
        dau = "+" if cong else "-"
        de = (r"Given an angle $\alpha$ satisfying $\tan\alpha %s \cot\alpha = %d$. Find the value of the expression "
              r"$A = \tan^{2}\alpha + \cot^{2}\alpha$." % (dau, m))
        giai = (r"Since $\tan\alpha\cdot\cot\alpha = 1$, "
                r"$\left(\tan\alpha %s \cot\alpha\right)^{2} = A %s 2$, that is, $%d = A %s 2$. Hence $A = %d$."
                % (dau, dau, m * m, dau, k))
        cau += MC_SA_answer_const(de, str(k), [str(k + 1), str(k - 1), str(k + 3)], giai, 0, 0, dang)
    return cau


_COS_DEP = [Rational(1, 2), Rational(1, 3), Rational(2, 3), Rational(1, 4), Rational(3, 4),
            Rational(1, 5), Rational(2, 5), Rational(3, 5), Rational(4, 5), Rational(-1, 2),
            Rational(-1, 3), Rational(-2, 3), Rational(-3, 4), Rational(-3, 5), Rational(-4, 5)]


def _bo_bac_hai(can_sa):
    while True:
        cho_cos = random.random() < 0.5
        g = random.choice(_COS_DEP)
        if not cho_cos and g < 0:
            g = -g                       # sin của góc từ 0 đến 180 độ không âm
        a, b = random.sample([1, 2, 3, 4, 5, -1, -2], 2)
        c2 = g ** 2 if cho_cos else 1 - g ** 2
        s2 = 1 - c2
        P = a * s2 + b * c2
        if P == 0:
            continue
        if can_sa:
            s = _so_thap_phan_gon(P)
            if s is None or len(s) > 4:
                continue
        return cho_cos, g, a, b, s2, c2, P


def _de_giai_bac_hai(cho_cos, g, a, b, s2, c2, P):
    ham = r"\cos" if cho_cos else r"\sin"
    bt = _bt_bac_nhat(a, b, r"\sin^{2}\alpha", r"\cos^{2}\alpha")
    de = r"Given an angle $\alpha$ satisfying $%s\alpha = %s$. The value of the expression $P = %s$ is" % (ham, _L(g), bt)
    if cho_cos:
        b1 = (r"$\cos^{2}\alpha = %s$, so $\sin^{2}\alpha = 1 - \cos^{2}\alpha = %s$ "
              r"(the sign of $\sin\alpha$ is not needed)." % (_L(c2), _L(s2)))
    else:
        b1 = (r"$\sin^{2}\alpha = %s$, so $\cos^{2}\alpha = 1 - \sin^{2}\alpha = %s$ "
              r"(the sign of $\cos\alpha$ is not needed)." % (_L(s2), _L(c2)))
    giai = (r"Using $\sin^{2}\alpha + \cos^{2}\alpha = 1$: " + b1 + "\\\\\n" +
            r"$P = %s\cdot %s %s %s\cdot %s = %s$." % (a, _L(s2), "+" if b > 0 else "-", abs(b), _L(c2), _L(P)))
    return de, giai


def L10_C3_B5_VD030_MC_C_01(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Biết $\sin\alpha$ hoặc $\cos\alpha$, tính
    $P = a\sin^{2}\alpha + b\cos^{2}\alpha$ (chỉ cần bình phương, không xét dấu).

    CLAUDE THEM 01/10/2026 - theo cau 39, cau 46 tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_bac_hai(False)
        if v[:4] not in [x[:4] for x in gt]:
            gt.append(v)
    for cho_cos, g, a, b, s2, c2, P in gt:
        de, giai = _de_giai_bac_hai(cho_cos, g, a, b, s2, c2, P)
        dap = _L(P)
        nh = _ba_nhieu(dap, [_L(a * c2 + b * s2), _L(a * s2 - b * c2), _L(a + b), _L(a * g + b * (1 - g))],
                       buoc=lambda k: _L(P + k))
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD030_SA_C_01(socau, dang=2):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ) - trả lời ngắn: biết $\sin\alpha$ hoặc $\cos\alpha$, tính
    $a\sin^{2}\alpha + b\cos^{2}\alpha$. Đáp số thập phân hữu hạn (tối đa 4 kí tự).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_bac_hai(True)
        if v[:4] not in [x[:4] for x in gt]:
            gt.append(v)
    for cho_cos, g, a, b, s2, c2, P in gt:
        de, giai = _de_giai_bac_hai(cho_cos, g, a, b, s2, c2, P)
        de = de[:-len("is")].rstrip() + r". Find the value of $P$."
        dap = _so_thap_phan_gon(P)
        cau += MC_SA_answer_const(de, dap, [_so_thap_phan_gon(P + k) or str(k) for k in (1, -1, 2)],
                                  giai, 0, 0, dang)
    return cau


def _bo_tich_tan():
    """tan a . tan(a+d) ... tan(90-a): các góc cách đều, đối xứng qua 45 độ."""
    while True:
        d = random.choice([1, 2, 3, 5, 9, 10, 15])
        a = random.choice([d, 2 * d]) if 2 * d < 45 else d
        if (45 - a) % d == 0 and a < 45:
            return a, d


def L10_C3_B5_VD031_MC_A_01(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Tích nhiều $\tan$ của các góc cách đều đối xứng qua
    $45^{\circ}$: ghép cặp hai góc phụ nhau, $\tan x\cdot\tan\left(90^{\circ} - x\right) = 1$.
    $P = k\cdot\tan a^{\circ}\tan\left(a+d\right)^{\circ}\cdots\tan\left(90-a\right)^{\circ} + c$.

    CLAUDE THEM 01/10/2026 - theo cau 55, cau 60 tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        a, d = _bo_tich_tan()
        k, c = random.choice([1, 2, 3]), random.choice([0, 1, -1, 2])
        if (a, d, k, c) not in gt:
            gt.append((a, d, k, c))
    for a, d, k, c in gt:
        b = 90 - a
        tich = r"\tan %d^{\circ}\cdot\tan %d^{\circ}\cdots\tan %d^{\circ}" % (a, a + d, b)
        bt = (("%d" % k if k > 1 else "") + tich + (" + %d" % c if c > 0 else (" - %d" % -c if c < 0 else "")))
        kq = k + c
        de = (r"Given the expression $P = %s$, where the product consists of the tangents of the angles $%d^{\circ}, %d^{\circ}, \ldots, %d^{\circ}$ "
              r"(consecutive angles differ by $%d^{\circ}$). The value of $P$ is" % (bt, a, a + d, b, d))
        giai = (r"Group the factors into pairs of complementary angles: "
                r"$\tan x^{\circ}\cdot\tan\left(90 - x\right)^{\circ} = \tan x^{\circ}\cdot\cot x^{\circ} = 1$, "
                r"and the remaining middle factor is $\tan 45^{\circ} = 1$." "\\\\\n"
                r"Hence $\tan %d^{\circ}\cdots\tan %d^{\circ} = 1$ and $P = %d\cdot 1 %s = %d$."
                % (a, b, k, ("+ %d" % c if c > 0 else ("- %d" % -c if c < 0 else "+ 0")), kq))
        nh = _ba_nhieu(str(kq), [str(c), str(kq + 1), str(-k + c), str(2 * k + c)], buoc=lambda t: str(kq + 2 * t))
        cau += MC_SA_answer_const(de, str(kq), nh, giai, 0, 0, dang)
    return cau


def _bo_tong_cos():
    """cos a + cos(a+d) + ... + cos b, các góc cách đều; tính được nhờ ghép hai góc bù nhau."""
    while True:
        d = random.choice([1, 2, 5, 10, 15, 20, 30])
        bat_dau = random.choice([0, d])
        ket_thuc = random.choice([180, 180 - d])
        if bat_dau == 0 and ket_thuc == 180 - d:
            continue
        return bat_dau, ket_thuc, d


def _gia_tri_tong_cos(bat_dau, ket_thuc, d):
    """Tổng cos các góc bat_dau, bat_dau + d, ..., ket_thuc (tính số rồi làm tròn - tập góc
    luôn gồm các cặp bù nhau cộng thêm cos 0 / cos 90 / cos 180 nên tổng là số nguyên)."""
    goc = list(range(bat_dau, ket_thuc + 1, d))
    s = sum(math.cos(math.radians(x)) for x in goc)
    assert abs(s - round(s)) < 1e-9
    return Integer(round(s)), goc


def L10_C3_B5_VD031_MC_A_02(socau, dang=1):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ). Tổng nhiều $\cos$ của các góc cách đều từ $0^{\circ}$ (hoặc
    $d^{\circ}$) đến $180^{\circ}$: ghép cặp hai góc bù nhau, $\cos x + \cos\left(180^{\circ} - x\right) = 0$.

    CLAUDE THEM 01/10/2026 - theo cau 53, phan III tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_tong_cos()
        if v not in gt:
            gt.append(v)
    for bat_dau, ket_thuc, d in gt:
        S, goc = _gia_tri_tong_cos(bat_dau, ket_thuc, d)
        bt = r"\cos %d^{\circ} + \cos %d^{\circ} + \cdots + \cos %d^{\circ}" % (goc[0], goc[1], goc[-1])
        de = (r"Given the expression $S = %s$, where the sum consists of the cosines of the angles $%d^{\circ}, %d^{\circ}, \ldots, %d^{\circ}$ "
              r"(consecutive angles differ by $%d^{\circ}$). The value of $S$ is" % (bt, goc[0], goc[1], goc[-1], d))
        le = [x for x in goc if 180 - x not in goc or x == 90]
        if le:
            con = (r"only the unpaired terms remain: " + ", ".join(r"$\cos %d^{\circ} = %d$" % (x, round(math.cos(math.radians(x))))
                                             for x in le) + ".")
        else:
            con = r"every term can be paired."
        giai = (r"Supplementary angles have opposite cosines: $\cos x + \cos\left(180^{\circ} - x\right) = 0$. "
                r"Group the terms into pairs of supplementary angles; each pair has sum $0$; " + con
                + "\\\\\n" + r"Hence $S = %s$." % _L(S))
        nh = _ba_nhieu(_L(S), ["0", "1", "-1", "2", "-2"], buoc=lambda t: str(t + 2))
        cau += MC_SA_answer_const(de, _L(S), nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_VD031_SA_A_01(socau, dang=2):
    r"""LUYỆN TẬP THÊM (ngoài YCCĐ) - trả lời ngắn: hoặc tích $\tan$ các góc đối xứng qua
    $45^{\circ}$ (ghép phụ), hoặc tổng $\cos$ các góc từ $0^{\circ}$ đến $180^{\circ}$ (ghép bù),
    có nhân hệ số và cộng hằng số để đáp số thay đổi.

    CLAUDE THEM 01/10/2026 - theo cau 53, 55 va phan III tai lieu C3-B1. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        if random.random() < 0.5:
            a, d = _bo_tich_tan()
            v = ("tan", a, d, random.choice([2, 3, 4, 5]), random.choice([1, 2, 3, -1]))
        else:
            # Chỉ lấy dãy góc cho tổng KHÁC 0 (tổng = -1): nếu tổng = 0 thì P = hằng số cộng thêm,
            # hệ số nhân không có tác dụng và đáp án đoán được (cô Lan duyệt 13/10/2026).
            while True:
                bd, kt, dd = _bo_tong_cos()
                if _gia_tri_tong_cos(bd, kt, dd)[0] != 0:
                    break
            v = ("cos", bd, kt, dd, random.choice([2, 3, 4, 5]), random.choice([1, 2, 3, 5]))
        if v not in gt:
            gt.append(v)
    for v in gt:
        if v[0] == "tan":
            _, a, d, k, c = v
            kq = k + c
            de = (r"Given the expression $P = %d\tan %d^{\circ}\cdot\tan %d^{\circ}\cdots\tan %d^{\circ} %s$, "
                  r"where the product consists of the tangents of the angles $%d^{\circ}, %d^{\circ}, \ldots, %d^{\circ}$ "
                  r"(consecutive angles differ by $%d^{\circ}$). Find the value of $P$."
                  % (k, a, a + d, 90 - a, ("+ %d" % c) if c > 0 else ("- %d" % -c), a, a + d, 90 - a, d))
            giai = (r"Pairing complementary angles: $\tan x^{\circ}\cdot\tan\left(90 - x\right)^{\circ} = 1$, "
                    r"the middle factor is $\tan 45^{\circ} = 1$, so the product equals $1$. Hence $P = %d + %d = %d$."
                    % (k, c, kq) if c > 0 else
                    r"Pairing complementary angles: $\tan x^{\circ}\cdot\tan\left(90 - x\right)^{\circ} = 1$, "
                    r"the middle factor is $\tan 45^{\circ} = 1$, so the product equals $1$. Hence $P = %d - %d = %d$."
                    % (k, -c, kq))
        else:
            _, bat_dau, ket_thuc, d, k, c = v
            S, goc = _gia_tri_tong_cos(bat_dau, ket_thuc, d)
            kq = k * S + c
            de = (r"Given the expression $P = %d\left(\cos %d^{\circ} + \cos %d^{\circ} + \cdots + "
                  r"\cos %d^{\circ}\right) + %d$, where the sum consists of the cosines of the angles "
                  r"$%d^{\circ}, %d^{\circ}, \ldots, %d^{\circ}$ (consecutive angles differ by $%d^{\circ}$). "
                  r"Find the value of $P$."
                  % (k, goc[0], goc[1], goc[-1], c, goc[0], goc[1], goc[-1], d))
            le = [x for x in goc if 180 - x not in goc or x == 90]   # số hạng không ghép được cặp bù
            con = (r"only the unpaired terms remain: " + ", ".join(r"$\cos %d^{\circ} = %d$" % (x, round(math.cos(math.radians(x))))
                                              for x in le)) if le else r"every term can be paired"
            giai = (r"Supplementary angles have opposite cosines: $\cos x + \cos\left(180^{\circ} - x\right) = 0$. "
                    r"Group the terms in parentheses into pairs of supplementary angles; each pair has sum $0$; "
                    + con + r", so the sum in parentheses equals $%s$." % _L(S) + "\\\\\n"
                    + r"Hence $P = %d\cdot\left(%s\right) + %d = %s$." % (k, _L(S), c, _L(kq)))
        dap = str(kq)
        cau += MC_SA_answer_const(de, dap, [str(kq + 1), str(kq - 1), str(kq + 2)], giai, 0, 0, dang)
    return cau


# =====================================================================
# BÀI 6 - DẠNG HỎI NGƯỢC MỨC THÔNG HIỂU (CLAUDE THEM 01/10/2026 theo tai lieu
# C3-B2 co Lan gui). Co Lan: "chuyen sao cho ve don gian de dap ung YCCD cua
# Bo" -> so lieu nho, mot cong thuc, dap so dep. Co Lan duyet lai.
# =====================================================================

def _can_gon(x):
    """Chuỗi LaTeX của sqrt(x) đã rút gọn (x hữu tỉ không âm)."""
    return _L(sqrt(Rational(x)))


def _bo_nguoc_trung_tuyen(can_nguyen):
    """(dinh, ten cạnh đối, hai cạnh kề, giá trị) với cạnh đối nguyên, m^2 hữu tỉ,
    m viết gọn (nguyên hoặc k/2 hoặc căn gọn)."""
    while True:
        v = _bo_trung_tuyen(so_nguyen=can_nguyen)
        if v is None:
            continue
        a, b, c, m2 = v
        m = sqrt(m2)
        if not can_nguyen and len(_L(m)) > 18:
            continue
        return a, b, c, m2


def L10_C3_B6_TH032_MC_G_01(socau, dang=1):
    r"""Hỏi ngược công thức trung tuyến: biết hai cạnh và đường trung tuyến xuất phát từ đỉnh
    chung của hai cạnh ấy, tính cạnh thứ ba ($a^{2} = 2b^{2} + 2c^{2} - 4m_{a}^{2}$).

    CLAUDE THEM 01/10/2026 - theo cau 49, phan III tai lieu C3-B2 ("AB = 4, AC = 10,
    AM = 6, tinh BC"). Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_nguoc_trung_tuyen(False) + (random.randrange(3),)
        if v[:3] not in [g[:3] for g in gt]:
            gt.append(v)
    for a, b, c, m2, k in gt:
        dinh, doi, ke1, ke2 = _DINH_CANH[k]
        M = "M"
        de = (r"Given triangle $ABC$ with $%s = %d$, $%s = %d$ and median $%s%s = %s$ ($%s$ is the "
              r"midpoint of $%s$). The length of side $%s$ is"
              % (ke1, b, ke2, c, dinh, M, _L(sqrt(m2)), M, doi, doi))
        giai = (r"By the median formula: $%s%s^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}$." "\\\\\n"
                r"It follows that $%s^{2} = 2\left(%s^{2} + %s^{2}\right) - 4\cdot %s%s^{2} = 2\left(%d + %d\right) - 4\cdot %s = %d$, "
                r"so $%s = %d$."
                % (dinh, M, ke1, ke2, doi, doi, ke1, ke2, dinh, M, b * b, c * c, _L(m2), a * a, doi, a))
        dap = str(a)
        sai = [_can_gon(2 * b * b + 2 * c * c - m2), _can_gon(abs(b * b + c * c - 2 * m2)),
               _can_gon(Rational(2 * b * b + 2 * c * c, 1) - 2 * m2), str(a + 1)]
        nh = _ba_nhieu(dap, [s for s in sai if s != dap], buoc=lambda t: str(a + t + 1))
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH032_SA_G_01(socau, dang=2):
    r"""Trả lời ngắn - hỏi ngược công thức trung tuyến: biết hai cạnh và trung tuyến, tính cạnh
    thứ ba (đáp số nguyên).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_nguoc_trung_tuyen(False) + (random.randrange(3),)
        if v[:3] not in [g[:3] for g in gt]:
            gt.append(v)
    for a, b, c, m2, k in gt:
        dinh, doi, ke1, ke2 = _DINH_CANH[k]
        de = (r"Given triangle $ABC$ with $%s = %d$, $%s = %d$ and median $%sM = %s$ ($M$ is the "
              r"midpoint of $%s$). Find the length of side $%s$."
              % (ke1, b, ke2, c, dinh, _L(sqrt(m2)), doi, doi))
        giai = (r"From $%sM^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}$ we get "
                r"$%s^{2} = 2\left(%d + %d\right) - 4\cdot %s = %d$, so $%s = %d$."
                % (dinh, ke1, ke2, doi, doi, b * b, c * c, _L(m2), a * a, doi, a))
        cau += MC_SA_answer_const(de, str(a), [str(a + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


_GOC_TU_SIN = {Rational(1, 2): (30, 150), sqrt(2) / 2: (45, 135), sqrt(3) / 2: (60, 120)}


def _bo_nguoc_sin(cho_R):
    """Chọn góc A đặc biệt (nhọn hoặc tù), cạnh a = 2R sinA dạng đẹp."""
    while True:
        sA = random.choice(list(_GOC_TU_SIN))
        nhon = random.random() < 0.6
        A = _GOC_TU_SIN[sA][0 if nhon else 1]
        R = random.randint(2, 9)
        a = 2 * R * sA
        return sA, A, nhon, R, a


def L10_C3_B6_TH033_MC_D_01(socau, dang=1):
    r"""Hỏi ngược định lí sin: biết cạnh $BC = a$ và bán kính đường tròn ngoại tiếp $R$ (tam giác
    có góc $A$ nhọn hoặc tù cho trước), tìm số đo góc $A$ từ $\sin A = \dfrac{a}{2R}$.

    CLAUDE THEM 01/10/2026 - theo cau 36, 39 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_nguoc_sin(True)
        if (v[1], v[3]) not in [(g[1], g[3]) for g in gt]:
            gt.append(v)
    for sA, A, nhon, R, a in gt:
        loai = "acute" if nhon else "obtuse"
        de = (r"Given triangle $ABC$ in which angle $A$ is %s, $BC = %s$ and circumradius $R = %d$. "
              r"The measure of angle $A$ is" % (loai, _L(a), R))
        giai = (r"By the law of sines: $\dfrac{BC}{\sin A} = 2R \Rightarrow \sin A = \dfrac{BC}{2R} = "
                r"\dfrac{%s}{%d} = %s$." "\\\\\n"
                r"The two angles whose sine is $%s$ are $%d^{\circ}$ and $%d^{\circ}$; since angle $A$ is %s, "
                r"$\widehat{A} = %d^{\circ}$."
                % (_L(a), 2 * R, _L(sA), _L(sA), _GOC_TU_SIN[sA][0], _GOC_TU_SIN[sA][1], loai, A))
        dap = r"%d^{\circ}" % A
        khac = [g for p in _GOC_TU_SIN.values() for g in p if g != A]
        nh = _ba_nhieu(dap, [r"%d^{\circ}" % (180 - A)] + [r"%d^{\circ}" % g for g in random.sample(khac, 4)])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_MC_D_02(socau, dang=1):
    r"""Hỏi ngược định lí sin, cách hỏi khác: tam giác thoả $k\cdot a\sin B = b\sqrt{n}$ (hoặc
    $k\cdot a\sin B = b$), dùng $a\sin B = b\sin A$ suy ra $\sin A$ rồi góc $A$ (nhọn/tù cho trước).

    CLAUDE THEM 01/10/2026 - theo cau 41 tai lieu C3-B2 ("2a sinB = b can 3"). Co Lan duyet lai.
    """
    BO = [(2, "", Rational(1, 2)), (2, r"\sqrt{2}", sqrt(2) / 2), (2, r"\sqrt{3}", sqrt(3) / 2),
          (4, "2", Rational(1, 2)), (4, r"2\sqrt{3}", sqrt(3) / 2), (6, r"3\sqrt{2}", sqrt(2) / 2)]
    cau, gt = "", []
    while len(gt) < socau:
        v = (random.choice(BO), random.random() < 0.6)
        if v not in gt:
            gt.append(v)
    for (k, ve_phai, sA), nhon in gt:
        A = _GOC_TU_SIN[sA][0 if nhon else 1]
        loai = "acute" if nhon else "obtuse"
        vp = "b" if ve_phai == "" else ve_phai + "\\, b" if not ve_phai[0].isdigit() else ve_phai + "b"
        vp = ("b" if ve_phai == "" else (ve_phai.replace(r"\sqrt", "b\\sqrt", 1) if ve_phai.startswith(r"\sqrt")
                                         else ve_phai[0] + "b" + ve_phai[1:]))
        de = (r"Given triangle $ABC$ in which angle $A$ is %s and $%da\sin B = %s$ (where $a = BC$, $b = CA$). "
              r"The measure of angle $A$ is" % (loai, k, vp))
        giai = (r"By the law of sines: $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} \Rightarrow a\sin B = b\sin A$." "\\\\\n"
                r"Substituting into the given condition: $%db\sin A = %s \Rightarrow \sin A = %s$." "\\\\\n"
                r"Since angle $A$ is %s, $\widehat{A} = %d^{\circ}$."
                % (k, vp, _L(sA), loai, A))
        dap = r"%d^{\circ}" % A
        khac = [g for p in _GOC_TU_SIN.values() for g in p if g != A]
        nh = _ba_nhieu(dap, [r"%d^{\circ}" % (180 - A)] + [r"%d^{\circ}" % g for g in random.sample(khac, 4)])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - hỏi ngược định lí sin: biết $BC$ và $R$, góc $A$ nhọn hoặc tù cho trước,
    tính số đo góc $A$ (độ).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_nguoc_sin(True)
        if (v[1], v[3]) not in [(g[1], g[3]) for g in gt]:
            gt.append(v)
    for sA, A, nhon, R, a in gt:
        loai = "acute" if nhon else "obtuse"
        de = (r"Given triangle $ABC$ in which angle $A$ is %s, $BC = %s$ and circumradius $R = %d$. "
              r"Find the measure of angle $A$ (in degrees)." % (loai, _L(a), R))
        giai = (r"$\sin A = \dfrac{BC}{2R} = \dfrac{%s}{%d} = %s$; since angle $A$ is %s, $\widehat{A} = %d^{\circ}$."
                % (_L(a), 2 * R, _L(sA), loai, A))
        cau += MC_SA_answer_const(de, str(A), [str(180 - A), str(A + 15), str(A - 15)], giai, 0, 0, dang)
    return cau


def _bo_cos_bac_hai():
    """AB = c, BC = x (ẩn, nguyên), góc B = 60 hoặc 120 độ, AC = b nguyên và b > c để phương
    trình x^2 -+ c x + c^2 - b^2 = 0 có đúng một nghiệm dương."""
    while True:
        B = random.choice([60, 120])
        c = random.randint(3, 12)
        x = random.randint(2, 16)
        b2 = c * c + x * x + (-c * x if B == 60 else c * x)
        b = math.isqrt(b2)
        if b * b == b2 and b > c and x != c:
            return B, c, x, b


def _giai_cos_bac_hai(B, c, x, b):
    hs = -c if B == 60 else c           # x^2 + hs.x + (c^2 - b^2) = 0
    td = c * c - b * b
    x2 = -hs - x
    return (r"Let $BC = x\ \left(x > 0\right)$. By the law of cosines: $AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos B$" "\\\\\n"
            r"$\Leftrightarrow %d = %d + x^{2} - 2\cdot %d\cdot x\cdot\left(%s\right) \Leftrightarrow x^{2} %s %dx %s %d = 0$." "\\\\\n"
            r"The equation has two roots $x = %d$ and $x = %d$; since $x > 0$, we have $BC = %d$."
            % (b * b, c * c, c, r"\dfrac{1}{2}" if B == 60 else r"-\dfrac{1}{2}",
               "-" if hs < 0 else "+", abs(hs), "-" if td < 0 else "+", abs(td), x, x2, x))


def L10_C3_B6_TH035_MC_E_01(socau, dang=1):
    r"""Giải tam giác biết hai cạnh và một góc KHÔNG xen giữa: đặt cạnh cần tìm là $x$, định lí
    côsin cho phương trình bậc hai (góc $60^{\circ}$ hoặc $120^{\circ}$, nghiệm nguyên, một nghiệm âm bị loại).

    Mức TH: số liệu chọn để phương trình bậc hai có nghiệm nguyên, nhẩm được.
    CLAUDE THEM 01/10/2026 - theo cau 8 (dam lay) va phan III (mieng bia AB = 8, AC = 13, B = 60)
    tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_cos_bac_hai()
        if v not in gt:
            gt.append(v)
    for B, c, x, b in gt:
        de = r"Given triangle $ABC$ with $AB = %d$, $AC = %d$ and $\widehat{B} = %d^{\circ}$. The length of side $BC$ is" % (c, b, B)
        dap = str(x)
        hs = -c if B == 60 else c
        sai = [str(abs(-hs - x)), _can_gon(b * b + c * c), _can_gon(abs(b * b - c * c)), str(x + 1)]
        nh = _ba_nhieu(dap, sai, buoc=lambda t: str(x + t + 1))
        cau += MC_SA_answer_const(de, dap, nh, _giai_cos_bac_hai(B, c, x, b), 0, 0, dang)
    return cau


def L10_C3_B6_TH035_SA_E_01(socau, dang=2):
    r"""Trả lời ngắn - giải tam giác biết hai cạnh và một góc không xen giữa (định lí côsin ra
    phương trình bậc hai có nghiệm nguyên).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_cos_bac_hai()
        if v not in gt:
            gt.append(v)
    for B, c, x, b in gt:
        de = r"Given triangle $ABC$ with $AB = %d$, $AC = %d$ and $\widehat{B} = %d^{\circ}$. Find the length of side $BC$." % (c, b, B)
        cau += MC_SA_answer_const(de, str(x), [str(x + k) for k in (1, -1, 2)], _giai_cos_bac_hai(B, c, x, b), 0, 0, dang)
    return cau


def _bo_ti_le_sin():
    """Hai kiểu đề: 'p sinA = q sinB = r sinC' hoặc 'x/sinA = y/sinB = z/sinC', cho một cạnh,
    hỏi chu vi. Tỉ lệ cạnh a : b : c nguyên, tam giác hợp lệ."""
    while True:
        u, v, w = sorted(random.sample(range(2, 9), 3))
        ti = [w, v, u]                       # a : b : c
        random.shuffle(ti)
        a_, b_, c_ = ti
        if not (a_ + b_ > c_ and b_ + c_ > a_ and a_ + c_ > b_):
            continue
        if math.gcd(math.gcd(a_, b_), c_) != 1:
            continue
        kieu = random.choice(["tich", "thuong"])
        if kieu == "tich":
            L = a_ * b_ * c_ // math.gcd(math.gcd(a_ * b_, b_ * c_), a_ * c_)
            # p sinA = q sinB = r sinC  <=>  a : b : c = 1/p : 1/q : 1/r ; chọn p = L/a ...
            p, q, r = L // a_, L // b_, L // c_
            if max(p, q, r) > 12 or L % a_ or L % b_ or L % c_:
                continue
            he = (p, q, r)
        else:
            he = (a_, b_, c_)
        k = random.choice([1, 2, 3])
        canh = random.randrange(3)
        return kieu, he, (a_, b_, c_), k, canh


def L10_C3_B6_TH033_MC_E_01(socau, dang=1):
    r"""Định lí sin cho tỉ lệ cạnh $a : b : c = \sin A : \sin B : \sin C$: biết hệ thức giữa các sin
    (dạng $p\sin A = q\sin B = r\sin C$ hoặc $\dfrac{x}{\sin A} = \dfrac{y}{\sin B} = \dfrac{z}{\sin C}$)
    và một cạnh, tính chu vi.

    CLAUDE THEM 01/10/2026 - theo cau 34, 46 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_ti_le_sin()
        if v not in gt:
            gt.append(v)
    for kieu, he, ti, k, canh in gt:
        de, giai, chu_vi, sai = _de_ti_le_sin(kieu, he, ti, k, canh)
        dap = str(chu_vi)
        nh = _ba_nhieu(dap, [str(s) for s in sai], buoc=lambda t: str(chu_vi + t))
        cau += MC_SA_answer_const(de + " The perimeter of triangle $ABC$ is", dap, nh, giai, 0, 0, dang)
    return cau


def _de_ti_le_sin(kieu, he, ti, k, canh):
    ten = ["BC", "CA", "AB"]
    a_, b_, c_ = ti
    canh_that = [k * a_, k * b_, k * c_]
    if kieu == "tich":
        p, q, r = he
        gia = r"$%d\sin A = %d\sin B = %d\sin C$" % (p, q, r)
        b1 = (r"From the given condition, $\sin A : \sin B : \sin C = \dfrac{1}{%d} : \dfrac{1}{%d} : \dfrac{1}{%d} = %d : %d : %d$."
              % (p, q, r, a_, b_, c_))
    else:
        gia = r"$\dfrac{%d}{\sin A} = \dfrac{%d}{\sin B} = \dfrac{%d}{\sin C}$" % he
        b1 = r"From the given condition, $\sin A : \sin B : \sin C = %d : %d : %d$." % (a_, b_, c_)
    de = r"Given triangle $ABC$ satisfying %s and $%s = %d$." % (gia, ten[canh], canh_that[canh])
    chu_vi = sum(canh_that)
    giai = (b1 + "\\\\\n" +
            r"By the law of sines, $a : b : c = \sin A : \sin B : \sin C = %d : %d : %d$ (where $a = BC$, $b = CA$, $c = AB$)." % ti
            + "\\\\\n" +
            r"Since $%s = %d$, each part equals $%d$: $BC = %d$, $CA = %d$, $AB = %d$. The perimeter is $%d$."
            % (ten[canh], canh_that[canh], k, canh_that[0], canh_that[1], canh_that[2], chu_vi))
    he_sai = he if kieu == "tich" else ti
    sai = [k * sum(he_sai) if kieu == "tich" else chu_vi + k, canh_that[canh] * 3, chu_vi + 2 * k, chu_vi - k]
    return de, giai, chu_vi, sai


def L10_C3_B6_TH033_MC_E_02(socau, dang=1):
    r"""Định lí sin cho tỉ số cạnh, cách hỏi khác: biết hai góc $A$, $B$, tính tỉ số hai đường cao
    $\dfrac{h_a}{h_b} = \dfrac{b}{a} = \dfrac{\sin B}{\sin A}$ (dùng thêm $S = \dfrac{1}{2}a h_a$).

    CLAUDE THEM 01/10/2026 - theo cau 32 tai lieu C3-B2. Co Lan duyet lai.
    """
    SIN = {30: Rational(1, 2), 45: sqrt(2) / 2, 60: sqrt(3) / 2, 90: Integer(1), 120: sqrt(3) / 2, 135: sqrt(2) / 2}
    cau, gt = "", []
    while len(gt) < socau:
        A, B = random.sample(list(SIN), 2)
        if A + B >= 180 or SIN[A] == SIN[B] or (A, B) in gt:
            continue
        gt.append((A, B))
    for A, B in gt:
        kq = simplify(SIN[B] / SIN[A])
        de = (r"Given triangle $ABC$ with $\widehat{A} = %d^{\circ}$, $\widehat{B} = %d^{\circ}$. Let $h_a$, $h_b$ be the "
              r"lengths of the altitudes from $A$ and $B$, respectively. The ratio $\dfrac{h_a}{h_b}$ is" % (A, B))
        giai = (r"We have $S = \dfrac{1}{2}a h_a = \dfrac{1}{2}b h_b \Rightarrow \dfrac{h_a}{h_b} = \dfrac{b}{a}$." "\\\\\n"
                r"By the law of sines, $\dfrac{b}{a} = \dfrac{\sin B}{\sin A} = \dfrac{\sin %d^{\circ}}{\sin %d^{\circ}} = "
                r"\dfrac{%s}{%s} = %s$." % (B, A, _L(SIN[B]), _L(SIN[A]), _L(kq)))
        dap = _L(kq)
        nh = _ba_nhieu(dap, [_L(simplify(1 / kq)), _L(SIN[B]), _L(SIN[A]), _L(simplify(2 * kq))])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_SA_E_01(socau, dang=2):
    r"""Trả lời ngắn - tỉ lệ sin cho tỉ lệ cạnh: biết hệ thức giữa $\sin A$, $\sin B$, $\sin C$
    và một cạnh, tính chu vi tam giác.

    CLAUDE THEM 01/10/2026 - theo cau 34, 46 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_ti_le_sin()
        if v not in gt:
            gt.append(v)
    for kieu, he, ti, k, canh in gt:
        de, giai, chu_vi, sai = _de_ti_le_sin(kieu, he, ti, k, canh)
        cau += MC_SA_answer_const(de + " Find the perimeter of triangle $ABC$.", str(chu_vi),
                                  [str(chu_vi + t) for t in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def _bo_hbh(can_nguyen):
    """Hình bình hành ABCD: AB = m, AD = n, góc A = 60 hoặc 120 độ; BD^2 = m^2 + n^2 - 2mn cos A,
    AC^2 = m^2 + n^2 + 2mn cos A."""
    while True:
        A = random.choice([60, 120, 45, 135, 30, 150]) if not can_nguyen else random.choice([60, 120])
        m, n = random.sample(range(2, 11), 2)
        cs = {60: Rational(1, 2), 120: Rational(-1, 2), 45: sqrt(2) / 2, 135: -sqrt(2) / 2,
              30: sqrt(3) / 2, 150: -sqrt(3) / 2}[A]
        BD2 = simplify(m * m + n * n - 2 * m * n * cs)
        AC2 = simplify(m * m + n * n + 2 * m * n * cs)
        hoi = random.choice(["AC", "BD"])
        X2 = AC2 if hoi == "AC" else BD2
        if can_nguyen:
            if not X2.is_Integer or math.isqrt(int(X2)) ** 2 != int(X2):
                continue
        elif not (cs.is_Rational):
            continue
        return A, m, n, cs, hoi, X2


def L10_C3_B6_TH032_MC_I_01(socau, dang=1):
    r"""Định lí côsin trong hình bình hành: biết hai cạnh kề và một góc, tính một đường chéo
    (đường chéo đối diện góc $A$ dùng $\cos A$, đường chéo còn lại dùng góc kề bù $180^{\circ} - A$).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 ("hinh binh hanh A = 60, AB = 5,
    AD = 8, tinh AC"). Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_hbh(False)
        if v[:3] + (v[4],) not in [g[:3] + (g[4],) for g in gt]:
            gt.append(v)
    for A, m, n, cs, hoi, X2 in gt:
        de, giai = _de_hbh(A, m, n, cs, hoi, X2)
        dap = _L(sqrt(X2))
        khac = simplify(2 * (m * m + n * n) - X2)
        nh = _ba_nhieu(dap, [_L(sqrt(khac)), _L(sqrt(m * m + n * n)), _L(X2), str(m + n)])
        cau += MC_SA_answer_const(de + r" The length of diagonal $%s$ is" % hoi, dap, nh, giai, 0, 0, dang)
    return cau


def _de_hbh(A, m, n, cs, hoi, X2):
    de = r"Given parallelogram $ABCD$ with $AB = %d$, $AD = %d$ and $\widehat{BAD} = %d^{\circ}$." % (m, n, A)
    if hoi == "BD":
        giai = (r"In triangle $ABD$: $BD^{2} = AB^{2} + AD^{2} - 2\cdot AB\cdot AD\cdot\cos %d^{\circ} = "
                r"%d + %d - 2\cdot %d\cdot %d\cdot\left(%s\right) = %s$." % (A, m * m, n * n, m, n, _L(cs), _L(X2)))
    else:
        giai = (r"Since $ABCD$ is a parallelogram, $BC = AD = %d$ and $\widehat{ABC} = 180^{\circ} - %d^{\circ} = %d^{\circ}$." "\\\\\n"
                r"In triangle $ABC$: $AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos %d^{\circ} = "
                r"%d + %d - 2\cdot %d\cdot %d\cdot\left(%s\right) = %s$."
                % (n, A, 180 - A, 180 - A, m * m, n * n, m, n, _L(-cs), _L(X2)))
    giai += r" Hence $%s = %s$." % (hoi, _L(sqrt(X2)))
    return de, giai


def L10_C3_B6_VD032_MC_A_01(socau, dang=1):
    r"""LUYỆN TẬP THÊM (công thức trung tuyến - SBT). Hình bình hành, cách hỏi khác: biết một cạnh và hai đường chéo, tính
    cạnh kề. Dùng công thức trung tuyến trong tam giác $ABD$ (tâm $O$ là trung điểm $BD$):
    $AB^{2} + AD^{2} = \dfrac{AC^{2} + BD^{2}}{2}$.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 ("mot canh 4, hai duong cheo 6 va 8").
    01/10/2026: tach tu TH032_MC_I_02 sang TH032_MC_J (ngoai YCCD). Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        p, q = sorted(random.sample(range(4, 17, 2), 2))   # hai đường chéo chẵn để nửa đường chéo nguyên
        m = random.randint(2, 10)
        n2 = Rational(p * p + q * q, 2) - m * m
        if n2 <= 0 or not n2.is_Integer or n2 > 120:
            continue
        n = sqrt(n2)
        # tam giác OAB với OA = p/2, OB = q/2, AB = m phải tồn tại; tương tự cạnh còn lại
        if not (abs(p - q) / 2 < m < (p + q) / 2 and abs(p - q) / 2 < float(n) < (p + q) / 2):
            continue
        if (p, q, m) not in gt:
            gt.append((p, q, m))
    for p, q, m in gt:
        n2 = Rational(p * p + q * q, 2) - m * m
        de = (r"Given parallelogram $ABCD$ with $AB = %d$ and the two diagonals $AC = %d$, $BD = %d$. The length of side $AD$ is"
              % (m, p, q))
        giai = (r"Let $O$ be the intersection of the two diagonals; then $O$ is the midpoint of $BD$, $AO = \dfrac{AC}{2} = %s$." "\\\\\n"
                r"In triangle $ABD$, $AO$ is a median: $AO^{2} = \dfrac{AB^{2} + AD^{2}}{2} - \dfrac{BD^{2}}{4}$" "\\\\\n"
                r"$\Rightarrow AD^{2} = 2AO^{2} + \dfrac{BD^{2}}{2} - AB^{2} = 2\cdot %s + %s - %d = %s$, so $AD = %s$."
                % (_L(Rational(p, 2)), _L(Rational(p * p, 4)), _L(Rational(q * q, 2)), m * m, _L(n2), _L(sqrt(n2))))
        dap = _L(sqrt(n2))
        nh = _ba_nhieu(dap, [_L(sqrt(p * p + q * q - m * m)), _L(sqrt(abs(Rational(p * p + q * q, 4) - m * m))),
                             _L(n2), str(abs(q - m))])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH032_SA_I_01(socau, dang=2):
    r"""Trả lời ngắn - định lí côsin trong hình bình hành: tính một đường chéo (đáp số nguyên).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_hbh(True)
        if v[:3] + (v[4],) not in [g[:3] + (g[4],) for g in gt]:
            gt.append(v)
    for A, m, n, cs, hoi, X2 in gt:
        de, giai = _de_hbh(A, m, n, cs, hoi, X2)
        x = math.isqrt(int(X2))
        cau += MC_SA_answer_const(de + r" Find the length of diagonal $%s$." % hoi, str(x),
                                  [str(x + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def _bo_dien_tich_hbh(can_sa):
    while True:
        thoi = random.random() < 0.5
        A = random.choice([30, 150]) if can_sa else random.choice([30, 45, 60, 120, 135, 150])
        m = random.randint(2, 12)
        n = m if thoi else random.randint(2, 12)
        if not thoi and n == m:
            continue
        sA = {30: Rational(1, 2), 150: Rational(1, 2), 45: sqrt(2) / 2, 135: sqrt(2) / 2,
              60: sqrt(3) / 2, 120: sqrt(3) / 2}[A]
        S = m * n * sA
        if can_sa and (_so_thap_phan_gon(S) is None or len(_so_thap_phan_gon(S)) > 4):
            continue
        return thoi, A, m, n, sA, S


def _de_dien_tich_hbh(thoi, A, m, n, sA, S):
    if thoi:
        de = r"Given rhombus $ABCD$ with side length $%d$ and $\widehat{BAD} = %d^{\circ}$." % (m, A)
    else:
        de = r"Given parallelogram $ABCD$ with $AB = %d$, $AD = %d$ and $\widehat{BAD} = %d^{\circ}$." % (m, n, A)
    giai = (r"Diagonal $BD$ divides the figure into two congruent triangles $ABD$ and $CDB$, so" "\\\\\n"
            r"$S_{ABCD} = 2S_{ABD} = 2\cdot\dfrac{1}{2}\cdot AB\cdot AD\cdot\sin\widehat{BAD} = %d\cdot %d\cdot\sin %d^{\circ} = %s$."
            % (m, n, A, _L(S)))
    return de, giai


def L10_C3_B6_TH034_MC_J_01(socau, dang=1):
    r"""Diện tích hình bình hành, hình thoi biết hai cạnh kề và góc xen giữa:
    $S = 2S_{ABD} = AB\cdot AD\cdot\sin A$.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 ("hinh thoi canh a, goc 30"). Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_dien_tich_hbh(False)
        if v[:4] not in [g[:4] for g in gt]:
            gt.append(v)
    for thoi, A, m, n, sA, S in gt:
        de, giai = _de_dien_tich_hbh(thoi, A, m, n, sA, S)
        dap = _L(S)
        nh = _ba_nhieu(dap, [_L(S / 2), _L(m * n), _L(2 * S), _L(m * n * (sqrt(1 - sA ** 2)))])
        cau += MC_SA_answer_const(de + r" The area of quadrilateral $ABCD$ is", dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_J_01(socau, dang=2):
    r"""Trả lời ngắn - diện tích hình bình hành, hình thoi theo hai cạnh và góc xen giữa.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau, gt = "", []
    while len(gt) < socau:
        v = _bo_dien_tich_hbh(True)
        if v[:4] not in [g[:4] for g in gt]:
            gt.append(v)
    for thoi, A, m, n, sA, S in gt:
        de, giai = _de_dien_tich_hbh(thoi, A, m, n, sA, S)
        dap = _so_thap_phan_gon(S)
        cau += MC_SA_answer_const(de + r" Find the area of quadrilateral $ABCD$.", dap,
                                  [_so_thap_phan_gon(S + k) or str(k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


# =====================================================================
# VD036 - BỐI CẢNH THỰC TIỄN MỚI (CLAUDE THEM 01/10/2026 theo tai lieu C3-B2
# co Lan gui). Moi boi canh: MC + SA muc VD (y a cua tu luan), MC + SA muc VDC
# (y b, "muc_do_dang": "VDC" o Mapping), TL a) VD b) VDC. Cung mo ta "Dang"
# trong mot boi canh de khong ra chung mot de. So lieu sat thuc te.
# =====================================================================

def _m(x, n=0, don_vi=r"\,\text{m}"):
    """Số đo làm tròn n chữ số (n = 0: hàng đơn vị), kèm đơn vị."""
    s = str(_lt(x)) if n == 0 else _x1(x, n)
    return "$%s%s$" % (s, don_vi)


def _so(x, n=0):
    """Đáp số trả lời ngắn: làm tròn kiểu SGK rồi bỏ số 0 thừa ở cuối (4,0 -> 4)."""
    if n == 0:
        return str(_lt(x))
    t = _x1(x, n)
    if DAU_THAP_PHAN in t:
        t = t.rstrip("0").rstrip(DAU_THAP_PHAN)
    return t


# ---------- A. Ngọn núi nhìn từ chân và nóc toà nhà ----------

def _bo_nui_toa_nha():
    """Toà nhà AB thẳng đứng cao h (A chân, B nóc); đỉnh núi C; góc nâng từ A là al, từ B là be
    (be < al). Tam giác ABC: A = 90 - al, B = 90 + be, C = al - be.
    AC = h cos(be)/sin(al - be); chiều cao núi CH = AC sin(al)."""
    while True:
        h = random.choice([50, 60, 70, 80])
        al = random.choice([26, 28, 30, 32, 34, 35])
        be = al - random.choice([10, 12, 14, 15])
        AC = h * _cos_d(be) / _sin_d(al - be)
        CH = AC * _sin_d(al)
        if 100 <= CH <= 400 and _xa_bien(AC) and _xa_bien(CH) and _xa_bien(CH, 1):
            return h, al, be, AC, CH


def _hinh_nui_toa_nha(h, al, be, CH):
    k = 3.0 / CH
    hb = max(h * k, 0.55)
    yc = CH * k
    xc = yc / math.tan(math.radians(al))
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
        "\\fill[green!15] (%.2f,0) -- (%.2f,%.2f) -- (%.2f,0) -- cycle;\n" % (xc - 1.6, xc, yc, xc + 1.4)
        + "\\draw (%.2f,0) -- (%.2f,%.2f) -- (%.2f,0);\n" % (xc - 1.6, xc, yc, xc + 1.4)
        + "\\draw (-0.6,0) -- (%.2f,0);\n" % (xc + 1.6)
        + "\\fill[black!20] (-0.35,0) rectangle (0,%.2f);\n\\draw (-0.35,0) rectangle (0,%.2f);\n" % (hb, hb)
        + "\\draw[dashed] (0,%.2f) -- (%.2f,%.2f);\n" % (hb, xc, hb)
        + "\\draw[dashed] (%.2f,%.2f) -- (%.2f,0);\n" % (xc, yc, xc)
        + "\\draw[thick,red] (0,0) -- (%.2f,%.2f) (0,%.2f) -- (%.2f,%.2f);\n" % (xc, yc, hb, xc, yc)
        + "\\draw (0.75,0) arc (0:%.1f:0.75);\n" % al
        + "\\node at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (1.05 * _cos_d(al / 2) + 0.05, 1.05 * _sin_d(al / 2), al)
        + "\\draw (0.95,%.2f) arc (0:%.1f:0.95);\n" % (hb, be)
        + "\\node at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (1.3 * _cos_d(be / 2) + 0.1, hb + 1.3 * _sin_d(be / 2), be)
        + "\\fill (0,0) circle (0.03) node[below] {$A$};\n"
        "\\fill (0,%.2f) circle (0.03) node[above left] {$B$};\n" % hb
        + "\\fill (%.2f,%.2f) circle (0.03) node[above] {$C$};\n" % (xc, yc)
        + "\\fill (%.2f,0) circle (0.03) node[below] {$H$};\n" % xc
        + "\\end{tikzpicture}"
    )


def _de_nui_toa_nha(h, al, be):
    return (r"From two positions $A$ and $B$ on a building, the summit $C$ of a mountain is observed. Here $A$ is the "
            r"foot of the building on the ground, $B$ is the top of the building, $AB$ is perpendicular to the ground and $AB = %d\,\text{m}$; "
            r"the line of sight $AC$ makes an angle of $%s$ with the horizontal, and the line of sight $BC$ makes an angle of "
            r"$%s$ with the horizontal (see figure). Let $H$ be the projection of $C$ onto the ground." % (h, _goc(al), _goc(be)))


def _giai_goc_nui(h, al, be, AC):
    return (r"In triangle $ABC$: $\widehat{BAC} = 90^{\circ} - %s = %s$ (the angle between the vertical $AB$ and $AC$); "
            r"$\widehat{ABC} = 90^{\circ} + %s = %s$; hence $\widehat{ACB} = 180^{\circ} - %s - %s = %s$." "\\\\\n"
            r"By the law of sines: $\dfrac{AC}{\sin\widehat{ABC}} = \dfrac{AB}{\sin\widehat{ACB}} \Rightarrow "
            r"AC = \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$."
            % (_goc(al), _goc(90 - al), _goc(be), _goc(90 + be), _goc(90 - al), _goc(90 + be), _goc(al - be),
               h, _goc(90 + be), _goc(al - be), _x1(AC, 1)))


def _giai_cao_nui(al, CH, AC):
    return (r"Triangle $ACH$ is right-angled at $H$ with $\widehat{CAH} = %s$, so $CH = AC\cdot\sin %s \approx %s\,\text{(m)}$."
            % (_goc(al), _goc(al), _x1(CH, 1)))


def L10_C3_B6_VD036_MC_N_01(socau, dang=1):
    r"""Ngọn núi quan sát từ chân và nóc toà nhà (mức VD): tính khoảng cách $AC$ từ chân toà nhà tới
    đỉnh núi bằng định lí sin (có hình).

    CLAUDE THEM 01/10/2026 - theo cau 60-62 tai lieu C3-B2 (AB = 70 m, 30 do, 15 do 30'). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        dap = _m(AC)
        sai = [h * _cos_d(be) / _sin_d(al + be), h * _sin_d(be) / _sin_d(al - be), CH, h / _sin_d(al - be)]
        nh = _ba_nhieu(dap, [_m(x) for x in sai], buoc=lambda t: _m(AC + 7 * t))
        de = _de_nui_toa_nha(h, al, be) + r" The distance $AC$ (rounded to the nearest whole number) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_goc_nui(h, al, be, AC),
                                  _hinh_nui_toa_nha(h, al, be, CH), 0, dang)
    return cau


def L10_C3_B6_VD036_MC_O_01(socau, dang=1):
    r"""Ngọn núi quan sát từ chân và nóc toà nhà (mức VDC): tính chiều cao $CH$ của ngọn núi - định lí
    sin trong tam giác $ABC$ rồi tam giác vuông $ACH$ (có hình).

    CLAUDE THEM 01/10/2026 - theo cau 60-62 tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        dap = _m(CH)
        sai = [AC, AC * _cos_d(al), CH + h, h * _cos_d(be) / _sin_d(al + be) * _sin_d(al)]
        nh = _ba_nhieu(dap, [_m(x) for x in sai], buoc=lambda t: _m(CH + 5 * t))
        de = _de_nui_toa_nha(h, al, be) + r" The height $CH$ of the mountain (rounded to the nearest whole number) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh],
                                  _giai_goc_nui(h, al, be, AC) + "\\\\\n" + _giai_cao_nui(al, CH, AC),
                                  _hinh_nui_toa_nha(h, al, be, CH), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_N_01(socau, dang=2):
    r"""Trả lời ngắn - ngọn núi quan sát từ chân và nóc toà nhà (mức VD): tính $AC$ (m, hàng đơn vị).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        dap = _so(AC)
        de = _de_nui_toa_nha(h, al, be) + r" Find the distance $AC$ (in meters, rounded to the nearest whole number)."
        cau += MC_SA_answer_const(de, dap, [str(int(dap) + k) for k in (1, -1, 2)], _giai_goc_nui(h, al, be, AC),
                                  _hinh_nui_toa_nha(h, al, be, CH), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_O_01(socau, dang=2):
    r"""Trả lời ngắn - ngọn núi quan sát từ chân và nóc toà nhà (mức VDC): chiều cao ngọn núi.

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        dap = _so(CH)
        de = _de_nui_toa_nha(h, al, be) + r" Find the height $CH$ of the mountain (in meters, rounded to the nearest whole number)."
        cau += MC_SA_answer_const(de, dap, [str(int(dap) + k) for k in (1, -1, 2)],
                                  _giai_goc_nui(h, al, be, AC) + "\\\\\n" + _giai_cao_nui(al, CH, AC),
                                  _hinh_nui_toa_nha(h, al, be, CH), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_J_01(socau, dong=1):
    r"""Tự luận - ngọn núi quan sát từ chân và nóc toà nhà.
    a) (VD) Tính các góc của tam giác $ABC$ và khoảng cách $AC$. b) (VDC) Tính chiều cao ngọn núi.

    CLAUDE THEM 01/10/2026 - theo cau 60-62 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        ds = [(r"Find the measures of the angles of triangle $ABC$ and the distance $AC$ (round to the nearest tenth, in meters).",
               r"AC \approx %s\,\text{m}" % _x1(AC, 1), _giai_goc_nui(h, al, be, AC)),
              (r"Find the height $CH$ of the mountain above the ground (round to the nearest tenth, in meters).",
               r"CH \approx %s\,\text{m}" % _x1(CH, 1), _giai_cao_nui(al, CH, AC))]
        cau += TL_answer_text(_de_nui_toa_nha(h, al, be), ds, _hinh_nui_toa_nha(h, al, be, CH), 0, dong)
    return cau


# ---------- B. Đường tròn qua ba điểm: đĩa cổ bị vỡ, hồ nước hình tròn ----------

def _bo_dia_co():
    """Đĩa cổ bán kính thật 5-12 cm; ba điểm trên mép đĩa. Cạnh làm tròn 1 chữ số thập phân,
    R TÍNH LẠI từ chính các cạnh đã làm tròn (đề cho số nào, đáp số theo số đó)."""
    while True:
        R0 = random.uniform(5, 12)
        A, B = random.randint(40, 80), random.randint(35, 75)
        C = 180 - A - B
        if C < 30 or C > 100:
            continue
        a, b, c = (round(2 * R0 * _sin_d(x), 1) for x in (A, B, C))
        p = (a + b + c) / 2
        S2 = p * (p - a) * (p - b) * (p - c)
        if S2 <= 0:
            continue
        S = math.sqrt(S2)
        R = a * b * c / (4 * S)
        lon = max((a, "A"), (b, "B"), (c, "C"))
        cos_lon = {"A": (b * b + c * c - a * a) / (2 * b * c), "B": (a * a + c * c - b * b) / (2 * a * c),
                   "C": (a * a + b * b - c * c) / (2 * a * b)}[lon[1]]
        goc_lon = math.degrees(math.acos(cos_lon))
        if _xa_bien(R, 1) and _xa_bien(S, 1) and _xa_bien(goc_lon):
            return a, b, c, p, S, R, lon[1], goc_lon


def _de_dia_co(a, b, c):
    return (r"While excavating an ancient tomb, archaeologists found a broken circular ancient plate. To reconstruct "
            r"the shape of the plate, they took three points $A$, $B$, $C$ on its rim and measured "
            r"$BC = %s\,\text{cm}$, $CA = %s\,\text{cm}$, $AB = %s\,\text{cm}$ (see figure)."
            % (_x1(a, 1), _x1(b, 1), _x1(c, 1)))


def _hinh_duong_tron_ba_diem(goc, nhan, ho=False):
    """Ba điểm trên đường tròn ở các góc (độ, theo tâm) cho trước; ho=True tô màu hồ nước."""
    pts = [(1.5 * math.cos(math.radians(g)), 1.5 * math.sin(math.radians(g))) for g in goc]
    if ho:
        mat = "\\fill[blue!12] (0,0) circle (1.5);\n\\draw (0,0) circle (1.5);\n"
    else:
        # Đĩa vỡ: phần MẤT (nét đứt) nằm giữa hai điểm liền kề cách xa nhau nhất, chừa mép 15 độ
        # mỗi bên => cả ba điểm A, B, C luôn nằm trên phần đĩa còn nguyên (nét liền).
        gs = sorted(g % 360 for g in goc)
        khe = [((gs[(i + 1) % 3] - gs[i]) % 360 or 360, gs[i]) for i in range(3)]
        rong, dau = max(khe)
        le = min(15.0, rong / 4)
        s0, e0 = dau + le, dau + rong - le          # cung đứt: s0 -> e0
        mat = ("\\draw[dashed] (%.3f:1.5) arc (%.3f:%.3f:1.5);\n"
               "\\draw[thick] (%.3f:1.5) arc (%.3f:%.3f:1.5);\n" % (s0, s0, e0, e0, e0, s0 + 360))
    hinh = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n" + mat
    hinh += "\\draw[thick] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f)%s;\n" % (
        pts[1] + pts[0] + pts[2] + ("" if ho else " -- cycle",))
    for (x, y), t in zip(pts, nhan):
        hinh += "\\fill (%.3f,%.3f) circle (0.04) node[%s] {$%s$};\n" % (
            x, y, "above" if y > 0.3 else ("below" if y < -0.3 else ("right" if x > 0 else "left")), t)
    return hinh + "\\end{tikzpicture}"


def _giai_dia_co(a, b, c, p, S, R):
    return (r"The radius of the plate equals the circumradius $R$ of triangle $ABC$." "\\\\\n"
            r"Semiperimeter $p = \dfrac{%s + %s + %s}{2} = %s$; by Heron's formula "
            r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} \approx %s\,\left(\text{cm}^{2}\right)$." "\\\\\n"
            r"From $S = \dfrac{abc}{4R}$ we get $R = \dfrac{abc}{4S} \approx \dfrac{%s\cdot %s\cdot %s}{4\cdot %s} \approx %s\,\text{(cm)}$."
            % (_x1(a, 1), _x1(b, 1), _x1(c, 1), _xx(p, 2), _x1(S, 2), _x1(a, 1), _x1(b, 1), _x1(c, 1), _x1(S, 2), _x1(R, 1)))


def _bo_ho_tron():
    """Hồ hình tròn, đường kính thật 20-60 m; A, B, C trên bờ hồ, đo AB, AC và góc BAC (tù)."""
    while True:
        A = random.choice([120, 125, 130, 135, 140, 145])
        AB, AC = random.randint(6, 20), random.randint(8, 24)
        if AB == AC:
            continue
        BC = math.sqrt(AB * AB + AC * AC - 2 * AB * AC * _cos_d(A))
        d = BC / _sin_d(A)
        if 20 <= d <= 60 and _xa_bien(d) and _xa_bien(BC, 1) and _xa_bien(d / 2, 1):
            return A, AB, AC, BC, d


def _de_ho_tron(A, AB, AC):
    return (r"To measure the diameter of a circular lake, three points $A$, $B$, $C$ on the shore are chosen and "
            r"$AB = %d\,\text{m}$, $AC = %d\,\text{m}$, $\widehat{BAC} = %s$ are measured (see figure)." % (AB, AC, _goc(A)))


def _giai_ho_bc(A, AB, AC, BC):
    return (r"By the law of cosines: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos %s = %d + %d - 2\cdot %d\cdot %d\cdot\cos %s$, "
            r"so $BC \approx %s\,\text{(m)}$." % (_goc(A), AB * AB, AC * AC, AB, AC, _goc(A), _x1(BC, 2)))


def _giai_ho_d(A, BC, d):
    return (r"The lake is the circumscribed circle of triangle $ABC$. By the law of sines: $\dfrac{BC}{\sin A} = 2R = d$, so the "
            r"diameter is $d = \dfrac{BC}{\sin %s} \approx %s\,\text{(m)}$." % (_goc(A), _x1(d, 1)))


def _goc_ve_ho(A, AB, AC):
    """Vị trí (độ, theo tâm) của A, B, C trên bờ hồ để HÌNH KHỚP SỐ LIỆU: góc BAC đúng bằng A và
    tỉ lệ AB : AC đúng như đề (A đặt ở đỉnh, 90 độ).
    Góc nội tiếp: dây đối diện góc X chắn cung 2X ở tâm => cung AB = 2C, cung AC = 2B,
    cung BC (không chứa A) = 2A (A tù thì cung này > 180 độ, A nằm trên cung nhỏ BC)."""
    BC2 = AB * AB + AC * AC - 2 * AB * AC * _cos_d(A)
    BC = math.sqrt(BC2)
    B = math.degrees(math.acos((AB * AB + BC2 - AC * AC) / (2 * AB * BC)))   # góc B (đối diện AC)
    C = 180 - A - B
    return [90, 90 + 2 * C, 90 - 2 * B]      # B ở bên trái, C ở bên phải (AB < AC thì B gần A hơn)


def L10_C3_B6_VD036_MC_P_01(socau, dang=1):
    r"""Đĩa cổ bị vỡ (mức VD): biết ba khoảng cách giữa ba điểm trên mép đĩa, tính số đo góc lớn nhất
    của tam giác (hệ quả định lí côsin) - có hình.

    CLAUDE THEM 01/10/2026 - theo cau 56 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        a, b, c, p, S, R, dinh, g = _bo_dia_co()
        doi = {"A": "BC", "B": "CA", "C": "AB"}[dinh]
        dap = r"%d^{\circ}" % _lt(g)
        nh = _ba_nhieu(dap, [r"%d^{\circ}" % _lt(180 - g), r"%d^{\circ}" % _lt(g - 10), r"%d^{\circ}" % _lt(g + 8)],
                       buoc=lambda t: r"%d^{\circ}" % (_lt(g) + 3 * t))
        de = (_de_dia_co(a, b, c) + r" The measure of the largest angle of triangle $ABC$ (rounded to the nearest degree) is")
        giai = (r"The largest angle is the angle opposite the longest side $%s$, that is, angle $%s$. By the corollary of the law of cosines, "
                r"$\cos %s \approx %s$, so $\widehat{%s} \approx %s$."
                % (doi, dinh, dinh, _xx(math.cos(math.radians(g)), 4), dinh, dap))
        cau += MC_SA_answer_const(de, dap, nh, giai, _hinh_duong_tron_ba_diem([100, 220, 330], "ABC"), 0, dang)
    return cau


def L10_C3_B6_VD036_MC_P_02(socau, dang=1):
    r"""Hồ nước hình tròn (mức VD): biết $AB$, $AC$ và góc $BAC$ (ba điểm trên bờ hồ), tính $BC$ bằng
    định lí côsin - có hình.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 (AB = 8,5 m; AC = 11,5 m; A = 141 do). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        A, AB, AC, BC, d = _bo_ho_tron()
        dap = _m(BC, 1)
        sai = [math.sqrt(AB * AB + AC * AC), math.sqrt(abs(AB * AB + AC * AC + 2 * AB * AC * _cos_d(A))), AB + AC - 1, d]
        nh = _ba_nhieu(dap, [_m(x, 1) for x in sai], buoc=lambda t: _m(BC + 1.3 * t, 1))
        de = _de_ho_tron(A, AB, AC) + r" The distance $BC$ (rounded to the nearest tenth) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_ho_bc(A, AB, AC, BC),
                                  _hinh_duong_tron_ba_diem(_goc_ve_ho(A, AB, AC), "ABC", ho=True), 0, dang)
    return cau


def L10_C3_B6_VD036_MC_Q_01(socau, dang=1):
    r"""Đĩa cổ bị vỡ (mức VDC): tính bán kính đĩa - Heron rồi $R = \dfrac{abc}{4S}$ (có hình).

    CLAUDE THEM 01/10/2026 - theo cau 56 tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        a, b, c, p, S, R, dinh, g = _bo_dia_co()
        dap = _m(R, 1, r"\,\text{cm}")
        sai = [2 * R, R / 2, a * b * c / (2 * S) / 2 + 0.6, a * b * c / S / 4 * 1.25]
        nh = _ba_nhieu(dap, [_m(x, 1, r"\,\text{cm}") for x in sai], buoc=lambda t: _m(R + 0.4 * t, 1, r"\,\text{cm}"))
        de = _de_dia_co(a, b, c) + r" The radius of the plate (rounded to the nearest tenth) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_dia_co(a, b, c, p, S, R),
                                  _hinh_duong_tron_ba_diem([100, 220, 330], "ABC"), 0, dang)
    return cau


def L10_C3_B6_VD036_MC_Q_02(socau, dang=1):
    r"""Hồ nước hình tròn (mức VDC): tính đường kính hồ - định lí côsin tính $BC$ rồi định lí sin
    $d = 2R = \dfrac{BC}{\sin A}$ (có hình).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        A, AB, AC, BC, d = _bo_ho_tron()
        dap = _m(d)
        nh = _ba_nhieu(dap, [_m(d / 2), _m(BC), _m(BC / _cos_d(180 - A)), _m(2 * d)], buoc=lambda t: _m(d + 3 * t))
        de = _de_ho_tron(A, AB, AC) + r" The diameter of the lake (rounded to the nearest whole number) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh],
                                  _giai_ho_bc(A, AB, AC, BC) + "\\\\\n" + _giai_ho_d(A, BC, d),
                                  _hinh_duong_tron_ba_diem(_goc_ve_ho(A, AB, AC), "ABC", ho=True), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_P_01(socau, dang=2):
    r"""Trả lời ngắn - đường tròn qua ba điểm (mức VD): đĩa cổ - góc lớn nhất (độ), hoặc hồ nước - $BC$ (m).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.5:
            a, b, c, p, S, R, dinh, g = _bo_dia_co()
            doi = {"A": "BC", "B": "CA", "C": "AB"}[dinh]
            dap = str(_lt(g))
            de = _de_dia_co(a, b, c) + r" Find the measure of the largest angle of triangle $ABC$ (in degrees, rounded to the nearest whole number)."
            giai = (r"The largest angle is opposite the longest side $%s$: by the corollary of the law of cosines, $\cos %s \approx %s$, "
                    r"so $\widehat{%s} \approx %s^{\circ}$." % (doi, dinh, _xx(math.cos(math.radians(g)), 4), dinh, dap))
            hinh = _hinh_duong_tron_ba_diem([100, 220, 330], "ABC")
        else:
            A, AB, AC, BC, d = _bo_ho_tron()
            dap = _so(BC, 1)
            de = _de_ho_tron(A, AB, AC) + r" Find the distance $BC$ (in meters, rounded to the nearest tenth)."
            giai = _giai_ho_bc(A, AB, AC, BC)
            hinh = _hinh_duong_tron_ba_diem(_goc_ve_ho(A, AB, AC), "ABC", ho=True)
        cau += MC_SA_answer_const(de, dap, [dap + "1", "1" + dap, "2" + dap], giai, hinh, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_Q_01(socau, dang=2):
    r"""Trả lời ngắn - đường tròn qua ba điểm (mức VDC): bán kính đĩa cổ (cm) hoặc đường kính hồ (m).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.5:
            a, b, c, p, S, R, dinh, g = _bo_dia_co()
            dap = _so(R, 1)
            de = _de_dia_co(a, b, c) + r" Find the radius of the plate (in centimeters, rounded to the nearest tenth)."
            giai, hinh = _giai_dia_co(a, b, c, p, S, R), _hinh_duong_tron_ba_diem([100, 220, 330], "ABC")
        else:
            A, AB, AC, BC, d = _bo_ho_tron()
            dap = _so(d)
            de = _de_ho_tron(A, AB, AC) + r" Find the diameter of the lake (in meters, rounded to the nearest whole number)."
            giai = _giai_ho_bc(A, AB, AC, BC) + "\\\\\n" + _giai_ho_d(A, BC, d)
            hinh = _hinh_duong_tron_ba_diem(_goc_ve_ho(A, AB, AC), "ABC", ho=True)
        cau += MC_SA_answer_const(de, dap, [dap + "1", "1" + dap, "2" + dap], giai, hinh, 0, dang)
    return cau


def L10_C3_B6_VD036_TL_K_01(socau, dong=1):
    r"""Tự luận - đĩa cổ bị vỡ. a) (VD) Tính số đo góc lớn nhất của tam giác $ABC$. b) (VDC) Tính bán kính đĩa.

    CLAUDE THEM 01/10/2026 - theo cau 56 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        a, b, c, p, S, R, dinh, g = _bo_dia_co()
        doi = {"A": "BC", "B": "CA", "C": "AB"}[dinh]
        ds = [(r"Find the measure of the largest angle of triangle $ABC$ (round to the nearest degree).",
               r"\widehat{%s} \approx %d^{\circ}" % (dinh, _lt(g)),
               r"The largest angle is opposite the longest side $%s$: $\cos %s \approx %s$ (corollary of the law of cosines), so "
               r"$\widehat{%s} \approx %d^{\circ}$." % (doi, dinh, _xx(math.cos(math.radians(g)), 4), dinh, _lt(g))),
              (r"Find the radius of the disc (round to the nearest tenth, in centimeters).",
               r"R \approx %s\,\text{cm}" % _x1(R, 1), _giai_dia_co(a, b, c, p, S, R))]
        cau += TL_answer_text(_de_dia_co(a, b, c), ds, _hinh_duong_tron_ba_diem([100, 220, 330], "ABC"), 0, dong)
    return cau


def L10_C3_B6_VD036_TL_K_02(socau, dong=1):
    r"""Tự luận - hồ nước hình tròn. a) (VD) Tính $BC$. b) (VDC) Tính đường kính hồ.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        A, AB, AC, BC, d = _bo_ho_tron()
        ds = [(r"Find the distance $BC$ (round to the nearest tenth, in meters).",
               r"BC \approx %s\,\text{m}" % _x1(BC, 1), _giai_ho_bc(A, AB, AC, BC)),
              (r"Find the diameter of the lake (round to the nearest whole number, in meters).",
               r"d \approx %d\,\text{m}" % _lt(d), _giai_ho_d(A, BC, d))]
        cau += TL_answer_text(_de_ho_tron(A, AB, AC), ds, _hinh_duong_tron_ba_diem(_goc_ve_ho(A, AB, AC), "ABC", ho=True), 0, dong)
    return cau


# ---------- C. Cây bị gãy ----------

def _bo_cay_gay():
    """A gốc cây, C chỗ gãy, B ngọn cây chạm đất; đo AB, góc CAB và góc CBA.
    AC = AB sin B / sin C, BC = AB sin A / sin C; chiều cao trước khi gãy AC + BC (8-16 m)."""
    while True:
        AB = random.choice([4, 4.5, 5, 5.5, 6, 6.5, 7, 8])
        A = random.choice([70, 72, 75, 76, 78, 80, 85])
        B = random.choice([30, 32, 35, 38, 40, 42])
        C = 180 - A - B
        AC = AB * _sin_d(B) / _sin_d(C)
        BC = AB * _sin_d(A) / _sin_d(C)
        H = AC + BC
        if 7 <= H <= 16 and _xa_bien(AC, 1) and _xa_bien(BC, 1) and _xa_bien(H, 1):
            return AB, A, B, C, AC, BC, H


def _hinh_cay_gay(AB, A, B, AC):
    k = 3.2 / max(AB, AC)
    xb = AB * k
    xc, yc = AC * k * _cos_d(A), AC * k * _sin_d(A)
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
        "\\draw (-0.5,0) -- (%.2f,0);\n" % (xb + 0.5)
        + "\\draw[line width=2.2pt,brown!70!black] (0,0) -- (%.3f,%.3f);\n" % (xc, yc)
        + "\\draw[line width=1.6pt,brown!70!black] (%.3f,%.3f) -- (%.3f,0);\n" % (xc, yc, xb)
        + "\\fill[green!50!black,opacity=0.6] (%.3f,0.08) circle (0.18);\n" % (xb - 0.1)
        + "\\draw[dashed] (0,0) -- (%.3f,0);\n" % xb
        + "\\draw (0.45,0) arc (0:%.1f:0.45);\n" % A
        + "\\node at (%.3f,%.3f) {$%d^{\\circ}$};\n" % (0.75 * _cos_d(A / 2), 0.75 * _sin_d(A / 2), A)
        + "\\draw (%.3f,0) arc (180:%.1f:0.5);\n" % (xb - 0.5, 180 - B)
        + "\\node at (%.3f,%.3f) {$%d^{\\circ}$};\n" % (xb - 0.85 * _cos_d(B / 2), 0.85 * _sin_d(B / 2), B)
        + "\\fill (0,0) circle (0.04) node[below] {$A$};\n"
        "\\fill (%.3f,0) circle (0.04) node[below] {$B$};\n" % xb
        + "\\fill (%.3f,%.3f) circle (0.04) node[above] {$C$};\n" % (xc, yc)
        + "\\end{tikzpicture}"
    )


def _de_cay_gay(AB, A, B):
    return (r"A tree growing on flat ground is partly broken by a strong wind: the top falls down, the treetop "
            r"$B$ touches the ground, and the break point $C$ stays attached (see figure). The distance from the base $A$ of the tree to the treetop "
            r"is measured as $AB = %s\,\text{m}$ and the angles are $\widehat{CAB} = %s$, $\widehat{CBA} = %s$. Assume the break does not "
            r"change the total length of the trunk." % (_xx(AB, 1), _goc(A), _goc(B)))


def _giai_cay_gay(AB, A, B, C, AC, BC, ca_hai):
    s = (r"$\widehat{ACB} = 180^{\circ} - %s - %s = %s$. By the law of sines: "
         r"$\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$." "\\\\\n"
         r"$AC = \dfrac{%s\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$"
         % (_goc(A), _goc(B), _goc(C), _xx(AB, 1), _goc(B), _goc(C), _x1(AC, 2)))
    if ca_hai:
        s += (r"; $BC = \dfrac{%s\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$." "\\\\\n"
              r"The height of the tree before it broke is $AC + BC \approx %s\,\text{(m)}$."
              % (_xx(AB, 1), _goc(A), _goc(C), _x1(BC, 2), _x1(AC + BC, 1)))
    else:
        s += "."
    return s


def L10_C3_B6_VD036_MC_R_01(socau, dang=1):
    r"""Cây bị gãy (mức VD): tính độ dài đoạn thân còn đứng $AC$ (định lí sin, có hình).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 (AB = 6 m, 76 do, 35 do). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        dap = _m(AC, 1)
        nh = _ba_nhieu(dap, [_m(BC, 1), _m(AB * _sin_d(B), 1), _m(AB * _cos_d(B) / _sin_d(C), 1), _m(H, 1)],
                       buoc=lambda t: _m(AC + 0.4 * t, 1))
        de = _de_cay_gay(AB, A, B) + r" The length of the part $AC$ of the trunk that is still standing (rounded to the nearest tenth) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_cay_gay(AB, A, B, C, AC, BC, False),
                                  _hinh_cay_gay(AB, A, B, AC), 0, dang)
    return cau


def L10_C3_B6_VD036_MC_S_01(socau, dang=1):
    r"""Cây bị gãy (mức VDC): tính chiều cao cây trước khi gãy $AC + BC$ (định lí sin hai lần, có hình).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        dap = _m(H, 1)
        nh = _ba_nhieu(dap, [_m(AC + AB, 1), _m(BC, 1), _m(BC + AB, 1), _m(H + 1.2, 1)], buoc=lambda t: _m(H + 0.7 * t, 1))
        de = _de_cay_gay(AB, A, B) + r" The height of the tree before it was broken (rounded to the nearest tenth) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_cay_gay(AB, A, B, C, AC, BC, True),
                                  _hinh_cay_gay(AB, A, B, AC), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_R_01(socau, dang=2):
    r"""Trả lời ngắn - cây bị gãy (mức VD): độ dài đoạn thân còn đứng $AC$.

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        dap = _so(AC, 1)
        de = _de_cay_gay(AB, A, B) + r" Find the length of the part $AC$ of the trunk that is still standing (in meters, rounded to the nearest tenth)."
        cau += MC_SA_answer_const(de, dap, [_so(AC + k, 1) for k in (0.1, -0.1, 0.2)],
                                  _giai_cay_gay(AB, A, B, C, AC, BC, False), _hinh_cay_gay(AB, A, B, AC), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_S_01(socau, dang=2):
    r"""Trả lời ngắn - cây bị gãy (mức VDC): chiều cao cây trước khi gãy.

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        dap = _so(H, 1)
        de = _de_cay_gay(AB, A, B) + r" Find the height of the tree before it was broken (in meters, rounded to the nearest tenth)."
        cau += MC_SA_answer_const(de, dap, [_so(H + k, 1) for k in (0.1, -0.1, 0.2)],
                                  _giai_cay_gay(AB, A, B, C, AC, BC, True), _hinh_cay_gay(AB, A, B, AC), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_L_01(socau, dong=1):
    r"""Tự luận - cây bị gãy. a) (VD) Tính $AC$. b) (VDC) Tính chiều cao cây trước khi gãy.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        ds = [(r"Find the length of the part $AC$ of the trunk that is still standing (round to the nearest tenth, in meters).",
               r"AC \approx %s\,\text{m}" % _x1(AC, 1), _giai_cay_gay(AB, A, B, C, AC, BC, False)),
              (r"Find the height of the tree before it was broken (round to the nearest tenth, in meters).",
               r"AC + BC \approx %s\,\text{m}" % _x1(H, 1),
               r"$BC = \dfrac{%s\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$, so the height of the tree before it broke is "
               r"$AC + BC \approx %s\,\text{(m)}$." % (_xx(AB, 1), _goc(A), _goc(C), _x1(BC, 2), _x1(H, 1)))]
        cau += TL_answer_text(_de_cay_gay(AB, A, B), ds, _hinh_cay_gay(AB, A, B, AC), 0, dong)
    return cau


# ---------- D. Cây cao nhìn từ một điểm trên cao ----------

def _bo_cay_cao():
    """Người quan sát ở A cao AH so với mặt đất (H là chân), gốc cây B cách H một đoạn HB, ngọn C.
    Góc BAC = al. Tam giác ABC: góc ABC = 90 + góc(ABH)... ở đây góc giữa BA và BC thẳng đứng là
    90 - phi với tan(phi) = AH/HB; góc ACB = 180 - al - (90 - phi); BC = AB sin(al)/sin(ACB)."""
    while True:
        AH = random.choice([3, 4, 5, 6])
        HB = random.choice([15, 18, 20, 24, 25, 30])
        al = random.choice([40, 42, 45, 48, 50])
        phi = math.degrees(math.atan(AH / HB))
        B = 90 - phi
        C = 180 - al - B
        AB = math.hypot(AH, HB)
        BC = AB * _sin_d(al) / _sin_d(C)
        if 10 <= BC <= 30 and _xa_bien(BC, 1) and _xa_bien(C, 1):
            return AH, HB, al, phi, B, C, AB, BC


def _hinh_cay_cao(AH, HB, BC):
    k = 3.0 / max(HB, BC)
    xa, ya, xb, yc = 0, AH * k, HB * k, BC * k
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
        "\\draw (-0.4,0) -- (%.2f,0);\n" % (xb + 0.5)
        + "\\draw[very thick] (0,0) -- (0,%.3f);\n" % ya
        + "\\draw[line width=2pt,brown!70!black] (%.3f,0) -- (%.3f,%.3f);\n" % (xb, xb, yc)
        + "\\fill[green!50!black,opacity=0.5] (%.3f,%.3f) circle (0.35);\n" % (xb, yc)
        + "\\draw (0,%.3f) -- (%.3f,0) (0,%.3f) -- (%.3f,%.3f);\n" % (ya, xb, ya, xb, yc)
        + "\\fill (0,%.3f) circle (0.04) node[left] {$A$};\n" % ya
        + "\\fill (0,0) circle (0.04) node[below] {$H$};\n"
        "\\fill (%.3f,0) circle (0.04) node[below] {$B$};\n" % xb
        + "\\fill (%.3f,%.3f) circle (0.04) node[right] {$C$};\n" % (xb, yc)
        + "\\end{tikzpicture}"
    )


def _de_cay_cao(AH, HB, al):
    return (r"From a point $A$ at height $AH = %d\,\text{m}$ above the ground, a person observes a tall tree growing vertically with base $B$ "
            r"and top $C$ (see figure). Given $HB = %d\,\text{m}$ ($H$ and $B$ lie on level ground) and "
            r"$\widehat{BAC} = %s$." % (AH, HB, _goc(al)))


def _giai_cay_cao_a(AH, HB, al, phi, B, C, AB):
    return (r"Triangle $AHB$ is right-angled at $H$: $AB = \sqrt{%d^{2} + %d^{2}} = %s$ and $\tan\widehat{ABH} = \dfrac{%d}{%d}$, "
            r"so $\widehat{ABH} \approx %s^{\circ}$." "\\\\\n"
            r"Since the tree is vertical, $\widehat{ABC} = 90^{\circ} - \widehat{ABH} \approx %s^{\circ}$; "
            r"$\widehat{ACB} = 180^{\circ} - %s - \widehat{ABC} \approx %s^{\circ}$."
            % (AH, HB, _L(sqrt(AH * AH + HB * HB)), AH, HB, _xx(phi, 2), _xx(B, 2), _goc(al), _xx(C, 2)))


def _giai_cay_cao_b(al, C, AB, BC):
    return (r"By the law of sines in triangle $ABC$: $\dfrac{BC}{\sin\widehat{BAC}} = \dfrac{AB}{\sin\widehat{ACB}}$ "
            r"$\Rightarrow BC = \dfrac{AB\cdot\sin %s}{\sin\widehat{ACB}} \approx %s\,\text{(m)}$." % (_goc(al), _x1(BC, 1)))


def L10_C3_B6_VD036_MC_T_01(socau, dang=1):
    r"""Cây cao nhìn từ một điểm trên cao (mức VDC): biết độ cao điểm quan sát, khoảng cách tới gốc cây
    theo phương ngang và góc nhìn $\widehat{BAC}$, tính chiều cao cây (có hình).

    CLAUDE THEM 01/10/2026 - theo cau 64 tai lieu C3-B2 (AH = 4 m, HB = 20 m, 45 do). Co Lan duyet lai
    (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        AH, HB, al, phi, B, C, AB, BC = _bo_cay_cao()
        dap = _m(BC, 1)
        sai = [HB * math.tan(math.radians(al)), HB * math.tan(math.radians(al)) + AH, AB * _sin_d(al) / _sin_d(180 - al - 90),
               BC + AH]
        nh = _ba_nhieu(dap, [_m(x, 1) for x in sai], buoc=lambda t: _m(BC + 0.9 * t, 1))
        de = _de_cay_cao(AH, HB, al) + r" The height $BC$ of the tree (rounded to the nearest tenth) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh],
                                  _giai_cay_cao_a(AH, HB, al, phi, B, C, AB) + "\\\\\n" + _giai_cay_cao_b(al, C, AB, BC),
                                  _hinh_cay_cao(AH, HB, BC), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_T_01(socau, dang=2):
    r"""Trả lời ngắn - cây cao nhìn từ một điểm trên cao (mức VDC): chiều cao cây.

    CLAUDE THEM 01/10/2026 - theo cau 64 tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        AH, HB, al, phi, B, C, AB, BC = _bo_cay_cao()
        dap = _so(BC, 1)
        de = _de_cay_cao(AH, HB, al) + r" Find the height $BC$ of the tree (in meters, rounded to the nearest tenth)."
        cau += MC_SA_answer_const(de, dap, [_so(BC + k, 1) for k in (0.1, -0.1, 0.2)],
                                  _giai_cay_cao_a(AH, HB, al, phi, B, C, AB) + "\\\\\n" + _giai_cay_cao_b(al, C, AB, BC),
                                  _hinh_cay_cao(AH, HB, BC), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_M_01(socau, dong=1):
    r"""Tự luận - cây cao nhìn từ một điểm trên cao.
    a) (VD) Tính $AB$ và các góc $\widehat{ABC}$, $\widehat{ACB}$. b) (VDC) Tính chiều cao cây.

    CLAUDE THEM 01/10/2026 - theo cau 64 tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        AH, HB, al, phi, B, C, AB, BC = _bo_cay_cao()
        ds = [(r"Find the length $AB$ and the measures of the angles $\widehat{ABC}$, $\widehat{ACB}$ (round to the nearest hundredth of a degree).",
               r"\widehat{ACB} \approx %s^{\circ}" % _xx(C, 2), _giai_cay_cao_a(AH, HB, al, phi, B, C, AB)),
              (r"Find the height $BC$ of the tree (round to the nearest tenth, in meters).",
               r"BC \approx %s\,\text{m}" % _x1(BC, 1), _giai_cay_cao_b(al, C, AB, BC))]
        cau += TL_answer_text(_de_cay_cao(AH, HB, al), ds, _hinh_cay_cao(AH, HB, BC), 0, dong)
    return cau


# ---------- E. Tháp Chàm Pô Klông Garai (biến thể của VD036_MC_D, SA_D) ----------

def _bo_thap_cham():
    """Tháp chính Pô Klông Garai cao khoảng 20,5 m (vietnamplus.vn). Hai giác kế cao h đặt ở A, B
    thẳng hàng với chân tháp C; góc ngắm tới đỉnh D: al tại A1 (gần), be tại B1 (xa).
    CD = h + AB sin(al) sin(be)/sin(al - be). Chọn góc trước, tính AB nguyên rồi giữ khi CD 19,7-21,3 m."""
    while True:
        h = random.choice([1.2, 1.3, 1.5])
        al = random.choice([45, 48, 50, 52, 55])
        be = random.choice([30, 32, 35, 38])
        if al - be < 10:
            continue
        AB = round((20.5 - h) * _sin_d(al - be) / (_sin_d(al) * _sin_d(be)) + random.choice([-1, 0, 1]))
        if AB < 6:
            continue
        BD = AB * _sin_d(al) / _sin_d(al - be)    # đoạn B1D (B1 là mắt giác kế xa)
        C1D = BD * _sin_d(be)
        CD = C1D + h
        if 19.7 <= CD <= 21.3 and _xa_bien(CD, 1):
            return h, al, be, AB, BD, C1D, CD


def _de_thap_cham(h, al, be, AB):
    return (r"To measure the height of the main tower of the Po Klong Garai Cham tower complex (Ninh Thuan), two theodolites with "
            r"legs of height $%s\,\text{m}$ are set up at two points $A$, $B$ on the ground, $AB = %d\,\text{m}$, collinear with the foot $C$ "
            r"of the tower ($A$ is closer to the tower). Let $D$ be the top of the tower, $A_1$, $B_1$ the eye positions of the two theodolites, and "
            r"$C_1$ the intersection of line $A_1B_1$ with $CD$. The measured angles are $\widehat{DA_1C_1} = %s$ and "
            r"$\widehat{DB_1C_1} = %s$." % (_xx(h, 1), AB, _goc(al), _goc(be)))


def _giai_thap_cham(h, al, be, AB, BD, C1D, CD):
    return (r"$\widehat{A_1DB_1} = \widehat{DA_1C_1} - \widehat{DB_1C_1} = %s$ (exterior angle of triangle $A_1DB_1$)." "\\\\\n"
            r"Law of sines in triangle $A_1DB_1$: $B_1D = \dfrac{A_1B_1\cdot\sin\widehat{B_1A_1D}}{\sin\widehat{A_1DB_1}}"
            r" = \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$." "\\\\\n"
            r"Triangle $B_1C_1D$ is right-angled at $C_1$: $C_1D = B_1D\cdot\sin %s \approx %s\,\text{(m)}$." "\\\\\n"
            r"Hence $CD = C_1D + CC_1 \approx %s + %s \approx %s\,\text{(m)}$."
            % (_goc(al - be), AB, _goc(180 - al), _goc(al - be), _x1(BD, 2), _goc(be), _x1(C1D, 2),
               _x1(C1D, 2), _xx(h, 1), _x1(CD, 1)))


def _hinh_thap_cham(h, al, be, AB, CD):
    k = 3.0 / max(CD, AB + CD / math.tan(math.radians(al)))
    xa = (CD - h) / math.tan(math.radians(al)) * k
    xb = xa + AB * k
    hk, yd = h * k, CD * k
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
        "\\draw (-0.5,0) -- (%.2f,0);\n" % (xb + 0.5)
        + "\\fill[brown!35] (-0.35,0) -- (-0.25,%.2f) -- (0,%.2f) -- (0.25,%.2f) -- (0.35,0) -- cycle;\n" % (0.75 * yd, yd, 0.75 * yd)
        + "\\draw[dashed] (0,0) -- (0,%.2f);\n" % yd
        + "\\draw (%.2f,0) -- (%.2f,%.2f) (%.2f,0) -- (%.2f,%.2f);\n" % (xa, xa, hk, xb, xb, hk)
        + "\\draw[dashed] (0,%.2f) -- (%.2f,%.2f);\n" % (hk, xb, hk)
        + "\\draw (%.2f,%.2f) -- (0,%.2f) -- (%.2f,%.2f);\n" % (xa, hk, yd, xb, hk)
        + "\\fill (0,%.2f) circle (0.035) node[above] {$D$};\n" % yd
        + "\\fill (0,0) circle (0.035) node[below] {$C$};\n"
        "\\fill (0,%.2f) circle (0.035) node[left] {$C_1$};\n" % hk
        + "\\fill (%.2f,%.2f) circle (0.035) node[above right] {$A_1$};\n" % (xa, hk)
        + "\\fill (%.2f,%.2f) circle (0.035) node[above right] {$B_1$};\n" % (xb, hk)
        + "\\node[below] at (%.2f,0) {$A$};\n\\node[below] at (%.2f,0) {$B$};\n" % (xa, xb)
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_MC_D_04(socau, dang=1):
    r"""Biến thể 04 của VD036_MC_D: hai góc nâng, CÓ CHIỀU CAO GIÁC KẾ - đo chiều cao tháp chính
    Pô Klông Garai (thật khoảng 20,5 m). Đáp số phải cộng chiều cao giác kế (có hình).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 (AB = 12 m, giac ke 1,3 m, 49 va 35 do;
    dap so tai lieu 22,77 m - doi so lieu cho sat chieu cao that 20,5 m). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AB, BD, C1D, CD = _bo_thap_cham()
        dap = _m(CD, 1)
        nh = _ba_nhieu(dap, [_m(C1D, 1), _m(BD, 1), _m(CD + h, 1), _m(C1D * _sin_d(al) / _sin_d(be) + h, 1)],
                       buoc=lambda t: _m(CD + 0.8 * t, 1))
        de = _de_thap_cham(h, al, be, AB) + r" The height $CD$ of the tower (rounded to the nearest tenth) is"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_thap_cham(h, al, be, AB, BD, C1D, CD),
                                  _hinh_thap_cham(h, al, be, AB, CD), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_D_04(socau, dang=2):
    r"""Biến thể 04 của VD036_SA_D: chiều cao tháp chính Pô Klông Garai đo bằng hai giác kế (có hình).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AB, BD, C1D, CD = _bo_thap_cham()
        dap = _so(CD, 1)
        de = _de_thap_cham(h, al, be, AB) + r" Find the height $CD$ of the tower (in meters, rounded to the nearest tenth)."
        cau += MC_SA_answer_const(de, dap, [_so(CD + k, 1) for k in (0.1, -0.1, 0.2)],
                                  _giai_thap_cham(h, al, be, AB, BD, C1D, CD), _hinh_thap_cham(h, al, be, AB, CD), 0, dang)
    return cau


# =====================================================================
# ĐÚNG/SAI CHƯƠNG 3 - MỞ RỘNG (CLAUDE THEM 01/10/2026, co Lan chon dang).
# Moi cau: a) NB, b) TH, c) VD, d) VDC. Cau co boi canh thuc tien ghi
# "boi_canh" o Mapping trung voi MC/SA/TL cung boi canh -> mot de khong ra
# hai cau cung boi canh (o moi chuong, docs/04).
# =====================================================================

# ---------- Tiện ích Đúng/Sai: nhiều phát biểu đúng + nhiều phát biểu sai cho một ý (cô Lan 01/10/2026) ----------
_HANG_LT = {0: "whole number", 1: "tenth", 2: "hundredth", 3: "thousandth"}


def _tf_nguong(v):
    """Hai ngưỡng 'tròn' lo < v < hi, cách v đủ xa (để phát biểu so sánh không sát biên)."""
    g = 10 ** math.floor(math.log10(abs(v)))
    if abs(v) / g < 2:
        g /= 5
    elif abs(v) / g < 5:
        g /= 2
    lo = math.floor(v / g) * g
    if v - lo < 0.15 * g:
        lo -= g
    hi = math.ceil(v / g) * g
    if hi - v < 0.15 * g:
        hi += g
    return round(lo, 6), round(hi, 6)


def _tf_mau_bdt(mau):
    r"""Suy mẫu phát biểu SO SÁNH từ mẫu phát biểu giá trị (01/10/2026, cô Lan: mỗi ý phải nhiều đúng, nhiều sai).
    '... = %s$' hoặc '... \approx %s$' -> '... > a$' / '... < b$'; '... xấp xỉ / bằng / là $%s$' -> 'lớn hơn / nhỏ hơn';
    '... khoảng $%s$' -> 'hơn / chưa đến'. Trả về (mẫu có hai %s, (từ lớn, từ nhỏ)) hoặc None."""
    for k in (r" \approx %s$", r" = %s$"):
        if mau.count(k) == 1:
            return mau.replace(k, r" %s %s$"), (">", "<")
    for k, rep, tu in (("approximately $%s$", "%s $%s$", ("greater than", "less than")),
                       ("equals $%s$", "is %s $%s$", ("greater than", "less than")),
                       ("is $%s$", "is %s $%s$", ("greater than", "less than")),
                       ("about $%s$", "%s $%s$", ("more than", "less than"))):
        if mau.count(k) == 1:
            return mau.replace(k, rep), tu
    return None


def _tf_so(mau, v, n, ly, sai, dv="", bdt=None, tu=("greater than", "less than"), mien=(0, None)):
    r"""Phát biểu đúng / sai cho MỘT giá trị gần đúng v (độ dài, góc, diện tích...).
    mau : chuỗi có một %s cho số (đã kèm đơn vị dv), ví dụ r"$AC \approx %s$".
    n   : số chữ số làm tròn trong phát biểu chính.
    ly  : lời giải (chưa có câu chốt).
    sai : [(giá trị sai, ghi chú lỗi)] - các lỗi hay gặp của học sinh.
    bdt : chuỗi có hai %s (từ so sánh, số kèm đơn vị), ví dụ r"$AC$ %s $%s$" -> thêm phát biểu so sánh.
    mien: khoảng giá trị hợp lí (lo, hi) của phát biểu sai (mặc định số dương; côsin dùng (-1, 1)).
    Trả về (dung_ds, sai_ds) để đưa vào _phat_bieu."""
    def so(x, k):
        return (str(_lt(x)) if k == 0 else _x1(x, k)) + dv

    def hang(k):
        return " (rounded to the nearest %s)" % _HANG_LT[k]

    chot = r" Hence the required value is $\approx %s$." % so(v, n + 1)
    giai = ly + chot
    dung = [(mau % so(v, n) + hang(n), giai)]
    k2 = n - 1 if n >= 1 else 1
    if _xa_bien(v, k2) and so(v, k2) != so(v, n):
        dung.append((mau % so(v, k2) + hang(k2), giai))
    sai_ds = []
    for w, ghi in sai:
        if w is None or w <= mien[0] or (mien[1] is not None and w >= mien[1]) or so(w, n) == so(v, n):
            continue
        sai_ds.append((mau % so(w, n) + hang(n), (ghi.rstrip(".") + ". " if ghi else "") + giai))
    # lỗi làm tròn: cắt bỏ hoặc làm tròn lên sai
    cat = math.floor(v * 10 ** n) / 10 ** n
    len_ = (math.floor(v * 10 ** n) + 1) / 10 ** n
    for w in (cat, len_):
        if so(w, n) != so(v, n):
            sai_ds.append((mau % so(w, n) + hang(n), "Rounding was not done correctly. " + giai))
            break
    if not bdt and _tf_mau_bdt(mau):
        bdt, tu = _tf_mau_bdt(mau)
    if bdt and abs(v) > 1e-9:
        lo, hi = _tf_nguong(v)
        f = lambda x: _so(x, 3) + dv
        dung += [(bdt % (tu[0], f(lo)), giai), (bdt % (tu[1], f(hi)), giai)]
        sai_ds += [(bdt % (tu[0], f(hi)), giai), (bdt % (tu[1], f(lo)), giai)]
    return dung, sai_ds


def _tf_ct(mau, v, ly, sai, them=()):
    r"""Phát biểu đúng / sai cho MỘT giá trị chính xác v (sympy).
    mau : chuỗi có một %s cho giá trị LaTeX, ví dụ r"$\cos\alpha = %s$".
    sai : [(giá trị sai, ghi chú lỗi)]; them: các phát biểu ĐÚNG tương đương [(nội dung)] dùng chung lời giải.
    Trả về (dung_ds, sai_ds)."""
    dung = [(mau % _L(v), ly)] + [(t, ly) for t in them]
    sai_ds = []
    sai_ok = []
    for w, ghi in sai:
        if w is None:
            continue
        if simplify(w - v) == 0:
            continue
        sai_ok.append((simplify(w), ghi))
        sai_ds.append((mau % _L(simplify(w)), (ghi.rstrip(".") + ". " if ghi else "") + ly))
    # 01/10/2026 (cô Lan): thêm phát biểu gần đúng và phát biểu so sánh để mỗi ý có nhiều đúng, nhiều sai
    try:
        vf = float(v)
    except TypeError:
        return dung, sai_ds
    mau_xx = None
    if mau.count(r" = %s$") == 1:
        mau_xx = mau.replace(r" = %s$", r" \approx %s$")
    elif mau.count("equals $%s$") == 1:
        mau_xx = mau.replace("equals $%s$", "is approximately $%s$")
    hang = " (rounded to the nearest hundredth)"
    if mau_xx and not v.is_Integer and _so_thap_phan_gon(v) is None and _xa_bien(vf, 2) and _x1(vf, 2).rstrip("0").rstrip(".") != _L(v):
        dung.append((mau_xx % _x1(vf, 2) + hang, ly + r" We have $%s \approx %s$." % (_L(v), _x1(vf, 3))))
        for w, ghi in sai_ok:
            if w.is_real and _x1(float(w), 2) != _x1(vf, 2):
                sai_ds.append((mau_xx % _x1(float(w), 2) + hang, (ghi.rstrip(".") + ". " if ghi else "") + ly))
    bd = _tf_mau_bdt(mau)
    if bd and abs(vf) > 1e-9:
        d_, s_ = _tf_bdt(bd[0], vf, ly + r" We have $%s \approx %s$." % (_L(v), _x1(vf, 3)), tu=bd[1])
        dung += d_
        sai_ds += s_
    return dung, sai_ds


def _tf_gop(*cap):
    """Gộp nhiều cặp (dung_ds, sai_ds) rồi tạo một ý bằng _phat_bieu."""
    d, s = [], []
    for a, b in cap:
        d += a
        s += b
    return _phat_bieu(d, s)


def _tf_them(y, dung, sai):
    """Bổ sung vào một ý ĐÃ CÓ (danh sách của TF_baitoan_du) nhiều phát biểu đúng / sai mới,
    bỏ những phát biểu trùng nội dung với phát biểu đã có (cô Lan 01/10/2026)."""
    co = {t.replace("{\\True ", "{") for t, _ in y}
    for t, l in _phat_bieu(dung, sai):
        if t.replace("{\\True ", "{") not in co:
            co.add(t.replace("{\\True ", "{"))
            y.append((t, l))
    return y


def _tf_bdt(mau, v, ly, tu=("greater than", "less than"), dv=""):
    """Hai phát biểu so sánh đúng và hai phát biểu so sánh sai cho giá trị v (ngưỡng tròn).
    mau có hai %s: (từ so sánh, số)."""
    lo, hi = _tf_nguong(v)
    f = lambda x: _so(x, 3) + dv
    return ([(mau % (tu[0], f(lo)), ly), (mau % (tu[1], f(hi)), ly)],
            [(mau % (tu[0], f(hi)), ly), (mau % (tu[1], f(lo)), ly)])


def _n1_phan_thuc(s, c):
    """Biểu thức (p sin + q cos)/(u sin + v cos) với hệ số nhỏ: (LaTeX, giá trị, [(giá trị sai, lỗi)]).
    Trả về None nếu mẫu bằng 0."""
    while True:
        p, q, u, v = [random.choice([1, 2, 3, -1, -2]) for _ in range(4)]
        if p * v != q * u:
            break
    mau = u * s + v * c
    tu_ = p * s + q * c
    if simplify(mau) == 0 or simplify(tu_) == 0:
        return None

    def hang(a, b, x, y):
        t = ("" if a == 1 else ("-" if a == -1 else str(a))) + x
        t += (" + " if b > 0 else " - ") + ("" if abs(b) == 1 else str(abs(b))) + y
        return t

    bt = r"\dfrac{%s}{%s}" % (hang(p, q, r"\sin\alpha", r"\cos\alpha"), hang(u, v, r"\sin\alpha", r"\cos\alpha"))
    P = simplify(tu_ / mau)
    sai = [(simplify(mau / tu_), "Numerator and denominator swapped")]
    if simplify(u * s - v * c) != 0:
        sai.append((simplify((p * s - q * c) / (u * s - v * c)), "Wrong sign of $\\cos\\alpha$"))
    if simplify(u * s + v * abs(c)) != 0:
        sai.append((simplify((p * s + q * abs(c)) / (u * s + v * abs(c))), "Mistakenly taking $\\cos\\alpha$ as positive"))
    return bt, P, sai


def _n2_lech_truc(h):
    """Số đo góc lệch khỏi trục bắc - nam của hướng h (số trong kí hiệu N x E, S x W...)."""
    h %= 180
    return h if h <= 90 else 180 - h


def _n3_chi_phi(S, gia, ly, ten="tile the entire plot of land"):
    """Phát biểu về chi phí (triệu đồng) và diện tích cho TF_H."""
    tien = S * gia / 1000
    T = math.floor(tien)
    R = math.floor(tien + 0.5)       # làm tròn đến hàng đơn vị (triệu đồng)
    mau = r"The cost to %s is %s $%d$ million VND"
    dung = [(mau % (ten, "greater than", T), ly), (mau % (ten, "less than", T + 1), ly)]
    sai = [(mau % (ten, "greater than", T + 1), ly), (mau % (ten, "less than", T), ly)]
    if T >= 2:
        sai.append((mau % (ten, "less than", T - 1), ly))
    # CLAUDE THEM 09/10/2026 (co Lan duyet): ý d) phải LUÔN hỏi về tiền (câu dẫn có giá),
    # mỗi ý ít nhất 3 phát biểu đúng, 3 sai -> thêm phát biểu "xấp xỉ" và "trong khoảng".
    mau2 = r"The cost to %s is approximately $%d$ million VND (rounded to the nearest whole number)"
    mau3 = r"The cost to %s is between $%d$ and $%d$ million VND"
    dung += [(mau2 % (ten, R), ly), (mau3 % (ten, T, T + 1), ly)]
    sai += [(mau2 % (ten, R + 1), ly), (mau3 % (ten, T + 1, T + 2), ly)]
    if R >= 2:
        sai.append((mau2 % (ten, R - 1), ly))
    if T >= 1:
        sai.append((mau3 % (ten, T - 1, T), ly))
    return dung, sai


def _y_ds(dung, sai, ly):
    """Một ý đúng/sai: phát biểu đúng (dung) hoặc sai (sai), cùng lời giải."""
    if sai == dung:
        sai = None
    ds = [(r"{\True %s}" % dung, "True. " + ly)]
    if sai is not None:
        ds.append((r"{%s}" % sai, "False. " + ly))
    return ds


def _sai_so(x, n, buoc):
    """Một số sai khác hẳn x sau khi làm tròn n chữ số (n = 0: hàng đơn vị)."""
    while True:
        y = x + random.choice([-1, 1]) * buoc * random.choice([1, 2, 3])
        if (_lt(y) if n == 0 else _x1(y, n)) != (_lt(x) if n == 0 else _x1(x, n)) and y > 0:
            return y


def _sm(x, n=1, dv=r"\,\text{m}"):
    return (str(_lt(x)) if n == 0 else _x1(x, n)) + dv


# Các biểu thức góc bù, góc phụ dùng cho ý d) của TF_J: (LaTeX, giá trị theo (s, c, t, k), giá trị SAI hay gặp)
_BU_PHU_TF_J = [
    (r"\sin\left(180^{\circ} - \alpha\right)", lambda s, c, t, k: s, lambda s, c, t, k: -s),
    (r"\cos\left(180^{\circ} - \alpha\right)", lambda s, c, t, k: -c, lambda s, c, t, k: c),
    (r"\tan\left(180^{\circ} - \alpha\right)", lambda s, c, t, k: -t, lambda s, c, t, k: t),
    (r"\cot\left(180^{\circ} - \alpha\right)", lambda s, c, t, k: -k, lambda s, c, t, k: k),
    (r"\sin\left(90^{\circ} - \alpha\right)", lambda s, c, t, k: c, lambda s, c, t, k: s),
    (r"\cos\left(90^{\circ} - \alpha\right)", lambda s, c, t, k: s, lambda s, c, t, k: c),
    (r"\tan\left(90^{\circ} - \alpha\right)", lambda s, c, t, k: k, lambda s, c, t, k: t),
    (r"\cot\left(90^{\circ} - \alpha\right)", lambda s, c, t, k: t, lambda s, c, t, k: k),
]
_TEN_BU_PHU = [r"\sin\alpha", r"-\cos\alpha", r"-\tan\alpha", r"-\cot\alpha",
               r"\cos\alpha", r"\sin\alpha", r"\cot\alpha", r"\tan\alpha"]


def L10_C3_TF_J_01(socau, socot=1):
    r"""Đúng/Sai - biết MỘT giá trị lượng giác ($\sin$, $\cos$, $\tan$ hoặc $\cot$, số của bộ ba Pythagore) và
    góc nhọn / tù:
    a) (NB) dấu của một giá trị lượng giác;
    b) (TH) đổi một bước: từ $\cos$ tìm $\sin$, từ $\sin$ tìm $\cos$, từ $\tan$ tìm $\cot$, từ $\cot$ tìm $\tan$;
    c) (VD) giá trị còn lại cần hai bước ($\tan = \dfrac{\sin}{\cos}$, hoặc $1 + \tan^{2}\alpha = \dfrac{1}{\cos^{2}\alpha}$,
       $1 + \cot^{2}\alpha = \dfrac{1}{\sin^{2}\alpha}$);
    d) (VDC) tính biểu thức chứa các góc bù, góc phụ của $\alpha$.

    CLAUDE THEM 01/10/2026 - lam lai theo y co Lan ("cau b tu cos tim sin, tu tan tim cot...; cau b cu
    chuyen thanh cau c; cau d tinh bieu thuc co goc bu phu"). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    so = 0
    while so < socau:
        doi, ke, huyen = random.choice(BO_BA_PYTAGO)
        if random.random() < 0.5:
            doi, ke = ke, doi
        tu = random.random() < 0.5
        dau = -1 if tu else 1
        s, c = Rational(doi, huyen), Rational(dau * ke, huyen)
        t, k = s / c, c / s
        cho = random.choice(["sin", "cos", "tan", "cot"])
        gia = {"sin": s, "cos": c, "tan": t, "cot": k}[cho]
        loai = "obtuse" if tu else "acute"
        khoang = r"90^{\circ} < \alpha < 180^{\circ}" if tu else r"0^{\circ} < \alpha < 90^{\circ}"
        lon, be_ = ("<", ">") if tu else (">", "<")

        # Chuẩn bị trước cho ý d (VDC): 2 biểu thức góc bù / phụ, mỗi biểu thức kèm các giá trị SAI (nhầm một số hạng)
        bts = []
        for _ in range(2):
            terms = random.sample(range(len(_BU_PHU_TF_J)), 3)
            hs = [random.choice([1, 2, 3, -1, -2]) for _ in terms]
            P = sum(h * _BU_PHU_TF_J[i][1](s, c, t, k) for h, i in zip(hs, terms))
            Ps = []
            for jj in range(3):
                Ps.append(sum(h * (_BU_PHU_TF_J[i][2] if j == jj else _BU_PHU_TF_J[i][1])(s, c, t, k)
                              for j, (h, i) in enumerate(zip(hs, terms))))
            bts.append((terms, hs, P, Ps))
        if any(all(simplify(Q - P) == 0 for Q in Ps) for _, _, P, Ps in bts):
            continue
        so += 1
        debai = (r"Given an angle $\alpha$ with $%s$ (angle $\alpha$ is %s) and $\%s\alpha = %s$. Determine whether each of the following statements is true or false."
                 % (khoang, loai, cho, _L(gia)))

        # a) NB - dấu của các giá trị lượng giác (trừ giá trị đã cho)
        ly_a = r"Since angle $\alpha$ is %s, $\cos\alpha %s 0$, $\tan\alpha %s 0$, $\cot\alpha %s 0$ (and $\sin\alpha > 0$)." % (
            loai, lon, lon, lon)
        dung = [(r"$\%s\alpha %s 0$" % (h, lon), ly_a) for h in ("cos", "tan", "cot") if h != cho]
        sai = [(r"$\%s\alpha %s 0$" % (h, be_), ly_a) for h in ("cos", "tan", "cot") if h != cho]
        if cho != "sin":
            dung.append((r"$\sin\alpha > 0$", ly_a))
            sai.append((r"$\sin\alpha < 0$", ly_a))
        dung.append((r"$\sin\alpha\cdot\cos\alpha %s 0$" % lon, ly_a))
        sai.append((r"$\sin\alpha\cdot\cos\alpha %s 0$" % be_, ly_a))
        y1 = _phat_bieu(dung, sai)

        # b) TH - đổi một bước
        if cho == "cos":
            ly_b = r"$\sin^{2}\alpha = 1 - \cos^{2}\alpha = 1 - %s = %s$, and since $\sin\alpha > 0$, $\sin\alpha = %s$." % (_L(c ** 2), _L(s ** 2), _L(s))
            y2 = _tf_gop(_tf_ct(r"$\sin\alpha = %s$", s, ly_b,
                                [(-s, "Wrong sign: $\\sin\\alpha > 0$"), (1 - c, "Forgot to square"), (s ** 2, "Forgot to take the square root"),
                                 (1 - abs(c), "Mistakenly using $\\sin\\alpha = 1 - \\left|\\cos\\alpha\\right|$")]),
                         _tf_ct(r"$\sin^{2}\alpha = %s$", s ** 2, ly_b, [(1 + c ** 2, "Sign mistake: $\\sin^{2}\\alpha = 1 - \\cos^{2}\\alpha$"),
                                                                           (c ** 2, "Mistakenly using $\\sin^{2}\\alpha = \\cos^{2}\\alpha$")]))
        elif cho == "sin":
            ly_b = (r"$\cos^{2}\alpha = 1 - \sin^{2}\alpha = 1 - %s = %s$, and since angle $\alpha$ is %s, $\cos\alpha = %s$."
                    % (_L(s ** 2), _L(c ** 2), loai, _L(c)))
            y2 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", c, ly_b,
                                [(-c, "Wrong sign (the type of angle was not considered)"), (1 - s, "Forgot to square"), (dau * c ** 2, "Forgot to take the square root"),
                                 (dau * (1 - s), "Mistakenly using $\\cos\\alpha = 1 - \\sin\\alpha$")]),
                         _tf_ct(r"$\cos^{2}\alpha = %s$", c ** 2, ly_b, [(1 + s ** 2, "Sign mistake: $\\cos^{2}\\alpha = 1 - \\sin^{2}\\alpha$"),
                                                                           (s ** 2, "Mistakenly using $\\cos^{2}\\alpha = \\sin^{2}\\alpha$")]))
        elif cho == "tan":
            ly_b = r"$\cot\alpha = \dfrac{1}{\tan\alpha} = %s$." % _L(k)
            y2 = _tf_gop(_tf_ct(r"$\cot\alpha = %s$", k, ly_b,
                                [(-k, "Wrong sign: $\\tan\\alpha$ and $\\cot\\alpha$ have the same sign"), (t, "Mistakenly using $\\cot\\alpha = \\tan\\alpha$"),
                                 (-t, "Mistakenly using $\\cot\\alpha = -\\tan\\alpha$"), (1 - t, "Mistakenly using $\\cot\\alpha = 1 - \\tan\\alpha$")]),
                         _tf_ct(r"$\cot^{2}\alpha = %s$", k ** 2, ly_b, [(t ** 2, "Mistakenly using $\\cot^{2}\\alpha = \\tan^{2}\\alpha$")]))
        else:
            ly_b = r"$\tan\alpha = \dfrac{1}{\cot\alpha} = %s$." % _L(t)
            y2 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", t, ly_b,
                                [(-t, "Wrong sign: $\\tan\\alpha$ and $\\cot\\alpha$ have the same sign"), (k, "Mistakenly using $\\tan\\alpha = \\cot\\alpha$"),
                                 (-k, "Mistakenly using $\\tan\\alpha = -\\cot\\alpha$"), (1 - k, "Mistakenly using $\\tan\\alpha = 1 - \\cot\\alpha$")]),
                         _tf_ct(r"$\tan^{2}\alpha = %s$", t ** 2, ly_b, [(k ** 2, "Mistakenly using $\\tan^{2}\\alpha = \\cot^{2}\\alpha$")]))

        # c) VD - giá trị còn lại, hai bước
        if cho in ("sin", "cos"):
            ly_c = ly_b + r" Hence $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$, $\cot\alpha = \dfrac{\cos\alpha}{\sin\alpha} = %s$." % (_L(t), _L(k))
            y3 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", t, ly_c, [(1 / t, "Numerator and denominator swapped"), (-t, "Sign error"), (s * c, "Mistakenly using $\\tan\\alpha = \\sin\\alpha\\cdot\\cos\\alpha$")]),
                         _tf_ct(r"$\cot\alpha = %s$", k, ly_c, [(t, "Mistakenly using $\\cot\\alpha = \\tan\\alpha$"), (-k, "Sign error")]))
        elif cho == "tan":
            ly_c = (r"$\dfrac{1}{\cos^{2}\alpha} = 1 + \tan^{2}\alpha = %s$, so $\cos^{2}\alpha = %s$; since angle $\alpha$ is %s, "
                    r"$\cos\alpha = %s$, $\sin\alpha = \tan\alpha\cdot\cos\alpha = %s$." % (_L(1 + t ** 2), _L(c ** 2), loai, _L(c), _L(s)))
            y3 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", c, ly_c, [(-c, "Wrong sign (the type of angle was not considered)"), (dau * 1 / (1 + t ** 2), "Forgot to take the square root"),
                                                                 (dau * sqrt(1 + t ** 2), "Forgot to take the reciprocal")]),
                         _tf_ct(r"$\sin\alpha = %s$", s, ly_c, [(-s, "Wrong sign: $\\sin\\alpha > 0$"), (abs(c), "Confused $\\sin$ with $\\cos$")]),
                         _tf_ct(r"$\cos^{2}\alpha = %s$", c ** 2, ly_c, [(1 + t ** 2, "Forgot to take the reciprocal")]))
        else:
            ly_c = (r"$\dfrac{1}{\sin^{2}\alpha} = 1 + \cot^{2}\alpha = %s$, so $\sin^{2}\alpha = %s$; since $\sin\alpha > 0$, "
                    r"$\sin\alpha = %s$, $\cos\alpha = \cot\alpha\cdot\sin\alpha = %s$." % (_L(1 + k ** 2), _L(s ** 2), _L(s), _L(c)))
            y3 = _tf_gop(_tf_ct(r"$\sin\alpha = %s$", s, ly_c, [(abs(c), "Confused $\\sin$ with $\\cos$"), (1 / (1 + k ** 2), "Forgot to take the square root"),
                                                                 (-s, "Wrong sign: $\\sin\\alpha > 0$")]),
                         _tf_ct(r"$\cos\alpha = %s$", c, ly_c, [(-c, "Wrong sign (the type of angle was not considered)"), (abs(s) * dau, "Confusing $\\cos$ with $\\sin$")]),
                         _tf_ct(r"$\sin^{2}\alpha = %s$", s ** 2, ly_c, [(1 + k ** 2, "Forgot to take the reciprocal")]))

        # d) VDC - biểu thức chứa góc bù, góc phụ (2 biểu thức khác nhau, mỗi biểu thức nhiều kết quả sai)
        dung, sai = [], []
        for terms, hs, P, Ps in bts:
            bt = ""
            for j, (h, i) in enumerate(zip(hs, terms)):
                he = ("" if h == 1 else ("-" if h == -1 else str(h))) if j == 0 else \
                     (" + " if h == 1 else (" - " if h == -1 else (" + %d" % h if h > 0 else " - %d" % -h)))
                bt += he + _BU_PHU_TF_J[i][0]
            doi_ra = ", ".join(r"$%s = %s$" % (_BU_PHU_TF_J[i][0], _TEN_BU_PHU[i]) for i in terms)
            ly_d = (r"By the relations of supplementary and complementary angles: %s. With $\sin\alpha = %s$, $\cos\alpha = %s$, $\tan\alpha = %s$, "
                    r"$\cot\alpha = %s$, the expression equals $%s$." % (doi_ra, _L(s), _L(c), _L(t), _L(k), _L(P)))
            a_, b_ = _tf_ct("$" + bt + " = %s$", P, ly_d, [(Q, "Mixed up the supplementary / complementary angle relations in one term") for Q in Ps])
            dung += a_
            sai += b_
        y4 = _phat_bieu(dung, sai)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C3_TF_K_01(socau, socot=1):
    r"""Đúng/Sai - hỏi ngược định lí sin: biết $BC$ và $R$ (góc $A$ nhọn hoặc tù), biết thêm góc $B$:
    hệ thức định lí sin, số đo góc $A$, cạnh $CA$, diện tích tam giác.

    CLAUDE THEM 01/10/2026 - theo cau 36, 39 tai lieu C3-B2. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    n = 0
    while n < socau:
        sA, A, nhon, R, a = _bo_nguoc_sin(True)
        B = random.choice([g for g in (15, 20, 30, 45, 60) if g + A < 170])
        C = 180 - A - B
        b = 2 * R * _sin_d(B)
        S = 2 * R * R * _sin_d(A) * _sin_d(B) * _sin_d(C)
        if not (_xa_bien(b, 1) and _xa_bien(S, 1)):
            continue
        n += 1
        loai = "acute" if nhon else "obtuse"
        debai = (r"Given triangle $ABC$ with angle $A$ %s, $BC = %s$, $\widehat{B} = %s$ and circumradius "
                 r"$R = %d$. Determine whether each of the following statements is true or false." % (loai, _L(a), _goc(B), R))
        # a) NB - nhận ra định lí sin
        ly_a = r"Law of sines: $\dfrac{BC}{\sin A} = \dfrac{CA}{\sin B} = \dfrac{AB}{\sin C} = 2R$."
        y1 = _phat_bieu(
            [(r"$\dfrac{BC}{\sin A} = 2R$", ly_a), (r"$\dfrac{CA}{\sin B} = 2R$", ly_a), (r"$\dfrac{AB}{\sin C} = 2R$", ly_a),
             (r"$BC = 2R\sin A$", ly_a), (r"$\sin A = \dfrac{BC}{2R}$", ly_a)],
            [(r"$\dfrac{BC}{\sin A} = R$", ly_a), (r"$\dfrac{BC}{\sin B} = 2R$", ly_a), (r"$BC = R\sin A$", ly_a),
             (r"$\dfrac{CA}{\sin A} = 2R$", ly_a), (r"$\sin A = \dfrac{2R}{BC}$", ly_a), (r"$\dfrac{AB}{\cos C} = 2R$", ly_a)])
        # b) TH - một bước: sin A = BC/(2R), rồi chọn góc theo loại góc
        ly_b = r"$\sin A = \dfrac{BC}{2R} = %s$; since angle $A$ is %s, $\widehat{A} = %s$." % (_L(sA), loai, _goc(A))
        dung = [(r"$\widehat{A} = %s$" % _goc(A), ly_b), (r"$\sin A = %s$" % _L(sA), ly_b)]
        sai = [(r"$\widehat{A} = %s$" % _goc(180 - A), "Did not take into account that angle $A$ is %s. " % loai + ly_b)]
        if A != 45 and 90 - A > 0:
            sai.append((r"$\widehat{A} = %s$" % _goc(90 - A), ly_b))
        for w, ghi in ((sA / 2, "Forgot to multiply by 2 in $2R$"), (2 * sA, "Mistakenly using $\\sin A = \\dfrac{BC}{R}$")):
            if 0 < w <= 1 and simplify(w - sA) != 0:
                sai.append((r"$\sin A = %s$" % _L(simplify(w)), ghi + ". " + ly_b))
        y2 = _phat_bieu(dung, sai)
        # c) VD - cạnh CA
        ly_c = r"$CA = 2R\sin B = %d\cdot\sin %s$." % (2 * R, _goc(B))
        y3 = _tf_gop(_tf_so(r"$CA \approx %s$", b, 1, ly_c,
                            [(R * _sin_d(B), "Forgot to multiply by 2 (used $R\\sin B$)"), (2 * R * _cos_d(B), "Confused $\\sin$ with $\\cos$"),
                             (2 * R * _sin_d(C), "Wrong angle: that gives side $AB$"), (2 * R / _sin_d(B), "Mistakenly using $CA = \\dfrac{2R}{\\sin B}$")],
                            bdt=r"$CA$ %s $%s$"))
        # d) VDC - diện tích
        C_sai = A - B if not nhon else None        # nếu lấy nhầm A = 180 - A
        ly_d = (r"$\widehat{C} = 180^{\circ} - %s - %s = %s$, $AB = 2R\sin C$, so "
                r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\sin C = 2R^{2}\sin A\sin B\sin C$." % (_goc(A), _goc(B), _goc(C)))
        sai = [(2 * S, "Forgot the factor $\\dfrac{1}{2}$"), (S / 2, "Multiplied by an extra $\\dfrac{1}{2}$"),
               (0.5 * float(a) * b * _sin_d(B), "Used angle $B$ instead of the included angle $C$"),
               (0.5 * float(a) * b * _cos_d(C), "Confused $\\sin C$ with $\\cos C$")]
        if C_sai and C_sai > 0:
            sai.append((2 * R * R * _sin_d(A) * _sin_d(B) * _sin_d(C_sai), "Mistakenly taking angle $A$ to be acute"))
        y4 = _tf_gop(_tf_so(r"The area of triangle $ABC$ is approximately $%s$", S, 1, ly_d, sai,
                            bdt=r"The area of triangle $ABC$ is %s $%s$"))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _lyk = ly_b + r" Hence $\widehat{C} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C))
        _tf_them(y2, [(r"$\widehat{C} = %s$" % _goc(C), _lyk)],
                 [(r"$\widehat{C} = %s$" % _goc(w), _lyk) for w in (A - B, 180 - B, 90 - B) if 0 < w < 180 and w != C])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def _cong_thuc_tam_giac():
    """Một công thức của chương 3 (Bài 6, SGK) cho tam giác ABC: (đúng, sai, lời giải).
    Đỉnh được hoán vị ngẫu nhiên để công thức đa dạng. KHÔNG dùng công thức trung
    tuyến (chỉ có trong SBT - cô Lan 01/10/2026)."""
    X, Y, Z = random.sample("ABC", 3)
    x, y, z = X.lower(), Y.lower(), Z.lower()
    bo = [
        (r"%s^{2} = %s^{2} + %s^{2} - 2%s%s\cos %s" % (x, y, z, y, z, X),
         random.choice([r"%s^{2} = %s^{2} + %s^{2} + 2%s%s\cos %s" % (x, y, z, y, z, X),
                        r"%s^{2} = %s^{2} + %s^{2} - %s%s\cos %s" % (x, y, z, y, z, X),
                        r"%s^{2} = %s^{2} + %s^{2} - 2%s%s\cos %s" % (x, y, z, y, z, Y)]),
         "Law of cosines"),
        (r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s%s}" % (X, y, z, x, y, z),
         random.choice([r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{%s%s}" % (X, y, z, x, y, z),
                        r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s%s}" % (X, x, y, z, y, z)]),
         "Corollary of the law of cosines"),
        (r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s} = 2R" % (x, X, y, Y),
         random.choice([r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s} = R" % (x, X, y, Y),
                        r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s} = 2R" % (x, Y, y, X)]),
         r"Law of sines ($R$ is the circumradius)"),
        (r"S = \dfrac{1}{2}%s%s\sin %s" % (y, z, X),
         random.choice([r"S = \dfrac{1}{2}%s%s\sin %s" % (y, z, Y), r"S = %s%s\sin %s" % (y, z, X)]),
         r"Area formula using two sides and the included angle"),
        (r"S = \dfrac{abc}{4R}", random.choice([r"S = \dfrac{abc}{2R}", r"S = \dfrac{4R}{abc}"]),
         r"Area formula using the circumradius $R$"),
        (r"S = pr", random.choice([r"S = 2pr", r"S = \dfrac{r}{p}"]),
         r"Area formula using the semiperimeter $p$ and the inradius $r$"),
        (r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}",
         random.choice([r"S = \sqrt{\left(p - a\right)\left(p - b\right)\left(p - c\right)}",
                        r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}"]),
         r"Heron's formula ($p$ is the semiperimeter)"),
        (r"S = \dfrac{1}{2}%s\cdot h_%s" % (x, x), random.choice([r"S = %s\cdot h_%s" % (x, x), r"S = \dfrac{1}{2}%s\cdot h_%s" % (y, x)]),
         r"Area formula using a side and the corresponding altitude"),
    ]
    dung, sai, ten = random.choice(bo)
    return "$" + dung + "$", "$" + sai + "$", ten + r": $" + dung + "$."


def L10_C3_TF_L_01(socau, socot=1):
    r"""Đúng/Sai - tam giác biết BA CẠNH (cạnh nguyên, diện tích nguyên):
    a) (NB) nhận ra một công thức của Bài 6 (chọn ngẫu nhiên trong định lí côsin, hệ quả, định lí sin, bốn
       công thức diện tích, Heron; đỉnh hoán vị ngẫu nhiên) - KHÔNG dùng công thức trung tuyến (chỉ có ở SBT);
    b) (TH) tính rất đơn giản: nửa chu vi $p$ hoặc côsin một góc (thay số một lần);
    c) (VD) diện tích (Heron);
    d) (VDC) đường cao, bán kính nội tiếp hoặc ngoại tiếp (qua diện tích).

    CLAUDE THEM 01/10/2026 - lam lai theo y co Lan. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        x, y, z, S, p = random.choice([t for t in HERON_NGUYEN if t[2] <= 20])
        a, b, c = random.sample([x, y, z], 3)
        debai = (r"Given triangle $ABC$ with $BC = a = %d$, $CA = b = %d$, $AB = c = %d$. Let $S$, $p$, $R$, $r$ be, respectively, the "
                 r"area, semiperimeter, circumradius, and inradius of the triangle. Determine whether each of the following "
                 r"statements is true or false." % (a, b, c))
        # a) NB - nhận ra công thức (nhiều công thức đúng, nhiều biến dạng sai)
        dung, sai = [], []
        _da_co = set()  # không để hai phát biểu trùng nhau trong cùng một ý
        for _k in range(60):
            d_, s_, ly = _cong_thuc_tam_giac()
            if d_ in _da_co or s_ in _da_co:
                continue
            _da_co.update((d_, s_))
            dung.append((d_, ly))
            sai.append((s_, ly))
            if len(dung) == 6:
                break
        y1 = _phat_bieu(dung, sai)
        # b) TH - tính cực kì đơn giản: nửa chu vi hoặc côsin một góc
        ly_p = r"$p = \dfrac{a + b + c}{2} = \dfrac{%d + %d + %d}{2} = %s$." % (a, b, c, _L(Rational(a + b + c, 2)))
        dung, sai = _tf_ct(r"$p = %s$", Rational(a + b + c, 2), ly_p,
                           [(Integer(a + b + c), "That is the perimeter, not yet divided by 2"), (Rational(a + b + c, 3), "Mistakenly divided by 3")])
        for X, (u, v, w) in random.sample([("A", (b, c, a)), ("B", (a, c, b)), ("C", (a, b, c))], 2):
            cs = Rational(u * u + v * v - w * w, 2 * u * v)
            ly = r"$\cos %s = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$." % (X, u, v, w, u, v, _L(cs))
            d_, s_ = _tf_ct(r"$\cos %s = %s$" % (X, "%s"), cs, ly,
                            [(-cs, "Wrong sign (swapped the opposite sides)"), (2 * cs, "Forgot the 2 in the denominator"),
                             (Rational(u * u + w * w - v * v, 2 * u * w), "Took the wrong opposite side")])
            dung += d_
            sai += s_
        y2 = _phat_bieu(dung, sai)
        # c) VD - diện tích (Heron)
        ly_c = r"$p = %d$, $S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$." % (
            p, p, p - a, p - b, p - c, S)
        y3 = _tf_gop(_tf_ct(r"$S = %s$", Integer(S), ly_c,
                            [(Integer(2 * S), "Multiplied by an extra factor of 2"), (sqrt((p - a) * (p - b) * (p - c)), "Missing factor $p$"),
                             (Rational(S, 2), "Divided by an extra factor of 2"), (sqrt(p * (p - a) * (p - b)), "Missing factor $\\left(p - c\\right)$")],
                            them=[r"$S^{2} = %d$" % (S * S)]))
        # d) VDC - đường cao / bán kính (hai đại lượng khác nhau)
        dung, sai = [], []
        for chon in random.sample(["h", "r", "R"], 2):
            if chon == "h":
                ten, canh, khac = random.choice([("a", a, b), ("b", b, c), ("c", c, a)])
                ha = Rational(2 * S, canh)
                ly = r"$S = \dfrac{1}{2}%s\cdot h_%s \Rightarrow h_%s = \dfrac{2S}{%s} = \dfrac{%d}{%d} = %s$." % (ten, ten, ten, ten, 2 * S, canh, _L(ha))
                d_, s_ = _tf_ct(r"$h_%s = %s$" % (ten, "%s"), ha, ly,
                                [(ha / 2, "Forgot to multiply by 2"), (Rational(2 * S, khac), "Divided by the wrong side"), (Rational(canh, 2 * S), "Numerator and denominator swapped")])
            elif chon == "r":
                r_ = Rational(S, p)
                ly = r"$S = pr \Rightarrow r = \dfrac{S}{p} = \dfrac{%d}{%d} = %s$." % (S, p, _L(r_))
                d_, s_ = _tf_ct(r"$r = %s$", r_, ly,
                                [(2 * r_, "Mistakenly used $S = \\dfrac{1}{2}pr$"), (Rational(S, 2 * p), "Divided by the perimeter instead of the semiperimeter"),
                                 (Rational(a * b * c, 4 * S), "Confused with the circumradius")])
            else:
                R_ = Rational(a * b * c, 4 * S)
                ly = r"$S = \dfrac{abc}{4R} \Rightarrow R = \dfrac{abc}{4S} = \dfrac{%d}{%d} = %s$." % (a * b * c, 4 * S, _L(R_))
                d_, s_ = _tf_ct(r"$R = %s$", R_, ly,
                                [(2 * R_, "Mistakenly using $R = \\dfrac{abc}{2S}$"), (4 * R_, "Forgot to divide by 4"), (Rational(S, p), "Confused with the inradius")])
            dung += d_
            sai += s_
        y4 = _phat_bieu(dung, sai)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C3_TF_M_01(socau, socot=1):
    r"""Đúng/Sai - hình bình hành $ABCD$ biết hai cạnh kề và góc $A$ ($60^{\circ}$ hoặc $120^{\circ}$): góc kề bù,
    đường chéo $BD$, đường chéo $AC$, côsin góc giữa hai đường chéo (tam giác $OAB$).

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    so = 0
    while so < socau:
        A = random.choice([60, 120])
        m, n = random.sample(range(2, 10), 2)
        cs = Rational(1, 2) if A == 60 else Rational(-1, 2)
        BD2, AC2 = m * m + n * n - 2 * m * n * cs, m * m + n * n + 2 * m * n * cs
        OA2, OB2 = AC2 / 4, BD2 / 4
        cosO = float((OA2 + OB2 - m * m) / (2 * sqrt(OA2) * sqrt(OB2)))
        gocO = math.degrees(math.acos(cosO))
        if not _xa_bien(cosO * 100) or m == n:
            continue
        so += 1
        debai = (r"Given parallelogram $ABCD$ with $AB = %d$, $AD = %d$, $\widehat{BAD} = %s$; $O$ is the intersection of the two diagonals. "
                 r"Determine whether each of the following statements is true or false." % (m, n, _goc(A)))
        # a) NB - tính chất hình bình hành
        ly_a = (r"In a parallelogram, opposite sides are equal ($BC = AD = %d$, $CD = AB = %d$), opposite angles are equal, "
                r"and two angles adjacent to a side are supplementary: $\widehat{ABC} = \widehat{ADC} = 180^{\circ} - %s = %s$, $\widehat{BCD} = %s$."
                % (n, m, _goc(A), _goc(180 - A), _goc(A)))
        y1 = _phat_bieu(
            [(r"$\widehat{ABC} = %s$" % _goc(180 - A), ly_a), (r"$\widehat{ADC} = %s$" % _goc(180 - A), ly_a),
             (r"$\widehat{BCD} = %s$" % _goc(A), ly_a), (r"$BC = %d$" % n, ly_a), (r"$CD = %d$" % m, ly_a)],
            [(r"$\widehat{ABC} = %s$" % _goc(A), ly_a), (r"$\widehat{ADC} = %s$" % _goc(A), ly_a),
             (r"$\widehat{BCD} = %s$" % _goc(180 - A), ly_a), (r"$BC = %d$" % m, ly_a), (r"$CD = %d$" % n, ly_a)])
        # b) TH - định lí côsin trong tam giác ABD (một lần thay số)
        ly_b = r"In triangle $ABD$: $BD^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %s = %s$." % (m * m, n * n, m, n, _goc(A), _L(BD2))
        y2 = _tf_gop(_tf_ct(r"$BD = %s$", sqrt(BD2), ly_b,
                            [(sqrt(AC2), "Wrong sign of $\\cos %s$" % _goc(A)), (sqrt(m * m + n * n), "Forgot the term $-2\\cdot AB\\cdot AD\\cos A$"),
                             (sqrt(m * m + n * n - m * n * cs), "Forgot the factor 2")],
                            them=[r"$BD^{2} = %s$" % _L(BD2)]))
        # c) VD - đường chéo AC (tam giác ABC, góc B = 180 - A)
        ly_c = (r"$BC = AD = %d$, $\widehat{ABC} = %s$; in triangle $ABC$: $AC^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %s = %s$."
                % (n, _goc(180 - A), m * m, n * n, m, n, _goc(180 - A), _L(AC2)))
        y3 = _tf_gop(_tf_ct(r"$AC = %s$", sqrt(AC2), ly_c,
                            [(sqrt(BD2), "Used angle $A$ instead of angle $B$"), (sqrt(m * m + n * n), "Forgot the term containing $\\cos B$"),
                             (sqrt(m * m + n * n + m * n * cs), "Forgot the factor 2")],
                            them=[r"$AC^{2} = %s$" % _L(AC2), r"$AC^{2} + BD^{2} = %d$" % (2 * (m * m + n * n))]))
        # d) VDC - côsin góc giữa hai đường chéo (tam giác OAB)
        ly_d = (r"$OA = \dfrac{AC}{2} = %s$, $OB = \dfrac{BD}{2} = %s$; in triangle $OAB$: "
                r"$\cos\widehat{AOB} = \dfrac{OA^{2} + OB^{2} - AB^{2}}{2\cdot OA\cdot OB}$." % (_L(sqrt(OA2)), _L(sqrt(OB2))))
        sai_c = [(-cosO, "Confused with angle $\\widehat{AOD}$ (side $AD$)"),
                 (float((AC2 + BD2 - m * m) / (2 * sqrt(AC2) * sqrt(BD2))), "Forgot to halve the two diagonals"),
                 (float((OA2 + OB2 - m * m) / (sqrt(OA2) * sqrt(OB2))), "Forgot the 2 in the denominator")]
        d1, s1 = _tf_so(r"$\cos\widehat{AOB} \approx %s$", cosO, 2, ly_d, sai_c, mien=(-1, 1))
        if _xa_bien(gocO):
            d2, s2 = _tf_so(r"$\widehat{AOB} \approx %s$", gocO, 0, ly_d + r" Hence $\widehat{AOB}$ is found with a calculator.",
                            [(180 - gocO, "Confused with the adjacent supplementary angle $\\widehat{AOD}$")], dv=r"^{\circ}")
            d1, s1 = d1 + d2, s1 + s2
        y4 = _phat_bieu(d1, s1)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C3_TF_N_01(socau, socot=1):
    r"""Đúng/Sai - ngọn núi quan sát từ chân và nóc toà nhà (có hình): a) góc $BAC$, b) góc $ACB$,
    c) khoảng cách $AC$, d) chiều cao ngọn núi.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_MC_N/MC_O/SA_P/SA_Q/TL_J. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        debai = _de_nui_toa_nha(h, al, be) + " Determine whether each of the following statements is true or false."
        # a) NB - đọc góc từ hình
        ly_a = (r"$AB$ is vertical and $AC$ makes an angle of $%s$ with the horizontal, so $\widehat{BAC} = 90^{\circ} - %s = %s$; "
                r"$BC$ makes an angle of $%s$ with the horizontal (upward), so $\widehat{ABC} = 90^{\circ} + %s = %s$."
                % (_goc(al), _goc(al), _goc(90 - al), _goc(be), _goc(be), _goc(90 + be)))
        y1 = _phat_bieu(
            [(r"$\widehat{BAC} = %s$" % _goc(90 - al), ly_a), (r"$\widehat{ABC} = %s$" % _goc(90 + be), ly_a),
             (r"$\widehat{CAH} = %s$" % _goc(al), ly_a)],
            [(r"$\widehat{BAC} = %s$" % _goc(al), ly_a), (r"$\widehat{ABC} = %s$" % _goc(90 - be), ly_a),
             (r"$\widehat{ABC} = %s$" % _goc(be), ly_a), (r"$\widehat{BAC} = %s$" % _goc(90 + al), ly_a)])
        # b) TH - tổng ba góc / góc tại C
        ly_b = (r"$\widehat{ACB} = 180^{\circ} - %s - %s = %s$; $CH$ is vertical, so $\widehat{ACH} = 90^{\circ} - %s = %s$."
                % (_goc(90 - al), _goc(90 + be), _goc(al - be), _goc(al), _goc(90 - al)))
        y2 = _phat_bieu(
            [(r"$\widehat{ACB} = %s$" % _goc(al - be), ly_b), (r"$\widehat{ACH} = %s$" % _goc(90 - al), ly_b)],
            [(r"$\widehat{ACB} = %s$" % _goc(al + be), ly_b), (r"$\widehat{ACB} = %s$" % _goc(90 - al + be), ly_b),
             (r"$\widehat{ACH} = %s$" % _goc(al), ly_b), (r"$\widehat{ACB} = %s$" % _goc(180 - al - be), ly_b)])
        # c) VD - định lí sin tìm AC
        ly_c = _giai_goc_nui(h, al, be, AC).split("\\\\\n")[-1]
        y3 = _tf_gop(_tf_so(r"$AC \approx %s$", AC, 0, ly_c,
                            [(h * _cos_d(be) / _sin_d(al + be), "Mistakenly taking $\\widehat{ACB} = %s$" % _goc(al + be)),
                             (h * _sin_d(al - be) / _cos_d(be), "Numerator and denominator swapped"),
                             (h * _sin_d(90 - al) / _sin_d(al - be), "Mistakenly used angle $\\widehat{BAC}$ (opposite $BC$)"),
                             (h / _sin_d(al - be), "Forgot to multiply by $\\sin\\widehat{ABC}$")], dv=r"\,\text{m}",
                            bdt=r"The distance $AC$ is %s $%s$"))
        # d) VDC - chiều cao ngọn núi
        ly_d = _giai_goc_nui(h, al, be, AC).split("\\\\\n")[-1] + " " + _giai_cao_nui(al, CH, AC)
        y4 = _tf_gop(_tf_so(r"The mountain's height above the ground is about $%s$", CH, 0, ly_d,
                            [(CH + h, "Wrongly added the height of the building"), (AC * _cos_d(al), "Confused $\\sin$ with $\\cos$"),
                             (AC * math.tan(math.radians(al)), "Mistakenly using $CH = AC\\cdot\\tan %s$" % _goc(al)), (CH - h, "Mistakenly subtracted the height of the building")],
                            dv=r"\,\text{m}", bdt=r"The mountain's height above the ground is %s $%s$", tu=("greater than", "less than")))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _lyn = ly_b + r" $\widehat{BCH} = 90^{\circ} - %s = %s$ ($CH$ is vertical and $BC$ makes an angle of $%s$ with the horizontal)." % (_goc(be), _goc(90 - be), _goc(be))
        _tf_them(y2, [(r"$\widehat{BCH} = %s$" % _goc(90 - be), _lyn)], [(r"$\widehat{BCH} = %s$" % _goc(be), _lyn), (r"$\widehat{BCH} = %s$" % _goc(90 + be), _lyn)])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_nui_toa_nha(h, al, be, CH), 0, socot)
    return cau


def L10_C3_TF_O_01(socau, socot=1):
    r"""Đúng/Sai - đĩa cổ bị vỡ (có hình): a) nửa chu vi, b) diện tích (Heron), c) góc lớn nhất, d) bán kính đĩa.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_MC_P/MC_Q/SA_R/SA_S/TL_K. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        a, b, c, p, S, R, dinh, g = _bo_dia_co()
        debai = _de_dia_co(a, b, c) + " Determine whether each of the following statements is true or false."
        cm, cm2 = r"\,\text{cm}", r"\,\text{cm}^{2}"
        # a) NB - nửa chu vi, chu vi
        ly_a = r"$p = \dfrac{%s + %s + %s}{2} = %s$ (cm), perimeter $2p = %s$ (cm)." % (_x1(a, 1), _x1(b, 1), _x1(c, 1), _xx(p, 2), _xx(2 * p, 2))
        y1 = _phat_bieu(
            [(r"The semiperimeter of triangle $ABC$ is $p = %s%s$" % (_xx(p, 2), cm), ly_a),
             (r"The perimeter of triangle $ABC$ is $%s%s$" % (_xx(2 * p, 2), cm), ly_a)],
            [(r"The semiperimeter of triangle $ABC$ is $p = %s%s$" % (_xx(2 * p, 2), cm), "That is the perimeter. " + ly_a),
             (r"The semiperimeter of triangle $ABC$ is $p = %s%s$" % (_xx((a + b + c) / 3, 2), cm), "Mistakenly divided by 3. " + ly_a),
             (r"The perimeter of triangle $ABC$ is $%s%s$" % (_xx(p, 2), cm), "That is the semiperimeter. " + ly_a)])
        # b) TH - Heron
        ly_b = r"By Heron's formula: $S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$."
        y2 = _tf_gop(_tf_so(r"$S_{ABC} \approx %s$", S, 1, ly_b,
                            [(2 * S, "Multiplied by an extra factor of 2"), (math.sqrt((p - a) * (p - b) * (p - c)), "Missing factor $p$"),
                             (math.sqrt(2 * p * (p - a) * (p - b) * (p - c)), "Used the perimeter instead of the semiperimeter")],
                            dv=cm2, bdt=r"The area of triangle $ABC$ is %s $%s$"))
        # c) VD - góc lớn nhất (đối diện cạnh lớn nhất)
        doi = {"A": "BC", "B": "CA", "C": "AB"}[dinh]
        goc_k = {"A": (b, c, a), "B": (a, c, b), "C": (a, b, c)}
        cac_goc = {X: math.degrees(math.acos((u * u + v * v - w * w) / (2 * u * v))) for X, (u, v, w) in goc_k.items()}
        nho = min(cac_goc, key=cac_goc.get)
        ly_c = (r"The largest angle is angle $%s$, opposite the longest side $%s$; $\cos %s \approx %s$, so $\widehat{%s} \approx %d^{\circ}$."
                % (dinh, doi, dinh, _xx(math.cos(math.radians(g)), 4), dinh, _lt(g)))
        dung = [(r"The largest angle of triangle $ABC$ is angle $%s$" % dinh, ly_c)]
        sai = [(r"The largest angle of triangle $ABC$ is angle $%s$" % X, ly_c) for X in "ABC" if X != dinh]
        d_, s_ = _tf_so(r"The largest angle of triangle $ABC$ is approximately $%s$", g, 0, ly_c,
                        [(180 - g, "Wrong sign of the cosine"), (cac_goc[nho], "That is the smallest angle")], dv=r"^{\circ}")
        (dung if g > 90 else sai).append((r"Triangle $ABC$ has an obtuse angle", ly_c))
        y3 = _phat_bieu(dung + d_, sai + s_)
        # d) VDC - bán kính đĩa
        ly_d = r"The edge of the disc is the circumcircle of triangle $ABC$, $R = \dfrac{abc}{4S}$."
        sai_R = [(2 * R, "That is the diameter"), (4 * R, "Forgot to divide by 4"), (S / p, "Confused with the inradius $r = \\dfrac{S}{p}$")]
        d1, s1 = _tf_so(r"The radius of the disc is approximately $%s$", R, 1, ly_d, sai_R, dv=cm,
                        bdt=r"The radius of the disc is %s $%s$")
        d2, s2 = _tf_so(r"The diameter of the disc is approximately $%s$", 2 * R, 1, ly_d, [(R, "That is the radius"), (4 * R, "Multiplied by an extra factor of 2")], dv=cm) \
            if _xa_bien(2 * R, 1) else ([], [])
        y4 = _phat_bieu(d1 + d2, s1 + s2)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _d1, _s1 = _tf_bdt(r"The semiperimeter of triangle $ABC$ is %s $%s$", p, ly_a, dv=cm)
        _tf_them(y1, _d1, _s1)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_duong_tron_ba_diem([100, 220, 330], "ABC"), 0, socot)
    return cau


def L10_C3_TF_O_02(socau, socot=1):
    r"""Đúng/Sai - hồ nước hình tròn (có hình): a) công thức côsin cho $BC$, b) $BC$, c) định lí sin cho
    đường kính, d) đường kính hồ.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_MC_P/MC_Q/SA_R/SA_S/TL_K. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        A, AB, AC, BC, d = _bo_ho_tron()
        debai = _de_ho_tron(A, AB, AC) + " Determine whether each of the following statements is true or false."
        g = _goc(A)
        # a) NB - định lí côsin
        ly_a = r"The law of cosines in triangle $ABC$ gives the side $BC$ opposite angle $A$."
        y1 = _phat_bieu(
            [(r"$BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$\cos %s = \dfrac{AB^{2} + AC^{2} - BC^{2}}{2\cdot AB\cdot AC}$" % g, ly_a)],
            [(r"$BC^{2} = AB^{2} + AC^{2} + 2\cdot AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$BC^{2} = AB^{2} + AC^{2} - AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$BC = AB + AC - 2\cdot AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$\cos %s = \dfrac{AB^{2} + AC^{2} + BC^{2}}{2\cdot AB\cdot AC}$" % g, ly_a)])
        # b) TH - tính BC
        y2 = _tf_gop(_tf_so(r"$BC \approx %s$", BC, 1, _giai_ho_bc(A, AB, AC, BC),
                            [(math.sqrt(AB * AB + AC * AC), "Omitted the term containing $\\cos A$"),
                             (math.sqrt(AB * AB + AC * AC + 2 * AB * AC * _cos_d(A)), "Sign error"),
                             (math.sqrt(AB * AB + AC * AC - AB * AC * _cos_d(A)), "Forgot the factor 2")],
                            dv=r"\,\text{m}", bdt=r"$BC$ %s $%s$"))
        # c) VD - định lí sin cho đường kính
        ly_c = r"The shore of the lake is the circumcircle of triangle $ABC$; by the law of sines, $\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B} = 2R$ is exactly the diameter."
        y3 = _phat_bieu(
            [(r"The diameter of the lake equals $\dfrac{BC}{\sin\widehat{BAC}}$", ly_c), (r"The radius of the lake equals $\dfrac{BC}{2\sin\widehat{BAC}}$", ly_c),
             (r"The diameter of the lake equals $\dfrac{AC}{\sin\widehat{ABC}}$", ly_c)],
            [(r"The diameter of the lake equals $\dfrac{BC}{2\sin\widehat{BAC}}$", ly_c), (r"The radius of the lake equals $\dfrac{BC}{\sin\widehat{BAC}}$", ly_c),
             (r"The diameter of the lake equals $\dfrac{BC}{\cos\widehat{BAC}}$", ly_c), (r"The diameter of the lake equals $BC\cdot\sin\widehat{BAC}$", ly_c),
             (r"The diameter of the lake equals $\dfrac{AC}{\sin\widehat{BAC}}$", ly_c)])
        # d) VDC - đường kính hồ
        ly_d = _giai_ho_bc(A, AB, AC, BC) + " " + _giai_ho_d(A, BC, d)
        y4 = _tf_gop(_tf_so(r"The diameter of the lake is approximately $%s$", d, 0, ly_d,
                            [(d / 2, "That is the radius"), (BC * _sin_d(A), "Mistakenly using $d = BC\\cdot\\sin A$"),
                             (math.sqrt(AB * AB + AC * AC) / _sin_d(A), "Miscalculated $BC$ (forgot the term containing $\\cos A$)")],
                            dv=r"\,\text{m}", bdt=r"The diameter of the lake is %s $%s$"))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(r"$AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos\widehat{ABC}$", ly_a)],
                 [(r"$AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos %s$" % g, ly_a)])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_duong_tron_ba_diem(_goc_ve_ho(A, AB, AC), "ABC", ho=True), 0, socot)
    return cau


def L10_C3_TF_P_01(socau, socot=1):
    r"""Đúng/Sai - cây bị gãy (có hình): a) góc $ACB$, b) đoạn $AC$, c) đoạn $BC$, d) chiều cao cây trước khi gãy.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_MC_R/MC_S/SA_T/SA_U/TL_L. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        debai = _de_cay_gay(AB, A, B) + " Determine whether each of the following statements is true or false."
        m = r"\,\text{m}"
        # a) NB - tổng ba góc
        ly_a = r"$\widehat{ACB} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C))
        y1 = _phat_bieu(
            [(r"$\widehat{ACB} = %s$" % _goc(C), ly_a), (r"$\widehat{ACB} + \widehat{CAB} = %s$" % _goc(180 - B), ly_a)],
            [(r"$\widehat{ACB} = %s$" % _goc(C + 10), ly_a), (r"$\widehat{ACB} = %s$" % _goc(A + B), ly_a),
             (r"$\widehat{ACB} = %s$" % _goc(90 - B), "There is no right angle at $A$. " + ly_a),
             (r"$\widehat{ACB} + \widehat{CAB} = %s$" % _goc(180 - A), ly_a)])
        # b) TH - định lí sin cho AC
        ly_b = r"Law of sines: $AC = \dfrac{AB\cdot\sin B}{\sin C} = \dfrac{%s\cdot\sin %s}{\sin %s}$." % (_xx(AB, 1), _goc(B), _goc(C))
        y2 = _tf_gop(_tf_so(r"$AC \approx %s$", AC, 1, ly_b,
                            [(BC, "Mistakenly used angle $A$ (that gives $BC$)"), (AB * _sin_d(C) / _sin_d(B), "Numerator and denominator swapped"),
                             (AB * math.tan(math.radians(B)), "Treated the triangle as right-angled at $A$")], dv=m, bdt=r"The segment $AC$ is %s $%s$"))
        # c) VD - BC
        ly_c = r"$BC = \dfrac{AB\cdot\sin A}{\sin C} = \dfrac{%s\cdot\sin %s}{\sin %s}$." % (_xx(AB, 1), _goc(A), _goc(C))
        y3 = _tf_gop(_tf_so(r"$BC \approx %s$", BC, 1, ly_c,
                            [(AC, "Mistakenly used angle $B$ (that gives $AC$)"), (AB / _cos_d(B), "Treated the triangle as right-angled at $A$"),
                             (AB * _sin_d(A) / _sin_d(B), "Mistakenly used the angle opposite $AB$")], dv=m, bdt=r"The segment $BC$ is %s $%s$"))
        # d) VDC - chiều cao cây trước khi gãy
        ly_d = ly_b + " " + ly_c + r" The height of the tree before it broke is $AC + BC$."
        y4 = _tf_gop(_tf_so(r"Before it broke, the tree's height was about $%s$", H, 1, ly_d,
                            [(AC + AB, "Mistakenly added $AB$"), (AC, "Forgot the broken-off top part $BC$"), (BC + AB, "Mistakenly added $AB$"),
                             (math.sqrt(AB * AB + AC * AC) + AC, "Treated the triangle as right-angled at $A$")],
                            dv=m, bdt=r"Before it broke, the tree's height was %s $%s$", tu=("greater than", "less than")))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(r"Angle $\widehat{ACB}$ is %s" % ("acute" if C < 90 else "obtuse"), ly_a)],
                 [(r"Angle $\widehat{ACB}$ is %s" % ("obtuse" if C < 90 else "acute"), ly_a)])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_cay_gay(AB, A, B, AC), 0, socot)
    return cau


def L10_C3_TF_Q_01(socau, socot=1):
    r"""Đúng/Sai - đo chiều cao tháp chính Pô Klông Garai bằng hai giác kế (có hình): a) góc $A_1DB_1$, b) $B_1D$,
    c) $C_1D$, d) chiều cao tháp.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_MC_D_04/SA_D_04. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AB, BD, C1D, CD = _bo_thap_cham()
        debai = _de_thap_cham(h, al, be, AB) + " Determine whether each of the following statements is true or false."
        m = r"\,\text{m}"
        # a) NB - góc ngoài, góc kề bù
        ly_a = (r"$\widehat{DA_1B_1} = 180^{\circ} - %s = %s$ (supplementary to $\widehat{DA_1C_1}$); angle $\widehat{DA_1C_1}$ is an exterior angle "
                r"of triangle $A_1DB_1$, so $\widehat{A_1DB_1} = %s - %s = %s$." % (_goc(al), _goc(180 - al), _goc(al), _goc(be), _goc(al - be)))
        y1 = _phat_bieu(
            [(r"$\widehat{A_1DB_1} = %s$" % _goc(al - be), ly_a), (r"$\widehat{DA_1B_1} = %s$" % _goc(180 - al), ly_a)],
            [(r"$\widehat{A_1DB_1} = %s$" % _goc(180 - al - be), ly_a), (r"$\widehat{A_1DB_1} = %s$" % _goc(al + be), ly_a),
             (r"$\widehat{DA_1B_1} = %s$" % _goc(al), ly_a), (r"$\widehat{A_1DB_1} = %s$" % _goc(90 - be), ly_a)])
        # b) TH - định lí sin trong tam giác A1DB1
        ly_b = r"Law of sines: $B_1D = \dfrac{A_1B_1\cdot\sin\left(180^{\circ} - %s\right)}{\sin %s}$." % (_goc(al), _goc(al - be))
        y2 = _tf_gop(_tf_so(r"$B_1D \approx %s$", BD, 1, ly_b,
                            [(AB * _sin_d(be) / _sin_d(al - be), "Mistakenly used angle $B_1$ (that gives $A_1D$)"),
                             (AB * _sin_d(al) / _sin_d(be), "Mistakenly divided by $\\sin %s$" % _goc(be)),
                             (AB / _sin_d(al - be), "Forgot to multiply by $\\sin\\widehat{DA_1B_1}$")], dv=m, bdt=r"$B_1D$ %s $%s$"))
        # c) VD - tam giác vuông B1C1D
        ly_c = ly_b + r" Triangle $B_1C_1D$ is right-angled at $C_1$: $C_1D = B_1D\cdot\sin %s$." % _goc(be)
        y3 = _tf_gop(_tf_so(r"$C_1D \approx %s$", C1D, 1, ly_c,
                            [(BD * _cos_d(be), "Confused $\\sin$ with $\\cos$"), (BD * math.tan(math.radians(be)), "Mistakenly using $C_1D = B_1D\\cdot\\tan %s$" % _goc(be)),
                             (BD, "Took the hypotenuse $B_1D$")], dv=m, bdt=r"$C_1D$ %s $%s$"))
        # d) VDC - chiều cao tháp
        ly_d = ly_c + r" $CD = C_1D + CC_1 = C_1D + %s$ (the height of the theodolite must be added)." % _xx(h, 1)
        y4 = _tf_gop(_tf_so(r"The tower's height is about $%s$", CD, 1, ly_d,
                            [(C1D, "Forgot to add the height of the theodolite"), (C1D + 2 * h, "Added the height of the theodolite twice"),
                             (BD * _cos_d(be) + h, "Confused $\\sin$ with $\\cos$")],
                            dv=m, bdt=r"The tower's height is %s $%s$", tu=("greater than", "less than")))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(r"$\widehat{DB_1A_1} = %s$" % _goc(be), ly_a)], [(r"$\widehat{DB_1A_1} = %s$" % _goc(180 - be), ly_a)])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_thap_cham(h, al, be, AB, CD), 0, socot)
    return cau


def L10_C3_TF_R_01(socau, socot=1):
    r"""Đúng/Sai - hai tàu cùng xuất phát từ một bến theo hai hướng hợp góc $\varphi$ (có hình): a) quãng
    đường tàu thứ nhất sau $t$ giờ, b) khoảng cách hai tàu sau $t$ giờ, c) côsin góc tại vị trí tàu thứ
    nhất, d) sau bao lâu hai tàu cách nhau $D$ hải lí.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_SA_C ("hai tau cung xuat phat"); theo phan III tai lieu
    C3-B2 (120 do, 8 va 10 hai li/gio, cach 60 hai li). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    n = 0
    while n < socau:
        g = random.choice([60, 75, 100, 110, 120])
        v1, v2 = random.sample(range(6, 15), 2)
        t = random.choice([1.5, 2, 2.5, 3])
        D = random.choice([30, 40, 50, 60, 80])
        b, c = v1 * t, v2 * t
        k = math.sqrt(v1 * v1 + v2 * v2 - 2 * v1 * v2 * _cos_d(g))
        d = k * t
        cosB = (b * b + d * d - c * c) / (2 * b * d)
        cosC = (c * c + d * d - b * b) / (2 * c * d)
        T = D / k
        if not (_xa_bien(d, 1) and _xa_bien(T, 1) and _xa_bien(cosB * 100, 0) and 1 < T < 8):
            continue
        n += 1
        debai = (r"Two fishing boats leave harbor $A$ at the same time and sail straight at constant speeds in two directions forming an angle of $%s$. "
                 r"The first boat travels at $%d$ nautical miles per hour and the second boat at $%d$ nautical miles per hour. Let $B$, $C$ "
                 r"be the positions of the two boats after $%s$ hours. Determine whether each of the following statements is true or false." % (_goc(g), v1, v2, _xx(t, 1)))
        # a) NB - quãng đường = vận tốc x thời gian
        ly_a = r"$AB = %d\cdot %s = %s$ (nautical miles), $AC = %d\cdot %s = %s$ (nautical miles)." % (v1, _xx(t, 1), _xx(b, 1), v2, _xx(t, 1), _xx(c, 1))
        y1 = _phat_bieu(
            [(r"$AB = %s$ nautical miles" % _xx(b, 1), ly_a), (r"$AC = %s$ nautical miles" % _xx(c, 1), ly_a)],
            [(r"$AB = %s$ nautical miles" % _xx(v1 + t, 1), ly_a), (r"$AB = %s$ nautical miles" % _xx(c, 1), ly_a),
             (r"$AC = %s$ nautical miles" % _xx(b, 1), ly_a), (r"$AB = %s$ nautical miles" % _xx(v1 / t, 1), ly_a)])
        # b) TH - định lí côsin
        ly_b = r"$BC^{2} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot\cos %s$." % (_xx(b, 1), _xx(c, 1), _xx(b, 1), _xx(c, 1), _goc(g))
        y2 = _tf_gop(_tf_so(r"$BC \approx %s$ nautical miles", d, 1, ly_b,
                            [(math.sqrt(b * b + c * c), "Forgot the term containing $\\cos$"),
                             (math.sqrt(b * b + c * c + 2 * b * c * _cos_d(g)), "Sign error"),
                             (math.sqrt(b * b + c * c - b * c * _cos_d(g)), "Forgot the factor 2")],
                            bdt=r"After $%s$ hours, the two boats are %s $%s$ nautical miles apart" % (_xx(t, 1), "%s", "%s"), tu=("more than", "less than")))
        # c) VD - côsin góc tại B
        ly_c = ly_b + r" $\cos\widehat{ABC} = \dfrac{AB^{2} + BC^{2} - AC^{2}}{2\cdot AB\cdot BC}$."
        d_, s_ = _tf_so(r"$\cos\widehat{ABC} \approx %s$", cosB, 2, ly_c,
                        [(-cosB, "Sign error"), (cosC, "Mistakenly used angle $C$"), (2 * cosB, "Forgot the 2 in the denominator")], mien=(-1, 1))
        dung, sai = d_, s_
        (dung if cosB > 0 else sai).append((r"Angle $\widehat{ABC}$ is an acute angle", ly_c))
        (sai if cosB > 0 else dung).append((r"Angle $\widehat{ABC}$ is an obtuse angle", ly_c))
        y3 = _phat_bieu(dung, sai)
        # d) VDC - thời gian để hai tàu cách nhau D hải lí
        ly_d = (r"After $x$ hours: $AB = %dx$, $AC = %dx$, $BC^{2} = x^{2}\left(%d + %d - 2\cdot %d\cdot %d\cdot\cos %s\right)$, so "
                r"$BC = x\cdot %s$. Solve $x\cdot %s = %d$." % (v1, v2, v1 * v1, v2 * v2, v1, v2, _goc(g), _xx(k, 3), _xx(k, 3), D))
        y4 = _tf_gop(_tf_so(r"The two boats are $%d$ nautical miles apart after about $%s$ hours from the time they set out" % (D, "%s"), T, 1, ly_d,
                            [(D / (v1 + v2), "Added the two speeds as if the boats were traveling in opposite directions"),
                             (D / math.sqrt(v1 * v1 + v2 * v2), "Forgot the term containing $\\cos$"),
                             (D / math.sqrt(v1 * v1 + v2 * v2 + 2 * v1 * v2 * _cos_d(g)), "Sign error")],
                            bdt=r"The two boats are $%d$ nautical miles apart after %s $%s$ hours from the time they set out" % (D, "%s", "%s"), tu=("more than", "less than")))
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _lyr = ly_a + r" After $%s$ hours, the two boats have traveled a total of $%s$ nautical miles." % (_xx(t, 1), _xx(b + c, 1))
        _tf_them(y1, [(r"After $%s$ hours, the two boats have traveled a total of $%s$ nautical miles" % (_xx(t, 1), _xx(b + c, 1)), _lyr)],
                 [(r"After $%s$ hours, the two boats have traveled a total of $%s$ nautical miles" % (_xx(t, 1), _xx(v1 + v2 + t, 1)), _lyr),
                  (r"After $%s$ hours, the two boats have traveled a total of $%s$ nautical miles" % (_xx(t, 1), _xx(abs(c - b), 1)), _lyr)])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_hai_tau(g), 0, socot)
    return cau


# ---------- TF_S: điểm M trên nửa đường tròn đơn vị xác định bởi góc alpha (có hình) ----------
# Mỗi ý là một DANH SÁCH nhiều phát biểu ĐÚNG và nhiều phát biểu SAI (lỗi hay gặp khác nhau);
# TF_baitoan_du chọn ngẫu nhiên một phát biểu cho mỗi ý -> mỗi lần chạy ra đề khác (cô Lan 01/10/2026).

_GOC_DAC_BIET_TF_S = {30: (Rational(1, 2), sqrt(3) / 2), 45: (sqrt(2) / 2, sqrt(2) / 2), 60: (sqrt(3) / 2, Rational(1, 2)),
                      120: (sqrt(3) / 2, Rational(-1, 2)), 135: (sqrt(2) / 2, -sqrt(2) / 2), 150: (Rational(1, 2), -sqrt(3) / 2)}


def _hinh_nua_dtdv(goc):
    """Nửa đường tròn đơn vị trong hệ trục Oxy, M ứng với góc xOM = goc (độ), hình chiếu của M lên hai trục,
    cung góc alpha, A(1; 0), A'(-1; 0)."""
    c, s = math.cos(math.radians(goc)), math.sin(math.radians(goc))
    R = 1.8
    xm, ym = R * c, R * s
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round,>=stealth]\n"
        "\\draw[->] (-2.4,0) -- (2.5,0) node[below] {$x$};\n"
        "\\draw[->] (0,-0.3) -- (0,2.4) node[left] {$y$};\n"
        "\\draw (%.2f,0) arc (0:180:%.2f);\n" % (R, R)
        + "\\draw[thick] (0,0) -- (%.3f,%.3f);\n" % (xm, ym)
        + "\\draw[dashed] (%.3f,%.3f) -- (%.3f,0) (%.3f,%.3f) -- (0,%.3f);\n" % (xm, ym, xm, xm, ym, ym)
        + "\\draw[->] (0.45,0) arc (0:%.1f:0.45);\n" % goc
        + "\\node at (%.3f,%.3f) {$\\alpha$};\n" % (0.72 * math.cos(math.radians(goc / 2)), 0.72 * math.sin(math.radians(goc / 2)))
        + "\\fill (%.3f,%.3f) circle (0.04) node[above %s] {$M$};\n" % (xm, ym, "right" if c >= 0 else "left")
        + "\\node[below] at (%.3f,0) {$x_0$};\n" % xm
        + "\\node[%s] at (0,%.3f) {$y_0$};\n" % ("left" if c >= 0 else "right", ym)
        + "\\fill (%.2f,0) circle (0.03) node[below right] {$A$};\n" % R
        + "\\fill (%.2f,0) circle (0.03) node[below left] {$A'$};\n" % (-R)
        + "\\node[below left] at (0,0) {$O$};\n"
        + "\\end{tikzpicture}"
    )


def _bo_tf_s():
    """(kiểu cho, góc (độ, để vẽ), sin, cos) - sin, cos chính xác. Kiểu 'goc' luôn là góc đặc biệt."""
    kieu = random.choice(["goc", "goc", "x", "y", "cos", "sin", "tan", "cot"])
    if kieu == "goc" or random.random() < 0.3:
        g = random.choice(list(_GOC_DAC_BIET_TF_S))
        s, c = _GOC_DAC_BIET_TF_S[g]
    else:
        doi, ke, huyen = random.choice(BO_BA_PYTAGO)
        if random.random() < 0.5:
            doi, ke = ke, doi
        s, c = Rational(doi, huyen), Rational(random.choice([1, -1]) * ke, huyen)
        g = math.degrees(math.atan2(float(s), float(c)))
    return kieu, g, s, c


def _phat_bieu(dung_ds, sai_ds):
    """Gộp nhiều phát biểu đúng [(nội dung, lời giải)] và sai [(nội dung, lời giải)] thành một ý TF;
    bỏ phát biểu sai trùng nội dung với phát biểu đúng."""
    noi_dung_dung = {d for d, _ in dung_ds}
    y = [(r"{\True %s}" % d, "True. " + l) for d, l in dung_ds]
    da = set()
    for d, l in sai_ds:
        if d in noi_dung_dung or d in da:
            continue
        da.add(d)
        y.append((r"{%s}" % d, "False. " + l))
    return y


def _so_tf(v, n=2):
    """Giá trị đúng: dạng chính xác nếu gọn, không thì gần đúng n chữ số (kèm 'làm tròn')."""
    v = simplify(v)
    t = _gon(v)
    if len(t) <= 24:
        return "= " + t, None
    return r"\approx " + _x1(float(v), n), "(rounded to the nearest hundredth)"


def L10_C3_TF_S_01(socau, socot=1):
    r"""Đúng/Sai - điểm $M\left(x_0; y_0\right)$ trên nửa đường tròn đơn vị, $\widehat{xOM} = \alpha$, $A\left(1; 0\right)$,
    $A'\left(-1; 0\right)$ (có hình). Câu dẫn cho NGẪU NHIÊN: số đo góc $\alpha$ (góc đặc biệt), hoành độ $x_0$, tung độ
    $y_0$ (kèm nhọn/tù), $\cos\alpha$, $\sin\alpha$ (kèm nhọn/tù), $\tan\alpha$ hoặc $\cot\alpha$.
    Mỗi ý có NHIỀU phát biểu đúng và NHIỀU phát biểu sai (lỗi khác nhau), mỗi lần chạy chọn ngẫu nhiên.
    a) (NB) lý thuyết: định nghĩa theo toạ độ, dấu, miền giá trị, điều kiện xác định;
    b) (TH) một bước: cho góc / toạ độ -> sin, cos, toạ độ; cos -> sin, sin -> cos, tan -> cot, cot -> tan;
    c) (VD) biểu thức đơn giản (a sin + b cos, a tan + b cot, sin.cos, sin^2 - cos^2, ...);
    d) (VDC) giải tam giác OAM, OA'M, AMA': cạnh AM, A'M (định lí côsin), chu vi, đường cao, bán kính
       ngoại tiếp, bán kính nội tiếp (KHÔNG hỏi các yếu tố có ngay từ đường tròn đơn vị: OM = 1, AA' = 2,
       góc AMA' vuông, diện tích = y_0/2...).

    CLAUDE THEM 01/10/2026 - theo y co Lan. Co Lan duyet lai.
    01/10/2026: b) them phat bieu dung khi cau dan cho toa do.
    """
    cau = ""
    so = 0
    while so < socau:
        kieu, g, s, c = _bo_tf_s()
        t, k = simplify(s / c), simplify(c / s)
        tu = float(c) < 0
        loai = "obtuse" if tu else "acute"
        gi = int(round(g))
        if kieu == "goc":
            gia = r"$\alpha = %s$" % _goc(gi)
        elif kieu == "x":
            gia = r"point $M$ has x-coordinate $x_0 = %s$" % _L(c)
        elif kieu == "y":
            gia = r"point $M$ has y-coordinate $y_0 = %s$ and angle $\alpha$ is %s" % (_L(s), loai)
        elif kieu == "cos":
            gia = r"$\cos\alpha = %s$" % _L(c)
        elif kieu == "sin":
            gia = r"$\sin\alpha = %s$ and angle $\alpha$ is %s" % (_L(s), loai)
        elif kieu == "tan":
            gia = r"$\tan\alpha = %s$" % _L(t)
        else:
            gia = r"$\cot\alpha = %s$" % _L(k)
        debai = (r"In the coordinate plane $Oxy$, the point $M\left(x_0; y_0\right)$ lies on the unit semicircle such that "
                 r"$\widehat{xOM} = \alpha$, and the points are $A\left(1; 0\right)$, $A'\left(-1; 0\right)$ (see figure). Given that %s. "
                 r"Determine whether each of the following statements is true or false." % gia)
        dau = "<" if tu else ">"
        nguoc = ">" if tu else "<"

        # a) NB - lý thuyết
        DN = r"By definition: $\sin\alpha = y_0$, $\cos\alpha = x_0$, $\tan\alpha = \dfrac{y_0}{x_0}$, $\cot\alpha = \dfrac{x_0}{y_0}$."
        DAU = r"Since angle $\alpha$ is %s, $\cos\alpha %s 0$, $\tan\alpha %s 0$, $\cot\alpha %s 0$; always $\sin\alpha \ge 0$ for $0^{\circ} \le \alpha \le 180^{\circ}$." % (loai, dau, dau, dau)
        y1 = _phat_bieu(
            [(r"$\sin\alpha = y_0$", DN), (r"$\cos\alpha = x_0$", DN), (r"$\tan\alpha = \dfrac{y_0}{x_0}$", DN),
             (r"$\cot\alpha = \dfrac{x_0}{y_0}$", DN),
             (r"$x_0^{2} + y_0^{2} = 1$", r"Since $M$ lies on the unit circle, $OM^{2} = x_0^{2} + y_0^{2} = 1$."),
             (r"$\cos\alpha %s 0$" % dau, DAU), (r"$\tan\alpha %s 0$" % dau, DAU), (r"$\sin\alpha > 0$", DAU),
             (r"$-1 \le \cos\alpha \le 1$", r"$\cos\alpha = x_0$ with $-1 \le x_0 \le 1$.")],
            [(r"$\sin\alpha = x_0$", DN), (r"$\cos\alpha = y_0$", DN), (r"$\tan\alpha = \dfrac{x_0}{y_0}$", DN),
             (r"$\cot\alpha = \dfrac{y_0}{x_0}$", DN),
             (r"$x_0 + y_0 = 1$", r"Since $M$ lies on the unit circle, $x_0^{2} + y_0^{2} = 1$, not $x_0 + y_0 = 1$."),
             (r"$\cos\alpha %s 0$" % nguoc, DAU), (r"$\tan\alpha %s 0$" % nguoc, DAU), (r"$\sin\alpha < 0$", DAU),
             (r"$\tan\alpha\cdot\cot\alpha = -1$", r"$\tan\alpha\cdot\cot\alpha = \dfrac{y_0}{x_0}\cdot\dfrac{x_0}{y_0} = 1$.")])

        # b) TH - một bước
        if kieu == "goc":
            ly = r"Table of trigonometric values: $\sin %s = %s$, $\cos %s = %s$, so $M\left(%s; %s\right)$." % (
                _goc(gi), _L(s), _goc(gi), _L(c), _L(c), _L(s))
            dung = [(r"$\sin\alpha = %s$" % _L(s), ly), (r"$\cos\alpha = %s$" % _L(c), ly),
                    (r"$M\left(%s; %s\right)$" % (_L(c), _L(s)), ly), (r"$x_0 = %s$" % _L(c), ly)]
            sai = [(r"$\sin\alpha = %s$" % _L(c), ly), (r"$\cos\alpha = %s$" % _L(-c), ly),
                   (r"$M\left(%s; %s\right)$" % (_L(s), _L(c)), ly), (r"$y_0 = %s$" % _L(c), ly)]
        elif kieu in ("x", "y"):
            ly = r"$\cos\alpha = x_0 = %s$." % _L(c) if kieu == "x" else r"$\sin\alpha = y_0 = %s$." % _L(s)
            v, ham = (c, "cos") if kieu == "x" else (s, "sin")
            khac = "sin" if ham == "cos" else "cos"
            dung = [(r"$\%s\alpha = %s$" % (ham, _L(v)), ly), (r"$\%s^{2}\alpha = %s$" % (ham, _L(v ** 2)), ly)]
            if ham == "sin":
                dung.append((r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(v), ly + r" Two supplementary angles have equal sines."))
            else:
                dung.append((r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(-v), ly + r" Two supplementary angles have opposite cosines."))
            sai = [(r"$\%s\alpha = %s$" % (khac, _L(v)), ly), (r"$\%s\alpha = %s$" % (ham, _L(-v)), ly),
                   (r"$\%s\alpha = %s$" % (ham, _L(1 - v)), ly), (r"$\%s^{2}\alpha = %s$" % (ham, _L(1 - v ** 2)), ly)]
        elif kieu == "cos":
            ly = r"$\sin^{2}\alpha = 1 - \cos^{2}\alpha = %s$, and since $\sin\alpha \ge 0$, $\sin\alpha = %s$." % (_L(s ** 2), _L(s))
            dung = [(r"$\sin\alpha = %s$" % _L(s), ly), (r"$\sin^{2}\alpha = %s$" % _L(s ** 2), ly)]
            sai = [(r"$\sin\alpha = %s$" % _L(-s), ly), (r"$\sin\alpha = %s$" % _L(1 - c), ly), (r"$\sin^{2}\alpha = %s$" % _L(1 + c ** 2), ly)]
        elif kieu == "sin":
            ly = r"$\cos^{2}\alpha = 1 - \sin^{2}\alpha = %s$, and since angle $\alpha$ is %s, $\cos\alpha = %s$." % (_L(c ** 2), loai, _L(c))
            dung = [(r"$\cos\alpha = %s$" % _L(c), ly), (r"$\cos^{2}\alpha = %s$" % _L(c ** 2), ly)]
            sai = [(r"$\cos\alpha = %s$" % _L(-c), ly), (r"$\cos\alpha = %s$" % _L(1 - s), ly), (r"$\cos^{2}\alpha = %s$" % _L(1 + s ** 2), ly)]
        elif kieu == "tan":
            ly = r"$\cot\alpha = \dfrac{1}{\tan\alpha} = %s$." % _L(k)
            dung = [(r"$\cot\alpha = %s$" % _L(k), ly), (r"$\tan\alpha\cdot\cot\alpha = 1$", ly)]
            sai = [(r"$\cot\alpha = %s$" % _L(-k), ly), (r"$\cot\alpha = %s$" % _L(t), ly), (r"$\cot\alpha = %s$" % _L(-t), ly),
                   (r"$\tan\alpha\cdot\cot\alpha = -1$", ly + r" We always have $\tan\alpha\cdot\cot\alpha = 1$.")]
        else:
            ly = r"$\tan\alpha = \dfrac{1}{\cot\alpha} = %s$." % _L(t)
            dung = [(r"$\tan\alpha = %s$" % _L(t), ly), (r"$\tan\alpha\cdot\cot\alpha = 1$", ly)]
            sai = [(r"$\tan\alpha = %s$" % _L(-t), ly), (r"$\tan\alpha = %s$" % _L(k), ly), (r"$\tan\alpha = %s$" % _L(-k), ly),
                   (r"$\tan\alpha\cdot\cot\alpha = -1$", ly + r" We always have $\tan\alpha\cdot\cot\alpha = 1$.")]
        y2 = _phat_bieu(dung, sai)

        # c) VD - biểu thức đơn giản (nhiều dạng)
        nen = r"We have $\sin\alpha = %s$, $\cos\alpha = %s$, $\tan\alpha = %s$, $\cot\alpha = %s$" % (_L(s), _L(c), _L(t), _L(k))
        if kieu in ("tan", "cot"):
            nen += r" (from $1 + \tan^{2}\alpha = \dfrac{1}{\cos^{2}\alpha}$ and the sign of $\cos\alpha$)"
        a_, b_ = random.choice([(1, 1), (2, 1), (1, 2), (2, -1), (1, -1), (3, 1), (1, 3), (3, -2)])

        def _bt(x, y, u, v):
            return ("" if x == 1 else str(x)) + u + (" + " if y > 0 else " - ") + ("" if abs(y) == 1 else str(abs(y))) + v

        BT = [
            (_bt(a_, b_, r"\sin\alpha", r"\cos\alpha"), a_ * s + b_ * c, [a_ * s - b_ * c, a_ * c + b_ * s]),
            (_bt(a_, b_, r"\tan\alpha", r"\cot\alpha"), a_ * t + b_ * k, [a_ * t - b_ * k, a_ * k + b_ * t]),
            (r"\sin\alpha\cdot\cos\alpha", s * c, [-s * c, s + c]),
            (r"\sin^{2}\alpha - \cos^{2}\alpha", s ** 2 - c ** 2, [c ** 2 - s ** 2, s - c, Integer(1), Integer(-1)]),
            (r"2\sin^{2}\alpha + \cos^{2}\alpha", 2 * s ** 2 + c ** 2, [2 * s ** 2 - c ** 2, s ** 2 + 2 * c ** 2, 2 * s + c]),
            (r"\dfrac{\sin\alpha + \cos\alpha}{\sin\alpha - \cos\alpha}", (s + c) / (s - c) if s != c else None,
             [(s - c) / (s + c) if s != -c else None, -(s + c) / (s - c) if s != c else None]),
        ]
        dung, sai = [], []
        for bt, P, Ps in random.sample(BT, len(BT)):
            if P is None:
                continue
            if len(dung) == 3:
                break
            P = simplify(P)
            ly = nen + r", so $P = %s = %s$." % (bt, _gon(P))
            dung.append((r"$P = %s = %s$" % (bt, _gon(P)), ly))
            for Q in Ps:
                if Q is not None and simplify(Q - P) != 0:
                    sai.append((r"$P = %s = %s$" % (bt, _gon(simplify(Q))), ly))
        y3 = _phat_bieu(dung, sai)

        # d) VDC - giải tam giác OAM / OA'M / AMA'
        cf, sf = float(c), float(s)
        AM, AM_ = math.sqrt(2 - 2 * cf), math.sqrt(2 + 2 * cf)            # AM, A'M
        S_OAM, S_AMA = sf / 2, sf                                         # diện tích
        nen_d = (r"Triangle $OAM$ has $OA = OM = 1$, $\widehat{AOM} = \alpha$; by the law of cosines, "
                 r"$AM^{2} = 1 + 1 - 2\cos\alpha = 2 - 2\cdot\left(%s\right)$, so $AM \approx %s$. "
                 r"Similarly, in triangle $OA'M$ ($\widehat{A'OM} = 180^{\circ} - \alpha$): "
                 r"$A'M^{2} = 2 + 2\cos\alpha$, $A'M \approx %s$." % (_L(c), _x1(AM, 3), _x1(AM_, 3)))
        DL = [
            (r"Perimeter of triangle $AMA'$", 2 + AM + AM_, nen_d + r" The perimeter of triangle $AMA'$ is $2 + AM + A'M$.", [AM + AM_, 1 + AM + AM_]),
            (r"Inradius of triangle $AMA'$", S_AMA / ((2 + AM + AM_) / 2),
             nen_d + r" $S_{AMA'} = \dfrac{1}{2}\cdot AA'\cdot y_0 = %s$, semiperimeter $p = \dfrac{2 + AM + A'M}{2}$, "
                     r"$r = \dfrac{S}{p}$." % _L(s), [S_AMA / (2 + AM + AM_), S_AMA * 2 / (2 + AM + AM_) * 2]),
            (r"Altitude from $O$ of triangle $OAM$", 2 * S_OAM / AM,
             nen_d + r" $S_{OAM} = \dfrac{1}{2}\cdot OA\cdot OM\cdot\sin\alpha = %s$, altitude $h = \dfrac{2S_{OAM}}{AM}$." % _L(s / 2),
             [S_OAM / AM, AM / 2 + 0.1]),
            (r"Altitude from $O$ of triangle $OA'M$", 2 * (sf / 2) / AM_,
             nen_d + r" $S_{OA'M} = \dfrac{1}{2}\sin\left(180^{\circ} - \alpha\right) = %s$, altitude $h = \dfrac{2S_{OA'M}}{A'M}$." % _L(s / 2),
             [(sf / 2) / AM_, AM_ / 2 + 0.1]),
            (r"Circumradius of triangle $OAM$", AM / (2 * sf),
             nen_d + r" By the law of sines in triangle $OAM$: $\dfrac{AM}{\sin\widehat{AOM}} = 2R$, so $R = \dfrac{AM}{2\sin\alpha}$.",
             [AM / sf, AM * sf / 2]),
            (r"Length of $AM$", AM, nen_d, [AM_, 2 - 2 * cf]),
            (r"Length of $A'M$", AM_, nen_d, [AM, 2 + 2 * cf]),
        ]
        dung, sai = [], []
        for ten, v, ly, vs in random.sample(DL, len(DL)):
            if not _xa_bien(v * 100):
                continue
            if len(dung) == 3:
                break
            dung.append((r"%s is approximately $%s$ (rounded to the nearest hundredth)" % (ten, _x1(v, 2)), ly + r" Hence the value is $\approx %s$." % _x1(v, 3)))
            for w in vs:
                if _x1(w, 2) != _x1(v, 2) and w > 0:
                    sai.append((r"%s is approximately $%s$ (rounded to the nearest hundredth)" % (ten, _x1(w, 2)),
                                ly + r" Hence the value is $\approx %s$." % _x1(v, 3)))
        if not dung or not sai:
            continue
        y4 = _phat_bieu(dung, sai)
        so += 1
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _lys = r"Supplementary angles: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha = %s$, $\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha = %s$." % (_L(s), _L(-c))
        _tf_them(y2, [(r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(s), _lys), (r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(-c), _lys)],
                 [(r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(-s), _lys), (r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(c), _lys)])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_nua_dtdv(g), 0, socot)
    return cau


# =====================================================================
# BIẾN THỂ _02 CHO 10 DẠNG MỚI CỦA BÀI 5 (30/09/2026)
# ---------------------------------------------------------------------
# Cô Lan: "_02 phải là cách hỏi khác đi, nhưng cùng về một đơn vị kiến
# thức". Mỗi hàm _02 dưới đây giữ nguyên ID (đơn vị kiến thức, mức độ) của
# _01 nhưng đặt câu hỏi theo hướng khác (hỏi ngược, cho góc không đặc biệt,
# chuyển sang tam giác...).
# =====================================================================

def L10_C3_B5_NB029_MC_H_02(socau, dang=1):
    r"""Hỏi NGƯỢC của _01: cho một giá trị, chọn giá trị lượng giác (của góc
    đặc biệt) BẰNG giá trị đó.

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB029_MC_H (_01: chon dang
    thuc dung/sai cua mot goc; _02: chon GTLG bang mot so cho truoc). Co Lan
    duyet lai.
    """
    CAP = [(h, d) for d in (0, 30, 45, 60, 90, 120, 135, 150, 180)
           for h in _HAM4 if _gtlg(h, d) is not None and _gtlg(h, d) != 0]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        h, d = random.choice(CAP)
        if (h, d) not in gt:
            gt.append((h, d))
    cau = ""
    for h, d in gt:
        v = _gtlg(h, d)
        khac = [(h2, d2) for h2, d2 in CAP if simplify(_gtlg(h2, d2) - v) != 0]
        # uu tien nhieu "de nham": gia tri doi, cung tri tuyet doi, cung ham
        khac.sort(key=lambda c: (simplify(abs(_gtlg(*c)) - abs(v)) != 0, c[0] != h,
                                 random.random()))
        nhieu, chon = [], []
        for h2, d2 in khac:
            t = r"$\%s %s$" % (h2, _goc(d2))
            if t not in nhieu:
                nhieu.append(t)
                chon.append((h2, d2))
            if len(nhieu) == 3:
                break
        dung = r"$\%s %s$" % (h, _goc(d))
        debai = r"Which of the following values is equal to $%s$?" % _L(v)
        giai = (r"From the table of trigonometric values of special angles: $\%s %s = %s$." % (h, _goc(d), _L(v))
                + "\\\\\n" + r"The other three values: " +
                ", ".join(r"$\%s %s = %s$" % (h2, _goc(d2), _L(_gtlg(h2, d2))) for h2, d2 in chon) + ".")
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_NB029_SA_J_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi NGƯỢC của _01: biết hoành độ (hoặc tung độ và phía
    của trục tung) của điểm $M$ trên nửa đường tròn đơn vị, tìm số đo góc
    $\widehat{xOM}$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB029_SA_B (_01: biet goc, tinh
    bieu thuc toa do; _02: biet toa do, tim goc). Dap so la so nguyen do.
    Co Lan duyet lai.
    """
    BO = [("x", Rational(1, 2), None, 60), ("x", Rational(-1, 2), None, 120),
          ("x", Integer(0), None, 90), ("x", Integer(-1), None, 180),
          ("y", Rational(1, 2), "right", 30), ("y", Rational(1, 2), "left", 150),
          ("y", Integer(1), None, 90)]
    ds = list(range(len(BO)))
    random.shuffle(ds)
    ds = (ds * (socau // len(ds) + 1))[:socau]
    cau = ""
    for i in ds:
        loai, v, phia, goc = BO[i]
        so = _so_thap_phan_gon(v)
        if loai == "x":
            cho = r"has x-coordinate equal to $%s$" % so
            ly = (r"For $M$ on the unit semicircle, $\cos\widehat{xOM} = x_M = %s$." % so
                  + "\\\\\n" + r"The angle from $0^{\circ}$ to $180^{\circ}$ whose cosine is $%s$ is $%s$." % (so, _goc(goc)))
        else:
            cho = (r"has y-coordinate equal to $%s$" % so) + (r" and lies on the %s side of the y-axis" % phia if phia else "")
            ly = (r"For $M$ on the unit semicircle, $\sin\widehat{xOM} = y_M = %s$." % so
                  + "\\\\\n" +
                  (r"There are two angles whose sine is $%s$, namely $30^{\circ}$ and $150^{\circ}$; $M$ lies on the %s side of the "
                   r"y-axis, so $\widehat{xOM}$ is %s, that is, $\widehat{xOM} = %s$."
                   % (so, phia, "acute" if phia == "right" else "obtuse", _goc(goc)) if phia else
                   r"The angle whose sine is $1$ is $90^{\circ}$."))
        debai = (r"In the coordinate plane $Oxy$, the point $M$ lies on the unit semicircle and %s. "
                 r"What is the measure of angle $\widehat{xOM}$ in degrees?" % cho)
        dap = str(goc)
        nhieu = _ba_nhieu(dap, [str(180 - goc), str(abs(90 - goc)), str(goc + 30)],
                          buoc=lambda t: str(goc + 15 * t))
        cau += MC_SA_answer_const(debai, dap, nhieu, ly + "\\\\\n" + r"Hence $\widehat{xOM} = %s$." % _goc(goc),
                                  0, 0, dang)
    return cau


def L10_C3_B5_TH030_MC_D_02(socau, dang=1):
    r"""Hỏi NGƯỢC của _01: biết $\sin\alpha\cos\alpha$, tính
    $\left(\sin\alpha \pm \cos\alpha\right)^{2}$ hoặc $\sin^{4}\alpha + \cos^{4}\alpha$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH030_MC_D (cung don vi: bien
    doi nho sin^2 + cos^2 = 1; _01 cho tong tinh tich, _02 cho tich tinh
    tong binh phuong). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        k = random.randrange(3)
        # sin^4 + cos^4 chi dung bo (3; 4; 5) de phan so khong qua cong kenh
        a, b, c = random.choice(BO_BA_PYTAGO[:3] if k < 2 else BO_BA_PYTAGO[:1])
        p = random.choice([1, -1]) * Rational(a * b, c * c)
        if (p, k) not in gt:
            gt.append((p, k))
    cau = ""
    for p, k in gt:
        if k == 0:
            hoi, P = r"\left(\sin\alpha + \cos\alpha\right)^{2}", 1 + 2 * p
            bd = r"\sin^{2}\alpha + \cos^{2}\alpha + 2\sin\alpha\cos\alpha = 1 + 2\sin\alpha\cos\alpha"
            ung = [1 - 2 * p, 2 * p, 1 + p]
            thay = r"1 + 2\cdot %s" % _ngoac(p)
        elif k == 1:
            hoi, P = r"\left(\sin\alpha - \cos\alpha\right)^{2}", 1 - 2 * p
            bd = r"\sin^{2}\alpha + \cos^{2}\alpha - 2\sin\alpha\cos\alpha = 1 - 2\sin\alpha\cos\alpha"
            ung = [1 + 2 * p, -2 * p, 1 - p]
            thay = r"1 - 2\cdot %s" % _ngoac(p)
        else:
            hoi, P = r"\sin^{4}\alpha + \cos^{4}\alpha", 1 - 2 * p ** 2
            bd = (r"\left(\sin^{2}\alpha + \cos^{2}\alpha\right)^{2} - 2\sin^{2}\alpha\cos^{2}\alpha = "
                  r"1 - 2\left(\sin\alpha\cos\alpha\right)^{2}")
            ung = [1 + 2 * p ** 2, 1 - p ** 2, 1 - 2 * p]
            thay = r"1 - 2\cdot\left(%s\right)^{2}" % _L(p)
        dung = _L(P)
        # (sin ± cos)^2 nằm trong [0; 2] (không bao giờ âm); sin^4 + cos^4 nằm trong [1/2; 1]
        thap, cao = (Rational(1, 2), Integer(1)) if k == 2 else (Integer(0), Integer(2))
        nhieu = _nhieu_trong_mien(P, ung, thap, cao, Rational(1, 100))
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ satisfying "
                 r"$\sin\alpha\cos\alpha = %s$. The value of $%s$ is" % (_L(p), hoi))
        giai = (r"We have $%s = %s$." % (hoi, bd) + "\\\\\n" +
                r"Substituting $\sin\alpha\cos\alpha = %s$ gives $%s = %s = %s$." % (_L(p), hoi, thay, dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_SA_N_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi NGƯỢC của _01: biết diện tích tam giác $AOM$ và
    $M$ nằm bên trái / phải trục tung, tìm $\cos\widehat{xOM}$ (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH030_SA_B (_01: cos -> dien
    tich; _02: dien tich -> cos). Dap so thap phan huu han, toi da 4 ki tu.
    Co Lan duyet lai.
    """
    BO = []
    for doi, ke, huyen in [(3, 4, 5), (4, 3, 5), (7, 24, 25), (24, 7, 25)]:
        for dau in (1, -1):
            cs = Rational(dau * ke, huyen)
            if _so_thap_phan_gon(cs):
                BO.append((doi, ke, huyen, dau))
    random.shuffle(BO)
    BO = (BO * (socau // len(BO) + 1))[:socau]
    cau = ""
    for doi, ke, huyen, dau in BO:
        sn, cs = Rational(doi, huyen), Rational(dau * ke, huyen)
        S = sn / 2
        dap = _so_thap_phan_gon(cs)
        phia = "left" if dau < 0 else "right"
        goc = math.degrees(math.acos(float(cs)))
        debai = (r"In the coordinate plane $Oxy$, given the point $A\left(1; 0\right)$ and a point $M$ on the unit "
                 r"semicircle, on the %s side of the y-axis, such that triangle $AOM$ has area $%s$. "
                 r"Find $\cos\widehat{xOM}$." % (phia, _so_thap_phan_gon(S)))
        giai = (r"$S_{\triangle AOM} = \dfrac{1}{2}\cdot OA\cdot y_M = \dfrac{1}{2}y_M$, so "
                r"$y_M = 2\cdot %s = %s$, that is, $\sin\widehat{xOM} = %s$."
                % (_so_thap_phan_gon(S), _so_thap_phan_gon(sn), _so_thap_phan_gon(sn)) + "\\\\\n" +
                r"$\cos^{2}\widehat{xOM} = 1 - \sin^{2}\widehat{xOM} = %s$." % _so_thap_phan_gon(cs ** 2)
                + "\\\\\n" +
                r"$M$ lies on the %s side of the y-axis, so $x_M %s 0$. Hence $\cos\widehat{xOM} = %s$."
                % (phia, "<" if dau < 0 else ">", dap))
        nhieu = _ba_nhieu(dap, [_so_thap_phan_gon(-cs) or "0", _so_thap_phan_gon(sn),
                                _so_thap_phan_gon(S)], buoc=lambda t: str(t))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_AOM(goc), 0, dang)
    return cau


# (mẫu có "a" là góc, giá trị, cách biến đổi) - góc a KHÔNG đặc biệt
_BT_GOC_LE = [
    (r"\sin^{2}{a} + \sin^{2}{p}", 1, r"\sin^{2}{a} + \cos^{2}{a} = 1"),
    (r"\cos^{2}{a} + \cos^{2}{p}", 1, r"\cos^{2}{a} + \sin^{2}{a} = 1"),
    (r"\tan{a}\cdot\tan{p}", 1, r"\tan{a}\cdot\cot{a} = 1"),
    (r"\cos{a} + \cos{b}", 0, r"\cos{a} - \cos{a} = 0"),
    (r"\sin{a} - \sin{b}", 0, r"\sin{a} - \sin{a} = 0"),
    (r"\sin^{2}{a} + \cos^{2}{b}", 1, r"\sin^{2}{a} + \cos^{2}{a} = 1"),
    (r"\tan{a} + \tan{b}", 0, r"\tan{a} - \tan{a} = 0"),
]


def L10_C3_B5_TH031_MC_C_02(socau, dang=1):
    r"""Tính biểu thức với các góc KHÔNG đặc biệt (không tra bảng được, phải
    dùng quan hệ hai góc phụ nhau, bù nhau), vd
    $P = \sin^{2}20^{\circ} + \sin^{2}70^{\circ} + 2\left(\cos 35^{\circ} + \cos 145^{\circ}\right)$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_C (_01: goc dac biet,
    tinh bang bang; _02: goc le, bat buoc dung quan he phu/bu). Co Lan duyet lai.
    """
    LE = [10, 15, 20, 25, 35, 40, 50, 55, 65, 70, 75, 80]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        i, j = random.sample(range(len(_BT_GOC_LE)), 2)
        a1, a2 = random.sample(LE, 2)
        k1, k2 = random.choice([1, 2, 3]), random.choice([1, 2, 3, -1, -2])
        P = k1 * _BT_GOC_LE[i][1] + k2 * _BT_GOC_LE[j][1]
        if P == 0 or (i, j, a1, a2) in [g[:4] for g in gt]:
            continue
        gt.append((i, j, a1, a2, k1, k2))
    cau = ""
    for i, j, a1, a2, k1, k2 in gt:
        def dien(mau, a):
            return (mau.replace("{a}", " " + _goc(a)).replace("{p}", " " + _goc(90 - a))
                    .replace("{b}", " " + _goc(180 - a)))
        def hang(k, e, dau_dau):
            so = "" if abs(k) == 1 else "%d" % abs(k)
            than = (r"%s\left(%s\right)" % (so, e)) if so else e
            if not so and not dau_dau and k < 0 and (" + " in e or " - " in e):
                than = r"\left(%s\right)" % e
            return (("-" if k < 0 else "") if dau_dau else (" - " if k < 0 else " + ")) + than
        E1, E2 = dien(_BT_GOC_LE[i][0], a1), dien(_BT_GOC_LE[j][0], a2)
        bt = hang(k1, E1, True) + hang(k2, E2, False)
        P = k1 * _BT_GOC_LE[i][1] + k2 * _BT_GOC_LE[j][1]
        ly = []
        for (mau, v, bd), a in ((_BT_GOC_LE[i], a1), (_BT_GOC_LE[j], a2)):
            if "{p}" in mau:
                qh = (r"$%s$ and $%s$ are complementary, so $\sin %s = \cos %s$, $\cos %s = \sin %s$, $\tan %s = \cot %s$"
                      % (_goc(a), _goc(90 - a), _goc(90 - a), _goc(a), _goc(90 - a), _goc(a),
                         _goc(90 - a), _goc(a)))
            else:
                qh = (r"$%s$ and $%s$ are supplementary, so $\sin %s = \sin %s$, $\cos %s = -\cos %s$, $\tan %s = -\tan %s$"
                      % (_goc(a), _goc(180 - a), _goc(180 - a), _goc(a), _goc(180 - a), _goc(a),
                         _goc(180 - a), _goc(a)))
            ly.append(qh + r"; hence $%s = %s$." % (dien(mau, a), dien(bd, a)))
        tinh = ("%d\\cdot %s" % (k1, _ngoac(Integer(_BT_GOC_LE[i][1])))) if k1 != 1 else str(_BT_GOC_LE[i][1])
        tinh += " %s %s" % ("-" if k2 < 0 else "+",
                            ("%d\\cdot %s" % (abs(k2), _ngoac(Integer(_BT_GOC_LE[j][1]))))
                            if abs(k2) != 1 else str(_BT_GOC_LE[j][1]))
        dung = "$P = %d$" % P
        nhieu = _ba_nhieu(dung, ["$P = %d$" % x for x in (P + 1, P - 1, -P, 0, 2 * P)],
                          buoc=lambda t: "$P = %d$" % (P + t + 1))
        debai = r"Find the value of the expression $P = %s$." % bt
        giai = ("\\\\\n".join(ly) + "\\\\\n" + r"Hence $P = %s = %d$." % (tinh, P))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


# alpha + beta = 180 độ trong TAM GIÁC: X là một góc, YZ là tổng hai góc còn lại
_BT_TAM_GIAC = [
    (r"\sin X\cos\left(YZ\right) + \cos X\sin\left(YZ\right)", 0,
     r"\sin X\cdot\left(-\cos X\right) + \cos X\sin X = 0"),
    (r"\cos X\cos\left(YZ\right) - \sin X\sin\left(YZ\right)", -1,
     r"-\cos^{2}X - \sin^{2}X = -1"),
    (r"\sin^{2}X + \cos^{2}\left(YZ\right)", 1, r"\sin^{2}X + \cos^{2}X = 1"),
    (r"\cos X + \cos\left(YZ\right)", 0, r"\cos X - \cos X = 0"),
    (r"\sin X - \sin\left(YZ\right)", 0, r"\sin X - \sin X = 0"),
    (r"\sin X\sin\left(YZ\right) - \cos X\cos\left(YZ\right)", 1, r"\sin^{2}X + \cos^{2}X = 1"),
]


def L10_C3_B5_TH031_SA_C_02(socau, dang=2):
    r"""Trả lời ngắn - như _01 nhưng đặt trong TAM GIÁC: hai góc bù nhau là
    $\widehat{A}$ và $B + C$ (không cho $\alpha + \beta = 180^{\circ}$ sẵn, học
    sinh phải tự nhận ra).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_SA_C (_01: cho san
    alpha + beta; _02: tu suy ra tu tong ba goc tam giac). Dap so nguyen.
    Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        X, Y, Z = random.sample("ABC", 3)
        i = random.choice([t for t, e in enumerate(_BT_TAM_GIAC) if e[1] != 0])
        k1 = random.choice([1, 2, 3])
        if random.random() < 0.6:
            j = random.choice([t for t in range(len(_BT_TAM_GIAC)) if t != i])
            k2 = random.choice([1, 2, 3]) * random.choice([1, -1])
        else:
            j, k2 = None, 0
        P = k1 * _BT_TAM_GIAC[i][1] + (k2 * _BT_TAM_GIAC[j][1] if j is not None else 0)
        if P == 0 or (X, i, k1, j, k2) in [g[:1] + g[3:] for g in gt]:
            continue
        gt.append((X, Y, Z, i, k1, j, k2))
    cau = ""
    for X, Y, Z, i, k1, j, k2 in gt:
        yz = "%s + %s" % tuple(sorted([Y, Z]))
        def dien(t):
            return t.replace("YZ", yz).replace("X", X)
        def hang(k, e, dau_dau):
            so = "" if abs(k) == 1 else "%d" % abs(k)
            than = (r"%s\left(%s\right)" % (so, e)) if so else e
            if not so and not dau_dau and k < 0 and (" + " in e or " - " in e):
                than = r"\left(%s\right)" % e
            return (("-" if k < 0 else "") if dau_dau else (" - " if k < 0 else " + ")) + than
        E = _BT_TAM_GIAC
        bt = hang(k1, dien(E[i][0]), True) + (hang(k2, dien(E[j][0]), False) if j is not None else "")
        P = k1 * E[i][1] + (k2 * E[j][1] if j is not None else 0)
        dong = [r"$%s = %s$." % (dien(E[i][0]), dien(E[i][2]))]
        tinh = ("%d\\cdot %s" % (k1, _ngoac(Integer(E[i][1])))) if k1 != 1 else "%d" % E[i][1]
        if j is not None:
            dong.append(r"$%s = %s$." % (dien(E[j][0]), dien(E[j][2])))
            tinh += " %s %d\\cdot %s" % ("-" if k2 < 0 else "+", abs(k2), _ngoac(Integer(E[j][1])))
        debai = r"Given triangle $ABC$. Find the value of the expression $P = %s$." % bt
        giai = (r"Since $\widehat{A} + \widehat{B} + \widehat{C} = 180^{\circ}$, we have $%s = 180^{\circ} - %s$: "
                r"the two angles are supplementary, so $\sin\left(%s\right) = \sin %s$, $\cos\left(%s\right) = -\cos %s$."
                % (yz, X, yz, X, yz, X) + "\\\\\n" + "\\\\\n".join(dong) + "\\\\\n" +
                r"Hence $P = %s = %d$." % (tinh, P))
        dap = str(P)
        ds = _ba_nhieu(dap, [str(-P), str(P + 1), "0", str(P - 1)], buoc=lambda t: str(P + t + 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_D_02(socau, dang=1):
    r"""Biết GIÁ TRỊ GẦN ĐÚNG của một giá trị lượng giác của góc nhọn KHÔNG đặc
    biệt (vd $\sin 50^{\circ} \approx 0,77$), suy ra giá trị lượng giác của góc
    phụ hoặc góc bù với nó.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_D (_01: dang thuc giua
    hai goc dac biet phu/bu; _02: dung quan he phu/bu de suy ra gia tri cua
    goc le). Co Lan duyet lai.
    """
    LE = [20, 25, 35, 40, 50, 55, 65, 70]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (random.choice(LE), random.choice(["sin", "cos", "tan"]), random.choice(["phu", "bu"]))
        if v not in gt:
            gt.append(v)
    F = {"sin": math.sin, "cos": math.cos, "tan": math.tan,
         "cot": lambda x: 1 / math.tan(x)}
    def so(x):
        return ("%.2f" % x).replace(".", DAU_THAP_PHAN)
    cau = ""
    for a, h, qh in gt:
        v = F[h](math.radians(a))
        w = F[_DOI_HAM[h]](math.radians(a))
        if qh == "phu":
            b, g, ket = 90 - a, _DOI_HAM[h], v
            ly = (r"The angles $%s$ and $%s$ are complementary, so $\%s %s = \%s %s$."
                  % (_goc(a), _goc(b), g, _goc(b), h, _goc(a)))
        else:
            b, g = 180 - a, h
            ket = v if h == "sin" else -v
            ly = (r"The angles $%s$ and $%s$ are supplementary, so $\%s %s = %s\%s %s$."
                  % (_goc(a), _goc(b), g, _goc(b), "" if h == "sin" else "-", h, _goc(a)))
        dung = so(ket)
        nhieu = _ba_nhieu(dung, [so(-ket), so(w), so(-w)], buoc=lambda t: so(ket + 0.1 * t))
        debai = (r"Given $\%s %s \approx %s$. The value of $\%s %s$ is approximately"
                 % (h, _goc(a), so(v), g, _goc(b)))
        giai = ly + "\\\\\n" + r"Hence $\%s %s \approx %s$." % (g, _goc(b), dung)
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


# (biểu thức, kết quả đúng, [kết quả sai]) - alpha là góc nhọn
_RUT_GON = [
    (r"\sin\left(180^{\circ} - \alpha\right) + \sin\alpha", r"2\sin\alpha",
     [r"0", r"2\cos\alpha", r"-2\sin\alpha"],
     r"\sin\alpha + \sin\alpha = 2\sin\alpha"),
    (r"\cos\left(180^{\circ} - \alpha\right) + \cos\alpha", r"0",
     [r"2\cos\alpha", r"-2\cos\alpha", r"2\sin\alpha"],
     r"-\cos\alpha + \cos\alpha = 0"),
    (r"\cos\left(180^{\circ} - \alpha\right) - \cos\alpha", r"-2\cos\alpha",
     [r"0", r"2\cos\alpha", r"-2\sin\alpha"],
     r"-\cos\alpha - \cos\alpha = -2\cos\alpha"),
    (r"\sin\left(90^{\circ} - \alpha\right) + \cos\left(180^{\circ} - \alpha\right)", r"0",
     [r"2\cos\alpha", r"-2\cos\alpha", r"\sin\alpha - \cos\alpha"],
     r"\cos\alpha - \cos\alpha = 0"),
    (r"\cos\left(90^{\circ} - \alpha\right) + \sin\left(180^{\circ} - \alpha\right)", r"2\sin\alpha",
     [r"0", r"2\cos\alpha", r"\sin\alpha + \cos\alpha"],
     r"\sin\alpha + \sin\alpha = 2\sin\alpha"),
    (r"\tan\left(180^{\circ} - \alpha\right) + \cot\left(90^{\circ} - \alpha\right)", r"0",
     [r"2\tan\alpha", r"-2\tan\alpha", r"\tan\alpha + \cot\alpha"],
     r"-\tan\alpha + \tan\alpha = 0"),
    (r"\cos\left(90^{\circ} - \alpha\right)\sin\left(180^{\circ} - \alpha\right) + "
     r"\sin\left(90^{\circ} - \alpha\right)\cos\alpha", r"1",
     [r"0", r"2", r"\sin^{2}\alpha - \cos^{2}\alpha"],
     r"\sin\alpha\cdot\sin\alpha + \cos\alpha\cdot\cos\alpha = \sin^{2}\alpha + \cos^{2}\alpha = 1"),
]


def L10_C3_B5_TH031_MC_E_02(socau, dang=1):
    r"""RÚT GỌN biểu thức bằng công thức tổng quát của góc phụ, góc bù
    (vd $P = \sin\left(180^{\circ} - \alpha\right) + \cos\left(90^{\circ} - \alpha\right)$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_E (_01: chon cong thuc
    dung/sai; _02: dung cong thuc de rut gon). Co Lan duyet lai.
    """
    ds = list(range(len(_RUT_GON)))
    random.shuffle(ds)
    ds = (ds * (socau // len(ds) + 1))[:socau]
    cau = ""
    for i in ds:
        bt, dung, sai, bd = _RUT_GON[i]
        debai = r"Given an acute angle $\alpha$. Simplifying the expression $P = %s$ gives" % bt
        giai = (r"Using the relations between supplementary and complementary angles: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha$, "
                r"$\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha$, $\tan\left(180^{\circ} - \alpha\right) = "
                r"-\tan\alpha$; $\sin\left(90^{\circ} - \alpha\right) = \cos\alpha$, $\cos\left(90^{\circ} - "
                r"\alpha\right) = \sin\alpha$, $\cot\left(90^{\circ} - \alpha\right) = \tan\alpha$." + "\\\\\n" +
                r"Hence $P = %s$." % bd)
        cau += MC_SA_answer_text(debai, "$P = %s$" % dung, ["$P = %s$" % s for s in sai], giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_F_02(socau, dang=1):
    r"""Tam giác vuông cho một giá trị lượng giác (phân số) của một góc nhọn,
    tính giá trị lượng giác của góc nhọn CÒN LẠI (hai góc phụ nhau).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_F (_01: biet so do goc,
    chon khang dinh dung/sai; _02: biet sin/cos mot goc, tinh cua goc kia).
    Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (tuple(random.sample("ABC", 3)), random.choice(BO_BA_PYTAGO[:4]),
             random.choice(["sin", "cos"]), random.choice(["sin", "cos", "tan"]))
        if v not in gt:
            gt.append(v)
    cau = ""
    for (X, Y, Z), (p, q, r), cho, hoi in gt:
        sY = Rational(p, r) if cho == "sin" else Rational(q, r)
        cY = Rational(q, r) if cho == "sin" else Rational(p, r)
        gia = {"sin": cY, "cos": sY, "tan": cY / sY}
        dap = gia[hoi]
        dung = _L(dap)
        nhieu = _ba_nhieu(dung, [_L(x) for x in (sY if hoi == "sin" else cY, sY / cY, -dap, cY / sY, 1 / dap)],
                          buoc=lambda t: _L(dap + Rational(t, 5)))
        cho_gt = sY if cho == "sin" else cY
        con = cY if cho == "sin" else sY
        debai = (r"Triangle $ABC$ is right-angled at $%s$ with $\%s %s = %s$. The value of $\%s %s$ is"
                 % (X, cho, Y, _L(cho_gt), hoi, Z))
        buoc = []
        if hoi == "tan" or (hoi == "sin" and cho == "sin") or (hoi == "cos" and cho == "cos"):
            buoc.append(r"Since $\widehat{%s}$ is acute, $\%s %s = \sqrt{1 - %s} = %s$."
                        % (Y, "cos" if cho == "sin" else "sin", Y, _L(cho_gt ** 2), _L(con)))
        qh = {"sin": r"\sin %s = \cos %s" % (Z, Y), "cos": r"\cos %s = \sin %s" % (Z, Y),
              "tan": r"\tan %s = \cot %s = \dfrac{\cos %s}{\sin %s}" % (Z, Y, Y, Y)}[hoi]
        giai = (r"The two acute angles $\widehat{%s}$ and $\widehat{%s}$ of a right triangle are complementary." % (Y, Z)
                + ("\\\\\n" + buoc[0] if buoc else "") + "\\\\\n" +
                r"Hence $%s = %s$." % (qh, dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_TF_F_02(socau, socot=1):
    r"""Đúng/Sai - tam giác cho SỐ ĐO một góc đặc biệt: giá trị lượng giác của
    góc đó và của tổng hai góc còn lại (hai góc bù nhau), tính bằng số.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TF_F (_01: chi biet goc tu/nhon,
    xet dau va dang thuc; _02: cho so do goc, tinh gia tri cu the). Co Lan
    duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        X, Y, Z = random.sample("ABC", 3)
        x = random.choice(_GOC_DB)
        s, c, t = _gtlg("sin", x), _gtlg("cos", x), _gtlg("tan", x)
        yz = "%s + %s" % tuple(sorted([Y, Z]))
        debai = (r"Given triangle $ABC$ with $\widehat{%s} = %s$. Determine whether each of the following statements is true or false:"
                 % (X, _goc(x)))
        # a) NB - bảng giá trị lượng giác
        ly_a = r"Table of trigonometric values: $\sin %s = %s$, $\cos %s = %s$, $\tan %s = %s$." % (_goc(x), _L(s), _goc(x), _L(c), _goc(x), _L(t))
        y1 = _tf_gop(_tf_ct(r"$\cos %s = %s$" % (X, "%s"), c, ly_a, [(-c, "Sign error"), (s, "Confused $\\sin$ with $\\cos$")]),
                     _tf_ct(r"$\sin %s = %s$" % (X, "%s"), s, ly_a, [(abs(c), "Confused $\\sin$ with $\\cos$"), (-s, "Sign error")]),
                     _tf_ct(r"$\tan %s = %s$" % (X, "%s"), t, ly_a, [(-t, "Sign error"), (1 / t, "Confused $\\tan$ with $\\cot$")]))
        ly = (r"$%s = 180^{\circ} - %s = %s$" % (yz, _goc(x), _goc(180 - x)))
        # b) TH - một bước: góc bù có sin bằng nhau
        ly_b = r"%s, so $\sin\left(%s\right) = \sin %s = %s$." % (ly, yz, _goc(x), _L(s))
        sai_b = [(r"$\sin\left(%s\right) = %s$" % (yz, _L(-s)), ly_b), (r"$\sin\left(%s\right) = %s$" % (yz, _L(c)), "Confused with complementary angles. " + ly_b)]
        if 90 - x > 0:
            sai_b.append((r"$\widehat{%s} + \widehat{%s} = %s$" % (tuple(sorted([Y, Z])) + (_goc(90 - x),)), ly_b))
        sai_b.append((r"$\widehat{%s} + \widehat{%s} = %s$" % (tuple(sorted([Y, Z])) + (_goc(x),)), ly_b))
        y2 = _phat_bieu(
            [(r"$\sin\left(%s\right) = %s$" % (yz, _L(s)), ly_b), (r"$\widehat{%s} + \widehat{%s} = %s$" % (tuple(sorted([Y, Z])) + (_goc(180 - x),)), ly_b)],
            sai_b)
        # c) VD - côsin, tang của góc bù
        ly_c = r"%s, so $\cos\left(%s\right) = -\cos %s = %s$, $\tan\left(%s\right) = -\tan %s = %s$." % (ly, yz, _goc(x), _L(-c), yz, _goc(x), _L(-t))
        y3 = _tf_gop(_tf_ct(r"$\cos\left(%s\right) = %s$" % (yz, "%s"), -c, ly_c, [(c, "Forgot to change the sign"), (-s, "Confused $\\sin$ with $\\cos$")]),
                     _tf_ct(r"$\tan\left(%s\right) = %s$" % (yz, "%s"), -t, ly_c, [(t, "Forgot to change the sign"), (-1 / t, "Confused $\\tan$ with $\\cot$")]))
        # d) VDC - biểu thức tổ hợp (2 biểu thức hệ số ngẫu nhiên)
        dung, sai = [], []
        bo_hs = set()
        while len(bo_hs) < 2:
            bo_hs.add(tuple(random.choice([1, 2, 3, -1, -2]) for _ in range(3)))
        for u, v, w in bo_hs:
            hs = lambda h, first: ("" if h == 1 else ("-" if h == -1 else str(h))) if first else \
                (" + " if h == 1 else (" - " if h == -1 else (" + %d" % h if h > 0 else " - %d" % -h)))
            bt = (hs(u, True) + r"\sin %s" % X + hs(v, False) + r"\cos\left(%s\right)" % yz + hs(w, False) + r"\tan\left(%s\right)" % yz)
            P = simplify(u * s - v * c - w * t)
            ly_d = (r"%s, so $\cos\left(%s\right) = -\cos %s$, $\tan\left(%s\right) = -\tan %s$; substituting $\sin %s = %s$, $\cos %s = %s$, "
                    r"$\tan %s = %s$ gives $%s$." % (ly, yz, X, yz, X, X, _L(s), X, _L(c), X, _L(t), _tri(P)))
            dung.append(("$" + bt + " = %s$" % _tri(P), ly_d))
            for Q, ghi in ((u * s + v * c - w * t, "Forgot to change the sign of $\\cos$"), (u * s - v * c + w * t, "Forgot to change the sign of $\\tan$"),
                           (u * s + v * c + w * t, "Forgot to change the signs of both")):
                if simplify(Q - P) != 0:
                    sai.append(("$" + bt + " = %s$" % _tri(Q), ghi + ". " + ly_d))
        y4 = _phat_bieu(dung, sai)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y2, [(r"$\sin\left(%s\right) = \sin %s$" % (yz, X), ly_b)],
                 [(r"$\sin\left(%s\right) = -\sin %s$" % (yz, X), ly_b), (r"$\sin\left(%s\right) = \cos %s$" % (yz, X), ly_b)])
        _lyd = r"%s, so $\cos\left(%s\right) = -\cos %s$, $\tan\left(%s\right) = -\tan %s$." % (ly, yz, X, yz, X)
        _tf_them(y4, [(r"$\sin %s + \cos\left(%s\right) = \sin %s - \cos %s$" % (X, yz, X, X), _lyd),
                      (r"$\tan %s + \tan\left(%s\right) = 0$" % (X, yz), _lyd)],
                 [(r"$\sin %s + \cos\left(%s\right) = \sin %s + \cos %s$" % (X, yz, X, X), _lyd),
                  (r"$\tan %s - \tan\left(%s\right) = 0$" % (X, yz), _lyd)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF



# =====================================================================
# BÀI 6 - "BÀI TẬP TRẮC NGHIỆM" CỦA CÔ LAN (30/09/2026)
# ---------------------------------------------------------------------
# Theo docs/27_DANG_BIEN_THE_VA_NHAP_BAI.md: chữ cái A, B... là các dạng
# khác nhau cùng một đơn vị kiến thức; _01, _02... cùng dạng nhưng CÁCH
# HỎI khác nhau. Mỗi dạng mới có _01 (theo câu của giáo án) và _02 (hỏi
# theo cách khác).
# =====================================================================

_GOC_TAM_GIAC = [30, 45, 60, 90, 120, 135, 150]


def _lt(x):
    """Làm tròn đến hàng đơn vị theo quy tắc SGK (0,5 làm tròn lên) - _lt() của
    Python làm tròn về số chẵn nên KHÔNG dùng."""
    return int(math.floor(x + 0.5))


def _x1(x, n=1):
    """Số làm tròn đúng n chữ số thập phân, GIỮ chữ số 0 cuối (vd 21,0), dấu phẩy."""
    return ("%%.%df" % n % (math.floor(x * 10 ** n + 0.5) / 10 ** n)).replace(".", DAU_THAP_PHAN)


def _xa_bien(x, n=0):
    """True nếu x không nằm sát ranh giới làm tròn (tránh kết quả lệch khi tính trung gian)."""
    f = x * 10 ** n - math.floor(x * 10 ** n)
    return abs(f - 0.5) > 0.06


def _sin_d(d):
    return math.sin(math.radians(d))


def _cos_d(d):
    return math.cos(math.radians(d))


def _heron_nguyen(gioi_han=30):
    """Tam giác cạnh nguyên, diện tích nguyên (không đòi r nguyên), không vuông."""
    ra = []
    for a in range(3, gioi_han + 1):
        for b in range(a, gioi_han + 1):
            for c in range(b, min(a + b, gioi_han + 1)):
                if (a + b + c) % 2 or a * a + b * b == c * c:
                    continue
                p = (a + b + c) // 2
                t = p * (p - a) * (p - b) * (p - c)
                s = math.isqrt(t)
                if s * s == t and s > 0:
                    ra.append((a, b, c, s, p))
    return ra


HERON_NGUYEN = _heron_nguyen()


# ------------------------- TH032: định lí côsin -------------------------

def L10_C3_B6_TH032_MC_B_03(socau, dang=1):
    r"""Biết ba cạnh, hỏi SỐ ĐO một góc (không hỏi côsin như _01, _02).

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH032_MC_B, theo cau 5 Phan I
    bai tap trac nghiem Bai 6 ("AB = 5, BC = 7, CA = 8, goc A bang"). Co Lan
    duyet lai.
    """
    BO = [(60, b, c) for b, c in CAP_COSIN[60]] + [(120, b, c) for b, c in CAP_COSIN[120]] + \
         [(90, p, q) for p, q, _ in BO_BA_PYTAGO]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = random.choice(BO)
        if v not in gt:
            gt.append(v)
    cau = ""
    for A, b, c in gt:
        a2 = b * b + c * c - 2 * b * c * _gtlg("cos", A)
        a = int(math.isqrt(int(a2)))
        cosA = Rational(b * b + c * c - a * a, 2 * b * c)
        debai = (r"Triangle $ABC$ has $AB = %d$, $BC = %d$, $CA = %d$. The measure of angle $\widehat{A}$ is"
                 % (c, a, b))
        giai = (r"By the corollary of the law of cosines: $\cos A = \dfrac{AB^{2} + AC^{2} - BC^{2}}{2\cdot AB\cdot AC}"
                r" = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$." % (c, b, a, c, b, _L(cosA))
                + "\\\\\n" + r"Hence $\widehat{A} = %s$." % _goc(A))
        dung = _goc(A)
        nhieu = _ba_nhieu(dung, [_goc(x) for x in (180 - A, 90, 30, 45, 150, 60)])
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


_CT_COSIN_DUNG = [r"a^{2} = b^{2} + c^{2} - 2bc\cos A", r"\cos A = \dfrac{b^{2} + c^{2} - a^{2}}{2bc}",
                  r"b^{2} = a^{2} + c^{2} - 2ac\cos B", r"\cos B = \dfrac{a^{2} + c^{2} - b^{2}}{2ac}",
                  r"c^{2} = a^{2} + b^{2} - 2ab\cos C", r"\cos C = \dfrac{a^{2} + b^{2} - c^{2}}{2ab}"]
_CT_COSIN_SAI = [(r"a^{2} = b^{2} + c^{2} + 2bc\cos A", r"there must be a minus sign before $2bc\cos A$"),
                 (r"\cos A = \dfrac{b^{2} + c^{2} - a^{2}}{bc}", r"the denominator must be $2bc$"),
                 (r"\cos A = \dfrac{a^{2} + b^{2} - c^{2}}{2bc}", r"the side opposite angle $A$ is $a$, so $a^{2}$ must be subtracted"),
                 (r"b^{2} = a^{2} + c^{2} - 2ac\cos A", r"the angle included between sides $a$ and $c$ is angle $B$"),
                 (r"\cos C = \dfrac{a^{2} + b^{2} + c^{2}}{2ab}", r"$c^{2}$ must be subtracted"),
                 (r"\cos B = \dfrac{b^{2} + c^{2} - a^{2}}{2ac}", r"the correct form is $\dfrac{a^{2} + c^{2} - b^{2}}{2ac}$"),
                 (r"c^{2} = a^{2} + b^{2} - ab\cos C", r"the factor $2$ is missing")]


def L10_C3_B6_NB032_MC_A_01(socau, dang=1):
    r"""Chọn hệ thức ĐÚNG (hoặc SAI) của định lí côsin và hệ quả.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 3 Phan I bai tap trac nghiem
    Bai 6 ("he thuc nao dung: cos A = ..."). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        hoi_dung = random.random() < 0.5
        if hoi_dung:
            dung = "$%s$" % random.choice(_CT_COSIN_DUNG)
            ba = random.sample(_CT_COSIN_SAI, 3)
            nhieu = ["$%s$" % x[0] for x in ba]
            giai = (r"%s is a true relation (law of cosines and its corollary). The other relations are false: " % dung
                    + "; ".join(r"$%s$: %s" % x for x in ba) + ".")
        else:
            sai, ly = random.choice(_CT_COSIN_SAI)
            dung = "$%s$" % sai
            nhieu = ["$%s$" % x for x in random.sample(_CT_COSIN_DUNG, 3)]
            giai = r"Relation %s is false because %s. The other three relations are the law of cosines and its corollary." % (dung, ly)
        debai = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$. Which of the following relations is \textbf{%s}?"
                 % ("true" if hoi_dung else "false"))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_NB032_MC_A_02(socau, dang=1):
    r"""Cho SỐ ĐO ba cạnh; chọn biểu thức đã THAY SỐ đúng để tính côsin của một
    góc (nhận ra cạnh đối diện và hai cạnh kề).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH032_MC_E (_01: he thuc bang chu;
    _02: he thuc da thay so). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        x, y, z = random.sample(range(3, 13), 3)
        if x + y <= z or x + z <= y or y + z <= x:
            continue
        dinh = random.choice("ABC")
        if (x, y, z, dinh) not in gt:
            gt.append((x, y, z, dinh))
    cau = ""
    for AB, BC, CA, dinh in gt:
        canh = {"A": (AB, CA, BC), "B": (AB, BC, CA), "C": (BC, CA, AB)}   # (ke1, ke2, doi)
        k1, k2, d = canh[dinh]
        def bt(u, v, w, dau="-", he="2\\cdot "):
            return r"\dfrac{%d^{2} + %d^{2} %s %d^{2}}{%s%d\cdot %d}" % (u, v, dau, w, he, u, v)
        dung = "$%s$" % bt(k1, k2, d)
        khac = [x for x in "ABC" if x != dinh]
        u1, v1, w1 = canh[khac[0]]
        nhieu = ["$%s$" % bt(u1, v1, w1), "$%s$" % bt(k1, k2, d, "+"), "$%s$" % bt(k1, k2, d, "-", "")]
        debai = (r"Given triangle $ABC$ with $AB = %d$, $BC = %d$, $CA = %d$. Which of the following expressions gives "
                 r"the value of $\cos %s$?" % (AB, BC, CA, dinh))
        v = Rational(k1 * k1 + k2 * k2 - d * d, 2 * k1 * k2)
        giai = (r"The two sides adjacent to angle $%s$ have lengths $%d$ and $%d$, and the opposite side has length $%d$. By the corollary "
                r"of the law of cosines: $\cos %s = %s = %s$." % (dinh, k1, k2, d, dinh, bt(k1, k2, d), _L(v)))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


# ------------------------- TH033: định lí sin -------------------------

def L10_C3_B6_TH033_MC_A_03(socau, dang=1):
    r"""Định lí sin khi cạnh đã biết và cạnh cần tìm KHÔNG đối diện hai góc đã
    cho: phải tính góc thứ ba trước (vd $A = 105^\circ$, $B = 45^\circ$, $AC = 10$, tính $AB$).

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH033_MC_A, theo cau 7 Phan I
    bai tap trac nghiem Bai 6. Co Lan duyet lai.
    """
    CAP = [(B, C) for B in (30, 45, 60, 120, 135) for C in (30, 45, 60, 90, 120, 135)
           if B + C < 180 and 180 - B - C not in (B, C)]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        B, C = random.choice(CAP)
        b = random.randint(4, 12)
        if (B, C, b) not in gt:
            gt.append((B, C, b))
    cau = ""
    for B, C, b in gt:
        A = 180 - B - C
        sB, sC = _gtlg("sin", B), _gtlg("sin", C)
        c = simplify(b * sC / sB)
        dung = _tri(c)
        nhieu = _ba_nhieu(dung, [_tri(simplify(x)) for x in (b * sB / sC, b * sC, 2 * c, b * sB, c / 2,
                                                             Integer(b), c * sqrt(2), c * sqrt(3))],
                          buoc=lambda t: _tri(c * (t + 2)))
        debai = (r"Triangle $ABC$ has $\widehat{A} = %s$, $\widehat{B} = %s$, $AC = %d$. Find the length of side $AB$."
                 % (_goc(A), _goc(B), b))
        giai = (r"$\widehat{C} = 180^{\circ} - \left(%s + %s\right) = %s$." % (_goc(A), _goc(B), _goc(C))
                + "\\\\\n" +
                r"By the law of sines: $\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B}$, so $AB = \dfrac{AC\cdot\sin C}{\sin B}"
                r" = \dfrac{%d\cdot\sin %s}{\sin %s} = %s$." % (b, _goc(C), _goc(B), dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


_CT_SIN_DUNG = [r"\dfrac{a}{\sin A} = 2R", r"\sin A = \dfrac{a}{2R}", r"b = 2R\sin B",
                r"\sin C = \dfrac{c\sin A}{a}", r"\dfrac{b}{\sin B} = \dfrac{c}{\sin C}",
                r"a\sin B = b\sin A"]
_CT_SIN_SAI = [(r"b\sin B = 2R", r"the correct form is $\dfrac{b}{\sin B} = 2R$"),
               (r"a = R\sin A", r"the correct form is $a = 2R\sin A$"),
               (r"\sin A = \dfrac{a}{R}", r"the correct form is $\sin A = \dfrac{a}{2R}$"),
               (r"a\sin A = b\sin B", r"the correct form is $a\sin B = b\sin A$"),
               (r"\dfrac{a}{\sin B} = \dfrac{b}{\sin A}", r"each side must be divided by the sine of the angle OPPOSITE it"),
               (r"c = 2R\cos C", r"the correct form is $c = 2R\sin C$")]


def L10_C3_B6_NB033_MC_A_01(socau, dang=1):
    r"""Chọn khẳng định ĐÚNG (hoặc SAI) về định lí sin.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 2 Phan I bai tap trac nghiem
    Bai 6 ("khang dinh nao sai: b sin B = 2R..."). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        hoi_dung = random.random() < 0.5
        if hoi_dung:
            dung = "$%s$" % random.choice(_CT_SIN_DUNG)
            ba = random.sample(_CT_SIN_SAI, 3)
            nhieu = ["$%s$" % x[0] for x in ba]
            giai = (r"Law of sines: $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$, which gives %s. "
                    % dung + r"The remaining statements are false: " + "; ".join(r"$%s$: %s" % x for x in ba) + ".")
        else:
            sai, ly = random.choice(_CT_SIN_SAI)
            dung = "$%s$" % sai
            nhieu = ["$%s$" % x for x in random.sample(_CT_SIN_DUNG, 3)]
            giai = (r"Law of sines: $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$. "
                    r"Statement %s is false because %s." % (dung, ly))
        debai = (r"In any triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$ and $R$ the radius of the circumscribed "
                 r"circle, which of the following statements is \textbf{%s}?" % ("true" if hoi_dung else "false"))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_MC_C_01(socau, dang=1):
    r"""Định lí sin cho TỈ SỐ hai cạnh: biết hai góc, tính $\dfrac{BC}{CA}$
    (bằng $\dfrac{\sin A}{\sin B}$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH033_MC_C (_01: chon he thuc
    dung/sai; _02: dung he thuc de tinh ti so hai canh). Co Lan duyet lai.
    """
    CAP = [(A, B) for A in _GOC_TAM_GIAC for B in _GOC_TAM_GIAC if A != B and A + B < 180]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = random.choice(CAP)
        if v not in gt:
            gt.append(v)
    cau = ""
    for A, B in gt:
        sA, sB = _gtlg("sin", A), _gtlg("sin", B)
        k = simplify(sA / sB)
        dung = _tri(k)
        ung = [sB / sA, Rational(A, B)]
        cA, cB = _gtlg("cos", A), _gtlg("cos", B)
        if cA != 0 and cB != 0:
            ung.append(cA / cB)
        nhieu = _ba_nhieu(dung, [_tri(x) for x in ung] + ["1", "2"], buoc=lambda t: _tri(k + t))
        debai = (r"Triangle $ABC$ has $\widehat{A} = %s$, $\widehat{B} = %s$. The ratio $\dfrac{BC}{CA}$ equals"
                 % (_goc(A), _goc(B)))
        giai = (r"By the law of sines, $\dfrac{BC}{\sin A} = \dfrac{CA}{\sin B}$, so $\dfrac{BC}{CA} = "
                r"\dfrac{\sin A}{\sin B} = \dfrac{\sin %s}{\sin %s} = \dfrac{%s}{%s} = %s$."
                % (_goc(A), _goc(B), _L(sA), _L(sB), dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


# ------------------------- TH034: diện tích -------------------------

def L10_C3_B6_TH034_MC_D_01(socau, dang=1):
    r"""Diện tích tam giác biết hai cạnh và góc xen giữa (số đo đặc biệt).

    CLAUDE THEM 30/09/2026 - dang moi (ban trac nghiem cua TH034_SA_A), theo
    cau 8 Phan I bai tap trac nghiem Bai 6 ("AB = 3, AC = 6, A = 60, tinh
    dien tich"). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (random.choice(_GOC_TAM_GIAC), random.randint(2, 12), random.randint(2, 12))
        if v[1] != v[2] and v not in gt:
            gt.append(v)
    cau = ""
    for A, b, c in gt:
        sA, cA = _gtlg("sin", A), _gtlg("cos", A)
        S = simplify(b * c * sA / 2)
        dung = "S = %s" % _tri(S)
        ung = [b * c * sA, Rational(b * c, 2), b * c * sA / 4]
        if cA != 0:
            ung.append(abs(b * c * cA / 2))
        nhieu = _ba_nhieu(dung, ["S = %s" % _tri(simplify(x)) for x in ung], buoc=lambda t: "S = %s" % _tri(S + t))
        debai = (r"Triangle $ABC$ has $AB = %d$, $AC = %d$, $\widehat{BAC} = %s$. Find the area $S$ of triangle "
                 r"$ABC$." % (c, b, _goc(A)))
        giai = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s = %s$."
                % (c, b, _goc(A), _tri(S)))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_D_02(socau, dang=1):
    r"""Diện tích tam giác biết hai cạnh và CÔSIN của góc xen giữa: phải tính
    sin trước ($\sin A = \sqrt{1 - \cos^{2}A}$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH034_MC_D (_01: cho so do goc;
    _02: cho cos goc). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = (random.choice(_COS_PHAN_SO), random.randint(2, 12), random.randint(2, 12))
        if v[1] != v[2] and v not in gt:
            gt.append(v)
    cau = ""
    for cA, b, c in gt:
        sA = simplify(_sin_tu_cos(cA))
        S = simplify(b * c * sA / 2)
        dung = _tri(S)
        nhieu = _ba_nhieu(dung, [_tri(simplify(x)) for x in (abs(b * c * cA / 2), b * c * sA, b * c * (1 - abs(cA)) / 2)],
                          buoc=lambda t: _tri(S + t))
        debai = (r"Triangle $ABC$ has $AB = %d$, $AC = %d$ and $\cos A = %s$. The area of triangle $ABC$ equals"
                 % (c, b, _L(cA)))
        giai = (r"Since $0^{\circ} < A < 180^{\circ}$, we have $\sin A > 0$, so $\sin A = \sqrt{1 - \cos^{2}A} = "
                r"\sqrt{1 - %s} = %s$." % (_L(cA ** 2), _L(sA)) + "\\\\\n" +
                r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$."
                % (c, b, _L(sA), dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_E_01(socau, dang=1):
    r"""Biết ba cạnh: Heron rồi bán kính đường tròn NỘI tiếp $r = \dfrac{S}{p}$.

    CLAUDE THEM 30/09/2026 - dang moi (ban trac nghiem cua TH034_SA_B), theo
    cau 10 Phan I bai tap trac nghiem Bai 6 ("a = 21, b = 17, c = 10, tinh r").
    Co Lan duyet lai.
    """
    ds = random.sample(HERON_NGUYEN, min(socau, len(HERON_NGUYEN)))
    cau = ""
    for x, y, z, S, p in ds:
        a, b, c = random.sample([x, y, z], 3)
        r = Rational(S, p)
        dung = "r = %s" % _L(r)
        nhieu = _ba_nhieu(dung, ["r = %s" % _L(v) for v in (Integer(S), Rational(S, 2 * p), Rational(2 * S, p),
                                                           Rational(p, 2))],
                          buoc=lambda t: "r = %s" % _L(r + t))
        debai = (r"Given triangle $ABC$ with $a = %d$, $b = %d$, $c = %d$. Find the inradius $r$ of triangle "
                 r"$ABC$." % (a, b, c))
        giai = (r"The semiperimeter is $p = \dfrac{%d + %d + %d}{2} = %d$." % (a, b, c, p) + "\\\\\n" +
                r"Heron's formula: $S = \sqrt{%d\left(%d - %d\right)\left(%d - %d\right)\left(%d - %d\right)} = %d$."
                % (p, p, a, p, b, p, c, S) + "\\\\\n" +
                r"Hence $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %s$." % (S, p, _L(r)))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_E_02(socau, dang=1):
    r"""Biết ba cạnh: Heron rồi bán kính đường tròn NGOẠI tiếp
    $R = \dfrac{abc}{4S}$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH034_MC_E (_01: hoi r = S/p;
    _02: hoi R = abc/4S). Co Lan duyet lai.
    """
    ds = random.sample(HERON_NGUYEN, min(socau, len(HERON_NGUYEN)))
    cau = ""
    for x, y, z, S, p in ds:
        a, b, c = random.sample([x, y, z], 3)
        R = Rational(a * b * c, 4 * S)
        dung = "R = %s" % _L(R)
        nhieu = _ba_nhieu(dung, ["R = %s" % _L(v) for v in (Rational(a * b * c, 2 * S), Rational(a * b * c, S),
                                                           Rational(S, p), 2 * R)],
                          buoc=lambda t: "R = %s" % _L(R + t))
        debai = (r"Given triangle $ABC$ with $a = %d$, $b = %d$, $c = %d$. Find the circumradius $R$ of triangle "
                 r"$ABC$." % (a, b, c))
        giai = (r"The semiperimeter is $p = %d$; by Heron's formula, $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
                % (p, p, p - a, p - b, p - c, S) + "\\\\\n" +
                r"From $S = \dfrac{abc}{4R}$ we get $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$."
                % (a, b, c, S, _L(R)))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_F_01(socau, dang=1):
    r"""Đường cao $h_a$ khi biết hai cạnh và góc xen giữa: định lí côsin tính
    $BC$, rồi diện tích, rồi $h_a = \dfrac{2S}{BC}$.

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 11 Phan I bai tap trac nghiem
    Bai 6 ("AB = 3, AC = 6, A = 60, tinh h_a"). Co Lan duyet lai.
    """
    BO = [(60, b, c) for b, c in CAP_COSIN[60]] + [(120, b, c) for b, c in CAP_COSIN[120]]
    ds = random.sample(BO, min(socau, len(BO)))
    cau = ""
    for A, b, c in ds:
        sA, cA = _gtlg("sin", A), _gtlg("cos", A)
        a = int(math.isqrt(int(b * b + c * c - 2 * b * c * cA)))
        S = simplify(b * c * sA / 2)
        ha = simplify(2 * S / a)
        dung = "h_a = %s" % _tri(ha)
        nhieu = _ba_nhieu(dung, ["h_a = %s" % _tri(simplify(v)) for v in (S / a, 2 * S / b, 2 * S / c, 2 * S)],
                          buoc=lambda t: "h_a = %s" % _tri(ha + t))
        debai = (r"Triangle $ABC$ has $AB = %d$, $AC = %d$, $\widehat{BAC} = %s$. Find the length of the altitude $h_a$ "
                 r"from $A$ of the triangle." % (c, b, _goc(A)))
        giai = (r"Law of cosines: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cos A = %d + %d - 2\cdot %d\cdot %d"
                r"\cdot %s = %d$, so $BC = %d$." % (c * c, b * b, c, b, _ngoac(cA), a * a, a) + "\\\\\n" +
                r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = %s$." % _tri(S) + "\\\\\n" +
                r"Since $S = \dfrac{1}{2}BC\cdot h_a$, we have $h_a = \dfrac{2S}{BC} = %s$." % _tri(ha))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_F_02(socau, dang=1):
    r"""Đường cao khi biết BA CẠNH: Heron rồi $h = \dfrac{2S}{\text{cạnh đáy}}$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH034_MC_F (_01: hai canh va goc
    xen giua; _02: ba canh). Co Lan duyet lai.
    """
    ds = random.sample(HERON_NGUYEN, min(socau, len(HERON_NGUYEN)))
    cau = ""
    for x, y, z, S, p in ds:
        a, b, c = random.sample([x, y, z], 3)
        ha = Rational(2 * S, a)
        dung = "h_a = %s" % _L(ha)
        nhieu = _ba_nhieu(dung, ["h_a = %s" % _L(v) for v in (Rational(S, a), Rational(2 * S, b),
                                                             Rational(2 * S, c), Rational(S, p))],
                          buoc=lambda t: "h_a = %s" % _L(ha + t))
        debai = (r"Triangle $ABC$ has $BC = %d$, $CA = %d$, $AB = %d$. The length of the altitude $h_a$ from $A$ equals"
                 % (a, b, c))
        giai = (r"The semiperimeter is $p = %d$; by Heron's formula, $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
                % (p, p, p - a, p - b, p - c, S) + "\\\\\n" +
                r"Since $S = \dfrac{1}{2}BC\cdot h_a$, we have $h_a = \dfrac{2S}{BC} = \dfrac{2\cdot %d}{%d} = %s$."
                % (S, a, _L(ha)))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau



# ------------------------- VD036: bài toán thực tế -------------------------

def _hinh_ve_tinh(al, be):
    """Tam giác hai trạm A (trái), B (phải) và vệ tinh C, góc nâng al tại A, be tại B."""
    ta, tb = math.tan(math.radians(al)), math.tan(math.radians(be))
    x = 4 * tb / (ta + tb)
    y = x * ta
    k = 2.2 / y if y > 2.2 else 1
    return (
        "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
        "\\coordinate (A) at (0,0);\n\\coordinate (B) at (%.2f,0);\n\\coordinate (C) at (%.2f,%.2f);\n"
        % (4 * k, x * k, y * k)
        + "\\draw[thick] (A) -- (B) -- (C) -- cycle;\n"
        "\\fill (C) circle (1.5pt) node[above] {$C$ (satellite)};\n"
        "\\node[below left] at (A) {$A$};\n\\node[below right] at (B) {$B$};\n"
        "\\node at ($(A)+(%.1f:0.7)$) {$%d^{\\circ}$};\n" % (al / 2, al)
        + "\\node at ($(B)+(%.1f:0.7)$) {$%d^{\\circ}$};\n" % (180 - be / 2, be)
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_MC_B_02(socau, dang=1):
    r"""Định lí sin trong thực tế - hai trạm quan sát cùng nhìn một vệ tinh với
    hai góc nâng; tính khoảng cách từ vệ tinh tới một trạm (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD036_MC_B (_01: qua dam lay, tinh
    canh doi dien goc; _02: ve tinh, tinh canh ke). Theo cau 12 Phan I bai tap
    trac nghiem Bai 6 (goc nang 55 va 80 do, AB = 127 km). Co Lan duyet lai.
    """
    TRAM = [("Can Tho", "Ho Chi Minh City"), ("Ha Noi", "Hai Phong"), ("Hue", "Da Nang")]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        al, be = random.randint(40, 85), random.randint(40, 85)
        d = random.randint(80, 200)
        C = 180 - al - be
        if C < 15 or al == be:
            continue
        AC = d * _sin_d(be) / _sin_d(C)
        BC = d * _sin_d(al) / _sin_d(C)
        hoi_A = random.random() < 0.5
        dap = _lt(AC if hoi_A else BC)
        ung = [_lt(BC if hoi_A else AC), _lt(d * _sin_d(be)), _lt(d * _sin_d(C) / _sin_d(be)), dap + 3]
        if len(set([dap] + ung[:3])) < 4 or not _xa_bien(AC if hoi_A else BC):
            continue
        gt.append((al, be, d, hoi_A, dap, ung, random.choice(TRAM)))
    cau = ""
    for al, be, d, hoi_A, dap, ung, (ta, tb) in gt:
        C = 180 - al - be
        dung = "$%d$ km" % dap
        nhieu = _ba_nhieu(dung, ["$%d$ km" % x for x in ung], buoc=lambda t: "$%d$ km" % (dap + 5 * t))
        tram = ta if hoi_A else tb
        debai = (r"A satellite $C$ flies above two observation stations $A$ (in %s) and $B$ (in %s). When the satellite is "
                 r"between the two stations, its angles of elevation observed at the same time are $%d^{\circ}$ at $A$ and $%d^{\circ}$ at $B$. "
                 r"The distance between the two stations is $%d$ km. How far is the satellite from the station in %s (round "
                 r"to the nearest whole number)?" % (ta, tb, al, be, d, tram))
        canh, goc_doi = ("AC", "B") if hoi_A else ("BC", "A")
        giai = (r"$\widehat{C} = 180^{\circ} - \left(%d^{\circ} + %d^{\circ}\right) = %d^{\circ}$." % (al, be, C)
                + "\\\\\n" +
                r"Law of sines in triangle $ABC$: $%s = \dfrac{AB\cdot\sin %s}{\sin C} = \dfrac{%d\cdot\sin %d^{\circ}}"
                r"{\sin %d^{\circ}} \approx %d$ (km)." % (canh, goc_doi, d, be if hoi_A else al, C, dap))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, _hinh_ve_tinh(al, be), 0, dang)
    return cau


def _hinh_hai_tau(g):
    return (
        "\\begin{tikzpicture}[scale=0.7,font=\\footnotesize]\n"
        "\\coordinate (A) at (0,0);\n\\coordinate (B) at (%.1f:3);\n\\coordinate (C) at (%.1f:4.2);\n"
        % (90 - g / 2 + g, 90 - g / 2)
        + "\\draw[thick] (A) -- (B) (A) -- (C);\n\\draw[dashed] (B) -- (C);\n"
        "\\foreach \\p/\\v in {A/below,B/above left,C/above right} \\fill (\\p) circle (1.5pt) node[\\v] {$\\p$};\n"
        "\\draw (%.1f:0.6) arc (%.1f:%.1f:0.6);\n" % (90 - g / 2, 90 - g / 2, 90 + g / 2)
        + "\\node at (90:1) {$%d^{\\circ}$};\n" % g
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - hai tàu cùng xuất phát từ một bến, đi thẳng theo hai
    hướng hợp với nhau một góc; tính khoảng cách giữa hai tàu sau $t$ giờ
    (định lí côsin, có hình).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 2 Phan III bai tap trac nghiem
    Bai 6 (goc 75 do, 8 va 12 hai li/gio, 2,5 gio). Dap so lam tron hang phan
    muoi, toi da 4 ki tu. Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        g = random.choice([35, 40, 50, 55, 65, 70, 75, 80, 100, 110])
        v1, v2 = random.sample(range(6, 16), 2)
        t = random.choice([1.5, 2, 2.5, 3])
        b, c = v1 * t, v2 * t
        d = math.sqrt(b * b + c * c - 2 * b * c * _cos_d(g))
        dap = _xx(d, 1)
        if not _xa_bien(d, 1) or len(dap) > 4 or (g, v1, v2, t) in [x[:4] for x in gt]:
            continue
        gt.append((g, v1, v2, t, dap))
    cau = ""
    for g, v1, v2, t, dap in gt:
        b, c = v1 * t, v2 * t
        d2 = b * b + c * c - 2 * b * c * _cos_d(g)
        debai = (r"Two fishing boats leave harbor $A$ at the same time and sail at constant speed in straight lines toward two different sea areas, along "
                 r"two directions forming an angle of $%d^{\circ}$. The first boat travels at $%d$ nautical miles per hour and the "
                 r"second boat at $%d$ nautical miles per hour. After $%s$ hours, what is the distance between the two boats, in "
                 r"nautical miles (round the result to the nearest tenth)?" % (g, v1, v2, _xx(t, 1)))
        giai = (r"After $%s$ hours the first boat is at $B$ and the second boat is at $C$, where $AB = %s\cdot %d = %s$, $AC = %s\cdot %d = %s$ "
                r"(nautical miles)." % (_xx(t, 1), _xx(t, 1), v1, _xx(b, 1), _xx(t, 1), v2, _xx(c, 1)) + "\\\\\n" +
                r"Law of cosines: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos %d^{\circ} \approx %s$." % (g, _xx(d2, 2))
                + "\\\\\n" + r"Hence $BC \approx %s$ nautical miles." % dap)
        ds = _ba_nhieu(dap, [_xx(b + c, 1), _xx(math.sqrt(b * b + c * c), 1), _xx(abs(c - b), 1)],
                       buoc=lambda k: _xx(float(dap.replace(",", ".")) + k, 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, _hinh_hai_tau(g), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_C_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi NGƯỢC của _01: hai tàu cùng xuất phát, biết khoảng
    cách cần đạt, hỏi SAU BAO LÂU (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD036_SA_C (_01: biet thoi gian
    tinh khoang cach; _02: biet khoang cach tinh thoi gian). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        g = random.choice([40, 50, 60, 70, 80, 100, 110, 120])
        v1, v2 = random.sample(range(6, 16), 2)
        k = math.sqrt(v1 * v1 + v2 * v2 - 2 * v1 * v2 * _cos_d(g))   # khoang cach sau 1 gio
        t0 = random.choice([1.5, 2, 2.5, 3, 3.5, 4])
        D = _lt(k * t0)
        t = D / k
        dap = _xx(t, 1)
        if not _xa_bien(t, 1) or D < 5 or len(dap) > 4 or (g, v1, v2, D) in [x[:4] for x in gt]:
            continue
        gt.append((g, v1, v2, D, dap))
    cau = ""
    for g, v1, v2, D, dap in gt:
        k2 = v1 * v1 + v2 * v2 - 2 * v1 * v2 * _cos_d(g)
        debai = (r"Two ships leave port $A$ at the same time and sail straight along two directions forming an angle of $%d^{\circ}$, "
                 r"at speeds of $%d$ nautical miles per hour and $%d$ nautical miles per hour, respectively. After how many hours will the two ships be "
                 r"$%d$ nautical miles apart (round the result to the nearest tenth)?" % (g, v1, v2, D))
        giai = (r"After $t$ hours: $AB = %dt$, $AC = %dt$. Law of cosines:" % (v1, v2) + "\\\\\n" +
                r"$BC^{2} = \left(%dt\right)^{2} + \left(%dt\right)^{2} - 2\cdot %dt\cdot %dt\cdot\cos %d^{\circ}"
                r" \approx %s\,t^{2}$." % (v1, v2, v1, v2, g, _xx(k2, 2)) + "\\\\\n" +
                r"$BC = %d$, so $t^{2} \approx \dfrac{%d^{2}}{%s}$, $t \approx %s$ (hours)." % (D, D, _xx(k2, 2), dap))
        ds = _ba_nhieu(dap, [_xx(D / (v1 + v2), 1), _xx(D / abs(v2 - v1), 1), _xx(D / max(v1, v2), 1)],
                       buoc=lambda j: _xx(float(dap.replace(",", ".")) + 0.5 * j, 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, _hinh_hai_tau(g), 0, dang)
    return cau


def _hinh_hai_dang(al, be):
    """Bờ biển AB, hải đăng C; góc al tại A, góc ngoài be tại B."""
    ta, tb = math.tan(math.radians(al)), math.tan(math.radians(be))
    AB = 2.2
    x = AB * tb / (tb - ta)          # hoanh do chan duong vuong goc H
    y = x * ta
    k = 2.6 / y if y > 2.6 else 1
    return (
        "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
        "\\coordinate (A) at (0,0);\n\\coordinate (B) at (%.2f,0);\n\\coordinate (C) at (%.2f,%.2f);\n"
        "\\coordinate (H) at (%.2f,0);\n" % (AB * k, x * k, y * k, x * k)
        + "\\draw (-0.4,0) -- (%.2f,0);\n" % (x * k + 0.6)
        + "\\draw[thick] (A) -- (C) -- (B);\n\\draw[dashed] (C) -- (H);\n"
        "\\fill (C) circle (1.5pt) node[above] {$C$};\n"
        "\\node[below] at (A) {$A$};\n\\node[below] at (B) {$B$};\n\\node[below] at (H) {$H$};\n"
        "\\node at ($(A)+(%.1f:0.6)$) {$%d^{\\circ}$};\n" % (al / 2, al)
        + "\\node at ($(B)+(%.1f:0.55)$) {$%d^{\\circ}$};\n" % (be / 2, be)
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - khoảng cách từ ngọn hải đăng tới bờ biển: đi từ $A$
    đến $B$ dọc bờ, biết hai góc nhìn (góc tại $B$ là góc ngoài), dùng định lí
    sin rồi tam giác vuông (có hình).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 3 Phan III bai tap trac nghiem
    Bai 6 (45 do, 75 do, AB = 30 m). Dap so lam tron hang don vi. Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        al = random.choice([30, 35, 40, 45, 50])
        be = al + random.choice([20, 25, 30, 35])
        d = random.choice(range(20, 81, 5))
        if be >= 88 or (al, be, d) in [x[:3] for x in gt]:
            continue
        h = d * _sin_d(al) * _sin_d(be) / _sin_d(be - al)
        if not _xa_bien(h):
            continue
        gt.append((al, be, d, _lt(h)))
    cau = ""
    for al, be, d, dap in gt:
        BC = d * _sin_d(al) / _sin_d(be - al)
        debai = (r"A person walks along the coast from position $A$ to position $B$ and observes a lighthouse $C$. The angles "
                 r"between the lines of sight from positions $A$ and $B$ to the lighthouse and the observer's path "
                 r"are $%d^{\circ}$ and $%d^{\circ}$ (as shown in the figure). The distance between positions $A$ and $B$ is "
                 r"$%d$ m. How many meters is the lighthouse from the coast (round the result to the nearest whole number)?"
                 % (al, be, d))
        giai = (r"In triangle $ABC$: $\widehat{ABC} = 180^{\circ} - %d^{\circ} = %d^{\circ}$, "
                r"$\widehat{ACB} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$."
                % (be, 180 - be, al, 180 - be, be - al) + "\\\\\n" +
                r"Law of sines: $BC = \dfrac{AB\cdot\sin A}{\sin C} = \dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} "
                r"\approx %s$ (m)." % (d, al, be - al, _xx(BC, 2)) + "\\\\\n" +
                r"Draw $CH \perp AB$. In triangle $BCH$, right-angled at $H$: $CH = BC\cdot\sin %d^{\circ} \approx %d$ (m)."
                % (be, dap))
        ds = _ba_nhieu(str(dap), [str(_lt(BC)), str(_lt(d * _sin_d(al))), str(_lt(d * math.tan(math.radians(al))))],
                       buoc=lambda t: str(dap + t))
        cau += MC_SA_answer_const(debai, str(dap), ds, giai, _hinh_hai_dang(al, be), 0, dang)
    return cau


def _hinh_cay(h0, d):
    k = 5.0 / d
    return (
        "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
        "\\coordinate (H) at (0,0);\n\\coordinate (A) at (0,%.2f);\n\\coordinate (B) at (5,0);\n"
        "\\coordinate (C) at (5,3.2);\n" % max(0.5, h0 * k)
        + "\\draw (-0.3,0) -- (5.6,0);\n\\draw[thick] (H) -- (A) -- (C) -- (B);\n\\draw (A) -- (B);\n"
        "\\draw (0,0.25) -- (0.25,0.25) -- (0.25,0);\n"
        "\\node[left] at (A) {$A$};\n\\node[below] at (H) {$H$};\n\\node[below] at (B) {$B$};\n"
        "\\node[above] at (C) {$C$};\n\\node[below] at (2.5,0) {$%d$ m};\n\\node[left] at (0,%.2f) {$%s$ m};\n"
        % (d, max(0.5, h0 * k) / 2, _xx(h0, 1))
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_SA_D_02(socau, dang=2):
    r"""Trả lời ngắn - chiều cao của cây: từ vị trí $A$ (cao $AH$ so với mặt
    đất, cách gốc cây $HB$) nhìn gốc và ngọn cây dưới góc $\widehat{BAC}$ (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD036_SA_D (_01: hai dang - hai
    goc nhin tu hai diem; _02: mot diem quan sat co do cao, biet goc giua hai
    tia nhin). Theo cau 4 Phan III bai tap trac nghiem Bai 6 (AH = 4, HB = 20,
    goc BAC = 45). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        h0 = random.choice([1.5, 2, 3, 4, 5])
        d = random.choice(range(10, 31, 2))
        th = random.choice([30, 35, 40, 45, 50])
        ABC = math.degrees(math.atan(d / h0))
        ACB = 180 - th - ABC
        if ACB < 20 or (h0, d, th) in [x[:3] for x in gt]:
            continue
        AB = math.hypot(h0, d)
        BC = AB * _sin_d(th) / _sin_d(ACB)
        if not _xa_bien(BC):
            continue
        gt.append((h0, d, th, _lt(BC)))
    cau = ""
    for h0, d, th, dap in gt:
        AB = math.hypot(h0, d)
        ABC = math.degrees(math.atan(d / h0))
        ACB = 180 - th - ABC
        debai = (r"From position $A$, a person observes a tree $BC$ ($B$ is the base of the tree) as shown in the figure. Given $AH = %s$ m, "
                 r"$HB = %d$ m, $\widehat{BAC} = %d^{\circ}$. Find the height of the tree (in meters, rounded to the nearest "
                 r"whole number)." % (_xx(h0, 1), d, th))
        giai = (r"$AB = \sqrt{AH^{2} + HB^{2}} = \sqrt{%s + %d} \approx %s$ (m); $\tan\widehat{HAB} = \dfrac{HB}{HA} = %s$ "
                r"so $\widehat{HAB} \approx %s^{\circ}$." % (_xx(h0 * h0, 2), d * d, _xx(AB, 2), _xx(d / h0, 2), _xx(ABC, 2))
                + "\\\\\n" +
                r"Since $AH \parallel BC$, $\widehat{ABC} = \widehat{HAB} \approx %s^{\circ}$, hence "
                r"$\widehat{ACB} \approx 180^{\circ} - %d^{\circ} - %s^{\circ} = %s^{\circ}$." % (_xx(ABC, 2), th, _xx(ABC, 2), _xx(ACB, 2))
                + "\\\\\n" +
                r"Law of sines: $BC = \dfrac{AB\cdot\sin %d^{\circ}}{\sin\widehat{ACB}} \approx %d$ (m)." % (th, dap))
        ds = _ba_nhieu(str(dap), [str(_lt(d * math.tan(math.radians(th)))), str(_lt(AB)), str(dap + 2)],
                       buoc=lambda t: str(dap + t + 2))
        cau += MC_SA_answer_const(debai, str(dap), ds, giai, _hinh_cay(h0, d), 0, dang)
    return cau


def _hinh_ang_ten():
    return (
        "\\begin{tikzpicture}[scale=0.8,font=\\footnotesize,line join=round]\n"
        "\\draw (-0.3,0) -- (6.3,0);\n"
        "\\draw[thick] (0,0) rectangle (1.2,1.5);\n\\draw[thick] (4.5,0) rectangle (6,3.2);\n"
        "\\coordinate (A) at (1.2,1.5);\n\\coordinate (C) at (4.5,3.2);\n\\coordinate (B) at (4.5,4.6);\n"
        "\\coordinate (D) at (4.5,1.5);\n\\coordinate (H) at (4.5,0);\n"
        "\\draw[very thick] (C) -- (B);\n\\draw (A) -- (B) (A) -- (C);\n\\draw[dashed] (A) -- (D);\n"
        "\\node[left] at (A) {$A$};\n\\node[right] at (C) {$C$};\n\\node[right] at (B) {$B$};\n"
        "\\node[right] at (D) {$D$};\n\\node[below] at (H) {$H$};\n"
        "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_SA_D_03(socau, dang=2):
    r"""Trả lời ngắn - chiều cao toà nhà có cột ăng-ten trên nóc: biết chiều
    cao cột, độ cao điểm quan sát và hai góc nâng tới đỉnh, chân cột (có hình).

    CLAUDE THEM 30/09/2026 - bien the 03 cua VD036_SA_D (hoi chieu cao toa nha
    qua dinh li sin roi tam giac vuong). Theo cau 5 Phan III bai tap trac
    nghiem Bai 6 (cot 5 m, A cao 7 m, 50 va 40 do). Co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        L = random.randint(3, 10)
        h0 = random.randint(5, 15)
        be = random.choice([30, 35, 40, 45])
        al = be + random.choice([5, 10, 15])
        if (L, h0, al, be) in [x[:4] for x in gt]:
            continue
        AC = L * _cos_d(al) / _sin_d(al - be)
        CH = h0 + AC * _sin_d(be)
        if not _xa_bien(CH):
            continue
        gt.append((L, h0, al, be, _lt(CH)))
    cau = ""
    for L, h0, al, be, dap in gt:
        AC = L * _cos_d(al) / _sin_d(al - be)
        CD = AC * _sin_d(be)
        debai = (r"On the roof of a building there is an antenna mast $BC$ of height $%d$ m ($C$ is the foot of the mast). From an observation point $A$ "
                 r"at a height of $%d$ m above the ground, the top $B$ and the foot $C$ of the mast are seen at angles of $%d^{\circ}$ "
                 r"and $%d^{\circ}$ to the horizontal. Find the height $CH$ of the building (in meters, rounded to the nearest "
                 r"whole number)." % (L, h0, al, be))
        giai = (r"$\widehat{BAC} = %d^{\circ} - %d^{\circ} = %d^{\circ}$; since triangle $ABD$ is right-angled at $D$, "
                r"$\widehat{ABC} = 90^{\circ} - %d^{\circ} = %d^{\circ}$." % (al, be, al - be, al, 90 - al) + "\\\\\n" +
                r"Law of sines in triangle $ABC$: $AC = \dfrac{BC\cdot\sin\widehat{ABC}}{\sin\widehat{BAC}} = "
                r"\dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$ (m)." % (L, 90 - al, al - be, _xx(AC, 2))
                + "\\\\\n" +
                r"In triangle $ADC$, right-angled at $D$: $CD = AC\cdot\sin %d^{\circ} \approx %s$ (m). Hence $CH = CD + DH \approx "
                r"%s + %d \approx %d$ (m)." % (be, _xx(CD, 2), _xx(CD, 2), h0, dap))
        ds = _ba_nhieu(str(dap), [str(_lt(CD)), str(_lt(CD + h0 + L)), str(dap - 1)],
                       buoc=lambda t: str(dap + t + 1))
        cau += MC_SA_answer_const(debai, str(dap), ds, giai, _hinh_ang_ten(), 0, dang)
    return cau


def _hai_ban(phi, m, n, psi, k):
    """Hình học bài An - Bình. Trả về PD, APD, BPD, BD (độ, số thực) hoặc None."""
    PD = math.sqrt(m * m + n * n - 2 * m * n * _cos_d(psi))
    APD = math.degrees(math.acos((m * m + PD * PD - n * n) / (2 * m * PD)))
    BPD = phi - APD
    if BPD < 5:
        return None
    BD = math.sqrt(k * k + PD * PD - 2 * k * PD * _cos_d(BPD))
    return PD, APD, BPD, BD


def _hinh_hai_ban(phi, m, n, k, PD, BPD):
    s = 8.0 / max(k, m, PD)
    A = (m * s * _cos_d(phi), m * s * _sin_d(phi))
    D = (PD * s * _cos_d(BPD), PD * s * _sin_d(BPD))
    return (
        "\\begin{tikzpicture}[scale=0.7,font=\\footnotesize,line join=round]\n"
        "\\coordinate (P) at (0,0);\n\\coordinate (B) at (%.2f,0);\n\\coordinate (A) at (%.2f,%.2f);\n"
        "\\coordinate (D) at (%.2f,%.2f);\n" % (k * s, A[0], A[1], D[0], D[1])
        + "\\draw[thick] (P) -- (A) -- (D) -- (B) -- cycle;\n"
        "\\foreach \\p/\\v in {P/left,B/below right,A/above,D/right} \\fill (\\p) circle (1.5pt) node[\\v] {$\\p$};\n"
        "\\node[above left] at ($(P)!0.5!(A)$) {$%d$ km};\n\\node[above right] at ($(A)!0.5!(D)$) {$%d$ km};\n"
        "\\node[below] at ($(P)!0.5!(B)$) {$%d$ km};\n\\node at (%.1f:1.1) {$%d^{\\circ}$};\n"
        % (m, n, k, phi / 2, phi)
        + "\\end{tikzpicture}"
    )


def _bo_hai_ban(socau, dieu_kien):
    gt = []
    lan = 0
    while len(gt) < socau and lan < 3000:
        lan += 1
        phi = random.choice([35, 40, 45, 50])
        m, n, k = random.randint(5, 10), random.randint(2, 5), random.randint(5, 10)
        psi = random.choice([95, 100, 105, 110, 115, 120])
        kq = _hai_ban(phi, m, n, psi, k)
        if kq is None or (phi, m, n, psi, k) in [x[:5] for x in gt] or not dieu_kien(phi, m, n, psi, k, kq):
            continue
        gt.append((phi, m, n, psi, k, kq))
    return gt


def L10_C3_B6_VD036_SA_X_01(socau, dang=2):
    r"""Trả lời ngắn - hai bạn đi theo hai hướng tới cùng một đích: định lí
    côsin HAI LẦN (tính đường chéo, góc, rồi quãng đường còn lại) (có hình).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 6 Phan III bai tap trac nghiem
    Bai 6 (An va Binh, goc 40 do, PAD = 100 do). Tinh khong lam tron trung gian.
    Dap so lam tron hang phan muoi, toi da 4 ki tu. Co Lan duyet lai.
    """
    gt = _bo_hai_ban(socau, lambda *a: len(_xx(a[-1][3], 1)) <= 4 and a[-1][3] > 1 and _xa_bien(a[-1][3], 1))
    cau = ""
    for phi, m, n, psi, k, (PD, APD, BPD, BD) in gt:
        dap = _xx(BD, 1)
        debai = (r"Two friends, An and Binh, start from the same point $P$ and walk in two different directions forming an angle of "
                 r"$%d^{\circ}$ to reach the destination, point $D$. An walks $%d$ km and stops for lunch at $A$, then walks another $%d$ km "
                 r"to $D$, where $\widehat{PAD} = %d^{\circ}$. Binh walks $%d$ km and stops for lunch at $B$ (as shown in the figure). "
                 r"How many more km must Binh walk to reach the destination (round to the nearest tenth)?" % (phi, m, n, psi, k))
        giai = (r"Triangle $PAD$: $PD = \sqrt{%d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %d^{\circ}} \approx %s$ (km)."
                % (m, n, m, n, psi, _xx(PD, 3)) + "\\\\\n" +
                r"Since $\cos\widehat{APD} = \dfrac{PA^{2} + PD^{2} - AD^{2}}{2\cdot PA\cdot PD}$, we get $\widehat{APD} \approx %s^{\circ}$."
                % _xx(APD, 2) + "\\\\\n" +
                r"$\widehat{BPD} = %d^{\circ} - \widehat{APD} \approx %s^{\circ}$." % (phi, _xx(BPD, 2)) + "\\\\\n" +
                r"Triangle $PBD$: $BD = \sqrt{PB^{2} + PD^{2} - 2\cdot PB\cdot PD\cdot\cos\widehat{BPD}} \approx %s$ (km)."
                % dap)
        ds = _ba_nhieu(dap, [_xx(abs(PD - k), 1), _xx(PD, 1), _xx(m + n - k, 1)],
                       buoc=lambda t: _xx(BD + 0.5 * t, 1))
        cau += MC_SA_answer_const(debai + "\n\n" + r"\begin{center}" + "\n" +
                                  _hinh_hai_ban(phi, m, n, k, PD, BPD) + "\n" + r"\end{center}",
                                  dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_X_02(socau, dang=2):
    r"""Trả lời ngắn - cùng hình vẽ của _01 nhưng hỏi DIỆN TÍCH tứ giác $PADB$
    (định lí côsin, tính góc, rồi hai công thức diện tích) (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD036_SA_E (_01: hoi quang duong
    con lai; _02: hoi dien tich khu vuc gioi han boi hai duong di). Co Lan
    duyet lai.
    """
    gt = _bo_hai_ban(socau, lambda phi, m, n, psi, k, kq:
                     len(_xx(0.5 * m * n * _sin_d(psi) + 0.5 * k * kq[0] * _sin_d(kq[2]), 1)) <= 4)
    cau = ""
    for phi, m, n, psi, k, (PD, APD, BPD, BD) in gt:
        S1 = 0.5 * m * n * _sin_d(psi)
        S2 = 0.5 * k * PD * _sin_d(BPD)
        dap = _xx(S1 + S2, 1)
        debai = (r"Two friends, An and Binh, start from the same point $P$ in two directions forming an angle of $%d^{\circ}$ to "
                 r"reach the destination $D$. An walks $%d$ km to $A$ and then another $%d$ km to $D$, where $\widehat{PAD} = %d^{\circ}$. "
                 r"Binh walks $%d$ km to $B$ and then goes straight to $D$ (as shown in the figure). Find the area of the quadrilateral region $PADB$ "
                 r"(in $\text{km}^{2}$, rounded to the nearest tenth)." % (phi, m, n, psi, k))
        giai = (r"$S_{PAD} = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %d^{\circ} \approx %s$." % (m, n, psi, _xx(S1, 3))
                + "\\\\\n" +
                r"$PD = \sqrt{%d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %d^{\circ}} \approx %s$; "
                r"$\widehat{APD} \approx %s^{\circ}$, so $\widehat{BPD} \approx %s^{\circ}$."
                % (m, n, m, n, psi, _xx(PD, 3), _xx(APD, 2), _xx(BPD, 2)) + "\\\\\n" +
                r"$S_{PBD} = \dfrac{1}{2}\cdot PB\cdot PD\cdot\sin\widehat{BPD} \approx %s$." % _xx(S2, 3) + "\\\\\n" +
                r"Hence $S_{PADB} \approx %s$ $\text{km}^{2}$." % dap)
        ds = _ba_nhieu(dap, [_xx(S1, 1), _xx(S2, 1), _xx(0.5 * m * k * _sin_d(phi), 1)],
                       buoc=lambda t: _xx(S1 + S2 + t, 1))
        cau += MC_SA_answer_const(debai + "\n\n" + r"\begin{center}" + "\n" + _hinh_hai_ban(phi, m, n, k, PD, BPD) +
                                  "\n" + r"\end{center}", dap, ds, giai, 0, 0, dang)
    return cau



# ------------------------- Câu Đúng/Sai -------------------------

def _so_hoac_phan_so(v):
    return _so_thap_phan_gon(v) or _L(v)


def L10_C3_TF_E_04(socau, socot=1):
    r"""Đúng/Sai - biết BA CẠNH: nhận dạng góc (có góc tù không), côsin một
    góc, diện tích (Heron), bán kính ngoại tiếp.

    CLAUDE THEM 30/09/2026 - bien the 04 cua L10_C3_TF_E, theo cau 1 Phan II
    bai tap trac nghiem Bai 6 (a = 13, b = 14, c = 15). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        a, b, c, S, p = random.choice(HERON_NGUYEN)
        a, b, c = random.sample([a, b, c], 3)
        lon = max(a, b, c)
        ten_lon = "A" if lon == a else ("B" if lon == b else "C")
        con = [x for x in (a, b, c) if x != lon] if [a, b, c].count(lon) == 1 else [lon, lon]
        cos_lon = Rational(sum(x * x for x in (a, b, c)) - 2 * lon * lon, 2 * con[0] * con[1])
        tu = cos_lon < 0
        cosA = Rational(b * b + c * c - a * a, 2 * b * c)
        cosB = Rational(a * a + c * c - b * b, 2 * a * c)
        R = Rational(a * b * c, 4 * S)
        debai = r"Given triangle $ABC$ with $a = %d$, $b = %d$, $c = %d$. Determine whether each of the following statements is true or false:" % (a, b, c)
        # a) NB - góc lớn nhất đối diện cạnh lớn nhất, dấu côsin
        ly_a = (r"The largest angle is angle $%s$ (opposite the longest side). Since $\cos %s = %s %s 0$, the triangle %s."
                % (ten_lon, ten_lon, _L(cos_lon), "<" if tu else ">", "has one obtuse angle" if tu else "has three acute angles"))
        dung = [("Triangle $ABC$ has one obtuse angle" if tu else "Triangle $ABC$ has three acute angles", ly_a)]
        sai = [("Triangle $ABC$ has three acute angles" if tu else "Triangle $ABC$ has one obtuse angle", ly_a), ("Triangle $ABC$ is a right triangle", ly_a)]
        if [a, b, c].count(lon) == 1:
            dung.append((r"The largest angle of triangle $ABC$ is angle $%s$" % ten_lon, ly_a))
            sai += [(r"The largest angle of triangle $ABC$ is angle $%s$" % X, ly_a) for X, v in zip("ABC", (a, b, c)) if v != lon]
        dung.append((r"$\cos %s %s 0$" % (ten_lon, "<" if tu else ">"), ly_a))
        sai.append((r"$\cos %s %s 0$" % (ten_lon, ">" if tu else "<"), ly_a))
        y1 = _phat_bieu(dung, sai)
        # b) TH - hệ quả định lí côsin (thay số một lần)
        ly_b = (r"$\cos A = \dfrac{b^{2} + c^{2} - a^{2}}{2bc} = \dfrac{%d + %d - %d}{2\cdot %d\cdot %d} = %s$, "
                r"$\cos B = \dfrac{a^{2} + c^{2} - b^{2}}{2ac} = %s$." % (b * b, c * c, a * a, b, c, _so_hoac_phan_so(cosA), _so_hoac_phan_so(cosB)))
        dung, sai = [], []
        for ten, v, ws in (("A", cosA, [Rational(a * a + b * b - c * c, 2 * a * b), -cosA, 2 * cosA]),
                           ("B", cosB, [Rational(b * b + c * c - a * a, 2 * b * c), -cosB, 2 * cosB])):
            dung.append((r"$\cos %s = %s$" % (ten, _so_hoac_phan_so(v)), ly_b))
            for w in ws:
                if w != v:
                    sai.append((r"$\cos %s = %s$" % (ten, _so_hoac_phan_so(w)), ly_b))
        y2 = _phat_bieu(dung, sai)
        # c) VD - Heron
        ly_c = (r"$p = %d$, $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$." % (p, p, p - a, p - b, p - c, S))
        y3 = _tf_gop(_tf_ct(r"The area of triangle $ABC$ equals $%s$", Integer(S), ly_c,
                            [(Integer(2 * S), "Multiplied by an extra factor of 2"), (sqrt((p - a) * (p - b) * (p - c)), "Missing factor $p$"), (Rational(S, 2), "Divided by an extra factor of 2")],
                            them=[r"The semiperimeter of triangle $ABC$ is $p = %d$" % p]))
        # d) VDC - bán kính ngoại tiếp, nội tiếp
        ly_d = (ly_c + r" $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$, $r = \dfrac{S}{p} = %s$."
                % (a, b, c, S, _so_hoac_phan_so(R), _so_hoac_phan_so(Rational(S, p))))
        dung = [(r"The circumradius of triangle $ABC$ equals $%s$" % _so_hoac_phan_so(R), ly_d),
                (r"The inradius of triangle $ABC$ equals $%s$" % _so_hoac_phan_so(Rational(S, p)), ly_d)]
        sai = [(r"The circumradius of triangle $ABC$ equals $%s$" % _so_hoac_phan_so(w), ly_d)
               for w in (4 * R, 2 * R, Rational(S, p)) if w != R]
        sai += [(r"The inradius of triangle $ABC$ equals $%s$" % _so_hoac_phan_so(w), ly_d)
                for w in (Rational(S, 2 * p), Rational(2 * S, p), R) if w != Rational(S, p)]
        y4 = _phat_bieu(dung, sai)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _nho = min(a, b, c)
        if [a, b, c].count(_nho) == 1:
            _tn = "ABC"[[a, b, c].index(_nho)]
            _tf_them(y1, [(r"The smallest angle of triangle $ABC$ is angle $%s$" % _tn, ly_a)],
                     [(r"The smallest angle of triangle $ABC$ is angle $%s$" % X, ly_a) for X, v in zip("ABC", (a, b, c)) if v != _nho])
        else:
            _tf_them(y1, [(r"Triangle $ABC$ is an isosceles triangle", ly_a)], [(r"Triangle $ABC$ is an equilateral triangle", ly_a)])
        _cosC = Rational(a * a + b * b - c * c, 2 * a * b)
        _lyC = r"$\cos C = \dfrac{a^{2} + b^{2} - c^{2}}{2ab} = %s$." % _so_hoac_phan_so(_cosC)
        _tf_them(y2, [(r"$\cos C = %s$" % _so_hoac_phan_so(_cosC), _lyC)],
                 [(r"$\cos C = %s$" % _so_hoac_phan_so(w), _lyC) for w in (-_cosC, 2 * _cosC) if w != _cosC])
        _d1, _s1 = _tf_bdt(r"The circumradius of triangle $ABC$ is %s $%s$", float(R), ly_d)
        _tf_them(y4, _d1, _s1)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_E_05(socau, socot=1):
    r"""Đúng/Sai - biết hai cạnh và góc xen giữa: công thức diện tích, diện
    tích, đường cao $h_b$, và bài toán thực tế "trụ điện cách đều ba hộ dân"
    (bán kính ngoại tiếp).

    CLAUDE THEM 30/09/2026 - bien the 05 cua L10_C3_TF_E, theo cau 2 Phan II
    bai tap trac nghiem Bai 6 (A = 60, AB = 15, AC = 35). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        A = random.choice([30, 45, 60, 120, 135, 150])
        c, b = random.sample(range(5, 36, 5), 2)
        sA, cA = _gtlg("sin", A), _gtlg("cos", A)
        S = simplify(b * c * sA / 2)
        hb = simplify(2 * S / b)
        a2 = simplify(b * b + c * c - 2 * b * c * cA)
        R = simplify(sqrt(a2) / (2 * sA))
        debai = (r"Given triangle $ABC$ with $\widehat{BAC} = %s$, $AB = %d$ and $AC = %d$. Determine whether each of the "
                 r"following statements is true or false:" % (_goc(A), c, b))
        # a) NB - nhận ra công thức diện tích
        ly_a = r"The area equals half the product of two sides and the sine of the included angle: $S = \dfrac{1}{2}AB\cdot AC\cdot\sin A$; also, $S = \dfrac{1}{2}AC\cdot h_b$."
        mau = r"The area of triangle $ABC$ is given by the formula $S = %s$"
        y1 = _phat_bieu(
            [(mau % r"\dfrac{1}{2}AB\cdot AC\cdot\sin A", ly_a), (mau % r"\dfrac{1}{2}AC\cdot h_b", ly_a)],
            [(mau % r"\dfrac{1}{2}AB\cdot AC\cdot\cos A", ly_a), (mau % r"AB\cdot AC\cdot\sin A", ly_a),
             (mau % r"\dfrac{1}{2}AB\cdot BC\cdot\sin A", ly_a), (mau % r"\dfrac{1}{2}AB\cdot h_b", ly_a)])
        # b) TH - thay số
        ly_b = r"$S = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s = %s$." % (c, b, _goc(A), _L(S))
        y2 = _tf_gop(_tf_ct(r"The area of triangle $ABC$ is $S = %s$", S, ly_b,
                            [(2 * S, "Forgot the factor $\\dfrac{1}{2}$"), (simplify(b * c * abs(cA) / 2), "Confused $\\sin A$ with $\\cos A$"), (S / 2, "Divided by an extra factor of 2")]),
                     _tf_bdt(r"The area of triangle $ABC$ is %s $%s$", float(S), ly_b))
        # c) VD - đường cao
        ly_c = ly_b + r" $h_b = \dfrac{2S}{AC} = \dfrac{2\cdot %s}{%d} = %s$." % (_L(S), b, _L(hb))
        y3 = _tf_gop(_tf_ct(r"The length of the altitude from $B$ is $h_b = %s$", hb, ly_c,
                            [(2 * hb, "Multiplied by an extra factor of 2"), (hb / 2, "Forgot to multiply by 2"), (simplify(2 * S / c), "Divided by the wrong side $AB$")],
                            them=[r"The length of the altitude from $B$ is $h_b = AB\cdot\sin %s$" % _goc(A)]))
        # d) VDC - trụ điện cách đều ba hộ dân
        bai = (r"Three locations $A$, $B$, $C$ are three households that need to be connected to the power supply. An electric pole is to be placed at "
               r"location $D$ so that the wires from the pole to the households are equally long. Then $DA = %s$")
        ly_d = (r"Since $DA = DB = DC$, $D$ is the circumcenter, so $DA = R$. $BC^{2} = %d + %d - 2\cdot %d\cdot %d"
                r"\cdot %s = %s$, $R = \dfrac{BC}{2\sin A} = %s$." % (c * c, b * b, c, b, _ngoac(cA), _L(a2), _L(R)))
        dung = [(bai % _L(R), ly_d), (bai.replace("$DA = %s$", "$DB + DC = %s$") % _L(simplify(2 * R)), ly_d)]
        sai = []
        for w, ghi in ((simplify(2 * R), "Forgot to divide by 2"), (simplify(sqrt(b * b + c * c + 2 * b * c * cA) / (2 * sA)), "Sign error when computing $BC$"),
                       (simplify(sqrt(a2) / (2 * abs(cA))), "Confused $\\sin A$ with $\\cos A$")):
            if simplify(w - R) != 0:
                sai.append((bai % _L(w), ghi + ". " + ly_d))
        sai.append((bai.replace("$DA = %s$", "$DB + DC = %s$") % _L(R), ly_d))
        y4 = _phat_bieu(dung, sai)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(mau % r"\dfrac{1}{2}AB\cdot h_c", ly_a)], [(mau % r"AB\cdot h_c", ly_a)])
        _bd = _tf_mau_bdt(bai)
        _d1, _s1 = _tf_bdt(_bd[0], float(R), ly_d, tu=_bd[1])
        _tf_them(y4, _d1, _s1)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def _hinh_doc():
    return (
        "\\begin{tikzpicture}[scale=0.55,font=\\footnotesize,line join=round]\n"
        "\\coordinate (A) at (0,0);\n\\coordinate (B) at (10,0);\n\\coordinate (H) at (3.5,0);\n"
        "\\coordinate (C) at (3.5,1.5);\n"
        "\\draw[gray] (-0.5,0) -- (10.5,0);\n\\draw[thick] (A) -- (C) -- (B);\n\\draw (C) -- (H);\n"
        "\\draw (3.3,0) -- (3.3,0.2) -- (3.5,0.2);\n"
        "\\fill (A) circle (2pt) node[below] {$A$};\n\\fill (B) circle (2pt) node[below] {$B$};\n"
        "\\node[below] at (H) {$H$};\n\\node[above] at (C) {$C$};\n"
        "\\end{tikzpicture}"
    )


def L10_C3_TF_G_01(socau, socot=1):
    r"""Đúng/Sai - bài toán con dốc: biết đoạn lên dốc và hai góc nghiêng; so
    sánh độ dốc, độ cao dốc, quãng đường chim bay, vận tốc lên dốc (có hình).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 3 Phan II bai tap trac nghiem
    Bai 6 (ban Mai di xe dap, AC = 300 m, A = 6 do, B = 4 do). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        while True:
            L = random.choice(range(200, 451, 50))
            al, be = random.sample([3, 4, 5, 6, 7, 8], 2)
            phut = random.choice([5, 6, 8, 10])
            v2 = random.choice([12, 15, 18])
            CH = L * _sin_d(al)
            CB = L * _sin_d(al) / _sin_d(be)
            AB = L * _sin_d(al + be) / _sin_d(be)
            t_len = phut / 60 - CB / 1000 / v2
            if t_len <= 0:
                continue
            v1 = L / 1000 / t_len
            if (3 <= v1 <= 20 and _x1(CH) != _x1(L * math.tan(math.radians(al))) and _xa_bien(v1)
                    and _xa_bien(CH, 1) and _xa_bien(AB)):
                break
        m = r"\,\text{m}"
        debai = (r"At $%d$ minutes before $7$ o'clock, Mai rides her bicycle from home (point $A$) to school (point $B$), and has to climb the slope "
                 r"$AC$ and then descend the slope $CB$ ($C$ is the top of the hill, as shown in the figure). The uphill section is $%d$ m long, $\widehat{A} = "
                 r"%d^{\circ}$, $\widehat{B} = %d^{\circ}$. Determine whether each of the following statements is true or false:" % (phut, L, al, be))
        # a) NB - đọc góc
        len_cao = al > be
        ly_a = (r"The angle of inclination going up is $%d^{\circ}$ and going down is $%d^{\circ}$; $\widehat{ACB} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$."
                % (al, be, al, be, 180 - al - be))
        y1 = _phat_bieu(
            [(r"The slope going up is %s the slope going down" % ("greater than" if len_cao else "less than"), ly_a),
             (r"$\widehat{ACB} = %d^{\circ}$" % (180 - al - be), ly_a)],
            [(r"The slope going up is %s the slope going down" % ("less than" if len_cao else "greater than"), ly_a),
             (r"$\widehat{ACB} = %d^{\circ}$" % (al + be), ly_a), (r"$\widehat{ACB} = %d^{\circ}$" % (180 - al), ly_a),
             (r"$\widehat{ACB} = %d^{\circ}$" % (90 - al), ly_a)])
        # b) TH - độ cao dốc
        ly_b = r"$CH = AC\cdot\sin A = %d\cdot\sin %d^{\circ}$." % (L, al)
        y2 = _tf_gop(_tf_so(r"The height of the hill is $%s$", CH, 1, ly_b,
                            [(L * math.tan(math.radians(al)), "Mistakenly used $CH = AC\\cdot\\tan A$"), (L * _cos_d(al), "Confused $\\sin$ with $\\cos$"),
                             (L * _sin_d(be), "Used the wrong angle $B$")], dv=m, bdt=r"The height of the hill is %s $%s$"))
        # c) VD - quãng đường chim bay (định lí sin)
        ly_c = (r"$\widehat{C} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$; law of sines: $AB = \dfrac{AC\cdot\sin C}"
                r"{\sin B}$." % (al, be, 180 - al - be))
        y3 = _tf_gop(_tf_so(r"The straight-line distance from home to school is $%s$", AB, 0, ly_c,
                            [(L + CB, "That is the distance traveled along the slope, $AC + CB$"), (L * _sin_d(al + be) / _sin_d(al), "Divided by $\\sin A$ by mistake"),
                             (math.hypot(L, CB), "Treated the triangle as right-angled at $C$")], dv=m, bdt=r"The straight-line distance from home to school is %s $%s$"))
        # d) VDC - vận tốc lên dốc
        ly_d = (r"$CB = \dfrac{AC\cdot\sin A}{\sin B} \approx %s$ m; the time going downhill is $\approx %s$ hours; the time going "
                r"uphill is $\approx \dfrac{%d}{60} - %s \approx %s$ hours; the uphill speed is $\approx \dfrac{%s}{%s}$ km/h."
                % (_xx(CB, 2), _xx(CB / 1000 / v2, 4), phut, _xx(CB / 1000 / v2, 4), _xx(t_len, 4), _xx(L / 1000, 3), _xx(t_len, 4)))
        mau = (r"To arrive at school at exactly $7$ o'clock, given that Mai rides downhill at a constant speed of $%d$ km/h, Mai "
               r"climbed the slope at a speed of about $%s$ km/h" % (v2, "%s"))
        t_sai = phut / 60 - AB / 1000 / v2
        sai = [(L / 1000 / (phut / 60), "Forgot to subtract the downhill time"),
               (L / 1000 / t_sai if t_sai > 0 else None, "Used $AB$ instead of $CB$ by mistake"),
               (L / 1000 / (phut / 60 - CB / v2 / 60) if phut / 60 - CB / v2 / 60 > 0 else None, "Wrong unit conversion")]
        d1, s1 = _tf_so(mau, v1, 0, ly_d, sai, bdt=r"To arrive at school at exactly $7$ o'clock, Mai must climb the slope at a speed %s $%s$ km/h")
        d2, s2 = _tf_so(r"The time Mai spends climbing the slope is about $%s$ minutes", t_len * 60, 1, ly_d,
                        [(phut - CB / 1000 / v2, "Mixed up minutes and hours"), (phut, "Forgot to subtract the downhill time")]) \
            if _xa_bien(t_len * 60, 1) else ([], [])
        y4 = _phat_bieu(d1 + d2, s1 + s2)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y1, [(r"Angle $\widehat{ACB}$ is an obtuse angle", ly_a)], [(r"Angle $\widehat{ACB}$ is an acute angle", ly_a), (r"$\widehat{ACB} = %d^{\circ}$" % (180 - al), ly_a)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_doc(), 0, socot)
    return cauTF


def L10_C3_TF_G_02(socau, socot=1):
    r"""Đúng/Sai - con dốc cho biết ĐỘ CAO đỉnh dốc và hai góc nghiêng: tính
    đoạn lên dốc, đoạn xuống dốc, khoảng cách hai chân dốc, thời gian đi (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TF_G (_01: cho doan len doc; _02:
    cho do cao doc, hoi nguoc lai do dai cac doan va thoi gian). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cauTF = ""
    for _ in range(socau):
        h = random.choice(range(15, 41, 5))
        al, be = random.sample([4, 5, 6, 7, 8, 10], 2)
        v1, v2 = random.choice([6, 8, 10]), random.choice([15, 18, 20])
        AC, CB = h / _sin_d(al), h / _sin_d(be)
        AB = h / math.tan(math.radians(al)) + h / math.tan(math.radians(be))
        t = (AC / 1000 / v1 + CB / 1000 / v2) * 60
        m = r"\,\text{m}"
        debai = (r"A hill has its top $C$ at a height $CH = %d$ m above the road surface ($H$ lies on $AB$). The uphill section $AC$ is inclined at "
                 r"$\widehat{A} = %d^{\circ}$ and the downhill section $CB$ is inclined at $\widehat{B} = %d^{\circ}$ to the "
                 r"horizontal (as shown in the figure). Determine whether each of the following statements is true or false:" % (h, al, be))
        # a) NB - tam giác vuông AHC
        ly_a = r"In triangle $AHC$, right-angled at $H$: $AC = \dfrac{CH}{\sin A} = \dfrac{%d}{\sin %d^{\circ}}$." % (h, al)
        y1 = _tf_gop(_tf_so(r"The uphill section is about $%s$ long", AC, 0, ly_a,
                            [(h / math.tan(math.radians(al)), "That is $AH$"), (h / _cos_d(al), "Confused $\\sin$ with $\\cos$"),
                             (h * _sin_d(al), "Mistakenly used $AC = CH\\cdot\\sin A$")], dv=m, bdt=r"The uphill section is %s $%s$", tu=("longer than", "shorter than")))
        # b) TH - tam giác vuông BHC
        ly_b = r"In triangle $BHC$, right-angled at $H$: $CB = \dfrac{CH}{\sin B} = \dfrac{%d}{\sin %d^{\circ}}$." % (h, be)
        y2 = _tf_gop(_tf_so(r"The downhill section is about $%s$ long", CB, 0, ly_b,
                            [(h / math.tan(math.radians(be)), "That is $HB$"), (h / _cos_d(be), "Confused $\\sin$ with $\\cos$"),
                             (h / _sin_d(al), "Used the wrong angle $A$")], dv=m, bdt=r"The downhill section is %s $%s$", tu=("longer than", "shorter than")))
        # c) VD - khoảng cách hai chân dốc
        ly_c = (r"$AB = AH + HB = \dfrac{CH}{\tan A} + \dfrac{CH}{\tan B}$ (or use the law of sines in triangle $ABC$).")
        y3 = _tf_gop(_tf_so(r"The distance between the two foot points $A$ and $B$ of the hill is about $%s$", AB, 0, ly_c,
                            [(AC + CB, "That is the sum of the two slope sections"), (abs(h / math.tan(math.radians(al)) - h / math.tan(math.radians(be))), "Subtracted instead of added"),
                             (h * (math.tan(math.radians(al)) + math.tan(math.radians(be))), "Confused $\\tan$ with $\\cot$")], dv=m,
                            bdt=r"The distance between the two foot points of the hill is %s $%s$"))
        # d) VDC - thời gian đi hết con dốc
        ly_d = (r"The time going uphill is $\dfrac{%s}{%d}$ hours and going downhill is $\dfrac{%s}{%d}$ hours; the total (converted to minutes)."
                % (_xx(AC / 1000, 4), v1, _xx(CB / 1000, 4), v2))
        mau = (r"A cyclist rides uphill at a speed of $%d$ km/h and downhill at a speed of $%d$ km/h; covering the whole "
               r"hill takes about $%s$ minutes" % (v1, v2, "%s"))
        y4 = _tf_gop(_tf_so(mau, t, 1, ly_d,
                            [((AC + CB) / 1000 / ((v1 + v2) / 2) * 60, "Used the average of the two speeds"),
                             ((AC / 1000 / v2 + CB / 1000 / v1) * 60, "Swapped the two speeds"), (AB / 1000 / v1 * 60, "Used $AB$ by mistake")],
                            bdt=(r"A cyclist rides uphill at a speed of $%d$ km/h and downhill at a speed of $%d$ km/h; covering the whole "
                                 r"hill takes %s $%s$ minutes" % (v1, v2, "%s", "%s")), tu=("more than", "less than")))
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_doc(), 0, socot)
    return cauTF


def _hinh_tu_giac(A, B, C, D, nhan=("A", "B", "C", "D"), cheo=("B", "D")):
    pts = {"A": A, "B": B, "C": C, "D": D}
    xs = [p[0] for p in pts.values()]
    ys = [p[1] for p in pts.values()]
    k = 4.0 / max(max(xs) - min(xs), max(ys) - min(ys))
    s = "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
    for t, (x, y) in pts.items():
        s += "\\coordinate (%s) at (%.2f,%.2f);\n" % (t, x * k, y * k)
    s += "\\draw[thick] (A) -- (B) -- (C) -- (D) -- cycle;\n\\draw[dashed] (%s) -- (%s);\n" % cheo
    cx, cy = sum(xs) / 4 * k, sum(ys) / 4 * k
    for t in "ABCD":
        x, y = pts[t][0] * k, pts[t][1] * k
        s += "\\node at ($(%s)+(%.2f,%.2f)$) {$%s$};\n" % (t, 0.3 * (x - cx) / (abs(x - cx) + abs(y - cy) + 1e-9),
                                                            0.3 * (y - cy) / (abs(x - cx) + abs(y - cy) + 1e-9), t)
    return s + "\\end{tikzpicture}"


def L10_C3_TF_H_01(socau, socot=1):
    r"""Đúng/Sai - mảnh đất tứ giác $ABCD$ ($BC = CD$), biết $AB$, $BC$, hai góc
    $\widehat{ABC}$, $\widehat{BCD}$: đường chéo $BD$, góc $\widehat{ABD}$, diện tích,
    chi phí lát gạch (có hình).

    CLAUDE THEM 30/09/2026 - dang moi, theo cau 4 Phan II bai tap trac nghiem
    Bai 6 (AB = 6, BC = CD = 4, ABC = 100, BCD = 120, 400 000 dong/m2). Co Lan
    duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    CAN = {60: Integer(1), 90: sqrt(2), 120: sqrt(3)}
    cauTF = ""
    for _ in range(socau):
        while True:
            p, q = random.randint(5, 9), random.randint(3, 6)
            g = random.choice([60, 90, 120])
            dbc = (180 - g) // 2
            b = random.choice(range(dbc + 30, 115, 5))
            gia = random.choice([300, 350, 400, 450, 500])
            BD = q * CAN[g]
            abd = b - dbc
            S1 = q * q * _sin_d(g) / 2
            S2 = 0.5 * p * float(BD) * _sin_d(abd)
            tien = (S1 + S2) * gia / 1000          # trieu dong
            T = math.floor(tien)
            if 0.2 < tien - T < 0.8 and T >= 1 and _xa_bien(S1 + S2, 1):
                break
        Bp, Cp = (0, 0), (q, 0)
        Ap = (p * _cos_d(b), p * _sin_d(b))
        Dp = (q + q * _cos_d(180 - g), q * _sin_d(180 - g))
        SBCD = simplify(q * q * _gtlg("sin", g) / 2)
        debai = (r"A plot of land in the shape of a quadrilateral $ABCD$ is to be tiled, as shown in the figure. Given $AB = %d$ m, $BC = CD = %d$ m, "
                 r"$\widehat{ABC} = %d^{\circ}$, $\widehat{BCD} = %d^{\circ}$, and the tiling cost is $%d\,000$ VND per "
                 r"square meter. Determine whether each of the following statements is true or false:" % (p, q, b, g, gia))
        # a) NB - định lí côsin trong tam giác BCD
        ly_a = (r"Triangle $BCD$: $BD^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %d^{\circ} = %s$, so $BD = %s$ m."
                % (q * q, q * q, q, q, g, _L(BD ** 2), _L(BD)))
        y1 = _tf_gop(_tf_ct(r"The length of the diagonal $BD$ equals $%s$ m", BD, ly_a,
                            [(q * CAN[{60: 90, 90: 120, 120: 90}[g]], "Calculation error"), (Integer(q), "Mistook triangle $BCD$ for an equilateral triangle"),
                             (simplify(q * sqrt(2 + 2 * _gtlg("cos", g))), "Sign error"), (Integer(2 * q), "Added the two sides")],
                            them=[r"$BD^{2} = %s$" % _L(BD ** 2)]))
        # b) TH - tam giác cân
        ly_b = (r"Since triangle $BCD$ is isosceles at $C$, $\widehat{DBC} = \dfrac{180^{\circ} - %d^{\circ}}{2} = %d^{\circ}$, hence "
                r"$\widehat{ABD} = %d^{\circ} - %d^{\circ} = %d^{\circ}$." % (g, dbc, b, dbc, abd))
        y2 = _phat_bieu(
            [(r"The measure of angle $\widehat{ABD}$ equals $%d^{\circ}$" % abd, ly_b), (r"The measure of angle $\widehat{DBC}$ equals $%d^{\circ}$" % dbc, ly_b)],
            [(r"The measure of angle $\widehat{ABD}$ equals $%d^{\circ}$" % w, ly_b) for w in (abd + 10, b - g, b - (180 - g)) if 0 < w < 180 and w != abd] +
            [(r"The measure of angle $\widehat{DBC}$ equals $%d^{\circ}$" % w, ly_b) for w in (g, 180 - g) if w != dbc])
        # c) VD - diện tích tam giác BCD
        ly_c = r"$S_{BCD} = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %d^{\circ} = %s$ ($\text{m}^{2}$)." % (q, q, g, _L(SBCD))
        sai_c = [(2 * SBCD, "Forgot the factor $\\dfrac{1}{2}$"), (SBCD / 2, "Divided by an extra factor of 2")]
        if g != 90:
            sai_c.append((simplify(q * q * abs(_gtlg("cos", g)) / 2), "Confused $\\sin$ with $\\cos$"))
        y3 = _tf_gop(_tf_ct(r"The area of triangle $BCD$ equals $%s$ $\text{m}^{2}$", SBCD, ly_c, sai_c),
                     _tf_bdt(r"The area of triangle $BCD$ is %s $%s$", float(SBCD), ly_c, dv=r"\,\text{m}^{2}"))
        # d) VDC - diện tích tứ giác, chi phí
        ly_d = (r"$S_{ABD} = \dfrac{1}{2}\cdot %d\cdot %s\cdot\sin %d^{\circ} \approx %s$; $S_{ABCD} \approx %s$ "
                r"$\text{m}^{2}$; cost $\approx %s$ VND." % (p, _L(BD), abd, _xx(S2, 2), _xx(S1 + S2, 2),
                                                               "{:,}".format(_lt((S1 + S2) * gia * 1000)).replace(",", r"\,")))
        d1, s1 = _n3_chi_phi(S1 + S2, gia, ly_d)
        d2, s2 = _tf_so(r"The area of the plot $ABCD$ is approximately $%s$", S1 + S2, 1, ly_d,
                        [(S1 + 2 * S2, "Forgot the factor $\\dfrac{1}{2}$ in $S_{ABD}$"), (S1 + 0.5 * p * q * _sin_d(b), "Mistakenly used $\\widehat{ABC}$ for triangle $ABD$")],
                        dv=r"\,\text{m}^{2}")
        # ý d) CHỈ hỏi về chi phí (khớp câu dẫn có giá); phát biểu về diện tích mảnh đất chuyển sang ý c)
        y4 = _phat_bieu(d1, s1)
        _tf_them(y3, d2, s2)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _tf_them(y2, [(r"Triangle $BCD$ is isosceles at $C$", ly_b), (r"$\widehat{ABD} + \widehat{DBC} = %d^{\circ}$" % b, ly_b)],
                 [(r"Triangle $BCD$ is isosceles at $B$", ly_b), (r"$\widehat{ABD} + \widehat{DBC} = %d^{\circ}$" % (180 - b), ly_b)])
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_tu_giac(Ap, Bp, Cp, Dp), 0, socot)
    return cauTF


def L10_C3_TF_H_02(socau, socot=1):
    r"""Đúng/Sai - mảnh đất tứ giác biết $AB$, $AD$, góc $\widehat{A}$ và hai cạnh
    $BC$, $CD$: đường chéo $BD$ (định lí côsin), côsin góc $C$, diện tích hai
    tam giác, tổng diện tích / chi phí (có hình).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TF_H (_01: biet hai goc tai B, C
    va BC = CD; _02: biet goc A va bon canh). Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    BO = [(60, b, c) for b, c in CAP_COSIN[60] if b + c < 30] + [(120, b, c) for b, c in CAP_COSIN[120] if b + c < 30]
    cauTF = ""
    for _ in range(socau):
        while True:
            A, u, v = random.choice(BO)
            BD = int(_lt(math.sqrt(u * u + v * v - 2 * u * v * _cos_d(A))))
            x, y = random.randint(3, 15), random.randint(3, 15)
            if not (x + y > BD and x + BD > y and y + BD > x):
                continue
            gia = random.choice([300, 400, 500])
            cosC = Rational(x * x + y * y - BD * BD, 2 * x * y)
            S1 = 0.5 * u * v * _sin_d(A)
            sC = math.sqrt(1 - float(cosC) ** 2)
            S2 = 0.5 * x * y * sC
            tien = (S1 + S2) * gia / 1000
            T = math.floor(tien)
            if 0.2 < tien - T < 0.8 and T >= 1 and cosC != 0 and _xa_bien(S1 + S2, 1):
                break
        S1e = simplify(u * v * _gtlg("sin", A) / 2)
        # hinh: A goc toa do, B tren truc Ox, D theo goc A; C phia ben kia BD
        Ap, Bp = (0, 0), (u, 0)
        Dp = (v * _cos_d(A), v * _sin_d(A))
        ang_BD = math.atan2(Dp[1] - Bp[1], Dp[0] - Bp[0])
        gB = math.acos((x * x + BD * BD - y * y) / (2 * x * BD))
        Cp = (Bp[0] + x * math.cos(ang_BD - gB), Bp[1] + x * math.sin(ang_BD - gB))
        def _phia(P):
            return (Dp[0] - Bp[0]) * (P[1] - Bp[1]) - (Dp[1] - Bp[1]) * (P[0] - Bp[0])
        if _phia(Cp) * _phia(Ap) > 0:
            Cp = (Bp[0] + x * math.cos(ang_BD + gB), Bp[1] + x * math.sin(ang_BD + gB))
        debai = (r"A quadrilateral plot of land $ABCD$ (as shown in the figure) has $AB = %d$ m, $AD = %d$ m, $\widehat{BAD} = %d^{\circ}$, "
                 r"$BC = %d$ m, $CD = %d$ m. The cost of mowing is $%d\,000$ VND per square meter. Determine whether each of the "
                 r"following statements is true or false:" % (u, v, A, x, y, gia))
        # a) NB - định lí côsin trong tam giác ABD
        ly_a = (r"$BD^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %d^{\circ} = %d$, so $BD = %d$ m."
                % (u * u, v * v, u, v, A, BD * BD, BD))
        y1 = _tf_gop(_tf_ct(r"The length of the diagonal $BD$ equals $%s$ m", Integer(BD), ly_a,
                            [(sqrt(Integer(u * u + v * v + 2 * u * v * int(round(2 * _cos_d(A))) // 2)), "Wrong sign of $\\cos A$"),
                             (sqrt(Integer(u * u + v * v)), "Omitted the term containing $\\cos A$"), (Integer(u + v), "Added the two sides")],
                            them=[r"$BD^{2} = %d$" % (BD * BD)]))
        # b) TH - hệ quả định lí côsin trong tam giác BCD
        ly_b = (r"$\cos\widehat{BCD} = \dfrac{CB^{2} + CD^{2} - BD^{2}}{2\cdot CB\cdot CD} = \dfrac{%d + %d - %d}{2\cdot %d"
                r"\cdot %d} = %s$." % (x * x, y * y, BD * BD, x, y, _so_hoac_phan_so(cosC)))
        dung = [(r"$\cos\widehat{BCD} = %s$" % _so_hoac_phan_so(cosC), ly_b),
                (r"Angle $\widehat{BCD}$ is an %s angle" % ("obtuse" if cosC < 0 else "acute"), ly_b)]
        sai = [(r"$\cos\widehat{BCD} = %s$" % _so_hoac_phan_so(w), ly_b)
               for w in (-cosC, 2 * cosC, Rational(x * x + BD * BD - y * y, 2 * x * BD)) if w != cosC]
        sai.append((r"Angle $\widehat{BCD}$ is an %s angle" % ("acute" if cosC < 0 else "obtuse"), ly_b))
        y2 = _phat_bieu(dung, sai)
        # c) VD - diện tích tam giác ABD
        ly_c = r"$S_{ABD} = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %d^{\circ} = %s$ ($\text{m}^{2}$)." % (u, v, A, _L(S1e))
        y3 = _tf_gop(_tf_ct(r"The area of triangle $ABD$ equals $%s$ $\text{m}^{2}$", S1e, ly_c,
                            [(2 * S1e, "Forgot the factor $\\dfrac{1}{2}$"), (Rational(u * v, 4), "Confused $\\sin$ with $\\cos$"), (S1e / 2, "Divided by an extra factor of 2")]),
                     _tf_bdt(r"The area of triangle $ABD$ is %s $%s$", float(S1e), ly_c, dv=r"\,\text{m}^{2}"))
        # d) VDC - tổng diện tích, chi phí
        ly_d = (r"$\sin\widehat{BCD} = \sqrt{1 - \cos^{2}\widehat{BCD}} \approx %s$, $S_{BCD} \approx %s$; $S_{ABCD} \approx "
                r"%s$ $\text{m}^{2}$; cost $\approx %s$ VND." % (_xx(sC, 4), _xx(S2, 2), _xx(S1 + S2, 2),
                                                                   "{:,}".format(_lt((S1 + S2) * gia * 1000)).replace(",", r"\,")))
        d1, s1 = _n3_chi_phi(S1 + S2, gia, ly_d, "mowing the entire plot of land")
        d2, s2 = _tf_so(r"The area of the plot $ABCD$ is approximately $%s$", S1 + S2, 1, ly_d,
                        [(S1 + 2 * S2, "Forgot the factor $\\dfrac{1}{2}$ in $S_{BCD}$"), (S1 + 0.5 * x * y * abs(float(cosC)), "Confused $\\sin$ with $\\cos$")],
                        dv=r"\,\text{m}^{2}")
        # ý d) CHỈ hỏi về chi phí (khớp câu dẫn có giá); phát biểu về diện tích mảnh đất chuyển sang ý c)
        y4 = _phat_bieu(d1, s1)
        _tf_them(y3, d2, s2)
        # --- Bổ sung 01/10/2026 (cô Lan): ý nào cũng ít nhất 3 phát biểu đúng, 3 phát biểu sai ---
        _d1, _s1 = _tf_bdt(r"$\cos\widehat{BCD} %s %s$", float(cosC), ly_b, tu=(">", "<"))
        _tf_them(y2, _d1, _s1)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_tu_giac(Ap, Bp, Cp, Dp), 0, socot)
    return cauTF


# =====================================================================
# TH031 - GÓC PHỤ NHAU, BÙ NHAU VỚI GIÁ TRỊ LƯỢNG GIÁC "ĐẸP" KHÔNG ĐẶC BIỆT
# CLAUDE THEM 30/09/2026 theo cô Lan:
#   TH031_MC_G  biết một GTLG của α (vd cos α = 1/5), tìm GTLG của 180° - α (và ngược lại)
#   TH031_MC_H  như G với góc phụ 90° - α (α nhọn)
#   TH031_MC_I  có hình: góc bẹt (_01) / góc vuông (_02) chia bởi một tia
# Giá trị chọn trước (phân số, căn bậc hai ghi ra được), KHÔNG phải của góc đặc
# biệt; số đo góc để vẽ hình tính ngược từ giá trị đó.
# =====================================================================

_DAC_BIET_SC = {Rational(1, 2), sqrt(2) / 2, sqrt(3) / 2}
_DAC_BIET_TC = {Integer(1), sqrt(3), sqrt(3) / 3}
_SC_DEP = ([Rational(p, q) for q in range(3, 10) for p in range(1, q) if math.gcd(p, q) == 1] +
           [sqrt(2) / 3, 2 * sqrt(2) / 3, sqrt(2) / 4, 3 * sqrt(2) / 5, sqrt(3) / 3, sqrt(3) / 4, sqrt(3) / 5,
            sqrt(5) / 3, sqrt(5) / 4, sqrt(5) / 5, 2 * sqrt(5) / 5, sqrt(6) / 3, sqrt(6) / 4, sqrt(7) / 3,
            sqrt(7) / 4])
_TC_DEP = ([Rational(p, q) for q in range(2, 6) for p in range(1, 3 * q) if math.gcd(p, q) == 1 and p != q] +
           [Integer(k) for k in (2, 3, 4, 5)] +
           [sqrt(2), sqrt(5), 2 * sqrt(2), sqrt(2) / 2, sqrt(6) / 2, sqrt(3) / 2, sqrt(5) / 2, 2 * sqrt(3)])
_BIEU_BU = {"sin": r"\sin\left(180^{\circ} - \alpha\right) = \sin\alpha",
            "cos": r"\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha",
            "tan": r"\tan\left(180^{\circ} - \alpha\right) = -\tan\alpha",
            "cot": r"\cot\left(180^{\circ} - \alpha\right) = -\cot\alpha"}
_BIEU_PHU = {"sin": r"\cos\left(90^{\circ} - \alpha\right) = \sin\alpha",
             "cos": r"\sin\left(90^{\circ} - \alpha\right) = \cos\alpha",
             "tan": r"\cot\left(90^{\circ} - \alpha\right) = \tan\alpha",
             "cot": r"\tan\left(90^{\circ} - \alpha\right) = \cot\alpha"}
_MIEN_GOC = {"sin": r"$0^{\circ} < \alpha < 180^{\circ}$", "cos": r"$0^{\circ} < \alpha < 180^{\circ}$",
             "tan": r"$0^{\circ} < \alpha < 180^{\circ}$, $\alpha \ne 90^{\circ}$",
             "cot": r"$0^{\circ} < \alpha < 180^{\circ}$"}


def _gtlg_dep(ham, am_duoc):
    """Giá trị 'đẹp' của hàm ham (sin, cos, tan, cot), không phải giá trị của góc đặc biệt.
    sin luôn dương (góc từ 0° đến 180°); am_duoc=True cho phép cos, tan, cot âm."""
    if ham in ("sin", "cos"):
        v = random.choice([t for t in _SC_DEP if t not in _DAC_BIET_SC])
    else:
        v = random.choice([t for t in _TC_DEP if t not in _DAC_BIET_TC])
    if am_duoc and ham != "sin" and random.random() < 0.5:
        v = -v
    return v


def _goc_tu_gtlg(ham, v, tu_duoc=True):
    """Số đo (độ) của góc α trong (0°; 180°) có ham(α) = v - dùng để vẽ hình.
    Với sin có hai góc: chọn ngẫu nhiên góc nhọn hoặc góc tù nếu tu_duoc."""
    x = float(v)
    if ham == "sin":
        a = math.degrees(math.asin(x))
        return 180 - a if (tu_duoc and random.random() < 0.5) else a
    if ham == "cos":
        return math.degrees(math.acos(x))
    t = x if ham == "tan" else 1 / x
    a = math.degrees(math.atan(t))
    return a + 180 if a < 0 else a


def _nhieu_phu_bu(ham, dap, v):
    """Ba phương án nhiễu: sai dấu, nghịch đảo, nhầm sang GTLG còn lại (căn(1 - v^2))."""
    ung = [_tri(-dap)]
    if ham in ("sin", "cos"):
        con = sqrt(1 - v ** 2)
        ung += [_tri(con), _tri(-con), _tri(1 / dap)]
    else:
        ung += [_tri(1 / dap), _tri(-1 / dap)]
    return _ba_nhieu(_tri(dap), ung, buoc=lambda t: _tri(dap + Rational(t, 5)))


def L10_C3_B5_TH031_MC_G_01(socau, dang=1):
    r"""Biết một giá trị lượng giác của $\alpha$ (số đẹp không phải của góc đặc
    biệt, vd $\cos\alpha = \dfrac{1}{5}$), tìm giá trị lượng giác CÙNG TÊN của góc bù
    $180^{\circ} - \alpha$. Hàm sin, cos, tan, cot chọn ngẫu nhiên.

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, True)
        dap = v if ham == "sin" else -v
        debai = (r"Given an angle $\alpha$ with %s and $\%s\alpha = %s$. The value of $\%s\left(180^{\circ} - \alpha\right)$ equals"
                 % (_MIEN_GOC[ham], ham, _tri(v), ham))
        giai = (r"Since the angles $\alpha$ and $180^{\circ} - \alpha$ are supplementary, $%s = %s$."
                % (_BIEU_BU[ham], _tri(dap)))
        cau += MC_SA_answer_const(debai, _tri(dap), _nhieu_phu_bu(ham, dap, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_G_02(socau, dang=1):
    r"""Hỏi NGƯỢC của _01: biết giá trị lượng giác của góc $180^{\circ} - \alpha$
    (vd $\cos\left(180^{\circ} - \alpha\right) = -\dfrac{\sqrt{2}}{4}$), tìm giá trị lượng
    giác cùng tên của $\alpha$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_G theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, True)                  # v = ham(180° - α)
        dap = v if ham == "sin" else -v           # ham(α)
        debai = (r"Given an angle $\alpha$ with %s and $\%s\left(180^{\circ} - \alpha\right) = %s$. The value of $\%s\alpha$ equals"
                 % (_MIEN_GOC[ham], ham, _tri(v), ham))
        giai = (r"Since the angles $\alpha$ and $180^{\circ} - \alpha$ are supplementary, $%s$, so $\%s\alpha = %s$."
                % (_BIEU_BU[ham], ham, _tri(dap)))
        cau += MC_SA_answer_const(debai, _tri(dap), _nhieu_phu_bu(ham, dap, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_H_01(socau, dang=1):
    r"""Góc nhọn $\alpha$ biết một giá trị lượng giác (số đẹp, không đặc biệt, vd
    $\sin\alpha = \dfrac{1}{3}$), tìm giá trị lượng giác của góc phụ $90^{\circ} - \alpha$
    ($\cos\left(90^{\circ} - \alpha\right) = \sin\alpha$, ...).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, False)
        hoi = _DOI_HAM[ham]
        debai = (r"Given an acute angle $\alpha$ with $\%s\alpha = %s$. The value of $\%s\left(90^{\circ} - \alpha\right)$ equals"
                 % (ham, _tri(v), hoi))
        giai = (r"Since the angles $\alpha$ and $90^{\circ} - \alpha$ are complementary, $%s = %s$."
                % (_BIEU_PHU[ham], _tri(v)))
        cau += MC_SA_answer_const(debai, _tri(v), _nhieu_phu_bu(ham, v, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_MC_H_02(socau, dang=1):
    r"""Hỏi NGƯỢC của _01: biết giá trị lượng giác của góc $90^{\circ} - \alpha$
    ($\alpha$ nhọn), tìm giá trị lượng giác của $\alpha$ (vd biết
    $\sin\left(90^{\circ} - \alpha\right) = \dfrac{2}{7}$, tìm $\cos\alpha$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_H theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ham = random.choice(_HAM4)                # hỏi ham(α)
        cho = _DOI_HAM[ham]                        # cho cho(90° - α) = ham(α)
        v = _gtlg_dep(ham, False)
        debai = (r"Given an acute angle $\alpha$ with $\%s\left(90^{\circ} - \alpha\right) = %s$. The value of $\%s\alpha$ equals"
                 % (cho, _tri(v), ham))
        giai = (r"Since the angles $\alpha$ and $90^{\circ} - \alpha$ are complementary, $%s$, so $\%s\alpha = %s$."
                % (_BIEU_PHU[ham], ham, _tri(v)))
        cau += MC_SA_answer_const(debai, _tri(v), _nhieu_phu_bu(ham, v, v), giai, 0, 0, dang)
    return cau


def _hinh_goc_bet(a):
    """Góc bẹt AOB (A bên phải, B bên trái), tia OC tạo với OA góc a độ; ghi α, β."""
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize]\n"
        "\\coordinate (O) at (0,0);\n\\coordinate (A) at (2.4,0);\n\\coordinate (B) at (-2.4,0);\n"
        "\\coordinate (C) at (%.1f:2.2);\n" % a
        + "\\draw[thick] (B) -- (A);\n\\draw[thick] (O) -- (C);\n"
        "\\draw (0.5,0) arc (0:%.1f:0.5);\n" % a
        + "\\draw (%.1f:0.7) arc (%.1f:180:0.7);\n" % (a, a)
        + "\\node at (%.1f:0.85) {$\\alpha$};\n" % (a / 2)
        + "\\node at (%.1f:1.05) {$\\beta$};\n" % ((a + 180) / 2)
        + "\\fill (O) circle (0.03) node[below] {$O$};\n"
        "\\fill (A) circle (0.03) node[below] {$A$};\n"
        "\\fill (B) circle (0.03) node[below] {$B$};\n"
        "\\fill (C) circle (0.03) node[%s] {$C$};\n" % ("above left" if a > 90 else "above right")
        + "\\end{tikzpicture}"
    )


def _hinh_goc_vuong(a):
    """Góc vuông xOy, tia Oz nằm giữa tạo với Ox góc a độ; ghi α, β."""
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize]\n"
        "\\coordinate (O) at (0,0);\n"
        "\\draw[thick] (0,0) -- (2.4,0) node[below] {$x$};\n"
        "\\draw[thick] (0,0) -- (0,2.4) node[left] {$y$};\n"
        "\\draw[thick] (0,0) -- (%.1f:2.4) node[above right] {$z$};\n" % a
        + "\\draw (0.6,0) arc (0:%.1f:0.6);\n" % a
        + "\\draw (%.1f:0.85) arc (%.1f:90:0.85);\n" % (a, a)
        + "\\node at (%.1f:0.95) {$\\alpha$};\n" % (a / 2)
        + "\\node at (%.1f:1.2) {$\\beta$};\n" % ((a + 90) / 2)
        + "\\fill (O) circle (0.03) node[below left] {$O$};\n"
        "\\end{tikzpicture}"
    )


def L10_C3_B5_TH031_MC_I_01(socau, dang=1):
    r"""Có hình: góc bẹt $\widehat{AOB}$, tia $OC$ chia thành hai góc kề bù
    $\alpha = \widehat{AOC}$, $\beta = \widehat{BOC}$. Biết một giá trị lượng giác
    của $\alpha$ (số đẹp), tìm giá trị lượng giác cùng tên của $\beta = 180^{\circ} - \alpha$.
    Giá trị chọn trước, số đo góc tính ngược để vẽ đúng hình.

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, True)
        a = _goc_tu_gtlg(ham, v)
        if not (20 <= a <= 160) or abs(a - 90) < 10:
            continue
        so += 1
        dap = v if ham == "sin" else -v
        debai = (r"In the figure shown, the points $A$, $O$, $B$ are collinear, $\widehat{AOC} = \alpha$, "
                 r"$\widehat{BOC} = \beta$. Given $\%s\alpha = %s$. The value of $\%s\beta$ equals"
                 % (ham, _tri(v), ham))
        giai = (r"Since $A$, $O$, $B$ are collinear, $\alpha + \beta = 180^{\circ}$, that is, $\beta = 180^{\circ} - \alpha$."
                + "\\\\\n" + r"Hence $\%s\beta = %s = %s$."
                % (ham, _BIEU_BU[ham].split("= ")[1], _tri(dap)))
        cau += MC_SA_answer_const(debai, _tri(dap), _nhieu_phu_bu(ham, dap, v), giai, _hinh_goc_bet(a), 0, dang)
    return cau


def L10_C3_B5_TH031_MC_I_02(socau, dang=1):
    r"""Có hình (thay góc bẹt của _01 bằng GÓC VUÔNG): $\widehat{xOy} = 90^{\circ}$, tia
    $Oz$ nằm giữa, $\alpha = \widehat{xOz}$, $\beta = \widehat{zOy}$ phụ nhau. Biết một
    giá trị lượng giác của $\alpha$, tìm giá trị lượng giác của $\beta$
    ($\cos\beta = \sin\alpha$, ...).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_MC_I theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, False)
        a = _goc_tu_gtlg(ham, v, tu_duoc=False)
        if not (20 <= a <= 70):
            continue
        so += 1
        hoi = _DOI_HAM[ham]
        debai = (r"In the figure shown, $\widehat{xOy} = 90^{\circ}$, ray $Oz$ lies between rays $Ox$ and $Oy$, "
                 r"$\widehat{xOz} = \alpha$, $\widehat{zOy} = \beta$. Given $\%s\alpha = %s$. The value of $\%s\beta$ equals"
                 % (ham, _tri(v), hoi))
        giai = (r"Since ray $Oz$ lies between rays $Ox$ and $Oy$, $\alpha + \beta = 90^{\circ}$, that is, "
                r"$\beta = 90^{\circ} - \alpha$." + "\\\\\n" +
                r"Hence $\%s\beta = \%s\left(90^{\circ} - \alpha\right) = \%s\alpha = %s$." % (hoi, hoi, ham, _tri(v)))
        cau += MC_SA_answer_const(debai, _tri(v), _nhieu_phu_bu(ham, v, v), giai, _hinh_goc_vuong(a), 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH031 - bản TRẢ LỜI NGẮN (số thập phân) và TỰ LUẬN của các dạng MC_G, MC_H, MC_I
# CLAUDE THEM 30/09/2026 theo cô Lan.
#   SA_D ~ MC_G (góc bù), SA_E ~ MC_H (góc phụ), SA_F ~ MC_I (có hình): cùng mô tả
#   dạng trong Mapping để bộ chọn câu không đưa cả MC lẫn SA cùng dạng vào một đề.
#   Tự luận: xem L10_C3_TH031_TH032/TH033/TH034_TL_A (ý a TH031, ý b Bài 6).
# ---------------------------------------------------------------------

_TP_SC = [Rational(k, 100) for k in range(5, 100, 5) if k != 50]
_TP_TC = [Rational(k, 10) for k in range(2, 41) if k != 10] + [Rational(k, 4) for k in (1, 3, 5, 7, 9)]


def _tp(v):
    """Số thập phân hữu hạn, dấu phẩy, bỏ số 0 thừa: 0,35; -1,5; 2."""
    s = ("%.4f" % float(v)).rstrip("0").rstrip(".")
    return s.replace(".", DAU_THAP_PHAN)


def _tp_dep(ham, am_duoc):
    """Giá trị thập phân của hàm ham; sin luôn dương, cos/tan/cot âm được nếu am_duoc."""
    v = random.choice(_TP_SC if ham in ("sin", "cos") else _TP_TC)
    if am_duoc and ham != "sin" and random.random() < 0.5:
        v = -v
    return v


def _nhieu_tp(dap):
    return _ba_nhieu(_tp(dap), [_tp(-dap), _tp(1 - dap), _tp(dap + Rational(1, 10))],
                     buoc=lambda t: _tp(dap + Rational(t, 20)))


def L10_C3_B5_TH031_SA_G_01(socau, dang=2):
    r"""Trả lời ngắn - bản số thập phân của TH031_MC_G_01: biết $\cos\alpha = -0,35$
    (hoặc sin, tan, cot), tính giá trị lượng giác cùng tên của $180^{\circ} - \alpha$.

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Dap so toi da 4 ki tu. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, True)
        dap = v if ham == "sin" else -v
        if len(_tp(dap)) > 4:
            continue
        so += 1
        debai = (r"Given an angle $\alpha$ with %s and $\%s\alpha = %s$. Calculate $\%s\left(180^{\circ} - \alpha\right)$."
                 % (_MIEN_GOC[ham], ham, _tp(v), ham))
        giai = (r"Since the angles $\alpha$ and $180^{\circ} - \alpha$ are supplementary, $%s = %s$."
                % (_BIEU_BU[ham], _tp(dap)))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_G_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi ngược: biết giá trị lượng giác của $180^{\circ} - \alpha$ (số
    thập phân), tính giá trị lượng giác cùng tên của $\alpha$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_SA_D. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, True)
        dap = v if ham == "sin" else -v
        if len(_tp(dap)) > 4:
            continue
        so += 1
        debai = (r"Given an angle $\alpha$ with %s and $\%s\left(180^{\circ} - \alpha\right) = %s$. Calculate $\%s\alpha$."
                 % (_MIEN_GOC[ham], ham, _tp(v), ham))
        giai = (r"Since the angles $\alpha$ and $180^{\circ} - \alpha$ are supplementary, $%s$, so $\%s\alpha = %s$."
                % (_BIEU_BU[ham], ham, _tp(dap)))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_H_01(socau, dang=2):
    r"""Trả lời ngắn - bản số thập phân của TH031_MC_H_01: góc nhọn $\alpha$ có
    $\sin\alpha = 0,28$, tính $\cos\left(90^{\circ} - \alpha\right)$ (và các hàm khác).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, False)
        if len(_tp(v)) > 4:
            continue
        so += 1
        debai = (r"Given an acute angle $\alpha$ with $\%s\alpha = %s$. Calculate $\%s\left(90^{\circ} - \alpha\right)$."
                 % (ham, _tp(v), _DOI_HAM[ham]))
        giai = r"Since the angles $\alpha$ and $90^{\circ} - \alpha$ are complementary, $%s = %s$." % (_BIEU_PHU[ham], _tp(v))
        cau += MC_SA_answer_const(debai, _tp(v), _nhieu_tp(v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_H_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi ngược: biết giá trị lượng giác của $90^{\circ} - \alpha$
    ($\alpha$ nhọn, số thập phân), tính giá trị lượng giác của $\alpha$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_SA_E. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, False)
        if len(_tp(v)) > 4:
            continue
        so += 1
        debai = (r"Given an acute angle $\alpha$ with $\%s\left(90^{\circ} - \alpha\right) = %s$. Calculate $\%s\alpha$."
                 % (_DOI_HAM[ham], _tp(v), ham))
        giai = (r"Since the angles $\alpha$ and $90^{\circ} - \alpha$ are complementary, $%s$, so $\%s\alpha = %s$."
                % (_BIEU_PHU[ham], ham, _tp(v)))
        cau += MC_SA_answer_const(debai, _tp(v), _nhieu_tp(v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_I_01(socau, dang=2):
    r"""Trả lời ngắn có hình (như TH031_MC_I_01): góc bẹt $\widehat{AOB}$, tia $OC$;
    biết giá trị lượng giác (số thập phân) của $\alpha = \widehat{AOC}$, tính của
    $\beta = \widehat{BOC}$.

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, True)
        dap = v if ham == "sin" else -v
        a = _goc_tu_gtlg(ham, v)
        if len(_tp(dap)) > 4 or not (20 <= a <= 160) or abs(a - 90) < 10:
            continue
        so += 1
        debai = (r"In the figure shown, the points $A$, $O$, $B$ are collinear, $\widehat{AOC} = \alpha$, "
                 r"$\widehat{BOC} = \beta$. Given $\%s\alpha = %s$. Calculate $\%s\beta$." % (ham, _tp(v), ham))
        giai = (r"Since $A$, $O$, $B$ are collinear, $\beta = 180^{\circ} - \alpha$." + "\\\\\n" +
                r"Hence $\%s\beta = %s = %s$." % (ham, _BIEU_BU[ham].split("= ")[1], _tp(dap)))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, _hinh_goc_bet(a), 0, dang)
    return cau


def L10_C3_B5_TH031_SA_I_02(socau, dang=2):
    r"""Trả lời ngắn có hình (như TH031_MC_I_02): góc vuông $\widehat{xOy}$, tia $Oz$
    nằm giữa; biết giá trị lượng giác của $\alpha = \widehat{xOz}$, tính của $\beta = \widehat{zOy}$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH031_SA_F. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, False)
        a = _goc_tu_gtlg(ham, v, tu_duoc=False)
        if len(_tp(v)) > 4 or not (20 <= a <= 70):
            continue
        so += 1
        hoi = _DOI_HAM[ham]
        debai = (r"In the figure shown, $\widehat{xOy} = 90^{\circ}$, ray $Oz$ lies between rays $Ox$ and $Oy$, "
                 r"$\widehat{xOz} = \alpha$, $\widehat{zOy} = \beta$. Given $\%s\alpha = %s$. Calculate $\%s\beta$."
                 % (ham, _tp(v), hoi))
        giai = (r"Since ray $Oz$ lies between rays $Ox$ and $Oy$, $\beta = 90^{\circ} - \alpha$." + "\\\\\n" +
                r"Hence $\%s\beta = \%s\left(90^{\circ} - \alpha\right) = \%s\alpha = %s$." % (hoi, hoi, ham, _tp(v)))
        cau += MC_SA_answer_const(debai, _tp(v), _nhieu_tp(v), giai, _hinh_goc_vuong(a), 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH031 - biến thể TRONG TAM GIÁC của các dạng góc bù / góc phụ (theo cô Lan 30/09/2026)
#   MC_G_03, SA_D_03: tam giác ABC biết GTLG của (A + B) -> GTLG của C (bù nhau)
#   MC_H_03, SA_E_03: tam giác ABC vuông tại A biết GTLG của B (hoặc C) -> GTLG của góc kia
# ---------------------------------------------------------------------

def _tam_giac_bu(ham):
    """(X, tổng hai góc còn lại, dấu): ham(Y + Z) = dấu * ham(X) vì Y + Z = 180° - X."""
    X, Y, Z = random.sample("ABC", 3)
    tong = r"%s + %s" % tuple(sorted([Y, Z]))
    return X, tong, (1 if ham == "sin" else -1)


def _giai_tam_giac_bu(ham, X, tong, cho_tong, dap_tex):
    bt = r"\%s\left(%s\right) = %s\%s %s" % (ham, tong, "" if ham == "sin" else "-", ham, X)
    hoi = (r"\%s %s" % (ham, X)) if cho_tong else (r"\%s\left(%s\right)" % (ham, tong))
    return (r"Since $A + B + C = 180^{\circ}$, $%s = 180^{\circ} - %s$, so the angles $%s$ and $%s$ are supplementary."
            % (tong, X, tong, X) + "\\\\\n" + r"Hence $%s$, which gives $%s = %s$." % (bt, hoi, dap_tex))


def L10_C3_B5_TH031_MC_G_03(socau, dang=1):
    r"""Biến thể TRONG TAM GIÁC của TH031_MC_G: tam giác $ABC$ biết một giá trị lượng
    giác của $A + B$ (số đẹp, vd $\cos\left(A + B\right) = -\dfrac{1}{5}$), tìm giá trị
    lượng giác cùng tên của $C$ (hoặc ngược lại). Cặp góc, hàm chọn ngẫu nhiên.

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH031_MC_G theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, True)
        X, tong, dau = _tam_giac_bu(ham)
        dap = dau * v
        cho_tong = random.random() < 0.7
        cho, hoi = ((r"\%s\left(%s\right)" % (ham, tong), r"\%s %s" % (ham, X)) if cho_tong
                    else (r"\%s %s" % (ham, X), r"\%s\left(%s\right)" % (ham, tong)))
        debai = r"Given triangle $ABC$ with $%s = %s$. The value of $%s$ equals" % (cho, _tri(v), hoi)
        giai = _giai_tam_giac_bu(ham, X, tong, cho_tong, _tri(dap))
        cau += MC_SA_answer_const(debai, _tri(dap), _nhieu_phu_bu(ham, dap, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_G_03(socau, dang=2):
    r"""Trả lời ngắn - biến thể trong tam giác của SA_D: biết giá trị lượng giác của
    $A + B$ (số thập phân), tính giá trị lượng giác cùng tên của $C$ (hoặc ngược lại).

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH031_SA_D theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, True)
        X, tong, dau = _tam_giac_bu(ham)
        dap = dau * v
        if len(_tp(dap)) > 4:
            continue
        so += 1
        cho_tong = random.random() < 0.7
        cho, hoi = ((r"\%s\left(%s\right)" % (ham, tong), r"\%s %s" % (ham, X)) if cho_tong
                    else (r"\%s %s" % (ham, X), r"\%s\left(%s\right)" % (ham, tong)))
        debai = r"Given triangle $ABC$ with $%s = %s$. Calculate $%s$." % (cho, _tp(v), hoi)
        giai = _giai_tam_giac_bu(ham, X, tong, cho_tong, _tp(dap))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, 0, 0, dang)
    return cau


def _giai_tam_giac_vuong(Y, Z, ham, dap_tex):
    hoi = _DOI_HAM[ham]
    return (r"Since triangle $ABC$ is right-angled at $A$, $\widehat{B} + \widehat{C} = 90^{\circ}$, so the angles $B$ and $C$ "
            r"are complementary." + "\\\\\n" + r"Hence $\%s %s = \%s %s = %s$." % (hoi, Z, ham, Y, dap_tex))


def L10_C3_B5_TH031_MC_H_03(socau, dang=1):
    r"""Biến thể TRONG TAM GIÁC VUÔNG của TH031_MC_H: tam giác $ABC$ vuông tại $A$, biết
    một giá trị lượng giác của góc $B$ (hoặc $C$, chọn ngẫu nhiên) là số đẹp, tìm giá trị
    lượng giác của góc còn lại ($\cos C = \sin B$, $\cot C = \tan B$, ...).
    (Khác TH031_MC_F_02: F_02 chỉ dùng bộ ba Py-ta-go và có câu phải tính thêm bằng
    $\sin^2 + \cos^2 = 1$; H_03 chỉ dùng quan hệ hai góc phụ nhau.)

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH031_MC_H theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ham = random.choice(_HAM4)
        v = _gtlg_dep(ham, False)
        Y, Z = random.sample("BC", 2)
        debai = (r"Given triangle $ABC$ right-angled at $A$ with $\%s %s = %s$. The value of $\%s %s$ equals"
                 % (ham, Y, _tri(v), _DOI_HAM[ham], Z))
        giai = _giai_tam_giac_vuong(Y, Z, ham, _tri(v))
        cau += MC_SA_answer_const(debai, _tri(v), _nhieu_phu_bu(ham, v, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_H_03(socau, dang=2):
    r"""Trả lời ngắn - biến thể trong tam giác vuông của SA_E: tam giác $ABC$ vuông tại
    $A$ biết giá trị lượng giác (số thập phân) của $B$ hoặc $C$, tính của góc còn lại.

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH031_SA_E theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ham = random.choice(_HAM4)
        v = _tp_dep(ham, False)
        if len(_tp(v)) > 4:
            continue
        so += 1
        Y, Z = random.sample("BC", 2)
        debai = (r"Given triangle $ABC$ right-angled at $A$ with $\%s %s = %s$. Calculate $\%s %s$."
                 % (ham, Y, _tp(v), _DOI_HAM[ham], Z))
        giai = _giai_tam_giac_vuong(Y, Z, ham, _tp(v))
        cau += MC_SA_answer_const(debai, _tp(v), _nhieu_tp(v), giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TỰ LUẬN hai ý hai đơn vị kiến thức (theo cô Lan 30/09/2026):
#   ý a) quan hệ góc bù / góc phụ trong tam giác (TH031, Bài 5)
#   ý b) một phép tính đơn giản bằng hệ thức lượng trong tam giác (Bài 6):
#        định lí côsin (TH032), định lí sin (TH033), công thức diện tích (TH034).
# ID ghi CẢ HAI đơn vị (như câu Đúng/Sai, theo chương, không ghi bài):
#   L10_C3_TH031_TH032_TL_A = ý a) TH031, ý b) TH032. Ma trận tính theo TỪNG Ý
#   (mỗi ý một suất ở đúng mức độ, đơn vị của nó) - xem docs/04 Ngoại lệ 3.
# ---------------------------------------------------------------------

_PS_TL = [Rational(p, q) for q in range(3, 9) for p in range(1, q) if math.gcd(p, q) == 1]
# (cos C, a, b, c) với c^2 = a^2 + b^2 - 2ab cos C là số chính phương: cạnh thứ ba nguyên (mức TH)
_BO_COSIN_TL = [(c_, m_, n_, math.isqrt(int(m_ * m_ + n_ * n_ - 2 * m_ * n_ * c_)))
                for c_ in [s_ * Rational(p, q) for q in range(2, 9) for p in range(1, q)
                           if math.gcd(p, q) == 1 for s_ in (1, -1)]
                for m_ in range(2, 11) for n_ in range(m_ + 1, 11)
                if (m_ * m_ + n_ * n_ - 2 * m_ * n_ * c_).q == 1
                and math.isqrt(int(m_ * m_ + n_ * n_ - 2 * m_ * n_ * c_)) ** 2 == m_ * m_ + n_ * n_ - 2 * m_ * n_ * c_]


def _tam_giac_ba_dinh():
    """(X, Y, Z, tổng): góc X, hai góc còn lại Y + Z = 180° - X."""
    X, Y, Z = random.sample("ABC", 3)
    Y, Z = sorted([Y, Z])
    return X, Y, Z, r"%s + %s" % (Y, Z)


def _canh(P, Q):
    return "".join(sorted([P, Q]))


def L10_C3_TH031_TH032_TL_A_01(socau, dong=1):
    r"""Tự luận: tam giác $ABC$ biết $\cos\left(A + B\right)$ (số đẹp) và hai cạnh kề góc $C$.
    a) Tính $\cos C$ (hai góc bù nhau - TH031).
    b) Tính cạnh $AB$ bằng định lí côsin (TH032).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan (y a TH031, y b TH032). Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        # muc TH: chon san bo (cos C, a, b) de canh thu ba la SO NGUYEN
        cX, m_, n_, _ = random.choice(_BO_COSIN_TL)
        if random.random() < 0.5:
            m_, n_ = n_, m_
        v = -cX
        X, Y, Z, tong = _tam_giac_ba_dinh()
        c2 = m_ ** 2 + n_ ** 2 - 2 * m_ * n_ * cX
        so += 1
        XY, XZ, YZ = _canh(X, Y), _canh(X, Z), _canh(Y, Z)
        debai = (r"Triangle $ABC$ has $%s = %d$, $%s = %d$ and $\cos\left(%s\right) = %s$."
                 % (XY, m_, XZ, n_, tong, _tri(v)))
        ds = [(r"Calculate $\cos %s$." % X, r"\cos %s = %s" % (X, _tri(cX)),
               r"Since $A + B + C = 180^{\circ}$, $%s = 180^{\circ} - %s$, so the two angles are supplementary. Therefore "
               r"$\cos %s = -\cos\left(%s\right) = %s$." % (tong, X, X, tong, _tri(cX))),
              (r"Find the length of side $%s$." % YZ, r"%s = %s" % (YZ, _tri(sqrt(c2))),
               r"By the law of cosines, $%s^{2} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot\cos %s "
               r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %s$." % (
                   YZ, XY, XZ, XY, XZ, X, m_, n_, m_, n_, _ngoac(cX), _tri(c2)) + "\\\\\n" +
               r"Hence $%s = %s$." % (YZ, _tri(sqrt(c2))))]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


def L10_C3_TH031_TH033_TL_A_01(socau, dong=1):
    r"""Tự luận: tam giác $ABC$ biết $\sin\left(A + B\right)$ (số đẹp) và cạnh $AB$.
    a) Tính $\sin C$ (hai góc bù nhau - TH031).
    b) Tính bán kính $R$ đường tròn ngoại tiếp bằng định lí sin (TH033).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan (y a TH031, y b TH033). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        v = random.choice(_PS_TL)
        X, Y, Z, tong = _tam_giac_ba_dinh()
        YZ = _canh(Y, Z)
        a_ = 2 * v.p * random.randint(1, 4)
        R = a_ / (2 * v)
        debai = (r"Triangle $ABC$ has $%s = %d$ and $\sin\left(%s\right) = %s$."
                 % (YZ, a_, tong, _tri(v)))
        ds = [(r"Calculate $\sin %s$." % X, r"\sin %s = %s" % (X, _tri(v)),
               r"Since $A + B + C = 180^{\circ}$, $%s = 180^{\circ} - %s$, so the two angles are supplementary. Therefore "
               r"$\sin %s = \sin\left(%s\right) = %s$." % (tong, X, X, tong, _tri(v))),
              (r"Calculate the circumradius $R$ of triangle $ABC$.", r"R = %s" % _tri(R),
               r"By the law of sines, $\dfrac{%s}{\sin %s} = 2R$, so $R = \dfrac{%s}{2\sin %s} "
               r"= \dfrac{%d}{2\cdot %s} = %s$." % (YZ, X, YZ, X, a_, _tri(v), _tri(R)))]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


def L10_C3_TH031_TH033_TL_A_02(socau, dong=1):
    r"""Tự luận: tam giác $ABC$ VUÔNG tại $A$, biết cạnh huyền $BC$ và côsin của một góc
    nhọn (số đẹp).
    a) Tính sin của góc nhọn còn lại (hai góc phụ nhau - TH031).
    b) Tính cạnh đối diện góc đó bằng định lí sin (TH033).

    CLAUDE THEM 30/09/2026 - bien the 02 cua L10_C3_TH031_TH033_TL_A theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        v = random.choice(_PS_TL)
        Y, Z = random.sample("BC", 2)             # cho cos Z, hoi sin Y
        a_ = v.q * random.randint(1, 4)
        doi = _canh("A", Z)                        # canh doi dien goc Y
        canh = a_ * v
        debai = r"Triangle $ABC$ is right-angled at $A$ with $BC = %d$ and $\cos %s = %s$." % (a_, Z, _tri(v))
        ds = [(r"Calculate $\sin %s$." % Y, r"\sin %s = %s" % (Y, _tri(v)),
               r"Since triangle $ABC$ is right-angled at $A$, $\widehat{B} + \widehat{C} = 90^{\circ}$, so the two angles are complementary. "
               r"Therefore $\sin %s = \cos %s = %s$." % (Y, Z, _tri(v))),
              (r"Find the length of side $%s$." % doi, r"%s = %s" % (doi, _tri(canh)),
               r"By the law of sines, $\dfrac{%s}{\sin %s} = \dfrac{BC}{\sin A}$, where $\sin A = \sin 90^{\circ} = 1$, "
               r"so $%s = BC\cdot\sin %s = %d\cdot %s = %s$." % (doi, Y, doi, Y, a_, _tri(v), _tri(canh)))]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


def L10_C3_TH031_TH034_TL_A_01(socau, dong=1):
    r"""Tự luận: tam giác $ABC$ biết $\sin\left(A + B\right)$ (số đẹp) và hai cạnh kề góc $C$.
    a) Tính $\sin C$ (hai góc bù nhau - TH031).
    b) Tính diện tích tam giác bằng $S = \dfrac{1}{2}ab\sin C$ (TH034).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan (y a TH031, y b TH034). Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        v = random.choice(_PS_TL)
        X, Y, Z, tong = _tam_giac_ba_dinh()
        m_, n_ = random.randint(2, 12), random.randint(2, 12)
        S = Rational(m_ * n_, 2) * v
        if S.q != 1 or m_ == n_:
            continue
        so += 1
        XY, XZ = _canh(X, Y), _canh(X, Z)
        debai = (r"Triangle $ABC$ has $%s = %d$, $%s = %d$ and $\sin\left(%s\right) = %s$."
                 % (XY, m_, XZ, n_, tong, _tri(v)))
        ds = [(r"Calculate $\sin %s$." % X, r"\sin %s = %s" % (X, _tri(v)),
               r"Since $A + B + C = 180^{\circ}$, $%s = 180^{\circ} - %s$, so the two angles are supplementary. Therefore "
               r"$\sin %s = \sin\left(%s\right) = %s$." % (tong, X, X, tong, _tri(v))),
              (r"Calculate the area of triangle $ABC$.", r"S = %s" % _tri(S),
               r"$S = \dfrac{1}{2}\cdot %s\cdot %s\cdot\sin %s = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$."
               % (XY, XZ, X, m_, n_, _tri(v), _tri(S)))]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


# =====================================================================
# VD036 - hai bài toán thực tế cô Lan gửi 30/09/2026. SỐ LIỆU CHỌN TRƯỚC sao
# cho đáp số làm tròn không sát ranh giới (_xa_bien) và hợp lí rồi mới ra đề.
#  1) Sườn đồi độ dốc p% (tang góc dốc), cây mọc thẳng đứng; từ chân đồi cách
#     gốc cây d m nhìn ngọn cây dưới góc beta so với phương nằm ngang.
#     MC_E_01, SA_G_01 (chiều cao cây), TL_F_01 (a) góc dốc, b) chiều cao).
#  2) Tàu chạy d1 km theo một phương (đông/tây/nam/bắc) rồi đổi sang hướng
#     X theta Y chạy d2 km: khoảng cách AC và hướng từ A tới C.
#     MC_C_03, SA_F_01 (hỏi ngẫu nhiên AC hoặc hướng), TL_D_03 (a) AC, b) hướng).
# =====================================================================

def _bo_suon_doi():
    """(p, d, beta, alpha, h): độ dốc p%, AB = d (m) dọc sườn đồi, góc nhìn beta."""
    while True:
        p = random.choice([8, 10, 12, 15, 18, 20, 25])
        d = random.choice([20, 24, 25, 30, 35, 40, 45, 50])
        be = random.choice([35, 40, 45, 50, 55, 60])
        al = math.degrees(math.atan(p / 100))
        if be - al < 20:
            continue
        h = d * math.sin(math.radians(be - al)) / math.cos(math.radians(be))
        if h < 5 or not _xa_bien(h) or not _xa_bien(al, 1):
            continue
        return p, d, be, al, h


def _hinh_suon_doi(al, be):
    """Sườn đồi AB (vẽ dốc hơn thật cho dễ nhìn), cây BC thẳng đứng, tia AC."""
    a_v = min(max(al * 1.8, 10), 22)             # góc dốc khi vẽ
    L = 3.2
    bx, by = L * math.cos(math.radians(a_v)), L * math.sin(math.radians(a_v))
    cy = bx * math.tan(math.radians(be))
    return (
        "\\begin{tikzpicture}[scale=0.95,font=\\footnotesize]\n"
        "\\coordinate (A) at (0,0);\n\\coordinate (B) at (%.2f,%.2f);\n\\coordinate (C) at (%.2f,%.2f);\n"
        % (bx, by, bx, cy)
        + "\\draw[dashed] (A) -- (%.2f,0);\n" % (bx + 0.8)
        + "\\draw[thick] (A) -- (%.2f,%.2f);\n" % (bx + 0.8, by + 0.8 * math.tan(math.radians(a_v)))
        + "\\draw[thick,green!50!black] (B) -- (C);\n\\draw (A) -- (C);\n"
        "\\draw (1.4,0) arc (0:%.1f:1.4);\n" % a_v
        + "\\node at (%.1f:1.75) {$\\alpha$};\n" % (a_v / 2)
        + "\\draw (0.5,0) arc (0:%.1f:0.5);\n" % be
        + "\\node at (%.1f:0.85) {$%d^{\\circ}$};\n" % (max(be * 0.6, a_v + 14), be)
        + "\\fill (A) circle (0.04) node[below left] {$A$};\n"
        "\\fill (B) circle (0.04) node[below right] {$B$};\n"
        "\\fill (C) circle (0.04) node[above] {$C$};\n"
        "\\end{tikzpicture}"
    )


def _de_suon_doi(p, d, be):
    return (r"On a hillside with a gradient of $%d\%%$ (the gradient of a hillside is measured by the tangent of the angle between "
            r"the hillside and the horizontal) there is a tree $BC$ growing vertically ($B$ is the base of the tree). At the foot of the "
            r"hill, at a point $A$ that is $%d\,\text{m}$ from the base of the tree, the top of the tree is seen at an angle of $%s$ to the "
            r"horizontal (as shown in the figure)." % (p, d, _goc(be)))


def _giai_suon_doi(p, d, be, al, h):
    return (r"Let $\alpha$ be the angle between the hillside and the horizontal: $\tan\alpha = %s$, so "
            r"$\alpha \approx %s^{\circ}$." % (_xx(p / 100), _x1(al)) + "\\\\\n" +
            r"In triangle $ABC$: $\widehat{BAC} = %s - \alpha$, $\widehat{ABC} = 90^{\circ} + \alpha$ "
            r"(the tree is vertical), $\widehat{ACB} = 180^{\circ} - \widehat{BAC} - \widehat{ABC} = 90^{\circ} - %s = %s$."
            % (_goc(be), _goc(be), _goc(90 - be)) + "\\\\\n" +
            r"Law of sines: $BC = \dfrac{AB\cdot\sin\widehat{BAC}}{\sin\widehat{ACB}} = "
            r"\dfrac{%d\cdot\sin\left(%s - \alpha\right)}{\sin %s} \approx %s\,\text{m}$."
            % (d, _goc(be), _goc(90 - be), _xx(h, 2)))


def L10_C3_B6_VD036_MC_E_01(socau, dang=1):
    r"""Sườn đồi độ dốc $p\%$ (tang góc dốc), cây mọc thẳng đứng trên sườn đồi; từ
    chân đồi cách gốc cây $d$ m nhìn ngọn cây dưới góc $\beta$. Tính chiều cao cây
    (làm tròn đến hàng đơn vị) - có hình.

    CLAUDE THEM 30/09/2026 - dang moi theo bai co Lan gui (do doc 12%, 30 m, 45 do).
    So lieu chon truoc de dap so khong sat ranh gioi lam tron. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        p, d, be, al, h = _bo_suon_doi()
        a_r = math.radians(al)
        dap = str(_lt(h))
        nhieu = _ba_nhieu(dap, [str(_lt(d * math.tan(math.radians(be)))),                     # bỏ qua độ dốc
                                str(_lt(d * math.cos(a_r) * math.tan(math.radians(be)))),       # quên trừ độ cao gốc cây
                                str(_lt(d * math.sin(math.radians(be + al)) / math.cos(math.radians(be)))),  # sai dấu
                                str(_lt(h) + 2)],
                          buoc=lambda t: str(_lt(h) + t))
        debai = _de_suon_doi(p, d, be) + r" The height of the tree (rounded to the nearest whole number, in meters) is"
        giai = _giai_suon_doi(p, d, be, al, h) + "\\\\\n" + r"Hence the tree is about $%s\,\text{m}$ tall." % dap
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_suon_doi(al, be), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_E_01(socau, dang=2):
    r"""Trả lời ngắn - sườn đồi độ dốc $p\%$, cây mọc thẳng đứng: tính chiều cao của
    cây (làm tròn đến hàng đơn vị) - có hình.

    CLAUDE THEM 30/09/2026 - dang moi theo bai co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        p, d, be, al, h = _bo_suon_doi()
        dap = str(_lt(h))
        debai = _de_suon_doi(p, d, be) + r" Find the height of the tree (rounded to the nearest whole number, in meters)."
        giai = _giai_suon_doi(p, d, be, al, h) + "\\\\\n" + r"Hence the tree is about $%s\,\text{m}$ tall." % dap
        cau += MC_SA_answer_const(debai, dap, [str(_lt(h) + k) for k in (1, -1, 2)], giai,
                                  _hinh_suon_doi(al, be), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_F_01(socau, dong=1):
    r"""Tự luận - sườn đồi độ dốc $p\%$, cây mọc thẳng đứng (có hình).
    a) (VD) Tính góc tạo bởi sườn đồi với phương nằm ngang (làm tròn đến hàng phần mười của độ).
    b) (VDC) Tính chiều cao của cây (làm tròn đến hàng đơn vị, theo đơn vị mét).

    CLAUDE THEM 30/09/2026 - dang moi theo bai co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        p, d, be, al, h = _bo_suon_doi()
        debai = _de_suon_doi(p, d, be)
        ds = [(r"Find the angle between the hillside and the horizontal (round to the nearest tenth of a degree).",
               r"\alpha \approx %s^{\circ}" % _x1(al),
               r"Let $\alpha$ be the angle between the hillside and the horizontal. Since the gradient is $%d\%%$, "
               r"$\tan\alpha = %s$, so $\alpha \approx %s^{\circ}$." % (p, _xx(p / 100), _x1(al))),
              (r"Find the height of the tree (rounded to the nearest whole number, in meters).",
               r"BC \approx %d\,\text{m}" % _lt(h),
               r"In triangle $ABC$: $\widehat{BAC} = %s - \alpha$, $\widehat{ABC} = 90^{\circ} + \alpha$, "
               r"$\widehat{ACB} = 90^{\circ} - %s = %s$.\\ Law of sines: $BC = \dfrac{AB\cdot\sin\widehat{BAC}}"
               r"{\sin\widehat{ACB}} = \dfrac{%d\cdot\sin\left(%s - \alpha\right)}{\sin %s} \approx %s$, "
               r"that is, the tree is about $%d\,\text{m}$ tall." % (_goc(be), _goc(be), _goc(90 - be), d, _goc(be),
                                                         _goc(90 - be), _xx(h, 2), _lt(h)))]
        cau += TL_answer_text(debai, ds, _hinh_suon_doi(al, be), 0, dong)
    return cau


_PHUONG = {"E": "east", "W": "west", "N": "north", "S": "south"}
_VUONG_GOC = {"E": "NS", "W": "NS", "N": "EW", "S": "EW"}


def _huong_la_ban(X, g, Y):
    """Hướng kiểu E 30° S: từ phương X quay về phía Y một góc g."""
    return r"$\mathrm{%s}\,%d^{\circ}\,\mathrm{%s}$" % (X, g, Y)


def _bo_tau_doi_huong():
    """(X, Y, theta, d1, d2, AC, phi): tàu chạy d1 km về phương X tới B, đổi sang
    hướng X theta Y chạy d2 km tới C; AC và góc phi = BAC (hướng AC là X phi Y)."""
    while True:
        X = random.choice("EWNS")
        Y = random.choice(_VUONG_GOC[X])
        th = random.choice([20, 25, 30, 35, 40, 45, 50, 55, 60])
        d1, d2 = random.randint(6, 30), random.randint(6, 30)
        AC = math.sqrt(d1 * d1 + d2 * d2 + 2 * d1 * d2 * math.cos(math.radians(th)))
        phi = math.degrees(math.asin(d2 * math.sin(math.radians(th)) / AC))
        if not _xa_bien(AC) or not _xa_bien(phi) or not (1 <= _lt(phi) < th):
            continue
        return X, Y, th, d1, d2, AC, phi


def _de_tau(X, Y, th, d1, d2):
    return (r"At sea, a fishing boat leaves port $A$ and travels %s for $%d\,\text{km}$ to $B$, then changes "
            r"to the heading %s and travels another $%d\,\text{km}$ to island $C$." % (_PHUONG[X], d1, _huong_la_ban(X, th, Y), d2))


def _giai_tau_AC(X, Y, th, d1, d2, AC):
    return (r"The boat travels %s and then turns toward the %s through an angle of $%s$, so $\widehat{ABC} = 180^{\circ} - %s = %s$."
            % (_PHUONG[X], _PHUONG[Y], _goc(th), _goc(th), _goc(180 - th)) + "\\\\\n" +
            r"Law of cosines: $AC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s \approx %s$, so "
            r"$AC \approx %s\,\text{km}$." % (d1, d2, d1, d2, _goc(180 - th), _xx(AC * AC, 2), _xx(AC, 2)))


def _giai_tau_huong(X, Y, th, d2, AC, phi):
    return (r"Law of sines: $\sin\widehat{BAC} = \dfrac{BC\cdot\sin\widehat{ABC}}{AC} = "
            r"\dfrac{%d\cdot\sin %s}{AC} \approx %s$, and since $\widehat{BAC}$ is acute, $\widehat{BAC} \approx %s$."
            % (d2, _goc(180 - th), _xx(math.sin(math.radians(phi)), 4), _goc(_lt(phi))) + "\\\\\n" +
            r"Ray $AB$ points %s and point $C$ lies toward the %s, so the direction from $A$ to $C$ is %s."
            % (_PHUONG[X], _PHUONG[Y], _huong_la_ban(X, _lt(phi), Y)))


def L10_C3_B6_VD036_MC_C_03(socau, dang=1):
    r"""Tàu chạy $d_1$ km về một phương (đông/tây/nam/bắc) rồi đổi sang hướng
    $X\,\theta^{\circ}\,Y$ chạy $d_2$ km: hỏi khoảng cách $AC$ (hàng đơn vị) - mức VD.
    Câu hỏi hướng từ $A$ tới $C$ (mức VDC) tách sang VD036_MC_M_01 (01/10/2026).

    CLAUDE THEM 30/09/2026 - bien the 03 cua VD036_MC_C theo bai co Lan gui (dong
    15 km, E30S 20 km). So lieu chon truoc. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        dap = str(_lt(AC))
        nhieu = _ba_nhieu(dap, [str(_lt(math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * math.cos(math.radians(th))))),
                                str(_lt(math.sqrt(d1 * d1 + d2 * d2))), str(d1 + d2)],
                          buoc=lambda t: str(_lt(AC) + t))
        debai = _de_tau(X, Y, th, d1, d2) + (r" The distance from $A$ to $C$ (rounded to the nearest whole number, in "
                                             r"kilometers) is")
        giai = _giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + r"Hence $AC \approx %s\,\text{km}$." % dap
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_MC_M_01(socau, dang=1):
    r"""Tàu chạy $d_1$ km về một phương rồi đổi sang hướng $X\,\theta^{\circ}\,Y$ chạy $d_2$ km:
    xác định hướng từ $A$ tới $C$ (côsin rồi sin) - mức VDC (muc_do_dang VDC ở mapping).

    CLAUDE THEM 01/10/2026 - tach tu nhanh hoi huong cua VD036_MC_C_03. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        g = _lt(phi)
        Z = [c for c in _VUONG_GOC[X] if c != Y][0]
        dung = _huong_la_ban(X, g, Y)
        ung = [_huong_la_ban(X, g, Z), _huong_la_ban(X, th, Y), _huong_la_ban(X, th - g, Y)]
        nhieu = [u for u in dict.fromkeys(ung) if u != dung][:3]
        if len(nhieu) < 3:
            nhieu.append(_huong_la_ban(X, g + 5, Y))
        debai = _de_tau(X, Y, th, d1, d2) + (r" The direction from $A$ to $C$ (angle measure rounded to the nearest whole number) is")
        giai = _giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + _giai_tau_huong(X, Y, th, d2, AC, phi)
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_C_03(socau, dang=2):
    r"""Trả lời ngắn - tàu chạy $d_1$ km về một phương rồi đổi sang hướng
    $X\,\theta^{\circ}\,Y$ chạy $d_2$ km: tính khoảng cách $AC$ (km, hàng đơn vị) - mức VD.
    Câu hỏi hướng (mức VDC) tách sang VD036_SA_O_01 (01/10/2026).

    CLAUDE THEM 30/09/2026 - dang moi theo bai co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        dap = str(_lt(AC))
        debai = _de_tau(X, Y, th, d1, d2) + (r" Find the distance from $A$ to $C$ (rounded to the nearest whole number, "
                                             r"in kilometers).")
        giai = _giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + r"Hence $AC \approx %s\,\text{km}$." % dap
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_M_01(socau, dang=2):
    r"""Trả lời ngắn - tàu đổi hướng: tìm số đo $x$ trong hướng $X\,x^{\circ}\,Y$ từ $A$ tới $C$
    (côsin rồi sin) - mức VDC (muc_do_dang VDC ở mapping).

    CLAUDE THEM 01/10/2026 - tach tu nhanh hoi huong cua VD036_SA_F_01. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        dap = str(_lt(phi))
        debai = _de_tau(X, Y, th, d1, d2) + (r" The direction from $A$ to $C$ is $\mathrm{%s}\,x^{\circ}\,\mathrm{%s}$. "
                                             r"Find $x$ (round to the nearest whole number)." % (X, Y))
        giai = (_giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + _giai_tau_huong(X, Y, th, d2, AC, phi)
                + " Hence $x = %s$." % dap)
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_TL_D_03(socau, dong=1):
    r"""Tự luận - tàu chạy $d_1$ km về một phương rồi đổi sang hướng $X\,\theta^{\circ}\,Y$
    chạy $d_2$ km.
    a) (VD) Tính khoảng cách từ $A$ đến $C$ (hàng đơn vị, km).
    b) (VDC) Xác định hướng từ $A$ tới $C$ (hàng đơn vị, độ).

    CLAUDE THEM 30/09/2026 - bien the 03 cua VD036_TL_D theo bai co Lan gui (dong 15 km,
    E30S 20 km); so lieu, huong chon truoc de dap so hop li. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        ds = [(r"Find the distance from $A$ to $C$ (rounded to the nearest whole number, in kilometers).",
               r"AC \approx %d\,\text{km}" % _lt(AC),
               _giai_tau_AC(X, Y, th, d1, d2, AC) + r" Hence $AC \approx %d\,\text{km}$." % _lt(AC)),
              (r"Determine the direction from $A$ to $C$ (rounded to the nearest whole number, in degrees).",
               r"\mathrm{%s}\,%d^{\circ}\,\mathrm{%s}" % (X, _lt(phi), Y),
               _giai_tau_huong(X, Y, th, d2, AC, phi))]
        cau += TL_answer_text(_de_tau(X, Y, th, d1, d2), ds, 0, 0, dong)
    return cau


# =====================================================================
# VD036 - VẬN DỤNG CAO (cô Lan 30/09/2026): hai người quan sát P, Q trên sườn đồi
# nghiêng s độ, cùng nhìn khinh khí cầu O dưới các góc a (tại P), b (tại Q) so với
# phương nằm ngang, PQ = d m dọc sườn đồi. Hỏi khoảng cách từ P (hoặc Q) tới O.
#   OPQ = a - s, OQP = 180 - (b - s), POQ = b - a; định lí sin.
# Mapping đánh dấu "muc_do_dang": "VDC" - bộ chọn câu dùng cho suất VDC trước.
# MC_F_01, SA_H_01, TL_G_01 cùng mô tả dạng -> không ra hai câu cùng bối cảnh
# trong một đề (trừ khi không còn dạng nào khác).
# =====================================================================

def _bo_khinh_khi_cau():
    """(s, a, b, d, OP, OQ) chọn trước: góc hợp lí, khoảng cách không quá xa, đáp số
    không sát ranh giới làm tròn."""
    while True:
        s = random.randint(15, 35)
        a = random.randint(s + 15, 75)
        b = a + random.randint(6, 15)
        if b > 85:
            continue
        d = random.choice([30, 40, 50, 60, 80, 100])
        O = b - a
        OP = d * _sin_d(180 - b + s) / _sin_d(O)
        OQ = d * _sin_d(a - s) / _sin_d(O)
        if not (40 <= OQ <= 800 and 40 <= OP <= 800) or not _xa_bien(OP) or not _xa_bien(OQ):
            continue
        return s, a, b, d, OP, OQ


def _hinh_khinh_khi_cau(s, d):
    """Hình minh hoạ (không đúng tỉ lệ): sườn đồi nghiêng s độ, P, Q trên sườn, khinh khí cầu O."""
    t = math.tan(math.radians(s))
    Bx = 3.0
    P, Q = (1.0, 1.0 * t), (2.3, 2.3 * t)
    return (
        "\\begin{tikzpicture}[scale=1.2,font=\\footnotesize]\n"
        "\\fill[black!15] (0,0) -- (%.2f,%.2f) -- (%.2f,0) -- cycle;\n" % (Bx, Bx * t, Bx)
        + "\\draw[very thick] (-0.8,0) -- (%.2f,0);\n" % (Bx + 0.3)
        + "\\draw[thick] (0,0) -- (%.2f,%.2f);\n" % (Bx, Bx * t)
        + "\\coordinate (O) at (2.6,3.3);\n\\coordinate (P) at (%.2f,%.2f);\n\\coordinate (Q) at (%.2f,%.2f);\n"
        % (P + Q)
        + "\\draw[dashed] (P) -- (O) (Q) -- (O);\n"
        "\\draw (0.6,0) arc (0:%.1f:0.6);\n\\node at (%.1f:0.9) {$%d^{\\circ}$};\n" % (s, s / 2, s)
        + "\\node[below right] at (%.2f,%.2f) {$%d$ m};\n" % ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2, d)
        + "\\fill (P) circle (0.04) node[above left] {$P$};\n"
        "\\fill (Q) circle (0.04) node[above left] {$Q$};\n"
        "\\fill[yellow!80!orange] (2.6,3.62) circle (0.25);\n"
        "\\draw (2.6,3.62) circle (0.25);\n"
        "\\draw (2.38,3.5) -- (2.52,3.3) (2.82,3.5) -- (2.68,3.3);\n"
        "\\fill[brown] (2.52,3.2) rectangle (2.68,3.3);\n"
        "\\node[right] at (2.9,3.4) {$O$};\n"
        "\\end{tikzpicture}"
    )


def _de_khinh_khi_cau(s, a, b, d):
    return (r"Two observers at $P$ and $Q$ stand on the slope of a hill inclined at $%s$ to the horizontal "
            r"plane, as shown in the figure. The observer at $P$ sees a hot-air balloon (point $O$) at an angle of "
            r"$%s$ to the horizontal. At the same time, the observer at $Q$ sees the balloon at an "
            r"angle of $%s$ to the horizontal. The distance between $P$ and $Q$ along the slope is $%d\,\text{m}$."
            % (_goc(s), _goc(a), _goc(b), d))


def _giai_goc_khinh_khi_cau(s, a, b):
    return (r"Let $A$ be the intersection of line $PQ$ with the horizontal line, and let $P'$ be the intersection of $OP$ with "
            r"the horizontal line. By the exterior angle theorem in triangle $APP'$: $\widehat{OPQ} = %s - %s = %s$." % (
                _goc(a), _goc(s), _goc(a - s)) + "\\\\\n" +
            r"Similarly, $\widehat{OQP} = 180^{\circ} - \left(%s - %s\right) = %s$." % (_goc(b), _goc(s), _goc(180 - b + s))
            + "\\\\\n" + r"Hence $\widehat{POQ} = 180^{\circ} - %s - %s = %s$." % (_goc(a - s), _goc(180 - b + s), _goc(b - a)))


def _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc):
    if tu == "P":
        return (r"Law of sines in triangle $OPQ$: $OP = \dfrac{PQ\cdot\sin\widehat{OQP}}{\sin\widehat{POQ}} = "
                r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (d, _goc(180 - b + s), _goc(b - a), _xx(kc, 2)))
    return (r"Law of sines in triangle $OPQ$: $OQ = \dfrac{PQ\cdot\sin\widehat{OPQ}}{\sin\widehat{POQ}} = "
            r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (d, _goc(a - s), _goc(b - a), _xx(kc, 2)))


def L10_C3_B6_VD036_MC_F_01(socau, dang=1):
    r"""VẬN DỤNG CAO - khinh khí cầu nhìn từ hai điểm $P$, $Q$ trên sườn đồi nghiêng: tính
    khoảng cách từ $P$ (hoặc $Q$, chọn ngẫu nhiên) tới khinh khí cầu (có hình).

    CLAUDE THEM 30/09/2026 - dang moi theo de co Lan gui (32, 62, 71 do, 50 m -> OP ~ 201 m).
    So lieu chon truoc. Mapping danh dau muc_do_dang VDC. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        s, a, b, d, OP, OQ = _bo_khinh_khi_cau()
        tu = random.choice("PQ")
        kc, kia = (OP, OQ) if tu == "P" else (OQ, OP)
        dap = str(_lt(kc))
        sai_Q = d * _sin_d(b - s) / _sin_d(b - a)          # quên lấy góc bù tại Q
        nhieu = _ba_nhieu(dap, [str(_lt(kia)), str(_lt(sai_Q)), str(_lt(d * _sin_d(a) / _sin_d(b - a)))],
                          buoc=lambda t: str(_lt(kc) + 5 * t))
        debai = (_de_khinh_khi_cau(s, a, b, d) + r" The distance from $%s$ to the hot-air balloon (in meters, rounded "
                 r"to the nearest whole number) is" % tu)
        giai = (_giai_goc_khinh_khi_cau(s, a, b) + "\\\\\n" + _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_khinh_khi_cau(s, d), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn - VẬN DỤNG CAO: khinh khí cầu nhìn từ hai điểm trên sườn đồi nghiêng;
    tính khoảng cách từ $P$ (hoặc $Q$) tới khinh khí cầu (có hình).

    CLAUDE THEM 30/09/2026 - dang moi theo de co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        s, a, b, d, OP, OQ = _bo_khinh_khi_cau()
        tu = random.choice("PQ")
        kc = OP if tu == "P" else OQ
        dap = str(_lt(kc))
        debai = (_de_khinh_khi_cau(s, a, b, d) + r" Find the distance from $%s$ to the hot-air balloon (in meters, rounded "
                 r"to the nearest whole number)." % tu)
        giai = _giai_goc_khinh_khi_cau(s, a, b) + "\\\\\n" + _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc)
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai,
                                  _hinh_khinh_khi_cau(s, d), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_G_01(socau, dong=1):
    r"""Tự luận - khinh khí cầu nhìn từ hai điểm trên sườn đồi nghiêng (có hình).
    a) (VD, tiền đề) Tính số đo các góc của tam giác $OPQ$.
    b) (VDC) Tính khoảng cách từ $P$ (hoặc $Q$) đến khinh khí cầu (hàng đơn vị).

    CLAUDE THEM 30/09/2026 - dang moi theo de co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        s, a, b, d, OP, OQ = _bo_khinh_khi_cau()
        tu = random.choice("PQ")
        kc = OP if tu == "P" else OQ
        ds = [(r"Find the measures of the angles of triangle $OPQ$.",
               r"\widehat{OPQ} = %s,\ \widehat{OQP} = %s,\ \widehat{POQ} = %s" % (_goc(a - s), _goc(180 - b + s), _goc(b - a)),
               _giai_goc_khinh_khi_cau(s, a, b)),
              (r"Find the distance from $%s$ to the hot-air balloon (in meters, rounded to the nearest whole number)." % tu,
               r"O%s \approx %d\,\text{m}" % (tu, _lt(kc)),
               _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc) + r" Hence the distance is about $%d\,\text{m}$." % _lt(kc))]
        cau += TL_answer_text(_de_khinh_khi_cau(s, a, b, d), ds, _hinh_khinh_khi_cau(s, d), 0, dong)
    return cau


# =====================================================================
# BÀI 6 - CÔNG THỨC DIỆN TÍCH, BÁN KÍNH, TRUNG TUYẾN, PHÂN GIÁC (cô Lan 30/09/2026)
#   TH032_MC_F   công thức độ dài đường trung tuyến (lí thuyết)
#   TH034_MC_G   công thức diện tích theo R, r, Heron; công thức R, r (lí thuyết)
#   TH035_MC_D / SA_C   giải tam giác nhỏ: trung tuyến AM (_01), phân giác AD (_02)
#   TH034_MC_H / SA_C   diện tích khi dữ kiện ứng đúng một công thức (h, R, r, Heron)
#   TH034_MC_I / SA_D   bán kính R, r "nhìn là thấy": đã cho sẵn diện tích
#   VD036_MC_G / SA_I   (VD) mảnh vườn tam giác: Heron rồi r, R hoặc đường cao
#   VD036_MC_H / SA_J   (VDC, nhiều bước) biết hai cạnh + góc: côsin -> diện tích -> r
#   L10_C3_TH032_VD036_TL_A, L10_C3_TH034_VD036_TL_A: a) TH, b) VD (thực tiễn)
# Mức VD/VDC đặt ở VD036 (bối cảnh thực tiễn) vì Curriculum Bài 6 chỉ có VD ở đó.
# =====================================================================

def _dap_gon(x):
    """(chuỗi đáp số, câu làm tròn): số nguyên -> không cần làm tròn; còn lại làm tròn
    hàng phần mười (None nếu x sát ranh giới làm tròn)."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x))), ""
    if not _xa_bien(x, 1):
        return None, None
    return _x1(x), " (rounded to the nearest tenth)"


def _heron_mot():
    a, b, c, S, p = random.choice(HERON_NGUYEN)
    ds = [a, b, c]
    random.shuffle(ds)
    return ds[0], ds[1], ds[2], S, p


_TEN_CANH = [("a", "b", "c", "A", "B", "C"), ("b", "c", "a", "B", "C", "A"), ("c", "a", "b", "C", "A", "B")]


def L10_C3_B6_NB032_MC_B_01(socau, dang=1):
    r"""Lí thuyết - chọn công thức ĐÚNG tính độ dài đường trung tuyến ($m_a$, $m_b$ hoặc $m_c$).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan ("hoi cac cong thuc"). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        x, y, z, X, _, _ = random.choice(_TEN_CANH)
        dung = r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}$" % (x, y, z, x)
        sai = [r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} + \dfrac{%s^{2}}{4}$" % (x, y, z, x),
               r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{4} - \dfrac{%s^{2}}{2}$" % (x, y, z, x),
               r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2}$" % (x, y, z, x),
               r"$m_{%s}^{2} = %s^{2} + %s^{2} - \dfrac{%s^{2}}{4}$" % (x, y, z, x)]
        debai = (r"Triangle $ABC$ has $BC = a$, $CA = b$, $AB = c$, and $m_{%s}$ is the length of the median "
                 r"from vertex $%s$. Which of the following formulas is correct?" % (x, X))
        giai = (r"Formula for the length of a median: $m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}"
                r" = \dfrac{2\left(%s^{2} + %s^{2}\right) - %s^{2}}{4}$." % (x, y, z, x, y, z, x))
        cau += MC_SA_answer_text(debai, dung, random.sample(sai, 3), giai, 0, 0, dang)
    return cau


def L10_C3_B6_NB032_MC_B_02(socau, dang=1):
    r"""Lí thuyết - cách hỏi khác của _01: trong bốn hệ thức về ba đường trung tuyến
    $m_a$, $m_b$, $m_c$, chọn hệ thức SAI.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH032_MC_F. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        x, y, z, _, _, _ = random.choice(_TEN_CANH)
        # ba hệ thức đúng KHÔNG nói về m_x (tránh hai phương án cùng m_x, đoán được đáp án)
        dung_ds = [r"$m_{%s}^{2} = \dfrac{2\left(%s^{2} + %s^{2}\right) - %s^{2}}{4}$" % (u, v, w, u)
                   for u, v, w, _, _, _ in _TEN_CANH if u != x]
        dung_ds.append(r"$m_{a}^{2} + m_{b}^{2} + m_{c}^{2} = \dfrac{3}{4}\left(a^{2} + b^{2} + c^{2}\right)$")
        sai = random.choice([r"$m_{%s}^{2} = \dfrac{2\left(%s^{2} + %s^{2}\right) + %s^{2}}{4}$" % (x, y, z, x),
                             r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2} - %s^{2}}{4}$" % (x, y, z, x),
                             r"$m_{%s}^{2} = \dfrac{2\left(%s^{2} + %s^{2}\right) - %s^{2}}{2}$" % (x, y, z, x)])
        debai = (r"Triangle $ABC$ has $BC = a$, $CA = b$, $AB = c$; $m_a$, $m_b$, $m_c$ are the lengths of the "
                 r"medians from $A$, $B$, $C$, respectively. Which of the following relations is \textbf{incorrect}?")
        giai = (r"By the median formula $m_{a}^{2} = \dfrac{2\left(b^{2} + c^{2}\right) - a^{2}}{4}$ "
                r"(and similarly for $m_b$, $m_c$), adding the three equalities gives "
                r"$m_{a}^{2} + m_{b}^{2} + m_{c}^{2} = \dfrac{3}{4}\left(a^{2} + b^{2} + c^{2}\right)$. "
                r"Hence the incorrect relation is %s." % sai)
        cau += MC_SA_answer_text(debai, sai, random.sample(dung_ds, 3), giai, 0, 0, dang)
    return cau


_CT_BAN_KINH_DUNG = [r"$S = \dfrac{abc}{4R}$", r"$S = pr$", r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$",
                     r"$R = \dfrac{abc}{4S}$", r"$r = \dfrac{S}{p}$", r"$S = \dfrac{1}{2}a\cdot h_a$"]
_CT_BAN_KINH_SAI = [r"$S = \dfrac{abc}{2R}$", r"$S = 2pr$", r"$S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}$",
                    r"$R = \dfrac{4S}{abc}$", r"$r = \dfrac{p}{S}$", r"$S = a\cdot h_a$", r"$S = \dfrac{abc}{4r}$",
                    r"$S = \left(p - a\right)\left(p - b\right)\left(p - c\right)$"]
_CAC_KI_HIEU = (r"Triangle $ABC$ has $BC = a$, $CA = b$, $AB = c$, area $S$, semiperimeter $p$, and altitude "
                r"$h_a$ from $A$; $R$ and $r$ are the circumradius and the inradius of the triangle, respectively.")


def L10_C3_B6_NB034_MC_A_01(socau, dang=1):
    r"""Lí thuyết - chọn công thức ĐÚNG về diện tích và bán kính ($S = \dfrac{abc}{4R}$,
    $S = pr$, Heron, $R = \dfrac{abc}{4S}$, $r = \dfrac{S}{p}$).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan ("hoi cac cong thuc"). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung = random.choice(_CT_BAN_KINH_DUNG)
        debai = _CAC_KI_HIEU + " Which of the following formulas is correct?"
        giai = (r"The formulas: $S = \dfrac{1}{2}a\cdot h_a = \dfrac{abc}{4R} = pr = "
                r"\sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$, which give $R = \dfrac{abc}{4S}$, "
                r"$r = \dfrac{S}{p}$. Hence the correct formula is %s." % dung)
        cau += MC_SA_answer_text(debai, dung, random.sample(_CT_BAN_KINH_SAI, 3), giai, 0, 0, dang)
    return cau


def L10_C3_B6_NB034_MC_A_02(socau, dang=1):
    r"""Lí thuyết - cách hỏi khác của _01: chọn công thức SAI (ba phương án đúng).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH034_MC_G. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        sai = random.choice(_CT_BAN_KINH_SAI)
        debai = _CAC_KI_HIEU + r" Which of the following formulas is \textbf{incorrect}?"
        giai = (r"The correct formulas: $S = \dfrac{1}{2}a\cdot h_a = \dfrac{abc}{4R} = pr = "
                r"\sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$, $R = \dfrac{abc}{4S}$, "
                r"$r = \dfrac{S}{p}$. Hence the incorrect formula is %s." % sai)
        cau += MC_SA_answer_text(debai, sai, random.sample(_CT_BAN_KINH_DUNG, 3), giai, 0, 0, dang)
    return cau


def _bo_tt_tam_giac_nho():
    """(AB, BM, góc B, AM): AM^2 = AB^2 + BM^2 - 2 AB.BM cos B, AM nguyên (bộ số chọn trước)."""
    cB, c, k, m_ = random.choice([t for t in _BO_COSIN_TL if abs(t[0]) == Rational(1, 2)])
    if random.random() < 0.5:
        c, k = k, c
    return c, k, (60 if cB > 0 else 120), m_


def _bo_phan_giac():
    """(AB, AD, BD) với góc BAD = 60 độ (góc A = 120 độ), AB > AD, BD nguyên."""
    while True:
        cA, x, y, z = random.choice([t for t in _BO_COSIN_TL if t[0] == Rational(1, 2)])
        AB, AD = max(x, y), min(x, y)
        if AB > AD:
            return AB, AD, z


def _de_tam_giac_nho(bien):
    if bien == 1:
        c, k, B, m_ = _bo_tt_tam_giac_nho()
        de = (r"Triangle $ABC$ has $AB = %d$, $BC = %d$, $\widehat{ABC} = %s$. Let $M$ be the midpoint of $BC$."
              % (c, 2 * k, _goc(B)))
        hoi, dap = r"the length of median $AM$", m_
        giai = (r"Since $M$ is the midpoint of $BC$, $BM = %d$. In triangle $ABM$, by the law of cosines: "
                r"$AM^{2} = AB^{2} + BM^{2} - 2\cdot AB\cdot BM\cdot\cos %s = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s "
                r"= %d$, so $AM = %d$." % (k, _goc(B), c, k, c, k, "\\dfrac{1}{2}" if B == 60 else "\\left(-\\dfrac{1}{2}\\right)",
                                          m_ * m_, m_))
        sai = [round(math.sqrt(c * c + 4 * k * k - 2 * c * 2 * k * math.cos(math.radians(B)))), m_ + 1, 2 * m_,
               round(math.sqrt(c * c + k * k)) ]
        return de, hoi, dap, giai, sai
    AB, AD, BD = _bo_phan_giac()
    de = (r"Triangle $ABC$ has $\widehat{BAC} = 120^{\circ}$ and $AB = %d$. The internal angle bisector of angle $A$ meets "
          r"$BC$ at $D$, and $AD = %d$." % (AB, AD))
    hoi, dap = r"the length of segment $BD$", BD
    giai = (r"Since $AD$ is the angle bisector, $\widehat{BAD} = \dfrac{120^{\circ}}{2} = 60^{\circ}$. In triangle $ABD$, by "
            r"the law of cosines: $BD^{2} = AB^{2} + AD^{2} - 2\cdot AB\cdot AD\cdot\cos 60^{\circ} = %d^{2} + %d^{2} - %d\cdot %d "
            r"= %d$, so $BD = %d$." % (AB, AD, AB, AD, BD * BD, BD))
    sai = [round(math.sqrt(AB * AB + AD * AD + AB * AD)), round(math.sqrt(AB * AB + AD * AD)), BD + 1, AB + AD - BD]
    return de, hoi, dap, giai, sai


def L10_C3_B6_TH035_MC_D_01(socau, dang=1):
    r"""Giải tam giác nhỏ - đường TRUNG TUYẾN: biết $AB$, $BC$, góc $B$, tính trung tuyến $AM$
    bằng định lí côsin trong tam giác $ABM$ (mức TH, đáp số nguyên).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, hoi, dap, giai, sai = _de_tam_giac_nho(1)
        nhieu = _ba_nhieu(str(dap), [str(v) for v in sai], buoc=lambda t: str(dap + t))
        cau += MC_SA_answer_const(de + r" Find %s." % hoi, str(dap), nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH035_MC_D_02(socau, dang=1):
    r"""Giải tam giác nhỏ - đường PHÂN GIÁC: góc $A = 120^{\circ}$, biết $AB$ và phân giác $AD$,
    tính $BD$ bằng định lí côsin trong tam giác $ABD$ (mức TH, đáp số nguyên).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH035_MC_D. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, hoi, dap, giai, sai = _de_tam_giac_nho(2)
        nhieu = _ba_nhieu(str(dap), [str(v) for v in sai], buoc=lambda t: str(dap + t))
        cau += MC_SA_answer_const(de + r" Find %s." % hoi, str(dap), nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH035_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - giải tam giác nhỏ với đường TRUNG TUYẾN (như TH035_MC_D_01).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, hoi, dap, giai, sai = _de_tam_giac_nho(1)
        cau += MC_SA_answer_const(de + r" Find %s." % hoi, str(dap), [str(dap + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH035_SA_D_02(socau, dang=2):
    r"""Trả lời ngắn - giải tam giác nhỏ với đường PHÂN GIÁC (như TH035_MC_D_02).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH035_SA_C. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, hoi, dap, giai, sai = _de_tam_giac_nho(2)
        cau += MC_SA_answer_const(de + r" Find %s." % hoi, str(dap), [str(dap + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def _so_gon(v):
    """Số hữu tỉ viết gọn: số nguyên, thập phân hữu hạn ngắn, hoặc phân số."""
    return _so_thap_phan_gon(v) or _tri(v)


def _dien_tich_mot_cong_thuc():
    """(đề, S, lời giải, nhiễu) - dữ kiện ứng đúng MỘT công thức diện tích (mức TH)."""
    while True:
        a, b, c, S, p = _heron_mot()
        kieu = random.choice(["h", "R", "r", "heron"])
        if kieu == "h":
            h = Rational(2 * S, a)
            if _so_thap_phan_gon(h) is None:
                continue
            de = r"Triangle $ABC$ has $BC = %d$ and the altitude from $A$ is $h_a = %s$." % (a, _so_gon(h))
            giai = r"$S = \dfrac{1}{2}BC\cdot h_a = \dfrac{1}{2}\cdot %d\cdot %s = %d$." % (a, _so_gon(h), S)
            return de, S, giai, [a * h, S * 2, S // 2 if S % 2 == 0 else S + 3]
        if kieu == "R":
            R = Rational(a * b * c, 4 * S)
            de = (r"Triangle $ABC$ has $BC = %d$, $CA = %d$, $AB = %d$ and circumradius "
                  r"$R = %s$." % (a, b, c, _so_gon(R)))
            giai = (r"$S = \dfrac{abc}{4R} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %s} = %d$." % (a, b, c, _so_gon(R), S))
            return de, S, giai, [2 * S, S * 4, round(a * b * c / float(R))]
        if kieu == "r":
            r_ = Rational(S, p)
            if _so_thap_phan_gon(r_) is None:
                continue
            de = (r"Triangle $ABC$ has $BC = %d$, $CA = %d$, $AB = %d$ and inradius $r = %s$."
                  % (a, b, c, _so_gon(r_)))
            giai = (r"The semiperimeter is $p = \dfrac{%d + %d + %d}{2} = %d$, so $S = pr = %d\cdot %s = %d$."
                    % (a, b, c, p, p, _so_gon(r_), S))
            return de, S, giai, [2 * S, (a + b + c) * r_ * 2, S + p]
        de = r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$." % (a, b, c)
        giai = (r"The semiperimeter is $p = %d$. By Heron's formula: $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
                % (p, p, p - a, p - b, p - c, S))
        return de, S, giai, [S * S, 2 * S, p * (p - a)]


def L10_C3_B6_TH034_MC_H_01(socau, dang=1):
    r"""Tính diện tích tam giác khi dữ kiện ứng ĐÚNG MỘT công thức: cạnh và đường cao, ba cạnh
    và $R$, ba cạnh và $r$, hoặc ba cạnh (Heron) - chọn ngẫu nhiên (mức TH).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan ("cac truong hop de ra duoc dien tich luon"). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, S, giai, sai = _dien_tich_mot_cong_thuc()
        nhieu = _ba_nhieu(str(S), [_so_gon(nsimplify(v)) for v in sai], buoc=lambda t: str(S + 2 * t))
        cau += MC_SA_answer_const(de + " The area of triangle $ABC$ is", str(S), nhieu,
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_H_01(socau, dang=2):
    r"""Trả lời ngắn - diện tích tam giác khi dữ kiện ứng đúng một công thức (như TH034_MC_H_01).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        de, S, giai, sai = _dien_tich_mot_cong_thuc()
        if len(str(S)) > 4:
            continue
        so += 1
        cau += MC_SA_answer_const(de + " Find the area of triangle $ABC$.", str(S), [str(S + k) for k in (1, -1, 2)],
                                  giai, 0, 0, dang)
    return cau


def _ban_kinh_nhin_la_thay():
    """TH cực đơn giản: đã cho diện tích, tính r = S/p hoặc R = abc/(4S)."""
    while True:
        a, b, c, S, p = _heron_mot()
        if random.random() < 0.5:
            r_ = Rational(S, p)
            if _so_thap_phan_gon(r_) is None:
                continue
            de = (r"Triangle $ABC$ has area $S = %d$ and perimeter $%d$. The radius $r$ of the inscribed circle "
                  r"of triangle $ABC$" % (S, 2 * p))
            giai = r"The semiperimeter is $p = %d$, so $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %s$." % (p, S, p, _so_thap_phan_gon(r_))
            return de, r_, giai, [Rational(S, 2 * p), Rational(2 * S, p), Rational(p, S)]
        R = Rational(a * b * c, 4 * S)
        if _so_thap_phan_gon(R) is None:
            continue
        de = (r"Triangle $ABC$ has $BC = %d$, $CA = %d$, $AB = %d$ and area $S = %d$. The radius $R$ of the "
              r"circumscribed circle of triangle $ABC$" % (a, b, c, S))
        giai = r"$R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$." % (a, b, c, S, _so_thap_phan_gon(R))
        return de, R, giai, [Rational(a * b * c, 2 * S), Rational(a * b * c, S), Rational(4 * S, a * b * c)]


def L10_C3_B6_TH034_MC_I_01(socau, dang=1):
    r"""Bán kính đường tròn nội tiếp / ngoại tiếp khi ĐÃ CHO diện tích: $r = \dfrac{S}{p}$,
    $R = \dfrac{abc}{4S}$ - mức TH rất đơn giản (thay thẳng công thức).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan ("TH cuc ki don gian, nhin la thay luon"). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, v, giai, sai = _ban_kinh_nhin_la_thay()
        dap = _so_thap_phan_gon(v)
        nhieu = _ba_nhieu(dap, [_so_gon(t) for t in sai], buoc=lambda t: _so_gon(v + t))
        cau += MC_SA_answer_const(de + " is", dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_I_01(socau, dang=2):
    r"""Trả lời ngắn - bán kính $r$ hoặc $R$ khi đã cho diện tích (như TH034_MC_I_01).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        de, v, giai, sai = _ban_kinh_nhin_la_thay()
        dap = _so_thap_phan_gon(v)
        if dap is None or len(dap) > 4:
            continue
        so += 1
        cau += MC_SA_answer_const(de.replace("The radius", "Find the radius") + ".", dap,
                                  [_so_gon(v + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


# ---- VD036 (VD): mảnh vườn tam giác, Heron rồi suy ra r, R hoặc đường cao ----
_HOI_VUON = {
    "r": (r"Workers install an automatic sprinkler at the incenter of triangle $ABC$ so that it waters "
          r"the largest circular part of the garden without spraying water outside the edges. Find the distance from the sprinkler to "
          r"each edge of the garden (in meters%s)."),
    "R": (r"Workers erect a lamppost at the point equidistant from the three corners $A$, $B$, $C$ of the garden. Find the distance from the lamppost "
          r"to each corner of the garden (in meters%s)."),
    "h": (r"Workers build the shortest straight path from corner $A$ to edge $BC$. Find the length of that path "
          r"(in meters%s)."),
}


def _bo_vuon_heron():
    """(đề, đáp số (chuỗi), lời giải) - chọn trước tam giác Heron và đại lượng hỏi."""
    while True:
        a, b, c, S, p = _heron_mot()
        k = random.choice([1, 2, 3])
        a, b, c, S, p = a * k, b * k, c * k, S * k * k, p * k
        hoi = random.choice(["r", "R", "h"])
        gt = {"r": S / p, "R": a * b * c / (4 * S), "h": 2 * S / a}[hoi]
        dap, lam_tron = _dap_gon(gt)
        if dap is None or len(dap) > 4:
            continue
        de = (r"A triangular garden $ABC$ has $BC = %d\,\text{m}$, $CA = %d\,\text{m}$, $AB = %d\,\text{m}$. "
              % (a, b, c) + _HOI_VUON[hoi] % (", rounded to the nearest tenth" if lam_tron else ""))
        giai = (r"The semiperimeter is $p = \dfrac{%d + %d + %d}{2} = %d$. By Heron's formula: "
                r"$S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d\,\left(\text{m}^{2}\right)$.\\ " % (a, b, c, p, p, p - a, p - b, p - c, S))
        giai += {"r": r"The required distance is the inradius: $r = \dfrac{S}{p} = \dfrac{%d}{%d}" % (S, p),
                 "R": r"The point equidistant from the three vertices is the circumcenter: $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d}" % (a, b, c, S),
                 "h": r"The shortest path is the altitude $h_a$: $S = \dfrac{1}{2}BC\cdot h_a$, so $h_a = \dfrac{2S}{BC} = \dfrac{2\cdot %d}{%d}" % (S, a)}[hoi]
        giai += (r" \approx %s\,\text{m}$." if lam_tron else r" = %s\,\text{m}$.") % dap
        return de, dap, giai, gt


def L10_C3_B6_VD036_MC_G_01(socau, dang=1):
    r"""VD - mảnh vườn tam giác biết ba cạnh: tính diện tích (Heron) rồi suy ra bán kính nội tiếp
    (vòi phun), ngoại tiếp (cột đèn) hoặc đường cao (lối đi) từ công thức diện tích khác.

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan (dang cau b tu luan). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dap, giai, gt = _bo_vuon_heron()
        nhieu = _ba_nhieu(dap, [_x1(gt * 2), _x1(gt / 2), _x1(gt + 1)], buoc=lambda t: _x1(gt + t))
        cau += MC_SA_answer_const(de.replace("Find the distance", "The distance").replace("Find the length", "The length").rstrip(".") + " is",
                                  dap, [x.replace(".0", "") for x in nhieu], giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_G_01(socau, dang=2):
    r"""Trả lời ngắn - VD: mảnh vườn tam giác biết ba cạnh, tính $r$, $R$ hoặc đường cao qua diện tích.

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dap, giai, gt = _bo_vuon_heron()
        cau += MC_SA_answer_const(de, dap, [_x1(gt + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


# ---- VD036 (VDC, nhiều bước): hai cạnh + góc xen giữa -> cạnh thứ ba -> diện tích -> r ----
def _bo_vuon_vdc():
    while True:
        cA, b, c, a = random.choice([t for t in _BO_COSIN_TL if abs(t[0]) == Rational(1, 2)])
        A = 60 if cA > 0 else 120
        k = random.choice([1, 2, 3])
        a, b, c = a * k, b * k, c * k
        S = b * c * math.sqrt(3) / 4
        p = (a + b + c) / 2
        r_ = S / p
        dap, lam_tron = _dap_gon(r_)
        if dap is None or len(dap) > 4 or not lam_tron:
            continue
        de = (r"A triangular garden $ABC$ has $AB = %d\,\text{m}$, $AC = %d\,\text{m}$ and angle $\widehat{BAC} = %s$. "
              r"Workers install an automatic sprinkler at the incenter of triangle $ABC$. Find the distance "
              r"from the sprinkler to each edge of the garden (in meters, rounded to the nearest tenth)." % (c, b, _goc(A)))
        giai = (r"Law of cosines: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s = %d$, so $BC = %d$.\\ "
                r"Area $S = \dfrac{1}{2}AB\cdot AC\cdot\sin %s = %s\sqrt{3}$; semiperimeter $p = %s$.\\ "
                r"The required distance is $r = \dfrac{S}{p} = \dfrac{%s\sqrt{3}}{%s} \approx %s\,\text{m}$."
                % (c, b, c, b, _goc(A), a * a, a, _goc(A), _so_gon(Rational(b * c, 4)), _so_gon(Rational(a + b + c, 2)),
                   _so_gon(Rational(b * c, 4)), _so_gon(Rational(a + b + c, 2)), dap))
        return de, dap, giai, r_


def L10_C3_B6_VD036_MC_H_01(socau, dang=1):
    r"""VẬN DỤNG CAO (nhiều bước) - mảnh vườn tam giác biết hai cạnh và góc xen giữa: định lí côsin
    tính cạnh thứ ba, tính diện tích, nửa chu vi rồi bán kính nội tiếp (vòi phun).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan ("VDC tim thong qua nhieu buoc"). Mapping danh dau VDC.
    Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dap, giai, r_ = _bo_vuon_vdc()
        nhieu = _ba_nhieu(dap, [_x1(2 * r_), _x1(r_ * 2 / math.sqrt(3)), _x1(r_ + 0.5)], buoc=lambda t: _x1(r_ + t / 10))
        cau += MC_SA_answer_const(de.replace("Find the distance", "The distance").rstrip(".") + " is", dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_H_01(socau, dang=2):
    r"""Trả lời ngắn - VẬN DỤNG CAO (như VD036_MC_H_01).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Mapping danh dau VDC. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dap, giai, r_ = _bo_vuon_vdc()
        cau += MC_SA_answer_const(de, dap, [_x1(r_ + k / 10) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_TH032_VD036_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý hai đơn vị: mảnh vườn tam giác biết hai cạnh và góc xen giữa.
    a) (TH032) Tính cạnh thứ ba bằng định lí côsin.
    b) (VD036) Tính diện tích rồi suy ra bán kính nội tiếp (vòi phun) hoặc ngoại tiếp (cột đèn).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        cA, b, c, a = random.choice([t for t in _BO_COSIN_TL if abs(t[0]) == Rational(1, 2)])
        A = 60 if cA > 0 else 120
        S = b * c * math.sqrt(3) / 4
        p = (a + b + c) / 2
        hoi = random.choice(["r", "R"])
        gt = S / p if hoi == "r" else a * b * c / (4 * S)
        dap, lam_tron = _dap_gon(gt)
        if dap is None:
            continue
        so += 1
        de = (r"A triangular garden $ABC$ has $AB = %d\,\text{m}$, $AC = %d\,\text{m}$ and angle $\widehat{BAC} = %s$."
              % (c, b, _goc(A)))
        cau_b = (r"Workers install an automatic sprinkler at the incenter of triangle $ABC$. Find the distance "
                 r"from the sprinkler to each edge of the garden" if hoi == "r" else
                 r"Workers erect a lamppost at the point equidistant from the three corners of the garden. Find the distance from the lamppost to each corner of the garden")
        giai_b = (r"Area $S = \dfrac{1}{2}AB\cdot AC\cdot\sin %s = %s\sqrt{3}\,\text{m}^{2}$. " % (_goc(A), _so_gon(Rational(b * c, 4))))
        giai_b += (r"The semiperimeter is $p = %s$, so the required distance is $r = \dfrac{S}{p} %s %s\,\text{m}$."
                   % (_so_gon(Rational(a + b + c, 2)), r"\approx" if lam_tron else "=", dap) if hoi == "r" else
                   r"The required distance is $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %s\sqrt{3}} %s %s\,\text{m}$."
                   % (a, b, c, _so_gon(Rational(b * c, 4)), r"\approx" if lam_tron else "=", dap))
        ds = [(r"Calculate the length of side $BC$.", r"BC = %d\,\text{m}" % a,
               r"Law of cosines: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s = %d$, so $BC = %d\,\text{m}$."
               % (c, b, c, b, _goc(A), a * a, a)),
              (cau_b + r" (in meters%s)." % (", rounded to the nearest tenth" if lam_tron else ""),
               r"%s \approx %s\,\text{m}" % (hoi, dap) if lam_tron else r"%s = %s\,\text{m}" % (hoi, dap), giai_b)]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau


def L10_C3_TH034_VD036_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý hai đơn vị: mảnh vườn tam giác biết ba cạnh.
    a) (TH034) Tính diện tích bằng công thức Heron.
    b) (VD036) Từ diện tích, suy ra bán kính nội tiếp, ngoại tiếp hoặc đường cao (công thức diện tích khác).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dap, giai, gt = _bo_vuon_heron()
        tach = de.index("Workers")
        than, hoi_b = de[:tach].strip(), de[tach:]
        g_a, g_b = giai.split(r"\\ ", 1)
        S = re.search(r"= (\d+)\\,\\left", g_a).group(1)
        ds = [(r"Find the area of the garden.", r"S = %s\,\text{m}^{2}" % S, g_a),
              (hoi_b, r"\approx %s\,\text{m}" % dap if "round" in hoi_b else r"%s\,\text{m}" % dap, g_b)]
        cau += TL_answer_text(than, ds, 0, 0, dong)
    return cau


# =====================================================================
# VD036 - VẬN DỤNG CAO (cô Lan 01/10/2026): tháp BC cao h trên đỉnh đồi; đỉnh tháp B
# và chân tháp C nhìn điểm A ở chân đồi dưới các góc beta, gamma so với PHƯƠNG THẲNG
# ĐỨNG (gamma > beta). Hỏi chiều cao CH của ngọn đồi (hoặc khoảng cách nằm ngang AH).
#   ABC = beta, ACB = 180 - gamma, BAC = gamma - beta; AC = h.sin(beta)/sin(gamma - beta);
#   CH = AC.cos(gamma), AH = AC.sin(gamma).
# Bài gốc: h = 100 m, 30 và 60 độ -> AC = 100 m, CH = 50 m.
# MC_I_01, SA_K_01, TL_H_01 cùng mô tả dạng, Mapping đánh dấu "muc_do_dang": "VDC".
# =====================================================================

def _bo_thap_doi():
    """(h, beta, gamma, AC, CH, AH) chọn trước: góc hợp lí, đáp số không sát ranh giới làm tròn.
    01/10/2026 (cô Lan: đề phải hợp lí): sườn đồi AC dốc không quá 30 độ (gamma >= 60 độ so với phương thẳng đứng),
    đồi cao ít nhất nửa tháp, chân đồi A cách chân đường thẳng đứng qua tháp ít nhất 50 m
    (đề gốc của cô: tháp 100 m, 30 và 60 độ -> đồi 50 m)."""
    while True:
        ga = random.randint(60, 75)
        be = random.randint(15, ga - 10)
        h = random.choice([20, 25, 30, 40, 50, 60, 80, 100, 120])
        AC = h * _sin_d(be) / _sin_d(ga - be)
        CH, AH = AC * _cos_d(ga), AC * _sin_d(ga)
        if CH < max(10, h / 2) or CH > 600 or AH < 50 or AH > 900:
            continue
        if not (_xa_bien(CH) and _xa_bien(AH) and _xa_bien(AC)):
            continue
        return h, be, ga, AC, CH, AH


def _hinh_thap_doi(h, CH, AH, be, ga):
    """Hình vẽ theo số liệu (thu nhỏ cho vừa khung): đồi, tháp BC, điểm A ở chân đồi, H."""
    k = 3.2 / max(AH, CH + h)
    x, yc, yb = AH * k, CH * k, (CH + h) * k
    huong_BA = math.degrees(math.atan2(-yb, -x)) % 360
    huong_CA = math.degrees(math.atan2(-yc, -x)) % 360
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize]\n"
        "\\fill[black!12] (0,0) .. controls (%.2f,%.2f) and (%.2f,%.2f) .. (%.2f,%.2f) "
        ".. controls (%.2f,%.2f) and (%.2f,%.2f) .. (%.2f,0) -- cycle;\n"
        % (0.5 * x, 0.15 * yc, 0.75 * x, yc, x, yc, 1.25 * x, yc, 1.5 * x, 0.15 * yc, 2 * x)
        + "\\draw (-0.3,0) -- (%.2f,0);\n" % (2 * x + 0.3)
        + "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (x, yc, x, yb)
        + "\\draw[dashed] (%.2f,%.2f) -- (%.2f,0);\n" % (x, yc, x)
        + "\\draw[dashed] (0,0) -- (%.2f,%.2f) (0,0) -- (%.2f,%.2f);\n" % (x, yb, x, yc)
        + "\\draw (%.2f,%.2f) arc (270:%.1f:0.45);\n" % (x, yb - 0.45, huong_BA)
        + "\\draw (%.2f,%.2f) arc (270:%.1f:0.3);\n" % (x, yc - 0.3, huong_CA)
        + "\\node[left] at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (x - 0.15, yb - 0.6, be)
        + "\\node[left] at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (x - 0.12, yc - 0.42, ga)
        + "\\draw (%.2f,0) rectangle (%.2f,0.15);\n" % (x - 0.15, x)
        + "\\fill (0,0) circle (0.04) node[below left] {$A$};\n"
        "\\fill (%.2f,0) circle (0.04) node[below] {$H$};\n" % x
        + "\\fill (%.2f,%.2f) circle (0.04) node[right] {$C$};\n" % (x, yc)
        + "\\fill (%.2f,%.2f) circle (0.04) node[right] {$B$};\n" % (x, yb)
        + "\\end{tikzpicture}"
    )


def _de_thap_doi(h, be, ga):
    return (r"On a hill stands a tower $%d\,\text{m}$ tall (see figure). From the top $B$ and the base $C$ of the tower, "
            r"the point $A$ at the foot of the hill is seen at angles of $%s$ and $%s$, respectively, measured from the vertical. "
            r"Let $H$ be the orthogonal projection of $C$ onto the horizontal plane through $A$." % (h, _goc(be), _goc(ga)))


def _giai_goc_thap_doi(be, ga):
    return (r"By the given data, $\widehat{ABC} = %s$ (the angle between $BA$ and the vertical $BH$); $\widehat{ACH} = %s$, so "
            r"$\widehat{ACB} = 180^{\circ} - %s = %s$; hence $\widehat{BAC} = 180^{\circ} - %s - %s = %s$."
            % (_goc(be), _goc(ga), _goc(ga), _goc(180 - ga), _goc(be), _goc(180 - ga), _goc(ga - be)))


def _giai_ac_thap_doi(h, be, ga, AC):
    return (r"Law of sines in triangle $ABC$: $AC = \dfrac{BC\cdot\sin\widehat{ABC}}{\sin\widehat{BAC}} = "
            r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (h, _goc(be), _goc(ga - be), _xx(AC, 2)))


def _giai_hoi_thap_doi(hoi, ga, AC, gt):
    if hoi == "CH":
        return (r"Triangle $ACH$ is right-angled at $H$: $CH = AC\cdot\cos\widehat{ACH} = AC\cdot\cos %s \approx %s\,\text{m}$."
                % (_goc(ga), _xx(gt, 2)))
    return (r"Triangle $ACH$ is right-angled at $H$: $AH = AC\cdot\sin\widehat{ACH} = AC\cdot\sin %s \approx %s\,\text{m}$."
            % (_goc(ga), _xx(gt, 2)))


_HOI_THAP = {"CH": r"the height $CH$ of the hill", "AH": r"the distance $AH$ from $A$ to the foot of the vertical line through the tower"}


def L10_C3_B6_VD036_MC_I_01(socau, dang=1):
    r"""VẬN DỤNG CAO - tháp trên đỉnh đồi, đỉnh và chân tháp nhìn điểm $A$ ở chân đồi dưới hai góc so
    với PHƯƠNG THẲNG ĐỨNG: tính chiều cao ngọn đồi (hoặc khoảng cách nằm ngang $AH$) - có hình.

    CLAUDE THEM 01/10/2026 - dang moi theo de co Lan gui (thap 100 m, 30 va 60 do -> CH = 50 m).
    So lieu chon truoc. Mapping danh dau muc_do_dang VDC. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, be, ga, AC, CH, AH = _bo_thap_doi()
        hoi = random.choice(["CH", "AH"])
        gt, kia = (CH, AH) if hoi == "CH" else (AH, CH)
        dap = str(_lt(gt))
        nhieu = _ba_nhieu(dap, [str(_lt(kia)), str(_lt(AC)), str(_lt(gt + h * _cos_d(ga)))],
                          buoc=lambda t: str(_lt(gt) + 3 * t))
        debai = _de_thap_doi(h, be, ga) + r" Then %s (rounded to the nearest whole number) is approximately" % _HOI_THAP[hoi]
        giai = (_giai_goc_thap_doi(be, ga) + "\\\\\n" + _giai_ac_thap_doi(h, be, ga, AC) + "\\\\\n"
                + _giai_hoi_thap_doi(hoi, ga, AC, gt))
        cau += MC_SA_answer_const(debai, dap + r"\,\text{m}", [v + r"\,\text{m}" for v in nhieu], giai,
                                  _hinh_thap_doi(h, CH, AH, be, ga), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_I_01(socau, dang=2):
    r"""Trả lời ngắn - VẬN DỤNG CAO: tháp trên đỉnh đồi, hai góc so với phương thẳng đứng; tính chiều cao
    ngọn đồi hoặc khoảng cách nằm ngang $AH$ (có hình).

    CLAUDE THEM 01/10/2026 - dang moi theo de co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, be, ga, AC, CH, AH = _bo_thap_doi()
        hoi = random.choice(["CH", "AH"])
        gt = CH if hoi == "CH" else AH
        dap = str(_lt(gt))
        debai = (_de_thap_doi(h, be, ga) + r" Find %s (in meters, rounded to the nearest whole number)." % _HOI_THAP[hoi])
        giai = (_giai_goc_thap_doi(be, ga) + "\\\\\n" + _giai_ac_thap_doi(h, be, ga, AC) + "\\\\\n"
                + _giai_hoi_thap_doi(hoi, ga, AC, gt))
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai,
                                  _hinh_thap_doi(h, CH, AH, be, ga), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_H_01(socau, dong=1):
    r"""Tự luận - tháp trên đỉnh đồi (có hình).
    a) (VD, tiền đề) Tính các góc của tam giác $ABC$ và độ dài $AC$.
    b) (VDC) Tính chiều cao $CH$ của ngọn đồi (hoặc khoảng cách $AH$).

    CLAUDE THEM 01/10/2026 - dang moi theo de co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, be, ga, AC, CH, AH = _bo_thap_doi()
        hoi = random.choice(["CH", "AH"])
        gt = CH if hoi == "CH" else AH
        ds = [(r"Find the measures of the angles of triangle $ABC$ and the length $AC$ (rounded to the nearest tenth).",
               r"\widehat{ABC} = %s,\ \widehat{ACB} = %s,\ \widehat{BAC} = %s;\ AC \approx %s\,\text{m}"
               % (_goc(be), _goc(180 - ga), _goc(ga - be), _x1(AC)),
               _giai_goc_thap_doi(be, ga) + "\\\\\n" + _giai_ac_thap_doi(h, be, ga, AC)),
              (r"Find %s (in meters, rounded to the nearest whole number)." % _HOI_THAP[hoi],
               r"%s \approx %d\,\text{m}" % (hoi, _lt(gt)),
               _giai_hoi_thap_doi(hoi, ga, AC, gt) + r" Hence $%s \approx %d\,\text{m}$." % (hoi, _lt(gt)))]
        cau += TL_answer_text(_de_thap_doi(h, be, ga), ds, _hinh_thap_doi(h, CH, AH, be, ga), 0, dong)
    return cau


# =====================================================================
# CỔNG TRỜI - XÃ DÂN HÓA (cô Lan 01/10/2026, đề giữa kì I 2025-2026): vùng đất tứ giác
# ABCD được đường chéo BD chia thành hai tam giác BCD, ABD; đo các cạnh trên Google Maps.
#   TF_I_01   Đúng/Sai: hệ quả côsin, định lí sin, sin qua diện tích, ước lượng diện tích
#   VD036_MC_J_01 / SA_L_01   ước lượng diện tích vùng đất (Heron hai lần)
#   VD036_TL_I_01   a) diện tích một tam giác (VD)  b) diện tích cả vùng (VDC)
# Bài gốc: BC = 15, CD = 20, BD = 20, AB = 11, AD = 10 (km) -> 139,05 + 31,98 ~ 171 km^2.
# Số đo lấy theo số đo thực tế của cô, mỗi đoạn chỉ lệch tối đa 1 km (không khác xa thực tế).
# =====================================================================

_DOAN_CONG_TROI = (
    r"In the (former) province of Quang Binh there is a special historical relic named Cong Troi (Heaven's Gate, also called Cha Lo Heaven's Gate), "
    r"with majestic scenery tied to the immortal feats of our army. Cong Troi is the road linking "
    r"Eastern Truong Son with Western Truong Son, located in the area of Dan Hoa commune, Minh Hoa district. After the reorganization of "
    r"administrative units (effective 01/07/2025, day/month/year), this place belongs to Dan Hoa commune, Quang Tri province.\\ "
    r"Cong Troi stands towering and proud, as if bowing to protect every column of troops and every convoy supporting the "
    r"southern battlefield in the resistance war against America. This place was regarded as the ``coordinates of fire'' when the American enemy "
    r"furiously bombed it in an attempt to cut off this supply route. The figure shows the boundary of the former Dan Hoa commune "
    r"during the war. Someone uses Google Maps to measure the distances as shown in the figure."
)


def _heron_f(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(max(p * (p - a) * (p - b) * (p - c), 0))


def _goc_tam_giac(doi, k1, k2):
    """Góc (độ) đối diện cạnh doi, kẹp giữa hai cạnh k1, k2."""
    return math.degrees(math.acos((k1 * k1 + k2 * k2 - doi * doi) / (2 * k1 * k2)))


def _bo_cong_troi(ph="BD"):
    """(BC, CD, BD, AB, AD, S_BCD, S_ABD) - số đo THỰC TẾ đo trên Google Maps (BC = 15, CD = 20,
    BD = 20, AB = 11, AD = 10 km) chỉ xê dịch nhẹ (mỗi đoạn lệch tối đa 1 km) để đề vẫn đúng thực tế
    (cô Lan 01/10/2026); hai tam giác không dẹt, tứ giác lồi.

    13/10/2026 (cô Lan): đường chéo được đo có thể là BD (ph = "BD", như trên) hoặc AC (ph = "AC").
    Khung ABCD thật giữ nguyên, AC suy ra từ hình thật = 17,8 (làm tròn 18). Với ph = "AC" hàm trả về
    các số theo VAI TRÒ (đỉnh A', B', C', D' = D, A, B, C thật; đường chéo B'D' = AC thật) để mọi
    công thức bên dưới dùng lại nguyên; tên đỉnh thật được đổi lại bằng _dich_ten_ct(ph)."""
    # (BC, CD, BD, AB, AD) theo vai trò:  BD -> thật;  AC -> (AB, BC, AC, DA, CD) thật = (11, 15, 18, 10, 20)
    goc_so = (15, 20, 20, 11, 10) if ph == "BD" else (11, 15, 18, 10, 20)
    while True:
        BC, CD, BD, AB, AD = [g + random.choice([-1, 0, 0, 1]) for g in goc_so]
        if not (BC + CD > BD + 2 and AB + AD > BD + 0.5 and abs(BC - CD) < BD and abs(AB - AD) < BD):
            continue
        tam_giac = [(BC, CD, BD), (AB, AD, BD)]
        goc = [_goc_tam_giac(x, y, z) for (u, v, w) in tam_giac
               for x, y, z in ((u, v, w), (v, w, u), (w, u, v))]
        if min(goc) < 8:
            continue
        # tứ giác lồi: góc tại B và tại D (tổng hai góc thành phần) nhỏ hơn 180 độ
        gB = _goc_tam_giac(CD, BC, BD) + _goc_tam_giac(AD, AB, BD)
        gD = _goc_tam_giac(BC, CD, BD) + _goc_tam_giac(AB, AD, BD)
        if gB >= 170 or gD >= 170:
            continue
        S1, S2 = _heron_f(BC, CD, BD), _heron_f(AB, AD, BD)
        if abs(S1 + S2 - 171) > 15:          # diện tích gần thực tế (khoảng 171 km^2)
            continue
        if not (_xa_bien(S1 + S2) and _xa_bien(S1) and _xa_bien(S2)):
            continue
        return BC, CD, BD, AB, AD, S1, S2


def _hinh_cong_troi(BC, CD, BD, AB, AD, don_vi="km"):
    """Sơ đồ vùng đất tứ giác ABCD (đường chéo BD) vẽ theo số đo, ghi độ dài các đoạn."""
    huong = 70.0
    gC = _goc_tam_giac(BC, CD, BD)            # góc BDC
    gA = _goc_tam_giac(AB, AD, BD)            # góc BDA
    D = (0.0, 0.0)
    B = (BD * math.cos(math.radians(huong)), BD * math.sin(math.radians(huong)))
    C = (CD * math.cos(math.radians(huong + gC)), CD * math.sin(math.radians(huong + gC)))
    A = (AD * math.cos(math.radians(huong - gA)), AD * math.sin(math.radians(huong - gA)))
    xs, ys = [p[0] for p in (A, B, C, D)], [p[1] for p in (A, B, C, D)]
    k = 3.6 / max(max(xs) - min(xs), max(ys) - min(ys))
    P = {t: (p[0] * k, p[1] * k) for t, p in zip("ABCD", (A, B, C, D))}

    cx = sum(p[0] for p in P.values()) / 4
    cy = sum(p[1] for p in P.values()) / 4

    def nhan_doan(u, v, phia=None):
        """Vị trí ghi độ dài: trung điểm lệch ra ngoài tứ giác (đường chéo: lệch về phía A)."""
        (x1, y1), (x2, y2) = P[u], P[v]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nx, ny = -(y2 - y1), x2 - x1
        dai = math.hypot(nx, ny) or 1
        nx, ny = nx / dai, ny / dai
        tx, ty = (P[phia] if phia else (cx, cy))
        if (nx * (tx - mx) + ny * (ty - my) > 0) != bool(phia):
            nx, ny = -nx, -ny
        return mx + 0.32 * nx, my + 0.32 * ny
    s = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s += "\\fill[green!12] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;\n" % (
        P["A"] + P["B"] + P["C"] + P["D"])
    s += "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;\n" % (
        P["A"] + P["B"] + P["C"] + P["D"])
    s += "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (P["B"] + P["D"])
    for t, vt in zip("ABCD", ("right", "above right", "above left", "below")):
        s += "\\fill (%.2f,%.2f) circle (0.06) node[%s] {$%s$};\n" % (P[t] + (vt, t))
    for (u, v), d, phia in ((("B", "C"), BC, None), (("C", "D"), CD, None), (("B", "D"), BD, "A"),
                            (("A", "B"), AB, None), (("A", "D"), AD, None)):
        s += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d$ %s};\n" % (nhan_doan(u, v, phia) + (d, don_vi))
    return s + "\\end{tikzpicture}"


_PH_CT = {"BD": {}, "AC": {"A": "D", "B": "A", "C": "B", "D": "C"}}


def _dich_ten_ct(ph):
    """Trả về hàm đổi TÊN ĐỈNH theo vai trò (A', B', C', D') về tên thật khi đường chéo đo là AC.
    Chỉ đổi trong phần công thức giữa hai dấu $ (hoặc cả chuỗi nếu toan=True) nên không đụng chữ
    ``Dân Hóa'', ``Diện tích''. Tên đoạn / tam giác viết theo thứ tự chữ cái (AD, ACD...); tên góc
    giữ đỉnh ở giữa (BAC)."""
    import re
    ban_do = _PH_CT[ph]
    mau = re.compile(r"\\widehat\{([A-D]+)\}|([A-D]+)")

    def doi(m):
        if m.group(1):
            r = "".join(ban_do.get(c, c) for c in m.group(1))
            if len(r) == 3:
                a, b = sorted((r[0], r[2]))
                r = a + r[1] + b
            return "\\widehat{%s}" % r
        r = "".join(ban_do.get(c, c) for c in m.group(2))
        return "".join(sorted(r)) if len(r) > 1 else r

    def dich(chuoi, toan=False):
        if not ban_do:
            return chuoi
        if toan:
            return mau.sub(doi, chuoi)
        return re.sub(r"\$([^$]*)\$", lambda k: "$" + mau.sub(doi, k.group(1)) + "$", chuoi)
    return dich


def _hinh_cong_troi_ph(ph, BC, CD, BD, AB, AD):
    """Hình vùng đất. ph = "BD": như cũ. ph = "AC": vẽ lại theo TÊN THẬT (đường chéo AC), các số
    BC, CD, BD, AB, AD ở đây là số theo vai trò (xem _bo_cong_troi)."""
    if ph == "BD":
        return _hinh_cong_troi(BC, CD, BD, AB, AD)
    # số đo thật: AB = BC(vt), BC = CD(vt), CD = AD(vt), DA = AB(vt), AC = BD(vt)
    ab, bc, cd, da, ac = BC, CD, AD, AB, BD
    x = (ab * ab + ac * ac - bc * bc) / (2 * ac)
    B = (x, math.sqrt(ab * ab - x * x))
    x = (da * da + ac * ac - cd * cd) / (2 * ac)
    D = (x, -math.sqrt(da * da - x * x))
    P = {"A": (0.0, 0.0), "B": B, "C": (float(ac), 0.0), "D": D}
    if ((P["B"][0] - P["D"][0]) * (P["C"][1] - P["D"][1]) - (P["B"][1] - P["D"][1]) * (P["C"][0] - P["D"][0])) < 0:
        P = {k: (v[0], -v[1]) for k, v in P.items()}
    quay = math.radians(70) - math.atan2(P["B"][1] - P["D"][1], P["B"][0] - P["D"][0])
    o = P["D"]
    P = {k: ((v[0] - o[0]) * math.cos(quay) - (v[1] - o[1]) * math.sin(quay),
             (v[0] - o[0]) * math.sin(quay) + (v[1] - o[1]) * math.cos(quay)) for k, v in P.items()}
    xs, ys = [p[0] for p in P.values()], [p[1] for p in P.values()]
    k = 3.6 / max(max(xs) - min(xs), max(ys) - min(ys))
    P = {t: (p[0] * k, p[1] * k) for t, p in P.items()}
    cx = sum(p[0] for p in P.values()) / 4
    cy = sum(p[1] for p in P.values()) / 4

    def nhan_doan(u, v, phia=None):
        (x1, y1), (x2, y2) = P[u], P[v]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nx, ny = -(y2 - y1), x2 - x1
        dai = math.hypot(nx, ny) or 1
        nx, ny = nx / dai, ny / dai
        tx, ty = (P[phia] if phia else (cx, cy))
        if (nx * (tx - mx) + ny * (ty - my) > 0) != bool(phia):
            nx, ny = -nx, -ny
        return mx + 0.32 * nx, my + 0.32 * ny
    q = P["A"] + P["B"] + P["C"] + P["D"]
    s = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s += "\\fill[green!12] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;\n" % q
    s += "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;\n" % q
    s += "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (P["A"] + P["C"])
    for t, vt in zip("ABCD", ("right", "above right", "above left", "below")):
        s += "\\fill (%.2f,%.2f) circle (0.06) node[%s] {$%s$};\n" % (P[t] + (vt, t))
    for (u, v), d, phia in ((("B", "C"), bc, None), (("C", "D"), cd, None), (("A", "C"), ac, "D"),
                            (("A", "B"), ab, None), (("A", "D"), da, None)):
        s += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d$ km};\n" % (nhan_doan(u, v, phia) + (d,))
    return s + "\\end{tikzpicture}"


def _giai_heron(ten, a, b, c, S):
    p = (a + b + c) / 2
    return (r"Triangle $%s$ has semiperimeter $p = \dfrac{%d + %d + %d}{2} = %s$, so "
            r"$S_{%s} = \sqrt{%s\cdot %s\cdot %s\cdot %s} \approx %s\,\left(\text{km}^{2}\right)$."
            % (ten, a, b, c, _xx(p, 1), ten, _xx(p, 1), _xx(p - a, 1), _xx(p - b, 1), _xx(p - c, 1), _xx(S, 2)))


def L10_C3_TF_I_01(socau, socot=1):
    r"""Đúng/Sai - Cổng Trời, xã Dân Hóa: vùng đất tứ giác $ABCD$ chia bởi đường chéo $BD$, các cạnh đo
    trên Google Maps (có hình). a) hệ quả định lí côsin; b) định lí sin; c) sin của góc qua diện tích;
    d) ước lượng diện tích vùng đất (Heron hai lần).

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I 2025-2026 co Lan gui (Phan II cau 2). Bo hinh
    Google Maps (ban quyen, khong khop so ngau nhien) - ve so do TikZ theo so lieu. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        ph = random.choice(["BD", "AC"])        # đường chéo được đo: BD hoặc AC (cô Lan 13/10/2026)
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi(ph)
        _tn = _dich_ten_ct(ph)
        _tl = lambda ds: [(_tn(a), _tn(b)) for a, b in ds]
        S = S1 + S2
        debai = _DOAN_CONG_TROI + _tn(r" Here $S_{ABD}$ is the area of triangle $ABD$. Determine whether each of the following statements is true or false.")
        # a) NB - nhận ra hệ quả định lí côsin trong tam giác BCD
        ly_a = r"Corollary of the law of cosines: the cosine of an angle equals the sum of the squares of the two adjacent sides minus the square of the opposite side, divided by twice the product of the two adjacent sides."
        F = r"$\cos\widehat{%s} = \dfrac{%s^{2} + %s^{2} - %s^{2}}{%s\cdot %s\cdot %s}$"
        dung, sai = [], []
        for g, k1, k2, d_ in (("DBC", "BC", "BD", "CD"), ("BCD", "BC", "CD", "BD"), ("BDC", "BD", "CD", "BC")):
            dung.append((F % (g, k1, k2, d_, "2", k1, k2), ly_a))
            sai += [(F % (g, k1, k2, d_, "1", k1, k2), ly_a), (F % (g, k1, d_, k2, "2", k1, d_), ly_a),
                    (F % (g, k1, k2, d_, "2", k1, d_), ly_a)]
        y1 = _phat_bieu(_tl([(t.replace(r"{1\cdot ", "{"), l) for t, l in dung]),
                        _tl([(t.replace(r"{1\cdot ", "{"), l) for t, l in sai]))
        # b) TH - định lí sin trong tam giác ABD (cạnh đối diện góc)
        ly_b = (r"Law of sines in triangle $ABD$: side $AD$ is opposite angle $\widehat{ABD}$, side $AB$ is opposite angle "
                r"$\widehat{ADB}$, and side $BD$ is opposite angle $\widehat{BAD}$.")
        G = r"$\dfrac{%s}{\sin\widehat{%s}} = \dfrac{%s}{\sin\widehat{%s}}$"
        y2 = _phat_bieu(
            _tl([(G % ("AD", "ABD", "AB", "ADB"), ly_b), (G % ("BD", "BAD", "AD", "ABD"), ly_b), (G % ("AB", "ADB", "BD", "BAD"), ly_b)]),
            _tl([(G % ("AD", "ADB", "AB", "ABD"), ly_b), (G % ("AD", "ABD", "BD", "ADB"), ly_b), (G % ("BD", "ABD", "AD", "BAD"), ly_b),
                 (G % ("AB", "ABD", "BD", "BAD"), ly_b)]))
        # c) VD - suy ra sin của góc từ công thức diện tích
        ly_c = (r"$S_{ABD} = \dfrac{1}{2}AB\cdot BD\cdot\sin\widehat{ABD} = \dfrac{1}{2}AD\cdot BD\cdot\sin\widehat{ADB} = "
                r"\dfrac{1}{2}AB\cdot AD\cdot\sin\widehat{BAD}$ (the angle between the two sides).")
        H = r"$\sin\widehat{%s} = \dfrac{%sS_{ABD}}{%s\cdot %s}$"
        y3 = _phat_bieu(
            _tl([(H % ("ABD", "2", "AB", "BD"), ly_c), (H % ("ADB", "2", "AD", "BD"), ly_c), (H % ("BAD", "2", "AB", "AD"), ly_c)]),
            _tl([(H % ("ABD", "", "AB", "BD"), ly_c), (H % ("ABD", "2", "AD", "BD"), ly_c), (H % ("ADB", "2", "AB", "BD"), ly_c),
                 (H % ("BAD", "", "AB", "AD"), ly_c), (H % ("BAD", "2", "AB", "BD"), ly_c)]))
        # d) VDC - ước lượng diện tích: Heron hai lần rồi cộng
        ly_d = _tn(_giai_heron("BCD", BC, CD, BD, S1) + "\\\\ " + _giai_heron("ABD", AB, AD, BD, S2) + "\\\\ "
                   r"The area of the former Dan Hoa commune is about $S_{BCD} + S_{ABD}$.")
        y4 = _tf_gop(_tf_so(r"The estimated area of the former Dan Hoa commune is $%s$", S, 0, ly_d,
                            [(S1, _tn("Counted only triangle $BCD$")), (S2, _tn("Counted only triangle $ABD$")), (2 * S, "Multiplied by an extra factor of 2")],
                            dv=r"\,\text{km}^{2}", bdt=r"The area of the former Dan Hoa commune is %s $%s$"))
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_cong_troi_ph(ph, BC, CD, BD, AB, AD), 0, socot)
    return cau


def L10_C3_B6_VD036_MC_J_01(socau, dang=1):
    r"""Ước lượng diện tích vùng đất tứ giác (Cổng Trời - xã Dân Hóa) chia bởi một đường chéo thành hai
    tam giác biết ba cạnh: Heron hai lần rồi cộng (có hình).

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I cua co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ph = random.choice(["BD", "AC"])
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi(ph)
        _tn = _dich_ten_ct(ph)
        dap = str(_lt(S1 + S2))
        nhieu = _ba_nhieu(dap, [str(_lt(S1)), str(_lt(S2)), str(_lt(2 * (S1 + S2)))],
                          buoc=lambda t: str(_lt(S1 + S2) + 4 * t))
        debai = (_DOAN_CONG_TROI + r" The estimated area of the former Dan Hoa commune (rounded to the nearest whole number, in "
                 r"$\text{km}^{2}$) is")
        giai = _tn(_giai_heron("BCD", BC, CD, BD, S1) + "\\\\\n" + _giai_heron("ABD", AB, AD, BD, S2) + "\\\\\n"
                   r"Hence the area is about $S_{BCD} + S_{ABD} \approx %s\,\text{km}^{2}$." % dap)
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_cong_troi_ph(ph, BC, CD, BD, AB, AD), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_J_01(socau, dang=2):
    r"""Trả lời ngắn - ước lượng diện tích vùng đất tứ giác (Cổng Trời - xã Dân Hóa) bằng Heron hai lần.

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I cua co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ph = random.choice(["BD", "AC"])
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi(ph)
        _tn = _dich_ten_ct(ph)
        dap = str(_lt(S1 + S2))
        if len(dap) > 4:
            continue
        so += 1
        debai = (_DOAN_CONG_TROI + r" Estimate the area of the former Dan Hoa commune (in $\text{km}^{2}$, rounded to the nearest "
                 r"whole number).")
        giai = _tn(_giai_heron("BCD", BC, CD, BD, S1) + "\\\\\n" + _giai_heron("ABD", AB, AD, BD, S2) + "\\\\\n"
                   r"Hence the area is about $S_{BCD} + S_{ABD} \approx %s\,\text{km}^{2}$." % dap)
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai,
                                  _hinh_cong_troi_ph(ph, BC, CD, BD, AB, AD), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_I_01(socau, dong=1):
    r"""Tự luận - Cổng Trời, xã Dân Hóa (có hình).
    a) (VD) Tính diện tích tam giác $BCD$ (hoặc $ABD$).
    b) (VDC) Ước lượng diện tích của xã Dân Hóa cũ (vùng tứ giác $ABCD$).

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I cua co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ph = random.choice(["BD", "AC"])
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi(ph)
        _tn = _dich_ten_ct(ph)
        if random.random() < 0.5:
            ten, ba, Sa, ten2, ba2, Sb = "BCD", (BC, CD, BD), S1, "ABD", (AB, AD, BD), S2
        else:
            ten, ba, Sa, ten2, ba2, Sb = "ABD", (AB, AD, BD), S2, "BCD", (BC, CD, BD), S1
        ds = [(_tn(r"Find the area of triangle $%s$ (rounded to the nearest tenth, in $\text{km}^{2}$)." % ten),
               _tn(r"S_{%s} \approx %s\,\text{km}^{2}" % (ten, _x1(Sa)), True), _tn(_giai_heron(ten, *ba, Sa))),
              (r"Estimate the area of the former Dan Hoa commune (rounded to the nearest whole number, in $\text{km}^{2}$).",
               r"S \approx %d\,\text{km}^{2}" % _lt(S1 + S2),
               _tn(_giai_heron(ten2, *ba2, Sb) + "\\\\ " +
                   r"The area of the former Dan Hoa commune is about $S_{BCD} + S_{ABD} \approx %s \approx %d\,\text{km}^{2}$."
                   % (_xx(S1 + S2, 2), _lt(S1 + S2))))]
        cau += TL_answer_text(_DOAN_CONG_TROI, ds, _hinh_cong_troi_ph(ph, BC, CD, BD, AB, AD), 0, dong)
    return cau


# =====================================================================================================
# CÔNG VIÊN LÊ THỊ RIÊNG - SỰ KIỆN NĂM 2026 (cô Lan 13/10/2026)
# CÙNG DẠNG với Cổng Trời (ước lượng diện tích vùng đất tứ giác chia bởi một đường chéo thành hai tam giác biết ba cạnh,
# Heron hai lần). Thêm HAI BIẾN THỂ _02, _03 vào chính các ID MC_J, SA_L, TL_I (không tạo dạng mới):
#   _02: tìm diện tích CÔNG VIÊN (khoảng 75 000 m^2 = 7,5 ha; đáp số tính bằng ha)
#   _03: tìm diện tích KHU VỰC rãnh mộ tập thể - mỗi câu ngẫu nhiên một trong bốn khu vực: Khu vực 1 (khoảng 800 m^2),
#        Khu vực 2 (khoảng 1 200 m^2), Khu vực 3 (khoảng 500 m^2), khu vực tìm kiếm mở rộng (khoảng 5 800 m^2)
# Số liệu THẬT (sơ đồ cô Lan gửi 13/10/2026 + báo Dân Việt, VietNamNet, Tuổi Trẻ, VietnamPlus, Báo Lào Cai): diện tích các khu vực
# và công viên (sơ đồ hiện trạng ghi khoảng 75 000 m^2; báo ghi khoảng 8 ha), Tết Mậu Thân 1968, quy tập từ 6/7/2026, 731 bộ hài cốt
# đến 11/10/2026, ước tính hơn 900 liệt sĩ, lễ viếng - truy điệu - an táng 14/10/2026. SỐ ĐO CÁC CẠNH là GIẢ ĐỊNH (nói rõ trong đề),
# chọn ngẫu nhiên sao cho diện tích tứ giác sát số thật (lệch tối đa 3%). Đề KHÔNG nêu diện tích của chính đối tượng được hỏi.
# =====================================================================================================

_LTR_DAN = (r"Le Thi Rieng Cultural Park (Ho Chi Minh City) lies on part of the former Do Thanh Cemetery. According to "
            r"eyewitness accounts, during the Tet Mau Than General Offensive and Uprising (in $2/1968$), many martyrs were buried together "
            r"in trench graves right here. Since $6/7/2026$ (day/month/year) the city has been recovering the remains; by $11/10/2026$, "
            r"$731$ sets of remains had been found, and it is estimated that more than $900$ martyrs still lie here. %s In such a small plot of land, so many "
            r"outstanding sons and daughters of the nation fell; they lay here for nearly sixty years until $14/10/2026$ (day/month/year), when the city held a "
            r"visiting ceremony, a memorial service and a burial. That is the price of peace, so that each of us may be more grateful for the sacrifice of our forefathers. ")
_LTR_SO_SANH_CV = r"The three zones suspected of containing mass-grave trenches that have been delimited have a total area of only about $2\,500\ \text{m}^{2}$."
_LTR_SO_SANH_KV = r"The whole park covers about $7.5$ hectares, and the zones suspected of containing mass-grave trenches are only a very small part of it."

# (tên khu vực, diện tích thật m^2, bước làm tròn số đo cạnh m)
_LTR_KHU_VUC = [("Zone $1$", 800, 1), ("Zone $2$", 1200, 1), ("Zone $3$", 500, 1),
                ("the expanded search zone", 5800, 5)]


def _ltr_bo(S0, buoc, ha):
    """(BC, CD, BD, AB, AD, S_BCD, S_ABD): số đo GIẢ ĐỊNH (bội của `buoc` m), tứ giác ABCD lồi, diện tích sát S0 (lệch <= 3%)."""
    L = math.sqrt(S0)
    q = lambda x: int(round(x / buoc)) * buoc
    while True:
        BC, CD, AB, AD = (q(L * random.uniform(0.7, 1.3)) for _ in range(4))
        BD = q(L * random.uniform(1.0, 1.7))
        if min(BC, CD, AB, AD, BD) <= 0:
            continue
        if not (BC + CD > BD + buoc and AB + AD > BD + buoc and abs(BC - CD) < BD - buoc and abs(AB - AD) < BD - buoc):
            continue
        goc = [_goc_tam_giac(x, y, z) for (u, v, w) in ((BC, CD, BD), (AB, AD, BD)) for x, y, z in ((u, v, w), (v, w, u), (w, u, v))]
        if min(goc) < 15:
            continue
        gB = _goc_tam_giac(CD, BC, BD) + _goc_tam_giac(AD, AB, BD)
        gD = _goc_tam_giac(BC, CD, BD) + _goc_tam_giac(AB, AD, BD)
        if gB >= 170 or gD >= 170:
            continue
        S1, S2 = _heron_f(BC, CD, BD), _heron_f(AB, AD, BD)
        if abs(S1 + S2 - S0) > 0.03 * S0:
            continue
        if not (_xa_bien(S1) and _xa_bien(S2) and (_xa_bien((S1 + S2) / 1e4, 1) if ha else _xa_bien(S1 + S2))):
            continue
        return BC, CD, BD, AB, AD, S1, S2


def _giai_heron_m(ten, a, b, c, S):
    p = (a + b + c) / 2
    return (r"Triangle $%s$ has semiperimeter $p = \dfrac{%d + %d + %d}{2} = %s$ (m), so "
            r"$S_{%s} = \sqrt{%s\cdot %s\cdot %s\cdot %s} \approx %d\,\left(\text{m}^{2}\right)$."
            % (ten, a, b, c, _xx(p, 1), ten, _xx(p, 1), _xx(p - a, 1), _xx(p - b, 1), _xx(p - c, 1), _lt(S)))


def _ltr_cau(cv):
    """Một bộ dữ liệu: cv = True -> công viên (đáp số ha); False -> một khu vực ngẫu nhiên (đáp số m^2)."""
    if cv:
        ten, S0, buoc = "Le Thi Rieng Park", 75000, 10
        mo = (_LTR_DAN % _LTR_SO_SANH_CV) + r"The area of the whole park is estimated by approximating the park"
    else:
        ten, S0, buoc = random.choice(_LTR_KHU_VUC)
        mo = (_LTR_DAN % _LTR_SO_SANH_KV) + r"We approximate %s" % ten
    BC, CD, BD, AB, AD, S1, S2 = _ltr_bo(S0, buoc, cv)
    S = S1 + S2
    f = (lambda x: _x1(x / 1e4, 1)) if cv else (lambda x: str(_lt(x)))
    dv = r"\,\text{ha}" if cv else r"\,\text{m}^{2}"
    intro = (mo + r" by the convex quadrilateral $ABCD$ (the measurements are hypothetical) with $AB = %d$ m, $BC = %d$ m, $CD = %d$ m, $DA = %d$ m and "
             r"diagonal $BD = %d$ m (see figure)." % (AB, BC, CD, AD, BD))
    giai = _giai_heron_m("BCD", BC, CD, BD, S1) + "\\\\\n" + _giai_heron_m("ABD", AB, AD, BD, S2) + "\\\\\n"
    duoi = ""
    if cv:
        duoi += (r"The area is approximately $S_{BCD} + S_{ABD} \approx %d\,\text{m}^{2} \approx %s$ ha (since $1\ \text{ha} = 10\,000\ \text{m}^{2}$)."
                 % (_lt(S), f(S)))
    else:
        duoi += r"Hence the area is about $S_{BCD} + S_{ABD} \approx %d\,\text{m}^{2}$." % _lt(S)
    giai += duoi
    donvi = r"in hectares, rounded to the nearest tenth" if cv else r"in $\text{m}^{2}$, rounded to the nearest whole number"
    return dict(ten=ten, cv=cv, dv=dv, f=f, intro=intro, giai=giai, duoi=duoi, donvi=donvi, S=S, S1=S1, S2=S2, BC=BC, CD=CD, BD=BD,
                AB=AB, AD=AD, hinh=_hinh_cong_troi(BC, CD, BD, AB, AD, "m"))


def _ltr_mc_sa(cv, socau, dang):
    cau = ""
    so = 0
    while so < socau:
        c = _ltr_cau(cv)
        dap = c["f"](c["S"])
        if dang == 2 and len(dap) > 4:
            continue
        so += 1
        if dang == 1:
            debai = c["intro"] + r" The area of %s (%s) is" % (c["ten"], c["donvi"])
            sai = [c["f"](c["S1"]), c["f"](c["S2"]), str(_lt(c["S"])) if cv else c["f"](2 * c["S"])]
            nh = _ba_nhieu(dap, sai, buoc=lambda t: _x1(c["S"] / 1e4 + 0.1 * t, 1) if cv else str(_lt(c["S"]) + 5 * t))
        else:
            debai = c["intro"] + r" Find the area of %s (%s)." % (c["ten"], c["donvi"])
            nh = [_x1(c["S"] / 1e4 + 0.1 * d, 1) if cv else str(_lt(c["S"]) + d) for d in (1, -1, 2)]
        cau += MC_SA_answer_const(debai, dap, nh, c["giai"], c["hinh"], 0, dang)
    return cau


def _ltr_tl(cv, socau, dong):
    cau = ""
    for _ in range(socau):
        c = _ltr_cau(cv)
        if random.random() < 0.5:
            tg, ba, Sa, tg2, ba2, Sb = "BCD", (c["BC"], c["CD"], c["BD"]), c["S1"], "ABD", (c["AB"], c["AD"], c["BD"]), c["S2"]
        else:
            tg, ba, Sa, tg2, ba2, Sb = "ABD", (c["AB"], c["AD"], c["BD"]), c["S2"], "BCD", (c["BC"], c["CD"], c["BD"]), c["S1"]
        ds = [(r"Find the area of triangle $%s$ (in $\text{m}^{2}$, rounded to the nearest whole number)." % tg,
               r"S_{%s} \approx %d\,\text{m}^{2}" % (tg, _lt(Sa)), _giai_heron_m(tg, *ba, Sa)),
              (r"Find the area of %s (%s)." % (c["ten"], c["donvi"]),
               r"S \approx %s%s" % (c["f"](c["S"]), c["dv"]),
               _giai_heron_m(tg2, *ba2, Sb) + "\\\\\n" + c["duoi"])]
        cau += TL_answer_text(c["intro"], ds, c["hinh"], 0, dong)
    return cau


def L10_C3_B6_VD036_MC_J_02(socau, dang=1):
    r"""Diện tích vùng đất tứ giác, Heron hai lần: Công viên Lê Thị Riêng - công viên (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo cạnh giả định, diện tích sát số thật).
    """
    return _ltr_mc_sa(True, socau, 1)


def L10_C3_B6_VD036_MC_J_03(socau, dang=1):
    r"""Diện tích vùng đất tứ giác, Heron hai lần: Công viên Lê Thị Riêng - khu vực rãnh mộ (ngẫu nhiên) (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo cạnh giả định, diện tích sát số thật).
    """
    return _ltr_mc_sa(False, socau, 1)


def L10_C3_B6_VD036_SA_J_02(socau, dang=2):
    r"""Diện tích vùng đất tứ giác, Heron hai lần: Công viên Lê Thị Riêng - công viên (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo cạnh giả định, diện tích sát số thật).
    """
    return _ltr_mc_sa(True, socau, 2)


def L10_C3_B6_VD036_SA_J_03(socau, dang=2):
    r"""Diện tích vùng đất tứ giác, Heron hai lần: Công viên Lê Thị Riêng - khu vực rãnh mộ (ngẫu nhiên) (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo cạnh giả định, diện tích sát số thật).
    """
    return _ltr_mc_sa(False, socau, 2)


def L10_C3_B6_VD036_TL_I_02(socau, dong=1):
    r"""Tự luận: a) (VD) diện tích một tam giác, b) (VDC) diện tích công viên - Công viên Lê Thị Riêng (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo cạnh giả định, diện tích sát số thật).
    """
    return _ltr_tl(True, socau, dong)


def L10_C3_B6_VD036_TL_I_03(socau, dong=1):
    r"""Tự luận: a) (VD) diện tích một tam giác, b) (VDC) diện tích khu vực rãnh mộ (ngẫu nhiên) - Công viên Lê Thị Riêng (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo cạnh giả định, diện tích sát số thật).
    """
    return _ltr_tl(False, socau, dong)


# =====================================================================================================
# BÀI TOÁN THỰC TIỄN GẮN VỚI ĐƯỜNG TRƯỜNG SƠN (cô Lan 13/10/2026)
# Năm bối cảnh là NĂM BIẾN THỂ _01.._05 của CÙNG một dạng (cùng ID): chọn ID đó thì mỗi đề chỉ ra MỘT bối cảnh.
#   _01 trạm bơm tiếp sức vượt đèo (tam giác vuông)          _02 bản đồ cố ý dịch vị trí >= 10 km (côsin, sin)
#   _03 tổ khảo sát đi theo phương vị (côsin, sin)           _04 kéo ống vòng sau trận đánh phá (côsin)
#   _05 rừng cháy sau trận B-52 ở suối Ra Vơ (Heron, đường cao)
# Mỗi bối cảnh có hai câu hỏi: ý a) mức VD, ý b) mức VDC (đúng quy ước câu tự luận một đơn vị mức VD):
#   TL_N: ý a) + ý b);  MC_U / SA_W: hỏi như ý a) (VD);  MC_V / SA_X: hỏi như ý b) (VDC, muc_do_dang = VDC).
# Số liệu LẤY TỪ BÁO CHÍ chỉ có ở phần dẫn (tuyến ống 6/1968-2/1975, đèo Mụ Giạ 700 m, bản đồ 1:500 000 dịch >= 10 km,
# trận B-52 ngày 6/9/1969 ở suối Ra Vơ, tổ khảo sát "cắt rừng theo phương vị"); mọi số đo trong đề là GIẢ SỬ.
# Hình vẽ TikZ theo đúng số liệu của từng đề; đề không có dữ kiện góc đo bằng Google Maps.
# =====================================================================================================

# Phần dẫn chung (số liệu và lời nói có nguồn, cô Lan 13/10/2026): câu "huyền thoại trong huyền thoại" là lời Tư lệnh
# Đồng Sỹ Nguyên (VINPA - Hiệp hội Xăng dầu Việt Nam, bài "Đường ống xăng dầu Trường Sơn - một dòng sông mang lửa");
# "hàng trăm cán bộ, chiến sĩ đã ngã xuống", xăng dầu phục vụ Chiến dịch Hồ Chí Minh: cùng bài; đường Trường Sơn
# gần 20 000 km, 1959-1975, "một trong những nhân tố chiến lược có ý nghĩa quyết định" (Đại tướng Võ Nguyên Giáp):
# Báo Pháp Luật Việt Nam 18/5/2009. Chỉ chữ trong phần dẫn, không phải dữ kiện để tính.
_TS_DAN_ONG = (r"The Truong Son Road is called the legendary road; and the Truong Son petroleum pipeline, in the words of "
               r"Lieutenant General Dong Sy Nguyen, is ``a legend among legends''. From late 1968 to 1975, the flow of petroleum "
               r"ran through old forests and over high passes, amid bombs and bullets, to bring fuel to the southern battlefield, serving even the Ho Chi Minh "
               r"Campaign of 1975; hundreds of cadres and soldiers fell along that pipeline. Today, sitting in a peaceful "
               r"classroom, we are grateful to those who sacrificed so that we may have peace, independence and unification. ")
_TS_DAN_DUONG = (r"The Truong Son Road is nearly $20\,000$ km long and was opened and held for $16$ years (1959-1975); it is called the "
                 r"legendary road. General Vo Nguyen Giap regarded it as one of the strategic factors of decisive significance "
                 r"in leading the resistance war to victory. Countless cadres and soldiers fell to keep that road open. "
                 r"Today, sitting in a peaceful classroom, we are grateful to those who sacrificed so that we may have peace, independence and "
                 r"unification. ")


def _ts_hinh_bom(H, al):
    k = 7.0
    y = k * math.tan(math.radians(al))
    s = "\\begin{tikzpicture}[scale=0.8,font=\\footnotesize,line join=round]\n"
    s += "\\draw[thick] (0,0) -- (%.2f,0) -- (%.2f,%.2f) -- cycle;\n" % (k, k, y)
    for i in range(6):
        x0, y0, x1, y1 = k * i / 6, y * i / 6, k * (i + 1) / 6, y * (i + 1) / 6
        s += "\\draw[gray,dashed] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f);\n" % (x0, y0, x1, y0, x1, y1)
    s += "\\draw (%.2f,0) -- (%.2f,0.3) -- (%.2f,0.3);\n" % (k - 0.3, k - 0.3, k)
    s += "\\draw (1.5,0) arc (0:%.2f:1.5);\n" % al
    s += "\\node at (%.2f,%.2f) {$%s$};\n" % (2.1 * math.cos(math.radians(al / 2)), 2.1 * math.sin(math.radians(al / 2)), _goc(al))
    s += "\\fill (0,0) circle (0.06) node[left] {$A$};\n"
    s += "\\fill (%.2f,0) circle (0.06) node[below] {$B$};\n" % k
    s += "\\fill (%.2f,%.2f) circle (0.06) node[above] {$C$};\n" % (k, y)
    s += "\\node[right] at (%.2f,%.2f) {$BC = %d$ m};\n" % (k, y / 2, H)
    s += "\\node[gray,font=\\scriptsize] at (%.2f,-0.6) {dashed: staircase layout (illustration)};\n" % (k / 2)
    return s + "\\end{tikzpicture}"


def _ts_bom():
    """Trạm bơm tiếp sức: a) số trạm bơm tối thiểu; b) độ dài tối thiểu của ống bám sườn dốc AC."""
    while True:
        H = random.randrange(600, 801, 20)
        al = random.randint(14, 22)
        h = random.choice([100, 110, 120])
        if H % h == 0:
            continue
        AC = H / _sin_d(al)
        if _xa_bien(AC, 0) and len(str(_lt(AC))) <= 4:
            break
    n = -(-H // h)
    intro = (_TS_DAN_ONG + r"The pipeline had to cross many high passes. A single pump is not strong enough "
             r"to push gasoline in one go up to a high peak, so the soldiers set up relay pumping stations: the pipe goes up one stretch, turns sideways along the mountainside "
             r"to reduce the pressure, enters a pumping station and only then continues upward, forming a staircase shape. With ingenuity and human strength, the soldiers "
             r"carried the flow of gasoline over mountains that seemed impossible to cross. Suppose each pumping station can raise the gasoline by at most "
             r"$%d$ m. For simplicity, we ignore the horizontal sections of the pipe and treat the pipe as running straight along the slope from the foot $A$ up to "
             r"the peak $C$ of a mountain $%d$ m high above the foot ($BC = %d$ m, $B$ is the projection of $C$ onto the horizontal plane "
             r"through $A$), and the mountain slope is inclined at an angle of $%s$ to the horizontal plane (see figure)." % (h, H, H, _goc(al)))
    ga = (r"Each pumping station can raise the gasoline by at most $%d$ m, so $\dfrac{%d}{%d} \approx %s$ stations are needed; since the number of stations is an integer, "
          r"at least $%d$ pumping stations are needed (with $%d$ stations the gasoline can be raised at most $%d$ m, which is less than $%d$ m)."
          % (h, H, h, _xx(H / h, 2), n, n - 1, (n - 1) * h, H))
    gb = (r"In triangle $ABC$ with a right angle at $B$: $\sin\widehat{BAC} = \dfrac{BC}{AC}$, so "
          r"$AC = \dfrac{BC}{\sin %s} = \dfrac{%d}{\sin %s} \approx %d$ m. This is the \textbf{minimum} length, because in reality the pipe also "
          r"has horizontal sections in the staircase shape." % (_goc(al), H, _goc(al), _lt(AC)))
    return {
        "intro": intro, "fig": _ts_hinh_bom(H, al),
        "hoi": {"a": r"At least how many pumping stations are needed to bring the gasoline from the foot of the slope to the peak?",
                "b": r"Find the minimum length of the pipe section $AC$ (in meters, rounded to the nearest whole number)."},
        "v": {"a": n, "b": AC}, "n": {"a": 0, "b": 0}, "buoc": {"a": 1, "b": 37},
        "sai": {"a": [n - 1, n + 1, n + 2, round(H / h)], "b": [H * _sin_d(al), H / _sin_d(90 - al), H / math.tan(math.radians(al)), H * math.tan(math.radians(al))]},
        "ga": ga, "gb": gb,
        "ya": r"%d \text{ pumping stations}" % n, "yb": r"AC \approx %d\,\text{m}" % _lt(AC),
    }


def _ts_hinh_ban_do(d, th):
    k = 5.0 / d
    kx = d * k
    p = (kx - 10 * k * math.cos(math.radians(th)), 10 * k * math.sin(math.radians(th)))
    a0 = 180 - th
    s = "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
    s += "\\draw[very thick] (0,0) -- (%.2f,0);\n" % kx
    s += "\\draw[very thick] (%.2f,0) -- (%.2f,%.2f);\n" % (kx, p[0], p[1])
    s += "\\draw[red!70!black,dashed,thick] (0,0) -- (%.2f,%.2f);\n" % p
    s += "\\draw (%.2f,%.2f) arc (%d:180:0.8);\n" % (kx + 0.8 * math.cos(math.radians(a0)), 0.8 * math.sin(math.radians(a0)), a0)
    s += "\\node at (%.2f,%.2f) {$%s$};\n" % (kx + 1.15 * math.cos(math.radians(a0 + th / 2)), 1.15 * math.sin(math.radians(a0 + th / 2)), _goc(th))
    s += "\\fill (0,0) circle (0.06) node[left] {$O$ (command post)};\n"
    s += "\\fill (%.2f,0) circle (0.06) node[below right] {$K$ (real depot)};\n" % kx
    s += "\\fill (%.2f,%.2f) circle (0.06) node[above] {$K'$ (on the map)};\n" % p
    s += "\\node[below] at (%.2f,0) {$%d$ km};\n" % (kx / 2, d)
    s += "\\node[right] at (%.2f,%.2f) {$10$ km};\n" % ((kx + p[0]) / 2 + 0.05, p[1] / 2)
    return s + "\\end{tikzpicture}"


def _ts_ban_do():
    """Bản đồ cố ý dịch vị trí >= 10 km: a) OK' (định lí côsin); b) góc KOK' (định lí sin)."""
    while True:
        d = random.randint(18, 32)
        th = random.randint(50, 130)
        OK2 = d * d + 100 - 20 * d * math.cos(math.radians(th))
        OKp = math.sqrt(OK2)
        goc = math.degrees(math.asin(10 * _sin_d(th) / OKp))
        if OKp > 10 and _xa_bien(OKp, 1) and _xa_bien(goc, 0) and len(_so(OKp, 1)) <= 4:
            break
    intro = (_TS_DAN_DUONG + r"In early 1969, the operational map of the Truong Son Road was drawn at a scale of $1:500\,000$. To prevent the map from falling into enemy hands, "
             r"higher command ordered that the positions of units be deliberately shifted by at least $10$ km before submission. A deliberately misplaced pen stroke could "
             r"save an entire depot from bombs and bullets. Suppose a real gasoline depot is at point $K$, at a distance from the command post $O$ of $OK = %d$ km; "
             r"on the submitted map, the depot is recorded at point $K'$ with $KK' = 10$ km and $\widehat{OKK'} = %s$ (see figure)."
             % (d, _goc(th)))
    ga = (r"In triangle $OKK'$, by the law of cosines: $OK'^{2} = OK^{2} + KK'^{2} - 2 \cdot OK \cdot KK' \cdot \cos\widehat{OKK'} "
          r"= %d^{2} + 10^{2} - 2 \cdot %d \cdot 10 \cdot \cos %s \approx %s$, so $OK' \approx %s$ km."
          % (d, d, _goc(th), _xx(OK2, 2), _x1(OKp, 1)))
    gb = (ga + "\\\\\n" + r"By the law of sines: $\dfrac{KK'}{\sin\widehat{KOK'}} = \dfrac{OK'}{\sin\widehat{OKK'}}$, which gives "
          r"$\sin\widehat{KOK'} = \dfrac{10 \cdot \sin %s}{OK'} \approx %s$, so $\widehat{KOK'} \approx %d^{\circ}$ "
          r"(an acute angle since $KK' < OK$)." % (_goc(th), _xx(10 * _sin_d(th) / OKp, 3), _lt(goc)))
    gp = 180 - th - goc
    return {
        "intro": intro, "fig": _ts_hinh_ban_do(d, th),
        "hoi": {"a": r"Find the distance $OK'$ from the command post to the position recorded on the map (in kilometers, rounded to the nearest tenth).",
                "b": r"As seen from $O$, the direction to the depot recorded on the map differs from the direction to the real depot by the angle "
                     r"$\widehat{KOK'}$. How many degrees is this angle (rounded to the nearest whole number)?"},
        "v": {"a": OKp, "b": goc}, "n": {"a": 1, "b": 0}, "buoc": {"a": 0.7, "b": 3},
        "sai": {"a": [math.sqrt(d * d + 100), d + 10, math.sqrt(d * d + 100 + 20 * d * math.cos(math.radians(th))), math.sqrt(abs(d * d - 100))],
                "b": [gp, 180 - th, math.degrees(math.asin(10 * _sin_d(th) / d)), math.degrees(math.atan(10 * _sin_d(th) / d))]},
        "ga": ga, "gb": gb,
        "ya": r"OK' \approx %s\,\text{km}" % _x1(OKp, 1), "yb": r"\widehat{KOK'} \approx %d^{\circ}" % _lt(goc),
    }


def _ts_hinh_phuong_vi(d1, d2, a1, a2):
    B = (d1 * math.sin(math.radians(a1)), d1 * math.cos(math.radians(a1)))
    C = (B[0] + d2 * math.sin(math.radians(a2)), B[1] + d2 * math.cos(math.radians(a2)))
    xs, ys = [0, B[0], C[0]], [0, B[1], C[1]]
    k = 3.6 / max(max(xs) - min(xs), max(ys) - min(ys))
    B, C = (B[0] * k, B[1] * k), (C[0] * k, C[1] * k)
    r = 0.75

    def cung(P, a, ten):
        m = math.radians(90 - a / 2)
        return ("\\draw[->] (%.2f,%.2f) arc (90:%.1f:%.2f);\n" % (P[0], P[1] + r, 90 - a, r)
                + "\\node at (%.2f,%.2f) {$%s$};\n" % (P[0] + (r + 0.38) * math.cos(m), P[1] + (r + 0.38) * math.sin(m), ten))
    s = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s += "\\draw[dashed,gray] (0,0) -- (0,1.35) node[above] {North};\n"
    s += "\\draw[dashed,gray] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (B[0], B[1], B[0], B[1] + 1.35)
    s += "\\draw[very thick,blue!60!black] (0,0) -- (%.2f,%.2f) -- (%.2f,%.2f);\n" % (B + C)
    s += "\\draw[dashed,red!70!black,thick] (0,0) -- (%.2f,%.2f);\n" % C
    s += cung((0, 0), a1, _goc(a1)) + cung(B, a2, _goc(a2))
    s += "\\fill (0,0) circle (0.06) node[below] {$A$};\n"
    s += "\\fill (%.2f,%.2f) circle (0.06) node[above left] {$B$};\n" % B
    s += "\\fill (%.2f,%.2f) circle (0.06) node[right] {$C$};\n" % C
    # nhãn độ dài: AB nằm bên phải đoạn AB (trong tam giác), BC nằm phía ngoài (xa A)
    n1 = (math.cos(math.radians(a1)), -math.sin(math.radians(a1)))
    m2 = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
    n2 = (math.cos(math.radians(a2)), -math.sin(math.radians(a2)))
    if n2[0] * (0 - m2[0]) + n2[1] * (0 - m2[1]) > 0:
        n2 = (-n2[0], -n2[1])
    s += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d$ km};\n" % (B[0] / 2 + 0.3 * n1[0], B[1] / 2 + 0.3 * n1[1], d1)
    s += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d$ km};\n" % (m2[0] + 0.32 * n2[0], m2[1] + 0.32 * n2[1], d2)
    return s + "\\end{tikzpicture}"


def _ts_phuong_vi():
    """Tổ khảo sát đi theo phương vị: a) khoảng cách AC (côsin); b) phương vị của AC (sin/côsin)."""
    while True:
        a1 = random.randint(20, 70)
        de = random.randint(40, 110)
        a2 = a1 + de
        d1, d2 = random.randint(4, 9), random.randint(4, 9)
        AC2 = d1 * d1 + d2 * d2 + 2 * d1 * d2 * math.cos(math.radians(de))
        AC = math.sqrt(AC2)
        gam = math.degrees(math.acos((d1 * d1 + AC2 - d2 * d2) / (2 * d1 * AC)))
        pv = a1 + gam
        if _xa_bien(AC, 1) and _xa_bien(pv, 0) and len(_so(AC, 1)) <= 4:
            break
    intro = (_TS_DAN_ONG + r"To open the petroleum pipeline through the forests and mountains of Truong Son, survey teams had to ``cut through the forest along a bearing'' or follow "
             r"streams and cross mountain peaks along the watershed. The engineers and soldiers of the survey teams pushed through forests and crossed streams to "
             r"find a path for the flow of gasoline. The \textit{bearing} of a direction is the angle measured clockwise from the north "
             r"direction to that direction. Suppose a survey team starts from $A$, travels $%d$ km on a bearing of $%s$ to $B$, then changes "
             r"direction and travels another $%d$ km on a bearing of $%s$ to $C$ (see figure)." % (d1, _goc(a1), d2, _goc(a2)))
    ga = (r"The bearing of direction $BA$ is $%d^{\circ} + 180^{\circ}$, the bearing of direction $BC$ is $%s$, so "
          r"$\widehat{ABC} = 180^{\circ} - (%d^{\circ} - %d^{\circ}) = %d^{\circ}$." "\\\\\n"
          r"By the law of cosines: $AC^{2} = %d^{2} + %d^{2} - 2 \cdot %d \cdot %d \cdot \cos %d^{\circ} \approx %s$, so $AC \approx %s$ km."
          % (a1, _goc(a2), a2, a1, 180 - de, d1, d2, d1, d2, 180 - de, _xx(AC2, 2), _x1(AC, 1)))
    gb = (ga + "\\\\\n" + r"In triangle $ABC$: $\cos\widehat{BAC} = \dfrac{AB^{2} + AC^{2} - BC^{2}}{2 \cdot AB \cdot AC} "
          r"= \dfrac{%d^{2} + %s^{2} - %d^{2}}{2 \cdot %d \cdot %s} \approx %s$, so $\widehat{BAC} \approx %s^{\circ}$." "\\\\\n"
          r"Point $C$ lies to the right of direction $AB$ (the change of direction is to the right), so the bearing of $AC$ is "
          r"$%d^{\circ} + \widehat{BAC} \approx %d^{\circ}$."
          % (d1, _x1(AC, 1), d2, d1, _x1(AC, 1), _xx(math.cos(math.radians(gam)), 3), _xx(gam, 1), a1, _lt(pv)))
    ac_sai = math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * math.cos(math.radians(de)))
    return {
        "intro": intro, "fig": _ts_hinh_phuong_vi(d1, d2, a1, a2),
        "hoi": {"a": r"Find the distance $AC$ from the starting point to the end point (in kilometers, rounded to the nearest tenth).",
                "b": r"To go straight from $A$ to $C$, on what bearing, in degrees, must the team travel (rounded to the nearest whole number)?"},
        "v": {"a": AC, "b": pv}, "n": {"a": 1, "b": 0}, "buoc": {"a": 0.6, "b": 4},
        "sai": {"a": [d1 + d2, ac_sai, math.sqrt(d1 * d1 + d2 * d2), abs(d1 - d2) + 1.5],
                "b": [a1 - gam, a2 - gam, a1 + (180 - de - gam), a1 + 180 - gam]},
        "ga": ga, "gb": gb,
        "ya": r"AC \approx %s\,\text{km}" % _x1(AC, 1), "yb": r"\text{bearing} \approx %d^{\circ}" % _lt(pv),
    }


def _ts_hinh_ong_vong(AC, CB, ang):
    AB2 = AC * AC + CB * CB - 2 * AC * CB * math.cos(math.radians(ang))
    AB = math.sqrt(AB2)
    k = 7.2 / AB
    cx = (AC * AC + AB2 - CB * CB) / (2 * AB) * k
    cy = math.sqrt(max(AC * AC * k * k - cx * cx, 0))
    s = "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
    s += "\\fill[red!15] (%.2f,0.1) ellipse (0.9 and 0.45);\n" % (3.6)
    s += "\\node[red!60!black,font=\\scriptsize] at (3.6,0.5) {bomb field};\n"
    s += "\\draw[dashed] (0,0) -- (7.2,0);\n"
    s += "\\draw[very thick,blue!60!black] (0,0) -- (%.2f,%.2f) -- (7.2,0);\n" % (cx, cy)
    s += "\\fill (0,0) circle (0.05) node[left] {$A$};\\fill (7.2,0) circle (0.05) node[right] {$B$};\n"
    s += "\\fill (%.2f,%.2f) circle (0.05) node[above] {$C$};\n" % (cx, cy)
    s += "\\node[above left] at (%.2f,%.2f) {$%d$ m}; \\node[above right] at (%.2f,%.2f) {$%d$ m};\n" % (cx / 2, cy / 2, AC, (cx + 7.2) / 2, cy / 2, CB)
    t1 = math.degrees(math.atan2(-cy, -cx))
    t2 = math.degrees(math.atan2(-cy, 7.2 - cx))
    tm = math.radians((t1 + t2) / 2)
    s += "\\draw (%.2f,%.2f) arc (%.1f:%.1f:0.6);\n" % (cx + 0.6 * math.cos(math.radians(t1)), cy + 0.6 * math.sin(math.radians(t1)), t1, t2)
    s += "\\node at (%.2f,%.2f) {$%s$};\n" % (cx + 1.0 * math.cos(tm), cy + 1.0 * math.sin(tm), _goc(ang))
    return s + "\\end{tikzpicture}"


def _ts_ong_vong():
    """Kéo ống vòng qua bãi bom: a) khoảng cách thẳng AB (côsin); b) số mét ống phải kéo thêm."""
    while True:
        AC = random.randrange(400, 501, 10)
        CB = random.randrange(480, 561, 10)
        ang = random.randint(105, 130)
        AB = math.sqrt(AC * AC + CB * CB - 2 * AC * CB * math.cos(math.radians(ang)))
        if _xa_bien(AB, 0):
            break
    them = AC + CB - AB
    intro = (_TS_DAN_ONG + r"The pipeline was frequently bombed by American aircraft; some raids set hundreds of hectares of forest on fire and damaged "
             r"both the depots and the pipes (such as the B-52 bombing of the Ra Vo stream area on $6/9/1969$ (day/month/year)). Despite the fierce bombing, the soldiers "
             r"resolutely reconnected the pipe section by section so that the flow of gasoline was not interrupted. Suppose the straight pipe section from station $A$ to station $B$ "
             r"was destroyed, with a field of unexploded bombs in the middle of the route; the soldiers had to lay new pipe detouring through point $C$ outside the bomb field, with "
             r"$AC = %d$ m, $CB = %d$ m and $\widehat{ACB} = %s$ (see figure)." % (AC, CB, _goc(ang)))
    ga = (r"By the law of cosines in triangle $ABC$: $AB^{2} = %d^{2} + %d^{2} - 2 \cdot %d \cdot %d \cdot \cos %s \approx %s$, "
          r"so $AB \approx %d$ m." % (AC, CB, AC, CB, _goc(ang), _xx(AB * AB, 0), _lt(AB)))
    gb = (ga + "\\\\\n" + r"The detour has length $AC + CB = %d + %d = %d$ m, so $%d - %d = %d$ m more pipe must be laid than for the straight route."
          % (AC, CB, AC + CB, AC + CB, _lt(AB), AC + CB - _lt(AB)))
    return {
        "intro": intro, "fig": _ts_hinh_ong_vong(AC, CB, ang),
        "hoi": {"a": r"Find the straight-line distance $AB$ (in meters, rounded to the nearest whole number).",
                "b": r"By how many meters of pipe is the detour through $C$ longer than the straight route from $A$ to $B$ (rounded to the nearest whole number)?"},
        "v": {"a": AB, "b": them}, "n": {"a": 0, "b": 0}, "buoc": {"a": 9, "b": 9},
        "sai": {"a": [AC + CB, math.sqrt(AC * AC + CB * CB), math.sqrt(AC * AC + CB * CB + 2 * AC * CB * math.cos(math.radians(ang))), AB * AB],
                "b": [AB, AC + CB, AC + CB - math.sqrt(AC * AC + CB * CB), abs(AC - CB)]},
        "ga": ga, "gb": gb,
        "ya": r"AB \approx %d\,\text{m}" % _lt(AB), "yb": r"%d\,\text{m}" % (AC + CB - _lt(AB)),
    }


def _ts_hinh_rung_chay(a, b, c, S):
    k = 4.8 / a
    x = (a * a + c * c - b * b) / (2 * a) * k
    y = math.sqrt(max(c * c * k * k - x * x, 0))
    s = "\\begin{tikzpicture}[scale=0.9,font=\\footnotesize,line join=round]\n"
    s += "\\fill[orange!25] (0,0) -- (%.2f,0) -- (%.2f,%.2f) -- cycle;\n" % (4.8, x, y)
    s += "\\draw[very thick] (0,0) -- (%.2f,%.2f) -- (4.8,0);\n" % (x, y)
    s += "\\draw[very thick,blue!60!black] (0,0) -- (4.8,0);\n"
    s += "\\node[blue!60!black,font=\\scriptsize] at (2.4,-0.65) {pipeline $BC$};\n"
    s += "\\fill (0,0) circle (0.05) node[below left] {$B$};\\fill (4.8,0) circle (0.05) node[below right] {$C$};\n"
    s += "\\fill (%.2f,%.2f) circle (0.05) node[above] {$A$};\n" % (x, y)
    s += "\\node at (%.2f,%.2f) {forest fire};\n" % ((x + 4.8) / 3, y / 3)
    s += "\\node[left] at (%.2f,%.2f) {$%s$ km};\n" % (x / 2, y / 2, _xx(c, 1))
    s += "\\node[right] at (%.2f,%.2f) {$%s$ km};\n" % ((x + 4.8) / 2, y / 2, _xx(b, 1))
    s += "\\node[above] at (2.4,0) {$%s$ km};\n" % _xx(a, 1)
    return s + "\\end{tikzpicture}"


def _ts_rung_chay():
    """Rừng cháy sau trận B-52: a) diện tích (Heron); b) đoạn đường ngắn nhất từ A đến đường ống BC (đường cao)."""
    while True:
        c = random.randint(18, 26) / 10
        a = random.randint(20, 28) / 10
        b = random.randint(24, 32) / 10
        if not (a + b > c + 0.4 and a + c > b + 0.4 and b + c > a + 0.4):
            continue
        p = (a + b + c) / 2
        S = math.sqrt(p * (p - a) * (p - b) * (p - c))
        ha = 2 * S / a
        if _xa_bien(S, 2) and _xa_bien(ha, 2) and S > 1.5:
            break
    intro = (_TS_DAN_ONG + r"On $6/9/1969$ (day/month/year), American B-52s bombed the Ra Vo stream area, setting hundreds of hectares of forest on fire and damaging "
             r"the depots and petroleum pipelines there. Even so, the soldiers resolutely stayed on the route, keeping the gasoline flowing. "
             r"Suppose the burned forest region is outlined as triangle $ABC$ with $AB = %s$ km, $BC = %s$ km, $CA = %s$ km, where side $BC$ "
             r"lies along the pipeline (see figure)." % (_xx(c, 1), _xx(a, 1), _xx(b, 1)))
    ga = (r"The semiperimeter is $p = \dfrac{%s + %s + %s}{2} = %s$ km. By Heron's formula: "
          r"$S = \sqrt{%s \cdot %s \cdot %s \cdot %s} \approx %s\,\text{km}^{2}$."
          % (_xx(c, 1), _xx(a, 1), _xx(b, 1), _xx(p, 2), _xx(p, 2), _xx(p - a, 2), _xx(p - b, 2), _xx(p - c, 2), _x1(S, 2)))
    gb = (ga + "\\\\\n" + r"The shortest path from $A$ to the pipeline $BC$ is the altitude $h_a$ dropped from $A$ to $BC$: "
          r"$S = \dfrac{1}{2} \cdot BC \cdot h_a$, so $h_a = \dfrac{2S}{BC} \approx \dfrac{2 \cdot %s}{%s} \approx %s$ km."
          % (_x1(S, 2), _xx(a, 1), _x1(ha, 2)))
    return {
        "intro": intro, "fig": _ts_hinh_rung_chay(a, b, c, S),
        "hoi": {"a": r"Find the area of the burned forest region (in $\text{km}^{2}$, rounded to the nearest hundredth).",
                "b": r"The firefighting team at $A$ wants to reach the pipeline $BC$ by the shortest route. Find the length of that route (in kilometers, "
                     r"rounded to the nearest hundredth)."},
        "v": {"a": S, "b": ha}, "n": {"a": 2, "b": 2}, "buoc": {"a": 0.13, "b": 0.11},
        "sai": {"a": [S / 2, 2 * S, a * b / 2, a * c / 2],
                "b": [S / a, 2 * S / b, 2 * S / c, S * a / 2]},
        "ga": ga, "gb": gb,
        "ya": r"S \approx %s\,\text{km}^{2}" % _x1(S, 2), "yb": r"h_a \approx %s\,\text{km}" % _x1(ha, 2),
    }


_TS_BOI_CANH = [_ts_bom, _ts_ban_do, _ts_phuong_vi, _ts_ong_vong, _ts_rung_chay]


def _ts_dinh_dang(x, n):
    return _x1(x, n) if n else str(_lt(x))


def _ts_mc_sa(bien, ph, socau, dang):
    """MC (dang = 1) / SA (dang = 2) của bối cảnh số `bien` (1..5); ph = "a" (VD) hoặc "b" (VDC)."""
    cau = ""
    for _ in range(socau):
        c = _TS_BOI_CANH[bien - 1]()
        n, v, st = c["n"][ph], c["v"][ph], c["buoc"][ph]
        dap = _ts_dinh_dang(v, n) if dang == 1 else _so(v, n)
        mau = _ts_dinh_dang if dang == 1 else _so
        nh = _ba_nhieu(dap, [mau(x, n) for x in c["sai"][ph] if x > 0], buoc=lambda t: mau(v + t * st, n))
        giai = c["ga"] if ph == "a" else c["gb"]
        cau += MC_SA_answer_const(c["intro"] + " " + c["hoi"][ph], dap, nh, giai, c["fig"], 0, dang)
    return cau


def _ts_tl(bien, socau, dong):
    cau = ""
    for _ in range(socau):
        c = _TS_BOI_CANH[bien - 1]()
        ds = [(c["hoi"]["a"], c["ya"], c["ga"]), (c["hoi"]["b"], c["yb"], c["gb"])]
        cau += TL_answer_text(c["intro"], ds, c["fig"], 0, dong)
    return cau


def L10_C3_B6_VD036_MC_U_01(socau, dang=1):
    r"""Trường Sơn - trạm bơm tiếp sức vượt đèo (mức VD, hỏi như ý a) - biến thể 1/5 của dạng: trạm bơm tiếp sức vượt đèo.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(1, "a", socau, 1)

def L10_C3_B6_VD036_MC_U_02(socau, dang=1):
    r"""Trường Sơn - bản đồ cố ý dịch vị trí (mức VD, hỏi như ý a) - biến thể 2/5 của dạng: bản đồ cố ý dịch vị trí.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(2, "a", socau, 1)

def L10_C3_B6_VD036_MC_U_03(socau, dang=1):
    r"""Trường Sơn - tổ khảo sát đi theo phương vị (mức VD, hỏi như ý a) - biến thể 3/5 của dạng: tổ khảo sát đi theo phương vị.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(3, "a", socau, 1)

def L10_C3_B6_VD036_MC_U_04(socau, dang=1):
    r"""Trường Sơn - kéo ống vòng sau trận đánh phá (mức VD, hỏi như ý a) - biến thể 4/5 của dạng: kéo ống vòng sau trận đánh phá.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(4, "a", socau, 1)

def L10_C3_B6_VD036_MC_U_05(socau, dang=1):
    r"""Trường Sơn - rừng cháy sau trận B-52 (mức VD, hỏi như ý a) - biến thể 5/5 của dạng: rừng cháy sau trận B-52.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(5, "a", socau, 1)

def L10_C3_B6_VD036_MC_V_01(socau, dang=1):
    r"""Trường Sơn - trạm bơm tiếp sức vượt đèo (mức VDC, hỏi như ý b) - biến thể 1/5 của dạng: trạm bơm tiếp sức vượt đèo.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(1, "b", socau, 1)

def L10_C3_B6_VD036_MC_V_02(socau, dang=1):
    r"""Trường Sơn - bản đồ cố ý dịch vị trí (mức VDC, hỏi như ý b) - biến thể 2/5 của dạng: bản đồ cố ý dịch vị trí.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(2, "b", socau, 1)

def L10_C3_B6_VD036_MC_V_03(socau, dang=1):
    r"""Trường Sơn - tổ khảo sát đi theo phương vị (mức VDC, hỏi như ý b) - biến thể 3/5 của dạng: tổ khảo sát đi theo phương vị.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(3, "b", socau, 1)

def L10_C3_B6_VD036_MC_V_04(socau, dang=1):
    r"""Trường Sơn - kéo ống vòng sau trận đánh phá (mức VDC, hỏi như ý b) - biến thể 4/5 của dạng: kéo ống vòng sau trận đánh phá.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(4, "b", socau, 1)

def L10_C3_B6_VD036_MC_V_05(socau, dang=1):
    r"""Trường Sơn - rừng cháy sau trận B-52 (mức VDC, hỏi như ý b) - biến thể 5/5 của dạng: rừng cháy sau trận B-52.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(5, "b", socau, 1)

def L10_C3_B6_VD036_SA_U_01(socau, dang=2):
    r"""Trường Sơn - trạm bơm tiếp sức vượt đèo (mức VD, hỏi như ý a) - biến thể 1/5 của dạng: trạm bơm tiếp sức vượt đèo.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(1, "a", socau, 2)

def L10_C3_B6_VD036_SA_U_02(socau, dang=2):
    r"""Trường Sơn - bản đồ cố ý dịch vị trí (mức VD, hỏi như ý a) - biến thể 2/5 của dạng: bản đồ cố ý dịch vị trí.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(2, "a", socau, 2)

def L10_C3_B6_VD036_SA_U_03(socau, dang=2):
    r"""Trường Sơn - tổ khảo sát đi theo phương vị (mức VD, hỏi như ý a) - biến thể 3/5 của dạng: tổ khảo sát đi theo phương vị.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(3, "a", socau, 2)

def L10_C3_B6_VD036_SA_U_04(socau, dang=2):
    r"""Trường Sơn - kéo ống vòng sau trận đánh phá (mức VD, hỏi như ý a) - biến thể 4/5 của dạng: kéo ống vòng sau trận đánh phá.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(4, "a", socau, 2)

def L10_C3_B6_VD036_SA_U_05(socau, dang=2):
    r"""Trường Sơn - rừng cháy sau trận B-52 (mức VD, hỏi như ý a) - biến thể 5/5 của dạng: rừng cháy sau trận B-52.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(5, "a", socau, 2)

def L10_C3_B6_VD036_SA_V_01(socau, dang=2):
    r"""Trường Sơn - trạm bơm tiếp sức vượt đèo (mức VDC, hỏi như ý b) - biến thể 1/5 của dạng: trạm bơm tiếp sức vượt đèo.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(1, "b", socau, 2)

def L10_C3_B6_VD036_SA_V_02(socau, dang=2):
    r"""Trường Sơn - bản đồ cố ý dịch vị trí (mức VDC, hỏi như ý b) - biến thể 2/5 của dạng: bản đồ cố ý dịch vị trí.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(2, "b", socau, 2)

def L10_C3_B6_VD036_SA_V_03(socau, dang=2):
    r"""Trường Sơn - tổ khảo sát đi theo phương vị (mức VDC, hỏi như ý b) - biến thể 3/5 của dạng: tổ khảo sát đi theo phương vị.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(3, "b", socau, 2)

def L10_C3_B6_VD036_SA_V_04(socau, dang=2):
    r"""Trường Sơn - kéo ống vòng sau trận đánh phá (mức VDC, hỏi như ý b) - biến thể 4/5 của dạng: kéo ống vòng sau trận đánh phá.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(4, "b", socau, 2)

def L10_C3_B6_VD036_SA_V_05(socau, dang=2):
    r"""Trường Sơn - rừng cháy sau trận B-52 (mức VDC, hỏi như ý b) - biến thể 5/5 của dạng: rừng cháy sau trận B-52.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_mc_sa(5, "b", socau, 2)

def L10_C3_B6_VD036_TL_N_01(socau, dong=1):
    r"""Trường Sơn - trạm bơm tiếp sức vượt đèo: a) (VD), b) (VDC) - biến thể 1/5 của dạng.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_tl(1, socau, dong)

def L10_C3_B6_VD036_TL_N_02(socau, dong=1):
    r"""Trường Sơn - bản đồ cố ý dịch vị trí: a) (VD), b) (VDC) - biến thể 2/5 của dạng.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_tl(2, socau, dong)

def L10_C3_B6_VD036_TL_N_03(socau, dong=1):
    r"""Trường Sơn - tổ khảo sát đi theo phương vị: a) (VD), b) (VDC) - biến thể 3/5 của dạng.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_tl(3, socau, dong)

def L10_C3_B6_VD036_TL_N_04(socau, dong=1):
    r"""Trường Sơn - kéo ống vòng sau trận đánh phá: a) (VD), b) (VDC) - biến thể 4/5 của dạng.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_tl(4, socau, dong)

def L10_C3_B6_VD036_TL_N_05(socau, dong=1):
    r"""Trường Sơn - rừng cháy sau trận B-52: a) (VD), b) (VDC) - biến thể 5/5 của dạng.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (bài toán thực tiễn gắn với đường Trường Sơn; số đo giả sử).
    """
    return _ts_tl(5, socau, dong)


# =====================================================================================================
# PÁC BÓ - HÀNH TRÌNH VỀ NƯỚC CỦA BÁC (cô Lan 13/10/2026) - bản TỨ GIÁC
# Năm địa danh thật ở khu di tích Pác Bó (Hà Quảng, Cao Bằng); mỗi đề lấy BỐN trong năm (chỉ các bộ tạo được tứ giác LỒI):
#   km0  = cột mốc Km 0 đường Hồ Chí Minh   - Plus Code Google Maps X3H2+4F8 (tiền tố 7PJ8)   -> 22,97779; 106,05120
#   hang = hang Cốc Bó                       - showcaves.com                                   -> 22,98728; 106,05027
#   lan  = lán Khuổi Nặm                     - Plus Code Google Maps X2MV+9PF (tiền tố 7PJ8)   -> 22,98344; 106,04430
#   moc  = cột mốc 675 (mốc 108 cũ)          - Plus Code Google Maps X3H3+P8 (tiền tố 7PJ8; ô ~14 m) -> 22,97931; 106,05331
#   suoi = suối Lê-nin                       - điểm đánh dấu "suối Lê Nin" của Google Maps (cô Lan gửi liên kết) -> 22,97267; 106,04680
# Plus Code do cô Lan chụp ảnh gửi 13/10/2026 (đã giải mã bằng bộ giải kiểm với ví dụ chuẩn của đặc tả Open Location Code).
# Khoảng cách (đường chim bay) tính bằng haversine từ các toạ độ trên rồi làm tròn chục mét; đề giữ khung "lỏng": mỗi số đo
# (4 cạnh và đường chéo AC) xê dịch -10, 0, +10 m. Bốn đỉnh A, B, C, D theo thứ tự vòng quanh, quay vòng ngẫu nhiên nên đường chéo
# cho trước (AC) và đường chéo hỏi (BD) là hai đường chéo khác nhau tuỳ đề.
# CÙNG DẠNG với Cổng Trời và Lê Thị Riêng (cô Lan 13/10/2026: đề thực tế chỉ tính chiều dài trên bản đồ, KHÔNG tính góc): thêm biến thể
# _04 vào chính các ID MC_J, SA_L, TL_I (không còn ID riêng, không còn câu hỏi góc / khoảng cách). Mỗi đề lấy bốn địa danh (nhãn quay vòng),
# cho AB, BC, CD, DA và đường chéo AC, hỏi diện tích tứ giác ABCD (héc-ta) bằng Heron hai lần; TL: a) diện tích một tam giác, b) cả tứ giác.
# Thông tin ở phần dẫn (đã kiểm chứng): Bác về nước 28/1/1941 cùng 5 đồng chí qua mốc 108 (Báo Nhân Dân 30/1/2025; Google Maps ghi
# "Mốc 675 = mốc 108 cũ"); sau 30 năm bôn ba; ở Pác Bó trong hang Cốc Bó, bên suối Lê-nin, khu vực núi Các Mác, thiếu thốn, gian
# khổ (Luật Minh Khuê; Mia.vn); bài thơ "Tức cảnh Pác Bó" viết tháng 2/1941, thể thất ngôn tứ tuyệt (Luật Minh Khuê; Báo Pháp Luật);
# Hội nghị Trung ương 8 họp tại lán Khuổi Nặm 10-19/5/1941, Bác chủ trì, đặt nhiệm vụ giải phóng dân tộc lên hàng đầu, thành lập
# Mặt trận Việt Minh (Vietnam News); Km 0 thứ hai của đường Hồ Chí Minh đặt ở Pác Bó (HTV). KHÔNG chép lời thơ (13/10/2026: cô Lan bỏ hẳn
# phần thơ và đoạn hang Cốc Bó - Hội nghị 8 cho đề ngắn lại). Bản tam giác cũ (Km 0 - hang - lán) còn ở nhap/pac_bo_block_moi.py.
# =====================================================================================================

_PB_TOA_DO = {
    "km0": (22.9777875, 106.051203125),
    "hang": (22.9872767, 106.0502709),
    "lan": (22.9834375, 106.044296875),
    "moc": (22.9793125, 106.0533125),
    "suoi": (22.9726677, 106.0467982),
}
# tên đầy đủ (trong đề) và tên hai dòng (trên hình)
_PB_TEN = {
    "km0": (r"the Km $0$ marker of the Ho Chi Minh Road", r"Km $0$"),
    "hang": (r"Coc Bo Cave", r"Coc Bo\\Cave"),
    "lan": (r"Khuoi Nam hut", r"Khuoi Nam\\hut"),
    "moc": (r"border marker $675$ (formerly marker $108$)", r"marker $675$"),
    "suoi": (r"a point near Lenin Stream", r"Lenin\\Stream"),
}
# các bộ bốn địa danh tạo tứ giác lồi, ghi theo thứ tự vòng quanh (đã kiểm bằng toạ độ)
_PB_TU_GIAC = [("km0", "moc", "hang", "lan"), ("suoi", "km0", "hang", "lan"), ("suoi", "moc", "hang", "lan")]


def _pb_hv(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = (math.radians(x) for x in (p[0], p[1], q[0], q[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _pb_goc(a, b, c):
    """Số đo góc (độ) đối diện cạnh a trong tam giác có ba cạnh a, b, c."""
    return math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))


def _pb_heron(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def _pb_dan():
    return (r"On $28/1/1941$ (day/month/year), after $30$ years of wandering abroad in search of a way to save the nation, Nguyen Ai Quoc and $5$ comrades crossed border marker no. $108$ "
            r"(now marker $675$) and returned to the Fatherland, setting foot in Pac Bo (Ha Quang, Cao Bang), a small hamlet on the frontier. His return to the country "
            r"opened a new period for the Vietnamese revolution. Today, Pac Bo is also the site of the Km $0$ marker of the Ho Chi Minh Road. "
            r"A small piece of land that made a historic turning point for the whole nation, so that each of us may feel more pride in Uncle Ho, in our country's rivers and mountains "
            r"and cherish more the peaceful life today. ")


def _pb_toa_do(k):
    """Toạ độ địa danh k. Lán, hang, mốc 675, Km 0 giữ NGUYÊN toạ độ thật; riêng điểm trên suối Lê-nin dịch ngẫu nhiên không quá 30 m
    (cô Lan 13/10/2026) nên đề chỉ nói "một điểm gần suối Lê-nin"."""
    p = _PB_TOA_DO[k]
    if k != "suoi":
        return p
    while True:
        dx, dy = random.uniform(-30, 30), random.uniform(-30, 30)
        if math.hypot(dx, dy) <= 30:
            return (p[0] + dy / 111195.0, p[1] + dx / (111195.0 * math.cos(math.radians(p[0]))))


def _pb_bo():
    """Chọn bộ bốn địa danh (nhãn quay vòng A, B, C, D) và đường chéo cho trước (AC hoặc BD, ngẫu nhiên). Các độ dài = khoảng cách
    thật làm tròn đến chục mét (KHÔNG cộng nhiễu). Trả về dict hợp lệ (tứ giác lồi)."""
    while True:
        bo = random.choice(_PB_TU_GIAC)
        r = random.randrange(4)
        ten = [bo[(r + i) % 4] for i in range(4)]
        P = [_pb_toa_do(k) for k in ten]
        hv = {nm: _pb_hv(P[i], P[j]) for nm, i, j in
              (("AB", 0, 1), ("BC", 1, 2), ("CD", 2, 3), ("DA", 3, 0), ("AC", 0, 2), ("BD", 1, 3))}
        so = {nm: int(round(v / 10.0)) * 10 for nm, v in hv.items()}
        ab, bc, cd, da = so["AB"], so["BC"], so["CD"], so["DA"]
        cheo = random.choice(("AC", "BD"))
        if cheo == "AC":                       # E1 = A, E2 = C; X = B (tam giác ABC), Y = D (tam giác ACD)
            dd, l1, l2, kia = so["AC"], (ab, bc), (da, cd), "BD"
            t1, t2 = ("ABC", ab, bc, dd), ("ACD", dd, cd, da)
        else:                                  # E1 = B, E2 = D; X = A (tam giác ABD), Y = C (tam giác BCD)
            dd, l1, l2, kia = so["BD"], (ab, da), (bc, cd), "AC"
            t1, t2 = ("ABD", ab, da, dd), ("BCD", bc, cd, dd)
        ok = True
        for (p, q) in (l1, l2):
            pass
        for (p, q) in (l1, l2):
            if not (p + q > dd and p + dd > q and q + dd > p):
                ok = False
        if not ok:
            continue
        g1x, g1y = _pb_goc(l1[1], l1[0], dd), _pb_goc(l2[1], l2[0], dd)      # góc tại E1 của hai tam giác
        g2x, g2y = _pb_goc(l1[0], l1[1], dd), _pb_goc(l2[0], l2[1], dd)      # góc tại E2
        if g1x + g1y > 175 or g2x + g2y > 175:                               # đòi tứ giác lồi
            continue
        X = (l1[0] * math.cos(math.radians(g1x)), l1[0] * math.sin(math.radians(g1x)))
        Y = (l2[0] * math.cos(math.radians(g1y)), -l2[0] * math.sin(math.radians(g1y)))
        kk = math.hypot(X[0] - Y[0], X[1] - Y[1])                            # đường chéo còn lại dựng từ số liệu đề cho
        if abs(kk - hv[kia]) > 15:                                           # giữ sát khoảng cách thật (tránh khuếch đại sai số làm tròn)
            continue
        return {"ten": ten, "ab": ab, "bc": bc, "cd": cd, "da": da, "cheo": cheo, "dd": dd, "l1": l1, "l2": l2,
                "g1x": g1x, "g1y": g1y, "t1": t1, "t2": t2, "s1": _pb_heron(*t1[1:]), "s2": _pb_heron(*t2[1:])}


def _pb_hinh(c):
    dd, l1, l2 = c["dd"], c["l1"], c["l2"]
    k = 3.3 / dd
    E1, E2 = (0.0, 0.0), (dd * k, 0.0)
    X = (l1[0] * math.cos(math.radians(c["g1x"])) * k, l1[0] * math.sin(math.radians(c["g1x"])) * k)
    Y = (l2[0] * math.cos(math.radians(c["g1y"])) * k, -l2[0] * math.sin(math.radians(c["g1y"])) * k)
    # đường chéo AC: A = E1, B = X, C = E2, D = Y; đường chéo BD: B = E1, A = X, D = E2, C = Y
    V = [E1, X, E2, Y] if c["cheo"] == "AC" else [X, E1, Y, E2]
    G = (sum(p[0] for p in V) / 4, sum(p[1] for p in V) / 4)
    s = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s += "\\fill[green!12] " + " -- ".join("(%.2f,%.2f)" % p for p in V) + " -- cycle;\n"
    s += "\\draw[very thick] " + " -- ".join("(%.2f,%.2f)" % p for p in V) + " -- cycle;\n"
    s += "\\draw[dashed] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (E1 + E2)
    for i, p in enumerate(V):
        vx, vy = p[0] - G[0], p[1] - G[1]
        h = ("right" if vx > 0 else "left") if abs(vx) >= abs(vy) else ("above" if vy > 0 else "below")
        s += "\\fill (%.2f,%.2f) circle (0.06) node[%s] {$%s$};\n" % (p[0], p[1], h, "ABCD"[i])

    def nhan(P, Q, d):
        mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
        nx, ny = -(Q[1] - P[1]), Q[0] - P[0]
        L = math.hypot(nx, ny)
        nx, ny = nx / L, ny / L
        if nx * (G[0] - mx) + ny * (G[1] - my) > 0:
            nx, ny = -nx, -ny
        return "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d$ m};\n" % (mx + 0.48 * nx, my + 0.48 * ny, d)
    for (P, Q, d) in ((V[0], V[1], c["ab"]), (V[1], V[2], c["bc"]), (V[2], V[3], c["cd"]), (V[3], V[0], c["da"])):
        s += nhan(P, Q, d)
    s += "\\node[font=\\scriptsize,fill=green!12,inner sep=1pt] at (%.2f,%.2f) {$%d$ m};\n" % (dd * k / 2, 0.0, dd)
    return s + "\\end{tikzpicture}"


def _pb_de(c):
    ds = ", ".join(r"$%s$ (%s)" % ("ABCD"[i], _PB_TEN[k][0]) for i, k in enumerate(c["ten"]))
    return (_pb_dan() + r"According to the positions marked on the digital map, the four locations " + ds + r" are the four vertices of the convex quadrilateral "
            r"$ABCD$ with $AB = %d$ m, $BC = %d$ m, $CD = %d$ m, $DA = %d$ m and diagonal $%s = %d$ m (straight-line distances, rounded "
            r"to the nearest ten meters, see the figure)." % (c["ab"], c["bc"], c["cd"], c["da"], c["cheo"], c["dd"]))


def _pb_cau():
    """Một bộ số đo Pác Bó: bốn địa danh (tứ giác lồi ABCD), AB, BC, CD, DA và một đường chéo (AC hoặc BD); diện tích hai tam giác do đường chéo chia."""
    while True:
        c = _pb_bo()
        S = c["s1"] + c["s2"]
        if _xa_bien(c["s1"]) and _xa_bien(c["s2"]) and _xa_bien(S / 1e4, 1):
            return c


def _pb_giai(c):
    """(lời giải hai tam giác + kết luận, phần chỉ tam giác ACD + kết luận, kết luận)."""
    S = c["s1"] + c["s2"]
    tg1 = _giai_heron_m(c["t1"][0], c["t1"][1], c["t1"][2], c["t1"][3], c["s1"])
    tg2 = _giai_heron_m(c["t2"][0], c["t2"][1], c["t2"][2], c["t2"][3], c["s2"])
    duoi = (r"Hence $S_{ABCD} = S_{%s} + S_{%s} \approx %d\,\text{m}^{2} \approx %s$ ha (since $1\ \text{ha} = 10\,000\ \text{m}^{2}$)."
            % (c["t1"][0], c["t2"][0], _lt(S), _x1(S / 1e4, 1)))
    return tg1 + "\\\\\n" + tg2 + "\\\\\n" + duoi, tg1, tg2, duoi


def _pb_mc_sa(socau, dang):
    cau = ""
    for _ in range(socau):
        c = _pb_cau()
        S = c["s1"] + c["s2"]
        dap = _x1(S / 1e4, 1)
        giai = _pb_giai(c)[0]
        if dang == 1:
            debai = _pb_de(c) + r" The area of quadrilateral $ABCD$ (in hectares, rounded to the nearest tenth) is"
            nh = _ba_nhieu(dap, [_x1(c["s1"] / 1e4, 1), _x1(c["s2"] / 1e4, 1), str(_lt(S)), _x1(S / 2e4, 1)],
                           buoc=lambda t: _x1(S / 1e4 + 0.9 * t, 1))
        else:
            debai = _pb_de(c) + r" Calculate the area of quadrilateral $ABCD$ (in hectares, rounded to the nearest tenth)."
            nh = [_x1(S / 1e4 + 0.1 * d, 1) for d in (1, -1, 2)]
        cau += MC_SA_answer_const(debai, dap, nh, giai, _pb_hinh(c), 0, dang)
    return cau


def _pb_tl(socau, dong):
    cau = ""
    for _ in range(socau):
        c = _pb_cau()
        S = c["s1"] + c["s2"]
        _, tg1, tg2, duoi = _pb_giai(c)
        if random.random() < 0.5:
            ten, Sa, giai_a, giai_b = c["t1"][0], c["s1"], tg1, tg2
        else:
            ten, Sa, giai_a, giai_b = c["t2"][0], c["s2"], tg2, tg1
        ds = [(r"Find the area of triangle $%s$ (in $\text{m}^{2}$, rounded to the nearest whole number)." % ten,
               r"S_{%s} \approx %d\,\text{m}^{2}" % (ten, _lt(Sa)), giai_a),
              (r"Calculate the area of quadrilateral $ABCD$ (in hectares, rounded to the nearest tenth).",
               r"S_{ABCD} \approx %s\,\text{ha}" % _x1(S / 1e4, 1), giai_b + "\\\\\n" + duoi)]
        cau += TL_answer_text(_pb_de(c), ds, _pb_hinh(c), 0, dong)
    return cau


def L10_C3_B6_VD036_MC_J_04(socau, dang=1):
    r"""Diện tích vùng đất tứ giác, Heron hai lần: Pác Bó - bốn trong năm địa danh (biến thể cùng dạng với Cổng Trời, Lê Thị Riêng).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (Plus Code Google Maps cô gửi; khoảng cách haversine, độ dài làm tròn đến chục mét từ toạ độ thật, điểm trên suối dịch ≤30 m; đường chéo cho trước là AC hoặc BD; chỉ tính chiều dài, không tính góc).
    """
    return _pb_mc_sa(socau, 1)


def L10_C3_B6_VD036_SA_J_04(socau, dang=2):
    r"""Diện tích vùng đất tứ giác, Heron hai lần: Pác Bó - bốn trong năm địa danh (biến thể cùng dạng với Cổng Trời, Lê Thị Riêng).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (Plus Code Google Maps cô gửi; khoảng cách haversine, độ dài làm tròn đến chục mét từ toạ độ thật, điểm trên suối dịch ≤30 m; đường chéo cho trước là AC hoặc BD; chỉ tính chiều dài, không tính góc).
    """
    return _pb_mc_sa(socau, 2)


def L10_C3_B6_VD036_TL_I_04(socau, dong=1):
    r"""Tự luận: a) (VD) diện tích một tam giác, b) (VDC) diện tích tứ giác - Pác Bó, bốn trong năm địa danh (biến thể cùng dạng với Cổng Trời).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (Plus Code Google Maps cô gửi; khoảng cách haversine, độ dài làm tròn đến chục mét từ toạ độ thật, điểm trên suối dịch ≤30 m; đường chéo cho trước là AC hoặc BD; chỉ tính chiều dài, không tính góc).
    """
    return _pb_tl(socau, dong)


# =====================================================================================================
# "ĐỒNG CHÍ" (CHÍNH HỮU) - VẦNG TRĂNG CỦA NGƯỜI LÍNH CỤ HỒ (cô Lan 13/10/2026; thay hai bài Cảnh khuya, Rằm tháng Giêng)
# MỘT DẠNG MỚI (các ID MC_W, SA_Y, TL_O của bài 6, các chữ cái đã gỡ khỏi Pác Bó), HAI BIẾN THỂ:
#   _01: tính ĐƯỜNG KÍNH MẶT TRĂNG từ khoảng cách Trái Đất - Mặt Trăng và góc nhìn (tam giác cân, nửa góc, sin)
#   _02: tính CHIỀU CAO CÂY CỔ THỤ từ bóng trăng đổ trên sườn đồi dốc (định lí sin, số đo GIẢ SỬ)
# Số liệu thật (đã kiểm chứng, nguồn: bảng số liệu Mặt Trăng của NASA qua sites.uni.edu và space.fm): khoảng cách trung bình Trái Đất -
# Mặt Trăng 384 400 km, cận điểm 363 300 km, viễn điểm 405 500 km, đường kính Mặt Trăng khoảng 3 474 - 3 476 km. Góc nhìn trong đề được
# TÍNH từ các số liệu đó (2.asin(đường kính/2d), làm tròn 0,01 độ) nên đúng thực tế; đề KHÔNG nêu đường kính thật (đó là đáp số).
# Phần dẫn chỉ nêu điều đã kiểm chứng (hoatieu.vn, luatminhkhue.vn): bài thơ Đồng chí của Chính Hữu viết đầu năm 1948, sau chiến dịch
# Việt Bắc thu đông 1947, ca ngợi tình đồng đội của người lính kháng chiến chống Pháp; ý "chiến tranh khốc liệt mà người lính vẫn yêu đời,
# yêu thiên nhiên" theo yêu cầu cô Lan. KHÔNG chép lời thơ (cô Lan bỏ phần thơ cho đề ngắn lại). Bối cảnh chung
# "trang_dong_chi" (mỗi đề tối đa một câu).
# =====================================================================================================

_TR_DAN = (r"The poem \textit{Dong chi} (Comrades) by the poet Chinh Huu was written in early $1948$, after the Viet Bac autumn-winter campaign of $1947$, praising "
           r"the comradeship of the soldiers in the resistance war against the French colonialists."
           +
           r" The war was extremely fierce: freezing forest nights, hardship, danger lurking everywhere; yet Uncle Ho's soldier still loved life and nature, "
           r"and still saw the moon as beautiful as if it were hanging right at the muzzle of his gun. That moon is very far from us, but with mathematics "
           r"we can still measure it. ")


def _tr_ng(n):
    """Số nguyên viết kiểu SGK, ngăn cách hàng nghìn bằng khoảng cách hẹp: 384400 -> 384\\,400."""
    return "{:,}".format(int(n)).replace(",", r"\,")


def _tr_d_th(d):
    """Góc nhìn (độ, làm tròn 0,01) của Mặt Trăng (đường kính thật 3 476 km) khi cách Trái Đất d km."""
    return round(math.degrees(2 * math.asin(1738.0 / d)), 2)


def _tr_bo1():
    """(d, theta, D): D = 2.d.sin(theta/2) tính từ số đo đã cho; D làm tròn đến hàng chục không sát ranh giới."""
    while True:
        d = random.randrange(363300, 405501, 100)
        th = _tr_d_th(d)
        D = 2 * d * math.sin(math.radians(th) / 2)
        if _xa_bien(D / 10):
            return d, th, D


def _tr_hinh1(d, th):
    """Sơ đồ tam giác cân EAB (hình KHÔNG đúng tỉ lệ: góc thật chỉ khoảng nửa độ)."""
    s = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s += "\\draw[fill=yellow!25] (5.0,0) circle (1.0);\n"
    s += "\\draw[very thick] (0,0) -- (5.0,1.0) -- (5.0,-1.0) -- cycle;\n"
    s += "\\fill (0,0) circle (0.06) node[left] {$E$};\n"
    s += "\\fill (5.0,1.0) circle (0.06) node[above right] {$A$};\n"
    s += "\\fill (5.0,-1.0) circle (0.06) node[below right] {$B$};\n"
    s += "\\node[font=\\scriptsize] at (2.3,0.95) {$%s$ km};\n" % _tr_ng(d)
    s += "\\node[font=\\scriptsize] at (2.3,-0.95) {$%s$ km};\n" % _tr_ng(d)
    s += "\\draw (1.1,0.22) arc (11.3:-11.3:1.12);\n"
    s += "\\node[font=\\scriptsize] at (1.55,0) {$%s^{\\circ}$};\n" % _x1(th, 2)
    s += "\\node[font=\\scriptsize] at (5.0,-1.55) {Moon};\n"
    s += "\\node[font=\\scriptsize,gray] at (2.5,-1.9) {(figure not to scale)};\n"
    return s + "\\end{tikzpicture}"


def _tr_cau1():
    d, th, D = _tr_bo1()
    chuc = _lt(D / 10) * 10
    intro = (_TR_DAN + r"The Moon is about $%s$ km from the Earth (this distance varies over the course of each month, from about $363\,300$ km "
             r"to about $405\,500$ km). Seen from the Earth, the diameter of the Moon subtends an angle of about $%s^{\circ}$ (rounded data). Treat "
             r"the Moon as a circle; let $E$ be the position of the observer and $AB$ a diameter of the Moon, so that $EAB$ is an isosceles "
             r"triangle with apex $E$, $EA = EB = %s$ km and $\widehat{AEB} = %s^{\circ}$ (see the figure)."
             % (_tr_ng(d), _x1(th, 2), _tr_ng(d), _x1(th, 2)))
    giai = (r"Let $H$ be the midpoint of $AB$. Since triangle $EAB$ is isosceles at $E$, $EH$ is at the same time a median, an altitude and an "
            r"angle bisector, so $EH \perp AB$ and $\widehat{AEH} = \dfrac{\widehat{AEB}}{2} = %s^{\circ}$. In right triangle $AEH$: "
            r"$AH = EA \cdot \sin\widehat{AEH}$, so $AB = 2AH = 2 \cdot EA \cdot \sin\dfrac{\widehat{AEB}}{2} = 2 \cdot %s \cdot \sin %s^{\circ} \approx %s$ "
            r"(km). Hence the diameter of the Moon is about $%s$ km."
            % (_xx(th / 2, 3), _tr_ng(d), _xx(th / 2, 3), _xx(D, 1), _tr_ng(chuc)))
    return dict(intro=intro, hinh=_tr_hinh1(d, th), d=d, th=th, D=D, chuc=chuc, giai=giai)


def _tr_bo2():
    """(alpha, beta, s, h, BC): cây thẳng đứng cao h = AB trên sườn dốc nghiêng beta; bóng AC = s trên sườn; ánh trăng hợp ngang alpha."""
    while True:
        al, be, s = random.randint(35, 60), random.randint(8, 20), random.randint(8, 20)
        h = s * math.sin(math.radians(al + be)) / math.cos(math.radians(al))
        bc = s * math.cos(math.radians(be)) / math.cos(math.radians(al))
        if 7 <= h <= 32 and _xa_bien(h, 1) and _xa_bien(bc, 1):
            return al, be, s, h, bc


def _tr_hinh2(al, be, s, h):
    """Tam giác ABC: A gốc cây, B ngọn cây (AB thẳng đứng), C đầu bóng trên sườn dốc (AC = s, nghiêng be so với phương ngang)."""
    k = 4.0 / max(s * math.cos(math.radians(be)), h)
    A = (0.0, 0.0)
    C = (s * math.cos(math.radians(be)) * k, s * math.sin(math.radians(be)) * k)
    B = (0.0, h * k)
    r = min(0.8, 0.4 * C[0])
    s_ = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s_ += "\\draw[gray] (-1.2,0) -- (%.2f,0);\n" % (C[0] + 0.2)
    s_ += "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;\n" % (A + B + C)
    s_ += "\\draw[gray,dashed] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (C[0], C[1], max(C[0] - 1.4, 0.15), C[1])
    for t, p, v in (("A", A, "below left"), ("B", B, "above"), ("C", C, "right")):
        s_ += "\\fill (%.2f,%.2f) circle (0.06) node[%s] {$%s$};\n" % (p + (v, t))
    s_ += "\\draw (%.2f,0) arc (0:%d:%.2f);\n" % (r, be, r)
    s_ += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (
        (r + 0.45) * math.cos(math.radians(be / 2)), (r + 0.45) * math.sin(math.radians(be / 2)), be)
    s_ += "\\draw (%.2f,%.2f) arc (%d:180:%.2f);\n" % (C[0] + r * math.cos(math.radians(180 - al)), C[1] + r * math.sin(math.radians(180 - al)), 180 - al, r)
    s_ += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (
        C[0] + (r + 0.4) * math.cos(math.radians(180 - al / 2)), C[1] + (r + 0.4) * math.sin(math.radians(180 - al / 2)), al)
    s_ += "\\node[font=\\scriptsize,rotate=%d,above] at (%.2f,%.2f) {$%d$ m};\n" % (be, 0.42 * C[0], 0.42 * C[1], s)   # nhãn độ dài ở PHÍA TRÊN cạnh AC để không đè lên nhãn góc ở A
    # nhãn "ánh trăng" song song với tia BC, lệch ra phía ngoài tam giác (không đè lên tia)
    dx, dy = C[0] - B[0], C[1] - B[1]
    L = math.hypot(dx, dy)
    s_ += "\\node[font=\\scriptsize,gray,rotate=%d] at (%.2f,%.2f) {moonlight};\n" % (
        -al, (B[0] + C[0]) / 2 - 0.3 * dy / L, (B[1] + C[1]) / 2 + 0.3 * dx / L)
    return s_ + "\\end{tikzpicture}"


def _tr_cau2():
    al, be, s, h, bc = _tr_bo2()
    intro = (_TR_DAN + r"On a bright moonlit night on a forested hillside, an old tree grows vertically. The hillside is inclined at $%d^{\circ}$ to the horizontal plane, "
             r"the moonlight strikes the ground at an angle of $%d^{\circ}$ to the horizontal plane, and the tree's shadow falls on the slope with length $%d$ m (measured along "
             r"the hillside). Let $A$ be the base of the tree, $B$ the top of the tree and $C$ the tip of the shadow of the treetop (the measurements are hypothetical, "
             r"see the figure)." % (be, al, s))
    giai_h = (r"In triangle $ABC$: $AB$ is vertical and $AC$ lies on the slope inclined at $%d^{\circ}$ to the horizontal, so $\widehat{BAC} = 90^{\circ} - %d^{\circ} = %d^{\circ}$. The ray of "
              r"light $BC$ makes an angle of $%d^{\circ}$ with the horizontal while the slope $CA$ makes an angle of $%d^{\circ}$ with the horizontal (on opposite "
              r"sides of the horizontal), so $\widehat{ACB} = %d^{\circ} + %d^{\circ} = %d^{\circ}$, hence $\widehat{ABC} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$. "
              r"By the law of sines: $\dfrac{AB}{\sin\widehat{ACB}} = \dfrac{AC}{\sin\widehat{ABC}}$, so "
              r"$AB = \dfrac{AC \cdot \sin\widehat{ACB}}{\sin\widehat{ABC}} = \dfrac{%d \cdot \sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$ (m)."
              % (be, be, 90 - be, al, be, al, be, al + be, 90 - be, al + be, 90 - al, s, al + be, 90 - al, _x1(h, 1)))
    giai_bc = (r"By the law of sines in triangle $ABC$: $\dfrac{BC}{\sin\widehat{BAC}} = \dfrac{AC}{\sin\widehat{ABC}}$ with $\widehat{BAC} = %d^{\circ}$, "
               r"$\widehat{ABC} = %d^{\circ}$, so $BC = \dfrac{%d \cdot \sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$ (m)."
               % (90 - be, 90 - al, s, 90 - be, 90 - al, _x1(bc, 1)))
    return dict(intro=intro, hinh=_tr_hinh2(al, be, s, h), al=al, be=be, s=s, h=h, bc=bc, giai_h=giai_h, giai_bc=giai_bc)


def _tr_mc_sa(bt, socau, dang):
    cau = ""
    so = 0
    while so < socau:
        if bt == 1:
            c = _tr_cau1()
            dap = str(c["chuc"])
            if dang == 2 and len(dap) > 4:
                continue
            hoi = r"the diameter of the Moon (in km, rounded to the nearest ten)"
            sai = [str(_lt(c["D"] / 2 / 10) * 10), str(_lt(c["D"] * 2 / 10) * 10), str(_lt(c["D"] / 10) * 10 + 40)]
            buoc = lambda t: str(c["chuc"] + 30 * t)
            giai = c["giai"]
        else:
            c = _tr_cau2()
            dap = _x1(c["h"], 1) if dang == 1 else _so(c["h"], 1)
            if dang == 2 and len(dap) > 4:
                continue
            hoi = r"the height of the old tree, that is, the length $AB$ (in meters, rounded to the nearest tenth)"
            mau = _x1 if dang == 1 else _so
            sai = [mau(c["s"] * math.tan(math.radians(c["al"])), 1), mau(c["s"] * math.sin(math.radians(c["al"] + c["be"])), 1),
                   mau(c["bc"], 1)]
            buoc = lambda t: mau(c["h"] + 1.3 * t, 1)
            giai = c["giai_h"]
        so += 1
        if dang == 1:
            debai = c["intro"] + r" " + hoi[0].upper() + hoi[1:] + r" is"
            nh = _ba_nhieu(dap, [x for x in sai if x != "0"], buoc=buoc)
        else:
            debai = c["intro"] + r" Calculate " + hoi + r"."
            nh = [buoc(d) for d in (1, -1, 2)]
        cau += MC_SA_answer_const(debai, dap, nh, giai, c["hinh"], 0, dang)
    return cau


def _tr_tl(bt, socau, dong):
    cau = ""
    for _ in range(socau):
        if bt == 1:
            c = _tr_cau1()
            # ý b): khi Mặt Trăng ở khoảng cách khác thì nhìn dưới góc bao nhiêu (dùng đường kính làm tròn ở ý a)
            while True:
                d2 = random.randrange(363300, 405501, 100)
                if abs(d2 - c["d"]) < 15000:
                    continue
                th2 = 2 * math.degrees(math.asin(c["chuc"] / (2.0 * d2)))
                th2_ex = 2 * math.degrees(math.asin(c["D"] / (2.0 * d2)))
                if _xa_bien(th2, 2) and _lt(th2 * 100) == _lt(th2_ex * 100):
                    break
            ds = [(r"Calculate the diameter of the Moon (in km, rounded to the nearest ten).",
                   r"AB \approx %s\,\text{km}" % _tr_ng(c["chuc"]), c["giai"]),
                  (r"When the Moon is $%s$ km from the Earth, at what angle, in degrees, is the diameter of the Moon (use the result of the previous part) seen "
                   r"(rounded to the nearest hundredth)?" % _tr_ng(d2),
                   r"\widehat{AEB} \approx %s^{\circ}" % _x1(th2, 2),
                   r"Triangle $EAB$ is isosceles at $E$ with $EA = EB = %s$ km, $AB \approx %s$ km, so $\sin\dfrac{\widehat{AEB}}{2} = \dfrac{AB}{2 \cdot EA} = \dfrac{%s}{2 \cdot %s} \approx %s$, "
                   r"hence $\dfrac{\widehat{AEB}}{2} \approx %s^{\circ}$ and $\widehat{AEB} \approx %s^{\circ}$."
                   % (_tr_ng(d2), _tr_ng(c["chuc"]), _tr_ng(c["chuc"]), _tr_ng(d2), _xx(c["chuc"] / (2.0 * d2), 6), _xx(th2 / 2, 3), _x1(th2, 2)))]
        else:
            c = _tr_cau2()
            ds = [(r"Calculate the height of the old tree, that is, the length $AB$ (in meters, rounded to the nearest tenth).",
                   r"AB \approx %s\,\text{m}" % _x1(c["h"], 1), c["giai_h"]),
                  (r"Calculate the distance from the top of the tree to the tip of the shadow, that is, the length $BC$ (in meters, rounded to the nearest tenth).",
                   r"BC \approx %s\,\text{m}" % _x1(c["bc"], 1), c["giai_bc"])]
        cau += TL_answer_text(c["intro"], ds, c["hinh"], 0, dong)
    return cau


def L10_C3_B6_VD036_MC_W_01(socau, dang=1):
    r"""Vầng trăng của người lính (Đồng chí) - tính đường kính Mặt Trăng từ khoảng cách và góc nhìn (tam giác cân).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số liệu Mặt Trăng thật, góc nhìn tính từ đường kính thật).
    """
    return _tr_mc_sa(1, socau, 1)


def L10_C3_B6_VD036_MC_W_02(socau, dang=1):
    r"""Vầng trăng của người lính (Đồng chí) - tính chiều cao cây cổ thụ từ bóng trăng trên sườn đồi (định lí sin).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo giả sử).
    """
    return _tr_mc_sa(2, socau, 1)


def L10_C3_B6_VD036_SA_W_01(socau, dang=2):
    r"""Vầng trăng của người lính (Đồng chí) - tính đường kính Mặt Trăng từ khoảng cách và góc nhìn (tam giác cân).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số liệu Mặt Trăng thật, góc nhìn tính từ đường kính thật).
    """
    return _tr_mc_sa(1, socau, 2)


def L10_C3_B6_VD036_SA_W_02(socau, dang=2):
    r"""Vầng trăng của người lính (Đồng chí) - tính chiều cao cây cổ thụ từ bóng trăng trên sườn đồi (định lí sin).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo giả sử).
    """
    return _tr_mc_sa(2, socau, 2)


def L10_C3_B6_VD036_TL_O_01(socau, dong=1):
    r"""Vầng trăng của người lính (Đồng chí) - tự luận: a) đường kính Mặt Trăng, b) góc nhìn khi Mặt Trăng ở khoảng cách khác.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số liệu Mặt Trăng thật, góc nhìn tính từ đường kính thật).
    """
    return _tr_tl(1, socau, dong)


def L10_C3_B6_VD036_TL_O_02(socau, dong=1):
    r"""Vầng trăng của người lính (Đồng chí) - tự luận: a) chiều cao cây cổ thụ AB, b) khoảng cách từ ngọn cây đến đầu bóng BC (định lí sin).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo giả sử).
    """
    return _tr_tl(2, socau, dong)


# =====================================================================================================
# ĐÚNG/SAI "GIẢI TAM GIÁC" PHỦ CẢ BÀI 5 VÀ BÀI 6 (cô Lan 10/10/2026)
# Mỗi câu: a) NB, b) TH dùng giá trị lượng giác (Bài 5); c) VD, d) VDC dùng hệ thức lượng (Bài 6).
# Tam giác sinh ra là tam giác HERON (cạnh nguyên, diện tích nguyên, không vuông) nên sin, cos, S, R, r, h đều
# hữu tỉ; riêng TF_U (góc cho bằng số đo độ) dùng số gần đúng. Quy ước: a = BC, b = CA, c = AB.
#   TF_T (MỘT ID duy nhất, 15 biến thể _01.._15; mọi biến thể cùng dạng "giải tam giác", chỉ khác cách cho và cách hỏi):
#     _01.._03 biết 2 cạnh + 1 góc, góc cho bằng cos A / sin A (nhọn-tù) / tan A      (`_gt_sas`)
#     _04.._06 biết 2 góc (số đo độ) + 1 cạnh: AAS BC, ASA (cạnh kẹp), AAS AB        (`_gu_goc`)
#     _07.._09 biết 3 cạnh: cos-sin + Heron + R-r; cos-tan + h_a + m_a; cos-sin + h_c + R-m_c   (`_gt_sss`)
#     _10, _11 biết 1 cạnh, cos B, 1 đường cao: (BC, AH), (AB, CK)                     (`_gt_cao`)
#     _12, _13 biết 2 cạnh + trung tuyến AM: (BC, AB), (BC, AC)                        (`_gt_med`)
#     _14, _15 biết 3 cạnh + phân giác AD: tính qua góc B, qua góc C                   (`_gt_pg`)
# Một đại lượng = (mẫu phát biểu, giá trị, lời giải, [(giá trị sai, lỗi hay gặp)]) do `_gt_q` trả về; `_gt_gop_q`
# ghép một danh sách đại lượng thành một ý (mỗi ý >= 3 phát biểu đúng và >= 3 phát biểu sai).
# =====================================================================================================

_GT_TEN_CANH = {"a": "BC", "b": "CA", "c": "AB"}
_GT_NHO = {}  # bộ nhớ đệm các danh sách tam giác


def _gt_ke(X):
    """Hai cạnh kề đỉnh X, ví dụ "A" -> ("b", "c")."""
    return tuple(k for k in "abc" if k != X.lower())


def _gt_khac(X):
    """Hai đỉnh còn lại, ví dụ "A" -> ("B", "C")."""
    return tuple(k for k in "ABC" if k != X)


def _gt_heron(a, b, c):
    """(a, b, c) là tam giác Heron (diện tích nguyên) không vuông."""
    if a + b <= c or a + c <= b or b + c <= a:
        return False
    if a * a + b * b == c * c or a * a + c * c == b * b or b * b + c * c == a * a:
        return False
    s = a + b + c
    x = s * (s - 2 * a) * (s - 2 * b) * (s - 2 * c)
    r = math.isqrt(x)
    return r * r == x and r % 4 == 0


def _gt_heron_ds():
    """Các bộ ba cạnh nguyên a <= b <= c <= 52 của tam giác Heron."""
    if "heron" not in _GT_NHO:
        _GT_NHO["heron"] = [(a, b, c) for a in range(3, 53) for b in range(a, 53) for c in range(b, 53) if _gt_heron(a, b, c)]
    return _GT_NHO["heron"]


def _gt_binh_phuong(q):
    """q (hữu tỉ không âm) là bình phương của một số hữu tỉ."""
    q = Rational(q)
    return math.isqrt(q.p) ** 2 == q.p and math.isqrt(q.q) ** 2 == q.q


def _gt_med_ds():
    """Tam giác Heron (b < c, cạnh <= 60) có trung tuyến m_a hữu tỉ."""
    if "med" not in _GT_NHO:
        _GT_NHO["med"] = [(a, b, c) for a in range(3, 61) for b in range(2, 61) for c in range(b + 1, 61)
                          if _gt_heron(a, b, c) and _gt_binh_phuong(Rational(2 * b * b + 2 * c * c - a * a, 4))]
    return _GT_NHO["med"]


def _gt_dung(a, b, c):
    """Mọi đại lượng của tam giác ABC (BC = a, CA = b, AB = c) dưới dạng chính xác."""
    s = a + b + c
    S = Rational(math.isqrt(s * (s - 2 * a) * (s - 2 * b) * (s - 2 * c)), 4)
    p = Rational(s, 2)
    return dict(
        a=a, b=b, c=c, S=S, p=p, R=Rational(a * b * c) / (4 * S), r=S / p,
        cos={"A": Rational(b * b + c * c - a * a, 2 * b * c), "B": Rational(a * a + c * c - b * b, 2 * a * c),
             "C": Rational(a * a + b * b - c * c, 2 * a * b)},
        sin={"A": 2 * S / (b * c), "B": 2 * S / (a * c), "C": 2 * S / (a * b)},
        h={"a": 2 * S / a, "b": 2 * S / b, "c": 2 * S / c},
        m2={"a": Rational(2 * b * b + 2 * c * c - a * a, 4), "b": Rational(2 * a * a + 2 * c * c - b * b, 4),
            "c": Rational(2 * a * a + 2 * b * b - c * c, 4)},
        BD=Rational(a * c, b + c), DC=Rational(a * b, b + c),
        l2=Rational(b * c * ((b + c) ** 2 - a * a), (b + c) ** 2))


def _gt_dang_dep(a, b, c):
    """Loại tam giác quá dẹt (góc nhỏ dưới khoảng 16 độ hoặc góc tù quá lớn)."""
    cs = [Rational(b * b + c * c - a * a, 2 * b * c), Rational(a * a + c * c - b * b, 2 * a * c), Rational(a * a + b * b - c * c, 2 * a * b)]
    return max(cs) < Rational(24, 25) and min(cs) > Rational(-4, 5)


def _gt_chon(dk=None, tran=40):
    """Chọn ngẫu nhiên một tam giác Heron (nhân 1 hoặc 2, cạnh lớn nhất <= tran), gán nhãn ngẫu nhiên.
    dk: hàm nhận dict của `_gt_dung` và trả về True nếu dùng được."""
    ds = _gt_heron_ds()
    for _ in range(4000):
        x = list(random.choice(ds))
        k = random.choice([1, 1, 2])
        x = [v * k for v in x]
        if max(x) > tran:
            continue
        random.shuffle(x)
        if not _gt_dang_dep(*x):
            continue
        t = _gt_dung(*x)
        if dk is None or dk(t):
            return t
    raise RuntimeError("could not choose a Heron triangle satisfying the condition")


def _gt_ngoac(x):
    """Số âm đặt trong ngoặc."""
    return (r"\left(%s\right)" % _L(x)) if x < 0 else _L(x)


def _gt_p(x):
    """Ngoặc khi luỹ thừa: số âm hoặc phân số."""
    x = sympify(x)
    return (r"\left(%s\right)" % _L(x)) if (x < 0 or not x.is_Integer) else _L(x)


def _gt_sai(lst, duong=True, gh1=False):
    """Giữ các giá trị sai hợp lệ: thực, (dương nếu duong), (|x| < 1 nếu gh1); bỏ None."""
    kq = []
    for w, ghi in lst:
        if w is None:
            continue
        try:
            w = simplify(w)
            if not w.is_real:
                continue
            f = float(w)
        except (TypeError, ValueError):
            continue
        if (duong and f <= 0) or (gh1 and abs(f) >= 1):
            continue
        kq.append((w, ghi))
    return kq


def _gt_cos_m(t):
    """cos của góc AMB (M là trung điểm BC) từ dữ liệu của dạng TF_X: t["m"] = AM, t["_med"] = "c" (cho AB) hoặc "b" (cho AC)."""
    m, a = t["m"], t["a"]
    cb = simplify(Rational(4 * m * m + a * a - 4 * t[t["_med"]] ** 2, 4) / (m * a))  # côsin của góc AMB (nếu cho AB) hoặc AMC (nếu cho AC)
    return cb if t["_med"] == "c" else -cb


def _gt_q(t, ten):
    """Một đại lượng của tam giác t: (mẫu có 1 %s, giá trị, lời giải, [(giá trị sai, lỗi)]).
    Tên: cosX sinX tanX (X = A, B, C), a b c, S, Sheron, p, R, r, ha hb hc, ma mb mc, BD DC, la laC (phân giác kẻ từ A, tính qua B hoặc C),
    c_cao a_cao (cạnh AB / BC tính từ đường cao h_a / h_c và góc B), Sha Shc, cosAMB cosAMC sinAMB, b_med c_med (cạnh còn lại khi biết AM)."""
    a, b, c, S, p = t["a"], t["b"], t["c"], t["S"], t["p"]
    cs, sn = t["cos"], t["sin"]
    kieu, X = ten[:3], ten[3:4]
    if len(ten) == 4 and kieu in ("cos", "sin", "tan"):
        o = X.lower()
        s1, s2 = _gt_ke(X)
        cd = (t[s1], t[s2], t[o])
        if kieu == "cos":
            v = cs[X]
            ly = (r"Corollary of the law of cosines: "
                  r"$\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2\cdot %s\cdot %s} = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$." % (X, s1, s2, o, s1, s2, cd[0], cd[1], cd[2], cd[0], cd[1], _L(v)))
            sai = [(-v, "Sign error"), (sn[X], r"Mixing up $\cos %s$ with $\sin %s$" % (X, X)),
                   (Rational(cd[0] ** 2 + cd[1] ** 2 + cd[2] ** 2, 2 * cd[0] * cd[1]), r"Wrong sign of $%s^{2}$" % o),
                   (Rational(cd[0] ** 2 + cd[1] ** 2 - cd[2] ** 2, cd[0] * cd[1]), "Forgetting the factor 2 in the denominator")]
            return r"$\cos %s = %%s$" % X, v, ly, _gt_sai(sai, duong=False, gh1=True)
        if kieu == "sin":
            v = sn[X]
            ly = (r"Since $0^{\circ} < %s < 180^{\circ}$, we have $\sin %s > 0$ and $\sin %s = \sqrt{1 - \cos^{2}%s} = \sqrt{1 - %s^{2}} = %s$."
                  % (X, X, X, X, _gt_p(cs[X]), _L(v)))
            sai = [(-v, r"Forgetting that $\sin %s > 0$" % X), (abs(cs[X]), r"Mixing up $\sin %s$ with $\cos %s$" % (X, X)),
                   (1 - cs[X] ** 2, "Forgot to take the square root"), (1 - abs(cs[X]), "Mistakenly using $\\sin^{2}+\\cos^{2}=1$")]
            return r"$\sin %s = %%s$" % X, v, ly, _gt_sai(sai, duong=True, gh1=True)
        v = sn[X] / cs[X]
        ly = r"$\tan %s = \dfrac{\sin %s}{\cos %s} = \dfrac{%s}{%s} = %s$." % (X, X, X, _L(sn[X]), _gt_ngoac(cs[X]), _L(v))
        sai = [(1 / v, "Numerator and denominator swapped"), (-v, "Sign error"), (sn[X] * cs[X], r"Mistakenly using $\tan = \sin\cdot\cos$")]
        return r"$\tan %s = %%s$" % X, v, ly, _gt_sai(sai, duong=False)
    if ten in ("a", "b", "c"):
        X = ten.upper()
        s1, s2 = _gt_ke(X)
        n1, n2 = _GT_TEN_CANH[s1], _GT_TEN_CANH[s2]
        v = t[ten]
        tong = t[s1] ** 2 + t[s2] ** 2 - 2 * t[s1] * t[s2] * cs[X]
        ly = (r"Law of cosines: $%s^{2} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot\cos %s = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %d$, "
              r"so $%s = %d$." % (_GT_TEN_CANH[ten], n1, n2, n1, n2, X, t[s1], t[s2], t[s1], t[s2], _gt_ngoac(cs[X]), tong, _GT_TEN_CANH[ten], v))
        sai = [(sqrt(t[s1] ** 2 + t[s2] ** 2 + 2 * t[s1] * t[s2] * cs[X]), "Wrong sign of the cosine term"),
               (sqrt(t[s1] ** 2 + t[s2] ** 2), "Forgetting the cosine term"),
               (sqrt(t[s1] ** 2 + t[s2] ** 2 - t[s1] * t[s2] * cs[X]), "Forgot the factor 2"), (tong, "Forgetting to take the square root")]
        return r"$%s = %%s$" % _GT_TEN_CANH[ten], v, ly, _gt_sai(sai)
    if ten == "S":
        v = S
        ly = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$." % (c, b, _L(sn["A"]), _L(v)))
        sai = [(2 * v, r"Forgetting the factor $\dfrac{1}{2}$"), (Rational(1, 2) * b * c * abs(cs["A"]), r"Mixing up $\sin A$ with $\cos A$"),
               (Rational(1, 2) * b * c * sn["A"] ** 2, r"Mistakenly using $\sin^{2}A$"), (v / 2, r"Multiplying by an extra $\dfrac{1}{2}$")]
        return r"The area of triangle $ABC$ equals $%s$", v, ly, _gt_sai(sai)
    if ten == "Sheron":
        v = S
        ly = (r"Semiperimeter $p = \dfrac{%d + %d + %d}{2} = %s$. Heron's formula: "
              r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} = \sqrt{%s\cdot %s\cdot %s\cdot %s} = %s$." % (a, b, c, _L(p), _L(p), _L(p - a), _L(p - b), _L(p - c), _L(v)))
        sai = [(2 * v, r"Forgetting the factor $\dfrac{1}{2}$"), (sqrt(Integer(a + b + c) * (a + b + c - 2 * a) * (a + b + c - 2 * b) * (a + b + c - 2 * c)), "Used the perimeter instead of the semiperimeter"),
               (sqrt((p - a) * (p - b) * (p - c)), "Forgetting the factor $p$"), (v / 2, "Dividing by an extra 2")]
        return r"The area of triangle $ABC$ equals $%s$", v, ly, _gt_sai(sai)
    if ten == "p":
        v = p
        ly = r"Semiperimeter $p = \dfrac{a + b + c}{2} = \dfrac{%d + %d + %d}{2} = %s$." % (a, b, c, _L(v))
        sai = [(a + b + c, "That is the perimeter"), (v / 2, "Dividing by an extra 2"), (Rational(a + b, 2), "Missing one side")]
        return r"The semiperimeter of triangle $ABC$ equals $%s$", v, ly, _gt_sai(sai)
    if ten == "R":
        v = t["R"]
        ly = r"Law of sines: $R = \dfrac{BC}{2\sin A} = \dfrac{%d}{2\cdot %s} = %s$." % (a, _L(sn["A"]), _L(v))
        sai = [(2 * v, "Forgot to divide by 2"), (v / 2, "Dividing by an extra 2"), (a / (2 * abs(cs["A"])), r"Mixing up $\sin A$ with $\cos A$"), (a / sn["A"] / 4, "Dividing by an extra factor")]
        return r"The circumradius of triangle $ABC$ equals $%s$", v, ly, _gt_sai(sai)
    if ten == "r":
        v = t["r"]
        ly = (r"Semiperimeter $p = %s$, area $S = %s$, so $r = \dfrac{S}{p} = %s$." % (_L(p), _L(S), _L(v)))
        sai = [(2 * v, "Multiplied by an extra factor of 2"), (v / 2, "Used the perimeter instead of the semiperimeter"), (S * p, "Multiplying instead of dividing"), (S / a, "Dividing by one side")]
        return r"The inradius of triangle $ABC$ equals $%s$", v, ly, _gt_sai(sai)
    if ten in ("ha", "hb", "hc"):
        k = ten[1]
        v = t["h"][k]
        ly = r"$S = \dfrac{1}{2}\cdot %d\cdot h_%s$, so $h_%s = \dfrac{2S}{%d} = %s$." % (t[k], k, k, t[k], _L(v))
        sai = [(S / t[k], "Forgot to multiply by 2"), (2 * v, "Multiplied by an extra factor of 2"), (2 * S, "Forgetting to divide by the side"), (v / 2, "Dividing by an extra 2")]
        return r"The altitude $h_%s$ from vertex $%s$ equals $%%s$" % (k, k.upper()), v, ly, _gt_sai(sai)
    if ten in ("ma", "mb", "mc"):
        k = ten[1]
        X = k.upper()
        s1, s2 = _gt_ke(X)
        v = sqrt(t["m2"][k])
        ly = (r"Let $M$ be the midpoint of the side opposite vertex $%s$. Apply the law of cosines in the two triangles sharing $%sM$, noting that the two angles at $M$ "
              r"are supplementary (opposite cosines), then add the two equations: $m_%s^{2} = \dfrac{2%s^{2} + 2%s^{2} - %s^{2}}{4} = \dfrac{2\cdot %d^{2} + 2\cdot %d^{2} - %d^{2}}{4} = %s$, "
              r"so $m_%s = %s$." % (X, X, k, s1, s2, k, t[s1], t[s2], t[k], _L(t["m2"][k]), k, _L(v)))
        m4 = 2 * t[s1] ** 2 + 2 * t[s2] ** 2 - t[k] ** 2
        sai = [(sqrt(Rational(m4, 2)), "Dividing by 2 instead of 4"), (sqrt(Integer(m4)), "Forgot to divide by 4"),
               (sqrt(Rational(2 * t[s1] ** 2 + 2 * t[s2] ** 2 + t[k] ** 2, 4)), "Wrong sign of $%s^{2}$" % k),
               (sqrt(Rational(t[s1] ** 2 + t[s2] ** 2 - t[k] ** 2, 4)), "Missing the factor 2")]
        return r"The length of the median $m_%s$ from $%s$ equals $%%s$" % (k, X), v, ly, _gt_sai(sai)
    if ten == "BD":
        v = t["BD"]
        ly = (r"Since $AD$ is the angle bisector, $\dfrac{BD}{DC} = \dfrac{AB}{AC} = \dfrac{%d}{%d}$ and $BD + DC = %d$, so $BD = \dfrac{%d\cdot %d}{%d + %d} = %s$."
              % (c, b, a, a, c, b, c, _L(v)))
        sai = [(t["DC"], "Mixing up $BD$ with $DC$"), (Rational(a, 2), "Confusing with the midpoint"), (Rational(a * b, b + c) * b / c, "Wrong ratio"),
               (Rational(a * c, abs(b - c)) if b != c else None, "Using the difference of the two sides")]
        return r"$BD = %s$", v, ly, _gt_sai(sai)
    if ten == "DC":
        v = t["DC"]
        ly = (r"Since $AD$ is the angle bisector, $\dfrac{BD}{DC} = \dfrac{AB}{AC}$ and $BD + DC = %d$, so $DC = \dfrac{%d\cdot %d}{%d + %d} = %s$."
              % (a, a, b, b, c, _L(v)))
        sai = [(t["BD"], "Mixing up $DC$ with $BD$"), (Rational(a, 2), "Confusing with the midpoint"), (Rational(a * c, b + c) * c / b, "Wrong ratio")]
        return r"$DC = %s$", v, ly, _gt_sai(sai)
    if ten in ("la", "laC"):  # AD tính qua tam giác ABD (la) hoặc ACD (laC)
        K, kc, x, Dn, tg, En = ("B", "c", t["BD"], "BD", "ABD", "AB") if ten == "la" else ("C", "b", t["DC"], "DC", "ACD", "AC")
        ben, v = t[kc], sqrt(t["l2"])
        ly = (r"Since $AD$ is the angle bisector, $%s = \dfrac{%d\cdot %d}{%d + %d} = %s$. Law of cosines in triangle "
              r"$%s$: $AD^{2} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot\cos %s = %d^{2} + %s^{2} - 2\cdot %d\cdot %s\cdot %s = %s$, so $AD = %s$."
              % (Dn, a, ben, b, c, _L(x), tg, En, Dn, En, Dn, K, ben, _gt_p(x), ben, _L(x), _gt_ngoac(cs[K]), _L(t["l2"]), _L(v)))
        sai = [(sqrt(ben * ben + x ** 2 + 2 * ben * x * cs[K]), "Wrong sign of the cosine term"),
               (sqrt(ben * ben + x ** 2), "Forgetting the cosine term"), (2 * v, "Multiplied by an extra factor of 2"), (sqrt(Integer(b * c)), "Mistakenly using $\\sqrt{AB\\cdot AC}$")]
        return r"The length of the angle bisector $AD$ ($D$ on $BC$) equals $%s$", v, ly, _gt_sai(sai)
    if ten in ("c_cao", "a_cao"):  # AB từ h_a (c_cao), BC từ h_c (a_cao), cùng với góc B
        k, ten_c, h_t, dinh = ("a", "AB", "h_a", "AH") if ten == "c_cao" else ("c", "BC", "h_c", "CK")
        v, hh = (c if ten == "c_cao" else a), t["h"][k]
        ly = (r"In the right triangle formed by the altitude %s: $%s = \dfrac{%s}{\sin B} = \dfrac{%s}{%s} = %d$." % (dinh, ten_c, h_t, _L(hh), _L(sn["B"]), v))
        sai = [(hh * sn["B"], r"Mistakenly using $%s\cdot\sin B$" % h_t), (hh / cs["B"] if cs["B"] != 0 else None, r"Mixing up $\sin B$ with $\cos B$"),
               (hh * cs["B"], r"Mistakenly using $%s\cdot\cos B$" % h_t), (hh, r"Confusing the side with the altitude")]
        return r"$%s = %%s$" % ten_c, Integer(v), ly, _gt_sai(sai)
    if ten in ("Sha", "Shc"):
        k = ten[2]
        ly = r"$S = \dfrac{1}{2}\cdot %s\cdot h_%s = \dfrac{1}{2}\cdot %d\cdot %s = %s$." % (_GT_TEN_CANH[k], k, t[k], _L(t["h"][k]), _L(S))
        sai = [(2 * S, r"Forgetting the factor $\dfrac{1}{2}$"), (S / 2, "Multiplying by an extra factor of $\\dfrac{1}{2}$"), (t[k] + t["h"][k], "Adding instead of multiplying")]
        return r"The area of triangle $ABC$ equals $%s$", S, ly, _gt_sai(sai)
    if ten in ("cosAMB", "cosAMC", "sinAMB"):  # trung tuyến AM, hai góc AMB và AMC bù nhau
        dau, m = t["_med"], t["m"]
        tg, gk, dinh = ("ABM", "AMB", "B") if dau == "c" else ("ACM", "AMC", "C")
        cb = _gt_cos_m(t) if dau == "c" else -_gt_cos_m(t)  # côsin của góc tại M trong tam giác đã cho cạnh
        ly0 = (r"In triangle $%s$ (where $M$ is the midpoint of $BC$, $BM = CM = \dfrac{%d}{2}$, $AM = %s$): "
               r"$\cos\widehat{%s} = \dfrac{AM^{2} + BM^{2} - A%s^{2}}{2\cdot AM\cdot BM} = %s$." % (tg, a, _L(m), gk, dinh, _L(cb)))
        if ten == "sinAMB":
            v = simplify(sqrt(1 - _gt_cos_m(t) ** 2))
            ly = r"$\sin\widehat{AMB} = \sqrt{1 - \cos^{2}\widehat{AMB}} = \sqrt{1 - %s^{2}} = %s$ (since $0^{\circ} < \widehat{AMB} < 180^{\circ}$)." % (_gt_ngoac(_gt_cos_m(t)), _L(v))
            sai = [(-v, r"Forgetting that $\sin > 0$"), (abs(_gt_cos_m(t)), r"Mixing up $\sin$ with $\cos$"), (1 - _gt_cos_m(t) ** 2, "Forgot to take the square root")]
            return r"$\sin\widehat{AMB} = %s$", v, ly, _gt_sai(sai, duong=True, gh1=True)
        G, kia = ("B", "C") if ten == "cosAMB" else ("C", "B")
        v = _gt_cos_m(t) if ten == "cosAMB" else -_gt_cos_m(t)
        if dau != ("c" if G == "B" else "b"):
            ly = ly0 + r" Since angles $AMB$ and $AMC$ are supplementary, $\cos\widehat{AM%s} = -\cos\widehat{AM%s} = %s$." % (G, kia, _L(v))
        else:
            ly = ly0
        sai = [(-v, "Forgetting that supplementary angles have opposite cosines"), (simplify(v / 2), "Mistakenly using $BM = a$ in the denominator"), (simplify(v * 2), "Wrong coefficient in the denominator")]
        return r"$\cos\widehat{AM%s} = %%s$" % G, v, ly, _gt_sai(sai, duong=False, gh1=True)
    if ten in ("b_med", "c_med"):  # cạnh còn lại (AC hoặc AB) tính từ định lí côsin trong tam giác chứa M
        m = t["m"]
        G, ang, ten_c, v, co = ("C", "AMC", "AC", b, -_gt_cos_m(t)) if ten == "b_med" else ("B", "AMB", "AB", c, _gt_cos_m(t))
        val = m * m + Rational(a * a, 4) - m * a * co
        ly = (r"In triangle $A%sM$: $%s^{2} = AM^{2} + %sM^{2} - 2\cdot AM\cdot %sM\cdot\cos\widehat{%s} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot %s = %s$, so $%s = %s$."
              % (G, ten_c, G, G, ang, _gt_p(m), _gt_p(Rational(a, 2)), _L(m), _L(Rational(a, 2)), _gt_ngoac(co), _L(val), ten_c, _L(v)))
        sai = [(sqrt(m * m + Rational(a * a, 4) + m * a * co), "Wrong sign of the cosine term"), (sqrt(m * m + Rational(a * a, 4)), "Forgetting the cosine term"),
               (sqrt(m * m + Rational(a * a, 4) - 2 * m * a * co), "Multiplied by an extra factor of 2"), (m * m + Rational(a * a, 4) - m * a * co, "Forgetting to take the square root")]
        return r"$%s = %%s$" % ten_c, Integer(v), ly, _gt_sai(sai)
    raise KeyError(ten)


def _gt_gop_q(t, ds_ten):
    """Một ý gồm các đại lượng trong ds_ten."""
    return _tf_gop(*[_tf_ct(mau, sympify(v), ly, sai) for mau, v, ly, sai in (_gt_q(t, ten) for ten in ds_ten)])


def _gt_ya(t, X):
    """Ý a (NB, Bài 5): hai góc bù nhau trong tam giác, hệ thức cơ bản, dấu theo loại góc."""
    s, c = t["sin"][X], t["cos"][X]
    nhon = c > 0
    y, z = _gt_khac(X)
    ly = (r"In triangle $ABC$: $%s + %s = 180^{\circ} - %s$, so $\sin\left(%s + %s\right) = \sin\left(180^{\circ} - %s\right) = \sin %s = %s$ "
          r"and $\cos\left(%s + %s\right) = -\cos %s = %s$. Also $\sin^{2}%s + \cos^{2}%s = 1$; angle $%s$ is %s, so $\cos %s %s 0$, $\tan %s %s 0$."
          % (y, z, X, y, z, X, X, _L(s), y, z, X, _L(-c), X, X, X, "acute" if nhon else "obtuse", X, ">" if nhon else "<", X, ">" if nhon else "<"))
    dung = [(r"$\sin\left(%s + %s\right) = %s$" % (y, z, _L(s)), ly), (r"$\sin\left(180^{\circ} - %s\right) = %s$" % (X, _L(s)), ly),
            (r"$\cos\left(%s + %s\right) = %s$" % (y, z, _L(-c)), ly), (r"$\sin^{2}%s + \cos^{2}%s = 1$" % (X, X), ly),
            (r"$\cos %s %s 0$" % (X, ">" if nhon else "<"), ly), (r"$\tan %s %s 0$" % (X, ">" if nhon else "<"), ly)]
    sai = [(r"$\sin\left(%s + %s\right) = %s$" % (y, z, _L(-s)), ly), (r"$\sin\left(180^{\circ} - %s\right) = %s$" % (X, _L(c)), ly),
           (r"$\cos\left(%s + %s\right) = %s$" % (y, z, _L(c)), ly), (r"$\sin^{2}%s + \cos^{2}%s = %s$" % (X, X, _L(s)), ly),
           (r"$\cos %s %s 0$" % (X, "<" if nhon else ">"), ly), (r"$\tan %s %s 0$" % (X, "<" if nhon else ">"), ly)]
    return _phat_bieu(dung, sai)


def _gt_rut_goc(t, X, co):
    """Ý b (TH, Bài 5): hai giá trị lượng giác còn lại của góc X khi đã cho một giá trị (co = "cos" | "sin" | "tan")."""
    s, c = t["sin"][X], t["cos"][X]
    nhon = c > 0
    dau = ">" if nhon else "<"
    cap = []
    for ten in {"cos": ("sin", "tan"), "sin": ("cos", "tan"), "tan": ("cos", "sin")}[co]:
        if ten == "sin":
            ly = (r"From $\cos %s = %s$: $\sin^{2}%s = 1 - \cos^{2}%s = %s$, and since $\sin %s > 0$, $\sin %s = %s$." % (X, _L(c), X, X, _L(1 - c * c), X, X, _L(s))
                  if co != "tan" else r"$\sin %s = \tan %s\cdot\cos %s = %s$." % (X, X, X, _L(s)))
            sai = [(-s, r"Forgetting that $\sin %s > 0$" % X), (c, r"Mixing up $\sin %s$ with $\cos %s$" % (X, X)), (1 - c * c, "Forgot to take the square root")]
            cap.append(_tf_ct(r"$\sin %s = %%s$" % X, s, ly, _gt_sai(sai, duong=True, gh1=True)))
        elif ten == "cos":
            if co == "sin":
                ly = (r"$\cos^{2}%s = 1 - \sin^{2}%s = %s$; angle $%s$ is %s, so $\cos %s %s 0$, hence $\cos %s = %s$."
                      % (X, X, _L(1 - s * s), X, "acute" if nhon else "obtuse", X, dau, X, _L(c)))
            else:
                ly = (r"$\dfrac{1}{\cos^{2}%s} = 1 + \tan^{2}%s = %s$, so $\cos^{2}%s = %s$; since $\tan %s %s 0$, angle $%s$ is %s, "
                      r"$\cos %s %s 0$ and $\cos %s = %s$."
                      % (X, X, _L(1 + (s / c) ** 2), X, _L(c * c), X, dau, X, "acute" if nhon else "obtuse", X, dau, X, _L(c)))
            sai = [(-c, "Sign error"), (c * c, "Forgot to take the square root"), ((1 if nhon else -1) * (1 - s), "Forgot to square")]
            cap.append(_tf_ct(r"$\cos %s = %%s$" % X, c, ly, _gt_sai(sai, duong=False, gh1=True)))
        else:
            v = s / c
            ly = r"$\tan %s = \dfrac{\sin %s}{\cos %s} = %s$." % (X, X, X, _L(v))
            sai = [(1 / v, "Numerator and denominator swapped"), (-v, "Sign error"), (s * c, r"Mistakenly using $\tan = \sin\cdot\cos$")]
            cap.append(_tf_ct(r"$\tan %s = %%s$" % X, v, ly, _gt_sai(sai, duong=False)))
    return _tf_gop(*cap)


def _gt_cau(socau, socot, tao):
    """Ghép `socau` câu đúng/sai; `tao()` trả về (đề bài, [ý a, ý b, ý c, ý d])."""
    cauTF = ""
    for _ in range(socau):
        debai, ys = tao()
        cauTF += TF_baitoan_du(debai, ys, 0, 0, socot)
    return cauTF


# ---------- TF_T: biết hai cạnh kề và một giá trị lượng giác của góc A ----------

def _gt_sas(co, hoi_c, hoi_d):
    t = _gt_chon(dk=lambda t: t["b"] != t["c"], tran=30)
    s, c = t["sin"]["A"], t["cos"]["A"]
    cho = {"cos": r"$\cos A = %s$" % _L(c), "sin": r"$\sin A = %s$ and angle $A$ is %s" % (_L(s), "acute" if c > 0 else "obtuse"),
           "tan": r"$\tan A = %s$" % _L(s / c)}[co]
    debai = r"In triangle $ABC$, $AB = %d$, $AC = %d$ and %s. Determine whether each of the following statements is true or false:" % (t["c"], t["b"], cho)
    return debai, [_gt_ya(t, "A"), _gt_rut_goc(t, "A", co), _gt_gop_q(t, hoi_c), _gt_gop_q(t, hoi_d)]


def L10_C3_TF_T_01(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $AB$, $AC$ và $\cos A$ (phân số, có thể âm).
    a) hai góc bù nhau, hệ thức cơ bản; b) $\sin A$, $\tan A$; c) $BC$, diện tích; d) $R$, $h_a$."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_sas("cos", ["a", "S"], ["R", "ha"]))


def L10_C3_TF_T_02(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù. b) cos A, tan A; c) BC, p; d) cos B, sin B."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_sas("sin", ["a", "p"], ["cosB", "sinB"]))


def L10_C3_TF_T_03(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $AB$, $AC$ và $\tan A$ (dấu cho biết nhọn / tù). b) cos A, sin A; c) BC, S; d) r, m_a."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_sas("tan", ["a", "S"], ["r", "ma"]))


# ---------- TF_V: biết ba cạnh ----------

def _gt_sss(hoi_b, hoi_c, hoi_d):
    t = _gt_chon(tran=40)
    debai = r"In triangle $ABC$, $BC = %d$, $CA = %d$, $AB = %d$. Determine whether each of the following statements is true or false:" % (t["a"], t["b"], t["c"])
    X = random.choice(["A", "B", "C"])
    return debai, [_gt_ya(t, X), _gt_gop_q(t, hoi_b), _gt_gop_q(t, hoi_c), _gt_gop_q(t, hoi_d)]


def L10_C3_TF_T_07(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết ba cạnh. b) cos A, sin A; c) nửa chu vi, diện tích (Heron); d) R, r."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_sss(["cosA", "sinA"], ["p", "Sheron"], ["R", "r"]))


def L10_C3_TF_T_08(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết ba cạnh. b) cos B, tan B; c) diện tích (Heron), $h_a$; d) trung tuyến $m_a$, r."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_sss(["cosB", "tanB"], ["Sheron", "ha"], ["ma", "r"]))


def L10_C3_TF_T_09(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết ba cạnh. b) cos C, sin C; c) diện tích (Heron), $h_c$; d) R, trung tuyến $m_c$."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_sss(["cosC", "sinC"], ["Sheron", "hc"], ["R", "mc"]))


# ---------- TF_W: biết một cạnh, cos B và một đường cao ----------

def _gt_cao(loai):
    ok = lambda t, k: (2 * t["S"]) % t[k] == 0 and 0 not in t["cos"].values()  # đường cao nguyên
    if loai == "a":
        t = _gt_chon(dk=lambda t: ok(t, "a"), tran=30)
        debai = (r"In triangle $ABC$, $BC = %d$, $\cos B = %s$ and the altitude $AH = %s$ ($H$ lies on line $BC$). Determine whether "
                 r"each of the following statements is true or false:" % (t["a"], _L(t["cos"]["B"]), _L(t["h"]["a"])))
        y3, y4 = _gt_gop_q(t, ["c_cao", "Sha"]), _gt_gop_q(t, ["b", "cosC"])
    else:
        t = _gt_chon(dk=lambda t: ok(t, "c"), tran=30)
        debai = (r"In triangle $ABC$, $AB = %d$, $\cos B = %s$ and the altitude $CK = %s$ ($K$ lies on line $AB$). Determine whether "
                 r"each of the following statements is true or false:" % (t["c"], _L(t["cos"]["B"]), _L(t["h"]["c"])))
        y3, y4 = _gt_gop_q(t, ["a_cao", "Shc"]), _gt_gop_q(t, ["b", "R"])
    return debai, [_gt_ya(t, "B"), _gt_rut_goc(t, "B", "cos"), y3, y4]


def L10_C3_TF_T_10(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $BC$, $\cos B$ và đường cao $AH$. b) sin B, tan B; c) AB, S; d) AC (định lí côsin), cos C."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_cao("a"))


def L10_C3_TF_T_11(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $AB$, $\cos B$ và đường cao $CK$. b) sin B, tan B; c) BC, S; d) AC (định lí côsin), R."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_cao("c"))


# ---------- TF_X: biết hai cạnh và đường trung tuyến AM ----------

def _gt_chon_med(dau):
    """Tam giác có trung tuyến m_a hữu tỉ (b khác c); dau = "c" (đề cho AB) hoặc "b" (đề cho AC)."""
    for _ in range(500):
        a, b, c = random.choice(_gt_med_ds())
        if random.random() < 0.5:
            b, c = c, b
        if _gt_dang_dep(a, b, c):
            break
    t = _gt_dung(a, b, c)
    t["m"], t["_med"] = sqrt(t["m2"]["a"]), dau
    return t


def _gt_ya_med(t):
    """Ý a (NB, Bài 5): hai góc AMB và AMC bù nhau."""
    nh = _gt_cos_m(t) > 0
    ly = (r"Since $M$ lies between $B$ and $C$, $\widehat{AMB} + \widehat{AMC} = 180^{\circ}$, so $\sin\widehat{AMB} = \sin\widehat{AMC}$ "
          r"and $\cos\widehat{AMB} = -\cos\widehat{AMC}$; $BM = CM = \dfrac{%d}{2}$." % t["a"])
    dung = [(r"$\widehat{AMB} + \widehat{AMC} = 180^{\circ}$", ly), (r"$\sin\widehat{AMB} = \sin\widehat{AMC}$", ly),
            (r"$\cos\widehat{AMB} + \cos\widehat{AMC} = 0$", ly), (r"$\cos\widehat{AMC} = -\cos\widehat{AMB}$", ly),
            (r"$BM = CM = %s$" % _L(Rational(t["a"], 2)), ly),
            (r"Angle $\widehat{AMB}$ is %s" % ("acute" if nh else "obtuse"), ly + r" Since $\cos\widehat{AMB} %s 0$, the statement is true." % (">" if nh else "<"))]
    sai = [(r"$\cos\widehat{AMB} = \cos\widehat{AMC}$", ly), (r"$\sin\widehat{AMB} + \sin\widehat{AMC} = 0$", ly),
           (r"$\widehat{AMB} = \widehat{AMC}$", ly + r" (The two angles are equal only when $AB = AC$.)"), (r"$\widehat{AMB} + \widehat{AMC} = 90^{\circ}$", ly),
           (r"$BM = %s$" % _L(t["a"]), ly),
           (r"Angle $\widehat{AMB}$ is %s" % ("obtuse" if nh else "acute"), ly + r" Since $\cos\widehat{AMB} %s 0$, the statement is false." % (">" if nh else "<"))]
    return _phat_bieu(dung, sai)


def _gt_med(dau):
    t = _gt_chon_med(dau)
    debai = (r"In triangle $ABC$, $BC = %d$, $%s = %d$ and the median $AM = %s$ ($M$ is the midpoint of $BC$). Determine whether each "
             r"of the following statements is true or false:" % (t["a"], "AB" if dau == "c" else "AC", t[dau], _L(t["m"])))
    return debai, [_gt_ya_med(t), _gt_gop_q(t, ["cosAMB", "cosAMC", "sinAMB"]), _gt_gop_q(t, ["c_med" if dau == "b" else "b_med"]),
                   _gt_gop_q(t, ["cosA", "S"] if dau == "c" else ["R", "S"])]


def L10_C3_TF_T_12(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $BC$, $AB$ và trung tuyến $AM$. a) $AMB$, $AMC$ bù nhau; b) cos, sin góc tại M;
    c) AC (định lí côsin trong tam giác $AMC$); d) cos A, S."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_med("c"))


def L10_C3_TF_T_13(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $BC$, $AC$ và trung tuyến $AM$. c) AB (định lí côsin trong tam giác $AMB$); d) R, S."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_med("b"))


# ---------- TF_Y: biết ba cạnh và đường phân giác trong AD ----------

def _gt_ya_pg():
    """Ý a (NB, Bài 5): hai góc ADB, ADC bù nhau; AD chia đôi góc A."""
    ly = (r"Since $D$ lies between $B$ and $C$, $\widehat{ADB} + \widehat{ADC} = 180^{\circ}$, so $\sin\widehat{ADB} = \sin\widehat{ADC}$ and "
          r"$\cos\widehat{ADB} = -\cos\widehat{ADC}$; since $AD$ is the angle bisector, $\widehat{BAD} = \widehat{DAC} = \dfrac{\widehat{A}}{2}$.")
    dung = [(r"$\widehat{ADB} + \widehat{ADC} = 180^{\circ}$", ly), (r"$\sin\widehat{ADB} = \sin\widehat{ADC}$", ly),
            (r"$\cos\widehat{ADB} + \cos\widehat{ADC} = 0$", ly), (r"$\widehat{BAD} = \widehat{DAC}$", ly),
            (r"$\sin\widehat{BAD} = \sin\widehat{DAC}$", ly), (r"$\widehat{BAD} = \dfrac{\widehat{BAC}}{2}$", ly)]
    sai = [(r"$\cos\widehat{ADB} = \cos\widehat{ADC}$", ly), (r"$\sin\widehat{ADB} + \sin\widehat{ADC} = 0$", ly),
           (r"$\widehat{ADB} = \widehat{ADC}$", ly + r" (The two angles are equal only when $AB = AC$.)"), (r"$\widehat{ADB} + \widehat{ADC} = 90^{\circ}$", ly),
           (r"$\widehat{BAD} = \widehat{BAC}$", ly), (r"$\cos\widehat{BAD} = -\cos\widehat{DAC}$", ly)]
    return _phat_bieu(dung, sai)


def _gt_pg(dinh):
    t = _gt_chon(dk=lambda t: t["b"] != t["c"] and _gt_binh_phuong(t["l2"]), tran=60)
    debai = (r"In triangle $ABC$, $BC = %d$, $CA = %d$, $AB = %d$. Let $AD$ be the interior angle bisector of angle $A$ ($D$ lies on side $BC$). Determine whether "
             r"each of the following statements is true or false:" % (t["a"], t["b"], t["c"]))
    return debai, [_gt_ya_pg(), _gt_gop_q(t, ["cos" + dinh, "sin" + dinh]), _gt_gop_q(t, ["BD", "DC"]), _gt_gop_q(t, ["la" if dinh == "B" else "laC"])]


def L10_C3_TF_T_14(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết ba cạnh và phân giác $AD$. b) cos B, sin B; c) BD, DC; d) AD (định lí côsin trong tam giác $ABD$)."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_pg("B"))


def L10_C3_TF_T_15(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết ba cạnh và phân giác $AD$. b) cos C, sin C; c) BD, DC; d) AD (định lí côsin trong tam giác $ACD$)."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gt_pg("C"))


# ---------- TF_U: biết hai góc (số đo độ) và một cạnh; các giá trị là số gần đúng ----------

def _gu_dung(ang, cg, do_dai):
    """ang: số đo ba góc (độ); cg: cạnh cho trước ("a" | "b" | "c") có độ dài do_dai. Mọi đại lượng tính bằng số thực."""
    sin = {x: math.sin(math.radians(v)) for x, v in ang.items()}
    G = cg.upper()
    k = do_dai / sin[G]  # k = 2R
    canh = {x.lower(): k * sin[x] for x in "ABC"}
    S = 0.5 * canh["b"] * canh["c"] * sin["A"]
    return dict(ang=ang, sin=sin, cos={x: math.cos(math.radians(v)) for x, v in ang.items()}, G=G, cg=cg, k=k, canh=canh, S=S, R=k / 2,
                h={x: 2 * S / canh[x] for x in "abc"})


def _gu_g(g):
    """Độ dài cho trước: số nguyên thì không lấy chữ số thập phân."""
    return _x1(g, 0) if abs(g - round(g)) < 1e-9 else _x1(g, 1)


def _gu_ya(u, ten3, hai):
    """Ý a (NB, Bài 5): góc thứ ba và các giá trị lượng giác theo cung bù."""
    P, Q = hai
    gp, gq, g3 = u["ang"][P], u["ang"][Q], u["ang"][ten3]
    nh = g3 < 90
    ly = (r"The sum of the three angles of a triangle is $180^{\circ}$, so $\widehat{%s} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$; "
          r"since $\widehat{%s} = 180^{\circ} - \left(\widehat{%s} + \widehat{%s}\right)$, we have $\sin\widehat{%s} = \sin\left(\widehat{%s} + \widehat{%s}\right)$ "
          r"and $\cos\widehat{%s} = -\cos\left(\widehat{%s} + \widehat{%s}\right)$; angle $%s$ is %s." % (ten3, gp, gq, g3, ten3, P, Q, ten3, P, Q, ten3, P, Q, ten3, "acute" if nh else "obtuse"))
    dung = [(r"$\widehat{%s} = %d^{\circ}$" % (ten3, g3), ly), (r"$\sin\widehat{%s} = \sin\left(\widehat{%s} + \widehat{%s}\right)$" % (ten3, P, Q), ly),
            (r"$\cos\widehat{%s} = -\cos\left(\widehat{%s} + \widehat{%s}\right)$" % (ten3, P, Q), ly),
            (r"Angle $\widehat{%s}$ is %s" % (ten3, "acute" if nh else "obtuse"), ly),
            (r"$\cos\widehat{%s} %s 0$" % (ten3, ">" if nh else "<"), ly), (r"$\sin\widehat{%s} > 0$" % ten3, ly)]
    sai = [(r"$\widehat{%s} = %d^{\circ}$" % (ten3, g3 + random.choice([5, 10, 15])), ly), (r"$\sin\widehat{%s} = -\sin\left(\widehat{%s} + \widehat{%s}\right)$" % (ten3, P, Q), ly),
           (r"$\cos\widehat{%s} = \cos\left(\widehat{%s} + \widehat{%s}\right)$" % (ten3, P, Q), ly),
           (r"Angle $\widehat{%s}$ is %s" % (ten3, "obtuse" if nh else "acute"), ly), (r"$\cos\widehat{%s} %s 0$" % (ten3, "<" if nh else ">"), ly),
           (r"$\sin\widehat{%s} = \sin\widehat{%s} + \sin\widehat{%s}$" % (ten3, P, Q), ly)]
    return _phat_bieu(dung, sai)


def _gu_gtlg(u, ten3):
    """Ý b (TH, Bài 5): sin và cos của góc thứ ba (làm tròn đến hàng phần trăm)."""
    v_s, v_c, g = u["sin"][ten3], u["cos"][ten3], u["ang"][ten3]
    ds, ss = _tf_so(r"$\sin\widehat{%s} \approx %%s$" % ten3, v_s, 2, r"$\sin\widehat{%s} = \sin %d^{\circ} \approx %s$." % (ten3, g, _x1(v_s, 3)),
                    [(abs(v_c), r"Mixing up $\sin$ with $\cos$"), (1 - v_s, "Mistakenly using $1 - \\sin$"), (math.sin(g), "Leaving the calculator in radian mode")], mien=(0, 1))
    dc, sc = _tf_so(r"$\cos\widehat{%s} \approx %%s$" % ten3, v_c, 2, r"$\cos\widehat{%s} = \cos %d^{\circ} \approx %s$." % (ten3, g, _x1(v_c, 3)),
                    [(-v_c, "Sign error"), (v_s, r"Mixing up $\cos$ with $\sin$"), (math.cos(g), "Leaving the calculator in radian mode")], mien=(-1, 1))
    return _tf_gop((ds, ss), (dc, sc))


def _gu_canh(u, tc):
    """Cạnh tc ("a" | "b" | "c") theo định lí sin (làm tròn đến hàng phần mười)."""
    X, G, cg = tc.upper(), u["G"], u["cg"]
    ang, sin, cos, g, v = u["ang"], u["sin"], u["cos"], u["canh"][u["cg"]], u["canh"][tc]
    n_x, n_g = _GT_TEN_CANH[tc], _GT_TEN_CANH[cg]
    ly = (r"Law of sines: $\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s}$, so $%s = \dfrac{%s\cdot\sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$."
          % (n_x, X, n_g, G, n_x, _gu_g(g), ang[X], ang[G], _x1(v, 2)))
    sai = [(g * sin[X], r"Forgetting to divide by $\sin %s$" % G), (g * sin[G] / sin[X], "Numerator and denominator swapped"),
           (g * cos[X] / cos[G] if abs(cos[G]) > 1e-9 else None, r"Using $\cos$ instead of $\sin$"), (g * ang[X] / ang[G], "Using the ratio of the angle measures")]
    return _tf_so(r"$%s \approx %%s$" % n_x, v, 1, ly, [(w, s) for w, s in sai if w is not None and w > 0])


def _gu_dtich(u, ten):
    """ten: "S" (diện tích) | "R" (bán kính ngoại tiếp) | "h" (đường cao kẻ từ đỉnh đối diện cạnh cho trước)."""
    cg, G = u["cg"], u["G"]
    g = u["canh"][cg]
    if ten == "S":
        X = [x for x in "ABC" if x != G][0]
        Y = [x for x in "ABC" if x not in (G, X)][0]
        cx = X.lower()
        v = 0.5 * g * u["canh"][cx] * u["sin"][Y]
        ly = (r"Area $S = \dfrac{1}{2}\cdot %s\cdot %s\cdot\sin %d^{\circ} \approx \dfrac{1}{2}\cdot %s\cdot %s\cdot %s \approx %s$ (using the sides just calculated)."
              % (_GT_TEN_CANH[cg], _GT_TEN_CANH[cx], u["ang"][Y], _x1(g, 1), _x1(u["canh"][cx], 1), _x1(u["sin"][Y], 3), _x1(v, 1)))
        sai = [(2 * v, r"Forgetting the factor $\dfrac{1}{2}$"), (0.5 * g * u["canh"][cx] * u["cos"][Y] if u["cos"][Y] > 0 else None, r"Using $\cos$ instead of $\sin$"),
               (v / 2, r"Multiplying by an extra $\dfrac{1}{2}$"), (0.5 * g * u["canh"][cx], "Forgetting to multiply by the sine of the included angle")]
        mau = r"The area of triangle $ABC$ is approximately $%s$"
    elif ten == "R":
        v = u["R"]
        ly = r"Law of sines: $R = \dfrac{%s}{2\sin %d^{\circ}} \approx \dfrac{%s}{2\cdot %s} \approx %s$." % (_GT_TEN_CANH[cg], u["ang"][G], _gu_g(g), _x1(u["sin"][G], 3), _x1(v, 1))
        sai = [(2 * v, "Forgot to divide by 2"), (v / 2, "Dividing by an extra 2"), (g / (2 * abs(u["cos"][G])) if abs(u["cos"][G]) > 1e-9 else None, r"Using $\cos$ instead of $\sin$")]
        mau = r"The circumradius of triangle $ABC$ is approximately $%s$"
    else:
        v = u["h"][cg]
        ly = r"$S \approx %s$, so $h = \dfrac{2S}{%s} \approx %s$." % (_x1(u["S"], 1), _x1(g, 1), _x1(v, 1))
        sai = [(u["S"] / g, "Forgot to multiply by 2"), (2 * v, "Multiplied by an extra factor of 2"), (v / 2, "Dividing by an extra 2")]
        mau = r"The altitude from vertex $%s$ is approximately $%%s$" % G
    return _tf_so(mau, v, 1, ly, [(w, s) for w, s in sai if w is not None])


def _gu_goc(hai, cg, hoi_d):
    """hai: tên hai góc cho trước (vd "AB"); cg: cạnh cho trước; hoi_d: các đại lượng ở ý d."""
    g1 = random.choice(range(35, 85, 5))
    g2 = random.choice(range(35, 85, 5))
    while g1 == g2 or (180 - g1 - g2) in (90,) or not 25 <= 180 - g1 - g2 <= 115:  # chọn lại cho đến khi góc thứ ba hợp lí
        g1 = random.choice(range(35, 85, 5))
        g2 = random.choice(range(35, 85, 5))
    ten3 = [x for x in "ABC" if x not in hai][0]
    ang = {hai[0]: g1, hai[1]: g2, ten3: 180 - g1 - g2}
    do_dai = random.randint(10, 40)
    u = _gu_dung(ang, cg, do_dai)
    debai = (r"In triangle $ABC$, $\widehat{%s} = %d^{\circ}$, $\widehat{%s} = %d^{\circ}$ and $%s = %d$. Determine whether each of the following statements "
             r"is true or false (approximate results are rounded as stated in each statement):" % (hai[0], g1, hai[1], g2, _GT_TEN_CANH[cg], do_dai))
    return debai, [_gu_ya(u, ten3, hai), _gu_gtlg(u, ten3), _tf_gop(*[_gu_canh(u, x) for x in "abc" if x != cg]),
                   _tf_gop(*[_gu_dtich(u, x) for x in hoi_d])]


def L10_C3_TF_T_04(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $\widehat A$, $\widehat B$ và $BC$ (đối diện góc $A$). a) góc $C$, giá trị lượng giác theo cung bù;
    b) $\sin C$, $\cos C$; c) $CA$, $AB$ (định lí sin); d) S, R."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gu_goc("AB", "a", ["S", "R"]))


def L10_C3_TF_T_05(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc). b) $\sin A$, $\cos A$; c) $CA$, $AB$; d) S, đường cao từ $A$."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gu_goc("BC", "a", ["S", "h"]))


def L10_C3_TF_T_06(socau, socot=1):
    r"""Đúng/Sai - giải tam giác: biết $\widehat A$, $\widehat C$ và $AB$ (đối diện góc $C$). b) $\sin B$, $\cos B$; c) $BC$, $CA$; d) R, S."""
    # a) NB (Bài 5) # b) TH (Bài 5) # c) VD (Bài 6) # d) VDC (Bài 6)
    return _gt_cau(socau, socot, lambda: _gu_goc("AC", "c", ["R", "S"]))


# =====================================================================
# SIN +- COS <-> SIN.COS: bản TRẢ LỜI NGẮN và TỰ LUẬN (cùng dạng với TH030_MC_D)
# ---------------------------------------------------------------------
# CLAUDE THEM 11/10/2026 - co Lan ("kiem tra xem co bai toan nguoc lai: tu tong
# hoac hieu tim tich chua. da du MC, SA, TL chua" -> "ban xu ly het cho toi"):
# truoc day dang nay chi co MC (TH030_MC_D_01 tong/hieu -> tich, _02 tich -> (sin +- cos)^2, sin^4 + cos^4).
# Muc do giu dung nhu MC_D (TH030, khong ghi chu LUYEN TAP THEM). Dap so SA toi da 4 ky tu
# (nhu cac cau SA khac) nen SA dung so thap phan; TL dung bo ba Pythagore nen dap so la phan so.
# Co Lan duyet lai.
# =====================================================================

def _sa_sc_chuoi(x):
    """Số thập phân hữu hạn (dấu phẩy), tối đa 4 kí tự (kể cả dấu); không gọn được thì None."""
    return _so_thap_phan_gon(x, 4)


def L10_C3_B5_TH030_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn: biết $\sin\alpha + \cos\alpha$ (hoặc $\sin\alpha - \cos\alpha$) bằng một số thập phân,
    tính $\sin\alpha\cos\alpha$ (đáp số thập phân tối đa 4 kí tự)."""
    # a nằm trong [-1; căn 2] để góc tồn tại; chỉ lấy a cho đáp số gọn (<= 4 kí tự).
    CAC = [(Rational(k, 10), True) for k in (12, 14)] + \
          [(Rational(k, 10), False) for k in (-8, -6, -4, -2, 2, 4, 6, 8)]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        v = random.choice(CAC)
        if v not in gt:
            gt.append(v)
    cau = ""
    for a, tong in gt:
        P = (a ** 2 - 1) / 2 if tong else (1 - a ** 2) / 2
        dap = _sa_sc_chuoi(P)
        assert dap is not None and -Rational(1, 2) <= P <= Rational(1, 2)
        bt = r"\sin\alpha + \cos\alpha" if tong else r"\sin\alpha - \cos\alpha"
        dau = "+" if tong else "-"
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ such "
                 r"that $%s = %s$. What is the value of $\sin\alpha\cos\alpha$?" % (bt, _xx(a, 2)))
        giai = (r"Squaring both sides: $\left(%s\right)^{2} = %s^{2}$" % (bt, _ngoac_dec(a)) + "\\\\\n" +
                r"$\Leftrightarrow \sin^{2}\alpha + \cos^{2}\alpha %s 2\sin\alpha\cos\alpha = %s$"
                % (dau, _xx(a ** 2, 4)) + "\\\\\n" +
                r"$\Leftrightarrow 1 %s 2\sin\alpha\cos\alpha = %s$ (since $\sin^{2}\alpha + \cos^{2}\alpha = 1$)"
                % (dau, _xx(a ** 2, 4)) + "\\\\\n" +
                r"$\Leftrightarrow \sin\alpha\cos\alpha = %s = %s$." % (
                    (r"\dfrac{%s - 1}{2}" % _xx(a ** 2, 4)) if tong else (r"\dfrac{1 - %s}{2}" % _xx(a ** 2, 4)), dap))
        ds = [_xx(P + d, 3) for d in (Rational(1, 10), -Rational(1, 10), Rational(1, 5))]
        ds = [x for x in ds if x != dap][:3]
        while len(ds) < 3:
            ds.append(_xx(P + Rational(len(ds) + 3, 10), 3))
        cau += MC_SA_answer_text(debai, dap, ds, giai, 0, 0, dang)
    return cau


def _ngoac_dec(a):
    """Số thập phân đặt trong ngoặc khi nâng luỹ thừa nếu âm."""
    return (r"\left(%s\right)" % _xx(a, 2)) if a < 0 else _xx(a, 2)


def _sa_tich_hoi(socau, dang, loai):
    """Biết tích sinα.cosα = p (số thập phân) -> loai: 'tong' (sin+cos)^2, 'hieu' (sin-cos)^2, 'bon' sin^4+cos^4."""
    if loai == "bon":
        CAC = [Rational(s * k, 10) for k in (1, 2, 3, 4, 5) for s in (1, -1)]
    else:
        CAC = [Rational(s * k, 100) for k in range(1, 50) for s in (1, -1)]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 800:
        lan += 1
        p = random.choice(CAC)
        if p not in gt:
            gt.append(p)
    cau = ""
    for p in gt:
        if loai == "tong":
            hoi, P = r"\left(\sin\alpha + \cos\alpha\right)^{2}", 1 + 2 * p
            ket = r"1 + 2\cdot %s" % _ngoac_dec(p)
            ds_u = [1 - 2 * p, 2 * p, 1 + p]
            thap, cao = Integer(0), Integer(2)
            giai = (r"We have $%s = \sin^{2}\alpha + \cos^{2}\alpha + 2\sin\alpha\cos\alpha = 1 + 2\sin\alpha\cos\alpha$.\\" % hoi
                    + "\n" + r"Substituting $\sin\alpha\cos\alpha = %s$ gives $%s = %s = %s$." % (_xx(p, 2), hoi, ket, _sa_sc_chuoi(P)))
        elif loai == "hieu":
            hoi, P = r"\left(\sin\alpha - \cos\alpha\right)^{2}", 1 - 2 * p
            ket = r"1 - 2\cdot %s" % _ngoac_dec(p)
            ds_u = [1 + 2 * p, 2 * p, 1 - p]
            thap, cao = Integer(0), Integer(2)
            giai = (r"We have $%s = \sin^{2}\alpha + \cos^{2}\alpha - 2\sin\alpha\cos\alpha = 1 - 2\sin\alpha\cos\alpha$.\\" % hoi
                    + "\n" + r"Substituting $\sin\alpha\cos\alpha = %s$ gives $%s = %s = %s$." % (_xx(p, 2), hoi, ket, _sa_sc_chuoi(P)))
        else:
            hoi, P = r"\sin^{4}\alpha + \cos^{4}\alpha", 1 - 2 * p ** 2
            ket = r"1 - 2\cdot \left(%s\right)^{2}" % _xx(p, 2)
            ds_u = [1 + 2 * p ** 2, 1 - p ** 2, 1 - 2 * p]
            thap, cao = Rational(1, 2), Integer(1)
            giai = (r"We have "
                    r"$\sin^{4}\alpha + \cos^{4}\alpha = \left(\sin^{2}\alpha + \cos^{2}\alpha\right)^{2} - 2\sin^{2}\alpha\cos^{2}\alpha = 1 - 2\left(\sin\alpha\cos\alpha\right)^{2}$.\\" + "\n"
                    + r"Substituting $\sin\alpha\cos\alpha = %s$ gives $%s = %s = %s$." % (_xx(p, 2), hoi, ket, _sa_sc_chuoi(P)))
        dap = _sa_sc_chuoi(P)
        assert dap is not None and thap <= P <= cao, (loai, p, P)
        ds = _nhieu_trong_mien(P, ds_u, thap, cao, Rational(1, 100), fmt=lambda x: _xx(x, 4))
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ such "
                 r"that $\sin\alpha\cos\alpha = %s$. What is the value of $%s$?" % (_xx(p, 2), hoi))
        cau += MC_SA_answer_text(debai, dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_SA_D_02(socau, dang=2):
    r"""Trả lời ngắn: biết $\sin\alpha\cos\alpha$, tính $(\sin\alpha + \cos\alpha)^{2}$."""
    return _sa_tich_hoi(socau, dang, "tong")


def L10_C3_B5_TH030_SA_D_03(socau, dang=2):
    r"""Trả lời ngắn: biết $\sin\alpha\cos\alpha$, tính $(\sin\alpha - \cos\alpha)^{2}$."""
    return _sa_tich_hoi(socau, dang, "hieu")


def L10_C3_B5_TH030_SA_D_04(socau, dang=2):
    r"""Trả lời ngắn: biết $\sin\alpha\cos\alpha$, tính $\sin^{4}\alpha + \cos^{4}\alpha$."""
    return _sa_tich_hoi(socau, dang, "bon")


# Bo ba Pythagore cho TL sin +- cos <-> sin.cos: them bon bo nho de nhieu de bai khac nhau (tich P khac nhau)
_BO_TL_SC = BO_BA_PYTAGO + [(9, 40, 41), (12, 35, 37), (11, 60, 61), (16, 63, 65)]


def L10_C3_B5_TH030_TL_F_01(socau, dong=1):
    r"""Tự luận 2 ý: biết $\sin\alpha + \cos\alpha$ (hoặc hiệu) = a. a) Tính $\sin\alpha\cos\alpha$.
    b) Tính $|\sin\alpha - \cos\alpha|$ (hoặc $|\sin\alpha + \cos\alpha|$) hay $\sin^{4}\alpha + \cos^{4}\alpha$,
    dùng kết quả ý a)."""
    BO = _BO_TL_SC + [(y, x, z) for x, y, z in _BO_TL_SC]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        p, q, r = random.choice(BO)
        s = random.choice([1, -1])
        tong = random.random() < 0.5
        # sin^4 + cos^4 chi hoi voi bo (3,4,5): voi r lon dap so co tu so, mau so 4-5 chu so, qua cong kenh
        kieu = random.choice(["tuyet_doi", "bon"]) if r == 5 else "tuyet_doi"
        sn, cs = Rational(p, r), Rational(s * q, r)
        a = sn + cs if tong else sn - cs
        v = (a, tong, kieu)
        if a == 0 or v in gt:
            continue
        gt.append(v)
        gt[-1] = (a, tong, kieu, sn, cs)
    cau = ""
    for a, tong, kieu, sn, cs in gt:
        P = sn * cs
        assert P == (a ** 2 - 1) / 2 if tong else P == (1 - a ** 2) / 2
        bt = r"\sin\alpha + \cos\alpha" if tong else r"\sin\alpha - \cos\alpha"
        kia = r"\sin\alpha - \cos\alpha" if tong else r"\sin\alpha + \cos\alpha"
        dau = "+" if tong else "-"
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ such that $%s = %s$."
                 % (bt, _L(a)))
        giai_a = (r"Squaring both sides: $\left(%s\right)^{2} = %s^{2}$" % (bt, _ngoac_mu(a)) + "\\\\\n" +
                  r"$\Leftrightarrow \sin^{2}\alpha + \cos^{2}\alpha %s 2\sin\alpha\cos\alpha = %s$" % (dau, _L(a ** 2))
                  + "\\\\\n" +
                  r"$\Leftrightarrow 1 %s 2\sin\alpha\cos\alpha = %s$ (since $\sin^{2}\alpha + \cos^{2}\alpha = 1$)" % (dau, _L(a ** 2))
                  + "\\\\\n" +
                  r"$\Leftrightarrow \sin\alpha\cos\alpha = %s$." % _L(P))
        y_a = (r"Calculate $\sin\alpha\cos\alpha$.", _L(P), giai_a)
        if kieu == "tuyet_doi":
            Q = 1 - 2 * P if tong else 1 + 2 * P           # (kia)^2
            kq = abs(sn - cs) if tong else abs(sn + cs)
            assert kq ** 2 == Q
            giai_b = (r"From part a) we already have $\sin\alpha\cos\alpha = %s$." % _L(P) + "\\\\\n" +
                      r"We have $\left(%s\right)^{2} = \sin^{2}\alpha + \cos^{2}\alpha %s 2\sin\alpha\cos\alpha = 1 %s 2\cdot %s = %s$."
                      % (kia, "-" if tong else "+", "-" if tong else "+", _ngoac_mu(P), _L(Q)) + "\\\\\n" +
                      r"Hence $\left|%s\right| = \sqrt{%s} = %s$." % (kia, _L(Q), _L(kq)))
            y_b = (r"Calculate $\left|%s\right|$." % kia, _L(kq), giai_b)
        else:
            Q = 1 - 2 * P ** 2
            giai_b = (r"We have "
                      r"$\sin^{4}\alpha + \cos^{4}\alpha = \left(\sin^{2}\alpha + \cos^{2}\alpha\right)^{2} - 2\sin^{2}\alpha\cos^{2}\alpha = 1 - 2\left(\sin\alpha\cos\alpha\right)^{2}$." + "\\\\\n" +
                      r"From part a) we already have $\sin\alpha\cos\alpha = %s$, so $\sin^{4}\alpha + \cos^{4}\alpha = 1 - 2\cdot %s^{2} = %s$."
                      % (_L(P), _ngoac_mu(P), _L(Q)))
            y_b = (r"Calculate $\sin^{4}\alpha + \cos^{4}\alpha$.", _L(Q), giai_b)
        cau += TL_answer_text(debai, [y_a, y_b], 0, 0, dong)
    return cau


def L10_C3_B5_TH030_TL_G_01(socau, dong=1):
    r"""Tự luận 2 ý: biết $\sin\alpha\cos\alpha = P < 0$ (góc tù). Hoặc a) $(\sin\alpha - \cos\alpha)^{2}$,
    b) $\sin\alpha - \cos\alpha$ (xét dấu); hoặc a) $(\sin\alpha + \cos\alpha)^{2}$, b) $\sin^{4}\alpha + \cos^{4}\alpha$."""
    BO = _BO_TL_SC + [(y, x, z) for x, y, z in _BO_TL_SC]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        p, q, r = random.choice(BO)
        kieu = random.choice(["hieu", "bon"]) if r == 5 else "hieu"
        v = (p, q, r, kieu)
        if v not in gt:
            gt.append(v)
    cau = ""
    for p, q, r, kieu in gt:
        sn, cs = Rational(p, r), -Rational(q, r)     # góc tù: sin > 0 > cos
        P = sn * cs
        debai = (r"Given an angle $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ such "
                 r"that $\sin\alpha\cos\alpha = %s$." % _L(P))
        if kieu == "hieu":
            Q = 1 - 2 * P
            kq = sn - cs
            assert kq ** 2 == Q and kq > 0
            y_a = (r"Calculate $\left(\sin\alpha - \cos\alpha\right)^{2}$.", _L(Q),
                   r"We have "
                   r"$\left(\sin\alpha - \cos\alpha\right)^{2} = \sin^{2}\alpha + \cos^{2}\alpha - 2\sin\alpha\cos\alpha = 1 - 2\sin\alpha\cos\alpha = 1 - 2\cdot %s = %s$." % (_ngoac_mu(P), _L(Q)))
            y_b = (r"Calculate $\sin\alpha - \cos\alpha$.", _L(kq),
                   r"Since $0^{\circ} \le \alpha \le 180^{\circ}$, we have $\sin\alpha \ge 0$; since $\sin\alpha\cos\alpha = %s < 0$, we get $\sin\alpha > 0$ "
                   r"and $\cos\alpha < 0$." % _L(P) + "\\\\\n" +
                   r"Therefore $\sin\alpha - \cos\alpha > 0$. From part a): $\sin\alpha - \cos\alpha = \sqrt{%s} = %s$." % (_L(Q), _L(kq)))
        else:
            Q1 = 1 + 2 * P
            Q = 1 - 2 * P ** 2
            assert (sn + cs) ** 2 == Q1
            y_a = (r"Calculate $\left(\sin\alpha + \cos\alpha\right)^{2}$.", _L(Q1),
                   r"We have "
                   r"$\left(\sin\alpha + \cos\alpha\right)^{2} = \sin^{2}\alpha + \cos^{2}\alpha + 2\sin\alpha\cos\alpha = 1 + 2\sin\alpha\cos\alpha = 1 + 2\cdot %s = %s$." % (_ngoac_mu(P), _L(Q1)))
            y_b = (r"Calculate $\sin^{4}\alpha + \cos^{4}\alpha$.", _L(Q),
                   r"We have "
                   r"$\sin^{4}\alpha + \cos^{4}\alpha = \left(\sin^{2}\alpha + \cos^{2}\alpha\right)^{2} - 2\sin^{2}\alpha\cos^{2}\alpha = 1 - 2\left(\sin\alpha\cos\alpha\right)^{2}$." + "\\\\\n" +
                   r"Substituting $\sin\alpha\cos\alpha = %s$ gives $1 - 2\cdot %s^{2} = %s$." % (_L(P), _ngoac_mu(P), _L(Q)))
        cau += TL_answer_text(debai, [y_a, y_b], 0, 0, dong)
    return cau


# ===== MS_BEGIN (MC/SA/TL giải tam giác, sinh bởi build) =====
# =====================================================================
# MC / SA / TL "GIẢI TAM GIÁC" (CLAUDE THEM 10/10/2026, theo bảng ID cô Lan đã duyệt)
# ---------------------------------------------------------------------
# Dùng lại CÙNG câu dẫn với đúng/sai TF_T (chương 3): mỗi ID là một đơn vị kiến thức, mỗi chữ cái là MỘT CÁCH CHO
# (dạng), mỗi biến thể _01.._03 là một cách cho / cách hỏi khác:
#   cách cho A: 2 cạnh + 1 góc (_01 cos A, _02 sin A nhọn/tù, _03 tan A)    B: 2 góc (độ) + 1 cạnh (_01 AAS BC, _02 ASA, _03 AAS AB)
#   cách cho C: 3 cạnh (_01.._03 hỏi theo đỉnh A, B, C)                       D: 1 cạnh, cos B, 1 đường cao (_01 BC-AH, _02 AB-CK)
#   cách cho E: 2 cạnh + trung tuyến AM (_01 cho AB, _02 cho AC)             F: 3 cạnh + phân giác AD (_01 qua B, _02 qua C)
# E, F ngoài yêu cầu cần đạt (trung tuyến, phân giác) -> LUYEN TAP THEM.
# Một đại lượng = dict(hoi, v, ly, sai, ...) do `_ms_q` trả về (dùng lại `_gt_q` của TF_T cho dạng chính xác, `_msu_q` cho dạng
# góc cho bằng độ). Một câu = chuỗi các đại lượng (bước trung gian ... đại lượng cần hỏi); lời giải ghép các bước.
# Hàm công khai chỉ là lớp mỏng: `_ms_sinh(loai, don_vi, cach_cho, bien_the, socau, dang)`.
# =====================================================================

_MS_MUC_HANG = {0: "whole number", 1: "tenth", 2: "hundredth", 3: "thousandth"}
_MS_NOI = r"\\ "  # ngắt dòng trong lời giải


def _ms_chuan(c, can_sin):
    """Dòng lời giải đổi giá trị lượng giác cho trước của góc A sang cos A (và sin A nếu cần) - cách cho A."""
    t, co = c["t"], c["co"]
    cs, sn = t["cos"]["A"], t["sin"]["A"]
    if co == "cos":
        if not can_sin:
            return ""
        return (r"Since $0^{\circ} < A < 180^{\circ}$, we have $\sin A > 0$ and $\sin A = \sqrt{1 - \cos^{2}A} = \sqrt{1 - %s^{2}} = %s$."
                % (_gt_p(cs), _L(sn)))
    if co == "sin":
        loai = "acute" if cs > 0 else "obtuse"
        return (r"Angle $A$ is %s, so $\cos A %s 0$ and $\cos A = %s\sqrt{1 - \sin^{2}A} = %s\sqrt{1 - %s^{2}} = %s$."
                % (loai, ">" if cs > 0 else "<", "" if cs > 0 else "-", "" if cs > 0 else "-", _gt_p(sn), _L(cs)))
    tg = sn / cs
    return (r"From $1 + \tan^{2}A = \dfrac{1}{\cos^{2}A}$ we get $\cos^{2}A = \dfrac{1}{1 + %s^{2}} = %s$. Since $\sin A > 0$ and $\tan A %s 0$, we have $\cos A %s 0$, "
            r"so $\cos A = %s$ and $\sin A = \tan A\cdot\cos A = %s$." % (_gt_p(tg), _L(cs * cs), ">" if tg > 0 else "<", ">" if cs > 0 else "<", _L(cs), _L(sn)))


def _ms_chuan_d(c):
    """Cách cho D: sin B từ cos B."""
    t = c["t"]
    return (r"Since $0^{\circ} < B < 180^{\circ}$, we have $\sin B > 0$ and $\sin B = \sqrt{1 - \cos^{2}B} = \sqrt{1 - %s^{2}} = %s$."
            % (_gt_p(t["cos"]["B"]), _L(t["sin"]["B"])))


# ---------- câu dẫn (đề) cho từng cách cho: trả về dict c ----------

def _ms_le(t):
    """Tam giác thường (ba cạnh khác nhau), để các đáp số không trùng nhau."""
    return len({t["a"], t["b"], t["c"]}) == 3


# Quy tắc cô Lan 10/10/2026: "không đưa các dữ liệu không sử dụng trong quá trình giải bài vào câu dẫn".
# Các (đơn vị, cách cho) mà lời giải KHÔNG dùng hết dữ kiện của cách cho nguyên bản -> câu dẫn chỉ nêu dữ kiện thực sự dùng:
#   A (TH031, TH030): chỉ cần một giá trị lượng giác của góc A -> không nêu AB, AC;
#   B (TH031, TH030): chỉ cần hai góc -> không nêu độ dài cạnh;
#   D (TH034): S = 1/2.a.h_a chỉ cần cạnh và đường cao -> không nêu cos B.
_MS_DE_GON = {("TH031", "A"), ("TH030", "A"), ("TH031", "B"), ("TH030", "B"), ("TH034", "D")}


def _ms_ctx(cach, bt, dv=""):
    """Sinh dữ liệu một câu: c["de"] là câu dẫn (đã có dấu chấm), c["t"] / c["u"] là tam giác chính xác / gần đúng.
    dv: đơn vị kiến thức (để bỏ dữ kiện không dùng, xem _MS_DE_GON)."""
    gon = (dv, cach) in _MS_DE_GON
    if cach == "A":
        co = ("cos", "sin", "tan")[bt - 1]
        if gon:
            # câu dẫn không nêu cạnh -> không cần tam giác thường; chỉ cần góc A không vuông
            t = _gt_chon(dk=lambda x: x["cos"]["A"] != 0, tran=40)
        else:
            t = _gt_chon(dk=_ms_le, tran=30)
        s, cc = t["sin"]["A"], t["cos"]["A"]
        loai_a = "acute" if cc > 0 else "obtuse"
        cho = {"cos": r"$\cos A = %s$" % _L(cc),
               "sin": (r"$\sin A = %s$ and angle $A$ is %s" if gon else r"$\sin A = %s$, angle $A$ is %s") % (_L(s), loai_a),
               "tan": r"$\tan A = %s$" % _L(s / cc)}[co]
        if gon:
            return dict(t=t, co=co, de=r"In triangle $ABC$, %s." % cho)
        return dict(t=t, co=co, de=r"In triangle $ABC$, $AB = %d$, $AC = %d$ and %s." % (t["c"], t["b"], cho))
    if cach == "B":
        hai, cg = (("AB", "a"), ("BC", "a"), ("AC", "c"))[bt - 1]
        g1 = random.choice(range(35, 80, 5))
        g2 = random.choice(range(35, 80, 5))
        while len({g1, g2, 180 - g1 - g2}) < 3 or not 25 <= 180 - g1 - g2 <= 115 or abs(180 - g1 - g2 - 90) < 10:
            g1 = random.choice(range(35, 80, 5))
            g2 = random.choice(range(35, 80, 5))
        ten3 = [x for x in "ABC" if x not in hai][0]
        ang = {hai[0]: g1, hai[1]: g2, ten3: 180 - g1 - g2}
        do_dai = random.randint(10, 40)
        u = _gu_dung(ang, cg, do_dai)
        if gon:
            de = (r"In triangle $ABC$, $\widehat{%s} = %d^{\circ}$ and $\widehat{%s} = %d^{\circ}$." % (hai[0], g1, hai[1], g2))
        else:
            de = (r"In triangle $ABC$, $\widehat{%s} = %d^{\circ}$, $\widehat{%s} = %d^{\circ}$ and $%s = %d$."
                  % (hai[0], g1, hai[1], g2, _GT_TEN_CANH[cg], do_dai))
        return dict(u=u, hai=hai, ten3=ten3, cg=cg, de=de)
    if cach == "C":
        t = _gt_chon(dk=_ms_le, tran=40)
        return dict(t=t, X="ABC"[bt - 1], de=r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$." % (t["a"], t["b"], t["c"]))
    if cach == "D":
        k = "a" if bt == 1 else "c"
        if gon:
            # câu dẫn chỉ nêu một cạnh và đường cao tương ứng: chỉ cần đường cao nguyên (không cần cos B khác 0, tam giác thường)
            t = _gt_chon(dk=lambda t: (2 * t["S"]) % t[k] == 0, tran=100)
        else:
            ok = lambda t: (2 * t["S"]) % t[k] == 0 and 0 not in t["cos"].values() and _ms_le(t)
            t = _gt_chon(dk=ok, tran=30)
        if gon and k == "a":
            de = (r"In triangle $ABC$, $BC = %d$ and the altitude $AH = %s$ ($H$ lies on line $BC$)." % (t["a"], _L(t["h"]["a"])))
        elif gon:
            de = (r"In triangle $ABC$, $AB = %d$ and the altitude $CK = %s$ ($K$ lies on line $AB$)." % (t["c"], _L(t["h"]["c"])))
        elif k == "a":
            de = (r"In triangle $ABC$, $BC = %d$, $\cos B = %s$ and the altitude $AH = %s$ ($H$ lies on line $BC$)."
                  % (t["a"], _L(t["cos"]["B"]), _L(t["h"]["a"])))
        else:
            de = (r"In triangle $ABC$, $AB = %d$, $\cos B = %s$ and the altitude $CK = %s$ ($K$ lies on line $AB$)."
                  % (t["c"], _L(t["cos"]["B"]), _L(t["h"]["c"])))
        return dict(t=t, k=k, de=de)
    if cach == "E":
        dau = "c" if bt == 1 else "b"
        t = _gt_chon_med(dau)
        de = (r"In triangle $ABC$, $BC = %d$, $%s = %d$ and the median $AM = %s$ ($M$ is the midpoint of $BC$)."
              % (t["a"], "AB" if dau == "c" else "AC", t[dau], _L(t["m"])))
        return dict(t=t, dau=dau, de=de)
    if cach == "F":
        t = _gt_chon(dk=lambda t: _ms_le(t) and _gt_binh_phuong(t["l2"]), tran=60)
        de = (r"In triangle $ABC$, $BC = %d$, $CA = %d$, $AB = %d$. Let $AD$ be the interior angle bisector of angle $A$ ($D$ lies on side $BC$)."
              % (t["a"], t["b"], t["c"]))
        return dict(t=t, V="B" if bt == 1 else "C", de=de)
    raise KeyError(cach)


# ---------- các đại lượng ----------

def _ms_hoi(ten, c):
    """Câu hỏi (có dấu chấm) cho đại lượng `ten`."""
    k = ten[:3]
    if ten == "sin3":
        return r"Calculate $\sin\widehat{%s}$." % c["ten3"]
    if ten == "cos3":
        return r"Calculate $\cos\widehat{%s}$." % c["ten3"]
    if len(ten) == 4 and k in ("cos", "sin", "tan") and ten[3] in "ABC":
        return r"Calculate $\%s %s$." % (k, ten[3])
    if len(ten) == 5 and ten[:4] == "goc_":
        return r"Calculate the measure of angle $\widehat{%s}$ (in degrees)." % ten[4]
    tb = {"a": r"Calculate the length of side $BC$.", "b": r"Calculate the length of side $AC$.", "c": r"Calculate the length of side $AB$.",
          "c_cao": r"Calculate the length of side $AB$.", "a_cao": r"Calculate the length of side $BC$.", "b_med": r"Calculate the length of side $AC$.", "c_med": r"Calculate the length of side $AB$.",
          "S": r"Calculate the area $S$ of triangle $ABC$.", "Sheron": r"Calculate the area $S$ of triangle $ABC$.",
          "Sha": r"Calculate the area $S$ of triangle $ABC$.", "Shc": r"Calculate the area $S$ of triangle $ABC$.",
          "p": r"Calculate the semiperimeter $p$ of triangle $ABC$.",
          "R": r"Calculate the circumradius $R$ of triangle $ABC$.",
          "RA": r"Calculate the circumradius $R$ of triangle $ABC$.", "RB": r"Calculate the circumradius $R$ of triangle $ABC$.",
          "RC": r"Calculate the circumradius $R$ of triangle $ABC$.",
          "r": r"Calculate the inradius $r$ of triangle $ABC$.",
          "BD": r"Calculate the length of segment $BD$.", "DC": r"Calculate the length of segment $DC$.",
          "la": r"Calculate the length of the angle bisector $AD$.", "laC": r"Calculate the length of the angle bisector $AD$.",
          "SABD": r"Calculate the area of triangle $ABD$.", "SACD": r"Calculate the area of triangle $ACD$.",
          "sinBC": r"Calculate $\sin\left(B + C\right)$.", "cosBC": r"Calculate $\cos\left(B + C\right)$.",
          "sin180A": r"Calculate $\sin\left(180^{\circ} - A\right)$.", "cos180A": r"Calculate $\cos\left(180^{\circ} - A\right)$.",
          "ha": r"Calculate the length of the altitude $h_a$ from vertex $A$.", "hb": r"Calculate the length of the altitude $h_b$ from vertex $B$.",
          "hc": r"Calculate the length of the altitude $h_c$ from vertex $C$.",
          "ma": r"Calculate the length of the median $m_a$ from vertex $A$.",
          "cosAMB": r"Calculate $\cos\widehat{AMB}$.", "cosAMC": r"Calculate $\cos\widehat{AMC}$.", "sinAMB": r"Calculate $\sin\widehat{AMB}$.",
          "rut_sin": r"Calculate $\sin A$.", "rut_cos": r"Calculate $\cos A$.", "rut_tan": r"Calculate $\tan A$."}
    if ten in tb:
        return tb[ten]
    if ten in ("canh_a", "canh_b", "canh_c"):
        return r"Find the length of side $%s$." % _GT_TEN_CANH[ten[-1]]
    if ten == "goc3":
        return r"Calculate the measure of angle $\widehat{%s}$ (in degrees)." % c["ten3"]
    if ten == "sin3":
        return r"Calculate $\sin\widehat{%s}$." % c["ten3"]
    if ten == "cos3":
        return r"Calculate $\cos\widehat{%s}$." % c["ten3"]
    if ten == "sinPQ":
        return r"Calculate $\sin\left(\widehat{%s} + \widehat{%s}\right)$." % tuple(c["hai"])
    if ten == "cosPQ":
        return r"Calculate $\cos\left(\widehat{%s} + \widehat{%s}\right)$." % tuple(c["hai"])
    if ten == "chuvi":
        return r"Calculate the perimeter of triangle $ABC$."
    if ten == "h":
        return r"Calculate the length of the altitude from vertex $%s$ of triangle $ABC$." % c["u"]["G"]
    raise KeyError(ten)


def _ms_goc_t(t, X):
    """Số đo (độ) của góc X từ cos X chính xác."""
    return math.degrees(math.acos(float(t["cos"][X])))


def _ms_q(c, ten):
    """Một đại lượng: dict(hoi, v, ly, sai, xap, n, goc). Dạng góc cho bằng độ (c có "u") dùng `_msu_q`."""
    if "u" in c:
        return _msu_q(c, ten)
    t = c["t"]
    a, b, cc, S, p = t["a"], t["b"], t["c"], t["S"], t["p"]
    cs, sn = t["cos"], t["sin"]
    q = dict(hoi=_ms_hoi(ten, c), xap=False, goc=False, n=2 if ten[:3] in ("cos", "sin", "tan") else 1)
    if ten in ("sinBC", "cosBC", "sin180A", "cos180A"):
        if ten == "sinBC":
            v, ly = sn["A"], (r"In triangle $ABC$: $B + C = 180^{\circ} - A$, so $\sin\left(B + C\right) = \sin\left(180^{\circ} - A\right) = \sin A = %s$." % _L(sn["A"]))
            sai = [(-sn["A"], r"Wrong sign: the $\sin$ of two supplementary angles are equal"), (cs["A"], r"Mixing up $\sin A$ with $\cos A$"), (-cs["A"], r"Confusing with $\cos\left(B + C\right)$")]
        elif ten == "cosBC":
            v, ly = -cs["A"], (r"In triangle $ABC$: $B + C = 180^{\circ} - A$, so $\cos\left(B + C\right) = \cos\left(180^{\circ} - A\right) = -\cos A = %s$." % _L(-cs["A"]))
            sai = [(cs["A"], r"Forgetting the minus sign: the $\cos$ of two supplementary angles are opposite"), (sn["A"], r"Mixing up $\cos$ with $\sin$"), (-sn["A"], r"Mixing up $\cos$ with $\sin$ and wrong sign")]
        elif ten == "sin180A":
            v, ly = sn["A"], r"$\sin\left(180^{\circ} - A\right) = \sin A = %s$ (supplementary angles have equal sines)." % _L(sn["A"])
            sai = [(-sn["A"], "Sign error"), (cs["A"], r"Mixing up $\sin A$ with $\cos A$"), (-cs["A"], r"Confusing with $\cos\left(180^{\circ} - A\right)$")]
        else:
            v, ly = -cs["A"], r"$\cos\left(180^{\circ} - A\right) = -\cos A = %s$ (supplementary angles have opposite cosines)." % _L(-cs["A"])
            sai = [(cs["A"], "Forgetting the minus sign"), (sn["A"], r"Mixing up $\cos$ with $\sin$"), (-sn["A"], "Mixing up $\\cos$ with $\\sin$ and wrong sign")]
        q.update(v=v, ly=ly, sai=_gt_sai(sai, duong=False, gh1=True))
        return q
    if ten in ("rut_sin", "rut_cos", "rut_tan"):  # Bài 5: từ một giá trị lượng giác của A suy ra giá trị còn lại (không dùng cạnh)
        co = c["co"]
        s, k = sn["A"], cs["A"]
        nhon = k > 0
        dau = ">" if nhon else "<"
        if ten == "rut_sin":
            v = s
            ly = (r"From $\cos A = %s$: $\sin^{2}A = 1 - \cos^{2}A = %s$, and since $\sin A > 0$, $\sin A = %s$." % (_L(k), _L(1 - k * k), _L(s))
                  if co == "cos" else r"$\sin A = \tan A\cdot\cos A = %s$." % _L(s))
            sai = [(-s, r"Forgetting that $\sin A > 0$"), (k, r"Mixing up $\sin A$ with $\cos A$"), (1 - k * k, "Forgot to take the square root")]
            q.update(v=v, ly=ly, sai=_gt_sai(sai, duong=True, gh1=True))
        elif ten == "rut_cos":
            v = k
            if co == "sin":
                ly = (r"$\cos^{2}A = 1 - \sin^{2}A = %s$; angle $A$ is %s, so $\cos A %s 0$, hence $\cos A = %s$." % (_L(1 - s * s), "acute" if nhon else "obtuse", dau, _L(k)))
            else:
                ly = (r"$\dfrac{1}{\cos^{2}A} = 1 + \tan^{2}A = %s$, so $\cos^{2}A = %s$; since $\tan A %s 0$, angle $A$ is %s, $\cos A %s 0$ and $\cos A = %s$."
                      % (_L(1 + (s / k) ** 2), _L(k * k), dau, "acute" if nhon else "obtuse", dau, _L(k)))
            sai = [(-k, "Sign error"), (k * k, "Forgot to take the square root"), ((1 if nhon else -1) * (1 - s), "Forgot to square")]
            q.update(v=v, ly=ly, sai=_gt_sai(sai, duong=False, gh1=True))
        else:
            v = s / k
            ly = r"$\tan A = \dfrac{\sin A}{\cos A} = \dfrac{%s}{%s} = %s$." % (_L(s), _gt_ngoac(k), _L(v))
            sai = [(1 / v, "Numerator and denominator swapped"), (-v, "Sign error"), (s * k, r"Mistakenly using $\tan = \sin\cdot\cos$")]
            q.update(v=v, ly=ly, sai=_gt_sai(sai, duong=False))
        return q
    if len(ten) == 5 and ten[:4] == "goc_":
        X = ten[4]
        g = _ms_goc_t(t, X)
        v = cs[X]
        ly = (r"From $\cos %s = %s$ we get $\widehat{%s} = \arccos\left(%s\right) \approx %s^{\circ}$ (using a handheld calculator in degree mode)." % (X, _L(v), X, _L(v), _x1(g, 2)))
        sai = [(180 - g, "Confusing with the supplementary angle"), (math.degrees(math.asin(float(sn[X]))) if cs[X] < 0 else 90 - g, "Mistakenly using $\\sin$ instead of $\\cos$"), (g / 2, "Dividing by an extra 2")]
        q.update(v=g, ly=ly, sai=[(w, l) for w, l in sai if 0 < w < 180], xap=True, goc=True, n=1)
        return q
    if len(ten) == 2 and ten[0] == "R" and ten[1] in "ABC":
        X = ten[1]
        x = t[X.lower()]
        v = t["R"]
        ly = r"Law of sines: $R = \dfrac{%s}{2\sin %s} = \dfrac{%d}{2\cdot %s} = %s$." % (_GT_TEN_CANH[X.lower()], X, x, _L(sn[X]), _L(v))
        sai = [(2 * v, "Forgot to divide by 2"), (v / 2, "Dividing by an extra 2"), (x / (2 * abs(cs[X])), r"Mixing up $\sin %s$ with $\cos %s$" % (X, X)), (x / sn[X], "Forgetting the factor 2 in the denominator")]
        q.update(v=v, ly=ly, sai=_gt_sai(sai))
        return q
    if ten in ("SABD", "SACD"):
        ABD = ten == "SABD"
        x = t["BD"] if ABD else t["DC"]
        v = S * x / a
        ly = (r"Triangles $%s$ and $ABC$ share the altitude from $A$, so $S_{%s} = \dfrac{%s}{BC}\cdot S = \dfrac{%s}{%d}\cdot %s = %s$."
              % ("ABD" if ABD else "ACD", "ABD" if ABD else "ACD", "BD" if ABD else "DC", _L(x), a, _L(S), _L(v)))
        sai = [(S / 2, "Confusing with half the area"), (S * (t["DC"] if ABD else t["BD"]) / a, "Mixing up triangles $ABD$ and $ACD$"), (S * x, "Forgetting to divide by $BC$"), (S * x / a / 2, "Dividing by an extra 2")]
        q.update(v=v, ly=ly, sai=_gt_sai(sai))
        return q
    # còn lại: đại lượng đã có trong `_gt_q` (TF_T)
    mau, v, ly, sai = _gt_q(t, ten)
    q.update(v=sympify(v), ly=ly, sai=sai)
    return q


def _msu_q(c, ten):
    """Đại lượng của tam giác cho bằng hai góc (độ) và một cạnh (cách cho B); giá trị gần đúng."""
    u = c["u"]
    ang, sin, cos = u["ang"], u["sin"], u["cos"]
    G, cg, g = u["G"], u["cg"], u["canh"][u["cg"]]
    P, Q = c["hai"]
    R3 = c["ten3"]
    g3 = ang[R3]
    q = dict(hoi=_ms_hoi(ten, c), xap=True, goc=False, n=1)
    if ten == "goc3":
        gp, gq = ang[P], ang[Q]
        ly = r"The sum of the three angles of a triangle is $180^{\circ}$, so $\widehat{%s} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$." % (R3, gp, gq, g3)
        sai = [(g3 + 10, "Addition error"), (gp + gq, r"Forgetting to subtract from $180^{\circ}$"), (180 - g3, "Confusing with the supplementary angle")]
        q.update(v=Integer(g3), ly=ly, sai=[(w, l) for w, l in sai if 0 < w < 180 and w != g3], xap=False, goc=True)
        return q
    if ten in ("canh_a", "canh_b", "canh_c"):
        tc = ten[-1]
        X = tc.upper()
        n_x, n_g = _GT_TEN_CANH[tc], _GT_TEN_CANH[cg]
        v = u["canh"][tc]
        ly = (r"Law of sines: $\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s}$, so $%s = \dfrac{%s\cdot\sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$."
              % (n_x, X, n_g, G, n_x, _gu_g(g), ang[X], ang[G], _x1(v, 2)))
        sai = [(g * sin[X], r"Forgetting to divide by $\sin %s$" % G), (g * sin[G] / sin[X], "Numerator and denominator swapped"),
               (g * cos[X] / cos[G] if abs(cos[G]) > 1e-9 else None, r"Using $\cos$ instead of $\sin$"), (g * ang[X] / ang[G], "Using the ratio of the angle measures")]
        q.update(v=v, ly=ly, sai=[(w, l) for w, l in sai if w is not None and w > 0])
        return q
    if ten == "S":
        X = [x for x in "ABC" if x != G][0]
        Y = [x for x in "ABC" if x not in (G, X)][0]
        cx = X.lower()
        v = 0.5 * g * u["canh"][cx] * sin[Y]
        ly = (r"Area $S = \dfrac{1}{2}\cdot %s\cdot %s\cdot\sin %d^{\circ} \approx \dfrac{1}{2}\cdot %s\cdot %s\cdot %s \approx %s$."
              % (_GT_TEN_CANH[cg], _GT_TEN_CANH[cx], ang[Y], _x1(g, 2), _x1(u["canh"][cx], 2), _x1(sin[Y], 3), _x1(v, 2)))
        sai = [(2 * v, r"Forgetting the factor $\dfrac{1}{2}$"), (0.5 * g * u["canh"][cx] * cos[Y] if cos[Y] > 0 else None, r"Using $\cos$ instead of $\sin$"),
               (v / 2, r"Multiplying by an extra $\dfrac{1}{2}$"), (0.5 * g * u["canh"][cx], "Forgetting to multiply by the sine of the included angle")]
        q.update(v=v, ly=ly, sai=[(w, l) for w, l in sai if w is not None])
        return q
    if ten == "R":
        v = u["R"]
        ly = r"Law of sines: $R = \dfrac{%s}{2\sin %d^{\circ}} \approx \dfrac{%s}{2\cdot %s} \approx %s$." % (_GT_TEN_CANH[cg], ang[G], _gu_g(g), _x1(sin[G], 3), _x1(v, 2))
        sai = [(2 * v, "Forgot to divide by 2"), (v / 2, "Dividing by an extra 2"), (g / (2 * abs(cos[G])) if abs(cos[G]) > 1e-9 else None, r"Using $\cos$ instead of $\sin$")]
        q.update(v=v, ly=ly, sai=[(w, l) for w, l in sai if w is not None])
        return q
    if ten == "h":
        v = u["h"][cg]
        ly = r"$S \approx %s$, so the altitude from $%s$ is $h = \dfrac{2S}{%s} \approx \dfrac{2\cdot %s}{%s} \approx %s$." % (_x1(u["S"], 2), G, _x1(g, 2), _x1(u["S"], 2), _x1(g, 2), _x1(v, 2))
        sai = [(u["S"] / g, "Forgot to multiply by 2"), (2 * v, "Multiplied by an extra factor of 2"), (v / 2, "Dividing by an extra 2")]
        q.update(v=v, ly=ly, sai=sai)
        return q
    if ten in ("sin3", "cos3"):
        k = ten[:3]
        v = sin[R3] if k == "sin" else cos[R3]
        ly = r"$\%s\widehat{%s} = \%s %d^{\circ} \approx %s$ (using a handheld calculator in degree mode)." % (k, R3, k, g3, _x1(v, 3))
        if k == "sin":
            sai = [(abs(cos[R3]), r"Mixing up $\sin$ with $\cos$"), (1 - v, r"Mistakenly using $1 - \sin$"), (math.sin(g3), "Leaving the calculator in radian mode")]
        else:
            sai = [(-v, "Sign error"), (sin[R3], r"Mixing up $\cos$ with $\sin$"), (math.cos(g3), "Leaving the calculator in radian mode")]
        q.update(v=v, ly=ly, sai=sai, n=2)
        return q
    if ten in ("sinPQ", "cosPQ"):
        k = ten[:3]
        tong = ang[P] + ang[Q]
        v = math.sin(math.radians(tong)) if k == "sin" else math.cos(math.radians(tong))
        cu = (r"$\widehat{%s} + \widehat{%s} = %d^{\circ} + %d^{\circ} = %d^{\circ}$, which is supplementary to $\widehat{%s} = %d^{\circ}$, so "
              % (P, Q, ang[P], ang[Q], tong, R3, g3))
        if k == "sin":
            ly = cu + r"$\sin\left(\widehat{%s} + \widehat{%s}\right) = \sin\widehat{%s} = \sin %d^{\circ} \approx %s$." % (P, Q, R3, g3, _x1(v, 3))
            sai = [(-v, "Sign error"), (math.cos(math.radians(tong)), r"Mixing up $\sin$ with $\cos$"), (math.sin(tong), "Leaving the calculator in radian mode")]
        else:
            ly = cu + r"$\cos\left(\widehat{%s} + \widehat{%s}\right) = -\cos\widehat{%s} = -\cos %d^{\circ} \approx %s$." % (P, Q, R3, g3, _x1(v, 3))
            sai = [(-v, "Forgetting the minus sign for the supplementary angle"), (math.sin(math.radians(tong)), r"Mixing up $\cos$ with $\sin$"), (math.cos(tong), "Leaving the calculator in radian mode")]
        q.update(v=v, ly=ly, sai=sai, n=2)
        return q
    if ten == "chuvi":
        tong = sum(u["canh"].values())
        ly = r"Perimeter $= BC + CA + AB \approx %s + %s + %s \approx %s$." % (_x1(u["canh"]["a"], 2), _x1(u["canh"]["b"], 2), _x1(u["canh"]["c"], 2), _x1(tong, 2))
        sai = [(tong / 2, "Confusing with the semiperimeter"), (tong - g, "Missing the given side"), (tong + g, "Adding the given side an extra time")]
        q.update(v=tong, ly=ly, sai=sai)
        return q
    raise KeyError(ten)


# ---------- chuỗi đại lượng cho từng (đơn vị, cách cho, biến thể) ----------

def _ms_ten_y(c, bt):
    """Ý thứ hai: một trong hai đỉnh còn lại ngoài đỉnh của biến thể (cách cho C)."""
    return random.choice([x for x in "ABC" if x != c["X"]])


def _ms_pool(dv, cach, bt, c):
    """Trả về dict(mc=[chuỗi], tl=[(chuỗi ý a, chuỗi ý b)], sin=bool, hd=...).
    - mc: các chuỗi (bước trung gian ... đại lượng hỏi) dùng cho MC và SA, chọn ngẫu nhiên một chuỗi;
    - tl: các cặp chuỗi (ý a, ý b) dùng cho tự luận (đúng 2 ý);
    - sin: lời giải cần sin A (cách cho A) để `_ms_chuan` biết có nêu dòng tính sin A hay không."""
    k = (dv, cach)
    t = c.get("t")
    X = c.get("X")
    if cach == "D":
        xc = "c_cao" if bt == 1 else "a_cao"
    if k == ("TH031", "A"):
        return dict(mc=[["sinBC"], ["cosBC"], ["sin180A"]], sin=True)
    if k == ("TH031", "B"):
        return dict(mc=[["sinPQ"], ["cosPQ"]])
    if k == ("TH030", "A"):
        cap = {1: (["rut_sin"], ["rut_tan"]), 2: (["rut_cos"], ["rut_tan"]), 3: (["rut_cos"], ["rut_sin"])}[bt]
        return dict(mc=[cap[0], cap[0] + cap[1]], tl=[cap], sin=True, chuan_khong=True)
    if k == ("TH030", "B"):
        return dict(mc=[["goc3", "sin3"], ["goc3", "cos3"]])
    if k == ("TH032", "A"):
        return dict(mc=[["a"]], tl=[(["a"], ["cosB"]), (["a"], ["cosC"])])
    if k == ("TH032", "C"):
        return dict(mc=[["cos" + X]], tl=[(["cos" + X], ["cos" + _ms_ten_y(c, bt)])])
    if k == ("TH032", "D"):
        return dict(mc=[[xc, "b"]], tl=[([xc], ["b"])], chuan_d=True)
    if k == ("TH032", "E"):
        cm, med = ("cosAMB", "b_med") if bt == 1 else ("cosAMC", "c_med")
        return dict(mc=[[cm, med]], tl=[([cm], [med])])
    if k == ("TH032", "F"):
        bd, la = ("BD", "la") if bt == 1 else ("DC", "laC")
        return dict(mc=[[la]], tl=[([bd], [la])])
    if k == ("TH033", "B"):
        cd = [x for x in "abc" if x != c["cg"]]
        random.shuffle(cd)
        return dict(mc=[["goc3", "canh_" + x] for x in cd], tl=[(["goc3", "canh_" + cd[0]], ["canh_" + cd[1]])])
    if k == ("TH033", "C"):
        return dict(mc=[["cos" + X, "sin" + X, "R" + X]], tl=[(["cos" + X, "sin" + X], ["R" + X])])
    if k == ("TH034", "A"):
        return dict(mc=[["S"]], tl=[(["S"], ["a", "ha"]), (["S"], ["a", "r"])], sin=True)
    if k == ("TH034", "B"):
        x = [y for y in "abc" if y.upper() != c["u"]["G"]][0]
        return dict(mc=[["goc3", "canh_" + x, "S"]])
    if k == ("TH034", "C"):
        hk = "h" + random.choice("abc")
        mc = {1: [["Sheron"]], 2: [["Sheron", "r"]], 3: [["Sheron", hk]]}[bt]
        return dict(mc=mc, tl=[(["Sheron"], ["r"]), (["Sheron"], [hk])])
    if k == ("TH034", "D"):
        return dict(mc=[["Sha" if bt == 1 else "Shc"]])
    if k == ("TH035", "A"):
        Y = random.choice("BC")
        return dict(mc=[["a", "cos" + Y, "goc_" + Y]], tl=[(["a"], ["cos" + Y, "goc_" + Y])])
    if k == ("TH035", "B"):
        cd = [x for x in "abc" if x != c["cg"]]
        random.shuffle(cd)
        return dict(mc=[["goc3", "canh_" + cd[0], "canh_" + cd[1], "chuvi"]], tl=[(["goc3", "canh_" + cd[0]], ["canh_" + cd[1], "chuvi"])])
    if k == ("TH035", "C"):
        Y = _ms_ten_y(c, bt)
        return dict(mc=[["cos" + X, "goc_" + X]], tl=[(["cos" + X, "goc_" + X], ["cos" + Y, "goc_" + Y])])
    if k == ("VD032", "A"):
        return dict(mc=[["a", "R"], ["a", "S", "ha"]], tl=[(["a"], ["R"]), (["a"], ["S", "ha"])], sin=True)
    if k == ("VD032", "B"):
        x = [y for y in "abc" if y.upper() != c["u"]["G"]][0]
        return dict(mc=[["goc3", "canh_" + x, "S"], ["goc3", "canh_" + x, "S", "h"]],
                    tl=[(["goc3", "canh_" + x], ["S"]), (["goc3", "canh_" + x], ["S", "h"])])
    if k == ("VD032", "C"):
        hx = "h" + X.lower()
        ch = [["Sheron", hx], ["Sheron", "r"], ["cos" + X, "sin" + X, "R" + X]]
        return dict(mc=ch, tl=[(["Sheron"], ch[1]), (["Sheron"], ch[0]), (["cos" + X, "sin" + X], ["R" + X])])
    if k == ("VD032", "D"):
        return dict(mc=[[xc, "b", "cosC"], [xc, "b", "RB"]], tl=[([xc, "b"], ["cosC"]), ([xc, "b"], ["RB"])], chuan_d=True)
    if k == ("VD032", "E"):
        cm, med = ("cosAMB", "b_med") if bt == 1 else ("cosAMC", "c_med")
        fin = [["cosA"], ["cosA", "sinA", "S"]] if bt == 1 else [["cosA", "sinA", "R"], ["cosA", "sinA", "S"]]
        return dict(mc=[[cm, med] + f for f in fin], tl=[([cm, med], f) for f in fin])
    if k == ("VD032", "F"):
        bd, sq = ("BD", "SABD") if bt == 1 else ("DC", "SACD")
        return dict(mc=[["Sheron", bd, sq]], tl=[([bd], ["Sheron", sq])])
    raise KeyError(k)


# ---------- định dạng đáp số, nhiễu, ghép câu ----------

class _MsLai(Exception):
    """The generated data is unusable (too close to a rounding boundary...): generate again."""


def _ms_chon_n(q, loai):
    """Số chữ số làm tròn cho đại lượng hỏi: None nếu giữ giá trị chính xác. Ném _MsLai nếu sát ranh giới làm tròn."""
    v = q["v"]
    if not q["xap"]:
        if loai == "MC" or loai == "TL" or v.is_Integer:
            return None
        if (v * 100).is_Integer:  # thập phân hữu hạn (tối đa hai chữ số): đáp số viết đúng, không cần làm tròn
            return None
    f = float(v)
    for n in (q["n"], q["n"] + 1, q["n"] + 2):
        if _xa_bien(f, n):
            return n
    raise _MsLai()


def _ms_so(q, w, n):
    """Chuỗi số (không có $) của giá trị w."""
    if n is None:
        return _L(sympify(w))
    return _x1(float(w), n)


def _ms_mc_fmt(q, w, n):
    return "$%s%s$" % (_ms_so(q, w, n), r"^{\circ}" if q["goc"] else "")


def _ms_sa_fmt(q, w, n):
    if n is None:
        w = sympify(w)
        return str(int(w)) if w.is_Integer else _xx(float(w), 2)
    return _xx(float(w), n)


def _ms_pad(q, n):
    """Hàm sinh thêm phương án nhiễu khi chưa đủ ba: k = 1, 2, ... -> giá trị khác (sympy nếu chính xác, float nếu gần đúng)."""
    v = q["v"]
    f = float(v)
    if q["goc"]:
        return lambda k: (v if n is None else f) + (5 * k if f < 90 else -5 * k)
    if n is None:
        if abs(f) < 1:
            return lambda k: v * Rational(k + 1, k + 2)
        if v.is_Integer:
            return lambda k: v + k
        return lambda k: v * Rational(10 + k, 10)
    if abs(f) < 1:
        return lambda k: f * (1 - 0.07 * k)
    return lambda k: f * (1 + 0.09 * k)


def _ms_nhieu(q, n, dinh_dang):
    """Đúng ba phương án nhiễu (chuỗi) khác nhau và khác đáp số."""
    dung = dinh_dang(q, q["v"], n)
    pad = _ms_pad(q, n)
    f = float(q["v"])
    uv = [dinh_dang(q, w, n) for w, _ in q["sai"] if not (q["xap"] and not q["goc"] and f > 0 and not f / 3 <= float(w) <= 3 * f)]
    return dung, _ba_nhieu(dung, uv, buoc=lambda k: dinh_dang(q, pad(k), n))


def _ms_lam_tron(hoi, n):
    """Thêm yêu cầu làm tròn vào câu hỏi."""
    if n is None:
        return hoi
    yc = "rounded to %s" % _MS_MUC_HANG[n]
    if hoi.endswith("(in degrees)."):
        return hoi[:-len("(in degrees).")] + "(in degrees, %s)." % yc
    return hoi.rstrip(".") + " (%s)." % yc


def _ms_giai(qs, chuan, n, loai=""):
    """Lời giải: [dòng đổi giá trị lượng giác] + lời giải từng bước; câu chốt khi có làm tròn (hoặc đổi ra số thập phân ở câu trả lời ngắn)."""
    buoc = ([chuan] if chuan else []) + [q["ly"] for q in qs]
    s = _MS_NOI.join(buoc)
    f = qs[-1]
    if loai == "SA" and n is None and not f["v"].is_Integer:
        s += r" In decimal form: $%s$." % _xx(float(f["v"]), 2)
    if n is not None:
        s += r" Rounding to %s, we get $%s%s$." % (_MS_MUC_HANG[n], _x1(float(f["v"]), n), r"^{\circ}" if f["goc"] else "")
    return s


def _ms_chuan_tong(c, pool, cach):
    if pool.get("chuan_d"):
        return _ms_chuan_d(c)
    if cach == "A" and not pool.get("chuan_khong"):
        return _ms_chuan(c, pool.get("sin", False))
    return ""


def _ms_tl_da(c, q, n):
    if n is None:
        return _L(q["v"]) + (r"^{\circ}" if q["goc"] else "")
    return r"\approx %s%s" % (_x1(float(q["v"]), n), r"^{\circ}" if q["goc"] else "")


def _ms_nb029(bt):
    """NB029 (Bài 5): dấu của sin, côsin, tang, côtang của MỘT góc trong tam giác (cô Lan 11/10/2026).
    bt = 1: tam giác nhọn; bt = 2: tam giác có góc A tù. Bốn phương án cùng nói về một góc X (A, B hoặc C ngẫu nhiên),
    mỗi phương án là dấu của một trong bốn giá trị lượng giác; hỏi khẳng định ĐÚNG hoặc SAI (ngẫu nhiên).
    Trả về (đề, đáp án, nhiễu, lời giải, khoá)."""
    X = random.choice("ABC")
    tu = (bt == 2 and X == "A")  # góc X là góc tù
    ham = ["sin", "cos", "tan", "cot"]
    dau = {"sin": 1, "cos": -1 if tu else 1, "tan": -1 if tu else 1, "cot": -1 if tu else 1}  # dấu thật của từng giá trị lượng giác
    hoi_dung = random.choice([True, False])
    le = random.choice(ham)  # phương án "lẻ loi": là khẳng định đúng duy nhất (hỏi đúng) hoặc sai duy nhất (hỏi sai)
    pa = {}
    for f in ham:
        la_dung = (f == le) if hoi_dung else (f != le)
        pa[f] = r"$\%s %s %s 0$" % (f, X, ">" if (dau[f] if la_dung else -dau[f]) > 0 else "<")
    dap = pa[le]
    nhieu = [pa[f] for f in ham if f != le]
    kq = r"the %s statement is %s" % ("true" if hoi_dung else "false", dap)
    bang = ", ".join(r"$\%s %s %s 0$" % (f, X, ">" if dau[f] > 0 else "<") for f in ham)
    if bt == 1:
        de = r"Given an acute triangle $ABC$."
        ly = r"Since triangle $ABC$ is acute, angle $%s$ is acute, so %s." % (X, bang)
    else:
        de = r"Given triangle $ABC$ with obtuse angle $A$."
        if X == "A":
            ly = r"Angle $A$ is obtuse, so %s." % bang
        else:
            ly = (r"Since triangle $ABC$ has an obtuse angle $A$, the other two angles are both acute (the three angles sum to $180^{\circ}$); angle $%s$ is acute, so %s." % (X, bang))
    ly += " Hence " + kq + "."
    debai = de + r" Which of the following statements is \textbf{%s}?" % ("true" if hoi_dung else "false")
    return debai, dap, nhieu, ly, (bt, X, hoi_dung, le)


# ===== Bài 5: từ MỘT giá trị lượng giác của góc α tìm MỘT giá trị lượng giác khác (cô Lan 11/10/2026) =====
# Cách cho G, H, I, J = cho sin, cos, tan, cot của α; biến thể = giá trị lượng giác cần tìm. Mỗi câu chỉ tìm MỘT giá trị
# (cả bốn phương án MC cùng là giá trị của đại lượng đó), câu dẫn không nêu dữ kiện thừa.
_MS_ALPHA_CHO = {"G": "sin", "H": "cos", "I": "tan", "J": "cot"}
_MS_ALPHA_HOI = {"G": ["cos", "tan", "cot"], "H": ["sin", "tan", "cot"], "I": ["cot", "cos", "sin"], "J": ["tan", "sin", "cos"]}
_MS_BA_PY = list(BO_BA_PYTAGO) + [(12, 35, 37), (9, 40, 41)]


def _ms_ctx_alpha(cach):
    d, k, h = random.choice(_MS_BA_PY)
    if random.random() < 0.5:
        d, k = k, d
    tu = random.random() < 0.5  # góc tù
    sn = Rational(d, h)
    cs = (-1 if tu else 1) * Rational(k, h)
    v = dict(sin=sn, cos=cs, tan=sn / cs, cot=cs / sn)
    cho = _MS_ALPHA_CHO[cach]
    if cho == "sin":  # sin luôn dương trên (0°; 180°) nên PHẢI cho khoảng của góc để biết dấu côsin
        kh = r"$90^{\circ} < \alpha < 180^{\circ}$" if tu else r"$0^{\circ} < \alpha < 90^{\circ}$"
        de = r"Given an angle $\alpha$ such that $\sin\alpha = %s$ and %s." % (_L(sn), kh)
    else:  # dấu của giá trị cho trước đã cho biết góc nhọn hay tù
        de = r"Given an angle $\alpha$ with $0^{\circ} < \alpha < 180^{\circ}$ and $\%s\alpha = %s$." % (cho, _L(v[cho]))
    return dict(de=de, v=v, tu=tu, cho=cho, cach=cach)


def _ms_alpha_cos_tu_sin(v, tu):
    return (r"From $\sin^{2}\alpha + \cos^{2}\alpha = 1$ we get $\cos^{2}\alpha = 1 - %s^{2} = %s$, so $\cos\alpha = \pm %s$. "
            r"Since $\alpha$ is %s, $\cos\alpha %s 0$, hence $\cos\alpha = %s$."
            % (_gt_p(v["sin"]), _L(v["cos"] ** 2), _L(abs(v["cos"])), "obtuse" if tu else "acute", "<" if tu else ">", _L(v["cos"])))


def _ms_alpha_sin_tu_cos(v):
    return (r"From $\sin^{2}\alpha + \cos^{2}\alpha = 1$ we get $\sin^{2}\alpha = 1 - %s^{2} = %s$, so $\sin\alpha = \pm %s$. Since "
            r"$0^{\circ} < \alpha < 180^{\circ}$, we have $\sin\alpha > 0$, hence $\sin\alpha = %s$."
            % (_gt_p(v["cos"]), _L(v["sin"] ** 2), _L(v["sin"]), _L(v["sin"])))


def _ms_alpha_buoc(c, ten):
    """Lời giải tìm `ten` từ giá trị cho trước, tách thành (trung_gian, phần_tính_trung_gian, dòng_cuối).
    trung_gian: tên giá trị lượng giác phải tính trước (cos hoặc sin) hoặc None; khi không có thì phần tính trung gian là None."""
    v, tu, cho = c["v"], c["tu"], c["cho"]
    loai = "obtuse" if tu else "acute"
    ngang = lambda k: (r"\dfrac{%s}{%s}" % (_L(v[k[0]]), _gt_ngoac(v[k[1]])))
    if cho == "sin":
        b = _ms_alpha_cos_tu_sin(v, tu)
        if ten == "cos":
            return None, None, b
        if ten == "tan":
            return "cos", b, r"$\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = \dfrac{%s}{%s} = %s$." % (_L(v["sin"]), _gt_ngoac(v["cos"]), _L(v["tan"]))
        return "cos", b, r"$\cot\alpha = \dfrac{\cos\alpha}{\sin\alpha} = \dfrac{%s}{%s} = %s$." % (_gt_ngoac(v["cos"]), _L(v["sin"]), _L(v["cot"]))
    if cho == "cos":
        b = _ms_alpha_sin_tu_cos(v)
        if ten == "sin":
            return None, None, b
        if ten == "tan":
            return "sin", b, r"$\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = \dfrac{%s}{%s} = %s$." % (_L(v["sin"]), _gt_ngoac(v["cos"]), _L(v["tan"]))
        return "sin", b, r"$\cot\alpha = \dfrac{\cos\alpha}{\sin\alpha} = \dfrac{%s}{%s} = %s$." % (_gt_ngoac(v["cos"]), _L(v["sin"]), _L(v["cot"]))
    if cho == "tan":
        if ten == "cot":
            return None, None, r"Since $\tan\alpha\cdot\cot\alpha = 1$, we have $\cot\alpha = \dfrac{1}{\tan\alpha} = \dfrac{1}{%s} = %s$." % (_gt_ngoac(v["tan"]), _L(v["cot"]))
        b = (r"From $1 + \tan^{2}\alpha = \dfrac{1}{\cos^{2}\alpha}$ we get $\cos^{2}\alpha = \dfrac{1}{1 + %s^{2}} = %s$, so $\cos\alpha = \pm %s$. "
             r"Since $\tan\alpha %s 0$ and $\sin\alpha > 0$, $\alpha$ is %s, $\cos\alpha %s 0$, hence $\cos\alpha = %s$."
             % (_gt_p(v["tan"]), _L(v["cos"] ** 2), _L(abs(v["cos"])), "<" if tu else ">", loai, "<" if tu else ">", _L(v["cos"])))
        if ten == "cos":
            return None, None, b
        return "cos", b, r"$\sin\alpha = \tan\alpha\cdot\cos\alpha = %s\cdot %s = %s$." % (_gt_ngoac(v["tan"]), _gt_ngoac(v["cos"]), _L(v["sin"]))
    # cho == "cot"
    if ten == "tan":
        return None, None, r"Since $\tan\alpha\cdot\cot\alpha = 1$, we have $\tan\alpha = \dfrac{1}{\cot\alpha} = \dfrac{1}{%s} = %s$." % (_gt_ngoac(v["cot"]), _L(v["tan"]))
    b = (r"From $1 + \cot^{2}\alpha = \dfrac{1}{\sin^{2}\alpha}$ we get $\sin^{2}\alpha = \dfrac{1}{1 + %s^{2}} = %s$, so $\sin\alpha = \pm %s$. Since "
         r"$0^{\circ} < \alpha < 180^{\circ}$, we have $\sin\alpha > 0$, hence $\sin\alpha = %s$." % (_gt_p(v["cot"]), _L(v["sin"] ** 2), _L(v["sin"]), _L(v["sin"])))
    if ten == "sin":
        return None, None, b
    return "sin", b, r"$\cos\alpha = \cot\alpha\cdot\sin\alpha = %s\cdot %s = %s$." % (_gt_ngoac(v["cot"]), _L(v["sin"]), _L(v["cos"]))


def _ms_alpha_ly(c, ten, biet=()):
    """Lời giải; biet: các giá trị lượng giác đã tính ở ý trước (tự luận) -> không tính lại."""
    trung, base, cuoi = _ms_alpha_buoc(c, ten)
    if trung is None:
        return cuoi
    if trung in biet:
        return r"From part a) we already have $\%s\alpha = %s$." % (trung, _L(c["v"][trung])) + _MS_NOI + cuoi
    return base + _MS_NOI + cuoi


def _ms_q_alpha(c, ten, biet=()):
    """Đại lượng (một giá trị lượng giác của α) ở dạng dict dùng chung với `_ms_chon_n`, `_ms_nhieu`, `_ms_giai`."""
    v = c["v"]
    x = v[ten]
    sai = [(-x, "Sign mistake"), (1 / x, "Confusing with the reciprocal value"), (-1 / x, "Wrong sign and reciprocal")]
    sai += [(w, "Confusing the trigonometric function") for f in ("sin", "cos", "tan", "cot") if f != ten for w in (v[f], -v[f])]
    return dict(hoi=r"Calculate $\%s\alpha$." % ten, v=x, ly=_ms_alpha_ly(c, ten, biet), sai=sai, xap=False, goc=False, n=2)


def _ms_sinh_alpha(loai, cach, bt, socau, tham):
    ket, da, lan = "", set(), 0
    hoi = _MS_ALPHA_HOI[cach]
    while len(da) < socau:
        lan += 1
        if lan > 800:
            raise RuntimeError("could not generate %d distinct questions for TH030 %s %d" % (socau, cach, bt))
        try:
            c = _ms_ctx_alpha(cach)
            if loai == "TL":
                cap = [(0, 1), (0, 2), (1, 2)][bt - 1]
                a, b = random.sample([hoi[cap[0]], hoi[cap[1]]], 2)
                if _ms_alpha_buoc(c, a)[0] == b:  # ý a cần tính b trước: đặt b làm ý a để ý b dùng lại kết quả
                    a, b = b, a
                khoa = c["de"]  # mỗi câu dẫn chỉ ra một lần (kể cả khi hai ý đổi chỗ)
                if khoa in da:
                    continue
                qa = _ms_q_alpha(c, a)
                qb = _ms_q_alpha(c, b, biet={a, _ms_alpha_buoc(c, a)[0]})
                na, nb = _ms_chon_n(qa, "TL"), _ms_chon_n(qb, "TL")
                ds = [(_ms_lam_tron(qa["hoi"], na), _ms_tl_da(c, qa, na), _ms_giai([qa], "", na)),
                      (_ms_lam_tron(qb["hoi"], nb), _ms_tl_da(c, qb, nb), _ms_giai([qb], "", nb))]
                da.add(khoa)
                ket += TL_answer_text(c["de"], ds, 0, 0, tham)
                continue
            ten = hoi[bt - 1]
            khoa = (c["de"], ten)
            if khoa in da:
                continue
            q = _ms_q_alpha(c, ten)
            n = _ms_chon_n(q, loai)
            fmt = _ms_mc_fmt if loai == "MC" else _ms_sa_fmt
            dap, nhieu = _ms_nhieu(q, n, fmt)
            da.add(khoa)
            ket += MC_SA_answer_text(c["de"] + " " + _ms_lam_tron(q["hoi"], n), dap, nhieu, _ms_giai([q], "", n, loai), 0, 0, tham)
        except _MsLai:
            continue
    return ket


def _ms_sinh(loai, dv, cach, bt, socau, tham):
    """Sinh `socau` câu khác nhau. loai: "MC" | "SA" | "TL"; tham: dang (MC=1, SA=2) hoặc dong (TL)."""
    if cach in _MS_ALPHA_CHO:
        return _ms_sinh_alpha(loai, cach, bt, socau, tham)
    ket, da, lan = "", set(), 0
    while len(da) < socau:
        lan += 1
        if lan > 800:
            raise RuntimeError("could not generate %d distinct questions for %s %s %d" % (socau, dv, cach, bt))
        try:
            if dv == "NB029":
                debai, dap, nhieu, giai, khoa = _ms_nb029(bt)
                if khoa in da:
                    continue
                da.add(khoa)
                ket += MC_SA_answer_text(debai, dap, nhieu, giai, 0, 0, tham)
                continue
            c = _ms_ctx(cach, bt, dv)
            pool = _ms_pool(dv, cach, bt, c)
            chuan = _ms_chuan_tong(c, pool, cach)
            if loai == "TL":
                ca, cb = random.choice(pool["tl"])
                qa = [_ms_q(c, x) for x in ca]
                qb = [_ms_q(c, x) for x in cb]
                na, nb = _ms_chon_n(qa[-1], "TL"), _ms_chon_n(qb[-1], "TL")
                khoa = (c["de"], tuple(ca), tuple(cb))
                if khoa in da:
                    continue
                ds = [(_ms_lam_tron(qa[-1]["hoi"], na), _ms_tl_da(c, qa[-1], na), _ms_giai(qa, chuan, na)),
                      (_ms_lam_tron(qb[-1]["hoi"], nb), _ms_tl_da(c, qb[-1], nb), _ms_giai(qb, "", nb))]
                da.add(khoa)
                ket += TL_answer_text(c["de"], ds, 0, 0, tham)
                continue
            ch = random.choice(pool["mc"])
            qs = [_ms_q(c, x) for x in ch]
            f = qs[-1]
            n = _ms_chon_n(f, loai)
            khoa = (c["de"], tuple(ch))
            if khoa in da:
                continue
            fmt = _ms_mc_fmt if loai == "MC" else _ms_sa_fmt
            dap, nhieu = _ms_nhieu(f, n, fmt)
            debai = c["de"] + " " + _ms_lam_tron(f["hoi"], n)
            da.add(khoa)
            ket += MC_SA_answer_text(debai, dap, nhieu, _ms_giai(qs, chuan, n, loai), 0, 0, tham)
        except _MsLai:
            continue
    return ket


# ---------- các hàm công khai (mỗi hàm = một biến thể; ID xem docs/04) ----------

def L10_C3_B5_NB029_MC_I_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (NB029, A): tam giác nhọn, xét dấu sin, côsin, tang, côtang của một góc - Xét dấu sin, côsin, tang, côtang của một góc trong tam giác nhọn hoặc tam giác có góc A tù (chọn khẳng định đúng / sai)"""
    return _ms_sinh("MC", "NB029", "A", 1, socau, dang)


def L10_C3_B5_NB029_MC_I_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (NB029, A): tam giác có góc $A$ tù, xét dấu sin, côsin, tang, côtang của một góc - Xét dấu sin, côsin, tang, côtang của một góc trong tam giác nhọn hoặc tam giác có góc A tù (chọn khẳng định đúng / sai)"""
    return _ms_sinh("MC", "NB029", "A", 2, socau, dang)


def L10_C3_B5_TH031_MC_K_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH031, A): biết $\cos A$ - Biết một giá trị lượng giác của góc A: tính sin(B + C), cos(B + C), sin(180° − A) nhờ quan hệ hai góc bù nhau"""
    return _ms_sinh("MC", "TH031", "A", 1, socau, dang)


def L10_C3_B5_TH031_MC_K_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH031, A): biết $\sin A$ và góc $A$ nhọn / tù - Biết một giá trị lượng giác của góc A: tính sin(B + C), cos(B + C), sin(180° − A) nhờ quan hệ hai góc bù nhau"""
    return _ms_sinh("MC", "TH031", "A", 2, socau, dang)


def L10_C3_B5_TH031_MC_K_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH031, A): biết $\tan A$ - Biết một giá trị lượng giác của góc A: tính sin(B + C), cos(B + C), sin(180° − A) nhờ quan hệ hai góc bù nhau"""
    return _ms_sinh("MC", "TH031", "A", 3, socau, dang)


def L10_C3_B5_TH031_SA_K_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH031, A): biết $\cos A$ - Biết một giá trị lượng giác của góc A: tính sin(B + C), cos(B + C), sin(180° − A) nhờ quan hệ hai góc bù nhau"""
    return _ms_sinh("SA", "TH031", "A", 1, socau, dang)


def L10_C3_B5_TH031_SA_K_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH031, A): biết $\sin A$ và góc $A$ nhọn / tù - Biết một giá trị lượng giác của góc A: tính sin(B + C), cos(B + C), sin(180° − A) nhờ quan hệ hai góc bù nhau"""
    return _ms_sinh("SA", "TH031", "A", 2, socau, dang)


def L10_C3_B5_TH031_SA_K_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH031, A): biết $\tan A$ - Biết một giá trị lượng giác của góc A: tính sin(B + C), cos(B + C), sin(180° − A) nhờ quan hệ hai góc bù nhau"""
    return _ms_sinh("SA", "TH031", "A", 3, socau, dang)


def L10_C3_B5_TH031_MC_L_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH031, B): biết $\widehat A$ và $\widehat B$ - Biết hai góc: tính sin, côsin của tổng hai góc (bù với góc thứ ba) bằng máy tính cầm tay"""
    return _ms_sinh("MC", "TH031", "B", 1, socau, dang)


def L10_C3_B5_TH031_MC_L_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH031, B): biết $\widehat B$ và $\widehat C$ - Biết hai góc: tính sin, côsin của tổng hai góc (bù với góc thứ ba) bằng máy tính cầm tay"""
    return _ms_sinh("MC", "TH031", "B", 2, socau, dang)


def L10_C3_B5_TH031_MC_L_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH031, B): biết $\widehat A$ và $\widehat C$ - Biết hai góc: tính sin, côsin của tổng hai góc (bù với góc thứ ba) bằng máy tính cầm tay"""
    return _ms_sinh("MC", "TH031", "B", 3, socau, dang)


def L10_C3_B5_TH031_SA_L_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH031, B): biết $\widehat A$ và $\widehat B$ - Biết hai góc: tính sin, côsin của tổng hai góc (bù với góc thứ ba) bằng máy tính cầm tay"""
    return _ms_sinh("SA", "TH031", "B", 1, socau, dang)


def L10_C3_B5_TH031_SA_L_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH031, B): biết $\widehat B$ và $\widehat C$ - Biết hai góc: tính sin, côsin của tổng hai góc (bù với góc thứ ba) bằng máy tính cầm tay"""
    return _ms_sinh("SA", "TH031", "B", 2, socau, dang)


def L10_C3_B5_TH031_SA_L_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH031, B): biết $\widehat A$ và $\widehat C$ - Biết hai góc: tính sin, côsin của tổng hai góc (bù với góc thứ ba) bằng máy tính cầm tay"""
    return _ms_sinh("SA", "TH031", "B", 3, socau, dang)


def L10_C3_B5_TH030_MC_H_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, A): biết $\cos A$ - Biết một giá trị lượng giác của góc A: tính giá trị lượng giác còn lại (sin² + cos² = 1, tan = sin/cos)"""
    return _ms_sinh("MC", "TH030", "A", 1, socau, dang)


def L10_C3_B5_TH030_MC_H_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, A): biết $\sin A$ và góc $A$ nhọn / tù - Biết một giá trị lượng giác của góc A: tính giá trị lượng giác còn lại (sin² + cos² = 1, tan = sin/cos)"""
    return _ms_sinh("MC", "TH030", "A", 2, socau, dang)


def L10_C3_B5_TH030_MC_H_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, A): biết $\tan A$ - Biết một giá trị lượng giác của góc A: tính giá trị lượng giác còn lại (sin² + cos² = 1, tan = sin/cos)"""
    return _ms_sinh("MC", "TH030", "A", 3, socau, dang)


def L10_C3_B5_TH030_SA_H_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, A): biết $\cos A$ - Biết một giá trị lượng giác của góc A: tính giá trị lượng giác còn lại (sin² + cos² = 1, tan = sin/cos)"""
    return _ms_sinh("SA", "TH030", "A", 1, socau, dang)


def L10_C3_B5_TH030_SA_H_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, A): biết $\sin A$ và góc $A$ nhọn / tù - Biết một giá trị lượng giác của góc A: tính giá trị lượng giác còn lại (sin² + cos² = 1, tan = sin/cos)"""
    return _ms_sinh("SA", "TH030", "A", 2, socau, dang)


def L10_C3_B5_TH030_SA_H_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, A): biết $\tan A$ - Biết một giá trị lượng giác của góc A: tính giá trị lượng giác còn lại (sin² + cos² = 1, tan = sin/cos)"""
    return _ms_sinh("SA", "TH030", "A", 3, socau, dang)


def L10_C3_B5_TH030_MC_I_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, B): biết $\widehat A$ và $\widehat B$ - Biết hai góc: tính sin, côsin của góc thứ ba bằng máy tính cầm tay"""
    return _ms_sinh("MC", "TH030", "B", 1, socau, dang)


def L10_C3_B5_TH030_MC_I_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, B): biết $\widehat B$ và $\widehat C$ - Biết hai góc: tính sin, côsin của góc thứ ba bằng máy tính cầm tay"""
    return _ms_sinh("MC", "TH030", "B", 2, socau, dang)


def L10_C3_B5_TH030_MC_I_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, B): biết $\widehat A$ và $\widehat C$ - Biết hai góc: tính sin, côsin của góc thứ ba bằng máy tính cầm tay"""
    return _ms_sinh("MC", "TH030", "B", 3, socau, dang)


def L10_C3_B5_TH030_SA_I_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, B): biết $\widehat A$ và $\widehat B$ - Biết hai góc: tính sin, côsin của góc thứ ba bằng máy tính cầm tay"""
    return _ms_sinh("SA", "TH030", "B", 1, socau, dang)


def L10_C3_B5_TH030_SA_I_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, B): biết $\widehat B$ và $\widehat C$ - Biết hai góc: tính sin, côsin của góc thứ ba bằng máy tính cầm tay"""
    return _ms_sinh("SA", "TH030", "B", 2, socau, dang)


def L10_C3_B5_TH030_SA_I_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, B): biết $\widehat A$ và $\widehat C$ - Biết hai góc: tính sin, côsin của góc thứ ba bằng máy tính cầm tay"""
    return _ms_sinh("SA", "TH030", "B", 3, socau, dang)


def L10_C3_B5_TH030_MC_J_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\cos\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("MC", "TH030", "G", 1, socau, dang)


def L10_C3_B5_TH030_MC_J_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\tan\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("MC", "TH030", "G", 2, socau, dang)


def L10_C3_B5_TH030_MC_J_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\cot\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("MC", "TH030", "G", 3, socau, dang)


def L10_C3_B5_TH030_SA_J_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\cos\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("SA", "TH030", "G", 1, socau, dang)


def L10_C3_B5_TH030_SA_J_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\tan\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("SA", "TH030", "G", 2, socau, dang)


def L10_C3_B5_TH030_SA_J_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\cot\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("SA", "TH030", "G", 3, socau, dang)


def L10_C3_B5_TH030_TL_B_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\cos\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("TL", "TH030", "G", 1, socau, dong)


def L10_C3_B5_TH030_TL_B_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\tan\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("TL", "TH030", "G", 2, socau, dong)


def L10_C3_B5_TH030_TL_B_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, G): biết $\sin\alpha$ và khoảng của $\alpha$, tìm $\cot\alpha$ - Biết sin của góc α và khoảng của α: tìm MỘT giá trị lượng giác khác (cos, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("TL", "TH030", "G", 3, socau, dong)


def L10_C3_B5_TH030_MC_K_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\sin\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("MC", "TH030", "H", 1, socau, dang)


def L10_C3_B5_TH030_MC_K_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\tan\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("MC", "TH030", "H", 2, socau, dang)


def L10_C3_B5_TH030_MC_K_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\cot\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("MC", "TH030", "H", 3, socau, dang)


def L10_C3_B5_TH030_SA_K_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\sin\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("SA", "TH030", "H", 1, socau, dang)


def L10_C3_B5_TH030_SA_K_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\tan\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("SA", "TH030", "H", 2, socau, dang)


def L10_C3_B5_TH030_SA_K_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\cot\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("SA", "TH030", "H", 3, socau, dang)


def L10_C3_B5_TH030_TL_C_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\sin\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("TL", "TH030", "H", 1, socau, dong)


def L10_C3_B5_TH030_TL_C_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\tan\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("TL", "TH030", "H", 2, socau, dong)


def L10_C3_B5_TH030_TL_C_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, H): biết $\cos\alpha$, tìm $\cot\alpha$ - Biết cos của góc α: tìm MỘT giá trị lượng giác khác (sin, tan hoặc cot) bằng sin² + cos² = 1, tan = sin/cos"""
    return _ms_sinh("TL", "TH030", "H", 3, socau, dong)


def L10_C3_B5_TH030_MC_L_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\cot\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("MC", "TH030", "I", 1, socau, dang)


def L10_C3_B5_TH030_MC_L_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\cos\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("MC", "TH030", "I", 2, socau, dang)


def L10_C3_B5_TH030_MC_L_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\sin\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("MC", "TH030", "I", 3, socau, dang)


def L10_C3_B5_TH030_SA_L_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\cot\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("SA", "TH030", "I", 1, socau, dang)


def L10_C3_B5_TH030_SA_L_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\cos\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("SA", "TH030", "I", 2, socau, dang)


def L10_C3_B5_TH030_SA_L_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\sin\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("SA", "TH030", "I", 3, socau, dang)


def L10_C3_B5_TH030_TL_D_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\cot\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("TL", "TH030", "I", 1, socau, dong)


def L10_C3_B5_TH030_TL_D_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\cos\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("TL", "TH030", "I", 2, socau, dong)


def L10_C3_B5_TH030_TL_D_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, I): biết $\tan\alpha$, tìm $\sin\alpha$ - Biết tan của góc α: tìm MỘT giá trị lượng giác khác (cot, cos hoặc sin) bằng tan.cot = 1, 1 + tan² = 1/cos²"""
    return _ms_sinh("TL", "TH030", "I", 3, socau, dong)


def L10_C3_B5_TH030_MC_M_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\tan\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("MC", "TH030", "J", 1, socau, dang)


def L10_C3_B5_TH030_MC_M_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\sin\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("MC", "TH030", "J", 2, socau, dang)


def L10_C3_B5_TH030_MC_M_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\cos\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("MC", "TH030", "J", 3, socau, dang)


def L10_C3_B5_TH030_SA_M_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\tan\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("SA", "TH030", "J", 1, socau, dang)


def L10_C3_B5_TH030_SA_M_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\sin\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("SA", "TH030", "J", 2, socau, dang)


def L10_C3_B5_TH030_SA_M_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\cos\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("SA", "TH030", "J", 3, socau, dang)


def L10_C3_B5_TH030_TL_E_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\tan\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("TL", "TH030", "J", 1, socau, dong)


def L10_C3_B5_TH030_TL_E_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\sin\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("TL", "TH030", "J", 2, socau, dong)


def L10_C3_B5_TH030_TL_E_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH030, J): biết $\cot\alpha$, tìm $\cos\alpha$ - Biết cot của góc α: tìm MỘT giá trị lượng giác khác (tan, sin hoặc cos) bằng tan.cot = 1, 1 + cot² = 1/sin²"""
    return _ms_sinh("TL", "TH030", "J", 3, socau, dong)


def L10_C3_B6_TH032_MC_K_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("MC", "TH032", "A", 1, socau, dang)


def L10_C3_B6_TH032_MC_K_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("MC", "TH032", "A", 2, socau, dang)


def L10_C3_B6_TH032_MC_K_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("MC", "TH032", "A", 3, socau, dang)


def L10_C3_B6_TH032_SA_K_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("SA", "TH032", "A", 1, socau, dang)


def L10_C3_B6_TH032_SA_K_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("SA", "TH032", "A", 2, socau, dang)


def L10_C3_B6_TH032_SA_K_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("SA", "TH032", "A", 3, socau, dang)


def L10_C3_B6_TH032_TL_C_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("TL", "TH032", "A", 1, socau, dong)


def L10_C3_B6_TH032_TL_C_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("TL", "TH032", "A", 2, socau, dong)


def L10_C3_B6_TH032_TL_C_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính cạnh thứ ba bằng định lí côsin (tự luận: rồi tính côsin một góc)"""
    return _ms_sinh("TL", "TH032", "A", 3, socau, dong)


def L10_C3_B6_TH032_MC_L_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("MC", "TH032", "C", 1, socau, dang)


def L10_C3_B6_TH032_MC_L_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("MC", "TH032", "C", 2, socau, dang)


def L10_C3_B6_TH032_MC_L_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("MC", "TH032", "C", 3, socau, dang)


def L10_C3_B6_TH032_SA_L_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("SA", "TH032", "C", 1, socau, dang)


def L10_C3_B6_TH032_SA_L_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("SA", "TH032", "C", 2, socau, dang)


def L10_C3_B6_TH032_SA_L_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("SA", "TH032", "C", 3, socau, dang)


def L10_C3_B6_TH032_TL_D_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("TL", "TH032", "C", 1, socau, dong)


def L10_C3_B6_TH032_TL_D_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("TL", "TH032", "C", 2, socau, dong)


def L10_C3_B6_TH032_TL_D_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: tính côsin của một góc bằng hệ quả của định lí côsin"""
    return _ms_sinh("TL", "TH032", "C", 3, socau, dong)


def L10_C3_B6_TH032_MC_M_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, D): biết $BC$, $\cos B$ và đường cao $AH$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh còn lại bằng định lí côsin"""
    return _ms_sinh("MC", "TH032", "D", 1, socau, dang)


def L10_C3_B6_TH032_MC_M_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, D): biết $AB$, $\cos B$ và đường cao $CK$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh còn lại bằng định lí côsin"""
    return _ms_sinh("MC", "TH032", "D", 2, socau, dang)


def L10_C3_B6_TH032_SA_M_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, D): biết $BC$, $\cos B$ và đường cao $AH$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh còn lại bằng định lí côsin"""
    return _ms_sinh("SA", "TH032", "D", 1, socau, dang)


def L10_C3_B6_TH032_SA_M_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, D): biết $AB$, $\cos B$ và đường cao $CK$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh còn lại bằng định lí côsin"""
    return _ms_sinh("SA", "TH032", "D", 2, socau, dang)


def L10_C3_B6_TH032_TL_E_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, D): biết $BC$, $\cos B$ và đường cao $AH$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh còn lại bằng định lí côsin"""
    return _ms_sinh("TL", "TH032", "D", 1, socau, dong)


def L10_C3_B6_TH032_TL_E_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH032, D): biết $AB$, $\cos B$ và đường cao $CK$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh còn lại bằng định lí côsin"""
    return _ms_sinh("TL", "TH032", "D", 2, socau, dong)


def L10_C3_B6_TH032_MC_N_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, E): biết $BC$, $AB$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh còn lại bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("MC", "TH032", "E", 1, socau, dang)


def L10_C3_B6_TH032_MC_N_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, E): biết $BC$, $AC$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh còn lại bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("MC", "TH032", "E", 2, socau, dang)


def L10_C3_B6_TH032_SA_N_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, E): biết $BC$, $AB$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh còn lại bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("SA", "TH032", "E", 1, socau, dang)


def L10_C3_B6_TH032_SA_N_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, E): biết $BC$, $AC$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh còn lại bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("SA", "TH032", "E", 2, socau, dang)


def L10_C3_B6_TH032_MC_O_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ABD$ - Biết ba cạnh và đường phân giác trong: tính độ dài đường phân giác bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("MC", "TH032", "F", 1, socau, dang)


def L10_C3_B6_TH032_MC_O_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ACD$ - Biết ba cạnh và đường phân giác trong: tính độ dài đường phân giác bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("MC", "TH032", "F", 2, socau, dang)


def L10_C3_B6_TH032_SA_O_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ABD$ - Biết ba cạnh và đường phân giác trong: tính độ dài đường phân giác bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("SA", "TH032", "F", 1, socau, dang)


def L10_C3_B6_TH032_SA_O_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ACD$ - Biết ba cạnh và đường phân giác trong: tính độ dài đường phân giác bằng định lí côsin - luyện tập thêm"""
    return _ms_sinh("SA", "TH032", "F", 2, socau, dang)


def L10_C3_B6_TH033_MC_F_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("MC", "TH033", "B", 1, socau, dang)


def L10_C3_B6_TH033_MC_F_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("MC", "TH033", "B", 2, socau, dang)


def L10_C3_B6_TH033_MC_F_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("MC", "TH033", "B", 3, socau, dang)


def L10_C3_B6_TH033_SA_F_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("SA", "TH033", "B", 1, socau, dang)


def L10_C3_B6_TH033_SA_F_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("SA", "TH033", "B", 2, socau, dang)


def L10_C3_B6_TH033_SA_F_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("SA", "TH033", "B", 3, socau, dang)


def L10_C3_B6_TH033_TL_C_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("TL", "TH033", "B", 1, socau, dong)


def L10_C3_B6_TH033_TL_C_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("TL", "TH033", "B", 2, socau, dong)


def L10_C3_B6_TH033_TL_C_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH033, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính hai cạnh còn lại bằng định lí sin"""
    return _ms_sinh("TL", "TH033", "B", 3, socau, dong)


def L10_C3_B6_TH033_MC_G_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("MC", "TH033", "C", 1, socau, dang)


def L10_C3_B6_TH033_MC_G_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("MC", "TH033", "C", 2, socau, dang)


def L10_C3_B6_TH033_MC_G_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("MC", "TH033", "C", 3, socau, dang)


def L10_C3_B6_TH033_SA_G_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("SA", "TH033", "C", 1, socau, dang)


def L10_C3_B6_TH033_SA_G_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("SA", "TH033", "C", 2, socau, dang)


def L10_C3_B6_TH033_SA_G_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("SA", "TH033", "C", 3, socau, dang)


def L10_C3_B6_TH033_TL_D_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("TL", "TH033", "C", 1, socau, dong)


def L10_C3_B6_TH033_TL_D_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("TL", "TH033", "C", 2, socau, dong)


def L10_C3_B6_TH033_TL_D_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH033, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: tính bán kính đường tròn ngoại tiếp bằng định lí sin"""
    return _ms_sinh("TL", "TH033", "C", 3, socau, dong)


def L10_C3_B6_TH034_MC_K_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("MC", "TH034", "A", 1, socau, dang)


def L10_C3_B6_TH034_MC_K_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("MC", "TH034", "A", 2, socau, dang)


def L10_C3_B6_TH034_MC_K_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("MC", "TH034", "A", 3, socau, dang)


def L10_C3_B6_TH034_SA_K_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("SA", "TH034", "A", 1, socau, dang)


def L10_C3_B6_TH034_SA_K_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("SA", "TH034", "A", 2, socau, dang)


def L10_C3_B6_TH034_SA_K_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("SA", "TH034", "A", 3, socau, dang)


def L10_C3_B6_TH034_TL_C_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("TL", "TH034", "A", 1, socau, dong)


def L10_C3_B6_TH034_TL_C_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("TL", "TH034", "A", 2, socau, dong)


def L10_C3_B6_TH034_TL_C_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH034, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: tính diện tích tam giác (S = 1/2.b.c.sin A)"""
    return _ms_sinh("TL", "TH034", "A", 3, socau, dong)


def L10_C3_B6_TH034_MC_L_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính diện tích tam giác"""
    return _ms_sinh("MC", "TH034", "B", 1, socau, dang)


def L10_C3_B6_TH034_MC_L_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: tính diện tích tam giác"""
    return _ms_sinh("MC", "TH034", "B", 2, socau, dang)


def L10_C3_B6_TH034_MC_L_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính diện tích tam giác"""
    return _ms_sinh("MC", "TH034", "B", 3, socau, dang)


def L10_C3_B6_TH034_SA_L_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính diện tích tam giác"""
    return _ms_sinh("SA", "TH034", "B", 1, socau, dang)


def L10_C3_B6_TH034_SA_L_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: tính diện tích tam giác"""
    return _ms_sinh("SA", "TH034", "B", 2, socau, dang)


def L10_C3_B6_TH034_SA_L_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: tính diện tích tam giác"""
    return _ms_sinh("SA", "TH034", "B", 3, socau, dang)


def L10_C3_B6_TH034_MC_M_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("MC", "TH034", "C", 1, socau, dang)


def L10_C3_B6_TH034_MC_M_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("MC", "TH034", "C", 2, socau, dang)


def L10_C3_B6_TH034_MC_M_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("MC", "TH034", "C", 3, socau, dang)


def L10_C3_B6_TH034_SA_M_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("SA", "TH034", "C", 1, socau, dang)


def L10_C3_B6_TH034_SA_M_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("SA", "TH034", "C", 2, socau, dang)


def L10_C3_B6_TH034_SA_M_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("SA", "TH034", "C", 3, socau, dang)


def L10_C3_B6_TH034_TL_D_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("TL", "TH034", "C", 1, socau, dong)


def L10_C3_B6_TH034_TL_D_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("TL", "TH034", "C", 2, socau, dong)


def L10_C3_B6_TH034_TL_D_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH034, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: nửa chu vi, công thức Heron, bán kính đường tròn nội tiếp, đường cao"""
    return _ms_sinh("TL", "TH034", "C", 3, socau, dong)


def L10_C3_B6_TH034_MC_N_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, D): biết $BC$ và đường cao $AH$ - Biết một cạnh và đường cao tương ứng: tính diện tích tam giác (S = 1/2.a.h_a)"""
    return _ms_sinh("MC", "TH034", "D", 1, socau, dang)


def L10_C3_B6_TH034_MC_N_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH034, D): biết $AB$ và đường cao $CK$ - Biết một cạnh và đường cao tương ứng: tính diện tích tam giác (S = 1/2.a.h_a)"""
    return _ms_sinh("MC", "TH034", "D", 2, socau, dang)


def L10_C3_B6_TH034_SA_N_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, D): biết $BC$ và đường cao $AH$ - Biết một cạnh và đường cao tương ứng: tính diện tích tam giác (S = 1/2.a.h_a)"""
    return _ms_sinh("SA", "TH034", "D", 1, socau, dang)


def L10_C3_B6_TH034_SA_N_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH034, D): biết $AB$ và đường cao $CK$ - Biết một cạnh và đường cao tương ứng: tính diện tích tam giác (S = 1/2.a.h_a)"""
    return _ms_sinh("SA", "TH034", "D", 2, socau, dang)


def L10_C3_B6_TH035_MC_A_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$ và $\cos A$ - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("MC", "TH035", "A", 1, socau, dang)


def L10_C3_B6_TH035_MC_A_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("MC", "TH035", "A", 2, socau, dang)


def L10_C3_B6_TH035_MC_A_04(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$ và $\tan A$ - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("MC", "TH035", "A", 3, socau, dang)


def L10_C3_B6_TH035_SA_A_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$ và $\cos A$ - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("SA", "TH035", "A", 1, socau, dang)


def L10_C3_B6_TH035_SA_A_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("SA", "TH035", "A", 2, socau, dang)


def L10_C3_B6_TH035_SA_A_04(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$ và $\tan A$ - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("SA", "TH035", "A", 3, socau, dang)


def L10_C3_B6_TH035_TL_B_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$ và $\cos A$ - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("TL", "TH035", "A", 1, socau, dong)


def L10_C3_B6_TH035_TL_B_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("TL", "TH035", "A", 2, socau, dong)


def L10_C3_B6_TH035_TL_B_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, A): biết $AB$, $AC$ và $\tan A$ - Giải tam giác biết hai cạnh và một giá trị lượng giác của góc A: cạnh thứ ba và số đo góc còn lại"""
    return _ms_sinh("TL", "TH035", "A", 3, socau, dong)


def L10_C3_B6_TH035_MC_B_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("MC", "TH035", "B", 1, socau, dang)


def L10_C3_B6_TH035_MC_B_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("MC", "TH035", "B", 2, socau, dang)


def L10_C3_B6_TH035_MC_B_04(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("MC", "TH035", "B", 3, socau, dang)


def L10_C3_B6_TH035_SA_B_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("SA", "TH035", "B", 1, socau, dang)


def L10_C3_B6_TH035_SA_B_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("SA", "TH035", "B", 2, socau, dang)


def L10_C3_B6_TH035_SA_B_04(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("SA", "TH035", "B", 3, socau, dang)


def L10_C3_B6_TH035_TL_A_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("TL", "TH035", "B", 1, socau, dong)


def L10_C3_B6_TH035_TL_A_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("TL", "TH035", "B", 2, socau, dong)


def L10_C3_B6_TH035_TL_A_04(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Giải tam giác biết hai góc và một cạnh: góc thứ ba, hai cạnh còn lại, chu vi"""
    return _ms_sinh("TL", "TH035", "B", 3, socau, dong)


def L10_C3_B6_TH035_MC_F_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $A$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("MC", "TH035", "C", 1, socau, dang)


def L10_C3_B6_TH035_MC_F_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $B$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("MC", "TH035", "C", 2, socau, dang)


def L10_C3_B6_TH035_MC_F_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $C$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("MC", "TH035", "C", 3, socau, dang)


def L10_C3_B6_TH035_SA_F_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $A$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("SA", "TH035", "C", 1, socau, dang)


def L10_C3_B6_TH035_SA_F_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $B$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("SA", "TH035", "C", 2, socau, dang)


def L10_C3_B6_TH035_SA_F_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $C$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("SA", "TH035", "C", 3, socau, dang)


def L10_C3_B6_TH035_TL_C_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $A$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("TL", "TH035", "C", 1, socau, dong)


def L10_C3_B6_TH035_TL_C_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $B$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("TL", "TH035", "C", 2, socau, dong)


def L10_C3_B6_TH035_TL_C_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (TH035, C): biết ba cạnh, hỏi theo đỉnh $C$ - Giải tam giác biết ba cạnh: số đo các góc (hệ quả của định lí côsin)"""
    return _ms_sinh("TL", "TH035", "C", 3, socau, dong)


def L10_C3_B6_VD032_MC_B_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("MC", "VD032", "A", 1, socau, dang)


def L10_C3_B6_VD032_MC_B_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("MC", "VD032", "A", 2, socau, dang)


def L10_C3_B6_VD032_MC_B_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("MC", "VD032", "A", 3, socau, dang)


def L10_C3_B6_VD032_SA_B_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("SA", "VD032", "A", 1, socau, dang)


def L10_C3_B6_VD032_SA_B_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("SA", "VD032", "A", 2, socau, dang)


def L10_C3_B6_VD032_SA_B_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("SA", "VD032", "A", 3, socau, dang)


def L10_C3_B6_VD032_TL_A_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$ và $\cos A$ - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("TL", "VD032", "A", 1, socau, dong)


def L10_C3_B6_VD032_TL_A_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$, $\sin A$ và góc $A$ nhọn / tù - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("TL", "VD032", "A", 2, socau, dong)


def L10_C3_B6_VD032_TL_A_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, A): biết $AB$, $AC$ và $\tan A$ - Biết hai cạnh và một giá trị lượng giác của góc A: kết hợp định lí côsin với định lí sin, công thức diện tích (R, h_a)"""
    return _ms_sinh("TL", "VD032", "A", 3, socau, dong)


def L10_C3_B6_VD032_MC_C_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("MC", "VD032", "B", 1, socau, dang)


def L10_C3_B6_VD032_MC_C_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("MC", "VD032", "B", 2, socau, dang)


def L10_C3_B6_VD032_MC_C_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("MC", "VD032", "B", 3, socau, dang)


def L10_C3_B6_VD032_SA_C_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("SA", "VD032", "B", 1, socau, dang)


def L10_C3_B6_VD032_SA_C_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("SA", "VD032", "B", 2, socau, dang)


def L10_C3_B6_VD032_SA_C_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("SA", "VD032", "B", 3, socau, dang)


def L10_C3_B6_VD032_TL_B_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat A$, $\widehat B$ và $BC$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("TL", "VD032", "B", 1, socau, dong)


def L10_C3_B6_VD032_TL_B_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat B$, $\widehat C$ và $BC$ (cạnh kẹp giữa hai góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("TL", "VD032", "B", 2, socau, dong)


def L10_C3_B6_VD032_TL_B_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, B): biết $\widehat A$, $\widehat C$ và $AB$ (hai góc và cạnh đối của một góc) - Biết hai góc và một cạnh: kết hợp định lí sin với công thức diện tích (S, đường cao)"""
    return _ms_sinh("TL", "VD032", "B", 3, socau, dong)


def L10_C3_B6_VD032_MC_D_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("MC", "VD032", "C", 1, socau, dang)


def L10_C3_B6_VD032_MC_D_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("MC", "VD032", "C", 2, socau, dang)


def L10_C3_B6_VD032_MC_D_03(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("MC", "VD032", "C", 3, socau, dang)


def L10_C3_B6_VD032_SA_D_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("SA", "VD032", "C", 1, socau, dang)


def L10_C3_B6_VD032_SA_D_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("SA", "VD032", "C", 2, socau, dang)


def L10_C3_B6_VD032_SA_D_03(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("SA", "VD032", "C", 3, socau, dang)


def L10_C3_B6_VD032_TL_C_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $A$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("TL", "VD032", "C", 1, socau, dong)


def L10_C3_B6_VD032_TL_C_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $B$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("TL", "VD032", "C", 2, socau, dong)


def L10_C3_B6_VD032_TL_C_03(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, C): biết ba cạnh, hỏi theo đỉnh $C$ - Biết ba cạnh: kết hợp hệ quả định lí côsin, Heron, định lí sin (đường cao, r, R)"""
    return _ms_sinh("TL", "VD032", "C", 3, socau, dong)


def L10_C3_B6_VD032_MC_E_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, D): biết $BC$, $\cos B$ và đường cao $AH$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh rồi côsin góc còn lại hoặc R"""
    return _ms_sinh("MC", "VD032", "D", 1, socau, dang)


def L10_C3_B6_VD032_MC_E_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, D): biết $AB$, $\cos B$ và đường cao $CK$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh rồi côsin góc còn lại hoặc R"""
    return _ms_sinh("MC", "VD032", "D", 2, socau, dang)


def L10_C3_B6_VD032_SA_E_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, D): biết $BC$, $\cos B$ và đường cao $AH$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh rồi côsin góc còn lại hoặc R"""
    return _ms_sinh("SA", "VD032", "D", 1, socau, dang)


def L10_C3_B6_VD032_SA_E_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, D): biết $AB$, $\cos B$ và đường cao $CK$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh rồi côsin góc còn lại hoặc R"""
    return _ms_sinh("SA", "VD032", "D", 2, socau, dang)


def L10_C3_B6_VD032_TL_D_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, D): biết $BC$, $\cos B$ và đường cao $AH$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh rồi côsin góc còn lại hoặc R"""
    return _ms_sinh("TL", "VD032", "D", 1, socau, dong)


def L10_C3_B6_VD032_TL_D_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, D): biết $AB$, $\cos B$ và đường cao $CK$ - Biết một cạnh, côsin góc B và một đường cao: tính cạnh rồi côsin góc còn lại hoặc R"""
    return _ms_sinh("TL", "VD032", "D", 2, socau, dong)


def L10_C3_B6_VD032_MC_F_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, E): biết $BC$, $AB$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh rồi côsin góc A, R hoặc diện tích - luyện tập thêm"""
    return _ms_sinh("MC", "VD032", "E", 1, socau, dang)


def L10_C3_B6_VD032_MC_F_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, E): biết $BC$, $AC$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh rồi côsin góc A, R hoặc diện tích - luyện tập thêm"""
    return _ms_sinh("MC", "VD032", "E", 2, socau, dang)


def L10_C3_B6_VD032_SA_F_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, E): biết $BC$, $AB$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh rồi côsin góc A, R hoặc diện tích - luyện tập thêm"""
    return _ms_sinh("SA", "VD032", "E", 1, socau, dang)


def L10_C3_B6_VD032_SA_F_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, E): biết $BC$, $AC$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh rồi côsin góc A, R hoặc diện tích - luyện tập thêm"""
    return _ms_sinh("SA", "VD032", "E", 2, socau, dang)


def L10_C3_B6_VD032_TL_E_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, E): biết $BC$, $AB$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh rồi côsin góc A, R hoặc diện tích - luyện tập thêm"""
    return _ms_sinh("TL", "VD032", "E", 1, socau, dong)


def L10_C3_B6_VD032_TL_E_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, E): biết $BC$, $AC$ và trung tuyến $AM$ - Biết hai cạnh và đường trung tuyến: tính cạnh rồi côsin góc A, R hoặc diện tích - luyện tập thêm"""
    return _ms_sinh("TL", "VD032", "E", 2, socau, dong)


def L10_C3_B6_VD032_MC_G_01(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ABD$ - Biết ba cạnh và đường phân giác trong: tính BD hoặc DC rồi diện tích tam giác ABD hoặc ACD - luyện tập thêm"""
    return _ms_sinh("MC", "VD032", "F", 1, socau, dang)


def L10_C3_B6_VD032_MC_G_02(socau, dang=1):
    r"""MC/SA/TL giải tam giác (VD032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ACD$ - Biết ba cạnh và đường phân giác trong: tính BD hoặc DC rồi diện tích tam giác ABD hoặc ACD - luyện tập thêm"""
    return _ms_sinh("MC", "VD032", "F", 2, socau, dang)


def L10_C3_B6_VD032_SA_G_01(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ABD$ - Biết ba cạnh và đường phân giác trong: tính BD hoặc DC rồi diện tích tam giác ABD hoặc ACD - luyện tập thêm"""
    return _ms_sinh("SA", "VD032", "F", 1, socau, dang)


def L10_C3_B6_VD032_SA_G_02(socau, dang=2):
    r"""MC/SA/TL giải tam giác (VD032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ACD$ - Biết ba cạnh và đường phân giác trong: tính BD hoặc DC rồi diện tích tam giác ABD hoặc ACD - luyện tập thêm"""
    return _ms_sinh("SA", "VD032", "F", 2, socau, dang)


def L10_C3_B6_VD032_TL_F_01(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ABD$ - Biết ba cạnh và đường phân giác trong: tính BD hoặc DC rồi diện tích tam giác ABD hoặc ACD - luyện tập thêm"""
    return _ms_sinh("TL", "VD032", "F", 1, socau, dong)


def L10_C3_B6_VD032_TL_F_02(socau, dong=1):
    r"""MC/SA/TL giải tam giác (VD032, F): biết ba cạnh và phân giác $AD$, tính qua tam giác $ACD$ - Biết ba cạnh và đường phân giác trong: tính BD hoặc DC rồi diện tích tam giác ABD hoặc ACD - luyện tập thêm"""
    return _ms_sinh("TL", "VD032", "F", 2, socau, dong)

# ===== MS_END =====


# =====================================================================
# BỔ SUNG 15/10/2026 (cô Lan: "ghép các dạng đã thấy giống, cùng dạng; các dạng thiếu làm bổ sung luôn")
# Bản TRẢ LỜI NGẮN (SA) / TRẮC NGHIỆM (MC) cùng chữ, cùng "Dang" với câu đã có trong Mapping.
#  - MC "chọn khẳng định đúng/sai" -> SA "có bao nhiêu khẳng định đúng (sai)"; chân trị của mọi khẳng định do
#    Python TÍNH (sympy chính xác hoặc thử số trên tam giác ngẫu nhiên), không gõ tay.
#  - Đáp số trả lời ngắn là số nguyên hoặc số thập phân (dấu phẩy), làm tròn theo đề nói rõ.
# CLAUDE THEM 15/10/2026 - co Lan duyet lai.
# =====================================================================
from fractions import Fraction as _Fr3


def _chon_bon_kd(dung_ds, sai_ds):
    """Chọn bốn mục (số mục đúng t trong {1; 2; 3}); mỗi mục (tex, lí do) hoặc (tex, lí do, khoá): hai mục cùng khoá
    (vd cùng vế trái, cùng biểu thức xét dấu) không cùng xuất hiện, để khẳng định này không làm lộ khẳng định kia."""
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


def _c3s_dem(mo, dung_ds, sai_ds, dang, hinh=0, giai_mo="", hoi_rieng=None, ten_kd="statements"):
    r"""Câu ĐẾM: bốn mục lấy từ dung_ds / sai_ds ([(tex, lí do)]), số mục đúng trong {1; 2; 3}.
    hoi_rieng: (câu hỏi, chữ cho mục đúng, chữ cho mục sai) khi chỉ hỏi một chiều (vd ``có thể xảy ra'');
    mặc định hỏi ngẫu nhiên số khẳng định đúng hoặc sai."""
    ds = _chon_bon_kd(dung_ds, sai_ds)
    t = sum(1 for _, d in ds if d)
    if hoi_rieng:
        ket = hoi_rieng[0]
        dap = t
        chu = lambda d: hoi_rieng[1] if d else hoi_rieng[2]
    else:
        hoi_dung = random.random() < 0.6
        dap = t if hoi_dung else 4 - t
        tu = r"\textbf{true}" if hoi_dung else r"\textbf{false}"
        ket = r"Among the following %s, how many %s are %s?" % (ten_kd, ten_kd, tu)
        chu = lambda d: "true" if d else "false"
    debai = (mo + " " if mo else "") + ket + r"\\ " + r"\\ ".join("%d. %s" % (i + 1, x[0]) for i, (x, _) in enumerate(ds))
    giai = giai_mo + r"\\ ".join(r"%d. %s is %s because %s." % (i + 1, x[0], chu(d), x[1]) for i, (x, d) in enumerate(ds))
    giai += r"\\ So the answer is $%d$." % dap
    nhieu = [str(x) for x in (4 - dap, dap + 1, dap - 1, 0, 4, 1, 2, 3) if x != dap and 0 <= x <= 4]
    return MC_SA_answer_const(debai, str(dap), nhieu, giai, hinh, 0, dang)


def _c3s_tam_giac_so():
    """Một tam giác ngẫu nhiên (không vuông, không cân) dùng để THỬ chân trị các hệ thức: trả về dict a, b, c, A, B,
    C (radian), S, p, R, r, ha, hb, hc, ma, mb, mc."""
    while True:
        A, B = math.radians(random.uniform(20, 120)), math.radians(random.uniform(20, 120))
        C = math.pi - A - B
        if C < math.radians(15) or min(abs(A - B), abs(B - C), abs(A - C)) < 0.05 or \
                min(abs(x - math.pi / 2) for x in (A, B, C)) < 0.05:
            continue
        R = random.uniform(2, 6)
        a, b, c = 2 * R * math.sin(A), 2 * R * math.sin(B), 2 * R * math.sin(C)
        p = (a + b + c) / 2
        S = 0.5 * b * c * math.sin(A)
        return dict(a=a, b=b, c=c, A=A, B=B, C=C, S=S, p=p, R=R, r=S / p, ha=2 * S / a, hb=2 * S / b, hc=2 * S / c,
                    ma=math.sqrt((2 * b * b + 2 * c * c - a * a) / 4), mb=math.sqrt((2 * a * a + 2 * c * c - b * b) / 4),
                    mc=math.sqrt((2 * a * a + 2 * b * b - c * c) / 4))


def _c3s_dung(f, so=4):
    """f(T) -> (vế trái, vế phải); đúng nếu bằng nhau trên 'so' tam giác ngẫu nhiên."""
    for _ in range(so):
        T = _c3s_tam_giac_so()
        l, r = f(T)
        if abs(l - r) > 1e-7 * max(1.0, abs(l), abs(r)):
            return False
    return True


# ---------------------------------------------------------------------
# NB029 (Bài 5): giá trị lượng giác của góc từ 0 đến 180 độ
# ---------------------------------------------------------------------
def L10_C3_B5_NB029_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB029_MC_A (cùng Dang: giá trị lượng giác của góc đặc biệt): tính
    biểu thức gồm ba, bốn giá trị lượng giác HỮU TỈ của các góc đặc biệt; đáp số là số thập phân hữu hạn.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    HUU_TI = [(h, d) for d in (0, 30, 45, 60, 90, 120, 135, 150, 180) for h in ("sin", "cos", "tan", "cot")
              if _gtlg(h, d) is not None and _gtlg(h, d).is_Rational and _gtlg(h, d) != 0]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        hang = random.sample(HUU_TI, random.choice([3, 4]))
        he = [random.choice([1, 2, 3, 4, -1, -2, -3]) for _ in hang]
        key = list(zip(he, hang))
        tong = sum(k * _gtlg(h, d) for k, (h, d) in key)
        if _so_thap_phan_gon(tong) is None or key in gt:
            continue
        gt.append(key)
    cau = ""
    for key in gt:
        tong = sum(k * _gtlg(h, d) for k, (h, d) in key)
        bt, thay = "", ""
        for i, (k, (h, d)) in enumerate(key):
            dau = ("-" if k < 0 else "") if i == 0 else (" - " if k < 0 else " + ")
            so = "" if abs(k) == 1 else str(abs(k))
            bt += r"%s%s\%s %s" % (dau, so, h, _goc(d))
            v = _gtlg(h, d)
            thay += r"%s%s%s" % (dau, (so + r"\cdot ") if so else "", (r"\left(%s\right)" % _L(v)) if v < 0 else _L(v))
        sai1 = sum(k * abs(_gtlg(h, d)) for k, (h, d) in key)
        dap = _so_thap_phan_gon(tong)
        ung = [_so_thap_phan_gon(x) for x in (sai1, -tong, tong + 1, tong - 1, 2 * tong, tong + 2, tong - Rational(1, 2))]
        debai = r"Find the value of the expression $A = %s$." % bt
        giai = (r"Use the table of trigonometric values of special angles (for obtuse angles use the relation between supplementary angles):\\ $A = %s = %s$." % (thay, dap))
        cau += MC_SA_answer_const(debai, dap, [x for x in ung if x], giai, 0, 0, dang)
    return cau


_C3S_BO_PY = [(3, 4, 5), (7, 24, 25), (44, 117, 125), (4, 3, 5), (24, 7, 25), (117, 44, 125)]


def L10_C3_B5_NB029_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB029_MC_C (cùng Dang: tìm toạ độ điểm $M$ trên nửa đường tròn đơn vị
    khi biết giá trị lượng giác của góc $xOM$): cho $\sin$, $\cos$ (số thập phân), hỏi hoành độ hoặc tung độ của $M$.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(_C3S_BO_PY)
        w = (p, q, r, random.choice([1, -1]), random.choice(["x-coordinate", "y-coordinate"]))
        if w not in gt:
            gt.append(w)
        if len(gt) >= 24:
            break
    cau = ""
    for p, q, r, dau, hoi in gt:
        x, y = _Fr3(dau * p, r), _Fr3(q, r)
        sx, sy = _xx(float(x), 3), _xx(float(y), 3)
        dap, khac = (sx, sy) if hoi == "x-coordinate" else (sy, sx)
        debai = (r"In the coordinate plane $Oxy$, take a point $M$ on the unit semicircle such that $\sin\widehat{xOM} = %s$ and $\cos\widehat{xOM} = %s$. Find the %s of point $M$." % (sy, sx, hoi))
        giai = (r"A point $M\left(x_0; y_0\right)$ on the unit semicircle with $\widehat{xOM} = \alpha$ has $x_0 = \cos\alpha$, $y_0 = \sin\alpha$. So $M\left(%s; %s\right)$, and the %s of $M$ is $%s$."
                % (sx, sy, hoi, dap))
        ung = [khac, _xx(-float(x), 3), _xx(-float(y), 3), "1"]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


def _c3s_phan_so(p, q, am=False):
    return ("-" if am else "") + r"\dfrac{%d}{%d}" % (p, q)


def L10_C3_B5_NB029_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB029_MC_D (cùng Dang: giá trị lượng giác nào có thể xảy ra với
    $0^{\circ} \le \alpha \le 180^{\circ}$): bốn đẳng thức, đếm số đẳng thức CÓ THỂ xảy ra. Điều kiện:
    $0 \le \sin\alpha \le 1$, $-1 \le \cos\alpha \le 1$; $\tan\alpha$, $\cot\alpha$ nhận mọi giá trị thực (nên chỉ
    dùng $\tan$, $\cot$ cho đẳng thức có thể xảy ra, như lưu ý của NB029_MC_D).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for _l in range(6):
            p, q = _cap_nguyen_to_cung_nhau()
            n = random.randint(2, 5)
            dung += [(r"$\sin\alpha = %s$" % _c3s_phan_so(p, q), r"$0 \le %s \le 1$" % _c3s_phan_so(p, q)),
                     (r"$\cos\alpha = %s$" % _c3s_phan_so(p, q, True), r"$-1 \le %s \le 1$" % _c3s_phan_so(p, q, True)),
                     (r"$\cos\alpha = %s$" % _c3s_phan_so(p, q), r"$-1 \le %s \le 1$" % _c3s_phan_so(p, q)),
                     (r"$\tan\alpha = %d$" % random.choice([-n, n]), r"$\tan\alpha$ can take any real value"),
                     (r"$\cot\alpha = %s$" % _c3s_phan_so(q, p, random.random() < 0.5), r"$\cot\alpha$ can take any real value")]
            sai += [(r"$\sin\alpha = %s$" % _c3s_phan_so(p, q, True), r"$\sin\alpha \ge 0$ for every $\alpha$ from $0^{\circ}$ to $180^{\circ}$"),
                    (r"$\sin\alpha = %s$" % _c3s_phan_so(q, p), r"$\sin\alpha \le 1$ but $%s > 1$" % _c3s_phan_so(q, p)),
                    (r"$\cos\alpha = %s$" % _c3s_phan_so(q, p, random.random() < 0.5),
                     r"$-1 \le \cos\alpha \le 1$ but $\dfrac{%d}{%d} > 1$" % (q, p)),
                    (r"$%s\alpha = %d$" % (random.choice([r"\sin", r"\cos"]), random.choice([-n, n])),
                     r"both $\sin\alpha$ and $\cos\alpha$ have absolute value at most $1$")]
        mo = r"Given an angle $\alpha$ with $0^{\circ} \le \alpha \le 180^{\circ}$."
        cau += _c3s_dem(mo, dung, sai, dang, hoi_rieng=(r"How many of the following equalities \textbf{can} occur?", "possible", "impossible"),
                        giai_mo=r"For $0^{\circ} \le \alpha \le 180^{\circ}$: $0 \le \sin\alpha \le 1$, $-1 \le \cos\alpha \le 1$.\\ ")
    return cau


_C3S_DAU = [  # (tex biểu thức theo alpha, hàm số)
    (r"\sin\alpha", lambda t: math.sin(t)), (r"\cos\alpha", lambda t: math.cos(t)),
    (r"\tan\alpha", lambda t: math.tan(t)), (r"\cot\alpha", lambda t: 1 / math.tan(t)),
    (r"\sin\alpha\cdot\cos\alpha", lambda t: math.sin(t) * math.cos(t)),
    (r"\sin\alpha\cdot\tan\alpha", lambda t: math.sin(t) * math.tan(t)),
    (r"\dfrac{\cos\alpha}{\cot\alpha}", lambda t: math.cos(t) * math.tan(t)),
    (r"\dfrac{\sin\alpha}{\cot\alpha}", lambda t: math.sin(t) * math.tan(t)),
    (r"\tan\alpha\cdot\cot\alpha", lambda t: 1.0),
    (r"\cos\alpha\cdot\cot\alpha", lambda t: math.cos(t) / math.tan(t)),
]


def L10_C3_B5_NB029_SA_E_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB029_MC_E (cùng Dang: xét dấu giá trị lượng giác khi biết khoảng của
    góc): bốn khẳng định về dấu của một giá trị (hoặc tích, thương hai giá trị) lượng giác; đếm số khẳng định
    đúng (sai). Chân trị tính bằng số với một góc trong khoảng đã cho.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        tu = random.random() < 0.6
        lo, hi = (90, 180) if tu else (0, 90)
        thu = [math.radians(random.uniform(lo + 1, hi - 1)) for _ in range(3)]
        dung, sai = [], []
        for tex, f in _C3S_DAU:
            dau = 1 if f(thu[0]) > 0 else -1
            assert all((f(t) > 0) == (dau > 0) for t in thu)
            for d_kd in (">", "<"):
                ok = (d_kd == ">") == (dau > 0)
                (dung if ok else sai).append((r"$%s %s 0$" % (tex, d_kd),
                                              r"for $%d^{\circ} < \alpha < %d^{\circ}$, $%s$ is %s" % (
                                                  lo, hi, tex, "positive" if dau > 0 else "negative"), tex))
        mo = r"Given an angle $\alpha$ satisfying $%d^{\circ} < \alpha < %d^{\circ}$." % (lo, hi)
        giai_mo = (r"For $%d^{\circ} < \alpha < %d^{\circ}$: $\sin\alpha > 0$, $\cos\alpha %s 0$, $\tan\alpha %s 0$, $\cot\alpha %s 0$.\\ " % ((lo, hi) + (("<", "<", "<") if tu else (">", ">", ">"))))
        cau += _c3s_dem(mo, dung, sai, dang, giai_mo=giai_mo)
    return cau


def L10_C3_B5_NB029_SA_H_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB029_MC_H (cùng Dang: nhận ra giá trị lượng giác của góc đặc biệt):
    bốn đẳng thức về $\sin$, $\cos$, $\tan$, $\cot$ của cùng một góc đặc biệt; đếm số đẳng thức đúng (sai). Đẳng thức
    sai: sai dấu hoặc lấy nhầm giá trị của hàm khác (như MC_H). Giá trị tính bằng sympy.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        d = random.choice(_GOC_DB)
        dung, sai = [], []
        for h in _HAM4:
            v = _gtlg(h, d)
            w = _gtlg(_DOI_HAM[h], d)
            dung.append((r"$\%s %s = %s$" % (h, _goc(d), _L(v)), r"$\%s %s = %s$" % (h, _goc(d), _L(v))))
            for x in (-v, w, -w):
                if simplify(x - v) != 0:
                    sai.append((r"$\%s %s = %s$" % (h, _goc(d), _L(x)), r"$\%s %s = %s$" % (h, _goc(d), _L(v))))
        # mỗi hàm chỉ xuất hiện MỘT lần trong bốn đẳng thức
        t = random.choice([1, 2, 3])
        ham = list(_HAM4)
        random.shuffle(ham)
        chon_d = [x for x in dung if any(x[0].startswith(r"$\%s " % h) for h in ham[:t])]
        chon_s = []
        for h in ham[t:]:
            chon_s.append(random.choice([x for x in sai if x[0].startswith(r"$\%s " % h)]))
        cau += _c3s_dem("", chon_d, chon_s, dang, ten_kd="equalities",
                        giai_mo=r"Use the table of trigonometric values of special angles.\\ ")
    return cau


def L10_C3_B5_NB029_SA_I_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB029_MC_I (cùng Dang: dấu của $\sin$, $\cos$, $\tan$, $\cot$ của một góc
    trong tam giác nhọn hoặc tam giác có một góc tù): bốn khẳng định về dấu; đếm số khẳng định đúng (sai).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        tu = random.choice([None, "A", "B", "C"])
        goc = {X: (random.uniform(95, 140) if X == tu else random.uniform(10, 80)) for X in "ABC"}
        HAM = [(r"\sin", math.sin), (r"\cos", math.cos), (r"\tan", math.tan), (r"\cot", lambda t: 1 / math.tan(t))]
        dung, sai = [], []
        for X in "ABC":
            loai = "obtuse" if X == tu else "acute"
            for h, f in HAM:
                dau = f(math.radians(goc[X])) > 0
                for d_kd in (">", "<"):
                    ok = (d_kd == ">") == dau
                    (dung if ok else sai).append((r"$%s %s %s 0$" % (h, X, d_kd),
                                                  r"angle $%s$ is %s, so $%s %s %s 0$" % (X, loai, h, X, ">" if dau else "<"),
                                                  (h, X)))
        mo = (r"Given an acute triangle $ABC$." if tu is None else r"Given triangle $ABC$ with obtuse angle $%s$." % tu)
        giai_mo = (r"An acute angle has positive $\sin$, $\cos$, $\tan$, $\cot$; an obtuse angle has positive $\sin$ but negative $\cos$, $\tan$, $\cot$." + ("" if tu is None else r" If angle $%s$ of a triangle is obtuse, the other two angles are acute." % tu) + r"\\ ")
        cau += _c3s_dem(mo, dung, sai, dang, giai_mo=giai_mo)
    return cau


def L10_C3_B5_NB029_MC_J_01(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với NB029_SA_J_01 (biết góc $xOM$, tính bình phương hoành độ / tung độ của $M$): gọi
    lại hàm SA với dang=1. CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B5_NB029_SA_J_01(socau, dang)


def L10_C3_B5_NB029_MC_J_02(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với NB029_SA_J_02 (biết toạ độ, tìm số đo góc $xOM$): gọi lại hàm SA với dang=1.
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B5_NB029_SA_J_02(socau, dang)


# ---------------------------------------------------------------------
# TH030 (Bài 5): máy tính cầm tay, hệ thức cơ bản
# ---------------------------------------------------------------------
_C3S_HAM_SO = {"sin": lambda t: math.sin(t), "cos": lambda t: math.cos(t), "tan": lambda t: math.tan(t),
               "cot": lambda t: 1 / math.tan(t)}


def _c3s_goc_le(ham):
    """Góc nguyên không đặc biệt (tan, cot tránh 90 độ), giá trị làm tròn hàng phần trăm không sát nửa đơn vị."""
    while True:
        d = random.randint(1, 179)
        if d % 15 == 0 or (ham in ("tan", "cot") and abs(d - 90) < 5) or (ham == "cot" and d < 5) or (ham == "tan" and d > 175):
            continue
        v = _C3S_HAM_SO[ham](math.radians(d))
        if abs(v) > 20 or abs(v * 100 - math.floor(v * 100) - 0.5) < 0.02:
            continue
        return d, v


def L10_C3_B5_TH030_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH030_MC_A (cùng Dang: tính giá trị lượng giác bằng máy tính cầm tay),
    làm tròn đến hàng phần trăm.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        h = random.choice(["sin", "cos", "tan", "cot"])
        d, v = _c3s_goc_le(h)
        if (h, d) not in gt:
            gt.append((h, d))
    cau = ""
    for h, d in gt:
        v = _C3S_HAM_SO[h](math.radians(d))
        dap = _xx(v, 2)
        debai = (r"Using a calculator, compute $\%s %s$ (round the result to the nearest hundredth)." % (h, _goc(d)))
        giai = ((r"With the calculator in degree mode, press $\%s %d$ to get $\%s %s \approx %s$." % (h, d, h, _goc(d), dap))
                if h != "cot" else
                (r"The calculator has no $\cot$ key: $\cot %s = \dfrac{1}{\tan %s} \approx %s$." % (_goc(d), _goc(d), dap)))
        ung = [_xx(-v, 2)] + [_xx(_C3S_HAM_SO[g](math.radians(d)), 2) for g in ("sin", "cos", "tan", "cot") if g != h]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH030_MC_C (cùng Dang: khẳng định về giá trị lượng giác tra bằng máy tính
    cầm tay): bốn khẳng định ``$\sin d^{\circ} \approx x$'' (làm tròn hàng phần trăm); khẳng định sai lấy nhầm giá trị
    của hàm khác hoặc sai dấu. Đếm số khẳng định đúng (sai).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for _l in range(6):
            h = random.choice(["sin", "cos", "tan", "cot"])
            d, v = _c3s_goc_le(h)
            dap = _xx(v, 2)
            dung.append((r"$\%s %s \approx %s$" % (h, _goc(d), dap), r"the calculator gives $\%s %s \approx %s$" % (h, _goc(d), dap),
                         (h, d)))
            khac = [_xx(_C3S_HAM_SO[g](math.radians(d)), 2) for g in ("sin", "cos", "tan", "cot") if g != h]
            khac = [x for x in khac + [_xx(-v, 2)] if x != dap]
            if khac:
                sai.append((r"$\%s %s \approx %s$" % (h, _goc(d), random.choice(khac)),
                            r"the calculator gives $\%s %s \approx %s$" % (h, _goc(d), dap), (h, d)))
        cau += _c3s_dem(r"Using a calculator (results rounded to the nearest hundredth).", dung, sai, dang)
    return cau


def L10_C3_B5_TH030_MC_N_01(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với TH030_SA_N_01 (biết $\cos\widehat{xOM}$, tính diện tích tam giác $AOM$): gọi lại
    hàm SA với dang=1. CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B5_TH030_SA_N_01(socau, dang)


def L10_C3_B5_TH030_MC_N_02(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với TH030_SA_N_02 (biết diện tích tam giác $AOM$, tính $\cos\widehat{xOM}$): gọi lại
    hàm SA với dang=1. CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B5_TH030_SA_N_02(socau, dang)


# ---------------------------------------------------------------------
# TH031 (Bài 5): hai góc bù nhau, phụ nhau
# ---------------------------------------------------------------------
_C3S_TEN_HAM = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "cot": lambda t: 1 / math.tan(t)}


def L10_C3_B5_TH031_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH031_MC_A (cùng Dang: quan hệ giữa giá trị lượng giác của hai góc bù
    nhau, phụ nhau): bốn khẳng định trong tam giác $ABC$ (vd $\cos\left(A + C\right) = -\cos B$) hoặc với góc nhọn
    $\alpha$ (vd $\cos\left(90^{\circ} - \alpha\right) = \sin\alpha$); đếm số khẳng định đúng (sai). Chân trị thử bằng
    số trên nhiều tam giác (góc) ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        if random.random() < 0.5:
            mo = r"Given triangle $ABC$."
            thu = []
            while len(thu) < 4:
                A, B = random.uniform(10, 150), random.uniform(10, 150)
                if 180 - A - B > 10 and all(abs(x - 90) > 3 for x in (A, B, 180 - A - B)):
                    thu.append({"A": math.radians(A), "B": math.radians(B), "C": math.radians(180 - A - B)})
            for X, Y, Z in (("A", "B", "C"), ("A", "C", "B"), ("B", "C", "A")):
                for h in ("sin", "cos", "tan", "cot"):
                    for g in (h, _DOI_HAM[h]):
                        for dau in ("", "-"):
                            tex = r"$\%s\left(%s + %s\right) = %s\%s %s$" % (h, X, Y, dau, g, Z)
                            ok = all(abs(_C3S_TEN_HAM[h](T[X] + T[Y]) - (-1 if dau else 1) * _C3S_TEN_HAM[g](T[Z])) < 1e-9
                                     for T in thu)
                            ly = (r"$%s + %s = 180^{\circ} - %s$, so $\%s\left(%s + %s\right) = %s\%s %s$"
                                  % (X, Y, Z, h, X, Y, "" if h == "sin" else "-", h, Z))
                            (dung if ok else sai).append((tex, ly, (h, X, Y)))
        else:
            mo = r"Given an acute angle $\alpha$."
            thu = [math.radians(random.uniform(5, 85)) for _ in range(4)]
            for goc_tex, goc_f, phu in ((r"180^{\circ} - \alpha", lambda t: math.pi - t, False),
                                        (r"90^{\circ} - \alpha", lambda t: math.pi / 2 - t, True)):
                for h in ("sin", "cos", "tan", "cot"):
                    for g in (h, _DOI_HAM[h]):
                        for dau in ("", "-"):
                            tex = r"$\%s\left(%s\right) = %s\%s\alpha$" % (h, goc_tex, dau, g)
                            ok = all(abs(_C3S_TEN_HAM[h](goc_f(t)) - (-1 if dau else 1) * _C3S_TEN_HAM[g](t)) < 1e-9
                                     for t in thu)
                            if phu:
                                ly = r"for complementary angles, $\%s\left(90^{\circ} - \alpha\right) = \%s\alpha$" % (h, _DOI_HAM[h])
                            else:
                                ly = (r"for supplementary angles, $\%s\left(180^{\circ} - \alpha\right) = %s\%s\alpha$"
                                      % (h, "" if h == "sin" else "-", h))
                            (dung if ok else sai).append((tex, ly, (h, goc_tex)))
        cau += _c3s_dem(mo, dung, sai, dang)
    return cau


def L10_C3_B5_TH031_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH031_MC_B (cùng Dang: hai góc bù nhau qua hai điểm đối xứng trên nửa
    đường tròn đơn vị): cho toạ độ (số thập phân) của $M$, $N$ đối xứng với $M$ qua trục tung; tính một giá trị lượng
    giác của góc $xON$.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        p, q, r = random.choice(_C3S_BO_PY)
        x, y = _Fr3(random.choice([1, -1]) * p, r), _Fr3(q, r)
        h = random.choice(["sin", "cos", "tan", "cot"])
        v = {"sin": y, "cos": -x, "tan": y / -x, "cot": -x / y}[h]
        if _so_thap_phan_gon(Rational(v.numerator, v.denominator), 6) is None or (x, h) in [g[:1] + g[2:3] for g in gt]:
            continue
        gt.append((x, y, h, v))
    cau = ""
    for x, y, h, v in gt:
        sx, sy = _xx(float(x), 3), _xx(float(y), 3)
        dap = _so_thap_phan_gon(Rational(v.numerator, v.denominator), 6)
        debai = (r"In the coordinate plane $Oxy$, let $M\left(%s; %s\right)$ be a point on the unit semicircle. Let $N$ be the reflection of $M$ across the y-axis. Find $\%s\widehat{xON}$." % (sx, sy, h))
        giai = (r"$N$ is the reflection of $M$ across the y-axis, so $N\left(%s; %s\right)$ and $\widehat{xON} = 180^{\circ} - \widehat{xOM}$. Hence $\cos\widehat{xON} = %s$, $\sin\widehat{xON} = %s$, so $\%s\widehat{xON} = %s$."
                % (_xx(-float(x), 3), sy, _xx(-float(x), 3), sy, h, dap))
        ung = [_xx(-float(v), 3), _xx(float(x), 3), sy, _xx(float(y / x), 3)]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH031_MC_D_02 (cùng Dang: suy ra giá trị gần đúng nhờ quan hệ hai góc phụ
    nhau, bù nhau): biết $\cos 65^{\circ} \approx 0,42$, tính giá trị gần đúng của $\sin 25^{\circ}$ (hoặc góc bù).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        h = random.choice(["sin", "cos", "tan", "cot"])
        d = random.randint(10, 80)
        if d % 15 == 0:
            continue
        kieu = random.choice(["phu", "bu"])
        if (h, d, kieu) not in gt:
            gt.append((h, d, kieu))
    cau = ""
    for h, d, kieu in gt:
        v = _C3S_TEN_HAM[h](math.radians(d))
        sv = _xx(v, 2)
        if kieu == "phu":
            g, d2, dau = _DOI_HAM[h], 90 - d, ""
            ly = r"$%s$ and $%s$ are complementary angles, so $\%s %s = \%s %s$" % (_goc(d), _goc(d2), g, _goc(d2), h, _goc(d))
        else:
            g, d2, dau = h, 180 - d, ("" if h == "sin" else "-")
            ly = r"$%s$ and $%s$ are supplementary angles, so $\%s %s = %s\%s %s$" % (_goc(d), _goc(d2), g, _goc(d2), dau, h, _goc(d))
        dap = _xx((-1 if dau else 1) * float(sv.replace(",", ".")), 2)
        debai = (r"Given $\%s %s \approx %s$. Find the approximate value of $\%s %s$ (rounded to the nearest hundredth)."
                 % (h, _goc(d), sv, g, _goc(d2)))
        giai = ly + r", hence $\%s %s \approx %s$." % (g, _goc(d2), dap)
        so = float(dap.replace(",", "."))
        cau += MC_SA_answer_const(debai, dap, [_xx(-so, 2), _xx(math.sqrt(max(0.0, 1 - so * so)), 2), _xx(1 - abs(so), 2), "1"],
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH031_MC_F (cùng Dang: hai góc nhọn của tam giác vuông phụ nhau): tam
    giác $ABC$ vuông tại $B$, biết $\sin C$ hoặc $\cos C$ (số thập phân), tính $\sin A$ hoặc $\cos A$.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        p, q, r = random.choice(_C3S_BO_PY)
        w = (p, q, r, random.choice(["sin", "cos"]), random.choice(["sin", "cos"]))
        if w not in gt:
            gt.append(w)
        if len(gt) >= 24:
            break
    cau = ""
    for p, q, r, cho, hoi in gt:
        sC, cC = _Fr3(p, r), _Fr3(q, r)
        gtC = sC if cho == "sin" else cC
        dap_f = cC if hoi == "sin" else sC          # sin A = cos C, cos A = sin C
        dap = _xx(float(dap_f), 3)
        debai = (r"Triangle $ABC$ is right-angled at $B$ with $\%s C = %s$. Find $\%s A$." % (cho, _xx(float(gtC), 3), hoi))
        buoc = ""
        if (cho == "sin") == (hoi == "sin"):
            khac = "cos" if cho == "sin" else "sin"
            buoc = (r"$\%s^{2} C + \%s^{2} C = 1$ and $C$ is acute, so $\%s C = %s$; " % (cho, khac, khac,
                                                                                  _xx(float(cC if khac == "cos" else sC), 3)))
        giai = (buoc + r"$A + C = 90^{\circ}$ (the two acute angles of a right triangle are complementary), so $\%s A = \%s C = %s$."
                % (hoi, "cos" if hoi == "sin" else "sin", dap))
        ung = [_xx(float(gtC), 3), _xx(-float(dap_f), 3), _xx(float(1 - dap_f), 3), _xx(float(1 - gtC), 3),
               _xx(float(dap_f) + 0.1, 3)]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH032 (Bài 6): định lí côsin
# ---------------------------------------------------------------------
def L10_C3_B6_TH032_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH032_MC_D_01 (cùng Dang: từ hệ thức giữa các cạnh tính số đo một góc):
    cùng bộ sinh với MC_D_01, đáp số là số đo (độ). CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return _cau_he_thuc_goc(socau, dang, dang_nhan_tu=False, tra_loi_ngan=True)


def L10_C3_B6_TH032_SA_D_02(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH032_MC_D_02 (hệ thức dạng tích). CLAUDE THEM 15/10/2026 - co Lan duyet
    lai."""
    return _cau_he_thuc_goc(socau, dang, dang_nhan_tu=True, tra_loi_ngan=True)


_C3S_DINH = {"A": ("a", "b", "c"), "B": ("b", "c", "a"), "C": ("c", "a", "b")}   # góc: (cạnh đối, hai cạnh kề)


def L10_C3_B6_NB032_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH032_MC_E (cùng Dang: nhận ra hệ thức định lí côsin): bốn hệ thức (dạng
    chữ); đếm số hệ thức đúng (sai). Chân trị thử bằng số trên nhiều tam giác ngẫu nhiên.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for X in "ABC":
            d, u, v = _C3S_DINH[X]
            Y = [Z for Z in "ABC" if Z != X][random.randrange(2)]
            mau = [
                (r"%s^{2} = %s^{2} + %s^{2} - 2%s%s\cos %s" % (d, u, v, u, v, X),
                 lambda T, d=d, u=u, v=v, X=X: (T[d] ** 2, T[u] ** 2 + T[v] ** 2 - 2 * T[u] * T[v] * math.cos(T[X]))),
                (r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s%s}" % (X, u, v, d, u, v),
                 lambda T, d=d, u=u, v=v, X=X: (math.cos(T[X]), (T[u] ** 2 + T[v] ** 2 - T[d] ** 2) / (2 * T[u] * T[v]))),
                (r"%s^{2} = %s^{2} + %s^{2} + 2%s%s\cos %s" % (d, u, v, u, v, X),
                 lambda T, d=d, u=u, v=v, X=X: (T[d] ** 2, T[u] ** 2 + T[v] ** 2 + 2 * T[u] * T[v] * math.cos(T[X]))),
                (r"%s^{2} = %s^{2} + %s^{2} - %s%s\cos %s" % (d, u, v, u, v, X),
                 lambda T, d=d, u=u, v=v, X=X: (T[d] ** 2, T[u] ** 2 + T[v] ** 2 - T[u] * T[v] * math.cos(T[X]))),
                (r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{%s%s}" % (X, u, v, d, u, v),
                 lambda T, d=d, u=u, v=v, X=X: (math.cos(T[X]), (T[u] ** 2 + T[v] ** 2 - T[d] ** 2) / (T[u] * T[v]))),
                (r"%s^{2} = %s^{2} + %s^{2} - 2%s%s\cos %s" % (d, u, v, u, v, Y),
                 lambda T, d=d, u=u, v=v, Y=Y: (T[d] ** 2, T[u] ** 2 + T[v] ** 2 - 2 * T[u] * T[v] * math.cos(T[Y]))),
                (r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s%s}" % (X, u, d, v, u, d),
                 lambda T, d=d, u=u, v=v, X=X: (math.cos(T[X]), (T[u] ** 2 + T[d] ** 2 - T[v] ** 2) / (2 * T[u] * T[d]))),
            ]
            for tex, f in mau:
                ok = _c3s_dung(f)
                ly = ((r"this is the Law of Cosines (or its corollary) for angle $%s$" % X) if ok else
                      (r"by the Law of Cosines, $%s^{2} = %s^{2} + %s^{2} - 2%s%s\cos %s$" % (d, u, v, u, v, X)))
                (dung if ok else sai).append(("$%s$" % tex, ly))
        mo = r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$."
        cau += _c3s_dem(mo, dung, sai, dang, ten_kd="identities")
    return cau


def L10_C3_B6_NB032_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH032_MC_F (cùng Dang: nhận ra công thức độ dài đường trung tuyến - luyện
    tập thêm, công thức chỉ có trong SBT): bốn hệ thức; đếm số hệ thức đúng (sai). Chân trị thử bằng số.

    CLAUDE THEM 15/10/2026 - LUYEN TAP THEM (ngoai yeu cau can dat), co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for X in "ABC":
            d, u, v = _C3S_DINH[X]
            m = "m_{%s}" % d
            mk = "m" + d
            mau = [
                (r"%s^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}" % (m, u, v, d),
                 lambda T, d=d, u=u, v=v, mk=mk: (T[mk] ** 2, (T[u] ** 2 + T[v] ** 2) / 2 - T[d] ** 2 / 4)),
                (r"%s^{2} = \dfrac{2\left(%s^{2} + %s^{2}\right) - %s^{2}}{4}" % (m, u, v, d),
                 lambda T, d=d, u=u, v=v, mk=mk: (T[mk] ** 2, (2 * (T[u] ** 2 + T[v] ** 2) - T[d] ** 2) / 4)),
                (r"%s^{2} = \dfrac{%s^{2} + %s^{2}}{2} + \dfrac{%s^{2}}{4}" % (m, u, v, d),
                 lambda T, d=d, u=u, v=v, mk=mk: (T[mk] ** 2, (T[u] ** 2 + T[v] ** 2) / 2 + T[d] ** 2 / 4)),
                (r"%s^{2} = \dfrac{%s^{2} + %s^{2}}{4} - \dfrac{%s^{2}}{2}" % (m, u, v, d),
                 lambda T, d=d, u=u, v=v, mk=mk: (T[mk] ** 2, (T[u] ** 2 + T[v] ** 2) / 4 - T[d] ** 2 / 2)),
                (r"%s^{2} = \dfrac{%s^{2} + %s^{2} - %s^{2}}{4}" % (m, u, v, d),
                 lambda T, d=d, u=u, v=v, mk=mk: (T[mk] ** 2, (T[u] ** 2 + T[v] ** 2 - T[d] ** 2) / 4)),
                (r"%s^{2} = %s^{2} + %s^{2} - \dfrac{%s^{2}}{4}" % (m, u, v, d),
                 lambda T, d=d, u=u, v=v, mk=mk: (T[mk] ** 2, T[u] ** 2 + T[v] ** 2 - T[d] ** 2 / 4)),
            ]
            for tex, f in mau:
                ok = _c3s_dung(f)
                ly = ((r"this is the formula for the length of the median from $%s$" % X) if ok else
                      (r"the correct formula is $%s^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}$" % (m, u, v, d)))
                (dung if ok else sai).append(("$%s$" % tex, ly))
        dung.append((r"$m_{a}^{2} + m_{b}^{2} + m_{c}^{2} = \dfrac{3}{4}\left(a^{2} + b^{2} + c^{2}\right)$",
                     r"add the three median length formulas"))
        sai.append((r"$m_{a}^{2} + m_{b}^{2} + m_{c}^{2} = \dfrac{1}{2}\left(a^{2} + b^{2} + c^{2}\right)$",
                    r"adding the three median length formulas gives $\dfrac{3}{4}\left(a^{2} + b^{2} + c^{2}\right)$"))
        assert _c3s_dung(lambda T: (T["ma"] ** 2 + T["mb"] ** 2 + T["mc"] ** 2, 0.75 * (T["a"] ** 2 + T["b"] ** 2 + T["c"] ** 2)))
        mo = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$; $m_a$, $m_b$, $m_c$ are the lengths of the medians from $A$, $B$, $C$ respectively.")
        cau += _c3s_dem(mo, dung, sai, dang, ten_kd="identities")
    return cau


# ---------------------------------------------------------------------
# TH033 (Bài 6): định lí sin
# ---------------------------------------------------------------------
def L10_C3_B6_NB033_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH033_MC_C (cùng Dang: nhận ra và dùng hệ thức định lí sin): bốn hệ thức
    (dạng chữ, $R$ là bán kính đường tròn ngoại tiếp); đếm số hệ thức đúng (sai). Chân trị thử bằng số.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for X, Y in (("A", "B"), ("B", "C"), ("C", "A"), ("B", "A"), ("C", "B"), ("A", "C")):
            x, y = _C3S_DINH[X][0], _C3S_DINH[Y][0]
            mau = [
                (r"\dfrac{%s}{\sin %s} = 2R" % (x, X), lambda T, x=x, X=X: (T[x] / math.sin(T[X]), 2 * T["R"])),
                (r"%s = 2R\sin %s" % (x, X), lambda T, x=x, X=X: (T[x], 2 * T["R"] * math.sin(T[X]))),
                (r"\sin %s = \dfrac{%s}{2R}" % (X, x), lambda T, x=x, X=X: (math.sin(T[X]), T[x] / (2 * T["R"]))),
                (r"%s\sin %s = %s\sin %s" % (x, Y, y, X), lambda T, x=x, y=y, X=X, Y=Y: (T[x] * math.sin(T[Y]), T[y] * math.sin(T[X]))),
                (r"\dfrac{%s}{\sin %s} = R" % (x, X), lambda T, x=x, X=X: (T[x] / math.sin(T[X]), T["R"])),
                (r"%s = R\sin %s" % (x, X), lambda T, x=x, X=X: (T[x], T["R"] * math.sin(T[X]))),
                (r"\sin %s = \dfrac{2R}{%s}" % (X, x), lambda T, x=x, X=X: (math.sin(T[X]), 2 * T["R"] / T[x])),
                (r"%s\sin %s = %s\sin %s" % (x, X, y, Y), lambda T, x=x, y=y, X=X, Y=Y: (T[x] * math.sin(T[X]), T[y] * math.sin(T[Y]))),
                (r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s}" % (x, Y, y, X),
                 lambda T, x=x, y=y, X=X, Y=Y: (T[x] / math.sin(T[Y]), T[y] / math.sin(T[X]))),
            ]
            for tex, f in mau:
                ok = _c3s_dung(f)
                ly = (r"by the Law of Sines, $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$" if ok else
                      r"the Law of Sines gives $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$, and this identity does not follow from it")
                (dung if ok else sai).append(("$%s$" % tex, ly))
        mo = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$, and $R$ the circumradius of the triangle.")
        cau += _c3s_dem(mo, dung, sai, dang, ten_kd="identities")
    return cau


# ---------------------------------------------------------------------
# TH034 (Bài 6): diện tích tam giác
# ---------------------------------------------------------------------
def _c3s_heron_nguyen():
    """Các tam giác cạnh nguyên (<= 30), diện tích nguyên, không suy biến."""
    ra = []
    for a in range(3, 31):
        for b in range(a, 31):
            for c in range(b, min(a + b, 31)):
                s16 = (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)
                r = math.isqrt(s16)
                if r * r == s16 and r % 4 == 0:
                    ra.append((a, b, c, r // 4))
    return ra


_C3S_HERON = _c3s_heron_nguyen()


def L10_C3_B6_TH034_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH034_MC_B (cùng Dang: công thức Heron, biết ba cạnh tính diện tích).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        w = random.choice(_C3S_HERON)
        if w not in gt:
            gt.append(w)
    cau = ""
    for a, b, c, S in gt:
        ds = [a, b, c]
        random.shuffle(ds)
        a, b, c = ds
        p = _Fr3(a + b + c, 2)
        sp = _xx(float(p), 1)
        debai = r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$. Find the area of triangle $ABC$." % (a, b, c)
        giai = (r"Semi-perimeter $p = \dfrac{%d + %d + %d}{2} = %s$.\\ Heron's formula: $S = \sqrt{p(p - a)(p - b)(p - c)} = \sqrt{%s\cdot %s\cdot %s\cdot %s} = %d$."
                % (a, b, c, sp, sp, _xx(float(p - a), 1), _xx(float(p - b), 1), _xx(float(p - c), 1), S))
        cau += MC_SA_answer_const(debai, str(S), [str(2 * S), str(S // 2) if S % 2 == 0 else str(S + 1), str(S * S)],
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH034_MC_C (cùng Dang: biết diện tích và hai cạnh, tìm góc xen giữa;
    cho biết góc nhọn hay tù để góc xác định duy nhất). Đáp số là số đo (độ).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        w = (random.choice([30, 45, 60, 120, 135, 150]), random.randint(2, 12), random.randint(2, 12))
        if w not in gt:
            gt.append(w)
    cau = ""
    for g, b, c in gt:
        sA = _gtlg("sin", g)
        S = simplify(Rational(1, 2) * b * c * sA)
        debai = (r"Triangle $ABC$ has $AB = %d$, $AC = %d$ and area $S = %s$. Given that angle $A$ is %s, find the measure of angle $A$ (in degrees)." % (c, b, _L(S), "obtuse" if g > 90 else "acute"))
        giai = (r"$S = \dfrac{1}{2}AB\cdot AC\cdot\sin A$, so $\sin A = \dfrac{2S}{AB\cdot AC} = \dfrac{2\cdot %s}{%d\cdot %d} = %s$. Angle $A$ is %s, so $\widehat{A} = %d^{\circ}$." % (_L(S), c, b, _L(sA), "obtuse" if g > 90 else "acute", g))
        cau += MC_SA_answer_const(debai, str(g), [str(180 - g), "90", str(abs(90 - g)), str(g + 15), str(g - 15)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH034_MC_F (cùng Dang: tính đường cao qua diện tích): biết ba cạnh (Heron)
    hoặc hai cạnh và góc xen giữa; tính đường cao $h_a$ (làm tròn đến hàng phần trăm).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.5:
            a, b, c, S = random.choice(_C3S_HERON)
            ds = [a, b, c]
            random.shuffle(ds)
            a, b, c = ds
            h = 2 * S / a
            debai = (r"Given triangle $ABC$ with $BC = %d$, $CA = %d$, $AB = %d$. Find the length of the altitude $h_a$ from $A$ (rounded to the nearest hundredth)." % (a, b, c))
            giai = (r"By Heron's formula, the area of the triangle is $S = %d$. Since $S = \dfrac{1}{2}a\cdot h_a$, $h_a = \dfrac{2S}{a} = \dfrac{2\cdot %d}{%d} \approx %s$." % (S, S, a, _xx(h, 2)))
        else:
            g = random.choice([60, 120])
            b, c = random.sample(range(2, 13), 2)
            a2 = b * b + c * c - 2 * b * c * (0.5 if g == 60 else -0.5)
            a = math.sqrt(a2)
            S = 0.5 * b * c * math.sin(math.radians(g))
            h = 2 * S / a
            debai = (r"Triangle $ABC$ has $AB = %d$, $AC = %d$, $\widehat{BAC} = %s$. Find the length of the altitude $h_a$ from $A$ (rounded to the nearest hundredth)." % (c, b, _goc(g)))
            giai = (r"$BC^{2} = AB^{2} + AC^{2} - 2AB\cdot AC\cos A = %d$, so $BC = \sqrt{%d}$.\\ $S = \dfrac{1}{2}AB\cdot AC\sin A = %s$.\\ $h_a = \dfrac{2S}{BC} \approx %s$."
                    % (round(a2), round(a2), _L(simplify(Rational(1, 2) * b * c * _gtlg("sin", g))), _xx(h, 2)))
        dap = _xx(h, 2)
        cau += MC_SA_answer_const(debai, dap, [_xx(h / 2, 2), _xx(2 * h, 2), _xx(h + 1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_NB034_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH034_MC_G (cùng Dang: nhận ra công thức diện tích theo $R$, $r$, Heron
    và công thức tính $R$, $r$): bốn công thức; đếm số công thức đúng (sai). Chân trị thử bằng số.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    sq = math.sqrt
    KHO = [
        (r"S = \dfrac{abc}{4R}", lambda T: (T["S"], T["a"] * T["b"] * T["c"] / (4 * T["R"]))),
        (r"S = pr", lambda T: (T["S"], T["p"] * T["r"])),
        (r"S = \dfrac{1}{2}ab\sin C", lambda T: (T["S"], 0.5 * T["a"] * T["b"] * math.sin(T["C"]))),
        (r"S = \dfrac{1}{2}bc\sin A", lambda T: (T["S"], 0.5 * T["b"] * T["c"] * math.sin(T["A"]))),
        (r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}",
         lambda T: (T["S"], sq(T["p"] * (T["p"] - T["a"]) * (T["p"] - T["b"]) * (T["p"] - T["c"])))),
        (r"R = \dfrac{abc}{4S}", lambda T: (T["R"], T["a"] * T["b"] * T["c"] / (4 * T["S"]))),
        (r"r = \dfrac{S}{p}", lambda T: (T["r"], T["S"] / T["p"])),
        (r"S = \dfrac{1}{2}a\cdot h_a", lambda T: (T["S"], 0.5 * T["a"] * T["ha"])),
        (r"S = \dfrac{abc}{4r}", lambda T: (T["S"], T["a"] * T["b"] * T["c"] / (4 * T["r"]))),
        (r"S = 2pr", lambda T: (T["S"], 2 * T["p"] * T["r"])),
        (r"S = \dfrac{1}{2}ab\sin A", lambda T: (T["S"], 0.5 * T["a"] * T["b"] * math.sin(T["A"]))),
        (r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}",
         lambda T: (T["S"], sq(T["p"] * (T["p"] + T["a"]) * (T["p"] + T["b"]) * (T["p"] + T["c"])))),
        (r"S = \dfrac{abc}{2R}", lambda T: (T["S"], T["a"] * T["b"] * T["c"] / (2 * T["R"]))),
        (r"r = \dfrac{2S}{p}", lambda T: (T["r"], 2 * T["S"] / T["p"])),
        (r"S = a\cdot h_a", lambda T: (T["S"], T["a"] * T["ha"])),
        (r"R = \dfrac{abc}{S}", lambda T: (T["R"], T["a"] * T["b"] * T["c"] / T["S"])),
    ]
    LY_DUNG = r"this is one of the area formulas ($S = \dfrac{1}{2}ab\sin C = \dfrac{abc}{4R} = pr = \sqrt{p(p - a)(p - b)(p - c)}$)"
    LY_SAI = (r"the correct formulas are $S = \dfrac{1}{2}a\cdot h_a = \dfrac{1}{2}ab\sin C = \dfrac{abc}{4R} = pr = \sqrt{p(p - a)(p - b)(p - c)}$")
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for tex, f in KHO:
            ok = _c3s_dung(f)
            (dung if ok else sai).append(("$%s$" % tex, LY_DUNG if ok else LY_SAI))
        mo = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$, area $S$, semi-perimeter $p$, altitude $h_a$ from $A$; $R$, $r$ are the circumradius and the inradius of the triangle.")
        cau += _c3s_dem(mo, dung, sai, dang, ten_kd="formulas")
    return cau


# ---------------------------------------------------------------------
# TH035 (Bài 6): nhận dạng tam giác nhọn, vuông, tù
# ---------------------------------------------------------------------
def L10_C3_B6_TH035_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH035_MC_C (cùng Dang: nhận dạng tam giác nhọn, vuông hay tù bằng định lí
    côsin): cho bốn tam giác (ba cạnh nguyên), hỏi có bao nhiêu tam giác nhọn (vuông, tù).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    VUONG = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15), (20, 21, 29), (12, 16, 20)]

    def loai(x, y, z):
        x, y, z = sorted((x, y, z))
        return "right" if x * x + y * y == z * z else ("obtuse" if x * x + y * y < z * z else "acute")
    cau = ""
    for _ in range(socau):
        hoi = random.choice(["acute", "right", "obtuse"])
        t = random.choice([1, 2, 3])
        ds = []
        lan = 0
        while len(ds) < 4 and lan < 5000:
            lan += 1
            if random.random() < 0.3:
                bo = list(random.choice(VUONG))
            else:
                x, y = random.randint(3, 20), random.randint(3, 20)
                z = random.randint(abs(x - y) + 1, x + y - 1)
                bo = [x, y, z]
            random.shuffle(bo)
            k = loai(*bo)
            can = (k == hoi) if sum(1 for b in ds if loai(*b) == hoi) < t else (k != hoi)
            if can and sorted(bo) not in [sorted(b) for b in ds]:
                ds.append(bo)
        random.shuffle(ds)
        dap = sum(1 for b in ds if loai(*b) == hoi)
        debai = (r"Given four triangles whose side lengths are as follows:\\ " +
                 r"\\ ".join(r"%d. $%d$, $%d$, $%d$" % ((i + 1,) + tuple(b)) for i, b in enumerate(ds)) +
                 r"\\ How many of them are \textbf{%s} triangles?" % hoi)
        dong = []
        for i, b in enumerate(ds):
            x, y, z = sorted(b)
            dau = "=" if x * x + y * y == z * z else ("<" if x * x + y * y < z * z else ">")
            dong.append(r"%d. Longest side $%d$: $%d^{2} + %d^{2} = %d %s %d = %d^{2}$, so the triangle is %s."
                        % (i + 1, z, x, y, x * x + y * y, dau, z * z, z, loai(*b)))
        giai = (r"Let $z$ be the longest side and $x$, $y$ the other two sides. By the corollary of the Law of Cosines, the largest angle is acute, right, obtuse when $x^{2} + y^{2}$ is greater than, equal to, less than $z^{2}$ respectively.\\ " + r"\\ ".join(dong) +
                r"\\ So there are $%d$ %s triangles." % (dap, hoi))
        cau += MC_SA_answer_const(debai, str(dap), [str(x) for x in (4 - dap, dap + 1, dap - 1, 0, 4) if x != dap and 0 <= x <= 4],
                                  giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# VD032 (Bài 6): hình bình hành biết một cạnh và hai đường chéo (luyện tập thêm)
# ---------------------------------------------------------------------
def L10_C3_B6_VD032_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của VD032_MC_A (cùng Dang: hình bình hành biết một cạnh và hai đường chéo,
    tính cạnh kề - dùng công thức trung tuyến, luyện tập thêm). Làm tròn đến hàng phần mười.

    CLAUDE THEM 15/10/2026 - LUYEN TAP THEM (ngoai yeu cau can dat), co Lan duyet lai.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 3000:
        lan += 1
        ac, bd = sorted(random.sample(range(6, 25, 2), 2))
        ab = random.randint(3, 20)
        ad2 = _Fr3(ac * ac + bd * bd, 2) - ab * ab
        if ad2 <= 0:
            continue
        ad = math.sqrt(ad2)
        # tam giác OAB, OAD (O là giao hai đường chéo) phải tồn tại
        oa, ob = ac / 2, bd / 2
        if not (abs(oa - ob) < ab < oa + ob and abs(oa - ob) < ad < oa + ob):
            continue
        if (ab, ac, bd) not in [g[:3] for g in gt]:
            gt.append((ab, ac, bd, ad2))
    cau = ""
    for ab, ac, bd, ad2 in gt:
        ad = math.sqrt(ad2)
        dap = _xx(ad, 1)
        debai = (r"Parallelogram $ABCD$ has $AB = %d$ and diagonals $AC = %d$, $BD = %d$. Find the length of side $AD$ (rounded to the nearest tenth)." % (ab, ac, bd))
        giai = (r"Let $O$ be the intersection of the diagonals; $O$ is the midpoint of $AC$ and $BD$. $AO$ is a median of triangle $ABD$, so $AO^{2} = \dfrac{AB^{2} + AD^{2}}{2} - \dfrac{BD^{2}}{4}$ with $AO = \dfrac{AC}{2} = %s$.\\ Hence $AD^{2} = 2AO^{2} + \dfrac{BD^{2}}{2} - AB^{2} = \dfrac{AC^{2} + BD^{2}}{2} - AB^{2} = %s$, so $AD \approx %s$." % (_xx(ac / 2, 1), _xx(float(ad2), 2), dap))
        cau += MC_SA_answer_const(debai, dap, [_xx(float(ad2), 1), _xx(math.sqrt(ac * ac + bd * bd - ab * ab), 1),
                                              _xx(math.sqrt(abs((ac * ac + bd * bd) / 4 - ab * ab)), 1), _xx(ad + 1, 1),
                                              _xx(ad - 1, 1)], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# VD036 (Bài 6): khoảng cách qua vật cản bằng định lí sin; bản MC của SA_Z, SA_X
# ---------------------------------------------------------------------
def L10_C3_B6_VD036_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của VD036_MC_B_01 (cùng Dang: đo khoảng cách qua đầm lầy bằng định lí sin):
    biết $AC$ và hai góc $\widehat{BAC}$, $\widehat{BCA}$, tính $AB$ (làm tròn đến hàng phần trăm). Số đo giả sử.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    gt = []
    while len(gt) < socau:
        b, A, C = random.randint(3, 20), random.randint(92, 118), random.randint(35, 70)
        if A + C >= 170:
            continue
        ket = b * math.sin(math.radians(C)) / math.sin(math.radians(180 - A - C))
        if abs(ket * 100 - math.floor(ket * 100) - 0.5) < 0.02 or (b, A, C) in gt:
            continue
        gt.append((b, A, C))
    cau = ""
    for b, A, C in gt:
        B = 180 - A - C
        c = b * math.sin(math.radians(C)) / math.sin(math.radians(B))
        dap = _xx(c, 2)
        debai = (r"To measure the distance from point $A$ to point $B$ across a swamp, a point $C$ is chosen and the measurements are $AC = %d\,\text{m}$, $\widehat{BAC} = %s$, $\widehat{BCA} = %s$ (assumed values). Find the distance $AB$ (in meters, rounded to the nearest hundredth)." % (b, _goc(A), _goc(C)))
        giai = (r"$\widehat{ABC} = 180^{\circ} - %s - %s = %s$. By the Law of Sines, $\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B}$, so $AB = \dfrac{%d\sin %s}{\sin %s} \approx %s\,\text{m}$." % (_goc(A), _goc(C), _goc(B), b, _goc(C), _goc(B), dap))
        ung = [_xx(b * math.sin(math.radians(B)) / math.sin(math.radians(C)), 2), _xx(b * math.sin(math.radians(C)), 2),
               _xx(b * math.sin(math.radians(A)) / math.sin(math.radians(B)), 2), _xx(c + 1, 2), _xx(c - 1, 2)]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_MC_Z_01(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với VD036_SA_Z_01 (diện tích thửa ruộng tam giác bằng Heron): gọi lại hàm SA với
    dang=1. CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B6_VD036_SA_Z_01(socau, dang)


def L10_C3_B6_VD036_MC_Z_02(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với VD036_SA_Z_02 (hai cạnh và góc xen giữa). CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B6_VD036_SA_Z_02(socau, dang)


def L10_C3_B6_VD036_MC_Z_03(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với VD036_SA_Z_03 (tứ giác = hai tam giác Heron). CLAUDE THEM 15/10/2026 - co Lan duyet
    lai."""
    return L10_C3_B6_VD036_SA_Z_03(socau, dang)


def L10_C3_B6_VD036_MC_X_01(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với VD036_SA_X_01 (hai người đi theo hai hướng tới cùng một đích: quãng đường còn lại).
    CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B6_VD036_SA_X_01(socau, dang)


def L10_C3_B6_VD036_MC_X_02(socau, dang=1):
    r"""Trắc nghiệm cùng dạng với VD036_SA_X_02 (diện tích tứ giác). CLAUDE THEM 15/10/2026 - co Lan duyet lai."""
    return L10_C3_B6_VD036_SA_X_02(socau, dang)


# =====================================================================
# BỔ SUNG 15/10/2026 (lần 2): MỨC NHẬN BIẾT BÀI 6 (cô Lan: "ra đề hỏi về nhận biết các công thức toán học trong bài
# 6. MC là tìm công thức đúng/sai. SA là có bao nhiêu công thức đúng/sai"). Curriculum của Bộ không có NB ở Bài 6 nên
# các dạng NB032, NB033, NB034 là LUYỆN TẬP THÊM (ngoai_yccd) - hệ thống cảnh báo giáo viên khi vào đề.
# CLAUDE THEM 15/10/2026 - co Lan duyet lai.
# =====================================================================
def L10_C3_B6_TH033_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của TH033_MC_C (cùng Dang: dùng định lí sin tính tỉ số hai cạnh khi biết hai
    góc): $\dfrac{BC}{CA} = \dfrac{\sin A}{\sin B}$, làm tròn đến hàng phần trăm.

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    CAP = [(A, B) for A in _GOC_TAM_GIAC for B in _GOC_TAM_GIAC if A != B and A + B < 180]
    gt = []
    lan = 0
    while len(gt) < socau and lan < 300:
        lan += 1
        v = random.choice(CAP)
        k = float(_gtlg("sin", v[0]) / _gtlg("sin", v[1]))
        if v not in gt and abs(k * 100 - math.floor(k * 100) - 0.5) > 0.02:
            gt.append(v)
    cau = ""
    for A, B in gt:
        sA, sB = _gtlg("sin", A), _gtlg("sin", B)
        k = float(sA / sB)
        dap = _xx(k, 2)
        debai = (r"Triangle $ABC$ has $\widehat{A} = %s$, $\widehat{B} = %s$. Find the ratio $\dfrac{BC}{CA}$ (round the result to the nearest hundredth)." % (_goc(A), _goc(B)))
        giai = (r"By the Law of Sines, $\dfrac{BC}{\sin A} = \dfrac{CA}{\sin B}$, so $\dfrac{BC}{CA} = \dfrac{\sin A}{\sin B} = \dfrac{%s}{%s} \approx %s$." % (_L(sA), _L(sB), dap))
        ung = [_xx(1 / k, 2), _xx(A / B, 2), _xx(k + 1, 2), _xx(abs(k - 1), 2)]
        cau += MC_SA_answer_const(debai, dap, ung, giai, 0, 0, dang)
    return cau


# Dữ kiện (mô tả, các đại lượng biết) và công thức (tex, đại lượng dùng, hàm thử số, đúng?) cho NB034_SA_B.
_C3S_DU_KIEN = [
    (r"the three sides $a$, $b$, $c$", {"a", "b", "c", "p"}),
    (r"the three sides $a$, $b$, $c$ and the circumradius $R$", {"a", "b", "c", "p", "R"}),
    (r"the semi-perimeter $p$ and the inradius $r$", {"p", "r"}),
    (r"two sides $b$, $c$ and angle $A$", {"b", "c", "A"}),
    (r"two sides $a$, $b$ and angle $C$", {"a", "b", "C"}),
    (r"side $a$ and the altitude $h_a$", {"a", "ha"}),
]
_C3S_CT_S = [
    (r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}", {"p", "a", "b", "c"}),
    (r"S = \dfrac{abc}{4R}", {"a", "b", "c", "R"}),
    (r"S = pr", {"p", "r"}),
    (r"S = \dfrac{1}{2}bc\sin A", {"b", "c", "A"}),
    (r"S = \dfrac{1}{2}ab\sin C", {"a", "b", "C"}),
    (r"S = \dfrac{1}{2}a\cdot h_a", {"a", "ha"}),
    (r"S = \dfrac{abc}{2R}", {"a", "b", "c", "R"}),
    (r"S = 2pr", {"p", "r"}),
    (r"S = \dfrac{1}{2}bc\cos A", {"b", "c", "A"}),
    (r"S = \dfrac{1}{2}ab\sin A", {"a", "b", "A"}),
    (r"S = a\cdot h_a", {"a", "ha"}),
    (r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}", {"p", "a", "b", "c"}),
]


def _c3s_ct_dung(tex):
    """Công thức diện tích tex có đúng với mọi tam giác không (thử số)."""
    f = {
        r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}":
            lambda T: math.sqrt(T["p"] * (T["p"] - T["a"]) * (T["p"] - T["b"]) * (T["p"] - T["c"])),
        r"S = \dfrac{abc}{4R}": lambda T: T["a"] * T["b"] * T["c"] / (4 * T["R"]),
        r"S = pr": lambda T: T["p"] * T["r"],
        r"S = \dfrac{1}{2}bc\sin A": lambda T: 0.5 * T["b"] * T["c"] * math.sin(T["A"]),
        r"S = \dfrac{1}{2}ab\sin C": lambda T: 0.5 * T["a"] * T["b"] * math.sin(T["C"]),
        r"S = \dfrac{1}{2}a\cdot h_a": lambda T: 0.5 * T["a"] * T["ha"],
        r"S = \dfrac{abc}{2R}": lambda T: T["a"] * T["b"] * T["c"] / (2 * T["R"]),
        r"S = 2pr": lambda T: 2 * T["p"] * T["r"],
        r"S = \dfrac{1}{2}bc\cos A": lambda T: 0.5 * T["b"] * T["c"] * math.cos(T["A"]),
        r"S = \dfrac{1}{2}ab\sin A": lambda T: 0.5 * T["a"] * T["b"] * math.sin(T["A"]),
        r"S = a\cdot h_a": lambda T: T["a"] * T["ha"],
        r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}":
            lambda T: math.sqrt(T["p"] * (T["p"] + T["a"]) * (T["p"] + T["b"]) * (T["p"] + T["c"])),
    }[tex]
    return _c3s_dung(lambda T: (T["S"], f(T)))


def L10_C3_B6_NB034_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB034_MC_B (cùng Dang: chọn công thức diện tích phù hợp với dữ kiện):
    bốn khẳng định ``Biết <dữ kiện> thì $S = \ldots$''; khẳng định đúng khi công thức đúng VÀ chỉ dùng các đại lượng
    đã biết (biết ba cạnh thì biết nửa chu vi $p$). Đếm số khẳng định đúng (sai). Mức Nhận biết - LUYỆN TẬP THÊM
    (ngoài YCCĐ).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    ten_dai = {"a": "$a$", "b": "$b$", "c": "$c$", "p": "$p$", "R": "$R$", "r": "$r$", "A": "angle $A$", "C": "angle $C$",
               "ha": "$h_a$"}
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for mo_dk, biet in _C3S_DU_KIEN:
            for tex, dung_dl in _C3S_CT_S:
                ok_ct = _c3s_ct_dung(tex)
                thieu = sorted(dung_dl - biet)
                kd = r"Knowing %s, $%s$" % (mo_dk, tex)
                if ok_ct and not thieu:
                    dung.append((kd, r"this is an area formula and it uses only known quantities", tex))
                elif ok_ct:
                    sai.append((kd, r"the formula is correct but it also needs %s, which is not known" % ", ".join(ten_dai[x] for x in thieu), tex))
                elif not thieu or random.random() < 0.3:
                    sai.append((kd, r"the formula $%s$ is wrong" % tex, tex))
        mo = (r"Given triangle $ABC$ with $BC = a$, $CA = b$, $AB = c$, area $S$, semi-perimeter $p$, altitude $h_a$ from $A$; $R$, $r$ are the circumradius and the inradius of the triangle.")
        cau += _c3s_dem(mo, dung, sai, dang)
    return cau
