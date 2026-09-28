# ==========================================================
# CHƯƠNG 8 (lớp 10): ĐẠI SỐ TỔ HỢP
#   Bài 23. Quy tắc đếm
#   Bài 24. Hoán vị, chỉnh hợp, tổ hợp
#   Bài 25. Nhị thức Newton
#
# Nguồn: tệp LopXChuong8.py của cô Lan, chuyển sang chuẩn ngân hàng
# (đổi tên hàm theo ID, bỏ lệnh gọi ở mức mô-đun, sửa lỗi LaTeX).
# Những dạng tệp của cô chưa có thì viết mới, đều ghi rõ CLAUDE THEM.
#
# RÀNG BUỘC: nhị thức Newton lớp 10 CHỈ tới n = 4 và n = 5 (SGK KNTT).
# ==========================================================
import math
import random

from num2words import num2words
from sympy import Symbol, expand, latex

from math_type import *
from DefChung import calculate_coefficient, calculate_permutations


def _hv(n):
    """Số hoán vị của n phần tử."""
    return math.factorial(n)


def _ba_nhieu8(dapso, ung_vien, buoc=None):
    """Ba phương án nhiễu đôi một khác nhau và khác đáp số."""
    ds = []
    for v in ung_vien:
        if v != dapso and v not in ds:
            ds.append(v)
        if len(ds) == 3:
            return ds
    k = 1
    while len(ds) < 3:
        v = buoc(k) if buoc else k
        if v != dapso and v not in ds:
            ds.append(v)
        k += 1
    return ds


def _cach(n):
    """Viết số cách kèm đơn vị, dùng chung cho phần đếm."""
    return "$%d$ cách" % n


# =====================================================================
# BÀI 23. QUY TẮC ĐẾM
# =====================================================================

# Tình huống dùng quy tắc CỘNG: hai phương án LOẠI TRỪ nhau ("hoặc"),
# làm xong một việc là xong. Tình huống dùng quy tắc NHÂN: phải làm
# LẦN LƯỢT đủ các công đoạn ("và") thì mới xong một kết quả.
TINH_HUONG_CONG = [
    "Chọn một bạn đi dự đại hội, từ tổ $1$ hoặc từ tổ $2$",
    "Chọn mua một quyển sách, hoặc sách Toán hoặc sách Văn",
    "Đi từ nhà đến trường bằng xe buýt hoặc bằng xe đạp",
    "Chọn một học sinh giỏi, hoặc là nam hoặc là nữ",
]
TINH_HUONG_NHAN = [
    "Chọn một bộ quần áo gồm một áo và một quần",
    "Lập một mật khẩu gồm một chữ cái rồi đến một chữ số",
    "Chọn một món chính và một món tráng miệng cho bữa ăn",
    "Đi từ $A$ đến $C$ bắt buộc phải qua $B$",
]


def L10_C8_B23_TH125_MC_A_01(socau, dang=1):
    """Giải thích quy tắc cộng qua ví dụ thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Đáp án đúng lấy từ nhóm tình huống "hoặc", ba phương án nhiễu lấy từ
    nhóm "và" nên chắc chắn chỉ có một phương án đúng.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(TINH_HUONG_CONG))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(TINH_HUONG_CONG):
            break

    cauTN = ""
    for i in gt:
        dung = "%s." % TINH_HUONG_CONG[i]
        nhieu = ["%s." % t for t in TINH_HUONG_NHAN]
        debai = (r"Trong các tình huống sau, tình huống nào đếm số cách "
                 r"thực hiện bằng \textbf{quy tắc cộng}?")
        giai = (r"Quy tắc cộng dùng khi công việc có nhiều phương án "
                r"\textbf{loại trừ nhau}: chọn xong một phương án là công "
                r"việc đã hoàn thành."
                "\\\\\n"
                r"Quy tắc nhân dùng khi công việc phải làm \textbf{lần lượt} "
                r"qua nhiều công đoạn, thiếu một công đoạn thì chưa xong."
                "\\\\\n"
                r"Tình huống ``%s'' cho hai phương án loại trừ nhau nên "
                r"dùng quy tắc cộng." % TINH_HUONG_CONG[i])
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B23_TH126_MC_A_01(socau, dang=1):
    """Giải thích quy tắc nhân qua ví dụ thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(TINH_HUONG_NHAN))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(TINH_HUONG_NHAN):
            break

    cauTN = ""
    for i in gt:
        dung = "%s." % TINH_HUONG_NHAN[i]
        nhieu = ["%s." % t for t in TINH_HUONG_CONG]
        debai = (r"Trong các tình huống sau, tình huống nào đếm số cách "
                 r"thực hiện bằng \textbf{quy tắc nhân}?")
        giai = (r"Quy tắc nhân dùng khi công việc phải làm \textbf{lần lượt} "
                r"qua nhiều công đoạn, làm thiếu một công đoạn thì công việc "
                r"chưa hoàn thành."
                "\\\\\n"
                r"Tình huống ``%s'' bắt buộc phải làm đủ các công đoạn nên "
                r"dùng quy tắc nhân." % TINH_HUONG_NHAN[i])
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B23_TH127_MC_A_01(socau, dang=1):
    """Đếm số cách chọn bằng quy tắc cộng.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(12, 25)
        b = random.randint(12, 25)
        if a == b or (a, b) in gt:
            continue
        gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        kq = a + b
        dung = _cach(kq)
        nhieu = [_cach(x) for x in _ba_nhieu8(
            kq, [a * b, abs(a - b), a * b - kq, kq + 2],
            buoc=lambda t: kq + 3 * t)]
        debai = (r"Một lớp có $%d$ học sinh nam và $%d$ học sinh nữ. Giáo "
                 r"viên cần chọn $1$ học sinh của lớp đi dự đại hội đoàn "
                 r"trường. Hỏi có bao nhiêu cách chọn?" % (a, b))
        giai = (r"Chọn $1$ học sinh thì hoặc chọn một bạn nam, hoặc chọn một "
                r"bạn nữ - hai phương án này loại trừ nhau nên dùng quy tắc "
                r"cộng."
                "\\\\\n"
                r"Chọn một bạn nam: $%d$ cách. Chọn một bạn nữ: $%d$ cách."
                "\\\\\n"
                r"Vậy số cách chọn là $%d + %d = %d$." % (a, b, a, b, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B23_TH127_SA_A_01(socau):
    r"""Số cách chọn theo quy tắc cộng - chọn hai viên bi cùng màu.

    Giữ nguyên bài của cô Lan (K10_8_23_2_Ngan_1_NB), chỉ sửa phần LaTeX:
    bản cũ viết $C_{blue}^{2}$ bằng f-string nên ra "C_9^2" không có ngoặc,
    số có hai chữ số sẽ hiển thị sai (C_10^2 thành $C_1$ rồi $0^2$).
    """
    gt = []
    while len(gt) < socau:
        person = random.choice(["Hùng", "Hà", "Tuấn", "Lan", "Minh"])
        blue = random.randint(5, 12)
        red = random.randint(5, 12)
        v = (person, blue, red)
        if v not in gt:
            gt.append(v)

    cau = ""
    for person, blue, red in gt:
        c_blue = calculate_coefficient(blue, 2)
        c_red = calculate_coefficient(red, 2)
        kq = c_blue + c_red

        debai = (r"Bạn %s có $%d$ viên bi xanh và $%d$ viên bi đỏ, các viên "
                 r"bi đôi một khác nhau. Có bao nhiêu cách để bạn %s chọn ra "
                 r"đúng hai viên bi \textbf{cùng màu}?"
                 % (person, blue, red, person))
        giai = (r"Hai viên bi cùng màu thì hoặc cùng xanh, hoặc cùng đỏ - hai "
                r"phương án loại trừ nhau nên dùng quy tắc cộng."
                "\\\\\n"
                r"Chọn hai viên bi xanh: $C_{%d}^{2} = %d$ cách."
                "\\\\\n"
                r"Chọn hai viên bi đỏ: $C_{%d}^{2} = %d$ cách."
                "\\\\\n"
                r"Vậy số cách chọn là $%d + %d = %d$."
                % (blue, c_blue, red, c_red, c_blue, c_red, kq))
        nhieu = _ba_nhieu8(kq, [c_blue * c_red, abs(c_blue - c_red),
                                calculate_coefficient(blue + red, 2), kq + 5],
                           buoc=lambda t: kq + 7 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C8_B23_TH128_MC_A_01(socau, dang=1):
    """Đếm số cách chọn bằng quy tắc nhân.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        a = random.randint(4, 9)
        b = random.randint(4, 9)
        if (a, b) in gt:
            continue
        gt.append((a, b))

    cauTN = ""
    for a, b in gt:
        kq = a * b
        dung = _cach(kq)
        nhieu = [_cach(x) for x in _ba_nhieu8(
            kq, [a + b, a ** b if a ** b < 10 ** 6 else kq + 1, kq - a, kq + b],
            buoc=lambda t: kq + 4 * t)]
        debai = (r"Một cửa hàng có $%d$ loại áo và $%d$ loại quần. Một khách "
                 r"muốn mua một bộ gồm \textbf{một áo và một quần}. Hỏi khách "
                 r"đó có bao nhiêu cách chọn?" % (a, b))
        giai = (r"Muốn có một bộ thì phải làm đủ hai công đoạn: chọn áo "
                r"\textbf{rồi} chọn quần, nên dùng quy tắc nhân."
                "\\\\\n"
                r"Công đoạn chọn áo: $%d$ cách. Ứng với mỗi áo, công đoạn "
                r"chọn quần: $%d$ cách."
                "\\\\\n"
                r"Vậy số cách chọn là $%d \cdot %d = %d$."
                % (a, b, a, b, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B23_TH128_SA_A_01(socau):
    """Số cách chọn theo quy tắc nhân - lập số từ tập chữ số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        k = random.choice([5, 6, 7, 8])
        d = random.choice([3, 4])
        if (k, d) not in gt:
            gt.append((k, d))

    cau = ""
    for k, d in gt:
        kq = k ** d
        debai = (r"Cho tập $A = \{1;\ 2;\ \ldots;\ %d\}$. Có bao nhiêu số tự "
                 r"nhiên gồm $%d$ chữ số, các chữ số đều thuộc $A$ và "
                 r"\textbf{được phép lặp lại}?" % (k, d))
        giai = (r"Số cần lập có $%d$ chữ số, mỗi chữ số là một công đoạn phải "
                r"làm lần lượt nên dùng quy tắc nhân." % d +
                "\\\\\n"
                r"Vì các chữ số được phép lặp lại nên mỗi công đoạn đều có "
                r"$%d$ cách chọn." % k +
                "\\\\\n"
                r"Vậy số các số lập được là $%d^{%d} = %d$." % (k, d, kq))
        nhieu = _ba_nhieu8(kq, [d ** k, k * d, calculate_permutations(k, d),
                                kq + k],
                           buoc=lambda t: kq + 10 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C8_B23_TH129_MC_A_01(socau, dang=1):
    """Dùng sơ đồ hình cây đếm số kết quả.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = (random.randint(2, 4), random.randint(2, 4), random.randint(2, 3))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c in gt:
        kq = a * b * c
        dung = _cach(kq)
        nhieu = [_cach(x) for x in _ba_nhieu8(
            kq, [a + b + c, a * b + c, a + b * c, kq + a],
            buoc=lambda t: kq + 3 * t)]
        debai = (r"Một nhà hàng có $%d$ món khai vị, $%d$ món chính và $%d$ "
                 r"món tráng miệng. Một thực khách vẽ sơ đồ hình cây để chọn "
                 r"một bữa ăn gồm đủ ba món, mỗi loại một món. Sơ đồ hình cây "
                 r"đó có bao nhiêu nhánh ở tầng cuối cùng?" % (a, b, c))
        giai = (r"Sơ đồ hình cây có ba tầng ứng với ba lần chọn."
                "\\\\\n"
                r"Tầng thứ nhất có $%d$ nhánh (món khai vị); mỗi nhánh ấy toả "
                r"ra $%d$ nhánh (món chính); mỗi nhánh mới lại toả ra $%d$ "
                r"nhánh (món tráng miệng)." % (a, b, c) +
                "\\\\\n"
                r"Vậy số nhánh ở tầng cuối là $%d \cdot %d \cdot %d = %d$."
                % (a, b, c, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B23_VD130_MC_A_01(socau, dang=1):
    """Bài toán đếm thực tiễn dùng CẢ quy tắc cộng và quy tắc nhân.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = (random.randint(2, 5), random.randint(2, 5), random.randint(3, 6))
        if v[0] != v[1] and v not in gt:
            gt.append(v)

    cauTN = ""
    for m, n, p in gt:
        kq = (m + n) * p
        dung = _cach(kq)
        nhieu = [_cach(x) for x in _ba_nhieu8(
            kq, [m + n + p, m * n * p, m * p + n, m + n * p],
            buoc=lambda t: kq + 5 * t)]
        debai = (r"Từ thành phố $A$ đến thành phố $C$ bắt buộc phải đi qua "
                 r"thành phố $B$. Từ $A$ đến $B$ có $%d$ tuyến đường bộ và "
                 r"$%d$ tuyến đường thuỷ; từ $B$ đến $C$ có $%d$ tuyến đường "
                 r"bộ. Hỏi có bao nhiêu cách đi từ $A$ đến $C$?" % (m, n, p))
        giai = (r"Chặng $A \to B$: đi đường bộ \textbf{hoặc} đường thuỷ, hai "
                r"phương án loại trừ nhau nên dùng quy tắc cộng:"
                "\\\\\n"
                r"$%d + %d = %d$ cách." % (m, n, m + n) +
                "\\\\\n"
                r"Muốn đi từ $A$ đến $C$ phải đi chặng $A \to B$ "
                r"\textbf{rồi} chặng $B \to C$, nên dùng quy tắc nhân:"
                "\\\\\n"
                r"$%d \cdot %d = %d$ cách." % (m + n, p, kq))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B23_VD130_TL_A_01(socau, dong=1):
    """Tự luận: bài toán đếm có nội dung thực tiễn.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = (random.randint(10, 18), random.randint(10, 18))
        if v[0] != v[1] and v not in gt:
            gt.append(v)

    cauTN = ""
    for nam, nu in gt:
        tong = nam + nu

        debai = (r"Một câu lạc bộ có $%d$ học sinh nam và $%d$ học sinh nữ, "
                 r"các học sinh đôi một khác nhau." % (nam, nu))

        hoi_a = r"Chọn $1$ học sinh của câu lạc bộ đi dự hội nghị. Hỏi có bao nhiêu cách chọn?"
        giai_a = (r"Chọn một bạn nam hoặc một bạn nữ, hai phương án loại trừ "
                  r"nhau nên dùng quy tắc cộng:"
                  "\\\\\n"
                  r"$%d + %d = %d$ (cách)." % (nam, nu, tong))

        kq_b = nam * nu
        hoi_b = r"Chọn $2$ học sinh gồm $1$ nam và $1$ nữ đi dự hội nghị. Hỏi có bao nhiêu cách chọn?"
        giai_b = (r"Phải chọn một bạn nam \textbf{rồi} chọn một bạn nữ nên "
                  r"dùng quy tắc nhân:"
                  "\\\\\n"
                  r"$%d \cdot %d = %d$ (cách)." % (nam, nu, kq_b))

        kq_c = calculate_coefficient(tong, 2) - kq_b
        hoi_c = r"Chọn $2$ học sinh \textbf{cùng giới tính}. Hỏi có bao nhiêu cách chọn?"
        giai_c = (r"Hai bạn cùng giới thì hoặc cùng nam, hoặc cùng nữ:"
                  "\\\\\n"
                  r"$C_{%d}^{2} + C_{%d}^{2} = %d + %d = %d$ (cách)."
                  % (nam, nu, calculate_coefficient(nam, 2),
                     calculate_coefficient(nu, 2), kq_c) +
                  "\\\\\n"
                  r"Có thể kiểm tra lại bằng cách lấy tổng số cách chọn $2$ "
                  r"bạn bất kì trừ đi số cách chọn $1$ nam $1$ nữ: "
                  r"$C_{%d}^{2} - %d = %d - %d = %d$."
                  % (tong, kq_b, calculate_coefficient(tong, 2), kq_b, kq_c))

        ds_abcd = [(hoi_a, "%d" % tong, giai_a),
                   (hoi_b, "%d" % kq_b, giai_b),
                   (hoi_c, "%d" % kq_c, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 24. HOÁN VỊ, CHỈNH HỢP, TỔ HỢP
# =====================================================================

# Ba nhóm tình huống, dùng chung cho ba dạng nhận biết NB131/132/133.
# Mỗi nhóm chỉ chứa tình huống của ĐÚNG một khái niệm, nên khi lấy đáp án
# từ một nhóm và phương án nhiễu từ hai nhóm kia thì không bao giờ có hai
# đáp án đúng.
TH_HOAN_VI = [
    "Xếp toàn bộ $5$ học sinh thành một hàng dọc",
    "Sắp xếp thứ tự thi đấu cho tất cả $6$ đội bóng",
    "Xếp tất cả $4$ quyển sách khác nhau lên một giá",
]
TH_CHINH_HOP = [
    "Chọn $3$ bạn trong $10$ bạn để làm lớp trưởng, lớp phó, thủ quỹ",
    "Chọn $2$ trong $8$ vận động viên để trao huy chương vàng và huy chương bạc",
    "Lập số có $3$ chữ số khác nhau từ các chữ số $1$ đến $9$",
]
TH_TO_HOP = [
    "Chọn $3$ bạn trong $10$ bạn để cùng đi trực nhật",
    "Chọn $5$ cầu thủ trong $12$ cầu thủ để ra sân",
    "Chọn $2$ quyển sách trong $7$ quyển để mang về đọc",
]


def _nhan_biet_PAC(socau, dang, nhom_dung, nhom_khac, ten, ly_do):
    """Khung chung cho ba dạng nhận biết hoán vị / chỉnh hợp / tổ hợp."""
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(nhom_dung))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(nhom_dung):
            break

    cauTN = ""
    for i in gt:
        dung = "%s." % nhom_dung[i]
        nhieu = ["%s." % t for nh in nhom_khac for t in nh]
        random.shuffle(nhieu)
        debai = (r"Trong các bài toán đếm sau, bài toán nào là bài toán "
                 r"\textbf{%s}?" % ten)
        giai = (ly_do + "\\\\\n" +
                r"Tình huống ``%s'' đúng là bài toán %s."
                % (nhom_dung[i], ten))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B24_NB131_MC_A_01(socau, dang=1):
    """Nhận ra bài toán hoán vị.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _nhan_biet_PAC(
        socau, dang, TH_HOAN_VI, [TH_CHINH_HOP, TH_TO_HOP], "hoán vị",
        r"Hoán vị: sắp xếp \textbf{TẤT CẢ} $n$ phần tử theo một thứ tự, "
        r"số cách là $P_n = n!$."
        "\\\\\n"
        r"Chỉnh hợp: chọn $k$ trong $n$ phần tử \textbf{có} phân biệt thứ tự."
        "\\\\\n"
        r"Tổ hợp: chọn $k$ trong $n$ phần tử \textbf{không} phân biệt thứ tự.")


def L10_C8_B24_NB132_MC_A_01(socau, dang=1):
    """Nhận ra bài toán chỉnh hợp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _nhan_biet_PAC(
        socau, dang, TH_CHINH_HOP, [TH_HOAN_VI, TH_TO_HOP], "chỉnh hợp",
        r"Chỉnh hợp chập $k$ của $n$: chọn $k$ trong $n$ phần tử rồi "
        r"\textbf{sắp thứ tự} cho $k$ phần tử ấy, số cách là $A_n^k$."
        "\\\\\n"
        r"Dấu hiệu nhận ra: các vị trí được chọn có \textbf{vai trò khác "
        r"nhau} (chức vụ khác nhau, giải thưởng khác nhau, hàng đơn vị - "
        r"hàng chục khác nhau).")


def L10_C8_B24_NB133_MC_A_01(socau, dang=1):
    """Nhận ra bài toán tổ hợp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _nhan_biet_PAC(
        socau, dang, TH_TO_HOP, [TH_HOAN_VI, TH_CHINH_HOP], "tổ hợp",
        r"Tổ hợp chập $k$ của $n$: chọn ra một \textbf{nhóm} $k$ phần tử từ "
        r"$n$ phần tử, \textbf{không} phân biệt thứ tự, số cách là $C_n^k$."
        "\\\\\n"
        r"Dấu hiệu nhận ra: những phần tử được chọn có \textbf{vai trò như "
        r"nhau}, đổi chỗ cho nhau vẫn là cùng một kết quả.")


def _ky_hieu_PAC(loai, n, k):
    if loai == "P":
        return "$P_{%d}$" % n
    if loai == "A":
        return "$A_{%d}^{%d}$" % (n, k)
    return "$C_{%d}^{%d}$" % (n, k)


def _tinh_PAC(loai, n, k):
    if loai == "P":
        return _hv(n)
    if loai == "A":
        return calculate_permutations(n, k)
    return calculate_coefficient(n, k)


def L10_C8_B24_TH134_MC_A_01(socau, dang=1):
    """Tính số hoán vị, chỉnh hợp, tổ hợp bằng công thức.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        loai = random.choice(["P", "A", "C"])
        n = random.randint(5, 8)
        k = random.randint(2, n - 2)
        v = (loai, n, k)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for loai, n, k in gt:
        kq = _tinh_PAC(loai, n, k)
        # nhiễu: các giá trị LÁNG GIỀNG mà học sinh hay nhầm sang
        ung_vien = [_tinh_PAC("A", n, k), _tinh_PAC("C", n, k),
                    _tinh_PAC("P", k, k), _tinh_PAC("A", n, n - k),
                    _tinh_PAC("C", n, n - k) + 1]
        nhieu = ["$%d$" % x for x in _ba_nhieu8(
            kq, ung_vien, buoc=lambda t: kq + 3 * t)]
        if loai == "P":
            ct = r"$P_{%d} = %d! = %d$" % (n, n, kq)
            nhac = r"$P_n = n!$"
        elif loai == "A":
            ct = (r"$A_{%d}^{%d} = \dfrac{%d!}{\left(%d - %d\right)!} "
                  r"= \dfrac{%d!}{%d!} = %d$" % (n, k, n, n, k, n, n - k, kq))
            nhac = r"$A_n^k = \dfrac{n!}{(n-k)!}$"
        else:
            ct = (r"$C_{%d}^{%d} = \dfrac{%d!}{%d!\left(%d - %d\right)!} = %d$"
                  % (n, k, n, k, n, k, kq))
            nhac = r"$C_n^k = \dfrac{n!}{k!(n-k)!}$"

        debai = r"Giá trị của %s bằng bao nhiêu?" % _ky_hieu_PAC(loai, n, k)
        giai = r"Áp dụng công thức %s:" % nhac + "\\\\\n" + ct + "."
        cauTN += MC_SA_answer_text(debai, "$%d$" % kq, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B24_TH134_SA_A_01(socau):
    """Giá trị của biểu thức chứa hoán vị, chỉnh hợp, tổ hợp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.randint(5, 9)
        k = random.randint(2, n - 2)
        if (n, k) not in gt:
            gt.append((n, k))

    cau = ""
    for n, k in gt:
        a = calculate_permutations(n, k)
        c = calculate_coefficient(n, k)
        kq = a + c
        debai = (r"Tính giá trị của biểu thức $M = A_{%d}^{%d} + C_{%d}^{%d}$."
                 % (n, k, n, k))
        giai = (r"$A_{%d}^{%d} = \dfrac{%d!}{%d!} = %d$." % (n, k, n, n - k, a) +
                "\\\\\n"
                r"$C_{%d}^{%d} = \dfrac{%d!}{%d!\cdot %d!} = %d$."
                % (n, k, n, k, n - k, c) +
                "\\\\\n"
                r"Vậy $M = %d + %d = %d$." % (a, c, kq))
        nhieu = _ba_nhieu8(kq, [a - c, a * c, a, c],
                           buoc=lambda t: kq + 11 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def _mtct(socau, dang, loai, ten, nhac):
    """Khung chung cho ba dạng tính bằng máy tính cầm tay.

    Số liệu cố ý lấy lớn để bấm tay không xuể - đúng tinh thần
    "tính bằng máy tính cầm tay" của Mapping.
    """
    gt = []
    while len(gt) < socau:
        if loai == "P":
            n, k = random.randint(8, 11), 0
        else:
            n = random.randint(11, 16)
            k = random.randint(3, 6)
        if (n, k) not in gt:
            gt.append((n, k))

    cauTN = ""
    for n, k in gt:
        kq = _tinh_PAC(loai, n, k)
        ung_vien = [_tinh_PAC("A", n, k) if loai != "A" else _tinh_PAC("C", n, k),
                    _tinh_PAC("C", n, k) if loai != "C" else _tinh_PAC("A", n, k),
                    _tinh_PAC("P", n, k) if loai != "P" else _hv(n - 1),
                    kq // 2 if kq > 1 else kq + 1]
        nhieu = ["$%d$" % x for x in _ba_nhieu8(
            kq, ung_vien, buoc=lambda t: kq + 13 * t)]
        debai = (r"Dùng máy tính cầm tay, tính %s. Kết quả bằng bao nhiêu?"
                 % _ky_hieu_PAC(loai, n, k))
        giai = (r"Trên máy tính cầm tay, %s" % nhac + "\\\\\n" +
                r"Kết quả: %s $= %d$." % (_ky_hieu_PAC(loai, n, k), kq))
        cauTN += MC_SA_answer_text(debai, "$%d$" % kq, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B24_TH135_MC_A_01(socau, dang=1):
    """Tính số hoán vị bằng máy tính cầm tay.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _mtct(socau, dang, "P", "hoán vị",
                 r"nhập số $n$ rồi bấm phím $x!$ (có thể phải bấm "
                 r"\texttt{SHIFT} trước), vì $P_n = n!$.")


def L10_C8_B24_TH136_MC_A_01(socau, dang=1):
    """Tính số chỉnh hợp bằng máy tính cầm tay.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _mtct(socau, dang, "A", "chỉnh hợp",
                 r"nhập $n$, bấm phím $nPr$, rồi nhập $k$.")


def L10_C8_B24_TH137_MC_A_01(socau, dang=1):
    """Tính số tổ hợp bằng máy tính cầm tay.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _mtct(socau, dang, "C", "tổ hợp",
                 r"nhập $n$, bấm phím $nCr$, rồi nhập $k$.")


def L10_C8_B24_VD138_MC_A_01(socau, dang=1):
    """Bài toán đếm thực tiễn dùng hoán vị, chỉnh hợp, tổ hợp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.randint(9, 15)
        k = random.choice([3, 4])
        co_thu_tu = random.choice([True, False])
        v = (n, k, co_thu_tu)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for n, k, co_thu_tu in gt:
        if co_thu_tu:
            kq = calculate_permutations(n, k)
            viec = (r"chọn ra $%d$ bạn giữ $%d$ chức vụ \textbf{khác nhau} "
                    r"của câu lạc bộ" % (k, k))
            ly_do = (r"Các chức vụ khác nhau nên thứ tự của $%d$ bạn được "
                     r"chọn là có phân biệt: đây là bài toán chỉnh hợp." % k)
            ct = r"$A_{%d}^{%d} = %d$" % (n, k, kq)
        else:
            kq = calculate_coefficient(n, k)
            viec = (r"chọn ra $%d$ bạn cùng tham gia một đội tình nguyện" % k)
            ly_do = (r"Các bạn trong đội có vai trò như nhau, đổi chỗ cho "
                     r"nhau vẫn là cùng một đội: đây là bài toán tổ hợp.")
            ct = r"$C_{%d}^{%d} = %d$" % (n, k, kq)

        ung_vien = [calculate_permutations(n, k), calculate_coefficient(n, k),
                    _hv(k), calculate_coefficient(n, k) * _hv(k) + 1]
        nhieu = ["$%d$" % x for x in _ba_nhieu8(
            kq, ung_vien, buoc=lambda t: kq + 17 * t)]

        debai = (r"Một câu lạc bộ có $%d$ thành viên. Cần %s. Hỏi có bao "
                 r"nhiêu cách?" % (n, viec))
        giai = ly_do + "\\\\\n" + r"Vậy số cách là %s." % ct
        cauTN += MC_SA_answer_text(debai, "$%d$" % kq, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B24_VD138_TL_A_01(socau, dong=1):
    """Tự luận: bài toán đếm có điều kiện ràng buộc.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Bài xếp hàng có hai bạn phải đứng cạnh nhau - cách làm "buộc hai bạn
    thành một khối" là cách chuẩn của SGK lớp 10, không dùng gì ngoài
    hoán vị.
    """
    gt = []
    while len(gt) < socau:
        n = random.randint(5, 8)
        if n not in gt:
            gt.append(n)
        if len(gt) >= 4:
            break

    cauTN = ""
    for n in gt:
        tong = _hv(n)
        canh_nhau = 2 * _hv(n - 1)
        khong_canh = tong - canh_nhau

        debai = (r"Xếp $%d$ học sinh, trong đó có hai bạn An và Bình, thành "
                 r"một hàng ngang. Các học sinh đôi một khác nhau." % n)

        hoi_a = r"Hỏi có bao nhiêu cách xếp?"
        giai_a = (r"Xếp toàn bộ $%d$ học sinh theo thứ tự là một hoán vị của "
                  r"$%d$ phần tử:" % (n, n) +
                  "\\\\\n"
                  r"$P_{%d} = %d! = %d$ (cách)." % (n, n, tong))

        hoi_b = r"Hỏi có bao nhiêu cách xếp sao cho An và Bình \textbf{đứng cạnh nhau}?"
        giai_b = (r"Buộc An và Bình thành một khối, khi đó ta xếp $%d$ đối "
                  r"tượng (khối đó và $%d$ bạn còn lại):" % (n - 1, n - 2) +
                  "\\\\\n"
                  r"$P_{%d} = %d! = %d$ (cách)." % (n - 1, n - 1, _hv(n - 1)) +
                  "\\\\\n"
                  r"Trong khối, An và Bình còn đổi chỗ cho nhau được $2$ cách."
                  "\\\\\n"
                  r"Vậy số cách xếp là $%d \cdot 2 = %d$ (cách)."
                  % (_hv(n - 1), canh_nhau))

        hoi_c = r"Hỏi có bao nhiêu cách xếp sao cho An và Bình \textbf{không đứng cạnh nhau}?"
        giai_c = (r"Lấy tổng số cách xếp trừ đi số cách xếp mà An và Bình "
                  r"đứng cạnh nhau:"
                  "\\\\\n"
                  r"$%d - %d = %d$ (cách)." % (tong, canh_nhau, khong_canh))

        ds_abcd = [(hoi_a, "%d" % tong, giai_a),
                   (hoi_b, "%d" % canh_nhau, giai_b),
                   (hoi_c, "%d" % khong_canh, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BÀI 25. NHỊ THỨC NEWTON
# Lớp 10 CHỈ học n = 4 và n = 5 (SGK KNTT), không dùng n tổng quát.
# =====================================================================

def _da_thuc(hs):
    r"""Viết đa thức $\sum hs[k]\,x^{n-k}$ thành LaTeX, n = len(hs) - 1."""
    n = len(hs) - 1
    cac_hang = []
    for k, c in enumerate(hs):
        mu = n - k
        if c == 0:
            continue
        if mu == 0:
            bien = ""
        elif mu == 1:
            bien = "x"
        else:
            bien = "x^{%d}" % mu
        if bien and abs(c) == 1:
            he_so = "" if c > 0 else "-"
        else:
            he_so = "%d" % c
        hang = he_so + bien
        if not cac_hang:
            cac_hang.append(hang)
        elif c > 0:
            cac_hang.append("+ " + hang)
        else:
            cac_hang.append("- " + hang.lstrip("-"))
    return "$" + " ".join(cac_hang) + "$"


def _khai_trien(socau, dang, n):
    """Khung chung cho hai dạng khai triển nhị thức, n = 4 hoặc n = 5."""
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, -2, -3])
        if a not in gt:
            gt.append(a)
        if len(gt) >= 4:
            break

    cauTN = ""
    for a in gt:
        dung_hs = [calculate_coefficient(n, k) * a ** k for k in range(n + 1)]
        sai1 = [calculate_coefficient(n, k) * a for k in range(n + 1)]
        sai2 = [a ** k for k in range(n + 1)]
        sai3 = [(-1) ** k * calculate_coefficient(n, k) * a ** k
                for k in range(n + 1)]
        dung = _da_thuc(dung_hs)
        nhieu = _ba_nhieu8(dung, [_da_thuc(sai1), _da_thuc(sai2),
                                  _da_thuc(sai3)],
                           buoc=lambda t: _da_thuc(
                               [calculate_coefficient(n, k) * a ** k + t
                                for k in range(n + 1)]))

        dau = "+" if a > 0 else "-"
        debai = (r"Khai triển nhị thức Newton $\left(x %s %d\right)^{%d}$ ta "
                 r"được kết quả nào sau đây?" % (dau, abs(a), n))

        cac_dong = []
        for k in range(n + 1):
            cac_dong.append(
                r"$C_{%d}^{%d}\,x^{%d}\cdot\left(%d\right)^{%d} = %d x^{%d}$"
                % (n, k, n - k, a, k, dung_hs[k], n - k))
        giai = (r"Công thức nhị thức Newton:"
                "\\\\\n"
                r"$\left(x + a\right)^{%d} = C_{%d}^{0}x^{%d} + "
                r"C_{%d}^{1}x^{%d}a + \ldots + C_{%d}^{%d}a^{%d}$, "
                r"với $a = %d$." % (n, n, n, n, n - 1, n, n, n, a) +
                "\\\\\n" + ";\\\\\n".join(cac_dong) + "." +
                "\\\\\n"
                r"Cộng lại được %s." % dung)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B25_TH139_MC_A_01(socau, dang=1):
    """Khai triển nhị thức Newton với n = 4.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _khai_trien(socau, dang, 4)


def L10_C8_B25_TH140_MC_A_01(socau, dang=1):
    """Khai triển nhị thức Newton với n = 5.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _khai_trien(socau, dang, 5)


def _he_so_mot_nhi_thuc(socau, n):
    """Khung chung: hệ số của x^k trong khai triển (a + bx)^n."""
    gt = []
    while len(gt) < socau:
        a = random.randint(1, 3)
        b = random.choice([2, 3, -2, -3])
        k = random.randint(1, n - 1)
        v = (a, b, k)
        if v not in gt:
            gt.append(v)

    cau = ""
    for a, b, k in gt:
        kq = calculate_coefficient(n, k) * a ** (n - k) * b ** k
        dau = "+" if b > 0 else "-"
        debai = (r"Tìm hệ số của $x^{%d}$ trong khai triển "
                 r"$\left(%d %s %dx\right)^{%d}$."
                 % (k, a, dau, abs(b), n))
        giai = (r"Số hạng tổng quát của khai triển "
                r"$\left(a + bx\right)^{%d}$ là $C_{%d}^{k}\,a^{%d-k}\,"
                r"\left(bx\right)^{k}$, với $a = %d$, $b = %d$."
                % (n, n, n, a, b) +
                "\\\\\n"
                r"Số hạng chứa $x^{%d}$ ứng với $k = %d$:" % (k, k) +
                "\\\\\n"
                r"$C_{%d}^{%d}\cdot %d^{%d}\cdot\left(%d\right)^{%d} = %d$."
                % (n, k, a, n - k, b, k, kq) +
                "\\\\\n"
                r"Vậy hệ số cần tìm là $%d$." % kq)
        ung_vien = [calculate_coefficient(n, k) * a ** k * b ** (n - k),
                    calculate_coefficient(n, k) * b ** k,
                    a ** (n - k) * b ** k,
                    -kq]
        nhieu = _ba_nhieu8(kq, ung_vien, buoc=lambda t: kq + 7 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C8_B25_TH139_SA_A_01(socau):
    """Hệ số trong khai triển với n = 4.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _he_so_mot_nhi_thuc(socau, 4)


def L10_C8_B25_TH140_SA_A_01(socau):
    """Hệ số trong khai triển với n = 5.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    return _he_so_mot_nhi_thuc(socau, 5)


def L10_C8_B25_VD141_MC_A_01(socau, dang=1):
    """Tìm hệ số của một số hạng trong khai triển.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Khác dạng TH139/TH140 ở chỗ phải khai triển HAI nhị thức rồi cộng hệ
    số cùng bậc lại - không thay thẳng vào một công thức được.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([1, 2, -2])
        b = random.choice([1, 2, -2, 3])
        k = random.choice([2, 3])
        v = (a, b, k)
        if v not in gt:
            gt.append(v)

    def _viet(he_so):
        return ("1 + %dx" % he_so) if he_so > 0 else ("1 - %dx" % abs(he_so))

    cauTN = ""
    for a, b, k in gt:
        p4 = calculate_coefficient(4, k) * a ** k
        p5 = calculate_coefficient(5, k) * b ** k
        kq = p4 + p5
        ung_vien = [p4, p5, p4 * p5, abs(p4 - p5)]
        nhieu = ["$%d$" % x for x in _ba_nhieu8(
            kq, ung_vien, buoc=lambda t: kq + 9 * t)]

        debai = (r"Tìm hệ số của $x^{%d}$ trong khai triển của biểu thức "
                 r"$P(x) = \left(%s\right)^{4} + \left(%s\right)^{5}$."
                 % (k, _viet(a), _viet(b)))
        giai = (r"Hệ số của $x^{%d}$ trong $\left(%s\right)^{4}$ là "
                r"$C_{4}^{%d}\cdot\left(%d\right)^{%d} = %d$."
                % (k, _viet(a), k, a, k, p4) +
                "\\\\\n"
                r"Hệ số của $x^{%d}$ trong $\left(%s\right)^{5}$ là "
                r"$C_{5}^{%d}\cdot\left(%d\right)^{%d} = %d$."
                % (k, _viet(b), k, b, k, p5) +
                "\\\\\n"
                r"Hai khai triển cộng vào nhau nên hệ số cùng bậc cộng lại: "
                r"$%d + %d = %d$." % (p4, p5, kq))
        cauTN += MC_SA_answer_text(debai, "$%d$" % kq, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C8_B25_VD141_SA_A_01(socau):
    """Hệ số của số hạng chứa x mũ k - tổng các hệ số của khai triển.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Tổng các hệ số bằng giá trị của biểu thức tại x = 1; cách này nằm
    trọn trong lớp 10 và là chỗ hay hỏi ở mức vận dụng.
    """
    gt = []
    while len(gt) < socau:
        a = random.choice([2, 3, -2])
        n = random.choice([4, 5])
        if (a, n) not in gt:
            gt.append((a, n))

    cau = ""
    for a, n in gt:
        kq = (1 + a) ** n
        dau = "+" if a > 0 else "-"
        cac_hs = [calculate_coefficient(n, k) * a ** k for k in range(n + 1)]
        debai = (r"Tính tổng tất cả các hệ số trong khai triển của "
                 r"$\left(1 %s %dx\right)^{%d}$." % (dau, abs(a), n))
        giai = (r"Khai triển có dạng $a_0 + a_1x + \ldots + a_{%d}x^{%d}$, "
                r"nên tổng các hệ số $a_0 + a_1 + \ldots + a_{%d}$ chính là "
                r"giá trị của biểu thức tại $x = 1$." % (n, n, n) +
                "\\\\\n"
                r"Thay $x = 1$: $\left(1 %s %d\right)^{%d} = "
                r"\left(%d\right)^{%d} = %d$."
                % (dau, abs(a), n, 1 + a, n, kq) +
                "\\\\\n"
                r"Kiểm tra lại bằng cách cộng trực tiếp: $%s = %d$."
                % (" + ".join(("%d" % c) if c >= 0 else ("(%d)" % c)
                              for c in cac_hs), kq))
        nhieu = _ba_nhieu8(kq, [(1 - a) ** n, 2 ** n, (1 + a) * n, a ** n],
                           buoc=lambda t: kq + 6 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


# =====================================================================
# CÂU ĐÚNG/SAI - bốn ý phải TĂNG DẦN mức độ NB, TH, VD, VDC
# =====================================================================

def L10_C8_TF_A_01(socau, socot=1):
    """Đúng/Sai - quy tắc đếm; hoán vị, chỉnh hợp, tổ hợp.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        nam = random.randint(5, 8)
        nu = random.randint(4, 7)
        if (nam, nu) not in gt:
            gt.append((nam, nu))

    cauTF = ''
    for nam, nu in gt:
        tong = nam + nu
        chon2 = calculate_coefficient(tong, 2)
        a2 = calculate_permutations(tong, 2)
        mot_nam_mot_nu = nam * nu
        cung_gioi = chon2 - mot_nam_mot_nu

        debai = (r"Một tổ có $%d$ học sinh nam và $%d$ học sinh nữ, các học "
                 r"sinh đôi một khác nhau." % (nam, nu))

        ds_abcd = (
            # a) NB - nhắc lại một công thức
            [
                (r"{\True Số cách xếp toàn bộ $%d$ học sinh của tổ thành một "
                 r"hàng dọc là $%d!$}" % (tong, tong),
                 r"Đúng. Xếp tất cả $%d$ phần tử theo thứ tự là một hoán vị: "
                 r"$P_{%d} = %d!$." % (tong, tong, tong)),
                (r"{Số cách xếp toàn bộ $%d$ học sinh của tổ thành một hàng "
                 r"dọc là $%d^{2}$}" % (tong, tong),
                 r"Sai. Đó là hoán vị của $%d$ phần tử nên bằng $%d!$, không "
                 r"phải $%d^{2}$." % (tong, tong, tong)),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True Số cách chọn $2$ học sinh bất kì của tổ là $%d$}"
                 % chon2,
                 r"Đúng. Hai bạn được chọn có vai trò như nhau nên đây là tổ "
                 r"hợp: $C_{%d}^{2} = %d$." % (tong, chon2)),
                (r"{Số cách chọn $2$ học sinh bất kì của tổ là $%d$}" % a2,
                 r"Sai. $%d$ là $A_{%d}^{2}$, dùng khi hai vị trí có vai trò "
                 r"khác nhau. Ở đây hai bạn như nhau nên phải dùng "
                 r"$C_{%d}^{2} = %d$." % (a2, tong, tong, chon2)),
            ],
            # c) VD - phải có kết quả ý trước mới làm được
            [
                (r"{\True Số cách chọn $2$ học sinh gồm $1$ nam và $1$ nữ là "
                 r"$%d$}" % mot_nam_mot_nu,
                 r"Đúng. Chọn một bạn nam rồi chọn một bạn nữ, dùng quy tắc "
                 r"nhân: $%d \cdot %d = %d$." % (nam, nu, mot_nam_mot_nu)),
                (r"{Số cách chọn $2$ học sinh gồm $1$ nam và $1$ nữ là $%d$}"
                 % tong,
                 r"Sai. $%d$ là số cách chọn MỘT bạn bất kì (quy tắc cộng). "
                 r"Chọn một nam và một nữ phải dùng quy tắc nhân: "
                 r"$%d \cdot %d = %d$." % (tong, nam, nu, mot_nam_mot_nu)),
            ],
            # d) VDC - phải tự nghĩ ra cách, không có công thức sẵn
            [
                (r"{\True Số cách chọn $2$ học sinh cùng giới tính là $%d$}"
                 % cung_gioi,
                 r"Đúng. Lấy tổng số cách chọn $2$ bạn bất kì trừ đi số cách "
                 r"chọn $1$ nam $1$ nữ: $%d - %d = %d$."
                 "\\\\\n"
                 r"Cách khác: $C_{%d}^{2} + C_{%d}^{2} = %d + %d = %d$."
                 % (chon2, mot_nam_mot_nu, cung_gioi, nam, nu,
                    calculate_coefficient(nam, 2),
                    calculate_coefficient(nu, 2), cung_gioi)),
                (r"{Số cách chọn $2$ học sinh cùng giới tính là $%d$}" % chon2,
                 r"Sai. $%d$ là số cách chọn $2$ bạn \textbf{bất kì}. Phải "
                 r"trừ đi $%d$ cách chọn $1$ nam $1$ nữ mới ra $%d$."
                 % (chon2, mot_nam_mot_nu, cung_gioi)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


def L10_C8_TF_B_01(socau, socot=1):
    """Đúng/Sai - nhị thức Newton.

    Dựa trên bài K10_8_DS_1_TH của cô Lan, xếp lại bốn ý theo đúng thang
    NB - TH - VD - VDC (bản cũ bốn ý ngang mức nhau), và bỏ vòng lặp
    "while l > n: k = np.randint([1, n-1])" - vòng đó truyền một LIST cho
    randint và không cập nhật l, nếu rơi vào thì treo máy.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([4, 5])
        k = random.randint(1, n - 1)
        a = random.randint(2, 4)
        v = (n, k, a)
        if v not in gt:
            gt.append(v)

    cauTF = ''
    for n, k, a in gt:
        # nhị thức (a + a x)^n
        he_so = calculate_coefficient(n, k) * a ** n
        tong_he_so = (a + a) ** n
        k_lech = k + 1 if k + 1 != n - k else max(1, k - 1)

        debai = (r"Xét khai triển nhị thức Newton của "
                 r"$\left(%d + %dx\right)^{%d}$." % (a, a, n))

        ds_abcd = (
            # a) NB - nhắc lại một tính chất
            [
                (r"{\True Khai triển này có $%d$ số hạng}" % (n + 1),
                 r"Đúng. Khai triển $\left(a + bx\right)^{n}$ có $n + 1$ số "
                 r"hạng, ứng với $k = 0,\ 1,\ \ldots,\ %d$." % n),
                (r"{Khai triển này có $%d$ số hạng}" % n,
                 r"Sai. Chỉ số $k$ chạy từ $0$ đến $%d$ nên có $%d$ số hạng."
                 % (n, n + 1)),
            ],
            # b) TH - thay số vào đúng một công thức
            [
                (r"{\True Hệ số của $x^{%d}$ trong khai triển bằng $%d$}"
                 % (k, he_so),
                 r"Đúng. Số hạng chứa $x^{%d}$ là $C_{%d}^{%d}\cdot "
                 r"%d^{%d}\cdot\left(%dx\right)^{%d} = %dx^{%d}$."
                 % (k, n, k, a, n - k, a, k, he_so, k)),
                (r"{Hệ số của $x^{%d}$ trong khai triển bằng $%d$}"
                 % (k, calculate_coefficient(n, k)),
                 r"Sai. $C_{%d}^{%d} = %d$ mới chỉ là hệ số nhị thức, còn "
                 r"phải nhân thêm $%d^{%d}\cdot %d^{%d}$ nữa, được $%d$."
                 % (n, k, calculate_coefficient(n, k), a, n - k, a, k, he_so)),
            ],
            # c) VD - phải hiểu ý trước mới kết luận được
            [
                (r"{\True Hệ số của $x^{%d}$ bằng hệ số của $x^{%d}$}"
                 % (k, n - k),
                 r"Đúng. Hệ số của $x^{k}$ là $C_{%d}^{k}\cdot %d^{%d-k}"
                 r"\cdot %d^{k} = C_{%d}^{k}\cdot %d^{%d}$ - phần luỹ thừa "
                 r"KHÔNG phụ thuộc $k$ vì hai số hạng của nhị thức bằng nhau. "
                 r"Mà $C_{%d}^{%d} = C_{%d}^{%d}$ nên hai hệ số bằng nhau."
                 % (n, a, n, a, n, a, n, n, k, n, n - k)),
                (r"{Hệ số của $x^{%d}$ bằng hệ số của $x^{%d}$}"
                 % (k, k_lech),
                 r"Sai. Tính đối xứng cho hệ số của $x^{%d}$ bằng hệ số của "
                 r"$x^{%d}$, chứ không phải $x^{%d}$." % (k, n - k, k_lech)),
            ],
            # d) VDC - phải tự nghĩ ra cách, không có công thức sẵn
            [
                (r"{\True Tổng tất cả các hệ số của khai triển bằng $%d$}"
                 % tong_he_so,
                 r"Đúng. Viết khai triển là $a_0 + a_1x + \ldots + "
                 r"a_{%d}x^{%d}$. Thay $x = 1$: vế phải thành đúng tổng các "
                 r"hệ số, vế trái thành $\left(%d + %d\right)^{%d} = %d$."
                 % (n, n, a, a, n, tong_he_so)),
                (r"{Tổng tất cả các hệ số của khai triển bằng $%d$}" % (a ** n),
                 r"Sai. Thay $x = 1$ được $\left(%d + %d\right)^{%d} = %d$, "
                 r"chứ không phải $%d^{%d} = %d$."
                 % (a, a, n, tong_he_so, a, n, a ** n)),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)
    return cauTF


# ---------------------------------------------------------------------
# Ba dạng bổ sung: bộ chọn câu cần TRẢ LỜI NGẮN cho VD130, VD138 và
# TỰ LUẬN cho VD141, nhưng Mapping chưa khai nên đề hệ số 1 bị thiếu câu.
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
# ---------------------------------------------------------------------

def L10_C8_B23_VD130_SA_A_01(socau):
    """Trả lời ngắn: bài toán đếm thực tiễn dùng quy tắc cộng và nhân.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = (random.randint(3, 6), random.randint(3, 6), random.randint(2, 5))
        if v[0] != v[1] and v not in gt:
            gt.append(v)

    cau = ""
    for m, n, p in gt:
        kq = (m + n) * p
        debai = (r"Từ thành phố $A$ đến thành phố $C$ bắt buộc phải đi qua "
                 r"thành phố $B$. Từ $A$ đến $B$ có $%d$ tuyến xe khách và "
                 r"$%d$ tuyến tàu hoả; từ $B$ đến $C$ có $%d$ tuyến xe khách. "
                 r"Hỏi có bao nhiêu cách đi từ $A$ đến $C$?" % (m, n, p))
        giai = (r"Chặng $A \to B$: đi xe khách \textbf{hoặc} tàu hoả, hai "
                r"phương án loại trừ nhau nên dùng quy tắc cộng, được "
                r"$%d + %d = %d$ cách." % (m, n, m + n) +
                "\\\\\n"
                r"Đi từ $A$ đến $C$ phải qua chặng $A \to B$ \textbf{rồi} "
                r"chặng $B \to C$ nên dùng quy tắc nhân:"
                "\\\\\n"
                r"$%d \cdot %d = %d$ (cách)." % (m + n, p, kq))
        nhieu = _ba_nhieu8(kq, [m + n + p, m * n * p, m * p + n, m + n * p],
                           buoc=lambda t: kq + 5 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C8_B24_VD138_SA_A_01(socau):
    """Trả lời ngắn: đếm thực tiễn dùng tổ hợp, có điều kiện về thành phần.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        nam = random.randint(6, 10)
        nu = random.randint(5, 9)
        v = (nam, nu)
        if v not in gt:
            gt.append(v)

    cau = ""
    for nam, nu in gt:
        c_nam = calculate_coefficient(nam, 2)
        kq = c_nam * nu
        debai = (r"Một tổ có $%d$ học sinh nam và $%d$ học sinh nữ. Cần chọn "
                 r"một nhóm gồm $3$ học sinh, trong đó có \textbf{đúng $2$ "
                 r"nam và $1$ nữ}, các bạn trong nhóm có vai trò như nhau. "
                 r"Hỏi có bao nhiêu cách chọn?" % (nam, nu))
        giai = (r"Chọn $2$ bạn nam trong $%d$ bạn nam, các bạn có vai trò như "
                r"nhau nên là tổ hợp: $C_{%d}^{2} = %d$ cách."
                % (nam, nam, c_nam) +
                "\\\\\n"
                r"Chọn $1$ bạn nữ trong $%d$ bạn nữ: $%d$ cách." % (nu, nu) +
                "\\\\\n"
                r"Phải làm đủ hai công đoạn nên dùng quy tắc nhân:"
                "\\\\\n"
                r"$%d \cdot %d = %d$ (cách)." % (c_nam, nu, kq))
        nhieu = _ba_nhieu8(
            kq, [c_nam + nu, calculate_coefficient(nam + nu, 3),
                 calculate_permutations(nam, 2) * nu,
                 calculate_coefficient(nam, 2) * calculate_coefficient(nu, 2)],
            buoc=lambda t: kq + 13 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C8_B25_VD141_TL_A_01(socau, dong=1):
    """Tự luận: khai triển nhị thức Newton và các hệ số.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        n = random.choice([4, 5])
        a = random.choice([2, 3, -2])
        k = random.randint(1, n - 1)
        v = (n, a, k)
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for n, a, k in gt:
        dau = "+" if a > 0 else "-"
        cac_hs = [calculate_coefficient(n, j) * a ** j for j in range(n + 1)]
        he_so_k = cac_hs[k]
        tong = (1 + a) ** n
        lon_nhat = max(cac_hs)
        vi_tri = [j for j, c in enumerate(cac_hs) if c == lon_nhat]

        debai = (r"Cho biểu thức $P(x) = \left(1 %s %dx\right)^{%d}$."
                 % (dau, abs(a), n))

        hoi_a = r"Viết khai triển nhị thức Newton của $P(x)$."
        giai_a = (r"$P(x) = %s$." % _da_thuc(list(reversed(cac_hs))) +
                  "\\\\\n"
                  r"(Số hạng chứa $x^{j}$ có hệ số $C_{%d}^{j}\cdot "
                  r"\left(%d\right)^{j}$.)" % (n, a))

        hoi_b = r"Tìm hệ số của $x^{%d}$ trong khai triển." % k
        giai_b = (r"Hệ số của $x^{%d}$ là $C_{%d}^{%d}\cdot"
                  r"\left(%d\right)^{%d} = %d\cdot %d = %d$."
                  % (k, n, k, a, k, calculate_coefficient(n, k),
                     a ** k, he_so_k))

        hoi_c = r"Tính tổng tất cả các hệ số trong khai triển của $P(x)$."
        giai_c = (r"Tổng các hệ số chính là giá trị của $P(x)$ tại $x = 1$:"
                  "\\\\\n"
                  r"$P(1) = \left(1 %s %d\right)^{%d} = "
                  r"\left(%d\right)^{%d} = %d$."
                  % (dau, abs(a), n, 1 + a, n, tong) +
                  "\\\\\n"
                  r"Cộng trực tiếp để kiểm tra: $%s = %d$."
                  % (" + ".join(("%d" % c) if c >= 0 else ("(%d)" % c)
                                for c in cac_hs), tong))

        ds_abcd = [(hoi_a, r"P(x) = %s" % _da_thuc(list(reversed(cac_hs))).strip("$"), giai_a),
                   (hoi_b, "%d" % he_so_k, giai_b),
                   (hoi_c, "%d" % tong, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN
