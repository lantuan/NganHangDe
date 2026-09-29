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
DAU_THAP_PHAN = ","


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

        debai = r"Giá trị của $%s %s$ bằng" % (ki, _goc(d))
        giai = (r"Tra bảng giá trị lượng giác của các góc đặc biệt: $%s %s = %s$."
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
                ds.add("%.2f" % lech)
        debai = (r"Dùng máy tính cầm tay, giá trị của $\%s %s$ (làm tròn đến hàng phần trăm) bằng"
                 % (ki, _goc(d)))
        giai = (r"Chuyển máy tính về chế độ \textbf{DEG} rồi bấm $\%s %s$, được $%.2f$."
                % (ki, _goc(d), dung))
        cauTN += MC_SA_answer_const(debai, "%.2f" % dung, list(ds), giai, 0, 0, dang)
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

        debai = r"Cho $\%s %s = %s$. Giá trị của $\%s %s$ bằng" % (
            ki, _goc(d), latex(hang[chi]), ki, _goc(bu))
        giai = (r"Hai góc $%s$ và $%s$ bù nhau nên $%s$. Do đó $\%s %s = %s$."
                % (_goc(d), _goc(bu), he_thuc, ki, _goc(bu), latex(gia_tri_bu)))
        cauTN += MC_SA_answer_const(debai, latex(gia_tri_bu), list(ds), giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_SA_A_01(socau, dang=2):
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
        debai = (r"Rút gọn biểu thức $P = %d\left(\cos %s + \cos %s\right) + \sin^{2} %s + \cos^{2} %s$."
                 % (he_so, _goc(d), _goc(bu), _goc(d), _goc(d)))
        giai = (r"Vì $%s$ và $%s$ bù nhau nên $\cos %s = -\cos %s$, do đó "
                r"$\cos %s + \cos %s = 0$.\\ "
                r"Lại có $\sin^{2}\alpha + \cos^{2}\alpha = 1$ nên $P = %d \cdot 0 + 1 = 1$."
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

        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\widehat{A} = %s$. "
                 r"Độ dài cạnh $BC$ bằng" % (b, c, _goc(A)))
        giai = (r"Áp dụng định lí côsin trong tam giác $ABC$:\\ "
                r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
                r"Vậy $BC = %d$."
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\widehat{A} = %s$. "
                 r"Tính độ dài cạnh $BC$." % (b, c, _goc(A)))
        giai = (r"Định lí côsin: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, "
                r"suy ra $BC = %d$." % (b, c, b, c, latex(cos_A), a2, a))
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

        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$. "
                 r"Độ dài cạnh $AC$ bằng" % (a, _goc(A), _goc(B)))
        giai = (r"Áp dụng định lí sin: $\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B}$.\\ "
                r"Suy ra $AC = \dfrac{BC\cdot\sin B}{\sin A} "
                r"= \dfrac{%d\cdot %s}{%s} = %s$."
                % (a, latex(hang_B[1]), latex(hang_A[1]), latex(b)))
        ds = _ba_nhieu(
            latex(b),
            [latex(simplify(a / k)), latex(a * 2), latex(simplify(b + a))],
            buoc=lambda t: latex(a + t + 2))
        cauTN += MC_SA_answer_const(debai, latex(b), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_SA_A_01(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$ và $\widehat{A} = 30^{\circ}$. "
                 r"Bán kính $R$ của đường tròn ngoại tiếp tam giác $ABC$ bằng bao nhiêu?" % a)
        giai = (r"Áp dụng định lí sin: $\dfrac{BC}{\sin A} = 2R$.\\ "
                r"Suy ra $R = \dfrac{BC}{2\sin A} = \dfrac{%d}{2\cdot\frac{1}{2}} = %d$."
                % (a, R))
        ds = [str(2 * a), str(a // 2 if a % 2 == 0 else a + 1), str(a + 3)]
        cauTN += MC_SA_answer_const(debai, str(R), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_MC_A_01(socau, dang=1):
    """Chọn công thức tính diện tích tam giác phù hợp với dữ kiện cho trước."""
    BO = [
        ("biết hai cạnh $b$, $c$ và góc $A$ xen giữa",
         r"$S = \dfrac{1}{2}bc\sin A$"),
        ("biết ba cạnh $a$, $b$, $c$",
         r"$S = \sqrt{p(p-a)(p-b)(p-c)}$"),
        ("biết ba cạnh $a$, $b$, $c$ và bán kính $R$ của đường tròn ngoại tiếp",
         r"$S = \dfrac{abc}{4R}$"),
        ("biết ba cạnh $a$, $b$, $c$ và bán kính $r$ của đường tròn nội tiếp",
         r"$S = pr$"),
        ("biết cạnh $a$ và đường cao $h_a$ ứng với cạnh đó",
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
        debai = (r"Tam giác $ABC$ có diện tích $S$, nửa chu vi $p$. "
                 r"Khi %s, công thức tính diện tích tam giác là" % du_kien)
        giai = r"Với dữ kiện %s, ta dùng công thức %s." % (du_kien, ct)
        cauTN += MC_SA_answer_text(debai, ct, ds[:3], giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_SA_A_01(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $AB = %d$, $AC = %d$ và $\widehat{A} = %s$. "
                 r"Diện tích tam giác $ABC$ bằng bao nhiêu?" % (c, b, _goc(A)))
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

        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$, $\widehat{A} = %s$. "
                 r"Giá trị $\cos B$ bằng" % (b, c, _goc(A)))
        giai = (r"Định lí côsin cho $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, "
                r"nên $BC = %d$.\\ "
                r"Lại theo định lí côsin: $\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} "
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{B} = %s$, $\widehat{C} = %s$. "
                 r"Số đo góc $\widehat{A}$ bằng" % (a, _goc(A), _goc(B)))
        giai = (r"Tổng ba góc trong tam giác bằng $180^{\circ}$ nên "
                r"$\widehat{A} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C)))
        ds = list(dict.fromkeys([_goc(C + 15), _goc(abs(C - 15)), _goc(180 - C)]))
        ds = [x for x in ds if x != _goc(C)][:3]
        while len(ds) < 3:
            ds.append(_goc(C + 10 * (len(ds) + 2)))
        cauTN += MC_SA_answer_const(debai, _goc(C), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH035_SA_A_01(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{B} = %s$, $\widehat{C} = %s$. "
                 r"Tính số đo góc $\widehat{A}$ (đơn vị độ)." % (a, _goc(A), _goc(B)))
        giai = (r"$\widehat{A} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C)))
        ds = list(dict.fromkeys([str(C + 15), str(abs(C - 15)), str(180 - C)]))
        ds = [x for x in ds if x != str(C)][:3]
        while len(ds) < 3:
            ds.append(str(C + 10 * (len(ds) + 2)))
        cauTN += MC_SA_answer_const(debai, str(C), ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_MC_A_01(socau, dang=1):
    """Đo khoảng cách giữa hai địa điểm khi gặp vật cản (định lí côsin)."""
    DIA_DIEM = [("hai bờ của một cái hồ", "hồ"), ("hai bên một khu rừng", "khu rừng"),
                ("hai phía của một toà nhà", "toà nhà")]
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

        debai = (r"Để đo khoảng cách giữa hai điểm $A$ và $B$ nằm ở %s (không đo trực tiếp được), "
                 r"người ta chọn điểm $C$ rồi đo được $CA = %d\,\text{m}$, $CB = %d\,\text{m}$ và "
                 r"$\widehat{ACB} = %s$. Khoảng cách $AB$ bằng"
                 % (canh, b, c, _goc(A)))
        giai = (r"Áp dụng định lí côsin trong tam giác $ABC$:\\ "
                r"$AB^{2} = CA^{2} + CB^{2} - 2\cdot CA\cdot CB\cdot\cos\widehat{ACB} "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
                r"Vậy $AB = %d\,\text{m}$."
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
        vat, chan = random.choice([("một ngọn tháp", "chân tháp"),
                                   ("một cột ăng-ten", "chân cột"),
                                   ("một toà nhà cao tầng", "chân toà nhà")])

        debai = (r"Để đo chiều cao $CH$ của %s mà không lên được đỉnh, người ta đứng tại điểm $A$ "
                 r"trên mặt đất đo được góc nâng tới đỉnh $C$ là $30^{\circ}$, rồi tiến thẳng về phía "
                 r"%s thêm $%d\,\text{m}$ tới điểm $B$ thì đo được góc nâng là $60^{\circ}$ "
                 r"(ba điểm $A$, $B$, $H$ thẳng hàng)." % (vat, chan, d))

        hoi_a = r"Tính số đo góc $\widehat{ACB}$."
        giai_a = (r"Góc $\widehat{CBH} = 60^{\circ}$ là góc ngoài tại $B$ của tam giác $ABC$ nên "
                  r"$\widehat{ACB} = 60^{\circ} - 30^{\circ} = 30^{\circ}$.")

        hoi_b = r"Tính độ dài $BC$."
        BC = d
        giai_b = (r"Tam giác $ABC$ có $\widehat{A} = \widehat{ACB} = 30^{\circ}$ nên cân tại $B$, "
                  r"do đó $BC = AB = %d\,\text{m}$." % d)

        hoi_c = r"Tính chiều cao $CH$."
        giai_c = (r"Tam giác $BCH$ vuông tại $H$ có $\widehat{CBH} = 60^{\circ}$ nên\\ "
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

        debai = r"Cho góc $\alpha = %s$. Xét tính đúng sai của các khẳng định sau:" % _goc(d)

        # a) NB - nhắc lại quan hệ giữa hai góc bù nhau
        y1 = [(r"{\True $\sin %s = \sin %s$}" % (_goc(bu), _goc(d)),
               r"Đúng. Hai góc bù nhau có sin bằng nhau."),
              (r"{$\sin %s = -\sin %s$}" % (_goc(bu), _goc(d)),
               r"Sai. Hai góc bù nhau có sin \textbf{bằng nhau}, không đối nhau.")]

        # b) TH - thay số: dùng quan hệ bù nhau rồi tra bảng
        y2 = [(r"{\True $\cos %s = %s$}" % (_goc(bu), _L(simplify(-cos_d))),
               r"Hai góc bù nhau có côsin đối nhau nên $\cos %s = -\cos %s = %s$."
               % (_goc(bu), _goc(d), _L(simplify(-cos_d)))),
              (r"{$\cos %s = %s$}" % (_goc(bu), _L(cos_d)),
               r"Sai. Đó là $\cos %s$; côsin của hai góc bù nhau \textbf{đối nhau} nên $\cos %s = %s$."
               % (_goc(d), _goc(bu), _L(simplify(-cos_d))))]

        # c) VD - phải dùng CẢ hai quan hệ ở trên, RỒI tra bảng giá trị
        #         của chính góc alpha đã cho mới ra được số
        # together: gộp thành MỘT phân số cho gọn, ví dụ
        # 1/2 - căn3/2  ->  (1 - căn3)/2  chứ không để rời hai phân số
        P = together(simplify(hang[1] - cos_d))     # sin(alpha) - cos(alpha)
        P_sai = together(simplify(hang[1] + cos_d))
        y3 = [(r"{\True Giá trị của biểu thức $P = \sin\left(180^{\circ} - \alpha\right) "
               r"+ \cos\left(180^{\circ} - \alpha\right)$ bằng $%s$}" % _gon(P),
               r"Ta có $\sin\left(180^{\circ}-\alpha\right) = \sin\alpha$ và "
               r"$\cos\left(180^{\circ}-\alpha\right) = -\cos\alpha$, nên "
               r"$P = \sin\alpha - \cos\alpha$.\\ "
               r"Với $\alpha = %s$ thì $P = %s - %s = %s$."
               % (_goc(d), _L(hang[1]), _L(cos_d), _gon(P))),
              (r"{Giá trị của biểu thức $P = \sin\left(180^{\circ} - \alpha\right) "
               r"+ \cos\left(180^{\circ} - \alpha\right)$ bằng $%s$}" % _gon(P_sai),
               r"Sai. Đó là $\sin\alpha + \cos\alpha$; quên rằng "
               r"$\cos\left(180^{\circ}-\alpha\right) = \textbf{--}\cos\alpha$, "
               r"nên $P = \sin\alpha - \cos\alpha = %s$." % _gon(P))]

        # d) VDC - đổi sang một góc tù chưa biết: phải dùng hệ thức cơ bản
        #          VÀ xét dấu của côsin trên khoảng góc tù
        y4 = [(r"{\True Nếu $90^{\circ} < \beta < 180^{\circ}$ và $\sin\beta = \dfrac{%d}{%d}$ "
               r"thì $\cos\beta = -\dfrac{%d}{%d}$}" % (doi, huyen, ke, huyen),
               r"Từ $\sin^{2}\beta + \cos^{2}\beta = 1$ suy ra "
               r"$\cos^{2}\beta = 1 - \left(\dfrac{%d}{%d}\right)^{2} = \dfrac{%d}{%d}$, "
               r"nên $\cos\beta = \pm\dfrac{%d}{%d}$.\\ "
               r"Vì $90^{\circ} < \beta < 180^{\circ}$ nên $\beta$ là góc tù, côsin \textbf{âm}, "
               r"do đó $\cos\beta = -\dfrac{%d}{%d}$."
               % (doi, huyen, ke * ke, huyen * huyen, ke, huyen, ke, huyen)),
              (r"{Nếu $90^{\circ} < \beta < 180^{\circ}$ và $\sin\beta = \dfrac{%d}{%d}$ "
               r"thì $\cos\beta = \dfrac{%d}{%d}$}" % (doi, huyen, ke, huyen),
               r"Sai ở \textbf{dấu}. Hệ thức cơ bản cho $\cos\beta = \pm\dfrac{%d}{%d}$, "
               r"mà góc tù có côsin âm nên $\cos\beta = -\dfrac{%d}{%d}$."
               % (ke, huyen, ke, huyen))]

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

        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$, $\widehat{A} = %s$. "
                 r"Xét tính đúng sai của các khẳng định sau:" % (b, c, _goc(A)))

        # a) NB - nhắc lại định lí côsin
        y1 = [(r"{\True $BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A$}",
               r"Đúng. Đây chính là định lí côsin."),
              (r"{$BC^{2} = AC^{2} + AB^{2} + 2\cdot AC\cdot AB\cdot\cos A$}",
               r"Sai. Định lí côsin mang dấu \textbf{trừ} trước số hạng cuối.")]

        # b) TH - thay số vào đúng công thức vừa nhắc ở ý a)
        y2 = [(r"{\True $BC = %d$}" % a,
               r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$ nên $BC = %d$."
               % (b, c, b, c, _L(cos_A), a2, a)),
              (r"{$BC = %d$}" % (b + c),
               r"Sai. $BC = %d$ chứ không phải tổng hai cạnh kia." % a)]

        # c) VD - phải có BC của ý b) rồi mới dùng được định lí sin
        y3 = [(r"{\True Bán kính đường tròn ngoại tiếp tam giác $ABC$ là $R = %s$}" % _L(R),
               r"Định lí sin: $\dfrac{BC}{\sin A} = 2R$ nên $R = \dfrac{BC}{2\sin A}$.\\ "
               r"Với $\sin %s = \dfrac{\sqrt{3}}{2}$ và $BC = %d$ thì "
               r"$R = \dfrac{%d}{2\cdot\dfrac{\sqrt{3}}{2}} = %s$."
               % (_goc(A), a, a, _L(R))),
              (r"{Bán kính đường tròn ngoại tiếp tam giác $ABC$ là $R = %s$}"
               % _L(simplify(R / 2)),
               r"Sai. Đó là $\dfrac{BC}{4\sin A}$; định lí sin cho $\dfrac{BC}{\sin A} = 2R$ "
               r"nên $R = \dfrac{BC}{2\sin A} = %s$." % _L(R))]

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
        y4 = [(r"{\True Gọi $AD$ là đường phân giác trong của góc $A$ $\left(D \in BC\right)$, "
               r"khi đó $AD = %s$}" % _L(AD),
               r"$AD$ là phân giác của góc $A$ nên nó chia góc $%s$ thành hai góc bằng nhau: "
               r"$\widehat{BAD} = \widehat{CAD} = %s$.\\ "
               r"Điểm $D$ nằm trên cạnh $BC$ nên tam giác $ABC$ được chia thành hai tam giác "
               r"$ABD$ và $ACD$, do đó $S_{ABD} + S_{ACD} = S_{ABC}$.\\ "
               r"Dùng công thức diện tích $S = \dfrac{1}{2}\cdot\text{cạnh}\cdot\text{cạnh}\cdot\sin(\text{góc xen giữa})$:\\ "
               r"$\dfrac{1}{2}\cdot %d\cdot AD\cdot\sin %s + \dfrac{1}{2}\cdot %d\cdot AD\cdot\sin %s "
               r"= \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s$.\\ "
               r"Tra bảng: $\sin %s = %s$ và $\sin %s = %s$, thay vào:\\ "
               r"$\dfrac{1}{2}\cdot %s\cdot AD\cdot\left(%d + %d\right) "
               r"= \dfrac{1}{2}\cdot %s\cdot %d$.\\ "
               r"Rút gọn được $AD = %s$."
               % (_goc(A), _goc(nua),
                  c, _goc(nua), b, _goc(nua), b, c, _goc(A),
                  _goc(nua), _L(sin_nua), _goc(A), _L(sin_A),
                  _L(sin_nua), c, b, _L(sin_A), b * c,
                  _L(AD))),
              (r"{Gọi $AD$ là đường phân giác trong của góc $A$ $\left(D \in BC\right)$, "
               r"khi đó $AD = %s$}" % _L(AD_sai),
               r"Sai vì lấy nhầm sin của \textbf{nửa góc} $A$. "
               r"Phân giác chia góc $%s$ thành hai góc $%s$, mà $\sin %s = %s$ "
               r"(chứ không phải $%s$).\\ "
               r"Thay đúng vào $S_{ABD} + S_{ACD} = S_{ABC}$ sẽ được $AD = %s$."
               % (_goc(A), _goc(nua), _goc(nua), _L(sin_nua),
                  _L(sin_nua_lan), _L(AD)))]

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

        debai = (r"Để đo khoảng cách giữa hai điểm $A$ và $B$ bị ngăn bởi một đầm lầy, người ta "
                 r"chọn điểm $C$ đo trực tiếp được và đo được $CA = %d\,\text{m}$, $CB = %d\,\text{m}$, "
                 r"$\widehat{ACB} = %s$. Tính khoảng cách $AB$ (đơn vị mét)."
                 % (b, c, _goc(A)))
        giai = (r"Định lí côsin: $AB^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$, "
                r"suy ra $AB = %d\,\text{m}$." % (b, c, b, c, latex(cos_A), d2, d))
        ds = [str(b + c), str(d + 2), str(d - 2)]
        ds = [x for x in dict.fromkeys(ds) if x != str(d)][:3]
        while len(ds) < 3:
            ds.append(str(d + len(ds) + 5))
        cauTN += MC_SA_answer_const(debai, str(d), ds, giai, 0, 0, dang)
    return cauTN



_BOI_CANH_VAT_CAN = [
    (r"Hai đầu $A$, $B$ của một đường hầm xuyên qua một ngọn núi không đo trực tiếp "
     r"được. Từ một điểm $C$ ở chân núi, người ta đo được", r"chiều dài đường hầm $AB$"),
    (r"Hai điểm $A$, $B$ nằm ở hai bên bờ một hồ nước. Từ một điểm $C$ trên bờ, người "
     r"ta đo được", r"khoảng cách $AB$"),
    (r"Một ngôi nhà che khuất tầm nhìn giữa hai cột điện $A$ và $B$. Từ vị trí $C$, "
     r"một kĩ sư đo được", r"khoảng cách giữa hai cột điện"),
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
        debai = (mo + r" $CA = %d\,\text{m}$, $CB = %d\,\text{m}$ và $\widehat{ACB} = %s$. "
                 r"Tính %s (đơn vị mét)." % (B_, C_, _goc(A), hoi))
        giai = (r"Trong tam giác $ABC$, theo định lí côsin:\\ "
                r"$AB^{2} = CA^{2} + CB^{2} - 2\cdot CA\cdot CB\cdot\cos %s "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
                r"Suy ra $AB = %d\,\text{m}$."
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
        debai = (r"Để đo khoảng cách từ điểm $A$ trên bờ sông đến gốc cây $B$ ở bờ bên kia, "
                 r"người ta chọn điểm $C$ cùng bờ với $A$ và đo được $AC = %d\,\text{m}$, "
                 r"$\widehat{BAC} = %s$, $\widehat{BCA} = %s$. Tính khoảng cách $AB$ (đơn vị "
                 r"mét, làm tròn đến hàng phần mười)." % (d, _goc(al), _goc(ga)))
        giai = (r"Trong tam giác $ABC$: $\widehat{ABC} = 180^{\circ} - %s - %s = %s$.\\ "
                r"Theo định lí sin: $\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B}$ nên\\ "
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

    debai = (r"Cho góc $\alpha$ với $0^{\circ} \le \alpha \le 180^{\circ}$. "
             r"Khẳng định nào sau đây \textbf{có thể} xảy ra?")

    cauTN = ''
    for p, q, r1, r2, ten, nguyen in gt:
        dung = r"$\cos\alpha = -\dfrac{%d}{%d}$" % (p, q)
        giai = (r"Với $0^{\circ} \le \alpha \le 180^{\circ}$, điểm $M$ chạy trên nửa đường tròn "
                r"đơn vị nằm \textbf{phía trên} trục hoành, nên\\ "
                r"$\sin\alpha = y_{0} \ge 0$ và $-1 \le \cos\alpha = x_{0} \le 1$.\\ "
                r"$\bullet$ $\sin\alpha = -\dfrac{%d}{%d} < 0$: loại, vì sin của góc từ "
                r"$0^{\circ}$ đến $180^{\circ}$ không âm.\\ "
                r"$\bullet$ $%s\alpha = %d$: loại, vì $\left| %d \right| > 1$.\\ "
                r"$\bullet$ $\cos\alpha = \dfrac{%d}{%d} > 1$: loại.\\ "
                r"$\bullet$ $\cos\alpha = -\dfrac{%d}{%d}$: nhận, vì côsin của góc tù mang dấu âm "
                r"và $\dfrac{%d}{%d} \le 1$."
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


def _hinh_cu_lao(c, A, B):
    """Hình con sông và cù lao; nhãn cạnh AB và hai góc lấy theo số liệu đề."""
    return r"""\begin{tikzpicture}[scale=.7, font=\footnotesize, line join = round, line cap = round,>=stealth]
\clip (-4.39,3.2) rectangle (4,-4);
\draw[pattern=north east lines,opacity=0.3] plot[smooth] coordinates{(-4.39,1.43)(-2.43,1.46) (-1.48,1.67)(1.43,2.12)(2.01,2.09)(4,1.64) (4.1,-1.06)(3.02,-0.77)(1.85,-1.38)(0.95,-1.48)(0.13,-1.72)(-1.48,-1.67)(-2.46,-1.51)(-3.57,-0.98)(-4.37,-1.08)};
\draw[opacity=3] plot[smooth] coordinates{(-4.39,1.43)(-2.43,1.46) (-1.48,1.67)(1.43,2.12)(2.01,2.09)(4,1.64) (4.1,-1.06)(3.02,-0.77)(1.85,-1.38)(0.95,-1.48)(0.13,-1.72)(-1.48,-1.67)(-2.46,-1.51)(-3.57,-0.98)(-4.37,-1.08)};
\draw[fill=white] plot[smooth  cycle] coordinates{(-2.75,-0.08)(-1.83,0.32) (-0.03,0.42) (1,0) (0.24,-0.48)(-0.58,-0.79)(-1.38,-0.77)(-1.91,-0.71)};
\draw[fill=black!70]  plot[smooth  cycle] coordinates{(-2.14,0.58)(-2.09,0.24)(-2.33,-0.13) (-1.19,-0.13) (-1.38,-0.13) (-1.69,0.21)(-1.75,0.53)};
\draw[fill=blue!30]  plot[smooth  cycle] coordinates{(-1.75,0.53)(-1.46,0.79) (-1.01,0.58) (-1.08,1.06) (-0.64,1.08)(-0.93,1.59)(-0.53,1.85)(-0.93,2.2)(-1.38,2.7)(-2.04,3.18)(-2.49,2.91)(-3.07,2.91)(-3.2,2.22)(-3.73,1.96)(-3.1,1.3)(-3.31,1.01)(-2.83,1.01)(-2.99,0.69)(-2.14,0.58)};
\tkzDefPoints{-1.38/-0.13/C,-2/-3/B,3/-2/A}
\tkzDrawPoints[fill=black](A,B,C)
\tkzDrawPolygon[very thick](A,B,C)
\tkzDefMidPoint(A,B) \tkzGetPoint{M}
\node at (M) [below] {$ %d $ };
\tkzLabelPoints[below](A,B)
\tkzLabelPoints[above right](C)
\tkzMarkAngles[size=.7cm,arc=l,mark=|](C,A,B)
\tkzMarkAngles[size=.5cm,arc=l,mark=||](A,B,C)
\tkzLabelAngles[left=.8cm,pos=0.4,rotate=-20](B,A,C){\footnotesize$%d ^{\circ}$}
\tkzLabelAngles[right=.5cm,pos=0.3](A,B,C){$%d ^{\circ}$}
\end{tikzpicture}""" % (c, A, B)


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
        debai = (r"Trên mặt phẳng toạ độ $Oxy$, lấy điểm $M\left( x_{0}; y_{0} \right)$ thuộc nửa "
                 r"đường tròn đơn vị như hình bên. Lấy điểm $N$ đối xứng với $M$ qua trục $Oy$. "
                 r"Xác định $%s\widehat{xON}$." % ten)
        giai = (r"$N$ đối xứng với $M$ qua trục $Oy$ nên $N\left( -x_{0}; y_{0} \right)$, "
                r"tức $\widehat{xON} = 180^{\circ} - \widehat{xOM}$.\\ "
                r"Theo định nghĩa giá trị lượng giác của một góc từ $0^{\circ}$ đến $180^{\circ}$:\\ "
                r"$\sin\widehat{xON} = y_{0}$, $\cos\widehat{xON} = -x_{0}$, "
                r"$\tan\widehat{xON} = \dfrac{y_{0}}{-x_{0}} = -\dfrac{y_{0}}{x_{0}}$, "
                r"$\cot\widehat{xON} = \dfrac{-x_{0}}{y_{0}} = -\dfrac{x_{0}}{y_{0}}$.\\ "
                r"Vậy $%s\widehat{xON} = %s$." % (ten, GIA_TRI[ten]))
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
        giai = (r"Dùng máy tính cầm tay (chế độ $\mathrm{DEG}$):\\ "
                r"$\sin %d^{\circ} \approx %s$, $\cos %d^{\circ} \approx %s$, "
                r"$\tan %d^{\circ} \approx %s$, $\cot %d^{\circ} \approx %s$.\\ "
                r"Vậy chỉ có $%s %d^{\circ} \approx %s$ là đúng."
                % (goc, _xx(val[r"\sin"]), goc, _xx(val[r"\cos"]),
                   goc, _xx(val[r"\tan"]), goc, _xx(val[r"\cot"]), ten, goc, so))
        ds = _ba_nhieu(dung, [r"$%s %d^{\circ} \approx %s$" % (k, goc, so)
                              for k in TEN if k != ten])
        cauTN += MC_SA_answer_text(debai_MTCT(), dung, ds, giai, 0, 0, dang)
    return cauTN


def debai_MTCT():
    return r"Trong các khẳng định sau, khẳng định nào \textbf{đúng}?"



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
        giai = (r"Định lí sin trong tam giác $ABC$: $\dfrac{BC}{\sin A} = 2R$, "
                r"suy ra $R = \dfrac{BC}{2\sin A}$.\\ "
                r"Với $BC = %d$ và $\sin %d^{\circ} \approx %s$ thì "
                r"$R \approx \dfrac{%d}{2\cdot %s} \approx %s$."
                % (a, A, _xx(sinA, 4), a, _xx(sinA, 4), _xx(R)))
        ds = _ba_nhieu(
            dung,
            [r"$R \approx %s$" % _xx(a / sinA),          # quên chia 2
             r"$R \approx %s$" % _xx(a * sinA / 2),      # nhân thay vì chia
             r"$R \approx %s$" % _xx(2 * sinA / a)],     # lộn ngược phân số
            buoc=lambda k: r"$R \approx %s$" % _xx(R + k))
        debai = (r"Cho tam giác $ABC$ có $\widehat{A} = %d^{\circ}$ và $BC = %d$. "
                 r"Tính bán kính $R$ của đường tròn ngoại tiếp tam giác $ABC$ "
                 r"(làm tròn đến hàng phần trăm)." % (A, a))
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

        debai = (r"Để đo khoảng cách từ một điểm $A$ trên bờ sông đến gốc cây $C$ trên cù lao "
                 r"giữa sông, người ta chọn một điểm $B$ cùng ở trên bờ với $A$ sao cho từ $A$ "
                 r"và $B$ đều nhìn thấy điểm $C$. Đo được $AB = %d\,\text{m}$, "
                 r"$\widehat{CAB} = %d^{\circ}$ và $\widehat{CBA} = %d^{\circ}$." % (c, A, B))
        ds_abcd = [
            (r"Tính số đo góc $\widehat{ACB}$.",
             r"%d^{\circ}" % C,
             r"Tổng ba góc trong tam giác $ABC$ bằng $180^{\circ}$ nên\\ "
             r"$\widehat{ACB} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$."
             % (A, B, C)),
            (r"Tính khoảng cách từ $A$ đến gốc cây $C$ (làm tròn đến hàng phần trăm).",
             r"%s\,\text{m}" % _xx(AC),
             r"Áp dụng định lí sin trong tam giác $ABC$:\\ "
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

        debai = f"""Trong mặt phẳng toạ độ $Oxy$, lấy điểm $M {M_toa_do}$ thuộc nửa đường tròn đơn vị. Tính ${gtlg} \\widehat{{ xOM }}$.
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
            Điểm $M(x_M; y_M)$ thuộc nửa đường tròn đơn vị (bán kính $R=1$) nên ta có:
            \\[\\cos \\widehat{{ xOM }} = x_M \\quad \\text{{và}} \\quad \\sin \\widehat{{ xOM }} = y_M\\]
            Từ tọa độ điểm $M {M_toa_do}$, ta có:
            \\begin{{itemize}}
                \\item $x_M = {x_coord}$
                \\item $y_M = {y_coord}$
            \\end{{itemize}}
            Giá trị cần tìm là ${gtlg} \\widehat{{ xOM }}$.
            \\begin{{itemize}}
                \\item Nếu cần tính $\\cos \\widehat{{ xOM }}$, ta lấy $x_M = {dapso_cos}$.
                \\item Nếu cần tính $\\sin \\widehat{{ xOM }}$, ta lấy $y_M = {dapso_sin}$.
            \\end{{itemize}}
            Do đó, ${gtlg} \\widehat{{ xOM }} = {dapso}$.
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
        debai = f"""Trong mặt phẳng toạ độ $Oxy$, lấy điểm $M$ thuộc nửa đường tròn đơn vị.
        Biết $\\sin \\widehat{{ xOM }} = {sin_val}$ và $\\cos \\widehat{{ xOM }} = {cos_val}$. Tìm toạ độ điểm $M$.
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
            Điểm $M(x_M; y_M)$ thuộc nửa đường tròn đơn vị (bán kính $R=1$).
            Theo định nghĩa, toạ độ điểm $M$ trên nửa đường tròn đơn vị là:
            \\[x_M = \\cos \\widehat{{ xOM }} \\quad \\text{{và}} \\quad y_M = \\sin \\widehat{{ xOM }}\\]
            Theo đề bài, ta có:
            \\begin{{itemize}}
                \\item $x_M = \\cos \\widehat{{ xOM }} = {cos_val}$
                \\item $y_M = \\sin \\widehat{{ xOM }} = {sin_val}$
            \\end{{itemize}}
            Vậy toạ độ điểm $M$ là $M \\left( {cos_val}; {sin_val} \\right)$, tức là ${dapso}$.
            (Vì $M$ thuộc nửa đường tròn đơn vị, nên $\\sin \\widehat{{ xOM }} = y_M$ luôn dương.)
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
        Cho tam giác $ABC$ có $\\widehat{{ C }} = {C} ^\\circ$ và các cạnh $AC = {a}$, $BC = {b}$. Tính độ dài cạnh $AB$.
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
        Áp dụng Định lí Cosin cho tam giác $ABC$ để tính độ dài cạnh $AB$ (tức cạnh $c$) với góc $\\widehat{{ C }}$ và hai cạnh $AC=b={a}$, $BC=a={b}$.
        Công thức: $c^2 = a^2 + b^2 - 2ab \\cos C$.
        Với $a={b}$, $b={a}$, $C = {C}^\\circ$, ta có:
        \\[AB^2 = {b}^2 + {a}^2 - 2 \\cdot {b} \\cdot {a} \\cdot \\cos({C}^\\circ)\\]
        \\[AB^2 = {b ** 2 + a ** 2} - {2 * a * b} \\cdot \\cos({C}^\\circ)\\]
        Sử dụng $\\cos({C}^\\circ) \\approx {cos_C_giai}$, ta tính được:
        \\[AB^2 \\approx {c_square_giai}\\]
        \\[AB = \\sqrt{{AB^2}} \\approx {c}\\]
        Vậy độ dài cạnh $AB$ xấp xỉ ${c}$.
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
        c = str(c_val).replace('.', ',')
        c_sai1 = str(c_sai1_val).replace('.', ',')
        c_sai2 = str(c_sai2_val).replace('.', ',')
        c_sai3 = str(c_sai3_val).replace('.', ',')

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
        Để đo khoảng cách từ $A$ đến $B$ ngang qua một đầm lầy, người ta chọn điểm $C$ như hình. Người ta đo được khoảng cách từ $A$ đến $C$ bằng ${b}$ m. Và biết rằng từ điểm $A$ nhìn hai điểm $B$ và $C$ dưới một góc bằng $ {A} ^\\circ$, từ điểm $C$ nhìn hai điểm $A$ và $B$ dưới một góc bằng $ {C} ^\\circ$. Tính khoảng cách từ $A$ đến $B$.
        """

        # 6. Định dạng đáp án và nhiễu (chỉ là giá trị số xấp xỉ)
        dapso = str(c)
        dsnhieu = [str(c_sai1), str(c_sai2), str(c_sai3)]

        # 7. Lời giải
        giai = f"""
        Trong tam giác $ABC$, ta đã biết hai góc $\\widehat{{A}} = {A}^\\circ$, $\\widehat{{C}} = {C}^\\circ$ và cạnh $b = AC = {b}$ m.
        Khoảng cách từ $A$ đến $B$ là độ dài cạnh $c=AB$.

        \\textbf{{Bước 1: Tính góc $\\widehat{{B}}$}}
        Tổng ba góc trong tam giác là $180^\\circ$, nên:
        \\[\\widehat{{B}} = 180^\\circ - \\widehat{{A}} - \\widehat{{C}} = 180^\\circ - {A}^\\circ - {C}^\\circ = {B}^\\circ\\]

        \\textbf{{Bước 2: Áp dụng Định lí Sin}}
        Ta có tỉ lệ:
        \\[\\dfrac{{AB}}{{\\sin C}} = \\dfrac{{AC}}{{\\sin B}}\\]
        Thay các giá trị đã biết ($AC=b={b}$, $\\widehat{{B}}={B}^\\circ$, $\\widehat{{C}}={C}^\\circ$):
        \\[AB = \\dfrac{{AC \\cdot \\sin C}}{{\\sin B}} = \\dfrac{{{b} \\cdot \\sin({C}^\\circ)}}{{\\sin({B}^\\circ)}}\\]

        \\textbf{{Bước 3: Tính toán}}
        \\[AB \\approx \\dfrac{{{b} \\cdot {round(math.sin(C_rad), 4)}}}{{{round(math.sin(B_rad), 4)}}} \\approx {c} \\mathrm{{~m}}\\]
        Vậy khoảng cách từ $A$ đến $B$ xấp xỉ ${c}$ m.
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
            return str(round(x, 2)).replace('.', ',')

        a, b, c = f(a_val), f(b_val), f(c_val)
        b_square = f(b_square_val)
        cos_B_str = f(cos_B)
        t1_h_str, t2_h_str = f(t1_h), f(t2_h)

        z_sai1 = f(math.sqrt(a_val ** 2 + c_val ** 2))
        z_sai2 = f(math.sqrt(a_val ** 2 + c_val ** 2 + 2 * a_val * c_val * cos_B))
        z_sai3 = f(math.sqrt(a_val ** 2 + c_val ** 2 - a_val * c_val * cos_B))

        debai = f"""
        Một tàu xuất phát từ bãi biển $A$, chạy theo hướng $N {goc1}^\\circ E$ với vận tốc ${vt1}$ km/h. 
        Sau khi đi được ${t1}$ phút đến vị trí $B$, tàu chuyển sang hướng $S {goc2}^\\circ E$ 
        và chạy với tốc độ ${vt2}$ km/h trong ${t2}$ phút nữa thì đến đảo $C$. 
        Hỏi tàu cách vị trí xuất phát xấp xỉ bao nhiêu kilômet?
        """

        giai = f"""
        Quỹ đạo chuyển động của tàu tạo thành tam giác $ABC$ với:
        $A$ là vị trí xuất phát, $B$ là vị trí đổi hướng, và $C$ là đảo.
        Khoảng cách cần tìm là $AC$ (cạnh $b$).

        \\textbf{{Bước 1. Tính độ dài các cạnh}}
        \\begin{{itemize}}
        \\item $AB = c = {vt1} \\cdot {t1_h_str} = {c} \\mathrm{{~(km)}}$
        \\item $BC = a = {vt2} \\cdot {t2_h_str} = {a} \\mathrm{{~(km)}}$
        \\end{{itemize}}

        \\textbf{{Bước 2. Xác định góc $\\widehat{{ABC}}$}}
        Hai hướng $N{goc1}^\\circ E$ và $S{goc2}^\\circ E$ cùng nghiêng về phía Đông,
        nên góc giữa hai hướng bằng tổng hai góc phương vị:
        \\[\\widehat{{ABC}} = {goc1}^\\circ + {goc2}^\\circ = {Goc_B_deg}^\\circ\\]

        \\textbf{{Bước 3. Áp dụng định lí Cosin}}
        \\[AC^2 = AB^2 + BC^2 - 2AB \\cdot BC \\cdot \\cos(\\widehat{{ABC}})\\]
        Thay số:
        \\[AC^2 = {c}^2 + {a}^2 - 2 \\cdot {c} \\cdot {a} \\cdot \\cos({Goc_B_deg}^\\circ)\\]
        Với $\\cos({Goc_B_deg}^\\circ) \\approx {cos_B_str}$, ta được:
        \\[AC^2 \\approx {b_square}\\]
        \\[AC = \\sqrt{{AC^2}} \\approx {b} \\mathrm{{~(km)}}\\]

        Vậy tàu cách vị trí xuất phát xấp xỉ ${b}$ km.
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
        return s.replace('.', ',')

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
        Một tàu xuất phát từ bãi biển $A$, chạy theo hướng $N {goc1_f}^\\circ E$ với vận tốc ${vt1}$ km/h. 
        Sau khi đi được ${t1}$ phút đến vị trí $B$, tàu chuyển sang hướng $S {goc2_f}^\\circ E$ 
        và chạy với tốc độ ${vt2}$ km/h trong ${t2}$ phút nữa thì đến đảo $C$. 
        Xác định tính đúng/sai của các phát biểu sau:
        """

        # Lời giải chi tiết (không có dấu chấm cuối)
        giai_chung = f"""
        \\textbf{{Phân tích bài toán:}} Quỹ đạo chuyển động của tàu tạo thành tam giác $ABC$.
        $AB = c = {vt1} \\cdot \\frac{{{t1}}}{{60}} = {c}$ km 
        $BC = a = {vt2} \\cdot \\frac{{{t2}}}{{60}} = {a}$ km
        Góc $\\widehat{{ABC}} = {goc1_f}^\\circ + {goc2_f}^\\circ = {goc_B_dung}^\\circ$
        Áp dụng Định lí Cosin: $AC = b \\approx {b}$ km
        Hướng từ $A$ đến $C$ là ${Huong_AC_str}$
        """

        # a) Độ dài AB hoặc BC
        ds_a = [
            (f"{{\\True Độ dài đoạn $AB$ là ${c}$ km}}", f"Độ dài $AB = {c}$ km. Phát biểu \\textbf{{Đúng}}. {giai_chung}"),
            (f"{{Độ dài đoạn $AB$ là ${a}$ km}}",
             f"Độ dài $AB = {c}$ km $\\ne {a}$ km. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
            (f"{{\\True Độ dài đoạn $BC$ là ${a}$ km}}", f"Độ dài $BC = {a}$ km. Phát biểu \\textbf{{Đúng}}. {giai_chung}"),
            (f"{{Độ dài đoạn $BC$ là ${b}$ km}}",
             f"Độ dài $BC = {a}$ km $\\ne {b}$ km. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
        ]

        # b) Góc ABC
        ds_b = [
            (f"{{\\True Góc $\\widehat{{ABC}}$ bằng ${goc_B_dung}^\\circ$}}",
             f"Góc $\\widehat{{ABC}} = {goc_B_dung}^\\circ$. Phát biểu \\textbf{{Đúng}}. {giai_chung}"),
            (f"{{Góc $\\widehat{{ABC}}$ bằng ${goc_B_sai}^\\circ$}}",
             f"Góc $\\widehat{{ABC}} = {goc_B_dung}^\\circ \\ne {goc_B_sai}^\\circ$. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
            (f"{{Góc $\\widehat{{ABC}}$ bằng ${goc1_f}^\\circ$}}",
             f"Góc $\\widehat{{ABC}} = {goc_B_dung}^\\circ \\ne {goc1_f}^\\circ$. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
        ]

        # CÂU C: Khoảng cách từ A đến C
        ds_c = [
            (f"{{\\True Khoảng cách từ $A$ đến $C$ xấp xỉ ${b}$ km}}",
             f"Áp dụng Định lí Cosin, $AC = b \\approx {b}$ km. Phát biểu \\textbf{{Đúng}}. {giai_chung}"),
            (f"{{Khoảng cách từ $A$ đến $C$ xấp xỉ ${a}$ km}}",
             f"Áp dụng Định lí Cosin, $AC = b \\approx {b}$ km $\\ne {a}$ km. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
            (f"{{Khoảng cách từ $A$ đến $C$ xấp xỉ ${c}$ km}}",
             f"Áp dụng Định lí Cosin, $AC = b \\approx {b}$ km $\\ne {c}$ km. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
        ]

        # CÂU D: Hướng đi từ A đến C
        ds_d = [
            (f"{{\\True Muốn đi thẳng từ $A$ đến $C$ thì đi theo hướng ${Huong_AC_str}$}}",
             f"Hướng $AC$ là ${Huong_AC_str}$. Phát biểu \\textbf{{Đúng}}. {giai_chung}"),
            (f"{{Muốn đi thẳng từ $A$ đến $C$ thì đi theo hướng ${Huong_AC_str_sai}$}}",
             f"Hướng $AC$ là ${Huong_AC_str} \\ne {Huong_AC_str_sai}$. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
            (f"{{Muốn đi thẳng từ $A$ đến $C$ thì đi theo hướng $N {goc1_f}^\\circ E$}}",
             f"Hướng $AC$ là ${Huong_AC_str} \\ne N {goc1_f}^\\circ E$. Phát biểu \\textbf{{Sai}}. {giai_chung}"),
        ]

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
            giai = (r"Từ $\sin^{2}\alpha + \cos^{2}\alpha = 1$ suy ra "
                    r"$\cos^{2}\alpha = 1 - \left(\dfrac{%d}{%d}\right)^{2} "
                    r"= \dfrac{%d}{%d}$, nên $\cos\alpha = \pm\dfrac{%d}{%d}$.\\ "
                    r"Vì %s nên $\alpha$ là góc %s, côsin mang dấu %s. "
                    r"Vậy $\cos\alpha = %s\dfrac{%d}{%d}$."
                    % (doi, huyen, ke * ke, huyen * huyen, ke, huyen,
                       khoang, "tù" if tu else "nhọn",
                       "âm" if tu else "dương", dau, ke, huyen))
            nhieu = [r"%s\dfrac{%d}{%d}" % ("" if tu else "-", ke, huyen),
                     r"\dfrac{%d}{%d}" % (doi, huyen),
                     r"%s\dfrac{%d}{%d}" % (dau, doi, ke),
                     r"\dfrac{%d}{%d}" % (ke, doi)]
        else:
            cho = r"\cos\alpha = %s\dfrac{%d}{%d}" % (dau, ke, huyen)
            hoi, dapso = r"\sin\alpha", r"\dfrac{%d}{%d}" % (doi, huyen)
            giai = (r"Từ $\sin^{2}\alpha + \cos^{2}\alpha = 1$ suy ra "
                    r"$\sin^{2}\alpha = 1 - \left(\dfrac{%d}{%d}\right)^{2} "
                    r"= \dfrac{%d}{%d}$, nên $\sin\alpha = \pm\dfrac{%d}{%d}$.\\ "
                    r"Với $0^{\circ} < \alpha < 180^{\circ}$ thì $\sin\alpha$ luôn "
                    r"\textbf{dương}. Vậy $\sin\alpha = \dfrac{%d}{%d}$."
                    % (ke, huyen, doi * doi, huyen * huyen, doi, huyen, doi, huyen))
            nhieu = [r"-\dfrac{%d}{%d}" % (doi, huyen),
                     r"%s\dfrac{%d}{%d}" % (dau, ke, huyen),
                     r"\dfrac{%d}{%d}" % (doi, ke),
                     r"\dfrac{%d}{%d}" % (ke, doi)]

        debai = (r"Cho góc $\alpha$ thoả mãn $%s$ và %s. Tính $%s$."
                 % (cho, khoang, hoi))
        dung = "$%s$" % dapso
        ds = _ba_nhieu(dung, ["$%s$" % x for x in nhieu],
                       buoc=lambda k: r"$\dfrac{%d}{%d}$" % (k, huyen + k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH030_SA_A_01(socau, dang=2):
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
        debai = (r"Cho góc $\alpha$ có $\cos\alpha = %s$ và %s. "
                 r"Tính $\sin\alpha$." % (_xx(cos_val), khoang))
        giai = (r"Áp dụng $\sin^{2}\alpha + \cos^{2}\alpha = 1$:\\ "
                r"$\sin^{2}\alpha = 1 - \left(%s\right)^{2} = %s$, "
                r"nên $\sin\alpha = \pm %s$.\\ "
                r"Với $0^{\circ} < \alpha < 180^{\circ}$ thì $\sin\alpha$ luôn dương, "
                r"vậy $\sin\alpha = %s$."
                % (_xx(cos_val), _xx(sin_val * sin_val, 4), _xx(sin_val), _xx(sin_val)))
        dung = _xx(sin_val)
        ds = _ba_nhieu(dung, [_xx(-sin_val), _xx(cos_val), _xx(abs(cos_val))],
                       buoc=lambda k: _xx(sin_val + k / 10.0))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_SA_B_01(socau, dang=2):
    """Trả lời ngắn: rút gọn biểu thức bằng hệ thức cơ bản và quan hệ hai góc bù."""
    gt = []
    while len(gt) < socau:
        v = (random.randint(2, 9), random.randint(2, 9))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for m, n in gt:
        dapso = m + n
        debai = (r"Cho góc $\alpha$ với $0^{\circ} < \alpha < 90^{\circ}$. "
                 r"Tính giá trị của biểu thức\\ "
                 r"$P = %d\left[\sin^{2}\left(180^{\circ} - \alpha\right) "
                 r"+ \cos^{2}\left(180^{\circ} - \alpha\right)\right] "
                 r"+ %d\cdot\tan\alpha\cdot\cot\alpha$." % (m, n))
        giai = (r"Đặt $\beta = 180^{\circ} - \alpha$. Hệ thức lượng giác cơ bản đúng với "
                r"mọi góc nên\\ "
                r"$\sin^{2}\beta + \cos^{2}\beta = 1$, tức phần trong ngoặc vuông bằng $1$.\\ "
                r"Mặt khác $\tan\alpha\cdot\cot\alpha = 1$ với mọi $\alpha$ mà hai giá trị "
                r"này xác định.\\ "
                r"Vậy $P = %d\cdot 1 + %d\cdot 1 = %d$." % (m, n, dapso))
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $AC = %d$, $AB = %d$. "
                 r"Tính $\cos %s$." % (a, b, c, dinh))
        giai = (r"Định lí côsin viết cho góc $%s$:\\ "
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$, $BC = %d$. "
                 r"Tính số đo góc $A$ (đơn vị độ)." % (b, c, a))
        cos_A = Rational(b * b + c * c - a * a, 2 * b * c)
        giai = (r"Định lí côsin: $\cos A = \dfrac{AC^{2} + AB^{2} - BC^{2}}{2\cdot AC\cdot AB} "
                r"= \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$.\\ "
                r"Tra bảng giá trị lượng giác, góc có côsin bằng $%s$ là $%s$."
                % (b, c, a, b, c, _L(cos_A), _L(cos_A), _goc(goc)))
        dung = str(goc)
        ds = _ba_nhieu(dung, [str(180 - goc), str(goc // 2), str(goc + 30)],
                       buoc=lambda k: str(goc + 10 * (k + 1)))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_SA_B_01(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$. "
                 r"Tính độ dài cạnh $AC$ (làm tròn đến hàng phần trăm)."
                 % (a, _goc(A), _goc(B)))
        giai = (r"Định lí sin: $\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B}$, "
                r"suy ra $AC = \dfrac{BC\cdot\sin B}{\sin A}$.\\ "
                r"Với $\sin %s = %s$ và $\sin %s = %s$ thì "
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Tính diện tích tam giác $ABC$." % (a, b, c))
        giai = (r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d$.\\ "
                r"Công thức Heron:\\ "
                r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} "
                r"= \sqrt{%d\cdot %d\cdot %d\cdot %d} = \sqrt{%d} = %d$."
                % (a, b, c, p, p, p - a, p - b, p - c, S * S, S))
        dung = "$%d$" % S
        ds = _ba_nhieu(dung, ["$%d$" % (2 * S), "$%d$" % p, "$%d$" % (S + p)],
                       buoc=lambda k: "$%d$" % (S + 2 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH034_SA_B_01(socau, dang=2):
    """Trả lời ngắn: bán kính đường tròn nội tiếp, dùng S = p.r."""
    gt = []
    while len(gt) < socau:
        v = random.choice(BANG_HERON)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a, b, c, S, p, r in gt:
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Tính bán kính $r$ của đường tròn nội tiếp tam giác $ABC$."
                 % (a, b, c))
        giai = (r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d$.\\ "
                r"Heron: $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$.\\ "
                r"Mà $S = p\cdot r$ nên $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$."
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
        that = "vuông" if abs(lon - 90) < 1e-9 else ("tù" if lon > 90 else "nhọn")
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Tam giác $ABC$ là tam giác gì?" % (a, b, c))
        giai = (r"Cạnh lớn nhất là $%d$, nên góc lớn nhất là góc đối diện cạnh ấy. "
                r"Gọi góc đó là $\varphi$, định lí côsin cho\\ "
                r"$\cos\varphi = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$.\\ "
                r"Côsin của góc lớn nhất %s nên tam giác %s."
                % (canh[2], canh[0], canh[1], canh[2], canh[0], canh[1],
                   _L(Rational(canh[0] ** 2 + canh[1] ** 2 - canh[2] ** 2,
                               2 * canh[0] * canh[1])),
                   {"nhọn": "dương", "vuông": "bằng $0$", "tù": "âm"}[that],
                   {"nhọn": "có ba góc nhọn", "vuông": "vuông", "tù": "tù"}[that]))
        dung = "tam giác %s" % that
        ds = _ba_nhieu(dung, ["tam giác %s" % x for x in ("nhọn", "vuông", "tù", "đều")
                              if x != that],
                       buoc=lambda k: "tam giác cân")
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_VD036_SA_B_01(socau, dang=2):
    """Trả lời ngắn (thực tế): tính diện tích mảnh đất tam giác bằng Heron."""
    NOI = [("một mảnh vườn", "mảnh vườn"), ("một thửa ruộng", "thửa ruộng"),
           ("một khu đất", "khu đất")]
    gt = []
    while len(gt) < socau:
        v = random.choice(BANG_HERON)
        if v[3] >= 20 and v not in gt:      # dien tich du lon cho hop ly thuc te
            gt.append(v)

    cauTN = ''
    for a, b, c, S, p, r in gt:
        ten, goi = random.choice(NOI)
        debai = (r"Người ta đo %s hình tam giác và được ba cạnh lần lượt là "
                 r"$%d\,\text{m}$, $%d\,\text{m}$ và $%d\,\text{m}$. "
                 r"Tính diện tích %s (đơn vị $\text{m}^{2}$)."
                 % (ten, a, b, c, goi))
        giai = (r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d\,\text{(m)}$.\\ "
                r"Theo công thức Heron:\\ "
                r"$S = \sqrt{p\left(p-a\right)\left(p-b\right)\left(p-c\right)} "
                r"= \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d\,\text{(m}^{2}\text{)}$."
                % (a, b, c, p, p, p - a, p - b, p - c, S))
        dung = str(S)
        ds = _ba_nhieu(dung, [str(2 * S), str(p), str(a + b + c)],
                       buoc=lambda k: str(S + 3 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN



def L10_C3_B6_VD036_SA_B_02(socau, dang=2):
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
            lam_tron = ", làm tròn đến hàng phần mười"
        if (a, b, C) in [g[:3] for g in gt]:
            continue
        gt.append((a, b, C, dap, lam_tron))
    ten = [("mảnh vườn", "mảnh vườn"), ("thửa ruộng", "thửa ruộng"), ("khu đất", "khu đất")]
    cau = ''
    for a, b, C, dap, lam_tron in gt:
        t1, t2 = random.choice(ten)
        sin_tex = {30: r"\dfrac{1}{2}", 150: r"\dfrac{1}{2}", 45: r"\dfrac{\sqrt{2}}{2}",
                   135: r"\dfrac{\sqrt{2}}{2}", 60: r"\dfrac{\sqrt{3}}{2}",
                   120: r"\dfrac{\sqrt{3}}{2}"}[C]
        debai = (r"Một %s hình tam giác $ABC$ có $CA = %d\,\text{m}$, $CB = %d\,\text{m}$ và "
                 r"$\widehat{ACB} = %s$. Tính diện tích %s (đơn vị $\text{m}^{2}$%s)."
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


def L10_C3_B6_VD036_SA_B_03(socau, dang=2):
    r"""Diện tích mảnh đất hình TỨ GIÁC khi đo được bốn cạnh và một đường chéo:
    chia thành hai tam giác, dùng Heron hai lần rồi cộng lại.

    CLAUDE THEM 29/09/2026 - bien the 03 (cung dang Heron cho manh dat).
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
        debai = (r"Một mảnh đất hình tứ giác $ABCD$ có $AB = %d\,\text{m}$, $BC = %d\,\text{m}$, "
                 r"$CD = %d\,\text{m}$, $DA = %d\,\text{m}$ và đường chéo $AC = %d\,\text{m}$ "
                 r"(hai điểm $B$, $D$ nằm khác phía đối với $AC$). Tính diện tích mảnh đất "
                 r"(đơn vị $\text{m}^{2}$)." % (AB, BC, CD, DA, c))
        giai = (r"Đường chéo $AC$ chia mảnh đất thành hai tam giác $ABC$ và $ACD$.\\ "
                r"Tam giác $ABC$: $p = \dfrac{%d + %d + %d}{2} = %d$, "
                r"$S_1 = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$.\\ "
                r"Tam giác $ACD$: $p = \dfrac{%d + %d + %d}{2} = %d$, "
                r"$S_2 = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$.\\ "
                r"Diện tích mảnh đất: $S = S_1 + S_2 = %d + %d = %d\,\text{(m}^{2}\text{)}$."
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

        debai = (r"Một khu đất hình tam giác $ABC$ có hai cạnh $AB = %d\,\text{m}$, "
                 r"$AC = %d\,\text{m}$ và góc giữa hai cạnh đó là "
                 r"$\widehat{A} = %s$." % (c, b, _goc(A)))
        ds_abcd = [
            (r"Tính độ dài cạnh $BC$ (đơn vị mét).",
             r"%d\,\text{m}" % a,
             r"Định lí côsin trong tam giác $ABC$:\\ "
             r"$BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos A "
             r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
             r"Vậy $BC = %d\,\text{(m)}$."
             % (c, b, c, b, _L(cos_A), a2, a)),
            (r"Tính diện tích khu đất (đơn vị $\text{m}^{2}$).",
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

def L10_C3_B5_NB029_SA_A_01(socau, dang=2):
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
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, điểm $M\left(%s; %s\right)$ thuộc nửa đường "
                 r"tròn đơn vị. Tính $%s\widehat{xOM}$." % (_xx(x0), _xx(y0), ten))
        giai = (r"Với điểm $M\left(x_{0}; y_{0}\right)$ thuộc nửa đường tròn đơn vị thì "
                r"$\cos\widehat{xOM} = x_{0}$ và $\sin\widehat{xOM} = y_{0}$.\\ "
                r"Kiểm tra: $\left(%s\right)^{2} + \left(%s\right)^{2} = 1$ nên $M$ đúng là "
                r"điểm trên nửa đường tròn đơn vị.\\ "
                r"Vậy $%s\widehat{xOM} = %s$." % (_xx(x0), _xx(y0), ten, _xx(dapso)))
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
        debai = (r"Cho góc $\alpha$ thoả mãn $\sin\alpha = \dfrac{%d}{%d}$ và "
                 r"$90^{\circ} < \alpha < 180^{\circ}$." % (doi, huyen))
        ds_abcd = [
            (r"Tính $\cos\alpha$.",
             r"-\dfrac{%d}{%d}" % (ke, huyen),
             r"Từ $\sin^{2}\alpha + \cos^{2}\alpha = 1$ ta có "
             r"$\cos^{2}\alpha = 1 - \left(\dfrac{%d}{%d}\right)^{2} = \dfrac{%d}{%d}$, "
             r"suy ra $\cos\alpha = \pm\dfrac{%d}{%d}$.\\ "
             r"Vì $90^{\circ} < \alpha < 180^{\circ}$ nên $\alpha$ là góc tù, côsin âm. "
             r"Vậy $\cos\alpha = -\dfrac{%d}{%d}$."
             % (doi, huyen, ke * ke, huyen * huyen, ke, huyen, ke, huyen)),
            (r"Tính giá trị biểu thức $P = %d\sin\alpha + %d\cos\alpha$." % (m, n),
             r"%d" % P,
             r"Thay hai giá trị vừa tìm được:\\ "
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\widehat{A} = %s$."
                 % (b, c, _goc(A)))
        ds_abcd = [
            (r"Tính độ dài cạnh $BC$.", r"%d" % a,
             r"Định lí côsin:\\ "
             r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A "
             r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$.\\ "
             r"Vậy $BC = %d$." % (b, c, b, c, _L(cos_A), a2, a)),
            (r"Tính $\cos B$.", _L(cos_B),
             r"Lại dùng định lí côsin, lần này cho góc $B$:\\ "
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$."
                 % (a, _goc(A), _goc(B)))
        ds_abcd = [
            (r"Tính bán kính $R$ của đường tròn ngoại tiếp tam giác $ABC$.", _L(R),
             r"Định lí sin: $\dfrac{BC}{\sin A} = 2R$, suy ra $R = \dfrac{BC}{2\sin A}$.\\ "
             r"Với $\sin %s = %s$ thì $R = \dfrac{%d}{2\cdot %s} = %s$."
             % (_goc(A), _L(sin_A), a, _L(sin_A), _L(R))),
            (r"Tính độ dài cạnh $AC$.", _L(b),
             r"Vẫn định lí sin: $\dfrac{AC}{\sin B} = 2R$, suy ra $AC = 2R\sin B$.\\ "
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
        debai = r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$." % (a, b, c)
        ds_abcd = [
            (r"Tính diện tích tam giác $ABC$.", r"%d" % S,
             r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d$.\\ "
             r"Công thức Heron:\\ "
             r"$S = \sqrt{p\left(p-a\right)\left(p-b\right)\left(p-c\right)} "
             r"= \sqrt{%d\cdot %d\cdot %d\cdot %d} = \sqrt{%d} = %d$."
             % (a, b, c, p, p, p - a, p - b, p - c, S * S, S)),
            (r"Tính bán kính $r$ của đường tròn nội tiếp tam giác $ABC$.", r"%d" % r,
             r"Diện tích tam giác còn tính được bằng $S = p\cdot r$, nên\\ "
             r"$r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH035_SA_B_01(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$, $\widehat{A} = %s$. "
                 r"Tính số đo góc $B$ (đơn vị độ, làm tròn đến hàng phần trăm)."
                 % (b, c, _goc(A)))
        giai = (r"Định lí côsin cho $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot"
                r"\left(%s\right) = %d$, nên $BC = %d$.\\ "
                r"Lại theo định lí côsin:\\ "
                r"$\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} "
                r"= \dfrac{%d + %d - %d}{2\cdot %d\cdot %d} = %s$.\\ "
                r"Suy ra $\widehat{B} \approx %s^{\circ}$."
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{A} = %s$, $\widehat{B} = %s$."
                 % (a, _goc(A), _goc(B)))
        ds_abcd = [
            (r"Tính số đo góc $C$.", r"%s" % _goc(C),
             r"Tổng ba góc trong một tam giác bằng $180^{\circ}$ nên\\ "
             r"$\widehat{C} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C))),
            (r"Tính độ dài cạnh $AC$.", _L(b),
             r"Định lí sin: $\dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$, suy ra "
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

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, điểm $M\left(x_{0}; y_{0}\right)$ thuộc nửa "
                 r"đường tròn đơn vị, với $x_{0} = %s$ và $y_{0} = %s$. "
                 r"Xét tính đúng sai của các khẳng định sau:" % (_xx(x0), _xx(y0)))

        # a) NB - nhac lai dinh nghia
        y1 = [(r"{\True $\cos\widehat{xOM} = x_{0}$}",
               r"Đúng. Theo định nghĩa, hoành độ của $M$ chính là côsin của góc $\widehat{xOM}$."),
              (r"{$\cos\widehat{xOM} = y_{0}$}",
               r"Sai. $y_{0}$ là \textbf{sin}, còn côsin là $x_{0}$.")]

        # b) TH - thay so cu the
        y2 = [(r"{\True $\sin\widehat{xOM} = %s$}" % _xx(y0),
               r"Sin của góc bằng tung độ của $M$, tức $\sin\widehat{xOM} = y_{0} = %s$." % _xx(y0)),
              (r"{$\sin\widehat{xOM} = %s$}" % _xx(x0),
               r"Sai. Đó là hoành độ, tức côsin. Sin bằng $%s$." % _xx(y0))]

        # c) VD - phai lap ti so tu hai toa do
        y3 = [(r"{\True $\tan\widehat{xOM} = %s$}" % _xx(tan0),
               r"$\tan\widehat{xOM} = \dfrac{\sin\widehat{xOM}}{\cos\widehat{xOM}} "
               r"= \dfrac{y_{0}}{x_{0}} = \dfrac{%s}{%s} = %s$."
               % (_xx(y0), _xx(x0), _xx(tan0))),
              (r"{$\tan\widehat{xOM} = %s$}" % _xx(-tan0),
               r"Sai ở dấu. Vì $x_{0} < 0$ và $y_{0} > 0$ nên $\tan\widehat{xOM}$ \textbf{âm}, "
               r"bằng $%s$." % _xx(tan0))]

        # d) VDC - diem doi xung, phai suy ra quan he hai goc bu nhau
        y4 = [(r"{\True Gọi $N$ là điểm đối xứng với $M$ qua trục $Oy$. "
               r"Khi đó $\cos\widehat{xON} + \cos\widehat{xOM} = 0$}",
               r"$N$ đối xứng với $M$ qua $Oy$ nên $N\left(-x_{0}; y_{0}\right)$, "
               r"do đó $\cos\widehat{xON} = -x_{0}$.\\ "
               r"Vậy $\cos\widehat{xON} + \cos\widehat{xOM} = -x_{0} + x_{0} = 0$ "
               r"(hai góc $\widehat{xOM}$ và $\widehat{xON}$ bù nhau)."),
              (r"{Gọi $N$ là điểm đối xứng với $M$ qua trục $Oy$. "
               r"Khi đó $\sin\widehat{xON} + \sin\widehat{xOM} = 0$}",
               r"Sai. Hai điểm đối xứng qua $Oy$ có \textbf{cùng} tung độ, nên hai sin "
               r"\textbf{bằng nhau} chứ không đối nhau; tổng của chúng bằng $2y_{0} = %s$."
               % _xx(2 * y0))]

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_E_01(socau, socot=1):
    """Đúng/Sai - định lí sin, công thức diện tích và quan hệ giữa chúng."""
    cauTF = ''
    for _ in range(socau):
        a, b, c, S, p, r = random.choice([t for t in BANG_HERON if t[3] >= 20])
        R = Rational(a * b * c, 4 * S)

        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$. "
                 r"Gọi $S$, $p$, $R$, $r$ lần lượt là diện tích, nửa chu vi, bán kính đường "
                 r"tròn ngoại tiếp và bán kính đường tròn nội tiếp của tam giác. "
                 r"Xét tính đúng sai của các khẳng định sau:" % (a, b, c))

        # a) NB - nhac lai cong thuc
        y1 = [(r"{\True $S = p\cdot r$}",
               r"Đúng. Đây là một trong các công thức tính diện tích tam giác."),
              (r"{$S = 2p\cdot r$}",
               r"Sai. Công thức đúng là $S = p\cdot r$, không có hệ số $2$.")]

        # b) TH - thay so vao cong thuc Heron
        y2 = [(r"{\True $p = %d$ và $S = %d$}" % (p, S),
               r"$p = \dfrac{%d + %d + %d}{2} = %d$; Heron cho "
               r"$S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
               % (a, b, c, p, p, p - a, p - b, p - c, S)),
              (r"{$p = %d$ và $S = %d$}" % (p, S + 2),
               r"Sai. Heron cho $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$ chứ không phải $%d$."
               % (p, p - a, p - b, p - c, S, S + 2))]

        # c) VD - phai co S cua y b) moi tinh duoc r
        y3 = [(r"{\True $r = %d$}" % r,
               r"Từ $S = p\cdot r$ suy ra $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r)),
              (r"{$r = %s$}" % _L(simplify(Rational(S, p) + 1)),
               r"Sai. $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %d$." % (S, p, r))]

        # d) VDC - noi hai cong thuc dien tich khac nhau lai voi nhau
        y4 = [(r"{\True $R = %s$}" % _L(R),
               r"Diện tích tam giác còn tính được bằng $S = \dfrac{abc}{4R}$, "
               r"suy ra $R = \dfrac{abc}{4S}$.\\ "
               r"$R = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$."
               % (a, b, c, S, _L(R))),
              (r"{$R = %s$}" % _L(simplify(R * 2)),
               r"Sai. Từ $S = \dfrac{abc}{4R}$ ta được $R = \dfrac{abc}{4S} = %s$." % _L(R))]

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
    "nhon": (r"Với $0^{\circ} < \alpha < 90^{\circ}$ thì điểm $M$ nằm trên phần "
             r"nửa đường tròn đơn vị ở \textbf{bên phải} trục $Oy$, nên "
             r"$x_M > 0$ và $y_M > 0$."),
    "tu": (r"Với $90^{\circ} < \alpha < 180^{\circ}$ thì điểm $M$ nằm trên phần "
           r"nửa đường tròn đơn vị ở \textbf{bên trái} trục $Oy$, nên "
           r"$x_M < 0$ còn $y_M > 0$."),
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
        "{\\footnotesize $M$};\n"
        "\\fill[black] (N) circle[radius=1.5pt] node[above left]"
        "{\\footnotesize $N$};\n"
        "\\node[below] at ({cos(55)*1.6},0) {\\footnotesize $x_M$};\n"
        "\\node[below] at ({cos(130)*1.6},0) {\\footnotesize $x_N$};\n"
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

        debai = (r"Cho góc $\alpha$ thoả mãn %s. Khẳng định nào sau đây "
                 r"\textbf{đúng}?" % MO_TA_KHOANG[khoang])

        dau_chu = "dương" if bang[ten_dung] > 0 else "âm"
        if ten_dung == r"\sin":
            cach = r"$\sin\alpha = y_M$"
        elif ten_dung == r"\cos":
            cach = r"$\cos\alpha = x_M$"
        elif ten_dung == r"\tan":
            cach = r"$\tan\alpha = \dfrac{y_M}{x_M}$"
        else:
            cach = r"$\cot\alpha = \dfrac{x_M}{y_M}$"

        giai = (LY_DO_KHOANG[khoang] + "\\\\\n"
                + r"Mà %s nên $%s\alpha$ mang dấu %s, tức là %s."
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
        debai = (r"Cho góc $\alpha$ với $0^{\circ} < \alpha < 90^{\circ}$ và "
                 r"điểm $M$ nằm trên nửa đường tròn đơn vị như hình vẽ, "
                 r"trong đó $x_M$, $y_M$ lần lượt là hoành độ và tung độ "
                 r"của $M$. Khẳng định nào sau đây \textbf{đúng}?")

        giai = (r"Theo định nghĩa giá trị lượng giác của góc $\alpha$ với "
                r"$0^{\circ} \le \alpha \le 180^{\circ}$, nếu $M(x_M; y_M)$ "
                r"là điểm trên nửa đường tròn đơn vị ứng với góc $\alpha$ thì"
                "\\\\\n"
                r"$\sin\alpha = y_M$, \quad $\cos\alpha = x_M$, \quad "
                r"$\tan\alpha = \dfrac{y_M}{x_M}$ \ $(\alpha \ne 90^{\circ})$, "
                r"\quad $\cot\alpha = \dfrac{x_M}{y_M}$ \ "
                r"$(\alpha \ne 0^{\circ},\ \alpha \ne 180^{\circ})$."
                "\\\\\n"
                r"Vậy khẳng định đúng là %s." % CT[ten])

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
         r"$\cos\alpha = x_M$ nên $\cos\alpha > 0$ khi và chỉ khi $x_M > 0$, "
         r"tức là $M$ nằm bên phải trục $Oy$."),
        (r"\cos\alpha < 0", r"$90^{\circ} < \alpha \le 180^{\circ}$",
         [r"$0^{\circ} \le \alpha < 90^{\circ}$",
          r"$0^{\circ} < \alpha < 90^{\circ}$",
          r"$0^{\circ} \le \alpha \le 90^{\circ}$",
          r"$\alpha = 90^{\circ}$"],
         r"$\cos\alpha = x_M$ nên $\cos\alpha < 0$ khi và chỉ khi $x_M < 0$, "
         r"tức là $M$ nằm bên trái trục $Oy$. Chú ý $\cos 180^{\circ} = -1 < 0$ "
         r"nên $\alpha = 180^{\circ}$ vẫn thoả mãn."),
        (r"\tan\alpha > 0", r"$0^{\circ} < \alpha < 90^{\circ}$",
         [r"$90^{\circ} < \alpha < 180^{\circ}$",
          r"$0^{\circ} \le \alpha < 90^{\circ}$",
          r"$90^{\circ} < \alpha \le 180^{\circ}$",
          r"$0^{\circ} < \alpha \le 90^{\circ}$"],
         r"$\tan\alpha = \dfrac{y_M}{x_M}$ với $y_M > 0$, nên $\tan\alpha > 0$ "
         r"khi và chỉ khi $x_M > 0$. Chú ý $\tan 0^{\circ} = 0$ nên loại "
         r"$\alpha = 0^{\circ}$, và $\tan 90^{\circ}$ không xác định."),
        (r"\tan\alpha < 0", r"$90^{\circ} < \alpha < 180^{\circ}$",
         [r"$0^{\circ} < \alpha < 90^{\circ}$",
          r"$90^{\circ} \le \alpha \le 180^{\circ}$",
          r"$90^{\circ} < \alpha \le 180^{\circ}$",
          r"$0^{\circ} \le \alpha < 90^{\circ}$"],
         r"$\tan\alpha = \dfrac{y_M}{x_M}$ với $y_M > 0$, nên $\tan\alpha < 0$ "
         r"khi và chỉ khi $x_M < 0$. Chú ý $\tan 180^{\circ} = 0$ nên loại "
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
        debai = (r"Cho góc $\alpha$ với $0^{\circ} \le \alpha \le 180^{\circ}$ "
                 r"và $M$ là điểm trên nửa đường tròn đơn vị ứng với góc "
                 r"$\alpha$. Hình vẽ minh hoạ hai vị trí có thể có của $M$. "
                 r"Biết $%s$. Khẳng định nào sau đây \textbf{đúng}?"
                 % gia_thiet)
        giai = ly_do + "\\\\\n" + r"Vậy %s." % dung
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
        ("một ngọn núi", "chân núi", "đỉnh núi"),
        ("một toà nhà cao tầng", "chân toà nhà", "nóc toà nhà"),
        ("một cây cổ thụ", "gốc cây", "ngọn cây"),
        ("một ngọn hải đăng", "chân hải đăng", "đỉnh hải đăng"),
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

        debai = (r"Để đo chiều cao $DH$ của %s mà không tới được %s, người ta "
                 r"chọn hai điểm $A$, $B$ trên mặt đất cùng nằm trên một đường "
                 r"thẳng đi qua $H$ (điểm $B$ nằm giữa $A$ và $H$) với "
                 r"$AB = %d\,\text{m}$. Từ $A$ nhìn lên %s được góc nâng "
                 r"$%d^{\circ}$, từ $B$ nhìn lên %s được góc nâng $%d^{\circ}$. "
                 r"Chiều cao $DH$ gần nhất với giá trị nào sau đây "
                 r"(làm tròn đến hàng phần mười)?"
                 % (vat, chan, a, dinh, alpha, dinh, beta))

        giai = (r"Trong tam giác $ABD$: $\widehat{DAB} = %d^{\circ}$, còn "
                r"$\widehat{DBA} = 180^{\circ} - %d^{\circ}$ (hai góc kề bù với "
                r"góc nâng tại $B$), nên"
                "\\\\\n"
                r"$\widehat{ADB} = 180^{\circ} - %d^{\circ} - "
                r"\left(180^{\circ} - %d^{\circ}\right) = %d^{\circ}$."
                "\\\\\n"
                r"Áp dụng định lí sin trong tam giác $ABD$:"
                "\\\\\n"
                r"$\dfrac{BD}{\sin\widehat{DAB}} = "
                r"\dfrac{AB}{\sin\widehat{ADB}} \Rightarrow "
                r"BD = \dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} "
                r"\approx %s\,\text{(m)}$."
                "\\\\\n"
                r"Tam giác $BDH$ vuông tại $H$ có $\widehat{DBH} = %d^{\circ}$ nên"
                "\\\\\n"
                r"$DH = BD\cdot\sin %d^{\circ} \approx %s\,\text{(m)}$."
                % (alpha, beta, alpha, beta, beta - alpha,
                   a, alpha, beta - alpha, _xx(a * math.sin(ra) / hieu, 2),
                   beta, beta, _xx(h, 1)))

        cauTN += MC_SA_answer_text(debai, dapso, nhieu, giai, 0, 0, dang)
    return cauTN


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
    NUI = [("Phan Xi Păng", 3.1), ("Ngọc Linh", 2.6), ("Bà Đen", 1.0),
           ("Tây Côn Lĩnh", 2.4), ("Pu Ta Leng", 3.0)]

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

        debai = (r"Đứng trên đỉnh núi %s ở độ cao $h = %s\,\text{km}$ so với "
                 r"mực nước biển, một người nhìn về phía biển thì thấy đường "
                 r"chân trời. Tia nhìn tới đường chân trời tạo với phương nằm "
                 r"ngang một góc hạ $\theta = %s^{\circ}$. Coi Trái Đất là "
                 r"khối cầu tâm $O$ bán kính $R$; gọi $M$ là vị trí người quan "
                 r"sát và $T$ là điểm mà tia nhìn chạm mặt biển."
                 % (ten, _xx(h, 1), _xx(theta, 2)))

        hoi_a = (r"Chứng tỏ tam giác $OTM$ vuông tại $T$ và tính "
                 r"$\widehat{OMT}$ theo $\theta$.")
        giai_a = (r"Tia nhìn chạm mặt biển ở đúng đường chân trời nên $MT$ "
                  r"là tiếp tuyến của đường tròn tâm $O$ tại $T$, do đó "
                  r"$OT \perp MT$: tam giác $OTM$ vuông tại $T$."
                  "\\\\\n"
                  r"Phương nằm ngang tại $M$ vuông góc với bán kính $OM$. "
                  r"Tia nhìn $MT$ hạ xuống dưới phương ấy một góc $\theta$, "
                  r"nên góc giữa $MT$ và $MO$ là"
                  "\\\\\n"
                  r"$\widehat{OMT} = 90^{\circ} - \theta = %s^{\circ}$."
                  % _xx(90 - theta, 2))

        hoi_b = r"Chứng minh rằng $\cos\theta = \dfrac{R}{R + h}$."
        giai_b = (r"Tam giác $OTM$ vuông tại $T$ có $OT = R$ là cạnh đối diện "
                  r"góc $\widehat{OMT}$ và $OM = R + h$ là cạnh huyền, nên"
                  "\\\\\n"
                  r"$\sin\widehat{OMT} = \dfrac{OT}{OM} = \dfrac{R}{R + h}$."
                  "\\\\\n"
                  r"Mà $\widehat{OMT} = 90^{\circ} - \theta$ và hai góc phụ "
                  r"nhau có sin góc này bằng côsin góc kia, nên "
                  r"$\sin\left(90^{\circ} - \theta\right) = \cos\theta$."
                  "\\\\\n"
                  r"Vậy $\cos\theta = \dfrac{R}{R + h}$.")

        hoi_c = (r"Từ đó tính bán kính $R$ của Trái Đất (làm tròn đến hàng "
                 r"đơn vị, tính theo ki-lô-mét).")
        giai_c = (r"Từ $\cos\theta = \dfrac{R}{R+h}$ suy ra "
                  r"$\left(R + h\right)\cos\theta = R$, tức là"
                  "\\\\\n"
                  r"$R\left(1 - \cos\theta\right) = h\cos\theta "
                  r"\Rightarrow R = \dfrac{h\cos\theta}{1 - \cos\theta}$."
                  "\\\\\n"
                  r"Thay số $h = %s\,\text{km}$ và $\theta = %s^{\circ}$:"
                  "\\\\\n"
                  r"$R = \dfrac{%s\cdot\cos %s^{\circ}}{1 - \cos %s^{\circ}} "
                  r"\approx %s\,\text{(km)}$."
                  "\\\\\n"
                  r"Kết quả này sát với bán kính Trái Đất thường dùng là "
                  r"$6371\,\text{km}$. Lưu ý $1 - \cos\theta$ là một số rất "
                  r"bé, nên khi bấm máy phải giữ đủ chữ số thập phân, làm "
                  r"tròn sớm sẽ ra kết quả lệch nhiều."
                  % (_xx(h, 1), _xx(theta, 2), _xx(h, 1),
                     _xx(theta, 2), _xx(theta, 2), _xx(R, 0)))

        ds_abcd = [(hoi_a, r"90^{\circ} - \theta", giai_a),
                   (hoi_b, r"\cos\theta = \dfrac{R}{R + h}", giai_b),
                   (hoi_c, r"R \approx %s\,\text{km}" % _xx(R, 0), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


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

    PHUONG_TIEN = [("Một chiếc tàu", "tàu"), ("Một chiếc ca nô", "ca nô"),
                   ("Một chiếc thuyền buồm", "thuyền")]

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

        debai = (r"%s xuất phát từ cảng $A$, chạy thẳng $%d\,\text{km}$ theo "
                 r"một hướng cố định tới vị trí $B$. Tại $B$, %s đổi hướng "
                 r"một góc $60^{\circ}$ rồi chạy thẳng thêm $%d\,\text{km}$ "
                 r"nữa thì tới đảo $C$."
                 % (ten_hoa, a, ten, b))

        hoi_a = r"Tính số đo góc $\widehat{ABC}$."
        giai_a = (r"Hướng cũ của %s là tia đối của tia $BA$. Đổi hướng một góc "
                  r"$60^{\circ}$ nghĩa là tia $BC$ hợp với hướng cũ ấy một góc "
                  r"$60^{\circ}$, nên $\widehat{ABC}$ kề bù với góc $60^{\circ}$:"
                  "\\\\\n"
                  r"$\widehat{ABC} = 180^{\circ} - 60^{\circ} = 120^{\circ}$."
                  % ten)

        hoi_b = r"Tính khoảng cách $AC$ từ cảng $A$ tới đảo $C$."
        giai_b = (r"Áp dụng định lí côsin trong tam giác $ABC$:"
                  "\\\\\n"
                  r"$AC^2 = AB^2 + BC^2 - 2\cdot AB\cdot BC\cdot"
                  r"\cos\widehat{ABC}$"
                  "\\\\\n"
                  r"$AC^2 = %d^2 + %d^2 - 2\cdot %d\cdot %d\cdot"
                  r"\left(-\dfrac{1}{2}\right) = %d$."
                  "\\\\\n"
                  r"Vậy $AC = %d\,\text{(km)}$."
                  % (a, b, a, b, k * k, k))

        hoi_c = (r"Từ đảo $C$, %s muốn quay thẳng về cảng $A$. Tính số đo góc "
                 r"$\widehat{BAC}$ (làm tròn đến hàng phần mười của độ)." % ten)
        giai_c = (r"Áp dụng định lí sin trong tam giác $ABC$:"
                  "\\\\\n"
                  r"$\dfrac{BC}{\sin\widehat{BAC}} = "
                  r"\dfrac{AC}{\sin\widehat{ABC}} \Rightarrow "
                  r"\sin\widehat{BAC} = \dfrac{BC\cdot\sin\widehat{ABC}}{AC} "
                  r"= \dfrac{%d\cdot\sin 120^{\circ}}{%d} \approx %s$."
                  "\\\\\n"
                  r"Vì tam giác $ABC$ đã có góc tù $\widehat{ABC} = "
                  r"120^{\circ}$ nên $\widehat{BAC}$ là góc nhọn, do đó"
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
        debai = r"Giá trị của biểu thức $A = %s$ bằng" % bt
        giai = (r"Tra bảng giá trị lượng giác của các góc đặc biệt (góc tù dùng quan hệ "
                r"hai góc bù nhau):\\ $A = %s = %s$." % (thay, _L(tong)))
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
        debai = (r"Cho góc $\alpha$ thoả mãn $90^{\circ} < \alpha < 180^{\circ}$. Biểu thức nào "
                 r"sau đây luôn \textbf{%s}?" % ("âm" if hoi_am else "dương"))
        giai = (r"Góc $\alpha$ tù nên $\sin\alpha > 0$, còn $\cos\alpha < 0$, $\tan\alpha < 0$, "
                r"$\cot\alpha < 0$." + "\\\\\n" +
                r"Tích (thương) của hai số cùng dấu thì dương, trái dấu thì âm. Do đó "
                r"$%s$ %s." % (viet(*d), "âm" if hoi_am else "dương") + "\\\\\n" +
                r"Ba biểu thức còn lại đều %s." % ("dương" if hoi_am else "âm"))
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
    PA = {"nhon": r"$\alpha$ là góc nhọn", "tu": r"$\alpha$ là góc tù",
          "vuong": r"$\alpha = 90^{\circ}$", "bet": r"$\alpha = 0^{\circ}$ hoặc $\alpha = 180^{\circ}$"}
    ds = list(range(len(TH)))
    random.shuffle(ds)
    cauTN = ""
    for i in ds[:min(socau, len(ds))]:
        dk, loai, suy = TH[i]
        dung = PA[loai]
        nhieu = [PA[k] for k in PA if k != loai]
        debai = (r"Cho góc $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ thoả mãn "
                 r"$%s$. Khẳng định nào sau đây \textbf{đúng}?" % dk)
        giai = (r"Vì $0^{\circ} \le \alpha \le 180^{\circ}$ nên $\sin\alpha \ge 0$. Tích khác $0$ nên "
                r"$\sin\alpha > 0$, tức $\alpha \ne 0^{\circ}$, $\alpha \ne 180^{\circ}$ (và các giá trị "
                r"trong tích xác định nên $\alpha \ne 90^{\circ}$)." + "\\\\\n" +
                r"Do đó $%s$, suy ra %s." % (suy, dung))
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
        debai = r"Cho tam giác $ABC$. Khẳng định nào sau đây \textbf{đúng}?"
        giai = (r"Vì $A + B + C = 180^{\circ}$ nên $%s = 180^{\circ} - %s$: hai góc $%s$ và $%s$ "
                r"bù nhau." % (tong, X, tong, X) + "\\\\\n" +
                r"Hai góc bù nhau có sin bằng nhau; côsin, tang đối nhau. Do đó "
                r"$\sin\left(%s\right) = \sin %s$, $\cos\left(%s\right) = -\cos %s$, "
                r"$\tan\left(%s\right) = -\tan %s$." % (tong, X, tong, X, tong, X) + "\\\\\n" +
                r"Vậy khẳng định đúng là %s." % dung)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_TH031_SA_A_02(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $\widehat{A} = %s$, $\widehat{B} = %s$. Tính giá trị "
                 r"của biểu thức $T = \%s C\cdot\%s\left(A + B\right)$."
                 % (_goc(A), _goc(B), h1, h2))
        giai = (r"$\widehat{C} = 180^{\circ} - %s - %s = %s$ nên $\%s C = \%s %s = %s$.\\ "
                r"$A + B = 180^{\circ} - C = %s$, nên $\%s\left(A + B\right) = \%s %s = %s$.\\ "
                r"Vậy $T = %s\cdot %s = %s$."
                % (_goc(A), _goc(B), _goc(C), h1, h1, _goc(C), _L(v1),
                   _goc(180 - C), h2, h2, _goc(180 - C), _L(v2),
                   (r"\left(%s\right)" % _L(v1)) if v1 < 0 else _L(v1),
                   (r"\left(%s\right)" % _L(v2)) if v2 < 0 else _L(v2), dap))
        nguoc = _so_thap_phan_gon(-T) or "0"
        ds = _ba_nhieu(dap, [nguoc, "1", "-1", "0"], buoc=lambda t: str(t + 1))
        cau += MC_SA_answer_const(debai, dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_B_02(socau, dang=2):
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
        debai = (r"Tính $S = %s\left(%s\right)$, trong đó các góc tăng đều mỗi lần $%s$."
                 % (he, day, _goc(d))) if k != 1 else \
            (r"Tính $S = %s$, trong đó các góc tăng đều mỗi lần $%s$." % (day, _goc(d)))
        phu = "sin" if ham == "cos" else "cos"
        giai = (r"Dãy góc $%s, %s, \ldots, %s$ có $\dfrac{%d - %d}{%d} + 1 = %d$ góc."
                % (_goc(goc[0]), _goc(goc[1]), _goc(goc[-1]), goc[-1], goc[0], d, n) + "\\\\\n" +
                r"Ghép hai góc phụ nhau $x$ và $90^{\circ} - x$: $\%s^{2}\left(90^{\circ} - x\right) = "
                r"\%s^{2}x$ nên mỗi cặp $\%s^{2}x + \%s^{2}\left(90^{\circ} - x\right) = 1$."
                % (ham, phu, ham, ham) + "\\\\\n" +
                (r"Có $%d$ cặp, còn lại góc $45^{\circ}$ với $\%s^{2}45^{\circ} = \dfrac{1}{2}$."
                 % (so_cap, ham) if co45 else r"Có $%d$ cặp." % so_cap) + "\\\\\n" +
                r"Vậy $S = %s%s$." % (("%d\\cdot " % k) if k != 1 else "",
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
    """
    BO = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (4, 3, 5), (12, 5, 13)]
    cauTF = ""
    for _ in range(socau):
        a, b, c = random.choice(BO)
        tu = random.random() < 0.5
        sn = Rational(a, c)
        cs = Rational(-b, c) if tu else Rational(b, c)
        tn, ct = sn / cs, cs / sn
        khoang = r"90^{\circ} < \alpha < 180^{\circ}" if tu else r"0^{\circ} < \alpha < 90^{\circ}"
        debai = (r"Cho góc $\alpha$ thoả mãn $\sin\alpha = %s$ và $%s$. Xét tính đúng sai của "
                 r"các khẳng định sau:" % (_L(sn), khoang))
        # a) NB - quan he hai goc bu nhau
        y1 = [(r"{\True $\sin\left(180^{\circ} - \alpha\right) = %s$}" % _L(sn),
               r"Đúng. Hai góc bù nhau có sin bằng nhau."),
              (r"{$\sin\left(180^{\circ} - \alpha\right) = %s$}" % _L(-sn),
               r"Sai. $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha = %s$." % _L(sn))]
        # b) TH - he thuc co ban va xet dau cos theo loai goc
        ly_cos = (r"$\cos^{2}\alpha = 1 - \left(%s\right)^{2} = %s$, và vì $\alpha$ %s nên "
                  r"$\cos\alpha %s 0$, do đó $\cos\alpha = %s$."
                  % (_L(sn), _L(1 - sn ** 2), "tù" if tu else "nhọn", "<" if tu else ">", _L(cs)))
        y2 = [(r"{\True $\cos\alpha = %s$}" % _L(cs), r"Đúng. " + ly_cos),
              (r"{$\cos\alpha = %s$}" % _L(-cs), r"Sai (sai dấu). " + ly_cos)]
        # c) VD - dung ket qua cua b) de tinh tan
        y3 = [(r"{\True $\tan\alpha = %s$}" % _L(tn),
               r"Đúng. $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$." % _L(tn)),
              (r"{$\tan\alpha = %s$}" % _L(1 / tn),
               r"Sai (đảo tử và mẫu). $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$." % _L(tn))]
        # d) VDC - thay ca sin va cos vao bieu thuc
        P = simplify((sn + cs) / (sn - cs))
        P_sai = simplify((sn - cs) / (sn + cs))
        y4 = [(r"{\True $\dfrac{\sin\alpha + \cos\alpha}{\sin\alpha - \cos\alpha} = %s$}" % _L(P),
               r"Đúng. Thay $\sin\alpha = %s$, $\cos\alpha = %s$ được $%s$." % (_L(sn), _L(cs), _L(P))),
              (r"{$\dfrac{\sin\alpha + \cos\alpha}{\sin\alpha - \cos\alpha} = %s$}" % _L(P_sai),
               r"Sai. Thay $\sin\alpha = %s$, $\cos\alpha = %s$ được $%s$." % (_L(sn), _L(cs), _L(P)))]
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
        debai = (r"Cho tam giác $ABC$ có $AB = %d$, $AC = %d$ và $\cos A = %s$. Độ dài cạnh "
                 r"$BC$ bằng" % (c, b, _L(cA)))
        giai = (r"Theo định lí côsin: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos A$\\ "
                r"$= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %d$.\\ Vậy $BC = %s$."
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
        debai = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$, $%s = %d$. Độ dài đường trung "
                 r"tuyến kẻ từ đỉnh $%s$ bằng" % (doi, a, k1, b, k2, c, dinh))
        giai = (r"Đường trung tuyến kẻ từ $%s$ ứng với cạnh đối diện $%s = %d$:\\ "
                r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4} = \dfrac{%d + %d}{2} - "
                r"\dfrac{%d}{4} = %s$.\\ Vậy độ dài trung tuyến bằng $%s$."
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
        debai = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$, $%s = %d$. Tính độ dài đường trung "
                 r"tuyến kẻ từ đỉnh $%s$." % (doi, a, k1, b, k2, c, dinh))
        giai = (r"$m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4} = \dfrac{%d + %d}{2} - "
                r"\dfrac{%d}{4} = %d$, nên $m_{%s} = %d$."
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
        debai = (r"Tam giác $ABC$ nội tiếp đường tròn bán kính $R = %d$, có $\widehat{A} = %s$, "
                 r"$\widehat{B} = %s$. Độ dài cạnh $AB$ bằng" % (R, _goc(A), _goc(B)))
        giai = (r"$\widehat{C} = 180^{\circ} - %s - %s = %s$. Cạnh $AB = c$ đối diện góc $C$.\\ "
                r"Theo định lí sin: $c = 2R\sin C = 2\cdot %d\cdot\sin %s = %s$."
                % (_goc(A), _goc(B), _goc(C), R, _goc(C), _L(c)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C3_B6_TH033_SA_A_02(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$, $%s = %d$. Tính bán kính $R$ của "
                 r"đường tròn ngoại tiếp tam giác." % (canh[0][0], canh[0][1], canh[1][0], canh[1][1],
                                                      canh[2][0], canh[2][1]))
        giai = (r"Ta có $%d^{2} + %d^{2} = %d = %d^{2}$ nên tam giác vuông, cạnh huyền là $%s = %d$.\\ "
                r"Tam giác vuông nội tiếp đường tròn có đường kính là cạnh huyền nên "
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
        debai = (r"Tam giác $ABC$ có $AB = %d$, $AC = %d$ và diện tích $S = %s$. Biết góc $A$ %s, "
                 r"số đo góc $A$ bằng" % (c, b, _L(S), "tù" if tu else "nhọn"))
        giai = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A \Rightarrow %s = %s\sin A \Rightarrow "
                r"\sin A = %s$.\\ Suy ra $\widehat{A} = %s$ hoặc $\widehat{A} = %s$. Vì $A$ %s nên "
                r"$\widehat{A} = %s$."
                % (_L(S), _L(Rational(b * c, 2)), _L(sg), _goc(g), _goc(bu), "tù" if tu else "nhọn",
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
        debai = r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$." % (a, b, c)
        ds_abcd = [
            (r"Tính diện tích tam giác $ABC$.", "%d" % S,
             r"$p = \dfrac{%d + %d + %d}{2} = %d$, $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
             % (a, b, c, p, p, p - a, p - b, p - c, S)),
            (r"Tính bán kính $R$ của đường tròn ngoại tiếp tam giác.", _L(R),
             r"$R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$." % (a, b, c, S, _L(R))),
            (r"Tính độ dài đường cao kẻ từ đỉnh $A$.", _L(ha),
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
        dung = r"Tam giác vuông tại $%s$" % dinh
        nhieu = [r"Tam giác vuông tại $%s$" % d for d in "ABC" if d != dinh] + [r"Tam giác tù"]
        debai = (r"Tam giác $ABC$ có $a = %d$, $b = %d$, $c = %d$. Khẳng định nào sau đây "
                 r"\textbf{đúng}?" % (a, b, c))
        x, y = [v for v in ba if v != z]
        giai = (r"Cạnh lớn nhất là $%s = %d$. Ta có $%d^{2} + %d^{2} = %d = %d^{2}$.\\ "
                r"Theo định lí côsin, $\cos %s = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = 0$ "
                r"nên $\widehat{%s} = 90^{\circ}$: tam giác vuông tại $%s$ (đỉnh đối diện cạnh lớn nhất)."
                % ("abc"[ba.index(z)], z, x, y, z * z, z, dinh, x, y, z, x, y, dinh, dinh))
        cauTN += MC_SA_answer_text(debai, dung, nhieu[:3], giai, 0, 0, dang)
    return cauTN


def L10_C3_TF_B_02(socau, socot=1):
    r"""Đúng/Sai - hệ thức lượng: biết $b$, $c$ và $\cos A$ (phân số): cạnh $a$,
    $\sin A$, diện tích, bán kính ngoại tiếp.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C3_TF_B, theo cau Dung/Sai
    "b = 5, c = 7, cos A = 3/5" trong giao an Bai 6. Co Lan duyet.
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\cos A = %s$. Xét tính đúng sai "
                 r"của các khẳng định sau:" % (b, c, _L(cA)))
        # a) NB - sin A tu he thuc co ban (sin A > 0)
        y1 = [(r"{\True $\sin A = %s$}" % _L(sA),
               r"Đúng. $\sin A = \sqrt{1 - \cos^{2}A} = %s$ (vì $\sin A > 0$)." % _L(sA)),
              (r"{$\sin A = %s$}" % _L(-sA),
               r"Sai. Trong tam giác $0^{\circ} < A < 180^{\circ}$ nên $\sin A > 0$, $\sin A = %s$."
               % _L(sA))]
        # b) TH - dinh li cosin
        y2 = [(r"{\True $BC = %s$}" % _L(a),
               r"Đúng. $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %d$." % (
                   b, c, b, c, (r"\left(%s\right)" % _L(cA)) if cA < 0 else _L(cA), a2)),
              (r"{$BC = %s$}" % _L(sqrt(Integer(b * b + c * c + 2 * b * c * cA))),
               r"Sai (sai dấu). $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos A = %d$ nên "
               r"$BC = %s$." % (b, c, b, c, a2, _L(a)))]
        # c) VD - dien tich
        y3 = [(r"{\True Diện tích tam giác $ABC$ bằng $%s$}" % _L(S),
               r"Đúng. $S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$."
               % (c, b, _L(sA), _L(S))),
              (r"{Diện tích tam giác $ABC$ bằng $%s$}" % _L(2 * S),
               r"Sai (quên hệ số $\dfrac{1}{2}$). $S = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$."
               % (c, b, _L(sA), _L(S)))]
        # d) VDC - ban kinh ngoai tiep (can BC tu y b)
        y4 = [(r"{\True Bán kính đường tròn ngoại tiếp tam giác bằng $%s$}" % _L(R),
               r"Đúng. $R = \dfrac{BC}{2\sin A} = \dfrac{%s}{2\cdot %s} = %s$." % (_L(a), _L(sA), _L(R))),
              (r"{Bán kính đường tròn ngoại tiếp tam giác bằng $%s$}" % _L(simplify(2 * R)),
               r"Sai. $\dfrac{BC}{\sin A} = 2R$ nên $R = \dfrac{BC}{2\sin A} = %s$." % _L(R))]
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_TF_E_02(socau, socot=1):
    r"""Đúng/Sai - định lí sin và diện tích trong tam giác VUÔNG có góc
    $30^{\circ}$ hoặc $60^{\circ}$.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C3_TF_E, theo cau "vuong tai
    B, A = 30, a = 5" trong giao an Bai 6. Co Lan duyet.
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
        debai = (r"Cho tam giác $ABC$ vuông tại $B$, có $\widehat{A} = %s$ và $BC = %d$. Xét tính "
                 r"đúng sai của các khẳng định sau:" % (_goc(A), a))
        # a) NB
        y1 = [(r"{\True $\widehat{C} = %s$}" % _goc(C),
               r"Đúng. $\widehat{C} = 180^{\circ} - 90^{\circ} - %s = %s$." % (_goc(A), _goc(C))),
              (r"{$\widehat{C} = %s$}" % _goc(A),
               r"Sai. $\widehat{C} = 180^{\circ} - 90^{\circ} - %s = %s$." % (_goc(A), _goc(C)))]
        # b) TH
        y2 = [(r"{\True Bán kính đường tròn ngoại tiếp $R = %s$}" % _L(R),
               r"Đúng. $R = \dfrac{BC}{2\sin A} = \dfrac{%d}{2\cdot %s} = %s$." % (a, _L(sA), _L(R))),
              (r"{Bán kính đường tròn ngoại tiếp $R = %s$}" % _L(2 * R),
               r"Sai. Đó là $2R$; $R = \dfrac{BC}{2\sin A} = %s$." % _L(R))]
        # c) VD
        y3 = [(r"{\True $AB = %s$}" % _L(c),
               r"Đúng. $AC = 2R = %s$ (cạnh huyền là đường kính), $AB = 2R\sin C = %s$." % (_L(b), _L(c))),
              (r"{$AB = %s$}" % _L(simplify(b * _gtlg("sin", A))),
               r"Sai. $AB$ đối diện góc $C$ nên $AB = 2R\sin C = %s$." % _L(c))]
        # d) VDC
        y4 = [(r"{\True Diện tích tam giác $ABC$ bằng $%s$}" % _L(S),
               r"Đúng. Hai cạnh góc vuông là $BC$ và $AB$: $S = \dfrac{1}{2}\cdot %d\cdot %s = %s$."
               % (a, _L(c), _L(S))),
              (r"{Diện tích tam giác $ABC$ bằng $%s$}" % _L(2 * S),
               r"Sai (quên hệ số $\dfrac{1}{2}$). $S = \dfrac{1}{2}\cdot BC\cdot AB = %s$." % _L(S))]
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
        debai = (r"Một mảnh đất hình tam giác $ABC$ có $AB = %d\,\text{m}$, $AC = %d\,\text{m}$, "
                 r"$\widehat{A} = %s$. Người ta rào toàn bộ mảnh đất dọc theo ba cạnh, giá làm "
                 r"hàng rào là $%d$ nghìn đồng/mét." % (AB, AC, _goc(A), gia))
        ds_abcd = [
            (r"Tính độ dài cạnh $BC$ (làm tròn đến hàng phần mười mét).", r"%s\,\text{m}" % _xx(BC1, 1),
             r"Theo định lí côsin: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s \approx %s$, "
             r"nên $BC \approx %s\,\text{m}$." % (AB, AC, AB, AC, _goc(A), _xx(BC * BC, 1), _xx(BC1, 1))),
            (r"Tính chi phí làm hàng rào (làm tròn đến triệu đồng).", r"%d\ \text{triệu đồng}" % trieu,
             r"Chu vi $P \approx %d + %d + %s = %s\,\text{m}$.\\ Chi phí $\approx %s\cdot %d\,000 "
             r"\approx %d$ triệu đồng." % (AB, AC, _xx(BC1, 1), _xx(P, 1), _xx(P, 1), gia, trieu)),
            (r"Tính diện tích mảnh đất (làm tròn đến hàng đơn vị mét vuông).",
             r"%d\,\text{m}^{2}" % int(round(S)),
             r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s "
             r"\approx %d\,\text{m}^{2}$." % (AB, AC, _goc(A), int(round(S)))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN

