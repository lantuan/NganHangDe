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
            "Which of the following inequalities is a linear inequality in two variables?"
        )

        # Lời giải
        giai = f"""
        A linear inequality in two variables has the form $a x + b y {dau} c$ where $a,b$ are not both 0.\\\\
        Among the options, only the inequality:
        \\[{latex(fx[0]*x + fx[1]*y)} {dau} {fx[2]}\\]
        is a linear inequality in two variables, because each variable has exponent 1.
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

        debai = "Which of the following inequalities is a linear inequality in two variables?"

        giai = f"""
        A linear inequality in two variables has the general form $a x + b y {dau} c$ (or with the symbols $<, \\le, \\ge$), where $a,b$ are not both $0$.\\\\
        * Considering the distractor options: they contain the second-degree terms $x^2, y^2$, the product $x \\cdot y$, or the third-degree term ${latex(bien_ngau_nhien ** 3)}$, so they are not linear inequalities in two variables.\\\\
        * Correct option: ${latex(fx[0] * x + fx[1] * y)} {dau} {fx[2]}$ is a linear inequality in two variables because both variables $x, y$ have degree $1$.
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

        debai = f"""Which of the following points lies in the solution region of the inequality ${VT_BPT} {dau} 0$?"""

        # Đáp án đúng
        dapso = f"({diem_dung[0]}; {diem_dung[1]})"

        # Danh sách nhiễu
        dsnhieu = [f"({p[0]}; {p[1]})" for p in diem if p != diem_dung]

        # Lời giải
        giai = f"""
            The given inequality is $${VT_BPT} {dau} 0$$

            We check the correct-answer point $P({diem_dung[0]}; {diem_dung[1]})$:
            Substituting the coordinates of $P$ into the left side of the inequality, we get:
            $$F({diem_dung[0]}; {diem_dung[1]}) = {a}({diem_dung[0]}) + {b}({diem_dung[1]}) + {c} = {F(diem_dung[0], diem_dung[1])}$$

            Since ${F(diem_dung[0], diem_dung[1])} {dau} 0$ is a \\textbf{{TRUE}} statement, the point $P({diem_dung[0]}; {diem_dung[1]})$ belongs to the solution region of the inequality.

            (The remaining points do not satisfy the inequality.)
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
    debai = (r"Which figure below shows the solution region of the inequality $%s %s %d$ "
             r"(the solution region is the \textbf{unshaded} part%s)?"
             % (bt, dau, c, ", including the boundary if it is drawn as a solid line" if co_bang else ""))
    giai = (r"Draw the line $d\colon %s = %d$ as a %s line (the symbol $%s$ %s the equals sign).\\ "
            r"Substitute the point $(%d; %d)$ (not on $d$) into the left side: $%d %s %d$ is %s.\\ "
            r"Therefore the solution region is the half-plane bounded by $d$ that %s the point $(%d; %d)$ (%s the boundary $d$); shade the other half-plane. "
            r"The correct figure is the one in which the boundary $d$ is drawn as a %s line and the unshaded part %s the point $(%d; %d)$."
            % (bt, c, "solid" if co_bang else "dashed", dau, "includes" if co_bang else "does not include",
               X, Y, vt, dau, c, "true" if ok else "false",
               "contains" if ok else "does not contain", X, Y, "including" if co_bang else "not including",
               "solid" if co_bang else "dashed", "contains" if ok else "does not contain", X, Y))
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

        debai = "The figure shows the solution region of which of the following systems of inequalities?"

        giai = f"""
        From the figure, we see that the solution region is bounded by two lines:\\\\
        $d_1: {latex(AB[0] * x + AB[1] * y)} = {c}$ and $d_2: {latex(BC[0] * x + BC[1] * y)} = {d}$.\\\\
        Testing the origin $O(0;0)$ or another point in the unshaded region, we choose the matching system of inequalities:\\\\
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
        mien = {1: 'Triangular region', 2: 'Quadrilateral region', 3: 'Pentagonal region'}[so_dinh]
        Mien_list = ['Triangular region', 'Quadrilateral region', 'Pentagonal region', 'Hexagonal region']
        Mien_list.remove(mien)

        # Loi giai: neu ro hinh chu nhat, hai giao diem M, N, roi thay tung dinh vao ve trai
        cac_dong = []
        for ten, p, g in gia_tri:
            thoa = (g >= VP_MN) if chon_duong else (g <= VP_MN)
            ket = "true" if thoa else "false"
            cac_dong.append(
                f"${ten}\\left({p[0]};{p[1]}\\right)$: ${g} {dau} {VP_MN}$ {ket}")
        so_canh = so_dinh + 2
        giai = (
            f"The inequalities ${fx} \\le x \\le {gx}$ and ${hx} \\le y \\le {kx}$ define "
            f"the rectangle $ABCD$ with $A\\left({A[0]};{A[1]}\\right)$, $B\\left({B[0]};{B[1]}\\right)$, "
            f"$C\\left({C[0]};{C[1]}\\right)$, $D\\left({D[0]};{D[1]}\\right)$.\\\\ "
            f"The line $d \\colon {latex(VT_MN)} = {VP_MN}$ meets the rectangle at "
            f"$M\\left({M[0]};{M[1]}\\right)$ and $N\\left({N[0]};{N[1]}\\right)$.\\\\ "
            f"Substituting the coordinates of the vertices into the left-hand side ${latex(VT_MN)}$ and comparing with ${VP_MN}$:\\\\ "
            + "; ".join(cac_dong) + ".\\\\ "
            f"There are ${so_dinh}$ rectangle vertices that satisfy the inequality ({', '.join(trong)}), so the solution region "
            f"is the polygon whose vertices are those {so_dinh} vertices together with the two points $M$, $N$, "
            f"that is, a polygon with ${so_canh}$ vertices: \\textbf{{{mien.lower()}}}."
        )

        v = [fx, gx, hx, kx, VT_MN, dau, VP_MN, mien, Mien_list, giai]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        fx, gx, hx, kx, VT_MN, dau, VP_MN, mien, Mien_list, giai = v

        debai = f"The solution region of the system of inequalities $\\heva{{& {fx} \\le x \\le {gx} \\\\ & {hx} \\le y \\le {kx} \\\\ & {latex(VT_MN)} {dau} {VP_MN} }}$ is"

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
        GiaTri_list = ['The maximum value', 'The minimum value', 'The sum of the minimum value and the maximum value',
                       'The product of the minimum value and the maximum value']
        GiaTri = np.random.choice(GiaTri_list)

        z = 0
        if GiaTri == 'The maximum value':
            z = max_F
        elif GiaTri == 'The minimum value':
            z = min_F
        elif GiaTri == 'The sum of the minimum value and the maximum value':
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
        debai = f"""{GiaTri} of the expression $F(x;y) = {F_expr}$ for $(x;y)$ in the solution region of the system of inequalities
        $$\\begin{{cases}}
            x \\ge {fx} \\\\
            x \\le {gx} \\\\
            {latex(VT_BD)} {dau_BD} {VP_BD} \\\\
            {latex(VT_CA)} {dau_CA} {VP_CA}
        \\end{{cases}}$$ is"""

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
            The solution region $D$ of the system of inequalities is the convex quadrilateral region $ABDC$ (bounded by the 4 sides $x = {fx}, x = {gx}, {latex(VT_BD)} = {VP_BD}, {latex(VT_CA)} = {VP_CA}$), with vertex coordinates:\\\\
            \\begin{{itemize}}
                \\item $A({A[0]}; {A[1]})$
                \\item $B({B[0]}; {B[1]})$
                \\item $D({D[0]}; {D[1]})$
                \\item $C({C[0]}; {C[1]})$
            \\end{{itemize}}

            The values of the objective function $F(x;y) = {F_expr}$ at the vertices are:\\\\
            \\begin{{itemize}}
                \\item $F(A) = {H0} \\cdot {A[0]} + {H1} \\cdot {A[1]} = {F_A}$
                \\item $F(B) = {H0} \\cdot {B[0]} + {H1} \\cdot {B[1]} = {F_B}$
                \\item $F(D) = {H0} \\cdot {D[0]} + {H1} \\cdot {D[1]} = {F_D}$
                \\item $F(C) = {H0} \\cdot {C[0]} + {H1} \\cdot {C[1]} = {F_C}$
            \\end{{itemize}}

            Applying the theorem on the maximum/minimum values of the objective function over a bounded solution region, we have:\\\\
            $$\\min F = {min_F_giai} \\quad \\text{{and}} \\quad \\max F = {max_F_giai}$$

            According to the problem statement ({GiaTri}):
            \\begin{{itemize}}
                \\item If the maximum value is asked for: $\\max F = {max_F_giai}$.
                \\item If the minimum value is asked for: $\\min F = {min_F_giai}$.
                \\item If the sum is asked for: $\\min F + \\max F = {min_F_giai} + {max_F_giai} = {min_F_giai + max_F_giai}$.
                \\item If the product is asked for: $\\min F \\cdot \\max F = {min_F_giai} \\cdot {max_F_giai} = {min_F_giai * max_F_giai}$.
            \\end{{itemize}}
            Therefore, the answer ({GiaTri}) is ${z}$.
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
        Mien = ['Triangular region', 'Quadrilateral region', 'Pentagonal region', 'Hexagonal region']
        if (Dau == 'Duong') and (len(Duong) == 1):
            dau = r'\ge'
            mien = 'Triangular region'
            Mien.remove(mien)
        elif (Dau == 'Duong') and (len(Duong) == 2):
            dau = r'\ge'
            mien = 'Quadrilateral region'
            Mien.remove(mien)
        elif (Dau == 'Duong') and (len(Duong) == 3):
            dau = r'\ge'
            mien = 'Pentagonal region'
            Mien.remove(mien)
        elif (Dau == 'Am') and (len(Am) == 1):
            dau = r'\le'
            mien = 'Triangular region'
            Mien.remove(mien)
        elif (Dau == 'Am') and (len(Am) == 2):
            dau = r'\le'
            mien = 'Quadrilateral region'
            Mien.remove(mien)
        elif (Dau == 'Am') and (len(Am) == 3):
            dau = r'\le'
            mien = 'Pentagonal region'
            Mien.remove(mien)
        de.write(r"\begin{ex}" + os.linesep)
        de.write(f"The solution region of the system of inequalities $\\heva{{& {fx} \\le x \\le {gx} \\\\ & {hx} \\le y \\le {kx} \\\\ & {latex(VT_MN)} {dau} {VP_MN} }}$ is{os.linesep}")
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
        debai = (r"Given the inequality $%s$, compute the value of the expression "
                 r"$f\left(x; y\right) = %dx + %dy + %d$ at the point $M\left(%d; %d\right)$."
                 % (_bpt_tex(a, b, -c), a, b, c, x0, y0))
        giai = (r"Substitute $x = %d$ and $y = %d$ into the expression:\\ "
                r"$f\left(%d; %d\right) = %d\cdot\left(%d\right) + %d\cdot\left(%d\right) + %d = %d$.\\ "
                r"(This value is %s, so the point $M$ %s the solution region of the given inequality.)"
                % (x0, y0, x0, y0, a, x0, b, y0, c, gt_ve_trai,
                   "less than or equal to $0$" if gt_ve_trai <= 0 else "greater than $0$",
                   "belongs to" if gt_ve_trai <= 0 else "does not belong to"))
        dung = str(gt_ve_trai)
        ds = _ba_nhieu2(dung, [str(a * x0 + b * y0), str(-gt_ve_trai), str(gt_ve_trai + c)],
                        buoc=lambda k: str(gt_ve_trai + 2 * k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C2_B3_NB025_MC_A_01(socau, dang=1):
    """Chọn bất phương trình mô tả đúng một tình huống thực tế."""
    TINH_HUONG = [
        ("A store sells two kinds of writing tools: pencils cost {p} thousand VND each and "
         "ballpoint pens cost {q} thousand VND each. An has {c} thousand VND. Let $x$, $y$ "
         "be the number of pencils and the number of ballpoint pens An buys, respectively. Which of the following inequalities "
         "correctly describes the condition on the amount of money?", "amount of money"),
        ("A tailor shop makes two kinds of garments: a shirt requires {p} labor hours and a jacket requires {q} "
         "labor hours to complete. In one week the shop has at most {c} labor hours. "
         "Let $x$, $y$ be the number of shirts and the number of jackets made during the week, respectively. "
         "Which of the following inequalities correctly describes the condition on labor hours?", "labor hours"),
        ("A person transports two types of goods: each type-one crate weighs {p} kg, each type-two "
         "crate weighs {q} kg. The vehicle can carry at most {c} kg. Let $x$, $y$ be the number of "
         "type-one crates and type-two crates, respectively. Which of the following inequalities describes the condition "
         "on weight correctly?", "weight"),
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
        giai = (r"For $x$ units of type one and $y$ units of type two, the total %s is "
                r"$%dx + %dy$.\\ "
                r"Since it must not exceed $%d$, we have $%dx + %dy \le %d$.\\ "
                r"The sign must be $\le$ (not exceeding), not $\ge$; and the coefficient "
                r"of $x$ must be $%d$, and the coefficient of $y$ must be $%d$."
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
        debai = (r"Given the inequality $%dx + %dy \le %d$. To represent its solution region "
                 r"in the coordinate plane, we first draw the boundary line "
                 r"$d: %dx + %dy = %d$." % (a, b, c, a, b, c))
        ds_abcd = [
            (r"Find the coordinates of the point where $d$ intersects the x-axis.",
             r"\left(%d; 0\right)" % (c // a),
             r"At the intersection with the x-axis, $y = 0$; substituting into $d$:\\ "
             r"$%dx + %d\cdot 0 = %d \Rightarrow x = \dfrac{%d}{%d} = %d$.\\ "
             r"Therefore, the point of intersection is $\left(%d; 0\right)$."
             % (a, b, c, c, a, c // a, c // a)),
            (r"Find the coordinates of the point where $d$ intersects the y-axis.",
             r"\left(0; %d\right)" % (c // b),
             r"At the intersection with the y-axis, $x = 0$; substituting into $d$:\\ "
             r"$%d\cdot 0 + %dy = %d \Rightarrow y = \dfrac{%d}{%d} = %d$.\\ "
             r"Therefore, the point of intersection is $\left(0; %d\right)$. Connecting the two points just found gives "
             r"the line $d$; substituting $O\left(0; 0\right)$ into the left side gives $0 \le %d$ "
             r"(true), so the solution region is the half-plane bounded by $d$ that contains the origin."
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
        giai = (r"A system of linear inequalities in two variables is a system consisting of inequalities "
                r"of the form $ax + by \le c$ (or $<, \ge, >$), where $a$ and $b$ are not both "
                r"$0$ and the variables $x$, $y$ both have degree one.\\ "
                r"$\bullet$ A system with a term $x^{2}$, $y^{2}$ or a product $xy$: rejected.\\ "
                r"$\bullet$ A system with a third variable $z$: rejected, since then it no longer has two variables.\\ "
                r"Only the system of two inequalities in which $x$ and $y$ both have degree one qualifies.")
        ds = _ba_nhieu2(dung,
                        [he(r"%dx^{2} + %dy \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2)),
                         he(r"%dxy + %dy \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2)),
                         he(r"%dx + %dy - z \le %d" % (a1, b1, c1), r"%dx - %dy > %d" % (a2, b2, c2))],
                        buoc=lambda k: he(r"%dx^{%d} + %dy \le %d" % (a1, k + 1, b1, c1),
                                          r"%dx - %dy > %d" % (a2, b2, c2)))
        debai = r"Which of the following systems is a system of linear inequalities in two variables?"
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
            r"has the term $x^{2}$ (second degree)"
    if kieu == "xy":
        return r"%s %s %d" % (_bt((a, "xy"), (b, "y")), dau, c), \
            r"has the product $xy$ (second degree)"
    if kieu == "z":
        return r"%s %s %d" % (_bt((a, "x"), (b, "y"), (-1, "z")), dau, c), \
            r"has a third variable $z$"
    if kieu == "phan_so":
        # a, b > 0 (noi goi truyen so duong)
        return r"\dfrac{%d}{x} + %s %s %d" % (a, _bt((b, "y")), dau, c), \
            r"has the variable $x$ in the denominator"
    return r"%s %s %d" % (_bt((a, "x"), (b, r"\sqrt{y}")), dau, c), \
        r"has the radical $\sqrt{y}$"


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
        debai = (r"Which of the following systems is \textbf{not} a system of linear "
                 r"inequalities in two variables?")
        giai = (r"A system of linear inequalities in two variables consists of inequalities "
                r"of the form $ax + by \le c$ (or $<, \ge, >$) where $a$, $b$ are not both "
                r"$0$. An inequality missing one variable, such as $x \ge 0$ or "
                r"$%s$, still has the correct form (the coefficient of the other variable is $0$)." % _bpt_bac_nhat(0, b, c, d[3]) +
                "\\\\\n"
                r"The system %s is not a system of linear inequalities in two variables, because the inequality $%s$ %s." % (dung, sai, ly_do))
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
        debai = (r"Which inequality, when paired with the inequality $%s$, gives a system of linear inequalities in two variables $x$, $y$?"
                 % khuyet)
        giai = (r"The inequality $%s$ is a linear inequality in two variables (the coefficient of one variable equals $0$)." % khuyet +
                "\\\\\n"
                r"Among the added inequalities: " + "; ".join(ly_do) +
                r", so none of them is a linear inequality in two variables." +
                "\\\\\n"
                r"Only $%s$ is a linear inequality in two variables; the resulting system is %s." % (_bpt_bac_nhat(a, -b, c, d[1]),
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
        debai = (r"Given the system of inequalities $\heva{& x \ge 0 \\ & y \ge 0 \\ & %dx + %dy \le %d}$"
                 % (a, b, c))
        ds_abcd = [
            (r"Find the coordinates of the three vertices of the solution region.",
             r"\left(0;0\right), \left(%d;0\right), \left(0;%d\right)" % (m, n),
             r"The solution region lies in the first quadrant and is bounded by the line "
             r"$d: %dx + %dy = %d$.\\ "
             r"$d$ meets the x-axis at $\left(%d; 0\right)$ and the y-axis at "
             r"$\left(0; %d\right)$; together with the origin $O\left(0;0\right)$ we obtain the three vertices."
             % (a, b, c, m, n)),
            (r"Compute the area of the solution region.", r"%d" % S,
             r"The three vertices form a right triangle with the right angle at $O$; the two legs lie on the two "
             r"coordinate axes and have lengths $%d$ and $%d$.\\ "
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
        debai = (r"Consider the system of inequalities $\heva{& x \ge 0 \\ & y \ge 0 \\ "
                 r"& %s \\ & %s}$. Find the maximum value of the expression "
                 r"$F\left(x; y\right) = %dx + %dy$ on the solution region of the system."
                 % (_bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2), p, q))
        bang = r"\\ ".join(r"$F\left(%d; %d\right) = %d\cdot %d + %d\cdot %d = %d$"
                           % (X, Y, p, X, q, Y, p * X + q * Y) for X, Y in dinh)
        giai = (r"The solution region of the system is a quadrilateral with four vertices "
                r"$\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, "
                r"$\left(0;%d\right)$.\\ "
                r"The expression $F = %dx + %dy$ attains its maximum value at one of the vertices, "
                r"so it suffices to compute $F$ at these four vertices:\\ %s.\\ "
                r"Therefore the maximum value of $F$ equals $%d$."
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
        debai = (r"A workshop manufactures two types of products. Let $x$, $y$ be the numbers of "
                 r"type-one and type-two products made in one day, respectively. The constraints on "
                 r"materials and labor hours lead to the system "
                 r"$\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$, and the profit "
                 r"(in thousands of VND) is $F\left(x; y\right) = %dx + %dy$."
                 % (_bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2), p, q))
        bang = r"\\ ".join(r"$F\left(%d; %d\right) = %d$" % (X, Y, p * X + q * Y)
                           for X, Y in dinh)
        ds_abcd = [
            (r"Find the coordinates of the vertices of the solution region.",
             r"\left(0;0\right), \left(%d;0\right), \left(%d;%d\right), \left(0;%d\right)"
             % (m, u, v, n),
             r"The solution region is the intersection of four half-planes and lies in the first quadrant.\\ "
             r"Solving each pair of boundary-line equations gives the four vertices "
             r"$\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, "
             r"$\left(0;%d\right)$." % (m, u, v, n)),
            (r"How many products of each type should be made per day to maximize the profit? "
             r"What is the maximum profit, in thousands of VND?",
             r"%d" % lon,
             r"The linear expression $F$ attains its maximum value at a vertex of the solution region, "
             r"so it suffices to compare $F$ at the four vertices:\\ %s.\\ "
             r"The maximum is $%d$, attained at $\left(%d; %d\right)$. Therefore each day $%d$ "
             r"type-one products and $%d$ type-two products should be made, and the maximum profit is $%d$ "
             r"thousand VND."
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
        debai = (r"The expression $F\left(x; y\right) = %s$, where $\left(x; y\right)$ lies in the solution "
                 r"region of the system $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$, attains its "
                 r"maximum value at which of the following points?"
                 % (_F_tex(p, q), _bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2)))
        giai = (r"The solution region is a quadrilateral with vertices $\left(0;0\right)$, $\left(%d;0\right)$, "
                r"$\left(%d;%d\right)$, $\left(0;%d\right)$ (the intersections of the boundary lines)."
                % (dinh[1][0], dinh[2][0], dinh[2][1], dinh[3][1]) +
                "\\\\\n" + r"$F$ attains its maximum value at a vertex; compute $F$ at the vertices:\\ " +
                _bang_F(dinh, p, q) + "." + "\\\\\n" +
                r"The maximum value is $%d$, attained at $\left(%d; %d\right)$." % (max(gtri), dinh_lon[0], dinh_lon[1]))
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
        ten = "maximum" if hoi_lon else "minimum"
        hinh = _hinh_mien_da_giac(dinh)
        gtri = [p * X + q * Y for X, Y in dinh]
        dung = "$%d$" % t
        khac = [g for g in dict.fromkeys(gtri) if g != t]
        nhieu = _ba_nhieu2(dung, ["$%d$" % g for g in khac] + ["$%d$" % (-t)],
                           buoc=lambda k: "$%d$" % (t + k + 1))
        debai = (r"The shaded polygonal region in the figure (boundary included) is the solution region of a "
                 r"system of linear inequalities in two variables. The %s value of the expression "
                 r"$F\left(x; y\right) = %s$ on that region equals" % (ten, _F_tex(p, q)))
        giai = (r"Reading from the figure, the solution region is a quadrilateral with four vertices $\left(0;0\right)$, "
                r"$\left(%d;0\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$." % (m, u, v, n) +
                "\\\\\n" + r"$F$ attains its %s value at a vertex:\\ " % ten + _bang_F(dinh, p, q) +
                "." + "\\\\\n" + r"Therefore the %s value of $F$ equals $%d$." % (ten, t))
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, hinh, 0, dang)
    return cauTN


def L10_C2_B4_VD028_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn: GTLN của F trên miền đa giác cho bằng HÌNH VẼ."""
    cau = ''
    for _ in range(socau):
        m, n, u, v, _b1, _b2, dinh = _mien_tu_giac()
        p, q, t = _chon_F_co_dau(dinh, True)
        hinh = _hinh_mien_da_giac(dinh)
        debai = (r"The shaded quadrilateral region in the figure (boundary included) is the solution region of a "
                 r"system of linear inequalities in two variables. Find the maximum value of the expression "
                 r"$F\left(x; y\right) = %s$ on that region." % _F_tex(p, q))
        giai = (r"The vertices of the region: $\left(0;0\right)$, $\left(%d;0\right)$, "
                r"$\left(%d;%d\right)$, $\left(0;%d\right)$." % (m, u, v, n) +
                "\\\\\n" + _bang_F(dinh, p, q) + "." + "\\\\\n" +
                r"The maximum value of $F$ is $%d$." % t)
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
        debai = (r"Consider the system of inequalities $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$. "
                 r"Find the minimum value of the expression $F\left(x; y\right) = %s$ on the solution "
                 r"region of the system." % (_bpt_ge_tex(*l1), _bpt_ge_tex(*l2), _F_tex(p, q)))
        giai = (r"The solution region is unbounded and has vertices $\left(0;%d\right)$, "
                r"$\left(%d;%d\right)$, $\left(%d;0\right)$." % (R[1], Q[0], Q[1], P[0]) +
                "\\\\\n" +
                r"Since the coefficients of $x$ and $y$ in $F$ are both positive, $F$ gets larger as we move farther out; "
                r"the minimum value is attained at a vertex:\\ " + _bang_F(dinh, p, q) + "." +
                "\\\\\n" + r"Therefore the minimum value of $F$ is $%d$." % t)
        nhieu = _ba_nhieu2(str(t), [str(x) for x in g if x != t] + [str(t + 1)],
                           buoc=lambda k: str(t + k + 1))
        cau += MC_SA_answer_text(debai, str(t), nhieu, giai, 0, 0, dang)
    return cau


_BOI_CANH_SAN_XUAT = [
    ("A garment workshop makes two types of clothing: shirts and jackets. Making one shirt requires "
     "{a1} m of fabric and {a2} hr of labor, and making one jacket requires {b1} m of fabric and {b2} "
     "hr of labor. Each day the workshop has at most {c1} meters of fabric and {c2} labor hours. Each shirt "
     "earns a profit of {p} thousand VND, and each jacket earns a profit of {q} thousand VND.",
     "shirts", "jackets", "meters of fabric", "labor hours", "thousand VND"),
    ("A farmer grows corn and potatoes on a plot of land. Each plot of corn requires {a1} "
     "workday(s) and {a2} bag(s) of fertilizer, and each plot of potatoes requires {b1} workday(s) and {b2} bag(s) of fertilizer. "
     "The farmer has at most {c1} workdays and {c2} bags of fertilizer. Each plot of corn earns a profit of {p} hundred "
     "thousand VND, and each plot of potatoes earns a profit of {q} hundred thousand VND.",
     "plots of corn", "plots of potatoes", "workdays", "bags of fertilizer", "hundred thousand VND"),
    ("A bakery makes two kinds of pastry: savory and sweet. Each batch of savory pastries requires "
     "{a1} kg of flour and {a2} hr of baking, and each batch of sweet pastries requires {b1} kg of flour and {b2} hr of "
     "baking. Each day the bakery has at most {c1} kg of flour and {c2} hr of baking. Each batch of savory "
     "pastries earns a profit of {p} ten thousand VND, and each batch of sweet pastries earns a profit of {q} ten thousand VND.",
     "batches of savory pastries", "batches of sweet pastries", "kilograms of flour", "hours of baking", "ten thousand VND"),
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
        debai = (de + r" Let $x$, $y$ be the numbers of %s and %s, respectively." % (bc[1], bc[2]))
        he = (r"\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}"
              % (_bpt_tex(A1, B1, C1), _bpt_tex(A2, B2, C2)))
        ds_abcd = [
            (r"Set up a system of inequalities that describes the conditions of the problem.",
             he,
             r"The numbers of %s and %s are nonnegative: $x \ge 0$, $y \ge 0$.\\ " % (bc[1], bc[2]) +
             r"The number of %s needed: $%s \le %d$.\\ " % (bc[3], _bt((A1, "x"), (B1, "y")), C1) +
             r"The number of %s needed: $%s \le %d$.\\ " % (bc[4], _bt((A2, "x"), (B2, "y")), C2) +
             r"We obtain the system $%s$." % he),
            (r"Find the plan that maximizes the profit.",
             r"\left(%d; %d\right)" % dl,
             r"Profit $F\left(x; y\right) = %s$. The solution region is a quadrilateral with vertices $\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$."
             % (_F_tex(p, q), m, u, v, n) + "\\\\\n" +
             r"$F$ attains its maximum at a vertex:\\ " + _bang_F(dinh, p, q) + "." + "\\\\\n" +
             r"Therefore, make $%d$ %s and $%d$ %s; the maximum profit is $%d$ %s."
             % (dl[0], bc[1], dl[1], bc[2], lon, bc[5])),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


_BOI_CANH_CHI_PHI = [
    ("A poultry farm mixes two types of feed, I and II, for chickens. Each kg of feed I contains {a1} and {a2} units of protein and minerals, respectively, and each kg of feed II contains {b1} and {b2} units of protein and minerals, respectively. Each day the flock needs at least {c1} units of protein and {c2} units of minerals. Feed I costs {p} thousand VND per kg, and feed II costs {q} thousand VND per kg.",
     "kg of feed I", "kg of feed II", "protein units", "mineral units"),
    ("A cafeteria needs to buy two types of vegetables, A and B. Each kg of vegetable A provides {a1} and {a2} units of vitamin C and fiber, respectively, and each kg of vegetable B provides {b1} and {b2} units of vitamin C and fiber, respectively. Each meal needs at least {c1} units of vitamin C and {c2} units of fiber. Vegetable A costs {p} thousand VND per kg, and vegetable B costs {q} thousand VND per kg.",
     "kg of vegetable A", "kg of vegetable B", "vitamin C units", "fiber units"),
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
        debai = de + r" Let $x$ and $y$ be the number of %s and the number of %s to buy, respectively." % (bc[1], bc[2])
        ds_abcd = [
            (r"Set up a system of inequalities that describes the conditions of the problem.", he,
             r"$x \ge 0$, $y \ge 0$; total number of %s: $%s \ge %d$; total number of %s: $%s \ge %d$.\\ "
             % (bc[3], _bt((A1, "x"), (B1, "y")), C1, bc[4], _bt((A2, "x"), (B2, "y")), C2) +
             r"We obtain the system $%s$." % he),
            (r"How many kilograms of each type should be bought to minimize the cost, and what is that minimum cost?",
             r"%d" % nho,
             r"Cost $F\left(x; y\right) = %s$ (thousand VND). The solution region is unbounded, with vertices $\left(0;%d\right)$, $\left(%d;%d\right)$, $\left(%d;0\right)$."
             % (_F_tex(p, q), R[1], Q[0], Q[1], P[0]) + "\\\\\n" +
             r"Since the coefficients of $x$ and $y$ are both positive, $F$ is minimized at a vertex:\\ " +
             _bang_F(dinh, p, q) + "." + "\\\\\n" +
             r"Therefore, buy $%d$ %s and $%d$ %s; the minimum cost is $%d$ thousand VND."
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
            return "positive" if chat else "non-negative"
        return "negative" if chat else "non-positive"
    wx, wy = tu(sx, chat_x), tu(sy, chat_y)
    if wx == wy:
        return r"$x$, $y$ are both %s integers" % wx
    return r"$x$ is a %s integer, $y$ is a %s integer" % (wx, wy)


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

        debai = (r"Given the inequality $%s$. "
                 r"Determine the truth value of each of the following statements:" % bpt)

        # a) NB - nhan dang
        ly_do = (r"It is of the form $ax + by %s c$ with $a = %d$, $b = %d$ not both "
                 r"$0$, and $x$, $y$ both being of the first degree." % (ks, a, b))
        ten = r"``The inequality $%s$ %s a linear inequality with two variables''"
        y1 = [(r"{\True The given inequality is a linear inequality in two variables}",
               r"True. " + ly_do),
              (r"{The given inequality is not a linear inequality in two variables}",
               r"False. " + ly_do),
              (r"{\True " + ten % (bpt, "is") + r" is a true proposition}", r"True. " + ly_do),
              (r"{" + ten % (bpt, "is") + r" is a false proposition}", r"False. " + ly_do),
              (r"{" + ten % (bpt, "is not") + r" is a true proposition}", r"False. " + ly_do),
              (r"{\True " + ten % (bpt, "is not") + r" is a false proposition}", r"True. " + ly_do)]

        # b) TH - thay so kiem tra mot cap so
        x0, y0 = _rd.randint(-4, 4), _rd.randint(-4, 4)
        ve = a * x0 + b * y0
        dung_b = _tfa_thoa(ve, ky, c)
        thay = (r"Substituting into the left-hand side: $%s\cdot %s + %s\cdot %s = %d$. "
                r"We have $%d %s %d$ which is a %s proposition, so this ordered pair %s a solution of the inequality."
                % (_tfa_so(a), _tfa_so(x0), _tfa_so(b), _tfa_so(y0), ve, ve, ks, c,
                   "true" if dung_b else "false", "is" if dung_b else "is not"))
        cap = r"\left(%d; %d\right)" % (x0, y0)
        y2 = [((r"{\True " if dung_b else "{") +
               r"The ordered pair $%s$ is a solution of the inequality}" % cap,
               ("True. " if dung_b else "False. ") + thay),
              ((r"{" if dung_b else r"{\True ") +
               r"The ordered pair $%s$ is not a solution of the inequality}" % cap,
               ("False. " if dung_b else "True. ") + thay),
              ((r"{\True " if dung_b else "{") +
               r"The point $%s$ belongs to the solution region of the inequality}" % cap,
               ("True. " if dung_b else "False. ") + thay),
              ((r"{" if dung_b else r"{\True ") +
               r"The point $%s$ does not belong to the solution region of the inequality}" % cap,
               ("False. " if dung_b else "True. ") + thay)]

        # c) VD - hinh dung nua mat phang nghiem
        # Su that: co_O (chua O hay khong), ngat (khong ke bo d hay co ke bo d)
        thu_O = (r"Substituting $O\left(0;0\right)$ into the left-hand side yields $0$; $0 %s %d$ is a %s proposition "
                 r"so $O$ %s belong to the solution region.\\ The inequality is %s, so the line $d$ %s belong to the solution region."
                 % (ks, c, "true" if co_O else "false", "belongs to" if co_O else "does not belong to",
                    "strict" if ngat else "non-strict", "does not belong to" if ngat else "belongs to"))

        def mo_ta1(chua, ke_bo):
            return (r"The solution region of the inequality is the half-plane bounded by the line "
                    r"$%s$, %s containing the origin $O$ and %s including the line $d$"
                    % (duong, "contains" if chua else "does not contain",
                       "including" if ke_bo else "not including"))

        def mo_ta2(chua, ke_bo):
            return (r"The origin $O$ %s belong to the solution region of the inequality, while points "
                    r"lying on the line $%s$ %s belong to the solution region"
                    % ("belongs to" if chua else "does not belong to", duong,
                       "belongs to" if ke_bo else "does not belong to"))

        dung_O, dung_bo = co_O, (not ngat)
        sai = _rd.choice([(not dung_O, dung_bo), (dung_O, not dung_bo),
                          (not dung_O, not dung_bo)])
        sai2 = _rd.choice([(not dung_O, dung_bo), (dung_O, not dung_bo),
                           (not dung_O, not dung_bo)])
        y3 = [(r"{\True " + mo_ta1(dung_O, dung_bo) + "}", "True. " + thu_O),
              (r"{" + mo_ta1(*sai) + "}", "False. " + thu_O),
              (r"{\True " + mo_ta2(dung_O, dung_bo) + "}", "True. " + thu_O),
              (r"{" + mo_ta2(*sai2) + "}", "False. " + thu_O)]

        # d) VDC - dem nghiem nguyen trong goc phan tu
        dau = _tfa_dieu_kien_xy(sx, sy, t["chat_x"], t["chat_y"])
        giao = (r"The line $d$ intersects the $Ox$ axis at $\left(%d; 0\right)$ and the $Oy$ axis at "
                r"$\left(0; %d\right)$, thus forming a right-angled triangle with both coordinate axes "
                r"located in quadrant %s." % (t["p"], t["q"], _tfa_goc_phan_tu(sx, sy)))
        if co_O:
            chi_tiet = r"\\ ".join(
                r"For $x = %d$ there are $%d$ integer values of $y$ satisfying" % (X, k)
                for X, k in t["theo_x"])
            giai_d = (giao + r"\\ The solution region contains $O$, so the pairs to be counted lie within that triangle "
                      r"(%s the line $d$; points lying on the axes are only counted if the problem allows "
                      r"$x$ or $y$ to be $0$).\\ %s\\ "
                      r"Summing them up yields $%d$ pairs of numbers."
                      % ("not including" if ngat else "including", chi_tiet, dem))
            y4 = [(r"{\True There are exactly $%d$ pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % (dem, dau), "True. " + giai_d),
                  (r"{There are exactly $%d$ pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % (dem + s, dau),
                   "False. " + giai_d)]
        else:
            T = t["T"]
            giai_d = (giao + r"\\ The solution region DOES NOT contain $O$, so it lies on the side far away from the triangle "
                      r"and is unbounded.\\ For instance, all pairs of numbers "
                      r"$\left(%s; %s\right)$ with $t$ a positive integer, $t \ge %d$ satisfy it "
                      r"(the left-hand side is $%d t$ and $%d t %s %d$ for all $t \ge %d$).\\ "
                      r"Thus, there are infinitely many pairs of numbers satisfying it.\\ If mistakenly considering the other half-plane "
                      r"(containing $O$), only $%d$ pairs of numbers lying inside the aforementioned triangle would be counted, "
                      r"which is the incorrect result."
                      % ("t" if sx > 0 else "-t", "t" if sy > 0 else "-t", T, a * sx + b * sy, a * sx + b * sy, ks, c, T, dem))
            y4 = [(r"{\True There are infinitely many pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % dau, "True. " + giai_d),
                  (r"{There are exactly $%d$ pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % (dem, dau), "False. " + giai_d)]

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C2_TF_B_01(socau, socot=1):
    """Đúng/Sai - hệ bất phương trình bậc nhất hai ẩn và bài toán tối ưu."""
    cauTF = ''
    for _ in range(socau):
        while True:
            m, n, u, v, bpt1, bpt2, dinh = _mien_tu_giac()
            p, q = _rd.randint(1, 9), _rd.randint(1, 9)
            gtri = [p * X + q * Y for X, Y in dinh]
            if gtri.count(max(gtri)) == 1:
                break
        (a1, b1, c1), (a2, b2, c2) = bpt1, bpt2
        lon = max(gtri)
        dinh_lon = [d for d in dinh if p * d[0] + q * d[1] == lon][0]

        debai = (r"Consider the system of inequalities $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$ and the expression $F\left(x; y\right) = %dx + %dy$. Determine whether each of the following statements is true or false:"
                 % (_bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2), p, q))

        # a) NB - nhan dang he
        y1 = [(r"{\True The given system is a system of linear inequalities in two variables}",
               r"True. Each inequality in the system is linear in the two variables $x$ and $y$."),
              (r"{The given system is not a system of linear inequalities in two variables}",
               r"False. All four inequalities are linear in $x$ and $y$.")]

        # b) TH - thay mot diem vao he
        y2 = [(r"{\True The point $\left(%d; %d\right)$ belongs to the solution region of the system}" % (u, v),
               r"Substituting $x = %d$, $y = %d$ into each inequality, we find that all are satisfied (this point is exactly the intersection of the two boundary lines), so it belongs to the solution region."
               % (u, v)),
              (r"{The point $\left(%d; %d\right)$ does not belong to the solution region of the system}" % (u, v),
               r"False. It is a vertex of the solution region, so it belongs to the solution region.")]

        # c) VD - phai giai he de biet hinh dang mien nghiem
        y3 = [(r"{\True The solution region of the system is a quadrilateral region}",
               r"The four inequalities give four half-planes; their intersection is a quadrilateral region with four vertices $\left(0;0\right)$, $\left(%d;0\right)$, $\left(%d;%d\right)$, $\left(0;%d\right)$." % (m, u, v, n)),
              (r"{The solution region of the system is a triangular region}",
               r"False. Solving each pair of boundary lines gives FOUR vertices, not three, so the solution region is a quadrilateral.")]

        # d) VDC - tim gia tri lon nhat, phai co toa do cac dinh o y c)
        y4 = [(r"{\True The maximum value of $F$ on the solution region equals $%d$}" % lon,
               r"A linear expression attains its maximum at a vertex of the solution region. Compute $F$ at the four vertices:\\ %s.\\ The maximum is $%d$, attained at $\left(%d; %d\right)$."
               % (r"\\ ".join(r"$F\left(%d; %d\right) = %d$" % (X, Y, p * X + q * Y)
                              for X, Y in dinh), lon, dinh_lon[0], dinh_lon[1])),
              (r"{The maximum value of $F$ on the solution region equals $%d$}" % (lon + p + q),
               r"False. Comparing $F$ at the four vertices, the maximum value is $%d$." % lon)]

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
        khong = [(r"$%s %s %d$" % (_bn_tex(a, 0) + " + y^2" if a else "y^2", d, c), r"it contains $y^2$ (second degree)"),
                 (r"$(x + y)(x - y) %s 0$" % d, r"it expands to $x^2 - y^2$ (second degree)"),
                 (r"$%sxy + y %s %d$" % ("" if abs(a) == 1 else a, d, c), r"it has an $xy$ term (degree two)"),
                 (r"$%s + \dfrac{1}{y} %s %d$" % (_bn_tex(a, 0), d, c), r"it has $\dfrac{1}{y}$, so it is not a polynomial of degree one"),
                 (r"$x^3 %s %s %s %d$" % ("+" if b > 0 else "-", _bn_tex(0, abs(b)), d, c), r"it has $x^3$")]
        k = random.randint(2, 5)
        la = [(r"$%s %s %d$" % (_bn_tex(a, b), d, c), "it has the form $ax + by %s c$" % d),
              (r"$%s %s 0$" % (_bn_tex(a, 0, c), d), r"it is missing $y$, that is, the coefficient of $y$ is $0$, but it is still linear in two variables"),
              (r"$%dx - %d(y - x + %d) %s 0$" % (abs(a) + 1, k, abs(c) + 1, d),
               r"it expands to $%s %s 0$" % (_bn_tex(abs(a) + 1 + k, -k, -k * (abs(c) + 1)), d)),
              (r"$%s %s %s$" % (_bn_tex(a, 0), d, _bn_tex(0, b, c)), r"it rearranges to $%s %s 0$" % (_bn_tex(a, -b, -c), d))]
        sai = random.choice(khong)
        dung3 = random.sample(la, 3)
        debai = r"Which of the following inequalities is \textbf{not} a linear inequality in two variables?"
        giai = (r"%s is not a linear inequality in two variables because %s.\\ " % sai
                + r"\\ ".join(r"%s is a linear inequality in two variables (%s)." % t for t in dung3))
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
        debai = (r"The ordered pair $\left(%d; %d\right)$ %s a solution of which of the following inequalities?"
                 % (x0, y0, "is" if hoi_thuoc else r"is \textbf{not}"))

        def thay(m):
            _, a, b, c, d, v = m
            return r"$%s %s 0$: the left side equals $%d$, and $%d %s 0$ is %s" % (
                _bn_tex(a, b, c), d, v, v, d, "true" if _DAU_KT[d](v) else "false")
        giai = (r"Substitute $x = %d$, $y = %d$ into the left side of each inequality:\\ " % (x0, y0)
                + r"\\ ".join(thay(m) for m in [chon] + khac)
                + r".\\ Therefore, the answer is %s." % chon[0])
        cauTN += MC_SA_answer_text(debai, chon[0], [m[0] for m in khac], giai, 0, 0, dang)
    return cauTN


def _thuc_te_bpt():
    """Tình huống thực tế -> (đề, đáp án, nhiễu, lời giải). Bất phương trình đã rút gọn."""
    kieu = random.randint(0, 3)
    if kieu == 0:
        p, q = random.choice([(26, 20), (24, 18), (22, 16), (30, 20), (28, 21)])
        c = 2 * p
        g = math.gcd(math.gcd(p, q), c)
        de = (r"In $1$ serving (100 g) of beef there are about $%d$ g of protein, and in $1$ serving of tilapia there are about $%d$ g "
              r"of protein. A person needs at least $%d$ g of protein per day. Let $x$ and $y$ be the number of servings of beef "
              r"and tilapia, respectively, that the person eats in one day. The inequality describing the required amount of protein is"
              % (p, q, c))
        dau, P, Q, C = r"\ge", p // g, q // g, c // g
        giai = (r"The amount of protein is $%dx + %dy$ (g). ``At least $%d$ g'' means $%dx + %dy \ge %d$; dividing both sides by "
                r"$%d$ gives $%dx + %dy \ge %d$." % (p, q, c, p, q, c, g, P, Q, C))
        sai = [(P, Q, ">", C), (P, Q, r"\le", C), (Q, P, r"\ge", C)]
    elif kieu == 1:
        p, q = random.choice([(1190, 1390), (1100, 1500), (1200, 1400), (990, 1290)])
        T = random.choice([100, 150, 200])
        g = math.gcd(math.gcd(p, q), 1000 * T)
        de = (r"A phone plan charges $%d$ VND per minute for in-network calls and $%d$ VND per minute for out-of-network calls. "
              r"Let $x$ and $y$ be the number of in-network and out-of-network minutes in one month, respectively. The inequality describing "
              r"a monthly bill of less than $%d$ thousand VND is" % (p, q, T))
        dau, P, Q, C = "<", p // g, q // g, 1000 * T // g
        giai = (r"The amount is $%dx + %dy$ (VND). ``Less than $%d$ thousand VND'' means $%dx + %dy < %d$; dividing both sides by "
                r"$%d$ gives $%dx + %dy < %d$." % (p, q, T, p, q, 1000 * T, g, P, Q, C))
        sai = [(P, Q, r"\le", C), (Q, P, "<", C), (P, Q, "<", T)]
    elif kieu == 2:
        p, q = random.choice([(15, 10), (20, 15), (25, 20), (30, 20), (18, 12)])
        c = random.choice([600, 900, 1200])
        g = math.gcd(math.gcd(p, q), c)
        de = (r"Outside of school hours, Nam earns $%d$ thousand VND per hour helping at a rice restaurant and $%d$ thousand "
              r"VND per hour helping at a grocery store. Let $x$ and $y$ be the number of hours per week he helps at the restaurant and at the "
              r"grocery store, respectively. The inequality for Nam to earn at least $%d$ thousand VND per week is" % (p, q, c))
        dau, P, Q, C = r"\ge", p // g, q // g, c // g
        giai = (r"The amount earned is $%dx + %dy$ (thousand VND). ``At least $%d$'' means $%dx + %dy \ge %d$; dividing both "
                r"sides by $%d$ gives $%dx + %dy \ge %d$." % (p, q, c, p, q, c, g, P, Q, C))
        sai = [(P, Q, ">", C), (P, Q, r"\le", C), (Q, P, r"\ge", C)]
    else:
        F1, F2 = random.choice([(900, 1200), (800, 1000), (1000, 1500)])
        p, q = random.choice([(10, 15), (8, 12), (12, 18)])
        T = random.choice([20000, 25000, 30000])
        con = T - 5 * F1 - 2 * F2
        g = math.gcd(math.gcd(p, q), con)
        de = (r"Mr. A rents a car for one week. From Monday to Friday the fixed fee is $%d$ thousand VND/day plus "
              r"$%d$ thousand VND/km; on Saturday and Sunday the fixed fee is $%d$ thousand VND/day plus $%d$ thousand VND/km. Let "
              r"$x$ and $y$ be the number of km Mr. A drives on the days from Monday to Friday and on the two weekend days, respectively. "
              r"The inequality for the total cost to be at most $%d$ million VND is" % (F1, p, F2, q, T // 1000))
        dau, P, Q, C = r"\le", p // g, q // g, con // g
        giai = (r"The total cost (thousand VND) is $5\cdot %d + %dx + 2\cdot %d + %dy$. ``At most $%d$ million'' means "
                r"$%d + %dx + %dy \le %d$, that is, $%dx + %dy \le %d$; dividing both sides by $%d$ gives $%dx + %dy \le %d$."
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


def L10_C2_TF_A_02(socau, socot=1):
    r"""Đúng/Sai - bất phương trình $ax + by + c > 0$ (dấu bất kì): số nghiệm,
    điểm $O$, một điểm NẰM TRÊN BỜ, mô tả miền nghiệm (kể / không kể bờ, chứa /
    không chứa $O$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua L10_C2_TF_A, theo cau "x - 2y + 6 >
    0: vo so nghiem; (0; 0); (0; 3); mien nghiem" trong phan bai tap Bai 3.
    Co Lan duyet.
    """
    cauTF = ""
    for _ in range(socau):
        a = random.choice([i for i in range(-4, 5) if i])
        b = random.choice([i for i in range(-4, 5) if i])
        c = random.choice([i for i in range(-9, 10) if i])
        # điểm trên bờ: a*x1 + b*y1 + c = 0, chọn x1 = 0 nếu b | c, ngược lại y1 = 0 nếu a | c
        if c % b == 0:
            P = (0, -c // b)
        elif c % a == 0:
            P = (-c // a, 0)
        else:
            c = b * random.choice([1, 2, 3, -1, -2])
            P = (0, -c // b)
        d = random.choice(list(_DAU_KT))
        f = _DAU_KT[d]
        bt = _bn_tex(a, b, c)
        O_ok = f(c)
        ke_bo = d in (r"\le", r"\ge")
        debai = r"Consider the inequality $%s %s 0$. Determine whether each of the following statements is true or false:" % (bt, d)
        # a) NB
        y1 = [(r"{\True The inequality has infinitely many solutions}",
               r"True. The solution region is an entire half-plane, so there are infinitely many solutions."),
              (r"{The inequality has exactly one solution}",
               r"False. The solution region is a half-plane, so there are infinitely many solutions.")]
        # b) TH
        gb = r"Substitute $(0; 0)$: the left side equals $%d$, and $%d %s 0$ is %s." % (c, c, d, "true" if O_ok else "false")
        y2 = [((r"{\True " if O_ok else "{") + r"The ordered pair $(0; 0)$ is a solution of the inequality}",
               ("True. " if O_ok else "False. ") + gb),
              ((r"{" if O_ok else r"{\True ") + r"The ordered pair $(0; 0)$ is not a solution of the inequality}",
               ("False. " if O_ok else "True. ") + gb)]
        # c) VD - điểm nằm trên bờ
        gc = (r"Substitute $(%d; %d)$: the left side equals $0$, so the point lies on the boundary line $%s = 0$; %s."
              % (P[0], P[1], bt, "the sign includes equality, so it is still a solution" if ke_bo else "the sign does not include equality, so it is not a solution"))
        y3 = [((r"{\True " if ke_bo else "{") + r"The ordered pair $(%d; %d)$ is a solution of the inequality}" % P,
               ("True. " if ke_bo else "False. ") + gc),
              ((r"{" if ke_bo else r"{\True ") + r"The ordered pair $(%d; %d)$ is not a solution of the inequality}" % P,
               ("False. " if ke_bo else "True. ") + gc)]
        # d) VDC - mô tả miền nghiệm
        mo_ta = lambda ke, chua: (r"The solution region is the half-plane with boundary $\Delta\colon %s = 0$ that %s the origin $O$ (%s the boundary $\Delta$)"
                                  % (bt, "contains" if chua else "does not contain", "including" if ke else "not including"))
        gd = (r"$O$ is %sin the solution region (part b), and the sign $%s$ %s, so the solution region is the half-plane with boundary $\Delta$ that %s $O$, %s the boundary."
              % ("" if O_ok else "not ", d, "includes equality" if ke_bo else "does not include equality",
                 "contains" if O_ok else "does not contain", "including" if ke_bo else "not including"))
        sai_ke, sai_chua = random.choice([(not ke_bo, O_ok), (ke_bo, not O_ok)])
        y4 = [(r"{\True %s}" % mo_ta(ke_bo, O_ok), "True. " + gd),
              (r"{%s}" % mo_ta(sai_ke, sai_chua), "False. " + gd)]
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


def L10_C2_TF_A_03(socau, socot=1):
    r"""Đúng/Sai - biết miền nghiệm (mô tả bằng lời): bờ $d$ đi qua $A(p; 0)$,
    $B(0; q)$, có / không chứa $O$, kể / không kể bờ. Xét điểm thuộc miền,
    phương trình $d$, bất phương trình.

    CLAUDE THEM 30/09/2026 - bien the 03 cua L10_C2_TF_A, theo hai cau "mien
    nghiem khong gach cheo, bo d qua (-5; 0), (0; 2)" va "qua (3; 0), (0; 2)"
    trong phan bai tap Bai 3. Hinh duoc thay bang mo ta bang loi de web hien
    duoc. Co Lan duyet.
    """
    cauTF = ""
    for _ in range(socau):
        p = random.choice([i for i in range(-6, 7) if abs(i) >= 2])
        q = random.choice([i for i in range(-6, 7) if abs(i) >= 2])
        # d: x/p + y/q = 1  <=>  q x + p y - p q = 0
        g = math.gcd(math.gcd(abs(q), abs(p)), abs(p * q))
        A_, B_, C_ = q // g, p // g, -p * q // g
        if A_ < 0:                      # cho hệ số của x dương, đề nhìn gọn hơn
            A_, B_, C_ = -A_, -B_, -C_
        chua_O = random.random() < 0.5
        ke = random.random() < 0.5
        # dấu sao cho O thỏa mãn khi chua_O: tại O vế trái bằng C_
        if (C_ < 0) == chua_O:
            dau = r"\le" if ke else "<"
        else:
            dau = r"\ge" if ke else ">"
        f = _DAU_KT[dau]
        bt = _bn_tex(A_, B_, C_)
        # một điểm kiểm tra không nằm trên bờ
        while True:
            X, Y = random.randint(-6, 6), random.randint(-6, 6)
            if A_ * X + B_ * Y + C_ != 0:
                break
        X_ok = f(A_ * X + B_ * Y + C_)
        debai = (r"Consider a linear inequality in two variables whose solution region is the half-plane that %s the origin $O$ (%s the boundary line $d$), "
                 r"where the line $d$ passes through the two points $A(%d; 0)$ and $B(0; %d)$. Determine whether each of the "
                 r"following statements is true or false:" % ("contains" if chua_O else "does not contain", "including" if ke else "not including", p, q))
        # a) NB
        y1 = [((r"{\True " if chua_O else "{") + r"The point $O(0; 0)$ belongs to the solution region of the inequality}",
               ("True" if chua_O else "False") + r" by hypothesis: the solution region %s $O$." % ("contains" if chua_O else "does not contain")),
              ((r"{" if chua_O else r"{\True ") + r"The point $O(0; 0)$ does not belong to the solution region of the inequality}",
               ("False" if chua_O else "True") + r" by hypothesis: the solution region %s $O$." % ("contains" if chua_O else "does not contain"))]
        # b) TH
        gb = (r"$d$ passes through $A(%d; 0)$, $B(0; %d)$, so $d\colon \dfrac{x}{%d} + \dfrac{y}{%d} = 1 \Leftrightarrow %s = 0$."
              % (p, q, p, q, bt))
        sai_d = _bn_tex(B_, A_, C_) if A_ != B_ else _bn_tex(A_, -B_, C_)
        y2 = [(r"{\True The equation of the line $d$ is $%s = 0$}" % bt, "True. " + gb),
              (r"{The equation of the line $d$ is $%s = 0$}" % sai_d, "False. " + gb)]
        # c) VD
        gc = (r"At $O$ the left side $%s$ equals $%d$; the solution region %s $O$ (%s the boundary), so the inequality is $%s %s 0$."
              % (bt, C_, "contains" if chua_O else "does not contain", "including" if ke else "not including", bt, dau))
        doi = {"<": ">", ">": "<", r"\le": r"\ge", r"\ge": r"\le"}[dau]
        bo = {"<": r"\le", r"\le": "<", ">": r"\ge", r"\ge": ">"}[dau]
        y3 = [(r"{\True The given inequality is $%s %s 0$}" % (bt, dau), "True. " + gc),
              (r"{The given inequality is $%s %s 0$}" % (bt, random.choice([doi, bo])), "False. " + gc)]
        # d) VDC
        gd = (r"Substitute $(%d; %d)$ into the left side to get $%d$, and $%d %s 0$ is %s." %
              (X, Y, A_ * X + B_ * Y + C_, A_ * X + B_ * Y + C_, dau, "true" if X_ok else "false"))
        y4 = [((r"{\True " if X_ok else "{") + r"The point $(%d; %d)$ belongs to the solution region of the inequality}" % (X, Y),
               ("True. " if X_ok else "False. ") + gd),
              ((r"{" if X_ok else r"{\True ") + r"The point $(%d; %d)$ does not belong to the solution region of the inequality}" % (X, Y),
               ("False. " if X_ok else "True. ") + gd)]
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

        debai = (r"Given the inequality $%s$ and four points $%s$, $%s$, $%s$, $%s$. "
                 r"Determine the truth value of each of the following statements:" % ((bpt,) + tuple(tex_d)))

        def thay(i):
            X, Y = diem[i]
            g = a * X + b * Y
            return (r"Substituting the coordinates of point $%s$ into the left-hand side: "
                    r"$%s\cdot %s + %s\cdot %s = %d$; $%d %s %d$ is a %s proposition, "
                    r"so the point $%s$ %s the solution region."
                    % (TEN[i], _tfa_so(a), _tfa_so(X), _tfa_so(b), _tfa_so(Y), g, g, ks, c,
                       "true" if thuoc[i] else "false", TEN[i],
                       "belongs to" if thuoc[i] else "does not belong to"))

        # a) NB - nhan dang
        ly_do = (r"It is of the form $ax + by %s c$ with $a = %d$, $b = %d$ not both "
                 r"$0$, and $x$, $y$ both being of the first degree." % (ks, a, b))
        ten = r"``The inequality $%s$ %s a linear inequality with two variables''"
        y1 = [(r"{\True The given inequality is a linear inequality in two variables}",
               r"True. " + ly_do),
              (r"{The given inequality is not a linear inequality in two variables}",
               r"False. " + ly_do),
              (r"{\True " + ten % (bpt, "is") + r" is a true proposition}", r"True. " + ly_do),
              (r"{" + ten % (bpt, "is") + r" is a false proposition}", r"False. " + ly_do),
              (r"{" + ten % (bpt, "is not") + r" is a true proposition}", r"False. " + ly_do),
              (r"{\True " + ten % (bpt, "is not") + r" is a false proposition}", r"True. " + ly_do)]

        # b) TH - mot trong bon diem co thuoc mien nghiem khong
        k = _rd.randrange(4)
        dung_b = thuoc[k]
        cap = tex_d[k]
        gb = thay(k)
        y2 = [((r"{\True " if dung_b else "{") +
               r"The point $%s$ belongs to the solution region of the inequality}" % cap,
               ("True. " if dung_b else "False. ") + gb),
              ((r"{" if dung_b else r"{\True ") +
               r"The point $%s$ does not belong to the solution region of the inequality}" % cap,
               ("False. " if dung_b else "True. ") + gb),
              ((r"{\True " if dung_b else "{") +
               r"The coordinates of point $%s$ are a solution of the inequality}" % TEN[k],
               ("True. " if dung_b else "False. ") + gb),
              ((r"{" if dung_b else r"{\True ") +
               r"The coordinates of point $%s$ are not a solution of the inequality}" % TEN[k],
               ("False. " if dung_b else "True. ") + gb)]

        # c) VD - dem so diem thuoc / khong thuoc mien nghiem trong bon diem
        def cau_c(so, thuoc_mn):
            if so == 0:
                return (r"Among the given points, there is no point that belongs to the solution "
                        r"region of the inequality" if thuoc_mn else
                        r"Among the given points, there is no point that lies outside the solution "
                        r"region of the inequality")
            if so == 4:
                return (r"Among the given points, all four points belong to the solution region "
                        r"of the inequality" if thuoc_mn else
                        r"Among the given points, all four points lie outside the solution region "
                        r"of the inequality")
            return ((r"Among the given points, the number of points belonging to the solution "
                     r"region of the inequality is exactly $%d$" if thuoc_mn else
                     r"Among the given points, the number of points lying outside the solution "
                     r"region of the inequality is exactly $%d$") % so)

        ds_in = ", ".join(TEN[i] for i in range(4) if thuoc[i])
        ds_ngoai = ", ".join(TEN[i] for i in range(4) if not thuoc[i])
        gc = (r"\\ ".join(thay(i) for i in range(4)) +
              r"\\ Hence there are $%d$ point(s) belonging to the solution region%s and $%d$ "
              r"point(s) not belonging to it%s."
              % (n_in, " (%s)" % ds_in if ds_in else "",
                 n_ngoai, " (%s)" % ds_ngoai if ds_ngoai else ""))
        sai_in = _rd.choice([i for i in range(5) if i != n_in])
        sai_ngoai = _rd.choice([i for i in range(5) if i != n_ngoai])
        y3 = [(r"{\True " + cau_c(n_in, True) + "}", "True. " + gc),
              (r"{" + cau_c(sai_in, True) + "}", "False. " + gc),
              (r"{\True " + cau_c(n_ngoai, False) + "}", "True. " + gc),
              (r"{" + cau_c(sai_ngoai, False) + "}", "False. " + gc)]

        # d) VDC - dem nghiem nguyen trong goc phan tu
        dau = _tfa_dieu_kien_xy(sx, sy, t["chat_x"], t["chat_y"])
        giao = (r"The line $d$ intersects the $Ox$ axis at $\left(%d; 0\right)$ and the $Oy$ axis at "
                r"$\left(0; %d\right)$, thus forming a right-angled triangle with both coordinate axes "
                r"located in quadrant %s." % (t["p"], t["q"], _tfa_goc_phan_tu(sx, sy)))
        if co_O:
            chi_tiet = r"\\ ".join(
                r"For $x = %d$ there are $%d$ integer values of $y$ satisfying" % (X, k)
                for X, k in t["theo_x"])
            giai_d = (giao + r"\\ The solution region contains $O$, so the pairs to be counted lie within that triangle "
                      r"(%s the line $d$; points lying on the axes are only counted if the problem allows "
                      r"$x$ or $y$ to be $0$).\\ %s\\ "
                      r"Summing them up yields $%d$ pairs of numbers."
                      % ("not including" if ngat else "including", chi_tiet, dem))
            y4 = [(r"{\True There are exactly $%d$ pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % (dem, dau), "True. " + giai_d),
                  (r"{There are exactly $%d$ pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % (dem + s, dau),
                   "False. " + giai_d)]
        else:
            T = t["T"]
            giai_d = (giao + r"\\ The solution region DOES NOT contain $O$, so it lies on the side far away from the triangle "
                      r"and is unbounded.\\ For instance, all pairs of numbers "
                      r"$\left(%s; %s\right)$ with $t$ a positive integer, $t \ge %d$ satisfy it "
                      r"(the left-hand side is $%d t$ and $%d t %s %d$ for all $t \ge %d$).\\ "
                      r"Thus, there are infinitely many pairs of numbers satisfying it.\\ If mistakenly considering the other half-plane "
                      r"(containing $O$), only $%d$ pairs of numbers lying inside the aforementioned triangle would be counted, "
                      r"which is the incorrect result."
                      % ("t" if sx > 0 else "-t", "t" if sy > 0 else "-t", T, a * sx + b * sy, a * sx + b * sy, ks, c, T, dem))
            y4 = [(r"{\True There are infinitely many pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % dau, "True. " + giai_d),
                  (r"{There are exactly $%d$ pairs of numbers $\left(x; y\right)$ satisfying the inequality, "
                   r"where %s}" % (dem, dau), "False. " + giai_d)]

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


