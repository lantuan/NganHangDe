# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 1. Hàm số lượng giác và phương trình lượng giác
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Kiến thức dùng trong tệp:

  * Đổi đơn vị: $1^{\circ} = \dfrac{\pi}{180}$ rad; hệ thức Chasles
    $\left(Ou, Ov\right) + \left(Ov, Ow\right) = \left(Ou, Ow\right) +
    k2\pi$.
  * Hệ thức cơ bản: $\sin^{2}\alpha + \cos^{2}\alpha = 1$;
    $\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha}$;
    $1 + \tan^{2}\alpha = \dfrac{1}{\cos^{2}\alpha}$.
  * Góc liên quan đặc biệt: đối nhau, bù nhau, phụ nhau, hơn kém $\pi$.
  * Công thức cộng, nhân đôi, biến đổi tích thành tổng và tổng thành
    tích.
  * Hàm số $y = \sin x$, $y = \cos x$ tuần hoàn chu kì $2\pi$;
    $y = \tan x$, $y = \cot x$ tuần hoàn chu kì $\pi$.
  * Phương trình lượng giác cơ bản:
    $\sin x = \sin\alpha \Leftrightarrow x = \alpha + k2\pi$ hoặc
    $x = \pi - \alpha + k2\pi$;
    $\cos x = \cos\alpha \Leftrightarrow x = \pm\alpha + k2\pi$;
    $\tan x = \tan\alpha \Leftrightarrow x = \alpha + k\pi$.

Số liệu chọn để ĐÁP SỐ ĐẸP: mọi góc đều là bội của $\dfrac{\pi}{6}$
hoặc $\dfrac{\pi}{4}$ nên giá trị lượng giác luôn nằm trong bảng giá trị
đặc biệt; bảng này được DỰNG TỰ ĐỘNG khi nạp tệp (đối chiếu với math)
nên không thể chép nhầm.

Bài học lớp 10 đã áp dụng: chữ tiếng Việt không nằm trần trong $...$;
không dùng **đậm**; mọi chuỗi có dấu gạch chéo đều là r"..."; mọi danh
sách phương án nhiễu đều qua _ba_nhieu1; đồ thị vẽ bằng TikZ THUẦN
(MathJax trên web không dựng được tabular).
"""
import math
import random
from fractions import Fraction

from math_type import *          # noqa: F401,F403

DAU_THAP_PHAN = ","


def _xx(x, n=2):
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _toa(x):
    """Toạ độ TikZ - luôn dùng dấu CHẤM thập phân."""
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _ba_nhieu1(dapso, ung_vien, buoc=None):
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


# ---------------------------------------------------------------------
# GÓC VIẾT THEO BỘI CỦA pi/12 (nên chứa cả pi/6 và pi/4)
# ---------------------------------------------------------------------

def _pi_ps(k, mau=12):
    r"""Viết góc $\dfrac{k\pi}{mau}$ đã rút gọn, ví dụ
    $\dfrac{\pi}{3}$, $-\dfrac{2\pi}{3}$, $\pi$, $2\pi$, $0$."""
    f = Fraction(k, mau)
    if f == 0:
        return "0"
    dau = "-" if f < 0 else ""
    f = abs(f)
    tu = "" if f.numerator == 1 else "%d" % f.numerator
    if f.denominator == 1:
        return r"%s%s\pi" % (dau, tu)
    return r"%s\dfrac{%s\pi}{%d}" % (dau, tu, f.denominator)


# Bảng giá trị lượng giác đặc biệt, DỰNG TỰ ĐỘNG rồi đối chiếu với math
# nên không thể chép nhầm.
_GOC_TRI = [(0.0, "0"), (0.5, r"\dfrac{1}{2}"),
            (math.sqrt(2) / 2, r"\dfrac{\sqrt{2}}{2}"),
            (math.sqrt(3) / 2, r"\dfrac{\sqrt{3}}{2}"), (1.0, "1")]
_TAN_TRI = [(0.0, "0"), (math.sqrt(3) / 3, r"\dfrac{\sqrt{3}}{3}"),
            (1.0, "1"), (math.sqrt(3), r"\sqrt{3}")]

def _chon_chi_muc(n, socau):
    r"""Chọn socau chỉ mục trong 0..n-1, KHÔNG trùng nhau chừng nào còn
    đủ; hết mẫu thì quay vòng (tránh vòng lặp vô hạn khi socau > n)."""
    ds = []
    while len(ds) < socau:
        thieu = socau - len(ds)
        ds += random.sample(range(n), min(n, thieu))
    return ds


def _dep(x, bang):
    r"""Trả về chuỗi LaTeX của $x$ nếu $x$ nằm trong bảng đặc biệt."""
    for v, s in bang:
        if abs(abs(x) - v) < 1e-9:
            if abs(x) < 1e-12:
                return "0"
            return ("-" + s) if x < 0 else s
    return None


def _sin_dep(k, mau=12):
    return _dep(math.sin(k * math.pi / mau), _GOC_TRI)


def _cos_dep(k, mau=12):
    return _dep(math.cos(k * math.pi / mau), _GOC_TRI)


def _tan_dep(k, mau=12):
    c = math.cos(k * math.pi / mau)
    if abs(c) < 1e-12:
        return None
    return _dep(math.tan(k * math.pi / mau), _TAN_TRI)


# Các bội của pi/12 mà cả sin lẫn cos đều "đẹp" (tức bội của pi/6 hoặc
# pi/4) - dựng tự động, không gõ tay.
GOC_DEP = [k for k in range(-24, 25)
           if _sin_dep(k) is not None and _cos_dep(k) is not None]


# =====================================================================
# BÀI 1. GIÁ TRỊ LƯỢNG GIÁC CỦA GÓC LƯỢNG GIÁC
# =====================================================================

def L11_C1_B1_NB001_MC_A_01(socau, dang=1):
    r"""Nhận biết khái niệm góc lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([k for k in GOC_DEP if 0 < k < 24])
        if k not in gt:
            gt.append(k)

    cauTN = ""
    for k in gt:
        a = _pi_ps(k)
        dung = r"$%s + k2\pi,\ k \in \mathbb{Z}$" % a
        nhieu = _ba_nhieu1(
            dung,
            [r"$%s + k\pi,\ k \in \mathbb{Z}$" % a,
             r"$%s + k\dfrac{\pi}{2},\ k \in \mathbb{Z}$" % a,
             r"$%s$" % a],
            buoc=lambda t: r"$%s + k%d\pi,\ k \in \mathbb{Z}$" % (a, t + 2))
        debai = (r"Cho góc lượng giác $\left(Ou, Ov\right)$ có số đo "
                 r"$%s$. Số đo của các góc lượng giác có cùng tia đầu "
                 r"$Ou$ và tia cuối $Ov$ là" % a)
        giai = (r"Hai góc lượng giác có cùng tia đầu và tia cuối thì khác "
                r"nhau một số nguyên lần một VÒNG tròn." +
                "\\\\\n"
                r"Một vòng tròn ứng với $2\pi$ (hay $360^{\circ}$)." +
                "\\\\\n"
                r"Vậy số đo của chúng là $%s + k2\pi$ với "
                r"$k \in \mathbb{Z}$." % a +
                "\\\\\n"
                r"Chú ý là $k2\pi$ chứ không phải $k\pi$: cộng thêm $\pi$ "
                r"chỉ mới đi được NỬA vòng, tia cuối sẽ đổi hướng.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B1_NB002_MC_A_01(socau, dang=1):
    r"""Đổi số đo góc giữa độ và radian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([k for k in GOC_DEP if 0 < k <= 24])
        if k not in gt:
            gt.append(k)

    cauTN = ""
    for k in gt:
        do = k * 180 // 12
        rad = _pi_ps(k)
        dung = "$%s$" % rad
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$" % _pi_ps(k, 6), "$%s$" % _pi_ps(k, 24),
             "$%s$" % _pi_ps(do, 12)],
            buoc=lambda t: "$%s$" % _pi_ps(k + t, 12))
        debai = r"Đổi số đo góc $%d^{\circ}$ sang radian." % do
        giai = (r"Vì $180^{\circ}$ tương ứng với $\pi$ rad nên "
                r"$1^{\circ} = \dfrac{\pi}{180}$ rad." +
                "\\\\\n"
                r"$%d^{\circ} = %d\cdot\dfrac{\pi}{180} = "
                r"\dfrac{%d\pi}{180} = %s$."
                % (do, do, do, rad) +
                "\\\\\n"
                r"Kiểm lại: $%s$ tương ứng với "
                r"$%s\cdot\dfrac{180}{\pi} = %d^{\circ}$."
                % (rad, rad, do))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B1_NB004_MC_A_01(socau, dang=1):
    r"""Đường tròn lượng giác - xác định góc phần tư.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    TEN = {1: "thứ nhất", 2: "thứ hai", 3: "thứ ba", 4: "thứ tư"}
    gt = []
    while len(gt) < socau:
        k = random.choice([k for k in GOC_DEP
                           if 0 < k < 24 and k % 6 != 0])
        if k not in gt:
            gt.append(k)

    cauTN = ""
    for k in gt:
        s = math.sin(k * math.pi / 12)
        c = math.cos(k * math.pi / 12)
        pt = 1 if (c > 0 and s > 0) else (2 if (c < 0 and s > 0)
                                          else (3 if (c < 0 and s < 0)
                                                else 4))
        dung = "Góc phần tư %s" % TEN[pt]
        nhieu = [("Góc phần tư %s" % TEN[t]) for t in (1, 2, 3, 4)
                 if t != pt]
        debai = (r"Trên đường tròn lượng giác, điểm biểu diễn góc lượng "
                 r"giác có số đo $%s$ thuộc góc phần tư nào?" % _pi_ps(k))
        giai = (r"Ta có $\sin\alpha = %s$ và $\cos\alpha = %s$."
                % (_sin_dep(k), _cos_dep(k)) +
                "\\\\\n"
                r"Dấu của hoành độ (là $\cos$) và tung độ (là $\sin$) cho "
                r"biết góc phần tư." +
                "\\\\\n"
                r"Ở đây $\cos\alpha %s 0$ và $\sin\alpha %s 0$ nên điểm "
                r"biểu diễn nằm ở góc phần tư %s."
                % (">" if c > 0 else "<", ">" if s > 0 else "<", TEN[pt]))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B1_NB005_MC_A_01(socau, dang=1):
    r"""Nhận biết dấu của các giá trị lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    KHOANG = [
        (r"0 < \alpha < \dfrac{\pi}{2}", 1),
        (r"\dfrac{\pi}{2} < \alpha < \pi", 2),
        (r"\pi < \alpha < \dfrac{3\pi}{2}", 3),
        (r"\dfrac{3\pi}{2} < \alpha < 2\pi", 4),
    ]
    DAU_SIN = {1: "+", 2: "+", 3: "-", 4: "-"}
    DAU_COS = {1: "+", 2: "-", 3: "-", 4: "+"}
    gt = []
    while len(gt) < socau:
        i = random.randrange(4)
        ham = random.choice(["\\sin", "\\cos"])
        if (i, ham) not in gt:
            gt.append((i, ham))

    cauTN = ""
    for i, ham in gt:
        mo_ta, pt = KHOANG[i]
        dau = DAU_SIN[pt] if ham == "\\sin" else DAU_COS[pt]
        ten = "dương" if dau == "+" else "âm"
        dung = r"$%s\alpha$ mang dấu %s" % (ham, ten)
        khac = "\\cos" if ham == "\\sin" else "\\sin"
        nhieu = [r"$%s\alpha$ mang dấu %s"
                 % (ham, "âm" if ten == "dương" else "dương"),
                 r"$%s\alpha = 0$" % ham,
                 r"$%s\alpha$ và $%s\alpha$ luôn cùng dấu" % (ham, khac)]
        debai = (r"Cho góc lượng giác $\alpha$ thoả mãn $%s$. Khẳng định "
                 r"nào sau đây ĐÚNG?" % mo_ta)
        giai = (r"Góc $\alpha$ nằm ở góc phần tư thứ %d của đường tròn "
                r"lượng giác." % pt +
                "\\\\\n"
                r"Ở góc phần tư đó, hoành độ ($\cos$) mang dấu $%s$ và "
                r"tung độ ($\sin$) mang dấu $%s$."
                % (DAU_COS[pt], DAU_SIN[pt]) +
                "\\\\\n"
                r"Vậy $%s\alpha$ mang dấu %s." % (ham, ten))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B1_NB006_MC_A_01(socau, dang=1):
    r"""Bảng giá trị lượng giác của một số góc đặc biệt.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([k for k in GOC_DEP if 0 < k < 24])
        ham = random.choice(["\\sin", "\\cos"])
        if (k, ham) not in gt:
            gt.append((k, ham))

    cauTN = ""
    for k, ham in gt:
        gt_sin, gt_cos = _sin_dep(k), _cos_dep(k)
        dung_tri = gt_sin if ham == "\\sin" else gt_cos
        khac_tri = gt_cos if ham == "\\sin" else gt_sin
        dung = "$%s$" % dung_tri
        # KHONG doi dau cua so 0 (tranh phuong an "-0")
        if dung_tri == "0":
            doi_dau = "1"
        elif dung_tri.startswith("-"):
            doi_dau = dung_tri[1:]
        else:
            doi_dau = "-" + dung_tri
        ung_vien = ["$%s$" % khac_tri, "$%s$" % doi_dau]
        ung_vien += ["$%s$" % v for _, v in _GOC_TRI[1:]]
        ung_vien += ["$-%s$" % v for _, v in _GOC_TRI[1:]]
        nhieu = _ba_nhieu1(dung, ung_vien,
                           buoc=lambda t: "$%s$" % _GOC_TRI[t % 5][1])
        debai = r"Tính $%s%s$." % (ham, _pi_ps(k))
        giai = (r"Góc $%s$ có điểm biểu diễn trên đường tròn lượng giác "
                r"với $\cos = %s$ và $\sin = %s$."
                % (_pi_ps(k), gt_cos, gt_sin) +
                "\\\\\n"
                r"Tra bảng giá trị lượng giác đặc biệt: $%s%s = %s$."
                % (ham, _pi_ps(k), dung_tri))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# Bộ ba Pytago để sin, cos đều là phân số hữu tỉ ĐẸP.
PYTAGO1 = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13),
           (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25),
           (20, 21, 29), (21, 20, 29)]


def _ps1(p, q):
    r"""Phân số tối giản dạng LaTeX."""
    f = Fraction(p, q)
    if f.denominator == 1:
        return "%d" % f.numerator
    if f < 0:
        return r"-\dfrac{%d}{%d}" % (-f.numerator, f.denominator)
    return r"\dfrac{%d}{%d}" % (f.numerator, f.denominator)


def L11_C1_B1_TH003_MC_A_01(socau, dang=1):
    r"""Hệ thức Chasles cho các góc lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k1 = random.choice([k for k in GOC_DEP if 0 < k < 12])
        k2 = random.choice([k for k in GOC_DEP if 0 < k < 12])
        if (k1, k2) not in gt:
            gt.append((k1, k2))

    cauTN = ""
    for k1, k2 in gt:
        tong = _pi_ps(k1 + k2)
        dung = r"$%s + k2\pi,\ k \in \mathbb{Z}$" % tong
        nhieu = _ba_nhieu1(
            dung,
            [r"$%s + k2\pi,\ k \in \mathbb{Z}$" % _pi_ps(k1 - k2),
             r"$%s + k2\pi,\ k \in \mathbb{Z}$" % _pi_ps(k2 - k1),
             r"$%s$" % tong],
            buoc=lambda t: r"$%s + k2\pi,\ k \in \mathbb{Z}$"
            % _pi_ps(k1 + k2 + t))
        debai = (r"Cho ba tia $Ou$, $Ov$, $Ow$ với "
                 r"$\left(Ou, Ov\right) = %s$ và "
                 r"$\left(Ov, Ow\right) = %s$. Số đo của góc lượng giác "
                 r"$\left(Ou, Ow\right)$ là"
                 % (_pi_ps(k1), _pi_ps(k2)))
        giai = (r"Hệ thức Chasles: $\left(Ou, Ov\right) + "
                r"\left(Ov, Ow\right) = \left(Ou, Ow\right) + k2\pi$ với "
                r"$k \in \mathbb{Z}$." +
                "\\\\\n"
                r"$\left(Ou, Ow\right) = %s + %s + k2\pi = %s + k2\pi$."
                % (_pi_ps(k1), _pi_ps(k2), tong) +
                "\\\\\n"
                r"Phải có $k2\pi$ vì góc lượng giác chỉ xác định sai khác "
                r"một số nguyên lần một vòng.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B1_TH007_MC_A_01(socau, dang=1):
    r"""Hệ thức cơ bản giữa các giá trị lượng giác của một góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    KHOANG = [
        (r"0 < \alpha < \dfrac{\pi}{2}", 1, 1),
        (r"\dfrac{\pi}{2} < \alpha < \pi", -1, 1),
        (r"\pi < \alpha < \dfrac{3\pi}{2}", -1, -1),
        (r"\dfrac{3\pi}{2} < \alpha < 2\pi", 1, -1),
    ]
    gt = []
    while len(gt) < socau:
        s, c, h = random.choice(PYTAGO1)
        i = random.randrange(4)
        if (s, c, h, i) not in gt:
            gt.append((s, c, h, i))

    cauTN = ""
    for s, c, h, i in gt:
        mo_ta, dau_cos, dau_sin = KHOANG[i]
        sin_a = dau_sin * s
        cos_a = dau_cos * c
        dung = "$%s$" % _ps1(cos_a, h)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$" % _ps1(-cos_a, h), "$%s$" % _ps1(sin_a, h),
             "$%s$" % _ps1(c * c, h * h)],
            buoc=lambda t: "$%s$" % _ps1(cos_a + t, h))
        debai = (r"Cho $\sin\alpha = %s$ và $%s$. Tính $\cos\alpha$."
                 % (_ps1(sin_a, h), mo_ta))
        giai = (r"Từ $\sin^{2}\alpha + \cos^{2}\alpha = 1$ suy ra "
                r"$\cos^{2}\alpha = 1 - \sin^{2}\alpha$." +
                "\\\\\n"
                r"$\cos^{2}\alpha = 1 - \left(%s\right)^{2} = "
                r"1 - \dfrac{%d}{%d} = \dfrac{%d}{%d}$."
                % (_ps1(sin_a, h), s * s, h * h, c * c, h * h) +
                "\\\\\n"
                r"Suy ra $\cos\alpha = \pm\dfrac{%d}{%d}$." % (c, h) +
                "\\\\\n"
                r"Vì $%s$ nên $\alpha$ ở góc phần tư %s, do đó "
                r"$\cos\alpha$ mang dấu %s."
                % (mo_ta, ("thứ nhất", "thứ hai", "thứ ba", "thứ tư")[i],
                   "dương" if dau_cos > 0 else "âm") +
                "\\\\\n"
                r"Vậy $\cos\alpha = %s$." % _ps1(cos_a, h))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# Các góc liên quan đặc biệt: (mô tả, hàm sau khi rút gọn, dấu)
LIEN_QUAN = [
    (r"\sin\left(\pi - \alpha\right)", "sin", 1, r"bù nhau"),
    (r"\cos\left(\pi - \alpha\right)", "cos", -1, r"bù nhau"),
    (r"\sin\left(-\alpha\right)", "sin", -1, r"đối nhau"),
    (r"\cos\left(-\alpha\right)", "cos", 1, r"đối nhau"),
    (r"\sin\left(\dfrac{\pi}{2} - \alpha\right)", "cos", 1, r"phụ nhau"),
    (r"\cos\left(\dfrac{\pi}{2} - \alpha\right)", "sin", 1, r"phụ nhau"),
    (r"\sin\left(\pi + \alpha\right)", "sin", -1, r"hơn kém $\pi$"),
    (r"\cos\left(\pi + \alpha\right)", "cos", -1, r"hơn kém $\pi$"),
]


def _viet_lien_quan(ham, dau):
    return r"%s\%s\alpha" % ("-" if dau < 0 else "", ham)


def L11_C1_B1_TH008_MC_A_01(socau, dang=1):
    r"""Quan hệ giữa giá trị lượng giác của các góc liên quan đặc biệt.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(len(LIEN_QUAN), socau)

    cauTN = ""
    for i in gt:
        bt, ham, dau, quan_he = LIEN_QUAN[i]
        khac = "cos" if ham == "sin" else "sin"
        dung = "$%s$" % _viet_lien_quan(ham, dau)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$" % _viet_lien_quan(ham, -dau),
             "$%s$" % _viet_lien_quan(khac, dau),
             "$%s$" % _viet_lien_quan(khac, -dau)],
            buoc=lambda t: r"$\tan\alpha$")
        debai = r"Rút gọn biểu thức $%s$." % bt
        giai = (r"Hai góc trong biểu thức là hai góc %s." % quan_he +
                "\\\\\n"
                r"Theo công thức các góc liên quan đặc biệt: "
                r"$%s = %s$." % (bt, _viet_lien_quan(ham, dau)) +
                "\\\\\n"
                r"Nhớ mẹo: với góc %s thì giá trị lượng giác %s, còn dấu "
                r"thì xét theo góc phần tư."
                % (quan_he,
                   "giữ nguyên tên hàm" if ham ==
                   ("sin" if bt.startswith(r"\sin") else "cos")
                   else "ĐỔI tên hàm (sin thành cos và ngược lại)"))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B1_TH008_SA_A_01(socau):
    r"""Rút gọn biểu thức dùng góc liên quan đặc biệt - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    # chi lay bo co mau 5 hoac 25 de 2cos(a) la so thap phan HUU HAN
    BO = [b for b in PYTAGO1 if b[2] in (5, 25)]
    gt = [BO[i] for i in _chon_chi_muc(len(BO), socau)]

    cau = ""
    for s, c, h in gt:
        # P = sin(pi/2 + a) + cos(2pi - a) = cos a + cos a = 2cos a
        P = Fraction(2 * c, h)
        dapso = _xx(P)
        debai = (r"Cho $\cos\alpha = %s$. Tính giá trị của biểu thức "
                 r"$P = \sin\left(\dfrac{\pi}{2} + \alpha\right) + "
                 r"\cos\left(2\pi - \alpha\right)$." % _ps1(c, h))
        giai = (r"$\sin\left(\dfrac{\pi}{2} + \alpha\right) = "
                r"\cos\alpha$ (hai góc phụ nhau, có thêm nửa vòng)." +
                "\\\\\n"
                r"$\cos\left(2\pi - \alpha\right) = \cos\left(-\alpha"
                r"\right) = \cos\alpha$ (bớt đúng một vòng rồi dùng góc "
                r"đối)." +
                "\\\\\n"
                r"Vậy $P = \cos\alpha + \cos\alpha = 2\cos\alpha = "
                r"2\cdot %s = %s = %s$."
                % (_ps1(c, h), _ps1(2 * c, h), dapso))
        assert (P * 100).denominator == 1
        nhieu = _ba_nhieu1(dapso,
                           [_xx(Fraction(c, h)), _xx(Fraction(-2 * c, h)),
                            "0"],
                           buoc=lambda t: _xx(float(P) + t / 10.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B1_TH009_MC_A_01(socau, dang=1):
    r"""Dùng máy tính cầm tay tính giá trị lượng giác của một góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        do = random.choice([17, 23, 28, 34, 37, 41, 52, 58, 63, 71, 76, 82])
        ham = random.choice(["sin", "cos"])
        if (do, ham) not in gt:
            gt.append((do, ham))

    cauTN = ""
    for do, ham in gt:
        r = math.radians(do)
        v = math.sin(r) if ham == "sin" else math.cos(r)
        khac = math.cos(r) if ham == "sin" else math.sin(r)
        dapso = _xx(v)
        dung = "$%s$" % dapso
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$" % _xx(khac), "$%s$" % _xx(math.tan(r)),
             "$%s$" % _xx(-v)],
            buoc=lambda t: "$%s$" % _xx(v + t / 100.0))
        debai = (r"Dùng máy tính cầm tay, tính $\%s %d^{\circ}$ (làm tròn "
                 r"đến hàng phần trăm)." % (ham, do))
        giai = (r"Chuyển máy tính về chế độ DEG (đơn vị độ)." +
                "\\\\\n"
                r"Bấm $\%s$ rồi nhập $%d$ và nhấn $=$." % (ham, do) +
                "\\\\\n"
                r"Kết quả $\%s %d^{\circ} \approx %s$." % (ham, do, dapso) +
                "\\\\\n"
                r"Nếu máy đang ở chế độ RAD thì kết quả sẽ sai hoàn toàn, "
                r"vì khi đó máy hiểu $%d$ là $%d$ radian." % (do, do))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# =====================================================================
# BÀI 2. CÔNG THỨC LƯỢNG GIÁC
# =====================================================================

KHOANG_GPT = [
    (r"0 < \alpha < \dfrac{\pi}{2}", 1, 1, "thứ nhất"),
    (r"\dfrac{\pi}{2} < \alpha < \pi", -1, 1, "thứ hai"),
    (r"\pi < \alpha < \dfrac{3\pi}{2}", -1, -1, "thứ ba"),
    (r"\dfrac{3\pi}{2} < \alpha < 2\pi", 1, -1, "thứ tư"),
]


def L11_C1_B2_TH010_MC_A_01(socau, dang=1):
    r"""Công thức cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        s1, c1, h1 = random.choice([b for b in PYTAGO1 if b[2] == 5])
        s2, c2, h2 = random.choice([b for b in PYTAGO1 if b[2] == 13])
        ham = random.choice(["sin", "cos"])
        v = (s1, c1, s2, c2, ham)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for s1, c1, s2, c2, ham in gt:
        if ham == "sin":
            tu = s1 * c2 + c1 * s2
            ct = (r"\sin\left(\alpha + \beta\right) = \sin\alpha\cos\beta "
                  r"+ \cos\alpha\sin\beta")
            khai = (r"%s\cdot %s + %s\cdot %s"
                    % (_ps1(s1, 5), _ps1(c2, 13), _ps1(c1, 5),
                       _ps1(s2, 13)))
            sai_tu = s1 * s2 + c1 * c2
        else:
            tu = c1 * c2 - s1 * s2
            ct = (r"\cos\left(\alpha + \beta\right) = \cos\alpha\cos\beta "
                  r"- \sin\alpha\sin\beta")
            khai = (r"%s\cdot %s - %s\cdot %s"
                    % (_ps1(c1, 5), _ps1(c2, 13), _ps1(s1, 5),
                       _ps1(s2, 13)))
            sai_tu = c1 * c2 + s1 * s2
        dung = "$%s$" % _ps1(tu, 65)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$" % _ps1(sai_tu, 65), "$%s$" % _ps1(-tu, 65),
             "$%s$" % _ps1(s1 * s2, 65)],
            buoc=lambda t: "$%s$" % _ps1(tu + t, 65))
        debai = (r"Cho $\sin\alpha = %s$, $\cos\alpha = %s$, "
                 r"$\sin\beta = %s$, $\cos\beta = %s$. Tính "
                 r"$\%s\left(\alpha + \beta\right)$."
                 % (_ps1(s1, 5), _ps1(c1, 5), _ps1(s2, 13),
                    _ps1(c2, 13), ham))
        giai = (r"Công thức cộng: $%s$." % ct +
                "\\\\\n"
                r"Thay số: $%s$." % khai +
                "\\\\\n"
                r"$= \dfrac{%d}{65} %s \dfrac{%d}{65} = %s$."
                % (s1 * c2 if ham == "sin" else c1 * c2,
                   "+" if ham == "sin" else "-",
                   c1 * s2 if ham == "sin" else s1 * s2, _ps1(tu, 65)) +
                "\\\\\n"
                r"Chú ý công thức của $\cos$ có dấu TRỪ ở giữa, còn của "
                r"$\sin$ có dấu CỘNG.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B2_TH010_SA_A_01(socau):
    r"""Tính giá trị biểu thức bằng công thức cộng - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chọn hai góc có $\sin$, $\cos$ mẫu $5$ nên kết quả là số thập phân
    HỮU HẠN (mẫu $25$), không phải làm tròn.
    """
    gt = []
    while len(gt) < socau:
        s1, c1, _ = random.choice([b for b in PYTAGO1 if b[2] == 5])
        s2, c2, _ = random.choice([b for b in PYTAGO1 if b[2] == 5])
        ham = random.choice(["sin", "cos"])
        v = (s1, c1, s2, c2, ham)
        if v not in gt:
            gt.append(v)

    cau = ""
    for s1, c1, s2, c2, ham in gt:
        if ham == "sin":
            tu = s1 * c2 + c1 * s2
            ct = (r"\sin\left(\alpha + \beta\right) = \sin\alpha\cos\beta "
                  r"+ \cos\alpha\sin\beta")
        else:
            tu = c1 * c2 - s1 * s2
            ct = (r"\cos\left(\alpha + \beta\right) = \cos\alpha\cos\beta "
                  r"- \sin\alpha\sin\beta")
        P = Fraction(tu, 25)
        assert (P * 100).denominator == 1
        dapso = _xx(P)
        debai = (r"Cho $\sin\alpha = %s$, $\cos\alpha = %s$, "
                 r"$\sin\beta = %s$, $\cos\beta = %s$. Tính "
                 r"$\%s\left(\alpha + \beta\right)$."
                 % (_ps1(s1, 5), _ps1(c1, 5), _ps1(s2, 5),
                    _ps1(c2, 5), ham))
        giai = (r"Công thức cộng: $%s$." % ct +
                "\\\\\n"
                r"Thay số được $\dfrac{%d}{25} = %s$." % (tu, dapso))
        nhieu = _ba_nhieu1(dapso,
                           [_xx(Fraction(-tu, 25)),
                            _xx(Fraction(s1 * s2 + c1 * c2, 25)),
                            _xx(Fraction(s1 * c2, 25))],
                           buoc=lambda t: _xx(float(P) + t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B2_TH011_MC_A_01(socau, dang=1):
    r"""Công thức góc nhân đôi.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        s, c, h = random.choice(PYTAGO1)
        i = random.randrange(4)
        ham = random.choice(["sin", "cos"])
        v = (s, c, h, i, ham)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for s, c, h, i, ham in gt:
        mo_ta, dau_cos, dau_sin, ten_pt = KHOANG_GPT[i]
        sin_a, cos_a = dau_sin * s, dau_cos * c
        if ham == "sin":
            tu = 2 * sin_a * cos_a
            mau = h * h
            ct = r"\sin 2\alpha = 2\sin\alpha\cos\alpha"
            thay = (r"2\cdot\left(%s\right)\cdot\left(%s\right)"
                    % (_ps1(sin_a, h), _ps1(cos_a, h)))
            sai = sin_a * cos_a
        else:
            tu = cos_a * cos_a - sin_a * sin_a
            mau = h * h
            ct = (r"\cos 2\alpha = \cos^{2}\alpha - \sin^{2}\alpha "
                  r"= 1 - 2\sin^{2}\alpha")
            thay = (r"1 - 2\cdot\left(%s\right)^{2}" % _ps1(sin_a, h))
            sai = 2 * cos_a * cos_a
        dung = "$%s$" % _ps1(tu, mau)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$" % _ps1(sai, mau), "$%s$" % _ps1(-tu, mau),
             "$%s$" % _ps1(2 * sin_a, h)],
            buoc=lambda t: "$%s$" % _ps1(tu + t, mau))
        debai = (r"Cho $\sin\alpha = %s$ và $%s$. Tính $\%s 2\alpha$."
                 % (_ps1(sin_a, h), mo_ta, ham))
        giai = (r"Vì $%s$ nên $\alpha$ ở góc phần tư %s, do đó "
                r"$\cos\alpha = %s$." % (mo_ta, ten_pt, _ps1(cos_a, h)) +
                "\\\\\n"
                r"Công thức nhân đôi: $%s$." % ct +
                "\\\\\n"
                r"$\%s 2\alpha = %s = %s$." % (ham, thay, _ps1(tu, mau)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B2_TH011_SA_A_01(socau):
    r"""Tính giá trị biểu thức bằng công thức góc nhân đôi - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chỉ dùng bộ Pytago mẫu $5$ nên $\sin 2\alpha$, $\cos 2\alpha$ có
    mẫu $25$, là số thập phân HỮU HẠN.
    """
    gt = []
    while len(gt) < socau:
        s, c, h = random.choice([b for b in PYTAGO1 if b[2] == 5])
        i = random.randrange(4)
        ham = random.choice(["sin", "cos"])
        v = (s, c, h, i, ham)
        if v not in gt:
            gt.append(v)

    cau = ""
    for s, c, h, i, ham in gt:
        mo_ta, dau_cos, dau_sin, ten_pt = KHOANG_GPT[i]
        sin_a, cos_a = dau_sin * s, dau_cos * c
        if ham == "sin":
            P = Fraction(2 * sin_a * cos_a, h * h)
            ct = r"\sin 2\alpha = 2\sin\alpha\cos\alpha"
            thay = (r"2\cdot\left(%s\right)\cdot\left(%s\right)"
                    % (_ps1(sin_a, h), _ps1(cos_a, h)))
        else:
            P = Fraction(cos_a * cos_a - sin_a * sin_a, h * h)
            ct = r"\cos 2\alpha = 1 - 2\sin^{2}\alpha"
            thay = (r"1 - 2\cdot\left(%s\right)^{2}"
                    % _ps1(sin_a, h))
        assert (P * 100).denominator == 1
        dapso = _xx(P)
        debai = (r"Cho $\sin\alpha = %s$ và $%s$. Tính $\%s 2\alpha$."
                 % (_ps1(sin_a, h), mo_ta, ham))
        giai = (r"Vì $%s$ nên $\cos\alpha = %s$."
                % (mo_ta, _ps1(cos_a, h)) +
                "\\\\\n"
                r"Công thức nhân đôi: $%s$." % ct +
                "\\\\\n"
                r"$\%s 2\alpha = %s = %s = %s$."
                % (ham, thay, _ps1(P.numerator, P.denominator), dapso))
        nhieu = _ba_nhieu1(dapso,
                           [_xx(-P), _xx(Fraction(sin_a, h)),
                            _xx(Fraction(cos_a, h))],
                           buoc=lambda t: _xx(float(P) + t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B2_TH012_MC_A_01(socau, dang=1):
    r"""Công thức biến đổi tích thành tổng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"2\cos\alpha\cos\beta",
         r"\cos\left(\alpha - \beta\right) + \cos\left(\alpha + \beta\right)",
         r"\cos\left(\alpha - \beta\right) - \cos\left(\alpha + \beta\right)",
         r"\sin\left(\alpha + \beta\right) + \sin\left(\alpha - \beta\right)",
         r"2\cos\left(\alpha + \beta\right)"),
        (r"2\sin\alpha\sin\beta",
         r"\cos\left(\alpha - \beta\right) - \cos\left(\alpha + \beta\right)",
         r"\cos\left(\alpha - \beta\right) + \cos\left(\alpha + \beta\right)",
         r"\sin\left(\alpha - \beta\right) - \sin\left(\alpha + \beta\right)",
         r"2\sin\left(\alpha - \beta\right)"),
        (r"2\sin\alpha\cos\beta",
         r"\sin\left(\alpha + \beta\right) + \sin\left(\alpha - \beta\right)",
         r"\sin\left(\alpha + \beta\right) - \sin\left(\alpha - \beta\right)",
         r"\cos\left(\alpha - \beta\right) + \cos\left(\alpha + \beta\right)",
         r"2\sin\left(\alpha + \beta\right)"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        bt, dung_ct, n1, n2, n3 = MAU[i]
        dung = "$%s$" % dung_ct
        debai = r"Biến đổi tích thành tổng: $%s$ bằng" % bt
        giai = (r"Công thức biến đổi tích thành tổng suy ra từ công thức "
                r"cộng." +
                "\\\\\n"
                r"Cộng (hoặc trừ) hai công thức cộng của "
                r"$\left(\alpha + \beta\right)$ và "
                r"$\left(\alpha - \beta\right)$ ta được" +
                "\\\\\n"
                r"$%s = %s$." % (bt, dung_ct) +
                "\\\\\n"
                r"Mẹo nhớ: tích hai $\cos$ và tích hai $\sin$ cho ra "
                r"TỔNG/HIỆU hai $\cos$; tích $\sin$ với $\cos$ cho ra "
                r"tổng hai $\sin$.")
        cauTN += MC_SA_answer_text(debai, dung,
                                   ["$%s$" % n1, "$%s$" % n2, "$%s$" % n3],
                                   giai, 0, 0, dang)
    return cauTN


def L11_C1_B2_TH013_MC_A_01(socau, dang=1):
    r"""Công thức biến đổi tổng thành tích.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"\sin\alpha + \sin\beta",
         r"2\sin\dfrac{\alpha + \beta}{2}\cos\dfrac{\alpha - \beta}{2}",
         r"2\cos\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}",
         r"2\sin\dfrac{\alpha - \beta}{2}\cos\dfrac{\alpha + \beta}{2}",
         r"2\sin\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}"),
        (r"\sin\alpha - \sin\beta",
         r"2\cos\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}",
         r"2\sin\dfrac{\alpha + \beta}{2}\cos\dfrac{\alpha - \beta}{2}",
         r"-2\sin\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}",
         r"2\cos\dfrac{\alpha - \beta}{2}\cos\dfrac{\alpha + \beta}{2}"),
        (r"\cos\alpha + \cos\beta",
         r"2\cos\dfrac{\alpha + \beta}{2}\cos\dfrac{\alpha - \beta}{2}",
         r"-2\sin\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}",
         r"2\sin\dfrac{\alpha + \beta}{2}\cos\dfrac{\alpha - \beta}{2}",
         r"2\cos\dfrac{\alpha - \beta}{2}\sin\dfrac{\alpha + \beta}{2}"),
        (r"\cos\alpha - \cos\beta",
         r"-2\sin\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}",
         r"2\cos\dfrac{\alpha + \beta}{2}\cos\dfrac{\alpha - \beta}{2}",
         r"2\sin\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}",
         r"-2\cos\dfrac{\alpha + \beta}{2}\sin\dfrac{\alpha - \beta}{2}"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        bt, dung_ct, n1, n2, n3 = MAU[i]
        dung = "$%s$" % dung_ct
        debai = r"Biến đổi tổng thành tích: $%s$ bằng" % bt
        giai = (r"Đặt $u = \dfrac{\alpha + \beta}{2}$ và "
                r"$v = \dfrac{\alpha - \beta}{2}$, khi đó $\alpha = u + v$ "
                r"và $\beta = u - v$." +
                "\\\\\n"
                r"Áp dụng công thức cộng cho $\alpha$ và $\beta$ rồi cộng "
                r"(hoặc trừ) hai kết quả:" +
                "\\\\\n"
                r"$%s = %s$." % (bt, dung_ct) +
                "\\\\\n"
                r"Chú ý riêng $\cos\alpha - \cos\beta$ có DẤU TRỪ đứng "
                r"trước, đây là chỗ hay nhầm nhất.")
        cauTN += MC_SA_answer_text(debai, dung,
                                   ["$%s$" % n1, "$%s$" % n2, "$%s$" % n3],
                                   giai, 0, 0, dang)
    return cauTN


def _bo_guong_nuoc():
    r"""$(a, b, T, k)$: $h(t) = a + b\sin\dfrac{2\pi t}{T}$, thời điểm
    hỏi ứng với góc $\dfrac{k\pi}{12}$ có $\sin$ nằm trong
    $\left\{0; \dfrac{1}{2}; 1\right\}$ nên $h$ luôn là số ĐẸP."""
    a = random.choice([2, 3, 4, 5])
    b = random.choice([2, 4, 6])
    T = random.choice([4, 6, 12])
    k = random.choice([2, 6, 10, 14, 18, 22])     # sin = 1/2, 1, -1/2, -1
    return a, b, T, k


def L11_C1_B2_VD014_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với giá trị lượng giác - guồng nước.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_guong_nuoc()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, T, k in gt:
        t = Fraction(k * T, 24)
        s = math.sin(k * math.pi / 12)
        h = Fraction(a) + Fraction(b) * Fraction(round(s * 2), 2)
        dung = "$%s$ mét" % _xx(h)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$ mét" % _xx(Fraction(a)),
             "$%s$ mét" % _xx(Fraction(a + b)),
             "$%s$ mét" % _xx(2 * Fraction(a) - h)],
            buoc=lambda x: "$%s$ mét" % _xx(float(h) + x))
        debai = (r"Một chiếc guồng nước quay đều. Khoảng cách từ một chiếc "
                 r"gàu đến mặt nước (tính bằng mét) ở thời điểm $t$ phút "
                 r"được cho bởi $h\left(t\right) = %d + %d"
                 r"\sin\dfrac{2\pi t}{%d}$. Tính khoảng cách đó tại thời "
                 r"điểm $t = %s$ phút."
                 % (a, b, T, _ps1(t.numerator, t.denominator)))
        giai = (r"Thay $t = %s$ vào công thức:"
                % _ps1(t.numerator, t.denominator) +
                "\\\\\n"
                r"$\dfrac{2\pi t}{%d} = \dfrac{2\pi}{%d}\cdot %s = %s$."
                % (T, T, _ps1(t.numerator, t.denominator), _pi_ps(k)) +
                "\\\\\n"
                r"$\sin %s = %s$." % (_pi_ps(k), _sin_dep(k)) +
                "\\\\\n"
                r"$h = %d + %d\cdot\left(%s\right) = %s$ (mét)."
                % (a, b, _sin_dep(k), _xx(h)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B2_VD014_SA_A_01(socau):
    r"""Giá trị lượng giác trong bài toán thực tiễn - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_guong_nuoc()
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, T, k in gt:
        t = Fraction(k * T, 24)
        s = math.sin(k * math.pi / 12)
        h = Fraction(a) + Fraction(b) * Fraction(round(s * 2), 2)
        dapso = _xx(h)
        debai = (r"Khoảng cách từ một chiếc gàu của guồng nước đến mặt "
                 r"nước (tính bằng mét) ở thời điểm $t$ phút được cho bởi "
                 r"$h\left(t\right) = %d + %d\sin\dfrac{2\pi t}{%d}$. "
                 r"Tính $h$ tại thời điểm $t = %s$ phút (đơn vị: mét)."
                 % (a, b, T, _ps1(t.numerator, t.denominator)))
        giai = (r"$\dfrac{2\pi}{%d}\cdot %s = %s$ và $\sin %s = %s$."
                % (T, _ps1(t.numerator, t.denominator), _pi_ps(k),
                   _pi_ps(k), _sin_dep(k)) +
                "\\\\\n"
                r"$h = %d + %d\cdot\left(%s\right) = %s$ (mét)."
                % (a, b, _sin_dep(k), dapso))
        nhieu = _ba_nhieu1(dapso,
                           [_xx(Fraction(a)), _xx(Fraction(a + b)),
                            _xx(2 * Fraction(a) - h)],
                           buoc=lambda x: _xx(float(h) + x))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B2_VD014_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn dùng biến đổi lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5])
        b = random.choice([2, 4, 6])
        T = random.choice([4, 6, 12])
        if (a, b, T) not in gt:
            gt.append((a, b, T))

    cauTN = ""
    for a, b, T in gt:
        t1 = Fraction(T, 4)          # goc pi/2 -> sin = 1
        t2 = Fraction(T, 12)         # goc pi/6 -> sin = 1/2
        h1 = a + b
        h2 = Fraction(a) + Fraction(b, 2)
        debai = (r"Một chiếc guồng nước quay đều. Khoảng cách từ một chiếc "
                 r"gàu đến mặt nước (tính bằng mét) ở thời điểm $t$ phút "
                 r"được cho bởi $h\left(t\right) = %d + %d"
                 r"\sin\dfrac{2\pi t}{%d}$ với $t \geq 0$." % (a, b, T))

        hoi_a = r"Tính $h\left(0\right)$ và cho biết ý nghĩa của nó."
        giai_a = (r"$h\left(0\right) = %d + %d\sin 0 = %d + 0 = %d$ (mét)."
                  % (a, b, a, a) +
                  "\\\\\n"
                  r"Đây là khoảng cách từ gàu đến mặt nước ở thời điểm bắt "
                  r"đầu quan sát.")

        hoi_b = (r"Tìm khoảng cách LỚN NHẤT và NHỎ NHẤT từ gàu đến mặt "
                 r"nước.")
        giai_b = (r"Vì $-1 \leq \sin\dfrac{2\pi t}{%d} \leq 1$ nên" % T +
                  "\\\\\n"
                  r"$%d - %d \leq h\left(t\right) \leq %d + %d$, tức là "
                  r"$%d \leq h\left(t\right) \leq %d$."
                  % (a, b, a, b, a - b, a + b) +
                  "\\\\\n"
                  r"Khoảng cách lớn nhất là $%d$ mét (khi "
                  r"$\sin\dfrac{2\pi t}{%d} = 1$), nhỏ nhất là $%d$ mét "
                  r"(khi $\sin\dfrac{2\pi t}{%d} = -1$)."
                  % (a + b, T, a - b, T))

        hoi_c = r"Tính $h$ tại thời điểm $t = %s$ phút." % \
            _ps1(t2.numerator, t2.denominator)
        giai_c = (r"$\dfrac{2\pi}{%d}\cdot %s = \dfrac{\pi}{6}$."
                  % (T, _ps1(t2.numerator, t2.denominator)) +
                  "\\\\\n"
                  r"$\sin\dfrac{\pi}{6} = \dfrac{1}{2}$ nên "
                  r"$h = %d + %d\cdot\dfrac{1}{2} = %s$ (mét)."
                  % (a, b, _xx(h2)))

        ds_abcd = [(hoi_a, r"h\left(0\right) = %d \text{ mét}" % a, giai_a),
                   (hoi_b, r"%d \leq h \leq %d" % (a - b, a + b), giai_b),
                   (hoi_c, r"h = %s \text{ mét}" % _xx(h2), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 3. HÀM SỐ LƯỢNG GIÁC VÀ ĐỒ THỊ
# =====================================================================

def _hinh_luong_giac(ham):
    r"""Đồ thị $y = \sin x$, $y = \cos x$ hoặc $y = \tan x$ trên
    $\left[-2\pi;\ 2\pi\right]$, vẽ bằng TikZ THUẦN.

    Trong TikZ, hàm sin/cos/tan nhận ĐỘ; viết ``\x r'' để báo rằng
    đối số đang tính bằng radian.
    """
    P = math.pi
    ra = ["\\begin{tikzpicture}[>=stealth,x=0.62cm,y=0.85cm,thick,"
          "line join=round,font=\\footnotesize]"]
    ra.append("\\draw[->] (%s,0) -- (%s,0) node[below right]{$x$};"
              % (_toa(-2 * P - 0.6), _toa(2 * P + 0.8)))
    ra.append("\\draw[->] (0,-2.4) -- (0,2.4) node[left]{$y$};")
    ra.append("\\node[below left] at (0,0) {$O$};")
    for k, ten in ((-2, r"-2\pi"), (-1, r"-\pi"), (1, r"\pi"),
                   (2, r"2\pi")):
        ra.append("\\draw (%s,0.1) -- (%s,-0.1) node[below]{$%s$};"
                  % (_toa(k * P), _toa(k * P), ten))
    ra.append("\\node[left] at (0,1) {$1$};")
    ra.append("\\draw (-0.1,1) -- (0.1,1);")
    ra.append("\\node[left] at (0,-1) {$-1$};")
    ra.append("\\draw (-0.1,-1) -- (0.1,-1);")
    ra.append("\\clip (%s,-2.4) rectangle (%s,2.4);"
              % (_toa(-2 * P - 0.6), _toa(2 * P + 0.8)))
    if ham == "tan":
        # ve tung nhanh giua hai tiem can lien tiep
        for j in (-2, -1, 0, 1, 2):
            tu = (j - 0.5) * P + 0.12
            den = (j + 0.5) * P - 0.12
            ra.append("\\draw[very thick,smooth,samples=120,domain=%s:%s] "
                      "plot(\\x,{tan(\\x r)});" % (_toa(tu), _toa(den)))
        for j in (-2, -1, 0, 1, 2):
            x = (j + 0.5) * P
            ra.append("\\draw[dashed,line width=0.4pt] (%s,-2.4) -- "
                      "(%s,2.4);" % (_toa(x), _toa(x)))
    else:
        ra.append("\\draw[very thick,smooth,samples=240,domain=%s:%s] "
                  "plot(\\x,{%s(\\x r)});"
                  % (_toa(-2 * P), _toa(2 * P), ham))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


def L11_C1_B3_NB015_MC_A_01(socau, dang=1):
    r"""Nhận biết hàm số chẵn, hàm số lẻ, hàm số tuần hoàn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"hàm số chẵn",
         r"$f\left(-x\right) = f\left(x\right)$ với mọi $x$ thuộc tập xác "
         r"định",
         [r"$f\left(-x\right) = -f\left(x\right)$ với mọi $x$ thuộc tập "
          r"xác định",
          r"$f\left(x + T\right) = f\left(x\right)$ với mọi $x$ thuộc tập "
          r"xác định",
          r"$f\left(x\right) > 0$ với mọi $x$ thuộc tập xác định"],
         r"Hàm số chẵn có đồ thị đối xứng qua TRỤC TUNG."),
        (r"hàm số lẻ",
         r"$f\left(-x\right) = -f\left(x\right)$ với mọi $x$ thuộc tập xác "
         r"định",
         [r"$f\left(-x\right) = f\left(x\right)$ với mọi $x$ thuộc tập xác "
          r"định",
          r"$f\left(x + T\right) = f\left(x\right)$ với mọi $x$ thuộc tập "
          r"xác định",
          r"$f\left(x\right) < 0$ với mọi $x$ thuộc tập xác định"],
         r"Hàm số lẻ có đồ thị đối xứng qua GỐC TOẠ ĐỘ."),
        (r"hàm số tuần hoàn với chu kì $T$",
         r"$f\left(x + T\right) = f\left(x\right)$ với mọi $x$ thuộc tập "
         r"xác định",
         [r"$f\left(-x\right) = f\left(x\right)$ với mọi $x$ thuộc tập xác "
          r"định",
          r"$f\left(x + T\right) = -f\left(x\right)$ với mọi $x$ thuộc tập "
          r"xác định",
          r"$f\left(Tx\right) = f\left(x\right)$ với mọi $x$ thuộc tập xác "
          r"định"],
         r"Hàm tuần hoàn lặp lại chính nó sau mỗi đoạn có độ dài $T$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        ten, dung, nhieu, y_nghia = MAU[i]
        debai = (r"Hàm số $y = f\left(x\right)$ được gọi là %s khi nào?"
                 % ten)
        giai = (r"Theo định nghĩa, $y = f\left(x\right)$ là %s khi %s."
                % (ten, dung.replace("$", "")) +
                "\\\\\n" + y_nghia)
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), giai, 0, 0,
                                   dang)
    return cauTN


def L11_C1_B3_NB016_MC_A_01(socau, dang=1):
    r"""Đặc trưng hình học của đồ thị hàm số chẵn, hàm số lẻ.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"chẵn", r"trục tung", r"gốc toạ độ", r"trục hoành",
         r"đường thẳng $y = x$"),
        (r"lẻ", r"gốc toạ độ", r"trục tung", r"trục hoành",
         r"đường thẳng $y = x$"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        ten, dung_tt, n1, n2, n3 = MAU[i]
        dung = r"Đối xứng qua %s" % dung_tt
        nhieu = [r"Đối xứng qua %s" % n1, r"Đối xứng qua %s" % n2,
                 r"Đối xứng qua %s" % n3]
        debai = (r"Đồ thị của một hàm số %s có đặc điểm hình học nào sau "
                 r"đây?" % ten)
        giai = (r"Nếu hàm số %s thì với mỗi điểm "
                r"$M\left(x_0;\ y_0\right)$ thuộc đồ thị," % ten +
                "\\\\\n" +
                (r"điểm $M'\left(-x_0;\ y_0\right)$ cũng thuộc đồ thị, nên "
                 r"đồ thị đối xứng qua TRỤC TUNG."
                 if ten == "chẵn" else
                 r"điểm $M'\left(-x_0;\ -y_0\right)$ cũng thuộc đồ thị, "
                 r"nên đồ thị đối xứng qua GỐC TOẠ ĐỘ.") +
                "\\\\\n"
                r"Ví dụ: $y = \cos x$ là hàm chẵn, $y = \sin x$ và "
                r"$y = \tan x$ là hàm lẻ.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B3_NB017_MC_A_01(socau, dang=1):
    r"""Định nghĩa các hàm số lượng giác - tập xác định.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"y = \sin x", r"$\mathbb{R}$",
         [r"$\left[-1;\ 1\right]$",
          r"$\mathbb{R} \setminus \left\{\dfrac{\pi}{2} + k\pi\right\}$",
          r"$\left(0;\ +\infty\right)$"],
         r"$\sin x$ xác định với mọi số thực $x$."),
        (r"y = \cos x", r"$\mathbb{R}$",
         [r"$\left[-1;\ 1\right]$",
          r"$\mathbb{R} \setminus \left\{k\pi\right\}$",
          r"$\left(0;\ +\infty\right)$"],
         r"$\cos x$ xác định với mọi số thực $x$."),
        (r"y = \tan x",
         r"$\mathbb{R} \setminus \left\{\dfrac{\pi}{2} + k\pi,"
         r"\ k \in \mathbb{Z}\right\}$",
         [r"$\mathbb{R}$",
          r"$\mathbb{R} \setminus \left\{k\pi,\ k \in \mathbb{Z}\right\}$",
          r"$\left[-1;\ 1\right]$"],
         r"$\tan x = \dfrac{\sin x}{\cos x}$ nên phải có $\cos x \neq 0$, "
         r"tức là $x \neq \dfrac{\pi}{2} + k\pi$."),
        (r"y = \cot x",
         r"$\mathbb{R} \setminus \left\{k\pi,\ k \in \mathbb{Z}\right\}$",
         [r"$\mathbb{R}$",
          r"$\mathbb{R} \setminus \left\{\dfrac{\pi}{2} + k\pi,"
          r"\ k \in \mathbb{Z}\right\}$",
          r"$\left[-1;\ 1\right]$"],
         r"$\cot x = \dfrac{\cos x}{\sin x}$ nên phải có $\sin x \neq 0$, "
         r"tức là $x \neq k\pi$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        ham, dung, nhieu, ly_do = MAU[i]
        debai = r"Tập xác định của hàm số $%s$ là" % ham
        giai = (ly_do + "\\\\\n" +
                r"Vậy tập xác định của $%s$ là %s." % (ham, dung))
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), giai, 0, 0,
                                   dang)
    return cauTN


def L11_C1_B3_TH018_MC_A_01(socau, dang=1):
    r"""Bảng giá trị của bốn hàm số lượng giác trên một chu kì.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([k for k in GOC_DEP if 0 <= k <= 24])
        ham = random.choice(["sin", "cos", "tan"])
        if _tan_dep(k) is None and ham == "tan":
            continue
        if (k, ham) not in gt:
            gt.append((k, ham))

    cauTN = ""
    for k, ham in gt:
        tri = {"sin": _sin_dep(k), "cos": _cos_dep(k),
               "tan": _tan_dep(k)}[ham]
        dung = "$%s$" % tri
        ung_vien = ["$%s$" % v for h, v in
                    (("sin", _sin_dep(k)), ("cos", _cos_dep(k)),
                     ("tan", _tan_dep(k)))
                    if h != ham and v is not None]
        ung_vien += ["$%s$" % v for _, v in _GOC_TRI[1:]]
        ung_vien += ["$-%s$" % v for _, v in _GOC_TRI[1:]]
        nhieu = _ba_nhieu1(dung, ung_vien,
                           buoc=lambda t: "$%s$" % _TAN_TRI[t % 4][1])
        debai = (r"Cho $x = %s$. Tính $\%s x$." % (_pi_ps(k), ham))
        giai = (r"Trên một chu kì, giá trị của các hàm số lượng giác tại "
                r"góc đặc biệt được tra từ bảng giá trị." +
                "\\\\\n"
                r"Với $x = %s$: $\sin x = %s$, $\cos x = %s$%s."
                % (_pi_ps(k), _sin_dep(k), _cos_dep(k),
                   (r", $\tan x = %s$" % _tan_dep(k))
                   if _tan_dep(k) is not None else
                   r", còn $\tan x$ không xác định") +
                "\\\\\n"
                r"Vậy $\%s %s = %s$." % (ham, _pi_ps(k), tri))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B3_TH019_MC_A_01(socau, dang=1):
    r"""Nhận dạng đồ thị của các hàm số lượng giác (có hình).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    HAM = ["sin", "cos", "tan"]
    gt = [HAM[i] for i in _chon_chi_muc(len(HAM), socau)]

    cauTN = ""
    for ham in gt:
        hinh = _hinh_luong_giac(ham)
        dung = r"$y = \%s x$" % ham
        nhieu = [r"$y = \%s x$" % h for h in HAM if h != ham]
        nhieu.append(r"$y = \cot x$")
        if ham == "sin":
            ly_do = (r"Đồ thị cắt trục tung tại điểm $O\left(0;\ 0\right)$ "
                     r"và nhận giá trị lớn nhất bằng $1$ tại "
                     r"$x = \dfrac{\pi}{2}$." +
                     "\\\\\n"
                     r"Đồ thị đối xứng qua GỐC TOẠ ĐỘ nên đây là hàm số "
                     r"LẺ. Chỉ có $y = \sin x$ thoả mãn cả hai điều đó.")
        elif ham == "cos":
            ly_do = (r"Đồ thị cắt trục tung tại điểm $\left(0;\ 1\right)$, "
                     r"tức là đạt giá trị lớn nhất ngay tại $x = 0$." +
                     "\\\\\n"
                     r"Đồ thị đối xứng qua TRỤC TUNG nên đây là hàm số "
                     r"CHẴN. Vậy đó là $y = \cos x$.")
        else:
            ly_do = (r"Đồ thị gồm nhiều nhánh rời nhau, có các đường tiệm "
                     r"cận đứng $x = \dfrac{\pi}{2} + k\pi$." +
                     "\\\\\n"
                     r"Trên mỗi khoảng xác định đồ thị ĐỒNG BIẾN và nhận "
                     r"mọi giá trị thực. Vậy đó là $y = \tan x$.")
        debai = r"Hình vẽ sau là đồ thị của hàm số nào?"
        giai = (ly_do + "\\\\\n" +
                r"Nhắc lại: $y = \sin x$ và $y = \cos x$ có tập giá trị "
                r"$\left[-1;\ 1\right]$, tuần hoàn chu kì $2\pi$; "
                r"$y = \tan x$ và $y = \cot x$ tuần hoàn chu kì $\pi$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


HAM_LG = [
    (r"y = \sin x", r"\mathbb{R}", r"\left[-1;\ 1\right]", r"lẻ", r"2\pi"),
    (r"y = \cos x", r"\mathbb{R}", r"\left[-1;\ 1\right]", r"chẵn",
     r"2\pi"),
    (r"y = \tan x",
     r"\mathbb{R} \setminus \left\{\dfrac{\pi}{2} + k\pi\right\}",
     r"\mathbb{R}", r"lẻ", r"\pi"),
    (r"y = \cot x", r"\mathbb{R} \setminus \left\{k\pi\right\}",
     r"\mathbb{R}", r"lẻ", r"\pi"),
]


def L11_C1_B3_TH020_MC_A_01(socau, dang=1):
    r"""Tập xác định, tập giá trị, tính chẵn lẻ, tính tuần hoàn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = [(i, j) for i, j in
          zip(_chon_chi_muc(len(HAM_LG), socau),
              [random.randrange(3) for _ in range(socau)])]

    cauTN = ""
    for i, j in gt:
        ham, txd, tgt, chan_le, chu_ki = HAM_LG[i]
        if j == 0:
            hoi, dung, ung_vien = (
                r"có tập giá trị là", "$%s$" % tgt,
                ["$%s$" % v for v in
                 (r"\mathbb{R}", r"\left[-1;\ 1\right]",
                  r"\left[0;\ 1\right]", r"\left(0;\ +\infty\right)")])
        elif j == 1:
            hoi, dung, ung_vien = (
                r"là hàm số", "Hàm số %s" % chan_le,
                ["Hàm số chẵn", "Hàm số lẻ", "Không chẵn không lẻ",
                 "Vừa chẵn vừa lẻ"])
        else:
            hoi, dung, ung_vien = (
                r"tuần hoàn với chu kì", "$%s$" % chu_ki,
                ["$%s$" % v for v in (r"\pi", r"2\pi", r"\dfrac{\pi}{2}",
                                      r"4\pi")])
        nhieu = _ba_nhieu1(dung, ung_vien, buoc=lambda t: "$%d\\pi$"
                           % (t + 2))
        debai = r"Hàm số $%s$ %s" % (ham, hoi)
        giai = (r"Với hàm số $%s$:" % ham + "\\\\\n" +
                r"tập xác định $%s$; tập giá trị $%s$."
                % (txd, tgt) + "\\\\\n" +
                r"Đây là hàm số %s và tuần hoàn với chu kì $%s$."
                % (chan_le, chu_ki) + "\\\\\n" +
                r"Vậy đáp án đúng là %s." % dung)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B3_TH020_SA_A_01(socau):
    r"""Giá trị lớn nhất, nhỏ nhất của hàm số lượng giác - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5])
        b = random.randint(-6, 6)
        ham = random.choice(["sin", "cos"])
        hoi = random.choice(["max", "min"])
        if (a, b, ham, hoi) not in gt:
            gt.append((a, b, ham, hoi))

    cau = ""
    for a, b, ham, hoi in gt:
        lon = a + b
        nho = -a + b
        kq = lon if hoi == "max" else nho
        ten = "lớn nhất" if hoi == "max" else "nhỏ nhất"
        debai = (r"Tìm giá trị %s của hàm số "
                 r"$y = %d\%s x %s$."
                 % (ten, a, ham, ("+ %d" % b) if b >= 0 else
                    ("- %d" % (-b))))
        giai = (r"Với mọi $x$ ta có $-1 \leq \%s x \leq 1$." % ham +
                "\\\\\n"
                r"Nhân hai vế với $%d > 0$: $%d \leq %d\%s x \leq %d$."
                % (a, -a, a, ham, a) +
                "\\\\\n"
                r"Cộng $%d$ vào cả ba vế: $%d \leq y \leq %d$."
                % (b, nho, lon) +
                "\\\\\n"
                r"Vậy giá trị %s của hàm số là $%d$ (đạt được vì $\%s x$ "
                r"nhận được giá trị $%d$)."
                % (ten, kq, ham, 1 if hoi == "max" else -1))
        nhieu = _ba_nhieu1(str(kq), [str(lon if hoi == "min" else nho),
                                     str(a), str(b)],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def _bo_dao_dong():
    r"""$(A, w, k)$: li độ $x = A\cos\left(w\pi t\right)$ cm; thời điểm
    hỏi ứng với góc $\dfrac{k\pi}{12}$ có $\cos$ nằm trong bảng đặc
    biệt và $A$ chia hết cho $2$ nên li độ luôn là số ĐẸP."""
    A = random.choice([2, 4, 6, 8, 10])
    w = random.choice([1, 2, 4])
    k = random.choice([0, 4, 6, 8, 12, 16, 18, 20])   # cos = 1, 1/2, 0, -1/2, -1
    return A, w, k


def L11_C1_B3_VD021_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với hàm số lượng giác - dao động điều hoà.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_dao_dong()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for A, w, k in gt:
        t = Fraction(k, 12 * w)
        c = math.cos(k * math.pi / 12)
        x = Fraction(A) * Fraction(round(c * 2), 2)
        dung = "$%s$ cm" % _xx(x)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$ cm" % _xx(Fraction(A)), "$%s$ cm" % _xx(-x),
             "$0$ cm"],
            buoc=lambda u: "$%s$ cm" % _xx(float(x) + u))
        debai = (r"Một vật dao động điều hoà có li độ (tính bằng "
                 r"xentimét) ở thời điểm $t$ giây được cho bởi "
                 r"$x\left(t\right) = %d\cos\left(%s\pi t\right)$. Tính "
                 r"li độ của vật tại thời điểm $t = %s$ giây."
                 % (A, "" if w == 1 else "%d" % w,
                    _ps1(t.numerator, t.denominator)))
        giai = (r"Thay $t = %s$ vào công thức:"
                % _ps1(t.numerator, t.denominator) +
                "\\\\\n"
                r"$%s\pi t = %s\pi\cdot %s = %s$."
                % ("" if w == 1 else "%d" % w, "" if w == 1 else "%d" % w,
                   _ps1(t.numerator, t.denominator), _pi_ps(k)) +
                "\\\\\n"
                r"$\cos %s = %s$." % (_pi_ps(k), _cos_dep(k)) +
                "\\\\\n"
                r"$x = %d\cdot\left(%s\right) = %s$ (cm)."
                % (A, _cos_dep(k), _xx(x)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B3_VD021_SA_A_01(socau):
    r"""Dao động điều hoà - trả lời ngắn (li độ là số ĐẸP).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_dao_dong()
        if v not in gt:
            gt.append(v)

    cau = ""
    for A, w, k in gt:
        t = Fraction(k, 12 * w)
        c = math.cos(k * math.pi / 12)
        x = Fraction(A) * Fraction(round(c * 2), 2)
        dapso = _xx(x)
        debai = (r"Một vật dao động điều hoà có li độ (tính bằng "
                 r"xentimét) ở thời điểm $t$ giây được cho bởi "
                 r"$x\left(t\right) = %d\cos\left(%s\pi t\right)$. Tính "
                 r"li độ của vật tại thời điểm $t = %s$ giây (đơn vị: cm)."
                 % (A, "" if w == 1 else "%d" % w,
                    _ps1(t.numerator, t.denominator)))
        giai = (r"$%s\pi\cdot %s = %s$ và $\cos %s = %s$."
                % ("" if w == 1 else "%d" % w,
                   _ps1(t.numerator, t.denominator), _pi_ps(k),
                   _pi_ps(k), _cos_dep(k)) +
                "\\\\\n"
                r"$x = %d\cdot\left(%s\right) = %s$ (cm)."
                % (A, _cos_dep(k), dapso))
        nhieu = _ba_nhieu1(dapso, [_xx(Fraction(A)), _xx(-x), "0"],
                           buoc=lambda u: _xx(float(x) + u))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B3_VD021_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán dao động điều hoà.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A = random.choice([2, 4, 6, 8, 10])
        w = random.choice([1, 2, 4])
        if (A, w) not in gt:
            gt.append((A, w))

    cauTN = ""
    for A, w in gt:
        T = Fraction(2, w)
        t1 = Fraction(1, 3 * w)      # goc pi/3 -> cos = 1/2
        x1 = Fraction(A, 2)
        debai = (r"Một vật dao động điều hoà có li độ (tính bằng "
                 r"xentimét) ở thời điểm $t$ giây được cho bởi "
                 r"$x\left(t\right) = %d\cos\left(%s\pi t\right)$ với "
                 r"$t \geq 0$."
                 % (A, "" if w == 1 else "%d" % w))

        hoi_a = r"Tính li độ của vật tại thời điểm $t = 0$."
        giai_a = (r"$x\left(0\right) = %d\cos 0 = %d\cdot 1 = %d$ (cm)."
                  % (A, A, A) +
                  "\\\\\n"
                  r"Đây là vị trí xa vị trí cân bằng nhất, gọi là biên độ.")

        hoi_b = (r"Tìm chu kì dao động của vật, tức số $T > 0$ nhỏ nhất "
                 r"sao cho $x\left(t + T\right) = x\left(t\right)$ với "
                 r"mọi $t$.")
        giai_b = (r"Hàm $\cos u$ tuần hoàn với chu kì $2\pi$, nghĩa là "
                  r"$u$ phải tăng thêm $2\pi$." +
                  "\\\\\n"
                  r"Ở đây $u = %s\pi t$ nên $%s\pi T = 2\pi$."
                  % ("" if w == 1 else "%d" % w,
                     "" if w == 1 else "%d" % w) +
                  "\\\\\n"
                  r"Suy ra $T = %s$ (giây)."
                  % _ps1(T.numerator, T.denominator))

        hoi_c = (r"Tính li độ tại thời điểm $t = %s$ giây."
                 % _ps1(t1.numerator, t1.denominator))
        giai_c = (r"$%s\pi\cdot %s = \dfrac{\pi}{3}$."
                  % ("" if w == 1 else "%d" % w,
                     _ps1(t1.numerator, t1.denominator)) +
                  "\\\\\n"
                  r"$\cos\dfrac{\pi}{3} = \dfrac{1}{2}$ nên "
                  r"$x = %d\cdot\dfrac{1}{2} = %s$ (cm)."
                  % (A, _xx(x1)))

        ds_abcd = [(hoi_a, r"x\left(0\right) = %d \text{ cm}" % A, giai_a),
                   (hoi_b, r"T = %s \text{ giây}"
                    % _ps1(T.numerator, T.denominator), giai_b),
                   (hoi_c, r"x = %s \text{ cm}" % _xx(x1), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 4. PHƯƠNG TRÌNH LƯỢNG GIÁC CƠ BẢN
# =====================================================================

CT_NGHIEM = [
    (r"\sin x = \sin\alpha",
     r"\left[\begin{aligned} x &= \alpha + k2\pi \\ "
     r"x &= \pi - \alpha + k2\pi \end{aligned}\right.",
     r"\left[\begin{aligned} x &= \alpha + k2\pi \\ "
     r"x &= -\alpha + k2\pi \end{aligned}\right.",
     r"x = \alpha + k\pi",
     r"x = \pm\alpha + k2\pi",
     r"Với $\sin$, hai điểm trên đường tròn lượng giác có cùng tung độ "
     r"đối xứng nhau qua TRỤC TUNG, nên góc thứ hai là "
     r"$\pi - \alpha$."),
    (r"\cos x = \cos\alpha",
     r"x = \pm\alpha + k2\pi",
     r"x = \alpha + k2\pi",
     r"\left[\begin{aligned} x &= \alpha + k2\pi \\ "
     r"x &= \pi - \alpha + k2\pi \end{aligned}\right.",
     r"x = \alpha + k\pi",
     r"Với $\cos$, hai điểm có cùng hoành độ đối xứng nhau qua TRỤC "
     r"HOÀNH, nên góc thứ hai là $-\alpha$."),
    (r"\tan x = \tan\alpha",
     r"x = \alpha + k\pi",
     r"x = \alpha + k2\pi",
     r"x = \pm\alpha + k\pi",
     r"\left[\begin{aligned} x &= \alpha + k\pi \\ "
     r"x &= \pi - \alpha + k\pi \end{aligned}\right.",
     r"Hàm $\tan$ tuần hoàn với chu kì $\pi$ nên chỉ cần cộng thêm "
     r"$k\pi$."),
    (r"\cot x = \cot\alpha",
     r"x = \alpha + k\pi",
     r"x = \alpha + k2\pi",
     r"x = \pm\alpha + k\pi",
     r"\left[\begin{aligned} x &= \alpha + k\pi \\ "
     r"x &= -\alpha + k\pi \end{aligned}\right.",
     r"Hàm $\cot$ cũng tuần hoàn với chu kì $\pi$ nên nghiệm chỉ sai "
     r"khác $k\pi$."),
]


def _cau_ct_nghiem(socau, dang, chi_muc):
    r"""Khung chung cho bốn dạng nhận biết công thức nghiệm."""
    gt = [chi_muc] * socau
    cauTN = ""
    for i in gt:
        pt, dung_ct, n1, n2, n3 = CT_NGHIEM[i][:5]
        ly_do = CT_NGHIEM[i][5]
        dung = "$%s$" % dung_ct
        debai = (r"Với $k \in \mathbb{Z}$, nghiệm của phương trình "
                 r"$%s$ là" % pt)
        giai = (r"Công thức nghiệm của phương trình lượng giác cơ bản:" +
                "\\\\\n"
                r"$%s \Leftrightarrow %s$ với $k \in \mathbb{Z}$."
                % (pt, dung_ct) +
                "\\\\\n" + ly_do)
        cauTN += MC_SA_answer_text(debai, dung,
                                   ["$%s$" % n1, "$%s$" % n2, "$%s$" % n3],
                                   giai, 0, 0, dang)
    return cauTN


def L11_C1_B4_NB022_MC_A_01(socau, dang=1):
    r"""Công thức nghiệm của phương trình $\sin x = \sin\alpha$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _cau_ct_nghiem(socau, dang, 0)


def L11_C1_B4_NB023_MC_A_01(socau, dang=1):
    r"""Công thức nghiệm của phương trình $\cos x = \cos\alpha$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _cau_ct_nghiem(socau, dang, 1)


def L11_C1_B4_NB024_MC_A_01(socau, dang=1):
    r"""Công thức nghiệm của phương trình $\tan x = \tan\alpha$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _cau_ct_nghiem(socau, dang, 2)


def L11_C1_B4_NB025_MC_A_01(socau, dang=1):
    r"""Công thức nghiệm của phương trình $\cot x = \cot\alpha$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _cau_ct_nghiem(socau, dang, 3)


def L11_C1_B4_TH026_MC_A_01(socau, dang=1):
    r"""Giải phương trình lượng giác cơ bản với giá trị đặc biệt.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([2, 3, 4, 6])       # pi/6, pi/4, pi/3, pi/2
        ham = random.choice(["sin", "cos"])
        if (k, ham) not in gt:
            gt.append((k, ham))

    cauTN = ""
    for k, ham in gt:
        a = _pi_ps(k)
        tri = _sin_dep(k) if ham == "sin" else _cos_dep(k)
        if ham == "sin":
            dung_ct = (r"\left[\begin{aligned} x &= %s + k2\pi \\ "
                       r"x &= %s + k2\pi \end{aligned}\right." %
                       (a, _pi_ps(12 - k)))
            n1 = r"x = \pm %s + k2\pi" % a
            n2 = r"x = %s + k\pi" % a
            ly_do = (r"Với phương trình $\sin$, nghiệm thứ hai là "
                     r"$\pi - %s = %s$." % (a, _pi_ps(12 - k)))
        else:
            dung_ct = r"x = \pm %s + k2\pi" % a
            n1 = (r"\left[\begin{aligned} x &= %s + k2\pi \\ "
                  r"x &= %s + k2\pi \end{aligned}\right." %
                  (a, _pi_ps(12 - k)))
            n2 = r"x = %s + k\pi" % a
            ly_do = (r"Với phương trình $\cos$, nghiệm thứ hai là "
                     r"$-%s$, viết gộp thành $\pm %s$." % (a, a))
        dung = "$%s$" % dung_ct
        nhieu = ["$%s$" % n1, "$%s$" % n2,
                 r"$x = %s$" % a]
        debai = (r"Giải phương trình $\%s x = %s$ (với "
                 r"$k \in \mathbb{Z}$)." % (ham, tri))
        giai = (r"Ta có $\%s %s = %s$ nên phương trình trở thành "
                r"$\%s x = \%s %s$." % (ham, a, tri, ham, ham, a) +
                "\\\\\n" + ly_do +
                "\\\\\n"
                r"Vậy nghiệm là $%s$ với $k \in \mathbb{Z}$." % dung_ct)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B4_TH026_SA_A_01(socau):
    r"""Số nghiệm của phương trình lượng giác trên một khoảng - SA.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([2, 3, 4])
        ham = random.choice(["sin", "cos"])
        n = random.choice([1, 2, 3])          # khoang [0; 2n*pi)
        if (k, ham, n) not in gt:
            gt.append((k, ham, n))

    cau = ""
    for k, ham, n in gt:
        tri = _sin_dep(k) if ham == "sin" else _cos_dep(k)
        # tren moi chu ki 2pi, sin x = c (0 < c < 1) co 2 nghiem;
        # cos x = c (0 < c < 1) cung co 2 nghiem
        so = 2 * n
        debai = (r"Tìm số nghiệm của phương trình $\%s x = %s$ trên "
                 r"nửa khoảng $\left[0;\ %s\right)$."
                 % (ham, tri, _pi_ps(24 * n)))
        giai = (r"Trên mỗi chu kì có độ dài $2\pi$, đường thẳng "
                r"$y = %s$ (với $0 < %s < 1$) cắt đồ thị hàm số "
                r"$y = \%s x$ đúng $2$ điểm." % (tri, tri, ham) +
                "\\\\\n"
                r"Nửa khoảng $\left[0;\ %s\right)$ dài $%s$, gồm đúng "
                r"$%d$ chu kì." % (_pi_ps(24 * n), _pi_ps(24 * n), n) +
                "\\\\\n"
                r"Vậy phương trình có $2\cdot %d = %d$ nghiệm."
                % (n, so))
        nhieu = _ba_nhieu1(str(so), [str(n), str(so + 1), str(4 * n)],
                           buoc=lambda t: str(so + t + 1))
        cau += MC_SA_answer_const(debai, str(so), nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B4_TH026_TL_A_01(socau, dong=1):
    r"""Tự luận: giải phương trình lượng giác cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k1 = random.choice([2, 3, 4])
        k2 = random.choice([2, 3, 4, 6])
        k3 = random.choice([3, 4])
        if (k1, k2, k3) not in gt:
            gt.append((k1, k2, k3))

    cauTN = ""
    for k1, k2, k3 in gt:
        debai = (r"Giải các phương trình lượng giác sau (với "
                 r"$k \in \mathbb{Z}$).")

        a1 = _pi_ps(k1)
        hoi_a = r"$\sin x = %s$" % _sin_dep(k1)
        giai_a = (r"Vì $\sin %s = %s$ nên phương trình trở thành "
                  r"$\sin x = \sin %s$." % (a1, _sin_dep(k1), a1) +
                  "\\\\\n"
                  r"$\Leftrightarrow \left[\begin{aligned} x &= %s + k2\pi "
                  r"\\ x &= %s + k2\pi \end{aligned}\right.$"
                  % (a1, _pi_ps(12 - k1)))
        dap_a = (r"x = %s + k2\pi \text{ hoặc } x = %s + k2\pi"
                 % (a1, _pi_ps(12 - k1)))

        a2 = _pi_ps(k2)
        hoi_b = r"$\cos x = %s$" % _cos_dep(k2)
        giai_b = (r"Vì $\cos %s = %s$ nên phương trình trở thành "
                  r"$\cos x = \cos %s$." % (a2, _cos_dep(k2), a2) +
                  "\\\\\n"
                  r"$\Leftrightarrow x = \pm %s + k2\pi$." % a2)
        dap_b = r"x = \pm %s + k2\pi" % a2

        a3 = _pi_ps(k3)
        hoi_c = r"$\tan x = %s$" % _tan_dep(k3)
        giai_c = (r"Vì $\tan %s = %s$ nên phương trình trở thành "
                  r"$\tan x = \tan %s$." % (a3, _tan_dep(k3), a3) +
                  "\\\\\n"
                  r"$\Leftrightarrow x = %s + k\pi$." % a3 +
                  "\\\\\n"
                  r"Chú ý với $\tan$ chỉ cộng $k\pi$ (chu kì $\pi$), "
                  r"không phải $k2\pi$.")
        dap_c = r"x = %s + k\pi" % a3

        ds_abcd = [(hoi_a, dap_a, giai_a), (hoi_b, dap_b, giai_b),
                   (hoi_c, dap_c, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L11_C1_B4_TH027_MC_A_01(socau, dang=1):
    r"""Phương trình lượng giác dạng vận dụng trực tiếp công thức nghiệm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        m = random.choice([2, 3])
        k = random.choice([2, 3, 4, 6])
        if (m, k) not in gt:
            gt.append((m, k))

    cauTN = ""
    for m, k in gt:
        a = _pi_ps(k)
        tri = _cos_dep(k)
        # 2pi/m phai RUT GON: m = 2 thi la k\pi chu khong phai
        # k\dfrac{2\pi}{2}.
        buoc = _pi_ps(24, 12 * m)
        dung_ct = r"x = \pm %s + k%s" % (_pi_ps(k, 12 * m), buoc)
        dung = "$%s$" % dung_ct
        nhieu = ["$%s$" % v for v in
                 (r"x = \pm %s + k2\pi" % _pi_ps(k, 12 * m),
                  r"x = \pm %s + k%s" % (a, buoc),
                  r"x = %s + k%s" % (_pi_ps(k, 12 * m), buoc))]
        debai = (r"Giải phương trình $\cos %dx = %s$ (với "
                 r"$k \in \mathbb{Z}$)." % (m, tri))
        giai = (r"Vì $\cos %s = %s$ nên phương trình trở thành "
                r"$\cos %dx = \cos %s$." % (a, tri, m, a) +
                "\\\\\n"
                r"$\Leftrightarrow %dx = \pm %s + k2\pi$." % (m, a) +
                "\\\\\n"
                r"Chia hai vế cho $%d$: $x = \pm %s + k%s$."
                % (m, _pi_ps(k, 12 * m), buoc) +
                "\\\\\n"
                r"Chú ý phải chia CẢ $k2\pi$ cho $%d$, đây là chỗ hay "
                r"quên nhất." % m)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B4_VD028_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn dẫn đến phương trình lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5])
        b = random.choice([2, 4, 6])
        T = random.choice([6, 12, 24])
        if (a, b, T) not in gt:
            gt.append((a, b, T))

    cauTN = ""
    for a, b, T in gt:
        h = Fraction(a) + Fraction(b, 2)
        t = Fraction(T, 12)
        dung = "$%s$ phút" % _xx(t)
        nhieu = _ba_nhieu1(
            dung,
            ["$%s$ phút" % _xx(Fraction(T, 4)),
             "$%s$ phút" % _xx(Fraction(T, 6)),
             "$%s$ phút" % _xx(Fraction(T))],
            buoc=lambda u: "$%s$ phút" % _xx(float(t) + u))
        debai = (r"Khoảng cách từ một chiếc gàu của guồng nước đến mặt "
                 r"nước (tính bằng mét) ở thời điểm $t$ phút được cho bởi "
                 r"$h\left(t\right) = %d + %d\sin\dfrac{2\pi t}{%d}$. Hỏi "
                 r"LẦN ĐẦU TIÊN khoảng cách đó bằng $%s$ mét là ở thời "
                 r"điểm nào?" % (a, b, T, _xx(h)))
        giai = (r"Giải phương trình $%d + %d\sin\dfrac{2\pi t}{%d} = %s$."
                % (a, b, T, _xx(h)) +
                "\\\\\n"
                r"$%d\sin\dfrac{2\pi t}{%d} = %s \Leftrightarrow "
                r"\sin\dfrac{2\pi t}{%d} = \dfrac{1}{2}$."
                % (b, T, _xx(Fraction(b, 2)), T) +
                "\\\\\n"
                r"$\Leftrightarrow \left[\begin{aligned} "
                r"\dfrac{2\pi t}{%d} &= \dfrac{\pi}{6} + k2\pi \\ "
                r"\dfrac{2\pi t}{%d} &= \dfrac{5\pi}{6} + k2\pi "
                r"\end{aligned}\right.$" % (T, T) +
                "\\\\\n"
                r"Từ nhánh thứ nhất với $k = 0$: $t = \dfrac{%d}{12} = "
                r"%s$ (phút); từ nhánh thứ hai với $k = 0$: "
                r"$t = \dfrac{5\cdot %d}{12} = %s$ (phút)."
                % (T, _xx(t), T, _xx(Fraction(5 * T, 12))) +
                "\\\\\n"
                r"Thời điểm nhỏ nhất dương là $t = %s$ phút." % _xx(t))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C1_B4_VD028_SA_A_01(socau):
    r"""Thời điểm đầu tiên thoả mãn điều kiện - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A = random.choice([2, 4, 6, 8, 10])
        T = random.choice([6, 12, 24])
        if (A, T) not in gt:
            gt.append((A, T))

    cau = ""
    for A, T in gt:
        # x(t) = A cos(2pi t / T) = A/2  <=>  2pi t / T = pi/3
        t = Fraction(T, 6)
        dapso = _xx(t)
        debai = (r"Một vật dao động điều hoà có li độ (tính bằng "
                 r"xentimét) ở thời điểm $t$ giây được cho bởi "
                 r"$x\left(t\right) = %d\cos\dfrac{2\pi t}{%d}$. Hỏi lần "
                 r"đầu tiên vật có li độ bằng $%s$ cm là ở thời điểm nào "
                 r"(đơn vị: giây)?" % (A, T, _xx(Fraction(A, 2))))
        giai = (r"Giải $%d\cos\dfrac{2\pi t}{%d} = %s \Leftrightarrow "
                r"\cos\dfrac{2\pi t}{%d} = \dfrac{1}{2}$."
                % (A, T, _xx(Fraction(A, 2)), T) +
                "\\\\\n"
                r"$\Leftrightarrow \dfrac{2\pi t}{%d} = "
                r"\pm\dfrac{\pi}{3} + k2\pi$." % T +
                "\\\\\n"
                r"$\Leftrightarrow t = \pm\dfrac{%d}{6} + k%d$."
                % (T, T) +
                "\\\\\n"
                r"Giá trị dương nhỏ nhất là $t = \dfrac{%d}{6} = %s$ "
                r"(giây)." % (T, dapso))
        nhieu = _ba_nhieu1(dapso,
                           [_xx(Fraction(T, 3)), _xx(Fraction(T)),
                            _xx(Fraction(T, 12))],
                           buoc=lambda u: _xx(float(t) + u))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C1_B4_VD028_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn dẫn đến phương trình lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5])
        b = random.choice([2, 4, 6])
        T = random.choice([6, 12, 24])
        if (a, b, T) not in gt:
            gt.append((a, b, T))

    cauTN = ""
    for a, b, T in gt:
        h = Fraction(a) + Fraction(b, 2)
        t1 = Fraction(T, 12)
        t2 = Fraction(5 * T, 12)
        debai = (r"Khoảng cách từ một chiếc gàu của guồng nước đến mặt "
                 r"nước (tính bằng mét) ở thời điểm $t$ phút được cho bởi "
                 r"$h\left(t\right) = %d + %d\sin\dfrac{2\pi t}{%d}$ với "
                 r"$t \geq 0$." % (a, b, T))

        hoi_a = (r"Viết phương trình để tìm thời điểm gàu cách mặt nước "
                 r"$%s$ mét." % _xx(h))
        giai_a = (r"Cho $h\left(t\right) = %s$ ta được phương trình"
                  % _xx(h) +
                  "\\\\\n"
                  r"$%d + %d\sin\dfrac{2\pi t}{%d} = %s$."
                  % (a, b, T, _xx(h)))

        hoi_b = r"Giải phương trình vừa lập."
        giai_b = (r"$%d\sin\dfrac{2\pi t}{%d} = %s \Leftrightarrow "
                  r"\sin\dfrac{2\pi t}{%d} = \dfrac{1}{2} = "
                  r"\sin\dfrac{\pi}{6}$."
                  % (b, T, _xx(Fraction(b, 2)), T) +
                  "\\\\\n"
                  r"$\Leftrightarrow \left[\begin{aligned} "
                  r"\dfrac{2\pi t}{%d} &= \dfrac{\pi}{6} + k2\pi \\ "
                  r"\dfrac{2\pi t}{%d} &= \dfrac{5\pi}{6} + k2\pi "
                  r"\end{aligned}\right.$" % (T, T) +
                  "\\\\\n"
                  r"$\Leftrightarrow \left[\begin{aligned} "
                  r"t &= %s + k%d \\ t &= %s + k%d \end{aligned}\right.$ "
                  r"với $k \in \mathbb{Z}$."
                  % (_xx(t1), T, _xx(t2), T))

        hoi_c = (r"Tìm hai thời điểm đầu tiên (kể từ lúc $t = 0$) mà gàu "
                 r"cách mặt nước $%s$ mét." % _xx(h))
        giai_c = (r"Lấy $k = 0$ ở cả hai họ nghiệm được $t = %s$ và "
                  r"$t = %s$ (phút)." % (_xx(t1), _xx(t2)) +
                  "\\\\\n"
                  r"Các nghiệm tiếp theo đều lớn hơn (cộng thêm bội của "
                  r"$%d$ phút)." % T +
                  "\\\\\n"
                  r"Vậy hai thời điểm đầu tiên là $t = %s$ phút và "
                  r"$t = %s$ phút." % (_xx(t1), _xx(t2)))

        ds_abcd = [(hoi_a, r"%d + %d\sin\dfrac{2\pi t}{%d} = %s"
                    % (a, b, T, _xx(h)), giai_a),
                   (hoi_b, r"t = %s + k%d \text{ hoặc } t = %s + k%d"
                    % (_xx(t1), T, _xx(t2), T), giai_b),
                   (hoi_c, r"t = %s \text{ và } t = %s"
                    % (_xx(t1), _xx(t2)), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 1
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C1_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - giá trị lượng giác và công thức lượng giác.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        s, c, h = random.choice([b for b in PYTAGO1 if b[2] == 5])
        i = random.randrange(4)
        if (s, c, h, i) not in gt:
            gt.append((s, c, h, i))

    cauTF = ""
    for s, c, h, i in gt:
        mo_ta, dau_cos, dau_sin, ten_pt = KHOANG_GPT[i]
        sin_a, cos_a = dau_sin * s, dau_cos * c
        sin2 = Fraction(2 * sin_a * cos_a, h * h)
        cos2 = Fraction(cos_a * cos_a - sin_a * sin_a, h * h)
        debai = (r"Cho góc lượng giác $\alpha$ thoả mãn "
                 r"$\sin\alpha = %s$ và $%s$."
                 % (_ps1(sin_a, h), mo_ta))

        ds_abcd = (
            # a) NB - hệ thức cơ bản, chỉ cần nhớ
            [
                (r"{\True $\sin^{2}\alpha + \cos^{2}\alpha = 1$}",
                 r"Đúng. Đây là hệ thức lượng giác cơ bản, đúng với mọi "
                 r"góc lượng giác $\alpha$."),
                (r"{$\sin\alpha + \cos\alpha = 1$ với mọi $\alpha$}",
                 r"Sai. Hệ thức đúng là với BÌNH PHƯƠNG: "
                 r"$\sin^{2}\alpha + \cos^{2}\alpha = 1$."),
            ],
            # b) TH - một lần dùng hệ thức và xét dấu
            [
                (r"{\True $\cos\alpha = %s$}" % _ps1(cos_a, h),
                 r"Đúng. $\cos^{2}\alpha = 1 - \left(%s\right)^{2} = "
                 r"\dfrac{%d}{%d}$ nên $\cos\alpha = \pm\dfrac{%d}{%d}$."
                 % (_ps1(sin_a, h), c * c, h * h, c, h) + "\\\\\n" +
                 r"Vì $\alpha$ ở góc phần tư %s nên $\cos\alpha$ mang dấu "
                 r"%s, tức $\cos\alpha = %s$."
                 % (ten_pt, "dương" if dau_cos > 0 else "âm",
                    _ps1(cos_a, h))),
                (r"{$\cos\alpha = %s$}" % _ps1(-cos_a, h),
                 r"Sai. Dấu của $\cos\alpha$ do góc phần tư %s quyết "
                 r"định, phải là %s nên $\cos\alpha = %s$."
                 % (ten_pt, "dương" if dau_cos > 0 else "âm",
                    _ps1(cos_a, h))),
            ],
            # c) VD - công thức nhân đôi
            [
                (r"{\True $\sin 2\alpha = %s$}"
                 % _ps1(sin2.numerator, sin2.denominator),
                 r"Đúng. $\sin 2\alpha = 2\sin\alpha\cos\alpha = "
                 r"2\cdot\left(%s\right)\cdot\left(%s\right) = %s$."
                 % (_ps1(sin_a, h), _ps1(cos_a, h),
                    _ps1(sin2.numerator, sin2.denominator))),
                (r"{$\sin 2\alpha = 2\sin\alpha = %s$}"
                 % _ps1(2 * sin_a, h),
                 r"Sai. $\sin 2\alpha$ KHÔNG bằng $2\sin\alpha$; công "
                 r"thức đúng là $2\sin\alpha\cos\alpha = %s$."
                 % _ps1(sin2.numerator, sin2.denominator)),
            ],
            # d) VDC - phải tự chọn công thức rồi mới tính được
            [
                (r"{\True $\cos 2\alpha = %s$}"
                 % _ps1(cos2.numerator, cos2.denominator),
                 r"Đúng. Dùng $\cos 2\alpha = 1 - 2\sin^{2}\alpha$ thì "
                 r"không cần biết dấu của $\cos\alpha$:" + "\\\\\n" +
                 r"$\cos 2\alpha = 1 - 2\cdot\left(%s\right)^{2} = %s$."
                 % (_ps1(sin_a, h),
                    _ps1(cos2.numerator, cos2.denominator))),
                (r"{$\cos 2\alpha = 2\cos^{2}\alpha = %s$}"
                 % _ps1(2 * c * c, h * h),
                 r"Sai. Công thức đúng là $\cos 2\alpha = "
                 r"2\cos^{2}\alpha - 1$ (còn phải TRỪ $1$), cho kết quả "
                 r"$%s$." % _ps1(cos2.numerator, cos2.denominator)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L11_C1_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - hàm số lượng giác và phương trình lượng giác cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([2, 3, 4])
        a = random.choice([2, 3, 4, 5])
        b = random.randint(-4, 4)
        if (k, a, b) not in gt:
            gt.append((k, a, b))

    cauTF = ""
    for k, a, b in gt:
        goc = _pi_ps(k)
        tri = _sin_dep(k)
        debai = (r"Cho hàm số $y = %d\sin x %s$ và phương trình "
                 r"$\sin x = %s$."
                 % (a, ("+ %d" % b) if b >= 0 else ("- %d" % (-b)), tri))

        ds_abcd = (
            # a) NB - tập xác định
            [
                (r"{\True Hàm số $y = \sin x$ có tập xác định "
                 r"$\mathbb{R}$}",
                 r"Đúng. $\sin x$ xác định với mọi số thực $x$."),
                (r"{Hàm số $y = \sin x$ có tập xác định "
                 r"$\left[-1;\ 1\right]$}",
                 r"Sai. $\left[-1;\ 1\right]$ là TẬP GIÁ TRỊ, còn tập xác "
                 r"định là $\mathbb{R}$."),
            ],
            # b) TH - chu kì và tính chẵn lẻ
            [
                (r"{\True Hàm số $y = \sin x$ là hàm số lẻ và tuần hoàn "
                 r"với chu kì $2\pi$}",
                 r"Đúng. $\sin\left(-x\right) = -\sin x$ nên hàm số lẻ; "
                 r"$\sin\left(x + 2\pi\right) = \sin x$ nên chu kì là "
                 r"$2\pi$."),
                (r"{Hàm số $y = \sin x$ là hàm số chẵn}",
                 r"Sai. $\sin\left(-x\right) = -\sin x$ nên $y = \sin x$ "
                 r"là hàm số LẺ; $y = \cos x$ mới là hàm chẵn."),
            ],
            # c) VD - giá trị lớn nhất của hàm số
            [
                (r"{\True Giá trị lớn nhất của hàm số $y = %d\sin x %s$ "
                 r"bằng $%d$}"
                 % (a, ("+ %d" % b) if b >= 0 else ("- %d" % (-b)),
                    a + b),
                 r"Đúng. Vì $-1 \leq \sin x \leq 1$ nên "
                 r"$%d \leq y \leq %d$." % (-a + b, a + b) + "\\\\\n" +
                 r"Dấu bằng ở vế phải xảy ra khi $\sin x = 1$, nên giá "
                 r"trị lớn nhất là $%d$." % (a + b)),
                (r"{Giá trị lớn nhất của hàm số $y = %d\sin x %s$ bằng "
                 r"$%d$}"
                 % (a, ("+ %d" % b) if b >= 0 else ("- %d" % (-b)), a),
                 r"Sai. Còn phải cộng thêm $%d$: giá trị lớn nhất là "
                 r"$%d$." % (b, a + b)),
            ],
            # d) VDC - công thức nghiệm đầy đủ của phương trình sin
            [
                (r"{\True Phương trình $\sin x = %s$ có nghiệm "
                 r"$x = %s + k2\pi$ hoặc $x = %s + k2\pi$ "
                 r"($k \in \mathbb{Z}$)}"
                 % (tri, goc, _pi_ps(12 - k)),
                 r"Đúng. $\sin x = \sin %s$ nên có HAI họ nghiệm: "
                 r"$x = %s + k2\pi$ và $x = \pi - %s + k2\pi = %s + k2\pi$."
                 % (goc, goc, goc, _pi_ps(12 - k))),
                (r"{Phương trình $\sin x = %s$ chỉ có một họ nghiệm "
                 r"$x = %s + k2\pi$ ($k \in \mathbb{Z}$)}" % (tri, goc),
                 r"Sai. Còn họ nghiệm thứ hai $x = \pi - %s + k2\pi = "
                 r"%s + k2\pi$; bỏ sót họ này là lỗi rất hay gặp."
                 % (goc, _pi_ps(12 - k))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
