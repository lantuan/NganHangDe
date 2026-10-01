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
                ds.add(("%.2f" % lech).replace(".", DAU_THAP_PHAN))
        debai = (r"Dùng máy tính cầm tay, giá trị của $\%s %s$ (làm tròn đến hàng phần trăm) bằng"
                 % (ki, _goc(d)))
        giai = (r"Chuyển máy tính về chế độ \textbf{DEG} rồi bấm $\%s %s$, được $%s$."
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
                 r"sát và $T$ là điểm mà tia nhìn chạm mặt biển (hình vẽ minh hoạ, "
                 r"không đúng tỉ lệ)."
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
        cauTN += TL_answer_text(debai, ds_abcd, _hinh_trai_dat(), 0, dong)
    return cauTN


# ---- Bán kính Trái Đất / đường chân trời: MC + SA tách VD và VDC ----
# CLAUDE THEM 01/10/2026 - co Lan duyet cach hoi (VD: cho R, tinh goc ha / khoang cach
# toi chan troi; VDC: cho h va goc ha, tinh R). Cung mo ta "Dang" voi TL_E de khong ra
# chung mot de. Do cao lay xap xi so lieu thuc te (km).
_NUI_CHAN_TROI = [("Phan Xi Păng", 3.14), ("Pu Si Lung", 3.08), ("Pu Ta Leng", 3.05),
                  ("Ngọc Linh", 2.6), ("Chư Yang Sin", 2.44), ("Tây Côn Lĩnh", 2.42),
                  ("Lang Biang", 2.17), ("Mẫu Sơn", 1.54), ("Bạch Mã", 1.45), ("Bà Đen", 0.99)]
_R_TRAI_DAT = 6371


def _chon_nui(socau):
    """Chọn socau ngọn núi, không lặp khi còn đủ núi."""
    ds = random.sample(range(len(_NUI_CHAN_TROI)), min(socau, len(_NUI_CHAN_TROI)))
    while len(ds) < socau:
        ds.append(random.randrange(len(_NUI_CHAN_TROI)))
    return [_NUI_CHAN_TROI[i] for i in ds]


def _mo_dau_chan_troi(ten, h):
    return (r"Đứng trên đỉnh núi %s ở độ cao $h = %s\,\text{km}$ so với mực nước biển, một người "
            r"nhìn về phía biển thì thấy đường chân trời. Coi Trái Đất là khối cầu tâm $O$ bán kính "
            r"$R$; gọi $M$ là vị trí người quan sát và $T$ là điểm mà tia nhìn chạm mặt biển, "
            r"$\theta$ là góc hạ của tia nhìn $MT$ so với phương nằm ngang (hình vẽ minh hoạ, "
            r"không đúng tỉ lệ)." % (ten, _xx(h, 2)))


_GIAI_VUONG_T = (r"Tia nhìn chạm mặt biển ở đúng đường chân trời nên $MT$ là tiếp tuyến của "
                 r"đường tròn tâm $O$ tại $T$, do đó tam giác $OTM$ vuông tại $T$, có "
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
        debai = (_mo_dau_chan_troi(ten, h) + r" Biết $R = %d\,\text{km}$. Góc hạ $\theta$ (làm "
                 r"tròn đến hàng phần trăm của độ) bằng" % R)
        giai = (_GIAI_VUONG_T + "\\\\\n"
                r"Phương nằm ngang tại $M$ vuông góc với $OM$ nên "
                r"$\widehat{OMT} = 90^{\circ} - \theta$, suy ra "
                r"$\widehat{TOM} = 90^{\circ} - \widehat{OMT} = \theta$."
                "\\\\\n"
                r"Do đó $\cos\theta = \dfrac{OT}{OM} = \dfrac{R}{R + h} = \dfrac{%d}{%s}"
                r"\Rightarrow \theta \approx %s$." % (R, _xx(R + h, 2), dap))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_M_01(socau, dang=2):
    r"""Đường chân trời (mức VD): biết $R = 6371\,\text{km}$ và $h$, tính khoảng cách $MT$
    từ người quan sát tới đường chân trời (định lí Pythagore trong tam giác $OTM$ vuông tại $T$).

    CLAUDE THEM 01/10/2026 - co Lan duyet lai.
    """
    R = _R_TRAI_DAT
    cau = ""
    for ten, h in _chon_nui(socau):
        MT = math.sqrt((R + h) ** 2 - R ** 2)
        dap = str(_lt(MT))
        debai = (_mo_dau_chan_troi(ten, h) + r" Biết $R = %d\,\text{km}$. Tính khoảng cách $MT$ "
                 r"từ người quan sát tới đường chân trời (đơn vị km, làm tròn đến hàng đơn vị)." % R)
        giai = (_GIAI_VUONG_T + "\\\\\n"
                r"Theo định lí Pythagore: $MT = \sqrt{OM^{2} - OT^{2}} = "
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
         r"Phương nằm ngang tại $M$ vuông góc với $OM$ nên $\widehat{OMT} = 90^{\circ} - \theta$, "
         r"suy ra $\widehat{TOM} = \theta$."
         "\\\\\n"
         r"Do đó $\cos\theta = \dfrac{OT}{OM} = \dfrac{R}{R + h} \Rightarrow "
         r"\left(R + h\right)\cos\theta = R \Rightarrow R\left(1 - \cos\theta\right) = h\cos\theta$,"
         "\\\\\n"
         r"tức là $" + _CT_R_DUNG + r"$.")
    if R is not None:
        s += ("\\\\\n"
              r"Thay số: $R = \dfrac{%s\cdot\cos %s^{\circ}}{1 - \cos %s^{\circ}} \approx %s\,\text{(km)}$. "
              r"Vì $1 - \cos\theta$ rất bé nên khi bấm máy phải giữ đủ chữ số, không làm tròn sớm."
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
        debai = (_mo_dau_chan_troi(ten, h) + r" Người đó đo được $\theta = %s^{\circ}$. Bán kính "
                 r"$R$ của Trái Đất được tính theo $h$ và $\theta$ bởi công thức nào sau đây?"
                 % _xx(theta, 2))
        nhieu = random.sample(_CT_R_NHIEU, 3)
        cau += MC_SA_answer_const(debai, _CT_R_DUNG, nhieu, _giai_tim_R(), _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_N_01(socau, dang=2):
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
        debai = (_mo_dau_chan_troi(ten, h) + r" Người đó đo được $\theta = %s^{\circ}$. Tính bán "
                 r"kính $R$ của Trái Đất (đơn vị km, làm tròn đến hàng đơn vị)." % _xx(theta, 2))
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
        debai = (r"Cho góc $\alpha$ thoả mãn $\sin\alpha = %s$ và $%s$. Xét tính đúng sai của "
                 r"các khẳng định sau:" % (_L(sn), khoang))
        # a) NB - quan he hai goc bu nhau, phu nhau
        ly_a = (r"Hai góc bù nhau có sin bằng nhau: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha = %s$; "
                r"hai góc phụ nhau: $\cos\left(90^{\circ} - \alpha\right) = \sin\alpha = %s$." % (_L(sn), _L(sn)))
        y1 = _phat_bieu(
            [(r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a), (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a)],
            [(r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a), (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a),
             (r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(1 - sn), ly_a), (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(1 - sn), ly_a)])
        # b) TH - he thuc co ban va xet dau cos theo loai goc
        ly_cos = (r"$\cos^{2}\alpha = 1 - \left(%s\right)^{2} = %s$, và vì $\alpha$ %s nên "
                  r"$\cos\alpha %s 0$, do đó $\cos\alpha = %s$."
                  % (_L(sn), _L(1 - sn ** 2), "tù" if tu else "nhọn", "<" if tu else ">", _L(cs)))
        y2 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", cs, ly_cos,
                            [(-cs, "Sai dấu"), ((-1 if tu else 1) * (1 - sn), "Quên bình phương"),
                             ((-1 if tu else 1) * cs ** 2, "Quên lấy căn")]),
                     _tf_ct(r"$\cos^{2}\alpha = %s$", cs ** 2, ly_cos, [(1 + sn ** 2, "Sai dấu trong $1 - \\sin^{2}\\alpha$"), (sn ** 2, "Nhầm $\\cos^{2}\\alpha = \\sin^{2}\\alpha$")]))
        # c) VD - dung ket qua cua b) de tinh tan, cot
        ly_c = ly_cos + r" $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$, $\cot\alpha = \dfrac{1}{\tan\alpha} = %s$." % (_L(tn), _L(ct))
        y3 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", tn, ly_c, [(1 / tn, "Đảo tử và mẫu"), (-tn, "Sai dấu"), (sn * cs, "Nhầm $\\tan\\alpha = \\sin\\alpha\\cdot\\cos\\alpha$")]),
                     _tf_ct(r"$\cot\alpha = %s$", ct, ly_c, [(tn, "Nhầm $\\cot\\alpha = \\tan\\alpha$"), (-ct, "Sai dấu")]))
        # d) VDC - thay ca sin va cos vao bieu thuc phan thuc (2 bieu thuc)
        dung, sai = [], []
        for bt, P, Ps in bts:
            ly = r"Thay $\sin\alpha = %s$, $\cos\alpha = %s$ (ý b) vào biểu thức, được $%s$." % (_L(sn), _L(cs), _L(P))
            d_, s_ = _tf_ct("$" + bt + " = %s$", P, ly, Ps)
            dung += d_
            sai += s_
        y4 = _phat_bieu(dung, sai)
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\cos A = %s$. Xét tính đúng sai "
                 r"của các khẳng định sau:" % (b, c, _L(cA)))
        # a) NB - sin A tu he thuc co ban (sin A > 0)
        ly_a = r"$\sin A = \sqrt{1 - \cos^{2}A} = %s$ (vì $0^{\circ} < A < 180^{\circ}$ nên $\sin A > 0$)." % _L(sA)
        y1 = _tf_gop(_tf_ct(r"$\sin A = %s$", sA, ly_a, [(-sA, "$\\sin A$ luôn dương"), (1 - abs(cA), "Quên bình phương"), (sA ** 2, "Quên lấy căn")]),
                     _tf_ct(r"$\sin^{2}A = %s$", sA ** 2, ly_a, [(1 + cA ** 2, "Sai dấu")]))
        # b) TH - dinh li cosin
        ly_b = r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %d$." % (
            b, c, b, c, (r"\left(%s\right)" % _L(cA)) if cA < 0 else _L(cA), a2)
        y2 = _tf_gop(_tf_ct(r"$BC = %s$", a, ly_b,
                            [(sqrt(Integer(b * b + c * c + 2 * b * c * cA)), "Sai dấu"), (sqrt(Integer(b * b + c * c)), "Quên số hạng chứa $\\cos A$"),
                             (sqrt(b * b + c * c - b * c * cA), "Quên hệ số 2")],
                            them=[r"$BC^{2} = %d$" % a2]))
        # c) VD - dien tich, khoang cach
        ly_c = (r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = \dfrac{1}{2}\cdot %d\cdot %d\cdot %s = %s$; khoảng cách từ $B$ đến $AC$ là "
                r"$\dfrac{2S}{AC} = AB\cdot\sin A = %s$." % (c, b, _L(sA), _L(S), _L(c * sA)))
        d1, s1 = _tf_ct(r"Diện tích tam giác $ABC$ bằng $%s$", S, ly_c,
                        [(2 * S, "Quên hệ số $\\dfrac{1}{2}$"), (abs(Rational(1, 2) * b * c * cA), "Nhầm $\\sin A$ với $\\cos A$"),
                         (Rational(1, 2) * b * c * sA ** 2, "Dùng nhầm $\\sin^{2}A$")])
        d2, s2 = _tf_ct(r"Khoảng cách từ $B$ đến đường thẳng $AC$ bằng $%s$", c * sA, ly_c,
                        [(b * sA, "Nhầm cạnh"), (c * abs(cA), "Nhầm $\\sin A$ với $\\cos A$")])
        y3 = _phat_bieu(d1 + d2, s1 + s2)
        # d) VDC - ban kinh ngoai tiep (can BC tu y b)
        ly_d = ly_b + r" $R = \dfrac{BC}{2\sin A} = \dfrac{%s}{2\cdot %s} = %s$." % (_L(a), _L(sA), _L(R))
        d1, s1 = _tf_ct(r"Bán kính đường tròn ngoại tiếp tam giác bằng $%s$", R, ly_d,
                        [(simplify(2 * R), "Quên chia 2"), (simplify(a / (2 * abs(cA))), "Nhầm $\\sin A$ với $\\cos A$"),
                         (simplify(sqrt(Integer(b * b + c * c + 2 * b * c * cA)) / (2 * sA)), "Tính sai $BC$ (sai dấu)")])
        d2, s2 = _tf_ct(r"Đường tròn ngoại tiếp tam giác có đường kính bằng $%s$", simplify(2 * R), ly_d,
                        [(R, "Đó là bán kính"), (simplify(a / abs(cA)), "Nhầm $\\sin A$ với $\\cos A$")])
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
        debai = (r"Cho tam giác $ABC$ vuông tại $B$, có $\widehat{A} = %s$ và $BC = %d$. Xét tính "
                 r"đúng sai của các khẳng định sau:" % (_goc(A), a))
        # a) NB - tổng ba góc, cạnh huyền
        ly_a = r"$\widehat{C} = 180^{\circ} - 90^{\circ} - %s = %s$; cạnh đối diện góc vuông $B$ là cạnh huyền $AC$." % (_goc(A), _goc(C))
        y1 = _phat_bieu(
            [(r"$\widehat{C} = %s$" % _goc(C), ly_a), (r"$\widehat{A} + \widehat{C} = 90^{\circ}$", ly_a), (r"$AC$ là cạnh huyền", ly_a)],
            [(r"$\widehat{C} = %s$" % _goc(A), ly_a), (r"$\widehat{C} = %s$" % _goc(180 - A), ly_a), (r"$AB$ là cạnh huyền", ly_a),
             (r"$\widehat{A} + \widehat{C} = 180^{\circ}$", ly_a)])
        # b) TH - định lí sin
        ly_b = r"$R = \dfrac{BC}{2\sin A} = \dfrac{%d}{2\cdot %s} = %s$, $AC = 2R = %s$ (cạnh huyền là đường kính)." % (a, _L(sA), _L(R), _L(b))
        y2 = _tf_gop(_tf_ct(r"Bán kính đường tròn ngoại tiếp $R = %s$", R, ly_b,
                            [(2 * R, "Đó là $2R$"), (simplify(a / (2 * _gtlg("cos", A))), "Nhầm $\\sin A$ với $\\cos A$"),
                             (simplify(a * sA / 2), "Nhầm $R = \\dfrac{BC\\cdot\\sin A}{2}$")]),
                     _tf_ct(r"$AC = %s$", b, ly_b, [(R, "Quên nhân 2"), (Integer(a), "Nhầm cạnh")]))
        # c) VD - cạnh AB
        ly_c = r"$AC = 2R = %s$ (cạnh huyền là đường kính), $AB = 2R\sin C = %s$." % (_L(b), _L(c))
        y3 = _tf_gop(_tf_ct(r"$AB = %s$", c, ly_c,
                            [(simplify(b * _gtlg("sin", A)), "Dùng nhầm góc $A$ (đó là $BC$)"), (b, "Lấy cạnh huyền"),
                             (simplify(a * _gtlg("tan", A)), "Nhầm $AB = BC\\cdot\\tan A$")],
                            them=[r"$AB^{2} = %s$" % _L(simplify(c ** 2))]))
        # d) VDC - diện tích, đường cao ứng với cạnh huyền
        hB = simplify(2 * S / b)
        ly_d = (r"Hai cạnh góc vuông là $BC$ và $AB$: $S = \dfrac{1}{2}\cdot %d\cdot %s = %s$; đường cao kẻ từ $B$ là "
                r"$h = \dfrac{2S}{AC} = %s$." % (a, _L(c), _L(S), _L(hB)))
        y4 = _tf_gop(_tf_ct(r"Diện tích tam giác $ABC$ bằng $%s$", S, ly_d,
                            [(2 * S, "Quên hệ số $\\dfrac{1}{2}$"), (simplify(Rational(1, 2) * a * b), "Dùng nhầm cạnh huyền"), (S / 2, "Chia thừa 2")]),
                     _tf_ct(r"Đường cao kẻ từ $B$ của tam giác $ABC$ bằng $%s$", hB, ly_d,
                            [(hB / 2, "Quên nhân 2"), (simplify(2 * S / a), "Chia nhầm cạnh")]))
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
    ten = {0: "bắc", 90: "đông", 180: "nam", 270: "tây"}
    if huong in ten:
        return (r"hướng %s" % ten[huong],
                r"hướng %s ứng với $%d^{\circ}$" % (ten[huong], huong))
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
    return r"hướng $%s$" % kh, r"$%s$ ứng với $%s$" % (kh, doi)


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
    return (r"Đổi các hướng ra góc tính từ hướng bắc theo chiều kim đồng hồ: %s; %s. "
            r"Tại $B$ tàu đã đổi hướng một góc $%s$, nên "
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
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\cos A = %s$." % (b, c, _L(cA)))
        ds_abcd = [
            (r"Tính độ dài cạnh $BC$.", _L(a),
             r"$BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A = %d^{2} + %d^{2} - "
             r"2\cdot %d\cdot %d\cdot %s = %d$, nên $BC = %s$." % (b, c, b, c, cA_, a2, _L(a))),
            (r"Tính $\cos B$.", _L(cB),
             r"$\cos B = \dfrac{BC^{2} + AB^{2} - AC^{2}}{2\cdot BC\cdot AB} = "
             r"\dfrac{%d + %d - %d}{2\cdot %s\cdot %d} = %s$." % (a2, c * c, b * b, _L(a), c, _L(cB))),
            (r"Tính $\cos C$.", _L(cC),
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$ và $AB = %d$. Côsin của góc có số đo "
                 r"lớn nhất của tam giác bằng" % (canh["A"], canh["B"], canh["C"]))
        giai = (r"Cạnh dài nhất là $%s = %d$ nên góc lớn nhất là góc $%s$ (đối diện cạnh đó).\\ "
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


def _cau_he_thuc_goc(socau, dang, dang_nhan_tu):
    cauTN = ""
    for _ in range(socau):
        k, g = random.choice(_HE_SO_GOC)
        X = random.choice("ABC")
        d, u, v = _BA_DINH[X]                     # d đối diện góc X
        uv = u + v if u < v else v + u
        u, v = sorted([u, v])
        if dang_nhan_tu:
            he = simplify(2 + k)
            ve = _he_so_tex(he, uv) if he != 0 else "0"
            debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$ thoả mãn "
                     r"$(%s + %s + %s)(%s + %s - %s) = %s$. Số đo góc $%s$ bằng"
                     % (u, v, d, u, v, d, ve, X))
            buoc1 = (r"Vế trái bằng $(%s + %s)^{2} - %s^{2} = %s^{2} + %s^{2} + 2%s - %s^{2}$, nên "
                     r"$%s^{2} + %s^{2} - %s^{2} = %s$.\\ "
                     % (u, v, d, u, v, uv, d, u, v, d, _he_so_tex(k, uv) if k != 0 else "0"))
        else:
            dang_viet = random.choice([0, 1])
            if dang_viet == 0 and k != 0:
                ve = _he_so_tex(-k, uv)
                ve = ("+ " + ve) if not ve.startswith("-") else ("- " + ve[1:])
                debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$ thoả mãn "
                         r"$%s^{2} = %s^{2} + %s^{2} %s$. Số đo góc $%s$ bằng" % (d, u, v, ve, X))
            else:
                ve = _he_so_tex(k, uv) if k != 0 else "0"
                debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$ thoả mãn "
                         r"$%s^{2} + %s^{2} - %s^{2} = %s$. Số đo góc $%s$ bằng" % (u, v, d, ve, X))
            buoc1 = (r"Từ giả thiết: $%s^{2} + %s^{2} - %s^{2} = %s$.\\ "
                     % (u, v, d, _he_so_tex(k, uv) if k != 0 else "0"))
        giai = (buoc1 + r"Theo hệ quả định lí côsin: $\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s} "
                r"= %s$, nên $\widehat{%s} = %s$." % (X, u, v, d, uv, _L(k / 2), X, _goc(g)))
        dung = "$%s$" % _goc(g)
        khac = [x for _, x in _HE_SO_GOC if x not in (g, 180 - g)]
        random.shuffle(khac)
        ung = ([] if g == 90 else ["$%s$" % _goc(180 - g)]) + ["$%s$" % _goc(x) for x in khac]
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $\widehat{B} = %s$ và $\widehat{C} = %s$."
                 % (a, _goc(B), _goc(C)))
        ds_abcd = [
            (r"Tính số đo góc $A$.", _goc(A),
             r"$\widehat{A} = 180^{\circ} - \left(%s + %s\right) = %s$." % (_goc(B), _goc(C), _goc(A))),
            (r"Tính độ dài cạnh $AC$.", _L(b),
             r"Định lí sin: $\dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$ nên "
             r"$AC = \dfrac{BC\cdot\sin B}{\sin A} = \dfrac{%d\cdot %s}{%s} = %s$."
             % (a, _L(sB), _L(sA), _L(b))),
            (r"Tính bán kính $R$ của đường tròn ngoại tiếp tam giác $ABC$.", _L(R),
             r"$\dfrac{BC}{\sin A} = 2R$ nên $R = \dfrac{%d}{2\cdot %s} = %s$." % (a, _L(sA), _L(R))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C3_B6_TH034_MC_A_02(socau, dang=1):
    r"""Chọn công thức diện tích ĐÚNG (hoặc SAI) trong bốn công thức.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH034_MC_A, theo cac cau nhan
    dang cong thuc trong phan trac nghiem giao an Bai 6. Co Lan duyet.
    """
    DUNG = [r"$S = \dfrac{1}{2}ab\sin C$", r"$S = \dfrac{1}{2}bc\sin A$", r"$S = \dfrac{1}{2}ca\sin B$",
            r"$S = \dfrac{abc}{4R}$", r"$S = pr$", r"$S = \sqrt{p(p-a)(p-b)(p-c)}$",
            r"$S = \dfrac{1}{2}a\cdot h_a$", r"$S = \dfrac{1}{2}b\cdot h_b$"]
    SAI = [(r"$S = \dfrac{1}{2}ab\sin A$", r"góc trong công thức phải là góc XEN GIỮA hai cạnh $a$, $b$, tức góc $C$"),
           (r"$S = \dfrac{1}{2}bc\cos A$", r"phải là $\sin A$ chứ không phải $\cos A$"),
           (r"$S = \dfrac{abc}{2R}$", r"đúng phải là $\dfrac{abc}{4R}$"),
           (r"$S = \dfrac{abc}{R}$", r"đúng phải là $\dfrac{abc}{4R}$"),
           (r"$S = 2pr$", r"$p$ là NỬA chu vi nên $S = pr$"),
           (r"$S = \sqrt{p(p+a)(p+b)(p+c)}$", r"công thức Heron là $\sqrt{p(p-a)(p-b)(p-c)}$"),
           (r"$S = a\cdot h_a$", r"thiếu hệ số $\dfrac{1}{2}$"),
           (r"$S = \dfrac{1}{2}ab\sin B$", r"góc xen giữa hai cạnh $a$, $b$ là góc $C$")]
    cauTN = ""
    for _ in range(socau):
        hoi_sai = random.choice([True, False])
        if hoi_sai:
            sai, ly_do = random.choice(SAI)
            dung, nhieu = sai, random.sample(DUNG, 3)
            debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$, diện tích $S$, nửa chu vi $p$, "
                     r"bán kính đường tròn ngoại tiếp, nội tiếp lần lượt là $R$, $r$. Công thức nào sau "
                     r"đây \textbf{sai}?")
            giai = r"Công thức %s sai vì %s. Ba công thức còn lại đều đúng." % (sai, ly_do)
        else:
            dung = random.choice(DUNG)
            ba = random.sample(SAI, 3)
            nhieu = [x[0] for x in ba]
            debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$, diện tích $S$, nửa chu vi $p$, "
                     r"bán kính đường tròn ngoại tiếp, nội tiếp lần lượt là $R$, $r$. Công thức nào sau "
                     r"đây đúng?")
            giai = (r"%s là công thức đúng. Các công thức còn lại sai: " % dung
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
        debai = (r"Cho tam giác $ABC$ có $BC = %s$, $CA = %d$ và $\widehat{C} = %s$. Xét tính đúng sai "
                 r"của các khẳng định sau:" % (_L(a), m, _goc(C)))
        cC_ = (r"\left(%s\right)" % _L(cC)) if cC < 0 else _L(cC)
        # a) NB - công thức diện tích hai cạnh, góc xen giữa
        ly_a = r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\sin C = \dfrac{1}{2}\cdot %s\cdot %d\cdot %s = %s$." % (_L(a), m, _L(sC), _L(S))
        d1, s1 = _tf_ct(r"Diện tích tam giác $ABC$ bằng $%s$", S, ly_a,
                        [(2 * S, "Quên hệ số $\\dfrac{1}{2}$"), (simplify(abs(a * b * cC) / 2), "Nhầm $\\sin C$ với $\\cos C$")],
                        them=[r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\sin C$"])
        s1.append((r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\cos C$", ly_a))
        s1.append((r"$S = BC\cdot CA\cdot\sin C$", ly_a))
        y1 = _phat_bieu(d1, s1)
        # b) TH - đường cao
        ly_b = r"$h_a = \dfrac{2S}{BC} = \dfrac{2\cdot %s}{%s} = %s$ (cũng bằng $CA\cdot\sin C$)." % (_L(S), _L(a), _L(ha))
        y2 = _tf_gop(_tf_ct(r"Đường cao kẻ từ $A$ có độ dài $h_a = %s$", ha, ly_b,
                            [(simplify(S / a), "Quên nhân 2"), (simplify(2 * S / b), "Chia nhầm cạnh $CA$"), (simplify(b * abs(cC)), "Nhầm $\\sin$ với $\\cos$")],
                            them=[r"$h_a = CA\cdot\sin C$"]))
        # c) VD - định lí côsin
        ly_c = (r"$AB^{2} = BC^{2} + CA^{2} - 2\cdot BC\cdot CA\cdot\cos C = %s + %d - 2\cdot %s\cdot %d"
                r"\cdot %s = %s$, nên $AB = %s$." % (_L(a ** 2), m * m, _L(a), m, cC_, _L(c2), _L(c)))
        y3 = _tf_gop(_tf_ct(r"$AB = %s$", c, ly_c,
                            [(sqrt(c2_sai), "Nhầm dấu"), (sqrt(simplify(a ** 2 + b ** 2)), "Quên số hạng chứa $\\cos C$"),
                             (sqrt(simplify(a ** 2 + b ** 2 - a * b * cC)), "Quên hệ số 2")],
                            them=[r"$AB^{2} = %s$" % _L(c2)]))
        # d) VDC - bán kính ngoại tiếp
        ly_d = ly_c + r" Định lí sin: $\dfrac{AB}{\sin C} = 2R$, nên $R = \dfrac{%s}{2\cdot %s} = %s$." % (_L(c), _L(sC), _L(R))
        y4 = _tf_gop(_tf_ct(r"Bán kính đường tròn ngoại tiếp tam giác $ABC$ bằng $%s$", R, ly_d,
                            [(simplify(2 * R), "Quên chia 2"), (simplify(c / (2 * abs(cC))), "Nhầm $\\sin C$ với $\\cos C$"),
                             (simplify(sqrt(c2_sai) / (2 * sC)), "Tính sai $AB$ (nhầm dấu)")]),
                     _tf_ct(r"Đường kính đường tròn ngoại tiếp tam giác $ABC$ bằng $%s$", simplify(2 * R), ly_d, [(R, "Đó là bán kính")]))
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
        debai = (r"Một tàu cá xuất phát từ đảo $A$, chạy $%d\,\text{km}$ theo %s đến đảo $B$, rồi chuyển "
                 r"sang %s chạy tiếp $%d\,\text{km}$ đến ngư trường $C$. Xét tính đúng sai của các khẳng "
                 r"định sau:" % (d1, t1, t2, d2))
        g_B = _giai_goc_doi_huong(h1, h2, delta)
        cB = math.cos(math.radians(B))
        sinA = d2 * math.sin(math.radians(B)) / AC
        # a) NB - đọc góc đổi hướng, góc ABC
        x1, x2 = _n2_lech_truc(h1), _n2_lech_truc(h2)
        sai = [(r"$\widehat{ABC} = %s$" % _goc(delta), "Đó là góc đổi hướng. " + g_B)]
        for g in (x1 + x2, abs(x1 - x2), 180 - x1 - x2):
            if 0 < g < 180 and g != B:
                sai.append((r"$\widehat{ABC} = %s$" % _goc(g), g_B))
        if delta != 180 - delta:
            sai.append((r"Tại $B$ tàu đổi hướng một góc $%s$" % _goc(180 - delta), g_B))
        y1 = _phat_bieu([(r"$\widehat{ABC} = %s$" % _goc(B), g_B), (r"Tại $B$ tàu đổi hướng một góc $%s$" % _goc(delta), g_B)], sai)
        # b) TH - định lí côsin
        giai_AC = r"Định lí côsin: $AC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s$." % (d1, d2, d1, d2, _goc(B))
        y2 = _tf_gop(_tf_so(r"Khoảng cách $AC \approx %s$", AC, 1, giai_AC,
                            [(math.sqrt(d1 * d1 + d2 * d2 + 2 * d1 * d2 * cB), "Sai dấu"), (math.sqrt(d1 * d1 + d2 * d2), "Quên số hạng chứa $\\cos B$"),
                             (math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * math.cos(math.radians(delta))), "Dùng nhầm góc đổi hướng")],
                            dv=r"\,\text{km}", bdt=r"Khoảng cách $AC$ %s $%s$"))
        # c) VD - định lí sin tìm góc BAC
        giai_A = (giai_AC + r" Định lí sin: $\sin\widehat{BAC} = \dfrac{BC\cdot\sin B}{AC} \approx %s$; góc $B$ không nhọn nên "
                  r"$\widehat{BAC}$ nhọn." % _xx(sinA, 4))
        y3 = _tf_gop(_tf_so(r"$\widehat{BAC} \approx %s$", gA, 0, giai_A,
                            [(180 - B - gA, "Đó là góc $C$"), (180 - gA, "Lấy nhầm nghiệm góc tù"),
                             (90 - gA, "Nhầm $\\sin$ với $\\cos$ khi bấm máy")],
                            dv=r"^{\circ}", bdt=r"$\widehat{BAC}$ %s $%s$"))
        # d) VDC - hướng từ A đến C
        phia = "phải" if re_phai else "trái"
        giai_h = (r"Tàu rẽ sang %s tại $B$ nên $C$ nằm lệch về bên %s của tia $AB$: hướng $AC$ ứng với "
                  r"$%s$ (tính từ hướng bắc theo chiều kim đồng hồ), tức là %s."
                  % (phia, phia, _cong_goc(h1, gA_n if re_phai else -gA_n), tAC))
        dung = [(r"Hướng từ $A$ đến $C$ là %s" % tAC[6:], giai_h),
                (r"Hướng từ $A$ đến $C$ hợp với hướng bắc (theo chiều kim đồng hồ) một góc $%s$" % _goc(hAC), giai_h)]
        sai = []
        for hs, ghi in (((h1 - gA_n) % 360 if re_phai else (h1 + gA_n) % 360, "Lệch nhầm phía"), (h2 % 360, "Đó là hướng chặng thứ hai"),
                        (h1 % 360, "Đó là hướng chặng thứ nhất"), ((hAC + 180) % 360, "Đó là hướng từ $C$ về $A$")):
            if hs % 90 and hs != hAC:
                ts, _ = _huong_sang_phuong_vi(hs)
                sai.append((r"Hướng từ $A$ đến $C$ là %s" % ts[6:], ghi + ". " + giai_h))
        sai.append((r"Hướng từ $A$ đến $C$ hợp với hướng bắc (theo chiều kim đồng hồ) một góc $%s$" % _goc((360 - hAC) % 360),
                    "Tính ngược chiều kim đồng hồ. " + giai_h))
        y4 = _phat_bieu(dung, sai)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C3_B6_VD036_MC_C_02(socau, dang=1):
    r"""Hai phương tiện cùng xuất phát từ một điểm, đi theo HAI HƯỚNG LA BÀN
    khác nhau; sau một thời gian cách nhau bao xa (định lí côsin).

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD036_MC_C, theo bai "hai may bay:
    450 km/h huong tay, 630 km/h huong N25W, sau 90 phut" trong giao an Bai 6.
    Co Lan duyet.
    """
    BOI_CANH = [("Hai máy bay cùng cất cánh từ một sân bay $O$", "máy bay", "km/h", "km",
                 list(range(300, 901, 50)), [30, 45, 60, 90, 120]),
                ("Hai chiếc tàu cùng rời cảng $O$", "tàu", "km/h", "km",
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
        tg = ("%d phút" % t) if t < 60 or t % 60 else ("%d giờ" % (t // 60))
        debai = (r"%s. Chiếc thứ nhất đi theo %s với vận tốc $%d$ %s, chiếc thứ hai đi theo %s với vận "
                 r"tốc $%d$ %s. Sau %s, hai %s cách nhau khoảng bao nhiêu ki-lô-mét (làm tròn đến hàng "
                 r"đơn vị)? Giả sử hai %s chuyển động thẳng đều, cùng độ cao."
                 % (mo, t1, v1, dv_v, t2, v2, dv_v, tg, ten, ten))
        a1, a2 = h1 % 360, h2 % 360
        lon, nho = max(a1, a2), min(a1, a2)
        tinh = (r"%d^{\circ} - %d^{\circ} = %d^{\circ}" % (lon, nho, goc) if lon - nho <= 180 else
                r"360^{\circ} - (%d^{\circ} - %d^{\circ}) = %d^{\circ}" % (lon, nho, goc))
        giai = (r"Sau %s: $OA = %d\cdot\dfrac{%d}{60} = %s\,\text{km}$, $OB = %d\cdot\dfrac{%d}{60} = "
                r"%s\,\text{km}$.\\ Đổi hướng ra góc tính từ hướng bắc theo chiều kim đồng hồ: %s; %s, "
                r"nên $\widehat{AOB} = %s$.\\ Định lí côsin: $AB^{2} = OA^{2} + OB^{2} - 2\cdot OA\cdot OB\cdot"
                r"\cos %s \approx %s$, suy ra $AB \approx %s\,\text{km}$."
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
        phia = "phải" if re_phai else "trái"
        debai = (r"Một tàu xuất phát từ cảng $A$, chạy theo %s với vận tốc $%d\,\text{km/h}$. Sau $%d$ phút "
                 r"tàu tới $B$ thì chuyển sang %s, chạy với vận tốc $%d\,\text{km/h}$ thêm $%d$ phút nữa "
                 r"thì tới đảo $C$." % (tt1, v1, t1, tt2, v2, t2))
        ds_abcd = [
            (r"Tính quãng đường $AB$, $BC$ và số đo góc $\widehat{ABC}$.",
             r"AB = %s\,\text{km},\ BC = %s\,\text{km},\ \widehat{ABC} = %s" % (_xx(d1, 2), _xx(d2, 2), _goc(B)),
             r"$AB = %d\cdot\dfrac{%d}{60} = %s\,\text{km}$, $BC = %d\cdot\dfrac{%d}{60} = %s\,\text{km}$.\\ "
             % (v1, t1, _xx(d1, 2), v2, t2, _xx(d2, 2)) + _giai_goc_doi_huong(h1, h2, delta)),
            (r"Tính khoảng cách từ cảng $A$ tới đảo $C$ (làm tròn đến hàng phần mười).",
             r"AC \approx %s\,\text{km}" % _xx(AC, 1),
             r"Định lí côsin: $AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos %s \approx %s$, "
             r"nên $AC \approx %s\,\text{km}$." % (_goc(B), _xx(AC * AC, 2), _xx(AC, 1))),
            (r"Xác định hướng từ cảng $A$ tới đảo $C$ (làm tròn số đo góc đến hàng đơn vị).",
             tAC[6:].strip("$") if "$" in tAC else tAC,
             r"Định lí sin: $\sin\widehat{BAC} = \dfrac{BC\cdot\sin B}{AC} \approx %s$, góc $B$ không nhọn "
             r"nên $\widehat{BAC} \approx %d^{\circ}$.\\ Tàu rẽ sang %s tại $B$ nên hướng $AC$ ứng với $%s$ "
             r"(tính từ hướng bắc), tức là %s." % (_xx(sinA, 4), gA_n, phia,
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
        debai = (r"Trên nóc một toà nhà có một cột ăng-ten $BC$ cao $%d\,\text{m}$ ($C$ là chân cột, nằm trên "
                 r"nóc nhà). Từ vị trí quan sát $A$ cao $%d\,\text{m}$ so với mặt đất, người ta nhìn thấy "
                 r"đỉnh $B$ và chân $C$ của cột với các góc nâng lần lượt là $%s$ và $%s$ so với phương "
                 r"nằm ngang." % (d, h0, _goc(al), _goc(be)))
        ds_abcd = [
            (r"Tính các góc của tam giác $ABC$.",
             r"\widehat{A} = %s,\ \widehat{B} = %s,\ \widehat{C} = %s" % (_goc(A), _goc(B), _goc(C)),
             r"Gọi $H$ là hình chiếu của $A$ lên đường thẳng $BC$ (thẳng đứng), $AH$ nằm ngang.\\ "
             r"$\widehat{BAC} = %s - %s = %s$; tam giác $ABH$ vuông tại $H$ nên "
             r"$\widehat{ABC} = 90^{\circ} - %s = %s$;\\ $\widehat{ACB} = 180^{\circ} - %s - %s = %s$."
             % (_goc(al), _goc(be), _goc(A), _goc(al), _goc(B), _goc(A), _goc(B), _goc(C))),
            (r"Tính độ dài $AC$ (làm tròn đến hàng phần trăm).", r"AC \approx %s\,\text{m}" % _xx(AC, 2),
             r"Định lí sin trong tam giác $ABC$: $\dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$ nên "
             r"$AC = \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (d, _goc(B), _goc(A), _xx(AC, 2))),
            (r"Tính chiều cao của toà nhà (làm tròn đến hàng phần mười).", r"\approx %s\,\text{m}" % _xx(cao, 1),
             r"Tam giác $ACH$ vuông tại $H$: $CH = AC\cdot\sin %s \approx %s\,\text{m}$.\\ Chiều cao toà nhà "
             r"(từ mặt đất tới $C$) là $%d + CH \approx %s\,\text{m}$." % (_goc(be), _xx(CH, 2), h0, _xx(cao, 1))),
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
        be = random.choice([20, 25, 30, 35, 40])
        al = be + random.choice([15, 20, 25, 30])
        if al > 70:
            continue
        AC = h * math.cos(math.radians(al)) / math.sin(math.radians(al - be))
        cao = AC * math.sin(math.radians(be))
        dung = _mot_le_m(cao)
        ung = [_mot_le_m(AC), _mot_le_m(cao + h), _mot_le_m(AC * math.cos(math.radians(be))),
               _mot_le_m(h * math.sin(math.radians(al)) / math.sin(math.radians(al - be)) * math.sin(math.radians(be)))]
        nhieu = _ba_nhieu(dung, ung, buoc=lambda k: _mot_le_m(cao + 3.7 * k))
        so += 1
        if random.random() < 0.5:
            mo = (r"Từ điểm $A$ ở chân đồi nhìn đỉnh $B$ và chân $C$ của tháp với các góc nâng lần lượt là "
                  r"$%s$ và $%s$." % (_goc(al), _goc(be)))
            doi = r""
        else:
            mo = (r"Đỉnh tháp $B$ và chân tháp $C$ nhìn điểm $A$ ở chân đồi dưới các góc lần lượt bằng "
                  r"$%s$ và $%s$ so với phương thẳng đứng." % (_goc(90 - al), _goc(90 - be)))
            doi = (r"Góc nhìn so với phương thẳng đứng là $%s$ và $%s$ nên các góc nâng từ $A$ là "
                   r"$\alpha = 90^{\circ} - %s = %s$, $\beta = 90^{\circ} - %s = %s$.\\ "
                   % (_goc(90 - al), _goc(90 - be), _goc(90 - al), _goc(al), _goc(90 - be), _goc(be)))
        debai = (r"Trên đỉnh một ngọn đồi có một cái tháp $BC$ cao $%d\,\text{m}$ ($C$ là chân tháp). %s Gọi $H$ "
                 r"là hình chiếu của $C$ lên mặt phẳng nằm ngang qua $A$. Chiều cao $CH$ của ngọn đồi gần nhất "
                 r"với giá trị nào (làm tròn đến hàng phần mười)?" % (h, mo))
        giai = (doi + r"Trong tam giác $ABC$: $\widehat{BAC} = %s - %s = %s$, $\widehat{ABC} = 90^{\circ} - %s "
                r"= %s$.\\ Định lí sin: $AC = \dfrac{BC\cdot\sin\widehat{ABC}}{\sin\widehat{BAC}} = "
                r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$.\\ Tam giác $ACH$ vuông tại $H$: "
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
        debai = (r"Bạn An đứng trên nóc một toà nhà cao $%d\,\text{m}$, bạn Bình đứng ở chân toà nhà; tầm mắt "
                 r"mỗi bạn cách chỗ đứng $%s\,\text{m}$ và hai bạn đứng trên cùng một đường thẳng đứng. An nhìn "
                 r"chiếc diều với góc nâng $%s$, Bình nhìn chiếc diều với góc nâng $%s$. Chiếc diều bay cao "
                 r"bao nhiêu mét so với mặt đất (làm tròn đến hàng phần mười)?" % (h, e_s, _goc(al), _goc(be)))
        giai = (r"Gọi $A$, $B$ là mắt của An và Bình, $C$ là chiếc diều thì $AB = %d\,\text{m}$ (hai tầm mắt "
                r"cùng cao $%s\,\text{m}$ so với chỗ đứng). Kẻ $CK$ vuông góc với đường nằm ngang qua $B$.\\ "
                r"$\widehat{CAB} = 90^{\circ} + %s = %s$, $\widehat{CBA} = 90^{\circ} - %s = %s$, nên "
                r"$\widehat{ACB} = %s$.\\ Định lí sin: $BC = \dfrac{AB\cdot\sin\widehat{CAB}}{\sin\widehat{ACB}} "
                r"= \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$.\\ $CK = BC\cdot\sin %s \approx "
                r"%s\,\text{m}$. Độ cao của diều so với mặt đất: $%s + %s \approx %s\,\text{m}$."
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
        debai = (r"Để tránh núi, đường giao thông hiện tại phải đi vòng $A \to B \to C \to D$ với "
                 r"$AB = %d\,\text{km}$, $BC = %d\,\text{km}$, $CD = %d\,\text{km}$, $\widehat{ABC} = %s$, "
                 r"$\widehat{BCD} = %s$ (tứ giác $ABCD$ lồi). Người ta dự định làm đường hầm xuyên núi nối "
                 r"thẳng từ $A$ tới $D$. Đường mới ngắn hơn đường cũ bao nhiêu ki-lô-mét (làm tròn đến hàng "
                 r"phần mười)?" % (AB, BC, CD, _goc(gB), _goc(gC)))
        giai = (r"Tam giác $ABC$: $AC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s \approx %s$, "
                r"$AC \approx %s\,\text{km}$.\\ $\cos\widehat{BCA} = \dfrac{BC^{2} + AC^{2} - AB^{2}}{2\cdot BC"
                r"\cdot AC} \approx %s$ nên $\widehat{BCA} \approx %s^{\circ}$, do đó "
                r"$\widehat{ACD} = %s - \widehat{BCA} \approx %s^{\circ}$.\\ Tam giác $ACD$: $AD^{2} = AC^{2} + "
                r"CD^{2} - 2\cdot AC\cdot CD\cdot\cos\widehat{ACD} \approx %s$, $AD \approx %s\,\text{km}$.\\ "
                r"Đường cũ dài $%d + %d + %d = %d\,\text{km}$, nên đường mới ngắn hơn khoảng "
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
        debai = r"Giá trị của $%s$ bằng" % bt
        giai = (r"Tra bảng giá trị lượng giác của các góc đặc biệt (hoặc dùng máy tính cầm tay):"
                r" $\%s %s = %s$, $\%s %s = %s$." % (h1, _goc(d1), _L(v1), h2, _goc(d2), _L(v2))
                + "\\\\\n" + r"Do đó $%s = %s = %s$." % (bt, thay, dung))
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
        debai = (r"Trong các đẳng thức sau đây, đẳng thức nào \textbf{%s}?"
                 % ("đúng" if hoi_dung else "sai"))
        giai = (r"Tra bảng giá trị lượng giác của các góc đặc biệt (hoặc dùng máy tính cầm tay):"
                + "\\\\\n" + ", ".join(r"$\%s %s = %s$" % (h, _goc(d), _L(that[h])) for h in _HAM4)
                + ".\\\\\n" + r"Vậy đẳng thức %s là %s." % ("đúng" if hoi_dung else "sai", dung))
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
            ly = (r"Vì $%s + %s = 90^{\circ}$ nên hai góc phụ nhau: $\sin %s = \cos %s$, "
                  r"$\cos %s = \sin %s$." % (_goc(a), _goc(b), _goc(b), _goc(a), _goc(b), _goc(a)))
        else:
            doi = mau_nhan.replace(r"\cos BB", r"\left(-\cos AA\right)").replace(r"\sin BB", r"\sin AA")
            ly = (r"Vì $%s + %s = 180^{\circ}$ nên hai góc bù nhau: $\sin %s = \sin %s$, "
                  r"$\cos %s = -\cos %s$." % (_goc(a), _goc(b), _goc(b), _goc(a), _goc(b), _goc(a)))
        so = doi.replace(r"\left(-\cos AA\right)", _ngoac(simplify(-ca)))
        so = so.replace(r"\sin AA", _ngoac(sa)).replace(r"\cos AA", _ngoac(ca))
        doi = doi.replace("AA", _goc(a))
        dung = "$P = %s$" % _tri(P)
        khac = [simplify(g(sa, ca, sb, cb)) for i, (_, g) in enumerate(_TICH) if i != k]
        nhieu = _ba_nhieu(dung, ["$P = %s$" % _tri(x) for x in khac + [-P, Integer(1), Integer(0)]],
                          buoc=lambda t: "$P = %s$" % _tri(P + t))
        debai = r"Tính giá trị biểu thức $P = %s$." % bt
        giai = (ly + "\\\\\n" + r"Do đó $P = %s$." % doi + "\\\\\n" +
                r"Mà $\sin %s = %s$, $\cos %s = %s$ nên $P = %s = %s$."
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
            dk = r"Cho hai góc nhọn $\alpha$ và $\beta$ với $\alpha + \beta = 90^{\circ}$."
            ly = (r"Hai góc $\alpha$ và $\beta$ phụ nhau nên $\sin\beta = \cos\alpha$, "
                  r"$\cos\beta = \sin\alpha$, $\tan\beta = \cot\alpha$.")
        else:
            dk = r"Cho hai góc $\alpha$ và $\beta$ với $\alpha + \beta = 180^{\circ}$."
            ly = (r"Hai góc $\alpha$ và $\beta$ bù nhau nên $\sin\beta = \sin\alpha$, "
                  r"$\cos\beta = -\cos\alpha$.")
        dong = [r"$%s = %s$." % (BT[i][0], BT[i][2])]
        if j is not None:
            dong.append(r"$%s = %s$." % (BT[j][0], BT[j][2]))
        tinh = ("%d\\cdot %s" % (k1, _ngoac(Integer(BT[i][1])))) if k1 != 1 else "%d" % BT[i][1]
        if j is not None:
            tinh += " %s %d\\cdot %s" % ("-" if k2 < 0 else "+", abs(k2), _ngoac(Integer(BT[j][1])))
        debai = dk + r" Tính giá trị của biểu thức $P = %s$." % bt
        giai = (ly + "\\\\\n" + "\\\\\n".join(dong) + "\\\\\n" +
                r"Do đó $P = %s = %s$." % (tinh, dap))
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
            dong.append(r"%s: \textbf{%s}, vì $\%s %s = %s$ còn $%s\%s %s = %s$."
                        % (tex, "đúng" if dung_that else "sai", h1, _goc(d1), _L(v1),
                           "" if dau > 0 else "-", h2, _goc(d2), _L(simplify(dau * v2))))
        random.shuffle(dong)
        debai = (r"Trong các khẳng định sau, khẳng định nào \textbf{%s}?"
                 % ("đúng" if hoi_dung else "sai"))
        giai = (r"Dùng bảng giá trị lượng giác của các góc đặc biệt (hai góc bù nhau có sin bằng "
                r"nhau, côsin đối nhau; hai góc phụ nhau thì sin góc này bằng côsin góc kia):"
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
            debai = (r"Cho góc $\alpha$ với $0^{\circ} < \alpha < 180^{\circ}$, $\alpha \ne 90^{\circ}$. "
                     r"Trong các đẳng thức sau, đẳng thức nào \textbf{%s}?"
                     % ("đúng" if hoi_dung else "sai"))
            ly = (r"Hai góc bù nhau $\alpha$ và $180^{\circ} - \alpha$ có sin bằng nhau; côsin, tang, "
                  r"côtang đối nhau:" + "\\\\\n" +
                  ", ".join("$%s = %s$" % (x, CT[x][0]) for x in trai) + ".")
        else:
            debai = (r"Cho hai góc nhọn $\alpha$ và $\beta$ phụ nhau. Hệ thức nào sau đây là "
                     r"\textbf{%s}?" % ("đúng" if hoi_dung else "sai"))
            ly = (r"Hai góc nhọn phụ nhau thì sin góc này bằng côsin góc kia, tang góc này bằng "
                  r"côtang góc kia:" + "\\\\\n" +
                  ", ".join("$%s = %s$" % (x, CT[x][0]) for x in trai) + ".")
        giai = ly + "\\\\\n" + r"Vậy hệ thức %s là %s." % ("đúng" if hoi_dung else "sai", dung)
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
        debai = (r"Tam giác $ABC$ vuông ở $%s$ có góc $\widehat{%s} = %s$. Khẳng định nào sau đây "
                 r"là \textbf{%s}?" % (X, Y, _goc(g), "đúng" if hoi_dung else "sai"))
        giai = (r"Hai góc nhọn của tam giác vuông phụ nhau nên $\widehat{%s} = 90^{\circ} - %s = %s$."
                % (Z, _goc(g), _goc(z)) + "\\\\\n" +
                r"Tra bảng giá trị lượng giác của các góc đặc biệt: " +
                ", ".join(r"$\%s %s = %s$" % (h, dinh, _L(_gtlg(h, goc)))
                          for dinh, goc in ((Y, g), (Z, z)) for h in ("sin", "cos", "tan")) + ".\\\\\n" +
                r"Vậy khẳng định %s là %s." % ("đúng" if hoi_dung else "sai", dung))
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
        debai = (r"Trên mặt phẳng toạ độ $Oxy$, lấy điểm $M$ thuộc nửa đường tròn đơn vị sao cho "
                 r"$\widehat{xOM} = %s$. Gọi $N$ là điểm đối xứng với $M$ qua trục tung. Giá trị "
                 r"của $\%s\widehat{xON}$ bằng" % (_goc(a), h))
        giai = (r"$N$ đối xứng với $M$ qua trục tung nên $\widehat{xON} = 180^{\circ} - "
                r"\widehat{xOM} = 180^{\circ} - %s = %s$." % (_goc(a), _goc(b)) + "\\\\\n" +
                r"Do đó $\%s\widehat{xON} = \%s %s = %s$." % (h, h, _goc(b), dung))
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
        nhieu = _ba_nhieu(dung, [_L(x) for x in ung], buoc=lambda t: _L(P + Rational(t, 10)))
        debai = (r"Cho góc $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ thoả mãn "
                 r"$%s = %s$. Tính giá trị của $\sin\alpha\cos\alpha$." % (bt, _L(a)))
        giai = (r"Bình phương hai vế: $\left(%s\right)^{2} = %s^{2}$" % (bt, _ngoac_mu(a))
                + "\\\\\n" +
                r"$\Leftrightarrow \sin^{2}\alpha + \cos^{2}\alpha %s 2\sin\alpha\cos\alpha = %s$"
                % ("+" if tong else "-", _L(a ** 2)) + "\\\\\n" +
                r"$\Leftrightarrow %s = %s$ (vì $\sin^{2}\alpha + \cos^{2}\alpha = 1$)" % (bien, _L(a ** 2))
                + "\\\\\n" + r"$\Leftrightarrow \sin\alpha\cos\alpha = %s = %s$." % (ket, dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


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
        debai = (r"Biết $%s$ và $%s$. Xét tính đúng sai của các khẳng định sau:" % (cho, khoang))
        # a) NB - goc phu nhau, goc bu nhau (cua gia tri da cho)
        if cho_sin:
            ly_a = (r"Hai góc phụ nhau: $\cos\left(90^{\circ} - \alpha\right) = \sin\alpha$; hai góc bù nhau: "
                    r"$\sin\left(180^{\circ} - \alpha\right) = \sin\alpha = %s$." % _L(sn))
            dung = [(r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a), (r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(sn), ly_a)]
            sai = [(r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a), (r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(-sn), ly_a),
                   (r"$\sin\left(90^{\circ} - \alpha\right) = %s$" % _L(sn), "Đó là $\\cos\\alpha$. " + ly_a)]
        else:
            ly_a = (r"Hai góc phụ nhau: $\sin\left(90^{\circ} - \alpha\right) = \cos\alpha$; hai góc bù nhau: "
                    r"$\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha = %s$." % _L(-cs))
            dung = [(r"$\sin\left(90^{\circ} - \alpha\right) = %s$" % _L(cs), ly_a), (r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(-cs), ly_a)]
            sai = [(r"$\sin\left(90^{\circ} - \alpha\right) = %s$" % _L(-cs), ly_a), (r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(cs), ly_a),
                   (r"$\cos\left(90^{\circ} - \alpha\right) = %s$" % _L(cs), "Đó là $\\sin\\alpha$. " + ly_a)]
        y1 = _phat_bieu(dung, sai)
        # b) TH - tinh gia tri con lai, xet dau theo khoang
        if cho_sin:
            ly_b = (r"Vì $%s$ nên $\cos\alpha %s 0$. Do đó $\cos\alpha = %s\sqrt{1 - \sin^{2}\alpha} = "
                    r"%s\sqrt{1 - %s} = %s$." % (khoang, "<" if tu else ">", "-" if tu else "",
                                                 "-" if tu else "", _L(sn ** 2), _L(cs)))
            y2 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", cs, ly_b, [(-cs, "Sai dấu"), (dau * (1 - sn), "Quên bình phương"),
                                                                 (dau * cs ** 2, "Quên lấy căn")]),
                         _tf_ct(r"$\cos^{2}\alpha = %s$", cs ** 2, ly_b, [(1 + sn ** 2, "Sai dấu trong $1 - \\sin^{2}\\alpha$"), (sn ** 2, "Nhầm $\\cos^{2}\\alpha = \\sin^{2}\\alpha$")]))
        else:
            ly_b = (r"Vì $%s$ nên $\sin\alpha > 0$. Do đó $\sin\alpha = \sqrt{1 - \cos^{2}\alpha} = "
                    r"\sqrt{1 - %s} = %s$." % (khoang, _L(cs ** 2), _L(sn)))
            y2 = _tf_gop(_tf_ct(r"$\sin\alpha = %s$", sn, ly_b, [(-sn, "$\\sin\\alpha$ luôn dương"), (1 - abs(cs), "Quên bình phương"),
                                                                 (sn ** 2, "Quên lấy căn")]),
                         _tf_ct(r"$\sin^{2}\alpha = %s$", sn ** 2, ly_b, [(1 + cs ** 2, "Sai dấu trong $1 - \\cos^{2}\\alpha$"), (cs ** 2, "Nhầm $\\sin^{2}\\alpha = \\cos^{2}\\alpha$")]))
        # c) VD - tang, cotang tu hai gia tri
        ly_c = ly_b + r" $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$, $\cot\alpha = \dfrac{\cos\alpha}{\sin\alpha} = %s$." % (_L(tn), _L(ct))
        y3 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", tn, ly_c, [(1 / tn, "Đảo tử và mẫu"), (-tn, "Sai dấu"), (sn * cs, "Nhầm $\\tan\\alpha = \\sin\\alpha\\cdot\\cos\\alpha$")]),
                     _tf_ct(r"$\cot\alpha = %s$", ct, ly_c, [(tn, "Nhầm $\\cot\\alpha = \\tan\\alpha$"), (-ct, "Sai dấu")]))
        # d) VDC - goc bu nhau, dung gia tri vua tinh (nhieu bieu thuc)
        ly_d = ly_c + (r" Hai góc bù nhau: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha$, $\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha$, "
                       r"$\tan\left(180^{\circ} - \alpha\right) = -\tan\alpha$, $\cot\left(180^{\circ} - \alpha\right) = -\cot\alpha$.")
        BT = [(r"\tan\left(180^{\circ} - \alpha\right)", -tn, [tn, -ct]),
              (r"\cot\left(180^{\circ} - \alpha\right)", -ct, [ct, -tn]),
              (r"\sin\left(180^{\circ} - \alpha\right) + \cos\left(180^{\circ} - \alpha\right)", sn - cs, [sn + cs, -sn - cs]),
              (r"\sin\left(180^{\circ} - \alpha\right)\cdot\tan\left(180^{\circ} - \alpha\right)", -sn * tn, [sn * tn, -cs * tn]),
              (r"\cos\left(180^{\circ} - \alpha\right) - 2\sin\left(90^{\circ} - \alpha\right)", -3 * cs, [cs, -cs - 2 * sn])]
        dung, sai = [], []
        for bt, P, Ps in random.sample(BT, 3):
            d_, s_ = _tf_ct("$" + bt + " = %s$", simplify(P), ly_d, [(simplify(Q), "Nhầm quan hệ góc bù / góc phụ") for Q in Ps])
            dung += d_
            sai += s_
        y4 = _phat_bieu(dung, sai)
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
        loai = "tù" if tu else "nhọn"
        debai = (r"Cho tam giác $ABC$, biết $\widehat{%s}$ là góc %s. Xét tính đúng sai của các "
                 r"khẳng định sau:" % (X, loai))
        yz = "%s + %s" % tuple(sorted([Y, Z]))
        am, duong = ("<", ">") if tu else (">", "<")
        # a) NB - dau cua gia tri luong giac cua goc X
        ly_a = (r"Vì $\widehat{%s}$ là góc %s nên $\sin %s > 0$, còn $\cos %s$, $\tan %s$, $\cot %s$ %s."
                % (X, loai, X, X, X, X, "âm" if tu else "dương"))
        y1 = _phat_bieu(
            [(r"$\sin %s > 0$" % X, ly_a)] + [(r"$\%s %s %s 0$" % (h, X, am), ly_a) for h in ("cos", "tan", "cot")],
            [(r"$\sin %s < 0$" % X, ly_a)] + [(r"$\%s %s %s 0$" % (h, X, duong), ly_a) for h in ("cos", "tan", "cot")])
        # b) TH - Y + Z = 180 - X (mot buoc: goc bu)
        ly_b = (r"Vì $\widehat{A} + \widehat{B} + \widehat{C} = 180^{\circ}$ nên $%s = 180^{\circ} - %s$; "
                r"hai góc bù nhau có sin bằng nhau, côsin, tang, côtang đối nhau." % (yz, X))
        y2 = _phat_bieu(
            [(r"$\sin\left(%s\right) = \sin %s$" % (yz, X), ly_b), (r"$\cos\left(%s\right) = -\cos %s$" % (yz, X), ly_b),
             (r"$\tan\left(%s\right) = -\tan %s$" % (yz, X), ly_b), (r"$\cot\left(%s\right) = -\cot %s$" % (yz, X), ly_b)],
            [(r"$\sin\left(%s\right) = -\sin %s$" % (yz, X), ly_b), (r"$\cos\left(%s\right) = \cos %s$" % (yz, X), ly_b),
             (r"$\tan\left(%s\right) = \tan %s$" % (yz, X), ly_b), (r"$\sin\left(%s\right) = \cos %s$" % (yz, X), ly_b)])
        # c) VD - voi mot cap khac: (X + Y) va Z
        xy = "%s + %s" % tuple(sorted([X, Y]))
        ly_c = (r"$%s = 180^{\circ} - %s$ nên $\cos\left(%s\right) = -\cos %s$, $\sin\left(%s\right) = \sin %s$." % (xy, Z, xy, Z, xy, Z))
        dung = [(r"$\cos\left(%s\right) + \cos %s = 0$" % (xy, Z), ly_c), (r"$\sin\left(%s\right) - \sin %s = 0$" % (xy, Z), ly_c)]
        sai = [(r"$\sin\left(%s\right) + \sin %s = 0$" % (xy, Z), ly_c + r" Mà $\sin %s > 0$." % Z)]
        if tu:      # khi X tù thì Z nhọn (khác 90 độ) nên các khẳng định dưới đây luôn sai / luôn đúng
            dung.append((r"$\tan\left(%s\right) + \tan %s = 0$" % (xy, Z), ly_c))
            sai += [(r"$\cos\left(%s\right) = \cos %s$" % (xy, Z), ly_c + r" Mà $\widehat{%s}$ nhọn nên $\cos %s \ne 0$." % (Z, Z)),
                    (r"$\cos\left(%s\right) - \cos %s = 0$" % (xy, Z), ly_c + r" Mà $\widehat{%s}$ nhọn nên $\cos %s \ne 0$." % (Z, Z))]
        else:
            sai.append((r"$\sin\left(%s\right) = -\sin %s$" % (xy, Z), ly_c + r" Mà $\sin %s > 0$." % Z))
        y3 = _phat_bieu(dung, sai)
        # d) VDC - ket hop quan he bu va dau
        ly_d = (r"$\cos\left(%s\right) = -\cos %s$, $\sin\left(%s\right) = \sin %s$, $\tan\left(%s\right) = -\tan %s$ nên "
                r"$\cos %s\cdot\cos\left(%s\right) = -\cos^{2} %s < 0$, $\tan %s\cdot\tan\left(%s\right) = -\tan^{2} %s < 0$ "
                r"(vì $\widehat{%s} \ne 90^{\circ}$), $\sin %s\cdot\sin\left(%s\right) = \sin^{2} %s > 0$; "
                r"$\sin\left(%s\right)\cdot\cos\left(%s\right) = -\sin %s\cos %s %s 0$."
                % (yz, X, yz, X, yz, X, X, yz, X, X, yz, X, X, X, yz, X, yz, yz, X, X, duong))
        y4 = _phat_bieu(
            [(r"$\cos %s\cdot\cos\left(%s\right) < 0$" % (X, yz), ly_d), (r"$\tan %s\cdot\tan\left(%s\right) < 0$" % (X, yz), ly_d),
             (r"$\sin %s\cdot\sin\left(%s\right) > 0$" % (X, yz), ly_d),
             (r"$\sin\left(%s\right)\cdot\cos\left(%s\right) %s 0$" % (yz, yz, duong), ly_d)],
            [(r"$\cos %s\cdot\cos\left(%s\right) > 0$" % (X, yz), ly_d), (r"$\tan %s\cdot\tan\left(%s\right) > 0$" % (X, yz), ly_d),
             (r"$\sin %s\cdot\sin\left(%s\right) < 0$" % (X, yz), ly_d),
             (r"$\sin\left(%s\right)\cdot\cos\left(%s\right) %s 0$" % (yz, yz, am), ly_d)])
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
        debai = (r"Trên mặt phẳng toạ độ $Oxy$ lấy điểm $M$ thuộc nửa đường tròn đơn vị sao cho "
                 r"$\widehat{xOM} = %s$ và điểm $A\left(1; 0\right)$. Lấy $N$ đối xứng với $M$ qua "
                 r"trục tung. Xét tính đúng sai của các khẳng định sau:" % _goc(a))
        # a) NB - đối xứng qua trục tung
        ly_a = (r"$N$ đối xứng với $M$ qua trục tung nên $\widehat{xON} = 180^{\circ} - %s = %s$ (hai góc $\widehat{xOM}$, "
                r"$\widehat{xON}$ bù nhau)." % (_goc(a), _goc(b)))
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
        ly_c = (r"$x_N = \cos %s = %s$, $y_N = \sin %s = %s$ (cùng tung độ với $M$, hoành độ đối nhau)."
                % (_goc(b), _L(-c), _goc(b), _L(s)))
        y3 = _phat_bieu(
            [(r"$N\left(%s; %s\right)$" % (_L(-c), _L(s)), ly_c), (r"$x_N = %s$" % _L(-c), ly_c),
             (r"$MN = %s$" % _L(-2 * c), ly_c + r" $MN = x_N - x_M = %s$." % _L(-2 * c))],
            [(r"$N\left(%s; %s\right)$" % (_L(-c), _L(-s)), ly_c), (r"$N\left(%s; %s\right)$" % (_L(c), _L(-s)), ly_c),
             (r"$N\left(%s; %s\right)$" % (_L(s), _L(-c)), ly_c), (r"$x_N = %s$" % _L(c), ly_c),
             (r"$MN = %s$" % _L(-c), ly_c + r" $MN = x_N - x_M = %s$." % _L(-2 * c))])
        # d) VDC - tam giác MAN
        ly_d = (r"$MN$ song song với $Ox$ và $MN = 2x_N = %s$; khoảng cách từ $A$ (và từ $O$) đến $MN$ bằng "
                r"$y_N = %s$. Do đó $S_{\triangle MAN} = S_{\triangle MON} = \dfrac{1}{2}\cdot %s\cdot %s = %s$; "
                r"$AM^{2} = \left(%s - 1\right)^{2} + %s = %s$, $AN^{2} = \left(%s - 1\right)^{2} + %s = %s$."
                % (_L(-2 * c), _L(s), _L(-2 * c), _L(s), _L(S), _L(c), _L(s ** 2), _L(simplify(2 - 2 * c)),
                   _L(-c), _L(s ** 2), _L(simplify(2 + 2 * c))))
        y4 = _tf_gop(_tf_ct(r"$S_{\triangle MAN} = %s$", S, ly_d,
                            [(2 * S, "Quên nhân $\\dfrac{1}{2}$"), (S / 2, "Lấy nhầm $MN = x_N$"), (s / 2, "Lấy nhầm $MN = 1$")],
                            them=[r"$S_{\triangle MAN} = S_{\triangle MON}$"]),
                     _tf_ct(r"$AM = %s$", sqrt(simplify(2 - 2 * c)), ly_d,
                            [(sqrt(simplify(2 + 2 * c)), "Đó là $AN$"), (simplify(1 - c), "Quên tung độ của $M$")]))
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_MAN(a), 0, socot)
    return cauTF


# (lời, kí hiệu, hàm tính, cách thay số)
_TOA_DO_BT = [
    ("tích hoành độ và tung độ", r"x_M\cdot y_M", lambda x, y: x * y,
     lambda x, y: r"%s\cdot %s" % (_ngoac(x), _ngoac(y))),
    ("hiệu giữa bình phương hoành độ và bình phương tung độ", r"x_M^{2} - y_M^{2}",
     lambda x, y: x ** 2 - y ** 2,
     lambda x, y: r"\left(%s\right)^{2} - \left(%s\right)^{2}" % (_L(x), _L(y))),
    ("bình phương tung độ", r"y_M^{2}", lambda x, y: y ** 2,
     lambda x, y: r"\left(%s\right)^{2}" % _L(y)),
    ("bình phương hoành độ", r"x_M^{2}", lambda x, y: x ** 2,
     lambda x, y: r"\left(%s\right)^{2}" % _L(x)),
]


def L10_C3_B5_NB029_SA_B_01(socau, dang=2):
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
        debai = (r"Trên mặt phẳng toạ độ $Oxy$, lấy điểm $M$ thuộc nửa đường tròn đơn vị sao cho "
                 r"$\widehat{xOM} = %s$. %s của điểm $M$ bằng bao nhiêu?"
                 % (_goc(a), chu[0].upper() + chu[1:]))
        giai = (r"Vì $M$ thuộc nửa đường tròn đơn vị và $\widehat{xOM} = %s$ nên "
                r"$x_M = \cos %s = %s$, $y_M = \sin %s = %s$."
                % (_goc(a), _goc(a), _L(x), _goc(a), _L(y))
                + "\\\\\n" + r"Do đó $%s = %s = %s = %s$." % (ki, thay_so(x, y), _L(v), dap))
        ds = _ba_nhieu(dap, [_so_thap_phan_gon(-v) or "0", "1", "0", "0,5"],
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


def L10_C3_B5_TH030_SA_B_01(socau, dang=2):
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
        debai = (r"Trên mặt phẳng toạ độ $Oxy$ lấy điểm $M$ thuộc nửa đường tròn đơn vị sao cho "
                 r"$\cos\widehat{xOM} = %s$ và điểm $A\left(1; 0\right)$. Diện tích của tam giác $AOM$ "
                 r"bằng bao nhiêu?" % _L(cs))
        giai = (r"Vì $M$ thuộc nửa đường tròn đơn vị nên $y_M \ge 0$, tức $\sin\widehat{xOM} \ge 0$."
                + "\\\\\n" +
                r"$\sin^{2}\widehat{xOM} = 1 - \cos^{2}\widehat{xOM} = 1 - %s = %s$ nên "
                r"$\sin\widehat{xOM} = %s$." % (_L(cs ** 2), _L(sn ** 2), _L(sn)) + "\\\\\n" +
                r"Chiều cao hạ từ $M$ xuống $OA$ là $h = y_M = \sin\widehat{xOM} = %s$, còn $OA = 1$."
                % _L(sn) + "\\\\\n" +
                r"Vậy $S_{\triangle AOM} = \dfrac{1}{2}\cdot OA\cdot h = \dfrac{1}{2}\cdot 1\cdot %s = %s$."
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
    de = (r"Cho góc $\alpha$ thoả mãn $%s\alpha = %s$. Giá trị của biểu thức "
          r"$P = \dfrac{%s}{%s}$ bằng" % (ham, _L(t), tu, mau))
    if cho_tan:
        giai = (r"Vì $\tan\alpha = %s$ nên $\cos\alpha \ne 0$. Chia cả tử và mẫu của $P$ cho "
                r"$\cos\alpha$, dùng $\dfrac{\sin\alpha}{\cos\alpha} = \tan\alpha$:" "\\\\\n"
                r"$P = \dfrac{%s}{%s} = \dfrac{%s}{%s} = %s$."
                % (_L(t), _bt_mot_bien(a, r"\tan\alpha", b), _bt_mot_bien(c, r"\tan\alpha", d),
                   _L(a * t + b), _L(c * t + d), _L(P)))
    else:
        giai = (r"Vì $\cot\alpha = %s$ nên $\sin\alpha \ne 0$. Chia cả tử và mẫu của $P$ cho "
                r"$\sin\alpha$, dùng $\dfrac{\cos\alpha}{\sin\alpha} = \cot\alpha$:" "\\\\\n"
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


def L10_C3_B5_TH030_MC_E_01(socau, dang=1):
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


def L10_C3_B5_TH030_MC_E_02(socau, dang=1):
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


def L10_C3_B5_TH030_SA_C_01(socau, dang=2):
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
        de = de[:-len("bằng")].rstrip() + r". Tính giá trị của $P$."
        dap = _so_thap_phan_gon(P)
        cau += MC_SA_answer_const(de, dap, [_so_thap_phan_gon(P + k) or str(k) for k in (1, -1, 2)],
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_MC_F_01(socau, dang=1):
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
        de = (r"Cho góc $\alpha$ thoả mãn $\tan\alpha %s \cot\alpha = %d$. Giá trị của biểu thức "
              r"$A = \tan^{2}\alpha + \cot^{2}\alpha$ bằng" % (dau, m))
        giai = (r"Ta có $\tan\alpha\cdot\cot\alpha = 1$. Bình phương hai vế của giả thiết:" "\\\\\n"
                r"$\left(\tan\alpha %s \cot\alpha\right)^{2} = \tan^{2}\alpha + \cot^{2}\alpha %s "
                r"2\tan\alpha\cot\alpha = A %s 2 = %d$." "\\\\\n"
                r"Vậy $A = %d$." % (dau, dau, dau, m * m, k))
        nh = _ba_nhieu(str(k), [str(m * m + (2 if cong else -2)), str(m * m), str(m * m + (-1 if cong else 1))],
                       buoc=lambda t: str(k + 3 * t))
        cau += MC_SA_answer_const(de, str(k), nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_MC_F_02(socau, dang=1):
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
        de = (r"Cho góc $\alpha$ thoả mãn $\tan^{2}\alpha + \cot^{2}\alpha = %d$. Giá trị của "
              r"$\left(\tan\alpha %s \cot\alpha\right)^{2}$ bằng" % (k, dau))
        giai = (r"Vì $\tan\alpha\cdot\cot\alpha = 1$ nên" "\\\\\n"
                r"$\left(\tan\alpha %s \cot\alpha\right)^{2} = \tan^{2}\alpha + \cot^{2}\alpha %s 2 = %d %s 2 = %d$."
                % (dau, dau, k, dau, kq))
        nh = _ba_nhieu(str(kq), [str(k - 2 if cong else k + 2), str(k), str(k + (1 if cong else -1))],
                       buoc=lambda t: str(kq + 3 * t))
        cau += MC_SA_answer_const(de, str(kq), nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_SA_D_01(socau, dang=2):
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
        de = (r"Cho góc $\alpha$ thoả mãn $\tan\alpha %s \cot\alpha = %d$. Tính giá trị của biểu thức "
              r"$A = \tan^{2}\alpha + \cot^{2}\alpha$." % (dau, m))
        giai = (r"Vì $\tan\alpha\cdot\cot\alpha = 1$ nên "
                r"$\left(\tan\alpha %s \cot\alpha\right)^{2} = A %s 2$, tức là $%d = A %s 2$. Vậy $A = %d$."
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
    de = r"Cho góc $\alpha$ thoả mãn $%s\alpha = %s$. Giá trị của biểu thức $P = %s$ bằng" % (ham, _L(g), bt)
    if cho_cos:
        b1 = (r"$\cos^{2}\alpha = %s$ nên $\sin^{2}\alpha = 1 - \cos^{2}\alpha = %s$ "
              r"(không cần biết dấu của $\sin\alpha$)." % (_L(c2), _L(s2)))
    else:
        b1 = (r"$\sin^{2}\alpha = %s$ nên $\cos^{2}\alpha = 1 - \sin^{2}\alpha = %s$ "
              r"(không cần biết dấu của $\cos\alpha$)." % (_L(s2), _L(c2)))
    giai = (r"Dùng $\sin^{2}\alpha + \cos^{2}\alpha = 1$: " + b1 + "\\\\\n" +
            r"$P = %s\cdot %s %s %s\cdot %s = %s$." % (a, _L(s2), "+" if b > 0 else "-", abs(b), _L(c2), _L(P)))
    return de, giai


def L10_C3_B5_TH030_MC_G_01(socau, dang=1):
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


def L10_C3_B5_TH030_SA_E_01(socau, dang=2):
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
        de = de[:-len("bằng")].rstrip() + r". Tính giá trị của $P$."
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


def L10_C3_B5_TH031_MC_J_01(socau, dang=1):
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
        de = r"Giá trị của biểu thức $P = %s$ (các góc tăng đều $%d^{\circ}$) bằng" % (bt, d)
        giai = (r"Ghép các thừa số thành từng cặp hai góc phụ nhau: "
                r"$\tan x^{\circ}\cdot\tan\left(90 - x\right)^{\circ} = \tan x^{\circ}\cdot\cot x^{\circ} = 1$, "
                r"còn lại thừa số giữa $\tan 45^{\circ} = 1$." "\\\\\n"
                r"Do đó $\tan %d^{\circ}\cdots\tan %d^{\circ} = 1$ và $P = %d\cdot 1 %s = %d$."
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


def L10_C3_B5_TH031_MC_J_02(socau, dang=1):
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
        de = r"Giá trị của biểu thức $S = %s$ (các góc tăng đều $%d^{\circ}$) bằng" % (bt, d)
        le = [x for x in goc if 180 - x not in goc or x == 90]
        if le:
            con = (r"chỉ còn lại " + ", ".join(r"$\cos %d^{\circ} = %d$" % (x, round(math.cos(math.radians(x))))
                                             for x in le) + ".")
        else:
            con = r"mọi số hạng đều ghép được thành cặp."
        giai = (r"Hai góc bù nhau có côsin đối nhau: $\cos x + \cos\left(180^{\circ} - x\right) = 0$. "
                r"Ghép các số hạng thành từng cặp hai góc bù nhau, mỗi cặp có tổng bằng $0$; " + con
                + "\\\\\n" + r"Vậy $S = %s$." % _L(S))
        nh = _ba_nhieu(_L(S), ["0", "1", "-1", "2", "-2"], buoc=lambda t: str(t + 2))
        cau += MC_SA_answer_const(de, _L(S), nh, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_G_01(socau, dang=2):
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
            v = ("cos",) + _bo_tong_cos() + (random.choice([2, 3, 4, 5]), random.choice([1, 2, 3, 5]))
        if v not in gt:
            gt.append(v)
    for v in gt:
        if v[0] == "tan":
            _, a, d, k, c = v
            kq = k + c
            de = (r"Tính giá trị của biểu thức $P = %d\tan %d^{\circ}\cdot\tan %d^{\circ}\cdots\tan %d^{\circ} %s$ "
                  r"(các góc tăng đều $%d^{\circ}$)."
                  % (k, a, a + d, 90 - a, ("+ %d" % c) if c > 0 else ("- %d" % -c), d))
            giai = (r"Ghép từng cặp hai góc phụ nhau: $\tan x^{\circ}\cdot\tan\left(90 - x\right)^{\circ} = 1$, "
                    r"thừa số giữa là $\tan 45^{\circ} = 1$, nên tích bằng $1$. Vậy $P = %d + %d = %d$."
                    % (k, c, kq) if c > 0 else
                    r"Ghép từng cặp hai góc phụ nhau: $\tan x^{\circ}\cdot\tan\left(90 - x\right)^{\circ} = 1$, "
                    r"thừa số giữa là $\tan 45^{\circ} = 1$, nên tích bằng $1$. Vậy $P = %d - %d = %d$."
                    % (k, -c, kq))
        else:
            _, bat_dau, ket_thuc, d, k, c = v
            S, goc = _gia_tri_tong_cos(bat_dau, ket_thuc, d)
            kq = k * S + c
            de = (r"Tính giá trị của biểu thức $P = %d\left(\cos %d^{\circ} + \cos %d^{\circ} + \cdots + "
                  r"\cos %d^{\circ}\right) + %d$ (các góc tăng đều $%d^{\circ}$)."
                  % (k, goc[0], goc[1], goc[-1], c, d))
            giai = (r"Ghép từng cặp hai góc bù nhau: $\cos x + \cos\left(180^{\circ} - x\right) = 0$; tổng trong "
                    r"ngoặc chỉ còn các số hạng không có cặp, bằng $%s$. Vậy $P = %d\cdot\left(%s\right) + %d = %s$."
                    % (_L(S), k, _L(S), c, _L(kq)))
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
        de = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$ và đường trung tuyến $%s%s = %s$ ($%s$ là "
              r"trung điểm của $%s$). Độ dài cạnh $%s$ bằng"
              % (ke1, b, ke2, c, dinh, M, _L(sqrt(m2)), M, doi, doi))
        giai = (r"Theo công thức đường trung tuyến: $%s%s^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}$." "\\\\\n"
                r"Suy ra $%s^{2} = 2\left(%s^{2} + %s^{2}\right) - 4\cdot %s%s^{2} = 2\left(%d + %d\right) - 4\cdot %s = %d$, "
                r"nên $%s = %d$."
                % (dinh, M, ke1, ke2, doi, doi, ke1, ke2, dinh, M, b * b, c * c, _L(m2), a * a, doi, a))
        dap = str(a)
        sai = [_can_gon(2 * b * b + 2 * c * c - m2), _can_gon(abs(b * b + c * c - 2 * m2)),
               _can_gon(Rational(2 * b * b + 2 * c * c, 1) - 2 * m2), str(a + 1)]
        nh = _ba_nhieu(dap, [s for s in sai if s != dap], buoc=lambda t: str(a + t + 1))
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH032_SA_D_01(socau, dang=2):
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
        de = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$ và đường trung tuyến $%sM = %s$ ($M$ là trung "
              r"điểm của $%s$). Tính độ dài cạnh $%s$."
              % (ke1, b, ke2, c, dinh, _L(sqrt(m2)), doi, doi))
        giai = (r"Từ $%sM^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}$ suy ra "
                r"$%s^{2} = 2\left(%d + %d\right) - 4\cdot %s = %d$, nên $%s = %d$."
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
        loai = "nhọn" if nhon else "tù"
        de = (r"Cho tam giác $ABC$ có góc $A$ %s, $BC = %s$ và bán kính đường tròn ngoại tiếp $R = %d$. "
              r"Số đo góc $A$ bằng" % (loai, _L(a), R))
        giai = (r"Theo định lí sin: $\dfrac{BC}{\sin A} = 2R \Rightarrow \sin A = \dfrac{BC}{2R} = "
                r"\dfrac{%s}{%d} = %s$." "\\\\\n"
                r"Có hai góc có sin bằng $%s$ là $%d^{\circ}$ và $%d^{\circ}$; vì góc $A$ %s nên "
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
        loai = "nhọn" if nhon else "tù"
        vp = "b" if ve_phai == "" else ve_phai + "\\, b" if not ve_phai[0].isdigit() else ve_phai + "b"
        vp = ("b" if ve_phai == "" else (ve_phai.replace(r"\sqrt", "b\\sqrt", 1) if ve_phai.startswith(r"\sqrt")
                                         else ve_phai[0] + "b" + ve_phai[1:]))
        de = (r"Cho tam giác $ABC$ có góc $A$ %s và thoả mãn $%da\sin B = %s$ (với $a = BC$, $b = CA$). "
              r"Số đo góc $A$ bằng" % (loai, k, vp))
        giai = (r"Theo định lí sin: $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} \Rightarrow a\sin B = b\sin A$." "\\\\\n"
                r"Thay vào giả thiết: $%db\sin A = %s \Rightarrow \sin A = %s$." "\\\\\n"
                r"Vì góc $A$ %s nên $\widehat{A} = %d^{\circ}$."
                % (k, vp, _L(sA), loai, A))
        dap = r"%d^{\circ}" % A
        khac = [g for p in _GOC_TU_SIN.values() for g in p if g != A]
        nh = _ba_nhieu(dap, [r"%d^{\circ}" % (180 - A)] + [r"%d^{\circ}" % g for g in random.sample(khac, 4)])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_SA_C_01(socau, dang=2):
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
        loai = "nhọn" if nhon else "tù"
        de = (r"Cho tam giác $ABC$ có góc $A$ %s, $BC = %s$ và bán kính đường tròn ngoại tiếp $R = %d$. "
              r"Tính số đo góc $A$ (đơn vị: độ)." % (loai, _L(a), R))
        giai = (r"$\sin A = \dfrac{BC}{2R} = \dfrac{%s}{%d} = %s$; góc $A$ %s nên $\widehat{A} = %d^{\circ}$."
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
    return (r"Đặt $BC = x\ \left(x > 0\right)$. Theo định lí côsin: $AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos B$" "\\\\\n"
            r"$\Leftrightarrow %d = %d + x^{2} - 2\cdot %d\cdot x\cdot\left(%s\right) \Leftrightarrow x^{2} %s %dx %s %d = 0$." "\\\\\n"
            r"Phương trình có hai nghiệm $x = %d$ và $x = %d$; vì $x > 0$ nên $BC = %d$."
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
        de = r"Cho tam giác $ABC$ có $AB = %d$, $AC = %d$ và $\widehat{B} = %d^{\circ}$. Độ dài cạnh $BC$ bằng" % (c, b, B)
        dap = str(x)
        hs = -c if B == 60 else c
        sai = [str(abs(-hs - x)), _can_gon(b * b + c * c), _can_gon(abs(b * b - c * c)), str(x + 1)]
        nh = _ba_nhieu(dap, sai, buoc=lambda t: str(x + t + 1))
        cau += MC_SA_answer_const(de, dap, nh, _giai_cos_bac_hai(B, c, x, b), 0, 0, dang)
    return cau


def L10_C3_B6_TH035_SA_D_01(socau, dang=2):
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
        de = r"Cho tam giác $ABC$ có $AB = %d$, $AC = %d$ và $\widehat{B} = %d^{\circ}$. Tính độ dài cạnh $BC$." % (c, b, B)
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
        cau += MC_SA_answer_const(de + " Chu vi của tam giác $ABC$ bằng", dap, nh, giai, 0, 0, dang)
    return cau


def _de_ti_le_sin(kieu, he, ti, k, canh):
    ten = ["BC", "CA", "AB"]
    a_, b_, c_ = ti
    canh_that = [k * a_, k * b_, k * c_]
    if kieu == "tich":
        p, q, r = he
        gia = r"$%d\sin A = %d\sin B = %d\sin C$" % (p, q, r)
        b1 = (r"Từ giả thiết, $\sin A : \sin B : \sin C = \dfrac{1}{%d} : \dfrac{1}{%d} : \dfrac{1}{%d} = %d : %d : %d$."
              % (p, q, r, a_, b_, c_))
    else:
        gia = r"$\dfrac{%d}{\sin A} = \dfrac{%d}{\sin B} = \dfrac{%d}{\sin C}$" % he
        b1 = r"Từ giả thiết, $\sin A : \sin B : \sin C = %d : %d : %d$." % (a_, b_, c_)
    de = r"Cho tam giác $ABC$ thoả mãn %s và $%s = %d$." % (gia, ten[canh], canh_that[canh])
    chu_vi = sum(canh_that)
    giai = (b1 + "\\\\\n" +
            r"Theo định lí sin, $a : b : c = \sin A : \sin B : \sin C = %d : %d : %d$ (với $a = BC$, $b = CA$, $c = AB$)." % ti
            + "\\\\\n" +
            r"Vì $%s = %d$ nên mỗi phần bằng $%d$: $BC = %d$, $CA = %d$, $AB = %d$. Chu vi bằng $%d$."
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
        de = (r"Cho tam giác $ABC$ có $\widehat{A} = %d^{\circ}$, $\widehat{B} = %d^{\circ}$. Gọi $h_a$, $h_b$ lần lượt là "
              r"độ dài đường cao kẻ từ $A$, $B$. Tỉ số $\dfrac{h_a}{h_b}$ bằng" % (A, B))
        giai = (r"Ta có $S = \dfrac{1}{2}a h_a = \dfrac{1}{2}b h_b \Rightarrow \dfrac{h_a}{h_b} = \dfrac{b}{a}$." "\\\\\n"
                r"Theo định lí sin, $\dfrac{b}{a} = \dfrac{\sin B}{\sin A} = \dfrac{\sin %d^{\circ}}{\sin %d^{\circ}} = "
                r"\dfrac{%s}{%s} = %s$." % (B, A, _L(SIN[B]), _L(SIN[A]), _L(kq)))
        dap = _L(kq)
        nh = _ba_nhieu(dap, [_L(simplify(1 / kq)), _L(SIN[B]), _L(SIN[A]), _L(simplify(2 * kq))])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_SA_D_01(socau, dang=2):
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
        cau += MC_SA_answer_const(de + " Tính chu vi của tam giác $ABC$.", str(chu_vi),
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
        cau += MC_SA_answer_const(de + r" Độ dài đường chéo $%s$ bằng" % hoi, dap, nh, giai, 0, 0, dang)
    return cau


def _de_hbh(A, m, n, cs, hoi, X2):
    de = r"Cho hình bình hành $ABCD$ có $AB = %d$, $AD = %d$ và $\widehat{BAD} = %d^{\circ}$." % (m, n, A)
    if hoi == "BD":
        giai = (r"Trong tam giác $ABD$: $BD^{2} = AB^{2} + AD^{2} - 2\cdot AB\cdot AD\cdot\cos %d^{\circ} = "
                r"%d + %d - 2\cdot %d\cdot %d\cdot\left(%s\right) = %s$." % (A, m * m, n * n, m, n, _L(cs), _L(X2)))
    else:
        giai = (r"Vì $ABCD$ là hình bình hành nên $BC = AD = %d$ và $\widehat{ABC} = 180^{\circ} - %d^{\circ} = %d^{\circ}$." "\\\\\n"
                r"Trong tam giác $ABC$: $AC^{2} = AB^{2} + BC^{2} - 2\cdot AB\cdot BC\cdot\cos %d^{\circ} = "
                r"%d + %d - 2\cdot %d\cdot %d\cdot\left(%s\right) = %s$."
                % (n, A, 180 - A, 180 - A, m * m, n * n, m, n, _L(-cs), _L(X2)))
    giai += r" Vậy $%s = %s$." % (hoi, _L(sqrt(X2)))
    return de, giai


def L10_C3_B6_TH032_MC_I_02(socau, dang=1):
    r"""Định lí côsin trong hình bình hành, cách hỏi khác: biết một cạnh và hai đường chéo, tính
    cạnh kề. Dùng công thức trung tuyến trong tam giác $ABD$ (tâm $O$ là trung điểm $BD$):
    $AB^{2} + AD^{2} = \dfrac{AC^{2} + BD^{2}}{2}$.

    CLAUDE THEM 01/10/2026 - theo phan III tai lieu C3-B2 ("mot canh 4, hai duong cheo 6 va 8").
    Co Lan duyet lai.
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
        de = (r"Cho hình bình hành $ABCD$ có $AB = %d$ và hai đường chéo $AC = %d$, $BD = %d$. Độ dài cạnh $AD$ bằng"
              % (m, p, q))
        giai = (r"Gọi $O$ là giao điểm hai đường chéo thì $O$ là trung điểm của $BD$, $AO = \dfrac{AC}{2} = %s$." "\\\\\n"
                r"Trong tam giác $ABD$, $AO$ là trung tuyến: $AO^{2} = \dfrac{AB^{2} + AD^{2}}{2} - \dfrac{BD^{2}}{4}$" "\\\\\n"
                r"$\Rightarrow AD^{2} = 2AO^{2} + \dfrac{BD^{2}}{2} - AB^{2} = 2\cdot %s + %s - %d = %s$, nên $AD = %s$."
                % (_L(Rational(p, 2)), _L(Rational(p * p, 4)), _L(Rational(q * q, 2)), m * m, _L(n2), _L(sqrt(n2))))
        dap = _L(sqrt(n2))
        nh = _ba_nhieu(dap, [_L(sqrt(p * p + q * q - m * m)), _L(sqrt(abs(Rational(p * p + q * q, 4) - m * m))),
                             _L(n2), str(abs(q - m))])
        cau += MC_SA_answer_const(de, dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH032_SA_F_01(socau, dang=2):
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
        cau += MC_SA_answer_const(de + r" Tính độ dài đường chéo $%s$." % hoi, str(x),
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
        de = r"Cho hình thoi $ABCD$ có cạnh bằng $%d$ và $\widehat{BAD} = %d^{\circ}$." % (m, A)
    else:
        de = r"Cho hình bình hành $ABCD$ có $AB = %d$, $AD = %d$ và $\widehat{BAD} = %d^{\circ}$." % (m, n, A)
    giai = (r"Đường chéo $BD$ chia hình thành hai tam giác bằng nhau $ABD$ và $CDB$, nên" "\\\\\n"
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
        cau += MC_SA_answer_const(de + r" Diện tích hình $ABCD$ bằng", dap, nh, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_E_01(socau, dang=2):
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
        cau += MC_SA_answer_const(de + r" Tính diện tích hình $ABCD$.", dap,
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
    return (r"Từ hai vị trí $A$ và $B$ của một toà nhà, người ta quan sát đỉnh $C$ của một ngọn núi. Biết $A$ là "
            r"chân toà nhà trên mặt đất, $B$ là nóc toà nhà, $AB$ vuông góc với mặt đất và $AB = %d\,\text{m}$; "
            r"phương nhìn $AC$ tạo với phương nằm ngang góc $%s$, phương nhìn $BC$ tạo với phương nằm ngang góc "
            r"$%s$ (hình vẽ). Gọi $H$ là hình chiếu của $C$ trên mặt đất." % (h, _goc(al), _goc(be)))


def _giai_goc_nui(h, al, be, AC):
    return (r"Trong tam giác $ABC$: $\widehat{BAC} = 90^{\circ} - %s = %s$ (góc giữa $AB$ thẳng đứng và $AC$); "
            r"$\widehat{ABC} = 90^{\circ} + %s = %s$; do đó $\widehat{ACB} = 180^{\circ} - %s - %s = %s$." "\\\\\n"
            r"Theo định lí sin: $\dfrac{AC}{\sin\widehat{ABC}} = \dfrac{AB}{\sin\widehat{ACB}} \Rightarrow "
            r"AC = \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$."
            % (_goc(al), _goc(90 - al), _goc(be), _goc(90 + be), _goc(90 - al), _goc(90 + be), _goc(al - be),
               h, _goc(90 + be), _goc(al - be), _x1(AC, 1)))


def _giai_cao_nui(al, CH, AC):
    return (r"Tam giác $ACH$ vuông tại $H$, $\widehat{CAH} = %s$ nên $CH = AC\cdot\sin %s \approx %s\,\text{(m)}$."
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
        de = _de_nui_toa_nha(h, al, be) + r" Khoảng cách $AC$ (làm tròn đến hàng đơn vị) là"
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
        de = _de_nui_toa_nha(h, al, be) + r" Chiều cao $CH$ của ngọn núi (làm tròn đến hàng đơn vị) là"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh],
                                  _giai_goc_nui(h, al, be, AC) + "\\\\\n" + _giai_cao_nui(al, CH, AC),
                                  _hinh_nui_toa_nha(h, al, be, CH), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_P_01(socau, dang=2):
    r"""Trả lời ngắn - ngọn núi quan sát từ chân và nóc toà nhà (mức VD): tính $AC$ (m, hàng đơn vị).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        dap = _so(AC)
        de = _de_nui_toa_nha(h, al, be) + r" Tính khoảng cách $AC$ (đơn vị mét, làm tròn đến hàng đơn vị)."
        cau += MC_SA_answer_const(de, dap, [str(int(dap) + k) for k in (1, -1, 2)], _giai_goc_nui(h, al, be, AC),
                                  _hinh_nui_toa_nha(h, al, be, CH), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_Q_01(socau, dang=2):
    r"""Trả lời ngắn - ngọn núi quan sát từ chân và nóc toà nhà (mức VDC): chiều cao ngọn núi.

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        h, al, be, AC, CH = _bo_nui_toa_nha()
        dap = _so(CH)
        de = _de_nui_toa_nha(h, al, be) + r" Tính chiều cao $CH$ của ngọn núi (đơn vị mét, làm tròn đến hàng đơn vị)."
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
        ds = [(r"Tính số đo các góc của tam giác $ABC$ và khoảng cách $AC$ (làm tròn đến hàng phần mười, đơn vị mét).",
               r"AC \approx %s\,\text{m}" % _x1(AC, 1), _giai_goc_nui(h, al, be, AC)),
              (r"Tính chiều cao $CH$ của ngọn núi so với mặt đất (làm tròn đến hàng phần mười, đơn vị mét).",
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
    return (r"Khi khai quật một ngôi mộ cổ, các nhà khảo cổ tìm được một chiếc đĩa cổ hình tròn bị vỡ. Để khôi "
            r"phục hình dạng chiếc đĩa, họ lấy ba điểm $A$, $B$, $C$ trên mép đĩa và đo được "
            r"$BC = %s\,\text{cm}$, $CA = %s\,\text{cm}$, $AB = %s\,\text{cm}$ (hình vẽ)."
            % (_x1(a, 1), _x1(b, 1), _x1(c, 1)))


def _hinh_duong_tron_ba_diem(goc, nhan, ho=False):
    """Ba điểm trên đường tròn ở các góc (độ, theo tâm) cho trước; ho=True tô màu hồ nước."""
    pts = [(1.5 * math.cos(math.radians(g)), 1.5 * math.sin(math.radians(g))) for g in goc]
    hinh = ("\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
            + ("\\fill[blue!12] (0,0) circle (1.5);\n\\draw (0,0) circle (1.5);\n" if ho else
               "\\draw[dashed] (0,0) circle (1.5);\n\\draw[thick] (1.5,0) arc (0:250:1.5);\n"))
    hinh += "\\draw[thick] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f)%s;\n" % (
        pts[1] + pts[0] + pts[2] + ("" if ho else " -- cycle",))
    for (x, y), t in zip(pts, nhan):
        hinh += "\\fill (%.3f,%.3f) circle (0.04) node[%s] {$%s$};\n" % (
            x, y, "above" if y > 0.3 else ("below" if y < -0.3 else ("right" if x > 0 else "left")), t)
    return hinh + "\\end{tikzpicture}"


def _giai_dia_co(a, b, c, p, S, R):
    return (r"Bán kính đĩa bằng bán kính $R$ của đường tròn ngoại tiếp tam giác $ABC$." "\\\\\n"
            r"Nửa chu vi $p = \dfrac{%s + %s + %s}{2} = %s$; theo công thức Heron "
            r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} \approx %s\,\left(\text{cm}^{2}\right)$." "\\\\\n"
            r"Từ $S = \dfrac{abc}{4R}$ suy ra $R = \dfrac{abc}{4S} \approx \dfrac{%s\cdot %s\cdot %s}{4\cdot %s} \approx %s\,\text{(cm)}$."
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
    return (r"Để đo đường kính một hồ nước hình tròn, người ta lấy ba điểm $A$, $B$, $C$ trên bờ hồ và đo được "
            r"$AB = %d\,\text{m}$, $AC = %d\,\text{m}$, $\widehat{BAC} = %s$ (hình vẽ)." % (AB, AC, _goc(A)))


def _giai_ho_bc(A, AB, AC, BC):
    return (r"Theo định lí côsin: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos %s = %d + %d - 2\cdot %d\cdot %d\cdot\cos %s$, "
            r"nên $BC \approx %s\,\text{(m)}$." % (_goc(A), AB * AB, AC * AC, AB, AC, _goc(A), _x1(BC, 2)))


def _giai_ho_d(A, BC, d):
    return (r"Hồ là đường tròn ngoại tiếp tam giác $ABC$. Theo định lí sin: $\dfrac{BC}{\sin A} = 2R = d$, nên đường "
            r"kính $d = \dfrac{BC}{\sin %s} \approx %s\,\text{(m)}$." % (_goc(A), _x1(d, 1)))


def _goc_ve_ho(A):
    # đặt A ở trên, B, C phía dưới: cung BC (không chứa A) chắn góc 360 - 2A ở tâm
    g = 360 - 2 * A
    return [90, 270 - g / 2, 270 + g / 2]


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
        de = (_de_dia_co(a, b, c) + r" Số đo góc lớn nhất của tam giác $ABC$ (làm tròn đến hàng đơn vị của độ) là")
        giai = (r"Góc lớn nhất là góc đối diện cạnh lớn nhất $%s$, tức là góc $%s$. Theo hệ quả định lí côsin "
                r"$\cos %s \approx %s$, nên $\widehat{%s} \approx %s$."
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
        de = _de_ho_tron(A, AB, AC) + r" Khoảng cách $BC$ (làm tròn đến hàng phần mười) là"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_ho_bc(A, AB, AC, BC),
                                  _hinh_duong_tron_ba_diem(_goc_ve_ho(A), "ABC", ho=True), 0, dang)
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
        de = _de_dia_co(a, b, c) + r" Bán kính của chiếc đĩa (làm tròn đến hàng phần mười) là"
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
        de = _de_ho_tron(A, AB, AC) + r" Đường kính của hồ nước (làm tròn đến hàng đơn vị) là"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh],
                                  _giai_ho_bc(A, AB, AC, BC) + "\\\\\n" + _giai_ho_d(A, BC, d),
                                  _hinh_duong_tron_ba_diem(_goc_ve_ho(A), "ABC", ho=True), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_R_01(socau, dang=2):
    r"""Trả lời ngắn - đường tròn qua ba điểm (mức VD): đĩa cổ - góc lớn nhất (độ), hoặc hồ nước - $BC$ (m).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.5:
            a, b, c, p, S, R, dinh, g = _bo_dia_co()
            doi = {"A": "BC", "B": "CA", "C": "AB"}[dinh]
            dap = str(_lt(g))
            de = _de_dia_co(a, b, c) + r" Tính số đo góc lớn nhất của tam giác $ABC$ (đơn vị độ, làm tròn đến hàng đơn vị)."
            giai = (r"Góc lớn nhất đối diện cạnh lớn nhất $%s$: theo hệ quả định lí côsin $\cos %s \approx %s$, "
                    r"nên $\widehat{%s} \approx %s^{\circ}$." % (doi, dinh, _xx(math.cos(math.radians(g)), 4), dinh, dap))
            hinh = _hinh_duong_tron_ba_diem([100, 220, 330], "ABC")
        else:
            A, AB, AC, BC, d = _bo_ho_tron()
            dap = _so(BC, 1)
            de = _de_ho_tron(A, AB, AC) + r" Tính khoảng cách $BC$ (đơn vị mét, làm tròn đến hàng phần mười)."
            giai = _giai_ho_bc(A, AB, AC, BC)
            hinh = _hinh_duong_tron_ba_diem(_goc_ve_ho(A), "ABC", ho=True)
        cau += MC_SA_answer_const(de, dap, [dap + "1", "1" + dap, "2" + dap], giai, hinh, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_S_01(socau, dang=2):
    r"""Trả lời ngắn - đường tròn qua ba điểm (mức VDC): bán kính đĩa cổ (cm) hoặc đường kính hồ (m).

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.5:
            a, b, c, p, S, R, dinh, g = _bo_dia_co()
            dap = _so(R, 1)
            de = _de_dia_co(a, b, c) + r" Tính bán kính của chiếc đĩa (đơn vị xăng-ti-mét, làm tròn đến hàng phần mười)."
            giai, hinh = _giai_dia_co(a, b, c, p, S, R), _hinh_duong_tron_ba_diem([100, 220, 330], "ABC")
        else:
            A, AB, AC, BC, d = _bo_ho_tron()
            dap = _so(d)
            de = _de_ho_tron(A, AB, AC) + r" Tính đường kính của hồ nước (đơn vị mét, làm tròn đến hàng đơn vị)."
            giai = _giai_ho_bc(A, AB, AC, BC) + "\\\\\n" + _giai_ho_d(A, BC, d)
            hinh = _hinh_duong_tron_ba_diem(_goc_ve_ho(A), "ABC", ho=True)
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
        ds = [(r"Tính số đo góc lớn nhất của tam giác $ABC$ (làm tròn đến hàng đơn vị của độ).",
               r"\widehat{%s} \approx %d^{\circ}" % (dinh, _lt(g)),
               r"Góc lớn nhất đối diện cạnh lớn nhất $%s$: $\cos %s \approx %s$ (hệ quả định lí côsin), nên "
               r"$\widehat{%s} \approx %d^{\circ}$." % (doi, dinh, _xx(math.cos(math.radians(g)), 4), dinh, _lt(g))),
              (r"Tính bán kính của chiếc đĩa (làm tròn đến hàng phần mười, đơn vị xăng-ti-mét).",
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
        ds = [(r"Tính khoảng cách $BC$ (làm tròn đến hàng phần mười, đơn vị mét).",
               r"BC \approx %s\,\text{m}" % _x1(BC, 1), _giai_ho_bc(A, AB, AC, BC)),
              (r"Tính đường kính của hồ nước (làm tròn đến hàng đơn vị, đơn vị mét).",
               r"d \approx %d\,\text{m}" % _lt(d), _giai_ho_d(A, BC, d))]
        cau += TL_answer_text(_de_ho_tron(A, AB, AC), ds, _hinh_duong_tron_ba_diem(_goc_ve_ho(A), "ABC", ho=True), 0, dong)
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
    return (r"Một cây mọc trên mặt đất bằng phẳng bị gió mạnh làm gãy không hoàn toàn: phần ngọn đổ xuống, ngọn cây "
            r"$B$ chạm đất, chỗ gãy $C$ vẫn dính liền (hình vẽ). Người ta đo được khoảng cách từ gốc cây $A$ đến ngọn "
            r"cây là $AB = %s\,\text{m}$ và các góc $\widehat{CAB} = %s$, $\widehat{CBA} = %s$. Giả sử chỗ gãy không "
            r"làm thay đổi tổng chiều dài thân cây." % (_xx(AB, 1), _goc(A), _goc(B)))


def _giai_cay_gay(AB, A, B, C, AC, BC, ca_hai):
    s = (r"$\widehat{ACB} = 180^{\circ} - %s - %s = %s$. Theo định lí sin: "
         r"$\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B} = \dfrac{BC}{\sin A}$." "\\\\\n"
         r"$AC = \dfrac{%s\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$"
         % (_goc(A), _goc(B), _goc(C), _xx(AB, 1), _goc(B), _goc(C), _x1(AC, 2)))
    if ca_hai:
        s += (r"; $BC = \dfrac{%s\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$." "\\\\\n"
              r"Chiều cao của cây trước khi gãy là $AC + BC \approx %s\,\text{(m)}$."
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
        de = _de_cay_gay(AB, A, B) + r" Độ dài đoạn thân cây $AC$ còn đứng (làm tròn đến hàng phần mười) là"
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
        de = _de_cay_gay(AB, A, B) + r" Chiều cao của cây trước khi bị gãy (làm tròn đến hàng phần mười) là"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh], _giai_cay_gay(AB, A, B, C, AC, BC, True),
                                  _hinh_cay_gay(AB, A, B, AC), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_T_01(socau, dang=2):
    r"""Trả lời ngắn - cây bị gãy (mức VD): độ dài đoạn thân còn đứng $AC$.

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        dap = _so(AC, 1)
        de = _de_cay_gay(AB, A, B) + r" Tính độ dài đoạn thân cây $AC$ còn đứng (đơn vị mét, làm tròn đến hàng phần mười)."
        cau += MC_SA_answer_const(de, dap, [_so(AC + k, 1) for k in (0.1, -0.1, 0.2)],
                                  _giai_cay_gay(AB, A, B, C, AC, BC, False), _hinh_cay_gay(AB, A, B, AC), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_U_01(socau, dang=2):
    r"""Trả lời ngắn - cây bị gãy (mức VDC): chiều cao cây trước khi gãy.

    CLAUDE THEM 01/10/2026 - theo tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        dap = _so(H, 1)
        de = _de_cay_gay(AB, A, B) + r" Tính chiều cao của cây trước khi bị gãy (đơn vị mét, làm tròn đến hàng phần mười)."
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
        ds = [(r"Tính độ dài đoạn thân cây $AC$ còn đứng (làm tròn đến hàng phần mười, đơn vị mét).",
               r"AC \approx %s\,\text{m}" % _x1(AC, 1), _giai_cay_gay(AB, A, B, C, AC, BC, False)),
              (r"Tính chiều cao của cây trước khi bị gãy (làm tròn đến hàng phần mười, đơn vị mét).",
               r"AC + BC \approx %s\,\text{m}" % _x1(H, 1),
               r"$BC = \dfrac{%s\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$, nên chiều cao cây trước khi gãy là "
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
    return (r"Từ vị trí $A$ cách mặt đất $AH = %d\,\text{m}$, người ta quan sát một cây cao mọc thẳng đứng có gốc $B$ "
            r"và ngọn $C$ (hình vẽ). Biết $HB = %d\,\text{m}$ ($H$, $B$ nằm trên mặt đất nằm ngang) và "
            r"$\widehat{BAC} = %s$." % (AH, HB, _goc(al)))


def _giai_cay_cao_a(AH, HB, al, phi, B, C, AB):
    return (r"Tam giác $AHB$ vuông tại $H$: $AB = \sqrt{%d^{2} + %d^{2}} = %s$ và $\tan\widehat{ABH} = \dfrac{%d}{%d}$, "
            r"nên $\widehat{ABH} \approx %s^{\circ}$." "\\\\\n"
            r"Cây thẳng đứng nên $\widehat{ABC} = 90^{\circ} - \widehat{ABH} \approx %s^{\circ}$; "
            r"$\widehat{ACB} = 180^{\circ} - %s - \widehat{ABC} \approx %s^{\circ}$."
            % (AH, HB, _L(sqrt(AH * AH + HB * HB)), AH, HB, _xx(phi, 2), _xx(B, 2), _goc(al), _xx(C, 2)))


def _giai_cay_cao_b(al, C, AB, BC):
    return (r"Theo định lí sin trong tam giác $ABC$: $\dfrac{BC}{\sin\widehat{BAC}} = \dfrac{AB}{\sin\widehat{ACB}}$ "
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
        de = _de_cay_cao(AH, HB, al) + r" Chiều cao $BC$ của cây (làm tròn đến hàng phần mười) là"
        cau += MC_SA_answer_const(de, dap[1:-1], [x[1:-1] for x in nh],
                                  _giai_cay_cao_a(AH, HB, al, phi, B, C, AB) + "\\\\\n" + _giai_cay_cao_b(al, C, AB, BC),
                                  _hinh_cay_cao(AH, HB, BC), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_V_01(socau, dang=2):
    r"""Trả lời ngắn - cây cao nhìn từ một điểm trên cao (mức VDC): chiều cao cây.

    CLAUDE THEM 01/10/2026 - theo cau 64 tai lieu C3-B2. Co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for _ in range(socau):
        AH, HB, al, phi, B, C, AB, BC = _bo_cay_cao()
        dap = _so(BC, 1)
        de = _de_cay_cao(AH, HB, al) + r" Tính chiều cao $BC$ của cây (đơn vị mét, làm tròn đến hàng phần mười)."
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
        ds = [(r"Tính độ dài $AB$ và số đo các góc $\widehat{ABC}$, $\widehat{ACB}$ (làm tròn đến hàng phần trăm của độ).",
               r"\widehat{ACB} \approx %s^{\circ}" % _xx(C, 2), _giai_cay_cao_a(AH, HB, al, phi, B, C, AB)),
              (r"Tính chiều cao $BC$ của cây (làm tròn đến hàng phần mười, đơn vị mét).",
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
    return (r"Để đo chiều cao tháp chính của cụm tháp Chăm Pô Klông Garai (Ninh Thuận), người ta đặt hai giác kế có "
            r"chân cao $%s\,\text{m}$ tại hai điểm $A$, $B$ trên mặt đất, $AB = %d\,\text{m}$, thẳng hàng với chân $C$ "
            r"của tháp ($A$ gần tháp hơn). Gọi $D$ là đỉnh tháp, $A_1$, $B_1$ là vị trí đặt mắt ngắm của hai giác kế, "
            r"$C_1$ là giao điểm của đường thẳng $A_1B_1$ với $CD$. Đo được $\widehat{DA_1C_1} = %s$ và "
            r"$\widehat{DB_1C_1} = %s$." % (_xx(h, 1), AB, _goc(al), _goc(be)))


def _giai_thap_cham(h, al, be, AB, BD, C1D, CD):
    return (r"$\widehat{A_1DB_1} = \widehat{DA_1C_1} - \widehat{DB_1C_1} = %s$ (góc ngoài tam giác $A_1DB_1$)." "\\\\\n"
            r"Định lí sin trong tam giác $A_1DB_1$: $B_1D = \dfrac{A_1B_1\cdot\sin\widehat{B_1A_1D}}{\sin\widehat{A_1DB_1}}"
            r" = \dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{(m)}$." "\\\\\n"
            r"Tam giác $B_1C_1D$ vuông tại $C_1$: $C_1D = B_1D\cdot\sin %s \approx %s\,\text{(m)}$." "\\\\\n"
            r"Vậy $CD = C_1D + CC_1 \approx %s + %s \approx %s\,\text{(m)}$."
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
        de = _de_thap_cham(h, al, be, AB) + r" Chiều cao $CD$ của tháp (làm tròn đến hàng phần mười) là"
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
        de = _de_thap_cham(h, al, be, AB) + r" Tính chiều cao $CD$ của tháp (đơn vị mét, làm tròn đến hàng phần mười)."
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
_HANG_LT = {0: "hàng đơn vị", 1: "hàng phần mười", 2: "hàng phần trăm", 3: "hàng phần nghìn"}


def _tf_nguong(v):
    """Hai ngưỡng 'tròn' lo < v < hi, cách v đủ xa (để phát biểu so sánh không sát biên)."""
    g = 10 ** math.floor(math.log10(abs(v)))
    if v / g < 2:
        g /= 5
    elif v / g < 5:
        g /= 2
    lo = math.floor(v / g) * g
    if v - lo < 0.15 * g:
        lo -= g
    hi = math.ceil(v / g) * g
    if hi - v < 0.15 * g:
        hi += g
    return round(lo, 6), round(hi, 6)


def _tf_so(mau, v, n, ly, sai, dv="", bdt=None, tu=("lớn hơn", "nhỏ hơn"), mien=(0, None)):
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
        return " (làm tròn đến %s)" % _HANG_LT[k]

    chot = r" Vậy giá trị cần tìm $\approx %s$." % so(v, n + 1)
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
            sai_ds.append((mau % so(w, n) + hang(n), "Làm tròn chưa đúng quy tắc. " + giai))
            break
    if bdt:
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
    for w, ghi in sai:
        if w is None:
            continue
        if simplify(w - v) == 0:
            continue
        sai_ds.append((mau % _L(simplify(w)), (ghi.rstrip(".") + ". " if ghi else "") + ly))
    return dung, sai_ds


def _tf_gop(*cap):
    """Gộp nhiều cặp (dung_ds, sai_ds) rồi tạo một ý bằng _phat_bieu."""
    d, s = [], []
    for a, b in cap:
        d += a
        s += b
    return _phat_bieu(d, s)


def _tf_bdt(mau, v, ly, tu=("lớn hơn", "nhỏ hơn"), dv=""):
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
    sai = [(simplify(mau / tu_), "Đảo tử và mẫu")]
    if simplify(u * s - v * c) != 0:
        sai.append((simplify((p * s - q * c) / (u * s - v * c)), "Sai dấu của $\\cos\\alpha$"))
    if simplify(u * s + v * abs(c)) != 0:
        sai.append((simplify((p * s + q * abs(c)) / (u * s + v * abs(c))), "Lấy nhầm $\\cos\\alpha$ dương"))
    return bt, P, sai


def _n2_lech_truc(h):
    """Số đo góc lệch khỏi trục bắc - nam của hướng h (số trong kí hiệu N x E, S x W...)."""
    h %= 180
    return h if h <= 90 else 180 - h


def _n3_chi_phi(S, gia, ly, ten="lát gạch toàn bộ mảnh đất"):
    """Phát biểu về chi phí (triệu đồng) và diện tích cho TF_H."""
    tien = S * gia / 1000
    T = math.floor(tien)
    mau = r"Chi phí để %s %s $%d$ triệu đồng"
    dung = [(mau % (ten, "lớn hơn", T), ly), (mau % (ten, "nhỏ hơn", T + 1), ly)]
    sai = [(mau % (ten, "lớn hơn", T + 1), ly), (mau % (ten, "nhỏ hơn", T), ly)]
    if T >= 2:
        sai.append((mau % (ten, "nhỏ hơn", T - 1), ly))
    return dung, sai


def _y_ds(dung, sai, ly):
    """Một ý đúng/sai: phát biểu đúng (dung) hoặc sai (sai), cùng lời giải."""
    if sai == dung:
        sai = None
    ds = [(r"{\True %s}" % dung, "Đúng. " + ly)]
    if sai is not None:
        ds.append((r"{%s}" % sai, "Sai. " + ly))
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
        loai = "tù" if tu else "nhọn"
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
        debai = (r"Cho góc $\alpha$ với $%s$ (góc $\alpha$ %s) và $\%s\alpha = %s$. Xét tính đúng, sai của các mệnh đề sau."
                 % (khoang, loai, cho, _L(gia)))

        # a) NB - dấu của các giá trị lượng giác (trừ giá trị đã cho)
        ly_a = r"Góc $\alpha$ %s nên $\cos\alpha %s 0$, $\tan\alpha %s 0$, $\cot\alpha %s 0$ (còn $\sin\alpha > 0$)." % (
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
            ly_b = r"$\sin^{2}\alpha = 1 - \cos^{2}\alpha = 1 - %s = %s$, mà $\sin\alpha > 0$ nên $\sin\alpha = %s$." % (_L(c ** 2), _L(s ** 2), _L(s))
            y2 = _tf_gop(_tf_ct(r"$\sin\alpha = %s$", s, ly_b,
                                [(-s, "Sai dấu: $\\sin\\alpha > 0$"), (1 - c, "Quên bình phương"), (s ** 2, "Quên lấy căn"),
                                 (1 - abs(c), "Nhầm $\\sin\\alpha = 1 - \\left|\\cos\\alpha\\right|$")]),
                         _tf_ct(r"$\sin^{2}\alpha = %s$", s ** 2, ly_b, [(1 + c ** 2, "Nhầm dấu: $\\sin^{2}\\alpha = 1 - \\cos^{2}\\alpha$"),
                                                                           (c ** 2, "Nhầm $\\sin^{2}\\alpha = \\cos^{2}\\alpha$")]))
        elif cho == "sin":
            ly_b = (r"$\cos^{2}\alpha = 1 - \sin^{2}\alpha = 1 - %s = %s$, góc $\alpha$ %s nên $\cos\alpha = %s$."
                    % (_L(s ** 2), _L(c ** 2), loai, _L(c)))
            y2 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", c, ly_b,
                                [(-c, "Sai dấu (xét loại góc)"), (1 - s, "Quên bình phương"), (dau * c ** 2, "Quên lấy căn"),
                                 (dau * (1 - s), "Nhầm $\\cos\\alpha = 1 - \\sin\\alpha$")]),
                         _tf_ct(r"$\cos^{2}\alpha = %s$", c ** 2, ly_b, [(1 + s ** 2, "Nhầm dấu: $\\cos^{2}\\alpha = 1 - \\sin^{2}\\alpha$"),
                                                                           (s ** 2, "Nhầm $\\cos^{2}\\alpha = \\sin^{2}\\alpha$")]))
        elif cho == "tan":
            ly_b = r"$\cot\alpha = \dfrac{1}{\tan\alpha} = %s$." % _L(k)
            y2 = _tf_gop(_tf_ct(r"$\cot\alpha = %s$", k, ly_b,
                                [(-k, "Sai dấu: $\\tan\\alpha$, $\\cot\\alpha$ cùng dấu"), (t, "Nhầm $\\cot\\alpha = \\tan\\alpha$"),
                                 (-t, "Nhầm $\\cot\\alpha = -\\tan\\alpha$"), (1 - t, "Nhầm $\\cot\\alpha = 1 - \\tan\\alpha$")]),
                         _tf_ct(r"$\cot^{2}\alpha = %s$", k ** 2, ly_b, [(t ** 2, "Nhầm $\\cot^{2}\\alpha = \\tan^{2}\\alpha$")]))
        else:
            ly_b = r"$\tan\alpha = \dfrac{1}{\cot\alpha} = %s$." % _L(t)
            y2 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", t, ly_b,
                                [(-t, "Sai dấu: $\\tan\\alpha$, $\\cot\\alpha$ cùng dấu"), (k, "Nhầm $\\tan\\alpha = \\cot\\alpha$"),
                                 (-k, "Nhầm $\\tan\\alpha = -\\cot\\alpha$"), (1 - k, "Nhầm $\\tan\\alpha = 1 - \\cot\\alpha$")]),
                         _tf_ct(r"$\tan^{2}\alpha = %s$", t ** 2, ly_b, [(k ** 2, "Nhầm $\\tan^{2}\\alpha = \\cot^{2}\\alpha$")]))

        # c) VD - giá trị còn lại, hai bước
        if cho in ("sin", "cos"):
            ly_c = ly_b + r" Do đó $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha} = %s$, $\cot\alpha = \dfrac{\cos\alpha}{\sin\alpha} = %s$." % (_L(t), _L(k))
            y3 = _tf_gop(_tf_ct(r"$\tan\alpha = %s$", t, ly_c, [(1 / t, "Đảo tử và mẫu"), (-t, "Sai dấu"), (s * c, "Nhầm $\\tan\\alpha = \\sin\\alpha\\cdot\\cos\\alpha$")]),
                         _tf_ct(r"$\cot\alpha = %s$", k, ly_c, [(t, "Nhầm $\\cot\\alpha = \\tan\\alpha$"), (-k, "Sai dấu")]))
        elif cho == "tan":
            ly_c = (r"$\dfrac{1}{\cos^{2}\alpha} = 1 + \tan^{2}\alpha = %s$ nên $\cos^{2}\alpha = %s$; góc $\alpha$ %s nên "
                    r"$\cos\alpha = %s$, $\sin\alpha = \tan\alpha\cdot\cos\alpha = %s$." % (_L(1 + t ** 2), _L(c ** 2), loai, _L(c), _L(s)))
            y3 = _tf_gop(_tf_ct(r"$\cos\alpha = %s$", c, ly_c, [(-c, "Sai dấu (xét loại góc)"), (dau * 1 / (1 + t ** 2), "Quên lấy căn"),
                                                                 (dau * sqrt(1 + t ** 2), "Quên nghịch đảo")]),
                         _tf_ct(r"$\sin\alpha = %s$", s, ly_c, [(-s, "Sai dấu: $\\sin\\alpha > 0$"), (abs(c), "Nhầm $\\sin$ với $\\cos$")]),
                         _tf_ct(r"$\cos^{2}\alpha = %s$", c ** 2, ly_c, [(1 + t ** 2, "Quên nghịch đảo")]))
        else:
            ly_c = (r"$\dfrac{1}{\sin^{2}\alpha} = 1 + \cot^{2}\alpha = %s$ nên $\sin^{2}\alpha = %s$; vì $\sin\alpha > 0$ nên "
                    r"$\sin\alpha = %s$, $\cos\alpha = \cot\alpha\cdot\sin\alpha = %s$." % (_L(1 + k ** 2), _L(s ** 2), _L(s), _L(c)))
            y3 = _tf_gop(_tf_ct(r"$\sin\alpha = %s$", s, ly_c, [(abs(c), "Nhầm $\\sin$ với $\\cos$"), (1 / (1 + k ** 2), "Quên lấy căn"),
                                                                 (-s, "Sai dấu: $\\sin\\alpha > 0$")]),
                         _tf_ct(r"$\cos\alpha = %s$", c, ly_c, [(-c, "Sai dấu (xét loại góc)"), (abs(s) * dau, "Nhầm $\\cos$ với $\\sin$")]),
                         _tf_ct(r"$\sin^{2}\alpha = %s$", s ** 2, ly_c, [(1 + k ** 2, "Quên nghịch đảo")]))

        # d) VDC - biểu thức chứa góc bù, góc phụ (2 biểu thức khác nhau, mỗi biểu thức nhiều kết quả sai)
        dung, sai = [], []
        for terms, hs, P, Ps in bts:
            bt = ""
            for j, (h, i) in enumerate(zip(hs, terms)):
                he = ("" if h == 1 else ("-" if h == -1 else str(h))) if j == 0 else \
                     (" + " if h == 1 else (" - " if h == -1 else (" + %d" % h if h > 0 else " - %d" % -h)))
                bt += he + _BU_PHU_TF_J[i][0]
            doi_ra = ", ".join(r"$%s = %s$" % (_BU_PHU_TF_J[i][0], _TEN_BU_PHU[i]) for i in terms)
            ly_d = (r"Theo quan hệ góc bù, góc phụ: %s. Với $\sin\alpha = %s$, $\cos\alpha = %s$, $\tan\alpha = %s$, "
                    r"$\cot\alpha = %s$ ta được biểu thức bằng $%s$." % (doi_ra, _L(s), _L(c), _L(t), _L(k), _L(P)))
            a_, b_ = _tf_ct("$" + bt + " = %s$", P, ly_d, [(Q, "Nhầm quan hệ góc bù / góc phụ ở một số hạng") for Q in Ps])
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
        loai = "nhọn" if nhon else "tù"
        debai = (r"Cho tam giác $ABC$ có góc $A$ %s, $BC = %s$, $\widehat{B} = %s$ và bán kính đường tròn ngoại tiếp "
                 r"$R = %d$. Xét tính đúng, sai của các mệnh đề sau." % (loai, _L(a), _goc(B), R))
        # a) NB - nhận ra định lí sin
        ly_a = r"Định lí sin: $\dfrac{BC}{\sin A} = \dfrac{CA}{\sin B} = \dfrac{AB}{\sin C} = 2R$."
        y1 = _phat_bieu(
            [(r"$\dfrac{BC}{\sin A} = 2R$", ly_a), (r"$\dfrac{CA}{\sin B} = 2R$", ly_a), (r"$\dfrac{AB}{\sin C} = 2R$", ly_a),
             (r"$BC = 2R\sin A$", ly_a), (r"$\sin A = \dfrac{BC}{2R}$", ly_a)],
            [(r"$\dfrac{BC}{\sin A} = R$", ly_a), (r"$\dfrac{BC}{\sin B} = 2R$", ly_a), (r"$BC = R\sin A$", ly_a),
             (r"$\dfrac{CA}{\sin A} = 2R$", ly_a), (r"$\sin A = \dfrac{2R}{BC}$", ly_a), (r"$\dfrac{AB}{\cos C} = 2R$", ly_a)])
        # b) TH - một bước: sin A = BC/(2R), rồi chọn góc theo loại góc
        ly_b = r"$\sin A = \dfrac{BC}{2R} = %s$; góc $A$ %s nên $\widehat{A} = %s$." % (_L(sA), loai, _goc(A))
        dung = [(r"$\widehat{A} = %s$" % _goc(A), ly_b), (r"$\sin A = %s$" % _L(sA), ly_b)]
        sai = [(r"$\widehat{A} = %s$" % _goc(180 - A), "Không xét góc $A$ %s. " % loai + ly_b)]
        if A != 45 and 90 - A > 0:
            sai.append((r"$\widehat{A} = %s$" % _goc(90 - A), ly_b))
        for w, ghi in ((sA / 2, "Quên nhân 2 ở $2R$"), (2 * sA, "Nhầm $\\sin A = \\dfrac{BC}{R}$")):
            if 0 < w <= 1 and simplify(w - sA) != 0:
                sai.append((r"$\sin A = %s$" % _L(simplify(w)), ghi + ". " + ly_b))
        y2 = _phat_bieu(dung, sai)
        # c) VD - cạnh CA
        ly_c = r"$CA = 2R\sin B = %d\cdot\sin %s$." % (2 * R, _goc(B))
        y3 = _tf_gop(_tf_so(r"$CA \approx %s$", b, 1, ly_c,
                            [(R * _sin_d(B), "Quên nhân 2 (dùng $R\\sin B$)"), (2 * R * _cos_d(B), "Nhầm $\\sin$ với $\\cos$"),
                             (2 * R * _sin_d(C), "Nhầm góc: đó là cạnh $AB$"), (2 * R / _sin_d(B), "Nhầm $CA = \\dfrac{2R}{\\sin B}$")],
                            bdt=r"$CA$ %s $%s$"))
        # d) VDC - diện tích
        C_sai = A - B if not nhon else None        # nếu lấy nhầm A = 180 - A
        ly_d = (r"$\widehat{C} = 180^{\circ} - %s - %s = %s$, $AB = 2R\sin C$, nên "
                r"$S = \dfrac{1}{2}\cdot BC\cdot CA\cdot\sin C = 2R^{2}\sin A\sin B\sin C$." % (_goc(A), _goc(B), _goc(C)))
        sai = [(2 * S, "Quên hệ số $\\dfrac{1}{2}$"), (S / 2, "Nhân thừa $\\dfrac{1}{2}$"),
               (0.5 * float(a) * b * _sin_d(B), "Dùng nhầm góc $B$ thay cho góc $C$ xen giữa"),
               (0.5 * float(a) * b * _cos_d(C), "Nhầm $\\sin C$ với $\\cos C$")]
        if C_sai and C_sai > 0:
            sai.append((2 * R * R * _sin_d(A) * _sin_d(B) * _sin_d(C_sai), "Lấy nhầm góc $A$ nhọn"))
        y4 = _tf_gop(_tf_so(r"Diện tích tam giác $ABC$ xấp xỉ $%s$", S, 1, ly_d, sai,
                            bdt=r"Diện tích tam giác $ABC$ %s $%s$"))
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
         "Định lí côsin"),
        (r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s%s}" % (X, y, z, x, y, z),
         random.choice([r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{%s%s}" % (X, y, z, x, y, z),
                        r"\cos %s = \dfrac{%s^{2} + %s^{2} - %s^{2}}{2%s%s}" % (X, x, y, z, y, z)]),
         "Hệ quả của định lí côsin"),
        (r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s} = 2R" % (x, X, y, Y),
         random.choice([r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s} = R" % (x, X, y, Y),
                        r"\dfrac{%s}{\sin %s} = \dfrac{%s}{\sin %s} = 2R" % (x, Y, y, X)]),
         r"Định lí sin ($R$ là bán kính đường tròn ngoại tiếp)"),
        (r"S = \dfrac{1}{2}%s%s\sin %s" % (y, z, X),
         random.choice([r"S = \dfrac{1}{2}%s%s\sin %s" % (y, z, Y), r"S = %s%s\sin %s" % (y, z, X)]),
         r"Công thức diện tích theo hai cạnh và góc xen giữa"),
        (r"S = \dfrac{abc}{4R}", random.choice([r"S = \dfrac{abc}{2R}", r"S = \dfrac{4R}{abc}"]),
         r"Công thức diện tích theo bán kính đường tròn ngoại tiếp $R$"),
        (r"S = pr", random.choice([r"S = 2pr", r"S = \dfrac{r}{p}"]),
         r"Công thức diện tích theo nửa chu vi $p$ và bán kính đường tròn nội tiếp $r$"),
        (r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}",
         random.choice([r"S = \sqrt{\left(p - a\right)\left(p - b\right)\left(p - c\right)}",
                        r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}"]),
         r"Công thức Heron ($p$ là nửa chu vi)"),
        (r"S = \dfrac{1}{2}%s\cdot h_%s" % (x, x), random.choice([r"S = %s\cdot h_%s" % (x, x), r"S = \dfrac{1}{2}%s\cdot h_%s" % (y, x)]),
         r"Công thức diện tích theo cạnh và đường cao tương ứng"),
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
        debai = (r"Cho tam giác $ABC$ có $BC = a = %d$, $CA = b = %d$, $AB = c = %d$. Gọi $S$, $p$, $R$, $r$ lần lượt là "
                 r"diện tích, nửa chu vi, bán kính đường tròn ngoại tiếp, nội tiếp của tam giác. Xét tính đúng, sai của các "
                 r"mệnh đề sau." % (a, b, c))
        # a) NB - nhận ra công thức (nhiều công thức đúng, nhiều biến dạng sai)
        dung, sai = [], []
        for _k in range(6):
            d_, s_, ly = _cong_thuc_tam_giac()
            dung.append((d_, ly))
            sai.append((s_, ly))
        y1 = _phat_bieu(dung, sai)
        # b) TH - tính cực kì đơn giản: nửa chu vi hoặc côsin một góc
        ly_p = r"$p = \dfrac{a + b + c}{2} = \dfrac{%d + %d + %d}{2} = %s$." % (a, b, c, _L(Rational(a + b + c, 2)))
        dung, sai = _tf_ct(r"$p = %s$", Rational(a + b + c, 2), ly_p,
                           [(Integer(a + b + c), "Đó là chu vi, chưa chia 2"), (Rational(a + b + c, 3), "Chia nhầm cho 3")])
        for X, (u, v, w) in random.sample([("A", (b, c, a)), ("B", (a, c, b)), ("C", (a, b, c))], 2):
            cs = Rational(u * u + v * v - w * w, 2 * u * v)
            ly = r"$\cos %s = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$." % (X, u, v, w, u, v, _L(cs))
            d_, s_ = _tf_ct(r"$\cos %s = %s$" % (X, "%s"), cs, ly,
                            [(-cs, "Sai dấu (đổi vị trí cạnh đối)"), (2 * cs, "Quên số 2 ở mẫu"),
                             (Rational(u * u + w * w - v * v, 2 * u * w), "Lấy nhầm cạnh đối diện")])
            dung += d_
            sai += s_
        y2 = _phat_bieu(dung, sai)
        # c) VD - diện tích (Heron)
        ly_c = r"$p = %d$, $S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)} = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$." % (
            p, p, p - a, p - b, p - c, S)
        y3 = _tf_gop(_tf_ct(r"$S = %s$", Integer(S), ly_c,
                            [(Integer(2 * S), "Nhân thừa 2"), (sqrt((p - a) * (p - b) * (p - c)), "Thiếu thừa số $p$"),
                             (Rational(S, 2), "Chia thừa 2"), (sqrt(p * (p - a) * (p - b)), "Thiếu thừa số $\\left(p - c\\right)$")],
                            them=[r"$S^{2} = %d$" % (S * S)]))
        # d) VDC - đường cao / bán kính (hai đại lượng khác nhau)
        dung, sai = [], []
        for chon in random.sample(["h", "r", "R"], 2):
            if chon == "h":
                ten, canh, khac = random.choice([("a", a, b), ("b", b, c), ("c", c, a)])
                ha = Rational(2 * S, canh)
                ly = r"$S = \dfrac{1}{2}%s\cdot h_%s \Rightarrow h_%s = \dfrac{2S}{%s} = \dfrac{%d}{%d} = %s$." % (ten, ten, ten, ten, 2 * S, canh, _L(ha))
                d_, s_ = _tf_ct(r"$h_%s = %s$" % (ten, "%s"), ha, ly,
                                [(ha / 2, "Quên nhân 2"), (Rational(2 * S, khac), "Chia nhầm cạnh"), (Rational(canh, 2 * S), "Đảo tử và mẫu")])
            elif chon == "r":
                r_ = Rational(S, p)
                ly = r"$S = pr \Rightarrow r = \dfrac{S}{p} = \dfrac{%d}{%d} = %s$." % (S, p, _L(r_))
                d_, s_ = _tf_ct(r"$r = %s$", r_, ly,
                                [(2 * r_, "Nhầm $S = \\dfrac{1}{2}pr$"), (Rational(S, 2 * p), "Chia cho chu vi thay vì nửa chu vi"),
                                 (Rational(a * b * c, 4 * S), "Nhầm sang bán kính ngoại tiếp")])
            else:
                R_ = Rational(a * b * c, 4 * S)
                ly = r"$S = \dfrac{abc}{4R} \Rightarrow R = \dfrac{abc}{4S} = \dfrac{%d}{%d} = %s$." % (a * b * c, 4 * S, _L(R_))
                d_, s_ = _tf_ct(r"$R = %s$", R_, ly,
                                [(2 * R_, "Nhầm $R = \\dfrac{abc}{2S}$"), (4 * R_, "Quên chia 4"), (Rational(S, p), "Nhầm sang bán kính nội tiếp")])
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
        debai = (r"Cho hình bình hành $ABCD$ có $AB = %d$, $AD = %d$, $\widehat{BAD} = %s$; $O$ là giao điểm hai đường chéo. "
                 r"Xét tính đúng, sai của các mệnh đề sau." % (m, n, _goc(A)))
        # a) NB - tính chất hình bình hành
        ly_a = (r"Hình bình hành có các cạnh đối bằng nhau ($BC = AD = %d$, $CD = AB = %d$), các góc đối bằng nhau, "
                r"hai góc kề một cạnh bù nhau: $\widehat{ABC} = \widehat{ADC} = 180^{\circ} - %s = %s$, $\widehat{BCD} = %s$."
                % (n, m, _goc(A), _goc(180 - A), _goc(A)))
        y1 = _phat_bieu(
            [(r"$\widehat{ABC} = %s$" % _goc(180 - A), ly_a), (r"$\widehat{ADC} = %s$" % _goc(180 - A), ly_a),
             (r"$\widehat{BCD} = %s$" % _goc(A), ly_a), (r"$BC = %d$" % n, ly_a), (r"$CD = %d$" % m, ly_a)],
            [(r"$\widehat{ABC} = %s$" % _goc(A), ly_a), (r"$\widehat{ADC} = %s$" % _goc(A), ly_a),
             (r"$\widehat{BCD} = %s$" % _goc(180 - A), ly_a), (r"$BC = %d$" % m, ly_a), (r"$CD = %d$" % n, ly_a)])
        # b) TH - định lí côsin trong tam giác ABD (một lần thay số)
        ly_b = r"Trong tam giác $ABD$: $BD^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %s = %s$." % (m * m, n * n, m, n, _goc(A), _L(BD2))
        y2 = _tf_gop(_tf_ct(r"$BD = %s$", sqrt(BD2), ly_b,
                            [(sqrt(AC2), "Sai dấu của $\\cos %s$" % _goc(A)), (sqrt(m * m + n * n), "Quên số hạng $-2\\cdot AB\\cdot AD\\cos A$"),
                             (sqrt(m * m + n * n - m * n * cs), "Quên hệ số 2")],
                            them=[r"$BD^{2} = %s$" % _L(BD2)]))
        # c) VD - đường chéo AC (tam giác ABC, góc B = 180 - A)
        ly_c = (r"$BC = AD = %d$, $\widehat{ABC} = %s$; trong tam giác $ABC$: $AC^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %s = %s$."
                % (n, _goc(180 - A), m * m, n * n, m, n, _goc(180 - A), _L(AC2)))
        y3 = _tf_gop(_tf_ct(r"$AC = %s$", sqrt(AC2), ly_c,
                            [(sqrt(BD2), "Dùng nhầm góc $A$ thay cho góc $B$"), (sqrt(m * m + n * n), "Quên số hạng chứa $\\cos B$"),
                             (sqrt(m * m + n * n + m * n * cs), "Quên hệ số 2")],
                            them=[r"$AC^{2} = %s$" % _L(AC2), r"$AC^{2} + BD^{2} = %d$" % (2 * (m * m + n * n))]))
        # d) VDC - côsin góc giữa hai đường chéo (tam giác OAB)
        ly_d = (r"$OA = \dfrac{AC}{2} = %s$, $OB = \dfrac{BD}{2} = %s$; trong tam giác $OAB$: "
                r"$\cos\widehat{AOB} = \dfrac{OA^{2} + OB^{2} - AB^{2}}{2\cdot OA\cdot OB}$." % (_L(sqrt(OA2)), _L(sqrt(OB2))))
        sai_c = [(-cosO, "Nhầm sang góc $\\widehat{AOD}$ (cạnh $AD$)"),
                 (float((AC2 + BD2 - m * m) / (2 * sqrt(AC2) * sqrt(BD2))), "Quên chia đôi hai đường chéo"),
                 (float((OA2 + OB2 - m * m) / (sqrt(OA2) * sqrt(OB2))), "Quên số 2 ở mẫu")]
        d1, s1 = _tf_so(r"$\cos\widehat{AOB} \approx %s$", cosO, 2, ly_d, sai_c, mien=(-1, 1))
        if _xa_bien(gocO):
            d2, s2 = _tf_so(r"$\widehat{AOB} \approx %s$", gocO, 0, ly_d + r" Suy ra $\widehat{AOB}$ bằng máy tính.",
                            [(180 - gocO, "Nhầm sang góc kề bù $\\widehat{AOD}$")], dv=r"^{\circ}")
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
        debai = _de_nui_toa_nha(h, al, be) + " Xét tính đúng, sai của các mệnh đề sau."
        # a) NB - đọc góc từ hình
        ly_a = (r"$AB$ thẳng đứng, $AC$ hợp với phương ngang góc $%s$ nên $\widehat{BAC} = 90^{\circ} - %s = %s$; "
                r"$BC$ hợp với phương ngang góc $%s$ (hướng lên) nên $\widehat{ABC} = 90^{\circ} + %s = %s$."
                % (_goc(al), _goc(al), _goc(90 - al), _goc(be), _goc(be), _goc(90 + be)))
        y1 = _phat_bieu(
            [(r"$\widehat{BAC} = %s$" % _goc(90 - al), ly_a), (r"$\widehat{ABC} = %s$" % _goc(90 + be), ly_a),
             (r"$\widehat{CAH} = %s$" % _goc(al), ly_a)],
            [(r"$\widehat{BAC} = %s$" % _goc(al), ly_a), (r"$\widehat{ABC} = %s$" % _goc(90 - be), ly_a),
             (r"$\widehat{ABC} = %s$" % _goc(be), ly_a), (r"$\widehat{BAC} = %s$" % _goc(90 + al), ly_a)])
        # b) TH - tổng ba góc / góc tại C
        ly_b = (r"$\widehat{ACB} = 180^{\circ} - %s - %s = %s$; $CH$ thẳng đứng nên $\widehat{ACH} = 90^{\circ} - %s = %s$."
                % (_goc(90 - al), _goc(90 + be), _goc(al - be), _goc(al), _goc(90 - al)))
        y2 = _phat_bieu(
            [(r"$\widehat{ACB} = %s$" % _goc(al - be), ly_b), (r"$\widehat{ACH} = %s$" % _goc(90 - al), ly_b)],
            [(r"$\widehat{ACB} = %s$" % _goc(al + be), ly_b), (r"$\widehat{ACB} = %s$" % _goc(90 - al + be), ly_b),
             (r"$\widehat{ACH} = %s$" % _goc(al), ly_b), (r"$\widehat{ACB} = %s$" % _goc(180 - al - be), ly_b)])
        # c) VD - định lí sin tìm AC
        ly_c = _giai_goc_nui(h, al, be, AC).split("\\\\\n")[-1]
        y3 = _tf_gop(_tf_so(r"$AC \approx %s$", AC, 0, ly_c,
                            [(h * _cos_d(be) / _sin_d(al + be), "Nhầm $\\widehat{ACB} = %s$" % _goc(al + be)),
                             (h * _sin_d(al - be) / _cos_d(be), "Đảo tử và mẫu"),
                             (h * _sin_d(90 - al) / _sin_d(al - be), "Dùng nhầm góc $\\widehat{BAC}$ (đối diện $BC$)"),
                             (h / _sin_d(al - be), "Quên nhân $\\sin\\widehat{ABC}$")], dv=r"\,\text{m}",
                            bdt=r"Khoảng cách $AC$ %s $%s$"))
        # d) VDC - chiều cao ngọn núi
        ly_d = _giai_goc_nui(h, al, be, AC).split("\\\\\n")[-1] + " " + _giai_cao_nui(al, CH, AC)
        y4 = _tf_gop(_tf_so(r"Ngọn núi cao khoảng $%s$ so với mặt đất", CH, 0, ly_d,
                            [(CH + h, "Cộng thừa chiều cao toà nhà"), (AC * _cos_d(al), "Nhầm $\\sin$ với $\\cos$"),
                             (AC * math.tan(math.radians(al)), "Nhầm $CH = AC\\cdot\\tan %s$" % _goc(al)), (CH - h, "Trừ nhầm chiều cao toà nhà")],
                            dv=r"\,\text{m}", bdt=r"Ngọn núi %s $%s$ so với mặt đất", tu=("cao hơn", "thấp hơn")))
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
        debai = _de_dia_co(a, b, c) + " Xét tính đúng, sai của các mệnh đề sau."
        cm, cm2 = r"\,\text{cm}", r"\,\text{cm}^{2}"
        # a) NB - nửa chu vi, chu vi
        ly_a = r"$p = \dfrac{%s + %s + %s}{2} = %s$ (cm), chu vi $2p = %s$ (cm)." % (_x1(a, 1), _x1(b, 1), _x1(c, 1), _xx(p, 2), _xx(2 * p, 2))
        y1 = _phat_bieu(
            [(r"Nửa chu vi tam giác $ABC$ là $p = %s%s$" % (_xx(p, 2), cm), ly_a),
             (r"Chu vi tam giác $ABC$ là $%s%s$" % (_xx(2 * p, 2), cm), ly_a)],
            [(r"Nửa chu vi tam giác $ABC$ là $p = %s%s$" % (_xx(2 * p, 2), cm), "Đó là chu vi. " + ly_a),
             (r"Nửa chu vi tam giác $ABC$ là $p = %s%s$" % (_xx((a + b + c) / 3, 2), cm), "Chia nhầm cho 3. " + ly_a),
             (r"Chu vi tam giác $ABC$ là $%s%s$" % (_xx(p, 2), cm), "Đó là nửa chu vi. " + ly_a)])
        # b) TH - Heron
        ly_b = r"Theo công thức Heron: $S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$."
        y2 = _tf_gop(_tf_so(r"$S_{ABC} \approx %s$", S, 1, ly_b,
                            [(2 * S, "Nhân thừa 2"), (math.sqrt((p - a) * (p - b) * (p - c)), "Thiếu thừa số $p$"),
                             (math.sqrt(2 * p * (p - a) * (p - b) * (p - c)), "Dùng chu vi thay cho nửa chu vi")],
                            dv=cm2, bdt=r"Diện tích tam giác $ABC$ %s $%s$"))
        # c) VD - góc lớn nhất (đối diện cạnh lớn nhất)
        doi = {"A": "BC", "B": "CA", "C": "AB"}[dinh]
        goc_k = {"A": (b, c, a), "B": (a, c, b), "C": (a, b, c)}
        cac_goc = {X: math.degrees(math.acos((u * u + v * v - w * w) / (2 * u * v))) for X, (u, v, w) in goc_k.items()}
        nho = min(cac_goc, key=cac_goc.get)
        ly_c = (r"Góc lớn nhất là góc $%s$ đối diện cạnh lớn nhất $%s$; $\cos %s \approx %s$ nên $\widehat{%s} \approx %d^{\circ}$."
                % (dinh, doi, dinh, _xx(math.cos(math.radians(g)), 4), dinh, _lt(g)))
        dung = [(r"Góc lớn nhất của tam giác $ABC$ là góc $%s$" % dinh, ly_c)]
        sai = [(r"Góc lớn nhất của tam giác $ABC$ là góc $%s$" % X, ly_c) for X in "ABC" if X != dinh]
        d_, s_ = _tf_so(r"Góc lớn nhất của tam giác $ABC$ xấp xỉ $%s$", g, 0, ly_c,
                        [(180 - g, "Nhầm dấu của côsin"), (cac_goc[nho], "Đó là góc nhỏ nhất")], dv=r"^{\circ}")
        (dung if g > 90 else sai).append((r"Tam giác $ABC$ có một góc tù", ly_c))
        y3 = _phat_bieu(dung + d_, sai + s_)
        # d) VDC - bán kính đĩa
        ly_d = r"Mép đĩa là đường tròn ngoại tiếp tam giác $ABC$, $R = \dfrac{abc}{4S}$."
        sai_R = [(2 * R, "Đó là đường kính"), (4 * R, "Quên chia 4"), (S / p, "Nhầm sang bán kính nội tiếp $r = \\dfrac{S}{p}$")]
        d1, s1 = _tf_so(r"Bán kính chiếc đĩa xấp xỉ $%s$", R, 1, ly_d, sai_R, dv=cm,
                        bdt=r"Bán kính chiếc đĩa %s $%s$")
        d2, s2 = _tf_so(r"Đường kính chiếc đĩa xấp xỉ $%s$", 2 * R, 1, ly_d, [(R, "Đó là bán kính"), (4 * R, "Nhân thừa 2")], dv=cm) \
            if _xa_bien(2 * R, 1) else ([], [])
        y4 = _phat_bieu(d1 + d2, s1 + s2)
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
        debai = _de_ho_tron(A, AB, AC) + " Xét tính đúng, sai của các mệnh đề sau."
        g = _goc(A)
        # a) NB - định lí côsin
        ly_a = r"Định lí côsin trong tam giác $ABC$ cho cạnh $BC$ đối diện góc $A$."
        y1 = _phat_bieu(
            [(r"$BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$\cos %s = \dfrac{AB^{2} + AC^{2} - BC^{2}}{2\cdot AB\cdot AC}$" % g, ly_a)],
            [(r"$BC^{2} = AB^{2} + AC^{2} + 2\cdot AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$BC^{2} = AB^{2} + AC^{2} - AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$BC = AB + AC - 2\cdot AB\cdot AC\cdot\cos %s$" % g, ly_a),
             (r"$\cos %s = \dfrac{AB^{2} + AC^{2} + BC^{2}}{2\cdot AB\cdot AC}$" % g, ly_a)])
        # b) TH - tính BC
        y2 = _tf_gop(_tf_so(r"$BC \approx %s$", BC, 1, _giai_ho_bc(A, AB, AC, BC),
                            [(math.sqrt(AB * AB + AC * AC), "Quên số hạng chứa $\\cos A$"),
                             (math.sqrt(AB * AB + AC * AC + 2 * AB * AC * _cos_d(A)), "Sai dấu"),
                             (math.sqrt(AB * AB + AC * AC - AB * AC * _cos_d(A)), "Quên hệ số 2")],
                            dv=r"\,\text{m}", bdt=r"$BC$ %s $%s$"))
        # c) VD - định lí sin cho đường kính
        ly_c = r"Bờ hồ là đường tròn ngoại tiếp tam giác $ABC$; theo định lí sin $\dfrac{BC}{\sin A} = \dfrac{AC}{\sin B} = 2R$ chính là đường kính."
        y3 = _phat_bieu(
            [(r"Đường kính hồ bằng $\dfrac{BC}{\sin\widehat{BAC}}$", ly_c), (r"Bán kính hồ bằng $\dfrac{BC}{2\sin\widehat{BAC}}$", ly_c),
             (r"Đường kính hồ bằng $\dfrac{AC}{\sin\widehat{ABC}}$", ly_c)],
            [(r"Đường kính hồ bằng $\dfrac{BC}{2\sin\widehat{BAC}}$", ly_c), (r"Bán kính hồ bằng $\dfrac{BC}{\sin\widehat{BAC}}$", ly_c),
             (r"Đường kính hồ bằng $\dfrac{BC}{\cos\widehat{BAC}}$", ly_c), (r"Đường kính hồ bằng $BC\cdot\sin\widehat{BAC}$", ly_c),
             (r"Đường kính hồ bằng $\dfrac{AC}{\sin\widehat{BAC}}$", ly_c)])
        # d) VDC - đường kính hồ
        ly_d = _giai_ho_bc(A, AB, AC, BC) + " " + _giai_ho_d(A, BC, d)
        y4 = _tf_gop(_tf_so(r"Đường kính hồ xấp xỉ $%s$", d, 0, ly_d,
                            [(d / 2, "Đó là bán kính"), (BC * _sin_d(A), "Nhầm $d = BC\\cdot\\sin A$"),
                             (math.sqrt(AB * AB + AC * AC) / _sin_d(A), "Tính sai $BC$ (quên số hạng chứa $\\cos A$)")],
                            dv=r"\,\text{m}", bdt=r"Đường kính hồ %s $%s$"))
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_duong_tron_ba_diem(_goc_ve_ho(A), "ABC", ho=True), 0, socot)
    return cau


def L10_C3_TF_P_01(socau, socot=1):
    r"""Đúng/Sai - cây bị gãy (có hình): a) góc $ACB$, b) đoạn $AC$, c) đoạn $BC$, d) chiều cao cây trước khi gãy.

    CLAUDE THEM 01/10/2026 - cung boi canh VD036_MC_R/MC_S/SA_T/SA_U/TL_L. Co Lan duyet lai.
    01/10/2026: moi y nhieu phat bieu dung + nhieu phat bieu sai (y co Lan).
    """
    cau = ""
    for _ in range(socau):
        AB, A, B, C, AC, BC, H = _bo_cay_gay()
        debai = _de_cay_gay(AB, A, B) + " Xét tính đúng, sai của các mệnh đề sau."
        m = r"\,\text{m}"
        # a) NB - tổng ba góc
        ly_a = r"$\widehat{ACB} = 180^{\circ} - %s - %s = %s$." % (_goc(A), _goc(B), _goc(C))
        y1 = _phat_bieu(
            [(r"$\widehat{ACB} = %s$" % _goc(C), ly_a), (r"$\widehat{ACB} + \widehat{CAB} = %s$" % _goc(180 - B), ly_a)],
            [(r"$\widehat{ACB} = %s$" % _goc(C + 10), ly_a), (r"$\widehat{ACB} = %s$" % _goc(A + B), ly_a),
             (r"$\widehat{ACB} = %s$" % _goc(90 - B), "Không có góc vuông tại $A$. " + ly_a),
             (r"$\widehat{ACB} + \widehat{CAB} = %s$" % _goc(180 - A), ly_a)])
        # b) TH - định lí sin cho AC
        ly_b = r"Định lí sin: $AC = \dfrac{AB\cdot\sin B}{\sin C} = \dfrac{%s\cdot\sin %s}{\sin %s}$." % (_xx(AB, 1), _goc(B), _goc(C))
        y2 = _tf_gop(_tf_so(r"$AC \approx %s$", AC, 1, ly_b,
                            [(BC, "Dùng nhầm góc $A$ (đó là $BC$)"), (AB * _sin_d(C) / _sin_d(B), "Đảo tử và mẫu"),
                             (AB * math.tan(math.radians(B)), "Coi tam giác vuông tại $A$")], dv=m, bdt=r"Đoạn $AC$ %s $%s$"))
        # c) VD - BC
        ly_c = r"$BC = \dfrac{AB\cdot\sin A}{\sin C} = \dfrac{%s\cdot\sin %s}{\sin %s}$." % (_xx(AB, 1), _goc(A), _goc(C))
        y3 = _tf_gop(_tf_so(r"$BC \approx %s$", BC, 1, ly_c,
                            [(AC, "Dùng nhầm góc $B$ (đó là $AC$)"), (AB / _cos_d(B), "Coi tam giác vuông tại $A$"),
                             (AB * _sin_d(A) / _sin_d(B), "Dùng nhầm góc đối diện $AB$")], dv=m, bdt=r"Đoạn $BC$ %s $%s$"))
        # d) VDC - chiều cao cây trước khi gãy
        ly_d = ly_b + " " + ly_c + r" Chiều cao cây trước khi gãy là $AC + BC$."
        y4 = _tf_gop(_tf_so(r"Trước khi gãy, cây cao khoảng $%s$", H, 1, ly_d,
                            [(AC + AB, "Cộng nhầm $AB$"), (AC, "Quên phần ngọn bị gãy $BC$"), (BC + AB, "Cộng nhầm $AB$"),
                             (math.sqrt(AB * AB + AC * AC) + AC, "Coi tam giác vuông tại $A$")],
                            dv=m, bdt=r"Trước khi gãy, cây %s $%s$", tu=("cao hơn", "thấp hơn")))
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
        debai = _de_thap_cham(h, al, be, AB) + " Xét tính đúng, sai của các mệnh đề sau."
        m = r"\,\text{m}"
        # a) NB - góc ngoài, góc kề bù
        ly_a = (r"$\widehat{DA_1B_1} = 180^{\circ} - %s = %s$ (kề bù với $\widehat{DA_1C_1}$); góc $\widehat{DA_1C_1}$ là góc ngoài "
                r"của tam giác $A_1DB_1$ nên $\widehat{A_1DB_1} = %s - %s = %s$." % (_goc(al), _goc(180 - al), _goc(al), _goc(be), _goc(al - be)))
        y1 = _phat_bieu(
            [(r"$\widehat{A_1DB_1} = %s$" % _goc(al - be), ly_a), (r"$\widehat{DA_1B_1} = %s$" % _goc(180 - al), ly_a)],
            [(r"$\widehat{A_1DB_1} = %s$" % _goc(180 - al - be), ly_a), (r"$\widehat{A_1DB_1} = %s$" % _goc(al + be), ly_a),
             (r"$\widehat{DA_1B_1} = %s$" % _goc(al), ly_a), (r"$\widehat{A_1DB_1} = %s$" % _goc(90 - be), ly_a)])
        # b) TH - định lí sin trong tam giác A1DB1
        ly_b = r"Định lí sin: $B_1D = \dfrac{A_1B_1\cdot\sin\left(180^{\circ} - %s\right)}{\sin %s}$." % (_goc(al), _goc(al - be))
        y2 = _tf_gop(_tf_so(r"$B_1D \approx %s$", BD, 1, ly_b,
                            [(AB * _sin_d(be) / _sin_d(al - be), "Dùng nhầm góc $B_1$ (đó là $A_1D$)"),
                             (AB * _sin_d(al) / _sin_d(be), "Chia nhầm cho $\\sin %s$" % _goc(be)),
                             (AB / _sin_d(al - be), "Quên nhân $\\sin\\widehat{DA_1B_1}$")], dv=m, bdt=r"$B_1D$ %s $%s$"))
        # c) VD - tam giác vuông B1C1D
        ly_c = ly_b + r" Tam giác $B_1C_1D$ vuông tại $C_1$: $C_1D = B_1D\cdot\sin %s$." % _goc(be)
        y3 = _tf_gop(_tf_so(r"$C_1D \approx %s$", C1D, 1, ly_c,
                            [(BD * _cos_d(be), "Nhầm $\\sin$ với $\\cos$"), (BD * math.tan(math.radians(be)), "Nhầm $C_1D = B_1D\\cdot\\tan %s$" % _goc(be)),
                             (BD, "Lấy cạnh huyền $B_1D$")], dv=m, bdt=r"$C_1D$ %s $%s$"))
        # d) VDC - chiều cao tháp
        ly_d = ly_c + r" $CD = C_1D + CC_1 = C_1D + %s$ (phải cộng chiều cao giác kế)." % _xx(h, 1)
        y4 = _tf_gop(_tf_so(r"Tháp cao khoảng $%s$", CD, 1, ly_d,
                            [(C1D, "Quên cộng chiều cao giác kế"), (C1D + 2 * h, "Cộng chiều cao giác kế hai lần"),
                             (BD * _cos_d(be) + h, "Nhầm $\\sin$ với $\\cos$")],
                            dv=m, bdt=r"Tháp %s $%s$", tu=("cao hơn", "thấp hơn")))
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
        debai = (r"Hai tàu đánh cá cùng xuất phát từ bến $A$, đi thẳng đều theo hai hướng hợp với nhau góc $%s$. "
                 r"Tàu thứ nhất đi với tốc độ $%d$ hải lí/giờ, tàu thứ hai đi với tốc độ $%d$ hải lí/giờ. Gọi $B$, $C$ "
                 r"là vị trí hai tàu sau $%s$ giờ. Xét tính đúng, sai của các mệnh đề sau." % (_goc(g), v1, v2, _xx(t, 1)))
        # a) NB - quãng đường = vận tốc x thời gian
        ly_a = r"$AB = %d\cdot %s = %s$ (hải lí), $AC = %d\cdot %s = %s$ (hải lí)." % (v1, _xx(t, 1), _xx(b, 1), v2, _xx(t, 1), _xx(c, 1))
        y1 = _phat_bieu(
            [(r"$AB = %s$ hải lí" % _xx(b, 1), ly_a), (r"$AC = %s$ hải lí" % _xx(c, 1), ly_a)],
            [(r"$AB = %s$ hải lí" % _xx(v1 + t, 1), ly_a), (r"$AB = %s$ hải lí" % _xx(c, 1), ly_a),
             (r"$AC = %s$ hải lí" % _xx(b, 1), ly_a), (r"$AB = %s$ hải lí" % _xx(v1 / t, 1), ly_a)])
        # b) TH - định lí côsin
        ly_b = r"$BC^{2} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot\cos %s$." % (_xx(b, 1), _xx(c, 1), _xx(b, 1), _xx(c, 1), _goc(g))
        y2 = _tf_gop(_tf_so(r"$BC \approx %s$ hải lí", d, 1, ly_b,
                            [(math.sqrt(b * b + c * c), "Quên số hạng chứa $\\cos$"),
                             (math.sqrt(b * b + c * c + 2 * b * c * _cos_d(g)), "Sai dấu"),
                             (math.sqrt(b * b + c * c - b * c * _cos_d(g)), "Quên hệ số 2")],
                            bdt=r"Sau $%s$ giờ, hai tàu cách nhau %s $%s$ hải lí" % (_xx(t, 1), "%s", "%s"), tu=("hơn", "chưa đến")))
        # c) VD - côsin góc tại B
        ly_c = ly_b + r" $\cos\widehat{ABC} = \dfrac{AB^{2} + BC^{2} - AC^{2}}{2\cdot AB\cdot BC}$."
        d_, s_ = _tf_so(r"$\cos\widehat{ABC} \approx %s$", cosB, 2, ly_c,
                        [(-cosB, "Sai dấu"), (cosC, "Nhầm sang góc $C$"), (2 * cosB, "Quên số 2 ở mẫu")], mien=(-1, 1))
        dung, sai = d_, s_
        (dung if cosB > 0 else sai).append((r"Góc $\widehat{ABC}$ là góc nhọn", ly_c))
        (sai if cosB > 0 else dung).append((r"Góc $\widehat{ABC}$ là góc tù", ly_c))
        y3 = _phat_bieu(dung, sai)
        # d) VDC - thời gian để hai tàu cách nhau D hải lí
        ly_d = (r"Sau $x$ giờ: $AB = %dx$, $AC = %dx$, $BC^{2} = x^{2}\left(%d + %d - 2\cdot %d\cdot %d\cdot\cos %s\right)$, nên "
                r"$BC = x\cdot %s$. Giải $x\cdot %s = %d$." % (v1, v2, v1 * v1, v2 * v2, v1, v2, _goc(g), _xx(k, 3), _xx(k, 3), D))
        y4 = _tf_gop(_tf_so(r"Hai tàu cách nhau $%d$ hải lí sau khoảng $%s$ giờ kể từ lúc xuất phát" % (D, "%s"), T, 1, ly_d,
                            [(D / (v1 + v2), "Cộng hai vận tốc như hai tàu đi ngược chiều"),
                             (D / math.sqrt(v1 * v1 + v2 * v2), "Quên số hạng chứa $\\cos$"),
                             (D / math.sqrt(v1 * v1 + v2 * v2 + 2 * v1 * v2 * _cos_d(g)), "Sai dấu")],
                            bdt=r"Hai tàu cách nhau $%d$ hải lí sau %s $%s$ giờ kể từ lúc xuất phát" % (D, "%s", "%s"), tu=("hơn", "chưa đến")))
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
    y = [(r"{\True %s}" % d, "Đúng. " + l) for d, l in dung_ds]
    da = set()
    for d, l in sai_ds:
        if d in noi_dung_dung or d in da:
            continue
        da.add(d)
        y.append((r"{%s}" % d, "Sai. " + l))
    return y


def _so_tf(v, n=2):
    """Giá trị đúng: dạng chính xác nếu gọn, không thì gần đúng n chữ số (kèm 'làm tròn')."""
    v = simplify(v)
    t = _gon(v)
    if len(t) <= 24:
        return "= " + t, None
    return r"\approx " + _x1(float(v), n), "(làm tròn đến hàng phần trăm)"


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
        loai = "tù" if tu else "nhọn"
        gi = int(round(g))
        if kieu == "goc":
            gia = r"$\alpha = %s$" % _goc(gi)
        elif kieu == "x":
            gia = r"điểm $M$ có hoành độ $x_0 = %s$" % _L(c)
        elif kieu == "y":
            gia = r"điểm $M$ có tung độ $y_0 = %s$ và góc $\alpha$ %s" % (_L(s), loai)
        elif kieu == "cos":
            gia = r"$\cos\alpha = %s$" % _L(c)
        elif kieu == "sin":
            gia = r"$\sin\alpha = %s$ và góc $\alpha$ %s" % (_L(s), loai)
        elif kieu == "tan":
            gia = r"$\tan\alpha = %s$" % _L(t)
        else:
            gia = r"$\cot\alpha = %s$" % _L(k)
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho điểm $M\left(x_0; y_0\right)$ thuộc nửa đường tròn đơn vị sao cho "
                 r"$\widehat{xOM} = \alpha$, các điểm $A\left(1; 0\right)$, $A'\left(-1; 0\right)$ (hình vẽ). Biết %s. "
                 r"Xét tính đúng, sai của các mệnh đề sau." % gia)
        dau = "<" if tu else ">"
        nguoc = ">" if tu else "<"

        # a) NB - lý thuyết
        DN = r"Theo định nghĩa: $\sin\alpha = y_0$, $\cos\alpha = x_0$, $\tan\alpha = \dfrac{y_0}{x_0}$, $\cot\alpha = \dfrac{x_0}{y_0}$."
        DAU = r"Góc $\alpha$ %s nên $\cos\alpha %s 0$, $\tan\alpha %s 0$, $\cot\alpha %s 0$; luôn có $\sin\alpha \ge 0$ với $0^{\circ} \le \alpha \le 180^{\circ}$." % (loai, dau, dau, dau)
        y1 = _phat_bieu(
            [(r"$\sin\alpha = y_0$", DN), (r"$\cos\alpha = x_0$", DN), (r"$\tan\alpha = \dfrac{y_0}{x_0}$", DN),
             (r"$\cot\alpha = \dfrac{x_0}{y_0}$", DN),
             (r"$x_0^{2} + y_0^{2} = 1$", r"$M$ thuộc đường tròn đơn vị nên $OM^{2} = x_0^{2} + y_0^{2} = 1$."),
             (r"$\cos\alpha %s 0$" % dau, DAU), (r"$\tan\alpha %s 0$" % dau, DAU), (r"$\sin\alpha > 0$", DAU),
             (r"$-1 \le \cos\alpha \le 1$", r"$\cos\alpha = x_0$ với $-1 \le x_0 \le 1$.")],
            [(r"$\sin\alpha = x_0$", DN), (r"$\cos\alpha = y_0$", DN), (r"$\tan\alpha = \dfrac{x_0}{y_0}$", DN),
             (r"$\cot\alpha = \dfrac{y_0}{x_0}$", DN),
             (r"$x_0 + y_0 = 1$", r"$M$ thuộc đường tròn đơn vị nên $x_0^{2} + y_0^{2} = 1$, không phải $x_0 + y_0 = 1$."),
             (r"$\cos\alpha %s 0$" % nguoc, DAU), (r"$\tan\alpha %s 0$" % nguoc, DAU), (r"$\sin\alpha < 0$", DAU),
             (r"$\tan\alpha\cdot\cot\alpha = -1$", r"$\tan\alpha\cdot\cot\alpha = \dfrac{y_0}{x_0}\cdot\dfrac{x_0}{y_0} = 1$.")])

        # b) TH - một bước
        if kieu == "goc":
            ly = r"Bảng giá trị lượng giác: $\sin %s = %s$, $\cos %s = %s$, nên $M\left(%s; %s\right)$." % (
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
                dung.append((r"$\sin\left(180^{\circ} - \alpha\right) = %s$" % _L(v), ly + r" Hai góc bù nhau có sin bằng nhau."))
            else:
                dung.append((r"$\cos\left(180^{\circ} - \alpha\right) = %s$" % _L(-v), ly + r" Hai góc bù nhau có côsin đối nhau."))
            sai = [(r"$\%s\alpha = %s$" % (khac, _L(v)), ly), (r"$\%s\alpha = %s$" % (ham, _L(-v)), ly),
                   (r"$\%s\alpha = %s$" % (ham, _L(1 - v)), ly), (r"$\%s^{2}\alpha = %s$" % (ham, _L(1 - v ** 2)), ly)]
        elif kieu == "cos":
            ly = r"$\sin^{2}\alpha = 1 - \cos^{2}\alpha = %s$, mà $\sin\alpha \ge 0$ nên $\sin\alpha = %s$." % (_L(s ** 2), _L(s))
            dung = [(r"$\sin\alpha = %s$" % _L(s), ly), (r"$\sin^{2}\alpha = %s$" % _L(s ** 2), ly)]
            sai = [(r"$\sin\alpha = %s$" % _L(-s), ly), (r"$\sin\alpha = %s$" % _L(1 - c), ly), (r"$\sin^{2}\alpha = %s$" % _L(1 + c ** 2), ly)]
        elif kieu == "sin":
            ly = r"$\cos^{2}\alpha = 1 - \sin^{2}\alpha = %s$, góc $\alpha$ %s nên $\cos\alpha = %s$." % (_L(c ** 2), loai, _L(c))
            dung = [(r"$\cos\alpha = %s$" % _L(c), ly), (r"$\cos^{2}\alpha = %s$" % _L(c ** 2), ly)]
            sai = [(r"$\cos\alpha = %s$" % _L(-c), ly), (r"$\cos\alpha = %s$" % _L(1 - s), ly), (r"$\cos^{2}\alpha = %s$" % _L(1 + s ** 2), ly)]
        elif kieu == "tan":
            ly = r"$\cot\alpha = \dfrac{1}{\tan\alpha} = %s$." % _L(k)
            dung = [(r"$\cot\alpha = %s$" % _L(k), ly), (r"$\tan\alpha\cdot\cot\alpha = 1$", ly)]
            sai = [(r"$\cot\alpha = %s$" % _L(-k), ly), (r"$\cot\alpha = %s$" % _L(t), ly), (r"$\cot\alpha = %s$" % _L(-t), ly),
                   (r"$\tan\alpha\cdot\cot\alpha = -1$", ly + r" Luôn có $\tan\alpha\cdot\cot\alpha = 1$.")]
        else:
            ly = r"$\tan\alpha = \dfrac{1}{\cot\alpha} = %s$." % _L(t)
            dung = [(r"$\tan\alpha = %s$" % _L(t), ly), (r"$\tan\alpha\cdot\cot\alpha = 1$", ly)]
            sai = [(r"$\tan\alpha = %s$" % _L(-t), ly), (r"$\tan\alpha = %s$" % _L(k), ly), (r"$\tan\alpha = %s$" % _L(-k), ly),
                   (r"$\tan\alpha\cdot\cot\alpha = -1$", ly + r" Luôn có $\tan\alpha\cdot\cot\alpha = 1$.")]
        y2 = _phat_bieu(dung, sai)

        # c) VD - biểu thức đơn giản (nhiều dạng)
        nen = r"Ta có $\sin\alpha = %s$, $\cos\alpha = %s$, $\tan\alpha = %s$, $\cot\alpha = %s$" % (_L(s), _L(c), _L(t), _L(k))
        if kieu in ("tan", "cot"):
            nen += r" (từ $1 + \tan^{2}\alpha = \dfrac{1}{\cos^{2}\alpha}$ và dấu của $\cos\alpha$)"
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
        for bt, P, Ps in random.sample(BT, 3):
            if P is None:
                continue
            P = simplify(P)
            ly = nen + r", nên $P = %s = %s$." % (bt, _gon(P))
            dung.append((r"$P = %s = %s$" % (bt, _gon(P)), ly))
            for Q in Ps:
                if Q is not None and simplify(Q - P) != 0:
                    sai.append((r"$P = %s = %s$" % (bt, _gon(simplify(Q))), ly))
        y3 = _phat_bieu(dung, sai)

        # d) VDC - giải tam giác OAM / OA'M / AMA'
        cf, sf = float(c), float(s)
        AM, AM_ = math.sqrt(2 - 2 * cf), math.sqrt(2 + 2 * cf)            # AM, A'M
        S_OAM, S_AMA = sf / 2, sf                                         # diện tích
        nen_d = (r"Tam giác $OAM$ có $OA = OM = 1$, $\widehat{AOM} = \alpha$; theo định lí côsin "
                 r"$AM^{2} = 1 + 1 - 2\cos\alpha = 2 - 2\cdot\left(%s\right)$, nên $AM \approx %s$. "
                 r"Tương tự trong tam giác $OA'M$ ($\widehat{A'OM} = 180^{\circ} - \alpha$): "
                 r"$A'M^{2} = 2 + 2\cos\alpha$, $A'M \approx %s$." % (_L(c), _x1(AM, 3), _x1(AM_, 3)))
        DL = [
            (r"Chu vi tam giác $AMA'$", 2 + AM + AM_, nen_d + r" Chu vi tam giác $AMA'$ là $2 + AM + A'M$.", [AM + AM_, 1 + AM + AM_]),
            (r"Bán kính đường tròn nội tiếp tam giác $AMA'$", S_AMA / ((2 + AM + AM_) / 2),
             nen_d + r" $S_{AMA'} = \dfrac{1}{2}\cdot AA'\cdot y_0 = %s$, nửa chu vi $p = \dfrac{2 + AM + A'M}{2}$, "
                     r"$r = \dfrac{S}{p}$." % _L(s), [S_AMA / (2 + AM + AM_), S_AMA * 2 / (2 + AM + AM_) * 2]),
            (r"Đường cao kẻ từ $O$ của tam giác $OAM$", 2 * S_OAM / AM,
             nen_d + r" $S_{OAM} = \dfrac{1}{2}\cdot OA\cdot OM\cdot\sin\alpha = %s$, đường cao $h = \dfrac{2S_{OAM}}{AM}$." % _L(s / 2),
             [S_OAM / AM, AM / 2 + 0.1]),
            (r"Đường cao kẻ từ $O$ của tam giác $OA'M$", 2 * (sf / 2) / AM_,
             nen_d + r" $S_{OA'M} = \dfrac{1}{2}\sin\left(180^{\circ} - \alpha\right) = %s$, đường cao $h = \dfrac{2S_{OA'M}}{A'M}$." % _L(s / 2),
             [(sf / 2) / AM_, AM_ / 2 + 0.1]),
            (r"Bán kính đường tròn ngoại tiếp tam giác $OAM$", AM / (2 * sf),
             nen_d + r" Theo định lí sin trong tam giác $OAM$: $\dfrac{AM}{\sin\widehat{AOM}} = 2R$, nên $R = \dfrac{AM}{2\sin\alpha}$.",
             [AM / sf, AM * sf / 2]),
            (r"Độ dài $AM$", AM, nen_d, [AM_, 2 - 2 * cf]),
            (r"Độ dài $A'M$", AM_, nen_d, [AM, 2 + 2 * cf]),
        ]
        dung, sai = [], []
        for ten, v, ly, vs in random.sample(DL, len(DL)):
            if not _xa_bien(v * 100):
                continue
            if len(dung) == 3:
                break
            dung.append((r"%s xấp xỉ $%s$ (làm tròn đến hàng phần trăm)" % (ten, _x1(v, 2)), ly + r" Vậy giá trị $\approx %s$." % _x1(v, 3)))
            for w in vs:
                if _x1(w, 2) != _x1(v, 2) and w > 0:
                    sai.append((r"%s xấp xỉ $%s$ (làm tròn đến hàng phần trăm)" % (ten, _x1(w, 2)),
                                ly + r" Vậy giá trị $\approx %s$." % _x1(v, 3)))
        if not dung or not sai:
            continue
        y4 = _phat_bieu(dung, sai)
        so += 1
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
        debai = r"Giá trị nào sau đây bằng $%s$?" % _L(v)
        giai = (r"Tra bảng giá trị lượng giác của các góc đặc biệt: $\%s %s = %s$." % (h, _goc(d), _L(v))
                + "\\\\\n" + r"Ba giá trị còn lại: " +
                ", ".join(r"$\%s %s = %s$" % (h2, _goc(d2), _L(_gtlg(h2, d2))) for h2, d2 in chon) + ".")
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_NB029_SA_B_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi NGƯỢC của _01: biết hoành độ (hoặc tung độ và phía
    của trục tung) của điểm $M$ trên nửa đường tròn đơn vị, tìm số đo góc
    $\widehat{xOM}$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB029_SA_B (_01: biet goc, tinh
    bieu thuc toa do; _02: biet toa do, tim goc). Dap so la so nguyen do.
    Co Lan duyet lai.
    """
    BO = [("x", Rational(1, 2), None, 60), ("x", Rational(-1, 2), None, 120),
          ("x", Integer(0), None, 90), ("x", Integer(-1), None, 180),
          ("y", Rational(1, 2), "phải", 30), ("y", Rational(1, 2), "trái", 150),
          ("y", Integer(1), None, 90)]
    ds = list(range(len(BO)))
    random.shuffle(ds)
    ds = (ds * (socau // len(ds) + 1))[:socau]
    cau = ""
    for i in ds:
        loai, v, phia, goc = BO[i]
        so = _so_thap_phan_gon(v)
        if loai == "x":
            cho = r"có hoành độ bằng $%s$" % so
            ly = (r"Với $M$ thuộc nửa đường tròn đơn vị thì $\cos\widehat{xOM} = x_M = %s$." % so
                  + "\\\\\n" + r"Góc từ $0^{\circ}$ đến $180^{\circ}$ có côsin bằng $%s$ là $%s$." % (so, _goc(goc)))
        else:
            cho = (r"có tung độ bằng $%s$" % so) + (r" và nằm bên %s trục tung" % phia if phia else "")
            ly = (r"Với $M$ thuộc nửa đường tròn đơn vị thì $\sin\widehat{xOM} = y_M = %s$." % so
                  + "\\\\\n" +
                  (r"Có hai góc có sin bằng $%s$ là $30^{\circ}$ và $150^{\circ}$; $M$ nằm bên %s trục "
                   r"tung nên $\widehat{xOM}$ là góc %s, tức $\widehat{xOM} = %s$."
                   % (so, phia, "nhọn" if phia == "phải" else "tù", _goc(goc)) if phia else
                   r"Góc có sin bằng $1$ là $90^{\circ}$."))
        debai = (r"Trên mặt phẳng toạ độ $Oxy$, điểm $M$ thuộc nửa đường tròn đơn vị %s. "
                 r"Số đo của góc $\widehat{xOM}$ bằng bao nhiêu độ?" % cho)
        dap = str(goc)
        nhieu = _ba_nhieu(dap, [str(180 - goc), str(abs(90 - goc)), str(goc + 30)],
                          buoc=lambda t: str(goc + 15 * t))
        cau += MC_SA_answer_const(debai, dap, nhieu, ly + "\\\\\n" + r"Vậy $\widehat{xOM} = %s$." % _goc(goc),
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
        nhieu = _ba_nhieu(dung, [_L(x) for x in ung], buoc=lambda t: _L(P + Rational(t, 25)))
        debai = (r"Cho góc $\alpha$ $\left(0^{\circ} \le \alpha \le 180^{\circ}\right)$ thoả mãn "
                 r"$\sin\alpha\cos\alpha = %s$. Giá trị của $%s$ bằng" % (_L(p), hoi))
        giai = (r"Ta có $%s = %s$." % (hoi, bd) + "\\\\\n" +
                r"Thay $\sin\alpha\cos\alpha = %s$ được $%s = %s = %s$." % (_L(p), hoi, thay, dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH030_SA_B_02(socau, dang=2):
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
        phia = "trái" if dau < 0 else "phải"
        goc = math.degrees(math.acos(float(cs)))
        debai = (r"Trên mặt phẳng toạ độ $Oxy$ cho điểm $A\left(1; 0\right)$ và điểm $M$ thuộc nửa đường "
                 r"tròn đơn vị, nằm bên %s trục tung, sao cho tam giác $AOM$ có diện tích bằng $%s$. "
                 r"Tính $\cos\widehat{xOM}$." % (phia, _so_thap_phan_gon(S)))
        giai = (r"$S_{\triangle AOM} = \dfrac{1}{2}\cdot OA\cdot y_M = \dfrac{1}{2}y_M$ nên "
                r"$y_M = 2\cdot %s = %s$, tức $\sin\widehat{xOM} = %s$."
                % (_so_thap_phan_gon(S), _so_thap_phan_gon(sn), _so_thap_phan_gon(sn)) + "\\\\\n" +
                r"$\cos^{2}\widehat{xOM} = 1 - \sin^{2}\widehat{xOM} = %s$." % _so_thap_phan_gon(cs ** 2)
                + "\\\\\n" +
                r"$M$ nằm bên %s trục tung nên $x_M %s 0$. Vậy $\cos\widehat{xOM} = %s$."
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
                qh = (r"$%s$ và $%s$ phụ nhau nên $\sin %s = \cos %s$, $\cos %s = \sin %s$, $\tan %s = \cot %s$"
                      % (_goc(a), _goc(90 - a), _goc(90 - a), _goc(a), _goc(90 - a), _goc(a),
                         _goc(90 - a), _goc(a)))
            else:
                qh = (r"$%s$ và $%s$ bù nhau nên $\sin %s = \sin %s$, $\cos %s = -\cos %s$, $\tan %s = -\tan %s$"
                      % (_goc(a), _goc(180 - a), _goc(180 - a), _goc(a), _goc(180 - a), _goc(a),
                         _goc(180 - a), _goc(a)))
            ly.append(qh + r"; do đó $%s = %s$." % (dien(mau, a), dien(bd, a)))
        tinh = ("%d\\cdot %s" % (k1, _ngoac(Integer(_BT_GOC_LE[i][1])))) if k1 != 1 else str(_BT_GOC_LE[i][1])
        tinh += " %s %s" % ("-" if k2 < 0 else "+",
                            ("%d\\cdot %s" % (abs(k2), _ngoac(Integer(_BT_GOC_LE[j][1]))))
                            if abs(k2) != 1 else str(_BT_GOC_LE[j][1]))
        dung = "$P = %d$" % P
        nhieu = _ba_nhieu(dung, ["$P = %d$" % x for x in (P + 1, P - 1, -P, 0, 2 * P)],
                          buoc=lambda t: "$P = %d$" % (P + t + 1))
        debai = r"Tính giá trị biểu thức $P = %s$." % bt
        giai = ("\\\\\n".join(ly) + "\\\\\n" + r"Vậy $P = %s = %d$." % (tinh, P))
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
        debai = r"Cho tam giác $ABC$. Tính giá trị của biểu thức $P = %s$." % bt
        giai = (r"Vì $\widehat{A} + \widehat{B} + \widehat{C} = 180^{\circ}$ nên $%s = 180^{\circ} - %s$: "
                r"hai góc bù nhau, do đó $\sin\left(%s\right) = \sin %s$, $\cos\left(%s\right) = -\cos %s$."
                % (yz, X, yz, X, yz, X) + "\\\\\n" + "\\\\\n".join(dong) + "\\\\\n" +
                r"Vậy $P = %s = %d$." % (tinh, P))
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
            ly = (r"Hai góc $%s$ và $%s$ phụ nhau nên $\%s %s = \%s %s$."
                  % (_goc(a), _goc(b), g, _goc(b), h, _goc(a)))
        else:
            b, g = 180 - a, h
            ket = v if h == "sin" else -v
            ly = (r"Hai góc $%s$ và $%s$ bù nhau nên $\%s %s = %s\%s %s$."
                  % (_goc(a), _goc(b), g, _goc(b), "" if h == "sin" else "-", h, _goc(a)))
        dung = so(ket)
        nhieu = _ba_nhieu(dung, [so(-ket), so(w), so(-w)], buoc=lambda t: so(ket + 0.1 * t))
        debai = (r"Biết $\%s %s \approx %s$. Giá trị của $\%s %s$ xấp xỉ bằng"
                 % (h, _goc(a), so(v), g, _goc(b)))
        giai = ly + "\\\\\n" + r"Vậy $\%s %s \approx %s$." % (g, _goc(b), dung)
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
        debai = r"Cho góc nhọn $\alpha$. Rút gọn biểu thức $P = %s$ ta được" % bt
        giai = (r"Dùng quan hệ hai góc bù nhau, phụ nhau: $\sin\left(180^{\circ} - \alpha\right) = \sin\alpha$, "
                r"$\cos\left(180^{\circ} - \alpha\right) = -\cos\alpha$, $\tan\left(180^{\circ} - \alpha\right) = "
                r"-\tan\alpha$; $\sin\left(90^{\circ} - \alpha\right) = \cos\alpha$, $\cos\left(90^{\circ} - "
                r"\alpha\right) = \sin\alpha$, $\cot\left(90^{\circ} - \alpha\right) = \tan\alpha$." + "\\\\\n" +
                r"Do đó $P = %s$." % bd)
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
        debai = (r"Tam giác $ABC$ vuông tại $%s$ có $\%s %s = %s$. Giá trị của $\%s %s$ bằng"
                 % (X, cho, Y, _L(cho_gt), hoi, Z))
        buoc = []
        if hoi == "tan" or (hoi == "sin" and cho == "sin") or (hoi == "cos" and cho == "cos"):
            buoc.append(r"$\widehat{%s}$ nhọn nên $\%s %s = \sqrt{1 - %s} = %s$."
                        % (Y, "cos" if cho == "sin" else "sin", Y, _L(cho_gt ** 2), _L(con)))
        qh = {"sin": r"\sin %s = \cos %s" % (Z, Y), "cos": r"\cos %s = \sin %s" % (Z, Y),
              "tan": r"\tan %s = \cot %s = \dfrac{\cos %s}{\sin %s}" % (Z, Y, Y, Y)}[hoi]
        giai = (r"Hai góc nhọn $\widehat{%s}$ và $\widehat{%s}$ của tam giác vuông phụ nhau." % (Y, Z)
                + ("\\\\\n" + buoc[0] if buoc else "") + "\\\\\n" +
                r"Do đó $%s = %s$." % (qh, dung))
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
        debai = (r"Cho tam giác $ABC$ có $\widehat{%s} = %s$. Xét tính đúng sai của các khẳng định sau:"
                 % (X, _goc(x)))
        # a) NB - bảng giá trị lượng giác
        ly_a = r"Bảng giá trị lượng giác: $\sin %s = %s$, $\cos %s = %s$, $\tan %s = %s$." % (_goc(x), _L(s), _goc(x), _L(c), _goc(x), _L(t))
        y1 = _tf_gop(_tf_ct(r"$\cos %s = %s$" % (X, "%s"), c, ly_a, [(-c, "Sai dấu"), (s, "Nhầm $\\sin$ với $\\cos$")]),
                     _tf_ct(r"$\sin %s = %s$" % (X, "%s"), s, ly_a, [(abs(c), "Nhầm $\\sin$ với $\\cos$"), (-s, "Sai dấu")]),
                     _tf_ct(r"$\tan %s = %s$" % (X, "%s"), t, ly_a, [(-t, "Sai dấu"), (1 / t, "Nhầm $\\tan$ với $\\cot$")]))
        ly = (r"$%s = 180^{\circ} - %s = %s$" % (yz, _goc(x), _goc(180 - x)))
        # b) TH - một bước: góc bù có sin bằng nhau
        ly_b = r"%s nên $\sin\left(%s\right) = \sin %s = %s$." % (ly, yz, _goc(x), _L(s))
        sai_b = [(r"$\sin\left(%s\right) = %s$" % (yz, _L(-s)), ly_b), (r"$\sin\left(%s\right) = %s$" % (yz, _L(c)), "Nhầm góc phụ. " + ly_b)]
        if 90 - x > 0:
            sai_b.append((r"$\widehat{%s} + \widehat{%s} = %s$" % (tuple(sorted([Y, Z])) + (_goc(90 - x),)), ly_b))
        sai_b.append((r"$\widehat{%s} + \widehat{%s} = %s$" % (tuple(sorted([Y, Z])) + (_goc(x),)), ly_b))
        y2 = _phat_bieu(
            [(r"$\sin\left(%s\right) = %s$" % (yz, _L(s)), ly_b), (r"$\widehat{%s} + \widehat{%s} = %s$" % (tuple(sorted([Y, Z])) + (_goc(180 - x),)), ly_b)],
            sai_b)
        # c) VD - côsin, tang của góc bù
        ly_c = r"%s nên $\cos\left(%s\right) = -\cos %s = %s$, $\tan\left(%s\right) = -\tan %s = %s$." % (ly, yz, _goc(x), _L(-c), yz, _goc(x), _L(-t))
        y3 = _tf_gop(_tf_ct(r"$\cos\left(%s\right) = %s$" % (yz, "%s"), -c, ly_c, [(c, "Quên đổi dấu"), (-s, "Nhầm $\\sin$ với $\\cos$")]),
                     _tf_ct(r"$\tan\left(%s\right) = %s$" % (yz, "%s"), -t, ly_c, [(t, "Quên đổi dấu"), (-1 / t, "Nhầm $\\tan$ với $\\cot$")]))
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
            ly_d = (r"%s nên $\cos\left(%s\right) = -\cos %s$, $\tan\left(%s\right) = -\tan %s$; thay $\sin %s = %s$, $\cos %s = %s$, "
                    r"$\tan %s = %s$ được $%s$." % (ly, yz, X, yz, X, X, _L(s), X, _L(c), X, _L(t), _tri(P)))
            dung.append(("$" + bt + " = %s$" % _tri(P), ly_d))
            for Q, ghi in ((u * s + v * c - w * t, "Quên đổi dấu $\\cos$"), (u * s - v * c + w * t, "Quên đổi dấu $\\tan$"),
                           (u * s + v * c + w * t, "Quên đổi dấu cả hai")):
                if simplify(Q - P) != 0:
                    sai.append(("$" + bt + " = %s$" % _tri(Q), ghi + ". " + ly_d))
        y4 = _phat_bieu(dung, sai)
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
        debai = (r"Tam giác $ABC$ có $AB = %d$, $BC = %d$, $CA = %d$. Số đo góc $\widehat{A}$ bằng"
                 % (c, a, b))
        giai = (r"Theo hệ quả của định lí côsin: $\cos A = \dfrac{AB^{2} + AC^{2} - BC^{2}}{2\cdot AB\cdot AC}"
                r" = \dfrac{%d^{2} + %d^{2} - %d^{2}}{2\cdot %d\cdot %d} = %s$." % (c, b, a, c, b, _L(cosA))
                + "\\\\\n" + r"Do đó $\widehat{A} = %s$." % _goc(A))
        dung = _goc(A)
        nhieu = _ba_nhieu(dung, [_goc(x) for x in (180 - A, 90, 30, 45, 150, 60)])
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


_CT_COSIN_DUNG = [r"a^{2} = b^{2} + c^{2} - 2bc\cos A", r"\cos A = \dfrac{b^{2} + c^{2} - a^{2}}{2bc}",
                  r"b^{2} = a^{2} + c^{2} - 2ac\cos B", r"\cos B = \dfrac{a^{2} + c^{2} - b^{2}}{2ac}",
                  r"c^{2} = a^{2} + b^{2} - 2ab\cos C", r"\cos C = \dfrac{a^{2} + b^{2} - c^{2}}{2ab}"]
_CT_COSIN_SAI = [(r"a^{2} = b^{2} + c^{2} + 2bc\cos A", r"phải là dấu trừ trước $2bc\cos A$"),
                 (r"\cos A = \dfrac{b^{2} + c^{2} - a^{2}}{bc}", r"mẫu số phải là $2bc$"),
                 (r"\cos A = \dfrac{a^{2} + b^{2} - c^{2}}{2bc}", r"cạnh đối diện góc $A$ là $a$, phải trừ $a^{2}$"),
                 (r"b^{2} = a^{2} + c^{2} - 2ac\cos A", r"góc xen giữa hai cạnh $a$, $c$ là góc $B$"),
                 (r"\cos C = \dfrac{a^{2} + b^{2} + c^{2}}{2ab}", r"phải trừ $c^{2}$"),
                 (r"\cos B = \dfrac{b^{2} + c^{2} - a^{2}}{2ac}", r"đúng phải là $\dfrac{a^{2} + c^{2} - b^{2}}{2ac}$"),
                 (r"c^{2} = a^{2} + b^{2} - ab\cos C", r"thiếu hệ số $2$")]


def L10_C3_B6_TH032_MC_E_01(socau, dang=1):
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
            giai = (r"%s là hệ thức đúng (định lí côsin và hệ quả). Các hệ thức còn lại sai: " % dung
                    + "; ".join(r"$%s$: %s" % x for x in ba) + ".")
        else:
            sai, ly = random.choice(_CT_COSIN_SAI)
            dung = "$%s$" % sai
            nhieu = ["$%s$" % x for x in random.sample(_CT_COSIN_DUNG, 3)]
            giai = r"Hệ thức %s sai vì %s. Ba hệ thức còn lại là định lí côsin và hệ quả." % (dung, ly)
        debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$. Hệ thức nào dưới đây \textbf{%s}?"
                 % ("đúng" if hoi_dung else "sai"))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH032_MC_E_02(socau, dang=1):
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
        debai = (r"Cho tam giác $ABC$ có $AB = %d$, $BC = %d$, $CA = %d$. Giá trị của $\cos %s$ được tính "
                 r"bởi biểu thức nào sau đây?" % (AB, BC, CA, dinh))
        v = Rational(k1 * k1 + k2 * k2 - d * d, 2 * k1 * k2)
        giai = (r"Hai cạnh kề góc $%s$ có độ dài $%d$ và $%d$, cạnh đối diện có độ dài $%d$. Theo hệ quả "
                r"của định lí côsin: $\cos %s = %s = %s$." % (dinh, k1, k2, d, dinh, bt(k1, k2, d), _L(v)))
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
        debai = (r"Tam giác $ABC$ có $\widehat{A} = %s$, $\widehat{B} = %s$, $AC = %d$. Tính độ dài cạnh $AB$."
                 % (_goc(A), _goc(B), b))
        giai = (r"$\widehat{C} = 180^{\circ} - \left(%s + %s\right) = %s$." % (_goc(A), _goc(B), _goc(C))
                + "\\\\\n" +
                r"Theo định lí sin: $\dfrac{AB}{\sin C} = \dfrac{AC}{\sin B}$ nên $AB = \dfrac{AC\cdot\sin C}{\sin B}"
                r" = \dfrac{%d\cdot\sin %s}{\sin %s} = %s$." % (b, _goc(C), _goc(B), dung))
        cau += MC_SA_answer_const(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


_CT_SIN_DUNG = [r"\dfrac{a}{\sin A} = 2R", r"\sin A = \dfrac{a}{2R}", r"b = 2R\sin B",
                r"\sin C = \dfrac{c\sin A}{a}", r"\dfrac{b}{\sin B} = \dfrac{c}{\sin C}",
                r"a\sin B = b\sin A"]
_CT_SIN_SAI = [(r"b\sin B = 2R", r"đúng phải là $\dfrac{b}{\sin B} = 2R$"),
               (r"a = R\sin A", r"đúng phải là $a = 2R\sin A$"),
               (r"\sin A = \dfrac{a}{R}", r"đúng phải là $\sin A = \dfrac{a}{2R}$"),
               (r"a\sin A = b\sin B", r"đúng phải là $a\sin B = b\sin A$"),
               (r"\dfrac{a}{\sin B} = \dfrac{b}{\sin A}", r"mỗi cạnh phải chia cho sin của góc ĐỐI DIỆN nó"),
               (r"c = 2R\cos C", r"đúng phải là $c = 2R\sin C$")]


def L10_C3_B6_TH033_MC_C_01(socau, dang=1):
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
            giai = (r"Định lí sin: $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$, suy ra %s. "
                    % dung + r"Các khẳng định còn lại sai: " + "; ".join(r"$%s$: %s" % x for x in ba) + ".")
        else:
            sai, ly = random.choice(_CT_SIN_SAI)
            dung = "$%s$" % sai
            nhieu = ["$%s$" % x for x in random.sample(_CT_SIN_DUNG, 3)]
            giai = (r"Định lí sin: $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$. "
                    r"Khẳng định %s sai vì %s." % (dung, ly))
        debai = (r"Trong tam giác $ABC$ bất kì với $BC = a$, $CA = b$, $AB = c$ và $R$ là bán kính đường tròn "
                 r"ngoại tiếp. Khẳng định nào sau đây là \textbf{%s}?" % ("đúng" if hoi_dung else "sai"))
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH033_MC_C_02(socau, dang=1):
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
        debai = (r"Tam giác $ABC$ có $\widehat{A} = %s$, $\widehat{B} = %s$. Tỉ số $\dfrac{BC}{CA}$ bằng"
                 % (_goc(A), _goc(B)))
        giai = (r"Theo định lí sin: $\dfrac{BC}{\sin A} = \dfrac{CA}{\sin B}$ nên $\dfrac{BC}{CA} = "
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
        debai = (r"Tam giác $ABC$ có $AB = %d$, $AC = %d$, $\widehat{BAC} = %s$. Tính diện tích $S$ của tam "
                 r"giác $ABC$." % (c, b, _goc(A)))
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
        debai = (r"Tam giác $ABC$ có $AB = %d$, $AC = %d$ và $\cos A = %s$. Diện tích tam giác $ABC$ bằng"
                 % (c, b, _L(cA)))
        giai = (r"Vì $0^{\circ} < A < 180^{\circ}$ nên $\sin A > 0$, do đó $\sin A = \sqrt{1 - \cos^{2}A} = "
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
        debai = (r"Cho tam giác $ABC$ có $a = %d$, $b = %d$, $c = %d$. Tính bán kính $r$ của đường tròn nội "
                 r"tiếp tam giác $ABC$." % (a, b, c))
        giai = (r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d$." % (a, b, c, p) + "\\\\\n" +
                r"Công thức Heron: $S = \sqrt{%d\left(%d - %d\right)\left(%d - %d\right)\left(%d - %d\right)} = %d$."
                % (p, p, a, p, b, p, c, S) + "\\\\\n" +
                r"Vậy $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %s$." % (S, p, _L(r)))
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
        debai = (r"Cho tam giác $ABC$ có $a = %d$, $b = %d$, $c = %d$. Tính bán kính $R$ của đường tròn ngoại "
                 r"tiếp tam giác $ABC$." % (a, b, c))
        giai = (r"Nửa chu vi $p = %d$, công thức Heron: $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
                % (p, p, p - a, p - b, p - c, S) + "\\\\\n" +
                r"Từ $S = \dfrac{abc}{4R}$ suy ra $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$."
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
        debai = (r"Tam giác $ABC$ có $AB = %d$, $AC = %d$, $\widehat{BAC} = %s$. Tính độ dài đường cao $h_a$ "
                 r"kẻ từ $A$ của tam giác." % (c, b, _goc(A)))
        giai = (r"Định lí côsin: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cos A = %d + %d - 2\cdot %d\cdot %d"
                r"\cdot %s = %d$ nên $BC = %d$." % (c * c, b * b, c, b, _ngoac(cA), a * a, a) + "\\\\\n" +
                r"$S = \dfrac{1}{2}\cdot AB\cdot AC\cdot\sin A = %s$." % _tri(S) + "\\\\\n" +
                r"$S = \dfrac{1}{2}BC\cdot h_a$ nên $h_a = \dfrac{2S}{BC} = %s$." % _tri(ha))
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
        debai = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$. Độ dài đường cao $h_a$ kẻ từ $A$ bằng"
                 % (a, b, c))
        giai = (r"Nửa chu vi $p = %d$, công thức Heron: $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
                % (p, p, p - a, p - b, p - c, S) + "\\\\\n" +
                r"$S = \dfrac{1}{2}BC\cdot h_a$ nên $h_a = \dfrac{2S}{BC} = \dfrac{2\cdot %d}{%d} = %s$."
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
        "\\fill (C) circle (1.5pt) node[above] {$C$ (vệ tinh)};\n"
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
    TRAM = [("Cần Thơ", "Thành phố Hồ Chí Minh"), ("Hà Nội", "Hải Phòng"), ("Huế", "Đà Nẵng")]
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
        debai = (r"Một vệ tinh $C$ bay phía trên hai trạm quan sát $A$ (ở %s) và $B$ (ở %s). Khi vệ tinh nằm "
                 r"giữa hai trạm, góc nâng của nó quan sát đồng thời là $%d^{\circ}$ tại $A$ và $%d^{\circ}$ tại $B$. "
                 r"Biết khoảng cách giữa hai trạm là $%d$ km. Khi đó vệ tinh cách trạm ở %s bao xa (làm tròn "
                 r"đến hàng đơn vị)?" % (ta, tb, al, be, d, tram))
        canh, goc_doi = ("AC", "B") if hoi_A else ("BC", "A")
        giai = (r"$\widehat{C} = 180^{\circ} - \left(%d^{\circ} + %d^{\circ}\right) = %d^{\circ}$." % (al, be, C)
                + "\\\\\n" +
                r"Định lí sin trong tam giác $ABC$: $%s = \dfrac{AB\cdot\sin %s}{\sin C} = \dfrac{%d\cdot\sin %d^{\circ}}"
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
        debai = (r"Hai tàu đánh cá cùng xuất phát từ bến $A$ và đi thẳng đều về hai vùng biển khác nhau, theo "
                 r"hai hướng tạo với nhau góc $%d^{\circ}$. Tàu thứ nhất đi với tốc độ $%d$ hải lí một giờ, tàu "
                 r"thứ hai đi với tốc độ $%d$ hải lí một giờ. Sau $%s$ giờ thì khoảng cách giữa hai tàu là bao "
                 r"nhiêu hải lí (làm tròn kết quả đến hàng phần mười)?" % (g, v1, v2, _xx(t, 1)))
        giai = (r"Sau $%s$ giờ tàu thứ nhất ở $B$, tàu thứ hai ở $C$ với $AB = %s\cdot %d = %s$, $AC = %s\cdot %d = %s$ "
                r"(hải lí)." % (_xx(t, 1), _xx(t, 1), v1, _xx(b, 1), _xx(t, 1), v2, _xx(c, 1)) + "\\\\\n" +
                r"Định lí côsin: $BC^{2} = AB^{2} + AC^{2} - 2\cdot AB\cdot AC\cdot\cos %d^{\circ} \approx %s$." % (g, _xx(d2, 2))
                + "\\\\\n" + r"Suy ra $BC \approx %s$ hải lí." % dap)
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
        debai = (r"Hai tàu cùng xuất phát từ cảng $A$, đi thẳng theo hai hướng tạo với nhau góc $%d^{\circ}$ với "
                 r"tốc độ lần lượt là $%d$ hải lí một giờ và $%d$ hải lí một giờ. Sau bao nhiêu giờ thì hai tàu "
                 r"cách nhau $%d$ hải lí (làm tròn kết quả đến hàng phần mười)?" % (g, v1, v2, D))
        giai = (r"Sau $t$ giờ: $AB = %dt$, $AC = %dt$. Định lí côsin:" % (v1, v2) + "\\\\\n" +
                r"$BC^{2} = \left(%dt\right)^{2} + \left(%dt\right)^{2} - 2\cdot %dt\cdot %dt\cdot\cos %d^{\circ}"
                r" \approx %s\,t^{2}$." % (v1, v2, v1, v2, g, _xx(k2, 2)) + "\\\\\n" +
                r"$BC = %d$ nên $t^{2} \approx \dfrac{%d^{2}}{%s}$, $t \approx %s$ (giờ)." % (D, D, _xx(k2, 2), dap))
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
        debai = (r"Một người đi dọc bờ biển từ vị trí $A$ đến vị trí $B$ và quan sát một ngọn hải đăng $C$. Góc "
                 r"nghiêng của phương quan sát từ các vị trí $A$, $B$ tới ngọn hải đăng với đường đi của người "
                 r"quan sát là $%d^{\circ}$ và $%d^{\circ}$ (như hình vẽ). Biết khoảng cách giữa hai vị trí $A$, $B$ là "
                 r"$%d$ m. Ngọn hải đăng cách bờ biển bao nhiêu mét (làm tròn kết quả đến hàng đơn vị)?"
                 % (al, be, d))
        giai = (r"Trong tam giác $ABC$: $\widehat{ABC} = 180^{\circ} - %d^{\circ} = %d^{\circ}$, "
                r"$\widehat{ACB} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$."
                % (be, 180 - be, al, 180 - be, be - al) + "\\\\\n" +
                r"Định lí sin: $BC = \dfrac{AB\cdot\sin A}{\sin C} = \dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} "
                r"\approx %s$ (m)." % (d, al, be - al, _xx(BC, 2)) + "\\\\\n" +
                r"Kẻ $CH \perp AB$. Tam giác $BCH$ vuông tại $H$: $CH = BC\cdot\sin %d^{\circ} \approx %d$ (m)."
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
        debai = (r"Từ vị trí $A$ người ta quan sát một cây cao $BC$ ($B$ là gốc cây) như hình vẽ. Biết $AH = %s$ m, "
                 r"$HB = %d$ m, $\widehat{BAC} = %d^{\circ}$. Tính chiều cao của cây (đơn vị mét, làm tròn đến hàng "
                 r"đơn vị)." % (_xx(h0, 1), d, th))
        giai = (r"$AB = \sqrt{AH^{2} + HB^{2}} = \sqrt{%s + %d} \approx %s$ (m); $\tan\widehat{HAB} = \dfrac{HB}{HA} = %s$ "
                r"nên $\widehat{HAB} \approx %s^{\circ}$." % (_xx(h0 * h0, 2), d * d, _xx(AB, 2), _xx(d / h0, 2), _xx(ABC, 2))
                + "\\\\\n" +
                r"$AH \parallel BC$ nên $\widehat{ABC} = \widehat{HAB} \approx %s^{\circ}$, suy ra "
                r"$\widehat{ACB} \approx 180^{\circ} - %d^{\circ} - %s^{\circ} = %s^{\circ}$." % (_xx(ABC, 2), th, _xx(ABC, 2), _xx(ACB, 2))
                + "\\\\\n" +
                r"Định lí sin: $BC = \dfrac{AB\cdot\sin %d^{\circ}}{\sin\widehat{ACB}} \approx %d$ (m)." % (th, dap))
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
        debai = (r"Trên nóc một toà nhà có một cột ăng-ten $BC$ cao $%d$ m ($C$ là chân cột). Từ vị trí quan sát $A$ "
                 r"cao $%d$ m so với mặt đất, có thể nhìn thấy đỉnh $B$ và chân $C$ của cột ăng-ten dưới góc $%d^{\circ}$ "
                 r"và $%d^{\circ}$ so với phương nằm ngang. Tính chiều cao $CH$ của toà nhà (đơn vị mét, làm tròn đến "
                 r"hàng đơn vị)." % (L, h0, al, be))
        giai = (r"$\widehat{BAC} = %d^{\circ} - %d^{\circ} = %d^{\circ}$; tam giác $ABD$ vuông tại $D$ nên "
                r"$\widehat{ABC} = 90^{\circ} - %d^{\circ} = %d^{\circ}$." % (al, be, al - be, al, 90 - al) + "\\\\\n" +
                r"Định lí sin trong tam giác $ABC$: $AC = \dfrac{BC\cdot\sin\widehat{ABC}}{\sin\widehat{BAC}} = "
                r"\dfrac{%d\cdot\sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$ (m)." % (L, 90 - al, al - be, _xx(AC, 2))
                + "\\\\\n" +
                r"Tam giác $ADC$ vuông tại $D$: $CD = AC\cdot\sin %d^{\circ} \approx %s$ (m). Vậy $CH = CD + DH \approx "
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


def L10_C3_B6_VD036_SA_E_01(socau, dang=2):
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
        debai = (r"Hai bạn An và Bình cùng xuất phát từ điểm $P$, đi theo hai hướng khác nhau tạo với nhau một góc "
                 r"$%d^{\circ}$ để đến đích là điểm $D$. An đi $%d$ km thì dừng ăn trưa tại $A$, rồi đi tiếp $%d$ km "
                 r"đến $D$, biết $\widehat{PAD} = %d^{\circ}$. Bình đi $%d$ km thì dừng ăn trưa tại $B$ (như hình vẽ). "
                 r"Hỏi Bình phải đi bao nhiêu km nữa để đến đích (làm tròn đến hàng phần mười)?" % (phi, m, n, psi, k))
        giai = (r"Tam giác $PAD$: $PD = \sqrt{%d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %d^{\circ}} \approx %s$ (km)."
                % (m, n, m, n, psi, _xx(PD, 3)) + "\\\\\n" +
                r"$\cos\widehat{APD} = \dfrac{PA^{2} + PD^{2} - AD^{2}}{2\cdot PA\cdot PD}$ nên $\widehat{APD} \approx %s^{\circ}$."
                % _xx(APD, 2) + "\\\\\n" +
                r"$\widehat{BPD} = %d^{\circ} - \widehat{APD} \approx %s^{\circ}$." % (phi, _xx(BPD, 2)) + "\\\\\n" +
                r"Tam giác $PBD$: $BD = \sqrt{PB^{2} + PD^{2} - 2\cdot PB\cdot PD\cdot\cos\widehat{BPD}} \approx %s$ (km)."
                % dap)
        ds = _ba_nhieu(dap, [_xx(abs(PD - k), 1), _xx(PD, 1), _xx(m + n - k, 1)],
                       buoc=lambda t: _xx(BD + 0.5 * t, 1))
        cau += MC_SA_answer_const(debai + "\n\n" + r"\begin{center}" + "\n" +
                                  _hinh_hai_ban(phi, m, n, k, PD, BPD) + "\n" + r"\end{center}",
                                  dap, ds, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_E_02(socau, dang=2):
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
        debai = (r"Hai bạn An và Bình cùng xuất phát từ điểm $P$ theo hai hướng tạo với nhau một góc $%d^{\circ}$ để "
                 r"đến đích $D$. An đi $%d$ km tới $A$ rồi đi tiếp $%d$ km tới $D$, biết $\widehat{PAD} = %d^{\circ}$. "
                 r"Bình đi $%d$ km tới $B$ rồi đi thẳng tới $D$ (như hình vẽ). Tính diện tích khu vực tứ giác $PADB$ "
                 r"(đơn vị $\text{km}^{2}$, làm tròn đến hàng phần mười)." % (phi, m, n, psi, k))
        giai = (r"$S_{PAD} = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %d^{\circ} \approx %s$." % (m, n, psi, _xx(S1, 3))
                + "\\\\\n" +
                r"$PD = \sqrt{%d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %d^{\circ}} \approx %s$; "
                r"$\widehat{APD} \approx %s^{\circ}$ nên $\widehat{BPD} \approx %s^{\circ}$."
                % (m, n, m, n, psi, _xx(PD, 3), _xx(APD, 2), _xx(BPD, 2)) + "\\\\\n" +
                r"$S_{PBD} = \dfrac{1}{2}\cdot PB\cdot PD\cdot\sin\widehat{BPD} \approx %s$." % _xx(S2, 3) + "\\\\\n" +
                r"Vậy $S_{PADB} \approx %s$ $\text{km}^{2}$." % dap)
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
        debai = r"Cho tam giác $ABC$ có $a = %d$, $b = %d$, $c = %d$. Xét tính đúng sai của các khẳng định sau:" % (a, b, c)
        # a) NB - góc lớn nhất đối diện cạnh lớn nhất, dấu côsin
        ly_a = (r"Góc lớn nhất là góc $%s$ (đối diện cạnh lớn nhất). $\cos %s = %s %s 0$ nên tam giác %s."
                % (ten_lon, ten_lon, _L(cos_lon), "<" if tu else ">", "có một góc tù" if tu else "có ba góc nhọn"))
        dung = [("Tam giác $ABC$ có một góc tù" if tu else "Tam giác $ABC$ có ba góc nhọn", ly_a)]
        sai = [("Tam giác $ABC$ có ba góc nhọn" if tu else "Tam giác $ABC$ có một góc tù", ly_a), ("Tam giác $ABC$ vuông", ly_a)]
        if [a, b, c].count(lon) == 1:
            dung.append((r"Góc lớn nhất của tam giác $ABC$ là góc $%s$" % ten_lon, ly_a))
            sai += [(r"Góc lớn nhất của tam giác $ABC$ là góc $%s$" % X, ly_a) for X, v in zip("ABC", (a, b, c)) if v != lon]
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
        y3 = _tf_gop(_tf_ct(r"Diện tích tam giác $ABC$ bằng $%s$", Integer(S), ly_c,
                            [(Integer(2 * S), "Nhân thừa 2"), (sqrt((p - a) * (p - b) * (p - c)), "Thiếu thừa số $p$"), (Rational(S, 2), "Chia thừa 2")],
                            them=[r"Nửa chu vi tam giác $ABC$ là $p = %d$" % p]))
        # d) VDC - bán kính ngoại tiếp, nội tiếp
        ly_d = (ly_c + r" $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d} = %s$, $r = \dfrac{S}{p} = %s$."
                % (a, b, c, S, _so_hoac_phan_so(R), _so_hoac_phan_so(Rational(S, p))))
        dung = [(r"Bán kính đường tròn ngoại tiếp tam giác $ABC$ bằng $%s$" % _so_hoac_phan_so(R), ly_d),
                (r"Bán kính đường tròn nội tiếp tam giác $ABC$ bằng $%s$" % _so_hoac_phan_so(Rational(S, p)), ly_d)]
        sai = [(r"Bán kính đường tròn ngoại tiếp tam giác $ABC$ bằng $%s$" % _so_hoac_phan_so(w), ly_d)
               for w in (4 * R, 2 * R, Rational(S, p)) if w != R]
        sai += [(r"Bán kính đường tròn nội tiếp tam giác $ABC$ bằng $%s$" % _so_hoac_phan_so(w), ly_d)
                for w in (Rational(S, 2 * p), Rational(2 * S, p), R) if w != Rational(S, p)]
        y4 = _phat_bieu(dung, sai)
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
        debai = (r"Cho tam giác $ABC$ có $\widehat{BAC} = %s$, $AB = %d$ và $AC = %d$. Xét tính đúng sai của các "
                 r"khẳng định sau:" % (_goc(A), c, b))
        # a) NB - nhận ra công thức diện tích
        ly_a = r"Diện tích bằng nửa tích hai cạnh nhân sin góc xen giữa: $S = \dfrac{1}{2}AB\cdot AC\cdot\sin A$; ngoài ra $S = \dfrac{1}{2}AC\cdot h_b$."
        mau = r"Diện tích tam giác $ABC$ được tính theo công thức $S = %s$"
        y1 = _phat_bieu(
            [(mau % r"\dfrac{1}{2}AB\cdot AC\cdot\sin A", ly_a), (mau % r"\dfrac{1}{2}AC\cdot h_b", ly_a)],
            [(mau % r"\dfrac{1}{2}AB\cdot AC\cdot\cos A", ly_a), (mau % r"AB\cdot AC\cdot\sin A", ly_a),
             (mau % r"\dfrac{1}{2}AB\cdot BC\cdot\sin A", ly_a), (mau % r"\dfrac{1}{2}AB\cdot h_b", ly_a)])
        # b) TH - thay số
        ly_b = r"$S = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %s = %s$." % (c, b, _goc(A), _L(S))
        y2 = _tf_gop(_tf_ct(r"Diện tích tam giác $ABC$ là $S = %s$", S, ly_b,
                            [(2 * S, "Quên hệ số $\\dfrac{1}{2}$"), (simplify(b * c * abs(cA) / 2), "Nhầm $\\sin A$ với $\\cos A$"), (S / 2, "Chia thừa 2")]),
                     _tf_bdt(r"Diện tích tam giác $ABC$ %s $%s$", float(S), ly_b))
        # c) VD - đường cao
        ly_c = ly_b + r" $h_b = \dfrac{2S}{AC} = \dfrac{2\cdot %s}{%d} = %s$." % (_L(S), b, _L(hb))
        y3 = _tf_gop(_tf_ct(r"Độ dài đường cao kẻ từ $B$ là $h_b = %s$", hb, ly_c,
                            [(2 * hb, "Nhân thừa 2"), (hb / 2, "Quên nhân 2"), (simplify(2 * S / c), "Chia nhầm cạnh $AB$")],
                            them=[r"Độ dài đường cao kẻ từ $B$ là $h_b = AB\cdot\sin %s$" % _goc(A)]))
        # d) VDC - trụ điện cách đều ba hộ dân
        bai = (r"Ba vị trí $A$, $B$, $C$ là ba hộ dân cần kéo điện sinh hoạt. Người ta muốn đặt một trụ điện tại vị "
               r"trí $D$ sao cho dây điện kéo từ trụ điện đến các hộ dân dài như nhau. Khi đó $DA = %s$")
        ly_d = (r"$DA = DB = DC$ nên $D$ là tâm đường tròn ngoại tiếp, $DA = R$. $BC^{2} = %d + %d - 2\cdot %d\cdot %d"
                r"\cdot %s = %s$, $R = \dfrac{BC}{2\sin A} = %s$." % (c * c, b * b, c, b, _ngoac(cA), _L(a2), _L(R)))
        dung = [(bai % _L(R), ly_d), (bai.replace("$DA = %s$", "$DB + DC = %s$") % _L(simplify(2 * R)), ly_d)]
        sai = []
        for w, ghi in ((simplify(2 * R), "Quên chia 2"), (simplify(sqrt(b * b + c * c + 2 * b * c * cA) / (2 * sA)), "Sai dấu khi tính $BC$"),
                       (simplify(sqrt(a2) / (2 * abs(cA))), "Nhầm $\\sin A$ với $\\cos A$")):
            if simplify(w - R) != 0:
                sai.append((bai % _L(w), ghi + ". " + ly_d))
        sai.append((bai.replace("$DA = %s$", "$DB + DC = %s$") % _L(R), ly_d))
        y4 = _phat_bieu(dung, sai)
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
        debai = (r"Lúc $7$ giờ kém $%d$ phút, bạn Mai đi xe đạp từ nhà (điểm $A$) đến trường (điểm $B$), phải lên dốc "
                 r"$AC$ rồi xuống dốc $CB$ ($C$ là đỉnh dốc, như hình vẽ). Biết đoạn lên dốc dài $%d$ m, $\widehat{A} = "
                 r"%d^{\circ}$, $\widehat{B} = %d^{\circ}$. Xét tính đúng sai của các khẳng định sau:" % (phut, L, al, be))
        # a) NB - đọc góc
        len_cao = al > be
        ly_a = (r"Góc nghiêng lúc lên là $%d^{\circ}$, lúc xuống là $%d^{\circ}$; $\widehat{ACB} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$."
                % (al, be, al, be, 180 - al - be))
        y1 = _phat_bieu(
            [(r"Độ dốc lúc lên %s lúc xuống" % ("cao hơn" if len_cao else "thấp hơn"), ly_a),
             (r"$\widehat{ACB} = %d^{\circ}$" % (180 - al - be), ly_a)],
            [(r"Độ dốc lúc lên %s lúc xuống" % ("thấp hơn" if len_cao else "cao hơn"), ly_a),
             (r"$\widehat{ACB} = %d^{\circ}$" % (al + be), ly_a), (r"$\widehat{ACB} = %d^{\circ}$" % (180 - al), ly_a),
             (r"$\widehat{ACB} = %d^{\circ}$" % (90 - al), ly_a)])
        # b) TH - độ cao dốc
        ly_b = r"$CH = AC\cdot\sin A = %d\cdot\sin %d^{\circ}$." % (L, al)
        y2 = _tf_gop(_tf_so(r"Độ cao con dốc là $%s$", CH, 1, ly_b,
                            [(L * math.tan(math.radians(al)), "Nhầm $CH = AC\\cdot\\tan A$"), (L * _cos_d(al), "Nhầm $\\sin$ với $\\cos$"),
                             (L * _sin_d(be), "Dùng nhầm góc $B$")], dv=m, bdt=r"Độ cao con dốc %s $%s$"))
        # c) VD - quãng đường chim bay (định lí sin)
        ly_c = (r"$\widehat{C} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$; định lí sin: $AB = \dfrac{AC\cdot\sin C}"
                r"{\sin B}$." % (al, be, 180 - al - be))
        y3 = _tf_gop(_tf_so(r"Quãng đường chim bay từ nhà đến trường là $%s$", AB, 0, ly_c,
                            [(L + CB, "Đó là quãng đường đi theo dốc $AC + CB$"), (L * _sin_d(al + be) / _sin_d(al), "Chia nhầm cho $\\sin A$"),
                             (math.hypot(L, CB), "Coi tam giác vuông tại $C$")], dv=m, bdt=r"Quãng đường chim bay từ nhà đến trường %s $%s$"))
        # d) VDC - vận tốc lên dốc
        ly_d = (r"$CB = \dfrac{AC\cdot\sin A}{\sin B} \approx %s$ m; thời gian xuống dốc $\approx %s$ giờ; thời gian lên "
                r"dốc $\approx \dfrac{%d}{60} - %s \approx %s$ giờ; vận tốc lên dốc $\approx \dfrac{%s}{%s}$ km/h."
                % (_xx(CB, 2), _xx(CB / 1000 / v2, 4), phut, _xx(CB / 1000 / v2, 4), _xx(t_len, 4), _xx(L / 1000, 3), _xx(t_len, 4)))
        mau = (r"Để đến trường lúc $7$ giờ đúng, biết khi xuống dốc Mai đi với vận tốc không đổi $%d$ km/h, thì Mai "
               r"đã lên dốc với vận tốc khoảng $%s$ km/h" % (v2, "%s"))
        t_sai = phut / 60 - AB / 1000 / v2
        sai = [(L / 1000 / (phut / 60), "Quên trừ thời gian xuống dốc"),
               (L / 1000 / t_sai if t_sai > 0 else None, "Dùng nhầm $AB$ thay cho $CB$"),
               (L / 1000 / (phut / 60 - CB / v2 / 60) if phut / 60 - CB / v2 / 60 > 0 else None, "Đổi đơn vị sai")]
        d1, s1 = _tf_so(mau, v1, 0, ly_d, sai, bdt=r"Để đến trường lúc $7$ giờ đúng, Mai phải lên dốc với vận tốc %s $%s$ km/h")
        d2, s2 = _tf_so(r"Thời gian Mai lên dốc khoảng $%s$ phút", t_len * 60, 1, ly_d,
                        [(phut - CB / 1000 / v2, "Trừ lẫn phút với giờ"), (phut, "Quên trừ thời gian xuống dốc")]) \
            if _xa_bien(t_len * 60, 1) else ([], [])
        y4 = _phat_bieu(d1 + d2, s1 + s2)
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
        debai = (r"Một con dốc có đỉnh $C$ cao $CH = %d$ m so với mặt đường ($H$ thuộc $AB$). Đoạn lên dốc $AC$ nghiêng "
                 r"$\widehat{A} = %d^{\circ}$, đoạn xuống dốc $CB$ nghiêng $\widehat{B} = %d^{\circ}$ so với phương nằm "
                 r"ngang (như hình vẽ). Xét tính đúng sai của các khẳng định sau:" % (h, al, be))
        # a) NB - tam giác vuông AHC
        ly_a = r"Tam giác $AHC$ vuông tại $H$: $AC = \dfrac{CH}{\sin A} = \dfrac{%d}{\sin %d^{\circ}}$." % (h, al)
        y1 = _tf_gop(_tf_so(r"Đoạn lên dốc dài khoảng $%s$", AC, 0, ly_a,
                            [(h / math.tan(math.radians(al)), "Đó là $AH$"), (h / _cos_d(al), "Nhầm $\\sin$ với $\\cos$"),
                             (h * _sin_d(al), "Nhầm $AC = CH\\cdot\\sin A$")], dv=m, bdt=r"Đoạn lên dốc %s $%s$", tu=("dài hơn", "ngắn hơn")))
        # b) TH - tam giác vuông BHC
        ly_b = r"Tam giác $BHC$ vuông tại $H$: $CB = \dfrac{CH}{\sin B} = \dfrac{%d}{\sin %d^{\circ}}$." % (h, be)
        y2 = _tf_gop(_tf_so(r"Đoạn xuống dốc dài khoảng $%s$", CB, 0, ly_b,
                            [(h / math.tan(math.radians(be)), "Đó là $HB$"), (h / _cos_d(be), "Nhầm $\\sin$ với $\\cos$"),
                             (h / _sin_d(al), "Dùng nhầm góc $A$")], dv=m, bdt=r"Đoạn xuống dốc %s $%s$", tu=("dài hơn", "ngắn hơn")))
        # c) VD - khoảng cách hai chân dốc
        ly_c = (r"$AB = AH + HB = \dfrac{CH}{\tan A} + \dfrac{CH}{\tan B}$ (hoặc dùng định lí sin trong tam giác $ABC$).")
        y3 = _tf_gop(_tf_so(r"Khoảng cách giữa hai chân dốc $A$ và $B$ khoảng $%s$", AB, 0, ly_c,
                            [(AC + CB, "Đó là tổng hai đoạn dốc"), (abs(h / math.tan(math.radians(al)) - h / math.tan(math.radians(be))), "Trừ thay vì cộng"),
                             (h * (math.tan(math.radians(al)) + math.tan(math.radians(be))), "Nhầm $\\tan$ với $\\cot$")], dv=m,
                            bdt=r"Khoảng cách giữa hai chân dốc %s $%s$"))
        # d) VDC - thời gian đi hết con dốc
        ly_d = (r"Thời gian lên dốc $\dfrac{%s}{%d}$ giờ, xuống dốc $\dfrac{%s}{%d}$ giờ; tổng (đổi ra phút)."
                % (_xx(AC / 1000, 4), v1, _xx(CB / 1000, 4), v2))
        mau = (r"Một người đi xe đạp lên dốc với vận tốc $%d$ km/h và xuống dốc với vận tốc $%d$ km/h thì đi hết cả "
               r"con dốc mất khoảng $%s$ phút" % (v1, v2, "%s"))
        y4 = _tf_gop(_tf_so(mau, t, 1, ly_d,
                            [((AC + CB) / 1000 / ((v1 + v2) / 2) * 60, "Dùng vận tốc trung bình cộng"),
                             ((AC / 1000 / v2 + CB / 1000 / v1) * 60, "Đảo hai vận tốc"), (AB / 1000 / v1 * 60, "Dùng nhầm $AB$")],
                            bdt=(r"Một người đi xe đạp lên dốc với vận tốc $%d$ km/h và xuống dốc với vận tốc $%d$ km/h thì đi hết cả "
                                 r"con dốc mất %s $%s$ phút" % (v1, v2, "%s", "%s")), tu=("hơn", "chưa đến")))
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
        debai = (r"Người ta định lát gạch trên mảnh đất hình tứ giác $ABCD$ như hình vẽ. Biết $AB = %d$ m, $BC = CD = %d$ m, "
                 r"$\widehat{ABC} = %d^{\circ}$, $\widehat{BCD} = %d^{\circ}$ và giá lát gạch là $%d\,000$ đồng trên một mét "
                 r"vuông. Xét tính đúng sai của các khẳng định sau:" % (p, q, b, g, gia))
        # a) NB - định lí côsin trong tam giác BCD
        ly_a = (r"Tam giác $BCD$: $BD^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %d^{\circ} = %s$ nên $BD = %s$ m."
                % (q * q, q * q, q, q, g, _L(BD ** 2), _L(BD)))
        y1 = _tf_gop(_tf_ct(r"Độ dài đường chéo $BD$ bằng $%s$ m", BD, ly_a,
                            [(q * CAN[{60: 90, 90: 120, 120: 90}[g]], "Tính sai"), (Integer(q), "Nhầm tam giác $BCD$ đều"),
                             (simplify(q * sqrt(2 + 2 * _gtlg("cos", g))), "Sai dấu"), (Integer(2 * q), "Cộng hai cạnh")],
                            them=[r"$BD^{2} = %s$" % _L(BD ** 2)]))
        # b) TH - tam giác cân
        ly_b = (r"Tam giác $BCD$ cân tại $C$ nên $\widehat{DBC} = \dfrac{180^{\circ} - %d^{\circ}}{2} = %d^{\circ}$, do đó "
                r"$\widehat{ABD} = %d^{\circ} - %d^{\circ} = %d^{\circ}$." % (g, dbc, b, dbc, abd))
        y2 = _phat_bieu(
            [(r"Số đo góc $\widehat{ABD}$ bằng $%d^{\circ}$" % abd, ly_b), (r"Số đo góc $\widehat{DBC}$ bằng $%d^{\circ}$" % dbc, ly_b)],
            [(r"Số đo góc $\widehat{ABD}$ bằng $%d^{\circ}$" % w, ly_b) for w in (abd + 10, b - g, b - (180 - g)) if 0 < w < 180 and w != abd] +
            [(r"Số đo góc $\widehat{DBC}$ bằng $%d^{\circ}$" % w, ly_b) for w in (g, 180 - g) if w != dbc])
        # c) VD - diện tích tam giác BCD
        ly_c = r"$S_{BCD} = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %d^{\circ} = %s$ ($\text{m}^{2}$)." % (q, q, g, _L(SBCD))
        sai_c = [(2 * SBCD, "Quên hệ số $\\dfrac{1}{2}$"), (SBCD / 2, "Chia thừa 2")]
        if g != 90:
            sai_c.append((simplify(q * q * abs(_gtlg("cos", g)) / 2), "Nhầm $\\sin$ với $\\cos$"))
        y3 = _tf_gop(_tf_ct(r"Diện tích tam giác $BCD$ bằng $%s$ $\text{m}^{2}$", SBCD, ly_c, sai_c),
                     _tf_bdt(r"Diện tích tam giác $BCD$ %s $%s$", float(SBCD), ly_c, dv=r"\,\text{m}^{2}"))
        # d) VDC - diện tích tứ giác, chi phí
        ly_d = (r"$S_{ABD} = \dfrac{1}{2}\cdot %d\cdot %s\cdot\sin %d^{\circ} \approx %s$; $S_{ABCD} \approx %s$ "
                r"$\text{m}^{2}$; chi phí $\approx %s$ đồng." % (p, _L(BD), abd, _xx(S2, 2), _xx(S1 + S2, 2),
                                                               "{:,}".format(_lt((S1 + S2) * gia * 1000)).replace(",", r"\,")))
        d1, s1 = _n3_chi_phi(S1 + S2, gia, ly_d)
        d2, s2 = _tf_so(r"Diện tích mảnh đất $ABCD$ xấp xỉ $%s$", S1 + S2, 1, ly_d,
                        [(S1 + 2 * S2, "Quên hệ số $\\dfrac{1}{2}$ ở $S_{ABD}$"), (S1 + 0.5 * p * q * _sin_d(b), "Dùng nhầm $\\widehat{ABC}$ cho tam giác $ABD$")],
                        dv=r"\,\text{m}^{2}")
        y4 = _phat_bieu(d1 + d2, s1 + s2)
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
        debai = (r"Một mảnh đất hình tứ giác $ABCD$ (như hình vẽ) có $AB = %d$ m, $AD = %d$ m, $\widehat{BAD} = %d^{\circ}$, "
                 r"$BC = %d$ m, $CD = %d$ m. Giá làm cỏ là $%d\,000$ đồng trên một mét vuông. Xét tính đúng sai của các "
                 r"khẳng định sau:" % (u, v, A, x, y, gia))
        # a) NB - định lí côsin trong tam giác ABD
        ly_a = (r"$BD^{2} = %d + %d - 2\cdot %d\cdot %d\cdot\cos %d^{\circ} = %d$ nên $BD = %d$ m."
                % (u * u, v * v, u, v, A, BD * BD, BD))
        y1 = _tf_gop(_tf_ct(r"Độ dài đường chéo $BD$ bằng $%s$ m", Integer(BD), ly_a,
                            [(sqrt(Integer(u * u + v * v + 2 * u * v * int(round(2 * _cos_d(A))) // 2)), "Sai dấu của $\\cos A$"),
                             (sqrt(Integer(u * u + v * v)), "Quên số hạng chứa $\\cos A$"), (Integer(u + v), "Cộng hai cạnh")],
                            them=[r"$BD^{2} = %d$" % (BD * BD)]))
        # b) TH - hệ quả định lí côsin trong tam giác BCD
        ly_b = (r"$\cos\widehat{BCD} = \dfrac{CB^{2} + CD^{2} - BD^{2}}{2\cdot CB\cdot CD} = \dfrac{%d + %d - %d}{2\cdot %d"
                r"\cdot %d} = %s$." % (x * x, y * y, BD * BD, x, y, _so_hoac_phan_so(cosC)))
        dung = [(r"$\cos\widehat{BCD} = %s$" % _so_hoac_phan_so(cosC), ly_b),
                (r"Góc $\widehat{BCD}$ là góc %s" % ("tù" if cosC < 0 else "nhọn"), ly_b)]
        sai = [(r"$\cos\widehat{BCD} = %s$" % _so_hoac_phan_so(w), ly_b)
               for w in (-cosC, 2 * cosC, Rational(x * x + BD * BD - y * y, 2 * x * BD)) if w != cosC]
        sai.append((r"Góc $\widehat{BCD}$ là góc %s" % ("nhọn" if cosC < 0 else "tù"), ly_b))
        y2 = _phat_bieu(dung, sai)
        # c) VD - diện tích tam giác ABD
        ly_c = r"$S_{ABD} = \dfrac{1}{2}\cdot %d\cdot %d\cdot\sin %d^{\circ} = %s$ ($\text{m}^{2}$)." % (u, v, A, _L(S1e))
        y3 = _tf_gop(_tf_ct(r"Diện tích tam giác $ABD$ bằng $%s$ $\text{m}^{2}$", S1e, ly_c,
                            [(2 * S1e, "Quên hệ số $\\dfrac{1}{2}$"), (Rational(u * v, 4), "Nhầm $\\sin$ với $\\cos$"), (S1e / 2, "Chia thừa 2")]),
                     _tf_bdt(r"Diện tích tam giác $ABD$ %s $%s$", float(S1e), ly_c, dv=r"\,\text{m}^{2}"))
        # d) VDC - tổng diện tích, chi phí
        ly_d = (r"$\sin\widehat{BCD} = \sqrt{1 - \cos^{2}\widehat{BCD}} \approx %s$, $S_{BCD} \approx %s$; $S_{ABCD} \approx "
                r"%s$ $\text{m}^{2}$; chi phí $\approx %s$ đồng." % (_xx(sC, 4), _xx(S2, 2), _xx(S1 + S2, 2),
                                                                   "{:,}".format(_lt((S1 + S2) * gia * 1000)).replace(",", r"\,")))
        d1, s1 = _n3_chi_phi(S1 + S2, gia, ly_d, "làm cỏ toàn bộ mảnh đất")
        d2, s2 = _tf_so(r"Diện tích mảnh đất $ABCD$ xấp xỉ $%s$", S1 + S2, 1, ly_d,
                        [(S1 + 2 * S2, "Quên hệ số $\\dfrac{1}{2}$ ở $S_{BCD}$"), (S1 + 0.5 * x * y * abs(float(cosC)), "Nhầm $\\sin$ với $\\cos$")],
                        dv=r"\,\text{m}^{2}")
        y4 = _phat_bieu(d1 + d2, s1 + s2)
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
        debai = (r"Cho góc $\alpha$ với %s và $\%s\alpha = %s$. Giá trị của $\%s\left(180^{\circ} - \alpha\right)$ bằng"
                 % (_MIEN_GOC[ham], ham, _tri(v), ham))
        giai = (r"Hai góc $\alpha$ và $180^{\circ} - \alpha$ bù nhau nên $%s = %s$."
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
        debai = (r"Cho góc $\alpha$ với %s và $\%s\left(180^{\circ} - \alpha\right) = %s$. Giá trị của $\%s\alpha$ bằng"
                 % (_MIEN_GOC[ham], ham, _tri(v), ham))
        giai = (r"Hai góc $\alpha$ và $180^{\circ} - \alpha$ bù nhau nên $%s$, suy ra $\%s\alpha = %s$."
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
        debai = (r"Cho góc nhọn $\alpha$ có $\%s\alpha = %s$. Giá trị của $\%s\left(90^{\circ} - \alpha\right)$ bằng"
                 % (ham, _tri(v), hoi))
        giai = (r"Hai góc $\alpha$ và $90^{\circ} - \alpha$ phụ nhau nên $%s = %s$."
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
        debai = (r"Cho góc nhọn $\alpha$ có $\%s\left(90^{\circ} - \alpha\right) = %s$. Giá trị của $\%s\alpha$ bằng"
                 % (cho, _tri(v), ham))
        giai = (r"Hai góc $\alpha$ và $90^{\circ} - \alpha$ phụ nhau nên $%s$, suy ra $\%s\alpha = %s$."
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
        debai = (r"Cho hình vẽ bên, trong đó ba điểm $A$, $O$, $B$ thẳng hàng, $\widehat{AOC} = \alpha$, "
                 r"$\widehat{BOC} = \beta$. Biết $\%s\alpha = %s$. Giá trị của $\%s\beta$ bằng"
                 % (ham, _tri(v), ham))
        giai = (r"Vì $A$, $O$, $B$ thẳng hàng nên $\alpha + \beta = 180^{\circ}$, tức $\beta = 180^{\circ} - \alpha$."
                + "\\\\\n" + r"Do đó $\%s\beta = %s = %s$."
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
        debai = (r"Cho hình vẽ bên, trong đó $\widehat{xOy} = 90^{\circ}$, tia $Oz$ nằm giữa hai tia $Ox$, $Oy$, "
                 r"$\widehat{xOz} = \alpha$, $\widehat{zOy} = \beta$. Biết $\%s\alpha = %s$. Giá trị của $\%s\beta$ bằng"
                 % (ham, _tri(v), hoi))
        giai = (r"Vì tia $Oz$ nằm giữa hai tia $Ox$, $Oy$ nên $\alpha + \beta = 90^{\circ}$, tức "
                r"$\beta = 90^{\circ} - \alpha$." + "\\\\\n" +
                r"Do đó $\%s\beta = \%s\left(90^{\circ} - \alpha\right) = \%s\alpha = %s$." % (hoi, hoi, ham, _tri(v)))
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


def L10_C3_B5_TH031_SA_D_01(socau, dang=2):
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
        debai = (r"Cho góc $\alpha$ với %s và $\%s\alpha = %s$. Tính $\%s\left(180^{\circ} - \alpha\right)$."
                 % (_MIEN_GOC[ham], ham, _tp(v), ham))
        giai = (r"Hai góc $\alpha$ và $180^{\circ} - \alpha$ bù nhau nên $%s = %s$."
                % (_BIEU_BU[ham], _tp(dap)))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_D_02(socau, dang=2):
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
        debai = (r"Cho góc $\alpha$ với %s và $\%s\left(180^{\circ} - \alpha\right) = %s$. Tính $\%s\alpha$."
                 % (_MIEN_GOC[ham], ham, _tp(v), ham))
        giai = (r"Hai góc $\alpha$ và $180^{\circ} - \alpha$ bù nhau nên $%s$, suy ra $\%s\alpha = %s$."
                % (_BIEU_BU[ham], ham, _tp(dap)))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_E_01(socau, dang=2):
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
        debai = (r"Cho góc nhọn $\alpha$ có $\%s\alpha = %s$. Tính $\%s\left(90^{\circ} - \alpha\right)$."
                 % (ham, _tp(v), _DOI_HAM[ham]))
        giai = r"Hai góc $\alpha$ và $90^{\circ} - \alpha$ phụ nhau nên $%s = %s$." % (_BIEU_PHU[ham], _tp(v))
        cau += MC_SA_answer_const(debai, _tp(v), _nhieu_tp(v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_E_02(socau, dang=2):
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
        debai = (r"Cho góc nhọn $\alpha$ có $\%s\left(90^{\circ} - \alpha\right) = %s$. Tính $\%s\alpha$."
                 % (_DOI_HAM[ham], _tp(v), ham))
        giai = (r"Hai góc $\alpha$ và $90^{\circ} - \alpha$ phụ nhau nên $%s$, suy ra $\%s\alpha = %s$."
                % (_BIEU_PHU[ham], ham, _tp(v)))
        cau += MC_SA_answer_const(debai, _tp(v), _nhieu_tp(v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_F_01(socau, dang=2):
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
        debai = (r"Cho hình vẽ bên, trong đó ba điểm $A$, $O$, $B$ thẳng hàng, $\widehat{AOC} = \alpha$, "
                 r"$\widehat{BOC} = \beta$. Biết $\%s\alpha = %s$. Tính $\%s\beta$." % (ham, _tp(v), ham))
        giai = (r"Vì $A$, $O$, $B$ thẳng hàng nên $\beta = 180^{\circ} - \alpha$." + "\\\\\n" +
                r"Do đó $\%s\beta = %s = %s$." % (ham, _BIEU_BU[ham].split("= ")[1], _tp(dap)))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, _hinh_goc_bet(a), 0, dang)
    return cau


def L10_C3_B5_TH031_SA_F_02(socau, dang=2):
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
        debai = (r"Cho hình vẽ bên, trong đó $\widehat{xOy} = 90^{\circ}$, tia $Oz$ nằm giữa hai tia $Ox$, $Oy$, "
                 r"$\widehat{xOz} = \alpha$, $\widehat{zOy} = \beta$. Biết $\%s\alpha = %s$. Tính $\%s\beta$."
                 % (ham, _tp(v), hoi))
        giai = (r"Vì tia $Oz$ nằm giữa hai tia $Ox$, $Oy$ nên $\beta = 90^{\circ} - \alpha$." + "\\\\\n" +
                r"Do đó $\%s\beta = \%s\left(90^{\circ} - \alpha\right) = \%s\alpha = %s$." % (hoi, hoi, ham, _tp(v)))
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
    return (r"Vì $A + B + C = 180^{\circ}$ nên $%s = 180^{\circ} - %s$, hai góc $%s$ và $%s$ bù nhau."
            % (tong, X, tong, X) + "\\\\\n" + r"Do đó $%s$, suy ra $%s = %s$." % (bt, hoi, dap_tex))


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
        debai = r"Cho tam giác $ABC$ có $%s = %s$. Giá trị của $%s$ bằng" % (cho, _tri(v), hoi)
        giai = _giai_tam_giac_bu(ham, X, tong, cho_tong, _tri(dap))
        cau += MC_SA_answer_const(debai, _tri(dap), _nhieu_phu_bu(ham, dap, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_D_03(socau, dang=2):
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
        debai = r"Cho tam giác $ABC$ có $%s = %s$. Tính $%s$." % (cho, _tp(v), hoi)
        giai = _giai_tam_giac_bu(ham, X, tong, cho_tong, _tp(dap))
        cau += MC_SA_answer_const(debai, _tp(dap), _nhieu_tp(dap), giai, 0, 0, dang)
    return cau


def _giai_tam_giac_vuong(Y, Z, ham, dap_tex):
    hoi = _DOI_HAM[ham]
    return (r"Tam giác $ABC$ vuông tại $A$ nên $\widehat{B} + \widehat{C} = 90^{\circ}$, hai góc $B$ và $C$ "
            r"phụ nhau." + "\\\\\n" + r"Do đó $\%s %s = \%s %s = %s$." % (hoi, Z, ham, Y, dap_tex))


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
        debai = (r"Cho tam giác $ABC$ vuông tại $A$ có $\%s %s = %s$. Giá trị của $\%s %s$ bằng"
                 % (ham, Y, _tri(v), _DOI_HAM[ham], Z))
        giai = _giai_tam_giac_vuong(Y, Z, ham, _tri(v))
        cau += MC_SA_answer_const(debai, _tri(v), _nhieu_phu_bu(ham, v, v), giai, 0, 0, dang)
    return cau


def L10_C3_B5_TH031_SA_E_03(socau, dang=2):
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
        debai = (r"Cho tam giác $ABC$ vuông tại $A$ có $\%s %s = %s$. Tính $\%s %s$."
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
        debai = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$ và $\cos\left(%s\right) = %s$."
                 % (XY, m_, XZ, n_, tong, _tri(v)))
        ds = [(r"Tính $\cos %s$." % X, r"\cos %s = %s" % (X, _tri(cX)),
               r"Vì $A + B + C = 180^{\circ}$ nên $%s = 180^{\circ} - %s$, hai góc bù nhau. Do đó "
               r"$\cos %s = -\cos\left(%s\right) = %s$." % (tong, X, X, tong, _tri(cX))),
              (r"Tính độ dài cạnh $%s$." % YZ, r"%s = %s" % (YZ, _tri(sqrt(c2))),
               r"Theo định lí côsin: $%s^{2} = %s^{2} + %s^{2} - 2\cdot %s\cdot %s\cdot\cos %s "
               r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s = %s$." % (
                   YZ, XY, XZ, XY, XZ, X, m_, n_, m_, n_, _ngoac(cX), _tri(c2)) + "\\\\\n" +
               r"Vậy $%s = %s$." % (YZ, _tri(sqrt(c2))))]
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
        debai = (r"Cho tam giác $ABC$ có $%s = %d$ và $\sin\left(%s\right) = %s$."
                 % (YZ, a_, tong, _tri(v)))
        ds = [(r"Tính $\sin %s$." % X, r"\sin %s = %s" % (X, _tri(v)),
               r"Vì $A + B + C = 180^{\circ}$ nên $%s = 180^{\circ} - %s$, hai góc bù nhau. Do đó "
               r"$\sin %s = \sin\left(%s\right) = %s$." % (tong, X, X, tong, _tri(v))),
              (r"Tính bán kính $R$ của đường tròn ngoại tiếp tam giác $ABC$.", r"R = %s" % _tri(R),
               r"Theo định lí sin: $\dfrac{%s}{\sin %s} = 2R$, suy ra $R = \dfrac{%s}{2\sin %s} "
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
        debai = r"Cho tam giác $ABC$ vuông tại $A$ có $BC = %d$ và $\cos %s = %s$." % (a_, Z, _tri(v))
        ds = [(r"Tính $\sin %s$." % Y, r"\sin %s = %s" % (Y, _tri(v)),
               r"Tam giác $ABC$ vuông tại $A$ nên $\widehat{B} + \widehat{C} = 90^{\circ}$, hai góc phụ nhau. "
               r"Do đó $\sin %s = \cos %s = %s$." % (Y, Z, _tri(v))),
              (r"Tính độ dài cạnh $%s$." % doi, r"%s = %s" % (doi, _tri(canh)),
               r"Theo định lí sin: $\dfrac{%s}{\sin %s} = \dfrac{BC}{\sin A}$, với $\sin A = \sin 90^{\circ} = 1$ "
               r"nên $%s = BC\cdot\sin %s = %d\cdot %s = %s$." % (doi, Y, doi, Y, a_, _tri(v), _tri(canh)))]
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
        debai = (r"Cho tam giác $ABC$ có $%s = %d$, $%s = %d$ và $\sin\left(%s\right) = %s$."
                 % (XY, m_, XZ, n_, tong, _tri(v)))
        ds = [(r"Tính $\sin %s$." % X, r"\sin %s = %s" % (X, _tri(v)),
               r"Vì $A + B + C = 180^{\circ}$ nên $%s = 180^{\circ} - %s$, hai góc bù nhau. Do đó "
               r"$\sin %s = \sin\left(%s\right) = %s$." % (tong, X, X, tong, _tri(v))),
              (r"Tính diện tích tam giác $ABC$.", r"S = %s" % _tri(S),
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
    return (r"Trên một sườn đồi có độ dốc $%d\%%$ (độ dốc của sườn đồi được tính bằng tang của góc tạo bởi "
            r"sườn đồi với phương nằm ngang) có một cây cao $BC$ mọc thẳng đứng ($B$ là gốc cây). Ở phía chân "
            r"đồi, tại điểm $A$ cách gốc cây $%d\,\text{m}$, người ta nhìn ngọn cây dưới một góc $%s$ so với "
            r"phương nằm ngang (như hình vẽ)." % (p, d, _goc(be)))


def _giai_suon_doi(p, d, be, al, h):
    return (r"Gọi $\alpha$ là góc tạo bởi sườn đồi với phương nằm ngang: $\tan\alpha = %s$ nên "
            r"$\alpha \approx %s^{\circ}$." % (_xx(p / 100), _x1(al)) + "\\\\\n" +
            r"Trong tam giác $ABC$: $\widehat{BAC} = %s - \alpha$, $\widehat{ABC} = 90^{\circ} + \alpha$ "
            r"(cây thẳng đứng), $\widehat{ACB} = 180^{\circ} - \widehat{BAC} - \widehat{ABC} = 90^{\circ} - %s = %s$."
            % (_goc(be), _goc(be), _goc(90 - be)) + "\\\\\n" +
            r"Định lí sin: $BC = \dfrac{AB\cdot\sin\widehat{BAC}}{\sin\widehat{ACB}} = "
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
        debai = _de_suon_doi(p, d, be) + r" Chiều cao của cây (làm tròn đến hàng đơn vị, theo đơn vị mét) là"
        giai = _giai_suon_doi(p, d, be, al, h) + "\\\\\n" + r"Vậy cây cao khoảng $%s\,\text{m}$." % dap
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_suon_doi(al, be), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_G_01(socau, dang=2):
    r"""Trả lời ngắn - sườn đồi độ dốc $p\%$, cây mọc thẳng đứng: tính chiều cao của
    cây (làm tròn đến hàng đơn vị) - có hình.

    CLAUDE THEM 30/09/2026 - dang moi theo bai co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        p, d, be, al, h = _bo_suon_doi()
        dap = str(_lt(h))
        debai = _de_suon_doi(p, d, be) + r" Tính chiều cao của cây (làm tròn đến hàng đơn vị, theo đơn vị mét)."
        giai = _giai_suon_doi(p, d, be, al, h) + "\\\\\n" + r"Vậy cây cao khoảng $%s\,\text{m}$." % dap
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
        ds = [(r"Tính góc tạo bởi sườn đồi với phương nằm ngang (làm tròn đến hàng phần mười của độ).",
               r"\alpha \approx %s^{\circ}" % _x1(al),
               r"Gọi $\alpha$ là góc tạo bởi sườn đồi với phương nằm ngang. Độ dốc $%d\%%$ nên "
               r"$\tan\alpha = %s$, suy ra $\alpha \approx %s^{\circ}$." % (p, _xx(p / 100), _x1(al))),
              (r"Tính chiều cao của cây (làm tròn đến hàng đơn vị, theo đơn vị mét).",
               r"BC \approx %d\,\text{m}" % _lt(h),
               r"Trong tam giác $ABC$: $\widehat{BAC} = %s - \alpha$, $\widehat{ABC} = 90^{\circ} + \alpha$, "
               r"$\widehat{ACB} = 90^{\circ} - %s = %s$.\\ Định lí sin: $BC = \dfrac{AB\cdot\sin\widehat{BAC}}"
               r"{\sin\widehat{ACB}} = \dfrac{%d\cdot\sin\left(%s - \alpha\right)}{\sin %s} \approx %s$, "
               r"tức cây cao khoảng $%d\,\text{m}$." % (_goc(be), _goc(be), _goc(90 - be), d, _goc(be),
                                                         _goc(90 - be), _xx(h, 2), _lt(h)))]
        cau += TL_answer_text(debai, ds, _hinh_suon_doi(al, be), 0, dong)
    return cau


_PHUONG = {"E": "đông", "W": "tây", "N": "bắc", "S": "nam"}
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
    return (r"Trên biển, một tàu cá xuất phát từ cảng $A$, chạy về phía %s $%d\,\text{km}$ tới $B$, rồi chuyển "
            r"sang hướng %s chạy tiếp $%d\,\text{km}$ nữa tới đảo $C$." % (_PHUONG[X], d1, _huong_la_ban(X, th, Y), d2))


def _giai_tau_AC(X, Y, th, d1, d2, AC):
    return (r"Tàu chạy về phía %s rồi quay về phía %s một góc $%s$ nên $\widehat{ABC} = 180^{\circ} - %s = %s$."
            % (_PHUONG[X], _PHUONG[Y], _goc(th), _goc(th), _goc(180 - th)) + "\\\\\n" +
            r"Định lí côsin: $AC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s \approx %s$, nên "
            r"$AC \approx %s\,\text{km}$." % (d1, d2, d1, d2, _goc(180 - th), _xx(AC * AC, 2), _xx(AC, 2)))


def _giai_tau_huong(X, Y, th, d2, AC, phi):
    return (r"Định lí sin: $\sin\widehat{BAC} = \dfrac{BC\cdot\sin\widehat{ABC}}{AC} = "
            r"\dfrac{%d\cdot\sin %s}{AC} \approx %s$, góc $\widehat{BAC}$ nhọn nên $\widehat{BAC} \approx %s$."
            % (d2, _goc(180 - th), _xx(math.sin(math.radians(phi)), 4), _goc(_lt(phi))) + "\\\\\n" +
            r"Tia $AB$ chỉ hướng %s, điểm $C$ lệch về phía %s nên hướng từ $A$ tới $C$ là %s."
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
        debai = _de_tau(X, Y, th, d1, d2) + (r" Khoảng cách từ $A$ đến $C$ (làm tròn đến hàng đơn vị, theo "
                                             r"đơn vị ki-lô-mét) là")
        giai = _giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + r"Vậy $AC \approx %s\,\text{km}$." % dap
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
        debai = _de_tau(X, Y, th, d1, d2) + (r" Hướng từ $A$ tới $C$ (làm tròn số đo góc đến hàng đơn vị) là")
        giai = _giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + _giai_tau_huong(X, Y, th, d2, AC, phi)
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn - tàu chạy $d_1$ km về một phương rồi đổi sang hướng
    $X\,\theta^{\circ}\,Y$ chạy $d_2$ km: tính khoảng cách $AC$ (km, hàng đơn vị) - mức VD.
    Câu hỏi hướng (mức VDC) tách sang VD036_SA_O_01 (01/10/2026).

    CLAUDE THEM 30/09/2026 - dang moi theo bai co Lan gui. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        dap = str(_lt(AC))
        debai = _de_tau(X, Y, th, d1, d2) + (r" Tính khoảng cách từ $A$ đến $C$ (làm tròn đến hàng đơn vị, "
                                             r"theo đơn vị ki-lô-mét).")
        giai = _giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + r"Vậy $AC \approx %s\,\text{km}$." % dap
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_O_01(socau, dang=2):
    r"""Trả lời ngắn - tàu đổi hướng: tìm số đo $x$ trong hướng $X\,x^{\circ}\,Y$ từ $A$ tới $C$
    (côsin rồi sin) - mức VDC (muc_do_dang VDC ở mapping).

    CLAUDE THEM 01/10/2026 - tach tu nhanh hoi huong cua VD036_SA_F_01. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        X, Y, th, d1, d2, AC, phi = _bo_tau_doi_huong()
        dap = str(_lt(phi))
        debai = _de_tau(X, Y, th, d1, d2) + (r" Hướng từ $A$ tới $C$ là $\mathrm{%s}\,x^{\circ}\,\mathrm{%s}$. "
                                             r"Tìm $x$ (làm tròn đến hàng đơn vị)." % (X, Y))
        giai = (_giai_tau_AC(X, Y, th, d1, d2, AC) + "\\\\\n" + _giai_tau_huong(X, Y, th, d2, AC, phi)
                + " Vậy $x = %s$." % dap)
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
        ds = [(r"Tính khoảng cách từ $A$ đến $C$ (làm tròn đến hàng đơn vị, theo đơn vị ki-lô-mét).",
               r"AC \approx %d\,\text{km}" % _lt(AC),
               _giai_tau_AC(X, Y, th, d1, d2, AC) + r" Vậy $AC \approx %d\,\text{km}$." % _lt(AC)),
              (r"Xác định hướng từ $A$ tới $C$ (làm tròn đến hàng đơn vị, theo đơn vị độ).",
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
    return (r"Hai người quan sát tại $P$ và $Q$ đứng trên sườn của một ngọn đồi có độ nghiêng $%s$ so với mặt "
            r"phẳng ngang, như hình. Người quan sát tại $P$ nhìn một chiếc khinh khí cầu (điểm $O$) dưới một góc "
            r"$%s$ so với phương nằm ngang. Cùng lúc đó, người quan sát tại $Q$ nhìn khinh khí cầu này dưới một "
            r"góc $%s$ so với phương nằm ngang. Biết rằng $P$ và $Q$ cách nhau $%d\,\text{m}$ dọc theo sườn đồi."
            % (_goc(s), _goc(a), _goc(b), d))


def _giai_goc_khinh_khi_cau(s, a, b):
    return (r"Gọi $A$ là giao điểm của đường thẳng $PQ$ với đường nằm ngang, $P'$ là giao điểm của $OP$ với "
            r"đường nằm ngang. Góc ngoài của tam giác $APP'$: $\widehat{OPQ} = %s - %s = %s$." % (
                _goc(a), _goc(s), _goc(a - s)) + "\\\\\n" +
            r"Tương tự, $\widehat{OQP} = 180^{\circ} - \left(%s - %s\right) = %s$." % (_goc(b), _goc(s), _goc(180 - b + s))
            + "\\\\\n" + r"Do đó $\widehat{POQ} = 180^{\circ} - %s - %s = %s$." % (_goc(a - s), _goc(180 - b + s), _goc(b - a)))


def _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc):
    if tu == "P":
        return (r"Định lí sin trong tam giác $OPQ$: $OP = \dfrac{PQ\cdot\sin\widehat{OQP}}{\sin\widehat{POQ}} = "
                r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (d, _goc(180 - b + s), _goc(b - a), _xx(kc, 2)))
    return (r"Định lí sin trong tam giác $OPQ$: $OQ = \dfrac{PQ\cdot\sin\widehat{OPQ}}{\sin\widehat{POQ}} = "
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
        debai = (_de_khinh_khi_cau(s, a, b, d) + r" Khoảng cách từ $%s$ đến khinh khí cầu (đơn vị mét, làm tròn "
                 r"đến hàng đơn vị) là" % tu)
        giai = (_giai_goc_khinh_khi_cau(s, a, b) + "\\\\\n" + _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_khinh_khi_cau(s, d), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_H_01(socau, dang=2):
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
        debai = (_de_khinh_khi_cau(s, a, b, d) + r" Tính khoảng cách từ $%s$ đến khinh khí cầu (đơn vị mét, làm "
                 r"tròn đến hàng đơn vị)." % tu)
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
        ds = [(r"Tính số đo các góc của tam giác $OPQ$.",
               r"\widehat{OPQ} = %s,\ \widehat{OQP} = %s,\ \widehat{POQ} = %s" % (_goc(a - s), _goc(180 - b + s), _goc(b - a)),
               _giai_goc_khinh_khi_cau(s, a, b)),
              (r"Tính khoảng cách từ $%s$ đến khinh khí cầu (đơn vị mét, làm tròn đến hàng đơn vị)." % tu,
               r"O%s \approx %d\,\text{m}" % (tu, _lt(kc)),
               _giai_kc_khinh_khi_cau(tu, s, a, b, d, kc) + r" Vậy khoảng cách khoảng $%d\,\text{m}$." % _lt(kc))]
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
    return _x1(x), " (làm tròn đến hàng phần mười)"


def _heron_mot():
    a, b, c, S, p = random.choice(HERON_NGUYEN)
    ds = [a, b, c]
    random.shuffle(ds)
    return ds[0], ds[1], ds[2], S, p


_TEN_CANH = [("a", "b", "c", "A", "B", "C"), ("b", "c", "a", "B", "C", "A"), ("c", "a", "b", "C", "A", "B")]


def L10_C3_B6_TH032_MC_F_01(socau, dang=1):
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
        debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$ và $m_{%s}$ là độ dài đường trung tuyến "
                 r"kẻ từ đỉnh $%s$. Công thức nào sau đây đúng?" % (x, X))
        giai = (r"Công thức độ dài đường trung tuyến: $m_{%s}^{2} = \dfrac{%s^{2} + %s^{2}}{2} - \dfrac{%s^{2}}{4}"
                r" = \dfrac{2\left(%s^{2} + %s^{2}\right) - %s^{2}}{4}$." % (x, y, z, x, y, z, x))
        cau += MC_SA_answer_text(debai, dung, random.sample(sai, 3), giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH032_MC_F_02(socau, dang=1):
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
        debai = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$; $m_a$, $m_b$, $m_c$ lần lượt là độ dài các "
                 r"đường trung tuyến kẻ từ $A$, $B$, $C$. Hệ thức nào sau đây \textbf{sai}?")
        giai = (r"Theo công thức đường trung tuyến $m_{a}^{2} = \dfrac{2\left(b^{2} + c^{2}\right) - a^{2}}{4}$ "
                r"(tương tự cho $m_b$, $m_c$); cộng ba đẳng thức được "
                r"$m_{a}^{2} + m_{b}^{2} + m_{c}^{2} = \dfrac{3}{4}\left(a^{2} + b^{2} + c^{2}\right)$. "
                r"Vậy hệ thức sai là %s." % sai)
        cau += MC_SA_answer_text(debai, sai, random.sample(dung_ds, 3), giai, 0, 0, dang)
    return cau


_CT_BAN_KINH_DUNG = [r"$S = \dfrac{abc}{4R}$", r"$S = pr$", r"$S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$",
                     r"$R = \dfrac{abc}{4S}$", r"$r = \dfrac{S}{p}$", r"$S = \dfrac{1}{2}a\cdot h_a$"]
_CT_BAN_KINH_SAI = [r"$S = \dfrac{abc}{2R}$", r"$S = 2pr$", r"$S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}$",
                    r"$R = \dfrac{4S}{abc}$", r"$r = \dfrac{p}{S}$", r"$S = a\cdot h_a$", r"$S = \dfrac{abc}{4r}$",
                    r"$S = \left(p - a\right)\left(p - b\right)\left(p - c\right)$"]
_CAC_KI_HIEU = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$, diện tích $S$, nửa chu vi $p$, đường cao "
                r"$h_a$ kẻ từ $A$; $R$, $r$ lần lượt là bán kính đường tròn ngoại tiếp, nội tiếp tam giác.")


def L10_C3_B6_TH034_MC_G_01(socau, dang=1):
    r"""Lí thuyết - chọn công thức ĐÚNG về diện tích và bán kính ($S = \dfrac{abc}{4R}$,
    $S = pr$, Heron, $R = \dfrac{abc}{4S}$, $r = \dfrac{S}{p}$).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan ("hoi cac cong thuc"). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        dung = random.choice(_CT_BAN_KINH_DUNG)
        debai = _CAC_KI_HIEU + " Công thức nào sau đây đúng?"
        giai = (r"Các công thức: $S = \dfrac{1}{2}a\cdot h_a = \dfrac{abc}{4R} = pr = "
                r"\sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$, suy ra $R = \dfrac{abc}{4S}$, "
                r"$r = \dfrac{S}{p}$. Vậy công thức đúng là %s." % dung)
        cau += MC_SA_answer_text(debai, dung, random.sample(_CT_BAN_KINH_SAI, 3), giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_MC_G_02(socau, dang=1):
    r"""Lí thuyết - cách hỏi khác của _01: chọn công thức SAI (ba phương án đúng).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH034_MC_G. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        sai = random.choice(_CT_BAN_KINH_SAI)
        debai = _CAC_KI_HIEU + r" Công thức nào sau đây \textbf{sai}?"
        giai = (r"Các công thức đúng: $S = \dfrac{1}{2}a\cdot h_a = \dfrac{abc}{4R} = pr = "
                r"\sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}$, $R = \dfrac{abc}{4S}$, "
                r"$r = \dfrac{S}{p}$. Vậy công thức sai là %s." % sai)
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
        de = (r"Cho tam giác $ABC$ có $AB = %d$, $BC = %d$, $\widehat{ABC} = %s$. Gọi $M$ là trung điểm của $BC$."
              % (c, 2 * k, _goc(B)))
        hoi, dap = r"độ dài đường trung tuyến $AM$", m_
        giai = (r"$M$ là trung điểm $BC$ nên $BM = %d$. Trong tam giác $ABM$, theo định lí côsin: "
                r"$AM^{2} = AB^{2} + BM^{2} - 2\cdot AB\cdot BM\cdot\cos %s = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot %s "
                r"= %d$, nên $AM = %d$." % (k, _goc(B), c, k, c, k, "\\dfrac{1}{2}" if B == 60 else "\\left(-\\dfrac{1}{2}\\right)",
                                          m_ * m_, m_))
        sai = [round(math.sqrt(c * c + 4 * k * k - 2 * c * 2 * k * math.cos(math.radians(B)))), m_ + 1, 2 * m_,
               round(math.sqrt(c * c + k * k)) ]
        return de, hoi, dap, giai, sai
    AB, AD, BD = _bo_phan_giac()
    de = (r"Cho tam giác $ABC$ có $\widehat{BAC} = 120^{\circ}$, $AB = %d$. Đường phân giác trong của góc $A$ cắt "
          r"$BC$ tại $D$ và $AD = %d$." % (AB, AD))
    hoi, dap = r"độ dài đoạn thẳng $BD$", BD
    giai = (r"$AD$ là phân giác nên $\widehat{BAD} = \dfrac{120^{\circ}}{2} = 60^{\circ}$. Trong tam giác $ABD$, theo "
            r"định lí côsin: $BD^{2} = AB^{2} + AD^{2} - 2\cdot AB\cdot AD\cdot\cos 60^{\circ} = %d^{2} + %d^{2} - %d\cdot %d "
            r"= %d$, nên $BD = %d$." % (AB, AD, AB, AD, BD * BD, BD))
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
        cau += MC_SA_answer_const(de + r" Tính %s." % hoi, str(dap), nhieu, giai, 0, 0, dang)
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
        cau += MC_SA_answer_const(de + r" Tính %s." % hoi, str(dap), nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH035_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - giải tam giác nhỏ với đường TRUNG TUYẾN (như TH035_MC_D_01).

    CLAUDE THEM 30/09/2026 - dang moi theo co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, hoi, dap, giai, sai = _de_tam_giac_nho(1)
        cau += MC_SA_answer_const(de + r" Tính %s." % hoi, str(dap), [str(dap + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH035_SA_C_02(socau, dang=2):
    r"""Trả lời ngắn - giải tam giác nhỏ với đường PHÂN GIÁC (như TH035_MC_D_02).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH035_SA_C. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, hoi, dap, giai, sai = _de_tam_giac_nho(2)
        cau += MC_SA_answer_const(de + r" Tính %s." % hoi, str(dap), [str(dap + k) for k in (1, -1, 2)], giai, 0, 0, dang)
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
            de = r"Cho tam giác $ABC$ có $BC = %d$ và đường cao kẻ từ $A$ là $h_a = %s$." % (a, _so_gon(h))
            giai = r"$S = \dfrac{1}{2}BC\cdot h_a = \dfrac{1}{2}\cdot %d\cdot %s = %d$." % (a, _so_gon(h), S)
            return de, S, giai, [a * h, S * 2, S // 2 if S % 2 == 0 else S + 3]
        if kieu == "R":
            R = Rational(a * b * c, 4 * S)
            de = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$ và bán kính đường tròn ngoại tiếp "
                  r"$R = %s$." % (a, b, c, _so_gon(R)))
            giai = (r"$S = \dfrac{abc}{4R} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %s} = %d$." % (a, b, c, _so_gon(R), S))
            return de, S, giai, [2 * S, S * 4, round(a * b * c / float(R))]
        if kieu == "r":
            r_ = Rational(S, p)
            if _so_thap_phan_gon(r_) is None:
                continue
            de = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$ và bán kính đường tròn nội tiếp $r = %s$."
                  % (a, b, c, _so_gon(r_)))
            giai = (r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d$, nên $S = pr = %d\cdot %s = %d$."
                    % (a, b, c, p, p, _so_gon(r_), S))
            return de, S, giai, [2 * S, (a + b + c) * r_ * 2, S + p]
        de = r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$." % (a, b, c)
        giai = (r"Nửa chu vi $p = %d$. Công thức Heron: $S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d$."
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
        cau += MC_SA_answer_const(de + " Diện tích tam giác $ABC$ bằng", str(S), nhieu,
                                  giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_C_01(socau, dang=2):
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
        cau += MC_SA_answer_const(de + " Tính diện tích tam giác $ABC$.", str(S), [str(S + k) for k in (1, -1, 2)],
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
            de = (r"Cho tam giác $ABC$ có diện tích $S = %d$ và chu vi bằng $%d$. Bán kính $r$ của đường tròn nội tiếp "
                  r"tam giác $ABC$" % (S, 2 * p))
            giai = r"Nửa chu vi $p = %d$, nên $r = \dfrac{S}{p} = \dfrac{%d}{%d} = %s$." % (p, S, p, _so_thap_phan_gon(r_))
            return de, r_, giai, [Rational(S, 2 * p), Rational(2 * S, p), Rational(p, S)]
        R = Rational(a * b * c, 4 * S)
        if _so_thap_phan_gon(R) is None:
            continue
        de = (r"Cho tam giác $ABC$ có $BC = %d$, $CA = %d$, $AB = %d$ và diện tích $S = %d$. Bán kính $R$ của đường "
              r"tròn ngoại tiếp tam giác $ABC$" % (a, b, c, S))
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
        cau += MC_SA_answer_const(de + " bằng", dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_TH034_SA_D_01(socau, dang=2):
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
        cau += MC_SA_answer_const(de.replace("Bán kính", "Tính bán kính") + ".", dap,
                                  [_so_gon(v + k) for k in (1, -1, 2)], giai, 0, 0, dang)
    return cau


# ---- VD036 (VD): mảnh vườn tam giác, Heron rồi suy ra r, R hoặc đường cao ----
_HOI_VUON = {
    "r": (r"Người ta đặt một vòi phun nước tự động tại tâm đường tròn nội tiếp tam giác $ABC$ để tưới "
          r"được phần vườn hình tròn lớn nhất mà nước không phun ra ngoài bờ. Tính khoảng cách từ vòi phun đến "
          r"mỗi bờ vườn (đơn vị mét%s)."),
    "R": (r"Người ta dựng một cột đèn tại điểm cách đều ba góc vườn $A$, $B$, $C$. Tính khoảng cách từ cột đèn "
          r"đến mỗi góc vườn (đơn vị mét%s)."),
    "h": (r"Người ta làm một lối đi thẳng ngắn nhất từ góc $A$ tới bờ $BC$. Tính độ dài lối đi đó "
          r"(đơn vị mét%s)."),
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
        de = (r"Một mảnh vườn hình tam giác $ABC$ có $BC = %d\,\text{m}$, $CA = %d\,\text{m}$, $AB = %d\,\text{m}$. "
              % (a, b, c) + _HOI_VUON[hoi] % (", làm tròn đến hàng phần mười" if lam_tron else ""))
        giai = (r"Nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %d$. Công thức Heron: "
                r"$S = \sqrt{%d\cdot %d\cdot %d\cdot %d} = %d\,\left(\text{m}^{2}\right)$.\\ " % (a, b, c, p, p, p - a, p - b, p - c, S))
        giai += {"r": r"Khoảng cách cần tìm là bán kính đường tròn nội tiếp: $r = \dfrac{S}{p} = \dfrac{%d}{%d}" % (S, p),
                 "R": r"Điểm cách đều ba đỉnh là tâm đường tròn ngoại tiếp: $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %d}" % (a, b, c, S),
                 "h": r"Lối đi ngắn nhất là đường cao $h_a$: $S = \dfrac{1}{2}BC\cdot h_a$ nên $h_a = \dfrac{2S}{BC} = \dfrac{2\cdot %d}{%d}" % (S, a)}[hoi]
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
        cau += MC_SA_answer_const(de.replace("Tính khoảng", "Khoảng").replace("Tính độ dài", "Độ dài").rstrip(".") + " là",
                                  dap, [x.replace(",0", "") for x in nhieu], giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_I_01(socau, dang=2):
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
        de = (r"Một mảnh vườn hình tam giác $ABC$ có $AB = %d\,\text{m}$, $AC = %d\,\text{m}$ và góc $\widehat{BAC} = %s$. "
              r"Người ta đặt một vòi phun nước tự động tại tâm đường tròn nội tiếp tam giác $ABC$. Tính khoảng cách "
              r"từ vòi phun đến mỗi bờ vườn (đơn vị mét, làm tròn đến hàng phần mười)." % (c, b, _goc(A)))
        giai = (r"Định lí côsin: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s = %d$, nên $BC = %d$.\\ "
                r"Diện tích $S = \dfrac{1}{2}AB\cdot AC\cdot\sin %s = %s\sqrt{3}$; nửa chu vi $p = %s$.\\ "
                r"Khoảng cách cần tìm là $r = \dfrac{S}{p} = \dfrac{%s\sqrt{3}}{%s} \approx %s\,\text{m}$."
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
        cau += MC_SA_answer_const(de.replace("Tính khoảng", "Khoảng").rstrip(".") + " là", dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C3_B6_VD036_SA_J_01(socau, dang=2):
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
        de = (r"Một mảnh vườn hình tam giác $ABC$ có $AB = %d\,\text{m}$, $AC = %d\,\text{m}$ và góc $\widehat{BAC} = %s$."
              % (c, b, _goc(A)))
        cau_b = (r"Người ta đặt một vòi phun nước tự động tại tâm đường tròn nội tiếp tam giác $ABC$. Tính khoảng cách "
                 r"từ vòi phun đến mỗi bờ vườn" if hoi == "r" else
                 r"Người ta dựng một cột đèn tại điểm cách đều ba góc vườn. Tính khoảng cách từ cột đèn đến mỗi góc vườn")
        giai_b = (r"Diện tích $S = \dfrac{1}{2}AB\cdot AC\cdot\sin %s = %s\sqrt{3}\,\text{m}^{2}$. " % (_goc(A), _so_gon(Rational(b * c, 4))))
        giai_b += (r"Nửa chu vi $p = %s$, khoảng cách cần tìm là $r = \dfrac{S}{p} %s %s\,\text{m}$."
                   % (_so_gon(Rational(a + b + c, 2)), r"\approx" if lam_tron else "=", dap) if hoi == "r" else
                   r"Khoảng cách cần tìm là $R = \dfrac{abc}{4S} = \dfrac{%d\cdot %d\cdot %d}{4\cdot %s\sqrt{3}} %s %s\,\text{m}$."
                   % (a, b, c, _so_gon(Rational(b * c, 4)), r"\approx" if lam_tron else "=", dap))
        ds = [(r"Tính độ dài cạnh $BC$.", r"BC = %d\,\text{m}" % a,
               r"Định lí côsin: $BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\cos %s = %d$, nên $BC = %d\,\text{m}$."
               % (c, b, c, b, _goc(A), a * a, a)),
              (cau_b + r" (đơn vị mét%s)." % (", làm tròn đến hàng phần mười" if lam_tron else ""),
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
        tach = de.index("Người ta")
        than, hoi_b = de[:tach].strip(), de[tach:]
        g_a, g_b = giai.split(r"\\ ", 1)
        S = re.search(r"= (\d+)\\,\\left", g_a).group(1)
        ds = [(r"Tính diện tích mảnh vườn.", r"S = %s\,\text{m}^{2}" % S, g_a),
              (hoi_b, r"\approx %s\,\text{m}" % dap if "làm tròn" in hoi_b else r"%s\,\text{m}" % dap, g_b)]
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
    """(h, beta, gamma, AC, CH, AH) chọn trước: góc hợp lí, đáp số không sát ranh giới làm tròn."""
    while True:
        be = random.randint(15, 45)
        ga = random.randint(be + 10, min(be + 40, 75))
        h = random.choice([20, 25, 30, 40, 50, 60, 80, 100, 120])
        AC = h * _sin_d(be) / _sin_d(ga - be)
        CH, AH = AC * _cos_d(ga), AC * _sin_d(ga)
        if CH < 10 or CH > 600 or AH > 900:
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
    return (r"Trên một ngọn đồi có một cái tháp cao $%d\,\text{m}$ (hình vẽ). Đỉnh tháp $B$ và chân tháp $C$ lần "
            r"lượt nhìn điểm $A$ ở chân đồi dưới các góc tương ứng bằng $%s$ và $%s$ so với phương thẳng đứng. "
            r"Gọi $H$ là hình chiếu vuông góc của $C$ trên mặt phẳng nằm ngang đi qua $A$." % (h, _goc(be), _goc(ga)))


def _giai_goc_thap_doi(be, ga):
    return (r"Theo đề: $\widehat{ABC} = %s$ (góc giữa $BA$ và phương thẳng đứng $BH$); $\widehat{ACH} = %s$ nên "
            r"$\widehat{ACB} = 180^{\circ} - %s = %s$; do đó $\widehat{BAC} = 180^{\circ} - %s - %s = %s$."
            % (_goc(be), _goc(ga), _goc(ga), _goc(180 - ga), _goc(be), _goc(180 - ga), _goc(ga - be)))


def _giai_ac_thap_doi(h, be, ga, AC):
    return (r"Định lí sin trong tam giác $ABC$: $AC = \dfrac{BC\cdot\sin\widehat{ABC}}{\sin\widehat{BAC}} = "
            r"\dfrac{%d\cdot\sin %s}{\sin %s} \approx %s\,\text{m}$." % (h, _goc(be), _goc(ga - be), _xx(AC, 2)))


def _giai_hoi_thap_doi(hoi, ga, AC, gt):
    if hoi == "CH":
        return (r"Tam giác $ACH$ vuông tại $H$: $CH = AC\cdot\cos\widehat{ACH} = AC\cdot\cos %s \approx %s\,\text{m}$."
                % (_goc(ga), _xx(gt, 2)))
    return (r"Tam giác $ACH$ vuông tại $H$: $AH = AC\cdot\sin\widehat{ACH} = AC\cdot\sin %s \approx %s\,\text{m}$."
            % (_goc(ga), _xx(gt, 2)))


_HOI_THAP = {"CH": r"chiều cao $CH$ của ngọn đồi", "AH": r"khoảng cách $AH$ từ $A$ đến chân đường thẳng đứng qua tháp"}


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
        debai = _de_thap_doi(h, be, ga) + r" Khi đó %s (làm tròn đến hàng đơn vị) xấp xỉ bằng" % _HOI_THAP[hoi]
        giai = (_giai_goc_thap_doi(be, ga) + "\\\\\n" + _giai_ac_thap_doi(h, be, ga, AC) + "\\\\\n"
                + _giai_hoi_thap_doi(hoi, ga, AC, gt))
        cau += MC_SA_answer_const(debai, dap + r"\,\text{m}", [v + r"\,\text{m}" for v in nhieu], giai,
                                  _hinh_thap_doi(h, CH, AH, be, ga), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_K_01(socau, dang=2):
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
        debai = (_de_thap_doi(h, be, ga) + r" Tính %s (đơn vị mét, làm tròn đến hàng đơn vị)." % _HOI_THAP[hoi])
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
        ds = [(r"Tính số đo các góc của tam giác $ABC$ và độ dài $AC$ (làm tròn đến hàng phần mười).",
               r"\widehat{ABC} = %s,\ \widehat{ACB} = %s,\ \widehat{BAC} = %s;\ AC \approx %s\,\text{m}"
               % (_goc(be), _goc(180 - ga), _goc(ga - be), _x1(AC)),
               _giai_goc_thap_doi(be, ga) + "\\\\\n" + _giai_ac_thap_doi(h, be, ga, AC)),
              (r"Tính %s (đơn vị mét, làm tròn đến hàng đơn vị)." % _HOI_THAP[hoi],
               r"%s \approx %d\,\text{m}" % (hoi, _lt(gt)),
               _giai_hoi_thap_doi(hoi, ga, AC, gt) + r" Vậy $%s \approx %d\,\text{m}$." % (hoi, _lt(gt)))]
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
    r"Ở tỉnh Quảng Bình (cũ) có một di tích lịch sử đặc biệt mang tên Cổng Trời (còn gọi là Cổng Trời Cha Lo), "
    r"với cảnh quan hùng vĩ gắn liền cùng những chiến công bất diệt của quân đội ta. Cổng Trời là con đường nối "
    r"Trường Sơn Đông với Trường Sơn Tây, nằm trong khu vực xã Dân Hóa, huyện Minh Hóa. Sau sắp xếp đơn vị hành "
    r"chính (từ ngày 01/7/2025), địa danh này thuộc xã Dân Hóa, tỉnh Quảng Trị.\\ "
    r"Cổng Trời đứng sừng sững hiên ngang, như nghiêng mình bảo vệ từng đoàn quân, đoàn xe chi viện cho chiến "
    r"trường miền Nam trong kháng chiến chống Mỹ cứu nước. Nơi đây được xem như là ``tọa độ lửa'' khi giặc Mỹ "
    r"điên cuồng ném bom đánh phá nhằm cắt đứt tuyến đường chi viện này. Hình bên mô tả ranh giới xã Dân Hóa cũ "
    r"thời kháng chiến. Một người sử dụng Google Maps để đo các khoảng cách như trong hình vẽ."
)


def _heron_f(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(max(p * (p - a) * (p - b) * (p - c), 0))


def _goc_tam_giac(doi, k1, k2):
    """Góc (độ) đối diện cạnh doi, kẹp giữa hai cạnh k1, k2."""
    return math.degrees(math.acos((k1 * k1 + k2 * k2 - doi * doi) / (2 * k1 * k2)))


def _bo_cong_troi():
    """(BC, CD, BD, AB, AD, S_BCD, S_ABD) - số đo THỰC TẾ đo trên Google Maps (BC = 15, CD = 20,
    BD = 20, AB = 11, AD = 10 km) chỉ xê dịch nhẹ (mỗi đoạn lệch tối đa 1 km) để đề vẫn đúng thực tế
    (cô Lan 01/10/2026); hai tam giác không dẹt, tứ giác lồi."""
    while True:
        BC, CD, BD, AB, AD = [g + random.choice([-1, 0, 0, 1]) for g in (15, 20, 20, 11, 10)]
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


def _hinh_cong_troi(BC, CD, BD, AB, AD):
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
        s += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d$ km};\n" % (nhan_doan(u, v, phia) + (d,))
    return s + "\\end{tikzpicture}"


def _giai_heron(ten, a, b, c, S):
    p = (a + b + c) / 2
    return (r"Tam giác $%s$ có nửa chu vi $p = \dfrac{%d + %d + %d}{2} = %s$, nên "
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
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi()
        S = S1 + S2
        debai = _DOAN_CONG_TROI + r" Với $S_{ABD}$ là diện tích của tam giác $ABD$. Xét tính đúng, sai của các mệnh đề sau."
        # a) NB - nhận ra hệ quả định lí côsin trong tam giác BCD
        ly_a = r"Hệ quả định lí côsin: côsin của một góc bằng tổng bình phương hai cạnh kề trừ bình phương cạnh đối, chia cho hai lần tích hai cạnh kề."
        F = r"$\cos\widehat{%s} = \dfrac{%s^{2} + %s^{2} - %s^{2}}{%s\cdot %s\cdot %s}$"
        dung, sai = [], []
        for g, k1, k2, d_ in (("DBC", "BC", "BD", "CD"), ("BCD", "BC", "CD", "BD"), ("BDC", "BD", "CD", "BC")):
            dung.append((F % (g, k1, k2, d_, "2", k1, k2), ly_a))
            sai += [(F % (g, k1, k2, d_, "1", k1, k2), ly_a), (F % (g, k1, d_, k2, "2", k1, d_), ly_a),
                    (F % (g, k1, k2, d_, "2", k1, d_), ly_a)]
        y1 = _phat_bieu([(t.replace(r"{1\cdot ", "{"), l) for t, l in dung], [(t.replace(r"{1\cdot ", "{"), l) for t, l in sai])
        # b) TH - định lí sin trong tam giác ABD (cạnh đối diện góc)
        ly_b = (r"Định lí sin trong tam giác $ABD$: cạnh $AD$ đối diện góc $\widehat{ABD}$, cạnh $AB$ đối diện góc "
                r"$\widehat{ADB}$, cạnh $BD$ đối diện góc $\widehat{BAD}$.")
        G = r"$\dfrac{%s}{\sin\widehat{%s}} = \dfrac{%s}{\sin\widehat{%s}}$"
        y2 = _phat_bieu(
            [(G % ("AD", "ABD", "AB", "ADB"), ly_b), (G % ("BD", "BAD", "AD", "ABD"), ly_b), (G % ("AB", "ADB", "BD", "BAD"), ly_b)],
            [(G % ("AD", "ADB", "AB", "ABD"), ly_b), (G % ("AD", "ABD", "BD", "ADB"), ly_b), (G % ("BD", "ABD", "AD", "BAD"), ly_b),
             (G % ("AB", "ABD", "BD", "BAD"), ly_b)])
        # c) VD - suy ra sin của góc từ công thức diện tích
        ly_c = (r"$S_{ABD} = \dfrac{1}{2}AB\cdot BD\cdot\sin\widehat{ABD} = \dfrac{1}{2}AD\cdot BD\cdot\sin\widehat{ADB} = "
                r"\dfrac{1}{2}AB\cdot AD\cdot\sin\widehat{BAD}$ (góc kẹp giữa hai cạnh).")
        H = r"$\sin\widehat{%s} = \dfrac{%sS_{ABD}}{%s\cdot %s}$"
        y3 = _phat_bieu(
            [(H % ("ABD", "2", "AB", "BD"), ly_c), (H % ("ADB", "2", "AD", "BD"), ly_c), (H % ("BAD", "2", "AB", "AD"), ly_c)],
            [(H % ("ABD", "", "AB", "BD"), ly_c), (H % ("ABD", "2", "AD", "BD"), ly_c), (H % ("ADB", "2", "AB", "BD"), ly_c),
             (H % ("BAD", "", "AB", "AD"), ly_c), (H % ("BAD", "2", "AB", "BD"), ly_c)])
        # d) VDC - ước lượng diện tích: Heron hai lần rồi cộng
        ly_d = (_giai_heron("BCD", BC, CD, BD, S1) + "\\\\ " + _giai_heron("ABD", AB, AD, BD, S2) + "\\\\ "
                r"Diện tích xã Dân Hóa cũ khoảng $S_{BCD} + S_{ABD}$.")
        y4 = _tf_gop(_tf_so(r"Ước lượng diện tích của xã Dân Hóa cũ là $%s$", S, 0, ly_d,
                            [(S1, "Chỉ tính tam giác $BCD$"), (S2, "Chỉ tính tam giác $ABD$"), (2 * S, "Nhân thừa 2")],
                            dv=r"\,\text{km}^{2}", bdt=r"Diện tích của xã Dân Hóa cũ %s $%s$"))
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], _hinh_cong_troi(BC, CD, BD, AB, AD), 0, socot)
    return cau


def L10_C3_B6_VD036_MC_J_01(socau, dang=1):
    r"""Ước lượng diện tích vùng đất tứ giác (Cổng Trời - xã Dân Hóa) chia bởi một đường chéo thành hai
    tam giác biết ba cạnh: Heron hai lần rồi cộng (có hình).

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I cua co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi()
        dap = str(_lt(S1 + S2))
        nhieu = _ba_nhieu(dap, [str(_lt(S1)), str(_lt(S2)), str(_lt(2 * (S1 + S2)))],
                          buoc=lambda t: str(_lt(S1 + S2) + 4 * t))
        debai = (_DOAN_CONG_TROI + r" Ước lượng diện tích của xã Dân Hóa cũ (làm tròn đến hàng đơn vị, đơn vị "
                 r"$\text{km}^{2}$) là")
        giai = (_giai_heron("BCD", BC, CD, BD, S1) + "\\\\\n" + _giai_heron("ABD", AB, AD, BD, S2) + "\\\\\n"
                r"Vậy diện tích khoảng $S_{BCD} + S_{ABD} \approx %s\,\text{km}^{2}$." % dap)
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_cong_troi(BC, CD, BD, AB, AD), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_L_01(socau, dang=2):
    r"""Trả lời ngắn - ước lượng diện tích vùng đất tứ giác (Cổng Trời - xã Dân Hóa) bằng Heron hai lần.

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I cua co Lan. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi()
        dap = str(_lt(S1 + S2))
        if len(dap) > 4:
            continue
        so += 1
        debai = (_DOAN_CONG_TROI + r" Ước lượng diện tích của xã Dân Hóa cũ (đơn vị $\text{km}^{2}$, làm tròn đến "
                 r"hàng đơn vị).")
        giai = (_giai_heron("BCD", BC, CD, BD, S1) + "\\\\\n" + _giai_heron("ABD", AB, AD, BD, S2) + "\\\\\n"
                r"Vậy diện tích khoảng $S_{BCD} + S_{ABD} \approx %s\,\text{km}^{2}$." % dap)
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai,
                                  _hinh_cong_troi(BC, CD, BD, AB, AD), 0, dang)
    return cau


def L10_C3_B6_VD036_TL_I_01(socau, dong=1):
    r"""Tự luận - Cổng Trời, xã Dân Hóa (có hình).
    a) (VD) Tính diện tích tam giác $BCD$ (hoặc $ABD$).
    b) (VDC) Ước lượng diện tích của xã Dân Hóa cũ (vùng tứ giác $ABCD$).

    CLAUDE THEM 01/10/2026 - dang moi theo de giua ki I cua co Lan. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        BC, CD, BD, AB, AD, S1, S2 = _bo_cong_troi()
        if random.random() < 0.5:
            ten, ba, Sa, ten2, ba2, Sb = "BCD", (BC, CD, BD), S1, "ABD", (AB, AD, BD), S2
        else:
            ten, ba, Sa, ten2, ba2, Sb = "ABD", (AB, AD, BD), S2, "BCD", (BC, CD, BD), S1
        ds = [(r"Tính diện tích tam giác $%s$ (làm tròn đến hàng phần mười, đơn vị $\text{km}^{2}$)." % ten,
               r"S_{%s} \approx %s\,\text{km}^{2}" % (ten, _x1(Sa)), _giai_heron(ten, *ba, Sa)),
              (r"Ước lượng diện tích của xã Dân Hóa cũ (làm tròn đến hàng đơn vị, đơn vị $\text{km}^{2}$).",
               r"S \approx %d\,\text{km}^{2}" % _lt(S1 + S2),
               _giai_heron(ten2, *ba2, Sb) + "\\\\ " +
               r"Diện tích xã Dân Hóa cũ khoảng $S_{BCD} + S_{ABD} \approx %s \approx %d\,\text{km}^{2}$."
               % (_xx(S1 + S2, 2), _lt(S1 + S2)))]
        cau += TL_answer_text(_DOAN_CONG_TROI, ds, _hinh_cong_troi(BC, CD, BD, AB, AD), 0, dong)
    return cau
