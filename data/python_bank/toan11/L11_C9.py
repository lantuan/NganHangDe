# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 9. Đạo hàm (bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Công thức dùng trong tệp (đúng SGK KNTT lớp 11):

  * Định nghĩa: $f'(x_0) = \lim\limits_{x \to x_0}
    \dfrac{f(x) - f(x_0)}{x - x_0}$.
  * Ý nghĩa hình học: $f'(x_0)$ là hệ số góc của tiếp tuyến của đồ thị
    tại điểm $M\left(x_0;\ f(x_0)\right)$; tiếp tuyến có phương trình
    $y = f'(x_0)\left(x - x_0\right) + f(x_0)$.
  * Ý nghĩa cơ học: $s(t)$ là quãng đường thì $v(t) = s'(t)$ là vận tốc
    tức thời và $a(t) = s''(t)$ là gia tốc tức thời.
  * Quy tắc: $\left(u \pm v\right)' = u' \pm v'$;
    $\left(uv\right)' = u'v + uv'$;
    $\left(\dfrac{u}{v}\right)' = \dfrac{u'v - uv'}{v^2}$;
    hàm hợp $\left[f(u)\right]' = f'(u)\cdot u'$.
  * $\left(x^{n}\right)' = nx^{\,n-1}$; $\left(\sqrt{x}\right)' =
    \dfrac{1}{2\sqrt{x}}$; $\left(\sin x\right)' = \cos x$;
    $\left(\cos x\right)' = -\sin x$; $\left(e^{x}\right)' = e^{x}$;
    $\left(\ln x\right)' = \dfrac{1}{x}$.

Số liệu chọn để ĐÁP SỐ ĐẸP: hệ số nguyên, điểm $x_0$ nguyên, nên mọi
giá trị đạo hàm và mọi hệ số của tiếp tuyến đều nguyên - câu trả lời
ngắn chấm bằng SO KHỚP CHUỖI.

Bài học từ lớp 10 (docs/16_CHANGELOG Version 3.14) đã áp dụng: chữ
tiếng Việt không nằm trần trong $...$; không dùng chữ đậm kiểu Markdown;
mọi chuỗi có dấu gạch chéo đều là chuỗi r"..."; mọi danh sách phương án
nhiễu đều đi qua _ba_nhieu9.
"""
import math
import random

from math_type import *          # noqa: F401,F403

DAU_THAP_PHAN = ","


def _xx(x, n=2):
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu9(dapso, ung_vien, buoc=None):
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


def _dau(x):
    return ("+ %d" % abs(x)) if x >= 0 else ("- %d" % abs(x))


def _da_thuc(hs, bien="x"):
    r"""Viết đa thức từ danh sách hệ số [a_n, ..., a_1, a_0]."""
    bac = len(hs) - 1
    phan = []
    for i, a in enumerate(hs):
        k = bac - i
        if a == 0:
            continue
        if k == 0:
            he = "%d" % abs(a)
        else:
            he = "" if abs(a) == 1 else "%d" % abs(a)
        mu = "" if k == 0 else (bien if k == 1 else r"%s^{%d}" % (bien, k))
        cum = he + mu
        if not phan:
            phan.append(("-" if a < 0 else "") + cum)
        else:
            phan.append(("+ " if a > 0 else "- ") + cum)
    return " ".join(phan) if phan else "0"


def _gia_tri(hs, x):
    s = 0
    for a in hs:
        s = s * x + a
    return s


def _dao_ham(hs):
    """Hệ số của đạo hàm, cùng quy ước [a_n, ..., a_0]."""
    bac = len(hs) - 1
    ra = [a * (bac - i) for i, a in enumerate(hs[:-1])]
    return ra if ra else [0]


def _bo_da_thuc(bac=3):
    """Đa thức hệ số nguyên, hệ số đầu khác 0."""
    while True:
        hs = [random.randint(-4, 5) for _ in range(bac + 1)]
        if hs[0]:
            return hs


def _diem_dep(hs, lan_thu=200):
    """x0 nguyên nhỏ để f(x0) và f'(x0) không quá lớn."""
    dh = _dao_ham(hs)
    for _ in range(lan_thu):
        x0 = random.randint(-3, 3)
        if abs(_gia_tri(hs, x0)) <= 60 and abs(_gia_tri(dh, x0)) <= 60:
            return x0
    return 1


# =====================================================================
# BÀI 31. ĐỊNH NGHĨA VÀ Ý NGHĨA CỦA ĐẠO HÀM
# =====================================================================

def L11_C9_B31_NB137_MC_A_01(socau, dang=1):
    r"""Bài toán dẫn đến khái niệm đạo hàm (vận tốc tức thời).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(2, 6)
        b = random.randint(1, 9)
        if (a, b) not in gt:
            gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        dung = r"$s'\left(t_0\right)$"
        nhieu = _ba_nhieu9(
            dung,
            [r"$s\left(t_0\right)$", r"$\dfrac{s\left(t_0\right)}{t_0}$",
             r"$s''\left(t_0\right)$"],
            buoc=lambda k: r"$s\left(t_0\right) - s(0)$")
        debai = (r"Một chất điểm chuyển động thẳng có phương trình quãng "
                 r"đường $s = s(t) = %dt^2 %s t$ (mét, giây). Vận tốc TỨC "
                 r"THỜI của chất điểm tại thời điểm $t_0$ được tính bằng "
                 r"đại lượng nào sau đây?" % (a, _dau(b)))
        giai = (r"Vận tốc trung bình trên đoạn từ $t_0$ đến $t$ là "
                r"$\dfrac{s(t) - s\left(t_0\right)}{t - t_0}$."
                "\\\\\n"
                r"Cho $t \to t_0$, giới hạn của tỉ số ấy chính là vận tốc "
                r"tức thời, và theo định nghĩa đó cũng là đạo hàm:"
                "\\\\\n"
                r"$v\left(t_0\right) = \lim\limits_{t \to t_0}"
                r"\dfrac{s(t) - s\left(t_0\right)}{t - t_0} "
                r"= s'\left(t_0\right)$."
                "\\\\\n"
                r"Đây chính là bài toán đã dẫn đến khái niệm đạo hàm.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B31_NB138_MC_A_01(socau, dang=1):
    r"""Định nghĩa đạo hàm tại một điểm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        x0 = random.randint(1, 5)
        if x0 not in gt:
            gt.append(x0)

    cauTN = ""
    for x0 in gt:
        dung = (r"$\lim\limits_{x \to %d}\dfrac{f(x) - f(%d)}{x - %d}$"
                % (x0, x0, x0))
        nhieu = _ba_nhieu9(
            dung,
            [r"$\lim\limits_{x \to %d}\dfrac{f(x) - f(%d)}{x}$" % (x0, x0),
             r"$\lim\limits_{x \to %d}\dfrac{f(x)}{x - %d}$" % (x0, x0),
             r"$\lim\limits_{x \to 0}\dfrac{f(x) - f(%d)}{x - %d}$"
             % (x0, x0)],
            buoc=lambda k: r"$\dfrac{f(%d)}{%d}$" % (x0, x0))
        debai = (r"Cho hàm số $y = f(x)$ xác định trên một khoảng chứa "
                 r"$x_0 = %d$. Đạo hàm của hàm số tại $x_0 = %d$ được định "
                 r"nghĩa là giới hạn nào sau đây?" % (x0, x0))
        giai = (r"Theo định nghĩa, $f'\left(x_0\right) = "
                r"\lim\limits_{x \to x_0}"
                r"\dfrac{f(x) - f\left(x_0\right)}{x - x_0}$ (nếu giới hạn "
                r"này tồn tại và hữu hạn)."
                "\\\\\n"
                r"Thay $x_0 = %d$ được đúng biểu thức ở phương án đúng."
                % x0 +
                "\\\\\n"
                r"Chú ý cả tử và mẫu đều phải trừ đi giá trị tại $x_0$, và "
                r"$x$ phải dần tới $x_0$ chứ không phải tới $0$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B31_NB140_MC_A_01(socau, dang=1):
    r"""Ý nghĩa hình học của đạo hàm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = _bo_da_thuc(random.choice([2, 3]))
        x0 = _diem_dep(hs)
        k = _gia_tri(_dao_ham(hs), x0)
        if (tuple(hs), x0) not in gt:
            gt.append((tuple(hs), x0, k))

    cauTN = ""
    for hs, x0, k in gt:
        hs = list(hs)
        dung = r"$%d$" % k
        nhieu = _ba_nhieu9(
            dung,
            [r"$%d$" % _gia_tri(hs, x0), r"$%d$" % x0, r"$%d$" % (-k)],
            buoc=lambda t: r"$%d$" % (k + t))
        debai = (r"Cho hàm số $y = f(x) = %s$ có đồ thị $\left(C\right)$. "
                 r"Hệ số góc của tiếp tuyến của $\left(C\right)$ tại điểm "
                 r"có hoành độ $x_0 = %d$ bằng bao nhiêu?"
                 % (_da_thuc(hs), x0))
        giai = (r"Ý nghĩa hình học của đạo hàm: hệ số góc của tiếp tuyến "
                r"tại điểm có hoành độ $x_0$ chính là $f'\left(x_0\right)$."
                "\\\\\n"
                r"$f'(x) = %s$." % _da_thuc(_dao_ham(hs)) +
                "\\\\\n"
                r"$f'\left(%d\right) = %d$." % (x0, k) +
                "\\\\\n"
                r"Chú ý phân biệt với $f\left(%d\right) = %d$ - đó là TUNG "
                r"ĐỘ của tiếp điểm, không phải hệ số góc."
                % (x0, _gia_tri(hs, x0)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B31_NB142_MC_A_01(socau, dang=1):
    r"""Số e.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    Y = [
        (r"$e = \lim\limits_{n \to +\infty}"
         r"\left(1 + \dfrac{1}{n}\right)^{n}$",
         r"Đúng. Đây là định nghĩa của số $e$ trong SGK: giới hạn của dãy "
         r"$\left(1 + \dfrac{1}{n}\right)^{n}$ khi $n \to +\infty$."),
        (r"$e$ là một số vô tỉ, $e \approx 2,718281$",
         r"Đúng. $e$ là số vô tỉ; giá trị gần đúng thường dùng là "
         r"$e \approx 2,718$."),
    ]
    SAI = [
        r"$e$ là một số hữu tỉ",
        r"$e = \lim\limits_{n \to +\infty}\left(1 + n\right)^{n}$",
        r"$e = 2$",
        r"$e = \lim\limits_{n \to 0}\left(1 + \dfrac{1}{n}\right)^{n}$",
        r"$e \approx 3,141592$",
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(Y))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(Y):
            break

    cauTN = ""
    for i in gt:
        dung, vi_sao = Y[i]
        nhieu = _ba_nhieu9(dung, list(SAI),
                           buoc=lambda t: r"$e = %d$" % (t + 3))
        debai = r"Khẳng định nào sau đây về số $e$ là đúng?"
        giai = (vi_sao +
                "\\\\\n"
                r"Nhắc lại: $e = \lim\limits_{n \to +\infty}"
                r"\left(1 + \dfrac{1}{n}\right)^{n} \approx 2,718281$, là "
                r"một số vô tỉ; $e$ được chọn làm cơ số của lôgarit tự "
                r"nhiên $\ln$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B31_TH139_MC_A_01(socau, dang=1):
    r"""Đạo hàm của hàm đơn giản bằng ĐỊNH NGHĨA.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([1, 2, 3, -1, -2])
        b = random.randint(-6, 6)
        c = random.randint(-6, 6)
        x0 = random.randint(-3, 4)
        v = (a, b, c, x0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, x0 in gt:
        hs = [a, b, c]
        k = 2 * a * x0 + b
        dung = r"$%d$" % k
        nhieu = _ba_nhieu9(
            dung,
            [r"$%d$" % _gia_tri(hs, x0), r"$%d$" % (a * x0 + b),
             r"$%d$" % (2 * a * x0), r"$%d$" % (-k)],
            buoc=lambda t: r"$%d$" % (k + t))
        debai = (r"Dùng định nghĩa, tính đạo hàm của hàm số "
                 r"$f(x) = %s$ tại điểm $x_0 = %d$."
                 % (_da_thuc(hs), x0))
        giai = (r"$f\left(%d\right) = %d$." % (x0, _gia_tri(hs, x0)) +
                "\\\\\n"
                r"Với $x \ne %d$:" % x0 +
                "\\\\\n"
                r"$\dfrac{f(x) - f\left(%d\right)}{x - %d} "
                r"= \dfrac{%s\left(x^2 - %d\right) %s\left(x - %d\right)}"
                r"{x - %d}$"
                % (x0, x0,
                   ("" if a == 1 else ("-" if a == -1 else "%d" % a)),
                   x0 * x0,
                   ("+ %d" % b) if b >= 0 else ("- %d" % (-b)), x0, x0) +
                "\\\\\n"
                r"$= %s\left(x + %d\right) %s$."
                % (("" if a == 1 else ("-" if a == -1 else "%d" % a)), x0,
                   ("+ %d" % b) if b >= 0 else ("- %d" % (-b))) +
                "\\\\\n"
                r"Cho $x \to %d$ được $f'\left(%d\right) "
                r"= %s\cdot %d %s = %d$."
                % (x0, x0,
                   ("" if a == 1 else ("-" if a == -1 else "%d" % a)),
                   2 * x0, ("+ %d" % b) if b >= 0 else ("- %d" % (-b)), k) +
                "\\\\\n"
                r"Kiểm lại bằng công thức: $f'(x) = %s$, thay $x = %d$ "
                r"cũng được $%d$." % (_da_thuc(_dao_ham(hs)), x0, k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B31_TH139_SA_A_01(socau):
    r"""Đạo hàm tại một điểm bằng định nghĩa - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = _bo_da_thuc(random.choice([2, 3]))
        x0 = _diem_dep(hs)
        if (tuple(hs), x0) not in gt:
            gt.append((tuple(hs), x0))

    cau = ""
    for hs, x0 in gt:
        hs = list(hs)
        dh = _dao_ham(hs)
        k = _gia_tri(dh, x0)
        debai = (r"Cho hàm số $f(x) = %s$. Tính $f'\left(%d\right)$."
                 % (_da_thuc(hs), x0))
        giai = (r"$f'(x) = %s$." % _da_thuc(dh) +
                "\\\\\n"
                r"$f'\left(%d\right) = %d$." % (x0, k))
        nhieu = _ba_nhieu9(str(k), [str(_gia_tri(hs, x0)), str(k + 1),
                                    str(-k)],
                           buoc=lambda t: str(k + t + 1))
        cau += MC_SA_answer_const(debai, str(k), nhieu, giai, 0, 0, 2)
    return cau


def L11_C9_B31_TH141_MC_A_01(socau, dang=1):
    r"""Phương trình tiếp tuyến tại một điểm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = _bo_da_thuc(random.choice([2, 3]))
        x0 = _diem_dep(hs)
        if (tuple(hs), x0) not in gt:
            gt.append((tuple(hs), x0))

    cauTN = ""
    for hs, x0 in gt:
        hs = list(hs)
        y0 = _gia_tri(hs, x0)
        k = _gia_tri(_dao_ham(hs), x0)
        b = y0 - k * x0
        dung = r"$y = %s$" % _da_thuc([k, b]) if k else r"$y = %d$" % b
        nhieu = _ba_nhieu9(
            dung,
            [r"$y = %s$" % _da_thuc([k, y0]),          # quen tru k*x0
             r"$y = %s$" % _da_thuc([y0, b]),          # nham he so goc
             r"$y = %s$" % _da_thuc([k, b + 1]),
             r"$y = %s$" % _da_thuc([-k, b])],
            buoc=lambda t: r"$y = %s$" % _da_thuc([k, b + t + 1]))
        debai = (r"Viết phương trình tiếp tuyến của đồ thị hàm số "
                 r"$y = %s$ tại điểm có hoành độ $x_0 = %d$."
                 % (_da_thuc(hs), x0))
        giai = (r"Tung độ tiếp điểm: $y_0 = f\left(%d\right) = %d$."
                % (x0, y0) +
                "\\\\\n"
                r"$f'(x) = %s$ nên hệ số góc $k = f'\left(%d\right) = %d$."
                % (_da_thuc(_dao_ham(hs)), x0, k) +
                "\\\\\n"
                r"Phương trình tiếp tuyến tại $M\left(%d;\ %d\right)$:"
                % (x0, y0) +
                "\\\\\n"
                r"$y = f'\left(x_0\right)\left(x - x_0\right) + y_0 "
                r"= %d\left(x %s\right) %s = %s$."
                % (k, _dau(-x0), _dau(y0), _da_thuc([k, b])) +
                "\\\\\n"
                r"Chú ý phải trừ $x_0$ trong ngoặc rồi mới cộng $y_0$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B31_TH141_SA_A_01(socau):
    r"""Hệ số góc của tiếp tuyến - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = _bo_da_thuc(random.choice([2, 3]))
        x0 = _diem_dep(hs)
        if (tuple(hs), x0) not in gt:
            gt.append((tuple(hs), x0))

    cau = ""
    for hs, x0 in gt:
        hs = list(hs)
        k = _gia_tri(_dao_ham(hs), x0)
        debai = (r"Cho hàm số $y = %s$. Tính hệ số góc của tiếp tuyến của "
                 r"đồ thị hàm số tại điểm có hoành độ $x_0 = %d$."
                 % (_da_thuc(hs), x0))
        giai = (r"Hệ số góc của tiếp tuyến bằng đạo hàm tại tiếp điểm."
                "\\\\\n"
                r"$f'(x) = %s$ nên $k = f'\left(%d\right) = %d$."
                % (_da_thuc(_dao_ham(hs)), x0, k))
        nhieu = _ba_nhieu9(str(k), [str(_gia_tri(hs, x0)), str(-k),
                                    str(k + 1)],
                           buoc=lambda t: str(k + t + 1))
        cau += MC_SA_answer_const(debai, str(k), nhieu, giai, 0, 0, 2)
    return cau


def L11_C9_B31_TH141_TL_A_01(socau, dong=1):
    r"""Tự luận: viết phương trình tiếp tuyến.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = _bo_da_thuc(3)
        x0 = _diem_dep(hs)
        if (tuple(hs), x0) not in gt:
            gt.append((tuple(hs), x0))

    cauTN = ""
    for hs, x0 in gt:
        hs = list(hs)
        dh = _dao_ham(hs)
        y0 = _gia_tri(hs, x0)
        k = _gia_tri(dh, x0)
        b = y0 - k * x0
        debai = (r"Cho hàm số $y = f(x) = %s$ có đồ thị $\left(C\right)$."
                 % _da_thuc(hs))

        hoi_a = r"Tính $f'(x)$."
        giai_a = (r"Áp dụng $\left(x^{n}\right)' = nx^{\,n-1}$ cho từng "
                  r"hạng tử:"
                  "\\\\\n"
                  r"$f'(x) = %s$." % _da_thuc(dh))

        hoi_b = (r"Tính $f\left(%d\right)$ và $f'\left(%d\right)$."
                 % (x0, x0))
        giai_b = (r"$f\left(%d\right) = %d$ và $f'\left(%d\right) = %d$."
                  % (x0, y0, x0, k))

        hoi_c = (r"Viết phương trình tiếp tuyến của $\left(C\right)$ tại "
                 r"điểm có hoành độ $x_0 = %d$." % x0)
        giai_c = (r"$y = f'\left(x_0\right)\left(x - x_0\right) + "
                  r"f\left(x_0\right)$"
                  "\\\\\n"
                  r"$= %d\left(x %s\right) %s = %s$."
                  % (k, _dau(-x0), _dau(y0), _da_thuc([k, b])))

        ds_abcd = [(hoi_a, r"f'(x) = %s" % _da_thuc(dh), giai_a),
                   (hoi_b, r"f\left(%d\right) = %d,\ f'\left(%d\right) = %d"
                    % (x0, y0, x0, k), giai_b),
                   (hoi_c, r"y = %s" % _da_thuc([k, b]), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 32. CÁC QUY TẮC TÍNH ĐẠO HÀM
# =====================================================================

SO_CAP = [
    (r"x^{%d}", r"%dx^{%d}", "luy_thua"),
    (r"\sqrt{x}", r"\dfrac{1}{2\sqrt{x}}", "can"),
    (r"\sin x", r"\cos x", "sin"),
    (r"\cos x", r"-\sin x", "cos"),
    (r"e^{x}", r"e^{x}", "mu"),
    (r"\ln x", r"\dfrac{1}{x}", "ln"),
]


def L11_C9_B32_TH143_MC_A_01(socau, dang=1):
    r"""Đạo hàm của một số hàm số sơ cấp cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(SO_CAP))
        n = random.randint(3, 7)
        if (i, n) not in gt:
            gt.append((i, n))

    cauTN = ""
    for i, n in gt:
        ham, dh, loai = SO_CAP[i]
        if loai == "luy_thua":
            f = ham % n
            d = dh % (n, n - 1)
            sai = [r"%dx^{%d}" % (n, n), r"x^{%d}" % (n - 1),
                   r"\dfrac{x^{%d}}{%d}" % (n + 1, n + 1)]
            vi_sao = (r"Áp dụng $\left(x^{n}\right)' = nx^{\,n-1}$: hạ số "
                      r"mũ xuống làm hệ số rồi giảm số mũ đi $1$.")
        else:
            f = ham
            d = dh
            sai = [x[1] for x in SO_CAP if x[1] != d][:3]
            vi_sao = r"Đây là công thức đạo hàm cơ bản cần thuộc."
        dung = r"$%s$" % d
        nhieu = _ba_nhieu9(dung, [r"$%s$" % x for x in sai],
                           buoc=lambda t: r"$%dx$" % (t + 1))
        debai = r"Tính đạo hàm của hàm số $y = %s$." % f
        giai = (vi_sao +
                "\\\\\n"
                r"$\left(%s\right)' = %s$." % (f, d))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B32_TH143_SA_A_01(socau):
    r"""Giá trị đạo hàm của hàm sơ cấp tại một điểm - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.randint(2, 5)
        a = random.randint(2, 6)
        x0 = random.randint(1, 4)
        if (n, a, x0) not in gt:
            gt.append((n, a, x0))

    cau = ""
    for n, a, x0 in gt:
        k = a * n * x0 ** (n - 1)
        debai = (r"Cho hàm số $y = f(x) = %dx^{%d}$. Tính "
                 r"$f'\left(%d\right)$." % (a, n, x0))
        giai = (r"$f'(x) = %d\cdot %dx^{%d} = %dx^{%d}$."
                % (a, n, n - 1, a * n, n - 1) +
                "\\\\\n"
                r"$f'\left(%d\right) = %d\cdot %d^{%d} = %d$."
                % (x0, a * n, x0, n - 1, k))
        nhieu = _ba_nhieu9(str(k), [str(a * x0 ** n), str(a * n * x0 ** n),
                                    str(k + 1)],
                           buoc=lambda t: str(k + t + 1))
        cau += MC_SA_answer_const(debai, str(k), nhieu, giai, 0, 0, 2)
    return cau


def L11_C9_B32_TH144_MC_A_01(socau, dang=1):
    r"""Quy tắc đạo hàm của tích hai đa thức.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([1, 2, 3])
        b = random.randint(-5, 5)
        c = random.choice([1, 2, 3])
        d = random.randint(-5, 5)
        x0 = random.randint(-2, 3)
        v = (a, b, c, d, x0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, d, x0 in gt:
        # u = ax + b, v = cx^2 + d  ->  (uv)' = a(cx^2+d) + (ax+b)(2cx)
        u0, v0 = a * x0 + b, c * x0 * x0 + d
        k = a * v0 + u0 * 2 * c * x0
        dung = r"$%d$" % k
        nhieu = _ba_nhieu9(
            dung,
            [r"$%d$" % (a * 2 * c * x0),         # nhan hai dao ham
             r"$%d$" % (u0 * v0),
             r"$%d$" % (a * v0), r"$%d$" % (u0 * 2 * c * x0)],
            buoc=lambda t: r"$%d$" % (k + t))
        debai = (r"Cho hàm số $y = f(x) = \left(%s\right)\left(%s\right)$. "
                 r"Tính $f'\left(%d\right)$."
                 % (_da_thuc([a, b]), _da_thuc([c, 0, d]), x0))
        giai = (r"Đặt $u = %s$ và $v = %s$, ta có $u' = %d$ và $v' = %dx$."
                % (_da_thuc([a, b]), _da_thuc([c, 0, d]), a, 2 * c) +
                "\\\\\n"
                r"$\left(uv\right)' = u'v + uv'$ nên"
                "\\\\\n"
                r"$f'(x) = %d\left(%s\right) + \left(%s\right)\cdot %dx$."
                % (a, _da_thuc([c, 0, d]), _da_thuc([a, b]), 2 * c) +
                "\\\\\n"
                r"Thay $x = %d$: $u\left(%d\right) = %d$, "
                r"$v\left(%d\right) = %d$." % (x0, x0, u0, x0, v0) +
                "\\\\\n"
                r"$f'\left(%d\right) = %d\cdot %d + %d\cdot %d = %d$."
                % (x0, a, v0, u0, 2 * c * x0, k) +
                "\\\\\n"
                r"Chú ý đạo hàm của tích KHÔNG phải tích hai đạo hàm.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B32_TH144_SA_A_01(socau):
    r"""Đạo hàm của hàm hợp - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4])
        b = random.randint(-5, 5)
        n = random.choice([2, 3])
        x0 = random.randint(-1, 3)
        if abs(a * x0 + b) > 8:
            continue
        v = (a, b, n, x0)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, n, x0 in gt:
        u0 = a * x0 + b
        k = n * u0 ** (n - 1) * a
        debai = (r"Cho hàm số $y = f(x) = \left(%s\right)^{%d}$. Tính "
                 r"$f'\left(%d\right)$." % (_da_thuc([a, b]), n, x0))
        giai = (r"Đặt $u = %s$ thì $y = u^{%d}$, $u' = %d$."
                % (_da_thuc([a, b]), n, a) +
                "\\\\\n"
                r"Đạo hàm hàm hợp: $y' = %du^{%d}\cdot u' "
                r"= %d\left(%s\right)^{%d}\cdot %d$."
                % (n, n - 1, n, _da_thuc([a, b]), n - 1, a) +
                "\\\\\n"
                r"Thay $x = %d$: $u = %d$ nên "
                r"$f'\left(%d\right) = %d\cdot %d^{%d}\cdot %d = %d$."
                % (x0, u0, x0, n, u0, n - 1, a, k))
        nhieu = _ba_nhieu9(str(k), [str(n * u0 ** (n - 1)), str(u0 ** n),
                                    str(k + a)],
                           buoc=lambda t: str(k + t + 1))
        cau += MC_SA_answer_const(debai, str(k), nhieu, giai, 0, 0, 2)
    return cau


def L11_C9_B32_TH144_TL_A_01(socau, dong=1):
    r"""Tự luận: tính đạo hàm rồi giải phương trình $f'(x) = 0$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        # f(x) = 2x^3 - 3(p+q)x^2 + 6pq x + r  =>  f'(x) = 6(x-p)(x-q)
        p = random.randint(-4, 4)
        q = random.randint(-4, 4)
        r = random.randint(-6, 6)
        if p == q:
            continue
        if (p, q, r) not in gt:
            gt.append((p, q, r))

    cauTN = ""
    for p, q, r in gt:
        hs = [2, -3 * (p + q), 6 * p * q, r]
        dh = _dao_ham(hs)
        x0 = 1
        debai = r"Cho hàm số $y = f(x) = %s$." % _da_thuc(hs)

        hoi_a = r"Tính $f'(x)$."
        giai_a = (r"$f'(x) = %s$." % _da_thuc(dh) +
                  "\\\\\n"
                  r"Có thể đặt $6$ làm nhân tử chung: "
                  r"$f'(x) = 6\left(x^{2} %s x %s\right)$."
                  % (_dau(-(p + q)), _dau(p * q)))

        hoi_b = r"Tính $f'\left(%d\right)$." % x0
        giai_b = (r"$f'\left(%d\right) = %d$." % (x0, _gia_tri(dh, x0)))

        hoi_c = r"Giải phương trình $f'(x) = 0$."
        giai_c = (r"$f'(x) = 6\left(x %s\right)\left(x %s\right) = 0$."
                  % (_dau(-p), _dau(-q)) +
                  "\\\\\n"
                  r"Vậy $x = %d$ hoặc $x = %d$."
                  % (min(p, q), max(p, q)) +
                  "\\\\\n"
                  r"Kiểm lại: $%d + %d = %d$ và $%d\cdot %d = %d$, khớp "
                  r"với $x^{2} %s x %s$."
                  % (p, q, p + q, p, q, p * q, _dau(-(p + q)), _dau(p * q)))

        ds_abcd = [(hoi_a, r"f'(x) = %s" % _da_thuc(dh), giai_a),
                   (hoi_b, r"f'\left(%d\right) = %d" % (x0, _gia_tri(dh, x0)),
                    giai_b),
                   (hoi_c, r"x = %d \text{ hoặc } x = %d"
                    % (min(p, q), max(p, q)), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def _bo_chuyen_dong():
    r"""$s(t) = at^3 + bt^2 + ct$ với hệ số nguyên nhỏ."""
    a = random.choice([1, 2])
    b = random.randint(-6, 6)
    c = random.randint(1, 12)
    t0 = random.randint(1, 5)
    return a, b, c, t0


def L11_C9_B32_VD145_MC_A_01(socau, dang=1):
    r"""Vận tốc tức thời - bài toán liên môn Vật lí.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_chuyen_dong()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, t0 in gt:
        s = [a, b, c, 0]
        vt = _dao_ham(s)
        k = _gia_tri(vt, t0)
        dung = r"$%d$" % k
        nhieu = _ba_nhieu9(
            dung,
            [r"$%d$" % _gia_tri(s, t0),                       # nham quang duong
             r"$%d$" % _gia_tri(_dao_ham(vt), t0),            # nham gia toc
             r"$%d$" % (_gia_tri(s, t0) // t0 if t0 else 0)],  # van toc trung binh
            buoc=lambda t: r"$%d$" % (k + t))
        debai = (r"Một chất điểm chuyển động thẳng có phương trình quãng "
                 r"đường $s(t) = %s$, trong đó $s$ tính bằng mét và $t$ "
                 r"tính bằng giây. Tính vận tốc tức thời của chất điểm tại "
                 r"thời điểm $t = %d$ giây (đơn vị: m/s)."
                 % (_da_thuc(s, "t"), t0))
        giai = (r"Vận tốc tức thời là đạo hàm của quãng đường theo thời "
                r"gian: $v(t) = s'(t)$."
                "\\\\\n"
                r"$v(t) = %s$." % _da_thuc(vt, "t") +
                "\\\\\n"
                r"$v\left(%d\right) = %d$ (m/s)." % (t0, k) +
                "\\\\\n"
                r"Chú ý phân biệt với $s\left(%d\right) = %d$ mét - đó là "
                r"QUÃNG ĐƯỜNG đi được, không phải vận tốc."
                % (t0, _gia_tri(s, t0)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B32_VD145_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán vận tốc tức thời.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_chuyen_dong()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, t0 in gt:
        s = [a, b, c, 0]
        vt = _dao_ham(s)
        debai = (r"Một chất điểm chuyển động thẳng có phương trình quãng "
                 r"đường $s(t) = %s$ ($s$ tính bằng mét, $t$ tính bằng "
                 r"giây)." % _da_thuc(s, "t"))

        hoi_a = r"Viết công thức vận tốc tức thời $v(t)$."
        giai_a = (r"$v(t) = s'(t) = %s$ (m/s)." % _da_thuc(vt, "t"))

        hoi_b = (r"Tính quãng đường đi được và vận tốc tức thời tại thời "
                 r"điểm $t = %d$ giây." % t0)
        giai_b = (r"$s\left(%d\right) = %d$ (m) và "
                  r"$v\left(%d\right) = %d$ (m/s)."
                  % (t0, _gia_tri(s, t0), t0, _gia_tri(vt, t0)))

        t1 = t0 + 2
        hoi_c = (r"Tính vận tốc trung bình trên đoạn từ $t = %d$ đến "
                 r"$t = %d$ giây và so sánh với $v\left(%d\right)$."
                 % (t0, t1, t0))
        tb = (_gia_tri(s, t1) - _gia_tri(s, t0)) / float(t1 - t0)
        giai_c = (r"$v_{tb} = \dfrac{s\left(%d\right) - s\left(%d\right)}"
                  r"{%d - %d} = \dfrac{%d - %d}{%d} = %s$ (m/s)."
                  % (t1, t0, t1, t0, _gia_tri(s, t1), _gia_tri(s, t0),
                     t1 - t0, _xx(tb)) +
                  "\\\\\n"
                  r"Vận tốc trung bình tính trên CẢ ĐOẠN, còn "
                  r"$v\left(%d\right) = %d$ (m/s) là vận tốc tại ĐÚNG một "
                  r"thời điểm; nói chung hai số này khác nhau."
                  % (t0, _gia_tri(vt, t0)))

        ds_abcd = [(hoi_a, r"v(t) = %s" % _da_thuc(vt, "t"), giai_a),
                   (hoi_b, r"s\left(%d\right) = %d,\ v\left(%d\right) = %d"
                    % (t0, _gia_tri(s, t0), t0, _gia_tri(vt, t0)), giai_b),
                   (hoi_c, r"v_{tb} = %s" % _xx(tb), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 33. ĐẠO HÀM CẤP HAI
# =====================================================================

def L11_C9_B33_NB146_MC_A_01(socau, dang=1):
    r"""Đạo hàm cấp hai của một hàm số - định nghĩa.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = tuple(_bo_da_thuc(3))
        if hs not in gt:
            gt.append(hs)

    cauTN = ""
    for hs in gt:
        hs = list(hs)
        d1 = _dao_ham(hs)
        d2 = _dao_ham(d1)
        dung = r"$%s$" % _da_thuc(d2)
        nhieu = _ba_nhieu9(
            dung,
            [r"$%s$" % _da_thuc(d1), r"$%s$" % _da_thuc(hs),
             r"$%s$" % _da_thuc(_dao_ham(d2))],
            buoc=lambda t: r"$%s$" % _da_thuc([d2[0] + t] + d2[1:]))
        debai = (r"Cho hàm số $y = f(x) = %s$. Tính đạo hàm cấp hai "
                 r"$f''(x)$." % _da_thuc(hs))
        giai = (r"Đạo hàm cấp hai là đạo hàm CỦA đạo hàm cấp một."
                "\\\\\n"
                r"$f'(x) = %s$." % _da_thuc(d1) +
                "\\\\\n"
                r"$f''(x) = \left[f'(x)\right]' = %s$." % _da_thuc(d2))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B33_TH147_MC_A_01(socau, dang=1):
    r"""Đạo hàm cấp hai tại một điểm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = tuple(_bo_da_thuc(random.choice([3, 4])))
        x0 = random.randint(-3, 3)
        if (hs, x0) not in gt:
            gt.append((hs, x0))

    cauTN = ""
    for hs, x0 in gt:
        hs = list(hs)
        d1 = _dao_ham(hs)
        d2 = _dao_ham(d1)
        k = _gia_tri(d2, x0)
        dung = r"$%d$" % k
        nhieu = _ba_nhieu9(
            dung,
            [r"$%d$" % _gia_tri(d1, x0), r"$%d$" % _gia_tri(hs, x0),
             r"$%d$" % (-k)],
            buoc=lambda t: r"$%d$" % (k + t))
        debai = (r"Cho hàm số $y = f(x) = %s$. Tính $f''\left(%d\right)$."
                 % (_da_thuc(hs), x0))
        giai = (r"$f'(x) = %s$." % _da_thuc(d1) +
                "\\\\\n"
                r"$f''(x) = %s$." % _da_thuc(d2) +
                "\\\\\n"
                r"$f''\left(%d\right) = %d$." % (x0, k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B33_TH147_SA_A_01(socau):
    r"""Đạo hàm cấp hai tại một điểm - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = tuple(_bo_da_thuc(random.choice([3, 4])))
        x0 = random.randint(-3, 3)
        if (hs, x0) not in gt:
            gt.append((hs, x0))

    cau = ""
    for hs, x0 in gt:
        hs = list(hs)
        d1 = _dao_ham(hs)
        d2 = _dao_ham(d1)
        k = _gia_tri(d2, x0)
        debai = (r"Cho hàm số $y = f(x) = %s$. Tính $f''\left(%d\right)$."
                 % (_da_thuc(hs), x0))
        giai = (r"$f'(x) = %s$; $f''(x) = %s$."
                % (_da_thuc(d1), _da_thuc(d2)) +
                "\\\\\n"
                r"$f''\left(%d\right) = %d$." % (x0, k))
        nhieu = _ba_nhieu9(str(k), [str(_gia_tri(d1, x0)),
                                    str(_gia_tri(hs, x0)), str(-k)],
                           buoc=lambda t: str(k + t + 1))
        cau += MC_SA_answer_const(debai, str(k), nhieu, giai, 0, 0, 2)
    return cau


def L11_C9_B33_VD148_MC_A_01(socau, dang=1):
    r"""Gia tốc tức thời - bài toán liên môn Vật lí.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_chuyen_dong()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, t0 in gt:
        s = [a, b, c, 0]
        vt = _dao_ham(s)
        gt_a = _dao_ham(vt)
        k = _gia_tri(gt_a, t0)
        dung = r"$%d$" % k
        nhieu = _ba_nhieu9(
            dung,
            [r"$%d$" % _gia_tri(vt, t0), r"$%d$" % _gia_tri(s, t0),
             r"$%d$" % (-k)],
            buoc=lambda t: r"$%d$" % (k + t))
        debai = (r"Một chất điểm chuyển động thẳng có phương trình quãng "
                 r"đường $s(t) = %s$ ($s$ tính bằng mét, $t$ tính bằng "
                 r"giây). Tính gia tốc tức thời của chất điểm tại thời "
                 r"điểm $t = %d$ giây (đơn vị: m/s$^2$)."
                 % (_da_thuc(s, "t"), t0))
        giai = (r"Gia tốc tức thời là đạo hàm CẤP HAI của quãng đường: "
                r"$a(t) = s''(t)$."
                "\\\\\n"
                r"$v(t) = s'(t) = %s$." % _da_thuc(vt, "t") +
                "\\\\\n"
                r"$a(t) = v'(t) = %s$." % _da_thuc(gt_a, "t") +
                "\\\\\n"
                r"$a\left(%d\right) = %d$ (m/s$^2$)." % (t0, k) +
                "\\\\\n"
                r"Chú ý phân biệt: $v\left(%d\right) = %d$ m/s là VẬN TỐC, "
                r"còn gia tốc là đạo hàm của vận tốc."
                % (t0, _gia_tri(vt, t0)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C9_B33_VD148_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán gia tốc của chuyển động.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_chuyen_dong()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, t0 in gt:
        s = [a, b, c, 0]
        vt = _dao_ham(s)
        ga = _dao_ham(vt)
        debai = (r"Một chất điểm chuyển động thẳng có phương trình quãng "
                 r"đường $s(t) = %s$ ($s$ tính bằng mét, $t$ tính bằng "
                 r"giây)." % _da_thuc(s, "t"))

        hoi_a = r"Viết công thức vận tốc $v(t)$ và gia tốc $a(t)$."
        giai_a = (r"$v(t) = s'(t) = %s$ (m/s)." % _da_thuc(vt, "t") +
                  "\\\\\n"
                  r"$a(t) = v'(t) = s''(t) = %s$ (m/s$^2$)."
                  % _da_thuc(ga, "t"))

        hoi_b = r"Tính $v\left(%d\right)$ và $a\left(%d\right)$." % (t0, t0)
        giai_b = (r"$v\left(%d\right) = %d$ (m/s) và "
                  r"$a\left(%d\right) = %d$ (m/s$^2$)."
                  % (t0, _gia_tri(vt, t0), t0, _gia_tri(ga, t0)))

        # a(t) = 6at + 2b = 0  ->  t = -b/(3a)
        hoi_c = (r"Tìm thời điểm $t > 0$ mà gia tốc của chất điểm bằng $0$ "
                 r"(nếu có).")
        if b < 0 and (-b) % (3 * a) == 0:
            t_star = (-b) // (3 * a)
            dap_c = r"t = %d" % t_star
            giai_c = (r"$a(t) = %s = 0$" % _da_thuc(ga, "t") +
                      "\\\\\n"
                      r"$\Leftrightarrow %dt = %d \Leftrightarrow t = %d$ "
                      r"(giây)." % (6 * a, -2 * b, t_star))
        else:
            t_star = -b / float(3 * a)
            if t_star > 0:
                dap_c = r"t = %s" % _xx(t_star)
                giai_c = (r"$a(t) = %s = 0 \Leftrightarrow t = %s$ (giây)."
                          % (_da_thuc(ga, "t"), _xx(t_star)))
            else:
                dap_c = r"\text{Không có } t > 0"
                giai_c = (r"$a(t) = %s = 0 \Leftrightarrow t = %s \le 0$."
                          % (_da_thuc(ga, "t"), _xx(t_star)) +
                          "\\\\\n"
                          r"Vậy không có thời điểm dương nào mà gia tốc "
                          r"bằng $0$: gia tốc luôn dương với mọi $t > 0$.")

        ds_abcd = [(hoi_a, r"v(t) = %s;\ a(t) = %s"
                    % (_da_thuc(vt, "t"), _da_thuc(ga, "t")), giai_a),
                   (hoi_b, r"v\left(%d\right) = %d;\ a\left(%d\right) = %d"
                    % (t0, _gia_tri(vt, t0), t0, _gia_tri(ga, t0)), giai_b),
                   (hoi_c, dap_c, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 9
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C9_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - định nghĩa, ý nghĩa của đạo hàm và các quy tắc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        hs = tuple(_bo_da_thuc(3))
        x0 = _diem_dep(list(hs))
        if (hs, x0) not in gt:
            gt.append((hs, x0))

    cauTF = ""
    for hs, x0 in gt:
        hs = list(hs)
        d1 = _dao_ham(hs)
        y0 = _gia_tri(hs, x0)
        k = _gia_tri(d1, x0)
        b = y0 - k * x0
        debai = (r"Cho hàm số $y = f(x) = %s$ có đồ thị $\left(C\right)$."
                 % _da_thuc(hs))

        ds_abcd = (
            # a) NB - nhắc lại một công thức đạo hàm
            [
                (r"{\True $f'(x) = %s$}" % _da_thuc(d1),
                 r"Đúng. Áp dụng $\left(x^{n}\right)' = nx^{\,n-1}$ cho "
                 r"từng hạng tử được $f'(x) = %s$." % _da_thuc(d1)),
                (r"{$f'(x) = %s$}" % _da_thuc(_dao_ham(d1)),
                 r"Sai. Đó là đạo hàm CẤP HAI. Đạo hàm cấp một là "
                 r"$f'(x) = %s$." % _da_thuc(d1)),
            ],
            # b) TH - thay số vào đạo hàm
            [
                (r"{\True $f'\left(%d\right) = %d$}" % (x0, k),
                 r"Đúng. Thay $x = %d$ vào $f'(x) = %s$ được $%d$."
                 % (x0, _da_thuc(d1), k)),
                (r"{$f'\left(%d\right) = %d$}" % (x0, y0),
                 r"Sai. $%d$ là $f\left(%d\right)$ - GIÁ TRỊ của hàm số, "
                 r"không phải đạo hàm; $f'\left(%d\right) = %d$."
                 % (y0, x0, x0, k)),
            ],
            # c) VD - phải dùng cả f và f' mới viết được tiếp tuyến
            [
                (r"{\True Tiếp tuyến của $\left(C\right)$ tại điểm có hoành "
                 r"độ $x_0 = %d$ có phương trình $y = %s$}"
                 % (x0, _da_thuc([k, b])),
                 r"Đúng. Tiếp điểm là $M\left(%d;\ %d\right)$, hệ số góc "
                 r"$k = f'\left(%d\right) = %d$." % (x0, y0, x0, k) +
                 "\\\\\n"
                 r"$y = %d\left(x %s\right) %s = %s$."
                 % (k, _dau(-x0), _dau(y0), _da_thuc([k, b]))),
                (r"{Tiếp tuyến của $\left(C\right)$ tại điểm có hoành độ "
                 r"$x_0 = %d$ có phương trình $y = %s$}"
                 % (x0, _da_thuc([k, y0])),
                 r"Sai. Thiếu bước trừ $x_0$: phải viết "
                 r"$y = f'\left(x_0\right)\left(x - x_0\right) + y_0$, kết "
                 r"quả đúng là $y = %s$." % _da_thuc([k, b])),
            ],
            # d) VDC - phải tự nhận ra đạo hàm của tích không phải tích đạo hàm
            [
                (r"{\True Với hai hàm số $u(x)$, $v(x)$ có đạo hàm thì "
                 r"$\left(uv\right)' = u'v + uv'$}",
                 r"Đúng. Đó là quy tắc đạo hàm của một tích."
                 "\\\\\n"
                 r"Thử lại với $u = x$ và $v = x$: vế trái "
                 r"$\left(x^{2}\right)' = 2x$; vế phải "
                 r"$1\cdot x + x\cdot 1 = 2x$ - khớp."),
                (r"{Với hai hàm số $u(x)$, $v(x)$ có đạo hàm thì "
                 r"$\left(uv\right)' = u'v'$}",
                 r"Sai. Thử với $u = x$, $v = x$: vế trái "
                 r"$\left(x^{2}\right)' = 2x$ nhưng vế phải "
                 r"$1\cdot 1 = 1$ - khác nhau."
                 "\\\\\n"
                 r"Công thức đúng là $\left(uv\right)' = u'v + uv'$."),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L11_C9_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - đạo hàm cấp hai và ý nghĩa cơ học.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_chuyen_dong()
        if v not in gt:
            gt.append(v)

    cauTF = ""
    for a, b, c, t0 in gt:
        s = [a, b, c, 0]
        vt = _dao_ham(s)
        ga = _dao_ham(vt)
        debai = (r"Một chất điểm chuyển động thẳng có phương trình quãng "
                 r"đường $s(t) = %s$ ($s$ tính bằng mét, $t$ tính bằng "
                 r"giây)." % _da_thuc(s, "t"))

        ds_abcd = (
            # a) NB - nhắc lại ý nghĩa cơ học
            [
                (r"{\True Vận tốc tức thời của chất điểm là "
                 r"$v(t) = s'(t)$}",
                 r"Đúng. Đạo hàm cấp một của quãng đường theo thời gian "
                 r"chính là vận tốc tức thời."),
                (r"{Vận tốc tức thời của chất điểm là $v(t) = s''(t)$}",
                 r"Sai. $s''(t)$ là GIA TỐC. Vận tốc là đạo hàm CẤP MỘT: "
                 r"$v(t) = s'(t)$."),
            ],
            # b) TH - một lần lấy đạo hàm
            [
                (r"{\True $v(t) = %s$}" % _da_thuc(vt, "t"),
                 r"Đúng. $v(t) = s'(t) = %s$." % _da_thuc(vt, "t")),
                (r"{$v(t) = %s$}" % _da_thuc(ga, "t"),
                 r"Sai. Đó là $s''(t)$, tức gia tốc. Vận tốc là "
                 r"$v(t) = %s$." % _da_thuc(vt, "t")),
            ],
            # c) VD - lấy đạo hàm hai lần rồi thay số
            [
                (r"{\True Gia tốc của chất điểm tại thời điểm $t = %d$ "
                 r"giây bằng $%d$ m/s$^2$}" % (t0, _gia_tri(ga, t0)),
                 r"Đúng. $a(t) = s''(t) = %s$." % _da_thuc(ga, "t") +
                 "\\\\\n"
                 r"$a\left(%d\right) = %d$ (m/s$^2$)."
                 % (t0, _gia_tri(ga, t0))),
                (r"{Gia tốc của chất điểm tại thời điểm $t = %d$ giây bằng "
                 r"$%d$ m/s$^2$}" % (t0, _gia_tri(vt, t0)),
                 r"Sai. $%d$ là VẬN TỐC tại thời điểm đó. Gia tốc là "
                 r"$a\left(%d\right) = %d$ (m/s$^2$)."
                 % (_gia_tri(vt, t0), t0, _gia_tri(ga, t0))),
            ],
            # d) VDC - phải tự xét dấu gia tốc trên cả nửa trục
            [
                (r"{\True Gia tốc của chất điểm là một hàm bậc nhất theo "
                 r"$t$, nên nó tăng đều theo thời gian}",
                 r"Đúng. $a(t) = %s$ có dạng bậc nhất theo $t$ với hệ số "
                 r"góc $%d > 0$, nên gia tốc tăng đều."
                 % (_da_thuc(ga, "t"), 6 * a) +
                 "\\\\\n"
                 r"Nói cách khác, mỗi giây trôi qua thì gia tốc tăng thêm "
                 r"đúng $%d$ m/s$^2$." % (6 * a)),
                (r"{Gia tốc của chất điểm không đổi theo thời gian}",
                 r"Sai. $a(t) = %s$ CÓ chứa $t$ nên gia tốc thay đổi."
                 % _da_thuc(ga, "t") +
                 "\\\\\n"
                 r"Gia tốc chỉ không đổi khi $s(t)$ là đa thức bậc không "
                 r"quá hai."),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
