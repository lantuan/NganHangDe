# Import các hàm và lớp từ thư viện sympy để giải phương trình và thực hiện các phép tính toán khác.
from sympy import Symbol, solve, sqrt, factor, cancel, Poly, Eq, Function, exp, Abs, And
from sympy.abc import x, y, z, a, b
from sympy import init_printing, nroots
import numpy as np
import numpy
import random
import io
import os
import datetime  # Thư viện để lấy thời gian thực


import math
from math_type import *

import re

# ==========================================
# CHƯƠNG 1: MỆNH ĐỀ - TẬP HỢP
# ==========================================



def L10_C1_B1_NB001_MC_A_01(socau, dang=1):
    # Danh sách các mệnh đề (câu khẳng định có tính đúng hoặc sai)
    ds_menhde = [
        'Số 2025 là số chính phương',
        'Hình thoi có hai đường chéo vuông góc với nhau',
        'Tổng hai góc đối của một tứ giác nội tiếp bằng 180 độ',
        'Số 1 là số nguyên tố',
        'Hình chữ nhật là một hình bình hành có một góc vuông',
        'Số 0 là số tự nhiên nhỏ nhất',
        'Việt Nam nằm ở phía đông của bán đảo Đông Dương',
        'Sông Hồng là con sông dài nhất thế giới',
        'Chiến thắng Điện Biên Phủ diễn ra vào năm 1954',
        'Vua Quang Trung đại phá quân Thanh vào năm 1789',
        'Nước tinh khiết đóng băng ở 0 độ C',
        'Mặt Trời là một hành tinh trong Hệ Mặt Trời',
        'Oxy là nguyên tố chiếm tỉ lệ lớn nhất trong khí quyển Trái Đất',
    ]

    # Danh sách các câu không phải mệnh đề (câu hỏi, cảm thán, câu cầu khiến)
    ds_khongphai = [
        'Đại tá Phạm Ngọc Thảo là ai?',
        'Anh hùng lực lượng vũ trang nhân dân Nguyễn Văn Bảy đã bắn rơi bao nhiêu máy bay địch?',
        'Bác Hồ đã đi qua bao nhiêu quốc gia trong suốt hành trình 30 năm bôn ba tìm đường cứu nước?',
        'Ai yêu nhi đồng bằng bác Hồ Chí Minh?',
        'Cái răng, cái tóc là gốc con người, đúng không nào?',
        'Sống trong đời sống cần có một tấm lòng!',
        'Bài thi toán này dễ quá!',
        'Bạn bao nhiêu tuổi?',
        'Trời ơi, nóng quá!',
        'Hãy trật tự trong lớp học!'
    ]

    gt = []
    dem = 0

    while dem < socau:
        # Chọn câu hỏi: 0 - Tìm mệnh đề, 1 - Tìm câu không phải mệnh đề
        loai = random.choice([0, 1])

        if loai == 0:
            dapso = random.choice(ds_menhde)
            dsnhieu = random.sample(ds_khongphai, 3)
            debai = r"Trong các câu sau, câu nào là mệnh đề?"
            giai = r"Mệnh đề là câu khẳng định có tính đúng hoặc sai. Các câu hỏi, câu cảm thán, câu cầu khiến không phải là mệnh đề."
        else:
            dapso = random.choice(ds_khongphai)
            dsnhieu = random.sample(ds_menhde, 3)
            debai = r"Trong các câu sau, câu nào \textbf{không phải} là mệnh đề?"
            giai = r"Câu không phải mệnh đề thường là câu hỏi, câu cảm thán hoặc câu cầu khiến, không thể xác định tính đúng sai."

        if [dsnhieu, dapso, debai, giai] not in gt:
            gt.append([dsnhieu, dapso, debai, giai])
            dem += 1

    cauTN = ''
    for dsnhieu, dapso, debai, giai in gt:
        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


def L10_C1_B1_NB001_MC_B_01(socau, dang=1):

    # Danh sách các mệnh đề
    ds_menhde = [
        'Số 2025 là số chính phương.',
        'Hình thoi có hai đường chéo vuông góc với nhau.',
        'Tổng hai góc đối của một tứ giác nội tiếp bằng 180 độ.',
        'Số 1 là số nguyên tố.',
        'Hình chữ nhật là một hình bình hành có một góc vuông.',
        'Số 0 là số tự nhiên nhỏ nhất.',
        'Việt Nam nằm ở phía đông của bán đảo Đông Dương.',
        'Sông Hồng là con sông dài nhất thế giới.',
        'Chiến thắng Điện Biên Phủ diễn ra vào năm 1954.',
        'Vua Quang Trung đại phá quân Thanh vào năm 1789.',
        'Nước tinh khiết đóng băng ở 0 độ C.',
        'Mặt Trời là một hành tinh trong Hệ Mặt Trời.',
        'Oxy là nguyên tố chiếm tỉ lệ lớn nhất trong khí quyển Trái Đất.',
    ]

    # Danh sách các câu không phải mệnh đề
    ds_khongphai = [
        'Đại tá Phạm Ngọc Thảo là ai?',
        'Anh hùng lực lượng vũ trang nhân dân Nguyễn Văn Bảy đã bắn rơi bao nhiêu máy bay địch?',
        'Bác Hồ đã đi qua bao nhiêu quốc gia trong suốt hành trình 30 năm bôn ba tìm đường cứu nước?',
        'Ai yêu nhi đồng bằng bác Hồ Chí Minh?',
        'Cái răng, cái tóc là gốc con người, đúng không nào?',
        'Sống trong đời sống cần có một tấm lòng!',
        'Bài thi toán này dễ quá!',
        'Bạn bao nhiêu tuổi?',
        'Trời ơi, nóng quá!',
        'Hãy trật tự trong lớp học!'
    ]

    gt = []
    dem = 0

    while dem < socau:

        # Loại câu hỏi
        # 0: hỏi số mệnh đề
        # 1: hỏi số câu không phải mệnh đề
        loai = random.choice([0, 1])

        # Số đáp án đúng trong 4 câu
        dapso = random.randint(1, 4)

        # Các đáp án nhiễu
        dsnhieu = random.sample(
            [x for x in range(5) if x != dapso],
            3
        )

        if loai == 0:

            # Chọn các mệnh đề đúng
            list_dapso = random.sample(ds_menhde, dapso)

            # Chọn các câu không phải mệnh đề
            list_kp = random.sample(ds_khongphai, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_dapso + list_kp

            # Trộn vị trí
            random.shuffle(ds_cau)

            # Chuyển thành chuỗi LaTeX xuống dòng
            noi_dung = r"\\ ".join(
                [f"{i+1}. {cau}" for i, cau in enumerate(ds_cau)]
            )

            debai = (
                r"Trong các câu sau, có bao nhiêu câu là mệnh đề?\\ "
                + noi_dung
            )

            giai = (
                r"Mệnh đề là câu khẳng định có tính đúng hoặc sai. "
                r"Các câu hỏi, câu cảm thán, câu cầu khiến "
                r"không phải là mệnh đề."
            )

        else:

            # Chọn các câu không phải mệnh đề
            list_dapso = random.sample(ds_khongphai, dapso)

            # Chọn các mệnh đề
            list_kp = random.sample(ds_menhde, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_dapso + list_kp

            # Trộn vị trí
            random.shuffle(ds_cau)

            # Chuyển thành chuỗi LaTeX xuống dòng
            noi_dung = r"\\ ".join(
                [f"{i+1}. {cau}" for i, cau in enumerate(ds_cau)]
            )

            debai = (
                r"Trong các câu sau, có bao nhiêu câu "
                r"\textbf{không phải} là mệnh đề?\\ "
                + noi_dung
            )

            giai = (
                r"Câu không phải mệnh đề thường là câu hỏi, "
                r"câu cảm thán hoặc câu cầu khiến, "
                r"không thể xác định tính đúng sai."
            )

        # Tránh trùng đề
        if [dsnhieu, dapso, debai, giai] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN



def L10_C1_B1_TH003_MC_A_01(socau, dang=1):

    # Danh sách các mệnh đề đúng
    ds_dung = [
        r'Tam giác đều có ba cạnh bằng nhau',
        r'Tổng ba góc trong một tam giác bằng $180^{\circ}$',
        r'Hình chữ nhật có bốn góc vuông',
        r'Hình vuông là hình chữ nhật có bốn cạnh bằng nhau',
        r'Mọi số nguyên chẵn đều chia hết cho $2$',
        r'Số $0$ là số nguyên',
        r'Đường kính đi qua tâm của đường tròn',
        r'Hai đường thẳng song song không có điểm chung',
        r'Trong tam giác vuông, bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông',
        r'Hình thoi có hai đường chéo vuông góc với nhau',
        r'Mọi số nguyên tố lớn hơn $2$ đều là số lẻ',
        r'Hình bình hành có các cạnh đối song song',
        r'Số $25$ là số chính phương',
        r'Tập hợp rỗng được kí hiệu là $\varnothing$',
        r'Nếu một số chia hết cho $10$ thì số đó chia hết cho $5$',
        r'Góc bẹt có số đo bằng $180^{\circ}$',
        r'Hai góc đối đỉnh thì bằng nhau',
        r'Hình tròn có vô số trục đối xứng',
        r'Mọi hình vuông đều là hình thoi',
        r'Hình thang cân là hình thang có hai cạnh bên bằng nhau.',
        r'Số $\sqrt{16}$ bằng $4$'
    ]

    # Danh sách các mệnh đề sai
    ds_sai = [
        r'Hình vuông có tổng bốn góc trong bằng $180^{\circ}$',
        r'Hình thang có hai cạnh bên bằng nhau là hình thang cân',
        r'Mọi số nguyên đều là số nguyên tố',
        r'Tam giác có bốn cạnh',
        r'Hai đường thẳng song song thì cắt nhau',
        r'Số $9$ là số nguyên tố',
        r'Hình chữ nhật có bốn cạnh bằng nhau',
        r'Mọi số chẵn đều chia hết cho $3$',
        r'Góc vuông có số đo bằng $180^{\circ}$',
        r'Đường tròn có ba tâm',
        r'Số $1$ là số nguyên tố',
        r'Hình thang có hai cặp cạnh đối song song',
        r'Tam giác vuông có ba góc vuông',
        r'Số $15$ là số chính phương',
        r'Hai góc kề bù thì bằng nhau',
        r'Mọi hình bình hành đều là hình vuông',
        r'Mọi số tự nhiên đều là số âm',
        r'Số $\sqrt{25}$ bằng $10$',
        r'Đường kính nhỏ hơn bán kính'
    ]

    gt = []
    dem = 0

    while dem < socau:

        # 0: hỏi mệnh đề đúng
        # 1: hỏi mệnh đề sai
        loai = random.choice([0, 1])

        if loai == 0:

            # Đáp án đúng
            dapso = random.choice(ds_dung)

            # 3 đáp án nhiễu
            dsnhieu = random.sample(ds_sai, 3)

            debai = (
                r"Trong các mệnh đề sau, mệnh đề nào đúng?"
            )

            giai = (
                r"Mệnh đề đúng là: " + dapso + "."
            )

        else:

            # Đáp án đúng là mệnh đề sai
            dapso = random.choice(ds_sai)

            # 3 đáp án nhiễu là mệnh đề đúng
            dsnhieu = random.sample(ds_dung, 3)

            debai = (
                r"Trong các mệnh đề sau, mệnh đề nào \textbf{sai}?"
            )

            giai = (
                r"Mệnh đề sai là: " + dapso + "."
            )

        # Tránh trùng đề
        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += _MC_khong_cham(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B1_TH003_MC_B_01(socau, dang=1):

    # Danh sách các mệnh đề đúng
    ds_dung = [
        r'Tam giác đều có ba cạnh bằng nhau.',
        r'Tổng ba góc trong một tam giác bằng $180^{\circ}$.',
        r'Hình chữ nhật có bốn góc vuông.',
        r'Hình vuông là hình chữ nhật có bốn cạnh bằng nhau.',
        r'Mọi số nguyên chẵn đều chia hết cho $2$.',
        r'Số $0$ là số nguyên.',
        r'Đường kính đi qua tâm của đường tròn.',
        r'Hai đường thẳng song song không có điểm chung.',
        r'Trong tam giác vuông, bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông.',
        r'Hình thoi có hai đường chéo vuông góc với nhau.',
        r'Mọi số nguyên tố lớn hơn $2$ đều là số lẻ.',
        r'Hình bình hành có các cạnh đối song song.',
        r'Số $25$ là số chính phương.',
        r'Tập hợp rỗng được kí hiệu là $\varnothing$.',
        r'Nếu một số chia hết cho $10$ thì số đó chia hết cho $5$.',
        r'Góc bẹt có số đo bằng $180^{\circ}$.',
        r'Hai góc đối đỉnh thì bằng nhau.',
        r'Hình tròn có vô số trục đối xứng.',
        r'Mọi hình vuông đều là hình thoi.',
        r'Hình thang cân là hình thang có hai cạnh bên bằng nhau.',
        r'Số $\sqrt{16}$ bằng $4$.'
    ]

    # Danh sách các mệnh đề sai
    ds_sai = [
        r'Hình vuông có tổng bốn góc trong bằng $180^{\circ}$.',
        r'Hình thang có hai cạnh bên bằng nhau là hình thang cân.',
        r'Mọi số nguyên đều là số nguyên tố.',
        r'Tam giác có bốn cạnh.',
        r'Hai đường thẳng song song thì cắt nhau.',
        r'Số $9$ là số nguyên tố.',
        r'Hình chữ nhật có bốn cạnh bằng nhau.',
        r'Mọi số chẵn đều chia hết cho $3$.',
        r'Góc vuông có số đo bằng $180^{\circ}$.',
        r'Đường tròn có ba tâm.',
        r'Số $1$ là số nguyên tố.',
        r'Hình thang có hai cặp cạnh đối song song.',
        r'Tam giác vuông có ba góc vuông.',
        r'Số $15$ là số chính phương.',
        r'Hai góc kề bù thì bằng nhau.',
        r'Mọi hình bình hành đều là hình vuông.',
        r'Mọi số tự nhiên đều là số âm.',
        r'Số $\sqrt{25}$ bằng $10$.',
        r'Trong đường tròn, đường kính nhỏ hơn bán kính.'
    ]

    gt = []
    dem = 0

    while dem < socau:

        # 0: hỏi số mệnh đề đúng
        # 1: hỏi số mệnh đề sai
        loai = random.choice([0, 1])

        # Số lượng mệnh đề cần đếm
        dapso = random.randint(1, 4)

        if loai == 0:

            # Chọn các mệnh đề đúng
            list_dung = random.sample(ds_dung, dapso)

            # Chọn các mệnh đề sai
            list_sai = random.sample(ds_sai, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_dung + list_sai

            debai = (
                r"Trong các mệnh đề sau, có bao nhiêu mệnh đề đúng?"
            )

            giai = (
                r"Có " + str(dapso) + r" mệnh đề đúng."
            )

        else:

            # Chọn các mệnh đề sai
            list_sai = random.sample(ds_sai, dapso)

            # Chọn các mệnh đề đúng
            list_dung = random.sample(ds_dung, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_sai + list_dung

            debai = (
                r"Trong các mệnh đề sau, có bao nhiêu mệnh đề \textbf{sai}?"
            )

            giai = (
                r"Có " + str(dapso) + r" mệnh đề sai."
            )

        # Trộn vị trí các câu
        random.shuffle(ds_cau)

        # Ghép nội dung đề
        debai += r"\\ " + r"\\ ".join(
            [f"{i+1}. {cau}" for i, cau in enumerate(ds_cau)]
        )

        # Các đáp án nhiễu
        dsnhieu = random.sample(
            [x for x in range(5) if x != dapso],
            3
        )

        # Tránh trùng đề
        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN



def L10_C1_B1_TH003_TL_A_01(socau, dong=1):

    gt = []
    dem = len(gt)

    while dem < socau:

        a_val = np.random.randint(1, 16)

        loai_luong_tu = np.random.randint(0, 2)  # 0: forall, 1: exists
        loai_dau = np.random.randint(0, 4)       # >, >=, <, <=

        v = [a_val, loai_luong_tu, loai_dau]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''

    for v in gt:

        a_val, loai_luong_tu, loai_dau = v

        if loai_luong_tu == 0:
            luong_tu_tex = r"\forall x \in \mathbb{R}"
            luong_tu_text = "với mọi"
        else:
            luong_tu_tex = r"\exists x \in \mathbb{R}"
            luong_tu_text = "tồn tại"

        if loai_dau == 0:
            dau = ">"
            dap_an_dung_sai = "$Đúng$"

            giai_dung_sai = (
                f"Mệnh đề đảo là "
                f"\"${luong_tu_tex}: x > {a_val} \\Rightarrow |x| > {a_val}$\". "
                f"Nếu $x>{a_val}$ thì do ${a_val}>0$ nên $x>0$. "
                f"Suy ra $|x|=x>{a_val}$. "
                f"Do đó mệnh đề đảo là mệnh đề đúng."
            )

        elif loai_dau == 1:
            dau = r"\ge"

            dap_an_dung_sai = "$Đúng$"

            giai_dung_sai = (
                f"Mệnh đề đảo là "
                f"\"${luong_tu_tex}: x \\ge {a_val} \\Rightarrow |x| \\ge {a_val}$\". "
                f"Nếu $x\\ge {a_val}$ thì do ${a_val}>0$ nên $x\\ge0$. "
                f"Suy ra $|x|=x\\ge {a_val}$. "
                f"Do đó mệnh đề đảo là mệnh đề đúng."
            )

        elif loai_dau == 2:
            dau = "<"

            if loai_luong_tu == 0:

                dap_an_dung_sai = "$Sai$"

                phan_vi_du = -a_val - 1

                giai_dung_sai = (
                    f"Mệnh đề đảo là "
                    f"\"$\\forall x \\in \\mathbb{{R}}: x < {a_val} \\Rightarrow |x| < {a_val}$\". "
                    f"Mệnh đề này sai. "
                    f"Thật vậy, lấy $x={phan_vi_du}$ thì "
                    f"$x<{a_val}$ nhưng "
                    f"$|x|={abs(phan_vi_du)}>{a_val}$. "
                    f"Do đó mệnh đề đảo là mệnh đề sai."
                )

            else:

                dap_an_dung_sai = "$Đúng$"

                giai_dung_sai = (
                    f"Mệnh đề đảo là "
                    f"\"$\\exists x \\in \\mathbb{{R}}: x < {a_val} \\Rightarrow |x| < {a_val}$\". "
                    f"Lấy $x=0$ thì $0<{a_val}$ và $|0|=0<{a_val}$. "
                    f"Do đó tồn tại một số thực thỏa mãn mệnh đề, nên mệnh đề đảo đúng."
                )

        else:
            dau = r"\le"

            if loai_luong_tu == 0:

                dap_an_dung_sai = "$Sai$"

                phan_vi_du = -a_val - 1

                giai_dung_sai = (
                    f"Mệnh đề đảo là "
                    f"\"$\\forall x \\in \\mathbb{{R}}: x \\le {a_val} \\Rightarrow |x| \\le {a_val}$\". "
                    f"Mệnh đề này sai. "
                    f"Thật vậy, lấy $x={phan_vi_du}$ thì "
                    f"$x\\le {a_val}$ nhưng "
                    f"$|x|={abs(phan_vi_du)}>{a_val}$. "
                    f"Do đó mệnh đề đảo là mệnh đề sai."
                )

            else:

                dap_an_dung_sai = "$Đúng$"

                giai_dung_sai = (
                    f"Mệnh đề đảo là "
                    f"\"$\\exists x \\in \\mathbb{{R}}: x \\le {a_val} \\Rightarrow |x| \\le {a_val}$\". "
                    f"Lấy $x=0$ thì $0\\le {a_val}$ và $|0|=0\\le {a_val}$. "
                    f"Do đó tồn tại một số thực thỏa mãn mệnh đề, nên mệnh đề đảo đúng."
                )

        debai = (
            f"""Cho mệnh đề $P \\colon ``{luong_tu_tex}: |x| {dau} {a_val} """
            f"""\\Rightarrow x {dau} {a_val}$''."""
        )

        ds_abcd = [

            [
                "Phát biểu mệnh đề đảo của mệnh đề đã cho.",
                f"${luong_tu_tex}: x {dau} {a_val} \\Rightarrow |x| {dau} {a_val}$",
                f"Mệnh đề đảo của mệnh đề $P$ là "
                f"\"${luong_tu_tex}: x {dau} {a_val} \\Rightarrow |x| {dau} {a_val}$\"."
            ],

            [
                "Xét tính đúng sai của mệnh đề đảo.",
                dap_an_dung_sai,
                giai_dung_sai
            ]

        ]

        cauTN += TL_answer_const(
            debai,
            ds_abcd,
            0,
            0,
            dong
        )

    return cauTN

def L10_C1_B1_TH003_TL_B_01(socau, dong=1):

    gt = []
    dem = len(gt)

    while dem < socau:

        loai = np.random.randint(0, 6)

        if loai == 0:
            n = np.random.choice([2, 4, 6, 8])
            v = [loai, n]

        elif loai == 1:
            n = np.random.choice([2, 4, 6, 8])
            v = [loai, n]

        elif loai == 2:
            n = np.random.choice([2, 4, 6])
            a = np.random.choice([1, 4, 9, 16, 25])
            v = [loai, n, a]

        elif loai == 3:
            n = np.random.choice([2, 4, 6])
            a = np.random.choice([-1, -4, -9, -16])
            v = [loai, n, a]

        elif loai == 4:
            n = np.random.choice([3, 5, 7])
            v = [loai, n]

        else:
            n = np.random.choice([3, 5, 7])
            v = [loai, n]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''

    for v in gt:

        loai = v[0]

        # =========================
        # ∀ x, x^n ≥ 0
        # =========================
        if loai == 0:

            n = v[1]

            debai = (
                f"""Cho mệnh đề $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ge 0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}<0$"
            )

            ds_abcd = [

                [
                    "Phát biểu mệnh đề phủ định của mệnh đề đã cho.",
                    phu_dinh,
                    f"Mệnh đề phủ định của $P$ là: ``{phu_dinh}''."
                ],

                [
                    "Xét tính đúng sai của mệnh đề phủ định.",
                    "$Sai$",
                    f"Do $n={n}$ là số chẵn nên với mọi $x\\in\\mathbb{{R}}$ ta luôn có $x^{n}\\ge0$. "
                    f"Vì vậy không tồn tại số thực nào để $x^{n}<0$. "
                    f"Do đó mệnh đề phủ định là sai."
                ]

            ]

        # =========================
        # ∀ x, x^n > 0
        # =========================
        elif loai == 1:

            n = v[1]

            debai = (
                f"""Cho mệnh đề $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}>0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}\\le 0$"
            )

            ds_abcd = [

                [
                    "Phát biểu mệnh đề phủ định của mệnh đề đã cho.",
                    phu_dinh,
                    f"Mệnh đề phủ định của $P$ là: ``{phu_dinh}''."
                ],

                [
                    "Xét tính đúng sai của mệnh đề phủ định.",
                    "$Đúng$",
                    f"Lấy $x=0$ thì $0^{n}=0\\le0$. "
                    f"Do đó tồn tại số thực thỏa mãn điều kiện. "
                    f"Vì vậy mệnh đề phủ định đúng."
                ]

            ]

        # =========================
        # ∃ x, x^n = a (a > 0)
        # =========================
        elif loai == 2:

            n = v[1]
            a = v[2]

            debai = (
                f"""Cho mệnh đề $P:$ ``$\\exists x\\in\\mathbb{{R}},\\ x^{n}={a}$''. """
            )

            phu_dinh = (
                f"$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ne {a}$"
            )

            ds_abcd = [

                [
                    "Phát biểu mệnh đề phủ định của mệnh đề đã cho.",
                    phu_dinh,
                    f"Mệnh đề phủ định của $P$ là: ``{phu_dinh}''."
                ],

                [
                    "Xét tính đúng sai của mệnh đề phủ định.",
                    "$Sai$",
                    f"Ta có $x=\\sqrt[{n}]{{{a}}}$ là một số thực và "
                    f"$x^{n}={a}$. "
                    f"Do đó mệnh đề ban đầu đúng nên mệnh đề phủ định sai."
                ]

            ]

        # =========================
        # ∃ x, x^n = a (a < 0)
        # =========================
        elif loai == 3:

            n = v[1]
            a = v[2]

            debai = (
                f"""Cho mệnh đề $P:$ ``$\\exists x\\in\\mathbb{{R}},\\ x^{n}={a}$''. """
            )

            phu_dinh = (
                f"$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ne {a}$"
            )

            ds_abcd = [

                [
                    "Phát biểu mệnh đề phủ định của mệnh đề đã cho.",
                    phu_dinh,
                    f"Mệnh đề phủ định của $P$ là: ``{phu_dinh}''."
                ],

                [
                    "Xét tính đúng sai của mệnh đề phủ định.",
                    "$Đúng$",
                    f"Do $n={n}$ là số chẵn nên với mọi số thực $x$ ta có "
                    f"$x^{n}\\ge0$. "
                    f"Không thể có $x^{n}={a}$ với $a={a}<0$. "
                    f"Vì vậy mệnh đề phủ định đúng."
                ]

            ]

        # =========================
        # ∀ x, x^n ≥ 0 (n lẻ)
        # =========================
        elif loai == 4:

            n = v[1]

            debai = (
                f"""Cho mệnh đề $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ge0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}<0$"
            )

            ds_abcd = [

                [
                    "Phát biểu mệnh đề phủ định của mệnh đề đã cho.",
                    phu_dinh,
                    f"Mệnh đề phủ định của $P$ là: ``{phu_dinh}''."
                ],

                [
                    "Xét tính đúng sai của mệnh đề phủ định.",
                    "$Đúng$",
                    f"Lấy $x=-1$ thì "
                    f"$(-1)^{n}=-1<0$. "
                    f"Do đó tồn tại số thực thỏa mãn điều kiện. "
                    f"Vì vậy mệnh đề phủ định đúng."
                ]

            ]

        # =========================
        # ∀ x, x^n ≤ 0 (n lẻ)
        # =========================
        else:

            n = v[1]

            debai = (
                f"""Cho mệnh đề $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\le0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}>0$"
            )

            ds_abcd = [

                [
                    "Phát biểu mệnh đề phủ định của mệnh đề đã cho.",
                    phu_dinh,
                    f"Mệnh đề phủ định của $P$ là: ``{phu_dinh}''."
                ],

                [
                    "Xét tính đúng sai của mệnh đề phủ định.",
                    "$Đúng$",
                    f"Lấy $x=1$ thì "
                    f"$1^{n}=1>0$. "
                    f"Do đó tồn tại số thực thỏa mãn điều kiện. "
                    f"Vì vậy mệnh đề phủ định đúng."
                ]

            ]

        cauTN += TL_answer_const(
            debai,
            ds_abcd,
            0,
            0,
            dong
        )

    return cauTN



def L10_C1_B1_NB005_MC_A_01(socau, dang=1):
    # ==========================================
    # HÀM PHỤ BỎ VÀO TRONG (NESTED FUNCTION)
    # AI Agent bốc hàm chính đi đâu, hàm phụ đi theo đó
    # ==========================================
    def kiem_tra_nguyen_to(n):
        n = int(n)  # Ép kiểu chặn lỗi xung đột dữ liệu từ SymPy
        if n < 2:
            return False
        for i in range(2, int(float(n) ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    # ==========================================
    # LOGIC XỬ LÝ CHÍNH CỦA HÀM
    # ==========================================
    gt = []
    dem = 0
    da_dung_k = set()

    while dem < socau:
        k = random.randint(2000, 9999)
        if k in da_dung_k:
            continue

        # Gọi hàm phụ nằm bên trong nội bộ
        if kiem_tra_nguyen_to(k):
            c1_dung, c1_sai = 'số nguyên tố', 'hợp số'
        else:
            c1_dung, c1_sai = 'hợp số', 'số nguyên tố'

        if k % 2 == 0:
            c2_dung, c2_sai = 'số chẵn', 'số lẻ'
        else:
            c2_dung, c2_sai = 'số lẻ', 'số chẵn'

        tc = random.choice([c1_dung, c2_dung])

        dsnhieu = [f'${k}$ là {c1_sai}', f'${k}$ là {c2_sai}']
        thuoc_tinh_dung_con_lai = c2_dung if tc == c1_dung else c1_dung
        dsnhieu.append(f'${k}$ không phải là {thuoc_tinh_dung_con_lai}')

        dsnhieu = random.sample(dsnhieu, 3)

        da_dung_k.add(k)
        gt.append([k, tc, dsnhieu])
        dem += 1

    cauTN = ''
    for v in gt:
        k, tc, dsnhieu = v[0], v[1], v[2]

        dapso = f'${k}$ không phải là {tc}'
        debai = f"""Mệnh đề nào sau đây là mệnh đề phủ định của mệnh đề: ``${k}$ là {tc}''."""
        giai = f"""Mệnh đề phủ định của mệnh đề "$P$" là mệnh đề "Không phải $P$". Do đó phủ định của mệnh đề ``${k}$ là {tc}'' là ``${k}$ không phải là {tc}''."""

        # Gọi hàm framework chuẩn từ file math_type.py
        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    # Chuẩn hóa hệ thống chuỗi LaTeX bằng Regex an toàn
    cauTN = cauTN.replace("--", "+").replace("-+", "-").replace("+-", "-")
    cauTN = re.sub(r'(?<=\d)\.(?=\d)', ',', cauTN)

    return cauTN

def L10_C1_B1_NB005_MC_B_01(socau, dang=1):

    # Mỗi phần tử gồm:
    # [mệnh đề gốc, phủ định đúng, nhiễu 1, nhiễu 2, nhiễu 3]

    ds_menhde = [

        [
            'Lan là học sinh lớp 10',
            'Lan không phải là học sinh lớp 10',
            'Lan là giáo viên',
            'Lan thích học môn Toán',
            'Lan không thích học môn Toán'
        ],

        [
            'Minh thích học môn Toán',
            'Minh không thích học môn Toán',
            'Minh thích học môn Văn',
            'Minh là học sinh giỏi',
            'Minh không phải là học sinh'
        ],

        [
            'Nam biết chơi đàn guitar',
            'Nam không biết chơi đàn guitar',
            'Nam biết chơi piano',
            'Nam thích nghe nhạc',
            'Nam không thích âm nhạc'
        ],

        [
            'Hà là đội trưởng đội bóng',
            'Hà không phải là đội trưởng đội bóng',
            'Hà là thủ môn',
            'Hà thích đá bóng',
            'Hà không tham gia đội bóng'
        ],

        [
            'An đi học bằng xe đạp',
            'An không đi học bằng xe đạp',
            'An đi học bằng xe buýt',
            'An thích đi bộ',
            'An không đi học'
        ],

        [
            'Mai biết bơi',
            'Mai không biết bơi',
            'Mai thích đi biển',
            'Mai chơi cầu lông rất giỏi',
            'Mai không thích thể thao'
        ],

        [
            'Huy sống ở Hà Nội',
            'Huy không sống ở Hà Nội',
            'Huy sống ở Đà Nẵng',
            'Huy thích du lịch',
            'Huy chưa từng đến Hà Nội'
        ],

        [
            'Vy thích ăn kem',
            'Vy không thích ăn kem',
            'Vy thích uống trà sữa',
            'Vy ăn rất ít đồ ngọt',
            'Vy không thích món tráng miệng'
        ],

        [
            'Long biết nói tiếng Anh',
            'Long không biết nói tiếng Anh',
            'Long biết nói tiếng Pháp',
            'Long thích học ngoại ngữ',
            'Long không học tiếng Anh'
        ],

        [
            'Trâm học giỏi môn Vật lí',
            'Trâm không học giỏi môn Vật lí',
            'Trâm học giỏi môn Hóa học',
            'Trâm thích làm thí nghiệm',
            'Trâm không thích học'
        ],
        [
            'Lớp 10A toàn là nữ',
            'Lớp 10A không phải toàn là nữ',
            'Lớp 10A toàn là nam',
            'Lớp 10A không có bạn nam nào',
            'Lớp 10A có cả nam và nữ'
        ],


    ]

    gt = []
    dem = 0

    while dem < socau:

        data = random.choice(ds_menhde)

        # Mệnh đề gốc
        md_goc = data[0]

        # Đáp án đúng
        dapso = data[1]

        # 3 đáp án nhiễu
        dsnhieu = data[2:]

        debai = (
            f'Mệnh đề nào sau đây là mệnh đề phủ định của mệnh đề: '
            f"``{md_goc}''."
        )

        giai = (
            f'Mệnh đề phủ định của mệnh đề "$P$" là mệnh đề '
            f'"Không phải $P$". '
            f'Do đó phủ định của mệnh đề '
            f'``{md_goc}'' là ``{dapso}''.'
        )

        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dapso, dsnhieu, debai, giai])

            dem += 1

    cauTN = ''

    for dapso, dsnhieu, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    cauTN = cauTN.replace("--", "+").replace("-+", "-").replace("+-", "-")
    cauTN = re.sub(r'(?<=\d)\.(?=\d)', ',', cauTN)

    return cauTN

def L10_C1_B1_NB005_MC_C_01(socau, dang=1):

    x = Symbol('x')
    y = Symbol('y')

    # =========================================================
    # HÀM PHỤ
    # =========================================================

    PhuDinhDict = {

        '\\exists': '\\forall',

        '\\forall': '\\exists',

        '>': '\\leq',

        '<': '\\geq',

        '\\leq': '>',

        '\\geq': '<',

        '=': '\\ne',

        '\\ne': '='
    }

    # =========================================================
    # DANH SÁCH BIỂU THỨC
    # =========================================================

    ds_ham = []

    for _ in range(50):

        a = random.choice([i for i in range(-9, 10) if i != 0])

        b = random.randint(-9, 9)

        c = random.randint(-9, 9)

        d = random.choice([i for i in range(-9, 10) if i != 0])

        # Bậc nhất
        ds_ham.append(a * x + b)

        # Bậc hai
        ds_ham.append(a * x**2 + b * x + c)

        # Phân thức
        ds_ham.append((a * x + b) / d)

        # Hai biến
        ds_ham.append(a * x + b * y + c)

        # Tích
        ds_ham.append((x + a) * (x + b))

        # Giá trị tuyệt đối
        ds_ham.append(Abs(a * x + b))

        # Căn
        ds_ham.append(sqrt((x + a)**2 + 1))

        # Mũ đơn giản
        ds_ham.append(x**3 + a * x)

    # =========================================================
    # SINH DỮ LIỆU
    # =========================================================

    gt = []

    dem = len(gt)

    while dem < socau:

        ham = random.choice(ds_ham)

        dk1 = random.choice(['\\exists', '\\forall'])

        dk2 = random.choice([

            '>', '<',

            '\\leq', '\\geq',

            '=', '\\ne'
        ])

        dk2_phudinh = PhuDinhDict[dk2]

        dk1_phudinh = PhuDinhDict[dk1]

        tap = random.choice([

            r'\mathbb{R}',

            r'\mathbb{Z}',

            r'\mathbb{N}',

            r'\mathbb{Q}'
        ])

        bien = random.choice(['x', 'y'])

        # Chống trùng

        v = [

            latex(ham),

            dk1,

            dk2,

            tap,

            bien
        ]

        if v not in gt:

            gt.append(v)

            dem += 1

    # =========================================================
    # SINH ĐỀ
    # =========================================================

    cauTN = ''

    for v in gt:

        ham_latex = v[0]

        dk1 = v[1]

        dk2 = v[2]

        tap = v[3]

        bien = v[4]

        dk1_phudinh = PhuDinhDict[dk1]

        dk2_phudinh = PhuDinhDict[dk2]

        debai = (
            f"""Mệnh đề nào sau đây là mệnh đề phủ định của mệnh đề:
``${dk1} {bien} \\in {tap}, {ham_latex} {dk2} 0$''?"""
        )

        dapso = (
            rf"""{dk1_phudinh} {bien} \in {tap}, {ham_latex} {dk2_phudinh} 0"""
        )

        nhieu1 = (
            rf"""{dk1} {bien} \in {tap}, {ham_latex} {dk2_phudinh} 0"""
        )

        nhieu2 = (
            rf"""{dk1_phudinh} {bien} \in {tap}, {ham_latex} {dk2} 0"""
        )

        nhieu3 = (
            rf"""{dk1} {bien} \in {tap}, {ham_latex} {dk2} 0"""
        )

        dsnhieu = [

            nhieu1,

            nhieu2,

            nhieu3
        ]

        giai = (
            r"""Phủ định của mệnh đề chứa kí hiệu $\forall$ là $\exists$ và ngược lại,
đồng thời phủ định mệnh đề tính chất phía sau."""
        )

        cauTN += MC_SA_answer_const(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    # =========================================================
    # LÀM SẠCH CHUỖI
    # =========================================================

    cauTN = cauTN.replace("--", "+").replace("-+", "-").replace("+-", "-")

    cauTN = cauTN.replace(".0", ",0").replace(".1", ",1").replace(".2", ",2")

    cauTN = cauTN.replace(".3", ",3").replace(".4", ",4").replace(".5", ",5")

    cauTN = cauTN.replace(".6", ",6").replace(".7", ",7").replace(".8", ",8")

    cauTN = cauTN.replace(".9", ",9")

    return cauTN

def L10_C1_B1_NB007_MC_A_01(socau, dang=1):

    # Danh sách các mệnh đề kéo theo
    ds_keotheo = [
        r'Nếu một số chia hết cho $10$ thì số đó chia hết cho $5$',
        r'Nếu một tam giác là tam giác đều thì tam giác đó có ba cạnh bằng nhau',
        r'Nếu một số là số nguyên tố lớn hơn $2$ thì số đó là số lẻ',
        r'Nếu một tứ giác là hình vuông thì tứ giác đó có bốn góc vuông',
        r'Nếu một hình chữ nhật có bốn cạnh bằng nhau thì hình đó là hình vuông',
        r'Nếu hai góc đối đỉnh thì hai góc đó bằng nhau',
        r'Nếu một tam giác là tam giác vuông thì bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông',
        r'Nếu một số chia hết cho $6$ thì số đó chia hết cho $2$',
        r'Nếu một số chia hết cho $6$ thì số đó chia hết cho $3$',
        r'Nếu một hình bình hành có một góc vuông thì hình đó là hình chữ nhật',
        r'Nếu một hình thoi có một góc vuông thì hình đó là hình vuông',
        r'Nếu một số là bội của $4$ thì số đó là số chẵn',
        r'Nếu một số tận cùng bằng $0$ thì số đó chia hết cho $5$',
        r'Nếu một tam giác có ba cạnh bằng nhau thì tam giác đó là tam giác đều',
        r'Nếu một số là số chính phương thì căn bậc hai của nó là một số nguyên',
        r'Nếu hai đường thẳng cùng vuông góc với một đường thẳng thứ ba thì chúng song song với nhau',
        r'Nếu một hình chữ nhật có hai cạnh kề bằng nhau thì hình đó là hình vuông',
        r'Nếu một số chia hết cho $9$ thì tổng các chữ số của số đó chia hết cho $9$',
        r'Nếu một tam giác cân có một góc vuông thì tam giác đó là tam giác vuông cân',
        r'Nếu một số chia hết cho $2$ và $3$ thì số đó chia hết cho $6$'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    ds_khong_keotheo = [
        r'Tam giác đều có ba cạnh bằng nhau',
        r'Hình chữ nhật có bốn góc vuông',
        r'Số $25$ là số chính phương',
        r'Mọi số nguyên tố lớn hơn $2$ đều là số lẻ',
        r'Hai đường thẳng song song không có điểm chung',
        r'Hình vuông là hình chữ nhật có bốn cạnh bằng nhau',
        r'Tổng ba góc trong một tam giác bằng $180^{\circ}$',
        r'Đường kính đi qua tâm của đường tròn',
        r'Hình thoi có hai đường chéo vuông góc với nhau',
        r'Tập hợp rỗng được kí hiệu là $\varnothing$',
        r'Góc bẹt có số đo bằng $180^{\circ}$',
        r'Hình tròn có vô số trục đối xứng',
        r'Mọi hình vuông đều là hình thoi',
        r'Hình bình hành có các cạnh đối song song',
        r'Số $0$ là số nguyên',
        r'Hai góc đối đỉnh thì bằng nhau',
        r'Hình thang cân là hình thang có hai cạnh bên bằng nhau',
        r'Số $\sqrt{16}$ bằng $4$',
        r'Trong tam giác vuông, bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông',
        r'Mọi số nguyên chẵn đều chia hết cho $2$',

        r'Một số chia hết cho $2$ và chia hết cho $3$',
        r'Một tam giác vừa cân vừa vuông',
        r'Một hình vừa là hình chữ nhật vừa là hình thoi',
        r'Một số là số nguyên hoặc là số hữu tỉ',
        r'Một tam giác là tam giác đều hoặc là tam giác cân',
        r'Hai đường thẳng song song hoặc cắt nhau',

        r'Một số chia hết cho $6$ khi và chỉ khi số đó chia hết cho $2$ và $3$',
        r'Một tứ giác là hình vuông khi và chỉ khi nó là hình chữ nhật có bốn cạnh bằng nhau',
        r'Một tam giác là tam giác đều khi và chỉ khi nó có ba cạnh bằng nhau',
        r'Một số là số chẵn khi và chỉ khi số đó chia hết cho $2$',
        r'Một hình là hình chữ nhật khi và chỉ khi nó có bốn góc vuông',
        r'Hai tam giác bằng nhau khi và chỉ khi các cạnh tương ứng bằng nhau',
        r'Một số là số chính phương khi và chỉ khi căn bậc hai của nó là số nguyên',
        r'Hai đường thẳng vuông góc khi và chỉ khi góc tạo bởi chúng bằng $90^{\circ}$.'
    ]

    gt = []
    dem = 0

    while dem < socau:

        # 0: hỏi mệnh đề kéo theo
        # 1: hỏi mệnh đề không phải kéo theo
        loai = random.choice([0, 1])

        if loai == 0:

            # Đáp án đúng là mệnh đề kéo theo
            dapso = random.choice(ds_keotheo)

            # 3 đáp án nhiễu là không phải kéo theo
            dsnhieu = random.sample(ds_khong_keotheo, 3)

            debai = (
                r"Trong các mệnh đề sau, mệnh đề nào là mệnh đề kéo theo?"
            )

            giai = (
                r"Mệnh đề kéo theo là: " + dapso
            )

        else:

            # Đáp án đúng là không phải kéo theo
            dapso = random.choice(ds_khong_keotheo)

            # 3 đáp án nhiễu là kéo theo
            dsnhieu = random.sample(ds_keotheo, 3)

            debai = (
                r"Trong các mệnh đề sau, mệnh đề nào \textbf{không phải} là mệnh đề kéo theo?"
            )

            giai = (
                r"Mệnh đề không phải là mệnh đề kéo theo là: " + dapso
            )

        # Tránh trùng đề
        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B1_NB007_MC_C_01(socau, dang=1):
    # Danh sách các mệnh đề kéo theo
    ds_keotheo = [
        r'Nếu một số chia hết cho $10$ thì số đó chia hết cho $5$.',
        r'Nếu một tam giác là tam giác đều thì tam giác đó có ba cạnh bằng nhau.',
        r'Nếu một số là số nguyên tố lớn hơn $2$ thì số đó là số lẻ.',
        r'Nếu một tứ giác là hình vuông thì tứ giác đó có bốn góc vuông.',
        r'Nếu một hình chữ nhật có bốn cạnh bằng nhau thì hình đó là hình vuông.',
        r'Nếu hai góc đối đỉnh thì hai góc đó bằng nhau.',
        r'Nếu một tam giác là tam giác vuông thì bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông.',
        r'Nếu một số chia hết cho $6$ thì số đó chia hết cho $2$.',
        r'Nếu một số chia hết cho $6$ thì số đó chia hết cho $3$.',
        r'Nếu một hình bình hành có một góc vuông thì hình đó là hình chữ nhật.',
        r'Nếu một hình thoi có một góc vuông thì hình đó là hình vuông.',
        r'Nếu một số là bội của $4$ thì số đó là số chẵn.',
        r'Nếu một số tận cùng bằng $0$ thì số đó chia hết cho $5$.',
        r'Nếu một tam giác có ba cạnh bằng nhau thì tam giác đó là tam giác đều.',
        r'Nếu một số là số chính phương thì căn bậc hai của nó là một số nguyên.',
        r'Nếu hai đường thẳng cùng vuông góc với một đường thẳng thứ ba thì chúng song song với nhau.',
        r'Nếu một hình chữ nhật có hai cạnh kề bằng nhau thì hình đó là hình vuông.',
        r'Nếu một số chia hết cho $9$ thì tổng các chữ số của số đó chia hết cho $9$.',
        r'Nếu một tam giác cân có một góc vuông thì tam giác đó là tam giác vuông cân.',
        r'Nếu một số chia hết cho $2$ và $3$ thì số đó chia hết cho $6$.'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    ds_khong_keotheo = [
        r'Tam giác đều có ba cạnh bằng nhau.',
        r'Hình chữ nhật có bốn góc vuông.',
        r'Số $25$ là số chính phương.',
        r'Mọi số nguyên tố lớn hơn $2$ đều là số lẻ.',
        r'Hai đường thẳng song song không có điểm chung.',
        r'Hình vuông là hình chữ nhật có bốn cạnh bằng nhau.',
        r'Tổng ba góc trong một tam giác bằng $180^{\circ}$.',
        r'Đường kính đi qua tâm của đường tròn.',
        r'Hình thoi có hai đường chéo vuông góc với nhau.',
        r'Tập hợp rỗng được kí hiệu là $\varnothing$.',
        r'Góc bẹt có số đo bằng $180^{\circ}$.',
        r'Hình tròn có vô số trục đối xứng.',
        r'Mọi hình vuông đều là hình thoi.',
        r'Hình bình hành có các cạnh đối song song.',
        r'Số $0$ là số nguyên.',
        r'Hai góc đối đỉnh thì bằng nhau.',
        r'Hình thang cân là hình thang có hai cạnh bên bằng nhau.',
        r'Số $\sqrt{16}$ bằng $4$.',
        r'Trong tam giác vuông, bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông.',
        r'Mọi số nguyên chẵn đều chia hết cho $2$.',

        r'Một số chia hết cho $2$ và chia hết cho $3$.',
        r'Một tam giác vừa cân vừa vuông.',
        r'Một hình vừa là hình chữ nhật vừa là hình thoi.',
        r'Một số là số nguyên hoặc là số hữu tỉ.',
        r'Một tam giác là tam giác đều hoặc là tam giác cân.',
        r'Hai đường thẳng song song hoặc cắt nhau.',

        r'Một số chia hết cho $6$ khi và chỉ khi số đó chia hết cho $2$ và $3$.',
        r'Một tứ giác là hình vuông khi và chỉ khi nó là hình chữ nhật có bốn cạnh bằng nhau.',
        r'Một tam giác là tam giác đều khi và chỉ khi nó có ba cạnh bằng nhau.',
        r'Một số là số chẵn khi và chỉ khi số đó chia hết cho $2$.',
        r'Một hình là hình chữ nhật khi và chỉ khi nó có bốn góc vuông.',
        r'Hai tam giác bằng nhau khi và chỉ khi các cạnh tương ứng bằng nhau.',
        r'Một số là số chính phương khi và chỉ khi căn bậc hai của nó là số nguyên.',
        r'Hai đường thẳng vuông góc khi và chỉ khi góc tạo bởi chúng bằng $90^{\circ}$.'
    ]

    gt = []
    dem = 0

    while dem < socau:

        # 0: hỏi số mệnh đề kéo theo
        # 1: hỏi số mệnh đề không phải kéo theo
        loai = random.choice([0, 1])

        # Số lượng cần đếm
        dapso = random.randint(1, 4)

        if loai == 0:

            # Chọn mệnh đề kéo theo
            list_keotheo = random.sample(ds_keotheo, dapso)

            # Chọn mệnh đề không phải kéo theo
            list_khong = random.sample(ds_khong_keotheo, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_keotheo + list_khong

            debai = (
                r"Trong các mệnh đề sau, có bao nhiêu mệnh đề là mệnh đề kéo theo?"
            )

            giai = (
                r"Có " + str(dapso) + r" mệnh đề kéo theo."
            )

        else:

            # Chọn mệnh đề không phải kéo theo
            list_khong = random.sample(ds_khong_keotheo, dapso)

            # Chọn mệnh đề kéo theo
            list_keotheo = random.sample(ds_keotheo, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_khong + list_keotheo

            debai = (
                r"Trong các mệnh đề sau, có bao nhiêu mệnh đề \textbf{không phải} là mệnh đề kéo theo?"
            )

            giai = (
                r"Có " + str(dapso) + r" mệnh đề không phải là mệnh đề kéo theo."
            )

        # Trộn thứ tự
        random.shuffle(ds_cau)

        # Ghép nội dung đề
        debai += r"\\ " + r"\\ ".join(
            [f"{i+1}. {cau}" for i, cau in enumerate(ds_cau)]
        )

        # Đáp án nhiễu
        dsnhieu = random.sample(
            [x for x in range(5) if x != dapso],
            3
        )

        # Tránh trùng đề
        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B1_NB007_MC_B_01(socau, dang=1):

    # Danh sách các mệnh đề kéo theo
    # Nội dung thực tế, liên môn, kiến thức THCS trở xuống

    ds_keotheo = [

        # Toán học
        r'Nếu một số chia hết cho $10$ thì số đó chia hết cho $5$',
        r'Nếu một số chia hết cho $2$ thì chữ số tận cùng của số đó là số chẵn',
        r'Nếu một số là bội của $3$ thì tổng các chữ số của nó chia hết cho $3$',
        r'Nếu một tam giác có ba cạnh bằng nhau thì tam giác đó là tam giác đều',
        r'Nếu một hình chữ nhật có bốn cạnh bằng nhau thì hình đó là hình vuông',

        # Vật lí
        r'Nếu đun nóng nước đến $100^{\circ}$C ở áp suất thường thì nước sôi',
        r'Nếu có dòng điện chạy qua bóng đèn thì bóng đèn phát sáng',
        r'Nếu ngắt công tắc điện thì bóng đèn tắt',
        r'Nếu vật bị kéo xuống thì lò xo bị dãn',
        r'Nếu ma sát giảm thì vật chuyển động dễ hơn',

        # Hóa học
        r'Nếu cho kim loại sắt vào axit clohiđric thì có khí hiđro thoát ra',
        r'Nếu cho giấy quỳ tím vào dung dịch axit thì giấy chuyển sang màu đỏ',
        r'Nếu đốt cháy than trong không khí thì tạo ra khí cacbonic',
        r'Nếu hòa tan muối ăn vào nước thì thu được dung dịch',
        r'Nếu cho vôi sống vào nước thì xảy ra phản ứng hóa học',

        # Sinh học
        r'Nếu cây không được tưới nước trong thời gian dài thì cây sẽ héo',
        r'Nếu con người không hít thở thì không thể sống',
        r'Nếu thiếu ánh sáng thì cây xanh phát triển kém',
        r'Nếu ăn quá nhiều đồ ngọt thì dễ bị sâu răng',
        r'Nếu rửa tay bằng xà phòng thì giúp hạn chế vi khuẩn',

        # Địa lí
        r'Nếu nhiệt độ giảm xuống dưới $0^{\circ}$C thì nước có thể đóng băng',
        r'Nếu trời mưa lớn kéo dài thì dễ xảy ra ngập lụt',
        r'Nếu phá rừng đầu nguồn thì dễ xảy ra xói mòn đất',
        r'Nếu có động đất mạnh dưới đáy biển thì có thể xảy ra sóng thần',

        # Tin học
        r'Nếu nhập sai mật khẩu thì không đăng nhập được tài khoản',
        r'Nếu máy tính bị mất điện đột ngột thì dữ liệu chưa lưu có thể bị mất',
        r'Nếu kết nối Internet bị ngắt thì không truy cập được trang web',

        # Đời sống
        r'Nếu thức khuya thường xuyên thì cơ thể dễ mệt mỏi',
        r'Nếu đội mũ bảo hiểm khi đi xe máy thì giúp giảm nguy cơ chấn thương',
        r'Nếu học bài đầy đủ thì kết quả kiểm tra thường tốt hơn',
        r'Nếu tập thể dục thường xuyên thì sức khỏe được cải thiện'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    # Gồm mệnh đề đơn, tuyển, hội, tương đương

    ds_khong_keotheo = [

        # Mệnh đề đơn
        r'Trái Đất quay quanh Mặt Trời',
        r'Nước biển có vị mặn',
        r'Không khí chứa khí oxi',
        r'Hình vuông có bốn cạnh bằng nhau',
        r'Tam giác đều có ba góc bằng nhau',
        r'Con người cần nước để sống',
        r'Cây xanh tạo ra khí oxi',
        r'Mặt Trăng quay quanh Trái Đất',
        r'Số $25$ là số chính phương',
        r'Tổng ba góc trong tam giác bằng $180^{\circ}$',

        # Hội
        r'Một số chia hết cho $2$ và chia hết cho $5$',
        r'Một tam giác vừa cân vừa vuông',
        r'Một học sinh vừa học giỏi vừa chăm chỉ',
        r'Một hình vừa là hình chữ nhật vừa là hình thoi',
        r'Một chất vừa ở thể rắn vừa ở thể lỏng',

        # Tuyển
        r'Một số là số nguyên hoặc là số hữu tỉ',
        r'Hôm nay trời mưa hoặc trời nắng',
        r'Một học sinh học Toán hoặc học Tiếng Anh',
        r'Một tam giác là tam giác cân hoặc tam giác đều',
        r'Một vật chìm hoặc nổi trong nước',

        # Mệnh đề tương đương
        r'Một số chia hết cho $10$ khi và chỉ khi chữ số tận cùng là $0$',
        r'Một tam giác là tam giác đều khi và chỉ khi nó có ba cạnh bằng nhau',
        r'Một số là số chẵn khi và chỉ khi số đó chia hết cho $2$',
        r'Một hình là hình vuông khi và chỉ khi nó là hình chữ nhật có bốn cạnh bằng nhau',
        r'Nước sôi khi và chỉ khi nhiệt độ đạt $100^{\circ}$C ở áp suất thường',
        r'Một học sinh được lên lớp khi và chỉ khi đạt đủ điều kiện đánh giá',
        r'Một chất dẫn điện khi và chỉ khi nó cho dòng điện đi qua',
        r'Một phương trình bậc nhất có nghiệm duy nhất khi và chỉ khi hệ số của $x$ khác $0$',

        r'Một số chia hết cho $6$ khi và chỉ khi số đó chia hết cho $2$ và $3$',
        r'Một tam giác vuông khi và chỉ khi bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông',
        r'Một số là số chính phương khi và chỉ khi căn bậc hai của nó là số nguyên',
        r'Một tứ giác là hình chữ nhật khi và chỉ khi nó có bốn góc vuông',
        r'Một hình thang là hình thang cân khi và chỉ khi hai cạnh bên bằng nhau',
        r'Hai góc đối đỉnh bằng nhau khi và chỉ khi chúng là hai góc đối đỉnh',
        r'Một số chia hết cho $9$ khi và chỉ khi tổng các chữ số của nó chia hết cho $9$',
        r'Một tam giác cân khi và chỉ khi nó có hai cạnh bằng nhau',
        r'Một số nguyên là số chẵn khi và chỉ khi nó không có số dư khi chia cho $2$',
        r'Một phân số bằng $0$ khi và chỉ khi tử số bằng $0$ và mẫu số khác $0$',

        r'Một máy tính kết nối Internet khi và chỉ khi nó truy cập được trang web',
        r'Một học sinh được công nhận hoàn thành môn học khi và chỉ khi đạt yêu cầu đánh giá',
        r'Một bóng đèn sáng khi và chỉ khi có dòng điện chạy qua',
        r'Một cây phát triển tốt khi và chỉ khi được cung cấp đủ nước và ánh sáng',
        r'Một vật nổi trên nước khi và chỉ khi khối lượng riêng của nó nhỏ hơn khối lượng riêng của nước',
        r'Một phản ứng cháy xảy ra khi và chỉ khi có oxi tham gia',
        r'Một số nguyên tố khi và chỉ khi nó chỉ có đúng hai ước dương',
        r'Một tam giác cân tại $A$ khi và chỉ khi hai góc ở đáy bằng nhau',
        r'Một hình bình hành là hình chữ nhật khi và chỉ khi nó có một góc vuông',
        r'Một hình bình hành là hình thoi khi và chỉ khi hai cạnh kề bằng nhau'
    ]

    gt = []
    dem = 0

    while dem < socau:

        # 0: hỏi mệnh đề kéo theo
        # 1: hỏi mệnh đề không phải kéo theo
        loai = random.choice([0, 1])

        if loai == 0:

            # Đáp án đúng là mệnh đề kéo theo
            dapso = random.choice(ds_keotheo)

            # 3 đáp án nhiễu
            dsnhieu = random.sample(ds_khong_keotheo, 3)

            debai = (
                r"Trong các mệnh đề sau, mệnh đề nào là mệnh đề kéo theo?"
            )

            giai = (
                r"Mệnh đề kéo theo là: " + dapso + "."
            )

        else:

            # Đáp án đúng là không phải kéo theo
            dapso = random.choice(ds_khong_keotheo)

            # 3 đáp án nhiễu
            dsnhieu = random.sample(ds_keotheo, 3)

            debai = (
                r"Trong các mệnh đề sau, mệnh đề nào \textbf{không phải} là mệnh đề kéo theo?"
            )

            giai = (
                r"Mệnh đề không phải là mệnh đề kéo theo là: " + dapso + "."
            )

        # Tránh trùng đề
        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B1_NB007_MC_D_01(socau, dang=1):

    # Danh sách các mệnh đề kéo theo
    # Nội dung thực tế, liên môn, kiến thức THCS trở xuống

    ds_keotheo = [

        # Toán học
        r'Nếu một số chia hết cho $10$ thì số đó chia hết cho $5$.',
        r'Nếu một số chia hết cho $2$ thì chữ số tận cùng của số đó là số chẵn.',
        r'Nếu một số là bội của $3$ thì tổng các chữ số của nó chia hết cho $3$.',
        r'Nếu một tam giác có ba cạnh bằng nhau thì tam giác đó là tam giác đều.',
        r'Nếu một hình chữ nhật có bốn cạnh bằng nhau thì hình đó là hình vuông.',

        # Vật lí
        r'Nếu đun nóng nước đến $100^{\circ}$C ở áp suất thường thì nước sôi.',
        r'Nếu có dòng điện chạy qua bóng đèn thì bóng đèn phát sáng.',
        r'Nếu ngắt công tắc điện thì bóng đèn tắt.',
        r'Nếu vật bị kéo xuống thì lò xo bị dãn.',
        r'Nếu ma sát giảm thì vật chuyển động dễ hơn.',

        # Hóa học
        r'Nếu cho kim loại sắt vào axit clohiđric thì có khí hiđro thoát ra.',
        r'Nếu cho giấy quỳ tím vào dung dịch axit thì giấy chuyển sang màu đỏ.',
        r'Nếu đốt cháy than trong không khí thì tạo ra khí cacbonic.',
        r'Nếu hòa tan muối ăn vào nước thì thu được dung dịch.',
        r'Nếu cho vôi sống vào nước thì xảy ra phản ứng hóa học.',

        # Sinh học
        r'Nếu cây không được tưới nước trong thời gian dài thì cây sẽ héo.',
        r'Nếu con người không hít thở thì không thể sống.',
        r'Nếu thiếu ánh sáng thì cây xanh phát triển kém.',
        r'Nếu ăn quá nhiều đồ ngọt thì dễ bị sâu răng.',
        r'Nếu rửa tay bằng xà phòng thì giúp hạn chế vi khuẩn.',

        # Địa lí
        r'Nếu nhiệt độ giảm xuống dưới $0^{\circ}$C thì nước có thể đóng băng.',
        r'Nếu trời mưa lớn kéo dài thì dễ xảy ra ngập lụt.',
        r'Nếu phá rừng đầu nguồn thì dễ xảy ra xói mòn đất.',
        r'Nếu có động đất mạnh dưới đáy biển thì có thể xảy ra sóng thần.',

        # Tin học
        r'Nếu nhập sai mật khẩu thì không đăng nhập được tài khoản.',
        r'Nếu máy tính bị mất điện đột ngột thì dữ liệu chưa lưu có thể bị mất.',
        r'Nếu kết nối Internet bị ngắt thì không truy cập được trang web.',

        # Đời sống
        r'Nếu thức khuya thường xuyên thì cơ thể dễ mệt mỏi.',
        r'Nếu đội mũ bảo hiểm khi đi xe máy thì giúp giảm nguy cơ chấn thương.',
        r'Nếu học bài đầy đủ thì kết quả kiểm tra thường tốt hơn.',
        r'Nếu tập thể dục thường xuyên thì sức khỏe được cải thiện.'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    # Gồm mệnh đề đơn, tuyển, hội, tương đương

    ds_khong_keotheo = [

        # Mệnh đề đơn
        r'Trái Đất quay quanh Mặt Trời.',
        r'Nước biển có vị mặn.',
        r'Không khí chứa khí oxi.',
        r'Hình vuông có bốn cạnh bằng nhau.',
        r'Tam giác đều có ba góc bằng nhau.',
        r'Con người cần nước để sống.',
        r'Cây xanh tạo ra khí oxi.',
        r'Mặt Trăng quay quanh Trái Đất.',
        r'Số $25$ là số chính phương.',
        r'Tổng ba góc trong tam giác bằng $180^{\circ}$.',

        # Hội
        r'Một số chia hết cho $2$ và chia hết cho $5$.',
        r'Một tam giác vừa cân vừa vuông.',
        r'Một học sinh vừa học giỏi vừa chăm chỉ.',
        r'Một hình vừa là hình chữ nhật vừa là hình thoi.',
        r'Một chất vừa ở thể rắn vừa ở thể lỏng.',

        # Tuyển
        r'Một số là số nguyên hoặc là số hữu tỉ.',
        r'Hôm nay trời mưa hoặc trời nắng.',
        r'Một học sinh học Toán hoặc học Tiếng Anh.',
        r'Một tam giác là tam giác cân hoặc tam giác đều.',
        r'Một vật chìm hoặc nổi trong nước.',

        # Mệnh đề tương đương
        r'Một số chia hết cho $10$ khi và chỉ khi chữ số tận cùng là $0$.',
        r'Một tam giác là tam giác đều khi và chỉ khi nó có ba cạnh bằng nhau.',
        r'Một số là số chẵn khi và chỉ khi số đó chia hết cho $2$.',
        r'Một hình là hình vuông khi và chỉ khi nó là hình chữ nhật có bốn cạnh bằng nhau.',
        r'Nước sôi khi và chỉ khi nhiệt độ đạt $100^{\circ}$C ở áp suất thường.',
        r'Một học sinh được lên lớp khi và chỉ khi đạt đủ điều kiện đánh giá.',
        r'Một chất dẫn điện khi và chỉ khi nó cho dòng điện đi qua.',
        r'Một phương trình bậc nhất có nghiệm duy nhất khi và chỉ khi hệ số của $x$ khác $0$.',

        r'Một số chia hết cho $6$ khi và chỉ khi số đó chia hết cho $2$ và $3$.',
        r'Một tam giác vuông khi và chỉ khi bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông.',
        r'Một số là số chính phương khi và chỉ khi căn bậc hai của nó là số nguyên.',
        r'Một tứ giác là hình chữ nhật khi và chỉ khi nó có bốn góc vuông.',
        r'Một hình thang là hình thang cân khi và chỉ khi hai cạnh bên bằng nhau.',
        r'Hai góc đối đỉnh bằng nhau khi và chỉ khi chúng là hai góc đối đỉnh.',
        r'Một số chia hết cho $9$ khi và chỉ khi tổng các chữ số của nó chia hết cho $9$.',
        r'Một tam giác cân khi và chỉ khi nó có hai cạnh bằng nhau.',
        r'Một số nguyên là số chẵn khi và chỉ khi nó không có số dư khi chia cho $2$.',
        r'Một phân số bằng $0$ khi và chỉ khi tử số bằng $0$ và mẫu số khác $0$.',

        r'Một máy tính kết nối Internet khi và chỉ khi nó truy cập được trang web.',
        r'Một học sinh được công nhận hoàn thành môn học khi và chỉ khi đạt yêu cầu đánh giá.',
        r'Một bóng đèn sáng khi và chỉ khi có dòng điện chạy qua.',
        r'Một cây phát triển tốt khi và chỉ khi được cung cấp đủ nước và ánh sáng.',
        r'Một vật nổi trên nước khi và chỉ khi khối lượng riêng của nó nhỏ hơn khối lượng riêng của nước.',
        r'Một phản ứng cháy xảy ra khi và chỉ khi có oxi tham gia.',
        r'Một số nguyên tố khi và chỉ khi nó chỉ có đúng hai ước dương.',
        r'Một tam giác cân tại $A$ khi và chỉ khi hai góc ở đáy bằng nhau.',
        r'Một hình bình hành là hình chữ nhật khi và chỉ khi nó có một góc vuông.',
        r'Một hình bình hành là hình thoi khi và chỉ khi hai cạnh kề bằng nhau.'
    ]
    gt = []
    dem = 0

    while dem < socau:

        # 0: hỏi số mệnh đề kéo theo
        # 1: hỏi số mệnh đề không phải kéo theo
        loai = random.choice([0, 1])

        # Số lượng cần đếm
        dapso = random.randint(1, 4)

        if loai == 0:

            # Chọn mệnh đề kéo theo
            list_keotheo = random.sample(ds_keotheo, dapso)

            # Chọn mệnh đề không phải kéo theo
            list_khong = random.sample(ds_khong_keotheo, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_keotheo + list_khong

            debai = (
                r"Trong các mệnh đề sau, có bao nhiêu mệnh đề là mệnh đề kéo theo?"
            )

            giai = (
                r"Có " + str(dapso) + r" mệnh đề kéo theo."
            )

        else:

            # Chọn mệnh đề không phải kéo theo
            list_khong = random.sample(ds_khong_keotheo, dapso)

            # Chọn mệnh đề kéo theo
            list_keotheo = random.sample(ds_keotheo, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_khong + list_keotheo

            debai = (
                r"Trong các mệnh đề sau, có bao nhiêu mệnh đề \textbf{không phải} là mệnh đề kéo theo?"
            )

            giai = (
                r"Có " + str(dapso) + r" mệnh đề không phải là mệnh đề kéo theo."
            )

        # Trộn thứ tự
        random.shuffle(ds_cau)

        # Ghép nội dung đề
        debai += r"\\ " + r"\\ ".join(
            [f"{i+1}. {cau}" for i, cau in enumerate(ds_cau)]
        )

        # Đáp án nhiễu
        dsnhieu = random.sample(
            [x for x in range(5) if x != dapso],
            3
        )

        # Tránh trùng đề
        if [debai, dapso, dsnhieu] not in gt:

            gt.append([dsnhieu, dapso, debai, giai])

            dem += 1

    cauTN = ''

    for dsnhieu, dapso, debai, giai in gt:

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B1_NB008_MC_A_01(socau, dang=1):

    gt = []
    dem = len(gt)

    # =========================================================
    # DANH SÁCH MỆNH ĐỀ TOÁN HỌC
    # =========================================================

    ds_toan = [

        (
            "$a$ là một số chia hết cho $10$",
            "$a$ là một số chia hết cho $5$",
            "$a$ là một số chia hết cho $10$",
            "$a$ là một số chia hết cho $5$"
        ),

        (
            "$a$ là một số chia hết cho $6$",
            "$a$ là một số chia hết cho $2$",
            "$a$ là một số chia hết cho $6$",
            "$a$ là một số chia hết cho $2$"
        ),

        (
            "$a$ là một số chia hết cho $6$",
            "$a$ là một số chia hết cho $3$",
            "$a$ là một số chia hết cho $6$",
            "$a$ là một số chia hết cho $3$"
        ),

        (
            "$a$ là một số chính phương",
            "Căn bậc hai của $a$ là số nguyên",
            "$a$ là một số chính phương",
            "căn bậc hai của $a$ là số nguyên"
        ),

        (
            "$a$ là số nguyên tố lớn hơn $2$",
            "$a$ là số lẻ",
            "$a$ là số nguyên tố lớn hơn $2$",
            "$a$ là số lẻ"
        ),

        (
            "Tam giác $ABC$ có ba cạnh bằng nhau",
            "Tam giác $ABC$ là tam giác đều",
            "tam giác $ABC$ có ba cạnh bằng nhau",
            "tam giác $ABC$ là tam giác đều"
        ),

        (
            "Tam giác  $ABC$ là tam giác đều",
            "Tam giác $ABC$ có ba góc bằng nhau",
            "tam giác $ABC$ là tam giác đều",
            "tam giác $ABC$ có ba góc bằng nhau"
        ),

        (
            "Tam giác $ABC$ là tam giác vuông",
            "Tam giác $ABC$ có bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông",
            "tam giác $ABC$ là tam giác vuông",
            "tam giác $ABC$ có bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông"
        ),

        (
            "Hình chữ nhật $MNPQ$ có bốn cạnh bằng nhau",
            "Hình chữ nhật $MNPQ$ là hình vuông",
            "hình chữ nhật $MNPQ$ có bốn cạnh bằng nhau",
            "hình chữ nhật $MNPQ$ là hình vuông"
        ),

        (
            "Hình bình hành $MNPQ$ có một góc vuông",
            "Hình bình hành $MNPQ$ là hình chữ nhật",
            "hình bình hành $MNPQ$ có một góc vuông",
            "hình bình hành $MNPQ$ là hình chữ nhật"
        ),

        (
            "Hình thoi $ABCD$ có một góc vuông",
            "Hình thoi $ABCD$ là hình vuông",
            "hình thoi $ABCD$ có một góc vuông",
            "hình thoi $ABCD$ là hình vuông"
        ),

        (
            "Hai đường thẳng $a$ và $b$ cùng vuông góc với đường thẳng $c$",
            "Hai đường thẳng $a$ và $b$ song song với nhau",
            "hai đường thẳng $a$ và $b$ cùng vuông góc với đường thẳng $c$",
            "hai đường thẳng $a$ và $b$ song song với nhau"
        ),

        (
            "$a$ là bội của $4$",
            "$a$ là số chẵn",
            "$a$ là bội của $4$",
            "$a$ là số chẵn"
        )
    ]

    while dem < socau:

        P_text, Q_text, p_text, q_text = random.choice(ds_toan)

        v = [P_text, Q_text]

        if v not in gt:
            gt.append([P_text, Q_text, p_text, q_text])
            dem += 1

    cauTN = ''

    for v in gt:

        P_text, Q_text, p_text, q_text = v

        debai = f"""Cho hai mệnh đề sau:\\\\
            $P \\colon$ ``{P_text}'';\\\\
            $Q \\colon$ ``{Q_text}''.\\\\
            Hãy phát biểu mệnh đề kéo theo $P \\Rightarrow Q$."""

        dapso = f"""Nếu {p_text} thì {q_text}"""

        dsnhieu = [
            f"""Nếu {q_text} thì {p_text}""",
            f"""{P_text} khi và chỉ khi {q_text}""",
            f"""Nếu {p_text} thì không có chuyện {q_text}"""
        ]

        giai = f"""Mệnh đề kéo theo $P \\Rightarrow Q$ được phát biểu dưới dạng: ``Nếu $P$ thì $Q$''. Do đó đáp án đúng là: ``Nếu {p_text} thì {q_text}''."""

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN



def L10_C1_B1_NB008_MC_B_01(socau, dang=1):

    gt = []
    dem = len(gt)

    # =========================================================
    # DANH SÁCH MỆNH ĐỀ LIÊN MÔN / THỰC TẾ
    # =========================================================

    ds_thucte = [

        # Vật lí
        (
            "Thanh kim loại A bị đốt nóng ở nhiệt độ cao",
            "Chiều dài của thanh kim loại A tăng lên",
            "thanh kim loại A bị đốt nóng ở nhiệt độ cao",
            "chiều dài của thanh kim loại A tăng lên"
        ),

        (
            "Tia sáng truyền xiên góc từ không khí vào nước",
            "Tia sáng bị gãy khúc tại mặt phân cách",
            "tia sáng truyền xiên góc từ không khí vào nước",
            "tia sáng bị gãy khúc tại mặt phân cách"
        ),

        (
            "Vật bị kéo xuống",
            "Lò xo bị dãn",
            "vật bị kéo xuống",
            "lò xo bị dãn"
        ),

        # Lịch sử
        (
            "Hiệp định Genève năm 1954 được ký kết",
            "Hòa bình được lập lại ở miền Bắc Việt Nam",
            "Hiệp định Genève năm 1954 được ký kết",
            "hòa bình được lập lại ở miền Bắc Việt Nam"
        ),

        # Kinh tế
        (
            "Nguồn cung dầu mỏ toàn cầu bị cắt giảm mạnh",
            "Giá xăng dầu có xu hướng tăng",
            "nguồn cung dầu mỏ toàn cầu bị cắt giảm mạnh",
            "giá xăng dầu có xu hướng tăng"
        ),

        (
            "Một quốc gia rơi vào siêu lạm phát",
            "Sức mua của đồng tiền giảm mạnh",
            "một quốc gia rơi vào siêu lạm phát",
            "sức mua của đồng tiền giảm mạnh"
        ),

        # Đời sống
        (
            "Tập thể dục thường xuyên",
            "Sức khỏe được cải thiện",
            "tập thể dục thường xuyên",
            "sức khỏe được cải thiện"
        ),

        (
            "Căng thẳng địa chính trị xảy ra nghiêm trọng trên thế giới",
            "Giá vàng có xu hướng tăng nhanh trong ngắn hạn",
            "căng thẳng địa chính trị xảy ra nghiêm trọng trên thế giới",
            "giá vàng có xu hướng tăng nhanh trong ngắn hạn"
        ),

        (
            "James Watt phát minh ra máy hơi nước vào thế kỷ XVIII",
            "Cuộc cách mạng công nghiệp được mở đầu tại Anh",
            "James Watt phát minh ra máy hơi nước vào thế kỷ XVIII",
            "cuộc cách mạng công nghiệp được mở đầu tại Anh"
        ),

        (
            "Hiệp định Genève năm 1954 về Đông Dương được ký kết",
            "Hòa bình được lập lại ở miền Bắc Việt Nam",
            "Hiệp định Genève năm 1954 về Đông Dương được ký kết",
            "hòa bình được lập lại ở miền Bắc Việt Nam"
        ),

        (
            "Trái Đất tự quay quanh trục từ Tây sang Đông",
            "Hiện tượng ngày và đêm luân phiên diễn ra trên Trái Đất",
            "Trái Đất tự quay quanh trục từ Tây sang Đông",
            "hiện tượng ngày và đêm luân phiên diễn ra trên Trái Đất"
        ),

        (
            "Thanh kim loại bị đốt nóng ở nhiệt độ cao",
            "Chiều dài của thanh kim loại đó tăng lên so với ban đầu",
            "thanh kim loại bị đốt nóng ở nhiệt độ cao",
            "chiều dài của thanh kim loại đó tăng lên so với ban đầu"
        ),

        (
            "Đốt cháy hoàn toàn một lượng than củi trong khí ô-xi",
            "Khí cac-bo-nic được sinh ra từ phản ứng hóa học",
            "đốt cháy hoàn toàn một lượng than củi trong khí ô-xi",
            "khí cac-bo-nic được sinh ra từ phản ứng hóa học"
        ),

        (
            "Nguồn cung dầu mỏ toàn cầu bị cắt giảm đột ngột",
            "Giá xăng dầu trong nước và quốc tế đồng loạt tăng vọt",
            "nguồn cung dầu mỏ toàn cầu bị cắt giảm đột ngột",
            "giá xăng dầu trong nước và quốc tế đồng loạt tăng vọt"
        ),

        (
            "Tia sáng truyền xiên góc từ môi trường không khí vào nước",
            "Tia sáng bị gãy khúc tại mặt phân cách giữa hai môi trường",
            "tia sáng truyền xiên góc từ môi trường không khí vào nước",
            "tia sáng bị gãy khúc tại mặt phân cách giữa hai môi trường"
        ),

        (
            "Dòng điện xoay chiều chạy qua một cuộn dây dẫn",
            "Từ trường biến thiên được hình thành xung quanh cuộn dây",
            "dòng điện xoay chiều chạy qua một cuộn dây dẫn",
            "từ trường biến thiên được hình thành xung quanh cuộn dây"
        ),

        (
            "Thả một mẩu đá vôi vào dung dịch acid clohydric",
            "Hiện tượng sủi bọt khí xuất hiện trong ống nghiệm",
            "thả một mẩu đá vôi vào dung dịch acid clohydric",
            "hiện tượng sủi bọt khí xuất hiện trong ống nghiệm"
        ),

        (
            "Cây xanh thực hiện quá trình quang hợp dưới ánh sáng mặt trời",
            "Khí ô-xi được giải phóng ra môi trường khí quyển",
            "cây xanh thực hiện quá trình quang hợp dưới ánh sáng mặt trời",
            "khí ô-xi được giải phóng ra môi trường khí quyển"
        ),

        (
            "Mặt Trăng đi vào vùng bóng tối của Trái Đất",
            "Hiện tượng nguyệt thực xảy ra đối với người quan sát",
            "Mặt Trăng đi vào vùng bóng tối của Trái Đất",
            "hiện tượng nguyệt thực xảy ra đối với người quan sát"
        ),

        (
            "Không khí chứa hơi nước bị đẩy lên cao gặp lạnh",
            "Quá trình ngưng tụ tạo thành mây và gây mưa diễn ra",
            "không khí chứa hơi nước bị đẩy lên cao gặp lạnh",
            "quá trình ngưng tụ tạo thành mây và gây mưa diễn ra"
        ),

        (
            "Quân dân nhà Trần giành thắng lợi lớn tại trận Bạch Đằng năm 1288",
            "Cuộc xâm lược lần thứ ba của quân Nguyên Mông hoàn toàn tan rã",
            "quân dân nhà Trần giành thắng lợi lớn tại trận Bạch Đằng năm 1288",
            "cuộc xâm lược lần thứ ba của quân Nguyên Mông hoàn toàn tan rã"
        ),

        (
            "Triều đình nhà Nguyễn ký kết Hiệp ước Nhâm Tuất năm 1862",
            "Ba tỉnh miền Đông Nam Kỳ bị cắt nhượng cho thực dân Pháp",
            "Triều đình nhà Nguyễn ký kết Hiệp ước Nhâm Tuất năm 1862",
            "ba tỉnh miền Đông Nam Kỳ bị cắt nhượng cho thực dân Pháp"
        ),

        (
            "Cuộc Cách mạng tháng Mười Nga năm 1917 giành được thắng lợi",
            "Nhà nước xã hội chủ nghĩa đầu tiên trên thế giới được thành lập",
            "cuộc Cách mạng tháng Mười Nga năm 1917 giành được thắng lợi",
            "nhà nước xã hội chủ nghĩa đầu tiên trên thế giới được thành lập"
        ),

        (
            "Nhu cầu mua một loại nông sản xuất khẩu tăng mạnh",
            "Thương lái đẩy mạnh thu mua làm giá nông sản đó tăng theo",
            "nhu cầu mua một loại nông sản xuất khẩu tăng mạnh",
            "thương lái đẩy mạnh thu mua làm giá nông sản đó tăng theo"
        ),

        (
            "Một quốc gia rơi vào tình trạng siêu lạm phát kéo dài",
            "Sức mua tiêu dùng của đồng nội tệ bị suy giảm nghiêm trọng",
            "một quốc gia rơi vào tình trạng siêu lạm phát kéo dài",
            "sức mua tiêu dùng của đồng nội tệ bị suy giảm nghiêm trọng"
        ),

        (
            "Dòng sông mang theo lượng phù sa lớn đổ về cửa biển",
            "Đồng bằng châu thổ tại vùng cửa sông được mở rộng dần",
            "dòng sông mang theo lượng phù sa lớn đổ về cửa biển",
            "đồng bằng châu thổ tại vùng cửa sông được mở rộng dần"
        ),

        (
            "Vùng địa chất xảy ra sự đứt gãy mạnh trong lòng đất",
            "Các trận động đất và chấn động lan truyền trên bề mặt",
            "vùng địa chất xảy ra sự đứt gãy mạnh trong lòng đất",
            "các trận động đất và chấn động lan truyền trên bề mặt"
        )
    ]

    while dem < socau:

        P_text, Q_text, p_text, q_text = random.choice(ds_thucte)

        v = [P_text, Q_text]

        if v not in gt:
            gt.append([P_text, Q_text, p_text, q_text])
            dem += 1

    cauTN = ''

    for v in gt:

        P_text, Q_text, p_text, q_text = v

        debai = f"""Cho hai mệnh đề sau:\\\\
            $P \\colon$ ``{P_text}'';\\\\
            $Q \\colon$ ``{Q_text}''.\\\\
            Hãy phát biểu mệnh đề kéo theo $P \\Rightarrow Q$."""

        dapso = f"""Nếu {p_text} thì {q_text}"""

        dsnhieu = [
            f"""Nếu {q_text} thì {p_text}""",
            f"""{P_text} khi và chỉ khi {q_text}""",
            f"""Nếu {p_text} thì không có chuyện {q_text}"""
        ]

        giai = f"""Mệnh đề kéo theo $P \\Rightarrow Q$ được phát biểu dưới dạng: ``Nếu $P$ thì $Q$''. Do đó đáp án đúng là: ``Nếu {p_text} thì {q_text}''."""

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B1_NB010_MC_A_01(socau, dang=1):

    ds_boi_canh = [

        # Góc bù
        {
            "P": "hai góc $\\widehat{A}$ và $\\widehat{B}$ bù nhau",
            "P_hoa": "Hai góc $\\widehat{A}$ và $\\widehat{B}$ bù nhau",
            "Q": "tổng hai góc $\\widehat{A}$ và $\\widehat{B}$ bằng $180^{\\circ}$",
            "Q_hoa": "Tổng hai góc $\\widehat{A}$ và $\\widehat{B}$ bằng $180^{\\circ}$",
            "dao": "Nếu tổng hai góc $\\widehat{A}$ và $\\widehat{B}$ bằng $180^{\\circ}$ thì hai góc $\\widehat{A}$ và $\\widehat{B}$ bù nhau"
        },

        # Góc phụ
        {
            "P": "hai góc $\\widehat{M}$ và $\\widehat{N}$ phụ nhau",
            "P_hoa": "Hai góc $\\widehat{M}$ và $\\widehat{N}$ phụ nhau",
            "Q": "tổng hai góc $\\widehat{M}$ và $\\widehat{N}$ bằng $90^{\\circ}$",
            "Q_hoa": "Tổng hai góc $\\widehat{M}$ và $\\widehat{N}$ bằng $90^{\\circ}$",
            "dao": "Nếu tổng hai góc $\\widehat{M}$ và $\\widehat{N}$ bằng $90^{\\circ}$ thì hai góc $\\widehat{M}$ và $\\widehat{N}$ phụ nhau"
        },

        # Chia hết
        {
            "P": "$a$ là số chia hết cho $10$",
            "P_hoa": "$a$ là số chia hết cho $10$",
            "Q": "$a$ là số chia hết cho $5$",
            "Q_hoa": "$a$ là số chia hết cho $5$",
            "dao": "Nếu $a$ là số chia hết cho $5$ thì $a$ là số chia hết cho $10$"
        },

        {
            "P": "$a$ là số chia hết cho $6$",
            "P_hoa": "$a$ là số chia hết cho $6$",
            "Q": "$a$ là số chia hết cho $3$",
            "Q_hoa": "$a$ là số chia hết cho $3$",
            "dao": "Nếu $a$ là số chia hết cho $3$ thì $a$ là số chia hết cho $6$"
        },

        # Tam giác đều
        {
            "P": "một tam giác là tam giác đều",
            "P_hoa": "Một tam giác là tam giác đều",
            "Q": "tam giác đó có ba cạnh bằng nhau",
            "Q_hoa": "Tam giác đó có ba cạnh bằng nhau",
            "dao": "Nếu một tam giác có ba cạnh bằng nhau thì tam giác đó là tam giác đều"
        },

        # Hình vuông
        {
            "P": "một hình vuông",
            "P_hoa": "Một hình vuông",
            "Q": "hình đó có bốn góc vuông",
            "Q_hoa": "Hình đó có bốn góc vuông",
            "dao": "Nếu một hình có bốn góc vuông thì hình đó là hình vuông"
        },

        # Hình chữ nhật
        {
            "P": "một hình chữ nhật có bốn cạnh bằng nhau",
            "P_hoa": "Một hình chữ nhật có bốn cạnh bằng nhau",
            "Q": "hình đó là hình vuông",
            "Q_hoa": "Hình đó là hình vuông",
            "dao": "Nếu một hình là hình vuông thì hình đó là hình chữ nhật có bốn cạnh bằng nhau"
        },

        # Song song
        {
            "P": "hai đường thẳng cùng vuông góc với một đường thẳng thứ ba",
            "P_hoa": "Hai đường thẳng cùng vuông góc với một đường thẳng thứ ba",
            "Q": "hai đường thẳng đó song song với nhau",
            "Q_hoa": "Hai đường thẳng đó song song với nhau",
            "dao": "Nếu hai đường thẳng song song với nhau thì chúng cùng vuông góc với một đường thẳng thứ ba"
        },

        # Số nguyên tố
        {
            "P": "một số là số nguyên tố lớn hơn $2$",
            "P_hoa": "Một số là số nguyên tố lớn hơn $2$",
            "Q": "số đó là số lẻ",
            "Q_hoa": "Số đó là số lẻ",
            "dao": "Nếu một số là số lẻ thì số đó là số nguyên tố lớn hơn $2$"
        },

        # Số chính phương
        {
            "P": "một số là số chính phương",
            "P_hoa": "Một số là số chính phương",
            "Q": "căn bậc hai của số đó là số nguyên",
            "Q_hoa": "Căn bậc hai của số đó là số nguyên",
            "dao": "Nếu căn bậc hai của một số là số nguyên thì số đó là số chính phương"
        },

        # Parabol
        {
            "P": "hàm số có hệ số $a > 0$",
            "P_hoa": "Hàm số có hệ số $a > 0$",
            "Q": "đồ thị hàm số quay bề lõm lên trên",
            "Q_hoa": "Đồ thị hàm số quay bề lõm lên trên",
            "dao": "Nếu đồ thị hàm số quay bề lõm lên trên thì hệ số $a > 0$"
        },

        # Phương trình bậc nhất
        {
            "P": "phương trình có dạng $ax+b=0$ với $a \\ne 0$",
            "P_hoa": "Phương trình có dạng $ax+b=0$ với $a \\ne 0$",
            "Q": "phương trình có nghiệm duy nhất",
            "Q_hoa": "Phương trình có nghiệm duy nhất",
            "dao": "Nếu một phương trình có nghiệm duy nhất thì phương trình đó có dạng $ax+b=0$ với $a \\ne 0$"
        }
    ]

    # Khống chế số câu
    if socau > len(ds_boi_canh):
        socau = len(ds_boi_canh)

    gt = []
    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        if v not in gt:

            gt.append(v)

            dem += 1

    cauTN = ''

    for v in gt:

        P = v["P"]
        Q = v["Q"]
        dapso = v["dao"]

        debai = (
            f"""Hãy phát biểu mệnh đề đảo của mệnh đề ``Nếu {P} thì {Q}''. """
        )

        giai = (
            r"Mệnh đề đảo của mệnh đề $P \Rightarrow Q$ là mệnh đề $Q \Rightarrow P$."
        )

        dsnhieu = [

            f"Nếu không phải {P} thì không phải {Q}",

            f"Nếu {Q} thì không phải {P}",

            f"{v['P_hoa']} khi và chỉ khi {Q}"
        ]

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B1_NB010_MC_A_02(socau, dang=1):

    cac_cap_goc = [('A', 'B'), ('X', 'Y'), ('M', 'N'), ('P', 'Q'), ('C', 'D'), ('E', 'F'), ('H', 'K')]

    # ĐÃ SỬA: Sinh thẳng cấu hình ngẫu nhiên theo số lượng câu hỏi, bỏ qua vòng lặp check trùng gây treo máy
    gt = []
    for _ in range(socau):
        goc_cap = random.choice(cac_cap_goc)
        loai_tinh_chat = np.random.randint(0, 2)
        gt.append([goc_cap[0], goc_cap[1], loai_tinh_chat])

    cauTN = ''
    for v in gt:
        goc1, goc2, loai_tinh_chat = v[0], v[1], v[2]

        # SUA 29/09/2026 (co Lan): ve nao dung SAU chu "Neu" thi ve do phai
        # GOI TEN hai goc. Truoc day menh de dao ra kieu "Neu tong so do
        # cua CHUNG bang 90 do thi hai goc M va N phu nhau" - "chung" la ai
        # thi chua he duoc noi toi. Nay moi ve co hai cach viet:
        #   _ten : goi ten day du  (dung khi ve do dung sau "Neu")
        #   _tro : noi lai "hai goc do" / "chung" (dung sau "thi")
        cap = r"hai góc $\widehat{%s}$ và $\widehat{%s}$" % (goc1, goc2)
        if loai_tinh_chat == 0:
            dung_goc, sai_goc, k_dung, k_sai = "phụ nhau", "bù nhau", 90, 180
        else:
            dung_goc, sai_goc, k_dung, k_sai = "bù nhau", "phụ nhau", 180, 90
        khong_goc = "không " + dung_goc

        def tc_ten(tc):            # P goi ten: "hai goc M va N phu nhau"
            return "%s %s" % (cap, tc)

        def tc_tro(tc):            # P noi lai: "hai goc do phu nhau"
            return "hai góc đó %s" % tc

        def tong_ten(dk):          # Q goi ten: "tong so do cua hai goc M va N bang 90"
            return "tổng số đo của %s %s" % (cap, dk)

        def tong_tro(dk):          # Q noi lai: "tong so do cua chung bang 90"
            return "tổng số đo của chúng %s" % dk

        bang = r"bằng $%d^\circ$" % k_dung
        khac = r"khác $%d^\circ$" % k_dung
        bang_sai = r"bằng $%d^\circ$" % k_sai

        # Menh de goc P => Q: P dung sau "Neu" nen P goi ten.
        P_text, Q_text = tc_ten(dung_goc), tong_tro(bang)
        debai = f"""Hãy phát biểu mệnh đề đảo của mệnh đề: ``Nếu {P_text} thì {Q_text}''."""

        # Menh de dao Q => P: bay gio Q dung sau "Neu" nen Q goi ten.
        dapso = f"""Nếu {tong_ten(bang)} thì {tc_tro(dung_goc)}."""

        # Phuong an nhieu - cung quy tac goi ten nhu vay.
        dsnhieu = [
            f"""Nếu {tc_ten(khong_goc)} thì {tong_tro(khac)}.""",     # phu dinh
            f"""Nếu {tong_ten(khac)} thì {tc_tro(khong_goc)}.""",     # phan dao
            f"""Nếu {tong_ten(bang_sai)} thì {tc_tro(sai_goc)}.""",   # nham tinh chat
        ]

        giai = f"""Xét mệnh đề kéo theo đã cho có cấu trúc: ``Nếu $P$ thì $Q$'' (ký hiệu là $P \\Rightarrow Q$), trong đó:\\\\
        - $P$: ``{tc_ten(dung_goc)}''\\\\
        - $Q$: ``{tong_ten(bang)}''\\\\
        Theo định nghĩa, mệnh đề đảo của mệnh đề $P \\Rightarrow Q$ là mệnh đề $Q \\Rightarrow P$, phát biểu dưới dạng: ``Nếu $Q$ thì $P$''.\\\\
        Do đó, mệnh đề đảo của mệnh đề trên là: ``{dapso[:-1]}''. """

        cauTN += _MC_khong_cham(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B1_NB011_MC_A_01(socau, dang=1):

    ds_boi_canh = [

        # ================= TOÁN - SỐ HỌC =================

        {
            "P": "số tự nhiên $n$ chia hết cho $2$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $2$",
            "Q": "số tự nhiên $n$ có chữ số tận cùng là số chẵn",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng là số chẵn"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $3$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $3$",
            "Q": "tổng các chữ số của $n$ chia hết cho $3$",
            "Q_hoa": "Tổng các chữ số của $n$ chia hết cho $3$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $5$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $5$",
            "Q": "số tự nhiên $n$ có chữ số tận cùng bằng $0$ hoặc $5$",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng bằng $0$ hoặc $5$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $10$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $10$",
            "Q": "số tự nhiên $n$ có chữ số tận cùng bằng $0$",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng bằng $0$"
        },

        # ================= TOÁN - TAM GIÁC =================

        {
            "P": "tam giác $ABC$ là tam giác vuông",
            "P_hoa": "Tam giác $ABC$ là tam giác vuông",
            "Q": "tam giác $ABC$ có một góc bằng $90^{\\circ}$",
            "Q_hoa": "Tam giác $ABC$ có một góc bằng $90^{\\circ}$"
        },

        {
            "P": "tam giác $ABC$ là tam giác cân",
            "P_hoa": "Tam giác $ABC$ là tam giác cân",
            "Q": "tam giác $ABC$ có hai cạnh bằng nhau",
            "Q_hoa": "Tam giác $ABC$ có hai cạnh bằng nhau"
        },

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",
            "Q": "tam giác $ABC$ có ba cạnh bằng nhau",
            "Q_hoa": "Tam giác $ABC$ có ba cạnh bằng nhau"
        },

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",
            "Q": "tam giác $ABC$ có ba góc bằng $60^{\\circ}$",
            "Q_hoa": "Tam giác $ABC$ có ba góc bằng $60^{\\circ}$"
        },

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",
            "Q": "tam giác $ABC$ là tam giác cân",
            "Q_hoa": "Tam giác $ABC$ là tam giác cân"
        },

        # ================= TOÁN - TỨ GIÁC =================

        {
            "P": "tứ giác $ABCD$ là hình thang cân",
            "P_hoa": "Tứ giác $ABCD$ là hình thang cân",
            "Q": "tứ giác $ABCD$ là hình thang có hai cạnh bên bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ là hình thang có hai cạnh bên bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình thang",
            "P_hoa": "Tứ giác $ABCD$ là hình thang",
            "Q": "tứ giác $ABCD$ có một cặp cạnh đối song song",
            "Q_hoa": "Tứ giác $ABCD$ có một cặp cạnh đối song song"
        },

        {
            "P": "tứ giác $ABCD$ có hai cạnh đối diện song song",
            "P_hoa": "Tứ giác $ABCD$ có hai cạnh đối diện song song",
            "Q": "tứ giác $ABCD$ là hình thang",
            "Q_hoa": "Tứ giác $ABCD$ là hình thang"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",
            "Q": "tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",
            "Q": "tứ giác $ABCD$ là hình thoi có một góc vuông",
            "Q_hoa": "Tứ giác $ABCD$ là hình thoi có một góc vuông"
        },

        {
            "P": "tứ giác $ABCD$ là hình thang",
            "P_hoa": "Tứ giác $ABCD$ là hình thang",
            "Q": "tứ giác $ABCD$ có một cặp cạnh đối song song",
            "Q_hoa": "Tứ giác $ABCD$ có một cặp cạnh đối song song"
        },

        # ================= KHÁC =================

        {
            "P": "$a$ là số chính phương",
            "P_hoa": "$a$ là số chính phương",
            "Q": "căn bậc hai của số $a$ là số nguyên",
            "Q_hoa": "Căn bậc hai của số $a$ là số nguyên"
        },

        # ================= THỰC TẾ =================

        {
            "P": "học sinh $A$ đạt học lực giỏi",
            "P_hoa": "Học sinh $A$ đạt học lực giỏi",
            "Q": "điểm trung bình của học sinh $A$ từ $8{,}0$ trở lên",
            "Q_hoa": "Điểm trung bình của học sinh $A$ từ $8{,}0$ trở lên"
        },

        {
            "P": "nước đạt nhiệt độ $100^{\\circ}$C ở áp suất tiêu chuẩn",
            "P_hoa": "Nước đạt nhiệt độ $100^{\\circ}$C ở áp suất tiêu chuẩn",
            "Q": "nước bắt đầu sôi",
            "Q_hoa": "Nước bắt đầu sôi"
        },

        {
            "P": "anh Nam đủ $18$ tuổi",
            "P_hoa": "Anh Nam đủ $18$ tuổi",
            "Q": "anh Nam đủ tuổi công dân theo quy định",
            "Q_hoa": "Anh Nam đủ tuổi công dân theo quy định"
        },

        {
            "P": "thanh kim loại $AB$ bị nung nóng",
            "P_hoa": "Thanh kim loại $AB$ bị nung nóng",
            "Q": "thanh kim loại $AB$ nở ra",
            "Q_hoa": "Thanh kim loại $AB$ nở ra"
        },

        {
            "P": "học sinh $B$ vi phạm nội quy nghiêm trọng",
            "P_hoa": "Học sinh $B$ vi phạm nội quy nghiêm trọng",
            "Q": "học sinh $B$ bị xử lí kỉ luật",
            "Q_hoa": "Học sinh $B$ bị xử lí kỉ luật"
        },

        {
            "P": "số điện thoại $x$ nhận quá nhiều cuộc gọi quảng cáo",
            "P_hoa": "Số điện thoại $x$ nhận quá nhiều cuộc gọi quảng cáo",
            "Q": "người dùng có xu hướng chặn số điện thoại $x$",
            "Q_hoa": "Người dùng có xu hướng chặn số điện thoại $x$"
        },

        {
            "P": "trời có nhiều mây đen và độ ẩm không khí cao",
            "P_hoa": "Trời có nhiều mây đen và độ ẩm không khí cao",
            "Q": "khả năng xảy ra mưa lớn",
            "Q_hoa": "Khả năng xảy ra mưa lớn"
        },

        {
            "P": "cây xanh thực hiện quá trình quang hợp",
            "P_hoa": "Cây xanh thực hiện quá trình quang hợp",
            "Q": "khí ô-xi được giải phóng",
            "Q_hoa": "Khí ô-xi được giải phóng"
        },

        {
            "P": "quốc gia $X$ xảy ra lạm phát cao",
            "P_hoa": "Quốc gia $X$ xảy ra lạm phát cao",
            "Q": "giá hàng hóa tại quốc gia $X$ tăng nhanh",
            "Q_hoa": "Giá hàng hóa tại quốc gia $X$ tăng nhanh"
        },

        {
            "P": "anh Nam tập thể dục đều đặn",
            "P_hoa": "Anh Nam tập thể dục đều đặn",
            "Q": "sức khỏe của anh Nam được cải thiện",
            "Q_hoa": "Sức khỏe của anh Nam được cải thiện"
        }
    ]

    if socau > len(ds_boi_canh):
        socau = len(ds_boi_canh)

    gt = []
    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        if v not in gt:

            gt.append(v)

            dem += 1

    cauTN = ''

    for v in gt:

        P = v["P"]
        P_hoa = v["P_hoa"]
        Q = v["Q"]
        Q_hoa = v["Q_hoa"]

        debai = (
            f"""Cho hai mệnh đề sau:\\\\
            $P \\colon$ ``{P_hoa}'';\\\\
            $Q \\colon$ ``{Q_hoa}''.\\\\
            Hãy phát biểu mệnh đề $P \\Leftrightarrow Q$."""
        )

        dapso = random.choice([
            f"{P_hoa} khi và chỉ khi {Q}",
            f"{P_hoa} nếu và chỉ nếu {Q}",
            f"{Q_hoa} khi và chỉ khi {P}",
            f"{Q_hoa} nếu và chỉ nếu {P}"
        ])

        dsnhieu = [

            f"Nếu {P} thì {Q}",

            f"Nếu {Q} thì {P}",

            f"Vì {P} nên {Q}"
        ]

        giai = (
            r"Mệnh đề tương đương $P \Leftrightarrow Q$ được phát biểu dưới dạng ``$P$ khi và chỉ khi $Q$''."
        )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B1_NB013_MC_A_01(socau, dang=1):

    # =========================================================
    # HÀM PHỤ
    # =========================================================

    def doi_dau(dau):

        if dau == ">":
            return r"\leq"

        elif dau == "<":
            return r"\geq"

        elif dau == r"\geq":
            return "<"

        elif dau == r"\leq":
            return ">"

        elif dau == "=":
            return r"\ne"

        elif dau == r"\ne":
            return "="


    def doc_dau(dau):

        if dau == ">":
            return "lớn hơn"

        elif dau == "<":
            return "nhỏ hơn"

        elif dau == r"\geq":
            return "lớn hơn hoặc bằng"

        elif dau == r"\leq":
            return "nhỏ hơn hoặc bằng"

        elif dau == "=":
            return "bằng"

        elif dau == r"\ne":
            return "khác"


    def doi_thuoc(dau):

        if dau == r"\in":
            return r"\notin"

        elif dau == r"\notin":
            return r"\in"


    def doc_thuoc(dau):

        if dau == r"\in":
            return "thuộc"

        elif dau == r"\notin":
            return "không thuộc"


    ds_boi_canh = []

    # =========================================================
    # DẠNG 1
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall x\in \mathbb{{R}}, x^2 {dau} 0$',

            "dung": rf'Mọi số thực đều có bình phương {doc_dau(dau)} $0$',

            "nhieu": [

                rf'Tồn tại số thực mà bình phương của nó {doc_dau(dau)} $0$',

                rf'Mọi số thực đều có bình phương {doc_dau(doi_dau(dau))} $0$',

                rf'Tồn tại số thực mà bình phương của nó {doc_dau(doi_dau(dau))} $0$',

                rf'Có ít nhất một số thực có bình phương {doc_dau(dau)} $0$',

                rf'Mọi số thực đều có bình phương khác $0$'
            ]
        })

    # =========================================================
    # DẠNG 2
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall n\in \mathbb{{N}}, n^2 {dau} n$',

            "dung": rf'Mọi số tự nhiên đều có bình phương {doc_dau(dau)} chính nó',

            "nhieu": [

                rf'Tồn tại số tự nhiên mà bình phương của nó {doc_dau(dau)} chính nó',

                rf'Mọi số tự nhiên đều có bình phương {doc_dau(doi_dau(dau))} chính nó',

                rf'Tồn tại số tự nhiên mà bình phương của nó {doc_dau(doi_dau(dau))} chính nó',

                rf'Có ít nhất một số tự nhiên có bình phương {doc_dau(dau)} chính nó',

                rf'Mọi số tự nhiên đều có bình phương bằng chính nó'
            ]
        })

    # =========================================================
    # DẠNG 3
    # =========================================================

    for dau in ["=", r"\ne"]:

        ds_boi_canh.append({

            "latex": rf'$\exists x\in \mathbb{{R}}, \dfrac{{1}}{{x}} {dau} x$',

            "dung": rf'Tồn tại số thực mà nghịch đảo của nó {doc_dau(dau)} chính nó',

            "nhieu": [

                rf'Mọi số thực đều có nghịch đảo {doc_dau(dau)} chính nó',

                rf'Tồn tại số thực mà nghịch đảo của nó {doc_dau(doi_dau(dau))} chính nó',

                rf'Mọi số thực đều có nghịch đảo {doc_dau(doi_dau(dau))} chính nó',

                rf'Có ít nhất một số thực mà nghịch đảo của nó {doc_dau(dau)} chính nó',

                rf'Mọi số thực đều bằng nghịch đảo của chính nó'
            ]
        })

    # =========================================================
    # DẠNG 4
    # =========================================================

    for dau in [r"\in", r"\notin"]:

        ds_boi_canh.append({

            "latex": rf'$\exists n\in \mathbb{{N}}, \dfrac{{1}}{{n}} {dau} \mathbb{{N}}$',

            "dung": rf'Tồn tại số tự nhiên mà nghịch đảo của nó {doc_thuoc(dau)} tập số tự nhiên',

            "nhieu": [

                rf'Mọi số tự nhiên đều có nghịch đảo {doc_thuoc(dau)} tập số tự nhiên',

                rf'Tồn tại số tự nhiên mà nghịch đảo của nó {doc_thuoc(doi_thuoc(dau))} tập số tự nhiên',

                rf'Mọi số tự nhiên đều có nghịch đảo {doc_thuoc(doi_thuoc(dau))} tập số tự nhiên',

                rf'Có ít nhất một số tự nhiên mà nghịch đảo {doc_thuoc(dau)} tập số tự nhiên',

                rf'Mọi nghịch đảo của số tự nhiên đều là số tự nhiên'
            ]
        })

    # =========================================================
    # DẠNG 5
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall x\in \mathbb{{R}}, |x| {dau} 0$',

            "dung": rf'Mọi số thực đều có trị tuyệt đối {doc_dau(dau)} $0$',

            "nhieu": [

                rf'Tồn tại số thực mà trị tuyệt đối của nó {doc_dau(dau)} $0$',

                rf'Mọi số thực đều có trị tuyệt đối {doc_dau(doi_dau(dau))} $0$',

                rf'Tồn tại số thực mà trị tuyệt đối của nó {doc_dau(doi_dau(dau))} $0$',

                rf'Có ít nhất một số thực có trị tuyệt đối {doc_dau(dau)} $0$',

                rf'Mọi số thực đều có trị tuyệt đối khác $0$'
            ]
        })

    # =========================================================
    # DẠNG 6
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\exists x\in \mathbb{{Z}}, x^2 {dau} 0$',

            "dung": rf'Tồn tại số nguyên mà bình phương của nó {doc_dau(dau)} $0$',

            "nhieu": [

                rf'Mọi số nguyên đều có bình phương {doc_dau(dau)} $0$',

                rf'Tồn tại số nguyên mà bình phương của nó {doc_dau(doi_dau(dau))} $0$',

                rf'Mọi số nguyên đều có bình phương {doc_dau(doi_dau(dau))} $0$',

                rf'Có ít nhất một số nguyên mà bình phương {doc_dau(dau)} $0$',

                rf'Mọi số nguyên đều có bình phương khác $0$'
            ]
        })

    # =========================================================
    # KHỐNG CHẾ SỐ CÂU
    # =========================================================

    if socau > len(ds_boi_canh):

        socau = len(ds_boi_canh)

    gt = []

    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        if v not in gt:

            gt.append(v)

            dem += 1

    # =========================================================
    # SINH ĐỀ
    # =========================================================

    cauTN = ''

    for v in gt:

        P = v["latex"]

        dapso = v["dung"]

        dsnhieu = random.sample(v["nhieu"], 3)

        debai = (
            f"""Phát biểu bằng lời mệnh đề:
``{P}''."""
        )

        giai = (
            r"""Kí hiệu $\forall$ phát biểu là "mọi",
kí hiệu $\exists$ phát biểu là "tồn tại"."""
        )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    cauTN = cauTN.replace("--", "+").replace("-+", "-").replace("+-", "-").replace(".0", ",0").replace(".1",
                                                                                                           ",1").replace(
        ".2", ",2").replace(".3", ",3").replace(".4", ",4").replace(".5", ",5").replace(".6", ",6").replace(".7",
                                                                                                                ",7").replace(
        ".8", ",8").replace(".9", ",9")

    return cauTN


def L10_C1_B1_NB013_MC_B_01(socau, dang=1):

    # =========================================================
    # HÀM PHỤ
    # =========================================================

    def dao_dau(dau):

        if dau == ">":
            return r"\leq"

        elif dau == "<":
            return r"\geq"

        elif dau == r"\geq":
            return "<"

        elif dau == r"\leq":
            return ">"

        elif dau == "=":
            return r"\ne"

        elif dau == r"\ne":
            return "="


    def sp_dau(dau):

        if dau == ">":
            return "lớn hơn"

        elif dau == "<":
            return "nhỏ hơn"

        elif dau == r"\geq":
            return "lớn hơn hoặc bằng"

        elif dau == r"\leq":
            return "nhỏ hơn hoặc bằng"


    def sp_dau_text(dau):

        if dau == "=":
            return "bằng"

        elif dau == r"\ne":
            return "khác"


    def dao_thuoc(dau):

        if dau == r"\in":
            return r"\notin"

        elif dau == r"\notin":
            return r"\in"


    def sp_thuoc(dau):

        if dau == r"\in":
            return "thuộc"

        elif dau == r"\notin":
            return "không thuộc"

    # =========================================================
    # SINH DỮ LIỆU
    # =========================================================

    ds_boi_canh = []

    # =========================================================
    # DẠNG 1
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall x\in \mathbb{{R}}, x^2 {dau} 0$',

            "loi": rf'Mọi số thực đều có bình phương {sp_dau(dau)} $0$',

            "nhieu1": rf'$\exists x\in \mathbb{{R}}, x^2 {dau} 0$',

            "nhieu2": rf'$\forall x\in \mathbb{{R}}, x^2 {dao_dau(dau)} 0$',

            "nhieu3": rf'$\exists x\in \mathbb{{R}}, x^2 {dao_dau(dau)} 0$'
        })

    # =========================================================
    # DẠNG 2
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall n \in \mathbb{{N}}, n^2 {dau} n$',

            "loi": rf'Mọi số tự nhiên đều có bình phương {sp_dau(dau)} chính nó',

            "nhieu1": rf'$\forall n \in \mathbb{{N}}, n^2 {dao_dau(dau)} n$',

            "nhieu2": rf'$\exists n \in \mathbb{{N}}, n^2 {dau} n$',

            "nhieu3": rf'$\exists n \in \mathbb{{N}}, n^2 {dao_dau(dau)} n$'
        })

    # =========================================================
    # DẠNG 3
    # =========================================================

    for dau in ["=", r"\ne"]:

        ds_boi_canh.append({

            "latex": rf'$\exists x\in \mathbb{{R}}, \dfrac{{1}}{{x}} {dau} x$',

            "loi": rf'Tồn tại số thực mà nghịch đảo của nó {sp_dau_text(dau)} chính nó',

            "nhieu1": rf'$\forall x\in \mathbb{{R}}, \dfrac{{1}}{{x}} {dau} x$',

            "nhieu2": rf'$\exists x\in \mathbb{{R}}, \dfrac{{1}}{{x}} {dao_dau(dau)} x$',

            "nhieu3": rf'$\forall x\in \mathbb{{R}}, \dfrac{{1}}{{x}} {dao_dau(dau)} x$'
        })

    # =========================================================
    # DẠNG 4
    # =========================================================

    for dau in [r"\in", r"\notin"]:

        ds_boi_canh.append({

            "latex": rf'$\exists n\in \mathbb{{N}}, \dfrac{{1}}{{n}} {dau} \mathbb{{N}}$',

            "loi": rf'Tồn tại số tự nhiên mà nghịch đảo của nó {sp_thuoc(dau)} tập số tự nhiên',

            "nhieu1": rf'$\forall n\in \mathbb{{N}}, \dfrac{{1}}{{n}} {dau} \mathbb{{N}}$',

            "nhieu2": rf'$\exists n\in \mathbb{{N}}, \dfrac{{1}}{{n}} {dao_thuoc(dau)} \mathbb{{N}}$',

            "nhieu3": rf'$\forall n\in \mathbb{{N}}, \dfrac{{1}}{{n}} {dao_thuoc(dau)} \mathbb{{N}}$'
        })

    # =========================================================
    # DẠNG 5
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall x\in \mathbb{{R}}, |x| {dau} 0$',

            "loi": rf'Mọi số thực đều có trị tuyệt đối {sp_dau(dau)} $0$',

            "nhieu1": rf'$\exists x\in \mathbb{{R}}, |x| {dau} 0$',

            "nhieu2": rf'$\forall x\in \mathbb{{R}}, |x| {dao_dau(dau)} 0$',

            "nhieu3": rf'$\exists x\in \mathbb{{R}}, |x| {dao_dau(dau)} 0$'
        })

    # =========================================================
    # DẠNG 6
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\exists x\in \mathbb{{Z}}, x^2 {dau} 0$',

            "loi": rf'Tồn tại số nguyên mà bình phương của nó {sp_dau(dau)} $0$',

            "nhieu1": rf'$\forall x\in \mathbb{{Z}}, x^2 {dau} 0$',

            "nhieu2": rf'$\exists x\in \mathbb{{Z}}, x^2 {dao_dau(dau)} 0$',

            "nhieu3": rf'$\forall x\in \mathbb{{Z}}, x^2 {dao_dau(dau)} 0$'
        })

    # =========================================================
    # GIỚI HẠN SỐ CÂU
    # =========================================================

    if socau > len(ds_boi_canh):

        socau = len(ds_boi_canh)

    gt = []

    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        if v not in gt:

            gt.append(v)

            dem += 1

    # =========================================================
    # SINH ĐỀ
    # =========================================================

    cauTN = ''

    for v in gt:

        dapso = v["latex"]

        dsnhieu = [

            v["nhieu1"],

            v["nhieu2"],

            v["nhieu3"]
        ]

        debai = (
            f"""Chọn mệnh đề kí hiệu đúng cho mệnh đề:
``{v["loi"]}''."""
        )

        giai = (
            r"""Kí hiệu $\forall$ đọc là "mọi", kí hiệu $\exists$ đọc là "tồn tại"."""
        )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    cauTN = cauTN.replace("--", "+").replace("-+", "-").replace("+-", "-").replace(".0", ",0").replace(".1",
                                                                                                           ",1").replace(
        ".2", ",2").replace(".3", ",3").replace(".4", ",4").replace(".5", ",5").replace(".6", ",6").replace(".7",
                                                                                                                ",7").replace(
        ".8", ",8").replace(".9", ",9")

    return cauTN



def L10_C1_B1_TH014_MC_A_01(socau, dang=1):

    import random

    gt = []
    dem = 0

    while dem < socau:

        nhom = random.randint(1, 17)

        if nhom == 1:
            a = random.randint(1, 30)
            dapso = rf"$\forall n\in\mathbb Z,\ n^2+{a}\ge 0$"
            dsnhieu = [
                rf"$\forall n\in\mathbb Z,\ n^2+{a}<0$",
                rf"$\exists n\in\mathbb Z,\ n^2+{a}<0$",
                rf"$\forall n\in\mathbb Z,\ n^2+{a}=-1$"
            ]

        elif nhom == 2:
            a = random.randint(1, 30)
            dapso = rf"$\forall x\in\mathbb R,\ |x|+{a}>0$"
            dsnhieu = [
                rf"$\forall x\in\mathbb R,\ |x|+{a}<0$",
                rf"$\exists x\in\mathbb R,\ |x|+{a}<0$",
                rf"$\forall x\in\mathbb R,\ |x|+{a}=0$"
            ]

        elif nhom == 3:
            a = random.randint(1, 9)
            b = random.randint(-20, 20)
            dapso = rf"$\exists x\in\mathbb R,\ {a}x+({b})=0$"
            dsnhieu = [
                rf"$\forall x\in\mathbb R,\ {a}x+({b})=0$",
                rf"$\nexists x\in\mathbb R,\ {a}x+({b})=0$",
                rf"$\forall x\in\mathbb R,\ {a}x+({b})>0$"
            ]

        elif nhom == 4:
            # SUA 28/09/2026 - hai loi:
            #
            # 1) b lay trong range(1, a+1) nen b CO THE BANG a. Khi do dap
            #    so thanh "a|n => a|n" va phuong an nhieu thu nhat cung la
            #    "a|n => a|n" - trung het, math_type bao NhieuTrungError.
            #    Do duoc: hong 10/400 lan chay. b = 1 cung cho menh de
            #    tam thuong. Nay b la uoc THUC SU cua a, 1 < b < a.
            #
            # 2) Phuong an nhieu "ton tai n, a|n => b khong chia het n" la
            #    menh de DUNG, khong phai sai: chi can lay mot so n khong
            #    chia het cho a thi gia thiet sai nen phep keo theo dung,
            #    va menh de ton tai duoc thoa man. Nhu vay cau hoi co HAI
            #    dap an dung. Da thay bang menh de sai that.
            a = random.choice([x for x in range(4, 31)
                               if any(x % u == 0 for u in range(2, x))])
            b = random.choice([u for u in range(2, a) if a % u == 0])
            dapso = rf"$\forall n\in\mathbb Z,\ {a}\mid n\Rightarrow {b}\mid n$"
            dsnhieu = [
                rf"$\forall n\in\mathbb Z,\ {b}\mid n\Rightarrow {a}\mid n$",
                rf"$\forall n\in\mathbb Z,\ {a}\mid n\Rightarrow {b}\nmid n$",
                rf"$\forall n\in\mathbb Z,\ {a}\mid n\Rightarrow {a+1}\mid n$"
            ]

        elif nhom == 5:
            dapso = r"$\mathbb N\subset\mathbb Z$"
            dsnhieu = [r"$\mathbb Z\subset\mathbb N$", r"$\mathbb N=\varnothing$", r"$\mathbb N\not\subset\mathbb Z$"]

        elif nhom == 6:
            dapso = r"$\exists p\in\mathbb N,\ p\ \text{nguyên tố và chẵn}$"
            dsnhieu = [
                r"$\nexists p\in\mathbb N,\ p\ \text{nguyên tố và chẵn}$",
                r"$\forall p\in\mathbb N,\ p\ \text{nguyên tố}\Rightarrow p\ \text{chẵn}$",
                r"$\forall p\in\mathbb N,\ p\ \text{nguyên tố}\Rightarrow p\ \text{lẻ}$"
            ]

        elif nhom == 7:
            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{chẵn}\Rightarrow n^2\ \text{chẵn}$"
            dsnhieu = [
                r"$\forall n\in\mathbb Z,\ n\ \text{chẵn}\Rightarrow n^2\ \text{lẻ}$",
                r"$\exists n\in\mathbb Z,\ n\ \text{chẵn và }n^2\ \text{lẻ}$",
                r"$\forall n\in\mathbb Z,\ n^2\ \text{chẵn}\Rightarrow n\ \text{lẻ}$"
            ]

        elif nhom == 8:
            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{lẻ}\Rightarrow n^2\ \text{lẻ}$"
            dsnhieu = [
                r"$\forall n\in\mathbb Z,\ n\ \text{lẻ}\Rightarrow n^2\ \text{chẵn}$",
                r"$\exists n\in\mathbb Z,\ n\ \text{lẻ và }n^2\ \text{chẵn}$",
                r"$\forall n\in\mathbb Z,\ n^2\ \text{lẻ}\Rightarrow n\ \text{chẵn}$"
            ]

        elif nhom == 9:
            a = random.randint(1,20)
            dapso = rf"$\exists n\in\mathbb Z,\ {a}\mid n$"
            dsnhieu = [
                rf"$\forall n\in\mathbb Z,\ {a}\mid n$",
                rf"$\forall n\in\mathbb Z,\ {a}\nmid n$",
                rf"$\nexists n\in\mathbb Z,\ {a}\mid n$"
            ]

        elif nhom == 10:
            dapso = r"$\exists x\in\mathbb R,\ x<0$"
            dsnhieu = [r"$\forall x\in\mathbb R,\ x<0$", r"$\forall x\in\mathbb R,\ x>0$", r"$\nexists x\in\mathbb R,\ x<0$"]

        elif nhom == 11:
            dapso = r"$\exists x\in\mathbb R,\ |x|=0$"
            dsnhieu = [r"$\forall x\in\mathbb R,\ |x|=0$", r"$\nexists x\in\mathbb R,\ |x|=0$", r"$\forall x\in\mathbb R,\ |x|>0$"]

        elif nhom == 12:
            dapso = r"$\forall x\in\mathbb R,\ x=x$"
            dsnhieu = [r"$\forall x\in\mathbb R,\ x\ne x$", r"$\exists x\in\mathbb R,\ x\ne x$", r"$\forall x\in\mathbb R,\ x<x$"]

        elif nhom == 13:
            dapso = r"$\forall n\in\mathbb N,\ n+1>n$"
            dsnhieu = [r"$\forall n\in\mathbb N,\ n+1<n$", r"$\exists n\in\mathbb N,\ n+1<n$", r"$\forall n\in\mathbb N,\ n+1=n$"]

        elif nhom == 14:
            c = random.randint(1,20)
            dapso = rf"$\forall x\in\mathbb R,\ x^2+{c}>0$"
            dsnhieu = [rf"$\forall x\in\mathbb R,\ x^2+{c}<0$", rf"$\exists x\in\mathbb R,\ x^2+{c}<0$", rf"$\forall x\in\mathbb R,\ x^2+{c}=0$"]

        elif nhom == 15:
            dapso = r"$\exists n\in\mathbb N,\ n\ \text{chẵn}$"
            dsnhieu = [r"$\forall n\in\mathbb N,\ n\ \text{chẵn}$", r"$\nexists n\in\mathbb N,\ n\ \text{chẵn}$", r"$\forall n\in\mathbb N,\ n\ \text{lẻ}$"]

        elif nhom == 16:
            dapso = r"$\exists n\in\mathbb N,\ n\ \text{lẻ}$"
            dsnhieu = [r"$\forall n\in\mathbb N,\ n\ \text{lẻ}$", r"$\nexists n\in\mathbb N,\ n\ \text{lẻ}$", r"$\forall n\in\mathbb N,\ n\ \text{chẵn}$"]

        else:
            a = random.randint(101,500)
            dapso = rf"$\exists n\in\mathbb Z,\ n>{a}$"
            dsnhieu = [rf"$\forall n\in\mathbb Z,\ n>{a}$", rf"$\nexists n\in\mathbb Z,\ n>{a}$", rf"$\forall n\in\mathbb Z,\ n<{a}$"]

        khoa = dapso

        if khoa not in [u["dapso"] for u in gt]:
            gt.append({"dapso": dapso, "dsnhieu": dsnhieu})
            dem += 1

    cauTN = ""

    for v in gt:

        debai = "Trong các khẳng định sau, khẳng định nào đúng?"
        giai = "Khẳng định đúng là phương án đã chọn."

        cauTN += MC_SA_answer_text(
            debai,
            v["dapso"],
            v["dsnhieu"],
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B1_TH014_MC_B_01(socau, dang=1): ####### kiểm tra lại nội dung câu hỏi, các phương án.

    gt = []
    dem = 0

    while dem < socau:

        nhom = random.randint(1, 17)

        if nhom == 1:
            a = random.randint(1, 30)

            dapso = rf"$\forall n\in\mathbb Z,\ n^2+{a}<0$"

            dsnhieu = [
                rf"$\forall n\in\mathbb Z,\ n^2+{a}\ge0$",
                rf"$\exists n\in\mathbb Z,\ n^2+{a}>0$",
                rf"$\exists n\in\mathbb Z,\ n^2+{a}\ge {a}$"
            ]

        elif nhom == 2:

            a = random.randint(1, 30)

            dapso = rf"$\forall x\in\mathbb R,\ |x|+{a}<0$"

            dsnhieu = [

                rf"$\forall x\in\mathbb R,\ |x|+{a}>0$",

                rf"$\exists x\in\mathbb R,\ |x|+{a}={a}$",

                rf"$\exists x\in\mathbb R,\ |x|+{a}>{a}$"

            ]

        elif nhom == 3:

            a = random.randint(1, 9)

            b = random.randint(-20, 20)

            dapso = rf"$\forall x\in\mathbb R,\ {a}x+({b})=0$"

            dsnhieu = [

                rf"$\exists x\in\mathbb R,\ {a}x+({b})=0$",

                rf"$\exists x\in\mathbb R,\ {a}x+({b})\le0$",

                rf"$\exists x\in\mathbb R,\ {a}x+({b})\ge0$"

            ]

        elif nhom == 4:

            # SUA 28/09/2026 - cung mot loi nhu ham _01: b lay trong
            # range(1, a+1) nen CO THE BANG a. Khi do:
            #   - dap so thanh "a|n => a|n" la menh de DUNG, trong khi de
            #     hoi "khang dinh nao SAI" -> dap an bi sai han;
            #   - phuong an nhieu thu nhat cung la "a|n => a|n" -> trung
            #     voi dap so, math_type bao NhieuTrungError.
            # Nay b la uoc THUC SU cua a, 1 < b < a, khi do
            # "b|n => a|n" luon SAI - dung y do cua de.
            a = random.choice([x for x in range(4, 21)
                               if any(x % u == 0 for u in range(2, x))])

            b = random.choice([u for u in range(2, a) if a % u == 0])

            dapso = rf"$\forall n\in\mathbb Z,\ {b}\mid n\Rightarrow {a}\mid n$"

            dsnhieu = [

                rf"$\forall n\in\mathbb Z,\ {a}\mid n\Rightarrow {b}\mid n$",

                rf"$\exists n\in\mathbb Z,\ {a}\mid n$",

                rf"$\exists n\in\mathbb Z,\ {b}\mid n$"

            ]

        elif nhom == 5:

            dapso = r"$\forall p\in\mathbb N,\ p\ \text{nguyên tố}\Rightarrow p\ \text{chẵn}$"

            dsnhieu = [
                r"$\exists p\in\mathbb N,\ p\ \text{nguyên tố và chẵn}$",
                r"$2\ \text{là số nguyên tố}$",
                r"$3\ \text{là số nguyên tố}$"
            ]

        elif nhom == 6:

            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{chẵn}\Rightarrow n^2\ \text{lẻ}$"

            dsnhieu = [

                r"$\forall n\in\mathbb Z,\ n\ \text{chẵn}\Rightarrow n^2\ \text{chẵn}$",

                r"$4^2\ \text{là số chẵn}$",

                r"$2^2\ \text{là số chẵn}$"

            ]

        elif nhom == 7:

            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{lẻ}\Rightarrow n^2\ \text{chẵn}$"

            dsnhieu = [

                r"$\forall n\in\mathbb Z,\ n\ \text{lẻ}\Rightarrow n^2\ \text{lẻ}$",

                r"$3^2\ \text{là số lẻ}$",

                r"$5^2\ \text{là số lẻ}$"

            ]

        elif nhom == 8:

            a = random.randint(1, 20)

            dapso = rf"$\forall n\in\mathbb Z,\ {a}\nmid n$"

            dsnhieu = [

                rf"$\exists n\in\mathbb Z,\ {a}\mid n$",

                rf"${a}\mid 0$",

                rf"${a}\mid {a}$"

            ]

        elif nhom == 9:

            dapso = r"$\forall x\in\mathbb R,\ x<0$"

            dsnhieu = [

                r"$\exists x\in\mathbb R,\ x<0$",

                r"$-1<0$",

                r"$-100<0$"

            ]

        elif nhom == 10:

            dapso = r"$\nexists x\in\mathbb R,\ |x|=0$"

            dsnhieu = [

                r"$\exists x\in\mathbb R,\ |x|=0$",

                r"$|0|=0$",

                r"$0\in\mathbb R$"

            ]

        elif nhom == 11:

            dapso = r"$\forall x\in\mathbb R,\ x\ne x$"

            dsnhieu = [
                r"$\forall x\in\mathbb R,\ x=x$",
                r"$0=0$",
                r"$1=1$"
            ]

        elif nhom == 12:

            dapso = r"$\forall n\in\mathbb N,\ n+1<n$"

            dsnhieu = [
                r"$\forall n\in\mathbb N,\ n+1>n$",
                r"$1+1>1$",
                r"$10+1>10$"
            ]

        elif nhom == 13:
            c = random.randint(1, 20)

            dapso = rf"$\forall x\in\mathbb R,\ x^2+{c}<0$"

            dsnhieu = [
                rf"$\forall x\in\mathbb R,\ x^2+{c}>0$",
                rf"$0^2+{c}>0$",
                rf"$1^2+{c}>0$"
            ]

        elif nhom == 14:

            dapso = r"$\forall n\in\mathbb N,\ n\ \text{chẵn}$"

            dsnhieu = [
                r"$\exists n\in\mathbb N,\ n\ \text{chẵn}$",
                r"$2\ \text{là số chẵn}$",
                r"$4\ \text{là số chẵn}$"
            ]

        elif nhom == 15:

            dapso = r"$\forall n\in\mathbb N,\ n\ \text{lẻ}$"

            dsnhieu = [
                r"$\exists n\in\mathbb N,\ n\ \text{lẻ}$",
                r"$1\ \text{là số lẻ}$",
                r"$3\ \text{là số lẻ}$"
            ]

        else:
            a = random.randint(101, 500)

            dapso = rf"$\forall n\in\mathbb Z,\ n>{a}$"

            dsnhieu = [
                rf"$\exists n\in\mathbb Z,\ n>{a}$",
                rf"${a + 1}>{a}$",
                rf"${a + 100}>{a}$"
            ]
        khoa = dapso

        if khoa not in [u["dapso"] for u in gt]:
            gt.append({"dapso": dapso, "dsnhieu": dsnhieu})
            dem += 1

    cauTN = ""

    for v in gt:

        debai = "Trong các khẳng định sau, khẳng định nào \\textbf{sai}?"
        giai = "Khẳng định đúng là phương án đã chọn."

        cauTN += MC_SA_answer_text(
            debai,
            v["dapso"],
            v["dsnhieu"],
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_TF_A_01(socau, socot=1):

    import numpy as np

    gt = []
    dem = 0

    while dem < socau:

        huong_tich = np.random.choice([1, 2])

        nhom_C = np.random.choice([1, 2, 3])

        bien_the_D = np.random.choice([1, 2])

        v = [

            int(huong_tich),

            int(nhom_C),

            int(bien_the_D)
        ]

        if v not in gt:

            gt.append(v)

            dem += 1

    cauTF = ''

    for v in gt:

        huong_tich, nhom_C, bien_the_D = v

        debai = r"""Với $n \in \mathbb{N}$."""

        # =====================================================
        # NHÓM A
        # =====================================================

        list_A = [

            (

                r"""{\True Mệnh đề ``$n$ là một số không âm'' là một mệnh đề đúng}""",

                r"""Đúng. $\mathbb{N} = \{0;1;2;\ldots\}$ nên mọi $n \in \mathbb{N}$ đều thỏa $n \geq 0$."""
            ),

            (

                r"""{Mệnh đề ``$n$ là một số dương'' là một mệnh đề đúng}""",

                r"""Sai. Tại $n = 0$: số $0$ là số tự nhiên nhưng không phải số dương."""
            ),

            (

                r"""{Mệnh đề ``$n$ là một số âm'' là một mệnh đề đúng}""",

                r"""Sai. Không tồn tại số tự nhiên nào nhận giá trị âm."""
            ),

            (

                r"""{Mệnh đề ``$n$ là một số không dương'' là một mệnh đề đúng}""",

                r"""Sai. Chỉ có $n = 0$ không dương; mọi $n \geq 1$ đều là số dương."""
            ),

            ####################

            (

                r"""{Mệnh đề ``$n$ là một số không âm'' là một mệnh đề sai}""",

                r"""Sai. $\mathbb{N} = \{0;1;2;\ldots\}$ nên mọi $n \in \mathbb{N}$ đều thỏa $n \geq 0$."""
            ),

            (

                r"""{\True Mệnh đề ``$n$ là một số dương'' là một mệnh đề sai}""",

                r"""Đúng. Tại $n = 0$: số $0$ là số tự nhiên nhưng không phải số dương."""
            ),

            (

                r"""{\True Mệnh đề ``$n$ là một số âm'' là một mệnh đề sai}""",

                r"""Đúng. Không tồn tại số tự nhiên nào nhận giá trị âm."""
            ),

            (

                r"""{\True Mệnh đề ``$n$ là một số không dương'' là một mệnh đề sai}""",

                r"""Đúng. Chỉ có $n = 0$ không dương; mọi $n \geq 1$ đều là số dương."""
            )
        ]

        # =====================================================
        # NHÓM B
        # =====================================================

        if huong_tich == 1:

            list_B = [

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \mid n(n+1)$'' là mệnh đề đúng}""",

                    r"""Đúng. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, n(n+1)$ là số lẻ'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \mid n(n+1)$'' là mệnh đề đúng}""",

                    r"""Đúng. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, n(n+1)$ là số lẻ'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\,n(n+1)$ là số chẵn'' là mệnh đề đúng}""",

                    r"""Đúng. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \nmid n(n+1)$' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\,n(n+1)$ là số chẵn'' là mệnh đề đúng}""",

                    r"""Đúng. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \nmid n(n+1)$'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                ####################################

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \mid n(n+1)$'' là mệnh đề sai}""",

                    r"""Sai. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, n(n+1)$ là số lẻ'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \mid n(n+1)$'' là mệnh đề sai}""",

                    r"""Sai. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, n(n+1)$ là số lẻ'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\,n(n+1)$ là số chẵn'' là mệnh đề sai}""",

                    r"""Sai. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \nmid n(n+1)$' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\,n(n+1)$ là số chẵn'' là mệnh đề sai}""",

                    r"""Sai. $n$ và $n+1$ là hai số nguyên liên tiếp nên luôn có một số chẵn. Do đó $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \nmid n(n+1)$'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                )
            ]

            tich = r"n(n+1)"

            vd_nguyen_to = r"$n=1$: $1\cdot2=2$"

            vd_hop_so = r"$n=2$: $2\cdot3=6$"

            vd_cp_dung = r"$n=0$: $0\cdot1=0=0^2$"

            vd_cp_sai = r"$n=1$: $1\cdot2=2$"

            ly_giai_nt = (
                r"""Với mọi $n \geq 2$, cả $n$ và $n+1$ đều lớn hơn $1$ """
                r"""nên tích là hợp số."""
            )

        else:

            list_B = [

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \mid (n-1)n$'' là mệnh đề đúng}""",

                    r"""Đúng. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, (n-1)n$ là số lẻ'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \mid (n-1)n$'' là mệnh đề đúng}""",

                    r"""Đúng. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, (n-1)n$ là số lẻ'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, (n-1)n$ là số chẵn'' là mệnh đề đúng}""",

                    r"""Đúng. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \nmid (n-1)n$'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, (n-1)n$ là số chẵn'' là mệnh đề đúng}""",

                    r"""Đúng. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \nmid (n-1)n$'' là mệnh đề đúng}""",

                    r"""Sai. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                ##############===============

                    (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \mid (n-1)n$'' là mệnh đề sai}""",

                    r"""Sai. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, (n-1)n$ là số lẻ'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \mid (n-1)n$'' là mệnh đề sai}""",

                    r"""Sai. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, (n-1)n$ là số lẻ'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, (n-1)n$ là số chẵn'' là mệnh đề sai}""",

                    r"""Sai. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 2 \nmid (n-1)n$'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, (n-1)n$ là số chẵn'' là mệnh đề sai}""",

                    r"""Sai. Nếu $n=0$ thì $(n-1)n=0$ là số chẵn. Với $n \geq 1$, $(n-1)$ và $n$ là hai số nguyên liên tiếp nên tích chia hết cho $2$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 2 \nmid (n-1)n$'' là mệnh đề sai}""",

                    r"""Đúng. Tích hai số nguyên liên tiếp luôn là số chẵn."""
                )
            ]

            tich = r"(n-1)n"

            vd_nguyen_to = r"$n=2$: $1\cdot2=2$"

            vd_hop_so = r"$n=3$: $2\cdot3=6$"

            vd_cp_dung = r"$n=1$: $0\cdot1=0=0^2$"

            vd_cp_sai = r"$n=2$: $1\cdot2=2$"

            ly_giai_nt = (
                r"""Với mọi $n \geq 3$, cả $n-1$ và $n$ đều lớn hơn $1$ """
                r"""nên tích là hợp số."""
            )

        # =====================================================
        # NHÓM C
        # =====================================================

        if nhom_C == 1:

            list_C = [

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ là số chính phương'' là mệnh đề đúng}}""",

                    rf"""Đúng. {vd_cp_dung} là số chính phương."""
                ),

                (

                    rf"""{{Mệnh đề ``$\forall n \in \mathbb{{N}},\, {tich}$ là số chính phương'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số chính phương'' là mệnh đề đúng}}""",

                    rf"""Đúng. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{Mệnh đề ``$\forall n \in \mathbb{{N}}$ sao cho ${tich}$ là số chính phương'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{Mệnh đề ``$\exists n \in \mathbb{{N}},\, {tich}$ là số chính phương'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{Mệnh đề ``$\forall n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số chính phương'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_cp_sai} không phải là số chính phương."""
                ),

                ################# =======

                (

                    rf"""{{Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ là số chính phương'' là mệnh đề sai}}""",

                    rf"""Sai. {vd_cp_dung} là số chính phương."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\forall n \in \mathbb{{N}},\, {tich}$ là số chính phương'' là mệnh đề sai}}""",

                    rf"""Đúng. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số chính phương'' là mệnh đề sai}}""",

                    rf"""Sai. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\forall n \in \mathbb{{N}}$ sao cho ${tich}$ là số chính phương'' là mệnh đề sai}}""",

                    rf"""Đúng. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}},\, {tich}$ là số chính phương'' là mệnh đề sai}}""",

                    rf"""Đúng. {vd_cp_sai} không phải là số chính phương."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\forall n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số chính phương'' là mệnh đề sai}}""",

                    rf"""Đúng. {vd_cp_sai} không phải là số chính phương."""
                )

            ]

        elif nhom_C == 2:

            list_C = [

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ là số nguyên tố'' là mệnh đề đúng}}""",

                    rf"""Đúng. {vd_nguyen_to} là số nguyên tố. {ly_giai_nt}"""
                ),

                (

                    rf"""{{Mệnh đề ``$\forall n \in \mathbb{{N}},\, {tich}$ là số nguyên tố'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_hop_so} là hợp số."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số nguyên tố'' là mệnh đề đúng}}""",

                    rf"""Đúng. {vd_hop_so} là hợp số."""
                ),

                (

                    rf"""{{Mệnh đề ``$\forall n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số nguyên tố'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_nguyen_to} là số nguyên tố."""
                ),

                ########################################

                (

                    rf"""{{Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ là số nguyên tố'' là mệnh đề sai}}""",

                    rf"""Sai. {vd_nguyen_to} là số nguyên tố. {ly_giai_nt}"""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\forall n \in \mathbb{{N}},\, {tich}$ là số nguyên tố'' là mệnh đề sai}}""",

                    rf"""Đúng. {vd_hop_so} là hợp số."""
                ),

                (

                    rf"""{{Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số nguyên tố'' là mệnh đề sai}}""",

                    rf"""Sai. {vd_hop_so} là hợp số."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\forall n \in \mathbb{{N}}$ sao cho ${tich}$ không phải số nguyên tố'' là mệnh đề sai}}""",

                    rf"""Đúng. {vd_nguyen_to} là số nguyên tố."""
                )
            ]

        else:

            list_C = [

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ là hợp số'' là mệnh đề đúng}}""",

                    rf"""Đúng. {vd_hop_so} là hợp số."""
                ),

                (

                    rf"""{{Mệnh đề ``$\forall n \in \mathbb{{N}},\, {tich}$ là hợp số'' là mệnh đề đúng}}""",

                    rf"""Sai. {vd_nguyen_to} là số nguyên tố."""
                ),

                (

                    rf"""{{\True Mệnh đề ``$\exists n \in \mathbb{{N}}$ sao cho ${tich}$ không phải hợp số'' là mệnh đề đúng}}""",

                    rf"""Đúng. {vd_nguyen_to} là số nguyên tố."""
                )
            ]

        # =====================================================
        # NHÓM D
        # =====================================================

        list_D = [

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 6 \mid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Đúng. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 9 \mid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Sai. Với $n=2$ thì $n^3-n=6$, mà $6$ không chia hết cho $9$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 6 \mid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Đúng. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 9 \mid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Đúng. Với $n=0$ thì $n^3-n=0$, mà $0$ chia hết cho $9$."""
                ),
                ##########

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Sai. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Sai. Với $n=0$ thì $n^3-n=0$, mà $0$ chia hết cho $9$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Sai. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' là mệnh đề đúng}""",

                    r"""Đúng. Với $n=2$ thì $n^3-n=6$, mà $6$ không chia hết cho $9$."""
                ),

                ################################====================

                (

                    r"""{Mệnh đề ``$\forall n \in \mathbb{N},\, 6 \mid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Sai. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 9 \mid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Đúng. Với $n=2$ thì $n^3-n=6$, mà $6$ không chia hết cho $9$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 6 \mid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Sai. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 9 \mid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Sai. Với $n=0$ thì $n^3-n=0$, mà $0$ chia hết cho $9$."""
                ),
                ##########

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Đúng. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\forall n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Đúng. Với $n=0$ thì $n^3-n=0$, mà $0$ chia hết cho $9$."""
                ),

                (

                    r"""{\True Mệnh đề ``$\exists n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Đúng. Ta có $n^3-n=(n-1)n(n+1)$ là tích ba số nguyên liên tiếp nên luôn chia hết cho $2$ và $3$. Do đó chia hết cho $6$."""
                ),

                (

                    r"""{Mệnh đề ``$\exists n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' là mệnh đề sai}""",

                    r"""Sai. Với $n=2$ thì $n^3-n=6$, mà $6$ không chia hết cho $9$."""
                )

            ]

        # =====================================================
        # GHÉP
        # =====================================================

        ds_abcd = (

            list_A,

            list_B,

            list_C,

            list_D
        )

        cauTF += TF_baitoan_du(

            debai,

            ds_abcd,

            0,

            0,

            socot
        )

    return cauTF


def L10_C1_B1_NB015_MC_A_01(socau, dang=1):

    x = Symbol('x')
    y = Symbol('y')

    # ================= P => Q =================

    ds_boi_canh = [

        # ================= SỐ HỌC =================

        {
            "P": "số tự nhiên $n$ chia hết cho $6$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $6$",

            "Q": "số tự nhiên $n$ chia hết cho $2$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $2$"
        },

        {
            "P": "số tự nhiên $n$ có tổng các chữ số chia hết cho $3$",
            "P_hoa": "Số tự nhiên $n$ có tổng các chữ số chia hết cho $3$",

            "Q": "số tự nhiên $n$ chia hết cho $3$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $3$"
        },

        {
            "P": "số tự nhiên $n$ có chữ số tận cùng bằng $0$",
            "P_hoa": "Số tự nhiên $n$ có chữ số tận cùng bằng $0$",

            "Q": "số tự nhiên $n$ chia hết cho $5$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $5$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $10$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $10$",

            "Q": "số tự nhiên $n$ có chữ số tận cùng là số chẵn",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng là số chẵn"
        },

        # ================= TAM GIÁC =================

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",

            "Q": "tam giác $ABC$ là tam giác cân",
            "Q_hoa": "Tam giác $ABC$ là tam giác cân"
        },

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",

            "Q": "tam giác $ABC$ có hai góc bằng nhau",
            "Q_hoa": "Tam giác $ABC$ có hai góc bằng nhau"
        },

        {
            "P": "tam giác $ABC$ có một góc bằng $90^{\\circ}$",
            "P_hoa": "Tam giác $ABC$ có một góc bằng $90^{\\circ}$",

            "Q": "tam giác $ABC$ là tam giác vuông",
            "Q_hoa": "Tam giác $ABC$ là tam giác vuông"
        },

        {
            "P": "tam giác $ABC$ là tam giác cân và có một góc bằng $60^{\\circ}$",
            "P_hoa": "Tam giác $ABC$ là tam giác cân và có một góc bằng $60^{\\circ}$",

            "Q": "tam giác $ABC$ là tam giác đều",
            "Q_hoa": "Tam giác $ABC$ là tam giác đều"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "tứ giác $ABCD$ là hình thoi",
            "P_hoa": "Tứ giác $ABCD$ là hình thoi",

            "Q": "tứ giác $ABCD$ có hai đường chéo vuông góc",
            "Q_hoa": "Tứ giác $ABCD$ có hai đường chéo vuông góc"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình thoi có một góc vuông",
            "Q_hoa": "Tứ giác $ABCD$ là hình thoi có một góc vuông"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình chữ nhật",
            "Q_hoa": "Tứ giác $ABCD$ là hình chữ nhật"
        }
    ]

    if socau > 2 * len(ds_boi_canh):
        socau = 2 * len(ds_boi_canh)

    gt = []
    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        # 0: điều kiện cần
        # 1: điều kiện đủ

        kieu_hoi = np.random.randint(0, 2)

        data = [v, kieu_hoi]

        if data not in gt:

            gt.append(data)

            dem += 1

    cauTN = ''

    for data in gt:

        v = data[0]
        kieu_hoi = data[1]

        P = v["P"]
        P_hoa = v["P_hoa"]

        Q = v["Q"]
        Q_hoa = v["Q_hoa"]

        debai = (
            f"""Cho hai mệnh đề sau:\\\\
            $P \\colon$ ``{P_hoa}'';\\\\
            $Q \\colon$ ``{Q_hoa}''.\\\\
            Trong các phát biểu sau, phát biểu nào đúng với mệnh đề $P \\Rightarrow Q$?"""
        )

        # ================= ĐIỀU KIỆN CẦN =================

        if kieu_hoi == 0:

            dapso = f"{Q_hoa} là điều kiện cần để có {P}"

            dsnhieu = [

                f"{P_hoa} là điều kiện cần để có {Q}",

                f"{P_hoa} là điều kiện cần và đủ để có {Q}",

                f"{Q_hoa} là điều kiện đủ để có {P}"
            ]

            giai = (
                f"Mệnh đề $P \\Rightarrow Q$ được phát biểu dưới dạng "
                f"``{Q_hoa} là điều kiện cần để có {P}''."
            )

        # ================= ĐIỀU KIỆN ĐỦ =================

        else:

            dapso = f"{P_hoa} là điều kiện đủ để có {Q}"

            dsnhieu = [

                f"{Q_hoa} là điều kiện đủ để có {P}",

                f"{P_hoa} là điều kiện cần và đủ để có {Q}",

                f"{Q_hoa} là điều kiện cần để có {P}"
            ]

            giai = (
                f"Mệnh đề $P \\Rightarrow Q$ được phát biểu dưới dạng "
                f"``{P_hoa} là điều kiện đủ để có {Q}''."
            )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B1_NB015_MC_A_02(socau, dang=1):

    x = Symbol('x')
    y = Symbol('y')

    # ================= P <=> Q =================

    ds_boi_canh = [

        # ================= SỐ HỌC =================

        {
            "P": "số tự nhiên $n$ chia hết cho $2$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $2$",

            "Q": "số tự nhiên $n$ có chữ số tận cùng là số chẵn",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng là số chẵn"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $5$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $5$",

            "Q": "số tự nhiên $n$ có chữ số tận cùng bằng $0$ hoặc $5$",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng bằng $0$ hoặc $5$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $10$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $10$",

            "Q": "số tự nhiên $n$ có chữ số tận cùng bằng $0$",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng bằng $0$"
        },

        # ================= TAM GIÁC =================

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",

            "Q": "tam giác $ABC$ là tam giác cân và có một góc bằng $60^{\\circ}$",
            "Q_hoa": "Tam giác $ABC$ là tam giác cân và có một góc bằng $60^{\\circ}$"
        },

        {
            "P": "tam giác $ABC$ là tam giác vuông",
            "P_hoa": "Tam giác $ABC$ là tam giác vuông",

            "Q": "tam giác $ABC$ có một góc bằng $90^{\\circ}$",
            "Q_hoa": "Tam giác $ABC$ có một góc bằng $90^{\\circ}$"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình thoi có một góc vuông",
            "Q_hoa": "Tứ giác $ABCD$ là hình thoi có một góc vuông"
        }
    ]

    if socau > 2 * len(ds_boi_canh):
        socau = 2 * len(ds_boi_canh)

    gt = []
    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        # 0: điều kiện cần và đủ
        # 1: tương đương

        kieu_hoi = np.random.randint(0, 2)

        data = [v, kieu_hoi]

        if data not in gt:

            gt.append(data)

            dem += 1

    cauTN = ''

    for data in gt:

        v = data[0]
        kieu_hoi = data[1]

        P = v["P"]
        P_hoa = v["P_hoa"]

        Q = v["Q"]
        Q_hoa = v["Q_hoa"]

        debai = (
            f"""Cho hai mệnh đề sau:\\\\
            $P \\colon$ ``{P_hoa}'';\\\\
            $Q \\colon$ ``{Q_hoa}''.\\\\
            Trong các phát biểu sau, phát biểu nào đúng với mệnh đề $P \\Leftrightarrow Q$?"""
        )

        # ================= ĐIỀU KIỆN CẦN VÀ ĐỦ =================

        if kieu_hoi == 0:

            dapso = f"{P_hoa} là điều kiện cần và đủ để có {Q}"

            dsnhieu = [

                f"{P_hoa} là điều kiện cần để có {Q}",

                f"{P_hoa} là điều kiện đủ để có {Q}",

                f"{Q_hoa} là điều kiện đủ để có {P}"
            ]

            giai = (
                f"Mệnh đề $P \\Leftrightarrow Q$ được phát biểu dưới dạng "
                f"``{P_hoa} là điều kiện cần và đủ để có {Q}''."
            )

        # ================= TƯƠNG ĐƯƠNG =================

        else:

            dapso = f"{P_hoa} tương đương với {Q}"

            dsnhieu = [

                f"{P_hoa} là điều kiện cần để có {Q}",

                f"{P_hoa} là điều kiện đủ để có {Q}",

                f"{Q_hoa} là điều kiện đủ để có {P}"
            ]

            giai = (
                f"Mệnh đề $P \\Leftrightarrow Q$ được phát biểu dưới dạng "
                f"``{P_hoa} tương đương với {Q}''."
            )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B1_NB015_MC_B_01(socau, dang=1):

    x = Symbol('x')
    y = Symbol('y')

    ds_boi_canh = [

        # ================= SỐ HỌC =================

        {
            "P": "số tự nhiên $n$ chia hết cho $6$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $6$",

            "Q": "số tự nhiên $n$ chia hết cho $2$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $2$"
        },

        {
            "P": "số tự nhiên $n$ có tổng các chữ số chia hết cho $3$",
            "P_hoa": "Số tự nhiên $n$ có tổng các chữ số chia hết cho $3$",

            "Q": "số tự nhiên $n$ chia hết cho $3$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $3$"
        },

        {
            "P": "số tự nhiên $n$ có chữ số tận cùng bằng $0$",
            "P_hoa": "Số tự nhiên $n$ có chữ số tận cùng bằng $0$",

            "Q": "số tự nhiên $n$ chia hết cho $5$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $5$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $10$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $10$",

            "Q": "số tự nhiên $n$ có chữ số tận cùng là số chẵn",
            "Q_hoa": "Số tự nhiên $n$ có chữ số tận cùng là số chẵn"
        },

        # ================= TAM GIÁC =================

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",

            "Q": "tam giác $ABC$ là tam giác cân",
            "Q_hoa": "Tam giác $ABC$ là tam giác cân"
        },

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",

            "Q": "tam giác $ABC$ có hai góc bằng nhau",
            "Q_hoa": "Tam giác $ABC$ có hai góc bằng nhau"
        },

        {
            "P": "tam giác $ABC$ có một góc bằng $90^{\\circ}$",
            "P_hoa": "Tam giác $ABC$ có một góc bằng $90^{\\circ}$",

            "Q": "tam giác $ABC$ là tam giác vuông",
            "Q_hoa": "Tam giác $ABC$ là tam giác vuông"
        },

        {
            "P": "tam giác $ABC$ là tam giác cân và có một góc bằng $60^{\\circ}$",
            "P_hoa": "Tam giác $ABC$ là tam giác cân và có một góc bằng $60^{\\circ}$",

            "Q": "tam giác $ABC$ là tam giác đều",
            "Q_hoa": "Tam giác $ABC$ là tam giác đều"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "tứ giác $ABCD$ là hình thoi",
            "P_hoa": "Tứ giác $ABCD$ là hình thoi",

            "Q": "tứ giác $ABCD$ có hai đường chéo vuông góc",
            "Q_hoa": "Tứ giác $ABCD$ có hai đường chéo vuông góc"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình thoi có một góc vuông",
            "Q_hoa": "Tứ giác $ABCD$ là hình thoi có một góc vuông"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ là hình chữ nhật có hai cạnh kề bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình chữ nhật",
            "Q_hoa": "Tứ giác $ABCD$ là hình chữ nhật"
        },
        # ================= SỐ HỌC =================

        {
            "P": "số tự nhiên $n$ chia hết cho $12$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $12$",

            "Q": "số tự nhiên $n$ chia hết cho $3$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $3$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $12$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $12$",

            "Q": "số tự nhiên $n$ chia hết cho $4$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $4$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $15$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $15$",

            "Q": "số tự nhiên $n$ chia hết cho $5$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $5$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $18$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $18$",

            "Q": "số tự nhiên $n$ chia hết cho $9$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $9$"
        },

        {
            "P": "số tự nhiên $n$ có chữ số tận cùng là $5$",
            "P_hoa": "Số tự nhiên $n$ có chữ số tận cùng là $5$",

            "Q": "số tự nhiên $n$ chia hết cho $5$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $5$"
        },

        {
            "P": "số tự nhiên $n$ chia hết cho $8$",
            "P_hoa": "Số tự nhiên $n$ chia hết cho $8$",

            "Q": "số tự nhiên $n$ chia hết cho $2$",
            "Q_hoa": "Số tự nhiên $n$ chia hết cho $2$"
        },

        # ================= TAM GIÁC =================

        {
            "P": "tam giác $ABC$ là tam giác vuông cân",
            "P_hoa": "Tam giác $ABC$ là tam giác vuông cân",

            "Q": "tam giác $ABC$ là tam giác cân",
            "Q_hoa": "Tam giác $ABC$ là tam giác cân"
        },

        {
            "P": "tam giác $ABC$ là tam giác vuông cân",
            "P_hoa": "Tam giác $ABC$ là tam giác vuông cân",

            "Q": "tam giác $ABC$ là tam giác vuông",
            "Q_hoa": "Tam giác $ABC$ là tam giác vuông"
        },

        {
            "P": "tam giác $ABC$ là tam giác đều",
            "P_hoa": "Tam giác $ABC$ là tam giác đều",

            "Q": "tam giác $ABC$ có ba cạnh bằng nhau",
            "Q_hoa": "Tam giác $ABC$ có ba cạnh bằng nhau"
        },

        {
            "P": "tam giác $ABC$ có ba cạnh bằng nhau",
            "P_hoa": "Tam giác $ABC$ có ba cạnh bằng nhau",

            "Q": "tam giác $ABC$ là tam giác đều",
            "Q_hoa": "Tam giác $ABC$ là tam giác đều"
        },

        {
            "P": "tam giác $ABC$ là tam giác cân",
            "P_hoa": "Tam giác $ABC$ là tam giác cân",

            "Q": "tam giác $ABC$ có hai cạnh bằng nhau",
            "Q_hoa": "Tam giác $ABC$ có hai cạnh bằng nhau"
        },

        {
            "P": "tam giác $ABC$ là tam giác vuông",
            "P_hoa": "Tam giác $ABC$ là tam giác vuông",

            "Q": "tam giác $ABC$ có một góc bằng $90^{\\circ}$",
            "Q_hoa": "Tam giác $ABC$ có một góc bằng $90^{\\circ}$"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ có bốn cạnh bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ có bốn cạnh bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ có hai đường chéo bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ có hai đường chéo bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ có hai đường chéo vuông góc",
            "Q_hoa": "Tứ giác $ABCD$ có hai đường chéo vuông góc"
        },

        {
            "P": "tứ giác $ABCD$ là hình chữ nhật",
            "P_hoa": "Tứ giác $ABCD$ là hình chữ nhật",

            "Q": "tứ giác $ABCD$ có bốn góc vuông",
            "Q_hoa": "Tứ giác $ABCD$ có bốn góc vuông"
        },

        {
            "P": "tứ giác $ABCD$ là hình thoi",
            "P_hoa": "Tứ giác $ABCD$ là hình thoi",

            "Q": "tứ giác $ABCD$ có bốn cạnh bằng nhau",
            "Q_hoa": "Tứ giác $ABCD$ có bốn cạnh bằng nhau"
        },

        {
            "P": "tứ giác $ABCD$ là hình bình hành",
            "P_hoa": "Tứ giác $ABCD$ là hình bình hành",

            "Q": "tứ giác $ABCD$ có các cạnh đối song song",
            "Q_hoa": "Tứ giác $ABCD$ có các cạnh đối song song"
        },

        {
            "P": "tứ giác $ABCD$ là hình chữ nhật",
            "P_hoa": "Tứ giác $ABCD$ là hình chữ nhật",

            "Q": "tứ giác $ABCD$ là hình bình hành",
            "Q_hoa": "Tứ giác $ABCD$ là hình bình hành"
        },

        {
            "P": "tứ giác $ABCD$ là hình vuông",
            "P_hoa": "Tứ giác $ABCD$ là hình vuông",

            "Q": "tứ giác $ABCD$ là hình bình hành",
            "Q_hoa": "Tứ giác $ABCD$ là hình bình hành"
        }
    ]

    if socau > 2 * len(ds_boi_canh):
        socau = 2 * len(ds_boi_canh)

    gt = []
    dem = len(gt)

    while dem < socau:

        v = random.choice(ds_boi_canh)

        # 0: giả thiết
        # 1: kết luận

        kieu_hoi = np.random.randint(0, 2)

        data = [v, kieu_hoi]

        if data not in gt:

            gt.append(data)

            dem += 1

    cauTN = ''

    for data in gt:

        v = data[0]
        kieu_hoi = data[1]

        P = v["P"]
        P_hoa = v["P_hoa"]

        Q = v["Q"]
        Q_hoa = v["Q_hoa"]

        debai = (
            f"""Cho định lí sau:\\\\
            ``Nếu {P} thì {Q}''.\\\\
            Trong các mệnh đề sau, mệnh đề nào là """
        )

        # ================= GIẢ THIẾT =================

        if kieu_hoi == 0:

            debai += "giả thiết của định lí đã cho?"

            dapso = P_hoa

            dsnhieu = [

                Q_hoa,

                f"Nếu {Q} thì {P}",

                f"{P_hoa} và {Q.lower()}"
            ]

            giai = (
                f"Trong mệnh đề ``Nếu {P} thì {Q}'', "
                f"mệnh đề đứng sau từ ``Nếu'' là giả thiết."
            )

        # ================= KẾT LUẬN =================

        else:

            debai += "kết luận của định lí đã cho?"

            dapso = Q_hoa

            dsnhieu = [

                P_hoa,

                f"Nếu {Q} thì {P}",

                f"{P_hoa} và {Q.lower()}"
            ]

            giai = (
                f"Trong định lí ``Nếu {P} thì {Q}'', "
                f"mệnh đề đứng sau từ ``thì'' là kết luận."
            )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B2_NB017_MC_A_01(socau, dang=1):
    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:

        A_list = []

        # Tập hợp gồm 3 đến 5 phần tử
        k = np.random.randint(3, 6)

        for i in range(0, k):

            a_val = np.random.randint(-12, 13)

            while a_val in A_list:
                a_val = np.random.randint(-12, 13)

            A_list.append(a_val)

        # Sắp xếp tăng dần cho đẹp
        A_list.sort()

        v = tuple(A_list)

        if v not in gt:

            gt.append(v)

            dem += 1

    cauTN = ''

    for v in gt:

        A_list = list(v)

        # =====================================================
        # CHỌN KIỂU ĐÁP ÁN SAI
        # =====================================================

        # 0: phần tử đơn
        # 1: tập chứa phần tử ngoài A
        # 2: tập nhiều phần tử có 1 phần tử ngoài A

        kieu_sai = np.random.randint(0, 3)

        # =====================================================
        # TẠO PHẦN TỬ NGOÀI A
        # =====================================================

        ngoai = np.random.randint(-12, 13)

        while ngoai in A_list:
            ngoai = np.random.randint(-12, 13)

        # =====================================================
        # TẠO ĐÁP ÁN ĐÚNG
        # =====================================================

        if kieu_sai == 0:

            # Đáp án là phần tử đơn

            idx_choice = np.random.randint(0, len(A_list))

            pt_thuoc = A_list[idx_choice]

            dapso = f"""${pt_thuoc}$"""

            giai = (
                f"Ký hiệu tập con phải dùng ngoặc nhọn hoặc ký hiệu tập rỗng.\\\\"
                f"Vì ${pt_thuoc}$ chỉ là một phần tử thuộc tập hợp $A$ nên ta có "
                f"${pt_thuoc} \\in A$, không phải ${pt_thuoc} \\subset A$.\\\\"
                f"Do đó, phương án ${pt_thuoc}$ không phải là tập con của $A$."
            )

        elif kieu_sai == 1:

            # Đáp án là tập một phần tử ngoài A

            dapso = f"""$\\left\\{{ {ngoai} \\right\\}}$"""

            giai = (
                f"Ta có ${ngoai} \\notin A$ nên "
                f"$\\left\\{{ {ngoai} \\right\\}}$ không phải là tập con của $A$."
            )

        else:

            # Đáp án là tập nhiều phần tử chứa phần tử ngoài A

            idx1 = np.random.randint(0, len(A_list))

            pt1 = A_list[idx1]

            # Viet theo thu tu tang dan, cach nhau boi dau ";" nhu tap A
            nho, lon = sorted([pt1, ngoai])

            dapso = f"""$\\left\\{{ {nho}; {lon} \\right\\}}$"""

            giai = (
                f"Ta có ${ngoai} \\notin A$ nên "
                f"$\\left\\{{ {nho}; {lon} \\right\\}}$ không phải là tập con của $A$."
            )

        # =====================================================
        # TẠO CÁC PHƯƠNG ÁN NHIỄU ĐÚNG
        # =====================================================

        # Nhiễu 1: tập rỗng
        nhieu1 = f"""$\\varnothing$"""

        # Nhiễu 2: tập 1 phần tử thuộc A
        idx2 = np.random.randint(0, len(A_list))

        pt2 = A_list[idx2]

        nhieu2 = f"""$\\left\\{{ {pt2} \\right\\}}$"""

        # Nhiễu 3: tập 2 phần tử thuộc A
        idx3, idx4 = random.sample(range(len(A_list)), 2)

        pt3 = A_list[idx3]
        pt4 = A_list[idx4]

        if pt3 > pt4:
            pt3, pt4 = pt4, pt3

        nhieu3 = f"""$\\left\\{{ {pt3}; {pt4} \\right\\}}$"""

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        # =====================================================
        # HIỂN THỊ TẬP HỢP A
        # =====================================================

        A_latex = (
            f"\\left\\{{ "
            + "; ".join(map(str, A_list))
            + " \\right\\}"
        )

        # =====================================================
        # TẠO ĐỀ
        # =====================================================

        # SUA 29/09/2026 (co Lan bao loi): hai cach hoi cu "Tim phuong an sai
        # trong cac khang dinh sau" / "phuong an nao khong dung?" lai dua ra
        # cac TAP HOP tran (khong phai khang dinh) -> cau vo nghia. Nay ca
        # 3 cach hoi deu hoi cung mot y: phuong an nao KHONG la tap con cua A.
        cach_hoi = np.random.randint(0, 3)

        if cach_hoi == 0:

            debai = (
                f"""Trong các phương án sau, phương án nào """
                f"""\\textbf{{không}} phải là tập con của tập hợp """
                f"""$A = {A_latex}$?"""
            )

        elif cach_hoi == 1:

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Trong các phương án sau, phương án nào """
                f"""\\textbf{{không}} là tập con của $A$?"""
            )

        elif cach_hoi == 2:

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Tìm phương án \\textbf{{không}} phải là tập con của $A$."""
            )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B2_NB017_MC_D_01(socau, dang=1):

    x = Symbol('x')
    y = Symbol('y')

    bang_chu_cai = [
        'a', 'b', 'c', 'd', 'e',
        'm', 'n', 'p', 'q',
        'x', 'y', 'z',
        'u', 'v', 't'
    ]

    gt = []
    dem = len(gt)

    while dem < socau:

        # =====================================================
        # SINH TẬP HỢP A
        # =====================================================

        k = np.random.randint(2, 5)

        A_list = list(
            np.random.choice(
                bang_chu_cai,
                size=k,
                replace=False
            )
        )

        A_list.sort()

        v = tuple(A_list)

        if v not in gt:

            gt.append(v)

            dem += 1

    cauTN = ''

    for v in gt:

        A_list = list(v)

        # =====================================================
        # CHỌN PHẦN TỬ THUỘC A LÀM ĐÁP ÁN
        # =====================================================

        idx_choice = np.random.randint(0, len(A_list))

        pt_thuoc = A_list[idx_choice]

        # =====================================================
        # TẠO NHIỄU
        # =====================================================

        # tập rỗng
        nhieu1 = "$\\varnothing$"

        # tập một phần tử
        idx2 = np.random.randint(0, len(A_list))

        while idx2 == idx_choice and len(A_list) > 1:
            idx2 = np.random.randint(0, len(A_list))

        pt2 = A_list[idx2]

        nhieu2 = (
            f"$\\left\\{{ {pt2} \\right\\}}$"
        )

        # tập nhiều phần tử
        if len(A_list) >= 3:

            idx3 = random.sample(range(len(A_list)), 2)

            a = A_list[idx3[0]]
            b = A_list[idx3[1]]

            if a > b:
                a, b = b, a

            nhieu3 = (
                f"$\\left\\{{ {a}; {b} \\right\\}}$"
            )

        else:

            nhieu3 = (
                f"$\\left\\{{ "
                + "; ".join(A_list)
                + " \\right\\}$"
            )

        dsnhieu = [nhieu1, nhieu2, nhieu3]

        # =====================================================
        # HIỂN THỊ TẬP A
        # =====================================================

        A_elements_str = "; ".join(A_list)

        A_latex = (
            f"\\left\\{{ "
            + A_elements_str
            + " \\right\\}"
        )

        # =====================================================
        # ĐỀ BÀI
        # =====================================================

        cach_hoi = np.random.randint(0, 3)

        if cach_hoi == 0:

            debai = (
                f"""Trong các phương án sau, """
                f"""phương án nào \\textbf{{không}} """
                f"""phải là tập con của tập hợp """
                f"""$A = {A_latex}$?"""
            )

        elif cach_hoi == 1:

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Trong các phương án sau, """
                f"""phương án nào \\textbf{{không}} là tập con của $A$?"""
            )

        else:

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Tìm phương án \\textbf{{không}} phải là tập con của $A$."""
            )
        # =====================================================
        # ĐÁP ÁN
        # =====================================================

        dapso = f"${pt_thuoc}$"

        # =====================================================
        # LỜI GIẢI
        # =====================================================

        giai = (
            f"${pt_thuoc}$ là một phần tử thuộc tập hợp $A$, "
            f"tức là ${pt_thuoc} \\in A$.\\\\"
            f"Để biểu diễn tập con, ta phải dùng "
            f"ngoặc nhọn hoặc ký hiệu tập rỗng.\\\\"
            f"Ví dụ: "
            f"$\\left\\{{ {pt_thuoc} \\right\\}} \\subset A$.\\\\"
            f"Do đó, phương án ${pt_thuoc}$ "
            f"không phải là tập con của $A$."
        )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B2_NB017_MC_B_01(socau, dang=1):

    x = Symbol('x')
    y = Symbol('y')

    gt = []
    dem = len(gt)

    while dem < socau:

        # =====================================================
        # TẠO TẬP HỢP A
        # =====================================================

        A_list = []

        k = np.random.randint(4, 7)

        for i in range(k):

            a_val = np.random.randint(-12, 13)

            while a_val in A_list:

                a_val = np.random.randint(-12, 13)

            A_list.append(a_val)

        A_list.sort()

        # =====================================================
        # TẠO CÁC PHẦN TỬ KHÁC NHAU
        # =====================================================

        pt1, pt2, pt3, pt4 = random.sample(A_list, 4)

        # =====================================================
        # KHẲNG ĐỊNH CHỨA RỖNG
        # =====================================================

        kh_rong = random.choice([

            (
                f"$\\varnothing \\in A$",

                False,

                f"$A$ không chứa phần tử $\\varnothing$."
            ),

            (
                f"$\\varnothing \\subset A$",

                True,

                f"Tập rỗng là tập con của mọi tập hợp."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\in A$",

                False,

                f"$A$ không chứa phần tử "
                f"$\\left\\{{ \\varnothing \\right\\}}$."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$",

                False,

                f"Muốn "
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$ "
                f"thì cần $\\varnothing \\in A$."
            )
        ])

        # =====================================================
        # DANH SÁCH KHẲNG ĐỊNH THƯỜNG
        # =====================================================

        ds_khangdinh = [

            (
                f"${pt1} \\in A$",

                True,

                f"Vì ${pt1}$ là phần tử của $A$ nên "
                f"${pt1} \\in A$."
            ),

            (
                f"${pt2} \\subset A$",

                False,

                f"${pt2}$ là phần tử nên không dùng kí hiệu "
                f"$\\subset$."
            ),

            (
                f"$\\left\\{{ {pt3} \\right\\}} \\in A$",

                False,

                f"$A$ không chứa phần tử "
                f"$\\left\\{{ {pt3} \\right\\}}$."
            ),

            (
                f"$\\left\\{{ {pt4} \\right\\}} \\subset A$",

                True,

                f"Mọi phần tử của "
                f"$\\left\\{{ {pt4} \\right\\}}$ đều thuộc $A$."
            )
        ]

        # =====================================================
        # CHỌN 3 KHẲNG ĐỊNH THƯỜNG
        # =====================================================

        ds_thuong = random.sample(ds_khangdinh, 3)

        # =====================================================
        # THÊM KHẲNG ĐỊNH RỖNG
        # =====================================================

        ds_chon = ds_thuong + [kh_rong]

        random.shuffle(ds_chon)

        # =====================================================
        # HỎI ĐÚNG HAY SAI
        # =====================================================

        hoi_dung = np.random.randint(0, 2)

        # =====================================================
        # DATA TRÁNH TRÙNG
        # =====================================================

        data = [

            tuple(A_list),

            tuple(
                (x[0], x[1], x[2]) for x in ds_chon
            ),

            hoi_dung
        ]

        if data not in gt:

            gt.append(data)

            dem += 1

    # =====================================================
    # SINH ĐỀ
    # =====================================================

    cauTN = ''

    for data in gt:

        A_list = list(data[0])

        ds_chon = list(data[1])

        hoi_dung = data[2]

        # =====================================================
        # ĐẾM
        # =====================================================

        so_dung = sum(1 for x in ds_chon if x[1])

        so_sai = 4 - so_dung

        # =====================================================
        # HIỂN THỊ TẬP HỢP
        # =====================================================

        A_latex = (
            "\\left\\{ "
            + "; ".join(map(str, A_list))
            + " \\right\\}"
        )

        # =====================================================
        # TẠO ĐỀ
        # =====================================================

        if hoi_dung == 0:

            dapso = f"${so_dung}$"

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Trong các khẳng định sau, có bao nhiêu khẳng định đúng?"""
            )

        else:

            dapso = f"${so_sai}$"

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Trong các khẳng định sau, có bao nhiêu khẳng định """
                f"""\\textbf{{sai}}?"""
            )

        # =====================================================
        # GHÉP KHẲNG ĐỊNH
        # =====================================================

        noi_dung = ""

        for i, (md, dung_sai, lg) in enumerate(ds_chon):

            noi_dung += (
                f"{chr(97+i)}) {md}.\\\\"
            )

        debai += "\\\\" + noi_dung

        # =====================================================
        # TẠO NHIỄU
        # =====================================================

        dsnhieu = []

        for val in range(5):

            pa = f"${val}$"

            if pa != dapso:

                dsnhieu.append(pa)

        dsnhieu = random.sample(dsnhieu, 3)

        # =====================================================
        # LỜI GIẢI
        # =====================================================

        giai = ""

        for i, (md, dung_sai, lg) in enumerate(ds_chon):

            if dung_sai:

                kq = "đúng"

            else:

                kq = "sai"

            giai += (
                f"{chr(97+i)}) {md} là khẳng định {kq}. "
                f"{lg}\\\\"
            )

        if hoi_dung == 0:

            giai += (
                f"Vậy có ${so_dung}$ khẳng định đúng."
            )

        else:

            giai += (
                f"Vậy có ${so_sai}$ khẳng định sai."
            )

        cauTN += MC_SA_answer_text(

            debai,

            dapso,

            dsnhieu,

            giai,

            0,

            0,

            dang
        )

    return cauTN

def L10_C1_B2_NB017_MC_E_01(socau, dang=1):

    gt = []
    dem = len(gt)

    while dem < socau:

        # =====================================================
        # TẠO TẬP HỢP A BẰNG KÍ HIỆU CHỮ
        # =====================================================
        # SUA 29/09/2026 (co Lan bao): truoc day tap A la tap SO
        # (vi du $A=\{-9;-1;2;4;12\}$) nhung cac khang dinh ben duoi
        # lai viet bang chu z, w, v - ma de KHONG he cho biet z, w, v
        # la gi. Hoc sinh khong co cach nao lam duoc, chi loi giai moi
        # lo ra "Ta gan z = -9".
        # Nguyen tac co Lan chot: DE CHU THI CHU HET, DE SO THI SO HET.
        # Nay A cung la tap ki hieu chu, moi khang dinh doc thang tren
        # A, khong con phep gan ngam nao nua. Ban dung SO la ham
        # L10_C1_B2_NB017_MC_B_01, de rieng - hai ban khong tron nhau.

        ds_ki_hieu = random.choice([
            ['a', 'b', 'c', 'd', 'e', 'f'],
            ['m', 'n', 'p', 'q', 'r', 's'],
            ['u', 'v', 'w', 'x', 'y', 'z'],
        ])

        k = np.random.randint(4, 7)

        A_list = sorted(random.sample(ds_ki_hieu, k))

        pt1, pt2, pt3, pt4 = random.sample(A_list, 4)

        # =====================================================
        # HIỂN THỊ TẬP HỢP
        # =====================================================

        A_latex = (
            "\\left\\{ "
            + "; ".join(map(str, A_list))
            + " \\right\\}"
        )

        # =====================================================
        # KHẲNG ĐỊNH CHỨA RỖNG
        # =====================================================

        kh_rong = random.choice([

            (
                f"$\\varnothing \\in A$",

                False,

                f"$A$ không chứa phần tử $\\varnothing$."
            ),

            (
                f"$\\varnothing \\subset A$",

                True,

                f"Tập rỗng là tập con của mọi tập hợp."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\in A$",

                False,

                f"$A$ không chứa phần tử "
                f"$\\left\\{{ \\varnothing \\right\\}}$."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$",

                False,

                f"Muốn "
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$ "
                f"thì cần $\\varnothing \\in A$."
            )
        ])

        # =====================================================
        # DANH SÁCH KHẲNG ĐỊNH THƯỜNG
        # =====================================================

        ds_khangdinh = [

            (
                f"${pt1} \\in A$",

                True,

                f"Vì ${pt1}$ là một phần tử của $A$ nên "
                f"${pt1} \\in A$ là đúng."
            ),

            (
                f"${pt2} \\subset A$",

                False,

                f"${pt2}$ là phần tử nên không dùng kí hiệu "
                f"$\\subset$."
            ),

            (
                f"$\\left\\{{ {pt3} \\right\\}} \\in A$",

                False,

                f"$A$ không chứa phần tử "
                f"$\\left\\{{ {pt3} \\right\\}}$."
            ),

            (
                f"$\\left\\{{ {pt4} \\right\\}} \\subset A$",

                True,

                f"Mọi phần tử của "
                f"$\\left\\{{ {pt4} \\right\\}}$ đều thuộc $A$."
            )
        ]

        # =====================================================
        # CHỌN 3 KHẲNG ĐỊNH THƯỜNG
        # =====================================================

        ds_thuong = random.sample(ds_khangdinh, 3)

        # =====================================================
        # THÊM KHẲNG ĐỊNH RỖNG
        # =====================================================

        ds_chon = ds_thuong + [kh_rong]

        random.shuffle(ds_chon)

        # =====================================================
        # HỎI ĐÚNG HAY SAI
        # =====================================================

        hoi_dung = np.random.randint(0, 2)

        # =====================================================
        # DATA TRÁNH TRÙNG
        # =====================================================

        data = [

            tuple(A_list),

            tuple(
                (x[0], x[1], x[2]) for x in ds_chon
            ),

            hoi_dung
        ]

        if data not in gt:

            gt.append(data)

            dem += 1

    # =====================================================
    # SINH ĐỀ
    # =====================================================

    cauTN = ''

    for data in gt:

        A_list = list(data[0])

        ds_chon = list(data[1])

        hoi_dung = data[2]

        # =====================================================
        # ĐẾM
        # =====================================================

        so_dung = sum(1 for x in ds_chon if x[1])

        so_sai = 4 - so_dung

        # =====================================================
        # HIỂN THỊ TẬP HỢP
        # =====================================================

        A_latex = (
            "\\left\\{ "
            + "; ".join(map(str, A_list))
            + " \\right\\}"
        )

        # =====================================================
        # TẠO ĐỀ
        # =====================================================

        if hoi_dung == 0:

            dapso = f"${so_dung}$"

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Trong các khẳng định sau, có bao nhiêu khẳng định đúng?"""
            )

        else:

            dapso = f"${so_sai}$"

            debai = (
                f"""Cho tập hợp $A = {A_latex}$.\\\\
                Trong các khẳng định sau, có bao nhiêu khẳng định """
                f"""\\textbf{{sai}}?"""
            )

        # =====================================================
        # GHÉP KHẲNG ĐỊNH
        # =====================================================

        noi_dung = ""

        for i, (md, dung_sai, lg) in enumerate(ds_chon):

            noi_dung += (
                f"{chr(97+i)}) {md}.\\\\"
            )

        debai += "\\\\" + noi_dung

        # =====================================================
        # TẠO NHIỄU
        # =====================================================

        dsnhieu = []

        for val in range(5):

            pa = f"${val}$"

            if pa != dapso:

                dsnhieu.append(pa)

        dsnhieu = random.sample(dsnhieu, 3)

        # =====================================================
        # LỜI GIẢI
        # =====================================================

        giai = ""

        for i, (md, dung_sai, lg) in enumerate(ds_chon):

            if dung_sai:

                kq = "đúng"

            else:

                kq = "sai"

            giai += (
                f"{chr(97+i)}) {md} là khẳng định {kq}. "
                f"{lg}\\\\"
            )

        if hoi_dung == 0:

            giai += (
                f"Vậy có ${so_dung}$ khẳng định đúng."
            )

        else:

            giai += (
                f"Vậy có ${so_sai}$ khẳng định sai."
            )

        cauTN += MC_SA_answer_text(

            debai,

            dapso,

            dsnhieu,

            giai,

            0,

            0,

            dang
        )

    return cauTN


def L10_C1_B2_NB017_MC_F_01(socau, dang=1):

    # Danh sách các chữ cái hoa đặt tên cho tập hợp và chữ thường đặt tên cho phần tử
    chu_hoa = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'Q', 'S', 'T', 'V', 'X', 'Y', 'Z']
    chu_thuong = ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'p', 'q', 't', 'u', 'v', 'x', 'y', 'z']

    gt = []
    dem = len(gt)
    while dem < socau:
        # Lấy ngẫu nhiên 2 chữ cái viết hoa khác nhau làm tên tập hợp
        taps = np.random.choice(chu_hoa, size=2, replace=False)
        Tap_Con = taps[0]
        Tap_Me = taps[1]

        # Lấy ngẫu nhiên 1 chữ cái viết thường làm tên phần tử
        Phan_Tu = np.random.choice(chu_thuong)

        v = [Tap_Con, Tap_Me, Phan_Tu]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        Tap_Con, Tap_Me, Phan_Tu = v[0], v[1], v[2]

        debai = f"""Cho hai tập hợp ${Tap_Con}$, ${Tap_Me}$ thỏa mãn ${Tap_Con} \\subset {Tap_Me}$ và một phần tử ${Phan_Tu} \\in {Tap_Con}$. Tìm khẳng định đúng trong các khẳng định sau."""

        dapso = f"""${Phan_Tu} \\in {Tap_Me}$"""
        dsnhieu = [
            f"""${Phan_Tu} \\subset {Tap_Me}$""",
            f"""${Phan_Tu} \\notin {Tap_Me}$""",
            f"""$\\left\\{{ {Phan_Tu} \\right\\}} \\in {Tap_Con}$"""
        ]

        giai = f"""Vì phần tử ${Phan_Tu}$ thuộc tập hợp ${Tap_Con}$ (ký hiệu ${Phan_Tu} \\in {Tap_Con}$) và mọi phần tử của tập hợp ${Tap_Con}$ đều phải thuộc tập hợp ${Tap_Me}$ (do quan hệ tập con ${Tap_Con} \\subset {Tap_Me}$), nên chắc chắn phần tử ${Phan_Tu}$ phải thuộc tập hợp ${Tap_Me}$. Ký hiệu toán học đúng là ${Phan_Tu} \\in {Tap_Me}$.\\\\
        - Phương án ${Phan_Tu} \\subset {Tap_Me}$ sai vì giữa phần tử và tập hợp chỉ có quan hệ thuộc ($\\in$), không dùng ký hiệu chứa ($\\subset$).\\\\
        - Phương án $\\left\\{{ {Phan_Tu} \\right\\}} \\in {Tap_Con}$ sai vì tập hợp chứa phần tử ${Phan_Tu}$ thì phải dùng quan hệ chứa $\\left\\{{ {Phan_Tu} \\right\\}} \\subset {Tap_Con}$ chứ không phải thuộc."""

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B2_TH018_MC_A_01(socau, dang=1):

    # Danh sách các chữ cái hoa đặt tên cho tập hợp
    chu_hoa = ['A', 'B', 'X', 'Y', 'M', 'P', 'E', 'F']

    max_cau = len(chu_hoa) * 4
    if socau > max_cau:
        raise ValueError(f"socau không được vượt quá {max_cau}")

    gt = []
    dem = 0

    while dem < socau:
        T_Hop = np.random.choice(chu_hoa)

        # 0: A\A
        # 1: A\∅
        # 2: A∩∅
        # 3: A∪∅
        k = np.random.randint(0, 4)

        v = [T_Hop, k]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''

    for v in gt:
        T_Hop, k = v

        debai = f"""Cho tập hợp ${T_Hop} \\ne \\varnothing$. Mệnh đề nào sau đây \\textbf{{đúng}}?"""

        if k == 0:
            dapso = f"""${T_Hop} \\setminus {T_Hop} = \\varnothing$"""

            dsnhieu = [
                f"""${T_Hop} \\setminus \\varnothing = \\varnothing$""",
                f"""$\\varnothing \\setminus {T_Hop} = {T_Hop}$""",
                f"""$\\varnothing \\setminus \\varnothing = {T_Hop}$"""
            ]

            giai = (
                f"""Hiệu của hai tập hợp ${T_Hop} \\setminus {T_Hop}$ là tập hợp gồm các phần tử thuộc ${T_Hop}$ """
                f"""nhưng không thuộc ${T_Hop}$. Do đó ${T_Hop} \\setminus {T_Hop}=\\varnothing$."""
            )

        elif k == 1:
            dapso = f"""${T_Hop} \\setminus \\varnothing = {T_Hop}$"""

            dsnhieu = [
                f"""${T_Hop} \\setminus {T_Hop} = {T_Hop}$""",
                f"""$\\varnothing \\setminus {T_Hop} = {T_Hop}$""",
                f"""${T_Hop} \\setminus \\varnothing = \\varnothing$"""
            ]

            giai = (
                f"""Vì tập rỗng không chứa phần tử nào nên khi bỏ đi các phần tử thuộc """
                f"""$\\varnothing$ khỏi ${T_Hop}$ thì tập hợp không thay đổi. Do đó """
                f"""${T_Hop} \\setminus \\varnothing = {T_Hop}$."""
            )

        elif k == 2:
            dapso = f"""${T_Hop} \\cap \\varnothing = \\varnothing$"""

            dsnhieu = [
                f"""${T_Hop} \\cap \\varnothing = {T_Hop}$""",
                f"""${T_Hop} \\cap {T_Hop} = \\varnothing$""",
                f"""$\\varnothing \\cap \\varnothing = {T_Hop}$"""
            ]

            giai = (
                f"""Giao của ${T_Hop}$ với tập rỗng là tập các phần tử chung của hai tập hợp. """
                f"""Vì tập rỗng không có phần tử nào nên ${T_Hop} \\cap \\varnothing = \\varnothing$."""
            )

        else:
            dapso = f"""${T_Hop} \\cup \\varnothing = {T_Hop}$"""

            dsnhieu = [
                f"""${T_Hop} \\cup \\varnothing = \\varnothing$""",
                f"""${T_Hop} \\cup {T_Hop} = \\varnothing$""",
                f"""$\\varnothing \\cup \\varnothing = {T_Hop}$"""
            ]

            giai = (
                f"""Hợp của ${T_Hop}$ với tập rỗng gồm tất cả các phần tử thuộc ${T_Hop}$ """
                f"""hoặc thuộc $\\varnothing$. Vì tập rỗng không thêm phần tử nào nên """
                f"""${T_Hop} \\cup \\varnothing = {T_Hop}$."""
            )

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B2_TH018_MC_B_01(socau, dang=1):

    gt = []
    dem = len(gt)

    ten_tap_list = [
        ("A", "B"),
        ("M", "N"),
        ("X", "Y"),
        ("P", "Q"),
        ("E", "F")
    ]

    while dem < socau:
        tap1, tap2 = random.choice(ten_tap_list)

        a_len = np.random.randint(3, 9)
        b_len = np.random.randint(3, 9)

        A_set = set(np.random.choice(range(-20, 21), size=a_len, replace=False))
        B_set = set(np.random.choice(range(-20, 21), size=b_len, replace=False))

        pheptoan_code = np.random.randint(0, 4)

        if len(A_set & B_set) == 0 or len(A_set - B_set) == 0 or len(B_set - A_set) == 0:
            continue

        v = (
            tuple(sorted(A_set)),
            tuple(sorted(B_set)),
            pheptoan_code,
            tap1,
            tap2
        )

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''

    for v in gt:
        A_list, B_list, pheptoan_code, tap1, tap2 = v

        A_set = set(A_list)
        B_set = set(B_list)

        len_hieu_AB = len(A_set - B_set)
        len_hieu_BA = len(B_set - A_set)
        len_giao = len(A_set & B_set)
        len_hop = len(A_set | B_set)

        if pheptoan_code == 0:
            pheptoan_tex = f"{tap1} \\setminus {tap2}"
            z_ans = len_hieu_AB
            tap_kq_list = sorted(list(A_set - B_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap1} \\setminus {tap2}$ gồm các phần tử thuộc "
                f"${tap1}$ nhưng không thuộc ${tap2}$. Ta có "
                f"${tap1} \\setminus {tap2}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        elif pheptoan_code == 1:
            pheptoan_tex = f"{tap2} \\setminus {tap1}"
            z_ans = len_hieu_BA
            tap_kq_list = sorted(list(B_set - A_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap2} \\setminus {tap1}$ gồm các phần tử thuộc "
                f"${tap2}$ nhưng không thuộc ${tap1}$. Ta có "
                f"${tap2} \\setminus {tap1}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        elif pheptoan_code == 2:
            pheptoan_tex = f"{tap1} \\cap {tap2}"
            z_ans = len_giao
            tap_kq_list = sorted(list(A_set & B_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap1} \\cap {tap2}$ gồm các phần tử vừa thuộc "
                f"${tap1}$ vừa thuộc ${tap2}$. Ta có "
                f"${tap1} \\cap {tap2}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        else:
            pheptoan_tex = f"{tap1} \\cup {tap2}"
            z_ans = len_hop
            tap_kq_list = sorted(list(A_set | B_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap1} \\cup {tap2}$ gồm các phần tử thuộc "
                f"${tap1}$ hoặc thuộc ${tap2}$. Ta có "
                f"${tap1} \\cup {tap2}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        A_tex = "\\left\\{" + "; ".join(map(str, A_list)) + "\\right\\}"
        B_tex = "\\left\\{" + "; ".join(map(str, B_list)) + "\\right\\}"

        mau_de = [
            f"Cho hai tập hợp:\\\\ ${tap1}={A_tex}$,\\\\ ${tap2}={B_tex}$.\\\\ Tập hợp ${pheptoan_tex}$ có bao nhiêu phần tử?",
            f"Cho ${tap1}={A_tex}$ \\\\ và ${tap2}={B_tex}$. \\\\ Số phần tử của tập hợp ${pheptoan_tex}$ bằng",
            f"Biết ${tap1}={A_tex}$ \\\\ và ${tap2}={B_tex}$.\\\\ Tính số phần tử của tập hợp ${pheptoan_tex}$.",
            f"Với hai tập hợp:\\\\ ${tap1}={A_tex}$,\\\\ ${tap2}={B_tex}$.\\\\ Giá trị $n({pheptoan_tex})$ là",
            f"Cho hai tập hợp ${tap1}$ và ${tap2}$ như sau:\\\\ ${tap1}={A_tex}$,\\\\ ${tap2}={B_tex}$.\\\\ Tập hợp ${pheptoan_tex}$ chứa bao nhiêu phần tử?"
        ]

        debai = random.choice(mau_de)

        dapso = f"${z_ans}$"

        ds_nhieu_so = []
        sai_so = [-2, -1, 1, 2, 3]

        for delta in sai_so:
            val_nhieu = z_ans + delta
            if val_nhieu >= 0 and val_nhieu != z_ans and val_nhieu not in ds_nhieu_so:
                ds_nhieu_so.append(val_nhieu)

        nhieu_chon = list(np.random.choice(ds_nhieu_so, size=3, replace=False))

        dsnhieu = [
            f"${nhieu_chon[0]}$",
            f"${nhieu_chon[1]}$",
            f"${nhieu_chon[2]}$"
        ]

        mau_giai = [
            f"{giai_chi_tiet}\\\\ Đếm số phần tử của tập hợp trên, ta được ${z_ans}$ phần tử.",
            f"{giai_chi_tiet}\\\\ Do đó $n({pheptoan_tex})={z_ans}$.",
            f"{giai_chi_tiet}\\\\ Suy ra tập hợp cần tìm có ${z_ans}$ phần tử.",
            f"{giai_chi_tiet}\\\\ Vậy số phần tử của tập hợp ${pheptoan_tex}$ là ${z_ans}$."
        ]

        giai = random.choice(mau_giai)

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN


def L10_C1_B2_NB017_MC_C_01(socau, dang=1):

    gt = []
    dem = len(gt)
    while dem < socau:
        # Sinh tập gốc A = [a_val; b_val) với độ dài khoảng đủ lớn để chứa các tập con
        a_val = np.random.randint(-9, 5)
        b_val = np.random.randint(a_val + 5, a_val + 15)  # Đảm bảo b_val luôn lớn hơn a_val ít nhất 5 đơn vị

        # Sinh đáp án đúng (a0; b0) nằm hoàn toàn bên trong [a_val; b_val)
        a0 = np.random.randint(a_val + 1, b_val - 2)
        b0 = np.random.randint(a0 + 1, b_val)

        # Sinh nhiễu 1: [a1; b1) vi phạm ở đầu mút trái (a1 < a_val)
        a1 = np.random.randint(a_val - 5, a_val)
        b1 = np.random.randint(a_val + 1, b_val)  # Bảo đảm b1 > a_val > a1 để tập không bị rỗng

        # Sinh nhiễu 2: (-\infty; b2) chắc chắn vươn về âm vô cùng nên không thể là tập con của A
        b2 = np.random.randint(a_val + 1, b_val)

        # Sinh nhiễu 3: (a3; b_val] vi phạm ở đầu mút phải vì chứa phần tử b_val, trong khi A không chứa b_val
        a3 = np.random.randint(a_val + 1, b_val)

        v = [a_val, b_val, a0, b0, a1, b1, b2, a3]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        a_val, b_val, a0, b0, a1, b1, b2, a3 = v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]

        debai = f"""Cho tập hợp $A = [{a_val}; {b_val})$. Trong các tập hợp sau, tập hợp nào là tập con của tập hợp $A$?"""

        # ĐỒNG BỘ BỌC TOÀN BỘ PHƯƠNG ÁN CHỌN TRONG CẶP DẤU $ DUY NHẤT
        dapso = f"""$({a0}; {b0})$"""
        dsnhieu = [
            f"""$[{a1}; {b1})$""",
            f"""$(-\\infty; {b2})$""",
            f"""$({a3}; {b_val}]$"""
        ]

        giai = f"""Điều kiện để một tập số $X$ là tập con của $A = [{a_val}; {b_val})$ là mọi phần tử của $X$ phải thuộc $A$.\\\\
        - Xét phương án $({a0}; {b0})$: Do ${a_val} < {a0} < {b0} < {b_val}$, nên toàn bộ khoảng $({a0}; {b0})$ đều nằm trọn bên trong nửa khoảng $[{a_val}; {b_val})$. Do đó $({a0}; {b0}) \\subset A$.\\\\
        - Các phương án còn lại đều chứa các phần tử không thuộc $A$ (ví dụ: $[{a1}; {b1})$ chứa phần tử nhỏ hơn ${a_val}$, $(-\\infty; {b2})$ chứa các số âm vô cùng, $({a3}; {b_val}]$ chứa phần tử ${b_val}$ mà $A$ không có)."""

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


def L10_C1_B2_TH021_MC_A_01(socau, dang=1):

    gt = []
    dem = len(gt)

    ten_tap_list = ["A", "B", "C", "D", "E", "F", "M", "N", "P", "Q", "X", "Y"]

    while dem < socau:
        ten_tap = np.random.choice(ten_tap_list)

        loai_tap = np.random.randint(0, 8)

        A_arr = list(np.random.choice(range(-30, 31), size=2, replace=False))
        A_arr.sort()
        a, b = A_arr[0], A_arr[1]

        v = [ten_tap, a, b, loai_tap]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''

    for v in gt:
        ten_tap, a, b, loai_tap = v

        if loai_tap == 0:
            A_str = f"[{a}; {b}]"
            dap_so_str = f"(-\\infty; {a}) \\cup ({b}; +\\infty)"
            nhieu1 = f"(-\\infty; {a}] \\cup [{b}; +\\infty)"
            nhieu2 = f"({a}; {b})"
            nhieu3 = f"[{a}; {b})"

        elif loai_tap == 1:
            A_str = f"[{a}; {b})"
            dap_so_str = f"(-\\infty; {a}) \\cup [{b}; +\\infty)"
            nhieu1 = f"(-\\infty; {a}] \\cup ({b}; +\\infty)"
            nhieu2 = f"({a}; {b}]"
            nhieu3 = f"({a}; {b})"

        elif loai_tap == 2:
            A_str = f"({a}; {b}]"
            dap_so_str = f"(-\\infty; {a}] \\cup ({b}; +\\infty)"
            nhieu1 = f"(-\\infty; {a}) \\cup [{b}; +\\infty)"
            nhieu2 = f"[{a}; {b})"
            nhieu3 = f"[{a}; {b}]"

        elif loai_tap == 3:
            A_str = f"({a}; {b})"
            dap_so_str = f"(-\\infty; {a}] \\cup [{b}; +\\infty)"
            nhieu1 = f"(-\\infty; {a}) \\cup ({b}; +\\infty)"
            nhieu2 = f"[{a}; {b}]"
            nhieu3 = f"[{a}; {b})"

        elif loai_tap == 4:
            A_str = f"(-\\infty; {b}]"
            dap_so_str = f"({b}; +\\infty)"
            nhieu1 = f"[{b}; +\\infty)"
            nhieu2 = f"(-\\infty; {b})"
            nhieu3 = f"[{b}; +\\infty]"

        elif loai_tap == 5:
            A_str = f"(-\\infty; {b})"
            dap_so_str = f"[{b}; +\\infty)"
            nhieu1 = f"({b}; +\\infty)"
            nhieu2 = f"(-\\infty; {b}]"
            nhieu3 = f"[{b}; +\\infty]"

        elif loai_tap == 6:
            A_str = f"[{a}; +\\infty)"
            dap_so_str = f"(-\\infty; {a})"
            nhieu1 = f"(-\\infty; {a}]"
            nhieu2 = f"[{a}; +\\infty)"
            nhieu3 = f"({a}; +\\infty)"

        else:
            A_str = f"({a}; +\\infty)"
            dap_so_str = f"(-\\infty; {a}]"
            nhieu1 = f"(-\\infty; {a})"
            nhieu2 = f"[{a}; +\\infty)"
            nhieu3 = f"({a}; +\\infty)"

        mau_de = [
            f"Cho tập hợp ${ten_tap}={A_str}$. Tìm tập hợp phần bù $C_{{\\mathbb{{R}}}}^{ten_tap}$.",
            f"Cho ${ten_tap}={A_str}$. Mệnh đề nào sau đây biểu diễn đúng tập hợp phần bù của ${ten_tap}$ trong $\\mathbb{{R}}$?",
            f"Xác định $C_{{\\mathbb{{R}}}}^{ten_tap}$ biết ${ten_tap}={A_str}$.",
            f"Trong $\\mathbb{{R}}$, phần bù của tập hợp ${ten_tap}={A_str}$ là",
            f"Tìm $\\mathbb{{R}}\\setminus {ten_tap}$ với ${ten_tap}={A_str}$."
        ]

        debai = np.random.choice(mau_de)

        dapso = f"${dap_so_str}$"

        dsnhieu = [
            f"${nhieu1}$",
            f"${nhieu2}$",
            f"${nhieu3}$"
        ]

        mau_giai = [
            f"Theo định nghĩa, $C_{{\\mathbb{{R}}}}^{ten_tap}=\\mathbb{{R}}\\setminus {ten_tap}$. Do đó kết quả là ${dap_so_str}$.",
            f"Phần bù của tập hợp ${ten_tap}$ trong $\\mathbb{{R}}$ là tập hợp các số thực không thuộc ${ten_tap}$. Suy ra $C_{{\\mathbb{{R}}}}^{ten_tap}={dap_so_str}$.",
            f"Xét các điểm biên của ${ten_tap}$ và áp dụng quy tắc đổi ngoặc khi lấy phần bù. Ta được $C_{{\\mathbb{{R}}}}^{ten_tap}={dap_so_str}$.",
            f"Tập hợp phần bù gồm tất cả các số thực nằm ngoài ${ten_tap}$. Vậy $C_{{\\mathbb{{R}}}}^{ten_tap}={dap_so_str}$."
        ]

        giai = np.random.choice(mau_giai)

        cauTN += MC_SA_answer_text(
            debai,
            dapso,
            dsnhieu,
            giai,
            0,
            0,
            dang
        )

    return cauTN

def L10_C1_B2_TH019_MC_A_01(socau, dang=1):

    # Sinh mảng cấu hình ngẫu nhiên theo số lượng câu hỏi để tránh lặp vô hạn
    gt = list(np.random.randint(0, 4, size=socau))

    cauTN = ''
    for loai_vung in gt:
        # Khởi tạo khung TikZ nền và vị trí 3 đường tròn cố định
        tikz_base = r"""\begin{tikzpicture}[scale=0.5, font=\footnotesize, baseline=(current bounding box.center)]
    \def\circleA{(0,0.5) circle (1.5)}
    \def\circleB{(2,0.5) circle (1.5)}
    \def\circleC{(1,-0.7) circle (1.5)}"""

        tikz_footer = r"""    \draw \circleA; \draw \circleB; \draw \circleC;
    \node at (-1.3,2) {$A$};
    \node at (3.3,2) {$B$};
    \node at (1,-2.4) {$C$};
\end{tikzpicture}"""

        if loai_vung == 0:
            # Trường hợp 0: (A giao B) \ C
            # Giải pháp chuẩn: Clip lấy giao A và B, sau đó Clip loại bỏ C bằng đảo vùng chọn [remember picture]
            shading_code = r"""    \begin{scope}
        \clip \circleA;
        \clip \circleB;
        \begin{scope}
            \clip (1,-0.7) circle (1.505) (-3,-4) rectangle (5,4);
            \fill[pattern=north west lines, pattern color=black!70] (-2,-3) rectangle (4,3);
        \end{scope}
    \end{scope}"""

            tikz_full = f"{tikz_base}\n{shading_code}\n{tikz_footer}"

            debai = f"""\\immini{{Cho các tập hợp $A$, $B$, $C$ được biểu diễn bằng biểu đồ Ven như hình vẽ bên. Biết phần gạch sọc biểu diễn cho vùng không gian thuộc cả $A$ và $B$ nhưng nằm hoàn toàn bên ngoài tập hợp $C$. Phần gạch sọc đó minh họa cho tập hợp nào sau đây?}}{{{tikz_full}}}"""
            dapso = """$(A \\cap B) \\setminus C$"""
            dsnhieu = ["""$A \\setminus (B \\cap C)$""", """$(B \\cap C) \\setminus A$""",
                       """$B \\setminus (A \\cap C)$"""]
            giai = """Phần gạch sọc thuộc về vùng chung của hai tập hợp $A$ và $B$, tức là thuộc vào tập hợp giao $A \\cap B$. Đồng thời, phần không gian này nằm ngoài phạm vi bao phủ của tập hợp $C$. Do đó, theo định nghĩa phép toán hiệu của hai tập hợp, phần gạch sọc biểu diễn cho tập hợp $(A \\cap B) \\setminus C$."""

        elif loai_vung == 1:
            # Trường hợp 1: (B giao C) \ A
            shading_code = r"""    \begin{scope}
        \clip \circleB;
        \clip \circleC;
        \begin{scope}
            \clip (0,0.5) circle (1.505) (-3,-4) rectangle (5,4);
            \fill[pattern=north west lines, pattern color=black!70] (-2,-3) rectangle (4,3);
        \end{scope}
    \end{scope}"""

            tikz_full = f"{tikz_base}\n{shading_code}\n{tikz_footer}"

            debai = f"""\\immini{{Cho các tập hợp $A$, $B$, $C$ được biểu diễn bằng biểu đồ Ven như hình vẽ bên. Biết phần gạch sọc biểu diễn cho vùng không gian thuộc cả $B$ và $C$ nhưng nằm hoàn toàn bên ngoài tập hợp $A$. Phần gạch sọc đó minh họa cho tập hợp nào sau đây?}}{{{tikz_full}}}"""
            dapso = """$(B \\cap C) \\setminus A$"""
            dsnhieu = ["""$B \\setminus (A \\cap C)$""", """$(A \\cap B) \\setminus C$""",
                       """$C \\setminus (A \\cap B)$"""]
            giai = """Phần gạch sọc thuộc về vùng chung của hai tập hợp $B$ và $C$, tức là thuộc vào tập hợp giao $B \\cap C$. Đồng thời, phần không gian này nằm ngoài phạm vi bao phủ của tập hợp $A$. Do đó, theo định nghĩa phép toán hiệu của hai tập hợp, phần gạch sọc biểu diễn cho tập hợp $(B \\cap C) \\setminus A$."""

        elif loai_vung == 2:
            # Trường hợp 2: (A giao C) \ B
            shading_code = r"""    \begin{scope}
        \clip \circleA;
        \clip \circleC;
        \begin{scope}
            \clip (2,0.5) circle (1.505) (-3,-4) rectangle (5,4);
            \fill[pattern=north west lines, pattern color=black!70] (-2,-3) rectangle (4,3);
        \end{scope}
    \end{scope}"""

            tikz_full = f"{tikz_base}\n{shading_code}\n{tikz_footer}"

            debai = f"""\\immini{{Cho các tập hợp $A$, $B$, $C$ được biểu diễn bằng biểu đồ Ven như hình vẽ bên. Biết phần gạch sọc biểu diễn cho vùng không gian thuộc cả $A$ và $C$ nhưng nằm hoàn toàn bên ngoài tập hợp $B$. Phần gạch sọc đó minh họa cho tập hợp nào sau đây?}}{{{tikz_full}}}"""
            dapso = """$(A \\cap C) \\setminus B$"""
            dsnhieu = ["""$A \\setminus (B \\cap C)$""", """$(A \\cap B) \\setminus C$""",
                       """$C \\setminus (A \\cap B)$"""]
            giai = """Phần gạch sọc thuộc về vùng chung của hai tập hợp $A$ và $C$, tức là thuộc vào tập hợp giao $A \\cap C$. Đồng thời, phần không gian này nằm ngoài phạm vi bao phủ của tập hợp $B$. Do đó, theo định nghĩa phép toán hiệu của hai tập hợp, phần gạch sọc biểu diễn cho tập hợp $(A \\cap C) \\setminus B$."""

        else:
            # Trường hợp 3: A \ (B hợp C)
            # Chỉ lấy phần riêng của A, loại bỏ bất cứ phần nào chạm vào đường tròn B hoặc C
            shading_code = r"""    \begin{scope}
        \clip \circleA;
        \begin{scope}
            \clip (2,0.5) circle (1.505) (-3,-4) rectangle (5,4);
            \clip (1,-0.7) circle (1.505) (-3,-4) rectangle (5,4);
            \fill[pattern=north west lines, pattern color=black!70] (-2,-3) rectangle (4,3);
        \end{scope}
    \end{scope}"""

            tikz_full = f"{tikz_base}\n{shading_code}\n{tikz_footer}"

            debai = f"""\\immini{{Cho các tập hợp $A$, $B$, $C$ được biểu diễn bằng biểu đồ Ven như hình vẽ bên. Biết phần gạch sọc chỉ nằm trong tập hợp $A$ và hoàn toàn không giao với hai tập hợp $B, C$. Phần gạch sọc đó minh họa cho tập hợp nào sau đây?}}{{{tikz_full}}}"""
            dapso = """$A \\setminus (B \\cup C)$"""
            dsnhieu = ["""$A \\setminus (B \\cap C)$""", """$(A \\setminus B) \\cap C$""",
                       """$(A \\cap B) \\setminus C$"""]
            giai = """Phần gạch sọc thuộc vào phạm vi của tập hợp $A$, nhưng loại bỏ hoàn toàn tất cả các phần tử thuộc về tập hợp $B$ hoặc thuộc về tập hợp $C$. Do tập hợp gồm các phần tử thuộc $B$ hoặc thuộc $C$ là tập hợp hợp $B \\cup C$, nên phần gạch sọc minh họa cho phép hiệu $A \\setminus (B \\cup C)$."""

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)
    return cauTN

def L10_C1_B2_VD020_MC_A_01(socau, dang=1):

    gt = []
    dem = len(gt)
    while dem < socau:
        lop = int(np.random.choice([35, 40, 42, 45, 50]))
        a_val = np.random.randint(18, 28)
        b_val = np.random.randint(12, 22)
        ab = np.random.randint(4, 10)

        if ab >= a_val or ab >= b_val:
            continue

        tong_tham_gia = a_val + b_val - ab
        if tong_tham_gia >= lop:
            continue

        z_ans = lop - tong_tham_gia

        v = [lop, a_val, b_val, ab, z_ans]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        lop, a_val, b_val, ab, z_ans = v[0], v[1], v[2], v[3], v[4]

        debai = f"""Lớp 10A tham gia hai tiết mục văn nghệ để chào mừng ngày Nhà giáo Việt Nam 20/11. Tiết mục thứ nhất có ${a_val}$ bạn tham gia, tiết mục thứ hai có ${b_val}$ bạn tham gia, trong đó có ${ab}$ bạn tham gia vào cả hai tiết mục. Biết rằng tổng số học sinh của lớp 10A là ${lop}$ học sinh. Hỏi lớp 10A có tất cả bao nhiêu bạn không tham gia tiết mục văn nghệ nào?"""
        dapso = f"""${z_ans}$"""

        ds_nhieu_so = []
        sai_so = [-3, -2, -1, 1, 2, 3, 4, 5]
        for delta in sai_so:
            val_nhieu = z_ans + delta
            if val_nhieu >= 0 and val_nhieu != z_ans and val_nhieu not in ds_nhieu_so:
                ds_nhieu_so.append(val_nhieu)

        nhieu_chon = list(np.random.choice(ds_nhieu_so, size=3, replace=False))

        dsnhieu = [
            f"""${nhieu_chon[0]}$""",
            f"""${nhieu_chon[1]}$""",
            f"""${nhieu_chon[2]}$"""
        ]

        tong_tg = a_val + b_val - ab
        giai = f"""Gọi $A$ là tập hợp các học sinh tham gia tiết mục thứ nhất, $B$ là tập hợp các học sinh tham gia tiết mục thứ hai.\\\\
Theo giả thiết đề bài, ta có:\\\\
- Số phần tử của tập hợp $A$ là: $n(A) = {a_val}$.\\\\
- Số phần tử của tập hợp $B$ là: $n(B) = {b_val}$.\\\\
- Số phần tử thuộc phần giao của hai tập hợp (tham gia cả hai tiết mục) là: $n(A \\cap B) = {ab}$.\\\\
Áp dụng công thức bao hàm - loại trừ, tổng số học sinh tham gia ít nhất một trong hai tiết mục văn nghệ là:\\\\
$n(A \\cup B) = n(A) + n(B) - n(A \\cap B) = {a_val} + {b_val} - {ab} = {tong_tg}$ (học sinh).\\\\
Số học sinh của lớp 10A không tham gia tiết mục văn nghệ nào là hiệu giữa tổng số học sinh cả lớp và số học sinh có tham gia văn nghệ:\\\\
${lop} - {tong_tg} = {z_ans}$ (học sinh).\\\\
Vậy lớp 10A có tất cả ${z_ans}$ học sinh không tham gia văn nghệ."""

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

# =====================================================================
# DẠNG VD021: tìm tham số m để hợp / giao của hai tập thoả điều kiện
# ---------------------------------------------------------------------
# Dùng CHUNG cho câu trắc nghiệm (_MC_A) và câu trả lời ngắn (_SA_A), để hai
# câu không bao giờ lệch nhau về đề bài hoặc lời giải.
#
# SỬA TOÁN 27/09/2026 - hai chỗ trước đây cho đáp số sai:
#   1) Đề phải nói rõ $B \ne \varnothing$. Nếu không, với $m \le n$ thì
#      $B = \varnothing$; mà $\varnothing \subset A$ nên $A \cup B = A$ vẫn
#      đúng, và $A \cap B = \varnothing$ cũng vẫn đúng. Khi đó có VÔ SỐ giá
#      trị nguyên của $m$, không phải $b - n$ hay $a - n - 1$.
#   2) Kiểu 2 dẫn tới $m \ge b$, kiểu 4 dẫn tới $m \ge a$ - tức cũng có VÔ SỐ
#      giá trị nguyên của $m$. Bản cũ lặng lẽ lấy $m \le 15$ theo cách sinh
#      số liệu, nhưng ĐỀ KHÔNG HỀ NÓI $m \le 15$ nên học sinh không thể biết.
#      Nay hai kiểu này hỏi GIÁ TRỊ NGUYÊN NHỎ NHẤT của $m$ - luôn tồn tại và
#      duy nhất, đúng tinh thần một câu một đáp số.
# =====================================================================
def _VD021_ngoac(x):
    """Bọc ngoặc số âm để phép trừ không ra hai dấu trừ liền nhau: 10 - (-1)."""
    return f"\\left( {x} \\right)" if x < 0 else f"{x}"


def _VD021_liet_ke(dau, cuoi):
    """Liệt kê các số nguyên từ dau đến cuoi.

    Ít giá trị thì ghi ra hết; nhiều thì mới dùng dấu $\\ldots$ - tránh cảnh
    vô lí như $\\left\\{ -9; -8; \\ldots; -8 \\right\\}$ khi chỉ có hai giá trị.
    """
    so = list(range(dau, cuoi + 1))
    if len(so) <= 4:
        ben_trong = "; ".join(str(x) for x in so)
    else:
        ben_trong = f"{so[0]}; {so[1]}; \\ldots; {so[-1]}"
    return "\\left\\{ " + ben_trong + " \\right\\}"


def _VD021_de_giai(kieu, a_val, b_val, n_val):
    """Trả về (debai, dapso, giai) cho một bộ số liệu của dạng VD021."""

    cho = (f"Cho hai tập hợp $A = \\left[ {a_val}; {b_val} \\right]$ và "
           f"$B = \\left( {n_val}; m \\right]$, trong đó $m$ là số nguyên "
           f"sao cho $B \\ne \\varnothing$. ")

    # ---- KIỂU 1: A ∪ B = A  ⟺  B ⊂ A. Vì n > a nên chỉ cần m ≤ b ----
    if kieu == 1:
        dapso = b_val - n_val
        debai = cho + ("Có tất cả bao nhiêu giá trị nguyên của tham số $m$ "
                       "để $A \\cup B = A$?")
        giai = f"""Ta có $A \\cup B = A \\Leftrightarrow B \\subset A$.\\\\
Vì $B \\ne \\varnothing$ nên $m > {n_val}$.\\\\
Do ${n_val} > {a_val}$ nên đầu bên trái của $B$ đã nằm trong $A$, vậy chỉ cần thêm
$m \\le {b_val}$.\\\\
Suy ra
$\\heva{{m > {n_val} \\\\ m \\le {b_val}}}$ hay ${n_val} < m \\le {b_val}$.\\\\
Vì $m \\in \\mathbb{{Z}}$ nên $m \\in {_VD021_liet_ke(n_val + 1, b_val)}$,
số giá trị nguyên của $m$ là ${b_val} - {_VD021_ngoac(n_val)} = {dapso}$.\\\\
Vậy có tất cả ${dapso}$ giá trị nguyên của tham số $m$ thỏa mãn yêu cầu đề bài."""

    # ---- KIỂU 2: A ∪ B = B  ⟺  A ⊂ B  ⟺  m ≥ b (có vô số m nguyên) ----
    elif kieu == 2:
        dapso = b_val
        debai = cho + ("Tìm giá trị nguyên nhỏ nhất của tham số $m$ "
                       "để $A \\cup B = B$.")
        giai = f"""Ta có $A \\cup B = B \\Leftrightarrow A \\subset B$.\\\\
Với $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$, để $A \\subset B$ thì cần
$\\heva{{{n_val} < {a_val} \\\\ m \\ge {b_val}}}$.\\\\
Bất đẳng thức ${n_val} < {a_val}$ đã đúng, nên điều kiện còn lại là
$m \\ge {b_val}$.\\\\
Có vô số số nguyên $m$ thỏa mãn, nhưng số nguyên NHỎ NHẤT trong số đó là
$m = {b_val}$.\\\\
Thử lại: với $m = {b_val}$ thì $B = \\left( {n_val}; {b_val} \\right] \\supset \\left[ {a_val}; {b_val} \\right] = A$, suy ra $A \\cup B = B$.\\\\
Vậy $m = {dapso}$."""

    # ---- KIỂU 3: A ∩ B = ∅. B ≠ ∅ nên n < m, và B nằm hẳn bên trái A ----
    elif kieu == 3:
        dapso = a_val - n_val - 1
        debai = cho + ("Có tất cả bao nhiêu giá trị nguyên của tham số $m$ "
                       "để $A \\cap B = \\varnothing$?")
        giai = f"""Vì $B \\ne \\varnothing$ nên $m > {n_val}$.\\\\
Do ${n_val} < {a_val}$, tập $B = \\left( {n_val}; m \\right]$ nằm bên trái $A = \\left[ {a_val}; {b_val} \\right]$;
hai tập không có phần tử chung khi và chỉ khi
$m < {a_val}$.\\\\
Suy ra
$\\heva{{m > {n_val} \\\\ m < {a_val}}}$ hay ${n_val} < m < {a_val}$.\\\\
Vì $m \\in \\mathbb{{Z}}$ nên $m \\in {_VD021_liet_ke(n_val + 1, a_val - 1)}$,
số giá trị nguyên của $m$ là ${a_val} - {_VD021_ngoac(n_val)} - 1 = {dapso}$.\\\\
Vậy có tất cả ${dapso}$ giá trị nguyên của tham số $m$ thỏa mãn yêu cầu đề bài."""

    # ---- KIỂU 4: A ∩ B ≠ ∅  ⟺  m ≥ a (có vô số m nguyên) ----
    else:
        dapso = a_val
        debai = cho + ("Tìm giá trị nguyên nhỏ nhất của tham số $m$ "
                       "để $A \\cap B \\ne \\varnothing$.")
        giai = f"""Do ${n_val} < {a_val}$ nên $B = \\left( {n_val}; m \\right]$ và $A = \\left[ {a_val}; {b_val} \\right]$ có phần tử chung
khi và chỉ khi đầu bên phải của $B$ chạm tới $A$, tức là
$m \\ge {a_val}$.\\\\
Khi đó phần tử ${a_val}$ thuộc cả $A$ và $B$, suy ra $A \\cap B \\ne \\varnothing$.\\\\
Có vô số số nguyên $m$ thỏa mãn, nhưng số nguyên NHỎ NHẤT trong số đó là
$m = {a_val}$.\\\\
Vậy $m = {dapso}$."""

    return debai, dapso, giai


def _VD021_nhieu(dapso, khong_am):
    """Ba phương án nhiễu khác nhau và khác đáp số (câu trả lời ngắn không dùng)."""
    ds = []
    for delta in (-3, -2, -1, 1, 2, 3, 4):
        val = dapso + delta
        if val == dapso or val in ds:
            continue
        if khong_am and val < 0:
            continue
        ds.append(val)
    return [f"""${val}$""" for val in ds[:3]]


def _VD021_sinh(socau, dang):
    """Sinh socau câu của dạng VD021; dang=1 -> trắc nghiệm, dang=2/3 -> trả lời ngắn."""
    gt = []
    while len(gt) < socau:
        kieu = int(np.random.choice([1, 2, 3, 4]))
        a_val = int(np.random.randint(-15, 5))
        b_val = int(np.random.randint(a_val + 5, 16))

        if kieu == 1:
            # n nằm TRONG A để đầu bên trái của B chắc chắn thuộc A
            n_val = int(np.random.randint(a_val + 1, b_val))
        elif kieu == 3:
            n_val = int(np.random.randint(a_val - 8, a_val - 1))
        else:
            n_val = int(np.random.randint(a_val - 8, a_val))

        v = (kieu, a_val, b_val, n_val)
        if v in gt:
            continue

        dapso = _VD021_de_giai(*v)[1]
        # Kiểu 1, 3 đếm số giá trị -> đáp số phải là số dương.
        if kieu in (1, 3) and dapso <= 0:
            continue
        if len(_VD021_nhieu(dapso, kieu in (1, 3))) < 3:
            continue

        gt.append(v)

    cau = ''
    for v in gt:
        debai, dapso, giai = _VD021_de_giai(*v)
        dsnhieu = _VD021_nhieu(dapso, v[0] in (1, 3))
        cau += MC_SA_answer_text(debai, f"""${dapso}$""", dsnhieu, giai, 0, 0, dang)
    return cau


def L10_C1_B2_VD021_MC_A_01(socau, dang=1):
    """Trắc nghiệm 4 phương án."""
    return _VD021_sinh(socau, dang)


def L10_C1_B2_VD021_SA_A_01(socau, dang=2):
    """Trả lời ngắn: MỘT câu hỏi -> MỘT đáp số, không chia ý a), b).

    Trước 27/09/2026 dạng này là hàm tự luận L10_C1_B2_VD021_TL_A_01 nhưng chỉ
    có một ý, nên theo quy ước đã chốt thì nó phải là câu trả lời ngắn.
    """
    return _VD021_sinh(socau, dang)


def L10_C1_TF_B_01(socau, socot):

    gt = []
    dem = len(gt)
    while dem < socau:
        # 1. Sinh tập A = (left_A; right_A]
        left_A = np.random.randint(-10, -2)
        right_A = np.random.randint(6, 16)

        # 2. Sinh tập B gồm 2 phần tử nguyên {b1; b2}
        b1 = np.random.randint(left_A - 4, left_A)
        b2 = np.random.randint(2, right_A)

        # 3. Thiết lập phương trình bậc hai cho tập C: (x - x1)(x - k*m) = 0
        x1 = np.random.randint(-3, 0)
        k_coef = int(np.random.choice([2, 3, 4, 5]))

        # 4. Sinh các giá trị m khác nhau để làm phong phú ý C
        m_duong = np.random.randint(1, 4)
        m_am = np.random.randint(-4, 0)

        # 5. Chọn ngẫu nhiên phép toán tập hợp cho ý D: giao, hợp, A trừ B, B trừ A
        phep_toan_D = np.random.choice(['giao', 'hop', 'A_tru_B', 'B_tru_A'])

        v = [left_A, right_A, b1, b2, x1, k_coef, m_duong, m_am, phep_toan_D]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTF = ''
    for v in gt:
        left_A, right_A, b1, b2, x1, k_coef, m_duong, m_am, phep_toan_D = v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[
            7], v[8]

        abs_x1 = abs(x1)
        debai_pt = f"x^2 + ({abs_x1} - {k_coef}m)x - {abs_x1 * k_coef}m = 0"

        debai = f"""Cho ba tập hợp:\\\\ $A = ({left_A}; {right_A}]$,\\\\ $B = \\{{ {b1}; {b2} \\}}$,\\\\ $C = \\{{x \\in \\mathbb{{N}} \\mid {debai_pt} \\}}$ với $m$ là tham số nguyên."""

        # Tính toán các dữ kiện bổ trợ
        hieu_cuoi_dau_A_sai = right_A - left_A
        hieu_cuoi_dau_A_dung = right_A - left_A + 1
        hieu_cuoi_dau_B_sai = b2 - b1
        hieu_cuoi_dau_B_dung = b2 - b1 + 1

        nghiem_dung_C = k_coef * m_duong

        # Xác định tập đích và phần tử nguyên đích để so sánh cho ý D
        # C luôn có nghiệm tự nhiên duy nhất là x = k_coef * m (khi m >= 0)
        if phep_toan_D == 'giao':
            chuoi_phep_toan = "A \\cap B"
            chuoi_giai_thich_tap_dich = f"Ta có $A \\cap B = \\{{ {b2} \\}}$."
            # Điều kiện x thuộc giao: x = b2
            ds_target = [b2]
        elif phep_toan_D == 'hop':
            chuoi_phep_toan = "A \\cup B"
            chuoi_giai_thich_tap_dich = f"Ta có $A \\cup B = ({left_A}; {right_A}] \\cup \\{{ {b1} \\}}$."
            # Nghiệm tự nhiên x nằm trong tập hợp hợp (số tự nhiên thuộc A hoặc bằng b1)
            # Tập số thực A chứa các số tự nhiên từ max(0, left_A+1) đến right_A
            start_N = max(0, left_A + 1)
            ds_target = [x for x in range(start_N, right_A + 1)]
            if b1 >= 0:
                ds_target.append(b1)
            ds_target = list(set(ds_target))
        elif phep_toan_D == 'A_tru_B':
            chuoi_phep_toan = "A \\setminus B"
            chuoi_giai_thich_tap_dich = f"Ta có $A \\setminus B = ({left_A}; {right_A}] \\setminus \\{{ {b2} \\}}$."
            # Số tự nhiên thuộc A nhưng bỏ đi b2
            start_N = max(0, left_A + 1)
            ds_target = [x for x in range(start_N, right_A + 1) if x != b2]
        else:  # B_tru_A
            chuoi_phep_toan = "B \\setminus A"
            chuoi_giai_thich_tap_dich = f"Ta có $B \\setminus A = \\{{ {b1} \\}}$."
            # Chỉ chứa b1 (nếu b1 >= 0 thì mới có cơ hội có nghiệm tự nhiên m)
            ds_target = [b1] if b1 >= 0 else []

        # Đếm xem có bao nhiêu giá trị m nguyên dương/bằng 0 thỏa mãn k_coef * m nằm trong ds_target
        m_nguyen_thoa_man = []
        # Xét m từ 0 đến max của ds_target // k_coef + 1 để quét toàn bộ nghiệm nguyên dương và 0
        max_val = max(ds_target) if len(ds_target) > 0 else 0
        for m_check in range(0, (max_val // k_coef) + 2):
            if (k_coef * m_check) in ds_target:
                m_nguyen_thoa_man.append(m_check)

        so_luong_m_khong_am = len(m_nguyen_thoa_man)

        # Lời giải chi tiết động cho ý D
        loi_giai_bo_sung_D = f"{chuoi_giai_thich_tap_dich} Nghiệm tự nhiên duy nhất của tập $C$ (khi $m \\ge 0$) là $x = {k_coef}m$. "
        if phep_toan_D == 'hop' or phep_toan_D == 'A_tru_B':
            loi_giai_bo_sung_D += f"Để $C \\subset ({chuoi_phep_toan})$ thì $k \\cdot m$ phải thuộc tập hợp đích, dẫn tới bài toán có {so_luong_m_khong_am} giá trị nguyên không âm của $m$ thỏa mãn. Ngoài ra, khi $m < 0 \\Rightarrow C = \\varnothing  \\subset ({chuoi_phep_toan})$ (luôn đúng), dẫn đến có vô số giá trị nguyên âm của $m$ thỏa mãn."
        else:  # giao hoặc B_tru_A (chỉ có tối đa 1 phần tử đích)
            if so_luong_m_khong_am > 0:
                loi_giai_bo_sung_D += f"Để $C \\subset ({chuoi_phep_toan}) \\Rightarrow C = \\{{ {ds_target[0]} \\}} \\Rightarrow {k_coef}m = {ds_target[0]} \\Rightarrow m = {m_nguyen_thoa_man[0]}$ (thỏa mãn). Kết hợp với vô số giá trị nguyên âm $m < 0$ (khi đó $C = \\varnothing $), ta có vô số giá trị nguyên của $m$."
            else:
                loi_giai_bo_sung_D += f"Để $C \\subset ({chuoi_phep_toan})$ thì không có giá trị $m$ nguyên không âm nào thỏa mãn do nghiệm không nguyên hoặc âm. Tuy nhiên với mọi $m < 0 \\Rightarrow C = \\varnothing  \\subset ({chuoi_phep_toan})$, do đó vẫn có vô số giá trị nguyên âm thỏa mãn."

        phuong_an_sai_so_nghiem_D = f"Có tất cả đúng {so_luong_m_khong_am + 1} giá trị nguyên của tham số $m$ để $C \\subset ({chuoi_phep_toan})$"
        giai_thich_sai_so_nghiem_D = f"Sai. Vì ngoài các giá trị nguyên không âm thỏa mãn, bài toán luôn có vô số giá trị nguyên âm $m < 0$ khiến cho tập $C = \\varnothing $, mà tập rỗng là tập con của mọi tập hợp nên tổng số giá trị nguyên của $m$ phải là vô số."

        ds_abcd = (
            # ==================== Ý A: KHẢO SÁT VỀ MỆNH ĐỀ TOÁN HỌC ====================
            [
                (f"""{{\\True Phát biểu ``Tập $A$ có {hieu_cuoi_dau_A_sai} phần tử'' là một mệnh đề toán học}}""",
                 f"""Đúng. Khẳng định trên mang tính chất đúng sai rõ ràng (cụ thể đây là một mệnh đề toán học mang giá trị sai vì tập số thực $A$ có vô số phần tử)."""),

                (f"""{{\\True Phát biểu ``Tập $B$ có $2$ phần tử'' là một mệnh đề toán học}}""",
                 f"""Đúng. Khẳng định ``Tập $B$ có $2$ phần tử'' là một khẳng định hoàn toàn chính xác (mệnh đề đúng), do đó nó là một mệnh đề toán học."""),

                (f"""{{Phát biểu ``Tập $A$ có {hieu_cuoi_dau_A_sai} phần tử'' không phải là một mệnh đề toán học}}""",
                 f"""Sai. Mặc dù khẳng định trên sai về mặt giá trị toán học (do tập số thực $A$ có vô số phần tử), nhưng nó có tính chất đúng sai rõ ràng, vì vậy theo định nghĩa nó bắt buộc phải là một mệnh đề toán học."""),

                (f"""{{Phát biểu ``Tập $B$ có $2$ phần tử'' không phải là một mệnh đề toán học}}""",
                 f"""Sai. Khẳng định trên là một khẳng định toán học có tính đúng sai rõ ràng (mệnh đề đúng), do đó nó là một mệnh đề toán học."""),

                (f"""{{\\True Phát biểu ``Tập $A$ có {hieu_cuoi_dau_A_dung} phần tử'' là một mệnh đề toán học}}""",
                 f"""Đúng. Đây là một khẳng định toán học có tính đúng sai rõ ràng nên theo định nghĩa nó là một mệnh đề toán học."""),

                (f"""{{Phát biểu ``Tập $A$ có {hieu_cuoi_dau_A_dung} phần tử'' không phải là một mệnh đề toán học}}""",
                 f"""Sai. Phát biểu trên có tính đúng sai rõ ràng nên bắt buộc nó phải là một mệnh đề toán học."""),

                (f"""{{\\True Phát biểu ``Tập $B$ có ${hieu_cuoi_dau_B_dung}$ phần tử'' là một mệnh đề toán học}}""",
                 f"""Đúng. Khẳng định trên mang tính đúng sai rõ ràng nên theo định nghĩa nó là một mệnh đề toán học."""),

                (f"""{{Phát biểu ``Tập $B$ có ${hieu_cuoi_dau_B_dung}$ phần tử'' không phải là một mệnh đề toán học}}""",
                 f"""Sai. Vì nó có tính đúng sai rõ ràng nên bắt buộc là một mệnh đề toán học."""),

                (f"""{{\\True Phát biểu ``Tập $B$ có ${hieu_cuoi_dau_B_sai}$ phần tử'' là một mệnh đề toán học}}""",
                 f"""Đúng. Khẳng định trên mang tính đúng sai rõ ràng nên theo định nghĩa nó là một mệnh đề toán học."""),

                (f"""{{Phát biểu ``Tập $B$ có ${hieu_cuoi_dau_B_sai}$ phần tử'' không phải là một mệnh đề toán học}}""",
                 f"""Sai. Do nó là một khẳng định toán học mang tính đúng sai rõ ràng.""")
            ],

            # ==================== Ý B: CÁC PHÉP TOÁN TOÁN HỌC THUẦN TÚY ====================
            [
                (f"""{{\\True $A \\cap B = \\{{ {b2} \\}}$}}""",
                 f"""Đúng. Phần tử ${b1} < {left_A}$ nên ${b1} \\notin A$. Phần tử ${b2}$ nằm trong khoảng $({left_A}; {right_A}]$ nên ${b2} \\in A$. Do đó giao của hai tập hợp chỉ gồm phần tử ${b2}$."""),

                (f"""{{\\True $n(A \\cap B) = 1$}}""",
                 f"""Đúng. Tập hợp giao $A \\cap B$ có duy nhất đúng $1$ phần tử."""),

                (f"""{{\\True $B \\setminus A = \\{{ {b1} \\}}$}}""",
                 f"""Đúng. Phần tử ${b1} \\notin A$ và ${b2} \\in A$ nên khi thực hiện phép hiệu lấy tập $B$ trừ đi tập $A$, ta loại bỏ phần tử ${b2}$ và giữ lại phần tử ${b1}$."""),

                (f"""{{$A \\cup B = A$}}""",
                 f"""Sai. Vì phần tử ${b1} < {left_A}$ nên ${b1} \\notin A$, do đó phép hợp $A \\cup B$ phải chứa thêm phần tử ${b1}$, tức là $A \\cup B \\neq A$."""),

                (f"""{{$A \\cap B = \\{{ {b1}; {b2} \\}}$}}""",
                 f"""Sai. Phần tử ${b1} < {left_A}$ nên ${b1}$ không thuộc tập hợp $A$, dẫn đến phần tử này không thể nằm trong tập hợp giao $A \\cap B$."""),

                (f"""{{$A \\cap B = ( {left_A}; {b2} ]$}}""",
                 f"""Sai. Giao của một tập số thực và một tập rời rạc phải là một tập rời rạc (tập hữu hạn phần tử) chứ không thể là một khoảng hay nửa khoảng liên tục."""),

                (f"""{{$A \\cap B = \\{{ {b1} \\}}$}}""",
                 f"""Sai. Do phần tử ${b1} \\notin A$ và ${b2} \\in A$, vì thế tập hợp giao đúng phải có $1$ phần tử là phần tử nằm trong tập $A$."""),

                (f"""{{$A \\cup B = \\{{ {b1}; {right_A} \\}}$}}""",
                 f"""Sai. Vì tập hợp $A$ là tập hợp số thực chứa vô số phần tử nên phép hợp $A \\cup B$ là một tập vô hạn chứ không thể chỉ có hai phần tử cô lập."""),

                (f"""{{$B \\setminus A = \\{{ {b2} \\}}$}}""",
                 f"""Sai. Phần tử ${b2}$ thuộc tập $A$ nên bị loại bỏ khi thực hiện phép hiệu $B \\setminus A$, phần tử được giữ lại phải là phần tử không thuộc $A$."""),

                (f"""{{$B \\setminus A = \\varnothing $}}""",
                 f"""Sai. Vì phần tử ${b1} \\in B$ nhưng ${b1} \\notin A$ nên tập hiệu $B \\setminus A \\neq \\varnothing $."""),

                (f"""{{$A \\setminus B = A$}}""",
                 f"""Sai. Do tập hợp $A$ chứa phần tử ${b2} \\in B$ nên khi lấy hiệu $A \\setminus B$, tập hợp $A$ bị mất đi phần tử đó.""")
            ],

            # ==================== Ý C: KHẢO SÁT CHỈ DỰA VÀO SỐ LƯỢNG PHẦN TỬ ====================
            [
                (f"""{{\\True Với $m = {m_duong}$ tập hợp $C$ có đúng $1$ phần tử}}""",
                 f"""Đúng. Với $m = {m_duong}$, phương trình có hai nghiệm, trong đó có một nghiệm âm (loại) và một nghiệm dương (thỏa mãn). Do điều kiện $x \\in \\mathbb{{N}}$ nên tập hợp $C$ có đúng $1$ phần tử."""),

                (f"""{{Với $m = {m_duong}$ tập hợp $C$ có đúng $2$ phần tử}}""",
                 f"""Sai. Vì phương trình luôn có một nghiệm nguyên âm, nghiệm này không thỏa mãn điều kiện là số tự nhiên ($x \\in \\mathbb{{N}}$) nên bị loại, dẫn đến tập $C$ không thể có $2$ phần tử."""),

                (f"""{{\\True Với $m = {m_am}$ tập hợp $C$ là tập rỗng}}""",
                 f"""Đúng. Khi $m = {m_am} < 0$, cả hai nghiệm của phương trình đều nhận giá trị âm, do đó chúng không thuộc tập số tự nhiên $\\mathbb{{N}}$. Vậy tập hợp $C$ là tập rỗng."""),

                (f"""{{Với $m = {m_am}$ tập hợp $C$ có đúng $1$ phần tử}}""",
                 f"""Sai. Khi $m < 0$, tất cả các nghiệm của phương trình đều âm nên đều bị loại bởi điều kiện $x \\in \\mathbb{{N}}$, dẫn đến tập $C$ không có phần tử nào (tập rỗng)."""),

                (f"""{{\\True Với $m = 0$ tập hợp $C$ có đúng $1$ phần tử}}""",
                 f"""Đúng. Khi $m = 0$, phương trình có một nghiệm âm bị loại và một nghiệm bằng $0$ thỏa mãn điều kiện $x \\in \\mathbb{{N}}$. Vậy tập $C$ có đúng $1$ phần tử."""),

                (f"""{{Với $m = 0$ tập hợp $C$ là tập rỗng}}""",
                 f"""Sai. Khi $m = 0$, phương trình vẫn cho một nghiệm tự nhiên thỏa mãn điều kiện, do đó tập $C$ không phải là tập rỗng.""")
            ],

            # ==================== Ý D: XÈT TẬP CON ĐA PHÉP TOÁN (MỚI) ====================
            [
                # --- Các phương án ĐÚNG (Có dấu \True) ---
                (f"""{{\\True Có vô số giá trị nguyên của tham số $m$ để $C \\subset ({chuoi_phep_toan})$}}""",
                 f"""Đúng. {loi_giai_bo_sung_D}"""),
                
                # --- Các phương án SAI (Không có dấu \True) ---
                (f"""{{{phuong_an_sai_so_nghiem_D}}}""",
                 f"""{giai_thich_sai_so_nghiem_D}"""),

                (f"""{{Không có giá trị nguyên nào của tham số $m$ để $C \\subset ({chuoi_phep_toan})$}}""",
                 f"""Sai. Với mọi giá trị nguyên âm $m < 0$ thì $C = \\varnothing  \\subset ({chuoi_phep_toan})$ luôn thỏa mãn yêu cầu, do đó bài toán có vô số giá trị nguyên thỏa mãn.""")
            ]
        )

        cauTF += TF_baitoan_du(debai, ds_abcd, 0, 0, socot)

    return cauTF

def _vd014_de_giai(a, dau, i_left, i_right, k_min_val, k_max_val):
    r"""Đề + đáp số + lời giải chung cho L10_C1_B1_VD014_MC_A_01 và _SA_A_01.

    CLAUDE THEM 29/09/2026 (co Lan duyet). P(x) đúng với mọi x thuộc R:
      dấu >=, > : x^2 - 2ax + k  (hệ số x^2 dương)
      dấu <, <= : -x^2 + 2ax + k (hệ số x^2 âm) - trước đây vẫn để hệ số
                  dương nên đáp số luôn là 0.
    k là số NGUYÊN trong một khoảng bị chặn nên đếm được.
    """
    k_lower = k_min_val if i_left == '[' else k_min_val + 1
    k_upper = k_max_val if i_right == ']' else k_max_val - 1
    khoang = r"\left%s%d;\ %d\right%s" % (i_left, k_min_val, k_max_val, i_right)
    a2 = a ** 2
    if dau in (r'\geq', '>'):
        bt = r"x^2 - %dx + k" % (2 * a)
        bien_doi = (r"x^2 - %dx + k %s 0 \Leftrightarrow \left(x - %d\right)^2 %s %d - k"
                    % (2 * a, dau, a, dau, a2))
        if dau == r'\geq':
            dk = r"%d - k \leq 0 \Leftrightarrow k \geq %d" % (a2, a2)
            k_dau, k_cuoi = max(k_lower, a2), k_upper
        else:
            dk = r"%d - k < 0 \Leftrightarrow k > %d" % (a2, a2)
            k_dau, k_cuoi = max(k_lower, a2 + 1), k_upper
        ly_do = (r"Vì $\left(x - %d\right)^2 \geq 0$ với mọi $x$ và bằng $0$ khi "
                 r"$x = %d$ nên $P(x)$ đúng với mọi $x \in \mathbb{R}$ khi và chỉ "
                 r"khi $%s$." % (a, a, dk))
    else:
        bt = r"-x^2 + %dx + k" % (2 * a)
        dau_nguoc = '>' if dau == '<' else r'\geq'
        bien_doi = (r"-x^2 + %dx + k %s 0 \Leftrightarrow \left(x - %d\right)^2 %s k + %d"
                    % (2 * a, dau, a, dau_nguoc, a2))
        if dau == '<':
            dk = r"k + %d < 0 \Leftrightarrow k < -%d" % (a2, a2)
            k_dau, k_cuoi = k_lower, min(k_upper, -a2 - 1)
        else:
            dk = r"k + %d \leq 0 \Leftrightarrow k \leq -%d" % (a2, a2)
            k_dau, k_cuoi = k_lower, min(k_upper, -a2)
        ly_do = (r"Vì $\left(x - %d\right)^2$ nhỏ nhất bằng $0$ (khi $x = %d$) nên "
                 r"$P(x)$ đúng với mọi $x \in \mathbb{R}$ khi và chỉ khi $%s$."
                 % (a, a, dk))
    dapso_val = max(0, k_cuoi - k_dau + 1)
    debai = (r"Cho mệnh đề chứa biến $P(x)\colon %s %s 0$ với $x \in \mathbb{R}$. "
             r"Có tất cả bao nhiêu giá trị nguyên của tham số $k$ thuộc $%s$ để "
             r"mệnh đề $P(x)$ đúng với mọi $x \in \mathbb{R}$?" % (bt, dau, khoang))
    giai = (r"Ta có $%s$." % bien_doi + "\\\\\n" + ly_do + "\\\\\n" +
            r"Kết hợp với $k \in %s$ và $k$ nguyên (một khoảng bị chặn nên chỉ "
            r"có hữu hạn số nguyên): $k \in \left\{%d; %d; \ldots; %d\right\}$." % (khoang, k_dau, k_dau + 1, k_cuoi) +
            "\\\\\n" +
            r"Số giá trị nguyên của $k$ là $%d - %s + 1 = %d$."
            % (k_cuoi, (r"\left(%d\right)" % k_dau) if k_dau < 0 else str(k_dau), dapso_val))
    return debai, dapso_val, giai


def L10_C1_B1_VD014_MC_A_01(socau, dang = 1):
    gt = []
    dem = 0
    current_year = datetime.datetime.now().year
    k_min_val = -current_year
    k_max_val = current_year + 1

    while dem < socau:
        a = int(np.random.randint(1, 40))
        dau = np.random.choice(['<', '>', r'\geq', r'\leq'])
        i_left = np.random.choice(['(', '['])
        i_right = np.random.choice([')', ']'])

        v = [a, dau, i_left, i_right]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        a, dau, i_left, i_right = v

        # SUA 29/09/2026 (co Lan): bien thuc thi goi la x (n de danh cho so
        # tu nhien); dau < va <= truoc day luon ra 0 gia tri (he so x^2
        # duong thi khong the am voi moi x) - nay doi he so x^2 thanh -1
        # cho hai dau nay; khoang cua k viet trong che do toan.
        debai, dapso_val, giai = _vd014_de_giai(a, dau, i_left, i_right,
                                                k_min_val, k_max_val)
        dapso = str(dapso_val)

        # FIX QUAN TRỌNG: Đảm bảo danh sách nhiễu luôn có 3 phần tử duy nhất
        # Sử dụng set để lọc trùng, sau đó đảm bảo đủ 3 phần tử bằng cách thêm giá trị dự phòng
        base_nhieu = [str(max(0, dapso_val + 1)), str(max(0, dapso_val - 1)), str(max(0, dapso_val + 2)), "0", "1", "5", "10"]
        dsnhieu = random.sample([x for x in list(set(base_nhieu)) if x != dapso], 3)

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


def L10_C1_B1_VD014_SA_A_01(socau, dang = 2):
    gt = []
    dem = 0
    current_year = datetime.datetime.now().year
    k_min_val = -current_year
    k_max_val = current_year + 1

    while dem < socau:
        a = int(np.random.randint(1, 40))
        dau = np.random.choice(['<', '>', r'\geq', r'\leq'])
        i_left = np.random.choice(['(', '['])
        i_right = np.random.choice([')', ']'])

        v = [a, dau, i_left, i_right]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        a, dau, i_left, i_right = v

        # SUA 29/09/2026 (co Lan): bien thuc thi goi la x (n de danh cho so
        # tu nhien); dau < va <= truoc day luon ra 0 gia tri (he so x^2
        # duong thi khong the am voi moi x) - nay doi he so x^2 thanh -1
        # cho hai dau nay; khoang cua k viet trong che do toan.
        debai, dapso_val, giai = _vd014_de_giai(a, dau, i_left, i_right,
                                                k_min_val, k_max_val)
        dapso = str(dapso_val)

        # FIX QUAN TRỌNG: Đảm bảo danh sách nhiễu luôn có 3 phần tử duy nhất
        # Sử dụng set để lọc trùng, sau đó đảm bảo đủ 3 phần tử bằng cách thêm giá trị dự phòng
        base_nhieu = [str(max(0, dapso_val + 1)), str(max(0, dapso_val - 1)), str(max(0, dapso_val + 2)), "0", "1", "5", "10"]
        dsnhieu = random.sample([x for x in list(set(base_nhieu)) if x != dapso], 3)

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


def _vd014_bien_the(kieu, a, dau, i_left, i_right, k_min_val, k_max_val):
    r"""Biến thể 02/03 của VD014_MC_A / SA_A (CLAUDE THEM 29/09/2026).

    kieu = "ton_tai": mệnh đề "tồn tại x thuộc R, f(x) (dấu) 0" ĐÚNG.
    kieu = "moi_sai": mệnh đề "với mọi x thuộc R, f(x) (dấu) 0" SAI
                      (tức mệnh đề phủ định của nó đúng).
    Hệ số x^2 chọn theo dấu để bài không tầm thường:
      ton_tai: dấu <, <= đi với x^2 - 2ax + k ; dấu >, >= đi với -x^2 + 2ax + k
      moi_sai: dấu >, >= đi với x^2 - 2ax + k ; dấu <, <= đi với -x^2 + 2ax + k
    """
    k_lower = k_min_val if i_left == '[' else k_min_val + 1
    k_upper = k_max_val if i_right == ']' else k_max_val - 1
    khoang = r"\left%s%d;\ %d\right%s" % (i_left, k_min_val, k_max_val, i_right)
    a2 = a ** 2
    nho = dau in ('<', r'\leq')
    duong = (kieu == "ton_tai") == nho          # he so x^2 duong?
    bt = (r"x^2 - %dx + k" if duong else r"-x^2 + %dx + k") % (2 * a)
    ghep = r"\left(x - %d\right)^2 + k - %d" % (a, a2) if duong else \
        r"-\left(x - %d\right)^2 + k + %d" % (a, a2)
    cuc = r"k - %d" % a2 if duong else r"k + %d" % a2
    ten_cuc = "nhỏ nhất" if duong else "lớn nhất"
    # gia tri cuc tri cua f la  k - a^2 (duong)  hoac  k + a^2 (am)
    if kieu == "ton_tai":
        # ton tai x: f(x) dau 0  <=>  cuc tri dau 0 (min khi f<.., max khi f>..)
        dau_k = dau
        cau_hoi = r"mệnh đề ``$\exists x \in \mathbb{R},\ %s %s 0$'' là mệnh đề đúng" % (bt, dau)
        ly_do = (r"Ta có $%s = %s$ nên giá trị %s của vế trái là $%s$ (khi $x = %d$)."
                 % (bt, ghep, ten_cuc, cuc, a) + "\\\\\n" +
                 r"Tồn tại $x$ để $%s %s 0$ khi và chỉ khi giá trị %s ấy $%s 0$, "
                 r"tức là $%s %s 0$." % (bt, dau, ten_cuc, dau, cuc, dau))
    else:
        # voi moi x: f(x) dau 0 SAI <=> ton tai x: f(x) (dau phu dinh) 0
        phu = {'>': r'\leq', r'\geq': '<', '<': r'\geq', r'\leq': '>'}[dau]
        dau_k = phu
        cau_hoi = (r"mệnh đề ``$\forall x \in \mathbb{R},\ %s %s 0$'' là mệnh đề \textbf{sai}"
                   % (bt, dau))
        ly_do = (r"Mệnh đề ``$\forall x \in \mathbb{R},\ %s %s 0$'' sai khi và chỉ khi mệnh đề "
                 r"phủ định ``$\exists x \in \mathbb{R},\ %s %s 0$'' đúng." % (bt, dau, bt, phu) +
                 "\\\\\n" +
                 r"Ta có $%s = %s$ nên giá trị %s của vế trái là $%s$ (khi $x = %d$)."
                 % (bt, ghep, ten_cuc, cuc, a) + "\\\\\n" +
                 r"Do đó điều kiện là $%s %s 0$." % (cuc, phu))
    # giai bat phuong trinh cuc_tri (dau_k) 0 theo k
    nguong = a2 if duong else -a2               # cuc = k - nguong
    if dau_k == '<':
        k_dau, k_cuoi, dk = k_lower, min(k_upper, nguong - 1), r"k < %d" % nguong
    elif dau_k == r'\leq':
        k_dau, k_cuoi, dk = k_lower, min(k_upper, nguong), r"k \leq %d" % nguong
    elif dau_k == '>':
        k_dau, k_cuoi, dk = max(k_lower, nguong + 1), k_upper, r"k > %d" % nguong
    else:
        k_dau, k_cuoi, dk = max(k_lower, nguong), k_upper, r"k \geq %d" % nguong
    dem = max(0, k_cuoi - k_dau + 1)
    debai = (r"Có tất cả bao nhiêu giá trị nguyên của tham số $k$ thuộc $%s$ để %s?"
             % (khoang, cau_hoi))
    giai = (ly_do.rstrip(".") + r" $\Leftrightarrow %s$." % dk + "\\\\\n" +
            r"Kết hợp với $k \in %s$ và $k$ nguyên: $k \in \left\{%d; %d; \ldots; %d\right\}$."
            % (khoang, k_dau, k_dau + 1, k_cuoi) + "\\\\\n" +
            r"Số giá trị nguyên của $k$ là $%d - %s + 1 = %d$."
            % (k_cuoi, (r"\left(%d\right)" % k_dau) if k_dau < 0 else str(k_dau), dem))
    return debai, dem, giai


def _vd014_bien_the_cau(kieu, socau, dang, ham_ra):
    nam = datetime.datetime.now().year
    gt = []
    lan = 0
    while len(gt) < socau and lan < 500:
        lan += 1
        v = (random.randint(1, 39), random.choice(['<', '>', r'\geq', r'\leq']),
             random.choice(['(', '[']), random.choice([')', ']']))
        if v not in gt:
            gt.append(v)
    cau = ''
    for a, dau, tr, ph in gt:
        debai, dem, giai = _vd014_bien_the(kieu, a, dau, tr, ph, -nam, nam + 1)
        dap = str(dem)
        nhieu = [x for x in dict.fromkeys([str(dem + 1), str(max(0, dem - 1)), str(dem + 2),
                                            str(max(0, dem - 2))]) if x != dap][:3]
        cau += ham_ra(debai, dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C1_B1_VD014_MC_A_02(socau, dang=1):
    r"""Mệnh đề chứa biến có lượng từ TỒN TẠI: đếm k để mệnh đề đúng.

    CLAUDE THEM 29/09/2026 - bien the 02 (cung dang "Menh de chua bien":
    tim tham so de menh de co luong tu dung/sai). Co Lan duyet.
    """
    return _vd014_bien_the_cau("ton_tai", socau, dang, MC_SA_answer_const)


def L10_C1_B1_VD014_MC_A_03(socau, dang=1):
    r"""Mệnh đề ``với mọi x'' là mệnh đề SAI: đếm k (dùng mệnh đề phủ định).

    CLAUDE THEM 29/09/2026 - bien the 03. Co Lan duyet.
    """
    return _vd014_bien_the_cau("moi_sai", socau, dang, MC_SA_answer_const)


def L10_C1_B1_VD014_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn - biến thể 02 (lượng từ tồn tại). CLAUDE THEM 29/09/2026."""
    return _vd014_bien_the_cau("ton_tai", socau, dang, MC_SA_answer_const)


def L10_C1_B1_VD014_SA_A_03(socau, dang=2):
    r"""Trả lời ngắn - biến thể 03 (mệnh đề với mọi là sai). CLAUDE THEM 29/09/2026."""
    return _vd014_bien_the_cau("moi_sai", socau, dang, MC_SA_answer_const)


def L10_C1_B1_VD014_MC_B_01(socau, dang=1):
    """
    Thông hiểu: Mệnh đề chứa biến P(x): x [dau] x^n.
    Sử dụng SymPy để kiểm tra chân trị cho mỗi cặp tham số ngẫu nhiên.
    """
    gt = []
    dem = 0
    while dem < socau:
        n = random.randint(2, 4)
        a = random.randint(1, 3)
        p, q = 1, random.randint(2, 5)
        # Định nghĩa các dấu toán học
        dau_dict = {'>': '>', '<': '<', r'\ge': '>=', r'\le': '<='}
        dau_tex = random.choice(list(dau_dict.keys()))
        dau_py = dau_dict[dau_tex]

        v = [n, a, p, q, dau_tex, dau_py]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        n, a, p, q, dau_tex, dau_py = v

        # Hàm kiểm tra chân trị
        def check(x_val):
            # Biểu thức: x dau x^n
            expr = f"{x_val} {dau_py} {x_val}**{n}"
            return bool(sympify(expr))

        # Tính chân trị các ý
        p1 = check(a)
        p2 = check(p / q)
        # Ý 3: ∀x∈ℕ, P(x) - Kiểm tra với vài giá trị mẫu
        p3 = all(check(x) for x in range(5))
        # Ý 4: ∃x∈ℕ, ‾P(x) - Tương đương với NOT (∀x∈ℕ, P(x)) nếu tập xác định hữu hạn,
        # ở đây dùng logic phủ định đơn giản: có ít nhất 1 giá trị x sao cho P(x) sai
        p4 = any(not check(x) for x in range(5))

        so_menh_de_dung = sum([p1, p2, p3, p4])

        frac_str = f"\\dfrac{{{p}}}{{{q}}}"
        debai = (
            f"Cho mệnh đề chứa biến $P(x)\\colon x {dau_tex} x^{{{n}}}$. Trong các mệnh đề sau, có bao nhiêu mệnh đề đúng?\n"
            f"\\begin{{enumerate}}\n"
            f"\\item $P({a})$.\n"
            f"\\item $P\\left({frac_str}\\right)$.\n"
            f"\\item $\\forall x\\in \\mathbb{{N}}, P(x)$.\n"
            f"\\item $\\exists x\\in \\mathbb{{N}}, \\overline{{P(x)}}$.\n"
            f"\\end{{enumerate}}"
        )

        dapso = f"${so_menh_de_dung}$"
        dsnhieu = [f"${i}$" for i in range(5) if i != so_menh_de_dung]

        # SUA 29/09/2026 (co Lan: gach dau dong khong dat, cac y danh so
        # 1., 2., ...): loi giai cu viet "- P(3) la Sai. - ..." dinh lien
        # mot mach tren PDF va khong neu ly do. Nay danh so tung y, moi y
        # mot dong, kem phep thu cu the.
        def dung_sai(b):
            return "đúng" if b else "sai"

        phan_so = f"\\dfrac{{{p}}}{{{q}}}"
        mu_ps = f"\\dfrac{{{p ** n}}}{{{q ** n}}}"
        # phan vi du nho nhat trong N (0, 1, 2, ...) lam P(x) sai
        phan_vd = next((x for x in range(5) if not check(x)), None)
        if phan_vd is None:
            ly_do_3 = (f"đúng: với $x \\in \\left\\{{0; 1\\right\\}}$ thì $x = x^{{{n}}}$, "
                       f"với $x \\ge 2$ thì $x < x^{{{n}}}$")
            ly_do_4 = f"sai, vì $P(x)$ đúng với mọi $x \\in \\mathbb{{N}}$ (ý 3)"
        else:
            ly_do_3 = (f"sai, vì với $x = {phan_vd}$ thì ${phan_vd} {dau_tex} "
                       f"{phan_vd}^{{{n}}} = {phan_vd ** n}$ sai")
            ly_do_4 = f"đúng, vì $x = {phan_vd}$ làm $P(x)$ sai"
        giai = (
            f"Xét mệnh đề chứa biến $P(x)\\colon x {dau_tex} x^{{{n}}}$.\n"
            f"\\begin{{enumerate}}\n"
            f"\\item $P({a})\\colon {a} {dau_tex} {a}^{{{n}}} = {a ** n}$ là mệnh đề "
            f"{dung_sai(p1)}.\n"
            f"\\item $P\\left({phan_so}\\right)\\colon {phan_so} {dau_tex} "
            f"\\left({phan_so}\\right)^{{{n}}} = {mu_ps}$ là mệnh đề {dung_sai(p2)}.\n"
            f"\\item $\\forall x\\in \\mathbb{{N}}, P(x)$ là mệnh đề {ly_do_3}.\n"
            f"\\item $\\exists x\\in \\mathbb{{N}}, \\overline{{P(x)}}$ là mệnh đề "
            f"{ly_do_4}.\n"
            f"\\end{{enumerate}}\n"
            f"Vậy có $\\mathbf{{{so_menh_de_dung}}}$ mệnh đề đúng."
        )

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B2_VD020_TL_A_01(socau, dong=1):
    """
    Sinh bài toán tự luận về tập hợp với điều kiện:
    Số người không chọn sản phẩm nào >= 10.
    """
    gt = []
    dem = 0
    while dem < socau:
        tong = 100
        # Để đảm bảo (tong - n_AUB) >= 10, thì n_AUB <= 90
        # n_AUB = n_A + n_B - n_AB <= 90
        n_A = random.randint(50, 70)
        n_B = random.randint(50, 70)
        # Đảm bảo n_AB đủ lớn để n_AUB không vượt quá 90
        # n_AB >= n_A + n_B - 90
        min_n_AB = max(20, n_A + n_B - 90)
        n_AB = random.randint(min_n_AB, min(n_A, n_B) - 5)

        v = [tong, n_A, n_B, n_AB]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTL = ''
    for v in gt:
        tong, n_A, n_B, n_AB = v

        n_AUB = n_A + n_B - n_AB
        n_none = tong - n_AUB

        debai = (
            f"Tại một sự kiện có {tong} người tham gia khảo sát về hai sản phẩm A và B. "
            f"Biết có {n_A} người chọn sản phẩm A, {n_B} người chọn sản phẩm B và {n_AB} người chọn cả hai sản phẩm. "
            f"Tính:"
        )

        ds_abcd = [
            (
                "Số người đã chọn ít nhất một sản phẩm?",
                n_AUB,
                f"Theo nguyên lý bù trừ, số người chọn ít nhất một sản phẩm là: {n_A} + {n_B} - {n_AB} = {n_AUB} (người)."
            ),
            (
                "Số người không chọn sản phẩm nào?",
                n_none,
                f"Số người không chọn sản phẩm nào là: {tong} - {n_AUB} = {n_none} (người)."
            )
        ]

        cauTL += TL_answer_const(debai, ds_abcd, 0, 0, dong)

    return cauTL


def L10_C1_B2_TH019_TL_A_01(socau, dong=1):
    gt = []
    dem = len(gt)
    while dem < socau:
        # Giả lập các số học sinh
        x = np.random.randint(25, 35)  # Bóng đá
        y = np.random.randint(20, 30)  # Bóng bàn
        z = np.random.randint(15, 25)  # Cầu lông
        abc = np.random.randint(3, 8)
        ab = np.random.randint(abc + 5, abc + 12)
        bc = np.random.randint(abc + 3, abc + 8)
        ac = np.random.randint(abc + 3, abc + 8)

        # Số học sinh chỉ thích 1 môn
        m = x - (ab - abc) - (ac - abc) - abc
        n = y - (ab - abc) - (bc - abc) - abc
        p = z - (ac - abc) - (bc - abc) - abc

        if ab < x and ab < y and bc < y and bc < z and ac < x and ac < z and m > 0 and n > 0 and p > 0:
            v = (x, y, z, ab, bc, ac, abc, m, n, p)
            if v not in gt:
                gt.append(v)
                dem += 1

    cauTL = ''
    for v in gt:
        x, y, z, ab, bc, ac, abc, m, n, p = v

        debai = f"Câu lạc bộ thể thao có {x} học sinh yêu thích bóng đá, {y} học sinh yêu thích bóng bàn, {z} học sinh yêu thích cầu lông. Có {ab} học sinh thích cả bóng đá và bóng bàn, {bc} học sinh thích cả bóng bàn và cầu lông, {ac} học sinh thích cả bóng đá và cầu lông, và {abc} học sinh thích cả ba môn."

        # Code TikZ cho biểu đồ Venn 3 tập hợp
        tikz_venn = f"""
        \\begin{{tikzpicture}}
            \\def\\firstcircle{{(0,0) circle (1.5cm)}}
            \\def\\secondcircle{{(60:2cm) circle (1.5cm)}}
            \\def\\thirdcircle{{(0:2cm) circle (1.5cm)}}
            \\draw \\firstcircle node[below left] {{BĐ}};
            \\draw \\secondcircle node[above] {{BB}};
            \\draw \\thirdcircle node[below right] {{CL}};
            \\node at (1,0.6) {{{abc}}}; 
            \\node at (-0.3,0.3) {{{m}}};
            \\node at (2.3,0.3) {{{p}}};
            \\node at (1,1.5) {{{n}}};
        \\end{{tikzpicture}}"""

        hoi_a = f"Vẽ biểu đồ Venn biểu diễn các tập hợp trên."
        giai_a = f"Biểu đồ Venn được vẽ bằng TikZ như sau: \\n {tikz_venn}"

        hoi_b = f"Tính tổng số học sinh chỉ thích duy nhất một môn."
        dap_b = m + n + p
        giai_b = f"Tổng số học sinh chỉ thích một môn là: $S = {m} + {n} + {p} = {dap_b}$."

        ds_abcd = [
            (hoi_a, "\\text{Hình vẽ}", giai_a),
            (hoi_b, dap_b, giai_b)
        ]

        cauTL += TL_answer_text(debai, ds_abcd, 0, 0, dong)

    return cauTL

def L10_C1_B2_VD021_SA_B_01(socau, dang=2):
    r"""Tìm tham số m để khoảng/đoạn chứa đúng k số nguyên (dương, âm...).

    SUA 29/09/2026 (co Lan: "cau nay khong the la muc do NB duoc"): truoc
    day la L10_C1_B2_NB017_SA_C_01. Phai liet ke so nguyen theo kieu ngoac,
    loc theo loai roi suy nguoc ra tham so -> muc VD, doi sang
    L10_C1_B2_VD021 (khoang, doan, nua khoang tren truc so).
    """

    BIEN = 60          # miền quét tham số m để kiểm tra tính duy nhất
    A_MIN, A_MAX = -30, 30

    def dem_phan_tu(loai, trai, phai, a, m):
        """Đếm số phần tử nguyên thoả loại, trong khoảng (a;m) theo kiểu ngoặc trai/phai."""
        lo = a if trai == "[" else a + 1
        hi = m if phai == "]" else m - 1
        if lo > hi:
            return 0
        if loai == "duong":
            lo2 = max(lo, 1)
            return max(0, hi - lo2 + 1) if hi >= lo2 else 0
        elif loai == "am":
            hi2 = min(hi, -1)
            return max(0, hi2 - lo + 1) if hi2 >= lo else 0
        elif loai == "khong_am":
            lo2 = max(lo, 0)
            return max(0, hi - lo2 + 1) if hi >= lo2 else 0
        elif loai == "khong_duong":
            hi2 = min(hi, 0)
            return max(0, hi2 - lo + 1) if hi2 >= lo else 0
        else:  # "nguyen"
            return hi - lo + 1

    def m_hop_le_duy_nhat(loai, trai, phai, a, m, so_luong):
        """Kiểm tra m là NGHIỆM NGUYÊN DUY NHẤT trong miền quét [-BIEN, BIEN]."""
        nghiem = [
            mm for mm in range(-BIEN, BIEN + 1)
            if mm > a and dem_phan_tu(loai, trai, phai, a, mm) == so_luong
        ]
        if len(nghiem) != 1:
            return False
        # nếu nghiệm chạm biên quét -> nghi ngờ còn kéo dài vô hạn, loại bỏ
        if nghiem[0] in (-BIEN, BIEN):
            return False
        return nghiem[0] == m

    gt = []
    dem = 0

    while dem < socau:

        loai = random.choice(["duong", "am", "khong_am", "khong_duong", "nguyen"])
        trai = random.choice(["(", "["])
        phai = random.choice([")", "]"])

        a = random.randint(A_MIN, A_MAX - 1)
        so_luong = random.randint(1, 6)

        ok = False

        for m in range(a + 1, A_MAX + 20):
            if dem_phan_tu(loai, trai, phai, a, m) != so_luong:
                continue
            if not m_hop_le_duy_nhat(loai, trai, phai, a, m, so_luong):
                continue

            gt_mau = (loai, trai, phai, a, m, so_luong)
            if gt_mau not in gt:
                gt.append(gt_mau)
                dem += 1
                ok = True
            break

        if not ok:
            continue

    cauSA = ''

    ten_loai = {
        "duong": "số nguyên dương",
        "am": "số nguyên âm",
        "khong_am": "số nguyên không âm",
        "khong_duong": "số nguyên không dương",
        "nguyen": "số nguyên",
    }

    for loai, trai, phai, a, m, so_luong in gt:

        ten = ten_loai[loai]

        debai = (
            f"Tìm giá trị nguyên của tham số $m$ (với $m > {a}$) để tập hợp "
            f"$\\left{trai}{a};m\\right{phai}$ "
            f"chứa đúng {so_luong} {ten}."
        )

        # SUA 29/09/2026 (co Lan duyet): loi giai cu viet
        # "(a;m] = {cac so nguyen}" - SAI, vi nua khoang la tap so THUC,
        # khong bang tap may so nguyen; hon nua khi hoi so nguyen duong/am
        # thi danh sach chi la cac so da loc. Nay giai theo huong van dung:
        # tim so thu k va so thu k+1 cung loai, dat dieu kien cho m.
        def dung_loai(x):
            return {"duong": x > 0, "am": x < 0, "khong_am": x >= 0,
                    "khong_duong": x <= 0, "nguyen": True}[loai]

        lo = a if trai == "[" else a + 1
        day_so = [x for x in range(lo, lo + 200) if dung_loai(x)][:so_luong + 1]
        t_k, t_sau = day_so[so_luong - 1], day_so[so_luong]
        # m duy nhat (da loc o tren) nen hai so nay lien tiep nhau
        assert t_sau == t_k + 1
        if phai == "]":
            dk = f"{t_k} \\le m < {t_sau}"
            assert m == t_k
        else:
            dk = f"{t_k} < m \\le {t_sau}"
            assert m == t_sau
        ds = day_so[:so_luong]
        lietke = "; ".join(str(x) for x in ds)
        khoang = f"\\left{trai}{a};m\\right{phai}"

        giai = (
            f"Kể từ đầu mút trái, các {ten} có thể thuộc ${khoang}$ lần lượt "
            f"là ${'; '.join(str(x) for x in day_so)}; \\ldots$\\\\\n"
            f"Tập hợp chứa đúng {so_luong} {ten} khi và chỉ khi nó chứa "
            f"${t_k}$ nhưng không chứa ${t_sau}$, tức là ${dk}$.\\\\\n"
            f"Vì $m$ nguyên nên $m = {m}$. Khi đó các {ten} thuộc "
            f"$\\left{trai}{a};{m}\\right{phai}$ là ${lietke}$."
        )

        dsnhieu = []
        while len(dsnhieu) < 3:
            nhieu = m + random.choice([-3, -2, -1, 1, 2, 3])
            if nhieu != m and nhieu not in dsnhieu:
                dsnhieu.append(nhieu)

        cauSA += MC_SA_answer_const(debai, m, dsnhieu, giai, 0, 0, dang)

    return cauSA


# =====================================================================
# BỔ SUNG BA DẠNG CHO CHƯƠNG 1 (29/09/2026)
# ---------------------------------------------------------------------
# Ma trận đề hệ số 1 đòi ba dạng này nhưng Mapping chưa khai, nên mỗi
# lần ra đề chương 1 đều thiếu câu. Ba dạng đó là:
#     VD014_TL_A   tự luận về mệnh đề kéo theo và mệnh đề đảo
#     VD020_SA_A   trả lời ngắn, đếm phần tử tập hợp trong bài toán thực tế
#     VD021_TL_A   tự luận về phép toán tập hợp chứa tham số
# =====================================================================

def _ba_nhieu(dapso, ung_vien, buoc=None):
    """Ba phuong an nhieu doi mot khac nhau va khac dap so."""
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


def L10_C1_B1_VD014_TL_A_01(socau, dong=1):
    """Tự luận: xét tính đúng sai của mệnh đề kéo theo và của mệnh đề đảo."""
    # (boi, uoc): "n chia het cho boi" keo theo "n chia het cho uoc" la MENH DE DUNG
    CAP = [(6, 3), (6, 2), (4, 2), (9, 3), (10, 5), (8, 4), (12, 4), (15, 5)]
    gt = []
    while len(gt) < socau:
        boi, uoc = random.choice(CAP)
        nguoc = random.choice([False, True])   # co dao vai tro hai menh de khong
        if (boi, uoc, nguoc) not in gt:
            gt.append((boi, uoc, nguoc))

    cauTN = ''
    for boi, uoc, nguoc in gt:
        # P => Q dung khi so cua P la BOI cua so trong Q
        sP, sQ = (uoc, boi) if nguoc else (boi, uoc)
        pq_dung = (sP % sQ == 0)
        qp_dung = (sQ % sP == 0)
        # phan vi du khi menh de sai: so chia het cho so nho ma khong chia het cho so lon
        vd_pq = sQ if not pq_dung else None
        vd_qp = sP if not qp_dung else None

        debai = (r"Cho $n$ là một số tự nhiên và hai mệnh đề\\ "
                 r"$P$: ``$n$ chia hết cho $%d$'' \quad và \quad $Q$: ``$n$ chia hết cho $%d$''."
                 % (sP, sQ))
        ds_abcd = [
            (r"Xét tính đúng sai của mệnh đề $P \Rightarrow Q$.",
             r"\text{%s}" % ("Đúng" if pq_dung else "Sai"),
             (r"Mọi số chia hết cho $%d$ đều chia hết cho $%d$ (vì $%d$ chia hết cho $%d$), "
              r"nên $P \Rightarrow Q$ là mệnh đề \textbf{đúng}." % (sP, sQ, sP, sQ))
             if pq_dung else
             (r"Lấy $n = %d$: khi đó $n$ chia hết cho $%d$ nên $P$ đúng, nhưng $n$ không "
              r"chia hết cho $%d$ nên $Q$ sai.\\ "
              r"Có trường hợp $P$ đúng mà $Q$ sai, vậy $P \Rightarrow Q$ là mệnh đề "
              r"\textbf{sai}." % (vd_pq, sP, sQ))),
            (r"Xét tính đúng sai của mệnh đề đảo $Q \Rightarrow P$.",
             r"\text{%s}" % ("Đúng" if qp_dung else "Sai"),
             (r"Mọi số chia hết cho $%d$ đều chia hết cho $%d$, nên mệnh đề đảo "
              r"$Q \Rightarrow P$ \textbf{đúng}." % (sQ, sP))
             if qp_dung else
             (r"Lấy $n = %d$: khi đó $n$ chia hết cho $%d$ nên $Q$ đúng, nhưng $n$ không "
              r"chia hết cho $%d$ nên $P$ sai.\\ "
              r"Vậy mệnh đề đảo $Q \Rightarrow P$ \textbf{sai}." % (vd_qp, sQ, sP))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN



def _vd014_tl_cau(debai_dau, A, B, ab, ba, nguoc):
    r"""Ghép một câu tự luận "xét P => Q và mệnh đề đảo Q => P".

    ab = (A => B đúng?, lời giải), ba = (B => A đúng?, lời giải).
    nguoc = True thì đổi vai: P là B, Q là A.
    """
    P, Q, (pq, lg_pq), (qp, lg_qp) = (B, A, ba, ab) if nguoc else (A, B, ab, ba)
    debai = (debai_dau + r"\\ $P$: ``%s'' \quad và \quad $Q$: ``%s''." % (P, Q))
    return debai, [
        (r"Xét tính đúng sai của mệnh đề $P \Rightarrow Q$.",
         r"\text{%s}" % ("Đúng" if pq else "Sai"),
         lg_pq + (r" Vậy $P \Rightarrow Q$ là mệnh đề \textbf{%s}." % ("đúng" if pq else "sai"))),
        (r"Phát biểu mệnh đề đảo $Q \Rightarrow P$ và xét tính đúng sai của nó.",
         r"\text{%s}" % ("Đúng" if qp else "Sai"),
         r"Mệnh đề đảo: ``Nếu %s thì %s''.\\ " % (Q, P) + lg_qp +
         (r" Vậy $Q \Rightarrow P$ là mệnh đề \textbf{%s}." % ("đúng" if qp else "sai"))),
    ]


_VD014_HINH = [
    (r"tứ giác $ABCD$ là hình chữ nhật", r"tứ giác $ABCD$ có hai đường chéo bằng nhau",
     (True, r"Hình chữ nhật luôn có hai đường chéo bằng nhau."),
     (False, r"Hình thang cân (không có góc vuông) có hai đường chéo bằng nhau nhưng "
             r"không phải hình chữ nhật.")),
    (r"tứ giác $ABCD$ là hình vuông", r"tứ giác $ABCD$ là hình thoi",
     (True, r"Hình vuông có bốn cạnh bằng nhau nên là hình thoi."),
     (False, r"Hình thoi có một góc bằng $60^{\circ}$ không phải hình vuông.")),
    (r"tam giác $ABC$ đều", r"tam giác $ABC$ cân",
     (True, r"Tam giác đều có ba cạnh bằng nhau nên cân tại mỗi đỉnh."),
     (False, r"Tam giác cân tại $A$ có $\widehat{A} = 40^{\circ}$ không phải tam giác đều.")),
    (r"tam giác $ABC$ vuông tại $A$", r"$BC^2 = AB^2 + AC^2$",
     (True, r"Theo định lí Pythagore."),
     (True, r"Theo định lí Pythagore đảo.")),
    (r"tứ giác $ABCD$ là hình bình hành",
     r"hai đường chéo của tứ giác $ABCD$ cắt nhau tại trung điểm của mỗi đường",
     (True, r"Đó là tính chất của hình bình hành."),
     (True, r"Đó là dấu hiệu nhận biết hình bình hành.")),
    (r"tứ giác $ABCD$ là hình thoi", r"tứ giác $ABCD$ có hai đường chéo vuông góc",
     (True, r"Hai đường chéo của hình thoi vuông góc với nhau."),
     (False, r"Tứ giác có $AB = AD$, $CB = CD$ nhưng $AB \ne CB$ có hai đường chéo vuông "
             r"góc mà không phải hình thoi.")),
    (r"hai tam giác bằng nhau", r"hai tam giác có diện tích bằng nhau",
     (True, r"Hai tam giác bằng nhau thì có diện tích bằng nhau."),
     (False, r"Tam giác có đáy $4$, chiều cao $3$ và tam giác có đáy $6$, chiều cao $2$ "
             r"cùng có diện tích $6$ nhưng không bằng nhau.")),
    (r"tam giác $ABC$ có hai góc bằng $60^{\circ}$", r"tam giác $ABC$ đều",
     (True, r"Góc còn lại bằng $180^{\circ} - 2\cdot 60^{\circ} = 60^{\circ}$ nên tam giác đều."),
     (True, r"Tam giác đều có cả ba góc bằng $60^{\circ}$.")),
]


def L10_C1_B1_VD014_TL_A_02(socau, dong=1):
    r"""Tự luận: xét mệnh đề kéo theo và mệnh đề đảo - bối cảnh HÌNH HỌC.

    CLAUDE THEM 29/09/2026 - bien the 02 (cung dang "Xet tinh dung sai cua
    menh de keo theo va menh de dao"; _01 dung tinh chia het). Co Lan duyet.
    """
    ds = list(range(len(_VD014_HINH)))
    random.shuffle(ds)
    cauTN = ''
    for i in ds[:min(socau, len(ds))]:
        A, B, ab, ba = _VD014_HINH[i]
        debai, ds_abcd = _vd014_tl_cau(r"Cho hai mệnh đề", A, B, ab, ba,
                                       random.choice([False, True]))
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C1_B1_VD014_TL_A_03(socau, dong=1):
    r"""Tự luận: xét mệnh đề kéo theo và mệnh đề đảo - bối cảnh SỐ THỰC
    (bình phương, giá trị tuyệt đối, phương trình bậc hai), số thay đổi.

    CLAUDE THEM 29/09/2026 - bien the 03. Co Lan duyet.
    """
    cauTN = ''
    da = []
    lan = 0
    while len(da) < socau and lan < 200:
        lan += 1
        kieu = random.randrange(4)
        a = random.randint(2, 9)
        b = random.choice([k for k in range(-9, 10) if k not in (0, a, -a)])
        if (kieu, a, b) in da:
            continue
        da.append((kieu, a, b))
        if kieu == 0:
            A, B = r"$x > %d$" % a, r"$x^2 > %d$" % (a * a)
            ab = (True, r"Nếu $x > %d$ thì $x > 0$ nên $x^2 > %d^2 = %d$." % (a, a, a * a))
            ba = (False, r"Lấy $x = %d$: $x^2 = %d > %d$ nhưng $x < %d$."
                  % (-a - 1, (a + 1) ** 2, a * a, a))
        elif kieu == 1:
            A, B = r"$x = %d$" % a, r"$x^2 = %d$" % (a * a)
            ab = (True, r"Thay $x = %d$ được $x^2 = %d$." % (a, a * a))
            ba = (False, r"Lấy $x = %d$: $x^2 = %d$ nhưng $x \ne %d$." % (-a, a * a, a))
        elif kieu == 2:
            A, B = r"$\left|x\right| < %d$" % a, r"$x < %d$" % a
            ab = (True, r"$\left|x\right| < %d \Leftrightarrow -%d < x < %d$ nên $x < %d$."
                  % (a, a, a, a))
            ba = (False, r"Lấy $x = %d$: $x < %d$ nhưng $\left|x\right| = %d > %d$."
                  % (-a - 1, a, a + 1, a))
        else:
            tong, tich = a + b, a * b
            pt = (r"x^2" + (r" - %dx" % tong if tong > 0 else (r" + %dx" % -tong if tong < 0 else "")) +
                  (r" + %d" % tich if tich > 0 else r" - %d" % -tich) + " = 0")
            pt = pt.replace(" 1x", " x")
            A, B = r"$x = %d$" % a, r"$%s$" % pt
            ab = (True, r"Thay $x = %d$ vào vế trái được $%d^2 %s %s = 0$."
                  % (a, a, (r"- %d\cdot %d" % (tong, a)) if tong >= 0 else (r"+ %d\cdot %d" % (-tong, a)),
                     (r"+ %d" % tich) if tich >= 0 else (r"- %d" % -tich)))
            ba = (False, r"Phương trình $%s$ có hai nghiệm $x = %d$ và $x = %d$. Với $x = %d$ "
                         r"thì phương trình được thoả mãn nhưng $x \ne %d$." % (pt, a, b, b, a))
        debai, ds_abcd = _vd014_tl_cau(r"Cho $x$ là số thực và hai mệnh đề", A, B, ab, ba,
                                       random.choice([False, True]))
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN

def L10_C1_B2_VD020_SA_A_01(socau, dang=2):
    """Trả lời ngắn: đếm số phần tử bằng công thức n(A hợp B) = n(A) + n(B) - n(A giao B)."""
    BOI_CANH = [("lớp 10A", "thích môn Toán", "thích môn Văn", "học sinh"),
                ("tổ dân phố", "trồng cây cảnh", "nuôi cá cảnh", "hộ gia đình"),
                ("câu lạc bộ", "chơi cầu lông", "chơi bóng bàn", "thành viên")]
    gt = []
    while len(gt) < socau:
        n = random.randint(35, 50)
        ca_hai = random.randint(5, 12)
        chi_a = random.randint(6, 16)
        chi_b = random.randint(6, 16)
        khong = n - (chi_a + chi_b + ca_hai)
        if khong < 2:                      # phai con it nhat vai nguoi khong thuoc hai nhom
            continue
        i = random.randrange(len(BOI_CANH))
        v = (i, n, chi_a, chi_b, ca_hai, khong)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for i, n, chi_a, chi_b, ca_hai, khong in gt:
        noi, hd1, hd2, dv = BOI_CANH[i]
        A = chi_a + ca_hai                 # so nguoi thuoc nhom thu nhat
        B = chi_b + ca_hai
        debai = (r"Một %s có $%d$ %s, trong đó có $%d$ %s %s, $%d$ %s %s và $%d$ %s "
                 r"%s cả hai. Hỏi có bao nhiêu %s không %s và cũng không %s?"
                 % (noi, n, dv, A, dv, hd1, B, dv, hd2, ca_hai, dv,
                    hd1.split()[0], dv, hd1, hd2))
        giai = (r"Gọi $A$ là tập các %s %s, $B$ là tập các %s %s.\\ "
                r"Ta có $n\left(A\right) = %d$, $n\left(B\right) = %d$, "
                r"$n\left(A \cap B\right) = %d$.\\ "
                r"Số %s thuộc ít nhất một trong hai nhóm là\\ "
                r"$n\left(A \cup B\right) = n\left(A\right) + n\left(B\right) "
                r"- n\left(A \cap B\right) = %d + %d - %d = %d$.\\ "
                r"Vậy số %s không thuộc nhóm nào là $%d - %d = %d$."
                % (dv, hd1, dv, hd2, A, B, ca_hai, dv, A, B, ca_hai, A + B - ca_hai,
                   dv, n, A + B - ca_hai, khong))
        dung = str(khong)
        ds = _ba_nhieu(dung, [str(n - A - B), str(A + B - ca_hai), str(n - ca_hai)],
                       buoc=lambda k: str(khong + k + 1))
        cauTN += MC_SA_answer_text(debai, dung, ds, giai, 0, 0, dang)
    return cauTN


def L10_C1_B2_VD021_TL_A_01(socau, dong=1):
    """Tự luận: phép toán tập hợp chứa tham số - hai câu hỏi bổ sung cho nhau.

    Dùng lại đúng phần sinh đề và lời giải đã kiểm chứng của dạng VD021
    (xem _VD021_de_giai): ý (a) đếm số giá trị của m để giao bằng rỗng,
    ý (b) tìm m nhỏ nhất để giao khác rỗng. Cả hai đều cần n < a nên dùng
    chung được một bộ số liệu.
    """
    gt = []
    while len(gt) < socau:
        a_val = int(np.random.randint(-15, 5))
        b_val = int(np.random.randint(a_val + 5, 16))
        n_val = int(np.random.randint(a_val - 8, a_val - 1))
        if a_val - n_val - 1 <= 0:
            continue
        v = (a_val, b_val, n_val)
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for a_val, b_val, n_val in gt:
        _, dem, giai_dem = _VD021_de_giai(3, a_val, b_val, n_val)
        _, nho_nhat, giai_nn = _VD021_de_giai(4, a_val, b_val, n_val)
        debai = (r"Cho hai tập hợp $A = \left[ %d; %d \right]$ và "
                 r"$B = \left( %d; m \right]$, trong đó $m$ là số nguyên sao cho "
                 r"$B \ne \varnothing$." % (a_val, b_val, n_val))
        ds_abcd = [
            (r"Có bao nhiêu giá trị nguyên của $m$ để $A \cap B = \varnothing$?",
             r"%d" % dem, giai_dem),
            (r"Tìm giá trị nguyên nhỏ nhất của $m$ để $A \cap B \ne \varnothing$.",
             r"%d" % nho_nhat, giai_nn),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


# =====================================================================
# BIẾN THỂ LẤY TỪ GIÁO ÁN BÀI 1 (MỆNH ĐỀ) CỦA CÔ LAN (29/09/2026)
# CLAUDE THEM 29/09/2026 - co Lan duyet lai. Moi tinh dung sai trong cac
# ham duoi day deu do Python tinh (chia het, so nguyen to, delta...), khong
# go tay.
# =====================================================================

from sympy import Rational


def _la_nguyen_to(n):
    n = int(n)
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def _md_so(loai=None):
    r"""Một mệnh đề toán học về số, kèm phủ định, chân trị và lí do.

    Trả về dict: p (mệnh đề), phu (phủ định), dung (True/False), ly_do.
    """
    if loai is None:
        loai = random.randint(0, 8)
    if loai == 0:
        m = random.choice([3, 4, 6, 9, 11, 15, 25])
        N = random.randint(1000, 3000)
        if random.random() < 0.5:
            N -= N % m
        q, r = divmod(N, m)
        return dict(p=r"Số $%d$ chia hết cho $%d$" % (N, m), phu=r"Số $%d$ không chia hết cho $%d$" % (N, m),
                    dung=(r == 0), ly_do=(r"$%d = %d\cdot %d$" % (N, m, q) if r == 0 else
                                          r"$%d = %d\cdot %d + %d$ (dư $%d$)" % (N, m, q, r, r)))
    if loai == 1:
        s = random.randint(4, 45)
        k = s * s + random.choice([0, 0, 1, -1, 2])
        can = int(math.isqrt(k))
        dung = can * can == k
        return dict(p=r"Số $%d$ là số chính phương" % k, phu=r"Số $%d$ không là số chính phương" % k,
                    dung=dung, ly_do=(r"$%d = %d^2$" % (k, can) if dung else
                                      r"$%d^2 = %d < %d < %d = %d^2$" % (can, can * can, k, (can + 1) ** 2, can + 1)))
    if loai == 2:
        s = random.randint(2, 12)
        k = s * s if random.random() < 0.5 else s * s + random.randint(1, 2 * s)
        can = int(math.isqrt(k))
        dung = can * can == k
        return dict(p=r"$\sqrt{%d}$ là số hữu tỉ" % k, phu=r"$\sqrt{%d}$ không là số hữu tỉ" % k,
                    dung=dung, ly_do=(r"$\sqrt{%d} = %d$" % (k, can) if dung else
                                      r"$%d$ không là số chính phương nên $\sqrt{%d}$ là số vô tỉ" % (k, k)))
    if loai == 3:
        k = random.randint(2, 2025)
        if random.random() < 0.5:
            return dict(p=r"$\left|-%d\right| \le 0$" % k, phu=r"$\left|-%d\right| > 0$" % k, dung=False,
                        ly_do=r"$\left|-%d\right| = %d > 0$" % (k, k))
        return dict(p=r"$\left|-%d\right| = %d$" % (k, k), phu=r"$\left|-%d\right| \ne %d$" % (k, k), dung=True,
                    ly_do=r"giá trị tuyệt đối của số âm là số đối của nó")
    if loai == 4:
        c = random.randint(2, 5)
        m, n = random.sample(range(2, 6), 2)
        if random.random() < 0.5:
            return dict(p=r"$%d^{%d} + %d^{%d} = %d^{%d + %d}$" % (c, m, c, n, c, m, n),
                        phu=r"$%d^{%d} + %d^{%d} \ne %d^{%d + %d}$" % (c, m, c, n, c, m, n), dung=False,
                        ly_do=r"vế trái bằng $%d$, vế phải bằng $%d$" % (c ** m + c ** n, c ** (m + n)))
        return dict(p=r"$%d^{%d}\cdot %d^{%d} = %d^{%d + %d}$" % (c, m, c, n, c, m, n),
                    phu=r"$%d^{%d}\cdot %d^{%d} \ne %d^{%d + %d}$" % (c, m, c, n, c, m, n), dung=True,
                    ly_do=r"nhân hai luỹ thừa cùng cơ số thì cộng số mũ")
    if loai == 5:
        b = random.randint(-8, 8)
        c = random.randint(-10, 12)
        d = b * b - 4 * c
        bt = _tex_bac2(1, b, c)
        return dict(p=r"Phương trình $%s = 0$ có nghiệm" % bt, phu=r"Phương trình $%s = 0$ vô nghiệm" % bt,
                    dung=(d >= 0), ly_do=r"$\Delta = %s - 4\cdot %s = %d %s 0$"
                    % (("%d^2" % b) if b >= 0 else "(%d)^2" % b, ("%d" % c) if c >= 0 else "(%d)" % c, d,
                       r"\ge" if d >= 0 else "<"))
    if loai == 6:
        # (u x - v)(w x - z) = 0, hệ số nguyên; có nghiệm nguyên khi u = 1
        w = random.choice([2, 3])
        z = random.choice([i for i in range(-7, 8) if i % w])
        u = random.choice([1, 2, 3])
        v = random.choice([i for i in range(-5, 6) if i and (u == 1 or i % u)])
        a2, b2, c2 = u * w, -(u * z + v * w), v * z
        g = math.gcd(math.gcd(abs(a2), abs(b2)), abs(c2))
        a2, b2, c2 = a2 // g, b2 // g, c2 // g
        ngh = sorted({Rational(v, u), Rational(z, w)})
        co = any(n_.q == 1 for n_ in ngh)
        bt = _tex_bac2(a2, b2, c2)
        return dict(p=r"Phương trình $%s = 0$ có nghiệm nguyên" % bt,
                    phu=r"Phương trình $%s = 0$ không có nghiệm nguyên" % bt, dung=co,
                    ly_do=r"phương trình có %s $%s$" % ("nghiệm" if len(ngh) == 1 else "các nghiệm",
                                                     r";\ ".join("x = " + _tex_so(n_) for n_ in ngh)))
    if loai == 7:
        tu, mau, dung = random.choice([(22, 7, True), (10, 3, True), (16, 5, True), (157, 50, False),
                                       (31, 10, False), (25, 8, False)])
        return dict(p=r"$\pi < \dfrac{%d}{%d}$" % (tu, mau), phu=r"$\pi \ge \dfrac{%d}{%d}$" % (tu, mau),
                    dung=dung, ly_do=r"$\pi \approx 3{,}1416$ còn $\dfrac{%d}{%d} = %s$"
                    % (tu, mau, ("%.4f" % (tu / mau)).replace(".", "{,}")))
    k = random.choice([i for i in range(2, 120) if i % 2 or i == 2])
    nt = _la_nguyen_to(k)
    uoc = next((d for d in range(2, k) if k % d == 0), None)
    return dict(p=r"Số $%d$ là số nguyên tố" % k, phu=r"Số $%d$ không là số nguyên tố" % k, dung=nt,
                ly_do=(r"$%d$ chỉ có hai ước là $1$ và $%d$" % (k, k) if nt else
                       r"$%d$ chia hết cho $%d$" % (k, uoc)))


def _tex_so(v):
    v = Rational(v)
    if v.q == 1:
        return "%d" % v.p
    return (r"-\dfrac{%d}{%d}" if v < 0 else r"\dfrac{%d}{%d}") % (abs(v.p), v.q)


def _tex_bac2(a_, b_, c_):
    s = ("x^2" if a_ == 1 else "-x^2" if a_ == -1 else "%dx^2" % a_)
    if b_:
        s += (" + " if b_ > 0 else " - ") + ("" if abs(b_) == 1 else "%d" % abs(b_)) + "x"
    if c_:
        s += (" + %d" % c_) if c_ > 0 else (" - %d" % -c_)
    return s


def L10_C1_B1_TH003_MC_A_02(socau, dang=1):
    r"""Mệnh đề toán học về SỐ nào đúng (sai)? Chân trị do Python tính.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH003_MC_A, theo bai "Xet tinh
    dung sai: 1993 chia het cho 3, can 12 huu ti, |-1997| <= 0, pi < 10/3,
    phuong trinh 3x + 7 = 0 co nghiem" trong giao an Bai 1. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        hoi_dung = random.choice([True, False])
        chon, loai_da = None, set()
        cung = []
        cac_loai = random.sample(range(9), 9)
        kieu_da = set()
        for _t in range(400):
            lo = cac_loai[_t % 9]
            m = _md_so(lo)
            if m["p"] in loai_da or (lo in kieu_da and _t < 300):
                continue
            if m["dung"] == hoi_dung and chon is None:
                chon = m
                loai_da.add(m["p"]); kieu_da.add(lo)
            elif m["dung"] != hoi_dung and len(cung) < 3:
                cung.append(m)
                loai_da.add(m["p"]); kieu_da.add(lo)
            if chon and len(cung) == 3:
                break
        tu = "đúng" if hoi_dung else r"\textbf{sai}"
        debai = r"Mệnh đề nào sau đây là mệnh đề %s?" % tu
        giai = (r"%s là mệnh đề %s vì %s.\\ " % (chon["p"], "đúng" if hoi_dung else "sai", chon["ly_do"])
                + r"\\ ".join(r"%s: mệnh đề %s (%s)." % (m["p"], "đúng" if m["dung"] else "sai", m["ly_do"])
                              for m in cung))
        cauTN += MC_SA_answer_text(debai, chon["p"], [m["p"] for m in cung], giai, 0, 0, dang)
    return cauTN


def L10_C1_B1_TH003_TL_B_02(socau, dong=1):
    r"""Tự luận: lập mệnh đề phủ định của ba mệnh đề về số và xét tính đúng sai
    của từng mệnh đề phủ định.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH003_TL_B, theo bai "A: 5/1,2
    la phan so; B: phuong trinh x^2 + 3x + 2 = 0 co nghiem; C: 2^2 + 2^3 =
    2^(2+3); D: 2025 chia het cho 15" trong giao an Bai 1. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        ds, da = [], set()
        cac_loai = random.sample(range(9), 3)
        while len(ds) < 3:
            m = _md_so(cac_loai[len(ds)])
            if m["p"] not in da:
                ds.append(m)
                da.add(m["p"])
        ten = ["A", "B", "C"]
        debai = (r"Cho các mệnh đề " + "; ".join(r"$%s$: ``%s''" % (t, m["p"]) for t, m in zip(ten, ds))
                 + r". Lập mệnh đề phủ định của mỗi mệnh đề và xét tính đúng sai của mệnh đề phủ định đó.")
        ds_abcd = []
        for t, m in zip(ten, ds):
            phu_dung = not m["dung"]
            ds_abcd.append((r"Mệnh đề $\overline{%s}$." % t,
                            r"\overline{%s}\ \text{%s}" % (t, "đúng" if phu_dung else "sai"),
                            r"$\overline{%s}$: ``%s''. Vì %s nên $%s$ %s, do đó $\overline{%s}$ %s."
                            % (t, m["phu"], m["ly_do"], t, "đúng" if m["dung"] else "sai", t,
                               "đúng" if phu_dung else "sai")))
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C1_B1_TH003_TL_A_02(socau, dong=1):
    r"""Tự luận: dùng kí hiệu $\forall$, $\exists$ viết mệnh đề cho bằng lời rồi
    xét tính đúng sai.

    CLAUDE THEM 29/09/2026 - bien the 02 cua TH003_TL_A, theo cac vi du "Voi
    moi so thuc x, x^2 + 1 > 0", "Voi moi so tu nhien n, n^2 + n chia het cho
    6", "Ton tai so nguyen x sao cho 2x + 1 = 0" trong giao an Bai 1.
    Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        # a) với mọi số thực x, x^2 + k > 0  (k > 0 đúng; k < 0 sai)
        k = random.choice([i for i in range(-9, 10) if i])
        dau_k = "+ %d" % k if k > 0 else "- %d" % -k
        ky_a = r"\forall x\in\mathbb{R},\ x^2 %s > 0" % dau_k
        if k > 0:
            ga = (r"Với mọi $x$ thực, $x^2 %s \ge %d > 0$. Mệnh đề đúng." % (dau_k, k))
        else:
            ga = (r"Lấy $x = 0$ thì $0^2 %s = %d$, không lớn hơn $0$. Mệnh đề sai." % (dau_k, k))
        # b) tồn tại số nguyên x sao cho a x + b = 0
        a_ = random.randint(2, 6)
        b_ = random.choice([i for i in range(-20, 21) if i])
        dung_b = b_ % a_ == 0
        dau_b = "+ %d" % b_ if b_ > 0 else "- %d" % -b_
        ky_b = r"\exists x\in\mathbb{Z},\ %dx %s = 0" % (a_, dau_b)
        nghiem = _tex_so(Rational(-b_, a_))
        gb = (r"Phương trình $%dx %s = 0$ có nghiệm duy nhất $x = %s$, %s số nguyên. Mệnh đề %s."
              % (a_, dau_b, nghiem, "là" if dung_b else "không là", "đúng" if dung_b else "sai"))
        # c) với mọi số tự nhiên n, n^2 + n chia hết cho m
        m = random.choice([2, 3, 4, 6])
        ky_c = r"\forall n\in\mathbb{N},\ \left(n^2 + n\right)\ \vdots\ %d" % m
        if m == 2:
            gc = (r"$n^2 + n = n(n + 1)$ là tích hai số tự nhiên liên tiếp nên luôn chia hết cho $2$. "
                  r"Mệnh đề đúng.")
        else:
            n0 = next(n for n in range(0, 20) if (n * n + n) % m)
            gc = (r"Lấy $n = %d$ thì $n^2 + n = %d$ không chia hết cho $%d$. Mệnh đề sai." % (n0, n0 * n0 + n0, m))
        debai = (r"Dùng kí hiệu $\forall$ hoặc $\exists$ để viết mỗi mệnh đề sau và xét tính đúng sai của nó.")
        ds_abcd = [
            (r"$P$: ``Với mọi số thực $x$, $x^2 %s > 0$''." % dau_k,
             ky_a + r";\ \text{%s}" % ("đúng" if k > 0 else "sai"), r"$P$: ``$%s$''. " % ky_a + ga),
            (r"$Q$: ``Tồn tại số nguyên $x$ sao cho $%dx %s = 0$''." % (a_, dau_b),
             ky_b + r";\ \text{%s}" % ("đúng" if dung_b else "sai"), r"$Q$: ``$%s$''. " % ky_b + gb),
            (r"$R$: ``Với mọi số tự nhiên $n$, $n^2 + n$ chia hết cho $%d$''." % m,
             ky_c + r";\ \text{%s}" % ("đúng" if m == 2 else "sai"), r"$R$: ``$%s$''. " % ky_c + gc),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def _keo_theo():
    r"""Một mệnh đề kéo theo cùng chân trị và lí do (phần số học có tham số)."""
    loai = random.randint(0, 5)
    if loai == 0:
        m = random.choice([6, 8, 10, 12, 15, 18, 20])
        d = random.choice([i for i in range(2, 10) if i != m])
        dung = m % d == 0
        return (r"Nếu số tự nhiên $a$ chia hết cho $%d$ thì $a$ chia hết cho $%d$" % (m, d), dung,
                (r"$%d = %d\cdot %d$ nên mọi bội của $%d$ đều là bội của $%d$" % (m, d, m // d, m, d)) if dung else
                (r"với $a = %d$: $a$ chia hết cho $%d$ nhưng không chia hết cho $%d$" % (m, m, d)))
    if loai == 1:
        d = random.randint(3, 9)
        if random.random() < 0.5:
            return (r"Nếu hai số tự nhiên $a$, $b$ cùng chia hết cho $%d$ thì $a + b$ chia hết cho $%d$" % (d, d),
                    True, r"$a = %dk$, $b = %dl$ thì $a + b = %d(k + l)$" % (d, d, d))
        return (r"Nếu $a + b$ chia hết cho $%d$ thì hai số tự nhiên $a$, $b$ cùng chia hết cho $%d$" % (d, d),
                False, r"với $a = 1$, $b = %d$: $a + b = %d$ chia hết cho $%d$ nhưng $a$ không chia hết cho $%d$"
                % (d - 1, d, d, d))
    BO = [
        (r"Nếu $a$ và $b$ là hai số tự nhiên chẵn thì $a + b$ là số chẵn", True, r"tổng hai số chẵn là số chẵn"),
        (r"Nếu $a + b$ là số chẵn thì $a$ và $b$ là hai số tự nhiên chẵn", False,
         r"với $a = 1$, $b = 3$: $a + b = 4$ chẵn nhưng $a$, $b$ đều lẻ"),
        (r"Nếu $a$ và $b$ là hai số tự nhiên lẻ thì $ab$ là số lẻ", True, r"tích hai số lẻ là số lẻ"),
        (r"Nếu $ab$ là số chẵn thì $a$ và $b$ là hai số tự nhiên chẵn", False,
         r"với $a = 2$, $b = 3$: $ab = 6$ chẵn nhưng $b$ lẻ"),
        (r"Nếu tứ giác $ABCD$ có bốn cạnh bằng nhau thì $ABCD$ là hình vuông", False,
         r"tứ giác có bốn cạnh bằng nhau là hình thoi, chưa chắc là hình vuông"),
        (r"Nếu tứ giác $ABCD$ là hình vuông thì $ABCD$ có bốn cạnh bằng nhau", True,
         r"hình vuông có bốn cạnh bằng nhau"),
        (r"Nếu tam giác $ABC$ có $AB^2 + AC^2 = BC^2$ thì tam giác $ABC$ vuông tại $A$", True,
         r"định lí Pythagore đảo"),
        (r"Nếu tam giác $ABC$ vuông thì $AB^2 + AC^2 = BC^2$", False,
         r"tam giác có thể vuông tại $B$ hoặc $C$, khi đó đẳng thức không đúng"),
        (r"Nếu $b^2 \ge 4ac$ thì phương trình $ax^2 + bx + c = 0$ $(a \ne 0)$ vô nghiệm", False,
         r"$b^2 \ge 4ac$ nghĩa là $\Delta \ge 0$, phương trình có nghiệm"),
        (r"Nếu $b^2 < 4ac$ thì phương trình $ax^2 + bx + c = 0$ $(a \ne 0)$ vô nghiệm", True,
         r"$b^2 < 4ac$ nghĩa là $\Delta < 0$"),
        (r"Nếu tam giác $ABC$ có hai góc bằng $60^{\circ}$ thì tam giác $ABC$ đều", True,
         r"góc còn lại bằng $180^{\circ} - 120^{\circ} = 60^{\circ}$"),
        (r"Nếu tam giác $ABC$ cân thì $AB = AC$", False, r"tam giác có thể cân tại $B$ hoặc $C$"),
        (r"Nếu hai tam giác bằng nhau thì hai tam giác đó đồng dạng", True,
         r"hai tam giác bằng nhau là trường hợp đặc biệt của đồng dạng (tỉ số $1$)"),
        (r"Nếu hai tam giác có bán kính đường tròn ngoại tiếp bằng nhau thì hai tam giác đó bằng nhau", False,
         r"hai tam giác vuông cùng cạnh huyền $2R$ nhưng cạnh góc vuông khác nhau"),
        (r"Nếu hai tam giác có diện tích bằng nhau thì hai tam giác đó bằng nhau", False,
         r"tam giác có cạnh đáy $4$, chiều cao $3$ và tam giác có cạnh đáy $6$, chiều cao $2$"),
    ]
    return random.choice(BO)


def L10_C1_B1_TH014_MC_C_01(socau, dang=1):
    r"""Xác định tính đúng sai của mệnh đề kéo theo: chọn mệnh đề kéo theo
    đúng (hoặc sai) trong bốn mệnh đề.

    CLAUDE THEM 29/09/2026 - dang MOI (mapping co ghi chu), theo cac vi du
    "a chia het cho 6 thi a chia het cho 3", "tu giac co bon canh bang nhau
    thi la hinh vuong", "b^2 >= 4ac thi phuong trinh vo nghiem" trong giao an
    Bai 1. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        hoi_dung = random.choice([True, False])
        chon, cung, da = None, [], set()
        for _t in range(500):
            t, d_, l = _keo_theo()
            khoa = t[:45]                   # hai câu cùng khuôn chỉ khác số thì coi là trùng
            if khoa in da:
                continue
            if d_ == hoi_dung and chon is None:
                chon = (t, d_, l); da.add(khoa)
            elif d_ != hoi_dung and len(cung) < 3:
                cung.append((t, d_, l)); da.add(khoa)
            if chon and len(cung) == 3:
                break
        debai = r"Mệnh đề nào sau đây là mệnh đề %s?" % ("đúng" if hoi_dung else r"\textbf{sai}")
        giai = (r"Mệnh đề ``%s'' %s vì %s.\\ " % (chon[0], "đúng" if hoi_dung else "sai", chon[2])
                + r"\\ ".join(r"``%s'' %s (%s)." % (t, "đúng" if d_ else "sai", l) for t, d_, l in cung))
        cauTN += MC_SA_answer_text(debai, chon[0], [t for t, _, _ in cung], giai, 0, 0, dang)
    return cauTN


def L10_C1_B1_NB001_MC_A_02(socau, dang=1):
    r"""Câu nào là mệnh đề / không là mệnh đề - có cả MỆNH ĐỀ CHỨA BIẾN (chưa
    xác định được đúng sai nên không là mệnh đề) và mệnh đề toán có số.

    CLAUDE THEM 29/09/2026 - bien the 02 cua NB001_MC_A, theo bai "Khong duoc
    di loi nay!; Bay gio la may gio?; 7 khong la so nguyen to; can 5 la so vo
    ti" trong giao an Bai 1. Co Lan duyet.
    """
    KHONG = [(r"Không được đi lối này!", "câu cầu khiến"), (r"Bây giờ là mấy giờ?", "câu hỏi"),
             (r"Hôm nay trời đẹp quá!", "câu cảm thán"), (r"Bạn có thích học Toán không?", "câu hỏi"),
             (r"Hãy giải bài tập này!", "câu cầu khiến"), (r"Ôi, bài này khó quá!", "câu cảm thán")]
    cauTN = ""
    for _ in range(socau):
        a_, b_ = random.randint(1, 9), random.randint(2, 15)
        m = random.randint(3, 9)
        bien = [(r"$x + %d > %d$" % (a_, b_), r"câu chứa biến $x$ chưa rõ giá trị nên chưa xác định được đúng sai"),
                (r"$n$ chia hết cho $%d$" % m, r"câu chứa biến $n$ chưa rõ giá trị nên chưa xác định được đúng sai"),
                (r"$2x - %d = 0$" % a_, r"câu chứa biến $x$ chưa rõ giá trị nên chưa xác định được đúng sai")]
        khong = random.sample(KHONG, 3) + random.sample(bien, 2)
        co = []
        for lo in random.sample(range(9), 3):
            md = _md_so(lo)
            co.append((md["p"], "mệnh đề %s" % ("đúng" if md["dung"] else "sai")))
        la_md = random.choice([True, False])
        if la_md:
            dung, nhieu = co[0], random.sample(khong, 3)
            debai = r"Câu nào sau đây là mệnh đề?"
        else:
            dung, nhieu = random.choice(khong), co
            debai = r"Câu nào sau đây \textbf{không} là mệnh đề?"
        giai = (r"``%s'': %s. " % dung + r"Các câu còn lại: "
                + "; ".join(r"``%s'' (%s)" % c_ for c_ in nhieu) + ".")
        cauTN += MC_SA_answer_text(debai, dung[0], [c_[0] for c_ in nhieu], giai, 0, 0, dang)
    return cauTN


def L10_C1_B1_VD014_MC_B_02(socau, dang=1):
    r"""Mệnh đề chứa biến $P(n)$: "$2^n + k$ là số nguyên tố" (hoặc
    "$n^2 + n + k$..."): đếm số giá trị $n$ trong một đoạn làm $P(n)$ đúng
    (sai).

    CLAUDE THEM 29/09/2026 - bien the 02 cua VD014_MC_B, theo vi du "voi moi
    n thuoc N*, 2^n + 3 la so nguyen to" trong giao an Bai 1. Hoi "co bao
    nhieu" (dung quy tac muc VD). Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        kieu = random.choice([0, 1])
        k = random.choice([1, 3, 5, 7, 9, 11]) if kieu == 0 else random.choice([1, 5, 11, 17, 41])
        N = random.randint(6, 10)
        f = (lambda n: 2 ** n + k) if kieu == 0 else (lambda n: n * n + n + k)
        bt = (r"2^n + %d" % k) if kieu == 0 else (r"n^2 + n + %d" % k)
        hoi_dung = random.choice([True, False])
        gia_tri = [(n, f(n), _la_nguyen_to(f(n))) for n in range(1, N + 1)]
        dem = sum(1 for _, _, nt in gia_tri if nt == hoi_dung)
        if dem in (0, N):
            continue
        so += 1
        debai = (r"Cho mệnh đề chứa biến $P(n)$: ``$%s$ là số nguyên tố'' với $n \in \mathbb{N}^{*}$. "
                 r"Có bao nhiêu số $n$ thoả mãn $1 \le n \le %d$ để $P(n)$ là mệnh đề %s?"
                 % (bt, N, "đúng" if hoi_dung else r"\textbf{sai}"))
        dong = []
        for n, v, nt in gia_tri:
            if nt:
                dong.append(r"$n = %d$: $%d$ nguyên tố" % (n, v))
            else:
                u = next(d for d in range(2, v) if v % d == 0)
                dong.append(r"$n = %d$: $%d = %d\cdot %d$" % (n, v, u, v // u))
        giai = (r"Tính lần lượt: " + "; ".join(dong) + r".\\ Có $%d$ giá trị của $n$ làm $P(n)$ %s."
                % (dem, "đúng" if hoi_dung else "sai"))
        dung = "$%d$" % dem
        nhieu = _ba_nhieu_so(dem, N)
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def _ba_nhieu_so(dung, tran):
    ds = []
    for d in (1, -1, 2, -2, 3, -3, 4):
        v = dung + d
        if 0 <= v <= tran and ("$%d$" % v) not in ds:
            ds.append("$%d$" % v)
        if len(ds) == 3:
            break
    return ds


def L10_C1_TF_A_02(socau, socot=1):
    r"""Đúng/Sai - mệnh đề $P$: "$\forall x \in \mathbb{R},\ x^2 + 2px + q > 0$":
    phủ định, tính đúng sai, đếm số nguyên, tham số.

    CLAUDE THEM 29/09/2026 - bien the 02 cua L10_C1_TF_A, theo vi du "voi moi
    x thuc, x^2 + 4x + 5 > 0" trong giao an Bai 1. Co Lan duyet.
    """
    cauTF = ""
    for _ in range(socau):
        p = random.choice([-3, -2, -1, 1, 2, 3])
        q = p * p + random.choice([-4, -2, -1, 1, 2, 3, 5])
        bt = _tex_bac2(1, 2 * p, q)
        ghep = r"\left(x %s %d\right)^2 %s" % ("+" if p > 0 else "-", abs(p),
                                               ("+ %d" % (q - p * p)) if q - p * p > 0 else "- %d" % (p * p - q))
        dung_P = q - p * p > 0
        debai = (r"Cho mệnh đề $P$: ``$\forall x \in \mathbb{R},\ %s > 0$''. Xét tính đúng sai của các khẳng "
                 r"định sau:" % bt)
        # a) NB
        y1 = [(r"{\True Mệnh đề phủ định của $P$ là ``$\exists x \in \mathbb{R},\ %s \le 0$''}" % bt,
               r"Đúng. Phủ định của $\forall$ là $\exists$, phủ định của $>$ là $\le$."),
              (r"{Mệnh đề phủ định của $P$ là ``$\exists x \in \mathbb{R},\ %s < 0$''}" % bt,
               r"Sai. Phủ định của $>$ là $\le$, nên $\overline{P}$: ``$\exists x \in \mathbb{R},\ %s \le 0$''." % bt)]
        # b) TH
        ly_b = (r"$%s = %s$. " % (bt, ghep) + (r"Vì $\left(x %s %d\right)^2 \ge 0$ nên biểu thức luôn dương, $P$ đúng."
                                               % ("+" if p > 0 else "-", abs(p)) if dung_P else
                                               r"Với $x = %d$ biểu thức bằng $%d \le 0$, nên $P$ sai." % (-p, q - p * p)))
        noi = random.choice([True, False])
        y2 = [(r"{\True $P$ là mệnh đề %s}" % ("đúng" if dung_P else "sai"), r"Đúng. " + ly_b),
              (r"{$P$ là mệnh đề %s}" % ("sai" if dung_P else "đúng"), r"Sai. " + ly_b)]
        if noi:
            y2 = y2[::-1]
        # c) VD: số nguyên x với biểu thức <= t
        T = random.randint(2, 20)                      # (x + p)^2 <= T
        t = T + q - p * p
        so_nguyen = 2 * math.isqrt(T) + 1
        ly_c = (r"$%s \le %d \Leftrightarrow \left(x %s %d\right)^2 \le %d$. Với $x$ nguyên, $x %s %d$ là số nguyên "
                r"có bình phương không vượt quá $%d$ nên $%d \le x %s %d \le %d$, có $%d$ số nguyên $x$."
                % (bt, t, "+" if p > 0 else "-", abs(p), T, "+" if p > 0 else "-", abs(p), T, -math.isqrt(T),
                   "+" if p > 0 else "-", abs(p), math.isqrt(T), so_nguyen))
        y3 = [(r"{\True Có đúng $%d$ số nguyên $x$ thoả mãn $%s \le %d$}" % (so_nguyen, bt, t), r"Đúng. " + ly_c),
              (r"{Có đúng $%d$ số nguyên $x$ thoả mãn $%s \le %d$}" % (so_nguyen - 1, bt, t), r"Sai. " + ly_c)]
        # d) VDC: số m nguyên trong [-10; 10] để forall x, x^2 + 2px + m > 0
        K = sum(1 for m in range(-10, 11) if m > p * p)
        bt_m = r"x^2 %s %dx + m" % ("+" if p > 0 else "-", abs(2 * p)) if abs(p) != 0 else "x^2 + m"
        ly_d = (r"$%s = \left(x %s %d\right)^2 + m - %d > 0$ với mọi $x$ khi và chỉ khi $m > %d$. "
                r"Trong đoạn $[-10;\ 10]$ có $%d$ số nguyên $m$ như vậy."
                % (bt_m, "+" if p > 0 else "-", abs(p), p * p, p * p, K))
        y4 = [(r"{\True Có đúng $%d$ giá trị nguyên của $m \in [-10;\ 10]$ để mệnh đề ``$\forall x \in \mathbb{R},\ "
               r"%s > 0$'' đúng}" % (K, bt_m), r"Đúng. " + ly_d),
              (r"{Có đúng $%d$ giá trị nguyên của $m \in [-10;\ 10]$ để mệnh đề ``$\forall x \in \mathbb{R},\ "
               r"%s > 0$'' đúng}" % (K + 1, bt_m), r"Sai (tính cả $m = %d$). " % (p * p) + ly_d)]
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


# =====================================================================
# BIẾN THỂ LẤY TỪ GIÁO ÁN BÀI 2 (TẬP HỢP) CỦA CÔ LAN (30/09/2026)
# CLAUDE THEM 30/09/2026 - co Lan duyet lai. Phan tu cua tap hop do Python
# tinh (nghiem, uoc, so nguyen to...); phan tu cach nhau bang dau ";".
# =====================================================================

def _tex_gt(v):
    """Số (hữu tỉ hoặc căn) viết kiểu đề thi."""
    from sympy import latex as _latex, nsimplify as _ns
    v = _ns(v)
    if v.is_Rational:
        return _tex_so(v)
    return _latex(v).replace(r"\frac", r"\dfrac")


def _tap(ds):
    """Tập liệt kê, sắp tăng dần, cách nhau bằng dấu chấm phẩy."""
    ds = sorted(set(ds), key=float)
    if not ds:
        return r"\varnothing"
    return r"\left\{%s\right\}" % "; ".join(_tex_gt(v) for v in ds)


def _tap_dac_trung(loai):
    """Một tập cho bởi tính chất đặc trưng: (đề, đáp án (list), các list sai, lời giải)."""
    if loai == 0:
        a = random.randint(1, 10)
        b = a + random.randint(9, 16)
        dung = [n for n in range(a + 1, b) if _la_nguyen_to(n)]
        sai = [[n for n in range(a, b + 1) if _la_nguyen_to(n)],
               [n for n in range(a + 1, b) if n % 2 == 1],
               dung[1:], dung + [n for n in (a, b) if n % 2 and not _la_nguyen_to(n)][:1]]
        de = r"\left\{n \in \mathbb{N} \mid n \text{ là số nguyên tố, } %d < n < %d\right\}" % (a, b)
        giai = r"Các số nguyên tố lớn hơn $%d$ và nhỏ hơn $%d$ là $%s$." % (a, b, "; ".join(map(str, dung)))
        return de, dung, sai, giai
    if loai == 1:
        a = random.randint(-6, 0)
        b = a + random.randint(3, 6)
        tr, ph = random.choice([(True, False), (False, True), (True, True), (False, False)])
        tap_so = random.choice([r"\mathbb{Z}", r"\mathbb{Z}", r"\mathbb{N}"])
        lo = a if tr else a + 1
        hi = b if ph else b - 1
        if tap_so == r"\mathbb{N}":
            lo = max(lo, 0)
        dung = list(range(lo, hi + 1))
        if not dung:
            return _tap_dac_trung(0)
        dt, dp = (r"\le" if tr else "<"), (r"\le" if ph else "<")
        sai = [list(range(a if not tr else a + 1, (b - 1 if ph else b) + 1)),
               list(range(a, b + 1)), list(range(a + 1, b)), [v for v in dung if v >= 0] if tap_so != r"\mathbb{N}"
               else list(range(1, hi + 1))]
        sai = [[v for v in s if tap_so != r"\mathbb{N}" or v >= 0] for s in sai]
        de = r"\left\{x \in %s \mid %d %s x %s %d\right\}" % (tap_so, a, dt, dp, b)
        giai = (r"Các số %s $x$ thoả mãn $%d %s x %s %d$ là $%s$."
                % ("tự nhiên" if tap_so == r"\mathbb{N}" else "nguyên", a, dt, dp, b, "; ".join(map(str, dung))))
        return de, dung, sai, giai
    if loai == 2:
        k = random.choice([12, 18, 20, 24, 28, 30, 36, 40])
        dung = [d for d in range(1, k + 1) if k % d == 0]
        sai = [dung[1:-1], dung[1:], [d for d in dung if d != k], [k * i for i in range(1, 5)]]
        de = r"\left\{n \in \mathbb{N} \mid n \text{ là ước của } %d\right\}" % k
        giai = r"Các ước tự nhiên của $%d$ là $%s$ (kể cả $1$ và $%d$)." % (k, "; ".join(map(str, dung)), k)
        return de, dung, sai, giai
    if loai == 3:
        k = random.choice([5, 9, 10, 16, 17, 20, 25])
        dung = [x_ for x_ in range(-10, 11) if x_ * x_ < k]
        sai = [[v for v in dung if v >= 0], [x_ for x_ in range(-10, 11) if x_ * x_ <= k],
               [x_ for x_ in range(-10, 11) if abs(x_) < k and abs(x_) <= 5][:0] or list(range(0, k)),
               [v for v in dung if v > 0]]
        de = r"\left\{x \in \mathbb{Z} \mid x^2 < %d\right\}" % k
        can = math.isqrt(k - 1)
        giai = (r"$x^2 < %d$ với $x$ nguyên $\Leftrightarrow |x| \le %d$, nên $x \in \left\{%s\right\}$."
                % (k, can, "; ".join(map(str, dung))))
        return de, dung, sai, giai
    # Phương trình tích trên N, Z, Q, R (giáo án ghi mức B - thông hiểu) KHÔNG
    # đưa vào đây vì NB017 chỉ là mức nhận biết.
    raise ValueError(loai)


def L10_C1_B2_NB017_MC_G_01(socau, dang=1):
    r"""Liệt kê các phần tử của tập hợp cho bởi tính chất đặc trưng (số
    nguyên tố, số nguyên trong khoảng, ước, $x^2 < k$) - mức nhận biết.

    CLAUDE THEM 30/09/2026 - dang MOI (mapping co ghi chu), theo cac vi du
    "D = {n thuoc N | n nguyen to, 5 < n < 20}", "B = {x thuoc Z | -3 < x <=
    2}", "C = {x thuoc Z | x^2 < 9}" trong giao an Bai 2.
    Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        de, dung, sai, giai = _tap_dac_trung(random.randint(0, 3))
        dap = "$%s$" % _tap(dung)
        ung = []
        for s_ in sai:
            t_ = "$%s$" % _tap(s_)
            if t_ != dap and t_ not in ung:
                ung.append(t_)
        if len(ung) < 3:
            continue
        so += 1
        debai = r"Liệt kê các phần tử của tập hợp $A = %s$, ta được" % de
        cauTN += MC_SA_answer_text(debai, "$A = %s$" % _tap(dung), ["$A = %s$" % t_[1:-1] for t_ in ung[:3]],
                                   giai + r" Vậy $A = %s$." % _tap(dung), 0, 0, dang)
    return cauTN


def _tap_rong_hay_khong():
    """(đề tập hợp, rỗng hay không, lí do) - do Python kiểm tra."""
    loai = random.randint(1, 5)   # không dùng Delta: NB017 chỉ là mức nhận biết
    if loai == 1:
        k = random.choice([2, 3, 5, 6, 7, 4, 9, 16, 25])
        chinh = math.isqrt(k) ** 2 == k
        return (r"\left\{x \in \mathbb{Q} \mid x^2 = %d\right\}" % k, not chinh,
                (r"$x = \pm %d$ là số hữu tỉ" % math.isqrt(k)) if chinh else
                (r"$x = \pm\sqrt{%d}$ là số vô tỉ" % k))
    if loai == 2:
        a_ = random.randint(2, 6)
        b_ = random.choice([i for i in range(-15, 16) if i])
        chia = b_ % a_ == 0
        return (r"\left\{x \in \mathbb{Z} \mid %dx %s %d = 0\right\}" % (a_, "+" if b_ > 0 else "-", abs(b_)),
                not chia, r"nghiệm $x = %s$ %s số nguyên" % (_tex_so(Rational(-b_, a_)), "là" if chia else "không là"))
    if loai == 3:
        k = random.randint(1, 3)
        return (r"\left\{x \in \mathbb{Z} \mid |x| < %d\right\}" % k, False, r"$x = 0$ thoả mãn")
    if loai == 4:
        a_ = random.randint(-5, 8)
        if random.random() < 0.5:
            return (r"\left\{x \in \mathbb{Z} \mid %d < x < %d\right\}" % (a_, a_ + 1), True,
                    r"không có số nguyên nào nằm giữa hai số nguyên liên tiếp $%d$ và $%d$" % (a_, a_ + 1))
        return (r"\left\{x \in \mathbb{R} \mid %d < x < %d\right\}" % (a_, a_ + 1), False,
                r"chẳng hạn $x = %s$ thoả mãn" % _tex_so(Rational(2 * a_ + 1, 2)))
    k = random.randint(1, 9)
    if random.random() < 0.5:
        return (r"\left\{x \in \mathbb{N} \mid x < 0\right\}", True, r"không có số tự nhiên nào âm")
    return (r"\left\{x \in \mathbb{N} \mid x < %d\right\}" % k, False, r"$x = 0$ thoả mãn")


def L10_C1_B2_NB017_MC_H_01(socau, dang=1):
    r"""Nhận biết tập rỗng: trong bốn tập hợp cho bởi tính chất đặc trưng, tập
    nào rỗng (khác rỗng)?

    CLAUDE THEM 30/09/2026 - dang MOI (mapping co ghi chu), theo vi du "A =
    {x thuoc R | x^2 - x + 1 = 0}, B = {x thuoc Q | x^2 - 4x + 2 = 0}..." trong
    giao an Bai 2. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        hoi_rong = random.choice([True, False])
        chon, cung, da = None, [], set()
        for _t in range(500):
            de, rong, ly = _tap_rong_hay_khong()
            khoa = de[:30]
            if khoa in da:
                continue
            if rong == hoi_rong and chon is None:
                chon = (de, rong, ly); da.add(khoa)
            elif rong != hoi_rong and len(cung) < 3:
                cung.append((de, rong, ly)); da.add(khoa)
            if chon and len(cung) == 3:
                break
        debai = r"Tập hợp nào sau đây %s?" % ("là tập rỗng" if hoi_rong else r"\textbf{khác} tập rỗng")
        giai = (r"$%s$ %s vì %s.\\ " % (chon[0], r"$= \varnothing$" if hoi_rong else r"$\ne \varnothing$", chon[2])
                + r"\\ ".join(r"$%s$ %s vì %s." % (d_, r"$= \varnothing$" if r_ else r"$\ne \varnothing$", l_)
                              for d_, r_, l_ in cung))
        cauTN += MC_SA_answer_text(debai, "$%s$" % chon[0], ["$%s$" % c_[0] for c_ in cung], giai, 0, 0, dang)
    return cauTN


def L10_C1_B2_TH018_MC_B_02(socau, dang=1):
    r"""Tập hợp $M$ có nhiều phần tử nhất thoả mãn $M \subset A$ và $M \subset B$
    (tức là $A \cap B$), hai tập cho dạng liệt kê.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH018_MC_B, theo bai "A = {1; 2;
    3; 4; 5}, B = {1; 3; 5; 7; 9}, tim M nhieu phan tu nhat" trong giao an
    Bai 2. Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        A = sorted(random.sample(range(0, 13), random.randint(4, 6)))
        B = sorted(random.sample(range(0, 13), random.randint(4, 6)))
        giao = sorted(set(A) & set(B))
        if len(giao) < 2 or set(A) <= set(B) or set(B) <= set(A):
            continue
        dap = "$M = %s$" % _tap(giao)
        ung = []
        for s_ in (sorted(set(A) | set(B)), sorted(set(A) - set(B)), sorted(set(B) - set(A)), giao[1:], giao[:-1]):
            t_ = "$M = %s$" % _tap(s_)
            if t_ != dap and t_ not in ung:
                ung.append(t_)
        if len(ung) < 3:
            continue
        so += 1
        debai = (r"Cho hai tập hợp $A = %s$ và $B = %s$. Tập hợp $M$ có nhiều phần tử nhất thoả mãn "
                 r"$M \subset A$ và $M \subset B$ là" % (_tap(A), _tap(B)))
        giai = (r"$M \subset A$ và $M \subset B$ nghĩa là mọi phần tử của $M$ đều thuộc cả $A$ và $B$, tức là "
                r"$M \subset A \cap B = %s$. Tập $M$ nhiều phần tử nhất là $M = A \cap B = %s$."
                % (_tap(giao), _tap(giao)))
        cauTN += MC_SA_answer_text(debai, dap, ung[:3], giai, 0, 0, dang)
    return cauTN


def L10_C1_B2_VD021_SA_A_02(socau, dang=2):
    r"""Đếm số nguyên $m$ để $A \cap B = A$ với $A$ là đoạn / khoảng độ dài cố
    định chứa tham số, $B$ là đoạn / khoảng / nửa khoảng cho trước.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD021_SA_A, theo cac bai "A = [m;
    m + 2] con cua B = [-1; 2]", "B = [a; a + 2] con cua A = [0; 3]" trong
    giao an Bai 2. Hoi dang "A giao B = A" (dung Dang cua ID). Co Lan duyet.
    """
    def khoang(trai, a_, b_, phai):
        return r"%s%s;\ %s%s" % ("[" if trai else "(", a_, b_, "]" if phai else ")")

    cau = ""
    so = 0
    while so < socau:
        a = random.randint(-10, 3)
        b = a + random.randint(8, 20)
        k = random.randint(1, 5)
        tA, pA = random.choice([True, False]), random.choice([True, False])
        tB, pB = random.choice([True, False]), random.choice([True, False])

        def con(m):
            l_ok = m > a or (m == a and (tB or not tA))
            r_ok = m + k < b or (m + k == b and (pB or not pA))
            return l_ok and r_ok
        dem = sum(1 for m in range(a - 30, b + 30) if con(m))
        if dem < 1 or dem > 99:
            continue
        so += 1
        dau_l = ">" if (tA and not tB) else r"\ge"
        dau_r = "<" if (pA and not pB) else r"\le"
        A_tex = khoang(tA, "m", "m + %d" % k, pA)
        B_tex = khoang(tB, a, b, pB)
        debai = (r"Cho hai tập hợp $A = %s$ và $B = %s$ với $m$ là tham số. Có bao nhiêu số nguyên $m$ để "
                 r"$A \cap B = A$?" % (A_tex, B_tex))
        lo = a if dau_l == r"\ge" else a + 1
        hi = b - k if dau_r == r"\le" else b - k - 1
        giai = (r"$A \cap B = A \Leftrightarrow A \subset B \Leftrightarrow \begin{cases} m %s %d \\ m + %d %s %d "
                r"\end{cases} \Leftrightarrow %d \le m \le %d$ (với $m$ nguyên).\\ Có $%d - (%d) + 1 = %d$ số nguyên $m$."
                % (dau_l, a, k, dau_r, b, lo, hi, hi, lo, dem))
        cau += MC_SA_answer_text(debai, str(dem), [str(dem + 1), str(dem - 1), str(dem + 2)], giai, 0, 0, dang)
    return cau


def L10_C1_TF_B_02(socau, socot=1):
    r"""Đúng/Sai - tập $A = \{x \in \mathbb{Z} \mid \frac{x + k}{x - c} \in \mathbb{Z}\}$:
    phần tử, liệt kê, số tập con, tham số để $B \subset A$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua L10_C1_TF_B, theo cac bai "A = {x
    thuoc Z | (2x + 3)/(x - 1) thuoc Z}, B = {x | x^2 - (m + 2)x + 2m = 0},
    tim m nguyen de B con A" trong giao an Bai 2. Co Lan duyet.
    """
    cauTF = ""
    for _ in range(socau):
        c = random.choice([i for i in range(-3, 4) if i])
        d = random.choice([4, 5, 6, 7, 8, 9, 10, 12])          # d = k + c
        k = d - c
        uoc = [u for u in range(1, d + 1) if d % u == 0]
        A = sorted([c + u for u in uoc] + [c - u for u in uoc])
        N = len(A)
        r = random.choice(A)
        tu = r"x %s %d" % ("+" if k > 0 else "-", abs(k)) if k else "x"
        mau = r"x %s %d" % ("-" if c > 0 else "+", abs(c))
        debai = (r"Cho tập hợp $A = \left\{x \in \mathbb{Z} \mathrel{\Big|} \dfrac{%s}{%s} \in \mathbb{Z}\right\}$ và "
                 r"$B = \left\{x \in \mathbb{R} \mid %s = 0\right\}$ với $m$ là tham số. Xét tính đúng sai "
                 r"của các khẳng định sau:"
                 % (tu, mau, (r"(x - m)(x %s %d)" % ("-" if r > 0 else "+", abs(r))) if r else r"x(x - m)"))
        tach = r"\dfrac{%s}{%s} = 1 + \dfrac{%d}{%s}" % (tu, mau, d, mau)
        # a) NB
        y1 = [(r"{\True $%d \in A$}" % (c + 1),
               r"Đúng. Với $x = %d$: $\dfrac{%d}{1} = %d \in \mathbb{Z}$." % (c + 1, c + 1 + k, c + 1 + k)),
              (r"{$%d \in A$}" % c, r"Sai. Với $x = %d$ mẫu bằng $0$, biểu thức không xác định." % c)]
        # b) TH
        ly_b = (r"$%s$, nên $x %s %d$ là ước của $%d$: $x %s %d \in \left\{%s\right\}$, do đó $A = %s$."
                % (tach, "-" if c > 0 else "+", abs(c), d, "-" if c > 0 else "+", abs(c),
                   "; ".join(str(v) for v in sorted([-u for u in uoc] + uoc)), _tap(A)))
        y2 = [(r"{\True $A = %s$}" % _tap(A), r"Đúng. " + ly_b),
              (r"{$A = %s$}" % _tap([c + u for u in uoc]), r"Sai (thiếu các ước âm). " + ly_b)]
        # c) VD
        y3 = [(r"{\True Tập hợp $A$ có đúng $%d$ tập con}" % (2 ** N),
               r"Đúng. $A$ có $%d$ phần tử nên có $2^{%d} = %d$ tập con." % (N, N, 2 ** N)),
              (r"{Tập hợp $A$ có đúng $%d$ tập con}" % (2 ** N - 1),
               r"Sai. $A$ có $%d$ phần tử nên có $2^{%d} = %d$ tập con (kể cả $\varnothing$ và $A$)." % (N, N, 2 ** N))]
        # d) VDC
        ly_d = (r"$B = \left\{%d; m\right\}$ (hoặc $B = \left\{%d\right\}$ khi $m = %d$). Vì $%d \in A$ nên "
                r"$B \subset A \Leftrightarrow m \in A$: có $%d$ số nguyên $m$." % (r, r, r, r, N))
        y4 = [(r"{\True Có đúng $%d$ số nguyên $m$ để $B \subset A$}" % N, r"Đúng. " + ly_d),
              (r"{Có đúng $%d$ số nguyên $m$ để $B \subset A$}" % (N - 1),
               r"Sai (bỏ sót trường hợp $m = %d$). " % r + ly_d)]
        cauTF += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cauTF


# =====================================================================
# BIẾN THỂ LẤY TỪ GIÁO ÁN BÀI 3 (CÁC PHÉP TOÁN TRÊN TẬP HỢP) CỦA CÔ LAN
# CLAUDE THEM 30/09/2026 - co Lan duyet lai. Moi ket qua phep toan tren
# khoang / doan do mot bo may nho tinh (_k_*): xet tung diem mut va tung
# khoang giua hai diem mut, khong suy tay.
# =====================================================================
from fractions import Fraction as _Fr

_VC = float("inf")


def _k_thuoc(S, x):
    """x có thuộc hợp các khoảng S không; mỗi khoảng (lo, lo_dong, hi, hi_dong)."""
    for lo, lc, hi, hc in S:
        if lo < x < hi or (x == lo and lc) or (x == hi and hc):
            return True
    return False


def _k_dung(thuoc, diem):
    """Dựng lại tập (hợp các khoảng rời nhau) từ hàm thuộc và các điểm mút."""
    pts = sorted(set(p for p in diem if p not in (_VC, -_VC)))
    manh = []
    bien = [-_VC] + pts + [_VC]
    for i in range(len(bien) - 1):
        a, b = bien[i], bien[i + 1]
        if i > 0:
            manh.append(("d", a, thuoc(a)))
        if a == -_VC and b == _VC:
            giua = 0
        elif a == -_VC:
            giua = b - 1
        elif b == _VC:
            giua = a + 1
        else:
            giua = _Fr(a) / 2 + _Fr(b) / 2
        manh.append(("k", a, b, thuoc(giua)))
    kq, cur = [], None
    for m in manh:
        if m[0] == "d":
            _, p, vao = m
            if vao and cur is None:
                cur = [p, True]
            elif not vao and cur is not None:
                kq.append((cur[0], cur[1], p, False)); cur = None
        else:
            _, a, b, vao = m
            if vao and cur is None:
                cur = [a, False]
            elif not vao and cur is not None:
                kq.append((cur[0], cur[1], a, True)); cur = None
    if cur is not None:
        kq.append((cur[0], cur[1], _VC, False))
    return kq


def _k_phep(A, B, phep):
    diem = [p for S in (A, B) for k in S for p in (k[0], k[2])]
    f = {"giao": lambda x: _k_thuoc(A, x) and _k_thuoc(B, x),
         "hop": lambda x: _k_thuoc(A, x) or _k_thuoc(B, x),
         "hieu": lambda x: _k_thuoc(A, x) and not _k_thuoc(B, x),
         "bu": lambda x: not _k_thuoc(A, x)}[phep]
    return _k_dung(f, diem)


def _k_so(v):
    v = _Fr(v)
    if v.denominator == 1:
        return "%d" % v.numerator
    return (r"-\dfrac{%d}{%d}" if v < 0 else r"\dfrac{%d}{%d}") % (abs(v.numerator), v.denominator)


def _k_tex(S):
    if not S:
        return r"\varnothing"
    if len(S) == 1 and S[0][0] == -_VC and S[0][2] == _VC:
        return r"\mathbb{R}"
    phan = []
    for lo, lc, hi, hc in S:
        if lo == hi:
            phan.append(r"\left\{%s\right\}" % _k_so(lo))
            continue
        trai = r"\left(-\infty" if lo == -_VC else (r"\left[" if lc else r"\left(") + _k_so(lo)
        phai = r"+\infty\right)" if hi == _VC else _k_so(hi) + (r"\right]" if hc else r"\right)")
        phan.append(trai + ";\\ " + phai)
    return r" \cup ".join(phan)


def _k_lat(S, i, dau):
    """Đổi đóng/mở ở đầu mút (khoảng thứ i, đầu trái/phải) - làm phương án nhiễu."""
    S = [list(k) for k in S]
    if dau == 0 and S[i][0] != -_VC:
        S[i][1] = not S[i][1]
    elif dau == 1 and S[i][2] != _VC:
        S[i][3] = not S[i][3]
    return [tuple(k) for k in S]


def L10_C1_B2_TH018_MC_B_03(socau, dang=1):
    r"""Phần bù trong tập $E$ (liệt kê): $C_EA$, $C_E(A \cup B)$, $C_EA \cap C_EB$...

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH018_MC_B, theo vi du "E = {1;
    ...; 9}, A = {1; 2; 3; 4}, B = {2; 4; 6; 8}, xac dinh C_E A, C_E(A hop B),
    C_E A giao C_E B" trong giao an Bai 3. Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        n = random.randint(8, 12)
        E = set(range(1, n + 1))
        A = set(random.sample(sorted(E), random.randint(3, 5)))
        B = set(random.sample(sorted(E), random.randint(3, 5)))
        if not (A & B) or A <= B or B <= A or len(A | B) >= n:
            continue
        PHEP = [(r"C_EA", E - A, r"E \setminus A"), (r"C_EB", E - B, r"E \setminus B"),
                (r"C_E(A \cup B)", E - (A | B), r"E \setminus (A \cup B)"),
                (r"C_E(A \cap B)", E - (A & B), r"E \setminus (A \cap B)"),
                (r"C_EA \cap C_EB", (E - A) & (E - B), r"(E \setminus A) \cap (E \setminus B)"),
                (r"C_EA \cup C_EB", (E - A) | (E - B), r"(E \setminus A) \cup (E \setminus B)")]
        i = random.randrange(len(PHEP))
        ten, kq, cach = PHEP[i]
        dap = "$%s = %s$" % (ten, _tap(kq))
        ung = []
        for j, (_, k2, _) in enumerate(PHEP):
            t_ = "$%s = %s$" % (ten, _tap(k2))
            if j != i and t_ != dap and t_ not in ung:
                ung.append(t_)
        for k2 in (A, B, A | B, A & B):
            t_ = "$%s = %s$" % (ten, _tap(k2))
            if t_ != dap and t_ not in ung:
                ung.append(t_)
        random.shuffle(ung)
        so += 1
        debai = (r"Cho tập hợp $E = %s$ và các tập con $A = %s$, $B = %s$ của $E$. Tập hợp $%s$ là"
                 % (_tap(E), _tap(A), _tap(B), ten))
        giai = (r"$C_EA = %s$, $C_EB = %s$, $A \cup B = %s$, $A \cap B = %s$.\\ $%s = %s = %s$."
                % (_tap(E - A), _tap(E - B), _tap(A | B), _tap(A & B), ten, cach, _tap(kq)))
        cauTN += MC_SA_answer_text(debai, dap, ung[:3], giai, 0, 0, dang)
    return cauTN


def L10_C1_B2_TH018_MC_B_04(socau, dang=1):
    r"""Xác định lại tập $A$ (hoặc $B$, $A \cup B$) khi biết $A \setminus B$,
    $B \setminus A$ và $A \cap B$.

    CLAUDE THEM 30/09/2026 - bien the 04 cua TH018_MC_B, theo vi du "A \\ B =
    {1; 5; 7; 8}, B \\ A = {2; 10}, A giao B = {3; 6; 9}" trong giao an Bai 3.
    Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        so_ = random.sample(range(0, 16), random.randint(7, 10))
        k1, k2 = random.randint(2, 4), random.randint(2, 3)
        AB, BA, G = set(so_[:k1]), set(so_[k1:k1 + k2]), set(so_[k1 + k2:])
        if len(G) < 2:
            continue
        hoi = random.choice(["A", "B", r"A \cup B"])
        kq = {"A": AB | G, "B": BA | G, r"A \cup B": AB | BA | G}[hoi]
        dap = "$%s = %s$" % (hoi, _tap(kq))
        ung = []
        for k_ in (AB | G, BA | G, AB | BA | G, AB | BA, AB, G):
            t_ = "$%s = %s$" % (hoi, _tap(k_))
            if t_ != dap and t_ not in ung:
                ung.append(t_)
        so += 1
        debai = (r"Cho hai tập hợp $A$, $B$ thoả mãn $A \setminus B = %s$, $B \setminus A = %s$ và "
                 r"$A \cap B = %s$. Tập hợp $%s$ là" % (_tap(AB), _tap(BA), _tap(G), hoi))
        cach = {"A": r"(A \setminus B) \cup (A \cap B)", "B": r"(B \setminus A) \cup (A \cap B)",
                r"A \cup B": r"(A \setminus B) \cup (B \setminus A) \cup (A \cap B)"}[hoi]
        giai = (r"Mỗi phần tử của $A \cup B$ thuộc đúng một trong ba phần rời nhau: chỉ thuộc $A$, chỉ thuộc "
                r"$B$, thuộc cả hai. Do đó $%s = %s = %s$." % (hoi, cach, _tap(kq)))
        cauTN += MC_SA_answer_text(debai, dap, ung[:3], giai, 0, 0, dang)
    return cauTN


def _k_tap_de(S_lo, lc, S_hi, hc, cho_tinh_chat):
    """Viết một khoảng: dạng kí hiệu khoảng hoặc dạng {x thuộc R | ...}."""
    S = [(S_lo, lc, S_hi, hc)]
    if not cho_tinh_chat:
        return _k_tex(S), None
    if S_lo == -_VC:
        return r"\left\{x \in \mathbb{R} \mid x %s %s\right\}" % (r"\le" if hc else "<", _k_so(S_hi)), _k_tex(S)
    if S_hi == _VC:
        return r"\left\{x \in \mathbb{R} \mid x %s %s\right\}" % (r"\ge" if lc else ">", _k_so(S_lo)), _k_tex(S)
    if lc == hc and random.random() < 0.4 and (S_lo + S_hi) % 2 == 0:
        c, r = (S_lo + S_hi) // 2, (S_hi - S_lo) // 2
        tt = r"|x|" if c == 0 else r"|x %s %d|" % ("-" if c > 0 else "+", abs(c))
        return r"\left\{x \in \mathbb{R} \mid %s %s %d\right\}" % (tt, r"\le" if lc else "<", r), _k_tex(S)
    return (r"\left\{x \in \mathbb{R} \mid %s %s x %s %s\right\}"
            % (_k_so(S_lo), r"\le" if lc else "<", r"\le" if hc else "<", _k_so(S_hi)), _k_tex(S))


def L10_C1_B2_TH021_MC_A_02(socau, dang=1):
    r"""Giao, hợp, hiệu, phần bù của hai khoảng / đoạn / nửa khoảng (có thể cho
    dưới dạng $\{x \in \mathbb{R} \mid \dots\}$, kể cả $|x - c| \le k$).

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH021_MC_A, theo cac vi du "A =
    {x | -1 <= x <= 3}, B = {x | -2 < x < 2}", "A = {x | x^2 <= 4}, B = {x | x
    < 1}", "[-5; 1] va (-3; 2)" trong giao an Bai 3. Co Lan duyet.
    """
    cauTN = ""
    so = 0
    while so < socau:
        p = sorted(random.sample(range(-9, 10), 4))
        kieu = random.randint(0, 2)
        if kieu == 0:          # hai khoảng bị chặn chồng nhau
            A = (p[0], random.random() < .5, p[2], random.random() < .5)
            B = (p[1], random.random() < .5, p[3], random.random() < .5)
        elif kieu == 1:        # một khoảng bị chặn, một tia
            A = (p[0], random.random() < .5, p[2], random.random() < .5)
            B = random.choice([(-_VC, False, p[1], random.random() < .5), (p[1], random.random() < .5, _VC, False)])
        else:                  # hai tia ngược chiều chồng nhau
            A = (-_VC, False, p[2], random.random() < .5)
            B = (p[1], random.random() < .5, _VC, False)
        if random.random() < 0.5:
            A, B = B, A
        tcA, tcB = random.random() < 0.5, random.random() < 0.5
        deA, lai_A = _k_tap_de(*A, tcA)
        deB, lai_B = _k_tap_de(*B, tcB)
        phep = random.choice(["giao", "hop", "hieu", "hieu_nguoc", "bu"])
        SA, SB = [A], [B]
        if phep == "hieu_nguoc":
            kq, ten = _k_phep(SB, SA, "hieu"), r"B \setminus A"
        elif phep == "bu":
            kq, ten = _k_phep(SB, SA, "bu"), r"C_{\mathbb{R}}B"
        else:
            kq = _k_phep(SA, SB, phep)
            ten = {"giao": r"A \cap B", "hop": r"A \cup B", "hieu": r"A \setminus B"}[phep]
        if not kq:
            continue
        dap = "$%s$" % _k_tex(kq)
        ung = []
        for i in range(len(kq)):
            for d_ in (0, 1):
                t_ = "$%s$" % _k_tex(_k_lat(kq, i, d_))
                if t_ != dap and t_ not in ung:
                    ung.append(t_)
        random.shuffle(ung)
        khac = [_k_phep(SA, SB, "giao"), _k_phep(SA, SB, "hop"), _k_phep(SA, SB, "hieu"), _k_phep(SB, SA, "hieu")]
        for S_ in khac:
            t_ = "$%s$" % _k_tex(S_)
            if t_ != dap and t_ not in ung:
                ung.insert(1, t_)
        ung = [u for u in dict.fromkeys(ung)][:3]
        if len(ung) < 3:
            continue
        so += 1
        debai = r"Cho hai tập hợp $A = %s$ và $B = %s$. Tập hợp $%s$ là" % (deA, deB, ten)
        viet_lai = []
        if lai_A:
            viet_lai.append(r"$A = %s$" % lai_A)
        if lai_B:
            viet_lai.append(r"$B = %s$" % lai_B)
        giai = ((r"Viết lại: " + ", ".join(viet_lai) + r".\\ " if viet_lai else "")
                + r"Biểu diễn $A$, $B$ trên trục số, ta được $%s = %s$." % (ten, _k_tex(kq)))
        cauTN += MC_SA_answer_text(debai, dap, ung, giai, 0, 0, dang)
    return cauTN


def _vd021_tham_so():
    """Một câu tham số: (đề, đáp án tex, 3 nhiễu tex, lời giải, hàm kiểm tra theo bộ máy, hàm theo đáp án)."""
    kieu = random.randint(0, 3)
    if kieu == 3:
        # A = (m + p; a], B = (b; k m + q), hai tập khác rỗng, A giao B khác rỗng
        k = random.choice([1, 2])
        a = random.randint(2, 8)
        b = random.randint(-6, a - 1)
        p = random.randint(-4, 3)
        q = random.randint(p + 1, p + 6) if k == 1 else random.randint(-4, 6)
        A = lambda m: [(m + p, False, a, True)] if m + p < a else []
        B = lambda m: [(b, False, k * m + q, False)] if k * m + q > b else []
        kiem = lambda m: bool(A(m)) and bool(B(m)) and _k_phep(A(m), B(m), "giao") != []
        duoi = [_Fr(b - q, k)] + ([_Fr(p - q)] if k == 2 else [])
        L, U = max(duoi), _Fr(a - p)
        if L >= U:
            return _vd021_tham_so()
        theo = lambda m: L < m < U
        mp = r"m %s %d" % ("+" if p > 0 else "-", abs(p)) if p else "m"
        km = ("m" if k == 1 else "2m") + ((r" %s %d" % ("+" if q > 0 else "-", abs(q))) if q else "")
        de = (r"Cho hai tập hợp khác rỗng $A = \left(%s;\ %d\right]$ và $B = \left(%d;\ %s\right)$ với $m$ là "
              r"tham số thực. Tìm tất cả các giá trị của $m$ để $A \cap B \ne \varnothing$." % (mp, a, b, km))
        dk = [r"%s < %d" % (mp, a), r"%s > %d" % (km, b)] + ([r"%s < %s" % (mp, km)] if k == 2 else [])
        giai = (r"Hai tập khác rỗng và giao khác rỗng khi $\begin{cases} %s \end{cases}$ (vì $%d < %d$ nên chỉ "
                r"còn các điều kiện này) $\Leftrightarrow %s < m < %s$." % (r" \\ ".join(dk), b, a, _k_so(L), _k_so(U)))
        dap = r"$%s < m < %s$" % (_k_so(L), _k_so(U))
        nhieu = [r"$m < %s$" % _k_so(U), r"$m > %s$" % _k_so(L), r"$%s \le m \le %s$" % (_k_so(L), _k_so(U))]
        return de, dap, nhieu, giai, kiem, theo
    if kieu == 0:
        p, q = random.randint(-5, 5), random.randint(-5, 5)
        dA, dB = random.random() < .5, random.random() < .5
        t = q - p
        dau = r"\ge" if (dA or dB) else ">"
        A = lambda m: [(-_VC, False, m + p, dA)]
        B = [(q, dB, _VC, False)]
        kiem = lambda m: _k_phep(A(m), B, "hop") == [(-_VC, False, _VC, False)]
        theo = (lambda m: m >= t) if dau == r"\ge" else (lambda m: m > t)
        mp = r"m %s %d" % ("+" if p >= 0 else "-", abs(p)) if p else "m"
        de = (r"Cho hai tập hợp $A = \left(-\infty;\ %s\right%s$ và $B = \left%s%d;\ +\infty\right)$. Tìm tất cả "
              r"các giá trị của tham số $m$ để $A \cup B = \mathbb{R}$."
              % (mp, "]" if dA else ")", "[" if dB else "(", q))
        giai = (r"$A \cup B = \mathbb{R} \Leftrightarrow %s %s %d$ (%s) $\Leftrightarrow m %s %d$."
                % (mp, dau, q, "chỉ cần một trong hai đầu mút được lấy" if dau == r"\ge" else
                   r"hai đầu mút đều không được lấy nên phải có phần chồng lên nhau", dau, t))
        dap = r"$m %s %d$" % (dau, t)
        doi = {r"\ge": ">", ">": r"\ge"}[dau]
        nhieu = [r"$m %s %d$" % (doi, t), r"$m \le %d$" % t, r"$m < %d$" % t]
        return de, dap, nhieu, giai, kiem, theo
    if kieu == 1:
        k = random.choice([2, 3])
        a = random.choice([i for i in range(-7, 8) if i])
        b = a + random.randint(2, 5)
        dong = random.random() < .5                 # A = (-inf; m] hay (-inf; m)
        t = _Fr(-a, k - 1)
        dau = ">" if dong else r"\ge"
        A = lambda m: [(-_VC, False, m, dong)]
        B = lambda m: [(k * m + a, True, k * m + b, True)]
        kiem = lambda m: _k_phep(A(m), B(m), "giao") == []
        theo = (lambda m: m > t) if dong else (lambda m: m >= t)
        ka = lambda c: r"%dm %s %d" % (k, "+" if c > 0 else "-", abs(c))
        de = (r"Cho hai tập hợp $A = \left(-\infty;\ m\right%s$ và $B = \left[%s;\ %s\right]$. Tìm tất cả các giá "
              r"trị của tham số $m$ để $A \cap B = \varnothing$." % ("]" if dong else ")", ka(a), ka(b)))
        giai = (r"$A \cap B = \varnothing \Leftrightarrow m %s %s \Leftrightarrow %dm %s %d \Leftrightarrow m %s %s$."
                % ("<" if dong else r"\le", ka(a), k - 1, ">" if dong else r"\ge", -a, dau, _k_so(t)))
        dap = r"$m %s %s$" % (dau, _k_so(t))
        doi = {r"\ge": ">", ">": r"\ge"}[dau]
        nhieu = [r"$m %s %s$" % (doi, _k_so(t)), r"$m \le %s$" % _k_so(t), r"$m < %s$" % _k_so(t)]
        return de, dap, nhieu, giai, kiem, theo
    d = random.randint(1, 4)
    a = random.randint(-6, 2)
    b = a + random.randint(3, 7)
    lcA, hcA = random.random() < .5, random.random() < .5
    lcB, hcB = random.random() < .5, random.random() < .5
    A = lambda m: [(m, lcA, m + d, hcA)]
    B = [(a, lcB, b, hcB)]
    kiem = lambda m: _k_phep(A(m), B, "giao") != []
    d1 = r"\ge" if (hcA and lcB) else ">"          # m + d ... a
    d2 = r"\le" if (lcA and hcB) else "<"          # m ... b
    theo = lambda m: ((m + d >= a) if d1 == r"\ge" else (m + d > a)) and ((m <= b) if d2 == r"\le" else (m < b))
    de = (r"Cho hai tập hợp $A = \left%sm;\ m + %d\right%s$ và $B = \left%s%d;\ %d\right%s$. Tìm tất cả các giá trị "
          r"của tham số $m$ để $A \cap B \ne \varnothing$."
          % ("[" if lcA else "(", d, "]" if hcA else ")", "[" if lcB else "(", a, b, "]" if hcB else ")"))
    lt = {r"\ge": r"\le", ">": "<"}[d1]
    giai = (r"$A \cap B \ne \varnothing \Leftrightarrow \begin{cases} m + %d %s %d \\ m %s %d \end{cases} "
            r"\Leftrightarrow %d %s m %s %d$." % (d, d1, a, d2, b, a - d, lt, d2, b))
    dap = r"$%d %s m %s %d$" % (a - d, lt, d2, b)
    lt2 = {r"\le": "<", "<": r"\le"}[lt]
    d22 = {r"\le": "<", "<": r"\le"}[d2]
    nhieu = [r"$%d %s m %s %d$" % (a - d, lt2, d2, b), r"$%d %s m %s %d$" % (a - d, lt, d22, b),
             r"$%d %s m %s %d$" % (a, lt, d2, b - d)]
    return de, dap, nhieu, giai, kiem, theo


def L10_C1_B2_VD021_MC_A_02(socau, dang=1):
    r"""Tham số: tìm điều kiện của $m$ (đáp án là một bất phương trình / khoảng
    của $m$) để $A \cup B = \mathbb{R}$, $A \cap B = \varnothing$ hoặc
    $A \cap B \ne \varnothing$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD021_MC_A, theo cac vi du "A =
    (-inf; m + 1], B = (-1; +inf), A hop B = R", "A = (-inf; m), B = [3m - 1;
    3m + 3], A giao B rong", "A = [a; a + 2], B = [b; b + 1], giao khac rong"
    trong giao an Bai 3. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        de, dap, nhieu, giai, _k, _t = _vd021_tham_so()
        cauTN += MC_SA_answer_text(de, dap, nhieu, giai, 0, 0, dang)
    return cauTN


_BOI_CANH_BA_MON = [("Có", "học sinh giỏi", "em", ("Văn", "Toán", "Anh"), "giỏi"),
                    ("Một câu lạc bộ thể thao có", "thành viên", "bạn", ("bóng đá", "cầu lông", "bơi"), "chơi"),
                    ("Một lớp có", "học sinh tham gia câu lạc bộ", "bạn", ("Âm nhạc", "Hội hoạ", "Tin học"),
                     "tham gia câu lạc bộ")]


def L10_C1_B2_VD020_SA_A_02(socau, dang=2):
    r"""Ba tập hợp: biết tổng số, số phần tử mỗi tập và số phần tử thuộc ĐÚNG hai
    tập; tìm số phần tử thuộc cả ba tập.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD020_SA_A, theo bai "44 hoc sinh
    gioi, 22 Van, 25 Toan, 20 Anh, 8 dung Van-Toan, 7 dung Toan-Anh, 6 dung
    Anh-Van" trong giao an Bai 3. Co Lan duyet.
    """
    cau = ""
    for _ in range(socau):
        x = random.randint(1, 5)
        ab, bc, ca = (random.randint(2, 9) for _ in range(3))
        a1, b1, c1 = (random.randint(3, 12) for _ in range(3))
        nA, nB, nC = a1 + ab + ca + x, b1 + ab + bc + x, c1 + bc + ca + x
        N = a1 + b1 + c1 + ab + bc + ca + x
        mo, dt, dv, (M1, M2, M3), dong = random.choice(_BOI_CANH_BA_MON)
        debai = (r"%s $%d$ %s, mỗi %s %s ít nhất một môn trong ba môn %s, %s, %s. Có $%d$ %s %s %s, $%d$ %s %s "
                 r"%s, $%d$ %s %s %s. Có $%d$ %s %s đúng hai môn %s và %s; $%d$ %s %s đúng hai môn %s và %s; "
                 r"$%d$ %s %s đúng hai môn %s và %s. Hỏi có bao nhiêu %s %s cả ba môn?"
                 % (mo, N, dt, dv, dong, M1, M2, M3, nA, dv, dong, M1, nB, dv, dong, M2, nC, dv, dong, M3,
                    ab, dv, dong, M1, M2, bc, dv, dong, M2, M3, ca, dv, dong, M3, M1, dv, dong))
        giai = (r"Gọi $x$ là số %s %s cả ba môn. Số %s chỉ %s một môn: %s: $%d - %d - %d - x = %d - x$; "
                r"%s: $%d - %d - %d - x = %d - x$; %s: $%d - %d - %d - x = %d - x$.\\ "
                r"Cộng tất cả các phần của biểu đồ Ven: $(%d - x) + (%d - x) + (%d - x) + %d + %d + %d + x = %d$\\ "
                r"$\Leftrightarrow %d - 2x = %d \Leftrightarrow x = %d$."
                % (dv, dong, dv, dong, M1, nA, ab, ca, nA - ab - ca, M2, nB, ab, bc, nB - ab - bc,
                   M3, nC, bc, ca, nC - bc - ca, nA - ab - ca, nB - ab - bc, nC - bc - ca, ab, bc, ca, N,
                   nA + nB + nC - ab - bc - ca, N, x))
        cau += MC_SA_answer_text(debai, str(x), [str(x + 1), str(x + 2), str(x + 3)], giai, 0, 0, dang)
    return cau


_BOI_CANH_HAI_MON = [("Lớp 10A", "học sinh", "giỏi Văn", "giỏi Toán", "không đạt học sinh giỏi môn nào"),
                     ("Một lớp học", "học sinh", "biết chơi bóng chuyền", "biết chơi bóng đá",
                      "không biết chơi môn nào trong hai môn đó"),
                     ("Một nhóm khách du lịch", "người", "đã đến Huế", "đã đến Hội An",
                      "chưa đến nơi nào trong hai nơi đó")]


def L10_C1_B2_VD020_MC_A_02(socau, dang=1):
    r"""Hai tập hợp thực tế có thêm nhóm "không thuộc tập nào": tìm số phần tử
    thuộc cả hai tập, hoặc tìm tổng số.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD020_MC_A, theo cac bai "45 hoc
    sinh, 17 gioi Van, 25 gioi Toan, 13 khong dat" va "15 thich Van, 20 thich
    Toan, 8 thich ca hai, 10 khong thich mon nao" trong giao an Bai 3.
    Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        ab = random.randint(3, 12)
        a, b = ab + random.randint(4, 15), ab + random.randint(4, 15)
        khong = random.randint(2, 12)
        N = a + b - ab + khong
        noi, dv, t1, t2, t0 = random.choice(_BOI_CANH_HAI_MON)
        if random.random() < 0.5:
            debai = (r"%s có $%d$ %s, trong đó có $%d$ %s %s, $%d$ %s %s và $%d$ %s %s. Số %s vừa %s vừa %s là"
                     % (noi, N, dv, a, dv, t1, b, dv, t2, khong, dv, t0, dv, t1, t2))
            dung = ab
            ung = [a + b - N, a + b - (N - khong) + khong, N - khong]
            giai = (r"Gọi $A$, $B$ là tập các %s %s, %s. Số %s thuộc ít nhất một tập là $|A \cup B| = %d - %d = %d$.\\ "
                    r"$|A \cap B| = |A| + |B| - |A \cup B| = %d + %d - %d = %d$."
                    % (dv, t1, t2, dv, N, khong, N - khong, a, b, N - khong, ab))
        else:
            debai = (r"%s có $%d$ %s %s, $%d$ %s %s, trong đó $%d$ %s vừa %s vừa %s; ngoài ra còn $%d$ %s %s. "
                     r"Hỏi %s có tất cả bao nhiêu %s?"
                     % (noi, a, dv, t1, b, dv, t2, ab, dv, t1, t2, khong, dv, t0, noi[0].lower() + noi[1:], dv))
            dung = N
            ung = [a + b + khong, a + b - ab, a + b - khong]
            giai = (r"Số %s thuộc ít nhất một trong hai nhóm là $%d + %d - %d = %d$. Cộng thêm $%d$ %s %s: "
                    r"$%d + %d = %d$." % (dv, a, b, ab, a + b - ab, khong, dv, t0, a + b - ab, khong, N))
        nhieu = _ba_nhieu("$%d$" % dung, ["$%d$" % v for v in ung if v > 0],
                          buoc=lambda k: "$%d$" % (dung + k))
        cauTN += MC_SA_answer_text(debai, "$%d$" % dung, nhieu, giai, 0, 0, dang)
    return cauTN


# =====================================================================
# BIẾN THỂ LẤY TỪ ĐỀ TRẮC NGHIỆM ÔN TẬP CUỐI CHƯƠNG 1 CỦA CÔ LAN (30/09/2026)
# CLAUDE THEM 30/09/2026 - co Lan duyet lai.
# =====================================================================

def _k_bdt(lo, lc, hi, hc):
    """Viết một khoảng (một mảnh) dưới dạng {x thuộc R | bất đẳng thức} - không dùng trị tuyệt đối."""
    if lo == -_VC:
        dk = r"x %s %s" % (r"\le" if hc else "<", _k_so(hi))
    elif hi == _VC:
        dk = r"x %s %s" % (r"\ge" if lc else ">", _k_so(lo))
    else:
        dk = r"%s %s x %s %s" % (_k_so(lo), r"\le" if lc else "<", r"\le" if hc else "<", _k_so(hi))
    return r"\left\{x \in \mathbb{R} \mid %s\right\}" % dk


def L10_C1_B2_NB017_MC_I_01(socau, dang=1):
    r"""Viết tập con của $\mathbb{R}$ dưới dạng khoảng, đoạn, nửa khoảng (và
    ngược lại: khoảng, đoạn viết lại bằng tính chất đặc trưng).

    CLAUDE THEM 30/09/2026 - dang MOI (mapping co ghi chu), theo cac cau "A =
    {x thuoc R | 4 <= x <= 9}", "A = {x thuoc R | 0 < x < 2} bang tap nao" trong
    de on tap cuoi chuong 1. Muc nhan biet. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        a = random.randint(-9, 6)
        b = a + random.randint(2, 9)
        kieu = random.randint(0, 2)
        if kieu == 0:
            K = (a, random.random() < .5, b, random.random() < .5)
        elif kieu == 1:
            K = (-_VC, False, b, random.random() < .5)
        else:
            K = (a, random.random() < .5, _VC, False)
        S = [K]
        # phương án nhiễu: đổi đóng/mở từng đầu mút; tia ngược chiều; tập liệt kê hai đầu mút
        cac = []
        for S2 in (_k_lat(S, 0, 0), _k_lat(S, 0, 1), _k_lat(_k_lat(S, 0, 0), 0, 1)):
            if S2 != S and S2 not in cac:
                cac.append(S2)
        if K[0] == -_VC or K[2] == _VC:
            x0 = K[2] if K[0] == -_VC else K[0]
            for dong in (True, False):
                cac.append([(x0, dong, _VC, False)] if K[0] == -_VC else [(-_VC, False, x0, dong)])
        nguoc = random.random() < 0.4
        if not nguoc:
            dap = "$%s$" % _k_tex(S)
            ung = ["$%s$" % _k_tex(S2) for S2 in cac]
            if K[0] != -_VC and K[2] != _VC:
                ung.append(r"$\left\{%d; %d\right\}$" % (a, b))
            ung = list(dict.fromkeys(u for u in ung if u != dap))
            random.shuffle(ung)
            ung = ung[:3]
            debai = r"Tập hợp $A = %s$ bằng tập hợp nào dưới đây?" % _k_bdt(*K)
            giai = r"$A = %s = %s$." % (_k_bdt(*K), _k_tex(S))
        else:
            dap = "$%s$" % _k_bdt(*K)
            ung = list(dict.fromkeys("$%s$" % _k_bdt(*S2[0]) for S2 in cac))
            ung = [u for u in ung if u != dap]
            random.shuffle(ung)
            ung = ung[:3]
            debai = r"Tập hợp $A = %s$ được viết dưới dạng tính chất đặc trưng là" % _k_tex(S)
            giai = (r"Dấu ngoặc vuông: đầu mút được lấy (dấu $\le$, $\ge$); dấu ngoặc tròn: không lấy (dấu $<$, "
                    r"$>$). Vậy $A = %s$." % _k_bdt(*K))
        cauTN += MC_SA_answer_text(debai, dap, ung, giai, 0, 0, dang)
    return cauTN


def L10_C1_B1_TH003_MC_A_03(socau, dang=1):
    r"""Mệnh đề chứa biến $P(x)$ (bất đẳng thức bậc hai); thay từng giá trị để
    chọn mệnh đề đúng (sai) trong $P(a)$, $P(b)$, $P(c)$, $P(d)$.

    CLAUDE THEM 30/09/2026 - bien the 03 cua TH003_MC_A, theo cau "P(x): x + 15
    <= x^2; menh de nao dung: P(3), P(4), P(0), P(5)" trong de on tap cuoi
    chuong 1. Co Lan duyet.
    """
    import operator as _op
    DAU = [(r"\le", _op.le), ("<", _op.lt), (r"\ge", _op.ge), (">", _op.gt)]
    cauTN = ""
    so = 0
    while so < socau:
        k = random.randint(2, 20)
        dt, fn = random.choice(DAU)
        hoi_dung = random.choice([True, False])
        cand = list(range(-5, 9))
        dung_ds = [v for v in cand if fn(v + k, v * v) == hoi_dung]
        sai_ds = [v for v in cand if fn(v + k, v * v) != hoi_dung]
        if not dung_ds or len(sai_ds) < 3:
            continue
        chon = random.choice(dung_ds)
        khac = random.sample(sai_ds, 3)
        so += 1
        debai = (r"Cho mệnh đề chứa biến $P(x)$: ``$x + %d %s x^2$'' với $x \in \mathbb{R}$. Mệnh đề nào sau đây "
                 r"%s?" % (k, dt, "đúng" if hoi_dung else r"\textbf{sai}"))
        dong = []
        for v in sorted([chon] + khac):
            ok = fn(v + k, v * v)
            dong.append(r"$P(%d)$: $%s + %d %s %s$, tức là $%d %s %d$ (%s)"
                        % (v, "(%d)" % v if v < 0 else "%d" % v, k, dt, ("(%d)^2" % v) if v < 0 else "%d^2" % v,
                           v + k, dt, v * v, "đúng" if ok else "sai"))
        giai = r"Thay trực tiếp: " + r"; ".join(dong) + r". Vậy chọn $P(%d)$." % chon
        cauTN += MC_SA_answer_text(debai, "$P(%d)$" % chon, ["$P(%d)$" % v for v in khac], giai, 0, 0, dang)
    return cauTN


def _md_luong_tu():
    """Một mệnh đề có ∀/∃ trên tập số, kèm chân trị và lí do (tham số do Python chọn)."""
    loai = random.randint(0, 8)
    k = random.randint(2, 9)
    if loai == 0:
        return (r"\exists n \in \mathbb{N},\ n^2 = %dn" % k, True, r"với $n = %d$ thì $%d^2 = %d\cdot %d$" % (k, k, k, k))
    if loai == 1:
        if random.random() < .5:
            return (r"\forall n \in \mathbb{N},\ n^2 > 0", False, r"với $n = 0$ thì $n^2 = 0$")
        return (r"\forall n \in \mathbb{N}^*,\ n^2 > 0", True, r"$n \ge 1$ nên $n^2 \ge 1 > 0$")
    if loai == 2:
        return (r"\forall n \in \mathbb{N},\ n^2 + 1 \text{ là số lẻ}", False, r"với $n = 1$ thì $n^2 + 1 = 2$ chẵn")
    if loai == 3:
        c = random.choice([2, 3, 5, 6, 7, 4, 9, 16, 25, 36])
        s = math.isqrt(c)
        dung = s * s == c
        return (r"\exists n \in \mathbb{N},\ n^2 - %d = 0" % c, dung,
                (r"với $n = %d$" % s) if dung else (r"$n^2 = %d$ cho $n = \sqrt{%d} \notin \mathbb{N}$" % (c, c)))
    if loai == 4:
        return (r"\forall n \in \mathbb{N},\ n^2 + n \text{ chia hết cho } 2", True,
                r"$n^2 + n = n(n + 1)$ là tích hai số tự nhiên liên tiếp")
    if loai == 5:
        if random.random() < .5:
            return (r"\forall n \in \mathbb{N},\ n^2 \ge n", True, r"$n^2 - n = n(n - 1) \ge 0$ với $n$ tự nhiên")
        return (r"\forall x \in \mathbb{R},\ x^2 \ge x", False,
                r"với $x = \dfrac{1}{2}$ thì $x^2 = \dfrac{1}{4} < \dfrac{1}{2}$")
    if loai == 6:
        a_ = random.randint(2, 6)
        b_ = random.choice([i for i in range(-15, 16) if i])
        dung = b_ % a_ == 0
        return (r"\exists n \in \mathbb{Z},\ %dn = %d" % (a_, b_), dung,
                r"$n = %s$ %s số nguyên" % (_tex_so(Rational(b_, a_)), "là" if dung else "không là"))
    if loai == 7:
        c = random.randint(1, 9)
        if random.random() < .5:
            return (r"\forall x \in \mathbb{R},\ x^2 + %d > 0" % c, True, r"$x^2 + %d \ge %d > 0$" % (c, c))
        return (r"\forall x \in \mathbb{R},\ x^2 - %d > 0" % c, False, r"với $x = 0$ thì $x^2 - %d = -%d < 0$" % (c, c))
    m = random.randint(2, 9)
    c = m * (m + 1) if random.random() < .5 else m * (m + 1) + 1
    s = next((t for t in range(0, 20) if t * t + t == c), None)
    return (r"\exists n \in \mathbb{N},\ n^2 + n = %d" % c, s is not None,
            (r"với $n = %d$" % s) if s is not None else
            (r"$n^2 + n = n(n + 1)$ luôn chẵn mà $%d$ lẻ" % c if c % 2 else r"không có $n$ nào thoả mãn"))


def L10_C1_B1_TH014_MC_A_02(socau, dang=1):
    r"""Mệnh đề chứa kí hiệu $\forall$, $\exists$ trên $\mathbb{N}$, $\mathbb{Z}$,
    $\mathbb{R}$: chọn mệnh đề đúng (sai); tham số do Python chọn.

    CLAUDE THEM 30/09/2026 - bien the 02 cua TH014_MC_A, theo cau "ton tai n
    thuoc N: n^2 = n; voi moi n: n^2 > 0; n^2 + 1 le; n^2 - 2 = 0" trong de on
    tap cuoi chuong 1. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        hoi_dung = random.choice([True, False])
        chon, cung, da = None, [], set()
        for _t in range(500):
            t, d_, l = _md_luong_tu()
            khoa = t
            if khoa in da:
                continue
            if d_ == hoi_dung and chon is None:
                chon = (t, d_, l); da.add(khoa)
            elif d_ != hoi_dung and len(cung) < 3:
                cung.append((t, d_, l)); da.add(khoa)
            if chon and len(cung) == 3:
                break
        debai = r"Mệnh đề nào sau đây %s?" % ("đúng" if hoi_dung else r"\textbf{sai}")
        giai = (r"$%s$ %s vì %s.\\ " % (chon[0], "đúng" if hoi_dung else "sai", chon[2])
                + r"\\ ".join(r"$%s$ %s (%s)." % (t, "đúng" if d_ else "sai", l) for t, d_, l in cung))
        cauTN += MC_SA_answer_text(debai, "$%s$" % chon[0], ["$%s$" % c_[0] for c_ in cung], giai, 0, 0, dang)
    return cauTN


def _md_bdt():
    """Một mệnh đề kéo theo / tương đương giữa hai bất đẳng thức số, chân trị tính bằng số."""
    if random.random() < 0.3:
        X, v, X2 = r"\pi", math.pi, (r"\pi^2", math.pi ** 2)
    else:
        a = random.choice([i for i in range(2, 60) if math.isqrt(i) ** 2 != i])
        X, v, X2 = r"\sqrt{%d}" % a, math.sqrt(a), ("%d" % a, a)
    b = int(round(v)) + random.choice([-1, 0, 1])
    if b <= 0 or abs(b - v) < 1e-9:
        b = int(math.ceil(v))
    lon = random.random() < .5                       # P: X < b  hay  X > b
    P_tex = r"%s %s %d" % (X, ">" if lon else "<", b)
    P_dung = (v > b) if lon else (v < b)
    c = random.randint(2, 5)
    kieu = random.randint(0, 3)
    if kieu == 0:          # nhân -c, đổi chiều ĐÚNG hoặc quên đổi chiều
        doi = random.random() < .6
        dau = (("<" if lon else ">") if doi else (">" if lon else "<"))
        Q_tex = r"-%d%s %s -%d\cdot %d" % (c, X, dau, c, b)
        Q_dung = (-c * v < -c * b) if dau == "<" else (-c * v > -c * b)
    elif kieu == 1:        # nhân c > 0
        dau = ">" if lon else "<"
        Q_tex = r"%d%s %s %d\cdot %d" % (c, X, dau, c, b)
        Q_dung = (c * v > c * b) if lon else (c * v < c * b)
    elif kieu == 2:        # bình phương hai vế dương
        dau = ">" if lon else "<"
        Q_tex = r"%s %s %d" % (X2[0], dau, b * b)
        Q_dung = (X2[1] > b * b) if lon else (X2[1] < b * b)
    else:                  # đổi dấu cả hai vế: -X ? -b
        dau = random.choice(["<", ">"])
        Q_tex = r"-%s %s -%d" % (X, dau, b)
        Q_dung = (-v < -b) if dau == "<" else (-v > -b)
    tuong_duong = random.random() < 0.4
    ki = r"\Leftrightarrow" if tuong_duong else r"\Rightarrow"
    dung = (P_dung == Q_dung) if tuong_duong else ((not P_dung) or Q_dung)
    ly = (r"$%s$ %s, $%s$ %s" % (P_tex, "đúng" if P_dung else "sai", Q_tex, "đúng" if Q_dung else "sai")
          + (r" nên mệnh đề tương đương %s" % ("đúng" if dung else "sai") if tuong_duong else
             r" nên mệnh đề kéo theo %s" % ("đúng" if dung else "sai (P đúng, Q sai)" if not dung else "đúng")))
    return r"%s %s %s" % (P_tex, ki, Q_tex), dung, ly


def L10_C1_B1_VD014_MC_C_01(socau, dang=1):
    r"""Tính đúng sai của mệnh đề kéo theo, tương đương giữa hai bất đẳng thức
    số (có căn, có $\pi$): nhân với số âm, số dương, bình phương hai vế.

    CLAUDE THEM 30/09/2026 - dang MOI (mapping co ghi chu), theo cau "can 23 < 5
    => -2can23 > -2.5; -pi < -2 <=> pi^2 < 4..." trong de on tap cuoi chuong 1
    (co ghi muc K - van dung). Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        hoi_dung = random.choice([True, False])
        chon, cung, da = None, [], set()
        for _t in range(800):
            t, d_, l = _md_bdt()
            if t in da:
                continue
            if d_ == hoi_dung and chon is None:
                chon = (t, d_, l); da.add(t)
            elif d_ != hoi_dung and len(cung) < 3:
                cung.append((t, d_, l)); da.add(t)
            if chon and len(cung) == 3:
                break
        debai = r"Trong các mệnh đề sau, mệnh đề nào %s?" % ("đúng" if hoi_dung else r"\textbf{sai}")
        giai = (r"Mệnh đề $P \Rightarrow Q$ chỉ sai khi $P$ đúng và $Q$ sai; $P \Leftrightarrow Q$ đúng khi $P$, $Q$ "
                r"cùng đúng hoặc cùng sai.\\ " + r"\\ ".join(r"$%s$: %s." % (t, l) for t, _, l in [chon] + cung))
        cauTN += MC_SA_answer_text(debai, "$%s$" % chon[0], ["$%s$" % c_[0] for c_ in cung], giai, 0, 0, dang)
    return cauTN


def L10_C1_B2_VD021_MC_B_01(socau, dang=1):
    r"""Phép toán kết hợp trên BA khoảng / đoạn / nửa khoảng: $(A \cap B) \cup
    (A \cap C)$, $A \cap B \cap C$, $(A \cup B) \setminus C$...; đáp án có thể
    viết bằng kí hiệu khoảng hoặc bằng tính chất đặc trưng.

    CLAUDE THEM 30/09/2026 - dang MOI (mapping co ghi chu), theo cac cau "A =
    (-inf; 1], B = [-2; 2], C = (0; 5), P = (A giao B) hop (A giao C)" va "A giao
    B giao C = {x | -2 < x < 1/2}" trong de on tap cuoi chuong 1. Co Lan duyet.
    """
    def ngau_khoang(lo, hi):
        t = random.randint(0, 3)
        if t == 0:
            return (-_VC, False, hi, random.random() < .5)
        if t == 1:
            return (lo, random.random() < .5, _VC, False)
        return (lo, random.random() < .5, hi, random.random() < .5)

    BIEU = [(r"(A \cap B) \cup (A \cap C)", lambda A, B, C: _k_phep(_k_phep(A, B, "giao"), _k_phep(A, C, "giao"), "hop")),
            (r"A \cap B \cap C", lambda A, B, C: _k_phep(_k_phep(A, B, "giao"), C, "giao")),
            (r"(A \cup B) \cap C", lambda A, B, C: _k_phep(_k_phep(A, B, "hop"), C, "giao")),
            (r"(A \cap B) \setminus C", lambda A, B, C: _k_phep(_k_phep(A, B, "giao"), C, "hieu")),
            (r"A \cap (B \cup C)", lambda A, B, C: _k_phep(A, _k_phep(B, C, "hop"), "giao")),
            (r"(A \setminus B) \cup C", lambda A, B, C: _k_phep(_k_phep(A, B, "hieu"), C, "hop"))]
    cauTN = ""
    so = 0
    while so < socau:
        p = sorted(random.sample(range(-8, 9), 6))
        A = [ngau_khoang(p[0], p[3])]
        B = [ngau_khoang(p[1], p[4])]
        C = [ngau_khoang(p[2], p[5])]
        i = random.randrange(len(BIEU))
        ten, f = BIEU[i]
        kq = f(A, B, C)
        if not kq or kq == [(-_VC, False, _VC, False)]:
            continue
        bdt = len(kq) == 1 and random.random() < 0.35
        viet = (lambda S: "$%s$" % _k_bdt(*S[0])) if bdt else (lambda S: "$%s$" % _k_tex(S))
        dap = viet(kq)
        ung = []
        for j in range(len(kq)):
            for d_ in (0, 1):
                t_ = viet(_k_lat(kq, j, d_))
                if t_ != dap and t_ not in ung:
                    ung.append(t_)
        random.shuffle(ung)
        for j, (_, g) in enumerate(BIEU):
            if j == i:
                continue
            S2 = g(A, B, C)
            if S2 and (not bdt or len(S2) == 1) and S2 != [(-_VC, False, _VC, False)]:
                t_ = viet(S2)
                if t_ != dap and t_ not in ung:
                    ung.insert(0, t_)
                    break
        ung = ung[:3]
        if len(ung) < 3:
            continue
        so += 1
        debai = (r"Cho ba tập hợp $A = %s$, $B = %s$ và $C = %s$. Tập hợp $%s$ là"
                 % (_k_tex(A), _k_tex(B), _k_tex(C), ten))
        trung = []
        if "A \\cap B" in ten and "(A \\cap B) \\cup" not in ten:
            trung.append(r"$A \cap B = %s$" % _k_tex(_k_phep(A, B, "giao")))
        if "(A \\cap B) \\cup (A \\cap C)" == ten:
            trung += [r"$A \cap B = %s$" % _k_tex(_k_phep(A, B, "giao")),
                      r"$A \cap C = %s$" % _k_tex(_k_phep(A, C, "giao"))]
        if "A \\cup B" in ten:
            trung.append(r"$A \cup B = %s$" % _k_tex(_k_phep(A, B, "hop")))
        if "B \\cup C" in ten:
            trung.append(r"$B \cup C = %s$" % _k_tex(_k_phep(B, C, "hop")))
        if "A \\setminus B" in ten:
            trung.append(r"$A \setminus B = %s$" % _k_tex(_k_phep(A, B, "hieu")))
        giai = ((r"Ta có " + ", ".join(trung) + r".\\ " if trung else "")
                + r"Biểu diễn trên trục số ta được $%s = %s$%s." % (ten, _k_tex(kq),
                                                                   (r" $= %s$" % _k_bdt(*kq[0])) if bdt else ""))
        cauTN += MC_SA_answer_text(debai, dap, ung, giai, 0, 0, dang)
    return cauTN


_BOI_CANH_BA_TAP = [("Trong một khoảng thời gian, đài khí tượng thống kê được", "ngày",
                     ("mưa", "có gió", "lạnh"), "thời tiết xấu (mưa, có gió hoặc lạnh)"),
                    ("Một nhóm học sinh giỏi có", "em", ("giỏi Văn", "giỏi Toán", "giỏi Anh"),
                     "của nhóm (mỗi em giỏi ít nhất một môn)"),
                    ("Trong một đợt khảo sát, có", "người", ("dùng Zalo", "dùng Facebook", "dùng TikTok"),
                     "dùng ít nhất một trong ba ứng dụng")]


def L10_C1_B2_VD020_MC_A_03(socau, dang=1):
    r"""Ba tập hợp thực tế: biết $n(A)$, $n(B)$, $n(C)$, số phần tử của từng giao
    hai tập và của giao ba tập; tính số phần tử của hợp.

    CLAUDE THEM 30/09/2026 - bien the 03 cua VD020_MC_A, theo cau "10 ngay mua,
    8 ngay gio, 6 ngay lanh, 5 mua-gio, 4 mua-lanh, 3 lanh-gio, 1 ca ba" trong
    de on tap cuoi chuong 1. Co Lan duyet.
    """
    cauTN = ""
    for _ in range(socau):
        x = random.randint(1, 4)
        ab, bc, ca = (random.randint(0, 5) for _ in range(3))
        a1, b1, c1 = (random.randint(1, 8) for _ in range(3))
        nA, nB, nC = a1 + ab + ca + x, b1 + ab + bc + x, c1 + bc + ca + x
        nAB, nBC, nCA = ab + x, bc + x, ca + x
        hop = a1 + b1 + c1 + ab + bc + ca + x
        mo, dv, (t1, t2, t3), hoi = random.choice(_BOI_CANH_BA_TAP)
        debai = (r"%s: $%d$ %s %s, $%d$ %s %s, $%d$ %s %s; $%d$ %s vừa %s vừa %s, $%d$ %s vừa %s vừa %s, $%d$ %s "
                 r"vừa %s vừa %s; $%d$ %s cả ba. Số %s %s là"
                 % (mo, nA, dv, t1, nB, dv, t2, nC, dv, t3, nAB, dv, t1, t2, nCA, dv, t1, t3, nBC, dv, t2, t3,
                    x, dv, dv, hoi))
        tong = nA + nB + nC
        giai = (r"Gọi $A$, $B$, $C$ là tập các %s %s, %s, %s. Ta có\\ "
                r"$n(A \cup B \cup C) = n(A) + n(B) + n(C) - n(A \cap B) - n(B \cap C) - n(C \cap A) + n(A \cap B \cap C)$"
                r"\\ $= %d + %d + %d - (%d + %d + %d) + %d = %d$."
                % (dv, t1, t2, t3, nA, nB, nC, nAB, nBC, nCA, x, hop))
        ung = [hop - x, tong - nAB - nBC - nCA, tong, hop + x]
        nhieu = _ba_nhieu("$%d$" % hop, ["$%d$" % v for v in ung if v > 0], buoc=lambda k: "$%d$" % (hop + k + 1))
        cauTN += MC_SA_answer_text(debai, "$%d$" % hop, nhieu, giai, 0, 0, dang)
    return cauTN


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
