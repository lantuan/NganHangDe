# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 2. Dãy số. Cấp số cộng và cấp số nhân
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Công thức dùng trong tệp (đúng SGK KNTT lớp 11):

  * Cấp số cộng: $u_n = u_1 + (n-1)d$;
    $S_n = \dfrac{n\left(u_1 + u_n\right)}{2}
         = \dfrac{n\left[2u_1 + (n-1)d\right]}{2}$.
  * Cấp số nhân: $u_n = u_1q^{\,n-1}$;
    $S_n = u_1\dfrac{1 - q^{\,n}}{1 - q}$ với $q \ne 1$.

Số liệu chọn để ĐÁP SỐ ĐẸP: $u_1$, $d$, $q$ đều nguyên; với cấp số nhân
chỉ dùng $q$ nguyên ($\pm 2$, $3$, $\pm 1/2$ khi cần số thập phân) nên
mọi số hạng và mọi tổng đều viết được chính xác - câu trả lời ngắn chấm
bằng SO KHỚP CHUỖI.

Bài học từ lớp 10 (docs/16_CHANGELOG Version 3.14) đã áp dụng:
chữ tiếng Việt không bao giờ nằm trần trong $...$; không dùng chữ đậm
kiểu Markdown; mọi chuỗi có dấu gạch chéo đều là chuỗi r"..."; mọi danh
sách phương án nhiễu đều đi qua _ba_nhieu2.
"""
import math
import random

from math_type import *          # noqa: F401,F403
from DefChung import ngoac       # so am lam co so luy thua phai co ngoac

DAU_THAP_PHAN = ","


def _xx(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết theo cách viết Việt Nam."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu2(dapso, ung_vien, buoc=None):
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
    """'+ 3' hoặc '- 3' để ghép vào biểu thức."""
    return ("+ %s" % _xx(abs(x))) if x >= 0 else ("- %s" % _xx(abs(x)))


def _csc(u1, d, n):
    return u1 + (n - 1) * d


def _tong_csc(u1, d, n):
    return n * (2 * u1 + (n - 1) * d) // 2


def _csn(u1, q, n):
    return u1 * q ** (n - 1)


def _tong_csn(u1, q, n):
    if q == 1:
        return u1 * n
    return u1 * (1 - q ** n) // (1 - q)


def _liet_ke(ds):
    return r"$%s$" % r"$; $".join(_xx(x) for x in ds)


def _bo_csc():
    """(u1, d) nguyên, d khác 0."""
    while True:
        u1 = random.randint(-9, 12)
        d = random.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
        if d:
            return u1, d


def _bo_csn():
    """(u1, q) nguyên, |q| >= 2 để dãy tăng/giảm rõ."""
    u1 = random.choice([1, 2, 3, 4, 5, -2, -3])
    q = random.choice([2, 3, -2, -3])
    return u1, q


# =====================================================================
# BÀI 5. DÃY SỐ
# =====================================================================

def L11_C2_B5_NB029_MC_A_01(socau, dang=1):
    r"""Nhận biết dãy số hữu hạn và dãy số vô hạn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.randint(4, 7)
        u1 = random.randint(1, 9)
        d = random.randint(2, 6)
        if (k, u1, d) not in gt:
            gt.append((k, u1, d))

    cauTN = ""
    for k, u1, d in gt:
        ds = [u1 + i * d for i in range(k)]
        huu_han = random.choice([True, False])
        if huu_han:
            debai = (r"Cho dãy số $%s$. Dãy số này là dãy số hữu hạn hay vô "
                     r"hạn, và có bao nhiêu số hạng?"
                     % r"$; $".join(str(x) for x in ds))
            dung = "Dãy số hữu hạn, có %d số hạng." % k
            nhieu = _ba_nhieu2(
                dung,
                ["Dãy số vô hạn.",
                 "Dãy số hữu hạn, có %d số hạng." % (k + 1),
                 "Dãy số hữu hạn, có %d số hạng." % (k - 1)],
                buoc=lambda t: "Dãy số hữu hạn, có %d số hạng." % (k + t + 1))
            giai = (r"Dãy số được viết ra hết, đếm được $%d$ số hạng nên đây "
                    r"là \textbf{dãy số hữu hạn}." % k +
                    "\\\\\n"
                    r"Dãy số hữu hạn là dãy chỉ gồm hữu hạn số hạng, viết "
                    r"được đầy đủ từ $u_1$ đến $u_m$.")
        else:
            debai = (r"Cho dãy số $\left(u_n\right)$ với "
                     r"$u_n = %dn %s$, $n \in \mathbb{N}^{*}$. Dãy số này "
                     r"là dãy số hữu hạn hay vô hạn?" % (d, _dau(u1 - d)))
            dung = "Dãy số vô hạn."
            nhieu = _ba_nhieu2(
                dung,
                ["Dãy số hữu hạn, có %d số hạng." % k,
                 "Dãy số hữu hạn, có %d số hạng." % (k + 2),
                 "Không phải dãy số."],
                buoc=lambda t: "Dãy số hữu hạn, có %d số hạng." % (k + t + 2))
            giai = (r"Dãy số cho bởi công thức với $n$ chạy khắp "
                    r"$\mathbb{N}^{*}$ nên có vô số số hạng: đây là "
                    r"\textbf{dãy số vô hạn}."
                    "\\\\\n"
                    r"Ba số hạng đầu: $u_1 = %d$; $u_2 = %d$; $u_3 = %d$."
                    % (u1, u1 + d, u1 + 2 * d))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B5_TH030_MC_A_01(socau, dang=1):
    r"""Cho dãy số bằng công thức tổng quát, tìm một số hạng cụ thể.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([1, 2, 3, -1, -2])
        b = random.randint(-6, 6)
        c = random.randint(1, 5)
        k = random.randint(3, 6)
        v = (a, b, c, k)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, k in gt:
        def u(n):
            return a * n * n + b * n + c
        dung = r"$%d$" % u(k)
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % u(k + 1), r"$%d$" % u(k - 1),
             r"$%d$" % (a * k * k + b * k),          # quen hang tu tu do
             r"$%d$" % (a * k + b * k + c)],         # quen binh phuong
            buoc=lambda t: r"$%d$" % (u(k) + t))
        debai = (r"Cho dãy số $\left(u_n\right)$ với "
                 r"$u_n = %sn^2 %s n %s$. Tính $u_{%d}$."
                 % (("" if a == 1 else ("-" if a == -1 else "%d" % a)),
                    _dau(b), _dau(c), k))
        giai = (r"Thay $n = %d$ vào công thức tổng quát:" % k +
                "\\\\\n"
                r"$u_{%d} = %s\cdot %d^2 %s\cdot %d %s = %d$."
                % (k, ("" if a == 1 else ("-" if a == -1 else "%d" % a)),
                   k, _dau(b), k, _dau(c), u(k)) +
                "\\\\\n"
                r"Chú ý phải bình phương $n$ trước rồi mới nhân với hệ số.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B5_TH031_MC_A_01(socau, dang=1):
    r"""Tính chất tăng, giảm, bị chặn của dãy số.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        d = random.choice([-4, -3, -2, 2, 3, 4])
        u1 = random.randint(-8, 8)
        if (u1, d) not in gt:
            gt.append((u1, d))

    cauTN = ""
    for u1, d in gt:
        tang = d > 0
        dung = ("Dãy số tăng và bị chặn dưới." if tang
                else "Dãy số giảm và bị chặn trên.")
        nhieu = _ba_nhieu2(
            dung,
            ["Dãy số giảm và bị chặn trên." if tang
             else "Dãy số tăng và bị chặn dưới.",
             "Dãy số tăng và bị chặn trên." if tang
             else "Dãy số giảm và bị chặn dưới.",
             "Dãy số không tăng cũng không giảm."],
            buoc=lambda t: "Dãy số bị chặn (cả trên lẫn dưới).")
        debai = (r"Cho dãy số $\left(u_n\right)$ với $u_n = %dn %s$, "
                 r"$n \in \mathbb{N}^{*}$. Khẳng định nào sau đây đúng?"
                 % (d, _dau(u1 - d)))
        giai = (r"Xét hiệu hai số hạng liên tiếp:"
                "\\\\\n"
                r"$u_{n+1} - u_n = \left[%d(n+1) %s\right] - "
                r"\left[%dn %s\right] = %d$."
                % (d, _dau(u1 - d), d, _dau(u1 - d), d) +
                "\\\\\n"
                r"Vì $%d %s 0$ với mọi $n$ nên dãy số %s."
                % (d, ">" if tang else "<", "TĂNG" if tang else "GIẢM") +
                "\\\\\n" +
                (r"Dãy tăng thì mọi số hạng đều không nhỏ hơn $u_1 = %d$, "
                 r"nên dãy \textbf{bị chặn dưới} bởi $%d$; dãy không bị "
                 r"chặn trên vì $u_n \to +\infty$." % (u1, u1) if tang else
                 r"Dãy giảm thì mọi số hạng đều không lớn hơn $u_1 = %d$, "
                 r"nên dãy \textbf{bị chặn trên} bởi $%d$; dãy không bị "
                 r"chặn dưới vì $u_n \to -\infty$." % (u1, u1)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B5_TH031_SA_A_01(socau):
    r"""Số hạng thứ n của dãy cho bởi công thức - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([1, 2, 3])
        b = random.randint(-5, 5)
        k = random.randint(4, 9)
        v = (a, b, k)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, k in gt:
        gt_k = a * k * k + b
        debai = (r"Cho dãy số $\left(u_n\right)$ với $u_n = %sn^2 %s$. "
                 r"Tính $u_{%d}$."
                 % ("" if a == 1 else "%d" % a, _dau(b), k))
        giai = (r"$u_{%d} = %s\cdot %d^2 %s = %s\cdot %d %s = %d$."
                % (k, "" if a == 1 else "%d" % a, k, _dau(b),
                   "" if a == 1 else "%d" % a, k * k, _dau(b), gt_k))
        nhieu = _ba_nhieu2(str(gt_k),
                           [str(a * k * k), str(a * k + b), str(gt_k + 1)],
                           buoc=lambda t: str(gt_k + t + 1))
        cau += MC_SA_answer_const(debai, str(gt_k), nhieu, giai, 0, 0, 2)
    return cau


# =====================================================================
# BÀI 6. CẤP SỐ CỘNG
# =====================================================================

def L11_C2_B6_NB032_MC_A_01(socau, dang=1):
    r"""Nhận biết một dãy số là cấp số cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, d = _bo_csc()
        if (u1, d) not in gt:
            gt.append((u1, d))

    cauTN = ""
    for u1, d in gt:
        csc = [_csc(u1, d, i) for i in range(1, 5)]
        khong = list(csc)
        khong[2] += random.choice([1, -1, 2])
        q = random.choice([2, 3])
        csn = [u1 if u1 else 2]
        for _ in range(3):
            csn.append(csn[-1] * q)
        dung = _liet_ke(csc)
        nhieu = _ba_nhieu2(
            dung,
            [_liet_ke(khong), _liet_ke(csn),
             _liet_ke([x * x for x in range(1, 5)]),
             _liet_ke([u1, u1 + d, u1 + 3 * d, u1 + 6 * d])],
            buoc=lambda t: _liet_ke([u1 + t, u1 + d, u1 + 3 * d, u1 + 7 * d]))
        debai = r"Dãy số nào sau đây là một cấp số cộng?"
        giai = (r"Một dãy số là cấp số cộng khi hiệu hai số hạng liên tiếp "
                r"LUÔN bằng nhau."
                "\\\\\n"
                r"Với dãy %s: các hiệu lần lượt là $%d$; $%d$; $%d$ - đều "
                r"bằng nhau nên đây là cấp số cộng với công sai $d = %d$."
                % (dung, d, d, d, d) +
                "\\\\\n"
                r"Các dãy còn lại có hiệu hai số hạng liên tiếp thay đổi "
                r"nên không phải cấp số cộng.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B6_TH033_MC_A_01(socau, dang=1):
    r"""Số hạng tổng quát của cấp số cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, d = _bo_csc()
        k = random.randint(8, 25)
        if (u1, d, k) not in gt:
            gt.append((u1, d, k))

    cauTN = ""
    for u1, d, k in gt:
        uk = _csc(u1, d, k)
        dung = r"$%d$" % uk
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % (u1 + k * d),              # quen tru 1
             r"$%d$" % (u1 + (k - 2) * d),
             r"$%d$" % (u1 * d ** (k - 1) if abs(d) < 3 else u1 + k),
             r"$%d$" % (uk + d)],
            buoc=lambda t: r"$%d$" % (uk + t * d + 1))
        debai = (r"Cho cấp số cộng $\left(u_n\right)$ có $u_1 = %d$ và công "
                 r"sai $d = %d$. Tính $u_{%d}$." % (u1, d, k))
        giai = (r"Số hạng tổng quát của cấp số cộng: "
                r"$u_n = u_1 + \left(n - 1\right)d$."
                "\\\\\n"
                r"$u_{%d} = %d + \left(%d - 1\right)\cdot %d "
                r"= %d %s = %d$."
                % (k, u1, k, d, u1, _dau((k - 1) * d), uk) +
                "\\\\\n"
                r"Chú ý hệ số là $n - 1$ chứ không phải $n$: từ $u_1$ đến "
                r"$u_{%d}$ chỉ cộng thêm $d$ đúng $%d$ lần."
                % (k, k - 1))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B6_TH033_SA_A_01(socau):
    r"""Xác định công sai của cấp số cộng - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, d = _bo_csc()
        i = random.randint(3, 6)
        j = i + random.randint(2, 5)
        if (u1, d, i, j) not in gt:
            gt.append((u1, d, i, j))

    cau = ""
    for u1, d, i, j in gt:
        ui, uj = _csc(u1, d, i), _csc(u1, d, j)
        debai = (r"Cho cấp số cộng $\left(u_n\right)$ có $u_{%d} = %d$ và "
                 r"$u_{%d} = %d$. Tìm công sai $d$ của cấp số cộng đó."
                 % (i, ui, j, uj))
        giai = (r"$u_{%d} - u_{%d} = \left(%d - %d\right)d = %dd$."
                % (j, i, j, i, j - i) +
                "\\\\\n"
                r"$%d - \left(%d\right) = %d$ nên $%dd = %d$, suy ra "
                r"$d = %d$." % (uj, ui, uj - ui, j - i, uj - ui, d))
        nhieu = _ba_nhieu2(str(d), [str(uj - ui), str(-d), str(d + 1)],
                           buoc=lambda t: str(d + t + 1))
        cau += MC_SA_answer_const(debai, str(d), nhieu, giai, 0, 0, 2)
    return cau


def L11_C2_B6_TH034_MC_A_01(socau, dang=1):
    r"""Tổng n số hạng đầu tiên của cấp số cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, d = _bo_csc()
        n = random.choice([10, 12, 15, 16, 20])
        if (u1, d, n) not in gt:
            gt.append((u1, d, n))

    cauTN = ""
    for u1, d, n in gt:
        un = _csc(u1, d, n)
        S = _tong_csc(u1, d, n)
        dung = r"$%d$" % S
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % (n * (u1 + un)),                    # quen chia 2
             r"$%d$" % (n * (2 * u1 + n * d) // 2),        # dung n thay n-1
             r"$%d$" % un,
             r"$%d$" % (S + d)],
            buoc=lambda t: r"$%d$" % (S + t * n))
        debai = (r"Cho cấp số cộng $\left(u_n\right)$ có $u_1 = %d$ và công "
                 r"sai $d = %d$. Tính tổng $S_{%d}$ của $%d$ số hạng đầu "
                 r"tiên." % (u1, d, n, n))
        giai = (r"$u_{%d} = u_1 + \left(%d - 1\right)d = %d %s = %d$."
                % (n, n, u1, _dau((n - 1) * d), un) +
                "\\\\\n"
                r"$S_n = \dfrac{n\left(u_1 + u_n\right)}{2} "
                r"= \dfrac{%d\left(%d %s\right)}{2} = \dfrac{%d}{2} = %d$."
                % (n, u1, _dau(un), n * (u1 + un), S) +
                "\\\\\n"
                r"Cách khác: $S_n = \dfrac{n\left[2u_1 + "
                r"\left(n-1\right)d\right]}{2}$ cho cùng kết quả.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B6_TH034_SA_A_01(socau):
    r"""Số hạng tổng quát của cấp số cộng - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, d = _bo_csc()
        k = random.randint(10, 30)
        if (u1, d, k) not in gt:
            gt.append((u1, d, k))

    cau = ""
    for u1, d, k in gt:
        uk = _csc(u1, d, k)
        debai = (r"Cho cấp số cộng $\left(u_n\right)$ có $u_1 = %d$ và công "
                 r"sai $d = %d$. Tính $u_{%d}$." % (u1, d, k))
        giai = (r"$u_{%d} = u_1 + \left(%d - 1\right)d = %d + %d\cdot %d "
                r"= %d$." % (k, k, u1, k - 1, d, uk))
        nhieu = _ba_nhieu2(str(uk), [str(u1 + k * d), str(uk + d), str(uk - d)],
                           buoc=lambda t: str(uk + t + 1))
        cau += MC_SA_answer_const(debai, str(uk), nhieu, giai, 0, 0, 2)
    return cau


BOI_CANH_CSC = [
    ("Một nhà hát có {n} hàng ghế. Hàng thứ nhất có {u1} ghế, mỗi hàng "
     "sau nhiều hơn hàng liền trước {d} ghế", "ghế", "hàng"),
    ("Một công nhân tháng đầu tiên được trả {u1} triệu đồng, và mỗi tháng "
     "sau được tăng thêm {d} triệu đồng so với tháng liền trước", "triệu đồng",
     "tháng"),
    ("Một người tập chạy: ngày đầu chạy {u1} phút, mỗi ngày sau chạy nhiều "
     "hơn ngày liền trước {d} phút", "phút", "ngày"),
]


def L11_C2_B6_VD035_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với cấp số cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        mo_ta, don_vi, ten_bac = random.choice(BOI_CANH_CSC)
        u1 = random.randint(8, 20)
        d = random.randint(2, 5)
        n = random.choice([10, 12, 15, 18, 20])
        v = (mo_ta, don_vi, ten_bac, u1, d, n)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, ten_bac, u1, d, n in gt:
        un = _csc(u1, d, n)
        dung = r"$%d$" % un
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % (u1 + n * d), r"$%d$" % _tong_csc(u1, d, n),
             r"$%d$" % (u1 + (n - 2) * d)],
            buoc=lambda t: r"$%d$" % (un + t))
        debai = (mo_ta.format(n=n, u1=u1, d=d) +
                 r". Hỏi %s thứ $%d$ có bao nhiêu %s?"
                 % (ten_bac, n, don_vi))
        giai = (r"Số %s ở mỗi %s lập thành một cấp số cộng với "
                r"$u_1 = %d$ và $d = %d$." % (don_vi, ten_bac, u1, d) +
                "\\\\\n"
                r"$u_{%d} = u_1 + \left(%d - 1\right)d = %d + %d\cdot %d "
                r"= %d$." % (n, n, u1, n - 1, d, un) +
                "\\\\\n"
                r"Chú ý câu hỏi là số %s Ở RIÊNG %s thứ $%d$, chứ không "
                r"phải tổng của tất cả." % (don_vi, ten_bac, n))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B6_VD035_SA_A_01(socau):
    r"""Tổng n số hạng đầu của cấp số cộng trong bài toán thực tiễn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        mo_ta, don_vi, ten_bac = random.choice(BOI_CANH_CSC)
        u1 = random.randint(8, 20)
        d = random.randint(2, 5)
        n = random.choice([10, 12, 15, 16, 20])
        v = (mo_ta, don_vi, ten_bac, u1, d, n)
        if v not in gt:
            gt.append(v)

    cau = ""
    for mo_ta, don_vi, ten_bac, u1, d, n in gt:
        un = _csc(u1, d, n)
        S = _tong_csc(u1, d, n)
        debai = (mo_ta.format(n=n, u1=u1, d=d) +
                 r". Tính tổng số %s của cả $%d$ %s."
                 % (don_vi, n, ten_bac))
        giai = (r"$u_{%d} = %d + %d\cdot %d = %d$." % (n, u1, n - 1, d, un) +
                "\\\\\n"
                r"$S_{%d} = \dfrac{%d\left(%d %s\right)}{2} = %d$."
                % (n, n, u1, _dau(un), S))
        nhieu = _ba_nhieu2(str(S), [str(un), str(n * (u1 + un)), str(S + n)],
                           buoc=lambda t: str(S + t * n + 1))
        cau += MC_SA_answer_const(debai, str(S), nhieu, giai, 0, 0, 2)
    return cau


def L11_C2_B6_VD035_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về cấp số cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        mo_ta, don_vi, ten_bac = random.choice(BOI_CANH_CSC)
        u1 = random.randint(8, 20)
        d = random.randint(2, 5)
        n = random.choice([12, 15, 16, 20])
        v = (mo_ta, don_vi, ten_bac, u1, d, n)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, ten_bac, u1, d, n in gt:
        un = _csc(u1, d, n)
        S = _tong_csc(u1, d, n)
        k = n // 2
        uk = _csc(u1, d, k)
        debai = mo_ta.format(n=n, u1=u1, d=d) + "."

        hoi_a = (r"Viết công thức số hạng tổng quát $u_n$ của dãy số %s ở "
                 r"mỗi %s." % (don_vi, ten_bac))
        giai_a = (r"Đây là cấp số cộng với $u_1 = %d$, $d = %d$." % (u1, d) +
                  "\\\\\n"
                  r"$u_n = u_1 + \left(n - 1\right)d = %d + \left(n-1\right)"
                  r"\cdot %d = %dn %s$." % (u1, d, d, _dau(u1 - d)))

        hoi_b = r"Tính số %s ở %s thứ $%d$." % (don_vi, ten_bac, k)
        giai_b = (r"$u_{%d} = %d\cdot %d %s = %d$."
                  % (k, d, k, _dau(u1 - d), uk))

        hoi_c = r"Tính tổng số %s của cả $%d$ %s." % (don_vi, n, ten_bac)
        giai_c = (r"$u_{%d} = %d\cdot %d %s = %d$."
                  % (n, d, n, _dau(u1 - d), un) +
                  "\\\\\n"
                  r"$S_{%d} = \dfrac{n\left(u_1 + u_n\right)}{2} "
                  r"= \dfrac{%d\left(%d %s\right)}{2} = %d$."
                  % (n, n, u1, _dau(un), S))

        ds_abcd = [(hoi_a, r"u_n = %dn %s" % (d, _dau(u1 - d)), giai_a),
                   (hoi_b, r"u_{%d} = %d" % (k, uk), giai_b),
                   (hoi_c, r"S_{%d} = %d" % (n, S), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 7. CẤP SỐ NHÂN
# =====================================================================

def L11_C2_B7_NB036_MC_A_01(socau, dang=1):
    r"""Nhận biết một dãy số là cấp số nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_csn()
        if (u1, q) not in gt:
            gt.append((u1, q))

    cauTN = ""
    for u1, q in gt:
        csn = [_csn(u1, q, i) for i in range(1, 5)]
        hong = list(csn)
        hong[2] += random.choice([1, -1, 2])
        csc = [u1 + i * abs(q) for i in range(4)]
        dung = _liet_ke(csn)
        nhieu = _ba_nhieu2(
            dung,
            [_liet_ke(hong), _liet_ke(csc),
             _liet_ke([u1, u1 * q, u1 * q, u1 * q * q]),
             _liet_ke([i * i for i in range(1, 5)])],
            buoc=lambda t: _liet_ke([u1 + t, u1 * q, u1 * q ** 3, u1 * q ** 4]))
        debai = r"Dãy số nào sau đây là một cấp số nhân?"
        giai = (r"Một dãy số là cấp số nhân khi TỈ SỐ của hai số hạng liên "
                r"tiếp luôn bằng nhau (và khác $0$)."
                "\\\\\n"
                r"Với dãy %s: các tỉ số đều bằng $%d$ nên đây là cấp số "
                r"nhân với công bội $q = %d$." % (dung, q, q) +
                "\\\\\n"
                r"Chú ý phân biệt với cấp số cộng: cấp số cộng xét HIỆU, "
                r"cấp số nhân xét TỈ SỐ.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B7_NB036_TL_A_01(socau, dong=1):
    r"""Tự luận: nhận biết cấp số nhân rồi tính vài số hạng đầu.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    Nhan mapping ghi "cap so cong" nhung yeu cau can dat cua chinh
    L11_C2_B7_NB036 la "nhan biet mot day so la CAP SO NHAN" - viet
    theo yeu cau can dat. Co Lan xem lai nhan mapping giup.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_csn()
        k = random.randint(5, 8)
        if (u1, q, k) not in gt:
            gt.append((u1, q, k))

    cauTN = ""
    for u1, q, k in gt:
        ds = [_csn(u1, q, i) for i in range(1, 5)]
        uk = _csn(u1, q, k)
        debai = (r"Cho dãy số $\left(u_n\right)$ với $u_1 = %d$ và "
                 r"$u_{n+1} = %d u_n$ với mọi $n \in \mathbb{N}^{*}$."
                 % (u1, q))

        hoi_a = r"Viết bốn số hạng đầu của dãy số."
        giai_a = (r"$u_1 = %d$; $u_2 = %d\cdot %d = %d$; "
                  r"$u_3 = %d\cdot %d = %d$; $u_4 = %d\cdot %d = %d$."
                  % (u1, q, ds[0], ds[1], q, ds[1], ds[2], q, ds[2], ds[3]))

        hoi_b = (r"Chứng tỏ $\left(u_n\right)$ là một cấp số nhân và chỉ ra "
                 r"công bội.")
        giai_b = (r"Từ hệ thức truy hồi, $\dfrac{u_{n+1}}{u_n} = %d$ không "
                  r"đổi với mọi $n$." % q +
                  "\\\\\n"
                  r"Vậy $\left(u_n\right)$ là cấp số nhân với công bội "
                  r"$q = %d$." % q)

        hoi_c = r"Tính $u_{%d}$." % k
        giai_c = (r"$u_n = u_1q^{\,n-1}$ nên "
                  r"$u_{%d} = %d\cdot %s^{\,%d} = %d$."
                  % (k, u1, ngoac(q), k - 1, uk))

        ds_abcd = [(hoi_a, _liet_ke(ds).strip("$"), giai_a),
                   (hoi_b, r"q = %d" % q, giai_b),
                   (hoi_c, r"u_{%d} = %d" % (k, uk), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L11_C2_B7_TH037_MC_A_01(socau, dang=1):
    r"""Số hạng tổng quát của cấp số nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_csn()
        k = random.randint(5, 9)
        if abs(_csn(u1, q, k)) > 10 ** 6:
            continue
        if (u1, q, k) not in gt:
            gt.append((u1, q, k))

    cauTN = ""
    for u1, q, k in gt:
        uk = _csn(u1, q, k)
        dung = r"$%d$" % uk
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % _csn(u1, q, k + 1),      # quen tru 1
             r"$%d$" % (u1 * k * q),            # nham sang cap so cong
             r"$%d$" % _csn(u1, q, k - 1),
             r"$%d$" % (-uk)],
            buoc=lambda t: r"$%d$" % (uk + t))
        debai = (r"Cho cấp số nhân $\left(u_n\right)$ có $u_1 = %d$ và công "
                 r"bội $q = %d$. Tính $u_{%d}$." % (u1, q, k))
        giai = (r"Số hạng tổng quát của cấp số nhân: $u_n = u_1q^{\,n-1}$."
                "\\\\\n"
                r"$u_{%d} = %d\cdot %s^{\,%d} = %d\cdot %s = %d$."
                % (k, u1, ngoac(q), k - 1, u1, ngoac(q ** (k - 1)), uk) +
                "\\\\\n"
                r"Chú ý số mũ là $n - 1$ chứ không phải $n$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B7_TH038_MC_A_01(socau, dang=1):
    r"""Tổng n số hạng đầu tiên của cấp số nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_csn()
        n = random.randint(5, 9)
        if abs(_tong_csn(u1, q, n)) > 10 ** 6:
            continue
        if (u1, q, n) not in gt:
            gt.append((u1, q, n))

    cauTN = ""
    for u1, q, n in gt:
        S = _tong_csn(u1, q, n)
        un = _csn(u1, q, n)
        dung = r"$%d$" % S
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % un,
             r"$%d$" % _tong_csn(u1, q, n + 1),
             r"$%d$" % _tong_csc(u1, q, n),      # nham cong thuc cap so cong
             r"$%d$" % (S + un)],
            buoc=lambda t: r"$%d$" % (S + t))
        debai = (r"Cho cấp số nhân $\left(u_n\right)$ có $u_1 = %d$ và công "
                 r"bội $q = %d$. Tính tổng $S_{%d}$ của $%d$ số hạng đầu "
                 r"tiên." % (u1, q, n, n))
        giai = (r"$S_n = u_1\cdot\dfrac{1 - q^{\,n}}{1 - q}$ (với "
                r"$q \ne 1$)."
                "\\\\\n"
                r"$S_{%d} = %d\cdot\dfrac{1 - %s^{\,%d}}{1 - %s} "
                r"= %d\cdot\dfrac{%d}{%d} = %d$."
                % (n, u1, ngoac(q), n, ngoac(q), u1, 1 - q ** n, 1 - q, S))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B7_TH038_SA_A_01(socau):
    r"""Số hạng tổng quát của cấp số nhân - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_csn()
        k = random.randint(5, 9)
        if abs(_csn(u1, q, k)) > 10 ** 6:
            continue
        if (u1, q, k) not in gt:
            gt.append((u1, q, k))

    cau = ""
    for u1, q, k in gt:
        uk = _csn(u1, q, k)
        debai = (r"Cho cấp số nhân $\left(u_n\right)$ có $u_1 = %d$ và công "
                 r"bội $q = %d$. Tính $u_{%d}$." % (u1, q, k))
        giai = (r"$u_{%d} = u_1q^{\,%d} = %d\cdot %s^{\,%d} = %d$."
                % (k, k - 1, u1, ngoac(q), k - 1, uk))
        nhieu = _ba_nhieu2(str(uk),
                           [str(_csn(u1, q, k + 1)), str(_csn(u1, q, k - 1)),
                            str(u1 * k * q)],
                           buoc=lambda t: str(uk + t))
        cau += MC_SA_answer_const(debai, str(uk), nhieu, giai, 0, 0, 2)
    return cau


BOI_CANH_CSN = [
    ("Một loại vi khuẩn ban đầu có {u1} con, cứ sau mỗi giờ thì số vi "
     "khuẩn tăng lên gấp {q} lần", "con", "giờ", "số vi khuẩn"),
    ("Một người chơi trò xếp hạt: ô thứ nhất đặt {u1} hạt, mỗi ô sau đặt "
     "gấp {q} lần số hạt của ô liền trước", "hạt", "ô", "số hạt"),
    ("Một tờ giấy ban đầu dày {u1} đơn vị, mỗi lần gấp đôi thì bề dày "
     "tăng gấp {q} lần", "đơn vị", "lần gấp", "bề dày"),
]


def L11_C2_B7_VD039_MC_A_01(socau, dang=1):
    r"""Vấn đề thực tiễn gắn với cấp số nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        mo_ta, don_vi, ten_bac, ten_dl = random.choice(BOI_CANH_CSN)
        u1 = random.choice([2, 3, 4, 5, 10])
        q = random.choice([2, 3])
        n = random.randint(6, 10)
        if abs(_csn(u1, q, n)) > 10 ** 7:
            continue
        v = (mo_ta, don_vi, ten_bac, ten_dl, u1, q, n)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, ten_bac, ten_dl, u1, q, n in gt:
        un = _csn(u1, q, n)
        dung = r"$%d$" % un
        nhieu = _ba_nhieu2(
            dung,
            [r"$%d$" % _csn(u1, q, n + 1), r"$%d$" % (u1 * q * n),
             r"$%d$" % _tong_csn(u1, q, n)],
            buoc=lambda t: r"$%d$" % (un + t))
        debai = (mo_ta.format(u1=u1, q=q) +
                 r". Hỏi sau %s thứ $%d$ thì %s bằng bao nhiêu %s?"
                 % (ten_bac, n - 1, ten_dl, don_vi))
        giai = (r"%s ở mỗi %s lập thành một cấp số nhân với $u_1 = %d$ và "
                r"công bội $q = %d$; $u_n$ ứng với %s thứ $n - 1$."
                % (ten_dl.capitalize(), ten_bac, u1, q, ten_bac) +
                "\\\\\n"
                r"$u_{%d} = u_1q^{\,%d} = %d\cdot %d^{\,%d} = %d$."
                % (n, n - 1, u1, q, n - 1, un))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C2_B7_VD039_SA_A_01(socau):
    r"""Tổng n số hạng đầu của cấp số nhân - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        mo_ta, don_vi, ten_bac, ten_dl = random.choice(BOI_CANH_CSN)
        u1 = random.choice([2, 3, 4, 5])
        q = random.choice([2, 3])
        n = random.randint(6, 9)
        if abs(_tong_csn(u1, q, n)) > 10 ** 7:
            continue
        v = (mo_ta, don_vi, ten_bac, ten_dl, u1, q, n)
        if v not in gt:
            gt.append(v)

    cau = ""
    for mo_ta, don_vi, ten_bac, ten_dl, u1, q, n in gt:
        S = _tong_csn(u1, q, n)
        debai = (mo_ta.format(u1=u1, q=q) +
                 r". Tính tổng %s của $%d$ %s đầu tiên (đơn vị: %s)."
                 % (ten_dl, n, ten_bac, don_vi))
        giai = (r"$S_{%d} = u_1\cdot\dfrac{1 - q^{\,n}}{1 - q} "
                r"= %d\cdot\dfrac{1 - %d^{\,%d}}{1 - %d} = %d$."
                % (n, u1, q, n, q, S))
        nhieu = _ba_nhieu2(str(S), [str(_csn(u1, q, n)), str(S + 1),
                                    str(_tong_csn(u1, q, n + 1))],
                           buoc=lambda t: str(S + t + 1))
        cau += MC_SA_answer_const(debai, str(S), nhieu, giai, 0, 0, 2)
    return cau


def L11_C2_B7_VD039_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn về cấp số nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        mo_ta, don_vi, ten_bac, ten_dl = random.choice(BOI_CANH_CSN)
        u1 = random.choice([2, 3, 4, 5])
        q = random.choice([2, 3])
        n = random.randint(6, 9)
        if abs(_tong_csn(u1, q, n)) > 10 ** 7:
            continue
        v = (mo_ta, don_vi, ten_bac, ten_dl, u1, q, n)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, ten_bac, ten_dl, u1, q, n in gt:
        un = _csn(u1, q, n)
        S = _tong_csn(u1, q, n)
        debai = mo_ta.format(u1=u1, q=q) + "."

        hoi_a = (r"Viết công thức số hạng tổng quát $u_n$ của dãy %s."
                 % ten_dl)
        giai_a = (r"Đây là cấp số nhân với $u_1 = %d$, $q = %d$." % (u1, q) +
                  "\\\\\n"
                  r"$u_n = u_1q^{\,n-1} = %d\cdot %d^{\,n-1}$." % (u1, q))

        hoi_b = r"Tính $u_{%d}$." % n
        giai_b = (r"$u_{%d} = %d\cdot %d^{\,%d} = %d$."
                  % (n, u1, q, n - 1, un))

        hoi_c = r"Tính tổng $S_{%d}$ của $%d$ số hạng đầu tiên." % (n, n)
        giai_c = (r"$S_{%d} = u_1\cdot\dfrac{1 - q^{\,n}}{1 - q} "
                  r"= %d\cdot\dfrac{1 - %d^{\,%d}}{1 - %d} = %d$."
                  % (n, u1, q, n, q, S))

        ds_abcd = [(hoi_a, r"u_n = %d\cdot %d^{\,n-1}" % (u1, q), giai_a),
                   (hoi_b, r"u_{%d} = %d" % (n, un), giai_b),
                   (hoi_c, r"S_{%d} = %d" % (n, S), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 2
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C2_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - dãy số và cấp số cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, d = _bo_csc()
        n = random.choice([10, 12, 15, 20])
        if (u1, d, n) not in gt:
            gt.append((u1, d, n))

    cauTF = ""
    for u1, d, n in gt:
        u2 = _csc(u1, d, 2)
        un = _csc(u1, d, n)
        S = _tong_csc(u1, d, n)
        tang = d > 0
        debai = (r"Cho cấp số cộng $\left(u_n\right)$ có số hạng đầu "
                 r"$u_1 = %d$ và công sai $d = %d$." % (u1, d))

        ds_abcd = (
            # a) NB - nhắc lại định nghĩa
            [
                (r"{\True Số hạng thứ hai của cấp số cộng bằng $%d$}" % u2,
                 r"Đúng. $u_2 = u_1 + d = %d %s = %d$."
                 % (u1, _dau(d), u2)),
                (r"{Số hạng thứ hai của cấp số cộng bằng $%d$}" % (u1 * d),
                 r"Sai. Cấp số cộng thì số hạng sau bằng số hạng trước "
                 r"CỘNG công sai, không phải nhân: $u_2 = %d$." % u2),
            ],
            # b) TH - một lần dùng công thức tổng quát
            [
                (r"{\True $u_{%d} = %d$}" % (n, un),
                 r"Đúng. $u_n = u_1 + \left(n-1\right)d$ nên "
                 r"$u_{%d} = %d + %d\cdot %d = %d$."
                 % (n, u1, n - 1, d, un)),
                (r"{$u_{%d} = %d$}" % (n, u1 + n * d),
                 r"Sai. Hệ số là $n - 1$ chứ không phải $n$: từ $u_1$ đến "
                 r"$u_{%d}$ chỉ cộng thêm $d$ đúng $%d$ lần, được $%d$."
                 % (n, n - 1, un)),
            ],
            # c) VD - phải tính u_n rồi mới tính được tổng
            [
                (r"{\True $S_{%d} = %d$}" % (n, S),
                 r"Đúng. $S_n = \dfrac{n\left(u_1 + u_n\right)}{2} "
                 r"= \dfrac{%d\left(%d %s\right)}{2} = %d$."
                 % (n, u1, _dau(un), S)),
                (r"{$S_{%d} = %d$}" % (n, n * (u1 + un)),
                 r"Sai. Công thức còn phải CHIA CHO $2$: "
                 r"$S_{%d} = \dfrac{%d}{2} = %d$."
                 % (n, n * (u1 + un), S)),
            ],
            # d) VDC - phải tự xét dấu công sai rồi suy ra tính chất
            [
                (r"{\True Dãy số $\left(u_n\right)$ %s và bị chặn %s}"
                 % ("tăng" if tang else "giảm", "dưới" if tang else "trên"),
                 r"Đúng. $u_{n+1} - u_n = d = %d %s 0$ với mọi $n$ nên dãy "
                 r"%s." % (d, ">" if tang else "<",
                           "tăng" if tang else "giảm") +
                 "\\\\\n"
                 r"Dãy %s thì mọi số hạng đều %s $u_1 = %d$, nên bị chặn "
                 r"%s bởi $%d$; phía còn lại không bị chặn vì "
                 r"$u_n \to %s\infty$."
                 % ("tăng" if tang else "giảm",
                    "không nhỏ hơn" if tang else "không lớn hơn", u1,
                    "dưới" if tang else "trên", u1, "+" if tang else "-")),
                (r"{Dãy số $\left(u_n\right)$ bị chặn}",
                 r"Sai. Dãy bị chặn phải vừa bị chặn trên vừa bị chặn dưới. "
                 r"Ở đây $u_n \to %s\infty$ nên dãy chỉ bị chặn %s."
                 % ("+" if tang else "-", "dưới" if tang else "trên")),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L11_C2_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - cấp số nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u1, q = _bo_csn()
        n = random.randint(5, 8)
        if abs(_tong_csn(u1, q, n)) > 10 ** 6:
            continue
        if (u1, q, n) not in gt:
            gt.append((u1, q, n))

    cauTF = ""
    for u1, q, n in gt:
        u2 = _csn(u1, q, 2)
        un = _csn(u1, q, n)
        S = _tong_csn(u1, q, n)
        debai = (r"Cho cấp số nhân $\left(u_n\right)$ có số hạng đầu "
                 r"$u_1 = %d$ và công bội $q = %d$." % (u1, q))

        ds_abcd = (
            # a) NB - nhắc lại định nghĩa
            [
                (r"{\True Số hạng thứ hai của cấp số nhân bằng $%d$}" % u2,
                 r"Đúng. $u_2 = u_1q = %d\cdot %d = %d$." % (u1, q, u2)),
                (r"{Số hạng thứ hai của cấp số nhân bằng $%d$}" % (u1 + q),
                 r"Sai. Cấp số nhân thì số hạng sau bằng số hạng trước "
                 r"NHÂN công bội, không phải cộng: $u_2 = %d$." % u2),
            ],
            # b) TH - một lần dùng công thức tổng quát
            [
                (r"{\True $u_{%d} = %d$}" % (n, un),
                 r"Đúng. $u_n = u_1q^{\,n-1}$ nên "
                 r"$u_{%d} = %d\cdot %s^{\,%d} = %d$."
                 % (n, u1, ngoac(q), n - 1, un)),
                (r"{$u_{%d} = %d$}" % (n, _csn(u1, q, n + 1)),
                 r"Sai. Số mũ là $n - 1$ chứ không phải $n$; tính đúng ra "
                 r"$u_{%d} = %d$." % (n, un)),
            ],
            # c) VD - phải dùng công thức tổng
            [
                (r"{\True $S_{%d} = %d$}" % (n, S),
                 r"Đúng. $S_n = u_1\cdot\dfrac{1 - q^{\,n}}{1 - q} "
                 r"= %d\cdot\dfrac{1 - %s^{\,%d}}{1 - %s} = %d$."
                 % (u1, ngoac(q), n, ngoac(q), S)),
                (r"{$S_{%d} = %d$}" % (n, _tong_csc(u1, q, n)),
                 r"Sai. Đó là công thức tổng của CẤP SỐ CỘNG. Cấp số nhân "
                 r"dùng $S_n = u_1\dfrac{1 - q^{\,n}}{1 - q}$, ra $%d$."
                 % S),
            ],
            # d) VDC - phải tự nhận ra dấu của các số hạng đổi luân phiên
            [
                ((r"{\True Các số hạng của cấp số nhân đổi dấu luân phiên}"
                  if q < 0 else
                  r"{\True Mọi số hạng của cấp số nhân đều cùng dấu với "
                  r"$u_1$}"),
                 (r"Đúng. Vì $q = %d < 0$ nên $q^{\,n-1}$ đổi dấu mỗi khi "
                  r"$n$ tăng thêm $1$; do đó $u_n = u_1q^{\,n-1}$ đổi dấu "
                  r"luân phiên." % q if q < 0 else
                  r"Đúng. Vì $q = %d > 0$ nên $q^{\,n-1} > 0$ với mọi $n$; "
                  r"do đó $u_n = u_1q^{\,n-1}$ luôn cùng dấu với $u_1$."
                  % q) +
                 "\\\\\n"
                 r"Kiểm lại bốn số hạng đầu: $%s$."
                 % r"$; $".join(str(_csn(u1, q, i)) for i in range(1, 5))),
                ((r"{Mọi số hạng của cấp số nhân đều cùng dấu với $u_1$}"
                  if q < 0 else
                  r"{Các số hạng của cấp số nhân đổi dấu luân phiên}"),
                 (r"Sai. Công bội $q = %d$ ÂM nên dấu đổi luân phiên, "
                  r"không thể cùng dấu mãi." % q if q < 0 else
                  r"Sai. Công bội $q = %d$ DƯƠNG nên mọi số hạng cùng dấu "
                  r"với $u_1$, không đổi dấu." % q)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
