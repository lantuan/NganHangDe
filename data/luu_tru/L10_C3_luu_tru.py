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

Rút ngày 21/10/2026 theo yêu cầu cô Lan ("bài thơ Đồng chí tôi thấy không hay, chuyển vào nháp, sau này tôi chỉnh lí
lấy lại sau"): dạng "Vầng trăng của người lính" (bối cảnh trang_dong_chi), 6 hàm, 3 ID:
    L10_C3_B6_VD036_MC_W_01, _02  /  L10_C3_B6_VD036_SA_W_01, _02  /  L10_C3_B6_VD036_TL_O_01, _02
    (_01 đường kính Mặt Trăng - tam giác cân; _02 cây cổ thụ trên sườn đồi - định lí sin)
Ba dòng Mapping và 19 mục từ điển tiếng Anh cũng nằm ở hai tệp JSON trên. Test độc lập của dạng:
data/luu_tru/kiem_L10_C3_trang_dong_chi.py (chạy riêng bằng pytest). Khi đưa lại: thêm lại ba ID vào
CHO_PHEP_NHIEU_HAM trong tests/test_mot_id_mot_dang.py (một ID có hai hàm _01, _02).

Rút ngày 22/10/2026 theo yêu cầu cô Lan (câu "Biết ba cạnh a, b, c thì S = 1/2 ab sinC" bị chấm sai): "câu này vô lý,
cho tam giác ABC thì góc C đã biết, câu hỏi không rõ ràng. Bỏ chỗ biết đi, từ câu dẫn hỏi công thức đúng sai luôn".
Hỏi thẳng công thức đúng/sai chính là NB034_MC_A / NB034_SA_A nên cô chọn bỏ cả dạng B ("chọn công thức phù hợp với
dữ kiện"), 2 hàm:
    L10_C3_B6_NB034_MC_B_01   chọn công thức diện tích "phù hợp với dữ kiện" (bốn phương án đều là công thức đúng)
    L10_C3_B6_NB034_SA_B_01   đếm khẳng định "Biết <dữ kiện> thì S = ..." (kèm _C3S_DU_KIEN, _C3S_CT_S, _c3s_ct_dung)
Hai dòng Mapping và các mục từ điển tiếng Anh ở hai tệp JSON trên. Test cũ của SA_B (test_nb034_sa_b_cong_thuc_va_du_kien
trong tests/test_l10_c3_sa_bo_sung.py) xem trong lịch sử git.

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
from L10_C3 import _ba_nhieu, _c3s_dem, _c3s_dung, _lt, _so, _x1, _xa_bien  # noqa: E402  (hàm phụ dùng chung, vẫn còn trong L10_C3.py)


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


# Rút ngày 21/10/2026 - cô Lan: "bài thơ Đồng chí tôi thấy không hay, chuyển vào nháp, sau này tôi chỉnh lí lấy lại sau".
# =====================================================================================================
# "ĐỒNG CHÍ" (CHÍNH HỮU) - VẦNG TRĂNG CỦA NGƯỜI LÍNH CỤ HỒ (cô Lan 13/10/2026; thay hai bài Cảnh khuya, Rằm tháng Giêng)
# MỘT DẠNG MỚI (các ID MC_W, SA_Y, TL_O của bài 6, các chữ cái đã gỡ khỏi Pác Bó), HAI BIẾN THỂ:
#   _01: tính ĐƯỜNG KÍNH MẶT TRĂNG từ khoảng cách Trái Đất - Mặt Trăng và góc nhìn (tam giác cân, nửa góc, sin)
#   _02: tính CHIỀU CAO CÂY CỔ THỤ từ bóng trăng đổ trên sườn đồi dốc (định lí sin, số đo GIẢ SỬ)
# Số liệu thật (đã kiểm chứng, nguồn: bảng số liệu Mặt Trăng của NASA qua sites.uni.edu và space.fm): khoảng cách trung bình Trái Đất -
# Mặt Trăng 384 400 km, cận điểm 363 300 km, viễn điểm 405 500 km, đường kính Mặt Trăng khoảng 3 474 - 3 476 km. Góc nhìn trong đề được
# TÍNH từ các số liệu đó (2.asin(đường kính/2d), làm tròn 0,01 độ) nên đúng thực tế; đề KHÔNG nêu đường kính thật (đó là đáp số).
# Phần dẫn chỉ nêu điều đã kiểm chứng (hoatieu.vn, luatminhkhue.vn): bài thơ Đồng chí của Chính Hữu viết đầu năm 1948, sau chiến dịch
# Việt Bắc thu đông 1947, ca ngợi tình đồng đội của người lính kháng chiến chống Pháp; ý "chiến tranh khốc liệt mà người lính vẫn yêu đời,
# yêu thiên nhiên" theo yêu cầu cô Lan. KHÔNG chép lời thơ (cô Lan bỏ phần thơ cho đề ngắn lại). Bối cảnh chung
# "trang_dong_chi" (mỗi đề tối đa một câu).
# =====================================================================================================

_TR_DAN = (r"Bài thơ \textit{Đồng chí} của nhà thơ Chính Hữu được viết vào đầu năm $1948$, sau chiến dịch Việt Bắc thu đông $1947$, ca ngợi "
           r"tình đồng đội của những người lính trong kháng chiến chống thực dân Pháp."
           +
           r" Chiến tranh vô cùng khốc liệt: đêm rừng giá lạnh, thiếu thốn, hiểm nguy rình rập; vậy mà người chiến sĩ Cụ Hồ vẫn yêu đời, yêu "
           r"thiên nhiên, vẫn thấy vầng trăng đẹp như đang treo ngay đầu mũi súng của mình. Vầng trăng ấy cách chúng ta rất xa, nhưng bằng toán "
           r"học ta vẫn đo được nó. ")


def _tr_ng(n):
    """Số nguyên viết kiểu SGK, ngăn cách hàng nghìn bằng khoảng cách hẹp: 384400 -> 384\\,400."""
    return "{:,}".format(int(n)).replace(",", r"\,")


def _tr_d_th(d):
    """Góc nhìn (độ, làm tròn 0,01) của Mặt Trăng (đường kính thật 3 476 km) khi cách Trái Đất d km."""
    return round(math.degrees(2 * math.asin(1738.0 / d)), 2)


def _tr_bo1():
    """(d, theta, D): D = 2.d.sin(theta/2) tính từ số đo đã cho; D làm tròn đến hàng chục không sát ranh giới."""
    while True:
        d = random.randrange(363300, 405501, 100)
        th = _tr_d_th(d)
        D = 2 * d * math.sin(math.radians(th) / 2)
        if _xa_bien(D / 10):
            return d, th, D


def _tr_hinh1(d, th):
    """Sơ đồ tam giác cân EAB (hình KHÔNG đúng tỉ lệ: góc thật chỉ khoảng nửa độ)."""
    s = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s += "\\draw[fill=yellow!25] (5.0,0) circle (1.0);\n"
    s += "\\draw[very thick] (0,0) -- (5.0,1.0) -- (5.0,-1.0) -- cycle;\n"
    s += "\\fill (0,0) circle (0.06) node[left] {$E$};\n"
    s += "\\fill (5.0,1.0) circle (0.06) node[above right] {$A$};\n"
    s += "\\fill (5.0,-1.0) circle (0.06) node[below right] {$B$};\n"
    s += "\\node[font=\\scriptsize] at (2.3,0.95) {$%s$ km};\n" % _tr_ng(d)
    s += "\\node[font=\\scriptsize] at (2.3,-0.95) {$%s$ km};\n" % _tr_ng(d)
    s += "\\draw (1.1,0.22) arc (11.3:-11.3:1.12);\n"
    s += "\\node[font=\\scriptsize] at (1.55,0) {$%s^{\\circ}$};\n" % _x1(th, 2)
    s += "\\node[font=\\scriptsize] at (5.0,-1.55) {Mặt Trăng};\n"
    s += "\\node[font=\\scriptsize,gray] at (2.5,-1.9) {(hình không đúng tỉ lệ)};\n"
    return s + "\\end{tikzpicture}"


def _tr_cau1():
    d, th, D = _tr_bo1()
    chuc = _lt(D / 10) * 10
    intro = (_TR_DAN + r"Mặt Trăng cách Trái Đất khoảng $%s$ km (khoảng cách này thay đổi trong mỗi tháng, từ khoảng $363\,300$ km đến "
             r"khoảng $405\,500$ km). Từ Trái Đất, đường kính của Mặt Trăng được nhìn dưới góc khoảng $%s^{\circ}$ (số liệu làm tròn). "
             r"Coi Mặt Trăng là hình tròn; gọi $E$ là vị trí người quan sát, $AB$ là một đường kính của Mặt Trăng thì $EAB$ là tam giác "
             r"cân tại $E$ với $EA = EB = %s$ km và $\widehat{AEB} = %s^{\circ}$ (xem hình vẽ)."
             % (_tr_ng(d), _x1(th, 2), _tr_ng(d), _x1(th, 2)))
    giai = (r"Gọi $H$ là trung điểm của $AB$. Vì tam giác $EAB$ cân tại $E$ nên $EH$ vừa là trung tuyến vừa là đường cao và đường phân giác, "
            r"suy ra $EH \perp AB$ và $\widehat{AEH} = \dfrac{\widehat{AEB}}{2} = %s^{\circ}$. Trong tam giác vuông $AEH$: "
            r"$AH = EA \cdot \sin\widehat{AEH}$, nên $AB = 2AH = 2 \cdot EA \cdot \sin\dfrac{\widehat{AEB}}{2} = 2 \cdot %s \cdot \sin %s^{\circ} "
            r"\approx %s$ (km). Vậy đường kính Mặt Trăng khoảng $%s$ km."
            % (_xx(th / 2, 3), _tr_ng(d), _xx(th / 2, 3), _xx(D, 1), _tr_ng(chuc)))
    return dict(intro=intro, hinh=_tr_hinh1(d, th), d=d, th=th, D=D, chuc=chuc, giai=giai)


def _tr_bo2():
    """(alpha, beta, s, h, BC): cây thẳng đứng cao h = AB trên sườn dốc nghiêng beta; bóng AC = s trên sườn; ánh trăng hợp ngang alpha."""
    while True:
        al, be, s = random.randint(35, 60), random.randint(8, 20), random.randint(8, 20)
        h = s * math.sin(math.radians(al + be)) / math.cos(math.radians(al))
        bc = s * math.cos(math.radians(be)) / math.cos(math.radians(al))
        if 7 <= h <= 32 and _xa_bien(h, 1) and _xa_bien(bc, 1):
            return al, be, s, h, bc


def _tr_hinh2(al, be, s, h):
    """Tam giác ABC: A gốc cây, B ngọn cây (AB thẳng đứng), C đầu bóng trên sườn dốc (AC = s, nghiêng be so với phương ngang)."""
    k = 4.0 / max(s * math.cos(math.radians(be)), h)
    A = (0.0, 0.0)
    C = (s * math.cos(math.radians(be)) * k, s * math.sin(math.radians(be)) * k)
    B = (0.0, h * k)
    r = min(0.8, 0.4 * C[0])
    s_ = "\\begin{tikzpicture}[scale=1,font=\\footnotesize,line join=round]\n"
    s_ += "\\draw[gray] (-1.2,0) -- (%.2f,0);\n" % (C[0] + 0.2)
    s_ += "\\draw[very thick] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;\n" % (A + B + C)
    s_ += "\\draw[gray,dashed] (%.2f,%.2f) -- (%.2f,%.2f);\n" % (C[0], C[1], max(C[0] - 1.4, 0.15), C[1])
    for t, p, v in (("A", A, "below left"), ("B", B, "above"), ("C", C, "right")):
        s_ += "\\fill (%.2f,%.2f) circle (0.06) node[%s] {$%s$};\n" % (p + (v, t))
    s_ += "\\draw (%.2f,0) arc (0:%d:%.2f);\n" % (r, be, r)
    s_ += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (
        (r + 0.45) * math.cos(math.radians(be / 2)), (r + 0.45) * math.sin(math.radians(be / 2)), be)
    s_ += "\\draw (%.2f,%.2f) arc (%d:180:%.2f);\n" % (C[0] + r * math.cos(math.radians(180 - al)), C[1] + r * math.sin(math.radians(180 - al)), 180 - al, r)
    s_ += "\\node[font=\\scriptsize] at (%.2f,%.2f) {$%d^{\\circ}$};\n" % (
        C[0] + (r + 0.4) * math.cos(math.radians(180 - al / 2)), C[1] + (r + 0.4) * math.sin(math.radians(180 - al / 2)), al)
    s_ += "\\node[font=\\scriptsize,rotate=%d,above] at (%.2f,%.2f) {$%d$ m};\n" % (be, 0.42 * C[0], 0.42 * C[1], s)   # nhãn độ dài ở PHÍA TRÊN cạnh AC để không đè lên nhãn góc ở A
    # nhãn "ánh trăng" song song với tia BC, lệch ra phía ngoài tam giác (không đè lên tia)
    dx, dy = C[0] - B[0], C[1] - B[1]
    L = math.hypot(dx, dy)
    s_ += "\\node[font=\\scriptsize,gray,rotate=%d] at (%.2f,%.2f) {ánh trăng};\n" % (
        -al, (B[0] + C[0]) / 2 - 0.3 * dy / L, (B[1] + C[1]) / 2 + 0.3 * dx / L)
    return s_ + "\\end{tikzpicture}"


def _tr_cau2():
    al, be, s, h, bc = _tr_bo2()
    intro = (_TR_DAN + r"Một đêm trăng sáng trên một sườn đồi trong rừng, một cây cổ thụ mọc thẳng đứng. Sườn đồi nghiêng $%d^{\circ}$ so với "
             r"mặt phẳng nằm ngang, ánh trăng chiếu xuống hợp với mặt phẳng nằm ngang một góc $%d^{\circ}$ và bóng của cây đổ lên phía sườn dốc, "
             r"dài $%d$ m (đo dọc theo sườn đồi). Gọi $A$ là gốc cây, $B$ là ngọn cây, $C$ là đầu bóng của ngọn cây (các số đo là giả sử, "
             r"xem hình vẽ)." % (be, al, s))
    giai_h = (r"Trong tam giác $ABC$: $AB$ thẳng đứng, $AC$ nằm trên sườn dốc nghiêng $%d^{\circ}$ so với phương ngang nên $\widehat{BAC} = 90^{\circ} - %d^{\circ} = %d^{\circ}$. "
              r"Tia sáng $BC$ hợp với phương ngang góc $%d^{\circ}$ còn sườn dốc $CA$ hợp với phương ngang góc $%d^{\circ}$ (hai bên của phương ngang) nên "
              r"$\widehat{ACB} = %d^{\circ} + %d^{\circ} = %d^{\circ}$, suy ra $\widehat{ABC} = 180^{\circ} - %d^{\circ} - %d^{\circ} = %d^{\circ}$. "
              r"Theo định lí sin: $\dfrac{AB}{\sin\widehat{ACB}} = \dfrac{AC}{\sin\widehat{ABC}}$, nên $AB = \dfrac{AC \cdot \sin\widehat{ACB}}{\sin\widehat{ABC}} "
              r"= \dfrac{%d \cdot \sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$ (m)."
              % (be, be, 90 - be, al, be, al, be, al + be, 90 - be, al + be, 90 - al, s, al + be, 90 - al, _x1(h, 1)))
    giai_bc = (r"Theo định lí sin trong tam giác $ABC$: $\dfrac{BC}{\sin\widehat{BAC}} = \dfrac{AC}{\sin\widehat{ABC}}$ với $\widehat{BAC} = %d^{\circ}$, "
               r"$\widehat{ABC} = %d^{\circ}$, nên $BC = \dfrac{%d \cdot \sin %d^{\circ}}{\sin %d^{\circ}} \approx %s$ (m)."
               % (90 - be, 90 - al, s, 90 - be, 90 - al, _x1(bc, 1)))
    return dict(intro=intro, hinh=_tr_hinh2(al, be, s, h), al=al, be=be, s=s, h=h, bc=bc, giai_h=giai_h, giai_bc=giai_bc)


def _tr_mc_sa(bt, socau, dang):
    cau = ""
    so = 0
    while so < socau:
        if bt == 1:
            c = _tr_cau1()
            dap = str(c["chuc"])
            if dang == 2 and len(dap) > 4:
                continue
            hoi = r"đường kính của Mặt Trăng (đơn vị km, làm tròn đến hàng chục)"
            sai = [str(_lt(c["D"] / 2 / 10) * 10), str(_lt(c["D"] * 2 / 10) * 10), str(_lt(c["D"] / 10) * 10 + 40)]
            buoc = lambda t: str(c["chuc"] + 30 * t)
            giai = c["giai"]
        else:
            c = _tr_cau2()
            dap = _x1(c["h"], 1) if dang == 1 else _so(c["h"], 1)
            if dang == 2 and len(dap) > 4:
                continue
            hoi = r"chiều cao của cây cổ thụ, tức độ dài $AB$ (đơn vị mét, làm tròn đến hàng phần mười)"
            mau = _x1 if dang == 1 else _so
            sai = [mau(c["s"] * math.tan(math.radians(c["al"])), 1), mau(c["s"] * math.sin(math.radians(c["al"] + c["be"])), 1),
                   mau(c["bc"], 1)]
            buoc = lambda t: mau(c["h"] + 1.3 * t, 1)
            giai = c["giai_h"]
        so += 1
        if dang == 1:
            debai = c["intro"] + r" " + hoi[0].upper() + hoi[1:] + r" là"
            nh = _ba_nhieu(dap, [x for x in sai if x != "0"], buoc=buoc)
        else:
            debai = c["intro"] + r" Tính " + hoi + r"."
            nh = [buoc(d) for d in (1, -1, 2)]
        cau += MC_SA_answer_const(debai, dap, nh, giai, c["hinh"], 0, dang)
    return cau


def _tr_tl(bt, socau, dong):
    cau = ""
    for _ in range(socau):
        if bt == 1:
            c = _tr_cau1()
            # ý b): khi Mặt Trăng ở khoảng cách khác thì nhìn dưới góc bao nhiêu (dùng đường kính làm tròn ở ý a)
            while True:
                d2 = random.randrange(363300, 405501, 100)
                if abs(d2 - c["d"]) < 15000:
                    continue
                th2 = 2 * math.degrees(math.asin(c["chuc"] / (2.0 * d2)))
                th2_ex = 2 * math.degrees(math.asin(c["D"] / (2.0 * d2)))
                if _xa_bien(th2, 2) and _lt(th2 * 100) == _lt(th2_ex * 100):
                    break
            ds = [(r"Tính đường kính của Mặt Trăng (đơn vị km, làm tròn đến hàng chục).",
                   r"AB \approx %s\,\text{km}" % _tr_ng(c["chuc"]), c["giai"]),
                  (r"Khi Mặt Trăng ở cách Trái Đất $%s$ km, đường kính của Mặt Trăng (lấy kết quả câu trước) được nhìn dưới góc bao nhiêu độ "
                   r"(làm tròn đến hàng phần trăm)?" % _tr_ng(d2),
                   r"\widehat{AEB} \approx %s^{\circ}" % _x1(th2, 2),
                   r"Tam giác $EAB$ cân tại $E$ với $EA = EB = %s$ km, $AB \approx %s$ km nên $\sin\dfrac{\widehat{AEB}}{2} = \dfrac{AB}{2 \cdot EA} "
                   r"= \dfrac{%s}{2 \cdot %s} \approx %s$, suy ra $\dfrac{\widehat{AEB}}{2} \approx %s^{\circ}$ và $\widehat{AEB} \approx %s^{\circ}$."
                   % (_tr_ng(d2), _tr_ng(c["chuc"]), _tr_ng(c["chuc"]), _tr_ng(d2), _xx(c["chuc"] / (2.0 * d2), 6), _xx(th2 / 2, 3), _x1(th2, 2)))]
        else:
            c = _tr_cau2()
            ds = [(r"Tính chiều cao của cây cổ thụ, tức độ dài $AB$ (đơn vị mét, làm tròn đến hàng phần mười).",
                   r"AB \approx %s\,\text{m}" % _x1(c["h"], 1), c["giai_h"]),
                  (r"Tính khoảng cách từ ngọn cây đến đầu bóng, tức độ dài $BC$ (đơn vị mét, làm tròn đến hàng phần mười).",
                   r"BC \approx %s\,\text{m}" % _x1(c["bc"], 1), c["giai_bc"])]
        cau += TL_answer_text(c["intro"], ds, c["hinh"], 0, dong)
    return cau


def L10_C3_B6_VD036_MC_W_01(socau, dang=1):
    r"""Vầng trăng của người lính (Đồng chí) - tính đường kính Mặt Trăng từ khoảng cách và góc nhìn (tam giác cân).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số liệu Mặt Trăng thật, góc nhìn tính từ đường kính thật).
    """
    return _tr_mc_sa(1, socau, 1)


def L10_C3_B6_VD036_MC_W_02(socau, dang=1):
    r"""Vầng trăng của người lính (Đồng chí) - tính chiều cao cây cổ thụ từ bóng trăng trên sườn đồi (định lí sin).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo giả sử).
    """
    return _tr_mc_sa(2, socau, 1)


def L10_C3_B6_VD036_SA_W_01(socau, dang=2):
    r"""Vầng trăng của người lính (Đồng chí) - tính đường kính Mặt Trăng từ khoảng cách và góc nhìn (tam giác cân).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số liệu Mặt Trăng thật, góc nhìn tính từ đường kính thật).
    """
    return _tr_mc_sa(1, socau, 2)


def L10_C3_B6_VD036_SA_W_02(socau, dang=2):
    r"""Vầng trăng của người lính (Đồng chí) - tính chiều cao cây cổ thụ từ bóng trăng trên sườn đồi (định lí sin).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo giả sử).
    """
    return _tr_mc_sa(2, socau, 2)


def L10_C3_B6_VD036_TL_O_01(socau, dong=1):
    r"""Vầng trăng của người lính (Đồng chí) - tự luận: a) đường kính Mặt Trăng, b) góc nhìn khi Mặt Trăng ở khoảng cách khác.

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số liệu Mặt Trăng thật, góc nhìn tính từ đường kính thật).
    """
    return _tr_tl(1, socau, dong)


def L10_C3_B6_VD036_TL_O_02(socau, dong=1):
    r"""Vầng trăng của người lính (Đồng chí) - tự luận: a) chiều cao cây cổ thụ AB, b) khoảng cách từ ngọn cây đến đầu bóng BC (định lí sin).

    CLAUDE THEM 13/10/2026 - theo ý cô Lan (số đo giả sử).
    """
    return _tr_tl(2, socau, dong)

# Rút ngày 22/10/2026 - cô Lan: dạng NB034_B ("Biết <dữ kiện> thì S = ...") vô lý, xem đầu tệp.
def L10_C3_B6_NB034_MC_B_01(socau, dang=1):
    """Chọn công thức tính diện tích tam giác phù hợp với dữ kiện cho trước."""
    BO = [
        ("biết hai cạnh $b$, $c$ và góc $A$ xen giữa",
         r"$S = \dfrac{1}{2}bc\sin A$"),
        ("biết ba cạnh $a$, $b$, $c$",
         r"$S = \sqrt{p(p-a)(p-b)(p-c)}$"),
        ("biết ba cạnh $a$, $b$, $c$ và bán kính $R$ của đường tròn ngoại tiếp",
         r"$S = \dfrac{abc}{4R}$"),
        ("biết ba cạnh $a$, $b$, $c$ và bán kính $r$ của đường tròn nội tiếp",
         r"$S = pr$"),
        ("biết cạnh $a$ và đường cao $h_a$ ứng với cạnh đó",
         r"$S = \dfrac{1}{2}a h_a$"),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(BO))
        if i in gt:
            continue
        gt.append(i)

    cauTN = ''
    for i in gt:
        du_kien, ct = BO[i]
        ds = [x[1] for j, x in enumerate(BO) if j != i]
        random.shuffle(ds)
        debai = (r"Tam giác $ABC$ có diện tích $S$, nửa chu vi $p$. "
                 r"Khi %s, công thức tính diện tích tam giác là" % du_kien)
        giai = r"Với dữ kiện %s, ta dùng công thức %s." % (du_kien, ct)
        cauTN += MC_SA_answer_text(debai, ct, ds[:3], giai, 0, 0, dang)
    return cauTN


# Dữ kiện (mô tả, các đại lượng biết) và công thức (tex, đại lượng dùng, hàm thử số, đúng?) cho NB034_SA_B.
_C3S_DU_KIEN = [
    (r"ba cạnh $a$, $b$, $c$", {"a", "b", "c", "p"}),
    (r"ba cạnh $a$, $b$, $c$ và bán kính $R$ của đường tròn ngoại tiếp", {"a", "b", "c", "p", "R"}),
    (r"nửa chu vi $p$ và bán kính $r$ của đường tròn nội tiếp", {"p", "r"}),
    (r"hai cạnh $b$, $c$ và góc $A$", {"b", "c", "A"}),
    (r"hai cạnh $a$, $b$ và góc $C$", {"a", "b", "C"}),
    (r"cạnh $a$ và đường cao $h_a$", {"a", "ha"}),
]
_C3S_CT_S = [
    (r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}", {"p", "a", "b", "c"}),
    (r"S = \dfrac{abc}{4R}", {"a", "b", "c", "R"}),
    (r"S = pr", {"p", "r"}),
    (r"S = \dfrac{1}{2}bc\sin A", {"b", "c", "A"}),
    (r"S = \dfrac{1}{2}ab\sin C", {"a", "b", "C"}),
    (r"S = \dfrac{1}{2}a\cdot h_a", {"a", "ha"}),
    (r"S = \dfrac{abc}{2R}", {"a", "b", "c", "R"}),
    (r"S = 2pr", {"p", "r"}),
    (r"S = \dfrac{1}{2}bc\cos A", {"b", "c", "A"}),
    (r"S = \dfrac{1}{2}ab\sin A", {"a", "b", "A"}),
    (r"S = a\cdot h_a", {"a", "ha"}),
    (r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}", {"p", "a", "b", "c"}),
]


def _c3s_ct_dung(tex):
    """Công thức diện tích tex có đúng với mọi tam giác không (thử số)."""
    f = {
        r"S = \sqrt{p\left(p - a\right)\left(p - b\right)\left(p - c\right)}":
            lambda T: math.sqrt(T["p"] * (T["p"] - T["a"]) * (T["p"] - T["b"]) * (T["p"] - T["c"])),
        r"S = \dfrac{abc}{4R}": lambda T: T["a"] * T["b"] * T["c"] / (4 * T["R"]),
        r"S = pr": lambda T: T["p"] * T["r"],
        r"S = \dfrac{1}{2}bc\sin A": lambda T: 0.5 * T["b"] * T["c"] * math.sin(T["A"]),
        r"S = \dfrac{1}{2}ab\sin C": lambda T: 0.5 * T["a"] * T["b"] * math.sin(T["C"]),
        r"S = \dfrac{1}{2}a\cdot h_a": lambda T: 0.5 * T["a"] * T["ha"],
        r"S = \dfrac{abc}{2R}": lambda T: T["a"] * T["b"] * T["c"] / (2 * T["R"]),
        r"S = 2pr": lambda T: 2 * T["p"] * T["r"],
        r"S = \dfrac{1}{2}bc\cos A": lambda T: 0.5 * T["b"] * T["c"] * math.cos(T["A"]),
        r"S = \dfrac{1}{2}ab\sin A": lambda T: 0.5 * T["a"] * T["b"] * math.sin(T["A"]),
        r"S = a\cdot h_a": lambda T: T["a"] * T["ha"],
        r"S = \sqrt{p\left(p + a\right)\left(p + b\right)\left(p + c\right)}":
            lambda T: math.sqrt(T["p"] * (T["p"] + T["a"]) * (T["p"] + T["b"]) * (T["p"] + T["c"])),
    }[tex]
    return _c3s_dung(lambda T: (T["S"], f(T)))


def L10_C3_B6_NB034_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bản trả lời ngắn của NB034_MC_B (cùng Dang: chọn công thức diện tích phù hợp với dữ kiện):
    bốn khẳng định ``Biết <dữ kiện> thì $S = \ldots$''; khẳng định đúng khi công thức đúng VÀ chỉ dùng các đại lượng
    đã biết (biết ba cạnh thì biết nửa chu vi $p$). Đếm số khẳng định đúng (sai). Mức Nhận biết - LUYỆN TẬP THÊM
    (ngoài YCCĐ).

    CLAUDE THEM 15/10/2026 - co Lan duyet lai.
    """
    ten_dai = {"a": "$a$", "b": "$b$", "c": "$c$", "p": "$p$", "R": "$R$", "r": "$r$", "A": "góc $A$", "C": "góc $C$",
               "ha": "$h_a$"}
    cau = ""
    for _ in range(socau):
        dung, sai = [], []
        for mo_dk, biet in _C3S_DU_KIEN:
            for tex, dung_dl in _C3S_CT_S:
                ok_ct = _c3s_ct_dung(tex)
                thieu = sorted(dung_dl - biet)
                kd = r"Biết %s thì $%s$" % (mo_dk, tex)
                if ok_ct and not thieu:
                    dung.append((kd, r"đây là công thức diện tích và chỉ dùng các đại lượng đã biết", tex))
                elif ok_ct:
                    sai.append((kd, r"công thức đúng nhưng cần thêm %s chưa biết" % ", ".join(ten_dai[x] for x in thieu), tex))
                elif not thieu or random.random() < 0.3:
                    sai.append((kd, r"công thức $%s$ sai" % tex, tex))
        mo = (r"Cho tam giác $ABC$ có $BC = a$, $CA = b$, $AB = c$, diện tích $S$, nửa chu vi $p$, đường cao $h_a$ kẻ từ $A$; "
              r"$R$, $r$ lần lượt là bán kính đường tròn ngoại tiếp, nội tiếp tam giác.")
        cau += _c3s_dem(mo, dung, sai, dang)
    return cau

if __name__ == "__main__":
    random.seed(1)
    for ten in ("L10_C3_B6_VD036_TL_E_01", "L10_C3_B6_VD036_MC_K_01", "L10_C3_B6_VD036_SA_K_01",
                "L10_C3_B6_VD036_MC_L_01", "L10_C3_B6_VD036_SA_L_01",
                "L10_C3_B6_VD036_MC_W_01", "L10_C3_B6_VD036_MC_W_02", "L10_C3_B6_VD036_SA_W_01",
                "L10_C3_B6_VD036_SA_W_02", "L10_C3_B6_VD036_TL_O_01", "L10_C3_B6_VD036_TL_O_02",
                "L10_C3_B6_NB034_MC_B_01", "L10_C3_B6_NB034_SA_B_01"):
        print("%% ====", ten)
        print(globals()[ten](1))
