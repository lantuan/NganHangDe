# -*- coding: utf-8 -*-
r"""LƯU TRỮ - các dạng đã rút khỏi ngân hàng đề (KHÔNG ra đề, web và bộ ráp đề không đọc thư mục data/luu_tru/).

Rút ngày 20/10/2026 theo yêu cầu cô Lan: bài "đo bán kính Trái Đất bằng góc hạ tới đường chân trời" CHỈ dùng tam giác
vuông (OT vuông góc MT), không dùng hệ thức lượng trong tam giác thường (định lí côsin, định lí sin) nên không khớp
YCCĐ "Vận dụng được các hệ thức lượng trong tam giác". Cô xem lại sau để sửa thành dạng dùng được.

Gồm 5 dạng (cùng Dang "Đo bán kính Trái Đất bằng góc hạ tới đường chân trời"):
    L10_C3_B6_VD036_TL_E_01   tự luận: chứng minh tam giác OTM vuông, lập hệ thức, tính R
    L10_C3_B6_VD036_MC_K_01   (VD) biết R, h: tính góc hạ theta
    L10_C3_B6_VD036_SA_K_01   (VD) biết R, h: tính khoảng cách MT tới đường chân trời
    L10_C3_B6_VD036_MC_L_01   (VDC) biết h, theta: chọn công thức tính R
    L10_C3_B6_VD036_SA_L_01   (VDC) biết h, theta: tính R
Năm dòng Mapping cũ nằm ở data/luu_tru/L10_C3_mapping_luu_tru.json; 24 mục từ điển tiếng Anh ở
data/luu_tru/en_L10_C3_luu_tru.json.

Xem thử (đứng ở thư mục gốc dự án):  python3 data/luu_tru/L10_C3_luu_tru.py
Đưa trở lại ngân hàng: chép các hàm (và hàm phụ) về data/python_bank/toan10/L10_C3.py, chép các dòng Mapping về
data/mapping/toan10/L10_C3.json, chép các mục từ điển về data/i18n/bank/en_L10_C3.json, chạy lại
"python3 scripts/dich_ngan_hang.py dich data/python_bank/toan10/L10_C3.py" (bản tiếng Anh) và toàn bộ test.
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python_bank"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python_bank" / "toan10"))
from math_type import *  # noqa: E402,F401,F403
from L10_C3 import _ba_nhieu, _lt  # noqa: E402  (hàm phụ dùng chung, vẫn còn trong L10_C3.py)


# hàm phụ chép từ L10_C3.py
DAU_THAP_PHAN = ","


def _xx(x, n=2):
    """Làm tròn n chữ số thập phân rồi viết thành chuỗi (bỏ đuôi 0 thừa)."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", DAU_THAP_PHAN)


def _hinh_trai_dat():
    """Hình minh hoạ (KHÔNG đúng tỉ lệ - góc hạ thật chỉ khoảng 1-2 độ): Trái Đất tâm O, núi
    tại M, tia nhìn MT tiếp xúc mặt biển tại T, góc hạ theta so với phương nằm ngang tại M
    (cô Lan 01/10/2026: không có hình học sinh rất khó làm bài)."""
    R, h = 2.0, 0.7
    goc_T = math.degrees(math.acos(R / (R + h)))      # góc TOM
    Tx, Ty = R * math.sin(math.radians(goc_T)), R * math.cos(math.radians(goc_T))
    return (
        "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
        "\\fill[blue!8] (0,0) circle (%.2f);\n\\draw[thick] (0,0) circle (%.2f);\n" % (R, R)
        + "\\fill[brown!60] (-0.25,%.2f) -- (0,%.2f) -- (0.25,%.2f) -- cycle;\n" % (R - 0.02, R + h, R - 0.02)
        + "\\draw[dashed] (0,0) -- (0,%.2f);\n" % (R + h)
        + "\\draw (0,0) -- (%.3f,%.3f);\n" % (Tx, Ty)
        + "\\draw[thick,red] (0,%.2f) -- (%.3f,%.3f);\n" % (
            R + h, Tx + 0.35 * Tx / math.hypot(Tx, R + h - Ty), Ty - 0.35 * (R + h - Ty) / math.hypot(Tx, R + h - Ty))
        + "\\draw[dashed] (-1.2,%.2f) -- (2.4,%.2f);\n" % (R + h, R + h)
        + "\\draw (0.9,%.2f) arc (0:%.1f:0.9);\n" % (R + h, -(90 - goc_T))
        + "\\node at (%.2f,%.2f) {$\\theta$};\n" % (1.15, R + h - 0.25)
        + "\\fill (0,0) circle (0.03) node[below] {$O$};\n"
        "\\fill (0,%.2f) circle (0.03) node[above] {$M$};\n" % (R + h)
        + "\\fill (%.3f,%.3f) circle (0.03) node[right] {$T$};\n" % (Tx, Ty)
        + "\\node[left] at (0,%.2f) {$h$};\n" % (R + h / 2)
        + "\\node[left] at (0,%.2f) {$R$};\n" % (R / 2)
        + "\\node[below right] at (%.3f,%.3f) {$R$};\n" % (Tx / 2, Ty / 2)
        + "\\end{tikzpicture}"
    )


def L10_C3_B6_VD036_TL_E_01(socau, dong=1):
    r"""Đo bán kính Trái Đất bằng góc hạ tới đường chân trời.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    CHÚ Ý VỀ PHƯƠNG PHÁP (cô Lan dặn: không dùng kiến thức lớp 11).
    Cách đo bán kính Trái Đất quen thuộc nhất - cách của Eratosthenes -
    dùng ĐỘ DÀI CUNG TRÒN $\ell = R\alpha$ với $\alpha$ tính bằng radian.
    Đó là chương trình LỚP 11 nên KHÔNG dùng ở đây.

    Cách dùng trong dạng này chỉ cần tam giác vuông: từ đỉnh núi $M$ cao
    $h$, tia nhìn tới đường chân trời tiếp xúc mặt đất tại $T$ nên
    $OT \perp MT$. Tam giác $OTM$ vuông tại $T$, gọi $\theta$ là góc hạ
    của tia nhìn so với phương nằm ngang thì $\widehat{OMT} =
    90^{\circ} - \theta$, do đó $\cos\theta = \dfrac{R}{R+h}$ và
    $R = \dfrac{h\cos\theta}{1 - \cos\theta}$.

    VÌ SAO LÀ TỰ LUẬN CHỨ KHÔNG PHẢI TRẮC NGHIỆM: vì $\cos\theta$ rất
    gần $1$ nên $\dfrac{h\cos\theta}{1-\cos\theta}$ và $\dfrac{h}{1-\cos\theta}$
    cho kết quả lệch nhau chưa tới $1\,\text{km}$ - phương án nhiễu
    "quên nhân $\cos\theta$" hoá ra CŨNG ĐÚNG, câu hỏi có hai đáp án.
    Mọi biến thể sai khác thì lại lệch hẳn về cỡ $h$, nhìn là loại được
    ngay. Nói cách khác bài này không có bộ phương án nhiễu tử tế. Để tự
    luận thì học sinh phải lập được hệ thức, đúng chỗ cần đánh giá.
    """
    NUI = [("Phan Xi Păng", 3.1), ("Ngọc Linh", 2.6), ("Bà Đen", 1.0),
           ("Tây Côn Lĩnh", 2.4), ("Pu Ta Leng", 3.0)]

    gt = []
    thu = 0
    while len(gt) < socau and thu < 200:
        thu += 1
        i = random.randrange(len(NUI))
        # chọn theta từ bán kính thật 6371 km rồi làm tròn hai chữ số,
        # để số liệu đề bài là con số đo được hợp lí
        h = NUI[i][1]
        theta = round(math.degrees(math.acos(6371.0 / (6371.0 + h))), 2)
        if (i, theta) not in gt:
            gt.append((i, theta))

    cauTN = ''
    for i, theta in gt:
        ten, h = NUI[i]
        c = math.cos(math.radians(theta))
        R = h * c / (1 - c)

        debai = (r"Đứng trên đỉnh núi %s ở độ cao $h = %s\,\text{km}$ so với "
                 r"mực nước biển, một người nhìn về phía biển thì thấy đường "
                 r"chân trời. Tia nhìn tới đường chân trời tạo với phương nằm "
                 r"ngang một góc hạ $\theta = %s^{\circ}$. Coi Trái Đất là "
                 r"khối cầu tâm $O$ bán kính $R$; gọi $M$ là vị trí người quan "
                 r"sát và $T$ là điểm mà tia nhìn chạm mặt biển (hình vẽ minh hoạ, "
                 r"không đúng tỉ lệ)."
                 % (ten, _xx(h, 1), _xx(theta, 2)))

        hoi_a = (r"Chứng tỏ tam giác $OTM$ vuông tại $T$ và tính "
                 r"$\widehat{OMT}$ theo $\theta$.")
        giai_a = (r"Tia nhìn chạm mặt biển ở đúng đường chân trời nên $MT$ "
                  r"là tiếp tuyến của đường tròn tâm $O$ tại $T$, do đó "
                  r"$OT \perp MT$: tam giác $OTM$ vuông tại $T$."
                  "\\\\\n"
                  r"Phương nằm ngang tại $M$ vuông góc với bán kính $OM$. "
                  r"Tia nhìn $MT$ hạ xuống dưới phương ấy một góc $\theta$, "
                  r"nên góc giữa $MT$ và $MO$ là"
                  "\\\\\n"
                  r"$\widehat{OMT} = 90^{\circ} - \theta = %s^{\circ}$."
                  % _xx(90 - theta, 2))

        hoi_b = r"Chứng minh rằng $\cos\theta = \dfrac{R}{R + h}$."
        giai_b = (r"Tam giác $OTM$ vuông tại $T$ có $OT = R$ là cạnh đối diện "
                  r"góc $\widehat{OMT}$ và $OM = R + h$ là cạnh huyền, nên"
                  "\\\\\n"
                  r"$\sin\widehat{OMT} = \dfrac{OT}{OM} = \dfrac{R}{R + h}$."
                  "\\\\\n"
                  r"Mà $\widehat{OMT} = 90^{\circ} - \theta$ và hai góc phụ "
                  r"nhau có sin góc này bằng côsin góc kia, nên "
                  r"$\sin\left(90^{\circ} - \theta\right) = \cos\theta$."
                  "\\\\\n"
                  r"Vậy $\cos\theta = \dfrac{R}{R + h}$.")

        hoi_c = (r"Từ đó tính bán kính $R$ của Trái Đất (làm tròn đến hàng "
                 r"đơn vị, tính theo ki-lô-mét).")
        giai_c = (r"Từ $\cos\theta = \dfrac{R}{R+h}$ suy ra "
                  r"$\left(R + h\right)\cos\theta = R$, tức là"
                  "\\\\\n"
                  r"$R\left(1 - \cos\theta\right) = h\cos\theta "
                  r"\Rightarrow R = \dfrac{h\cos\theta}{1 - \cos\theta}$."
                  "\\\\\n"
                  r"Thay số $h = %s\,\text{km}$ và $\theta = %s^{\circ}$:"
                  "\\\\\n"
                  r"$R = \dfrac{%s\cdot\cos %s^{\circ}}{1 - \cos %s^{\circ}} "
                  r"\approx %s\,\text{(km)}$."
                  "\\\\\n"
                  r"Kết quả này sát với bán kính Trái Đất thường dùng là "
                  r"$6371\,\text{km}$. Lưu ý $1 - \cos\theta$ là một số rất "
                  r"bé, nên khi bấm máy phải giữ đủ chữ số thập phân, làm "
                  r"tròn sớm sẽ ra kết quả lệch nhiều."
                  % (_xx(h, 1), _xx(theta, 2), _xx(h, 1),
                     _xx(theta, 2), _xx(theta, 2), _xx(R, 0)))

        ds_abcd = [(hoi_a, r"90^{\circ} - \theta", giai_a),
                   (hoi_b, r"\cos\theta = \dfrac{R}{R + h}", giai_b),
                   (hoi_c, r"R \approx %s\,\text{km}" % _xx(R, 0), giai_c)]
        cauTN += TL_answer_text(debai, ds_abcd, _hinh_trai_dat(), 0, dong)
    return cauTN


# ---- Bán kính Trái Đất / đường chân trời: MC + SA tách VD và VDC ----
# CLAUDE THEM 01/10/2026 - co Lan duyet cach hoi (VD: cho R, tinh goc ha / khoang cach
# toi chan troi; VDC: cho h va goc ha, tinh R). Cung mo ta "Dang" voi TL_E de khong ra
# chung mot de. Do cao lay xap xi so lieu thuc te (km).
_NUI_CHAN_TROI = [("Phan Xi Păng", 3.14), ("Pu Si Lung", 3.08), ("Pu Ta Leng", 3.05),
                  ("Ngọc Linh", 2.6), ("Chư Yang Sin", 2.44), ("Tây Côn Lĩnh", 2.42),
                  ("Lang Biang", 2.17), ("Mẫu Sơn", 1.54), ("Bạch Mã", 1.45), ("Bà Đen", 0.99)]
_R_TRAI_DAT = 6371


def _chon_nui(socau):
    """Chọn socau ngọn núi, không lặp khi còn đủ núi."""
    ds = random.sample(range(len(_NUI_CHAN_TROI)), min(socau, len(_NUI_CHAN_TROI)))
    while len(ds) < socau:
        ds.append(random.randrange(len(_NUI_CHAN_TROI)))
    return [_NUI_CHAN_TROI[i] for i in ds]


def _mo_dau_chan_troi(ten, h):
    return (r"Đứng trên đỉnh núi %s ở độ cao $h = %s\,\text{km}$ so với mực nước biển, một người "
            r"nhìn về phía biển thì thấy đường chân trời. Coi Trái Đất là khối cầu tâm $O$ bán kính "
            r"$R$; gọi $M$ là vị trí người quan sát và $T$ là điểm mà tia nhìn chạm mặt biển, "
            r"$\theta$ là góc hạ của tia nhìn $MT$ so với phương nằm ngang (hình vẽ minh hoạ, "
            r"không đúng tỉ lệ)." % (ten, _xx(h, 2)))


_GIAI_VUONG_T = (r"Tia nhìn chạm mặt biển ở đúng đường chân trời nên $MT$ là tiếp tuyến của "
                 r"đường tròn tâm $O$ tại $T$, do đó tam giác $OTM$ vuông tại $T$, có "
                 r"$OT = R$, $OM = R + h$.")


def L10_C3_B6_VD036_MC_K_01(socau, dang=1):
    r"""Đường chân trời (mức VD): biết $R = 6371\,\text{km}$ và độ cao $h$, tính góc hạ $\theta$.

    Phương nằm ngang tại $M$ vuông góc với $OM$ nên $\widehat{OMT} = 90^{\circ} - \theta$,
    suy ra $\widehat{TOM} = \theta$ và $\cos\theta = \dfrac{R}{R + h}$.
    Nhiễu: $90^{\circ} - \theta$ (nhầm với $\widehat{OMT}$), $\tan\theta = \dfrac{h}{R}$,
    $\cos\theta = \dfrac{h}{R + h}$.

    CLAUDE THEM 01/10/2026 - co Lan duyet lai.
    """
    R = _R_TRAI_DAT
    cau = ""
    for ten, h in _chon_nui(socau):
        t = math.degrees(math.acos(R / (R + h)))
        dap = _xx(t, 2) + r"^{\circ}"
        ung = [_xx(90 - t, 2) + r"^{\circ}",
               _xx(math.degrees(math.atan(h / R)), 2) + r"^{\circ}",
               _xx(math.degrees(math.acos(h / (R + h))), 2) + r"^{\circ}"]
        nhieu = _ba_nhieu(dap, ung, buoc=lambda k: _xx(t + 0.1 * k, 2) + r"^{\circ}")
        debai = (_mo_dau_chan_troi(ten, h) + r" Biết $R = %d\,\text{km}$. Góc hạ $\theta$ (làm "
                 r"tròn đến hàng phần trăm của độ) bằng" % R)
        giai = (_GIAI_VUONG_T + "\\\\\n"
                r"Phương nằm ngang tại $M$ vuông góc với $OM$ nên "
                r"$\widehat{OMT} = 90^{\circ} - \theta$, suy ra "
                r"$\widehat{TOM} = 90^{\circ} - \widehat{OMT} = \theta$."
                "\\\\\n"
                r"Do đó $\cos\theta = \dfrac{OT}{OM} = \dfrac{R}{R + h} = \dfrac{%d}{%s}"
                r"\Rightarrow \theta \approx %s$." % (R, _xx(R + h, 2), dap))
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_K_01(socau, dang=2):
    r"""Đường chân trời (mức VD): biết $R = 6371\,\text{km}$ và $h$, tính khoảng cách $MT$
    từ người quan sát tới đường chân trời (định lí Pythagore trong tam giác $OTM$ vuông tại $T$).

    CLAUDE THEM 01/10/2026 - co Lan duyet lai.
    """
    R = _R_TRAI_DAT
    cau = ""
    for ten, h in _chon_nui(socau):
        MT = math.sqrt((R + h) ** 2 - R ** 2)
        dap = str(_lt(MT))
        debai = (_mo_dau_chan_troi(ten, h) + r" Biết $R = %d\,\text{km}$. Tính khoảng cách $MT$ "
                 r"từ người quan sát tới đường chân trời (đơn vị km, làm tròn đến hàng đơn vị)." % R)
        giai = (_GIAI_VUONG_T + "\\\\\n"
                r"Theo định lí Pythagore: $MT = \sqrt{OM^{2} - OT^{2}} = "
                r"\sqrt{%s^{2} - %d^{2}} \approx %s\,\text{(km)}$." % (_xx(R + h, 2), R, dap))
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)], giai,
                                  _hinh_trai_dat(), 0, dang)
    return cau


# Công thức đúng và các công thức nhiễu cho dạng VDC tìm R theo h, theta
_CT_R_DUNG = r"R = \dfrac{h\cos\theta}{1 - \cos\theta}"
_CT_R_NHIEU = [r"R = \dfrac{h}{1 - \cos\theta}",
               r"R = \dfrac{h\sin\theta}{1 - \sin\theta}",
               r"R = \dfrac{h\left(1 - \cos\theta\right)}{\cos\theta}",
               r"R = \dfrac{h\cos\theta}{1 + \cos\theta}"]


def _giai_tim_R(h=None, theta=None, R=None):
    """Lời giải lập công thức R theo h, theta (VDC); có số thì thay số ở cuối."""
    s = (_GIAI_VUONG_T + "\\\\\n"
         r"Phương nằm ngang tại $M$ vuông góc với $OM$ nên $\widehat{OMT} = 90^{\circ} - \theta$, "
         r"suy ra $\widehat{TOM} = \theta$."
         "\\\\\n"
         r"Do đó $\cos\theta = \dfrac{OT}{OM} = \dfrac{R}{R + h} \Rightarrow "
         r"\left(R + h\right)\cos\theta = R \Rightarrow R\left(1 - \cos\theta\right) = h\cos\theta$,"
         "\\\\\n"
         r"tức là $" + _CT_R_DUNG + r"$.")
    if R is not None:
        s += ("\\\\\n"
              r"Thay số: $R = \dfrac{%s\cdot\cos %s^{\circ}}{1 - \cos %s^{\circ}} \approx %s\,\text{(km)}$. "
              r"Vì $1 - \cos\theta$ rất bé nên khi bấm máy phải giữ đủ chữ số, không làm tròn sớm."
              % (_xx(h, 2), _xx(theta, 2), _xx(theta, 2), _xx(R, 0)))
    return s


def L10_C3_B6_VD036_MC_L_01(socau, dang=1):
    r"""Đường chân trời (mức VDC): biết $h$ và góc hạ $\theta$, chọn công thức tính bán kính $R$.

    Không hỏi ra số vì nhiễu "quên nhân $\cos\theta$" chỉ lệch khoảng $h$ (2-3 km) so với
    đáp số, dễ gây tranh cãi; hỏi công thức thì các phương án tách bạch.

    CLAUDE THEM 01/10/2026 - co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for ten, h in _chon_nui(socau):
        theta = round(math.degrees(math.acos(_R_TRAI_DAT / (_R_TRAI_DAT + h))), 2)
        debai = (_mo_dau_chan_troi(ten, h) + r" Người đó đo được $\theta = %s^{\circ}$. Bán kính "
                 r"$R$ của Trái Đất được tính theo $h$ và $\theta$ bởi công thức nào sau đây?"
                 % _xx(theta, 2))
        nhieu = random.sample(_CT_R_NHIEU, 3)
        cau += MC_SA_answer_const(debai, _CT_R_DUNG, nhieu, _giai_tim_R(), _hinh_trai_dat(), 0, dang)
    return cau


def L10_C3_B6_VD036_SA_L_01(socau, dang=2):
    r"""Đường chân trời (mức VDC): biết $h$ và góc hạ $\theta$, tính bán kính $R$ của Trái Đất.

    $\theta$ được tính từ bán kính thật $6371\,\text{km}$ rồi làm tròn hai chữ số thập phân
    (số đo hợp lí); đáp số làm tròn đến hàng đơn vị (4 chữ số).

    CLAUDE THEM 01/10/2026 - co Lan duyet lai (muc_do_dang VDC).
    """
    cau = ""
    for ten, h in _chon_nui(socau):
        theta = round(math.degrees(math.acos(_R_TRAI_DAT / (_R_TRAI_DAT + h))), 2)
        c = math.cos(math.radians(theta))
        R = h * c / (1 - c)
        dap = str(_lt(R))
        debai = (_mo_dau_chan_troi(ten, h) + r" Người đó đo được $\theta = %s^{\circ}$. Tính bán "
                 r"kính $R$ của Trái Đất (đơn vị km, làm tròn đến hàng đơn vị)." % _xx(theta, 2))
        cau += MC_SA_answer_const(debai, dap, [str(int(dap) + k) for k in (1, -1, 2)],
                                  _giai_tim_R(h, theta, R), _hinh_trai_dat(), 0, dang)
    return cau


if __name__ == "__main__":
    random.seed(1)
    for ten in ("L10_C3_B6_VD036_TL_E_01", "L10_C3_B6_VD036_MC_K_01", "L10_C3_B6_VD036_SA_K_01",
                "L10_C3_B6_VD036_MC_L_01", "L10_C3_B6_VD036_SA_L_01"):
        print("%% ====", ten)
        print(globals()[ten](1))
