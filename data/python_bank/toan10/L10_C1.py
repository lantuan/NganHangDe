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


def L10_C1_B1_NB001_MC_A_02(socau, dang=1):

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


def L10_C1_B1_TH003_MC_A_02(socau, dang=1):

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



def L10_C1_B1_TH003_TL_A_01(socau, dang):

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
            dang
        )

    return cauTN

def L10_C1_B1_TH003_TL_A_02(socau, dang):

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
            dang
        )

    return cauTN



def L10_C1_B1_NB005_MC_A_01(socau, dang):
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

def L10_C1_B1_NB005_MC_B_01(socau, dang):

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

def L10_C1_B1_NB005_MC_C_01(socau, dang):

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

def L10_C1_B1_NB007_MC_A_01(socau, dang):

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

def L10_C1_B1_NB007_MC_A_02(socau, dang=1):
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


def L10_C1_B1_NB007_MC_B_01(socau, dang):

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

def L10_C1_B1_NB007_MC_B_02(socau, dang=1):

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


def L10_C1_B1_NB008_MC_A_01(socau, dang):

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



def L10_C1_B1_NB008_MC_B_01(socau, dang):

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

def L10_C1_B1_NB010_MC_A_01(socau, dang):

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


def L10_C1_B1_NB010_MC_A_02(socau, dang):

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

        # Thiết lập cụm từ tiếng Việt chuẩn xác theo từng loại tính chất hình học
        if loai_tinh_chat == 0:
            P_text = f"hai góc $\\widehat{{{goc1}}}$ và $\\widehat{{{goc2}}}$ phụ nhau"
            Q_text = f"tổng số đo của chúng bằng $90^\\circ$"

            P_phu_dinh = f"hai góc $\\widehat{{{goc1}}}$ và $\\widehat{{{goc2}}}$ không phụ nhau"
            Q_phu_dinh = f"tổng số đo của chúng khác $90^\\circ$"
            P_sai_tinh_chat = f"hai góc $\\widehat{{{goc1}}}$ và $\\widehat{{{goc2}}}$ bù nhau"
            Q_sai_tinh_chat = f"tổng số đo của chúng bằng $180^\\circ$"
        else:
            P_text = f"hai góc $\\widehat{{{goc1}}}$ và $\\widehat{{{goc2}}}$ bù nhau"
            Q_text = f"tổng số đo của chúng bằng $180^\\circ$"

            P_phu_dinh = f"hai góc $\\widehat{{{goc1}}}$ và $\\widehat{{{goc2}}}$ không bù nhau"
            Q_phu_dinh = f"tổng số đo của chúng khác $180^\\circ$"
            P_sai_tinh_chat = f"hai góc $\\widehat{{{goc1}}}$ và $\\widehat{{{goc2}}}$ phụ nhau"
            Q_sai_tinh_chat = f"tổng số đo của chúng bằng $90^\\circ$"

        debai = f"""Hãy phát biểu mệnh đề đảo của mệnh đề: ``Nếu {P_text} thì {Q_text}''."""

        # Mệnh đề đảo chuẩn mực: Nếu Q thì P
        dapso = f"""Nếu {Q_text} thì {P_text}."""

        # Sinh các phương án nhiễu logic
        dsnhieu = [
            f"""Nếu {P_phu_dinh} thì {Q_phu_dinh}.""",
            f"""Nếu {Q_phu_dinh} thì {P_phu_dinh}.""",
            f"""Nếu {Q_sai_tinh_chat} thì {P_sai_tinh_chat}."""
        ]

        giai = f"""Xét mệnh đề kéo theo đã cho có cấu trúc: ``Nếu $P$ thì $Q$'' (ký hiệu là $P \\Rightarrow Q$), trong đó:\\\\
        - $P$: ``{P_text}''\\\\
        - $Q$: ``{Q_text}''\\\\
        Theo định nghĩa toán học, mệnh đề đảo của mệnh đề $P \\Rightarrow Q$ là mệnh đề $Q \\Rightarrow P$, phát biểu dưới dạng ngôn ngữ là: ``Nếu $Q$ thì $P$''.\\\\
        Do đó, mệnh đề đảo của mệnh đề trên là: ``Nếu {Q_text} thì {P_text}''. """

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B1_NB011_MC_A_01(socau, dang):

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


def L10_C1_B1_NB013_MC_A_01(socau, dang):

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


def L10_C1_B1_NB013_MC_B_01(socau, dang):

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



def L10_C1_B1_TH014_MC_A_01(socau, dang):

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
            a = random.randint(2,20)
            b = random.choice([u for u in range(1,a+1) if a % u == 0])
            dapso = rf"$\forall n\in\mathbb Z,\ {a}\mid n\Rightarrow {b}\mid n$"
            dsnhieu = [
                rf"$\forall n\in\mathbb Z,\ {b}\mid n\Rightarrow {a}\mid n$",
                rf"$\exists n\in\mathbb Z,\ {a}\mid n\Rightarrow {b}\nmid n$",
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


def L10_C1_B1_TH014_MC_A_02(socau, dang): ####### kiểm tra lại nội dung câu hỏi, các phương án.

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

            a = random.randint(2, 20)

            b = random.choice([u for u in range(1, a + 1) if a % u == 0])

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


def L10_C1_B1_NB015_MC_A_01(socau, dang):

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

def L10_C1_B1_NB015_MC_A_02(socau, dang):

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

def L10_C1_B1_NB015_MC_B_01(socau, dang):

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

def L10_C1_B2_NB017_MC_A_01(socau, dang):
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

            dapso = f"""$\\left\\{{ {pt1}, {ngoai} \\right\\}}$"""

            giai = (
                f"Ta có ${ngoai} \\notin A$ nên "
                f"$\\left\\{{ {pt1}, {ngoai} \\right\\}}$ không phải là tập con của $A$."
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

        nhieu3 = f"""$\\left\\{{ {pt3}, {pt4} \\right\\}}$"""

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

        cach_hoi = np.random.randint(0, 4)

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
                Tìm phương án sai trong các khẳng định sau."""
            )

        else:

            debai = (
                f"""Xét tập hợp $A = {A_latex}$.\\\\
                Trong các phương án sau, phương án nào không đúng?"""
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

def L10_C1_B2_NB017_MC_A_02(socau, dang):

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
                f"$\\left\\{{ {a}, {b} \\right\\}}$"
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

def L10_C1_B2_NB017_MC_B_01(socau, dang):

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

def L10_C1_B2_NB017_MC_B_02(socau, dang):

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
        # TẠO KÍ HIỆU
        # =====================================================

        ds_ki_hieu = random.choice([

            ['a', 'b', 'c', 'd'],

            ['x', 'y', 'z', 't'],

            ['m', 'n', 'p', 'q'],

            ['u', 'v', 'w', 'z']
        ])

        pt1, pt2, pt3, pt4 = ds_ki_hieu

        # =====================================================
        # GHÉP KÍ HIỆU VỚI PHẦN TỬ THẬT
        # =====================================================

        gia_tri = random.sample(A_list, 4)

        phan_tu_map = dict(zip(ds_ki_hieu, gia_tri))

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

                f"Ta gán ${pt1} = {phan_tu_map[pt1]}$. "
                f"Vì ${phan_tu_map[pt1]} \\in A$ nên "
                f"${pt1} \\in A$ là đúng."
            ),

            (
                f"${pt2} \\subset A$",

                False,

                f"Ta gán ${pt2} = {phan_tu_map[pt2]}$. "
                f"${pt2}$ là phần tử nên không dùng kí hiệu "
                f"$\\subset$."
            ),

            (
                f"$\\left\\{{ {pt3} \\right\\}} \\in A$",

                False,

                f"Ta gán ${pt3} = {phan_tu_map[pt3]}$. "
                f"$A$ không chứa phần tử "
                f"$\\left\\{{ {phan_tu_map[pt3]} \\right\\}}$."
            ),

            (
                f"$\\left\\{{ {pt4} \\right\\}} \\subset A$",

                True,

                f"Ta gán ${pt4} = {phan_tu_map[pt4]}$. "
                f"Mọi phần tử của "
                f"$\\left\\{{ {phan_tu_map[pt4]} \\right\\}}$ đều thuộc $A$."
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

    return


def L10_C1_B2_NB017_MC_B_03(socau, dang):

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

def L10_C1_B2_TH018_MC_A_01(socau, dang):

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

def L10_C1_B2_TH018_MC_B_01(socau, dang):

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
                f"${tap1} \\setminus {tap2}=\\left\\{{{', '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        elif pheptoan_code == 1:
            pheptoan_tex = f"{tap2} \\setminus {tap1}"
            z_ans = len_hieu_BA
            tap_kq_list = sorted(list(B_set - A_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap2} \\setminus {tap1}$ gồm các phần tử thuộc "
                f"${tap2}$ nhưng không thuộc ${tap1}$. Ta có "
                f"${tap2} \\setminus {tap1}=\\left\\{{{', '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        elif pheptoan_code == 2:
            pheptoan_tex = f"{tap1} \\cap {tap2}"
            z_ans = len_giao
            tap_kq_list = sorted(list(A_set & B_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap1} \\cap {tap2}$ gồm các phần tử vừa thuộc "
                f"${tap1}$ vừa thuộc ${tap2}$. Ta có "
                f"${tap1} \\cap {tap2}=\\left\\{{{', '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        else:
            pheptoan_tex = f"{tap1} \\cup {tap2}"
            z_ans = len_hop
            tap_kq_list = sorted(list(A_set | B_set))
            giai_chi_tiet = (
                f"Tập hợp ${tap1} \\cup {tap2}$ gồm các phần tử thuộc "
                f"${tap1}$ hoặc thuộc ${tap2}$. Ta có "
                f"${tap1} \\cup {tap2}=\\left\\{{{', '.join(map(str, tap_kq_list))}\\right\\}}$."
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


def L10_C1_B2_NB017_MC_C_01(socau, dang):

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


def L10_C1_B2_TH021_MC_A_01(socau, dang):

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

def L10_C1_B2_TH019_MC_A_01(socau, dang):

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

def L10_C1_B2_VD020_MC_A_01(socau, dang):

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

def L10_C1_B2_VD021_MC_A_01(socau, dang):

    gt = []
    dem = 0
    while dem < socau:
        kieu = int(np.random.choice([1, 2, 3, 4]))
        # 1: A \cup B = A
        # 2: A \cup B = B
        # 3: A \cap B = \varnothing
        # 4: A \cap B \ne \varnothing

        a_val = np.random.randint(-15, 5)
        b_val = np.random.randint(a_val + 5, 16)

        # =========================
        # KIỂU 1: A \cup B = A
        # <=> B \subset A
        # B = (n;m], cần n < m <= b
        # Chọn n nằm trong A để lời giải gọn
        # =========================
        if kieu == 1:
            n_val = np.random.randint(a_val + 1, b_val)
            z_ans = b_val - n_val

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        # =========================
        # KIỂU 2: A \cup B = B
        # <=> A \subset B
        # Với A = [a;b], B = (n;m]
        # cần n < a và m >= b
        # Chọn n < a để điều kiện còn lại chỉ là m >= b
        # =========================
        elif kieu == 2:
            n_val = np.random.randint(a_val - 8, a_val)
            z_ans = 16 - b_val   # m nguyên từ b_val đến 15

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        # =========================
        # KIỂU 3: A \cap B = \varnothing
        # Ép B nằm hoàn toàn bên trái A
        # B = (n;m], cần n < m < a
        # =========================
        elif kieu == 3:
            n_val = np.random.randint(a_val - 8, a_val - 1)
            z_ans = a_val - n_val - 1   # số m nguyên thỏa n < m < a

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        # =========================
        # KIỂU 4: A \cap B \ne \varnothing
        # Chọn n < a để khi đó giao khác rỗng <=> m >= a
        # Vì A chứa a_val, B = (n;m] chứa a_val khi m >= a_val
        # m nguyên từ a_val đến 15
        # =========================
        else:
            n_val = np.random.randint(a_val - 8, a_val)
            z_ans = 16 - a_val   # m nguyên từ a_val đến 15

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        kieu, a_val, b_val, n_val, z_ans = v

        ds_nhieu_so = []
        sai_so = [-3, -2, -1, 1, 2, 3, 4]
        for delta in sai_so:
            val_nhieu = z_ans + delta
            if val_nhieu >= 0 and val_nhieu != z_ans and val_nhieu not in ds_nhieu_so:
                ds_nhieu_so.append(val_nhieu)

        if len(ds_nhieu_so) < 3:
            continue

        nhieu_chon = list(np.random.choice(ds_nhieu_so, size=3, replace=False))
        dsnhieu = [
            f"""${nhieu_chon[0]}$""",
            f"""${nhieu_chon[1]}$""",
            f"""${nhieu_chon[2]}$"""
        ]

        # =========================
        # KIỂU 1: A \cup B = A
        # =========================
        if kieu == 1:
            debai = f"""Cho hai tập hợp $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$. Có tất cả bao nhiêu giá trị nguyên của tham số $m$ để $A \\cup B = A$?"""
            dapso = f"""${z_ans}$"""

            giai = f"""Ta có $A \\cup B = A \\Leftrightarrow B \\subset A$.\\\\
Vì $B = \\left( {n_val}; m \\right]$ nên để $B \\subset A = \\left[ {a_val}; {b_val} \\right]$ thì cần
$\\heva{{m > {n_val} \\\\ m \\le {b_val}}}$.\\\\
Suy ra ${n_val} < m \\le {b_val}$.\\\\
Vì $m \\in \\mathbb{{Z}}$ nên số giá trị nguyên của $m$ là
${b_val} - {n_val} = {z_ans}$.\\\\
Vậy có tất cả ${z_ans}$ giá trị nguyên của tham số $m$ thỏa mãn yêu cầu đề bài."""

        # =========================
        # KIỂU 2: A \cup B = B
        # =========================
        elif kieu == 2:
            debai = f"""Cho hai tập hợp $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$. Có tất cả bao nhiêu giá trị nguyên của tham số $m$ để $A \\cup B = B$?"""
            dapso = f"""${z_ans}$"""

            giai = f"""Ta có $A \\cup B = B \\Leftrightarrow A \\subset B$.\\\\
Với $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$, để $A \\subset B$ thì cần
$\\heva{{{n_val} < {a_val} \\\\ m \\ge {b_val}}}$.\\\\
Do ${n_val} < {a_val}$ luôn đúng theo cách chọn dữ liệu nên chỉ cần
$m \\ge {b_val}$.\\\\
Vì $m \\in \\mathbb{{Z}}$ và theo cách sinh dữ liệu ta có $m \\le 15$, nên
$m \\in \\{{{b_val}, {b_val + 1}, \\ldots, 15\\}}$.\\\\
Số giá trị nguyên của $m$ là
$15 - {b_val} + 1 = {z_ans}$.\\\\
Vậy có tất cả ${z_ans}$ giá trị nguyên của tham số $m$ thỏa mãn yêu cầu đề bài."""

        # =========================
        # KIỂU 3: A \cap B = \varnothing
        # =========================
        elif kieu == 3:
            debai = f"""Cho hai tập hợp $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$. Có tất cả bao nhiêu giá trị nguyên của tham số $m$ để $A \\cap B = \\varnothing$?"""
            dapso = f"""${z_ans}$"""

            giai = f"""Để $A \\cap B = \\varnothing$ thì hai tập hợp không có phần tử chung.\\\\
Với $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$, để $B$ nằm hoàn toàn bên trái $A$ thì cần
$m < {a_val}$.\\\\
Mặt khác, để $B = \\left( {n_val}; m \\right]$ là tập hợp khác rỗng thì cần
$m > {n_val}$.\\\\
Suy ra
${n_val} < m < {a_val}$.\\\\
Vì $m \\in \\mathbb{{Z}}$ nên số giá trị nguyên của $m$ là
${a_val} - {n_val} - 1 = {z_ans}$.\\\\
Vậy có tất cả ${z_ans}$ giá trị nguyên của tham số $m$ thỏa mãn yêu cầu đề bài."""

        # =========================
        # KIỂU 4: A \cap B \ne \varnothing
        # =========================
        else:
            debai = f"""Cho hai tập hợp $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$. Có tất cả bao nhiêu giá trị nguyên của tham số $m$ để $A \\cap B \\ne \\varnothing$?"""
            dapso = f"""${z_ans}$"""

            giai = f"""Để $A \\cap B \\ne \\varnothing$ thì hai tập hợp phải có ít nhất một phần tử chung.\\\\
Do ${n_val} < {a_val}$ theo cách chọn dữ liệu nên để $A = \\left[ {a_val}; {b_val} \\right]$ và $B = \\left( {n_val}; m \\right]$ có phần tử chung, chỉ cần
$m \\ge {a_val}$.\\\\
Khi đó phần tử ${a_val}$ thuộc cả $A$ và $B$, suy ra $A \\cap B \\ne \\varnothing$.\\\\
Vì $m \\in \\mathbb{{Z}}$ và theo cách sinh dữ liệu ta có $m \\le 15$, nên
$m \\in \\{{{a_val}, {a_val + 1}, \\ldots, 15\\}}$.\\\\
Số giá trị nguyên của $m$ là
$15 - {a_val} + 1 = {z_ans}$.\\\\
Vậy có tất cả ${z_ans}$ giá trị nguyên của tham số $m$ thỏa mãn yêu cầu đề bài."""

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B2_VD021_TL_A_01(socau, dong=1):

    gt = []
    dem = 0
    while dem < socau:
        kieu = int(np.random.choice([1, 2, 3, 4]))
        # 1: A ∪ B = A
        # 2: A ∪ B = B
        # 3: A ∩ B = ∅
        # 4: A ∩ B ≠ ∅

        a_val = np.random.randint(-15, 5)
        b_val = np.random.randint(a_val + 5, 16)

        # =========================
        # KIỂU 1: A ∪ B = A
        # <=> B ⊂ A
        # B = (n;m], cần n < m <= b
        # =========================
        if kieu == 1:
            n_val = np.random.randint(a_val + 1, b_val)
            z_ans = b_val - n_val

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        # =========================
        # KIỂU 2: A ∪ B = B
        # <=> A ⊂ B
        # cần n < a và m >= b
        # =========================
        elif kieu == 2:
            n_val = np.random.randint(a_val - 8, a_val)
            z_ans = 16 - b_val   # số m nguyên từ b_val đến 15

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        # =========================
        # KIỂU 3: A ∩ B = ∅
        # cần n < m < a
        # =========================
        elif kieu == 3:
            n_val = np.random.randint(a_val - 8, a_val - 1)
            z_ans = a_val - n_val - 1

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        # =========================
        # KIỂU 4: A ∩ B ≠ ∅
        # chọn n < a để điều kiện tương đương m >= a
        # =========================
        else:
            n_val = np.random.randint(a_val - 8, a_val)
            z_ans = 16 - a_val   # số m nguyên từ a_val đến 15

            if z_ans <= 0:
                continue

            v = [kieu, a_val, b_val, n_val, z_ans]

        if v not in gt:
            gt.append(v)
            dem += 1

    cauTL = ''
    for v in gt:
        kieu, a_val, b_val, n_val, z_ans = v

        # =========================
        # KIỂU 1: A ∪ B = A
        # =========================
        if kieu == 1:
            debai = (
                f"Cho hai tập hợp $A = \\left[{a_val}; {b_val}\\right]$ và "
                f"$B = \\left({n_val}; m\\right]$, với $m \\in \\mathbb{{Z}}$. Tính:"
            )

            ds_abcd = [
                (
                    "Số giá trị nguyên của tham số $m$ để $A \\cup B = A$.",
                    z_ans,
                    f"Ta có $A \\cup B = A \\Leftrightarrow B \\subset A$. "
                    f"Vì $B = \\left({n_val}; m\\right]$ nên để $B \\subset A = \\left[{a_val}; {b_val}\\right]$ thì cần "
                    f"$\\heva{{m > {n_val} \\\\ m \\le {b_val}}}$. "
                    f"Suy ra ${n_val} < m \\le {b_val}$. "
                    f"Vì $m \\in \\mathbb{{Z}}$ nên số giá trị nguyên của $m$ là "
                    f"${b_val} - {n_val} = {z_ans}$."
                )
            ]

        # =========================
        # KIỂU 2: A ∪ B = B
        # =========================
        elif kieu == 2:
            debai = (
                f"Cho hai tập hợp $A = \\left[{a_val}; {b_val}\\right]$ và "
                f"$B = \\left({n_val}; m\\right]$, với $m \\in \\mathbb{{Z}}$. Tính:"
            )

            ds_abcd = [
                (
                    "Số giá trị nguyên của tham số $m$ để $A \\cup B = B$.",
                    z_ans,
                    f"Ta có $A \\cup B = B \\Leftrightarrow A \\subset B$. "
                    f"Để $A = \\left[{a_val}; {b_val}\\right]$ là tập con của $B = \\left({n_val}; m\\right]$ thì cần "
                    f"$\\heva{{{n_val} < {a_val} \\\\ m \\ge {b_val}}}$. "
                    f"Do ${n_val} < {a_val}$ luôn đúng theo cách chọn dữ liệu nên chỉ cần $m \\ge {b_val}$. "
                    f"Vì $m \\in \\mathbb{{Z}}$ và theo cách sinh dữ liệu ta có $m \\le 15$, nên "
                    f"$m \\in \\{{{b_val}, {b_val + 1}, \\ldots, 15\\}}$. "
                    f"Vậy số giá trị nguyên của $m$ là $15 - {b_val} + 1 = {z_ans}$."
                )
            ]

        # =========================
        # KIỂU 3: A ∩ B = ∅
        # =========================
        elif kieu == 3:
            debai = (
                f"Cho hai tập hợp $A = \\left[{a_val}; {b_val}\\right]$ và "
                f"$B = \\left({n_val}; m\\right]$, với $m \\in \\mathbb{{Z}}$. Tính:"
            )

            ds_abcd = [
                (
                    "Số giá trị nguyên của tham số $m$ để $A \\cap B = \\varnothing$.",
                    z_ans,
                    f"Để $A \\cap B = \\varnothing$ thì hai tập hợp không có phần tử chung. "
                    f"Với $A = \\left[{a_val}; {b_val}\\right]$ và $B = \\left({n_val}; m\\right]$, để $B$ nằm hoàn toàn bên trái $A$ thì cần $m < {a_val}$. "
                    f"Mặt khác, để $B = \\left({n_val}; m\\right]$ là tập hợp khác rỗng thì cần $m > {n_val}$. "
                    f"Suy ra ${n_val} < m < {a_val}$. "
                    f"Vì $m \\in \\mathbb{{Z}}$ nên số giá trị nguyên của $m$ là ${a_val} - {n_val} - 1 = {z_ans}$."
                )
            ]

        # =========================
        # KIỂU 4: A ∩ B ≠ ∅
        # =========================
        else:
            debai = (
                f"Cho hai tập hợp $A = \\left[{a_val}; {b_val}\\right]$ và "
                f"$B = \\left({n_val}; m\\right]$, với $m \\in \\mathbb{{Z}}$. Tính:"
            )

            ds_abcd = [
                (
                    "Số giá trị nguyên của tham số $m$ để $A \\cap B \\ne \\varnothing$.",
                    z_ans,
                    f"Để $A \\cap B \\ne \\varnothing$ thì hai tập hợp phải có ít nhất một phần tử chung. "
                    f"Do ${n_val} < {a_val}$ theo cách chọn dữ liệu nên để $A = \\left[{a_val}; {b_val}\\right]$ và $B = \\left({n_val}; m\\right]$ có phần tử chung, chỉ cần $m \\ge {a_val}$. "
                    f"Khi đó phần tử ${a_val}$ thuộc cả $A$ và $B$, suy ra $A \\cap B \\ne \\varnothing$. "
                    f"Vì $m \\in \\mathbb{{Z}}$ và theo cách sinh dữ liệu ta có $m \\le 15$, nên "
                    f"$m \\in \\{{{a_val}, {a_val + 1}, \\ldots, 15\\}}$. "
                    f"Vậy số giá trị nguyên của $m$ là $15 - {a_val} + 1 = {z_ans}$."
                )
            ]

        cauTL += TL_answer_const(debai, ds_abcd, 0, 0, dong)

    return cauTL


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

        # Xác định cận thực tế của k dựa trên ký hiệu khoảng/đoạn
        # Cận dưới (k_lower): nếu là '[' thì k >= k_min_val, nếu '(' thì k >= k_min_val + 1
        k_lower = k_min_val if i_left == '[' else k_min_val + 1
        # Cận trên (k_upper): nếu là ']' thì k <= k_max_val, nếu ')' thì k <= k_max_val - 1
        k_upper = k_max_val if i_right == ']' else k_max_val - 1

        # Điều kiện cần để P(x) đúng với mọi x (dựa vào biến dau)
        if dau == r'\geq':
            # Cần k >= a^2
            # Giao của [k_lower, k_upper] và [a^2, +inf)
            start_k = max(k_lower, a ** 2)
            dapso_val = max(0, k_upper - start_k + 1) if start_k <= k_upper else 0

            giai = rf"Ta có $P(x): x^2 - {2 * a}x + k \geq 0 \Leftrightarrow (x-{a})^2 + k - {a ** 2} \geq 0$. Để đúng với mọi $x \in \mathbb{{R}}$, ta cần $k \geq {a ** 2}$. Kết hợp với $k \in {i_left}{k_min_val}; {k_max_val}{i_right}$, ta có $k \in [{start_k}; {k_upper}]$. Số giá trị nguyên $k$ là {dapso_val}."

        elif dau == '>':
            # Cần k > a^2 => k >= a^2 + 1
            start_k = max(k_lower, a ** 2 + 1)
            dapso_val = max(0, k_upper - start_k + 1) if start_k <= k_upper else 0

            giai = rf"Ta có $P(x): x^2 - {2 * a}x + k > 0 \Leftrightarrow (x-{a})^2 + k - {a ** 2} > 0$. Để đúng với mọi $x \in \mathbb{{R}}$, ta cần $k > {a ** 2}$, tức $k \geq {a ** 2 + 1}$. Kết hợp với $k \in {i_left}{k_min_val}; {k_max_val}{i_right}$, ta có $k \in [{start_k}; {k_upper}]$. Số giá trị nguyên $k$ là {dapso_val}."
        else:
            dapso_val = 0
            giai = rf"Ta có $P(n) = (n-{a})^2 + k - {a ** 2} {dau} 0$. Vì $(n-{a})^2 \geq 0$ nên biểu thức tiến tới $+\infty$. Không tồn tại $k$ để biểu thức luôn ${dau} 0$ với mọi $x$. Số giá trị là 0."

        dapso = str(dapso_val)
        debai = rf"Cho mệnh đề chứa biến $P(n): n^2 - {2 * a}n + k {dau} 0$ với $n \in \mathbb{{R}}$. Có tất cả bao nhiêu giá trị nguyên của tham số $k$ thuộc tập {i_left}{k_min_val}; {k_max_val}{i_right} để mệnh đề $P(n)$ đúng với mọi $n \in \mathbb{{R}}$?"

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

        # Xác định cận thực tế của k dựa trên ký hiệu khoảng/đoạn
        # Cận dưới (k_lower): nếu là '[' thì k >= k_min_val, nếu '(' thì k >= k_min_val + 1
        k_lower = k_min_val if i_left == '[' else k_min_val + 1
        # Cận trên (k_upper): nếu là ']' thì k <= k_max_val, nếu ')' thì k <= k_max_val - 1
        k_upper = k_max_val if i_right == ']' else k_max_val - 1

        # Điều kiện cần để P(x) đúng với mọi x (dựa vào biến dau)
        if dau == r'\geq':
            # Cần k >= a^2
            # Giao của [k_lower, k_upper] và [a^2, +inf)
            start_k = max(k_lower, a ** 2)
            dapso_val = max(0, k_upper - start_k + 1) if start_k <= k_upper else 0

            giai = rf"Ta có $P(x): x^2 - {2 * a}x + k \geq 0 \Leftrightarrow (x-{a})^2 + k - {a ** 2} \geq 0$. Để đúng với mọi $x \in \mathbb{{R}}$, ta cần $k \geq {a ** 2}$. Kết hợp với $k \in {i_left}{k_min_val}; {k_max_val}{i_right}$, ta có $k \in [{start_k}; {k_upper}]$. Số giá trị nguyên $k$ là {dapso_val}."

        elif dau == '>':
            # Cần k > a^2 => k >= a^2 + 1
            start_k = max(k_lower, a ** 2 + 1)
            dapso_val = max(0, k_upper - start_k + 1) if start_k <= k_upper else 0

            giai = rf"Ta có $P(x): x^2 - {2 * a}x + k > 0 \Leftrightarrow (x-{a})^2 + k - {a ** 2} > 0$. Để đúng với mọi $x \in \mathbb{{R}}$, ta cần $k > {a ** 2}$, tức $k \geq {a ** 2 + 1}$. Kết hợp với $k \in {i_left}{k_min_val}; {k_max_val}{i_right}$, ta có $k \in [{start_k}; {k_upper}]$. Số giá trị nguyên $k$ là {dapso_val}."
        else:
            dapso_val = 0
            giai = rf"Ta có $P(n) = (n-{a})^2 + k - {a ** 2} {dau} 0$. Vì $(n-{a})^2 \geq 0$ nên biểu thức tiến tới $+\infty$. Không tồn tại $k$ để biểu thức luôn ${dau} 0$ với mọi $x$. Số giá trị là 0."

        dapso = str(dapso_val)
        debai = rf"Cho mệnh đề chứa biến $P(n): n^2 - {2 * a}n + k {dau} 0$ với $n \in \mathbb{{R}}$. Có tất cả bao nhiêu giá trị nguyên của tham số $k$ thuộc tập {i_left}{k_min_val}; {k_max_val}{i_right} để mệnh đề $P(n)$ đúng với mọi $n \in \mathbb{{R}}$?"

        # FIX QUAN TRỌNG: Đảm bảo danh sách nhiễu luôn có 3 phần tử duy nhất
        # Sử dụng set để lọc trùng, sau đó đảm bảo đủ 3 phần tử bằng cách thêm giá trị dự phòng
        base_nhieu = [str(max(0, dapso_val + 1)), str(max(0, dapso_val - 1)), str(max(0, dapso_val + 2)), "0", "1", "5", "10"]
        dsnhieu = random.sample([x for x in list(set(base_nhieu)) if x != dapso], 3)

        cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


def L10_C1_B1_VD014_MC_A_02(socau, dang=1):
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

        giai = (
            f"Xét mệnh đề $P(x)\\colon x {dau_tex} x^{{{n}}}$.\n"
            f"- $P({a})$ là {'Đúng' if p1 else 'Sai'}.\n"
            f"- $P\\left({frac_str}\\right)$ là {'Đúng' if p2 else 'Sai'}.\n"
            f"- $\\forall x\\in \\mathbb{{N}}, P(x)$ là {'Đúng' if p3 else 'Sai'}.\n"
            f"- $\\exists x\\in \\mathbb{{N}}, \\overline{{P(x)}}$ là {'Đúng' if p4 else 'Sai'}.\n"
            f"Tổng cộng có $\\mathbf{{{so_menh_de_dung}}}$ mệnh đề đúng."
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

def L10_C1_B2_NB017_SA_C(socau, dang=2):

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
            f"Tìm giá trị nguyên của tham số $m$ để tập hợp "
            f"$\\left{trai}{a};m\\right{phai}$ "
            f"chứa đúng {so_luong} {ten}."
        )

        lo = a if trai == "[" else a + 1
        hi = m if phai == "]" else m - 1
        tap = list(range(lo, hi + 1)) if lo <= hi else []

        if loai == "duong":
            ds = [x for x in tap if x > 0]
        elif loai == "am":
            ds = [x for x in tap if x < 0]
        elif loai == "khong_am":
            ds = [x for x in tap if x >= 0]
        elif loai == "khong_duong":
            ds = [x for x in tap if x <= 0]
        else:
            ds = tap

        lietke = r"\varnothing" if len(ds) == 0 else "; ".join(str(x) for x in ds)

        giai = (
            f"Ta có\n"
            f"$$\\left{trai}{a};{m}\\right{phai}=\\{{{lietke}\\}}.$$\n"
            f"Trong khoảng trên có đúng {so_luong} {ten}. "
            f"Vậy $m={m}$."
        )

        dsnhieu = []
        while len(dsnhieu) < 3:
            nhieu = m + random.choice([-3, -2, -1, 1, 2, 3])
            if nhieu != m and nhieu not in dsnhieu:
                dsnhieu.append(nhieu)

        cauSA += MC_SA_answer_const(debai, m, dsnhieu, giai, 0, 0, dang)

    return cauSA

