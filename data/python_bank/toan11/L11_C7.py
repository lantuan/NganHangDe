# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 7. Quan hệ vuông góc trong không gian
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Kiến thức dùng trong tệp:

  * Góc giữa hai đường thẳng trong không gian: góc giữa hai đường thẳng
    cùng đi qua một điểm và lần lượt song song với chúng; luôn thuộc
    $\left[0^{\circ};\ 90^{\circ}\right]$.
  * $d \perp \left(P\right)$ khi $d$ vuông góc với MỌI đường thẳng nằm
    trong $\left(P\right)$; điều kiện đủ: $d$ vuông góc với hai đường
    thẳng CẮT NHAU nằm trong $\left(P\right)$.
  * Định lí ba đường vuông góc.
  * Góc giữa đường thẳng $d$ và mặt phẳng $\left(P\right)$ là góc giữa
    $d$ và hình chiếu vuông góc của nó trên $\left(P\right)$.
  * $\left(P\right) \perp \left(Q\right)$ khi góc nhị diện giữa chúng
    bằng $90^{\circ}$; điều kiện đủ: $\left(P\right)$ chứa một đường
    thẳng vuông góc với $\left(Q\right)$.
  * Khoảng cách: từ điểm đến đường thẳng, đến mặt phẳng; giữa hai
    đường thẳng chéo nhau (độ dài đoạn vuông góc chung).
  * Thể tích: khối chóp $V = \dfrac{1}{3}S_{\text{đáy}}h$; khối lăng
    trụ $V = S_{\text{đáy}}h$; khối chóp cụt đều
    $V = \dfrac{h}{3}\left(S_1 + \sqrt{S_1S_2} + S_2\right)$.

Số liệu chọn để ĐÁP SỐ ĐẸP: mọi góc đều rơi vào $30^{\circ}$,
$45^{\circ}$, $60^{\circ}$ hoặc $90^{\circ}$; mọi khoảng cách dùng bộ ba
Pytago nên là số thập phân hữu hạn; mọi thể tích đều là số NGUYÊN hoặc
số thập phân hữu hạn.

Bài học lớp 10 đã áp dụng: chữ tiếng Việt không nằm trần trong $...$;
không dùng **đậm**; mọi chuỗi có dấu gạch chéo đều là r"..."; mọi danh
sách phương án nhiễu đều qua _ba_nhieu7c; hình vẽ bằng TikZ THUẦN
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


def _ba_nhieu7c(dapso, ung_vien, buoc=None):
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


def _ps7(p, q=1):
    f = Fraction(p, q)
    if f.denominator == 1:
        return "%d" % f.numerator
    if f < 0:
        return r"-\dfrac{%d}{%d}" % (-f.numerator, f.denominator)
    return r"\dfrac{%d}{%d}" % (f.numerator, f.denominator)


def _can7c(n):
    r"""Viết $\sqrt{n}$, rút thành số nguyên khi $n$ chính phương."""
    g = int(round(math.sqrt(n)))
    return "%d" % g if g * g == n else r"\sqrt{%d}" % n


# Bộ ba Pytago: khoảng cách từ đỉnh góc vuông đến cạnh huyền là số ĐẸP.
PYTAGO7C = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15),
            (8, 15, 17), (12, 16, 20), (7, 24, 25), (20, 21, 29)]


# ---------------------------------------------------------------------
# HÌNH VẼ KHÔNG GIAN - TikZ THUẦN
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


# S.ABCD có SA vuông góc với đáy: SA vẽ THẲNG ĐỨNG từ A.
TOA_CHOP_VUONG = {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (5.3, 1.5),
                  "D": (1.3, 1.5), "S": (0.0, 3.8)}


def _hinh_chop_vuong(them=(), diem_them=()):
    r"""Hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$.

    Cạnh khuất: $AD$, $DC$ (đỉnh $D$ nằm phía sau).
    """
    T = TOA_CHOP_VUONG
    ra = []
    for p, q in (("A", "B"), ("B", "C"), ("S", "A"), ("S", "B"),
                 ("S", "C"), ("S", "D")):
        _canh(ra, T[p], T[q])
    for p, q in (("A", "D"), ("D", "C")):
        _canh(ra, T[p], T[q], "dut")
    # kí hiệu góc vuông tại A
    ra.append("\\draw (0.28,0) -- (0.28,0.28) -- (0,0.28);")
    for ten, vt in (("A", "below left"), ("B", "below right"),
                    ("C", "right"), ("D", "below"), ("S", "above")):
        _diem(ra, ten, T[ten][0], T[ten][1], vt)
    ra.extend(them)
    for ten, x, y, vt in diem_them:
        _diem(ra, ten, x, y, vt)
    return _khung(ra, 0.95)


TOA_LAP_PHUONG = {"A": (0.0, 0.0), "B": (3.4, 0.0), "C": (4.6, 1.3),
                  "D": (1.2, 1.3)}
for _k in list(TOA_LAP_PHUONG):
    TOA_LAP_PHUONG[_k + "'"] = (TOA_LAP_PHUONG[_k][0],
                                TOA_LAP_PHUONG[_k][1] + 3.0)


def _hinh_lap_phuong(them=(), diem_them=()):
    r"""Hình lập phương (hoặc hình hộp chữ nhật) $ABCD.A'B'C'D'$."""
    T = TOA_LAP_PHUONG
    ra = []
    lien = [("A", "B"), ("B", "C"), ("A", "A'"), ("B", "B'"),
            ("C", "C'"), ("A'", "B'"), ("B'", "C'"), ("C'", "D'"),
            ("D'", "A'")]
    for p, q in lien:
        _canh(ra, T[p], T[q])
    for p, q in (("A", "D"), ("D", "C"), ("D", "D'")):
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


TOA_CHOP_DEU = {"A": (0.0, 0.0), "B": (4.2, 0.0), "C": (1.5, 1.4),
                "S": (1.9, 3.6), "O": (1.9, 0.47)}


def _hinh_chop_deu(them=(), diem_them=()):
    r"""Hình chóp tam giác đều $S.ABC$ có đường cao $SO$."""
    T = TOA_CHOP_DEU
    ra = []
    for p, q in (("A", "B"), ("A", "S"), ("B", "S")):
        _canh(ra, T[p], T[q])
    for p, q in (("A", "C"), ("B", "C"), ("C", "S")):
        _canh(ra, T[p], T[q], "dut")
    _canh(ra, T["S"], T["O"], "dut")
    for ten, vt in (("A", "below left"), ("B", "below right"),
                    ("C", "below"), ("O", "below right")):
        _diem(ra, ten, T[ten][0], T[ten][1], vt)
    _diem(ra, "S", T["S"][0], T["S"][1], "above")
    ra.extend(them)
    for ten, x, y, vt in diem_them:
        _diem(ra, ten, x, y, vt)
    return _khung(ra, 0.95)


# =====================================================================
# BÀI 22. HAI ĐƯỜNG THẲNG VUÔNG GÓC
# =====================================================================

def L11_C7_B22_NB100_MC_A_01(socau, dang=1):
    r"""Nhận biết góc giữa hai đường thẳng trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Góc giữa hai đường thẳng trong không gian nhận giá trị trong "
         r"khoảng nào?",
         r"$\left[0^{\circ};\ 90^{\circ}\right]$",
         [r"$\left[0^{\circ};\ 180^{\circ}\right]$",
          r"$\left(0^{\circ};\ 90^{\circ}\right)$",
          r"$\left[90^{\circ};\ 180^{\circ}\right]$"],
         r"Góc giữa hai đường thẳng luôn được lấy là góc NHỌN hoặc "
         r"VUÔNG, nên thuộc $\left[0^{\circ};\ 90^{\circ}\right]$." +
         "\\\\\n" +
         r"Nếu góc giữa hai vectơ chỉ phương là góc tù thì ta lấy góc "
         r"bù của nó."),
        (r"Góc giữa hai đường thẳng $a$ và $b$ chéo nhau được xác định "
         r"như thế nào?",
         r"Là góc giữa hai đường thẳng cùng đi qua một điểm và lần lượt "
         r"song song với $a$, $b$",
         [r"Là góc giữa $a$ và mặt phẳng chứa $b$",
          r"Bằng $90^{\circ}$ vì hai đường chéo nhau",
          r"Không xác định được vì chúng không cắt nhau"],
         r"Qua một điểm $O$ bất kì, kẻ $a' \parallel a$ và "
         r"$b' \parallel b$; góc giữa $a'$ và $b'$ chính là góc giữa "
         r"$a$ và $b$." + "\\\\\n" +
         r"Kết quả không phụ thuộc vào cách chọn điểm $O$."),
        (r"Góc giữa hai đường thẳng song song bằng bao nhiêu?",
         r"$0^{\circ}$",
         [r"$90^{\circ}$", r"$180^{\circ}$",
          r"Không xác định"],
         r"Hai đường thẳng song song có cùng phương nên góc giữa chúng "
         r"bằng $0^{\circ}$; quy ước này cũng áp dụng cho hai đường "
         r"trùng nhau."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B22_NB101_MC_A_01(socau, dang=1):
    r"""Nhận biết hai đường thẳng vuông góc trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hai đường thẳng $a$ và $b$ gọi là vuông góc với nhau khi nào?",
         r"Khi góc giữa chúng bằng $90^{\circ}$",
         [r"Khi chúng cắt nhau", r"Khi chúng chéo nhau",
          r"Khi chúng cùng nằm trong một mặt phẳng"],
         r"Kí hiệu $a \perp b$. Hai đường thẳng vuông góc CÓ THỂ cắt "
         r"nhau, cũng có thể CHÉO NHAU."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Đường thẳng nào sau đây "
         r"vuông góc với $AB$?",
         r"$BC$", [r"$CD$", r"$A'B'$", r"$C'D'$"],
         r"$ABCD$ là hình vuông nên $AB \perp BC$." + "\\\\\n" +
         r"Còn $CD$, $A'B'$, $C'D'$ đều SONG SONG với $AB$ nên góc giữa "
         r"chúng với $AB$ bằng $0^{\circ}$.", "lp"),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$AB$ và $CC'$ bằng",
         r"$90^{\circ}$", [r"$0^{\circ}$", r"$45^{\circ}$",
                           r"$60^{\circ}$"],
         r"$CC' \parallel BB'$ mà $BB' \perp AB$ (mặt $ABB'A'$ là hình "
         r"vuông)." + "\\\\\n" +
         r"Vậy góc giữa $AB$ và $CC'$ bằng $90^{\circ}$; hai đường này "
         r"CHÉO NHAU nhưng vẫn vuông góc.", "lp"),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        bo = MAU[i]
        hoi, dung, nhieu, ly_do = bo[0], bo[1], bo[2], bo[3]
        hinh = _hinh_lap_phuong() if len(bo) > 4 else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C7_B22_TH102_MC_A_01(socau, dang=1):
    r"""Chứng minh hai đường thẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$AC$ và $B'D'$ bằng",
         r"$90^{\circ}$", [r"$0^{\circ}$", r"$45^{\circ}$",
                           r"$60^{\circ}$"],
         r"$B'D' \parallel BD$ (mặt $BDD'B'$ là hình bình hành)." +
         "\\\\\n" +
         r"Trong hình vuông $ABCD$ hai đường chéo vuông góc nên "
         r"$AC \perp BD$." + "\\\\\n" +
         r"Vậy góc giữa $AC$ và $B'D'$ bằng $90^{\circ}$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$AB$ và $B'C'$ bằng",
         r"$90^{\circ}$", [r"$0^{\circ}$", r"$45^{\circ}$",
                           r"$30^{\circ}$"],
         r"$B'C' \parallel BC$ và $AB \perp BC$ (hình vuông $ABCD$)." +
         "\\\\\n" +
         r"Vậy $AB \perp B'C'$, góc bằng $90^{\circ}$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$AC$ và $A'B'$ bằng",
         r"$45^{\circ}$", [r"$90^{\circ}$", r"$0^{\circ}$",
                           r"$60^{\circ}$"],
         r"$A'B' \parallel AB$ nên góc giữa $AC$ và $A'B'$ bằng góc giữa "
         r"$AC$ và $AB$." + "\\\\\n" +
         r"Trong hình vuông $ABCD$, $AC$ là đường chéo nên "
         r"$\widehat{BAC} = 45^{\circ}$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do,
                                   _hinh_lap_phuong(), 0, dang)
    return cauTN


def L11_C7_B22_TH102_TL_A_01(socau, dong=1):
    r"""Tự luận: chứng minh hai đường thẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_lap_phuong()
        debai = r"Cho hình lập phương $ABCD.A'B'C'D'$."

        hoi_a = r"Chứng minh $AB \perp CC'$."
        giai_a = (r"$CC' \parallel BB'$ (hai cạnh bên của hình lập "
                  r"phương)." +
                  "\\\\\n"
                  r"Mặt $ABB'A'$ là hình vuông nên $AB \perp BB'$." +
                  "\\\\\n"
                  r"Vậy $AB \perp CC'$ (dù hai đường này CHÉO nhau).")

        hoi_b = r"Chứng minh $AC \perp BD$ và $AC \perp B'D'$."
        giai_b = (r"Trong hình vuông $ABCD$, hai đường chéo vuông góc "
                  r"với nhau nên $AC \perp BD$." +
                  "\\\\\n"
                  r"Mặt $BDD'B'$ là hình bình hành nên "
                  r"$B'D' \parallel BD$." +
                  "\\\\\n"
                  r"Từ $AC \perp BD$ và $B'D' \parallel BD$ suy ra "
                  r"$AC \perp B'D'$.")

        hoi_c = r"Tính góc giữa hai đường thẳng $AC$ và $A'B'$."
        giai_c = (r"$A'B' \parallel AB$ nên góc giữa $AC$ và $A'B'$ bằng "
                  r"góc giữa $AC$ và $AB$." +
                  "\\\\\n"
                  r"Trong hình vuông $ABCD$, $AC$ là đường chéo xuất "
                  r"phát từ $A$ nên $\widehat{BAC} = 45^{\circ}$." +
                  "\\\\\n"
                  r"Vậy góc cần tìm bằng $45^{\circ}$.")

        ds_abcd = [(hoi_a, r"AB \perp CC'", giai_a),
                   (hoi_b, r"AC \perp BD \text{ và } AC \perp B'D'",
                    giai_b),
                   (hoi_c, r"45^{\circ}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B22_VD103_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về hai đường thẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$AB'$ và $BC'$ bằng",
         r"$60^{\circ}$", [r"$90^{\circ}$", r"$45^{\circ}$",
                           r"$30^{\circ}$"],
         r"$BC' \parallel AD'$ nên góc giữa $AB'$ và $BC'$ bằng góc giữa "
         r"$AB'$ và $AD'$." + "\\\\\n" +
         r"Tam giác $AB'D'$ có ba cạnh đều là đường chéo của các mặt "
         r"hình lập phương nên là tam giác ĐỀU." + "\\\\\n" +
         r"Vậy góc cần tìm bằng $60^{\circ}$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$AC$ và $BD'$ bằng",
         r"$90^{\circ}$", [r"$60^{\circ}$", r"$45^{\circ}$",
                           r"$30^{\circ}$"],
         r"$AC \perp BD$ (hai đường chéo hình vuông) và $AC \perp BB'$ "
         r"($BB'$ vuông góc với mặt đáy)." + "\\\\\n" +
         r"$BD$ và $BB'$ cắt nhau và cùng nằm trong "
         r"$\left(BDD'B'\right)$, nên "
         r"$AC \perp \left(BDD'B'\right)$." + "\\\\\n" +
         r"Mà $BD' \subset \left(BDD'B'\right)$ nên $AC \perp BD'$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa hai đường thẳng "
         r"$A'C'$ và $BD$ bằng",
         r"$90^{\circ}$", [r"$60^{\circ}$", r"$45^{\circ}$",
                           r"$0^{\circ}$"],
         r"$A'C' \parallel AC$ (mặt $ACC'A'$ là hình bình hành)." +
         "\\\\\n" +
         r"Trong hình vuông $ABCD$ có $AC \perp BD$." + "\\\\\n" +
         r"Vậy $A'C' \perp BD$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do,
                                   _hinh_lap_phuong(), 0, dang)
    return cauTN


def L11_C7_B22_VD103_SA_A_01(socau):
    r"""Số đo góc giữa hai đường thẳng - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"$AB'$ và $BC'$", 60,
         r"$BC' \parallel AD'$ nên góc cần tìm bằng góc giữa $AB'$ và "
         r"$AD'$." + "\\\\\n" +
         r"Tam giác $AB'D'$ có ba cạnh cùng là đường chéo của các mặt "
         r"nên là tam giác đều, do đó góc bằng $60^{\circ}$."),
        (r"$AC$ và $B'D'$", 90,
         r"$B'D' \parallel BD$ và $AC \perp BD$ (hai đường chéo hình "
         r"vuông)." + "\\\\\n" +
         r"Vậy góc bằng $90^{\circ}$."),
        (r"$AC$ và $A'B'$", 45,
         r"$A'B' \parallel AB$ nên góc cần tìm bằng "
         r"$\widehat{BAC} = 45^{\circ}$ (góc giữa cạnh và đường chéo "
         r"của hình vuông)."),
        (r"$AB$ và $C'D'$", 0,
         r"$C'D' \parallel CD \parallel AB$ nên hai đường thẳng song "
         r"song, góc giữa chúng bằng $0^{\circ}$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cau = ""
    for i in gt:
        mo_ta, dap, giai = MAU[i]
        debai = (r"Cho hình lập phương $ABCD.A'B'C'D'$. Tính số đo góc "
                 r"giữa hai đường thẳng %s (đơn vị: độ)." % mo_ta)
        nhieu = _ba_nhieu7c(str(dap), ["90", "60", "45", "30", "0"],
                            buoc=lambda t: str(dap + 10 * t))
        cau += MC_SA_answer_const(debai, str(dap), nhieu, giai,
                                  _hinh_lap_phuong(), 0, 2)
    return cau


def L11_C7_B22_VD103_TL_A_01(socau, dong=1):
    r"""Tự luận: vận dụng hai đường thẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_lap_phuong()
        debai = (r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $a$.")

        hoi_a = r"Tính góc giữa hai đường thẳng $AC$ và $B'D'$."
        giai_a = (r"$B'D' \parallel BD$ nên góc giữa $AC$ và $B'D'$ bằng "
                  r"góc giữa $AC$ và $BD$." +
                  "\\\\\n"
                  r"Hai đường chéo của hình vuông $ABCD$ vuông góc với "
                  r"nhau nên góc bằng $90^{\circ}$.")

        hoi_b = r"Tính góc giữa hai đường thẳng $AB'$ và $BC'$."
        giai_b = (r"$BC' \parallel AD'$ nên góc giữa $AB'$ và $BC'$ bằng "
                  r"góc giữa $AB'$ và $AD'$." +
                  "\\\\\n"
                  r"$AB' = AD' = B'D' = a\sqrt{2}$ (đều là đường chéo "
                  r"của một mặt hình vuông cạnh $a$)." +
                  "\\\\\n"
                  r"Tam giác $AB'D'$ đều nên "
                  r"$\widehat{B'AD'} = 60^{\circ}$.")

        hoi_c = (r"Gọi $M$, $N$ lần lượt là trung điểm của $AB$ và $CC'$. "
                 r"Chứng minh $MN$ không vuông góc với $AB$.")
        giai_c = (r"Chọn hệ toạ độ với $A$ là gốc, "
                  r"$AB$, $AD$, $AA'$ là ba trục." +
                  "\\\\\n"
                  r"Khi đó $M\left(\dfrac{a}{2};\ 0;\ 0\right)$ và "
                  r"$N\left(a;\ a;\ \dfrac{a}{2}\right)$." +
                  "\\\\\n"
                  r"$\overrightarrow{MN} = \left(\dfrac{a}{2};\ a;\ "
                  r"\dfrac{a}{2}\right)$ và "
                  r"$\overrightarrow{AB} = \left(a;\ 0;\ 0\right)$." +
                  "\\\\\n"
                  r"Tích vô hướng bằng $\dfrac{a^{2}}{2} \neq 0$ nên "
                  r"$MN$ KHÔNG vuông góc với $AB$.")

        ds_abcd = [(hoi_a, r"90^{\circ}", giai_a),
                   (hoi_b, r"60^{\circ}", giai_b),
                   (hoi_c, r"MN \text{ không vuông góc } AB", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 23. ĐƯỜNG THẲNG VUÔNG GÓC VỚI MẶT PHẲNG
# =====================================================================

def L11_C7_B23_NB104_MC_A_01(socau, dang=1):
    r"""Nhận biết đường thẳng vuông góc với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Đường thẳng $d$ gọi là vuông góc với mặt phẳng "
         r"$\left(P\right)$ khi nào?",
         r"Khi $d$ vuông góc với MỌI đường thẳng nằm trong "
         r"$\left(P\right)$",
         [r"Khi $d$ vuông góc với một đường thẳng nằm trong "
          r"$\left(P\right)$",
          r"Khi $d$ cắt $\left(P\right)$",
          r"Khi $d$ song song với $\left(P\right)$"],
         r"Đó là ĐỊNH NGHĨA. Còn ĐIỀU KIỆN ĐỦ để kiểm tra trong thực "
         r"hành là: $d$ vuông góc với hai đường thẳng CẮT NHAU nằm "
         r"trong $\left(P\right)$."),
        (r"Qua một điểm $O$ cho trước, có bao nhiêu mặt phẳng vuông góc "
         r"với một đường thẳng $d$ cho trước?",
         r"$1$", [r"$0$", r"$2$", r"vô số"],
         r"Qua một điểm có DUY NHẤT một mặt phẳng vuông góc với một "
         r"đường thẳng cho trước."),
        (r"Qua một điểm $O$ cho trước, có bao nhiêu đường thẳng vuông "
         r"góc với một mặt phẳng $\left(P\right)$ cho trước?",
         r"$1$", [r"$0$", r"$2$", r"vô số"],
         r"Qua một điểm có DUY NHẤT một đường thẳng vuông góc với một "
         r"mặt phẳng cho trước; đường thẳng đó cắt $\left(P\right)$ tại "
         r"hình chiếu vuông góc của $O$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B23_TH105_MC_A_01(socau, dang=1):
    r"""Điều kiện để đường thẳng vuông góc với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Điều kiện nào sau đây ĐỦ để kết luận "
         r"$d \perp \left(P\right)$?",
         r"$d$ vuông góc với hai đường thẳng CẮT NHAU nằm trong "
         r"$\left(P\right)$",
         [r"$d$ vuông góc với một đường thẳng nằm trong "
          r"$\left(P\right)$",
          r"$d$ vuông góc với hai đường thẳng song song nằm trong "
          r"$\left(P\right)$",
          r"$d$ cắt $\left(P\right)$ tại một điểm"],
         r"Điều kiện ``CẮT NHAU'' là bắt buộc." + "\\\\\n" +
         r"Nếu hai đường thẳng đó song song thì $d$ chỉ vuông góc với "
         r"MỘT phương, chưa đủ để vuông góc với cả mặt phẳng.", 0),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$ và đáy "
         r"$ABCD$ là hình vuông. Khẳng định nào sau đây ĐÚNG?",
         r"$BC \perp \left(SAB\right)$",
         [r"$BC \perp \left(SAD\right)$",
          r"$BC \perp \left(SAC\right)$",
          r"$BC \perp \left(SBD\right)$"],
         r"$SA \perp \left(ABCD\right)$ nên $SA \perp BC$." + "\\\\\n" +
         r"$ABCD$ là hình vuông nên $AB \perp BC$." + "\\\\\n" +
         r"$SA$ và $AB$ cắt nhau tại $A$ và cùng nằm trong "
         r"$\left(SAB\right)$." + "\\\\\n" +
         r"Vậy $BC \perp \left(SAB\right)$.", 1),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$ và đáy "
         r"$ABCD$ là hình vuông. Khẳng định nào sau đây ĐÚNG?",
         r"$BD \perp \left(SAC\right)$",
         [r"$BD \perp \left(SAB\right)$",
          r"$BD \perp \left(SAD\right)$",
          r"$AC \perp \left(SBD\right)$"],
         r"$SA \perp \left(ABCD\right)$ nên $SA \perp BD$." + "\\\\\n" +
         r"$ABCD$ là hình vuông nên $AC \perp BD$." + "\\\\\n" +
         r"$SA$ và $AC$ cắt nhau tại $A$ và cùng nằm trong "
         r"$\left(SAC\right)$." + "\\\\\n" +
         r"Vậy $BD \perp \left(SAC\right)$.", 1),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do, co_hinh = MAU[i]
        hinh = _hinh_chop_vuong() if co_hinh else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C7_B23_TH105_TL_A_01(socau, dong=1):
    r"""Tự luận: chứng minh đường thẳng vuông góc với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = _chon_chi_muc(2, socau)

    cauTN = ""
    for i in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông và "
                 r"$SA \perp \left(ABCD\right)$.")

        hoi_a = r"Chứng minh $BC \perp \left(SAB\right)$."
        giai_a = (r"$SA \perp \left(ABCD\right)$ mà "
                  r"$BC \subset \left(ABCD\right)$ nên $SA \perp BC$." +
                  "\\\\\n"
                  r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                  "\\\\\n"
                  r"$SA$ và $AB$ là hai đường thẳng CẮT NHAU tại $A$ và "
                  r"cùng nằm trong $\left(SAB\right)$." +
                  "\\\\\n"
                  r"Vậy $BC \perp \left(SAB\right)$.")

        hoi_b = r"Chứng minh $BD \perp \left(SAC\right)$."
        giai_b = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp BD$." +
                  "\\\\\n"
                  r"Hai đường chéo của hình vuông vuông góc nên "
                  r"$AC \perp BD$." +
                  "\\\\\n"
                  r"$SA$ và $AC$ cắt nhau tại $A$, cùng nằm trong "
                  r"$\left(SAC\right)$." +
                  "\\\\\n"
                  r"Vậy $BD \perp \left(SAC\right)$.")

        hoi_c = r"Suy ra $BC \perp SB$ và $BD \perp SC$."
        giai_c = (r"Theo câu a, $BC \perp \left(SAB\right)$ mà "
                  r"$SB \subset \left(SAB\right)$ nên $BC \perp SB$." +
                  "\\\\\n"
                  r"Theo câu b, $BD \perp \left(SAC\right)$ mà "
                  r"$SC \subset \left(SAC\right)$ nên $BD \perp SC$." +
                  "\\\\\n"
                  r"Đây là cách dùng quan hệ ``đường vuông góc mặt'' để "
                  r"suy ra ``đường vuông góc đường''.")

        ds_abcd = [(hoi_a, r"BC \perp \left(SAB\right)", giai_a),
                   (hoi_b, r"BD \perp \left(SAC\right)", giai_b),
                   (hoi_c, r"BC \perp SB,\ BD \perp SC", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B23_TH106_MC_A_01(socau, dang=1):
    r"""Định lí ba đường vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho đường thẳng $a$ nằm trong mặt phẳng $\left(P\right)$ và "
         r"đường thẳng $b$ không vuông góc với $\left(P\right)$, có hình "
         r"chiếu vuông góc trên $\left(P\right)$ là $b'$. Định lí ba "
         r"đường vuông góc khẳng định điều gì?",
         r"$a \perp b \Leftrightarrow a \perp b'$",
         [r"$a \perp b \Rightarrow b \perp \left(P\right)$",
          r"$a \parallel b \Leftrightarrow a \parallel b'$",
          r"$a \perp b' \Rightarrow a \parallel b$"],
         r"Định lí ba đường vuông góc cho phép chuyển việc kiểm tra "
         r"$a \perp b$ (trong không gian) thành kiểm tra $a \perp b'$ "
         r"(trong mặt phẳng), dễ hơn nhiều."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$, đáy "
         r"$ABCD$ là hình vuông. Hình chiếu vuông góc của $SC$ trên mặt "
         r"phẳng $\left(ABCD\right)$ là",
         r"$AC$", [r"$BC$", r"$CD$", r"$SA$"],
         r"$S$ có hình chiếu vuông góc trên $\left(ABCD\right)$ là $A$ "
         r"(vì $SA \perp \left(ABCD\right)$)." + "\\\\\n" +
         r"$C$ đã thuộc $\left(ABCD\right)$ nên hình chiếu của nó là "
         r"chính nó." + "\\\\\n" +
         r"Vậy hình chiếu của $SC$ là $AC$."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$, đáy "
         r"$ABCD$ là hình vuông. Dùng định lí ba đường vuông góc, ta suy "
         r"ra được điều nào sau đây?",
         r"$BD \perp SC$ vì $BD \perp AC$",
         [r"$BD \perp SC$ vì $BD \perp SA$",
          r"$BC \perp SC$ vì $BC \perp AC$",
          r"$AC \perp SB$ vì $AC \perp AB$"],
         r"Hình chiếu vuông góc của $SC$ trên $\left(ABCD\right)$ là "
         r"$AC$." + "\\\\\n" +
         r"Trong hình vuông có $BD \perp AC$." + "\\\\\n" +
         r"Theo định lí ba đường vuông góc, $BD \perp SC$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_vuong() if "hình chóp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C7_B23_TH107_MC_A_01(socau, dang=1):
    r"""Liên hệ giữa tính song song và tính vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho $a \parallel b$ và $a \perp \left(P\right)$. Khi đó",
         r"$b \perp \left(P\right)$",
         [r"$b \parallel \left(P\right)$",
          r"$b \subset \left(P\right)$",
          r"$b$ cắt $\left(P\right)$ nhưng không vuông góc"],
         r"Hai đường thẳng song song thì cùng phương; nếu một đường "
         r"vuông góc với mặt phẳng thì đường kia cũng vậy."),
        (r"Cho $a \perp \left(P\right)$ và $b \perp \left(P\right)$ với "
         r"$a \neq b$. Khi đó",
         r"$a \parallel b$",
         [r"$a$ cắt $b$", r"$a$ và $b$ chéo nhau",
          r"$a \perp b$"],
         r"Hai đường thẳng phân biệt cùng vuông góc với một mặt phẳng "
         r"thì song song với nhau."),
        (r"Cho $\left(P\right) \parallel \left(Q\right)$ và "
         r"$a \perp \left(P\right)$. Khi đó",
         r"$a \perp \left(Q\right)$",
         [r"$a \parallel \left(Q\right)$",
          r"$a \subset \left(Q\right)$",
          r"$a$ cắt $\left(Q\right)$ nhưng không vuông góc"],
         r"Hai mặt phẳng song song có cùng phương pháp tuyến, nên đường "
         r"thẳng vuông góc với mặt này cũng vuông góc với mặt kia."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B23_VD108_MC_A_01(socau, dang=1):
    r"""Vận dụng đường thẳng vuông góc với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$, đáy "
         r"$ABCD$ là hình vuông. Số mặt bên của hình chóp là tam giác "
         r"VUÔNG bằng",
         r"$4$", [r"$2$", r"$3$", r"$1$"],
         r"$SA \perp AB$ và $SA \perp AD$ nên $SAB$ và $SAD$ vuông tại "
         r"$A$." + "\\\\\n" +
         r"$BC \perp \left(SAB\right)$ nên $BC \perp SB$, do đó $SBC$ "
         r"vuông tại $B$." + "\\\\\n" +
         r"Tương tự $CD \perp \left(SAD\right)$ nên $SCD$ vuông tại "
         r"$D$." + "\\\\\n" +
         r"Vậy cả $4$ mặt bên đều là tam giác vuông."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$, đáy "
         r"$ABCD$ là hình vuông. Mặt phẳng nào sau đây chứa $BD$ và "
         r"vuông góc với $\left(SAC\right)$?",
         r"$\left(ABCD\right)$",
         [r"$\left(SAB\right)$", r"$\left(SAD\right)$",
          r"$\left(SBC\right)$"],
         r"Ta có $BD \perp \left(SAC\right)$ (vì $BD \perp AC$ và "
         r"$BD \perp SA$)." + "\\\\\n" +
         r"Mặt phẳng $\left(ABCD\right)$ chứa $BD$ nên "
         r"$\left(ABCD\right) \perp \left(SAC\right)$." + "\\\\\n" +
         r"Các mặt còn lại không chứa $BD$."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$, đáy "
         r"$ABCD$ là hình vuông. Hình chiếu vuông góc của $S$ trên "
         r"$\left(ABCD\right)$ là",
         r"điểm $A$", [r"điểm $B$", r"tâm hình vuông",
                       r"trung điểm $AB$"],
         r"Theo định nghĩa, hình chiếu vuông góc của $S$ là giao điểm "
         r"của đường thẳng qua $S$ vuông góc với $\left(ABCD\right)$ và "
         r"mặt phẳng đó." + "\\\\\n" +
         r"Đường thẳng ấy chính là $SA$, cắt $\left(ABCD\right)$ tại "
         r"$A$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do,
                                   _hinh_chop_vuong(), 0, dang)
    return cauTN


def L11_C7_B23_VD108_SA_A_01(socau):
    r"""Độ dài cạnh bên trong hình chóp có cạnh vuông góc đáy - SA.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(PYTAGO7C)
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cau = ""
    for a, h, c in gt:
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$ và $SA \perp \left(ABCD\right)$ với "
                 r"$SA = %d$. Tính độ dài $SB$." % (a, h))
        giai = (r"$SA \perp \left(ABCD\right)$ mà "
                r"$AB \subset \left(ABCD\right)$ nên $SA \perp AB$." +
                "\\\\\n"
                r"Tam giác $SAB$ vuông tại $A$." +
                "\\\\\n"
                r"$SB = \sqrt{SA^{2} + AB^{2}} = "
                r"\sqrt{%d^{2} + %d^{2}} = \sqrt{%d} = %d$."
                % (h, a, h * h + a * a, c))
        nhieu = _ba_nhieu7c(str(c), [str(a), str(h), str(a + h)],
                            buoc=lambda t: str(c + t))
        cau += MC_SA_answer_const(debai, str(c), nhieu, giai,
                                  _hinh_chop_vuong(), 0, 2)
    return cau


def L11_C7_B23_VD108_TL_A_01(socau, dong=1):
    r"""Tự luận: vận dụng đường thẳng vuông góc với mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(PYTAGO7C)
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cauTN = ""
    for a, h, c in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$ và $SA \perp \left(ABCD\right)$ với "
                 r"$SA = %d$." % (a, h))

        hoi_a = r"Chứng minh $BC \perp \left(SAB\right)$."
        giai_a = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp BC$." +
                  "\\\\\n"
                  r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                  "\\\\\n"
                  r"$SA$ và $AB$ cắt nhau tại $A$, cùng nằm trong "
                  r"$\left(SAB\right)$, nên "
                  r"$BC \perp \left(SAB\right)$.")

        hoi_b = r"Tính độ dài $SB$."
        giai_b = (r"Tam giác $SAB$ vuông tại $A$ (vì $SA \perp AB$)." +
                  "\\\\\n"
                  r"$SB = \sqrt{SA^{2} + AB^{2}} = "
                  r"\sqrt{%d^{2} + %d^{2}} = %d$." % (h, a, c))

        hoi_c = r"Tính độ dài $SC$."
        giai_c = (r"$AC$ là đường chéo hình vuông cạnh $%d$ nên "
                  r"$AC = %d\sqrt{2}$." % (a, a) +
                  "\\\\\n"
                  r"Tam giác $SAC$ vuông tại $A$ (vì "
                  r"$SA \perp \left(ABCD\right)$ nên $SA \perp AC$)." +
                  "\\\\\n"
                  r"$SC = \sqrt{SA^{2} + AC^{2}} = "
                  r"\sqrt{%d + %d} = %s$."
                  % (h * h, 2 * a * a, _can7c(h * h + 2 * a * a)))

        ds_abcd = [(hoi_a, r"BC \perp \left(SAB\right)", giai_a),
                   (hoi_b, r"SB = %d" % c, giai_b),
                   (hoi_c, r"SC = %s" % _can7c(h * h + 2 * a * a),
                    giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 24. PHÉP CHIẾU VUÔNG GÓC. GÓC GIỮA ĐƯỜNG THẲNG VÀ MẶT PHẲNG
# =====================================================================

def L11_C7_B24_NB109_MC_A_01(socau, dang=1):
    r"""Nhận biết phép chiếu vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Phép chiếu vuông góc lên mặt phẳng $\left(P\right)$ là phép "
         r"chiếu song song theo phương nào?",
         r"Phương vuông góc với $\left(P\right)$",
         [r"Phương song song với $\left(P\right)$",
          r"Phương bất kì", r"Phương nằm trong $\left(P\right)$"],
         r"Phép chiếu vuông góc là TRƯỜNG HỢP RIÊNG của phép chiếu song "
         r"song, với phương chiếu vuông góc với mặt phẳng chiếu." +
         "\\\\\n" +
         r"Vì vậy nó có đầy đủ các tính chất của phép chiếu song song."),
        (r"Hình chiếu vuông góc của điểm $M$ trên mặt phẳng "
         r"$\left(P\right)$ là",
         r"giao điểm của $\left(P\right)$ với đường thẳng qua $M$ và "
         r"vuông góc với $\left(P\right)$",
         [r"điểm bất kì của $\left(P\right)$",
          r"giao điểm của $\left(P\right)$ với một đường thẳng bất kì "
          r"qua $M$",
          r"chính điểm $M$"],
         r"Qua $M$ có DUY NHẤT một đường thẳng vuông góc với "
         r"$\left(P\right)$; giao điểm của nó với $\left(P\right)$ là "
         r"hình chiếu vuông góc của $M$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B24_NB111_MC_A_01(socau, dang=1):
    r"""Nhận biết góc giữa đường thẳng và mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Góc giữa đường thẳng $d$ (không vuông góc với "
         r"$\left(P\right)$) và mặt phẳng $\left(P\right)$ là",
         r"góc giữa $d$ và hình chiếu vuông góc của $d$ trên "
         r"$\left(P\right)$",
         [r"góc giữa $d$ và một đường thẳng bất kì trong "
          r"$\left(P\right)$",
          r"góc giữa $d$ và đường thẳng vuông góc với "
          r"$\left(P\right)$",
          r"luôn bằng $90^{\circ}$"],
         r"Đây là định nghĩa. Góc này luôn thuộc "
         r"$\left[0^{\circ};\ 90^{\circ}\right]$ và là góc NHỎ NHẤT "
         r"trong các góc giữa $d$ với các đường thẳng trong "
         r"$\left(P\right)$."),
        (r"Nếu $d \perp \left(P\right)$ thì góc giữa $d$ và "
         r"$\left(P\right)$ bằng",
         r"$90^{\circ}$", [r"$0^{\circ}$", r"$45^{\circ}$",
                           r"không xác định"],
         r"Theo quy ước, khi $d$ vuông góc với mặt phẳng thì góc giữa "
         r"chúng bằng $90^{\circ}$."),
        (r"Nếu $d \parallel \left(P\right)$ hoặc "
         r"$d \subset \left(P\right)$ thì góc giữa $d$ và "
         r"$\left(P\right)$ bằng",
         r"$0^{\circ}$", [r"$90^{\circ}$", r"$45^{\circ}$",
                          r"không xác định"],
         r"Khi đó hình chiếu của $d$ song song (hoặc trùng) với $d$, "
         r"nên góc bằng $0^{\circ}$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B24_TH110_MC_A_01(socau, dang=1):
    r"""Hình chiếu vuông góc của điểm, đường thẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"$S$ trên $\left(ABCD\right)$", r"$A$", [r"$B$", r"$C$",
                                                   r"tâm hình vuông"],
         r"$SA \perp \left(ABCD\right)$ nên đường thẳng qua $S$ vuông "
         r"góc với đáy chính là $SA$, cắt đáy tại $A$."),
        (r"$SB$ trên $\left(ABCD\right)$", r"$AB$", [r"$BC$", r"$AC$",
                                                     r"$BD$"],
         r"Hình chiếu của $S$ là $A$, hình chiếu của $B$ là chính $B$." +
         "\\\\\n" +
         r"Vậy hình chiếu của đoạn $SB$ là đoạn $AB$."),
        (r"$SC$ trên $\left(ABCD\right)$", r"$AC$", [r"$BC$", r"$CD$",
                                                     r"$BD$"],
         r"Hình chiếu của $S$ là $A$, của $C$ là chính $C$, nên hình "
         r"chiếu của $SC$ là $AC$."),
        (r"$SD$ trên $\left(ABCD\right)$", r"$AD$", [r"$CD$", r"$AC$",
                                                     r"$BD$"],
         r"Hình chiếu của $S$ là $A$, của $D$ là chính $D$, nên hình "
         r"chiếu của $SD$ là $AD$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        mo_ta, dung, nhieu, ly_do = MAU[i]
        debai = (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD"
                 r"\right)$ và đáy $ABCD$ là hình vuông. Hình chiếu "
                 r"vuông góc của %s là" % mo_ta)
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), ly_do,
                                   _hinh_chop_vuong(), 0, dang)
    return cauTN


def L11_C7_B24_TH112_MC_A_01(socau, dang=1):
    r"""Xác định và tính góc giữa đường thẳng và mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Chọn $SA = AB$ để góc bằng đúng $45^{\circ}$, hoặc
    $SA = AB\sqrt{3}$ để góc bằng $60^{\circ}$ - luôn là góc đẹp.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        kieu = random.choice(["45", "60", "30"])
        if (a, kieu) not in gt:
            gt.append((a, kieu))

    cauTN = ""
    for a, kieu in gt:
        if kieu == "45":
            sa = "%d" % a
            goc = "45^{\\circ}"
            tan = "1"
        elif kieu == "60":
            sa = r"%d\sqrt{3}" % a
            goc = "60^{\\circ}"
            tan = r"\sqrt{3}"
        else:
            sa = r"\dfrac{%d\sqrt{3}}{3}" % a
            goc = "30^{\\circ}"
            tan = r"\dfrac{\sqrt{3}}{3}"
        dung = "$%s$" % goc
        nhieu = _ba_nhieu7c(dung, [r"$30^{\circ}$", r"$45^{\circ}$",
                                   r"$60^{\circ}$", r"$90^{\circ}$"],
                            buoc=lambda t: r"$%d^{\circ}$" % (10 * t))
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %s$. Tính góc giữa đường thẳng $SB$ và mặt "
                 r"phẳng $\left(ABCD\right)$." % (a, sa))
        giai = (r"Hình chiếu vuông góc của $S$ trên $\left(ABCD\right)$ "
                r"là $A$, nên hình chiếu của $SB$ là $AB$." +
                "\\\\\n"
                r"Vậy góc giữa $SB$ và $\left(ABCD\right)$ là góc "
                r"$\widehat{SBA}$." +
                "\\\\\n"
                r"Tam giác $SAB$ vuông tại $A$ nên "
                r"$\tan\widehat{SBA} = \dfrac{SA}{AB} = "
                r"\dfrac{%s}{%d} = %s$." % (sa, a, tan) +
                "\\\\\n"
                r"Suy ra $\widehat{SBA} = %s$." % goc)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_chop_vuong(), 0, dang)
    return cauTN
