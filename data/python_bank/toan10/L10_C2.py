# ==========================================
# CHƯƠNG 2 (lớp 10): BẤT PHƯƠNG TRÌNH VÀ HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN
#   Bài 3. Bất phương trình bậc nhất hai ẩn
#   Bài 4. Hệ bất phương trình bậc nhất hai ẩn
#
# Nguồn: tệp LopXChuong2.py của cô Lan, chuyển sang chuẩn ngân hàng
# (đổi tên hàm theo ID, bỏ lệnh gọi ở mức mô-đun, vá lỗi). Nội dung toán
# và lời giải giữ NGUYÊN như cô viết.
# ==========================================
import io
import os
import re
import math
import random
from collections import namedtuple
from fractions import Fraction

# Tep goc cua co Lan import np HAI LAN: 'import numpy.random as np' roi
# 'import numpy as np'. Lan sau ghi de lan truoc, nen trong ca tep np
# CHINH LA numpy va ma nguon goi np.random.choice / np.random.randint.
import numpy as np
from sympy import *
from sympy import Symbol, latex
from sympy.abc import x, y, z, a, b

from math_type import *
import DefChung as dc



# ---- Ham bo tro: phuong trinh tong quat duong thang qua hai diem ----
def pttq_duong_thang(x1, y1, x2, y2):
    # Vector pháp tuyến n = (y1-y2, x2-x1)
    a = y1 - y2
    b = x2 - x1
    # c = -(a*x1 + b*y1)
    c = -(a * x1 + b * y1)

    # Rút gọn hệ số (Giữ nguyên logic rút gọn và chuẩn hóa dấu)
    if a == 0 and b == 0:
        return [0, 0, 0]

    g = 0
    if a != 0: g = math.gcd(g, abs(a))
    if b != 0: g = math.gcd(g, abs(b))
    if c != 0: g = math.gcd(g, abs(c))

    if g != 0:
        a = a // g
        b = b // g
        c = c // g

    # Đảm bảo hệ số đầu không âm (nếu không bằng 0)
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c

    return [a, b, c]


# ---- Nhan ra bat phuong trinh bac nhat hai an ----
# (tên cũ của cô: K10_2_3_1_1_H)
def L10_C2_B3_NB022_MC_A_01(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        dau_list = ['>', '<', '\\ge', '\\le']
        dau = np.random.choice(dau_list)

        # Sinh hệ số cho BPT bậc nhất hai ẩn
        bpt = []
        while len(bpt) < 3:
            k = np.random.randint(-10, 11)
            if k != 0 and k not in bpt:
                bpt.append(k)

        # Tính UCLN 3 số
        d0 = math.gcd(math.gcd(bpt[0], bpt[1]), bpt[2])
        fx = [int(bpt[0] / d0), int(bpt[1] / d0), int(bpt[2] / d0)]

        v = [fx, dau]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        fx, dau = v[0], v[1]

        # Tạo đáp án đúng (bpt bậc nhất hai ẩn)
        dapso = f"{latex(fx[0]*x + fx[1]*y)} {dau} {fx[2]}"

        # Tạo 3 đáp án sai (nhiễu)
        dau_nhieu = np.random.choice(['>', '<', '\\ge', '\\le'], 3, replace=True)
        f1x = [fx[0]*np.random.randint(1, 3), fx[1]*np.random.randint(1, 3), fx[2]]
        f2x = [fx[0], fx[1], fx[2]*np.random.randint(2, 4)]
        f3x = [fx[0]*fx[1], fx[1]*fx[1], fx[2]]

        nhieu1 = f"{latex(f1x[0]*x**2 + f1x[1]*y)} {dau_nhieu[0]} {f1x[2]}"
        nhieu2 = f"{latex((f2x[0]*x + f2x[1]*y)**2)} {dau_nhieu[1]} {f2x[2]}"
        nhieu3 = f"{latex(f3x[0]*x**3 + f3x[1])} {dau_nhieu[2]} 0"

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        # Sinh đề bài
        debai = (
            "Bất phương trình nào sau đây là bất phương trình bậc nhất hai ẩn?"
        )

        # Lời giải
        giai = f"""
        Một bất phương trình bậc nhất hai ẩn có dạng $a x + b y {dau} c$ với $a,b$ không đồng thời bằng 0.\\\\
        Trong các phương án, chỉ có bất phương trình:
        \\[{latex(fx[0]*x + fx[1]*y)} {dau} {fx[2]}\\]
        là bất phương trình bậc nhất hai ẩn, vì mỗi ẩn chỉ có số mũ 1.
        """


        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

# ================================================
# Cách dùng thử:
# ================================================
# Nếu bạn có sẵn MC_SA_answer_const:
#print(K10_2_3_1_1_H(4, 1))   # 4 câu trắc nghiệm


#
#
# def K10_2_3_1_1_NB(): #DẠNG 1: nhận biết bpt, hệ bpt
#     with open(r"latex\data\de.tex", "a", encoding='utf-8') as de:
#         x = Symbol('x')
#         y = Symbol('y')
#
#         dau = np.choice(['>', '<', '\ge', '\le'])
#         bpt = []
#         for i in range(0,3):
#             k = np.randint(-10,10)
#             while (k == 0) or (k in bpt):
#                 k = np.randint(-10,10)
#             bpt.append(k)
#         d01 = dc.UCLN(bpt[0],bpt[1])
#         d02 = dc.UCLN(bpt[1],bpt[2])
#         if d01 > d02:
#             d0 = d01 / d02
#         elif d01 == d02:
#             d0 = d01
#         else:
#             d0 = d02 / d01
#         if dc.is_integer(d0) == True:
#             fx = [int(bpt[0]/d0), int(bpt[1]/d0), int(bpt[2]/d0)]
#         else:
#             fx = bpt
#
#         dau1 = np.choice(['>', '<', '\ge', '\le'])
#         bpt1 = []
#         for i in range(0,3):
#             k = np.randint(-10,10)
#             while (k == 0) or (k in bpt1):
#                 k = np.randint(-10,10)
#             bpt1.append(k)
#         d11 = dc.UCLN(bpt1[0],bpt1[1])
#         d12 = dc.UCLN(bpt1[1],bpt1[2])
#         if d11 > d12:
#             d1 = d11 / d12
#         elif d11 == d12:
#             d1 = d11
#         else:
#             d1 = d12 / d11
#         if dc.is_integer(d1) == True:
#             f1x = [int(bpt1[0]/d1), int(bpt1[1]/d1), int(bpt1[2]/d1)]
#         else:
#             f1x = bpt1
#
#         dau2 = np.choice(['>', '<', '\ge', '\le'])
#         f2x = []
#         for i in range(0,4):
#             k = np.randint(1,3)
#             f2x.append(k)
#         while f2x[0] == f2x[1] == f2x[2] == f2x[3]:
#             k = np.randint(1,3)
#         f2x.pop(-1)
#         f2x.append(k)
#         c = np.choice([-1,1])
#
#
#         dau2 = np.choice(['>', '<', '\ge', '\le'])
#         bpt3 = []
#         for i in range(0,2):
#             k = np.randint(-9,9)
#             while (k == 0) or (k in bpt3):
#                 k = np.randint(-9,9)
#             bpt3.append(k)
#         d3 = dc.UCLN(bpt3[0], bpt3[1])
#         f3x = [int(bpt3[0]/d3),int(bpt3[1]/d3)]
#
#         de.write(r"\begin{ex}" + os.linesep)
#         de.write(r"Bất phương trình nào sau đây là bất phương trình bậc nhất hai ẩn?" + os.linesep)
#         de.write(r"\choice" + os.linesep)
#         de.write(r"{\True $%s %s %s$}" %(latex(fx[0] * x + fx[1] * y), dau, fx[2]) + os.linesep)
#         de.write(r"{$%s %s %s$}" %(latex(f1x[0] * x**2 + f1x[1] * y**2), dau1, f1x[2]) + os.linesep)
#         de.write(r"{$%s %s %s$}" %(latex((f2x[0] * x + f2x[1] * y) * (f2x[2] * x + f2x[3] * y)), dau2, c) + os.linesep)
#         de.write(r"{$%s %s 0$}" %(latex(f3x[0] * np.choice([x, y])**3  + f3x[1]), dau2) + os.linesep)
#         de.write(r"\loigiai{}" + os.linesep)
#         de.write(r"\end{ex}" + os.linesep)


# ---- Nhan ra bat phuong trinh bac nhat hai an (bien the) ----
# (tên cũ của cô: K10_2_3_1_1_NB)
def L10_C2_B3_NB022_MC_A_02(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        # --- Sinh dữ liệu cho phương án đúng (fx) ---
        dau = np.random.choice(['>', '<', '\\ge', '\\le'])
        bpt = []
        while len(bpt) < 3:
            k = np.random.randint(-10, 11)
            if k != 0 and k not in bpt:
                bpt.append(k)

        d01 = math.gcd(bpt[0], bpt[1])
        d02 = math.gcd(bpt[1], bpt[2])
        if d01 > d02:
            d0 = d01 / d02
        elif d01 == d02:
            d0 = d01
        else:
            d0 = d02 / d01

        if (int(d0) == d0):
            fx = [int(bpt[0] / d0), int(bpt[1] / d0), int(bpt[2] / d0)]
        else:
            fx = bpt

        # --- Sinh dữ liệu cho phương án nhiễu 1 (f1x) ---
        dau1 = np.random.choice(['>', '<', '\\ge', '\\le'])
        bpt1 = []
        while len(bpt1) < 3:
            k = np.random.randint(-10, 11)
            if k != 0 and k not in bpt1:
                bpt1.append(k)

        d11 = math.gcd(bpt1[0], bpt1[1])
        d12 = math.gcd(bpt1[1], bpt1[2])
        if d11 > d12:
            d1 = d11 / d12
        elif d11 == d12:
            d1 = d11
        else:
            d1 = d12 / d11

        if (int(d1) == d1):
            f1x = [int(bpt1[0] / d1), int(bpt1[1] / d1), int(bpt1[2] / d1)]
        else:
            f1x = bpt1

        # --- Sinh dữ liệu cho phương án nhiễu 2 (f2x) ---
        dau2 = np.random.choice(['>', '<', '\\ge', '\\le'])
        f2x = []
        for _ in range(4):
            f2x.append(np.random.randint(1, 4))

        # Đảm bảo các hệ số không bằng nhau đồng thời gây triệt tiêu bất thường
        while f2x[0] == f2x[1] == f2x[2] == f2x[3]:
            f2x[3] = np.random.randint(1, 4)

        c = int(np.random.choice([-1, 1]))

        # --- Sinh dữ liệu cho phương án nhiễu 3 (f3x) ---
        dau3 = np.random.choice(['>', '<', '\\ge', '\\le'])
        bpt3 = []
        while len(bpt3) < 2:
            k = np.random.randint(-9, 10)
            if k != 0 and k not in bpt3:
                bpt3.append(k)

        d3 = math.gcd(bpt3[0], bpt3[1])
        f3x = [int(bpt3[0] / d3), int(bpt3[1] / d3)]
        bien_ngau_nhien = np.random.choice([x, y])

        # Lưu bộ giá trị độc nhất nhằm tránh trùng lặp đề bài
        v = [fx, dau, f1x, dau1, f2x, dau2, c, f3x, dau3, bien_ngau_nhien]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        fx, dau, f1x, dau1, f2x, dau2, c, f3x, dau3, bien_ngau_nhien = v

        # Chuẩn hóa đáp số và phương án nhiễu (Không bọc dấu $ ở đây)
        dapso = f"{latex(fx[0] * x + fx[1] * y)} {dau} {fx[2]}"

        nhieu1 = f"{latex(f1x[0] * x ** 2 + f1x[1] * y ** 2)} {dau1} {f1x[2]}"
        nhieu2 = f"{latex((f2x[0] * x + f2x[1] * y) * (f2x[2] * x + f2x[3] * y))} {dau2} {c}"
        nhieu3 = f"{latex(f3x[0] * bien_ngau_nhien ** 3 + f3x[1])} {dau3} 0"

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        debai = "Bất phương trình nào sau đây là bất phương trình bậc nhất hai ẩn?"

        giai = f"""
        Bất phương trình bậc nhất hai ẩn có dạng tổng quát là $a x + b y {dau} c$ (hoặc với các dấu $<, \\le, \\ge$), trong đó $a,b$ không đồng thời bằng $0$.\\\\
        * Xét các phương án nhiễu: chứa các số hạng bậc hai $x^2, y^2$, tích $x \\cdot y$, hoặc bậc ba ${latex(bien_ngau_nhien ** 3)}$ nên không phải bậc nhất hai ẩn.\\\\
        * Phương án đúng: ${latex(fx[0] * x + fx[1] * y)} {dau} {fx[2]}$ là bất phương trình bậc nhất hai ẩn vì hai ẩn $x, y$ đều có bậc bằng $1$.
        """

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


# ---- Diem nao thuoc mien nghiem cua bat phuong trinh ----
# (tên cũ của cô: K10_CheckDiemBPT_H)
def L10_C2_B3_NB023_MC_A_01(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        # 1️⃣ Sinh Bất phương trình ax + by + c R 0

        # Hệ số a, b (khác 0)
        a = np.random.randint(-3, 4)
        while a == 0:
            a = np.random.randint(-3, 4)

        b = np.random.randint(-3, 4)
        while b == 0:
            b = np.random.randint(-3, 4)

        # Hệ số c
        c = np.random.randint(-5, 6)

        # Hàm kiểm tra F(x, y) = ax + by + c
        F = lambda x_val, y_val: a * x_val + b * y_val + c

        # Dấu bất đẳng thức
        dau_list = ['\\le', '\\ge', '<', '>']
        dau = np.random.choice(dau_list)

        # 2️⃣ Sinh 4 điểm A, B, C, D (1 đúng, 3 nhiễu)

        diem = []

        # Sinh Đáp án ĐÚNG (diem_dung)
        while len(diem) == 0:
            x_d = np.random.randint(-4, 5)
            y_d = np.random.randint(-4, 5)

            ketqua = F(x_d, y_d)

            # Kiểm tra xem điểm (x_d, y_d) có thỏa mãn BPT không
            thoa_man = False
            if dau == '\\le':
                if ketqua <= 0: thoa_man = True
            elif dau == '\\ge':
                if ketqua >= 0: thoa_man = True
            elif dau == '<':
                if ketqua < 0: thoa_man = True
            elif dau == '>':
                if ketqua > 0: thoa_man = True

            if thoa_man:
                diem_dung = (x_d, y_d)
                diem.append(diem_dung)

        # Sinh 3 điểm NHIỄU (không thỏa mãn BPT)
        while len(diem) < 4:
            x_n = np.random.randint(-4, 5)
            y_n = np.random.randint(-4, 5)
            diem_n = (x_n, y_n)

            # Đảm bảo điểm nhiễu chưa có trong danh sách
            if diem_n in diem:
                continue

            ketqua = F(x_n, y_n)

            # Kiểm tra xem điểm (x_n, y_n) có thỏa mãn BPT không (NGƯỢC LẠI)
            thoa_man_n = False
            if dau == '\\le':
                if ketqua <= 0: thoa_man_n = True
            elif dau == '\\ge':
                if ketqua >= 0: thoa_man_n = True
            elif dau == '<':
                if ketqua < 0: thoa_man_n = True
            elif dau == '>':
                if ketqua > 0: thoa_man_n = True

            # Nếu điểm này KHÔNG thỏa mãn BPT ban đầu (thoa_man_n == False), thì nó là nhiễu
            if not thoa_man_n:
                diem.append(diem_n)

        # Trộn các điểm để đáp án đúng không luôn ở vị trí đầu
        np.random.shuffle(diem)

        # 3️⃣ Đảm bảo mỗi câu sinh ra duy nhất
        v = [a, b, c, dau, diem]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        a, b, c, dau, diem = v
        diem_dung = (0, 0)

        # Xác định lại đáp án đúng trong danh sách đã trộn
        F = lambda x_val, y_val: a * x_val + b * y_val + c

        for p in diem:
            x_p, y_p = p
            ketqua = F(x_p, y_p)

            thoa_man = False
            if dau == '\\le':
                if ketqua <= 0: thoa_man = True
            elif dau == '\\ge':
                if ketqua >= 0: thoa_man = True
            elif dau == '<':
                if ketqua < 0: thoa_man = True
            elif dau == '>':
                if ketqua > 0: thoa_man = True

            if thoa_man:
                diem_dung = p
                break

        # 4️⃣ Tạo nội dung LaTeX

        # Biểu thức BPT: ax + by + c R 0
        VT_BPT = latex(a * x + b * y + c)

        debai = f"""Trong các điểm sau, điểm nào thuộc miền nghiệm của bất phương trình ${VT_BPT} {dau} 0$"""

        # Đáp án đúng
        dapso = f"({diem_dung[0]}; {diem_dung[1]})"

        # Danh sách nhiễu
        dsnhieu = [f"({p[0]}; {p[1]})" for p in diem if p != diem_dung]

        # Lời giải
        giai = f"""
            Bất phương trình đã cho là $${VT_BPT} {dau} 0$$

            Ta kiểm tra điểm đáp án đúng $P({diem_dung[0]}; {diem_dung[1]})$:
            Thay tọa độ của $P$ vào vế trái của BPT, ta được:
            $$F({diem_dung[0]}; {diem_dung[1]}) = {a}({diem_dung[0]}) + {b}({diem_dung[1]}) + {c} = {F(diem_dung[0], diem_dung[1])}$$

            Vì ${F(diem_dung[0], diem_dung[1])} {dau} 0$ là mệnh đề \\textbf{{ĐÚNG}}, nên điểm $P({diem_dung[0]}; {diem_dung[1]})$ thuộc miền nghiệm của bất phương trình.

            (Các điểm còn lại không thỏa mãn bất phương trình.)
        """

        # Thêm câu hỏi vào chuỗi kết quả
        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

# ---- Hinh nao bieu dien mien nghiem cua bat phuong trinh (co hinh) ----
# (tên cũ của cô: K10_2_3_2_1_H)
# ---------------------------------------------------------------------
# MIEN NGHIEM CUA BAT PHUONG TRINH BAC NHAT HAI AN - VE HINH (TH024_MC_A)
#
# SUA 30/09/2026 (co Lan: "gach phai het khu vuc duoc tao boi 2 truc Ox va
# Oy... cac hinh nay o moi phuong an chon"; "moi cai theo sach giao khoa hien
# hanh"). Ban cu:
#   - chi gach mot dai sat duong thang (lenh plot ... |- (diem goc));
#   - boc them mot cap { } quanh moi hinh -> tren web phuong an hien
#     "Unknown environment 'tikzpicture'";
#   - loi giai co dong "Ket qua la hinh anh ${...}$ (sau khi bo cap dau...)".
# Nay theo SGK hien hanh: MIEN NGHIEM LA PHAN KHONG BI GACH; bo d ve NET LIEN
# neu co dau bang (<=, >=), NET DUT neu khong. Phan bi gach la TOAN BO phan
# khung hinh nam o phia KHONG la nghiem (tinh dung da giac cat, khong uoc
# luong), khung hinh la hinh chu nhat chua hai truc Ox, Oy.
# ---------------------------------------------------------------------

def _cat_nua_mat_phang(da_giac, a, b, c, giu_lon_hon):
    """Cat da giac loi bang nua mat phang a x + b y >= c (giu_lon_hon) hoac <= c."""
    trong = (lambda p: a * p[0] + b * p[1] - c >= -1e-12) if giu_lon_hon else \
        (lambda p: a * p[0] + b * p[1] - c <= 1e-12)
    ra = []
    n = len(da_giac)
    for i in range(n):
        P, Q = da_giac[i], da_giac[(i + 1) % n]
        tp, tq = trong(P), trong(Q)
        if tp:
            ra.append(P)
        if tp != tq:
            fp = a * P[0] + b * P[1] - c
            fq = a * Q[0] + b * Q[1] - c
            t = fp / (fp - fq)
            ra.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return ra


def _doan_trong_khung(a, b, c, khung):
    """Hai dau mut cua duong a x + b y = c trong khung (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = khung
    diem = []
    if b != 0:
        for X in (x0, x1):
            Y = (c - a * X) / b
            if y0 - 1e-9 <= Y <= y1 + 1e-9:
                diem.append((X, Y))
    if a != 0:
        for Y in (y0, y1):
            X = (c - b * Y) / a
            if x0 - 1e-9 <= X <= x1 + 1e-9:
                diem.append((X, Y))
    duy_nhat = []
    for p in diem:
        if all(abs(p[0] - q[0]) > 1e-9 or abs(p[1] - q[1]) > 1e-9 for q in duy_nhat):
            duy_nhat.append(p)
    return duy_nhat[:2]


def _so_tikz(v):
    return ("%.3f" % v).rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else "%d" % round(v)


def _hinh_mien_nghiem(a, b, c, dau, khung, nhan_truc):
    r"""TikZ mien nghiem cua a x + b y (dau) c: GACH BO phan khong la nghiem.

    khung = (x0, x1, y0, y1) (so nguyen, chua goc O); nhan_truc: cac diem can
    ghi so tren truc [("x", 3), ("y", -2)...].
    """
    x0, x1, y0, y1 = khung
    hcn = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    # tap nghiem la a x + b y > c (dau > / >=) hoac < c; phan bi gach la phia con lai
    nghiem_lon = dau in (">", r"\ge")
    gach = _cat_nua_mat_phang(hcn, a, b, c, giu_lon_hon=not nghiem_lon)
    net = "" if dau in (r"\le", r"\ge") else "dashed,"
    doan = _doan_trong_khung(a, b, c, khung)
    s = [r"\begin{tikzpicture}[scale=0.5,font=\footnotesize,line join=round,>=stealth]"]
    if len(gach) >= 3:
        s.append(r"\fill[pattern=north east lines] " + " -- ".join(
            "(%s,%s)" % (_so_tikz(p[0]), _so_tikz(p[1])) for p in gach) + " -- cycle;")
    s.append(r"\draw[->] (%d,0)--(%s,0) node[below] {$x$};" % (x0, _so_tikz(x1 + 0.6)))
    s.append(r"\draw[->] (0,%d)--(0,%s) node[left] {$y$};" % (y0, _so_tikz(y1 + 0.6)))
    s.append(r"\node[below left,fill=white,inner sep=1pt] at (0,0) {$O$};")
    for truc, v in nhan_truc:
        if v == 0:
            continue
        if truc == "x":
            s.append(r"\draw (%d,0.12)--(%d,-0.12) node[below,fill=white,inner sep=1pt] {$%d$};" % (v, v, v))
        else:
            s.append(r"\draw (0.12,%d)--(-0.12,%d) node[left,fill=white,inner sep=1pt] {$%d$};" % (v, v, v))
    if len(doan) == 2:
        s.append(r"\draw[%sthick] (%s,%s)--(%s,%s);" % (net, _so_tikz(doan[0][0]), _so_tikz(doan[0][1]),
                                                         _so_tikz(doan[1][0]), _so_tikz(doan[1][1])))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def _dau_nguoc(d):
    return {">": "<", "<": ">", r"\ge": r"\le", r"\le": r"\ge"}[d]


def _dau_doi_net(d):
    return {">": r"\ge", r"\ge": ">", "<": r"\le", r"\le": "<"}[d]


def _cau_mien_nghiem(a, b, c, dau, khung, nhan, duong_sai, diem_thu, dang):
    """Ghep mot cau: 4 hinh (dung; sai phia; sai net; sai duong)."""
    bt = latex(a * x + b * y)
    dung = _hinh_mien_nghiem(a, b, c, dau, khung, nhan)
    a2, b2, c2, nhan2 = duong_sai
    nhieu = [_hinh_mien_nghiem(a, b, c, _dau_nguoc(dau), khung, nhan),
             _hinh_mien_nghiem(a, b, c, _dau_doi_net(dau), khung, nhan),
             _hinh_mien_nghiem(a2, b2, c2, dau, khung, nhan2)]
    X, Y = diem_thu
    vt = a * X + b * Y
    ok = {">": vt > c, "<": vt < c, r"\ge": vt >= c, r"\le": vt <= c}[dau]
    co_bang = dau in (r"\le", r"\ge")
    debai = (r"Hình nào dưới đây biểu diễn miền nghiệm của bất phương trình $%s %s %d$ "
             r"(miền nghiệm là phần \textbf{không bị gạch}%s)?"
             % (bt, dau, c, ", kể cả bờ nếu bờ vẽ nét liền" if co_bang else ""))
    giai = (r"Vẽ đường thẳng $d\colon %s = %d$ bằng nét %s (dấu $%s$ %s dấu bằng).\\ "
            r"Thay điểm $(%d; %d)$ (không nằm trên $d$) vào vế trái: $%d %s %d$ là %s.\\ "
            r"Vậy miền nghiệm là nửa mặt phẳng bờ $d$ %s điểm $(%d; %d)$ (%s bờ $d$); gạch bỏ nửa mặt phẳng còn lại. "
            r"Hình đúng là hình có bờ $d$ vẽ nét %s và phần không bị gạch %s điểm $(%d; %d)$."
            % (bt, c, "liền" if co_bang else "đứt", dau, "có" if co_bang else "không có",
               X, Y, vt, dau, c, "đúng" if ok else "sai",
               "chứa" if ok else "không chứa", X, Y, "kể cả" if co_bang else "không kể",
               "liền" if co_bang else "đứt", "chứa" if ok else "không chứa", X, Y))
    return MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)


def L10_C2_B3_TH024_MC_A_01(socau, dang=1):
    r"""Chọn hình biểu diễn miền nghiệm - bờ $d$ cắt hai trục tại $(p; 0)$, $(0; q)$.

    VIET LAI 30/09/2026 (xem ghi chu dau khoi). Kiem tra bang diem O(0;0).
    """
    cauTN = ""
    for _ in range(socau):
        p = int(np.random.choice([-4, -3, -2, -1, 1, 2, 3, 4]))
        q = int(np.random.choice([v for v in (-4, -3, -2, -1, 1, 2, 3, 4) if abs(v) != abs(p)]))
        k = int(np.random.choice([1, -1]))
        # x/p + y/q = 1  <=>  q x + p y = p q
        a, b, c = k * q, k * p, k * p * q
        dau = str(np.random.choice(["<", ">", r"\le", r"\ge"]))
        # CUNG MOT khung cho ca 4 hinh, phai chua ca giao diem (0; -q) cua duong sai
        khung = (min(0, p) - 2, max(0, p) + 2, -abs(q) - 1, abs(q) + 1)
        nhan = [("x", p), ("y", q)]
        # duong sai: doi dau giao diem voi Oy -> (p;0), (0;-q)
        duong_sai = (-k * q, k * p, -k * p * q, [("x", p), ("y", -q)])
        cauTN += _cau_mien_nghiem(a, b, c, dau, khung, nhan, duong_sai, (0, 0), dang)
    return cauTN


def L10_C2_B3_TH024_MC_A_02(socau, dang=1):
    r"""Chọn hình biểu diễn miền nghiệm - bờ $d$ song song trục toạ độ ($x \le a$,
    $y > b$, kể cả trục $Oy$, $Ox$) hoặc đi qua gốc $O$ (phải thử điểm khác $O$).

    VIET LAI 30/09/2026 (xem ghi chu dau khoi), theo cac cau "phan khong to va
    ca truc Oy la mien nghiem cua x <= 0" trong phan bai tap trac nghiem Bai 3.
    """
    cauTN = ""
    for _ in range(socau):
        kieu = int(np.random.randint(0, 3))
        dau = str(np.random.choice(["<", ">", r"\le", r"\ge"]))
        if kieu == 0:                       # x (dau) m
            m = int(np.random.randint(-3, 4))
            a, b, c = 1, 0, m
            khung = (-abs(m) - 2, abs(m) + 2, -2, 3)
            nhan = [("x", m), ("y", 2)]
            m2 = -m if m else 2
            duong_sai = (1, 0, m2, [("x", m2), ("y", 2)])
            diem = (m + 1, 0)
        elif kieu == 1:                     # y (dau) m
            m = int(np.random.randint(-3, 4))
            a, b, c = 0, 1, m
            khung = (-2, 3, -abs(m) - 2, abs(m) + 2)
            nhan = [("x", 2), ("y", m)]
            m2 = -m if m else 2
            duong_sai = (0, 1, m2, [("x", 2), ("y", m2)])
            diem = (0, m + 1)
        else:                               # a x + b y (dau) 0, bo qua O
            a = int(np.random.choice([-3, -2, -1, 1, 2, 3]))
            b = int(np.random.choice([-2, -1, 1, 2]))
            c = 0
            khung = (-3, 3, -3, 3)
            nhan = [("x", 1), ("y", 1)]
            duong_sai = (a, -b, 0, [("x", 1), ("y", 1)])
            diem = (1, 0) if a != 0 else (0, 1)
        cauTN += _cau_mien_nghiem(a, b, c, dau, khung, nhan, duong_sai, diem, dang)
    return cauTN

#print(K10_2_3_2_1_H(4,1))
#
# def K10_2_3_1_2_NB(): #DẠNG 1: nhận biết bpt, hệ bpt
#     with open(r"latex\data\de.tex", "a", encoding='utf-8') as de:
#         x = Symbol('x')
#         y = Symbol('y')
#         z = Symbol('z')
#
#         dau = np.choice(['>', '<', '\ge', '\le'])
#         mu0 = [2,3]
#         mu01 = np.choice(mu0)
#         mu0.remove(mu01)
#         mu02 = mu0[0]
#         bpt = []
#         for i in range(0,3):
#             k = np.randint(-10,10)
#             while (k == 0) or (k == 1) or (k == -1) or (k in bpt):
#                 k = np.randint(-10,10)
#             bpt.append(k)
#         d01 = dc.UCLN(bpt[0],bpt[1])
#         d02 = dc.UCLN(bpt[1],bpt[2])
#         if d01 > d02:
#             d0 = d01 / d02
#         elif d01 == d02:
#             d0 = d01
#         else:
#             d0 = d02 / d01
#         if dc.is_integer(d0) == True:
#             fx = [int(bpt[0]/d0), int(bpt[1]/d0), int(bpt[2]/d0)]
#         else:
#             fx = bpt
#
#         dau1 = np.choice(['>', '<', '\ge', '\le'])
#         mu1 = [2,3]
#         mu11 = np.choice(mu1)
#         bpt1 = []
#         for i in range(0,3):
#             k = np.randint(-10,10)
#             while (k == 0) or (k in bpt1):
#                 k = np.randint(-10,10)
#             bpt1.append(k)
#         d11 = dc.UCLN(bpt1[0],bpt1[1])
#         d12 = dc.UCLN(bpt1[1],bpt1[2])
#         if d11 > d12:
#             d1 = d11 / d12
#         elif d11 == d12:
#             d1 = d11
#         else:
#             d1 = d12 / d11
#         if dc.is_integer(d1) == True:
#             f1x = [int(bpt1[0]/d1), int(bpt1[1]/d1), int(bpt1[2]/d1)]
#         else:
#             f1x = bpt1
#
#         dau2 = np.choice(['>', '<', '\ge', '\le'])
#         bpt2 = []
#         for i in range(0,3):
#             k = np.randint(-10,10)
#             while (k == 0) or (k in bpt2):
#                 k = np.randint(-10,10)
#             bpt2.append(k)
#         d21 = dc.UCLN(bpt2[0],bpt2[1])
#         d22 = dc.UCLN(bpt2[1],bpt2[2])
#         if d21 > d22:
#             d2 = d21 / d22
#         elif d21 == d22:
#             d2 = d21
#         else:
#             d2 = d22 / d21
#         if dc.is_integer(d2) == True:
#             f2x = [int(bpt2[0]/d2), int(bpt2[1]/d2), int(bpt2[2]/d2)]
#         else:
#             f2x = bpt2
#
#
#         dau3 = np.choice(['>', '<', '\ge', '\le'])
#         f3x = []
#         for i in range(0,3):
#             k = np.randint(-10,10)
#             while (k == 0) or (k in f3x):
#                 k = np.randint(-10,10)
#             f3x.append(k)
#
#
#         de.write(r"\begin{ex}" + os.linesep)
#         de.write(r"Bất phương trình nào sau đây là bất phương trình bậc nhất hai ẩn?" + os.linesep)
#         de.write(r"\choice" + os.linesep)
#         de.write(r"{\True $%s^{%s} %s^{%s} y %s %s$}" %(fx[0], mu01, latex( x + fx[1]), mu02, dau, fx[2]) + os.linesep)
#         de.write(r"{$%s %s %s$}" %(latex(f1x[0] * x**mu11 + f1x[1] * y), dau1, f1x[2]) + os.linesep)
#         de.write(r"{$%s %s %s$}" %(latex(f2x[0] * x * y + f2x[1] * np.choice([x,y])), dau2, f2x[2]) + os.linesep)
#         de.write(r"{$%s %s %s$}" %(latex(f3x[0] * x + f3x[1] * y - z), dau3, f3x[2]) + os.linesep)
#         de.write(r"\loigiai{}" + os.linesep)
#         de.write(r"\end{ex}" + os.linesep)


# ---- Hinh nao bieu dien mien nghiem (bien the, co hinh) ----
# (tên cũ của cô: K10_2_3_2_1_TH)
#
# def K10_2_3_2_2_TH(): #DẠNG 2: miền nghiệm của bpt, hệ bpt
#     with open(r"latex\data\de.tex", "a", encoding='utf-8') as de:
#         x = Symbol('x')
#         y = Symbol('y')
#
#         dau1 = np.choice(['>', '<', '\ge', '\le'])
#         dau2 = np.choice(['>', '<', '\ge', '\le'])
#
#         point = [0,0,0]
#         while abs(point[0]) + abs(point[1]) < 3:
#             for i in range(0,3):
#                 k = np.randint(-4,4)
#                 while k == 0:
#                     k = np.randint(-4,4)
#                 point.pop(0)
#                 point.append(k)
#             while ((point[0] > 0) and (point[1] > 0) and (point[2] > 0)) or ((point[0] < 0) and (point[1] < 0) and (point[2] < 0)):
#                 point.pop(-1)
#                 k = np.randint(-4, 4)
#                 while k == 0:
#                     k = np.randint(-4, 4)
#                 point.append(k)
#             point.sort()
#
#         print('point: ', point[0], point[1], point[2])
#
#         choice = np.choice([0,1,2,3])
#         if choice == 0:
#             A = (point[0],0)
#             B = (0,point[1])
#             C = (point[2],0)
#             x_trai = point[0] - 1
#             x_phai = point[2] + 1
#             if point[1] < 0:
#                 y_duoi = point[1] - 1
#                 y_tren = 1
#             else:
#                 y_tren = point[1] + 1
#                 y_duoi = - 1
#
#         elif choice == 1:
#             A = (point[0],0)
#             B = (0,-point[1])
#             C = (point[2],0)
#             x_trai = point[0] - 1
#             x_phai = point[2] + 1
#             if -point[1] < 0:
#                 y_duoi = -point[1] - 1
#                 y_tren = 1
#             else:
#                 y_tren = -point[1] + 1
#                 y_duoi = - 1
#         elif choice == 2:
#             A = (0,point[0])
#             B = (point[1],0)
#             C = (0,point[2])
#             y_duoi = point[0] - 1
#             y_tren = point[2] + 1
#             if point[1] < 0:
#                 x_trai = point[1] - 1
#                 x_phai = 1
#             else:
#                 x_phai = point[1] + 1
#                 x_trai = - 1
#         else:
#             A = (0,point[0])
#             B = (-point[1],0)
#             C = (0,point[2])
#             y_duoi = point[0] - 1
#             y_tren = point[2] + 1
#             if -point[1] < 0:
#                 x_trai = -point[1] - 1
#                 x_phai = 1
#             else:
#                 x_phai = - point[1] + 1
#                 x_trai = - 1
#         print('x_trai, x_phai, y_duoi, y_tren: ', x_trai, x_phai, y_duoi, y_tren)
#         print('A', A, 'B', B, 'C', C)
#
#         AB = [-B[1]+A[1],B[0]-A[0]] # vecto pháp tuyến của AB
#         #phuong trình đường thẳng AB : y = -(AB[0]/AB[1]) * x + (AB[0]/AB[1]) * A[0] + A[1]
#         BC = [-C[1]+B[1],C[0]-B[0]]# vecto pháp tuyến của BC
#         #phuong trình đường thẳng BC : y = -(BC[0]/BC[1]) * x + (BC[0]/BC[1]) * B[0] + B[1]
#
#         #bất phương trình liên quan đường thẳng AB
#         fx = lambda x, y: AB[0] * x + AB[1] * y
#         c = AB[0] * A[0] + AB[1] * A[1]
#
#         #bất phương trình liên quan đường thẳng BC
#         gx = lambda x, y: BC[0] * x + BC[1] * y
#         d = BC[0] * C[0] + BC[1] * C[1]
#
#         ### tìm x_bien, y_bien để vẽ miền nghiệm cua fx
#         if (((dau1 == '>') or (dau1 == '\ge')) and (fx(0,0) > c)) or ((dau1 == '<') or (dau1 == '\le')) and (fx(0,0) < c):
#             if (choice == 0) or (choice == 1):
#                 if B[1] > 0:
#                     x_bien = x_trai - 1
#                     y_bien = y_tren + 1
#                 else:
#                     x_bien = x_trai - 1
#                     y_bien = y_duoi - 1
#             else:
#                 if B[0] > 0:
#                     x_bien = x_phai + 1
#                     y_bien = y_duoi - 1
#                 else:
#                     x_bien = x_trai - 1
#                     y_bien = y_duoi - 1
#         elif (((dau1 == '>') or (dau1 == '\ge')) and (fx(0,0) < c)) or ((dau1 == '<') or (dau1 == '\le')) and (fx(0,0) > c):
#             if (choice == 0) or (choice == 1):
#                 if B[1] > 0:
#                     x_bien = x_phai + 1
#                     y_bien = y_duoi - 1
#                 else:
#                     x_bien = x_phai + 1
#                     y_bien = y_tren + 1
#             else:
#                 if B[0] > 0:
#                     x_bien = x_trai - 1
#                     y_bien = y_tren + 1
#                 else:
#                     x_bien = x_phai + 1
#                     y_bien = y_tren + 1
#
#         ### tìm x_bien, y_bien để vẽ miền nghiệm cua gx
#         if (((dau2 == '>') or (dau2 == '\ge')) and (gx(0,0) > d)) or ((dau2 == '<') or (dau2 == '\le')) and (gx(0,0) < d):
#             if (choice == 0) or (choice == 1):
#                 if B[1] > 0:
#                     x_bien_1 = x_phai + 1
#                     y_bien_1 = y_tren + 1
#                 else:
#                     x_bien_1 = x_phai + 1
#                     y_bien_1 = y_duoi - 1
#             else:
#                 if B[0] > 0:
#                     x_bien_1 = x_phai + 1
#                     y_bien_1 = y_tren + 1
#                 else:
#                     x_bien_1 = x_trai - 1
#                     y_bien_1 = y_tren + 1
#         elif (((dau2 == '>') or (dau2 == '\ge')) and (gx(0,0) < d)) or ((dau2 == '<') or (dau2 == '\le')) and (gx(0,0) > d):
#             if (choice == 0) or (choice == 1):
#                 if B[1] > 0:
#                     x_bien_1 = x_trai - 1
#                     y_bien_1 = y_duoi - 1
#                 else:
#                     x_bien_1 = x_trai - 1
#                     y_bien_1 = y_tren + 1
#             else:
#                 if B[0] > 0:
#                     x_bien_1 = x_trai - 1
#                     y_bien_1 = y_duoi - 1
#                 else:
#                     x_bien_1 = x_phai + 1
#                     y_bien_1 = y_duoi - 1
#
#         if dau1 == '>':
#             dau11 = '<'
#         elif dau1 == '<':
#             dau11 = '>'
#         elif dau1 == '\ge':
#             dau11 = '\le'
#         else:
#             dau11 = '\ge'
#
#         if dau2 == '>':
#             dau21 = '<'
#         elif dau2 == '<':
#             dau21 = '>'
#         elif dau2 == '\ge':
#             dau21 = '\le'
#         else:
#             dau21 = '\ge'
#
#         de.write(r"\begin{ex}" + os.linesep)
#         de.write(r"\immini{Hình bên là biểu diễn miền nghiệm của hệ bất phương trình nào sau đây?" + os.linesep)
#         de.write(r"\choice" + os.linesep)
#         de.write(r"{\True $\heva{& %s %s %s \\& %s %s %s}$}" %(latex(AB[0] * x + AB[1] * y), dau1, c, latex(BC[0] * x + BC[1] * y), dau2, d) + os.linesep)
#         de.write(r"{$\heva{& %s %s %s \\& %s %s %s}$}" %(latex(AB[0] * x + AB[1] * y), dau1, c, latex(BC[0] * x + BC[1] * y), dau21, d) + os.linesep)
#         de.write(r"{$\heva{& %s %s %s \\& %s %s %s}$}" %(latex(AB[0] * x + AB[1] * y), dau11, c, latex(BC[0] * x + BC[1] * y), dau2, d) + os.linesep)
#         de.write(r"{$\heva{& %s %s %s \\& %s %s %s}$}" %(latex(AB[0] * x + AB[1] * y), dau11, c, latex(BC[0] * x + BC[1] * y), dau21, d) + os.linesep)
#         de.write(r"}{" + os.linesep)
#         de.write(r"\begin{tikzpicture}[scale=.7]" + os.linesep)
#         de.write(r"\draw[->] (%s,0)--(%s,0) node[below right] {$x$};" %(x_trai - 0.7, x_phai + 0.7) + os.linesep)
#         de.write(r"\draw[->] (0,%s)--(0,%s) node[right] {$y$};" %(y_duoi - 0.7, y_tren + 0.7) + os.linesep)
#         de.write(r"\node (0,0) [below left] {$ O $};" + os.linesep)
#         if (choice == 0) or (choice == 1):
#             de.write(r"\node at  (%s,0) [below left] {$ %s $};" %(A[0], A[0]) + os.linesep)
#             de.write(r"\node at (%s,0) [below left] {$ %s $};" %(C[0], C[0]) + os.linesep)
#             de.write(r"\node at (0,%s) [above right] {$ %s $};" %(B[1], B[1]) + os.linesep)
#         else:
#             de.write(r"\node at (0,%s) [above right] {$ %s $};" %(A[1], A[1]) + os.linesep)
#             de.write(r"\node at (0,%s) [above right] {$ %s $};" %(C[1], C[1]) + os.linesep)
#             de.write(r"\node at (%s,0) [below left] {$ %s $};" %(B[0], B[0]) + os.linesep)
#         de.write(r"\clip (%s,%s) rectangle (%s,%s);" %(x_trai - 0.5, y_duoi - 0.5, x_phai + 0.5, y_tren + 0.5) + os.linesep)
#         de.write(r"\foreach \x in {%s,%s,...,%s}" %(x_trai, x_trai + 1, x_phai) + os.linesep)
#         de.write(r"\draw[shift={(\x,0)},color=black] (0pt,2pt) -- (0pt,-2pt);" + os.linesep)
#         de.write(r"\foreach \y in {%s,%s,...,%s}" %(y_duoi, y_duoi + 1, y_tren) + os.linesep)
#         de.write(r"\draw[shift={(0,\y)},color=black] (2pt,0pt) -- (-2pt,0pt);" + os.linesep)
#         if (dau1 == '<') or (dau1 == '>'):
#             de.write(r"\draw [dashed, thick, domain=%s:%s, samples=100] plot (\x, {(%s)*\x + %s});" %(x_trai-1, x_phai+1, -(AB[0]/AB[1]), (AB[0]/AB[1]) * A[0] + A[1]) + os.linesep)
#         else:
#             de.write(r"\draw [thick, domain=%s:%s, samples=100] plot (\x, {(%s)*\x + %s});" %(x_trai-1, x_phai+1, -(AB[0]/AB[1]), (AB[0]/AB[1]) * A[0] + A[1]) + os.linesep)
#         de.write(r"\fill[pattern=north east lines,opacity=.7] plot (\x, {(%s)*\x + %s}) |- (%s,%s);" %(-(AB[0]/AB[1]), (AB[0]/AB[1]) * A[0] + A[1], x_bien, y_bien) + os.linesep)
#
#         if (dau2 == '<') or (dau2 == '>'):
#             de.write(
#                 r"\draw [dashed, thick, domain=%s:%s, samples=100] plot (\x, {(%s)*\x + %s});" % (
#                 x_trai - 1, x_phai + 1, -(BC[0] / BC[1]), (BC[0] / BC[1]) * B[0] + B[1]) + os.linesep)
#         else:
#             de.write(r"\draw [thick, domain=%s:%s, samples=100] plot (\x, {(%s)*\x + %s});" % (
#             x_trai - 1, x_phai + 1, -(BC[0] / BC[1]), (BC[0] / BC[1]) * B[0] + B[1]) + os.linesep)
#         de.write(r"\fill[pattern=north east lines,opacity=.7] plot (\x, {(%s)*\x + %s}) |- (%s,%s);" %(-(BC[0]/BC[1]), (BC[0]/BC[1]) * B[0] + B[1], x_bien_1, y_bien_1) + os.linesep)
#         de.write(r"\end{tikzpicture}}" + os.linesep)
#         de.write(r"\loigiai{}" + os.linesep)
#         de.write(r"\end{ex}" + os.linesep)
#


# ---- Hinh cho truoc la mien nghiem cua he nao (co hinh) ----
# (tên cũ của cô: K10_2_3_2_2_TH)
def L10_C2_B4_TH027_MC_A_01(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        dau1 = np.random.choice(['>', '<', '\\ge', '\\le'])
        dau2 = np.random.choice(['>', '<', '\\ge', '\\le'])

        point = [0, 0, 0]
        while abs(point[0]) + abs(point[1]) < 3:
            for i in range(3):
                k = np.random.randint(-4, 5)
                while k == 0:
                    k = np.random.randint(-4, 5)
                point.pop(0)
                point.append(k)
            while ((point[0] > 0) and (point[1] > 0) and (point[2] > 0)) or (
                    (point[0] < 0) and (point[1] < 0) and (point[2] < 0)):
                point.pop(-1)
                k = np.random.randint(-4, 5)
                while k == 0:
                    k = np.random.randint(-4, 5)
                point.append(k)
            point.sort()

        choice = np.random.choice([0, 1, 2, 3])
        if choice == 0:
            A = (point[0], 0)
            B = (0, point[1])
            C = (point[2], 0)
            x_trai = point[0] - 1
            x_phai = point[2] + 1
            if point[1] < 0:
                y_duoi = point[1] - 1
                y_tren = 1
            else:
                y_tren = point[1] + 1
                y_duoi = -1
        elif choice == 1:
            A = (point[0], 0)
            B = (0, -point[1])
            C = (point[2], 0)
            x_trai = point[0] - 1
            x_phai = point[2] + 1
            if -point[1] < 0:
                y_duoi = -point[1] - 1
                y_tren = 1
            else:
                y_tren = -point[1] + 1
                y_duoi = -1
        elif choice == 2:
            A = (0, point[0])
            B = (point[1], 0)
            C = (0, point[2])
            y_duoi = point[0] - 1
            y_tren = point[2] + 1
            if point[1] < 0:
                x_trai = point[1] - 1
                x_phai = 1
            else:
                x_phai = point[1] + 1
                x_trai = -1
        else:
            A = (0, point[0])
            B = (-point[1], 0)
            C = (0, point[2])
            y_duoi = point[0] - 1
            y_tren = point[2] + 1
            if -point[1] < 0:
                x_trai = -point[1] - 1
                x_phai = 1
            else:
                x_phai = -point[1] + 1
                x_trai = -1

        AB = [-B[1] + A[1], B[0] - A[0]]
        BC = [-C[1] + B[1], C[0] - B[0]]

        fx = lambda x_val, y_val: AB[0] * x_val + AB[1] * y_val
        c = AB[0] * A[0] + AB[1] * A[1]

        gx = lambda x_val, y_val: BC[0] * x_val + BC[1] * y_val
        d = BC[0] * C[0] + BC[1] * C[1]

        # Tìm tọa độ x_bien, y_bien cho miền nghiệm của fx
        if (((dau1 == '>') or (dau1 == '\\ge')) and (fx(0, 0) > c)) or ((dau1 == '<') or (dau1 == '\\le')) and (
                fx(0, 0) < c):
            if (choice == 0) or (choice == 1):
                x_bien, y_bien = (x_trai - 1, y_tren + 1) if B[1] > 0 else (x_trai - 1, y_duoi - 1)
            else:
                x_bien, y_bien = (x_phai + 1, y_duoi - 1) if B[0] > 0 else (x_trai - 1, y_duoi - 1)
        else:
            if (choice == 0) or (choice == 1):
                x_bien, y_bien = (x_phai + 1, y_duoi - 1) if B[1] > 0 else (x_phai + 1, y_tren + 1)
            else:
                x_bien, y_bien = (x_trai - 1, y_tren + 1) if B[0] > 0 else (x_phai + 1, y_tren + 1)

        # Tìm tọa độ x_bien_1, y_bien_1 cho miền nghiệm của gx
        if (((dau2 == '>') or (dau2 == '\\ge')) and (gx(0, 0) > d)) or ((dau2 == '<') or (dau2 == '\\le')) and (
                gx(0, 0) < d):
            if (choice == 0) or (choice == 1):
                x_bien_1, y_bien_1 = (x_phai + 1, y_tren + 1) if B[1] > 0 else (x_phai + 1, y_duoi - 1)
            else:
                x_bien_1, y_bien_1 = (x_phai + 1, y_tren + 1) if B[0] > 0 else (x_trai - 1, y_tren + 1)
        else:
            if (choice == 0) or (choice == 1):
                x_bien_1, y_bien_1 = (x_trai - 1, y_duoi - 1) if B[1] > 0 else (x_trai - 1, y_tren + 1)
            else:
                x_bien_1, y_bien_1 = (x_trai - 1, y_duoi - 1) if B[0] > 0 else (x_phai + 1, y_duoi - 1)

        # Đảo dấu phục vụ tạo phương án nhiễu
        dau_dao = {'>': '<', '<': '>', '\\ge': '\\le', '\\le': '\\ge'}
        dau11 = dau_dao[dau1]
        dau21 = dau_dao[dau2]

        v = [AB, BC, dau1, dau2, dau11, dau21, c, d, choice, A, B, C, x_trai, x_phai, y_duoi, y_tren, x_bien, y_bien,
             x_bien_1, y_bien_1]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        AB, BC, dau1, dau2, dau11, dau21, c, d, choice, A, B, C, x_trai, x_phai, y_duoi, y_tren, x_bien, y_bien, x_bien_1, y_bien_1 = v

        # Thiết lập các nhãn node cho hệ tọa độ
        if (choice == 0) or (choice == 1):
            label_nodes = f"""\\node at ({A[0]},0) [below left] {{ $ {A[0]} $ }};
            \\node at ({C[0]},0) [below left] {{ $ {C[0]} $ }};
            \\node at (0,{B[1]}) [above right] {{ $ {B[1]} $ }};"""
        else:
            label_nodes = f"""\\node at (0,{A[1]}) [above right] {{ $ {A[1]} $ }};
            \\node at (0,{C[1]}) [above right] {{ $ {C[1]} $ }};
            \\node at ({B[0]},0) [below left] {{ $ {B[0]} $ }};"""

        line_style1 = "dashed, thick" if (dau1 == '<' or dau1 == '>') else "thick"
        line_style2 = "dashed, thick" if (dau2 == '<' or dau2 == '>') else "thick"

        # Đồ thị dùng để đưa vào tham số dothi_de của hàm sinh câu hỏi
        dothi_de = f"""\\begin{{tikzpicture}}[scale=.7]
        \\draw[->] ({x_trai - 0.7},0)--({x_phai + 0.7},0) node[below right] {{$x$}};
        \\draw[->] (0,{y_duoi - 0.7})--(0,{y_tren + 0.7}) node[right] {{$y$}};
        \\node (0,0) [below left] {{$ O $}};
        {label_nodes}
        \\clip ({x_trai - 0.5},{y_duoi - 0.5}) rectangle ({x_phai + 0.5},{y_tren + 0.5});
        \\foreach \\x in {{{x_trai},{x_trai + 1},...,{x_phai}}} \\draw[shift={{(\\x,0)}},color=black] (0pt,2pt) -- (0pt,-2pt);
        \\foreach \\y in {{{y_duoi},{y_duoi + 1},...,{y_tren}}} \\draw[shift={{(0,\\y)}},color=black] (2pt,0pt) -- (-2pt,0pt);
        \\draw [{line_style1}, domain={x_trai - 1}:{x_phai + 1}, samples=100] plot (\\x, {{({-(AB[0] / AB[1])})*\\x + {(AB[0] / AB[1]) * A[0] + A[1]}}});
        \\fill[pattern=north east lines,opacity=.7] plot (\\x, {{({-(AB[0] / AB[1])})*\\x + {(AB[0] / AB[1]) * A[0] + A[1]}}}) |- ({x_bien},{y_bien});
        \\draw [{line_style2}, domain={x_trai - 1}:{x_phai + 1}, samples=100] plot (\\x, {{({-(BC[0] / BC[1])})*\\x + {(BC[0] / BC[1]) * B[0] + B[1]}}});
        \\fill[pattern=north east lines,opacity=.7] plot (\\x, {{({-(BC[0] / BC[1])})*\\x + {(BC[0] / BC[1]) * B[0] + B[1]}}}) |- ({x_bien_1},{y_bien_1});
        \\end{{tikzpicture}}"""

        # Định dạng chuỗi hiển thị công thức toán dạng kí tự (Sử dụng MC_SA_answer_text)
        dapso = f"$\\heva{{& {latex(AB[0] * x + AB[1] * y)} {dau1} {c} \\\\& {latex(BC[0] * x + BC[1] * y)} {dau2} {d}}}$"
        nhieu1 = f"$\\heva{{& {latex(AB[0] * x + AB[1] * y)} {dau1} {c} \\\\& {latex(BC[0] * x + BC[1] * y)} {dau21} {d}}}$"
        nhieu2 = f"$\\heva{{& {latex(AB[0] * x + AB[1] * y)} {dau11} {c} \\\\& {latex(BC[0] * x + BC[1] * y)} {dau2} {d}}}$"
        nhieu3 = f"$\\heva{{& {latex(AB[0] * x + AB[1] * y)} {dau11} {c} \\\\& {latex(BC[0] * x + BC[1] * y)} {dau21} {d}}}$"

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        debai = "Hình bên là biểu diễn miền nghiệm của hệ bất phương trình nào sau đây?"

        giai = f"""
        Dựa vào hình vẽ ta thấy miền nghiệm được giới hạn bởi hai đường thẳng:\\\\
        $d_1: {latex(AB[0] * x + AB[1] * y)} = {c}$ và $d_2: {latex(BC[0] * x + BC[1] * y)} = {d}$.\\\\
        Thử nghiệm với tọa độ điểm không bị gạch hoặc điểm gốc tọa độ $O(0;0)$, ta chọn được hệ bất phương trình tương ứng chính xác là:\\\\
        $\\heva{{& {latex(AB[0] * x + AB[1] * y)} {dau1} {c} \\\\& {latex(BC[0] * x + BC[1] * y)} {dau2} {d}}}$.
        """

        # Sử dụng MC_SA_answer_text do cấu trúc \heva và ký hiệu toán học thủ công đã bọc sẵn $...$
        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, dothi_de, 0, dang)

    return cauTN


# Hàm tính PTTQ đường thẳng đi qua A(x1, y1) và B(x2, y2)
# Trả về [a, b, c] với ax + by + c = 0


# ---- Mien nghiem cua he la da giac gi (tam giac, tu giac, ngu giac...) ----
# (tên cũ của cô: K10_2_3_3_2_VD)
def L10_C2_B4_TH027_MC_B_01(socau, dang=1):
    # CLAUDE SUA 07/10/2026 (co Lan duyet): ban cu chi cho dap an tam giac / ngu giac
    # (M, N luon nam tren hai canh KE NHAU nen khong bao gio ra tu giac).
    # Ban moi chon truoc dang da giac (tam / tu / ngu, moi dang 1/3):
    #   tu giac -> M, N tren hai canh DOI cua hinh chu nhat;
    #   tam giac, ngu giac -> M, N tren hai canh KE nhau, lay phia co 1 hoac 3 dinh.
    # Loi giai neu ro toa do M, N va thay tung dinh vao ve trai.
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        x_center = np.random.randint(-2, 3)
        y_center = np.random.randint(-2, 3)

        K = [np.random.randint(0, 6) for _ in range(4)]

        while K[0] + K[3] <= 5:
            K[0] = np.random.randint(0, 11)
            K[3] = np.random.randint(0, 11)

        while K[1] + K[2] <= 5:
            K[1] = np.random.randint(0, 11)
            K[2] = np.random.randint(0, 11)

        A = [x_center - K[0], y_center + K[1]]
        B = [x_center - K[0], y_center - K[2]]
        C = [x_center + K[3], y_center - K[2]]
        D = [x_center + K[3], y_center + K[1]]

        fx = x_center - K[0]
        gx = x_center + K[3]
        hx = y_center - K[2]
        kx = y_center + K[1]

        hinh = str(np.random.choice(['tam', 'tu', 'ngu']))
        if hinh == 'tu':
            if np.random.rand() < 0.5:
                # hai canh doi nam ngang: M tren canh tren, N tren canh duoi
                xa = int(np.random.randint(fx + 1, gx))
                xb = int(np.random.randint(fx + 1, gx))
                while xb == xa:
                    xb = int(np.random.randint(fx + 1, gx))
                M = [xa, kx]
                N = [xb, hx]
            else:
                # hai canh doi thang dung: M tren canh trai, N tren canh phai
                ya = int(np.random.randint(hx + 1, kx))
                yb = int(np.random.randint(hx + 1, kx))
                while yb == ya:
                    yb = int(np.random.randint(hx + 1, kx))
                M = [fx, ya]
                N = [gx, yb]
        else:
            # hai canh ke nhau: M tren canh ngang, N tren canh dung
            M = [int(np.random.randint(fx + 1, gx)), int(np.random.choice([hx, kx]))]
            N = [int(np.random.choice([fx, gx])), int(np.random.randint(hx + 1, kx))]

        # Vectơ chỉ phương MN = (x_N - x_M, y_N - y_M) -> VTPT = (-(y_N - y_M), x_N - x_M)
        a_MN = -(N[1] - M[1])
        b_MN = N[0] - M[0]
        c_MN = -(a_MN * M[0] + b_MN * M[1])

        # Tối giản hệ số bằng ước chung lớn nhất
        d_gcd = math.gcd(math.gcd(a_MN, b_MN), c_MN)
        if d_gcd > 0:
            a_MN //= d_gcd
            b_MN //= d_gcd
            c_MN //= d_gcd

        MN_func = lambda x_val, y_val: a_MN * x_val + b_MN * y_val + c_MN
        VT_MN = a_MN * x + b_MN * y
        VP_MN = -c_MN

        dinh = list(zip(['A', 'B', 'C', 'D'], [A, B, C, D]))
        gia_tri = [(ten, p, a_MN * p[0] + b_MN * p[1]) for ten, p in dinh]
        Duong = [t for t, p, g in gia_tri if g > VP_MN]
        Am = [t for t, p, g in gia_tri if g < VP_MN]
        if len(Duong) + len(Am) != 4:       # duong thang di qua dinh -> bo
            continue

        so_dinh = {'tam': 1, 'tu': 2, 'ngu': 3}[hinh]
        if len(Duong) == so_dinh and len(Am) == so_dinh:
            chon_duong = bool(np.random.rand() < 0.5)
        elif len(Duong) == so_dinh:
            chon_duong = True
        elif len(Am) == so_dinh:
            chon_duong = False
        else:
            continue

        dau = '\\ge' if chon_duong else '\\le'
        trong = Duong if chon_duong else Am
        mien = {1: 'Miền tam giác', 2: 'Miền tứ giác', 3: 'Miền ngũ giác'}[so_dinh]
        Mien_list = ['Miền tam giác', 'Miền tứ giác', 'Miền ngũ giác', 'Miền lục giác']
        Mien_list.remove(mien)

        # Loi giai: neu ro hinh chu nhat, hai giao diem M, N, roi thay tung dinh vao ve trai
        cac_dong = []
        for ten, p, g in gia_tri:
            thoa = (g >= VP_MN) if chon_duong else (g <= VP_MN)
            ket = "đúng" if thoa else "sai"
            cac_dong.append(
                f"${ten}\\left({p[0]};{p[1]}\\right)$: ${g} {dau} {VP_MN}$ {ket}")
        so_canh = so_dinh + 2
        giai = (
            f"Các bất phương trình ${fx} \\le x \\le {gx}$ và ${hx} \\le y \\le {kx}$ xác định "
            f"hình chữ nhật $ABCD$ với $A\\left({A[0]};{A[1]}\\right)$, $B\\left({B[0]};{B[1]}\\right)$, "
            f"$C\\left({C[0]};{C[1]}\\right)$, $D\\left({D[0]};{D[1]}\\right)$.\\\\ "
            f"Đường thẳng $d \\colon {latex(VT_MN)} = {VP_MN}$ cắt hình chữ nhật tại "
            f"$M\\left({M[0]};{M[1]}\\right)$ và $N\\left({N[0]};{N[1]}\\right)$.\\\\ "
            f"Thay toạ độ các đỉnh vào vế trái ${latex(VT_MN)}$ và so với ${VP_MN}$:\\\\ "
            + "; ".join(cac_dong) + ".\\\\ "
            f"Có ${so_dinh}$ đỉnh của hình chữ nhật thoả mãn ({', '.join(trong)}) nên miền nghiệm "
            f"là đa giác có các đỉnh là {so_dinh} đỉnh đó cùng hai điểm $M$, $N$, "
            f"tức là đa giác có ${so_canh}$ đỉnh: \\textbf{{{mien.lower()}}}."
        )

        v = [fx, gx, hx, kx, VT_MN, dau, VP_MN, mien, Mien_list, giai]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        fx, gx, hx, kx, VT_MN, dau, VP_MN, mien, Mien_list, giai = v

        debai = f"Miền nghiệm của hệ bất phương trình $\\heva{{& {fx} \\le x \\le {gx} \\\\ & {hx} \\le y \\le {kx} \\\\ & {latex(VT_MN)} {dau} {VP_MN} }}$ là"

        dapso = mien
        dsnhieu = [Mien_list[0], Mien_list[1], Mien_list[2]]

        # PHAI dung MC_SA_answer_text: dap an la CHU tieng Viet.
        # MC_SA_answer_const boc moi phuong an trong $...$, nen
        # "Mien ngu giac" bi doc nhu cong thuc -> mat het dau cach va in
        # nghieng: "Mienngugiac". Co Lan bat duoc tren web 29/09/2026.
        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

#
# def K10_2_4_1_1_VDC_TL(): #tự luận
#     with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
#         x = Symbol('x')
#         y = Symbol('y')
#         k = np.randint(13,17)
#         nguoi = k * 10 # số người cách nhau 10
#         hang = (k - 13) * 1.5 + 7.5 # số hàng cách nhau 1.5 tấn
#         dt1 = 20 * x + 10 * y - nguoi
#         dt2 = 0.6 * x + 1.5 * y - hang
#
#         S_A = solve([dt1, dt2], [x, y])
#         A = 10 # số xe A có
#         if S_A[x] % 2 == 1:
#             B = np.choice([4,6,8]) + int(S_A[x])  # Số xe B có (phải là số lẻ mới ra số đẹp)
#         else:
#             B = np.choice([3,5,7]) + int(S_A[x])
#         S_B = solve([x - A, dt2], [x, y])
#         S_C = solve([x - A, y - B], [x, y])
#         S_D = solve([dt1, y - B], [x, y])
#
#         giatien_A = np.randint(3,5)
#         giatien_B = giatien_A - 1
#         F = lambda x,y: giatien_A * x + giatien_B * y
#         F_tong = [F(S_A[x], S_A[y]), F(S_B[x], S_B[y]), F(S_C[x], S_C[y]), F(S_D[x], S_D[y])]
#         F_tong.sort()
#         if F(S_A[x], S_A[y]) == F_tong[0]:
#             diem_x = S_A[x]
#             diem_y = S_A[y]
#         elif F(S_B[x], S_B[y]) == F_tong[0]:
#             diem_x = S_B[x]
#             diem_y = S_B[y]
#         elif F(S_C[x], S_C[y]) == F_tong[0]:
#             diem_x = S_C[x]
#             diem_y = S_C[y]
#         else:
#             diem_x = S_D[x]
#             diem_y = S_D[y]
#
#         # chuyển số thập phân qua biểu thị chuỗi và có dấu là ,
#         if dc.KiemTraSoNguyen(hang) == True:
#             hang_string = int(hang)
#         else:
#             hang_string = str(hang).replace('.', ',')
#
#         def convert_to_string(value):
#             if dc.KiemTraSoNguyen(value):
#                 return str(int(round(value)))
#             else:
#                 # Chuyển đổi thành chuỗi và loại bỏ các số 0 không cần thiết sau dấu thập phân
#                 string_value = str(value).rstrip('0').rstrip('.')
#                 # Thay thế dấu '.' bằng dấu ','
#                 return string_value.replace('.', ',')
#
#         SAx_string = convert_to_string(S_A[x])
#         SBx_string = convert_to_string(S_B[x])
#         SCx_string = convert_to_string(S_C[x])
#         SDx_string = convert_to_string(S_D[x])
#         SAy_string = convert_to_string(S_A[y])
#         SBy_string = convert_to_string(S_B[y])
#         SCy_string = convert_to_string(S_C[y])
#         SDy_string = convert_to_string(S_D[y])
#         SA_string = convert_to_string(F(S_A[x], S_A[y]))
#         SB_string = convert_to_string(F(S_B[x], S_B[y]))
#         SC_string = convert_to_string(F(S_C[x], S_C[y]))
#         SD_string = convert_to_string(F(S_D[x], S_D[y]))
#
#         de.write(r"\begin{ex}"+ os.linesep)
#         de.write(r"[0,5 điểm]" + os.linesep)
#         de.write(r"Một công ty cần thuê xe để chở $ %s $ người và $ %s $ tấn hàng. Nơi thuê xe có hai loại xe $ A $ và $ B $, "
#                  r"trong đó loại xe $ A $ có $ %s $ chiếc và loại xe $ B $ có $ %s $ chiếc. "
#                  r"Một chiếc xe loại $ A $ cho thuê với giá $ %s $ triệu đồng, một chiếc xe loại $ B $ cho thuê với giá $ %s $ triệu đồng. "
#                  r"Biết rằng mỗi xe loại $ A $ có thể chở tối đa $ 20 $ người và $ 0,6 $ tấn hàng; mỗi xe loại $ B $ có thể chở tối đa $ 10 $ người và $ 1,5 $ tấn hàng. "
#                  r"Hỏi phải thuê bao nhiêu xe mỗi loại để chi phí bỏ ra là ít nhất?"
#                  %(nguoi, hang_string, A, B, giatien_A, giatien_B)+ os.linesep)
#         de.write(r"\loigiai{"+ os.linesep)
#         de.write(r"Gọi $ x, y $ lần lượt  là số xe loại $ A $ và $ B $. Khi đó số tiền cần bỏ ra để thuê xe là $ f(x;y)= %s x + %s y. $\\" %(giatien_A, giatien_B) + os.linesep)
#         de.write(r"Ta có $ x $ xe loại $ A $ sẽ chở được $ 20x $ người và $ 0,6x $ tấn hàng; $ y $ xe loại $ B $ sẽ chở được $ 10y $ người và $ 1,5y $ tấn hàng. "
#                  r"Suy ra $ x $ xe loại $ A $ và $ y $ xe loại $ B $ sẽ chở được $ 20x+10y $ người và $ 0,6x+1,5y $ tấn hàng.\\"+ os.linesep)
#         de.write(r"Ta có hệ bất phương trình sau $ \heva{&20x+10y\ge %s \\&0,6x+1,5y\ge %s \\&0\le x\le %s \\& 0\le y\le %s }$\\"
#                  %(nguoi, hang_string, A, B) + os.linesep)
#         de.write(f"Bài toán trở thành tìm giá trị nhỏ nhất của hàm số $ f(x;y) $ trên miền nghiệm của hệ $ (*) $. "
#                  f"Miền nghiệm của hệ $ (*) $ là tứ giác $ ABCD $ (kể cả biên)."
#                  f"Hàm số $ f(x;y)= {giatien_A}x + {giatien_B}y $ sẽ đạt giá trị nhỏ nhất trên miền nghiệm của hệ bất phương trình $ (*) $ khi $ (x;y) $ là tọa độ của một trong các đỉnh "
#                  f"$ A({SAx_string} ; {SAy_string}) $, $B({SBx_string} ; {SBy_string})  $, $ C({SCx_string} ; {SCy_string}) $, $ D\\left({SDx_string} ; {SDy_string}\\right). $\\"
#                  + os.linesep)
#         de.write(
#             f"Ta có: $ f({SAx_string} ; {SAy_string})= {SA_string}; f({SBx_string} ; {SBy_string})= {SB_string}; f({SCx_string} ; {SCy_string})= {SC_string}; f\\left({SDx_string} ; {SDy_string}\\right)= {SD_string}. $\\"
#             + os.linesep)
#
#         de.write(r"Suy ra $ f(x;y) $ nhỏ nhất khi $ (x;y)=(%s ; %s)$. Như vậy để chi phí vận chuyển thấp nhất cần thuê $ %s $ xe loại $ A $ và $ %s $ xe loại $ B$." %(int(diem_x), int(diem_y), int(diem_x), int(diem_y)) + os.linesep)
#         de.write(r"\begin{center}"+ os.linesep)
#         de.write(r"\begin{tikzpicture}[line width=1pt,>=stealth,x=1cm,y=1cm,scale=0.5]"+ os.linesep)
#         de.write(r"\draw[->] (-1,0)--(%s,0) node[below]{\footnotesize $ x $};" %(A + 2.2) + os.linesep)
#         de.write(r"\draw[->] (0,-1)--(0,%s) node[right]{\footnotesize $ y $};" %(B + 2.2) + os.linesep)
#         de.write(r"\draw (0,0) node[below left]{\footnotesize $O$};"+ os.linesep)
#         de.write(r"\clip (-1,-1) rectangle (%s, %s);" %(A + 2, B + 2)+ os.linesep)
#         de.write(r"\draw[smooth,domain=-1:%s] plot (\x,{-0.4*\x+ %s });" %(A + 2, hang/1.5) + os.linesep)
#         de.write(r"\draw[smooth,domain=-1:%s] plot (\x,{-2*\x+ %s });" %(A + 2, k) + os.linesep)
#         de.write(r"\draw[-] (%s,-1) -- (%s,%s);" %(A, A, B + 2) + os.linesep)
#         de.write(r"\draw[-] (-1,%s) -- (%s,%s);" %(B, A + 2, B) + os.linesep)
#         de.write(r"\fill[pattern=dots] (%s,-1)--(%s,%s)--(%s,%s)--(%s,-1)--cycle;" %(A, A, B+2, B+2, B+2, B+2) + os.linesep)
#         de.write(r"\fill[pattern=dots] (-1,%s)--(-1,%s)--(%s,%s)--(%s,%s)--cycle;" %(B, B+2,B+2, B+2, B+2, B)+ os.linesep)
#         de.write(r"\fill[pattern=dots] (-1,-1)--(-1,%s)--(%s,%s)--(%s,%s)--(%s,-1)--cycle;" %(S_D[y], S_D[x], S_D[y], S_A[x], S_A[y], S_A[x] ) + os.linesep)
#         de.write(r"\fill[pattern=dots] (-1,-1)--(-1,%s)--(%s,%s)--(%s, %s)--(%s,-1)--cycle;" %(S_A[x], S_A[x], S_A[y], S_B[x], S_B[y], S_B[x]) + os.linesep)
#         de.write(r"\draw (%s, %s) node[above right]{$A$};" %(S_A[x], S_A[y]) + os.linesep)
#         de.write(r"\draw[dashed] (%s,0) node [below] {$ %s $}--(%s,%s) node [above right] {$A$} -- (0, %s) node [left] {$%s$};"
#                  %(S_A[x], SAx_string, S_A[x], S_A[y], S_A[y], SAy_string) + os.linesep)
#         de.write(r"\draw[dashed] (0, %s) node [left] {$ %s $}--(%s,%s) node [above left] {$B$};" %(S_B[y], SBy_string, S_B[x], S_B[y])+ os.linesep)
#         de.write(r"\draw[dashed] (%s, 0) node [below] {$ %s $}--(%s,%s) node [below right] {$D$};" %(S_D[x], SDx_string, S_D[x], S_D[y])+ os.linesep)
#         de.write(r"\node at (%s, %s) [below left] {$C$};" %(S_C[x], S_C[y])+ os.linesep)
#         de.write(r"\end{tikzpicture}"+ os.linesep)
#         de.write(r"\end{center}"+ os.linesep)
#         de.write(r"}"+ os.linesep)
#         de.write(r"\end{ex}"+ os.linesep)
#


# ---- Gia tri lon nhat / nho nhat cua F(x;y) tren mien nghiem cua he ----
# (tên cũ của cô: K10_2_3_3_1_H)
def L10_C2_B4_VD028_MC_A_01(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        # 1️⃣ Sinh dữ liệu ngẫu nhiên

        x_center = np.random.randint(-2, 3)
        y_center = np.random.randint(-2, 3)

        # Sinh K = [K0, K1, K2, K3, K4, K5]
        K = np.random.randint(1, 6, 6).tolist()

        # Sửa lỗi: Thay K5 bằng K[5] trong điều kiện while
        while (K[0] + K[3] <= 2) or (K[1] == K[4]) or (K[2] == K[5]):
            K = np.random.randint(1, 6, 6).tolist()

        K0, K1, K2, K3, K4, K5 = K  # Gán giá trị sau khi vòng lặp kết thúc

        # Tọa độ 4 đỉnh A, B, C, D
        A = [x_center - K0, y_center + K1]  # Trên trái
        B = [x_center - K0, y_center - K2]  # Dưới trái
        D = [x_center + K3, y_center - K5]  # Dưới phải
        C = [x_center + K3, y_center + K4]  # Trên phải

        # 4 CẠNH CỦA TỨ GIÁC (AB, BD, DC, CA)
        # 1. Cạnh AB (x = fx)
        fx = x_center - K0
        # 2. Cạnh DC (x = gx)
        gx = x_center + K3

        # 3. Cạnh BD (Chéo dưới)
        a_BD, b_BD, c_BD = pttq_duong_thang(B[0], B[1], D[0], D[1])
        # 4. Cạnh CA (Chéo trên)
        a_CA, b_CA, c_CA = pttq_duong_thang(C[0], C[1], A[0], A[1])

        # ĐIỂM KIỂM TRA: Trung điểm M của AD
        x_check = (A[0] + D[0]) / 2
        y_check = (A[1] + D[1]) / 2

        # HỆ BPT (Miền nghiệm là tứ giác)

        # BPT 1: x >= fx (x - fx >= 0)
        # BPT 2: x <= gx (x - gx <= 0)

        # BPT 3: Đường BD (Chéo dưới). Phải chứa điểm M
        VT_BD_M = a_BD * x_check + b_BD * y_check
        if VT_BD_M + c_BD < 0:
            dau_BD = '\\le'
        else:
            dau_BD = '\\ge'

        VT_BD = a_BD * x + b_BD * y
        VP_BD = -c_BD

        # BPT 4: Đường CA (Chéo trên). Phải chứa điểm M
        VT_CA_M = a_CA * x_check + b_CA * y_check
        if VT_CA_M + c_CA < 0:
            dau_CA = '\\le'
        else:
            dau_CA = '\\ge'

        VT_CA = a_CA * x + b_CA * y
        VP_CA = -c_CA

        # Hàm mục tiêu F(x,y)
        Heso = []
        while len(Heso) < 2:
            k = np.random.randint(-3, 4)
            if k != 0:
                Heso.append(k)

        H0, H1 = Heso

        F = lambda x_val, y_val: H0 * x_val + H1 * y_val

        # Giá trị hàm F tại 4 đỉnh (A, B, D, C)
        Fxy_values = [F(A[0], A[1]), F(B[0], B[1]), F(D[0], D[1]), F(C[0], C[1])]

        min_F = min(Fxy_values)
        max_F = max(Fxy_values)

        # Chọn loại giá trị cần tìm
        GiaTri_list = ['Giá trị lớn nhất', 'Giá trị nhỏ nhất', 'Tổng của giá trị nhỏ nhất và giá trị lớn nhất',
                       'Tích của giá trị nhỏ nhất và giá trị lớn nhất']
        GiaTri = np.random.choice(GiaTri_list)

        z = 0
        if GiaTri == 'Giá trị lớn nhất':
            z = max_F
        elif GiaTri == 'Giá trị nhỏ nhất':
            z = min_F
        elif GiaTri == 'Tổng của giá trị nhỏ nhất và giá trị lớn nhất':
            z = min_F + max_F
        else:  # Tích
            z = min_F * max_F

        # 2️⃣ Đảm bảo mỗi câu sinh ra duy nhất
        v = [A, B, C, D, Heso, z, GiaTri, fx, gx, VT_BD, VP_BD, dau_BD, VT_CA, VP_CA, dau_CA]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        A, B, C, D, Heso, z, GiaTri, fx, gx, VT_BD, VP_BD, dau_BD, VT_CA, VP_CA, dau_CA = v
        H0, H1 = Heso

        # 3️⃣ Tách biến và tạo nội dung
        F_expr = latex(H0 * x + H1 * y)

        # Sử dụng \text{...} cho các phần tiếng Việt trong công thức LaTeX
        debai = f"""{GiaTri} của biểu thức $F(x;y) = {F_expr}$ với $(x;y)$ thuộc miền nghiệm của hệ bất phương trình
        $$\\begin{{cases}}
            x \\ge {fx} \\\\
            x \\le {gx} \\\\
            {latex(VT_BD)} {dau_BD} {VP_BD} \\\\
            {latex(VT_CA)} {dau_CA} {VP_CA}
        \\end{{cases}}$$ là"""

        # Đáp án đúng
        dapso = f"{z}"

        # Tạo nhiễu
        dsnhieu = []
        while len(dsnhieu) < 3:
            nhi = z + np.random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            if nhi != z and str(nhi) not in dsnhieu:
                dsnhieu.append(str(nhi))

        # Tính lại F tại các đỉnh để đưa vào lời giải
        F_A = F(A[0], A[1])
        F_B = F(B[0], B[1])
        F_C = F(C[0], C[1])
        F_D = F(D[0], D[1])
        min_F_giai = min([F_A, F_B, F_C, F_D])
        max_F_giai = max([F_A, F_B, F_C, F_D])

        giai = f"""
            Miền nghiệm $D$ của hệ bất phương trình là miền tứ giác lồi $ABDC$ (được giới hạn bởi 4 cạnh $x = {fx}, x = {gx}, {latex(VT_BD)} = {VP_BD}, {latex(VT_CA)} = {VP_CA}$), với tọa độ các đỉnh là:\\\\
            \\begin{{itemize}}
                \\item $A({A[0]}; {A[1]})$
                \\item $B({B[0]}; {B[1]})$
                \\item $D({D[0]}; {D[1]})$
                \\item $C({C[0]}; {C[1]})$
            \\end{{itemize}}

            Giá trị của hàm mục tiêu $F(x;y) = {F_expr}$ tại các đỉnh là:\\\\
            \\begin{{itemize}}
                \\item $F(A) = {H0} \\cdot {A[0]} + {H1} \\cdot {A[1]} = {F_A}$
                \\item $F(B) = {H0} \\cdot {B[0]} + {H1} \\cdot {B[1]} = {F_B}$
                \\item $F(D) = {H0} \\cdot {D[0]} + {H1} \\cdot {D[1]} = {F_D}$
                \\item $F(C) = {H0} \\cdot {C[0]} + {H1} \\cdot {C[1]} = {F_C}$
            \\end{{itemize}}

            Áp dụng định lý về giá trị lớn nhất/nhỏ nhất của hàm mục tiêu trên miền nghiệm giới hạn, ta có:\\\\
            $$\\min F = {min_F_giai} \\quad \\text{{và}} \\quad \\max F = {max_F_giai}$$

            Theo yêu cầu đề bài ({GiaTri}):
            \\begin{{itemize}}
                \\item Nếu tìm Giá trị lớn nhất: $\\max F = {max_F_giai}$.
                \\item Nếu tìm Giá trị nhỏ nhất: $\\min F = {min_F_giai}$.
                \\item Nếu tìm Tổng: $\\min F + \\max F = {min_F_giai} + {max_F_giai} = {min_F_giai + max_F_giai}$.
                \\item Nếu tìm Tích: $\\min F \\cdot \\max F = {min_F_giai} \\cdot {max_F_giai} = {min_F_giai * max_F_giai}$.
            \\end{{itemize}}
            Vậy {GiaTri} là ${z}$.
        """

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN
#print(K10_2_3_3_1_H(4,1))

def K10_2_3_3_2_VD(): #Dạng 3: Tìm miền nghiệm của bất phương trình
    with open(r"latex\data\de.tex", "a", encoding='utf-8') as de:
        x = Symbol('x')
        y = Symbol('y')

        x_center = np.randint(-2,2)
        y_center = np.randint(-2,2)
        K = []
        for i in range(0,4):
            k = np.randint(0,5)
            K.append(k)
        while (K[0] + K[3] <= 5):
            k0 = np.randint(0,10)
            k3 = np.randint(0,10)
            K.pop(3)
            K.insert(3,k3)
            K.pop(0)
            K.insert(0,k0)
        while (K[1] + K[2] <= 5):
            k1 = np.randint(0,10)
            k2 = np.randint(0,10)
            K.pop(2)
            K.insert(2,k2)
            K.pop(1)
            K.insert(1,k)

        A = [x_center - K[0], y_center + K[1]] # đường thẳng AB song song vơi Ox có pt x = x_center - K[0]
        B = [x_center - K[0], y_center - K[2]]
        C = [x_center + K[3], y_center - K[2]] # đường thẳng CD song song vơi Ox có pt x = x_center + K[3]
        D = [x_center + K[3], y_center + K[1]]
        fx = x_center - K[0] # đường thẳng AB : x = fx
        gx = x_center + K[3] # đường thẳng CD: x = gx
        hx = y_center - K[2] # đường thẳng BC
        kx = y_center + K[1] # đường thẳng AD

        # Đường thẳng MN với M,N nằm trên 2 cạnh bất kì của hình chữ nhật ABCD
        x_M = np.randint(x_center - K[0]+1, x_center + K[3]-1)
        y_N = np.randint(y_center - K[2]+1, y_center + K[1]-1)
        y_M = np.choice([y_center - K[2], y_center + K[1]])
        x_N = np.choice([x_center - K[0], x_center + K[3]])
        M = [x_M, y_M]
        N = [x_N, y_N]
        a_MN = dc.pttq(M[0],M[1],N[0],N[1])[0]
        b_MN = dc.pttq(M[0],M[1],N[0],N[1])[1]
        c_MN = dc.pttq(M[0],M[1],N[0],N[1])[2]
        MN = lambda x,y: a_MN * x + b_MN * y + c_MN # đường thẳng MN
        VT_MN = a_MN * x + b_MN * y
        VP_MN = - c_MN

        Duong = []
        Am = []
        if MN(A[0],A[1]) > 0:
            Duong.append('A')
        else:
            Am.append('A')
        if MN(B[0],B[1]) > 0:
            Duong.append('B')
        else:
            Am.append('B')
        if MN(C[0],C[1]) > 0:
            Duong.append('C')
        else:
            Am.append('C')
        if MN(D[0],D[1]) > 0:
            Duong.append('D')
        else:
            Am.append('D')
        Dau = np.choice(['Duong', 'Am'])
        Mien = ['Miền tam giác', 'Miền tứ giác', 'Miền ngũ giác', 'Miền lục giác']
        if (Dau == 'Duong') and (len(Duong) == 1):
            dau = r'\ge'
            mien = 'Miền tam giác'
            Mien.remove(mien)
        elif (Dau == 'Duong') and (len(Duong) == 2):
            dau = r'\ge'
            mien = 'Miền tứ giác'
            Mien.remove(mien)
        elif (Dau == 'Duong') and (len(Duong) == 3):
            dau = r'\ge'
            mien = 'Miền ngũ giác'
            Mien.remove(mien)
        elif (Dau == 'Am') and (len(Am) == 1):
            dau = r'\le'
            mien = 'Miền tam giác'
            Mien.remove(mien)
        elif (Dau == 'Am') and (len(Am) == 2):
            dau = r'\le'
            mien = 'Miền tứ giác'
            Mien.remove(mien)
        elif (Dau == 'Am') and (len(Am) == 3):
            dau = r'\le'
            mien = 'Miền ngũ giác'
            Mien.remove(mien)
        de.write(r"\begin{ex}" + os.linesep)
        de.write(f"Miền nghiệm của hệ bất phương trình $\\heva{{& {fx} \\le x \\le {gx} \\\\ & {hx} \\le y \\le {kx} \\\\ & {latex(VT_MN)} {dau} {VP_MN} }}$ là{os.linesep}")
        de.write(r"\choice"+ os.linesep)
        de.write(f"{{\\True {mien}}}{os.linesep}")
        de.write(f"{{{Mien[0]}}}{os.linesep}")
        de.write(f"{{{Mien[1]}}}{os.linesep}")
        de.write(f"{{{Mien[2]}}}{os.linesep}")
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\end{ex}" + os.linesep)


# =====================================================================
# BỔ SUNG DẠNG CHO CHƯƠNG 2 (29/09/2026)
# ---------------------------------------------------------------------
# Trước khối này chương 2 chỉ có 6/14 dạng có hàm, và TOÀN LÀ trắc
# nghiệm: không có câu trả lời ngắn, tự luận hay đúng/sai nào.
# Khối này lấp các ô còn trống của bảng loại câu.
#
# Quy ước đã chốt: câu trả lời ngắn có MỘT câu hỏi một đáp số, câu tự
# luận phải từ HAI ý trở lên, câu đúng/sai xếp bốn ý theo bậc
# NB -> TH -> VD -> VDC.
# =====================================================================
import math as _math
import random as _rd

from DefChung import bt as _bt   # viet bieu thuc gon (bo he so 1, dau)


def _xx2(gt, n=2):
    """Làm tròn rồi viết theo kiểu Việt Nam (dấu phẩy thập phân)."""
    s = ("%%.%df" % n) % float(gt)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return ("0" if s in ("-0", "") else s).replace(".", ",")


def _ba_nhieu2(dapso, ung_vien, buoc=None):
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


def _mien_tu_giac():
    r"""Sinh miền nghiệm là TỨ GIÁC có bốn đỉnh NGUYÊN.

    Cách làm: chọn trước ba đỉnh $P(m;0)$, $Q(u;v)$, $R(0;n)$ rồi mới viết
    hai bất phương trình đi qua chúng, nên đỉnh chắc chắn nguyên (nếu sinh
    bất phương trình trước rồi mới giải thì giao điểm hay ra phân số).
    Miền nghiệm là $x \ge 0$, $y \ge 0$ và hai bất phương trình đó.
    Trả về (m, n, u, v, (a1,b1,c1), (a2,b2,c2), dinh).
    """
    while True:
        m = _rd.randint(4, 12)
        n = _rd.randint(4, 12)
        u = _rd.randint(1, m - 1)
        v = _rd.randint(1, n - 1)
        # Q phải nằm NGOÀI đoạn PR thì mới thành tứ giác lồi
        if u * n + v * m <= m * n:
            continue
        a1, b1, c1 = v, m - u, v * m          # đường qua P và Q
        a2, b2, c2 = n - v, u, u * n          # đường qua Q và R
        if a1 <= 0 or b1 <= 0 or a2 <= 0 or b2 <= 0:
            continue
        g = _math.gcd(_math.gcd(a1, b1), c1)
        a1, b1, c1 = a1 // g, b1 // g, c1 // g
        g = _math.gcd(_math.gcd(a2, b2), c2)
        a2, b2, c2 = a2 // g, b2 // g, c2 // g
        dinh = [(0, 0), (m, 0), (u, v), (0, n)]
        return m, n, u, v, (a1, b1, c1), (a2, b2, c2), dinh


def _bpt_tex(a, b, c):
    """Viết ax + by <= c cho gọn (bỏ hệ số 1, đổi dấu cho đẹp)."""
    def he_so(k, ten, dau_dau):
        if k == 0:
            return ""
        d = "-" if k < 0 else ("+" if not dau_dau else "")
        k = abs(k)
        so = "" if k == 1 else str(k)
        return ("%s %s%s" % (d, so, ten)).strip() if not dau_dau else "%s%s%s" % (d, so, ten)
    return ("%s %s \\le %d" % (he_so(a, "x", True), he_so(b, "y", False), c)).strip()


# ---------------------------------------------------------------------
# BÀI 3 - bất phương trình bậc nhất hai ẩn
# ---------------------------------------------------------------------

def L10_C2_B3_NB023_SA_A_01(socau, dang=2):
    """Trả lời ngắn: tính giá trị vế trái của bất phương trình tại một điểm."""
    gt = []
    while len(gt) < socau:
        v = (_rd.randint(-6, 6) or 2, _rd.randint(-6, 6) or 3, _rd.randint(-9, 9),
             _rd.randint(-5, 5), _rd.randint(-5, 5))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a, b, c, x0, y0 in gt:
        gt_ve_trai = a * x0 + b * y0 + c
        debai = (r"Cho bất phương trình $%s$. Tính giá trị của biểu thức "
                 r"$f\left(x; y\right) = %dx + %dy + %d$ tại điểm $M\left(%d; %d\right)$."
                 % (_bpt_tex(a, b, -c), a, b, c, x0, y0))
        giai = (r"Thay $x = %d$ và $y = %d$ vào biểu thức:\\ "
                r"$f\left(%d; %d\right) = %d\cdot\left(%d\right) + %d\cdot\left(%d\right) + %d = %d$.\\ "
                r"(Giá trị này %s nên điểm $M$ %s miền nghiệm của bất phương trình đã cho.)"
                % (x0, y0, x0, y0, a, x0, b, y0, c, gt_ve_trai,
                   "nhỏ hơn hoặc bằng $0$" if gt_ve_trai <= 0 else "lớn hơn $0$",
                   "thuộc" if gt_ve_trai <= 0 else "không thuộc"))
        dung = str(gt_ve_trai)
        ds = _ba_nhieu2(dung, [str(a * x0 + b * y0), str(-gt_ve_trai), str(gt_ve_trai + c)],
                        buoc=lambda k: str(gt_ve_trai + 2 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C2_B3_NB025_MC_A_01(socau, dang=1):
    """Chọn bất phương trình mô tả đúng một tình huống thực tế."""
    TINH_HUONG = [
        ("Một cửa hàng bán hai loại bút: bút chì giá {p} nghìn đồng một chiếc và "
         "bút bi giá {q} nghìn đồng một chiếc. Bạn An có {c} nghìn đồng. Gọi $x$, $y$ "
         "lần lượt là số bút chì và số bút bi bạn An mua. Bất phương trình nào sau đây "
         "mô tả đúng điều kiện về số tiền?", "tiền"),
        ("Một xưởng may làm hai loại áo: áo sơ mi cần {p} giờ công và áo khoác cần {q} "
         "giờ công để hoàn thành. Trong một tuần xưởng có nhiều nhất {c} giờ công. "
         "Gọi $x$, $y$ lần lượt là số áo sơ mi và số áo khoác may được trong tuần. "
         "Bất phương trình nào sau đây mô tả đúng điều kiện về giờ công?", "giờ công"),
        ("Một người chở hai loại hàng: mỗi thùng hàng loại một nặng {p} kg, mỗi thùng "
         "loại hai nặng {q} kg. Xe chở được tối đa {c} kg. Gọi $x$, $y$ lần lượt là số "
         "thùng loại một và loại hai. Bất phương trình nào sau đây mô tả đúng điều kiện "
         "về khối lượng?", "khối lượng"),
    ]
    gt = []
    while len(gt) < socau:
        i = _rd.randrange(len(TINH_HUONG))
        p, q = _rd.randint(2, 9), _rd.randint(2, 9)
        c = _rd.randint(40, 200)
        if p == q:
            continue
        if (i, p, q, c) not in gt:
            gt.append((i, p, q, c))

    cauTN = ''
    for i, p, q, c in gt:
        mau, ten = TINH_HUONG[i]
        debai = mau.format(p=p, q=q, c=c)
        dung = r"$%dx + %dy \le %d$" % (p, q, c)
        giai = (r"Tổng %s dùng cho $x$ đơn vị loại một và $y$ đơn vị loại hai là "
                r"$%dx + %dy$.\\ "
                r"Vì không được vượt quá $%d$ nên ta có $%dx + %dy \le %d$.\\ "
                r"Dấu phải là $\le$ (không vượt quá) chứ không phải $\ge$; và hệ số đi "
                r"kèm $x$ phải là $%d$, đi kèm $y$ phải là $%d$."
                % (ten, p, q, c, p, q, c, p, q))
        ds = _ba_nhieu2(dung, [r"$%dx + %dy \ge %d$" % (p, q, c),
                               r"$%dx + %dy \le %d$" % (q, p, c),
                               r"$%dx + %dy < %d$" % (p, q, c - 1)],
                        buoc=lambda k: r"$%dx + %dy \le %d$" % (p, q, c + k))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C2_B3_TH024_TL_A_01(socau, dong=1):
    """Tự luận: các bước vẽ miền nghiệm - tìm hai giao điểm của đường bờ với hai trục."""
    gt = []
    while len(gt) < socau:
        a = _rd.choice([1, 2, 3, 4, 5])
        b = _rd.choice([1, 2, 3, 4, 5])
        k = _rd.randint(2, 8)
        c = a * b * k                      # chia het cho ca a va b -> giao diem nguyen
        if (a, b, c) not in gt:
            gt.append((a, b, c))

    cauTN = ''
    for a, b, c in gt:
        debai = (r"Cho bất phương trình $%dx + %dy \le %d$. Để biểu diễn miền nghiệm của "
                 r"nó trên mặt phẳng toạ độ, trước hết ta vẽ đường thẳng bờ "
                 r"$d: %dx + %dy = %d$." % (a, b, c, a, b, c))
        ds_abcd = [
            (r"Tìm toạ độ giao điểm của $d$ với trục hoành.",
             r"\left(%d; 0\right)" % (c // a),
             r"Giao điểm với trục hoành có $y = 0$, thay vào $d$:\\ "
             r"$%dx + %d\cdot 0 = %d \Rightarrow x = \dfrac{%d}{%d} = %d$.\\ "
             r"Vậy giao điểm là $\left(%d; 0\right)$."
             % (a, b, c, c, a, c // a, c // a)),
            (r"Tìm toạ độ giao điểm của $d$ với trục tung.",
             r"\left(0; %d\right)" % (c // b),
             r"Giao điểm với trục tung có $x = 0$, thay vào $d$:\\ "
             r"$%d\cdot 0 + %dy = %d \Rightarrow y = \dfrac{%d}{%d} = %d$.\\ "
             r"Vậy giao điểm là $\left(0; %d\right)$. Nối hai điểm vừa tìm được ta có "
             r"đường thẳng $d$; thay $O\left(0; 0\right)$ vào vế trái được $0 \le %d$ "
             r"(đúng), nên miền nghiệm là nửa mặt phẳng bờ $d$ có chứa gốc toạ độ."
             % (a, b, c, c, b, c // b, c // b, c)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# ---------------------------------------------------------------------
# BÀI 4 - hệ bất phương trình bậc nhất hai ẩn
# ---------------------------------------------------------------------

def L10_C2_B4_NB026_MC_A_01(socau, dang=1):
    """Nhận ra hệ bất phương trình bậc nhất hai ẩn."""
    gt = []
    while len(gt) < socau:
        v = tuple(_rd.randint(1, 9) for _ in range(6)) + (_rd.randrange(4),)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a1, b1, c1, a2, b2, c2, _k in gt:
        he = lambda t1, t2: r"$\heva{& %s \\ & %s}$" % (t1, t2)
        dung = he(r"%dx + %dy \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2))
        giai = (r"Hệ bất phương trình bậc nhất hai ẩn là hệ gồm các bất phương trình "
                r"dạng $ax + by \le c$ (hoặc $<, \ge, >$), trong đó $a$ và $b$ không đồng "
                r"thời bằng $0$ và các ẩn $x$, $y$ đều có bậc nhất.\\ "
                r"$\bullet$ Hệ có số hạng $x^{2}$, $y^{2}$ hoặc tích $xy$: loại.\\ "
                r"$\bullet$ Hệ có ẩn thứ ba $z$: loại, vì khi đó không còn là hai ẩn.\\ "
                r"Chỉ hệ gồm hai bất phương trình mà $x$, $y$ đều bậc nhất mới thoả mãn.")
        ds = _ba_nhieu2(dung,
                        [he(r"%dx^{2} + %dy \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2)),
                         he(r"%dxy + %dy \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2)),
                         he(r"%dx + %dy - z \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2))],
                        buoc=lambda k: he(r"%dx^{%d} + %dy \le %d" % (a1, k + 1, b1, c1),
                                          r"%dx - %dy > %d" % (a2, b2, c2)))
        debai = r"Hệ nào sau đây là hệ bất phương trình bậc nhất hai ẩn?"
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN



_DAU_BPT = [r"\le", r"<", r"\ge", r">"]


def _bpt_bac_nhat(a, b, c, dau):
    """ax + by (dau) c, viết gọn; a hoặc b có thể bằng 0 (bpt khuyết ẩn)."""
    return r"%s %s %d" % (_bt((a, "x"), (b, "y")), dau, c)


def _bpt_khong_bac_nhat(kieu, a, b, c, dau):
    """Một bất phương trình KHÔNG phải bậc nhất hai ẩn, theo kiểu lỗi."""
    if kieu == "x2":
        return r"%s %s %d" % (_bt((a, "x^{2}"), (b, "y")), dau, c), \
            r"có số hạng $x^{2}$ (bậc hai)"
    if kieu == "xy":
        return r"%s %s %d" % (_bt((a, "xy"), (b, "y")), dau, c), \
            r"có tích $xy$ (bậc hai)"
    if kieu == "z":
        return r"%s %s %d" % (_bt((a, "x"), (b, "y"), (-1, "z")), dau, c), \
            r"có ẩn thứ ba $z$"
    if kieu == "phan_so":
        # a, b > 0 (noi goi truyen so duong)
        return r"\dfrac{%d}{x} + %s %s %d" % (a, _bt((b, "y")), dau, c), \
            r"có ẩn $x$ ở mẫu"
    return r"%s %s %d" % (_bt((a, "x"), (b, r"\sqrt{y}")), dau, c), \
        r"có căn thức $\sqrt{y}$"


def _he2(t1, t2):
    return r"$\heva{& %s \\ & %s}$" % (t1, t2)


def L10_C2_B4_NB026_MC_A_02(socau, dang=1):
    r"""Nhận ra hệ bất phương trình bậc nhất hai ẩn - HỎI NGƯỢC: hệ nào
    KHÔNG phải.

    CLAUDE THEM 29/09/2026 - bien the 02, cung dang voi _01 (mapping: "Nhan
    ra he bat phuong trinh bac nhat hai an"). _01 hoi he nao LA; _02 hoi he
    nao KHONG PHAI: ba phuong an nhieu la ba he dung (co ca he khuyet an),
    dap an la he co mot bat phuong trinh sai dang. Co Lan duyet.
    """
    gt = []
    while len(gt) < socau:
        kieu = _rd.choice(["x2", "xy", "z", "phan_so", "can"])
        v = (kieu, _rd.randint(1, 6), _rd.randint(1, 6), _rd.randint(2, 12))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for kieu, a, b, c in gt:
        d = _rd.sample(_DAU_BPT, 4)
        sai, ly_do = _bpt_khong_bac_nhat(kieu, a, b, c, d[0])
        dung = _he2(sai, _bpt_bac_nhat(1, -b, c + 1, d[1]))
        ba_he = [
            _he2(_bpt_bac_nhat(a, b, c, d[1]), _bpt_bac_nhat(b, -a, 1, d[2])),
            _he2(_bpt_bac_nhat(1, 0, 0, r"\ge"), _bpt_bac_nhat(0, 1, 0, r"\ge")),
            _he2(_bpt_bac_nhat(0, b, c, d[3]), _bpt_bac_nhat(a, 1, c + a, d[0])),
        ]
        nhieu = _ba_nhieu2(dung, ba_he)
        debai = (r"Hệ nào sau đây \textbf{không} phải là hệ bất phương trình bậc "
                 r"nhất hai ẩn?")
        giai = (r"Hệ bất phương trình bậc nhất hai ẩn gồm các bất phương trình "
                r"dạng $ax + by \le c$ (hoặc $<, \ge, >$) với $a$, $b$ không đồng "
                r"thời bằng $0$. Bất phương trình khuyết một ẩn như $x \ge 0$ hay "
                r"$%s$ vẫn đúng dạng (hệ số của ẩn kia bằng $0$)." % _bpt_bac_nhat(0, b, c, d[3]) +
                "\\\\\n"
                r"Hệ %s không phải vì bất phương trình $%s$ %s." % (dung, sai, ly_do))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C2_B4_NB026_MC_A_03(socau, dang=1):
    r"""Nhận ra hệ bất phương trình bậc nhất hai ẩn - đáp án là hệ có bất
    phương trình KHUYẾT ẨN ($x \ge 0$, $y < 3$...), nhiễu là các hệ có
    $\dfrac{1}{x}$, $\sqrt{y}$, $x^2$, $xy$, ẩn $z$.

    CLAUDE THEM 29/09/2026 - bien the 03, cung dang voi _01. Loi dan khac
    (ghep cap bat phuong trinh thanh he) va kiem tra y "khuyet an van la bac
    nhat hai an" ma _01 khong co. Co Lan duyet.
    """
    gt = []
    while len(gt) < socau:
        v = (_rd.randint(1, 6), _rd.randint(1, 6), _rd.randint(2, 12),
             _rd.randrange(3))
        if v not in gt:
            gt.append(v)

    cauTN = ""
    for a, b, c, kieu_dung in gt:
        d = _rd.sample(_DAU_BPT, 4)
        if kieu_dung == 0:
            khuyet = _bpt_bac_nhat(1, 0, _rd.randint(-3, 3), d[0])       # x ... k
        elif kieu_dung == 1:
            khuyet = _bpt_bac_nhat(0, 1, _rd.randint(-3, 3), d[0])       # y ... k
        else:
            khuyet = _bpt_bac_nhat(0, -1, _rd.randint(-3, 3), d[0])      # -y ... k
        dung = "$%s$" % _bpt_bac_nhat(a, -b, c, d[1])
        loai_sai = _rd.sample(["x2", "xy", "z", "phan_so", "can"], 3)
        ba_he = []
        ly_do = []
        for k, ks in enumerate(loai_sai):
            t, ld = _bpt_khong_bac_nhat(ks, a, b, c, d[(k + 2) % 4])
            ba_he.append("$%s$" % t)
            ly_do.append(r"$%s$ %s" % (t, ld))
        nhieu = _ba_nhieu2(dung, ba_he)
        debai = (r"Ghép bất phương trình $%s$ với bất phương trình nào dưới đây "
                 r"thì được một hệ bất phương trình bậc nhất hai ẩn $x$, $y$?"
                 % khuyet)
        giai = (r"Bất phương trình $%s$ là bất phương trình bậc nhất hai ẩn "
                r"(hệ số của một ẩn bằng $0$)." % khuyet +
                "\\\\\n"
                r"Trong các bất phương trình ghép thêm: " + "; ".join(ly_do) +
                r" nên không phải bậc nhất hai ẩn." +
                "\\\\\n"
                r"Chỉ $%s$ là bất phương trình bậc nhất hai ẩn; hệ thu được "
                r"là %s." % (_bpt_bac_nhat(a, -b, c, d[1]),
                                  _he2(khuyet, _bpt_bac_nhat(a, -b, c, d[1]))))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN

def L10_C2_B4_TH027_TL_A_01(socau, dong=1):
    """Tự luận: miền nghiệm của hệ là tam giác vuông - tìm đỉnh và tính diện tích."""
    gt = []
    while len(gt) < socau:
        m = _rd.randint(3, 12)
        n = _rd.randint(3, 12)
        if (m * n) % 2:                    # de dien tich m.n/2 la so nguyen
            continue
        if (m, n) not in gt:
            gt.append((m, n))

    cauTN = ''
    for m, n in gt:
        g = _math.gcd(n, m)
        a, b, c = n // g, m // g, m * n // g
        S = m * n // 2
        debai = (r"Cho hệ bất phương trình $\heva{& x \ge 0 \\ & y \ge 0 \\ & %dx + %dy \le %d}$"
                 % (a, b, c))
        ds_abcd = [
            (r"Tìm toạ độ ba đỉnh của miền nghiệm.",
             r"\left(0;0\right), \left(%d;0\right), \left(0;%d\right)" % (m, n),
             r"Miền nghiệm nằm trong góc phần tư thứ nhất, bị chặn bởi đường thẳng "
             r"$d: %dx + %dy = %d$.\\ "
             r"$d$ cắt trục hoành tại $\left(%d; 0\right)$ và cắt trục tung tại "
             r"$\left(0; %d\right)$; cùng với gốc $O\left(0;0\right)$ ta được ba đỉnh."
             % (a, b, c, m, n)),
            (r"Tính diện tích miền nghiệm.", r"%d" % S,
             r"Ba đỉnh tạo thành tam giác vuông tại $O$, hai cạnh góc vuông nằm trên hai "
             r"trục toạ độ và có độ dài $%d$ và $%d$.\\ "
             r"$S = \dfrac{1}{2}\cdot %d\cdot %d = %d$." % (m, n, m, n, S)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C2_B4_VD028_SA_A_01(socau, dang=2):
    """Trả lời ngắn: giá trị lớn nhất của F = px + qy trên miền nghiệm của hệ."""
    gt = []
    while len(gt) < socau:
        m, n, u, v, bpt1, bpt2, dinh = _mien_tu_giac()
        p, q = _rd.randint(1, 9), _rd.randint(1, 9)
        gtri = [p * X + q * Y for X, Y in dinh]
        lon = max(gtri)
        if gtri.count(lon) != 1:           # phai co DUY NHAT mot dinh dat gia tri lon nhat
            continue
        gt.append((m, n, u, v, bpt1, bpt2, dinh, p, q, lon))
        if len(gt) > socau:
            break

    cauTN = ''
    for m, n, u, v, bpt1, bpt2, dinh, p, q, lon in gt[:socau]:
        (a1, b1, c1), (a2, b2, c2) = bpt1, bpt2
        debai = (r"Cho hệ bất phương trình $\heva{& x \ge 0 \\ & y \ge 0 \\ "
                 r"& %s \\ & %s}$. Tìm giá trị lớn nhất của biểu thức "
                 r"$F\left(x; y\right) = %dx + %dy$ trên miền nghiệm của hệ."
                 % (_bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2), p, q))
        bang = r"\\ ".join(r"$F\left(%d; %d\right) = %d\cdot %d + %d\cdot %d = %d$"
                           % (X, Y, p, X, q, Y, p * X + q * Y) for X, Y in dinh)
        giai = (r"Miền nghiệm của hệ là miền tứ giác có bốn đỉnh "
                r"$\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, "
                r"$\left(0;%d\right)$.\\ "
                r"Biểu thức $F = %dx + %dy$ đạt giá trị lớn nhất tại một trong các đỉnh, "
                r"nên chỉ cần tính $F$ tại bốn đỉnh đó:\\ %s.\\ "
                r"Vậy giá trị lớn nhất của $F$ bằng $%d$."
                % (m, u, v, n, p, q, bang, lon))
        dung = str(lon)
        ds = _ba_nhieu2(dung, [str(min(p * X + q * Y for X, Y in dinh)),
                               str(p * m + q * n), str(lon + p)],
                        buoc=lambda k: str(lon + 2 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C2_B4_VD028_TL_A_01(socau, dong=1):
    """Tự luận: bài toán tối ưu thực tiễn dẫn đến hệ bất phương trình."""
    gt = []
    while len(gt) < socau:
        m, n, u, v, bpt1, bpt2, dinh, = _mien_tu_giac()
        p, q = _rd.randint(2, 9), _rd.randint(2, 9)
        gtri = [p * X + q * Y for X, Y in dinh]
        lon = max(gtri)
        if gtri.count(lon) != 1 or lon < 30:
            continue
        gt.append((m, n, u, v, bpt1, bpt2, dinh, p, q, lon))

    cauTN = ''
    for m, n, u, v, bpt1, bpt2, dinh, p, q, lon in gt[:socau]:
        (a1, b1, c1), (a2, b2, c2) = bpt1, bpt2
        dinh_lon = [d for d in dinh if p * d[0] + q * d[1] == lon][0]
        debai = (r"Một xưởng sản xuất hai loại sản phẩm. Gọi $x$, $y$ lần lượt là số sản "
                 r"phẩm loại một và loại hai làm được trong một ngày. Điều kiện về nguyên "
                 r"liệu và giờ công dẫn đến hệ bất phương trình "
                 r"$\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$, và tiền lãi thu được "
                 r"(đơn vị nghìn đồng) là $F\left(x; y\right) = %dx + %dy$."
                 % (_bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2), p, q))
        bang = r"\\ ".join(r"$F\left(%d; %d\right) = %d$" % (X, Y, p * X + q * Y)
                           for X, Y in dinh)
        ds_abcd = [
            (r"Tìm toạ độ các đỉnh của miền nghiệm.",
             r"\left(0;0\right), \left(%d;0\right), \left(%d;%d\right), \left(0;%d\right)"
             % (m, u, v, n),
             r"Miền nghiệm là giao của bốn nửa mặt phẳng, nằm trong góc phần tư thứ nhất.\\ "
             r"Giải từng cặp phương trình đường bờ ta được bốn đỉnh "
             r"$\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, "
             r"$\left(0;%d\right)$." % (m, u, v, n)),
            (r"Hỏi mỗi ngày nên làm bao nhiêu sản phẩm mỗi loại để tiền lãi lớn nhất? "
             r"Tiền lãi lớn nhất là bao nhiêu nghìn đồng?",
             r"%d" % lon,
             r"Biểu thức bậc nhất $F$ đạt giá trị lớn nhất tại một đỉnh của miền nghiệm, "
             r"nên chỉ cần so sánh $F$ tại bốn đỉnh:\\ %s.\\ "
             r"Lớn nhất là $%d$, đạt tại $\left(%d; %d\right)$. Vậy mỗi ngày nên làm $%d$ "
             r"sản phẩm loại một và $%d$ sản phẩm loại hai, tiền lãi lớn nhất là $%d$ "
             r"nghìn đồng."
             % (bang, lon, dinh_lon[0], dinh_lon[1], dinh_lon[0], dinh_lon[1], lon)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# ---------------------------------------------------------------------
# CLAUDE THEM 29/09/2026 - bien the _02, _03 cho VD028 (MC_A, SA_A, TL_A).
# Co Lan duyet.
# ---------------------------------------------------------------------

def _hinh_mien_da_giac(dinh, ghi_dinh=True):
    r"""Hình vẽ miền nghiệm là đa giác (tô đậm) trên hệ trục Oxy, có lưới và
    ghi toạ độ các đỉnh. dinh: danh sách đỉnh NGUYÊN theo thứ tự vòng."""
    xm = max(x for x, _y in dinh) + 1
    ym = max(y for _x, y in dinh) + 1
    tl = 0.45 if max(xm, ym) > 10 else 0.6
    duong = " -- ".join("(%d,%d)" % d for d in dinh) + " -- cycle"
    nhan = ""
    if ghi_dinh:
        for X, Y in dinh:
            if (X, Y) == (0, 0):
                continue
            vt = "above right" if X > 0 and Y > 0 else ("below" if Y == 0 else "left")
            nhan += ("\\fill (%d,%d) circle[radius=2pt] node[%s]{\\scriptsize $\\left(%d;%d\\right)$};\n"
                     % (X, Y, vt, X, Y))
    return (
        "\\begin{tikzpicture}[scale=%s,>=stealth]\n" % tl +
        "\\draw[gray!40,very thin] (0,0) grid (%d,%d);\n" % (xm, ym) +
        "\\fill[gray!35] %s;\n" % duong +
        "\\draw[thick] %s;\n" % duong +
        "\\draw[->] (-0.5,0) -- (%s,0) node[below right]{$x$};\n" % (xm + 0.6) +
        "\\draw[->] (0,-0.5) -- (0,%s) node[above left]{$y$};\n" % (ym + 0.6) +
        "\\node[below left] at (0,0) {\\scriptsize $O$};\n" + nhan +
        "\\end{tikzpicture}")


def _F_tex(p, q):
    return _bt((p, "x"), (q, "y"))


def _bang_F(dinh, p, q):
    return r"\\ ".join(r"$F\left(%d; %d\right) = %d$" % (X, Y, p * X + q * Y) for X, Y in dinh)


def L10_C2_B4_VD028_MC_A_02(socau, dang=1):
    r"""Tìm ĐIỂM mà tại đó F = ax + by đạt giá trị lớn nhất trên miền đa giác
    (hỏi toạ độ điểm, không hỏi giá trị)."""
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        m, n, u, v, bpt1, bpt2, dinh = _mien_tu_giac()
        p, q = _rd.randint(1, 9), _rd.randint(1, 9)
        gtri = [p * X + q * Y for X, Y in dinh]
        if gtri.count(max(gtri)) != 1:
            continue
        gt.append((bpt1, bpt2, dinh, p, q))
    cauTN = ''
    for (a1, b1, c1), (a2, b2, c2), dinh, p, q in gt:
        gtri = [p * X + q * Y for X, Y in dinh]
        dinh_lon = dinh[gtri.index(max(gtri))]
        dung = r"$\left(%d; %d\right)$" % dinh_lon
        nhieu = [r"$\left(%d; %d\right)$" % d for d in dinh if d != dinh_lon]
        debai = (r"Biểu thức $F\left(x; y\right) = %s$, với $\left(x; y\right)$ thuộc miền "
                 r"nghiệm của hệ $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$, đạt giá trị "
                 r"lớn nhất tại điểm nào sau đây?"
                 % (_F_tex(p, q), _bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2)))
        giai = (r"Miền nghiệm là tứ giác có các đỉnh $\left(0;0\right)$, $\left(%d;0\right)$, "
                r"$\left(%d;%d\right)$, $\left(0;%d\right)$ (giao của các đường bờ)."
                % (dinh[1][0], dinh[2][0], dinh[2][1], dinh[3][1]) +
                "\\\\\n" + r"$F$ đạt giá trị lớn nhất tại một đỉnh; tính $F$ tại các đỉnh:\\ " +
                _bang_F(dinh, p, q) + "." + "\\\\\n" +
                r"Giá trị lớn nhất là $%d$, đạt tại $\left(%d; %d\right)$." % (max(gtri), dinh_lon[0], dinh_lon[1]))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _chon_F_co_dau(dinh, hoi_lon):
    """Hệ số p, q (có thể âm) để GTLN hoặc GTNN đạt tại DUY NHẤT một đỉnh."""
    while True:
        p = _rd.choice([k for k in range(-6, 7) if k])
        q = _rd.choice([k for k in range(-6, 7) if k])
        g = [p * X + q * Y for X, Y in dinh]
        t = max(g) if hoi_lon else min(g)
        # duy nhat mot dinh, va khong phai goc O (dat tai O thi qua de)
        if g.count(t) == 1 and dinh[g.index(t)] != (0, 0):
            return p, q, t


def L10_C2_B4_VD028_MC_A_03(socau, dang=1):
    r"""GTLN/GTNN của F = ax + by trên miền đa giác cho bằng HÌNH VẼ."""
    cauTN = ''
    for _ in range(socau):
        m, n, u, v, _b1, _b2, dinh = _mien_tu_giac()
        hoi_lon = _rd.random() < 0.5
        p, q, t = _chon_F_co_dau(dinh, hoi_lon)
        ten = "lớn nhất" if hoi_lon else "nhỏ nhất"
        hinh = _hinh_mien_da_giac(dinh)
        gtri = [p * X + q * Y for X, Y in dinh]
        dung = "$%d$" % t
        khac = [g for g in dict.fromkeys(gtri) if g != t]
        nhieu = _ba_nhieu2(dung, ["$%d$" % g for g in khac] + ["$%d$" % (-t)],
                           buoc=lambda k: "$%d$" % (t + k + 1))
        debai = (r"Miền đa giác tô đậm trong hình vẽ (kể cả biên) là miền nghiệm của một "
                 r"hệ bất phương trình bậc nhất hai ẩn. Giá trị %s của biểu thức "
                 r"$F\left(x; y\right) = %s$ trên miền đó bằng" % (ten, _F_tex(p, q)))
        giai = (r"Đọc trên hình, miền nghiệm là tứ giác có bốn đỉnh $\left(0;0\right)$, "
                r"$\left(%d;0\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$." % (m, u, v, n) +
                "\\\\\n" + r"$F$ đạt giá trị %s tại một đỉnh:\\ " % ten + _bang_F(dinh, p, q) +
                "." + "\\\\\n" + r"Vậy giá trị %s của $F$ bằng $%d$." % (ten, t))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C2_B4_VD028_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn: GTLN của F trên miền đa giác cho bằng HÌNH VẼ."""
    cau = ''
    for _ in range(socau):
        m, n, u, v, _b1, _b2, dinh = _mien_tu_giac()
        p, q, t = _chon_F_co_dau(dinh, True)
        hinh = _hinh_mien_da_giac(dinh)
        debai = (r"Miền tứ giác tô đậm trong hình vẽ (kể cả biên) là miền nghiệm của một "
                 r"hệ bất phương trình bậc nhất hai ẩn. Tìm giá trị lớn nhất của biểu thức "
                 r"$F\left(x; y\right) = %s$ trên miền đó." % _F_tex(p, q))
        giai = (r"Các đỉnh của miền: $\left(0;0\right)$, $\left(%d;0\right)$, "
                r"$\left(%d;%d\right)$, $\left(0;%d\right)$." % (m, u, v, n) +
                "\\\\\n" + _bang_F(dinh, p, q) + "." + "\\\\\n" +
                r"Giá trị lớn nhất của $F$ là $%d$." % t)
        nhieu = [str(t + 1), str(t - 1), str(t + 2)]
        cau += MC_SA_answer_text(debai, str(t), nhieu, giai, hinh, 0, dang)
    return cau


def _mien_khong_bi_chan():
    r"""Miền $x \ge 0$, $y \ge 0$, $a_1x + b_1y \ge c_1$, $a_2x + b_2y \ge c_2$ (không bị
    chặn) có ba đỉnh NGUYÊN $(0;N)$, $(u;v)$, $(M;0)$.

    Đường 1 qua $(0;N)$ và $(u;v)$: $(N - v)x + uy = uN$.
    Đường 2 qua $(u;v)$ và $(M;0)$: $vx + (M - u)y = vM$.
    Cần $(N - v)(M - u) > uv$ để $(u;v)$ thật sự là đỉnh.
    """
    while True:
        u, v = _rd.randint(1, 6), _rd.randint(1, 6)
        N = _rd.randint(v + 2, v + 10)
        M = _rd.randint(u + 2, u + 10)
        if (N - v) * (M - u) <= u * v:
            continue
        l1 = (N - v, u, u * N)
        l2 = (v, M - u, v * M)
        g1, g2 = _math.gcd(_math.gcd(*l1[:2]), l1[2]), _math.gcd(_math.gcd(*l2[:2]), l2[2])
        l1 = tuple(k // g1 for k in l1)
        l2 = tuple(k // g2 for k in l2)
        return (0, N), (u, v), (M, 0), l1, l2


def _bpt_ge_tex(a, b, c):
    return _bpt_tex(a, b, c).replace(r"\le", r"\ge")


def L10_C2_B4_VD028_SA_A_03(socau, dang=2):
    r"""Trả lời ngắn: GTNN của F = px + qy (p, q > 0) trên miền KHÔNG BỊ CHẶN
    $x \ge 0$, $y \ge 0$, $a_1x + b_1y \ge c_1$, $a_2x + b_2y \ge c_2$."""
    cau = ''
    lan = 0
    dem = 0
    while dem < socau and lan < 300:
        lan += 1
        R, Q, P, l1, l2 = _mien_khong_bi_chan()
        p, q = _rd.randint(1, 9), _rd.randint(1, 9)
        dinh = [R, Q, P]
        g = [p * X + q * Y for X, Y in dinh]
        t = min(g)
        if g.count(t) != 1:
            continue
        dem += 1
        debai = (r"Cho hệ bất phương trình $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$. "
                 r"Tìm giá trị nhỏ nhất của biểu thức $F\left(x; y\right) = %s$ trên miền "
                 r"nghiệm của hệ." % (_bpt_ge_tex(*l1), _bpt_ge_tex(*l2), _F_tex(p, q)))
        giai = (r"Miền nghiệm không bị chặn, có các đỉnh $\left(0;%d\right)$, "
                r"$\left(%d;%d\right)$, $\left(%d;0\right)$." % (R[1], Q[0], Q[1], P[0]) +
                "\\\\\n" +
                r"Vì hệ số của $x$, $y$ trong $F$ đều dương nên $F$ càng lớn khi đi ra xa; "
                r"giá trị nhỏ nhất đạt tại một đỉnh:\\ " + _bang_F(dinh, p, q) + "." +
                "\\\\\n" + r"Vậy giá trị nhỏ nhất của $F$ là $%d$." % t)
        nhieu = _ba_nhieu2(str(t), [str(x) for x in g if x != t] + [str(t + 1)],
                           buoc=lambda k: str(t + k + 1))
        cau += MC_SA_answer_text(debai, str(t), nhieu, giai, 0, 0, dang)
    return cau


_BOI_CANH_SAN_XUAT = [
    ("Một xưởng may làm hai loại áo: áo sơ mi và áo khoác. May một áo sơ mi cần "
     "{a1} mét vải và {a2} giờ công, may một áo khoác cần {b1} mét vải và {b2} giờ "
     "công. Mỗi ngày xưởng có không quá {c1} mét vải và {c2} giờ công. Mỗi áo sơ mi "
     "lãi {p} nghìn đồng, mỗi áo khoác lãi {q} nghìn đồng.",
     "áo sơ mi", "áo khoác", "mét vải", "giờ công", "nghìn đồng"),
    ("Một bác nông dân trồng ngô và khoai trên một khu đất. Mỗi sào ngô cần {a1} "
     "ngày công và {a2} bao phân, mỗi sào khoai cần {b1} ngày công và {b2} bao phân. "
     "Bác có không quá {c1} ngày công và {c2} bao phân. Mỗi sào ngô lãi {p} trăm "
     "nghìn đồng, mỗi sào khoai lãi {q} trăm nghìn đồng.",
     "sào ngô", "sào khoai", "ngày công", "bao phân", "trăm nghìn đồng"),
    ("Một tiệm bánh làm hai loại bánh: bánh mặn và bánh ngọt. Mỗi mẻ bánh mặn cần "
     "{a1} kg bột và {a2} giờ nướng, mỗi mẻ bánh ngọt cần {b1} kg bột và {b2} giờ "
     "nướng. Mỗi ngày tiệm có không quá {c1} kg bột và {c2} giờ nướng. Mỗi mẻ bánh "
     "mặn lãi {p} chục nghìn đồng, mỗi mẻ bánh ngọt lãi {q} chục nghìn đồng.",
     "mẻ bánh mặn", "mẻ bánh ngọt", "kg bột", "giờ nướng", "chục nghìn đồng"),
]


def L10_C2_B4_VD028_TL_A_02(socau, dong=1):
    r"""Tự luận: bài toán tối ưu thực tiễn - học sinh PHẢI TỰ LẬP hệ bất
    phương trình từ bối cảnh (sản xuất, trồng trọt, làm bánh), rồi tìm
    phương án lãi lớn nhất. (_01 cho sẵn hệ.)"""
    cauTN = ''
    dem, lan = 0, 0
    while dem < socau and lan < 500:
        lan += 1
        m, n, u, v, (A1, B1, C1), (A2, B2, C2), dinh = _mien_tu_giac()
        # bpt1: A1 x + B1 y <= C1 ; bpt2: A2 x + B2 y <= C2 -> tai nguyen 1, 2
        p, q = _rd.randint(2, 9), _rd.randint(2, 9)
        g = [p * X + q * Y for X, Y in dinh]
        if g.count(max(g)) != 1 or max(A1, B1, A2, B2) > 9:
            continue
        dem += 1
        bc = _rd.choice(_BOI_CANH_SAN_XUAT)
        de = bc[0].format(a1=A1, a2=A2, b1=B1, b2=B2, c1=C1, c2=C2, p=p, q=q)
        de = re.sub(r"(\d+)", r"$\1$", de)
        lon = max(g)
        dl = dinh[g.index(lon)]
        debai = (de + r" Gọi $x$, $y$ lần lượt là số %s và số %s." % (bc[1], bc[2]))
        he = (r"\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}"
              % (_bpt_tex(A1, B1, C1), _bpt_tex(A2, B2, C2)))
        ds_abcd = [
            (r"Lập hệ bất phương trình mô tả các điều kiện của bài toán.",
             he,
             r"Số %s và số %s không âm: $x \ge 0$, $y \ge 0$.\\ " % (bc[1], bc[2]) +
             r"Số %s cần dùng: $%s \le %d$.\\ " % (bc[3], _bt((A1, "x"), (B1, "y")), C1) +
             r"Số %s cần dùng: $%s \le %d$.\\ " % (bc[4], _bt((A2, "x"), (B2, "y")), C2) +
             r"Ta được hệ $%s$." % he),
            (r"Tìm phương án để tiền lãi lớn nhất.",
             r"\left(%d; %d\right)" % dl,
             r"Tiền lãi $F\left(x; y\right) = %s$. Miền nghiệm của hệ là tứ giác có các đỉnh "
             r"$\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$."
             % (_F_tex(p, q), m, u, v, n) + "\\\\\n" +
             r"$F$ đạt giá trị lớn nhất tại một đỉnh:\\ " + _bang_F(dinh, p, q) + "." + "\\\\\n" +
             r"Vậy cần làm $%d$ %s và $%d$ %s, tiền lãi lớn nhất là $%d$ %s."
             % (dl[0], bc[1], dl[1], bc[2], lon, bc[5])),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


_BOI_CANH_CHI_PHI = [
    ("Một trại chăn nuôi trộn hai loại thức ăn I và II cho gà. Mỗi kg thức ăn I chứa "
     "{a1} đơn vị đạm và {a2} đơn vị khoáng, mỗi kg thức ăn II chứa {b1} đơn vị đạm "
     "và {b2} đơn vị khoáng. Mỗi ngày đàn gà cần ít nhất {c1} đơn vị đạm và {c2} đơn "
     "vị khoáng. Giá mỗi kg thức ăn I là {p} nghìn đồng, thức ăn II là {q} nghìn đồng.",
     "kg thức ăn I", "kg thức ăn II", "đơn vị đạm", "đơn vị khoáng"),
    ("Một bếp ăn cần mua hai loại rau A và B. Mỗi kg rau A cung cấp {a1} đơn vị "
     "vitamin C và {a2} đơn vị chất xơ, mỗi kg rau B cung cấp {b1} đơn vị vitamin C và "
     "{b2} đơn vị chất xơ. Mỗi bữa cần ít nhất {c1} đơn vị vitamin C và {c2} đơn vị "
     "chất xơ. Giá mỗi kg rau A là {p} nghìn đồng, rau B là {q} nghìn đồng.",
     "kg rau A", "kg rau B", "đơn vị vitamin C", "đơn vị chất xơ"),
]


def L10_C2_B4_VD028_TL_A_03(socau, dong=1):
    r"""Tự luận: bài toán CHI PHÍ NHỎ NHẤT (điều kiện ``ít nhất'' - miền không
    bị chặn): lập hệ bất phương trình rồi tìm phương án rẻ nhất."""
    cauTN = ''
    dem, lan = 0, 0
    while dem < socau and lan < 500:
        lan += 1
        R, Q, P, (A1, B1, C1), (A2, B2, C2) = _mien_khong_bi_chan()
        if max(A1, B1, A2, B2) > 9:
            continue
        p, q = _rd.randint(10, 40), _rd.randint(10, 40)
        dinh = [R, Q, P]
        g = [p * X + q * Y for X, Y in dinh]
        if g.count(min(g)) != 1:
            continue
        dem += 1
        bc = _rd.choice(_BOI_CANH_CHI_PHI)
        de = bc[0].format(a1=A1, b1=B1, a2=A2, b2=B2, c1=C1, c2=C2, p=p, q=q)
        de = re.sub(r"(\d+)", r"$\1$", de)
        nho = min(g)
        dn = dinh[g.index(nho)]
        he = (r"\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}"
              % (_bpt_ge_tex(A1, B1, C1), _bpt_ge_tex(A2, B2, C2)))
        debai = de + r" Gọi $x$, $y$ lần lượt là số %s và số %s cần mua." % (bc[1], bc[2])
        ds_abcd = [
            (r"Lập hệ bất phương trình mô tả các điều kiện của bài toán.", he,
             r"$x \ge 0$, $y \ge 0$; tổng số %s: $%s \ge %d$; tổng số %s: $%s \ge %d$.\\ "
             % (bc[3], _bt((A1, "x"), (B1, "y")), C1, bc[4], _bt((A2, "x"), (B2, "y")), C2) +
             r"Ta được hệ $%s$." % he),
            (r"Cần mua bao nhiêu mỗi loại để chi phí nhỏ nhất? Tính chi phí đó.",
             r"%d" % nho,
             r"Chi phí $F\left(x; y\right) = %s$ (nghìn đồng). Miền nghiệm không bị chặn, có "
             r"các đỉnh $\left(0;%d\right)$, $\left(%d;%d\right)$, $\left(%d;0\right)$."
             % (_F_tex(p, q), R[1], Q[0], Q[1], P[0]) + "\\\\\n" +
             r"Hệ số của $x$, $y$ đều dương nên $F$ nhỏ nhất tại một đỉnh:\\ " +
             _bang_F(dinh, p, q) + "." + "\\\\\n" +
             r"Vậy mua $%d$ %s và $%d$ %s, chi phí nhỏ nhất là $%d$ nghìn đồng."
             % (dn[0], bc[1], dn[1], bc[2], nho)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# ---------------------------------------------------------------------
# CLAUDE SUA 07/10/2026 (co Lan duyet) - viet lai L10_C2_TF_A_01:
#  * a, b, c co ca am; dau bat phuong trinh ngau nhien <, <=, >, >=.
#  * Duong bo d luon cat hai truc tao tam giac vuong; tam giac o goc phan tu
#    nao thi x, y mang dau tuong ung (nguyen duong / am / khong am / khong duong).
#  * y d): bo rang buoc 0<=x<=k. Mien nghiem chua O -> dem so cap nguyen
#    trong tam giac (nhieu: N+s). Mien nghiem khong chua O -> "co vo so cap"
#    (nhieu: so cap trong tam giac o nua mat phang ben kia).
# Ban cu luu o nhap/TF_A_01_ban_cu.py.
# ---------------------------------------------------------------------

_TFA_LATEX = {"<=": r"\le", "<": "<", ">=": r"\ge", ">": ">"}
# Doi sang nua mat phang ben kia cua bo d, giu nguyen ngat / khong ngat:
# dung de lam NHIEU cho y d) (hoc sinh xet lon ben).
_TFA_DAO = {"<=": ">=", "<": ">", ">=": "<=", ">": "<"}


def _tfa_thoa(v, ky, c):
    """v ky c co dung khong (ky la mot trong <=, <, >=, >)."""
    return {"<=": v <= c, "<": v < c, ">=": v >= c, ">": v > c}[ky]


def _tfa_so(n):
    """So nguyen dung trong tich: am thi boc ngoac."""
    return "(%d)" % n if n < 0 else "%d" % n


def _tfa_bieu_thuc(a, b):
    """Ve trai ax + by viet gon (bo he so 1, xu ly dau)."""
    t1 = "x" if a == 1 else ("-x" if a == -1 else "%dx" % a)
    if b > 0:
        t2 = "+ " + ("y" if b == 1 else "%dy" % b)
    else:
        t2 = "- " + ("y" if b == -1 else "%dy" % -b)
    return t1 + " " + t2


def _tfa_dieu_kien_xy(sx, sy, chat_x, chat_y):
    """Cau chu dieu kien cua x, y. chat=True: nguyen duong/am; False: khong am/khong duong."""
    def tu(sg, chat):
        if sg > 0:
            return "dương" if chat else "không âm"
        return "âm" if chat else "không dương"
    wx, wy = tu(sx, chat_x), tu(sy, chat_y)
    if wx == wy:
        return r"$x$, $y$ đều là số nguyên %s" % wx
    return r"$x$ là số nguyên %s, $y$ là số nguyên %s" % (wx, wy)


def _tfa_goc_phan_tu(sx, sy):
    """Ten goc phan tu chua tam giac."""
    return {(1, 1): "I", (-1, 1): "II", (-1, -1): "III", (1, -1): "IV"}[(sx, sy)]


def _tfa_tao_tham_so():
    """Sinh tham so mot cau. Tra ve dict.

    Duong thang d: a x + b y = c cat Ox tai (sx*m; 0), cat Oy tai (0; sy*n)
    (m, n nguyen duong) nen d cung hai truc luon tao tam giac vuong o goc
    phan tu (sx, sy). Nhan ca ba he so voi -1 (ngau nhien) de a, b, c co ca am.
    """
    while True:
        sx, sy = _rd.choice([1, -1]), _rd.choice([1, -1])
        m, n = _rd.randint(2, 6), _rd.randint(2, 6)
        p, q = sx * m, sy * n                      # hoanh do, tung do giao diem
        g = _math.gcd(m, n)
        a, b, c = q // g, p // g, (p * q) // g     # q*x + p*y = p*q, rut gon
        if _rd.random() < 0.5:
            a, b, c = -a, -b, -c
        ky = _rd.choice(["<=", "<", ">=", ">"])
        co_O = _tfa_thoa(0, ky, c)                     # nua mat phang nghiem co chua O?

        chat_x, chat_y = _rd.choice([True, False]), _rd.choice([True, False])
        xs = [sx * i for i in range(1 if chat_x else 0, m + 1)]
        ys = [sy * j for j in range(1 if chat_y else 0, n + 1)]
        theo_x = [(X, sum(1 for Y in ys if _tfa_thoa(a * X + b * Y, ky, c))) for X in xs]
        dem = sum(k for _x, k in theo_x)           # dem trong hcn |x|<=m, |y|<=n
        if co_O:
            if dem < 3:                            # tam giac chua toi thieu 3 diem
                continue
            s = _rd.choice([t for t in (-3, -2, -1, 1, 2, 3) if dem + t >= 1])
            T = None
        else:
            # nhieu: xet lon sang nua mat phang ben kia (chua O, tao tam giac voi hai truc)
            ky_dao = _TFA_DAO[ky]
            dem = sum(1 for X in xs for Y in ys if _tfa_thoa(a * X + b * Y, ky_dao, c))
            if dem < 2:
                continue
            s = 0
            T = next(t for t in range(1, 200) if _tfa_thoa(a * sx * t + b * sy * t, ky, c))
        return dict(chat_x=chat_x, chat_y=chat_y, sx=sx, sy=sy, m=m, n=n, p=p, q=q, a=a, b=b, c=c, ky=ky,
                    co_O=co_O, theo_x=theo_x, dem=dem, s=s, T=T)


def _tfa_ps(num, den=1):
    """Phân số tối giản viết LaTeX (mẫu bằng 1 thì chỉ viết tử)."""
    g = _math.gcd(abs(num), abs(den)) or 1
    num, den = num // g, den // g
    return "%d" % num if den == 1 else r"\dfrac{%d}{%d}" % (num, den)


def _tfa_m(noi_dung, dung, ly):
    r"""Một phát biểu của ý TF: (nội dung có \True nếu đúng, lời giải có Đúng./Sai.)."""
    return ((r"{\True " if dung else "{") + noi_dung + "}", ("Đúng. " if dung else "Sai. ") + ly)


def _tfa_ds(dung, sai):
    """[(nội dung, lời giải)] phát biểu ĐÚNG + SAI -> danh sách của một ý (bỏ nội dung trùng)."""
    y, da = [], set()
    for d, l in dung:
        if d not in da:
            da.add(d)
            y.append((r"{\True %s}" % d, "Đúng. " + l))
    for d, l in sai:
        if d not in da:
            da.add(d)
            y.append((r"{%s}" % d, "Sai. " + l))
    return y


def _tfa_thuoc_he(t, X, Y):
    """(X; Y) có là nghiệm của hệ { bất phương trình ; x ⋈ 0 ; y ⋈ 0 } không."""
    sx, sy = t["sx"], t["sy"]
    ok_x = (X > 0 if sx > 0 else X < 0) if t["chat_x"] else (X >= 0 if sx > 0 else X <= 0)
    ok_y = (Y > 0 if sy > 0 else Y < 0) if t["chat_y"] else (Y >= 0 if sy > 0 else Y <= 0)
    return ok_x and ok_y and _tfa_thoa(t["a"] * X + t["b"] * Y, t["ky"], t["c"])


def _tfa_y_d(t):
    """Ý d) (VDC) của L10_C2_TF_A_01, _03, _04: khẳng định về HỆ bất phương trình gồm bất phương
    trình đã cho cùng hai điều kiện x ⋈ 0, y ⋈ 0 (dấu theo góc phần tư, ngặt / không ngặt).
    Đúng/sai tính bằng _tfa_thuoc_he (không gán nhãn tay). Mỗi ý có nhiều hơn 3 phát biểu đúng và 3 sai."""
    sx, sy, a, b, c, ky = t["sx"], t["sy"], t["a"], t["b"], t["c"], t["ky"]
    m, n, p, q = t["m"], t["n"], t["p"], t["q"]
    co_O, dem, s = t["co_O"], t["dem"], t["s"]
    vt = _tfa_bieu_thuc(a, b)
    ks = _TFA_LATEX[ky]
    dx = (">" if t["chat_x"] else r"\ge") if sx > 0 else ("<" if t["chat_x"] else r"\le")
    dy = (">" if t["chat_y"] else r"\ge") if sy > 0 else ("<" if t["chat_y"] else r"\le")
    he = r"\heva{& %s %s %d \\& x %s 0 \\& y %s 0}" % (vt, ks, c, dx, dy)
    tien_to = r"Hệ bất phương trình $%s$ " % he
    goc = _tfa_goc_phan_tu(sx, sy)
    S_tex = _tfa_ps(m * n, 2)

    giao = (r"Đường thẳng $d$ cắt $Ox$ tại $\left(%d; 0\right)$ và cắt $Oy$ tại "
            r"$\left(0; %d\right)$, nên cùng hai trục toạ độ tạo thành một tam giác vuông "
            r"nằm ở góc phần tư thứ %s." % (p, q, goc))
    giai = giao + (r"\\ Các điều kiện $x %s 0$, $y %s 0$ giới hạn miền nghiệm trong góc phần tư thứ %s."
                   % (dx, dy, goc))
    if co_O:
        chi_tiet = r"\\ ".join(r"Với $x = %d$ có $%d$ giá trị nguyên $y$ thoả mãn" % (X, k)
                               for X, k in t["theo_x"])
        giai += (r"\\ Nửa mặt phẳng nghiệm của bất phương trình đầu chứa $O$ nên miền nghiệm của hệ "
                 r"là tam giác nói trên (miền bị chặn), có diện tích $\dfrac{1}{2}\cdot %d\cdot %d = %s$.\\ %s\\ "
                 r"Cộng lại được $%d$ nghiệm nguyên." % (m, n, S_tex, chi_tiet, dem))
    else:
        T = t["T"]
        giai += (r"\\ Nửa mặt phẳng nghiệm của bất phương trình đầu KHÔNG chứa $O$ nên miền nghiệm của hệ "
                 r"nằm về phía xa tam giác nói trên: đó là miền không bị chặn. Chẳng hạn mọi cặp số "
                 r"$\left(%s; %s\right)$ với $t$ nguyên, $t \ge %d$ đều là nghiệm, nên có vô số nghiệm nguyên.\\ "
                 r"Nếu xét nhầm sang nửa mặt phẳng bên kia (chứa $O$) thì chỉ đếm được $%d$ nghiệm nguyên "
                 r"nằm trong tam giác, đó là kết quả sai."
                 % ("t" if sx > 0 else "-t", "t" if sy > 0 else "-t", T, dem))

    def giai_diem(X, Y):
        v = a * X + b * Y
        ok_bpt = _tfa_thoa(v, ky, c)
        ok_x = (X > 0 if sx > 0 else X < 0) if t["chat_x"] else (X >= 0 if sx > 0 else X <= 0)
        ok_y = (Y > 0 if sy > 0 else Y < 0) if t["chat_y"] else (Y >= 0 if sy > 0 else Y <= 0)
        ket = lambda ok: "đúng" if ok else "sai"
        return (r"Thay $x = %d$, $y = %d$: $%d %s %d$ là mệnh đề %s; $%d %s 0$ là mệnh đề %s; "
                r"$%d %s 0$ là mệnh đề %s. Vậy cặp số $\left(%d; %d\right)$ %s nghiệm của hệ."
                % (X, Y, v, ks, c, ket(ok_bpt), X, dx, ket(ok_x), Y, dy, ket(ok_y), X, Y,
                   "là" if (ok_bpt and ok_x and ok_y) else "không phải là"))

    dung, sai = [], []

    def them(pred, truth, ly):
        (dung if truth else sai).append((tien_to + pred, ly))

    # miền nghiệm nằm ở góc phần tư nào
    them(r"có miền nghiệm nằm trong góc phần tư thứ %s" % goc, True, giai)
    for g2 in _rd.sample([x for x in ("I", "II", "III", "IV") if x != goc], 2):
        them(r"có miền nghiệm nằm trong góc phần tư thứ %s" % g2, False, giai)
    # bị chặn hay không, hình dạng
    them(r"có miền nghiệm là một miền tam giác", co_O, giai)
    them(r"có miền nghiệm là một miền tứ giác", False, giai)
    them(r"có miền nghiệm là một miền bị chặn", co_O, giai)
    them(r"có miền nghiệm là một miền không bị chặn", not co_O, giai)
    # số nghiệm
    them(r"có vô số nghiệm $\left(x; y\right)$", True, giai)
    them(r"vô nghiệm", False, giai)
    them(r"có đúng một nghiệm", False, giai)
    if co_O:
        # diện tích, số nghiệm nguyên
        them(r"có miền nghiệm với diện tích bằng $%s$ (đơn vị diện tích)" % S_tex, True, giai)
        da = {m * n}
        for num, den in ((m * n, 1), (m * n, 4), (m + n, 2), (m + n, 1)):
            if num * 2 != m * n * den and (num, den) not in da:        # khác m*n/2
                da.add((num, den))
                them(r"có miền nghiệm với diện tích bằng $%s$ (đơn vị diện tích)" % _tfa_ps(num, den), False, giai)
        them(r"có đúng $%d$ nghiệm nguyên $\left(x; y\right)$" % dem, True, giai)
        sai_dem = []
        for d_ in (s, 1, -1, 2):
            v = dem + d_
            if v >= 1 and v != dem and v not in sai_dem:
                sai_dem.append(v)
        for v in sai_dem[:2]:
            them(r"có đúng $%d$ nghiệm nguyên $\left(x; y\right)$" % v, False, giai)
    else:
        them(r"có vô số nghiệm nguyên $\left(x; y\right)$", True, giai)
        them(r"có đúng $%d$ nghiệm nguyên $\left(x; y\right)$" % dem, False, giai)
        them(r"không có nghiệm nguyên nào", False, giai)
    # một số cặp số: nghiệm của hệ hay không (đúng / sai tính trực tiếp)
    luoi = [(X, Y) for X in range(-8, 9) for Y in range(-8, 9)]
    nghiem = [P for P in luoi if _tfa_thuoc_he(t, *P)]
    pha_dk = [P for P in luoi if not _tfa_thuoc_he(t, *P) and _tfa_thoa(a * P[0] + b * P[1], ky, c)]
    pha_bpt = [P for P in luoi if not _tfa_thuoc_he(t, *P) and not _tfa_thoa(a * P[0] + b * P[1], ky, c)]
    diem = [(0, 0), _rd.choice(nghiem), _rd.choice(pha_dk or pha_bpt), _rd.choice(pha_bpt or pha_dk)]
    for X, Y in dict.fromkeys(diem):
        ok = _tfa_thuoc_he(t, X, Y)
        gd = giai_diem(X, Y)
        them(r"nhận cặp số $\left(%d; %d\right)$ làm một nghiệm" % (X, Y), ok, gd)
        them(r"không nhận cặp số $\left(%d; %d\right)$ làm nghiệm" % (X, Y), not ok, gd)
    return _tfa_ds(dung, sai)


def L10_C2_TF_A_01(socau, socot=1):
    """Đúng/Sai - bất phương trình bậc nhất hai ẩn (bản nháp phát triển)."""
    cauTF = ''
    for _ in range(socau):
        t = _tfa_tao_tham_so()
        sx, sy, a, b, c, ky = t["sx"], t["sy"], t["a"], t["b"], t["c"], t["ky"]
        co_O, dem, s = t["co_O"], t["dem"], t["s"]
        vt = _tfa_bieu_thuc(a, b)
        ks = _TFA_LATEX[ky]
        bpt = r"%s %s %d" % (vt, ks, c)
        duong = r"d \colon %s = %d" % (vt, c)
        ngat = ky in ("<", ">")

        debai = (r"Cho bất phương trình $%s$. "
                 r"Xét tính đúng sai của các khẳng định sau:" % bpt)

        # a) NB - nhan dang
        ly_do = (r"Nó có dạng $ax + by %s c$ với $a = %d$, $b = %d$ không đồng thời "
                 r"bằng $0$, và $x$, $y$ đều bậc nhất." % (ks, a, b))
        ten = r"``Bất phương trình $%s$ %s bất phương trình bậc nhất hai ẩn''"
        y1 = [(r"{\True Bất phương trình đã cho là bất phương trình bậc nhất hai ẩn}",
               r"Đúng. " + ly_do),
              (r"{Bất phương trình đã cho không phải là bất phương trình bậc nhất hai ẩn}",
               r"Sai. " + ly_do),
              (r"{\True " + ten % (bpt, "là") + r" là mệnh đề đúng}", r"Đúng. " + ly_do),
              (r"{" + ten % (bpt, "là") + r" là mệnh đề sai}", r"Sai. " + ly_do),
              (r"{" + ten % (bpt, "không phải là") + r" là mệnh đề đúng}", r"Sai. " + ly_do),
              (r"{\True " + ten % (bpt, "không phải là") + r" là mệnh đề sai}", r"Đúng. " + ly_do)]

        # b) TH - thay so kiem tra: mot cap bat ki va hai giao diem cua d voi hai truc
        y2 = []
        for x0, y0 in dict.fromkeys([(_rd.randint(-4, 4), _rd.randint(-4, 4)), (t["p"], 0), (0, t["q"])]):
            ve = a * x0 + b * y0
            dung_b = _tfa_thoa(ve, ky, c)
            thay = (r"Thay vào vế trái: $%s\cdot %s + %s\cdot %s = %d$. "
                    r"Ta có $%d %s %d$ là mệnh đề %s nên cặp số này %s nghiệm của bất phương trình."
                    % (_tfa_so(a), _tfa_so(x0), _tfa_so(b), _tfa_so(y0), ve, ve, ks, c,
                       "đúng" if dung_b else "sai", "là" if dung_b else "không phải là"))
            cap = r"\left(%d; %d\right)" % (x0, y0)
            y2 += [_tfa_m(r"Cặp số $%s$ là một nghiệm của bất phương trình" % cap, dung_b, thay),
                   _tfa_m(r"Cặp số $%s$ không phải là nghiệm của bất phương trình" % cap, not dung_b, thay),
                   _tfa_m(r"Điểm $%s$ thuộc miền nghiệm của bất phương trình" % cap, dung_b, thay),
                   _tfa_m(r"Điểm $%s$ không thuộc miền nghiệm của bất phương trình" % cap, not dung_b, thay)]

        # c) VD - hinh dung nua mat phang nghiem
        # Su that: co_O (chua O hay khong), ngat (khong ke bo d hay co ke bo d)
        thu_O = (r"Thay $O\left(0;0\right)$ vào vế trái được $0$; $0 %s %d$ là mệnh đề %s "
                 r"nên $O$ %s miền nghiệm.\\ Bất phương trình %s nên đường thẳng $d$ %s miền nghiệm."
                 % (ks, c, "đúng" if co_O else "sai", "thuộc" if co_O else "không thuộc",
                    "ngặt" if ngat else "không ngặt", "không thuộc" if ngat else "thuộc"))

        def mo_ta1(chua, ke_bo):
            return (r"Miền nghiệm của bất phương trình là nửa mặt phẳng bờ là đường thẳng "
                    r"$%s$, %s gốc toạ độ $O$ và %s đường thẳng $d$"
                    % (duong, "chứa" if chua else "không chứa",
                       "kể cả" if ke_bo else "không kể"))

        def mo_ta2(chua, ke_bo):
            return (r"Gốc toạ độ $O$ %s miền nghiệm của bất phương trình, còn các điểm "
                    r"nằm trên đường thẳng $%s$ %s miền nghiệm"
                    % ("thuộc" if chua else "không thuộc", duong,
                       "thuộc" if ke_bo else "không thuộc"))

        dung_O, dung_bo = co_O, (not ngat)
        sai = _rd.choice([(not dung_O, dung_bo), (dung_O, not dung_bo),
                          (not dung_O, not dung_bo)])
        sai2 = _rd.choice([(not dung_O, dung_bo), (dung_O, not dung_bo),
                           (not dung_O, not dung_bo)])
        y3 = [(r"{\True " + mo_ta1(dung_O, dung_bo) + "}", "Đúng. " + thu_O),
              (r"{" + mo_ta1(*sai) + "}", "Sai. " + thu_O),
              (r"{\True " + mo_ta2(dung_O, dung_bo) + "}", "Đúng. " + thu_O),
              (r"{" + mo_ta2(*sai2) + "}", "Sai. " + thu_O)]

        y3 += [_tfa_m(r"Miền nghiệm của bất phương trình chứa gốc toạ độ $O$", co_O, thu_O),
               _tfa_m(r"Miền nghiệm của bất phương trình không chứa gốc toạ độ $O$", not co_O, thu_O),
               _tfa_m(r"Các điểm nằm trên đường thẳng $%s$ thuộc miền nghiệm của bất phương trình" % duong, not ngat, thu_O),
               _tfa_m(r"Các điểm nằm trên đường thẳng $%s$ không thuộc miền nghiệm của bất phương trình" % duong, ngat, thu_O)]

        # d) VDC - HE bat phuong trinh gom bat phuong trinh da cho va x ⋈ 0, y ⋈ 0 (xem _tfa_y_d)
        y4 = _tfa_y_d(t)

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def _tfb_thuoc(bpt1, bpt2, X, Y):
    """(X; Y) có thuộc miền nghiệm của hệ { x >= 0 ; y >= 0 ; bpt1 ; bpt2 } không."""
    (a1, b1, c1), (a2, b2, c2) = bpt1, bpt2
    return X >= 0 and Y >= 0 and a1 * X + b1 * Y <= c1 and a2 * X + b2 * Y <= c2


def L10_C2_TF_B_01(socau, socot=1):
    r"""Đúng/Sai - hệ bất phương trình bậc nhất hai ẩn $x \ge 0$, $y \ge 0$ và hai bất phương trình
    khác (miền nghiệm là tứ giác nguyên đỉnh) kèm biểu thức $F = px + qy$.

    NANG CAP 09/10/2026 (co Lan duyet): moi y co it nhat 3 phat bieu dung + 3 phat bieu sai
    (truoc day moi y chi 1 dung + 1 sai). Dung/sai tinh truc tiep tu cac dinh, dien tich, F.
    """
    cauTF = ''
    for _ in range(socau):
        while True:
            m, n, u, v, bpt1, bpt2, dinh = _mien_tu_giac()
            p, q = _rd.randint(1, 9), _rd.randint(1, 9)
            gtri = [p * X + q * Y for X, Y in dinh]
            if gtri.count(max(gtri)) == 1:
                break
        (a1, b1, c1), (a2, b2, c2) = bpt1, bpt2
        t1, t2 = _bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2)
        lon = max(gtri)
        dinh_lon = dinh[gtri.index(lon)]
        S2 = m * v + u * n                                   # hai lan dien tich tu giac OPQR

        debai = (r"Cho hệ bất phương trình $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$ "
                 r"và biểu thức $F\left(x; y\right) = %s$. "
                 r"Xét tính đúng sai của các khẳng định sau:"
                 % (t1, t2, _F_tex(p, q)))

        # a) NB - nhan dang he
        ly_a = (r"Bốn bất phương trình $x \ge 0$, $y \ge 0$, $%s$, $%s$ đều có dạng $ax + by \le c$ "
                r"hoặc $ax + by \ge c$ với $a$, $b$ không đồng thời bằng $0$, nên hệ gồm $4$ bất "
                r"phương trình bậc nhất hai ẩn." % (t1, t2))
        y1 = _tfa_ds(
            [(r"Hệ đã cho là hệ bất phương trình bậc nhất hai ẩn", ly_a),
             (r"Hệ đã cho gồm $4$ bất phương trình", ly_a),
             (r"Mỗi bất phương trình của hệ đều là bất phương trình bậc nhất hai ẩn", ly_a),
             (r"Bất phương trình $%s$ có hệ số của $y$ bằng $%d$" % (t1, b1), ly_a)],
            [(r"Hệ đã cho không phải là hệ bất phương trình bậc nhất hai ẩn", ly_a),
             (r"Hệ đã cho gồm $3$ bất phương trình", ly_a),
             (r"Hệ đã cho gồm $5$ bất phương trình", ly_a),
             (r"Trong hệ có một bất phương trình không phải là bất phương trình bậc nhất hai ẩn", ly_a),
             (r"Bất phương trình $%s$ có hệ số của $x$ bằng $%d$" % (t2, a2 + 1), ly_a)])

        # b) TH - thay toa do mot so diem vao he (dung / sai tinh truc tiep)
        luoi = [(X, Y) for X in range(-3, 15) for Y in range(-3, 15)]
        trong = [P for P in luoi if _tfb_thuoc(bpt1, bpt2, *P) and P[0] > 0 and P[1] > 0
                 and P not in dinh]
        ra_bpt = [P for P in luoi if P[0] >= 0 and P[1] >= 0 and not _tfb_thuoc(bpt1, bpt2, *P)]
        ra_truc = [P for P in luoi if (P[0] < 0 or P[1] < 0)
                   and a1 * P[0] + b1 * P[1] <= c1 and a2 * P[0] + b2 * P[1] <= c2]
        diem = [(u, v), (0, 0), _rd.choice(trong), _rd.choice(ra_bpt), _rd.choice(ra_truc)]

        def giai_diem(X, Y):
            kq = lambda ok: "đúng" if ok else "sai"
            v1, v2 = a1 * X + b1 * Y, a2 * X + b2 * Y
            return (r"Thay $x = %d$, $y = %d$: $%d \ge 0$ là mệnh đề %s; $%d \ge 0$ là mệnh đề %s; "
                    r"$%d \le %d$ là mệnh đề %s; $%d \le %d$ là mệnh đề %s. Vậy điểm "
                    r"$\left(%d; %d\right)$ %s miền nghiệm của hệ."
                    % (X, Y, X, kq(X >= 0), Y, kq(Y >= 0), v1, c1, kq(v1 <= c1),
                       v2, c2, kq(v2 <= c2), X, Y,
                       "thuộc" if _tfb_thuoc(bpt1, bpt2, X, Y) else "không thuộc"))
        dung_b, sai_b = [], []
        for X, Y in dict.fromkeys(diem):
            ok = _tfb_thuoc(bpt1, bpt2, X, Y)
            gd = giai_diem(X, Y)
            (dung_b if ok else sai_b).append((r"Điểm $\left(%d; %d\right)$ thuộc miền nghiệm của hệ" % (X, Y), gd))
            (sai_b if ok else dung_b).append((r"Điểm $\left(%d; %d\right)$ không thuộc miền nghiệm của hệ" % (X, Y), gd))
        y2 = _tfa_ds(dung_b, sai_b)

        # c) VD - giai he de biet hinh dang, dinh, dien tich cua mien nghiem
        S_tex = _tfa_ps(S2, 2)
        ly_c = (r"Giải các cặp đường bờ ta được bốn đỉnh $\left(0;0\right)$, $\left(%d;0\right)$, "
                r"$\left(%d;%d\right)$, $\left(0;%d\right)$; miền nghiệm là tứ giác lồi, bị chặn.\\ "
                r"Chia tứ giác thành hai tam giác có chung cạnh nối gốc $O$ với $\left(%d;%d\right)$: "
                r"$S = \dfrac{1}{2}\cdot %d\cdot %d + \dfrac{1}{2}\cdot %d\cdot %d = %s$."
                % (m, u, v, n, u, v, m, v, n, u, S_tex))
        sai_dt = []
        for num in (S2 + 2, S2 - 2, S2 + 4, 2 * m * n):
            if num > 0 and num != S2 and _tfa_ps(num, 2) not in sai_dt:
                sai_dt.append(_tfa_ps(num, 2))
        y3 = _tfa_ds(
            [(r"Miền nghiệm của hệ là một miền tứ giác", ly_c),
             (r"Miền nghiệm của hệ là một miền bị chặn", ly_c),
             (r"Miền nghiệm của hệ có đúng $4$ đỉnh", ly_c),
             (r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % (u, v), ly_c),
             (r"Miền nghiệm có diện tích bằng $%s$ (đơn vị diện tích)" % S_tex, ly_c)],
            [(r"Miền nghiệm của hệ là một miền tam giác", ly_c),
             (r"Miền nghiệm của hệ là một miền không bị chặn", ly_c),
             (r"Miền nghiệm của hệ có đúng $3$ đỉnh", ly_c),
             (r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % (m, n), ly_c)]
            + [(r"Miền nghiệm có diện tích bằng $%s$ (đơn vị diện tích)" % s, ly_c) for s in sai_dt[:2]])

        # d) VDC - gia tri lon nhat / nho nhat cua F tren mien nghiem
        ly_d = (r"Biểu thức bậc nhất $F$ đạt giá trị lớn nhất và nhỏ nhất tại các đỉnh của miền "
                r"nghiệm. Tính $F$ tại bốn đỉnh:\\ %s.\\ Lớn nhất là $%d$, đạt tại "
                r"$\left(%d; %d\right)$; nhỏ nhất là $0$, đạt tại gốc toạ độ $O$."
                % (_bang_F(dinh, p, q), lon, dinh_lon[0], dinh_lon[1]))
        khac = [d_ for d_ in dinh if d_ != dinh_lon]
        thu_hai = max(g_ for g_ in gtri if g_ != lon)
        nho_sai = min(g_ for g_ in gtri if g_ > 0)
        y4 = _tfa_ds(
            [(r"Giá trị lớn nhất của $F$ trên miền nghiệm bằng $%d$" % lon, ly_d),
             (r"$F$ đạt giá trị lớn nhất tại điểm $\left(%d; %d\right)$" % dinh_lon, ly_d),
             (r"Giá trị nhỏ nhất của $F$ trên miền nghiệm bằng $0$", ly_d),
             (r"$F$ đạt giá trị nhỏ nhất tại gốc toạ độ $O$", ly_d),
             (r"Tại đỉnh $\left(%d; %d\right)$, biểu thức $F$ nhận giá trị $%d$"
              % (u, v, p * u + q * v), ly_d)],
            [(r"Giá trị lớn nhất của $F$ trên miền nghiệm bằng $%d$" % (lon + p + q), ly_d),
             (r"Giá trị lớn nhất của $F$ trên miền nghiệm bằng $%d$" % thu_hai, ly_d),
             (r"$F$ đạt giá trị lớn nhất tại điểm $\left(%d; %d\right)$" % khac[0], ly_d),
             (r"$F$ đạt giá trị lớn nhất tại điểm $\left(%d; %d\right)$" % khac[1], ly_d),
             (r"Giá trị nhỏ nhất của $F$ trên miền nghiệm bằng $%d$" % nho_sai, ly_d),
             (r"$F$ không có giá trị lớn nhất trên miền nghiệm", ly_d)])

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


# =====================================================================
# BIẾN THỂ LẤY TỪ PHẦN "BÀI TẬP TRẮC NGHIỆM" BÀI 3 (BẤT PHƯƠNG TRÌNH BẬC
# NHẤT HAI ẨN) CỦA CÔ LAN - CLAUDE THEM 30/09/2026, co Lan duyet lai.
# Câu có hình (chọn hình miền nghiệm, đọc bất phương trình từ hình) đã có
# TH024_MC_A; ở đây chỉ làm các câu KHÔNG cần hình, hoặc mô tả miền nghiệm
# bằng lời để web hiện được.
# =====================================================================

def _bn_tex(a, b, c=0):
    """ax + by + c viết gọn (bỏ hệ số 1, bỏ số hạng 0)."""
    out = ""
    for k, ten in ((a, "x"), (b, "y"), (c, "")):
        if k == 0:
            continue
        so = ("" if abs(k) == 1 and ten else str(abs(k))) + ten
        if not out:
            out = ("-" if k < 0 else "") + so
        else:
            out += (" - " if k < 0 else " + ") + so
    return out or "0"


_DAU_KT = {"<": lambda v: v < 0, r"\le": lambda v: v <= 0, ">": lambda v: v > 0, r"\ge": lambda v: v >= 0}


def L10_C2_B3_NB022_MC_A_03(socau, dang=1):
    r"""Bất phương trình nào KHÔNG phải là bất phương trình bậc nhất hai ẩn?
    (có cả dạng khuyết một ẩn $x + 2 \ge 0$ và dạng phải khai triển mới thấy).

    CLAUDE THEM 30/09/2026 - bien the 03 cua NB022_MC_A, theo cac cau "x + y^2
    <= 7 khong phai; x + 2 >= 0 van la" va "(x + y)(x - y) >= 0" trong phan
    bai tap trac nghiem Bai 3. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        a, b = random.choice([i for i in range(-6, 7) if i]), random.choice([i for i in range(-6, 7) if i])
        c = random.randint(-9, 9)
        d = random.choice(list(_DAU_KT))
        khong = [(r"$%s %s %d$" % (_bn_tex(a, 0) + " + y^2" if a else "y^2", d, c), r"có $y^2$ (bậc hai)"),
                 (r"$(x + y)(x - y) %s 0$" % d, r"khai triển được $x^2 - y^2$ (bậc hai)"),
                 (r"$%sxy + y %s %d$" % ("" if abs(a) == 1 else a, d, c), r"có hạng tử $xy$ (bậc hai)"),
                 (r"$%s + \dfrac{1}{y} %s %d$" % (_bn_tex(a, 0), d, c), r"có $\dfrac{1}{y}$, không phải đa thức bậc nhất"),
                 (r"$x^3 %s %s %s %d$" % ("+" if b > 0 else "-", _bn_tex(0, abs(b)), d, c), r"có $x^3$")]
        k = random.randint(2, 5)
        la = [(r"$%s %s %d$" % (_bn_tex(a, b), d, c), "dạng $ax + by %s c$" % d),
              (r"$%s %s 0$" % (_bn_tex(a, 0, c), d), r"khuyết $y$ (hệ số của $y$ bằng $0$) nhưng vẫn là bậc nhất hai ẩn"),
              (r"$%dx - %d(y - x + %d) %s 0$" % (abs(a) + 1, k, abs(c) + 1, d),
               r"khai triển được $%s %s 0$" % (_bn_tex(abs(a) + 1 + k, -k, -k * (abs(c) + 1)), d)),
              (r"$%s %s %s$" % (_bn_tex(a, 0), d, _bn_tex(0, b, c)), r"chuyển vế được $%s %s 0$" % (_bn_tex(a, -b, -c), d))]
        sai = random.choice(khong)
        dung3 = random.sample(la, 3)
        debai = r"Trong các bất phương trình sau, bất phương trình nào \textbf{không phải} là bất phương trình bậc nhất hai ẩn?"
        giai = (r"%s không phải bất phương trình bậc nhất hai ẩn vì %s.\\ " % sai
                + r"\\ ".join(r"%s là bất phương trình bậc nhất hai ẩn (%s)." % t for t in dung3))
        cauTN += MC_SA_answer_text(debai, sai[0], [t[0] for t in dung3], giai, 0, 0, dang)
    return cauTN


def L10_C2_B3_NB023_MC_A_02(socau, dang=1):
    r"""Cho một điểm $M(x_0; y_0)$, chọn bất phương trình nhận $M$ làm nghiệm
    (hoặc KHÔNG nhận $M$ làm nghiệm).

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB023_MC_A, theo cac cau "Diem
    A(-1; 3) thuoc mien nghiem cua bat phuong trinh nao", "Cap so (-1; 4) la
    nghiem cua bat phuong trinh" trong phan bai tap trac nghiem Bai 3.
    Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        x0, y0 = random.randint(-4, 5), random.randint(-4, 5)
        hoi_thuoc = random.random() < 0.7
        dung_ds, sai_ds, da = [], [], set()
        for _t in range(200):
            a, b = random.choice([i for i in range(-5, 6) if i]), random.randint(-5, 5)
            c = random.randint(-8, 8)
            d = random.choice(list(_DAU_KT))
            v = a * x0 + b * y0 + c
            if v == 0 or (a, b, c) in da:
                continue                       # tránh điểm nằm trên bờ cho câu nhận biết
            da.add((a, b, c))
            muc = (r"$%s %s 0$" % (_bn_tex(a, b, c), d), a, b, c, d, v)
            (dung_ds if _DAU_KT[d](v) == hoi_thuoc else sai_ds).append(muc)
        if not dung_ds or len(sai_ds) < 3:
            continue
        chon, khac = dung_ds[0], sai_ds[:3]
        so += 1
        debai = (r"Cặp số $\left(%d; %d\right)$ %s nghiệm của bất phương trình nào sau đây?"
                 % (x0, y0, "là" if hoi_thuoc else r"\textbf{không} là"))

        def thay(m):
            _, a, b, c, d, v = m
            return r"$%s %s 0$: vế trái bằng $%d$, mà $%d %s 0$ %s" % (
                _bn_tex(a, b, c), d, v, v, d, "đúng" if _DAU_KT[d](v) else "sai")
        giai = (r"Thay $x = %d$, $y = %d$ vào vế trái của từng bất phương trình:\\ " % (x0, y0)
                + r"\\ ".join(thay(m) for m in [chon] + khac)
                + r".\\ Vậy chọn %s." % chon[0])
        cauTN += MC_SA_answer_text(debai, chon[0], [m[0] for m in khac], giai, 0, 0, dang)
    return cauTN


def _thuc_te_bpt():
    """Tình huống thực tế -> (đề, đáp án, nhiễu, lời giải). Bất phương trình đã rút gọn."""
    kieu = random.randint(0, 3)
    if kieu == 0:
        p, q = random.choice([(26, 20), (24, 18), (22, 16), (30, 20), (28, 21)])
        c = 2 * p
        g = math.gcd(math.gcd(p, q), c)
        de = (r"Trong $1$ lạng thịt bò có khoảng $%d$ g protein, trong $1$ lạng cá rô phi có khoảng $%d$ g "
              r"protein. Mỗi ngày một người cần tối thiểu $%d$ g protein. Gọi $x$, $y$ lần lượt là số lạng thịt bò "
              r"và số lạng cá rô phi người đó ăn trong một ngày. Bất phương trình mô tả lượng protein cần thiết là"
              % (p, q, c))
        dau, P, Q, C = r"\ge", p // g, q // g, c // g
        giai = (r"Lượng protein là $%dx + %dy$ (g). ``Tối thiểu $%d$ g'' nghĩa là $%dx + %dy \ge %d$, chia hai vế cho "
                r"$%d$ được $%dx + %dy \ge %d$." % (p, q, c, p, q, c, g, P, Q, C))
        sai = [(P, Q, ">", C), (P, Q, r"\le", C), (Q, P, r"\ge", C)]
    elif kieu == 1:
        p, q = random.choice([(1190, 1390), (1100, 1500), (1200, 1400), (990, 1290)])
        T = random.choice([100, 150, 200])
        g = math.gcd(math.gcd(p, q), 1000 * T)
        de = (r"Một gói cước điện thoại tính $%d$ đồng mỗi phút gọi nội mạng và $%d$ đồng mỗi phút gọi ngoại mạng. "
              r"Gọi $x$, $y$ lần lượt là số phút gọi nội mạng, ngoại mạng trong một tháng. Bất phương trình mô tả "
              r"số tiền phải trả trong tháng ít hơn $%d$ nghìn đồng là" % (p, q, T))
        dau, P, Q, C = "<", p // g, q // g, 1000 * T // g
        giai = (r"Số tiền là $%dx + %dy$ (đồng). ``Ít hơn $%d$ nghìn đồng'' nghĩa là $%dx + %dy < %d$, chia hai vế cho "
                r"$%d$ được $%dx + %dy < %d$." % (p, q, T, p, q, 1000 * T, g, P, Q, C))
        sai = [(P, Q, r"\le", C), (Q, P, "<", C), (P, Q, "<", T)]
    elif kieu == 2:
        p, q = random.choice([(15, 10), (20, 15), (25, 20), (30, 20), (18, 12)])
        c = random.choice([600, 900, 1200])
        g = math.gcd(math.gcd(p, q), c)
        de = (r"Ngoài giờ học, bạn Nam phụ bán cơm được $%d$ nghìn đồng một giờ và phụ bán tạp hoá được $%d$ nghìn "
              r"đồng một giờ. Gọi $x$, $y$ lần lượt là số giờ phụ bán cơm và phụ bán tạp hoá mỗi tuần. Bất phương "
              r"trình để Nam kiếm được ít nhất $%d$ nghìn đồng mỗi tuần là" % (p, q, c))
        dau, P, Q, C = r"\ge", p // g, q // g, c // g
        giai = (r"Số tiền kiếm được là $%dx + %dy$ (nghìn đồng). ``Ít nhất $%d$'' nghĩa là $%dx + %dy \ge %d$, chia hai "
                r"vế cho $%d$ được $%dx + %dy \ge %d$." % (p, q, c, p, q, c, g, P, Q, C))
        sai = [(P, Q, ">", C), (P, Q, r"\le", C), (Q, P, r"\ge", C)]
    else:
        F1, F2 = random.choice([(900, 1200), (800, 1000), (1000, 1500)])
        p, q = random.choice([(10, 15), (8, 12), (12, 18)])
        T = random.choice([20000, 25000, 30000])
        con = T - 5 * F1 - 2 * F2
        g = math.gcd(math.gcd(p, q), con)
        de = (r"Anh A thuê một chiếc ô tô trong một tuần. Từ thứ hai đến thứ sáu phí cố định là $%d$ nghìn đồng/ngày và "
              r"$%d$ nghìn đồng/km; thứ bảy và chủ nhật phí cố định là $%d$ nghìn đồng/ngày và $%d$ nghìn đồng/km. Gọi "
              r"$x$, $y$ lần lượt là số km anh A đi trong các ngày từ thứ hai đến thứ sáu và trong hai ngày cuối tuần. "
              r"Bất phương trình để tổng số tiền không quá $%d$ triệu đồng là" % (F1, p, F2, q, T // 1000))
        dau, P, Q, C = r"\le", p // g, q // g, con // g
        giai = (r"Tổng số tiền (nghìn đồng) là $5\cdot %d + %dx + 2\cdot %d + %dy$. ``Không quá $%d$ triệu'' nghĩa là "
                r"$%d + %dx + %dy \le %d$, tức là $%dx + %dy \le %d$; chia hai vế cho $%d$ được $%dx + %dy \le %d$."
                % (F1, p, F2, q, T // 1000, 5 * F1 + 2 * F2, p, q, T, p, q, con, g, P, Q, C))
        sai = [(P, Q, r"\ge", C), (P, Q, r"\le", T // g), (Q, P, r"\le", C)]
    dap = r"$%dx + %dy %s %d$" % (P, Q, dau, C)
    nhieu = [r"$%dx + %dy %s %d$" % s for s in sai]
    return de, dap, nhieu, giai


def L10_C2_B3_NB025_MC_A_02(socau, dang=1):
    r"""Viết bất phương trình mô tả tình huống thực tế (tối thiểu / ít nhất /
    ít hơn / không quá; có phí cố định; rút gọn hệ số).

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB025_MC_A, theo cac cau "protein
    thit bo - ca ro phi", "goi cuoc noi mang - ngoai mang", "Nam lam them",
    "thue o to" trong phan bai tap trac nghiem Bai 3. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        de, dap, nhieu, giai = _thuc_te_bpt()
        cauTN += MC_SA_answer_text(de, dap, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C2_TF_A_03(socau, socot=1):
    r"""Đúng/Sai - biết MIỀN NGHIỆM (mô tả bằng lời): bờ $d$ đi qua $A(p; 0)$, $B(0; q)$, miền nghiệm
    chứa / không chứa $O$, kể / không kể bờ (góc phần tư và dấu ngẫu nhiên như TF_A_01). Xét điểm
    $O$, $A$, $B$; phương trình $d$; bất phương trình; và (ý d) HỆ bất phương trình có thêm
    $x \gtrless 0$, $y \gtrless 0$.

    CLAUDE THEM 30/09/2026 - bien the 03 cua L10_C2_TF_A (theo hai cau "mien nghiem khong gach cheo,
    bo d qua (-5; 0), (0; 2)" va "qua (3; 0), (0; 2)" trong bai tap Bai 3). NANG CAP 09/10/2026 (co
    Lan duyet): phuc tap nhu TF_A_01/04, moi y it nhat 3 dung + 3 sai, y d) la HE bat phuong trinh.
    """
    from fractions import Fraction as _Fr
    cauTF = ""
    for _ in range(socau):
        t = _tfa_tao_tham_so()
        a, b, c, ky, p, q, co_O = t["a"], t["b"], t["c"], t["ky"], t["p"], t["q"], t["co_O"]
        ke = ky in ("<=", ">=")
        vt = _tfa_bieu_thuc(a, b)
        ks = _TFA_LATEX[ky]
        debai = (r"Cho một bất phương trình bậc nhất hai ẩn có miền nghiệm là nửa mặt phẳng %s gốc toạ độ $O$ "
                 r"(%s bờ $d$), trong đó đường thẳng $d$ đi qua hai điểm $A\left(%d; 0\right)$ và "
                 r"$B\left(0; %d\right)$. Xét tính đúng sai của các khẳng định sau:"
                 % ("chứa" if co_O else "không chứa", "kể cả" if ke else "không kể", p, q))

        # a) NB - O, A, B co thuoc mien nghiem khong (theo gia thiet)
        ga = (r"Theo giả thiết miền nghiệm %s $O$ và %s bờ $d$; hai điểm $A$, $B$ nằm trên $d$ nên %s miền nghiệm."
              % ("chứa" if co_O else "không chứa", "kể cả" if ke else "không kể", "thuộc" if ke else "không thuộc"))
        y1 = []
        for ten_d, dung_d in ((r"O\left(0; 0\right)", co_O), (r"A\left(%d; 0\right)" % p, ke), (r"B\left(0; %d\right)" % q, ke)):
            y1 += [_tfa_m(r"Điểm $%s$ thuộc miền nghiệm của bất phương trình" % ten_d, dung_d, ga),
                   _tfa_m(r"Điểm $%s$ không thuộc miền nghiệm của bất phương trình" % ten_d, not dung_d, ga)]
        y1 += [_tfa_m(r"Bất phương trình đã cho là bất phương trình ngặt", not ke, ga),
               _tfa_m(r"Bất phương trình đã cho là bất phương trình không ngặt", ke, ga)]

        # b) TH - phuong trinh duong thang d
        gb = (r"$d$ đi qua $A\left(%d; 0\right)$, $B\left(0; %d\right)$ nên $d\colon \dfrac{x}{%d} + \dfrac{y}{%d} = 1$, "
              r"tức là $d\colon %s = %d$ (hoặc phương trình tương đương)." % (p, q, p, q, vt, c))

        def cung_duong(al, be, ga_):
            return al * b == be * a and al * c == ga_ * a and be * c == ga_ * b and (al, be) != (0, 0)

        y2 = []
        for al, be, ga_ in dict.fromkeys([(a, b, c), (-a, -b, -c), (2 * a, 2 * b, 2 * c), (3 * a, 3 * b, 3 * c),
                                          (a, b, -c), (a, -b, c), (b, a, c), (-a, b, c), (a, b, c + 1)]):
            y2.append(_tfa_m(r"Đường thẳng $d$ có phương trình $%s = %d$" % (_tfa_bieu_thuc(al, be), ga_),
                             cung_duong(al, be, ga_), gb))
        y2.append(_tfa_m(r"Đường thẳng $d$ có phương trình $\dfrac{x}{%d} + \dfrac{y}{%d} = 1$" % (p, q), True, gb))
        for X, Y in ((p, 0), (0, q), (-p, 0), (0, -q), (p, q)):
            y2.append(_tfa_m(r"Đường thẳng $d$ đi qua điểm $\left(%d; %d\right)$" % (X, Y), a * X + b * Y == c, gb))

        # c) VD - bat phuong trinh da cho
        gc = (r"Tại $O$ vế trái $%s$ bằng $0$; $0 %s %d$ là mệnh đề %s mà miền nghiệm %s $O$, và %s bờ $d$, "
              r"nên bất phương trình là $%s %s %d$ (hoặc bất phương trình tương đương)."
              % (vt, ks, c, "đúng" if co_O else "sai", "chứa" if co_O else "không chứa", "kể cả" if ke else "không kể",
                 vt, ks, c))
        doi_huong = _TFA_DAO[ky]
        doi_ngat = {"<=": "<", "<": "<=", ">=": ">", ">": ">="}[ky]

        def tuong_duong(al, be, ga_, kp):
            lam = _Fr(al, a) if a else _Fr(be, b)
            if lam == 0 or be != lam * b or ga_ != lam * c:
                return False
            return kp == (ky if lam > 0 else _TFA_DAO[ky])

        y3 = []
        for al, be, ga_, kp in dict.fromkeys([
                (a, b, c, ky), (-a, -b, -c, _TFA_DAO[ky]), (2 * a, 2 * b, 2 * c, ky), (-2 * a, -2 * b, -2 * c, _TFA_DAO[ky]),
                (a, b, c, doi_huong), (a, b, c, doi_ngat), (-a, -b, -c, ky), (a, b, -c, ky), (b, a, c, ky)]):
            y3.append(_tfa_m(r"Bất phương trình đã cho tương đương với bất phương trình $%s %s %d$"
                             % (_tfa_bieu_thuc(al, be), _TFA_LATEX[kp], ga_), tuong_duong(al, be, ga_, kp), gc))

        # d) VDC - HE bat phuong trinh gom bat phuong trinh da cho va x ⋈ 0, y ⋈ 0
        y4 = _tfa_y_d(t)
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C2_TF_A_04(socau, socot=1):
    r"""Đúng/Sai - bất phương trình bậc nhất hai ẩn KÈM BỐN ĐIỂM cho trước.

    CLAUDE THEM 08/10/2026 (co Lan duyet) - theo y co Lan: cau dan "Cho bat
    phuong trinh ... va bon diem A, B, C, D"; a) nhan dang va d) dem nghiem
    nguyen y het L10_C2_TF_A_01; b) mot trong bon diem thuoc / khong thuoc mien
    nghiem; c) trong bon diem co khong / 1 / 2 / 3 / 4 diem thuoc (khong thuoc)
    mien nghiem.
    """
    cauTF = ''
    for _ in range(socau):
        t = _tfa_tao_tham_so()
        sx, sy, a, b, c, ky = t["sx"], t["sy"], t["a"], t["b"], t["c"], t["ky"]
        co_O, dem, s = t["co_O"], t["dem"], t["s"]
        vt = _tfa_bieu_thuc(a, b)
        ks = _TFA_LATEX[ky]
        bpt = r"%s %s %d" % (vt, ks, c)
        duong = r"d \colon %s = %d" % (vt, c)
        ngat = ky in ("<", ">")

        # bon diem cho truoc: n_in diem thuoc mien nghiem, con lai khong thuoc
        luoi = [(X, Y) for X in range(-6, 7) for Y in range(-6, 7)]
        trong = [p for p in luoi if _tfa_thoa(a * p[0] + b * p[1], ky, c)]
        ngoai = [p for p in luoi if not _tfa_thoa(a * p[0] + b * p[1], ky, c)]
        n_in = _rd.randint(0, 4)
        diem = _rd.sample(trong, n_in) + _rd.sample(ngoai, 4 - n_in)
        _rd.shuffle(diem)
        TEN = "ABCD"
        thuoc = [_tfa_thoa(a * p[0] + b * p[1], ky, c) for p in diem]
        tex_d = [r"%s\left(%d; %d\right)" % (TEN[i], diem[i][0], diem[i][1]) for i in range(4)]
        n_ngoai = 4 - n_in

        debai = (r"Cho bất phương trình $%s$ và bốn điểm $%s$, $%s$, $%s$, $%s$. "
                 r"Xét tính đúng sai của các khẳng định sau:" % ((bpt,) + tuple(tex_d)))

        def thay(i):
            X, Y = diem[i]
            g = a * X + b * Y
            return (r"Thay toạ độ điểm $%s$ vào vế trái: $%s\cdot %s + %s\cdot %s = %d$; "
                    r"$%d %s %d$ là mệnh đề %s nên điểm $%s$ %s miền nghiệm."
                    % (TEN[i], _tfa_so(a), _tfa_so(X), _tfa_so(b), _tfa_so(Y), g, g, ks, c,
                       "đúng" if thuoc[i] else "sai", TEN[i],
                       "thuộc" if thuoc[i] else "không thuộc"))

        # a) NB - nhan dang
        ly_do = (r"Nó có dạng $ax + by %s c$ với $a = %d$, $b = %d$ không đồng thời "
                 r"bằng $0$, và $x$, $y$ đều bậc nhất." % (ks, a, b))
        ten = r"``Bất phương trình $%s$ %s bất phương trình bậc nhất hai ẩn''"
        y1 = [(r"{\True Bất phương trình đã cho là bất phương trình bậc nhất hai ẩn}",
               r"Đúng. " + ly_do),
              (r"{Bất phương trình đã cho không phải là bất phương trình bậc nhất hai ẩn}",
               r"Sai. " + ly_do),
              (r"{\True " + ten % (bpt, "là") + r" là mệnh đề đúng}", r"Đúng. " + ly_do),
              (r"{" + ten % (bpt, "là") + r" là mệnh đề sai}", r"Sai. " + ly_do),
              (r"{" + ten % (bpt, "không phải là") + r" là mệnh đề đúng}", r"Sai. " + ly_do),
              (r"{\True " + ten % (bpt, "không phải là") + r" là mệnh đề sai}", r"Đúng. " + ly_do)]

        # b) TH - cac diem co thuoc mien nghiem khong (moi diem 4 cach noi)
        y2 = []
        for k in range(4):
            dung_b, cap, gb = thuoc[k], tex_d[k], thay(k)
            y2 += [_tfa_m(r"Điểm $%s$ thuộc miền nghiệm của bất phương trình" % cap, dung_b, gb),
                   _tfa_m(r"Điểm $%s$ không thuộc miền nghiệm của bất phương trình" % cap, not dung_b, gb),
                   _tfa_m(r"Toạ độ của điểm $%s$ là một nghiệm của bất phương trình" % TEN[k], dung_b, gb),
                   _tfa_m(r"Toạ độ của điểm $%s$ không phải là nghiệm của bất phương trình" % TEN[k], not dung_b, gb)]

        # c) VD - dem so diem thuoc / khong thuoc mien nghiem trong bon diem
        def cau_c(so, thuoc_mn):
            if so == 0:
                return (r"Trong các điểm đã cho, không có điểm nào thuộc miền nghiệm của "
                        r"bất phương trình" if thuoc_mn else
                        r"Trong các điểm đã cho, không có điểm nào không thuộc miền nghiệm của "
                        r"bất phương trình")
            if so == 4:
                return (r"Trong các điểm đã cho, cả bốn điểm đều thuộc miền nghiệm của "
                        r"bất phương trình" if thuoc_mn else
                        r"Trong các điểm đã cho, cả bốn điểm đều không thuộc miền nghiệm của "
                        r"bất phương trình")
            return ((r"Trong các điểm đã cho, có đúng $%d$ điểm thuộc miền nghiệm của "
                     r"bất phương trình" if thuoc_mn else
                     r"Trong các điểm đã cho, có đúng $%d$ điểm không thuộc miền nghiệm của "
                     r"bất phương trình") % so)

        ds_in = ", ".join(TEN[i] for i in range(4) if thuoc[i])
        ds_ngoai = ", ".join(TEN[i] for i in range(4) if not thuoc[i])
        gc = (r"\\ ".join(thay(i) for i in range(4)) +
              r"\\ Vậy có $%d$ điểm thuộc miền nghiệm%s và $%d$ điểm không thuộc miền nghiệm%s."
              % (n_in, " (%s)" % ds_in if ds_in else "",
                 n_ngoai, " (%s)" % ds_ngoai if ds_ngoai else ""))
        tc = []
        for k in range(5):
            tc.append((cau_c(k, True), k == n_in))
            tc.append((cau_c(k, False), k == n_ngoai))
        for k in (1, 2, 3):
            tc.append((r"Trong các điểm đã cho, có ít nhất $%d$ điểm thuộc miền nghiệm của "
                       r"bất phương trình" % k, n_in >= k))
        for k in (0, 1, 2, 3):
            tc.append((r"Trong các điểm đã cho, có nhiều nhất $%d$ điểm thuộc miền nghiệm của "
                       r"bất phương trình" % k, n_in <= k))
        tc += [(r"Trong các điểm đã cho, số điểm thuộc miền nghiệm nhiều hơn số điểm không thuộc "
                r"miền nghiệm của bất phương trình", n_in > n_ngoai),
               (r"Trong các điểm đã cho, số điểm thuộc miền nghiệm bằng số điểm không thuộc "
                r"miền nghiệm của bất phương trình", n_in == n_ngoai),
               (r"Trong các điểm đã cho, số điểm thuộc miền nghiệm ít hơn số điểm không thuộc "
                r"miền nghiệm của bất phương trình", n_in < n_ngoai)]
        y3 = _tfa_ds([(x, gc) for x, ok in tc if ok], [(x, gc) for x, ok in tc if not ok])

        # d) VDC - HE bat phuong trinh gom bat phuong trinh da cho va x ⋈ 0, y ⋈ 0 (xem _tfa_y_d)
        y4 = _tfa_y_d(t)

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF




# =====================================================================
# CLAUDE THEM 09/10/2026 (co Lan duyet) - BAI TOAN THUC TIEN MOI, TINH HUONG 1: PHA CHE NUOC
# (boi_canh "pha_che"). Moi lan sinh la mot bo so khac, cung cau truc:
#   x lit nuoc A, y lit nuoc B; ba dieu kien (huong lieu, nuoc, duong) dang "<=";
#   duong cua nuoc la x + y <= N; mien nghiem la NGU GIAC O(0;0), P(m;0), Q(u;N-u),
#   R(u2;N-u2), S(0;n) voi dinh nguyen; diem thuong F = px + qy dat lon nhat DUY NHAT
#   tai Q hoac R (khong phai P, S, O).
# Phan ra: NB025_MC_B (1 bat phuong trinh), VD028_MC_B / SA_B (VD: lap he, phuong an kha thi),
# VD028_MC_C / SA_C (VDC: toi uu), VD028_TL_B (2 y), TF_C (4 y).
# Co Lan: so lieu cua co (12 g huong lieu, 9 lit nuoc, 315 g duong, 60/80 diem) la mot truong hop.
# =====================================================================

def _so_vn(v):
    """Số thập phân hữu hạn viết kiểu Việt trong LaTeX (0{,}5; 1{,}95)."""
    v = Fraction(v)
    if v.denominator == 1:
        return "%d" % v.numerator
    return ("%.4f" % float(v)).rstrip("0").rstrip(".").replace(".", "{,}")


def _pc_hs(v, ten):
    return ten if Fraction(v) == 1 else _so_vn(v) + ten


def _pc_lhs(a, b):
    return "%s + %s" % (_pc_hs(a, "x"), _pc_hs(b, "y"))


def _pc_sinh():
    r"""Tham số bài toán pha chế (xem khối chú thích phía trên)."""
    while True:
        N = _rd.randint(7, 12)
        m = _rd.randint(4, N - 1)
        n = _rd.randint(4, N - 1)
        u2 = _rd.randint(1, N - 3)
        u = _rd.randint(2, N - 2)
        if not (u2 < u < m and u2 > N - n):
            continue
        A1, B1, C1 = N - u, m - u, (N - u) * m                 # đường qua P và Q
        g = _math.gcd(_math.gcd(A1, B1), C1)
        A1, B1, C1 = A1 // g, B1 // g, C1 // g
        A3, B3, C3 = u2 + n - N, u2, u2 * n                    # đường qua R và S
        g = _math.gcd(_math.gcd(A3, B3), C3)
        A3, B3, C3 = A3 // g, B3 // g, C3 // g
        if max(A1, B1, A3, B3) > 9 or A1 == B1 or A3 == B3:
            continue
        dinh = [(0, 0), (m, 0), (u, N - u), (u2, N - u2), (0, n)]
        loi = all((dinh[(i + 1) % 5][0] - dinh[i][0]) * (dinh[(i + 2) % 5][1] - dinh[(i + 1) % 5][1])
                  - (dinh[(i + 1) % 5][1] - dinh[i][1]) * (dinh[(i + 2) % 5][0] - dinh[(i + 1) % 5][0]) > 0
                  for i in range(5))
        if not loi:
            continue
        kd = _rd.choice([5, 10, 15, 20])
        kh = _rd.choice([Fraction(1, 2), Fraction(1)])
        if max(A1, B1) * kd > 100:
            continue
        p, q = 10 * _rd.randint(2, 10), 10 * _rd.randint(2, 10)
        if p == q:
            continue
        F = [p * X + q * Y for X, Y in dinh]
        lon = max(F)
        if F.count(lon) != 1 or F.index(lon) not in (2, 3):
            continue
        return dict(N=N, m=m, n=n, u=u, u2=u2, dinh=dinh, p=p, q=q, F=F, lon=lon,
                    dl=dinh[F.index(lon)], ad=A1 * kd, bd=B1 * kd, D=C1 * kd,
                    ah=A3 * kh, bh=B3 * kh, H=C3 * kh)


def _pc_de(t):
    return (r"Trong một cuộc thi pha chế, mỗi đội chơi được sử dụng tối đa $%s$ g hương liệu, $%d$ lít "
            r"nước và $%s$ g đường để pha chế hai loại nước A và B. Để pha chế $1$ lít nước A cần $%s$ g "
            r"đường, $1$ lít nước và $%s$ g hương liệu; để pha chế $1$ lít nước B cần $%s$ g đường, $1$ lít "
            r"nước và $%s$ g hương liệu. Mỗi lít nước A nhận được $%d$ điểm thưởng, mỗi lít nước B nhận được "
            r"$%d$ điểm thưởng. Gọi $x$, $y$ lần lượt là số lít nước A và số lít nước B mà một đội pha chế."
            % (_so_vn(t["H"]), t["N"], _so_vn(t["D"]), _so_vn(t["ad"]), _so_vn(t["ah"]),
               _so_vn(t["bd"]), _so_vn(t["bh"]), t["p"], t["q"]))


def _pc_rang_buoc(t):
    """[(a, b, c, tên, đơn vị)] theo thứ tự hương liệu, nước, đường."""
    return [(t["ah"], t["bh"], t["H"], "hương liệu", "g"),
            (1, 1, t["N"], "nước", "lít"),
            (t["ad"], t["bd"], t["D"], "đường", "g")]


def _pc_he_tex(dong):
    """dong: [(a, b, c, dấu LaTeX)] ba bất phương trình -> hệ cùng x >= 0, y >= 0."""
    return (r"\heva{& x \ge 0 \\ & y \ge 0 \\ & " +
            r" \\ & ".join("%s %s %s" % (_pc_lhs(a, b), d, _so_vn(c)) for a, b, c, d in dong) + "}")


def _pc_he_dung(t):
    return [(a, b, c, r"\le") for a, b, c, _, _ in _pc_rang_buoc(t)]


def _pc_thoa(t, X, Y):
    """Danh sách chỉ số ràng buộc (0 hương liệu, 1 nước, 2 đường) bị vi phạm; X, Y < 0 coi là vi phạm -1."""
    vp = [i for i, (a, b, c, _, _) in enumerate(_pc_rang_buoc(t)) if a * X + b * Y > c]
    if X < 0 or Y < 0:
        vp.append(-1)
    return vp


def _pc_giai_he(t):
    s = r"Số lít không âm nên $x \ge 0$, $y \ge 0$.\\ "
    for a, b, c, ten, dv in _pc_rang_buoc(t):
        s += r"Lượng %s dùng là $%s$ (%s), không quá $%s$ nên $%s \le %s$.\\ " % (
            ten, _pc_lhs(a, b), dv, _so_vn(c), _pc_lhs(a, b), _so_vn(c))
    return s + r"Ta được hệ $%s$." % _pc_he_tex(_pc_he_dung(t))


def _pc_giai_dinh(t):
    m, n, u, u2, N = t["m"], t["n"], t["u"], t["u2"], t["N"]
    return (r"Miền nghiệm là ngũ giác có các đỉnh $\left(0;0\right)$, $\left(%d;0\right)$, "
            r"$\left(%d;%d\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$.\\ " % (m, u, N - u, u2, N - u2, n))


def _pc_giai_F(t):
    return (r"Điểm thưởng $F\left(x; y\right) = %s$ đạt giá trị lớn nhất tại một đỉnh:\\ " % _F_tex(t["p"], t["q"]) +
            _bang_F(t["dinh"], t["p"], t["q"]) + r".\\ " +
            r"Lớn nhất là $%d$ tại $\left(%d; %d\right)$: pha chế $%d$ lít nước A và $%d$ lít nước B."
            % (t["lon"], t["dl"][0], t["dl"][1], t["dl"][0], t["dl"][1]))


def _pc_giai_toi_uu(t):
    return _pc_giai_he(t) + "\\\\\n" + _pc_giai_dinh(t) + _pc_giai_F(t)


# ---- NB025: bất phương trình của MỘT điều kiện -------------------------------------------------

def _pc_mc_bpt(socau, dang, k):
    cauTN = ""
    for _ in range(socau):
        t = _pc_sinh()
        a, b, c, ten, dv = _pc_rang_buoc(t)[k]
        dung = r"$%s \le %s$" % (_pc_lhs(a, b), _so_vn(c))
        khac = _pc_rang_buoc(t)[(k + 1) % 3][2]
        cands = [r"$%s \ge %s$" % (_pc_lhs(a, b), _so_vn(c)),
                 r"$%s \le %s$" % (_pc_lhs(b, a), _so_vn(c)),
                 r"$%s < %s$" % (_pc_lhs(a, b), _so_vn(c)),
                 r"$%s \le %s$" % (_pc_lhs(a, b), _so_vn(khac))]
        ds = _ba_nhieu2(dung, cands, buoc=lambda j: r"$%s \le %s$" % (_pc_lhs(a, b), _so_vn(c + j)))
        debai = (_pc_de(t) + r" Bất phương trình nào sau đây biểu thị điều kiện về lượng %s mà một đội được "
                 r"sử dụng?" % ten)
        giai = (r"Pha $x$ lít nước A và $y$ lít nước B cần $%s$ (%s) %s, mà mỗi đội dùng \textbf{tối đa} "
                r"$%s$ %s nên dấu là $\le$ (không loại trừ dấu bằng).\\ Vậy $%s \le %s$; lưu ý hệ số của $x$ là %s "
                r"(nước A) và của $y$ là %s (nước B)."
                % (_pc_lhs(a, b), dv, ten, _so_vn(c), dv, _pc_lhs(a, b), _so_vn(c),
                   "$%s$" % _so_vn(a), "$%s$" % _so_vn(b)))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C2_B3_NB025_MC_B_01(socau, dang=1):
    """Pha chế: bất phương trình về lượng ĐƯỜNG."""
    return _pc_mc_bpt(socau, dang, 2)


def L10_C2_B3_NB025_MC_B_02(socau, dang=1):
    """Pha chế: bất phương trình về lượng NƯỚC."""
    return _pc_mc_bpt(socau, dang, 1)


def L10_C2_B3_NB025_MC_B_03(socau, dang=1):
    """Pha chế: bất phương trình về lượng HƯƠNG LIỆU."""
    return _pc_mc_bpt(socau, dang, 0)


# ---- VD028 (VD): lập hệ, phương án khả thi, điểm thưởng của một phương án --------------------

def L10_C2_B4_VD028_MC_B_01(socau, dang=1):
    """Pha chế: chọn hệ bất phương trình mô tả đúng các điều kiện."""
    cauTN = ""
    for _ in range(socau):
        t = _pc_sinh()
        dung_dong = _pc_he_dung(t)
        d1 = [dict(zip("abcd", r)) for r in dung_dong]
        he = lambda ds: "$%s$" % _pc_he_tex(ds)
        sai1 = list(dung_dong); sai1[2] = (t["bd"], t["ad"], t["D"], r"\le")      # hoán đổi hệ số của đường
        sai2 = list(dung_dong); sai2[0] = (t["ah"], t["bh"], t["H"], r"\ge")      # đổi dấu hương liệu
        sai3 = list(dung_dong); sai3[1] = (1, 1, t["N"], r"\ge")                  # đổi dấu của nước
        sai4 = list(dung_dong); sai4[0] = (t["bh"], t["ah"], t["H"], r"\le")      # hoán đổi hệ số hương liệu
        ds = _ba_nhieu2(he(dung_dong), [he(sai1), he(sai2), he(sai3), he(sai4)])
        debai = _pc_de(t) + r" Hệ bất phương trình nào sau đây mô tả đúng các điều kiện của bài toán?"
        cauTN += MC_SA_answer_text(debai, he(dung_dong), ds, _pc_giai_he(t), 0, 0, dang)
    return cauTN


def L10_C2_B4_VD028_MC_B_02(socau, dang=1):
    """Pha chế: chọn cặp (x; y) là một phương án pha chế thoả mãn mọi điều kiện."""
    cauTN = ""
    dem = 0
    while dem < socau:
        t = _pc_sinh()
        luoi = [(X, Y) for X in range(1, t["N"] + 3) for Y in range(1, t["N"] + 3)]
        tot = [P for P in luoi if not _pc_thoa(t, *P)]
        sai = [[P for P in luoi if _pc_thoa(t, *P) == [i]] for i in range(3)]
        if not tot or not all(sai):
            continue
        dem += 1
        dung_pt = _rd.choice(tot)
        chon = [_rd.choice(s) for s in sai]
        fmt = lambda P: r"$\left(%d; %d\right)$" % P
        ten = ["hương liệu", "nước", "đường"]
        gi = r"Thay từng cặp vào ba bất phương trình của hệ:\\ "
        for X, Y in [dung_pt] + chon:
            vp = _pc_thoa(t, X, Y)
            gi += (r"Cặp $\left(%d; %d\right)$: lượng hương liệu $%s$, lượng nước $%d$, lượng đường $%s$ nên "
                   % (X, Y, _so_vn(t["ah"] * X + t["bh"] * Y), X + Y, _so_vn(t["ad"] * X + t["bd"] * Y)))
            gi += (r"thoả mãn cả ba điều kiện.\\ " if not vp else
                   r"vi phạm điều kiện về %s.\\ " % ten[vp[0]])
        gi += r"Vậy chọn cặp $\left(%d; %d\right)$." % dung_pt
        debai = (_pc_de(t) + r" Cặp số $\left(x; y\right)$ nào sau đây biểu diễn một phương án pha chế "
                 r"thoả mãn mọi điều kiện của đội?")
        cauTN += MC_SA_answer_text(debai, fmt(dung_pt), [fmt(P) for P in chon], gi, 0, 0, dang)
    return cauTN


def L10_C2_B4_VD028_MC_B_03(socau, dang=1):
    """Pha chế: số điểm thưởng của một phương án pha chế cho trước (phương án hợp lệ)."""
    cauTN = ""
    for _ in range(socau):
        t = _pc_sinh()
        luoi = [(X, Y) for X in range(1, t["N"]) for Y in range(1, t["N"]) if not _pc_thoa(t, X, Y)]
        X, Y = _rd.choice(luoi)
        p, q = t["p"], t["q"]
        v = p * X + q * Y
        ds = _ba_nhieu2("$%d$" % v, ["$%d$" % (p * Y + q * X), "$%d$" % (v + p), "$%d$" % (v - q),
                                     "$%d$" % (p + q)], buoc=lambda k: "$%d$" % (v + 10 * k))
        debai = (_pc_de(t) + r" Một đội pha chế $%d$ lít nước A và $%d$ lít nước B (thoả mãn mọi điều kiện). "
                 r"Số điểm thưởng đội đó nhận được là" % (X, Y))
        giai = (r"Điểm thưởng là $%d\cdot %d + %d\cdot %d = %d$ (mỗi lít nước A được $%d$ điểm, mỗi lít nước B "
                r"được $%d$ điểm)." % (p, X, q, Y, v, p, q))
        cauTN += MC_SA_answer_text(debai, "$%d$" % v, ds, giai, 0, 0, dang)
    return cauTN


# ---- VD028 (VDC): tìm phương án tối ưu ------------------------------------------------------------

def _pc_mc_toi_uu(socau, dang, hoi):
    cauTN = ""
    for _ in range(socau):
        t = _pc_sinh()
        dinh, F = t["dinh"], t["F"]
        if hoi == "diem":
            dap, khac = t["lon"], [g for g in F if g != t["lon"]]
            cau = r"Số điểm thưởng cao nhất mà một đội có thể nhận được là"
        elif hoi == "A":
            dap, khac = t["dl"][0], [d[0] for d in dinh]
            cau = r"Để nhận được số điểm thưởng cao nhất, đội chơi cần pha chế bao nhiêu lít nước A?"
        else:
            dap, khac = t["dl"][1], [d[1] for d in dinh]
            cau = r"Để nhận được số điểm thưởng cao nhất, đội chơi cần pha chế bao nhiêu lít nước B?"
        ds = _ba_nhieu2("$%d$" % dap, ["$%d$" % g for g in dict.fromkeys(khac) if g != dap],
                        buoc=lambda k: "$%d$" % (dap + k))
        cauTN += MC_SA_answer_text(_pc_de(t) + " " + cau, "$%d$" % dap, ds, _pc_giai_toi_uu(t), 0, 0, dang)
    return cauTN


def L10_C2_B4_VD028_MC_C_01(socau, dang=1):
    """Pha chế (VDC): số điểm thưởng cao nhất."""
    return _pc_mc_toi_uu(socau, dang, "diem")


def L10_C2_B4_VD028_MC_C_02(socau, dang=1):
    """Pha chế (VDC): số lít nước A ở phương án tối ưu."""
    return _pc_mc_toi_uu(socau, dang, "A")


def L10_C2_B4_VD028_MC_C_03(socau, dang=1):
    """Pha chế (VDC): số lít nước B ở phương án tối ưu."""
    return _pc_mc_toi_uu(socau, dang, "B")


def _pc_sa(socau, dang, hoi):
    cau = ""
    for _ in range(socau):
        t = _pc_sinh()
        dinh, N = t["dinh"], t["N"]
        rb = _pc_rang_buoc(t)
        if hoi == "dinh":
            dap, khac = 5, [4, 6, 3]
            hoi_cau = (r"Miền nghiệm của hệ bất phương trình mô tả các điều kiện của bài toán là một đa giác "
                       r"có bao nhiêu đỉnh?")
            giai = _pc_giai_he(t) + "\\\\\n" + _pc_giai_dinh(t)
        elif hoi in ("xmax", "ymax"):
            i = 0 if hoi == "xmax" else 1
            ten = "A" if i == 0 else "B"
            dap = t["m"] if i == 0 else t["n"]
            khac = [dap + 1, dap - 1, dap + 2]
            hoi_cau = (r"Nếu một đội chỉ pha chế nước %s (không pha nước %s) thì đội đó pha chế được tối đa "
                       r"bao nhiêu lít nước %s?" % (ten, "B" if i == 0 else "A", ten))
            gh = []
            for a, b, c, nm, dv in rb:
                he_so = a if i == 0 else b
                gh.append(r"%s: $%s \le %s$, tức là $%s \le %s$" % (
                    nm, _pc_hs(he_so, "x" if i == 0 else "y"), _so_vn(c), "x" if i == 0 else "y",
                    _tfa_ps((Fraction(c) / Fraction(he_so)).numerator, (Fraction(c) / Fraction(he_so)).denominator)))
            giai = (r"Chỉ pha nước %s nên số lít nước %s bằng $0$. Khi đó mỗi điều kiện cho một giới hạn:\\ " % (
                ten, "B" if i == 0 else "A") + r"\\ ".join(gh) +
                r".\\ Số lít lớn nhất thoả mãn cả ba giới hạn là giá trị nhỏ nhất, bằng $%d$." % dap)
        elif hoi == "diem":
            dap, khac = t["lon"], [g for g in t["F"] if g != t["lon"]]
            hoi_cau = r"Số điểm thưởng cao nhất mà một đội có thể nhận được là bao nhiêu?"
            giai = _pc_giai_toi_uu(t)
        elif hoi == "A":
            dap, khac = t["dl"][0], [d[0] for d in dinh]
            hoi_cau = r"Để nhận được số điểm thưởng cao nhất, đội chơi cần pha chế bao nhiêu lít nước A?"
            giai = _pc_giai_toi_uu(t)
        else:
            dap, khac = t["dl"][1], [d[1] for d in dinh]
            hoi_cau = r"Để nhận được số điểm thưởng cao nhất, đội chơi cần pha chế bao nhiêu lít nước B?"
            giai = _pc_giai_toi_uu(t)
        ds = _ba_nhieu2(str(dap), [str(v) for v in dict.fromkeys(khac) if v != dap and v > 0],
                        buoc=lambda k: str(dap + k + 2))
        cau += MC_SA_answer_text(_pc_de(t) + " " + hoi_cau, str(dap), ds, giai, 0, 0, dang)
    return cau


def L10_C2_B4_VD028_SA_B_01(socau, dang=2):
    """Pha chế (VD): số đỉnh của miền nghiệm."""
    return _pc_sa(socau, dang, "dinh")


def L10_C2_B4_VD028_SA_B_02(socau, dang=2):
    """Pha chế (VD): số lít nước A lớn nhất khi chỉ pha nước A."""
    return _pc_sa(socau, dang, "xmax")


def L10_C2_B4_VD028_SA_B_03(socau, dang=2):
    """Pha chế (VD): số lít nước B lớn nhất khi chỉ pha nước B."""
    return _pc_sa(socau, dang, "ymax")


def L10_C2_B4_VD028_SA_C_01(socau, dang=2):
    """Pha chế (VDC): số điểm thưởng cao nhất."""
    return _pc_sa(socau, dang, "diem")


def L10_C2_B4_VD028_SA_C_02(socau, dang=2):
    """Pha chế (VDC): số lít nước A ở phương án tối ưu."""
    return _pc_sa(socau, dang, "A")


def L10_C2_B4_VD028_SA_C_03(socau, dang=2):
    """Pha chế (VDC): số lít nước B ở phương án tối ưu."""
    return _pc_sa(socau, dang, "B")


def L10_C2_B4_VD028_TL_B_01(socau, dong=1):
    r"""Tự luận (2 ý) - pha chế: a) lập hệ bất phương trình (VD); b) phương án có điểm thưởng cao nhất (VDC)."""
    cauTN = ""
    for _ in range(socau):
        t = _pc_sinh()
        ds_abcd = [
            (r"Lập hệ bất phương trình mô tả các điều kiện của bài toán.",
             _pc_he_tex(_pc_he_dung(t)), _pc_giai_he(t)),
            (r"Đội chơi cần pha chế bao nhiêu lít nước mỗi loại để nhận được số điểm thưởng cao nhất? "
             r"Số điểm thưởng cao nhất là bao nhiêu?",
             r"\left(%d; %d\right)" % t["dl"], _pc_giai_dinh(t) + _pc_giai_F(t)),
        ]
        cauTN += TL_answer_text(_pc_de(t), ds_abcd, 0, 0, dong)
    return cauTN


# ---- Đúng/Sai theo chương (TF_C): bốn ý, mỗi ý ít nhất 3 đúng + 3 sai -------------------------

def _pc_giai_diem(t, X, Y):
    ten = ["hương liệu", "nước", "đường"]
    vp = _pc_thoa(t, X, Y)
    s = (r"Với $x = %d$, $y = %d$: lượng hương liệu là $%s$ g, lượng nước là $%d$ lít, lượng đường là $%s$ g "
         % (X, Y, _so_vn(t["ah"] * X + t["bh"] * Y), X + Y, _so_vn(t["ad"] * X + t["bd"] * Y)))
    s += (r"nên phương án thoả mãn cả ba điều kiện." if not vp else
          r"nên phương án vi phạm điều kiện về %s." % ten[vp[0]])
    return s


def L10_C2_TF_C_01(socau, socot=1):
    r"""Đúng/Sai theo chương - tình huống pha chế nước (boi_canh pha_che); ý a NB, b TH, c VD, d VDC."""
    cauTF = ""
    for _ in range(socau):
        t = _pc_sinh()
        m, n, u, u2, N, p, q = t["m"], t["n"], t["u"], t["u2"], t["N"], t["p"], t["q"]
        dinh, lon, dl = t["dinh"], t["lon"], t["dl"]
        rb = _pc_rang_buoc(t)
        debai = _pc_de(t) + r" Xét tính đúng sai của các khẳng định sau:"

        # a) NB - bất phương trình của từng điều kiện
        ly_a = _pc_giai_he(t)
        dung_a = [(r"Điều kiện về lượng %s được biểu thị bởi bất phương trình $%s \le %s$"
                   % (ten, _pc_lhs(a, b), _so_vn(c)), ly_a) for a, b, c, ten, dv in rb]
        dung_a.append((r"Hai điều kiện $x \ge 0$, $y \ge 0$ xuất hiện vì số lít nước pha chế không âm", ly_a))
        sai_a = [(r"Điều kiện về lượng %s được biểu thị bởi bất phương trình $%s \ge %s$"
                  % (ten, _pc_lhs(a, b), _so_vn(c)), ly_a) for a, b, c, ten, dv in rb]
        sai_a.append((r"Điều kiện về lượng nước được biểu thị bởi bất phương trình $x + y < %d$" % N, ly_a))
        sai_a.append((r"Điều kiện về lượng đường được biểu thị bởi bất phương trình $%s \le %s$"
                      % (_pc_lhs(t["bd"], t["ad"]), _so_vn(t["D"])), ly_a))
        y1 = _tfa_ds(dung_a, sai_a)

        # b) TH - phương án có thoả mãn mọi điều kiện không (tính trực tiếp)
        luoi = [(X, Y) for X in range(1, N + 3) for Y in range(1, N + 3)]
        tot = [P for P in luoi if not _pc_thoa(t, *P)]
        sai_pt = [[P for P in luoi if _pc_thoa(t, *P) == [i]] for i in range(3)]
        diem = [dinh[2], _rd.choice(tot)] + [_rd.choice(s) for s in sai_pt if s]
        dung_b, sai_b = [], []
        for X, Y in dict.fromkeys(diem):
            ok = not _pc_thoa(t, X, Y)
            gd = _pc_giai_diem(t, X, Y)
            (dung_b if ok else sai_b).append(
                (r"Phương án pha chế $%d$ lít nước A và $%d$ lít nước B thoả mãn mọi điều kiện của bài toán" % (X, Y), gd))
            (sai_b if ok else dung_b).append(
                (r"Phương án pha chế $%d$ lít nước A và $%d$ lít nước B không thoả mãn mọi điều kiện của bài toán"
                 % (X, Y), gd))
        y2 = _tfa_ds(dung_b, sai_b)

        # c) VD - miền nghiệm
        ly_c = (r"Giải các cặp đường biên ta được năm đỉnh $\left(0;0\right)$, $\left(%d;0\right)$, "
                r"$\left(%d;%d\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$; miền nghiệm là ngũ giác lồi, bị chặn."
                % (m, u, N - u, u2, N - u2, n))
        y3 = _tfa_ds(
            [(r"Miền nghiệm của hệ là một miền đa giác lồi có $5$ đỉnh", ly_c),
             (r"Miền nghiệm của hệ là một miền bị chặn", ly_c),
             (r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % (u, N - u), ly_c),
             (r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % (u2, N - u2), ly_c),
             (r"Điểm $\left(%d; 0\right)$ là một đỉnh của miền nghiệm" % m, ly_c)],
            [(r"Miền nghiệm của hệ là một miền đa giác lồi có $4$ đỉnh", ly_c),
             (r"Miền nghiệm của hệ là một miền đa giác lồi có $6$ đỉnh", ly_c),
             (r"Miền nghiệm của hệ là một miền không bị chặn", ly_c),
             (r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % (m, n), ly_c),
             (r"Điểm $\left(%d; 0\right)$ là một đỉnh của miền nghiệm" % N, ly_c)])

        # d) VDC - điểm thưởng lớn nhất
        ly_d = _pc_giai_toi_uu(t)
        ds_F = sorted(set(t["F"]))
        hai = ds_F[-2]
        sai_gt = [g for g in (lon + p + q, hai, p * m + q * n) if g != lon]
        y4 = _tfa_ds(
            [(r"Số điểm thưởng cao nhất mà một đội có thể nhận được bằng $%d$" % lon, ly_d),
             (r"Số điểm thưởng cao nhất đạt được khi pha chế $%d$ lít nước A và $%d$ lít nước B" % dl, ly_d),
             (r"Khi nhận được số điểm thưởng cao nhất, tổng lượng nước đã dùng là $%d$ lít" % N, ly_d),
             (r"Pha chế $%d$ lít nước A và không pha nước B thì nhận được $%d$ điểm thưởng" % (m, p * m), ly_d),
             (r"Pha chế $%d$ lít nước B và không pha nước A thì nhận được $%d$ điểm thưởng" % (n, q * n), ly_d)],
            [(r"Số điểm thưởng cao nhất mà một đội có thể nhận được bằng $%d$" % g, ly_d) for g in sai_gt[:3]]
            + [(r"Pha chế $%d$ lít nước A và không pha nước B thì nhận được số điểm thưởng cao nhất" % m, ly_d),
               (r"Pha chế $%d$ lít nước B và không pha nước A thì nhận được số điểm thưởng cao nhất" % n, ly_d)])

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


# =====================================================================
# CLAUDE THEM 09/10/2026 (co Lan duyet) - TINH HUONG THUC TE 2, 3, 4 (dung chung KHUNG "kb" cho moi tinh huong):
#   2 thuc_an_gia_suc (min, 3 dieu kien >=, mien khong bi chan), 3 phan_xuong_hai_may (max, 2 dieu kien <=),
#   4 do_uong_an_kieng (min, 3 dieu kien >=, calo: x + y >= N).
# Moi tinh huong la mot ham sinh `t` (dict) ma cac ham hoi (NB025_MC, VD028_MC/SA/TL, TF) dung chung:
#   t["de"] cau dan; t["rb"] cac dieu kien (a, b, c, dau); t["dinh"] cac dinh; t["cx"], t["cy"] he so cua F
#   (nghin dong); t["kind"] max / min; cac cau chu mo ta (q_gt, q_x, q_y, ket, pa_xy ...).
# Moi so tinh bang so nguyen / phan so; dung / sai cua dap an kiem lai doc lap trong
# tests/test_l10_c2_tinh_huong_kb.py.
# =====================================================================

def _kb_dinh_that(rb):
    """Đỉnh THẬT của miền {x >= 0, y >= 0, rb} (giao từng cặp đường biên), theo thứ tự quanh miền."""
    duong = [(Fraction(1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(1), Fraction(0))]
    duong += [(Fraction(r["a"]), Fraction(r["b"]), Fraction(r["c"])) for r in rb]

    def thoa(X, Y):
        if X < 0 or Y < 0:
            return False
        return all((r["a"] * X + r["b"] * Y <= r["c"]) if r["dau"] == r"\le" else (r["a"] * X + r["b"] * Y >= r["c"])
                   for r in rb)
    kq = set()
    for i in range(len(duong)):
        for j in range(i + 1, len(duong)):
            (a1, b1, c1), (a2, b2, c2) = duong[i], duong[j]
            D = a1 * b2 - a2 * b1
            if D == 0:
                continue
            X, Y = (c1 * b2 - c2 * b1) / D, (a1 * c2 - a2 * c1) / D
            if thoa(X, Y):
                kq.add((X, Y))
    return sorted(kq)


def _kb_thoa(t, X, Y):
    """Chỉ số các điều kiện bị vi phạm (-1: số âm)."""
    vp = [i for i, r in enumerate(t["rb"])
          if not ((r["a"] * X + r["b"] * Y <= r["c"]) if r["dau"] == r"\le" else (r["a"] * X + r["b"] * Y >= r["c"]))]
    if X < 0 or Y < 0:
        vp.append(-1)
    return vp


def _hoa(s):
    """Viết hoa chữ cái đầu của cả câu (không phụ thuộc ngôn ngữ)."""
    return s[:1].upper() + s[1:]


def _kb_hoan_tat(t):
    """Điền các trường suy ra: giá trị F tại đỉnh, đỉnh tối ưu, miền bị chặn hay không."""
    t["F"] = [t["cx"] * X + t["cy"] * Y for X, Y in t["dinh"]]
    cuc = max(t["F"]) if t["kind"] == "max" else min(t["F"])
    t["best"] = cuc
    t["opt"] = t["dinh"][t["F"].index(cuc)]
    t["cuc"] = "lớn nhất" if t["kind"] == "max" else "nhỏ nhất"
    t["F_cuc"] = "tiền lãi lớn nhất" if t["kind"] == "max" else "chi phí nhỏ nhất"
    return t


def _kb_hien(t, v):
    """Giá trị F (nghìn đồng, số nguyên) -> chuỗi hiển thị theo đơn vị của MC / TF."""
    return "%s %s" % (_so_vn(Fraction(v, t["chia"])), t["dv_hien"])


def _kb_dk_chu(t, i):
    return t["rb"][i]["dk"]


def _kb_sinh_max_tu_giac():
    """Tình huống 3: tứ giác O, P(m;0), Q(u;v), R(0;n); hai điều kiện <=."""
    while True:
        m, n = _rd.randint(2, 6), _rd.randint(3, 8)
        u, v = _rd.randint(1, m - 1), _rd.randint(1, n - 1)
        if u * n + v * m <= m * n:
            continue
        L1, L2 = [v, m - u, v * m], [n - v, u, u * n]
        for L in (L1, L2):
            g = _math.gcd(_math.gcd(L[0], L[1]), L[2])
            L[0], L[1], L[2] = L[0] // g, L[1] // g, L[2] // g
        if max(L1[0], L1[1], L2[0], L2[1]) > 5 or max(L1[2], L2[2]) > 12:
            continue
        return m, n, u, v, L1, L2


def _kb3_sinh():
    while True:
        m, n, u, v, L1, L2 = _kb_sinh_max_tu_giac()
        p, q = 100 * _rd.randint(10, 30), 100 * _rd.randint(8, 30)
        dinh = [(0, 0), (m, 0), (u, v), (0, n)]
        F = [p * X + q * Y for X, Y in dinh]
        if p == q or F.count(max(F)) != 1 or F.index(max(F)) != 2:
            continue
        rb = [dict(a=L1[0], b=L1[1], c=L1[2], dau=r"\le", dk="thời gian làm việc của máy M1 trong một ngày"),
              dict(a=L2[0], b=L2[1], c=L2[2], dau=r"\le", dk="thời gian làm việc của máy M2 trong một ngày")]
        for r_ in rb:
            r_["dv"] = "giờ"
        de = (r"Một phân xưởng có hai máy chuyên dụng M1 và M2 để sản xuất hai loại sản phẩm A và B theo đơn đặt "
              r"hàng. Nếu sản xuất được một tấn sản phẩm loại A thì phân xưởng nhận được số tiền lãi là $%s$ triệu "
              r"đồng; nếu sản xuất được một tấn sản phẩm loại B thì nhận được số tiền lãi là $%s$ triệu đồng. "
              r"Muốn sản xuất một tấn sản phẩm loại A, người ta phải dùng máy M1 trong $%d$ giờ và máy M2 trong "
              r"$%d$ giờ. Muốn sản xuất một tấn sản phẩm loại B, người ta phải dùng máy M1 trong $%d$ giờ và máy M2 "
              r"trong $%d$ giờ. Một máy không thể dùng để sản xuất đồng thời hai loại sản phẩm này. Máy M1 làm việc "
              r"không quá $%d$ giờ một ngày và máy M2 làm việc không quá $%d$ giờ một ngày. Gọi $x$, $y$ lần lượt "
              r"là số tấn sản phẩm loại A và loại B mà phân xưởng sản xuất trong một ngày."
              % (_so_vn(Fraction(p, 1000)), _so_vn(Fraction(q, 1000)), L1[0], L2[0], L1[1], L2[1], L1[2], L2[2]))
        t = dict(
            de=de, kind="max", rb=rb, dinh=dinh, cx=p, cy=q, F_ten="tiền lãi", dv_hien="triệu đồng", chia=1000,
            bi_chan=True, so_x="số tấn sản phẩm loại A", so_y="số tấn sản phẩm loại B",
            pa_xy="sản xuất $%d$ tấn sản phẩm loại A và $%d$ tấn sản phẩm loại B",
            pa_x="sản xuất $%d$ tấn sản phẩm loại A", pa_y="sản xuất $%d$ tấn sản phẩm loại B",
            ket="cần sản xuất $%d$ tấn sản phẩm loại A và $%d$ tấn sản phẩm loại B",
            q_gt=r"Số tiền lãi lớn nhất mà phân xưởng thu được trong một ngày là bao nhiêu?",
            q_x=r"Để tiền lãi lớn nhất thì mỗi ngày phân xưởng cần sản xuất bao nhiêu tấn sản phẩm loại A?",
            q_y=r"Để tiền lãi lớn nhất thì mỗi ngày phân xưởng cần sản xuất bao nhiêu tấn sản phẩm loại B?",
            q_xcuc=r"Nếu phân xưởng chỉ sản xuất sản phẩm loại A (không sản xuất loại B) thì mỗi ngày sản xuất được tối "
                   r"đa bao nhiêu tấn sản phẩm loại A?",
            q_ycuc=r"Nếu phân xưởng chỉ sản xuất sản phẩm loại B (không sản xuất loại A) thì mỗi ngày sản xuất được tối "
                   r"đa bao nhiêu tấn sản phẩm loại B?",
            q_tl_b=r"Gọi $F$ (nghìn đồng) là số tiền lãi phân xưởng thu được trong một ngày. Biểu diễn $F$ theo $x$, $y$, "
                   r"rồi tìm số tiền lãi lớn nhất và số tấn mỗi loại sản phẩm cần sản xuất.")
        return _kb_hoan_tat(t)


def _kb_sinh_min_chuoi(N=None):
    """Chuỗi đỉnh S(0;n), Q1, Q2, P(m;0) lồi (đường biên ngày càng thoải); N != None: Q1, Q2 nằm trên x + y = N.
    Trả về (n, Q1, Q2, m, [L1, L2, L3]) với L = [a, b, c] đã tối giản, hệ số <= 9."""
    while True:
        if N is None:
            n, m = _rd.randint(6, 14), _rd.randint(8, 20)
            u1, u2 = _rd.randint(1, 4), _rd.randint(2, 9)
            v1, v2 = _rd.randint(2, n - 1), _rd.randint(1, 8)
        else:
            n, m = N + _rd.randint(1, 4), N + _rd.randint(2, 7)
            u1, u2 = _rd.randint(1, N - 2), _rd.randint(2, N - 1)
            v1, v2 = N - u1, N - u2
        if not (0 < u1 < u2 < m and 0 < v2 < v1 < n):
            continue
        s1, s2, s3 = Fraction(v1 - n, u1), Fraction(v2 - v1, u2 - u1), Fraction(-v2, m - u2)
        if not (s1 < s2 < s3 < 0):
            continue
        L1 = [n - v1, u1, u1 * n]
        L2 = [v1 - v2, u2 - u1, (v1 - v2) * u1 + (u2 - u1) * v1]
        L3 = [v2, m - u2, v2 * m]
        for L in (L1, L2, L3):
            g = _math.gcd(_math.gcd(L[0], L[1]), L[2])
            L[0], L[1], L[2] = L[0] // g, L[1] // g, L[2] // g
        if max(L1[0], L1[1], L2[0], L2[1], L3[0], L3[1]) > 9:
            continue
        return n, (u1, v1), (u2, v2), m, [L1, L2, L3]


def _kb_chon_min(t_dinh, cx, cy):
    F = [cx * X + cy * Y for X, Y in t_dinh]
    return F.count(min(F)) == 1 and F.index(min(F)) in (1, 2)


def _kb2_sinh():
    while True:
        n, Q1, Q2, m, Ls = _kb_sinh_min_chuoi()
        cx, cy = 50 * _rd.randint(2, 8), 50 * _rd.randint(2, 8)
        dinh = [(0, n), Q1, Q2, (m, 0)]
        if cx == cy or not _kb_chon_min(dinh, cx, cy):
            continue
        hoan_vi = _rd.sample(range(3), 3)
        rb = []
        for ch, idx in zip("ABC", hoan_vi):
            a, b, c = Ls[idx]
            rb.append(dict(a=a, b=b, c=c, dau=r"\ge", dv="đơn vị",
                           dk="lượng chất dinh dưỡng %s trong hỗn hợp" % ch, ten=ch))
        if _kb_dinh_that(rb) != sorted((Fraction(X), Fraction(Y)) for X, Y in dinh):
            continue
        ax = [r["a"] for r in rb]
        ay = [r["b"] for r in rb]
        cc = [r["c"] for r in rb]
        de = (r"Một hợp tác xã chăn nuôi dự định trộn hai loại thức ăn gia súc X và Y để tạo thành thức ăn hỗn hợp "
              r"cho gia súc. Giá một bao loại X là $%d$ nghìn đồng, giá một bao loại Y là $%d$ nghìn đồng. Mỗi bao "
              r"loại X chứa $%d$ đơn vị chất dinh dưỡng A, $%d$ đơn vị chất dinh dưỡng B và $%d$ đơn vị chất dinh "
              r"dưỡng C. Mỗi bao loại Y chứa $%d$ đơn vị chất dinh dưỡng A, $%d$ đơn vị chất dinh dưỡng B và $%d$ "
              r"đơn vị chất dinh dưỡng C. Hỗn hợp thu được phải chứa tối thiểu $%d$ đơn vị chất dinh dưỡng A, $%d$ "
              r"đơn vị chất dinh dưỡng B và $%d$ đơn vị chất dinh dưỡng C. Gọi $x$, $y$ lần lượt là số bao thức ăn "
              r"loại X và loại Y cần mua."
              % (cx, cy, ax[0], ax[1], ax[2], ay[0], ay[1], ay[2], cc[0], cc[1], cc[2]))
        t = dict(
            de=de, kind="min", rb=rb, dinh=dinh, cx=cx, cy=cy, F_ten="chi phí", dv_hien="triệu đồng", chia=1000,
            bi_chan=False, so_x="số bao thức ăn loại X", so_y="số bao thức ăn loại Y",
            pa_xy="mua $%d$ bao thức ăn loại X và $%d$ bao thức ăn loại Y",
            pa_x="mua $%d$ bao thức ăn loại X", pa_y="mua $%d$ bao thức ăn loại Y",
            ket="cần mua $%d$ bao thức ăn loại X và $%d$ bao thức ăn loại Y",
            q_gt=r"Chi phí nhỏ nhất để mua hai loại thức ăn gia súc X và Y sao cho hỗn hợp thu được thoả mãn các yêu "
                 r"cầu trên là bao nhiêu?",
            q_x=r"Để chi phí nhỏ nhất thì cần mua bao nhiêu bao thức ăn loại X?",
            q_y=r"Để chi phí nhỏ nhất thì cần mua bao nhiêu bao thức ăn loại Y?",
            q_xcuc=r"Nếu chỉ mua thức ăn loại X (không mua loại Y) thì cần mua tối thiểu bao nhiêu bao loại X để hỗn "
                   r"hợp thoả mãn cả ba yêu cầu?",
            q_ycuc=r"Nếu chỉ mua thức ăn loại Y (không mua loại X) thì cần mua tối thiểu bao nhiêu bao loại Y để hỗn "
                   r"hợp thoả mãn cả ba yêu cầu?",
            q_tl_b=r"Gọi $F$ (nghìn đồng) là chi phí mua $x$ bao loại X và $y$ bao loại Y. Biểu diễn $F$ theo $x$, $y$, "
                   r"rồi tìm chi phí nhỏ nhất và số bao mỗi loại cần mua.")
        return _kb_hoan_tat(t)


def _kb4_sinh():
    while True:
        N = _rd.randint(4, 7)
        n, Q1, Q2, m, Ls = _kb_sinh_min_chuoi(N)
        if Ls[1][:2] != [1, 1]:
            continue
        cx, cy = _rd.randint(8, 20), _rd.randint(8, 20)
        dinh = [(0, n), Q1, Q2, (m, 0)]
        if cx == cy or not _kb_chon_min(dinh, cx, cy):
            continue
        kc = _rd.choice([20, 30, 60])
        va, vc = (Ls[0], Ls[2]) if _rd.random() < 0.5 else (Ls[2], Ls[0])
        ka, kcv = _rd.choice([3, 6]), _rd.choice([5, 10])
        rb = [dict(a=kc, b=kc, c=kc * N, dau=r"\ge", dv="calo", dk="lượng calo mỗi ngày"),
              dict(a=ka * va[0], b=ka * va[1], c=ka * va[2], dau=r"\ge", dv="đơn vị",
                   dk="lượng vitamin A mỗi ngày"),
              dict(a=kcv * vc[0], b=kcv * vc[1], c=kcv * vc[2], dau=r"\ge", dv="đơn vị",
                   dk="lượng vitamin C mỗi ngày")]
        if _kb_dinh_that(rb) != sorted((Fraction(X), Fraction(Y)) for X, Y in dinh):
            continue
        de = (r"Một người ăn kiêng cần được cung cấp ít nhất $%d$ calo, $%d$ đơn vị vitamin A và $%d$ đơn vị "
              r"vitamin C mỗi ngày từ hai loại đồ uống I và II. Mỗi cốc đồ uống I cung cấp $%d$ calo, $%d$ đơn vị "
              r"vitamin A và $%d$ đơn vị vitamin C. Mỗi cốc đồ uống II cung cấp $%d$ calo, $%d$ đơn vị vitamin A và "
              r"$%d$ đơn vị vitamin C. Biết rằng một cốc đồ uống I có giá $%d$ nghìn đồng và một cốc đồ uống II có "
              r"giá $%d$ nghìn đồng. Gọi $x$, $y$ lần lượt là số cốc đồ uống I và II mà người đó uống mỗi ngày."
              % (rb[0]["c"], rb[1]["c"], rb[2]["c"], rb[0]["a"], rb[1]["a"], rb[2]["a"],
                 rb[0]["b"], rb[1]["b"], rb[2]["b"], cx, cy))
        t = dict(
            de=de, kind="min", rb=rb, dinh=dinh, cx=cx, cy=cy, F_ten="chi phí", dv_hien="nghìn đồng", chia=1,
            bi_chan=False, so_x="số cốc đồ uống I", so_y="số cốc đồ uống II",
            pa_xy="uống $%d$ cốc đồ uống I và $%d$ cốc đồ uống II",
            pa_x="uống $%d$ cốc đồ uống I", pa_y="uống $%d$ cốc đồ uống II",
            ket="cần uống $%d$ cốc đồ uống I và $%d$ cốc đồ uống II",
            q_gt=r"Chi phí nhỏ nhất mỗi ngày để người đó đáp ứng đủ các yêu cầu trên là bao nhiêu?",
            q_x=r"Để chi phí nhỏ nhất mà vẫn đáp ứng đủ yêu cầu hằng ngày thì người đó cần uống bao nhiêu cốc đồ uống I?",
            q_y=r"Để chi phí nhỏ nhất mà vẫn đáp ứng đủ yêu cầu hằng ngày thì người đó cần uống bao nhiêu cốc đồ uống II?",
            q_xcuc=r"Nếu người đó chỉ uống đồ uống I (không uống đồ uống II) thì mỗi ngày cần uống tối thiểu bao nhiêu "
                   r"cốc đồ uống I để đủ cả ba yêu cầu?",
            q_ycuc=r"Nếu người đó chỉ uống đồ uống II (không uống đồ uống I) thì mỗi ngày cần uống tối thiểu bao nhiêu "
                   r"cốc đồ uống II để đủ cả ba yêu cầu?",
            q_tl_b=r"Gọi $F$ (nghìn đồng) là số tiền phải trả cho $x$ cốc đồ uống I và $y$ cốc đồ uống II. Biểu diễn $F$ "
                   r"theo $x$, $y$, rồi tìm chi phí nhỏ nhất và số cốc mỗi loại cần uống.")
        return _kb_hoan_tat(t)


# ---- Lời giải dùng chung ------------------------------------------------------------------------

_KB_TU_DAU = {r"\le": "không quá", r"\ge": "ít nhất"}


def _kb_lhs(r):
    return _pc_lhs(r["a"], r["b"])


def _kb_he_tex(dong):
    return (r"\heva{& x \ge 0 \\ & y \ge 0 \\ & " +
            r" \\ & ".join("%s %s %s" % (_pc_lhs(a, b), d, _so_vn(c)) for a, b, c, d in dong) + "}")


def _kb_he_dung(t):
    return [(r["a"], r["b"], r["c"], r["dau"]) for r in t["rb"]]


def _kb_giai_he(t):
    s = r"Số lượng không âm nên $x \ge 0$, $y \ge 0$.\\ "
    for r in t["rb"]:
        s += r"%s là $%s$ (%s), %s $%s$ nên $%s %s %s$.\\ " % (
            r["dk"][0].upper() + r["dk"][1:], _kb_lhs(r), r["dv"], _KB_TU_DAU[r["dau"]], _so_vn(r["c"]),
            _kb_lhs(r), r["dau"], _so_vn(r["c"]))
    return s + r"Ta được hệ $%s$." % _kb_he_tex(_kb_he_dung(t))


def _kb_dinh_tex(t):
    return ", ".join(r"$\left(%d;%d\right)$" % v for v in t["dinh"])


def _kb_giai_dinh(t):
    if t["bi_chan"]:
        return r"Miền nghiệm là đa giác có %d đỉnh: %s.\\ " % (len(t["dinh"]), _kb_dinh_tex(t))
    return (r"Miền nghiệm là miền không bị chặn, có %d đỉnh: %s.\\ " % (len(t["dinh"]), _kb_dinh_tex(t)))


def _kb_F_tex(t):
    return _F_tex(t["cx"], t["cy"])


def _kb_giai_F(t):
    bang = r"\\ ".join(r"$F\left(%d; %d\right) = %d$" % (X, Y, g) for (X, Y), g in zip(t["dinh"], t["F"]))
    return (r"Gọi $F\left(x; y\right) = %s$ (nghìn đồng) là %s. $F$ đạt giá trị %s tại một đỉnh của miền nghiệm:\\ "
            % (_kb_F_tex(t), t["F_ten"], t["cuc"]) + bang + r".\\ " +
            r"Giá trị %s là $%d$ nghìn đồng, tại $\left(%d; %d\right)$, tức là %s."
            % (t["cuc"], t["best"], t["opt"][0], t["opt"][1], t["ket"] % t["opt"]))


def _kb_giai_toi_uu(t):
    return _kb_giai_he(t) + "\\\\\n" + _kb_giai_dinh(t) + _kb_giai_F(t)


def _kb_giai_diem(t, X, Y):
    s = r"Với $x = %d$, $y = %d$: " % (X, Y)
    s += ", ".join(r"%s bằng $%s$ %s" % (r["dk"], _so_vn(r["a"] * X + r["b"] * Y), r["dv"]) for r in t["rb"])
    vp = _kb_thoa(t, X, Y)
    return s + (r", nên phương án thoả mãn cả ba điều kiện." if not vp and len(t["rb"]) == 3 else
                r", nên phương án thoả mãn mọi điều kiện." if not vp else
                r", nên phương án vi phạm điều kiện về %s." % t["rb"][vp[0]]["dk"])


def _kb_buoc(t):
    return 50 if t["chia"] == 1000 else 2


def _kb_so_hien(t, v):
    return "$%s$ %s" % (_so_vn(Fraction(v, t["chia"])), t["dv_hien"])


# ---- NB025: bất phương trình của MỘT điều kiện -----------------------------------------------

def _kb_mc_bpt(KB, socau, dang, k):
    cauTN = ""
    for _ in range(socau):
        t = KB()
        r = t["rb"][k]
        lhs = _kb_lhs(r)
        dung = r"$%s %s %s$" % (lhs, r["dau"], _so_vn(r["c"]))
        dao = r"\ge" if r["dau"] == r"\le" else r"\le"
        ngat = "<" if r["dau"] == r"\le" else ">"
        khac = t["rb"][(k + 1) % len(t["rb"])]["c"]
        cands = [r"$%s %s %s$" % (lhs, dao, _so_vn(r["c"])),
                 r"$%s %s %s$" % (_pc_lhs(r["b"], r["a"]), r["dau"], _so_vn(r["c"])),
                 r"$%s %s %s$" % (lhs, ngat, _so_vn(r["c"])),
                 r"$%s %s %s$" % (lhs, r["dau"], _so_vn(khac))]
        ds = _ba_nhieu2(dung, cands, buoc=lambda j: r"$%s %s %s$" % (lhs, r["dau"], _so_vn(r["c"] + j)))
        debai = t["de"] + r" Bất phương trình nào sau đây biểu thị điều kiện về %s?" % r["dk"]
        giai = (r"%s là $%s$ (%s) và phải %s $%s$ (%s) nên dấu là $%s$ (có xét dấu bằng).\\ Vậy $%s %s %s$; lưu ý "
                r"hệ số của $x$ là $%s$ và của $y$ là $%s$."
                % (r["dk"][0].upper() + r["dk"][1:], lhs, r["dv"], _KB_TU_DAU[r["dau"]], _so_vn(r["c"]), r["dv"],
                   r["dau"], lhs, r["dau"], _so_vn(r["c"]), _so_vn(r["a"]), _so_vn(r["b"])))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


# ---- VD028 (VD): hệ, phương án khả thi, giá trị F của một phương án ---------------------------

def _kb_mc_vd(KB, socau, dang, kieu):
    cauTN = ""
    dem = 0
    while dem < socau:
        t = KB()
        if kieu == "he":
            dung_dong = _kb_he_dung(t)
            he = lambda ds: "$%s$" % _kb_he_tex(ds)
            cands = []
            for i, (a, b, c, d) in enumerate(dung_dong):
                s = list(dung_dong); s[i] = (a, b, c, r"\ge" if d == r"\le" else r"\le"); cands.append(he(s))
            for i, (a, b, c, d) in enumerate(dung_dong):
                s = list(dung_dong); s[i] = (b, a, c, d); cands.append(he(s))
            s = list(dung_dong); s[0] = (dung_dong[0][0], dung_dong[0][1], dung_dong[0][2], "<" if dung_dong[0][3] == r"\le" else ">")
            cands.append(he(s))
            ds = _ba_nhieu2(he(dung_dong), cands)
            debai = t["de"] + r" Hệ bất phương trình nào sau đây mô tả đúng các điều kiện của bài toán?"
            cauTN += MC_SA_answer_text(debai, he(dung_dong), ds, _kb_giai_he(t), 0, 0, dang)
            dem += 1
            continue
        K = max(max(v) for v in t["dinh"]) + 3
        luoi = [(X, Y) for X in range(1, K) for Y in range(1, K)]
        tot = [P for P in luoi if not _kb_thoa(t, *P)]
        if kieu == "pa":
            sai = [[P for P in luoi if _kb_thoa(t, *P) == [i]] for i in range(len(t["rb"]))]
            ngoai = [P for P in luoi if _kb_thoa(t, *P)]
            if not tot or not ngoai:
                continue
            chon = [_rd.choice(s) for s in sai if s]
            while len(chon) < 3:
                P = _rd.choice(ngoai)
                if P not in chon:
                    chon.append(P)
            chon = chon[:3]
            dung_pt = _rd.choice(tot)
            fmt = lambda P: r"$\left(%d; %d\right)$" % P
            gi = r"Thay từng cặp vào các bất phương trình của hệ:\\ " + r"\\ ".join(
                r"Cặp $\left(%d; %d\right)$: %s" % (X, Y, _kb_giai_diem(t, X, Y)) for X, Y in [dung_pt] + chon)
            gi += r"\\ Vậy chọn cặp $\left(%d; %d\right)$." % dung_pt
            debai = (t["de"] + r" Cặp số $\left(x; y\right)$ nào sau đây biểu diễn một phương án thoả mãn mọi điều "
                     r"kiện của bài toán?")
            cauTN += MC_SA_answer_text(debai, fmt(dung_pt), [fmt(P) for P in chon], gi, 0, 0, dang)
            dem += 1
        else:                                                                   # "gt": F tại một phương án khả thi
            if not tot:
                continue
            X, Y = _rd.choice([P for P in tot if P[0] <= K - 3 and P[1] <= K - 3] or tot)
            v = t["cx"] * X + t["cy"] * Y
            st = _kb_buoc(t)
            ds = _ba_nhieu2(_kb_so_hien(t, v), [_kb_so_hien(t, t["cx"] * Y + t["cy"] * X), _kb_so_hien(t, v + st),
                                                 _kb_so_hien(t, v - st), _kb_so_hien(t, t["cx"] + t["cy"])],
                            buoc=lambda k: _kb_so_hien(t, v + 2 * st * k))
            debai = (t["de"] + r" Một phương án %s (thoả mãn mọi điều kiện của bài toán). "
                     % (t["pa_xy"] % (X, Y)) + _hoa(r"%s của phương án đó là" % t["F_ten"]))
            giai = _hoa(r"%s là $%d\cdot %d + %d\cdot %d = %d$ (nghìn đồng), tức là %s."
                        % (t["F_ten"], t["cx"], X, t["cy"], Y, v, _kb_so_hien(t, v)))
            cauTN += MC_SA_answer_text(debai, _kb_so_hien(t, v), ds, giai, 0, 0, dang)
            dem += 1
    return cauTN


# ---- VD028 (VDC): giá trị tối ưu, số lượng ở phương án tối ưu (MC và SA) ----------------------

def _kb_toi_uu(KB, socau, dang, hoi, sa):
    cau = ""
    for _ in range(socau):
        t = KB()
        dinh, F = t["dinh"], t["F"]
        st = _kb_buoc(t)
        if hoi == "gt":
            dap = t["best"]
            khac = [g for g in F if g != dap and g > 0] + [dap + st, dap - st, dap + 2 * st]
            hien = (lambda v: str(v)) if sa else (lambda v: _kb_so_hien(t, v))
            cau_hoi = t["q_gt"] + (r" (đơn vị: nghìn đồng)" if sa else "")
        else:
            i = 0 if hoi == "x" else 1
            dap = t["opt"][i]
            khac = [d[i] for d in dinh] + [dap + 1, dap + 2, dap + 3]
            hien = (lambda v: str(v)) if sa else (lambda v: "$%d$" % v)
            cau_hoi = t["q_x"] if hoi == "x" else t["q_y"]
        ds = _ba_nhieu2(hien(dap), [hien(v) for v in dict.fromkeys(khac) if v != dap and v > 0],
                        buoc=lambda k: hien(dap + k + 3))
        cau += MC_SA_answer_text(t["de"] + " " + cau_hoi, hien(dap), ds, _kb_giai_toi_uu(t), 0, 0, dang)
    return cau


# ---- VD028 (VD) trả lời ngắn: số đỉnh, giới hạn khi chỉ dùng một loại ----------------------------

def _kb_sa_vd(KB, socau, dang, hoi):
    cau = ""
    for _ in range(socau):
        t = KB()
        if hoi == "dinh":
            dap = len(t["dinh"])
            khac = [dap - 1, dap + 1, dap + 2]
            cau_hoi = (r"Miền nghiệm của hệ bất phương trình mô tả các điều kiện của bài toán có bao nhiêu đỉnh?")
            giai = _kb_giai_he(t) + "\\\\\n" + _kb_giai_dinh(t)
        else:
            i = 0 if hoi == "xcuc" else 1
            dap = max(v[i] for v in t["dinh"])
            khac = [dap + 1, dap - 1, dap + 2]
            cau_hoi = t["q_xcuc"] if i == 0 else t["q_ycuc"]
            bien = "x" if i == 0 else "y"
            kho = t["so_y"] if i == 0 else t["so_x"]
            gh = []
            for r in t["rb"]:
                he_so = r["a"] if i == 0 else r["b"]
                fr = Fraction(r["c"]) / Fraction(he_so)
                gh.append(r"$%s %s %s$, tức là $%s %s %s$"
                          % (_pc_hs(he_so, bien), r["dau"], _so_vn(r["c"]), bien, r["dau"],
                             _tfa_ps(fr.numerator, fr.denominator)))
            giai = (r"Khi %s bằng $0$ thì mỗi điều kiện cho một giới hạn của $%s$:\\ " % (kho, bien) +
                    r"\\ ".join(gh) + r".\\ " +
                    (r"Giá trị thoả mãn cả ba giới hạn phải bé hơn hoặc bằng giới hạn nhỏ nhất, nên lớn nhất là $%d$."
                     if t["kind"] == "max" else
                     r"Giá trị thoả mãn cả ba giới hạn phải lớn hơn hoặc bằng giới hạn lớn nhất, nên nhỏ nhất là $%d$.")
                    % dap)
        ds = _ba_nhieu2(str(dap), [str(v) for v in khac if v != dap and v > 0], buoc=lambda k: str(dap + k + 2))
        cau += MC_SA_answer_text(t["de"] + " " + cau_hoi, str(dap), ds, giai, 0, 0, dang)
    return cau


# ---- Tự luận 2 ý -------------------------------------------------------------------------------

def _kb_tl(KB, socau, dong):
    cauTN = ""
    for _ in range(socau):
        t = KB()
        ds_abcd = [
            (r"Lập hệ bất phương trình mô tả các điều kiện của bài toán.",
             _kb_he_tex(_kb_he_dung(t)), _kb_giai_he(t)),
            (t["q_tl_b"], r"\left(%d; %d\right)" % t["opt"], _kb_giai_dinh(t) + _kb_giai_F(t)),
        ]
        cauTN += TL_answer_text(t["de"], ds_abcd, 0, 0, dong)
    return cauTN


# ---- Đúng/Sai theo chương ----------------------------------------------------------------------

def _kb_tf(KB, socau, socot):
    cauTF = ""
    for _ in range(socau):
        t = KB()
        rb, dinh, st = t["rb"], t["dinh"], _kb_buoc(t)
        debai = t["de"] + r" Xét tính đúng sai của các khẳng định sau:"

        # a) NB - bất phương trình của từng điều kiện
        ly_a = _kb_giai_he(t)
        dung_a = [(r"Điều kiện về %s được biểu thị bởi bất phương trình $%s %s %s$"
                   % (r["dk"], _kb_lhs(r), r["dau"], _so_vn(r["c"])), ly_a) for r in rb]
        dung_a.append((r"Hai điều kiện $x \ge 0$, $y \ge 0$ xuất hiện vì số lượng không âm", ly_a))
        sai_a = [(r"Điều kiện về %s được biểu thị bởi bất phương trình $%s %s %s$"
                  % (r["dk"], _kb_lhs(r), r"\ge" if r["dau"] == r"\le" else r"\le", _so_vn(r["c"])), ly_a) for r in rb]
        sai_a.append((r"Điều kiện về %s được biểu thị bởi bất phương trình $%s %s %s$"
                      % (rb[0]["dk"], _kb_lhs(rb[0]), "<" if rb[0]["dau"] == r"\le" else ">", _so_vn(rb[0]["c"])), ly_a))
        sai_a.append((r"Điều kiện về %s được biểu thị bởi bất phương trình $%s %s %s$"
                      % (rb[0]["dk"], _pc_lhs(rb[0]["b"], rb[0]["a"]), rb[0]["dau"], _so_vn(rb[0]["c"])), ly_a))
        y1 = _tfa_ds(dung_a, sai_a)

        # b) TH - phương án có thoả mãn mọi điều kiện không (tính trực tiếp)
        K = max(max(v) for v in dinh) + 3
        luoi = [(X, Y) for X in range(1, K) for Y in range(1, K)]
        tot = [P for P in luoi if not _kb_thoa(t, *P)]
        ngoai = [P for P in luoi if _kb_thoa(t, *P)]
        sai_pt = [[P for P in luoi if _kb_thoa(t, *P) == [i]] for i in range(len(rb))]
        diem = [t["opt"], _rd.choice(tot)] + [_rd.choice(s) for s in sai_pt if s] + [_rd.choice(ngoai)]
        dung_b, sai_b = [], []
        for X, Y in dict.fromkeys(diem):
            ok = not _kb_thoa(t, X, Y)
            gd = _kb_giai_diem(t, X, Y)
            (dung_b if ok else sai_b).append((r"Phương án %s thoả mãn mọi điều kiện của bài toán" % (t["pa_xy"] % (X, Y)), gd))
            (sai_b if ok else dung_b).append((r"Phương án %s không thoả mãn mọi điều kiện của bài toán" % (t["pa_xy"] % (X, Y)), gd))
        y2 = _tfa_ds(dung_b, sai_b)

        # c) VD - miền nghiệm: số đỉnh, bị chặn hay không, các đỉnh
        ly_c = _kb_giai_dinh(t)
        gia = [(vx + dx, vy + dy) for vx, vy in dinh for dx in (-1, 1) for dy in (-1, 1)
               if vx + dx >= 0 and vy + dy >= 0 and (vx + dx, vy + dy) not in dinh]
        gia = _rd.sample(list(dict.fromkeys(gia)), 3)
        thuc = _rd.sample(dinh, 3)
        k = len(dinh)
        dung_c = [(r"Miền nghiệm của hệ có đúng $%d$ đỉnh" % k, ly_c),
                  (r"Miền nghiệm của hệ là một miền %s" % ("bị chặn" if t["bi_chan"] else "không bị chặn"), ly_c)]
        dung_c += [(r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % P, ly_c) for P in thuc]
        sai_c = [(r"Miền nghiệm của hệ có đúng $%d$ đỉnh" % (k - 1), ly_c),
                 (r"Miền nghiệm của hệ có đúng $%d$ đỉnh" % (k + 1), ly_c),
                 (r"Miền nghiệm của hệ là một miền %s" % ("không bị chặn" if t["bi_chan"] else "bị chặn"), ly_c)]
        sai_c += [(r"Điểm $\left(%d; %d\right)$ là một đỉnh của miền nghiệm" % P, ly_c) for P in gia]
        y3 = _tfa_ds(dung_c, sai_c)

        # d) VDC - giá trị tối ưu và phương án tối ưu
        ly_d = _kb_giai_F(t)
        xa = max(v[0] for v in dinh)
        yb = max(v[1] for v in dinh)
        khac_dinh = [v for v in dinh if v != t["opt"] and v != (0, 0)]
        sai_gt = []
        for g in [t["best"] + 2 * st] + [g for g in sorted(t["F"]) if g != t["best"] and g > 0] + [t["best"] - 2 * st]:
            if g != t["best"] and g > 0 and g not in sai_gt:
                sai_gt.append(g)
        dung_d = [(_hoa(r"%s bằng %s" % (t["F_cuc"], _kb_so_hien(t, t["best"]))), ly_d),
                  (_hoa(r"%s đạt được khi %s" % (t["F_cuc"], t["pa_xy"] % t["opt"])), ly_d),
                  (r"Nếu chỉ %s thì %s là %s" % (t["pa_x"] % xa, t["F_ten"], _kb_so_hien(t, t["cx"] * xa)), ly_d),
                  (r"Nếu chỉ %s thì %s là %s" % (t["pa_y"] % yb, t["F_ten"], _kb_so_hien(t, t["cy"] * yb)), ly_d)]
        V = _rd.choice(khac_dinh)
        dung_d.append((r"Nếu %s thì %s là %s" % (t["pa_xy"] % V, t["F_ten"], _kb_so_hien(t, t["cx"] * V[0] + t["cy"] * V[1])), ly_d))
        sai_d = [(_hoa(r"%s bằng %s" % (t["F_cuc"], _kb_so_hien(t, g))), ly_d) for g in sai_gt[:2]]
        sai_d += [(_hoa(r"%s đạt được khi %s" % (t["F_cuc"], t["pa_xy"] % W)), ly_d) for W in khac_dinh[:2]]
        sai_d.append((r"Nếu chỉ %s thì %s là %s" % (t["pa_x"] % xa, t["F_ten"], _kb_so_hien(t, t["cx"] * xa + st)), ly_d))
        y4 = _tfa_ds(dung_d, sai_d)

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF

# ---- Tình huống 2: các hàm mỏng gọi khung chung ----
def L10_C2_B3_NB025_MC_C_01(socau, dang=1):
    """Tình huống 2: bất phương trình của điều kiện thứ 1."""
    return _kb_mc_bpt(_kb2_sinh, socau, dang, 0)

def L10_C2_B3_NB025_MC_C_02(socau, dang=1):
    """Tình huống 2: bất phương trình của điều kiện thứ 2."""
    return _kb_mc_bpt(_kb2_sinh, socau, dang, 1)

def L10_C2_B3_NB025_MC_C_03(socau, dang=1):
    """Tình huống 2: bất phương trình của điều kiện thứ 3."""
    return _kb_mc_bpt(_kb2_sinh, socau, dang, 2)

def L10_C2_B4_VD028_MC_D_01(socau, dang=1):
    """Tình huống 2 (VD): chọn hệ bất phương trình."""
    return _kb_mc_vd(_kb2_sinh, socau, dang, "he")

def L10_C2_B4_VD028_MC_D_02(socau, dang=1):
    """Tình huống 2 (VD): chọn phương án thoả mãn."""
    return _kb_mc_vd(_kb2_sinh, socau, dang, "pa")

def L10_C2_B4_VD028_MC_D_03(socau, dang=1):
    """Tình huống 2 (VD): giá trị F của một phương án."""
    return _kb_mc_vd(_kb2_sinh, socau, dang, "gt")

def L10_C2_B4_VD028_SA_D_01(socau, dang=2):
    """Tình huống 2 (VD): số đỉnh của miền nghiệm."""
    return _kb_sa_vd(_kb2_sinh, socau, dang, "dinh")

def L10_C2_B4_VD028_SA_D_02(socau, dang=2):
    """Tình huống 2 (VD): giới hạn khi chỉ dùng loại thứ nhất."""
    return _kb_sa_vd(_kb2_sinh, socau, dang, "xcuc")

def L10_C2_B4_VD028_SA_D_03(socau, dang=2):
    """Tình huống 2 (VD): giới hạn khi chỉ dùng loại thứ hai."""
    return _kb_sa_vd(_kb2_sinh, socau, dang, "ycuc")

def L10_C2_B4_VD028_MC_E_01(socau, dang=1):
    """Tình huống 2 (VDC): giá trị tối ưu."""
    return _kb_toi_uu(_kb2_sinh, socau, dang, "gt", False)

def L10_C2_B4_VD028_MC_E_02(socau, dang=1):
    """Tình huống 2 (VDC): số lượng loại thứ nhất ở phương án tối ưu."""
    return _kb_toi_uu(_kb2_sinh, socau, dang, "x", False)

def L10_C2_B4_VD028_MC_E_03(socau, dang=1):
    """Tình huống 2 (VDC): số lượng loại thứ hai ở phương án tối ưu."""
    return _kb_toi_uu(_kb2_sinh, socau, dang, "y", False)

def L10_C2_B4_VD028_SA_E_01(socau, dang=2):
    """Tình huống 2 (VDC): giá trị tối ưu."""
    return _kb_toi_uu(_kb2_sinh, socau, dang, "gt", True)

def L10_C2_B4_VD028_SA_E_02(socau, dang=2):
    """Tình huống 2 (VDC): số lượng loại thứ nhất ở phương án tối ưu."""
    return _kb_toi_uu(_kb2_sinh, socau, dang, "x", True)

def L10_C2_B4_VD028_SA_E_03(socau, dang=2):
    """Tình huống 2 (VDC): số lượng loại thứ hai ở phương án tối ưu."""
    return _kb_toi_uu(_kb2_sinh, socau, dang, "y", True)

def L10_C2_B4_VD028_TL_C_01(socau, dong=1):
    """Tình huống 2: tự luận 2 ý (a lập hệ, b tối ưu)."""
    return _kb_tl(_kb2_sinh, socau, dong)

def L10_C2_TF_D_01(socau, socot=1):
    """Tình huống 2: đúng/sai theo chương, bốn ý."""
    # Bốn ý tăng dần độ khó (xem _kb_tf):
    # a) NB: bất phương trình của từng điều kiện
    # b) TH: phương án có thoả mãn mọi điều kiện không
    # c) VD: miền nghiệm (số đỉnh, bị chặn, các đỉnh)
    # d) VDC: giá trị và phương án tối ưu
    return _kb_tf(_kb2_sinh, socau, socot)


# ---- Tình huống 3: các hàm mỏng gọi khung chung ----
def L10_C2_B3_NB025_MC_D_01(socau, dang=1):
    """Tình huống 3: bất phương trình của điều kiện thứ 1."""
    return _kb_mc_bpt(_kb3_sinh, socau, dang, 0)

def L10_C2_B3_NB025_MC_D_02(socau, dang=1):
    """Tình huống 3: bất phương trình của điều kiện thứ 2."""
    return _kb_mc_bpt(_kb3_sinh, socau, dang, 1)

def L10_C2_B4_VD028_MC_F_01(socau, dang=1):
    """Tình huống 3 (VD): chọn hệ bất phương trình."""
    return _kb_mc_vd(_kb3_sinh, socau, dang, "he")

def L10_C2_B4_VD028_MC_F_02(socau, dang=1):
    """Tình huống 3 (VD): chọn phương án thoả mãn."""
    return _kb_mc_vd(_kb3_sinh, socau, dang, "pa")

def L10_C2_B4_VD028_MC_F_03(socau, dang=1):
    """Tình huống 3 (VD): giá trị F của một phương án."""
    return _kb_mc_vd(_kb3_sinh, socau, dang, "gt")

def L10_C2_B4_VD028_SA_F_01(socau, dang=2):
    """Tình huống 3 (VD): số đỉnh của miền nghiệm."""
    return _kb_sa_vd(_kb3_sinh, socau, dang, "dinh")

def L10_C2_B4_VD028_SA_F_02(socau, dang=2):
    """Tình huống 3 (VD): giới hạn khi chỉ dùng loại thứ nhất."""
    return _kb_sa_vd(_kb3_sinh, socau, dang, "xcuc")

def L10_C2_B4_VD028_SA_F_03(socau, dang=2):
    """Tình huống 3 (VD): giới hạn khi chỉ dùng loại thứ hai."""
    return _kb_sa_vd(_kb3_sinh, socau, dang, "ycuc")

def L10_C2_B4_VD028_MC_G_01(socau, dang=1):
    """Tình huống 3 (VDC): giá trị tối ưu."""
    return _kb_toi_uu(_kb3_sinh, socau, dang, "gt", False)

def L10_C2_B4_VD028_MC_G_02(socau, dang=1):
    """Tình huống 3 (VDC): số lượng loại thứ nhất ở phương án tối ưu."""
    return _kb_toi_uu(_kb3_sinh, socau, dang, "x", False)

def L10_C2_B4_VD028_MC_G_03(socau, dang=1):
    """Tình huống 3 (VDC): số lượng loại thứ hai ở phương án tối ưu."""
    return _kb_toi_uu(_kb3_sinh, socau, dang, "y", False)

def L10_C2_B4_VD028_SA_G_01(socau, dang=2):
    """Tình huống 3 (VDC): giá trị tối ưu."""
    return _kb_toi_uu(_kb3_sinh, socau, dang, "gt", True)

def L10_C2_B4_VD028_SA_G_02(socau, dang=2):
    """Tình huống 3 (VDC): số lượng loại thứ nhất ở phương án tối ưu."""
    return _kb_toi_uu(_kb3_sinh, socau, dang, "x", True)

def L10_C2_B4_VD028_SA_G_03(socau, dang=2):
    """Tình huống 3 (VDC): số lượng loại thứ hai ở phương án tối ưu."""
    return _kb_toi_uu(_kb3_sinh, socau, dang, "y", True)

def L10_C2_B4_VD028_TL_D_01(socau, dong=1):
    """Tình huống 3: tự luận 2 ý (a lập hệ, b tối ưu)."""
    return _kb_tl(_kb3_sinh, socau, dong)

def L10_C2_TF_E_01(socau, socot=1):
    """Tình huống 3: đúng/sai theo chương, bốn ý."""
    # Bốn ý tăng dần độ khó (xem _kb_tf):
    # a) NB: bất phương trình của từng điều kiện
    # b) TH: phương án có thoả mãn mọi điều kiện không
    # c) VD: miền nghiệm (số đỉnh, bị chặn, các đỉnh)
    # d) VDC: giá trị và phương án tối ưu
    return _kb_tf(_kb3_sinh, socau, socot)


# ---- Tình huống 4: các hàm mỏng gọi khung chung ----
def L10_C2_B3_NB025_MC_E_01(socau, dang=1):
    """Tình huống 4: bất phương trình của điều kiện thứ 1."""
    return _kb_mc_bpt(_kb4_sinh, socau, dang, 0)

def L10_C2_B3_NB025_MC_E_02(socau, dang=1):
    """Tình huống 4: bất phương trình của điều kiện thứ 2."""
    return _kb_mc_bpt(_kb4_sinh, socau, dang, 1)

def L10_C2_B3_NB025_MC_E_03(socau, dang=1):
    """Tình huống 4: bất phương trình của điều kiện thứ 3."""
    return _kb_mc_bpt(_kb4_sinh, socau, dang, 2)

def L10_C2_B4_VD028_MC_H_01(socau, dang=1):
    """Tình huống 4 (VD): chọn hệ bất phương trình."""
    return _kb_mc_vd(_kb4_sinh, socau, dang, "he")

def L10_C2_B4_VD028_MC_H_02(socau, dang=1):
    """Tình huống 4 (VD): chọn phương án thoả mãn."""
    return _kb_mc_vd(_kb4_sinh, socau, dang, "pa")

def L10_C2_B4_VD028_MC_H_03(socau, dang=1):
    """Tình huống 4 (VD): giá trị F của một phương án."""
    return _kb_mc_vd(_kb4_sinh, socau, dang, "gt")

def L10_C2_B4_VD028_SA_H_01(socau, dang=2):
    """Tình huống 4 (VD): số đỉnh của miền nghiệm."""
    return _kb_sa_vd(_kb4_sinh, socau, dang, "dinh")

def L10_C2_B4_VD028_SA_H_02(socau, dang=2):
    """Tình huống 4 (VD): giới hạn khi chỉ dùng loại thứ nhất."""
    return _kb_sa_vd(_kb4_sinh, socau, dang, "xcuc")

def L10_C2_B4_VD028_SA_H_03(socau, dang=2):
    """Tình huống 4 (VD): giới hạn khi chỉ dùng loại thứ hai."""
    return _kb_sa_vd(_kb4_sinh, socau, dang, "ycuc")

def L10_C2_B4_VD028_MC_I_01(socau, dang=1):
    """Tình huống 4 (VDC): giá trị tối ưu."""
    return _kb_toi_uu(_kb4_sinh, socau, dang, "gt", False)

def L10_C2_B4_VD028_MC_I_02(socau, dang=1):
    """Tình huống 4 (VDC): số lượng loại thứ nhất ở phương án tối ưu."""
    return _kb_toi_uu(_kb4_sinh, socau, dang, "x", False)

def L10_C2_B4_VD028_MC_I_03(socau, dang=1):
    """Tình huống 4 (VDC): số lượng loại thứ hai ở phương án tối ưu."""
    return _kb_toi_uu(_kb4_sinh, socau, dang, "y", False)

def L10_C2_B4_VD028_SA_I_01(socau, dang=2):
    """Tình huống 4 (VDC): giá trị tối ưu."""
    return _kb_toi_uu(_kb4_sinh, socau, dang, "gt", True)

def L10_C2_B4_VD028_SA_I_02(socau, dang=2):
    """Tình huống 4 (VDC): số lượng loại thứ nhất ở phương án tối ưu."""
    return _kb_toi_uu(_kb4_sinh, socau, dang, "x", True)

def L10_C2_B4_VD028_SA_I_03(socau, dang=2):
    """Tình huống 4 (VDC): số lượng loại thứ hai ở phương án tối ưu."""
    return _kb_toi_uu(_kb4_sinh, socau, dang, "y", True)

def L10_C2_B4_VD028_TL_E_01(socau, dong=1):
    """Tình huống 4: tự luận 2 ý (a lập hệ, b tối ưu)."""
    return _kb_tl(_kb4_sinh, socau, dong)

def L10_C2_TF_F_01(socau, socot=1):
    """Tình huống 4: đúng/sai theo chương, bốn ý."""
    # Bốn ý tăng dần độ khó (xem _kb_tf):
    # a) NB: bất phương trình của từng điều kiện
    # b) TH: phương án có thoả mãn mọi điều kiện không
    # c) VD: miền nghiệm (số đỉnh, bị chặn, các đỉnh)
    # d) VDC: giá trị và phương án tối ưu
    return _kb_tf(_kb4_sinh, socau, socot)


# =============================================================================================
# DIỆN TÍCH MIỀN NGHIỆM LÀ TAM GIÁC (VD028, ngoai_yccd) - cô Lan 09/10/2026
# Hệ 3 bất phương trình: hai bất phương trình xiên + MỘT bất phương trình song song với Ox hoặc Oy.
#   - Không tham số (VD): hỏi diện tích, toạ độ đỉnh, độ dài cạnh trên đường song song, ...
#   - Có tham số m ở bất phương trình song song, cho diện tích, tìm m (VDC): chỉ một trong hai nghiệm
#     của (m - m0)^2 = h^2 cho miền nghiệm là tam giác, nghiệm kia làm miền nghiệm rỗng.
# Cách làm: chọn trước đỉnh A và hai đỉnh B, C trên đường thẳng song song, rồi viết hai đường thẳng AB, AC
# (nên mọi đỉnh nguyên). Diện tích nguyên.
# =============================================================================================

def _dt_lhs(a, b):
    """a x + b y (a khác 0) viết gọn, có xét dấu."""
    s = ("-" if a < 0 else "") + _pc_hs(abs(a), "x")
    if b:
        s += (" - " if b < 0 else " + ") + _pc_hs(abs(b), "y")
    return s


def _dt_frac(f):
    f = Fraction(f)
    if f.denominator == 1:
        return "%d" % f.numerator
    return r"\dfrac{%d}{%d}" % (f.numerator, f.denominator)


def _dt_cf(f, sep=""):
    """Hệ số đứng trước biểu thức: bỏ nếu bằng 1."""
    return "" if Fraction(f) == 1 else _dt_frac(f) + sep


def _dt_sinh(tham):
    """Sinh một hệ; trả dict mô tả (xem các khoá bên dưới)."""
    while True:
        xa, ya = _rd.randint(-3, 4), _rd.randint(-3, 3)
        h = _rd.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        k = ya + h
        p1, p2 = sorted(_rd.sample([p for p in range(-6, 7) if p], 2))
        if (p2 - p1) * abs(h) % 2:
            continue
        S = (p2 - p1) * abs(h) // 2
        if not 3 <= S <= 60:
            continue
        ds = []
        for p in (p1, p2):
            a, b, c = h, -p, h * xa - p * ya
            g = _math.gcd(_math.gcd(abs(a), abs(b)), abs(c))
            ds.append((a // g, b // g, c // g))
        if max(max(abs(a), abs(b)) for a, b, c in ds) > 7 or max(abs(c) for a, b, c in ds) > 40:
            continue
        A, B, C = (xa, ya), (xa + p1, k), (xa + p2, k)
        if max(max(abs(u), abs(v)) for u, v in (A, B, C)) > 12:
            continue
        par = "y"
        if _rd.random() < 0.5:                                    # song song Oy: đổi vai trò x, y
            par = "x"
            ds = [(b, a, c) for a, b, c in ds]
            A, B, C = (A[1], A[0]), (B[1], B[0]), (C[1], C[0])
        ds = [(a, b, c) if a > 0 else (-a, -b, -c) for a, b, c in ds]
        i = 1 if par == "y" else 0                                # chỉ số biến bị chặn bởi bất phương trình song song
        G = [Fraction(A[j] + B[j] + C[j], 3) for j in (0, 1)]
        lines = []
        for a, b, c in ds:
            v = a * G[0] + b * G[1] - c
            lines.append((a, b, c, r"\le" if v < 0 else r"\ge"))
        pdau = r"\le" if G[i] < k else r"\ge"
        base = p2 - p1
        return dict(tham=tham, par=par, i=i, k=k, pdau=pdau, lines=lines, A=A, B=B, C=C, S=S, base=base,
                    h=abs(h), c0=Fraction(base, 2 * abs(h)), a_par=A[i], m_dung=k, m_sai=2 * A[i] - k)


def _dt_par_tex(d, gtri):
    return r"%s %s %s" % (d["par"], d["pdau"], gtri)


def _dt_he(d, gtri=None, thutu=None):
    """Hệ ba bất phương trình (thứ tự cố định theo d['thutu'] cho cả đề và lời giải)."""
    gtri = _so_vn(d["k"]) if gtri is None else gtri
    dong = ["%s %s %s" % (_dt_lhs(a, b), dau, _so_vn(c)) for a, b, c, dau in d["lines"]] + [_dt_par_tex(d, gtri)]
    dong = [dong[j] for j in d["thutu"]]
    return r"\heva{& " + r" \\ & ".join(dong) + "}"


def _dt_chuan(d):
    d["thutu"] = _rd.sample(range(3), 3)
    return d


def _dt_diem(P):
    return r"\left(%d; %d\right)" % P


def _dt_giai_vd(d):
    """Lời giải chung cho hệ không tham số."""
    (a1, b1, c1, _), (a2, b2, c2, _) = d["lines"]
    var, other = ("y", "x") if d["par"] == "y" else ("x", "y")
    j = 1 - d["i"]
    return (r"Gọi hai đường thẳng $%s = %s$ và $%s = %s$ lần lượt là $(d_1)$, $(d_2)$, còn $%s = %s$ là $(\Delta)$.\\ "
            % (_dt_lhs(a1, b1), _so_vn(c1), _dt_lhs(a2, b2), _so_vn(c2), var, _so_vn(d["k"])) +
            r"$(d_1)$ cắt $(d_2)$ tại $A%s$; $(d_1)$ cắt $(\Delta)$ tại $B%s$; $(d_2)$ cắt $(\Delta)$ tại $C%s$.\\ "
            % (_dt_diem(d["A"]), _dt_diem(d["B"]), _dt_diem(d["C"])) +
            r"Miền nghiệm của hệ là tam giác $ABC$.\\ "
            r"Cạnh $BC$ nằm trên $(\Delta)$ nên $BC = |%d - (%d)| = %d$; khoảng cách từ $A$ đến $(\Delta)$ là $|%d - %d| = %d$.\\ "
            % (d["B"][j], d["C"][j], d["base"], d["A"][d["i"]], d["k"], d["h"]) +
            r"Diện tích $S = \dfrac{1}{2}\cdot %d\cdot %d = %d$." % (d["base"], d["h"], d["S"]))


def _dt_giai_tham(d):
    """Lời giải chung cho hệ có tham số m."""
    (a1, b1, c1, _), (a2, b2, c2, _) = d["lines"]
    var = d["par"]
    m0 = d["a_par"]
    km = Fraction(d["base"], d["h"])
    dm = ("m" if m0 == 0 else "m - %d" % m0 if m0 > 0 else "m + %d" % -m0)
    dk = ("m > %d" if (d["pdau"] == r"\le") else "m < %d") % m0
    return (r"Hai đường thẳng $%s = %s$ và $%s = %s$ cắt nhau tại $A%s$.\\ " % (
                _dt_lhs(a1, b1), _so_vn(c1), _dt_lhs(a2, b2), _so_vn(c2), _dt_diem(d["A"])) +
            r"Để miền nghiệm là tam giác thì đường thẳng $%s = m$ phải cắt hai đường thẳng trên và $A$ nằm cùng phía "
            r"với miền nghiệm, tức là $%s$ (nếu không miền nghiệm rỗng hoặc chỉ là một điểm).\\ " % (var, dk) +
            r"Khi đó đường thẳng $%s = m$ cắt hai đường thẳng tại $B$, $C$ với $BC = %s|%s|$ và khoảng cách từ $A$ đến "
            r"đường thẳng đó là $|%s|$.\\ " % (var, _dt_cf(km, r"\,"), dm, dm) +
            r"Diện tích $S = \dfrac{1}{2}\cdot BC\cdot |%s| = %s\left(%s\right)^2$." % (dm, _dt_cf(d["c0"]), dm))


def _dt_giai_m(d):
    m0 = d["a_par"]
    dm = ("m" if m0 == 0 else "m - %d" % m0 if m0 > 0 else "m + %d" % -m0)
    dk = ("m > %d" if (d["pdau"] == r"\le") else "m < %d") % m0
    return (r"Theo đề, $%s\left(%s\right)^2 = %d$, suy ra $\left(%s\right)^2 = %d$, tức là $%s = \pm %d$.\\ "
            % (_dt_cf(d["c0"]), dm, d["S"], dm, d["h"] ** 2, dm, d["h"]) +
            r"Nghiệm $m = %d$ và $m = %d$. Điều kiện của tam giác là $%s$ nên chọn $m = %d$ (nghiệm $m = %d$ làm miền "
            r"nghiệm rỗng)." % (d["m_dung"], d["m_sai"], dk, d["m_dung"], d["m_sai"]))


def _dt_tex_he(d, tham):
    gt = "m" if tham else None
    return "$%s$" % _dt_he(d, gt)


def _dt_de_vd(d):
    return (r"Cho hệ bất phương trình $%s$. Biết miền nghiệm của hệ là một tam giác." % _dt_he(d))


def _dt_de_tham(d):
    return (r"Cho hệ bất phương trình $%s$ ($m$ là tham số). Biết miền nghiệm của hệ là một tam giác có diện tích "
            r"bằng $%d$ (đơn vị diện tích)." % (_dt_he(d, "m"), d["S"]))


def _dt_kt(tham):
    return _dt_chuan(_dt_sinh(tham))


def _dt_mc_vd(socau, dang, hoi):
    cau = ""
    for _ in range(socau):
        d = _dt_kt(False)
        S = d["S"]
        if hoi == "dt":
            dap = str(S)
            cands = [str(2 * S), str(S + 1), str(S - 1), str(S + 2)]
            cauhoi = r" Diện tích của miền nghiệm đó bằng bao nhiêu (đơn vị diện tích)?"
            bd = lambda k: str(S + k + 2)
        elif hoi == "dinh":
            A = d["A"]
            dap = "$%s$" % _dt_diem(A)
            cands = ["$%s$" % _dt_diem(P) for P in [(A[1], A[0]), (-A[0], A[1]), (A[0], -A[1]), d["B"], (A[0] + 1, A[1])]]
            cauhoi = (r" Đỉnh của tam giác đó không nằm trên đường thẳng $%s = %s$ có toạ độ là" % (d["par"], _so_vn(d["k"])))
            bd = lambda k: "$%s$" % _dt_diem((A[0] + k, A[1] - k))
        else:                                                         # "canh": độ dài cạnh trên đường thẳng song song
            dap = str(d["base"])
            cands = [str(d["base"] + 1), str(d["base"] - 1), str(2 * d["base"]), str(d["h"])]
            cauhoi = r" Độ dài cạnh của tam giác đó nằm trên đường thẳng $%s = %s$ bằng" % (d["par"], _so_vn(d["k"]))
            bd = lambda k: str(d["base"] + k + 1)
        ds = _ba_nhieu2(dap, [c for c in cands if c != dap and not c.startswith("0") and "-" not in c or c.startswith("$")],
                        buoc=bd)
        cau += MC_SA_answer_text(_dt_de_vd(d) + cauhoi, dap, ds, _dt_giai_vd(d), 0, 0, dang)
    return cau


def _dt_sa_vd(socau, dang, hoi):
    cau = ""
    for _ in range(socau):
        d = _dt_kt(False)
        if hoi == "dt":
            dap = d["S"]
            cauhoi = r" Tính diện tích của miền nghiệm đó (đơn vị diện tích)."
        else:
            dap = sum(P[0] + P[1] for P in (d["A"], d["B"], d["C"]))
            cauhoi = r" Tính tổng của tất cả các hoành độ và tung độ của ba đỉnh tam giác đó."
        giai = _dt_giai_vd(d)
        if hoi != "dt":
            giai += (r"\\ Tổng cần tìm: $(%d + %d) + (%d + %d) + (%d + %d) = %d$."
                     % (d["A"][0], d["A"][1], d["B"][0], d["B"][1], d["C"][0], d["C"][1], dap))
        ds = _ba_nhieu2(str(dap), [str(dap + 1), str(dap - 1), str(2 * dap)], buoc=lambda k: str(dap + k + 2))
        cau += MC_SA_answer_text(_dt_de_vd(d) + cauhoi, str(dap), ds, giai, 0, 0, dang)
    return cau


def _dt_mc_vdc(socau, dang, hoi):
    cau = ""
    for _ in range(socau):
        d = _dt_kt(True)
        md, ms, h = d["m_dung"], d["m_sai"], d["h"]
        if hoi == "m":
            dap = "$m = %d$" % md
            cands = ["$m = %d$" % v for v in (ms, d["a_par"] + 2 * h * (1 if md > d["a_par"] else -1), md + 1, md - 1)]
            cauhoi = r" Giá trị của $m$ là"
            bd = lambda k: "$m = %d$" % (md + k + 1)
        else:                                                         # "tap": tập các giá trị m
            dap = r"$m \in \left\{%d\right\}$" % md
            both = sorted((md, ms))
            cands = [r"$m \in \left\{%d; %d\right\}$" % tuple(both), r"$m \in \left\{%d\right\}$" % ms, r"$m \in \varnothing$"]
            cauhoi = r" Tập hợp tất cả các giá trị của $m$ thoả mãn là"
            bd = lambda k: r"$m \in \left\{%d\right\}$" % (md + k + 1)
        ds = _ba_nhieu2(dap, cands, buoc=bd)
        cau += MC_SA_answer_text(_dt_de_tham(d) + cauhoi, dap, ds, _dt_giai_tham(d) + "\\\\\n" + _dt_giai_m(d), 0, 0, dang)
    return cau


def _dt_sa_vdc(socau, dang, hoi):
    cau = ""
    for _ in range(socau):
        d = _dt_kt(True)
        if hoi == "m":
            dap = d["m_dung"]
            cauhoi = r" Tìm giá trị của $m$."
            extra = ""
        else:
            dap = d["base"]
            cauhoi = r" Tính độ dài cạnh của tam giác nằm trên đường thẳng $%s = m$." % d["par"]
            extra = (r"\\ Với $m = %d$ thì $BC = %s|%d - %d| = %d$."
                     % (d["m_dung"], _dt_cf(Fraction(d["base"], d["h"]), r"\,"), d["m_dung"], d["a_par"], dap))
        ds = _ba_nhieu2(str(dap), [str(dap + 1), str(dap - 1), str(2 * dap)], buoc=lambda k: str(dap + k + 2))
        cau += MC_SA_answer_text(_dt_de_tham(d) + cauhoi, str(dap), ds,
                                 _dt_giai_tham(d) + "\\\\\n" + _dt_giai_m(d) + extra, 0, 0, dang)
    return cau


def _dt_tl_vd(socau, dong):
    cau = ""
    for _ in range(socau):
        d = _dt_kt(False)
        ds_abcd = [
            (r"Xác định toạ độ các đỉnh của miền nghiệm của hệ.",
             r"A%s,\ B%s,\ C%s" % (_dt_diem(d["A"]), _dt_diem(d["B"]), _dt_diem(d["C"])),
             _dt_giai_dinh_vd(d)),
            (r"Tính diện tích của miền nghiệm đó (đơn vị diện tích).", "%d" % d["S"], _dt_giai_dt_vd(d)),
        ]
        cau += TL_answer_text(r"Cho hệ bất phương trình $%s$. Biết miền nghiệm của hệ là một tam giác." % _dt_he(d),
                              ds_abcd, 0, 0, dong)
    return cau


def _dt_giai_dinh_vd(d):
    (a1, b1, c1, _), (a2, b2, c2, _) = d["lines"]
    var = d["par"]
    return (r"Gọi hai đường thẳng $%s = %s$ và $%s = %s$ lần lượt là $(d_1)$, $(d_2)$, còn $%s = %s$ là $(\Delta)$.\\ "
            % (_dt_lhs(a1, b1), _so_vn(c1), _dt_lhs(a2, b2), _so_vn(c2), var, _so_vn(d["k"])) +
            r"$(d_1)$ cắt $(d_2)$ tại $A%s$; $(d_1)$ cắt $(\Delta)$ tại $B%s$; $(d_2)$ cắt $(\Delta)$ tại $C%s$.\\ "
            % (_dt_diem(d["A"]), _dt_diem(d["B"]), _dt_diem(d["C"])) +
            r"Cả ba điểm đều thoả mãn hệ nên miền nghiệm là tam giác $ABC$.")


def _dt_giai_dt_vd(d):
    j = 1 - d["i"]
    return (r"Cạnh $BC$ nằm trên $(\Delta)$ nên $BC = |%d - (%d)| = %d$; khoảng cách từ $A$ đến $(\Delta)$ là $|%d - %d| = %d$.\\ "
            % (d["B"][j], d["C"][j], d["base"], d["A"][d["i"]], d["k"], d["h"]) +
            r"Diện tích $S = \dfrac{1}{2}\cdot %d\cdot %d = %d$." % (d["base"], d["h"], d["S"]))


def _dt_tl_vdc(socau, dong):
    cau = ""
    for _ in range(socau):
        d = _dt_kt(True)
        m0 = d["a_par"]
        dm = ("m" if m0 == 0 else "m - %d" % m0 if m0 > 0 else "m + %d" % -m0)
        dk = ("m > %d" if (d["pdau"] == r"\le") else "m < %d") % m0
        ds_abcd = [
            (r"Với điều kiện để miền nghiệm là một tam giác, hãy biểu diễn diện tích $S$ của tam giác đó theo $m$.",
             r"S = %s\left(%s\right)^2\ \left(%s\right)" % (_dt_cf(d["c0"]), dm, dk), _dt_giai_tham(d)),
            (r"Biết diện tích tam giác bằng $%d$ (đơn vị diện tích), tìm $m$." % d["S"],
             r"m = %d" % d["m_dung"], _dt_giai_m(d)),
        ]
        cau += TL_answer_text(r"Cho hệ bất phương trình $%s$ ($m$ là tham số). Biết miền nghiệm của hệ là một tam giác."
                              % _dt_he(d, "m"), ds_abcd, 0, 0, dong)
    return cau


def L10_C2_B4_VD028_MC_J_01(socau, dang=1):
    """Diện tích miền nghiệm (tam giác) của hệ ba bất phương trình, một bất phương trình song song Ox hoặc Oy."""
    return _dt_mc_vd(socau, dang, "dt")


def L10_C2_B4_VD028_MC_J_02(socau, dang=1):
    """Toạ độ đỉnh không nằm trên đường thẳng song song với trục."""
    return _dt_mc_vd(socau, dang, "dinh")


def L10_C2_B4_VD028_MC_J_03(socau, dang=1):
    """Độ dài cạnh nằm trên đường thẳng song song với trục."""
    return _dt_mc_vd(socau, dang, "canh")


def L10_C2_B4_VD028_SA_J_01(socau, dang=2):
    """Diện tích miền nghiệm (tam giác)."""
    return _dt_sa_vd(socau, dang, "dt")


def L10_C2_B4_VD028_SA_J_02(socau, dang=2):
    """Tổng các toạ độ của ba đỉnh."""
    return _dt_sa_vd(socau, dang, "tong")


def L10_C2_B4_VD028_MC_K_01(socau, dang=1):
    """Có tham số (VDC): biết diện tích tam giác, tìm m."""
    return _dt_mc_vdc(socau, dang, "m")


def L10_C2_B4_VD028_MC_K_02(socau, dang=1):
    """Có tham số (VDC): tập các giá trị m."""
    return _dt_mc_vdc(socau, dang, "tap")


def L10_C2_B4_VD028_SA_K_01(socau, dang=2):
    """Có tham số (VDC): tìm m."""
    return _dt_sa_vdc(socau, dang, "m")


def L10_C2_B4_VD028_SA_K_02(socau, dang=2):
    """Có tham số (VDC): độ dài cạnh trên đường thẳng song song."""
    return _dt_sa_vdc(socau, dang, "canh")


def L10_C2_B4_VD028_TL_F_01(socau, dong=1):
    """Tự luận 2 ý: a) toạ độ các đỉnh, b) diện tích tam giác miền nghiệm."""
    return _dt_tl_vd(socau, dong)


def L10_C2_B4_VD028_TL_G_01(socau, dong=1):
    """Tự luận 2 ý có tham số: a) S theo m, b) cho S tìm m."""
    return _dt_tl_vdc(socau, dong)
