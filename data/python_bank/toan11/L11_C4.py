# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 4. Quan hệ song song trong không gian
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Kiến thức dùng trong tệp:

  * Ba cách xác định mặt phẳng: qua ba điểm không thẳng hàng; qua một
    đường thẳng và một điểm ngoài nó; qua hai đường thẳng cắt nhau.
  * Hai mặt phẳng phân biệt có một điểm chung thì có một đường thẳng
    chung duy nhất (giao tuyến) đi qua điểm đó.
  * Hai đường thẳng trong không gian: cắt nhau, song song, trùng nhau
    (đồng phẳng) hoặc CHÉO NHAU (không đồng phẳng).
  * $d \parallel \left(P\right)$ khi $d$ và $\left(P\right)$ không có
    điểm chung; điều kiện đủ: $d \parallel d'$ với
    $d' \subset \left(P\right)$ và $d \not\subset \left(P\right)$.
  * $\left(P\right) \parallel \left(Q\right)$ khi hai mặt phẳng cắt nhau
    trong $\left(P\right)$ cùng song song với $\left(Q\right)$.
  * Định lí Thalès trong không gian: ba mặt phẳng đôi một song song chắn
    trên hai cát tuyến những đoạn thẳng TƯƠNG ỨNG TỈ LỆ.
  * Phép chiếu song song bảo toàn: tính thẳng hàng, tính song song, tỉ
    số độ dài của hai đoạn thẳng cùng phương; KHÔNG bảo toàn độ dài và
    số đo góc.

Số liệu chọn để ĐÁP SỐ ĐẸP: các bài dùng định lí Thalès đều chọn tỉ số
là phân số tối giản có mẫu nhỏ; câu trả lời ngắn luôn có đáp số viết
được đúng hai chữ số thập phân.

Bài học lớp 10 đã áp dụng: chữ tiếng Việt không nằm trần trong $...$;
không dùng **đậm**; mọi chuỗi có dấu gạch chéo đều là r"..."; mọi danh
sách phương án nhiễu đều qua _ba_nhieu4; hình vẽ bằng TikZ THUẦN
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
    s = "%.3f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _ba_nhieu4(dapso, ung_vien, buoc=None):
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


def _ps4(p, q=1):
    f = Fraction(p, q)
    if f.denominator == 1:
        return "%d" % f.numerator
    if f < 0:
        return r"-\dfrac{%d}{%d}" % (-f.numerator, f.denominator)
    return r"\dfrac{%d}{%d}" % (f.numerator, f.denominator)


# ---------------------------------------------------------------------
# HÌNH VẼ KHÔNG GIAN - TikZ THUẦN
# Quy ước nét đứt: cạnh bị khuất sau khối vẽ bằng nét đứt.
# ---------------------------------------------------------------------

def _khung(noi_dung, ti_le=1.0):
    return ("\\begin{tikzpicture}[scale=%s,>=stealth,line join=round,"
            "font=\\footnotesize]\n%s\n\\end{tikzpicture}"
            % (_toa(ti_le), "\n".join(noi_dung)))


def _diem(ra, ten, x, y, vi_tri="below"):
    ra.append("\\fill[black] (%s,%s) circle[radius=1.4pt] "
              "node[%s]{$%s$};" % (_toa(x), _toa(y), vi_tri, ten))


def _canh(ra, p, q, net="lien"):
    kieu = "" if net == "lien" else "[dashed]"
    ra.append("\\draw%s (%s,%s) -- (%s,%s);"
              % (kieu, _toa(p[0]), _toa(p[1]), _toa(q[0]), _toa(q[1])))


# Toạ độ chuẩn dùng lại cho mọi hình chóp tứ giác S.ABCD
TOA_CHOP4 = {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (5.3, 1.5),
             "D": (1.3, 1.5), "S": (2.4, 3.8)}

# Toạ độ chuẩn cho hình chóp tam giác (tứ diện) S.ABC hoặc ABCD
TOA_TUDIEN = {"A": (0.0, 0.0), "B": (4.2, 0.0), "C": (1.5, 1.4),
              "S": (2.0, 3.6), "D": (2.0, 3.6)}


def _hinh_chop_tu_giac(them=(), diem_them=()):
    r"""Hình chóp $S.ABCD$ có đáy là hình bình hành.

    Cạnh khuất: $AD$, $DC$ và $SD$ (đỉnh $D$ nằm phía sau).
    """
    T = TOA_CHOP4
    ra = []
    for p, q in (("A", "B"), ("B", "C"), ("S", "A"), ("S", "B"),
                 ("S", "C")):
        _canh(ra, T[p], T[q])
    for p, q in (("A", "D"), ("D", "C"), ("S", "D")):
        _canh(ra, T[p], T[q], "dut")
    for ten, vt in (("A", "below left"), ("B", "below right"),
                    ("C", "right"), ("D", "left"), ("S", "above")):
        _diem(ra, ten, T[ten][0], T[ten][1], vt)
    ra.extend(them)
    for ten, x, y, vt in diem_them:
        _diem(ra, ten, x, y, vt)
    return _khung(ra, 0.95)


def _hinh_tu_dien(ten_dinh="D", them=(), diem_them=()):
    r"""Tứ diện $ABC%s$ - cạnh khuất là các cạnh đi qua $C$ (đỉnh sau)."""
    T = TOA_TUDIEN
    ra = []
    for p, q in (("A", "B"), ("A", "S"), ("B", "S")):
        _canh(ra, T[p], T[q])
    for p, q in (("A", "C"), ("B", "C"), ("C", "S")):
        _canh(ra, T[p], T[q], "dut")
    for ten, vt in (("A", "below left"), ("B", "below right"),
                    ("C", "below")):
        _diem(ra, ten, T[ten][0], T[ten][1], vt)
    _diem(ra, ten_dinh, T["S"][0], T["S"][1], "above")
    ra.extend(them)
    for ten, x, y, vt in diem_them:
        _diem(ra, ten, x, y, vt)
    return _khung(ra, 0.95)


# Toạ độ chuẩn cho hình hộp ABCD.A'B'C'D'
def _toa_hop():
    dx, dy, h = 4.0, 1.5, 3.0
    lech = (1.3, dy)
    A = (0.0, 0.0)
    B = (dx, 0.0)
    C = (dx + lech[0], lech[1])
    D = (lech[0], lech[1])
    return {"A": A, "B": B, "C": C, "D": D,
            "A'": (A[0], A[1] + h), "B'": (B[0], B[1] + h),
            "C'": (C[0], C[1] + h), "D'": (D[0], D[1] + h)}


def _hinh_hop(them=(), diem_them=()):
    r"""Hình hộp $ABCD.A'B'C'D'$; cạnh khuất là các cạnh đi qua $D$."""
    T = _toa_hop()
    ra = []
    lien = [("A", "B"), ("B", "C"), ("A", "A'"), ("B", "B'"),
            ("C", "C'"), ("A'", "B'"), ("B'", "C'"), ("C'", "D'"),
            ("D'", "A'")]
    dut = [("A", "D"), ("D", "C"), ("D", "D'")]
    for p, q in lien:
        _canh(ra, T[p], T[q])
    for p, q in dut:
        _canh(ra, T[p], T[q], "dut")
    for ten, vt in (("A", "below left"), ("B", "below right"),
                    ("C", "right"), ("D", "left"),
                    ("A'", "left"), ("B'", "right"), ("C'", "right"),
                    ("D'", "above left")):
        _diem(ra, ten, T[ten][0], T[ten][1], vt)
    ra.extend(them)
    for ten, x, y, vt in diem_them:
        _diem(ra, ten, x, y, vt)
    return _khung(ra, 0.9)


# =====================================================================
# BÀI 10. ĐƯỜNG THẲNG VÀ MẶT PHẲNG TRONG KHÔNG GIAN
# =====================================================================

def L11_C4_B10_NB048_MC_A_01(socau, dang=1):
    r"""Quan hệ liên thuộc giữa điểm, đường thẳng, mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Nếu một đường thẳng có HAI điểm phân biệt thuộc một mặt phẳng "
         r"thì mọi điểm của đường thẳng đó đều thuộc mặt phẳng ấy.",
         [r"Nếu một đường thẳng có một điểm thuộc một mặt phẳng thì đường "
          r"thẳng đó nằm trong mặt phẳng ấy.",
          r"Một đường thẳng và một mặt phẳng luôn có đúng một điểm chung.",
          r"Hai mặt phẳng phân biệt luôn không có điểm chung."],
         r"Đây là một tính chất thừa nhận của hình học không gian: hai "
         r"điểm đã xác định duy nhất một đường thẳng, nên nếu cả hai cùng "
         r"nằm trong mặt phẳng thì cả đường thẳng nằm trong mặt phẳng."),
        (r"Nếu hai mặt phẳng phân biệt có một điểm chung thì chúng có một "
         r"đường thẳng chung duy nhất đi qua điểm đó.",
         [r"Hai mặt phẳng phân biệt có một điểm chung thì có vô số đường "
          r"thẳng chung.",
          r"Hai mặt phẳng phân biệt luôn có đúng một điểm chung.",
          r"Hai mặt phẳng phân biệt không thể có điểm chung."],
         r"Đường thẳng chung duy nhất đó gọi là GIAO TUYẾN của hai mặt "
         r"phẳng. Nếu có hai đường thẳng chung phân biệt thì hai mặt "
         r"phẳng sẽ trùng nhau."),
        (r"Có duy nhất một mặt phẳng đi qua ba điểm KHÔNG THẲNG HÀNG cho "
         r"trước.",
         [r"Có duy nhất một mặt phẳng đi qua ba điểm bất kì.",
          r"Có duy nhất một mặt phẳng đi qua hai điểm phân biệt.",
          r"Qua ba điểm thẳng hàng có duy nhất một mặt phẳng."],
         r"Nếu ba điểm THẲNG HÀNG thì có VÔ SỐ mặt phẳng đi qua chúng, "
         r"nên điều kiện ``không thẳng hàng'' là bắt buộc."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        dung, nhieu, ly_do = MAU[i]
        debai = r"Khẳng định nào sau đây ĐÚNG?"
        giai = dung + "\\\\\n" + ly_do
        cauTN += _MC_khong_cham(debai, dung, list(nhieu), giai, 0, 0,
                                   dang)
    return cauTN


def L11_C4_B10_NB053_MC_A_01(socau, dang=1):
    r"""Nhận biết hình chóp, hình tứ diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hình chóp $S.ABCD$ có bao nhiêu mặt?", "5",
         ["4", "6", "8"],
         r"Hình chóp $S.ABCD$ có $1$ mặt đáy $ABCD$ và $4$ mặt bên "
         r"$SAB$, $SBC$, $SCD$, $SDA$, tổng cộng $5$ mặt."),
        (r"Hình chóp $S.ABCD$ có bao nhiêu cạnh?", "8",
         ["4", "5", "6"],
         r"Có $4$ cạnh đáy $AB$, $BC$, $CD$, $DA$ và $4$ cạnh bên $SA$, "
         r"$SB$, $SC$, $SD$, tổng cộng $8$ cạnh."),
        (r"Hình tứ diện $ABCD$ có bao nhiêu mặt?", "4",
         ["3", "5", "6"],
         r"Bốn mặt của tứ diện là các tam giác $ABC$, $ABD$, $ACD$, "
         r"$BCD$."),
        (r"Hình tứ diện $ABCD$ có bao nhiêu cạnh?", "6",
         ["4", "5", "8"],
         r"Sáu cạnh là $AB$, $AC$, $AD$, $BC$, $BD$, $CD$; mỗi cặp trong "
         r"bốn đỉnh cho một cạnh."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dap, nhieu, ly_do = MAU[i]
        hinh = (_hinh_chop_tu_giac() if "chóp" in hoi
                else _hinh_tu_dien())
        dung = "$%s$" % dap
        cauTN += MC_SA_answer_text(hoi, dung, ["$%s$" % v for v in nhieu],
                                   ly_do, hinh, 0, dang)
    return cauTN


def L11_C4_B10_TH049_MC_A_01(socau, dang=1):
    r"""Ba cách xác định một mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Qua ba điểm không thẳng hàng xác định được bao nhiêu mặt "
         r"phẳng?", "1", ["0", "2", "vô số"],
         r"Đây là cách xác định mặt phẳng thứ nhất: ba điểm không thẳng "
         r"hàng xác định DUY NHẤT một mặt phẳng."),
        (r"Qua một đường thẳng và một điểm không thuộc đường thẳng đó xác "
         r"định được bao nhiêu mặt phẳng?", "1", ["0", "2", "vô số"],
         r"Đây là cách xác định mặt phẳng thứ hai. Lấy thêm hai điểm trên "
         r"đường thẳng, ta quay về ba điểm không thẳng hàng."),
        (r"Qua hai đường thẳng CẮT NHAU xác định được bao nhiêu mặt "
         r"phẳng?", "1", ["0", "2", "vô số"],
         r"Đây là cách xác định mặt phẳng thứ ba. Chú ý hai đường thẳng "
         r"CHÉO NHAU thì KHÔNG xác định được mặt phẳng nào."),
        (r"Qua hai điểm phân biệt xác định được bao nhiêu mặt phẳng?",
         "vô số", ["0", "1", "2"],
         r"Hai điểm chỉ xác định một ĐƯỜNG THẲNG; có vô số mặt phẳng chứa "
         r"đường thẳng đó."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dap, nhieu, ly_do = MAU[i]
        dung = ("$%s$" % dap) if dap.isdigit() else dap
        ds = [("$%s$" % v) if v.isdigit() else v for v in nhieu]
        cauTN += MC_SA_answer_text(hoi, dung, ds, ly_do, 0, 0, dang)
    return cauTN


def L11_C4_B10_TH050_MC_A_01(socau, dang=1):
    r"""Tìm giao tuyến của hai mặt phẳng trong hình chóp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"\left(SAC\right)", r"\left(SBD\right)", "SO",
         r"$O$ là giao điểm của hai đường chéo $AC$ và $BD$",
         ["SA", "SB", "AC"]),
        (r"\left(SAB\right)", r"\left(SCD\right)", "Sx",
         r"$Sx$ là đường thẳng qua $S$ và song song với $AB$, $CD$",
         ["SA", "SC", "AB"]),
        (r"\left(SAB\right)", r"\left(SBC\right)", "SB",
         r"$S$ và $B$ là hai điểm chung của hai mặt phẳng",
         ["SA", "SC", "AC"]),
        (r"\left(SAD\right)", r"\left(SCD\right)", "SD",
         r"$S$ và $D$ là hai điểm chung của hai mặt phẳng",
         ["SA", "SC", "AD"]),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        mp1, mp2, dap, ly_do, nhieu = MAU[i]
        hinh = _hinh_chop_tu_giac()
        dung = "$%s$" % dap
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình "
                 r"hành. Giao tuyến của hai mặt phẳng $%s$ và $%s$ là"
                 % (mp1, mp2))
        if dap == "SO":
            giai = (r"$S$ là điểm chung thứ nhất của $%s$ và $%s$."
                    % (mp1, mp2) +
                    "\\\\\n"
                    r"Gọi $O = AC \cap BD$. Vì $O \in AC \subset %s$ và "
                    r"$O \in BD \subset %s$ nên $O$ là điểm chung thứ hai."
                    % (mp1, mp2) +
                    "\\\\\n"
                    r"Hai mặt phẳng phân biệt có hai điểm chung $S$ và "
                    r"$O$ nên giao tuyến là đường thẳng $SO$.")
        elif dap == "Sx":
            giai = (r"$S$ là điểm chung của $%s$ và $%s$." % (mp1, mp2) +
                    "\\\\\n"
                    r"Trong $%s$ có $AB$, trong $%s$ có $CD$, mà "
                    r"$AB \parallel CD$ (hai cạnh đối hình bình hành)."
                    % (mp1, mp2) +
                    "\\\\\n"
                    r"Theo định lí về giao tuyến của ba mặt phẳng, giao "
                    r"tuyến là đường thẳng $Sx$ đi qua $S$ và song song "
                    r"với $AB$ (và $CD$).")
        else:
            giai = (r"%s, nên giao tuyến của chúng là đường thẳng $%s$."
                    % (ly_do, dap) +
                    "\\\\\n"
                    r"Hai mặt phẳng phân biệt có hai điểm chung thì giao "
                    r"tuyến chính là đường thẳng đi qua hai điểm đó.")
        cauTN += MC_SA_answer_text(debai, dung,
                                   ["$%s$" % v for v in nhieu], giai,
                                   hinh, 0, dang)
    return cauTN


def L11_C4_B10_TH050_TL_A_01(socau, dong=1):
    r"""Tự luận: xác định giao tuyến của hai mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"tâm $O$ (giao điểm hai đường chéo).")

        hoi_a = r"Tìm giao tuyến của $\left(SAC\right)$ và $\left(SBD\right)$."
        giai_a = (r"$S$ thuộc cả hai mặt phẳng nên là điểm chung thứ nhất." +
                  "\\\\\n"
                  r"$O = AC \cap BD$ mà $AC \subset \left(SAC\right)$ và "
                  r"$BD \subset \left(SBD\right)$, nên $O$ là điểm chung "
                  r"thứ hai." +
                  "\\\\\n"
                  r"Vậy $\left(SAC\right) \cap \left(SBD\right) = SO$.")

        hoi_b = r"Tìm giao tuyến của $\left(SAB\right)$ và $\left(SCD\right)$."
        giai_b = (r"$S$ là điểm chung của hai mặt phẳng." +
                  "\\\\\n"
                  r"$AB \subset \left(SAB\right)$, "
                  r"$CD \subset \left(SCD\right)$ và $AB \parallel CD$ "
                  r"(hai cạnh đối của hình bình hành)." +
                  "\\\\\n"
                  r"Theo định lí về giao tuyến của ba mặt phẳng, giao "
                  r"tuyến là đường thẳng $Sx$ qua $S$ và song song với "
                  r"$AB$.")

        hoi_c = (r"Gọi $M$ là trung điểm $SA$. Tìm giao tuyến của "
                 r"$\left(MBD\right)$ và $\left(SAC\right)$.")
        giai_c = (r"$M \in SA \subset \left(SAC\right)$ và "
                  r"$M \in \left(MBD\right)$ nên $M$ là điểm chung thứ "
                  r"nhất." +
                  "\\\\\n"
                  r"$O \in BD \subset \left(MBD\right)$ và "
                  r"$O \in AC \subset \left(SAC\right)$ nên $O$ là điểm "
                  r"chung thứ hai." +
                  "\\\\\n"
                  r"Vậy $\left(MBD\right) \cap \left(SAC\right) = MO$.")

        ds_abcd = [(hoi_a, r"SO", giai_a),
                   (hoi_b, r"Sx \parallel AB", giai_b),
                   (hoi_c, r"MO", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C4_B10_TH051_MC_A_01(socau, dang=1):
    r"""Tìm giao điểm của đường thẳng và mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"đường thẳng $SO$ và mặt phẳng $\left(ABCD\right)$", "O",
         ["S", "A", "C"],
         r"$O \in AC \subset \left(ABCD\right)$ và $O \in SO$, mà $SO$ "
         r"không nằm trong $\left(ABCD\right)$ nên $O$ là giao điểm duy "
         r"nhất."),
        (r"đường thẳng $SA$ và mặt phẳng $\left(ABCD\right)$", "A",
         ["S", "O", "B"],
         r"$A$ vừa thuộc $SA$ vừa thuộc $\left(ABCD\right)$; $SA$ không "
         r"nằm trong $\left(ABCD\right)$ nên giao điểm duy nhất là $A$."),
        (r"đường thẳng $AC$ và mặt phẳng $\left(SBD\right)$", "O",
         ["A", "C", "S"],
         r"$O = AC \cap BD$ mà $BD \subset \left(SBD\right)$, nên "
         r"$O \in AC \cap \left(SBD\right)$; $AC$ không nằm trong "
         r"$\left(SBD\right)$ nên giao điểm duy nhất là $O$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        mo_ta, dap, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành tâm "
                 r"$O$. Giao điểm của %s là điểm nào?" % mo_ta)
        giai = (r"Muốn tìm giao điểm của một đường thẳng với một mặt "
                r"phẳng, ta tìm một điểm vừa thuộc đường thẳng vừa thuộc "
                r"mặt phẳng." +
                "\\\\\n" + ly_do)
        cauTN += MC_SA_answer_text(debai, "$%s$" % dap,
                                   ["$%s$" % v for v in nhieu], giai,
                                   hinh, 0, dang)
    return cauTN


def L11_C4_B10_TH051_TL_A_01(socau, dong=1):
    r"""Tự luận: xác định giao điểm của đường thẳng và mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"tâm $O$. Gọi $M$ là trung điểm của $SC$.")

        hoi_a = (r"Tìm giao điểm của đường thẳng $SO$ với mặt phẳng "
                 r"$\left(ABCD\right)$.")
        giai_a = (r"$O \in AC \subset \left(ABCD\right)$ và $O \in SO$." +
                  "\\\\\n"
                  r"Vì $SO \not\subset \left(ABCD\right)$ nên $O$ là giao "
                  r"điểm duy nhất.")

        hoi_b = (r"Tìm giao điểm của đường thẳng $AM$ với mặt phẳng "
                 r"$\left(SBD\right)$.")
        giai_b = (r"Xét mặt phẳng phụ $\left(SAC\right)$ chứa $AM$." +
                  "\\\\\n"
                  r"$\left(SAC\right) \cap \left(SBD\right) = SO$." +
                  "\\\\\n"
                  r"Trong mặt phẳng $\left(SAC\right)$, gọi "
                  r"$I = AM \cap SO$." +
                  "\\\\\n"
                  r"Khi đó $I \in AM$ và $I \in SO \subset "
                  r"\left(SBD\right)$, nên $I$ là giao điểm cần tìm.")

        hoi_c = (r"Nêu các bước chung để tìm giao điểm của một đường "
                 r"thẳng $d$ với một mặt phẳng $\left(P\right)$.")
        giai_c = (r"Bước 1: chọn một mặt phẳng phụ $\left(Q\right)$ chứa "
                  r"$d$ và cắt $\left(P\right)$." +
                  "\\\\\n"
                  r"Bước 2: tìm giao tuyến $a$ của $\left(P\right)$ và "
                  r"$\left(Q\right)$." +
                  "\\\\\n"
                  r"Bước 3: trong $\left(Q\right)$, tìm giao điểm của $d$ "
                  r"với $a$; đó chính là giao điểm của $d$ với "
                  r"$\left(P\right)$.")

        ds_abcd = [(hoi_a, r"O", giai_a),
                   (hoi_b, r"I = AM \cap SO", giai_b),
                   (hoi_c, r"\text{Dùng mặt phẳng phụ chứa } d", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C4_B10_VD052_MC_A_01(socau, dang=1):
    r"""Thiết diện của hình chóp - số cạnh của thiết diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Gọi $M$, $N$ "
         r"lần lượt là trung điểm của $SB$, $SD$. Thiết diện của hình "
         r"chóp cắt bởi mặt phẳng $\left(AMN\right)$ là đa giác có bao "
         r"nhiêu cạnh?", "4", ["3", "5", "6"],
         r"Mặt phẳng $\left(AMN\right)$ cắt các mặt $\left(SAB\right)$, "
         r"$\left(SBC\right)$, $\left(SCD\right)$, $\left(SAD\right)$." +
         "\\\\\n" +
         r"Nó cắt $SC$ tại một điểm $P$, nên thiết diện là tứ giác "
         r"$AMPN$ - đa giác có $4$ cạnh."),
        (r"Cho hình chóp $S.ABCD$. Thiết diện của hình chóp cắt bởi mặt "
         r"phẳng $\left(SAC\right)$ là đa giác có bao nhiêu cạnh?",
         "3", ["4", "5", "6"],
         r"$\left(SAC\right)$ cắt hình chóp theo tam giác $SAC$ (mặt "
         r"phẳng này chứa $S$, $A$, $C$ đều là đỉnh của hình chóp)." +
         "\\\\\n" +
         r"Vậy thiết diện là tam giác, có $3$ cạnh."),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Gọi $M$ là "
         r"trung điểm $SA$. Thiết diện cắt bởi mặt phẳng $\left(MBC"
         r"\right)$ là đa giác có bao nhiêu cạnh?", "4", ["3", "5", "6"],
         r"$\left(MBC\right)$ chứa $BC$ mà $BC \parallel AD$, nên giao "
         r"tuyến với $\left(SAD\right)$ là đường thẳng qua $M$ song song "
         r"với $AD$, cắt $SD$ tại $N$." +
         "\\\\\n" +
         r"Thiết diện là tứ giác $MBCN$ - có $4$ cạnh."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dap, nhieu, giai = MAU[i]
        hinh = _hinh_chop_tu_giac()
        cauTN += MC_SA_answer_text(hoi, "$%s$" % dap,
                                   ["$%s$" % v for v in nhieu], giai,
                                   hinh, 0, dang)
    return cauTN


def L11_C4_B10_VD052_SA_A_01(socau):
    r"""Đếm giao tuyến, cặp cạnh chéo nhau - trả lời ngắn (NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình tứ diện $ABCD$. Trong sáu cạnh của tứ diện, có bao "
         r"nhiêu cặp cạnh CHÉO NHAU?", 3, "tudien",
         r"Hai cạnh chéo nhau là hai cạnh không có đỉnh chung." +
         "\\\\\n" +
         r"Các cặp đó là $AB$ và $CD$; $AC$ và $BD$; $AD$ và $BC$." +
         "\\\\\n" +
         r"Vậy có $3$ cặp cạnh chéo nhau."),
        (r"Cho hình tứ diện $ABCD$. Có bao nhiêu mặt phẳng đi qua ba "
         r"trong bốn đỉnh của tứ diện?", 4, "tudien",
         r"Mỗi cách chọn $3$ đỉnh trong $4$ đỉnh cho một mặt phẳng, và "
         r"bốn đỉnh của tứ diện không đồng phẳng nên bốn mặt phẳng đó "
         r"phân biệt." + "\\\\\n" +
         r"Số mặt phẳng là $C_{4}^{3} = 4$."),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Có bao nhiêu "
         r"cạnh của hình chóp chéo nhau với cạnh $AB$?", 2, "chop4",
         r"Cạnh chéo với $AB$ là cạnh không cắt $AB$ và không cùng nằm "
         r"trong một mặt phẳng với $AB$." + "\\\\\n" +
         r"Đó là $SC$ và $SD$. (Các cạnh $BC$, $AD$, $SA$, $SB$ đều cắt "
         r"$AB$; còn $CD \parallel AB$.)" + "\\\\\n" +
         r"Vậy có $2$ cạnh."),
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Có bao nhiêu cạnh của hình hộp "
         r"song song với cạnh $AB$?", 3, "hop",
         r"Các cạnh song song với $AB$ là $CD$, $A'B'$ và $C'D'$." +
         "\\\\\n" +
         r"Vậy có $3$ cạnh (không kể chính $AB$)."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cau = ""
    for i in gt:
        hoi, dap, loai, giai = MAU[i]
        hinh = {"tudien": _hinh_tu_dien(), "chop4": _hinh_chop_tu_giac(),
                "hop": _hinh_hop()}[loai]
        nhieu = _ba_nhieu4(str(dap), [str(dap + 1), str(dap - 1),
                                      str(2 * dap)],
                           buoc=lambda t: str(dap + t + 1))
        cau += MC_SA_answer_const(hoi, str(dap), nhieu, giai, hinh, 0, 2)
    return cau


def L11_C4_B10_VD052_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thiết diện của hình chóp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình "
                 r"hành. Gọi $M$ là trung điểm của cạnh $SA$.")

        hoi_a = (r"Tìm giao tuyến của $\left(MBC\right)$ và "
                 r"$\left(SAD\right)$.")
        giai_a = (r"$M \in SA \subset \left(SAD\right)$ và "
                  r"$M \in \left(MBC\right)$ nên $M$ là điểm chung." +
                  "\\\\\n"
                  r"$BC \subset \left(MBC\right)$, "
                  r"$AD \subset \left(SAD\right)$ và $BC \parallel AD$." +
                  "\\\\\n"
                  r"Vậy giao tuyến là đường thẳng qua $M$ và song song "
                  r"với $AD$; gọi $N$ là giao điểm của đường thẳng đó với "
                  r"$SD$ thì giao tuyến là $MN$.")

        hoi_b = (r"Xác định thiết diện của hình chóp khi cắt bởi mặt "
                 r"phẳng $\left(MBC\right)$.")
        giai_b = (r"$\left(MBC\right)$ cắt $\left(SAB\right)$ theo $MB$, "
                  r"cắt $\left(ABCD\right)$ theo $BC$," +
                  "\\\\\n"
                  r"cắt $\left(SCD\right)$ theo $CN$ và cắt "
                  r"$\left(SAD\right)$ theo $NM$." +
                  "\\\\\n"
                  r"Vậy thiết diện là tứ giác $MBCN$.")

        hoi_c = r"Chứng minh thiết diện $MBCN$ là một hình thang."
        giai_c = (r"Theo câu a, $MN \parallel AD$." +
                  "\\\\\n"
                  r"Mà $BC \parallel AD$ (hai cạnh đối của hình bình "
                  r"hành), nên $MN \parallel BC$." +
                  "\\\\\n"
                  r"Tứ giác $MBCN$ có $MN \parallel BC$ nên là hình "
                  r"thang." +
                  "\\\\\n"
                  r"(Thêm: $MN$ là đường trung bình của tam giác $SAD$ "
                  r"nên $MN = \dfrac{1}{2}AD = \dfrac{1}{2}BC$, do đó "
                  r"$MBCN$ không phải hình bình hành.)")

        ds_abcd = [(hoi_a, r"MN \parallel AD", giai_a),
                   (hoi_b, r"\text{Tứ giác } MBCN", giai_b),
                   (hoi_c, r"MN \parallel BC", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C4_B10_VD054_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về đường thẳng, mặt phẳng trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([4, 5, 6, 7])
        if n not in gt:
            gt.append(n)

    cauTN = ""
    for n in gt:
        so = math.comb(n, 3)
        dung = "$%d$" % so
        nhieu = _ba_nhieu4(dung,
                           ["$%d$" % math.comb(n, 2), "$%d$" % n,
                            "$%d$" % math.comb(n, 4)],
                           buoc=lambda t: "$%d$" % (so + t))
        debai = (r"Trong không gian cho $%d$ điểm phân biệt, trong đó "
                 r"không có bốn điểm nào đồng phẳng. Có bao nhiêu mặt "
                 r"phẳng đi qua ba trong $%d$ điểm đó?" % (n, n))
        giai = (r"Vì không có bốn điểm nào đồng phẳng nên cũng không có "
                r"ba điểm nào thẳng hàng." +
                "\\\\\n"
                r"Do đó mỗi cách chọn $3$ điểm cho đúng MỘT mặt phẳng, và "
                r"hai cách chọn khác nhau cho hai mặt phẳng khác nhau." +
                "\\\\\n"
                r"Số mặt phẳng là $C_{%d}^{3} = %d$." % (n, so) +
                "\\\\\n"
                r"Chú ý nếu có bốn điểm đồng phẳng thì phải trừ bớt, vì "
                r"bốn điểm đó chỉ cho MỘT mặt phẳng chứ không phải $4$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C4_B10_VD054_SA_A_01(socau):
    r"""Đếm mặt phẳng, giao tuyến - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([4, 5, 6, 7, 8])
        if n not in gt:
            gt.append(n)

    cau = ""
    for n in gt:
        so = math.comb(n, 3)
        debai = (r"Trong không gian cho $%d$ điểm phân biệt, trong đó "
                 r"không có bốn điểm nào đồng phẳng. Hỏi có bao nhiêu mặt "
                 r"phẳng đi qua ba trong $%d$ điểm đó?" % (n, n))
        giai = (r"Không có bốn điểm nào đồng phẳng nên cũng không có ba "
                r"điểm nào thẳng hàng; mỗi bộ ba điểm cho đúng một mặt "
                r"phẳng." +
                "\\\\\n"
                r"Số mặt phẳng là $C_{%d}^{3} = "
                r"\dfrac{%d\cdot %d\cdot %d}{6} = %d$."
                % (n, n, n - 1, n - 2, so))
        nhieu = _ba_nhieu4(str(so), [str(math.comb(n, 2)), str(n),
                                     str(so + 1)],
                           buoc=lambda t: str(so + t + 1))
        cau += MC_SA_answer_const(debai, str(so), nhieu, giai, 0, 0, 2)
    return cau


def L11_C4_B10_VD054_TL_A_01(socau, dong=1):
    r"""Tự luận: tổng hợp về đường thẳng và mặt phẳng trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_tu_dien()
        debai = (r"Cho hình tứ diện $ABCD$. Gọi $M$, $N$ lần lượt là "
                 r"trung điểm của $AB$ và $CD$.")

        hoi_a = (r"Chứng minh rằng hai đường thẳng $AB$ và $CD$ chéo "
                 r"nhau.")
        giai_a = (r"Giả sử $AB$ và $CD$ đồng phẳng, tức cùng nằm trong "
                  r"một mặt phẳng $\left(P\right)$." +
                  "\\\\\n"
                  r"Khi đó bốn điểm $A$, $B$, $C$, $D$ đều thuộc "
                  r"$\left(P\right)$, tức là bốn đỉnh đồng phẳng." +
                  "\\\\\n"
                  r"Điều này trái với giả thiết $ABCD$ là tứ diện. Vậy "
                  r"$AB$ và $CD$ chéo nhau.")

        hoi_b = (r"Tìm giao tuyến của hai mặt phẳng $\left(ABN\right)$ "
                 r"và $\left(CDM\right)$.")
        giai_b = (r"$M$ là trung điểm $AB$ nên "
                  r"$M \in AB \subset \left(ABN\right)$; "
                  r"$M \in \left(CDM\right)$." +
                  "\\\\\n"
                  r"$N$ là trung điểm $CD$ nên "
                  r"$N \in CD \subset \left(CDM\right)$; "
                  r"$N \in \left(ABN\right)$." +
                  "\\\\\n"
                  r"Hai mặt phẳng phân biệt có hai điểm chung $M$, $N$ "
                  r"nên giao tuyến là đường thẳng $MN$.")

        hoi_c = (r"Gọi $G$ là trọng tâm tam giác $BCD$. Tìm giao điểm của "
                 r"đường thẳng $AG$ với mặt phẳng $\left(BCD\right)$.")
        giai_c = (r"$G$ là trọng tâm tam giác $BCD$ nên "
                  r"$G \in \left(BCD\right)$." +
                  "\\\\\n"
                  r"Mặt khác $G \in AG$." +
                  "\\\\\n"
                  r"Vì $A \notin \left(BCD\right)$ nên "
                  r"$AG \not\subset \left(BCD\right)$, do đó $G$ là giao "
                  r"điểm DUY NHẤT.")

        ds_abcd = [(hoi_a, r"AB \text{ và } CD \text{ chéo nhau}", giai_a),
                   (hoi_b, r"MN", giai_b), (hoi_c, r"G", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 11. HAI ĐƯỜNG THẲNG SONG SONG
# =====================================================================

def L11_C4_B11_NB055_MC_A_01(socau, dang=1):
    r"""Vị trí tương đối của hai đường thẳng trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hai đường thẳng phân biệt trong không gian có thể ở những vị "
         r"trí tương đối nào?",
         r"Cắt nhau, song song hoặc chéo nhau",
         [r"Chỉ cắt nhau hoặc song song",
          r"Chỉ song song hoặc chéo nhau",
          r"Luôn luôn chéo nhau"],
         r"Hai đường thẳng phân biệt hoặc ĐỒNG PHẲNG (khi đó cắt nhau "
         r"hoặc song song), hoặc KHÔNG đồng phẳng (khi đó chéo nhau)."),
        (r"Hai đường thẳng gọi là CHÉO NHAU khi nào?",
         r"Khi chúng không cùng nằm trong bất kì mặt phẳng nào",
         [r"Khi chúng không có điểm chung",
          r"Khi chúng cùng nằm trong một mặt phẳng và không cắt nhau",
          r"Khi chúng vuông góc với nhau"],
         r"Hai đường thẳng SONG SONG cũng không có điểm chung, nhưng "
         r"chúng ĐỒNG PHẲNG. Điểm khác biệt của hai đường chéo nhau là "
         r"không có mặt phẳng nào chứa cả hai."),
        (r"Hai đường thẳng gọi là SONG SONG khi nào?",
         r"Khi chúng đồng phẳng và không có điểm chung",
         [r"Khi chúng không có điểm chung",
          r"Khi chúng không cùng nằm trong một mặt phẳng nào",
          r"Khi chúng có đúng một điểm chung"],
         r"Điều kiện ``đồng phẳng'' là bắt buộc, nếu thiếu thì hai đường "
         r"chéo nhau cũng thoả mãn."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu),
                                   dung + "." + "\\\\\n" + ly_do,
                                   0, 0, dang)
    return cauTN


def L11_C4_B11_TH056_MC_A_01(socau, dang=1):
    r"""Tính chất cơ bản về hai đường thẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Trong không gian, qua một điểm không thuộc đường thẳng $d$, có "
         r"bao nhiêu đường thẳng song song với $d$?",
         "1", ["0", "2", "vô số"],
         r"Đây là tính chất thừa nhận: qua một điểm ngoài một đường "
         r"thẳng có DUY NHẤT một đường thẳng song song với đường thẳng "
         r"đó."),
        (r"Trong không gian, hai đường thẳng phân biệt cùng song song với "
         r"đường thẳng thứ ba thì",
         r"song song với nhau",
         [r"cắt nhau", r"chéo nhau",
          r"có thể cắt nhau hoặc chéo nhau"],
         r"Tính chất bắc cầu vẫn đúng trong không gian: "
         r"$a \parallel c$ và $b \parallel c$ với $a \neq b$ thì "
         r"$a \parallel b$."),
        (r"Cho ba mặt phẳng đôi một cắt nhau theo ba giao tuyến phân "
         r"biệt. Khi đó ba giao tuyến ấy",
         r"hoặc đồng quy hoặc đôi một song song",
         [r"luôn đồng quy", r"luôn đôi một song song",
          r"luôn đôi một chéo nhau"],
         r"Đây là định lí về giao tuyến của ba mặt phẳng, dùng rất nhiều "
         r"khi tìm giao tuyến có chứa yếu tố song song."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dap, nhieu, ly_do = MAU[i]
        dung = ("$%s$" % dap) if dap.isdigit() else dap
        ds = [("$%s$" % v) if v.isdigit() else v for v in nhieu]
        cauTN += MC_SA_answer_text(hoi, dung, ds, ly_do, 0, 0, dang)
    return cauTN


def L11_C4_B11_VD057_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về hai đường thẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình tứ diện $ABCD$. Gọi $M$, $N$, $P$, $Q$ lần lượt là "
         r"trung điểm của $AB$, $BC$, $CD$, $DA$. Tứ giác $MNPQ$ là hình "
         r"gì?", r"Hình bình hành",
         [r"Hình thang không phải hình bình hành", r"Hình thoi",
          r"Tứ giác không có cặp cạnh nào song song"],
         r"$MN$ là đường trung bình tam giác $ABC$ nên "
         r"$MN \parallel AC$ và $MN = \dfrac{1}{2}AC$." + "\\\\\n" +
         r"$QP$ là đường trung bình tam giác $ACD$ nên "
         r"$QP \parallel AC$ và $QP = \dfrac{1}{2}AC$." + "\\\\\n" +
         r"Vậy $MN \parallel QP$ và $MN = QP$, nên $MNPQ$ là hình bình "
         r"hành.", "tudien"),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Gọi $M$, $N$ "
         r"lần lượt là trung điểm của $SA$, $SB$. Khi đó $MN$ và $CD$",
         r"song song với nhau",
         [r"cắt nhau", r"chéo nhau", r"trùng nhau"],
         r"$MN$ là đường trung bình tam giác $SAB$ nên "
         r"$MN \parallel AB$." + "\\\\\n" +
         r"Mà $AB \parallel CD$ (hai cạnh đối hình bình hành)." +
         "\\\\\n" +
         r"Theo tính chất bắc cầu, $MN \parallel CD$.", "chop4"),
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Đường thẳng $AB$ và đường thẳng "
         r"$C'D'$ có vị trí tương đối nào?",
         r"Song song với nhau",
         [r"Cắt nhau", r"Chéo nhau", r"Trùng nhau"],
         r"$AB \parallel CD$ (đáy là hình bình hành) và "
         r"$CD \parallel C'D'$ (mặt bên $CDD'C'$ là hình bình hành)." +
         "\\\\\n" +
         r"Theo tính chất bắc cầu, $AB \parallel C'D'$.", "hop"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, giai, loai = MAU[i]
        hinh = {"tudien": _hinh_tu_dien(), "chop4": _hinh_chop_tu_giac(),
                "hop": _hinh_hop()}[loai]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), giai, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B11_VD057_SA_A_01(socau):
    r"""Độ dài đoạn nối trung điểm - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([4, 6, 8, 10, 12, 14, 16])
        if a not in gt:
            gt.append(a)

    cau = ""
    for a in gt:
        kq = Fraction(a, 2)
        hinh = _hinh_tu_dien()
        debai = (r"Cho hình tứ diện $ABCD$ có $AC = %d$. Gọi $M$, $N$ lần "
                 r"lượt là trung điểm của $AB$ và $BC$. Tính độ dài đoạn "
                 r"thẳng $MN$." % a)
        giai = (r"$M$, $N$ lần lượt là trung điểm của $AB$, $BC$ nên $MN$ "
                r"là ĐƯỜNG TRUNG BÌNH của tam giác $ABC$." +
                "\\\\\n"
                r"Do đó $MN \parallel AC$ và $MN = \dfrac{1}{2}AC$." +
                "\\\\\n"
                r"$MN = \dfrac{1}{2}\cdot %d = %s$." % (a, _xx(kq)))
        nhieu = _ba_nhieu4(_xx(kq), [str(a), _xx(Fraction(a, 4)),
                                     str(2 * a)],
                           buoc=lambda t: _xx(float(kq) + t))
        cau += MC_SA_answer_const(debai, _xx(kq), nhieu, giai, hinh, 0, 2)
    return cau


def L11_C4_B11_VD057_TL_A_01(socau, dong=1):
    r"""Tự luận: chứng minh hai đường thẳng song song trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_tu_dien()
        debai = (r"Cho hình tứ diện $ABCD$. Gọi $M$, $N$, $P$, $Q$ lần "
                 r"lượt là trung điểm của các cạnh $AB$, $BC$, $CD$, "
                 r"$DA$.")

        hoi_a = r"Chứng minh $MN \parallel AC$ và $QP \parallel AC$."
        giai_a = (r"Trong tam giác $ABC$, $M$ và $N$ là trung điểm của "
                  r"$AB$ và $BC$ nên $MN$ là đường trung bình." +
                  "\\\\\n"
                  r"Do đó $MN \parallel AC$ và $MN = \dfrac{1}{2}AC$." +
                  "\\\\\n"
                  r"Tương tự, trong tam giác $ACD$, $Q$ và $P$ là trung "
                  r"điểm của $DA$ và $CD$ nên $QP \parallel AC$ và "
                  r"$QP = \dfrac{1}{2}AC$.")

        hoi_b = r"Chứng minh tứ giác $MNPQ$ là hình bình hành."
        giai_b = (r"Từ câu a: $MN \parallel AC$ và $QP \parallel AC$ nên "
                  r"$MN \parallel QP$ (tính chất bắc cầu)." +
                  "\\\\\n"
                  r"Lại có $MN = QP = \dfrac{1}{2}AC$." +
                  "\\\\\n"
                  r"Tứ giác $MNPQ$ có một cặp cạnh đối vừa song song vừa "
                  r"bằng nhau nên là hình bình hành.")

        hoi_c = (r"Suy ra rằng $MP$ và $NQ$ cắt nhau tại trung điểm của "
                 r"mỗi đường.")
        giai_c = (r"$MP$ và $NQ$ chính là hai đường chéo của hình bình "
                  r"hành $MNPQ$." +
                  "\\\\\n"
                  r"Hai đường chéo của hình bình hành cắt nhau tại trung "
                  r"điểm của mỗi đường." +
                  "\\\\\n"
                  r"Điểm đó được gọi là trọng tâm của tứ diện $ABCD$.")

        ds_abcd = [(hoi_a, r"MN \parallel AC \parallel QP", giai_a),
                   (hoi_b, r"MNPQ \text{ là hình bình hành}", giai_b),
                   (hoi_c, r"MP \cap NQ \text{ tại trung điểm mỗi đường}",
                    giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 12. ĐƯỜNG THẲNG SONG SONG VỚI MẶT PHẲNG
# =====================================================================

def L11_C4_B12_NB058_MC_A_01(socau, dang=1):
    r"""Nhận biết đường thẳng song song với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Đường thẳng $d$ gọi là song song với mặt phẳng "
         r"$\left(P\right)$ khi nào?",
         r"Khi $d$ và $\left(P\right)$ không có điểm chung",
         [r"Khi $d$ nằm trong $\left(P\right)$",
          r"Khi $d$ và $\left(P\right)$ có đúng một điểm chung",
          r"Khi $d$ song song với mọi đường thẳng nằm trong "
          r"$\left(P\right)$"],
         r"Giữa $d$ và $\left(P\right)$ chỉ có ba khả năng: cắt nhau "
         r"(một điểm chung), $d$ nằm trong $\left(P\right)$ (vô số điểm "
         r"chung), hoặc song song (không có điểm chung)."),
        (r"Nếu đường thẳng $d$ song song với mặt phẳng $\left(P\right)$ "
         r"thì $d$ và một đường thẳng $a$ bất kì nằm trong "
         r"$\left(P\right)$",
         r"song song hoặc chéo nhau",
         [r"luôn song song", r"luôn chéo nhau", r"có thể cắt nhau"],
         r"$d$ và $a$ không có điểm chung (vì $d$ không cắt "
         r"$\left(P\right)$), nên chúng song song nếu đồng phẳng và chéo "
         r"nhau nếu không đồng phẳng." + "\\\\\n" +
         r"Chúng KHÔNG thể cắt nhau, vì điểm cắt sẽ là điểm chung của "
         r"$d$ và $\left(P\right)$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C4_B12_TH059_MC_A_01(socau, dang=1):
    r"""Điều kiện để đường thẳng song song với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Điều kiện nào sau đây ĐỦ để kết luận đường thẳng $d$ song song "
         r"với mặt phẳng $\left(P\right)$?",
         r"$d \not\subset \left(P\right)$ và $d$ song song với một đường "
         r"thẳng nằm trong $\left(P\right)$",
         [r"$d$ song song với một đường thẳng nằm trong "
          r"$\left(P\right)$",
          r"$d$ không cắt một đường thẳng nào nằm trong "
          r"$\left(P\right)$",
          r"$d$ song song với một đường thẳng song song với "
          r"$\left(P\right)$"],
         r"Thiếu điều kiện $d \not\subset \left(P\right)$ thì $d$ có thể "
         r"NẰM TRONG $\left(P\right)$, khi đó $d$ không song song với "
         r"$\left(P\right)$."),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Gọi $M$, $N$ "
         r"là trung điểm $SA$, $SB$. Khẳng định nào sau đây ĐÚNG?",
         r"$MN \parallel \left(ABCD\right)$",
         [r"$MN \subset \left(ABCD\right)$",
          r"$MN$ cắt $\left(ABCD\right)$",
          r"$MN \parallel SC$"],
         r"$MN$ là đường trung bình tam giác $SAB$ nên "
         r"$MN \parallel AB$." + "\\\\\n" +
         r"Mà $AB \subset \left(ABCD\right)$ và "
         r"$MN \not\subset \left(ABCD\right)$." + "\\\\\n" +
         r"Vậy $MN \parallel \left(ABCD\right)$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_tu_giac() if "hình chóp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B12_TH059_TL_A_01(socau, dong=1):
    r"""Tự luận: chứng minh đường thẳng song song với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình "
                 r"hành. Gọi $M$, $N$ lần lượt là trung điểm của $SA$ và "
                 r"$SB$.")

        hoi_a = r"Chứng minh $MN \parallel \left(ABCD\right)$."
        giai_a = (r"Trong tam giác $SAB$, $M$ và $N$ là trung điểm của "
                  r"$SA$ và $SB$ nên $MN$ là đường trung bình." +
                  "\\\\\n"
                  r"Do đó $MN \parallel AB$." +
                  "\\\\\n"
                  r"Mà $AB \subset \left(ABCD\right)$ và "
                  r"$MN \not\subset \left(ABCD\right)$." +
                  "\\\\\n"
                  r"Vậy $MN \parallel \left(ABCD\right)$.")

        hoi_b = r"Chứng minh $MN \parallel \left(SCD\right)$."
        giai_b = (r"Theo câu a, $MN \parallel AB$." +
                  "\\\\\n"
                  r"Mà $AB \parallel CD$ (hai cạnh đối của hình bình "
                  r"hành) nên $MN \parallel CD$." +
                  "\\\\\n"
                  r"Vì $CD \subset \left(SCD\right)$ và "
                  r"$MN \not\subset \left(SCD\right)$," +
                  "\\\\\n"
                  r"nên $MN \parallel \left(SCD\right)$.")

        hoi_c = (r"Gọi $P$ là trung điểm của $SC$. Chứng minh "
                 r"$NP \parallel \left(ABCD\right)$.")
        giai_c = (r"Trong tam giác $SBC$, $N$ và $P$ là trung điểm của "
                  r"$SB$ và $SC$ nên $NP$ là đường trung bình." +
                  "\\\\\n"
                  r"Do đó $NP \parallel BC$." +
                  "\\\\\n"
                  r"Mà $BC \subset \left(ABCD\right)$ và "
                  r"$NP \not\subset \left(ABCD\right)$." +
                  "\\\\\n"
                  r"Vậy $NP \parallel \left(ABCD\right)$.")

        ds_abcd = [(hoi_a, r"MN \parallel \left(ABCD\right)", giai_a),
                   (hoi_b, r"MN \parallel \left(SCD\right)", giai_b),
                   (hoi_c, r"NP \parallel \left(ABCD\right)", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C4_B12_TH060_MC_A_01(socau, dang=1):
    r"""Tính chất cơ bản về đường thẳng song song với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho $d \parallel \left(P\right)$. Mặt phẳng $\left(Q\right)$ "
         r"chứa $d$ và cắt $\left(P\right)$ theo giao tuyến $a$. Khi đó",
         r"$a \parallel d$",
         [r"$a$ cắt $d$", r"$a$ và $d$ chéo nhau", r"$a \equiv d$"],
         r"$a$ và $d$ cùng nằm trong $\left(Q\right)$ nên đồng phẳng." +
         "\\\\\n" +
         r"Nếu chúng cắt nhau thì điểm cắt thuộc $a \subset "
         r"\left(P\right)$, trái với $d \parallel \left(P\right)$." +
         "\\\\\n" +
         r"Vậy $a \parallel d$. Đây là tính chất dùng nhiều nhất khi tìm "
         r"giao tuyến và dựng thiết diện."),
        (r"Nếu hai mặt phẳng phân biệt cùng song song với một đường thẳng "
         r"$d$ và cắt nhau theo giao tuyến $a$ thì",
         r"$a \parallel d$",
         [r"$a$ cắt $d$", r"$a$ và $d$ chéo nhau",
          r"$a$ vuông góc với $d$"],
         r"Giao tuyến của hai mặt phẳng cùng song song với $d$ thì song "
         r"song với $d$." + "\\\\\n" +
         r"Tính chất này giúp xác định phương của giao tuyến mà không "
         r"cần dựng thêm điểm."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C4_B12_VD061_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về đường thẳng song song với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Gọi $M$ là "
         r"trung điểm $SA$. Mặt phẳng $\left(MBC\right)$ cắt $SD$ tại "
         r"$N$. Khi đó $MN$ và $BC$",
         r"song song với nhau",
         [r"cắt nhau", r"chéo nhau", r"vuông góc với nhau"],
         r"$BC \parallel AD$ nên $BC \parallel \left(SAD\right)$." +
         "\\\\\n" +
         r"Mặt phẳng $\left(MBC\right)$ chứa $BC$ và cắt "
         r"$\left(SAD\right)$ theo giao tuyến $MN$." + "\\\\\n" +
         r"Theo tính chất, $MN \parallel BC$.", "chop4"),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành tâm $O$. Gọi "
         r"$M$ là trung điểm $SA$. Khẳng định nào sau đây ĐÚNG?",
         r"$OM \parallel \left(SCD\right)$",
         [r"$OM \parallel \left(SAB\right)$",
          r"$OM \subset \left(SCD\right)$",
          r"$OM$ cắt $\left(SCD\right)$"],
         r"$O$ là trung điểm $AC$, $M$ là trung điểm $SA$ nên $OM$ là "
         r"đường trung bình tam giác $SAC$." + "\\\\\n" +
         r"Do đó $OM \parallel SC$." + "\\\\\n" +
         r"Mà $SC \subset \left(SCD\right)$ và "
         r"$OM \not\subset \left(SCD\right)$, nên "
         r"$OM \parallel \left(SCD\right)$.", "chop4"),
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Khẳng định nào sau đây ĐÚNG?",
         r"$AB \parallel \left(A'B'C'D'\right)$",
         [r"$AB \subset \left(A'B'C'D'\right)$",
          r"$AB$ cắt $\left(A'B'C'D'\right)$",
          r"$AA' \parallel \left(A'B'C'D'\right)$"],
         r"$AB \parallel A'B'$ (mặt bên $ABB'A'$ là hình bình hành)." +
         "\\\\\n" +
         r"Mà $A'B' \subset \left(A'B'C'D'\right)$ và "
         r"$AB \not\subset \left(A'B'C'D'\right)$." + "\\\\\n" +
         r"Vậy $AB \parallel \left(A'B'C'D'\right)$. Còn $AA'$ CẮT "
         r"$\left(A'B'C'D'\right)$ tại $A'$.", "hop"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, giai, loai = MAU[i]
        hinh = {"chop4": _hinh_chop_tu_giac(), "hop": _hinh_hop()}[loai]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), giai, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B12_VD061_SA_A_01(socau):
    r"""Tỉ số độ dài khi đường thẳng song song với mặt phẳng - SA.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
        if a not in gt:
            gt.append(a)

    cau = ""
    for a in gt:
        kq = Fraction(a, 2)
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"với $BC = %d$. Gọi $M$ là trung điểm $SA$. Mặt phẳng "
                 r"$\left(MBC\right)$ cắt $SD$ tại $N$. Tính độ dài $MN$."
                 % a)
        giai = (r"$BC \parallel AD$ nên "
                r"$BC \parallel \left(SAD\right)$." +
                "\\\\\n"
                r"Mặt phẳng $\left(MBC\right)$ chứa $BC$ và cắt "
                r"$\left(SAD\right)$ theo $MN$, nên $MN \parallel BC$, "
                r"do đó $MN \parallel AD$." +
                "\\\\\n"
                r"Trong tam giác $SAD$, $M$ là trung điểm $SA$ và "
                r"$MN \parallel AD$ nên $N$ là trung điểm $SD$ và $MN$ "
                r"là đường trung bình." +
                "\\\\\n"
                r"$MN = \dfrac{1}{2}AD = \dfrac{1}{2}BC = "
                r"\dfrac{1}{2}\cdot %d = %s$." % (a, _xx(kq)))
        nhieu = _ba_nhieu4(_xx(kq), [str(a), _xx(Fraction(a, 4)),
                                     str(2 * a)],
                           buoc=lambda t: _xx(float(kq) + t))
        cau += MC_SA_answer_const(debai, _xx(kq), nhieu, giai, hinh, 0, 2)
    return cau


def L11_C4_B12_VD061_TL_A_01(socau, dong=1):
    r"""Tự luận: vận dụng đường thẳng song song với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([6, 8, 10, 12, 16, 20])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"với $AD = %d$. Gọi $M$ là trung điểm của cạnh $SA$."
                 % a)

        hoi_a = r"Chứng minh $BC \parallel \left(SAD\right)$."
        giai_a = (r"$ABCD$ là hình bình hành nên $BC \parallel AD$." +
                  "\\\\\n"
                  r"Mà $AD \subset \left(SAD\right)$ và "
                  r"$BC \not\subset \left(SAD\right)$." +
                  "\\\\\n"
                  r"Vậy $BC \parallel \left(SAD\right)$.")

        hoi_b = (r"Xác định giao tuyến của $\left(MBC\right)$ và "
                 r"$\left(SAD\right)$.")
        giai_b = (r"$M$ là điểm chung của hai mặt phẳng." +
                  "\\\\\n"
                  r"$\left(MBC\right)$ chứa $BC$ mà "
                  r"$BC \parallel \left(SAD\right)$." +
                  "\\\\\n"
                  r"Vậy giao tuyến là đường thẳng qua $M$ song song với "
                  r"$BC$ (và $AD$); gọi $N$ là giao của đường thẳng đó "
                  r"với $SD$ thì giao tuyến là $MN$.")

        hoi_c = r"Tính độ dài $MN$."
        giai_c = (r"Trong tam giác $SAD$ có $MN \parallel AD$ và $M$ là "
                  r"trung điểm $SA$." +
                  "\\\\\n"
                  r"Suy ra $N$ là trung điểm $SD$, nên $MN$ là đường "
                  r"trung bình của tam giác $SAD$." +
                  "\\\\\n"
                  r"$MN = \dfrac{1}{2}AD = \dfrac{1}{2}\cdot %d = %s$."
                  % (a, _xx(Fraction(a, 2))))

        ds_abcd = [(hoi_a, r"BC \parallel \left(SAD\right)", giai_a),
                   (hoi_b, r"MN \parallel AD", giai_b),
                   (hoi_c, r"MN = %s" % _xx(Fraction(a, 2)), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 13. HAI MẶT PHẲNG SONG SONG
# =====================================================================

def L11_C4_B13_NB062_MC_A_01(socau, dang=1):
    r"""Nhận biết hai mặt phẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hai mặt phẳng gọi là song song với nhau khi nào?",
         r"Khi chúng không có điểm chung",
         [r"Khi chúng có đúng một điểm chung",
          r"Khi chúng có một đường thẳng chung",
          r"Khi mọi đường thẳng của mặt phẳng này đều song song với mặt "
          r"phẳng kia"],
         r"Hai mặt phẳng phân biệt hoặc CẮT NHAU (có một giao tuyến) "
         r"hoặc SONG SONG (không có điểm chung)."),
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Mặt phẳng nào sau đây song song "
         r"với $\left(ABCD\right)$?",
         r"$\left(A'B'C'D'\right)$",
         [r"$\left(ABB'A'\right)$", r"$\left(BCC'B'\right)$",
          r"$\left(ACC'A'\right)$"],
         r"Hai mặt đáy của hình hộp song song với nhau." + "\\\\\n" +
         r"Các mặt còn lại đều CẮT $\left(ABCD\right)$ theo một cạnh "
         r"đáy."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_hop() if "hình hộp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B13_TH063_MC_A_01(socau, dang=1):
    r"""Điều kiện để hai mặt phẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Điều kiện nào sau đây ĐỦ để kết luận "
         r"$\left(P\right) \parallel \left(Q\right)$?",
         r"Trong $\left(P\right)$ có hai đường thẳng CẮT NHAU cùng song "
         r"song với $\left(Q\right)$",
         [r"Trong $\left(P\right)$ có một đường thẳng song song với "
          r"$\left(Q\right)$",
          r"Trong $\left(P\right)$ có hai đường thẳng song song với nhau "
          r"và cùng song song với $\left(Q\right)$",
          r"$\left(P\right)$ và $\left(Q\right)$ cùng song song với một "
          r"đường thẳng"],
         r"Điều kiện ``CẮT NHAU'' là bắt buộc." + "\\\\\n" +
         r"Nếu hai đường thẳng đó song song với nhau thì "
         r"$\left(P\right)$ vẫn có thể cắt $\left(Q\right)$."),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành. Gọi $M$, $N$, "
         r"$P$ lần lượt là trung điểm của $SA$, $SB$, $SC$. Khẳng định "
         r"nào ĐÚNG?",
         r"$\left(MNP\right) \parallel \left(ABCD\right)$",
         [r"$\left(MNP\right)$ cắt $\left(ABCD\right)$",
          r"$\left(MNP\right) \equiv \left(ABCD\right)$",
          r"$\left(MNP\right) \parallel \left(SAB\right)$"],
         r"$MN$ là đường trung bình tam giác $SAB$ nên "
         r"$MN \parallel AB$, suy ra "
         r"$MN \parallel \left(ABCD\right)$." + "\\\\\n" +
         r"$NP$ là đường trung bình tam giác $SBC$ nên "
         r"$NP \parallel BC$, suy ra "
         r"$NP \parallel \left(ABCD\right)$." + "\\\\\n" +
         r"$MN$ và $NP$ CẮT NHAU tại $N$ và cùng nằm trong "
         r"$\left(MNP\right)$, nên "
         r"$\left(MNP\right) \parallel \left(ABCD\right)$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_tu_giac() if "hình chóp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B13_TH064_MC_A_01(socau, dang=1):
    r"""Tính chất cơ bản về hai mặt phẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho $\left(P\right) \parallel \left(Q\right)$. Mặt phẳng "
         r"$\left(R\right)$ cắt $\left(P\right)$ theo giao tuyến $a$ và "
         r"cắt $\left(Q\right)$ theo giao tuyến $b$. Khi đó",
         r"$a \parallel b$",
         [r"$a$ cắt $b$", r"$a$ và $b$ chéo nhau", r"$a \equiv b$"],
         r"$a$ và $b$ cùng nằm trong $\left(R\right)$ nên đồng phẳng." +
         "\\\\\n" +
         r"Nếu cắt nhau thì điểm cắt là điểm chung của "
         r"$\left(P\right)$ và $\left(Q\right)$, trái giả thiết." +
         "\\\\\n" +
         r"Vậy $a \parallel b$."),
        (r"Cho $\left(P\right) \parallel \left(Q\right)$ và đường thẳng "
         r"$d \subset \left(P\right)$. Khi đó",
         r"$d \parallel \left(Q\right)$",
         [r"$d \subset \left(Q\right)$", r"$d$ cắt $\left(Q\right)$",
          r"$d$ có thể cắt $\left(Q\right)$"],
         r"$d \subset \left(P\right)$ mà $\left(P\right)$ và "
         r"$\left(Q\right)$ không có điểm chung, nên $d$ cũng không có "
         r"điểm chung với $\left(Q\right)$." + "\\\\\n" +
         r"Vậy $d \parallel \left(Q\right)$."),
        (r"Qua một điểm nằm ngoài mặt phẳng $\left(Q\right)$ có bao "
         r"nhiêu mặt phẳng song song với $\left(Q\right)$?",
         r"$1$", [r"$0$", r"$2$", r"vô số"],
         r"Đây là tính chất: qua một điểm ngoài một mặt phẳng có DUY "
         r"NHẤT một mặt phẳng song song với mặt phẳng đó."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C4_B13_TH064_TL_A_01(socau, dong=1):
    r"""Tự luận: chứng minh hai mặt phẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình "
                 r"hành. Gọi $M$, $N$, $P$ lần lượt là trung điểm của "
                 r"$SA$, $SB$, $SC$.")

        hoi_a = (r"Chứng minh $MN \parallel \left(ABCD\right)$ và "
                 r"$NP \parallel \left(ABCD\right)$.")
        giai_a = (r"$MN$ là đường trung bình tam giác $SAB$ nên "
                  r"$MN \parallel AB$." +
                  "\\\\\n"
                  r"Vì $AB \subset \left(ABCD\right)$ và "
                  r"$MN \not\subset \left(ABCD\right)$ nên "
                  r"$MN \parallel \left(ABCD\right)$." +
                  "\\\\\n"
                  r"Tương tự $NP$ là đường trung bình tam giác $SBC$ nên "
                  r"$NP \parallel BC$ và "
                  r"$NP \parallel \left(ABCD\right)$.")

        hoi_b = (r"Chứng minh "
                 r"$\left(MNP\right) \parallel \left(ABCD\right)$.")
        giai_b = (r"$MN$ và $NP$ là hai đường thẳng CẮT NHAU tại $N$ và "
                  r"cùng nằm trong $\left(MNP\right)$." +
                  "\\\\\n"
                  r"Theo câu a, cả hai cùng song song với "
                  r"$\left(ABCD\right)$." +
                  "\\\\\n"
                  r"Vậy $\left(MNP\right) \parallel \left(ABCD\right)$.")

        hoi_c = (r"Gọi $Q$ là trung điểm $SD$. Chứng minh $Q$ thuộc "
                 r"$\left(MNP\right)$ và tứ giác $MNPQ$ là hình bình "
                 r"hành.")
        giai_c = (r"$MQ$ là đường trung bình tam giác $SAD$ nên "
                  r"$MQ \parallel AD$; $NP \parallel BC \parallel AD$." +
                  "\\\\\n"
                  r"Suy ra $MQ \parallel NP$, nên bốn điểm $M$, $N$, "
                  r"$P$, $Q$ đồng phẳng, tức $Q$ thuộc "
                  r"$\left(MNP\right)$." +
                  "\\\\\n"
                  r"Lại có $MQ = \dfrac{1}{2}AD = \dfrac{1}{2}BC = NP$." +
                  "\\\\\n"
                  r"Tứ giác $MNPQ$ có $MQ \parallel NP$ và $MQ = NP$ nên "
                  r"là hình bình hành.")

        ds_abcd = [(hoi_a, r"MN,\ NP \parallel \left(ABCD\right)", giai_a),
                   (hoi_b, r"\left(MNP\right) \parallel \left(ABCD\right)",
                    giai_b),
                   (hoi_c, r"MNPQ \text{ là hình bình hành}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C4_B13_TH065_MC_A_01(socau, dang=1):
    r"""Định lí Thalès trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q = random.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5),
                              (1, 2), (1, 3), (2, 7)])
        if (p, q) not in gt:
            gt.append((p, q))

    cauTN = ""
    for p, q in gt:
        dung = "$%s$" % _ps4(p, q)
        nhieu = _ba_nhieu4(dung,
                           ["$%s$" % _ps4(q, p), "$%s$" % _ps4(p, p + q),
                            "$%s$" % _ps4(p + q, q)],
                           buoc=lambda t: "$%s$" % _ps4(p + t, q))
        debai = (r"Cho ba mặt phẳng đôi một song song "
                 r"$\left(P\right)$, $\left(Q\right)$, $\left(R\right)$. "
                 r"Hai cát tuyến $d$ và $d'$ lần lượt cắt ba mặt phẳng "
                 r"tại $A$, $B$, $C$ và $A'$, $B'$, $C'$. Biết "
                 r"$\dfrac{AB}{BC} = %s$. Tính $\dfrac{A'B'}{B'C'}$."
                 % _ps4(p, q))
        giai = (r"Định lí Thalès trong không gian: ba mặt phẳng đôi một "
                r"song song chắn trên hai cát tuyến những đoạn thẳng "
                r"TƯƠNG ỨNG TỈ LỆ." +
                "\\\\\n"
                r"Nghĩa là $\dfrac{AB}{A'B'} = \dfrac{BC}{B'C'} = "
                r"\dfrac{AC}{A'C'}$." +
                "\\\\\n"
                r"Từ $\dfrac{AB}{A'B'} = \dfrac{BC}{B'C'}$ suy ra "
                r"$\dfrac{AB}{BC} = \dfrac{A'B'}{B'C'}$." +
                "\\\\\n"
                r"Vậy $\dfrac{A'B'}{B'C'} = %s$." % _ps4(p, q))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C4_B13_TH065_SA_A_01(socau):
    r"""Tính độ dài theo định lí Thalès - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        AB = random.choice([2, 3, 4, 5, 6])
        BC = random.choice([2, 4, 6, 8, 10])
        ApBp = random.choice([4, 6, 8, 10, 12])
        kq = Fraction(ApBp * BC, AB)
        if (kq * 100).denominator != 1:
            continue
        v = (AB, BC, ApBp)
        if v not in gt:
            gt.append(v)

    cau = ""
    for AB, BC, ApBp in gt:
        kq = Fraction(ApBp * BC, AB)
        debai = (r"Cho ba mặt phẳng đôi một song song. Hai cát tuyến $d$ "
                 r"và $d'$ lần lượt cắt ba mặt phẳng tại $A$, $B$, $C$ "
                 r"và $A'$, $B'$, $C'$. Biết $AB = %d$, $BC = %d$ và "
                 r"$A'B' = %d$. Tính $B'C'$." % (AB, BC, ApBp))
        giai = (r"Theo định lí Thalès trong không gian: "
                r"$\dfrac{AB}{A'B'} = \dfrac{BC}{B'C'}$." +
                "\\\\\n"
                r"Suy ra $B'C' = \dfrac{A'B'\cdot BC}{AB} = "
                r"\dfrac{%d\cdot %d}{%d} = %s$."
                % (ApBp, BC, AB, _xx(kq)))
        nhieu = _ba_nhieu4(_xx(kq), [str(BC), str(ApBp),
                                     _xx(Fraction(AB * BC, ApBp))],
                           buoc=lambda t: _xx(float(kq) + t))
        cau += MC_SA_answer_const(debai, _xx(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C4_B13_TH066_MC_A_01(socau, dang=1):
    r"""Tính chất cơ bản của hình lăng trụ và hình hộp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Các mặt của hình hộp là",
         r"sáu hình bình hành",
         [r"sáu hình chữ nhật", r"sáu hình vuông",
          r"bốn hình bình hành và hai hình thang"],
         r"Theo định nghĩa, hình hộp là hình lăng trụ có đáy là hình "
         r"bình hành, nên cả sáu mặt đều là hình bình hành." +
         "\\\\\n" +
         r"Hình chữ nhật và hình vuông chỉ là TRƯỜNG HỢP RIÊNG."),
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Bốn đường chéo $AC'$, $BD'$, "
         r"$CA'$, $DB'$ có tính chất gì?",
         r"Đồng quy tại trung điểm của mỗi đường",
         [r"Đôi một song song", r"Đôi một chéo nhau",
          r"Đồng quy nhưng không đi qua trung điểm"],
         r"Bốn đường chéo của hình hộp cắt nhau tại một điểm và điểm đó "
         r"là trung điểm của mỗi đường; điểm này gọi là TÂM của hình "
         r"hộp."),
        (r"Cho hình lăng trụ. Các mặt bên của hình lăng trụ là",
         r"các hình bình hành",
         [r"các hình chữ nhật", r"các tam giác", r"các hình thang"],
         r"Hai đáy của lăng trụ bằng nhau và nằm trong hai mặt phẳng "
         r"song song, các cạnh bên song song và bằng nhau, nên mỗi mặt "
         r"bên là một hình bình hành."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_hop() if "hình hộp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B13_VD067_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về quan hệ song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Khẳng định nào sau đây ĐÚNG?",
         r"$\left(ABB'A'\right) \parallel \left(DCC'D'\right)$",
         [r"$\left(ABB'A'\right) \parallel \left(BCC'B'\right)$",
          r"$\left(ABB'A'\right) \parallel \left(ABCD\right)$",
          r"$\left(ABB'A'\right) \parallel \left(ACC'A'\right)$"],
         r"$AB \parallel DC$ và $AA' \parallel DD'$, hai cặp đường thẳng "
         r"cắt nhau này lần lượt nằm trong hai mặt phẳng." + "\\\\\n" +
         r"Vậy $\left(ABB'A'\right) \parallel \left(DCC'D'\right)$ (hai "
         r"mặt bên đối diện của hình hộp).", "hop"),
        (r"Cho hình chóp $S.ABCD$ có đáy là hình bình hành tâm $O$. Gọi "
         r"$M$, $N$ lần lượt là trung điểm của $SA$, $SC$. Khẳng định "
         r"nào ĐÚNG?",
         r"$MN \parallel \left(ABCD\right)$",
         [r"$MN \parallel SB$", r"$MN$ cắt $\left(ABCD\right)$",
          r"$MN \subset \left(ABCD\right)$"],
         r"$MN$ là đường trung bình tam giác $SAC$ nên "
         r"$MN \parallel AC$." + "\\\\\n" +
         r"Mà $AC \subset \left(ABCD\right)$ và "
         r"$MN \not\subset \left(ABCD\right)$." + "\\\\\n" +
         r"Vậy $MN \parallel \left(ABCD\right)$.", "chop4"),
        (r"Cho hình hộp $ABCD.A'B'C'D'$. Thiết diện của hình hộp cắt bởi "
         r"mặt phẳng đi qua $A$ và song song với "
         r"$\left(A'B'C'D'\right)$ là",
         r"tứ giác $ABCD$",
         [r"tam giác $ABD$", r"tứ giác $ABB'A'$",
          r"tứ giác $ACC'A'$"],
         r"Qua điểm $A$ có DUY NHẤT một mặt phẳng song song với "
         r"$\left(A'B'C'D'\right)$." + "\\\\\n" +
         r"Mặt phẳng $\left(ABCD\right)$ đi qua $A$ và song song với "
         r"$\left(A'B'C'D'\right)$ (hai đáy của hình hộp)." + "\\\\\n" +
         r"Vậy thiết diện chính là đáy $ABCD$.", "hop"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, giai, loai = MAU[i]
        hinh = {"hop": _hinh_hop(), "chop4": _hinh_chop_tu_giac()}[loai]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), giai, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B13_VD067_SA_A_01(socau):
    r"""Độ dài trong thiết diện song song với đáy - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([6, 8, 9, 10, 12, 15, 16, 18, 20])
        p, q = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
        kq = Fraction(a * p, q)
        if (kq * 100).denominator != 1:
            continue
        v = (a, p, q)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, p, q in gt:
        kq = Fraction(a * p, q)
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"với $AB = %d$. Trên cạnh $SA$ lấy điểm $M$ sao cho "
                 r"$\dfrac{SM}{SA} = %s$. Mặt phẳng qua $M$ và song song "
                 r"với $\left(ABCD\right)$ cắt $SB$ tại $N$. Tính độ dài "
                 r"$MN$." % (a, _ps4(p, q)))
        giai = (r"Mặt phẳng qua $M$ song song với $\left(ABCD\right)$ cắt "
                r"$\left(SAB\right)$ theo giao tuyến $MN$." +
                "\\\\\n"
                r"Hai mặt phẳng song song bị cắt bởi $\left(SAB\right)$ "
                r"cho hai giao tuyến song song, nên $MN \parallel AB$." +
                "\\\\\n"
                r"Trong tam giác $SAB$ có $MN \parallel AB$ nên "
                r"$\dfrac{MN}{AB} = \dfrac{SM}{SA} = %s$." % _ps4(p, q) +
                "\\\\\n"
                r"$MN = %s\cdot %d = %s$." % (_ps4(p, q), a, _xx(kq)))
        nhieu = _ba_nhieu4(_xx(kq), [str(a), _xx(Fraction(a * q, p)),
                                     _xx(Fraction(a, 2))],
                           buoc=lambda t: _xx(float(kq) + t))
        cau += MC_SA_answer_const(debai, _xx(kq), nhieu, giai, hinh, 0, 2)
    return cau


def L11_C4_B13_VD067_TL_A_01(socau, dong=1):
    r"""Tự luận: vận dụng quan hệ song song, thiết diện song song đáy.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([8, 10, 12, 16, 20])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"với $AB = %d$. Gọi $M$ là trung điểm của $SA$ và "
                 r"$\left(\alpha\right)$ là mặt phẳng đi qua $M$, song "
                 r"song với mặt phẳng $\left(ABCD\right)$." % a)

        hoi_a = (r"Xác định thiết diện của hình chóp cắt bởi "
                 r"$\left(\alpha\right)$.")
        giai_a = (r"$\left(\alpha\right)$ song song với "
                  r"$\left(ABCD\right)$ nên cắt các mặt bên theo các "
                  r"giao tuyến song song với các cạnh đáy tương ứng." +
                  "\\\\\n"
                  r"Gọi $N$, $P$, $Q$ lần lượt là giao điểm của "
                  r"$\left(\alpha\right)$ với $SB$, $SC$, $SD$." +
                  "\\\\\n"
                  r"Thiết diện là tứ giác $MNPQ$.")

        hoi_b = r"Chứng minh $MNPQ$ là hình bình hành."
        giai_b = (r"$\left(\alpha\right) \parallel \left(ABCD\right)$ và "
                  r"$\left(SAB\right)$ cắt cả hai nên "
                  r"$MN \parallel AB$." +
                  "\\\\\n"
                  r"Tương tự $QP \parallel DC$, mà $AB \parallel DC$ nên "
                  r"$MN \parallel QP$." +
                  "\\\\\n"
                  r"Vì $M$ là trung điểm $SA$ nên các điểm $N$, $P$, $Q$ "
                  r"cũng là trung điểm của $SB$, $SC$, $SD$; do đó "
                  r"$MN = QP = \dfrac{1}{2}AB$." +
                  "\\\\\n"
                  r"Vậy $MNPQ$ là hình bình hành.")

        hoi_c = r"Tính độ dài $MN$."
        giai_c = (r"$MN$ là đường trung bình của tam giác $SAB$." +
                  "\\\\\n"
                  r"$MN = \dfrac{1}{2}AB = \dfrac{1}{2}\cdot %d = %s$."
                  % (a, _xx(Fraction(a, 2))))

        ds_abcd = [(hoi_a, r"\text{Tứ giác } MNPQ", giai_a),
                   (hoi_b, r"MNPQ \text{ là hình bình hành}", giai_b),
                   (hoi_c, r"MN = %s" % _xx(Fraction(a, 2)), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 14. PHÉP CHIẾU SONG SONG
# =====================================================================

def L11_C4_B14_NB068_MC_A_01(socau, dang=1):
    r"""Nhận biết phép chiếu song song và tính chất cơ bản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Phép chiếu song song BẢO TOÀN tính chất nào sau đây?",
         r"Tính thẳng hàng của ba điểm",
         [r"Độ dài của đoạn thẳng", r"Số đo của góc",
          r"Độ lớn của diện tích"],
         r"Phép chiếu song song bảo toàn: tính thẳng hàng, thứ tự các "
         r"điểm, tính song song và TỈ SỐ độ dài của hai đoạn thẳng cùng "
         r"phương." + "\\\\\n" +
         r"Nó KHÔNG bảo toàn độ dài, số đo góc và diện tích."),
        (r"Qua phép chiếu song song, ảnh của hai đường thẳng song song "
         r"(không song song với phương chiếu) là",
         r"hai đường thẳng song song hoặc trùng nhau",
         [r"hai đường thẳng cắt nhau", r"hai đường thẳng chéo nhau",
          r"hai điểm phân biệt"],
         r"Phép chiếu song song bảo toàn tính song song; hai đường thẳng "
         r"song song có ảnh song song, hoặc TRÙNG nhau khi mặt phẳng "
         r"chứa chúng song song với phương chiếu."),
        (r"Qua phép chiếu song song, ảnh của một đoạn thẳng (không song "
         r"song với phương chiếu) là",
         r"một đoạn thẳng",
         [r"một điểm", r"một đường thẳng", r"một tia"],
         r"Ảnh của đoạn thẳng $AB$ là đoạn thẳng $A'B'$ nối ảnh của hai "
         r"đầu mút." + "\\\\\n" +
         r"Ảnh chỉ suy biến thành một ĐIỂM khi đoạn thẳng song song với "
         r"phương chiếu."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C4_B14_TH069_MC_A_01(socau, dang=1):
    r"""Ảnh của điểm, đoạn thẳng, tam giác qua phép chiếu song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Qua phép chiếu song song, ảnh của trung điểm một đoạn thẳng "
         r"là",
         r"trung điểm của đoạn thẳng ảnh",
         [r"một điểm bất kì của đoạn thẳng ảnh",
          r"một đầu mút của đoạn thẳng ảnh",
          r"điểm nằm ngoài đoạn thẳng ảnh"],
         r"Phép chiếu song song bảo toàn TỈ SỐ độ dài của hai đoạn thẳng "
         r"cùng nằm trên một đường thẳng." + "\\\\\n" +
         r"Trung điểm ứng với tỉ số $\dfrac{1}{2}$, nên ảnh vẫn là trung "
         r"điểm."),
        (r"Qua phép chiếu song song, ảnh của một tam giác (nằm trong mặt "
         r"phẳng không song song với phương chiếu) là",
         r"một tam giác",
         [r"một đoạn thẳng", r"một điểm", r"một tứ giác"],
         r"Ba đỉnh không thẳng hàng có ảnh là ba điểm không thẳng hàng "
         r"(vì mặt phẳng chứa tam giác không song song với phương "
         r"chiếu)." + "\\\\\n" +
         r"Vậy ảnh là một tam giác, tuy nhiên hình dạng có thể thay đổi "
         r"vì độ dài và góc không được bảo toàn."),
        (r"Qua phép chiếu song song, ảnh của một hình bình hành (nằm "
         r"trong mặt phẳng không song song với phương chiếu) là",
         r"một hình bình hành",
         [r"một hình chữ nhật", r"một hình thang",
          r"một tứ giác bất kì"],
         r"Hai cặp cạnh đối song song và bằng nhau có ảnh là hai cặp "
         r"đoạn thẳng song song và bằng nhau (tỉ số $1$ được bảo toàn)." +
         "\\\\\n" +
         r"Vậy ảnh vẫn là hình bình hành; nhưng góc vuông thì KHÔNG được "
         r"bảo toàn nên chưa chắc là hình chữ nhật."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C4_B14_TH070_MC_A_01(socau, dang=1):
    r"""Hình biểu diễn của một số hình khối đơn giản.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hình biểu diễn của một hình vuông trong không gian thường là",
         r"một hình bình hành",
         [r"một hình vuông", r"một hình thang", r"một tứ giác bất kì"],
         r"Hình biểu diễn được dựng bằng phép chiếu song song, mà phép "
         r"này bảo toàn tính song song và tỉ số độ dài nhưng không bảo "
         r"toàn góc." + "\\\\\n" +
         r"Vì vậy hình vuông (một hình bình hành đặc biệt) có hình biểu "
         r"diễn là hình bình hành."),
        (r"Hình biểu diễn của một tam giác đều thường là",
         r"một tam giác bất kì",
         [r"một tam giác đều", r"một tam giác vuông",
          r"một tam giác cân"],
         r"Phép chiếu song song không bảo toàn độ dài và góc, nên tam "
         r"giác đều có thể có hình biểu diễn là tam giác bất kì."),
        (r"Trong hình biểu diễn của hình hộp, các cạnh bị KHUẤT thường "
         r"được vẽ bằng",
         r"nét đứt",
         [r"nét liền đậm", r"nét liền mảnh", r"nét chấm chấm màu đỏ"],
         r"Quy ước vẽ hình không gian: cạnh nhìn thấy vẽ nét LIỀN, cạnh "
         r"bị khuất vẽ nét ĐỨT, giúp hình dễ hình dung hơn."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_hop() if "hình hộp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C4_B14_VD071_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về phép chiếu song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p, q = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4),
                              (2, 5)])
        if (p, q) not in gt:
            gt.append((p, q))

    cauTN = ""
    for p, q in gt:
        dung = "$%s$" % _ps4(p, q)
        nhieu = _ba_nhieu4(dung,
                           ["$%s$" % _ps4(q, p), "$1$",
                            "$%s$" % _ps4(p, p + q)],
                           buoc=lambda t: "$%s$" % _ps4(p + t, q))
        debai = (r"Cho ba điểm $A$, $B$, $C$ thẳng hàng với "
                 r"$\dfrac{AB}{AC} = %s$. Gọi $A'$, $B'$, $C'$ lần lượt "
                 r"là ảnh của $A$, $B$, $C$ qua một phép chiếu song song "
                 r"(phương chiếu không song song với đường thẳng "
                 r"$AC$). Tính $\dfrac{A'B'}{A'C'}$." % _ps4(p, q))
        giai = (r"Phép chiếu song song bảo toàn tính thẳng hàng, nên "
                r"$A'$, $B'$, $C'$ cũng thẳng hàng." +
                "\\\\\n"
                r"Phép chiếu song song còn bảo toàn TỈ SỐ độ dài của hai "
                r"đoạn thẳng cùng nằm trên một đường thẳng." +
                "\\\\\n"
                r"Do đó $\dfrac{A'B'}{A'C'} = \dfrac{AB}{AC} = %s$."
                % _ps4(p, q) +
                "\\\\\n"
                r"Chú ý bản thân độ dài $A'B'$ và $AB$ có thể khác nhau, "
                r"chỉ TỈ SỐ là không đổi.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C4_B14_VD071_SA_A_01(socau):
    r"""Độ dài ảnh qua phép chiếu song song - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        AC = random.choice([6, 8, 10, 12, 15, 16, 20])
        p, q = random.choice([(1, 2), (1, 4), (3, 4), (2, 5), (1, 5)])
        ApCp = random.choice([4, 6, 8, 10, 12, 20])
        kq = Fraction(ApCp * p, q)
        if (kq * 100).denominator != 1:
            continue
        v = (AC, p, q, ApCp)
        if v not in gt:
            gt.append(v)

    cau = ""
    for AC, p, q, ApCp in gt:
        kq = Fraction(ApCp * p, q)
        debai = (r"Cho ba điểm $A$, $B$, $C$ thẳng hàng với "
                 r"$\dfrac{AB}{AC} = %s$. Qua một phép chiếu song song, "
                 r"ba điểm đó có ảnh lần lượt là $A'$, $B'$, $C'$ và "
                 r"$A'C' = %d$. Tính $A'B'$." % (_ps4(p, q), ApCp))
        giai = (r"Phép chiếu song song bảo toàn tỉ số độ dài của hai đoạn "
                r"thẳng cùng nằm trên một đường thẳng." +
                "\\\\\n"
                r"$\dfrac{A'B'}{A'C'} = \dfrac{AB}{AC} = %s$."
                % _ps4(p, q) +
                "\\\\\n"
                r"$A'B' = %s\cdot %d = %s$."
                % (_ps4(p, q), ApCp, _xx(kq)))
        nhieu = _ba_nhieu4(_xx(kq), [str(ApCp), str(AC),
                                     _xx(Fraction(ApCp * q, p))],
                           buoc=lambda t: _xx(float(kq) + t))
        cau += MC_SA_answer_const(debai, _xx(kq), nhieu, giai, 0, 0, 2)
    return cau


def L11_C4_B14_VD071_TL_A_01(socau, dong=1):
    r"""Tự luận: vận dụng phép chiếu song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        debai = (r"Cho hai mặt phẳng phân biệt $\left(P\right)$ và "
                 r"$\left(Q\right)$, cùng một phương chiếu $\ell$ không "
                 r"song song với $\left(Q\right)$. Xét phép chiếu song "
                 r"song lên $\left(Q\right)$ theo phương $\ell$.")

        hoi_a = (r"Nêu ảnh của một đường thẳng $d \subset \left(P\right)$ "
                 r"không song song với $\ell$.")
        giai_a = (r"Mặt phẳng chứa $d$ và song song với $\ell$ cắt "
                  r"$\left(Q\right)$ theo một đường thẳng." +
                  "\\\\\n"
                  r"Vậy ảnh của $d$ là một ĐƯỜNG THẲNG nằm trong "
                  r"$\left(Q\right)$." +
                  "\\\\\n"
                  r"Nếu $d$ song song với $\ell$ thì ảnh của $d$ suy "
                  r"biến thành một ĐIỂM.")

        hoi_b = (r"Cho tam giác $ABC$ nằm trong $\left(P\right)$ và $M$ "
                 r"là trung điểm $BC$. Chứng minh ảnh $M'$ của $M$ là "
                 r"trung điểm của $B'C'$.")
        giai_b = (r"Phép chiếu song song bảo toàn tính thẳng hàng nên "
                  r"$B'$, $M'$, $C'$ thẳng hàng." +
                  "\\\\\n"
                  r"Phép chiếu song song bảo toàn tỉ số độ dài của hai "
                  r"đoạn thẳng cùng phương, nên "
                  r"$\dfrac{B'M'}{B'C'} = \dfrac{BM}{BC} = "
                  r"\dfrac{1}{2}$." +
                  "\\\\\n"
                  r"Vậy $M'$ là trung điểm của $B'C'$.")

        hoi_c = (r"Suy ra ảnh của trọng tâm $G$ của tam giác $ABC$ là "
                 r"trọng tâm $G'$ của tam giác $A'B'C'$.")
        giai_c = (r"$G$ thuộc trung tuyến $AM$ với "
                  r"$\dfrac{AG}{AM} = \dfrac{2}{3}$." +
                  "\\\\\n"
                  r"Qua phép chiếu, $A'$, $G'$, $M'$ thẳng hàng và "
                  r"$\dfrac{A'G'}{A'M'} = \dfrac{AG}{AM} = "
                  r"\dfrac{2}{3}$." +
                  "\\\\\n"
                  r"Theo câu b, $M'$ là trung điểm $B'C'$ nên $A'M'$ là "
                  r"trung tuyến của tam giác $A'B'C'$." +
                  "\\\\\n"
                  r"Vậy $G'$ là trọng tâm tam giác $A'B'C'$.")

        ds_abcd = [(hoi_a, r"\text{Ảnh là một đường thẳng}", giai_a),
                   (hoi_b, r"M' \text{ là trung điểm } B'C'", giai_b),
                   (hoi_c, r"G' \text{ là trọng tâm } A'B'C'", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 4
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C4_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - đường thẳng và mặt phẳng, hai đường thẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([6, 8, 10, 12, 16, 20])
        if a not in gt:
            gt.append(a)

    cauTF = ""
    for a in gt:
        hinh = _hinh_tu_dien()
        debai = (r"Cho hình tứ diện $ABCD$ có $AC = %d$. Gọi $M$, $N$, "
                 r"$P$, $Q$ lần lượt là trung điểm của các cạnh $AB$, "
                 r"$BC$, $CD$, $DA$." % a)

        ds_abcd = (
            # a) NB - đếm trực tiếp
            [
                (r"{\True Hình tứ diện $ABCD$ có $6$ cạnh}",
                 r"Đúng. Sáu cạnh là $AB$, $AC$, $AD$, $BC$, $BD$, "
                 r"$CD$."),
                (r"{Hình tứ diện $ABCD$ có $4$ cạnh}",
                 r"Sai. Tứ diện có $4$ MẶT nhưng có $6$ CẠNH."),
            ],
            # b) TH - đường trung bình
            [
                (r"{\True $MN \parallel AC$ và $MN = %s$}"
                 % _xx(Fraction(a, 2)),
                 r"Đúng. $MN$ là đường trung bình của tam giác $ABC$ nên "
                 r"$MN \parallel AC$ và $MN = \dfrac{1}{2}AC = %s$."
                 % _xx(Fraction(a, 2))),
                (r"{$MN \parallel AC$ và $MN = %d$}" % a,
                 r"Sai. Đường trung bình bằng NỬA cạnh đáy, nên "
                 r"$MN = %s$ chứ không phải $%d$."
                 % (_xx(Fraction(a, 2)), a)),
            ],
            # c) VD - phải ghép hai đường trung bình
            [
                (r"{\True Tứ giác $MNPQ$ là hình bình hành}",
                 r"Đúng. $MN \parallel AC$ (đường trung bình tam giác "
                 r"$ABC$) và $QP \parallel AC$ (đường trung bình tam "
                 r"giác $ACD$)." + "\\\\\n" +
                 r"Suy ra $MN \parallel QP$ và $MN = QP = "
                 r"\dfrac{1}{2}AC$, nên $MNPQ$ là hình bình hành."),
                (r"{Bốn điểm $M$, $N$, $P$, $Q$ không đồng phẳng}",
                 r"Sai. Vì $MN \parallel QP$ nên bốn điểm đó ĐỒNG PHẲNG "
                 r"(hai đường thẳng song song xác định một mặt phẳng)."),
            ],
            # d) VDC - phải nhận ra AB và CD chéo nhau
            [
                (r"{\True Hai đường thẳng $AB$ và $CD$ chéo nhau}",
                 r"Đúng. Nếu $AB$ và $CD$ đồng phẳng thì bốn điểm $A$, "
                 r"$B$, $C$, $D$ cùng thuộc một mặt phẳng." + "\\\\\n" +
                 r"Điều đó trái với giả thiết $ABCD$ là tứ diện (bốn "
                 r"đỉnh không đồng phẳng)." + "\\\\\n" +
                 r"Vậy $AB$ và $CD$ không đồng phẳng, tức chéo nhau."),
                (r"{Hai đường thẳng $AB$ và $CD$ song song với nhau}",
                 r"Sai. Hai đường thẳng song song phải ĐỒNG PHẲNG; ở đây "
                 r"$AB$ và $CD$ không đồng phẳng nên chúng chéo nhau."),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF


def L11_C4_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - hai mặt phẳng song song và phép chiếu song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([6, 8, 10, 12, 16, 20])
        if a not in gt:
            gt.append(a)

    cauTF = ""
    for a in gt:
        hinh = _hinh_chop_tu_giac()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình bình hành "
                 r"với $AB = %d$. Gọi $M$, $N$, $P$, $Q$ lần lượt là "
                 r"trung điểm của $SA$, $SB$, $SC$, $SD$." % a)

        ds_abcd = (
            # a) NB - đọc thẳng định nghĩa
            [
                (r"{\True Hai mặt phẳng song song thì không có điểm "
                 r"chung}",
                 r"Đúng. Đó chính là định nghĩa hai mặt phẳng song "
                 r"song."),
                (r"{Hai mặt phẳng song song thì có đúng một điểm chung}",
                 r"Sai. Có đúng một điểm chung là điều KHÔNG XẢY RA với "
                 r"hai mặt phẳng: chúng hoặc không có điểm chung, hoặc "
                 r"cắt nhau theo cả một đường thẳng."),
            ],
            # b) TH - một lần dùng đường trung bình
            [
                (r"{\True $MN \parallel \left(ABCD\right)$}",
                 r"Đúng. $MN$ là đường trung bình tam giác $SAB$ nên "
                 r"$MN \parallel AB$." + "\\\\\n" +
                 r"Mà $AB \subset \left(ABCD\right)$ và "
                 r"$MN \not\subset \left(ABCD\right)$, nên "
                 r"$MN \parallel \left(ABCD\right)$."),
                (r"{$MN \subset \left(ABCD\right)$}",
                 r"Sai. $M$, $N$ nằm trên hai cạnh bên nên không thuộc "
                 r"mặt đáy; $MN$ chỉ SONG SONG với "
                 r"$\left(ABCD\right)$."),
            ],
            # c) VD - phải dùng hai đường cắt nhau
            [
                (r"{\True $\left(MNP\right) \parallel "
                 r"\left(ABCD\right)$}",
                 r"Đúng. $MN \parallel AB$ và $NP \parallel BC$ nên cả "
                 r"hai cùng song song với $\left(ABCD\right)$." +
                 "\\\\\n" +
                 r"$MN$ và $NP$ CẮT NHAU tại $N$ và cùng nằm trong "
                 r"$\left(MNP\right)$." + "\\\\\n" +
                 r"Vậy $\left(MNP\right) \parallel \left(ABCD\right)$."),
                (r"{Chỉ cần $MN \parallel \left(ABCD\right)$ là đủ để "
                 r"kết luận $\left(MNP\right) \parallel "
                 r"\left(ABCD\right)$}",
                 r"Sai. Phải có HAI đường thẳng CẮT NHAU trong "
                 r"$\left(MNP\right)$ cùng song song với "
                 r"$\left(ABCD\right)$; một đường là chưa đủ."),
            ],
            # d) VDC - tỉ số và tính chất thiết diện
            [
                (r"{\True Tứ giác $MNPQ$ là hình bình hành và "
                 r"$MN = %s$}" % _xx(Fraction(a, 2)),
                 r"Đúng. $MN \parallel AB$, $QP \parallel DC$ mà "
                 r"$AB \parallel DC$ nên $MN \parallel QP$." +
                 "\\\\\n" +
                 r"$MN = QP = \dfrac{1}{2}AB = %s$ nên $MNPQ$ là hình "
                 r"bình hành." % _xx(Fraction(a, 2))),
                (r"{Tứ giác $MNPQ$ là hình bình hành và $MN = %d$}" % a,
                 r"Sai. $MN$ là đường trung bình tam giác $SAB$ nên "
                 r"$MN = \dfrac{1}{2}AB = %s$, không phải $%d$."
                 % (_xx(Fraction(a, 2)), a)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF


# ----------------------------------------------------------------------
# CLAUDE THEM 30/09/2026 - goi ex_test TU THEM dau "." sau moi phuong an
# \choice, nen phuong an KHONG duoc tu cham cuoi (neu co se ra ".." tren PDF).
# Cac ham trac nghiem co phuong an la cau van (vd "Mot tuan co $7$ ngay.")
# goi _MC_khong_cham thay cho MC_SA_answer_text; math_type giu nguyen.
# ----------------------------------------------------------------------
def _bo_cham_cuoi(s):
    """Bo dau "." o cuoi phuong an (giu "\\right." cua he/tuyen va "...")."""
    s = str(s).rstrip()
    while s.endswith(".") and not s.endswith(r"\right.") and not s.endswith("..."):
        s = s[:-1].rstrip()
    return s


def _MC_khong_cham(debai, dung, nhieu, *con_lai):
    """Nhu MC_SA_answer_text nhung bo dau "." cuoi cua 4 phuong an."""
    return MC_SA_answer_text(debai, _bo_cham_cuoi(dung),
                             [_bo_cham_cuoi(x) for x in nhieu], *con_lai)
