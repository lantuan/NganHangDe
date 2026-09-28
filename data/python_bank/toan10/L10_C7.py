# ==========================================================
# CHƯƠNG 7 (lớp 10): PHƯƠNG PHÁP TOẠ ĐỘ TRONG MẶT PHẲNG
#   Bài 19. Phương trình đường thẳng
#   Bài 20. Vị trí tương đối giữa hai đường thẳng. Góc và khoảng cách
#   Bài 21. Đường tròn trong mặt phẳng toạ độ
#   Bài 22. Ba đường conic
#
# VIẾT MỚI HOÀN TOÀN. Tệp "LopXChuong7.py" cô Lan gửi (cả hai lần) đều
# là nội dung CHƯƠNG 9 (xác suất, toàn hàm K10_9_*), không phải chương 7,
# nên không có gì để chuyển. math_type.py GIỮ NGUYÊN, không sửa dòng nào.
#
# Số liệu được chọn để đáp số ra ĐẸP:
#   - khoảng cách từ điểm đến đường thẳng: vectơ pháp tuyến lấy từ bộ ba
#     Pytago nên mẫu $\sqrt{a^2+b^2}$ là số nguyên;
#   - góc giữa hai đường thẳng: chỉ dùng các cặp cho góc 0, 45, 90 độ -
#     với vectơ pháp tuyến NGUYÊN thì góc 30 và 60 độ không dựng được
#     (cần $b^2 = 3a^2$, vô nghiệm nguyên);
#   - đường tròn: tâm nguyên, bán kính nguyên.
# ==========================================================
import math
import random
from fractions import Fraction

from math_type import *

DAU_THAP_PHAN = ","


def _xx7(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết theo cách viết Việt Nam."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _toa7(x):
    """Số dùng LÀM TOẠ ĐỘ TikZ - luôn dấu CHẤM, không phải dấu phẩy."""
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _ba_nhieu7(dapso, ung_vien, buoc=None):
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


def _chon_chi_muc7(n, socau):
    r"""Chọn socau chỉ mục trong 0..n-1, KHÔNG trùng nhau chừng nào còn
    đủ; hết mẫu thì quay vòng (tránh vòng lặp vô hạn khi socau > n)."""
    ds = []
    while len(ds) < socau:
        thieu = socau - len(ds)
        ds += random.sample(range(n), min(n, thieu))
    return ds


def _pt_duong_thang(a, b, c):
    r"""Viết $ax + by + c = 0$ thành LaTeX gọn."""
    phan = []
    if a:
        phan.append("x" if a == 1 else ("-x" if a == -1 else "%dx" % a))
    if b:
        if not phan:
            phan.append("y" if b == 1 else ("-y" if b == -1 else "%dy" % b))
        elif b == 1:
            phan.append("+ y")
        elif b == -1:
            phan.append("- y")
        elif b > 0:
            phan.append("+ %dy" % b)
        else:
            phan.append("- %dy" % (-b))
    if c:
        if not phan:
            phan.append("%d" % c)
        else:
            phan.append(("+ %d" % c) if c > 0 else ("- %d" % (-c)))
    if not phan:
        phan.append("0")
    return " ".join(phan) + " = 0"


def _toado7(x, y):
    return r"\left(%s;\ %s\right)" % (_xx7(x), _xx7(y))


def _pt_tham_so(px, py, vx, vy):
    r"""Viết hệ phương trình tham số, bỏ hệ số 1 và bỏ hạng tử 0."""
    def _dong(ten, hang, he_so):
        if he_so == 0:
            return r"%s = %d" % (ten, hang)
        if he_so == 1:
            duoi = "t"
        elif he_so == -1:
            duoi = "-t"
        else:
            duoi = "%dt" % he_so
        if hang == 0:
            return r"%s = %s" % (ten, duoi)
        return r"%s = %d %s %st" % (ten, hang, "+" if he_so > 0 else "-",
                                    "" if abs(he_so) == 1
                                    else "%d" % abs(he_so))
    return (r"$\begin{cases} %s \\ %s \end{cases}$"
            % (_dong("x", px, vx), _dong("y", py, vy)))


def _tong7(u, v):
    r"""Viết $u + v$ cho đúng dấu: $-4 + (-2)$ phải thành $-4 - 2$."""
    return r"%d %s %d" % (u, "+" if v >= 0 else "-", abs(v))


def _ngoac7(ten, t):
    r"""Viết $\left(x - t\right)$; nếu $t = 0$ thì chỉ còn $x$."""
    if t == 0:
        return ten
    return r"\left(%s %s %d\right)" % (ten, "-" if t > 0 else "+", abs(t))


def _khai_trien7(a, b, x0, y0):
    r"""Viết $a\left(x-x_0\right) + b\left(y-y_0\right) = 0$ cho đúng dấu,
    bỏ hệ số 1 và bỏ hẳn hạng tử có hệ số 0."""
    phan = []
    if a:
        he = "" if a == 1 else ("-" if a == -1 else "%d" % a)
        phan.append(he + _ngoac7("x", x0))
    if b:
        he = "" if abs(b) == 1 else "%d" % abs(b)
        cum = he + _ngoac7("y", y0)
        phan.append(cum if not phan else
                    ("+ " if b > 0 else "- ") + cum)
        if len(phan) == 1 and b < 0:
            phan[0] = "-" + phan[0]
    return " ".join(phan) + " = 0"


def _don_thuc7(k, bien, dau_dau=True):
    r"""Viết hạng tử $k\cdot\text{bien}$: bỏ hệ số 1, bỏ hẳn khi $k = 0$.

    dau_dau=True: đứng đầu biểu thức (dấu cộng thì không viết).
    """
    if k == 0:
        return ""
    he = "" if abs(k) == 1 else "%d" % abs(k)
    if dau_dau:
        return ("-" if k < 0 else "") + he + bien
    return ("+ " if k > 0 else "- ") + he + bien


def _so7(t):
    r"""Số âm phải đóng ngoặc: $\left(-4\right)^2$ chứ không phải $-4^2$."""
    return "%d" % t if t >= 0 else r"\left(%d\right)" % t


def _can7(n):
    r"""Viết $\sqrt{n}$, rút thành số nguyên khi $n$ là số chính phương."""
    g = int(round(math.sqrt(n)))
    return "%d" % g if g * g == n else r"\sqrt{%d}" % n


def _tich7(u, v):
    r"""Viết $u\cdot v$, đóng ngoặc số âm: $0\cdot\left(-1\right)$."""
    def _so(t):
        return "%d" % t if t >= 0 else r"\left(%d\right)" % t
    return r"%s\cdot %s" % (_so(u), _so(v))


def _cong_tich7(k, t):
    r"""Viết hạng tử cộng thêm $k\cdot t$ cho đúng dấu:
    $3\cdot\left(-4\right) - 2\cdot\left(-1\right)$, không để "+ -2"."""
    return "%s %s" % ("+" if k >= 0 else "-", _tich7(abs(k), t))


def _rut_gon7(a, b, c):
    r"""Chia cả phương trình cho ước chung và chuẩn hoá dấu hệ số đầu."""
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c


# Bộ ba Pytago dùng làm vectơ pháp tuyến để mẫu căn ra SỐ NGUYÊN.
PYTAGO7 = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10),
           (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17)]


# =====================================================================
# BÀI 19. PHƯƠNG TRÌNH ĐƯỜNG THẲNG
# =====================================================================

def L10_C7_B19_NB106_MC_A_01(socau, dang=1):
    r"""Nhận ra phương trình tổng quát của đường thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-9, 9)
        # cả hai hệ số đều khác 0 thì phương án nhiễu không còn hạng tử "0y"
        if a == 0 or b == 0:
            continue
        if (a, b, c) not in gt:
            gt.append((a, b, c))

    cauTN = ""
    for a, b, c in gt:
        dung = r"$%s$" % _pt_duong_thang(a, b, c)
        nhieu = [r"$x^2 %s %dy %s %d = 0$"
                 % ("+" if b >= 0 else "-", abs(b),
                    "+" if c >= 0 else "-", abs(c)),
                 r"$\dfrac{%d}{x} %s %dy %s %d = 0$"
                 % (a if a else 1, "+" if b >= 0 else "-", abs(b),
                    "+" if c >= 0 else "-", abs(c)),
                 r"$%dxy %s %d = 0$" % (a if a else 1,
                                        "+" if c >= 0 else "-", abs(c)),
                 r"$%dx^2 %s %dy^2 = %d$" % (a if a else 1,
                                             "+" if b >= 0 else "-", abs(b),
                                             abs(c) + 1)]
        debai = (r"Trong các phương trình sau, phương trình nào là "
                 r"\textbf{phương trình tổng quát} của một đường thẳng?")
        giai = (r"Phương trình tổng quát của đường thẳng có dạng "
                r"$ax + by + c = 0$ với $a^2 + b^2 \ne 0$ - nghĩa là $x$ và "
                r"$y$ đều ở \textbf{bậc nhất}, không có $x^2$, $y^2$, $xy$ "
                r"hay $x$ ở mẫu."
                "\\\\\n"
                r"Chỉ $%s$ có đúng dạng ấy, với $a = %d$, $b = %d$, "
                r"$c = %d$." % (_pt_duong_thang(a, b, c), a, b, c))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B19_NB106_MC_B_01(socau, dang=1):
    r"""Nhận ra phương trình tham số của đường thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        u1 = random.randint(-4, 4)
        u2 = random.randint(-4, 4)
        # chặn các trường hợp làm bốn phương án trùng nhau
        if u1 == 0 and u2 == 0:
            continue
        if u1 == u2 or (x0, y0) == (0, 0) or (x0, y0) == (u1, u2):
            continue
        if math.gcd(abs(u1), abs(u2)) != 1:
            continue
        if (x0, y0, u1, u2) not in gt:
            gt.append((x0, y0, u1, u2))

    cauTN = ""
    for x0, y0, u1, u2 in gt:
        dung = _pt_tham_so(x0, y0, u1, u2)
        nhieu = _ba_nhieu7(
            dung,
            [_pt_tham_so(u1, u2, x0, y0), _pt_tham_so(x0, y0, u2, u1),
             _pt_tham_so(-x0, -y0, u1, u2), _pt_tham_so(x0, y0, -u1, -u2)],
            buoc=lambda t: _pt_tham_so(x0 + t, y0, u1, u2))
        debai = (r"Đường thẳng $d$ đi qua điểm $M%s$ và có vectơ chỉ phương "
                 r"$\overrightarrow{u} = %s$. Phương trình tham số của $d$ là"
                 % (_toado7(x0, y0), _toado7(u1, u2)))
        giai = (r"Đường thẳng đi qua $M\left(x_0;\ y_0\right)$ với vectơ chỉ "
                r"phương $\overrightarrow{u} = \left(u_1;\ u_2\right)$ có "
                r"phương trình tham số"
                "\\\\\n"
                r"$\begin{cases} x = x_0 + u_1t \\ y = y_0 + u_2t "
                r"\end{cases}$"
                "\\\\\n"
                r"Thay $x_0 = %d$, $y_0 = %d$, $u_1 = %d$, $u_2 = %d$ được "
                r"kết quả." % (x0, y0, u1, u2) +
                "\\\\\n"
                r"Chú ý \textbf{toạ độ điểm} đứng ở phần hằng số, còn "
                r"\textbf{toạ độ vectơ} đi kèm tham số $t$ - đổi chỗ hai thứ "
                r"này là sai.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B19_TH107_MC_A_01(socau, dang=1):
    r"""Lập phương trình đường thẳng qua một điểm và có vectơ pháp tuyến.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        # hai toạ độ khác 0 và nguyên tố cùng nhau => phương trình đã gọn
        if a == 0 or b == 0 or math.gcd(abs(a), abs(b)) != 1:
            continue
        if (x0, y0, a, b) not in gt:
            gt.append((x0, y0, a, b))

    cauTN = ""
    for x0, y0, a, b in gt:
        c = -(a * x0 + b * y0)
        dung = r"$%s$" % _pt_duong_thang(a, b, c)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_thang(a, b, -c),
             r"$%s$" % _pt_duong_thang(b, a, c),
             r"$%s$" % _pt_duong_thang(-b, a, c),
             r"$%s$" % _pt_duong_thang(a, b, c + 1)],
            buoc=lambda t: r"$%s$" % _pt_duong_thang(a, b, c + 1 + t))
        debai = (r"Lập phương trình tổng quát của đường thẳng $d$ đi qua "
                 r"điểm $M%s$ và có vectơ pháp tuyến "
                 r"$\overrightarrow{n} = %s$."
                 % (_toado7(x0, y0), _toado7(a, b)))
        giai = (r"Đường thẳng qua $M\left(x_0;\ y_0\right)$ với vectơ pháp "
                r"tuyến $\overrightarrow{n} = \left(a;\ b\right)$ có phương "
                r"trình"
                "\\\\\n"
                r"$a\left(x - x_0\right) + b\left(y - y_0\right) = 0$."
                "\\\\\n"
                r"$%s$" % _khai_trien7(a, b, x0, y0) +
                "\\\\\n"
                r"Khai triển và thu gọn: $%s$." % _pt_duong_thang(a, b, c) +
                "\\\\\n"
                r"Kiểm lại: thay $M%s$ vào vế trái được "
                r"$%s + %s %s %d = 0$."
                % (_toado7(x0, y0), _tich7(a, x0), _tich7(b, y0),
                   "+" if c >= 0 else "-", abs(c)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B19_TH107_MC_B_01(socau, dang=1):
    r"""Lập phương trình đường thẳng đi qua hai điểm.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa = random.randint(-5, 5)
        ya = random.randint(-5, 5)
        xb = random.randint(-5, 5)
        yb = random.randint(-5, 5)
        if (xa, ya) == (xb, yb):
            continue
        if (xa, ya, xb, yb) not in gt:
            gt.append((xa, ya, xb, yb))

    cauTN = ""
    for xa, ya, xb, yb in gt:
        u1, u2 = xb - xa, yb - ya      # vectơ chỉ phương
        a, b = u2, -u1                  # vectơ pháp tuyến
        g = math.gcd(math.gcd(abs(a), abs(b)),
                     abs(a * xa + b * ya)) or 1
        c = -(a * xa + b * ya)
        dung = r"$%s$" % _pt_duong_thang(a, b, c)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_thang(u1, u2, -(u1 * xa + u2 * ya)),
             r"$%s$" % _pt_duong_thang(a, b, -c),
             r"$%s$" % _pt_duong_thang(-a, b, c),
             r"$%s$" % _pt_duong_thang(a, b, c + 2)],
            buoc=lambda t: r"$%s$" % _pt_duong_thang(a, b, c + 2 + t))
        debai = (r"Lập phương trình tổng quát của đường thẳng đi qua hai "
                 r"điểm $A%s$ và $B%s$."
                 % (_toado7(xa, ya), _toado7(xb, yb)))
        giai = (r"Vectơ chỉ phương: $\overrightarrow{AB} = %s$."
                % _toado7(u1, u2) +
                "\\\\\n"
                r"Vectơ pháp tuyến vuông góc với $\overrightarrow{AB}$ nên "
                r"lấy $\overrightarrow{n} = %s$ (đổi chỗ hai toạ độ rồi đổi "
                r"dấu một toạ độ)." % _toado7(a, b) +
                "\\\\\n"
                r"Đường thẳng qua $A%s$ với pháp tuyến $%s$:"
                % (_toado7(xa, ya), _toado7(a, b)) +
                "\\\\\n"
                r"$%s \Leftrightarrow %s$."
                % (_khai_trien7(a, b, xa, ya),
                   _pt_duong_thang(a, b, c)) +
                "\\\\\n"
                r"Kiểm lại: cả $A$ và $B$ đều thoả mãn phương trình này.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B19_TH107_SA_A_01(socau):
    r"""Hệ số trong phương trình đường thẳng - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa = random.randint(-5, 5)
        ya = random.randint(-5, 5)
        xb = random.randint(-5, 5)
        yb = random.randint(-5, 5)
        if (xa, ya) == (xb, yb) or yb == ya:
            continue
        if (xa, ya, xb, yb) not in gt:
            gt.append((xa, ya, xb, yb))

    cau = ""
    for xa, ya, xb, yb in gt:
        u1, u2 = xb - xa, yb - ya
        a, b = u2, -u1
        c = -(a * xa + b * ya)
        debai = (r"Đường thẳng đi qua hai điểm $A%s$ và $B%s$ có phương "
                 r"trình tổng quát dạng $%dx + by + c = 0$. Tìm $b$."
                 % (_toado7(xa, ya), _toado7(xb, yb), a))
        giai = (r"$\overrightarrow{AB} = %s$ nên vectơ pháp tuyến là "
                r"$\overrightarrow{n} = %s$." % (_toado7(u1, u2),
                                                 _toado7(a, b)) +
                "\\\\\n"
                r"Phương trình tổng quát: $%s$." % _pt_duong_thang(a, b, c) +
                "\\\\\n"
                r"So với dạng $%dx + by + c = 0$ thì $b = %d$." % (a, b))
        nhieu = _ba_nhieu7(b, [a, -b, c, u2], buoc=lambda t: b + 2 * t)
        cau += MC_SA_answer_const(debai, b, nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B19_TH108_MC_A_01(socau, dang=1):
    r"""Liên hệ giữa đồ thị hàm số bậc nhất và đường thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([-3, -2, -1, 1, 2, 3])
        m = random.randint(-6, 6)
        if (k, m) not in gt:
            gt.append((k, m))

    cauTN = ""
    for k, m in gt:
        # y = kx + m  <=>  kx - y + m = 0
        dung = r"$%s$" % _pt_duong_thang(k, -1, m)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_thang(k, 1, m),
             r"$%s$" % _pt_duong_thang(k, -1, -m),
             r"$%s$" % _pt_duong_thang(1, -k, m),
             r"$%s$" % _pt_duong_thang(-k, -1, m)],
            buoc=lambda t: r"$%s$" % _pt_duong_thang(k, -1, m + t))
        debai = (r"Đồ thị của hàm số bậc nhất $y = %dx %s %d$ là một đường "
                 r"thẳng. Phương trình tổng quát của đường thẳng đó là"
                 % (k, "+" if m >= 0 else "-", abs(m)))
        giai = (r"Chuyển tất cả về một vế:"
                "\\\\\n"
                r"$y = %dx %s %d \Leftrightarrow %dx - y %s %d = 0$."
                % (k, "+" if m >= 0 else "-", abs(m),
                   k, "+" if m >= 0 else "-", abs(m)) +
                "\\\\\n"
                r"Vậy phương trình tổng quát là $%s$, với vectơ pháp tuyến "
                r"$\overrightarrow{n} = %s$."
                % (_pt_duong_thang(k, -1, m), _toado7(k, -1)) +
                "\\\\\n"
                r"Chú ý hệ số góc $k = %d$ chính là hệ số của $x$ trong dạng "
                r"$y = kx + m$, không phải hệ số của $y$." % k)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B19_VD107_MC_A_01(socau, dang=1):
    r"""Lập phương trình đường thẳng từ điều kiện không trực tiếp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đường trung trực của đoạn thẳng: phải tự tìm trung điểm rồi lấy
    $\overrightarrow{AB}$ làm pháp tuyến - không thay thẳng vào công
    thức nào được.
    """
    gt = []
    while len(gt) < socau:
        xa = random.randint(-5, 5)
        ya = random.randint(-5, 5)
        # chọn B sao cho trung điểm có toạ độ nguyên; (p, q) nguyên tố
        # cùng nhau để phương trình trung trực đã ở dạng gọn nhất
        p = random.randint(-3, 3)
        q = random.randint(-3, 3)
        if (p, q) == (0, 0) or math.gcd(abs(p), abs(q)) != 1:
            continue
        xb, yb = xa + 2 * p, ya + 2 * q
        if (xa, ya, xb, yb) not in gt:
            gt.append((xa, ya, xb, yb))

    cauTN = ""
    for xa, ya, xb, yb in gt:
        xm, ym = (xa + xb) // 2, (ya + yb) // 2
        ux, uy = xb - xa, yb - ya        # vectơ AB
        a, b = ux // 2, uy // 2          # pháp tuyến GỌN, cùng phương AB
        c = -(a * xm + b * ym)
        dung = r"$%s$" % _pt_duong_thang(a, b, c)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_thang(a, b, -(a * xa + b * ya)),
             r"$%s$" % _pt_duong_thang(-b, a, -(-b * xm + a * ym)),
             r"$%s$" % _pt_duong_thang(a, b, -c),
             r"$%s$" % _pt_duong_thang(a, b, c + 2)],
            buoc=lambda t: r"$%s$" % _pt_duong_thang(a, b, c + 2 + t))
        debai = (r"Lập phương trình đường trung trực của đoạn thẳng $AB$ với "
                 r"$A%s$ và $B%s$." % (_toado7(xa, ya), _toado7(xb, yb)))
        giai = (r"Đường trung trực của $AB$ đi qua \textbf{trung điểm} $M$ "
                r"của $AB$ và \textbf{vuông góc} với $AB$."
                "\\\\\n"
                r"Trung điểm: $M\left(\dfrac{%s}{2};\ "
                r"\dfrac{%s}{2}\right) = M%s$."
                % (_tong7(xa, xb), _tong7(ya, yb), _toado7(xm, ym)) +
                "\\\\\n"
                r"Vì trung trực vuông góc với $AB$ nên nhận "
                r"$\overrightarrow{AB} = %s$ làm \textbf{vectơ pháp "
                r"tuyến}; rút gọn lấy $\overrightarrow{n} = %s$ cùng phương."
                % (_toado7(ux, uy), _toado7(a, b)) +
                "\\\\\n"
                r"Phương trình: $%s \Leftrightarrow %s$."
                % (_khai_trien7(a, b, xm, ym),
                   _pt_duong_thang(a, b, c)) +
                "\\\\\n"
                r"Kiểm lại: $M$ thoả mãn phương trình, và $A$, $B$ cách đều "
                r"đường thẳng này.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B19_VD107_TL_A_01(socau, dong=1):
    r"""Tự luận: lập phương trình đường thẳng thoả điều kiện cho trước.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        xa = random.randint(-4, 4)
        ya = random.randint(-4, 4)
        xb = xa + 2 * random.randint(-3, 3)
        yb = ya + 2 * random.randint(-3, 3)
        if (xa, ya) == (xb, yb) or xa == xb:
            continue
        if (xa, ya, xb, yb) not in gt:
            gt.append((xa, ya, xb, yb))

    cauTN = ""
    for xa, ya, xb, yb in gt:
        u1, u2 = xb - xa, yb - ya
        a, b, c = _rut_gon7(u2, -u1, -(u2 * xa - u1 * ya))
        xm, ym = (xa + xb) // 2, (ya + yb) // 2
        a2, b2, c2 = _rut_gon7(u1, u2, -(u1 * xm + u2 * ym))

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai điểm $A%s$ và $B%s$."
                 % (_toado7(xa, ya), _toado7(xb, yb)))

        hoi_a = r"Lập phương trình tổng quát của đường thẳng $AB$."
        giai_a = (r"$\overrightarrow{AB} = %s$ là vectơ chỉ phương, nên một "
                  r"vectơ pháp tuyến là $%s$; rút gọn lấy "
                  r"$\overrightarrow{n} = %s$."
                  % (_toado7(u1, u2), _toado7(u2, -u1), _toado7(a, b)) +
                  "\\\\\n"
                  r"Đường thẳng qua $A%s$: $%s$."
                  % (_toado7(xa, ya), _pt_duong_thang(a, b, c)))

        hoi_b = r"Tìm toạ độ trung điểm $M$ của đoạn thẳng $AB$."
        giai_b = (r"$M\left(\dfrac{x_A + x_B}{2};\ "
                  r"\dfrac{y_A + y_B}{2}\right) = M%s$." % _toado7(xm, ym))

        hoi_c = r"Lập phương trình đường trung trực của đoạn thẳng $AB$."
        giai_c = (r"Đường trung trực đi qua $M%s$ và vuông góc với $AB$, nên "
                  r"nhận $\overrightarrow{AB} = %s$ làm vectơ pháp tuyến; "
                  r"rút gọn lấy $\overrightarrow{n} = %s$."
                  % (_toado7(xm, ym), _toado7(u1, u2), _toado7(a2, b2)) +
                  "\\\\\n"
                  r"$%s \Leftrightarrow %s$."
                  % (_khai_trien7(a2, b2, xm, ym),
                     _pt_duong_thang(a2, b2, c2)))

        ds_abcd = [(hoi_a, _pt_duong_thang(a, b, c), giai_a),
                   (hoi_b, r"M\left(%d;\ %d\right)" % (xm, ym), giai_b),
                   (hoi_c, _pt_duong_thang(a2, b2, c2), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 20. VỊ TRÍ TƯƠNG ĐỐI, GÓC VÀ KHOẢNG CÁCH
# =====================================================================

def L10_C7_B20_TH109_MC_A_01(socau, dang=1):
    r"""Xét vị trí tương đối của hai đường thẳng bằng toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    KIEU = ["cat", "song_song", "trung"]
    gt = []
    while len(gt) < socau:
        a1 = random.randint(-4, 4)
        b1 = random.randint(-4, 4)
        c1 = random.randint(-6, 6)
        # ba hệ số đều khác 0 thì mọi tỉ số trong lời giải đều có nghĩa
        if a1 == 0 or b1 == 0 or c1 == 0:
            continue
        kieu = random.choice(KIEU)
        k = random.choice([2, 3, -2])
        if kieu == "cat":
            a2, b2 = b1, a1 + 1
            if a1 * b2 - a2 * b1 == 0:
                continue
            # cắt nhau mà lại vuông góc thì câu có HAI đáp án đúng
            if a1 * a2 + b1 * b2 == 0:
                continue
            c2 = random.randint(-6, 6)
        elif kieu == "song_song":
            a2, b2 = k * a1, k * b1
            c2 = k * c1 + random.choice([1, 2, -1, -2])
        else:
            a2, b2, c2 = k * a1, k * b1, k * c1
        v = (a1, b1, c1, a2, b2, c2, kieu)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a1, b1, c1, a2, b2, c2, kieu in gt:
        ten = {"cat": "Cắt nhau", "song_song": "Song song",
               "trung": "Trùng nhau"}[kieu]
        dung = ten
        nhieu = [t for t in ("Cắt nhau", "Song song", "Trùng nhau",
                             "Vuông góc với nhau") if t != ten]
        dinh_thuc = a1 * b2 - a2 * b1
        debai = (r"Xét vị trí tương đối của hai đường thẳng "
                 r"$d_1: %s$ và $d_2: %s$."
                 % (_pt_duong_thang(a1, b1, c1), _pt_duong_thang(a2, b2, c2)))
        if kieu == "cat":
            ly_do = (r"$a_1b_2 - a_2b_1 = %s - %s = %d "
                     r"\ne 0$ nên hai vectơ pháp tuyến \textbf{không cùng "
                     r"phương}: hai đường thẳng cắt nhau."
                     % (_tich7(a1, b2), _tich7(a2, b1), dinh_thuc))
        elif kieu == "song_song":
            ly_do = (r"$\dfrac{%d}{%d} = \dfrac{%d}{%d}$ nhưng "
                     r"$\dfrac{%d}{%d}$ khác tỉ số đó, nên hai đường thẳng "
                     r"\textbf{song song}." % (a2, a1, b2, b1, c2, c1))
        else:
            ly_do = (r"$\dfrac{%d}{%d} = \dfrac{%d}{%d} = \dfrac{%d}{%d}$ "
                     r"nên hai phương trình \textbf{tỉ lệ} với nhau: đó là "
                     r"cùng một đường thẳng." % (a2, a1, b2, b1, c2, c1))
        giai = (r"So sánh hai bộ hệ số $\left(a_1;\ b_1;\ c_1\right)$ và "
                r"$\left(a_2;\ b_2;\ c_2\right)$."
                "\\\\\n" + ly_do)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B20_TH110_MC_A_01(socau, dang=1):
    r"""Tính khoảng cách từ một điểm đến một đường thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Vectơ pháp tuyến lấy từ bộ ba Pytago nên mẫu $\sqrt{a^2+b^2}$ là số
    nguyên, khoảng cách ra số thập phân hữu hạn.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice(PYTAGO7)
        if random.choice([True, False]):
            a = -a
        c = random.randint(-9, 9)
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        tu = abs(a * x0 + b * y0 + c)
        if tu == 0:
            continue
        v = (a, b, n, c, x0, y0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, n, c, x0, y0 in gt:
        tu = abs(a * x0 + b * y0 + c)
        d = tu / float(n)
        dung = r"$%s$" % _xx7(d)
        nhieu = [r"$%s$" % x for x in _ba_nhieu7(
            _xx7(d), [_xx7(tu), _xx7(tu / (n * n)), _xx7(d * n),
                      _xx7(a * x0 + b * y0 + c)],
            buoc=lambda t: _xx7(d + t / 2.0))]
        debai = (r"Tính khoảng cách từ điểm $M%s$ đến đường thẳng "
                 r"$\Delta: %s$." % (_toado7(x0, y0),
                                     _pt_duong_thang(a, b, c)))
        giai = (r"Công thức khoảng cách từ $M\left(x_0;\ y_0\right)$ đến "
                r"$\Delta: ax + by + c = 0$:"
                "\\\\\n"
                r"$d\left(M;\ \Delta\right) = "
                r"\dfrac{\left|ax_0 + by_0 + c\right|}{\sqrt{a^2 + b^2}}$."
                "\\\\\n"
                r"Tử số: $\left|%s + %s %s %d\right| "
                r"= \left|%d\right| = %d$."
                % (_tich7(a, x0), _tich7(b, y0),
                   "+" if c >= 0 else "-", abs(c),
                   a * x0 + b * y0 + c, tu) +
                "\\\\\n"
                r"Mẫu số: $\sqrt{%d^2 + %d^2} = \sqrt{%d} = %d$."
                % (a, b, a * a + b * b, n) +
                "\\\\\n"
                r"Vậy $d = \dfrac{%d}{%d} = %s$." % (tu, n, _xx7(d)) +
                "\\\\\n"
                r"Chú ý tử số có \textbf{dấu giá trị tuyệt đối} nên khoảng "
                r"cách luôn không âm.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B20_TH110_SA_A_01(socau):
    r"""Khoảng cách từ điểm đến đường thẳng - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice(PYTAGO7)
        if random.choice([True, False]):
            a = -a
        c = random.randint(-9, 9)
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        tu = abs(a * x0 + b * y0 + c)
        if tu == 0:
            continue
        d = tu / float(n)
        if abs(d * 100 - round(d * 100)) > 1e-9:
            continue
        v = (a, b, n, c, x0, y0)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, n, c, x0, y0 in gt:
        tu = abs(a * x0 + b * y0 + c)
        d = tu / float(n)
        debai = (r"Tính khoảng cách từ điểm $M%s$ đến đường thẳng "
                 r"$\Delta: %s$." % (_toado7(x0, y0),
                                     _pt_duong_thang(a, b, c)))
        giai = (r"$d = \dfrac{\left|%s + %s %s %d\right|}"
                r"{\sqrt{%s^2 + %s^2}} = \dfrac{%d}{%d} = %s$."
                % (_tich7(a, x0), _tich7(b, y0),
                   "+" if c >= 0 else "-", abs(c),
                   _so7(a), _so7(b), tu, n, _xx7(d)))
        nhieu = _ba_nhieu7(_xx7(d), [_xx7(tu), _xx7(tu / (n * n)),
                                     _xx7(d * n)],
                           buoc=lambda t: _xx7(d + t / 2.0))
        cau += MC_SA_answer_text(debai, _xx7(d), nhieu, giai, 0, 0, 2)
    return cau


# Các cặp vectơ pháp tuyến cho góc ĐẸP giữa hai đường thẳng.
# Với vectơ pháp tuyến NGUYÊN, góc 30 và 60 độ không dựng được
# (cần b^2 = 3a^2, vô nghiệm nguyên), nên chỉ dùng 0, 45, 90 độ.
# Giá trị cos CHÍNH XÁC của các góc dùng trong CAP_GOC7 (không dùng
# số thập phân gần đúng trong lời giải).
COS_GOC7 = {0: "1", 45: r"\dfrac{\sqrt{2}}{2}", 90: "0"}

CAP_GOC7 = [
    ((1, 0), (1, 1), 45), ((1, 0), (1, -1), 45),
    ((0, 1), (1, 1), 45), ((0, 1), (1, -1), 45),
    ((1, 2), (2, -1), 90), ((3, 4), (4, -3), 90),
    ((1, 0), (0, 1), 90), ((2, 3), (3, -2), 90),
    ((1, 2), (2, 4), 0), ((3, 1), (6, 2), 0),
]


def L10_C7_B20_TH111_MC_A_01(socau, dang=1):
    r"""Tính góc giữa hai đường thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(CAP_GOC7))
        c1 = random.randint(-6, 6)
        c2 = random.randint(-6, 6)
        v = (i, c1, c2)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for i, c1, c2 in gt:
        (a1, b1), (a2, b2), goc = CAP_GOC7[i]
        tich = a1 * a2 + b1 * b2
        n1 = math.sqrt(a1 * a1 + b1 * b1)
        n2 = math.sqrt(a2 * a2 + b2 * b2)
        dung = r"$%d^{\circ}$" % goc
        nhieu = [r"$%d^{\circ}$" % g for g in (0, 30, 45, 60, 90)
                 if g != goc]
        random.shuffle(nhieu)
        debai = (r"Tính góc giữa hai đường thẳng $d_1: %s$ và $d_2: %s$."
                 % (_pt_duong_thang(a1, b1, c1),
                    _pt_duong_thang(a2, b2, c2)))
        giai = (r"Góc giữa hai đường thẳng tính qua hai vectơ pháp tuyến "
                r"$\overrightarrow{n_1} = %s$, $\overrightarrow{n_2} = %s$:"
                % (_toado7(a1, b1), _toado7(a2, b2)) +
                "\\\\\n"
                r"$\cos\varphi = \dfrac{\left|\overrightarrow{n_1}\cdot"
                r"\overrightarrow{n_2}\right|}"
                r"{\left|\overrightarrow{n_1}\right|\cdot"
                r"\left|\overrightarrow{n_2}\right|}$."
                "\\\\\n"
                r"Tử số: $\left|%s + %s\right| = %d$."
                % (_tich7(a1, a2), _tich7(b1, b2), abs(tich)) +
                "\\\\\n"
                r"Mẫu số: $\sqrt{%d}\cdot\sqrt{%d} = %s$."
                % (a1 * a1 + b1 * b1, a2 * a2 + b2 * b2,
                   _can7((a1 * a1 + b1 * b1) * (a2 * a2 + b2 * b2))) +
                "\\\\\n"
                r"$\cos\varphi = %s$ nên $\varphi = %d^{\circ}$."
                % (COS_GOC7[goc], goc) +
                "\\\\\n"
                r"Chú ý có \textbf{dấu giá trị tuyệt đối} ở tử nên góc giữa "
                r"hai đường thẳng luôn thuộc $\left[0^{\circ};\ "
                r"90^{\circ}\right]$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu[:4], giai, 0, 0, dang)
    return cauTN


def L10_C7_B20_TH111_SA_A_01(socau):
    r"""Số đo góc giữa hai đường thẳng - trả lời ngắn (đơn vị độ).

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(CAP_GOC7))
        c1 = random.randint(-6, 6)
        c2 = random.randint(-6, 6)
        v = (i, c1, c2)
        if v not in gt:
            gt.append(v)

    cau = ""
    for i, c1, c2 in gt:
        (a1, b1), (a2, b2), goc = CAP_GOC7[i]
        tich = a1 * a2 + b1 * b2
        n1 = math.sqrt(a1 * a1 + b1 * b1)
        n2 = math.sqrt(a2 * a2 + b2 * b2)
        debai = (r"Tính số đo góc giữa hai đường thẳng $d_1: %s$ và "
                 r"$d_2: %s$ (đơn vị: độ, chỉ ghi số)."
                 % (_pt_duong_thang(a1, b1, c1),
                    _pt_duong_thang(a2, b2, c2)))
        giai = (r"$\cos\varphi = \dfrac{\left|%s + %s\right|}"
                r"{\sqrt{%d}\cdot\sqrt{%d}} = %s$."
                % (_tich7(a1, a2), _tich7(b1, b2),
                   a1 * a1 + b1 * b1, a2 * a2 + b2 * b2, COS_GOC7[goc]) +
                "\\\\\n"
                r"Vậy $\varphi = %d^{\circ}$." % goc)
        nhieu = _ba_nhieu7(goc, [g for g in (0, 30, 45, 60, 90) if g != goc],
                           buoc=lambda t: goc + 10 * t)
        cau += MC_SA_answer_const(debai, goc, nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B20_VD109_MC_A_01(socau, dang=1):
    r"""Tìm tham số để hai đường thẳng song song hoặc vuông góc.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a1 = random.choice([1, 2, 3, -2])
        b1 = random.choice([1, 2, 3, -3])
        c1 = random.randint(-6, 6)
        c2 = random.randint(-6, 6)
        kieu = random.choice(["song_song", "vuong_goc"])
        # vuông góc thì m = -b1^2/a1 phải NGUYÊN, nếu không thì bỏ bộ số
        if kieu == "vuong_goc" and (b1 * b1) % a1 != 0:
            continue
        # song song: c2 phải KHÁC c1, nếu bằng thì hai đường TRÙNG nhau
        if kieu == "song_song" and c2 == c1:
            continue
        v = (a1, b1, c1, c2, kieu)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a1, b1, c1, c2, kieu in gt:
        if kieu == "song_song":
            # d2: a1 x + m y + c2 = 0 song song d1  =>  m = b1
            m = b1
            dk = (r"Hai đường thẳng song song khi hai vectơ pháp tuyến "
                  r"\textbf{cùng phương}: "
                  r"$\dfrac{a_2}{a_1} = \dfrac{b_2}{b_1}$.")
            tinh = (r"$\dfrac{a_2}{a_1} = \dfrac{%d}{%d} = 1$ nên "
                    r"$\dfrac{m}{%d} = 1$, suy ra $m = %d$."
                    % (a1, a1, b1, m) +
                    "\\\\\n"
                    r"Kiểm lại hằng số: $%d \ne %d$ nên hai đường thẳng "
                    r"\textbf{song song} chứ không trùng nhau." % (c2, c1))
            mo_ta = "song song với"
        else:
            # d2: m x + b1' y + c2 = 0 vuong goc d1: a1 x + b1 y + c1 = 0
            # n1 . n2 = 0  =>  a1*m + b1*b1 = 0  =>  m = -b1^2/a1
            m = -(b1 * b1) // a1
            dk = (r"Hai đường thẳng vuông góc khi hai vectơ pháp tuyến "
                  r"\textbf{vuông góc}: $\overrightarrow{n_1}\cdot"
                  r"\overrightarrow{n_2} = 0$.")
            tinh = (r"$%s + %s = 0 \Rightarrow %s = %d \Rightarrow m = %d$."
                    % (_don_thuc7(a1, "m"), _tich7(b1, b1),
                       _don_thuc7(a1, "m"), -(b1 * b1), m))
            mo_ta = "vuông góc với"

        dung = r"$m = %d$" % m
        nhieu = [r"$m = %d$" % x for x in _ba_nhieu7(
            m, [-m, m + 1, m - 1, a1], buoc=lambda t: m + 2 * t)]
        if kieu == "song_song":
            d2 = r"%s + my %s %d = 0" % (_don_thuc7(a1, "x"),
                                         "+" if c2 >= 0 else "-", abs(c2))
        else:
            d2 = r"mx %s %s %d = 0" % (_don_thuc7(b1, "y", False),
                                       "+" if c2 >= 0 else "-", abs(c2))
        debai = (r"Tìm $m$ để đường thẳng $d_2: %s$ %s đường thẳng "
                 r"$d_1: %s$." % (d2, mo_ta, _pt_duong_thang(a1, b1, c1)))
        giai = (r"$\overrightarrow{n_1} = %s$." % _toado7(a1, b1) +
                "\\\\\n" + dk + "\\\\\n" + tinh)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B20_VD109_SA_A_01(socau):
    r"""Giá trị tham số thoả điều kiện - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a1 = random.choice([1, 2, 3])
        b1 = random.choice([1, 2, 3, 4, 6])
        if (b1 * b1) % a1 != 0:
            continue
        c1 = random.randint(-6, 6)
        c2 = random.randint(-6, 6)
        v = (a1, b1, c1, c2)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a1, b1, c1, c2 in gt:
        m = -(b1 * b1) // a1
        debai = (r"Tìm $m$ để đường thẳng $d_2: mx %s %s %d = 0$ vuông "
                 r"góc với đường thẳng $d_1: %s$."
                 % (_don_thuc7(b1, "y", False),
                    "+" if c2 >= 0 else "-", abs(c2),
                    _pt_duong_thang(a1, b1, c1)))
        giai = (r"$\overrightarrow{n_1} = %s$, $\overrightarrow{n_2} = "
                r"\left(m;\ %d\right)$." % (_toado7(a1, b1), b1) +
                "\\\\\n"
                r"Hai đường thẳng vuông góc khi "
                r"$\overrightarrow{n_1}\cdot\overrightarrow{n_2} = 0$:"
                "\\\\\n"
                r"$%s + %s = 0 \Rightarrow m = %d$."
                % (_don_thuc7(a1, "m"), _tich7(b1, b1), m))
        nhieu = _ba_nhieu7(m, [-m, a1, b1], buoc=lambda t: m + 2 * t)
        cau += MC_SA_answer_const(debai, m, nhieu, giai, 0, 0, 2)
    return cau


# =====================================================================
# BÀI 21. ĐƯỜNG TRÒN TRONG MẶT PHẲNG TOẠ ĐỘ
# =====================================================================

def _pt_duong_tron(a, b, R):
    r"""Viết $(x-a)^2 + (y-b)^2 = R^2$."""
    px = ("x" if a == 0 else
          (r"\left(x %s %d\right)" % ("-" if a > 0 else "+", abs(a))))
    py = ("y" if b == 0 else
          (r"\left(y %s %d\right)" % ("-" if b > 0 else "+", abs(b))))
    return r"%s^2 + %s^2 = %d" % (px, py, R * R)


def L10_C7_B21_TH112_MC_A_01(socau, dang=1):
    r"""Lập phương trình đường tròn khi biết tâm và bán kính.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        R = random.randint(2, 8)
        if (a, b, R) not in gt:
            gt.append((a, b, R))

    cauTN = ""
    for a, b, R in gt:
        dung = r"$%s$" % _pt_duong_tron(a, b, R)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_tron(-a, -b, R),
             r"$%s$" % _pt_duong_tron(a, b, R + 1),
             r"$%s$" % _pt_duong_tron(b, a, R),
             r"$\left(x %s %d\right)^2 + \left(y %s %d\right)^2 = %d$"
             % ("-" if a > 0 else "+", abs(a),
                "-" if b > 0 else "+", abs(b), R)],
            buoc=lambda t: r"$%s$" % _pt_duong_tron(a, b, R + 1 + t))
        debai = (r"Lập phương trình đường tròn có tâm $I%s$ và bán kính "
                 r"$R = %d$." % (_toado7(a, b), R))
        giai = (r"Đường tròn tâm $I\left(a;\ b\right)$ bán kính $R$ có "
                r"phương trình"
                "\\\\\n"
                r"$\left(x - a\right)^2 + \left(y - b\right)^2 = R^2$."
                "\\\\\n"
                r"Thay $a = %d$, $b = %d$, $R = %d$:" % (a, b, R) +
                "\\\\\n"
                r"$%s$." % _pt_duong_tron(a, b, R) +
                "\\\\\n"
                r"Chú ý vế phải là $R^2 = %d$ chứ không phải $R = %d$; và "
                r"trong ngoặc là $x - a$ nên dấu \textbf{ngược} với dấu của "
                r"toạ độ tâm." % (R * R, R))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B21_TH115_MC_A_01(socau, dang=1):
    r"""Xác định tâm và bán kính từ phương trình đường tròn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Dùng dạng khai triển $x^2+y^2-2ax-2by+c=0$ để học sinh phải đưa về
    dạng chính tắc, đúng mức Thông hiểu.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        R = random.randint(2, 7)
        if (a, b, R) not in gt:
            gt.append((a, b, R))

    cauTN = ""
    for a, b, R in gt:
        c = a * a + b * b - R * R
        dung = r"$I%s$, $R = %d$" % (_toado7(a, b), R)
        nhieu = _ba_nhieu7(
            dung,
            [r"$I%s$, $R = %d$" % (_toado7(-a, -b), R),
             r"$I%s$, $R = %d$" % (_toado7(a, b), R * R),
             r"$I%s$, $R = %d$" % (_toado7(2 * a, 2 * b), R),
             r"$I%s$, $R = %d$" % (_toado7(a, b), R + 1)],
            buoc=lambda t: r"$I%s$, $R = %d$" % (_toado7(a, b), R + 1 + t))
        ve_trai = _tron_khai_trien(a, b, c)
        debai = (r"Xác định tâm $I$ và bán kính $R$ của đường tròn "
                 r"$%s$." % ve_trai)
        giai = (r"Phương trình dạng $x^2 + y^2 - 2ax - 2by + c = 0$ là "
                r"đường tròn tâm $I\left(a;\ b\right)$ bán kính "
                r"$R = \sqrt{a^2 + b^2 - c}$ (khi biểu thức dưới căn dương)."
                "\\\\\n"
                r"So sánh hệ số: $-2a = %d \Rightarrow a = %d$; "
                r"$-2b = %d \Rightarrow b = %d$; $c = %d$."
                % (-2 * a, a, -2 * b, b, c) +
                "\\\\\n"
                r"$R = \sqrt{%s^2 + %s^2 - %s} = \sqrt{%d} = %d$."
                % (_so7(a), _so7(b), _so7(c), R * R, R) +
                "\\\\\n"
                r"Vậy $I%s$ và $R = %d$." % (_toado7(a, b), R))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B21_TH115_SA_A_01(socau):
    r"""Bán kính của đường tròn cho trước - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        R = random.randint(2, 9)
        if (a, b, R) not in gt:
            gt.append((a, b, R))

    cau = ""
    for a, b, R in gt:
        c = a * a + b * b - R * R
        ve_trai = _tron_khai_trien(a, b, c)
        debai = (r"Tìm bán kính của đường tròn $%s$." % ve_trai)
        giai = (r"So sánh với $x^2 + y^2 - 2ax - 2by + c = 0$ được "
                r"$a = %d$, $b = %d$, $c = %d$." % (a, b, c) +
                "\\\\\n"
                r"$R = \sqrt{a^2 + b^2 - c} = \sqrt{%d + %d - %s} "
                r"= \sqrt{%d} = %d$."
                % (a * a, b * b, _so7(c), R * R, R))
        nhieu = _ba_nhieu7(R, [R * R, abs(a), abs(b), R + 1],
                           buoc=lambda t: R + 2 * t)
        cau += MC_SA_answer_const(debai, R, nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B21_TH116_MC_A_01(socau, dang=1):
    r"""Lập phương trình tiếp tuyến tại một điểm của đường tròn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        b = random.randint(-4, 4)
        u, v, R = random.choice(PYTAGO7)
        if random.choice([True, False]):
            u = -u
        if random.choice([True, False]):
            v = -v
        w = (a, b, u, v, R)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, u, v, R in gt:
        xm, ym = a + u, b + v          # điểm M trên đường tròn
        # tiếp tuyến tại M: pháp tuyến là IM = (u; v); rút gọn và chuẩn
        # hoá dấu để phương trình không bắt đầu bằng dấu trừ
        pn, qn, cn = _rut_gon7(u, v, -(u * xm + v * ym))
        dung = r"$%s$" % _pt_duong_thang(pn, qn, cn)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_thang(pn, qn, -cn),
             r"$%s$" % _pt_duong_thang(-qn, pn, -(-qn * xm + pn * ym)),
             r"$%s$" % _pt_duong_thang(pn, qn, -(pn * a + qn * b)),
             r"$%s$" % _pt_duong_thang(qn, pn, cn)],
            buoc=lambda t: r"$%s$" % _pt_duong_thang(pn, qn, cn + t))
        debai = (r"Cho đường tròn $\left(C\right): %s$ và điểm $M%s$ thuộc "
                 r"$\left(C\right)$. Lập phương trình tiếp tuyến của "
                 r"$\left(C\right)$ tại $M$."
                 % (_pt_duong_tron(a, b, R), _toado7(xm, ym)))
        giai = (r"Tâm đường tròn là $I%s$." % _toado7(a, b) +
                "\\\\\n"
                r"Tiếp tuyến tại $M$ \textbf{vuông góc} với bán kính $IM$, "
                r"nên nhận $\overrightarrow{IM} = %s$ (hoặc một vectơ cùng "
                r"phương) làm vectơ pháp tuyến; chọn $%s$ cho gọn."
                % (_toado7(u, v), _toado7(pn, qn)) +
                "\\\\\n"
                r"Tiếp tuyến đi qua $M%s$ với pháp tuyến $%s$:"
                % (_toado7(xm, ym), _toado7(pn, qn)) +
                "\\\\\n"
                r"$%s \Leftrightarrow %s$."
                % (_khai_trien7(pn, qn, xm, ym),
                   _pt_duong_thang(pn, qn, cn)) +
                "\\\\\n"
                r"Kiểm lại: khoảng cách từ $I%s$ tới đường thẳng này bằng "
                r"$\dfrac{\left|%d\right|}{%s} = %d = R$."
                % (_toado7(a, b), abs(pn * a + qn * b + cn),
                   _can7(pn * pn + qn * qn), R))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _tron_khai_trien(a, b, c):
    r"""Viết $x^2+y^2-2ax-2by+c = 0$, bỏ hẳn hạng tử có hệ số 0."""
    ve = "x^2 + y^2"
    ve += _don_thuc7(-2 * a, "x", False) and \
        (" " + _don_thuc7(-2 * a, "x", False))
    ve += _don_thuc7(-2 * b, "y", False) and \
        (" " + _don_thuc7(-2 * b, "y", False))
    if c:
        ve += " %s %d" % ("+" if c > 0 else "-", abs(c))
    return ve + " = 0"


def _ba_diem_duong_tron(lan_thu=300):
    """Ba điểm nằm trên một đường tròn có tâm và bán kính NGUYÊN."""
    for _ in range(lan_thu):
        a = random.randint(-4, 4)
        b = random.randint(-4, 4)
        R = random.choice([5, 10, 13, 17])
        # các vectơ độ dài R từ bộ ba Pytago
        cap = [(u, v) for u, v, n in PYTAGO7 if n == R]
        cap = cap + [(-u, v) for u, v in cap] + [(u, -v) for u, v in cap] \
            + [(-u, -v) for u, v in cap] + [(R, 0), (-R, 0), (0, R), (0, -R)]
        cap = list({c for c in cap})
        if len(cap) < 3:
            continue
        ba = random.sample(cap, 3)
        diem = [(a + u, b + v) for u, v in ba]
        # ba điểm không thẳng hàng
        (x1, y1), (x2, y2), (x3, y3) = diem
        if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0:
            continue
        return a, b, R, diem
    return None


def L10_C7_B21_VD113_MC_A_01(socau, dang=1):
    r"""Lập phương trình đường tròn đi qua ba điểm.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    thu = 0
    while len(gt) < socau and thu < 60:
        thu += 1
        v = _ba_diem_duong_tron()
        if v is None:
            continue
        a, b, R, diem = v
        w = (a, b, R, tuple(diem))
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, R, diem in gt:
        diem = list(diem)
        dung = r"$%s$" % _pt_duong_tron(a, b, R)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_tron(-a, -b, R),
             r"$%s$" % _pt_duong_tron(a, b, R + 1),
             r"$%s$" % _pt_duong_tron(b, a, R),
             r"$%s$" % _pt_duong_tron(a + 1, b, R)],
            buoc=lambda t: r"$%s$" % _pt_duong_tron(a, b, R + 1 + t))
        ten = "ABC"
        mo_ta = ", ".join("$%s%s$" % (ten[i], _toado7(*diem[i]))
                          for i in range(3))
        debai = (r"Lập phương trình đường tròn đi qua ba điểm %s." % mo_ta)
        giai = (r"Gọi đường tròn là $x^2 + y^2 - 2ax - 2by + c = 0$. Thay "
                r"toạ độ ba điểm vào ta được hệ ba phương trình bậc nhất ẩn "
                r"$a$, $b$, $c$."
                "\\\\\n"
                r"Giải hệ được $a = %d$, $b = %d$, $c = %d$."
                % (a, b, a * a + b * b - R * R) +
                "\\\\\n"
                r"Tâm $I%s$, bán kính $R = \sqrt{a^2 + b^2 - c} = %d$."
                % (_toado7(a, b), R) +
                "\\\\\n"
                r"Kiểm lại từng điểm: khoảng cách từ $I$ tới mỗi điểm đều "
                r"bằng $%d$." % R +
                "\\\\\n"
                r"Vậy đường tròn là $%s$." % _pt_duong_tron(a, b, R))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B21_VD113_TL_A_01(socau, dong=1):
    r"""Tự luận: viết phương trình đường tròn ngoại tiếp tam giác.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    thu = 0
    while len(gt) < socau and thu < 60:
        thu += 1
        v = _ba_diem_duong_tron()
        if v is None:
            continue
        a, b, R, diem = v
        w = (a, b, R, tuple(diem))
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, R, diem in gt:
        diem = list(diem)
        c = a * a + b * b - R * R
        (x1, y1), (x2, y2), (x3, y3) = diem

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho tam giác $ABC$ với "
                 r"$A%s$, $B%s$, $C%s$."
                 % (_toado7(x1, y1), _toado7(x2, y2), _toado7(x3, y3)))

        hoi_a = (r"Gọi đường tròn ngoại tiếp tam giác có phương trình "
                 r"$x^2 + y^2 - 2ax - 2by + c = 0$. Tìm toạ độ tâm $I$ "
                 r"của đường tròn đó.")
        giai_a = (r"Thay lần lượt toạ độ ba điểm vào phương trình:"
                  "\\\\\n"
                  r"$%d - 2a\cdot %s - 2b\cdot %s + c = 0$;"
                  % (x1 * x1 + y1 * y1, _so7(x1), _so7(y1)) +
                  "\\\\\n"
                  r"$%d - 2a\cdot %s - 2b\cdot %s + c = 0$;"
                  % (x2 * x2 + y2 * y2, _so7(x2), _so7(y2)) +
                  "\\\\\n"
                  r"$%d - 2a\cdot %s - 2b\cdot %s + c = 0$."
                  % (x3 * x3 + y3 * y3, _so7(x3), _so7(y3)) +
                  "\\\\\n"
                  r"Trừ từng đôi một để khử $c$ rồi giải hệ hai phương "
                  r"trình bậc nhất còn lại: $a = %d$, $b = %d$, $c = %d$."
                  % (a, b, c) +
                  "\\\\\n"
                  r"Vậy tâm là $I%s$." % _toado7(a, b))

        hoi_b = r"Tính bán kính $R$ của đường tròn ngoại tiếp tam giác."
        giai_b = (r"$R = \sqrt{a^2 + b^2 - c} = \sqrt{%d + %d - %s} = "
                  r"\sqrt{%d} = %d$."
                  % (a * a, b * b, _so7(c), R * R, R) +
                  "\\\\\n"
                  r"Cách khác: $R = IA = \sqrt{%d + %d} = %d$."
                  % ((x1 - a) ** 2, (y1 - b) ** 2, R))

        hoi_c = r"Viết phương trình đường tròn ngoại tiếp tam giác $ABC$."
        giai_c = (r"$%s$." % _pt_duong_tron(a, b, R) +
                  "\\\\\n"
                  r"Kiểm lại: $IA = IB = IC = %d$ nên $I$ đúng là tâm đường "
                  r"tròn ngoại tiếp." % R)

        ds_abcd = [(hoi_a, r"I\left(%d;\ %d\right)" % (a, b), giai_a),
                   (hoi_b, r"R = %d" % R, giai_b),
                   (hoi_c, _pt_duong_tron(a, b, R), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C7_B21_VD114_MC_A_01(socau, dang=1):
    r"""Lập phương trình đường tròn từ điều kiện không trực tiếp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đường tròn có tâm cho trước và TIẾP XÚC một đường thẳng: bán kính
    chính là khoảng cách từ tâm tới đường thẳng.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        b = random.randint(-4, 4)
        u, v, n = random.choice(PYTAGO7)
        R = random.randint(2, 6)
        # chọn c để khoảng cách từ I tới đường thẳng đúng bằng R
        c = R * n - (u * a + v * b)
        w = (a, b, u, v, n, R, c)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, u, v, n, R, c in gt:
        dung = r"$%s$" % _pt_duong_tron(a, b, R)
        nhieu = [r"$%s$" % _pt_duong_tron(a, b, R + 1),
                 r"$%s$" % _pt_duong_tron(a, b, R * R),
                 r"$%s$" % _pt_duong_tron(-a, -b, R),
                 r"$%s$" % _pt_duong_tron(a, b, max(R - 1, 1))]
        debai = (r"Lập phương trình đường tròn có tâm $I%s$ và tiếp xúc với "
                 r"đường thẳng $\Delta: %s$."
                 % (_toado7(a, b), _pt_duong_thang(u, v, c)))
        giai = (r"Đường tròn tiếp xúc với $\Delta$ nghĩa là khoảng cách từ "
                r"tâm tới $\Delta$ \textbf{đúng bằng} bán kính."
                "\\\\\n"
                r"$R = d\left(I;\ \Delta\right) = "
                r"\dfrac{\left|%s + %s %s %d\right|}"
                r"{\sqrt{%s^2 + %s^2}}$"
                % (_tich7(u, a), _tich7(v, b),
                   "+" if c >= 0 else "-", abs(c), _so7(u), _so7(v)) +
                "\\\\\n"
                r"$= \dfrac{%d}{%d} = %d$."
                % (abs(u * a + v * b + c), n, R) +
                "\\\\\n"
                r"Vậy đường tròn là $%s$." % _pt_duong_tron(a, b, R))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B21_VD114_SA_A_01(socau):
    r"""Bán kính đường tròn thoả điều kiện - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-4, 4)
        b = random.randint(-4, 4)
        u, v, n = random.choice(PYTAGO7)
        R = random.randint(2, 8)
        c = R * n - (u * a + v * b)
        w = (a, b, u, v, n, R, c)
        if w not in gt:
            gt.append(w)

    cau = ""
    for a, b, u, v, n, R, c in gt:
        debai = (r"Đường tròn có tâm $I%s$ và tiếp xúc với đường thẳng "
                 r"$\Delta: %s$. Tính bán kính của đường tròn."
                 % (_toado7(a, b), _pt_duong_thang(u, v, c)))
        giai = (r"Tiếp xúc nghĩa là $R = d\left(I;\ \Delta\right)$:"
                "\\\\\n"
                r"$R = \dfrac{\left|%s + %s %s %d\right|}"
                r"{\sqrt{%s^2 + %s^2}} = \dfrac{%d}{%d} = %d$."
                % (_tich7(u, a), _tich7(v, b),
                   "+" if c >= 0 else "-", abs(c), _so7(u), _so7(v),
                   abs(u * a + v * b + c), n, R))
        nhieu = _ba_nhieu7(R, [R * R, n, abs(u * a + v * b + c)],
                           buoc=lambda t: R + 2 * t)
        cau += MC_SA_answer_const(debai, R, nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B21_VD117_MC_A_01(socau, dang=1):
    r"""Bài toán chuyển động tròn trong Vật lí.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-3, 3)
        b = random.randint(-3, 3)
        R = random.choice([5, 10, 13])
        cap = [(u, v) for u, v, n in PYTAGO7 if n == R]
        if not cap:
            continue
        u, v = random.choice(cap)
        w = (a, b, R, u, v)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, R, u, v in gt:
        xm, ym = a + u, b + v
        dung = r"$%s$" % _pt_duong_tron(a, b, R)
        nhieu = _ba_nhieu7(
            dung,
            [r"$%s$" % _pt_duong_tron(xm, ym, R),
             r"$%s$" % _pt_duong_tron(a, b, R + 1),
             r"$%s$" % _pt_duong_tron(-a, -b, R),
             r"$%s$" % _pt_duong_tron(a, b, R * 2)],
            buoc=lambda t: r"$%s$" % _pt_duong_tron(a, b, R + 1 + t))
        debai = (r"Một vệ tinh chuyển động tròn đều quanh tâm $I%s$ trong "
                 r"mặt phẳng toạ độ $Oxy$ (đơn vị trên mỗi trục là nghìn "
                 r"ki-lô-mét). Tại một thời điểm, vệ tinh ở vị trí $M%s$. "
                 r"Viết phương trình quỹ đạo của vệ tinh."
                 % (_toado7(a, b), _toado7(xm, ym)))
        giai = (r"Chuyển động tròn đều quanh tâm $I$ nên quỹ đạo là đường "
                r"tròn tâm $I$, bán kính $R = IM$."
                "\\\\\n"
                r"$\overrightarrow{IM} = %s$ nên "
                r"$R = \sqrt{%d^2 + %d^2} = \sqrt{%d} = %d$."
                % (_toado7(u, v), u, v, u * u + v * v, R) +
                "\\\\\n"
                r"Vậy quỹ đạo là $%s$." % _pt_duong_tron(a, b, R) +
                "\\\\\n"
                r"Chú ý tâm quỹ đạo là $I$ chứ không phải vị trí $M$ của vệ "
                r"tinh.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B21_VD117_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về đường tròn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-3, 3)
        b = random.randint(-3, 3)
        R = random.choice([5, 10, 13])
        cap = [(u, v) for u, v, n in PYTAGO7 if n == R]
        if not cap:
            continue
        u, v = random.choice(cap)
        w = (a, b, R, u, v)
        if w not in gt:
            gt.append(w)

    cauTN = ""
    for a, b, R, u, v in gt:
        xm, ym = a + u, b + v
        c = -(u * xm + v * ym)

        debai = (r"Một trạm phát sóng đặt tại $I%s$ có bán kính phủ sóng "
                 r"$R$ (đơn vị: ki-lô-mét). Biết điểm $M%s$ nằm đúng trên "
                 r"ranh giới vùng phủ sóng."
                 % (_toado7(a, b), _toado7(xm, ym)))

        hoi_a = r"Tính bán kính phủ sóng $R$."
        giai_a = (r"$M$ nằm trên ranh giới nên $R = IM$."
                  "\\\\\n"
                  r"$\overrightarrow{IM} = %s$ nên "
                  r"$R = \sqrt{%d^2 + %d^2} = %d$ (km)."
                  % (_toado7(u, v), u, v, R))

        hoi_b = r"Viết phương trình đường tròn ranh giới vùng phủ sóng."
        giai_b = (r"Đường tròn tâm $I%s$ bán kính $R = %d$:"
                  % (_toado7(a, b), R) +
                  "\\\\\n"
                  r"$%s$." % _pt_duong_tron(a, b, R))

        # điểm N ở trong vùng phủ sóng
        xn, yn = a + u // 2, b + v // 2
        p_in, q_in = xn - a, yn - b
        s_in = p_in * p_in + q_in * q_in
        hoi_c = (r"Điểm $N%s$ có nằm trong vùng phủ sóng không? Giải thích."
                 % _toado7(xn, yn))
        giai_c = (r"So sánh $IN$ với $R$ bằng cách so sánh BÌNH PHƯƠNG, "
                  r"khỏi phải tính căn:"
                  "\\\\\n"
                  r"$IN^2 = %s^2 + %s^2 = %d$ và $R^2 = %d$."
                  % (_so7(p_in), _so7(q_in), s_in, R * R) +
                  "\\\\\n"
                  r"Vì $%d < %d$ nên $IN < R$: điểm $N$ \textbf{nằm trong} "
                  r"vùng phủ sóng." % (s_in, R * R))

        ds_abcd = [(hoi_a, r"R = %d\ \text{km}" % R, giai_a),
                   (hoi_b, _pt_duong_tron(a, b, R), giai_b),
                   (hoi_c, r"\text{Có}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 22. BA ĐƯỜNG CONIC
# =====================================================================

def L10_C7_B22_NB118_MC_A_01(socau, dang=1):
    r"""Nhận ra elip, hypebol, parabol bằng hình học.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MO_TA = [
        ("elip", r"Tập hợp các điểm $M$ có \textbf{tổng} khoảng cách tới hai "
                 r"điểm cố định $F_1$, $F_2$ bằng một hằng số lớn hơn "
                 r"$F_1F_2$",
         r"Tổng $MF_1 + MF_2$ không đổi là đặc trưng của elip."),
        ("hypebol", r"Tập hợp các điểm $M$ có \textbf{trị tuyệt đối của hiệu} "
                    r"khoảng cách tới hai điểm cố định $F_1$, $F_2$ bằng một "
                    r"hằng số nhỏ hơn $F_1F_2$",
         r"Hiệu $\left|MF_1 - MF_2\right|$ không đổi là đặc trưng của "
         r"hypebol."),
        ("parabol", r"Tập hợp các điểm $M$ \textbf{cách đều} một điểm cố "
                    r"định $F$ và một đường thẳng cố định không đi qua $F$",
         r"Cách đều một điểm và một đường thẳng là đặc trưng của parabol."),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(MO_TA))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(MO_TA):
            break

    cauTN = ""
    for i in gt:
        ten, mo_ta, ly_do = MO_TA[i]
        dung = ten.capitalize()
        nhieu = [t.capitalize() for t, _m, _l in MO_TA if t != ten]
        nhieu.append("Đường tròn")
        debai = r"%s là đường conic nào sau đây?" % mo_ta
        giai = (ly_do +
                "\\\\\n"
                r"Nhắc lại: elip dùng \textbf{tổng} khoảng cách, hypebol "
                r"dùng \textbf{hiệu} khoảng cách tới hai tiêu điểm, còn "
                r"parabol dùng khoảng cách tới \textbf{một} tiêu điểm và "
                r"\textbf{một} đường chuẩn."
                "\\\\\n"
                r"Đường tròn là tập hợp các điểm cách đều \textbf{một} điểm "
                r"cố định, không thuộc ba đường conic kể trên.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B22_NB119_MC_A_01(socau, dang=1):
    r"""Nhận ra phương trình chính tắc của ba đường conic.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([3, 4, 5, 6])
        b = random.choice([2, 3, 4])
        if a <= b:
            continue
        loai = random.choice(["elip", "hypebol", "parabol"])
        p = random.choice([2, 4, 6, 8])
        v = (a, b, loai, p)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, loai, p in gt:
        pt_elip = r"\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1" % (a * a, b * b)
        pt_hyp = r"\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1" % (a * a, b * b)
        pt_par = r"y^2 = %dx" % (2 * p)
        pt_tron = r"x^2 + y^2 = %d" % (a * a)
        bang = {"elip": pt_elip, "hypebol": pt_hyp, "parabol": pt_par}
        dung = r"$%s$" % bang[loai]
        nhieu = [r"$%s$" % v for k, v in bang.items() if k != loai]
        nhieu.append(r"$%s$" % pt_tron)
        debai = (r"Phương trình nào sau đây là phương trình chính tắc của "
                 r"\textbf{%s}?" % loai)
        giai = (r"Phương trình chính tắc của ba đường conic:"
                "\\\\\n"
                r"$\bullet$ Elip: $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$ "
                r"- hai số hạng \textbf{cộng} nhau."
                "\\\\\n"
                r"$\bullet$ Hypebol: $\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} "
                r"= 1$ - hai số hạng \textbf{trừ} nhau."
                "\\\\\n"
                r"$\bullet$ Parabol: $y^2 = 2px$ với $p > 0$ - chỉ có "
                r"\textbf{một} biến bình phương."
                "\\\\\n"
                r"Vậy phương trình của %s là $%s$." % (loai, bang[loai]))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _bo_elip():
    """Bộ (a, b, c) cho elip có tiêu cự NGUYÊN: a^2 - b^2 là chính phương."""
    BO = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12),
          (10, 8, 6), (10, 6, 8), (17, 15, 8), (25, 24, 7)]
    return random.choice(BO)


def L10_C7_B22_TH120_MC_A_01(socau, dang=1):
    r"""Lập phương trình chính tắc của elip.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_elip()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c in gt:
        dung = r"$\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$" % (a * a, b * b)
        nhieu = [r"$\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$" % (b * b, a * a),
                 r"$\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1$" % (a * a, b * b),
                 r"$\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$" % (a, b),
                 r"$\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$"
                 % (a * a, c * c)]
        debai = (r"Lập phương trình chính tắc của elip có độ dài trục lớn "
                 r"bằng $%d$ và độ dài trục nhỏ bằng $%d$."
                 % (2 * a, 2 * b))
        giai = (r"Elip chính tắc $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$ "
                r"có trục lớn dài $2a$ và trục nhỏ dài $2b$ (với $a > b > 0$)."
                "\\\\\n"
                r"$2a = %d \Rightarrow a = %d$; $2b = %d \Rightarrow b = %d$."
                % (2 * a, a, 2 * b, b) +
                "\\\\\n"
                r"Vậy phương trình là "
                r"$\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$."
                % (a * a, b * b) +
                "\\\\\n"
                r"Chú ý mẫu số là $a^2$ và $b^2$ chứ không phải $a$ và $b$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B22_TH120_SA_A_01(socau):
    r"""Tiêu cự, độ dài trục của elip - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_elip()
        hoi = random.choice(["tieu_cu", "truc_lon", "truc_nho"])
        w = v + (hoi,)
        if w not in gt:
            gt.append(w)

    cau = ""
    for a, b, c, hoi in gt:
        if hoi == "tieu_cu":
            kq = 2 * c
            ten = "tiêu cự $F_1F_2$"
            tinh = (r"$c^2 = a^2 - b^2 = %d - %d = %d \Rightarrow c = %d$."
                    % (a * a, b * b, c * c, c) +
                    "\\\\\n"
                    r"Tiêu cự $F_1F_2 = 2c = %d$." % (2 * c))
        elif hoi == "truc_lon":
            kq = 2 * a
            ten = "độ dài trục lớn"
            tinh = (r"$a^2 = %d \Rightarrow a = %d$, nên trục lớn dài "
                    r"$2a = %d$." % (a * a, a, 2 * a))
        else:
            kq = 2 * b
            ten = "độ dài trục nhỏ"
            tinh = (r"$b^2 = %d \Rightarrow b = %d$, nên trục nhỏ dài "
                    r"$2b = %d$." % (b * b, b, 2 * b))
        debai = (r"Cho elip $\left(E\right): "
                 r"\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$. Tính %s."
                 % (a * a, b * b, ten))
        giai = (r"Elip chính tắc có $a^2 = %d$, $b^2 = %d$ với $a > b > 0$."
                % (a * a, b * b) +
                "\\\\\n" + tinh)
        nhieu = _ba_nhieu7(kq, [a, b, c, 2 * a if kq != 2 * a else 2 * b],
                           buoc=lambda t: kq + 2 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B22_TH121_MC_A_01(socau, dang=1):
    r"""Lập phương trình chính tắc của hypebol.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    # (a, b, c) với c^2 = a^2 + b^2
    BO = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (5, 12, 13),
          (12, 5, 13), (8, 15, 17), (15, 8, 17)]
    gt = [BO[i] for i in _chon_chi_muc7(len(BO), socau)]

    cauTN = ""
    for a, b, c in gt:
        dung = r"$\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1$" % (a * a, b * b)
        nhieu = [r"$\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$" % (a * a, b * b),
                 r"$\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1$" % (b * b, a * a),
                 r"$\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1$" % (a, b),
                 r"$\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1$" % (a * a, c * c)]
        debai = (r"Lập phương trình chính tắc của hypebol có độ dài trục "
                 r"thực bằng $%d$ và tiêu cự bằng $%d$." % (2 * a, 2 * c))
        giai = (r"Hypebol chính tắc $\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} = 1$ "
                r"có trục thực dài $2a$, tiêu cự $2c$ và $c^2 = a^2 + b^2$."
                "\\\\\n"
                r"$2a = %d \Rightarrow a = %d$; $2c = %d \Rightarrow c = %d$."
                % (2 * a, a, 2 * c, c) +
                "\\\\\n"
                r"$b^2 = c^2 - a^2 = %d - %d = %d$."
                % (c * c, a * a, b * b) +
                "\\\\\n"
                r"Vậy phương trình là "
                r"$\dfrac{x^2}{%d} - \dfrac{y^2}{%d} = 1$."
                % (a * a, b * b) +
                "\\\\\n"
                r"Chú ý với hypebol thì $c^2 = a^2 + b^2$ (khác elip, nơi "
                r"$c^2 = a^2 - b^2$).")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B22_TH122_MC_A_01(socau, dang=1):
    r"""Lập phương trình chính tắc của parabol.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p = random.choice([1, 2, 3, 4, 6, 8])
        if p not in gt:
            gt.append(p)
        if len(gt) >= 6:
            break

    cauTN = ""
    for p in gt:
        dung = r"$y^2 = %s$" % _don_thuc7(2 * p, "x")
        nhieu = _ba_nhieu7(
            dung,
            [r"$y^2 = %s$" % _don_thuc7(p, "x"),
             r"$y^2 = %s$" % _don_thuc7(4 * p, "x"),
             r"$x^2 = %s$" % _don_thuc7(2 * p, "y"),
             r"$y^2 = %s$" % _don_thuc7(2 * p + 2, "x")],
            buoc=lambda t: r"$y^2 = %s$" % _don_thuc7(2 * p + 2 + t, "x"))
        debai = (r"Lập phương trình chính tắc của parabol có tiêu điểm "
                 r"$F\left(%s;\ 0\right)$." % _xx7(p / 2.0))
        giai = (r"Parabol chính tắc $y^2 = 2px$ (với $p > 0$) có tiêu điểm "
                r"$F\left(\dfrac{p}{2};\ 0\right)$ và đường chuẩn "
                r"$x = -\dfrac{p}{2}$."
                "\\\\\n"
                r"$\dfrac{p}{2} = %s \Rightarrow p = %d$."
                % (_xx7(p / 2.0), p) +
                "\\\\\n"
                r"Vậy phương trình là $y^2 = 2\cdot %d\cdot x = %s$."
                % (p, _don_thuc7(2 * p, "x")))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B22_VD123_MC_A_01(socau, dang=1):
    r"""Hiện tượng Quang học gắn với đường conic.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p = random.choice([2, 4, 6, 8, 10])
        if p not in gt:
            gt.append(p)
        if len(gt) >= 5:
            break

    cauTN = ""
    for p in gt:
        tieu = p / 2.0
        dung = r"$%s$ cm" % _xx7(tieu)
        nhieu = [r"$%s$ cm" % x for x in _ba_nhieu7(
            _xx7(tieu), [_xx7(p), _xx7(2 * p), _xx7(tieu / 2), _xx7(p * p)],
            buoc=lambda t: _xx7(tieu + t))]
        debai = (r"Mặt cắt của một chảo ăng-ten (hoặc đèn pha ô tô) có dạng "
                 r"parabol với phương trình $y^2 = %dx$ (đơn vị: xăng-ti-mét) "
                 r"trong hệ trục đã chọn. Bộ thu tín hiệu được đặt tại tiêu "
                 r"điểm của parabol. Hỏi bộ thu cách đỉnh chảo bao nhiêu?"
                 % (2 * p))
        giai = (r"Parabol chính tắc $y^2 = 2px$ có đỉnh tại gốc toạ độ $O$ "
                r"và tiêu điểm $F\left(\dfrac{p}{2};\ 0\right)$."
                "\\\\\n"
                r"So sánh $y^2 = %dx$ với $y^2 = 2px$ được $2p = %d$, nên "
                r"$p = %d$." % (2 * p, 2 * p, p) +
                "\\\\\n"
                r"Khoảng cách từ tiêu điểm tới đỉnh là "
                r"$\dfrac{p}{2} = %s$ (cm)." % _xx7(tieu) +
                "\\\\\n"
                r"Đây chính là lí do chảo ăng-ten có dạng parabol: mọi tia "
                r"song song với trục sau khi phản xạ đều đi qua tiêu điểm, "
                r"nên tín hiệu tụ hết về bộ thu.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B22_VD123_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về đường conic.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_elip()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c in gt:
        debai = (r"Một mảnh vườn hình elip có độ dài trục lớn bằng $%d$ m và "
                 r"độ dài trục nhỏ bằng $%d$ m. Chọn hệ trục toạ độ $Oxy$ "
                 r"với gốc tại tâm mảnh vườn, trục $Ox$ dọc theo trục lớn."
                 % (2 * a, 2 * b))

        hoi_a = r"Viết phương trình chính tắc của elip."
        giai_a = (r"Trục lớn $2a = %d \Rightarrow a = %d$; trục nhỏ "
                  r"$2b = %d \Rightarrow b = %d$." % (2 * a, a, 2 * b, b) +
                  "\\\\\n"
                  r"$\left(E\right): \dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$."
                  % (a * a, b * b))

        hoi_b = r"Tính tiêu cự của elip."
        giai_b = (r"$c^2 = a^2 - b^2 = %d - %d = %d \Rightarrow c = %d$."
                  % (a * a, b * b, c * c, c) +
                  "\\\\\n"
                  r"Tiêu cự $F_1F_2 = 2c = %d$ (m)." % (2 * c))

        hoi_c = (r"Người ta cắm hai cọc tại hai tiêu điểm và buộc một sợi "
                 r"dây qua hai cọc. Tính chiều dài sợi dây để đầu bút luôn "
                 r"vẽ đúng trên đường biên của mảnh vườn.")
        giai_c = (r"Với mọi điểm $M$ trên elip, tổng khoảng cách tới hai "
                  r"tiêu điểm luôn bằng $2a$:"
                  "\\\\\n"
                  r"$MF_1 + MF_2 = 2a = %d$ (m)." % (2 * a) +
                  "\\\\\n"
                  r"Sợi dây gồm hai đoạn $MF_1$, $MF_2$ và đoạn nối hai cọc "
                  r"$F_1F_2 = %d$ m, nên dài" % (2 * c) +
                  "\\\\\n"
                  r"$2a + 2c = %d + %d = %d$ (m)." % (2 * a, 2 * c,
                                                      2 * a + 2 * c))

        ds_abcd = [(hoi_a, r"\dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1"
                    % (a * a, b * b), giai_a),
                   (hoi_b, r"2c = %d\ \text{m}" % (2 * c), giai_b),
                   (hoi_c, r"%d\ \text{m}" % (2 * a + 2 * c), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C7_B22_VD124_MC_A_01(socau, dang=1):
    r"""Bài toán thực tiễn dùng phương pháp toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice(PYTAGO7)
        c = random.randint(-9, 9)
        x0 = random.randint(-6, 6)
        y0 = random.randint(-6, 6)
        tu = abs(a * x0 + b * y0 + c)
        if tu == 0:
            continue
        d = tu / float(n)
        if abs(d * 100 - round(d * 100)) > 1e-9:
            continue
        v = (a, b, n, c, x0, y0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, n, c, x0, y0 in gt:
        tu = abs(a * x0 + b * y0 + c)
        d = tu / float(n)
        dung = r"$%s$ km" % _xx7(d)
        nhieu = [r"$%s$ km" % x for x in _ba_nhieu7(
            _xx7(d), [_xx7(tu), _xx7(d * n), _xx7(tu / (n * n))],
            buoc=lambda t: _xx7(d + t / 2.0))]
        debai = (r"Trên bản đồ đặt trong mặt phẳng toạ độ $Oxy$ (đơn vị: "
                 r"ki-lô-mét), một con đường thẳng có phương trình $%s$ và "
                 r"một trạm cứu hộ đặt tại điểm $A%s$. Tính khoảng cách "
                 r"ngắn nhất từ trạm cứu hộ tới con đường."
                 % (_pt_duong_thang(a, b, c), _toado7(x0, y0)))
        giai = (r"Khoảng cách ngắn nhất từ một điểm tới một đường thẳng "
                r"chính là khoảng cách theo phương vuông góc:"
                "\\\\\n"
                r"$d\left(A;\ \Delta\right) = "
                r"\dfrac{\left|ax_0 + by_0 + c\right|}{\sqrt{a^2 + b^2}}$."
                "\\\\\n"
                r"$= \dfrac{\left|%s + %s %s %d\right|}"
                r"{\sqrt{%s^2 + %s^2}} = \dfrac{%d}{%d} = %s$ (km)."
                % (_tich7(a, x0), _tich7(b, y0),
                   "+" if c >= 0 else "-", abs(c), _so7(a), _so7(b),
                   tu, n, _xx7(d)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C7_B22_VD124_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn tổng hợp về toạ độ.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice(PYTAGO7)
        c = random.randint(-9, 9)
        x0 = random.randint(-6, 6)
        y0 = random.randint(-6, 6)
        tu = abs(a * x0 + b * y0 + c)
        if tu == 0:
            continue
        d = tu / float(n)
        if abs(d * 100 - round(d * 100)) > 1e-9:
            continue
        v = (a, b, n, c, x0, y0)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, n, c, x0, y0 in gt:
        tu = abs(a * x0 + b * y0 + c)
        d = tu / float(n)
        # đường thẳng qua A vuông góc với con đường
        a2, b2, c2 = _rut_gon7(-b, a, b * x0 - a * y0)
        R = d
        pt_tron = (r"\left(x %s %d\right)^2 + \left(y %s %d\right)^2 = %s"
                   % ("-" if x0 >= 0 else "+", abs(x0),
                      "-" if y0 >= 0 else "+", abs(y0), _xx7(R * R, 4)))

        debai = (r"Trên bản đồ đặt trong mặt phẳng toạ độ $Oxy$ (đơn vị: "
                 r"ki-lô-mét), một con đường thẳng có phương trình "
                 r"$\Delta: %s$ và một trạm phát sóng đặt tại $A%s$."
                 % (_pt_duong_thang(a, b, c), _toado7(x0, y0)))

        hoi_a = r"Tính khoảng cách từ trạm $A$ tới con đường $\Delta$."
        giai_a = (r"$d\left(A;\ \Delta\right) = "
                  r"\dfrac{\left|%s + %s %s %d\right|}"
                  r"{\sqrt{%s^2 + %s^2}} = \dfrac{%d}{%d} = %s$ (km)."
                  % (_tich7(a, x0), _tich7(b, y0),
                     "+" if c >= 0 else "-", abs(c), _so7(a), _so7(b),
                     tu, n, _xx7(d)))

        hoi_b = (r"Lập phương trình đường thẳng đi qua $A$ và vuông góc với "
                 r"$\Delta$.")
        giai_b = (r"$\Delta$ có vectơ pháp tuyến $%s$, nên đường thẳng "
                  r"vuông góc với $\Delta$ nhận $%s$ làm \textbf{vectơ pháp "
                  r"tuyến} (quay vectơ kia đi $90^{\circ}$)."
                  % (_toado7(a, b), _toado7(a2, b2)) +
                  "\\\\\n"
                  r"Đường thẳng qua $A%s$: $%s$."
                  % (_toado7(x0, y0), _pt_duong_thang(a2, b2, c2)))

        hoi_c = (r"Viết phương trình đường tròn tâm $A$, tiếp xúc với con "
                 r"đường $\Delta$.")
        giai_c = (r"Đường tròn tiếp xúc với $\Delta$ nên bán kính bằng đúng "
                  r"khoảng cách từ tâm tới $\Delta$: $R = %s$ km." % _xx7(R) +
                  "\\\\\n"
                  r"Phương trình: $%s$." % pt_tron)

        ds_abcd = [(hoi_a, r"%s\ \text{km}" % _xx7(d), giai_a),
                   (hoi_b, _pt_duong_thang(a2, b2, c2), giai_b),
                   (hoi_c, pt_tron, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 7
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================


def L10_C7_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - phương trình đường thẳng; khoảng cách từ điểm đến
    đường thẳng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice(PYTAGO7)
        c = random.randint(-9, 9)
        x0 = random.randint(-6, 6)
        y0 = random.randint(-6, 6)
        tu = a * x0 + b * y0 + c
        if tu == 0:
            continue
        d = abs(tu) / float(n)
        if abs(d * 100 - round(d * 100)) > 1e-9:
            continue
        v = (a, b, n, c, x0, y0)
        if v not in gt:
            gt.append(v)

    cauTF = ''
    for a, b, n, c, x0, y0 in gt:
        tu = a * x0 + b * y0 + c
        d = abs(tu) / float(n)
        dau_c = "+" if c >= 0 else "-"
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho đường thẳng "
                 r"$\Delta: %s$ và điểm $A%s$."
                 % (_pt_duong_thang(a, b, c), _toado7(x0, y0)))

        ds_abcd = (
            # a) NB - đọc thẳng hệ số của phương trình tổng quát
            [
                (r"{\True Đường thẳng $\Delta$ có một vectơ pháp tuyến là "
                 r"$\overrightarrow{n} = %s$}" % _toado7(a, b),
                 r"Đúng. Phương trình tổng quát $ax + by + c = 0$ luôn "
                 r"nhận $\overrightarrow{n} = \left(a;\ b\right)$ làm vectơ pháp "
                 r"tuyến; ở đây $a = %d$, $b = %d$." % (a, b)),
                (r"{Đường thẳng $\Delta$ có một vectơ pháp tuyến là "
                 r"$\overrightarrow{n} = %s$}" % _toado7(-b, a),
                 r"Sai. $%s$ là vectơ CHỈ PHƯƠNG của $\Delta$ (vuông góc "
                 r"với $\overrightarrow{n} = %s$), không phải vectơ pháp tuyến."
                 % (_toado7(-b, a), _toado7(a, b))),
            ],
            # b) TH - thay toạ độ điểm vào vế trái
            [
                (r"{\True Điểm $A$ không nằm trên đường thẳng $\Delta$}",
                 r"Đúng. Thay $x = %d$, $y = %d$ vào vế trái:" % (x0, y0) +
                 "\\\\\n"
                 r"$%s + %s %s %d = %d \ne 0$,"
                 % (_tich7(a, x0), _tich7(b, y0), dau_c, abs(c), tu) +
                 "\\\\\n"
                 r"nên toạ độ của $A$ không thoả mãn phương trình của "
                 r"$\Delta$."),
                (r"{Điểm $A$ nằm trên đường thẳng $\Delta$}",
                 r"Sai. Thay toạ độ $A$ vào vế trái được $%d \ne 0$ nên "
                 r"$A \notin \Delta$." % tu),
            ],
            # c) VD - phải dùng công thức khoảng cách
            [
                (r"{\True Khoảng cách từ $A$ đến $\Delta$ bằng $%s$}"
                 % _xx7(d),
                 r"Đúng. $d\left(A;\ \Delta\right) = "
                 r"\dfrac{\left|ax_0 + by_0 + c\right|}{\sqrt{a^2+b^2}}$."
                 "\\\\\n"
                 r"$= \dfrac{\left|%d\right|}{\sqrt{%d^2 + %d^2}} = "
                 r"\dfrac{%d}{%d} = %s$." % (tu, a, b, abs(tu), n, _xx7(d))),
                (r"{Khoảng cách từ $A$ đến $\Delta$ bằng $%s$}"
                 % _xx7(abs(tu)),
                 r"Sai. $%d$ mới chỉ là tử số $\left|ax_0+by_0+c\right|$, "
                 r"còn thiếu bước chia cho $\sqrt{a^2+b^2} = %d$."
                 % (abs(tu), n)),
            ],
            # d) VDC - tự nhận ra bán kính chính là khoảng cách
            [
                (r"{\True Đường tròn tâm $A$ và tiếp xúc với $\Delta$ có "
                 r"bán kính bằng $%s$}" % _xx7(d),
                 r"Đúng. Đường tròn tiếp xúc với $\Delta$ khi và chỉ khi "
                 r"$\Delta$ có đúng một điểm chung với đường tròn, tức là "
                 r"$d\left(A;\ \Delta\right) = R$."
                 "\\\\\n"
                 r"Vậy $R = %s$, và phương trình đường tròn đó là"
                 % _xx7(d) +
                 "\\\\\n"
                 r"$\left(x %s %d\right)^2 + \left(y %s %d\right)^2 = %s$."
                 % ("-" if x0 >= 0 else "+", abs(x0),
                    "-" if y0 >= 0 else "+", abs(y0), _xx7(d * d, 4))),
                (r"{Đường tròn tâm $A$ và tiếp xúc với $\Delta$ có bán "
                 r"kính bằng $%s$}" % _xx7(2 * d),
                 r"Sai. Tiếp xúc nghĩa là bán kính bằng ĐÚNG khoảng cách "
                 r"từ tâm tới đường thẳng, tức $R = %s$; lấy $%s$ thì "
                 r"đường tròn sẽ cắt $\Delta$ tại hai điểm."
                 % (_xx7(d), _xx7(2 * d))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L10_C7_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - đường tròn trong mặt phẳng toạ độ; ba đường conic.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u, v, R = random.choice(PYTAGO7)
        p = random.randint(-5, 5)
        # tâm phải GẦN trục hoành hơn bán kính để (C) cắt Ox tại 2 điểm
        q = random.randint(-(R - 1), R - 1)
        if q == 0:                     # tâm nằm ngay trên Ox thì ý d) nhạt
            continue
        A, B, c = _bo_elip()
        bo = (p, q, u, v, R, A, B, c)
        if bo not in gt:
            gt.append(bo)

    cauTF = ''
    for p, q, u, v, R, A, B, c in gt:
        xM, yM = p + u, q + v          # M thuộc (C) vì u^2 + v^2 = R^2
        # tiếp tuyến tại M: vectơ pháp tuyến IM = (u; v)
        tu7, tv7, ct = _rut_gon7(u, v, -(u * xM + v * yM))
        # đường thẳng IM kéo dài - dùng làm phương án SAI
        sa7, sb7, sc7 = _rut_gon7(-v, u, v * xM - u * yM)
        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho đường tròn "
                 r"$\left(C\right): %s$ và elip "
                 r"$\left(E\right): \dfrac{x^2}{%d} + \dfrac{y^2}{%d} = 1$."
                 % (_pt_duong_tron(p, q, R), A * A, B * B))

        ds_abcd = (
            # a) NB - đọc tâm và bán kính từ dạng chính tắc
            [
                (r"{\True Đường tròn $\left(C\right)$ có tâm $I%s$ và bán "
                 r"kính $R = %d$}" % (_toado7(p, q), R),
                 r"Đúng. Dạng $\left(x-a\right)^2 + \left(y-b\right)^2 = "
                 r"R^2$ cho tâm $I\left(a;\ b\right)$ và bán kính $R$; ở "
                 r"đây $R^2 = %d$ nên $R = %d$." % (R * R, R)),
                (r"{Đường tròn $\left(C\right)$ có tâm $I%s$ và bán kính "
                 r"$R = %d$}" % (_toado7(-p, -q), R * R),
                 r"Sai. Hai chỗ đều nhầm dấu và nhầm bậc: tâm là $%s$ "
                 r"(đổi dấu số trong ngoặc) và $R = \sqrt{%d} = %d$."
                 % (_toado7(p, q), R * R, R)),
            ],
            # b) TH - một phép tính c^2 = a^2 - b^2
            [
                (r"{\True Elip $\left(E\right)$ có tiêu cự bằng $%d$}"
                 % (2 * c),
                 r"Đúng. Với $\left(E\right): \dfrac{x^2}{a^2} + "
                 r"\dfrac{y^2}{b^2} = 1$ ta có $a = %d$, $b = %d$ và"
                 % (A, B) +
                 "\\\\\n"
                 r"$c^2 = a^2 - b^2 = %d - %d = %d \Rightarrow c = %d$."
                 % (A * A, B * B, c * c, c) +
                 "\\\\\n"
                 r"Tiêu cự là $F_1F_2 = 2c = %d$." % (2 * c)),
                (r"{Elip $\left(E\right)$ có tiêu cự bằng $%d$}" % c,
                 r"Sai. $c = %d$ mới là NỬA tiêu cự; tiêu cự là "
                 r"$2c = %d$." % (c, 2 * c)),
            ],
            # c) VD - phải thấy IM là vectơ pháp tuyến của tiếp tuyến
            [
                (r"{\True Tiếp tuyến của $\left(C\right)$ tại điểm "
                 r"$M%s$ có phương trình $%s$}"
                 % (_toado7(xM, yM), _pt_duong_thang(tu7, tv7, ct)),
                 r"Đúng. Trước hết $M \in \left(C\right)$ vì "
                 r"$\left(%d\right)^2 + \left(%d\right)^2 = %d = R^2$."
                 % (u, v, R * R) +
                 "\\\\\n"
                 r"Tiếp tuyến tại $M$ vuông góc với bán kính $IM$, nên "
                 r"nhận $\overrightarrow{IM} = %s$ (rút gọn thành $%s$) "
                 r"làm vectơ pháp tuyến:"
                 % (_toado7(u, v), _toado7(tu7, tv7)) +
                 "\\\\\n"
                 r"$%s \Leftrightarrow %s$."
                 % (_khai_trien7(tu7, tv7, xM, yM),
                    _pt_duong_thang(tu7, tv7, ct))),
                (r"{Tiếp tuyến của $\left(C\right)$ tại điểm $M%s$ có "
                 r"phương trình $%s$}"
                 % (_toado7(xM, yM), _pt_duong_thang(sa7, sb7, sc7)),
                 r"Sai. Đó là đường thẳng $IM$ kéo dài chứ không phải "
                 r"tiếp tuyến: nó nhận $%s$ làm vectơ pháp tuyến, tức là "
                 r"VUÔNG GÓC với tiếp tuyến cần tìm."
                 % _toado7(sa7, sb7)),
            ],
            # d) VDC - phải tự so sánh khoảng cách tâm - trục với bán kính
            [
                (r"{\True Đường tròn $\left(C\right)$ cắt trục hoành tại "
                 r"hai điểm phân biệt}",
                 r"Đúng. Trục hoành là đường thẳng $y = 0$, khoảng cách "
                 r"từ tâm $I%s$ tới nó bằng $\left|%d\right| = %d$."
                 % (_toado7(p, q), q, abs(q)) +
                 "\\\\\n"
                 r"Vì $%d < %d = R$ nên đường thẳng cắt đường tròn tại "
                 r"hai điểm phân biệt." % (abs(q), R) +
                 "\\\\\n"
                 r"Kiểm lại bằng đại số: cho $y = 0$ thì "
                 r"$\left(x %s %d\right)^2 = %d - %d = %d > 0$, "
                 r"phương trình có hai nghiệm $x$ phân biệt."
                 % ("-" if p >= 0 else "+", abs(p), R * R, q * q,
                    R * R - q * q)),
                (r"{Đường tròn $\left(C\right)$ không có điểm chung với "
                 r"trục hoành}",
                 r"Sai. Muốn không có điểm chung thì phải có "
                 r"$d\left(I;\ Ox\right) > R$, trong khi ở đây "
                 r"$\left|%d\right| = %d < %d = R$."
                 % (q, abs(q), R)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


# =====================================================================
# BỔ SUNG 29/09/2026 - các yêu cầu cần đạt mức VD còn thiếu dạng SA/TL
# (Blueprint hệ số 1 gọi tới nhưng Mapping chưa khai, nên đề bị chèn
#  ô trống). Thứ tự theo bài 19 -> 22.
# CLAUDE THEM 29/09/2026 - co Lan kiem tra lai noi dung toan.
# =====================================================================

def L10_C7_B19_VD107_SA_A_01(socau):
    r"""Lập phương trình đường thẳng song song - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đáp số NGUYÊN: hệ số tự do $m$ của đường thẳng song song.
    """
    gt = []
    while len(gt) < socau:
        a, b = random.choice([(1, 2), (2, 1), (3, -2), (2, -3),
                              (1, -1), (3, 1), (1, 3), (2, 3)])
        c = random.randint(-6, 6)
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        m = -(a * x0 + b * y0)
        if m != c and (a, b, c, x0, y0) not in gt:
            gt.append((a, b, c, x0, y0))

    cau = ""
    for a, b, c, x0, y0 in gt:
        m = -(a * x0 + b * y0)
        debai = (r"Đường thẳng $d$ đi qua điểm $M%s$ và song song với đường "
                 r"thẳng $\Delta: %s$ có phương trình dạng $%s + m = 0$. "
                 r"Tìm $m$."
                 % (_toado7(x0, y0), _pt_duong_thang(a, b, c),
                    _pt_duong_thang(a, b, 0)[:-4].strip()))
        giai = (r"Vì $d \parallel \Delta$ nên $d$ nhận cùng vectơ pháp "
                r"tuyến $\overrightarrow{n} = %s$ với $\Delta$."
                % _toado7(a, b) +
                "\\\\\n"
                r"Do đó $d$ có dạng $%s + m = 0$."
                % _pt_duong_thang(a, b, 0)[:-4].strip() +
                "\\\\\n"
                r"Thay toạ độ $M%s$ vào: $%s %s + m = 0$."
                % (_toado7(x0, y0), _tich7(a, x0), _cong_tich7(b, y0)) +
                "\\\\\n"
                r"$%s + m = 0 \Rightarrow m = %d$."
                % (a * x0 + b * y0, m) +
                "\\\\\n"
                r"Kiểm lại $m = %d \neq %d$ nên $d$ thật sự song song với "
                r"$\Delta$ (không trùng)." % (m, c))
        nhieu = _ba_nhieu7(str(m), [str(-m), str(c), "0"],
                           buoc=lambda t: str(m + t))
        cau += MC_SA_answer_const(debai, str(m), nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B20_VD109_TL_A_01(socau, dong=1):
    r"""Tự luận: vị trí tương đối, tham số và khoảng cách.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Pháp tuyến lấy từ bộ ba Pytago nên khoảng cách ra SỐ HỮU TỈ đẹp.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10),
                                 (8, 6, 10)])
        c = random.randint(-8, 8)
        x0 = random.randint(-5, 5)
        y0 = random.randint(-5, 5)
        if a * x0 + b * y0 + c == 0:
            continue
        if (a, b, c, x0, y0) not in gt:
            gt.append((a, b, c, x0, y0))

    cauTN = ""
    for a, b, c, x0, y0 in gt:
        # d2 vuông góc d1, đi qua gốc toạ độ
        a2, b2 = -b, a
        tu = abs(a * x0 + b * y0 + c)
        kc = Fraction(tu, n)
        m = -(a * x0 + b * y0)          # để d3: ax + by + m = 0 qua M
        debai = (r"Trong mặt phẳng toạ độ $Oxy$ cho đường thẳng "
                 r"$d_1: %s$, đường thẳng $d_2: %s$ và điểm $M%s$."
                 % (_pt_duong_thang(a, b, c), _pt_duong_thang(a2, b2, 0),
                    _toado7(x0, y0)))

        hoi_a = r"Xét vị trí tương đối của $d_1$ và $d_2$."
        giai_a = (r"$d_1$ có vectơ pháp tuyến $\overrightarrow{n_1} = %s$, "
                  r"$d_2$ có $\overrightarrow{n_2} = %s$."
                  % (_toado7(a, b), _toado7(a2, b2)) +
                  "\\\\\n"
                  r"$\overrightarrow{n_1}\cdot\overrightarrow{n_2} = "
                  r"%s + %s = 0$."
                  % (_tich7(a, a2), _tich7(b, b2)) +
                  "\\\\\n"
                  r"Tích vô hướng bằng $0$ nên $d_1 \perp d_2$; hai đường "
                  r"thẳng cắt nhau và vuông góc với nhau.")

        hoi_b = (r"Viết phương trình đường thẳng $d_3$ đi qua $M$ và song "
                 r"song với $d_1$.")
        giai_b = (r"$d_3 \parallel d_1$ nên $d_3: %s + m = 0$."
                  % _pt_duong_thang(a, b, 0)[:-4].strip() +
                  "\\\\\n"
                  r"Thay $M%s$: $%s %s + m = 0 \Rightarrow m = %d$."
                  % (_toado7(x0, y0), _tich7(a, x0), _cong_tich7(b, y0), m) +
                  "\\\\\n"
                  r"Vậy $d_3: %s$." % _pt_duong_thang(a, b, m))

        hoi_c = r"Tính khoảng cách từ $M$ đến $d_1$."
        giai_c = (r"$d\left(M, d_1\right) = \dfrac{\left|%s %s %s\right|}"
                  r"{\sqrt{%d^2 + %d^2}}$."
                  % (_tich7(a, x0), _cong_tich7(b, y0),
                     ("+ %d" % c) if c >= 0 else ("- %d" % (-c)), a, b) +
                  "\\\\\n"
                  r"$= \dfrac{%d}{\sqrt{%d}} = \dfrac{%d}{%d} = %s$."
                  % (tu, a * a + b * b, tu, n, _xx7(float(kc), 4)))

        ds_abcd = [(hoi_a, r"d_1 \perp d_2", giai_a),
                   (hoi_b, r"d_3: %s" % _pt_duong_thang(a, b, m), giai_b),
                   (hoi_c, r"d\left(M, d_1\right) = \dfrac{%d}{%d}"
                    % (kc.numerator, kc.denominator), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C7_B21_VD113_SA_A_01(socau):
    r"""Đường tròn đi qua ba điểm - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        bo = _ba_diem_duong_tron()
        if bo is None:
            continue
        a, b, R, diem = bo
        if (a, b, R, tuple(diem)) not in [(x[0], x[1], x[2], tuple(x[3]))
                                          for x in gt]:
            gt.append((a, b, R, diem))

    cau = ""
    for a, b, R, diem in gt:
        kq = a + b + R
        (x1, y1), (x2, y2), (x3, y3) = diem
        debai = (r"Đường tròn đi qua ba điểm $A%s$, $B%s$, $C%s$ có tâm "
                 r"$I\left(a;\ b\right)$ và bán kính $R$. Tính $a + b + R$."
                 % (_toado7(x1, y1), _toado7(x2, y2), _toado7(x3, y3)))
        giai = (r"Gọi phương trình đường tròn là "
                r"$x^2 + y^2 - 2ax - 2by + c = 0$." +
                "\\\\\n"
                r"Thay lần lượt toạ độ $A$, $B$, $C$ vào ta được hệ ba "
                r"phương trình bậc nhất ba ẩn $a$, $b$, $c$." +
                "\\\\\n"
                r"Giải hệ được $a = %d$, $b = %d$, $c = %d$."
                % (a, b, a * a + b * b - R * R) +
                "\\\\\n"
                r"Bán kính $R = \sqrt{a^2 + b^2 - c} = "
                r"\sqrt{%d} = %d$." % (R * R, R) +
                "\\\\\n"
                r"Vậy $a + b + R = %d %s %s = %d$."
                % (a, ("+ %d" % b) if b >= 0 else ("- %d" % (-b)),
                   "+ %d" % R, kq) +
                "\\\\\n"
                r"Kiểm lại: $IA = IB = IC = %d$." % R)
        nhieu = _ba_nhieu7(str(kq), [str(a + b), str(R), str(a + b - R)],
                           buoc=lambda t: str(kq + t))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B21_VD114_TL_A_01(socau, dong=1):
    r"""Tự luận: đường tròn tiếp xúc với một đường thẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Pháp tuyến lấy từ bộ ba Pytago nên bán kính ra SỐ HỮU TỈ đẹp.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10),
                                 (8, 6, 10)])
        xi = random.randint(-4, 4)
        yi = random.randint(-4, 4)
        # chọn c sao cho khoảng cách là SỐ NGUYÊN
        R = random.randint(1, 5)
        c = R * n - (a * xi + b * yi)
        if (a, b, c, xi, yi) not in gt:
            gt.append((a, b, c, xi, yi))

    cauTN = ""
    for a, b, c, xi, yi in gt:
        n = int(round(math.sqrt(a * a + b * b)))
        tu = abs(a * xi + b * yi + c)
        R = tu // n
        debai = (r"Trong mặt phẳng toạ độ $Oxy$ cho điểm $I%s$ và đường "
                 r"thẳng $\Delta: %s$."
                 % (_toado7(xi, yi), _pt_duong_thang(a, b, c)))

        hoi_a = r"Tính khoảng cách từ $I$ đến $\Delta$."
        giai_a = (r"$d\left(I, \Delta\right) = \dfrac{\left|%s %s %s"
                  r"\right|}{\sqrt{%d^2 + %d^2}} = \dfrac{%d}{%d} = %d$."
                  % (_tich7(a, xi), _cong_tich7(b, yi),
                     ("+ %d" % c) if c >= 0 else ("- %d" % (-c)),
                     a, b, tu, n, R))

        hoi_b = (r"Viết phương trình đường tròn $\left(C\right)$ có tâm $I$ "
                 r"và tiếp xúc với $\Delta$.")
        giai_b = (r"Đường tròn tiếp xúc với $\Delta$ nên bán kính bằng "
                  r"đúng khoảng cách từ tâm đến $\Delta$: $R = %d$." % R +
                  "\\\\\n"
                  r"Vậy $\left(C\right): %s$." % _pt_duong_tron(xi, yi, R))

        hoi_c = (r"Điểm $O\left(0;\ 0\right)$ nằm trong, nằm trên hay nằm "
                 r"ngoài đường tròn $\left(C\right)$?")
        d2 = xi * xi + yi * yi
        vt = ("nằm trong" if d2 < R * R else
              ("nằm trên" if d2 == R * R else "nằm ngoài"))
        giai_c = (r"$IO^2 = %s + %s = %d$ còn $R^2 = %d$."
                  % (_tich7(xi, xi), _tich7(yi, yi), d2, R * R) +
                  "\\\\\n"
                  r"Vì $%d %s %d$ nên $O$ %s đường tròn."
                  % (d2, "<" if d2 < R * R else ("=" if d2 == R * R else ">"),
                     R * R, vt))

        ds_abcd = [(hoi_a, r"d\left(I, \Delta\right) = %d" % R, giai_a),
                   (hoi_b, r"%s" % _pt_duong_tron(xi, yi, R), giai_b),
                   (hoi_c, r"O \text{ %s đường tròn}" % vt, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C7_B21_VD117_SA_A_01(socau):
    r"""Bài toán thực tiễn về đường tròn - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(-6, 6)
        b = random.randint(-6, 6)
        R = random.choice([3, 4, 5, 6, 7, 8, 10])
        if (a, b, R) not in gt:
            gt.append((a, b, R))

    cau = ""
    for a, b, R in gt:
        c = a * a + b * b - R * R
        debai = (r"Một trạm phát sóng đặt tại vị trí $I%s$ (đơn vị: km) "
                 r"phủ sóng trong bán kính $%d$ km. Ranh giới vùng phủ "
                 r"sóng là đường tròn có phương trình "
                 r"$x^2 + y^2 - 2ax - 2by + c = 0$. Tính $c$."
                 % (_toado7(a, b), R))
        giai = (r"Ranh giới vùng phủ sóng là đường tròn tâm $I%s$, bán "
                r"kính $R = %d$." % (_toado7(a, b), R) +
                "\\\\\n"
                r"Phương trình dạng khai triển: $x^2 + y^2 - 2ax - 2by "
                r"+ c = 0$ với $c = a^2 + b^2 - R^2$." +
                "\\\\\n"
                r"$c = %s + %s - %d^2 = %d$."
                % (_tich7(a, a), _tich7(b, b), R, c) +
                "\\\\\n"
                r"Kiểm lại: $\sqrt{a^2 + b^2 - c} = \sqrt{%d} = %d = R$."
                % (R * R, R))
        nhieu = _ba_nhieu7(str(c), [str(-c), str(a * a + b * b), str(R * R)],
                           buoc=lambda t: str(c + t))
        cau += MC_SA_answer_const(debai, str(c), nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B22_VD123_SA_A_01(socau):
    r"""Bài toán thực tiễn về elip - trả lời ngắn (đáp số THẬP PHÂN HỮU HẠN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chọn $\left(a, x_0, k\right)$ là bộ ba Pytago với $a \in \{5, 10, 20,
    25\}$ để $\dfrac{bk}{a}$ luôn viết được thành số thập phân hữu hạn.
    """
    BO = [(5, 3, 4), (5, 4, 3), (10, 6, 8), (10, 8, 6),
          (20, 12, 16), (20, 16, 12), (25, 7, 24), (25, 24, 7),
          (25, 15, 20), (25, 20, 15)]
    gt = []
    while len(gt) < socau:
        a, x0, k = random.choice(BO)
        b = random.randint(2, a - 1)
        if (a, x0, k, b) not in gt:
            gt.append((a, x0, k, b))

    cau = ""
    for a, x0, k, b in gt:
        h = Fraction(b * k, a)
        dapso = _xx7(float(h), 6)
        debai = (r"Một cổng vòm có dạng nửa elip với chiều rộng đáy bằng "
                 r"$%d$ m và chiều cao ở giữa bằng $%d$ m. Tính chiều cao "
                 r"của cổng tại vị trí cách tâm đáy $%d$ m (đơn vị: m)."
                 % (2 * a, b, x0))
        giai = (r"Chọn hệ trục $Oxy$ với $O$ là tâm đáy cổng, trục $Ox$ "
                r"nằm trên đáy." +
                "\\\\\n"
                r"Nửa elip có phương trình $\dfrac{x^2}{%d^2} + "
                r"\dfrac{y^2}{%d^2} = 1$ với $y \geq 0$." % (a, b) +
                "\\\\\n"
                r"Thay $x = %d$: $\dfrac{%d}{%d} + \dfrac{y^2}{%d} = 1$."
                % (x0, x0 * x0, a * a, b * b) +
                "\\\\\n"
                r"$\dfrac{y^2}{%d} = \dfrac{%d}{%d} \Rightarrow "
                r"y^2 = \dfrac{%d}{%d}$."
                % (b * b, a * a - x0 * x0, a * a,
                   b * b * (a * a - x0 * x0), a * a) +
                "\\\\\n"
                r"$y = \dfrac{%d\cdot %d}{%d} = %s$ (m)."
                % (b, k, a, dapso))
        nhieu = _ba_nhieu7(dapso, [str(b), str(x0), _xx7(float(h) / 2, 6)],
                           buoc=lambda t: _xx7(float(h) + t, 6))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L10_C7_B22_VD124_SA_A_01(socau):
    r"""Bài toán thực tiễn tổng hợp về toạ độ - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Pháp tuyến lấy từ bộ ba Pytago có cạnh huyền $5$ hoặc $10$ nên
    khoảng cách luôn là số thập phân hữu hạn.
    """
    gt = []
    while len(gt) < socau:
        a, b, n = random.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10),
                                 (8, 6, 10)])
        c = random.randint(-10, 10)
        x0 = random.randint(-8, 8)
        y0 = random.randint(-8, 8)
        if a * x0 + b * y0 + c == 0:
            continue
        if (a, b, c, x0, y0) not in gt:
            gt.append((a, b, c, x0, y0))

    cau = ""
    for a, b, c, x0, y0 in gt:
        n = int(round(math.sqrt(a * a + b * b)))
        tu = abs(a * x0 + b * y0 + c)
        kc = Fraction(tu, n)
        dapso = _xx7(float(kc), 6)
        debai = (r"Một con tàu chạy thẳng theo đường có phương trình "
                 r"$%s$ trong hệ toạ độ $Oxy$ (đơn vị: km). Một hòn đảo "
                 r"nằm ở vị trí $M%s$. Tính khoảng cách ngắn nhất từ hòn "
                 r"đảo đến đường đi của tàu (đơn vị: km)."
                 % (_pt_duong_thang(a, b, c), _toado7(x0, y0)))
        giai = (r"Khoảng cách ngắn nhất từ $M$ đến đường đi của tàu chính "
                r"là khoảng cách từ điểm $M$ đến đường thẳng đó." +
                "\\\\\n"
                r"$d = \dfrac{\left|%s %s %s\right|}{\sqrt{%d^2 + %d^2}}$."
                % (_tich7(a, x0), _cong_tich7(b, y0),
                   ("+ %d" % c) if c >= 0 else ("- %d" % (-c)), a, b) +
                "\\\\\n"
                r"$= \dfrac{%d}{\sqrt{%d}} = \dfrac{%d}{%d} = %s$ (km)."
                % (tu, a * a + b * b, tu, n, dapso))
        nhieu = _ba_nhieu7(dapso, [str(tu), str(n), _xx7(float(kc) * 2, 6)],
                           buoc=lambda t: _xx7(float(kc) + t, 6))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau
