# -*- coding: utf-8 -*-
r"""Lớp 12 - Chương 2. Vectơ và hệ trục toạ độ trong không gian
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Bám đúng ba bài của PPCT:

  * Bài 6. Vectơ trong không gian - quy tắc hình hộp, tổng/hiệu, tích
    với một số, tích vô hướng.
  * Bài 7. Hệ trục toạ độ trong không gian - toạ độ vectơ, độ dài
    $\left|\vv{AB}\right| = \sqrt{\left(x_B-x_A\right)^2
    + \left(y_B-y_A\right)^2 + \left(z_B-z_A\right)^2}$.
  * Bài 8. Biểu thức toạ độ của các phép toán vectơ - cộng, trừ, nhân
    với một số, tích vô hướng $\vv{a}\cdot\vv{b} = a_1b_1 + a_2b_2
    + a_3b_3$.

SỐ LIỆU CHỌN ĐỂ ĐÁP SỐ ĐẸP. Câu trả lời ngắn chấm bằng SO KHỚP CHUỖI
nên đáp số phải viết được chính xác:

  * Mọi câu hỏi độ dài đều lấy hiệu toạ độ từ BO_PYTAGO3 - các bộ ba
    $(a,b,c)$ có $a^2+b^2+c^2$ là số chính phương, nên căn ra số NGUYÊN.
  * Mọi câu hỏi toạ độ / tích vô hướng đều ra số nguyên.

Quy ước trình bày (theo bài học lớp 10, 11):
chữ tiếng Việt không bao giờ nằm trần trong $...$ (phải bọc \text{});
không dùng chữ đậm kiểu Markdown; mọi chuỗi có dấu gạch chéo đều là
chuỗi r"..."; mọi danh sách phương án nhiễu đều đi qua _ba_nhieu12.
"""
import math
import random

from math_type import *          # noqa: F401,F403

DAU_THAP_PHAN = ","

# Các bộ ba (a, b, c) có a^2 + b^2 + c^2 là SỐ CHÍNH PHƯƠNG.
# Dùng làm HIỆU toạ độ của hai điểm để độ dài đoạn thẳng luôn nguyên.
BO_PYTAGO3 = [
    (1, 2, 2),      # 3
    (2, 3, 6),      # 7
    (1, 4, 8),      # 9
    (4, 4, 7),      # 9
    (2, 6, 9),      # 11
    (6, 6, 7),      # 11
    (3, 4, 12),     # 13
    (2, 5, 14),     # 15
    (2, 10, 11),    # 15
    (1, 12, 12),    # 17
    (8, 9, 12),     # 17
    (6, 10, 15),    # 19
    (4, 8, 19),     # 21
    (4, 5, 20),     # 21
    (12, 15, 16),   # 25
]

DINH_HOP = ["A", "B", "C", "D"]


def _xx(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết theo cách viết Việt Nam."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu12(dapso, ung_vien, buoc=None):
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


def _toa(x):
    """Toạ độ TikZ - luôn dùng dấu CHẤM thập phân."""
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _bo3(v):
    r"""Viết bộ ba toạ độ: $\left(2; -3; 5\right)$."""
    return r"\left(%d; %d; %d\right)" % (v[0], v[1], v[2])


def _diem(ten, v):
    r"""Viết điểm kèm toạ độ: $A\left(1; 2; 3\right)$."""
    return r"%s\left(%d; %d; %d\right)" % (ten, v[0], v[1], v[2])


def _dau(x):
    """Viết ' + 5' hoặc ' - 5' cho đúng dấu, không để '+ -5'."""
    return r"%s %d" % ("+" if x >= 0 else "-", abs(x))


def _hieu(P, Q):
    """Vectơ PQ = Q - P."""
    return (Q[0] - P[0], Q[1] - P[1], Q[2] - P[2])


def _do_dai(v):
    return math.isqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def _cham(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _hai_diem_dep():
    """Hai điểm nguyên sao cho độ dài đoạn nối chúng là SỐ NGUYÊN."""
    a, b, c = random.choice(BO_PYTAGO3)
    hieu = (a * random.choice([-1, 1]),
            b * random.choice([-1, 1]),
            c * random.choice([-1, 1]))
    hieu = tuple(random.sample(hieu, 3))
    A = tuple(random.randint(-4, 4) for _ in range(3))
    B = (A[0] + hieu[0], A[1] + hieu[1], A[2] + hieu[2])
    return A, B


def _hinh_hop(nhan=("A", "B", "C", "D")):
    r"""Hình hộp $ABCD.A'B'C'D'$ vẽ bằng TikZ thuần.

    Đỉnh $D$ nằm phía sau nên ba cạnh đi qua nó vẽ nét đứt - đúng cách
    nhìn hình không gian trong sách giáo khoa.
    """
    A, B, C, D = nhan
    # Đáy: A trước-trái, B trước-phải, C sau-phải, D sau-trái.
    duoi = {A: (0, 0), B: (3.2, 0), C: (4.4, 1.3), D: (1.2, 1.3)}
    cao = 2.5
    tren = {k: (v[0], v[1] + cao) for k, v in duoi.items()}

    def xy(d, ten):
        return "(%s,%s)" % (_toa(d[ten][0]), _toa(d[ten][1]))

    ra = ["\\begin{tikzpicture}[scale=0.85,line join=round,"
          "font=\\footnotesize]"]
    # Cạnh khuất (đi qua D) vẽ nét đứt trước.
    for u, v in ((A, D), (C, D)):
        ra.append("\\draw[dashed,black!55] %s -- %s;"
                  % (xy(duoi, u), xy(duoi, v)))
    ra.append("\\draw[dashed,black!55] %s -- %s;"
              % (xy(duoi, D), xy(tren, D)))
    # Cạnh thấy.
    for u, v in ((A, B), (B, C)):
        ra.append("\\draw %s -- %s;" % (xy(duoi, u), xy(duoi, v)))
    for t in (A, B, C, D):
        if t != D:
            ra.append("\\draw %s -- %s;" % (xy(duoi, t), xy(tren, t)))
    for u, v in ((A, B), (B, C), (C, D), (D, A)):
        ra.append("\\draw %s -- %s;" % (xy(tren, u), xy(tren, v)))
    # Nhãn đỉnh.
    goc_duoi = {A: "below left", B: "below right", C: "right", D: "left"}
    goc_tren = {A: "left", B: "right", C: "right", D: "above left"}
    for t in (A, B, C, D):
        ra.append("\\node[%s] at %s {$%s$};"
                  % (goc_duoi[t], xy(duoi, t), t))
        ra.append("\\node[%s] at %s {$%s'$};"
                  % (goc_tren[t], xy(tren, t), t))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


def _hinh_oxyz(diem=()):
    r"""Hệ trục $Oxyz$ vẽ bằng TikZ thuần, kèm vài điểm nếu cần.

    Chỉ vẽ ba trục cho học sinh hình dung hệ trục, không vẽ đúng tỉ lệ
    toạ độ (toạ độ trong đề có thể âm, rất lớn - vẽ thật sẽ ra hình
    méo mó, không giúp gì cho việc tính).
    """
    ra = ["\\begin{tikzpicture}[scale=0.8,>=stealth,line join=round,"
          "font=\\footnotesize]"]
    ra.append("\\draw[->] (0,0) -- (-1.7,-1.2) node[below left]{$x$};")
    ra.append("\\draw[->] (0,0) -- (3,0) node[right]{$y$};")
    ra.append("\\draw[->] (0,0) -- (0,2.6) node[above]{$z$};")
    ra.append("\\node[above right] at (0,0) {$O$};")
    ra.append("\\fill (0,0) circle (1.1pt);")
    for ten, x, y in diem:
        ra.append("\\fill[red!75!black] (%s,%s) circle (1.6pt);"
                  % (_toa(x), _toa(y)))
        ra.append("\\node[red!75!black,above right] at (%s,%s) {$%s$};"
                  % (_toa(x), _toa(y), ten))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


# =====================================================================
# BÀI 6. VECTƠ TRONG KHÔNG GIAN
# =====================================================================

def L12_C2_B6_NB013_MC_A_01(socau, dang=1):
    r"""Nhận biết phép toán vectơ trong không gian - quy tắc hình hộp.

    Quy tắc hình hộp: nếu $X$ là một đỉnh của hình hộp và $Y$, $Z$, $T$
    là ba đỉnh kề $X$ thì $\vv{XY} + \vv{XZ} + \vv{XT} = \vv{XW}$ với
    $W$ là đỉnh ĐỐI XỨNG với $X$ qua tâm hình hộp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    # Hình hộp ABCD.A'B'C'D'. Với mỗi đỉnh: ba đỉnh kề và đỉnh đối tâm.
    # Mỗi đỉnh đáy -> ba đỉnh KỀ nó trên hình hộp.
    KE = {"A": ("B", "D", "A'"),
          "B": ("A", "C", "B'"),
          "C": ("B", "D", "C'"),
          "D": ("A", "C", "D'")}
    # Đỉnh ĐỐI XỨNG qua tâm hình hộp - chính là ngọn của tổng ba vectơ.
    DOI = {"A": "C'", "B": "D'", "C": "A'", "D": "B'"}
    DINH = ["A", "B", "C", "D"]

    gt = []
    while len(gt) < socau:
        X = random.choice(DINH)
        if X not in gt:
            gt.append(X)
        if len(gt) >= len(DINH):
            break
    while len(gt) < socau:
        gt.append(random.choice(DINH))

    cauTN = ""
    for X in gt:
        Y, Z, T = KE[X]
        W = DOI[X]
        dung = r"$\vv{%s%s}$" % (X, W)
        nhieu = _ba_nhieu12(
            dung,
            [r"$\vv{%s%s}$" % (X, Y), r"$\vv{%s%s}$" % (X, Z),
             r"$\vv{%s%s}$" % (X, T), r"$\vv{%s%s}$" % (W, X)],
            buoc=lambda k: r"$\vv{%s%s}$" % (DINH[k % 4], W))
        debai = (r"Cho hình hộp $ABCD.A'B'C'D'$. Tổng "
                 r"$\vv{%s%s} + \vv{%s%s} + \vv{%s%s}$ bằng vectơ nào "
                 r"sau đây?" % (X, Y, X, Z, X, T))
        giai = (r"Ba vectơ $\vv{%s%s}$, $\vv{%s%s}$, $\vv{%s%s}$ cùng "
                r"xuất phát từ đỉnh $%s$ và nằm trên ba cạnh của hình "
                r"hộp." % (X, Y, X, Z, X, T, X) +
                "\\\\\n"
                r"Theo quy tắc hình hộp, tổng của chúng là đường chéo "
                r"đi từ $%s$ tới đỉnh đối diện qua tâm, tức là "
                r"$\vv{%s%s}$." % (X, X, W))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_hop(), 0, dang)
    return cauTN


# =====================================================================
# BÀI 7. HỆ TRỤC TOẠ ĐỘ TRONG KHÔNG GIAN
# =====================================================================

def L12_C2_B7_NB014_MC_A_01(socau, dang=1):
    r"""Nhận biết toạ độ của một vectơ đối với hệ trục $Oxyz$.

    $\vv{a} = a_1\vec{i} + a_2\vec{j} + a_3\vec{k}
     \Leftrightarrow \vv{a} = \left(a_1; a_2; a_3\right)$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = tuple(random.choice([-9, -7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8])
                  for _ in range(3))
        if len(set(map(abs, v))) == 3 and v not in gt:
            gt.append(v)

    cauTN = ""
    for v in gt:
        a1, a2, a3 = v
        dung = "$%s$" % _bo3(v)
        nhieu = _ba_nhieu12(
            dung,
            ["$%s$" % _bo3((a2, a1, a3)),      # đảo hai thành phần đầu
             "$%s$" % _bo3((a1, -a2, a3)),     # quên dấu trừ
             "$%s$" % _bo3((a3, a2, a1)),      # đảo đầu với cuối
             "$%s$" % _bo3((-a1, -a2, -a3))],
            buoc=lambda k: "$%s$" % _bo3((a1 + k, a2, a3)))
        debai = (r"Trong không gian $Oxyz$, cho vectơ "
                 r"$\vv{a} = %d\vec{i} %s\vec{j} %s\vec{k}$. Toạ độ của "
                 r"vectơ $\vv{a}$ là" % (a1, _dau(a2), _dau(a3)))
        giai = (r"Theo định nghĩa, nếu "
                r"$\vv{a} = a_1\vec{i} + a_2\vec{j} + a_3\vec{k}$ thì "
                r"$\vv{a} = \left(a_1; a_2; a_3\right)$." +
                "\\\\\n"
                r"Ở đây $a_1 = %d$, $a_2 = %d$, $a_3 = %d$ nên "
                r"$\vv{a} = %s$." % (a1, a2, a3, _bo3(v)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_oxyz(), 0, dang)
    return cauTN


def L12_C2_B7_TH015_MC_A_01(socau, dang=1):
    r"""Độ dài vectơ khi biết toạ độ hai đầu mút.

    Hiệu toạ độ lấy từ BO_PYTAGO3 nên $\left|\vv{AB}\right|$ luôn là
    số NGUYÊN - không phải làm tròn, không có căn thức xấu.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A, B = _hai_diem_dep()
        if (A, B) not in gt:
            gt.append((A, B))

    cauTN = ""
    for A, B in gt:
        v = _hieu(A, B)
        d = _do_dai(v)
        binh = v[0] ** 2 + v[1] ** 2 + v[2] ** 2
        dung = "$%d$" % d
        nhieu = _ba_nhieu12(
            dung,
            ["$%d$" % binh,                                   # quên khai căn
             "$%d$" % (abs(v[0]) + abs(v[1]) + abs(v[2])),    # cộng thẳng
             "$%d$" % (d + 1), "$%d$" % max(1, d - 1)],
            buoc=lambda k: "$%d$" % (d + k + 1))
        debai = (r"Trong không gian $Oxyz$, cho hai điểm $%s$ và $%s$. "
                 r"Độ dài đoạn thẳng $AB$ bằng"
                 % (_diem("A", A), _diem("B", B)))
        giai = (r"$\vv{AB} = %s$." % _bo3(v) +
                "\\\\\n"
                r"$AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2 "
                r"+ \left(%d\right)^2} = \sqrt{%d} = %d$."
                % (v[0], v[1], v[2], binh, d))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L12_C2_B7_TH015_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - độ dài vectơ trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A, B = _hai_diem_dep()
        if (A, B) not in gt:
            gt.append((A, B))

    cau = ""
    for A, B in gt:
        v = _hieu(A, B)
        d = _do_dai(v)
        binh = v[0] ** 2 + v[1] ** 2 + v[2] ** 2
        dapso = "%d" % d
        nhieu = _ba_nhieu12(dapso,
                            ["%d" % binh, "%d" % (d + 2), "%d" % (d - 1)],
                            buoc=lambda k: "%d" % (d + k + 2))
        debai = (r"Trong không gian $Oxyz$, cho hai điểm $%s$ và $%s$. "
                 r"Tính độ dài đoạn thẳng $AB$."
                 % (_diem("A", A), _diem("B", B)))
        giai = (r"$\vv{AB} = %s$ nên" % _bo3(v) +
                "\\\\\n"
                r"$AB = \sqrt{\left(%d\right)^2 + \left(%d\right)^2 "
                r"+ \left(%d\right)^2} = \sqrt{%d} = %d$."
                % (v[0], v[1], v[2], binh, d))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


# =====================================================================
# BÀI 8. BIỂU THỨC TOẠ ĐỘ CỦA CÁC PHÉP TOÁN VECTƠ
# =====================================================================

def _bo_hai_vecto():
    """Hai vectơ toạ độ nguyên, không cùng phương, số không quá lớn."""
    while True:
        u = tuple(random.randint(-6, 6) for _ in range(3))
        v = tuple(random.randint(-6, 6) for _ in range(3))
        if u == (0, 0, 0) or v == (0, 0, 0):
            continue
        # Loại trường hợp cùng phương cho khỏi tầm thường.
        tich = (u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0])
        if tich != (0, 0, 0):
            return u, v


def L12_C2_B8_TH016_MC_A_01(socau, dang=1):
    r"""Biểu thức toạ độ của các phép toán vectơ.

    $m\vv{a} + n\vv{b}
     = \left(ma_1 + nb_1; ma_2 + nb_2; ma_3 + nb_3\right)$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        u, v = _bo_hai_vecto()
        m = random.choice([-3, -2, 2, 3])
        n = random.choice([-3, -2, 2, 3])
        if (u, v, m, n) not in gt:
            gt.append((u, v, m, n))

    cauTN = ""
    for u, v, m, n in gt:
        kq = tuple(m * u[i] + n * v[i] for i in range(3))
        # Ba lỗi hay gặp: quên nhân hệ số, đổi dấu sai, nhân nhầm chéo.
        sai1 = tuple(u[i] + v[i] for i in range(3))
        sai2 = tuple(m * u[i] - n * v[i] for i in range(3))
        sai3 = tuple(n * u[i] + m * v[i] for i in range(3))
        dung = "$%s$" % _bo3(kq)
        nhieu = _ba_nhieu12(
            dung,
            ["$%s$" % _bo3(sai1), "$%s$" % _bo3(sai2), "$%s$" % _bo3(sai3)],
            buoc=lambda k: "$%s$" % _bo3((kq[0] + k, kq[1], kq[2])))
        debai = (r"Trong không gian $Oxyz$, cho $\vv{a} = %s$ và "
                 r"$\vv{b} = %s$. Toạ độ của vectơ "
                 r"$\vv{u} = %d\vv{a} %s %d\vv{b}$ là"
                 % (_bo3(u), _bo3(v), m, "+" if n >= 0 else "-", abs(n)))
        giai = (r"$%d\vv{a} = %s$ và $%d\vv{b} = %s$."
                % (m, _bo3(tuple(m * t for t in u)),
                   n, _bo3(tuple(n * t for t in v))) +
                "\\\\\n"
                r"Cộng từng thành phần tương ứng: $\vv{u} = %s$."
                % _bo3(kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L12_C2_B8_TH016_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - MỘT thành phần toạ độ của vectơ sau phép toán.

    Trả lời ngắn chỉ được có MỘT đáp án, nên hỏi đúng một thành phần
    chứ không hỏi cả bộ ba.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    TEN_TP = [("hoành độ", 0), ("tung độ", 1), ("cao độ", 2)]
    gt = []
    while len(gt) < socau:
        u, v = _bo_hai_vecto()
        m = random.choice([-3, -2, 2, 3])
        n = random.choice([-3, -2, 2, 3])
        ten, i = random.choice(TEN_TP)
        if (u, v, m, n, i) not in gt:
            gt.append((u, v, m, n, i))

    cau = ""
    for u, v, m, n, i in gt:
        ten = TEN_TP[i][0]
        kq = m * u[i] + n * v[i]
        dapso = "%d" % kq
        nhieu = _ba_nhieu12(dapso,
                            ["%d" % (u[i] + v[i]),
                             "%d" % (m * u[i] - n * v[i]),
                             "%d" % (n * u[i] + m * v[i])],
                            buoc=lambda k: "%d" % (kq + k))
        debai = (r"Trong không gian $Oxyz$, cho $\vv{a} = %s$ và "
                 r"$\vv{b} = %s$. Tìm %s của vectơ "
                 r"$\vv{u} = %d\vv{a} %s %d\vv{b}$."
                 % (_bo3(u), _bo3(v), ten, m,
                    "+" if n >= 0 else "-", abs(n)))
        giai = (r"%s của $\vv{u}$ bằng $%d$ lần %s của $\vv{a}$, cộng "
                r"với $%s%d$ lần %s của $\vv{b}$."
                % (ten.capitalize(), m, ten,
                   "" if n >= 0 else "-", abs(n), ten) +
                "\\\\\n"
                r"$%d\cdot\left(%d\right) + \left(%d\right)\cdot"
                r"\left(%d\right) = %d %s = %d$."
                % (m, u[i], n, v[i], m * u[i], _dau(n * v[i]), kq))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


# ---------------------------------------------------------------------
# Mức VẬN DỤNG - bài toán thực tiễn dùng toạ độ trong không gian
#
# Bối cảnh chung: ba sợi dây (hoặc ba động cơ) kéo một vật, mỗi lực cho
# bằng toạ độ trong hệ $Oxyz$ gắn với mặt đất. Hợp lực là TỔNG ba vectơ,
# độ lớn hợp lực là độ dài vectơ tổng. Số liệu chọn sao cho tổng rơi
# đúng vào một bộ trong BO_PYTAGO3 nên độ lớn là SỐ NGUYÊN.
# ---------------------------------------------------------------------

BOI_CANH_LUC = [
    ("Ba sợi dây cáp cùng kéo một thùng hàng", "lực căng", r"\text{N}",
     "thùng hàng"),
    ("Ba động cơ của một thiết bị bay cùng đẩy thiết bị", "lực đẩy",
     r"\text{N}", "thiết bị bay"),
    ("Ba chiếc tàu kéo cùng kéo một sà lan", "lực kéo", r"\text{N}",
     "sà lan"),
]


def _bo_ba_luc():
    """Ba vectơ lực nguyên có TỔNG nằm trong BO_PYTAGO3 (nhân hệ số)."""
    a, b, c = random.choice(BO_PYTAGO3)
    he_so = random.choice([1, 2, 3])
    tong = (a * he_so * random.choice([-1, 1]),
            b * he_so * random.choice([-1, 1]),
            c * he_so * random.choice([-1, 1]))
    tong = tuple(random.sample(tong, 3))
    F1 = tuple(random.randint(-8, 8) for _ in range(3))
    F2 = tuple(random.randint(-8, 8) for _ in range(3))
    F3 = tuple(tong[i] - F1[i] - F2[i] for i in range(3))
    if max(abs(t) for t in F3) > 40:
        return _bo_ba_luc()
    return F1, F2, F3, tong, he_so * math.isqrt(a * a + b * b + c * c)


def L12_C2_B8_VD017_MC_A_01(socau, dang=1):
    r"""Vận dụng toạ độ vectơ vào bài toán thực tiễn - hợp lực.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_ba_luc()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for F1, F2, F3, tong, do_lon in gt:
        boi_canh, ten_luc, don_vi, vat = random.choice(BOI_CANH_LUC)
        binh = sum(t * t for t in tong)
        dung = "$%d$ N" % do_lon
        nhieu = _ba_nhieu12(
            dung,
            ["$%d$ N" % binh,
             "$%d$ N" % sum(abs(t) for t in tong),
             "$%d$ N" % (_do_dai(F1) + _do_dai(F2) + _do_dai(F3))],
            buoc=lambda k: "$%d$ N" % (do_lon + k + 1))
        debai = (r"%s. Trong một hệ toạ độ $Oxyz$ gắn với mặt đất, ba "
                 r"%s (đơn vị niutơn) lần lượt là $\vv{F_1} = %s$, "
                 r"$\vv{F_2} = %s$, $\vv{F_3} = %s$. Tính độ lớn của hợp "
                 r"lực tác dụng lên %s."
                 % (boi_canh, ten_luc, _bo3(F1), _bo3(F2), _bo3(F3), vat))
        giai = (r"Hợp lực là tổng ba vectơ lực, cộng theo từng thành "
                r"phần:" +
                "\\\\\n"
                r"$\vv{F} = \vv{F_1} + \vv{F_2} + \vv{F_3} = %s$."
                % _bo3(tong) +
                "\\\\\n"
                r"Độ lớn hợp lực là độ dài của vectơ đó:" +
                "\\\\\n"
                r"$\left|\vv{F}\right| = \sqrt{\left(%d\right)^2 + "
                r"\left(%d\right)^2 + \left(%d\right)^2} = \sqrt{%d} "
                r"= %d$ (N)." % (tong[0], tong[1], tong[2], binh, do_lon))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L12_C2_B8_VD017_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - độ lớn hợp lực trong bài toán thực tiễn.

    CLAUDE THEM 29/09/2026 - o tra loi ngan muc VD cua chuong 2 truoc
    day BO TRONG: ra de he so 1 chuong nay luon hut cau. Co Lan kiem
    tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_ba_luc()
        if v not in gt:
            gt.append(v)

    cau = ""
    for F1, F2, F3, tong, do_lon in gt:
        boi_canh, ten_luc, don_vi, vat = random.choice(BOI_CANH_LUC)
        binh = sum(t * t for t in tong)
        dapso = "%d" % do_lon
        nhieu = _ba_nhieu12(dapso,
                            ["%d" % binh,
                             "%d" % sum(abs(t) for t in tong),
                             "%d" % (do_lon + 2)],
                            buoc=lambda k: "%d" % (do_lon + k + 2))
        debai = (r"%s. Trong một hệ toạ độ $Oxyz$ gắn với mặt đất, ba "
                 r"%s (đơn vị niutơn) lần lượt là $\vv{F_1} = %s$, "
                 r"$\vv{F_2} = %s$, $\vv{F_3} = %s$. Tính độ lớn của hợp "
                 r"lực tác dụng lên %s (đơn vị: niutơn)."
                 % (boi_canh, ten_luc, _bo3(F1), _bo3(F2), _bo3(F3), vat))
        giai = (r"$\vv{F} = \vv{F_1} + \vv{F_2} + \vv{F_3} = %s$."
                % _bo3(tong) +
                "\\\\\n"
                r"$\left|\vv{F}\right| = \sqrt{\left(%d\right)^2 + "
                r"\left(%d\right)^2 + \left(%d\right)^2} = \sqrt{%d} "
                r"= %d$ (N)." % (tong[0], tong[1], tong[2], binh, do_lon))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L12_C2_B8_VD017_TL_A_01(socau, dong=1):
    r"""Tự luận - bài toán thực tiễn dùng toạ độ trong không gian.

    Ba ý theo thang NB - TH - VD: viết toạ độ vectơ, tính độ lớn, rồi
    tìm toạ độ một điểm thoả điều kiện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_ba_luc()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for F1, F2, F3, tong, do_lon in gt:
        boi_canh, ten_luc, don_vi, vat = random.choice(BOI_CANH_LUC)
        binh = sum(t * t for t in tong)
        # Ý c): tìm lực thứ tư để vật đứng yên (tổng bốn lực bằng vectơ 0).
        F4 = tuple(-t for t in tong)

        debai = (r"%s. Trong một hệ toạ độ $Oxyz$ gắn với mặt đất (đơn vị "
                 r"trên mỗi trục là niutơn), ba %s lần lượt là "
                 r"$\vv{F_1} = %s$, $\vv{F_2} = %s$, $\vv{F_3} = %s$."
                 % (boi_canh, ten_luc, _bo3(F1), _bo3(F2), _bo3(F3)))

        hoi_a = r"Tìm toạ độ của hợp lực $\vv{F}$ tác dụng lên %s." % vat
        giai_a = (r"Hợp lực là tổng ba vectơ lực, cộng theo từng thành "
                  r"phần tương ứng:" +
                  "\\\\\n"
                  r"$\vv{F} = \vv{F_1} + \vv{F_2} + \vv{F_3} = %s$."
                  % _bo3(tong))

        hoi_b = r"Tính độ lớn của hợp lực $\vv{F}$."
        giai_b = (r"$\left|\vv{F}\right| = \sqrt{\left(%d\right)^2 + "
                  r"\left(%d\right)^2 + \left(%d\right)^2} = \sqrt{%d} "
                  r"= %d$ (N)."
                  % (tong[0], tong[1], tong[2], binh, do_lon))

        hoi_c = (r"Người ta buộc thêm một sợi dây thứ tư để %s đứng yên. "
                 r"Tìm toạ độ của lực căng $\vv{F_4}$ trên dây đó." % vat)
        giai_c = (r"%s đứng yên khi tổng bốn lực bằng vectơ $\vec{0}$:"
                  % vat.capitalize() +
                  "\\\\\n"
                  r"$\vv{F_1} + \vv{F_2} + \vv{F_3} + \vv{F_4} = \vec{0} "
                  r"\Leftrightarrow \vv{F} + \vv{F_4} = \vec{0} "
                  r"\Leftrightarrow \vv{F_4} = -\vv{F}$." +
                  "\\\\\n"
                  r"Vậy $\vv{F_4} = %s$ (N). Lực này ngược hướng với hợp "
                  r"lực và có cùng độ lớn $%d$ N."
                  % (_bo3(F4), do_lon))

        ds_abcd = [(hoi_a, r"\vv{F} = %s" % _bo3(tong), giai_a),
                   (hoi_b, r"\left|\vv{F}\right| = %d \text{ N}" % do_lon,
                    giai_b),
                   (hoi_c, r"\vv{F_4} = %s" % _bo3(F4), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI (ra theo CHƯƠNG, thang a) NB - b) TH - c) VD - d) VDC)
# =====================================================================

def _bo_pytago_ngau_nhien(he_so=1):
    """Một bộ ba đã đảo thứ tự và đổi dấu ngẫu nhiên, kèm độ dài."""
    a, b, c = random.choice(BO_PYTAGO3)
    v = [a * he_so, b * he_so, c * he_so]
    random.shuffle(v)
    v = tuple(t * random.choice([-1, 1]) for t in v)
    return v, he_so * math.isqrt(a * a + b * b + c * c)


def L12_C2_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - vectơ trong không gian và hệ trục toạ độ (Bài 6, 7).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A = tuple(random.randint(-5, 5) for _ in range(3))
        p, dai_p = _bo_pytago_ngau_nhien()
        q, dai_q = _bo_pytago_ngau_nhien()
        if p == q:
            continue
        moi = (A, p, q, dai_p, dai_q)
        if moi not in gt:
            gt.append(moi)

    cauTF = ""
    for A, p, q, dai_p, dai_q in gt:
        B = tuple(A[i] + p[i] for i in range(3))
        C = tuple(A[i] + q[i] for i in range(3))
        D = tuple(A[i] + p[i] + q[i] for i in range(3))
        cham = _cham(p, q)
        binh_p = sum(t * t for t in p)

        debai = (r"Trong không gian $Oxyz$, cho ba điểm $%s$, $%s$, $%s$."
                 % (_diem("A", A), _diem("B", B), _diem("C", C)))

        ds_abcd = (
            # a) NB - đọc thẳng định nghĩa toạ độ vectơ
            [
                (r"{\True $\vv{AB} = %s$}" % _bo3(p),
                 r"Đúng. Toạ độ vectơ bằng toạ độ điểm ngọn trừ toạ độ "
                 r"điểm gốc: $\vv{AB} = %s$." % _bo3(p)),
                (r"{$\vv{AB} = %s$}" % _bo3(tuple(-t for t in p)),
                 r"Sai. Đó là toạ độ của $\vv{BA}$. Phải lấy toạ độ $B$ "
                 r"TRỪ toạ độ $A$, được $\vv{AB} = %s$." % _bo3(p)),
            ],
            # b) TH - một lần dùng công thức độ dài
            [
                (r"{\True $AB = %d$}" % dai_p,
                 r"Đúng. $AB = \sqrt{\left(%d\right)^2 + "
                 r"\left(%d\right)^2 + \left(%d\right)^2} = \sqrt{%d} "
                 r"= %d$." % (p[0], p[1], p[2], binh_p, dai_p)),
                (r"{$AB = %d$}" % binh_p,
                 r"Sai. Đó mới là $AB^2$. Còn phải khai căn: "
                 r"$AB = \sqrt{%d} = %d$." % (binh_p, dai_p)),
            ],
            # c) VD - phải lập hai vectơ rồi mới nhân vô hướng được
            [
                (r"{\True $\vv{AB}\cdot\vv{AC} = %d$}" % cham,
                 r"Đúng. $\vv{AB} = %s$, $\vv{AC} = %s$ nên"
                 % (_bo3(p), _bo3(q)) +
                 "\\\\\n"
                 r"$\vv{AB}\cdot\vv{AC} = %d\cdot%d + %d\cdot%d + "
                 r"%d\cdot%d = %d$."
                 % (p[0], q[0], p[1], q[1], p[2], q[2], cham)),
                (r"{$\vv{AB}\cdot\vv{AC} = %d$}" % (cham + dai_p),
                 r"Sai. Tích vô hướng là tổng các TÍCH của toạ độ tương "
                 r"ứng, kết quả đúng là $%d$." % cham),
            ],
            # d) VDC - phải hiểu quy tắc hình bình hành trong không gian
            [
                (r"{\True Điểm $D$ để $ABDC$ là hình bình hành có toạ "
                 r"độ $%s$}" % _bo3(D),
                 r"Đúng. $ABDC$ là hình bình hành khi "
                 r"$\vv{AB} = \vv{CD}$." +
                 "\\\\\n"
                 r"Suy ra $D = C + \vv{AB} = %s$." % _bo3(D)),
                (r"{Điểm $D$ để $ABDC$ là hình bình hành có toạ độ $%s$}"
                 % _bo3(tuple(A[i] - p[i] - q[i] for i in range(3))),
                 r"Sai. Từ $\vv{AB} = \vv{CD}$ ta được "
                 r"$D = C + \vv{AB}$, tức là $D%s$, không phải điểm đã "
                 r"nêu." % _bo3(D)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L12_C2_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - biểu thức toạ độ của các phép toán vectơ (Bài 8).

    Số liệu dựng NGƯỢC: chọn trước kết quả $2\vv{a} - \vv{b}$ là một bộ
    trong BO_PYTAGO3 rồi mới suy ra $\vv{b}$, nên độ dài ở ý d) là số
    nguyên.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        r, dai_r = _bo_pytago_ngau_nhien()
        a = tuple(random.randint(-5, 5) for _ in range(3))
        b = tuple(2 * a[i] - r[i] for i in range(3))
        if max(abs(t) for t in b) > 30 or b == (0, 0, 0) or a == (0, 0, 0):
            continue
        if (a, b) not in gt:
            gt.append((a, b, r, dai_r))

    cauTF = ""
    for a, b, r, dai_r in gt:
        tong = tuple(a[i] + b[i] for i in range(3))
        cham = _cham(a, b)
        binh_r = sum(t * t for t in r)

        debai = (r"Trong không gian $Oxyz$, cho hai vectơ "
                 r"$\vv{a} = %s$ và $\vv{b} = %s$."
                 % (_bo3(a), _bo3(b)))

        ds_abcd = (
            # a) NB - cộng hai vectơ theo từng thành phần
            [
                (r"{\True $\vv{a} + \vv{b} = %s$}" % _bo3(tong),
                 r"Đúng. Cộng hai vectơ thì cộng từng thành phần tương "
                 r"ứng, được $%s$." % _bo3(tong)),
                (r"{$\vv{a} + \vv{b} = %s$}"
                 % _bo3(tuple(a[i] - b[i] for i in range(3))),
                 r"Sai. Đó là $\vv{a} - \vv{b}$. Tổng hai vectơ là $%s$."
                 % _bo3(tong)),
            ],
            # b) TH - nhân với một số rồi trừ
            [
                (r"{\True $2\vv{a} - \vv{b} = %s$}" % _bo3(r),
                 r"Đúng. $2\vv{a} = %s$, trừ đi $\vv{b} = %s$ theo từng "
                 r"thành phần được $%s$."
                 % (_bo3(tuple(2 * t for t in a)), _bo3(b), _bo3(r))),
                (r"{$2\vv{a} - \vv{b} = %s$}"
                 % _bo3(tuple(2 * (a[i] - b[i]) for i in range(3))),
                 r"Sai. Hệ số $2$ chỉ nhân vào $\vv{a}$, không nhân vào "
                 r"$\vv{b}$. Kết quả đúng là $%s$." % _bo3(r)),
            ],
            # c) VD - tích vô hướng từ toạ độ
            [
                (r"{\True $\vv{a}\cdot\vv{b} = %d$}" % cham,
                 r"Đúng. $\vv{a}\cdot\vv{b} = %d\cdot%d + %d\cdot%d + "
                 r"%d\cdot%d = %d$."
                 % (a[0], b[0], a[1], b[1], a[2], b[2], cham)),
                (r"{$\vv{a}\cdot\vv{b} = %s$}"
                 % _bo3(tuple(a[i] * b[i] for i in range(3))),
                 r"Sai. Tích vô hướng là một SỐ, không phải một vectơ: "
                 r"phải cộng ba tích lại, được $%d$." % cham),
            ],
            # d) VDC - ghép phép toán với công thức độ dài
            [
                (r"{\True $\left|2\vv{a} - \vv{b}\right| = %d$}" % dai_r,
                 r"Đúng. Ở ý trên đã có $2\vv{a} - \vv{b} = %s$." % _bo3(r) +
                 "\\\\\n"
                 r"$\left|2\vv{a} - \vv{b}\right| = "
                 r"\sqrt{\left(%d\right)^2 + \left(%d\right)^2 + "
                 r"\left(%d\right)^2} = \sqrt{%d} = %d$."
                 % (r[0], r[1], r[2], binh_r, dai_r)),
                (r"{$\left|2\vv{a} - \vv{b}\right| = "
                 r"2\left|\vv{a}\right| - \left|\vv{b}\right|$}",
                 r"Sai. Độ dài KHÔNG cộng trừ được như vậy - đẳng thức "
                 r"này chỉ đúng khi hai vectơ cùng hướng." +
                 "\\\\\n"
                 r"Phải tính toạ độ $2\vv{a} - \vv{b} = %s$ rồi mới lấy "
                 r"độ dài, được $%d$." % (_bo3(r), dai_r)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
