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


# =====================================================================
# BÀI 25. HAI MẶT PHẲNG VUÔNG GÓC
# =====================================================================

def L11_C7_B25_NB113_MC_A_01(socau, dang=1):
    r"""Nhận biết hai mặt phẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hai mặt phẳng gọi là vuông góc với nhau khi nào?",
         r"Khi góc giữa chúng bằng $90^{\circ}$",
         [r"Khi chúng cắt nhau",
          r"Khi mọi đường thẳng của mặt này đều vuông góc với mặt kia",
          r"Khi chúng không có điểm chung"],
         r"Góc giữa hai mặt phẳng cắt nhau là góc phẳng nhị diện tạo "
         r"bởi chúng; bằng $90^{\circ}$ thì hai mặt phẳng vuông góc."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$. Mặt "
         r"phẳng nào sau đây vuông góc với $\left(ABCD\right)$?",
         r"$\left(SAB\right)$",
         [r"$\left(SBC\right)$", r"$\left(SCD\right)$",
          r"$\left(SBD\right)$"],
         r"$\left(SAB\right)$ chứa đường thẳng $SA$ mà "
         r"$SA \perp \left(ABCD\right)$." + "\\\\\n" +
         r"Theo điều kiện đủ, "
         r"$\left(SAB\right) \perp \left(ABCD\right)$." + "\\\\\n" +
         r"Các mặt còn lại không chứa $SA$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_vuong() if "hình chóp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C7_B25_NB113_SA_A_01(socau):
    r"""Số đo góc giữa đường thẳng và mặt phẳng - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        kieu = random.choice(["45", "60", "30", "90"])
        if (a, kieu) not in gt:
            gt.append((a, kieu))

    cau = ""
    for a, kieu in gt:
        if kieu == "90":
            debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình "
                     r"vuông cạnh $%d$ và $SA \perp \left(ABCD\right)$. "
                     r"Tính số đo góc giữa đường thẳng $SA$ và mặt phẳng "
                     r"$\left(ABCD\right)$ (đơn vị: độ)." % a)
            giai = (r"Theo giả thiết $SA \perp \left(ABCD\right)$." +
                    "\\\\\n"
                    r"Theo quy ước, khi đường thẳng vuông góc với mặt "
                    r"phẳng thì góc giữa chúng bằng $90^{\circ}$.")
            dap = "90"
        else:
            if kieu == "45":
                sa, tan = "%d" % a, "1"
            elif kieu == "60":
                sa, tan = r"%d\sqrt{3}" % a, r"\sqrt{3}"
            else:
                sa, tan = (r"\dfrac{%d\sqrt{3}}{3}" % a,
                           r"\dfrac{\sqrt{3}}{3}")
            dap = kieu
            debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình "
                     r"vuông cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                     r"$SA = %s$. Tính số đo góc giữa đường thẳng $SD$ "
                     r"và mặt phẳng $\left(ABCD\right)$ (đơn vị: độ)."
                     % (a, sa))
            giai = (r"Hình chiếu vuông góc của $S$ trên "
                    r"$\left(ABCD\right)$ là $A$, nên hình chiếu của "
                    r"$SD$ là $AD$." +
                    "\\\\\n"
                    r"Góc cần tìm là $\widehat{SDA}$." +
                    "\\\\\n"
                    r"Tam giác $SAD$ vuông tại $A$ nên "
                    r"$\tan\widehat{SDA} = \dfrac{SA}{AD} = "
                    r"\dfrac{%s}{%d} = %s$." % (sa, a, tan) +
                    "\\\\\n"
                    r"Suy ra $\widehat{SDA} = %s^{\circ}$." % dap)
        nhieu = _ba_nhieu7c(dap, ["30", "45", "60", "90"],
                            buoc=lambda t: str(10 * t))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai,
                                  _hinh_chop_vuong(), 0, 2)
    return cau


def L11_C7_B25_NB113_TL_A_01(socau, dong=1):
    r"""Tự luận: xác định và tính góc giữa đường thẳng và mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, a))

        hoi_a = (r"Xác định hình chiếu vuông góc của $SB$ trên mặt phẳng "
                 r"$\left(ABCD\right)$.")
        giai_a = (r"$SA \perp \left(ABCD\right)$ nên hình chiếu vuông "
                  r"góc của $S$ trên $\left(ABCD\right)$ là $A$." +
                  "\\\\\n"
                  r"$B$ đã thuộc $\left(ABCD\right)$ nên hình chiếu của "
                  r"$B$ là chính nó." +
                  "\\\\\n"
                  r"Vậy hình chiếu của $SB$ là $AB$.")

        hoi_b = (r"Tính góc giữa $SB$ và mặt phẳng "
                 r"$\left(ABCD\right)$.")
        giai_b = (r"Góc cần tìm là $\widehat{SBA}$." +
                  "\\\\\n"
                  r"Tam giác $SAB$ vuông tại $A$ với $SA = AB = %d$ nên "
                  r"nó vuông cân." % a +
                  "\\\\\n"
                  r"$\tan\widehat{SBA} = \dfrac{SA}{AB} = 1$, suy ra "
                  r"$\widehat{SBA} = 45^{\circ}$.")

        hoi_c = (r"Tính góc giữa $SC$ và mặt phẳng "
                 r"$\left(ABCD\right)$.")
        giai_c = (r"Hình chiếu của $SC$ trên $\left(ABCD\right)$ là "
                  r"$AC$, nên góc cần tìm là $\widehat{SCA}$." +
                  "\\\\\n"
                  r"$AC$ là đường chéo hình vuông cạnh $%d$ nên "
                  r"$AC = %d\sqrt{2}$." % (a, a) +
                  "\\\\\n"
                  r"$\tan\widehat{SCA} = \dfrac{SA}{AC} = "
                  r"\dfrac{%d}{%d\sqrt{2}} = \dfrac{\sqrt{2}}{2}$."
                  % (a, a) +
                  "\\\\\n"
                  r"Suy ra $\widehat{SCA} \approx 35^{\circ}16'$ (góc "
                  r"này không phải góc đặc biệt).")

        ds_abcd = [(hoi_a, r"AB", giai_a),
                   (hoi_b, r"45^{\circ}", giai_b),
                   (hoi_c, r"\tan\widehat{SCA} = \dfrac{\sqrt{2}}{2}",
                    giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B25_NB117_MC_A_01(socau, dang=1):
    r"""Nhận biết góc nhị diện, góc phẳng nhị diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Góc nhị diện là hình gồm",
         r"hai nửa mặt phẳng có chung bờ",
         [r"hai mặt phẳng song song", r"hai đường thẳng cắt nhau",
          r"một mặt phẳng và một đường thẳng"],
         r"Bờ chung đó gọi là CẠNH của góc nhị diện, hai nửa mặt phẳng "
         r"là hai MẶT của nó."),
        (r"Góc phẳng nhị diện của một góc nhị diện được dựng như thế "
         r"nào?",
         r"Từ một điểm trên cạnh, dựng trong mỗi mặt một tia vuông góc "
         r"với cạnh",
         [r"Dựng hai tia bất kì trong hai mặt",
          r"Dựng hai tia song song với cạnh",
          r"Dựng hai tia vuông góc với hai mặt"],
         r"Số đo góc phẳng nhị diện không phụ thuộc vào vị trí điểm "
         r"chọn trên cạnh; đó chính là số đo của góc nhị diện."),
        (r"Số đo góc nhị diện nhận giá trị trong khoảng nào?",
         r"$\left[0^{\circ};\ 180^{\circ}\right]$",
         [r"$\left[0^{\circ};\ 90^{\circ}\right]$",
          r"$\left(0^{\circ};\ 90^{\circ}\right)$",
          r"$\left[90^{\circ};\ 180^{\circ}\right]$"],
         r"Khác với góc giữa hai mặt phẳng (luôn không quá "
         r"$90^{\circ}$), góc NHỊ DIỆN có thể là góc tù, nhận giá trị "
         r"tới $180^{\circ}$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B25_TH114_MC_A_01(socau, dang=1):
    r"""Điều kiện để hai mặt phẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Điều kiện nào sau đây ĐỦ để kết luận "
         r"$\left(P\right) \perp \left(Q\right)$?",
         r"$\left(P\right)$ chứa một đường thẳng vuông góc với "
         r"$\left(Q\right)$",
         [r"$\left(P\right)$ chứa một đường thẳng song song với "
          r"$\left(Q\right)$",
          r"$\left(P\right)$ cắt $\left(Q\right)$",
          r"$\left(P\right)$ chứa một đường thẳng vuông góc với giao "
          r"tuyến"],
         r"Đây là điều kiện đủ quan trọng nhất của bài này." +
         "\\\\\n" +
         r"Chú ý ``vuông góc với giao tuyến'' là CHƯA ĐỦ, vì đường "
         r"thẳng đó có thể không vuông góc với $\left(Q\right)$."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$ và đáy "
         r"$ABCD$ là hình vuông. Cặp mặt phẳng nào sau đây vuông góc với "
         r"nhau?",
         r"$\left(SAB\right)$ và $\left(SBC\right)$",
         [r"$\left(SAB\right)$ và $\left(SAD\right)$ không vuông góc",
          r"$\left(SBC\right)$ và $\left(SCD\right)$",
          r"$\left(SAC\right)$ và $\left(SAB\right)$"],
         r"$BC \perp \left(SAB\right)$ (đã chứng minh ở bài trước) mà "
         r"$BC \subset \left(SBC\right)$." + "\\\\\n" +
         r"Theo điều kiện đủ, "
         r"$\left(SBC\right) \perp \left(SAB\right)$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_vuong() if "hình chóp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C7_B25_TH115_MC_A_01(socau, dang=1):
    r"""Tính chất cơ bản về hai mặt phẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho $\left(P\right) \perp \left(Q\right)$ và $a$ nằm trong "
         r"$\left(P\right)$, vuông góc với giao tuyến của hai mặt "
         r"phẳng. Khi đó",
         r"$a \perp \left(Q\right)$",
         [r"$a \parallel \left(Q\right)$",
          r"$a \subset \left(Q\right)$",
          r"$a$ cắt $\left(Q\right)$ nhưng không vuông góc"],
         r"Đây là tính chất dùng nhiều nhất khi dựng đường cao và tính "
         r"khoảng cách: trong mặt phẳng vuông góc, đường vuông góc với "
         r"giao tuyến thì vuông góc với mặt phẳng kia."),
        (r"Cho hai mặt phẳng $\left(P\right)$ và $\left(Q\right)$ cùng "
         r"vuông góc với mặt phẳng $\left(R\right)$ và cắt nhau theo "
         r"giao tuyến $d$. Khi đó",
         r"$d \perp \left(R\right)$",
         [r"$d \parallel \left(R\right)$",
          r"$d \subset \left(R\right)$",
          r"$d$ cắt $\left(R\right)$ nhưng không vuông góc"],
         r"Giao tuyến của hai mặt phẳng cùng vuông góc với một mặt "
         r"phẳng thứ ba thì vuông góc với mặt phẳng ấy."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B25_TH116_MC_A_01(socau, dang=1):
    r"""Tính chất của hình lăng trụ đứng, lăng trụ đều, hình hộp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hình lăng trụ ĐỨNG là hình lăng trụ có",
         r"cạnh bên vuông góc với mặt đáy",
         [r"đáy là đa giác đều", r"tất cả các mặt là hình chữ nhật",
          r"cạnh bên bằng cạnh đáy"],
         r"Khi cạnh bên vuông góc với đáy thì mọi mặt bên đều là hình "
         r"CHỮ NHẬT; nếu thêm điều kiện đáy là đa giác ĐỀU thì được "
         r"lăng trụ ĐỀU."),
        (r"Hình lăng trụ ĐỀU là hình lăng trụ",
         r"đứng và có đáy là đa giác đều",
         [r"có đáy là đa giác đều", r"có tất cả các cạnh bằng nhau",
          r"đứng và có đáy là hình vuông"],
         r"Cần CẢ HAI điều kiện: đứng (cạnh bên vuông góc đáy) và đáy "
         r"là đa giác đều."),
        (r"Hình hộp CHỮ NHẬT là hình hộp có",
         r"sáu mặt đều là hình chữ nhật",
         [r"sáu mặt đều là hình vuông", r"đáy là hình chữ nhật",
          r"bốn mặt bên là hình chữ nhật"],
         r"Hình hộp chữ nhật có cả sáu mặt là hình chữ nhật; nếu cả sáu "
         r"mặt là hình VUÔNG thì đó là hình LẬP PHƯƠNG."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B25_TH118_MC_A_01(socau, dang=1):
    r"""Xác định và tính số đo góc nhị diện, góc phẳng nhị diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
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
            sa, tan = "%d" % a, "1"
        elif kieu == "60":
            sa, tan = r"%d\sqrt{3}" % a, r"\sqrt{3}"
        else:
            sa, tan = r"\dfrac{%d\sqrt{3}}{3}" % a, r"\dfrac{\sqrt{3}}{3}"
        dung = r"$%s^{\circ}$" % kieu
        nhieu = _ba_nhieu7c(dung, [r"$30^{\circ}$", r"$45^{\circ}$",
                                   r"$60^{\circ}$", r"$90^{\circ}$"],
                            buoc=lambda t: r"$%d^{\circ}$" % (10 * t))
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %s$. Tính số đo góc nhị diện "
                 r"$\left[S, BC, A\right]$." % (a, sa))
        giai = (r"Cạnh của góc nhị diện là $BC$." +
                "\\\\\n"
                r"Ta có $BC \perp AB$ (hình vuông) và $BC \perp SA$ "
                r"(vì $SA \perp \left(ABCD\right)$), nên "
                r"$BC \perp \left(SAB\right)$, suy ra $BC \perp SB$." +
                "\\\\\n"
                r"Tại điểm $B$ trên cạnh $BC$: $BA$ nằm trong "
                r"$\left(ABCD\right)$ và vuông góc $BC$; $BS$ nằm trong "
                r"$\left(SBC\right)$ và vuông góc $BC$." +
                "\\\\\n"
                r"Vậy góc phẳng nhị diện là $\widehat{SBA}$." +
                "\\\\\n"
                r"$\tan\widehat{SBA} = \dfrac{SA}{AB} = "
                r"\dfrac{%s}{%d} = %s$, suy ra "
                r"$\widehat{SBA} = %s^{\circ}$." % (sa, a, tan, kieu))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_chop_vuong(), 0, dang)
    return cauTN


def L11_C7_B25_TH118_TL_A_01(socau, dong=1):
    r"""Tự luận: chứng minh hai mặt phẳng vuông góc.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, a))

        hoi_a = (r"Chứng minh "
                 r"$\left(SAB\right) \perp \left(ABCD\right)$.")
        giai_a = (r"$SA \perp \left(ABCD\right)$ theo giả thiết." +
                  "\\\\\n"
                  r"$SA \subset \left(SAB\right)$." +
                  "\\\\\n"
                  r"Mặt phẳng $\left(SAB\right)$ chứa một đường thẳng "
                  r"vuông góc với $\left(ABCD\right)$ nên "
                  r"$\left(SAB\right) \perp \left(ABCD\right)$.")

        hoi_b = (r"Chứng minh "
                 r"$\left(SBC\right) \perp \left(SAB\right)$.")
        giai_b = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp BC$." +
                  "\\\\\n"
                  r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                  "\\\\\n"
                  r"$SA$ và $AB$ cắt nhau tại $A$ nên "
                  r"$BC \perp \left(SAB\right)$." +
                  "\\\\\n"
                  r"$BC \subset \left(SBC\right)$ nên "
                  r"$\left(SBC\right) \perp \left(SAB\right)$.")

        hoi_c = r"Tính số đo góc nhị diện $\left[S, BC, A\right]$."
        giai_c = (r"Theo câu b, $BC \perp \left(SAB\right)$ nên "
                  r"$BC \perp SB$ và $BC \perp AB$." +
                  "\\\\\n"
                  r"Vậy góc phẳng nhị diện là $\widehat{SBA}$." +
                  "\\\\\n"
                  r"Tam giác $SAB$ vuông tại $A$ với $SA = AB = %d$ nên "
                  r"vuông cân, do đó "
                  r"$\widehat{SBA} = 45^{\circ}$." % a)

        ds_abcd = [(hoi_a,
                    r"\left(SAB\right) \perp \left(ABCD\right)", giai_a),
                   (hoi_b,
                    r"\left(SBC\right) \perp \left(SAB\right)", giai_b),
                   (hoi_c, r"45^{\circ}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B25_VD119_MC_A_01(socau, dang=1):
    r"""Vận dụng góc giữa đường thẳng và mặt phẳng, góc nhị diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa đường thẳng "
         r"$AC'$ và mặt phẳng $\left(ABCD\right)$ có $\tan$ bằng",
         r"$\dfrac{\sqrt{2}}{2}$",
         [r"$1$", r"$\sqrt{2}$", r"$\sqrt{3}$"],
         r"Hình chiếu của $C'$ trên $\left(ABCD\right)$ là $C$, nên góc "
         r"cần tìm là $\widehat{C'AC}$." + "\\\\\n" +
         r"Với cạnh $a$: $CC' = a$ và $AC = a\sqrt{2}$." + "\\\\\n" +
         r"$\tan\widehat{C'AC} = \dfrac{CC'}{AC} = "
         r"\dfrac{a}{a\sqrt{2}} = \dfrac{\sqrt{2}}{2}$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Góc giữa đường thẳng "
         r"$AB'$ và mặt phẳng $\left(ABCD\right)$ bằng",
         r"$45^{\circ}$", [r"$30^{\circ}$", r"$60^{\circ}$",
                           r"$90^{\circ}$"],
         r"Hình chiếu của $B'$ trên $\left(ABCD\right)$ là $B$, nên góc "
         r"cần tìm là $\widehat{B'AB}$." + "\\\\\n" +
         r"Tam giác $ABB'$ vuông cân tại $B$ (vì $AB = BB' = a$) nên "
         r"góc bằng $45^{\circ}$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$. Số đo góc nhị diện "
         r"$\left[A', BC, A\right]$ bằng",
         r"$45^{\circ}$", [r"$30^{\circ}$", r"$60^{\circ}$",
                           r"$90^{\circ}$"],
         r"$BC \perp AB$ và $BC \perp BB'$ nên "
         r"$BC \perp \left(ABB'A'\right)$, do đó $BC \perp BA'$." +
         "\\\\\n" +
         r"Góc phẳng nhị diện là $\widehat{A'BA}$." + "\\\\\n" +
         r"Tam giác $ABA'$ vuông cân tại $A$ nên góc bằng "
         r"$45^{\circ}$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do,
                                   _hinh_lap_phuong(), 0, dang)
    return cauTN


def L11_C7_B25_VD119_SA_A_01(socau):
    r"""Số đo góc trong hình lập phương - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"góc giữa đường thẳng $AB'$ và mặt phẳng "
         r"$\left(ABCD\right)$", 45,
         r"Hình chiếu của $B'$ trên $\left(ABCD\right)$ là $B$ nên góc "
         r"cần tìm là $\widehat{B'AB}$." + "\\\\\n" +
         r"Tam giác $ABB'$ vuông cân tại $B$ ($AB = BB'$) nên góc bằng "
         r"$45^{\circ}$."),
        (r"góc giữa đường thẳng $AA'$ và mặt phẳng "
         r"$\left(ABCD\right)$", 90,
         r"$AA' \perp \left(ABCD\right)$ (cạnh bên của hình lập phương "
         r"vuông góc với đáy)." + "\\\\\n" +
         r"Theo quy ước, góc bằng $90^{\circ}$."),
        (r"góc giữa đường thẳng $AB$ và mặt phẳng "
         r"$\left(A'B'C'D'\right)$", 0,
         r"$AB \parallel A'B' \subset \left(A'B'C'D'\right)$ nên "
         r"$AB \parallel \left(A'B'C'D'\right)$." + "\\\\\n" +
         r"Vậy góc bằng $0^{\circ}$."),
        (r"số đo góc nhị diện $\left[A', BC, A\right]$", 45,
         r"$BC \perp \left(ABB'A'\right)$ nên $BC \perp BA'$ và "
         r"$BC \perp BA$." + "\\\\\n" +
         r"Góc phẳng nhị diện là $\widehat{A'BA}$; tam giác $ABA'$ "
         r"vuông cân tại $A$ nên góc bằng $45^{\circ}$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cau = ""
    for i in gt:
        mo_ta, dap, giai = MAU[i]
        debai = (r"Cho hình lập phương $ABCD.A'B'C'D'$. Tính %s (đơn vị: "
                 r"độ)." % mo_ta)
        nhieu = _ba_nhieu7c(str(dap), ["90", "60", "45", "30", "0"],
                            buoc=lambda t: str(dap + 10 * t))
        cau += MC_SA_answer_const(debai, str(dap), nhieu, giai,
                                  _hinh_lap_phuong(), 0, 2)
    return cau


def L11_C7_B25_VD119_TL_A_01(socau, dong=1):
    r"""Tự luận: vận dụng góc giữa đường thẳng và mặt phẳng, góc nhị diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_lap_phuong()
        debai = r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $%d$." % a

        hoi_a = (r"Tính góc giữa đường thẳng $AB'$ và mặt phẳng "
                 r"$\left(ABCD\right)$.")
        giai_a = (r"$BB' \perp \left(ABCD\right)$ nên hình chiếu của "
                  r"$B'$ trên đáy là $B$." +
                  "\\\\\n"
                  r"Góc cần tìm là $\widehat{B'AB}$." +
                  "\\\\\n"
                  r"Tam giác $ABB'$ vuông tại $B$ với $AB = BB' = %d$ "
                  r"nên vuông cân, góc bằng $45^{\circ}$." % a)

        hoi_b = (r"Tính $\tan$ của góc giữa đường thẳng $AC'$ và mặt "
                 r"phẳng $\left(ABCD\right)$.")
        giai_b = (r"Hình chiếu của $C'$ trên đáy là $C$ nên góc cần tìm "
                  r"là $\widehat{C'AC}$." +
                  "\\\\\n"
                  r"$AC = %d\sqrt{2}$ (đường chéo hình vuông) và "
                  r"$CC' = %d$." % (a, a) +
                  "\\\\\n"
                  r"$\tan\widehat{C'AC} = \dfrac{CC'}{AC} = "
                  r"\dfrac{%d}{%d\sqrt{2}} = \dfrac{\sqrt{2}}{2}$."
                  % (a, a))

        hoi_c = r"Tính số đo góc nhị diện $\left[A', BC, A\right]$."
        giai_c = (r"$BC \perp AB$ và $BC \perp BB'$ nên "
                  r"$BC \perp \left(ABB'A'\right)$, suy ra "
                  r"$BC \perp BA'$." +
                  "\\\\\n"
                  r"Vậy góc phẳng nhị diện là $\widehat{A'BA}$." +
                  "\\\\\n"
                  r"Tam giác $ABA'$ vuông tại $A$ với $AB = AA' = %d$ "
                  r"nên vuông cân, góc bằng $45^{\circ}$." % a)

        ds_abcd = [(hoi_a, r"45^{\circ}", giai_a),
                   (hoi_b, r"\dfrac{\sqrt{2}}{2}", giai_b),
                   (hoi_c, r"45^{\circ}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 26. KHOẢNG CÁCH TRONG KHÔNG GIAN
# =====================================================================

def L11_C7_B26_TH120_MC_A_01(socau, dang=1):
    r"""Khoảng cách từ một điểm đến một đường thẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(PYTAGO7C)
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cauTN = ""
    for a, h, c in gt:
        dung = "$%d$" % h
        nhieu = _ba_nhieu7c(dung, ["$%d$" % a, "$%d$" % c,
                                   "$%d$" % (a + h)],
                            buoc=lambda t: "$%d$" % (h + t))
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$. Tính khoảng cách từ điểm $S$ đến đường "
                 r"thẳng $AB$." % (a, h))
        giai = (r"$SA \perp \left(ABCD\right)$ mà "
                r"$AB \subset \left(ABCD\right)$ nên $SA \perp AB$." +
                "\\\\\n"
                r"Vậy $A$ chính là hình chiếu vuông góc của $S$ trên "
                r"đường thẳng $AB$." +
                "\\\\\n"
                r"$d\left(S, AB\right) = SA = %d$." % h)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_chop_vuong(), 0, dang)
    return cauTN


def L11_C7_B26_TH120_SA_A_01(socau):
    r"""Số đo góc nhị diện - trả lời ngắn (đáp số NGUYÊN).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        kieu = random.choice(["45", "60", "30"])
        if (a, kieu) not in gt:
            gt.append((a, kieu))

    cau = ""
    for a, kieu in gt:
        if kieu == "45":
            sa, tan = "%d" % a, "1"
        elif kieu == "60":
            sa, tan = r"%d\sqrt{3}" % a, r"\sqrt{3}"
        else:
            sa, tan = r"\dfrac{%d\sqrt{3}}{3}" % a, r"\dfrac{\sqrt{3}}{3}"
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %s$. Tính số đo góc nhị diện "
                 r"$\left[S, AB, C\right]$ (đơn vị: độ)." % (a, sa))
        giai = (r"Cạnh của góc nhị diện là $AB$." +
                "\\\\\n"
                r"Tại $A$: $AS \perp AB$ (vì "
                r"$SA \perp \left(ABCD\right)$) và $AD \perp AB$ (hình "
                r"vuông)." +
                "\\\\\n"
                r"Vậy góc phẳng nhị diện là $\widehat{SAD}$." +
                "\\\\\n"
                r"Vì $SA \perp \left(ABCD\right)$ nên $SA \perp AD$, "
                r"do đó $\widehat{SAD} = 90^{\circ}$." +
                "\\\\\n"
                r"Số đo góc nhị diện $\left[S, AB, C\right]$ bằng "
                r"$90^{\circ}$ (không phụ thuộc độ dài $SA$).")
        nhieu = _ba_nhieu7c("90", ["30", "45", "60", "0"],
                            buoc=lambda t: str(10 * t))
        cau += MC_SA_answer_const(debai, "90", nhieu, giai,
                                  _hinh_chop_vuong(), 0, 2)
    return cau


def L11_C7_B26_TH120_TL_A_01(socau, dong=1):
    r"""Tự luận: xác định và tính góc phẳng nhị diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, a))

        hoi_a = (r"Xác định góc phẳng nhị diện của góc nhị diện "
                 r"$\left[S, BC, A\right]$.")
        giai_a = (r"Cạnh của góc nhị diện là $BC$." +
                  "\\\\\n"
                  r"$BC \perp AB$ (hình vuông) và $BC \perp SA$ (vì "
                  r"$SA \perp \left(ABCD\right)$) nên "
                  r"$BC \perp \left(SAB\right)$, suy ra $BC \perp SB$." +
                  "\\\\\n"
                  r"Tại $B$: $BA$ vuông góc $BC$ và nằm trong "
                  r"$\left(ABCD\right)$; $BS$ vuông góc $BC$ và nằm "
                  r"trong $\left(SBC\right)$." +
                  "\\\\\n"
                  r"Vậy góc phẳng nhị diện là $\widehat{SBA}$.")

        hoi_b = r"Tính số đo góc nhị diện đó."
        giai_b = (r"Tam giác $SAB$ vuông tại $A$ với $SA = AB = %d$." % a +
                  "\\\\\n"
                  r"$\tan\widehat{SBA} = \dfrac{SA}{AB} = 1$." +
                  "\\\\\n"
                  r"Vậy $\widehat{SBA} = 45^{\circ}$.")

        hoi_c = r"Tính số đo góc nhị diện $\left[S, AB, C\right]$."
        giai_c = (r"Cạnh là $AB$; tại $A$ có $AS \perp AB$ và "
                  r"$AD \perp AB$." +
                  "\\\\\n"
                  r"Góc phẳng nhị diện là $\widehat{SAD}$." +
                  "\\\\\n"
                  r"Vì $SA \perp \left(ABCD\right)$ nên $SA \perp AD$, "
                  r"do đó $\widehat{SAD} = 90^{\circ}$.")

        ds_abcd = [(hoi_a, r"\widehat{SBA}", giai_a),
                   (hoi_b, r"45^{\circ}", giai_b),
                   (hoi_c, r"90^{\circ}", giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B26_TH121_MC_A_01(socau, dang=1):
    r"""Khoảng cách giữa hai đường thẳng song song.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        dung = "$%d$" % a
        nhieu = _ba_nhieu7c(dung, [r"$%d\sqrt{2}$" % a, "$%d$" % (2 * a),
                                   "$0$"],
                            buoc=lambda t: "$%d$" % (a + t))
        debai = (r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $%d$. Tính "
                 r"khoảng cách giữa hai đường thẳng song song $AB$ và "
                 r"$C'D'$." % a)
        giai = (r"$AB \parallel CD \parallel C'D'$ nên hai đường thẳng "
                r"$AB$ và $C'D'$ song song." +
                "\\\\\n"
                r"Khoảng cách giữa hai đường thẳng song song là khoảng "
                r"cách từ một điểm của đường này đến đường kia." +
                "\\\\\n"
                r"Xét đoạn $DD'$: ta có $DD' \perp CD$ và "
                r"$DD' \perp C'D'$ (các mặt bên là hình vuông)." +
                "\\\\\n"
                r"Mà $AB \parallel CD$ nên $DD'$ cũng vuông góc với "
                r"phương của $AB$." +
                "\\\\\n"
                r"Vậy $DD'$ là đoạn vuông góc chung, khoảng cách cần "
                r"tìm bằng $DD' = %d$." % a)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_lap_phuong(), 0, dang)
    return cauTN


def L11_C7_B26_TH122_MC_A_01(socau, dang=1):
    r"""Đường vuông góc chung của hai đường thẳng chéo nhau.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Đường vuông góc chung của hai đường thẳng chéo nhau $a$ và "
         r"$b$ là đường thẳng",
         r"cắt cả $a$ và $b$, đồng thời vuông góc với cả hai",
         [r"vuông góc với cả $a$ và $b$",
          r"cắt cả $a$ và $b$",
          r"song song với cả $a$ và $b$"],
         r"Cần CẢ HAI điều kiện: vừa CẮT vừa VUÔNG GÓC với hai đường "
         r"thẳng đó." + "\\\\\n" +
         r"Hai đường thẳng chéo nhau có DUY NHẤT một đường vuông góc "
         r"chung."),
        (r"Khoảng cách giữa hai đường thẳng chéo nhau bằng",
         r"độ dài đoạn vuông góc chung",
         [r"khoảng cách từ một điểm bất kì của đường này đến đường kia",
          r"độ dài đoạn thẳng nối hai điểm bất kì",
          r"luôn bằng $0$"],
         r"Đoạn vuông góc chung là đoạn ngắn nhất nối hai đường thẳng "
         r"chéo nhau, nên độ dài của nó chính là khoảng cách."),
        (r"Cho hình chóp $S.ABCD$ có $SA \perp \left(ABCD\right)$, đáy "
         r"$ABCD$ là hình vuông. Đường vuông góc chung của $SA$ và $BC$ "
         r"là",
         r"$AB$", [r"$AC$", r"$SB$", r"$CD$"],
         r"$SA \perp AB$ (vì $SA \perp \left(ABCD\right)$) và "
         r"$AB \perp BC$ (hình vuông)." + "\\\\\n" +
         r"$AB$ cắt $SA$ tại $A$ và cắt $BC$ tại $B$." + "\\\\\n" +
         r"Vậy $AB$ là đường vuông góc chung của $SA$ và $BC$."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        hinh = _hinh_chop_vuong() if "hình chóp" in hoi else 0
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, hinh, 0,
                                   dang)
    return cauTN


def L11_C7_B26_TH122_SA_A_01(socau):
    r"""Khoảng cách từ một điểm đến một mặt phẳng - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.

    Dùng bộ ba Pytago nên $d = \dfrac{SA\cdot AB}{SB}$ luôn là số thập
    phân hữu hạn.
    """
    # chi lay bo ba cho AH = h.a/c la so thap phan HUU HAN
    BO = [b for b in PYTAGO7C
          if (Fraction(b[1] * b[0], b[2]) * 100).denominator == 1]
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(BO)
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cau = ""
    for a, h, c in gt:
        d = Fraction(h * a, c)
        dapso = _xx(d)
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$. Tính khoảng cách từ điểm $A$ đến mặt phẳng "
                 r"$\left(SBC\right)$." % (a, h))
        giai = (r"Ta có $BC \perp AB$ và $BC \perp SA$ nên "
                r"$BC \perp \left(SAB\right)$." +
                "\\\\\n"
                r"Kẻ $AH \perp SB$ tại $H$ (trong mặt phẳng "
                r"$\left(SAB\right)$)." +
                "\\\\\n"
                r"Vì $BC \perp \left(SAB\right)$ nên $BC \perp AH$; kết "
                r"hợp $AH \perp SB$ ta được "
                r"$AH \perp \left(SBC\right)$." +
                "\\\\\n"
                r"Vậy $d\left(A, \left(SBC\right)\right) = AH$." +
                "\\\\\n"
                r"Tam giác $SAB$ vuông tại $A$: "
                r"$SB = \sqrt{%d^{2} + %d^{2}} = %d$." % (h, a, c) +
                "\\\\\n"
                r"Hệ thức lượng: $AH = \dfrac{SA\cdot AB}{SB} = "
                r"\dfrac{%d\cdot %d}{%d} = %s$." % (h, a, c, dapso))
        nhieu = _ba_nhieu7c(dapso, [str(a), str(h), str(c)],
                            buoc=lambda t: _xx(float(d) + t))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai,
                                  _hinh_chop_vuong(), 0, 2)
    return cau


def L11_C7_B26_TH122_TL_A_01(socau, dong=1):
    r"""Tự luận: tính khoảng cách từ điểm đến mặt phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO = [b for b in PYTAGO7C
          if (Fraction(b[1] * b[0], b[2]) * 100).denominator == 1]
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(BO)
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cauTN = ""
    for a, h, c in gt:
        d = Fraction(h * a, c)
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, h))

        hoi_a = r"Chứng minh $BC \perp \left(SAB\right)$."
        giai_a = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp BC$." +
                  "\\\\\n"
                  r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                  "\\\\\n"
                  r"$SA$ và $AB$ cắt nhau tại $A$ nên "
                  r"$BC \perp \left(SAB\right)$.")

        hoi_b = (r"Gọi $H$ là hình chiếu vuông góc của $A$ trên $SB$. "
                 r"Chứng minh $AH \perp \left(SBC\right)$.")
        giai_b = (r"Theo câu a, $BC \perp \left(SAB\right)$ mà "
                  r"$AH \subset \left(SAB\right)$ nên $BC \perp AH$." +
                  "\\\\\n"
                  r"Lại có $AH \perp SB$ theo cách dựng." +
                  "\\\\\n"
                  r"$SB$ và $BC$ cắt nhau tại $B$, cùng nằm trong "
                  r"$\left(SBC\right)$, nên "
                  r"$AH \perp \left(SBC\right)$.")

        hoi_c = (r"Tính khoảng cách từ $A$ đến mặt phẳng "
                 r"$\left(SBC\right)$.")
        giai_c = (r"Theo câu b, "
                  r"$d\left(A, \left(SBC\right)\right) = AH$." +
                  "\\\\\n"
                  r"Tam giác $SAB$ vuông tại $A$ nên "
                  r"$SB = \sqrt{SA^{2} + AB^{2}} = "
                  r"\sqrt{%d^{2} + %d^{2}} = %d$." % (h, a, c) +
                  "\\\\\n"
                  r"Hệ thức lượng trong tam giác vuông: "
                  r"$AH\cdot SB = SA\cdot AB$." +
                  "\\\\\n"
                  r"$AH = \dfrac{%d\cdot %d}{%d} = %s$."
                  % (h, a, c, _xx(d)))

        ds_abcd = [(hoi_a, r"BC \perp \left(SAB\right)", giai_a),
                   (hoi_b, r"AH \perp \left(SBC\right)", giai_b),
                   (hoi_c, r"d = %s" % _xx(d), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B26_VD123_MC_A_01(socau, dang=1):
    r"""Khoảng cách giữa hai đường thẳng chéo nhau.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10])
        h = random.choice([2, 3, 4, 5, 6, 8, 10])
        if (a, h) not in gt:
            gt.append((a, h))

    cauTN = ""
    for a, h in gt:
        dung = "$%d$" % a
        nhieu = _ba_nhieu7c(dung, ["$%d$" % h, r"$%d\sqrt{2}$" % a,
                                   "$0$"],
                            buoc=lambda t: "$%d$" % (a + t))
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$. Tính khoảng cách giữa hai đường thẳng "
                 r"chéo nhau $SA$ và $BC$." % (a, h))
        giai = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp AB$." +
                "\\\\\n"
                r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                "\\\\\n"
                r"$AB$ cắt $SA$ tại $A$ và cắt $BC$ tại $B$, đồng thời "
                r"vuông góc với cả hai." +
                "\\\\\n"
                r"Vậy $AB$ là đoạn vuông góc chung, và "
                r"$d\left(SA, BC\right) = AB = %d$." % a +
                "\\\\\n"
                r"Chú ý khoảng cách này KHÔNG phụ thuộc vào $SA$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_chop_vuong(), 0, dang)
    return cauTN


def L11_C7_B26_VD123_SA_A_01(socau):
    r"""Khoảng cách giữa hai đường thẳng chéo nhau - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10])
        h = random.choice([2, 3, 4, 5, 6, 8, 10])
        if (a, h) not in gt:
            gt.append((a, h))

    cau = ""
    for a, h in gt:
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$. Tính khoảng cách giữa hai đường thẳng "
                 r"$SA$ và $CD$." % (a, h))
        giai = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp AD$." +
                "\\\\\n"
                r"$ABCD$ là hình vuông nên $AD \perp CD$." +
                "\\\\\n"
                r"$AD$ cắt $SA$ tại $A$, cắt $CD$ tại $D$ và vuông góc "
                r"với cả hai nên $AD$ là đoạn vuông góc chung." +
                "\\\\\n"
                r"$d\left(SA, CD\right) = AD = %d$." % a)
        nhieu = _ba_nhieu7c(str(a), [str(h), str(a + h), "0"],
                            buoc=lambda t: str(a + t))
        cau += MC_SA_answer_const(debai, str(a), nhieu, giai,
                                  _hinh_chop_vuong(), 0, 2)
    return cau


def L11_C7_B26_VD123_TL_A_01(socau, dong=1):
    r"""Tự luận: khoảng cách giữa hai đường thẳng chéo nhau.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        if a not in gt:
            gt.append(a)

    cauTN = ""
    for a in gt:
        hinh = _hinh_lap_phuong()
        debai = r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $%d$." % a

        hoi_a = r"Chứng minh $AB$ và $CC'$ chéo nhau."
        giai_a = (r"Nếu $AB$ và $CC'$ đồng phẳng thì bốn điểm $A$, $B$, "
                  r"$C$, $C'$ cùng thuộc một mặt phẳng." +
                  "\\\\\n"
                  r"Nhưng $C'$ không thuộc mặt phẳng "
                  r"$\left(ABC\right) = \left(ABCD\right)$." +
                  "\\\\\n"
                  r"Vậy $AB$ và $CC'$ chéo nhau.")

        hoi_b = r"Xác định đoạn vuông góc chung của $AB$ và $CC'$."
        giai_b = (r"$BC \perp AB$ (hình vuông $ABCD$)." +
                  "\\\\\n"
                  r"$CC' \perp \left(ABCD\right)$ nên $CC' \perp BC$." +
                  "\\\\\n"
                  r"$BC$ cắt $AB$ tại $B$, cắt $CC'$ tại $C$ và vuông "
                  r"góc với cả hai, nên $BC$ là đoạn vuông góc chung.")

        hoi_c = r"Tính khoảng cách giữa $AB$ và $CC'$."
        giai_c = (r"Khoảng cách giữa hai đường thẳng chéo nhau bằng độ "
                  r"dài đoạn vuông góc chung." +
                  "\\\\\n"
                  r"$d\left(AB, CC'\right) = BC = %d$." % a)

        ds_abcd = [(hoi_a, r"AB \text{ và } CC' \text{ chéo nhau}",
                    giai_a),
                   (hoi_b, r"BC", giai_b),
                   (hoi_c, r"d = %d" % a, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B26_VD124_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về khoảng cách trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $a$. Khoảng cách từ "
         r"điểm $A$ đến mặt phẳng $\left(A'B'C'D'\right)$ bằng",
         r"$a$", [r"$a\sqrt{2}$", r"$a\sqrt{3}$", r"$\dfrac{a}{2}$"],
         r"$AA' \perp \left(A'B'C'D'\right)$ nên $A'$ là hình chiếu "
         r"vuông góc của $A$ trên mặt phẳng đó." + "\\\\\n" +
         r"Vậy khoảng cách bằng $AA' = a$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $a$. Khoảng cách "
         r"giữa hai mặt phẳng song song $\left(ABCD\right)$ và "
         r"$\left(A'B'C'D'\right)$ bằng",
         r"$a$", [r"$a\sqrt{2}$", r"$a\sqrt{3}$", r"$2a$"],
         r"Khoảng cách giữa hai mặt phẳng song song là khoảng cách từ "
         r"một điểm của mặt này đến mặt kia." + "\\\\\n" +
         r"Lấy điểm $A$: khoảng cách bằng $AA' = a$."),
        (r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $a$. Khoảng cách từ "
         r"điểm $A$ đến đường thẳng $CC'$ bằng",
         r"$a\sqrt{2}$", [r"$a$", r"$a\sqrt{3}$", r"$\dfrac{a}{2}$"],
         r"$CC' \perp \left(ABCD\right)$ nên $CC' \perp AC$." +
         "\\\\\n" +
         r"Vậy $C$ là hình chiếu vuông góc của $A$ trên $CC'$, khoảng "
         r"cách bằng $AC = a\sqrt{2}$ (đường chéo hình vuông)."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do,
                                   _hinh_lap_phuong(), 0, dang)
    return cauTN


def L11_C7_B26_VD124_SA_A_01(socau):
    r"""Khoảng cách trong hình lập phương - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"khoảng cách từ điểm $A$ đến mặt phẳng "
         r"$\left(A'B'C'D'\right)$", 1,
         r"$AA' \perp \left(A'B'C'D'\right)$ nên khoảng cách bằng "
         r"$AA'$, tức bằng độ dài cạnh."),
        (r"khoảng cách giữa hai đường thẳng $AB$ và $CC'$", 1,
         r"$BC$ vuông góc với cả $AB$ và $CC'$, đồng thời cắt cả hai, "
         r"nên là đoạn vuông góc chung." + "\\\\\n" +
         r"Khoảng cách bằng $BC$, tức bằng độ dài cạnh."),
        (r"khoảng cách giữa hai mặt phẳng $\left(ABCD\right)$ và "
         r"$\left(A'B'C'D'\right)$", 1,
         r"Hai mặt phẳng song song; lấy điểm $A$ thì khoảng cách bằng "
         r"$AA'$, tức bằng độ dài cạnh."),
        (r"khoảng cách từ điểm $B$ đến đường thẳng $AD$", 1,
         r"$AB \perp AD$ (hình vuông $ABCD$) nên $A$ là hình chiếu "
         r"vuông góc của $B$ trên $AD$." + "\\\\\n" +
         r"Khoảng cách bằng $AB$, tức bằng độ dài cạnh."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)
    canh = [random.choice([2, 3, 4, 5, 6, 8, 10]) for _ in range(socau)]

    cau = ""
    for i, a in zip(gt, canh):
        mo_ta, he_so, giai = MAU[i]
        kq = he_so * a
        debai = (r"Cho hình lập phương $ABCD.A'B'C'D'$ cạnh $%d$. Tính "
                 r"%s." % (a, mo_ta))
        giai_du = giai + "\\\\\n" + r"Vậy khoảng cách bằng $%d$." % kq
        nhieu = _ba_nhieu7c(str(kq), [str(2 * a), str(a + 1), "0"],
                            buoc=lambda t: str(kq + t + 1))
        cau += MC_SA_answer_const(debai, str(kq), nhieu, giai_du,
                                  _hinh_lap_phuong(), 0, 2)
    return cau


def L11_C7_B26_VD124_TL_A_01(socau, dong=1):
    r"""Tự luận: tổng hợp về khoảng cách trong không gian.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(
            [b for b in PYTAGO7C
             if (Fraction(b[1] * b[0], b[2]) * 100).denominator == 1])
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cauTN = ""
    for a, h, c in gt:
        d = Fraction(h * a, c)
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, h))

        hoi_a = (r"Tính khoảng cách từ điểm $S$ đến mặt phẳng "
                 r"$\left(ABCD\right)$.")
        giai_a = (r"$SA \perp \left(ABCD\right)$ nên $A$ là hình chiếu "
                  r"vuông góc của $S$ trên mặt đáy." +
                  "\\\\\n"
                  r"$d\left(S, \left(ABCD\right)\right) = SA = %d$." % h)

        hoi_b = r"Tính khoảng cách giữa hai đường thẳng $SA$ và $BC$."
        giai_b = (r"$SA \perp AB$ và $AB \perp BC$." +
                  "\\\\\n"
                  r"$AB$ cắt $SA$ tại $A$, cắt $BC$ tại $B$ nên $AB$ là "
                  r"đoạn vuông góc chung." +
                  "\\\\\n"
                  r"$d\left(SA, BC\right) = AB = %d$." % a)

        hoi_c = (r"Tính khoảng cách từ điểm $A$ đến mặt phẳng "
                 r"$\left(SBC\right)$.")
        giai_c = (r"$BC \perp AB$ và $BC \perp SA$ nên "
                  r"$BC \perp \left(SAB\right)$." +
                  "\\\\\n"
                  r"Kẻ $AH \perp SB$ tại $H$ thì $AH \perp BC$, do đó "
                  r"$AH \perp \left(SBC\right)$." +
                  "\\\\\n"
                  r"$SB = \sqrt{%d^{2} + %d^{2}} = %d$." % (h, a, c) +
                  "\\\\\n"
                  r"$AH = \dfrac{SA\cdot AB}{SB} = "
                  r"\dfrac{%d\cdot %d}{%d} = %s$." % (h, a, c, _xx(d)))

        ds_abcd = [(hoi_a, r"SA = %d" % h, giai_a),
                   (hoi_b, r"AB = %d" % a, giai_b),
                   (hoi_c, r"AH = %s" % _xx(d), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# BÀI 27. THỂ TÍCH
# =====================================================================

def L11_C7_B27_NB125_MC_A_01(socau, dang=1):
    r"""Công thức tính thể tích khối chóp, khối lăng trụ.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Thể tích của khối chóp có diện tích đáy $S$ và chiều cao $h$ "
         r"được tính bởi công thức nào?",
         r"$V = \dfrac{1}{3}Sh$",
         [r"$V = Sh$", r"$V = \dfrac{1}{2}Sh$", r"$V = 3Sh$"],
         r"Khối chóp có thể tích bằng MỘT PHẦN BA tích của diện tích "
         r"đáy và chiều cao."),
        (r"Thể tích của khối lăng trụ có diện tích đáy $S$ và chiều cao "
         r"$h$ được tính bởi công thức nào?",
         r"$V = Sh$",
         [r"$V = \dfrac{1}{3}Sh$", r"$V = \dfrac{1}{2}Sh$",
          r"$V = 3Sh$"],
         r"Khối lăng trụ có thể tích bằng tích diện tích đáy và chiều "
         r"cao; khối chóp cùng đáy cùng chiều cao chỉ bằng "
         r"$\dfrac{1}{3}$ thể tích đó."),
        (r"Thể tích của khối hộp chữ nhật có ba kích thước $a$, $b$, "
         r"$c$ bằng",
         r"$abc$", [r"$\dfrac{1}{3}abc$", r"$2\left(ab + bc + ca\right)$",
                    r"$a + b + c$"],
         r"Hình hộp chữ nhật là một lăng trụ đứng có đáy là hình chữ "
         r"nhật diện tích $ab$ và chiều cao $c$, nên $V = abc$." +
         "\\\\\n" +
         r"Biểu thức $2\left(ab + bc + ca\right)$ là DIỆN TÍCH TOÀN "
         r"PHẦN, không phải thể tích."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B27_NB125_SA_A_01(socau):
    r"""Khoảng cách giữa hai đường thẳng chéo nhau - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6, 8, 10])
        h = random.choice([2, 3, 4, 5, 6, 8, 10])
        if (a, h) not in gt:
            gt.append((a, h))

    cau = ""
    for a, h in gt:
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$. Tính khoảng cách giữa hai đường thẳng "
                 r"chéo nhau $SA$ và $BC$." % (a, h))
        giai = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp AB$." +
                "\\\\\n"
                r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                "\\\\\n"
                r"$AB$ cắt $SA$ tại $A$, cắt $BC$ tại $B$ và vuông góc "
                r"với cả hai nên $AB$ là đoạn vuông góc chung." +
                "\\\\\n"
                r"$d\left(SA, BC\right) = AB = %d$." % a)
        nhieu = _ba_nhieu7c(str(a), [str(h), str(a + h), "0"],
                            buoc=lambda t: str(a + t))
        cau += MC_SA_answer_const(debai, str(a), nhieu, giai,
                                  _hinh_chop_vuong(), 0, 2)
    return cau


def L11_C7_B27_NB125_TL_A_01(socau, dong=1):
    r"""Tự luận: tính khoảng cách giữa hai đường thẳng chéo nhau.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 5, 6])
        h = random.choice([2, 3, 4, 5, 6])
        if (a, h) not in gt:
            gt.append((a, h))

    cauTN = ""
    for a, h in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, h))

        hoi_a = r"Chứng minh $SA$ và $BC$ chéo nhau."
        giai_a = (r"Nếu $SA$ và $BC$ đồng phẳng thì $S$ thuộc mặt phẳng "
                  r"chứa $A$ và $BC$, tức thuộc $\left(ABCD\right)$." +
                  "\\\\\n"
                  r"Điều đó trái với $SA \perp \left(ABCD\right)$ và "
                  r"$SA > 0$." +
                  "\\\\\n"
                  r"Vậy $SA$ và $BC$ chéo nhau.")

        hoi_b = r"Xác định đoạn vuông góc chung của $SA$ và $BC$."
        giai_b = (r"$SA \perp \left(ABCD\right)$ nên $SA \perp AB$." +
                  "\\\\\n"
                  r"$ABCD$ là hình vuông nên $AB \perp BC$." +
                  "\\\\\n"
                  r"$AB$ cắt $SA$ tại $A$ và cắt $BC$ tại $B$, đồng "
                  r"thời vuông góc với cả hai, nên $AB$ là đoạn vuông "
                  r"góc chung.")

        hoi_c = r"Tính khoảng cách giữa $SA$ và $BC$."
        giai_c = (r"Khoảng cách giữa hai đường thẳng chéo nhau bằng độ "
                  r"dài đoạn vuông góc chung." +
                  "\\\\\n"
                  r"$d\left(SA, BC\right) = AB = %d$." % a +
                  "\\\\\n"
                  r"Chú ý kết quả không phụ thuộc vào $SA = %d$." % h)

        ds_abcd = [(hoi_a, r"SA \text{ và } BC \text{ chéo nhau}",
                    giai_a),
                   (hoi_b, r"AB", giai_b),
                   (hoi_c, r"d = %d" % a, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B27_NB127_MC_A_01(socau, dang=1):
    r"""Nhận biết hình chóp cụt đều.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Hình chóp cụt đều được tạo thành như thế nào?",
         r"Cắt một hình chóp đều bởi một mặt phẳng song song với đáy và "
         r"bỏ đi phần chóp phía trên",
         [r"Cắt một hình chóp bất kì bởi một mặt phẳng bất kì",
          r"Ghép hai hình chóp đều lại với nhau",
          r"Cắt một hình lăng trụ đều bởi một mặt phẳng song song đáy"],
         r"Hai đáy của hình chóp cụt đều là hai đa giác ĐỀU ĐỒNG DẠNG "
         r"nằm trong hai mặt phẳng song song."),
        (r"Các mặt bên của hình chóp cụt đều là",
         r"các hình thang cân bằng nhau",
         [r"các hình chữ nhật", r"các tam giác cân",
          r"các hình bình hành"],
         r"Mỗi mặt bên là phần còn lại của một tam giác cân sau khi cắt "
         r"bởi đường thẳng song song với đáy, nên là hình thang cân."),
        (r"Hai đáy của hình chóp cụt đều là",
         r"hai đa giác đều đồng dạng nằm trong hai mặt phẳng song song",
         [r"hai đa giác đều bằng nhau",
          r"hai đa giác bất kì",
          r"hai hình tròn"],
         r"Mặt phẳng cắt song song với đáy nên đa giác thiết diện đồng "
         r"dạng với đáy; hai đáy bằng nhau chỉ xảy ra với LĂNG TRỤ."),
    ]
    gt = _chon_chi_muc(len(MAU), socau)

    cauTN = ""
    for i in gt:
        hoi, dung, nhieu, ly_do = MAU[i]
        cauTN += MC_SA_answer_text(hoi, dung, list(nhieu), ly_do, 0, 0,
                                   dang)
    return cauTN


def L11_C7_B27_TH126_MC_A_01(socau, dang=1):
    r"""Thể tích khối chóp, khối lăng trụ, khối hộp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([3, 4, 5, 6])
        h = random.choice([3, 6, 9, 12])
        loai = random.choice(["chop", "langtru"])
        if (a, h, loai) not in gt:
            gt.append((a, h, loai))

    cauTN = ""
    for a, h, loai in gt:
        S = a * a
        if loai == "chop":
            V = Fraction(S * h, 3)
            ct = r"V = \dfrac{1}{3}S_{\text{đáy}}h"
            mo_ta = (r"khối chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                     r"cạnh $%d$ và chiều cao $SA = %d$" % (a, h))
            thay = (r"\dfrac{1}{3}\cdot %d\cdot %d = %s"
                    % (S, h, _xx(V)))
            sai = S * h
        else:
            V = Fraction(S * h)
            ct = r"V = S_{\text{đáy}}h"
            mo_ta = (r"khối lăng trụ đứng có đáy là hình vuông cạnh $%d$ "
                     r"và chiều cao $%d$" % (a, h))
            thay = r"%d\cdot %d = %s" % (S, h, _xx(V))
            sai = Fraction(S * h, 3)
        dung = "$%s$" % _xx(V)
        nhieu = _ba_nhieu7c(dung, ["$%s$" % _xx(Fraction(sai)),
                                   "$%d$" % S, "$%d$" % (a * h)],
                            buoc=lambda t: "$%s$" % _xx(float(V) + t))
        debai = r"Tính thể tích của %s." % mo_ta
        giai = (r"Diện tích đáy: $S_{\text{đáy}} = %d^{2} = %d$."
                % (a, S) +
                "\\\\\n"
                r"Công thức thể tích: $%s$." % ct +
                "\\\\\n"
                r"$V = %s$." % thay)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C7_B27_TH128_MC_A_01(socau, dang=1):
    r"""Thể tích khối chóp cụt đều.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 4, 6])
        b = 2 * a
        h = random.choice([3, 6, 9])
        if (a, b, h) not in gt:
            gt.append((a, b, h))

    cauTN = ""
    for a, b, h in gt:
        S1, S2 = a * a, b * b
        V = Fraction(h, 3) * (S1 + a * b + S2)
        dung = "$%s$" % _xx(V)
        nhieu = _ba_nhieu7c(dung,
                            ["$%s$" % _xx(Fraction(h * (S1 + S2), 3)),
                             "$%s$" % _xx(Fraction(h * (S1 + S2), 2)),
                             "$%s$" % _xx(Fraction(h * S2, 3))],
                            buoc=lambda t: "$%s$" % _xx(float(V) + t))
        debai = (r"Tính thể tích khối chóp cụt đều có hai đáy là hai "
                 r"hình vuông cạnh $%d$ và $%d$, chiều cao bằng $%d$."
                 % (a, b, h))
        giai = (r"Diện tích hai đáy: $S_1 = %d^{2} = %d$ và "
                r"$S_2 = %d^{2} = %d$." % (a, S1, b, S2) +
                "\\\\\n"
                r"Công thức thể tích khối chóp cụt: "
                r"$V = \dfrac{h}{3}\left(S_1 + \sqrt{S_1S_2} + "
                r"S_2\right)$." +
                "\\\\\n"
                r"$\sqrt{S_1S_2} = \sqrt{%d\cdot %d} = %d$."
                % (S1, S2, a * b) +
                "\\\\\n"
                r"$V = \dfrac{%d}{3}\left(%d + %d + %d\right) = %s$."
                % (h, S1, a * b, S2, _xx(V)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C7_B27_TH128_SA_A_01(socau):
    r"""Thể tích khối chóp, khối lăng trụ - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([3, 4, 5, 6])
        h = random.choice([3, 6, 9, 12])
        loai = random.choice(["chop", "langtru"])
        if (a, h, loai) not in gt:
            gt.append((a, h, loai))

    cau = ""
    for a, h, loai in gt:
        S = a * a
        if loai == "chop":
            V = Fraction(S * h, 3)
            debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình "
                     r"vuông cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                     r"$SA = %d$. Tính thể tích khối chóp $S.ABCD$."
                     % (a, h))
            giai = (r"$SA \perp \left(ABCD\right)$ nên $SA$ là chiều cao "
                    r"của khối chóp." +
                    "\\\\\n"
                    r"$S_{ABCD} = %d^{2} = %d$." % (a, S) +
                    "\\\\\n"
                    r"$V = \dfrac{1}{3}S_{ABCD}\cdot SA = "
                    r"\dfrac{1}{3}\cdot %d\cdot %d = %s$."
                    % (S, h, _xx(V)))
            hinh = _hinh_chop_vuong()
        else:
            V = Fraction(S * h)
            debai = (r"Cho khối lăng trụ đứng có đáy là hình vuông cạnh "
                     r"$%d$ và chiều cao $%d$. Tính thể tích khối lăng "
                     r"trụ đó." % (a, h))
            giai = (r"$S_{\text{đáy}} = %d^{2} = %d$." % (a, S) +
                    "\\\\\n"
                    r"$V = S_{\text{đáy}}\cdot h = %d\cdot %d = %s$."
                    % (S, h, _xx(V)))
            hinh = _hinh_lap_phuong()
        nhieu = _ba_nhieu7c(_xx(V), [str(S), str(a * h),
                                     _xx(Fraction(S * h))],
                            buoc=lambda t: _xx(float(V) + t))
        cau += MC_SA_answer_const(debai, _xx(V), nhieu, giai, hinh, 0, 2)
    return cau


def L11_C7_B27_TH128_TL_A_01(socau, dong=1):
    r"""Tự luận: tính thể tích khối chóp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([3, 4, 5, 6])
        h = random.choice([3, 6, 9, 12])
        if (a, h) not in gt:
            gt.append((a, h))

    cauTN = ""
    for a, h in gt:
        S = a * a
        V = Fraction(S * h, 3)
        V2 = Fraction(S * h, 6)
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, h))

        hoi_a = r"Tính diện tích đáy $ABCD$."
        giai_a = r"$S_{ABCD} = %d^{2} = %d$." % (a, S)

        hoi_b = r"Tính thể tích khối chóp $S.ABCD$."
        giai_b = (r"$SA \perp \left(ABCD\right)$ nên $SA$ là chiều cao "
                  r"của khối chóp." +
                  "\\\\\n"
                  r"$V = \dfrac{1}{3}S_{ABCD}\cdot SA = "
                  r"\dfrac{1}{3}\cdot %d\cdot %d = %s$."
                  % (S, h, _xx(V)))

        hoi_c = r"Tính thể tích khối chóp $S.ABC$."
        giai_c = (r"Tam giác $ABC$ là nửa hình vuông $ABCD$ nên "
                  r"$S_{ABC} = \dfrac{1}{2}S_{ABCD} = %s$."
                  % _xx(Fraction(S, 2)) +
                  "\\\\\n"
                  r"Hai khối chóp có chung chiều cao $SA$." +
                  "\\\\\n"
                  r"$V_{S.ABC} = \dfrac{1}{2}V_{S.ABCD} = %s$."
                  % _xx(V2))

        ds_abcd = [(hoi_a, r"S_{ABCD} = %d" % S, giai_a),
                   (hoi_b, r"V = %s" % _xx(V), giai_b),
                   (hoi_c, r"V_{S.ABC} = %s" % _xx(V2), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def L11_C7_B27_VD129_MC_A_01(socau, dang=1):
    r"""Vận dụng kiến thức về hình chóp cụt đều.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 4, 6])
        b = 2 * a
        h = random.choice([3, 6, 9])
        if (a, b, h) not in gt:
            gt.append((a, b, h))

    cauTN = ""
    for a, b, h in gt:
        S1, S2 = a * a, b * b
        Vcut = Fraction(h, 3) * (S1 + a * b + S2)
        # chop lon: day canh b, chieu cao 2h (vi ti so dong dang 1/2)
        Vlon = Fraction(S2 * 2 * h, 3)
        dung = "$%s$" % _xx(Vlon)
        nhieu = _ba_nhieu7c(dung, ["$%s$" % _xx(Vcut),
                                   "$%s$" % _xx(Fraction(S2 * h, 3)),
                                   "$%s$" % _xx(Vlon - Vcut)],
                            buoc=lambda t: "$%s$" % _xx(float(Vlon) + t))
        debai = (r"Một khối chóp cụt đều có hai đáy là hai hình vuông "
                 r"cạnh $%d$ và $%d$, chiều cao bằng $%d$. Tính thể tích "
                 r"của khối chóp ĐỀU ban đầu (trước khi cắt)."
                 % (a, b, h))
        giai = (r"Vì cạnh đáy nhỏ bằng nửa cạnh đáy lớn nên mặt phẳng "
                r"cắt chia chiều cao theo tỉ số $\dfrac{1}{2}$." +
                "\\\\\n"
                r"Gọi $H$ là chiều cao khối chóp lớn; phần chóp bị bỏ "
                r"đi có chiều cao $\dfrac{H}{2}$." +
                "\\\\\n"
                r"Chiều cao khối chóp cụt là "
                r"$H - \dfrac{H}{2} = \dfrac{H}{2} = %d$, suy ra "
                r"$H = %d$." % (h, 2 * h) +
                "\\\\\n"
                r"$V = \dfrac{1}{3}\cdot %d^{2}\cdot %d = "
                r"\dfrac{1}{3}\cdot %d\cdot %d = %s$."
                % (b, 2 * h, S2, 2 * h, _xx(Vlon)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C7_B27_VD129_SA_A_01(socau):
    r"""Thể tích khối chóp cụt đều - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 6])
        b = 2 * a
        h = random.choice([3, 6, 9, 12])
        if (a, b, h) not in gt:
            gt.append((a, b, h))

    cau = ""
    for a, b, h in gt:
        S1, S2 = a * a, b * b
        V = Fraction(h, 3) * (S1 + a * b + S2)
        debai = (r"Tính thể tích khối chóp cụt đều có hai đáy là hai "
                 r"hình vuông cạnh $%d$ và $%d$, chiều cao bằng $%d$."
                 % (a, b, h))
        giai = (r"$S_1 = %d^{2} = %d$, $S_2 = %d^{2} = %d$."
                % (a, S1, b, S2) +
                "\\\\\n"
                r"$\sqrt{S_1S_2} = %d\cdot %d = %d$." % (a, b, a * b) +
                "\\\\\n"
                r"$V = \dfrac{h}{3}\left(S_1 + \sqrt{S_1S_2} + "
                r"S_2\right) = \dfrac{%d}{3}\left(%d + %d + %d\right) "
                r"= %s$." % (h, S1, a * b, S2, _xx(V)))
        nhieu = _ba_nhieu7c(_xx(V),
                            [_xx(Fraction(h * (S1 + S2), 3)),
                             _xx(Fraction(h * S2, 3)), str(S1 + S2)],
                            buoc=lambda t: _xx(float(V) + t))
        cau += MC_SA_answer_const(debai, _xx(V), nhieu, giai, 0, 0, 2)
    return cau


def L11_C7_B27_VD129_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán về hình chóp cụt đều.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, 4, 6])
        b = 2 * a
        h = random.choice([3, 6, 9, 12])
        if (a, b, h) not in gt:
            gt.append((a, b, h))

    cauTN = ""
    for a, b, h in gt:
        S1, S2 = a * a, b * b
        Vcut = Fraction(h, 3) * (S1 + a * b + S2)
        Vlon = Fraction(S2 * 2 * h, 3)
        Vnho = Vlon - Vcut
        debai = (r"Một khối chóp cụt đều có hai đáy là hai hình vuông "
                 r"cạnh $%d$ và $%d$, chiều cao bằng $%d$." % (a, b, h))

        hoi_a = r"Tính diện tích hai đáy của khối chóp cụt."
        giai_a = (r"$S_1 = %d^{2} = %d$ (đáy nhỏ)." % (a, S1) +
                  "\\\\\n"
                  r"$S_2 = %d^{2} = %d$ (đáy lớn)." % (b, S2))

        hoi_b = r"Tính thể tích khối chóp cụt."
        giai_b = (r"$V = \dfrac{h}{3}\left(S_1 + \sqrt{S_1S_2} + "
                  r"S_2\right)$." +
                  "\\\\\n"
                  r"$\sqrt{S_1S_2} = \sqrt{%d\cdot %d} = %d$."
                  % (S1, S2, a * b) +
                  "\\\\\n"
                  r"$V = \dfrac{%d}{3}\left(%d + %d + %d\right) = %s$."
                  % (h, S1, a * b, S2, _xx(Vcut)))

        hoi_c = (r"Tính thể tích phần chóp đã bị cắt bỏ (khối chóp nhỏ "
                 r"phía trên).")
        giai_c = (r"Cạnh đáy nhỏ bằng nửa cạnh đáy lớn nên tỉ số đồng "
                  r"dạng là $\dfrac{1}{2}$; chiều cao khối chóp nhỏ "
                  r"bằng nửa chiều cao khối chóp lớn." +
                  "\\\\\n"
                  r"Chiều cao khối chóp cụt bằng $\dfrac{H}{2} = %d$ "
                  r"nên $H = %d$ và chiều cao khối chóp nhỏ là $%d$."
                  % (h, 2 * h, h) +
                  "\\\\\n"
                  r"$V_{\text{nhỏ}} = \dfrac{1}{3}\cdot %d\cdot %d = %s$."
                  % (S1, h, _xx(Vnho)) +
                  "\\\\\n"
                  r"Kiểm lại: $V_{\text{lớn}} = \dfrac{1}{3}\cdot "
                  r"%d\cdot %d = %s$ và $%s - %s = %s$ đúng bằng thể "
                  r"tích khối chóp cụt."
                  % (S2, 2 * h, _xx(Vlon), _xx(Vlon), _xx(Vnho),
                     _xx(Vcut)))

        ds_abcd = [(hoi_a, r"S_1 = %d,\ S_2 = %d" % (S1, S2), giai_a),
                   (hoi_b, r"V = %s" % _xx(Vcut), giai_b),
                   (hoi_c, r"V_{\text{nhỏ}} = %s" % _xx(Vnho), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 7
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C7_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - hai đường thẳng vuông góc, đường thẳng vuông góc mặt
    phẳng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BO = [b for b in PYTAGO7C
          if (Fraction(b[1] * b[0], b[2]) * 100).denominator == 1]
    gt = []
    while len(gt) < socau:
        a, h, c = random.choice(BO)
        if (a, h, c) not in gt:
            gt.append((a, h, c))

    cauTF = ""
    for a, h, c in gt:
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, h))

        ds_abcd = (
            # a) NB - đọc thẳng từ giả thiết
            [
                (r"{\True $SA \perp AB$}",
                 r"Đúng. $SA \perp \left(ABCD\right)$ mà "
                 r"$AB \subset \left(ABCD\right)$ nên $SA \perp AB$."),
                (r"{$SA \parallel AB$}",
                 r"Sai. $SA$ vuông góc với mặt đáy nên vuông góc với "
                 r"$AB$, không thể song song."),
            ],
            # b) TH - một lần dùng điều kiện đủ
            [
                (r"{\True $BC \perp \left(SAB\right)$}",
                 r"Đúng. $BC \perp AB$ (hình vuông) và $BC \perp SA$ "
                 r"(vì $SA$ vuông góc với đáy)." + "\\\\\n" +
                 r"$AB$ và $SA$ CẮT NHAU tại $A$, cùng nằm trong "
                 r"$\left(SAB\right)$, nên "
                 r"$BC \perp \left(SAB\right)$."),
                (r"{$BC \perp \left(SAD\right)$}",
                 r"Sai. $BC \parallel AD$ mà "
                 r"$AD \subset \left(SAD\right)$, nên $BC$ SONG SONG "
                 r"với $\left(SAD\right)$ chứ không vuông góc."),
            ],
            # c) VD - dùng định lí Pytago
            [
                (r"{\True $SB = %d$}" % c,
                 r"Đúng. Tam giác $SAB$ vuông tại $A$ nên" + "\\\\\n" +
                 r"$SB = \sqrt{SA^{2} + AB^{2}} = "
                 r"\sqrt{%d^{2} + %d^{2}} = \sqrt{%d} = %d$."
                 % (h, a, h * h + a * a, c)),
                (r"{$SB = %d$}" % (h + a),
                 r"Sai. Không được CỘNG hai cạnh góc vuông; phải dùng "
                 r"định lí Pytago, được $SB = %d$." % c),
            ],
            # d) VDC - phải tự dựng đường vuông góc rồi mới tính được
            [
                (r"{\True Khoảng cách từ $A$ đến $\left(SBC\right)$ "
                 r"bằng $%s$}" % _xx(Fraction(h * a, c)),
                 r"Đúng. $BC \perp \left(SAB\right)$ nên "
                 r"$\left(SBC\right) \perp \left(SAB\right)$." +
                 "\\\\\n" +
                 r"Kẻ $AH \perp SB$ tại $H$ thì $BC \perp AH$, suy ra "
                 r"$AH \perp \left(SBC\right)$; khoảng cách cần tìm "
                 r"chính là $AH$." + "\\\\\n" +
                 r"$AH = \dfrac{SA\cdot AB}{SB} = "
                 r"\dfrac{%d\cdot %d}{%d} = %s$."
                 % (h, a, c, _xx(Fraction(h * a, c)))),
                (r"{Khoảng cách từ $A$ đến $\left(SBC\right)$ bằng "
                 r"$%d$}" % a,
                 r"Sai. $%d$ là độ dài $AB$, mà $AB$ KHÔNG vuông góc "
                 r"với $\left(SBC\right)$." % a + "\\\\\n" +
                 r"Khoảng cách đúng là $AH = %s$."
                 % _xx(Fraction(h * a, c))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF


def L11_C7_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - hai mặt phẳng vuông góc, khoảng cách và thể tích.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([3, 4, 5, 6])
        h = random.choice([3, 6, 9, 12])
        if (a, h) not in gt:
            gt.append((a, h))

    cauTF = ""
    for a, h in gt:
        S = a * a
        V = Fraction(S * h, 3)
        hinh = _hinh_chop_vuong()
        debai = (r"Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông "
                 r"cạnh $%d$, $SA \perp \left(ABCD\right)$ và "
                 r"$SA = %d$." % (a, h))

        ds_abcd = (
            # a) NB - nhớ công thức
            [
                (r"{\True Thể tích khối chóp bằng "
                 r"$\dfrac{1}{3}S_{\text{đáy}}h$}",
                 r"Đúng. Đây là công thức thể tích của khối chóp."),
                (r"{Thể tích khối chóp bằng $S_{\text{đáy}}h$}",
                 r"Sai. Đó là công thức của khối LĂNG TRỤ; khối chóp "
                 r"chỉ bằng $\dfrac{1}{3}$ giá trị đó."),
            ],
            # b) TH - điều kiện đủ để hai mặt phẳng vuông góc
            [
                (r"{\True $\left(SAB\right) \perp "
                 r"\left(ABCD\right)$}",
                 r"Đúng. $\left(SAB\right)$ chứa $SA$ mà "
                 r"$SA \perp \left(ABCD\right)$." + "\\\\\n" +
                 r"Mặt phẳng chứa một đường thẳng vuông góc với mặt "
                 r"phẳng kia thì vuông góc với mặt phẳng ấy."),
                (r"{$\left(SBC\right) \perp \left(ABCD\right)$}",
                 r"Sai. $\left(SBC\right)$ không chứa đường thẳng nào "
                 r"vuông góc với $\left(ABCD\right)$." + "\\\\\n" +
                 r"Thực tế $\left(SBC\right)$ tạo với mặt đáy một góc "
                 r"nhọn chứ không vuông góc."),
            ],
            # c) VD - tính thể tích
            [
                (r"{\True Thể tích khối chóp $S.ABCD$ bằng $%s$}"
                 % _xx(V),
                 r"Đúng. $S_{ABCD} = %d^{2} = %d$ và chiều cao là "
                 r"$SA = %d$." % (a, S, h) + "\\\\\n" +
                 r"$V = \dfrac{1}{3}\cdot %d\cdot %d = %s$."
                 % (S, h, _xx(V))),
                (r"{Thể tích khối chóp $S.ABCD$ bằng $%s$}"
                 % _xx(Fraction(S * h)),
                 r"Sai. Đó là thể tích khối LĂNG TRỤ cùng đáy cùng "
                 r"chiều cao; khối chóp chỉ bằng $\dfrac{1}{3}$, tức "
                 r"$%s$." % _xx(V)),
            ],
            # d) VDC - so sánh thể tích hai khối chóp chung chiều cao
            [
                (r"{\True Thể tích khối chóp $S.ABC$ bằng nửa thể tích "
                 r"khối chóp $S.ABCD$}",
                 r"Đúng. Tam giác $ABC$ là nửa hình vuông $ABCD$ nên "
                 r"$S_{ABC} = \dfrac{1}{2}S_{ABCD}$." + "\\\\\n" +
                 r"Hai khối chóp có CHUNG đỉnh $S$ và chung chiều cao "
                 r"$SA$." + "\\\\\n" +
                 r"Vậy $V_{S.ABC} = \dfrac{1}{2}V_{S.ABCD} = %s$."
                 % _xx(Fraction(S * h, 6))),
                (r"{Thể tích khối chóp $S.ABC$ bằng thể tích khối chóp "
                 r"$S.ABCD$}",
                 r"Sai. Hai khối chóp chung chiều cao nhưng diện tích "
                 r"đáy khác nhau: $S_{ABC}$ chỉ bằng nửa $S_{ABCD}$." +
                 "\\\\\n" +
                 r"Do đó thể tích cũng chỉ bằng một nửa."),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF
