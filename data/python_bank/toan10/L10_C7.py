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
        if a == 0 and b == 0:
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
        if u1 == 0 and u2 == 0:
            continue
        if (x0, y0, u1, u2) not in gt:
            gt.append((x0, y0, u1, u2))

    cauTN = ""
    for x0, y0, u1, u2 in gt:
        def _pt(px, py, vx, vy):
            return (r"$\begin{cases} x = %d %s %dt \\ y = %d %s %dt "
                    r"\end{cases}$"
                    % (px, "+" if vx >= 0 else "-", abs(vx),
                       py, "+" if vy >= 0 else "-", abs(vy)))
        dung = _pt(x0, y0, u1, u2)
        nhieu = [_pt(u1, u2, x0, y0), _pt(x0, y0, u2, u1),
                 _pt(-x0, -y0, u1, u2), _pt(x0, y0, -u1, -u2)]
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
        if a == 0 and b == 0:
            continue
        if (x0, y0, a, b) not in gt:
            gt.append((x0, y0, a, b))

    cauTN = ""
    for x0, y0, a, b in gt:
        c = -(a * x0 + b * y0)
        dung = r"$%s$" % _pt_duong_thang(a, b, c)
        nhieu = [r"$%s$" % _pt_duong_thang(a, b, -c),
                 r"$%s$" % _pt_duong_thang(b, a, c),
                 r"$%s$" % _pt_duong_thang(-b, a, c),
                 r"$%s$" % _pt_duong_thang(a, b, c + 1)]
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
                r"$%d\left(x %s %d\right) + %d\left(y %s %d\right) = 0$"
                % (a, "-" if x0 >= 0 else "+", abs(x0),
                   b, "-" if y0 >= 0 else "+", abs(y0)) +
                "\\\\\n"
                r"Khai triển và thu gọn: $%s$." % _pt_duong_thang(a, b, c) +
                "\\\\\n"
                r"Kiểm lại: thay $M%s$ vào vế trái được "
                r"$%d\cdot %d + %d\cdot %d %s %d = 0$."
                % (_toado7(x0, y0), a, x0, b, y0,
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
        nhieu = [r"$%s$" % _pt_duong_thang(u1, u2, -(u1 * xa + u2 * ya)),
                 r"$%s$" % _pt_duong_thang(a, b, -c),
                 r"$%s$" % _pt_duong_thang(-a, b, c),
                 r"$%s$" % _pt_duong_thang(a, b, c + 2)]
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
                r"$%d\left(x %s %d\right) + %d\left(y %s %d\right) = 0 "
                r"\Leftrightarrow %s$."
                % (a, "-" if xa >= 0 else "+", abs(xa),
                   b, "-" if ya >= 0 else "+", abs(ya),
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
        nhieu = [r"$%s$" % _pt_duong_thang(k, 1, m),
                 r"$%s$" % _pt_duong_thang(k, -1, -m),
                 r"$%s$" % _pt_duong_thang(1, -k, m),
                 r"$%s$" % _pt_duong_thang(-k, -1, m)]
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
        # chọn B sao cho trung điểm có toạ độ nguyên
        xb = xa + 2 * random.randint(-3, 3)
        yb = ya + 2 * random.randint(-3, 3)
        if (xa, ya) == (xb, yb):
            continue
        if (xa, ya, xb, yb) not in gt:
            gt.append((xa, ya, xb, yb))

    cauTN = ""
    for xa, ya, xb, yb in gt:
        xm, ym = (xa + xb) // 2, (ya + yb) // 2
        a, b = xb - xa, yb - ya          # pháp tuyến của trung trực
        c = -(a * xm + b * ym)
        dung = r"$%s$" % _pt_duong_thang(a, b, c)
        nhieu = [r"$%s$" % _pt_duong_thang(a, b, -(a * xa + b * ya)),
                 r"$%s$" % _pt_duong_thang(-b, a, -(-b * xm + a * ym)),
                 r"$%s$" % _pt_duong_thang(a, b, -c),
                 r"$%s$" % _pt_duong_thang(a, b, c + 2)]
        debai = (r"Lập phương trình đường trung trực của đoạn thẳng $AB$ với "
                 r"$A%s$ và $B%s$." % (_toado7(xa, ya), _toado7(xb, yb)))
        giai = (r"Đường trung trực của $AB$ đi qua \textbf{trung điểm} $M$ "
                r"của $AB$ và \textbf{vuông góc} với $AB$."
                "\\\\\n"
                r"Trung điểm: $M\left(\dfrac{%d + %d}{2};\ "
                r"\dfrac{%d + %d}{2}\right) = M%s$."
                % (xa, xb, ya, yb, _toado7(xm, ym)) +
                "\\\\\n"
                r"Vì trung trực vuông góc với $AB$ nên nhận "
                r"$\overrightarrow{AB} = %s$ làm \textbf{vectơ pháp tuyến}."
                % _toado7(a, b) +
                "\\\\\n"
                r"Phương trình: $%d\left(x %s %d\right) + "
                r"%d\left(y %s %d\right) = 0 \Leftrightarrow %s$."
                % (a, "-" if xm >= 0 else "+", abs(xm),
                   b, "-" if ym >= 0 else "+", abs(ym),
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
        a, b = u2, -u1
        c = -(a * xa + b * ya)
        xm, ym = (xa + xb) // 2, (ya + yb) // 2
        a2, b2 = u1, u2
        c2 = -(a2 * xm + b2 * ym)

        debai = (r"Trong mặt phẳng toạ độ $Oxy$, cho hai điểm $A%s$ và $B%s$."
                 % (_toado7(xa, ya), _toado7(xb, yb)))

        hoi_a = r"Lập phương trình tổng quát của đường thẳng $AB$."
        giai_a = (r"$\overrightarrow{AB} = %s$ là vectơ chỉ phương, nên vectơ "
                  r"pháp tuyến là $\overrightarrow{n} = %s$."
                  % (_toado7(u1, u2), _toado7(a, b)) +
                  "\\\\\n"
                  r"Đường thẳng qua $A%s$: $%s$."
                  % (_toado7(xa, ya), _pt_duong_thang(a, b, c)))

        hoi_b = r"Tìm toạ độ trung điểm $M$ của đoạn thẳng $AB$."
        giai_b = (r"$M\left(\dfrac{x_A + x_B}{2};\ "
                  r"\dfrac{y_A + y_B}{2}\right) = M%s$." % _toado7(xm, ym))

        hoi_c = r"Lập phương trình đường trung trực của đoạn thẳng $AB$."
        giai_c = (r"Đường trung trực đi qua $M%s$ và vuông góc với $AB$, nên "
                  r"nhận $\overrightarrow{AB} = %s$ làm vectơ pháp tuyến."
                  % (_toado7(xm, ym), _toado7(a2, b2)) +
                  "\\\\\n"
                  r"$%d\left(x %s %d\right) + %d\left(y %s %d\right) = 0 "
                  r"\Leftrightarrow %s$."
                  % (a2, "-" if xm >= 0 else "+", abs(xm),
                     b2, "-" if ym >= 0 else "+", abs(ym),
                     _pt_duong_thang(a2, b2, c2)))

        ds_abcd = [(hoi_a, _pt_duong_thang(a, b, c), giai_a),
                   (hoi_b, r"M\left(%d;\ %d\right)" % (xm, ym), giai_b),
                   (hoi_c, _pt_duong_thang(a2, b2, c2), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN
