# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 5. Giới hạn. Hàm số liên tục
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Kiến thức dùng trong tệp:

  * $\lim\limits_{n \to +\infty}\dfrac{1}{n^{k}} = 0$ với $k > 0$;
    $\lim q^{\,n} = 0$ khi $\left|q\right| < 1$.
  * Giới hạn của dãy phân thức: chia cả tử và mẫu cho luỹ thừa cao nhất.
  * Cấp số nhân lùi vô hạn ($\left|q\right| < 1$):
    $S = \dfrac{u_1}{1 - q}$.
  * Giới hạn hàm số dạng $\dfrac{0}{0}$: phân tích thành nhân tử rồi rút
    gọn.
  * Hàm số liên tục tại $x_0$ khi $\lim\limits_{x \to x_0} f(x) =
    f\left(x_0\right)$.

Số liệu chọn để ĐÁP SỐ ĐẸP: mọi giới hạn đều là số nguyên hoặc phân số
tối giản viết được chính xác; cấp số nhân lùi vô hạn chọn $q$ dạng
$\dfrac{1}{k}$ để tổng ra phân số đẹp.

Bài học lớp 10 đã áp dụng: chữ tiếng Việt không nằm trần trong $...$;
không dùng **đậm**; mọi chuỗi có dấu gạch chéo đều là r"..."; mọi danh
sách phương án nhiễu đều qua _ba_nhieu5.
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


def _ba_nhieu5(dapso, ung_vien, buoc=None):
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

def _chon_chi_muc(n, socau):
    r"""Chọn socau chỉ mục trong 0..n-1, KHÔNG trùng nhau chừng nào còn
    đủ; hết mẫu thì quay vòng (tránh vòng lặp vô hạn khi socau > n)."""
    ds = []
    while len(ds) < socau:
        thieu = socau - len(ds)
        ds += random.sample(range(n), min(n, thieu))
    return ds


def _dau(x):
    return ("+ %d" % abs(x)) if x >= 0 else ("- %d" % abs(x))


def _ps(p, q=1):
    r"""Viết phân số tối giản dạng LaTeX (rút gọn sẵn)."""
    f = Fraction(p, q)
    if f.denominator == 1:
        return "%d" % f.numerator
    if f < 0:
        return r"-\dfrac{%d}{%d}" % (-f.numerator, f.denominator)
    return r"\dfrac{%d}{%d}" % (f.numerator, f.denominator)


def _hang_chia(x, bien="n"):
    r"""Viết hạng tử $\pm\dfrac{|x|}{n}$ đúng dấu."""
    return r"%s \dfrac{%d}{%s}" % ("+" if x >= 0 else "-", abs(x), bien)


def _nhi_thuc(a, b, bien="n"):
    """a*bien + b, viết gọn."""
    he = "" if a == 1 else ("-" if a == -1 else "%d" % a)
    if b == 0:
        return "%s%s" % (he, bien)
    return "%s%s %s" % (he, bien, _dau(b))


def _tam_thuc(a, b, c, bien="x"):
    phan = []
    for he, mu in ((a, 2), (b, 1), (c, 0)):
        if he == 0:
            continue
        if mu == 0:
            cum = "%d" % abs(he)
        else:
            h = "" if abs(he) == 1 else "%d" % abs(he)
            cum = h + (bien if mu == 1 else r"%s^{2}" % bien)
        if not phan:
            phan.append(("-" if he < 0 else "") + cum)
        else:
            phan.append(("+ " if he > 0 else "- ") + cum)
    return " ".join(phan) if phan else "0"


# =====================================================================
# BÀI 15. GIỚI HẠN CỦA DÃY SỐ
# =====================================================================

def L11_C5_B15_NB072_MC_A_01(socau, dang=1):
    r"""Nhận biết giới hạn của dãy số cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"\lim\dfrac{1}{n}", "0"),
        (r"\lim\dfrac{1}{n^{2}}", "0"),
        (r"\lim\dfrac{1}{\sqrt{n}}", "0"),
        (r"\lim\left(\dfrac{1}{2}\right)^{n}", "0"),
        (r"\lim c \text{ (với } c \text{ là hằng số)}", "c"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        bieu_thuc, kq = MAU[i]
        dung = r"$%s$" % kq
        nhieu = _ba_nhieu5(dung, [r"$1$", r"$+\infty$", r"$-\infty$",
                                  r"$%s$" % ("c" if kq == "0" else "0")],
                           buoc=lambda t: r"$%d$" % (t + 1))
        debai = r"Tính $%s$." % bieu_thuc
        giai = (r"Các giới hạn cơ bản đã học:"
                "\\\\\n"
                r"$\lim\dfrac{1}{n^{k}} = 0$ với mọi $k > 0$; "
                r"$\lim q^{\,n} = 0$ khi $\left|q\right| < 1$; và giới hạn "
                r"của dãy hằng bằng chính hằng số đó."
                "\\\\\n"
                r"Vậy $%s = %s$." % (bieu_thuc, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B15_TH073_MC_A_01(socau, dang=1):
    r"""Giới hạn của dãy $q^n$ và tổng cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(2, 9)
        k = random.randint(2, 5)
        v = (a, k)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, k in gt:
        # lim (a + 1/n^k) = a
        dung = r"$%d$" % a
        nhieu = _ba_nhieu5(dung, [r"$0$", r"$+\infty$", r"$%d$" % (a + 1)],
                           buoc=lambda t: r"$%d$" % (a + t + 1))
        debai = (r"Tính $\lim\left(%d + \dfrac{1}{n^{%d}}\right)$."
                 % (a, k))
        giai = (r"$\lim\dfrac{1}{n^{%d}} = 0$." % k +
                "\\\\\n"
                r"Áp dụng phép toán về giới hạn của tổng:"
                "\\\\\n"
                r"$\lim\left(%d + \dfrac{1}{n^{%d}}\right) = %d + 0 = %d$."
                % (a, k, a, a))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B15_TH073_SA_A_01(socau):
    r"""Giới hạn của dãy số cơ bản - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(2, 9)
        b = random.randint(1, 9)
        k = random.randint(1, 3)
        v = (a, b, k)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, k in gt:
        debai = (r"Tính $\lim\left(%d - \dfrac{%d}{n^{%d}}\right)$."
                 % (a, b, k))
        giai = (r"$\lim\dfrac{%d}{n^{%d}} = 0$ nên giới hạn cần tìm bằng "
                r"$%d - 0 = %d$." % (b, k, a, a))
        nhieu = _ba_nhieu5(str(a), [str(a - b), "0", str(a + b)],
                           buoc=lambda t: str(a + t + 1))
        cau += MC_SA_answer_const(debai, str(a), nhieu, giai, 0, 0, 2)
    return cau


def _bo_phan_thuc():
    """(a, b, c, d) cho dãy (an+b)/(cn+d), c khác 0."""
    while True:
        a = random.randint(1, 9)
        b = random.randint(-9, 9)
        c = random.randint(1, 9)
        d = random.randint(-9, 9)
        if c and (a, c) != (0, 0):
            return a, b, c, d


def L11_C5_B15_TH074_MC_A_01(socau, dang=1):
    r"""Giới hạn của dãy phân thức bậc nhất trên bậc nhất.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_phan_thuc()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, d in gt:
        dung = r"$%s$" % _ps(a, c)
        nhieu = _ba_nhieu5(
            dung,
            [r"$%s$" % _ps(b, d) if d else r"$0$",
             r"$%s$" % _ps(c, a), r"$0$", r"$+\infty$"],
            buoc=lambda t: r"$%s$" % _ps(a + t, c))
        debai = (r"Tính $\lim\dfrac{%s}{%s}$."
                 % (_nhi_thuc(a, b), _nhi_thuc(c, d)))
        giai = (r"Chia cả tử và mẫu cho $n$ (luỹ thừa bậc cao nhất):"
                "\\\\\n"
                r"$\dfrac{%s}{%s} = "
                r"\dfrac{%d %s\dfrac{%d}{n}}{%d %s\dfrac{%d}{n}}$."
                % (_nhi_thuc(a, b), _nhi_thuc(c, d),
                   a, "+" if b >= 0 else "-", abs(b),
                   c, "+" if d >= 0 else "-", abs(d)) +
                "\\\\\n"
                r"Vì $\lim\dfrac{1}{n} = 0$ nên giới hạn bằng "
                r"$\dfrac{%d}{%d}%s$."
                % (a, c, ("" if _ps(a, c) == r"\dfrac{%d}{%d}" % (a, c)
                          else " = %s" % _ps(a, c))) +
                "\\\\\n"
                r"Chú ý giới hạn chỉ phụ thuộc HỆ SỐ BẬC CAO NHẤT của tử "
                r"và mẫu.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B15_TH074_SA_A_01(socau):
    r"""Giới hạn dãy phân thức - trả lời ngắn (đáp số nguyên).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        c = random.randint(1, 6)
        k = random.randint(2, 9)
        a = c * k                      # de a/c NGUYEN
        b = random.randint(-9, 9)
        d = random.randint(-9, 9)
        v = (a, b, c, d)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, c, d in gt:
        kq = a // c
        debai = (r"Tính $\lim\dfrac{%s}{%s}$."
                 % (_nhi_thuc(a, b), _nhi_thuc(c, d)))
        giai = (r"Chia cả tử và mẫu cho $n$, dùng $\lim\dfrac{1}{n} = 0$:"
                "\\\\\n"
                r"giới hạn bằng $\dfrac{%d}{%d} = %d$." % (a, c, kq))
        nhieu = _ba_nhieu5(str(kq), [str(a), str(c), "0"],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def _bo_lui_vo_han():
    r"""$u_1$ nguyên, $q = \pm\dfrac{1}{k}$ để tổng ra phân số đẹp."""
    u1 = random.randint(1, 12)
    k = random.choice([2, 3, 4, 5])
    dau = random.choice([1, -1])
    return u1, Fraction(dau, k)


def L11_C5_B15_VD075_MC_A_01(socau, dang=1):
    r"""Tổng của một cấp số nhân lùi vô hạn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_lui_vo_han()
        if (u1, q) not in gt:
            gt.append((u1, q))

    cauTN = ""
    for u1, q in gt:
        S = Fraction(u1) / (1 - q)
        dung = r"$%s$" % _ps(S.numerator, S.denominator)
        sai1 = Fraction(u1) / (1 + q)
        nhieu = _ba_nhieu5(
            dung,
            [r"$%s$" % _ps(sai1.numerator, sai1.denominator),
             r"$%d$" % u1,
             r"$%s$" % _ps(q.numerator, q.denominator)],
            buoc=lambda t: r"$%s$" % _ps(S.numerator + t * S.denominator,
                                         S.denominator))
        debai = (r"Tính tổng của cấp số nhân lùi vô hạn có số hạng đầu "
                 r"$u_1 = %d$ và công bội $q = %s$."
                 % (u1, _ps(q.numerator, q.denominator)))
        giai = (r"Vì $\left|q\right| = %s < 1$ nên đây là cấp số nhân lùi "
                r"vô hạn, tổng của nó tồn tại."
                % _ps(abs(q.numerator), q.denominator) +
                "\\\\\n"
                r"$S = \dfrac{u_1}{1 - q} = \dfrac{%d}{1 - \left(%s\right)} "
                r"= \dfrac{%d}{%s} = %s$."
                % (u1, _ps(q.numerator, q.denominator), u1,
                   _ps((1 - q).numerator, (1 - q).denominator),
                   _ps(S.numerator, S.denominator)) +
                "\\\\\n"
                r"Chú ý mẫu là $1 - q$ chứ không phải $1 + q$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B15_VD075_SA_A_01(socau):
    r"""Tổng cấp số nhân lùi vô hạn - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([2, 3, 4, 5])
        m = random.randint(1, 9)
        u1 = m * (k - 1)               # S = u1/(1 - 1/k) = m*k  NGUYEN
        v = (u1, k, m)
        if v not in gt:
            gt.append(v)

    cau = ""
    for u1, k, m in gt:
        S = m * k
        debai = (r"Tính tổng của cấp số nhân lùi vô hạn có số hạng đầu "
                 r"$u_1 = %d$ và công bội $q = \dfrac{1}{%d}$." % (u1, k))
        giai = (r"$S = \dfrac{u_1}{1 - q} = \dfrac{%d}{1 - \dfrac{1}{%d}} "
                r"= \dfrac{%d}{\dfrac{%d}{%d}} = %d$."
                % (u1, k, u1, k - 1, k, S))
        nhieu = _ba_nhieu5(str(S), [str(u1), str(k), str(S + 1)],
                           buoc=lambda t: str(S + t + 1))
        cau += MC_SA_answer_const(debai, str(S), nhieu, giai, 0, 0, 2)
    return cau


def L11_C5_B15_VD075_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về cấp số nhân lùi vô hạn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([2, 3, 4])
        m = random.randint(2, 9)
        h = m * (k - 1)                # quang duong roi dau, S nguyen
        v = (h, k, m)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for h, k, m in gt:
        S = m * k
        u3 = Fraction(h, k * k)
        debai = (r"Một quả bóng được thả rơi từ độ cao $%d$ mét. Mỗi lần "
                 r"chạm đất, quả bóng lại nảy lên một độ cao bằng "
                 r"$\dfrac{1}{%d}$ độ cao của lần rơi ngay trước đó."
                 % (h, k))

        hoi_a = (r"Gọi $u_n$ là độ cao của lần rơi thứ $n$. Chứng tỏ "
                 r"$\left(u_n\right)$ là cấp số nhân lùi vô hạn và chỉ ra "
                 r"$u_1$, $q$.")
        giai_a = (r"$u_1 = %d$ và mỗi lần sau bằng $\dfrac{1}{%d}$ lần "
                  r"trước nên $q = \dfrac{1}{%d}$." % (h, k, k) +
                  "\\\\\n"
                  r"Vì $\left|q\right| = \dfrac{1}{%d} < 1$ nên đây là cấp "
                  r"số nhân lùi vô hạn." % k)

        hoi_b = r"Tính độ cao của lần rơi thứ ba."
        giai_b = (r"$u_3 = u_1q^{2} = %d\cdot\dfrac{1}{%d} = %s$ (mét)."
                  % (h, k * k, _ps(u3.numerator, u3.denominator)))

        hoi_c = (r"Tính tổng các độ cao rơi xuống của quả bóng (coi quá "
                 r"trình kéo dài vô hạn).")
        giai_c = (r"$S = \dfrac{u_1}{1 - q} = \dfrac{%d}{1 - \dfrac{1}{%d}} "
                  r"= \dfrac{%d}{\dfrac{%d}{%d}} = %d$ (mét)."
                  % (h, k, h, k - 1, k, S))

        ds_abcd = [(hoi_a, r"u_1 = %d,\ q = \dfrac{1}{%d}" % (h, k), giai_a),
                   (hoi_b, r"u_3 = %s" % _ps(u3.numerator, u3.denominator),
                    giai_b),
                   (hoi_c, r"S = %d\ \text{m}" % S, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 16. GIỚI HẠN CỦA HÀM SỐ
# =====================================================================

def L11_C5_B16_NB076_MC_A_01(socau, dang=1):
    r"""Nhận biết giới hạn hữu hạn của hàm số tại một điểm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        b = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        c = random.randint(-6, 6)
        if (a, b, c) not in gt and b * a + c != 0:
            gt.append((a, b, c))

    cauTN = ""
    for a, b, c in gt:
        kq = b * a + c
        dung = "$%d$" % kq
        nhieu = _ba_nhieu5(dung,
                           ["$%d$" % (b + c), "$%d$" % a, "$%d$" % (b * a - c)],
                           buoc=lambda t: "$%d$" % (kq + t))
        debai = (r"Tính $\lim\limits_{x \to %d}\left(%s\right)$."
                 % (a, _nhi_thuc(b, c, "x")))
        giai = (r"Hàm số $f(x) = %s$ là hàm đa thức nên liên tục trên "
                r"$\mathbb{R}$." % _nhi_thuc(b, c, "x") +
                "\\\\\n"
                r"Do đó giới hạn bằng giá trị của hàm số tại $x = %d$:" % a +
                "\\\\\n"
                r"$\lim\limits_{x \to %d}\left(%s\right) = %d\cdot"
                r"%s %s = %d$."
                % (a, _nhi_thuc(b, c, "x"), b,
                   ("%d" % a) if a >= 0 else (r"\left(%d\right)" % a),
                   _dau(c), kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B16_NB077_MC_A_01(socau, dang=1):
    r"""Nhận biết giới hạn hữu hạn của hàm số tại vô cực.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        c = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        k = random.choice([1, 2, 3, 4, 5, 6])
        mu = random.choice([1, 2])
        if (c, k, mu) not in gt:
            gt.append((c, k, mu))

    cauTN = ""
    for c, k, mu in gt:
        ham = (r"%d + \dfrac{%d}{x}" % (c, k) if mu == 1
               else r"%d + \dfrac{%d}{x^{2}}" % (c, k))
        dung = "$%d$" % c
        nhieu = _ba_nhieu5(dung,
                           ["$%d$" % (c + k), "$%d$" % k, "$0$"],
                           buoc=lambda t: "$%d$" % (c - t))
        debai = (r"Tính $\lim\limits_{x \to +\infty}\left(%s\right)$." % ham)
        giai = (r"Ta có $\lim\limits_{x \to +\infty}\dfrac{%d}{%s} = 0$."
                % (k, "x" if mu == 1 else r"x^{2}") +
                "\\\\\n"
                r"Vậy $\lim\limits_{x \to +\infty}\left(%s\right) = %d + 0 "
                r"= %d$." % (ham, c, c))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B16_NB078_MC_A_01(socau, dang=1):
    r"""Nhận biết giới hạn vô cực một phía của hàm số.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        k = random.choice([1, 2, 3, 4, 5])
        ben = random.choice(["+", "-"])
        if (a, k, ben) not in gt:
            gt.append((a, k, ben))

    cauTN = ""
    for a, k, ben in gt:
        mau = _nhi_thuc(1, -a, "x")
        dung = r"$+\infty$" if ben == "+" else r"$-\infty$"
        nhieu = _ba_nhieu5(dung,
                           [r"$-\infty$" if ben == "+" else r"$+\infty$",
                            "$0$", "$%d$" % k],
                           buoc=lambda t: "$%d$" % t)
        debai = (r"Tính $\lim\limits_{x \to %d^{%s}}\dfrac{%d}{%s}$."
                 % (a, ben, k, mau))
        if ben == "+":
            mota = (r"Khi $x \to %d^{+}$ thì $%s \to 0$ và $%s > 0$."
                    % (a, mau, mau))
            ket = (r"Tử số $%d > 0$ không đổi, mẫu số dương và dần về $0$ "
                   r"nên thương dần tới $+\infty$." % k)
        else:
            mota = (r"Khi $x \to %d^{-}$ thì $%s \to 0$ và $%s < 0$."
                    % (a, mau, mau))
            ket = (r"Tử số $%d > 0$ không đổi, mẫu số âm và dần về $0$ "
                   r"nên thương dần tới $-\infty$." % k)
        giai = mota + "\\\\\n" + ket + "\\\\\n" + \
            (r"Vậy $\lim\limits_{x \to %d^{%s}}\dfrac{%d}{%s} = %s\infty$."
             % (a, ben, k, mau, "+" if ben == "+" else "-"))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B16_TH079_MC_A_01(socau, dang=1):
    r"""Giới hạn dạng $\dfrac{0}{0}$ - phân tích thành nhân tử.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        b = random.randint(-5, 5)
        if a != b and (a, b) not in gt:
            gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        kq = a - b
        tu = _tam_thuc(1, -(a + b), a * b, "x")
        mau = _nhi_thuc(1, -a, "x")
        dung = "$%d$" % kq
        nhieu = _ba_nhieu5(dung,
                           ["$%d$" % (a + b), "$%d$" % (b - a), "$0$"],
                           buoc=lambda t: "$%d$" % (kq + t))
        debai = (r"Tính $\lim\limits_{x \to %d}\dfrac{%s}{%s}$."
                 % (a, tu, mau))
        giai = (r"Thay $x = %d$ vào thì cả tử và mẫu đều bằng $0$, đây là "
                r"dạng vô định $\dfrac{0}{0}$." % a +
                "\\\\\n"
                r"Phân tích tử thức: $%s = \left(%s\right)\left(%s\right)$."
                % (tu, mau, _nhi_thuc(1, -b, "x")) +
                "\\\\\n"
                r"$\lim\limits_{x \to %d}\dfrac{\left(%s\right)"
                r"\left(%s\right)}{%s} = \lim\limits_{x \to %d}"
                r"\left(%s\right) = %d$."
                % (a, mau, _nhi_thuc(1, -b, "x"), mau, a,
                   _nhi_thuc(1, -b, "x"), kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B16_TH079_SA_A_01(socau):
    r"""Giới hạn của hàm số tại một điểm - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        if a not in gt:
            gt.append(a)

    cau = ""
    for a in gt:
        kq = 2 * a
        tu = _tam_thuc(1, 0, -a * a, "x")
        mau = _nhi_thuc(1, -a, "x")
        debai = (r"Tính $\lim\limits_{x \to %d}\dfrac{%s}{%s}$."
                 % (a, tu, mau))
        giai = (r"Đây là dạng vô định $\dfrac{0}{0}$." + "\\\\\n" +
                r"$%s = \left(%s\right)\left(%s\right)$."
                % (tu, mau, _nhi_thuc(1, a, "x")) +
                "\\\\\n"
                r"$\lim\limits_{x \to %d}\dfrac{%s}{%s} = "
                r"\lim\limits_{x \to %d}\left(%s\right) = %d$."
                % (a, tu, mau, a, _nhi_thuc(1, a, "x"), kq))
        nhieu = _ba_nhieu5(str(kq), [str(a), "0", str(a * a)],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C5_B16_VD080_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với giới hạn hàm số tại vô cực.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10])
        b = random.choice([2, 3, 4, 5])
        if (a, b) not in gt:
            gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        dung = r"$%d$ mg/l" % a
        nhieu = _ba_nhieu5(dung,
                           [r"$%d$ mg/l" % b, r"$0$ mg/l",
                            r"$%d$ mg/l" % (a + b)],
                           buoc=lambda t: r"$%d$ mg/l" % (a + t))
        debai = (r"Nồng độ của một loại muối trong dung dịch sau $t$ phút "
                 r"khuấy đều được cho bởi công thức "
                 r"$C(t) = \dfrac{%dt}{t + %d}$ (đơn vị: mg/l). "
                 r"Nếu quá trình khuấy kéo dài vô hạn thì nồng độ muối "
                 r"tiến tới giá trị nào?" % (a, b))
        giai = (r"Ta cần tính $\lim\limits_{t \to +\infty}C(t)$." +
                "\\\\\n"
                r"Chia cả tử và mẫu cho $t$:" +
                "\\\\\n"
                r"$C(t) = \dfrac{%dt}{t + %d} = \dfrac{%d}{1 + "
                r"\dfrac{%d}{t}}$." % (a, b, a, b) +
                "\\\\\n"
                r"Vì $\lim\limits_{t \to +\infty}\dfrac{%d}{t} = 0$ nên "
                r"$\lim\limits_{t \to +\infty}C(t) = \dfrac{%d}{1 + 0} "
                r"= %d$." % (b, a, a) +
                "\\\\\n"
                r"Vậy nồng độ muối tiến tới $%d$ mg/l." % a)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B16_VD080_SA_A_01(socau):
    r"""Vấn đề thực tiễn gắn với giới hạn hàm số - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đáp số NGUYÊN: giới hạn của $\dfrac{at}{t + b}$ khi $t \to +\infty$.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
        b = random.choice([2, 3, 4, 5, 6])
        if (a, b) not in gt:
            gt.append((a, b))

    cau = ""
    for a, b in gt:
        debai = (r"Số lượng vi khuẩn (đơn vị: nghìn con) trong một mẫu thí "
                 r"nghiệm sau $t$ giờ được cho bởi công thức "
                 r"$N\left(t\right) = \dfrac{%dt}{t + %d}$. Khi thời gian "
                 r"nuôi cấy kéo dài vô hạn thì số lượng vi khuẩn tiến tới "
                 r"giá trị nào (đơn vị: nghìn con)?" % (a, b))
        giai = (r"Ta cần tính $\lim\limits_{t \to +\infty}"
                r"N\left(t\right)$." +
                "\\\\\n"
                r"Chia cả tử và mẫu cho $t$:" +
                "\\\\\n"
                r"$N\left(t\right) = \dfrac{%d}{1 + \dfrac{%d}{t}}$."
                % (a, b) +
                "\\\\\n"
                r"Vì $\lim\limits_{t \to +\infty}\dfrac{%d}{t} = 0$ nên "
                r"$\lim\limits_{t \to +\infty}N\left(t\right) = "
                r"\dfrac{%d}{1 + 0} = %d$." % (b, a, a) +
                "\\\\\n"
                r"Vậy số lượng vi khuẩn tiến tới $%d$ nghìn con và không "
                r"vượt quá giá trị này." % a)
        nhieu = _ba_nhieu5(str(a), [str(b), "0", str(a + b)],
                           buoc=lambda t: str(a + t + 1))
        cau += MC_SA_answer_const(debai, str(a), nhieu, giai, 0, 0, 2)
    return cau


def L11_C5_B16_VD080_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn gắn với giới hạn hàm số.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
        b = random.choice([2, 3, 4, 5, 6])
        t0 = random.choice([1, 2, 3, 4, 5, 6])
        if (a, b, t0) not in gt:
            gt.append((a, b, t0))

    cauTN = ""
    for a, b, t0 in gt:
        N0 = Fraction(a * t0, t0 + b)
        debai = (r"Số lượng vi khuẩn (đơn vị: nghìn con) trong một mẫu thí "
                 r"nghiệm sau $t$ giờ được cho bởi công thức "
                 r"$N\left(t\right) = \dfrac{%dt}{t + %d}$ với $t \geq 0$."
                 % (a, b))

        hoi_a = r"Tính $N\left(0\right)$ và $N\left(%d\right)$." % t0
        giai_a = (r"$N\left(0\right) = \dfrac{%d\cdot 0}{0 + %d} = 0$."
                  % (a, b) + "\\\\\n" +
                  r"$N\left(%d\right) = \dfrac{%d\cdot %d}{%d + %d} = "
                  r"\dfrac{%d}{%d} = %s$ (nghìn con)."
                  % (t0, a, t0, t0, b, a * t0, t0 + b,
                     _ps(N0.numerator, N0.denominator)))

        hoi_b = (r"Viết lại $N\left(t\right)$ dưới dạng thuận tiện cho "
                 r"việc tính giới hạn khi $t \to +\infty$.")
        giai_b = (r"Chia cả tử và mẫu cho $t$ (với $t > 0$):" +
                  "\\\\\n"
                  r"$N\left(t\right) = \dfrac{%dt}{t + %d} = "
                  r"\dfrac{%d}{1 + \dfrac{%d}{t}}$." % (a, b, a, b))

        hoi_c = (r"Về lâu dài số lượng vi khuẩn tiến tới giá trị nào? Giá "
                 r"trị đó có đạt được hay không?")
        giai_c = (r"Vì $\lim\limits_{t \to +\infty}\dfrac{%d}{t} = 0$ nên "
                  r"$\lim\limits_{t \to +\infty}N\left(t\right) = "
                  r"\dfrac{%d}{1 + 0} = %d$." % (b, a, a) +
                  "\\\\\n"
                  r"Vậy số lượng vi khuẩn tiến tới $%d$ nghìn con." % a +
                  "\\\\\n"
                  r"Giá trị này KHÔNG đạt được: với mọi $t \geq 0$ ta có "
                  r"$\dfrac{%d}{t + %d} > 0$ nên "
                  r"$N\left(t\right) = %d - \dfrac{%d}{t + %d} < %d$."
                  % (a * b, b, a, a * b, b, a))

        ds_abcd = [(hoi_a, r"N\left(0\right) = 0,\ N\left(%d\right) = %s"
                    % (t0, _ps(N0.numerator, N0.denominator)), giai_a),
                   (hoi_b, r"N\left(t\right) = \dfrac{%d}{1 + \dfrac{%d}{t}}"
                    % (a, b), giai_b),
                   (hoi_c, r"\lim\limits_{t \to +\infty}N\left(t\right) = %d"
                    % a, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 17. HÀM SỐ LIÊN TỤC
# =====================================================================

def L11_C5_B17_NB083_MC_A_01(socau, dang=1):
    r"""Nhận biết tính liên tục của các hàm sơ cấp cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-5, 5)
        b = random.choice([-4, -3, -2, 2, 3, 4])
        c = random.randint(1, 6)
        if (a, b, c) not in gt:
            gt.append((a, b, c))

    cauTN = ""
    for a, b, c in gt:
        dathuc = _tam_thuc(1, b, c, "x")
        mau = _nhi_thuc(1, -a, "x")
        dung = r"$f(x) = %s$" % dathuc
        nhieu = _ba_nhieu5(
            dung,
            [r"$f(x) = \dfrac{%d}{%s}$" % (c, mau),
             r"$f(x) = \sqrt{%s}$" % mau,
             r"$f(x) = \tan x$"],
            buoc=lambda t: r"$f(x) = \dfrac{%d}{%s}$"
            % (c + t, _nhi_thuc(1, -a - t, "x")))
        debai = r"Hàm số nào sau đây liên tục trên $\mathbb{R}$?"
        giai = (r"Hàm đa thức liên tục trên toàn bộ $\mathbb{R}$, nên "
                r"$f(x) = %s$ liên tục trên $\mathbb{R}$." % dathuc +
                "\\\\\n"
                r"Hàm phân thức $\dfrac{%d}{%s}$ không xác định tại "
                r"$x = %d$ nên không liên tục trên $\mathbb{R}$."
                % (c, mau, a) +
                "\\\\\n"
                r"Hàm $\sqrt{%s}$ chỉ xác định khi $x \geq %d$; hàm "
                r"$\tan x$ không xác định tại $x = \dfrac{\pi}{2} + k\pi$."
                % (mau, a))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B17_TH081_MC_A_01(socau, dang=1):
    r"""Nhận dạng điểm gián đoạn của hàm phân thức.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.randint(-6, 6)
        if b != -a and (a, b) not in gt:
            gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        mau = _nhi_thuc(1, -a, "x")
        tu = _nhi_thuc(1, b, "x")
        dung = "$x = %d$" % a
        nhieu = _ba_nhieu5(dung,
                           ["$x = %d$" % (-a), "$x = %d$" % (-b), "$x = 0$"],
                           buoc=lambda t: "$x = %d$" % (a + 10 * t))
        debai = (r"Hàm số $f(x) = \dfrac{%s}{%s}$ gián đoạn tại điểm nào "
                 r"sau đây?" % (tu, mau))
        giai = (r"Hàm phân thức liên tục trên từng khoảng của tập xác định." +
                "\\\\\n"
                r"Mẫu thức bằng $0$ khi $%s = 0 \Leftrightarrow x = %d$."
                % (mau, a) +
                "\\\\\n"
                r"Tại $x = %d$ hàm số không xác định nên gián đoạn; ở mọi "
                r"điểm khác hàm số liên tục." % a)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C5_B17_TH081_SA_A_01(socau):
    r"""Tìm tham số để hàm số liên tục tại một điểm (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        b = random.randint(-5, 5)
        if a != b and (a, b) not in gt:
            gt.append((a, b))

    cau = ""
    for a, b in gt:
        m = a - b
        tu = _tam_thuc(1, -(a + b), a * b, "x")
        mau = _nhi_thuc(1, -a, "x")
        debai = (r"Cho hàm số $f(x) = \dfrac{%s}{%s}$ khi $x \neq %d$ và "
                 r"$f\left(%d\right) = m$. Tìm $m$ để hàm số liên tục "
                 r"tại $x = %d$." % (tu, mau, a, a, a))
        giai = (r"Với $x \neq %d$ ta rút gọn được" % a +
                "\\\\\n"
                r"$f(x) = \dfrac{\left(%s\right)\left(%s\right)}{%s} = %s$."
                % (mau, _nhi_thuc(1, -b, "x"), mau, _nhi_thuc(1, -b, "x")) +
                "\\\\\n"
                r"Do đó $\lim\limits_{x \to %d}f(x) = %d$." % (a, m) +
                "\\\\\n"
                r"Hàm số liên tục tại $x = %d$ khi và chỉ khi "
                r"$\lim\limits_{x \to %d}f(x) = f\left(%d\right)$, "
                r"tức là $m = %d$." % (a, a, a, m))
        nhieu = _ba_nhieu5(str(m), [str(a), str(b), "0"],
                           buoc=lambda t: str(m + t))
        cau += MC_SA_answer_const(debai, str(m), nhieu, giai, 0, 0, 2)
    return cau


def L11_C5_B17_TH081_TL_A_01(socau, dong=1):
    r"""Tự luận: xét tính liên tục của hàm số cho bởi nhiều công thức.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-3, 3)
        b = random.randint(-5, 5)
        k = random.randint(-6, 6)
        if a != b and k != a - b and (a, b, k) not in gt:
            gt.append((a, b, k))

    cauTN = ""
    for a, b, k in gt:
        L = a - b
        tu = _tam_thuc(1, -(a + b), a * b, "x")
        mau = _nhi_thuc(1, -a, "x")
        debai = (r"Cho hàm số $f(x) = \dfrac{%s}{%s}$ khi $x \neq %d$ và "
                 r"$f\left(%d\right) = %d$." % (tu, mau, a, a, k))

        hoi_a = r"Tính $f\left(%d\right)$." % a
        giai_a = (r"Theo giả thiết, giá trị của hàm số tại $x = %d$ được "
                  r"cho riêng: $f\left(%d\right) = %d$." % (a, a, k))

        hoi_b = r"Tính $\lim\limits_{x \to %d}f(x)$." % a
        giai_b = (r"Với $x \neq %d$:" % a + "\\\\\n" +
                  r"$f(x) = \dfrac{\left(%s\right)\left(%s\right)}{%s} = %s$."
                  % (mau, _nhi_thuc(1, -b, "x"), mau,
                     _nhi_thuc(1, -b, "x")) +
                  "\\\\\n"
                  r"Vậy $\lim\limits_{x \to %d}f(x) = %d %s = %d$."
                  % (a, a, _dau(-b), L))

        hoi_c = r"Xét tính liên tục của hàm số tại $x = %d$." % a
        giai_c = (r"Ta có $\lim\limits_{x \to %d}f(x) = %d$ nhưng "
                  r"$f\left(%d\right) = %d$." % (a, L, a, k) +
                  "\\\\\n"
                  r"Vì $%d \neq %d$ nên hàm số KHÔNG liên tục tại "
                  r"$x = %d$ (gián đoạn tại điểm này)." % (L, k, a) +
                  "\\\\\n"
                  r"Nếu đổi giá trị $f\left(%d\right)$ thành $%d$ thì hàm "
                  r"số sẽ liên tục tại $x = %d$." % (a, L, a))

        ds_abcd = [(hoi_a, r"f\left(%d\right) = %d" % (a, k), giai_a),
                   (hoi_b, r"\lim\limits_{x \to %d}f(x) = %d" % (a, L),
                    giai_b),
                   (hoi_c, r"\text{Không liên tục tại } x = %d" % a, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L11_C5_B17_TH082_MC_A_01(socau, dang=1):
    r"""Tính liên tục của tổng, hiệu, tích, thương hai hàm liên tục.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        b = random.randint(-5, 5)
        c = random.randint(-6, 6)
        a = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        if (a, b, c) not in gt:
            gt.append((a, b, c))

    cauTN = ""
    for a, b, c in gt:
        f = _tam_thuc(1, b, c, "x")
        g = _nhi_thuc(1, -a, "x")
        dung = r"$\dfrac{f(x)}{g(x)}$"
        nhieu = _ba_nhieu5(dung,
                           [r"$f(x) + g(x)$", r"$f(x) - g(x)$",
                            r"$f(x)\cdot g(x)$"],
                           buoc=lambda t: r"$%d f(x) + g(x)$" % (t + 1))
        debai = (r"Cho hai hàm số $f(x) = %s$ và $g(x) = %s$. Hàm số nào "
                 r"sau đây KHÔNG liên tục trên $\mathbb{R}$?" % (f, g))
        giai = (r"$f$ và $g$ đều là hàm đa thức nên liên tục trên "
                r"$\mathbb{R}$." +
                "\\\\\n"
                r"Tổng, hiệu, tích của hai hàm liên tục trên $\mathbb{R}$ "
                r"vẫn liên tục trên $\mathbb{R}$." +
                "\\\\\n"
                r"Thương $\dfrac{f(x)}{g(x)}$ chỉ liên tục tại những điểm "
                r"mà $g(x) \neq 0$. Ở đây $g(x) = 0$ khi $x = %d$ nên "
                r"thương không liên tục trên $\mathbb{R}$." % a)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# =====================================================================
# ĐÚNG/SAI (cấp chương)
# =====================================================================

def L11_C5_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - giới hạn của dãy số và giới hạn của hàm số.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        b = random.choice([-5, -3, -2, 2, 3, 5])
        c = random.choice([2, 3, 4, 5])
        d = random.choice([-4, -3, -1, 1, 3, 4])
        if (a, b, c, d) not in gt:
            gt.append((a, b, c, d))

    cauTF = ""
    for a, b, c, d in gt:
        L = Fraction(a, c)
        debai = (r"Cho dãy số $u_n = \dfrac{%s}{%s}$ và hàm số "
                 r"$f(x) = %s$."
                 % (_nhi_thuc(a, b, "n"), _nhi_thuc(c, d, "n"),
                    _nhi_thuc(a, b, "x")))

        ds_abcd = (
            # a) NB - chỉ cần nhớ một giới hạn cơ bản
            [
                (r"{\True $\lim\dfrac{1}{n} = 0$}",
                 r"Đúng. Đây là một giới hạn cơ bản của dãy số: khi $n$ "
                 r"càng lớn thì $\dfrac{1}{n}$ càng gần $0$."),
                (r"{$\lim\dfrac{1}{n} = 1$}",
                 r"Sai. Khi $n \to +\infty$ thì $\dfrac{1}{n} \to 0$, "
                 r"không phải $1$."),
            ],
            # b) TH - thay số vào hàm đa thức
            [
                (r"{\True $\lim\limits_{x \to %d}f(x) = %d$}"
                 % (c, a * c + b),
                 r"Đúng. $f$ là hàm đa thức nên liên tục, do đó "
                 r"$\lim\limits_{x \to %d}f(x) = f\left(%d\right) = "
                 r"%d\cdot %d %s = %d$."
                 % (c, c, a, c, _dau(b), a * c + b)),
                (r"{$\lim\limits_{x \to %d}f(x) = %d$}" % (c, a + b),
                 r"Sai. Phải thay $x = %d$ vào cả hạng tử chứa $x$: "
                 r"$f\left(%d\right) = %d$." % (c, c, a * c + b)),
            ],
            # c) VD - phải chia cho n rồi mới kết luận
            [
                (r"{\True $\lim u_n = %s$}"
                 % _ps(L.numerator, L.denominator),
                 r"Đúng. Chia cả tử và mẫu cho $n$:" + "\\\\\n" +
                 r"$u_n = \dfrac{%d %s}{%d %s}$."
                 % (a, _hang_chia(b), c, _hang_chia(d)) + "\\\\\n" +
                 r"Vì $\dfrac{%d}{n} \to 0$ và $\dfrac{%d}{n} \to 0$ nên "
                 r"$\lim u_n = \dfrac{%d}{%d}%s$."
                 % (abs(b), abs(d), a, c,
                    ("" if _ps(a, c) == r"\dfrac{%d}{%d}" % (a, c)
                     else " = %s" % _ps(a, c)))),
                (r"{$\lim u_n = %s$}" % _ps(b, d),
                 r"Sai. Đó là tỉ số của hai hạng tử tự do. Bậc cao nhất "
                 r"của tử và mẫu đều là $1$ nên giới hạn bằng tỉ số hai "
                 r"HỆ SỐ của $n$, tức là $%s$."
                 % _ps(L.numerator, L.denominator)),
            ],
            # d) VDC - phải tự nhận ra dạng 0/0 và phân tích nhân tử
            [
                (r"{\True $\lim\limits_{x \to %d}"
                 r"\dfrac{x^{2} - %d}{%s} = %d$}"
                 % (c, c * c, _nhi_thuc(1, -c, "x"), 2 * c),
                 r"Đúng. Thay $x = %d$ thì tử và mẫu cùng bằng $0$, đây là "
                 r"dạng vô định $\dfrac{0}{0}$." % c + "\\\\\n" +
                 r"$\dfrac{x^{2} - %d}{%s} = \dfrac{\left(%s\right)"
                 r"\left(%s\right)}{%s} = %s$ với $x \neq %d$."
                 % (c * c, _nhi_thuc(1, -c, "x"), _nhi_thuc(1, -c, "x"),
                    _nhi_thuc(1, c, "x"), _nhi_thuc(1, -c, "x"),
                    _nhi_thuc(1, c, "x"), c) + "\\\\\n" +
                 r"Vậy giới hạn bằng $%d + %d = %d$." % (c, c, 2 * c)),
                (r"{$\lim\limits_{x \to %d}\dfrac{x^{2} - %d}{%s}$ "
                 r"không tồn tại vì mẫu bằng $0$}"
                 % (c, c * c, _nhi_thuc(1, -c, "x")),
                 r"Sai. Mẫu bằng $0$ nhưng tử cũng bằng $0$, nên không kết "
                 r"luận ngay được. Sau khi rút gọn nhân tử $%s$ thì giới "
                 r"hạn tồn tại và bằng $%d$."
                 % (_nhi_thuc(1, -c, "x"), 2 * c)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L11_C5_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - hàm số liên tục.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-5, 5)
        k = random.randint(-6, 6)
        if a != b and k != a - b and (a, b, k) not in gt:
            gt.append((a, b, k))

    cauTF = ""
    for a, b, k in gt:
        L = a - b
        tu = _tam_thuc(1, -(a + b), a * b, "x")
        mau = _nhi_thuc(1, -a, "x")
        debai = (r"Cho hàm số $f(x) = \dfrac{%s}{%s}$ khi $x \neq %d$ và "
                 r"$f\left(%d\right) = %d$." % (tu, mau, a, a, k))

        ds_abcd = (
            # a) NB - chỉ cần đọc giả thiết
            [
                (r"{\True $f\left(%d\right) = %d$}" % (a, k),
                 r"Đúng. Giá trị của hàm số tại $x = %d$ được cho riêng "
                 r"trong giả thiết là $%d$." % (a, k)),
                (r"{Hàm số không xác định tại $x = %d$}" % a,
                 r"Sai. Hàm số có xác định tại $x = %d$ vì giả thiết đã "
                 r"cho $f\left(%d\right) = %d$." % (a, a, k)),
            ],
            # b) TH - rút gọn rồi thay số
            [
                (r"{\True Với $x \neq %d$ thì $f(x) = %s$}"
                 % (a, _nhi_thuc(1, -b, "x")),
                 r"Đúng. $%s = \left(%s\right)\left(%s\right)$ nên rút gọn "
                 r"được $f(x) = %s$ khi $x \neq %d$."
                 % (tu, mau, _nhi_thuc(1, -b, "x"),
                    _nhi_thuc(1, -b, "x"), a)),
                (r"{Với $x \neq %d$ thì $f(x) = %s$}"
                 % (a, _nhi_thuc(1, -a, "x")),
                 r"Sai. Nhân tử bị rút gọn là $%s$, phần còn lại là $%s$."
                 % (mau, _nhi_thuc(1, -b, "x"))),
            ],
            # c) VD - tính giới hạn từ dạng rút gọn
            [
                (r"{\True $\lim\limits_{x \to %d}f(x) = %d$}" % (a, L),
                 r"Đúng. Sau khi rút gọn, $\lim\limits_{x \to %d}f(x) = "
                 r"\lim\limits_{x \to %d}\left(%s\right) = %d %s = %d$."
                 % (a, a, _nhi_thuc(1, -b, "x"), a, _dau(-b), L)),
                (r"{$\lim\limits_{x \to %d}f(x) = %d$}" % (a, k),
                 r"Sai. Đó là GIÁ TRỊ $f\left(%d\right)$, còn giới hạn "
                 r"phải tính từ dạng rút gọn và bằng $%d$." % (a, L)),
            ],
            # d) VDC - so sánh giới hạn với giá trị rồi kết luận
            [
                (r"{\True Hàm số gián đoạn tại $x = %d$}" % a,
                 r"Đúng. Hàm số liên tục tại $x = %d$ khi và chỉ khi "
                 r"$\lim\limits_{x \to %d}f(x) = f\left(%d\right)$."
                 % (a, a, a) + "\\\\\n" +
                 r"Ở đây $\lim\limits_{x \to %d}f(x) = %d$ nhưng "
                 r"$f\left(%d\right) = %d$, mà $%d \neq %d$."
                 % (a, L, a, k, L, k) + "\\\\\n" +
                 r"Vậy hàm số gián đoạn tại $x = %d$; muốn liên tục thì "
                 r"phải sửa $f\left(%d\right)$ thành $%d$." % (a, a, L)),
                (r"{Hàm số liên tục trên $\mathbb{R}$}",
                 r"Sai. Hàm số liên tục tại mọi $x \neq %d$, nhưng tại "
                 r"$x = %d$ thì giới hạn ($%d$) khác giá trị ($%d$) nên "
                 r"gián đoạn." % (a, a, L, k)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
