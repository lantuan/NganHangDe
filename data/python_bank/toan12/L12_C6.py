# -*- coding: utf-8 -*-
r"""Lớp 12 - Chương 6. Xác suất có điều kiện
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Bám đúng hai bài của PPCT:

  * Bài 18. Xác suất có điều kiện
    $P\left(A \mid B\right) = \dfrac{P\left(AB\right)}{P\left(B\right)}$
    với $P\left(B\right) > 0$.
  * Bài 19. Công thức xác suất toàn phần và công thức Bayes
    $P\left(A\right) = P\left(B\right)P\left(A \mid B\right)
     + P\left(\overline{B}\right)P\left(A \mid \overline{B}\right)$;
    $P\left(B \mid A\right)
     = \dfrac{P\left(B\right)P\left(A \mid B\right)}{P\left(A\right)}$.

BÀI TOÁN LUÔN DỰNG TỪ SỐ ĐẾM, KHÔNG DỰNG TỪ SỐ THẬP PHÂN.

Lí do: câu trả lời ngắn chấm bằng SO KHỚP CHUỖI nên đáp số phải viết
được CHÍNH XÁC. Nếu thả số thập phân tuỳ ý vào sơ đồ cây thì Bayes hay
ra số vô hạn tuần hoàn (ví dụ $0{,}54 : 0{,}62$), học sinh bấm máy ra
$0{,}870967\ldots$ - không chấm được.

Cách làm: mọi mẫu số có thể bị chia đều là SỐ ĐẸP, tức chỉ gồm thừa số
$2$ và $5$ (xem MAU_DEP). Bảng $2 \times 2$ dựng sao cho CẢ BỐN tổng
lề đều đẹp; bài hai nguồn dựng NGƯỢC từ tổng số sản phẩm lỗi. Nhờ vậy
mọi xác suất trong đề đều là số thập phân HỮU HẠN.

Quy ước trình bày: chữ tiếng Việt không bao giờ nằm trần trong $...$;
mọi chuỗi có dấu gạch chéo đều là chuỗi r"..."; bảng số liệu vẽ bằng
TikZ chứ KHÔNG dùng tabular (MathJax trên web không dựng được tabular).
"""
import math
import random
from fractions import Fraction

from math_type import *          # noqa: F401,F403

DAU_THAP_PHAN = ","

# Mẫu số ĐẸP: chỉ gồm thừa số 2 và 5 nên phép chia luôn dừng.
# Chi lay UOC CUA 1000 (va >= 8): chia cho cac so nay luon ra toi da BA
# chu so thap phan. Ban dau co ca 16, 32, 64, 80, 128... - kiem toan doc
# lap bat duoc 15/128 = 0,1171875 bi in thanh 0,117188 (LAM TRON NGAM,
# khong he bao) va qua dai so voi o tra loi ngan 4 ky tu. Da bo.
MAU_DEP = [8, 10, 20, 25, 40, 50, 100, 125, 200, 250]


def _dep(n):
    """n có phải số chỉ gồm thừa số 2 và 5 không (n > 0)."""
    if n <= 0:
        return False
    for p in (2, 5):
        while n % p == 0:
            n //= p
    return n == 1


def _xx(x, n=4):
    """Viết số thập phân kiểu Việt Nam, bỏ các số 0 thừa ở cuối."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _chu_so(fr):
    """Số chữ số thập phân cần để viết ĐÚNG phân số fr (99 nếu vô hạn)."""
    fr = Fraction(fr)
    for k in range(0, 8):
        if (fr * 10 ** k).denominator == 1:
            return k
    return 99


def _ps(tu, mau):
    """Chia CHÍNH XÁC hai số nguyên, viết ra số thập phân hữu hạn.

    Viết bằng số học số nguyên chứ không qua float, nên không bao giờ có
    chuyện làm tròn ngầm. Cần quá BA chữ số thập phân thì vang lỗi ngay
    lúc sinh câu - không để lọt đáp số dài ngoằng hay bị làm tròn.
    """
    fr = Fraction(tu, mau)
    k = _chu_so(fr)
    if k > 3:
        raise ValueError("%s can %s chu so thap phan - qua dai" % (fr, k))
    v = fr * 10 ** k
    dau = "-" if v < 0 else ""
    v = abs(int(v))
    nguyen, le = divmod(v, 10 ** k)
    if k == 0:
        return "%s%d" % (dau, nguyen)
    return "%s%d%s%0*d" % (dau, nguyen, DAU_THAP_PHAN, k, le)


def _lech(fr, k):
    r"""Phương án nhiễu dự phòng: đáp số lệch đi $k$ phần trăm, luôn
    nằm trong $(0; 1)$ và luôn viết được chính xác."""
    fr = Fraction(fr)
    v = fr + Fraction(k, 100)
    if v >= 1:
        v = fr - Fraction(k, 100)
    if v <= 0:
        v = Fraction(k, 200)
    return _ps(v.numerator, v.denominator)

def _ba_nhieu6(dapso, ung_vien, buoc=None):
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


# =====================================================================
# BẢNG 2 x 2
# =====================================================================

BOI_CANH_BANG = [
    ("học sinh khối 12 của một trường", "Nam", "Nữ",
     "Có tham gia", "Không tham gia", "tham gia câu lạc bộ Toán",
     "học sinh"),
    ("khách hàng của một siêu thị", "Nam", "Nữ",
     "Có dùng", "Không dùng", "dùng thẻ thành viên", "khách hàng"),
    ("hộ gia đình trong một khu phố", "Nhà mặt phố", "Nhà trong ngõ",
     "Có lắp", "Không lắp", "lắp Internet cáp quang", "hộ gia đình"),
    ("bệnh nhân đến khám tại một phòng khám", "Dưới 40 tuổi",
     "Từ 40 tuổi trở lên", "Có tập thể dục", "Không tập thể dục",
     "tập thể dục đều đặn", "người"),
]


def _bang_2x2():
    r"""Bảng $2\times 2$ mà CẢ BỐN tổng lề đều là số đẹp.

    Trả về $(a, b, c, d)$ theo sơ đồ

        .            | cột 1 | cột 2 | tổng hàng
        hàng 1       |   a   |   b   |  a + b
        hàng 2       |   c   |   d   |  c + d
        tổng cột     | a + c | b + d |    n

    Nhờ cả $a+b$, $c+d$, $a+c$, $b+d$ đều đẹp nên MỌI xác suất có điều
    kiện đọc được từ bảng này đều là số thập phân hữu hạn.
    """
    for _ in range(400):
        n = random.choice([40, 50, 100, 125, 200, 250])
        cot = [(m, n - m) for m in MAU_DEP
               if 8 <= m <= n - 8 and _dep(n - m)]
        hang = [s for s in MAU_DEP if 8 <= s <= n - 8 and _dep(n - s)]
        if not cot or not hang:
            continue
        m1, m2 = random.choice(cot)
        s1 = random.choice(hang)
        lo = max(1, s1 - m2)
        hi = min(m1 - 1, s1 - 1)
        if lo > hi:
            continue
        a = random.randint(lo, hi)
        b = s1 - a
        c = m1 - a
        d = m2 - b
        if min(a, b, c, d) >= 3:
            return a, b, c, d
    return 20, 30, 30, 20         # bộ dự phòng: bốn tổng lề đều 50, tổng 100


def _hinh_bang2x2(cot1, cot2, hang1, hang2, a, b, c, d, ten_dv="Số người"):
    r"""Vẽ bảng $2\times 2$ bằng TikZ.

    KHÔNG dùng môi trường tabular: MathJax trên trang làm bài không
    dựng được tabular, câu sẽ vỡ hết. Vẽ bằng TikZ thì cả bản PDF lẫn
    bản web đều nhận được một tấm ảnh giống nhau.
    """
    ten = [ten_dv, cot1, cot2, "Tổng"]
    hang = [[hang1, a, b, a + b],
            [hang2, c, d, c + d],
            ["Tổng", a + c, b + d, a + b + c + d]]
    rong = [3.3, 2.1, 2.1, 1.6]
    x = [0.0]
    for w in rong:
        x.append(x[-1] + w)
    cao = 0.78
    y = [-i * cao for i in range(5)]

    ra = ["\\begin{tikzpicture}[scale=0.92,line join=round,"
          "font=\\footnotesize]"]
    # Nền cho hàng tiêu đề và cột tiêu đề.
    ra.append("\\fill[black!7] (%s,%s) rectangle (%s,%s);"
              % (_toa(x[0]), _toa(y[0]), _toa(x[4]), _toa(y[1])))
    ra.append("\\fill[black!7] (%s,%s) rectangle (%s,%s);"
              % (_toa(x[0]), _toa(y[1]), _toa(x[1]), _toa(y[4])))
    # Khung lưới.
    for i in range(5):
        ra.append("\\draw[black!65] (%s,%s) -- (%s,%s);"
                  % (_toa(x[0]), _toa(y[i]), _toa(x[4]), _toa(y[i])))
    for j in range(5):
        ra.append("\\draw[black!65] (%s,%s) -- (%s,%s);"
                  % (_toa(x[j]), _toa(y[0]), _toa(x[j]), _toa(y[4])))
    # Chữ.
    def o(j, i, chu, dam=False):
        gx = (x[j] + x[j + 1]) / 2.0
        gy = (y[i] + y[i + 1]) / 2.0
        ra.append("\\node[align=center,text width=%scm] at (%s,%s) "
                  "{%s%s%s};" % (_toa(rong[j] - 0.18), _toa(gx), _toa(gy),
                                 "\\textbf{" if dam else "", chu,
                                 "}" if dam else ""))
    for j in range(4):
        o(j, 0, ten[j], True)
    for i in range(3):
        o(0, i + 1, hang[i][0], i == 2)
        for j in range(3):
            o(j + 1, i + 1, "$%d$" % hang[i][j + 1], i == 2)
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


# =====================================================================
# BÀI TOÁN HAI NGUỒN (sơ đồ hình cây)
# =====================================================================

BOI_CANH_NGUON = [
    ("một lô hàng", "Phân xưởng I", "Phân xưởng II", "sản phẩm",
     "bị lỗi", "lấy ngẫu nhiên một sản phẩm từ lô hàng"),
    ("một kho linh kiện", "Nhà máy A", "Nhà máy B", "linh kiện",
     "không đạt chuẩn", "lấy ngẫu nhiên một linh kiện từ kho"),
    ("một vườn ươm", "Luống 1", "Luống 2", "cây giống",
     "bị sâu bệnh", "chọn ngẫu nhiên một cây giống trong vườn"),
    ("một đợt kiểm tra", "Lớp 12A", "Lớp 12B", "bài kiểm tra",
     "đạt điểm giỏi", "chọn ngẫu nhiên một bài kiểm tra"),
]


def _bo_hai_nguon(hoi=None):
    r"""Dựng NGƯỢC bài toán hai nguồn để mọi xác suất đều viết được đúng.

    Chọn trước TỔNG số sản phẩm đặc biệt $T = d_1 + d_2$ rồi mới suy ra
    cỡ hai nguồn. Sau đó KIỂM từng xác suất sẽ xuất hiện trong đề, trên
    sơ đồ cây và trong lời giải: tất cả phải viết được với tối đa ba chữ
    số thập phân.

    hoi: tên đại lượng được hỏi ở câu TRẢ LỜI NGẮN ("d1T", "d2T", "Tn") -
    đại lượng đó phải gọn hơn nữa, tối đa HAI chữ số thập phân, để vừa
    ô trả lời 4 ký tự (ví dụ "0,35").

    Trả về $(n_1, n_2, d_1, d_2)$.
    """
    for _ in range(3000):
        T = random.choice([10, 20, 25, 40, 50])
        d1 = random.randint(2, T - 2)
        d2 = T - d1
        k1 = random.choice([4, 5, 8, 10, 20, 25])
        k2 = random.choice([4, 5, 8, 10, 20, 25])
        # Hai nguon phai co TI LE KHAC NHAU. Trung ti le thi A va B doc
        # lap, P(B | A) = P(B): bai Bayes thanh tam thuong va de doc nhu
        # danh do (kiem toan 29/09/2026 bat duoc de 16/160 va 34/340).
        if k1 == k2:
            continue
        n1, n2 = d1 * k1, d2 * k2
        if not (40 <= n1 <= 1200 and 40 <= n2 <= 1200):
            continue
        # n1 = T thi P(B | A) = P(A | B): menh de SAI co y o cau Dung/Sai
        # lai hoa DUNG.
        if T in (n1, n2):
            continue
        n = n1 + n2
        xs = {"n1n": Fraction(n1, n), "n2n": Fraction(n2, n),
              "d1n1": Fraction(d1, n1), "d2n2": Fraction(d2, n2),
              "Tn": Fraction(T, n), "d1T": Fraction(d1, T),
              "d2T": Fraction(d2, T)}
        if any(_chu_so(v) > 3 for v in xs.values()):
            continue
        # P(B) trung P(A | B) thi menh de sai co y "P(B) = ti le loi" o
        # cau Dung/Sai lai hoa DUNG (kiem toan bat duoc 3 cau).
        if xs["n1n"] == xs["d1n1"] or xs["n2n"] == xs["d2n2"]:
            continue
        if hoi and _chu_so(xs[hoi]) > 2:
            continue
        return n1, n2, d1, d2
    return 200, 300, 10, 15

def _hinh_cay(ten1, ten2, n1, n2, d1, d2, ten_dac_biet):
    r"""Sơ đồ hình cây hai tầng, vẽ bằng TikZ thuần.

    Tầng 1: chọn nguồn. Tầng 2: sản phẩm có đặc biệt hay không.
    Trên mỗi nhánh ghi xác suất, viết dưới dạng số thập phân hữu hạn.
    """
    n = n1 + n2
    p1, p2 = _ps(n1, n), _ps(n2, n)
    q1, r1 = _ps(d1, n1), _ps(n1 - d1, n1)
    q2, r2 = _ps(d2, n2), _ps(n2 - d2, n2)
    D = ten_dac_biet

    ra = ["\\begin{tikzpicture}[scale=1,>=stealth,line join=round,"
          "font=\\footnotesize]"]
    ra.append("\\node (O) at (0,0) {$\\bullet$};")
    dinh = [("N1", 2.6, 1.9, ten1, p1), ("N2", 2.6, -1.9, ten2, p2)]
    for ten, x, y, nhan, p in dinh:
        # KHONG boc ten tieng Viet trong $...$: LaTeX che do toan se
        # nuot het dau ("Phan xuong" thanh "Phn xng"). Day la loi da
        # gap khi ve thu ngay 29/09/2026.
        ra.append("\\node[align=center] (%s) at (%s,%s) {%s};"
                  % (ten, _toa(x), _toa(y), nhan))
        ra.append("\\draw[->] (O) -- (%s);" % ten)
        ra.append("\\node[fill=white,inner sep=1pt] at (%s,%s) {$%s$};"
                  % (_toa(x / 2.0 - 0.15), _toa(y / 2.0 + 0.28), p))
    la = [("N1", 1.05, D, q1), ("N1", -1.05, r"\overline{%s}" % D, r1),
          ("N2", 1.05, D, q2), ("N2", -1.05, r"\overline{%s}" % D, r2)]
    for k, (cha, dy, nhan, p) in enumerate(la):
        gy = (1.9 if cha == "N1" else -1.9) + dy
        ra.append("\\node (L%d) at (5.6,%s) {$%s$};" % (k, _toa(gy), nhan))
        ra.append("\\draw[->] (%s) -- (L%d);" % (cha, k))
        ra.append("\\node[fill=white,inner sep=1pt] at (%s,%s) {$%s$};"
                  % (_toa(4.2), _toa((1.9 if cha == "N1" else -1.9)
                                     + dy / 2.0 + 0.2), p))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


# =====================================================================
# BÀI 18. XÁC SUẤT CÓ ĐIỀU KIỆN
# =====================================================================

def L12_C6_B18_NB053_MC_A_01(socau, dang=1):
    r"""Nhận biết khái niệm xác suất có điều kiện - dùng thẳng định nghĩa
    $P\left(A \mid B\right) = \dfrac{P\left(AB\right)}{P\left(B\right)}$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        kb = random.choice([20, 25, 40, 50, 80])
        kq = random.choice([20, 25, 40, 50, 60, 75, 80])
        if _chu_so(Fraction(kb * kq, 10000)) > 3:
            continue            # vi du 0,25 . 0,75 = 0,1875 - qua dai
        if (kb, kq) not in gt:
            gt.append((kb, kq))

    cauTN = ""
    for kb, kq in gt:
        pb = _ps(kb, 100)
        pq = _ps(kq, 100)
        pab = _ps(kb * kq, 10000)
        dung = "$%s$" % pq
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % pab, "$%s$" % pb, "$%s$" % _ps(100 - kq, 100),
             "$%s$" % _ps(kq, 200)],
            buoc=lambda k: "$%s$" % _lech(Fraction(kq, 100), 5 * k))
        debai = (r"Cho hai biến cố $A$ và $B$ với "
                 r"$P\left(B\right) = %s$ và $P\left(AB\right) = %s$. "
                 r"Tính $P\left(A \mid B\right)$." % (pb, pab))
        giai = (r"Theo định nghĩa xác suất có điều kiện," +
                "\\\\\n"
                r"$P\left(A \mid B\right) = "
                r"\dfrac{P\left(AB\right)}{P\left(B\right)} "
                r"= \dfrac{%s}{%s} = %s$." % (pab, pb, pq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _de_bang(boi_canh):
    """Dựng đề bảng 2x2: trả về (số liệu, câu dẫn, hình vẽ)."""
    a, b, c, d = _bang_2x2()
    nhom, h1, h2, c1, c2, viec, dv = boi_canh
    n = a + b + c + d
    dan = (r"Khảo sát $%d$ %s về việc %s, kết quả cho trong bảng sau."
           % (n, nhom, viec))
    hinh = _hinh_bang2x2(c1, c2, h1, h2, a, b, c, d,
                         "Số %s" % dv)
    return (a, b, c, d), (nhom, h1, h2, c1, c2, viec, dv), dan, hinh


def L12_C6_B18_TH054_MC_A_01(socau, dang=1):
    r"""Ý nghĩa xác suất có điều kiện trong tình huống thực tiễn - đọc
    số liệu từ bảng $2\times 2$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        (a, b, c, d), (nhom, h1, h2, c1, c2, viec, dv), dan, hinh = \
            _de_bang(random.choice(BOI_CANH_BANG))
        n = a + b + c + d
        dung = "$%s$" % _ps(a, a + b)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _ps(a, a + c), "$%s$" % _ps(a, n),
             "$%s$" % _ps(a + b, n), "$%s$" % _ps(b, a + b)],
            buoc=lambda k: "$%s$" % _lech(Fraction(a, a + b), k))
        debai = (dan + "\\\\\n" +
                 r"Chọn ngẫu nhiên một %s trong số đó. Biết %s đó thuộc "
                 r"nhóm ``%s'', tính xác suất %s đó %s."
                 % (dv, dv, h1, dv, c1.lower()))
        giai = (r"Trong $%d$ %s thuộc nhóm ``%s'' có $%d$ %s %s."
                % (a + b, dv, h1, a, dv, c1.lower()) +
                "\\\\\n"
                r"Gọi $A$ là biến cố ``%s %s'', $B$ là biến cố ``%s "
                r"thuộc nhóm %s''. Khi đó" % (dv.capitalize(), c1.lower(),
                                              dv.capitalize(), h1) +
                "\\\\\n"
                r"$P\left(A \mid B\right) = \dfrac{%d}{%d} = %s$."
                % (a, a + b, _ps(a, a + b)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L12_C6_B18_TH054_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - xác suất có điều kiện đọc từ bảng $2\times 2$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cau = ""
    for _ in range(socau):
        # Tra loi ngan: dap so toi da HAI chu so thap phan (vua o 4 ky tu).
        while True:
            (a, b, c, d), (nhom, h1, h2, c1, c2, viec, dv), dan, hinh = \
                _de_bang(random.choice(BOI_CANH_BANG))
            if _chu_so(Fraction(c, c + d)) <= 2:
                break
        n = a + b + c + d
        dapso = _ps(c, c + d)
        nhieu = _ba_nhieu6(dapso,
                           [_ps(c, a + c), _ps(c, n), _ps(c + d, n)],
                           buoc=lambda k: _lech(Fraction(c, c + d), k))
        debai = (dan + "\\\\\n" +
                 r"Chọn ngẫu nhiên một %s trong số đó. Biết %s đó thuộc "
                 r"nhóm ``%s'', tính xác suất %s đó %s."
                 % (dv, dv, h2, dv, c1.lower()))
        giai = (r"Nhóm ``%s'' có $%d$ %s, trong đó $%d$ %s %s."
                % (h2, c + d, dv, c, dv, c1.lower()) +
                "\\\\\n"
                r"Vậy xác suất cần tìm là $\dfrac{%d}{%d} = %s$."
                % (c, c + d, dapso))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, hinh, 0, 2)
    return cau


# =====================================================================
# BÀI 19. CÔNG THỨC XÁC SUẤT TOÀN PHẦN VÀ CÔNG THỨC BAYES
# =====================================================================

def L12_C6_B19_TH055_MC_A_01(socau, dang=1):
    r"""Công thức xác suất toàn phần đọc từ bảng $2\times 2$.

    $P\left(A\right) = P\left(B\right)P\left(A \mid B\right)
     + P\left(\overline{B}\right)P\left(A \mid \overline{B}\right)$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        (a, b, c, d), (nhom, h1, h2, c1, c2, viec, dv), dan, hinh = \
            _de_bang(random.choice(BOI_CANH_BANG))
        n = a + b + c + d
        dung = "$%s$" % _ps(a + c, n)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _ps(a, n), "$%s$" % _ps(a, a + b),
             "$%s$" % _ps(a + b, n), "$%s$" % _ps(b + d, n)],
            buoc=lambda k: "$%s$" % _lech(Fraction(a + c, n), k))
        debai = (dan + "\\\\\n" +
                 r"Chọn ngẫu nhiên một %s trong số đó. Tính xác suất %s "
                 r"đó %s." % (dv, dv, c1.lower()))
        giai = (r"Gọi $A$ là biến cố ``%s %s'', $B$ là biến cố ``%s "
                r"thuộc nhóm %s''."
                % (dv.capitalize(), c1.lower(), dv.capitalize(), h1) +
                "\\\\\n"
                r"Theo công thức xác suất toàn phần," +
                "\\\\\n"
                r"$P\left(A\right) = P\left(B\right)"
                r"P\left(A \mid B\right) + P\left(\overline{B}\right)"
                r"P\left(A \mid \overline{B}\right)$" +
                "\\\\\n"
                r"$= \dfrac{%d}{%d}\cdot\dfrac{%d}{%d} + "
                r"\dfrac{%d}{%d}\cdot\dfrac{%d}{%d} "
                r"= \dfrac{%d}{%d} = %s$."
                % (a + b, n, a, a + b, c + d, n, c, c + d,
                   a + c, n, _ps(a + c, n)) +
                "\\\\\n"
                r"Cũng có thể đọc thẳng trên bảng: cột ``%s'' có $%d$ "
                r"%s trên tổng $%d$." % (c1, a + c, dv, n))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L12_C6_B19_TH056_MC_A_01(socau, dang=1):
    r"""Công thức Bayes đọc từ bảng $2\times 2$ - ĐẢO chiều điều kiện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        (a, b, c, d), (nhom, h1, h2, c1, c2, viec, dv), dan, hinh = \
            _de_bang(random.choice(BOI_CANH_BANG))
        n = a + b + c + d
        dung = "$%s$" % _ps(a, a + c)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _ps(a, a + b), "$%s$" % _ps(a, n),
             "$%s$" % _ps(a + c, n), "$%s$" % _ps(c, a + c)],
            buoc=lambda k: "$%s$" % _lech(Fraction(a, a + c), k))
        debai = (dan + "\\\\\n" +
                 r"Chọn ngẫu nhiên một %s trong số đó và biết rằng %s "
                 r"đó %s. Tính xác suất %s đó thuộc nhóm ``%s''."
                 % (dv, dv, c1.lower(), dv, h1))
        giai = (r"Gọi $A$ là biến cố ``%s %s'', $B$ là biến cố ``%s "
                r"thuộc nhóm %s''. Cần tính $P\left(B \mid A\right)$."
                % (dv.capitalize(), c1.lower(), dv.capitalize(), h1) +
                "\\\\\n"
                r"Theo công thức Bayes," +
                "\\\\\n"
                r"$P\left(B \mid A\right) = \dfrac{P\left(B\right)"
                r"P\left(A \mid B\right)}{P\left(A\right)} = "
                r"\dfrac{\dfrac{%d}{%d}\cdot\dfrac{%d}{%d}}"
                r"{\dfrac{%d}{%d}} = \dfrac{%d}{%d} = %s$."
                % (a + b, n, a, a + b, a + c, n, a, a + c,
                   _ps(a, a + c)) +
                "\\\\\n"
                r"Trên bảng: trong $%d$ %s ở cột ``%s'' có $%d$ %s "
                r"thuộc nhóm ``%s''." % (a + c, dv, c1, a, dv, h1))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def _de_hai_nguon(hoi=None):
    """Dựng đề hai nguồn, trả về mọi số liệu cần cho cả MC, SA và TL.

    hoi: xem _bo_hai_nguon - câu trả lời ngắn truyền tên đại lượng hỏi.
    """
    n1, n2, d1, d2 = _bo_hai_nguon(hoi)
    bc = random.choice(BOI_CANH_NGUON)
    kho, ten1, ten2, dv, dac_biet, cach_lay = bc
    n, T = n1 + n2, d1 + d2
    dan = (r"%s gồm $%d$ %s, trong đó %s làm $%d$ %s và %s làm $%d$ %s. "
           r"Trong số %s của %s có $%d$ %s %s; trong số %s của %s có "
           r"$%d$ %s %s. Người ta %s."
           % (kho.capitalize(), n, dv, ten1, n1, dv, ten2, n2, dv,
              dv, ten1, d1, dv, dac_biet, dv, ten2, d2, dv, dac_biet,
              cach_lay))
    return n1, n2, d1, d2, n, T, ten1, ten2, dv, dac_biet, dan


def L12_C6_B19_VD057_MC_A_01(socau, dang=1):
    r"""Vận dụng công thức Bayes - biết kết quả, truy ngược về nguồn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon()
        dung = "$%s$" % _ps(d1, T)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _ps(d1, n1), "$%s$" % _ps(n1, n), "$%s$" % _ps(T, n),
             "$%s$" % _ps(d2, T)],
            buoc=lambda k: "$%s$" % _lech(Fraction(d1, T), k))
        debai = (dan + r" Biết %s lấy ra %s, tính xác suất %s đó do %s "
                 r"làm ra." % (dv, db, dv, t1))
        giai = (r"Gọi $A$ là biến cố ``%s lấy ra %s'', $B$ là biến cố "
                r"``%s lấy ra do %s làm ra''."
                % (dv.capitalize(), db, dv.capitalize(), t1) +
                "\\\\\n"
                r"$P\left(B\right) = \dfrac{%d}{%d}$, "
                r"$P\left(A \mid B\right) = \dfrac{%d}{%d}$."
                % (n1, n, d1, n1) +
                "\\\\\n"
                r"Xác suất toàn phần: $P\left(A\right) = "
                r"\dfrac{%d}{%d}\cdot\dfrac{%d}{%d} + "
                r"\dfrac{%d}{%d}\cdot\dfrac{%d}{%d} = \dfrac{%d}{%d}$."
                % (n1, n, d1, n1, n2, n, d2, n2, T, n) +
                "\\\\\n"
                r"Theo công thức Bayes," +
                "\\\\\n"
                r"$P\left(B \mid A\right) = "
                r"\dfrac{P\left(B\right)P\left(A \mid B\right)}"
                r"{P\left(A\right)} = \dfrac{\dfrac{%d}{%d}}"
                r"{\dfrac{%d}{%d}} = \dfrac{%d}{%d} = %s$."
                % (d1, n, T, n, d1, T, _ps(d1, T)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L12_C6_B19_VD057_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - xác suất tính bằng công thức Bayes.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cau = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon("d2T")
        dapso = _ps(d2, T)
        nhieu = _ba_nhieu6(dapso,
                           [_ps(d2, n2), _ps(n2, n), _ps(T, n)],
                           buoc=lambda k: _lech(Fraction(d2, T), k))
        debai = (dan + r" Biết %s lấy ra %s, tính xác suất %s đó do %s "
                 r"làm ra." % (dv, db, dv, t2))
        giai = (r"Tổng số %s %s của cả %s và %s là $%d + %d = %d$."
                % (dv, db, t1, t2, d1, d2, T) +
                "\\\\\n"
                r"Theo công thức Bayes, xác suất cần tìm là tỉ lệ số %s "
                r"%s của %s trên tổng đó:" % (dv, db, t2) +
                "\\\\\n"
                r"$\dfrac{%d}{%d} = %s$." % (d2, T, dapso))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L12_C6_B19_VD057_TL_A_01(socau, dong=1):
    r"""Tự luận - bài toán thực tiễn dùng công thức Bayes (ba ý).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon()
        debai = dan

        hoi_a = (r"Tính xác suất %s lấy ra do %s làm ra." % (dv, t1))
        giai_a = (r"Có $%d$ %s trên tổng $%d$ %s là do %s làm ra."
                  % (n1, dv, n, dv, t1) +
                  "\\\\\n"
                  r"$P = \dfrac{%d}{%d} = %s$." % (n1, n, _ps(n1, n)))

        hoi_b = r"Tính xác suất %s lấy ra %s." % (dv, db)
        giai_b = (r"Theo công thức xác suất toàn phần," +
                  "\\\\\n"
                  r"$P = \dfrac{%d}{%d}\cdot\dfrac{%d}{%d} + "
                  r"\dfrac{%d}{%d}\cdot\dfrac{%d}{%d} = \dfrac{%d}{%d} "
                  r"= %s$." % (n1, n, d1, n1, n2, n, d2, n2, T, n,
                               _ps(T, n)) +
                  "\\\\\n"
                  r"Cũng có thể đếm thẳng: cả lô có $%d + %d = %d$ %s %s "
                  r"trên tổng $%d$." % (d1, d2, T, dv, db, n))

        hoi_c = (r"Biết %s lấy ra %s, tính xác suất %s đó do %s làm ra."
                 % (dv, db, dv, t1))
        giai_c = (r"Theo công thức Bayes," +
                  "\\\\\n"
                  r"$P = \dfrac{\dfrac{%d}{%d}\cdot\dfrac{%d}{%d}}"
                  r"{\dfrac{%d}{%d}} = \dfrac{%d}{%d} = %s$."
                  % (n1, n, d1, n1, T, n, d1, T, _ps(d1, T)) +
                  "\\\\\n"
                  r"Ý nghĩa: trong $%d$ %s %s của cả lô thì có $%d$ %s "
                  r"là của %s." % (T, dv, db, d1, dv, t1))

        ds_abcd = [(hoi_a, r"P = %s" % _ps(n1, n), giai_a),
                   (hoi_b, r"P = %s" % _ps(T, n), giai_b),
                   (hoi_c, r"P = %s" % _ps(d1, T), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L12_C6_B19_VD058_MC_A_01(socau, dang=1):
    r"""Dùng SƠ ĐỒ HÌNH CÂY để tính xác suất - có hình vẽ trong đề.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon()
        hinh = _hinh_cay(t1, t2, n1, n2, d1, d2, "A")
        dung = "$%s$" % _ps(T, n)
        nhieu = _ba_nhieu6(
            dung,
            ["$%s$" % _ps(d1, n1), "$%s$" % _ps(d1, T),
             # loi hay gap: cong thang hai ti le, quen nhan trong so
             "$%s$" % _sai_cong_ti_le(n1, n2, d1, d2),
             "$%s$" % _ps(n1, n)],
            buoc=lambda k: "$%s$" % _lech(Fraction(T, n), k))
        debai = (dan + "\\\\\n" +
                 r"Sơ đồ hình cây bên mô tả phép chọn, trong đó $A$ là "
                 r"biến cố ``%s lấy ra %s''. Tính xác suất %s lấy ra %s."
                 % (dv, db, dv, db))
        giai = (r"Trên sơ đồ, đi theo hai nhánh dẫn tới $A$ rồi cộng "
                r"lại (công thức xác suất toàn phần):" +
                "\\\\\n"
                r"$P\left(A\right) = %s\cdot%s + %s\cdot%s = %s$."
                % (_ps(n1, n), _ps(d1, n1), _ps(n2, n), _ps(d2, n2),
                   _ps(T, n)) +
                "\\\\\n"
                r"Kiểm lại bằng cách đếm: cả lô có $%d + %d = %d$ %s %s "
                r"trên tổng $%d$, cho $\dfrac{%d}{%d} = %s$."
                % (d1, d2, T, dv, db, n, T, n, _ps(T, n)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L12_C6_B19_VD058_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - đọc sơ đồ hình cây để tính xác suất.

    CLAUDE THEM 29/09/2026 - o tra loi ngan muc VD cua chuong 6 truoc
    day BO TRONG. Co Lan kiem tra lai ID va mo ta.
    """
    cau = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon("Tn")
        hinh = _hinh_cay(t1, t2, n1, n2, d1, d2, "A")
        dapso = _ps(T, n)
        nhieu = _ba_nhieu6(dapso,
                           [_ps(d1, n1), _ps(d1, T), _ps(n1, n)],
                           buoc=lambda k: _lech(Fraction(T, n), k))
        debai = (dan + "\\\\\n" +
                 r"Sơ đồ hình cây bên mô tả phép chọn, trong đó $A$ là "
                 r"biến cố ``%s lấy ra %s''. Tính $P\left(A\right)$."
                 % (dv, db))
        giai = (r"Cộng hai nhánh dẫn tới $A$:" +
                "\\\\\n"
                r"$P\left(A\right) = %s\cdot%s + %s\cdot%s = %s$."
                % (_ps(n1, n), _ps(d1, n1), _ps(n2, n), _ps(d2, n2),
                   dapso))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, hinh, 0, 2)
    return cau


def L12_C6_B19_VD058_TL_A_01(socau, dong=1):
    r"""Tự luận - bài toán xác suất dùng sơ đồ hình cây (ba ý).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTN = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon()
        hinh = _hinh_cay(t1, t2, n1, n2, d1, d2, "A")
        debai = (dan + "\\\\\n" +
                 r"Sơ đồ hình cây bên mô tả phép chọn, với $A$ là biến "
                 r"cố ``%s lấy ra %s''." % (dv, db))

        hoi_a = (r"Đọc trên sơ đồ, cho biết xác suất %s lấy ra do %s làm "
                 r"ra và xác suất %s của %s %s."
                 % (dv, t1, dv, t1, db))
        giai_a = (r"Nhánh tầng một dẫn tới %s ghi $%s$, nhánh tầng hai "
                  r"từ %s tới $A$ ghi $%s$."
                  % (t1, _ps(n1, n), t1, _ps(d1, n1)) +
                  "\\\\\n"
                  r"Đó chính là $\dfrac{%d}{%d}$ và $\dfrac{%d}{%d}$."
                  % (n1, n, d1, n1))

        hoi_b = r"Tính $P\left(A\right)$."
        giai_b = (r"Cộng hai nhánh dẫn tới $A$:" +
                  "\\\\\n"
                  r"$P\left(A\right) = %s\cdot%s + %s\cdot%s = "
                  r"\dfrac{%d}{%d} = %s$."
                  % (_ps(n1, n), _ps(d1, n1), _ps(n2, n), _ps(d2, n2),
                     T, n, _ps(T, n)))

        hoi_c = (r"Biết %s lấy ra %s, tính xác suất %s đó do %s làm ra."
                 % (dv, db, dv, t2))
        giai_c = (r"Theo công thức Bayes," +
                  "\\\\\n"
                  r"$P = \dfrac{%s\cdot%s}{%s} = \dfrac{%d}{%d} = %s$."
                  % (_ps(n2, n), _ps(d2, n2), _ps(T, n), d2, T,
                     _ps(d2, T)) +
                  "\\\\\n"
                  r"Ý nghĩa: trong $%d$ %s %s của cả lô thì $%d$ %s là "
                  r"của %s." % (T, dv, db, d2, dv, t2))

        ds_abcd = [(hoi_a, r"%s \text{ và } %s" % (_ps(n1, n), _ps(d1, n1)),
                    giai_a),
                   (hoi_b, r"P\left(A\right) = %s" % _ps(T, n), giai_b),
                   (hoi_c, r"P = %s" % _ps(d2, T), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI (ra theo CHƯƠNG, thang a) NB - b) TH - c) VD - d) VDC)
# =====================================================================

def L12_C6_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - xác suất có điều kiện đọc từ bảng $2\times 2$.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTF = ""
    for _ in range(socau):
        # b = c thi P(B | A) = P(A | B): menh de sai co y o y c) hoa dung.
        while True:
            (a, b, c, d), (nhom, h1, h2, c1, c2, viec, dv), dan, hinh = \
                _de_bang(random.choice(BOI_CANH_BANG))
            if b != c:
                break
        n = a + b + c + d
        # Độc lập khi và chỉ khi P(A | B) = P(A). So sánh CHÍNH XÁC bằng
        # phân số, không so sánh số thập phân đã làm tròn.
        doc_lap = Fraction(a, a + b) == Fraction(a + c, n)

        debai = (dan + "\\\\\n" +
                 r"Chọn ngẫu nhiên một %s trong số đó. Gọi $A$ là biến "
                 r"cố ``%s %s'' và $B$ là biến cố ``%s thuộc nhóm %s''."
                 % (dv, dv.capitalize(), c1.lower(), dv.capitalize(), h1))

        y_d_dung = (
            r"{\True Hai biến cố $A$ và $B$ %s độc lập}"
            % ("" if doc_lap else "không"),
            r"Đúng. $P\left(A \mid B\right) = \dfrac{%d}{%d} = %s$ và "
            r"$P\left(A\right) = \dfrac{%d}{%d} = %s$."
            % (a, a + b, _ps(a, a + b), a + c, n, _ps(a + c, n)) +
            "\\\\\n" +
            (r"Hai số này BẰNG nhau nên biết $B$ xảy ra hay không cũng "
             r"không làm thay đổi xác suất của $A$: hai biến cố độc lập."
             if doc_lap else
             r"Hai số này KHÁC nhau nên việc biết $B$ đã xảy ra làm thay "
             r"đổi xác suất của $A$: hai biến cố không độc lập."))
        y_d_sai = (
            r"{Hai biến cố $A$ và $B$ %s độc lập}"
            % ("không" if doc_lap else ""),
            r"Sai. Phải so sánh $P\left(A \mid B\right) = %s$ với "
            r"$P\left(A\right) = %s$: hai số này %s nhau."
            % (_ps(a, a + b), _ps(a + c, n),
               "bằng" if doc_lap else "khác"))

        ds_abcd = (
            # a) NB - đọc thẳng một tỉ lệ trên bảng
            [
                (r"{\True $P\left(B\right) = %s$}" % _ps(a + b, n),
                 r"Đúng. Nhóm ``%s'' có $%d$ %s trên tổng $%d$, nên "
                 r"$P\left(B\right) = \dfrac{%d}{%d} = %s$."
                 % (h1, a + b, dv, n, a + b, n, _ps(a + b, n))),
                (r"{$P\left(B\right) = %s$}" % _ps(a, n),
                 r"Sai. Đó là xác suất vừa thuộc nhóm ``%s'' vừa %s. "
                 r"$P\left(B\right) = \dfrac{%d}{%d} = %s$."
                 % (h1, c1.lower(), a + b, n, _ps(a + b, n))),
            ],
            # b) TH - một lần dùng định nghĩa xác suất có điều kiện
            [
                (r"{\True $P\left(A \mid B\right) = %s$}" % _ps(a, a + b),
                 r"Đúng. Trong $%d$ %s thuộc nhóm ``%s'' có $%d$ %s %s, "
                 r"nên $P\left(A \mid B\right) = \dfrac{%d}{%d} = %s$."
                 % (a + b, dv, h1, a, dv, c1.lower(), a, a + b,
                    _ps(a, a + b))),
                (r"{$P\left(A \mid B\right) = %s$}" % _ps(a, n),
                 r"Sai. Đó là $P\left(AB\right)$. Khi đã biết $B$ xảy "
                 r"ra thì mẫu số chỉ còn $%d$, cho $%s$."
                 % (a + b, _ps(a, a + b))),
            ],
            # c) VD - đảo chiều điều kiện (công thức Bayes)
            [
                (r"{\True $P\left(B \mid A\right) = %s$}" % _ps(a, a + c),
                 r"Đúng. Đổi chiều điều kiện thì mẫu số là số %s %s, "
                 r"tức $%d$." % (dv, c1.lower(), a + c) +
                 "\\\\\n"
                 r"$P\left(B \mid A\right) = \dfrac{%d}{%d} = %s$."
                 % (a, a + c, _ps(a, a + c))),
                (r"{$P\left(B \mid A\right) = P\left(A \mid B\right)$}",
                 r"Sai. Hai xác suất có điều kiện ngược chiều nhau nói "
                 r"chung KHÁC nhau: $P\left(A \mid B\right) = %s$ còn "
                 r"$P\left(B \mid A\right) = %s$."
                 % (_ps(a, a + b), _ps(a, a + c))),
            ],
            # d) VDC - phải tự kiểm tra tính độc lập
            [y_d_dung, y_d_sai])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF


def _sai_cong_ti_le(n1, n2, d1, d2):
    r"""Lỗi hay gặp: cộng thẳng hai tỉ lệ $d_1/n_1 + d_2/n_2$.

    Hai tỉ lệ đều có mẫu đẹp nên tổng cũng có mẫu đẹp. Nếu vô tình
    trùng với đáp số đúng thì đổi sang $1 - P\left(A\right)$.
    """
    sai = Fraction(d1, n1) + Fraction(d2, n2)
    if sai == Fraction(d1 + d2, n1 + n2):
        sai = 1 - Fraction(d1 + d2, n1 + n2)
    return _ps(sai.numerator, sai.denominator)


def L12_C6_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - công thức xác suất toàn phần và công thức Bayes.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    cauTF = ""
    for _ in range(socau):
        n1, n2, d1, d2, n, T, t1, t2, dv, db, dan = _de_hai_nguon()
        hinh = _hinh_cay(t1, t2, n1, n2, d1, d2, "A")
        debai = (dan + "\\\\\n" +
                 r"Gọi $A$ là biến cố ``%s lấy ra %s'' và $B$ là biến cố "
                 r"``%s lấy ra do %s làm ra''."
                 % (dv.capitalize(), db, dv.capitalize(), t1))

        ds_abcd = (
            # a) NB - đọc một nhánh tầng một của sơ đồ cây
            [
                (r"{\True $P\left(B\right) = %s$}" % _ps(n1, n),
                 r"Đúng. %s làm $%d$ %s trên tổng $%d$, nên "
                 r"$P\left(B\right) = \dfrac{%d}{%d} = %s$."
                 % (t1, n1, dv, n, n1, n, _ps(n1, n))),
                (r"{$P\left(B\right) = %s$}" % _ps(d1, n1),
                 r"Sai. Đó là tỉ lệ %s TRONG SỐ %s của %s, tức "
                 r"$P\left(A \mid B\right)$."
                 % (db, dv, t1)),
            ],
            # b) TH - đọc một nhánh tầng hai
            [
                (r"{\True $P\left(A \mid B\right) = %s$}" % _ps(d1, n1),
                 r"Đúng. Trong $%d$ %s của %s có $%d$ %s %s, cho "
                 r"$\dfrac{%d}{%d} = %s$."
                 % (n1, dv, t1, d1, dv, db, d1, n1, _ps(d1, n1))),
                (r"{$P\left(A \mid B\right) = %s$}" % _ps(d1, T),
                 r"Sai. Đó là tỉ lệ %s của %s trên TỔNG số %s %s của cả "
                 r"lô, tức $P\left(B \mid A\right)$."
                 % (dv, t1, dv, db)),
            ],
            # c) VD - công thức xác suất toàn phần
            [
                (r"{\True $P\left(A\right) = %s$}" % _ps(T, n),
                 r"Đúng. Theo công thức xác suất toàn phần," +
                 "\\\\\n"
                 r"$P\left(A\right) = %s\cdot%s + %s\cdot%s = "
                 r"\dfrac{%d}{%d} = %s$."
                 % (_ps(n1, n), _ps(d1, n1), _ps(n2, n), _ps(d2, n2),
                    T, n, _ps(T, n))),
                (r"{$P\left(A\right) = %s$}" % _sai_cong_ti_le(n1, n2, d1, d2),
                 r"Sai. Không được CỘNG THẲNG hai tỉ lệ $%s$ và $%s$: mỗi "
                 r"tỉ lệ còn phải nhân với xác suất chọn trúng nguồn đó."
                 % (_ps(d1, n1), _ps(d2, n2)) +
                 "\\\\\n"
                 r"Đúng là $P\left(A\right) = %s\cdot%s + %s\cdot%s = %s$."
                 % (_ps(n1, n), _ps(d1, n1), _ps(n2, n), _ps(d2, n2),
                    _ps(T, n))),
            ],
            # d) VDC - công thức Bayes, truy ngược về nguồn
            [
                (r"{\True $P\left(B \mid A\right) = %s$}" % _ps(d1, T),
                 r"Đúng. Theo công thức Bayes," +
                 "\\\\\n"
                 r"$P\left(B \mid A\right) = "
                 r"\dfrac{P\left(B\right)P\left(A \mid B\right)}"
                 r"{P\left(A\right)} = \dfrac{\dfrac{%d}{%d}}"
                 r"{\dfrac{%d}{%d}} = \dfrac{%d}{%d} = %s$."
                 % (d1, n, T, n, d1, T, _ps(d1, T)) +
                 "\\\\\n"
                 r"Ý nghĩa: trong $%d$ %s %s của cả lô thì $%d$ %s là "
                 r"của %s." % (T, dv, db, d1, dv, t1)),
                (r"{$P\left(B \mid A\right) = P\left(A \mid B\right)$}",
                 r"Sai. Đây là hai xác suất ngược chiều nhau: "
                 r"$P\left(A \mid B\right) = %s$ (tỉ lệ %s trong %s của "
                 r"%s), còn $P\left(B \mid A\right) = %s$ (tỉ lệ %s của "
                 r"%s trong toàn bộ %s %s)."
                 % (_ps(d1, n1), db, dv, t1, _ps(d1, T), dv, t1, dv, db)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, hinh, 0, socot)
    return cauTF
