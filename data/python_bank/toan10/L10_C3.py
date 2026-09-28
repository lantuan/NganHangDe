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

        ds = set()
        for x in (-gia_tri_bu, hang[1], hang[2]):
            if x is not None and simplify(x - gia_tri_bu) != 0:
                ds.add(latex(x))
        while len(ds) < 3:
            ds.add(latex(Rational(random.randint(1, 3), random.randint(2, 4))))

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
        ds = list(dict.fromkeys([latex(simplify(a / k)), latex(a * 2), latex(simplify(b + a))]))
        ds = [x for x in ds if x != latex(b)][:3]
        while len(ds) < 3:
            ds.append(latex(a + len(ds) + 2))
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
        ds = [str(2 * S), str(S + 2), str(b * c // 2)]
        ds = [x for x in dict.fromkeys(ds) if x != str(S)][:3]
        while len(ds) < 3:
            ds.append(str(S + len(ds) + 5))
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


def L10_C3_B5_TH030_MC_A_02(socau, dang=1):
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

        **Bước 1: Tính góc $\\widehat{{B}}$**
        Tổng ba góc trong tam giác là $180^\\circ$, nên:
        \\[\\widehat{{B}} = 180^\\circ - \\widehat{{A}} - \\widehat{{C}} = 180^\\circ - {A}^\\circ - {C}^\\circ = {B}^\\circ\\]

        **Bước 2: Áp dụng Định lí Sin**
        Ta có tỉ lệ:
        \\[\\dfrac{{AB}}{{\\sin C}} = \\dfrac{{AC}}{{\\sin B}}\\]
        Thay các giá trị đã biết ($AC=b={b}$, $\\widehat{{B}}={B}^\\circ$, $\\widehat{{C}}={C}^\\circ$):
        \\[AB = \\dfrac{{AC \\cdot \\sin C}}{{\\sin B}} = \\dfrac{{{b} \\cdot \\sin({C}^\\circ)}}{{\\sin({B}^\\circ)}}\\]

        **Bước 3: Tính toán**
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

        **Bước 1. Tính độ dài các cạnh**
        \\begin{{itemize}}
        \\item $AB = c = {vt1} \\cdot {t1_h_str} = {c} \\mathrm{{~(km)}}$
        \\item $BC = a = {vt2} \\cdot {t2_h_str} = {a} \\mathrm{{~(km)}}$
        \\end{{itemize}}

        **Bước 2. Xác định góc $\\widehat{{ABC}}$**
        Hai hướng $N{goc1}^\\circ E$ và $S{goc2}^\\circ E$ cùng nghiêng về phía Đông,
        nên góc giữa hai hướng bằng tổng hai góc phương vị:
        \\[\\widehat{{ABC}} = {goc1}^\\circ + {goc2}^\\circ = {Goc_B_deg}^\\circ\\]

        **Bước 3. Áp dụng định lí Cosin**
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
        **Phân tích bài toán:** Quỹ đạo chuyển động của tàu tạo thành tam giác $ABC$.
        $AB = c = {vt1} \\cdot \\frac{{{t1}}}{{60}} = {c}$ km 
        $BC = a = {vt2} \\cdot \\frac{{{t2}}}{{60}} = {a}$ km
        Góc $\\widehat{{ABC}} = {goc1_f}^\\circ + {goc2_f}^\\circ = {goc_B_dung}^\\circ$
        Áp dụng Định lí Cosin: $AC = b \\approx {b}$ km
        Hướng từ $A$ đến $C$ là ${Huong_AC_str}$
        """

        # a) Độ dài AB hoặc BC
        ds_a = [
            (f"{{\\True Độ dài đoạn $AB$ là ${c}$ km}}", f"Độ dài $AB = {c}$ km. Phát biểu **Đúng**. {giai_chung}"),
            (f"{{Độ dài đoạn $AB$ là ${a}$ km}}",
             f"Độ dài $AB = {c}$ km $\\ne {a}$ km. Phát biểu **Sai**. {giai_chung}"),
            (f"{{\\True Độ dài đoạn $BC$ là ${a}$ km}}", f"Độ dài $BC = {a}$ km. Phát biểu **Đúng**. {giai_chung}"),
            (f"{{Độ dài đoạn $BC$ là ${b}$ km}}",
             f"Độ dài $BC = {a}$ km $\\ne {b}$ km. Phát biểu **Sai**. {giai_chung}"),
        ]

        # b) Góc ABC
        ds_b = [
            (f"{{\\True Góc $\\widehat{{ABC}}$ bằng ${goc_B_dung}^\\circ$}}",
             f"Góc $\\widehat{{ABC}} = {goc_B_dung}^\\circ$. Phát biểu **Đúng**. {giai_chung}"),
            (f"{{Góc $\\widehat{{ABC}}$ bằng ${goc_B_sai}^\\circ$}}",
             f"Góc $\\widehat{{ABC}} = {goc_B_dung}^\\circ \\ne {goc_B_sai}^\\circ$. Phát biểu **Sai**. {giai_chung}"),
            (f"{{Góc $\\widehat{{ABC}}$ bằng ${goc1_f}^\\circ$}}",
             f"Góc $\\widehat{{ABC}} = {goc_B_dung}^\\circ \\ne {goc1_f}^\\circ$. Phát biểu **Sai**. {giai_chung}"),
        ]

        # CÂU C: Khoảng cách từ A đến C
        ds_c = [
            (f"{{\\True Khoảng cách từ $A$ đến $C$ xấp xỉ ${b}$ km}}",
             f"Áp dụng Định lí Cosin, $AC = b \\approx {b}$ km. Phát biểu **Đúng**. {giai_chung}"),
            (f"{{Khoảng cách từ $A$ đến $C$ xấp xỉ ${a}$ km}}",
             f"Áp dụng Định lí Cosin, $AC = b \\approx {b}$ km $\\ne {a}$ km. Phát biểu **Sai**. {giai_chung}"),
            (f"{{Khoảng cách từ $A$ đến $C$ xấp xỉ ${c}$ km}}",
             f"Áp dụng Định lí Cosin, $AC = b \\approx {b}$ km $\\ne {c}$ km. Phát biểu **Sai**. {giai_chung}"),
        ]

        # CÂU D: Hướng đi từ A đến C
        ds_d = [
            (f"{{\\True Muốn đi thẳng từ $A$ đến $C$ thì đi theo hướng ${Huong_AC_str}$}}",
             f"Hướng $AC$ là ${Huong_AC_str}$. Phát biểu **Đúng**. {giai_chung}"),
            (f"{{Muốn đi thẳng từ $A$ đến $C$ thì đi theo hướng ${Huong_AC_str_sai}$}}",
             f"Hướng $AC$ là ${Huong_AC_str} \\ne {Huong_AC_str_sai}$. Phát biểu **Sai**. {giai_chung}"),
            (f"{{Muốn đi thẳng từ $A$ đến $C$ thì đi theo hướng $N {goc1_f}^\\circ E$}}",
             f"Hướng $AC$ là ${Huong_AC_str} \\ne N {goc1_f}^\\circ E$. Phát biểu **Sai**. {giai_chung}"),
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
