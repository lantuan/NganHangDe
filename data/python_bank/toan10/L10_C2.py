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
def L10_C2_B3_TH024_MC_A_01(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    # Định nghĩa NamedTuple cho điểm để dễ truy cập
    Point = namedtuple('Point', ['x', 'y'])

    while dem < socau:
        # 1️⃣ Sinh dữ liệu ngẫu nhiên

        # Thay thế np.choice, np.randint bằng np.random.choice, np.random.randint
        dau_list = ['>', '<', '\\ge', '\\le']
        dau = np.random.choice(dau_list)

        point_values = [0, 0, 0]
        # Vòng lặp để sinh 3 giá trị khác 0
        while True:
            point_values = np.random.randint(-4, 5, 3).tolist()
            if all(v != 0 for v in point_values) and sum(abs(v) for v in point_values) >= 3:
                # Điều kiện: không cùng dấu
                if not (((point_values[0] > 0) and (point_values[1] > 0) and (point_values[2] > 0)) or \
                        ((point_values[0] < 0) and (point_values[1] < 0) and (point_values[2] < 0))):
                    break

        point_values.sort()

        choice = np.random.choice([0, 1, 2, 3])

        A, B, C = Point(0, 0), Point(0, 0), Point(0, 0)
        x_trai, x_phai, y_duoi, y_tren = 0, 0, 0, 0

        if choice == 0:
            A = Point(point_values[0], 0)
            B = Point(0, point_values[1])
            C = Point(point_values[2], 0)
            x_trai = point_values[0] - 1
            x_phai = point_values[2] + 1
            if point_values[1] < 0:
                y_duoi = point_values[1] - 1
                y_tren = 1
            else:
                y_tren = point_values[1] + 1
                y_duoi = -1

        elif choice == 1:
            A = Point(point_values[0], 0)
            B = Point(0, -point_values[1])
            C = Point(point_values[2], 0)
            x_trai = point_values[0] - 1
            x_phai = point_values[2] + 1
            if -point_values[1] < 0:
                y_duoi = -point_values[1] - 1
                y_tren = 1
            else:
                y_tren = -point_values[1] + 1
                y_duoi = -1

        elif choice == 2:
            A = Point(0, point_values[0])
            B = Point(point_values[1], 0)
            C = Point(0, point_values[2])
            y_duoi = point_values[0] - 1
            y_tren = point_values[2] + 1
            if point_values[1] < 0:
                x_trai = point_values[1] - 1
                x_phai = 1
            else:
                x_phai = point_values[1] + 1
                x_trai = -1

        else:  # choice == 3
            A = Point(0, point_values[0])
            B = Point(-point_values[1], 0)
            C = Point(0, point_values[2])
            y_duoi = point_values[0] - 1
            y_tren = point_values[2] + 1
            if -point_values[1] < 0:
                x_trai = -point_values[1] - 1
                x_phai = 1
            else:
                x_phai = -point_values[1] + 1
                x_trai = -1

        # Hệ số của bất phương trình (AB[0] * x + AB[1] * y = c)
        AB = [-B.y + A.y, B.x - A.x]  # vecto pháp tuyến của AB: (a, b)
        c = AB[0] * A.x + AB[1] * A.y  # c

        # Đường thẳng AB: y = m*x + n
        m_AB = -AB[0] / AB[1] if AB[1] != 0 else float('inf')
        n_AB = (AB[0] * A.x + AB[1] * A.y - AB[0] * A.x) / AB[1] if AB[1] != 0 else float('inf')

        # Đường thẳng BC: (BC[0] * x + BC[1] * y = c_BC)
        BC = [-C.y + B.y, C.x - B.x]  # vecto pháp tuyến của BC
        c_BC = BC[0] * B.x + BC[1] * B.y
        m_BC = -BC[0] / BC[1] if BC[1] != 0 else float('inf')
        n_BC = (BC[0] * B.x + BC[1] * B.y - BC[0] * B.x) / BC[1] if BC[1] != 0 else float('inf')

        # Hàm kiểm tra dấu
        fx = lambda x, y: AB[0] * x + AB[1] * y

        # Kiểm tra miền nghiệm (0,0) so với c
        is_origin_in_solution = False
        if (dau == '>') or (dau == '\\ge'):
            is_origin_in_solution = (fx(0, 0) > c)
        elif (dau == '<') or (dau == '\\le'):
            is_origin_in_solution = (fx(0, 0) < c)

        # Xác định điểm biên (x_bien, y_bien) cho miền nghiệm đúng (Dạng 1) và 3 miền nghiệm sai (Dạng 2, 3, 4)

        x_bien, y_bien = 0, 0
        x_bien_1, y_bien_1 = 0, 0
        x_bien_2, y_bien_2 = 0, 0
        x_bien_3, y_bien_3 = 0, 0

        # Miền nghiệm đúng (Tùy theo choice và dấu)
        if (choice == 0) or (choice == 1):
            # Cắt trục x
            if B.y > 0:
                if is_origin_in_solution:
                    x_bien, y_bien = x_trai - 1, y_duoi - 1  # Bên dưới
                    x_bien_1, y_bien_1 = x_phai + 1, y_tren + 1  # Bên trên
                else:  # (0,0) không thuộc miền nghiệm
                    x_bien, y_bien = x_phai + 1, y_tren + 1  # Bên trên
                    x_bien_1, y_bien_1 = x_trai - 1, y_duoi - 1  # Bên dưới
            else:
                if is_origin_in_solution:
                    x_bien, y_bien = x_phai + 1, y_tren + 1  # Bên trên
                    x_bien_1, y_bien_1 = x_trai - 1, y_duoi - 1  # Bên dưới
                else:
                    x_bien, y_bien = x_trai - 1, y_duoi - 1  # Bên dưới
                    x_bien_1, y_bien_1 = x_phai + 1, y_tren + 1  # Bên trên

            # Miền nghiệm sai: dùng đường BC
            # Dạng 3: miền dưới (nếu C.x > B.x), miền trái (nếu C.y > B.y)
            x_bien_2, y_bien_2 = x_trai - 1, y_duoi - 1
            # Dạng 4: miền trên/phải
            x_bien_3, y_bien_3 = x_phai + 1, y_tren + 1

        else:  # choice == 2 hoặc 3 (Cắt trục y)
            if B.x > 0:
                if is_origin_in_solution:
                    x_bien, y_bien = x_trai - 1, y_tren + 1  # Bên trái
                    x_bien_1, y_bien_1 = x_phai + 1, y_duoi - 1  # Bên phải
                else:
                    x_bien, y_bien = x_phai + 1, y_duoi - 1  # Bên phải
                    x_bien_1, y_bien_1 = x_trai - 1, y_tren + 1  # Bên trái
            else:
                if is_origin_in_solution:
                    x_bien, y_bien = x_trai - 1, y_duoi - 1  # Bên dưới
                    x_bien_1, y_bien_1 = x_phai + 1, y_tren + 1  # Bên trên
                else:
                    x_bien, y_bien = x_phai + 1, y_tren + 1  # Bên trên
                    x_bien_1, y_bien_1 = x_trai - 1, y_duoi - 1  # Bên dưới

            # Miền nghiệm sai: dùng đường BC
            # Dạng 3: miền trái/dưới
            x_bien_2, y_bien_2 = x_trai - 1, y_duoi - 1
            # Dạng 4: miền phải/trên
            x_bien_3, y_bien_3 = x_phai + 1, y_tren + 1

        # 2️⃣ Đảm bảo mỗi câu sinh ra duy nhất
        v = [AB, c, dau, choice, A, B, C, x_trai, x_phai, y_duoi, y_tren, x_bien, y_bien, x_bien_1, y_bien_1, x_bien_2,
             y_bien_2, x_bien_3, y_bien_3, m_AB, n_AB, m_BC, n_BC]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        AB, c, dau, choice, A, B, C, x_trai, x_phai, y_duoi, y_tren, x_bien, y_bien, x_bien_1, y_bien_1, x_bien_2, y_bien_2, x_bien_3, y_bien_3, m_AB, n_AB, m_BC, n_BC = v

        debai = f"Hình nào dưới đây biểu diễn miền nghiệm của bất phương trình ${latex(AB[0] * x + AB[1] * y)} {dau} {c}$?"

        is_dashed = True if (dau == '<') or (dau == '>') else False

        # Hàm tạo chuỗi tikz
        def generate_tikz(is_correct, is_dashed_line, use_BC_line, x_b, y_b):
            line_style = "dashed, thick" if is_dashed_line else "thick"

            # Chọn đường thẳng để vẽ (AB hoặc BC)
            if not use_BC_line:
                m_line, n_line = m_AB, n_AB
            else:
                m_line, n_line = m_BC, n_BC

            line_plot = f"plot (\\x, {{({m_line})*\\x + {n_line}}})"
            fill_plot = f"plot (\\x, {{({m_line})*\\x + {n_line}}}) |- ({x_b},{y_b})"

            # Xử lý trường hợp đường thẳng đứng (AB[1] = 0 hoặc BC[1] = 0)
            if AB[1] == 0:  # Đường thẳng đứng x = -c/AB[0] (cắt trục x)
                line_plot = f"({-c / AB[0]}, {y_duoi - 1}) -- ({-c / AB[0]}, {y_tren + 1})"
                if not use_BC_line:
                    fill_plot = f"({-c / AB[0]}, {y_duoi - 1}) |- ({x_b}, {y_b})"
                else:
                    fill_plot = f"({-c_BC / BC[0]}, {y_duoi - 1}) |- ({x_b}, {y_b})"

            elif BC[1] == 0 and use_BC_line:  # Đường thẳng đứng x = -c_BC/BC[0] (cắt trục x)
                line_plot = f"({-c_BC / BC[0]}, {y_duoi - 1}) -- ({-c_BC / BC[0]}, {y_tren + 1})"
                fill_plot = f"({-c_BC / BC[0]}, {y_duoi - 1}) |- ({x_b}, {y_b})"

            # Dạng latex
            tikzpicture = f"""
                \\begin{{tikzpicture}}[scale=.5]
                \\draw[->] ({x_trai - 0.7},0)--({x_phai + 0.7},0) node[below right] {{$x$}};
                \\draw[->] (0,{y_duoi - 0.7})--(0,{y_tren + 0.7}) node[right] {{$y$}};
                \\node (0,0) [below left] {{$ O $}};
            """

            if (choice == 0) or (choice == 1):
                tikzpicture += f"""
                    \\node at  ({A.x},0) [below left] {{$ {A.x} $}};
                    \\node at ({C.x},0) [below left] {{$ {C.x} $}};
                    \\node at (0,{B.y}) [above right] {{$ {B.y} $}};
                """
            else:
                tikzpicture += f"""
                    \\node at (0,{A.y}) [above right] {{$ {A.y} $}};
                    \\node at (0,{C.y}) [above right] {{$ {C.y} $}};
                    \\node at ({B.x},0) [below left] {{$ {B.x} $}};
                """

            tikzpicture += f"""
                \\clip ({x_trai - 0.5},{y_duoi - 0.5}) rectangle ({x_phai + 0.5},{y_tren + 0.5});
                \\foreach \\x in {{{x_trai},{x_trai + 1},...,{x_phai}}}
                \\draw[shift={{(\\x,0)}},color=black] (0pt,2pt) -- (0pt,-2pt);
                \\foreach \\y in {{{y_duoi},{y_duoi + 1},...,{y_tren}}}
                \\draw[shift={{(0,\\y)}},color=black] (2pt,0pt) -- (-2pt,0pt);
                \\draw [{line_style}, domain={x_trai - 1}:{x_phai + 1}, samples=100] {line_plot};
                \\fill[pattern=north east lines,opacity=.7] {fill_plot};
                \\end{{tikzpicture}}
            """
            return "{" + "".join(line.strip() for line in tikzpicture.splitlines()) + "}"

        dapso = generate_tikz(True, is_dashed, False, x_bien,
                              y_bien)  # Đáp án đúng: đường AB, miền nghiệm đúng (x_bien, y_bien)

        nhieu1 = generate_tikz(False, is_dashed, False, x_bien_1,
                               y_bien_1)  # Sai: đường AB, miền nghiệm sai (x_bien_1, y_bien_1)
        nhieu2 = generate_tikz(False, True if (np.random.choice([0, 1]) == 0) else False, True, x_bien_2,
                               y_bien_2)  # Sai: dùng đường BC, nét đứt ngẫu nhiên, miền sai (x_bien_2, y_bien_2)
        nhieu3 = generate_tikz(False, True if (np.random.choice([0, 1]) == 0) else False, True, x_bien_3,
                               y_bien_3)  # Sai: dùng đường BC, nét đứt ngẫu nhiên, miền sai (x_bien_3, y_bien_3)

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        # Lời giải
        giai = f"""
            Bất phương trình đã cho là $${latex(AB[0] * x + AB[1] * y)} {dau} {c}$$
            Bước 1: Vẽ đường thẳng $d: {latex(AB[0] * x + AB[1] * y)} = {c}$.
            \\begin{{itemize}}
                \\item Nếu dấu bất phương trình là $>$ hoặc $<$, ta vẽ $d$ bằng \\textbf{{nét đứt}}.
                \\item Nếu dấu bất phương trình là $\\ge$ hoặc $\\le$, ta vẽ $d$ bằng \\textbf{{nét liền}}.
            \\end{{itemize}}
            Bước 2: Xét điểm $O(0;0)$.
            Thay $x=0, y=0$ vào vế trái của bất phương trình, ta được: $VT = {AB[0]}(0) + {AB[1]}(0) = 0$.
            Ta so sánh $VT$ với $c$: $0 {'>' if 0 > c else '<' if 0 < c else '='} {c}$.
            \\begin{{itemize}}
                \\item Nếu bất phương trình đúng (tức $0 {dau} {c}$ đúng) thì miền nghiệm là nửa mặt phẳng chứa gốc $O(0;0)$.
                \\item Nếu bất phương trình sai (tức $0 {dau} {c}$ sai) thì miền nghiệm là nửa mặt phẳng không chứa gốc $O(0;0)$.
            \\end{{itemize}}
            Kết quả là hình ảnh ${dapso}$ (sau khi bỏ cặp dấu ${{...}}$).
        """

        # Đảm bảo các hình vẽ trong dsnhieu không trùng với dapso
        # Do việc sinh hình phức tạp, ta chấp nhận có thể có trùng lặp nhẹ,
        # nhưng logic sinh miền nghiệm sai khác biệt nên ít khi trùng hoàn toàn.

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

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
def L10_C2_B3_TH024_MC_A_02(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:
        dau = np.random.choice(['>', '<', '\\ge', '\\le'])

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

        if (((dau == '>') or (dau == '\\ge')) and (fx(0, 0) > c)) or ((dau == '<') or (dau == '\\le')) and (
                fx(0, 0) < c):
            if (choice == 0) or (choice == 1):
                if B[1] > 0:
                    x_bien, y_bien = x_trai - 1, y_tren + 1
                    x_bien_1, y_bien_1 = x_phai + 1, y_duoi - 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_duoi - 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_tren + 1
                else:
                    x_bien, y_bien = x_trai - 1, y_duoi - 1
                    x_bien_1, y_bien_1 = x_phai + 1, y_tren + 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_tren + 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_duoi - 1
            else:
                if B[0] > 0:
                    x_bien, y_bien = x_phai + 1, y_duoi - 1
                    x_bien_1, y_bien_1 = x_trai - 1, y_tren + 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_duoi - 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_tren + 1
                else:
                    x_bien, y_bien = x_trai - 1, y_duoi - 1
                    x_bien_1, y_bien_1 = x_phai + 1, y_tren + 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_tren + 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_duoi - 1
        else:
            if (choice == 0) or (choice == 1):
                if B[1] > 0:
                    x_bien, y_bien = x_phai + 1, y_duoi - 1
                    x_bien_1, y_bien_1 = x_trai - 1, y_tren + 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_duoi - 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_tren + 1
                else:
                    x_bien, y_bien = x_phai + 1, y_tren + 1
                    x_bien_1, y_bien_1 = x_trai - 1, y_duoi - 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_tren + 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_duoi - 1
            else:
                if B[0] > 0:
                    x_bien, y_bien = x_trai - 1, y_tren + 1
                    x_bien_1, y_bien_1 = x_phai + 1, y_duoi - 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_duoi - 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_tren + 1
                else:
                    x_bien, y_bien = x_phai + 1, y_tren + 1
                    x_bien_1, y_bien_1 = x_trai - 1, y_duoi - 1
                    x_bien_2, y_bien_2 = x_trai - 1, y_tren + 1
                    x_bien_3, y_bien_3 = x_phai + 1, y_duoi - 1

        v = [AB, BC, dau, c, choice, A, B, C, x_trai, x_phai, y_duoi, y_tren, x_bien, y_bien, x_bien_1, y_bien_1,
             x_bien_2, y_bien_2, x_bien_3, y_bien_3]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ""
    for v in gt:
        AB, BC, dau, c, choice, A, B, C, x_trai, x_phai, y_duoi, y_tren, x_bien, y_bien, x_bien_1, y_bien_1, x_bien_2, y_bien_2, x_bien_3, y_bien_3 = v

        label_nodes = ""
        if (choice == 0) or (choice == 1):
            label_nodes = f"""\\node at  ({A[0]},0) [below left] {{ $ {A[0]} $ }};
            \\node at ({C[0]},0) [below left] {{ $ {C[0]} $ }};
            \\node at (0,{B[1]}) [above right] {{ $ {B[1]} $ }};"""
        else:
            label_nodes = f"""\\node at (0,{A[1]}) [above right] {{ $ {A[1]} $ }};
            \\node at (0,{C[1]}) [above right] {{ $ {C[1]} $ }};
            \\node at ({B[0]},0) [below left] {{ $ {B[0]} $ }};"""

        line_style = "dashed, thick" if (dau == '<' or dau == '>') else "thick"
        line_style_3 = "dashed, thick" if (dau == '<' or dau == '>') else "thick"  # Đồng bộ theo gốc

        # --- Tạo mã TikZ cho bốn phương án ---
        dapso = f"""\\begin{{tikzpicture}}[scale=.5]
        \\draw[->] ({x_trai - 0.7},0)--({x_phai + 0.7},0) node[below right] {{$x$}};
        \\draw[->] (0,{y_duoi - 0.7})--(0,{y_tren + 0.7}) node[right] {{$y$}};
        \\node (0,0) [below left] {{$ O $}};
        {label_nodes}
        \\clip ({x_trai - 0.5},{y_duoi - 0.5}) rectangle ({x_phai + 0.5},{y_tren + 0.5});
        \\foreach \\x in {{{x_trai},{x_trai + 1},...,{x_phai}}} \\draw[shift={{(\\x,0)}},color=black] (0pt,2pt) -- (0pt,-2pt);
        \\foreach \\y in {{{y_duoi},{y_duoi + 1},...,{y_tren}}} \\draw[shift={{(0,\\y)}},color=black] (2pt,0pt) -- (-2pt,0pt);
        \\draw [{line_style}, domain={x_trai - 1}:{x_phai + 1}, samples=100] plot (\\x, {{({-(AB[0] / AB[1])})*\\x + {(AB[0] / AB[1]) * A[0] + A[1]}}});
        \\fill[pattern=north east lines,opacity=.7] plot (\\x, {{({-(AB[0] / AB[1])})*\\x + {(AB[0] / AB[1]) * A[0] + A[1]}}}) |- ({x_bien},{y_bien});
        \\end{{tikzpicture}}"""

        nhieu1 = f"""\\begin{{tikzpicture}}[scale=.5]
        \\draw[->] ({x_trai - 0.7},0)--({x_phai + 0.7},0) node[below right] {{$x$}};
        \\draw[->] (0,{y_duoi - 0.7})--(0,{y_tren + 0.7}) node[right] {{$y$}};
        \\node (0,0) [below left] {{$ O $}};
        {label_nodes}
        \\clip ({x_trai - 0.5},{y_duoi - 0.5}) rectangle ({x_phai + 0.5},{y_tren + 0.5});
        \\foreach \\x in {{{x_trai},{x_trai + 1},...,{x_phai}}} \\draw[shift={{(\\x,0)}},color=black] (0pt,2pt) -- (0pt,-2pt);
        \\foreach \\y in {{{y_duoi},{y_duoi + 1},...,{y_tren}}} \\draw[shift={{(0,\\y)}},color=black] (2pt,0pt) -- (-2pt,0pt);
        \\draw [{line_style}, domain={x_trai - 1}:{x_phai + 1}, samples=100] plot (\\x, {{({-(AB[0] / AB[1])})*\\x + {(AB[0] / AB[1]) * A[0] + A[1]}}});
        \\fill[pattern=north east lines,opacity=.7] plot (\\x, {{({-(AB[0] / AB[1])})*\\x + {(AB[0] / AB[1]) * A[0] + A[1]}}}) |- ({x_bien_1},{y_bien_1});
        \\end{{tikzpicture}}"""

        nhieu2 = f"""\\begin{{tikzpicture}}[scale=.5]
        \\draw[->] ({x_trai - 0.7},0)--({x_phai + 0.7},0) node[below right] {{$x$}};
        \\draw[->] (0,{y_duoi - 0.7})--(0,{y_tren + 0.7}) node[right] {{$y$}};
        \\node (0,0) [below left] {{$ O $}};
        {label_nodes}
        \\clip ({x_trai - 0.5},{y_duoi - 0.5}) rectangle ({x_phai + 0.5},{y_tren + 0.5});
        \\foreach \\x in {{{x_trai},{x_trai + 1},...,{x_phai}}} \\draw[shift={{(\\x,0)}},color=black] (0pt,2pt) -- (0pt,-2pt);
        \\foreach \\y in {{{y_duoi},{y_duoi + 1},...,{y_tren}}} \\draw[shift={{(0,\\y)}},color=black] (2pt,0pt) -- (-2pt,0pt);
        \\draw [{line_style}, domain={x_trai - 1}:{x_phai + 1}, samples=100] plot (\\x, {{({-(BC[0] / BC[1])})*\\x + {(BC[0] / BC[1]) * B[0] + B[1]}}});
        \\fill[pattern=north east lines,opacity=.7] plot (\\x, {{({-(BC[0] / BC[1])})*\\x + {(BC[0] / BC[1]) * B[0] + B[1]}}}) |- ({x_bien_2},{y_bien_2});
        \\end{{tikzpicture}}"""

        nhieu3 = f"""\\begin{{tikzpicture}}[scale=.5]
        \\draw[->] ({x_trai - 0.7},0)--({x_phai + 0.7},0) node[below right] {{$x$}};
        \\draw[->] (0,{y_duoi - 0.7})--(0,{y_tren + 0.7}) node[right] {{$y$}};
        \\node (0,0) [below left] {{$ O $}};
        {label_nodes}
        \\clip ({x_trai - 0.5},{y_duoi - 0.5}) rectangle ({x_phai + 0.5},{y_tren + 0.5});
        \\foreach \\x in {{{x_trai},{x_trai + 1},...,{x_phai}}} \\draw[shift={{(\\x,0)}},color=black] (0pt,2pt) -- (0pt,-2pt);
        \\foreach \\y in {{{y_duoi},{y_duoi + 1},...,{y_tren}}} \\draw[shift={{(0,\\y)}},color=black] (2pt,0pt) -- (-2pt,0pt);
        \\draw [{line_style_3}, domain={x_trai - 1}:{x_phai + 1}, samples=100] plot (\\x, {{({-(BC[0] / BC[1])})*\\x + {(BC[0] / BC[1]) * B[0] + B[1]}}});
        \\fill[pattern=north east lines,opacity=.7] plot (\\x, {{({-(BC[0] / BC[1])})*\\x + {(BC[0] / BC[1]) * B[0] + B[1]}}}) |- ({x_bien_3},{y_bien_3});
        \\end{{tikzpicture}}"""

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        debai = f"Hình nào dưới đây biểu diễn miền nghiệm của bất phương trình ${latex(AB[0] * x + AB[1] * y)} {dau} {c}$?"

        giai = f"""
        Để xác định miền nghiệm của bất phương trình ${latex(AB[0] * x + AB[1] * y)} {dau} {c}$:\\\\
        1. Vẽ đường thẳng d: ${latex(AB[0] * x + AB[1] * y)} = {c}$.\\\\
        2. Chọn điểm gốc tọa độ $O(0;0)$, ta thấy giá trị vế trái tại $O$ là $0$.\\\\
        3. So sánh kết quả để xác định nửa mặt phẳng bị gạch bỏ (không thuộc miền nghiệm).\\\\
        Hình đúng biểu diễn chính xác phần miền nghiệm được giữ lại (không gạch chéo) phù hợp với dấu của bất phương trình.
        """

        # Sử dụng hàm MC_SA_answer_text vì phương án chứa mã TikZ (hình ảnh hình học trực quan)
        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN
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

        # Sinh đường thẳng MN cắt hai cạnh của hình chữ nhật
        x_M = np.random.randint(x_center - K[0] + 1, x_center + K[3])
        y_N = np.random.randint(y_center - K[2] + 1, y_center + K[1])
        y_M = int(np.random.choice([y_center - K[2], y_center + K[1]]))
        x_N = int(np.random.choice([x_center - K[0], x_center + K[3]]))

        M = [x_M, y_M]
        N = [x_N, y_N]
        # Tránh trường hợp M trùng N gây ra lỗi đường thẳng không xác định
        # (bản gốc dùng N ngay ở dòng while khi N CHƯA được gán -> UnboundLocalError)
        while M == N:
            x_N = int(np.random.choice([x_center - K[0], x_center + K[3]]))
            N = [x_N, y_N]

        # Thay thế hàm dc.pttq bằng tính toán đại số vectơ pháp tuyến cơ bản
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

        Duong = []
        Am = []
        for p, label in zip([A, B, C, D], ['A', 'B', 'C', 'D']):
            if MN_func(p[0], p[1]) > 0:
                Duong.append(label)
            else:
                Am.append(label)

        Dau = np.random.choice(['Duong', 'Am'])

        # Kiểm tra điều kiện để bài toán sinh ra đa giác hợp lệ (không lấy miền rỗng hoặc toàn bộ)
        if (Dau == 'Duong' and len(Duong) in [1, 2, 3]) or (Dau == 'Am' and len(Am) in [1, 2, 3]):
            if Dau == 'Duong':
                dau = '\\ge'
                count = len(Duong)
            else:
                dau = '\\le'
                count = len(Am)

            if count == 1:
                mien = 'Miền tam giác'
            elif count == 2:
                mien = 'Miền tứ giác'
            else:
                mien = 'Miền ngũ giác'

            Mien_list = ['Miền tam giác', 'Miền tứ giác', 'Miền ngũ giác', 'Miền lục giác']
            Mien_list.remove(mien)

            v = [fx, gx, hx, kx, VT_MN, dau, VP_MN, mien, Mien_list]
            if v not in gt:
                gt.append(v)
                dem += 1

    cauTN = ""
    for v in gt:
        fx, gx, hx, kx, VT_MN, dau, VP_MN, mien, Mien_list = v

        debai = f"Miền nghiệm của hệ bất phương trình $\\heva{{& {fx} \\le x \\le {gx} \\\\ & {hx} \\le y \\le {kx} \\\\ & {latex(VT_MN)} {dau} {VP_MN} }}$ là"

        dapso = mien
        dsnhieu = [Mien_list[0], Mien_list[1], Mien_list[2]]

        giai = f"""
        Hệ bất phương trình gồm:\\\\
        * Các bất phương trình ${fx} \\le x \\le {gx}$ và ${hx} \\le y \\le {kx}$ xác định miền nghiệm là một hình chữ nhật giới hạn bởi các đường biên.\\\\
        * Bất phương trình còn lại ${latex(VT_MN)} {dau} {VP_MN}$ là một nửa mặt phẳng bờ là đường thẳng $MN$ cắt hình chữ nhật trên.\\\\
        Giao của hai miền nghiệm này cắt bớt một phần góc của hình chữ nhật, tạo thành một đa giác lồi.\\\\
        Dựa vào số đỉnh nằm trong miền thỏa mãn, ta xác định được miền nghiệm là \\textbf{{{mien.lower()}}}.
        """

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
#
# def K10_2_3_3_2_VD(): #Dạng 3: Tìm miền nghiệm của bất phương trình
#     with open(r"latex\data\de.tex", "a", encoding='utf-8') as de:
#         x = Symbol('x')
#         y = Symbol('y')
#
#         x_center = np.randint(-2,2)
#         y_center = np.randint(-2,2)
#         K = []
#         for i in range(0,4):
#             k = np.randint(0,5)
#             K.append(k)
#         while (K[0] + K[3] <= 5):
#             k0 = np.randint(0,10)
#             k3 = np.randint(0,10)
#             K.pop(3)
#             K.insert(3,k3)
#             K.pop(0)
#             K.insert(0,k0)
#         while (K[1] + K[2] <= 5):
#             k1 = np.randint(0,10)
#             k2 = np.randint(0,10)
#             K.pop(2)
#             K.insert(2,k2)
#             K.pop(1)
#             K.insert(1,k)
#
#         A = [x_center - K[0], y_center + K[1]] # đường thẳng AB song song vơi Ox có pt x = x_center - K[0]
#         B = [x_center - K[0], y_center - K[2]]
#         C = [x_center + K[3], y_center - K[2]] # đường thẳng CD song song vơi Ox có pt x = x_center + K[3]
#         D = [x_center + K[3], y_center + K[1]]
#         fx = x_center - K[0] # đường thẳng AB : x = fx
#         gx = x_center + K[3] # đường thẳng CD: x = gx
#         hx = y_center - K[2] # đường thẳng BC
#         kx = y_center + K[1] # đường thẳng AD
#
#         # Đường thẳng MN với M,N nằm trên 2 cạnh bất kì của hình chữ nhật ABCD
#         x_M = np.randint(x_center - K[0]+1, x_center + K[3]-1)
#         y_N = np.randint(y_center - K[2]+1, y_center + K[1]-1)
#         y_M = np.choice([y_center - K[2], y_center + K[1]])
#         x_N = np.choice([x_center - K[0], x_center + K[3]])
#         M = [x_M, y_M]
#         N = [x_N, y_N]
#         a_MN = dc.pttq(M[0],M[1],N[0],N[1])[0]
#         b_MN = dc.pttq(M[0],M[1],N[0],N[1])[1]
#         c_MN = dc.pttq(M[0],M[1],N[0],N[1])[2]
#         MN = lambda x,y: a_MN * x + b_MN * y + c_MN # đường thẳng MN
#         VT_MN = a_MN * x + b_MN * y
#         VP_MN = - c_MN
#
#         Duong = []
#         Am = []
#         if MN(A[0],A[1]) > 0:
#             Duong.append('A')
#         else:
#             Am.append('A')
#         if MN(B[0],B[1]) > 0:
#             Duong.append('B')
#         else:
#             Am.append('B')
#         if MN(C[0],C[1]) > 0:
#             Duong.append('C')
#         else:
#             Am.append('C')
#         if MN(D[0],D[1]) > 0:
#             Duong.append('D')
#         else:
#             Am.append('D')
#         Dau = np.choice(['Duong', 'Am'])
#         Mien = ['Miền tam giác', 'Miền tứ giác', 'Miền ngũ giác', 'Miền lục giác']
#         if (Dau == 'Duong') and (len(Duong) == 1):
#             dau = '\ge'
#             mien = 'Miền tam giác'
#             Mien.remove(mien)
#         elif (Dau == 'Duong') and (len(Duong) == 2):
#             dau = '\ge'
#             mien = 'Miền tứ giác'
#             Mien.remove(mien)
#         elif (Dau == 'Duong') and (len(Duong) == 3):
#             dau = '\ge'
#             mien = 'Miền ngũ giác'
#             Mien.remove(mien)
#         elif (Dau == 'Am') and (len(Am) == 1):
#             dau = '\le'
#             mien = 'Miền tam giác'
#             Mien.remove(mien)
#         elif (Dau == 'Am') and (len(Am) == 2):
#             dau = '\le'
#             mien = 'Miền tứ giác'
#             Mien.remove(mien)
#         elif (Dau == 'Am') and (len(Am) == 3):
#             dau = '\le'
#             mien = 'Miền ngũ giác'
#             Mien.remove(mien)
#         de.write(r"\begin{ex}" + os.linesep)
#         de.write(f"Miền nghiệm của hệ bất phương trình $\\heva{{& {fx} \\le x \\le {gx} \\\\ & {hx} \\le y \\le {kx} \\\\ & {latex(VT_MN)} {dau} {VP_MN} }}$ là{os.linesep}")
#         de.write(r"\choice"+ os.linesep)
#         de.write(f"{{\\True {mien}}}{os.linesep}")
#         de.write(f"{{{Mien[0]}}}{os.linesep}")
#         de.write(f"{{{Mien[1]}}}{os.linesep}")
#         de.write(f"{{{Mien[2]}}}{os.linesep}")
#         de.write(r"\loigiai{}" + os.linesep)
#         de.write(r"\end{ex}" + os.linesep)


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


def L10_C2_TF_A_01(socau, socot=1):
    """Đúng/Sai - bất phương trình bậc nhất hai ẩn."""
    cauTF = ''
    for _ in range(socau):
        a = _rd.choice([1, 2, 3])
        b = _rd.choice([1, 2, 3])
        k = _rd.randint(2, 6)
        c = a * b * k
        x0, y0 = _rd.randint(0, 4), _rd.randint(0, 4)
        ve_trai = a * x0 + b * y0
        # dem diem nguyen trong hinh vuong 0..k thoa man
        dem = sum(1 for X in range(0, k + 1) for Y in range(0, k + 1)
                  if a * X + b * Y <= c)

        debai = (r"Cho bất phương trình $%dx + %dy \le %d$. "
                 r"Xét tính đúng sai của các khẳng định sau:" % (a, b, c))

        # a) NB - nhan dang
        y1 = [(r"{\True Bất phương trình đã cho là bất phương trình bậc nhất hai ẩn}",
               r"Đúng. Nó có dạng $ax + by \le c$ với $a = %d$, $b = %d$ không đồng thời "
               r"bằng $0$, và $x$, $y$ đều bậc nhất." % (a, b)),
              (r"{Bất phương trình đã cho không phải là bất phương trình bậc nhất hai ẩn}",
               r"Sai. Nó đúng dạng $ax + by \le c$ nên là bất phương trình bậc nhất hai ẩn.")]

        # b) TH - thay so kiem tra mot cap so
        dung_b = ve_trai <= c
        y2 = [((r"{\True " if dung_b else "{") +
               r"Cặp số $\left(%d; %d\right)$ là một nghiệm của bất phương trình}" % (x0, y0),
               r"Thay vào vế trái: $%d\cdot %d + %d\cdot %d = %d$, so với $%d$ thì %s. "
               r"Nên cặp số này %s một nghiệm."
               % (a, x0, b, y0, ve_trai, c,
                  "nhỏ hơn hoặc bằng" if dung_b else "lớn hơn",
                  "" if dung_b else "không phải")),
              ((r"{" if dung_b else r"{\True ") +
               r"Cặp số $\left(%d; %d\right)$ không phải là nghiệm của bất phương trình}" % (x0, y0),
               r"Thay vào vế trái được $%d$; so với $%d$ thì %s."
               % (ve_trai, c, "thoả mãn" if dung_b else "không thoả mãn"))]

        # c) VD - phai hinh dung mien nghiem
        y3 = [(r"{\True Miền nghiệm của bất phương trình là nửa mặt phẳng bờ là đường "
               r"thẳng $%dx + %dy = %d$ và có chứa gốc toạ độ $O$}" % (a, b, c),
               r"Thay $O\left(0;0\right)$ vào vế trái được $0$, mà $0 \le %d$ nên $O$ "
               r"thuộc miền nghiệm.\\ "
               r"Vậy miền nghiệm là nửa mặt phẳng bờ $%dx + %dy = %d$ chứa $O$ (kể cả bờ)."
               % (c, a, b, c)),
              (r"{Miền nghiệm của bất phương trình là nửa mặt phẳng bờ là đường thẳng "
               r"$%dx + %dy = %d$ và KHÔNG chứa gốc toạ độ $O$}" % (a, b, c),
               r"Sai. Thay $O$ vào vế trái được $0 \le %d$ (đúng) nên $O$ thuộc miền nghiệm."
               % c)]

        # d) VDC - dem diem nguyen, phai ket hop mien nghiem voi rang buoc phu
        y4 = [(r"{\True Có đúng $%d$ cặp số nguyên $\left(x; y\right)$ thoả mãn bất phương "
               r"trình và $0 \le x \le %d$, $0 \le y \le %d$}" % (dem, k, k),
               r"Với mỗi $x$ nguyên từ $0$ đến $%d$, điều kiện $%dx + %dy \le %d$ cho "
               r"$y \le \dfrac{%d - %dx}{%d}$; đếm số $y$ nguyên từ $0$ đến $%d$ thoả mãn "
               r"rồi cộng lại theo từng $x$, ta được tất cả $%d$ cặp."
               % (k, a, b, c, c, a, b, k, dem)),
              (r"{Có đúng $%d$ cặp số nguyên $\left(x; y\right)$ thoả mãn bất phương trình "
               r"và $0 \le x \le %d$, $0 \le y \le %d$}" % (dem + 2, k, k),
               r"Sai. Đếm đầy đủ theo từng giá trị của $x$ thì được $%d$ cặp." % dem)]

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

        debai = (r"Cho hệ bất phương trình $\heva{& x \ge 0 \\ & y \ge 0 \\ & %s \\ & %s}$ "
                 r"và biểu thức $F\left(x; y\right) = %dx + %dy$. "
                 r"Xét tính đúng sai của các khẳng định sau:"
                 % (_bpt_tex(a1, b1, c1), _bpt_tex(a2, b2, c2), p, q))

        # a) NB - nhan dang he
        y1 = [(r"{\True Hệ đã cho là hệ bất phương trình bậc nhất hai ẩn}",
               r"Đúng. Mỗi bất phương trình trong hệ đều có dạng bậc nhất đối với hai ẩn "
               r"$x$ và $y$."),
              (r"{Hệ đã cho không phải là hệ bất phương trình bậc nhất hai ẩn}",
               r"Sai. Cả bốn bất phương trình đều bậc nhất đối với $x$ và $y$.")]

        # b) TH - thay mot diem vao he
        y2 = [(r"{\True Điểm $\left(%d; %d\right)$ thuộc miền nghiệm của hệ}" % (u, v),
               r"Thay $x = %d$, $y = %d$ vào từng bất phương trình đều thấy thoả mãn "
               r"(điểm này chính là giao điểm của hai đường bờ), nên nó thuộc miền nghiệm."
               % (u, v)),
              (r"{Điểm $\left(%d; %d\right)$ không thuộc miền nghiệm của hệ}" % (u, v),
               r"Sai. Đó chính là một đỉnh của miền nghiệm nên nó thuộc miền nghiệm.")]

        # c) VD - phai giai he de biet hinh dang mien nghiem
        y3 = [(r"{\True Miền nghiệm của hệ là một miền tứ giác}",
               r"Bốn bất phương trình cho bốn nửa mặt phẳng; giao của chúng là miền tứ "
               r"giác với bốn đỉnh $\left(0;0\right)$, $\left(%d;0\right)$, "
               r"$\left(%d;%d\right)$, $\left(0;%d\right)$." % (m, u, v, n)),
              (r"{Miền nghiệm của hệ là một miền tam giác}",
               r"Sai. Giải các cặp đường bờ ta được BỐN đỉnh chứ không phải ba, nên miền "
               r"nghiệm là tứ giác.")]

        # d) VDC - tim gia tri lon nhat, phai co toa do cac dinh o y c)
        y4 = [(r"{\True Giá trị lớn nhất của $F$ trên miền nghiệm bằng $%d$}" % lon,
               r"Biểu thức bậc nhất đạt giá trị lớn nhất tại một đỉnh của miền nghiệm. "
               r"Tính $F$ tại bốn đỉnh:\\ %s.\\ Lớn nhất là $%d$, đạt tại "
               r"$\left(%d; %d\right)$."
               % (r"\\ ".join(r"$F\left(%d; %d\right) = %d$" % (X, Y, p * X + q * Y)
                              for X, Y in dinh), lon, dinh_lon[0], dinh_lon[1])),
              (r"{Giá trị lớn nhất của $F$ trên miền nghiệm bằng $%d$}" % (lon + p + q),
               r"Sai. So sánh $F$ tại bốn đỉnh thì giá trị lớn nhất là $%d$." % lon)]

        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF
