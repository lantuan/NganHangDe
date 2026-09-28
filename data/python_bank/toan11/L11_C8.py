# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 8. Các quy tắc tính xác suất
(bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Kiến thức dùng trong tệp:

  * Biến cố hợp $A \cup B$: "$A$ xảy ra hoặc $B$ xảy ra";
    biến cố giao $A \cap B$ (hay $AB$): "cả $A$ và $B$ cùng xảy ra".
  * Công thức cộng: $P\left(A \cup B\right) = P\left(A\right) +
    P\left(B\right) - P\left(AB\right)$; nếu $A$, $B$ xung khắc thì
    $P\left(A \cup B\right) = P\left(A\right) + P\left(B\right)$.
  * $A$, $B$ độc lập $\Leftrightarrow P\left(AB\right) =
    P\left(A\right)P\left(B\right)$.
  * Biến cố đối: $P\left(\overline{A}\right) = 1 - P\left(A\right)$;
    bài toán "có ít nhất một" nên đi qua biến cố đối.
  * Xác suất cổ điển: $P\left(A\right) =
    \dfrac{n\left(A\right)}{n\left(\Omega\right)}$.

Số liệu chọn để ĐÁP SỐ ĐẸP: mọi xác suất cho trước đều có MỘT chữ số
thập phân nên tích hai xác suất luôn có đúng hai chữ số thập phân; với
bài ba giai đoạn thì bộ số được lọc lại sao cho kết quả vẫn viết được
đúng hai chữ số thập phân (không phải làm tròn). Bài dùng tổ hợp thì
lọc bỏ các trường hợp rơi đúng vào mốc làm tròn $0,xx5$.

Bài học lớp 10 đã áp dụng: chữ tiếng Việt không nằm trần trong $...$;
không dùng **đậm**; mọi chuỗi có dấu gạch chéo đều là r"..."; mọi danh
sách phương án nhiễu đều qua _ba_nhieu8; sơ đồ hình cây vẽ bằng TikZ
THUẦN (MathJax trên web không dựng được tabular).
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


def _ba_nhieu8(dapso, ung_vien, buoc=None):
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


def _ps(f):
    r"""Viết phân số tối giản dạng LaTeX."""
    f = Fraction(f)
    if f.denominator == 1:
        return "%d" % f.numerator
    if f < 0:
        return r"-\dfrac{%d}{%d}" % (-f.numerator, f.denominator)
    return r"\dfrac{%d}{%d}" % (f.numerator, f.denominator)


def _hai_chu_so(f):
    r"""Kiểm tra $f$ viết được đúng bằng hai chữ số thập phân."""
    return (Fraction(f) * 100).denominator == 1


def _xs_mot_chu_so():
    r"""Xác suất có ĐÚNG một chữ số thập phân, tránh $0$ và $1$."""
    return Fraction(random.randint(1, 9), 10)


def _to_hop(n, k):
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def _an_toan_lam_tron(f, n=2):
    r"""Đúng nếu $f$ KHÔNG rơi vào mốc làm tròn (chữ số kế tiếp là $5$ và
    các chữ số sau đều bằng $0$) - để đáp số làm tròn không gây tranh cãi.
    """
    x = Fraction(f) * (10 ** (n + 1))
    if x.denominator != 1:
        return True
    return int(x) % 10 != 5


# Bối cảnh cho bài toán "có ít nhất một" và hai biến cố độc lập.
BOI_CANH_DOC_LAP = [
    (r"Hai xạ thủ cùng bắn vào một mục tiêu một cách độc lập",
     r"xạ thủ thứ nhất bắn trúng", r"xạ thủ thứ hai bắn trúng",
     r"có ít nhất một xạ thủ bắn trúng mục tiêu"),
    (r"Hai học sinh $A$ và $B$ cùng giải một bài toán một cách độc lập",
     r"bạn $A$ giải đúng", r"bạn $B$ giải đúng",
     r"có ít nhất một bạn giải đúng"),
    (r"Hai máy sản xuất hoạt động độc lập với nhau",
     r"máy thứ nhất bị hỏng trong ngày",
     r"máy thứ hai bị hỏng trong ngày",
     r"có ít nhất một máy bị hỏng trong ngày"),
    (r"Hai bóng đèn trong một mạch điện hoạt động độc lập với nhau",
     r"bóng thứ nhất bị cháy trong tháng",
     r"bóng thứ hai bị cháy trong tháng",
     r"có ít nhất một bóng bị cháy trong tháng"),
]


# =====================================================================
# BÀI 28. BIẾN CỐ HỢP, BIẾN CỐ GIAO, BIẾN CỐ ĐỘC LẬP
# =====================================================================

def L11_C8_B28_NB130_MC_A_01(socau, dang=1):
    r"""Nhận biết khái niệm biến cố hợp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"$A$: ``Học sinh được chọn giỏi Toán''",
         r"$B$: ``Học sinh được chọn giỏi Văn''",
         r"Học sinh được chọn giỏi Toán hoặc giỏi Văn",
         r"Học sinh được chọn giỏi cả Toán và Văn",
         r"Học sinh được chọn không giỏi Toán cũng không giỏi Văn",
         r"Học sinh được chọn chỉ giỏi Toán"),
        (r"$A$: ``Xuất hiện mặt chẵn chấm''",
         r"$B$: ``Xuất hiện mặt có số chấm lớn hơn $4$''",
         r"Xuất hiện mặt chẵn chấm hoặc mặt có số chấm lớn hơn $4$",
         r"Xuất hiện mặt chẵn chấm và có số chấm lớn hơn $4$",
         r"Xuất hiện mặt lẻ chấm",
         r"Xuất hiện mặt có số chấm không lớn hơn $4$"),
        (r"$A$: ``Lấy được viên bi màu đỏ''",
         r"$B$: ``Lấy được viên bi màu xanh''",
         r"Lấy được viên bi màu đỏ hoặc màu xanh",
         r"Lấy được viên bi vừa đỏ vừa xanh",
         r"Không lấy được viên bi màu đỏ",
         r"Lấy được viên bi không phải màu đỏ và không phải màu xanh"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(MAU))
        if i not in gt:
            gt.append(i)

    cauTN = ""
    for i in gt:
        mA, mB, dung, n1, n2, n3 = MAU[i]
        debai = (r"Cho hai biến cố %s và %s. Biến cố $A \cup B$ là biến cố"
                 % (mA, mB))
        giai = (r"Biến cố hợp $A \cup B$ xảy ra khi và chỉ khi ÍT NHẤT một "
                r"trong hai biến cố $A$, $B$ xảy ra." +
                "\\\\\n"
                r"Vì vậy $A \cup B$ được mô tả bằng liên từ ``HOẶC'': "
                r"%s." % dung +
                "\\\\\n"
                r"Chú ý ``và'' là biến cố GIAO $A \cap B$, còn ``không'' "
                r"là biến cố ĐỐI.")
        cauTN += MC_SA_answer_text(debai, dung, [n1, n2, n3], giai, 0, 0,
                                   dang)
    return cauTN


def L11_C8_B28_NB131_MC_A_01(socau, dang=1):
    r"""Nhận biết khái niệm biến cố giao.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"$A$: ``Học sinh được chọn chơi bóng đá''",
         r"$B$: ``Học sinh được chọn chơi cầu lông''",
         r"Học sinh được chọn chơi cả bóng đá và cầu lông",
         r"Học sinh được chọn chơi bóng đá hoặc cầu lông",
         r"Học sinh được chọn không chơi môn nào trong hai môn",
         r"Học sinh được chọn chỉ chơi cầu lông"),
        (r"$A$: ``Xuất hiện mặt chẵn chấm''",
         r"$B$: ``Xuất hiện mặt có số chấm chia hết cho $3$''",
         r"Xuất hiện mặt $6$ chấm",
         r"Xuất hiện mặt chẵn chấm hoặc chia hết cho $3$",
         r"Xuất hiện mặt lẻ chấm",
         r"Xuất hiện mặt $2$ chấm hoặc $3$ chấm"),
        (r"$A$: ``Sản phẩm lấy ra đạt tiêu chuẩn về kích thước''",
         r"$B$: ``Sản phẩm lấy ra đạt tiêu chuẩn về khối lượng''",
         r"Sản phẩm lấy ra đạt cả hai tiêu chuẩn",
         r"Sản phẩm lấy ra đạt ít nhất một tiêu chuẩn",
         r"Sản phẩm lấy ra không đạt tiêu chuẩn nào",
         r"Sản phẩm lấy ra chỉ đạt tiêu chuẩn về kích thước"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(MAU))
        if i not in gt:
            gt.append(i)

    cauTN = ""
    for i in gt:
        mA, mB, dung, n1, n2, n3 = MAU[i]
        debai = (r"Cho hai biến cố %s và %s. Biến cố $A \cap B$ là biến cố"
                 % (mA, mB))
        giai = (r"Biến cố giao $A \cap B$ (còn viết là $AB$) xảy ra khi và "
                r"chỉ khi CẢ HAI biến cố $A$ và $B$ cùng xảy ra." +
                "\\\\\n"
                r"Vì vậy $A \cap B$ được mô tả bằng liên từ ``VÀ'': %s."
                % dung +
                "\\\\\n"
                r"Chú ý ``hoặc'' mới là biến cố HỢP $A \cup B$.")
        cauTN += MC_SA_answer_text(debai, dung, [n1, n2, n3], giai, 0, 0,
                                   dang)
    return cauTN


def L11_C8_B28_NB132_MC_A_01(socau, dang=1):
    r"""Nhận biết khái niệm biến cố độc lập.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    MAU = [
        (r"Gieo một đồng xu và một con xúc xắc cân đối",
         r"$A$: ``Đồng xu xuất hiện mặt sấp''",
         r"$B$: ``Xúc xắc xuất hiện mặt $6$ chấm''"),
        (r"Hai xạ thủ bắn vào bia một cách riêng rẽ",
         r"$A$: ``Xạ thủ thứ nhất bắn trúng''",
         r"$B$: ``Xạ thủ thứ hai bắn trúng''"),
        (r"Lấy ngẫu nhiên một viên bi từ hộp thứ nhất và một viên bi từ "
         r"hộp thứ hai",
         r"$A$: ``Viên bi lấy từ hộp thứ nhất màu đỏ''",
         r"$B$: ``Viên bi lấy từ hộp thứ hai màu đỏ''"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(MAU))
        if i not in gt:
            gt.append(i)

    cauTN = ""
    for i in gt:
        boi_canh, mA, mB = MAU[i]
        dung = (r"$A$ và $B$ độc lập, vì việc xảy ra hay không xảy ra của "
                r"biến cố này không làm thay đổi xác suất xảy ra của biến "
                r"cố kia.")
        nhieu = [r"$A$ và $B$ xung khắc, vì chúng không thể cùng xảy ra.",
                 r"$A$ và $B$ đối nhau, vì luôn có đúng một biến cố xảy ra.",
                 r"$A$ và $B$ không độc lập, vì cùng được xét trong một "
                 r"phép thử."]
        debai = (r"%s. Xét hai biến cố %s và %s. Khẳng định nào sau đây "
                 r"ĐÚNG?" % (boi_canh, mA, mB))
        giai = (r"Hai biến cố gọi là ĐỘC LẬP nếu việc xảy ra hay không xảy "
                r"ra của biến cố này không làm thay đổi xác suất xảy ra "
                r"của biến cố kia." +
                "\\\\\n"
                r"Ở đây hai biến cố gắn với hai hành động riêng rẽ, không "
                r"ảnh hưởng lẫn nhau, nên $A$ và $B$ độc lập." +
                "\\\\\n"
                r"Hai biến cố này vẫn có thể CÙNG xảy ra nên không xung "
                r"khắc; và cũng có thể cùng KHÔNG xảy ra nên không đối "
                r"nhau.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _bo_it_nhat_mot():
    r"""$(i, p_1, p_2)$ với $p_1$, $p_2$ có một chữ số thập phân nên
    $1 - \left(1 - p_1\right)\left(1 - p_2\right)$ có đúng hai chữ số."""
    i = random.randrange(len(BOI_CANH_DOC_LAP))
    p1 = _xs_mot_chu_so()
    p2 = _xs_mot_chu_so()
    return i, p1, p2


def L11_C8_B28_VD149_MC_A_01(socau, dang=1):
    r"""Xác suất "có ít nhất một" của hai biến cố độc lập.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_it_nhat_mot()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for i, p1, p2 in gt:
        boi_canh, tenA, tenB, tenC = BOI_CANH_DOC_LAP[i]
        q = (1 - p1) * (1 - p2)
        P = 1 - q
        dung = "$%s$" % _xx(P)
        nhieu = _ba_nhieu8(
            dung,
            ["$%s$" % _xx(p1 * p2), "$%s$" % _xx(p1 + p2),
             "$%s$" % _xx(q)],
            buoc=lambda t: "$%s$" % _xx(float(P) - t / 100.0))
        debai = (r"%s. Xác suất để %s là $%s$, xác suất để %s là $%s$. "
                 r"Tính xác suất để %s."
                 % (boi_canh, tenA, _xx(p1), tenB, _xx(p2), tenC))
        giai = (r"Gọi $A$ là biến cố ``%s'', $B$ là biến cố ``%s''; $A$ và "
                r"$B$ độc lập." % (tenA, tenB) +
                "\\\\\n"
                r"Biến cố cần tính là $C = A \cup B$. Biến cố đối "
                r"$\overline{C} = \overline{A}\,\overline{B}$: cả hai cùng "
                r"KHÔNG xảy ra." +
                "\\\\\n"
                r"$P\left(\overline{A}\right) = 1 - %s = %s$ và "
                r"$P\left(\overline{B}\right) = 1 - %s = %s$."
                % (_xx(p1), _xx(1 - p1), _xx(p2), _xx(1 - p2)) +
                "\\\\\n"
                r"Vì độc lập nên $P\left(\overline{C}\right) = "
                r"%s\cdot %s = %s$."
                % (_xx(1 - p1), _xx(1 - p2), _xx(q)) +
                "\\\\\n"
                r"$P\left(C\right) = 1 - %s = %s$." % (_xx(q), _xx(P)) +
                "\\\\\n"
                r"Chú ý KHÔNG được cộng thẳng $%s + %s$ vì hai biến cố "
                r"không xung khắc." % (_xx(p1), _xx(p2)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C8_B28_VD149_SA_A_01(socau):
    r"""Xác suất "có ít nhất một" - trả lời ngắn (hai chữ số thập phân).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_it_nhat_mot()
        if v not in gt:
            gt.append(v)

    cau = ""
    for i, p1, p2 in gt:
        boi_canh, tenA, tenB, tenC = BOI_CANH_DOC_LAP[i]
        q = (1 - p1) * (1 - p2)
        P = 1 - q
        dapso = _xx(P)
        debai = (r"%s. Xác suất để %s là $%s$, xác suất để %s là $%s$. "
                 r"Tính xác suất để %s."
                 % (boi_canh, tenA, _xx(p1), tenB, _xx(p2), tenC))
        giai = (r"Gọi $A$, $B$ lần lượt là hai biến cố đã cho; chúng độc "
                r"lập với nhau." +
                "\\\\\n"
                r"Biến cố đối của ``%s'' là ``cả hai cùng không xảy ra''."
                % tenC +
                "\\\\\n"
                r"$P\left(\overline{A}\,\overline{B}\right) = "
                r"\left(1 - %s\right)\left(1 - %s\right) = "
                r"%s\cdot %s = %s$."
                % (_xx(p1), _xx(p2), _xx(1 - p1), _xx(1 - p2), _xx(q)) +
                "\\\\\n"
                r"Vậy xác suất cần tìm là $1 - %s = %s$."
                % (_xx(q), dapso))
        nhieu = _ba_nhieu8(dapso,
                           [_xx(p1 * p2), _xx(q), _xx(p1 + p2)],
                           buoc=lambda t: _xx(float(P) - t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C8_B28_VD149_TL_A_01(socau, dong=1):
    r"""Tự luận: biến cố đối và tính độc lập trong bài toán thực tiễn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_it_nhat_mot()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for i, p1, p2 in gt:
        boi_canh, tenA, tenB, tenC = BOI_CANH_DOC_LAP[i]
        q = (1 - p1) * (1 - p2)
        P = 1 - q
        ca_hai = p1 * p2
        debai = (r"%s. Xác suất để %s là $%s$, xác suất để %s là $%s$."
                 % (boi_canh, tenA, _xx(p1), tenB, _xx(p2)))

        hoi_a = (r"Gọi $A$, $B$ là hai biến cố đã cho. Tính "
                 r"$P\left(AB\right)$.")
        giai_a = (r"Hai biến cố $A$, $B$ độc lập nên "
                  r"$P\left(AB\right) = P\left(A\right)P\left(B\right)$." +
                  "\\\\\n"
                  r"$P\left(AB\right) = %s\cdot %s = %s$."
                  % (_xx(p1), _xx(p2), _xx(ca_hai)))

        hoi_b = (r"Tính xác suất để cả hai cùng KHÔNG xảy ra.")
        giai_b = (r"$P\left(\overline{A}\right) = 1 - %s = %s$; "
                  r"$P\left(\overline{B}\right) = 1 - %s = %s$."
                  % (_xx(p1), _xx(1 - p1), _xx(p2), _xx(1 - p2)) +
                  "\\\\\n"
                  r"$\overline{A}$ và $\overline{B}$ cũng độc lập nên "
                  r"$P\left(\overline{A}\,\overline{B}\right) = "
                  r"%s\cdot %s = %s$."
                  % (_xx(1 - p1), _xx(1 - p2), _xx(q)))

        hoi_c = r"Tính xác suất để %s." % tenC
        giai_c = (r"Biến cố ``%s'' chính là $A \cup B$, có biến cố đối là "
                  r"$\overline{A}\,\overline{B}$." % tenC +
                  "\\\\\n"
                  r"$P\left(A \cup B\right) = 1 - "
                  r"P\left(\overline{A}\,\overline{B}\right) = 1 - %s = %s$."
                  % (_xx(q), _xx(P)) +
                  "\\\\\n"
                  r"Kiểm lại bằng công thức cộng: $%s + %s - %s = %s$."
                  % (_xx(p1), _xx(p2), _xx(ca_hai), _xx(P)))

        ds_abcd = [(hoi_a, r"P\left(AB\right) = %s" % _xx(ca_hai), giai_a),
                   (hoi_b, r"P\left(\overline{A}\,\overline{B}\right) = %s"
                    % _xx(q), giai_b),
                   (hoi_c, r"P\left(A \cup B\right) = %s" % _xx(P), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 29. CÔNG THỨC CỘNG XÁC SUẤT
# =====================================================================

BOI_CANH_CONG = [
    (r"lớp", r"học sinh", r"giỏi môn Toán", r"giỏi môn Ngữ văn",
     r"giỏi ít nhất một trong hai môn"),
    (r"câu lạc bộ", r"thành viên", r"biết chơi cờ vua",
     r"biết chơi cầu lông", r"biết chơi ít nhất một trong hai môn"),
    (r"tổ dân phố", r"hộ gia đình", r"có đăng kí báo giấy",
     r"có đăng kí truyền hình cáp",
     r"có đăng kí ít nhất một trong hai dịch vụ"),
    (r"nhóm", r"khách hàng", r"đã từng mua sản phẩm $X$",
     r"đã từng mua sản phẩm $Y$",
     r"đã từng mua ít nhất một trong hai sản phẩm"),
]


def _bo_cong_xac_suat():
    r"""$(i, n, a, b, c)$: $n$ phần tử, $a$ có tính chất $A$, $b$ có tính
    chất $B$, $c$ có cả hai; mọi xác suất đều viết đúng hai chữ số."""
    for _ in range(400):
        i = random.randrange(len(BOI_CANH_CONG))
        n = random.choice([20, 25, 40, 50])
        a = random.randint(n // 4, n // 2)
        b = random.randint(n // 4, n // 2)
        c = random.randint(1, min(a, b) - 1) if min(a, b) > 1 else 0
        if c == 0 or a + b - c > n:
            continue
        if not all(_hai_chu_so(Fraction(t, n)) for t in (a, b, c,
                                                         a + b - c)):
            continue
        return i, n, a, b, c
    return None


def L11_C8_B29_TH133_MC_A_01(socau, dang=1):
    r"""Xác suất của biến cố hợp bằng công thức cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_cong_xac_suat()
        if v is not None and v not in gt:
            gt.append(v)

    cauTN = ""
    for i, n, a, b, c in gt:
        ten_nhom, ten_pt, tcA, tcB, tcC = BOI_CANH_CONG[i]
        pa, pb, pc = Fraction(a, n), Fraction(b, n), Fraction(c, n)
        P = pa + pb - pc
        dung = "$%s$" % _xx(P)
        nhieu = _ba_nhieu8(
            dung,
            ["$%s$" % _xx(pa + pb), "$%s$" % _xx(pa * pb),
             "$%s$" % _xx(pc)],
            buoc=lambda t: "$%s$" % _xx(float(P) - t / 100.0))
        debai = (r"Một %s có $%d$ %s, trong đó có $%d$ %s %s, $%d$ %s %s "
                 r"và $%d$ %s vừa %s vừa %s. Chọn ngẫu nhiên một %s. Tính "
                 r"xác suất để %s đó %s."
                 % (ten_nhom, n, ten_pt, a, ten_pt, tcA, b, ten_pt, tcB,
                    c, ten_pt, tcA, tcB, ten_pt, ten_pt, tcC))
        giai = (r"Gọi $A$ là biến cố ``%s được chọn %s'', $B$ là biến cố "
                r"``%s được chọn %s''." % (ten_pt, tcA, ten_pt, tcB) +
                "\\\\\n"
                r"$P\left(A\right) = \dfrac{%d}{%d} = %s$; "
                r"$P\left(B\right) = \dfrac{%d}{%d} = %s$; "
                r"$P\left(AB\right) = \dfrac{%d}{%d} = %s$."
                % (a, n, _xx(pa), b, n, _xx(pb), c, n, _xx(pc)) +
                "\\\\\n"
                r"Hai biến cố này KHÔNG xung khắc (có $%d$ %s có cả "
                r"hai tính chất) nên phải dùng công thức cộng đầy đủ:"
                % (c, ten_pt) +
                "\\\\\n"
                r"$P\left(A \cup B\right) = P\left(A\right) + "
                r"P\left(B\right) - P\left(AB\right) = %s + %s - %s = %s$."
                % (_xx(pa), _xx(pb), _xx(pc), _xx(P)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C8_B29_TH133_SA_A_01(socau):
    r"""Xác suất của biến cố hợp - trả lời ngắn (hai chữ số thập phân).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_cong_xac_suat()
        if v is not None and v not in gt:
            gt.append(v)

    cau = ""
    for i, n, a, b, c in gt:
        ten_nhom, ten_pt, tcA, tcB, tcC = BOI_CANH_CONG[i]
        pa, pb, pc = Fraction(a, n), Fraction(b, n), Fraction(c, n)
        P = pa + pb - pc
        dapso = _xx(P)
        debai = (r"Một %s có $%d$ %s, trong đó có $%d$ %s %s, $%d$ %s %s "
                 r"và $%d$ %s có cả hai tính chất trên. Chọn ngẫu nhiên "
                 r"một %s. Tính xác suất để %s đó %s."
                 % (ten_nhom, n, ten_pt, a, ten_pt, tcA, b, ten_pt, tcB,
                    c, ten_pt, ten_pt, ten_pt, tcC))
        giai = (r"$P\left(A\right) = \dfrac{%d}{%d} = %s$, "
                r"$P\left(B\right) = \dfrac{%d}{%d} = %s$, "
                r"$P\left(AB\right) = \dfrac{%d}{%d} = %s$."
                % (a, n, _xx(pa), b, n, _xx(pb), c, n, _xx(pc)) +
                "\\\\\n"
                r"$P\left(A \cup B\right) = %s + %s - %s = %s$."
                % (_xx(pa), _xx(pb), _xx(pc), dapso) +
                "\\\\\n"
                r"Cách khác: số %s %s là $%d + %d - %d = %d$, nên xác "
                r"suất là $\dfrac{%d}{%d} = %s$."
                % (ten_pt, tcC, a, b, c, a + b - c, a + b - c, n, dapso))
        nhieu = _ba_nhieu8(dapso, [_xx(pa + pb), _xx(pc), _xx(pa * pb)],
                           buoc=lambda t: _xx(float(P) - t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C8_B29_VD150_MC_A_01(socau, dang=1):
    r"""Công thức cộng cho hai biến cố không xung khắc - bài toán thực tiễn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p1 = _xs_mot_chu_so()
        p2 = _xs_mot_chu_so()
        pc = Fraction(random.randint(1, 9), 10) * Fraction(1, 1)
        pc = min(p1, p2) - Fraction(random.randint(0, 2), 10)
        if pc <= 0 or p1 + p2 - pc > 1:
            continue
        v = (p1, p2, pc)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for p1, p2, pc in gt:
        P = p1 + p2 - pc
        dung = "$%s$" % _xx(P)
        nhieu = _ba_nhieu8(
            dung,
            ["$%s$" % _xx(p1 + p2), "$%s$" % _xx(p1 * p2), "$%s$" % _xx(pc)],
            buoc=lambda t: "$%s$" % _xx(float(P) - t / 100.0))
        debai = (r"Một nhà máy có hai dây chuyền sản xuất. Xác suất để dây "
                 r"chuyền thứ nhất hoạt động trong ngày là $%s$, xác suất "
                 r"để dây chuyền thứ hai hoạt động là $%s$, xác suất để cả "
                 r"hai dây chuyền cùng hoạt động là $%s$. Tính xác suất để "
                 r"có ít nhất một dây chuyền hoạt động trong ngày."
                 % (_xx(p1), _xx(p2), _xx(pc)))
        giai = (r"Gọi $A$, $B$ lần lượt là biến cố dây chuyền thứ nhất, "
                r"thứ hai hoạt động." +
                "\\\\\n"
                r"Biến cố cần tính là $A \cup B$." +
                "\\\\\n"
                r"Vì $P\left(AB\right) = %s \neq 0$ nên $A$ và $B$ KHÔNG "
                r"xung khắc, phải trừ đi phần chung:" % _xx(pc) +
                "\\\\\n"
                r"$P\left(A \cup B\right) = P\left(A\right) + "
                r"P\left(B\right) - P\left(AB\right) = %s + %s - %s = %s$."
                % (_xx(p1), _xx(p2), _xx(pc), _xx(P)) +
                "\\\\\n"
                r"Nếu cộng thẳng $%s + %s = %s$ thì phần cả hai cùng hoạt "
                r"động đã bị đếm HAI lần."
                % (_xx(p1), _xx(p2), _xx(p1 + p2)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C8_B29_VD150_SA_A_01(socau):
    r"""Xác suất biến cố hợp trong bài toán thực tiễn - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p1 = _xs_mot_chu_so()
        p2 = _xs_mot_chu_so()
        pc = min(p1, p2) - Fraction(random.randint(0, 2), 10)
        if pc <= 0 or p1 + p2 - pc > 1:
            continue
        v = (p1, p2, pc)
        if v not in gt:
            gt.append(v)

    cau = ""
    for p1, p2, pc in gt:
        P = p1 + p2 - pc
        dapso = _xx(P)
        debai = (r"Trong một khu phố, xác suất để một hộ gia đình được "
                 r"chọn ngẫu nhiên có mua bảo hiểm y tế là $%s$, có mua "
                 r"bảo hiểm xe máy là $%s$, mua cả hai loại là $%s$. Tính "
                 r"xác suất để hộ đó mua ít nhất một loại bảo hiểm."
                 % (_xx(p1), _xx(p2), _xx(pc)))
        giai = (r"Gọi $A$: ``hộ đó mua bảo hiểm y tế'', $B$: ``hộ đó mua "
                r"bảo hiểm xe máy''." +
                "\\\\\n"
                r"Biến cố ``mua ít nhất một loại'' là $A \cup B$." +
                "\\\\\n"
                r"$P\left(A \cup B\right) = P\left(A\right) + "
                r"P\left(B\right) - P\left(AB\right) = %s + %s - %s = %s$."
                % (_xx(p1), _xx(p2), _xx(pc), dapso))
        nhieu = _ba_nhieu8(dapso, [_xx(p1 + p2), _xx(pc), _xx(p1 * p2)],
                           buoc=lambda t: _xx(float(P) - t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C8_B29_VD150_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán thực tiễn dùng công thức cộng xác suất.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_cong_xac_suat()
        if v is not None and v not in gt:
            gt.append(v)

    cauTN = ""
    for i, n, a, b, c in gt:
        ten_nhom, ten_pt, tcA, tcB, tcC = BOI_CANH_CONG[i]
        pa, pb, pc = Fraction(a, n), Fraction(b, n), Fraction(c, n)
        P = pa + pb - pc
        khong = 1 - P
        debai = (r"Một %s có $%d$ %s, trong đó có $%d$ %s %s, $%d$ %s %s "
                 r"và $%d$ %s có cả hai tính chất trên. Chọn ngẫu nhiên "
                 r"một %s trong %s đó."
                 % (ten_nhom, n, ten_pt, a, ten_pt, tcA, b, ten_pt, tcB,
                    c, ten_pt, ten_pt, ten_nhom))

        hoi_a = (r"Gọi $A$, $B$ là hai biến cố ứng với hai tính chất trên. "
                 r"Tính $P\left(A\right)$, $P\left(B\right)$, "
                 r"$P\left(AB\right)$.")
        giai_a = (r"$P\left(A\right) = \dfrac{%d}{%d} = %s$, "
                  r"$P\left(B\right) = \dfrac{%d}{%d} = %s$, "
                  r"$P\left(AB\right) = \dfrac{%d}{%d} = %s$."
                  % (a, n, _xx(pa), b, n, _xx(pb), c, n, _xx(pc)))

        hoi_b = r"Tính xác suất để %s được chọn %s." % (ten_pt, tcC)
        giai_b = (r"Biến cố cần tính là $A \cup B$; hai biến cố không xung "
                  r"khắc nên" +
                  "\\\\\n"
                  r"$P\left(A \cup B\right) = %s + %s - %s = %s$."
                  % (_xx(pa), _xx(pb), _xx(pc), _xx(P)) +
                  "\\\\\n"
                  r"Kiểm lại: số %s thoả mãn là $%d + %d - %d = %d$, xác "
                  r"suất $\dfrac{%d}{%d} = %s$."
                  % (ten_pt, a, b, c, a + b - c, a + b - c, n, _xx(P)))

        hoi_c = (r"Tính xác suất để %s được chọn KHÔNG có tính chất nào "
                 r"trong hai tính chất trên." % ten_pt)
        giai_c = (r"Biến cố này là biến cố đối của $A \cup B$." +
                  "\\\\\n"
                  r"$P\left(\overline{A \cup B}\right) = 1 - "
                  r"P\left(A \cup B\right) = 1 - %s = %s$."
                  % (_xx(P), _xx(khong)) +
                  "\\\\\n"
                  r"Kiểm lại: số %s không có tính chất nào là "
                  r"$%d - %d = %d$." % (ten_pt, n, a + b - c,
                                        n - (a + b - c)))

        ds_abcd = [(hoi_a, r"P\left(A\right) = %s,\ P\left(B\right) = %s,"
                    r"\ P\left(AB\right) = %s"
                    % (_xx(pa), _xx(pb), _xx(pc)), giai_a),
                   (hoi_b, r"P\left(A \cup B\right) = %s" % _xx(P), giai_b),
                   (hoi_c, r"P\left(\overline{A \cup B}\right) = %s"
                    % _xx(khong), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 30. CÔNG THỨC NHÂN XÁC SUẤT. PHƯƠNG PHÁP TỔ HỢP VÀ SƠ ĐỒ HÌNH CÂY
# =====================================================================

def _hinh_cay(nhan1, p1, nhan2, p2):
    r"""Sơ đồ hình cây hai tầng, vẽ bằng TikZ THUẦN.

    nhan1, nhan2: tên hai biến cố ở tầng 1 và tầng 2 (chuỗi LaTeX ngắn).
    p1, p2: xác suất nhánh "có xảy ra" ở tầng 1 và tầng 2.
    """
    q1, q2 = 1 - p1, 1 - p2
    ra = ["\\begin{tikzpicture}[>=stealth,x=1cm,y=0.9cm,thick,"
          "line join=round,font=\\footnotesize]"]
    ra.append("\\node (O) at (0,0) {};")
    ra.append("\\fill[black] (0,0) circle[radius=1.8pt];")
    # tang 1
    ra.append("\\draw[->] (0,0) -- (2,2) node[midway,above left]"
              "{$%s$};" % _xx(p1))
    ra.append("\\draw[->] (0,0) -- (2,-2) node[midway,below left]"
              "{$%s$};" % _xx(q1))
    ra.append("\\node[right] at (2,2) {$%s$};" % nhan1)
    ra.append("\\node[right] at (2,-2) {$\\overline{%s}$};" % nhan1)
    # tang 2 - nhanh tren
    ra.append("\\draw[->] (2.75,2) -- (4.75,3) node[midway,above]"
              "{$%s$};" % _xx(p2))
    ra.append("\\draw[->] (2.75,2) -- (4.75,1) node[midway,below]"
              "{$%s$};" % _xx(q2))
    ra.append("\\node[right] at (4.75,3) {$%s$};" % nhan2)
    ra.append("\\node[right] at (4.75,1) {$\\overline{%s}$};" % nhan2)
    # tang 2 - nhanh duoi
    ra.append("\\draw[->] (2.75,-2) -- (4.75,-1) node[midway,above]"
              "{$%s$};" % _xx(p2))
    ra.append("\\draw[->] (2.75,-2) -- (4.75,-3) node[midway,below]"
              "{$%s$};" % _xx(q2))
    ra.append("\\node[right] at (4.75,-1) {$%s$};" % nhan2)
    ra.append("\\node[right] at (4.75,-3) {$\\overline{%s}$};" % nhan2)
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


def L11_C8_B30_TH134_MC_A_01(socau, dang=1):
    r"""Xác suất của biến cố giao bằng công thức nhân.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_it_nhat_mot()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for i, p1, p2 in gt:
        boi_canh, tenA, tenB, _ = BOI_CANH_DOC_LAP[i]
        P = p1 * p2
        dung = "$%s$" % _xx(P)
        nhieu = _ba_nhieu8(
            dung,
            ["$%s$" % _xx(p1 + p2), "$%s$" % _xx(1 - (1 - p1) * (1 - p2)),
             "$%s$" % _xx((1 - p1) * (1 - p2))],
            buoc=lambda t: "$%s$" % _xx(float(P) + t / 100.0))
        debai = (r"%s. Xác suất để %s là $%s$, xác suất để %s là $%s$. "
                 r"Tính xác suất để CẢ HAI cùng xảy ra."
                 % (boi_canh, tenA, _xx(p1), tenB, _xx(p2)))
        giai = (r"Gọi $A$: ``%s'', $B$: ``%s''; hai biến cố này độc lập."
                % (tenA, tenB) +
                "\\\\\n"
                r"Biến cố ``cả hai cùng xảy ra'' là biến cố giao $AB$." +
                "\\\\\n"
                r"Áp dụng công thức nhân cho hai biến cố độc lập:" +
                "\\\\\n"
                r"$P\left(AB\right) = P\left(A\right)P\left(B\right) = "
                r"%s\cdot %s = %s$." % (_xx(p1), _xx(p2), _xx(P)) +
                "\\\\\n"
                r"Chú ý công thức nhân chỉ dùng được khi hai biến cố ĐỘC "
                r"LẬP.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C8_B30_TH134_SA_A_01(socau):
    r"""Xác suất của biến cố giao - trả lời ngắn (hai chữ số thập phân).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_it_nhat_mot()
        if v not in gt:
            gt.append(v)

    cau = ""
    for i, p1, p2 in gt:
        boi_canh, tenA, tenB, _ = BOI_CANH_DOC_LAP[i]
        P = p1 * p2
        dapso = _xx(P)
        debai = (r"%s. Xác suất để %s là $%s$, xác suất để %s là $%s$. "
                 r"Tính xác suất để cả hai cùng xảy ra."
                 % (boi_canh, tenA, _xx(p1), tenB, _xx(p2)))
        giai = (r"Hai biến cố $A$, $B$ độc lập nên áp dụng công thức "
                r"nhân:" +
                "\\\\\n"
                r"$P\left(AB\right) = P\left(A\right)P\left(B\right) = "
                r"%s\cdot %s = %s$." % (_xx(p1), _xx(p2), dapso))
        nhieu = _ba_nhieu8(dapso,
                           [_xx(p1 + p2), _xx((1 - p1) * (1 - p2)),
                            _xx(1 - (1 - p1) * (1 - p2))],
                           buoc=lambda t: _xx(float(P) + t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def _bo_to_hop():
    r"""$(d, x, k, j)$: hộp có $d$ bi đỏ, $x$ bi xanh, lấy $k$ bi, hỏi
    xác suất lấy được đúng $j$ bi đỏ; lọc để đáp số làm tròn không
    rơi vào mốc $0,xx5$."""
    for _ in range(500):
        d = random.randint(3, 7)
        x = random.randint(3, 7)
        k = random.choice([2, 3])
        # 1 <= j <= k-1 de cau hoi luon la HON HOP hai mau, tranh viet
        # C_x^0 trong loi giai.
        j = random.randint(1, k - 1)
        if j > d or k - j > x:
            continue
        P = Fraction(_to_hop(d, j) * _to_hop(x, k - j), _to_hop(d + x, k))
        if P == 0 or P == 1 or not _an_toan_lam_tron(P):
            continue
        return d, x, k, j, P
    return None


def L11_C8_B30_TH135_MC_A_01(socau, dang=1):
    r"""Tính xác suất bằng phương pháp tổ hợp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_to_hop()
        if v is not None and v not in gt:
            gt.append(v)

    cauTN = ""
    for d, x, k, j, P in gt:
        n_omega = _to_hop(d + x, k)
        n_A = _to_hop(d, j) * _to_hop(x, k - j)
        dung = "$%s$" % _ps(P)
        nhieu = _ba_nhieu8(
            dung,
            [r"$\dfrac{%d}{%d}$" % (n_A, d + x),
             r"$\dfrac{%d}{%d}$" % (_to_hop(d, j), n_omega),
             r"$\dfrac{%d}{%d}$" % (j, k)],
            buoc=lambda t: r"$\dfrac{%d}{%d}$" % (n_A + t, n_omega))
        debai = (r"Một hộp có $%d$ viên bi đỏ và $%d$ viên bi xanh (các "
                 r"viên bi đôi một khác nhau). Lấy ngẫu nhiên đồng thời "
                 r"$%d$ viên bi. Tính xác suất để lấy được đúng $%d$ viên "
                 r"bi đỏ." % (d, x, k, j))
        giai = (r"Số phần tử của không gian mẫu: "
                r"$n\left(\Omega\right) = C_{%d}^{%d} = %d$."
                % (d + x, k, n_omega) +
                "\\\\\n"
                r"Chọn $%d$ bi đỏ trong $%d$ bi đỏ: $C_{%d}^{%d} = %d$ "
                r"cách." % (j, d, d, j, _to_hop(d, j)) +
                "\\\\\n"
                r"Chọn $%d$ bi xanh trong $%d$ bi xanh: $C_{%d}^{%d} = %d$ "
                r"cách." % (k - j, x, x, k - j, _to_hop(x, k - j)) +
                "\\\\\n"
                r"Theo quy tắc nhân: $n\left(A\right) = %d\cdot %d = %d$."
                % (_to_hop(d, j), _to_hop(x, k - j), n_A) +
                "\\\\\n"
                r"$P\left(A\right) = \dfrac{%d}{%d} = %s$."
                % (n_A, n_omega, _ps(P)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C8_B30_TH135_SA_A_01(socau):
    r"""Xác suất tính bằng tổ hợp - trả lời ngắn (hai chữ số thập phân).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_to_hop()
        if v is not None and v not in gt:
            gt.append(v)

    cau = ""
    for d, x, k, j, P in gt:
        n_omega = _to_hop(d + x, k)
        n_A = _to_hop(d, j) * _to_hop(x, k - j)
        dapso = _xx(P)
        debai = (r"Một hộp có $%d$ viên bi đỏ và $%d$ viên bi xanh (các "
                 r"viên bi đôi một khác nhau). Lấy ngẫu nhiên đồng thời "
                 r"$%d$ viên bi. Tính xác suất để lấy được đúng $%d$ viên "
                 r"bi đỏ (làm tròn đến hàng phần trăm)." % (d, x, k, j))
        giai = (r"$n\left(\Omega\right) = C_{%d}^{%d} = %d$."
                % (d + x, k, n_omega) +
                "\\\\\n"
                r"$n\left(A\right) = C_{%d}^{%d}\cdot C_{%d}^{%d} = "
                r"%d\cdot %d = %d$."
                % (d, j, x, k - j, _to_hop(d, j), _to_hop(x, k - j), n_A) +
                "\\\\\n"
                r"$P\left(A\right) = \dfrac{%d}{%d}%s \approx %s$."
                % (n_A, n_omega,
                   ("" if _ps(P) == r"\dfrac{%d}{%d}" % (n_A, n_omega)
                    else " = %s" % _ps(P)), dapso))
        nhieu = _ba_nhieu8(dapso,
                           [_xx(Fraction(n_A, d + x)),
                            _xx(Fraction(_to_hop(d, j), n_omega)),
                            _xx(1 - P)],
                           buoc=lambda t: _xx(float(P) + t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C8_B30_TH135_TL_A_01(socau, dong=1):
    r"""Tự luận: bài toán xác suất dùng tổ hợp.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        d = random.randint(4, 7)
        x = random.randint(4, 7)
        k = 3
        if (d, x, k) not in gt:
            gt.append((d, x, k))

    cauTN = ""
    for d, x, k in gt:
        n_omega = _to_hop(d + x, k)
        n_3do = _to_hop(d, 3)
        P3 = Fraction(n_3do, n_omega)
        n_khong = _to_hop(x, 3)
        P_it1 = 1 - Fraction(n_khong, n_omega)
        n_2do = _to_hop(d, 2) * _to_hop(x, 1)
        P2 = Fraction(n_2do, n_omega)
        debai = (r"Một hộp có $%d$ viên bi đỏ và $%d$ viên bi xanh (các "
                 r"viên bi đôi một khác nhau). Lấy ngẫu nhiên đồng thời "
                 r"$%d$ viên bi." % (d, x, k))

        hoi_a = r"Tính số phần tử của không gian mẫu."
        giai_a = (r"Mỗi kết quả là một cách chọn $%d$ viên bi trong "
                  r"$%d$ viên, không kể thứ tự." % (k, d + x) +
                  "\\\\\n"
                  r"$n\left(\Omega\right) = C_{%d}^{%d} = %d$."
                  % (d + x, k, n_omega))

        hoi_b = r"Tính xác suất để lấy được $3$ viên bi cùng màu đỏ."
        giai_b = (r"Số cách chọn $3$ bi đỏ: $C_{%d}^{3} = %d$."
                  % (d, n_3do) +
                  "\\\\\n"
                  r"$P = \dfrac{%d}{%d} = %s \approx %s$."
                  % (n_3do, n_omega, _ps(P3), _xx(P3)))

        hoi_c = r"Tính xác suất để lấy được ít nhất một viên bi đỏ."
        giai_c = (r"Biến cố đối là ``không lấy được viên bi đỏ nào'', tức "
                  r"là cả $3$ viên đều xanh." +
                  "\\\\\n"
                  r"Số cách: $C_{%d}^{3} = %d$, nên xác suất biến cố đối "
                  r"là $\dfrac{%d}{%d}$." % (x, n_khong, n_khong, n_omega) +
                  "\\\\\n"
                  r"$P = 1 - \dfrac{%d}{%d} = %s \approx %s$."
                  % (n_khong, n_omega, _ps(P_it1), _xx(P_it1)) +
                  "\\\\\n"
                  r"(Nếu cộng trực tiếp thì phải tính ba trường hợp $1$, "
                  r"$2$, $3$ bi đỏ - dùng biến cố đối gọn hơn nhiều.)")

        ds_abcd = [(hoi_a, r"n\left(\Omega\right) = %d" % n_omega, giai_a),
                   (hoi_b, r"P = %s" % _ps(P3), giai_b),
                   (hoi_c, r"P = %s" % _ps(P_it1), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L11_C8_B30_TH136_MC_A_01(socau, dang=1):
    r"""Tính xác suất bằng sơ đồ hình cây (có hình).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p1 = _xs_mot_chu_so()
        p2 = _xs_mot_chu_so()
        if (p1, p2) not in gt:
            gt.append((p1, p2))

    cauTN = ""
    for p1, p2 in gt:
        P = p1 * (1 - p2)
        hinh = _hinh_cay("A", p1, "B", p2)
        dung = "$%s$" % _xx(P)
        nhieu = _ba_nhieu8(
            dung,
            ["$%s$" % _xx(p1 * p2), "$%s$" % _xx((1 - p1) * p2),
             "$%s$" % _xx((1 - p1) * (1 - p2))],
            buoc=lambda t: "$%s$" % _xx(float(P) + t / 100.0))
        debai = (r"Một học sinh lần lượt làm hai bài kiểm tra một cách độc "
                 r"lập. Gọi $A$ là biến cố ``đạt bài thứ nhất'', $B$ là "
                 r"biến cố ``đạt bài thứ hai''. Sơ đồ hình cây của phép "
                 r"thử được cho như hình vẽ. Tính xác suất để học sinh đó "
                 r"đạt bài thứ nhất nhưng KHÔNG đạt bài thứ hai.")
        giai = (r"Biến cố cần tính ứng với NHÁNH đi qua $A$ rồi "
                r"$\overline{B}$ trên sơ đồ hình cây." +
                "\\\\\n"
                r"Xác suất của một nhánh bằng TÍCH các xác suất ghi trên "
                r"nhánh đó." +
                "\\\\\n"
                r"$P\left(A\,\overline{B}\right) = P\left(A\right)\cdot "
                r"P\left(\overline{B}\right) = %s\cdot %s = %s$."
                % (_xx(p1), _xx(1 - p2), _xx(P)) +
                "\\\\\n"
                r"Kiểm lại: tổng xác suất của bốn nhánh bằng "
                r"$%s + %s + %s + %s = 1$."
                % (_xx(p1 * p2), _xx(P), _xx((1 - p1) * p2),
                   _xx((1 - p1) * (1 - p2))))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L11_C8_B30_TH136_SA_A_01(socau):
    r"""Xác suất tính bằng sơ đồ hình cây - trả lời ngắn (có hình).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        p1 = _xs_mot_chu_so()
        p2 = _xs_mot_chu_so()
        if (p1, p2) not in gt:
            gt.append((p1, p2))

    cau = ""
    for p1, p2 in gt:
        # dung dung MOT trong hai bai
        P = p1 * (1 - p2) + (1 - p1) * p2
        hinh = _hinh_cay("A", p1, "B", p2)
        dapso = _xx(P)
        debai = (r"Một học sinh lần lượt làm hai bài kiểm tra một cách độc "
                 r"lập. Gọi $A$ là biến cố ``đạt bài thứ nhất'', $B$ là "
                 r"biến cố ``đạt bài thứ hai'', với sơ đồ hình cây như "
                 r"hình vẽ. Tính xác suất để học sinh đó đạt ĐÚNG MỘT "
                 r"trong hai bài.")
        giai = (r"``Đạt đúng một bài'' ứng với HAI nhánh của sơ đồ: "
                r"$A\,\overline{B}$ và $\overline{A}\,B$." +
                "\\\\\n"
                r"$P\left(A\,\overline{B}\right) = %s\cdot %s = %s$."
                % (_xx(p1), _xx(1 - p2), _xx(p1 * (1 - p2))) +
                "\\\\\n"
                r"$P\left(\overline{A}\,B\right) = %s\cdot %s = %s$."
                % (_xx(1 - p1), _xx(p2), _xx((1 - p1) * p2)) +
                "\\\\\n"
                r"Hai nhánh này XUNG KHẮC nên cộng xác suất:" +
                "\\\\\n"
                r"$P = %s + %s = %s$."
                % (_xx(p1 * (1 - p2)), _xx((1 - p1) * p2), dapso))
        nhieu = _ba_nhieu8(dapso,
                           [_xx(p1 * p2), _xx(p1 * (1 - p2)),
                            _xx((1 - p1) * (1 - p2))],
                           buoc=lambda t: _xx(float(P) + t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, hinh, 0, 2)
    return cau


def _bo_ba_giai_doan():
    r"""$(p_1, p_2, p_3)$ mỗi số có một chữ số thập phân và tích ba số
    viết được đúng HAI chữ số thập phân (không phải làm tròn)."""
    for _ in range(800):
        p1 = _xs_mot_chu_so()
        p2 = _xs_mot_chu_so()
        p3 = _xs_mot_chu_so()
        if p1 * p2 * p3 == 0:
            continue
        if _hai_chu_so(p1 * p2 * p3) and _hai_chu_so(
                (1 - p1) * (1 - p2) * (1 - p3)):
            return p1, p2, p3
    return Fraction(5, 10), Fraction(4, 10), Fraction(5, 10)


def L11_C8_B30_VD151_MC_A_01(socau, dang=1):
    r"""Xác suất qua nhiều giai đoạn độc lập.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_ba_giai_doan()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for p1, p2, p3 in gt:
        P = p1 * p2 * p3
        dung = "$%s$" % _xx(P)
        nhieu = _ba_nhieu8(
            dung,
            ["$%s$" % _xx(p1 + p2 + p3),
             "$%s$" % _xx(1 - (1 - p1) * (1 - p2) * (1 - p3)),
             "$%s$" % _xx((1 - p1) * (1 - p2) * (1 - p3))],
            buoc=lambda t: "$%s$" % _xx(float(P) + t / 100.0))
        debai = (r"Một sản phẩm phải đi qua ba công đoạn kiểm tra độc lập "
                 r"nhau. Xác suất để sản phẩm đạt ở công đoạn thứ nhất, "
                 r"thứ hai, thứ ba lần lượt là $%s$, $%s$, $%s$. Tính xác "
                 r"suất để sản phẩm đạt cả ba công đoạn."
                 % (_xx(p1), _xx(p2), _xx(p3)))
        giai = (r"Gọi $A_1$, $A_2$, $A_3$ là các biến cố sản phẩm đạt ở "
                r"công đoạn thứ nhất, thứ hai, thứ ba; ba biến cố này độc "
                r"lập." +
                "\\\\\n"
                r"Biến cố cần tính là $A_1A_2A_3$; trên sơ đồ hình cây đó "
                r"là nhánh đi qua cả ba lần ``đạt''." +
                "\\\\\n"
                r"$P\left(A_1A_2A_3\right) = P\left(A_1\right)"
                r"P\left(A_2\right)P\left(A_3\right) = "
                r"%s\cdot %s\cdot %s = %s$."
                % (_xx(p1), _xx(p2), _xx(p3), _xx(P)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C8_B30_VD151_SA_A_01(socau):
    r"""Xác suất qua sơ đồ hình cây nhiều tầng - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_ba_giai_doan()
        if v not in gt:
            gt.append(v)

    cau = ""
    for p1, p2, p3 in gt:
        q = (1 - p1) * (1 - p2) * (1 - p3)
        P = 1 - q
        dapso = _xx(P)
        debai = (r"Ba máy hoạt động độc lập với nhau. Xác suất để máy thứ "
                 r"nhất, thứ hai, thứ ba bị hỏng trong ngày lần lượt là "
                 r"$%s$, $%s$, $%s$. Tính xác suất để trong ngày có ít "
                 r"nhất một máy bị hỏng."
                 % (_xx(p1), _xx(p2), _xx(p3)))
        giai = (r"Biến cố đối là ``cả ba máy đều KHÔNG hỏng''." +
                "\\\\\n"
                r"Ba biến cố độc lập nên xác suất của biến cố đối là" +
                "\\\\\n"
                r"$\left(1 - %s\right)\left(1 - %s\right)"
                r"\left(1 - %s\right) = %s\cdot %s\cdot %s = %s$."
                % (_xx(p1), _xx(p2), _xx(p3), _xx(1 - p1), _xx(1 - p2),
                   _xx(1 - p3), _xx(q)) +
                "\\\\\n"
                r"Vậy $P = 1 - %s = %s$." % (_xx(q), dapso))
        nhieu = _ba_nhieu8(dapso,
                           [_xx(q), _xx(p1 * p2 * p3),
                            _xx(p1 + p2 + p3)],
                           buoc=lambda t: _xx(float(P) - t / 100.0))
        cau += MC_SA_answer_const(debai, dapso, nhieu, giai, 0, 0, 2)
    return cau


def L11_C8_B30_VD151_TL_A_01(socau, dong=1):
    r"""Tự luận: công thức nhân và sơ đồ hình cây, bài toán nhiều giai đoạn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_ba_giai_doan()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for p1, p2, p3 in gt:
        ca_ba = p1 * p2 * p3
        q = (1 - p1) * (1 - p2) * (1 - p3)
        it_nhat = 1 - q
        debai = (r"Ba xạ thủ bắn vào cùng một mục tiêu một cách độc lập. "
                 r"Xác suất bắn trúng của xạ thủ thứ nhất, thứ hai, thứ ba "
                 r"lần lượt là $%s$, $%s$, $%s$."
                 % (_xx(p1), _xx(p2), _xx(p3)))

        hoi_a = r"Tính xác suất để cả ba xạ thủ đều bắn trúng."
        giai_a = (r"Gọi $A_1$, $A_2$, $A_3$ là các biến cố xạ thủ thứ "
                  r"nhất, thứ hai, thứ ba bắn trúng; chúng độc lập." +
                  "\\\\\n"
                  r"$P\left(A_1A_2A_3\right) = %s\cdot %s\cdot %s = %s$."
                  % (_xx(p1), _xx(p2), _xx(p3), _xx(ca_ba)))

        hoi_b = r"Tính xác suất để cả ba xạ thủ đều bắn trượt."
        giai_b = (r"$P\left(\overline{A_i}\right) = 1 - "
                  r"P\left(A_i\right)$ nên ba xác suất trượt lần lượt là "
                  r"$%s$, $%s$, $%s$."
                  % (_xx(1 - p1), _xx(1 - p2), _xx(1 - p3)) +
                  "\\\\\n"
                  r"$P\left(\overline{A_1}\,\overline{A_2}\,"
                  r"\overline{A_3}\right) = %s\cdot %s\cdot %s = %s$."
                  % (_xx(1 - p1), _xx(1 - p2), _xx(1 - p3), _xx(q)))

        hoi_c = r"Tính xác suất để mục tiêu bị trúng đạn."
        giai_c = (r"``Mục tiêu bị trúng đạn'' nghĩa là có ÍT NHẤT một xạ "
                  r"thủ bắn trúng." +
                  "\\\\\n"
                  r"Biến cố đối của nó chính là ``cả ba đều bắn trượt'' đã "
                  r"tính ở câu b." +
                  "\\\\\n"
                  r"$P = 1 - %s = %s$." % (_xx(q), _xx(it_nhat)) +
                  "\\\\\n"
                  r"Dùng biến cố đối gọn hơn nhiều so với cộng bảy trường "
                  r"hợp ``có $1$, $2$ hoặc $3$ xạ thủ trúng''.")

        ds_abcd = [(hoi_a, r"P\left(A_1A_2A_3\right) = %s" % _xx(ca_ba),
                    giai_a),
                   (hoi_b, r"P = %s" % _xx(q), giai_b),
                   (hoi_c, r"P = %s" % _xx(it_nhat), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 8
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C8_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - biến cố hợp, biến cố giao và công thức cộng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_cong_xac_suat()
        if v is not None and v not in gt:
            gt.append(v)

    cauTF = ""
    for i, n, a, b, c in gt:
        ten_nhom, ten_pt, tcA, tcB, tcC = BOI_CANH_CONG[i]
        pa, pb, pc = Fraction(a, n), Fraction(b, n), Fraction(c, n)
        P = pa + pb - pc
        debai = (r"Một %s có $%d$ %s, trong đó có $%d$ %s %s, $%d$ %s %s "
                 r"và $%d$ %s có cả hai tính chất trên. Chọn ngẫu nhiên "
                 r"một %s. Gọi $A$, $B$ lần lượt là hai biến cố ứng với "
                 r"hai tính chất đó."
                 % (ten_nhom, n, ten_pt, a, ten_pt, tcA, b, ten_pt, tcB,
                    c, ten_pt, ten_pt))

        ds_abcd = (
            # a) NB - đọc thẳng định nghĩa xác suất cổ điển
            [
                (r"{\True $P\left(A\right) = %s$}" % _xx(pa),
                 r"Đúng. $P\left(A\right) = \dfrac{%d}{%d} = %s$."
                 % (a, n, _xx(pa))),
                (r"{$P\left(A\right) = %s$}" % _xx(Fraction(a, a + b)),
                 r"Sai. Mẫu số phải là TỔNG số %s của %s, tức là $%d$, "
                 r"chứ không phải $%d$." % (ten_pt, ten_nhom, n, a + b)),
            ],
            # b) TH - một lần dùng công thức giao
            [
                (r"{\True $P\left(AB\right) = %s$}" % _xx(pc),
                 r"Đúng. $AB$ là biến cố ``có cả hai tính chất'', ứng với "
                 r"$%d$ %s nên $P\left(AB\right) = \dfrac{%d}{%d} = %s$."
                 % (c, ten_pt, c, n, _xx(pc))),
                (r"{$P\left(AB\right) = %s$}" % _xx(pa * pb),
                 r"Sai. $A$ và $B$ ở đây KHÔNG độc lập nên không được "
                 r"nhân hai xác suất; phải đếm trực tiếp, được $%s$."
                 % _xx(pc)),
            ],
            # c) VD - dùng công thức cộng đầy đủ
            [
                (r"{\True $P\left(A \cup B\right) = %s$}" % _xx(P),
                 r"Đúng. $P\left(A \cup B\right) = P\left(A\right) + "
                 r"P\left(B\right) - P\left(AB\right)$." + "\\\\\n" +
                 r"$= %s + %s - %s = %s$."
                 % (_xx(pa), _xx(pb), _xx(pc), _xx(P))),
                (r"{$P\left(A \cup B\right) = %s$}" % _xx(pa + pb),
                 r"Sai. Cộng thẳng thì $%d$ %s có CẢ HAI tính chất bị đếm "
                 r"hai lần; phải trừ $P\left(AB\right) = %s$, kết quả là "
                 r"$%s$." % (c, ten_pt, _xx(pc), _xx(P))),
            ],
            # d) VDC - phải tự chuyển sang biến cố đối rồi mới kết luận
            [
                (r"{\True Xác suất để %s được chọn không có tính chất nào "
                 r"trong hai tính chất trên bằng $%s$}"
                 % (ten_pt, _xx(1 - P)),
                 r"Đúng. Biến cố này là biến cố ĐỐI của $A \cup B$." +
                 "\\\\\n" +
                 r"$P\left(\overline{A \cup B}\right) = 1 - %s = %s$."
                 % (_xx(P), _xx(1 - P)) + "\\\\\n" +
                 r"Kiểm lại bằng cách đếm: $%d - \left(%d + %d - %d\right) "
                 r"= %d$ %s, chia cho $%d$ được $%s$."
                 % (n, a, b, c, n - (a + b - c), ten_pt, n, _xx(1 - P))),
                (r"{Xác suất để %s được chọn không có tính chất nào trong "
                 r"hai tính chất trên bằng $%s$}"
                 % (ten_pt, _xx(1 - pa - pb)),
                 r"Sai. $1 - P\left(A\right) - P\left(B\right)$ đã trừ hai "
                 r"lần phần chung. Phải lấy $1 - P\left(A \cup B\right) = "
                 r"%s$." % _xx(1 - P)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L11_C8_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - công thức nhân xác suất cho hai biến cố độc lập.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _bo_it_nhat_mot()
        if v not in gt:
            gt.append(v)

    cauTF = ""
    for i, p1, p2 in gt:
        boi_canh, tenA, tenB, tenC = BOI_CANH_DOC_LAP[i]
        ca_hai = p1 * p2
        khong = (1 - p1) * (1 - p2)
        it_nhat = 1 - khong
        dung_mot = p1 * (1 - p2) + (1 - p1) * p2
        debai = (r"%s. Gọi $A$ là biến cố ``%s'' với $P\left(A\right) = "
                 r"%s$, $B$ là biến cố ``%s'' với $P\left(B\right) = %s$."
                 % (boi_canh, tenA, _xx(p1), tenB, _xx(p2)))

        ds_abcd = (
            # a) NB - biến cố đối
            [
                (r"{\True $P\left(\overline{A}\right) = %s$}" % _xx(1 - p1),
                 r"Đúng. $P\left(\overline{A}\right) = 1 - "
                 r"P\left(A\right) = 1 - %s = %s$."
                 % (_xx(p1), _xx(1 - p1))),
                (r"{$P\left(\overline{A}\right) = %s$}" % _xx(p1),
                 r"Sai. Biến cố đối có xác suất $1 - P\left(A\right) = "
                 r"%s$, không phải chính $P\left(A\right)$." % _xx(1 - p1)),
            ],
            # b) TH - một lần dùng công thức nhân
            [
                (r"{\True $P\left(AB\right) = %s$}" % _xx(ca_hai),
                 r"Đúng. $A$, $B$ độc lập nên $P\left(AB\right) = "
                 r"%s\cdot %s = %s$." % (_xx(p1), _xx(p2), _xx(ca_hai))),
                (r"{$P\left(AB\right) = %s$}" % _xx(p1 + p2),
                 r"Sai. Đó là phép CỘNG. Với hai biến cố độc lập thì "
                 r"$P\left(AB\right) = P\left(A\right)P\left(B\right) = "
                 r"%s$." % _xx(ca_hai)),
            ],
            # c) VD - qua biến cố đối
            [
                (r"{\True Xác suất để %s bằng $%s$}" % (tenC, _xx(it_nhat)),
                 r"Đúng. Biến cố đối là ``cả hai cùng không xảy ra'', có "
                 r"xác suất $%s\cdot %s = %s$."
                 % (_xx(1 - p1), _xx(1 - p2), _xx(khong)) + "\\\\\n" +
                 r"Vậy xác suất cần tìm là $1 - %s = %s$."
                 % (_xx(khong), _xx(it_nhat))),
                (r"{Xác suất để %s bằng $%s$}" % (tenC, _xx(p1 + p2)),
                 r"Sai. Hai biến cố không xung khắc nên không cộng thẳng "
                 r"được; kết quả đúng là $%s$." % _xx(it_nhat)),
            ],
            # d) VDC - phải tự tách thành hai nhánh xung khắc
            [
                (r"{\True Xác suất để có ĐÚNG MỘT trong hai biến cố xảy ra "
                 r"bằng $%s$}" % _xx(dung_mot),
                 r"Đúng. ``Đúng một'' gồm hai trường hợp xung khắc: "
                 r"$A\,\overline{B}$ và $\overline{A}\,B$." + "\\\\\n" +
                 r"$P\left(A\,\overline{B}\right) = %s\cdot %s = %s$; "
                 r"$P\left(\overline{A}\,B\right) = %s\cdot %s = %s$."
                 % (_xx(p1), _xx(1 - p2), _xx(p1 * (1 - p2)),
                    _xx(1 - p1), _xx(p2), _xx((1 - p1) * p2)) + "\\\\\n" +
                 r"Cộng lại được $%s$." % _xx(dung_mot)),
                (r"{Xác suất để có đúng một trong hai biến cố xảy ra bằng "
                 r"$%s$}" % _xx(it_nhat),
                 r"Sai. $%s$ là xác suất ``có ít nhất một'', đã bao gồm cả "
                 r"trường hợp CẢ HAI cùng xảy ra." % _xx(it_nhat) +
                 "\\\\\n" +
                 r"Bỏ phần $P\left(AB\right) = %s$ đi thì còn $%s$."
                 % (_xx(ca_hai), _xx(dung_mot))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF
