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


def L10_C3_B5_NB029_MC_B_01(socau, dang=1):
    """Biết toạ độ điểm M trên nửa đường tròn đơn vị, tính sin hoặc côsin."""
    gt = []
    while len(gt) < socau:
        p, q = _cap_nguyen_to_cung_nhau()
        v = (p, q, random.choice([False, True]), random.choice([False, True]),
             random.choice(["sin", "cos"]))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for p, q, doi, ben_trai, ham in gt:
        hoanh, tung = _toa_do_nua_duong_tron(p, q, doi, ben_trai)
        dapso, con_lai = (tung, hoanh) if ham == "sin" else (hoanh, tung)
        ten = r"\sin" if ham == "sin" else r"\cos"

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, lấy điểm "
                 r"$M\left( %s; %s \right)$ thuộc nửa đường tròn đơn vị. "
                 r"Tính $%s\widehat{xOM}$." % (_L(hoanh), _L(tung), ten))
        giai = (r"Với điểm $M\left( x_{0}; y_{0} \right)$ thuộc nửa đường tròn đơn vị thì "
                r"$\cos\widehat{xOM} = x_{0}$ và $\sin\widehat{xOM} = y_{0}$.\\ "
                r"Do đó $%s\widehat{xOM} = %s$." % (ten, _L(dapso)))
        dung = "$%s$" % _L(dapso)
        ds = _ba_nhieu(dung, ["$%s$" % _L(simplify(-dapso)),
                              "$%s$" % _L(con_lai),
                              "$%s$" % _L(simplify(-con_lai))])
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C3_B5_NB029_MC_C_01(socau, dang=1):
    """Biết sin và côsin của góc, tìm toạ độ điểm M trên nửa đường tròn đơn vị."""
    gt = []
    while len(gt) < socau:
        p, q = _cap_nguyen_to_cung_nhau()
        v = (p, q, random.choice([False, True]), random.choice([False, True]))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for p, q, doi, ben_trai in gt:
        hoanh, tung = _toa_do_nua_duong_tron(p, q, doi, ben_trai)
        diem = lambda x, y: r"$M\left( %s; %s \right)$" % (_L(x), _L(y))

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, lấy điểm $M$ thuộc nửa đường tròn đơn vị. "
                 r"Biết $\sin\widehat{xOM} = %s$ và $\cos\widehat{xOM} = %s$. "
                 r"Tìm toạ độ điểm $M$." % (_L(tung), _L(hoanh)))
        giai = (r"Điểm $M\left( x_{0}; y_{0} \right)$ trên nửa đường tròn đơn vị có "
                r"hoành độ là côsin và tung độ là sin của góc $\widehat{xOM}$:\\ "
                r"$x_{0} = \cos\widehat{xOM} = %s$, $y_{0} = \sin\widehat{xOM} = %s$.\\ "
                r"Vậy $M\left( %s; %s \right)$." % (_L(hoanh), _L(tung), _L(hoanh), _L(tung)))
        dung = diem(hoanh, tung)
        ds = _ba_nhieu(dung, [diem(tung, hoanh),                  # đổi chỗ hai toạ độ
                              diem(simplify(-hoanh), tung),       # sai dấu hoành độ
                              diem(hoanh, simplify(-tung))])      # tung độ âm: không ở nửa trên
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


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


def L10_C3_B6_TH032_MC_A_02(socau, dang=1):
    """Định lí côsin với góc BẤT KÌ: đáp số gần đúng, học sinh phải bấm máy.

    Biến thể này bổ sung cho _01 (số liệu đẹp, góc đặc biệt). Ba phương án
    nhiễu đổi lại theo ba lỗi học sinh hay mắc: quên dấu trừ, dùng sin thay
    côsin, quên nhân 2.
    """
    DAC_BIET = (30, 45, 60, 90, 120, 135, 150)
    gt = []
    while len(gt) < socau:
        a = random.randint(3, 19)
        b = a + random.randint(1, 5)
        C = random.randint(20, 160)
        if C in DAC_BIET or (a, b, C) in gt:
            continue
        gt.append((a, b, C))

    cauTN = ''
    for a, b, C in gt:
        r = math.radians(C)
        c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(r))
        dung = r"$AB \approx %s$" % _xx(c)
        giai = (r"Áp dụng định lí côsin trong tam giác $ABC$:\\ "
                r"$AB^{2} = CA^{2} + CB^{2} - 2\cdot CA\cdot CB\cdot\cos\widehat{C} "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %d^{\circ} \approx %s$.\\ "
                r"Vậy $AB \approx %s$."
                % (a, b, a, b, C, _xx(a*a + b*b - 2*a*b*math.cos(r)), _xx(c)))
        ds = _ba_nhieu(
            dung,
            [r"$AB \approx %s$" % _xx(math.sqrt(a*a + b*b + 2*a*b*math.cos(r))),
             r"$AB \approx %s$" % _xx(math.sqrt(a*a + b*b - 2*a*b*math.sin(r))),
             r"$AB \approx %s$" % _xx(math.sqrt(a*a + b*b - a*b*math.cos(r)))],
            buoc=lambda k: r"$AB \approx %s$" % _xx(c + k))
        debai = (r"Cho tam giác $ABC$ có $\widehat{C} = %d^{\circ}$, $CA = %d$ và $CB = %d$. "
                 r"Tính độ dài cạnh $AB$ (làm tròn đến hàng phần trăm)." % (C, a, b))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


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


def L10_C3_B6_VD036_MC_B_01(socau, dang=1):
    """Đo khoảng cách qua đầm lầy bằng ĐỊNH LÍ SIN (biết một cạnh và hai góc)."""
    gt = []
    while len(gt) < socau:
        b = random.randint(3, 19)
        A = random.randint(92, 117)
        C = random.randint(35, 69)
        if not (80 <= A + C <= 150) or (b, A, C) in gt:
            continue
        gt.append((b, A, C))

    cauTN = ''
    for b, A, C in gt:
        B = 180 - A - C
        sinB, sinC = math.sin(math.radians(B)), math.sin(math.radians(C))
        AB = b * sinC / sinB
        dung = r"$AB \approx %s\,\text{m}$" % _xx(AB)
        giai = (r"Trong tam giác $ABC$: "
                r"$\widehat{B} = 180^{\circ} - \widehat{A} - \widehat{C} "
                r"= 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$.\\ "
                r"Áp dụng định lí sin:\\ "
                r"$\dfrac{AB}{\sin \widehat{C}} = \dfrac{AC}{\sin \widehat{B}} "
                r"\Rightarrow AB = \dfrac{AC\cdot\sin \widehat{C}}{\sin \widehat{B}} "
                r"= \dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} \approx %s\,\text{(m)}$."
                % (A, C, B, b, C, B, _xx(AB)))
        ds = _ba_nhieu(
            dung,
            [r"$AB \approx %s\,\text{m}$" % _xx(b * sinB / sinC),   # lộn hai góc
             r"$AB \approx %s\,\text{m}$" % _xx(b * sinC),          # quên chia
             r"$AB \approx %s\,\text{m}$" % _xx(b * sinC + b)],
            buoc=lambda k: r"$AB \approx %s\,\text{m}$" % _xx(AB + k))
        debai = (r"Để đo khoảng cách từ $A$ đến $B$ ngang qua một đầm lầy, người ta chọn "
                 r"điểm $C$ như hình bên và đo được khoảng cách từ $A$ đến $C$ bằng "
                 r"$%d\,\text{m}$. Biết rằng từ điểm $A$ nhìn hai điểm $B$ và $C$ dưới một góc "
                 r"$%d^{\circ}$, từ điểm $C$ nhìn hai điểm $A$ và $B$ dưới một góc $%d^{\circ}$. "
                 r"Tính khoảng cách từ $A$ đến $B$ (làm tròn đến hàng phần trăm)."
                 % (b, A, C))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, HINH_DAM_LAY, 0, dang)
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


def L10_C3_B6_VD036_MC_C_01(socau, dang=1):
    """Bài toán chuyển động: tàu chạy hai chặng theo hai hướng, tính khoảng cách.

    Bản cũ hỏi người dùng bằng input() để chọn tự luận hay trắc nghiệm, và
    gọi luôn hàm ở cuối tệp - hai thứ đó làm treo cả ngân hàng khi nạp
    mô-đun, nên đã bỏ; ở đây cố định là câu trắc nghiệm.
    """
    gt = []
    while len(gt) < socau:
        v = (random.choice([40, 50, 70, 80]),          # hướng chặng 1: N goc1 E
             random.choice([10, 20, 40, 50, 70, 80]),  # hướng chặng 2: S goc2 E
             random.choice([20, 30, 40, 50, 60]),      # vận tốc chặng 1
             random.choice([20, 30, 40, 50, 60]),      # vận tốc chặng 2
             random.choice([30, 35, 40, 45, 50, 55]),  # thời gian chặng 1 (phút)
             random.randint(20, 49))                   # thời gian chặng 2 (phút)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for goc1, goc2, vt1, vt2, t1, t2 in gt:
        AB = vt1 * t1 / 60.0
        BC = vt2 * t2 / 60.0
        gocB = goc1 + goc2
        r = math.radians(gocB)
        AC2 = AB * AB + BC * BC - 2 * AB * BC * math.cos(r)
        AC = math.sqrt(AC2)
        dung = r"$%s\,\text{km}$" % _xx(AC)
        giai = (r"Hướng $N %d^{\circ} E$ đi từ $A$ tới $B$, nên nhìn từ $B$ thì hướng về $A$ là "
                r"$S %d^{\circ} W$; chặng sau tàu đi theo hướng $S %d^{\circ} E$. "
                r"Hai hướng đó nằm hai bên hướng nam nên\\ "
                r"$\widehat{ABC} = %d^{\circ} + %d^{\circ} = %d^{\circ}$.\\ "
                r"Quãng đường mỗi chặng (đổi phút ra giờ):\\ "
                r"$AB = %d\cdot\dfrac{%d}{60} = %s\,\text{(km)}$, "
                r"$BC = %d\cdot\dfrac{%d}{60} = %s\,\text{(km)}$.\\ "
                r"Áp dụng định lí côsin trong tam giác $ABC$:\\ "
                r"$AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos\widehat{ABC} "
                r"\approx %s$, suy ra $AC \approx %s\,\text{(km)}$."
                % (goc1, goc1, goc2, goc1, goc2, gocB,
                   vt1, t1, _xx(AB), vt2, t2, _xx(BC), _xx(AC2), _xx(AC)))
        ds = _ba_nhieu(
            dung,
            [r"$%s\,\text{km}$" % _xx(math.sqrt(AB*AB + BC*BC)),                      # coi như vuông
             r"$%s\,\text{km}$" % _xx(math.sqrt(AB*AB + BC*BC + 2*AB*BC*math.cos(r))),# quên dấu trừ
             r"$%s\,\text{km}$" % _xx(AB + BC)],                                      # cộng thẳng
            buoc=lambda k: r"$%s\,\text{km}$" % _xx(AC + k))
        debai = (r"Một tàu xuất phát từ bãi biển $A$, chạy theo hướng $N %d^{\circ} E$ với tốc độ "
                 r"$%d\,\text{km/h}$. Sau khi đi được $%d$ phút thì đến vị trí $B$, tàu chuyển "
                 r"sang hướng $S %d^{\circ} E$ với tốc độ $%d\,\text{km/h}$ và chạy tiếp $%d$ phút "
                 r"nữa thì đến đảo $C$. Khi đó tàu cách vị trí xuất phát khoảng bao nhiêu kilômét "
                 r"(làm tròn đến hàng phần trăm)?"
                 % (goc1, vt1, t1, goc2, vt2, t2))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN
