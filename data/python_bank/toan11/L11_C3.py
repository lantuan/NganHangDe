# -*- coding: utf-8 -*-
r"""Lớp 11 - Chương 3. Các số đặc trưng đo xu thế trung tâm của mẫu số
liệu ghép nhóm (bộ Kết nối tri thức với cuộc sống).

CLAUDE VIET MOI 29/09/2026 - co Lan kiem tra lai noi dung toan.

Quy ước của SGK KNTT lớp 11 dùng trong tệp này:

  * Nhóm ghép là nửa khoảng $[u_i;\ u_{i+1})$, giá trị đại diện của nhóm
    là TRUNG ĐIỂM $c_i = \dfrac{u_i + u_{i+1}}{2}$.
  * Số trung bình: $\bar{x} = \dfrac{\sum n_i c_i}{n}$.
  * Trung vị: tìm nhóm chứa giá trị thứ $\dfrac{n}{2}$ (KHÔNG phải
    $\dfrac{n+1}{2}$ như mẫu không ghép nhóm ở lớp 10), rồi
    $M_e = u_m + \dfrac{\frac{n}{2} - C}{n_m}\left(u_{m+1} - u_m\right)$
    với $C$ là tần số tích luỹ của các nhóm ĐỨNG TRƯỚC nhóm $m$.
  * Tứ phân vị: cùng công thức, thay $\dfrac{n}{2}$ bằng $\dfrac{n}{4}$
    (cho $Q_1$) và $\dfrac{3n}{4}$ (cho $Q_3$); $Q_2 = M_e$.
  * Mốt: nhóm có tần số lớn nhất, rồi
    $M_o = u_m + \dfrac{n_m - n_{m-1}}{\left(n_m - n_{m-1}\right) +
    \left(n_m - n_{m+1}\right)}\left(u_{m+1} - u_m\right)$.

Số liệu được chọn để ĐÁP SỐ ĐẸP: cỡ mẫu $n$ chia hết cho 4, các vị trí
$\frac{n}{4}$, $\frac{n}{2}$, $\frac{3n}{4}$ đều rơi HẲN vào trong một
nhóm (không rơi đúng đầu mút), và mọi đáp số đều là số thập phân hữu hạn
không quá hai chữ số lẻ - câu trả lời ngắn chấm bằng SO KHỚP CHUỖI nên
đáp số phải viết được chính xác.

Bài học từ lớp 10 (xem docs/16_CHANGELOG Version 3.14) đã áp dụng ở đây:
  * chữ tiếng Việt KHÔNG bao giờ nằm trần trong $...$ (mất hết dấu cách
    khi hiện trên web) - luôn bọc \text{...} hoặc để ngoài công thức;
  * không dùng chữ đậm kiểu Markdown, chỉ dùng \textbf{...};
  * mọi chuỗi có dấu gạch chéo đều là chuỗi r"..." nên "\\" ra đúng hai
    dấu gạch chéo (dấu xuống dòng của LaTeX);
  * mọi danh sách phương án nhiễu đều đi qua _ba_nhieu11.
"""
import math
import random

from math_type import *          # noqa: F401,F403

DAU_THAP_PHAN = ","


# =====================================================================
# HÀM PHỤ TRỢ
# =====================================================================

def _xx(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết theo cách viết Việt Nam."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _ba_nhieu11(dapso, ung_vien, buoc=None):
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


def _tron(x, n=2):
    """Làm tròn thật (dùng để so sánh), tránh sai số dấu phẩy động."""
    return round(float(x) + 1e-12, n)


def _mau_ghep_nhom(so_nhom=4, h=10, dau=20, lan_thu=400):
    r"""Sinh một mẫu số liệu ghép nhóm "đẹp".

    Trả về (bien, tanso) với bien = [u_0, u_1, ..., u_k] (k+1 đầu mút,
    các nhóm đều rộng h) và tanso = [n_1, ..., n_k].

    Điều kiện để đáp số đẹp:
      * n chia hết cho 4;
      * cả ba vị trí n/4, n/2, 3n/4 rơi HẲN vào trong một nhóm, không
        rơi đúng vào tần số tích luỹ (nếu rơi đúng đầu mút thì công thức
        vẫn dùng được nhưng đề trở nên khó đọc, dễ gây tranh cãi);
      * mốt duy nhất, và nhóm chứa mốt KHÔNG phải nhóm đầu hay nhóm cuối
        (để công thức mốt dùng được cả n_{m-1} lẫn n_{m+1});
      * mọi số đặc trưng đều tròn không quá hai chữ số thập phân.
    """
    for _ in range(lan_thu):
        tanso = [random.randint(2, 12) for _ in range(so_nhom)]
        n = sum(tanso)
        if n % 4 or n < 16:
            continue
        # mot duy nhat, khong o hai dau
        lon_nhat = max(tanso)
        if tanso.count(lon_nhat) != 1:
            continue
        vi_tri_mot = tanso.index(lon_nhat)
        if vi_tri_mot in (0, so_nhom - 1):
            continue
        # ba vi tri tu phan vi phai roi HAN vao trong mot nhom
        tich_luy = []
        s = 0
        for t in tanso:
            s += t
            tich_luy.append(s)
        vi_tri = [n / 4.0, n / 2.0, 3 * n / 4.0]
        if any(abs(v - c) < 1e-9 for v in vi_tri for c in [0] + tich_luy):
            continue
        bien = [dau + i * h for i in range(so_nhom + 1)]
        # Moi so dac trung phai LAM TRON duoc dut khoat den hang phan
        # tram: tranh cac gia tri roi sat mep .xx5 vi luc ay hoc sinh
        # lam tron len hay xuong deu co ly, ma cau tra loi ngan cham
        # bang SO KHOP CHUOI nen se cham oan.
        gia_tri = [_so_trung_binh(bien, tanso), _mot(bien, tanso)]
        gia_tri += [_phan_vi(bien, tanso, k) for k in (1, 2, 3)]
        if any(abs(g * 1000 - round(g * 1000)) < 1e-6 and
               round(g * 1000) % 10 == 5 for g in gia_tri):
            continue
        return bien, tanso
    return None


def _trung_diem(bien):
    return [(bien[i] + bien[i + 1]) / 2.0 for i in range(len(bien) - 1)]


def _so_trung_binh(bien, tanso):
    c = _trung_diem(bien)
    return sum(t * x for t, x in zip(tanso, c)) / float(sum(tanso))


def _nhom_chua(tanso, moc):
    """Chỉ số nhóm chứa giá trị thứ `moc` và tần số tích luỹ trước đó."""
    s = 0
    for i, t in enumerate(tanso):
        if s + t > moc - 1e-9:
            return i, s
        s += t
    return len(tanso) - 1, s - tanso[-1]


def _phan_vi(bien, tanso, k):
    r"""$Q_k$ theo công thức của SGK: k = 1, 2, 3 (k = 2 chính là trung vị)."""
    n = sum(tanso)
    moc = k * n / 4.0
    i, truoc = _nhom_chua(tanso, moc)
    h = bien[i + 1] - bien[i]
    return bien[i] + (moc - truoc) / tanso[i] * h


def _mot(bien, tanso):
    i = tanso.index(max(tanso))
    truoc = tanso[i - 1] if i > 0 else 0
    sau = tanso[i + 1] if i < len(tanso) - 1 else 0
    h = bien[i + 1] - bien[i]
    return bien[i] + (tanso[i] - truoc) / float((tanso[i] - truoc) + (tanso[i] - sau)) * h


def _dai_dien_mot_dong(bien, tanso):
    r"""Viết giá trị đại diện thành MỘT DÒNG chữ, không dùng tabular.

    MathJax trên trang làm bài KHÔNG dựng được môi trường tabular - bảng
    viết bằng tabular sẽ biến mất khi học sinh xem lời giải trên web.
    Bảng số liệu của ĐỀ thì vẽ bằng TikZ (xem _hinh_bang) vì được dịch
    sẵn ra ảnh; còn trong LỜI GIẢI chỉ cần liệt kê một dòng là đủ rõ.
    """
    c = _trung_diem(bien)
    return ("; ".join(r"$c_{%d} = %s$ (tần số $%d$)" % (i + 1, _xx(x), t)
                      for i, (x, t) in enumerate(zip(c, tanso))) + ".")


BOI_CANH = [
    ("chiều cao của %d cây giống trong một vườn ươm", "cm", 20, 10),
    ("cân nặng của %d học sinh lớp 11A", "kg", 40, 5),
    ("thời gian tự học trong một tuần của %d học sinh", "giờ", 5, 5),
    ("số giờ nắng trong %d ngày của một trạm quan trắc", "giờ", 4, 2),
    # Diem phai nam tron trong thang 10: bat dau tu 2, bon nhom rong 2
    # -> [2;4), [4;6), [6;8), [8;10). Neu bat dau tu 4 thi nhom cuoi
    # thanh [10;12) - khong co diem nao nhu vay.
    ("điểm kiểm tra môn Toán của %d học sinh", "điểm", 2, 2),
]


def _hinh_bang(bien, tanso, ten_nhom="Nhóm", ten_tan="Tần số"):
    r"""Bảng tần số ghép nhóm vẽ bằng TikZ THUẦN (chỉ \draw và \node).

    Vì sao vẽ bằng TikZ chứ không dùng tabular: trang làm bài trên web
    hiện đề bằng MathJax, mà MathJax KHÔNG dựng được môi trường tabular
    - bảng sẽ biến mất, và mất bảng thì câu hỏi không còn làm được nữa.
    Hình TikZ thì được dịch sẵn ra ảnh lúc sinh đề (hinh_ve_service) nên
    hiện đúng ở cả PDF lẫn web. Cô Lan chốt 27/09/2026: "câu có hình thì
    phải có hình cả trên web".

    Cũng KHÔNG dùng tkz-tab: máy cô Lan thiếu gói tabvar.
    """
    k = len(tanso)
    # Bang nam o cot phai cua \immini nen phai GON: ca bang khong qua
    # khoang 8 don vi TikZ thi moi vua nua trang giay.
    rong = 1.55                      # bề rộng một ô
    cao = 0.72
    x0 = 1.7                         # bề rộng cột nhãn bên trái
    dai = x0 + k * rong
    dong = []
    dong.append(r"\begin{tikzpicture}[scale=1, font=\scriptsize]")
    # khung ngoai va hai duong ngang
    for y in (0, -cao, -2 * cao):
        dong.append(r"\draw (0,%s) -- (%s,%s);" % (_toa(y), _toa(dai), _toa(y)))
    # cac duong doc
    dong.append(r"\draw (0,0) -- (0,%s);" % _toa(-2 * cao))
    for i in range(k + 1):
        x = x0 + i * rong
        dong.append(r"\draw (%s,0) -- (%s,%s);" % (_toa(x), _toa(x), _toa(-2 * cao)))
    # nhan hai hang
    dong.append(r"\node at (%s,%s) {%s};" % (_toa(x0 / 2), _toa(-cao / 2), ten_nhom))
    dong.append(r"\node at (%s,%s) {%s};" % (_toa(x0 / 2), _toa(-3 * cao / 2), ten_tan))
    for i in range(k):
        x = x0 + i * rong + rong / 2
        dong.append(r"\node at (%s,%s) {$\left[%g;\ %g\right)$};"
                    % (_toa(x), _toa(-cao / 2), bien[i], bien[i + 1]))
        dong.append(r"\node at (%s,%s) {$%d$};"
                    % (_toa(x), _toa(-3 * cao / 2), tanso[i]))
    dong.append(r"\end{tikzpicture}")
    return "\n".join(dong)


def _toa(x):
    """Số dùng làm toạ độ TikZ - LUÔN dấu chấm, không phải dấu phẩy.

    Bài học lớp 10 chương 4: hàm viết số kiểu Việt Nam đổi dấu chấm
    thành dấu phẩy, nên "(4.4, 2.2)" thành "(4,4, 2,2)" và TikZ đọc
    thành bốn toạ độ - hình vẽ ra sai hoàn toàn.
    """
    s = "%.4f" % float(x)
    return s.rstrip("0").rstrip(".") or "0"


def _boi_canh(so_nhom=4):
    """Chọn ngẫu nhiên một bối cảnh thực tế và sinh mẫu khớp bối cảnh đó."""
    mo_ta, don_vi, dau, h = random.choice(BOI_CANH)
    v = _mau_ghep_nhom(so_nhom=so_nhom, h=h, dau=dau)
    if v is None:
        return None
    bien, tanso = v
    return mo_ta, don_vi, bien, tanso


def _cau_dan(mo_ta, don_vi, bien, tanso):
    r"""Câu dẫn chung: giới thiệu mẫu rồi mời đọc bảng."""
    return (r"Người ta khảo sát %s và ghi lại kết quả trong bảng tần số "
            r"ghép nhóm sau (đơn vị: %s)."
            % (mo_ta % sum(tanso), don_vi))


# =====================================================================
# BÀI 8. MẪU SỐ LIỆU GHÉP NHÓM
# =====================================================================

def L11_C3_B8_NB040_MC_A_01(socau, dang=1):
    r"""Nhận biết mẫu số liệu ghép nhóm: đọc nhóm, tần số, giá trị đại diện.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is None:
            continue
        gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, tanso in gt:
        i = random.randrange(len(tanso))
        c = (bien[i] + bien[i + 1]) / 2.0
        dung = r"$%s$" % _xx(c)
        nhieu = _ba_nhieu11(
            dung,
            [r"$%g$" % bien[i], r"$%g$" % bien[i + 1], r"$%d$" % tanso[i],
             r"$%g$" % (bien[i + 1] - bien[i])],
            buoc=lambda t: r"$%s$" % _xx(c + t))
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Giá trị đại diện của nhóm $\left[%g;\ %g\right)$ bằng bao nhiêu?"
                 % (bien[i], bien[i + 1]))
        giai = (r"Giá trị đại diện của một nhóm là \textbf{trung điểm} của "
                r"nửa khoảng ứng với nhóm đó:"
                "\\\\\n"
                r"$c = \dfrac{u_i + u_{i+1}}{2} = \dfrac{%g + %g}{2} = %s$."
                % (bien[i], bien[i + 1], _xx(c)) +
                "\\\\\n"
                r"Chú ý phân biệt: $%d$ là \textbf{tần số} của nhóm (số giá "
                r"trị thuộc nhóm), còn $%g$ và $%g$ là hai \textbf{đầu mút} "
                r"của nhóm." % (tanso[i], bien[i], bien[i + 1]))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_bang(bien, tanso), 0, dang)
    return cauTN


def L11_C3_B9_NB047_MC_A_01(socau, dang=1):
    r"""Đọc bảng ghép nhóm để trả lời một câu hỏi thực tiễn (liên môn).

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is None:
            continue
        gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, tanso in gt:
        i = random.randrange(1, len(tanso))
        tu = sum(tanso[i:])
        n = sum(tanso)
        dung = r"$%d$" % tu
        nhieu = _ba_nhieu11(
            dung,
            [r"$%d$" % tanso[i], r"$%d$" % (n - tu), r"$%d$" % sum(tanso[:i + 1]),
             r"$%d$" % n],
            buoc=lambda t: r"$%d$" % (tu + t))
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Có bao nhiêu giá trị trong mẫu lớn hơn hoặc bằng $%g$?"
                 % bien[i])
        giai = (r"Các giá trị lớn hơn hoặc bằng $%g$ nằm trong các nhóm kể "
                r"từ $\left[%g;\ %g\right)$ trở đi."
                % (bien[i], bien[i], bien[i + 1]) +
                "\\\\\n"
                r"Cộng tần số của các nhóm đó: $%s = %d$."
                % (" + ".join(str(t) for t in tanso[i:]), tu) +
                "\\\\\n"
                r"Đây chính là cách thống kê được dùng trong các môn học "
                r"khác: từ bảng tần số ghép nhóm, ta trả lời ngay được câu "
                r"hỏi \textit{có bao nhiêu đối tượng đạt ngưỡng cho trước}.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_bang(bien, tanso), 0, dang)
    return cauTN


# =====================================================================
# BÀI 9. CÁC SỐ ĐẶC TRƯNG ĐO XU THẾ TRUNG TÂM
# =====================================================================

def _giai_trung_binh(bien, tanso):
    c = _trung_diem(bien)
    n = sum(tanso)
    tong = sum(t * x for t, x in zip(tanso, c))
    return (r"Mỗi nhóm được thay bằng \textbf{giá trị đại diện} là trung "
            r"điểm của nhóm."
            "\\\\\n" + _dai_dien_mot_dong(bien, tanso) +
            "\\\\\n"
            r"Số trung bình của mẫu ghép nhóm:"
            "\\\\\n"
            r"$\bar{x} = \dfrac{n_1c_1 + n_2c_2 + \cdots + n_kc_k}{n} "
            r"= \dfrac{%s}{%d} = \dfrac{%s}{%d} = %s$."
            % (" + ".join(r"%d\cdot %s" % (t, _xx(x))
                          for t, x in zip(tanso, c)),
               n, _xx(tong), n, _xx(tong / n)))


def _giai_phan_vi(bien, tanso, k):
    n = sum(tanso)
    moc = k * n / 4.0
    i, truoc = _nhom_chua(tanso, moc)
    h = bien[i + 1] - bien[i]
    gt = _phan_vi(bien, tanso, k)
    ten = {1: "Q_1", 2: "M_e", 3: "Q_3"}[k]
    phan = {1: r"\dfrac{n}{4}", 2: r"\dfrac{n}{2}", 3: r"\dfrac{3n}{4}"}[k]
    tich_luy = []
    s = 0
    for t in tanso:
        s += t
        tich_luy.append(s)
    return (r"Cỡ mẫu $n = %d$. Tần số tích luỹ lần lượt là $%s$."
            % (n, "$; $".join(str(x) for x in tich_luy)) +
            "\\\\\n"
            r"Ta cần giá trị ở vị trí $%s = %s$. Vì $%s < %s \le %s$ nên "
            r"giá trị đó rơi vào nhóm $\left[%g;\ %g\right)$."
            % (phan, _xx(moc), _xx(truoc), _xx(moc), _xx(truoc + tanso[i]),
               bien[i], bien[i + 1]) +
            "\\\\\n"
            r"$%s = u_m + \dfrac{%s - C}{n_m}\left(u_{m+1} - u_m\right) "
            r"= %g + \dfrac{%s - %d}{%d}\cdot %g = %s$."
            % (ten, phan, bien[i], _xx(moc), truoc, tanso[i], h, _xx(gt)) +
            "\\\\\n"
            r"Trong đó $C = %d$ là tần số tích luỹ của các nhóm "
            r"\textbf{đứng trước} nhóm chứa $%s$." % (truoc, ten))


def _giai_mot(bien, tanso):
    i = tanso.index(max(tanso))
    truoc = tanso[i - 1] if i > 0 else 0
    sau = tanso[i + 1] if i < len(tanso) - 1 else 0
    h = bien[i + 1] - bien[i]
    mo = _mot(bien, tanso)
    return (r"Nhóm có tần số lớn nhất là $\left[%g;\ %g\right)$ với "
            r"$n_m = %d$; hai nhóm kề bên có $n_{m-1} = %d$ và "
            r"$n_{m+1} = %d$." % (bien[i], bien[i + 1], tanso[i], truoc, sau) +
            "\\\\\n"
            r"$M_o = u_m + \dfrac{n_m - n_{m-1}}"
            r"{\left(n_m - n_{m-1}\right) + \left(n_m - n_{m+1}\right)}"
            r"\left(u_{m+1} - u_m\right)$"
            "\\\\\n"
            r"$= %g + \dfrac{%d - %d}{\left(%d - %d\right) + "
            r"\left(%d - %d\right)}\cdot %g = %s$."
            % (bien[i], tanso[i], truoc, tanso[i], truoc, tanso[i], sau,
               h, _xx(mo)))


def L11_C3_B9_TH041_MC_A_01(socau, dang=1):
    r"""Số trung bình của mẫu số liệu ghép nhóm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, tanso in gt:
        tb = _so_trung_binh(bien, tanso)
        c = _trung_diem(bien)
        n = sum(tanso)
        dung = r"$%s$" % _xx(tb)
        # Nhieu: quen chia cho n, lay trung binh cac dau mut duoi,
        # lay trung binh cong cac gia tri dai dien (bo qua tan so).
        nhieu = _ba_nhieu11(
            dung,
            [r"$%s$" % _xx(sum(c) / len(c)),
             r"$%s$" % _xx(sum(t * bien[i] for i, t in enumerate(tanso)) / n),
             r"$%s$" % _xx(sum(t * bien[i + 1] for i, t in enumerate(tanso)) / n),
             r"$%s$" % _xx(tb + 1)],
            buoc=lambda t: r"$%s$" % _xx(tb + t + 1))
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Số trung bình của mẫu số liệu ghép nhóm trên bằng bao "
                 r"nhiêu (làm tròn đến hàng phần trăm)?")
        cauTN += MC_SA_answer_text(debai, dung, nhieu,
                                   _giai_trung_binh(bien, tanso),
                                   _hinh_bang(bien, tanso), 0, dang)
    return cauTN


def L11_C3_B9_TH041_SA_A_01(socau):
    r"""Số trung bình - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cau = ""
    for mo_ta, don_vi, bien, tanso in gt:
        tb = _so_trung_binh(bien, tanso)
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Tính số trung bình của mẫu số liệu ghép nhóm trên "
                 r"(làm tròn đến hàng phần trăm).")
        nhieu = _ba_nhieu11(_xx(tb), [_xx(tb + 1), _xx(tb - 1), _xx(tb + 2)],
                            buoc=lambda t: _xx(tb + t + 2))
        cau += MC_SA_answer_const(debai, _xx(tb), nhieu,
                                  _giai_trung_binh(bien, tanso),
                                  _hinh_bang(bien, tanso), 0, 2)
    return cau


def L11_C3_B9_TH042_MC_A_01(socau, dang=1):
    r"""Trung vị của mẫu số liệu ghép nhóm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, tanso in gt:
        me = _phan_vi(bien, tanso, 2)
        n = sum(tanso)
        i, truoc = _nhom_chua(tanso, n / 2.0)
        h = bien[i + 1] - bien[i]
        dung = r"$%s$" % _xx(me)
        nhieu = _ba_nhieu11(
            dung,
            # quen tru tan so tich luy; lay dau mut duoi; dung (n+1)/2
            [r"$%s$" % _xx(bien[i] + (n / 2.0) / tanso[i] * h),
             r"$%g$" % bien[i],
             r"$%s$" % _xx(bien[i] + ((n + 1) / 2.0 - truoc) / tanso[i] * h),
             r"$%s$" % _xx(_so_trung_binh(bien, tanso))],
            buoc=lambda t: r"$%s$" % _xx(me + t))
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Trung vị của mẫu số liệu ghép nhóm trên bằng bao nhiêu "
                 r"(làm tròn đến hàng phần trăm)?")
        cauTN += MC_SA_answer_text(debai, dung, nhieu,
                                   _giai_phan_vi(bien, tanso, 2),
                                   _hinh_bang(bien, tanso), 0, dang)
    return cauTN


def L11_C3_B9_TH042_SA_A_01(socau):
    r"""Trung vị - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cau = ""
    for mo_ta, don_vi, bien, tanso in gt:
        me = _phan_vi(bien, tanso, 2)
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Tính trung vị của mẫu số liệu ghép nhóm trên "
                 r"(làm tròn đến hàng phần trăm).")
        nhieu = _ba_nhieu11(_xx(me), [_xx(me + 1), _xx(me - 1), _xx(me + 2)],
                            buoc=lambda t: _xx(me + t + 2))
        cau += MC_SA_answer_const(debai, _xx(me), nhieu,
                                  _giai_phan_vi(bien, tanso, 2),
                                  _hinh_bang(bien, tanso), 0, 2)
    return cau


def L11_C3_B9_TH043_MC_A_01(socau, dang=1):
    r"""Tứ phân vị thứ nhất hoặc thứ ba của mẫu ghép nhóm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v + (random.choice([1, 3]),))

    cauTN = ""
    for mo_ta, don_vi, bien, tanso, k in gt:
        q = _phan_vi(bien, tanso, k)
        ten = "Q_1" if k == 1 else "Q_3"
        n = sum(tanso)
        i, truoc = _nhom_chua(tanso, k * n / 4.0)
        h = bien[i + 1] - bien[i]
        dung = r"$%s$" % _xx(q)
        nhieu = _ba_nhieu11(
            dung,
            [r"$%s$" % _xx(_phan_vi(bien, tanso, 2)),           # nham trung vi
             r"$%s$" % _xx(_phan_vi(bien, tanso, 4 - k)),        # nham Q kia
             r"$%s$" % _xx(bien[i] + (k * n / 4.0) / tanso[i] * h),  # quen tru C
             r"$%g$" % bien[i]],
            buoc=lambda t: r"$%s$" % _xx(q + t))
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Tứ phân vị thứ %s của mẫu số liệu ghép nhóm trên bằng "
                 r"bao nhiêu (làm tròn đến hàng phần trăm)?"
                 % ("nhất" if k == 1 else "ba"))
        giai = (_giai_phan_vi(bien, tanso, k) +
                "\\\\\n"
                r"Chú ý với mẫu ghép nhóm, $%s$ được tính bằng CÙNG một "
                r"công thức như trung vị, chỉ thay vị trí $\dfrac{n}{2}$ "
                r"bằng $%s$." % (ten, r"\dfrac{n}{4}" if k == 1
                                 else r"\dfrac{3n}{4}"))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_bang(bien, tanso), 0, dang)
    return cauTN


def L11_C3_B9_TH043_SA_A_01(socau):
    r"""Tứ phân vị - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v + (random.choice([1, 3]),))

    cau = ""
    for mo_ta, don_vi, bien, tanso, k in gt:
        q = _phan_vi(bien, tanso, k)
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Tính tứ phân vị thứ %s của mẫu số liệu ghép nhóm trên "
                 r"(làm tròn đến hàng phần trăm)."
                 % ("nhất" if k == 1 else "ba"))
        nhieu = _ba_nhieu11(_xx(q), [_xx(q + 1), _xx(q - 1), _xx(q + 2)],
                            buoc=lambda t: _xx(q + t + 2))
        cau += MC_SA_answer_const(debai, _xx(q), nhieu,
                                  _giai_phan_vi(bien, tanso, k),
                                  _hinh_bang(bien, tanso), 0, 2)
    return cau


def L11_C3_B9_TH044_MC_A_01(socau, dang=1):
    r"""Mốt của mẫu số liệu ghép nhóm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, tanso in gt:
        mo = _mot(bien, tanso)
        i = tanso.index(max(tanso))
        dung = r"$%s$" % _xx(mo)
        nhieu = _ba_nhieu11(
            dung,
            [r"$%d$" % max(tanso),                       # nham TAN SO lon nhat
             r"$%g$" % bien[i],                          # lay dau mut duoi
             r"$%s$" % _xx((bien[i] + bien[i + 1]) / 2.0),   # lay trung diem
             r"$%s$" % _xx(_so_trung_binh(bien, tanso))],
            buoc=lambda t: r"$%s$" % _xx(mo + t))
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Mốt của mẫu số liệu ghép nhóm trên bằng bao nhiêu "
                 r"(làm tròn đến hàng phần trăm)?")
        giai = (_giai_mot(bien, tanso) +
                "\\\\\n"
                r"Chú ý mốt là một GIÁ TRỊ nằm trong nhóm có tần số lớn "
                r"nhất, không phải chính tần số $%d$ ấy." % max(tanso))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai,
                                   _hinh_bang(bien, tanso), 0, dang)
    return cauTN


def L11_C3_B9_TH044_SA_A_01(socau):
    r"""Mốt - trả lời ngắn.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cau = ""
    for mo_ta, don_vi, bien, tanso in gt:
        mo = _mot(bien, tanso)
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso) +
                 "\\\\\n"
                 r"Tính mốt của mẫu số liệu ghép nhóm trên "
                 r"(làm tròn đến hàng phần trăm).")
        nhieu = _ba_nhieu11(_xx(mo), [_xx(mo + 1), _xx(mo - 1), _xx(mo + 2)],
                            buoc=lambda t: _xx(mo + t + 2))
        cau += MC_SA_answer_const(debai, _xx(mo), nhieu,
                                  _giai_mot(bien, tanso),
                                  _hinh_bang(bien, tanso), 0, 2)
    return cau


def L11_C3_B9_TH045_MC_A_01(socau, dang=1):
    r"""Ý nghĩa và vai trò của các số đặc trưng đo xu thế trung tâm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    Y_NGHIA = [
        ("Số trung bình",
         "dùng hết mọi giá trị của mẫu nên bị giá trị bất thường kéo lệch",
         "Số trung bình tính từ tất cả các giá trị đại diện, nên chỉ cần "
         "một nhóm ở xa có tần số đáng kể là nó bị kéo theo."),
        ("Trung vị",
         "chia mẫu thành hai nửa bằng nhau về số giá trị",
         "Trung vị là giá trị ở chính giữa khi sắp thứ tự, nên một nửa số "
         "giá trị nhỏ hơn nó và một nửa lớn hơn nó."),
        ("Mốt",
         "cho biết giá trị có nhiều số liệu tập trung quanh nó nhất",
         "Mốt được tính từ nhóm có tần số lớn nhất, nên nó chỉ ra chỗ số "
         "liệu dồn lại đông nhất."),
        ("Tứ phân vị thứ nhất",
         "có khoảng một phần tư số giá trị của mẫu nhỏ hơn nó",
         "Theo định nghĩa, $Q_1$ đứng ở vị trí $\\dfrac{n}{4}$ của mẫu đã "
         "sắp thứ tự."),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(Y_NGHIA))
        if i not in gt:
            gt.append(i)
        if len(gt) >= len(Y_NGHIA):
            break

    cauTN = ""
    for i in gt:
        ten, y, vi_sao = Y_NGHIA[i]
        dung = "%s %s." % (ten, y)
        nhieu = _ba_nhieu11(
            dung,
            ["%s %s." % (ten, Y_NGHIA[(i + 1) % len(Y_NGHIA)][1]),
             "%s %s." % (ten, Y_NGHIA[(i + 2) % len(Y_NGHIA)][1]),
             "%s %s." % (ten, Y_NGHIA[(i + 3) % len(Y_NGHIA)][1])],
            buoc=lambda t: "%s không phụ thuộc vào số liệu của mẫu." % ten)
        debai = (r"Khi phân tích một mẫu số liệu ghép nhóm, phát biểu nào "
                 r"sau đây về \textbf{%s} là đúng?" % ten.lower())
        giai = (r"%s" % vi_sao +
                "\\\\\n"
                r"Ba số đặc trưng đo xu thế trung tâm bổ sung cho nhau: số "
                r"trung bình cho mức chung, trung vị cho vị trí giữa và "
                r"không bị giá trị bất thường kéo lệch, còn mốt cho biết "
                r"chỗ số liệu tập trung đông nhất.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _dong_nhom(ten, bien, tanso):
    r"""Một dòng mô tả bảng ghép nhóm của một nhóm, viết bằng chữ.

    Câu so sánh HAI mẫu thì không dùng bảng TikZ: \immini chỉ có một ô
    hình, mà hai bảng cạnh nhau sẽ chật. Viết thành chữ thì hiện đúng ở
    cả PDF lẫn web, không cần ảnh.
    """
    return (r"Nhóm $%s$ (cỡ mẫu $%d$): " % (ten, sum(tanso)) +
            "; ".join(r"$\left[%g;\ %g\right)$ có $%d$ giá trị"
                      % (bien[i], bien[i + 1], tanso[i])
                      for i in range(len(tanso))) + ".")


def _mo_ta_chung(mo_ta):
    """Bỏ chỗ điền cỡ mẫu trong mô tả, dùng khi so sánh HAI nhóm có cỡ
    mẫu khác nhau (không thể ghi chung một con số)."""
    return mo_ta.replace("%d ", "")


def _giai_trung_binh_gon(ten, bien, tanso, tb):
    """Một dòng tính số trung bình của một nhóm."""
    return (r"Nhóm $%s$: $\bar{x}_%s = \dfrac{%s}{%d} = %s$."
            % (ten, ten,
               " + ".join(r"%d\cdot %s" % (t, _xx(x))
                          for t, x in zip(tanso, _trung_diem(bien))),
               sum(tanso), _xx(tb)))


def _cap_mau_so_sanh():
    r"""Hai mẫu ghép nhóm CÙNG bộ nhóm, số trung bình khác nhau rõ ràng."""
    for _ in range(300):
        v = _boi_canh()
        if v is None:
            continue
        mo_ta, don_vi, bien, tanso = v
        v2 = _mau_ghep_nhom(so_nhom=len(tanso), h=bien[1] - bien[0], dau=bien[0])
        if v2 is None:
            continue
        _, tanso2 = v2
        tb1 = _so_trung_binh(bien, tanso)
        tb2 = _so_trung_binh(bien, tanso2)
        # Chenh lech phai RO RANG de ket luan khong gay tranh cai
        if abs(tb1 - tb2) < (bien[1] - bien[0]) * 0.35:
            continue
        return mo_ta, don_vi, bien, tanso, tanso2, tb1, tb2
    return None


def L11_C3_B9_VD046_MC_A_01(socau, dang=1):
    r"""Rút ra kết luận nhờ ý nghĩa của các số đặc trưng.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _cap_mau_so_sanh()
        if v is not None:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, t1, t2, tb1, tb2 in gt:
        cao = "A" if tb1 > tb2 else "B"
        thap = "B" if cao == "A" else "A"
        dung = "Nhóm %s có số trung bình lớn hơn." % cao
        nhieu = _ba_nhieu11(
            dung,
            ["Nhóm %s có số trung bình lớn hơn." % thap,
             "Hai nhóm có số trung bình bằng nhau.",
             "Không so sánh được vì hai nhóm có cỡ mẫu khác nhau."],
            buoc=lambda k: "Không đủ dữ kiện để tính số trung bình.")
        debai = (r"Khảo sát %s ở hai nhóm $A$ và $B$ (đơn vị: %s), người ta "
                 r"thu được kết quả sau."
                 % (_mo_ta_chung(mo_ta), don_vi) +
                 "\\\\\n" + _dong_nhom("A", bien, t1) +
                 "\\\\\n" + _dong_nhom("B", bien, t2) +
                 "\\\\\n"
                 r"So sánh số trung bình của hai nhóm, kết luận nào đúng?")
        giai = (_giai_trung_binh_gon("A", bien, t1, tb1) +
                "\\\\\n" + _giai_trung_binh_gon("B", bien, t2, tb2) +
                "\\\\\n"
                r"Vì $%s %s %s$ nên nhóm $%s$ có số trung bình lớn hơn."
                % (_xx(tb1), ">" if tb1 > tb2 else "<", _xx(tb2), cao) +
                "\\\\\n"
                r"Chú ý hai nhóm có cỡ mẫu khác nhau vẫn so sánh được, vì số "
                r"trung bình đã chia cho cỡ mẫu của chính nhóm đó.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L11_C3_B9_VD046_TL_A_01(socau, dong=1):
    r"""Tự luận: so sánh hai mẫu ghép nhóm rồi kết luận.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _cap_mau_so_sanh()
        if v is not None:
            gt.append(v)

    cauTN = ""
    for mo_ta, don_vi, bien, t1, t2, tb1, tb2 in gt:
        me1 = _phan_vi(bien, t1, 2)
        cao = "A" if tb1 > tb2 else "B"
        debai = (r"Khảo sát %s ở hai nhóm $A$ và $B$ (đơn vị: %s), người ta "
                 r"thu được kết quả sau."
                 % (_mo_ta_chung(mo_ta), don_vi) +
                 "\\\\\n" + _dong_nhom("A", bien, t1) +
                 "\\\\\n" + _dong_nhom("B", bien, t2))

        hoi_a = r"Tính số trung bình của nhóm $A$ (làm tròn đến hàng phần trăm)."
        giai_a = (_dai_dien_mot_dong(bien, t1) +
                  "\\\\\n" + _giai_trung_binh_gon("A", bien, t1, tb1))

        hoi_b = r"Tính trung vị của nhóm $A$ (làm tròn đến hàng phần trăm)."
        giai_b = _giai_phan_vi(bien, t1, 2)

        hoi_c = (r"Nhóm nào có kết quả cao hơn? Giải thích dựa vào số trung "
                 r"bình của hai nhóm.")
        giai_c = (_giai_trung_binh_gon("B", bien, t2, tb2) +
                  "\\\\\n"
                  r"Vì $%s %s %s$ nên nhóm $%s$ có kết quả cao hơn."
                  % (_xx(tb1), ">" if tb1 > tb2 else "<", _xx(tb2), cao) +
                  "\\\\\n"
                  r"Số trung bình đã chia cho cỡ mẫu của từng nhóm nên dù hai "
                  r"nhóm có cỡ mẫu khác nhau vẫn so sánh được với nhau.")

        ds_abcd = [(hoi_a, r"\bar{x}_A = %s" % _xx(tb1), giai_a),
                   (hoi_b, r"M_e = %s" % _xx(me1), giai_b),
                   (hoi_c, r"\text{Nhóm } %s" % cao, giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# CÂU ĐÚNG/SAI CỦA CHƯƠNG 3
# Thang bậc: a) NB - b) TH - c) VD - d) VDC
# =====================================================================

def L11_C3_TF_A_01(socau, socot=1):
    r"""Đúng/Sai - đọc hiểu mẫu số liệu ghép nhóm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cauTF = ""
    for mo_ta, don_vi, bien, tanso in gt:
        n = sum(tanso)
        i = tanso.index(max(tanso))
        c_i = (bien[i] + bien[i + 1]) / 2.0
        tu_nhom2 = sum(tanso[1:])
        me = _phan_vi(bien, tanso, 2)
        j, truoc = _nhom_chua(tanso, n / 2.0)
        debai = (_cau_dan(mo_ta, don_vi, bien, tanso))

        ds_abcd = (
            # a) NB - đọc thẳng một số trên bảng
            [
                (r"{\True Cỡ mẫu của mẫu số liệu này bằng $%d$}" % n,
                 r"Đúng. Cỡ mẫu là tổng tần số của mọi nhóm: "
                 r"$%s = %d$." % (" + ".join(str(t) for t in tanso), n)),
                (r"{Cỡ mẫu của mẫu số liệu này bằng $%d$}" % len(tanso),
                 r"Sai. $%d$ là SỐ NHÓM, không phải cỡ mẫu. Cỡ mẫu là tổng "
                 r"tần số và bằng $%d$." % (len(tanso), n)),
            ],
            # b) TH - một phép tính trung điểm
            [
                (r"{\True Giá trị đại diện của nhóm $\left[%g;\ %g\right)$ "
                 r"bằng $%s$}" % (bien[i], bien[i + 1], _xx(c_i)),
                 r"Đúng. Giá trị đại diện là trung điểm của nhóm: "
                 r"$\dfrac{%g + %g}{2} = %s$."
                 % (bien[i], bien[i + 1], _xx(c_i))),
                (r"{Giá trị đại diện của nhóm $\left[%g;\ %g\right)$ bằng "
                 r"$%d$}" % (bien[i], bien[i + 1], tanso[i]),
                 r"Sai. $%d$ là TẦN SỐ của nhóm. Giá trị đại diện là trung "
                 r"điểm $%s$." % (tanso[i], _xx(c_i))),
            ],
            # c) VD - phải cộng dồn tần số nhiều nhóm
            [
                (r"{\True Có $%d$ giá trị trong mẫu lớn hơn hoặc bằng $%g$}"
                 % (tu_nhom2, bien[1]),
                 r"Đúng. Cộng tần số từ nhóm $\left[%g;\ %g\right)$ trở đi: "
                 r"$%s = %d$."
                 % (bien[1], bien[2], " + ".join(str(t) for t in tanso[1:]),
                    tu_nhom2)),
                (r"{Có $%d$ giá trị trong mẫu lớn hơn hoặc bằng $%g$}"
                 % (tanso[1], bien[1]),
                 r"Sai. $%d$ mới chỉ là tần số của RIÊNG nhóm "
                 r"$\left[%g;\ %g\right)$; còn các nhóm phía sau nữa."
                 % (tanso[1], bien[1], bien[2])),
            ],
            # d) VDC - phải xác định nhóm chứa trung vị rồi mới kết luận
            [
                (r"{\True Trung vị của mẫu thuộc nhóm "
                 r"$\left[%g;\ %g\right)$}" % (bien[j], bien[j + 1]),
                 r"Đúng. Trung vị ứng với vị trí $\dfrac{n}{2} = %s$."
                 % _xx(n / 2.0) +
                 "\\\\\n"
                 r"Tần số tích luỹ đến hết nhóm trước là $%d$, đến hết nhóm "
                 r"$\left[%g;\ %g\right)$ là $%d$; vì $%d < %s \le %d$ nên "
                 r"trung vị rơi vào nhóm ấy."
                 % (truoc, bien[j], bien[j + 1], truoc + tanso[j],
                    truoc, _xx(n / 2.0), truoc + tanso[j]) +
                 "\\\\\n"
                 r"Tính ra $M_e = %s$." % _xx(me)),
                (r"{Trung vị của mẫu bằng trung điểm của nhóm "
                 r"$\left[%g;\ %g\right)$}" % (bien[j], bien[j + 1]),
                 r"Sai. Trung vị NẰM TRONG nhóm đó nhưng không phải trung "
                 r"điểm: phải nội suy theo tần số tích luỹ, ra "
                 r"$M_e = %s$ (trung điểm là $%s$)."
                 % (_xx(me), _xx((bien[j] + bien[j + 1]) / 2.0))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, _hinh_bang(bien, tanso), 0, socot)
    return cauTF


def L11_C3_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - các số đặc trưng đo xu thế trung tâm.

    CLAUDE THEM 29/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    gt = []
    while len(gt) < socau:
        v = _boi_canh()
        if v is not None:
            gt.append(v)

    cauTF = ""
    for mo_ta, don_vi, bien, tanso in gt:
        n = sum(tanso)
        tb = _so_trung_binh(bien, tanso)
        me = _phan_vi(bien, tanso, 2)
        q1 = _phan_vi(bien, tanso, 1)
        q3 = _phan_vi(bien, tanso, 3)
        mo = _mot(bien, tanso)
        i = tanso.index(max(tanso))
        debai = _cau_dan(mo_ta, don_vi, bien, tanso)

        ds_abcd = (
            # a) NB - nhận ra nhóm chứa mốt
            [
                (r"{\True Mốt của mẫu thuộc nhóm $\left[%g;\ %g\right)$}"
                 % (bien[i], bien[i + 1]),
                 r"Đúng. Mốt luôn nằm trong nhóm có tần số lớn nhất, ở đây "
                 r"là nhóm $\left[%g;\ %g\right)$ với tần số $%d$."
                 % (bien[i], bien[i + 1], tanso[i])),
                (r"{Mốt của mẫu bằng $%d$}" % tanso[i],
                 r"Sai. $%d$ là TẦN SỐ lớn nhất, còn mốt là một giá trị "
                 r"nằm trong nhóm ấy; tính ra $M_o = %s$."
                 % (tanso[i], _xx(mo))),
            ],
            # b) TH - một lần dùng công thức số trung bình
            [
                (r"{\True Số trung bình của mẫu bằng $%s$}" % _xx(tb),
                 r"Đúng. Thay mỗi nhóm bằng giá trị đại diện rồi tính:"
                 "\\\\\n"
                 r"$\bar{x} = \dfrac{%s}{%d} = %s$."
                 % (" + ".join(r"%d\cdot %s" % (t, _xx(x))
                               for t, x in zip(tanso, _trung_diem(bien))),
                    n, _xx(tb))),
                (r"{Số trung bình của mẫu bằng $%s$}"
                 % _xx(sum(_trung_diem(bien)) / len(tanso)),
                 r"Sai. Đó là trung bình cộng của các giá trị đại diện, "
                 r"BỎ QUÊN tần số. Phải nhân mỗi giá trị đại diện với tần "
                 r"số của nó, kết quả là $%s$." % _xx(tb)),
            ],
            # c) VD - hai tứ phân vị, phải làm hai lần công thức
            [
                (r"{\True Khoảng tứ phân vị của mẫu bằng $%s$}"
                 % _xx(q3 - q1),
                 r"Đúng. $Q_1 = %s$ và $Q_3 = %s$ nên "
                 r"$\Delta_Q = Q_3 - Q_1 = %s - %s = %s$."
                 % (_xx(q1), _xx(q3), _xx(q3), _xx(q1), _xx(q3 - q1))),
                (r"{Khoảng tứ phân vị của mẫu bằng $%s$}" % _xx(q3 + q1),
                 r"Sai. Khoảng tứ phân vị là HIỆU $Q_3 - Q_1 = %s$, không "
                 r"phải tổng." % _xx(q3 - q1)),
            ],
            # d) VDC - phải so sánh hai số đặc trưng rồi rút ra ý nghĩa
            [
                (r"{\True Trong mẫu này có ít nhất một nửa số giá trị không "
                 r"vượt quá $%s$}" % _xx(me),
                 r"Đúng. Theo đúng ý nghĩa của trung vị: $M_e = %s$ chia "
                 r"mẫu thành hai nửa bằng nhau về SỐ GIÁ TRỊ, nên có ít "
                 r"nhất một nửa số giá trị nhỏ hơn hoặc bằng $M_e$."
                 % _xx(me) +
                 "\\\\\n"
                 r"Chú ý điều này KHÔNG đúng với số trung bình: "
                 r"$\bar{x} = %s$ chỉ cho biết mức chung, không nói gì về "
                 r"việc có bao nhiêu giá trị nằm dưới nó." % _xx(tb)),
                (r"{Trong mẫu này có ít nhất một nửa số giá trị không vượt "
                 r"quá $%s$}" % _xx(tb),
                 r"Sai. Tính chất \textit{chia đôi số giá trị} là của "
                 r"TRUNG VỊ ($M_e = %s$), không phải của số trung bình "
                 r"($\bar{x} = %s$)." % (_xx(me), _xx(tb))),
            ])
        cauTF += TF_baitoan_du(debai, ds_abcd, _hinh_bang(bien, tanso), 0, socot)
    return cauTF
