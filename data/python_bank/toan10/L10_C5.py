# ==========================================================
# CHƯƠNG 5 (lớp 10): CÁC SỐ ĐẶC TRƯNG CỦA MẪU SỐ LIỆU KHÔNG GHÉP NHÓM
#   Bài 12. Số gần đúng và sai số
#   Bài 13. Các số đặc trưng đo xu thế trung tâm
#   Bài 14. Các số đặc trưng đo độ phân tán
#
# Nguồn: tệp LopXChuong5.py của cô Lan. Tệp ấy ở FORM CŨ (tự mở tệp
# de.tex rồi de.write) và chỉ có 3 hàm, nên viết lại cho đúng khuôn
# math_type - math_type.py GIỮ NGUYÊN, không sửa một dòng nào.
#
# BA LỖI trong tệp của cô đã tránh khi viết lại (xem 16_CHANGELOG):
#   1. K10_5_13_2_1_TH có input() -> treo khi sinh đề tự động; đề hỏi
#      TRUNG VỊ nhưng lại tính numpy.mean; lời giải dùng biến "median"
#      chưa hề được gán -> NameError.
#   2. K10_5_14_1_1_TH ghi cân nặng trẻ sơ sinh "đơn vị kg" nhưng số
#      liệu là 2700-4200 (gam).
#   3. K10_5_14_1_3_VD gọi numpy.delete(X, i) với i là GIÁ TRỊ chứ không
#      phải chỉ số.
#
# QUY ƯỚC SGK KNTT LỚP 10 - bám đúng, không dùng công thức lớp trên:
#   - Tứ phân vị: sắp xếp tăng dần; Q2 là trung vị; Q1 là trung vị nửa
#     số liệu bên trái Q2, Q3 là trung vị nửa bên phải (nếu n lẻ thì
#     KHÔNG tính Q2 vào hai nửa).
#   - Phương sai: s^2 = (1/n) * tổng (x_i - x_tb)^2  - chia cho n,
#     KHÔNG phải n-1.
#   - Giá trị bất thường: x < Q1 - 1,5*(Q3-Q1) hoặc x > Q3 + 1,5*(Q3-Q1).
# ==========================================================
import math
import random

from math_type import *

DAU_THAP_PHAN = ","


def _xx5(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết theo cách viết Việt Nam."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu5(dapso, ung_vien, buoc=None):
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


def _bang(X):
    """Viết mẫu số liệu thành một dòng, cách nhau bằng \\quad."""
    return r"\quad ".join("$%s$" % _xx5(x) for x in X)


def _trung_vi(X):
    """Trung vị của mẫu ĐÃ SẮP XẾP tăng dần."""
    n = len(X)
    giua = n // 2
    if n % 2 == 1:
        return float(X[giua])
    return (X[giua - 1] + X[giua]) / 2.0


def _tu_phan_vi(X):
    """Ba tứ phân vị Q1, Q2, Q3 theo đúng quy ước SGK KNTT lớp 10.

    Sắp xếp tăng dần, Q2 là trung vị. Nếu n LẺ thì Q2 không thuộc nửa
    nào; nếu n CHẴN thì chia đôi đúng giữa.
    """
    Y = sorted(X)
    n = len(Y)
    q2 = _trung_vi(Y)
    if n % 2 == 1:
        duoi = Y[:n // 2]
        tren = Y[n // 2 + 1:]
    else:
        duoi = Y[:n // 2]
        tren = Y[n // 2:]
    return _trung_vi(duoi), q2, _trung_vi(tren)


def _so_trung_binh(X):
    return sum(X) / float(len(X))


def _phuong_sai(X):
    """s^2 = (1/n) * tổng (x_i - x_tb)^2 - đúng quy ước lớp 10 (chia n)."""
    tb = _so_trung_binh(X)
    return sum((x - tb) ** 2 for x in X) / float(len(X))


def _do_lech_chuan(X):
    return math.sqrt(_phuong_sai(X))


def _mot(X):
    """Mốt: giá trị có tần số lớn nhất. Trả về danh sách đã sắp xếp."""
    dem = {}
    for x in X:
        dem[x] = dem.get(x, 0) + 1
    lon_nhat = max(dem.values())
    return sorted(k for k, v in dem.items() if v == lon_nhat)


def _dep(x, n=2):
    """Số có viết gọn được bằng đúng n chữ số thập phân hay không.

    Câu trả lời ngắn chấm bằng SO KHỚP CHUỖI nên đáp số phải là số thập
    phân hữu hạn; nếu không, học sinh làm đúng vẫn có thể gõ ra số khác.
    """
    return abs(x * (10 ** n) - round(x * (10 ** n))) < 1e-9


# =====================================================================
# BÀI 12. SỐ GẦN ĐÚNG VÀ SAI SỐ
# =====================================================================

def L10_C5_B12_NB062_MC_A_01(socau, dang=1):
    """Nhận ra số gần đúng trong tình huống cho trước.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    GAN_DUNG = [
        "Dân số của một tỉnh là $1\\,850\\,000$ người",
        "Chu vi của một đường tròn bán kính $2$ cm là $12{,}57$ cm",
        "Chiều cao của một ngọn núi là $3143$ m",
        "Khoảng cách từ Trái Đất đến Mặt Trời là $150$ triệu ki-lô-mét",
    ]
    DUNG_HAN = [
        "Số học sinh của lớp 10A là $42$",
        "Một tuần có $7$ ngày",
        "Số cạnh của một hình lập phương là $12$",
        "Một giờ có $60$ phút",
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(GAN_DUNG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(GAN_DUNG):
            break

    cauTN = ""
    for i in gt:
        dung = "%s." % GAN_DUNG[i]
        nhieu = ["%s." % t for t in DUNG_HAN]
        debai = (r"Trong các số liệu sau, số liệu nào là \textbf{số gần "
                 r"đúng}?")
        giai = (r"Số gần đúng là số có được từ \textbf{đo đạc, tính toán hay "
                r"ước lượng}, nên không biểu thị chính xác giá trị thật."
                "\\\\\n"
                r"Số đúng là số đếm được hoặc do quy ước, không có sai số."
                "\\\\\n"
                r"``%s'' có được từ đo đạc/ước lượng nên là số gần đúng; còn "
                r"số học sinh, số ngày trong tuần, số cạnh hình lập phương, "
                r"số phút trong một giờ đều là số đúng." % GAN_DUNG[i])
        cauTN += _MC_khong_cham(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_NB063_MC_A_01(socau, dang=1):
    r"""Nhận ra sai số tuyệt đối của một số gần đúng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(20, 90) + random.choice([0.0, 0.5, 0.25])
        gd = a + random.choice([-0.3, -0.2, 0.2, 0.3, 0.4])
        v = (round(a, 2), round(gd, 2))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, gd in gt:
        sai_so = abs(a - gd)
        dung = r"$%s$" % _xx5(sai_so)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(sai_so), [_xx5(a - gd), _xx5(a + gd), _xx5(sai_so / a),
                           _xx5(sai_so * 2)],
            buoc=lambda t: _xx5(sai_so + t / 10.0))]
        debai = (r"Cho số đúng $\overline{a} = %s$ và số gần đúng của nó là "
                 r"$a = %s$. Sai số tuyệt đối $\Delta_a$ bằng bao nhiêu?"
                 % (_xx5(a), _xx5(gd)))
        giai = (r"Sai số tuyệt đối của số gần đúng $a$ so với số đúng "
                r"$\overline{a}$ là"
                "\\\\\n"
                r"$\Delta_a = \left|\overline{a} - a\right|$."
                "\\\\\n"
                r"$\Delta_a = \left|%s - %s\right| = %s$."
                % (_xx5(a), _xx5(gd), _xx5(sai_so)) +
                "\\\\\n"
                r"Chú ý sai số tuyệt đối luôn là số \textbf{không âm} vì có "
                r"dấu giá trị tuyệt đối.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_NB064_MC_A_01(socau, dang=1):
    r"""Nhận ra độ chính xác của một số gần đúng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    a = r"a"
    dung = (r"$\Delta_a \le d$, tức là "
            r"$a - d \le \overline{a} \le a + d$")
    nhieu = [r"$\Delta_a \ge d$, tức là $\overline{a} \ge a + d$",
             r"$\Delta_a = d$, tức là $\overline{a} = a + d$",
             r"$\delta_a \le d$, tức là sai số tương đối không vượt quá $d$",
             r"$\Delta_a \le d$, tức là $\overline{a} \le a - d$"]

    cauTN = ""
    for _ in range(socau):
        debai = (r"Cho số gần đúng $a$ của số đúng $\overline{a}$ với độ "
                 r"chính xác $d$. Khẳng định nào sau đây \textbf{đúng}?")
        giai = (r"Nói ``$a$ là số gần đúng của $\overline{a}$ với độ chính "
                r"xác $d$'' nghĩa là sai số tuyệt đối không vượt quá $d$:"
                "\\\\\n"
                r"$\Delta_a = \left|\overline{a} - a\right| \le d$."
                "\\\\\n"
                r"Bỏ dấu giá trị tuyệt đối được "
                r"$-d \le \overline{a} - a \le d$, tức là "
                r"$a - d \le \overline{a} \le a + d$."
                "\\\\\n"
                r"Ta viết gọn $\overline{a} = a \pm d$.")
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_NB065_MC_A_01(socau, dang=1):
    r"""Nhận ra sai số tương đối của một số gần đúng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    dung = r"$\delta_a = \dfrac{\Delta_a}{\left|a\right|}$"
    nhieu = [r"$\delta_a = \dfrac{\left|a\right|}{\Delta_a}$",
             r"$\delta_a = \Delta_a \cdot \left|a\right|$",
             r"$\delta_a = \Delta_a - \left|a\right|$",
             r"$\delta_a = \dfrac{\Delta_a}{\left|\overline{a} - a\right|}$"]

    cauTN = ""
    for _ in range(socau):
        debai = (r"Cho số gần đúng $a$ có sai số tuyệt đối $\Delta_a$. Công "
                 r"thức nào sau đây là công thức tính \textbf{sai số tương "
                 r"đối} $\delta_a$?")
        giai = (r"Sai số tương đối của số gần đúng $a$ là tỉ số giữa sai số "
                r"tuyệt đối và $\left|a\right|$:"
                "\\\\\n"
                r"$\delta_a = \dfrac{\Delta_a}{\left|a\right|}$."
                "\\\\\n"
                r"Sai số tương đối thường viết dưới dạng phần trăm và cho "
                r"biết phép đo \textbf{chính xác tới mức nào} so với độ lớn "
                r"của đại lượng - $\delta_a$ càng nhỏ thì phép đo càng chính "
                r"xác.")
        cauTN += MC_SA_answer_text(debai, dung, list(nhieu), giai, 0, 0, dang)
    return cauTN


def _hang_quy_tron(d):
    """Số chữ số thập phân khi quy tròn theo độ chính xác d.

    SGK KNTT: quy tròn đến hàng thấp nhất mà d nhỏ hơn MỘT đơn vị của
    hàng đó. Ví dụ d = 0,01 thì một đơn vị hàng phần trăm là 0,01, không
    lớn hơn d; một đơn vị hàng phần mười là 0,1 > d, nên quy tròn đến
    hàng phần mười (một chữ số thập phân).
    """
    k = 0
    while 10.0 ** (-k) > d:
        k += 1
    return max(k - 1, 0)


def L10_C5_B12_TH066_MC_A_01(socau, dang=1):
    r"""Xác định số gần đúng với độ chính xác cho trước.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(10, 99) + random.randint(1, 99) / 100.0
        d = random.choice([0.01, 0.05, 0.1, 0.5])
        v = (round(a, 2), d)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, d in gt:
        dung = (r"$%s \le \overline{a} \le %s$"
                % (_xx5(a - d, 3), _xx5(a + d, 3)))
        nhieu = [r"$%s \le \overline{a} \le %s$"
                 % (_xx5(a, 3), _xx5(a + d, 3)),
                 r"$%s \le \overline{a} \le %s$"
                 % (_xx5(a - 2 * d, 3), _xx5(a + 2 * d, 3)),
                 r"$%s \le \overline{a} \le %s$"
                 % (_xx5(a - d / 2, 3), _xx5(a + d / 2, 3)),
                 r"$\overline{a} = %s$" % _xx5(a, 3)]
        debai = (r"Một phép đo cho kết quả $\overline{a} = %s \pm %s$. Giá "
                 r"trị đúng $\overline{a}$ nằm trong khoảng nào?"
                 % (_xx5(a, 3), _xx5(d, 3)))
        giai = (r"Viết $\overline{a} = a \pm d$ nghĩa là sai số tuyệt đối "
                r"không vượt quá $d$: $\left|\overline{a} - a\right| \le d$."
                "\\\\\n"
                r"Bỏ dấu giá trị tuyệt đối: "
                r"$a - d \le \overline{a} \le a + d$."
                "\\\\\n"
                r"Thay số: $%s - %s \le \overline{a} \le %s + %s$, tức là "
                r"$%s \le \overline{a} \le %s$."
                % (_xx5(a, 3), _xx5(d, 3), _xx5(a, 3), _xx5(d, 3),
                   _xx5(a - d, 3), _xx5(a + d, 3)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_TH066_SA_A_01(socau):
    r"""Số gần đúng với độ chính xác cho trước - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(20, 99) + random.choice([0.0, 0.5, 0.25, 0.75])
        d = random.choice([0.25, 0.5, 1.0, 2.0])
        v = (a, d)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, d in gt:
        kq = a + d
        debai = (r"Một phép đo cho kết quả $\overline{a} = %s \pm %s$. Tìm "
                 r"giá trị \textbf{lớn nhất} có thể của $\overline{a}$."
                 % (_xx5(a), _xx5(d)))
        giai = (r"$\overline{a} = a \pm d$ nghĩa là "
                r"$a - d \le \overline{a} \le a + d$."
                "\\\\\n"
                r"Giá trị lớn nhất là $a + d = %s + %s = %s$."
                % (_xx5(a), _xx5(d), _xx5(kq)))
        nhieu = _ba_nhieu5(_xx5(kq), [_xx5(a - d), _xx5(a), _xx5(a + 2 * d),
                                      _xx5(a * d)],
                           buoc=lambda t: _xx5(kq + t))
        cau += MC_SA_answer_text(debai, _xx5(kq), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B12_TH067_MC_A_01(socau, dang=1):
    r"""Viết số gần đúng dưới dạng chuẩn (kí hiệu khoa học).

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Dạng chuẩn ở đây hiểu là $\alpha \times 10^{n}$ với
    $1 \le \alpha < 10$ - cách viết dùng cho các số rất lớn hoặc rất bé,
    nằm trong chương trình lớp 10.
    """
    gt = []
    while len(gt) < socau:
        alpha = random.randint(11, 99) / 10.0
        n = random.choice([3, 4, 5, 6, -3, -4, -5])
        v = (alpha, n)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for alpha, n in gt:
        gia_tri = alpha * (10 ** n)
        if n > 0:
            viet = ("%d" % round(gia_tri))
        else:
            viet = ("%.*f" % (abs(n) + 1, gia_tri)).rstrip("0")
        viet_tex = viet.replace(".", DAU_THAP_PHAN)
        dung = r"$%s \times 10^{%d}$" % (_xx5(alpha), n)
        nhieu = [r"$%s \times 10^{%d}$" % (_xx5(alpha), -n),
                 r"$%s \times 10^{%d}$" % (_xx5(alpha * 10), n - 1 + 2),
                 r"$%s \times 10^{%d}$" % (_xx5(alpha / 10), n),
                 r"$%s \times 10^{%d}$" % (_xx5(alpha), n + 1)]
        debai = (r"Viết số $%s$ dưới dạng chuẩn "
                 r"$\alpha \times 10^{n}$ với $1 \le \alpha < 10$."
                 % viet_tex)
        giai = (r"Dạng chuẩn của một số là $\alpha \times 10^{n}$ với "
                r"$1 \le \alpha < 10$ và $n$ nguyên."
                "\\\\\n"
                r"Dịch dấu phẩy về sau chữ số khác $0$ đầu tiên, được "
                r"$\alpha = %s$; số lần dịch cho ta $n = %d$."
                % (_xx5(alpha), n) +
                "\\\\\n"
                r"Vậy $%s = %s \times 10^{%d}$."
                % (viet_tex, _xx5(alpha), n))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_TH068_MC_A_01(socau, dang=1):
    r"""Tính sai số tương đối của số gần đúng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([20, 25, 40, 50, 80, 100, 125, 200])
        d = random.choice([0.1, 0.2, 0.25, 0.5, 1.0, 2.0])
        if not _dep(100.0 * d / a, 2):
            continue
        v = (a, d)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, d in gt:
        pt = 100.0 * d / a
        dung = r"$%s\%%$" % _xx5(pt)
        nhieu = [r"$%s\%%$" % x for x in _ba_nhieu5(
            _xx5(pt), [_xx5(100.0 * a / d), _xx5(pt * 10), _xx5(pt / 10),
                       _xx5(d)],
            buoc=lambda t: _xx5(pt + t / 100.0))]
        debai = (r"Cho số gần đúng $a = %s$ với độ chính xác $d = %s$. Sai "
                 r"số tương đối $\delta_a$ không vượt quá bao nhiêu phần "
                 r"trăm?" % (_xx5(a), _xx5(d)))
        giai = (r"$\delta_a = \dfrac{\Delta_a}{\left|a\right|} \le "
                r"\dfrac{d}{\left|a\right|}$."
                "\\\\\n"
                r"$\dfrac{%s}{%s} = %s = %s\%%$."
                % (_xx5(d), _xx5(a), _xx5(d / a, 5), _xx5(pt)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_TH068_SA_A_01(socau):
    r"""Sai số tương đối - trả lời ngắn, tính theo phần trăm.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([20, 25, 40, 50, 80, 100, 125, 200, 250])
        d = random.choice([0.1, 0.2, 0.25, 0.5, 1.0, 2.0, 2.5])
        if not _dep(100.0 * d / a, 2):
            continue
        v = (a, d)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, d in gt:
        pt = 100.0 * d / a
        debai = (r"Cho số gần đúng $a = %s$ với độ chính xác $d = %s$. Tính "
                 r"sai số tương đối $\delta_a$ lớn nhất, viết kết quả theo "
                 r"\textbf{phần trăm} (chỉ ghi số, không ghi dấu $\%%$)."
                 % (_xx5(a), _xx5(d)))
        giai = (r"$\delta_a \le \dfrac{d}{\left|a\right|} = "
                r"\dfrac{%s}{%s} = %s$."
                % (_xx5(d), _xx5(a), _xx5(d / a, 5)) +
                "\\\\\n"
                r"Đổi ra phần trăm: $%s \times 100 = %s\%%$."
                % (_xx5(d / a, 5), _xx5(pt)))
        nhieu = _ba_nhieu5(_xx5(pt), [_xx5(d / a, 5), _xx5(pt * 10),
                                      _xx5(pt / 10), _xx5(a / d)],
                           buoc=lambda t: _xx5(pt + t / 4.0))
        cau += MC_SA_answer_text(debai, _xx5(pt), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B12_TH069_MC_A_01(socau, dang=1):
    r"""Quy tròn số gần đúng theo độ chính xác.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(1, 99) + random.randint(1000, 9999) / 10000.0
        d = random.choice([0.001, 0.01, 0.1])
        v = (round(a, 4), d)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, d in gt:
        k = _hang_quy_tron(d)
        kq = round(a, k)
        dung = r"$%s$" % _xx5(kq, k)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(kq, k), [_xx5(round(a, k + 1), k + 1),
                          _xx5(round(a, max(k - 1, 0)), max(k - 1, 0)),
                          _xx5(a, 4), _xx5(round(a, k + 2), k + 2)],
            buoc=lambda t: _xx5(kq + t / 10.0 ** k, k))]
        ten_hang = {0: "hàng đơn vị", 1: "hàng phần mười",
                    2: "hàng phần trăm", 3: "hàng phần nghìn"}[k]
        debai = (r"Cho số gần đúng $a = %s$ với độ chính xác $d = %s$. Hãy "
                 r"quy tròn số $a$." % (_xx5(a, 4), _xx5(d, 4)))
        giai = (r"Quy tắc: quy tròn đến hàng thấp nhất mà $d$ nhỏ hơn "
                r"\textbf{một đơn vị} của hàng đó."
                "\\\\\n"
                r"Với $d = %s$, một đơn vị của %s là $%s > d$, nên quy tròn "
                r"đến %s."
                % (_xx5(d, 4), ten_hang, _xx5(10.0 ** (-k), 4), ten_hang) +
                "\\\\\n"
                r"Vậy số quy tròn của $a$ là $%s$." % _xx5(kq, k))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B12_TH069_SA_A_01(socau):
    r"""Số quy tròn - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(1, 99) + random.randint(1000, 9999) / 10000.0
        d = random.choice([0.001, 0.01, 0.1])
        v = (round(a, 4), d)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, d in gt:
        k = _hang_quy_tron(d)
        kq = round(a, k)
        debai = (r"Cho số gần đúng $a = %s$ với độ chính xác $d = %s$. Viết "
                 r"số quy tròn của $a$." % (_xx5(a, 4), _xx5(d, 4)))
        giai = (r"Quy tròn đến hàng thấp nhất mà $d$ nhỏ hơn một đơn vị của "
                r"hàng đó. Với $d = %s$ thì quy tròn đến %d chữ số thập phân."
                % (_xx5(d, 4), k) +
                "\\\\\n"
                r"Vậy số quy tròn của $a$ là $%s$." % _xx5(kq, k))
        nhieu = _ba_nhieu5(_xx5(kq, k),
                           [_xx5(round(a, k + 1), k + 1),
                            _xx5(round(a, max(k - 1, 0)), max(k - 1, 0)),
                            _xx5(a, 4)],
                           buoc=lambda t: _xx5(kq + t / 10.0 ** k, k))
        cau += MC_SA_answer_text(debai, _xx5(kq, k), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B12_TH071_MC_A_01(socau, dang=1):
    r"""Dùng máy tính cầm tay tính toán với số gần đúng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    BIEU_THUC = [
        (r"\sqrt{%d}", lambda n: math.sqrt(n), [2, 3, 5, 7, 10, 11, 13]),
        (r"\sqrt[3]{%d}", lambda n: n ** (1.0 / 3), [2, 3, 5, 7, 9, 11]),
        (r"\dfrac{%d}{7}", lambda n: n / 7.0, [3, 5, 8, 9, 11, 12]),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BIEU_THUC))
        n = random.choice(BIEU_THUC[i][2])
        if (i, n) not in gt:
            gt.append((i, n))

    cauTN = ""
    for i, n in gt:
        mau, tinh, _ds = BIEU_THUC[i]
        gia_tri = tinh(n)
        kq = round(gia_tri, 3)
        dung = r"$%s$" % _xx5(kq, 3)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(kq, 3), [_xx5(round(gia_tri, 2), 2),
                          _xx5(round(gia_tri + 0.001, 3), 3),
                          _xx5(round(gia_tri - 0.001, 3), 3),
                          _xx5(round(gia_tri * 10, 3), 3)],
            buoc=lambda t: _xx5(round(gia_tri + t / 100.0, 3), 3))]
        debai = (r"Dùng máy tính cầm tay, tính $%s$ và làm tròn kết quả đến "
                 r"\textbf{hàng phần nghìn}." % (mau % n))
        giai = (r"Bấm máy được $%s \approx %s\ldots$"
                % (mau % n, _xx5(gia_tri, 6)) +
                "\\\\\n"
                r"Làm tròn đến hàng phần nghìn (ba chữ số thập phân): "
                r"nhìn chữ số hàng phần chục nghìn để quyết định làm tròn "
                r"lên hay xuống."
                "\\\\\n"
                r"Kết quả: $%s \approx %s$." % (mau % n, _xx5(kq, 3)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


# CLAUDE THEM 29/09/2026 - VD070 (co Lan: "la dang van dung. vay khong hoi
# kieu so nao, ma phai la co bao nhieu so"). Bang nhieu dong, moi dong co
# hai thanh phan va cot tong; MOT SO dong tong bi ghi sai - hoc sinh phai
# kiem tra tung dong moi dem duoc.
_BOI_CANH_TONG = [
    ("Bảng sau ghi số học sinh nam, nữ và sĩ số của các lớp khối 10:",
     ("Lớp", "Nam", "Nữ", "Sĩ số"), ["10A1", "10A2", "10A3", "10A4", "10A5", "10A6"],
     (14, 24), "lớp", "sĩ số"),
    ("Bảng sau ghi số sản phẩm đạt chuẩn, không đạt chuẩn và tổng số sản phẩm "
     "của các tổ trong một ngày:",
     ("Tổ", "Đạt", "Không đạt", "Tổng"), ["Tổ 1", "Tổ 2", "Tổ 3", "Tổ 4", "Tổ 5", "Tổ 6"],
     (40, 70), "tổ", "tổng số sản phẩm"),
    ("Bảng sau ghi số vé người lớn, vé trẻ em và tổng số vé một rạp chiếu phim "
     "bán được trong các ngày:",
     ("Ngày", "Người lớn", "Trẻ em", "Tổng"), ["Thứ Hai", "Thứ Ba", "Thứ Tư",
                                             "Thứ Năm", "Thứ Sáu", "Thứ Bảy"],
     (60, 150), "ngày", "tổng số vé"),
]


def _bang_tong_co_dong_sai(so_dong, so_sai):
    """Trả về (bối cảnh, các dòng (a, b, tổng ghi), chỉ số dòng sai)."""
    bc = random.choice(_BOI_CANH_TONG)
    lo, hi = bc[3]
    hang = [(random.randint(lo, hi), random.randint(lo // 2, hi)) for _ in range(so_dong)]
    sai = sorted(random.sample(range(so_dong), so_sai))
    dong = []
    for k, (a, b) in enumerate(hang):
        t = a + b
        if k in sai:
            t += random.choice([-10, -2, -1, 1, 2, 10])
        dong.append((a, b, t))
    return bc, dong, sai


def _tex_bang_tong(bc, dong):
    cot, ten = bc[1], bc[2]
    than = " ".join(r"%s & $%d$ & $%d$ & $%d$ \\ \hline" % (ten[k], a, b, t)
                    for k, (a, b, t) in enumerate(dong))
    return (r"\begin{center}\begin{tabular}{|c|c|c|c|}\hline " + " & ".join(cot) +
            r" \\ \hline " + than + r"\end{tabular}\end{center}")


def _giai_bang_tong(bc, dong, sai):
    cot, ten, don_vi = bc[1], bc[2], bc[4]
    kiem = "; ".join(r"%s: $%d + %d = %d$%s" % (ten[k], a, b, a + b,
                                                  (r" $\ne %d$" % t) if a + b != t else "")
                     for k, (a, b, t) in enumerate(dong))
    return (r"Với mỗi %s, cột ``%s'' phải bằng tổng hai cột ``%s'' và ``%s''."
            % (don_vi, cot[3], cot[1], cot[2]) +
            "\\\\\n" + r"Kiểm tra từng dòng: " + kiem + "." +
            "\\\\\n" +
            r"Các %s ghi sai: %s. Vậy có $%d$ %s có số liệu không chính xác."
            % (don_vi, ", ".join(ten[k] for k in sai), len(sai), don_vi))


def L10_C5_B12_NB070_MC_A_01(socau, dang=1):
    r"""Phát hiện số liệu VÔ LÍ DỄ THẤY trong bảng dữ liệu (mức NB).

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    SUA 29/09/2026 (co Lan: "gia tri bat thuong qua ro, kiem tra lai muc
    do"): truoc la L10_C5_B12_VD070_MC_A_01. So lieu vo li nhin la thay
    (chieu cao 15 cm, diem 15/10...) nen chuyen ve muc NB.
    """
    BOI_CANH = [
        ("chiều cao (cm) của $6$ học sinh lớp 10", 150, 180, 15,
         "chiều cao $15$ cm là không thể có ở học sinh lớp 10"),
        ("cân nặng (kg) của $6$ học sinh lớp 10", 42, 60, 420,
         "cân nặng $420$ kg là không thể có ở học sinh lớp 10"),
        ("điểm kiểm tra môn Toán của $6$ học sinh", 5, 10, 15,
         "thang điểm chỉ tới $10$ nên điểm $15$ là không hợp lí"),
        ("số con trong $6$ gia đình", 1, 4, -2,
         "số con không thể là số âm"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BOI_CANH))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(BOI_CANH):
            break

    cauTN = ""
    for i in gt:
        mo_ta, lo, hi, la, ly_do = BOI_CANH[i]
        binh_thuong = [random.randint(lo, hi) for _ in range(5)]
        vi_tri = random.randrange(6)
        X = binh_thuong[:vi_tri] + [la] + binh_thuong[vi_tri:]
        dung = r"$%s$" % _xx5(la)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(la), [_xx5(v) for v in binh_thuong],
            buoc=lambda t: _xx5(lo + t))]
        debai = (r"Bảng sau ghi %s:" % mo_ta +
                 "\\\\\n" + r"\begin{center}" + _bang(X) + r"\end{center}" +
                 "\n" +
                 r"Số liệu nào trong bảng là \textbf{không hợp lí}?")
        giai = (r"Muốn biết một số liệu có hợp lí hay không, ta đối chiếu "
                r"với khoảng giá trị mà đại lượng ấy có thể nhận trong thực "
                r"tế."
                "\\\\\n"
                r"Ở đây %s." % ly_do +
                "\\\\\n"
                r"Các số liệu còn lại đều nằm trong khoảng hợp lí. Vậy số "
                r"liệu không hợp lí là $%s$." % _xx5(la))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN



def L10_C5_B12_VD070_MC_A_01(socau, dang=1):
    r"""Phát hiện số liệu KHÔNG CHÍNH XÁC dựa trên mối liên hệ toán học đơn
    giản (tổng các thành phần phải bằng số tổng) - hỏi CÓ BAO NHIÊU dòng sai.

    CLAUDE THEM 29/09/2026, sua cung ngay theo co Lan: muc van dung thi hoi
    "co bao nhieu", khong hoi "so nao". Ban de thay (so lieu vo li nhin la
    thay) o L10_C5_B12_NB070_MC_A_01.
    """
    cauTN = ""
    for _ in range(socau):
        so_dong = random.choice([5, 6])
        bc, dong, sai = _bang_tong_co_dong_sai(so_dong, random.choice([1, 2, 3]))
        dung = "$%d$" % len(sai)
        nhieu = ["$%d$" % x for x in random.sample([x for x in range(0, 5) if x != len(sai)], 3)]
        debai = (bc[0] + "\n" + _tex_bang_tong(bc, dong) + "\n" +
                 r"Có bao nhiêu %s có số liệu \textbf{không chính xác}?" % bc[4])
        cauTN += MC_SA_answer_text(debai, dung, nhieu, _giai_bang_tong(bc, dong, sai), 0, 0, dang)
    return cauTN


def L10_C5_B12_VD070_TL_A_01(socau, dong=1):
    r"""Tự luận: đếm số dòng có số liệu không chính xác và tính lại tổng đúng.

    SUA 29/09/2026 (co Lan: muc van dung thi hoi "co bao nhieu"): ban cu hoi
    "chi ra so lieu khong hop li" voi chieu cao 15 cm - nhin la thay.
    """
    cauTN = ""
    for _ in range(socau):
        bc, hang, sai = _bang_tong_co_dong_sai(6, random.choice([1, 2, 3]))
        cot, ten, don_vi, tong_ten = bc[1], bc[2], bc[4], bc[5]
        tong_ghi = sum(t for _a, _b, t in hang)
        tong_dung = sum(a + b for a, b, _t in hang)
        debai = (bc[0] + "\n" + _tex_bang_tong(bc, hang) +
                 "\n" + r"Biết rằng hai cột ``%s'' và ``%s'' được ghi đúng." % (cot[1], cot[2]))
        hoi_a = r"Có bao nhiêu %s có số liệu không chính xác? Đó là những %s nào?" % (don_vi, don_vi)
        giai_a = _giai_bang_tong(bc, hang, sai)
        hoi_b = (r"Nếu cộng cột ``%s'' như trong bảng thì được bao nhiêu? Tính lại "
                 r"%s đúng của cả bảng." % (cot[3], tong_ten))
        giai_b = (r"Cộng cột ``%s'' như trong bảng: $%s = %d$." %
                  (cot[3], " + ".join(str(t) for _a, _b, t in hang), tong_ghi) +
                  "\\\\\n" +
                  r"Vì hai cột ``%s'', ``%s'' đúng nên %s đúng là "
                  r"$%d + %d = %d$." % (cot[1], cot[2], tong_ten,
                                        sum(a for a, _b, _t in hang),
                                        sum(b for _a, b, _t in hang), tong_dung) +
                  "\\\\\n" +
                  r"Số liệu trong bảng lệch $%d$ so với thực tế." % abs(tong_ghi - tong_dung))
        ds_abcd = [(hoi_a, r"%d" % len(sai), giai_a),
                   (hoi_b, r"%d" % tong_dung, giai_b)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def _mau_so_lieu(n, lo, hi, dieu_kien=None, lan_thu=300):
    """Sinh một mẫu n số nguyên trong [lo; hi] thoả điều kiện cho trước.

    dieu_kien nhận danh sách ĐÃ SẮP XẾP và trả về True/False. Dùng để ép
    đáp số ra số thập phân hữu hạn - câu trả lời ngắn chấm bằng so khớp
    chuỗi nên không được để đáp số lẻ vô hạn.
    """
    for _ in range(lan_thu):
        X = sorted(random.randint(lo, hi) for _ in range(n))
        if dieu_kien is None or dieu_kien(X):
            return X
    return None


def L10_C5_B13_TH072_MC_A_01(socau, dang=1):
    r"""Tính số trung bình của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([5, 6, 8, 10])
        X = _mau_so_lieu(n, 10, 40, lambda Y: _dep(_so_trung_binh(Y), 2))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        X = list(X)
        tb = _so_trung_binh(X)
        dung = r"$%s$" % _xx5(tb)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(tb), [_xx5(_trung_vi(X)), _xx5(sum(X)),
                       _xx5(max(X) - min(X)), _xx5(tb + 1)],
            buoc=lambda t: _xx5(tb + t / 2.0))]
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(X) + r"\end{center}" +
                 "\n" + r"Số trung bình của mẫu số liệu trên bằng bao nhiêu?")
        giai = (r"Số trung bình bằng tổng các số liệu chia cho số số liệu:"
                "\\\\\n"
                r"$\overline{x} = \dfrac{%s}{%d} = \dfrac{%s}{%d} = %s$."
                % (" + ".join(str(x) for x in X), len(X),
                   _xx5(sum(X)), len(X), _xx5(tb)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B13_TH072_SA_A_01(socau):
    r"""Số trung bình của mẫu - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([5, 6, 8, 10])
        X = _mau_so_lieu(n, 20, 60, lambda Y: _dep(_so_trung_binh(Y), 2))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        X = list(X)
        tb = _so_trung_binh(X)
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(X) + r"\end{center}" +
                 "\n" + r"Tính số trung bình của mẫu số liệu.")
        giai = (r"$\overline{x} = \dfrac{%s}{%d} = %s$."
                % (_xx5(sum(X)), len(X), _xx5(tb)))
        nhieu = _ba_nhieu5(_xx5(tb), [_xx5(_trung_vi(X)), _xx5(sum(X)),
                                      _xx5(max(X) - min(X))],
                           buoc=lambda t: _xx5(tb + t / 2.0))
        cau += MC_SA_answer_text(debai, _xx5(tb), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B13_TH073_MC_A_01(socau, dang=1):
    r"""Tìm trung vị của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đề cố ý cho mẫu CHƯA SẮP XẾP để học sinh buộc phải sắp xếp trước -
    đây là chỗ hay sai nhất khi tìm trung vị.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([5, 6, 7, 8])
        X = _mau_so_lieu(n, 10, 45, lambda Y: _dep(_trung_vi(Y), 2))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Y = list(X)
        random.shuffle(Y)
        tv = _trung_vi(sorted(Y))
        dung = r"$%s$" % _xx5(tv)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(tv), [_xx5(_so_trung_binh(Y)), _xx5(Y[len(Y) // 2]),
                       _xx5(max(Y)), _xx5(min(Y))],
            buoc=lambda t: _xx5(tv + t))]
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Y) + r"\end{center}" +
                 "\n" + r"Trung vị của mẫu số liệu trên bằng bao nhiêu?")
        Z = sorted(Y)
        n = len(Z)
        if n % 2 == 1:
            cach = (r"Mẫu có $%d$ số liệu ($%d$ là số lẻ) nên trung vị là số "
                    r"liệu đứng \textbf{chính giữa}, tức số thứ $%d$: $%s$."
                    % (n, n, n // 2 + 1, _xx5(tv)))
        else:
            cach = (r"Mẫu có $%d$ số liệu ($%d$ là số chẵn) nên trung vị là "
                    r"trung bình cộng của hai số liệu đứng giữa, tức số thứ "
                    r"$%d$ và thứ $%d$:"
                    "\\\\\n"
                    r"$M_e = \dfrac{%s + %s}{2} = %s$."
                    % (n, n, n // 2, n // 2 + 1,
                       _xx5(Z[n // 2 - 1]), _xx5(Z[n // 2]), _xx5(tv)))
        giai = (r"\textbf{Bước 1.} Sắp xếp mẫu số liệu theo thứ tự không "
                r"giảm:"
                "\\\\\n" + _bang(Z) +
                "\\\\\n"
                r"\textbf{Bước 2.} " + cach)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B13_TH073_SA_A_01(socau):
    r"""Trung vị của mẫu - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([5, 6, 7, 8, 9])
        X = _mau_so_lieu(n, 15, 55, lambda Y: _dep(_trung_vi(Y), 2))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        Y = list(X)
        random.shuffle(Y)
        Z = sorted(Y)
        tv = _trung_vi(Z)
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Y) + r"\end{center}" +
                 "\n" + r"Tìm trung vị của mẫu số liệu.")
        giai = (r"Sắp xếp theo thứ tự không giảm:"
                "\\\\\n" + _bang(Z) +
                "\\\\\n"
                r"Mẫu có $%d$ số liệu nên trung vị $M_e = %s$."
                % (len(Z), _xx5(tv)))
        nhieu = _ba_nhieu5(_xx5(tv), [_xx5(_so_trung_binh(Z)), _xx5(max(Z)),
                                      _xx5(min(Z))],
                           buoc=lambda t: _xx5(tv + t))
        cau += MC_SA_answer_text(debai, _xx5(tv), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B13_TH074_MC_A_01(socau, dang=1):
    r"""Tìm tứ phân vị của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([8, 9, 10, 11])
        X = _mau_so_lieu(n, 10, 50,
                         lambda Y: all(_dep(q, 2) for q in _tu_phan_vi(Y)))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        q1, q2, q3 = _tu_phan_vi(Z)
        dung = (r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$"
                % (_xx5(q1), _xx5(q2), _xx5(q3)))
        nhieu = [r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$"
                 % (_xx5(q3), _xx5(q2), _xx5(q1)),
                 r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$"
                 % (_xx5(min(Z)), _xx5(q2), _xx5(max(Z))),
                 r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$"
                 % (_xx5(q1), _xx5(_so_trung_binh(Z)), _xx5(q3)),
                 r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$"
                 % (_xx5(q1 + 1), _xx5(q2), _xx5(q3 + 1))]
        n = len(Z)
        if n % 2 == 1:
            chia = (r"Mẫu có $%d$ số liệu (lẻ) nên $Q_2 = %s$ là số đứng "
                    r"giữa; nửa bên trái gồm $%d$ số liệu đầu, nửa bên phải "
                    r"gồm $%d$ số liệu cuối - \textbf{không} tính $Q_2$ vào "
                    r"hai nửa." % (n, _xx5(q2), n // 2, n // 2))
        else:
            chia = (r"Mẫu có $%d$ số liệu (chẵn) nên $Q_2$ là trung bình "
                    r"cộng hai số giữa: $Q_2 = %s$; nửa bên trái gồm $%d$ số "
                    r"liệu đầu, nửa bên phải gồm $%d$ số liệu cuối."
                    % (n, _xx5(q2), n // 2, n // 2))
        debai = (r"Cho mẫu số liệu đã sắp xếp theo thứ tự không giảm:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Ba tứ phân vị của mẫu số liệu trên là")
        giai = (chia +
                "\\\\\n"
                r"$Q_1$ là trung vị của nửa bên trái: $Q_1 = %s$."
                % _xx5(q1) +
                "\\\\\n"
                r"$Q_3$ là trung vị của nửa bên phải: $Q_3 = %s$."
                % _xx5(q3))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B13_TH074_SA_A_01(socau):
    r"""Tứ phân vị thứ nhất hoặc thứ ba - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([8, 9, 10, 11, 12])
        thu = random.choice([1, 3])
        X = _mau_so_lieu(n, 10, 50,
                         lambda Y: all(_dep(q, 2) for q in _tu_phan_vi(Y)))
        if X is None or (tuple(X), thu) in gt:
            continue
        gt.append((tuple(X), thu))

    cau = ""
    for X, thu in gt:
        Z = list(X)
        q1, q2, q3 = _tu_phan_vi(Z)
        kq = q1 if thu == 1 else q3
        nua = "bên trái" if thu == 1 else "bên phải"
        debai = (r"Cho mẫu số liệu đã sắp xếp theo thứ tự không giảm:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tìm tứ phân vị thứ %s $Q_{%d}$ của mẫu số liệu."
                 % ("nhất" if thu == 1 else "ba", thu))
        giai = (r"Trước hết $Q_2$ là trung vị của cả mẫu: $Q_2 = %s$."
                % _xx5(q2) +
                "\\\\\n"
                r"$Q_{%d}$ là trung vị của nửa %s (mẫu có $%d$ số liệu%s)."
                % (thu, nua, len(Z),
                   ", số đứng giữa không thuộc nửa nào" if len(Z) % 2 else "") +
                "\\\\\n"
                r"Vậy $Q_{%d} = %s$." % (thu, _xx5(kq)))
        nhieu = _ba_nhieu5(_xx5(kq), [_xx5(q2), _xx5(q3 if thu == 1 else q1),
                                      _xx5(_so_trung_binh(Z))],
                           buoc=lambda t: _xx5(kq + t))
        cau += MC_SA_answer_text(debai, _xx5(kq), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B13_TH075_MC_A_01(socau, dang=1):
    r"""Tìm mốt của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        goc = random.sample(range(5, 20), 4)
        mot = random.choice(goc)
        X = sorted(goc + [mot, mot])
        if tuple(X) in gt or len(_mot(X)) != 1:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        mot = _mot(Z)[0]
        dem = Z.count(mot)
        dung = r"$%s$" % _xx5(mot)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(mot), [_xx5(dem), _xx5(_trung_vi(Z)), _xx5(max(Z)),
                        _xx5(min(Z))],
            buoc=lambda t: _xx5(mot + t))]
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Mốt của mẫu số liệu trên bằng bao nhiêu?")
        giai = (r"Mốt là giá trị \textbf{xuất hiện nhiều lần nhất} trong mẫu "
                r"số liệu."
                "\\\\\n"
                r"Đếm số lần xuất hiện: giá trị $%s$ xuất hiện $%d$ lần, các "
                r"giá trị khác đều chỉ xuất hiện $1$ lần."
                % (_xx5(mot), dem) +
                "\\\\\n"
                r"Vậy mốt của mẫu là $M_o = %s$. Chú ý mốt là \textbf{giá "
                r"trị}, không phải số lần xuất hiện." % _xx5(mot))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B13_TH075_SA_A_01(socau):
    r"""Mốt của mẫu - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        goc = random.sample(range(10, 30), 5)
        mot = random.choice(goc)
        X = sorted(goc + [mot, mot])
        if tuple(X) in gt or len(_mot(X)) != 1:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        Z = list(X)
        mot = _mot(Z)[0]
        dem = Z.count(mot)
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tìm mốt của mẫu số liệu.")
        giai = (r"Giá trị $%s$ xuất hiện $%d$ lần, nhiều hơn mọi giá trị "
                r"khác. Vậy $M_o = %s$." % (_xx5(mot), dem, _xx5(mot)))
        nhieu = _ba_nhieu5(_xx5(mot), [_xx5(dem), _xx5(_trung_vi(Z)),
                                       _xx5(max(Z))],
                           buoc=lambda t: _xx5(mot + t))
        cau += MC_SA_answer_text(debai, _xx5(mot), nhieu, giai, 0, 0, 2)
    return cau


def _toa(x):
    """Số dùng LÀM TOẠ ĐỘ TikZ - luôn dấu CHẤM.

    Không được dùng _xx5 ở đây: _xx5 đổi dấu chấm thành dấu phẩy theo
    cách viết số Việt Nam, TikZ sẽ đọc (4.4, 2.2) thành bốn số và hình
    vẽ méo hoàn toàn (đã vấp đúng lỗi này khi dựng hình chương 4).
    """
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _hinh_bieu_do_hop(nho_nhat, q1, q2, q3, lon_nhat, ngoai_le=()):
    """Biểu đồ hộp (box plot) bằng TikZ thuần.

    Trục được co về bề ngang 10 cm để hình luôn vừa khổ, dù số liệu lớn.
    """
    cac_diem = [nho_nhat, lon_nhat] + list(ngoai_le)
    lo, hi = min(cac_diem), max(cac_diem)
    bien = (hi - lo) * 0.12 or 1.0
    lo, hi = lo - bien, hi + bien

    def X(v):
        return 10.0 * (v - lo) / (hi - lo)

    ra = ["\\begin{tikzpicture}[>=stealth,x=1cm,y=1cm,thick,scale=1]"]
    # trục
    ra.append("\\draw[->] (-0.3,0) -- (10.6,0) node[below right]"
              "{\\footnotesize $x$};")
    # hộp
    ra.append("\\draw (%s,0.45) rectangle (%s,1.45);" % (_toa(X(q1)),
                                                         _toa(X(q3))))
    ra.append("\\draw[very thick] (%s,0.45) -- (%s,1.45);"
              % (_toa(X(q2)), _toa(X(q2))))
    # râu
    ra.append("\\draw (%s,0.95) -- (%s,0.95);" % (_toa(X(nho_nhat)),
                                                  _toa(X(q1))))
    ra.append("\\draw (%s,0.95) -- (%s,0.95);" % (_toa(X(q3)),
                                                  _toa(X(lon_nhat))))
    ra.append("\\draw (%s,0.6) -- (%s,1.3);" % (_toa(X(nho_nhat)),
                                                _toa(X(nho_nhat))))
    ra.append("\\draw (%s,0.6) -- (%s,1.3);" % (_toa(X(lon_nhat)),
                                                _toa(X(lon_nhat))))
    # nhãn năm mốc
    for v, ten in ((nho_nhat, "\\footnotesize $%s$" % _xx5(nho_nhat)),
                   (q1, "\\footnotesize $%s$" % _xx5(q1)),
                   (q2, "\\footnotesize $%s$" % _xx5(q2)),
                   (q3, "\\footnotesize $%s$" % _xx5(q3)),
                   (lon_nhat, "\\footnotesize $%s$" % _xx5(lon_nhat))):
        ra.append("\\draw (%s,0) -- (%s,-0.12) node[below]{%s};"
                  % (_toa(X(v)), _toa(X(v)), ten))
    # giá trị ngoại lệ vẽ bằng dấu chấm tròn
    for v in ngoai_le:
        ra.append("\\fill[black] (%s,0.95) circle[radius=2pt];" % _toa(X(v)))
        ra.append("\\draw (%s,0) -- (%s,-0.12) node[below]"
                  "{\\footnotesize $%s$};" % (_toa(X(v)), _toa(X(v)),
                                              _xx5(v)))
    ra.append("\\end{tikzpicture}")
    return "\n".join(ra)


def L10_C5_B13_TH076_MC_A_01(socau, dang=1):
    r"""Ý nghĩa của số trung bình, trung vị, mốt trong tình huống thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    TINH_HUONG = [
        (r"Thu nhập của $10$ nhân viên trong một công ty, trong đó có một "
         r"người là giám đốc với thu nhập cao vượt trội",
         r"Trung vị",
         r"Số trung bình bị một giá trị quá lớn kéo lên rất cao nên không "
         r"còn đại diện cho mức thu nhập chung; trung vị thì không bị ảnh "
         r"hưởng bởi giá trị bất thường."),
        (r"Cỡ giày mà một cửa hàng bán được nhiều nhất trong tháng",
         r"Mốt",
         r"Cửa hàng cần biết cỡ giày nào bán chạy nhất để nhập hàng, tức là "
         r"giá trị xuất hiện nhiều lần nhất - đó chính là mốt."),
        (r"Điểm trung bình môn Toán của một lớp mà điểm các bạn khá đồng đều",
         r"Số trung bình",
         r"Khi số liệu không có giá trị bất thường và khá đồng đều thì số "
         r"trung bình đại diện tốt nhất, lại dùng hết mọi số liệu."),
    ]
    LUA_CHON = ["Số trung bình", "Trung vị", "Mốt", "Khoảng biến thiên"]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(TINH_HUONG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(TINH_HUONG):
            break

    cauTN = ""
    for i in gt:
        mo_ta, dap, ly_do = TINH_HUONG[i]
        dung = dap
        nhieu = [t for t in LUA_CHON if t != dap]
        debai = (r"%s. Số đặc trưng nào sau đây \textbf{đại diện tốt nhất} "
                 r"cho mẫu số liệu trong tình huống này?" % mo_ta)
        giai = (ly_do +
                "\\\\\n"
                r"Khoảng biến thiên đo \textbf{độ phân tán}, không phải xu "
                r"thế trung tâm, nên không dùng để đại diện cho mẫu.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B13_VD077_MC_A_01(socau, dang=1):
    r"""Rút ra kết luận từ số đặc trưng đo xu thế trung tâm.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = 9
        nen = sorted(random.randint(6, 12) for _ in range(n - 1))
        la = random.choice([60, 80, 100])
        X = sorted(nen + [la])
        if tuple(X) in gt or not _dep(_so_trung_binh(X), 2):
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        tb = _so_trung_binh(Z)
        tv = _trung_vi(Z)
        dung = (r"Trung vị, vì mẫu có một giá trị quá lớn làm số trung bình "
                r"không còn đại diện được")
        nhieu = [r"Số trung bình, vì nó dùng hết mọi số liệu của mẫu",
                 r"Mốt, vì đó là giá trị xuất hiện nhiều lần nhất",
                 r"Cả số trung bình và trung vị đều đại diện tốt như nhau",
                 r"Khoảng biến thiên, vì nó cho biết mẫu trải rộng bao nhiêu"]
        debai = (r"Số tiền (đơn vị: triệu đồng) mà $9$ hộ gia đình trong một "
                 r"khu phố đóng góp cho quỹ từ thiện được ghi lại:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" +
                 r"Nên dùng số đặc trưng nào để đại diện cho mức đóng góp "
                 r"của khu phố này, và vì sao?")
        giai = (r"Số trung bình: $\overline{x} = \dfrac{%s}{9} = %s$ (triệu "
                r"đồng)." % (_xx5(sum(Z)), _xx5(tb)) +
                "\\\\\n"
                r"Trung vị: sắp xếp rồi lấy số đứng giữa, được $M_e = %s$ "
                r"(triệu đồng)." % _xx5(tv) +
                "\\\\\n"
                r"Có tới $8$ trên $9$ hộ đóng góp không quá $%s$ triệu, "
                r"nhưng một hộ đóng $%s$ triệu đã kéo số trung bình lên "
                r"$%s$ - cao hơn hẳn mức đóng góp của đa số."
                % (_xx5(max(Z[:-1])), _xx5(max(Z)), _xx5(tb)) +
                "\\\\\n"
                r"Vậy \textbf{trung vị} đại diện tốt hơn, vì trung vị không "
                r"bị giá trị bất thường làm lệch.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B13_VD077_TL_A_01(socau, dong=1):
    r"""Tự luận: so sánh hai mẫu số liệu và kết luận.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        A = _mau_so_lieu(6, 5, 10, lambda Y: _dep(_so_trung_binh(Y), 2)
                         and _dep(_trung_vi(Y), 2))
        B = _mau_so_lieu(6, 4, 11, lambda Y: _dep(_so_trung_binh(Y), 2)
                         and _dep(_trung_vi(Y), 2))
        if A is None or B is None:
            continue
        if abs(_so_trung_binh(A) - _so_trung_binh(B)) < 0.3:
            continue
        v = (tuple(A), tuple(B))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for A, B in gt:
        A, B = list(A), list(B)
        tbA, tbB = _so_trung_binh(A), _so_trung_binh(B)
        tvA, tvB = _trung_vi(A), _trung_vi(B)
        hon = "An" if tbA > tbB else "Bình"

        debai = (r"Điểm kiểm tra môn Toán trong $6$ lần của hai bạn An và "
                 r"Bình được ghi lại:"
                 "\\\\\n"
                 r"An: \quad " + _bang(A) +
                 "\\\\\n"
                 r"Bình: \quad " + _bang(B))

        hoi_a = r"Tính số trung bình điểm của mỗi bạn."
        giai_a = (r"An: $\overline{x}_A = \dfrac{%s}{6} = %s$."
                  % (_xx5(sum(A)), _xx5(tbA)) +
                  "\\\\\n"
                  r"Bình: $\overline{x}_B = \dfrac{%s}{6} = %s$."
                  % (_xx5(sum(B)), _xx5(tbB)))

        hoi_b = r"Tìm trung vị điểm của mỗi bạn."
        giai_b = (r"An (đã sắp xếp): " + _bang(sorted(A)) +
                  r" nên $M_e = %s$." % _xx5(tvA) +
                  "\\\\\n"
                  r"Bình (đã sắp xếp): " + _bang(sorted(B)) +
                  r" nên $M_e = %s$." % _xx5(tvB))

        hoi_c = r"Theo em, bạn nào học tốt hơn? Giải thích."
        giai_c = (r"Bạn %s có cả số trung bình lẫn trung vị cao hơn nên "
                  r"nhìn chung học tốt hơn." % hon +
                  "\\\\\n"
                  r"Lưu ý: chỉ so số trung bình thôi thì chưa đủ chắc, vì "
                  r"số trung bình dễ bị một điểm quá cao hoặc quá thấp làm "
                  r"lệch. Khi cả hai số đặc trưng cùng nghiêng về một bạn "
                  r"thì kết luận mới vững.")

        ds_abcd = [(hoi_a, r"\overline{x}_A = %s,\ \overline{x}_B = %s"
                    % (_xx5(tbA), _xx5(tbB)), giai_a),
                   (hoi_b, r"M_e(A) = %s,\ M_e(B) = %s"
                    % (_xx5(tvA), _xx5(tvB)), giai_b),
                   (hoi_c, r"\text{Bạn %s}" % hon, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C5_B13_VD078_MC_A_01(socau, dang=1):
    r"""Tìm giá trị ngoại lệ của mẫu số liệu qua BIỂU ĐỒ HỘP.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Có HÌNH VẼ (biểu đồ hộp) đúng yêu cầu cô Lan chốt: câu có hình phải
    hiện được hình cả trên web, không thì mức độ của câu bị lệch.
    """
    gt = []
    while len(gt) < socau:
        q1 = random.randint(20, 35)
        delta = random.choice([4, 6, 8, 10])
        q3 = q1 + delta
        q2 = random.randint(q1 + 1, q3 - 1)
        nho = q1 - random.randint(1, int(1.5 * delta) - 1)
        lon = q3 + random.randint(1, int(1.5 * delta) - 1)
        ngoai = q3 + int(1.5 * delta) + random.randint(1, 5)
        v = (q1, q2, q3, nho, lon, ngoai)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for q1, q2, q3, nho, lon, ngoai in gt:
        delta = q3 - q1
        tren = q3 + 1.5 * delta
        duoi = q1 - 1.5 * delta
        hinh = _hinh_bieu_do_hop(nho, q1, q2, q3, lon, (ngoai,))
        dung = r"$%s$" % _xx5(ngoai)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(ngoai), [_xx5(lon), _xx5(nho), _xx5(q3), _xx5(q1)],
            buoc=lambda t: _xx5(ngoai + t))]
        debai = (r"Biểu đồ hộp sau mô tả một mẫu số liệu. Giá trị nào là "
                 r"\textbf{giá trị ngoại lệ} của mẫu?")
        giai = (r"Đọc trên biểu đồ hộp: $Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$."
                % (_xx5(q1), _xx5(q2), _xx5(q3)) +
                "\\\\\n"
                r"Khoảng tứ phân vị $\Delta_Q = Q_3 - Q_1 = %s - %s = %s$."
                % (_xx5(q3), _xx5(q1), _xx5(delta)) +
                "\\\\\n"
                r"Giá trị $x$ là ngoại lệ khi "
                r"$x < Q_1 - 1{,}5\Delta_Q$ hoặc $x > Q_3 + 1{,}5\Delta_Q$."
                "\\\\\n"
                r"$Q_1 - 1{,}5\Delta_Q = %s$; $Q_3 + 1{,}5\Delta_Q = %s$."
                % (_xx5(duoi), _xx5(tren)) +
                "\\\\\n"
                r"Chỉ có $%s > %s$ nên $%s$ là giá trị ngoại lệ; $%s$ và "
                r"$%s$ vẫn nằm trong khoảng cho phép."
                % (_xx5(ngoai), _xx5(tren), _xx5(ngoai), _xx5(nho),
                   _xx5(lon)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


# =====================================================================
# BÀI 14. CÁC SỐ ĐẶC TRƯNG ĐO ĐỘ PHÂN TÁN
# =====================================================================

def _mau_phuong_sai_dep(n, lo, hi, can_do_lech=False, lan_thu=600):
    """Mẫu n số nguyên có phương sai (và nếu cần cả độ lệch chuẩn) đẹp.

    Câu trả lời ngắn chấm bằng so khớp chuỗi nên đáp số phải là số thập
    phân hữu hạn. Độ lệch chuẩn là CĂN của phương sai nên hầu hết bộ số
    cho kết quả vô tỉ - phải lọc lấy bộ có căn đúng.
    """
    for _ in range(lan_thu):
        X = sorted(random.randint(lo, hi) for _ in range(n))
        if len(set(X)) < 2:
            continue
        ps = _phuong_sai(X)
        if not _dep(ps, 2):
            continue
        if can_do_lech:
            s = math.sqrt(ps)
            if not _dep(s, 1) or s < 0.5:
                continue
        return X
    return None


def L10_C5_B14_NB085_MC_A_01(socau, dang=1):
    r"""Liên hệ giữa thống kê với môn học khác và thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    DUNG = [
        (r"Trong môn Địa lí, người ta dùng số trung bình để mô tả lượng mưa "
         r"trung bình năm của một vùng",
         r"lượng mưa mỗi năm một khác, số trung bình cho biết mức chung của "
         r"cả giai đoạn"),
        (r"Trong môn Sinh học, người ta dùng độ lệch chuẩn để so sánh mức độ "
         r"đồng đều về chiều cao của hai giống cây",
         r"độ lệch chuẩn đo độ phân tán: giống nào có độ lệch chuẩn nhỏ hơn "
         r"thì chiều cao đồng đều hơn"),
        (r"Trong sản xuất, người ta theo dõi độ lệch chuẩn khối lượng sản "
         r"phẩm để đánh giá độ ổn định của dây chuyền",
         r"dây chuyền ổn định thì khối lượng các sản phẩm ít chênh lệch, tức "
         r"độ lệch chuẩn nhỏ"),
    ]
    # SUA 29/09/2026 (co Lan bao loi): cau dan hoi ve UNG DUNG thong ke
    # trong mon hoc khac va thuc tien, nhung 4 phuong an nhieu cu lai la
    # cau LI THUYET thuan ("Phuong sai co the am"...) -> chi mot phuong an
    # noi ve ung dung, hoc sinh loai tru la ra dap an. Nay moi phuong an
    # nhieu cung la mot tinh huong ung dung, nhung dung SAI so dac trung
    # hoac hieu SAI y nghia cua no. Moi cau sai kem ly do de loi giai giai
    # thich dung ba phuong an nhieu xuat hien trong cau.
    SAI = [
        (r"Trong sản xuất, dây chuyền có độ lệch chuẩn khối lượng sản phẩm "
         r"càng lớn thì hoạt động càng ổn định",
         r"độ lệch chuẩn lớn nghĩa là khối lượng các sản phẩm chênh lệch "
         r"nhiều, dây chuyền kém ổn định"),
        (r"Trong môn Sinh học, muốn biết giống cây nào có chiều cao đồng đều "
         r"hơn thì chỉ cần so sánh chiều cao trung bình của hai giống",
         r"số trung bình chỉ cho biết mức chung; muốn so sánh độ đồng đều "
         r"phải dùng số đo độ phân tán như phương sai, độ lệch chuẩn"),
        (r"Trong môn Địa lí, khoảng biến thiên của nhiệt độ các tháng trong "
         r"năm cho biết nhiệt độ trung bình năm của một địa phương",
         r"khoảng biến thiên $R = x_{\max} - x_{\min}$ chỉ đo độ chênh lệch "
         r"giữa tháng nóng nhất và tháng lạnh nhất, không phải mức trung bình"),
        (r"Khi so sánh hai vận động viên bắn súng có cùng điểm trung bình, "
         r"người có phương sai điểm số lớn hơn là người bắn ổn định hơn",
         r"phương sai lớn nghĩa là điểm số phân tán nhiều, người đó bắn "
         r"kém ổn định hơn"),
        (r"Khi khảo sát thu nhập ở một khu phố có vài hộ thu nhập rất cao, "
         r"số trung bình luôn phản ánh mức thu nhập phổ biến tốt hơn trung vị",
         r"số trung bình bị kéo lên bởi các giá trị ngoại lệ, lúc này trung "
         r"vị phản ánh mức phổ biến tốt hơn"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(DUNG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(DUNG):
            break

    cauTN = ""
    for i in gt:
        mo_ta, ly_do = DUNG[i]
        ba_sai = random.sample(SAI, 3)
        debai = (r"Khẳng định nào sau đây về ứng dụng của thống kê trong "
                 r"thực tiễn và trong các môn học khác là \textbf{đúng}?")
        giai = (r"``%s'' là đúng, vì %s." % (mo_ta, ly_do) +
                "\\\\\n"
                r"Các khẳng định còn lại đều sai:" +
                "".join("\\\\\n" + r"- ``%s'': sai, vì %s." % (t, ld)
                        for t, ld in ba_sai))
        cauTN += _MC_khong_cham(debai, "%s." % mo_ta,
                                   ["%s." % t for t, _ in ba_sai],
                                   giai, 0, 0, dang)
    return cauTN



# CLAUDE THEM 29/09/2026 - kho cau cho cac bien the 02, 03 cua NB085.
_UD_DUNG = [
    (r"Trong môn Địa lí, người ta dùng số trung bình để mô tả lượng mưa "
     r"trung bình năm của một vùng",
     r"lượng mưa mỗi năm một khác, số trung bình cho biết mức chung"),
    (r"Trong môn Sinh học, người ta dùng độ lệch chuẩn để so sánh mức độ "
     r"đồng đều về chiều cao của hai giống cây",
     r"độ lệch chuẩn đo độ phân tán của số liệu"),
    (r"Trong sản xuất, người ta theo dõi độ lệch chuẩn khối lượng sản phẩm "
     r"để đánh giá độ ổn định của dây chuyền",
     r"khối lượng càng ít chênh lệch thì dây chuyền càng ổn định"),
    (r"Trong môn Vật lí, người ta đo một đại lượng nhiều lần rồi lấy giá trị "
     r"trung bình để giảm sai số của phép đo",
     r"các lần đo lệch lên, lệch xuống bù trừ cho nhau"),
    (r"Trong y tế, người ta thống kê số ca bệnh theo từng tuần để kịp thời "
     r"phát hiện dấu hiệu bùng phát dịch",
     r"số liệu theo thời gian cho thấy xu hướng tăng bất thường"),
    (r"Một cửa hàng thống kê số áo bán được theo từng cỡ và dựa vào mốt để "
     r"quyết định nhập thêm cỡ nào",
     r"mốt là cỡ áo bán được nhiều nhất"),
    (r"Để so sánh kết quả học tập của hai lớp, người ta dùng cả điểm trung "
     r"bình và độ lệch chuẩn của điểm số",
     r"điểm trung bình cho mức chung, độ lệch chuẩn cho độ đồng đều"),
]
_UD_SAI = [
    (r"Trong sản xuất, dây chuyền có độ lệch chuẩn khối lượng sản phẩm "
     r"càng lớn thì hoạt động càng ổn định",
     r"độ lệch chuẩn lớn nghĩa là khối lượng chênh lệch nhiều, dây chuyền "
     r"kém ổn định"),
    (r"Trong môn Sinh học, muốn biết giống cây nào có chiều cao đồng đều "
     r"hơn thì chỉ cần so sánh chiều cao trung bình của hai giống",
     r"số trung bình chỉ cho mức chung; độ đồng đều phải xét phương sai, độ "
     r"lệch chuẩn"),
    (r"Trong môn Địa lí, khoảng biến thiên của nhiệt độ các tháng trong năm "
     r"cho biết nhiệt độ trung bình năm của một địa phương",
     r"khoảng biến thiên chỉ đo độ chênh lệch giữa tháng nóng nhất và tháng "
     r"lạnh nhất"),
    (r"Trong môn Vật lí, đo một đại lượng càng nhiều lần thì giá trị trung "
     r"bình của các lần đo càng kém tin cậy",
     r"đo nhiều lần rồi lấy trung bình giúp giảm sai số ngẫu nhiên"),
    (r"Khi so sánh hai vận động viên bắn súng có cùng điểm trung bình, người "
     r"có phương sai điểm số lớn hơn là người bắn ổn định hơn",
     r"phương sai lớn nghĩa là điểm số phân tán nhiều, bắn kém ổn định hơn"),
]


def L10_C5_B14_NB085_MC_A_02(socau, dang=1):
    r"""Liên hệ giữa thống kê với môn học khác và thực tiễn - HỎI NGƯỢC:
    khẳng định nào SAI.

    CLAUDE THEM 29/09/2026 - bien the 02, cung dang voi _01 (mapping: "Lien
    he giua thong ke voi mon hoc khac va thuc tien"). _01 hoi khang dinh
    DUNG; _02 cho ba ung dung dung va mot ung dung sai. Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 200:
        lan += 1
        i = random.randrange(len(_UD_SAI))
        if i not in gt:
            gt.append(i)

    cauTN = ""
    for i in gt:
        sai, ly_do = _UD_SAI[i]
        ba_dung = random.sample(_UD_DUNG, 3)
        debai = (r"Khẳng định nào sau đây về ứng dụng của thống kê trong thực "
                 r"tiễn và trong các môn học khác là \textbf{sai}?")
        giai = (r"``%s'' là sai, vì %s." % (sai, ly_do) +
                "".join("\\\\\n" + r"- ``%s'': đúng, vì %s." % (t, ld)
                        for t, ld in ba_dung))
        cauTN += _MC_khong_cham(debai, "%s." % sai,
                                   ["%s." % t for t, _ in ba_dung], giai, 0, 0, dang)
    return cauTN


_TH_CO_THONG_KE = [
    (r"Một trạm khí tượng ghi nhiệt độ lúc 12 giờ trưa của cả 30 ngày trong "
     r"tháng để biết nhiệt độ trung bình của tháng đó",
     r"phải thu thập 30 số liệu rồi tính số trung bình"),
    (r"Lớp trưởng hỏi thời gian tự học mỗi ngày của từng bạn trong lớp rồi "
     r"lập bảng tần số",
     r"thu thập số liệu của nhiều bạn và trình bày thành bảng tần số"),
    (r"Một cửa hàng ghi lại số đôi giày bán được theo từng cỡ trong tháng "
     r"để quyết định nhập thêm cỡ nào",
     r"thu thập số liệu bán hàng rồi tìm cỡ bán chạy nhất (mốt)"),
    (r"Trong giờ Vật lí, một nhóm học sinh đo chu kì dao động của con lắc 5 "
     r"lần rồi lấy giá trị trung bình",
     r"xử lí 5 số liệu đo được bằng số trung bình"),
    (r"Một bác sĩ ghi huyết áp của bệnh nhân mỗi sáng trong hai tuần để xem "
     r"huyết áp dao động nhiều hay ít",
     r"thu thập nhiều số liệu rồi xét độ phân tán của chúng"),
]
_TH_KHONG_THONG_KE = [
    # Viet dai tuong duong phuong an dung de hoc sinh khong doan theo do dai
    r"Một bác nông dân tính diện tích mảnh vườn hình chữ nhật dài $20$ m, "
    r"rộng $12$ m để biết cần mua bao nhiêu phân bón",
    r"Một tài xế tính quãng đường ô tô đi được trong $2$ giờ khi chạy với "
    r"vận tốc không đổi $50$ km/h",
    r"Trong giờ Toán, một học sinh giải phương trình $2x - 6 = 0$ để tìm "
    r"chiều dài còn thiếu của một đoạn dây",
    r"Một kĩ sư tính số đo góc còn lại của một khung tam giác khi đã biết "
    r"số đo của hai góc kia",
    r"Một người thợ tính chu vi của một nắp bể hình tròn bán kính $3$ dm để "
    r"cắt gioăng cao su vừa khít",
    r"Trong giờ Hoá học, một học sinh tính khối lượng mol của phân tử nước "
    r"từ khối lượng mol của hiđro và oxi",
]


def L10_C5_B14_NB085_MC_A_03(socau, dang=1):
    r"""Liên hệ giữa thống kê với thực tiễn - nhận ra tình huống nào CẦN
    dùng kiến thức thống kê (thu thập, xử lí số liệu).

    CLAUDE THEM 29/09/2026 - bien the 03, cung dang voi _01. Kieu cau khac:
    phan biet tinh huong thong ke (nhieu so lieu quan sat) voi tinh huong
    chi la mot phep tinh theo cong thuc. Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 200:
        lan += 1
        i = random.randrange(len(_TH_CO_THONG_KE))
        if i not in gt:
            gt.append(i)

    cauTN = ""
    for i in gt:
        co, ly_do = _TH_CO_THONG_KE[i]
        ba_khong = random.sample(_TH_KHONG_THONG_KE, 3)
        debai = (r"Tình huống nào sau đây cần dùng đến kiến thức thống kê (thu "
                 r"thập, xử lí số liệu)?")
        giai = (r"``%s'': cần dùng thống kê, vì %s." % (co, ly_do) +
                "\\\\\n"
                r"Ba tình huống còn lại chỉ là một phép tính theo công thức "
                r"(hoặc giải phương trình) với số liệu cho sẵn, không cần thu "
                r"thập hay xử lí một mẫu số liệu.")
        cauTN += _MC_khong_cham(debai, "%s." % co,
                                   ["%s." % t for t in ba_khong], giai, 0, 0, dang)
    return cauTN

def L10_C5_B14_TH079_MC_A_01(socau, dang=1):
    r"""Tính khoảng biến thiên của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_so_lieu(random.choice([6, 7, 8]), 10, 60)
        if X is None or len(set(X)) < 3 or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        R = max(Z) - min(Z)
        dung = r"$%s$" % _xx5(R)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(R), [_xx5(max(Z) + min(Z)), _xx5(max(Z)), _xx5(min(Z)),
                      _xx5(_so_trung_binh(Z))],
            buoc=lambda t: _xx5(R + t))]
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Khoảng biến thiên của mẫu số liệu bằng bao nhiêu?")
        giai = (r"Khoảng biến thiên bằng giá trị lớn nhất trừ giá trị nhỏ "
                r"nhất:"
                "\\\\\n"
                r"$R = x_{\max} - x_{\min} = %s - %s = %s$."
                % (_xx5(max(Z)), _xx5(min(Z)), _xx5(R)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_TH079_SA_A_01(socau):
    r"""Khoảng biến thiên - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_so_lieu(random.choice([7, 8, 9]), 15, 70)
        if X is None or len(set(X)) < 3 or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        Z = list(X)
        R = max(Z) - min(Z)
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tính khoảng biến thiên của mẫu số liệu.")
        giai = (r"$R = x_{\max} - x_{\min} = %s - %s = %s$."
                % (_xx5(max(Z)), _xx5(min(Z)), _xx5(R)))
        nhieu = _ba_nhieu5(_xx5(R), [_xx5(max(Z) + min(Z)), _xx5(max(Z)),
                                     _xx5(min(Z))],
                           buoc=lambda t: _xx5(R + t))
        cau += MC_SA_answer_text(debai, _xx5(R), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B14_TH080_MC_A_01(socau, dang=1):
    r"""Tính khoảng tứ phân vị của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([8, 9, 10, 11])
        X = _mau_so_lieu(n, 10, 50,
                         lambda Y: all(_dep(q, 2) for q in _tu_phan_vi(Y)))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        q1, q2, q3 = _tu_phan_vi(Z)
        delta = q3 - q1
        dung = r"$%s$" % _xx5(delta)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(delta), [_xx5(q3 + q1), _xx5(max(Z) - min(Z)), _xx5(q2),
                          _xx5(q3)],
            buoc=lambda t: _xx5(delta + t))]
        debai = (r"Cho mẫu số liệu đã sắp xếp theo thứ tự không giảm:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Khoảng tứ phân vị của mẫu bằng bao nhiêu?")
        giai = (r"Trước hết tìm ba tứ phân vị: $Q_1 = %s$, $Q_2 = %s$, "
                r"$Q_3 = %s$." % (_xx5(q1), _xx5(q2), _xx5(q3)) +
                "\\\\\n"
                r"Khoảng tứ phân vị "
                r"$\Delta_Q = Q_3 - Q_1 = %s - %s = %s$."
                % (_xx5(q3), _xx5(q1), _xx5(delta)) +
                "\\\\\n"
                r"Khác với khoảng biến thiên, $\Delta_Q$ chỉ đo độ trải của "
                r"$50\%$ số liệu ở giữa nên \textbf{không} bị giá trị ngoại "
                r"lệ làm lệch.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_TH080_SA_A_01(socau):
    r"""Khoảng tứ phân vị - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([8, 9, 10, 11, 12])
        X = _mau_so_lieu(n, 10, 60,
                         lambda Y: all(_dep(q, 2) for q in _tu_phan_vi(Y)))
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        Z = list(X)
        q1, q2, q3 = _tu_phan_vi(Z)
        delta = q3 - q1
        debai = (r"Cho mẫu số liệu đã sắp xếp theo thứ tự không giảm:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tính khoảng tứ phân vị của mẫu số liệu.")
        giai = (r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$."
                % (_xx5(q1), _xx5(q2), _xx5(q3)) +
                "\\\\\n"
                r"$\Delta_Q = Q_3 - Q_1 = %s - %s = %s$."
                % (_xx5(q3), _xx5(q1), _xx5(delta)))
        nhieu = _ba_nhieu5(_xx5(delta), [_xx5(q3 + q1), _xx5(max(Z) - min(Z)),
                                         _xx5(q2)],
                           buoc=lambda t: _xx5(delta + t))
        cau += MC_SA_answer_text(debai, _xx5(delta), nhieu, giai, 0, 0, 2)
    return cau


def _bang_tinh_phuong_sai(X):
    """Dòng lời giải trình bày từng bình phương độ lệch."""
    tb = _so_trung_binh(X)
    cac = [r"\left(%s - %s\right)^2" % (_xx5(x), _xx5(tb)) for x in X]
    return " + ".join(cac)


def L10_C5_B14_TH081_MC_A_01(socau, dang=1):
    r"""Tính phương sai của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Dùng đúng công thức lớp 10: chia cho $n$, KHÔNG phải $n-1$.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_phuong_sai_dep(random.choice([5, 6, 8]), 2, 15)
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        n = len(Z)
        tb = _so_trung_binh(Z)
        ps = _phuong_sai(Z)
        tong_bp = ps * n
        dung = r"$%s$" % _xx5(ps)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(ps), [_xx5(tong_bp / (n - 1)), _xx5(tong_bp),
                       _xx5(math.sqrt(ps)), _xx5(tb)],
            buoc=lambda t: _xx5(ps + t / 2.0))]
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Phương sai của mẫu số liệu bằng bao nhiêu?")
        giai = (r"\textbf{Bước 1.} Số trung bình: "
                r"$\overline{x} = \dfrac{%s}{%d} = %s$."
                % (_xx5(sum(Z)), n, _xx5(tb)) +
                "\\\\\n"
                r"\textbf{Bước 2.} Tổng các bình phương độ lệch:"
                "\\\\\n"
                r"$%s = %s$." % (_bang_tinh_phuong_sai(Z), _xx5(tong_bp)) +
                "\\\\\n"
                r"\textbf{Bước 3.} Phương sai "
                r"$s^2 = \dfrac{%s}{%d} = %s$."
                % (_xx5(tong_bp), n, _xx5(ps)) +
                "\\\\\n"
                r"Chú ý chương trình lớp 10 chia cho $n$ (số số liệu), "
                r"không chia cho $n-1$.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_TH081_SA_A_01(socau):
    r"""Phương sai của mẫu - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_phuong_sai_dep(random.choice([5, 6, 8, 10]), 2, 18)
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        Z = list(X)
        n = len(Z)
        tb = _so_trung_binh(Z)
        ps = _phuong_sai(Z)
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tính phương sai của mẫu số liệu.")
        giai = (r"$\overline{x} = \dfrac{%s}{%d} = %s$."
                % (_xx5(sum(Z)), n, _xx5(tb)) +
                "\\\\\n"
                r"$s^2 = \dfrac{1}{%d}\left[%s\right] = %s$."
                % (n, _bang_tinh_phuong_sai(Z), _xx5(ps)))
        nhieu = _ba_nhieu5(_xx5(ps), [_xx5(ps * n / (n - 1)), _xx5(ps * n),
                                      _xx5(math.sqrt(ps))],
                           buoc=lambda t: _xx5(ps + t / 2.0))
        cau += MC_SA_answer_text(debai, _xx5(ps), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B14_TH082_MC_A_01(socau, dang=1):
    r"""Tính độ lệch chuẩn của mẫu số liệu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Số liệu được lọc sao cho căn bậc hai của phương sai ra SỐ THẬP PHÂN
    HỮU HẠN - nếu không, đáp số là số vô tỉ, không so khớp được.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_phuong_sai_dep(random.choice([5, 6, 8]), 2, 16,
                                can_do_lech=True)
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTN = ""
    for X in gt:
        Z = list(X)
        n = len(Z)
        ps = _phuong_sai(Z)
        s = math.sqrt(ps)
        dung = r"$%s$" % _xx5(s)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            _xx5(s), [_xx5(ps), _xx5(s * s * n), _xx5(_so_trung_binh(Z)),
                      _xx5(s * 2)],
            buoc=lambda t: _xx5(s + t / 2.0))]
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Độ lệch chuẩn của mẫu số liệu bằng bao nhiêu?")
        giai = (r"Phương sai: $s^2 = \dfrac{1}{%d}\left[%s\right] = %s$."
                % (n, _bang_tinh_phuong_sai(Z), _xx5(ps)) +
                "\\\\\n"
                r"Độ lệch chuẩn là căn bậc hai của phương sai:"
                "\\\\\n"
                r"$s = \sqrt{%s} = %s$." % (_xx5(ps), _xx5(s)) +
                "\\\\\n"
                r"Độ lệch chuẩn có \textbf{cùng đơn vị} với số liệu nên dễ "
                r"so sánh hơn phương sai.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_TH082_SA_A_01(socau):
    r"""Độ lệch chuẩn - trả lời ngắn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_phuong_sai_dep(random.choice([5, 6, 8, 10]), 2, 18,
                                can_do_lech=True)
        if X is None or tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cau = ""
    for X in gt:
        Z = list(X)
        n = len(Z)
        ps = _phuong_sai(Z)
        s = math.sqrt(ps)
        debai = (r"Cho mẫu số liệu sau:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tính độ lệch chuẩn của mẫu số liệu.")
        giai = (r"$s^2 = \dfrac{1}{%d}\left[%s\right] = %s$."
                % (n, _bang_tinh_phuong_sai(Z), _xx5(ps)) +
                "\\\\\n"
                r"$s = \sqrt{%s} = %s$." % (_xx5(ps), _xx5(s)))
        nhieu = _ba_nhieu5(_xx5(s), [_xx5(ps), _xx5(ps * n),
                                     _xx5(_so_trung_binh(Z))],
                           buoc=lambda t: _xx5(s + t / 2.0))
        cau += MC_SA_answer_text(debai, _xx5(s), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B14_TH083_MC_A_01(socau, dang=1):
    r"""Ý nghĩa của độ phân tán trong tình huống thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    DUNG = [
        (r"Hai xạ thủ có điểm trung bình bằng nhau; xạ thủ nào có độ lệch "
         r"chuẩn nhỏ hơn thì bắn \textbf{ổn định} hơn",
         r"độ lệch chuẩn nhỏ nghĩa là các điểm số ít chênh lệch quanh giá "
         r"trị trung bình"),
        (r"Khoảng tứ phân vị \textbf{ít bị ảnh hưởng} bởi giá trị ngoại lệ "
         r"hơn khoảng biến thiên",
         r"khoảng biến thiên chỉ dùng giá trị lớn nhất và nhỏ nhất nên một "
         r"giá trị bất thường là làm nó đổi hẳn, còn khoảng tứ phân vị chỉ "
         r"đo độ trải của $50\%$ số liệu ở giữa"),
        (r"Phương sai và độ lệch chuẩn \textbf{luôn không âm}",
         r"cả hai đều được tính từ tổng các bình phương nên không thể âm"),
    ]
    SAI = [
        r"Độ lệch chuẩn càng lớn thì mẫu số liệu càng đồng đều",
        r"Khoảng biến thiên luôn nhỏ hơn khoảng tứ phân vị",
        r"Phương sai có cùng đơn vị đo với số liệu ban đầu",
        r"Hai mẫu có cùng số trung bình thì chắc chắn có cùng độ lệch chuẩn",
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(DUNG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(DUNG):
            break

    cauTN = ""
    for i in gt:
        mo_ta, ly_do = DUNG[i]
        debai = (r"Khẳng định nào sau đây về các số đặc trưng đo độ phân tán "
                 r"là \textbf{đúng}?")
        giai = (r"``%s'' đúng, vì %s." % (mo_ta, ly_do) +
                "\\\\\n"
                r"Các khẳng định còn lại đều sai. Chú ý: phương sai có đơn "
                r"vị là \textbf{bình phương} đơn vị số liệu, chỉ có độ lệch "
                r"chuẩn mới cùng đơn vị với số liệu; và hai mẫu cùng số "
                r"trung bình vẫn có thể phân tán rất khác nhau.")
        cauTN += _MC_khong_cham(debai, "%s." % mo_ta,
                                   ["%s." % t for t in SAI], giai, 0, 0, dang)
    return cauTN


def _cap_mau_khac_do_on_dinh(n, lo, hi, lan_thu=800):
    """Hai mẫu CÙNG số trung bình nhưng khác độ lệch chuẩn rõ rệt.

    Đây là tình huống kinh điển: chỉ nhìn số trung bình thì không phân
    biệt được, phải dùng độ lệch chuẩn.
    """
    for _ in range(lan_thu):
        A = _mau_phuong_sai_dep(n, lo, hi, can_do_lech=True, lan_thu=60)
        if A is None:
            continue
        tb = _so_trung_binh(A)
        if not float(tb).is_integer():
            continue
        B = _mau_phuong_sai_dep(n, lo, hi, can_do_lech=True, lan_thu=60)
        if B is None or _so_trung_binh(B) != tb:
            continue
        sa, sb = math.sqrt(_phuong_sai(A)), math.sqrt(_phuong_sai(B))
        if abs(sa - sb) < 0.5:
            continue
        return A, B
    return None, None


def L10_C5_B14_VD083_MC_A_01(socau, dang=1):
    r"""So sánh độ ổn định của hai mẫu số liệu thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    thu = 0
    while len(gt) < socau and thu < 30:
        thu += 1
        A, B = _cap_mau_khac_do_on_dinh(random.choice([5, 6]), 5, 14)
        if A is None:
            continue
        v = (tuple(A), tuple(B))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for A, B in gt:
        A, B = list(A), list(B)
        tb = _so_trung_binh(A)
        sa, sb = math.sqrt(_phuong_sai(A)), math.sqrt(_phuong_sai(B))
        on_dinh = "An" if sa < sb else "Bình"
        dung = (r"Bạn %s bắn ổn định hơn, vì hai bạn có cùng điểm trung "
                r"bình nhưng bạn %s có độ lệch chuẩn nhỏ hơn"
                % (on_dinh, on_dinh))
        kia = "Bình" if on_dinh == "An" else "An"
        nhieu = [r"Bạn %s bắn ổn định hơn, vì bạn ấy có độ lệch chuẩn lớn "
                 r"hơn" % kia,
                 r"Hai bạn ổn định như nhau, vì có cùng điểm trung bình",
                 r"Không so sánh được, vì hai mẫu có cùng số số liệu",
                 r"Bạn %s bắn ổn định hơn, vì bạn ấy có điểm cao nhất lớn "
                 r"hơn" % kia]
        debai = (r"Điểm bắn trong $%d$ lần của hai xạ thủ An và Bình được "
                 r"ghi lại:" % len(A) +
                 "\\\\\n" + r"An: \quad " + _bang(A) +
                 "\\\\\n" + r"Bình: \quad " + _bang(B) +
                 "\n" +
                 r"Ai bắn \textbf{ổn định} hơn và vì sao?")
        giai = (r"Số trung bình: An $= %s$, Bình $= %s$ - \textbf{bằng "
                r"nhau}, nên chưa phân biệt được."
                % (_xx5(tb), _xx5(_so_trung_binh(B))) +
                "\\\\\n"
                r"Độ lệch chuẩn: An $s_A = %s$, Bình $s_B = %s$."
                % (_xx5(sa), _xx5(sb)) +
                "\\\\\n"
                r"Độ lệch chuẩn đo mức chênh lệch của các số liệu quanh số "
                r"trung bình, nên độ lệch chuẩn càng \textbf{nhỏ} thì càng "
                r"ổn định."
                "\\\\\n"
                r"Vậy bạn %s bắn ổn định hơn." % on_dinh)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_VD084_MC_A_01(socau, dang=1):
    r"""Rút ra kết luận từ số đặc trưng đo độ phân tán.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    thu = 0
    while len(gt) < socau and thu < 40:
        thu += 1
        Z, _kq = _mau_co_dung_mot_ngoai_le()
        if Z is None or tuple(Z) in gt:
            continue
        gt.append(tuple(Z))

    cauTN = ""
    for Z in gt:
        Z = list(Z)
        q1, q2, q3 = _tu_phan_vi(Z)
        delta = q3 - q1
        tren = q3 + 1.5 * delta
        duoi = q1 - 1.5 * delta
        ngoai = [x for x in Z if x < duoi or x > tren]
        dung = r"$%s$" % _xx5(ngoai[0]) if len(ngoai) == 1 else \
            r"$%s$" % ", ".join(_xx5(x) for x in ngoai)
        nhieu = [r"$%s$" % x for x in _ba_nhieu5(
            dung.strip("$"), [_xx5(max(x for x in Z if x not in ngoai)),
                              _xx5(min(Z)), _xx5(q3), _xx5(q1)],
            buoc=lambda t: _xx5(max(Z) + t))]
        debai = (r"Cho mẫu số liệu đã sắp xếp theo thứ tự không giảm:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Giá trị nào của mẫu là \textbf{giá trị ngoại lệ}?")
        giai = (r"$Q_1 = %s$, $Q_3 = %s$ nên "
                r"$\Delta_Q = %s - %s = %s$."
                % (_xx5(q1), _xx5(q3), _xx5(q3), _xx5(q1), _xx5(delta)) +
                "\\\\\n"
                r"Ngưỡng dưới: $Q_1 - 1{,}5\Delta_Q = %s$; ngưỡng trên: "
                r"$Q_3 + 1{,}5\Delta_Q = %s$." % (_xx5(duoi), _xx5(tren)) +
                "\\\\\n"
                r"Số liệu nằm ngoài hai ngưỡng ấy là giá trị ngoại lệ: "
                r"$%s$." % ", ".join(_xx5(x) for x in ngoai) +
                "\\\\\n"
                r"Các số liệu còn lại đều nằm trong đoạn "
                r"$\left[%s;\ %s\right]$." % (_xx5(duoi), _xx5(tren)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_VD084_TL_A_01(socau, dong=1):
    r"""Tự luận: đánh giá mức độ ổn định và kết luận.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    thu = 0
    while len(gt) < socau and thu < 30:
        thu += 1
        A, B = _cap_mau_khac_do_on_dinh(random.choice([5, 6]), 5, 14)
        if A is None:
            continue
        v = (tuple(A), tuple(B))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for A, B in gt:
        A, B = list(A), list(B)
        n = len(A)
        tb = _so_trung_binh(A)
        psA, psB = _phuong_sai(A), _phuong_sai(B)
        sa, sb = math.sqrt(psA), math.sqrt(psB)
        on_dinh = "dây chuyền I" if sa < sb else "dây chuyền II"

        debai = (r"Khối lượng (đơn vị: gam) của $%d$ sản phẩm lấy ngẫu "
                 r"nhiên từ mỗi dây chuyền được ghi lại:" % n +
                 "\\\\\n" + r"Dây chuyền I: \quad " + _bang(A) +
                 "\\\\\n" + r"Dây chuyền II: \quad " + _bang(B))

        hoi_a = r"Tính số trung bình khối lượng sản phẩm của mỗi dây chuyền."
        giai_a = (r"Dây chuyền I: $\overline{x}_1 = \dfrac{%s}{%d} = %s$ (g)."
                  % (_xx5(sum(A)), n, _xx5(tb)) +
                  "\\\\\n"
                  r"Dây chuyền II: $\overline{x}_2 = \dfrac{%s}{%d} = %s$ (g)."
                  % (_xx5(sum(B)), n, _xx5(_so_trung_binh(B))) +
                  "\\\\\n"
                  r"Hai dây chuyền có khối lượng trung bình \textbf{bằng "
                  r"nhau}.")

        hoi_b = r"Tính phương sai và độ lệch chuẩn của mỗi dây chuyền."
        giai_b = (r"Dây chuyền I: $s_1^2 = \dfrac{1}{%d}\left[%s\right] "
                  r"= %s$, nên $s_1 = \sqrt{%s} = %s$ (g)."
                  % (n, _bang_tinh_phuong_sai(A), _xx5(psA), _xx5(psA),
                     _xx5(sa)) +
                  "\\\\\n"
                  r"Dây chuyền II: $s_2^2 = \dfrac{1}{%d}\left[%s\right] "
                  r"= %s$, nên $s_2 = \sqrt{%s} = %s$ (g)."
                  % (n, _bang_tinh_phuong_sai(B), _xx5(psB), _xx5(psB),
                     _xx5(sb)))

        hoi_c = (r"Dây chuyền nào sản xuất \textbf{ổn định} hơn? Giải thích.")
        giai_c = (r"Hai dây chuyền có cùng khối lượng trung bình nên phải "
                  r"nhìn vào độ phân tán."
                  "\\\\\n"
                  r"$s_1 = %s$ và $s_2 = %s$, mà độ lệch chuẩn càng nhỏ thì "
                  r"khối lượng các sản phẩm càng ít chênh lệch quanh giá "
                  r"trị trung bình." % (_xx5(sa), _xx5(sb)) +
                  "\\\\\n"
                  r"Vậy %s sản xuất ổn định hơn." % on_dinh)

        ds_abcd = [(hoi_a, r"\overline{x}_1 = \overline{x}_2 = %s" % _xx5(tb),
                    giai_a),
                   (hoi_b, r"s_1 = %s,\ s_2 = %s" % (_xx5(sa), _xx5(sb)),
                    giai_b),
                   (hoi_c, r"\text{%s}" % on_dinh, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI - bốn ý phải TĂNG DẦN mức độ NB, TH, VD, VDC
# =====================================================================

def L10_C5_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - số gần đúng và sai số; số đặc trưng đo xu thế trung tâm.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = 9
        nen = sorted(random.randint(5, 12) for _ in range(n - 1))
        la = random.choice([50, 60, 70])
        Z = sorted(nen + [la])
        if not _dep(_so_trung_binh(Z), 2) or tuple(Z) in gt:
            continue
        gt.append(tuple(Z))

    cauTF = ''
    for Z in gt:
        Z = list(Z)
        n = len(Z)
        tb = _so_trung_binh(Z)
        tv = _trung_vi(Z)
        tb_bo = _so_trung_binh(Z[:-1])

        debai = (r"Cho mẫu số liệu (đã sắp xếp theo thứ tự không giảm) về "
                 r"số giờ tự học trong tuần của $%d$ học sinh:" % n +
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}")

        ds_abcd = (
            # a) NB - nhắc lại một định nghĩa
            [
                (r"{\True Mẫu số liệu trên có $%d$ số liệu nên trung vị là "
                 r"số liệu đứng chính giữa}" % n,
                 r"Đúng. $%d$ là số lẻ nên trung vị là số liệu thứ $%d$, "
                 r"tức là $%s$." % (n, n // 2 + 1, _xx5(tv))),
                (r"{Mẫu số liệu trên có $%d$ số liệu nên trung vị là trung "
                 r"bình cộng của hai số liệu đứng giữa}" % n,
                 r"Sai. Cách lấy trung bình cộng hai số giữa chỉ dùng khi "
                 r"số số liệu là số CHẴN; ở đây $%d$ là số lẻ." % n),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True Số trung bình của mẫu bằng $%s$}" % _xx5(tb),
                 r"Đúng. $\overline{x} = \dfrac{%s}{%d} = %s$."
                 % (_xx5(sum(Z)), n, _xx5(tb))),
                (r"{Số trung bình của mẫu bằng $%s$}" % _xx5(tv),
                 r"Sai. $%s$ là TRUNG VỊ; số trung bình là "
                 r"$\dfrac{%s}{%d} = %s$."
                 % (_xx5(tv), _xx5(sum(Z)), n, _xx5(tb))),
            ],
            # c) VD - phải so được hai số đặc trưng vừa tính
            [
                (r"{\True Số trung bình của mẫu lớn hơn trung vị của mẫu}",
                 r"Đúng. $\overline{x} = %s$ còn $M_e = %s$."
                 % (_xx5(tb), _xx5(tv)) +
                 "\\\\\n"
                 r"Mẫu có một giá trị rất lớn là $%s$ kéo số trung bình lên "
                 r"cao, trong khi trung vị không bị ảnh hưởng."
                 % _xx5(max(Z))),
                (r"{Số trung bình của mẫu bằng đúng trung vị của mẫu}",
                 r"Sai. $\overline{x} = %s \ne %s = M_e$."
                 % (_xx5(tb), _xx5(tv))),
            ],
            # d) VDC - phải tự nghĩ ra cách, không có công thức sẵn
            [
                (r"{\True Nếu bỏ số liệu lớn nhất ra khỏi mẫu thì số trung "
                 r"bình giảm đi hơn $1$ đơn vị}",
                 r"Đúng. Bỏ $%s$ đi thì còn $%d$ số liệu với tổng $%s$, nên "
                 r"$\overline{x} = %s$."
                 % (_xx5(max(Z)), n - 1, _xx5(sum(Z[:-1])), _xx5(tb_bo)) +
                 "\\\\\n"
                 r"Số trung bình giảm $%s - %s = %s > 1$."
                 % (_xx5(tb), _xx5(tb_bo), _xx5(tb - tb_bo))),
                (r"{Nếu bỏ số liệu lớn nhất ra khỏi mẫu thì số trung bình "
                 r"không thay đổi}",
                 r"Sai. Bỏ $%s$ đi thì số trung bình còn $%s$, giảm $%s$ so "
                 r"với $%s$ ban đầu."
                 % (_xx5(max(Z)), _xx5(tb_bo), _xx5(tb - tb_bo), _xx5(tb))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L10_C5_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - các số đặc trưng đo độ phân tán.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        X = _mau_phuong_sai_dep(random.choice([6, 8]), 3, 16,
                                can_do_lech=True)
        if X is None:
            continue
        if not all(_dep(q, 2) for q in _tu_phan_vi(X)):
            continue
        if tuple(X) in gt:
            continue
        gt.append(tuple(X))

    cauTF = ''
    for X in gt:
        Z = list(X)
        n = len(Z)
        R = max(Z) - min(Z)
        q1, q2, q3 = _tu_phan_vi(Z)
        delta = q3 - q1
        ps = _phuong_sai(Z)
        s = math.sqrt(ps)

        debai = (r"Cho mẫu số liệu (đã sắp xếp theo thứ tự không giảm):"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}")

        ds_abcd = (
            # a) NB - nhắc lại một công thức
            [
                (r"{\True Khoảng biến thiên của mẫu bằng $%s$}" % _xx5(R),
                 r"Đúng. $R = x_{\max} - x_{\min} = %s - %s = %s$."
                 % (_xx5(max(Z)), _xx5(min(Z)), _xx5(R))),
                (r"{Khoảng biến thiên của mẫu bằng $%s$}"
                 % _xx5(max(Z) + min(Z)),
                 r"Sai. Khoảng biến thiên là HIỆU chứ không phải tổng: "
                 r"$R = %s - %s = %s$."
                 % (_xx5(max(Z)), _xx5(min(Z)), _xx5(R))),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True Khoảng tứ phân vị của mẫu bằng $%s$}" % _xx5(delta),
                 r"Đúng. $Q_1 = %s$, $Q_3 = %s$ nên "
                 r"$\Delta_Q = %s - %s = %s$."
                 % (_xx5(q1), _xx5(q3), _xx5(q3), _xx5(q1), _xx5(delta))),
                (r"{Khoảng tứ phân vị của mẫu bằng $%s$}" % _xx5(q2),
                 r"Sai. $%s$ là $Q_2$ (trung vị); khoảng tứ phân vị là "
                 r"$Q_3 - Q_1 = %s$." % (_xx5(q2), _xx5(delta))),
            ],
            # c) VD - phải tính qua hai bước mới ra
            [
                (r"{\True Phương sai của mẫu bằng $%s$}" % _xx5(ps),
                 r"Đúng. $\overline{x} = %s$, rồi"
                 % _xx5(_so_trung_binh(Z)) +
                 "\\\\\n"
                 r"$s^2 = \dfrac{1}{%d}\left[%s\right] = %s$."
                 % (n, _bang_tinh_phuong_sai(Z), _xx5(ps))),
                (r"{Phương sai của mẫu bằng $%s$}" % _xx5(ps * n),
                 r"Sai. $%s$ mới là TỔNG các bình phương độ lệch; phương sai "
                 r"còn phải chia cho $n = %d$, được $%s$."
                 % (_xx5(ps * n), n, _xx5(ps))),
            ],
            # d) VDC - phải hiểu quan hệ giữa hai đại lượng, không thay số
            [
                (r"{\True Nếu cộng thêm $5$ vào mọi số liệu của mẫu thì độ "
                 r"lệch chuẩn không thay đổi}",
                 r"Đúng. Cộng thêm cùng một số vào mọi số liệu thì số trung "
                 r"bình cũng tăng đúng số ấy, nên mỗi độ lệch "
                 r"$x_i - \overline{x}$ giữ nguyên."
                 "\\\\\n"
                 r"Phương sai và độ lệch chuẩn tính từ các độ lệch ấy nên "
                 r"cũng giữ nguyên: $s = %s$." % _xx5(s) +
                 "\\\\\n"
                 r"Độ phân tán đo mức CHÊNH LỆCH giữa các số liệu, không "
                 r"phụ thuộc việc dời cả mẫu đi một khoảng."),
                (r"{Nếu cộng thêm $5$ vào mọi số liệu của mẫu thì độ lệch "
                 r"chuẩn tăng thêm $5$}",
                 r"Sai. Số trung bình tăng $5$ nhưng mỗi độ lệch "
                 r"$x_i - \overline{x}$ không đổi, nên độ lệch chuẩn vẫn "
                 r"bằng $%s$." % _xx5(s)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


# ---------------------------------------------------------------------
# Bảy dạng bổ sung: bộ chọn câu cần TRẢ LỜI NGẮN cho VD070, VD077, VD078,
# VD083, VD084 và TỰ LUẬN cho VD078, VD083, mà Mapping chưa khai - đề hệ
# số 1 chương 5 vì thế mất 26/96 câu.
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
# ---------------------------------------------------------------------

def L10_C5_B12_VD070_SA_A_01(socau):
    r"""Trả lời ngắn: có bao nhiêu dòng của bảng có số liệu không chính xác
    (dựa vào quan hệ tổng).

    SUA 29/09/2026 (co Lan: muc van dung thi hoi "co bao nhieu"): ban cu hoi
    "so lieu nao khong hop li" voi chieu cao 15 cm / 1700 cm - nhin la thay.
    """
    cau = ""
    for _ in range(socau):
        bc, dong, sai = _bang_tong_co_dong_sai(6, random.choice([1, 2, 3, 4]))
        debai = (bc[0] + "\n" + _tex_bang_tong(bc, dong) + "\n" +
                 r"Có bao nhiêu %s có số liệu không chính xác?" % bc[4])
        dap = str(len(sai))
        nhieu = [str(x) for x in range(0, 6) if x != len(sai)][:3]
        cau += MC_SA_answer_text(debai, dap, nhieu, _giai_bang_tong(bc, dong, sai), 0, 0, 2)
    return cau


def L10_C5_B13_VD077_SA_A_01(socau):
    """Trả lời ngắn: dùng trung vị làm đại diện khi mẫu có giá trị bất thường."""
    gt = []
    while len(gt) < socau:
        nen = sorted(random.randint(6, 12) for _ in range(8))
        la = random.choice([60, 80, 100])
        Z = sorted(nen + [la])
        if tuple(Z) in gt or not _dep(_trung_vi(Z), 2):
            continue
        gt.append(tuple(Z))

    cau = ""
    for Z in gt:
        Z = list(Z)
        tv = _trung_vi(Z)
        tb = _so_trung_binh(Z)
        debai = (r"Số tiền (triệu đồng) mà $9$ hộ gia đình đóng góp cho quỹ "
                 r"từ thiện được ghi lại:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" +
                 r"Mẫu có một giá trị bất thường nên số trung bình không "
                 r"còn đại diện tốt. Hãy tính số đặc trưng \textbf{thay "
                 r"thế} phù hợp nhất cho mẫu này.")
        giai = (r"Mẫu có giá trị $%s$ lớn vượt trội, kéo số trung bình lên "
                r"$%s$ - cao hơn mức đóng góp của hầu hết các hộ."
                % (_xx5(max(Z)), _xx5(tb)) +
                "\\\\\n"
                r"Số đặc trưng không bị giá trị bất thường làm lệch là "
                r"\textbf{trung vị}."
                "\\\\\n"
                r"Mẫu có $9$ số liệu (lẻ) nên trung vị là số thứ $5$: "
                r"$M_e = %s$." % _xx5(tv))
        nhieu = _ba_nhieu5(_xx5(tv), [_xx5(tb), _xx5(max(Z)), _xx5(min(Z))],
                           buoc=lambda t: _xx5(tv + t))
        cau += MC_SA_answer_text(debai, _xx5(tv), nhieu, giai, 0, 0, 2)
    return cau


def _bo_so_hop(lan_thu=200):
    """Bộ (nho, q1, q2, q3, lon, ngoai_le) cho biểu đồ hộp, số đẹp."""
    for _ in range(lan_thu):
        q1 = random.randint(20, 35)
        delta = random.choice([4, 6, 8, 10])
        q3 = q1 + delta
        q2 = random.randint(q1 + 1, q3 - 1)
        nho = q1 - random.randint(1, int(1.5 * delta) - 1)
        lon = q3 + random.randint(1, int(1.5 * delta) - 1)
        ngoai = q3 + int(1.5 * delta) + random.randint(1, 5)
        return nho, q1, q2, q3, lon, ngoai
    return None


def L10_C5_B13_VD078_SA_A_01(socau):
    """Trả lời ngắn: giá trị ngoại lệ đọc từ biểu đồ hộp - CÓ HÌNH VẼ."""
    gt = []
    while len(gt) < socau:
        v = _bo_so_hop()
        if v not in gt:
            gt.append(v)

    cau = ""
    for nho, q1, q2, q3, lon, ngoai in gt:
        delta = q3 - q1
        hinh = _hinh_bieu_do_hop(nho, q1, q2, q3, lon, (ngoai,))
        debai = (r"Biểu đồ hộp bên mô tả một mẫu số liệu. Tìm giá trị ngoại "
                 r"lệ của mẫu.")
        giai = (r"Đọc trên biểu đồ: $Q_1 = %s$, $Q_3 = %s$ nên "
                r"$\Delta_Q = %s$." % (_xx5(q1), _xx5(q3), _xx5(delta)) +
                "\\\\\n"
                r"Ngưỡng trên $Q_3 + 1{,}5\Delta_Q = %s$; ngưỡng dưới "
                r"$Q_1 - 1{,}5\Delta_Q = %s$."
                % (_xx5(q3 + 1.5 * delta), _xx5(q1 - 1.5 * delta)) +
                "\\\\\n"
                r"Chỉ có $%s$ vượt ngưỡng trên nên đó là giá trị ngoại lệ."
                % _xx5(ngoai))
        nhieu = _ba_nhieu5(_xx5(ngoai), [_xx5(lon), _xx5(nho), _xx5(q3)],
                           buoc=lambda t: _xx5(ngoai + t))
        cau += MC_SA_answer_text(debai, _xx5(ngoai), nhieu, giai, hinh, 0, 2)
    return cau


def L10_C5_B13_VD078_TL_A_01(socau, dong=1):
    """Tự luận: đọc biểu đồ hộp và tìm giá trị ngoại lệ - CÓ HÌNH VẼ."""
    gt = []
    while len(gt) < socau:
        v = _bo_so_hop()
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for nho, q1, q2, q3, lon, ngoai in gt:
        delta = q3 - q1
        hinh = _hinh_bieu_do_hop(nho, q1, q2, q3, lon, (ngoai,))
        debai = (r"Biểu đồ hộp bên mô tả thời gian (phút) đi từ nhà đến "
                 r"trường của một nhóm học sinh.")

        hoi_a = r"Đọc ba tứ phân vị $Q_1$, $Q_2$, $Q_3$ từ biểu đồ."
        giai_a = (r"Hai cạnh của hộp cho $Q_1 = %s$ và $Q_3 = %s$; vạch "
                  r"đứng trong hộp cho $Q_2 = %s$."
                  % (_xx5(q1), _xx5(q3), _xx5(q2)))

        hoi_b = r"Tính khoảng tứ phân vị $\Delta_Q$."
        giai_b = (r"$\Delta_Q = Q_3 - Q_1 = %s - %s = %s$ (phút)."
                  % (_xx5(q3), _xx5(q1), _xx5(delta)))

        hoi_c = r"Tìm giá trị ngoại lệ của mẫu và giải thích."
        giai_c = (r"Giá trị $x$ là ngoại lệ khi "
                  r"$x < Q_1 - 1{,}5\Delta_Q$ hoặc $x > Q_3 + 1{,}5\Delta_Q$."
                  "\\\\\n"
                  r"$Q_1 - 1{,}5\Delta_Q = %s$; $Q_3 + 1{,}5\Delta_Q = %s$."
                  % (_xx5(q1 - 1.5 * delta), _xx5(q3 + 1.5 * delta)) +
                  "\\\\\n"
                  r"Điểm $%s$ nằm ngoài ngưỡng trên nên là giá trị ngoại "
                  r"lệ - có một học sinh đi mất nhiều thời gian hơn hẳn các "
                  r"bạn." % _xx5(ngoai))

        ds_abcd = [(hoi_a, r"Q_1 = %s,\ Q_2 = %s,\ Q_3 = %s"
                    % (_xx5(q1), _xx5(q2), _xx5(q3)), giai_a),
                   (hoi_b, r"\Delta_Q = %s" % _xx5(delta), giai_b),
                   (hoi_c, r"%s" % _xx5(ngoai), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, hinh, 0, dong)
    return cauTN


def _mau_co_dung_mot_ngoai_le(lan_thu=400):
    """Mẫu có ĐÚNG MỘT giá trị ngoại lệ, đã kiểm tra SAU KHI thêm.

    Phải kiểm tra lại sau khi thêm giá trị lạ: thêm một số liệu làm ba tứ
    phân vị dịch đi, nên số vừa thêm có thể KHÔNG còn vượt ngưỡng nữa.
    Bản đầu chỉ tính ngưỡng trên mẫu gốc rồi lấy ngoai_le[0] - hỏng
    4/10 lần với IndexError vì danh sách ngoại lệ rỗng.
    """
    for _ in range(lan_thu):
        n = random.choice([9, 10, 11])
        X = _mau_so_lieu(n, 20, 40,
                         lambda Y: all(_dep(q, 2) for q in _tu_phan_vi(Y)))
        if X is None:
            continue
        q1, q2, q3 = _tu_phan_vi(X)
        delta = q3 - q1
        if delta <= 0:
            continue
        la = int(q3 + 1.5 * delta) + random.randint(2, 8)
        Z = sorted(list(X) + [la])
        q1, q2, q3 = _tu_phan_vi(Z)
        delta = q3 - q1
        if delta <= 0:
            continue
        tren, duoi = q3 + 1.5 * delta, q1 - 1.5 * delta
        ngoai = [x for x in Z if x < duoi or x > tren]
        if len(ngoai) == 1 and all(_dep(q, 2) for q in (q1, q2, q3)):
            return Z, ngoai[0]
    return None, None


def _mau_ngoai_le_sat_nguong(lan_thu=2000):
    """Mẫu có ĐÚNG MỘT giá trị bất thường nằm SÁT ngưỡng (vượt 1-2 đơn vị)
    và một giá trị KHÔNG bất thường cũng sát ngưỡng ấy (bẫy): nhìn qua
    thấy hai số "lạ" như nhau, buộc phải tính ngưỡng mới phân biệt được.

    Cách dựng: mẫu n = 10 hoặc 11 số (mỗi nửa có 5 số) nên đổi giá trị của
    HAI số lớn nhất (hay nhỏ nhất) mà vẫn giữ thứ tự thì Q1, Q2, Q3 KHÔNG
    đổi - ngưỡng tính trên mẫu gốc vẫn đúng. Vẫn kiểm tra lại cho chắc.

    CLAUDE THEM 29/09/2026 cho L10_C5_B14_TH080_MC_B_01.
    """
    for _ in range(lan_thu):
        n = random.choice([10, 11])
        Z = _mau_so_lieu(n, 20, 40, lambda Y: all(_dep(q, 2) for q in _tu_phan_vi(Y)))
        if Z is None:
            continue
        Z = list(Z)
        q1, q2, q3 = _tu_phan_vi(Z)
        d = q3 - q1
        if not 3 <= d <= 10:
            continue
        if random.random() < 0.5:
            tren = q3 + 1.5 * d
            la = math.floor(tren) + random.choice([1, 2])
            bay = math.floor(tren) - random.choice([0, 1])
            if bay <= Z[-3]:
                continue
            Z[-1], Z[-2] = la, bay
        else:
            duoi = q1 - 1.5 * d
            la = math.ceil(duoi) - random.choice([1, 2])
            bay = math.ceil(duoi) + random.choice([0, 1])
            if la <= 0 or bay >= Z[2]:
                continue
            Z[0], Z[1] = la, bay
        Z.sort()
        q1, q2, q3 = _tu_phan_vi(Z)
        d = q3 - q1
        tren, duoi = q3 + 1.5 * d, q1 - 1.5 * d
        ngoai = [x for x in Z if x < duoi or x > tren]
        if ngoai != [la] or Z.count(la) != 1 or Z.count(bay) != 1:
            continue
        return Z, la, bay
    return None, None, None


def L10_C5_B14_TH080_MC_B_01(socau, dang=1):
    r"""Tìm giá trị bất thường của mẫu số liệu nhờ khoảng tứ phân vị - giá
    trị bất thường nằm SÁT ngưỡng $Q_3 + 1{,}5\Delta_Q$ (hoặc
    $Q_1 - 1{,}5\Delta_Q$), không nhìn qua mà thấy được, buộc phải tính.

    CLAUDE THEM 29/09/2026 (co Lan: muc TH "lay nhung gia tri bat thuong
    hoi sat voi 2 dau mut +- 1,5 Delta_Q de hoc sinh kho nhan ra, buoc phai
    tinh"). Phuong an nhieu co mot gia tri cung sat nguong nhung KHONG bat
    thuong. Co Lan duyet.
    """
    gt = []
    lan = 0
    while len(gt) < socau and lan < 50:
        lan += 1
        Z, la, bay = _mau_ngoai_le_sat_nguong()
        if Z is None or tuple(Z) in [g[0] for g in gt]:
            continue
        gt.append((tuple(Z), la, bay))

    cauTN = ""
    for Z, la, bay in gt:
        Z = list(Z)
        q1, q2, q3 = _tu_phan_vi(Z)
        d = q3 - q1
        tren, duoi = q3 + 1.5 * d, q1 - 1.5 * d
        dung = r"$%s$" % _xx5(la)
        khac = [x for x in (bay, max(Z), min(Z), Z[len(Z) // 2]) if x != la]
        nhieu = [r"$%s$" % t for t in _ba_nhieu5(_xx5(la), [_xx5(x) for x in khac],
                                                 buoc=lambda t: _xx5(Z[t % len(Z)]))]
        tron = list(Z)
        random.shuffle(tron)
        debai = (r"Cho mẫu số liệu:" + "\\\\\n" + r"\begin{center}" + _bang(tron) +
                 r"\end{center}" + "\n" +
                 r"Giá trị nào sau đây là \textbf{giá trị bất thường} của mẫu số liệu?")
        giai = (r"Sắp xếp theo thứ tự không giảm: " + ", ".join("$%s$" % _xx5(x) for x in Z) + "." +
                "\\\\\n" +
                r"$Q_1 = %s$, $Q_2 = %s$, $Q_3 = %s$ nên $\Delta_Q = %s - %s = %s$."
                % (_xx5(q1), _xx5(q2), _xx5(q3), _xx5(q3), _xx5(q1), _xx5(d)) +
                "\\\\\n" +
                r"$Q_1 - 1{,}5\Delta_Q = %s$ và $Q_3 + 1{,}5\Delta_Q = %s$."
                % (_xx5(duoi), _xx5(tren)) +
                "\\\\\n" +
                r"Giá trị bất thường là giá trị nhỏ hơn $%s$ hoặc lớn hơn $%s$: chỉ có $%s$."
                % (_xx5(duoi), _xx5(tren), _xx5(la)) +
                "\\\\\n" +
                r"Chú ý $%s$ tuy gần ngưỡng nhưng vẫn nằm trong đoạn "
                r"$\left[%s;\ %s\right]$ nên không phải giá trị bất thường."
                % (_xx5(bay), _xx5(duoi), _xx5(tren)))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C5_B14_VD083_SA_A_01(socau):
    """Trả lời ngắn: độ lệch chuẩn của mẫu ổn định hơn."""
    gt = []
    thu = 0
    while len(gt) < socau and thu < 30:
        thu += 1
        A, B = _cap_mau_khac_do_on_dinh(random.choice([5, 6]), 5, 14)
        if A is None:
            continue
        v = (tuple(A), tuple(B))
        if v not in gt:
            gt.append(v)

    cau = ""
    for A, B in gt:
        A, B = list(A), list(B)
        sa, sb = math.sqrt(_phuong_sai(A)), math.sqrt(_phuong_sai(B))
        nho = min(sa, sb)
        ten = "An" if sa < sb else "Bình"
        debai = (r"Điểm bắn trong $%d$ lần của hai xạ thủ được ghi lại:"
                 % len(A) +
                 "\\\\\n" + r"An: \quad " + _bang(A) +
                 "\\\\\n" + r"Bình: \quad " + _bang(B) +
                 "\n" +
                 r"Hai bạn có cùng điểm trung bình. Tính độ lệch chuẩn của "
                 r"bạn bắn \textbf{ổn định hơn}.")
        giai = (r"Số trung bình của hai bạn bằng nhau nên phải so độ phân "
                r"tán."
                "\\\\\n"
                r"$s_{\text{An}} = %s$; $s_{\text{Bình}} = %s$."
                % (_xx5(sa), _xx5(sb)) +
                "\\\\\n"
                r"Độ lệch chuẩn càng nhỏ thì càng ổn định, nên bạn %s ổn "
                r"định hơn với độ lệch chuẩn $%s$." % (ten, _xx5(nho)))
        nhieu = _ba_nhieu5(_xx5(nho), [_xx5(max(sa, sb)), _xx5(nho * nho),
                                       _xx5(_so_trung_binh(A))],
                           buoc=lambda t: _xx5(nho + t / 2.0))
        cau += MC_SA_answer_text(debai, _xx5(nho), nhieu, giai, 0, 0, 2)
    return cau


def L10_C5_B14_VD083_TL_A_01(socau, dong=1):
    """Tự luận: so sánh độ ổn định của hai mẫu số liệu thực tiễn."""
    gt = []
    thu = 0
    while len(gt) < socau and thu < 30:
        thu += 1
        A, B = _cap_mau_khac_do_on_dinh(random.choice([5, 6]), 5, 14)
        if A is None:
            continue
        v = (tuple(A), tuple(B))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for A, B in gt:
        A, B = list(A), list(B)
        n = len(A)
        tb = _so_trung_binh(A)
        sa, sb = math.sqrt(_phuong_sai(A)), math.sqrt(_phuong_sai(B))
        ten = "An" if sa < sb else "Bình"

        debai = (r"Điểm bắn trong $%d$ lần của hai xạ thủ An và Bình được "
                 r"ghi lại:" % n +
                 "\\\\\n" + r"An: \quad " + _bang(A) +
                 "\\\\\n" + r"Bình: \quad " + _bang(B))

        hoi_a = r"Tính số trung bình điểm bắn của mỗi bạn và nhận xét."
        giai_a = (r"An: $\overline{x}_A = \dfrac{%s}{%d} = %s$; "
                  r"Bình: $\overline{x}_B = \dfrac{%s}{%d} = %s$."
                  % (_xx5(sum(A)), n, _xx5(tb), _xx5(sum(B)), n,
                     _xx5(_so_trung_binh(B))) +
                  "\\\\\n"
                  r"Hai bạn có điểm trung bình \textbf{bằng nhau} nên chưa "
                  r"kết luận được ai bắn tốt hơn.")

        hoi_b = r"Tính độ lệch chuẩn điểm bắn của mỗi bạn."
        giai_b = (r"An: $s_A^2 = \dfrac{1}{%d}\left[%s\right] = %s$ nên "
                  r"$s_A = %s$."
                  % (n, _bang_tinh_phuong_sai(A), _xx5(_phuong_sai(A)),
                     _xx5(sa)) +
                  "\\\\\n"
                  r"Bình: $s_B^2 = \dfrac{1}{%d}\left[%s\right] = %s$ nên "
                  r"$s_B = %s$."
                  % (n, _bang_tinh_phuong_sai(B), _xx5(_phuong_sai(B)),
                     _xx5(sb)))

        hoi_c = r"Bạn nào bắn ổn định hơn? Giải thích."
        giai_c = (r"Độ lệch chuẩn đo mức chênh lệch của các điểm số quanh "
                  r"điểm trung bình; độ lệch chuẩn càng \textbf{nhỏ} thì "
                  r"điểm càng ít dao động, tức là bắn càng ổn định."
                  "\\\\\n"
                  r"Vì $s_{\text{An}} = %s$ và $s_{\text{Bình}} = %s$ nên "
                  r"bạn %s bắn ổn định hơn."
                  % (_xx5(sa), _xx5(sb), ten))

        ds_abcd = [(hoi_a, r"\overline{x}_A = \overline{x}_B = %s" % _xx5(tb),
                    giai_a),
                   (hoi_b, r"s_A = %s,\ s_B = %s" % (_xx5(sa), _xx5(sb)),
                    giai_b),
                   (hoi_c, r"\text{Bạn %s}" % ten, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C5_B14_VD084_SA_A_01(socau):
    """Trả lời ngắn: giá trị ngoại lệ từ số đặc trưng đo độ phân tán."""
    gt = []
    thu = 0
    while len(gt) < socau and thu < 40:
        thu += 1
        Z, kq = _mau_co_dung_mot_ngoai_le()
        if Z is None or tuple(Z) in gt:
            continue
        gt.append(tuple(Z))

    cau = ""
    for Z in gt:
        Z = list(Z)
        q1, q2, q3 = _tu_phan_vi(Z)
        delta = q3 - q1
        tren = q3 + 1.5 * delta
        duoi = q1 - 1.5 * delta
        ngoai = [x for x in Z if x < duoi or x > tren]
        kq = ngoai[0]
        debai = (r"Cho mẫu số liệu đã sắp xếp theo thứ tự không giảm:"
                 "\\\\\n" + r"\begin{center}" + _bang(Z) + r"\end{center}" +
                 "\n" + r"Tìm giá trị ngoại lệ của mẫu số liệu.")
        giai = (r"$Q_1 = %s$, $Q_3 = %s$, $\Delta_Q = %s$."
                % (_xx5(q1), _xx5(q3), _xx5(delta)) +
                "\\\\\n"
                r"Ngưỡng dưới $%s$, ngưỡng trên $%s$."
                % (_xx5(duoi), _xx5(tren)) +
                "\\\\\n"
                r"Chỉ có $%s$ nằm ngoài hai ngưỡng nên đó là giá trị ngoại "
                r"lệ." % _xx5(kq))
        nhieu = _ba_nhieu5(_xx5(kq), [_xx5(max(x for x in Z if x != kq)),
                                      _xx5(min(Z)), _xx5(q3)],
                           buoc=lambda t: _xx5(kq + t))
        cau += MC_SA_answer_text(debai, _xx5(kq), nhieu, giai, 0, 0, 2)
    return cau


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
