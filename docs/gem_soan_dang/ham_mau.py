# =====================================================================
# HÀM MẪU CHO GEM "SOẠN DẠNG" - Ngân Hàng Đề AI (cô Lan, 28/10/2026)
# Bốn hàm mẫu đủ bốn loại câu: MC (trắc nghiệm), SA (trả lời ngắn),
# TF (đúng/sai), TL (tự luận). Chữ cái X trong tên hàm chỉ để minh hoạ;
# khi viết thật, dùng chữ cái / số biến thể theo ID đã chọn.
# Tệp này chạy được: python3 ham_mau.py (cần math_type.py cùng thư mục).
# =====================================================================
from math_type import *


# ---------------------------------------------------------------------
# 1) TRẮC NGHIỆM NHIỀU LỰA CHỌN (MC) - tham số thứ hai là dang=1
# ---------------------------------------------------------------------
def L10_C3_B6_TH032_MC_X_01(socau, dang=1):
    """Định lí côsin: biết hai cạnh và góc xen giữa (60 hoặc 120 độ), tính cạnh thứ ba."""
    import random
    # Bộ số chọn sẵn để cạnh thứ ba là số nguyên (kết quả "đẹp")
    BO_SO = {60: [(3, 8, 7), (5, 8, 7), (8, 15, 13), (7, 15, 13), (5, 21, 19), (16, 21, 19)],
             120: [(3, 5, 7), (7, 8, 13), (5, 16, 19), (6, 10, 14), (9, 15, 21)]}
    da_co = []
    while len(da_co) < socau:                      # socau câu KHÁC NHAU về số liệu
        A = random.choice([60, 120])
        b, c, a = random.choice(BO_SO[A])
        if (A, b, c) not in da_co:
            da_co.append((A, b, c))
    cau = ''
    for A, b, c in da_co:
        a = [t for t in BO_SO[A] if t[0] == b and t[1] == c][0][2]
        cosA = r"\dfrac{1}{2}" if A == 60 else r"-\dfrac{1}{2}"
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\widehat{BAC} = %d^{\circ}$. "
                 r"Độ dài cạnh $BC$ bằng" % (b, c, A))
        # Nhiễu: sai lầm học sinh hay mắc (nhầm dấu cos, quên căn, cộng thẳng).
        # Số thập phân trong công thức viết dấu phẩy có ngoặc: 13{,}08 (không để LaTeX chèn khoảng trắng).
        a_nham_dau = round((b * b + c * c + (b * c if A == 60 else -b * c)) ** 0.5, 2)
        nhieu = [str(a_nham_dau).replace(".", "{,}"), str(a * a), str(b + c), str(abs(b - c) + 1)]
        giai = (r"Theo định lí côsin: $BC^{2} = AC^{2} + AB^{2} - 2\cdot AC\cdot AB\cdot\cos A "
                r"= %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\left(%s\right) = %d$. Vậy $BC = %d$."
                % (b, c, b, c, cosA, a * a, a))
        cau += MC_SA_answer_const(debai, str(a), nhieu, giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# 2) TRẢ LỜI NGẮN (SA) - CÙNG dạng, CÙNG chữ cái với MC; dang=2
#    Một câu hỏi - một đáp số; đáp số tối đa 4 kí tự (kể cả dấu "-" và ",")
# ---------------------------------------------------------------------
def L10_C3_B6_TH032_SA_X_01(socau, dang=2):
    """Định lí côsin: biết hai cạnh và góc xen giữa, tính cạnh thứ ba (trả lời ngắn)."""
    return L10_C3_B6_TH032_MC_X_01(socau, dang)   # dùng lại thân hàm MC, chỉ đổi dang=2


# ---------------------------------------------------------------------
# 3) ĐÚNG/SAI (TF) - theo CHƯƠNG, không có bài/mức độ trong ID; tham số socot
#    Bốn ý a) NB, b) TH, c) VD, d) VDC; MỖI ý có >= 3 phát biểu đúng và >= 3 phát biểu sai.
#    Phát biểu đúng: "{\True ...}", phát biểu sai: "{...}". Mỗi phát biểu kèm lời giải.
# ---------------------------------------------------------------------
def L10_C3_TF_X_01(socau, socot=1):
    """Đúng/Sai - giá trị lượng giác của góc bù nhau và định lí côsin."""
    import random
    cau = ''
    for _ in range(socau):
        b, c = random.choice([(3, 8), (5, 8), (8, 15)])
        a2 = b * b + c * c - b * c                       # góc A = 60 độ
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$, $\widehat{BAC} = 60^{\circ}$. "
                 r"Xét tính đúng sai của các khẳng định sau:" % (b, c))
        # a) NB - nhắc lại công thức / tính chất
        y_a = [(r"{\True $\sin(180^{\circ}-\alpha) = \sin\alpha$}", r"Đúng: hai góc bù nhau có sin bằng nhau."),
               (r"{\True $\cos(180^{\circ}-\alpha) = -\cos\alpha$}", r"Đúng: hai góc bù nhau có côsin đối nhau."),
               (r"{\True $BC^{2} = AB^{2} + AC^{2} - 2AB\cdot AC\cos A$}", r"Đúng: định lí côsin."),
               (r"{$\cos(180^{\circ}-\alpha) = \cos\alpha$}", r"Sai: côsin của hai góc bù nhau đối nhau."),
               (r"{$\sin(180^{\circ}-\alpha) = -\sin\alpha$}", r"Sai: sin của hai góc bù nhau bằng nhau."),
               (r"{$BC^{2} = AB^{2} + AC^{2} + 2AB\cdot AC\cos A$}", r"Sai dấu: định lí côsin là dấu trừ.")]
        # b) TH - một bước thay số
        y_b = [(r"{\True $\cos A = \dfrac{1}{2}$}", r"Đúng: $\cos 60^{\circ} = \dfrac{1}{2}$."),
               (r"{\True $\sin A = \dfrac{\sqrt{3}}{2}$}", r"Đúng: $\sin 60^{\circ} = \dfrac{\sqrt{3}}{2}$."),
               (r"{\True $\cos(B + C) = -\dfrac{1}{2}$}", r"Đúng: $B + C = 120^{\circ}$ nên $\cos(B+C) = -\cos A = -\dfrac{1}{2}$."),
               (r"{$\cos A = \dfrac{\sqrt{3}}{2}$}", r"Sai: $\cos 60^{\circ} = \dfrac{1}{2}$."),
               (r"{$\sin(B + C) = -\dfrac{\sqrt{3}}{2}$}", r"Sai: $\sin(B+C) = \sin A = \dfrac{\sqrt{3}}{2}$."),
               (r"{$\cos(B + C) = \dfrac{1}{2}$}", r"Sai: $\cos(B+C) = -\cos A = -\dfrac{1}{2}$.")]
        # c) VD - tính cạnh bằng định lí côsin
        a = int(round(a2 ** 0.5))
        ly_c = r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\dfrac{1}{2} = %d$ nên $BC = %d$." % (c, b, c, b, a2, a)
        y_c = [(r"{\True $BC^{2} = %d$}" % a2, r"Đúng. " + ly_c),
               (r"{\True $BC = %d$}" % a, r"Đúng. " + ly_c),
               (r"{\True Chu vi tam giác $ABC$ bằng $%d$}" % (a + b + c), r"Đúng. " + ly_c + r" Chu vi $= %d$." % (a + b + c)),
               (r"{$BC^{2} = %d$}" % (b * b + c * c + b * c), r"Sai: nhầm dấu. " + ly_c),
               (r"{$BC = %d$}" % (b + c), r"Sai: cộng thẳng hai cạnh. " + ly_c),
               (r"{Chu vi tam giác $ABC$ bằng $%d$}" % (2 * (b + c)), r"Sai. " + ly_c)]
        # d) VDC - nhiều bước: diện tích rồi đường cao
        S2 = b * c                                       # S = (1/2) b c sin60 = b c căn3 / 4
        y_d = [(r"{\True Diện tích tam giác $ABC$ bằng $\dfrac{%d\sqrt{3}}{4}$}" % S2,
                r"Đúng: $S = \dfrac{1}{2}AB\cdot AC\sin A = \dfrac{%d\sqrt{3}}{4}$." % S2),
               (r"{\True Đường cao kẻ từ $A$ bằng $\dfrac{%d\sqrt{3}}{%d}$}" % (S2, 2 * a),
                r"Đúng: $h_a = \dfrac{2S}{BC} = \dfrac{%d\sqrt{3}}{%d}$." % (S2, 2 * a)),
               (r"{\True $\sin B = \dfrac{%d\sqrt{3}}{%d}$}" % (b, 2 * a),
                r"Đúng: định lí sin $\sin B = \dfrac{AC\sin A}{BC} = \dfrac{%d\sqrt{3}}{%d}$." % (b, 2 * a)),
               (r"{Diện tích tam giác $ABC$ bằng $\dfrac{%d}{4}$}" % S2,
                r"Sai: dùng $\cos A$ thay cho $\sin A$; đúng là $\dfrac{%d\sqrt{3}}{4}$." % S2),
               (r"{Đường cao kẻ từ $A$ bằng $\dfrac{%d\sqrt{3}}{%d}$}" % (S2, 4 * a),
                r"Sai: quên nhân 2; $h_a = \dfrac{2S}{BC}$."),
               (r"{$\sin B = \dfrac{%d\sqrt{3}}{%d}$}" % (c, 2 * a),
                r"Sai: nhầm cạnh đối diện góc $B$ là $AC$.")]
        cau += TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], 0, 0, socot)
    return cau


# ---------------------------------------------------------------------
# 4) TỰ LUẬN (TL) - TỪ HAI Ý trở lên, hai đơn vị kiến thức của CÙNG chương;
#    ID theo chương: L<lớp>_C<chương>_<đơn vị ý a>_<đơn vị ý b>_TL_<chữ cái>; tham số dong
#    Mỗi ý là bộ ba (câu hỏi, đáp số, lời giải).
# ---------------------------------------------------------------------
def L10_C3_TH031_TH032_TL_X_01(socau, dong=1):
    """Ý a) góc bù trong tam giác (TH031), ý b) định lí côsin (TH032)."""
    import random
    cau = ''
    for _ in range(socau):
        b, c, a = random.choice([(3, 8, 7), (5, 8, 7), (8, 15, 13), (7, 15, 13), (5, 21, 19), (16, 21, 19)])
        debai = (r"Cho tam giác $ABC$ có $AC = %d$, $AB = %d$ và $\widehat{B} + \widehat{C} = 120^{\circ}$." % (b, c))
        ds_y = [
            (r"Tính $\cos A$.", r"\dfrac{1}{2}",
             r"$\widehat{A} = 180^{\circ} - (\widehat{B} + \widehat{C}) = 60^{\circ}$ nên $\cos A = \dfrac{1}{2}$."),
            (r"Tính độ dài cạnh $BC$.", str(a),
             r"$BC^{2} = %d^{2} + %d^{2} - 2\cdot %d\cdot %d\cdot\dfrac{1}{2} = %d$ nên $BC = %d$." % (b, c, b, c, a * a, a)),
        ]
        cau += TL_answer_text(debai, ds_y, 0, 0, dong)
    return cau


if __name__ == "__main__":
    import random
    for f in (L10_C3_B6_TH032_MC_X_01, L10_C3_B6_TH032_SA_X_01, L10_C3_TF_X_01, L10_C3_TH031_TH032_TL_X_01):
        for s in range(30):
            random.seed(s)
            f(2)
        print(f.__name__, "OK")
    print(L10_C3_B6_TH032_MC_X_01(1))
