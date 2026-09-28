# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 6. Hàm số mũ và hàm số lôgarit
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Kiến thức dùng trong tệp:

  * $a^{\frac{m}{n}} = \sqrt[n]{a^{m}}$ với $a > 0$;
    $a^{m}a^{n} = a^{m+n}$, $\dfrac{a^{m}}{a^{n}} = a^{m-n}$,
    $\left(a^{m}\right)^{n} = a^{mn}$.
  * $\log_a b = c \Leftrightarrow a^{c} = b$ ($a > 0$, $a \neq 1$,
    $b > 0$).
  * $\log_a\left(xy\right) = \log_a x + \log_a y$;
    $\log_a\dfrac{x}{y} = \log_a x - \log_a y$;
    $\log_a x^{\alpha} = \alpha\log_a x$;
    $\log_a b = \dfrac{\log_c b}{\log_c a}$.
  * Hàm số mũ $y = a^{x}$ và hàm số lôgarit $y = \log_a x$
    ($a > 0$, $a \neq 1$): đồng biến khi $a > 1$, nghịch biến khi
    $0 < a < 1$.
  * $a^{u} = a^{v} \Leftrightarrow u = v$;
    $\log_a u = \log_a v \Leftrightarrow u = v > 0$.

Số liệu chọn để ĐÁP SỐ ĐẸP: mọi luỹ thừa hữu tỉ đều chọn cơ số là luỹ
thừa đúng ($8^{\frac{2}{3}}$, $16^{\frac{3}{4}}$...) nên kết quả NGUYÊN;
mọi lôgarit đều có đối số là luỹ thừa đúng của cơ số; mọi phương trình
mũ - lôgarit đều có nghiệm NGUYÊN.

Bài học lớp 10 đã áp dụng: chữ tiếng Việt không nằm trần trong $...$;
không dùng **đậm**; mọi chuỗi có dấu gạch chéo đều là r"..."; mọi danh
sách phương án nhiễu đều qua _ba_nhieu6; bảng và đồ thị vẽ bằng TikZ
THUẦN (MathJax trên web không dựng được tabular).
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
    s = "%.3f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _ba_nhieu6(dapso, ung_vien, buoc=None):
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


def _dau(x):
    return ("+ %d" % abs(x)) if x >= 0 else ("- %d" % abs(x))


def _nhi_thuc6(m, n, bien="x"):
    r"""Viết $mx + n$ gọn (bỏ hệ số 1, bỏ hạng tử 0)."""
    he = "" if m == 1 else ("-" if m == -1 else "%d" % m)
    if n == 0:
        return "%s%s" % (he, bien)
    return "%s%s %s %d" % (he, bien, "+" if n > 0 else "-", abs(n))


def _mu(co_so, mu):
    r"""Viết $a^{m}$, bỏ số mũ 1."""
    cs = "%s" % co_so
    if str(mu) == "1":
        return cs
    return r"%s^{%s}" % (cs, mu)


def _mu_ps(co_so, p, q):
    r"""Viết $a^{\frac{p}{q}}$ (rút gọn phân số trước)."""
    f = Fraction(p, q)
    if f.denominator == 1:
        return _mu(co_so, "%d" % f.numerator)
    return r"%s^{\frac{%d}{%d}}" % (co_so, f.numerator, f.denominator)


def _can(n, trong):
    r"""Viết $\sqrt[n]{\cdot}$; $n = 2$ thì viết $\sqrt{\cdot}$."""
    if n == 2:
        return r"\sqrt{%s}" % trong
    return r"\sqrt[%s]{%s}" % (n, trong)


def _log(a, x):
    r"""Viết lôgarit theo đúng quy ước SGK: $\log$, $\ln$ hoặc $\log_a$."""
    if a == 10:
        return r"\log %s" % x
    if a == "e":
        return r"\ln %s" % x
    return r"\log_{%s}%s" % (a, x)


# Bộ (cơ số, số mũ) để luỹ thừa hữu tỉ ra SỐ NGUYÊN.
CAN_DEP = [(8, 3, 2), (8, 3, 4), (16, 4, 3), (16, 2, 3), (27, 3, 2),
           (27, 3, 4), (32, 5, 2), (32, 5, 3), (81, 4, 3), (125, 3, 2),
           (64, 6, 5), (64, 3, 2), (243, 5, 2), (1000, 3, 2)]


def _bo_can_dep():
    r"""Trả về $(A, n, m, b, kq)$ với $A = b^{n}$ và
    $A^{\frac{m}{n}} = b^{m} = kq$ NGUYÊN."""
    A, n, m = random.choice(CAN_DEP)
    b = int(round(A ** (1.0 / n)))
    return A, n, m, b, b ** m


# Bộ cơ số dùng cho lôgarit.
CO_SO_LOG = [2, 3, 5, 10]


def _muoi_mu(d):
    r"""Viết $10^{d} = kq$; khi $d = 1$ chỉ viết $10$ (không lặp lại)."""
    if d == 1:
        return "10"
    return r"10^{%d} = %d" % (d, 10 ** d)


# =====================================================================
# BÀI 18. LUỸ THỪA VỚI SỐ MŨ THỰC
# =====================================================================

def L11_C6_B18_NB084_MC_A_01(socau, dang=1):
    r"""Nhận biết luỹ thừa với số mũ hữu tỉ.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([2, 3, 4, 5])
        m = random.choice([1, 2, 3, 4, 5, 7])
        if m % n == 0:
            continue
        if (n, m) not in gt:
            gt.append((n, m))

    cauTN = ""
    for n, m in gt:
        dung = "$%s$" % _mu_ps("a", m, n)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _mu_ps("a", n, m), "$%s$" % _mu("a", "%d" % (m * n)),
             "$%s$" % _mu("a", "%d" % (m + n))],
            buoc=lambda t: "$%s$" % _mu_ps("a", m + t, n + t + 1))
        debai = (r"Với $a > 0$, biểu thức $%s$ được viết dưới dạng luỹ thừa "
                 r"với số mũ hữu tỉ là" % _can(n, _mu("a", "%d" % m)))
        giai = (r"Theo định nghĩa luỹ thừa với số mũ hữu tỉ: "
                r"$%s = %s$ với $a > 0$, $n$ nguyên dương."
                % (r"\sqrt[n]{a^{m}}", r"a^{\frac{m}{n}}") +
                "\\\\\n"
                r"Ở đây căn bậc $%d$ nên MẪU của số mũ là $%d$; luỹ thừa "
                r"bên trong căn là $%d$ nên TỬ của số mũ là $%d$."
                % (n, n, m, m) +
                "\\\\\n"
                r"Vậy $%s = %s$." % (_can(n, _mu("a", "%d" % m)),
                                     _mu_ps("a", m, n)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B18_TH085_MC_A_01(socau, dang=1):
    r"""Giải thích tính chất của phép tính luỹ thừa.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p = random.randint(2, 7)
        q = random.randint(2, 7)
        r = random.randint(1, 5)
        if p + q - r <= 0 or (p, q, r) in gt:
            continue
        gt.append((p, q, r))

    cauTN = ""
    for p, q, r in gt:
        k = p + q - r
        dung = "$%s$" % _mu("a", "%d" % k)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _mu("a", "%d" % (p + q + r)),
             "$%s$" % _mu("a", "%d" % (p * q - r)),
             "$%s$" % _mu("a", "%d" % (p + q))],
            buoc=lambda t: "$%s$" % _mu("a", "%d" % (k + t)))
        debai = (r"Với $a > 0$, rút gọn biểu thức "
                 r"$P = \dfrac{%s\cdot %s}{%s}$."
                 % (_mu("a", "%d" % p), _mu("a", "%d" % q),
                    _mu("a", "%d" % r)))
        giai = (r"Nhân hai luỹ thừa cùng cơ số thì CỘNG số mũ: "
                r"$%s\cdot %s = %s$."
                % (_mu("a", "%d" % p), _mu("a", "%d" % q),
                   _mu("a", "%d" % (p + q))) +
                "\\\\\n"
                r"Chia hai luỹ thừa cùng cơ số thì TRỪ số mũ: "
                r"$\dfrac{%s}{%s} = %s$."
                % (_mu("a", "%d" % (p + q)), _mu("a", "%d" % r),
                   _mu("a", "%d" % k)) +
                "\\\\\n"
                r"Vậy $P = %s$." % _mu("a", "%d" % k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B18_TH086_MC_A_01(socau, dang=1):
    r"""Dùng tính chất luỹ thừa để tính giá trị biểu thức số.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_can_dep()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for A, n, m, b, kq in gt:
        dung = "$%d$" % kq
        nhieu = _ba_nhieu6(
            dung,
            ["$%d$" % (A * m), "$%d$" % (b * m), "$%d$" % (A // b)],
            buoc=lambda t: "$%d$" % (kq + t))
        debai = r"Tính giá trị của biểu thức $%s$." % _mu_ps(A, m, n)
        giai = (r"Viết cơ số thành luỹ thừa đúng: $%d = %s$."
                % (A, _mu(b, "%d" % n)) +
                "\\\\\n"
                r"$%s = \left(%s\right)^{\frac{%d}{%d}} = %s = %s = %d$."
                % (_mu_ps(A, m, n), _mu(b, "%d" % n), m, n,
                   _mu(b, r"%d\cdot\frac{%d}{%d}" % (n, m, n)),
                   _mu(b, "%d" % m), kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B18_TH086_SA_A_01(socau):
    r"""Rút gọn biểu thức chứa luỹ thừa - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_can_dep()
        if v not in gt:
            gt.append(v)

    cau = ""
    for A, n, m, b, kq in gt:
        debai = (r"Tính giá trị của biểu thức "
                 r"$P = \dfrac{%s}{%s}$ (viết kết quả dưới dạng số nguyên)."
                 % (_can(n, _mu(A, "%d" % (m + n))), _mu(A, "1")))
        # A^((m+n)/n) / A = b^(m+n) / b^n = b^m
        giai = (r"Đưa về cùng cơ số $%d$: $%d = %s$."
                % (b, A, _mu(b, "%d" % n)) +
                "\\\\\n"
                r"$%s = %s = %s$."
                % (_can(n, _mu(A, "%d" % (m + n))),
                   _mu_ps(A, m + n, n), _mu(b, "%d" % (m + n))) +
                "\\\\\n"
                r"$P = \dfrac{%s}{%s} = %s = %d$."
                % (_mu(b, "%d" % (m + n)), _mu(b, "%d" % n),
                   _mu(b, "%d" % m), kq))
        nhieu = _ba_nhieu6(str(kq), [str(b), str(A), str(kq * b)],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B18_TH087_MC_A_01(socau, dang=1):
    r"""Tính giá trị biểu thức số có chứa luỹ thừa (dùng máy tính cầm tay).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5])
        p = random.randint(3, 6)
        q = random.randint(1, 3)
        if (a, p, q) not in gt:
            gt.append((a, p, q))

    cauTN = ""
    for a, p, q in gt:
        kq = a ** (p - q)
        dung = "$%d$" % kq
        nhieu = _ba_nhieu6(
            dung,
            ["$%d$" % (a ** (p + q)), "$%d$" % (a ** p - a ** q),
             "$%d$" % (a ** (p * q))],
            buoc=lambda t: "$%d$" % (kq + t))
        debai = (r"Tính giá trị của biểu thức "
                 r"$P = \dfrac{%s}{%s}$."
                 % (_mu(a, "%d" % p), _mu(a, "%d" % q)))
        giai = (r"Hai luỹ thừa cùng cơ số $%d$ nên khi chia thì TRỪ số mũ:"
                % a +
                "\\\\\n"
                r"$P = %s = %s = %d$."
                % (_mu(a, r"%d - %d" % (p, q)),
                   _mu(a, "%d" % (p - q)), kq) +
                "\\\\\n"
                r"Kiểm lại bằng máy tính cầm tay: $%d^{%d} = %d$ và "
                r"$%d^{%d} = %d$, thương bằng $%d$."
                % (a, p, a ** p, a, q, a ** q, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# Lãi suất chọn sao cho $\left(1 + r\right)^{n}$ là số thập phân HỮU HẠN.
LAI_SUAT = [Fraction(5, 100), Fraction(10, 100), Fraction(20, 100),
            Fraction(25, 100), Fraction(50, 100)]


def _bo_lai_kep():
    r"""$(P, r, n)$ với $P$ triệu đồng, $r$ là phân số, $n$ năm."""
    P = random.choice([100, 150, 200, 300, 400, 500, 800])
    r = random.choice(LAI_SUAT)
    n = random.choice([2, 3])
    return P, r, n


def _pt_lai(r):
    r"""Viết lãi suất thành phần trăm, ví dụ $10\%$."""
    return r"%s\%%" % _xx(float(r) * 100, 2)


def L11_C6_B18_VD088_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với phép tính luỹ thừa - lãi kép.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_lai_kep()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for P, r, n in gt:
        mot_cong = r"\left(1 + %s\right)" % _xx(float(r), 4)
        dung = "$%d\\cdot %s$ (triệu đồng)" % (P, _mu(mot_cong, "%d" % n))
        nhieu = _ba_nhieu6(
            dung,
            ["$%d\\cdot %s$ (triệu đồng)"
             % (P, _mu(r"\left(1 - %s\right)" % _xx(float(r), 4), "%d" % n)),
             "$%d\\left(1 + %s\\cdot %d\\right)$ (triệu đồng)"
             % (P, _xx(float(r), 4), n),
             "$%d + %s$ (triệu đồng)" % (P, _mu(mot_cong, "%d" % n))],
            buoc=lambda t: "$%d\\cdot %s$ (triệu đồng)"
            % (P, _mu(mot_cong, "%d" % (n + t))))
        debai = (r"Một người gửi tiết kiệm $%d$ triệu đồng theo thể thức "
                 r"lãi kép với lãi suất $%s$ một năm. Sau $%d$ năm, số "
                 r"tiền cả vốn lẫn lãi người đó nhận được là"
                 % (P, _pt_lai(r), n))
        giai = (r"Gọi $P$ là số tiền gửi ban đầu, $r$ là lãi suất một năm." +
                "\\\\\n"
                r"Sau năm thứ nhất: $P + Pr = P\left(1 + r\right)$." +
                "\\\\\n"
                r"Sau năm thứ hai: $P\left(1 + r\right)\left(1 + r\right) "
                r"= P\left(1 + r\right)^{2}$." +
                "\\\\\n"
                r"Lặp lại, sau $n$ năm số tiền là "
                r"$A = P\left(1 + r\right)^{n}$." +
                "\\\\\n"
                r"Thay $P = %d$, $r = %s$, $n = %d$ được "
                r"$A = %d\cdot %s$ (triệu đồng)."
                % (P, _xx(float(r), 4), n, P, _mu(mot_cong, "%d" % n)) +
                "\\\\\n"
                r"Chú ý lãi kép thì lãi được nhập vào vốn, nên phải dùng "
                r"LUỸ THỪA chứ không nhân lãi với số năm.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B18_VD088_SA_A_01(socau):
    r"""Giá trị biểu thức luỹ thừa (máy tính cầm tay) - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_lai_kep()
        if v not in gt:
            gt.append(v)

    cau = ""
    for P, r, n in gt:
        he = (1 + r) ** n
        A = P * he
        dapso = _xx(float(A), 2)
        debai = (r"Một người gửi tiết kiệm $%d$ triệu đồng theo thể thức "
                 r"lãi kép với lãi suất $%s$ một năm. Tính số tiền cả vốn "
                 r"lẫn lãi người đó nhận được sau $%d$ năm (đơn vị: triệu "
                 r"đồng, làm tròn đến hàng phần trăm)."
                 % (P, _pt_lai(r), n))
        giai = (r"Công thức lãi kép: $A = P\left(1 + r\right)^{n}$." +
                "\\\\\n"
                r"$A = %d\cdot\left(1 + %s\right)^{%d} = %d\cdot %s^{%d}$."
                % (P, _xx(float(r), 4), n, P, _xx(float(1 + r), 4), n) +
                "\\\\\n"
                r"Bấm máy tính: $%s^{%d} = %s$."
                % (_xx(float(1 + r), 4), n, _xx(float(he), 8)) +
                "\\\\\n"
                r"$A = %d\cdot %s = %s$ (triệu đồng)."
                % (P, _xx(float(he), 8), dapso))
        nhieu = _ba_nhieu6(dapso,
                           [str(P), _xx(float(P * (1 + r * n)), 2),
                            _xx(float(A) * 2, 2)],
                           buoc=lambda t: _xx(float(A) + t, 2))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B18_VD088_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán lãi kép (thực tiễn gắn với luỹ thừa).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_lai_kep()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for P, r, n in gt:
        A1 = P * (1 + r)
        An = P * (1 + r) ** n
        lai = An - P
        debai = (r"Một người gửi tiết kiệm $%d$ triệu đồng theo thể thức "
                 r"lãi kép với lãi suất $%s$ một năm (lãi mỗi năm được "
                 r"nhập vào vốn)." % (P, _pt_lai(r)))

        hoi_a = r"Tính số tiền nhận được sau $1$ năm."
        giai_a = (r"Sau $1$ năm: $A_1 = P\left(1 + r\right) = "
                  r"%d\cdot %s = %s$ (triệu đồng)."
                  % (P, _xx(float(1 + r), 4), _xx(float(A1), 2)))

        hoi_b = (r"Viết công thức tính số tiền $A_n$ nhận được sau $n$ năm "
                 r"và tính $A_{%d}$." % n)
        giai_b = (r"Mỗi năm số tiền được nhân thêm $\left(1 + r\right)$ nên "
                  r"$A_n = P\left(1 + r\right)^{n}$." +
                  "\\\\\n"
                  r"$A_{%d} = %d\cdot %s^{%d} = %s$ (triệu đồng)."
                  % (n, P, _xx(float(1 + r), 4), n, _xx(float(An), 2)))

        hoi_c = (r"Tính số tiền LÃI người đó nhận được sau $%d$ năm và so "
                 r"sánh với lãi đơn (lãi không nhập vốn)." % n)
        lai_don = P * r * n
        giai_c = (r"Lãi kép: $%s - %d = %s$ (triệu đồng)."
                  % (_xx(float(An), 2), P, _xx(float(lai), 2)) +
                  "\\\\\n"
                  r"Lãi đơn: $%d\cdot %s\cdot %d = %s$ (triệu đồng)."
                  % (P, _xx(float(r), 4), n, _xx(float(lai_don), 2)) +
                  "\\\\\n"
                  r"Vì $%s > %s$ nên lãi kép cho nhiều tiền lãi hơn lãi "
                  r"đơn; phần chênh lệch chính là lãi sinh ra từ tiền lãi "
                  r"của những năm trước."
                  % (_xx(float(lai), 2), _xx(float(lai_don), 2)))

        ds_abcd = [(hoi_a, r"A_1 = %s \text{ triệu đồng}"
                    % _xx(float(A1), 2), giai_a),
                   (hoi_b, r"A_n = P\left(1 + r\right)^{n},\ A_{%d} = %s"
                    % (n, _xx(float(An), 2)), giai_b),
                   (hoi_c, r"\text{Lãi } %s \text{ triệu đồng}"
                    % _xx(float(lai), 2), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 19. LÔGARIT
# =====================================================================

def L11_C6_B19_NB089_MC_A_01(socau, dang=1):
    r"""Nhận biết khái niệm lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice(CO_SO_LOG)
        k = random.randint(2, 5)
        if (a, k) not in gt:
            gt.append((a, k))

    cauTN = ""
    for a, k in gt:
        x = a ** k
        dung = "$%d$" % k
        nhieu = _ba_nhieu6(dung,
                           ["$%d$" % x, "$%d$" % a, "$%d$" % (x // a)],
                           buoc=lambda t: "$%d$" % (k + t))
        debai = r"Giá trị của $%s$ bằng" % _log(a, "%d" % x)
        giai = (r"Theo định nghĩa: $%s = c \Leftrightarrow %s = %d$."
                % (_log(a, "%d" % x), _mu(a, "c"), x) +
                "\\\\\n"
                r"Ta có $%d = %s$ nên $c = %d$."
                % (x, _mu(a, "%d" % k), k) +
                "\\\\\n"
                r"Vậy $%s = %d$." % (_log(a, "%d" % x), k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B19_NB089_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán tăng trưởng dùng lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        N0 = random.choice([100, 200, 500, 1000, 2000])
        t1 = random.randint(2, 4)
        k = random.randint(5, 9)
        if (N0, t1, k) not in gt:
            gt.append((N0, t1, k))

    cauTN = ""
    for N0, t1, k in gt:
        N1 = N0 * 2 ** t1
        Nk = N0 * 2 ** k
        debai = (r"Số lượng vi khuẩn trong một mẫu thí nghiệm được cho bởi "
                 r"công thức $N\left(t\right) = %d\cdot 2^{\,t}$, trong đó "
                 r"$t$ tính bằng giờ." % N0)

        hoi_a = r"Tính số vi khuẩn sau $%d$ giờ." % t1
        giai_a = (r"$N\left(%d\right) = %d\cdot 2^{%d} = %d\cdot %d = %d$ "
                  r"(con)." % (t1, N0, t1, N0, 2 ** t1, N1))

        hoi_b = (r"Sau bao nhiêu giờ thì số vi khuẩn đạt $%d$ con?" % Nk)
        giai_b = (r"Giải phương trình $%d\cdot 2^{\,t} = %d$." % (N0, Nk) +
                  "\\\\\n"
                  r"$2^{\,t} = \dfrac{%d}{%d} = %d$." % (Nk, N0, 2 ** k) +
                  "\\\\\n"
                  r"Theo định nghĩa lôgarit: $t = %s = %d$ (giờ)."
                  % (_log(2, "%d" % (2 ** k)), k))

        hoi_c = (r"Viết công thức tính thời gian $t$ để số vi khuẩn đạt "
                 r"$N$ con.")
        giai_c = (r"Từ $%d\cdot 2^{\,t} = N$ suy ra "
                  r"$2^{\,t} = \dfrac{N}{%d}$." % (N0, N0) +
                  "\\\\\n"
                  r"Theo định nghĩa lôgarit: "
                  r"$t = \log_{2}\dfrac{N}{%d}$ (giờ)." % N0 +
                  "\\\\\n"
                  r"Điều kiện $N > 0$; công thức này đúng với mọi $N$ lớn "
                  r"hơn $0$, không cần $\dfrac{N}{%d}$ là luỹ thừa của "
                  r"$2$." % N0)

        ds_abcd = [(hoi_a, r"N\left(%d\right) = %d" % (t1, N1), giai_a),
                   (hoi_b, r"t = %d \text{ giờ}" % k, giai_b),
                   (hoi_c, r"t = \log_{2}\dfrac{N}{%d}" % N0, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L11_C6_B19_TH090_MC_A_01(socau, dang=1):
    r"""Giải thích tính chất của phép tính lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"$\log_a\left(xy\right) = \log_a x + \log_a y$",
         [r"$\log_a\left(xy\right) = \log_a x\cdot\log_a y$",
          r"$\log_a\left(xy\right) = \log_a x - \log_a y$",
          r"$\log_a\left(x + y\right) = \log_a x + \log_a y$"],
         r"Lôgarit của một TÍCH bằng TỔNG các lôgarit.",
         r"Lôgarit không biến tích thành tích, cũng không biến tổng "
         r"thành tổng."),
        (r"$\log_a\dfrac{x}{y} = \log_a x - \log_a y$",
         [r"$\log_a\dfrac{x}{y} = \dfrac{\log_a x}{\log_a y}$",
          r"$\log_a\dfrac{x}{y} = \log_a x + \log_a y$",
          r"$\log_a\left(x - y\right) = \log_a x - \log_a y$"],
         r"Lôgarit của một THƯƠNG bằng HIỆU các lôgarit.",
         r"Thương của hai lôgarit là công thức ĐỔI CƠ SỐ, khác hẳn "
         r"lôgarit của một thương."),
        (r"$\log_a x^{\alpha} = \alpha\log_a x$",
         [r"$\log_a x^{\alpha} = \left(\log_a x\right)^{\alpha}$",
          r"$\log_a x^{\alpha} = \log_a \alpha\cdot\log_a x$",
          r"$\log_{a^{\alpha}} x = \alpha\log_a x$"],
         r"Số mũ của đối số được đưa ra TRƯỚC dấu lôgarit.",
         r"$\log_a x^{\alpha}$ khác $\left(\log_a x\right)^{\alpha}$; "
         r"còn $\log_{a^{\alpha}} x = \dfrac{1}{\alpha}\log_a x$."),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(MAU))
        if i not in gt:
            gt.append(i)

    cauTN = ""
    for i in gt:
        dung, nhieu, y_nghia, luu_y = MAU[i]
        debai = (r"Với $a > 0$, $a \neq 1$ và $x$, $y$, $\alpha$ thoả mãn "
                 r"điều kiện có nghĩa, khẳng định nào sau đây ĐÚNG?")
        giai = y_nghia + "\\\\\n" + luu_y
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), giai, 0, 0, dang)
    return cauTN


def L11_C6_B19_TH091_MC_A_01(socau, dang=1):
    r"""Dùng tính chất lôgarit để tính giá trị biểu thức số.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice(CO_SO_LOG)
        p = random.randint(1, 4)
        q = random.randint(1, 4)
        if (a, p, q) not in gt:
            gt.append((a, p, q))

    cauTN = ""
    for a, p, q in gt:
        x, y = a ** p, a ** q
        kq = p + q
        dung = "$%d$" % kq
        nhieu = _ba_nhieu6(
            dung,
            ["$%d$" % (p * q), "$%d$" % (x * y), "$%d$" % abs(p - q)],
            buoc=lambda t: "$%d$" % (kq + t))
        debai = (r"Tính giá trị của biểu thức $P = %s + %s$."
                 % (_log(a, "%d" % x), _log(a, "%d" % y)))
        giai = (r"Tổng hai lôgarit cùng cơ số bằng lôgarit của TÍCH:" +
                "\\\\\n"
                r"$P = %s = %s$."
                % (_log(a, r"\left(%d\cdot %d\right)" % (x, y)),
                   _log(a, "%d" % (x * y))) +
                "\\\\\n"
                r"Vì $%d = %s$ nên $P = %d$."
                % (x * y, _mu(a, "%d" % kq), kq) +
                "\\\\\n"
                r"Cách khác: $%s = %d$ và $%s = %d$ nên $P = %d + %d = %d$."
                % (_log(a, "%d" % x), p, _log(a, "%d" % y), q, p, q, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B19_TH091_SA_A_01(socau):
    r"""Tính giá trị biểu thức lôgarit - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice(CO_SO_LOG)
        p = random.randint(3, 6)
        q = random.randint(1, 2)
        if (a, p, q) not in gt:
            gt.append((a, p, q))

    cau = ""
    for a, p, q in gt:
        x, y = a ** p, a ** q
        kq = p - q
        debai = (r"Tính giá trị của biểu thức $P = %s - %s$."
                 % (_log(a, "%d" % x), _log(a, "%d" % y)))
        giai = (r"Hiệu hai lôgarit cùng cơ số bằng lôgarit của THƯƠNG:" +
                "\\\\\n"
                r"$P = %s = %s$."
                % (_log(a, r"\dfrac{%d}{%d}" % (x, y)),
                   _log(a, "%d" % (x // y))) +
                "\\\\\n"
                r"Vì $%d = %s$ nên $P = %d$."
                % (x // y, _mu(a, "%d" % kq), kq))
        nhieu = _ba_nhieu6(str(kq), [str(p + q), str(x // y), str(p * q)],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B19_TH092_MC_A_01(socau, dang=1):
    r"""Tính giá trị của lôgarit (có thể dùng máy tính cầm tay).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5])
        k = random.randint(2, 5)
        m = random.choice([2, 3])
        if (a, k, m) not in gt:
            gt.append((a, k, m))

    cauTN = ""
    for a, k, m in gt:
        # log_{a^m}(a^(k*m)) = k
        co_so = a ** m
        x = a ** (k * m)
        dung = "$%d$" % k
        nhieu = _ba_nhieu6(
            dung,
            ["$%d$" % (k * m), "$%d$" % m, "$%d$" % (k + m)],
            buoc=lambda t: "$%d$" % (k + t))
        debai = r"Tính giá trị của $%s$." % _log(co_so, "%d" % x)
        giai = (r"Đưa cả cơ số và đối số về luỹ thừa của $%d$: "
                r"$%d = %s$ và $%d = %s$."
                % (a, co_so, _mu(a, "%d" % m), x, _mu(a, "%d" % (k * m))) +
                "\\\\\n"
                r"$%s = \dfrac{%s}{%s} = \dfrac{%d}{%d} = %d$."
                % (_log(co_so, "%d" % x), _log(a, "%d" % x),
                   _log(a, "%d" % co_so), k * m, m, k) +
                "\\\\\n"
                r"(Đã dùng công thức đổi cơ số "
                r"$\log_a b = \dfrac{\log_c b}{\log_c a}$.)")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B19_TH092_SA_A_01(socau):
    r"""Rút gọn biểu thức chứa lôgarit - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice(CO_SO_LOG)
        p = random.randint(2, 5)
        al = random.randint(2, 4)
        if (a, p, al) not in gt:
            gt.append((a, p, al))

    cau = ""
    for a, p, al in gt:
        x = a ** p
        kq = al * p
        debai = (r"Tính giá trị của biểu thức $P = %s$."
                 % _log(a, _mu("%d" % x, "%d" % al)))
        giai = (r"Đưa số mũ ra trước dấu lôgarit: "
                r"$%s = %d\cdot %s$."
                % (_log(a, _mu("%d" % x, "%d" % al)), al,
                   _log(a, "%d" % x)) +
                "\\\\\n"
                r"Mà $%s = %d$ vì $%d = %s$."
                % (_log(a, "%d" % x), p, x, _mu(a, "%d" % p)) +
                "\\\\\n"
                r"Vậy $P = %d\cdot %d = %d$." % (al, p, kq))
        nhieu = _ba_nhieu6(str(kq), [str(al + p), str(p), str(al)],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B19_VD093_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với lôgarit - độ Richter của động đất.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.randint(3, 8)
        if k not in gt:
            gt.append(k)

    cauTN = ""
    for k in gt:
        dung = "$%d$" % k
        nhieu = _ba_nhieu6(dung,
                           ["$%d$" % (10 * k), "$%d$" % (k + 1),
                            "$%d$" % (10 ** 1)],
                           buoc=lambda t: "$%d$" % (k + t + 1))
        debai = (r"Độ lớn $M$ (theo thang Richter) của một trận động đất "
                 r"được tính bởi công thức "
                 r"$M = \log\dfrac{I}{I_0}$, trong đó $I$ là cường độ của "
                 r"trận động đất và $I_0$ là cường độ chuẩn. Một trận động "
                 r"đất có cường độ gấp $10^{%d}$ lần cường độ chuẩn thì có "
                 r"độ lớn bằng" % k)
        giai = (r"Theo giả thiết $I = 10^{%d}I_0$ nên "
                r"$\dfrac{I}{I_0} = 10^{%d}$." % (k, k) +
                "\\\\\n"
                r"$M = \log 10^{%d} = %d\cdot\log 10 = %d\cdot 1 = %d$."
                % (k, k, k, k) +
                "\\\\\n"
                r"Vậy trận động đất đó có độ lớn $%d$ độ Richter." % k)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B19_VD093_SA_A_01(socau):
    r"""So sánh cường độ hai trận động đất - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        m2 = random.randint(3, 5)
        d = random.randint(1, 3)
        m1 = m2 + d
        if (m1, m2) not in gt:
            gt.append((m1, m2))

    cau = ""
    for m1, m2 in gt:
        kq = 10 ** (m1 - m2)
        debai = (r"Độ lớn $M$ theo thang Richter của một trận động đất "
                 r"được tính bởi $M = \log\dfrac{I}{I_0}$, trong đó $I$ là "
                 r"cường độ trận động đất và $I_0$ là cường độ chuẩn. Trận "
                 r"động đất $A$ có độ lớn $%d$, trận động đất $B$ có độ "
                 r"lớn $%d$. Cường độ trận $A$ gấp bao nhiêu lần cường độ "
                 r"trận $B$?" % (m1, m2))
        giai = (r"Từ $M = \log\dfrac{I}{I_0}$ suy ra "
                r"$\dfrac{I}{I_0} = 10^{M}$, tức là $I = I_0\cdot 10^{M}$." +
                "\\\\\n"
                r"$I_A = I_0\cdot 10^{%d}$ và $I_B = I_0\cdot 10^{%d}$."
                % (m1, m2) +
                "\\\\\n"
                r"$\dfrac{I_A}{I_B} = \dfrac{10^{%d}}{10^{%d}} "
                r"= %s$." % (m1, m2, _muoi_mu(m1 - m2)) +
                "\\\\\n"
                r"Vậy cường độ trận $A$ gấp $%d$ lần trận $B$ (chênh lệch "
                r"$1$ độ Richter ứng với cường độ gấp $10$ lần)." % kq)
        nhieu = _ba_nhieu6(str(kq), [str(m1 - m2), str(m1 + m2),
                                     str(10 * (m1 - m2))],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B19_VD093_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về độ Richter.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        m1 = random.randint(5, 8)
        d = random.randint(1, 3)
        m2 = m1 - d
        k = random.randint(2, 4)
        if (m1, m2, k) not in gt:
            gt.append((m1, m2, k))

    cauTN = ""
    for m1, m2, k in gt:
        ti = 10 ** (m1 - m2)
        debai = (r"Độ lớn $M$ theo thang Richter của một trận động đất "
                 r"được tính bởi công thức $M = \log\dfrac{I}{I_0}$, trong "
                 r"đó $I$ là cường độ của trận động đất và $I_0$ là cường "
                 r"độ chuẩn.")

        hoi_a = (r"Một trận động đất có cường độ $I = 10^{%d}I_0$. Tính "
                 r"độ lớn của trận động đất đó." % k)
        giai_a = (r"$M = \log\dfrac{10^{%d}I_0}{I_0} = \log 10^{%d} = %d$."
                  % (k, k, k) +
                  "\\\\\n"
                  r"Vậy trận động đất có độ lớn $%d$ độ Richter." % k)

        hoi_b = (r"Trận động đất $A$ có độ lớn $%d$, trận $B$ có độ lớn "
                 r"$%d$. Cường độ trận $A$ gấp bao nhiêu lần trận $B$?"
                 % (m1, m2))
        giai_b = (r"Từ công thức suy ra $I = I_0\cdot 10^{M}$." +
                  "\\\\\n"
                  r"$\dfrac{I_A}{I_B} = \dfrac{I_0\cdot 10^{%d}}"
                  r"{I_0\cdot 10^{%d}} = %s$."
                  % (m1, m2, _muoi_mu(m1 - m2)) +
                  "\\\\\n"
                  r"Vậy cường độ trận $A$ gấp $%d$ lần trận $B$." % ti)

        hoi_c = (r"Giải thích vì sao độ lớn chỉ hơn kém nhau vài đơn vị mà "
                 r"mức tàn phá lại chênh lệch rất nhiều.")
        giai_c = (r"Thang Richter là thang LÔGARIT: mỗi khi độ lớn tăng "
                  r"thêm $1$ đơn vị thì cường độ $I$ tăng gấp $10$ lần." +
                  "\\\\\n"
                  r"Tăng $%d$ đơn vị thì cường độ tăng gấp "
                  r"$%s$ lần." % (m1 - m2, _muoi_mu(m1 - m2)) +
                  "\\\\\n"
                  r"Vì vậy chênh lệch nhỏ trên thang đo lại ứng với chênh "
                  r"lệch rất lớn về năng lượng và mức tàn phá.")

        ds_abcd = [(hoi_a, r"M = %d" % k, giai_a),
                   (hoi_b, r"\dfrac{I_A}{I_B} = %d" % ti, giai_b),
                   (hoi_c, r"\text{Vì thang Richter là thang lôgarit}",
                    giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 20. HÀM SỐ MŨ VÀ HÀM SỐ LÔGARIT
# =====================================================================

def _hinh_ham_mu(a):
    r"""Đồ thị $y = a^{x}$ vẽ bằng TikZ THUẦN (không dùng pgfplots)."""
    x_tu, x_den = -2.6, 2.6
    y_den = 6.0
    return (
        "\\begin{tikzpicture}[>=stealth,x=0.85cm,y=0.42cm,thick,"
        "line join=round,font=\\footnotesize]\n"
        "\\draw[->] (%s,0) -- (%s,0) node[below right]{$x$};\n"
        % (_toa(x_tu - 0.4), _toa(x_den + 0.5)) +
        "\\draw[->] (0,-0.8) -- (0,%s) node[left]{$y$};\n" % _toa(y_den + 0.8) +
        "\\node[below left] at (0,0) {$O$};\n"
        "\\node[left] at (0,1) {$1$};\n"
        "\\fill[black] (0,1) circle[radius=1.6pt];\n"
        "\\clip (%s,-0.8) rectangle (%s,%s);\n"
        % (_toa(x_tu - 0.4), _toa(x_den + 0.5), _toa(y_den + 0.8)) +
        "\\draw[very thick,smooth,samples=160,domain=%s:%s] "
        "plot(\\x,{pow(%s,\\x)});\n" % (_toa(x_tu), _toa(x_den), _toa(a)) +
        "\\end{tikzpicture}")


def _hinh_ham_log(a):
    r"""Đồ thị $y = \log_a x$ vẽ bằng TikZ THUẦN."""
    x_den = 6.0
    return (
        "\\begin{tikzpicture}[>=stealth,x=0.42cm,y=0.85cm,thick,"
        "line join=round,font=\\footnotesize]\n"
        "\\draw[->] (-0.8,0) -- (%s,0) node[below right]{$x$};\n"
        % _toa(x_den + 0.8) +
        "\\draw[->] (0,-2.8) -- (0,2.8) node[left]{$y$};\n"
        "\\node[below left] at (0,0) {$O$};\n"
        "\\node[below] at (1,0) {$1$};\n"
        "\\fill[black] (1,0) circle[radius=1.6pt];\n"
        "\\clip (-0.8,-2.8) rectangle (%s,2.8);\n" % _toa(x_den + 0.8) +
        "\\draw[very thick,smooth,samples=200,domain=0.08:%s] "
        "plot(\\x,{ln(\\x)/ln(%s)});\n" % (_toa(x_den), _toa(a)) +
        "\\end{tikzpicture}")


def L11_C6_B20_NB094_MC_A_01(socau, dang=1):
    r"""Nhận biết hàm số mũ và hàm số lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5, 10])
        loai = random.choice(["mu", "log"])
        if (a, loai) not in gt:
            gt.append((a, loai))

    cauTN = ""
    for a, loai in gt:
        if loai == "mu":
            dung = "$y = %s$" % _mu(a, "x")
            nhieu = ["$y = %s$" % _mu("x", "%d" % a),
                     "$y = %s$" % _log(a, "x"),
                     "$y = %dx$" % a]
            ten = "hàm số mũ"
            giai = (r"Hàm số mũ có dạng $y = a^{x}$ với $a > 0$, "
                    r"$a \neq 1$: BIẾN nằm ở SỐ MŨ." +
                    "\\\\\n"
                    r"$y = %s$ có biến $x$ ở số mũ nên là hàm số mũ."
                    % _mu(a, "x") +
                    "\\\\\n"
                    r"$y = %s$ là hàm số luỹ thừa (biến ở cơ số); "
                    r"$y = %s$ là hàm số lôgarit; $y = %dx$ là hàm bậc "
                    r"nhất." % (_mu("x", "%d" % a), _log(a, "x"), a))
        else:
            dung = "$y = %s$" % _log(a, "x")
            nhieu = ["$y = %s$" % _mu(a, "x"),
                     "$y = %s$" % _mu("x", "%d" % a),
                     "$y = %dx$" % a]
            ten = "hàm số lôgarit"
            giai = (r"Hàm số lôgarit có dạng $y = \log_a x$ với $a > 0$, "
                    r"$a \neq 1$ và $x > 0$." +
                    "\\\\\n"
                    r"$y = %s$ đúng dạng đó nên là hàm số lôgarit."
                    % _log(a, "x") +
                    "\\\\\n"
                    r"$y = %s$ là hàm số mũ; $y = %s$ là hàm số luỹ thừa; "
                    r"$y = %dx$ là hàm bậc nhất."
                    % (_mu(a, "x"), _mu("x", "%d" % a), a))
        debai = r"Trong các hàm số sau, hàm số nào là %s?" % ten
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B20_NB094_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán về độ pH.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p1 = random.randint(3, 6)
        p2 = random.randint(7, 10)
        if (p1, p2) not in gt:
            gt.append((p1, p2))

    cauTN = ""
    for p1, p2 in gt:
        ti = 10 ** (p2 - p1)
        debai = (r"Độ pH của một dung dịch được tính theo công thức "
                 r"$\text{pH} = -\log\left[\text{H}^{+}\right]$, trong đó "
                 r"$\left[\text{H}^{+}\right]$ là nồng độ ion hiđrô "
                 r"(đơn vị: mol/l).")

        hoi_a = (r"Một dung dịch có "
                 r"$\left[\text{H}^{+}\right] = 10^{-%d}$ mol/l. Tính độ "
                 r"pH của dung dịch đó." % p1)
        giai_a = (r"$\text{pH} = -\log 10^{-%d} = -\left(-%d\right)"
                  r"\log 10 = %d$." % (p1, p1, p1) +
                  "\\\\\n"
                  r"Vậy dung dịch có độ pH bằng $%d$." % p1)

        hoi_b = (r"Một dung dịch khác có độ pH bằng $%d$. Tính nồng độ "
                 r"ion hiđrô của dung dịch này." % p2)
        giai_b = (r"Từ $\text{pH} = -\log\left[\text{H}^{+}\right] = %d$ "
                  r"suy ra $\log\left[\text{H}^{+}\right] = -%d$."
                  % (p2, p2) +
                  "\\\\\n"
                  r"Theo định nghĩa lôgarit: "
                  r"$\left[\text{H}^{+}\right] = 10^{-%d}$ mol/l." % p2)

        hoi_c = (r"Nồng độ ion hiđrô của dung dịch thứ nhất gấp bao nhiêu "
                 r"lần dung dịch thứ hai? Dung dịch nào có tính axit "
                 r"mạnh hơn?")
        giai_c = (r"$\dfrac{10^{-%d}}{10^{-%d}} = 10^{%d} = %d$ lần."
                  % (p1, p2, p2 - p1, ti) +
                  "\\\\\n"
                  r"Dung dịch thứ nhất có nồng độ ion hiđrô lớn hơn nên "
                  r"có tính axit mạnh hơn." +
                  "\\\\\n"
                  r"Độ pH càng NHỎ thì tính axit càng MẠNH, vì trước "
                  r"lôgarit có dấu trừ.")

        ds_abcd = [(hoi_a, r"\text{pH} = %d" % p1, giai_a),
                   (hoi_b, r"\left[\text{H}^{+}\right] = 10^{-%d}"
                    r"\ \text{mol/l}" % p2, giai_b),
                   (hoi_c, r"\text{Gấp } %d \text{ lần}" % ti, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L11_C6_B20_TH095_MC_A_01(socau, dang=1):
    r"""Nhận dạng đồ thị của hàm số mũ, hàm số lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3])
        loai = random.choice(["mu", "log"])
        if (a, loai) not in gt:
            gt.append((a, loai))

    cauTN = ""
    for a, loai in gt:
        if loai == "mu":
            hinh = _hinh_ham_mu(a)
            dung = "$y = %s$" % _mu(a, "x")
            nhieu = ["$y = %s$" % _log(a, "x"),
                     r"$y = \left(\dfrac{1}{%d}\right)^{x}$" % a,
                     "$y = -%s$" % _mu(a, "x")]
            giai = (r"Đồ thị nằm hoàn toàn PHÍA TRÊN trục hoành và đi qua "
                    r"điểm $\left(0;\ 1\right)$ nên đây là đồ thị hàm số "
                    r"mũ $y = a^{x}$." +
                    "\\\\\n"
                    r"Đồ thị ĐI LÊN từ trái sang phải nên hàm số đồng "
                    r"biến, tức là $a > 1$." +
                    "\\\\\n"
                    r"Đồ thị đi qua $\left(1;\ %d\right)$ nên $a = %d$, "
                    r"vậy hàm số là $y = %s$." % (a, a, _mu(a, "x")) +
                    "\\\\\n"
                    r"Loại $y = %s$ vì đồ thị hàm lôgarit cắt trục hoành "
                    r"tại $\left(1;\ 0\right)$; loại "
                    r"$y = \left(\dfrac{1}{%d}\right)^{x}$ vì đồ thị đó đi "
                    r"xuống; loại $y = -%s$ vì đồ thị đó nằm dưới trục "
                    r"hoành." % (_log(a, "x"), a, _mu(a, "x")))
        else:
            hinh = _hinh_ham_log(a)
            dung = "$y = %s$" % _log(a, "x")
            nhieu = ["$y = %s$" % _mu(a, "x"),
                     r"$y = \log_{\frac{1}{%d}}x$" % a,
                     "$y = %s$" % _mu("x", "%d" % a)]
            giai = (r"Đồ thị chỉ nằm bên PHẢI trục tung (tập xác định "
                    r"$x > 0$) và cắt trục hoành tại $\left(1;\ 0\right)$ "
                    r"nên đây là đồ thị hàm số lôgarit $y = \log_a x$." +
                    "\\\\\n"
                    r"Đồ thị ĐI LÊN từ trái sang phải nên hàm số đồng "
                    r"biến, tức là $a > 1$." +
                    "\\\\\n"
                    r"Đồ thị đi qua $\left(%d;\ 1\right)$ nên $a = %d$, "
                    r"vậy hàm số là $y = %s$."
                    % (a, a, _log(a, "x")) +
                    "\\\\\n"
                    r"Loại $y = %s$ vì đồ thị hàm số mũ đi qua "
                    r"$\left(0;\ 1\right)$; loại "
                    r"$y = \log_{\frac{1}{%d}}x$ vì đồ thị đó đi xuống."
                    % (_mu(a, "x"), a))
        debai = r"Hình vẽ sau là đồ thị của hàm số nào?"
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L11_C6_B20_TH096_MC_A_01(socau, dang=1):
    r"""Giải thích tính chất của hàm số mũ, lôgarit qua đồ thị.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3])
        loai = random.choice(["mu", "log"])
        if (a, loai) not in gt:
            gt.append((a, loai))

    cauTN = ""
    for a, loai in gt:
        if loai == "mu":
            hinh = _hinh_ham_mu(a)
            dung = (r"Hàm số đồng biến trên $\mathbb{R}$ và có tập giá trị "
                    r"$\left(0;\ +\infty\right)$.")
            nhieu = [r"Hàm số nghịch biến trên $\mathbb{R}$.",
                     r"Hàm số có tập giá trị $\mathbb{R}$.",
                     r"Hàm số có tập xác định $\left(0;\ +\infty\right)$."]
            giai = (r"Đồ thị $y = %s$ ĐI LÊN từ trái sang phải trên toàn "
                    r"trục số nên hàm số đồng biến trên $\mathbb{R}$."
                    % _mu(a, "x") +
                    "\\\\\n"
                    r"Đồ thị nằm hoàn toàn phía trên trục hoành và nhận "
                    r"trục hoành làm tiệm cận ngang, nên tập giá trị là "
                    r"$\left(0;\ +\infty\right)$." +
                    "\\\\\n"
                    r"Tập xác định của hàm số mũ là $\mathbb{R}$, còn "
                    r"$\left(0;\ +\infty\right)$ mới là TẬP GIÁ TRỊ.")
        else:
            hinh = _hinh_ham_log(a)
            dung = (r"Hàm số đồng biến trên $\left(0;\ +\infty\right)$ và "
                    r"có tập giá trị $\mathbb{R}$.")
            nhieu = [r"Hàm số nghịch biến trên $\left(0;\ +\infty\right)$.",
                     r"Hàm số có tập xác định $\mathbb{R}$.",
                     r"Hàm số có tập giá trị $\left(0;\ +\infty\right)$."]
            giai = (r"Đồ thị $y = %s$ chỉ nằm bên phải trục tung nên tập "
                    r"xác định là $\left(0;\ +\infty\right)$."
                    % _log(a, "x") +
                    "\\\\\n"
                    r"Đồ thị ĐI LÊN từ trái sang phải nên hàm số đồng biến "
                    r"trên $\left(0;\ +\infty\right)$." +
                    "\\\\\n"
                    r"Khi $x$ chạy khắp $\left(0;\ +\infty\right)$ thì $y$ "
                    r"nhận mọi giá trị thực, nên tập giá trị là "
                    r"$\mathbb{R}$.")
        debai = (r"Dựa vào đồ thị dưới đây, khẳng định nào sau đây về hàm "
                 r"số ĐÚNG?")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L11_C6_B20_VD097_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với hàm số mũ - sự phân rã phóng xạ.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        m0 = random.choice([16, 32, 64, 100, 128, 200, 256])
        T = random.choice([5, 8, 10, 12, 20, 25])
        if (m0, T) not in gt:
            gt.append((m0, T))

    cauTN = ""
    for m0, T in gt:
        ct = r"m\left(t\right) = %d\cdot\left(\dfrac{1}{2}\right)" \
             r"^{\frac{t}{%d}}" % (m0, T)
        dung = "$%s$" % ct
        nhieu = _ba_nhieu6(
            dung,
            [r"$m\left(t\right) = %d\cdot 2^{\frac{t}{%d}}$" % (m0, T),
             r"$m\left(t\right) = %d\cdot\left(\dfrac{1}{2}\right)"
             r"^{%dt}$" % (m0, T),
             r"$m\left(t\right) = %d - \dfrac{t}{%d}$" % (m0, T)],
            buoc=lambda k: r"$m\left(t\right) = %d\cdot\left("
            r"\dfrac{1}{2}\right)^{\frac{t}{%d}}$" % (m0, T + k))
        debai = (r"Một chất phóng xạ có khối lượng ban đầu $%d$ gam và có "
                 r"chu kì bán rã $%d$ ngày (cứ sau $%d$ ngày thì khối "
                 r"lượng còn lại một nửa). Công thức tính khối lượng chất "
                 r"phóng xạ còn lại sau $t$ ngày là"
                 % (m0, T, T))
        giai = (r"Cứ mỗi $%d$ ngày khối lượng lại nhân với $\dfrac{1}{2}$."
                % T +
                "\\\\\n"
                r"Sau $t$ ngày, số lần bán rã là $\dfrac{t}{%d}$." % T +
                "\\\\\n"
                r"Vậy $%s$." % ct +
                "\\\\\n"
                r"Chú ý cơ số phải là $\dfrac{1}{2}$ (khối lượng GIẢM), và "
                r"số mũ là $\dfrac{t}{%d}$ chứ không phải $%dt$." % (T, T))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B20_VD097_SA_A_01(socau):
    r"""Phân rã phóng xạ - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.randint(2, 5)
        b = random.choice([1, 2, 3, 5])
        m0 = b * 2 ** k          # de m0 / 2^k NGUYEN
        T = random.choice([5, 8, 10, 12, 20, 25])
        if (m0, T, k) not in gt:
            gt.append((m0, T, k))

    cau = ""
    for m0, T, k in gt:
        con = m0 // 2 ** k
        t = k * T
        debai = (r"Một chất phóng xạ có khối lượng ban đầu $%d$ gam và có "
                 r"chu kì bán rã $%d$ ngày. Hỏi sau $%d$ ngày thì khối "
                 r"lượng chất phóng xạ còn lại bao nhiêu gam?"
                 % (m0, T, t))
        giai = (r"Công thức khối lượng còn lại: "
                r"$m\left(t\right) = %d\cdot\left(\dfrac{1}{2}\right)"
                r"^{\frac{t}{%d}}$." % (m0, T) +
                "\\\\\n"
                r"Với $t = %d$ ngày: $\dfrac{t}{%d} = \dfrac{%d}{%d} = %d$ "
                r"(đã qua $%d$ chu kì bán rã)." % (t, T, t, T, k, k) +
                "\\\\\n"
                r"$m\left(%d\right) = %d\cdot\left(\dfrac{1}{2}\right)"
                r"^{%d} = \dfrac{%d}{%d} = %d$ (gam)."
                % (t, m0, k, m0, 2 ** k, con))
        nhieu = _ba_nhieu6(str(con), [str(m0), str(m0 // 2), str(k)],
                           buoc=lambda x: str(con + x))
        cau += MC_SA_answer_const(debai, str(con), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B20_VD097_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về hàm số mũ (phân rã phóng xạ).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.randint(2, 4)
        b = random.choice([1, 2, 3, 5])
        m0 = b * 2 ** k
        T = random.choice([5, 8, 10, 12, 20, 25])
        if (m0, T, k) not in gt:
            gt.append((m0, T, k))

    cauTN = ""
    for m0, T, k in gt:
        con = m0 // 2 ** k
        t = k * T
        debai = (r"Một chất phóng xạ có khối lượng ban đầu $%d$ gam và có "
                 r"chu kì bán rã $%d$ ngày (cứ sau $%d$ ngày thì khối "
                 r"lượng còn lại một nửa)." % (m0, T, T))

        hoi_a = (r"Viết công thức tính khối lượng $m\left(t\right)$ còn "
                 r"lại sau $t$ ngày.")
        giai_a = (r"Sau mỗi $%d$ ngày khối lượng nhân với $\dfrac{1}{2}$, "
                  r"nên sau $t$ ngày đã qua $\dfrac{t}{%d}$ chu kì."
                  % (T, T) +
                  "\\\\\n"
                  r"$m\left(t\right) = %d\cdot\left(\dfrac{1}{2}\right)"
                  r"^{\frac{t}{%d}}$ (gam)." % (m0, T))

        hoi_b = r"Tính khối lượng còn lại sau $%d$ ngày." % t
        giai_b = (r"$\dfrac{%d}{%d} = %d$ nên đã qua $%d$ chu kì bán rã."
                  % (t, T, k, k) +
                  "\\\\\n"
                  r"$m\left(%d\right) = %d\cdot\left(\dfrac{1}{2}\right)"
                  r"^{%d} = \dfrac{%d}{%d} = %d$ (gam)."
                  % (t, m0, k, m0, 2 ** k, con))

        hoi_c = (r"Sau bao nhiêu ngày thì khối lượng chất phóng xạ còn "
                 r"lại $%d$ gam?" % (m0 // 2 ** (k + 1))
                 if m0 % 2 ** (k + 1) == 0 else
                 r"Viết công thức tính thời gian $t$ để khối lượng còn "
                 r"lại bằng $m$ gam.")
        if m0 % 2 ** (k + 1) == 0:
            giai_c = (r"Giải $%d\cdot\left(\dfrac{1}{2}\right)"
                      r"^{\frac{t}{%d}} = %d$."
                      % (m0, T, m0 // 2 ** (k + 1)) +
                      "\\\\\n"
                      r"$\left(\dfrac{1}{2}\right)^{\frac{t}{%d}} = "
                      r"\dfrac{1}{%d} = \left(\dfrac{1}{2}\right)^{%d}$."
                      % (T, 2 ** (k + 1), k + 1) +
                      "\\\\\n"
                      r"Hai luỹ thừa cùng cơ số bằng nhau nên "
                      r"$\dfrac{t}{%d} = %d \Rightarrow t = %d$ (ngày)."
                      % (T, k + 1, (k + 1) * T))
            dap_c = r"t = %d \text{ ngày}" % ((k + 1) * T)
        else:
            giai_c = (r"Giải $%d\cdot\left(\dfrac{1}{2}\right)"
                      r"^{\frac{t}{%d}} = m$." % (m0, T) +
                      "\\\\\n"
                      r"$\left(\dfrac{1}{2}\right)^{\frac{t}{%d}} = "
                      r"\dfrac{m}{%d}$." % (T, m0) +
                      "\\\\\n"
                      r"Lấy lôgarit cơ số $\dfrac{1}{2}$ hai vế: "
                      r"$\dfrac{t}{%d} = \log_{\frac{1}{2}}\dfrac{m}{%d}$."
                      % (T, m0) +
                      "\\\\\n"
                      r"Vậy $t = %d\log_{\frac{1}{2}}\dfrac{m}{%d}$ (ngày)."
                      % (T, m0))
            dap_c = r"t = %d\log_{\frac{1}{2}}\dfrac{m}{%d}" % (T, m0)

        ds_abcd = [(hoi_a, r"m\left(t\right) = %d\cdot\left("
                    r"\dfrac{1}{2}\right)^{\frac{t}{%d}}" % (m0, T), giai_a),
                   (hoi_b, r"m\left(%d\right) = %d \text{ gam}" % (t, con),
                    giai_b),
                   (hoi_c, dap_c, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 21. PHƯƠNG TRÌNH, BẤT PHƯƠNG TRÌNH MŨ VÀ LÔGARIT
# =====================================================================

def L11_C6_B21_TH098_MC_A_01(socau, dang=1):
    r"""Giải phương trình mũ dạng đơn giản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5])
        m = random.choice([1, 2, 3])
        x0 = random.randint(-3, 4)
        n = random.randint(-4, 4)
        k = m * x0 + n
        if k < 0 or k > 7:
            continue
        if (a, m, n, x0) not in gt:
            gt.append((a, m, n, x0))

    cauTN = ""
    for a, m, n, x0 in gt:
        k = m * x0 + n
        ve_trai = _mu(a, _nhi_thuc6(m, n))
        dung = "$x = %d$" % x0
        nhieu = _ba_nhieu6(
            dung,
            ["$x = %d$" % (-x0), "$x = %d$" % k,
             "$x = %d$" % (a ** k)],
            buoc=lambda t: "$x = %d$" % (x0 + t))
        debai = (r"Giải phương trình $%s = %d$." % (ve_trai, a ** k))
        giai = (r"Đưa hai vế về cùng cơ số $%d$: $%d = %s$."
                % (a, a ** k, _mu(a, "%d" % k)) +
                "\\\\\n"
                r"$%s = %s \Leftrightarrow %s = %d$ (hai luỹ thừa cùng cơ "
                r"số bằng nhau thì số mũ bằng nhau)."
                % (ve_trai, _mu(a, "%d" % k), _nhi_thuc6(m, n), k) +
                "\\\\\n"
                r"$%s = %d \Leftrightarrow x = %d$."
                % (_nhi_thuc6(m, n), k, x0))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B21_TH098_SA_A_01(socau):
    r"""Nghiệm của phương trình lôgarit - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5])
        k = random.randint(2, 4)
        m = random.choice([1, 2])
        n = random.randint(-5, 5)
        if (a ** k - n) % m != 0:
            continue
        x0 = (a ** k - n) // m
        if m * x0 + n <= 0:
            continue
        if (a, k, m, n) not in gt:
            gt.append((a, k, m, n))

    cau = ""
    for a, k, m, n in gt:
        x0 = (a ** k - n) // m
        bt = _nhi_thuc6(m, n)
        debai = (r"Giải phương trình $%s = %d$ (viết nghiệm $x$)."
                 % (_log(a, r"\left(%s\right)" % bt), k))
        giai = (r"Điều kiện: $%s > 0$." % bt +
                "\\\\\n"
                r"Theo định nghĩa lôgarit: "
                r"$%s = %d \Leftrightarrow %s = %s = %d$."
                % (_log(a, r"\left(%s\right)" % bt), k, bt,
                   _mu(a, "%d" % k), a ** k) +
                "\\\\\n"
                r"$%s = %d \Leftrightarrow x = %d$." % (bt, a ** k, x0) +
                "\\\\\n"
                r"Thử lại: $%s = %d > 0$ nên $x = %d$ thoả mãn điều kiện."
                % (bt, a ** k, x0))
        nhieu = _ba_nhieu6(str(x0), [str(k), str(a ** k), str(-x0)],
                           buoc=lambda t: str(x0 + t))
        cau += MC_SA_answer_const(debai, str(x0), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B21_TH098_TL_A_01(socau, dong=1):
    r"""Tự luận: giải phương trình và bất phương trình mũ, lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5])
        x1 = random.randint(-2, 4)
        n1 = random.randint(-3, 3)
        k1 = x1 + n1
        k2 = random.randint(2, 3)
        n2 = random.randint(-4, 4)
        k3 = random.randint(1, 4)
        n3 = random.randint(-3, 3)
        if k1 < 0 or k1 > 6:
            continue
        if a ** k2 - n2 <= 0:
            continue
        v = (a, x1, n1, k2, n2, k3, n3)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, x1, n1, k2, n2, k3, n3 in gt:
        k1 = x1 + n1
        x2 = a ** k2 - n2
        # BPT mu: a^(x + n3) > a^k3  <=>  x + n3 > k3  <=>  x > k3 - n3
        x3 = k3 - n3
        debai = r"Giải các phương trình và bất phương trình sau."

        pt1 = r"%s = %d" % (_mu(a, _nhi_thuc6(1, n1)), a ** k1)
        hoi_a = r"$%s$" % pt1
        giai_a = (r"Đưa về cùng cơ số: $%d = %s$."
                  % (a ** k1, _mu(a, "%d" % k1)) +
                  "\\\\\n"
                  r"$%s \Leftrightarrow %s = %d \Leftrightarrow x = %d$."
                  % (pt1, _nhi_thuc6(1, n1), k1, x1))

        pt2 = r"%s = %d" % (_log(a, r"\left(%s\right)" % _nhi_thuc6(1, n2)),
                            k2)
        hoi_b = r"$%s$" % pt2
        giai_b = (r"Điều kiện: $%s > 0$." % _nhi_thuc6(1, n2) +
                  "\\\\\n"
                  r"$%s \Leftrightarrow %s = %s = %d$."
                  % (pt2, _nhi_thuc6(1, n2), _mu(a, "%d" % k2), a ** k2) +
                  "\\\\\n"
                  r"$\Leftrightarrow x = %d$ (thoả mãn điều kiện)." % x2)

        bpt = r"%s > %d" % (_mu(a, _nhi_thuc6(1, n3)), a ** k3)
        hoi_c = r"$%s$" % bpt
        giai_c = (r"Đưa về cùng cơ số: $%d = %s$."
                  % (a ** k3, _mu(a, "%d" % k3)) +
                  "\\\\\n"
                  r"Vì cơ số $%d > 1$ nên hàm số mũ ĐỒNG BIẾN, bất phương "
                  r"trình giữ nguyên chiều:" % a +
                  "\\\\\n"
                  r"$%s \Leftrightarrow %s > %d \Leftrightarrow x > %d$."
                  % (bpt, _nhi_thuc6(1, n3), k3, x3) +
                  "\\\\\n"
                  r"Tập nghiệm: $S = \left(%d;\ +\infty\right)$." % x3)

        ds_abcd = [(hoi_a, r"x = %d" % x1, giai_a),
                   (hoi_b, r"x = %d" % x2, giai_b),
                   (hoi_c, r"S = \left(%d;\ +\infty\right)" % x3, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def _bo_lai_nguyen():
    r"""$(P, Q, r, n)$ với $P\left(1 + r\right)^{n} = Q$ và $n$ NGUYÊN.

    Dùng $r = \dfrac{1}{4}$ (kèm $P = c\cdot 4^{n}$, $Q = c\cdot 5^{n}$)
    hoặc $r = \dfrac{1}{2}$ (kèm $P = c\cdot 2^{n}$, $Q = c\cdot 3^{n}$)
    nên số tiền hai đầu đều NGUYÊN và số năm cũng NGUYÊN.
    """
    if random.random() < 0.5:
        r, u, v = Fraction(1, 4), 4, 5
        n = random.choice([2, 3, 4])
        c = random.choice([1, 2, 5])
    else:
        r, u, v = Fraction(1, 2), 2, 3
        n = random.choice([2, 3, 4])
        c = random.choice([5, 10, 20])
    return c * u ** n, c * v ** n, r, n


def L11_C6_B21_VD099_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với phương trình mũ - tăng trưởng vi khuẩn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        N0 = random.choice([200, 500, 1000, 2000, 5000])
        k = random.randint(3, 7)
        if (N0, k) not in gt:
            gt.append((N0, k))

    cauTN = ""
    for N0, k in gt:
        N = N0 * 2 ** k
        dung = "$%d$ giờ" % k
        nhieu = _ba_nhieu6(dung,
                           ["$%d$ giờ" % (2 ** k), "$%d$ giờ" % (k * 2),
                            "$%d$ giờ" % (N // N0 - k)],
                           buoc=lambda t: "$%d$ giờ" % (k + t))
        debai = (r"Số lượng vi khuẩn trong một mẫu thí nghiệm được cho bởi "
                 r"$N\left(t\right) = %d\cdot 2^{\,t}$ với $t$ tính bằng "
                 r"giờ. Sau bao lâu thì số vi khuẩn đạt $%d$ con?"
                 % (N0, N))
        giai = (r"Giải phương trình $%d\cdot 2^{\,t} = %d$." % (N0, N) +
                "\\\\\n"
                r"$2^{\,t} = \dfrac{%d}{%d} = %d$." % (N, N0, 2 ** k) +
                "\\\\\n"
                r"Đưa về cùng cơ số $2$: $%d = 2^{%d}$." % (2 ** k, k) +
                "\\\\\n"
                r"$2^{\,t} = 2^{%d} \Leftrightarrow t = %d$ (giờ)." % (k, k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C6_B21_VD099_SA_A_01(socau):
    r"""Số năm gửi tiết kiệm - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_lai_nguyen()
        if v not in gt:
            gt.append(v)

    cau = ""
    for P, Q, r, n in gt:
        mot = 1 + r
        debai = (r"Một người gửi tiết kiệm $%d$ triệu đồng theo thể thức "
                 r"lãi kép với lãi suất $%s$ một năm. Hỏi sau bao nhiêu "
                 r"năm người đó nhận được $%d$ triệu đồng?"
                 % (P, _pt_lai(r), Q))
        giai = (r"Số tiền sau $n$ năm: $A = %d\left(1 + %s\right)^{n} = "
                r"%d\cdot\left(\dfrac{%d}{%d}\right)^{n}$."
                % (P, _xx(float(r), 4), P, mot.numerator, mot.denominator) +
                "\\\\\n"
                r"Giải $%d\cdot\left(\dfrac{%d}{%d}\right)^{n} = %d$."
                % (P, mot.numerator, mot.denominator, Q) +
                "\\\\\n"
                r"$\left(\dfrac{%d}{%d}\right)^{n} = \dfrac{%d}{%d} = "
                r"\left(\dfrac{%d}{%d}\right)^{%d}$."
                % (mot.numerator, mot.denominator, Q, P,
                   mot.numerator, mot.denominator, n) +
                "\\\\\n"
                r"Hai luỹ thừa cùng cơ số bằng nhau nên $n = %d$ (năm)." % n)
        nhieu = _ba_nhieu6(str(n), [str(n + 1), str(Q // P if P else 2),
                                    str(2 * n)],
                           buoc=lambda t: str(n + t + 1))
        cau += MC_SA_answer_const(debai, str(n), nhieu, giai, 0, 0, 2)
    return cau


def L11_C6_B21_VD099_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về phương trình mũ, lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_lai_nguyen()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for P, Q, r, n in gt:
        mot = 1 + r
        A1 = P * mot
        debai = (r"Một người gửi tiết kiệm $%d$ triệu đồng theo thể thức "
                 r"lãi kép với lãi suất $%s$ một năm (lãi mỗi năm được "
                 r"nhập vào vốn)." % (P, _pt_lai(r)))

        hoi_a = r"Tính số tiền nhận được sau $1$ năm."
        giai_a = (r"$A_1 = %d\left(1 + %s\right) = %d\cdot\dfrac{%d}{%d} "
                  r"= %s$ (triệu đồng)."
                  % (P, _xx(float(r), 4), P, mot.numerator, mot.denominator,
                     _xx(float(A1), 2)))

        hoi_b = (r"Lập phương trình để tìm số năm $n$ cần gửi sao cho "
                 r"nhận được $%d$ triệu đồng." % Q)
        giai_b = (r"Sau $n$ năm số tiền là "
                  r"$A_n = %d\left(1 + %s\right)^{n}$."
                  % (P, _xx(float(r), 4)) +
                  "\\\\\n"
                  r"Phương trình cần giải: "
                  r"$%d\cdot\left(\dfrac{%d}{%d}\right)^{n} = %d$."
                  % (P, mot.numerator, mot.denominator, Q))

        hoi_c = r"Giải phương trình ở câu b để tìm $n$."
        giai_c = (r"$\left(\dfrac{%d}{%d}\right)^{n} = \dfrac{%d}{%d}$."
                  % (mot.numerator, mot.denominator, Q, P) +
                  "\\\\\n"
                  r"Nhận thấy $\dfrac{%d}{%d} = "
                  r"\left(\dfrac{%d}{%d}\right)^{%d}$."
                  % (Q, P, mot.numerator, mot.denominator, n) +
                  "\\\\\n"
                  r"Hai luỹ thừa cùng cơ số bằng nhau nên $n = %d$." % n +
                  "\\\\\n"
                  r"Cách khác: lấy lôgarit hai vế, "
                  r"$n = \log_{\frac{%d}{%d}}\dfrac{%d}{%d} = %d$ (năm)."
                  % (mot.numerator, mot.denominator, Q, P, n))

        ds_abcd = [(hoi_a, r"A_1 = %s \text{ triệu đồng}"
                    % _xx(float(A1), 2), giai_a),
                   (hoi_b, r"%d\cdot\left(\dfrac{%d}{%d}\right)^{n} = %d"
                    % (P, mot.numerator, mot.denominator, Q), giai_b),
                   (hoi_c, r"n = %d \text{ năm}" % n, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 6
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C6_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - luỹ thừa với số mũ thực và lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A, n, m, b, kq = _bo_can_dep()
        a = random.choice([2, 3, 5])
        p = random.randint(2, 4)
        q = random.randint(1, 3)
        v = (A, n, m, b, kq, a, p, q)
        if v not in gt:
            gt.append(v)

    cauTF = ""
    for A, n, m, b, kq, a, p, q in gt:
        x, y = a ** p, a ** q
        debai = (r"Cho $a > 0$, $a \neq 1$ và các số thực dương $x$, $y$.")

        ds_abcd = (
            # a) NB - nhắc lại định nghĩa
            [
                (r"{\True $\log_a 1 = 0$ với mọi $a > 0$, $a \neq 1$}",
                 r"Đúng. Vì $a^{0} = 1$ nên theo định nghĩa lôgarit "
                 r"$\log_a 1 = 0$."),
                (r"{$\log_a 1 = 1$ với mọi $a > 0$, $a \neq 1$}",
                 r"Sai. $\log_a a = 1$ mới đúng, còn $\log_a 1 = 0$."),
            ],
            # b) TH - một lần dùng tính chất
            [
                (r"{\True $%s = %d$}" % (_log(a, "%d" % x), p),
                 r"Đúng. Vì $%d = %s$ nên $%s = %d$."
                 % (x, _mu(a, "%d" % p), _log(a, "%d" % x), p)),
                (r"{$%s = %d$}" % (_log(a, "%d" % x), x),
                 r"Sai. Lôgarit trả về SỐ MŨ chứ không phải đối số: "
                 r"$%s = %d$." % (_log(a, "%d" % x), p)),
            ],
            # c) VD - phải đưa cơ số về luỹ thừa đúng rồi mới tính
            [
                (r"{\True $%s = %d$}" % (_mu_ps(A, m, n), kq),
                 r"Đúng. $%d = %s$ nên $%s = %s = %s = %d$."
                 % (A, _mu(b, "%d" % n), _mu_ps(A, m, n),
                    r"\left(%s\right)^{\frac{%d}{%d}}"
                    % (_mu(b, "%d" % n), m, n), _mu(b, "%d" % m), kq)),
                (r"{$%s = %d$}" % (_mu_ps(A, m, n), A * m),
                 r"Sai. Số mũ hữu tỉ KHÔNG phải phép nhân: phải viết "
                 r"$%d = %s$ rồi rút gọn, kết quả là $%d$."
                 % (A, _mu(b, "%d" % n), kq)),
            ],
            # d) VDC - phải tự ghép hai tính chất lôgarit
            [
                (r"{\True $%s + %s = %d$}"
                 % (_log(a, "%d" % x), _log(a, "%d" % y), p + q),
                 r"Đúng. Tổng hai lôgarit cùng cơ số bằng lôgarit của "
                 r"tích: $%s + %s = %s$."
                 % (_log(a, "%d" % x), _log(a, "%d" % y),
                    _log(a, "%d" % (x * y))) + "\\\\\n" +
                 r"Mà $%d = %s$ nên tổng bằng $%d$."
                 % (x * y, _mu(a, "%d" % (p + q)), p + q)),
                (r"{$%s\cdot %s = %d$}"
                 % (_log(a, "%d" % x), _log(a, "%d" % y), p + q),
                 r"Sai. TÍCH hai lôgarit không có công thức rút gọn như "
                 r"vậy; ở đây $%s\cdot %s = %d\cdot %d = %d$, khác $%d$."
                 % (_log(a, "%d" % x), _log(a, "%d" % y), p, q, p * q,
                    p + q)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L11_C6_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - hàm số mũ, hàm số lôgarit và phương trình, bất phương
    trình mũ, lôgarit.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 5])
        k = random.randint(2, 4)
        n = random.randint(-3, 3)
        x0 = k - n
        v = (a, k, n, x0)
        if v not in gt:
            gt.append(v)

    cauTF = ""
    for a, k, n, x0 in gt:
        bt = _nhi_thuc6(1, n)
        debai = (r"Cho hàm số $y = %s$ và phương trình $%s = %d$."
                 % (_mu(a, "x"), _mu(a, bt), a ** k))

        ds_abcd = (
            # a) NB - đọc thẳng từ định nghĩa
            [
                (r"{\True Hàm số $y = %s$ có tập xác định $\mathbb{R}$}"
                 % _mu(a, "x"),
                 r"Đúng. Hàm số mũ $y = a^{x}$ xác định với mọi số thực "
                 r"$x$."),
                (r"{Hàm số $y = %s$ có tập xác định "
                 r"$\left(0;\ +\infty\right)$}" % _mu(a, "x"),
                 r"Sai. $\left(0;\ +\infty\right)$ là TẬP GIÁ TRỊ của hàm "
                 r"số mũ, còn tập xác định là $\mathbb{R}$."),
            ],
            # b) TH - dùng tính đơn điệu
            [
                (r"{\True Hàm số $y = %s$ đồng biến trên $\mathbb{R}$}"
                 % _mu(a, "x"),
                 r"Đúng. Cơ số $%d > 1$ nên hàm số mũ đồng biến trên "
                 r"$\mathbb{R}$." % a),
                (r"{Hàm số $y = %s$ nghịch biến trên $\mathbb{R}$}"
                 % _mu(a, "x"),
                 r"Sai. Hàm số mũ chỉ nghịch biến khi $0 < a < 1$; ở đây "
                 r"$a = %d > 1$ nên hàm số đồng biến." % a),
            ],
            # c) VD - giải phương trình mũ
            [
                (r"{\True Phương trình đã cho có nghiệm $x = %d$}" % x0,
                 r"Đúng. Đưa về cùng cơ số: $%d = %s$."
                 % (a ** k, _mu(a, "%d" % k)) + "\\\\\n" +
                 r"$%s = %s \Leftrightarrow %s = %d \Leftrightarrow "
                 r"x = %d$."
                 % (_mu(a, bt), _mu(a, "%d" % k), bt, k, x0)),
                (r"{Phương trình đã cho có nghiệm $x = %d$}" % (a ** k),
                 r"Sai. Không được lấy thẳng vế phải làm nghiệm; phải đưa "
                 r"về cùng cơ số rồi cho hai số mũ bằng nhau, được "
                 r"$x = %d$." % x0),
            ],
            # d) VDC - phải tự xét chiều bất phương trình
            [
                (r"{\True Bất phương trình $%s < %d$ có tập nghiệm "
                 r"$\left(-\infty;\ %d\right)$}"
                 % (_mu(a, bt), a ** k, x0),
                 r"Đúng. Cơ số $%d > 1$ nên hàm số mũ đồng biến, bất "
                 r"phương trình GIỮ NGUYÊN chiều." % a + "\\\\\n" +
                 r"$%s < %s \Leftrightarrow %s < %d \Leftrightarrow "
                 r"x < %d$."
                 % (_mu(a, bt), _mu(a, "%d" % k), bt, k, x0) + "\\\\\n" +
                 r"Tập nghiệm $\left(-\infty;\ %d\right)$." % x0),
                (r"{Bất phương trình $%s < %d$ có tập nghiệm "
                 r"$\left(%d;\ +\infty\right)$}"
                 % (_mu(a, bt), a ** k, x0),
                 r"Sai. Chiều bất phương trình chỉ ĐỔI khi cơ số nằm giữa "
                 r"$0$ và $1$. Ở đây $a = %d > 1$ nên giữ nguyên chiều, "
                 r"tập nghiệm là $\left(-\infty;\ %d\right)$." % (a, x0)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
