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
        'The number 2025 is a perfect square',
        'A rhombus has two perpendicular diagonals',
        'The sum of two opposite angles of a cyclic quadrilateral is 180 degrees',
        'The number 1 is a prime',
        'A rectangle is a parallelogram with one right angle',
        'The number 0 is the smallest natural number',
        'Vietnam lies in the eastern part of the Indochina Peninsula',
        'The Red River is the longest river in the world',
        'The Dien Bien Phu victory took place in 1954',
        'King Quang Trung decisively defeated the Qing army in 1789',
        'Pure water freezes at 0 degrees Celsius',
        'The Sun is a planet in the Solar System',
        'Oxygen is the most abundant element in the atmosphere of the Earth',
    ]

    # Danh sách các câu không phải mệnh đề (câu hỏi, cảm thán, câu cầu khiến)
    ds_khongphai = [
        'Who is Colonel Pham Ngoc Thao?',
        'How many enemy aircraft did People\'s Armed Forces Hero Nguyen Van Bay shoot down?',
        'How many countries did Uncle Ho pass through during his 30-year journey abroad in search of a way to save the nation?',
        'Who loves children as much as Uncle Ho Chi Minh?',
        'Teeth and hair are the foundation of a person, are they not?',
        'In this life, one needs a kind heart!',
        'This math test is so easy!',
        'How old are you?',
        'Oh my, it is so hot!',
        'Please be quiet in the classroom!'
    ]

    gt = []
    dem = 0

    while dem < socau:
        # Chọn câu hỏi: 0 - Tìm mệnh đề, 1 - Tìm câu không phải mệnh đề
        loai = random.choice([0, 1])

        if loai == 0:
            dapso = random.choice(ds_menhde)
            dsnhieu = random.sample(ds_khongphai, 3)
            debai = r"Which of the following sentences is a statement?"
            giai = r"A statement is a declarative sentence that is either true or false. Questions, exclamations, and commands are not statements."
        else:
            dapso = random.choice(ds_khongphai)
            dsnhieu = random.sample(ds_menhde, 3)
            debai = r"Which of the following sentences is \textbf{not} a statement?"
            giai = r"A sentence that is not a statement is usually a question, an exclamation, or a command, whose truth value cannot be determined."

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
        'The number 2025 is a perfect square.',
        'A rhombus has two perpendicular diagonals.',
        'The sum of two opposite angles of a cyclic quadrilateral is 180 degrees.',
        'The number 1 is a prime.',
        'A rectangle is a parallelogram with one right angle.',
        'The number 0 is the smallest natural number.',
        'Vietnam lies in the eastern part of the Indochina Peninsula.',
        'The Red River is the longest river in the world.',
        'The Dien Bien Phu victory took place in 1954.',
        'King Quang Trung decisively defeated the Qing army in 1789.',
        'Pure water freezes at 0 degrees Celsius.',
        'The Sun is a planet in the Solar System.',
        'Oxygen is the most abundant element in the atmosphere of the Earth.',
    ]

    # Danh sách các câu không phải mệnh đề
    ds_khongphai = [
        'Who is Colonel Pham Ngoc Thao?',
        'How many enemy aircraft did People\'s Armed Forces Hero Nguyen Van Bay shoot down?',
        'How many countries did Uncle Ho pass through during his 30-year journey abroad in search of a way to save the nation?',
        'Who loves children as much as Uncle Ho Chi Minh?',
        'Teeth and hair are the foundation of a person, are they not?',
        'In this life, one needs a kind heart!',
        'This math test is so easy!',
        'How old are you?',
        'Oh my, it is so hot!',
        'Please be quiet in the classroom!'
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
                r"Among the following sentences, how many are statements?\\ "
                + noi_dung
            )

            giai = (
                r"A statement is a declarative sentence that is either true or false. Questions, exclamations, and commands are not statements."
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
                r"Among the following sentences, how many are \textbf{not} statements?\\ "
                + noi_dung
            )

            giai = (
                r"A sentence that is not a statement is usually a question, an exclamation, or a command, whose truth value cannot be determined."
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
        r'An equilateral triangle has three equal sides',
        r'The sum of the three angles in a triangle is $180^{\circ}$',
        r'A rectangle has four right angles',
        r'A square is a rectangle with four equal sides',
        r'Every even integer is divisible by $2$',
        r'The number $0$ is an integer',
        r'A diameter passes through the center of the circle',
        r'Two parallel lines have no common point',
        r'In a right triangle, the square of the hypotenuse equals the sum of the squares of the two legs',
        r'A rhombus has two perpendicular diagonals',
        r'Every prime greater than $2$ is odd',
        r'A parallelogram has opposite sides parallel',
        r'The number $25$ is a perfect square',
        r'The empty set is denoted by $\varnothing$',
        r'If a number is divisible by $10$, then it is divisible by $5$',
        r'A straight angle has a measure of $180^{\circ}$',
        r'Two vertical angles are equal',
        r'A disk has infinitely many lines of symmetry',
        r'Every square is a rhombus',
        r'An isosceles trapezoid is a trapezoid whose two legs are equal.',
        r'The number $\sqrt{16}$ equals $4$'
    ]

    # Danh sách các mệnh đề sai
    ds_sai = [
        r'The sum of the four interior angles of a square is $180^{\circ}$',
        r'A trapezoid with two equal legs is an isosceles trapezoid',
        r'Every integer is a prime',
        r'A triangle has four sides',
        r'Two parallel lines intersect',
        r'The number $9$ is a prime',
        r'A rectangle has four equal sides',
        r'Every even number is divisible by $3$',
        r'A right angle has a measure of $180^{\circ}$',
        r'A circle has three centers',
        r'The number $1$ is a prime',
        r'A trapezoid has two pairs of parallel sides',
        r'A right triangle has three right angles',
        r'The number $15$ is a perfect square',
        r'Two angles that form a linear pair are equal',
        r'Every parallelogram is a square',
        r'Every natural number is negative',
        r'The number $\sqrt{25}$ equals $10$',
        r'A diameter is shorter than a radius'
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
                r"Which of the following statements is true?"
            )

            giai = (
                r"The true statement is: " + dapso + "."
            )

        else:

            # Đáp án đúng là mệnh đề sai
            dapso = random.choice(ds_sai)

            # 3 đáp án nhiễu là mệnh đề đúng
            dsnhieu = random.sample(ds_dung, 3)

            debai = (
                r"Which of the following statements is \textbf{false}?"
            )

            giai = (
                r"The false statement is: " + dapso + "."
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
        r'An equilateral triangle has three equal sides.',
        r'The sum of the three angles in a triangle is $180^{\circ}$.',
        r'A rectangle has four right angles.',
        r'A square is a rectangle with four equal sides.',
        r'Every even integer is divisible by $2$.',
        r'The number $0$ is an integer.',
        r'A diameter passes through the center of the circle.',
        r'Two parallel lines have no common point.',
        r'In a right triangle, the square of the hypotenuse equals the sum of the squares of the two legs.',
        r'A rhombus has two perpendicular diagonals.',
        r'Every prime greater than $2$ is odd.',
        r'A parallelogram has opposite sides parallel.',
        r'The number $25$ is a perfect square.',
        r'The empty set is denoted by $\varnothing$.',
        r'If a number is divisible by $10$, then it is divisible by $5$.',
        r'A straight angle has a measure of $180^{\circ}$.',
        r'Two vertical angles are equal.',
        r'A disk has infinitely many lines of symmetry.',
        r'Every square is a rhombus.',
        r'An isosceles trapezoid is a trapezoid whose two legs are equal.',
        r'The number $\sqrt{16}$ equals $4$.'
    ]

    # Danh sách các mệnh đề sai
    ds_sai = [
        r'The sum of the four interior angles of a square is $180^{\circ}$.',
        r'A trapezoid with two equal legs is an isosceles trapezoid.',
        r'Every integer is a prime.',
        r'A triangle has four sides.',
        r'Two parallel lines intersect.',
        r'The number $9$ is a prime.',
        r'A rectangle has four equal sides.',
        r'Every even number is divisible by $3$.',
        r'A right angle has a measure of $180^{\circ}$.',
        r'A circle has three centers.',
        r'The number $1$ is a prime.',
        r'A trapezoid has two pairs of parallel sides.',
        r'A right triangle has three right angles.',
        r'The number $15$ is a perfect square.',
        r'Two angles that form a linear pair are equal.',
        r'Every parallelogram is a square.',
        r'Every natural number is negative.',
        r'The number $\sqrt{25}$ equals $10$.',
        r'In a circle, a diameter is shorter than a radius.'
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
                r"How many of the following statements are true?"
            )

            giai = (
                r"The number of true statements is " + str(dapso) + r"."
            )

        else:

            # Chọn các mệnh đề sai
            list_sai = random.sample(ds_sai, dapso)

            # Chọn các mệnh đề đúng
            list_dung = random.sample(ds_dung, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_sai + list_dung

            debai = (
                r"How many of the following statements are \textbf{false}?"
            )

            giai = (
                r"The number of false statements is " + str(dapso) + r"."
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
            luong_tu_text = "for all"
        else:
            luong_tu_tex = r"\exists x \in \mathbb{R}"
            luong_tu_text = "there exists"

        if loai_dau == 0:
            dau = ">"
            dap_an_dung_sai = "$True$"

            giai_dung_sai = (
                f"The converse is ``${luong_tu_tex}: x > {a_val} \\Rightarrow |x| > {a_val}$''. If $x>{a_val}$, then since ${a_val}>0$, we have $x>0$. It follows that $|x|=x>{a_val}$. Hence the converse is true."
            )

        elif loai_dau == 1:
            dau = r"\ge"

            dap_an_dung_sai = "$True$"

            giai_dung_sai = (
                f"The converse is ``${luong_tu_tex}: x \\ge {a_val} \\Rightarrow |x| \\ge {a_val}$''. If $x\\ge {a_val}$, then since ${a_val}>0$, we have $x\\ge0$. It follows that $|x|=x\\ge {a_val}$. Hence the converse is true."
            )

        elif loai_dau == 2:
            dau = "<"

            if loai_luong_tu == 0:

                dap_an_dung_sai = "$False$"

                phan_vi_du = -a_val - 1

                giai_dung_sai = (
                    f"The converse is ``$\\forall x \\in \\mathbb{{R}}: x < {a_val} \\Rightarrow |x| < {a_val}$''. This statement is false. Indeed, take $x={phan_vi_du}$. Then $x<{a_val}$ but $|x|={abs(phan_vi_du)}>{a_val}$. Hence the converse is false."
                )

            else:

                dap_an_dung_sai = "$True$"

                giai_dung_sai = (
                    f"The converse is ``$\\exists x \\in \\mathbb{{R}}: x < {a_val} \\Rightarrow |x| < {a_val}$''. Take $x=0$. Then $0<{a_val}$ and $|0|=0<{a_val}$. Hence there exists a real number that satisfies the statement, so the converse is true."
                )

        else:
            dau = r"\le"

            if loai_luong_tu == 0:

                dap_an_dung_sai = "$False$"

                phan_vi_du = -a_val - 1

                giai_dung_sai = (
                    f"The converse is ``$\\forall x \\in \\mathbb{{R}}: x \\le {a_val} \\Rightarrow |x| \\le {a_val}$''. This statement is false. Indeed, take $x={phan_vi_du}$. Then $x\\le {a_val}$ but $|x|={abs(phan_vi_du)}>{a_val}$. Hence the converse is false."
                )

            else:

                dap_an_dung_sai = "$True$"

                giai_dung_sai = (
                    f"The converse is ``$\\exists x \\in \\mathbb{{R}}: x \\le {a_val} \\Rightarrow |x| \\le {a_val}$''. Take $x=0$. Then $0\\le {a_val}$ and $|0|=0\\le {a_val}$. Hence there exists a real number that satisfies the statement, so the converse is true."
                )

        debai = (
            f"""Given the statement $P$: ``${luong_tu_tex}: |x| {dau} {a_val} \\Rightarrow x {dau} {a_val}$''."""
        )

        ds_abcd = [

            [
                "State the converse of the given statement.",
                f"${luong_tu_tex}: x {dau} {a_val} \\Rightarrow |x| {dau} {a_val}$",
                f"The converse of the statement $P$ is ``${luong_tu_tex}: x {dau} {a_val} \\Rightarrow |x| {dau} {a_val}$''."
            ],

            [
                "Determine whether the converse is true or false.",
                dap_an_dung_sai,
                giai_dung_sai
            ]

        ]

        cauTN += TL_answer_text(
            debai,
            _c1_ds_tl(ds_abcd),
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
                f"""Given the statement $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ge 0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}<0$"
            )

            ds_abcd = [

                [
                    "State the negation of the given statement.",
                    phu_dinh,
                    f"The negation of $P$ is: ``{phu_dinh}''."
                ],

                [
                    "Determine whether the negation is true or false.",
                    "$False$",
                    f"Since $n={n}$ is even, for all $x\\in\\mathbb{{R}}$ we always have $x^{n}\\ge0$. Therefore no real number satisfies $x^{n}<0$. Hence the negation is false."
                ]

            ]

        # =========================
        # ∀ x, x^n > 0
        # =========================
        elif loai == 1:

            n = v[1]

            debai = (
                f"""Given the statement $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}>0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}\\le 0$"
            )

            ds_abcd = [

                [
                    "State the negation of the given statement.",
                    phu_dinh,
                    f"The negation of $P$ is: ``{phu_dinh}''."
                ],

                [
                    "Determine whether the negation is true or false.",
                    "$True$",
                    f"Take $x=0$. Then $0^{n}=0\\le0$. Hence there exists a real number that satisfies the condition. Therefore the negation is true."
                ]

            ]

        # =========================
        # ∃ x, x^n = a (a > 0)
        # =========================
        elif loai == 2:

            n = v[1]
            a = v[2]

            debai = (
                f"""Given the statement $P:$ ``$\\exists x\\in\\mathbb{{R}},\\ x^{n}={a}$''. """
            )

            phu_dinh = (
                f"$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ne {a}$"
            )

            ds_abcd = [

                [
                    "State the negation of the given statement.",
                    phu_dinh,
                    f"The negation of $P$ is: ``{phu_dinh}''."
                ],

                [
                    "Determine whether the negation is true or false.",
                    "$False$",
                    f"We have that $x=\\sqrt[{n}]{{{a}}}$ is a real number and $x^{n}={a}$. Hence the original statement is true, so its negation is false."
                ]

            ]

        # =========================
        # ∃ x, x^n = a (a < 0)
        # =========================
        elif loai == 3:

            n = v[1]
            a = v[2]

            debai = (
                f"""Given the statement $P:$ ``$\\exists x\\in\\mathbb{{R}},\\ x^{n}={a}$''. """
            )

            phu_dinh = (
                f"$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ne {a}$"
            )

            ds_abcd = [

                [
                    "State the negation of the given statement.",
                    phu_dinh,
                    f"The negation of $P$ is: ``{phu_dinh}''."
                ],

                [
                    "Determine whether the negation is true or false.",
                    "$True$",
                    f"Since $n={n}$ is even, for every real number $x$ we have $x^{n}\\ge0$. It is impossible to have $x^{n}={a}$ with $a={a}<0$. Therefore the negation is true."
                ]

            ]

        # =========================
        # ∀ x, x^n ≥ 0 (n lẻ)
        # =========================
        elif loai == 4:

            n = v[1]

            debai = (
                f"""Given the statement $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\ge0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}<0$"
            )

            ds_abcd = [

                [
                    "State the negation of the given statement.",
                    phu_dinh,
                    f"The negation of $P$ is: ``{phu_dinh}''."
                ],

                [
                    "Determine whether the negation is true or false.",
                    "$True$",
                    f"Take $x=-1$. Then $(-1)^{n}=-1<0$. Hence there exists a real number that satisfies the condition. Therefore the negation is true."
                ]

            ]

        # =========================
        # ∀ x, x^n ≤ 0 (n lẻ)
        # =========================
        else:

            n = v[1]

            debai = (
                f"""Given the statement $P:$ ``$\\forall x\\in\\mathbb{{R}},\\ x^{n}\\le0$''. """
            )

            phu_dinh = (
                f"$\\exists x\\in\\mathbb{{R}},\\ x^{n}>0$"
            )

            ds_abcd = [

                [
                    "State the negation of the given statement.",
                    phu_dinh,
                    f"The negation of $P$ is: ``{phu_dinh}''."
                ],

                [
                    "Determine whether the negation is true or false.",
                    "$True$",
                    f"Take $x=1$. Then $1^{n}=1>0$. Hence there exists a real number that satisfies the condition. Therefore the negation is true."
                ]

            ]

        cauTN += TL_answer_text(
            debai,
            _c1_ds_tl(ds_abcd),
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
            c1_dung, c1_sai = 'a prime number', 'a composite number'
        else:
            c1_dung, c1_sai = 'a composite number', 'a prime number'

        if k % 2 == 0:
            c2_dung, c2_sai = 'an even number', 'an odd number'
        else:
            c2_dung, c2_sai = 'an odd number', 'an even number'

        tc = random.choice([c1_dung, c2_dung])

        dsnhieu = [f'${k}$ is {c1_sai}', f'${k}$ is {c2_sai}']
        thuoc_tinh_dung_con_lai = c2_dung if tc == c1_dung else c1_dung
        dsnhieu.append(f'${k}$ is not {thuoc_tinh_dung_con_lai}')

        dsnhieu = random.sample(dsnhieu, 3)

        da_dung_k.add(k)
        gt.append([k, tc, dsnhieu])
        dem += 1

    cauTN = ''
    for v in gt:
        k, tc, dsnhieu = v[0], v[1], v[2]

        dapso = f'${k}$ is not {tc}'
        debai = f"""Which of the following statements is the negation of the statement: ``${k}$ is {tc}''?"""
        giai = f"""The negation of a statement "$P$" is the statement "Not $P$". Hence the negation of the statement ``${k}$ is {tc}'' is ``${k}$ is not {tc}''."""

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
            'Lan is a 10th-grade student',
            'Lan is not a 10th-grade student',
            'Lan is a teacher',
            'Lan likes studying Math',
            'Lan does not like studying Math'
        ],

        [
            'Minh likes studying Math',
            'Minh does not like studying Math',
            'Minh likes studying Literature',
            'Minh is a top student',
            'Minh is not a student'
        ],

        [
            'Nam knows how to play the guitar',
            'Nam does not know how to play the guitar',
            'Nam knows how to play the piano',
            'Nam likes listening to music',
            'Nam does not like music'
        ],

        [
            'Ha is the captain of the soccer team',
            'Ha is not the captain of the soccer team',
            'Ha is a goalkeeper',
            'Ha likes playing soccer',
            'Ha is not on the soccer team'
        ],

        [
            'An goes to school by bicycle',
            'An does not go to school by bicycle',
            'An goes to school by bus',
            'An likes walking',
            'An does not go to school'
        ],

        [
            'Mai knows how to swim',
            'Mai does not know how to swim',
            'Mai likes going to the beach',
            'Mai plays badminton very well',
            'Mai does not like sports'
        ],

        [
            'Huy lives in Hanoi',
            'Huy does not live in Hanoi',
            'Huy lives in Da Nang',
            'Huy likes traveling',
            'Huy has never been to Hanoi'
        ],

        [
            'Vy likes eating ice cream',
            'Vy does not like eating ice cream',
            'Vy likes drinking milk tea',
            'Vy eats very few sweets',
            'Vy does not like desserts'
        ],

        [
            'Long can speak English',
            'Long cannot speak English',
            'Long can speak French',
            'Long likes studying foreign languages',
            'Long does not study English'
        ],

        [
            'Tram is good at Physics',
            'Tram is not good at Physics',
            'Tram is good at Chemistry',
            'Tram likes doing experiments',
            'Tram does not like studying'
        ],
        [
            'Class 10A is all girls',
            'Class 10A is not all girls',
            'Class 10A is all boys',
            'Class 10A has no boys',
            'Class 10A has both boys and girls'
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
            f"Which of the following is the negation of the statement: ``{md_goc}''?"
        )

        giai = (
            f'The negation of the statement "$P$" is the statement "Not $P$". Hence the negation of the statement ``{md_goc}\'\' is ``{dapso}\'\'.'
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
            f"""Which of the following is the negation of the statement:
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
            r"""Negating a statement that contains the symbol $\forall$ changes it to $\exists$, and vice versa,
and the property that follows is also negated."""
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
        r'If a number is divisible by $10$, then it is divisible by $5$',
        r'If a triangle is equilateral, then it has three equal sides',
        r'If a number is a prime greater than $2$, then it is odd',
        r'If a quadrilateral is a square, then it has four right angles',
        r'If a rectangle has four equal sides, then it is a square',
        r'If two angles are vertical angles, then they are equal',
        r'If a triangle is a right triangle, then the square of the hypotenuse equals the sum of the squares of the two legs',
        r'If a number is divisible by $6$, then it is divisible by $2$',
        r'If a number is divisible by $6$, then it is divisible by $3$',
        r'If a parallelogram has a right angle, then it is a rectangle',
        r'If a rhombus has a right angle, then it is a square',
        r'If a number is a multiple of $4$, then it is even',
        r'If a number ends in $0$, then it is divisible by $5$',
        r'If a triangle has three equal sides, then it is equilateral',
        r'If a number is a perfect square, then its square root is an integer',
        r'If two lines are both perpendicular to a third line, then they are parallel to each other',
        r'If a rectangle has two equal adjacent sides, then it is a square',
        r'If a number is divisible by $9$, then the sum of its digits is divisible by $9$',
        r'If an isosceles triangle has a right angle, then it is an isosceles right triangle',
        r'If a number is divisible by $2$ and $3$, then it is divisible by $6$'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    ds_khong_keotheo = [
        r'An equilateral triangle has three equal sides',
        r'A rectangle has four right angles',
        r'The number $25$ is a perfect square',
        r'Every prime greater than $2$ is odd',
        r'Two parallel lines have no common point',
        r'A square is a rectangle with four equal sides',
        r'The sum of the three angles in a triangle is $180^{\circ}$',
        r'A diameter passes through the center of the circle',
        r'A rhombus has two perpendicular diagonals',
        r'The empty set is denoted by $\varnothing$',
        r'A straight angle has a measure of $180^{\circ}$',
        r'A disk has infinitely many lines of symmetry',
        r'Every square is a rhombus',
        r'A parallelogram has opposite sides parallel',
        r'The number $0$ is an integer',
        r'Two vertical angles are equal',
        r'An isosceles trapezoid is a trapezoid with two equal legs',
        r'The number $\sqrt{16}$ equals $4$',
        r'In a right triangle, the square of the hypotenuse equals the sum of the squares of the two legs',
        r'Every even integer is divisible by $2$',

        r'A number is divisible by $2$ and divisible by $3$',
        r'A triangle is both isosceles and right',
        r'A figure is both a rectangle and a rhombus',
        r'A number is an integer or a rational number',
        r'A triangle is equilateral or isosceles',
        r'Two lines are parallel or intersecting',

        r'A number is divisible by $6$ if and only if it is divisible by $2$ and $3$',
        r'A quadrilateral is a square if and only if it is a rectangle with four equal sides',
        r'A triangle is equilateral if and only if it has three equal sides',
        r'A number is even if and only if it is divisible by $2$',
        r'A figure is a rectangle if and only if it has four right angles',
        r'Two triangles are congruent if and only if their corresponding sides are equal',
        r'A number is a perfect square if and only if its square root is an integer',
        r'Two lines are perpendicular if and only if the angle between them equals $90^{\circ}$.'
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
                r"Which of the following statements is a conditional statement?"
            )

            giai = (
                r"The conditional statement is: " + dapso
            )

        else:

            # Đáp án đúng là không phải kéo theo
            dapso = random.choice(ds_khong_keotheo)

            # 3 đáp án nhiễu là kéo theo
            dsnhieu = random.sample(ds_keotheo, 3)

            debai = (
                r"Which of the following statements is \textbf{not} a conditional statement?"
            )

            giai = (
                r"The statement that is not a conditional statement is: " + dapso
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
        r'If a number is divisible by $10$, then it is divisible by $5$.',
        r'If a triangle is equilateral, then it has three equal sides.',
        r'If a number is a prime greater than $2$, then it is odd.',
        r'If a quadrilateral is a square, then it has four right angles.',
        r'If a rectangle has four equal sides, then it is a square.',
        r'If two angles are vertical angles, then they are equal.',
        r'If a triangle is a right triangle, then the square of the hypotenuse equals the sum of the squares of the two legs.',
        r'If a number is divisible by $6$, then it is divisible by $2$.',
        r'If a number is divisible by $6$, then it is divisible by $3$.',
        r'If a parallelogram has a right angle, then it is a rectangle.',
        r'If a rhombus has a right angle, then it is a square.',
        r'If a number is a multiple of $4$, then it is even.',
        r'If a number ends in $0$, then it is divisible by $5$.',
        r'If a triangle has three equal sides, then it is equilateral.',
        r'If a number is a perfect square, then its square root is an integer.',
        r'If two lines are both perpendicular to a third line, then they are parallel to each other.',
        r'If a rectangle has two equal adjacent sides, then it is a square.',
        r'If a number is divisible by $9$, then the sum of its digits is divisible by $9$.',
        r'If an isosceles triangle has a right angle, then it is an isosceles right triangle.',
        r'If a number is divisible by $2$ and $3$, then it is divisible by $6$.'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    ds_khong_keotheo = [
        r'An equilateral triangle has three equal sides.',
        r'A rectangle has four right angles.',
        r'The number $25$ is a perfect square.',
        r'Every prime greater than $2$ is odd.',
        r'Two parallel lines have no common point.',
        r'A square is a rectangle with four equal sides.',
        r'The sum of the three angles in a triangle is $180^{\circ}$.',
        r'A diameter passes through the center of the circle.',
        r'A rhombus has two perpendicular diagonals.',
        r'The empty set is denoted by $\varnothing$.',
        r'A straight angle has a measure of $180^{\circ}$.',
        r'A disk has infinitely many lines of symmetry.',
        r'Every square is a rhombus.',
        r'A parallelogram has opposite sides parallel.',
        r'The number $0$ is an integer.',
        r'Two vertical angles are equal.',
        r'An isosceles trapezoid is a trapezoid whose two legs are equal.',
        r'The number $\sqrt{16}$ equals $4$.',
        r'In a right triangle, the square of the hypotenuse equals the sum of the squares of the two legs.',
        r'Every even integer is divisible by $2$.',

        r'A number is divisible by $2$ and divisible by $3$.',
        r'A triangle is both isosceles and right.',
        r'A figure is both a rectangle and a rhombus.',
        r'A number is an integer or a rational number.',
        r'A triangle is equilateral or isosceles.',
        r'Two lines are parallel or intersecting.',

        r'A number is divisible by $6$ if and only if it is divisible by $2$ and $3$.',
        r'A quadrilateral is a square if and only if it is a rectangle with four equal sides.',
        r'A triangle is equilateral if and only if it has three equal sides.',
        r'A number is even if and only if it is divisible by $2$.',
        r'A figure is a rectangle if and only if it has four right angles.',
        r'Two triangles are congruent if and only if their corresponding sides are equal.',
        r'A number is a perfect square if and only if its square root is an integer.',
        r'Two lines are perpendicular if and only if the angle between them equals $90^{\circ}$.'
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
                r"How many of the following statements are conditional statements?"
            )

            giai = (
                r"The number of conditional statements is " + str(dapso) + r"."
            )

        else:

            # Chọn mệnh đề không phải kéo theo
            list_khong = random.sample(ds_khong_keotheo, dapso)

            # Chọn mệnh đề kéo theo
            list_keotheo = random.sample(ds_keotheo, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_khong + list_keotheo

            debai = (
                r"How many of the following statements are \textbf{not} conditional statements?"
            )

            giai = (
                r"The number of statements that are not conditional statements is " + str(dapso) + r"."
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
        r'If a number is divisible by $10$, then it is divisible by $5$',
        r'If a number is divisible by $2$, then its last digit is even',
        r'If a number is a multiple of $3$, then the sum of its digits is divisible by $3$',
        r'If a triangle has three equal sides, then it is equilateral',
        r'If a rectangle has four equal sides, then it is a square',

        # Vật lí
        r'If water is heated to $100^{\circ}$C at normal pressure, then it boils',
        r'If current flows through a light bulb, then the bulb lights up',
        r'If the electric switch is turned off, then the light bulb goes out',
        r'If an object is pulled down, then the spring stretches',
        r'If friction decreases, then an object moves more easily',

        # Hóa học
        r'If iron metal is put into hydrochloric acid, then hydrogen gas is released',
        r'If litmus paper is put into an acid solution, then the paper turns red',
        r'If coal is burned in air, then carbon dioxide gas is produced',
        r'If table salt is dissolved in water, then a solution is obtained',
        r'If quicklime is added to water, then a chemical reaction occurs',

        # Sinh học
        r'If a plant is not watered for a long time, then it will wilt',
        r'If a person does not breathe, then they cannot live',
        r'If there is a lack of light, then green plants grow poorly',
        r'If a person eats too many sweets, then they are prone to tooth decay',
        r'If you wash your hands with soap, then it helps limit bacteria',

        # Địa lí
        r'If the temperature drops below $0^{\circ}$C, then water may freeze',
        r'If heavy rain lasts for a long time, then flooding is likely to occur',
        r'If headwater forests are cleared, then soil erosion is likely to occur',
        r'If a strong earthquake occurs under the seabed, then a tsunami may occur',

        # Tin học
        r'If the wrong password is entered, then you cannot log in to the account',
        r'If a computer suddenly loses power, then unsaved data may be lost',
        r'If the Internet connection is cut off, then web pages cannot be accessed',

        # Đời sống
        r'If you stay up late regularly, then your body tires easily',
        r'If you wear a helmet when riding a motorbike, then it helps reduce the risk of injury',
        r'If you study thoroughly, then your test results are usually better',
        r'If you exercise regularly, then your health improves'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    # Gồm mệnh đề đơn, tuyển, hội, tương đương

    ds_khong_keotheo = [

        # Mệnh đề đơn
        r'The Earth orbits the Sun',
        r'Seawater tastes salty',
        r'Air contains oxygen',
        r'A square has four equal sides',
        r'An equilateral triangle has three equal angles',
        r'People need water to live',
        r'Green plants produce oxygen',
        r'The Moon orbits the Earth',
        r'The number $25$ is a perfect square',
        r'The sum of the three angles in a triangle equals $180^{\circ}$',

        # Hội
        r'A number is divisible by $2$ and divisible by $5$',
        r'A triangle is both isosceles and right',
        r'A student is both academically strong and hardworking',
        r'A figure is both a rectangle and a rhombus',
        r'A substance is both a solid and a liquid',

        # Tuyển
        r'A number is an integer or a rational number',
        r'Today it is rainy or sunny',
        r'A student studies Math or studies English',
        r'A triangle is isosceles or equilateral',
        r'An object sinks or floats in water',

        # Mệnh đề tương đương
        r'A number is divisible by $10$ if and only if its last digit is $0$',
        r'A triangle is equilateral if and only if it has three equal sides',
        r'A number is even if and only if it is divisible by $2$',
        r'A figure is a square if and only if it is a rectangle with four equal sides',
        r'Water boils if and only if the temperature reaches $100^{\circ}$C at normal pressure',
        r'A student advances to the next grade if and only if the student meets all the assessment requirements',
        r'A substance conducts electricity if and only if it allows electric current to pass through',
        r'A linear equation has a unique solution if and only if the coefficient of $x$ is not $0$',

        r'A number is divisible by $6$ if and only if it is divisible by $2$ and $3$',
        r'A triangle is a right triangle if and only if the square of the hypotenuse equals the sum of the squares of the two legs',
        r'A number is a perfect square if and only if its square root is an integer',
        r'A quadrilateral is a rectangle if and only if it has four right angles',
        r'A trapezoid is an isosceles trapezoid if and only if its two legs are equal',
        r'Two vertical angles are equal if and only if they are vertical angles',
        r'A number is divisible by $9$ if and only if the sum of its digits is divisible by $9$',
        r'A triangle is isosceles if and only if it has two equal sides',
        r'An integer is even if and only if it leaves no remainder when divided by $2$',
        r'A fraction equals $0$ if and only if its numerator equals $0$ and its denominator is not $0$',

        r'A computer is connected to the Internet if and only if it can access web pages',
        r'A student is recognized as having completed a course if and only if the student meets the assessment requirements',
        r'A light bulb is lit if and only if current flows through it',
        r'A plant grows well if and only if it is supplied with enough water and light',
        r'An object floats on water if and only if its density is less than the density of water',
        r'A combustion reaction occurs if and only if oxygen is involved',
        r'A number is prime if and only if it has exactly two positive divisors',
        r'A triangle is isosceles at $A$ if and only if the two base angles are equal',
        r'A parallelogram is a rectangle if and only if it has a right angle',
        r'A parallelogram is a rhombus if and only if two adjacent sides are equal'
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
                r"Which of the following statements is a conditional statement?"
            )

            giai = (
                r"The conditional statement is: " + dapso + "."
            )

        else:

            # Đáp án đúng là không phải kéo theo
            dapso = random.choice(ds_khong_keotheo)

            # 3 đáp án nhiễu
            dsnhieu = random.sample(ds_keotheo, 3)

            debai = (
                r"Which of the following statements is \textbf{not} a conditional statement?"
            )

            giai = (
                r"The statement that is not a conditional statement is: " + dapso + "."
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
        r'If a number is divisible by $10$, then it is divisible by $5$.',
        r'If a number is divisible by $2$, then its last digit is even.',
        r'If a number is a multiple of $3$, then the sum of its digits is divisible by $3$.',
        r'If a triangle has three equal sides, then it is equilateral.',
        r'If a rectangle has four equal sides, then it is a square.',

        # Vật lí
        r'If water is heated to $100^{\circ}$C at normal pressure, then it boils.',
        r'If current flows through a light bulb, then the bulb lights up.',
        r'If the electric switch is turned off, then the light bulb goes out.',
        r'If an object is pulled down, then the spring stretches.',
        r'If friction decreases, then an object moves more easily.',

        # Hóa học
        r'If iron metal is put into hydrochloric acid, then hydrogen gas is released.',
        r'If litmus paper is put into an acid solution, then the paper turns red.',
        r'If coal is burned in air, then carbon dioxide gas is produced.',
        r'If table salt is dissolved in water, then a solution is obtained.',
        r'If quicklime is added to water, then a chemical reaction occurs.',

        # Sinh học
        r'If a plant is not watered for a long time, then it will wilt.',
        r'If a person does not breathe, then they cannot live.',
        r'If there is a lack of light, then green plants grow poorly.',
        r'If a person eats too many sweets, then they are prone to tooth decay.',
        r'If you wash your hands with soap, then it helps limit bacteria.',

        # Địa lí
        r'If the temperature drops below $0^{\circ}$C, then water may freeze.',
        r'If heavy rain lasts for a long time, then flooding is likely to occur.',
        r'If headwater forests are cleared, then soil erosion is likely to occur.',
        r'If a strong earthquake occurs under the seabed, then a tsunami may occur.',

        # Tin học
        r'If the wrong password is entered, then you cannot log in to the account.',
        r'If a computer suddenly loses power, then unsaved data may be lost.',
        r'If the Internet connection is cut off, then web pages cannot be accessed.',

        # Đời sống
        r'If you stay up late regularly, then your body tires easily.',
        r'If you wear a helmet when riding a motorbike, then it helps reduce the risk of injury.',
        r'If you study thoroughly, then your test results are usually better.',
        r'If you exercise regularly, then your health improves.'
    ]


    # Danh sách KHÔNG PHẢI mệnh đề kéo theo
    # Gồm mệnh đề đơn, tuyển, hội, tương đương

    ds_khong_keotheo = [

        # Mệnh đề đơn
        r'The Earth orbits the Sun.',
        r'Seawater tastes salty.',
        r'Air contains oxygen.',
        r'A square has four equal sides.',
        r'An equilateral triangle has three equal angles.',
        r'People need water to live.',
        r'Green plants produce oxygen.',
        r'The Moon orbits the Earth.',
        r'The number $25$ is a perfect square.',
        r'The sum of the three angles in a triangle equals $180^{\circ}$.',

        # Hội
        r'A number is divisible by $2$ and divisible by $5$.',
        r'A triangle is both isosceles and right.',
        r'A student is both academically strong and hardworking.',
        r'A figure is both a rectangle and a rhombus.',
        r'A substance is both a solid and a liquid.',

        # Tuyển
        r'A number is an integer or a rational number.',
        r'Today it is rainy or sunny.',
        r'A student studies Math or studies English.',
        r'A triangle is isosceles or equilateral.',
        r'An object sinks or floats in water.',

        # Mệnh đề tương đương
        r'A number is divisible by $10$ if and only if its last digit is $0$.',
        r'A triangle is equilateral if and only if it has three equal sides.',
        r'A number is even if and only if it is divisible by $2$.',
        r'A figure is a square if and only if it is a rectangle with four equal sides.',
        r'Water boils if and only if the temperature reaches $100^{\circ}$C at standard pressure.',
        r'A student is promoted to the next grade if and only if the student meets the evaluation requirements.',
        r'A substance conducts electricity if and only if it allows electric current to pass through.',
        r'A linear equation has a unique solution if and only if the coefficient of $x$ is not $0$.',

        r'A number is divisible by $6$ if and only if it is divisible by $2$ and $3$.',
        r'A triangle is a right triangle if and only if the square of the hypotenuse equals the sum of the squares of the two legs.',
        r'A number is a perfect square if and only if its square root is an integer.',
        r'A quadrilateral is a rectangle if and only if it has four right angles.',
        r'A trapezoid is an isosceles trapezoid if and only if its two legs are equal.',
        r'Two vertical angles are equal if and only if they are vertical angles.',
        r'A number is divisible by $9$ if and only if the sum of its digits is divisible by $9$.',
        r'A triangle is isosceles if and only if it has two equal sides.',
        r'An integer is even if and only if it leaves no remainder when divided by $2$.',
        r'A fraction equals $0$ if and only if its numerator equals $0$ and its denominator is not $0$.',

        r'A computer is connected to the Internet if and only if it can access web pages.',
        r'A student is recognized as having completed a course if and only if the student meets the evaluation requirements.',
        r'A light bulb shines if and only if an electric current flows through it.',
        r'A plant grows well if and only if it is given enough water and light.',
        r'An object floats on water if and only if its density is less than the density of water.',
        r'A combustion reaction occurs if and only if oxygen is involved.',
        r'A number is prime if and only if it has exactly two positive divisors.',
        r'A triangle is isosceles at $A$ if and only if its two base angles are equal.',
        r'A parallelogram is a rectangle if and only if it has one right angle.',
        r'A parallelogram is a rhombus if and only if two adjacent sides are equal.'
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
                r"How many of the following statements are conditional statements?"
            )

            giai = (
                r"The number of conditional statements is " + str(dapso) + r"."
            )

        else:

            # Chọn mệnh đề không phải kéo theo
            list_khong = random.sample(ds_khong_keotheo, dapso)

            # Chọn mệnh đề kéo theo
            list_keotheo = random.sample(ds_keotheo, 4 - dapso)

            # Gộp danh sách
            ds_cau = list_khong + list_keotheo

            debai = (
                r"How many of the following statements are \textbf{not} conditional statements?"
            )

            giai = (
                r"The number of statements that are not conditional statements is " + str(dapso) + r"."
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
            "$a$ is divisible by $10$",
            "$a$ is divisible by $5$",
            "$a$ is divisible by $10$",
            "$a$ is divisible by $5$"
        ),

        (
            "$a$ is divisible by $6$",
            "$a$ is divisible by $2$",
            "$a$ is divisible by $6$",
            "$a$ is divisible by $2$"
        ),

        (
            "$a$ is divisible by $6$",
            "$a$ is divisible by $3$",
            "$a$ is divisible by $6$",
            "$a$ is divisible by $3$"
        ),

        (
            "$a$ is a perfect square",
            "The square root of $a$ is an integer",
            "$a$ is a perfect square",
            "the square root of $a$ is an integer"
        ),

        (
            "$a$ is a prime greater than $2$",
            "$a$ is odd",
            "$a$ is a prime greater than $2$",
            "$a$ is odd"
        ),

        (
            "Triangle $ABC$ has three equal sides",
            "Triangle $ABC$ is equilateral",
            "triangle $ABC$ has three equal sides",
            "triangle $ABC$ is equilateral"
        ),

        (
            "Triangle $ABC$ is equilateral",
            "Triangle $ABC$ has three equal angles",
            "triangle $ABC$ is equilateral",
            "triangle $ABC$ has three equal angles"
        ),

        (
            "Triangle $ABC$ is a right triangle",
            "In triangle $ABC$, the square of the hypotenuse equals the sum of the squares of the two legs",
            "triangle $ABC$ is a right triangle",
            "in triangle $ABC$, the square of the hypotenuse equals the sum of the squares of the two legs"
        ),

        (
            "Rectangle $MNPQ$ has four equal sides",
            "Rectangle $MNPQ$ is a square",
            "rectangle $MNPQ$ has four equal sides",
            "rectangle $MNPQ$ is a square"
        ),

        (
            "Parallelogram $MNPQ$ has a right angle",
            "Parallelogram $MNPQ$ is a rectangle",
            "parallelogram $MNPQ$ has a right angle",
            "parallelogram $MNPQ$ is a rectangle"
        ),

        (
            "Rhombus $ABCD$ has a right angle",
            "Rhombus $ABCD$ is a square",
            "rhombus $ABCD$ has a right angle",
            "rhombus $ABCD$ is a square"
        ),

        (
            "Lines $a$ and $b$ are both perpendicular to line $c$",
            "Lines $a$ and $b$ are parallel to each other",
            "lines $a$ and $b$ are both perpendicular to line $c$",
            "lines $a$ and $b$ are parallel to each other"
        ),

        (
            "$a$ is a multiple of $4$",
            "$a$ is even",
            "$a$ is a multiple of $4$",
            "$a$ is even"
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

        debai = f"""Given the following two statements:\\\\
            $P \\colon$ ``{P_text}'';\\\\
            $Q \\colon$ ``{Q_text}''.\\\\
            State the conditional statement $P \\Rightarrow Q$."""

        dapso = f"""If {p_text}, then {q_text}"""

        dsnhieu = [
            f"""If {q_text}, then {p_text}""",
            f"""{P_text} if and only if {q_text}""",
            f"""If {p_text}, then it is not the case that {q_text}"""
        ]

        giai = f"""The conditional statement $P \\Rightarrow Q$ is stated in the form: ``If $P$, then $Q$''. Hence the correct answer is: ``If {p_text}, then {q_text}''."""

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
            "Metal rod A is heated to a high temperature",
            "The length of metal rod A increases",
            "metal rod A is heated to a high temperature",
            "the length of metal rod A increases"
        ),

        (
            "A light ray travels at an angle from air into water",
            "The light ray bends at the interface",
            "a light ray travels at an angle from air into water",
            "the light ray bends at the interface"
        ),

        (
            "An object is pulled downward",
            "The spring stretches",
            "an object is pulled downward",
            "the spring stretches"
        ),

        # Lịch sử
        (
            "The 1954 Geneva Accords were signed",
            "Peace was restored in North Vietnam",
            "The 1954 Geneva Accords were signed",
            "peace was restored in North Vietnam"
        ),

        # Kinh tế
        (
            "The global oil supply is sharply cut",
            "Fuel prices tend to rise",
            "the global oil supply is sharply cut",
            "fuel prices tend to rise"
        ),

        (
            "A country falls into hyperinflation",
            "The purchasing power of its currency drops sharply",
            "a country falls into hyperinflation",
            "the purchasing power of its currency drops sharply"
        ),

        # Đời sống
        (
            "A person exercises regularly",
            "Their health improves",
            "a person exercises regularly",
            "their health improves"
        ),

        (
            "Severe geopolitical tensions arise around the world",
            "Gold prices tend to rise rapidly in the short term",
            "severe geopolitical tensions arise around the world",
            "gold prices tend to rise rapidly in the short term"
        ),

        (
            "James Watt invented the steam engine in the 18th century",
            "The Industrial Revolution began in England",
            "James Watt invented the steam engine in the 18th century",
            "the Industrial Revolution began in England"
        ),

        (
            "The 1954 Geneva Accords on Indochina were signed",
            "Peace was restored in North Vietnam",
            "The 1954 Geneva Accords on Indochina were signed",
            "peace was restored in North Vietnam"
        ),

        (
            "Earth rotates on its axis from west to east",
            "The phenomenon of alternating day and night occurs on Earth",
            "Earth rotates on its axis from west to east",
            "the phenomenon of alternating day and night occurs on Earth"
        ),

        (
            "A metal rod is heated to a high temperature",
            "The length of that metal rod increases compared with its original length",
            "a metal rod is heated to a high temperature",
            "the length of that metal rod increases compared with its original length"
        ),

        (
            "A quantity of charcoal is completely burned in oxygen gas",
            "Carbon dioxide gas is produced by the chemical reaction",
            "a quantity of charcoal is completely burned in oxygen gas",
            "carbon dioxide gas is produced by the chemical reaction"
        ),

        (
            "The global oil supply is suddenly cut",
            "Domestic and international fuel prices all surge",
            "the global oil supply is suddenly cut",
            "domestic and international fuel prices all surge"
        ),

        (
            "A light ray travels at an angle from the air medium into water",
            "The light ray bends at the interface between the two media",
            "a light ray travels at an angle from the air medium into water",
            "the light ray bends at the interface between the two media"
        ),

        (
            "An alternating current flows through a wire coil",
            "A changing magnetic field forms around the coil",
            "an alternating current flows through a wire coil",
            "a changing magnetic field forms around the coil"
        ),

        (
            "A piece of limestone is dropped into hydrochloric acid solution",
            "Gas bubbles appear in the test tube",
            "a piece of limestone is dropped into hydrochloric acid solution",
            "gas bubbles appear in the test tube"
        ),

        (
            "Green plants carry out photosynthesis in sunlight",
            "Oxygen gas is released into the atmosphere",
            "green plants carry out photosynthesis in sunlight",
            "oxygen gas is released into the atmosphere"
        ),

        (
            "Earth's shadow falls on the Moon",
            "A lunar eclipse occurs for the observer",
            "Earth's shadow falls on the Moon",
            "a lunar eclipse occurs for the observer"
        ),

        (
            "Air containing water vapor is pushed upward and cooled",
            "Condensation forms clouds and rain occurs",
            "air containing water vapor is pushed upward and cooled",
            "condensation forms clouds and rain occurs"
        ),

        (
            "The Tran dynasty's army and people won a great victory at the Battle of Bach Dang in 1288",
            "The third Mongol-Yuan invasion completely collapsed",
            "the Tran dynasty's army and people won a great victory at the Battle of Bach Dang in 1288",
            "the third Mongol-Yuan invasion completely collapsed"
        ),

        (
            "Vietnam's Nguyen court signed the Treaty of Saigon in 1862",
            "Three eastern provinces of Cochinchina were ceded to the French colonists",
            "Vietnam's Nguyen court signed the Treaty of Saigon in 1862",
            "three eastern provinces of Cochinchina were ceded to the French colonists"
        ),

        (
            "The Russian October Revolution of 1917 succeeded",
            "The world's first socialist state was founded",
            "the Russian October Revolution of 1917 succeeded",
            "the world's first socialist state was founded"
        ),

        (
            "Demand for an export agricultural product rises sharply",
            "Traders step up purchasing, causing the price of that product to rise accordingly",
            "demand for an export agricultural product rises sharply",
            "traders step up purchasing, causing the price of that product to rise accordingly"
        ),

        (
            "A country falls into prolonged hyperinflation",
            "The consumer purchasing power of its national currency declines severely",
            "a country falls into prolonged hyperinflation",
            "the consumer purchasing power of its national currency declines severely"
        ),

        (
            "A river carries a large amount of alluvium to its mouth",
            "The delta at the river mouth gradually expands",
            "a river carries a large amount of alluvium to its mouth",
            "the delta at the river mouth gradually expands"
        ),

        (
            "A geological region experiences strong faulting deep underground",
            "Earthquakes and tremors propagate across the surface",
            "a geological region experiences strong faulting deep underground",
            "earthquakes and tremors propagate across the surface"
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

        debai = f"""Given the following two statements:\\\\
            $P \\colon$ ``{P_text}'';\\\\
            $Q \\colon$ ``{Q_text}''.\\\\
            State the conditional statement $P \\Rightarrow Q$."""

        dapso = f"""If {p_text}, then {q_text}"""

        dsnhieu = [
            f"""If {q_text}, then {p_text}""",
            f"""{P_text} if and only if {q_text}""",
            f"""If {p_text}, then it is not the case that {q_text}"""
        ]

        giai = f"""The conditional statement $P \\Rightarrow Q$ is stated in the form: ``If $P$, then $Q$''. Hence the correct answer is: ``If {p_text}, then {q_text}''."""

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
            "P": "angles $\\widehat{A}$ and $\\widehat{B}$ are supplementary",
            "P_hoa": "Angles $\\widehat{A}$ and $\\widehat{B}$ are supplementary",
            "Q": "the sum of angles $\\widehat{A}$ and $\\widehat{B}$ equals $180^{\\circ}$",
            "Q_hoa": "The sum of angles $\\widehat{A}$ and $\\widehat{B}$ equals $180^{\\circ}$",
            "dao": "If the sum of angles $\\widehat{A}$ and $\\widehat{B}$ equals $180^{\\circ}$, then angles $\\widehat{A}$ and $\\widehat{B}$ are supplementary"
        },

        # Góc phụ
        {
            "P": "angles $\\widehat{M}$ and $\\widehat{N}$ are complementary",
            "P_hoa": "Angles $\\widehat{M}$ and $\\widehat{N}$ are complementary",
            "Q": "the sum of angles $\\widehat{M}$ and $\\widehat{N}$ equals $90^{\\circ}$",
            "Q_hoa": "The sum of angles $\\widehat{M}$ and $\\widehat{N}$ equals $90^{\\circ}$",
            "dao": "If the sum of angles $\\widehat{M}$ and $\\widehat{N}$ equals $90^{\\circ}$, then angles $\\widehat{M}$ and $\\widehat{N}$ are complementary"
        },

        # Chia hết
        {
            "P": "$a$ is divisible by $10$",
            "P_hoa": "$a$ is divisible by $10$",
            "Q": "$a$ is divisible by $5$",
            "Q_hoa": "$a$ is divisible by $5$",
            "dao": "If $a$ is divisible by $5$, then $a$ is divisible by $10$"
        },

        {
            "P": "$a$ is divisible by $6$",
            "P_hoa": "$a$ is divisible by $6$",
            "Q": "$a$ is divisible by $3$",
            "Q_hoa": "$a$ is divisible by $3$",
            "dao": "If $a$ is divisible by $3$, then $a$ is divisible by $6$"
        },

        # Tam giác đều
        {
            "P": "a triangle is equilateral",
            "P_hoa": "A triangle is equilateral",
            "Q": "the triangle has three equal sides",
            "Q_hoa": "The triangle has three equal sides",
            "dao": "If a triangle has three equal sides, then the triangle is equilateral"
        },

        # Hình vuông
        {
            "P": "a figure is a square",
            "P_hoa": "A figure is a square",
            "Q": "the figure has four right angles",
            "Q_hoa": "The figure has four right angles",
            "dao": "If a figure has four right angles, then the figure is a square"
        },

        # Hình chữ nhật
        {
            "P": "a rectangle has four equal sides",
            "P_hoa": "A rectangle has four equal sides",
            "Q": "the figure is a square",
            "Q_hoa": "The figure is a square",
            "dao": "If a figure is a square, then the figure is a rectangle with four equal sides"
        },

        # Song song
        {
            "P": "two lines are both perpendicular to a third line",
            "P_hoa": "Two lines are both perpendicular to a third line",
            "Q": "the two lines are parallel to each other",
            "Q_hoa": "The two lines are parallel to each other",
            "dao": "If two lines are parallel to each other, then they are both perpendicular to a third line"
        },

        # Số nguyên tố
        {
            "P": "a number is a prime greater than $2$",
            "P_hoa": "A number is a prime greater than $2$",
            "Q": "the number is odd",
            "Q_hoa": "The number is odd",
            "dao": "If a number is odd, then the number is a prime greater than $2$"
        },

        # Số chính phương
        {
            "P": "a number is a perfect square",
            "P_hoa": "A number is a perfect square",
            "Q": "the square root of the number is an integer",
            "Q_hoa": "The square root of the number is an integer",
            "dao": "If the square root of a number is an integer, then the number is a perfect square"
        },

        # Parabol
        {
            "P": "the function has a coefficient $a > 0$",
            "P_hoa": "The function has a coefficient $a > 0$",
            "Q": "the graph of the function opens upward",
            "Q_hoa": "The graph of the function opens upward",
            "dao": "If the graph of the function opens upward, then the coefficient $a > 0$"
        },

        # Phương trình bậc nhất
        {
            "P": "the equation has the form $ax+b=0$ with $a \\ne 0$",
            "P_hoa": "The equation has the form $ax+b=0$ with $a \\ne 0$",
            "Q": "the equation has a unique solution",
            "Q_hoa": "The equation has a unique solution",
            "dao": "If an equation has a unique solution, then the equation has the form $ax+b=0$ with $a \\ne 0$"
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
            f"""State the converse of the statement ``If {P}, then {Q}''. """
        )

        giai = (
            r"The converse of the statement $P \Rightarrow Q$ is the statement $Q \Rightarrow P$."
        )

        dsnhieu = [

            f"If it is not the case that {P}, then it is not the case that {Q}",

            f"If {Q}, then it is not the case that {P}",

            f"{v['P_hoa']} if and only if {Q}"
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
        cap = r"the two angles $\widehat{%s}$ and $\widehat{%s}$" % (goc1, goc2)
        if loai_tinh_chat == 0:
            dung_goc, sai_goc, k_dung, k_sai = "form a pair of complementary angles", "form a pair of supplementary angles", 90, 180
        else:
            dung_goc, sai_goc, k_dung, k_sai = "form a pair of supplementary angles", "form a pair of complementary angles", 180, 90
        khong_goc = "do not " + dung_goc

        def tc_ten(tc):            # P goi ten: "hai goc M va N phu nhau"
            return "%s %s" % (cap, tc)

        def tc_tro(tc):            # P noi lai: "hai goc do phu nhau"
            return "those two angles %s" % tc

        def tong_ten(dk):          # Q goi ten: "tong so do cua hai goc M va N bang 90"
            return "the sum of the measures of %s %s" % (cap, dk)

        def tong_tro(dk):          # Q noi lai: "tong so do cua chung bang 90"
            return "the sum of their measures %s" % dk

        bang = r"is equal to $%d^\circ$" % k_dung
        khac = r"is not equal to $%d^\circ$" % k_dung
        bang_sai = r"is equal to $%d^\circ$" % k_sai

        # Menh de goc P => Q: P dung sau "Neu" nen P goi ten.
        P_text, Q_text = tc_ten(dung_goc), tong_tro(bang)
        debai = f"""State the converse of the statement: ``If {P_text}, then {Q_text}''."""

        # Menh de dao Q => P: bay gio Q dung sau "Neu" nen Q goi ten.
        dapso = f"""If {tong_ten(bang)}, then {tc_tro(dung_goc)}."""

        # Phuong an nhieu - cung quy tac goi ten nhu vay.
        dsnhieu = [
            f"""If {tc_ten(khong_goc)}, then {tong_tro(khac)}.""",     # phu dinh
            f"""If {tong_ten(khac)}, then {tc_tro(khong_goc)}.""",     # phan dao
            f"""If {tong_ten(bang_sai)}, then {tc_tro(sai_goc)}.""",   # nham tinh chat
        ]

        giai = f"""Consider the given conditional statement, which has the form ``If $P$, then $Q$'' (written $P \\Rightarrow Q$), where:\\\\
        - $P$: ``{tc_ten(dung_goc)}''\\\\
        - $Q$: ``{tong_ten(bang)}''\\\\
        By definition, the converse of the statement $P \\Rightarrow Q$ is the statement $Q \\Rightarrow P$, stated in the form: ``If $Q$, then $P$''.\\\\
        Hence, the converse of the above statement is: ``{dapso[:-1]}''. """

        cauTN += _MC_khong_cham(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B1_NB011_MC_A_01(socau, dang=1):

    ds_boi_canh = [

        # ================= TOÁN - SỐ HỌC =================

        {
            "P": "the natural number $n$ is divisible by $2$",
            "P_hoa": "The natural number $n$ is divisible by $2$",
            "Q": "the natural number $n$ has an even units digit",
            "Q_hoa": "The natural number $n$ has an even units digit"
        },

        {
            "P": "the natural number $n$ is divisible by $3$",
            "P_hoa": "The natural number $n$ is divisible by $3$",
            "Q": "the sum of the digits of $n$ is divisible by $3$",
            "Q_hoa": "The sum of the digits of $n$ is divisible by $3$"
        },

        {
            "P": "the natural number $n$ is divisible by $5$",
            "P_hoa": "The natural number $n$ is divisible by $5$",
            "Q": "the natural number $n$ has a units digit of $0$ or $5$",
            "Q_hoa": "The natural number $n$ has a units digit of $0$ or $5$"
        },

        {
            "P": "the natural number $n$ is divisible by $10$",
            "P_hoa": "The natural number $n$ is divisible by $10$",
            "Q": "the natural number $n$ has a units digit of $0$",
            "Q_hoa": "The natural number $n$ has a units digit of $0$"
        },

        # ================= TOÁN - TAM GIÁC =================

        {
            "P": "triangle $ABC$ is a right triangle",
            "P_hoa": "Triangle $ABC$ is a right triangle",
            "Q": "triangle $ABC$ has one angle equal to $90^{\\circ}$",
            "Q_hoa": "Triangle $ABC$ has one angle equal to $90^{\\circ}$"
        },

        {
            "P": "triangle $ABC$ is an isosceles triangle",
            "P_hoa": "Triangle $ABC$ is an isosceles triangle",
            "Q": "triangle $ABC$ has two equal sides",
            "Q_hoa": "Triangle $ABC$ has two equal sides"
        },

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",
            "Q": "triangle $ABC$ has three equal sides",
            "Q_hoa": "Triangle $ABC$ has three equal sides"
        },

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",
            "Q": "triangle $ABC$ has three angles equal to $60^{\\circ}$",
            "Q_hoa": "Triangle $ABC$ has three angles equal to $60^{\\circ}$"
        },

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",
            "Q": "triangle $ABC$ is an isosceles triangle",
            "Q_hoa": "Triangle $ABC$ is an isosceles triangle"
        },

        # ================= TOÁN - TỨ GIÁC =================

        {
            "P": "quadrilateral $ABCD$ is an isosceles trapezoid",
            "P_hoa": "Quadrilateral $ABCD$ is an isosceles trapezoid",
            "Q": "quadrilateral $ABCD$ is a trapezoid with two equal legs",
            "Q_hoa": "Quadrilateral $ABCD$ is a trapezoid with two equal legs"
        },

        {
            "P": "quadrilateral $ABCD$ is a trapezoid",
            "P_hoa": "Quadrilateral $ABCD$ is a trapezoid",
            "Q": "quadrilateral $ABCD$ has one pair of parallel opposite sides",
            "Q_hoa": "Quadrilateral $ABCD$ has one pair of parallel opposite sides"
        },

        {
            "P": "quadrilateral $ABCD$ has two opposite sides that are parallel",
            "P_hoa": "Quadrilateral $ABCD$ has two opposite sides that are parallel",
            "Q": "quadrilateral $ABCD$ is a trapezoid",
            "Q_hoa": "Quadrilateral $ABCD$ is a trapezoid"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",
            "Q": "quadrilateral $ABCD$ is a rectangle with two equal adjacent sides",
            "Q_hoa": "Quadrilateral $ABCD$ is a rectangle with two equal adjacent sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",
            "Q": "quadrilateral $ABCD$ is a rhombus with one right angle",
            "Q_hoa": "Quadrilateral $ABCD$ is a rhombus with one right angle"
        },

        {
            "P": "quadrilateral $ABCD$ is a trapezoid",
            "P_hoa": "Quadrilateral $ABCD$ is a trapezoid",
            "Q": "quadrilateral $ABCD$ has one pair of parallel opposite sides",
            "Q_hoa": "Quadrilateral $ABCD$ has one pair of parallel opposite sides"
        },

        # ================= KHÁC =================

        {
            "P": "$a$ is a perfect square",
            "P_hoa": "$a$ is a perfect square",
            "Q": "the square root of the number $a$ is an integer",
            "Q_hoa": "The square root of the number $a$ is an integer"
        },

        # ================= THỰC TẾ =================

        {
            "P": "student $A$ is rated a high-achieving student",
            "P_hoa": "Student $A$ is rated a high-achieving student",
            "Q": "the average score of student $A$ is $8{,}0$ or higher",
            "Q_hoa": "The average score of student $A$ is $8{,}0$ or higher"
        },

        {
            "P": "water reaches a temperature of $100^{\\circ}$C at standard pressure",
            "P_hoa": "Water reaches a temperature of $100^{\\circ}$C at standard pressure",
            "Q": "water begins to boil",
            "Q_hoa": "Water begins to boil"
        },

        {
            "P": "Nam has reached the age of $18$",
            "P_hoa": "Nam has reached the age of $18$",
            "Q": "Nam has reached the legal age required of a citizen",
            "Q_hoa": "Nam has reached the legal age required of a citizen"
        },

        {
            "P": "the metal rod $AB$ is heated",
            "P_hoa": "The metal rod $AB$ is heated",
            "Q": "the metal rod $AB$ expands",
            "Q_hoa": "The metal rod $AB$ expands"
        },

        {
            "P": "student $B$ seriously violates the school rules",
            "P_hoa": "Student $B$ seriously violates the school rules",
            "Q": "student $B$ is disciplined",
            "Q_hoa": "Student $B$ is disciplined"
        },

        {
            "P": "the phone number $x$ receives too many advertising calls",
            "P_hoa": "The phone number $x$ receives too many advertising calls",
            "Q": "users tend to block the phone number $x$",
            "Q_hoa": "Users tend to block the phone number $x$"
        },

        {
            "P": "there are many dark clouds and the air humidity is high",
            "P_hoa": "There are many dark clouds and the air humidity is high",
            "Q": "there is a chance of heavy rain",
            "Q_hoa": "There is a chance of heavy rain"
        },

        {
            "P": "green plants carry out photosynthesis",
            "P_hoa": "Green plants carry out photosynthesis",
            "Q": "oxygen gas is released",
            "Q_hoa": "Oxygen gas is released"
        },

        {
            "P": "country $X$ experiences high inflation",
            "P_hoa": "Country $X$ experiences high inflation",
            "Q": "the prices of goods in country $X$ rise rapidly",
            "Q_hoa": "The prices of goods in country $X$ rise rapidly"
        },

        {
            "P": "Nam exercises regularly",
            "P_hoa": "Nam exercises regularly",
            "Q": "Nam's health improves",
            "Q_hoa": "Nam's health improves"
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
            f"""Given the following two statements:\\\\
            $P \\colon$ ``{P_hoa}'';\\\\
            $Q \\colon$ ``{Q_hoa}''.\\\\
            State the biconditional statement $P \\Leftrightarrow Q$."""
        )

        dapso = random.choice([
            f"{P_hoa} if and only if {Q}",
            f"{P_hoa} exactly when {Q}",
            f"{Q_hoa} if and only if {P}",
            f"{Q_hoa} exactly when {P}"
        ])

        dsnhieu = [

            f"If {P}, then {Q}",

            f"If {Q}, then {P}",

            f"Because {P}, {Q}"
        ]

        giai = (
            r"The biconditional statement $P \Leftrightarrow Q$ is stated in the form ``$P$ if and only if $Q$''."
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
            return "greater than"

        elif dau == "<":
            return "less than"

        elif dau == r"\geq":
            return "greater than or equal to"

        elif dau == r"\leq":
            return "less than or equal to"

        elif dau == "=":
            return "equal to"

        elif dau == r"\ne":
            return "different from"


    def doi_thuoc(dau):

        if dau == r"\in":
            return r"\notin"

        elif dau == r"\notin":
            return r"\in"


    def doc_thuoc(dau):

        if dau == r"\in":
            return "belongs to"

        elif dau == r"\notin":
            return "does not belong to"


    ds_boi_canh = []

    # =========================================================
    # DẠNG 1
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall x\in \mathbb{{R}}, x^2 {dau} 0$',

            "dung": rf'Every real number has a square {doc_dau(dau)} $0$',

            "nhieu": [

                rf'There exists a real number whose square is {doc_dau(dau)} $0$',

                rf'Every real number has a square {doc_dau(doi_dau(dau))} $0$',

                rf'There exists a real number whose square is {doc_dau(doi_dau(dau))} $0$',

                rf'There is at least one real number whose square is {doc_dau(dau)} $0$',

                rf'Every real number has a square different from $0$'
            ]
        })

    # =========================================================
    # DẠNG 2
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall n\in \mathbb{{N}}, n^2 {dau} n$',

            "dung": rf'Every natural number has a square {doc_dau(dau)} itself',

            "nhieu": [

                rf'There exists a natural number whose square is {doc_dau(dau)} itself',

                rf'Every natural number has a square {doc_dau(doi_dau(dau))} itself',

                rf'There exists a natural number whose square is {doc_dau(doi_dau(dau))} itself',

                rf'There is at least one natural number whose square is {doc_dau(dau)} itself',

                rf'Every natural number has a square equal to itself'
            ]
        })

    # =========================================================
    # DẠNG 3
    # =========================================================

    for dau in ["=", r"\ne"]:

        ds_boi_canh.append({

            "latex": rf'$\exists x\in \mathbb{{R}}, \dfrac{{1}}{{x}} {dau} x$',

            "dung": rf'There exists a real number whose reciprocal is {doc_dau(dau)} itself',

            "nhieu": [

                rf'Every real number has a reciprocal {doc_dau(dau)} itself',

                rf'There exists a real number whose reciprocal is {doc_dau(doi_dau(dau))} itself',

                rf'Every real number has a reciprocal {doc_dau(doi_dau(dau))} itself',

                rf'There is at least one real number whose reciprocal is {doc_dau(dau)} itself',

                rf'Every real number is equal to its own reciprocal'
            ]
        })

    # =========================================================
    # DẠNG 4
    # =========================================================

    for dau in [r"\in", r"\notin"]:

        ds_boi_canh.append({

            "latex": rf'$\exists n\in \mathbb{{N}}, \dfrac{{1}}{{n}} {dau} \mathbb{{N}}$',

            "dung": rf'There exists a natural number whose reciprocal {doc_thuoc(dau)} the set of natural numbers',

            "nhieu": [

                rf'Every natural number has a reciprocal that {doc_thuoc(dau)} the set of natural numbers',

                rf'There exists a natural number whose reciprocal {doc_thuoc(doi_thuoc(dau))} the set of natural numbers',

                rf'Every natural number has a reciprocal that {doc_thuoc(doi_thuoc(dau))} the set of natural numbers',

                rf'There is at least one natural number whose reciprocal {doc_thuoc(dau)} the set of natural numbers',

                rf'The reciprocal of every natural number is a natural number'
            ]
        })

    # =========================================================
    # DẠNG 5
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\forall x\in \mathbb{{R}}, |x| {dau} 0$',

            "dung": rf'Every real number has an absolute value {doc_dau(dau)} $0$',

            "nhieu": [

                rf'There exists a real number whose absolute value is {doc_dau(dau)} $0$',

                rf'Every real number has an absolute value {doc_dau(doi_dau(dau))} $0$',

                rf'There exists a real number whose absolute value is {doc_dau(doi_dau(dau))} $0$',

                rf'There is at least one real number whose absolute value is {doc_dau(dau)} $0$',

                rf'Every real number has an absolute value different from $0$'
            ]
        })

    # =========================================================
    # DẠNG 6
    # =========================================================

    for dau in [">", "<", r"\geq", r"\leq"]:

        ds_boi_canh.append({

            "latex": rf'$\exists x\in \mathbb{{Z}}, x^2 {dau} 0$',

            "dung": rf'There exists an integer whose square is {doc_dau(dau)} $0$',

            "nhieu": [

                rf'Every integer has a square {doc_dau(dau)} $0$',

                rf'There exists an integer whose square is {doc_dau(doi_dau(dau))} $0$',

                rf'Every integer has a square {doc_dau(doi_dau(dau))} $0$',

                rf'There is at least one integer whose square is {doc_dau(dau)} $0$',

                rf'Every integer has a square different from $0$'
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
            f"""Express the following statement in words:
``{P}''."""
        )

        giai = (
            r"""The symbol $\forall$ is read as "for all",
the symbol $\exists$ is read as "there exists"."""
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
            return "greater than"

        elif dau == "<":
            return "less than"

        elif dau == r"\geq":
            return "greater than or equal to"

        elif dau == r"\leq":
            return "less than or equal to"


    def sp_dau_text(dau):

        if dau == "=":
            return "equal to"

        elif dau == r"\ne":
            return "different from"


    def dao_thuoc(dau):

        if dau == r"\in":
            return r"\notin"

        elif dau == r"\notin":
            return r"\in"


    def sp_thuoc(dau):

        if dau == r"\in":
            return "belongs to"

        elif dau == r"\notin":
            return "does not belong to"

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

            "loi": rf'Every real number has a square {sp_dau(dau)} $0$',

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

            "loi": rf'Every natural number has a square {sp_dau(dau)} itself',

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

            "loi": rf'There exists a real number whose reciprocal is {sp_dau_text(dau)} itself',

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

            "loi": rf'There exists a natural number whose reciprocal {sp_thuoc(dau)} the set of natural numbers',

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

            "loi": rf'Every real number has an absolute value {sp_dau(dau)} $0$',

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

            "loi": rf'There exists an integer whose square is {sp_dau(dau)} $0$',

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
            f"""Choose the correct symbolic form of the statement:
``{v["loi"]}''."""
        )

        giai = (
            r"""The symbol $\forall$ is read as "for all", the symbol $\exists$ is read as "there exists"."""
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
    _SO_NHOM = "c1_th014_mc_a"

    import random

    gt = []
    dem = 0

    while dem < socau:

        # 01/10/2026: nhóm lấy xoay vòng - nhóm đã ra thì chỉ ra lại khi đã ra hết các nhóm
        nhom = _c1_uu_tien(_SO_NHOM, 17)[0] + 1
        _c1_danh_dau(_SO_NHOM, [nhom - 1])

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
            dapso = r"$\exists p\in\mathbb N,\ p\ \text{prime and even}$"
            dsnhieu = [
                r"$\nexists p\in\mathbb N,\ p\ \text{prime and even}$",
                r"$\forall p\in\mathbb N,\ p\ \text{prime}\Rightarrow p\ \text{even}$",
                r"$\forall p\in\mathbb N,\ p\ \text{prime}\Rightarrow p\ \text{odd}$"
            ]

        elif nhom == 7:
            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{even}\Rightarrow n^2\ \text{even}$"
            dsnhieu = [
                r"$\forall n\in\mathbb Z,\ n\ \text{even}\Rightarrow n^2\ \text{odd}$",
                r"$\exists n\in\mathbb Z,\ n\ \text{even and }n^2\ \text{odd}$",
                r"$\forall n\in\mathbb Z,\ n^2\ \text{even}\Rightarrow n\ \text{odd}$"
            ]

        elif nhom == 8:
            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{odd}\Rightarrow n^2\ \text{odd}$"
            dsnhieu = [
                r"$\forall n\in\mathbb Z,\ n\ \text{odd}\Rightarrow n^2\ \text{even}$",
                r"$\exists n\in\mathbb Z,\ n\ \text{odd and }n^2\ \text{even}$",
                r"$\forall n\in\mathbb Z,\ n^2\ \text{odd}\Rightarrow n\ \text{even}$"
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
            dapso = r"$\exists n\in\mathbb N,\ n\ \text{even}$"
            dsnhieu = [r"$\forall n\in\mathbb N,\ n\ \text{even}$", r"$\nexists n\in\mathbb N,\ n\ \text{even}$", r"$\forall n\in\mathbb N,\ n\ \text{odd}$"]

        elif nhom == 16:
            dapso = r"$\exists n\in\mathbb N,\ n\ \text{odd}$"
            dsnhieu = [r"$\forall n\in\mathbb N,\ n\ \text{odd}$", r"$\nexists n\in\mathbb N,\ n\ \text{odd}$", r"$\forall n\in\mathbb N,\ n\ \text{even}$"]

        else:
            a = random.randint(101,500)
            dapso = rf"$\exists n\in\mathbb Z,\ n>{a}$"
            dsnhieu = [rf"$\forall n\in\mathbb Z,\ n>{a}$", rf"$\nexists n\in\mathbb Z,\ n>{a}$", rf"$\forall n\in\mathbb Z,\ n<{a}$"]

        khoa = dapso

        if khoa not in [u["dapso"] for u in gt]:
            gt.append({"dapso": dapso, "dsnhieu": dsnhieu, "ly": _c1_ly_th014_dung(nhom, locals())})
            dem += 1

    cauTN = ""

    for v in gt:

        debai = "Which of the following statements is true?"
        giai = v["ly"]

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
    _SO_NHOM = "c1_th014_mc_b"

    gt = []
    dem = 0

    while dem < socau:

        # 01/10/2026: nhóm lấy xoay vòng - nhóm đã ra thì chỉ ra lại khi đã ra hết các nhóm
        nhom = _c1_uu_tien(_SO_NHOM, 17)[0] + 1
        _c1_danh_dau(_SO_NHOM, [nhom - 1])

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

            dapso = r"$\forall p\in\mathbb N,\ p\ \text{prime}\Rightarrow p\ \text{even}$"

            dsnhieu = [
                r"$\exists p\in\mathbb N,\ p\ \text{prime and even}$",
                r"$2\ \text{is prime}$",
                r"$3\ \text{is prime}$"
            ]

        elif nhom == 6:

            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{even}\Rightarrow n^2\ \text{odd}$"

            dsnhieu = [

                r"$\forall n\in\mathbb Z,\ n\ \text{even}\Rightarrow n^2\ \text{even}$",

                r"$4^2\ \text{is even}$",

                r"$2^2\ \text{is even}$"

            ]

        elif nhom == 7:

            dapso = r"$\forall n\in\mathbb Z,\ n\ \text{odd}\Rightarrow n^2\ \text{even}$"

            dsnhieu = [

                r"$\forall n\in\mathbb Z,\ n\ \text{odd}\Rightarrow n^2\ \text{odd}$",

                r"$3^2\ \text{is odd}$",

                r"$5^2\ \text{is odd}$"

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

            dapso = r"$\forall n\in\mathbb N,\ n\ \text{even}$"

            dsnhieu = [
                r"$\exists n\in\mathbb N,\ n\ \text{even}$",
                r"$2\ \text{is even}$",
                r"$4\ \text{is even}$"
            ]

        elif nhom == 15:

            dapso = r"$\forall n\in\mathbb N,\ n\ \text{odd}$"

            dsnhieu = [
                r"$\exists n\in\mathbb N,\ n\ \text{odd}$",
                r"$1\ \text{is odd}$",
                r"$3\ \text{is odd}$"
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
            gt.append({"dapso": dapso, "dsnhieu": dsnhieu, "ly": _c1_ly_th014_sai(nhom, locals())})
            dem += 1

    cauTN = ""

    for v in gt:

        debai = "Which of the following statements is \\textbf{false}?"
        giai = v["ly"]

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

        debai = r"""Let $n \in \mathbb{N}$."""

        # =====================================================
        # NHÓM A
        # =====================================================

        list_A = [

            (

                r"""{\True The statement ``$n$ is a nonnegative number'' is a true statement}""",

                r"""True. $\mathbb{N} = \{0;1;2;\ldots\}$, so every $n \in \mathbb{N}$ satisfies $n \geq 0$."""
            ),

            (

                r"""{The statement ``$n$ is a positive number'' is a true statement}""",

                r"""False. At $n = 0$: the number $0$ is a natural number but not a positive number."""
            ),

            (

                r"""{The statement ``$n$ is a negative number'' is a true statement}""",

                r"""False. No natural number takes a negative value."""
            ),

            (

                r"""{The statement ``$n$ is a nonpositive number'' is a true statement}""",

                r"""False. Only $n = 0$ is nonpositive; every $n \geq 1$ is positive."""
            ),

            ####################

            (

                r"""{The statement ``$n$ is a nonnegative number'' is a false statement}""",

                r"""False. $\mathbb{N} = \{0;1;2;\ldots\}$, so every $n \in \mathbb{N}$ satisfies $n \geq 0$."""
            ),

            (

                r"""{\True The statement ``$n$ is a positive number'' is a false statement}""",

                r"""True. At $n = 0$: the number $0$ is a natural number but not a positive number."""
            ),

            (

                r"""{\True The statement ``$n$ is a negative number'' is a false statement}""",

                r"""True. No natural number takes a negative value."""
            ),

            (

                r"""{\True The statement ``$n$ is a nonpositive number'' is a false statement}""",

                r"""True. Only $n = 0$ is nonpositive; every $n \geq 1$ is positive."""
            )
        ]

        # =====================================================
        # NHÓM B
        # =====================================================

        if huong_tich == 1:

            list_B = [

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 2 \mid n(n+1)$'' is a true statement}""",

                    r"""True. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, n(n+1)$ is odd'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 2 \mid n(n+1)$'' is a true statement}""",

                    r"""True. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, n(n+1)$ is odd'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\,n(n+1)$ is even'' is a true statement}""",

                    r"""True. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 2 \nmid n(n+1)$'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\,n(n+1)$ is even'' is a true statement}""",

                    r"""True. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 2 \nmid n(n+1)$'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                ####################################

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 2 \mid n(n+1)$'' is a false statement}""",

                    r"""False. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, n(n+1)$ is odd'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 2 \mid n(n+1)$'' is a false statement}""",

                    r"""False. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, n(n+1)$ is odd'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\,n(n+1)$ is even'' is a false statement}""",

                    r"""False. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 2 \nmid n(n+1)$'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\,n(n+1)$ is even'' is a false statement}""",

                    r"""False. $n$ and $n+1$ are two consecutive integers, so one of them is always even. Hence $2 \mid n(n+1)$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 2 \nmid n(n+1)$'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                )
            ]

            tich = r"n(n+1)"

            vd_nguyen_to = r"$n=1$: $1\cdot2=2$"

            vd_hop_so = r"$n=2$: $2\cdot3=6$"

            vd_cp_dung = r"$n=0$: $0\cdot1=0=0^2$"

            vd_cp_sai = r"$n=1$: $1\cdot2=2$"

            ly_giai_nt = (
                r"""For every $n \geq 2$, both $n$ and $n+1$ are greater than $1$, so the product is a composite number."""
            )

        else:

            list_B = [

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 2 \mid (n-1)n$'' is a true statement}""",

                    r"""True. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, (n-1)n$ is odd'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 2 \mid (n-1)n$'' is a true statement}""",

                    r"""True. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, (n-1)n$ is odd'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, (n-1)n$ is even'' is a true statement}""",

                    r"""True. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 2 \nmid (n-1)n$'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, (n-1)n$ is even'' is a true statement}""",

                    r"""True. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 2 \nmid (n-1)n$'' is a true statement}""",

                    r"""False. The product of two consecutive integers is always even."""
                ),

                ##############===============

                    (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 2 \mid (n-1)n$'' is a false statement}""",

                    r"""False. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, (n-1)n$ is odd'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 2 \mid (n-1)n$'' is a false statement}""",

                    r"""False. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, (n-1)n$ is odd'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, (n-1)n$ is even'' is a false statement}""",

                    r"""False. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 2 \nmid (n-1)n$'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, (n-1)n$ is even'' is a false statement}""",

                    r"""False. If $n=0$, then $(n-1)n=0$ is even. For $n \geq 1$, $(n-1)$ and $n$ are two consecutive integers, so their product is divisible by $2$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 2 \nmid (n-1)n$'' is a false statement}""",

                    r"""True. The product of two consecutive integers is always even."""
                )
            ]

            tich = r"(n-1)n"

            vd_nguyen_to = r"$n=2$: $1\cdot2=2$"

            vd_hop_so = r"$n=3$: $2\cdot3=6$"

            vd_cp_dung = r"$n=1$: $0\cdot1=0=0^2$"

            vd_cp_sai = r"$n=2$: $1\cdot2=2$"

            ly_giai_nt = (
                r"""For every $n \geq 3$, both $n-1$ and $n$ are greater than $1$, so the product is a composite number."""
            )

        # =====================================================
        # NHÓM C
        # =====================================================

        # Sửa 01/10/2026 (Claude, cô Lan duyệt lại): bản cũ có hai phát biểu sai toán học
        # (``∃n∈N, tích là số chính phương'' bị đánh SAI dù n = 0 cho 0 = 0^2) và lỗi câu ``∀n∈N sao cho''.
        # Nay Python tự xác định chân trị của 4 mệnh đề ∃P, ∀P, ∃(không P), ∀(không P), mỗi mệnh đề hỏi
        # ``là mệnh đề đúng'' và ``là mệnh đề sai'' -> luôn có 4 phát biểu đúng, 4 phát biểu sai trở lên.
        tinh, vd_co, vd_khong, them_co = {
            1: ("is a perfect square", vd_cp_dung, vd_cp_sai, ""),
            2: ("is a prime number", vd_nguyen_to, vd_hop_so, " " + ly_giai_nt),
            3: ("is a composite number", vd_hop_so, vd_nguyen_to, ""),
        }[int(nhom_C)]
        khong = tinh.replace("is ", "is not ", 1)
        ly_co = rf"""{vd_co} {tinh}.{them_co}"""
        ly_khong = rf"""{vd_khong} {khong}."""
        bon_md = [
            (rf"""$\exists n \in \mathbb{{N}},\, {tich}$ {tinh}""", True, ly_co),
            (rf"""$\forall n \in \mathbb{{N}},\, {tich}$ {tinh}""", False, ly_khong),
            (rf"""$\exists n \in \mathbb{{N}},\, {tich}$ {khong}""", True, ly_khong),
            (rf"""$\forall n \in \mathbb{{N}},\, {tich}$ {khong}""", False, ly_co),
        ]
        c_dung, c_sai = [], []
        for md, gt_md, ly in bon_md:
            for hoi in (True, False):
                pb = rf"""The statement ``{md}'' is a {"true" if hoi else "false"} statement"""
                (c_dung if hoi == gt_md else c_sai).append((pb, ly))
        list_C = _phat_bieu(c_dung, c_sai)

        # =====================================================
        # NHÓM D
        # =====================================================

        list_D = [

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 6 \mid (n^3-n)$'' is a true statement}""",

                    r"""True. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 9 \mid (n^3-n)$'' is a true statement}""",

                    r"""False. For $n=2$, $n^3-n=6$, and $6$ is not divisible by $9$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 6 \mid (n^3-n)$'' is a true statement}""",

                    r"""True. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 9 \mid (n^3-n)$'' is a true statement}""",

                    r"""True. For $n=0$, $n^3-n=0$, and $0$ is divisible by $9$."""
                ),
                ##########

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' is a true statement}""",

                    r"""False. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' is a true statement}""",

                    r"""False. For $n=0$, $n^3-n=0$, and $0$ is divisible by $9$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' is a true statement}""",

                    r"""False. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' is a true statement}""",

                    r"""True. For $n=2$, $n^3-n=6$, and $6$ is not divisible by $9$."""
                ),

                ################################====================

                (

                    r"""{The statement ``$\forall n \in \mathbb{N},\, 6 \mid (n^3-n)$'' is a false statement}""",

                    r"""False. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 9 \mid (n^3-n)$'' is a false statement}""",

                    r"""True. For $n=2$, $n^3-n=6$, and $6$ is not divisible by $9$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 6 \mid (n^3-n)$'' is a false statement}""",

                    r"""False. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 9 \mid (n^3-n)$'' is a false statement}""",

                    r"""False. For $n=0$, $n^3-n=0$, and $0$ is divisible by $9$."""
                ),
                ##########

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' is a false statement}""",

                    r"""True. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{\True The statement ``$\forall n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' is a false statement}""",

                    r"""True. For $n=0$, $n^3-n=0$, and $0$ is divisible by $9$."""
                ),

                (

                    r"""{\True The statement ``$\exists n \in \mathbb{N},\, 6 \nmid (n^3-n)$'' is a false statement}""",

                    r"""True. We have $n^3-n=(n-1)n(n+1)$, which is the product of three consecutive integers, so it is always divisible by both $2$ and $3$. Hence it is divisible by $6$."""
                ),

                (

                    r"""{The statement ``$\exists n \in \mathbb{N},\, 9 \nmid (n^3-n)$'' is a false statement}""",

                    r"""False. For $n=2$, $n^3-n=6$, and $6$ is not divisible by $9$."""
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
            "P": "the natural number $n$ is divisible by $6$",
            "P_hoa": "The natural number $n$ is divisible by $6$",

            "Q": "the natural number $n$ is divisible by $2$",
            "Q_hoa": "The natural number $n$ is divisible by $2$"
        },

        {
            "P": "the sum of the digits of the natural number $n$ is divisible by $3$",
            "P_hoa": "The sum of the digits of the natural number $n$ is divisible by $3$",

            "Q": "the natural number $n$ is divisible by $3$",
            "Q_hoa": "The natural number $n$ is divisible by $3$"
        },

        {
            "P": "the natural number $n$ has a units digit of $0$",
            "P_hoa": "The natural number $n$ has a units digit of $0$",

            "Q": "the natural number $n$ is divisible by $5$",
            "Q_hoa": "The natural number $n$ is divisible by $5$"
        },

        {
            "P": "the natural number $n$ is divisible by $10$",
            "P_hoa": "The natural number $n$ is divisible by $10$",

            "Q": "the natural number $n$ has an even units digit",
            "Q_hoa": "The natural number $n$ has an even units digit"
        },

        # ================= TAM GIÁC =================

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",

            "Q": "triangle $ABC$ is an isosceles triangle",
            "Q_hoa": "Triangle $ABC$ is an isosceles triangle"
        },

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",

            "Q": "triangle $ABC$ has two equal angles",
            "Q_hoa": "Triangle $ABC$ has two equal angles"
        },

        {
            "P": "triangle $ABC$ has one angle equal to $90^{\\circ}$",
            "P_hoa": "Triangle $ABC$ has one angle equal to $90^{\\circ}$",

            "Q": "triangle $ABC$ is a right triangle",
            "Q_hoa": "Triangle $ABC$ is a right triangle"
        },

        {
            "P": "triangle $ABC$ is isosceles and has an angle of $60^{\\circ}$",
            "P_hoa": "Triangle $ABC$ is isosceles and has an angle of $60^{\\circ}$",

            "Q": "triangle $ABC$ is equilateral",
            "Q_hoa": "Triangle $ABC$ is equilateral"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "quadrilateral $ABCD$ is a rhombus",
            "P_hoa": "Quadrilateral $ABCD$ is a rhombus",

            "Q": "quadrilateral $ABCD$ has perpendicular diagonals",
            "Q_hoa": "Quadrilateral $ABCD$ has perpendicular diagonals"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rhombus with one right angle",
            "Q_hoa": "Quadrilateral $ABCD$ is a rhombus with one right angle"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rectangle with two equal adjacent sides",
            "Q_hoa": "Quadrilateral $ABCD$ is a rectangle with two equal adjacent sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rectangle",
            "Q_hoa": "Quadrilateral $ABCD$ is a rectangle"
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
            f"""Given the following two statements:\\\\
            $P \\colon$ ``{P_hoa}'';\\\\
            $Q \\colon$ ``{Q_hoa}''.\\\\
            Which of the following correctly states the conditional statement $P \\Rightarrow Q$?"""
        )

        # ================= ĐIỀU KIỆN CẦN =================

        if kieu_hoi == 0:

            dapso = f"``{Q_hoa}'' is a necessary condition for ``{P}''"

            dsnhieu = [

                f"``{P_hoa}'' is a necessary condition for ``{Q}''",

                f"``{P_hoa}'' is a necessary and sufficient condition for ``{Q}''",

                f"``{Q_hoa}'' is a sufficient condition for ``{P}''"
            ]

            giai = (
                f"The statement $P \\Rightarrow Q$ can be stated as: "
                f"``{Q_hoa}'' is a necessary condition for ``{P}''."
            )

        # ================= ĐIỀU KIỆN ĐỦ =================

        else:

            dapso = f"``{P_hoa}'' is a sufficient condition for ``{Q}''"

            dsnhieu = [

                f"``{Q_hoa}'' is a sufficient condition for ``{P}''",

                f"``{P_hoa}'' is a necessary and sufficient condition for ``{Q}''",

                f"``{Q_hoa}'' is a necessary condition for ``{P}''"
            ]

            giai = (
                f"The statement $P \\Rightarrow Q$ can be stated as: "
                f"``{P_hoa}'' is a sufficient condition for ``{Q}''."
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
            "P": "the natural number $n$ is divisible by $2$",
            "P_hoa": "The natural number $n$ is divisible by $2$",

            "Q": "the natural number $n$ has an even units digit",
            "Q_hoa": "The natural number $n$ has an even units digit"
        },

        {
            "P": "the natural number $n$ is divisible by $5$",
            "P_hoa": "The natural number $n$ is divisible by $5$",

            "Q": "the natural number $n$ has a units digit of $0$ or $5$",
            "Q_hoa": "The natural number $n$ has a units digit of $0$ or $5$"
        },

        {
            "P": "the natural number $n$ is divisible by $10$",
            "P_hoa": "The natural number $n$ is divisible by $10$",

            "Q": "the natural number $n$ has a units digit of $0$",
            "Q_hoa": "The natural number $n$ has a units digit of $0$"
        },

        # ================= TAM GIÁC =================

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",

            "Q": "triangle $ABC$ is isosceles and has an angle of $60^{\\circ}$",
            "Q_hoa": "Triangle $ABC$ is isosceles and has an angle of $60^{\\circ}$"
        },

        {
            "P": "triangle $ABC$ is a right triangle",
            "P_hoa": "Triangle $ABC$ is a right triangle",

            "Q": "triangle $ABC$ has one angle equal to $90^{\\circ}$",
            "Q_hoa": "Triangle $ABC$ has one angle equal to $90^{\\circ}$"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rectangle with two equal adjacent sides",
            "Q_hoa": "Quadrilateral $ABCD$ is a rectangle with two equal adjacent sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rhombus with one right angle",
            "Q_hoa": "Quadrilateral $ABCD$ is a rhombus with one right angle"
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
            f"""Given the following two statements:\\\\
            $P \\colon$ ``{P_hoa}'';\\\\
            $Q \\colon$ ``{Q_hoa}''.\\\\
            Which of the following correctly states the biconditional statement $P \\Leftrightarrow Q$?"""
        )

        # ================= ĐIỀU KIỆN CẦN VÀ ĐỦ =================

        if kieu_hoi == 0:

            dapso = f"``{P_hoa}'' is a necessary and sufficient condition for ``{Q}''"

            dsnhieu = [

                f"``{P_hoa}'' is a necessary condition for ``{Q}''",

                f"``{P_hoa}'' is a sufficient condition for ``{Q}''",

                f"``{Q_hoa}'' is a sufficient condition for ``{P}''"
            ]

            giai = (
                f"The statement $P \\Leftrightarrow Q$ can be stated as: "
                f"``{P_hoa}'' is a necessary and sufficient condition for ``{Q}''."
            )

        # ================= TƯƠNG ĐƯƠNG =================

        else:

            dapso = f"``{P_hoa}'' is equivalent to ``{Q}''"

            dsnhieu = [

                f"``{P_hoa}'' is a necessary condition for ``{Q}''",

                f"``{P_hoa}'' is a sufficient condition for ``{Q}''",

                f"``{Q_hoa}'' is a sufficient condition for ``{P}''"
            ]

            giai = (
                f"The statement $P \\Leftrightarrow Q$ can be stated as: "
                f"``{P_hoa}'' is equivalent to ``{Q}''."
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
            "P": "the natural number $n$ is divisible by $6$",
            "P_hoa": "The natural number $n$ is divisible by $6$",

            "Q": "the natural number $n$ is divisible by $2$",
            "Q_hoa": "The natural number $n$ is divisible by $2$"
        },

        {
            "P": "the sum of the digits of the natural number $n$ is divisible by $3$",
            "P_hoa": "The sum of the digits of the natural number $n$ is divisible by $3$",

            "Q": "the natural number $n$ is divisible by $3$",
            "Q_hoa": "The natural number $n$ is divisible by $3$"
        },

        {
            "P": "the natural number $n$ has a units digit of $0$",
            "P_hoa": "The natural number $n$ has a units digit of $0$",

            "Q": "the natural number $n$ is divisible by $5$",
            "Q_hoa": "The natural number $n$ is divisible by $5$"
        },

        {
            "P": "the natural number $n$ is divisible by $10$",
            "P_hoa": "The natural number $n$ is divisible by $10$",

            "Q": "the natural number $n$ has an even units digit",
            "Q_hoa": "The natural number $n$ has an even units digit"
        },

        # ================= TAM GIÁC =================

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",

            "Q": "triangle $ABC$ is an isosceles triangle",
            "Q_hoa": "Triangle $ABC$ is an isosceles triangle"
        },

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",

            "Q": "triangle $ABC$ has two equal angles",
            "Q_hoa": "Triangle $ABC$ has two equal angles"
        },

        {
            "P": "triangle $ABC$ has one angle equal to $90^{\\circ}$",
            "P_hoa": "Triangle $ABC$ has one angle equal to $90^{\\circ}$",

            "Q": "triangle $ABC$ is a right triangle",
            "Q_hoa": "Triangle $ABC$ is a right triangle"
        },

        {
            "P": "triangle $ABC$ is isosceles and has an angle of $60^{\\circ}$",
            "P_hoa": "Triangle $ABC$ is isosceles and has an angle of $60^{\\circ}$",

            "Q": "triangle $ABC$ is equilateral",
            "Q_hoa": "Triangle $ABC$ is equilateral"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "quadrilateral $ABCD$ is a rhombus",
            "P_hoa": "Quadrilateral $ABCD$ is a rhombus",

            "Q": "quadrilateral $ABCD$ has perpendicular diagonals",
            "Q_hoa": "Quadrilateral $ABCD$ has perpendicular diagonals"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rhombus with one right angle",
            "Q_hoa": "Quadrilateral $ABCD$ is a rhombus with one right angle"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rectangle with two equal adjacent sides",
            "Q_hoa": "Quadrilateral $ABCD$ is a rectangle with two equal adjacent sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a rectangle",
            "Q_hoa": "Quadrilateral $ABCD$ is a rectangle"
        },
        # ================= SỐ HỌC =================

        {
            "P": "the natural number $n$ is divisible by $12$",
            "P_hoa": "The natural number $n$ is divisible by $12$",

            "Q": "the natural number $n$ is divisible by $3$",
            "Q_hoa": "The natural number $n$ is divisible by $3$"
        },

        {
            "P": "the natural number $n$ is divisible by $12$",
            "P_hoa": "The natural number $n$ is divisible by $12$",

            "Q": "the natural number $n$ is divisible by $4$",
            "Q_hoa": "The natural number $n$ is divisible by $4$"
        },

        {
            "P": "the natural number $n$ is divisible by $15$",
            "P_hoa": "The natural number $n$ is divisible by $15$",

            "Q": "the natural number $n$ is divisible by $5$",
            "Q_hoa": "The natural number $n$ is divisible by $5$"
        },

        {
            "P": "the natural number $n$ is divisible by $18$",
            "P_hoa": "The natural number $n$ is divisible by $18$",

            "Q": "the natural number $n$ is divisible by $9$",
            "Q_hoa": "The natural number $n$ is divisible by $9$"
        },

        {
            "P": "the last digit of the natural number $n$ is $5$",
            "P_hoa": "The last digit of the natural number $n$ is $5$",

            "Q": "the natural number $n$ is divisible by $5$",
            "Q_hoa": "The natural number $n$ is divisible by $5$"
        },

        {
            "P": "the natural number $n$ is divisible by $8$",
            "P_hoa": "The natural number $n$ is divisible by $8$",

            "Q": "the natural number $n$ is divisible by $2$",
            "Q_hoa": "The natural number $n$ is divisible by $2$"
        },

        # ================= TAM GIÁC =================

        {
            "P": "triangle $ABC$ is an isosceles right triangle",
            "P_hoa": "Triangle $ABC$ is an isosceles right triangle",

            "Q": "triangle $ABC$ is an isosceles triangle",
            "Q_hoa": "Triangle $ABC$ is an isosceles triangle"
        },

        {
            "P": "triangle $ABC$ is an isosceles right triangle",
            "P_hoa": "Triangle $ABC$ is an isosceles right triangle",

            "Q": "triangle $ABC$ is a right triangle",
            "Q_hoa": "Triangle $ABC$ is a right triangle"
        },

        {
            "P": "triangle $ABC$ is equilateral",
            "P_hoa": "Triangle $ABC$ is equilateral",

            "Q": "triangle $ABC$ has three equal sides",
            "Q_hoa": "Triangle $ABC$ has three equal sides"
        },

        {
            "P": "triangle $ABC$ has three equal sides",
            "P_hoa": "Triangle $ABC$ has three equal sides",

            "Q": "triangle $ABC$ is equilateral",
            "Q_hoa": "Triangle $ABC$ is equilateral"
        },

        {
            "P": "triangle $ABC$ is an isosceles triangle",
            "P_hoa": "Triangle $ABC$ is an isosceles triangle",

            "Q": "triangle $ABC$ has two equal sides",
            "Q_hoa": "Triangle $ABC$ has two equal sides"
        },

        {
            "P": "triangle $ABC$ is a right triangle",
            "P_hoa": "Triangle $ABC$ is a right triangle",

            "Q": "triangle $ABC$ has one angle equal to $90^{\\circ}$",
            "Q_hoa": "Triangle $ABC$ has one angle equal to $90^{\\circ}$"
        },

        # ================= TỨ GIÁC =================

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ has four equal sides",
            "Q_hoa": "Quadrilateral $ABCD$ has four equal sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ has two equal diagonals",
            "Q_hoa": "Quadrilateral $ABCD$ has two equal diagonals"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ has perpendicular diagonals",
            "Q_hoa": "Quadrilateral $ABCD$ has perpendicular diagonals"
        },

        {
            "P": "quadrilateral $ABCD$ is a rectangle",
            "P_hoa": "Quadrilateral $ABCD$ is a rectangle",

            "Q": "quadrilateral $ABCD$ has four right angles",
            "Q_hoa": "Quadrilateral $ABCD$ has four right angles"
        },

        {
            "P": "quadrilateral $ABCD$ is a rhombus",
            "P_hoa": "Quadrilateral $ABCD$ is a rhombus",

            "Q": "quadrilateral $ABCD$ has four equal sides",
            "Q_hoa": "Quadrilateral $ABCD$ has four equal sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a parallelogram",
            "P_hoa": "Quadrilateral $ABCD$ is a parallelogram",

            "Q": "quadrilateral $ABCD$ has parallel opposite sides",
            "Q_hoa": "Quadrilateral $ABCD$ has parallel opposite sides"
        },

        {
            "P": "quadrilateral $ABCD$ is a rectangle",
            "P_hoa": "Quadrilateral $ABCD$ is a rectangle",

            "Q": "quadrilateral $ABCD$ is a parallelogram",
            "Q_hoa": "Quadrilateral $ABCD$ is a parallelogram"
        },

        {
            "P": "quadrilateral $ABCD$ is a square",
            "P_hoa": "Quadrilateral $ABCD$ is a square",

            "Q": "quadrilateral $ABCD$ is a parallelogram",
            "Q_hoa": "Quadrilateral $ABCD$ is a parallelogram"
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
            f"""Given the following theorem:\\\\
            ``If {P}, then {Q}''.\\\\
            Which of the following statements is the """
        )

        # ================= GIẢ THIẾT =================

        if kieu_hoi == 0:

            debai += "hypothesis of the given theorem?"

            dapso = P_hoa

            dsnhieu = [

                Q_hoa,

                f"If {Q}, then {P}",

                f"{P_hoa} and {_c1_thuong(Q)}"
            ]

            giai = (
                f"In the statement ``If {P}, then {Q}'', "
                f"the statement that follows ``If'' is the hypothesis."
            )

        # ================= KẾT LUẬN =================

        else:

            debai += "conclusion of the given theorem?"

            dapso = Q_hoa

            dsnhieu = [

                P_hoa,

                f"If {Q}, then {P}",

                f"{P_hoa} and {_c1_thuong(Q)}"
            ]

            giai = (
                f"In the theorem ``If {P}, then {Q}'', "
                f"the statement that follows ``then'' is the conclusion."
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
                f"Subset notation must use curly braces or the empty set symbol.\\\\"
                f"Since ${pt_thuoc}$ is only an element of the set $A$, we have "
                f"${pt_thuoc} \\in A$, not ${pt_thuoc} \\subset A$.\\\\"
                f"Hence, the option ${pt_thuoc}$ is not a subset of $A$."
            )

        elif kieu_sai == 1:

            # Đáp án là tập một phần tử ngoài A

            dapso = f"""$\\left\\{{ {ngoai} \\right\\}}$"""

            giai = (
                f"We have ${ngoai} \\notin A$, so "
                f"$\\left\\{{ {ngoai} \\right\\}}$ is not a subset of $A$."
            )

        else:

            # Đáp án là tập nhiều phần tử chứa phần tử ngoài A

            idx1 = np.random.randint(0, len(A_list))

            pt1 = A_list[idx1]

            # Viet theo thu tu tang dan, cach nhau boi dau ";" nhu tap A
            nho, lon = sorted([pt1, ngoai])

            dapso = f"""$\\left\\{{ {nho}; {lon} \\right\\}}$"""

            giai = (
                f"We have ${ngoai} \\notin A$, so "
                f"$\\left\\{{ {nho}; {lon} \\right\\}}$ is not a subset of $A$."
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
                f"""Which of the following options is """
                f"""\\textbf{{not}} a subset of the set """
                f"""$A = {A_latex}$?"""
            )

        elif cach_hoi == 1:

            debai = (
                f"""Given the set $A = {A_latex}$.\\\\
                Which of the following options is """
                f"""\\textbf{{not}} a subset of $A$?"""
            )

        elif cach_hoi == 2:

            debai = (
                f"""Given the set $A = {A_latex}$.\\\\
                Find the option that is \\textbf{{not}} a subset of $A$."""
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
                f"""Which of the following options """
                f"""is \\textbf{{not}} """
                f"""a subset of the set """
                f"""$A = {A_latex}$?"""
            )

        elif cach_hoi == 1:

            debai = (
                f"""Given the set $A = {A_latex}$.\\\\
                Which of the following options """
                f"""is \\textbf{{not}} a subset of $A$?"""
            )

        else:

            debai = (
                f"""Given the set $A = {A_latex}$.\\\\
                Find the option that is \\textbf{{not}} a subset of $A$."""
            )
        # =====================================================
        # ĐÁP ÁN
        # =====================================================

        dapso = f"${pt_thuoc}$"

        # =====================================================
        # LỜI GIẢI
        # =====================================================

        giai = (
            f"${pt_thuoc}$ is an element of the set $A$, "
            f"that is, ${pt_thuoc} \\in A$.\\\\"
            f"To represent a subset, we must use "
            f"curly braces or the empty set symbol.\\\\"
            f"For example: "
            f"$\\left\\{{ {pt_thuoc} \\right\\}} \\subset A$.\\\\"
            f"Hence, the option ${pt_thuoc}$ "
            f"is not a subset of $A$."
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

                f"$A$ does not contain the element $\\varnothing$."
            ),

            (
                f"$\\varnothing \\subset A$",

                True,

                f"The empty set is a subset of every set."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\in A$",

                False,

                f"$A$ does not contain the element "
                f"$\\left\\{{ \\varnothing \\right\\}}$."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$",

                False,

                f"For "
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$ "
                f"to hold, we need $\\varnothing \\in A$."
            )
        ])

        # =====================================================
        # DANH SÁCH KHẲNG ĐỊNH THƯỜNG
        # =====================================================

        ds_khangdinh = [

            (
                f"${pt1} \\in A$",

                True,

                f"Since ${pt1}$ is an element of $A$, "
                f"${pt1} \\in A$."
            ),

            (
                f"${pt2} \\subset A$",

                False,

                f"${pt2}$ is an element, so we do not use the symbol "
                f"$\\subset$."
            ),

            (
                f"$\\left\\{{ {pt3} \\right\\}} \\in A$",

                False,

                f"$A$ does not contain the element "
                f"$\\left\\{{ {pt3} \\right\\}}$."
            ),

            (
                f"$\\left\\{{ {pt4} \\right\\}} \\subset A$",

                True,

                f"Every element of "
                f"$\\left\\{{ {pt4} \\right\\}}$ belongs to $A$."
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
                f"""Given the set $A = {A_latex}$.\\\\
                How many of the following statements are true?"""
            )

        else:

            dapso = f"${so_sai}$"

            debai = (
                f"""Given the set $A = {A_latex}$.\\\\
                How many of the following statements are """
                f"""\\textbf{{false}}?"""
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

                kq = "true"

            else:

                kq = "false"

            giai += (
                f"{chr(97+i)}) {md} is a {kq} statement. "
                f"{lg}\\\\"
            )

        if hoi_dung == 0:

            giai += (
                f"Therefore, the number of true statements is ${so_dung}$."
            )

        else:

            giai += (
                f"Therefore, the number of false statements is ${so_sai}$."
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

                f"$A$ does not contain the element $\\varnothing$."
            ),

            (
                f"$\\varnothing \\subset A$",

                True,

                f"The empty set is a subset of every set."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\in A$",

                False,

                f"$A$ does not contain the element "
                f"$\\left\\{{ \\varnothing \\right\\}}$."
            ),

            (
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$",

                False,

                f"For "
                f"$\\left\\{{ \\varnothing \\right\\}} \\subset A$ "
                f"to hold, we need $\\varnothing \\in A$."
            )
        ])

        # =====================================================
        # DANH SÁCH KHẲNG ĐỊNH THƯỜNG
        # =====================================================

        ds_khangdinh = [

            (
                f"${pt1} \\in A$",

                True,

                f"Since ${pt1}$ is an element of $A$, "
                f"${pt1} \\in A$ is true."
            ),

            (
                f"${pt2} \\subset A$",

                False,

                f"${pt2}$ is an element, so we do not use the symbol "
                f"$\\subset$."
            ),

            (
                f"$\\left\\{{ {pt3} \\right\\}} \\in A$",

                False,

                f"$A$ does not contain the element "
                f"$\\left\\{{ {pt3} \\right\\}}$."
            ),

            (
                f"$\\left\\{{ {pt4} \\right\\}} \\subset A$",

                True,

                f"Every element of "
                f"$\\left\\{{ {pt4} \\right\\}}$ belongs to $A$."
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
                f"""Given the set $A = {A_latex}$.\\\\
                How many of the following statements are true?"""
            )

        else:

            dapso = f"${so_sai}$"

            debai = (
                f"""Given the set $A = {A_latex}$.\\\\
                How many of the following statements are """
                f"""\\textbf{{false}}?"""
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

                kq = "true"

            else:

                kq = "false"

            giai += (
                f"{chr(97+i)}) {md} is a {kq} statement. "
                f"{lg}\\\\"
            )

        if hoi_dung == 0:

            giai += (
                f"Therefore, the number of true statements is ${so_dung}$."
            )

        else:

            giai += (
                f"Therefore, the number of false statements is ${so_sai}$."
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

        debai = f"""Given two sets ${Tap_Con}$ and ${Tap_Me}$ such that ${Tap_Con} \\subset {Tap_Me}$ and an element ${Phan_Tu} \\in {Tap_Con}$. Choose the true statement."""

        dapso = f"""${Phan_Tu} \\in {Tap_Me}$"""
        dsnhieu = [
            f"""${Phan_Tu} \\subset {Tap_Me}$""",
            f"""${Phan_Tu} \\notin {Tap_Me}$""",
            f"""$\\left\\{{ {Phan_Tu} \\right\\}} \\in {Tap_Con}$"""
        ]

        giai = f"""Since the element ${Phan_Tu}$ belongs to the set ${Tap_Con}$ (written ${Phan_Tu} \\in {Tap_Con}$) and every element of the set ${Tap_Con}$ must belong to the set ${Tap_Me}$ (because of the subset relation ${Tap_Con} \\subset {Tap_Me}$), the element ${Phan_Tu}$ must belong to the set ${Tap_Me}$. The correct mathematical notation is ${Phan_Tu} \\in {Tap_Me}$.\\\\
        - The option ${Phan_Tu} \\subset {Tap_Me}$ is false because the only relation between an element and a set is membership ($\\in$), not containment ($\\subset$).\\\\
        - The option $\\left\\{{ {Phan_Tu} \\right\\}} \\in {Tap_Con}$ is false because a set containing the element ${Phan_Tu}$ must use the containment relation $\\left\\{{ {Phan_Tu} \\right\\}} \\subset {Tap_Con}$, not membership."""

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN

def L10_C1_B2_TH018_MC_A_01(socau, dang=1):

    # Danh sách các chữ cái hoa đặt tên cho tập hợp
    chu_hoa = ['A', 'B', 'X', 'Y', 'M', 'P', 'E', 'F']

    max_cau = len(chu_hoa) * 4
    if socau > max_cau:
        raise ValueError(f"socau must not exceed {max_cau}")

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

        debai = f"""Given the set ${T_Hop} \\ne \\varnothing$. Which of the following statements is \\textbf{{true}}?"""

        if k == 0:
            dapso = f"""${T_Hop} \\setminus {T_Hop} = \\varnothing$"""

            dsnhieu = [
                f"""${T_Hop} \\setminus \\varnothing = \\varnothing$""",
                f"""$\\varnothing \\setminus {T_Hop} = {T_Hop}$""",
                f"""$\\varnothing \\setminus \\varnothing = {T_Hop}$"""
            ]

            giai = (
                f"""The difference of the two sets ${T_Hop} \\setminus {T_Hop}$ is the set of elements that belong to ${T_Hop}$ """
                f"""but not to ${T_Hop}$. Hence ${T_Hop} \\setminus {T_Hop}=\\varnothing$."""
            )

        elif k == 1:
            dapso = f"""${T_Hop} \\setminus \\varnothing = {T_Hop}$"""

            dsnhieu = [
                f"""${T_Hop} \\setminus {T_Hop} = {T_Hop}$""",
                f"""$\\varnothing \\setminus {T_Hop} = {T_Hop}$""",
                f"""${T_Hop} \\setminus \\varnothing = \\varnothing$"""
            ]

            giai = (
                f"""Since the empty set contains no elements, removing the elements of """
                f"""$\\varnothing$ from ${T_Hop}$ leaves the set unchanged. Hence """
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
                f"""The intersection of ${T_Hop}$ with the empty set is the set of elements common to both sets. """
                f"""Since the empty set has no elements, ${T_Hop} \\cap \\varnothing = \\varnothing$."""
            )

        else:
            dapso = f"""${T_Hop} \\cup \\varnothing = {T_Hop}$"""

            dsnhieu = [
                f"""${T_Hop} \\cup \\varnothing = \\varnothing$""",
                f"""${T_Hop} \\cup {T_Hop} = \\varnothing$""",
                f"""$\\varnothing \\cup \\varnothing = {T_Hop}$"""
            ]

            giai = (
                f"""The union of ${T_Hop}$ with the empty set consists of all elements that belong to ${T_Hop}$ """
                f"""or to $\\varnothing$. Since the empty set adds no elements, """
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
                f"The set ${tap1} \\setminus {tap2}$ consists of the elements that belong to "
                f"${tap1}$ but not to ${tap2}$. We have "
                f"${tap1} \\setminus {tap2}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        elif pheptoan_code == 1:
            pheptoan_tex = f"{tap2} \\setminus {tap1}"
            z_ans = len_hieu_BA
            tap_kq_list = sorted(list(B_set - A_set))
            giai_chi_tiet = (
                f"The set ${tap2} \\setminus {tap1}$ consists of the elements that belong to "
                f"${tap2}$ but not to ${tap1}$. We have "
                f"${tap2} \\setminus {tap1}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        elif pheptoan_code == 2:
            pheptoan_tex = f"{tap1} \\cap {tap2}"
            z_ans = len_giao
            tap_kq_list = sorted(list(A_set & B_set))
            giai_chi_tiet = (
                f"The set ${tap1} \\cap {tap2}$ consists of the elements that belong to "
                f"${tap1}$ and also to ${tap2}$. We have "
                f"${tap1} \\cap {tap2}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        else:
            pheptoan_tex = f"{tap1} \\cup {tap2}"
            z_ans = len_hop
            tap_kq_list = sorted(list(A_set | B_set))
            giai_chi_tiet = (
                f"The set ${tap1} \\cup {tap2}$ consists of the elements that belong to "
                f"${tap1}$ or to ${tap2}$. We have "
                f"${tap1} \\cup {tap2}=\\left\\{{{'; '.join(map(str, tap_kq_list))}\\right\\}}$."
            )

        A_tex = "\\left\\{" + "; ".join(map(str, A_list)) + "\\right\\}"
        B_tex = "\\left\\{" + "; ".join(map(str, B_list)) + "\\right\\}"

        mau_de = [
            f"Given two sets:\\\\ ${tap1}={A_tex}$,\\\\ ${tap2}={B_tex}$.\\\\ How many elements does the set ${pheptoan_tex}$ have?",
            f"Given ${tap1}={A_tex}$ \\\\ and ${tap2}={B_tex}$. \\\\ The number of elements of the set ${pheptoan_tex}$ is",
            f"Suppose ${tap1}={A_tex}$ \\\\ and ${tap2}={B_tex}$.\\\\ Compute the number of elements of the set ${pheptoan_tex}$.",
            f"For the two sets:\\\\ ${tap1}={A_tex}$,\\\\ ${tap2}={B_tex}$.\\\\ The value of $n({pheptoan_tex})$ is",
            f"Given two sets ${tap1}$ and ${tap2}$ as follows:\\\\ ${tap1}={A_tex}$,\\\\ ${tap2}={B_tex}$.\\\\ How many elements does the set ${pheptoan_tex}$ contain?"
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
            f"{giai_chi_tiet}\\\\ Counting the elements of the set above, we get ${z_ans}$ elements.",
            f"{giai_chi_tiet}\\\\ Hence $n({pheptoan_tex})={z_ans}$.",
            f"{giai_chi_tiet}\\\\ It follows that the required set has ${z_ans}$ elements.",
            f"{giai_chi_tiet}\\\\ Therefore, the number of elements of the set ${pheptoan_tex}$ is ${z_ans}$."
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

        debai = f"""Given the set $A = [{a_val}; {b_val})$. Which of the following sets is a subset of the set $A$?"""

        # ĐỒNG BỘ BỌC TOÀN BỘ PHƯƠNG ÁN CHỌN TRONG CẶP DẤU $ DUY NHẤT
        dapso = f"""$({a0}; {b0})$"""
        dsnhieu = [
            f"""$[{a1}; {b1})$""",
            f"""$(-\\infty; {b2})$""",
            f"""$({a3}; {b_val}]$"""
        ]

        giai = f"""A set of numbers $X$ is a subset of $A = [{a_val}; {b_val})$ if and only if every element of $X$ belongs to $A$.\\\\
        - Consider the option $({a0}; {b0})$: Since ${a_val} < {a0} < {b0} < {b_val}$, the entire open interval $({a0}; {b0})$ lies inside the half-open interval $[{a_val}; {b_val})$. Hence $({a0}; {b0}) \\subset A$.\\\\
        - Each of the other options contains elements that do not belong to $A$ (for example: $[{a1}; {b1})$ contains an element less than ${a_val}$, $(-\\infty; {b2})$ contains arbitrarily large negative numbers, $({a3}; {b_val}]$ contains the element ${b_val}$, which $A$ does not have)."""

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
            f"Given the set ${ten_tap}={A_str}$. Find the complement set $C_{{\\mathbb{{R}}}}^{ten_tap}$.",
            f"Given ${ten_tap}={A_str}$. Which of the following correctly represents the complement of ${ten_tap}$ in $\\mathbb{{R}}$?",
            f"Determine $C_{{\\mathbb{{R}}}}^{ten_tap}$ given that ${ten_tap}={A_str}$.",
            f"In $\\mathbb{{R}}$, the complement of the set ${ten_tap}={A_str}$ is",
            f"Find $\\mathbb{{R}}\\setminus {ten_tap}$ for ${ten_tap}={A_str}$."
        ]

        debai = np.random.choice(mau_de)

        dapso = f"${dap_so_str}$"

        dsnhieu = [
            f"${nhieu1}$",
            f"${nhieu2}$",
            f"${nhieu3}$"
        ]

        mau_giai = [
            f"By definition, $C_{{\\mathbb{{R}}}}^{ten_tap}=\\mathbb{{R}}\\setminus {ten_tap}$. Hence the result is ${dap_so_str}$.",
            f"The complement of the set ${ten_tap}$ in $\\mathbb{{R}}$ is the set of real numbers not belonging to ${ten_tap}$. It follows that $C_{{\\mathbb{{R}}}}^{ten_tap}={dap_so_str}$.",
            f"Consider the endpoints of ${ten_tap}$ and apply the rule of switching the brackets when taking the complement. We obtain $C_{{\\mathbb{{R}}}}^{ten_tap}={dap_so_str}$.",
            f"The complement set consists of all real numbers outside ${ten_tap}$. Therefore $C_{{\\mathbb{{R}}}}^{ten_tap}={dap_so_str}$."
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

            debai = f"""\\immini{{The sets $A$, $B$, $C$ are represented by the Venn diagram shown at right. The shaded region consists of the points that belong to both $A$ and $B$ but lie entirely outside the set $C$. Which of the following sets does the shaded region represent?}}{{{tikz_full}}}"""
            dapso = """$(A \\cap B) \\setminus C$"""
            dsnhieu = ["""$A \\setminus (B \\cap C)$""", """$(B \\cap C) \\setminus A$""",
                       """$B \\setminus (A \\cap C)$"""]
            giai = """The shaded region lies in the common part of the two sets $A$ and $B$, that is, it belongs to the intersection $A \\cap B$. At the same time, this region lies outside the set $C$. Hence, by the definition of the difference of two sets, the shaded region represents the set $(A \\cap B) \\setminus C$."""

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

            debai = f"""\\immini{{Given the sets $A$, $B$, $C$ shown in the Venn diagram at right. The shaded region represents the region that belongs to both $B$ and $C$ but lies entirely outside the set $A$. Which of the following sets does the shaded region represent?}}{{{tikz_full}}}"""
            dapso = """$(B \\cap C) \\setminus A$"""
            dsnhieu = ["""$B \\setminus (A \\cap C)$""", """$(A \\cap B) \\setminus C$""",
                       """$C \\setminus (A \\cap B)$"""]
            giai = """The shaded region lies in the common part of the two sets $B$ and $C$, that is, it belongs to the intersection $B \\cap C$. At the same time, this region lies outside the set $A$. Hence, by the definition of the difference of two sets, the shaded region represents the set $(B \\cap C) \\setminus A$."""

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

            debai = f"""\\immini{{Given the sets $A$, $B$, $C$ shown in the Venn diagram at right. The shaded region represents the region that belongs to both $A$ and $C$ but lies entirely outside the set $B$. Which of the following sets does the shaded region represent?}}{{{tikz_full}}}"""
            dapso = """$(A \\cap C) \\setminus B$"""
            dsnhieu = ["""$A \\setminus (B \\cap C)$""", """$(A \\cap B) \\setminus C$""",
                       """$C \\setminus (A \\cap B)$"""]
            giai = """The shaded region lies in the common part of the two sets $A$ and $C$, that is, it belongs to the intersection $A \\cap C$. At the same time, this region lies outside the set $B$. Hence, by the definition of the difference of two sets, the shaded region represents the set $(A \\cap C) \\setminus B$."""

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

            debai = f"""\\immini{{Given the sets $A$, $B$, $C$ shown in the Venn diagram at right. The shaded region lies only inside the set $A$ and has no overlap at all with the two sets $B, C$. Which of the following sets does the shaded region represent?}}{{{tikz_full}}}"""
            dapso = """$A \\setminus (B \\cup C)$"""
            dsnhieu = ["""$A \\setminus (B \\cap C)$""", """$(A \\setminus B) \\cap C$""",
                       """$(A \\cap B) \\setminus C$"""]
            giai = """The shaded region lies within the set $A$ but excludes every element that belongs to the set $B$ or to the set $C$. Since the set of elements that belong to $B$ or to $C$ is the union $B \\cup C$, the shaded region represents the difference $A \\setminus (B \\cup C)$."""

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

    cho = (f"Given the sets $A = \\left[ {a_val}; {b_val} \\right]$ and $B = \\left( {n_val}; m \\right]$, where $m$ is an integer such that $B \\ne \\varnothing$. ")

    # ---- KIỂU 1: A ∪ B = A  ⟺  B ⊂ A. Vì n > a nên chỉ cần m ≤ b ----
    if kieu == 1:
        dapso = b_val - n_val
        debai = cho + ("How many integer values of the parameter $m$ are there such that $A \\cup B = A$?")
        giai = f"""We have $A \\cup B = A \\Leftrightarrow B \\subset A$.\\\\
Since $B \\ne \\varnothing$, we have $m > {n_val}$.\\\\
Since ${n_val} > {a_val}$, the left endpoint of $B$ already lies in $A$, so we only need to add
$m \\le {b_val}$.\\\\
It follows that
$\\heva{{m > {n_val} \\\\ m \\le {b_val}}}$ or ${n_val} < m \\le {b_val}$.\\\\
Since $m \\in \\mathbb{{Z}}$, we have $m \\in {_VD021_liet_ke(n_val + 1, b_val)}$,
and the number of integer values of $m$ is ${b_val} - {_VD021_ngoac(n_val)} = {dapso}$.\\\\
Therefore, the number of integer values of the parameter $m$ that satisfy the problem is ${dapso}$."""

    # ---- KIỂU 2: A ∪ B = B  ⟺  A ⊂ B  ⟺  m ≥ b (có vô số m nguyên) ----
    elif kieu == 2:
        dapso = b_val
        debai = cho + ("Find the smallest integer value of the parameter $m$ such that $A \\cup B = B$.")
        giai = f"""We have $A \\cup B = B \\Leftrightarrow A \\subset B$.\\\\
With $A = \\left[ {a_val}; {b_val} \\right]$ and $B = \\left( {n_val}; m \\right]$, for $A \\subset B$ we need
$\\heva{{{n_val} < {a_val} \\\\ m \\ge {b_val}}}$.\\\\
The inequality ${n_val} < {a_val}$ already holds, so the remaining condition is
$m \\ge {b_val}$.\\\\
There are infinitely many integers $m$ that work, but the SMALLEST integer among them is
$m = {b_val}$.\\\\
Check: for $m = {b_val}$ we have $B = \\left( {n_val}; {b_val} \\right] \\supset \\left[ {a_val}; {b_val} \\right] = A$, so $A \\cup B = B$.\\\\
Therefore, $m = {dapso}$."""

    # ---- KIỂU 3: A ∩ B = ∅. B ≠ ∅ nên n < m, và B nằm hẳn bên trái A ----
    elif kieu == 3:
        dapso = a_val - n_val - 1
        debai = cho + ("How many integer values of the parameter $m$ are there such that $A \\cap B = \\varnothing$?")
        giai = f"""Since $B \\ne \\varnothing$, we have $m > {n_val}$.\\\\
Since ${n_val} < {a_val}$, the set $B = \\left( {n_val}; m \\right]$ lies to the left of $A = \\left[ {a_val}; {b_val} \\right]$;
the two sets have no common element if and only if
$m < {a_val}$.\\\\
It follows that
$\\heva{{m > {n_val} \\\\ m < {a_val}}}$ or ${n_val} < m < {a_val}$.\\\\
Since $m \\in \\mathbb{{Z}}$, we have $m \\in {_VD021_liet_ke(n_val + 1, a_val - 1)}$,
and the number of integer values of $m$ is ${a_val} - {_VD021_ngoac(n_val)} - 1 = {dapso}$.\\\\
Therefore, the number of integer values of the parameter $m$ that satisfy the problem is ${dapso}$."""

    # ---- KIỂU 4: A ∩ B ≠ ∅  ⟺  m ≥ a (có vô số m nguyên) ----
    else:
        dapso = a_val
        debai = cho + ("Find the smallest integer value of the parameter $m$ such that $A \\cap B \\ne \\varnothing$.")
        giai = f"""Since ${n_val} < {a_val}$, the sets $B = \\left( {n_val}; m \\right]$ and $A = \\left[ {a_val}; {b_val} \\right]$ have a common element
if and only if the right endpoint of $B$ reaches $A$, that is,
$m \\ge {a_val}$.\\\\
Then the element ${a_val}$ belongs to both $A$ and $B$, so $A \\cap B \\ne \\varnothing$.\\\\
There are infinitely many integers $m$ that work, but the SMALLEST integer among them is
$m = {a_val}$.\\\\
Therefore, $m = {dapso}$."""

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

        debai = f"""Given three sets:\\\\ $A = ({left_A}; {right_A}]$,\\\\ $B = \\{{ {b1}; {b2} \\}}$,\\\\ $C = \\{{x \\in \\mathbb{{N}} \\mid {debai_pt} \\}}$ where $m$ is an integer parameter."""

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
            chuoi_giai_thich_tap_dich = f"We have $A \\cap B = \\{{ {b2} \\}}$."
            # Điều kiện x thuộc giao: x = b2
            ds_target = [b2]
        elif phep_toan_D == 'hop':
            chuoi_phep_toan = "A \\cup B"
            chuoi_giai_thich_tap_dich = f"We have $A \\cup B = ({left_A}; {right_A}] \\cup \\{{ {b1} \\}}$."
            # Nghiệm tự nhiên x nằm trong tập hợp hợp (số tự nhiên thuộc A hoặc bằng b1)
            # Tập số thực A chứa các số tự nhiên từ max(0, left_A+1) đến right_A
            start_N = max(0, left_A + 1)
            ds_target = [x for x in range(start_N, right_A + 1)]
            if b1 >= 0:
                ds_target.append(b1)
            ds_target = list(set(ds_target))
        elif phep_toan_D == 'A_tru_B':
            chuoi_phep_toan = "A \\setminus B"
            chuoi_giai_thich_tap_dich = f"We have $A \\setminus B = ({left_A}; {right_A}] \\setminus \\{{ {b2} \\}}$."
            # Số tự nhiên thuộc A nhưng bỏ đi b2
            start_N = max(0, left_A + 1)
            ds_target = [x for x in range(start_N, right_A + 1) if x != b2]
        else:  # B_tru_A
            chuoi_phep_toan = "B \\setminus A"
            chuoi_giai_thich_tap_dich = f"We have $B \\setminus A = \\{{ {b1} \\}}$."
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
        loi_giai_bo_sung_D = f"{chuoi_giai_thich_tap_dich} The only natural-number solution of the set $C$ (when $m \\ge 0$) is $x = {k_coef}m$. "
        if phep_toan_D == 'hop' or phep_toan_D == 'A_tru_B':
            loi_giai_bo_sung_D += f"For $C \\subset ({chuoi_phep_toan})$, ${k_coef}m$ must belong to the target set, which leads to {so_luong_m_khong_am} nonnegative integer values of $m$ that satisfy the condition. In addition, when $m < 0 \\Rightarrow C = \\varnothing  \\subset ({chuoi_phep_toan})$ (always true), infinitely many negative integer values of $m$ also satisfy the condition."
        else:  # giao hoặc B_tru_A (chỉ có tối đa 1 phần tử đích)
            if so_luong_m_khong_am > 0:
                loi_giai_bo_sung_D += f"For $C \\subset ({chuoi_phep_toan}) \\Rightarrow C = \\{{ {ds_target[0]} \\}} \\Rightarrow {k_coef}m = {ds_target[0]} \\Rightarrow m = {m_nguyen_thoa_man[0]}$ (valid). Combined with the infinitely many negative integers $m < 0$ (for which $C = \\varnothing $), there are infinitely many integer values of $m$."
            else:
                loi_giai_bo_sung_D += f"For $C \\subset ({chuoi_phep_toan})$, no nonnegative integer value of $m$ works, because the solution is not an integer or is negative. However, for every $m < 0 \\Rightarrow C = \\varnothing  \\subset ({chuoi_phep_toan})$, so infinitely many negative integer values still work."

        phuong_an_sai_so_nghiem_D = f"There are exactly {so_luong_m_khong_am + 1} integer values of the parameter $m$ such that $C \\subset ({chuoi_phep_toan})$"
        giai_thich_sai_so_nghiem_D = f"False. Besides the nonnegative integer values that work, there are always infinitely many negative integers $m < 0$ for which $C = \\varnothing $, and the empty set is a subset of every set, so the total number of integer values of $m$ must be infinite."

        ds_abcd = (
            # ==================== Ý A: KHẢO SÁT VỀ MỆNH ĐỀ TOÁN HỌC ====================
            [
                (f"""{{\\True The statement ``The set $A$ has {hieu_cuoi_dau_A_sai} elements'' is a mathematical statement}}""",
                 f"""True. The sentence above has a clearly defined truth value (specifically, it is a mathematical statement whose value is false, because the set $A$ of real numbers has infinitely many elements)."""),

                (f"""{{\\True The statement ``The set $B$ has $2$ elements'' is a mathematical statement}}""",
                 f"""True. The sentence ``The set $B$ has $2$ elements'' is a completely accurate assertion (a true statement), so it is a mathematical statement."""),

                (f"""{{The statement ``The set $A$ has {hieu_cuoi_dau_A_sai} elements'' is not a mathematical statement}}""",
                 f"""False. Although the sentence above is false mathematically (because the set $A$ of real numbers has infinitely many elements), it has a clearly defined truth value, so by definition it must be a mathematical statement."""),

                (f"""{{The statement ``The set $B$ has $2$ elements'' is not a mathematical statement}}""",
                 f"""False. The sentence above is a mathematical assertion with a clearly defined truth value (a true statement), so it is a mathematical statement."""),

                (f"""{{\\True The statement ``The set $A$ has {hieu_cuoi_dau_A_dung} elements'' is a mathematical statement}}""",
                 f"""True. This is a mathematical assertion with a clearly defined truth value, so by definition it is a mathematical statement."""),

                (f"""{{The statement ``The set $A$ has {hieu_cuoi_dau_A_dung} elements'' is not a mathematical statement}}""",
                 f"""False. The sentence above has a clearly defined truth value, so it must be a mathematical statement."""),

                (f"""{{\\True The statement ``The set $B$ has ${hieu_cuoi_dau_B_dung}$ elements'' is a mathematical statement}}""",
                 f"""True. The sentence above has a clearly defined truth value, so by definition it is a mathematical statement."""),

                (f"""{{The statement ``The set $B$ has ${hieu_cuoi_dau_B_dung}$ elements'' is not a mathematical statement}}""",
                 f"""False. Because it has a clearly defined truth value, it must be a mathematical statement."""),

                (f"""{{\\True The statement ``The set $B$ has ${hieu_cuoi_dau_B_sai}$ elements'' is a mathematical statement}}""",
                 f"""True. The sentence above has a clearly defined truth value, so by definition it is a mathematical statement."""),

                (f"""{{The statement ``The set $B$ has ${hieu_cuoi_dau_B_sai}$ elements'' is not a mathematical statement}}""",
                 f"""False. It is a mathematical assertion with a clearly defined truth value.""")
            ],

            # ==================== Ý B: CÁC PHÉP TOÁN TOÁN HỌC THUẦN TÚY ====================
            [
                (f"""{{\\True $A \\cap B = \\{{ {b2} \\}}$}}""",
                 f"""True. Since ${b1} < {left_A}$, we have ${b1} \\notin A$. The element ${b2}$ lies in the interval $({left_A}; {right_A}]$, so ${b2} \\in A$. Hence the intersection of the two sets consists only of the element ${b2}$."""),

                (f"""{{\\True $n(A \\cap B) = 1$}}""",
                 f"""True. The intersection $A \\cap B$ has exactly $1$ element."""),

                (f"""{{\\True $B \\setminus A = \\{{ {b1} \\}}$}}""",
                 f"""True. Since ${b1} \\notin A$ and ${b2} \\in A$, taking the difference of set $B$ minus set $A$ removes the element ${b2}$ and keeps the element ${b1}$."""),

                (f"""{{$A \\cup B = A$}}""",
                 f"""False. Since ${b1} < {left_A}$, we have ${b1} \\notin A$, so the union $A \\cup B$ must contain the additional element ${b1}$, that is, $A \\cup B \\neq A$."""),

                (f"""{{$A \\cap B = \\{{ {b1}; {b2} \\}}$}}""",
                 f"""False. Since ${b1} < {left_A}$, the element ${b1}$ does not belong to the set $A$, so this element cannot be in the intersection $A \\cap B$."""),

                (f"""{{$A \\cap B = ( {left_A}; {b2} ]$}}""",
                 f"""False. The intersection of a set of real numbers and a discrete set must be a discrete set (a set with finitely many elements), not a continuous interval or half-open interval."""),

                (f"""{{$A \\cap B = \\{{ {b1} \\}}$}}""",
                 f"""False. Since ${b1} \\notin A$ and ${b2} \\in A$, the intersection must have exactly $1$ element, namely the element that lies in the set $A$."""),

                (f"""{{$A \\cup B = \\{{ {b1}; {right_A} \\}}$}}""",
                 f"""False. Since the set $A$ is a set of real numbers with infinitely many elements, the union $A \\cup B$ is an infinite set and cannot have only two isolated elements."""),

                (f"""{{$B \\setminus A = \\{{ {b2} \\}}$}}""",
                 f"""False. The element ${b2}$ belongs to the set $A$, so it is removed when forming the difference $B \\setminus A$; the element that is kept must be one that does not belong to $A$."""),

                (f"""{{$B \\setminus A = \\varnothing $}}""",
                 f"""False. Since ${b1} \\in B$ but ${b1} \\notin A$, the difference set satisfies $B \\setminus A \\neq \\varnothing $."""),

                (f"""{{$A \\setminus B = A$}}""",
                 f"""False. Since the set $A$ contains the element ${b2} \\in B$, taking the difference $A \\setminus B$ removes that element from $A$.""")
            ],

            # ==================== Ý C: KHẢO SÁT CHỈ DỰA VÀO SỐ LƯỢNG PHẦN TỬ ====================
            [
                (f"""{{\\True For $m = {m_duong}$ the set $C$ has exactly $1$ element}}""",
                 f"""True. For $m = {m_duong}$, the equation has two solutions, one negative (rejected) and one positive (accepted). Because of the condition $x \\in \\mathbb{{N}}$, the set $C$ has exactly $1$ element."""),

                (f"""{{For $m = {m_duong}$ the set $C$ has exactly $2$ elements}}""",
                 f"""False. The equation always has a negative integer solution, which does not satisfy the condition of being a natural number ($x \\in \\mathbb{{N}}$) and is therefore rejected, so the set $C$ cannot have $2$ elements."""),

                (f"""{{\\True For $m = {m_am}$ the set $C$ is the empty set}}""",
                 f"""True. When $m = {m_am} < 0$, both solutions of the equation are negative, so they do not belong to the set $\\mathbb{{N}}$ of natural numbers. Hence the set $C$ is the empty set."""),

                (f"""{{For $m = {m_am}$ the set $C$ has exactly $1$ element}}""",
                 f"""False. When $m < 0$, all solutions of the equation are negative and are all rejected by the condition $x \\in \\mathbb{{N}}$, so the set $C$ has no elements (it is the empty set)."""),

                (f"""{{\\True For $m = 0$ the set $C$ has exactly $1$ element}}""",
                 f"""True. When $m = 0$, the equation has one negative solution, which is rejected, and one solution equal to $0$, which satisfies the condition $x \\in \\mathbb{{N}}$. Hence the set $C$ has exactly $1$ element."""),

                (f"""{{For $m = 0$ the set $C$ is the empty set}}""",
                 f"""False. When $m = 0$, the equation still gives a natural number solution that satisfies the condition, so the set $C$ is not the empty set.""")
            ],

            # ==================== Ý D: XÈT TẬP CON ĐA PHÉP TOÁN (MỚI) ====================
            [
                # --- Các phương án ĐÚNG (Có dấu \True) ---
                (f"""{{\\True There are infinitely many integer values of the parameter $m$ such that $C \\subset ({chuoi_phep_toan})$}}""",
                 f"""True. {loi_giai_bo_sung_D}"""),
                
                # --- Các phương án SAI (Không có dấu \True) ---
                (f"""{{{phuong_an_sai_so_nghiem_D}}}""",
                 f"""{giai_thich_sai_so_nghiem_D}"""),

                (f"""{{There is no integer value of the parameter $m$ such that $C \\subset ({chuoi_phep_toan})$}}""",
                 f"""False. For every negative integer $m < 0$, we have $C = \\varnothing  \\subset ({chuoi_phep_toan})$, which always satisfies the requirement, so the problem has infinitely many integer solutions.""")
            ]
        )

        # Bổ sung 01/10/2026 (Claude, cô Lan duyệt lại): ý d chỉ có 1 phát biểu đúng -> thêm phát biểu đếm
        # m không âm, m thuộc đoạn [-5; 20] (5 giá trị âm luôn thoả mãn vì C rỗng).
        so_m = so_luong_m_khong_am
        ds_m = "; ".join(str(t) for t in m_nguyen_thoa_man) if m_nguyen_thoa_man else ""
        ly_dem = (f"{chuoi_giai_thich_tap_dich} For $m < 0$ we have $C = \\varnothing \\subset ({chuoi_phep_toan})$. For $m \\ge 0$ we have $C = \\{{ {k_coef}m \\}}$, so we need ${k_coef}m \\in ({chuoi_phep_toan})$: "
                  + (f"$m \\in \\{{ {ds_m} \\}}$ (there are ${so_m}$ values)." if so_m else "no such value exists.")
                  + f" On the closed interval $[-5; 20]$ there are $5 + {so_m} = {5 + so_m}$ integer values of $m$.")
        mau_ko_am = f"There are exactly ${{}}$ nonnegative integer values of the parameter $m$ such that $C \\subset ({chuoi_phep_toan})$"
        mau_doan = f"There are exactly ${{}}$ integer values of $m$ in the closed interval $[-5; 20]$ such that $C \\subset ({chuoi_phep_toan})$"
        _tf_them(ds_abcd[3],
                 [(mau_ko_am.format(so_m) if so_m else
                   f"There is no nonnegative integer value of the parameter $m$ such that $C \\subset ({chuoi_phep_toan})$", ly_dem), (mau_doan.format(5 + so_m), ly_dem),
                  (f"Every negative integer value of $m$ satisfies $C \\subset ({chuoi_phep_toan})$", ly_dem)],
                 [(mau_ko_am.format(so_m + 1), ly_dem), (mau_doan.format(so_m), ly_dem), (mau_doan.format(4 + so_m), ly_dem),
                  (f"Every integer value of $m$ satisfies $C \\subset ({chuoi_phep_toan})$", ly_dem)])
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
        ly_do = (r"Since $\left(x - %d\right)^2 \geq 0$ for all $x$ and equals $0$ when $x = %d$, $P(x)$ is true for all $x \in \mathbb{R}$ if and only if $%s$." % (a, a, dk))
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
        ly_do = (r"Since the minimum value of $\left(x - %d\right)^2$ is $0$ (when $x = %d$), $P(x)$ is true for all $x \in \mathbb{R}$ if and only if $%s$."
                 % (a, a, dk))
    dapso_val = max(0, k_cuoi - k_dau + 1)
    debai = (r"Given the predicate $P(x)\colon %s %s 0$ with $x \in \mathbb{R}$. How many integer values of the parameter $k$ in $%s$ are there such that the statement $P(x)$ is true for all $x \in \mathbb{R}$?" % (bt, dau, khoang))
    giai = (r"We have $%s$." % bien_doi + "\\\\\n" + ly_do + "\\\\\n" +
            r"Combining with $k \in %s$ and $k$ an integer (a bounded interval contains only finitely many integers): $k \in \left\{%d; %d; \ldots; %d\right\}$." % (khoang, k_dau, k_dau + 1, k_cuoi) +
            "\\\\\n" +
            r"The number of integer values of $k$ is $%d - %s + 1 = %d$."
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
    ten_cuc = "minimum" if duong else "maximum"
    # gia tri cuc tri cua f la  k - a^2 (duong)  hoac  k + a^2 (am)
    if kieu == "ton_tai":
        # ton tai x: f(x) dau 0  <=>  cuc tri dau 0 (min khi f<.., max khi f>..)
        dau_k = dau
        cau_hoi = r"the statement ``$\exists x \in \mathbb{R},\ %s %s 0$'' is true" % (bt, dau)
        ly_do = (r"We have $%s = %s$, so the %s value of the left side is $%s$ (when $x = %d$)."
                 % (bt, ghep, ten_cuc, cuc, a) + "\\\\\n" +
                 r"There exists $x$ such that $%s %s 0$ if and only if that %s value is $%s 0$, that is, $%s %s 0$." % (bt, dau, ten_cuc, dau, cuc, dau))
    else:
        # voi moi x: f(x) dau 0 SAI <=> ton tai x: f(x) (dau phu dinh) 0
        phu = {'>': r'\leq', r'\geq': '<', '<': r'\geq', r'\leq': '>'}[dau]
        dau_k = phu
        cau_hoi = (r"the statement ``$\forall x \in \mathbb{R},\ %s %s 0$'' is \textbf{false}"
                   % (bt, dau))
        ly_do = (r"The statement ``$\forall x \in \mathbb{R},\ %s %s 0$'' is false if and only if its negation ``$\exists x \in \mathbb{R},\ %s %s 0$'' is true." % (bt, dau, bt, phu) +
                 "\\\\\n" +
                 r"We have $%s = %s$, so the %s value of the left side is $%s$ (when $x = %d$)."
                 % (bt, ghep, ten_cuc, cuc, a) + "\\\\\n" +
                 r"Hence the condition is $%s %s 0$." % (cuc, phu))
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
    debai = (r"How many integer values of the parameter $k$ in $%s$ are there such that %s?"
             % (khoang, cau_hoi))
    giai = (ly_do.rstrip(".") + r" $\Leftrightarrow %s$." % dk + "\\\\\n" +
            r"Combining with $k \in %s$ and $k$ an integer: $k \in \left\{%d; %d; \ldots; %d\right\}$."
            % (khoang, k_dau, k_dau + 1, k_cuoi) + "\\\\\n" +
            r"The number of integer values of $k$ is $%d - %s + 1 = %d$."
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
            f"Given the predicate $P(x)\\colon x {dau_tex} x^{{{n}}}$. How many of the following statements are true?\n\\begin{{enumerate}}\n\\item $P({a})$.\n\\item $P\\left({frac_str}\\right)$.\n\\item $\\forall x\\in \\mathbb{{N}}, P(x)$.\n\\item $\\exists x\\in \\mathbb{{N}}, \\overline{{P(x)}}$.\n\\end{{enumerate}}"
        )

        dapso = f"${so_menh_de_dung}$"
        dsnhieu = [f"${i}$" for i in range(5) if i != so_menh_de_dung]

        # SUA 29/09/2026 (co Lan: gach dau dong khong dat, cac y danh so
        # 1., 2., ...): loi giai cu viet "- P(3) la Sai. - ..." dinh lien
        # mot mach tren PDF va khong neu ly do. Nay danh so tung y, moi y
        # mot dong, kem phep thu cu the.
        def dung_sai(b):
            return "true" if b else "false"

        phan_so = f"\\dfrac{{{p}}}{{{q}}}"
        mu_ps = f"\\dfrac{{{p ** n}}}{{{q ** n}}}"
        # phan vi du nho nhat trong N (0, 1, 2, ...) lam P(x) sai
        phan_vd = next((x for x in range(5) if not check(x)), None)
        if phan_vd is None:
            ly_do_3 = (f"true: for $x \\in \\left\\{{0; 1\\right\\}}$ we have $x = x^{{{n}}}$, and for $x \\ge 2$ we have $x < x^{{{n}}}$")
            ly_do_4 = f"false, because $P(x)$ is true for all $x \\in \\mathbb{{N}}$ (item 3)"
        else:
            ly_do_3 = (f"false, because for $x = {phan_vd}$ the statement ${phan_vd} {dau_tex} {phan_vd}^{{{n}}} = {phan_vd ** n}$ is false")
            ly_do_4 = f"true, because $x = {phan_vd}$ makes $P(x)$ false"
        giai = (
            f"Consider the predicate $P(x)\\colon x {dau_tex} x^{{{n}}}$.\n\\begin{{enumerate}}\n\\item $P({a})\\colon {a} {dau_tex} {a}^{{{n}}} = {a ** n}$ is {dung_sai(p1)}.\n\\item $P\\left({phan_so}\\right)\\colon {phan_so} {dau_tex} \\left({phan_so}\\right)^{{{n}}} = {mu_ps}$ is {dung_sai(p2)}.\n\\item $\\forall x\\in \\mathbb{{N}}, P(x)$ is {ly_do_3}.\n\\item $\\exists x\\in \\mathbb{{N}}, \\overline{{P(x)}}$ is {ly_do_4}.\n\\end{{enumerate}}\nTherefore, $\\mathbf{{{so_menh_de_dung}}}$ of the statements are true."
        )

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)

    return cauTN


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
        "duong": "positive integer",
        "am": "negative integer",
        "khong_am": "nonnegative integer",
        "khong_duong": "nonpositive integer",
        "nguyen": "integer",
    }

    for loai, trai, phai, a, m, so_luong in gt:

        ten = ten_loai[loai]

        debai = (
            f"Find the integer value of the parameter $m$ (with $m > {a}$) such that the number of {ten} elements in the set $\\left{trai}{a};m\\right{phai}$ is exactly {so_luong}."
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
            f"Starting from the left endpoint, the {ten} elements that can belong to ${khoang}$ are, in order, ${'; '.join(str(x) for x in day_so)}; \\ldots$\\\\\nThe number of {ten} elements in the set is exactly {so_luong} if and only if it contains ${t_k}$ but not ${t_sau}$, that is, ${dk}$.\\\\\nSince $m$ is an integer, $m = {m}$. Then the {ten} elements in $\\left{trai}{a};{m}\\right{phai}$ are ${lietke}$."
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

        debai = (r"Let $n$ be a natural number and consider the two statements\\ $P$: ``$n$ is divisible by $%d$'' \quad and \quad $Q$: ``$n$ is divisible by $%d$''."
                 % (sP, sQ))
        ds_abcd = [
            (r"Determine whether the conditional statement $P \Rightarrow Q$ is true or false.",
             r"\text{%s}" % ("True" if pq_dung else "False"),
             (r"Every number divisible by $%d$ is divisible by $%d$ (since $%d$ is divisible by $%d$), so $P \Rightarrow Q$ is a \textbf{true} statement." % (sP, sQ, sP, sQ))
             if pq_dung else
             (r"Take $n = %d$: then $n$ is divisible by $%d$, so $P$ is true, but $n$ is not divisible by $%d$, so $Q$ is false.\\ There is a case where $P$ is true and $Q$ is false, so $P \Rightarrow Q$ is a \textbf{false} statement." % (vd_pq, sP, sQ))),
            (r"Determine whether the converse $Q \Rightarrow P$ is true or false.",
             r"\text{%s}" % ("True" if qp_dung else "False"),
             (r"Every number divisible by $%d$ is divisible by $%d$, so the converse $Q \Rightarrow P$ is \textbf{true}." % (sQ, sP))
             if qp_dung else
             (r"Take $n = %d$: then $n$ is divisible by $%d$, so $Q$ is true, but $n$ is not divisible by $%d$, so $P$ is false.\\ Therefore, the converse $Q \Rightarrow P$ is \textbf{false}." % (vd_qp, sQ, sP))),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def _vd014_tl_cau(debai_dau, A, B, ab, ba, nguoc):
    r"""Ghép một câu tự luận "xét P => Q và mệnh đề đảo Q => P".

    ab = (A => B đúng?, lời giải), ba = (B => A đúng?, lời giải).
    nguoc = True thì đổi vai: P là B, Q là A.
    """
    P, Q, (pq, lg_pq), (qp, lg_qp) = (B, A, ba, ab) if nguoc else (A, B, ab, ba)
    debai = (debai_dau + r"\\ $P$: ``%s'' \quad and \quad $Q$: ``%s''." % (P, Q))
    return debai, [
        (r"Determine whether the conditional statement $P \Rightarrow Q$ is true or false.",
         r"\text{%s}" % ("True" if pq else "False"),
         lg_pq + (r" Therefore, $P \Rightarrow Q$ is a \textbf{%s} statement." % ("true" if pq else "false"))),
        (r"State the converse $Q \Rightarrow P$ and determine whether it is true or false.",
         r"\text{%s}" % ("True" if qp else "False"),
         r"Converse: ``If %s, then %s''.\\ " % (Q, P) + lg_qp +
         (r" Therefore, $Q \Rightarrow P$ is a \textbf{%s} statement." % ("true" if qp else "false"))),
    ]


_VD014_HINH = [
    (r"quadrilateral $ABCD$ is a rectangle", r"quadrilateral $ABCD$ has two diagonals of equal length",
     (True, r"A rectangle always has two diagonals of equal length."),
     (False, r"An isosceles trapezoid (with no right angle) has two diagonals of equal length but is not a rectangle.")),
    (r"quadrilateral $ABCD$ is a square", r"quadrilateral $ABCD$ is a rhombus",
     (True, r"A square has four equal sides, so it is a rhombus."),
     (False, r"A rhombus with an angle of $60^{\circ}$ is not a square.")),
    (r"triangle $ABC$ is equilateral", r"triangle $ABC$ is isosceles",
     (True, r"An equilateral triangle has three equal sides, so it is isosceles at every vertex."),
     (False, r"A triangle that is isosceles at $A$ with $\widehat{A} = 40^{\circ}$ is not equilateral.")),
    (r"triangle $ABC$ has a right angle at $A$", r"$BC^2 = AB^2 + AC^2$",
     (True, r"By the Pythagorean theorem."),
     (True, r"By the converse of the Pythagorean theorem.")),
    (r"quadrilateral $ABCD$ is a parallelogram",
     r"the two diagonals of quadrilateral $ABCD$ bisect each other",
     (True, r"That is a property of a parallelogram."),
     (True, r"That is a criterion for recognizing a parallelogram.")),
    (r"quadrilateral $ABCD$ is a rhombus", r"quadrilateral $ABCD$ has two perpendicular diagonals",
     (True, r"The two diagonals of a rhombus are perpendicular to each other."),
     (False, r"A quadrilateral with $AB = AD$, $CB = CD$ but $AB \ne CB$ has perpendicular diagonals but is not a rhombus.")),
    (r"the two triangles are congruent", r"the two triangles have equal areas",
     (True, r"Two congruent triangles have equal areas."),
     (False, r"A triangle with base $4$ and height $3$ and a triangle with base $6$ and height $2$ both have area $6$ but are not congruent.")),
    (r"triangle $ABC$ has two angles equal to $60^{\circ}$", r"triangle $ABC$ is equilateral",
     (True, r"The remaining angle equals $180^{\circ} - 2\cdot 60^{\circ} = 60^{\circ}$, so the triangle is equilateral."),
     (True, r"An equilateral triangle has all three angles equal to $60^{\circ}$.")),
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
        debai, ds_abcd = _vd014_tl_cau(r"Consider the two statements", A, B, ab, ba,
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
            ab = (True, r"If $x > %d$, then $x > 0$, so $x^2 > %d^2 = %d$." % (a, a, a * a))
            ba = (False, r"Take $x = %d$: $x^2 = %d > %d$ but $x < %d$."
                  % (-a - 1, (a + 1) ** 2, a * a, a))
        elif kieu == 1:
            A, B = r"$x = %d$" % a, r"$x^2 = %d$" % (a * a)
            ab = (True, r"Substituting $x = %d$ gives $x^2 = %d$." % (a, a * a))
            ba = (False, r"Take $x = %d$: $x^2 = %d$ but $x \ne %d$." % (-a, a * a, a))
        elif kieu == 2:
            A, B = r"$\left|x\right| < %d$" % a, r"$x < %d$" % a
            ab = (True, r"$\left|x\right| < %d \Leftrightarrow -%d < x < %d$, so $x < %d$."
                  % (a, a, a, a))
            ba = (False, r"Take $x = %d$: $x < %d$ but $\left|x\right| = %d > %d$."
                  % (-a - 1, a, a + 1, a))
        else:
            tong, tich = a + b, a * b
            pt = (r"x^2" + (r" - %dx" % tong if tong > 0 else (r" + %dx" % -tong if tong < 0 else "")) +
                  (r" + %d" % tich if tich > 0 else r" - %d" % -tich) + " = 0")
            pt = pt.replace(" 1x", " x")
            A, B = r"$x = %d$" % a, r"$%s$" % pt
            ab = (True, r"Substituting $x = %d$ into the left side gives $%d^2 %s %s = 0$."
                  % (a, a, (r"- %d\cdot %d" % (tong, a)) if tong >= 0 else (r"+ %d\cdot %d" % (-tong, a)),
                     (r"+ %d" % tich) if tich >= 0 else (r"- %d" % -tich)))
            ba = (False, r"The equation $%s$ has two solutions $x = %d$ and $x = %d$. For $x = %d$ the equation is satisfied but $x \ne %d$." % (pt, a, b, b, a))
        debai, ds_abcd = _vd014_tl_cau(r"Let $x$ be a real number and consider the two statements", A, B, ab, ba,
                                       random.choice([False, True]))
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
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
        debai = (r"Given the sets $A = \left[ %d; %d \right]$ and $B = \left( %d; m \right]$, where $m$ is an integer such that $B \ne \varnothing$." % (a_val, b_val, n_val))
        ds_abcd = [
            (r"How many integer values of $m$ are there such that $A \cap B = \varnothing$?",
             r"%d" % dem, giai_dem),
            (r"Find the smallest integer value of $m$ such that $A \cap B \ne \varnothing$.",
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
        return dict(p=r"The number $%d$ is divisible by $%d$" % (N, m), phu=r"The number $%d$ is not divisible by $%d$" % (N, m),
                    dung=(r == 0), ly_do=(r"$%d = %d\cdot %d$" % (N, m, q) if r == 0 else
                                          r"$%d = %d\cdot %d + %d$ (remainder $%d$)" % (N, m, q, r, r)))
    if loai == 1:
        s = random.randint(4, 45)
        k = s * s + random.choice([0, 0, 1, -1, 2])
        can = int(math.isqrt(k))
        dung = can * can == k
        return dict(p=r"The number $%d$ is a perfect square" % k, phu=r"The number $%d$ is not a perfect square" % k,
                    dung=dung, ly_do=(r"$%d = %d^2$" % (k, can) if dung else
                                      r"$%d^2 = %d < %d < %d = %d^2$" % (can, can * can, k, (can + 1) ** 2, can + 1)))
    if loai == 2:
        s = random.randint(2, 12)
        k = s * s if random.random() < 0.5 else s * s + random.randint(1, 2 * s)
        can = int(math.isqrt(k))
        dung = can * can == k
        return dict(p=r"$\sqrt{%d}$ is a rational number" % k, phu=r"$\sqrt{%d}$ is not a rational number" % k,
                    dung=dung, ly_do=(r"$\sqrt{%d} = %d$" % (k, can) if dung else
                                      r"$%d$ is not a perfect square, so $\sqrt{%d}$ is an irrational number" % (k, k)))
    if loai == 3:
        k = random.randint(2, 2025)
        if random.random() < 0.5:
            return dict(p=r"$\left|-%d\right| \le 0$" % k, phu=r"$\left|-%d\right| > 0$" % k, dung=False,
                        ly_do=r"$\left|-%d\right| = %d > 0$" % (k, k))
        return dict(p=r"$\left|-%d\right| = %d$" % (k, k), phu=r"$\left|-%d\right| \ne %d$" % (k, k), dung=True,
                    ly_do=r"the absolute value of a negative number is its opposite")
    if loai == 4:
        c = random.randint(2, 5)
        m, n = random.sample(range(2, 6), 2)
        if random.random() < 0.5:
            return dict(p=r"$%d^{%d} + %d^{%d} = %d^{%d + %d}$" % (c, m, c, n, c, m, n),
                        phu=r"$%d^{%d} + %d^{%d} \ne %d^{%d + %d}$" % (c, m, c, n, c, m, n), dung=False,
                        ly_do=r"the left side equals $%d$ and the right side equals $%d$" % (c ** m + c ** n, c ** (m + n)))
        return dict(p=r"$%d^{%d}\cdot %d^{%d} = %d^{%d + %d}$" % (c, m, c, n, c, m, n),
                    phu=r"$%d^{%d}\cdot %d^{%d} \ne %d^{%d + %d}$" % (c, m, c, n, c, m, n), dung=True,
                    ly_do=r"multiplying two powers with the same base adds the exponents")
    if loai == 5:
        b = random.randint(-8, 8)
        c = random.randint(-10, 12)
        d = b * b - 4 * c
        bt = _tex_bac2(1, b, c)
        return dict(p=r"The equation $%s = 0$ has a real solution" % bt, phu=r"The equation $%s = 0$ has no real solution" % bt,
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
        return dict(p=r"The equation $%s = 0$ has an integer solution" % bt,
                    phu=r"The equation $%s = 0$ has no integer solution" % bt, dung=co,
                    ly_do=r"the equation has %s $%s$" % ("the solution" if len(ngh) == 1 else "the solutions",
                                                     r";\ ".join("x = " + _tex_so(n_) for n_ in ngh)))
    if loai == 7:
        tu, mau, dung = random.choice([(22, 7, True), (10, 3, True), (16, 5, True), (157, 50, False),
                                       (31, 10, False), (25, 8, False)])
        return dict(p=r"$\pi < \dfrac{%d}{%d}$" % (tu, mau), phu=r"$\pi \ge \dfrac{%d}{%d}$" % (tu, mau),
                    dung=dung, ly_do=r"$\pi \approx 3{,}1416$ while $\dfrac{%d}{%d} = %s$"
                    % (tu, mau, ("%.4f" % (tu / mau)).replace(".", "{,}")))
    k = random.choice([i for i in range(2, 120) if i % 2 or i == 2])
    nt = _la_nguyen_to(k)
    uoc = next((d for d in range(2, k) if k % d == 0), None)
    return dict(p=r"The number $%d$ is prime" % k, phu=r"The number $%d$ is not prime" % k, dung=nt,
                ly_do=(r"$%d$ has only two divisors, $1$ and $%d$" % (k, k) if nt else
                       r"$%d$ is divisible by $%d$" % (k, uoc)))


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
        # 01/10/2026 (cô Lan): một câu chỉ hỏi MỘT chủ đề - bốn phương án cùng một loại mệnh đề về số
        # (cùng chia hết, cùng số chính phương, cùng số nguyên tố...); loại lấy xoay vòng.
        for lo in _c1_uu_tien("c1_md_so_th003", 9):
            chon, cung, loai_da = None, [], set()
            for _t in range(400):
                m = _md_so(lo)
                if m["p"] in loai_da:
                    continue
                if m["dung"] == hoi_dung and chon is None:
                    chon = m
                    loai_da.add(m["p"])
                elif m["dung"] != hoi_dung and len(cung) < 3:
                    cung.append(m)
                    loai_da.add(m["p"])
                if chon and len(cung) == 3:
                    break
            if chon and len(cung) == 3:
                _c1_danh_dau("c1_md_so_th003", [lo])
                break
        tu = "true" if hoi_dung else r"\textbf{false}"
        debai = r"Which of the following statements is %s?" % tu
        giai = (r"The statement ``%s'' is %s because %s.\\ " % (chon["p"], "true" if hoi_dung else "false", chon["ly_do"])
                + r"\\ ".join(r"%s: a %s statement (%s)." % (m["p"], "true" if m["dung"] else "false", m["ly_do"])
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
        debai = (r"Given the statements " + "; ".join(r"$%s$: ``%s''" % (t, m["p"]) for t, m in zip(ten, ds))
                 + r". Write the negation of each statement and determine whether each negation is true or false.")
        ds_abcd = []
        for t, m in zip(ten, ds):
            phu_dung = not m["dung"]
            ds_abcd.append((r"Statement $\overline{%s}$." % t,
                            r"\overline{%s}\ \text{%s}" % (t, "true" if phu_dung else "false"),
                            r"$\overline{%s}$: ``%s''. Since %s, $%s$ is %s, so $\overline{%s}$ is %s."
                            % (t, m["phu"], m["ly_do"], t, "true" if m["dung"] else "false", t,
                               "true" if phu_dung else "false")))
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
            ga = (r"For every real $x$, $x^2 %s \ge %d > 0$. The statement is true." % (dau_k, k))
        else:
            ga = (r"Take $x = 0$: then $0^2 %s = %d$, which is not greater than $0$. The statement is false." % (dau_k, k))
        # b) tồn tại số nguyên x sao cho a x + b = 0
        a_ = random.randint(2, 6)
        b_ = random.choice([i for i in range(-20, 21) if i])
        dung_b = b_ % a_ == 0
        dau_b = "+ %d" % b_ if b_ > 0 else "- %d" % -b_
        ky_b = r"\exists x\in\mathbb{Z},\ %dx %s = 0" % (a_, dau_b)
        nghiem = _tex_so(Rational(-b_, a_))
        gb = (r"The equation $%dx %s = 0$ has the unique solution $x = %s$, which %s an integer. The statement is %s."
              % (a_, dau_b, nghiem, "is" if dung_b else "is not", "true" if dung_b else "false"))
        # c) với mọi số tự nhiên n, n^2 + n chia hết cho m
        m = random.choice([2, 3, 4, 6])
        ky_c = r"\forall n\in\mathbb{N},\ \left(n^2 + n\right)\ \vdots\ %d" % m
        if m == 2:
            gc = (r"$n^2 + n = n(n + 1)$ is the product of two consecutive natural numbers, so it is always divisible by $2$. The statement is true.")
        else:
            n0 = next(n for n in range(0, 20) if (n * n + n) % m)
            gc = (r"Take $n = %d$: then $n^2 + n = %d$ is not divisible by $%d$. The statement is false." % (n0, n0 * n0 + n0, m))
        debai = (r"Use the symbol $\forall$ or $\exists$ to write each of the following statements and determine whether it is true or false.")
        ds_abcd = [
            (r"$P$: ``For every real number $x$, $x^2 %s > 0$''." % dau_k,
             ky_a + r";\ \text{%s}" % ("true" if k > 0 else "false"), r"$P$: ``$%s$''. " % ky_a + ga),
            (r"$Q$: ``There exists an integer $x$ such that $%dx %s = 0$''." % (a_, dau_b),
             ky_b + r";\ \text{%s}" % ("true" if dung_b else "false"), r"$Q$: ``$%s$''. " % ky_b + gb),
            (r"$R$: ``For every natural number $n$, $n^2 + n$ is divisible by $%d$''." % m,
             ky_c + r";\ \text{%s}" % ("true" if m == 2 else "false"), r"$R$: ``$%s$''. " % ky_c + gc),
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
        return (r"If the natural number $a$ is divisible by $%d$, then $a$ is divisible by $%d$" % (m, d), dung,
                (r"$%d = %d\cdot %d$ so every multiple of $%d$ is a multiple of $%d$" % (m, d, m // d, m, d)) if dung else
                (r"for $a = %d$: $a$ is divisible by $%d$ but not divisible by $%d$" % (m, m, d)))
    if loai == 1:
        d = random.randint(3, 9)
        if random.random() < 0.5:
            return (r"If the natural numbers $a$ and $b$ are both divisible by $%d$, then $a + b$ is divisible by $%d$" % (d, d),
                    True, r"$a = %dk$, $b = %dl$, so $a + b = %d(k + l)$" % (d, d, d))
        return (r"If $a + b$ is divisible by $%d$, then the natural numbers $a$ and $b$ are both divisible by $%d$" % (d, d),
                False, r"for $a = 1$, $b = %d$: $a + b = %d$ is divisible by $%d$ but $a$ is not divisible by $%d$"
                % (d - 1, d, d, d))
    BO = [
        (r"If $a$ and $b$ are two even natural numbers, then $a + b$ is even", True, r"the sum of two even numbers is even"),
        (r"If $a + b$ is even, then $a$ and $b$ are two even natural numbers", False,
         r"for $a = 1$, $b = 3$: $a + b = 4$ is even but $a$, $b$ are both odd"),
        (r"If $a$ and $b$ are two odd natural numbers, then $ab$ is odd", True, r"the product of two odd numbers is odd"),
        (r"If $ab$ is even, then $a$ and $b$ are two even natural numbers", False,
         r"for $a = 2$, $b = 3$: $ab = 6$ is even but $b$ is odd"),
        (r"If quadrilateral $ABCD$ has four equal sides, then $ABCD$ is a square", False,
         r"a quadrilateral with four equal sides is a rhombus, not necessarily a square"),
        (r"If quadrilateral $ABCD$ is a square, then $ABCD$ has four equal sides", True,
         r"a square has four equal sides"),
        (r"If triangle $ABC$ has $AB^2 + AC^2 = BC^2$, then triangle $ABC$ has a right angle at $A$", True,
         r"the converse of the Pythagorean theorem"),
        (r"If triangle $ABC$ is a right triangle, then $AB^2 + AC^2 = BC^2$", False,
         r"the triangle may have its right angle at $B$ or $C$, in which case the equality does not hold"),
        (r"If $b^2 \ge 4ac$, then the equation $ax^2 + bx + c = 0$ $(a \ne 0)$ has no solution", False,
         r"$b^2 \ge 4ac$ means $\Delta \ge 0$, so the equation has a solution"),
        (r"If $b^2 < 4ac$, then the equation $ax^2 + bx + c = 0$ $(a \ne 0)$ has no solution", True,
         r"$b^2 < 4ac$ means $\Delta < 0$"),
        (r"If triangle $ABC$ has two angles equal to $60^{\circ}$, then triangle $ABC$ is equilateral", True,
         r"the remaining angle equals $180^{\circ} - 120^{\circ} = 60^{\circ}$"),
        (r"If triangle $ABC$ is isosceles, then $AB = AC$", False, r"the triangle may be isosceles with its apex at $B$ or $C$"),
        (r"If two triangles are congruent, then the two triangles are similar", True,
         r"congruent triangles are a special case of similar triangles (ratio $1$)"),
        (r"If two triangles have equal circumradii, then the two triangles are congruent", False,
         r"two right triangles with the same hypotenuse $2R$ but different legs"),
        (r"If two triangles have equal areas, then the two triangles are congruent", False,
         r"a triangle with base $4$ and height $3$, and a triangle with base $6$ and height $2$"),
    ]
    return random.choice(BO)




def L10_C1_B1_NB001_MC_A_02(socau, dang=1):
    r"""Câu nào là mệnh đề / không là mệnh đề - có cả MỆNH ĐỀ CHỨA BIẾN (chưa
    xác định được đúng sai nên không là mệnh đề) và mệnh đề toán có số.

    CLAUDE THEM 29/09/2026 - bien the 02 cua NB001_MC_A, theo bai "Khong duoc
    di loi nay!; Bay gio la may gio?; 7 khong la so nguyen to; can 5 la so vo
    ti" trong giao an Bai 1. Co Lan duyet.
    """
    KHONG = [(r"Do not go this way!", "an imperative sentence"), (r"What time is it now?", "an interrogative sentence"),
             (r"What a beautiful day today!", "an exclamatory sentence"), (r"Do you like studying Math?", "an interrogative sentence"),
             (r"Solve this problem!", "an imperative sentence"), (r"Wow, this problem is so hard!", "an exclamatory sentence")]
    cauTN = ""
    for _ in range(socau):
        a_, b_ = random.randint(1, 9), random.randint(2, 15)
        m = random.randint(3, 9)
        bien = [(r"$x + %d > %d$" % (a_, b_), r"a sentence containing the variable $x$ whose value is not given, so its truth value cannot be determined"),
                (r"$n$ is divisible by $%d$" % m, r"a sentence containing the variable $n$ whose value is not given, so its truth value cannot be determined"),
                (r"$2x - %d = 0$" % a_, r"a sentence containing the variable $x$ whose value is not given, so its truth value cannot be determined")]
        khong = random.sample(KHONG, 3) + random.sample(bien, 2)
        co = []
        for lo in random.sample(range(9), 3):
            md = _md_so(lo)
            co.append((md["p"], "a %s statement" % ("true" if md["dung"] else "false")))
        la_md = random.choice([True, False])
        if la_md:
            dung, nhieu = co[0], random.sample(khong, 3)
            debai = r"Which of the following sentences is a statement?"
        else:
            dung, nhieu = random.choice(khong), co
            debai = r"Which of the following sentences is \textbf{not} a statement?"
        giai = (r"``%s'': %s. " % dung + r"The remaining sentences: "
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
        debai = (r"Given the open sentence $P(n)$: ``$%s$ is prime'' with $n \in \mathbb{N}^{*}$. How many numbers $n$ satisfying $1 \le n \le %d$ make $P(n)$ a %s statement?"
                 % (bt, N, "true" if hoi_dung else r"\textbf{false}"))
        dong = []
        for n, v, nt in gia_tri:
            if nt:
                dong.append(r"$n = %d$: $%d$ is prime" % (n, v))
            else:
                u = next(d for d in range(2, v) if v % d == 0)
                dong.append(r"$n = %d$: $%d = %d\cdot %d$" % (n, v, u, v // u))
        giai = (r"Compute in turn: " + "; ".join(dong) + r".\\ There are $%d$ value(s) of $n$ for which $P(n)$ is %s."
                % (dem, "true" if hoi_dung else "false"))
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
        debai = (r"Given the statement $P$: ``$\forall x \in \mathbb{R},\ %s > 0$''. Determine whether each of the following statements is true or false:" % bt)
        # a) NB
        y1 = [(r"{\True The negation of $P$ is ``$\exists x \in \mathbb{R},\ %s \le 0$''}" % bt,
               r"True. The negation of $\forall$ is $\exists$, and the negation of $>$ is $\le$."),
              (r"{The negation of $P$ is ``$\exists x \in \mathbb{R},\ %s < 0$''}" % bt,
               r"False. The negation of $>$ is $\le$, so $\overline{P}$: ``$\exists x \in \mathbb{R},\ %s \le 0$''." % bt)]
        # b) TH
        ly_b = (r"$%s = %s$. " % (bt, ghep) + (r"Since $\left(x %s %d\right)^2 \ge 0$, the expression is always positive, so $P$ is true."
                                               % ("+" if p > 0 else "-", abs(p)) if dung_P else
                                               r"For $x = %d$ the expression equals $%d \le 0$, so $P$ is false." % (-p, q - p * p)))
        noi = random.choice([True, False])
        y2 = [(r"{\True $P$ is a %s statement}" % ("true" if dung_P else "false"), r"True. " + ly_b),
              (r"{$P$ is a %s statement}" % ("false" if dung_P else "true"), r"False. " + ly_b)]
        if noi:
            y2 = y2[::-1]
        # c) VD: số nguyên x với biểu thức <= t
        T = random.randint(2, 20)                      # (x + p)^2 <= T
        t = T + q - p * p
        so_nguyen = 2 * math.isqrt(T) + 1
        ly_c = (r"$%s \le %d \Leftrightarrow \left(x %s %d\right)^2 \le %d$. For integer $x$, $x %s %d$ is an integer whose square does not exceed $%d$, so $%d \le x %s %d \le %d$, giving $%d$ integers $x$."
                % (bt, t, "+" if p > 0 else "-", abs(p), T, "+" if p > 0 else "-", abs(p), T, -math.isqrt(T),
                   "+" if p > 0 else "-", abs(p), math.isqrt(T), so_nguyen))
        y3 = [(r"{\True There are exactly $%d$ integers $x$ satisfying $%s \le %d$}" % (so_nguyen, bt, t), r"True. " + ly_c),
              (r"{There are exactly $%d$ integers $x$ satisfying $%s \le %d$}" % (so_nguyen - 1, bt, t), r"False. " + ly_c)]
        # d) VDC: số m nguyên trong [-10; 10] để forall x, x^2 + 2px + m > 0
        K = sum(1 for m in range(-10, 11) if m > p * p)
        bt_m = r"x^2 %s %dx + m" % ("+" if p > 0 else "-", abs(2 * p)) if abs(p) != 0 else "x^2 + m"
        ly_d = (r"$%s = \left(x %s %d\right)^2 + m - %d > 0$ for all $x$ if and only if $m > %d$. In the closed interval $[-10;\ 10]$ there are $%d$ such integer(s) $m$."
                % (bt_m, "+" if p > 0 else "-", abs(p), p * p, p * p, K))
        y4 = [(r"{\True There are exactly $%d$ integer values of $m \in [-10;\ 10]$ for which the statement ``$\forall x \in \mathbb{R},\ %s > 0$'' is true}" % (K, bt_m), r"True. " + ly_d),
              (r"{There are exactly $%d$ integer values of $m \in [-10;\ 10]$ for which the statement ``$\forall x \in \mathbb{R},\ %s > 0$'' is true}" % (K + 1, bt_m), r"False (this includes $m = %d$). " % (p * p) + ly_d)]
        # Bổ sung 01/10/2026: mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai (cô Lan)
        dau = "+" if p > 0 else "-"
        ly_a = (r"The negation of $\forall$ is $\exists$, and the negation of $>$ is $\le$, so $\overline{P}$: ``$\exists x \in \mathbb{R},\ %s \le 0$''." % bt)
        _tf_them(y1, [(r"The statement $P$ reads ``For every real number $x$, $%s > 0$''" % bt, ly_a),
                      (r"The statement $\overline{P}$ reads ``There exists a real number $x$ such that $%s \le 0$''" % bt, ly_a)],
                 [(r"The negation of $P$ is ``$\forall x \in \mathbb{R},\ %s \le 0$''" % bt, ly_a),
                  (r"The negation of $P$ is ``$\exists x \in \mathbb{R},\ %s > 0$''" % bt, ly_a),
                  (r"The statement $P$ reads ``There exists a real number $x$ such that $%s > 0$''" % bt, ly_a)])
        gtri = q - p * p
        _tf_them(y2, [(r"$\overline{P}$ is a %s statement" % ("false" if dung_P else "true"), ly_b),
                      (r"$%s = %s$ for all $x \in \mathbb{R}$" % (bt, ghep), ly_b),
                      (r"For $x = %d$, $%s = %d$" % (-p, bt, gtri), ly_b)],
                 [(r"$\overline{P}$ is a %s statement" % ("true" if dung_P else "false"), ly_b),
                  (r"$%s = \left(x %s %d\right)^2 %s %d$ for all $x \in \mathbb{R}$" % (bt, dau, abs(p), "+" if q + p * p > 0 else "-", abs(q + p * p)), ly_b),
                  (r"For $x = %d$, $%s = %d$" % (-p, bt, gtri + 1), ly_b)])
        d3, s3 = _tf_dem(r"%%s $%%d$ integers $x$ satisfying $%s \le %d$" % (bt, t), so_nguyen, ly_c,
                         [so_nguyen - 1, so_nguyen + 1, so_nguyen + 2, math.isqrt(T) + 1])
        _tf_them(y3, d3, s3)
        d4, s4 = _tf_dem(r"%%s $%%d$ integer values of $m \in [-10;\ 10]$ for which the statement ``$\forall x \in \mathbb{R},\ %s > 0$'' is true"
                         % bt_m, K, ly_d, [K + 1, K - 1, 21 - K])
        _tf_them(y4, d4, s4)
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
        de = r"\left\{n \in \mathbb{N} \mid n \text{ is prime, } %d < n < %d\right\}" % (a, b)
        giai = r"The primes greater than $%d$ and less than $%d$ are $%s$." % (a, b, "; ".join(map(str, dung)))
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
        giai = (r"The %s numbers $x$ satisfying $%d %s x %s %d$ are $%s$."
                % ("natural" if tap_so == r"\mathbb{N}" else "integer", a, dt, dp, b, "; ".join(map(str, dung))))
        return de, dung, sai, giai
    if loai == 2:
        k = random.choice([12, 18, 20, 24, 28, 30, 36, 40])
        dung = [d for d in range(1, k + 1) if k % d == 0]
        sai = [dung[1:-1], dung[1:], [d for d in dung if d != k], [k * i for i in range(1, 5)]]
        de = r"\left\{n \in \mathbb{N} \mid n \text{ is a divisor of } %d\right\}" % k
        giai = r"The natural divisors of $%d$ are $%s$ (including $1$ and $%d$)." % (k, "; ".join(map(str, dung)), k)
        return de, dung, sai, giai
    if loai == 3:
        k = random.choice([5, 9, 10, 16, 17, 20, 25])
        dung = [x_ for x_ in range(-10, 11) if x_ * x_ < k]
        sai = [[v for v in dung if v >= 0], [x_ for x_ in range(-10, 11) if x_ * x_ <= k],
               [x_ for x_ in range(-10, 11) if abs(x_) < k and abs(x_) <= 5][:0] or list(range(0, k)),
               [v for v in dung if v > 0]]
        de = r"\left\{x \in \mathbb{Z} \mid x^2 < %d\right\}" % k
        can = math.isqrt(k - 1)
        giai = (r"$x^2 < %d$ for integer $x$ $\Leftrightarrow |x| \le %d$, so $x \in \left\{%s\right\}$."
                % (k, can, "; ".join(map(str, dung))))
        return de, dung, sai, giai
    # Phương trình tích trên N, Z, Q, R (giáo án ghi mức B - thông hiểu) KHÔNG
    # đưa vào đây vì NB017 chỉ là mức nhận biết. Bản HẠ MỨC theo cô Lan (2-3 nhân
    # tử, chỉ bậc nhất) ở _tap_dac_trung_4 bên dưới (30/09/2026).
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
        de, dung, sai, giai = _chon_tap_dac_trung()   # loai 0-3 cu + phuong trinh tich don gian, hai dieu kien tren N
        dap = "$%s$" % _tap(dung)
        ung = []
        for s_ in sai:
            t_ = "$%s$" % _tap(s_)
            if t_ != dap and t_ not in ung:
                ung.append(t_)
        if len(ung) < 3:
            continue
        so += 1
        debai = r"Listing the elements of the set $A = %s$, we get" % de
        cauTN += MC_SA_answer_text(debai, "$A = %s$" % _tap(dung), ["$A = %s$" % t_[1:-1] for t_ in ung[:3]],
                                   giai + r" Therefore $A = %s$." % _tap(dung), 0, 0, dang)
    return cauTN


def _tap_rong_hay_khong():
    """(đề tập hợp, rỗng hay không, lí do) - do Python kiểm tra."""
    loai = random.randint(1, 5)   # không dùng Delta: NB017 chỉ là mức nhận biết
    if loai == 1:
        k = random.choice([2, 3, 5, 6, 7, 4, 9, 16, 25])
        chinh = math.isqrt(k) ** 2 == k
        return (r"\left\{x \in \mathbb{Q} \mid x^2 = %d\right\}" % k, not chinh,
                (r"$x = \pm %d$ is a rational number" % math.isqrt(k)) if chinh else
                (r"$x = \pm\sqrt{%d}$ is an irrational number" % k))
    if loai == 2:
        a_ = random.randint(2, 6)
        b_ = random.choice([i for i in range(-15, 16) if i])
        chia = b_ % a_ == 0
        return (r"\left\{x \in \mathbb{Z} \mid %dx %s %d = 0\right\}" % (a_, "+" if b_ > 0 else "-", abs(b_)),
                not chia, r"the solution $x = %s$ %s an integer" % (_tex_so(Rational(-b_, a_)), "is" if chia else "is not"))
    if loai == 3:
        k = random.randint(1, 3)
        return (r"\left\{x \in \mathbb{Z} \mid |x| < %d\right\}" % k, False, r"$x = 0$ satisfies the condition")
    if loai == 4:
        a_ = random.randint(-5, 8)
        if random.random() < 0.5:
            return (r"\left\{x \in \mathbb{Z} \mid %d < x < %d\right\}" % (a_, a_ + 1), True,
                    r"there is no integer between the two consecutive integers $%d$ and $%d$" % (a_, a_ + 1))
        return (r"\left\{x \in \mathbb{R} \mid %d < x < %d\right\}" % (a_, a_ + 1), False,
                r"for example, $x = %s$ satisfies the condition" % _tex_so(Rational(2 * a_ + 1, 2)))
    k = random.randint(1, 9)
    if random.random() < 0.5:
        return (r"\left\{x \in \mathbb{N} \mid x < 0\right\}", True, r"no natural number is negative")
    return (r"\left\{x \in \mathbb{N} \mid x < %d\right\}" % k, False, r"$x = 0$ satisfies the condition")


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
        debai = r"Which of the following sets %s?" % ("is the empty set" if hoi_rong else r"is \textbf{not} the empty set")
        giai = (r"$%s$ %s because %s.\\ " % (chon[0], r"$= \varnothing$" if hoi_rong else r"$\ne \varnothing$", chon[2])
                + r"\\ ".join(r"$%s$ %s because %s." % (d_, r"$= \varnothing$" if r_ else r"$\ne \varnothing$", l_)
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
        debai = (r"Given two sets $A = %s$ and $B = %s$. The set $M$ with the most elements satisfying $M \subset A$ and $M \subset B$ is" % (_tap(A), _tap(B)))
        giai = (r"$M \subset A$ and $M \subset B$ mean that every element of $M$ belongs to both $A$ and $B$, that is, $M \subset A \cap B = %s$. The set $M$ with the most elements is $M = A \cap B = %s$."
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
        debai = (r"Given two sets $A = %s$ and $B = %s$, where $m$ is a parameter. How many integers $m$ satisfy $A \cap B = A$?" % (A_tex, B_tex))
        lo = a if dau_l == r"\ge" else a + 1
        hi = b - k if dau_r == r"\le" else b - k - 1
        giai = (r"$A \cap B = A \Leftrightarrow A \subset B \Leftrightarrow \begin{cases} m %s %d \\ m + %d %s %d \end{cases} \Leftrightarrow %d \le m \le %d$ (for integer $m$).\\ There are $%d - (%d) + 1 = %d$ integers $m$."
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
        debai = (r"Given the set $A = \left\{x \in \mathbb{Z} \mathrel{\Big|} \dfrac{%s}{%s} \in \mathbb{Z}\right\}$ and $B = \left\{x \in \mathbb{R} \mid %s = 0\right\}$, where $m$ is a parameter. Determine whether each of the following statements is true or false:"
                 % (tu, mau, (r"(x - m)(x %s %d)" % ("-" if r > 0 else "+", abs(r))) if r else r"x(x - m)"))
        tach = r"\dfrac{%s}{%s} = 1 + \dfrac{%d}{%s}" % (tu, mau, d, mau)
        # a) NB
        y1 = [(r"{\True $%d \in A$}" % (c + 1),
               r"True. For $x = %d$: $\dfrac{%d}{1} = %d \in \mathbb{Z}$." % (c + 1, c + 1 + k, c + 1 + k)),
              (r"{$%d \in A$}" % c, r"False. For $x = %d$ the denominator equals $0$, so the expression is undefined." % c)]
        # b) TH
        ly_b = (r"$%s$, so $x %s %d$ is a divisor of $%d$: $x %s %d \in \left\{%s\right\}$, hence $A = %s$."
                % (tach, "-" if c > 0 else "+", abs(c), d, "-" if c > 0 else "+", abs(c),
                   "; ".join(str(v) for v in sorted([-u for u in uoc] + uoc)), _tap(A)))
        y2 = [(r"{\True $A = %s$}" % _tap(A), r"True. " + ly_b),
              (r"{$A = %s$}" % _tap([c + u for u in uoc]), r"False (the negative divisors are missing). " + ly_b)]
        # c) VD
        y3 = [(r"{\True The set $A$ has exactly $%d$ subsets}" % (2 ** N),
               r"True. $A$ has $%d$ elements, so it has $2^{%d} = %d$ subsets." % (N, N, 2 ** N)),
              (r"{The set $A$ has exactly $%d$ subsets}" % (2 ** N - 1),
               r"False. $A$ has $%d$ elements, so it has $2^{%d} = %d$ subsets (including $\varnothing$ and $A$)." % (N, N, 2 ** N))]
        # d) VDC
        ly_d = (r"$B = \left\{%d; m\right\}$ (or $B = \left\{%d\right\}$ when $m = %d$). Since $%d \in A$, we have $B \subset A \Leftrightarrow m \in A$: there are $%d$ integers $m$." % (r, r, r, r, N))
        y4 = [(r"{\True There are exactly $%d$ integers $m$ for which $B \subset A$}" % N, r"True. " + ly_d),
              (r"{There are exactly $%d$ integers $m$ for which $B \subset A$}" % (N - 1),
               r"False (the case $m = %d$ is missed). " % r + ly_d)]
        # Bổ sung 01/10/2026: mỗi ý nhiều phát biểu đúng, nhiều phát biểu sai (cô Lan)
        ly_a2 = r"$x \in A \Leftrightarrow x %s %d$ is a divisor of $%d$ (integer divisors: $%s$)." % (
            "-" if c > 0 else "+", abs(c), d, "; ".join(str(v) for v in sorted([-u for u in uoc] + uoc)))
        ngoai = [c + w for w in range(2, d) if d % w] + [c - w for w in range(2, d) if d % w]
        _tf_them(y1, [(r"$%d \in A$" % (c + u), ly_a2) for u in random.sample(uoc, min(2, len(uoc)))]
                 + [(r"$%d \in A$" % (c - u), ly_a2) for u in random.sample(uoc, 1)] + [(r"$%d \notin A$" % c, ly_a2)],
                 [(r"$%d \in A$" % v, ly_a2) for v in random.sample(ngoai, min(2, len(ngoai)))]
                 + [(r"$%d \notin A$" % (c - 1), ly_a2), (r"$%d \notin A$" % (c + d), ly_a2)])
        _tf_them(y2, [(r"The set $A$ has exactly $%d$ elements" % N, ly_b), (r"$%d \in A$ and $%d \in A$" % (c + d, c - d), ly_b),
                      (r"The sum of the elements of $A$ equals $%d$" % sum(A), ly_b)],
                 [(r"The set $A$ has exactly $%d$ elements" % (N // 2), ly_b), (r"$A = %s$" % _tap(A + [c]), ly_b),
                  (r"The sum of the elements of $A$ equals $%d$" % (sum(A) + c), ly_b)])
        ly_c2 = r"$A$ has $%d$ elements, so it has $2^{%d} = %d$ subsets (including $\varnothing$ and $A$)." % (N, N, 2 ** N)
        _tf_them(y3, [(r"The set $A$ has exactly $%d$ subsets other than $\varnothing$" % (2 ** N - 1), ly_c2),
                      (r"The set $A$ has exactly $%d$ subsets consisting of a single element" % N, ly_c2)],
                 [(r"The set $A$ has exactly $%d$ subsets" % (2 ** (N - 1)), ly_c2),
                  (r"The set $A$ has exactly $%d$ subsets other than $\varnothing$" % (2 ** N), ly_c2),
                  (r"The set $A$ has exactly $%d$ subsets" % (N * N), ly_c2)])
        d4, s4 = _tf_dem(r"%s $%d$ integers $m$ for which $B \subset A$", N, ly_d, [N - 1, N + 1, N // 2])
        _tf_them(y4, d4, s4)
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
        debai = (r"Given the set $E = %s$ and the subsets $A = %s$, $B = %s$ of $E$. The set $%s$ is"
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
        debai = (r"Given two sets $A$, $B$ satisfying $A \setminus B = %s$, $B \setminus A = %s$ and $A \cap B = %s$. The set $%s$ is" % (_tap(AB), _tap(BA), _tap(G), hoi))
        cach = {"A": r"(A \setminus B) \cup (A \cap B)", "B": r"(B \setminus A) \cup (A \cap B)",
                r"A \cup B": r"(A \setminus B) \cup (B \setminus A) \cup (A \cap B)"}[hoi]
        giai = (r"Each element of $A \cup B$ belongs to exactly one of three disjoint parts: only in $A$, only in $B$, or in both. Hence $%s = %s = %s$." % (hoi, cach, _tap(kq)))
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
        debai = r"Given two sets $A = %s$ and $B = %s$. The set $%s$ is" % (deA, deB, ten)
        viet_lai = []
        if lai_A:
            viet_lai.append(r"$A = %s$" % lai_A)
        if lai_B:
            viet_lai.append(r"$B = %s$" % lai_B)
        giai = ((r"Rewrite: " + ", ".join(viet_lai) + r".\\ " if viet_lai else "")
                + r"Representing $A$, $B$ on the number line, we get $%s = %s$." % (ten, _k_tex(kq)))
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
        de = (r"Given two nonempty sets $A = \left(%s;\ %d\right]$ and $B = \left(%d;\ %s\right)$, where $m$ is a real parameter. Find all values of $m$ such that $A \cap B \ne \varnothing$." % (mp, a, b, km))
        dk = [r"%s < %d" % (mp, a), r"%s > %d" % (km, b)] + ([r"%s < %s" % (mp, km)] if k == 2 else [])
        giai = (r"Both sets are nonempty and their intersection is nonempty when $\begin{cases} %s \end{cases}$ (since $%d < %d$, only these conditions remain) $\Leftrightarrow %s < m < %s$." % (r" \\ ".join(dk), b, a, _k_so(L), _k_so(U)))
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
        de = (r"Given two sets $A = \left(-\infty;\ %s\right%s$ and $B = \left%s%d;\ +\infty\right)$. Find all values of the parameter $m$ such that $A \cup B = \mathbb{R}$."
              % (mp, "]" if dA else ")", "[" if dB else "(", q))
        giai = (r"$A \cup B = \mathbb{R} \Leftrightarrow %s %s %d$ (%s) $\Leftrightarrow m %s %d$."
                % (mp, dau, q, "only one of the two endpoints needs to be included" if dau == r"\ge" else
                   r"neither endpoint is included, so the sets must overlap", dau, t))
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
        de = (r"Given two sets $A = \left(-\infty;\ m\right%s$ and $B = \left[%s;\ %s\right]$. Find all values of the parameter $m$ such that $A \cap B = \varnothing$." % ("]" if dong else ")", ka(a), ka(b)))
        giai = (r"$A \cap B = \varnothing \Leftrightarrow m %s %s \Leftrightarrow %s %s %d \Leftrightarrow m %s %s$."
                % ("<" if dong else r"\le", ka(a), "m" if k == 2 else "%dm" % (k - 1), ">" if dong else r"\ge", -a, dau, _k_so(t)))
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
    de = (r"Given two sets $A = \left%sm;\ m + %d\right%s$ and $B = \left%s%d;\ %d\right%s$. Find all values of the parameter $m$ such that $A \cap B \ne \varnothing$."
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


_BOI_CANH_HAI_MON = [("Class 10A", "students", "good at Literature", "good at Math", "not a top student in either subject"),
                     ("A class", "students", "can play volleyball", "can play soccer",
                      "cannot play either of the two sports"),
                     ("A group of tourists", "people", "have visited Hue", "have visited Hoi An",
                      "have visited neither of the two places")]


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
            debai = r"The set $A = %s$ is equal to which of the following sets?" % _k_bdt(*K)
            giai = r"$A = %s = %s$." % (_k_bdt(*K), _k_tex(S))
        else:
            dap = "$%s$" % _k_bdt(*K)
            ung = list(dict.fromkeys("$%s$" % _k_bdt(*S2[0]) for S2 in cac))
            ung = [u for u in ung if u != dap]
            random.shuffle(ung)
            ung = ung[:3]
            debai = r"The set $A = %s$ written in set-builder notation is" % _k_tex(S)
            giai = (r"Square bracket: the endpoint is included (symbols $\le$, $\ge$); parenthesis: the endpoint is not included (symbols $<$, $>$). Therefore $A = %s$." % _k_bdt(*K))
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
        debai = (r"Given the open sentence $P(x)$: ``$x + %d %s x^2$'' with $x \in \mathbb{R}$. Which of the following statements is %s?" % (k, dt, "true" if hoi_dung else r"\textbf{false}"))
        dong = []
        for v in sorted([chon] + khac):
            ok = fn(v + k, v * v)
            dong.append(r"$P(%d)$: $%s + %d %s %s$, that is, $%d %s %d$ (%s)"
                        % (v, "(%d)" % v if v < 0 else "%d" % v, k, dt, ("(%d)^2" % v) if v < 0 else "%d^2" % v,
                           v + k, dt, v * v, "true" if ok else "false"))
        giai = r"Substitute directly: " + r"; ".join(dong) + r". Therefore choose $P(%d)$." % chon
        cauTN += MC_SA_answer_text(debai, "$P(%d)$" % chon, ["$P(%d)$" % v for v in khac], giai, 0, 0, dang)
    return cauTN


def _md_luong_tu():
    """Một mệnh đề có ∀/∃ trên tập số, kèm chân trị và lí do (tham số do Python chọn)."""
    loai = random.randint(0, 8)
    k = random.randint(2, 9)
    if loai == 0:
        return (r"\exists n \in \mathbb{N},\ n^2 = %dn" % k, True, r"for $n = %d$, $%d^2 = %d\cdot %d$" % (k, k, k, k))
    if loai == 1:
        if random.random() < .5:
            return (r"\forall n \in \mathbb{N},\ n^2 > 0", False, r"for $n = 0$, $n^2 = 0$")
        return (r"\forall n \in \mathbb{N}^*,\ n^2 > 0", True, r"$n \ge 1$, so $n^2 \ge 1 > 0$")
    if loai == 2:
        return (r"\forall n \in \mathbb{N},\ n^2 + 1 \text{ is odd}", False, r"for $n = 1$, $n^2 + 1 = 2$ is even")
    if loai == 3:
        c = random.choice([2, 3, 5, 6, 7, 4, 9, 16, 25, 36])
        s = math.isqrt(c)
        dung = s * s == c
        return (r"\exists n \in \mathbb{N},\ n^2 - %d = 0" % c, dung,
                (r"for $n = %d$" % s) if dung else (r"$n^2 = %d$ cho $n = \sqrt{%d} \notin \mathbb{N}$" % (c, c)))
    if loai == 4:
        return (r"\forall n \in \mathbb{N},\ n^2 + n \text{ is divisible by } 2", True,
                r"$n^2 + n = n(n + 1)$ is the product of two consecutive natural numbers")
    if loai == 5:
        if random.random() < .5:
            return (r"\forall n \in \mathbb{N},\ n^2 \ge n", True, r"$n^2 - n = n(n - 1) \ge 0$ for natural $n$")
        return (r"\forall x \in \mathbb{R},\ x^2 \ge x", False,
                r"for $x = \dfrac{1}{2}$, $x^2 = \dfrac{1}{4} < \dfrac{1}{2}$")
    if loai == 6:
        a_ = random.randint(2, 6)
        b_ = random.choice([i for i in range(-15, 16) if i])
        dung = b_ % a_ == 0
        return (r"\exists n \in \mathbb{Z},\ %dn = %d" % (a_, b_), dung,
                r"$n = %s$ %s an integer" % (_tex_so(Rational(b_, a_)), "is" if dung else "is not"))
    if loai == 7:
        c = random.randint(1, 9)
        if random.random() < .5:
            return (r"\forall x \in \mathbb{R},\ x^2 + %d > 0" % c, True, r"$x^2 + %d \ge %d > 0$" % (c, c))
        return (r"\forall x \in \mathbb{R},\ x^2 - %d > 0" % c, False, r"for $x = 0$, $x^2 - %d = -%d < 0$" % (c, c))
    m = random.randint(2, 9)
    c = m * (m + 1) if random.random() < .5 else m * (m + 1) + 1
    s = next((t for t in range(0, 20) if t * t + t == c), None)
    return (r"\exists n \in \mathbb{N},\ n^2 + n = %d" % c, s is not None,
            (r"for $n = %d$" % s) if s is not None else
            (r"$n^2 + n = n(n + 1)$ is always even but $%d$ is odd" % c if c % 2 else r"no $n$ satisfies it"))




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
    ly = (r"$%s$ %s, $%s$ %s" % (P_tex, "true" if P_dung else "false", Q_tex, "true" if Q_dung else "false")
          + (r", so the biconditional statement is %s" % ("true" if dung else "false") if tuong_duong else
             r", so the conditional statement is %s" % ("true" if dung else "false (P is true, Q is false)" if not dung else "true")))
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
        debai = r"Which of the following statements is %s?" % ("true" if hoi_dung else r"\textbf{false}")
        giai = (r"The statement $P \Rightarrow Q$ is false only when $P$ is true and $Q$ is false; $P \Leftrightarrow Q$ is true when $P$, $Q$ are both true or both false.\\ " + r"\\ ".join(r"$%s$: %s." % (t, l) for t, _, l in [chon] + cung))
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
        debai = (r"Given three sets $A = %s$, $B = %s$ and $C = %s$. The set $%s$ is"
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
        giai = ((r"We have " + ", ".join(trung) + r".\\ " if trung else "")
                + r"Representing on the number line, we get $%s = %s$%s." % (ten, _k_tex(kq),
                                                                   (r" $= %s$" % _k_bdt(*kq[0])) if bdt else ""))
        cauTN += MC_SA_answer_text(debai, dap, ung, giai, 0, 0, dang)
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


# =====================================================================
# THÊM DẠNG CHO L10_C1_B1_VD014 (30/09/2026)
# ---------------------------------------------------------------------
# Bài 1 chỉ có MỘT đơn vị mức VD (VD014 - Curriculum của Bộ, không thêm
# được đơn vị mới). Đề có VD ở bài 1 cho cả MC, SA, TL thì cả ba câu đều là
# VD014, nên cần NHIỀU DẠNG khác hẳn nhau (cô Lan: "làm thêm VD của bài 1").
#   SA_B  đếm số mệnh đề đúng / số n làm mệnh đề kéo theo sai
#   MC_D  tham số để mệnh đề kéo theo chứa kí hiệu với mọi là mệnh đề đúng
#   TL_B  lập mệnh đề phủ định của mệnh đề chứa kí hiệu với mọi, tồn tại và xét đúng sai
# Mỗi dạng có _01 và _02 hỏi theo cách khác (docs/27).
# =====================================================================

def _md_luong_tu_vd():
    """Một mệnh đề chứa kí hiệu với mọi / tồn tại, sinh ngẫu nhiên, kèm tính đúng
    sai và lí do (tính bằng Python)."""
    k = random.choice([1, 2, 3, 4, 5])
    a = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    s = random.choice([2, 4, 6])
    m = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16])
    kieu = random.randrange(8)
    if kieu == 0:
        tex = r"\forall x \in \mathbb{R},\ x^{2} + %d > 0" % a if a > 0 else \
              r"\forall x \in \mathbb{R},\ x^{2} - %d > 0" % (-a)
        dung = a > 0
        ly = (r"$x^{2} \ge 0$, so $x^{2} + %d > 0$ for all $x$" % a) if a > 0 else \
             (r"for $x = 0$, $0 - %d < 0$" % (-a))
    elif kieu == 1:
        tex = r"\exists x \in \mathbb{R},\ x^{2} = %d" % a
        dung = a >= 0
        ly = (r"take $x = \sqrt{%d}$" % a) if a >= 0 else r"$x^{2} \ge 0 > %d$ for all $x$" % a
    elif kieu == 2:
        tex = r"\forall x \in \mathbb{R},\ x^{2} - %dx + %d \ge 0" % (s, (s // 2) ** 2)
        dung = True
        ly = r"$x^{2} - %dx + %d = \left(x - %d\right)^{2} \ge 0$" % (s, (s // 2) ** 2, s // 2)
    elif kieu == 3:
        tex = r"\exists n \in \mathbb{N},\ n^{2} = %d" % m
        r = math.isqrt(m)
        dung = r * r == m
        ly = (r"$n = %d$" % r) if dung else (r"$%d^{2} < %d < %d^{2}$" % (r, m, r + 1))
    elif kieu == 4:
        tex = r"\forall n \in \mathbb{N},\ n\left(n + 1\right) \text{ is divisible by } %d" % random.choice([2, 3])
        d = int(tex.split("by } ")[1])
        dung = d == 2
        ly = (r"$n$, $n + 1$ are two consecutive natural numbers, so one of them is even") if dung else \
             r"for $n = 1$, $n\left(n + 1\right) = 2$ is not divisible by $3$"
    elif kieu == 5:
        tex = r"\exists n \in \mathbb{N},\ n^{2} + n + 1 \text{ is divisible by } 2"
        dung = False
        ly = r"$n^{2} + n = n\left(n + 1\right)$ is always even, so $n^{2} + n + 1$ is always odd"
    elif kieu == 6:
        tex = r"\forall x \in \mathbb{R},\ x > %d \Rightarrow x^{2} > %d" % (a, a * a)
        dung = a >= 0
        ly = (r"$x > %d \ge 0$, so $x^{2} > %d$" % (a, a * a)) if a >= 0 else \
             (r"for $x = 0 > %d$, $x^{2} = 0 \not> %d$" % (a, a * a))
    else:
        tex = r"\forall n \in \mathbb{N},\ n\left(n + 1\right)\left(n + 2\right) \text{ is divisible by } %d" % random.choice([6, 4])
        d = int(tex.split("by } ")[1])
        dung = d == 6
        ly = (r"the product of three consecutive natural numbers is divisible by both $2$ and $3$") if dung else \
             r"for $n = 1$, the product equals $6$, which is not divisible by $4$"
    return kieu, tex, dung, ly


def L10_C1_B1_VD014_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - cho bốn mệnh đề chứa kí hiệu $\forall$, $\exists$ (cả trên
    $\mathbb{R}$ và $\mathbb{N}$, có mệnh đề kéo theo); hỏi có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 30/09/2026 - dang moi cho VD014 (khac SA_A: SA_A tim tham so;
    SA_B dem so menh de dung). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ds, kieu_da = [], set()
        while len(ds) < 4:
            k, tex, dung, ly = _md_luong_tu_vd()
            if k in kieu_da:
                continue
            kieu_da.add(k)
            ds.append((tex, dung, ly))
        dap = str(sum(1 for _, d, _ in ds if d))
        # tra loi ngan khong duoc dung \item (khoa cua math_type) - danh so 1., 2., ... bang tay
        debai = (r"Given the following statements:" + "\\\\\n" +
                 "\\\\\n".join(r"%d. $%s$." % (i + 1, t) for i, (t, _, _) in enumerate(ds)) + "\\\\\n" +
                 r"How many of the statements are true?")
        giai = "\\\\\n".join(r"%d. %s because %s." % (i + 1, r"\textbf{True}" if d else r"\textbf{False}", ly)
                             for i, (t, d, ly) in enumerate(ds)) + "\\\\\n" + r"Therefore, the number of true statements is $%s$." % dap
        nhieu = [str(x) for x in range(5) if str(x) != dap]
        cau += MC_SA_answer_const(debai, dap, nhieu, giai, 0, 0, dang)
    return cau


def L10_C1_B1_VD014_SA_B_02(socau, dang=2):
    r"""Trả lời ngắn - hỏi theo cách khác của _01: cho hai mệnh đề chứa biến về
    chia hết, đếm số $n$ trong một đoạn làm cho mệnh đề KÉO THEO sai
    (kéo theo sai khi $P$ đúng mà $Q$ sai).

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD014_SA_B. Co Lan duyet lai.
    """
    CAP = [(a, b) for a in (2, 3, 4, 5, 6) for b in (3, 4, 6, 8, 9, 10, 12) if b % a != 0 and a % b != 0]
    cau = ""
    for _ in range(socau):
        a, b = random.choice(CAP)
        if random.random() < 0.5:
            a, b = b, a
        N = random.choice([30, 40, 50, 60, 100])
        so_P = N // a
        so_PQ = N // (a * b // math.gcd(a, b))
        dap = str(so_P - so_PQ)
        lcm = a * b // math.gcd(a, b)
        debai = (r"Given the statements $P(n)$: ``$n$ is divisible by $%d$'' and $Q(n)$: ``$n$ is divisible by $%d$'' where $n$ is a positive integer. How many positive integers $n \le %d$ make the conditional statement $P(n) \Rightarrow Q(n)$ \textbf{false}?" % (a, b, N))
        giai = (r"$P(n) \Rightarrow Q(n)$ is false if and only if $P(n)$ is true and $Q(n)$ is false, that is, $n$ is divisible by $%d$ but not divisible by $%d$." % (a, b) + "\\\\\n" +
                r"The number of $n \le %d$ divisible by $%d$ is $%d$; among them, the number divisible by both $%d$ and $%d$ (that is, divisible by $%d$) is $%d$." % (N, a, so_P, a, b, lcm, so_PQ) + "\\\\\n" +
                r"Therefore, there are $%d - %d = %s$ such numbers." % (so_P, so_PQ, dap))
        nhieu = [str(so_P), str(so_PQ), str(N - so_P), str(N // b)]
        cau += MC_SA_answer_const(debai, dap, [x for x in dict.fromkeys(nhieu) if x != dap] + ["0", "1"],
                                  giai, 0, 0, dang)
    return cau


_KEO_THEO_THAM_SO = [
    # (dang tex voi m, c; dieu kien dung theo m; ly do)
    (r"x > m \Rightarrow x > %d", lambda m, c: m >= c, r"every $x > m$ is greater than $%d$ if and only if $m \ge %d$"),
    (r"x < m \Rightarrow x < %d", lambda m, c: m <= c, r"every $x < m$ is less than $%d$ if and only if $m \le %d$"),
    (r"x > %d \Rightarrow x > m", lambda m, c: m <= c, r"every $x > %d$ is greater than $m$ if and only if $m \le %d$"),
    (r"x \ge m \Rightarrow x > %d", lambda m, c: m > c, r"every $x \ge m$ is greater than $%d$ if and only if $m > %d$"),
    (r"x > m \Rightarrow x \ge %d", lambda m, c: m >= c, r"every $x > m$ is greater than or equal to $%d$ if and only if $m \ge %d$"),
]


def L10_C1_B1_VD014_MC_D_01(socau, dang=1):
    r"""Tham số để mệnh đề KÉO THEO chứa kí hiệu $\forall$ là mệnh đề đúng
    (vd $\forall x \in \mathbb{R},\ x > m \Rightarrow x > 3$): có bao nhiêu giá trị nguyên của $m$.

    CLAUDE THEM 30/09/2026 - dang moi cho VD014 (khac MC_A: MC_A la bat phuong
    trinh bac hai co tham so; MC_D la menh de keo theo). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        mau, dk, ly = random.choice(_KEO_THEO_THAM_SO)
        c = random.randint(-6, 8)
        L, U = random.choice([(-10, 10), (-20, 20), (-15, 15)])
        dem = sum(1 for m in range(L, U + 1) if dk(m, c))
        mde = mau % c
        debai = (r"How many integer values of the parameter $m$ in the closed interval $\left[%d;\ %d\right]$ make the statement ``$\forall x \in \mathbb{R},\ %s$'' true?" % (L, U, mde))
        giai = (r"Observe that %s." % (ly % (c, c)) + "\\\\\n" +
                r"On the interval $\left[%d;\ %d\right]$ there are $%d$ integer values of $m$ that satisfy this condition." % (L, U, dem))
        dung = "$%d$" % dem
        nhieu = _ba_nhieu_dem(dem, [dem + 1, dem - 1, U - L + 1 - dem])
        cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cau


def _ba_nhieu_dem(dap, ung_vien):
    ra = []
    for x in ung_vien + [dap + 2, dap - 2, dap + 3]:
        if x != dap and x >= 0 and "$%d$" % x not in ra:
            ra.append("$%d$" % x)
    return ra[:3]


def L10_C1_B1_VD014_MC_D_02(socau, dang=1):
    r"""Cách hỏi khác của _01: mệnh đề kéo theo về CHIA HẾT chứa tham số
    ($\forall n \in \mathbb{N},\ n \text{ chia hết cho } m \Rightarrow n \text{ chia hết cho } c$
    đúng khi $m$ là bội của $c$); đếm số $m$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD014_MC_D. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        c = random.choice([2, 3, 4, 5, 6])
        N = random.choice([30, 40, 50, 60])
        nguoc = random.random() < 0.5
        if nguoc:
            # n chia het cho c => n chia het cho m  dung khi m la uoc cua c
            dem = sum(1 for m in range(1, N + 1) if c % m == 0)
            mde = r"n \text{ is divisible by } %d \Rightarrow n \text{ is divisible by } m" % c
            ly = (r"The statement is true if and only if every multiple of $%d$ is a multiple of $m$, that is, $m$ is a divisor of $%d$." % (c, c)
                  + "\\\\\n" + r"$%d$ has $%d$ positive divisors." % (c, dem))
        else:
            dem = N // c
            mde = r"n \text{ is divisible by } m \Rightarrow n \text{ is divisible by } %d" % c
            ly = (r"The statement is true if and only if every multiple of $m$ is divisible by $%d$, that is, $m$ is divisible by $%d$."
                  % (c, c) + "\\\\\n" + r"From $1$ to $%d$ there are $%d$ numbers divisible by $%d$." % (N, dem, c))
        debai = (r"How many positive integers $m \le %d$ make the statement ``$\forall n \in \mathbb{N},\ %s$'' true?" % (N, mde))
        dung = "$%d$" % dem
        nhieu = _ba_nhieu_dem(dem, [N - dem, dem + 1, N // (c + 1)])
        cau += MC_SA_answer_text(debai, dung, nhieu, ly, 0, 0, dang)
    return cau


def L10_C1_B1_VD014_TL_B_01(socau, dong=1):
    r"""Tự luận - lập mệnh đề PHỦ ĐỊNH của mệnh đề chứa kí hiệu $\forall$ (bất
    đẳng thức có tham số cụ thể) và xét tính đúng sai của mệnh đề phủ định.

    CLAUDE THEM 30/09/2026 - dang moi cho VD014 (khac TL_A: TL_A la keo theo va
    menh de dao). Co Lan duyet lai.
    """
    DAU = {">": r"\le", r"\ge": "<", "<": r"\ge", r"\le": ">"}
    cau = ""
    for _ in range(socau):
        s = random.choice([2, 4, 6])
        h = s // 2
        a = random.randint(-3, h * h + 3)
        dau = random.choice([">", r"\ge"])
        # x^2 - s x + a = (x - h)^2 + a - h^2
        du = a - h * h
        P_dung = du > 0 if dau == ">" else du >= 0
        P = r"\forall x \in \mathbb{R},\ x^{2} - %dx %s %d %s 0" % (s, "+" if a >= 0 else "-", abs(a), dau)
        Pbar = r"\exists x \in \mathbb{R},\ x^{2} - %dx %s %d %s 0" % (s, "+" if a >= 0 else "-", abs(a), DAU[dau])
        debai = r"Given the statement $P$: ``$%s$''." % P
        bien_doi = r"$x^{2} - %dx %s %d = \left(x - %d\right)^{2}%s$" % (
            s, "+" if a >= 0 else "-", abs(a), h, "" if du == 0 else (" %s %d" % ("+" if du > 0 else "-", abs(du))))
        ds = [
            (r"State the negation $\overline{P}$.", r"\overline{P}\colon %s" % Pbar,
             r"The negation of ``$\forall x, A(x)$'' is ``$\exists x, \overline{A(x)}$'', so $\overline{P}$: ``$%s$''." % Pbar),
            (r"Determine whether the statement $\overline{P}$ is true or false.", r"\text{%s}" % ("False" if P_dung else "True"),
             bien_doi + ". " +
             ((r"Since $\left(x - %d\right)^{2} \ge 0$, the expression is always $%s 0$: $P$ is true, hence $\overline{P}$ is \textbf{false}."
               % (h, dau)) if P_dung else
              (r"For $x = %d$ the expression equals $%d$, which does not satisfy $%s 0$: $P$ is false, hence $\overline{P}$ is \textbf{true}."
               % (h, du, dau)))),
        ]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


def L10_C1_B1_VD014_TL_B_02(socau, dong=1):
    r"""Tự luận - cách hỏi khác của _01: mệnh đề chứa kí hiệu $\exists$ trên
    $\mathbb{N}$ về chia hết; lập mệnh đề phủ định và xét tính đúng sai của cả hai.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD014_TL_B. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        a = random.randint(1, 9)
        k = random.choice([2, 3])
        if k == 2:
            P_dung = a % 2 == 0
            ly = (r"$n^{2} + n = n\left(n + 1\right)$ is always even, so for every $n$ the number $n^{2} + n + %d$ is %s" %
                  (a, "always even" if P_dung else "always odd"))
            bt = r"n^{2} + n + %d" % a
        else:
            # n(n+1)(n+2) chia het cho 3; n^3 - n = (n-1)n(n+1) chia het cho 3
            P_dung = a % 3 == 0
            ly = (r"$n^{3} - n = \left(n - 1\right)n\left(n + 1\right)$ is always divisible by $3$, so $n^{3} - n + %d$ is divisible by $3$ if and only if $%d$ is divisible by $3$" % (a, a))
            bt = r"n^{3} - n + %d" % a
        P = r"\exists n \in \mathbb{N},\ %s \text{ is divisible by } %d" % (bt, k)
        Pbar = r"\forall n \in \mathbb{N},\ %s \text{ is not divisible by } %d" % (bt, k)
        debai = r"Given the statement $P$: ``$%s$''." % P
        ds = [
            (r"State the negation $\overline{P}$.", r"\overline{P}\colon %s" % Pbar,
             r"The negation of ``$\exists n, A(n)$'' is ``$\forall n, \overline{A(n)}$'', so $\overline{P}$: ``$%s$''." % Pbar),
            (r"Determine whether the statement $P$ is true or false.", r"\text{%s}" % ("True" if P_dung else "False"),
             ly + r". Hence $P$ is \textbf{%s}." % ("true" if P_dung else "false")),
            (r"Determine whether the statement $\overline{P}$ is true or false.", r"\text{%s}" % ("False" if P_dung else "True"),
             r"$\overline{P}$ is the negation of $P$, so its truth value is opposite to that of $P$: $\overline{P}$ is \textbf{%s}."
             % ("false" if P_dung else "true")),
        ]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


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

        debai = f"The sports club has {x} students who like soccer, {y} students who like table tennis, and {z} students who like badminton. {ab} students like both soccer and table tennis, {bc} students like both table tennis and badminton, {ac} students like both soccer and badminton, and {abc} students like all three sports."

        # Code TikZ cho biểu đồ Venn 3 tập hợp
        tikz_venn = f"""
        \\begin{{tikzpicture}}
            \\def\\firstcircle{{(0,0) circle (1.5cm)}}
            \\def\\secondcircle{{(60:2cm) circle (1.5cm)}}
            \\def\\thirdcircle{{(0:2cm) circle (1.5cm)}}
            \\draw \\firstcircle node[below left] {{SC}};
            \\draw \\secondcircle node[above] {{TT}};
            \\draw \\thirdcircle node[below right] {{BD}};
            \\node at (1,0.6) {{{abc}}}; 
            \\node at (-0.3,0.3) {{{m}}};
            \\node at (2.3,0.3) {{{p}}};
            \\node at (1,1.5) {{{n}}};
        \\end{{tikzpicture}}"""

        hoi_a = f"Draw a Venn diagram representing the sets above."
        giai_a = f"The Venn diagram drawn with TikZ is as follows: \\n {tikz_venn}"

        hoi_b = f"Compute the total number of students who like exactly one sport."
        dap_b = m + n + p
        giai_b = f"The total number of students who like only one sport is: $S = {m} + {n} + {p} = {dap_b}$."

        ds_abcd = [
            (hoi_a, "\\text{Figure}", giai_a),
            (hoi_b, dap_b, giai_b)
        ]

        cauTL += TL_answer_text(debai, ds_abcd, 0, 0, dong)

    return cauTL


# =====================================================================
# BÀI TOÁN THỰC TẾ HAI TẬP HỢP - KHO BỐI CẢNH (cô Lan 30/09/2026)
# ---------------------------------------------------------------------
# Lời dẫn tự chọn ngẫu nhiên trong nhiều lĩnh vực để đề không nhàm chán.
# TRONG MỘT ĐỀ (một mã đề) các câu dùng kho này KHÔNG trùng bối cảnh:
# generator_service gán _DE_HIEN_TAI.da_dung = tập bối cảnh đã dùng của mã đề
# đang sinh (xem docs/27 mục 8). Chạy lẻ (nháp) thì mỗi lần gọi hàm tự không
# lặp bối cảnh giữa các câu của chính nó.
#
# Mỗi bối cảnh: mo (lời mở đầu, %(N)d, %(lop)s), dv (đơn vị), tap (tập hợp ...),
# cap = [(A, B, động từ chung, động từ phủ định, loại)], tỉ lệ n(A), n(B), phần
# giao (theo tập nhỏ hơn) để số liệu HỢP LÍ; mo_an + hoi_tong nếu dùng được cho
# câu hỏi "có tất cả bao nhiêu" (tổng số chưa biết).
# =====================================================================
import threading

_DE_HIEN_TAI = threading.local()

_LOP_CHV = ["10C1A", "10C1B", "10C2A", "10C2B", "10C3A", "10C3B", "10C4", "10C5A", "10C5B", "10C6", "10C7",
            "10C8", "10C9"]
_MO_LOP = r"Class %(lop)s of Hung Vuong Specialized High School has $%(N)d$ students. "

_BOI_CANH_HAI_TAP = [
    {"ten": "doc_sach", "lop": True, "N": [35], "dv": "students", "tap": "students",
     "mo": _MO_LOP + r"In a survey about the class's reading preferences,",
     "cap": [("liked reading comic books", "liked reading novels", "liked", "did not like", "genres"),
             ("liked reading science fiction", "liked reading mystery novels", "liked", "did not like", "genres"),
             ("liked reading books about historical stories", "liked reading books about businesspeople", "liked", "did not like", "types of books"),
             ("liked reading poetry", "liked reading short stories", "liked", "did not like", "genres")],
     "tA": (0.35, 0.65), "tB": (0.3, 0.6), "giao": (0.2, 0.7)},
    {"ten": "mon_hoc", "lop": True, "N": [35], "dv": "students", "tap": "students",
     "mo": _MO_LOP + r"When asked about their favorite school subjects,",
     "cap": [("liked studying Math", "liked studying Literature", "liked", "did not like", "subjects"),
             ("liked studying Physics", "liked studying Chemistry", "liked", "did not like", "subjects"),
             ("liked studying Biology", "liked studying Geography", "liked", "did not like", "subjects"),
             ("liked studying History", "liked studying English", "liked", "did not like", "subjects"),
             ("liked studying Computer Science", "liked studying Technology", "liked", "did not like", "subjects"),
             ("liked studying Math", "liked studying Physics", "liked", "did not like", "subjects")],
     "tA": (0.35, 0.65), "tB": (0.3, 0.6), "giao": (0.2, 0.65)},
    {"ten": "the_thao", "lop": True, "N": [35], "dv": "students", "tap": "students",
     "mo": _MO_LOP + r"In a survey about the students' favorite sports,",
     "cap": [("liked soccer", "liked badminton", "liked", "did not like", "sports"),
             ("liked swimming", "liked chess", "liked", "did not like", "sports"),
             ("liked basketball", "liked volleyball", "liked", "did not like", "sports"),
             ("liked soccer", "liked swimming", "liked", "did not like", "sports")],
     "tA": (0.35, 0.6), "tB": (0.3, 0.55), "giao": (0.2, 0.6)},
    {"ten": "cau_lac_bo", "lop": True, "N": [35], "dv": "students", "tap": "students",
     "mo": _MO_LOP + r"During the school year,",
     "cap": [("participated in the English Club", "participated in the Computer Science Club", "participated in", "did not participate in", "clubs"),
             ("participated in the Math Club", "participated in the Physics Club", "participated in", "did not participate in", "clubs"),
             ("participated in the Music Club", "participated in the Fine Arts Club", "participated in", "did not participate in", "clubs"),
             ("participated in the Music Club", "participated in the Painting Club", "participated in", "did not participate in", "clubs"),
             ("participated in the Painting Club", "participated in the Computer Science Club", "participated in", "did not participate in", "clubs")],
     "tA": (0.3, 0.55), "tB": (0.25, 0.5), "giao": (0.15, 0.5)},
    {"ten": "hoc_luc", "lop": True, "N": [35], "dv": "students", "tap": "students",
     "mo": _MO_LOP + r"At the end of the first semester,",
     "cap": [("scored a final grade of at least $8{,}0$ in Math", "scored a final grade of at least $8{,}0$ in Literature",
              "scored a final grade of at least $8{,}0$ in", "did not score a final grade of at least $8{,}0$ in", "subjects"),
             ("scored a final grade of at least $8{,}0$ in Physics", "scored a final grade of at least $8{,}0$ in Chemistry",
              "scored a final grade of at least $8{,}0$ in", "did not score a final grade of at least $8{,}0$ in", "subjects"),
             ("scored a final grade of at least $8{,}0$ in Math", "scored a final grade of at least $8{,}0$ in English",
              "scored a final grade of at least $8{,}0$ in", "did not score a final grade of at least $8{,}0$ in", "subjects")],
     "tA": (0.4, 0.7), "tB": (0.35, 0.65), "giao": (0.3, 0.8)},
    {"ten": "van_nghe", "lop": True, "N": [35], "dv": "students", "tap": "students",
     "mo": _MO_LOP + r"To celebrate Vietnamese Teachers' Day on November 20, the class takes part in two performances, in which",
     "cap": [("participated in the dance performance", "participated in the group singing performance", "participated in", "did not participate in", "performances"),
             ("participated in the drama performance", "participated in the modern dance performance", "participated in", "did not participate in", "performances")],
     "tA": (0.25, 0.45), "tB": (0.25, 0.45), "giao": (0.1, 0.45)},
    {"ten": "hoa", "lop": False, "N": [80, 100, 120, 150, 200], "dv": "people", "tap": "people",
     "mo": r"In a survey of $%(N)d$ randomly selected women on a pedestrian street in Gia Lai about the type of flower they would like to receive,",
     "mo_an": r"In a survey of a group of randomly selected women on a pedestrian street in Gia Lai about the type of flower they would like to receive,",
     "hoi_tong": r"How many women participated in the survey?",
     "cap": [("liked receiving roses", "liked receiving carnations", "liked receiving", "did not like receiving", "types of flowers"),
             ("liked receiving fresh flowers", "liked receiving dried flowers", "liked receiving", "did not like receiving", "types of flowers"),
             ("liked receiving orchids", "liked receiving sunflowers", "liked receiving", "did not like receiving", "types of flowers")],
     "tA": (0.45, 0.75), "tB": (0.25, 0.5), "giao": (0.1, 0.5)},
    {"ten": "tai_chinh", "lop": False, "N": [100, 120, 150, 200, 250], "dv": "people", "tap": "people",
     "mo": r"In a survey on financial literacy and personal finance management among $%(N)d$ working adults,",
     "mo_an": r"In a survey on financial literacy and personal finance management among a group of working adults,",
     "hoi_tong": r"How many people participated in the survey?",
     "cap": [("had a savings account at a bank", "had stock investments", "had", "did not have", "financial products"),
             ("had a bank account", "had mutual fund investments", "had", "did not have", "financial products"),
             ("had bond investments", "had stock investments", "had", "did not have", "financial products")],
     "tA": (0.5, 0.8), "tB": (0.2, 0.45), "giao": (0.6, 0.95)},
    {"ten": "mang_xa_hoi", "lop": False, "N": [100, 150, 200, 250, 300], "dv": "people", "tap": "people",
     "mo": r"In a survey of $%(N)d$ residents of Pleiku City about social media use,",
     "mo_an": r"In a survey of a group of residents of Pleiku City about social media use,",
     "hoi_tong": r"How many residents participated in the survey?",
     "cap": [("used Zalo", "used Facebook", "used", "did not use", "apps"),
             ("used TikTok", "used YouTube", "used", "did not use", "apps"),
             ("used Facebook", "used TikTok", "used", "did not use", "apps"),
             ("used Zalo", "used TikTok", "used", "did not use", "apps")],
     "tA": (0.55, 0.85), "tB": (0.4, 0.7), "giao": (0.5, 0.9)},
    {"ten": "du_lich", "lop": False, "N": [120, 150, 180, 200, 240], "dv": "tourists", "tap": "tourists",
     "mo": r"In a survey of $%(N)d$ tourists visiting Gia Lai during the holiday,",
     "mo_an": r"In a survey of a group of tourists visiting Gia Lai during the holiday,",
     "hoi_tong": r"How many tourists are in the group?",
     "cap": [("visited Bien Ho Lake", "visited Chu Dang Ya Volcano", "visited", "had not visited", "attractions"),
             ("visited Phu Cuong Waterfall", "visited Minh Thanh Pagoda", "visited", "had not visited", "attractions")],
     "tA": (0.45, 0.75), "tB": (0.3, 0.6), "giao": (0.3, 0.7)},
    {"ten": "do_uong", "lop": False, "N": [60, 80, 100, 120], "dv": "customers", "tap": "customers",
     "mo": r"A breakfast restaurant in Pleiku surveyed $%(N)d$ customers about their favorite drinks. Among them,",
     "mo_an": r"A breakfast restaurant in Pleiku surveyed a group of customers about their favorite drinks. Among them,",
     "hoi_tong": r"How many customers did the restaurant survey?",
     "cap": [("liked drinking coffee", "liked drinking milk tea", "liked", "did not like", "types of drinks"),
             ("liked drinking fruit juice", "liked drinking soy milk", "liked", "did not like", "types of drinks")],
     "tA": (0.4, 0.7), "tB": (0.25, 0.5), "giao": (0.15, 0.5)},
    {"ten": "am_thuc", "lop": False, "N": [80, 100, 120, 150], "dv": "tourists", "tap": "tourists",
     "mo": r"In a survey of $%(N)d$ tourists about the specialty dishes of Gia Lai,",
     "mo_an": r"In a survey of a group of tourists about the specialty dishes of Gia Lai,",
     "hoi_tong": r"How many tourists participated in the survey?",
     "cap": [("liked pho kho (dry pho)", "liked bun mam cua (crab paste noodle soup)", "liked", "did not like", "dishes"),
             ("liked grilled chicken with bamboo-tube sticky rice", "liked bo mot nang (sun-dried beef)", "liked", "did not like", "dishes")],
     "tA": (0.4, 0.7), "tB": (0.3, 0.6), "giao": (0.2, 0.6)},
    {"ten": "nong_nghiep", "lop": False, "N": [80, 100, 120, 150, 200], "dv": "households", "tap": "households",
     "mo": r"In a survey of $%(N)d$ households in a commune of Gia Lai Province,",
     "mo_an": r"In a survey of households in a village in Gia Lai Province,",
     "hoi_tong": r"How many households in that village participated in the survey?",
     "cap": [("grew coffee", "grew black pepper", "grew", "did not grow", "types of crops"),
             ("raised cattle", "raised pigs", "raised", "did not raise", "types of livestock")],
     "tA": (0.45, 0.75), "tB": (0.25, 0.55), "giao": (0.3, 0.7)},
    {"ten": "ngoai_ngu", "lop": False, "N": [50, 60, 80, 100, 120], "dv": "employees", "tap": "employees",
     "mo": r"A travel company has $%(N)d$ employees. Among them,",
     "mo_an": r"At a travel company,",
     "hoi_tong": r"How many employees does the company have?",
     "cap": [("spoke English", "spoke Japanese", "spoke", "did not speak", "foreign languages"),
             ("spoke Chinese", "spoke Korean", "spoke", "did not speak", "foreign languages")],
     "tA": (0.5, 0.8), "tB": (0.15, 0.4), "giao": (0.5, 0.9)},
    {"ten": "thoi_tiet", "lop": False, "N": [30, 60, 90], "dv": "days", "tap": "days",
     "mo": r"Over $%(N)d$ days of an observation period, the Gia Lai Provincial Hydrometeorological Station recorded that",
     "mo_an": r"During an observation period, the Gia Lai Provincial Hydrometeorological Station recorded that",
     "hoi_tong": r"How many days did the observation period last?",
     "cap": [("had rain", "had strong winds", "had", "did not have", "weather phenomena"),
             ("had rain", "had fog", "had", "did not have", "weather phenomena"),
             ("had strong winds", r"had a temperature below $18^{\circ}\mathrm{C}$", "had", "did not have", "weather phenomena")],
     "tA": (0.3, 0.6), "tB": (0.2, 0.5), "giao": (0.2, 0.6)},
    {"ten": "the_duc", "lop": False, "N": [60, 80, 100, 120], "dv": "people", "tap": "people",
     "mo": r"In a survey of $%(N)d$ people who regularly exercise in the morning at Dien Hong Park (Pleiku),",
     "mo_an": r"In a survey of a group of people who regularly exercise in the morning at Dien Hong Park (Pleiku),",
     "hoi_tong": r"How many people participated in the survey?",
     "cap": [("exercise by jogging", "exercise by cycling", "exercise by", "do not exercise by", "methods"),
             ("exercise by doing yoga", "exercise by doing traditional wellness exercises", "exercise by", "do not exercise by", "methods")],
     "tA": (0.4, 0.7), "tB": (0.25, 0.5), "giao": (0.15, 0.5)},
]


def _bo_chon_boi_canh():
    """Trả về hàm chọn bối cảnh CHƯA dùng (trong mã đề đang sinh, hoặc trong lần gọi này)."""
    da_dung = getattr(_DE_HIEN_TAI, "da_dung", None)
    if da_dung is None:
        da_dung = set()

    def chon(dieu_kien=lambda bc: True):
        ung = [bc for bc in _BOI_CANH_HAI_TAP if dieu_kien(bc)]
        chua = [bc for bc in ung if "hai_tap:" + bc["ten"] not in da_dung]
        bc = random.choice(chua or ung)
        da_dung.add("hai_tap:" + bc["ten"])
        return bc
    return chon


def _so_lieu_hai_tap(N, tA, tB, tg, it_nhat_khong=2):
    """n(A), n(B), n(A giao B) hợp lí theo bối cảnh (tỉ lệ từng tập, tỉ lệ phần giao
    theo tập nhỏ hơn), có ít nhất it_nhat_khong người không thuộc tập nào."""
    for _ in range(2000):
        nA = random.randint(max(2, int(N * tA[0])), max(3, int(N * tA[1])))
        nB = random.randint(max(2, int(N * tB[0])), max(3, int(N * tB[1])))
        nho = min(nA, nB)
        lo = max(1, nA + nB - (N - it_nhat_khong), int(nho * tg[0]))
        hi = min(nho - 1, int(nho * tg[1]))
        if lo <= hi:
            return nA, nB, random.randint(lo, hi)
    raise ValueError("khong sinh duoc so lieu")


def _de_hai_tap(chon, dieu_kien=lambda bc: True, an_N=False):
    """Sinh một đề: bối cảnh + số liệu + các cụm từ dùng để hỏi."""
    bc = chon(dieu_kien)
    A, B, dt, phu, loai = random.choice(bc["cap"])
    N = random.choice(bc["N"])
    nA, nB, nAB = _so_lieu_hai_tap(N, bc["tA"], bc["tB"], bc["giao"])
    lop = random.choice(_LOP_CHV) if bc["lop"] else ""
    mo = (bc["mo_an"] if an_N else bc["mo"]) % {"N": N, "lop": lop}
    dv = bc["dv"]
    so_lieu = r"%s$%d$ %s that %s, $%d$ %s that %s, and $%d$ %s that %s both %s" % (
        "" if mo.endswith("recorded that") else "there are ", nA, dv, A, nB, dv, B, nAB, dv, dt, loai)
    return {"bc": bc, "A": A, "B": B, "dt": dt, "phu": phu, "loai": loai, "N": N, "nA": nA, "nB": nB,
            "nAB": nAB, "nAuB": nA + nB - nAB, "khong": N - (nA + nB - nAB), "mo": mo, "dv": dv,
            "tap": bc["tap"], "so_lieu": so_lieu, "lop": lop,
            "B_phu": phu + B[len(dt):], "A_phu": phu + A[len(dt):]}


def _goi_tap(d):
    return (r"Let $A$ be the set of %s that %s, and let $B$ be the set of %s that %s. Then $n(A) = %d$, $n(B) = %d$, $n(A \cap B) = %d$." % (d["tap"], d["A"], d["tap"], d["B"], d["nA"], d["nB"], d["nAB"]))


def _nhieu_so(dap, ung):
    ra = []
    for x in ung + [dap + 1, dap - 1, dap + 2, dap + 3]:
        if isinstance(x, int) and x >= 0 and x != dap and x not in ra:
            ra.append(x)
    return ra[:3]


def L10_C1_B2_VD020_TL_A_01(socau, dong=1):
    r"""Tự luận - bài toán thực tế hai tập hợp: số người thuộc ít nhất một tập và
    số người không thuộc tập nào ($n(A \cup B) = n(A) + n(B) - n(A \cap B)$).

    SUA 30/09/2026 theo co Lan: loi dan chon ngau nhien trong kho _BOI_CANH_HAI_TAP
    (14 linh vuc), khong trung boi canh trong mot de. So lieu hop li theo boi canh.
    """
    chon = _bo_chon_boi_canh()
    cauTL = ""
    for _ in range(socau):
        d = _de_hai_tap(chon)
        debai = d["mo"] + " " + d["so_lieu"] + ". Answer the following:"
        ds_abcd = [
            (r"How many %s %s at least one of the two %s above?" % (d["dv"], d["dt"], d["loai"]), d["nAuB"],
             _goi_tap(d) + r"\\ The number of %s that %s at least one of the two %s is $n(A \cup B) = n(A) + n(B) - n(A \cap B) = %d + %d - %d = %d$." % (d["dv"], d["dt"], d["loai"], d["nA"], d["nB"], d["nAB"], d["nAuB"])),
            (r"How many %s %s any of the %s among the two %s above?" % (d["dv"], d["phu"], d["loai"], d["loai"]), d["khong"],
             r"The number of %s that %s any of the %s is $%d - n(A \cup B) = %d - %d = %d$."
             % (d["dv"], d["phu"], d["loai"], d["N"], d["N"], d["nAuB"], d["khong"])),
        ]
        cauTL += TL_answer_const(debai, ds_abcd, 0, 0, dong)
    return cauTL


def L10_C1_B2_VD020_TL_A_02(socau, dong=1):
    r"""Tự luận - cách hỏi khác của _01: biết tổng số, $n(A)$, $n(B)$ và số người
    KHÔNG thuộc tập nào; tính số thuộc ít nhất một tập, số thuộc cả hai, số chỉ thuộc $A$.

    CLAUDE THEM 30/09/2026 - bien the 02 cua VD020_TL_A (kho boi canh chung).
    Co Lan duyet lai.
    """
    chon = _bo_chon_boi_canh()
    cauTL = ""
    for _ in range(socau):
        d = _de_hai_tap(chon)
        debai = (d["mo"] + r" there are $%d$ %s that %s, $%d$ %s that %s, and $%d$ %s that %s any of the %s among the two %s above. Answer the following:"
                 % (d["nA"], d["dv"], d["A"], d["nB"], d["dv"], d["B"], d["khong"], d["dv"], d["phu"],
                    d["loai"], d["loai"]))
        chi_A = d["nA"] - d["nAB"]
        ds_abcd = [
            (r"How many %s %s at least one of the two %s above?" % (d["dv"], d["dt"], d["loai"]), d["nAuB"],
             r"Let $A$ and $B$ be the sets of %s that %s and that %s, respectively. The number of %s that %s at least one of the two %s is $n(A \cup B) = %d - %d = %d$." % (d["tap"], d["A"], d["B"], d["dv"], d["dt"], d["loai"],
                                                 d["N"], d["khong"], d["nAuB"])),
            (r"How many %s %s both %s?" % (d["dv"], d["dt"], d["loai"]), d["nAB"],
             r"$n(A \cap B) = n(A) + n(B) - n(A \cup B) = %d + %d - %d = %d$." % (d["nA"], d["nB"], d["nAuB"], d["nAB"])),
            (r"How many %s %s but %s?" % (d["dv"], d["A"], d["B_phu"]), chi_A,
             r"The number of %s that belong only to $A$ is $n(A) - n(A \cap B) = %d - %d = %d$." % (d["dv"], d["nA"], d["nAB"], chi_A)),
        ]
        cauTL += TL_answer_const(debai, ds_abcd, 0, 0, dong)
    return cauTL


def L10_C1_B2_VD020_MC_A_02(socau, dang=1):
    r"""Bài toán thực tế hai tập hợp: biết $n(A)$, $n(B)$, $n(A \cap B)$ và số người
    không thuộc tập nào, tìm TỔNG số người (trắc nghiệm).

    SUA 30/09/2026 theo co Lan: loi dan chon ngau nhien trong kho _BOI_CANH_HAI_TAP
    (chi nhung boi canh tong so thay doi duoc - bo boi canh lop 35 hoc sinh), khong
    trung boi canh trong mot de.
    """
    chon = _bo_chon_boi_canh()
    cau = ""
    for _ in range(socau):
        d = _de_hai_tap(chon, dieu_kien=lambda bc: "mo_an" in bc, an_N=True)
        debai = d["mo"] + " " + d["so_lieu"] + (
            r"; in addition, there are $%d$ %s that %s any of the %s among the two %s above. %s"
            % (d["khong"], d["dv"], d["phu"], d["loai"], d["loai"], d["bc"]["hoi_tong"]))
        giai = (_goi_tap(d) + "\\\\\n" +
                r"The number of %s that %s at least one of the two %s is $n(A \cup B) = %d + %d - %d = %d$."
                % (d["dv"], d["dt"], d["loai"], d["nA"], d["nB"], d["nAB"], d["nAuB"]) + "\\\\\n" +
                r"The total is $%d + %d = %d$." % (d["nAuB"], d["khong"], d["N"]))
        dap = d["N"]
        nhieu = ["$%d$" % x for x in _nhieu_so(dap, [d["nA"] + d["nB"] + d["khong"], d["nAuB"], d["N"] - d["nAB"]])]
        cau += MC_SA_answer_text(debai, "$%d$" % dap, nhieu, giai, 0, 0, dang)
    return cau


def _vung_hai_tap(bc, N, du_het=False):
    """CHỌN TRƯỚC số phần tử của từng vùng (đáp án có sẵn, cô Lan 30/09/2026):
    chỉ A (a), chỉ B (b), cả hai (c), không thuộc tập nào (k) - theo tỉ lệ hợp lí
    của bối cảnh; dữ kiện của đề suy ra từ các vùng nên đề không bao giờ vô lí.
    du_het=True: mọi phần tử thuộc ít nhất một tập (k = 0)."""
    tA, tB, tg = bc["tA"], bc["tB"], bc["giao"]
    for _ in range(5000):
        nA = random.randint(max(2, int(N * tA[0])), max(3, int(N * tA[1])))
        if du_het and bc["lop"]:
            nB = random.randint(max(2, N - nA + 1), max(3, int(N * 0.9)))
            c = nA + nB - N
        else:
            nB = random.randint(max(2, int(N * tB[0])), max(3, int(N * tB[1])))
            nho = min(nA, nB)
            c = random.randint(max(1, int(nho * tg[0])), max(1, int(nho * tg[1])))
        a, b = nA - c, nB - c
        k = 0 if du_het else N - a - b - c
        if a >= 1 and b >= 1 and c >= 1 and (du_het or k >= 2):
            if du_het and not bc["lop"]:
                N = a + b + c
            return a, b, c, k, a + b + c + k
    raise ValueError("khong sinh duoc so lieu")


def _de_hai_tap_vung(chon, dieu_kien=lambda bc: True, du_het=False):
    bc = chon(dieu_kien)
    A, B, dt, phu, loai = random.choice(bc["cap"])
    a, b, c, k, N = _vung_hai_tap(bc, random.choice(bc["N"]), du_het)
    lop = random.choice(_LOP_CHV) if bc["lop"] else ""
    mo = bc["mo"] % {"N": N, "lop": lop}
    return {"bc": bc, "A": A, "B": B, "dt": dt, "phu": phu, "loai": loai, "N": N, "nA": a + c, "nB": b + c,
            "nAB": c, "nAuB": a + b + c, "khong": k, "chi_A": a, "chi_B": b, "mo": mo, "dv": bc["dv"],
            "tap": bc["tap"], "lop": lop, "co": "" if mo.endswith("recorded that") else "there are ",
            "B_phu": phu + B[len(dt):], "A_phu": phu + A[len(dt):]}


def _hoi_hai_tap(d, muc, kieu):
    """Một câu hỏi về hai tập hợp. muc: ca_hai / khong / it_nhat / chi_A / chi_B.
    kieu: 'sa' (Hỏi có bao nhiêu ...?) hoặc 'mc' (Số ... là). Trả về (đề, đáp số,
    lời giải, ứng viên nhiễu)."""
    dv, dt, loai = d["dv"], d["dt"], d["loai"]
    goi = (r"Let $A$ and $B$ be the sets of %s that %s and that %s, respectively; $n(A) = %d$, $n(B) = %d$."
           % (d["tap"], d["A"], d["B"], d["nA"], d["nB"]))
    hai_tap = r"%s$%d$ %s that %s, $%d$ %s that %s" % (d["co"], d["nA"], dv, d["A"], d["nB"], dv, d["B"])
    ca_hai = r"$%d$ %s that %s both %s" % (d["nAB"], dv, dt, loai)
    if muc == "ca_hai":
        if d["khong"] == 0:
            cho = (r"%s$%d$ %s that %s and $%d$ %s that %s" % (d["co"], d["nA"], dv, d["A"], d["nB"], dv, d["B"]) +
                   r". It is known that all %s %s at least one of the two %s above" % (dv, dt, loai))
            ly = r"All %s belong to $A \cup B$, so $n(A \cup B) = %d$." % (dv, d["N"])
        else:
            cho = hai_tap + r" and $%d$ %s that %s any of the %s among the two %s above" % (d["khong"], dv, d["phu"], loai, loai)
            ly = r"$n(A \cup B) = %d - %d = %d$." % (d["N"], d["khong"], d["nAuB"])
        hoi = r"%s that %s both %s" % (dv, dt, loai)
        dap = d["nAB"]
        giai = goi + "\\\\\n" + ly + "\\\\\n" + (r"$n(A \cap B) = n(A) + n(B) - n(A \cup B) = %d + %d - %d = %d$."
                                              % (d["nA"], d["nB"], d["nAuB"], dap))
        ung = ([d["nA"] + d["nB"] - d["N"]] if d["khong"] else []) + \
            [d["N"] - d["nA"], d["N"] - d["nB"], d["nAuB"], abs(d["nA"] - d["nB"])]
    else:
        cho = hai_tap + " and " + ca_hai
        tinh_hop = (r"$n(A \cup B) = n(A) + n(B) - n(A \cap B) = %d + %d - %d = %d$."
                    % (d["nA"], d["nB"], d["nAB"], d["nAuB"]))
        if muc == "khong":
            hoi = r"%s that %s any of the %s among the two %s above" % (dv, d["phu"], loai, loai)
            dap = d["khong"]
            giai = goi + r" $n(A \cap B) = %d$." % d["nAB"] + "\\\\\n" + tinh_hop + "\\\\\n" + \
                r"The number of %s is $%d - %d = %d$." % (hoi, d["N"], d["nAuB"], dap)
            ung = [d["N"] - d["nA"] - d["nB"], d["N"] - d["nAB"], d["nAuB"]]
        elif muc == "it_nhat":
            hoi = r"%s that %s at least one of the two %s above" % (dv, dt, loai)
            dap = d["nAuB"]
            giai = goi + r" $n(A \cap B) = %d$." % d["nAB"] + "\\\\\n" + tinh_hop
            ung = [d["nA"] + d["nB"], d["nA"] + d["nB"] + d["nAB"], d["khong"]]
        else:
            laA = muc == "chi_A"
            hoi = r"%s that %s but %s" % (dv, d["A"] if laA else d["B"], d["B_phu"] if laA else d["A_phu"])
            n1 = d["nA"] if laA else d["nB"]
            dap = d["chi_A"] if laA else d["chi_B"]
            giai = goi + r" $n(A \cap B) = %d$." % d["nAB"] + "\\\\\n" + \
                r"The number of %s is $%d - %d = %d$." % (hoi, n1, d["nAB"], dap)
            ung = [n1, d["nAB"], d["nAuB"] - n1]
    de = d["mo"] + " " + cho + "." + (r" Find the number of %s." % hoi if kieu == "sa" else r" The number of %s is" % hoi)
    return de, dap, giai, ung


def _cau_hai_tap(socau, dang, cac_muc, kieu, du_het_khi_ca_hai=0.0):
    """Sinh socau câu hai tập hợp; mỗi câu chọn ngẫu nhiên nội dung hỏi trong cac_muc."""
    chon = _bo_chon_boi_canh()
    cau = ""
    for _ in range(socau):
        muc = random.choice(cac_muc)
        du_het = muc == "ca_hai" and random.random() < du_het_khi_ca_hai
        d = _de_hai_tap_vung(chon, du_het=du_het)
        de, dap, giai, ung = _hoi_hai_tap(d, muc, kieu)
        ds = _nhieu_so(dap, [x for x in ung if isinstance(x, int)])
        if kieu == "sa":
            cau += MC_SA_answer_const(de, str(dap), [str(x) for x in ds], giai, 0, 0, dang)
        else:
            cau += MC_SA_answer_text(de, "$%d$" % dap, ["$%d$" % x for x in ds], giai, 0, 0, dang)
    return cau


def L10_C1_B2_VD020_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bài toán thực tế hai tập hợp: hỏi ngẫu nhiên số người KHÔNG
    thuộc tập nào hoặc số người thuộc CẢ HAI tập (dữ kiện suy từ các vùng chọn trước).

    SUA 30/09/2026 theo co Lan: kho boi canh chung, khong trung boi canh trong de,
    noi dung hoi chon ngau nhien.
    """
    return _cau_hai_tap(socau, dang, ["khong", "ca_hai"], "sa")


def L10_C1_B2_VD020_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn - mỗi người đều thuộc ít nhất một tập, tìm số thuộc cả hai;
    hoặc (ngẫu nhiên) cho số thuộc cả hai, tìm số không thuộc tập nào.

    SUA 30/09/2026 theo co Lan: truoc la bai toan BA tap hop; nay hai tap, kho boi
    canh chung. Ban ba tap de danh o data/chuyen_de_hoc_tap/ba_tap_hop_L10_C1.py.
    """
    return _cau_hai_tap(socau, dang, ["ca_hai", "ca_hai", "khong"], "sa", du_het_khi_ca_hai=1.0)


def L10_C1_B2_VD020_SA_A_03(socau, dang=2):
    r"""Trả lời ngắn - số người CHỈ thuộc một tập (A mà không B, hoặc B mà không A),
    hoặc thuộc ít nhất một tập - chọn ngẫu nhiên.

    CLAUDE THEM 30/09/2026 - bien the 03 cua VD020_SA_A. Co Lan duyet lai.
    """
    return _cau_hai_tap(socau, dang, ["chi_A", "chi_B", "it_nhat"], "sa")


def L10_C1_B2_VD020_MC_A_01(socau, dang=1):
    r"""Trắc nghiệm - hai tập hợp: số người không thuộc tập nào hoặc thuộc cả hai
    (chọn ngẫu nhiên), kho bối cảnh chung.

    SUA 30/09/2026 theo co Lan.
    """
    return _cau_hai_tap(socau, dang, ["khong", "ca_hai"], "mc")


def L10_C1_B2_VD020_MC_A_03(socau, dang=1):
    r"""Trắc nghiệm - hai tập hợp: số người thuộc ít nhất một tập hoặc chỉ thuộc
    một tập (chọn ngẫu nhiên), kho bối cảnh chung.

    SUA 30/09/2026 theo co Lan: truoc la bai toan BA tap hop; nay hai tap.
    """
    return _cau_hai_tap(socau, dang, ["it_nhat", "chi_A", "chi_B"], "mc")


def L10_C1_B2_VD020_MC_A_04(socau, dang=1):
    r"""Trắc nghiệm - hai tập hợp: tìm số người thuộc cả hai tập (cho số không thuộc
    tập nào, hoặc biết mỗi người thuộc ít nhất một tập).

    CLAUDE THEM 30/09/2026 - bien the 04 cua VD020_MC_A. Co Lan duyet lai.
    """
    return _cau_hai_tap(socau, dang, ["ca_hai"], "mc", du_het_khi_ca_hai=0.5)


# =====================================================================
# LIỆT KÊ <-> TÍNH CHẤT ĐẶC TRƯNG (NB017) - bổ sung 30/09/2026 (cô Lan)
# ---------------------------------------------------------------------
# Theo bài Sách bài tập (A = {x ∈ Q | (2x + 1)(...)(...) = 0},
# B = {x ∈ N | x^2 > 2 và x < 4}) nhưng HẠ về mức NHẬN BIẾT theo cô Lan:
# phương trình tích chỉ có 2 hoặc 3 nhân tử, mỗi nhân tử BẬC NHẤT
# (nghiệm đọc ngay: số tự nhiên, số nguyên âm, phân số). Cái học sinh cần
# nhận biết là tập số N, Z, Q, R giữ lại nghiệm nào.
# Cùng một dạng, các cách hỏi:
#   NB017_MC_G_01  cho tính chất đặc trưng, chọn cách liệt kê đúng
#   NB017_MC_G_02  cho tập liệt kê, chọn cách viết bằng tính chất đặc trưng đúng
#   NB017_MC_G_03  hỏi phần tử a thuộc / không thuộc tập cho bởi tính chất
#   NB017_SA_A_01  cho tính chất đặc trưng, hỏi tập có bao nhiêu phần tử
#   NB017_SA_A_02  hỏi tổng các phần tử (tập đối xứng tổng = 0: hỏi tích/hiệu)
#   TH018_TL_A_01  tự luận: a) liệt kê A (NB017), b) giao/hợp/hiệu với B (TH018)
# =====================================================================

from sympy import Integer, nsimplify

_TAP_SO = {r"\mathbb{N}": "natural numbers", r"\mathbb{Z}": "integers", r"\mathbb{Q}": "rational numbers", r"\mathbb{R}": "real numbers"}


def _loc_tap_so(nghiem, tap):
    """Giữ các nghiệm thuộc tập số tap (N, Z, Q, R). Nghiệm ở đây đều hữu tỉ."""
    if tap == r"\mathbb{N}":
        return [v for v in nghiem if v.is_Integer and v >= 0]
    if tap == r"\mathbb{Z}":
        return [v for v in nghiem if v.is_Integer]
    return list(nghiem)


def _nhan_tu_bac_nhat(r):
    """Nhân tử bậc nhất có nghiệm r: x, (x - 2), (x + 3), (2x - 1), (3x + 2)."""
    r = Rational(r)
    p, q = r.q, r.p
    if q == 0:
        return "x"
    he = "" if p == 1 else "%d" % p
    return r"\left(%sx %s %d\right)" % (he, "-" if q > 0 else "+", abs(q))


def _viet_pt_tich(nghiem):
    """(phương trình, lời giải) của phương trình tích các nhân tử bậc nhất."""
    pt = "".join(_nhan_tu_bac_nhat(v) for v in nghiem) + " = 0"
    giai = r"$%s \Leftrightarrow %s$" % (pt, r" \text{ or } ".join("x = %s" % _tex_gt(v) for v in nghiem))
    return pt, giai


def _pt_tich_bo():
    """Nghiệm của phương trình tích 2 hoặc 3 nhân tử bậc nhất (mức NB). Hai kiểu:
    - chỉ có nghiệm nguyên, không cần liên tiếp (như -3; 1; 2 <-> (x + 3)(x - 1)(x - 2) = 0);
    - có nghiệm phân số: 3 nhân tử đủ ba loại nghiệm (số tự nhiên, số nguyên âm, phân số)
      hoặc 2 nhân tử lấy 2 trong 3 loại."""
    if random.random() < 0.4:
        n = random.choice([2, 3, 3])
        while True:
            nghiem = [Integer(v) for v in random.sample(range(-5, 6), n)]
            if any(v >= 0 for v in nghiem) and any(v < 0 for v in nghiem):
                break
    else:
        loai = ["tu_nhien", "am", "phan_so"]
        if random.random() < 0.4:
            loai = random.sample(loai, 2)
        nghiem = []
        for l_ in loai:
            if l_ == "tu_nhien":
                nghiem.append(Integer(random.randint(0, 5)))
            elif l_ == "am":
                nghiem.append(Integer(-random.randint(1, 5)))
            else:
                p = random.choice([2, 3])
                q = random.choice([v for v in (-2, -1, 1, 2) if math.gcd(abs(v), p) == 1])
                nghiem.append(Rational(q, p))
    if any(-v in nghiem for v in nghiem if v != 0):
        return _pt_tich_bo()                   # khong co cap nghiem doi nhau (doi dau nhan tu se trung nhan tu)
    random.shuffle(nghiem)
    nghiem.sort(key=lambda v: v != 0)          # nhân tử x (nghiệm 0) viết đầu: x(x + 3)(2x - 1)
    return nghiem


def _tap_dac_trung_4(tap):
    """Tập nghiệm của phương trình tích (mức NB) trên tập số tap."""
    nghiem = _pt_tich_bo()
    pt, giai_pt = _viet_pt_tich(nghiem)
    dung = _loc_tap_so(nghiem, tap)
    sai = [_loc_tap_so(nghiem, t) for t in _TAP_SO if t != tap]
    sai.append(_loc_tap_so([-v for v in nghiem], tap))                   # sai dấu khi giải
    sai.append([(1 / v if not v.is_Integer else v) for v in nghiem])     # 2x + 1 = 0 -> x = -2
    sai.append([-v for v in nghiem])
    if len(dung) >= 2:
        sai.append(dung[:-1])
    de = r"\left\{x \in %s \mid %s\right\}" % (tap, pt)
    giai = (r"We have %s. Keep only the solutions that are %s: $%s$."
            % (giai_pt, _TAP_SO[tap], "; ".join(_tex_gt(v) for v in sorted(dung, key=float)) if dung
               else r"\text{none}"))
    return de, dung, sai, giai


def _hai_dieu_kien_bo():
    """Tập trên N cho bởi hai điều kiện (kiểu x^2 > 2 và x < 4) cùng vài cách viết gần giống."""
    a_ = random.randint(1, 10)
    b_ = random.randint(math.isqrt(a_) + 2, math.isqrt(a_) + 4)
    mau = [(r"x^{2} > %d \text{ and } x < %d" % (a_, b_), lambda t: t * t > a_ and t < b_),
           (r"x^{2} \ge %d \text{ and } x < %d" % (a_, b_), lambda t: t * t >= a_ and t < b_),
           (r"x^{2} > %d \text{ and } x \le %d" % (a_, b_), lambda t: t * t > a_ and t <= b_),
           (r"x^{2} \ge %d \text{ and } x \le %d" % (a_, b_), lambda t: t * t >= a_ and t <= b_),
           (r"x^{2} < %d \text{ and } x < %d" % (a_, b_), lambda t: t * t < a_ and t < b_)]
    return [(r"\left\{x \in \mathbb{N} \mid %s\right\}" % m, [t for t in range(0, 30) if f(t)]) for m, f in mau]


def _loi_giai_hai_dieu_kien(de, dung):
    dk = de.split(r"\mid ")[1].replace(r"\right\}", "")
    return r"The natural numbers $x$ that simultaneously satisfy $%s$ are $%s$." % (
        dk.replace(r" \text{ and } ", r"$ and $"), "; ".join(map(str, dung)) if dung else r"\text{none}")


def _luy_thua_mo_ta(co_so, lo, hi, chat_tren=False):
    """Tập {x | x = a^n, n ∈ N, lo ≤ n ≤ hi} (hoặc n < hi) -> (đề, danh sách phần tử, lời giải)."""
    cs = ("(%d)" % co_so) if co_so < 0 else "%d" % co_so
    tren = "<" if chat_tren else r"\le"
    dk = (r"n %s %d" % (tren, hi)) if lo == 0 else (r"%d \le n %s %d" % (lo, tren, hi))
    de = r"\left\{x \mid x = %s^{n},\ n \in \mathbb{N},\ %s\right\}" % (cs, dk)
    cac_n = list(range(lo, (hi - 1 if chat_tren else hi) + 1))
    ds = [Integer(co_so) ** k for k in cac_n]
    giai = (r"For $n \in \mathbb{N}$, $%s$ gives $n \in \left\{%s\right\}$, so $x$ takes the values $%s$ respectively."
            % (dk, "; ".join(map(str, cac_n)), "; ".join(r"%s^{%d} = %d" % (cs, k, v) for k, v in zip(cac_n, ds))))
    return de, ds, giai


def _luy_thua_bo():
    """Tập lũy thừa 2^n, 3^n, (-2)^n, (-3)^n và các cách viết gần giống; tập đúng đứng đầu.
    Mỗi phần tử: (đề, danh sách phần tử, lời giải)."""
    co_so = random.choice([2, 3, -2, -3])
    so_pt = {2: random.choice([3, 4, 5]), -2: random.choice([3, 4]), 3: random.choice([3, 4]), -3: 3}[co_so]
    lo = random.choice([1, 1, 0])
    hi = lo + so_pt - 1
    lo2 = 1 - lo
    return [_luy_thua_mo_ta(co_so, lo, hi),
            _luy_thua_mo_ta(co_so, lo, hi, True),               # n < hi: thiếu phần tử cuối
            _luy_thua_mo_ta(co_so, lo2, lo2 + so_pt - 1),       # lệch n bắt đầu từ 0 / 1
            _luy_thua_mo_ta(-co_so, lo, hi),                    # đổi dấu cơ số
            _luy_thua_mo_ta(co_so, lo, hi + 1)]                 # thừa một phần tử


def _tap_luy_thua():
    bo = _luy_thua_bo()
    de, dung, giai = bo[0]
    return de, dung, [s for _, s, _ in bo[1:]], giai


def _chon_tap_dac_trung():
    """Chọn ngẫu nhiên một tập cho bởi tính chất đặc trưng: các loại cũ 0-3, phương trình
    tích bậc nhất, hai điều kiện trên N, lũy thừa 2^n, 3^n, (-2)^n, (-3)^n."""
    loai = random.randint(0, 6)
    if loai <= 3:
        return _tap_dac_trung(loai)
    if loai == 4:
        return _tap_dac_trung_4(random.choice(list(_TAP_SO)))
    if loai == 6:
        return _tap_luy_thua()
    bo = _hai_dieu_kien_bo()
    i = random.randrange(len(bo))
    de, dung = bo[i]
    sai = [s for j, (_, s) in enumerate(bo) if j != i]
    return de, dung, sai, _loi_giai_hai_dieu_kien(de, dung)


def L10_C1_B2_NB017_MC_G_02(socau, dang=1):
    r"""Hỏi NGƯỢC của _01: cho tập hợp dạng LIỆT KÊ (như $\{-3; 1; 2\}$, $\{2; 4; 8; 16\}$),
    chọn cách viết bằng TÍNH CHẤT ĐẶC TRƯNG đúng. Phương án: cùng phương trình tích
    bậc nhất trên các tập số khác nhau / đổi dấu nhân tử; lũy thừa $2^n, 3^n, (-2)^n,
    (-3)^n$ lệch điều kiện của $n$ hoặc dấu cơ số; cùng điều kiện với dấu < / ≤ khác nhau.

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB017_MC_G, theo bai Sach bai tap
    (da ha ve muc NB: 2-3 nhan tu bac nhat). Co Lan duyet lai.
    """
    N_, Z_ = r"\mathbb{N}", r"\mathbb{Z}"
    cau = ""
    so = 0
    while so < socau:
        kieu = random.randrange(4)
        if kieu == 0:
            nghiem = _pt_tich_bo()
            # Nghiem deu huu ti nen tren Q va R la mot tap: chi dung MOT trong hai
            tQR = random.choice([r"\mathbb{Q}", r"\mathbb{R}"])
            j = random.choice([i for i, v in enumerate(nghiem) if v != 0])
            cac_pt = [nghiem, [(-v if i == j else v) for i, v in enumerate(nghiem)], [-v for v in nghiem]]
            viet = [_viet_pt_tich(n_) for n_ in cac_pt]
            pt = viet[0][0]
            bo = [(r"\left\{x \in %s \mid %s\right\}" % (tQR, pt), list(nghiem), viet[0][1]),
                  (r"\left\{x \in %s \mid %s\right\}" % (N_, pt), _loc_tap_so(nghiem, N_), viet[0][1]),
                  (r"\left\{x \in %s \mid %s\right\}" % (Z_, pt), _loc_tap_so(nghiem, Z_), viet[0][1]),
                  (r"\left\{x \in %s \mid %s\right\}" % (tQR, viet[1][0]), list(cac_pt[1]), viet[1][1]),
                  (r"\left\{x \in %s \mid %s\right\}" % (tQR, viet[2][0]), list(cac_pt[2]), viet[2][1])]
            ly = r"Solve the equations:"
        elif kieu == 1:
            bo = [(d_, s_, "") for d_, s_ in _hai_dieu_kien_bo()]
            ly = r"Find the natural numbers that satisfy each condition in turn."
        elif kieu == 2:
            a_ = random.randint(-6, 0)
            b_ = a_ + random.randint(3, 6)
            tap = random.choice([Z_, Z_, N_])
            bo = []
            for tr in (True, False):
                for ph in (True, False):
                    lo = a_ if tr else a_ + 1
                    hi = b_ if ph else b_ - 1
                    ds = [t for t in range(lo, hi + 1) if tap != N_ or t >= 0]
                    bo.append((r"\left\{x \in %s \mid %d %s x %s %d\right\}" % (tap, a_, r"\le" if tr else "<",
                                                                                r"\le" if ph else "<", b_), ds, ""))
            ly = r"Write out the %s in each interval, then compare." % ("natural numbers" if tap == N_ else "integers")
        else:
            bo = _luy_thua_bo()
            ly = r"Let $n$ take each value satisfying the condition, then compute $x$:"
        # chi giu cac tap khac rong, doi mot khac nhau
        rieng = []
        for de, ds, g_ in bo:
            if ds and all(set(map(str, ds)) != set(map(str, d2)) for _, d2, _ in rieng):
                rieng.append((de, ds, g_))
        if len(rieng) < 4:
            continue
        rieng = rieng[:4]
        random.shuffle(rieng)
        nhieu_pt = [i for i, r_ in enumerate(rieng) if len(r_[1]) >= 2]
        if not nhieu_pt:
            continue
        i0 = random.choice(nhieu_pt)           # tap A dua ra co it nhat hai phan tu
        rieng.insert(0, rieng.pop(i0))
        de0, ds0, _ = rieng[0]
        so += 1
        cac_ly = [g_ for g_ in dict.fromkeys(g_ for _, _, g_ in rieng) if g_]
        debai = r"The set $A = %s$ written in set-builder notation (by a characteristic property of its elements) is" % _tap(ds0)
        giai = ("\\\\\n".join([ly] + cac_ly) + "\\\\\n" +
                "\\\\\n".join(r"$%s = %s$" % (d_, _tap(s_)) for d_, s_, _ in rieng) + ".\\\\\n" +
                r"Therefore $A = %s$." % de0)
        cau += MC_SA_answer_text(debai, "$A = %s$" % de0, ["$A = %s$" % d_ for d_, _, _ in rieng[1:4]],
                                 giai, 0, 0, dang)
    return cau


def L10_C1_B2_NB017_MC_G_03(socau, dang=1):
    r"""Cách hỏi thứ ba của NB017_MC_G: cho tập $A$ bằng tính chất đặc trưng (phương
    trình tích bậc nhất, lũy thừa $2^n, 3^n, (-2)^n, (-3)^n$, số nguyên tố, ước...),
    hỏi khẳng định ``$a \in A$'' / ``$a \notin A$'' nào đúng (hoặc sai). Các số đưa vào
    phương án là các số dễ nhầm (sai dấu, lệch biên, ngoài tập số).

    CLAUDE THEM 30/09/2026 - bien the 03 cua NB017_MC_G theo co Lan
    ("hoi phan tu 3 co thuoc tap ... theo dang tinh chat khong"). Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        de, dung, sai, giai = _chon_tap_dac_trung()
        if not dung:
            continue
        trong = {str(nsimplify(v)): nsimplify(v) for v in dung}
        ngoai = {}
        for s_ in sai:
            for v in s_:
                v = nsimplify(v)
                if str(v) not in trong:
                    ngoai[str(v)] = v
        if len(ngoai) < 2:
            continue
        hoi_dung = random.random() < 0.7
        # (so, khang dinh): khong de cap "a thuoc A" / "a khong thuoc A" cung mot so a
        # vao cung mot cau (hoc sinh se biet mot trong hai la dap an)
        md_dung = ([(k, r"%s \in A" % _tex_gt(v)) for k, v in trong.items()] +
                   [(k, r"%s \notin A" % _tex_gt(v)) for k, v in ngoai.items()])
        md_sai = ([(k, r"%s \notin A" % _tex_gt(v)) for k, v in trong.items()] +
                  [(k, r"%s \in A" % _tex_gt(v)) for k, v in ngoai.items()])
        if not hoi_dung:
            md_dung, md_sai = md_sai, md_dung
        k0, chon = random.choice(md_dung)
        con = [t_ for k, t_ in md_sai if k != k0]
        if len(con) < 3:
            continue
        nhieu = random.sample(con, 3)
        so += 1
        debai = r"Given the set $A = %s$. Which of the following statements is %s?" % (de, "true" if hoi_dung else "false")
        g = (giai + r" Therefore $A = %s$." % _tap(dung) + "\\\\\n" +
             r"Hence the %s statement is $%s$." % ("true" if hoi_dung else "false", chon))
        cau += MC_SA_answer_text(debai, "$%s$" % chon, ["$%s$" % t_ for t_ in nhieu], g, 0, 0, dang)
    return cau


def L10_C1_B2_NB017_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - cho tập hợp bằng tính chất đặc trưng (phương trình tích bậc
    nhất trên N, Z, Q, R; hai điều kiện trên N; số nguyên tố, ước, $x^2 < k$...),
    hỏi tập có bao nhiêu phần tử.

    CLAUDE THEM 30/09/2026 - dang moi (ban tra loi ngan cua NB017_MC_G). Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        de, dung, sai, giai = _chon_tap_dac_trung()
        if not dung:
            continue
        dap = len(set(map(str, dung)))
        so += 1
        debai = r"Given the set $A = %s$. How many elements does the set $A$ have?" % de
        g = giai + "\\\\\n" + r"Therefore $A = %s$ has $%d$ elements." % (_tap(dung), dap)
        ds = [str(len(set(map(str, s)))) for s in sai] + [str(dap + 1), str(dap + 2), str(max(dap - 1, 0))]
        cau += MC_SA_answer_const(debai, str(dap), [v for v in dict.fromkeys(ds) if v != str(dap)], g, 0, 0, dang)
    return cau


def _thap_phan_ngan(v):
    """Số hữu tỉ viết thập phân hữu hạn (dấu phẩy) tối đa 4 kí tự; không được thì None."""
    v = Rational(v)
    q = v.q
    for p_ in (2, 5):
        while q % p_ == 0:
            q //= p_
    if q != 1:
        return None
    s = ("%.4f" % float(v)).rstrip("0").rstrip(".")
    return s if len(s) <= 4 and s != "-0" else None


def L10_C1_B2_NB017_SA_A_02(socau, dang=2):
    r"""Trả lời ngắn - cách hỏi khác của _01: cho tập bằng tính chất đặc trưng, hỏi
    TỔNG các phần tử của tập (phải liệt kê đúng mới tính được).
    Tập đối xứng (như $\{x \in \mathbb{Z} \mid x^2 < k\}$) có tổng luôn bằng 0, học
    sinh đoán được - khi đó hỏi TÍCH các phần tử khác 0 hoặc HIỆU giữa phần tử lớn
    nhất và phần tử nhỏ nhất (theo cô Lan 30/09/2026).

    CLAUDE THEM 30/09/2026 - bien the 02 cua NB017_SA_A. Dap so thap phan huu han,
    toi da 4 ki tu. Co Lan duyet lai.
    """
    def _ngoac(v):
        return ("(%s)" % _tex_gt(v)) if float(v) < 0 else _tex_gt(v)

    cau = ""
    so = 0
    while so < socau:
        de, dung, sai, giai = _chon_tap_dac_trung()
        if len(dung) < 2:
            continue
        ds_ = sorted(set(nsimplify(v) for v in dung), key=float)
        tong = sum(ds_)
        if tong != 0:
            hoi, gia_tri = "tong", tong
        else:
            khac0 = [v for v in ds_ if v != 0]
            hoi = random.choice(["tich", "hieu"]) if len(khac0) >= 2 else "hieu"
            if hoi == "tich":
                gia_tri = 1
                for v in khac0:
                    gia_tri *= v
            else:
                gia_tri = ds_[-1] - ds_[0]
        dap = _thap_phan_ngan(gia_tri)
        if dap is None:
            continue
        so += 1
        tap_tex = _tap(dung)
        if hoi == "tong":
            debai = r"Given the set $A = %s$. Compute the sum of all elements of the set $A$." % de
            g = r"Therefore $A = %s$, and the sum of the elements is $%s = %s$." % (tap_tex, " + ".join(_ngoac(v) for v in ds_), dap)
        elif hoi == "tich":
            debai = r"Given the set $A = %s$. Compute the product of all elements of the set $A$ other than $0$." % de
            g = r"Therefore $A = %s$, and the product of the elements other than $0$ is $%s = %s$." % (
                tap_tex, r" \cdot ".join(_ngoac(v) for v in ds_ if v != 0), dap)
        else:
            debai = (r"Given the set $A = %s$. Compute the difference between the largest element and the smallest element of the set $A$." % de)
            g = r"Therefore $A = %s$, the largest element is $%s$, the smallest is $%s$; the difference is $%s - %s = %s$." % (
                tap_tex, _tex_gt(ds_[-1]), _tex_gt(ds_[0]), _tex_gt(ds_[-1]), _ngoac(ds_[0]), dap)
        g = giai + "\\\\\n" + g
        nhieu = [v_ for v_ in (_thap_phan_ngan(gia_tri + d_) for d_ in (1, -1, 2, -2, 3, 4)) if v_ and v_ != dap]
        nhieu += [v_ for v_ in (_thap_phan_ngan(-gia_tri), "0") if v_ and v_ != dap]
        cau += MC_SA_answer_const(debai, dap, list(dict.fromkeys(nhieu)), g, 0, 0, dang)
    return cau


def L10_C1_B2_TH018_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý thuộc HAI đơn vị kiến thức (theo cô Lan):
    a) liệt kê tập $A$ cho bởi tính chất đặc trưng - phương trình tích 2-3 nhân tử
       bậc nhất hoặc lũy thừa $2^n, 3^n, (-2)^n, (-3)^n$ (nội dung NB017);
    b) cho tập $B$ liệt kê đơn giản, tìm $A \cap B$, $A \cup B$, $A \setminus B$
       hoặc $B \setminus A$ (nội dung TH018).
    ID đặt ở TH018 (mức cao hơn của hai ý) để câu không vượt mức khi ma trận chọn TL.

    CLAUDE THEM 30/09/2026 - dang moi (thay NB017_TL_A cu). Co Lan duyet lai.
    """
    PHEP = [(r"A \cap B", lambda A_, B_: [v for v in A_ if v in B_],
             r"consists of the elements that belong to both $A$ and $B$"),
            (r"A \cup B", lambda A_, B_: list(A_) + [v for v in B_ if v not in A_],
             r"consists of the elements that belong to $A$ or to $B$"),
            (r"A \setminus B", lambda A_, B_: [v for v in A_ if v not in B_],
             r"consists of the elements that belong to $A$ but not to $B$"),
            (r"B \setminus A", lambda A_, B_: [v for v in B_ if v not in A_],
             r"consists of the elements that belong to $B$ but not to $A$")]
    cau = ""
    so = 0
    while so < socau:
        if random.random() < 0.35:
            de_a, A, giai_a = _luy_thua_bo()[0]
            giai_a += r" Therefore $A = %s$." % _tap(A)
        else:
            nghiem = _pt_tich_bo()
            pt, giai_pt = _viet_pt_tich(nghiem)
            tap = random.choice([r"\mathbb{Z}", r"\mathbb{Q}", r"\mathbb{R}"])
            A = _loc_tap_so(nghiem, tap)
            de_a = r"\left\{x \in %s \mid %s\right\}" % (tap, pt)
            giai_a = r"We have %s. Since $x \in %s$, $A = %s$." % (giai_pt, tap, _tap(A))
        if len(A) < 2:
            continue
        # B: mot vai phan tu cua A va vai so nguyen nho khac - chon truoc de ket qua khong rong
        chung = random.sample(A, random.randint(1, len(A) - 1))
        khac = random.sample([Integer(v) for v in range(-5, 7) if Integer(v) not in A], random.randint(1, 3))
        B = chung + khac
        ki_hieu, f, ly = random.choice(PHEP)
        KQ = f(A, B)
        if not KQ:
            continue
        so += 1
        debai = r"Given the sets $A = %s$ and $B = %s$." % (de_a, _tap(B))
        ds = [
            (r"List the elements of the set $A$.", r"A = %s" % _tap(A), giai_a),
            (r"Find $%s$." % ki_hieu, r"%s = %s" % (ki_hieu, _tap(KQ)),
             r"For $A = %s$ and $B = %s$, the set $%s$ %s, so $%s = %s$."
             % (_tap(A), _tap(B), ki_hieu, ly, ki_hieu, _tap(KQ))),
        ]
        cau += TL_answer_text(debai, ds, 0, 0, dong)
    return cau


# =====================================================================
# L10_C1_B1_TH014 - XÁC ĐỊNH TÍNH ĐÚNG SAI CỦA MỆNH ĐỀ TRONG TRƯỜNG HỢP ĐƠN GIẢN (01/10/2026)
# ---------------------------------------------------------------------
# Cô Lan: YCCĐ "Xác định được tính đúng/sai của một mệnh đề toán học trong những trường hợp đơn giản"
# -> CHỈ mức TH. Ba dạng lớn, mỗi dạng có MC, SA, TL:
#   1) kéo theo, mệnh đề đảo, tương đương, phủ định của các mệnh đề toán học đã học
#        MC_D (mệnh đề và mệnh đề đảo), MC_E (chọn mệnh đề đúng/sai), SA_A (đếm), TL L10_C1_NB010_TH014_TL_A
#   2) mệnh đề chứa kí hiệu với mọi, tồn tại
#        MC_F (đúng sai của P và của mệnh đề phủ định), SA_B (đếm), TL L10_C1_NB013_TH014_TL_A
#   3) biết A, B, C đúng/sai, xét tính đúng sai của mệnh đề kéo theo, tương đương ghép từ A, B, C
#        MC_G, SA_C (_01 cho sẵn đúng/sai, _02 cho mệnh đề cụ thể), TL L10_C1_TH003_TH014_TL_A
# Hạn chế trùng ngữ cảnh: mỗi kho mệnh đề được lấy XOAY VÒNG (_c1_xoay) - chỉ dùng lại một mệnh đề
# khi cả kho đã được dùng hết (giữ qua các lần gọi hàm trong cùng tiến trình máy chủ).
# =====================================================================
import sys as _sys
import types as _types

_C1_XV = _sys.modules.setdefault("_ngan_hang_xoay_vong", _types.ModuleType("_ngan_hang_xoay_vong"))
if not hasattr(_C1_XV, "da_dung"):
    _C1_XV.da_dung = {}


def _c1_xoay(ten, n, k=1, tru=()):
    """Chọn k chỉ số khác nhau trong range(n), ưu tiên chỉ số CHƯA dùng của kho 'ten'.
    Kho được nhớ trong sys.modules nên vẫn còn khi tệp chương được nạp lại ở lần ra đề sau;
    hết chỉ số chưa dùng thì xoá sổ, bắt đầu vòng mới."""
    da = _C1_XV.da_dung.setdefault(ten, set())
    con = [i for i in range(n) if i not in da and i not in tru]
    if len(con) < k:
        da.clear()
        con = [i for i in range(n) if i not in tru]
    chon = random.sample(con, k)
    da.update(chon)
    return chon


def _c1_tl_dap(s):
    """Đáp án tự luận đặt trong $...$ (TL_answer_text): phần chữ bọc \\text{}, phần công thức giữ nguyên."""
    ra = []
    for i, phan in enumerate(s.split("$")):
        if i % 2 == 0:
            if phan:
                ra.append(r"\text{%s}" % phan)
        else:
            ra.append(phan)
    return "".join(ra)


def _c1_hoa(s):
    """Viết hoa chữ cái đầu (bỏ qua công thức $...$ ở đầu câu)."""
    return s[0].upper() + s[1:] if s and s[0] != "$" else s


def _dl_chia_het():
    m = random.choice([6, 8, 10, 12, 14, 15, 18, 20, 21, 24, 30])
    d = random.choice([u for u in range(2, m) if m % u == 0])
    return (r"the natural number $n$ is divisible by $%d$" % m, r"$n$ is divisible by $%d$" % d, True, False,
            r"$%d = %d\cdot %d$ so every multiple of $%d$ is a multiple of $%d$" % (m, d, m // d, m, d),
            r"$n = %d$ is divisible by $%d$ but not by $%d$" % (d, d, m))


def _dl_hai_uoc():
    p, q = random.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (2, 7), (3, 7), (4, 7), (5, 6)])
    return (r"the natural number $n$ is divisible by both $%d$ and $%d$" % (p, q), r"$n$ is divisible by $%d$" % (p * q), True, True,
            r"$%d$ and $%d$ are relatively prime, so $n$ is divisible by $%d\cdot %d = %d$" % (p, q, p, q, p * q),
            r"$%d$ is divisible by both $%d$ and $%d$, so every multiple of $%d$ is too" % (p * q, p, q, p * q))


def _dl_tong_chu_so():
    k = random.choice([3, 9])
    return (r"the natural number $n$ is divisible by $%d$" % k, r"the sum of the digits of $n$ is divisible by $%d$" % k, True, True,
            r"this is the divisibility rule for $%d$" % k, r"the same rule for $%d$ applies in the other direction" % k)


def _dl_tan_cung():
    k = random.choice([2, 5])
    return (r"the natural number $n$ ends in the digit $0$", r"$n$ is divisible by $%d$" % k, True, False,
            r"a number ending in the digit $0$ is divisible by $10$, hence divisible by $%d$" % k,
            r"$n = %d$ is divisible by $%d$ but ends in the digit $%d$" % (k, k, k))


def _dl_x_bang_k():
    k = random.randint(2, 9)
    return (r"$x = %d$" % k, r"$x^{2} = %d$" % (k * k), True, False,
            r"$%d^{2} = %d$" % (k, k * k), r"$x = -%d$ also has $x^{2} = %d$" % (k, k * k))


def _dl_nghiem():
    r1, r2 = random.sample(range(-5, 7), 2)
    S, P = r1 + r2, r1 * r2
    pt = "x^{2}"
    if S:
        pt += (" - %dx" % S if S > 0 else " + %dx" % -S) if abs(S) != 1 else (" - x" if S > 0 else " + x")
    if P:
        pt += " + %d" % P if P > 0 else " - %d" % -P
    return (r"$x = %d$" % r1, r"$%s = 0$" % pt, True, False,
            r"substituting $x = %d$ into the left-hand side gives $0$" % r1,
            r"the equation also has the solution $x = %d \ne %d$" % (r2, r1))


def _dl_lon_hon():
    b = random.randint(1, 6)
    a = b + random.randint(1, 5)
    return (r"$x > %d$" % a, r"$x > %d$" % b, True, False,
            r"$x > %d > %d$" % (a, b), r"$x = %d$ satisfies $x > %d$ but $x \le %d$" % (a, b, a))


def _dl_tri_tuyet_doi():
    k = random.randint(2, 9)
    return (r"$\left|x\right| < %d$" % k, r"$-%d < x < %d$" % (k, k), True, True,
            r"this is the definition of absolute value", r"the same definition applies in the other direction")




def _dl_chan_le_ab():
    return (r"$a$ and $b$ are two even natural numbers", r"$a + b$ is even", True, False,
            r"the sum of two even numbers is even", r"$a = 1$, $b = 3$ gives $a + b = 4$ even, but $a$ and $b$ are odd")


def _dl_le_ab():
    return (r"$a$ and $b$ are two odd natural numbers", r"$a + b$ is even", True, False,
            r"the sum of two odd numbers is even", r"$a = 2$, $b = 4$ gives $a + b = 6$ even, but $a$ and $b$ are even")


def _dl_bon():
    return (r"the natural number $n$ is divisible by $4$", r"the number formed by the last two digits of $n$ is divisible by $4$", True, True,
            r"this is the divisibility rule for $4$", r"the same rule for $4$ applies in the other direction")


def _dl_ba_chin():
    return (r"the integer $n$ is divisible by $3$", r"$n^{2}$ is divisible by $9$", True, True,
            r"if $n = 3k$ then $n^{2} = 9k^{2}$",
            r"$3$ is prime, so if $n^{2}$ is divisible by $3$ then $n$ is divisible by $3$")


def _dl_lon_hon_duong():
    return (r"$a > b > 0$", r"$a^{2} > b^{2}$", True, False,
            r"multiplying two inequalities in the same direction whose sides are positive gives $a\cdot a > b\cdot b$",
            r"$a = -3$, $b = 1$ gives $a^{2} > b^{2}$ but $a > b > 0$ does not hold")


def _dl_khong_am():
    return (r"$x \ge 0$", r"$\left|x\right| = x$", True, True,
            r"this is the definition of absolute value", r"$\left|x\right| \ge 0$, so $x = \left|x\right| \ge 0$")


def _dl_ac_trai_dau():
    return (r"the quadratic equation $ax^{2} + bx + c = 0$ has $a$ and $c$ of opposite signs",
            r"the equation $ax^{2} + bx + c = 0$ has two distinct solutions", True, False,
            r"$ac < 0$, so $\Delta = b^{2} - 4ac > 0$",
            r"the equation $x^{2} - 3x + 2 = 0$ has two solutions $1$, $2$ but $a = 1$, $c = 2$ have the same sign")


# Kho 1 chia theo ĐƠN VỊ KIẾN THỨC (cô Lan 01/10/2026: "trong một câu chỉ hỏi về một chủ đề duy nhất,
# các đơn vị kiến thức khác nhau sẽ là các dạng A, B... khác nhau").
_KHO_DL = {
    "tu_giac": [
        lambda: (r"quadrilateral $ABCD$ is a square", r"quadrilateral $ABCD$ has four equal sides", True, False,
                 r"a square has four equal sides", r"a rhombus has four equal sides but is not necessarily a square"),
        lambda: (r"quadrilateral $ABCD$ is a rectangle", r"quadrilateral $ABCD$ has two diagonals of equal length", True, False,
                 r"a rectangle has two equal diagonals",
                 r"an isosceles trapezoid has two equal diagonals but is not a rectangle"),
        lambda: (r"quadrilateral $ABCD$ is a parallelogram", r"the two diagonals of quadrilateral $ABCD$ bisect each other",
                 True, True, r"this is a property of parallelograms", r"this is a criterion for recognizing a parallelogram"),
        lambda: (r"quadrilateral $ABCD$ is a parallelogram", r"quadrilateral $ABCD$ has two parallel opposite sides", True, False,
                 r"a parallelogram has parallel opposite sides",
                 r"a trapezoid has two parallel bases but is not necessarily a parallelogram"),
        lambda: (r"quadrilateral $ABCD$ is inscribed in a circle", r"quadrilateral $ABCD$ has two opposite angles that sum to $180^{\circ}$", True, True,
                 r"this is a property of cyclic quadrilaterals", r"this is a criterion for recognizing a cyclic quadrilateral"),
        lambda: (r"quadrilateral $ABCD$ is a rhombus", r"the diagonals of quadrilateral $ABCD$ are perpendicular", True, False,
                 r"the diagonals of a rhombus are perpendicular",
                 r"a quadrilateral with perpendicular diagonals that do not intersect at the midpoint of each diagonal is not a rhombus"),
        lambda: (r"quadrilateral $ABCD$ has three right angles", r"quadrilateral $ABCD$ is a rectangle", True, True,
                 r"the remaining angle equals $360^{\circ} - 270^{\circ} = 90^{\circ}$", r"a rectangle has four right angles"),
        lambda: (r"quadrilateral $ABCD$ is a square", r"quadrilateral $ABCD$ is a rectangle", True, False,
                 r"a square is a rectangle with four equal sides",
                 r"a rectangle with two different adjacent sides is not a square"),
        lambda: (r"quadrilateral $ABCD$ is a rectangle", r"quadrilateral $ABCD$ is a parallelogram with one right angle", True, True,
                 r"a rectangle is a parallelogram with four right angles", r"this is a criterion for recognizing a rectangle"),
    ],
    "tam_giac": [
        lambda: (r"triangle $ABC$ is equilateral", r"triangle $ABC$ has three equal angles", True, True,
                 r"an equilateral triangle has three angles equal to $60^{\circ}$", r"a triangle with three equal angles is equilateral"),
        lambda: (r"triangle $ABC$ is isosceles at $A$", r"triangle $ABC$ has $AB = AC$", True, True,
                 r"this is the definition of an isosceles triangle", r"the same definition applies in the other direction"),
        lambda: (r"triangle $ABC$ has a right angle at $A$", r"triangle $ABC$ has $AB^{2} + AC^{2} = BC^{2}$", True, True,
                 r"this is the Pythagorean theorem", r"the converse of the Pythagorean theorem"),
        lambda: (r"triangle $ABC$ is equilateral", r"triangle $ABC$ is isosceles", True, False,
                 r"an equilateral triangle is isosceles", r"an isosceles triangle with a vertex angle of $120^{\circ}$ is not equilateral"),
        lambda: (r"triangle $ABC$ has two angles equal to $60^{\circ}$", r"triangle $ABC$ is equilateral", True, True,
                 r"the remaining angle equals $180^{\circ} - 120^{\circ} = 60^{\circ}$", r"an equilateral triangle has three angles equal to $60^{\circ}$"),
        lambda: (r"triangle $ABC$ is an isosceles right triangle with the right angle at $A$", r"triangle $ABC$ has $\widehat{B} = \widehat{C} = 45^{\circ}$", True, True,
                 r"the two acute angles of an isosceles right triangle equal $45^{\circ}$", r"in that case $\widehat{A} = 90^{\circ}$ and $AB = AC$"),
        lambda: (r"triangle $ABC$ has a right angle at $A$", r"triangle $ABC$ has $\widehat{B} + \widehat{C} = 90^{\circ}$", True, True,
                 r"the sum of the three angles of a triangle is $180^{\circ}$", r"in that case $\widehat{A} = 180^{\circ} - 90^{\circ} = 90^{\circ}$"),
        lambda: (r"triangle $ABC$ has $AB > AC$", r"triangle $ABC$ has $\widehat{C} > \widehat{B}$", True, True,
                 r"in a triangle, the angle opposite the longer side is the larger angle",
                 r"in a triangle, the side opposite the larger angle is the longer side"),
        lambda: (r"triangle $ABC$ is isosceles", r"triangle $ABC$ has $AB = AC$", False, True,
                 r"a triangle may be isosceles at $B$ (then $BA = BC$) while $AB \ne AC$",
                 r"if $AB = AC$, then triangle $ABC$ is isosceles at $A$"),
        lambda: (r"the two triangles are congruent", r"the two triangles have equal areas", True, False,
                 r"two congruent triangles have equal areas",
                 r"a right triangle with legs $2$, $6$ and a right triangle with legs $3$, $4$ both have area $6$ but are not congruent"),
    ],
    "chia_het": [_dl_chia_het, _dl_hai_uoc, _dl_tong_chu_so, _dl_tan_cung, _dl_chan_le_ab, _dl_le_ab, _dl_bon, _dl_ba_chin,
                 lambda: (r"the integer $n$ is odd", r"$n^{2}$ is odd", True, True,
                          r"the product of two odd numbers is odd", r"if $n$ is even then $n^{2}$ is even"),
                 lambda: (r"the natural number $n$ is prime", r"$n$ is odd", False, False,
                          r"$2$ is prime but even", r"$9$ is odd but not prime")],
    "so_thuc": [_dl_x_bang_k, _dl_nghiem, _dl_lon_hon, _dl_tri_tuyet_doi, _dl_lon_hon_duong, _dl_khong_am, _dl_ac_trai_dau,
                lambda: (r"$a > b$", r"$a^{2} > b^{2}$", False, False,
                         r"$a = 1$, $b = -2$ gives $a > b$ but $a^{2} = 1 < 4 = b^{2}$",
                         r"$a = -3$, $b = 1$ gives $a^{2} > b^{2}$ but $a < b$"),
                lambda: (r"$x^{2} > 0$", r"$x \ne 0$", True, True,
                         r"if $x = 0$ then $x^{2} = 0$", r"if $x \ne 0$ then $x^{2} > 0$"),
                lambda: (r"$a = b$", r"$a^{2} = b^{2}$", True, False,
                         r"this follows by squaring both sides", r"$a = 2$, $b = -2$ gives $a^{2} = b^{2}$ but $a \ne b$")],
}
_TEN_DL = {"tu_giac": "quadrilaterals", "tam_giac": "triangles", "chia_het": "divisibility and parity of natural numbers",
           "so_thuc": "equalities, inequalities, and equations over the real numbers"}
_DL_PHANG = [(cd, i) for cd in _KHO_DL for i in range(len(_KHO_DL[cd]))]


def _c1_uu_tien(ten, n):
    """Thứ tự lấy phần tử của kho 'ten': phần tử CHƯA dùng trước (ngẫu nhiên), đã dùng sau.
    Kho đã dùng hết thì bắt đầu vòng mới. Dùng kèm _c1_danh_dau."""
    da = _C1_XV.da_dung.setdefault(ten, set())
    if len(da) >= n:
        da.clear()
    chua = [i for i in range(n) if i not in da]
    roi = [i for i in range(n) if i in da]
    random.shuffle(chua)
    random.shuffle(roi)
    return chua + roi


def _c1_bac_chon(ten, n, hoi_dung):
    """Các bậc tìm mệnh đề cho câu bốn phương án (khoá 01/10/2026 theo cô Lan: "chọn câu này rồi thì câu khác
    không chọn nữa, hết câu rồi mới quay lại"):
      1) chỉ mệnh đề CHƯA dùng, hỏi theo chiều đã định; 2) chỉ mệnh đề chưa dùng, đổi chiều câu hỏi;
      3) - 4) chỉ khi phần chưa dùng không đủ mới lấy thêm mệnh đề đã dùng."""
    da = _C1_XV.da_dung.setdefault(ten, set())
    if len(da) >= n:
        da.clear()
    chua = [i for i in range(n) if i not in da]
    roi = [i for i in range(n) if i in da]
    random.shuffle(chua)
    random.shuffle(roi)
    return [(chua, hoi_dung), (chua, not hoi_dung), (chua + roi, hoi_dung), (chua + roi, not hoi_dung)]


def _c1_danh_dau(ten, ds):
    _C1_XV.da_dung.setdefault(ten, set()).update(ds)


def _c1_dl(chu_de, i, dao=None):
    """Phần tử i của chủ đề chu_de trong kho 1; có thể đổi vai P, Q."""
    P, Q, pq, qp, l_pq, l_qp = _KHO_DL[chu_de][i]()
    if dao is None:
        dao = random.random() < 0.35
    if dao:
        P, Q, pq, qp, l_pq, l_qp = Q, P, qp, pq, l_qp, l_pq
    # "Nếu $n$ chia hết cho 3 thì số tự nhiên $n$ ..." -> đưa "số tự nhiên" lên mệnh đề đứng trước
    for ten in ("the natural number ", "the integer ", "the real number "):
        if P.startswith("$n$") and (ten + "$n$") in Q:
            P, Q = ten + P, Q.replace(ten + "$n$", "$n$", 1)
    return P, Q, pq, qp, l_pq, l_qp


def _c1_chon_bat_ky(tien_to, phang):
    """Chọn MỘT phần tử (chủ đề, chỉ số) trong cả kho, CHƯA dùng ở bất kì câu nào (cùng sổ với các câu
    theo chủ đề, nên câu một mệnh đề và câu bốn mệnh đề không lấy trùng nhau). Hết thì xoá sổ, vòng mới."""
    da = _C1_XV.da_dung
    con = [(cd, i) for cd, i in phang if i not in da.get(tien_to + cd, set())]
    if not con:
        for cd in {cd for cd, _ in phang}:
            da.get(tien_to + cd, set()).clear()
        con = list(phang)
    cd, i = random.choice(con)
    _c1_danh_dau(tien_to + cd, [i])
    return cd, i


def _c1_dl_bat_ky(dao=None):
    """Một phần tử bất kì của kho 1 - cho câu chỉ có MỘT mệnh đề (MC_D, tự luận NB010_TH014)."""
    cd, i = _c1_chon_bat_ky("c1_dl_", _DL_PHANG)
    return _c1_dl(cd, i, dao)


def _c1_cau_dl(chu_de, i, kieu=None):
    """Một mệnh đề (kéo theo / đảo / tương đương) từ phần tử i của chủ đề: (nội dung, đúng?, lí do)."""
    P, Q, pq, qp, l_pq, l_qp = _c1_dl(chu_de, i)
    kieu = kieu or random.choice(["keo", "keo", "tuong"])
    if kieu == "keo":
        return r"If %s, then %s" % (P, Q), pq, (l_pq if pq else r"there is a counterexample: " + l_pq)
    ly = (r"both statements ``If %s, then %s'' and ``If %s, then %s'' are true (%s; %s)" % (P, Q, Q, P, l_pq, l_qp)
          if pq and qp else
          r"the statement ``If %s, then %s'' is false (%s)" % ((P, Q, l_pq) if not pq else (Q, P, l_qp)))
    return _c1_hoa(r"%s if and only if %s" % (P, Q)), pq and qp, ly


def _c1_bon_cung_chu_de(chu_de, hoi_dung):
    """Bốn mệnh đề từ BỐN phần tử khác nhau của CÙNG một chủ đề: một mệnh đề có tính đúng sai = hoi_dung,
    ba mệnh đề còn lại ngược lại (đổi chiều câu hỏi nếu chủ đề không đủ)."""
    ten = "c1_dl_" + chu_de
    n = len(_KHO_DL[chu_de])
    for ds_i, hd in _c1_bac_chon(ten, n, hoi_dung):
        for _lan in range(20):
            chon, khac, dung_i = None, [], []
            for i in ds_i:
                for _t in range(6):
                    t, d, l = _c1_cau_dl(chu_de, i)
                    if d == hd and chon is None:
                        chon = (t, d, l); dung_i.append(i); break
                    if d != hd and len(khac) < 3:
                        khac.append((t, d, l)); dung_i.append(i); break
                if chon and len(khac) == 3:
                    _c1_danh_dau(ten, dung_i)
                    return hd, chon, khac
    raise CauHongError("chu de %s khong du menh de" % chu_de)


def _c1_mc_chu_de(socau, dang, chu_de):
    cau = ""
    for _ in range(socau):
        hoi_dung, (t, d, l), khac = _c1_bon_cung_chu_de(chu_de, random.choice([True, False]))
        de = r"Which of the following statements is %s?" % ("true" if hoi_dung else r"\textbf{false}")
        giai = (r"``%s'' is %s because %s.\\ " % (t, "true" if d else "false", l) +
                r"\\ ".join(r"``%s'' is %s because %s." % (t2, "true" if d2 else "false", l2) for t2, d2, l2 in khac))
        cau += _MC_khong_cham(de, t, [c[0] for c in khac], giai, 0, 0, dang)
    return cau


def _c1_sa_chu_de(socau, dang, chu_de):
    cau = ""
    ten = "c1_dl_" + chu_de
    for _ in range(socau):
        ds = []
        ids = _c1_uu_tien(ten, len(_KHO_DL[chu_de]))[:4]
        _c1_danh_dau(ten, ids)
        for i in ids:
            ds.append(_c1_cau_dl(chu_de, i))
        dap = sum(1 for _, d, _ in ds if d)
        de = r"Given the following statements:" + "\\\\\n" + _c1_danh_sach(ds) + "\\\\\n" + r"How many of the statements are true?"
        giai = _c1_giai_dem(ds) + "\\\\\n" + r"Therefore, the number of true statements is $%d$." % dap
        cau += MC_SA_answer_const(de, str(dap), [str(v) for v in range(5) if v != dap], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH014_MC_C_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề kéo theo, tương đương CÙNG chủ đề chia hết, chẵn lẻ
    của số tự nhiên (dấu hiệu chia hết, bội - ước, tổng hai số chẵn/lẻ...).

    CLAUDE THEM 29/09/2026; 01/10/2026 lam lai theo co Lan: mot cau chi mot chu de (truoc day tron chia het,
    tu giac, tam giac). Co Lan duyet lai.
    """
    return _c1_mc_chu_de(socau, dang, "chia_het")


def L10_C1_B1_TH014_MC_E_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề kéo theo, tương đương CÙNG chủ đề tứ giác
    (hình vuông, hình chữ nhật, hình thoi, hình bình hành, hình thang, tứ giác nội tiếp).

    CLAUDE THEM 01/10/2026 - lam lai theo co Lan: mot cau chi mot chu de. Co Lan duyet lai.
    """
    return _c1_mc_chu_de(socau, dang, "tu_giac")


def L10_C1_B1_TH014_MC_H_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề kéo theo, tương đương CÙNG chủ đề tam giác
    (tam giác đều, cân, vuông, Pythagore, tổng ba góc, quan hệ cạnh - góc).

    CLAUDE THEM 01/10/2026 - theo co Lan: mot cau chi mot chu de. Co Lan duyet lai.
    """
    return _c1_mc_chu_de(socau, dang, "tam_giac")


def L10_C1_B1_TH014_MC_I_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề kéo theo, tương đương CÙNG chủ đề đẳng thức, bất đẳng thức,
    phương trình với số thực.

    CLAUDE THEM 01/10/2026 - theo co Lan: mot cau chi mot chu de. Co Lan duyet lai.
    """
    return _c1_mc_chu_de(socau, dang, "so_thuc")


def L10_C1_B1_TH014_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề kéo theo, tương đương về tứ giác; có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - lam lai theo co Lan: mot cau chi mot chu de (cung chu de voi MC_E). Co Lan duyet lai.
    """
    return _c1_sa_chu_de(socau, dang, "tu_giac")


def L10_C1_B1_TH014_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề kéo theo, tương đương về tam giác; có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - theo co Lan (cung chu de voi MC_H). Co Lan duyet lai.
    """
    return _c1_sa_chu_de(socau, dang, "tam_giac")


def L10_C1_B1_TH014_SA_E_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề kéo theo, tương đương về chia hết, chẵn lẻ; có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - theo co Lan (cung chu de voi MC_C). Co Lan duyet lai.
    """
    return _c1_sa_chu_de(socau, dang, "chia_het")


def L10_C1_B1_TH014_SA_F_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề kéo theo, tương đương về đẳng thức, bất đẳng thức, phương trình với số thực;
    có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - theo co Lan (cung chu de voi MC_I). Co Lan duyet lai.
    """
    return _c1_sa_chu_de(socau, dang, "so_thuc")
def _c1_danh_sach(ds):
    """Liệt kê mệnh đề trong đề bài, đánh số 1., 2., ... (không dùng \\item, không gạch đầu dòng)."""
    return "\\\\\n".join(r"%d. %s." % (i + 1, t) for i, (t, _, _) in enumerate(ds))


def _c1_giai_dem(ds):
    return "\\\\\n".join(r"%d. %s because %s." % (i + 1, r"\textbf{True}" if d else r"\textbf{False}", l)
                         for i, (t, d, l) in enumerate(ds))


def L10_C1_B1_TH014_MC_D_01(socau, dang=1):
    r"""Cho mệnh đề kéo theo ``Nếu P thì Q'' (định lí, tính chất đã học): chọn khẳng định đúng về tính
    đúng sai của mệnh đề đó và của mệnh đề đảo ``Nếu Q thì P''.

    CLAUDE THEM 01/10/2026 - dang moi TH014 theo co Lan (dang 1: keo theo, dao, tuong duong). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        P, Q, pq, qp, l_pq, l_qp = _c1_dl_bat_ky()
        de = (r"Given the statement ``If %s, then %s''. Which of the following is true?" % (P, Q))
        tt = {True: "true", False: "false"}
        pa = {(a, b): r"The given statement is %s, and its converse is %s" % (tt[a], tt[b]) for a in (True, False) for b in (True, False)}
        giai = (r"The given statement is %s because %s.\\ The converse ``If %s, then %s'' is %s because %s."
                % (tt[pq], l_pq, Q, P, tt[qp], l_qp))
        cau += _MC_khong_cham(de, pa[(pq, qp)], [v for k, v in pa.items() if k != (pq, qp)], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH014_MC_D_02(socau, dang=1):
    r"""Cách hỏi khác của _01: cho mệnh đề tương đương ``P khi và chỉ khi Q'', chọn khẳng định đúng
    (đúng hay sai và vì sao: xét hai mệnh đề kéo theo P => Q, Q => P).

    CLAUDE THEM 01/10/2026 - bien the 02 cua TH014_MC_D. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        P, Q, pq, qp, l_pq, l_qp = _c1_dl_bat_ky(dao=random.random() < 0.5)
        de = (r"Given the statement ``%s if and only if %s''. Which of the following is true?" % (_c1_hoa(P), Q))
        k1, k2 = r"``If %s, then %s''" % (P, Q), r"``If %s, then %s''" % (Q, P)
        pa = {(True, True): r"The given statement is true because %s and %s are both true" % (k1, k2),
              (True, False): r"The given statement is false because %s is true but %s is false" % (k1, k2),
              (False, True): r"The given statement is false because %s is false but %s is true" % (k1, k2),
              (False, False): r"The given statement is false because %s and %s are both false" % (k1, k2)}
        tt = {True: "true", False: "false"}
        giai = (r"%s is %s because %s.\\ %s is %s because %s.\\ The biconditional statement is true only when both conditional statements are true."
                % (k1, tt[pq], l_pq, k2, tt[qp], l_qp))
        cau += _MC_khong_cham(de, pa[(pq, qp)], [v for k, v in pa.items() if k != (pq, qp)], giai, 0, 0, dang)
    return cau


def L10_C1_NB010_TH014_TL_A_01(socau, dong=1):
    r"""Tự luận - cho mệnh đề ``Nếu P thì Q'' (định lí, tính chất đã học).
    a) (NB010) Phát biểu mệnh đề đảo.
    b) (TH014) Xét tính đúng sai của mệnh đề đã cho và của mệnh đề đảo; từ đó cho biết mệnh đề
       ``P khi và chỉ khi Q'' đúng hay sai.

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi (NB010, TH014) theo co Lan (dang 1). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        P, Q, pq, qp, l_pq, l_qp = _c1_dl_bat_ky()
        tt = {True: "true", False: "false"}
        de = r"Given the statement ``If %s, then %s''." % (P, Q)
        ds = [(r"State the converse of the given statement.", _c1_tl_dap(r"If %s, then %s" % (Q, P)),
               r"Converse: ``If %s, then %s''." % (Q, P)),
              (r"Determine whether the given statement and its converse are true or false. Is the statement ``%s if and only if %s'' true or false?" % (_c1_hoa(P), Q),
               r"\text{Statement %s, converse %s, biconditional %s}" % (tt[pq], tt[qp], tt[pq and qp]),
               r"The given statement is %s because %s.\\ The converse is %s because %s.\\ Hence the statement ``%s if and only if %s'' is %s."
               % (tt[pq], l_pq, tt[qp], l_qp, _c1_hoa(P), Q, tt[pq and qp]))]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau




# ---------------------- Dạng 2: mệnh đề chứa kí hiệu với mọi, tồn tại ----------------------
# Kho 2 chia theo ĐƠN VỊ KIẾN THỨC: chẵn lẻ - bất đẳng thức trên R - nghiệm của phương trình trên tập số.
# Mỗi phần tử: (lượng từ A/E, tập, mệnh đề chứa biến, mệnh đề chứa biến phủ định, đúng?, lí do, cách đọc bằng lời).
_SO_BANG_LOI = {"N": "natural number", "Z": "integer", "Q": "rational number", "R": "real number"}


def _lt_chan_le():
    k = random.randint(1, 9)
    j = random.randint(1, 9)
    tn = r"n \in \mathbb{N}"
    return [
        ("A", tn, r"n\left(n + 1\right) \text{ is even}", r"n\left(n + 1\right) \text{ is odd}", True,
         r"$n\left(n + 1\right)$ is the product of two consecutive natural numbers, so it has an even factor",
         r"For every natural number $n$, $n\left(n + 1\right)$ is even"),
        ("A", tn, r"n^{2} + 1 \text{ is odd}", r"n^{2} + 1 \text{ is even}", False,
         r"for $n = 1$, $n^{2} + 1 = 2$ is even", r"For every natural number $n$, $n^{2} + 1$ is odd"),
        ("E", tn, r"n^{2} + 1 \text{ is even}", r"n^{2} + 1 \text{ is odd}", True,
         r"for $n = 1$, $n^{2} + 1 = 2$ is even", r"There exists a natural number $n$ such that $n^{2} + 1$ is even"),
        ("A", tn, r"n^{2} - n \text{ is even}", r"n^{2} - n \text{ is odd}", True,
         r"$n^{2} - n = n\left(n - 1\right)$ is the product of two consecutive natural numbers",
         r"For every natural number $n$, $n^{2} - n$ is even"),
        ("E", tn, r"n^{2} + n \text{ is odd}", r"n^{2} + n \text{ is even}", False,
         r"$n^{2} + n = n\left(n + 1\right)$ is always even", r"There exists a natural number $n$ such that $n^{2} + n$ is odd"),
        ("A", tn, r"2n + %d \text{ is odd}" % k, r"2n + %d \text{ is even}" % k, k % 2 == 1,
         (r"$2n$ is even, $%d$ is odd, so $2n + %d$ is odd" % (k, k)) if k % 2 else (r"$2n$ and $%d$ are both even, so $2n + %d$ is even" % (k, k)),
         r"For every natural number $n$, $2n + %d$ is odd" % k),
        ("A", tn, r"n^{2} + n + %d \text{ is odd}" % j, r"n^{2} + n + %d \text{ is even}" % j, j % 2 == 1,
         (r"$n^{2} + n$ is even, $%d$ is odd, so the sum is odd" % j) if j % 2 else (r"$n^{2} + n$ and $%d$ are both even, so the sum is even" % j),
         r"For every natural number $n$, $n^{2} + n + %d$ is odd" % j),
        ("E", tn, r"3n + 1 \text{ is even}", r"3n + 1 \text{ is odd}", True,
         r"for $n = 1$, $3n + 1 = 4$ is even", r"There exists a natural number $n$ such that $3n + 1$ is even"),
        ("A", tn, r"3n + 1 \text{ is even}", r"3n + 1 \text{ is odd}", False,
         r"for $n = 0$, $3n + 1 = 1$ is odd", r"For every natural number $n$, $3n + 1$ is even"),
        ("A", tn, r"n^{2} \text{ is even}", r"n^{2} \text{ is odd}", False,
         r"for $n = 1$, $n^{2} = 1$ is odd", r"For every natural number $n$, $n^{2}$ is even"),
        ("A", tn, r"\left(n + 1\right)\left(n + 2\right) \text{ is even}", r"\left(n + 1\right)\left(n + 2\right) \text{ is odd}", True,
         r"$n + 1$, $n + 2$ are two consecutive natural numbers, so one of them is even",
         r"For every natural number $n$, $\left(n + 1\right)\left(n + 2\right)$ is even"),
        ("E", tn, r"2n \text{ is odd}", r"2n \text{ is even}", False,
         r"$2n$ is always divisible by $2$", r"There exists a natural number $n$ such that $2n$ is odd"),
        ("E", tn, r"n^{2} - 1 \text{ is even}", r"n^{2} - 1 \text{ is odd}", True,
         r"for $n = 1$, $n^{2} - 1 = 0$ is even", r"There exists a natural number $n$ such that $n^{2} - 1$ is even"),
    ]


def _lt_bat_dang_thuc():
    c = random.randint(1, 9)
    a = random.randint(1, 9)
    tr = r"x \in \mathbb{R}"
    return [
        ("A", tr, r"x^{2} + %d > 0" % c, r"x^{2} + %d \le 0" % c, True,
         r"$x^{2} \ge 0$, so $x^{2} + %d \ge %d > 0$" % (c, c), r"For every real number $x$, $x^{2} + %d > 0$" % c),
        ("A", tr, r"x^{2} - %d > 0" % c, r"x^{2} - %d \le 0" % c, False,
         r"for $x = 0$, $x^{2} - %d = -%d < 0$" % (c, c), r"For every real number $x$, $x^{2} - %d > 0$" % c),
        ("E", tr, r"x^{2} - %d < 0" % c, r"x^{2} - %d \ge 0" % c, True,
         r"for $x = 0$, $x^{2} - %d = -%d < 0$" % (c, c), r"There exists a real number $x$ such that $x^{2} - %d < 0$" % c),
        ("E", tr, r"x^{2} + %d \le 0" % c, r"x^{2} + %d > 0" % c, False,
         r"$x^{2} + %d \ge %d > 0$ for all $x$" % (c, c), r"There exists a real number $x$ such that $x^{2} + %d \le 0$" % c),
        ("A", tr, r"\left(x - %d\right)^{2} \ge 0" % a, r"\left(x - %d\right)^{2} < 0" % a, True,
         r"the square of every real number is nonnegative", r"For every real number $x$, $\left(x - %d\right)^{2} \ge 0$" % a),
        ("A", tr, r"\left(x - %d\right)^{2} > 0" % a, r"\left(x - %d\right)^{2} \le 0" % a, False,
         r"for $x = %d$, $\left(x - %d\right)^{2} = 0$" % (a, a), r"For every real number $x$, $\left(x - %d\right)^{2} > 0$" % a),
        ("A", tr, r"\left|x\right| \ge 0", r"\left|x\right| < 0", True,
         r"the absolute value of every real number is nonnegative", r"For every real number $x$, $\left|x\right| \ge 0$"),
        ("A", tr, r"\left|x\right| > 0", r"\left|x\right| \le 0", False,
         r"for $x = 0$, $\left|x\right| = 0$", r"For every real number $x$, $\left|x\right| > 0$"),
        ("E", tr, r"x^{2} < x", r"x^{2} \ge x", True,
         r"for $x = \dfrac{1}{2}$, $x^{2} = \dfrac{1}{4} < \dfrac{1}{2}$", r"There exists a real number $x$ such that $x^{2} < x$"),
        ("A", tr, r"x^{2} \ge x", r"x^{2} < x", False,
         r"for $x = \dfrac{1}{2}$, $x^{2} = \dfrac{1}{4} < \dfrac{1}{2}$", r"For every real number $x$, $x^{2} \ge x$"),
        ("A", tr, r"x + %d > x" % c, r"x + %d \le x" % c, True,
         r"$\left(x + %d\right) - x = %d > 0$" % (c, c), r"For every real number $x$, $x + %d > x$" % c),
        ("A", tr, r"x - %d > x" % c, r"x - %d \le x" % c, False,
         r"$\left(x - %d\right) - x = -%d < 0$" % (c, c), r"For every real number $x$, $x - %d > x$" % c),
        ("E", tr, r"\left|x\right| + %d = 0" % c, r"\left|x\right| + %d \ne 0" % c, False,
         r"$\left|x\right| + %d \ge %d > 0$" % (c, c), r"There exists a real number $x$ such that $\left|x\right| + %d = 0$" % c),
        ("A", tr, r"x^{2} + 2x + 1 \ge 0", r"x^{2} + 2x + 1 < 0", True,
         r"$x^{2} + 2x + 1 = \left(x + 1\right)^{2} \ge 0$", r"For every real number $x$, $x^{2} + 2x + 1 \ge 0$"),
        ("E", tr, r"x^{2} + 1 < 2x", r"x^{2} + 1 \ge 2x", False,
         r"$x^{2} + 1 - 2x = \left(x - 1\right)^{2} \ge 0$", r"There exists a real number $x$ such that $x^{2} + 1 < 2x$"),
    ]


def _lt_phuong_trinh():
    c = random.randint(2, 9)
    a = random.randint(2, 6)
    s = random.randint(2, 9)
    k = random.choice([s * s, s * s + random.choice([1, 2, -1])])
    can = math.isqrt(k)
    r1, r2 = random.sample(range(1, 7), 2)
    m = random.randint(2, 6)
    hai = random.choice([m * (m + 1), m * (m + 1) + 1])
    n_hai = next((t for t in range(0, 12) if t * t + t == hai), None)
    bac2 = r"x^{2} %s %dx + %d" % ("+", r1 + r2, r1 * r2)
    return [
        ("E", r"x \in \mathbb{R}", r"x^{2} = %d" % c, r"x^{2} \ne %d" % c, True,
         r"for $x = \sqrt{%d}$, $x^{2} = %d$" % (c, c), r"There exists a real number $x$ such that $x^{2} = %d$" % c),
        ("E", r"x \in \mathbb{R}", r"x^{2} + %d = 0" % c, r"x^{2} + %d \ne 0" % c, False,
         r"$x^{2} + %d \ge %d > 0$ for all $x$" % (c, c), r"There exists a real number $x$ such that $x^{2} + %d = 0$" % c),
        ("E", r"x \in \mathbb{Q}", r"x^{2} = 2", r"x^{2} \ne 2", False,
         r"$x^{2} = 2$ has only the solutions $x = \pm\sqrt{2}$, which are irrational numbers", r"There exists a rational number $x$ such that $x^{2} = 2$"),
        ("E", r"n \in \mathbb{N}", r"n^{2} = %d" % k, r"n^{2} \ne %d" % k, can * can == k,
         (r"for $n = %d$, $n^{2} = %d$" % (can, k)) if can * can == k else
         (r"$%d^{2} < %d < %d^{2}$, so no natural number satisfies this" % (can, k, can + 1)),
         r"There exists a natural number $n$ such that $n^{2} = %d$" % k),
        ("E", r"n \in \mathbb{Z}", r"%dn = %d" % (a, a * c), r"%dn \ne %d" % (a, a * c), True,
         r"for $n = %d$, $%d\cdot %d = %d$" % (c, a, c, a * c), r"There exists an integer $n$ such that $%dn = %d$" % (a, a * c)),
        ("E", r"n \in \mathbb{Z}", r"%dn = %d" % (a, a * c + 1), r"%dn \ne %d" % (a, a * c + 1), False,
         r"$n = \dfrac{%d}{%d}$ is not an integer" % (a * c + 1, a), r"There exists an integer $n$ such that $%dn = %d$" % (a, a * c + 1)),
        ("E", r"x \in \mathbb{Q}", r"%dx = %d" % (a, a * c + 1), r"%dx \ne %d" % (a, a * c + 1), True,
         r"the solution $x = \dfrac{%d}{%d}$ is a rational number" % (a * c + 1, a), r"There exists a rational number $x$ such that $%dx = %d$" % (a, a * c + 1)),
        ("E", r"n \in \mathbb{N}", r"n + %d = 0" % c, r"n + %d \ne 0" % c, False,
         r"$n + %d \ge %d > 0$ for every natural number $n$" % (c, c), r"There exists a natural number $n$ such that $n + %d = 0$" % c),
        ("E", r"n \in \mathbb{Z}", r"n + %d = 0" % c, r"n + %d \ne 0" % c, True,
         r"$n = -%d$ satisfies the equation" % c, r"There exists an integer $n$ such that $n + %d = 0$" % c),
        ("A", r"x \in \mathbb{R}", r"x^{2} - 2x + 1 = 0", r"x^{2} - 2x + 1 \ne 0", False,
         r"for $x = 0$, $x^{2} - 2x + 1 = 1 \ne 0$", r"For every real number $x$, $x^{2} - 2x + 1 = 0$"),
        ("E", r"x \in \mathbb{N}", r"%s = 0" % bac2, r"%s \ne 0" % bac2, False,
         r"the equation has two solutions $x = -%d$, $x = -%d$, neither of which is a natural number" % (r1, r2),
         r"There exists a natural number $x$ such that $%s = 0$" % bac2),
        ("E", r"x \in \mathbb{Z}", r"%s = 0" % bac2, r"%s \ne 0" % bac2, True,
         r"$x = -%d$ is an integer and is a solution" % r1, r"There exists an integer $x$ such that $%s = 0$" % bac2),
        ("E", r"n \in \mathbb{N}", r"n^{2} + n = %d" % hai, r"n^{2} + n \ne %d" % hai, n_hai is not None,
         (r"for $n = %d$, $n^{2} + n = %d$" % (n_hai, hai)) if n_hai is not None else
         (r"$n^{2} + n = n\left(n + 1\right)$ is always even, but $%d$ is odd" % hai),
         r"There exists a natural number $n$ such that $n^{2} + n = %d$" % hai),
    ]


_KHO_LT = {"chan_le": _lt_chan_le, "bat_dang_thuc": _lt_bat_dang_thuc, "phuong_trinh": _lt_phuong_trinh}
_LT_PHANG = [(cd, i) for cd in _KHO_LT for i in range(len(_KHO_LT[cd]()))]


def _lt_tex(q, tap, p):
    return r"%s %s,\ %s" % (r"\forall" if q == "A" else r"\exists", tap, p)


def _lt(chu_de, i):
    q, tap, p, np_, d, ly, loi = _KHO_LT[chu_de]()[i]
    return dict(q=q, tap=tap, p=p, np=np_, dung=d, ly=ly, loi=loi, tex=_lt_tex(q, tap, p),
                phu=_lt_tex("E" if q == "A" else "A", tap, np_), phu_sai=_lt_tex(q, tap, np_))


def _lt_bat_ky():
    """Một mệnh đề chứa kí hiệu bất kì - cho câu chỉ có MỘT mệnh đề (MC_F_01, tự luận NB013_TH014)."""
    return _lt(*_c1_chon_bat_ky("c1_lt_", _LT_PHANG))


def L10_C1_B1_TH014_MC_F_01(socau, dang=1):
    r"""Cho mệnh đề $P$ chứa kí hiệu $\forall$ hoặc $\exists$ (mức đơn giản): chọn khẳng định đúng về tính
    đúng sai của $P$ và mệnh đề phủ định $\overline{P}$.

    CLAUDE THEM 01/10/2026 - dang moi TH014 theo co Lan (dang 2: voi moi, ton tai). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        m = _lt_bat_ky()
        tt = {True: "true", False: "false"}
        de = r"Given the statement $P$: ``$%s$''. Which of the following is true?" % m["tex"]
        pa = {(d, phu): r"$P$ is a %s statement and $\overline{P}$: ``$%s$''" % (tt[d], phu)
              for d in (True, False) for phu in (m["phu"], m["phu_sai"])}
        dung = pa[(m["dung"], m["phu"])]
        giai = (r"$P$ is %s because %s.\\ The negation of $\forall$ is $\exists$, the negation of $\exists$ is $\forall$, and we negate the predicate, so $\overline{P}$: ``$%s$''." % (tt[m["dung"]], m["ly"], m["phu"]))
        cau += _MC_khong_cham(de, dung, [v for v in pa.values() if v != dung], giai, 0, 0, dang)
    return cau


def _lt_bon(chu_de, hoi_dung):
    """Bốn mệnh đề chứa $\\forall$, $\\exists$ từ bốn phần tử khác nhau của CÙNG một chủ đề."""
    ten = "c1_lt_" + chu_de
    kho = _KHO_LT[chu_de]()
    bang = {i: _lt(chu_de, i) for i in range(len(kho))}     # một lần sinh số liệu cho cả câu
    bac = _c1_bac_chon(ten, len(kho), hoi_dung)
    chua = bac[0][0]
    so_dung = sum(1 for i in chua if bang[i]["dung"])
    so_sai = len(chua) - so_dung
    # chọn chiều câu hỏi để ba phương án nhiễu lấy ở nhóm còn NHIỀU mệnh đề chưa dùng hơn
    if (hoi_dung and so_sai < 3 <= so_dung) or (not hoi_dung and so_dung < 3 <= so_sai):
        hoi_dung = not hoi_dung
        bac = [(d, not h) for d, h in bac]
    for ds_i, hd in bac:
        chon, khac, ids = None, [], []
        for i in ds_i:
            m = bang[i]
            if m["dung"] == hd and chon is None:
                chon = m; ids.append(i)
            elif m["dung"] != hd and len(khac) < 3:
                khac.append(m); ids.append(i)
            if chon and len(khac) == 3:
                _c1_danh_dau(ten, ids)
                return hd, chon, khac
    raise CauHongError("chu de %s khong du menh de" % chu_de)


def _lt_mc_chu_de(socau, dang, chu_de):
    cau = ""
    for _ in range(socau):
        hoi_dung, chon, khac = _lt_bon(chu_de, random.choice([True, False]))
        de = r"Which of the following statements is %s?" % ("true" if hoi_dung else r"\textbf{false}")
        giai = "\\\\ ".join(r"$%s$ is %s because %s." % (m["tex"], "true" if m["dung"] else "false", m["ly"]) for m in [chon] + khac)
        cau += _MC_khong_cham(de, "$%s$" % chon["tex"], ["$%s$" % m["tex"] for m in khac], giai, 0, 0, dang)
    return cau


def _lt_sa_chu_de(socau, dang, chu_de):
    cau = ""
    ten = "c1_lt_" + chu_de
    for _ in range(socau):
        ids = _c1_uu_tien(ten, len(_KHO_LT[chu_de]()))[:4]
        _c1_danh_dau(ten, ids)
        ds = []
        for i in ids:
            m = _lt(chu_de, i)
            ds.append(("$%s$" % m["tex"], m["dung"], m["ly"]))
        dap = sum(1 for _, d, _ in ds if d)
        de = r"Given the following statements:" + "\\\\\n" + _c1_danh_sach(ds) + "\\\\\n" + r"How many of the statements are true?"
        giai = _c1_giai_dem(ds) + "\\\\\n" + r"Therefore, the number of true statements is $%d$." % dap
        cau += MC_SA_answer_const(de, str(dap), [str(v) for v in range(5) if v != dap], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH014_MC_J_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề chứa $\forall$, $\exists$ CÙNG chủ đề chẵn lẻ
    ($n\left(n + 1\right)$, $n^{2} + 1$, $2n + k$, ... là số chẵn / số lẻ).

    CLAUDE THEM 01/10/2026 - theo co Lan: mot cau chi mot chu de (thay TH014_MC_F_02, MC_A_02 tron chu de). Co Lan duyet lai.
    """
    return _lt_mc_chu_de(socau, dang, "chan_le")


def L10_C1_B1_TH014_MC_K_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề chứa $\forall$, $\exists$ CÙNG chủ đề bất đẳng thức trên
    $\mathbb{R}$ ($x^{2} + c > 0$, $\left|x\right| \ge 0$, $x^{2} \ge x$...).

    CLAUDE THEM 01/10/2026 - theo co Lan: mot cau chi mot chu de. Co Lan duyet lai.
    """
    return _lt_mc_chu_de(socau, dang, "bat_dang_thuc")


def L10_C1_B1_TH014_MC_L_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề chứa $\forall$, $\exists$ CÙNG chủ đề nghiệm của phương trình
    trên các tập $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$.

    CLAUDE THEM 01/10/2026 - theo co Lan: mot cau chi mot chu de. Co Lan duyet lai.
    """
    return _lt_mc_chu_de(socau, dang, "phuong_trinh")


def L10_C1_B1_TH014_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề chứa $\forall$, $\exists$ về chẵn lẻ; có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - lam lai theo co Lan: mot cau chi mot chu de (cung chu de voi MC_J). Co Lan duyet lai.
    """
    return _lt_sa_chu_de(socau, dang, "chan_le")


def L10_C1_B1_TH014_SA_G_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề chứa $\forall$, $\exists$ về bất đẳng thức trên $\mathbb{R}$; có bao nhiêu
    mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - theo co Lan (cung chu de voi MC_K). Co Lan duyet lai.
    """
    return _lt_sa_chu_de(socau, dang, "bat_dang_thuc")


def L10_C1_B1_TH014_SA_H_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề chứa $\forall$, $\exists$ về nghiệm của phương trình trên tập số; có bao nhiêu
    mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - theo co Lan (cung chu de voi MC_L). Co Lan duyet lai.
    """
    return _lt_sa_chu_de(socau, dang, "phuong_trinh")
def L10_C1_NB013_TH014_TL_A_01(socau, dong=1):
    r"""Tự luận - cho mệnh đề $P$ viết bằng kí hiệu $\forall$ hoặc $\exists$.
    a) (NB013) Phát biểu mệnh đề $P$ bằng lời.
    b) (TH014) Xét tính đúng sai của mệnh đề $P$ (giải thích).

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi (NB013, TH014) theo co Lan (dang 2). Khac TH003_TL_A_02
    (viet bang ki hieu) va VD014_TL_B (lap menh de phu dinh). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        m = _lt_bat_ky()
        de = r"Given the statement $P$: ``$%s$''." % m["tex"]
        ds = [(r"Write the statement $P$ in words.", _c1_tl_dap(m["loi"]),
               r"$P$: ``%s''." % m["loi"]),
              (r"Determine whether the statement $P$ is true or false.", r"\text{%s}" % ("True" if m["dung"] else "False"),
               r"Statement $P$ is %s because %s." % ("true" if m["dung"] else "false", m["ly"]))]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau


# ---------------------- Dạng 3: biết A, B, C đúng/sai, xét mệnh đề ghép ----------------------
def _ghep(X, Y, vX, vY):
    """Các mệnh đề ghép đơn giản từ X, Y: (LaTeX, đúng?, cách tính)."""
    tt = lambda v: "true" if v else "false"
    gn = lambda t: r"\overline{%s}" % t
    cX, cY = r"$%s$ is %s" % (X, tt(vX)), r"$%s$ is %s" % (Y, tt(vY))
    nX, nY = r"$\overline{%s}$ is %s" % (X, tt(not vX)), r"$\overline{%s}$ is %s" % (Y, tt(not vY))
    return [
        (r"%s \Rightarrow %s" % (X, Y), (not vX) or vY, cX + ", " + cY),
        (r"%s \Rightarrow %s" % (Y, X), (not vY) or vX, cY + ", " + cX),
        (r"%s \Leftrightarrow %s" % (X, Y), vX == vY, cX + ", " + cY),
        (r"%s \Rightarrow %s" % (gn(X), Y), vX or vY, nX + ", " + cY),
        (r"%s \Rightarrow %s" % (X, gn(Y)), (not vX) or (not vY), cX + ", " + nY),
        (r"%s \Leftrightarrow %s" % (gn(X), Y), (not vX) == vY, nX + ", " + cY),
    ]


def _c1_ly_ghep(t, d, gt):
    return r"$%s$ is %s (%s)" % (t, "true" if d else "false", gt)


def _c1_ba_md(cu_the):
    """Ba mệnh đề A, B, C: chân trị và đoạn giới thiệu. cu_the=True: mệnh đề về số cụ thể (_md_so)."""
    while True:
        v = [random.choice([True, False]) for _ in range(3)]
        if len(set(v)) == 2:
            break
    if not cu_the:
        tt = lambda x: "true" if x else "false"
        gt = r"$A$ is %s, $B$ is %s, $C$ is %s" % (tt(v[0]), tt(v[1]), tt(v[2]))
        return v, r"Given three statements $A$, $B$, $C$, where $A$ is a %s statement, $B$ is a %s statement, and $C$ is a %s statement." % (
            tt(v[0]), tt(v[1]), tt(v[2])), gt, None
    # 01/10/2026 (cô Lan: một câu chỉ một chủ đề): A, B, C cùng MỘT loại mệnh đề về số (cùng chia hết,
    # cùng số chính phương, cùng số nguyên tố...), loại được lấy xoay vòng.
    for loai in _c1_uu_tien("c1_md_so", 9):
        md, da = [], set()
        for vi in v:
            for _t in range(200):
                d = _md_so(loai)
                if d["dung"] == vi and d["p"] not in da:
                    da.add(d["p"])
                    md.append(d)
                    break
        if len(md) == 3:
            _c1_danh_dau("c1_md_so", [loai])
            break
    gt = "; ".join(r"$%s$ is %s because %s" % (T, "true" if d["dung"] else "false", d["ly_do"]) for T, d in zip("ABC", md))
    gioi = (r"Given three statements $A$: ``%s'', $B$: ``%s'', $C$: ``%s''." % (md[0]["p"], md[1]["p"], md[2]["p"]))
    return v, gioi, gt, md


def _c1_cac_ghep(v):
    """Mọi mệnh đề ghép đơn giản từ hai trong ba mệnh đề A, B, C."""
    ten = "ABC"
    ra = []
    for i in range(3):
        for j in range(3):
            if i < j:
                ra += _ghep(ten[i], ten[j], v[i], v[j])
    random.shuffle(ra)
    return ra


def _c1_mc_g(socau, dang, cu_the):
    cau = ""
    for _ in range(socau):
        v, gioi, gt, _md = _c1_ba_md(cu_the)
        hoi_dung = random.choice([True, False])
        ghep = _c1_cac_ghep(v)
        dung = [g for g in ghep if g[1] == hoi_dung]
        khac = [g for g in ghep if g[1] != hoi_dung]
        if not dung or len(khac) < 3:
            hoi_dung = not hoi_dung
            dung, khac = khac, dung
        chon = dung[0]
        khac = khac[:3]
        de = gioi + r" Which of the following is a %s statement?" % ("true" if hoi_dung else r"\textbf{false}")
        giai = (gt + r".\\ The conditional statement $X \Rightarrow Y$ is false only when $X$ is true and $Y$ is false; the biconditional $X \Leftrightarrow Y$ is true when $X$ and $Y$ are both true or both false; $\overline{X}$ has the opposite truth value of $X$.\\ "
                + r"\\ ".join(_c1_ly_ghep(t, d, w) + "." for t, d, w in [chon] + khac))
        cau += _MC_khong_cham(de, "$%s$" % chon[0], ["$%s$" % c[0] for c in khac], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH014_MC_G_01(socau, dang=1):
    r"""Cho ba mệnh đề $A$, $B$, $C$ đã biết tính đúng sai (ví dụ $A$ đúng, $B$ sai, $C$ đúng): chọn mệnh đề
    kéo theo, tương đương (có thể có phủ định) đúng / sai ghép từ $A$, $B$, $C$.

    CLAUDE THEM 01/10/2026 - dang moi TH014 theo co Lan (dang 3). Co Lan duyet lai.
    """
    return _c1_mc_g(socau, dang, False)


def L10_C1_B1_TH014_MC_G_02(socau, dang=1):
    r"""Cách hỏi khác của _01: $A$, $B$, $C$ là ba mệnh đề cụ thể về số (học sinh tự xét tính đúng sai),
    rồi chọn mệnh đề kéo theo, tương đương đúng / sai ghép từ chúng.

    CLAUDE THEM 01/10/2026 - bien the 02 cua TH014_MC_G. Co Lan duyet lai.
    """
    return _c1_mc_g(socau, dang, True)


def _c1_sa_c(socau, dang, cu_the):
    cau = ""
    for _ in range(socau):
        v, gioi, gt, _md = _c1_ba_md(cu_the)
        ghep = _c1_cac_ghep(v)[:4]
        ds = [("$%s$" % t, d, w) for t, d, w in ghep]
        dap = sum(1 for _, d, _ in ds if d)
        de = gioi + r" Among the following statements, how many are true?" + "\\\\\n" + _c1_danh_sach(ds)
        giai = (gt + r".\\ " + "\\\\\n".join(r"%d. $%s$ is %s because %s." % (i + 1, t, r"\textbf{true}" if d else r"\textbf{false}", w)
                                             for i, (t, d, w) in enumerate(ghep)) + "\\\\\n" + r"Therefore, the number of true statements is $%d$." % dap)
        cau += MC_SA_answer_const(de, str(dap), [str(x) for x in range(5) if x != dap], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH014_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - biết $A$, $B$, $C$ đúng hay sai; trong bốn mệnh đề kéo theo, tương đương ghép từ
    $A$, $B$, $C$ có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - dang moi TH014 theo co Lan (dang 3). Co Lan duyet lai.
    """
    return _c1_sa_c(socau, dang, False)


def L10_C1_B1_TH014_SA_C_02(socau, dang=2):
    r"""Cách hỏi khác của _01: $A$, $B$, $C$ là ba mệnh đề cụ thể về số.

    CLAUDE THEM 01/10/2026 - bien the 02 cua TH014_SA_C. Co Lan duyet lai.
    """
    return _c1_sa_c(socau, dang, True)


def L10_C1_TH003_TH014_TL_A_01(socau, dong=1):
    r"""Tự luận - ba mệnh đề cụ thể $A$, $B$, $C$ về số.
    a) (TH003) Xét tính đúng sai của $A$, $B$, $C$.
    b) (TH014) Xét tính đúng sai của hai mệnh đề kéo theo / tương đương ghép từ $A$, $B$, $C$.

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi (TH003, TH014) theo co Lan (dang 3). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        v, gioi, gt, md = _c1_ba_md(True)
        ghep = _c1_cac_ghep(v)
        g1 = ghep[0][:2]
        g2 = next(g for g in ghep[1:] if ("Leftrightarrow" in g[0]) != ("Leftrightarrow" in g1[0]))[:2]
        tt = lambda x: "true" if x else "false"
        ds = [(r"Determine whether the statements $A$, $B$, $C$ are true or false.",
               r"\text{A %s, B %s, C %s}" % (tt(v[0]), tt(v[1]), tt(v[2])), gt + "."),
              (r"Determine whether the statements $%s$ and $%s$ are true or false." % (g1[0], g2[0]),
               r"\text{%s %s, %s %s}" % ("first statement", tt(g1[1]), "second statement", tt(g2[1])),
               r"By part a): %s.\\ The conditional statement $X \Rightarrow Y$ is false only when $X$ is true and $Y$ is false; $X \Leftrightarrow Y$ is true when $X$, $Y$ are both true or both false.\\ Hence $%s$ is %s, $%s$ is %s."
               % (r"$A$ is %s, $B$ is %s, $C$ is %s" % (tt(v[0]), tt(v[1]), tt(v[2])), g1[0], tt(g1[1]), g2[0], tt(g2[1])))]
        cau += TL_answer_text(gioi, ds, 0, 0, dong)
    return cau


# ---------------------------------------------------------------------
# Sửa các hàm cũ của TH003 / TH014 (kiểm tra 01/10/2026)
# ---------------------------------------------------------------------
def _c1_ds_tl(ds):
    """Làm sạch đáp án tự luận cho TL_answer_text: bỏ cặp $...$ bao ngoài, 'Đúng'/'Sai' bọc \\text{}.
    (Trước đây TL_answer_const đưa chuỗi qua vlatex nên đáp án bị in thành \\mathtt{\\text{\\$...}}.)"""
    ra = []
    for hoi, dap, giai in ds:
        d = str(dap).strip()
        if d.startswith("$") and d.endswith("$") and d.count("$") == 2:
            d = d[1:-1]
        if d in ("True", "False"):
            d = r"\text{%s}" % d
        ra.append([hoi, d, giai])
    return ra


def _c1_ly_th014_dung(nhom, bien):
    """Lời giải cho L10_C1_B1_TH014_MC_A_01 (chọn khẳng định ĐÚNG), theo nhóm."""
    a, b, c = bien.get("a"), bien.get("b"), bien.get("c")
    LY = {
        1: r"$n^2 \ge 0$, so $n^2 + %s \ge %s > 0$ for every integer $n$" % (a, a),
        2: r"$\left|x\right| \ge 0$, so $\left|x\right| + %s \ge %s > 0$ for every real number $x$" % (a, a),
        3: r"the equation has the solution $x = %s$" % (_tex_so(Rational(-(b or 0), a or 1)) if a else "0"),
        4: r"$%s = %s\cdot %s$, so every multiple of $%s$ is a multiple of $%s$" % (a, b, (a // b) if a and b else "", a, b),
        5: r"every natural number is an integer",
        6: r"$p = 2$ is an even prime",
        7: r"if $n = 2k$, then $n^2 = 4k^2$ is even",
        8: r"if $n = 2k + 1$, then $n^2 = 2\left(2k^2 + 2k\right) + 1$ is odd",
        9: r"$n = %s$ is divisible by $%s$" % (a, a),
        10: r"$x = -1 < 0$",
        11: r"$x = 0$ gives $\left|x\right| = 0$",
        12: r"every real number equals itself",
        13: r"$\left(n + 1\right) - n = 1 > 0$",
        14: r"$x^2 \ge 0$, so $x^2 + %s \ge %s > 0$" % (c, c),
        15: r"$n = 2$ is an even natural number",
        16: r"$n = 1$ is an odd natural number",
    }
    ly = LY.get(nhom, r"$n = %s > %s$" % ((a or 0) + 1, a))
    return r"The true statement is the chosen option because %s. All the other statements are false." % ly


def _c1_ly_th014_sai(nhom, bien):
    """Lời giải cho L10_C1_B1_TH014_MC_B_01 (chọn khẳng định SAI), theo nhóm."""
    a, b, c = bien.get("a"), bien.get("b"), bien.get("c")
    LY = {
        1: r"for $n = 0$, $n^2 + %s = %s > 0$" % (a, a),
        2: r"$\left|x\right| + %s \ge %s > 0$ for every real number $x$" % (a, a),
        3: r"the equation $%sx + \left(%s\right) = 0$ has only one solution, so it does not hold for all real numbers $x$" % (a, b),
        4: r"$n = %s$ is divisible by $%s$ but not divisible by $%s$" % (b, b, a),
        5: r"$p = 3$ is prime but odd",
        6: r"$n = 2$ is even and $n^2 = 4$ is also even",
        7: r"$n = 1$ is odd and $n^2 = 1$ is also odd",
        8: r"$n = %s$ is divisible by $%s$" % (a, a),
        9: r"$x = 1 > 0$",
        10: r"$x = 0$ gives $\left|x\right| = 0$",
        11: r"every real number equals itself",
        12: r"$n + 1 > n$ for every natural number $n$",
        13: r"$x^2 + %s \ge %s > 0$ for every real number $x$" % (c, c),
        14: r"$n = 1$ is an odd natural number",
        15: r"$n = 2$ is an even natural number",
    }
    ly = LY.get(nhom, r"$n = %s$ is not greater than $%s$" % (a, a))
    return r"The false statement is the chosen option because %s. All the other statements are true." % ly


# =====================================================================
# BỔ SUNG TỪ TÀI LIỆU "CĐ DẠY THÊM TOÁN 10 - BÀI 1 MỆNH ĐỀ" (01/10/2026)
# ---------------------------------------------------------------------
# Cô Lan chọn: (1) biến thể hỏi khác cho TH014, (2) mệnh đề chứa biến TH003, (3) Đúng/Sai chương 1,
# (4) tự luận hai đơn vị mới. Giữ đúng YCCĐ của Bộ: KHÔNG dùng mệnh đề hai lượng từ (∀x ∀y, ∃x ∀y...),
# nguyên lí Dirichlet, bài đố ngoài chương; mỗi câu một chủ đề; mệnh đề lấy xoay vòng.
# =====================================================================

# ---------- thêm phần tử cho kho 1 (kéo theo / tương đương) ----------
def _dl_chia_het_tong():
    c = random.randint(3, 9)
    return (r"the natural numbers $a$ and $b$ are both divisible by $%d$" % c, r"$a + b$ is divisible by $%d$" % c, True, False,
            r"if $a = %dk$, $b = %dl$, then $a + b = %d\left(k + l\right)$" % (c, c, c),
            r"for $a = 1$, $b = %d$, $a + b = %d$ is divisible by $%d$, but $a$ and $b$ are not divisible by $%d$" % (c - 1, c, c, c))


def _dl_binh_phuong_lon():
    k = random.randint(1, 6)
    return (r"$x > %d$" % k, r"$x^{2} > %d$" % (k * k), True, False,
            r"$x > %d > 0$, so $x^{2} > %d^{2} = %d$" % (k, k, k * k),
            r"for $x = -%d$, $x^{2} = %d > %d$, but $x < %d$" % (k + 1, (k + 1) ** 2, k * k, k))


def _dl_tri_nho():
    k = random.randint(2, 9)
    return (r"$\left|x\right| < %d$" % k, r"$x < %d$" % k, True, False,
            r"$\left|x\right| < %d \Leftrightarrow -%d < x < %d$" % (k, k, k),
            r"for $x = -%d$, $x < %d$, but $\left|x\right| = %d > %d$" % (k + 1, k, k + 1, k))


_KHO_DL["tu_giac"] += [
    lambda: (r"trapezoid $ABCD$ is inscribed in a circle", r"trapezoid $ABCD$ is an isosceles trapezoid", True, True,
             r"a trapezoid inscribed in a circle has equal angles adjacent to one base, so it is an isosceles trapezoid",
             r"an isosceles trapezoid has opposite angles that sum to $180^{\circ}$, so it is inscribed in a circle"),
    lambda: (r"quadrilateral $ABCD$ is a square", r"quadrilateral $ABCD$ is a rectangle with perpendicular diagonals", True, True,
             r"a square is a rectangle with perpendicular diagonals", r"the criterion for identifying a square"),
    lambda: (r"quadrilateral $ABCD$ is a parallelogram", r"quadrilateral $ABCD$ has two diagonals of equal length", False, False,
             r"a parallelogram with a $60^{\circ}$ angle has unequal diagonals",
             r"an isosceles trapezoid has equal diagonals but is not a parallelogram"),
    lambda: (r"quadrilateral $ABCD$ is a square", r"the diagonals of quadrilateral $ABCD$ are perpendicular", True, False,
             r"the diagonals of a square are perpendicular to each other",
             r"a rhombus with a $60^{\circ}$ angle has perpendicular diagonals but is not a square"),
]
_KHO_DL["tam_giac"] += [
    lambda: (r"triangle $ABC$ has one angle equal to the sum of the other two angles", r"triangle $ABC$ is a right triangle", True, True,
             r"that angle equals $\dfrac{180^{\circ}}{2} = 90^{\circ}$", r"a right angle equals the sum of the other two acute angles"),
    lambda: (r"triangle $ABC$ is equilateral", r"triangle $ABC$ has $\widehat{A} = 60^{\circ}$", True, False,
             r"the three angles of an equilateral triangle each equal $60^{\circ}$",
             r"a triangle with $\widehat{A} = 60^{\circ}$, $\widehat{B} = 90^{\circ}$ is not equilateral"),
    lambda: (r"the two triangles are congruent", r"the two triangles are similar", True, False,
             r"two congruent triangles are similar triangles with ratio $1$",
             r"two equilateral triangles with side lengths $1$ and $2$ are similar but not congruent"),
    lambda: (r"triangle $ABC$ is isosceles at $A$", r"triangle $ABC$ has two equal altitudes $BE$, $CF$", True, True,
             r"right triangles $ABE$, $ACF$ are congruent (hypotenuse-angle)",
             r"right triangles $BCE$, $CBF$ are congruent (hypotenuse-leg), so $\widehat{B} = \widehat{C}$"),
]
_KHO_DL["chia_het"] += [_dl_chia_het_tong]
_KHO_DL["so_thuc"] += [_dl_binh_phuong_lon, _dl_tri_nho,
                       lambda: (r"$a + b > 2$", r"at least one of the numbers $a$, $b$ is greater than $1$", True, False,
                                r"if $a \le 1$ and $b \le 1$, then $a + b \le 2$",
                                r"for $a = 5$, $b = -10$, $a > 1$ but $a + b = -5 < 2$")]
_DL_PHANG[:] = [(cd, i) for cd in _KHO_DL for i in range(len(_KHO_DL[cd]))]


def _c1_bon_dao(chu_de, hoi_dung, kieu):
    """Bốn mệnh đề ``Nếu P thì Q'' cùng chủ đề. kieu = 'dao': xét tính đúng sai của MỆNH ĐỀ ĐẢO;
    kieu = 'dinh_li': xét mệnh đề đó có là định lí (mệnh đề kéo theo đúng) không."""
    ten = "c1_dl_" + chu_de
    n = len(_KHO_DL[chu_de])
    for ds_i, hd in _c1_bac_chon(ten, n, hoi_dung):
        for _lan in range(20):
            chon, khac, ids = None, [], []
            for i in ds_i:
                P, Q, pq, qp, l_pq, l_qp = _c1_dl(chu_de, i)
                gt = qp if kieu == "dao" else pq
                ly = (r"the converse ``If %s, then %s'' is %s (%s)" % (Q, P, "true" if qp else "false", l_qp) if kieu == "dao" else
                      r"this statement is %s (%s)" % ("true" if pq else "false", l_pq))
                muc = (r"If %s, then %s" % (P, Q), gt, ly)
                if gt == hd and chon is None:
                    chon = muc; ids.append(i)
                elif gt != hd and len(khac) < 3:
                    khac.append(muc); ids.append(i)
                if chon and len(khac) == 3:
                    _c1_danh_dau(ten, ids)
                    return hd, chon, khac
    raise CauHongError("chu de %s khong du menh de" % chu_de)


def _c1_mc_dao(socau, dang, chu_de, kieu):
    cau = ""
    for _ in range(socau):
        hd, (t, d, l), khac = _c1_bon_dao(chu_de, random.choice([True, False]), kieu)
        if kieu == "dao":
            de = r"Among the following statements, which one has a converse that is %s?" % ("true" if hd else r"\textbf{false}")
        else:
            de = (r"Among the following statements, which one is a theorem?" if hd else
                  r"Among the following statements, which one is \textbf{not} a theorem?")
        giai = ((r"A theorem is a true conditional statement.\\ " if kieu == "dinh_li" else "") +
                r"\\ ".join(r"``%s'': %s." % (t2, l2) for t2, d2, l2 in [(t, d, l)] + khac))
        cau += _MC_khong_cham(de, t, [c[0] for c in khac], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH014_MC_C_02(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề chia hết, chẵn lẻ): mệnh đề nào có mệnh đề ĐẢO đúng (sai).

    CLAUDE THEM 01/10/2026 - theo cau 38, 40 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "chia_het", "dao")


def L10_C1_B1_TH014_MC_C_03(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề chia hết, chẵn lẻ): mệnh đề nào là ĐỊNH LÍ (không là định lí).

    CLAUDE THEM 01/10/2026 - theo cau 41, 42 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "chia_het", "dinh_li")


def L10_C1_B1_TH014_MC_E_02(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề tứ giác): mệnh đề nào có mệnh đề ĐẢO đúng (sai).

    CLAUDE THEM 01/10/2026 - theo cau 38, 40 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "tu_giac", "dao")


def L10_C1_B1_TH014_MC_E_03(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề tứ giác): mệnh đề nào là ĐỊNH LÍ (không là định lí).

    CLAUDE THEM 01/10/2026 - theo cau 41, 42 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "tu_giac", "dinh_li")


def L10_C1_B1_TH014_MC_H_02(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề tam giác): mệnh đề nào có mệnh đề ĐẢO đúng (sai).

    CLAUDE THEM 01/10/2026 - theo cau 38, 40 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "tam_giac", "dao")


def L10_C1_B1_TH014_MC_H_03(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề tam giác): mệnh đề nào là ĐỊNH LÍ (không là định lí).

    CLAUDE THEM 01/10/2026 - theo cau 41, 42 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "tam_giac", "dinh_li")


def L10_C1_B1_TH014_MC_I_02(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề số thực): mệnh đề nào có mệnh đề ĐẢO đúng (sai).

    CLAUDE THEM 01/10/2026 - theo cau 38, 40 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "so_thuc", "dao")


def L10_C1_B1_TH014_MC_I_03(socau, dang=1):
    r"""Cách hỏi khác của _01 (chủ đề số thực): mệnh đề nào là ĐỊNH LÍ (không là định lí).

    CLAUDE THEM 01/10/2026 - theo cau 41, 42 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    return _c1_mc_dao(socau, dang, "so_thuc", "dinh_li")


# ---------- chủ đề mới cho kho 2 (∀, ∃): chia hết ----------
def _lt_chia_het():
    tn = r"n \in \mathbb{N}"
    return [
        ("A", tn, r"n^{2} + 1 \text{ is not divisible by } 3", r"n^{2} + 1 \text{ is divisible by } 3", True,
         r"$n^{2}$ leaves a remainder of $0$ or $1$ when divided by $3$, so $n^{2} + 1$ leaves a remainder of $1$ or $2$ when divided by $3$",
         r"For every natural number $n$, $n^{2} + 1$ is not divisible by $3$"),
        ("E", tn, r"n^{2} + 1 \text{ is divisible by } 4", r"n^{2} + 1 \text{ is not divisible by } 4", False,
         r"$n^{2}$ leaves a remainder of $0$ or $1$ when divided by $4$, so $n^{2} + 1$ leaves a remainder of $1$ or $2$ when divided by $4$",
         r"There exists a natural number $n$ such that $n^{2} + 1$ is divisible by $4$"),
        ("A", tn, r"n\left(n + 1\right)\left(n + 2\right) \text{ is divisible by } 6",
         r"n\left(n + 1\right)\left(n + 2\right) \text{ is not divisible by } 6", True,
         r"among three consecutive natural numbers, one is divisible by $2$ and one is divisible by $3$",
         r"For every natural number $n$, $n\left(n + 1\right)\left(n + 2\right)$ is divisible by $6$"),
        ("A", r"n \in \mathbb{N}^{*}", r"n^{2} - 1 \text{ is divisible by } 3", r"n^{2} - 1 \text{ is not divisible by } 3", False,
         r"for $n = 3$, $n^{2} - 1 = 8$ is not divisible by $3$", r"For every natural number $n$ other than $0$, $n^{2} - 1$ is divisible by $3$"),
        ("E", tn, r"n^{2} - 1 \text{ is divisible by } 3", r"n^{2} - 1 \text{ is not divisible by } 3", True,
         r"for $n = 2$, $n^{2} - 1 = 3$", r"There exists a natural number $n$ such that $n^{2} - 1$ is divisible by $3$"),
        ("A", tn, r"5n^{2} + 10 \text{ is divisible by } 5", r"5n^{2} + 10 \text{ is not divisible by } 5", True,
         r"$5n^{2} + 10 = 5\left(n^{2} + 2\right)$", r"For every natural number $n$, $5n^{2} + 10$ is divisible by $5$"),
        ("A", tn, r"n^{3} - n \text{ is divisible by } 3", r"n^{3} - n \text{ is not divisible by } 3", True,
         r"$n^{3} - n = \left(n - 1\right)n\left(n + 1\right)$ is a product of three consecutive integers",
         r"For every natural number $n$, $n^{3} - n$ is divisible by $3$"),
        ("E", tn, r"n^{2} + 2 \text{ is divisible by } 3", r"n^{2} + 2 \text{ is not divisible by } 3", True,
         r"for $n = 1$, $n^{2} + 2 = 3$", r"There exists a natural number $n$ such that $n^{2} + 2$ is divisible by $3$"),
        ("A", tn, r"n^{2} + 2 \text{ is divisible by } 3", r"n^{2} + 2 \text{ is not divisible by } 3", False,
         r"for $n = 0$, $n^{2} + 2 = 2$ is not divisible by $3$", r"For every natural number $n$, $n^{2} + 2$ is divisible by $3$"),
        ("E", tn, r"n^{2} + n \text{ is divisible by } 5", r"n^{2} + n \text{ is not divisible by } 5", True,
         r"for $n = 4$, $n^{2} + n = 20$", r"There exists a natural number $n$ such that $n^{2} + n$ is divisible by $5$"),
        ("A", tn, r"\left(n + 3\right)^{2} - n^{2} \text{ is divisible by } 3", r"\left(n + 3\right)^{2} - n^{2} \text{ is not divisible by } 3", True,
         r"$\left(n + 3\right)^{2} - n^{2} = 6n + 9 = 3\left(2n + 3\right)$",
         r"For every natural number $n$, $\left(n + 3\right)^{2} - n^{2}$ is divisible by $3$"),
        ("E", tn, r"3n + 2 \text{ is divisible by } 3", r"3n + 2 \text{ is not divisible by } 3", False,
         r"$3n + 2$ always leaves a remainder of $2$ when divided by $3$", r"There exists a natural number $n$ such that $3n + 2$ is divisible by $3$"),
        ("A", tn, r"n^{2} + n + 1 \text{ is divisible by } 3", r"n^{2} + n + 1 \text{ is not divisible by } 3", False,
         r"for $n = 0$, $n^{2} + n + 1 = 1$", r"For every natural number $n$, $n^{2} + n + 1$ is divisible by $3$"),
    ]


_KHO_LT["chia_het"] = _lt_chia_het
_LT_PHANG[:] = [(cd, i) for cd in _KHO_LT for i in range(len(_KHO_LT[cd]()))]


def L10_C1_B1_TH014_MC_M_01(socau, dang=1):
    r"""Chọn mệnh đề đúng (sai) trong bốn mệnh đề chứa $\forall$, $\exists$ CÙNG chủ đề chia hết
    ($n^{2} + 1$ không chia hết cho $3$, $n\left(n + 1\right)\left(n + 2\right)$ chia hết cho $6$...).

    CLAUDE THEM 01/10/2026 - theo cau 24, 25, 28, 44 tai lieu CĐ day them Bai 1; mot cau mot chu de. Co Lan duyet lai.
    """
    return _lt_mc_chu_de(socau, dang, "chia_het")


def L10_C1_B1_TH014_SA_I_01(socau, dang=2):
    r"""Trả lời ngắn - bốn mệnh đề chứa $\forall$, $\exists$ về chia hết; có bao nhiêu mệnh đề đúng.

    CLAUDE THEM 01/10/2026 - theo cau 44 tai lieu CĐ day them Bai 1 (cung chu de voi MC_M). Co Lan duyet lai.
    """
    return _lt_sa_chu_de(socau, dang, "chia_het")


# =====================================================================
# TH003 - MỆNH ĐỀ CHỨA BIẾN, MỆNH ĐỀ VỀ SỐ CÓ CĂN THỨC
# =====================================================================
def _c1_ham_chua_bien():
    """Mệnh đề chứa biến (một biến) và hàm tính đúng sai: (tên biến, tập, LaTeX P, hàm, cách kiểm tra)."""
    k = random.randint(2, 15)
    d = random.choice([3, 4, 5, 6, 7])
    c = random.randint(1, 5)
    return random.choice([
        ("x", r"\mathbb{R}", r"x + %d \le x^{2}" % k, lambda v: v + k <= v * v,
         lambda v: r"$%s + %d %s %s$" % (_tex_so(v), k, r"\le" if v + k <= v * v else ">", _tex_so(v * v))),
        ("n", r"\mathbb{Z}", r"n^{2} - 1 \text{ is divisible by } %d" % d, lambda v: (v * v - 1) % d == 0,
         lambda v: r"$%s^{2} - 1 = %d$ is%s divisible by $%d$" % (_tex_so(v) if v >= 0 else "(%d)" % v, v * v - 1,
                                                                "" if (v * v - 1) % d == 0 else " not", d)),
        ("x", r"\mathbb{R}", r"x^{2} - %dx < 0" % c, lambda v: v * v - c * v < 0,
         lambda v: r"$%s - %s %s 0$" % (_tex_so(v * v), _tex_so(c * v), "<" if v * v - c * v < 0 else r"\ge")),
        ("n", r"\mathbb{N}", r"n^{2} + n + %d \text{ is prime}" % (2 * c - 1),
         lambda v: _la_nguyen_to(v * v + v + 2 * c - 1),
         lambda v: r"$%d$ %s prime" % (v * v + v + 2 * c - 1, "is" if _la_nguyen_to(v * v + v + 2 * c - 1) else "is not")),
        ("x", r"\mathbb{R}", r"%dx^{2} - 1 < 0" % c, lambda v: c * v * v - 1 < 0,
         lambda v: r"$%d\cdot %s - 1 = %s %s 0$" % (c, _tex_so(v * v), _tex_so(c * v * v - 1), "<" if c * v * v - 1 < 0 else r"\ge")),
    ])


def L10_C1_B1_TH003_MC_A_04(socau, dang=1):
    r"""Cách hỏi khác của _03: cho mệnh đề chứa biến $P(x)$, xét đồng thời hai giá trị:
    ``$P(a)$ đúng và $P(b)$ sai''... (bốn khả năng, một khả năng đúng).

    CLAUDE THEM 01/10/2026 - theo cau 36 tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        for _t in range(200):
            bien, tap, p, f, kt = _c1_ham_chua_bien()
            gia = [v for v in range(-3, 9) if bien == "x" or tap != r"\mathbb{N}" or v >= 0]
            a, b = random.sample(gia, 2)
            if f(a) != f(b) or random.random() < 0.3:
                break
        tt = {True: "true", False: "false"}
        de = r"Given the open sentence $P(%s)$: ``$%s$'' with $%s \in %s$. Which of the following statements is true?" % (bien, p, bien, tap)
        pa = {(u, w): r"$P(%d)$ is %s and $P(%d)$ is %s" % (a, tt[u], b, tt[w]) for u in (True, False) for w in (True, False)}
        giai = r"$P(%d)$: %s, so $P(%d)$ is %s.\\ $P(%d)$: %s, so $P(%d)$ is %s." % (a, kt(a), a, tt[f(a)], b, kt(b), b, tt[f(b)])
        dung = pa[(f(a), f(b))]
        cau += _MC_khong_cham(de, dung, [v for v in pa.values() if v != dung], giai, 0, 0, dang)
    return cau


def L10_C1_B1_TH003_MC_C_01(socau, dang=1):
    r"""Cho $a = \sqrt{m} + k$, $b = \sqrt{m} - k$ ($m$ không chính phương): chọn khẳng định đúng (sai) về
    $a + b$, $a - b$, $ab$, $a^{2} + b^{2}$, $\left(a + b\right)^{2}$ (số tự nhiên, số hữu tỉ, giá trị).

    CLAUDE THEM 01/10/2026 - theo cau 39 tai lieu CĐ day them Bai 1 (a = can10 + 1, b = can10 - 1). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        m = random.choice([v for v in range(2, 40) if math.isqrt(v) ** 2 != v])
        k = random.randint(1, 5)
        if m == k * k:
            m += 1
        hoi_dung = random.choice([True, False])
        S2, P_, H = 2 * (m + k * k), m - k * k, 2 * k
        dung_ds = [(r"$a^{2} + b^{2} = %d$" % S2, r"$a^{2} + b^{2} = \left(m + 2k\sqrt{m} + k^{2}\right) + \left(m - 2k\sqrt{m} + k^{2}\right)$"),
                   (r"$ab = %d$" % P_, r"$ab = \left(\sqrt{%d}\right)^{2} - %d^{2}$" % (m, k)),
                   (r"$a - b = %d$" % H, r"$a - b = 2\cdot %d$" % k),
                   (r"$\left(a + b\right)^{2} = %d$" % (4 * m), r"$a + b = 2\sqrt{%d}$" % m),
                   (r"$a^{2} + b^{2} \in \mathbb{N}$", r"$a^{2} + b^{2} = %d$" % S2)]
        sai_ds = [(r"$a + b \in \mathbb{Q}$", r"$a + b = 2\sqrt{%d}$ is an irrational number" % m),
                  (r"$ab = %d$" % (m + k * k), r"$ab = %d - %d = %d$" % (m, k * k, P_)),
                  (r"$a^{2} + b^{2} = %d$" % (m + k * k), r"$a^{2} + b^{2} = 2\left(%d + %d\right) = %d$" % (m, k * k, S2)),
                  (r"$a - b = 2\sqrt{%d}$" % m, r"$a - b = %d$" % H),
                  (r"$\left(a - b\right)^{2} = %d$" % (4 * m), r"$\left(a - b\right)^{2} = %d$" % (H * H))]
        if hoi_dung:
            chon, khac = random.choice(dung_ds), random.sample(sai_ds, 3)
        else:
            chon, khac = random.choice(sai_ds), random.sample(dung_ds, 3)
        de = (r"Given two numbers $a = \sqrt{%d} + %d$ and $b = \sqrt{%d} - %d$. Which of the following statements is %s?"
              % (m, k, m, k, "true" if hoi_dung else r"\textbf{false}"))
        giai = r"\\ ".join(r"%s is %s because %s." % (t, "true" if (t, l) in dung_ds else "false", l) for t, l in [chon] + khac)
        cau += _MC_khong_cham(de, chon[0], [c[0] for c in khac], giai, 0, 0, dang)
    return cau


def L10_C1_NB001_TH003_TL_A_01(socau, dong=1):
    r"""Tự luận - một câu chứa biến (``$n$ chia hết cho $d$''...).
    a) (NB001) Câu đã cho có phải là mệnh đề không? Vì sao?
    b) (TH003) Thay hai giá trị cụ thể của biến, xét tính đúng sai của hai mệnh đề nhận được.

    CLAUDE THEM 01/10/2026 - theo cau 13, 24 phan tu luan tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        bien, tap, p, f, kt = _c1_ham_chua_bien()
        gia = [v for v in range(0, 25)]
        dung_v = [v for v in gia if f(v)]
        sai_v = [v for v in gia if not f(v)]
        if not dung_v or not sai_v:
            dung_v, sai_v = gia[:1], gia[1:2]
        a, b = random.choice(dung_v), random.choice(sai_v)
        if random.random() < 0.5:
            a, b = b, a
        tap_loi = {r"\mathbb{R}": "a real number", r"\mathbb{Z}": "an integer", r"\mathbb{N}": "a natural number"}[tap]
        de = r"Consider the sentence ``$%s$'' where $%s$ is %s." % (p, bien, tap_loi)
        tt = lambda v: "true" if f(v) else "false"
        ds = [(r"Is the given sentence a statement? Why?",
               r"\text{No, this is an open sentence}",
               r"The given sentence is not yet known to be true or false because it depends on the value of $%s$: it is an open sentence, not a statement." % bien),
              (r"For $%s = %d$ and $%s = %d$, which two statements do we obtain? Determine whether each is true or false." % (bien, a, bien, b),
               r"\text{%s = %d: %s; %s = %d: %s}" % (bien, a, tt(a), bien, b, tt(b)),
               r"For $%s = %d$: %s, the resulting statement is %s.\\ For $%s = %d$: %s, the resulting statement is %s."
               % (bien, a, kt(a), tt(a), bien, b, kt(b), tt(b)))]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau


# =====================================================================
# TỰ LUẬN HAI ĐƠN VỊ MỚI
# =====================================================================
def L10_C1_NB015_TH014_TL_A_01(socau, dong=1):
    r"""Tự luận - cho một định lí ``Nếu P thì Q'' (định lí, tính chất đã học).
    a) (NB015) Phát biểu định lí dưới dạng điều kiện cần, điều kiện đủ.
    b) (TH014) Phát biểu mệnh đề đảo và xét tính đúng sai của nó.

    CLAUDE THEM 01/10/2026 - theo cau 9/10 phan tu luan tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        for _t in range(100):
            P, Q, pq, qp, l_pq, l_qp = _c1_dl_bat_ky()
            if pq:
                break
        de = r"Given the theorem ``If %s, then %s''." % (P, Q)
        ds = [(r"State the given theorem in terms of necessary and sufficient conditions.",
               _c1_tl_dap(r"``%s'' is a sufficient condition for ``%s''; ``%s'' is a necessary condition for ``%s''" % (_c1_hoa(P), Q, _c1_hoa(Q), P)),
               r"Theorem ``If $P$, then $Q$'': $P$ is a sufficient condition for $Q$, and $Q$ is a necessary condition for $P$.\\ ``%s'' is a sufficient condition for ``%s''; ``%s'' is a necessary condition for ``%s''." % (_c1_hoa(P), Q, _c1_hoa(Q), P)),
              (r"State the converse of the given theorem and determine whether the converse is true or false.",
               _c1_tl_dap(r"If %s, then %s; %s" % (Q, P, "true" if qp else "false")),
               r"Converse: ``If %s, then %s''. The converse is %s because %s." % (Q, P, "true" if qp else "false", l_qp))]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau


def L10_C1_NB013_NB005_TL_A_01(socau, dong=1):
    r"""Tự luận - bạn An phát biểu một mệnh đề ``với mọi ...'' (hoặc ``tồn tại ...''), bạn Bình phủ định lại.
    a) (NB013) Dùng kí hiệu $\forall$ ($\exists$) viết mệnh đề của bạn An.
    b) (NB005) Dùng kí hiệu viết mệnh đề phủ định (mệnh đề của bạn Bình).

    CLAUDE THEM 01/10/2026 - theo cau 18/31 phan tu luan tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        m = _lt_bat_ky()
        de = (r"An says: ``%s''. Binh claims that An is wrong and states the negation of that statement."
              % m["loi"])
        ds = [(r"Use the symbol $\forall$ or $\exists$ to write An's statement.", m["tex"],
               r"An's statement: ``$%s$''." % m["tex"]),
              (r"Use the symbol $\forall$ or $\exists$ to write Binh's statement.", m["phu"],
               r"The negation of $\forall$ is $\exists$, the negation of $\exists$ is $\forall$, and we negate the open sentence: ``$%s$''." % m["phu"])]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau


# =====================================================================
# ĐÚNG/SAI CHƯƠNG 1 - mỗi ý NHIỀU phát biểu đúng + NHIỀU phát biểu sai (quy tắc như chương 3, cô Lan)
# a) NB, b) TH, c) VD, d) VDC; mỗi lần chạy mỗi ý có ít nhất 3 phát biểu đúng và 3 phát biểu sai.
# =====================================================================
def _phat_bieu(dung_ds, sai_ds):
    """Gộp phát biểu đúng [(nội dung, lời giải)] và sai thành một ý của TF_baitoan_du (bỏ trùng)."""
    noi_dung_dung = {d for d, _ in dung_ds}
    y, da = [], set()
    for d, l in dung_ds:
        if d not in da:
            da.add(d)
            y.append((r"{\True %s}" % d, "True. " + l))
    for d, l in sai_ds:
        if d in noi_dung_dung or d in da:
            continue
        da.add(d)
        y.append((r"{%s}" % d, "False. " + l))
    return y


def _tf_them(y, dung, sai):
    """Bổ sung phát biểu đúng / sai vào một ý ĐÃ CÓ, bỏ phát biểu trùng nội dung."""
    co = {t.replace("{\\True ", "{") for t, _ in y}
    for t, l in _phat_bieu(dung, sai):
        if t.replace("{\\True ", "{") not in co:
            co.add(t.replace("{\\True ", "{"))
            y.append((t, l))
    return y


def _c1_thuong(t):
    return t[0].lower() + t[1:]


def _tf_dem(mau, k, ly, sai_k, tu="There are exactly"):
    """Phát biểu đếm: đúng 'Có đúng k ...', 'Có ít nhất k - 1 ...' (k >= 2), 'Có không quá k + 1 ...';
    sai 'Có đúng w ...' với w trong sai_k (khác k), 'Có ít nhất k + 1 ...'."""
    dung = [(mau % ("There are exactly", k), ly), (mau % ("There are at most", k + 1), ly)]
    if k >= 2:
        dung.append((mau % ("There are at least", k - 1), ly))
    else:
        dung.append((mau % ("There are at most", k + 2), ly))
    sai = [(mau % ("There are exactly", w), ly) for w in sai_k if w != k and w >= 0]
    sai += [(mau % ("There are at least", k + 1), ly), (mau % ("There are at most", k - 1), ly)] if k >= 1 else [(mau % ("There are at least", k + 1), ly)]
    return dung, sai


# ---------------------------------------------------------------------
# TF_C: cho hai mệnh đề P, Q cụ thể (cùng một loại mệnh đề về số)
# ---------------------------------------------------------------------
def L10_C1_TF_C_01(socau, socot=1):
    r"""Đúng/Sai - cho hai mệnh đề $P$, $Q$ cụ thể về số (cùng một loại: chia hết, số chính phương, số nguyên tố...).
    a) (NB) nhận ra mệnh đề phủ định, mệnh đề kéo theo, mệnh đề đảo, mệnh đề tương đương;
    b) (TH) tính đúng sai của $P$, $Q$, $\overline{P}$, $\overline{Q}$;
    c) (VD) tính đúng sai của $P \Rightarrow Q$, $Q \Rightarrow P$;
    d) (VDC) tính đúng sai của $P \Leftrightarrow Q$, $\overline{P} \Rightarrow \overline{Q}$, $P \Leftrightarrow \overline{Q}$...

    CLAUDE THEM 01/10/2026 - theo cau 8, 9 phan Dung/Sai tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    tt = lambda x: "true" if x else "false"
    for _ in range(socau):
        for lo in _c1_uu_tien("c1_tf_c", 9):
            for _t in range(200):
                p, q = _md_so(lo), _md_so(lo)
                if p["p"] != q["p"] and (p["dung"] != q["dung"] or random.random() < 0.3):
                    break
            else:
                continue
            _c1_danh_dau("c1_tf_c", [lo])
            break
        P, Q = p["dung"], q["dung"]
        debai = (r"Given two statements $P$: ``%s'' and $Q$: ``%s''. Determine whether each of the following statements is true or false." % (p["p"], q["p"]))
        # a) NB - nhận ra dạng mệnh đề
        ly_a = (r"The negation of $P$ is ``%s'', the negation of $Q$ is ``%s''; $P \Rightarrow Q$ is stated as ``If $P$, then $Q$'', its converse is $Q \Rightarrow P$; $P \Leftrightarrow Q$ is stated as ``$P$ if and only if $Q$''." % (p["phu"], q["phu"]))
        y1 = _phat_bieu(
            [(r"The negation of $P$ is ``%s''" % p["phu"], ly_a), (r"The negation of $Q$ is ``%s''" % q["phu"], ly_a),
             (r"The statement $P \Rightarrow Q$ is ``If %s, then %s''" % (_c1_thuong(p["p"]), _c1_thuong(q["p"])), ly_a),
             (r"The converse of $P \Rightarrow Q$ is $Q \Rightarrow P$", ly_a)],
            [(r"The negation of $P$ is ``%s''" % q["p"], ly_a),
             (r"The statement $P \Rightarrow Q$ is ``If %s, then %s''" % (_c1_thuong(q["p"]), _c1_thuong(p["p"])), ly_a),
             (r"The converse of $P \Rightarrow Q$ is $\overline{P} \Rightarrow \overline{Q}$", ly_a),
             (r"The negation of $Q$ is ``%s''" % q["p"], ly_a)])
        # b) TH - đúng sai của P, Q và phủ định
        ly_b = r"$P$ is %s because %s; $Q$ is %s because %s." % (tt(P), p["ly_do"], tt(Q), q["ly_do"])
        y2 = _phat_bieu(
            [(r"$P$ is a %s statement" % tt(P), ly_b), (r"$Q$ is a %s statement" % tt(Q), ly_b),
             (r"$\overline{P}$ is a %s statement" % tt(not P), ly_b), (r"$\overline{Q}$ is a %s statement" % tt(not Q), ly_b)],
            [(r"$P$ is a %s statement" % tt(not P), ly_b), (r"$Q$ is a %s statement" % tt(not Q), ly_b),
             (r"$\overline{P}$ is a %s statement" % tt(P), ly_b), (r"$\overline{Q}$ is a %s statement" % tt(Q), ly_b)])
        # c) VD - kéo theo
        ly_c = ly_b + r" The statement $X \Rightarrow Y$ is false only when $X$ is true and $Y$ is false."
        ghep_c = [(r"P \Rightarrow Q", (not P) or Q), (r"Q \Rightarrow P", (not Q) or P),
                  (r"\overline{P} \Rightarrow Q", P or Q), (r"P \Rightarrow \overline{Q}", (not P) or (not Q)),
                  (r"\overline{Q} \Rightarrow P", Q or P), (r"Q \Rightarrow \overline{P}", (not Q) or (not P))]
        y3 = _phat_bieu([(r"$%s$ is a %s statement" % (t, tt(v)), ly_c) for t, v in ghep_c],
                        [(r"$%s$ is a %s statement" % (t, tt(not v)), ly_c) for t, v in ghep_c])
        # d) VDC - tương đương, kéo theo giữa hai phủ định
        ly_d = ly_b + r" The statement $X \Leftrightarrow Y$ is true when $X$ and $Y$ are both true or both false."
        ghep_d = [(r"P \Leftrightarrow Q", P == Q), (r"\overline{P} \Leftrightarrow \overline{Q}", P == Q),
                  (r"P \Leftrightarrow \overline{Q}", P != Q), (r"\overline{P} \Rightarrow \overline{Q}", P or (not Q)),
                  (r"\overline{Q} \Rightarrow \overline{P}", Q or (not P))]
        y4 = _phat_bieu([(r"$%s$ is a %s statement" % (t, tt(v)), ly_d) for t, v in ghep_d],
                        [(r"$%s$ is a %s statement" % (t, tt(not v)), ly_d) for t, v in ghep_d])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


# ---------------------------------------------------------------------
# TF_D: mệnh đề chứa kí hiệu với mọi, tồn tại và mệnh đề phủ định (cùng một chủ đề)
# ---------------------------------------------------------------------
def _so_chia_du(N, d, ds_du):
    return sum(1 for n in range(0, N + 1) if n % d in ds_du)


def L10_C1_TF_D_01(socau, socot=1):
    r"""Đúng/Sai - hai mệnh đề $A$, $B$ chứa $\forall$, $\exists$ về chia hết (cả câu chỉ một chủ đề: chia hết).
    a) (NB) cách đọc, mệnh đề phủ định; b) (TH) tính đúng sai của $A$, $B$, $\overline{A}$, $\overline{B}$;
    c) (VD) $A \Rightarrow B$, $B \Rightarrow A$, $A \Leftrightarrow B$; d) (VDC) đếm số tự nhiên $n \le N$ làm mệnh đề chứa biến
    về chia hết đúng.

    CLAUDE THEM 01/10/2026 - theo cau 12, 13, 14 phan Dung/Sai tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    tt = lambda x: "true" if x else "false"
    for _ in range(socau):
        cd = "chia_het"                 # một câu một chủ đề: ý d đếm số n làm biểu thức chia hết -> chủ đề chia hết
        ten = "c1_lt_" + cd
        ids = _c1_uu_tien(ten, len(_KHO_LT[cd]()))[:2]
        _c1_danh_dau(ten, ids)
        A, B = _lt(cd, ids[0]), _lt(cd, ids[1])
        debai = (r"Given two statements $A$: ``$%s$'' and $B$: ``$%s$''. Determine whether each of the following statements is true or false." % (A["tex"], B["tex"]))
        # a) NB - đọc, phủ định
        ly_a = (r"The negation of $\forall$ is $\exists$, the negation of $\exists$ is $\forall$, and we negate the open sentence: $\overline{A}$: ``$%s$'', $\overline{B}$: ``$%s$''. $A$ reads as ``%s''." % (A["phu"], B["phu"], A["loi"]))
        y1 = _phat_bieu(
            [(r"The negation of $A$ is ``$%s$''" % A["phu"], ly_a), (r"The negation of $B$ is ``$%s$''" % B["phu"], ly_a),
             (r"Statement $A$ reads as ``%s''" % A["loi"], ly_a),
             (r"Statement $B$ reads as ``%s''" % B["loi"], ly_a)],
            [(r"The negation of $A$ is ``$%s$''" % A["phu_sai"], ly_a), (r"The negation of $B$ is ``$%s$''" % B["phu_sai"], ly_a),
             (r"The negation of $A$ is ``$%s$''" % _lt_tex("E" if A["q"] == "A" else "A", A["tap"], A["p"]), ly_a),
             (r"The negation of $B$ is ``$%s$''" % _lt_tex("E" if B["q"] == "A" else "A", B["tap"], B["p"]), ly_a)])
        # b) TH - đúng sai
        ly_b = r"$A$ is %s because %s; $B$ is %s because %s." % (tt(A["dung"]), A["ly"], tt(B["dung"]), B["ly"])
        vA, vB = A["dung"], B["dung"]
        y2 = _phat_bieu(
            [(r"$A$ is a %s statement" % tt(vA), ly_b), (r"$B$ is a %s statement" % tt(vB), ly_b),
             (r"$\overline{A}$ is a %s statement" % tt(not vA), ly_b), (r"$\overline{B}$ is a %s statement" % tt(not vB), ly_b)],
            [(r"$A$ is a %s statement" % tt(not vA), ly_b), (r"$B$ is a %s statement" % tt(not vB), ly_b),
             (r"$\overline{A}$ is a %s statement" % tt(vA), ly_b), (r"$\overline{B}$ is a %s statement" % tt(vB), ly_b)])
        # c) VD - kéo theo, tương đương giữa A, B
        ly_c = ly_b + r" $X \Rightarrow Y$ is false only when $X$ is true and $Y$ is false; $X \Leftrightarrow Y$ is true when $X$ and $Y$ are both true or both false."
        ghep = [(r"A \Rightarrow B", (not vA) or vB), (r"B \Rightarrow A", (not vB) or vA), (r"A \Leftrightarrow B", vA == vB),
                (r"\overline{A} \Rightarrow B", vA or vB), (r"A \Leftrightarrow \overline{B}", vA != vB)]
        y3 = _phat_bieu([(r"$%s$ is a %s statement" % (t, tt(v)), ly_c) for t, v in ghep],
                        [(r"$%s$ is a %s statement" % (t, tt(not v)), ly_c) for t, v in ghep])
        # d) VDC - đếm số tự nhiên n <= N làm mệnh đề chứa biến (chia hết) đúng
        while True:                     # chỉ lấy biểu thức có ít nhất một số dư thoả mãn
            d = random.choice([3, 4, 5, 7])
            bt, du = random.choice([(r"n^{2} + 1", {r for r in range(d) if (r * r + 1) % d == 0}),
                                (r"n^{2} - 1", {r for r in range(d) if (r * r - 1) % d == 0}),
                                (r"n^{2} + n", {r for r in range(d) if (r * r + r) % d == 0}),
                                (r"n^{2} + 2", {r for r in range(d) if (r * r + 2) % d == 0})])
            if du:
                break
        N = random.choice([20, 25, 30, 40, 50])
        k = _so_chia_du(N, d, du)
        ly_d = (r"Consider the remainder $r$ of $n$ when divided by $%d$: $%s$ is divisible by $%d$ if and only if %s. Counting the natural numbers $n \le %d$ of this kind gives $%d$ numbers." % (d, bt, d,
                                                       (r"$r \in \left\{%s\right\}$" % "; ".join(str(r) for r in sorted(du))) if du else
                                                       r"no remainder satisfies the condition", N, k))
        mau = r"%%s $%%d$ natural numbers $n \le %d$ such that the statement ``$%s$ is divisible by $%d$'' is true" % (N, bt, d)
        dd, ss = _tf_dem(mau, k, ly_d, [k + 1, k - 1, k + 2, len(du) * (N // d)])
        y4 = _phat_bieu(dd, ss)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


# ---------------------------------------------------------------------
# TF_E: mệnh đề chứa biến P(x)
# ---------------------------------------------------------------------
def _p_x():
    """Mệnh đề chứa biến P(x) trên R: dict p (LaTeX), f (Fraction -> bool), ve (Fraction -> (vế trái, vế phải)),
    tap (tập số tự nhiên dùng cho ý d), ly_moi (lí do P(n) đúng với mọi n thuộc tap, nếu có)."""
    k = random.randint(1, 4)
    return random.choice([
        dict(p=r"x > x^{3}", f=lambda v: v > v ** 3, ve=lambda v: (v, v ** 3), tap=r"\mathbb{N}", ly_moi=None),
        dict(p=r"x > \dfrac{1}{x}", f=lambda v: v != 0 and v > 1 / v, ve=lambda v: (v, 1 / v), tap=r"\mathbb{N}^{*}", ly_moi=None),
        dict(p=r"x^{2} \ge %dx" % k if k > 1 else r"x^{2} \ge x", f=lambda v: v * v >= k * v, ve=lambda v: (v * v, k * v),
             tap=r"\mathbb{N}", ly_moi=(r"$n^{2} - n = n\left(n - 1\right) \ge 0$ for all $n \in \mathbb{N}$" if k == 1 else None)),
        dict(p=r"x + %d \le x^{2}" % (k + 1), f=lambda v: v + k + 1 <= v * v, ve=lambda v: (v + k + 1, v * v),
             tap=r"\mathbb{N}", ly_moi=None),
    ])


def _c1_thay(v, ve):
    L, R = ve(v)
    return r"with $x = %s$: the left side is $%s$, the right side is $%s$" % (_tex_so(v), _tex_so(L), _tex_so(R))


def _c1_ng(v):
    return r"\left(%s\right)" % _tex_so(v) if v < 0 or (hasattr(v, "denominator") and v.denominator != 1) else _tex_so(v)


def L10_C1_TF_E_01(socau, socot=1):
    r"""Đúng/Sai - mệnh đề chứa biến $P(x)$ với $x$ là số thực.
    a) (NB) $P(x)$ là mệnh đề chứa biến, $P(a)$ là mệnh đề; b) (TH) $P(a)$ với $a$ nguyên;
    c) (VD) $P(a)$ với $a$ là phân số, số âm; d) (VDC) $\forall x \in \mathbb{N}, P(x)$, $\exists x \in \mathbb{N}, P(x)$,
    số giá trị nguyên $x \in [-5; 5]$ làm $P(x)$ đúng.

    CLAUDE THEM 01/10/2026 - theo cau 18, 29, 35 phan Dung/Sai tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    from fractions import Fraction as F
    cau = ""
    tt = lambda x: "true" if x else "false"
    for _ in range(socau):
        px = _p_x()
        p, f, ve, tap = px["p"], px["f"], px["ve"], px["tap"]
        kt = lambda v: _c1_thay(v, ve)
        debai = r"Given the open sentence $P(x)$: ``$%s$'' with $x$ a real number. Determine whether each of the following statements is true or false." % p
        # a) NB
        ly_a = r"$P(x)$ is neither true nor false as it stands, so it is an open sentence; replacing $x$ with a specific number gives a statement."
        a0 = random.randint(2, 6)
        y1 = _phat_bieu(
            [(r"$P(x)$ is an open sentence", ly_a), (r"$P(%d)$ is a statement" % a0, ly_a), (r"$P(x)$ is not a statement", ly_a)],
            [(r"$P(x)$ is a statement", ly_a), (r"$P(%d)$ is an open sentence" % a0, ly_a), (r"$P(x)$ is a true statement", ly_a),
             (r"$P(x)$ is a false statement", ly_a)])
        # b) TH - giá trị nguyên
        nguyen = [F(v) for v in range(-3, 6) if v != 0]
        dung, sai = [], []
        for v in random.sample(nguyen, 5):
            ly = r"W%s, so $P(%s)$ is %s." % (kt(v)[1:], _tex_so(v), tt(f(v)))
            dung.append((r"$P(%s)$ is a %s statement" % (_tex_so(v), tt(f(v))), ly))
            sai.append((r"$P(%s)$ is a %s statement" % (_tex_so(v), tt(not f(v))), ly))
        y2 = _phat_bieu(dung, sai)
        # c) VD - phân số
        phan = [F(1, 2), F(1, 3), F(-1, 2), F(-1, 3), F(3, 2), F(2, 3), F(-3, 2), F(5, 2)]
        dung, sai = [], []
        for v in random.sample(phan, 5):
            ly = r"W%s, so $P\left(%s\right)$ is %s." % (kt(v)[1:], _tex_so(v), tt(f(v)))
            dung.append((r"$P\left(%s\right)$ is a %s statement" % (_tex_so(v), tt(f(v))), ly))
            sai.append((r"$P\left(%s\right)$ is a %s statement" % (_tex_so(v), tt(not f(v))), ly))
        y3 = _phat_bieu(dung, sai)
        # d) VDC - lượng từ trên N (hoặc N*), đếm số nguyên
        bd = 1 if "*" in tap else 0
        tn = [n for n in range(bd, 200) if f(F(n))]
        moi_n = len(tn) == 200 - bd
        co_n = len(tn) > 0
        ds = [v for v in range(-5, 6) if v != 0 or bd == 0]
        dem = sum(1 for v in ds if f(F(v)))
        if moi_n:
            ly_q = px["ly_moi"] + r", so ``$\forall x \in %s, P(x)$'' is true, and therefore ``$\exists x \in %s, P(x)$'' is also true" % (tap, tap)
        else:
            n0 = next(n for n in range(bd, 200) if not f(F(n)))
            ly_q = r"$P(%d)$ is false (%s), so ``$\forall x \in %s, P(x)$'' is false" % (n0, _c1_thay(F(n0), ve), tap)
            ly_q += ((r"; $P(%d)$ is true (%s), so ``$\exists x \in %s, P(x)$'' is true" % (tn[0], _c1_thay(F(tn[0]), ve), tap)) if co_n
                     else r"; there is no $x \in %s$ that makes $P(x)$ true, so ``$\exists x \in %s, P(x)$'' is false" % (tap, tap))
        ly_d = (r"%s. The integers $x \in [-5; 5]$%s that make $P(x)$ true: $%s$ (there are $%d$ of them)."
                % (ly_q, r" ($x \ne 0$)" if bd else "", "; ".join(str(v) for v in ds if f(F(v))) or r"\varnothing", dem))
        d1, s1 = _tf_dem(r"%s $%d$ integers $x \in [-5; 5]$ such that $P(x)$ is a true statement", dem, ly_d, [dem + 1, dem - 1, len(ds) - dem])
        d1 += [(r"The statement ``$\forall x \in %s, P(x)$'' is %s" % (tap, tt(moi_n)), ly_d), (r"The statement ``$\exists x \in %s, P(x)$'' is %s" % (tap, tt(co_n)), ly_d)]
        s1 += [(r"The statement ``$\forall x \in %s, P(x)$'' is %s" % (tap, tt(not moi_n)), ly_d), (r"The statement ``$\exists x \in %s, P(x)$'' is %s" % (tap, tt(not co_n)), ly_d)]
        y4 = _phat_bieu(d1, s1)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


# ---------------------------------------------------------------------
# TF_F: biểu thức P(n) = n^2 - an + b với n là số tự nhiên
# ---------------------------------------------------------------------
def L10_C1_TF_F_01(socau, socot=1):
    r"""Đúng/Sai - cho $P(n) = n^{2} - an + b$ với $n$ là số tự nhiên.
    a) (NB) giá trị $P(k)$; b) (TH) $P(k)$ chia hết cho $d$, là số chẵn / lẻ; c) (VD) mệnh đề chứa $\forall$, $\exists$
    về tính chẵn lẻ, dấu của $P(n)$; d) (VDC) số tự nhiên $n$ để $\dfrac{2P(n) - 1}{n - c}$ là số nguyên.

    CLAUDE THEM 01/10/2026 - theo cau 5 phan Dung/Sai tai lieu CĐ day them Bai 1 (P(n) = n^2 - 6n + 10). Co Lan duyet lai.
    """
    cau = ""
    tt = lambda x: "true" if x else "false"
    for _ in range(socau):
        a = random.randint(2, 7)
        b = random.randint(a * a // 4 + 1, a * a // 4 + 8)           # P(n) > 0 với mọi n
        P = lambda n: n * n - a * n + b
        bt = r"n^{2} - %dn + %d" % (a, b)
        debai = r"Given $P(n) = %s$ where $n$ is a natural number. Determine whether each of the following statements is true or false." % bt
        # a) NB - giá trị
        dung, sai = [], []
        for k in random.sample(range(0, 7), 4):
            ly = r"$P(%d) = %d^{2} - %d\cdot %d + %d = %d$." % (k, k, a, k, b, P(k))
            dung.append((r"$P(%d) = %d$" % (k, P(k)), ly))
            for w in (P(k) + 2 * a * k, k * k + a * k + b, P(k) - 1):
                if w != P(k):
                    sai.append((r"$P(%d) = %d$" % (k, w), ly))
        y1 = _phat_bieu(dung, sai[:6])
        # b) TH - chia hết, chẵn lẻ
        dung, sai = [], []
        for k in random.sample(range(0, 8), 4):
            d = random.choice([2, 3, 5])
            v = P(k)
            ly = r"$P(%d) = %d$." % (k, v)
            (dung if v % d == 0 else sai).append((r"$P(%d)$ is divisible by $%d$" % (k, d), ly))
            (sai if v % d == 0 else dung).append((r"$P(%d)$ is not divisible by $%d$" % (k, d), ly))
            (dung if v % 2 else sai).append((r"$P(%d)$ is odd" % k, ly))
            (sai if v % 2 else dung).append((r"$P(%d)$ is even" % k, ly))
        y2 = _phat_bieu(dung, sai)
        # c) VD - lượng từ về chẵn lẻ, dấu
        luon_cung = a % 2 == 1          # n^2 - an = n(n - a) luôn chẵn khi a lẻ
        ly_c = ((r"$n^{2} - %dn = n\left(n - %d\right)$; $n$ and $n - %d$ have opposite parity, so their product is always even, hence $P(n)$ always has the same parity as $%d$." % (a, a, a, b)) if luon_cung else
                (r"$n^{2} - %dn$ has the same parity as $n^{2}$, that is, as $n$; so $P(n)$ is sometimes even and sometimes odd ($P(0) = %d$, $P(1) = %d$)." % (a, P(0), P(1))))
        ly_c += r" Also, $P(n) = \left(n - \dfrac{%d}{2}\right)^{2} + %s > 0$." % (a, _tex_so(Rational(4 * b - a * a, 4)))
        ca_le = luon_cung and b % 2 == 1
        ca_chan = luon_cung and b % 2 == 0
        y3 = _phat_bieu(
            [(r"The statement ``$\forall n \in \mathbb{N},\ P(n) \text{ is odd}$'' is %s" % tt(ca_le), ly_c),
             (r"The statement ``$\exists n \in \mathbb{N},\ P(n) \text{ is even}$'' is %s" % tt(not ca_le), ly_c),
             (r"The statement ``$\forall n \in \mathbb{N},\ P(n) > 0$'' is true", ly_c),
             (r"The statement ``$\exists n \in \mathbb{N},\ P(n) \text{ is odd}$'' is %s" % tt(not ca_chan), ly_c)],
            [(r"The statement ``$\forall n \in \mathbb{N},\ P(n) \text{ is odd}$'' is %s" % tt(not ca_le), ly_c),
             (r"The statement ``$\exists n \in \mathbb{N},\ P(n) \text{ is even}$'' is %s" % tt(ca_le), ly_c),
             (r"The statement ``$\exists n \in \mathbb{N},\ P(n) \le 0$'' is true", ly_c),
             (r"The statement ``$\exists n \in \mathbb{N},\ P(n) \text{ is odd}$'' is %s" % tt(ca_chan), ly_c)])
        # d) VDC - (2P(n) - 1)/(n - c) nguyên
        c = random.choice([v for v in range(1, 7) if v != a])
        M = 2 * P(c) - 1
        uoc = [u for u in range(1, abs(M) + 1) if M % u == 0]
        nn = sorted({c + u for u in uoc} | {c - u for u in uoc if c - u >= 0})
        k = len(nn)
        ly_d = (r"$2P(n) - 1 = 2n^{2} - %dn + %d$. Dividing by $n - %d$: $2P(n) - 1 = \left(n - %d\right)\left(2n %s\right) + %d$, so $\dfrac{2P(n) - 1}{n - %d}$ is an integer if and only if $n - %d$ is a divisor of $%d$. For natural $n$, $n \ne %d$: $n \in \left\{%s\right\}$, so there are $%d$ such numbers." % (2 * a, 2 * b - 1, c, c, "%s %d" % ("+" if c >= a else "-", abs(2 * c - 2 * a)), M, c, c, M, c,
                                                       "; ".join(map(str, nn)), k))
        mau = r"%%s $%%d$ natural numbers $n$ such that $\dfrac{2P(n) - 1}{n - %d}$ is an integer" % c
        dd, ss = _tf_dem(mau, k, ly_d, [len(uoc), 2 * len(uoc), k + 1])
        y4 = _phat_bieu(dd, ss)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


# ---------------------------------------------------------------------
# TF_G: số hoàn hảo
# ---------------------------------------------------------------------
def _tong_uoc_that_su(n):
    return sum(d for d in range(1, n) if n % d == 0)


def L10_C1_TF_G_01(socau, socot=1):
    r"""Đúng/Sai - khái niệm mới ``số hoàn hảo'' (số nguyên dương bằng tổng các ước nguyên dương thực sự của nó).
    a) (NB) ước thực sự của một số; b) (TH) một số nhỏ có là số hoàn hảo không; c) (VD) mệnh đề chứa $\forall$, $\exists$
    về số hoàn hảo (số nguyên tố, luỹ thừa của $2$, số nhỏ hơn $10$...); d) (VDC) số lớn ($496$, $8128$, $2020$...).

    CLAUDE THEM 01/10/2026 - theo cau 7 phan Dung/Sai tai lieu CĐ day them Bai 1. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        debai = (r"A positive integer $n$ is called a \textbf{perfect number} if $n$ equals the sum of its proper positive divisors (the positive divisors other than $n$). Determine whether each of the following statements is true or false.")
        # a) NB - ước thực sự
        dung, sai = [], []
        for n in random.sample([8, 10, 12, 14, 15, 16, 18, 20, 21, 22], 3):
            u = [d for d in range(1, n) if n % d == 0]
            ly = r"The proper positive divisors of $%d$ are $%s$." % (n, "; ".join(map(str, u)))
            dung.append((r"The proper positive divisors of $%d$ are $%s$" % (n, "; ".join(map(str, u))), ly))
            sai.append((r"The proper positive divisors of $%d$ are $%s$" % (n, "; ".join(map(str, u + [n]))), ly))
            sai.append((r"The proper positive divisors of $%d$ are $%s$" % (n, "; ".join(map(str, u[1:]))), ly))
        y1 = _phat_bieu(dung, sai)
        # b) TH - số nhỏ
        dung, sai = [], []
        for n in random.sample([6, 8, 10, 12, 14, 18, 20, 24, 28], 5):
            s = _tong_uoc_that_su(n)
            ly = r"The sum of the proper divisors of $%d$ is $%d$." % (n, s)
            (dung if s == n else sai).append((r"$%d$ is a perfect number" % n, ly))
            (sai if s == n else dung).append((r"$%d$ is not a perfect number" % n, ly))
        y2 = _phat_bieu(dung, sai)
        # c) VD - lượng từ
        ly_c = (r"A prime $p$ has exactly one proper divisor, $1 < p$; the sum of the proper divisors of $2^{k}$ is $1 + 2 + \ldots + 2^{k - 1} = 2^{k} - 1 < 2^{k}$; among the numbers from $1$ to $9$, only $6 = 1 + 2 + 3$ is a perfect number.")
        y3 = _phat_bieu(
            [(r"No prime is a perfect number", ly_c), (r"There is exactly one perfect number less than $10$", ly_c),
             (r"No power $2^{k}$ ($k \in \mathbb{N}^{*}$) is a perfect number", ly_c),
             (r"There exists a perfect number that is even", ly_c)],
            [(r"There exists a prime that is a perfect number", ly_c), (r"There is no perfect number less than $10$", ly_c),
             (r"There is a perfect number of the form $2^{k}$ ($k \in \mathbb{N}^{*}$)", ly_c), (r"There are exactly two perfect numbers less than $10$", ly_c)])
        # d) VDC - số lớn
        dung, sai = [], []
        for n in random.sample([496, 8128, 2020, 2024, 500, 1000, 1024, 2026], 5):
            s = _tong_uoc_that_su(n)
            u = [d for d in range(1, n) if n % d == 0]
            ly = r"The proper divisors of $%d$ are $%s$, and their sum is $%d$." % (n, "; ".join(map(str, u)), s)
            (dung if s == n else sai).append((r"$%d$ is a perfect number" % n, ly))
            (sai if s == n else dung).append((r"$%d$ is not a perfect number" % n, ly))
        y4 = _phat_bieu(dung, sai)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


# =====================================================================
# BÀI 2 - BỔ SUNG TỪ TÀI LIỆU CĐ DẠY THÊM TOÁN 10 BÀI 2 (file docx cô Lan gửi 01/10/2026)
# CLAUDE THEM 01/10/2026 - co Lan duyet lai. Chỉ lấy dạng trong YCCĐ của Bộ; mỗi câu một chủ đề;
# kho mệnh đề / bối cảnh lấy xoay vòng (_c1_uu_tien, _c1_danh_dau) như Bài 1.
# =====================================================================
from itertools import combinations as _b2_tohop


def _b2_tap(ds):
    """Tập liệt kê: số (sắp tăng) hoặc chữ (giữ thứ tự); rỗng -> \\varnothing."""
    ds = list(dict.fromkeys(ds))
    if not ds:
        return r"\varnothing"
    if all(not isinstance(v, str) for v in ds):
        return _tap(ds)
    return r"\left\{%s\right\}" % "; ".join(ds)


def _b2_liet_ke_tap_con(ds):
    """Liệt kê mọi tập con của ds theo số phần tử (lời giải)."""
    dong = []
    for k in range(len(ds) + 1):
        con = [_b2_tap(list(c)) for c in _b2_tohop(ds, k)]
        ten = "no elements" if k == 0 else "$%d$ element(s)" % k
        dong.append(r"subsets with %s: $%s$" % (ten, "$, $".join(con)))
    return "; ".join(dong)


def _b2_nhieu_so(dap, ung, tran=None):
    """Ba số nhiễu khác đáp số, không âm, khác nhau."""
    ra = []
    for x in list(ung) + [dap + 1, dap - 1, dap + 2, 2 * dap, dap + 3]:
        if isinstance(x, int) and x >= 0 and x != dap and x not in ra and (tran is None or x <= tran):
            ra.append(x)
    return ra[:3]


# ---------------------------------------------------------------------
# NB017_MC_J / SA_B: đếm số tập con (tập nhỏ, lời giải liệt kê hết các tập con)
# ---------------------------------------------------------------------
def _b2_tap_nho():
    """Một tập 2 - 4 phần tử: (cách cho trong đề, danh sách phần tử, câu giải thích để liệt kê)."""
    kieu = random.randint(0, 4)
    if kieu == 0:                                   # liệt kê số
        ds = sorted(random.sample(range(-5, 13), random.randint(2, 4)))
        return _tap(ds), ds, ""
    if kieu == 1:                                   # liệt kê chữ
        bo = random.choice([["a", "b", "c", "d"], ["x", "y", "z", "t"], ["m", "n", "p", "q"]])
        ds = bo[:random.randint(2, 4)]
        return _b2_tap(ds), ds, ""
    if kieu == 2:                                   # {x thuộc Z | |x| < k}, k = 2 -> 3 phần tử
        k = 2
        ds = list(range(-k + 1, k))
        return (r"\left\{x \in \mathbb{Z} \mid |x| < %d\right\}" % k, ds,
                r"Since $|x| < %d$ and $x$ is an integer, $x \in %s$. " % (k, _tap(ds)))
    if kieu == 3:                                   # {x thuộc N | a <= x < b}
        a = random.randint(0, 6)
        ds = list(range(a, a + random.randint(2, 4)))
        return (r"\left\{x \in \mathbb{N} \mid %d \le x < %d\right\}" % (a, ds[-1] + 1), ds,
                r"The natural numbers $x$ satisfying $%d \le x < %d$ are $%s$. " % (a, ds[-1] + 1, "; ".join(map(str, ds))))
    for _ in range(50):                             # tập nghiệm phương trình tích trên N hoặc Z
        tap = random.choice([r"\mathbb{N}", r"\mathbb{Z}"])
        de, dung, _s, giai = _tap_dac_trung_4(tap)
        dung = sorted(set(dung), key=float)
        if 2 <= len(dung) <= 3:
            return de, [int(v) for v in dung], giai + " "
    return _b2_tap_nho()


def _b2_hoi_tap_con(ds, kieu):
    """(câu hỏi, đáp số, lời giải ngắn, ứng viên nhiễu) cho tập ds."""
    n = len(ds)
    tat = 2 ** n
    if kieu == "tat_ca":
        return ("subsets", tat, r"Therefore there are $%d$ subsets in total." % tat, [n, 2 * n, tat - 1, n * n])
    if kieu == "khac_rong":
        return ("nonempty subsets", tat - 1,
                r"Excluding $\varnothing$, there remain $%d - 1 = %d$ nonempty subsets." % (tat, tat - 1), [tat, n, tat - 2])
    if kieu == "chua":
        a = random.choice(ds)
        a_tex = a if isinstance(a, str) else "%d" % a
        dem = 2 ** (n - 1)
        return (r"subsets containing the element $%s$" % a_tex, dem,
                r"Among the subsets above, $%d$ contain the element $%s$." % (dem, a_tex), [tat, dem - 1, n, tat - 1])
    k = random.randint(1, n - 1)
    dem = math.comb(n, k)
    return (r"subsets with exactly $%d$ elements" % k, dem,
            r"There are $%d$ subsets with exactly $%d$ elements." % (dem, k), [k, n, tat, dem + 1])


def _b2_cau_tap_con(kieu_ds):
    """Sinh (đề, đáp số, lời giải, nhiễu) - đếm tập con của một tập nhỏ."""
    de, ds, giai_lk = _b2_tap_nho()
    kieu = random.choice(kieu_ds)
    hoi, dap, ket, ung = _b2_hoi_tap_con(ds, kieu)
    debai = r"Given the set $A = %s$. How many %s does the set $A$ have?" % (de, hoi)
    giai = (giai_lk + (r"Hence $A = %s$. " % _b2_tap(ds) if giai_lk else "")
            + r"List the subsets of $A$: " + _b2_liet_ke_tap_con(ds) + r".\\ " + ket)
    return debai, dap, giai, ung


def L10_C1_B2_NB017_MC_J_01(socau, dang=1):
    r"""Đếm số tập con của một tập hợp nhỏ (2 - 4 phần tử, cho bằng liệt kê hoặc tính chất đặc trưng):
    số tập con, số tập con khác rỗng, số tập con có đúng $k$ phần tử, số tập con chứa một phần tử cho trước.
    Lời giải liệt kê hết các tập con (không dùng công thức tổ hợp).

    CLAUDE THEM 01/10/2026 - theo cau 6, MC 20, 23, 25, 35, 36, 38 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        debai, dap, giai, ung = _b2_cau_tap_con(["tat_ca", "khac_rong", "k", "chua"])
        cau += MC_SA_answer_text(debai, "$%d$" % dap, ["$%d$" % x for x in _b2_nhieu_so(dap, ung)], giai, 0, 0, dang)
    return cau


def _b2_cau_x_giua():
    """Số tập X thoả A ⊂ X ⊂ B (B có thêm 1 - 3 phần tử so với A)."""
    chu = random.random() < 0.4
    if chu:
        goc = random.choice([["a", "b", "c", "d", "e"], ["m", "n", "p", "q", "r"], ["x", "y", "z", "t", "u"]])
    else:
        goc = sorted(random.sample(range(0, 12), 5))
    k = random.randint(1, 3)
    e = random.randint(1, min(3, 5 - k))
    A = goc[:k]
    them = goc[k:k + e]
    B = A + them
    if not chu:
        B = sorted(B)
    dem = 2 ** e
    cac_X = [_b2_tap(A + list(c) if chu else sorted(A + list(c))) for j in range(e + 1) for c in _b2_tohop(them, j)]
    giai = (r"$X$ must contain every element of $%s$ and can only additionally contain elements of $%s$. The sets $X$ are: $%s$.\\ Therefore there are $%d$ sets $X$." % (_b2_tap(A), _b2_tap(them), "$, $".join(cac_X), dem))
    debai = r"How many sets $X$ satisfy $%s \subset X \subset %s$?" % (_b2_tap(A), _b2_tap(B))
    return debai, dem, giai, [e, len(B), 2 ** len(B), dem - 1, dem + 2]


def L10_C1_B2_NB017_MC_J_02(socau, dang=1):
    r"""Cách hỏi khác của MC_J_01: đếm số tập $X$ thoả mãn $A \subset X \subset B$ ($A$, $B$ liệt kê;
    $B$ có thêm 1 - 3 phần tử). Lời giải liệt kê hết các tập $X$.

    CLAUDE THEM 01/10/2026 - theo cau 9 (phan dang), MC 37 tai lieu CĐ day them Bai 2 (cau 9 tai lieu chi ra
    2 tap, thieu 6 tap). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        debai, dap, giai, ung = _b2_cau_x_giua()
        cau += MC_SA_answer_text(debai, "$%d$" % dap, ["$%d$" % x for x in _b2_nhieu_so(dap, ung)], giai, 0, 0, dang)
    return cau


def L10_C1_B2_NB017_SA_B_01(socau, dang=2):
    r"""Trả lời ngắn - đếm số tập con (như MC_J_01) hoặc số tập $X$ thoả $A \subset X \subset B$ (như MC_J_02).

    CLAUDE THEM 01/10/2026 - ban tra loi ngan cua NB017_MC_J (cung Dang). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.6:
            debai, dap, giai, ung = _b2_cau_tap_con(["tat_ca", "khac_rong", "k", "chua"])
        else:
            debai, dap, giai, ung = _b2_cau_x_giua()
        cau += MC_SA_answer_const(debai, str(dap), [str(x) for x in _b2_nhieu_so(dap, ung)], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB017_MC_K / SA_D: hai tập hợp bằng nhau
# ---------------------------------------------------------------------
def _b2_pt2(r1, r2):
    """Phương trình bậc hai có hai nghiệm nguyên r1, r2 (viết x^2 - Sx + P = 0)."""
    return _tex_bac2(1, -(r1 + r2), r1 * r2) + " = 0"


def _b2_cap_bang(bang, kieu=None):
    """Một cặp tập (X, Y) bằng nhau (bang=True) hoặc không bằng nhau, kèm lời giải (kiểu 0 - 5)."""
    if kieu is None:
        kieu = random.randint(0, 5)
    if kieu == 0:
        r1, r2 = random.sample([v for v in range(-5, 7) if v], 2)
        X = r"\left\{x \in \mathbb{R} \mid %s\right\}" % _b2_pt2(r1, r2)
        Y = _tap([r1, r2]) if bang else random.choice([_tap([r1, -r2]), _tap([-r1, -r2]), _tap([r1])])
        ly = r"$%s \Leftrightarrow x = %d$ or $x = %d$, so $X = %s$" % (_b2_pt2(r1, r2), r1, r2, _tap([r1, r2]))
        return X, Y, ly
    if kieu == 1:
        k = random.randint(3, 6)
        X = r"\left\{x \in \mathbb{N} \mid x < %d\right\}" % k
        dung = list(range(0, k))
        Y = _tap(dung) if bang else random.choice([_tap(range(1, k)), _tap(range(0, k + 1))])
        return X, Y, r"The natural numbers less than $%d$ are $%s$, so $X = %s$" % (k, "; ".join(map(str, dung)), _tap(dung))
    if kieu == 2:
        a = random.randint(-4, 0)
        b = a + random.randint(3, 5)
        X = r"\left\{x \in \mathbb{Z} \mid %d < x \le %d\right\}" % (a, b)
        dung = list(range(a + 1, b + 1))
        Y = _tap(dung) if bang else random.choice([_tap(range(a, b + 1)), _tap(range(a + 1, b)), _tap(range(a, b))])
        return X, Y, r"The integers $x$ satisfying $%d < x \le %d$ are $%s$, so $X = %s$" % (a, b, "; ".join(map(str, dung)), _tap(dung))
    if kieu == 3:
        cs = random.choice([2, 3])
        hi = random.randint(3, 4)
        X = r"\left\{%d^{n} \mid n \in \mathbb{N},\ 1 \le n \le %d\right\}" % (cs, hi)
        dung = [cs ** i for i in range(1, hi + 1)]
        Y = _tap(dung) if bang else random.choice([_tap([cs ** i for i in range(0, hi + 1)]), _tap([cs ** i for i in range(1, hi)])])
        return X, Y, r"For $n = 1; \ldots; %d$ we get $X = %s$" % (hi, _tap(dung))
    if kieu == 4:
        c = random.randint(1, 9)
        X = r"\left\{x \in \mathbb{R} \mid x^{2} + %d = 0\right\}" % c
        Y = r"\varnothing" if bang else random.choice([r"\left\{0\right\}", r"\left\{\varnothing\right\}", _tap([-c, c])])
        return X, Y, r"$x^{2} + %d > 0$ for all $x$, so the equation has no solution, $X = \varnothing$" % c
    k = random.choice([6, 8, 10, 12, 15, 18, 20])
    dung = [d for d in range(1, k + 1) if k % d == 0]
    X = r"\left\{n \in \mathbb{N} \mid n \text{ is a divisor of } %d\right\}" % k
    Y = _tap(dung) if bang else random.choice([_tap(dung[1:]), _tap(dung[:-1]), _tap(dung + [2 * k])])
    return X, Y, r"The natural divisors of $%d$ are $%s$, so $X = %s$" % (k, "; ".join(map(str, dung)), _tap(dung))


def L10_C1_B2_NB017_MC_K_01(socau, dang=1):
    r"""Hai tập hợp bằng nhau: trong bốn cặp tập hợp (một tập cho bởi tính chất đặc trưng, một tập liệt kê),
    chọn cặp bằng nhau (hoặc cặp KHÔNG bằng nhau).

    CLAUDE THEM 01/10/2026 - theo cau 10, 14 (phan dang) tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        hoi_bang = random.random() < 0.6
        kieu = random.sample(range(6), 4)            # bốn cặp thuộc bốn kiểu khác nhau
        cap = [_b2_cap_bang(hoi_bang, kieu[0])] + [_b2_cap_bang(not hoi_bang, k) for k in kieu[1:]]
        pa = [r"$X = %s$ and $Y = %s$" % (X, Y) for X, Y, _ in cap]
        debai = r"Which of the following pairs of sets %s?" % ("are equal" if hoi_bang else r"are \textbf{not} equal")
        giai = r"\\ ".join(r"%s; the set obtained %s $Y$, so $X %s Y$." % (ly, "matches" if (i == 0) == hoi_bang else "is different from",
                                                         "=" if (i == 0) == hoi_bang else r"\ne")
                          for i, (_, _, ly) in enumerate(cap))
        cau += MC_SA_answer_text(debai, pa[0], pa[1:], giai, 0, 0, dang)
    return cau


def _b2_tim_m_bang():
    """A = tập nghiệm phương trình bậc hai (2 nghiệm nguyên), B = {r1; m + k}: tìm m để A = B."""
    r1, r2 = random.sample([v for v in range(-6, 8) if v], 2)
    k = random.choice([0, 0, 1, -1, 2, -2, 3])
    phan = "m" if k == 0 else (r"m %s %d" % ("+" if k > 0 else "-", abs(k)))
    m = r2 - k
    debai = (r"Given two sets $A = \left\{x \in \mathbb{R} \mid %s\right\}$ and $B = \left\{%d; %s\right\}$. Find $m$ such that $A = B$." % (_b2_pt2(r1, r2), r1, phan))
    giai = (r"$%s \Leftrightarrow x = %d$ or $x = %d$, so $A = %s$.\\ $A = B$ if and only if $%s = %d$, that is, $m = %d$." % (_b2_pt2(r1, r2), r1, r2, _tap([r1, r2]), phan, r2, m))
    ung = []
    for v in [r2, -r2 - k, r1 - k, r1, -m, r2 + k, m + 1, m - 1, m + 2]:
        if v != m and v not in ung:
            ung.append(v)
    return debai, m, giai, ung


def L10_C1_B2_NB017_MC_K_02(socau, dang=1):
    r"""Cách hỏi khác của MC_K_01: tìm phần tử (tham số) để hai tập hợp bằng nhau - hoặc
    $A = \{a; b\}$, $B = \{b; x\}$, $C = \{a; y\}$ tìm $x$, $y$ để $A = B = C$; hoặc $A$ là tập nghiệm của phương
    trình bậc hai, $B = \{r; m + k\}$ tìm $m$ để $A = B$.

    CLAUDE THEM 01/10/2026 - theo TF 38, TL 47 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        if random.random() < 0.4:
            a, b = random.sample(range(-5, 10), 2)
            debai = (r"Given three sets $A = \left\{%d; %d\right\}$, $B = \left\{%d; x\right\}$ and $C = \left\{%d; y\right\}$. The values of $x$ and $y$ such that $A = B = C$ are" % (a, b, b, a))
            dung = r"$x = %d$, $y = %d$" % (a, b)
            nhieu = [r"$x = %d$, $y = %d$" % (b, a), r"$x = %d$, $y = %d$" % (a, a), r"$x = %d$, $y = %d$" % (b, b)]
            giai = (r"$B = A$ and $%d \in B$, so $x$ must be the remaining element of $A$: $x = %d$. Similarly, $C = A$ gives $y = %d$." % (b, a, b))
            cau += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
        else:
            debai, m, giai, ung = _b2_tim_m_bang()
            nh = [v for v in dict.fromkeys(ung) if v != m][:3]
            cau += MC_SA_answer_text(debai.replace("Find $m$ such that $A = B$.", "The value of $m$ such that $A = B$ is"),
                                     "$m = %d$" % m, ["$m = %d$" % v for v in nh], giai, 0, 0, dang)
    return cau


def L10_C1_B2_NB017_SA_D_01(socau, dang=2):
    r"""Trả lời ngắn - tìm $m$ để hai tập hợp bằng nhau ($A$ là tập nghiệm của phương trình bậc hai,
    $B = \{r; m + k\}$).

    CLAUDE THEM 01/10/2026 - ban tra loi ngan cua NB017_MC_K (cung Dang). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        debai, m, giai, ung = _b2_tim_m_bang()
        nh = [v for v in dict.fromkeys(ung) if v != m][:3]
        cau += MC_SA_answer_const(debai, str(m), [str(v) for v in nh], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB017_MC_G_04, _05, SA_A_03: liệt kê / đếm phần tử - tập {f(k) | k ...} và phương trình tích có nhân tử bậc hai
# ---------------------------------------------------------------------
def _b2_tap_anh():
    """Tập {f(k) | k thuộc Z (N), điều kiện}: (đề, danh sách phần tử đúng, các danh sách sai, lời giải).
    Bẫy: nhiều giá trị k cho cùng một phần tử (k^2 + c, k^2 - ak, |k|...) và nhầm tập k với tập f(k)."""
    loai = random.randint(0, 3)
    if loai <= 1:
        t = random.randint(2, 3)
        dk, cac_k = r"k \in \mathbb{Z},\ |k| \le %d" % t, list(range(-t, t + 1))
    else:
        a = random.randint(1, 3)
        b = random.randint(2, 4)
        dk, cac_k = r"k \in \mathbb{Z},\ -%d < k \le %d" % (a, b), list(range(-a + 1, b + 1))
    if loai in (0, 2):
        c = random.choice([-3, -1, 1, 2, 3])
        bt = r"k^{2} %s %d" % ("+" if c > 0 else "-", abs(c))
        f = lambda k: k * k + c
    elif loai == 1:
        p = random.choice([2, 3])
        q = random.choice([-1, 1, 2])
        bt = r"%dk %s %d" % (p, "+" if q > 0 else "-", abs(q))
        f = lambda k: p * k + q
    else:
        a2 = random.choice([1, 2])
        bt = r"k^{2} - %sk" % ("" if a2 == 1 else "%d" % a2)
        f = lambda k: k * k - a2 * k
    gt = [f(k) for k in cac_k]
    dung = sorted(set(gt))
    sai = [cac_k, sorted(set(f(k) for k in cac_k[1:])), sorted(set(f(k) for k in cac_k[:-1])),
           sorted(set(f(k) for k in cac_k + [cac_k[-1] + 1])), sorted(set(f(-k) + 1 for k in cac_k)) if loai == 1 else
           sorted(set(gt[i] for i in range(len(gt)) if cac_k[i] >= 0))]
    de = r"\left\{%s \mid %s\right\}" % (bt, dk)
    giai = (r"$%s$, so $k \in \left\{%s\right\}$. Substituting each in turn: %s. Equal values are written only once."
            % (dk.replace(r"k \in \mathbb{Z},\ ", r"k \in \mathbb{Z}$, $"), "; ".join(map(str, cac_k)),
               "; ".join(r"$k = %d \Rightarrow %d$" % (k, v) for k, v in zip(cac_k, gt))))
    return de, dung, [s for s in sai if s != dung], giai


_B2_NHAN_TU2 = [  # (LaTeX nhân tử bậc hai, các nghiệm thực (sympy), lời giải ngắn)
    (r"\left(x^{2} - 4\right)", [-2, 2], r"x^{2} - 4 = 0 \Leftrightarrow x = \pm 2"),
    (r"\left(x^{2} - 9\right)", [-3, 3], r"x^{2} - 9 = 0 \Leftrightarrow x = \pm 3"),
    (r"\left(x^{2} - 2\right)", [-sqrt(2), sqrt(2)], r"x^{2} - 2 = 0 \Leftrightarrow x = \pm \sqrt{2}"),
    (r"\left(x^{2} - 3\right)", [-sqrt(3), sqrt(3)], r"x^{2} - 3 = 0 \Leftrightarrow x = \pm \sqrt{3}"),
    (r"\left(x^{2} + 1\right)", [], r"x^{2} + 1 = 0 \text{ has no solution}"),
    (r"\left(x^{2} + 4\right)", [], r"x^{2} + 4 = 0 \text{ has no solution}"),
    (r"\left(x^{2} - 3x + 2\right)", [1, 2], r"x^{2} - 3x + 2 = 0 \Leftrightarrow x = 1 \text{ or } x = 2"),
    (r"\left(x^{2} - x - 6\right)", [-2, 3], r"x^{2} - x - 6 = 0 \Leftrightarrow x = -2 \text{ or } x = 3"),
    (r"\left(2x^{2} - 5x + 2\right)", [Rational(1, 2), 2], r"2x^{2} - 5x + 2 = 0 \Leftrightarrow x = 2 \text{ or } x = \dfrac{1}{2}"),
    (r"\left(2x^{2} - 3x + 1\right)", [Rational(1, 2), 1], r"2x^{2} - 3x + 1 = 0 \Leftrightarrow x = 1 \text{ or } x = \dfrac{1}{2}"),
    (r"\left(3x^{2} - 10x + 3\right)", [Rational(1, 3), 3], r"3x^{2} - 10x + 3 = 0 \Leftrightarrow x = 3 \text{ or } x = \dfrac{1}{3}"),
    (r"\left(x^{2} - 5x + 6\right)", [2, 3], r"x^{2} - 5x + 6 = 0 \Leftrightarrow x = 2 \text{ or } x = 3"),
    (r"\left(x^{3} - 9x\right)", [-3, 0, 3], r"x^{3} - 9x = x\left(x^{2} - 9\right) = 0 \Leftrightarrow x = 0 \text{ or } x = \pm 3"),
    (r"\left(x^{4} - 5x^{2} + 4\right)", [-2, -1, 1, 2], r"x^{4} - 5x^{2} + 4 = 0 \Leftrightarrow x^{2} = 1 \text{ or } x^{2} = 4 \Leftrightarrow x = \pm 1 \text{ or } x = \pm 2"),
]


def _b2_loc(nghiem, tap):
    """Lọc nghiệm (có thể vô tỉ) theo tập số."""
    nghiem = [nsimplify(v) for v in nghiem]
    if tap == r"\mathbb{N}":
        return [v for v in nghiem if v.is_Integer and v >= 0]
    if tap == r"\mathbb{Z}":
        return [v for v in nghiem if v.is_Integer]
    if tap == r"\mathbb{Q}":
        return [v for v in nghiem if v.is_Rational]
    return nghiem


def _b2_pt_tich2():
    """Phương trình tích hai nhân tử (ít nhất một nhân tử bậc hai) trên N, Z, Q, R:
    (đề, đúng, các danh sách sai, lời giải)."""
    for _ in range(200):
        f1, f2 = random.sample(_B2_NHAN_TU2, 2)
        if random.random() < 0.4:                   # một nhân tử bậc nhất
            r = random.choice([Integer(random.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])), Rational(random.choice([-1, 1, 3]), 2)])
            f2 = (_nhan_tu_bac_nhat(r), [r], r"%s = 0 \Leftrightarrow x = %s" % (_nhan_tu_bac_nhat(r).replace(r"\left(", "").replace(r"\right)", ""), _tex_gt(r)))
        tap = random.choice([r"\mathbb{N}", r"\mathbb{Z}", r"\mathbb{Q}", r"\mathbb{R}"])
        tat = sorted(set(nsimplify(v) for v in f1[1] + f2[1]), key=float)
        dung = _b2_loc(tat, tap)
        cac = {t: _b2_loc(tat, t) for t in (r"\mathbb{N}", r"\mathbb{Z}", r"\mathbb{Q}", r"\mathbb{R}")}
        if len(dung) < 1 or len({str(v) for v in cac.values()}) < 3:
            continue
        sai = [cac[t] for t in cac if t != tap] + [_b2_loc(f1[1], tap), _b2_loc(f2[1], tap)]
        de = r"\left\{x \in %s \mid %s%s = 0\right\}" % (tap, f1[0], f2[0])
        trong = lambda t: t.replace(r"\left(", "").replace(r"\right)", "")
        giai = (r"$%s%s = 0 \Leftrightarrow %s = 0$ or $%s = 0$.\\ We have $%s$; $%s$.\\ Keep only the solutions that are %s: $%s$."
                % (f1[0], f2[0], trong(f1[0]), trong(f2[0]), f1[2], f2[2], _TAP_SO[tap], "; ".join(_tex_gt(v) for v in dung)))
        return de, dung, [s for s in sai if {str(v) for v in s} != {str(v) for v in dung}], giai
    raise ValueError("khong sinh duoc")


def _b2_mc_liet_ke(de, dung, sai, giai, dang):
    dap = "$%s$" % _tap(dung) if dung else r"$\varnothing$"
    ung = []
    for s in sai:
        t_ = "$%s$" % (_tap(s) if s else r"\varnothing")
        if t_ != dap and t_ not in ung:
            ung.append(t_)
    if len(ung) < 3:
        return None
    return MC_SA_answer_text(r"Write the set $A = %s$ by listing its elements." % de, dap, ung[:3],
                             giai + r"\\ Therefore $A = %s$." % (_tap(dung) if dung else r"\varnothing"), 0, 0, dang)


def L10_C1_B2_NB017_MC_G_04(socau, dang=1):
    r"""Cách hỏi thứ tư của NB017_MC_G: liệt kê tập hợp cho dạng $\{f(k) \mid k \in \mathbb{Z},\ \ldots\}$
    ($k^{2} + c$, $pk + q$, $k^{2} - ak$...): phải thay từng $k$, các giá trị trùng chỉ viết một lần.

    CLAUDE THEM 01/10/2026 - theo MC 1, MC 26 tai lieu CĐ day them Bai 2 (MC 1 tai lieu chon sai: dem so gia tri
    cua k thay cho so phan tu). Co Lan duyet lai.
    """
    cau = ""
    while cau.count(r"\begin{ex}") < socau:
        r = _b2_mc_liet_ke(*_b2_tap_anh(), dang)
        if r:
            cau += r
    return cau


def L10_C1_B2_NB017_MC_G_05(socau, dang=1):
    r"""Cách hỏi thứ năm của NB017_MC_G: liệt kê tập nghiệm của phương trình tích có nhân tử BẬC HAI
    ($x^{2} - 4$, $x^{2} - 2$, $2x^{2} - 5x + 2$, $x^{2} + 1$...) trên $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$.

    CLAUDE THEM 01/10/2026 - theo MC 19, 27, 29, 30, 33, 34, 41, 42 tai lieu CĐ day them Bai 2 (MC 42 tai lieu
    chon sai vi quen dieu kien x thuoc N). Co Lan duyet lai.
    """
    cau = ""
    while cau.count(r"\begin{ex}") < socau:
        r = _b2_mc_liet_ke(*_b2_pt_tich2(), dang)
        if r:
            cau += r
    return cau


def L10_C1_B2_NB017_SA_A_03(socau, dang=2):
    r"""Trả lời ngắn - cách hỏi thứ ba của SA_A: đếm số phần tử của tập $\{f(k) \mid k \in \mathbb{Z},\ \ldots\}$
    (bẫy: giá trị trùng) hoặc tập nghiệm phương trình tích có nhân tử bậc hai trên $\mathbb{N}$, $\mathbb{Z}$,
    $\mathbb{Q}$, $\mathbb{R}$.

    CLAUDE THEM 01/10/2026 - theo MC 1, MC 28, TF 20, 44 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        de, dung, sai, giai = _b2_tap_anh() if random.random() < 0.5 else _b2_pt_tich2()
        dap = len(dung)
        ung = [len(s) for s in sai]
        debai = r"Given the set $A = %s$. How many elements does the set $A$ have?" % de
        g = giai + r"\\ Therefore $A = %s$ has $%d$ elements." % (_tap(dung) if dung else r"\varnothing", dap)
        cau += MC_SA_answer_const(debai, str(dap), [str(x) for x in _b2_nhieu_so(dap, ung)], g, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB017_MC_H_02: nhận biết tập rỗng - tập hợp mô tả bằng lời (kho xoay vòng)
# ---------------------------------------------------------------------
_B2_RONG_LOI = [  # (mô tả, rỗng?, lí do)
    ("The set of triangles with two obtuse angles", True, "the sum of the three angles of a triangle is $180^\\circ$, so no triangle has two obtuse angles"),
    ("The set of quadrilaterals with four obtuse angles", True, "the sum of the four angles of a quadrilateral is $360^\\circ$, so all four angles cannot be obtuse"),
    ("The set of equilateral triangles with a right angle", True, "each angle of an equilateral triangle equals $60^\\circ$"),
    ("The set of rectangles whose two diagonals are unequal", True, "the two diagonals of a rectangle are always equal"),
    ("The set of perfect squares whose last digit is $2$", True, "the square of a natural number can only end in the digits $0; 1; 4; 5; 6; 9$"),
    ("The set of real numbers $x$ satisfying $x^{2} < 0$", True, "$x^{2} \\ge 0$ for every real number $x$"),
    ("The set of odd natural numbers divisible by $2$", True, "a number divisible by $2$ is even"),
    ("The set of even prime numbers greater than $2$", True, "an even number greater than $2$ has $2$ as a divisor, so it is composite"),
    ("The set of rational numbers $x$ satisfying $x^{2} = 2$", True, "$x = \\pm\\sqrt{2}$ are irrational numbers"),
    ("The set of integers $x$ satisfying $2x = 3$", True, "$x = \\dfrac{3}{2}$ is not an integer"),
    ("The set of natural numbers $n$ satisfying $n + 5 < 3$", True, "$n < -2$ but a natural number is non-negative"),
    ("The set of prime numbers divisible by $3$", False, "$3$ is a prime number divisible by $3$"),
    ("The set of even prime numbers", False, "$2$ is an even prime number"),
    ("The set of triangles whose three side lengths are three consecutive natural numbers", False, "it contains, for example, the triangle with sides $2; 3; 4$"),
    ("The set of right triangles with an angle of $45^\\circ$", False, "these are the isosceles right triangles"),
    ("The set of rhombuses with four right angles", False, "a square is a rhombus with four right angles"),
    ("The set of perfect squares less than $1$", False, "$0 = 0^{2}$ is a perfect square less than $1$"),
    ("The set of two-digit natural numbers divisible by $50$", False, "$50$ is a two-digit number divisible by $50$"),
    ("The set of integers $x$ satisfying $x^{2} = 4$", False, "$x = 2$ or $x = -2$"),
    ("The set of real numbers $x$ satisfying $x^{2} = 3$", False, "$x = \\pm\\sqrt{3}$"),
    ("The set of parallelograms whose two diagonals are perpendicular", False, "a rhombus is a parallelogram whose two diagonals are perpendicular"),
    ("The set of natural numbers less than $10$ that are divisible by both $2$ and $5$", False, "$0$ is divisible by both $2$ and $5$"),
]


def L10_C1_B2_NB017_MC_H_02(socau, dang=1):
    r"""Cách hỏi khác của NB017_MC_H_01: nhận biết tập rỗng khi tập hợp được MÔ TẢ BẰNG LỜI (tam giác có hai
    góc tù, số chính phương tận cùng là $2$, số nguyên tố chia hết cho $3$...). Kho mệnh đề lấy xoay vòng:
    tập đã ra thì chỉ ra lại khi đã dùng hết kho.

    CLAUDE THEM 01/10/2026 - theo MC 45 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    kho = _B2_RONG_LOI
    for _ in range(socau):
        hoi_rong = random.random() < 0.55
        for ung, hoi in _c1_bac_chon("b2_rong_loi", len(kho), hoi_rong):
            dung = [i for i in ung if kho[i][1] == hoi]
            sai = [i for i in ung if kho[i][1] != hoi]
            if dung and len(sai) >= 3:
                break
        chon = [dung[0]] + sai[:3]
        _c1_danh_dau("b2_rong_loi", chon)
        debai = r"Which of the following sets %s?" % ("is the empty set" if hoi else r"is \textbf{not} the empty set")
        giai = r"\\ ".join(r"%s is %s because %s." % (kho[i][0], "the empty set" if kho[i][1] else "nonempty", kho[i][2]) for i in chon)
        cau += _MC_khong_cham(debai, kho[chon[0]][0], [kho[i][0] for i in chon[1:]], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# NB017_MC_M: sắp xếp quan hệ bao hàm giữa ba tập hợp (một chuỗi X ⊂ Y ⊂ Z)
# ---------------------------------------------------------------------
def _b2_chuoi_so():
    """Ba tập lồng nhau về số: bội, ước, khoảng. Trả về [(tex tập nhỏ nhất)...(lớn nhất)], lời giải."""
    kieu = random.randint(0, 2)
    if kieu == 0:
        d = random.choice([2, 3, 4, 5])
        k1, k2 = random.choice([2, 3]), random.choice([2, 3, 5])
        so = [d * k1 * k2, d * k1, d]
        tap = [r"\left\{n \in \mathbb{N} \mid n \text{ is divisible by } %d\right\}" % v for v in so]
        ly = (r"A number divisible by $%d$ is divisible by $%d$, and a number divisible by $%d$ is divisible by $%d$."
              % (so[0], so[1], so[1], so[2]))
        if random.random() < 0.4:
            c = random.randint(1, 9)
            tap = [r"\left\{x \in \mathbb{R} \mid x^{2} + %d = 0\right\}" % c] + tap[:2]
            ly = (r"The set $\left\{x \in \mathbb{R} \mid x^{2} + %d = 0\right\}$ is empty, so it is a subset of every set. "
                  % c + r"A number divisible by $%d$ is divisible by $%d$." % (so[0], so[1]))
        return tap, ly
    if kieu == 1:
        a = random.choice([2, 3, 4, 5])
        k1, k2 = random.choice([2, 3]), random.choice([2, 3])
        so = [a, a * k1, a * k1 * k2]
        tap = [r"\left\{n \in \mathbb{N} \mid n \text{ is a divisor of } %d\right\}" % v for v in so]
        return tap, r"A divisor of $%d$ is a divisor of $%d$, and a divisor of $%d$ is a divisor of $%d$." % (so[0], so[1], so[1], so[2])
    p = sorted(random.sample(range(-9, 10), 4))
    tap = [r"\left[%d;\ %d\right]" % (p[1], p[2]), r"\left(%d;\ %d\right)" % (p[0], p[3]), r"\left(-\infty;\ %d\right)" % (p[3] + random.randint(1, 4))]
    return tap, r"On the number line: the closed interval lies within the open interval, which lies within the ray."


_B2_CHUOI_HINH = [  # các chuỗi bao hàm (nhỏ -> lớn) về hình học
    (["squares", "rectangles", "parallelograms"], "a square is a rectangle with two equal adjacent sides, and a rectangle is a parallelogram with one right angle"),
    (["squares", "rhombuses", "parallelograms"], "a square is a rhombus with one right angle, and a rhombus is a parallelogram with two equal adjacent sides"),
    (["rectangles", "parallelograms", "quadrilaterals"], "a rectangle is a parallelogram with one right angle, and a parallelogram is a quadrilateral"),
    (["rhombuses", "parallelograms", "quadrilaterals"], "a rhombus is a parallelogram with two equal adjacent sides, and a parallelogram is a quadrilateral"),
    (["equilateral triangles", "isosceles triangles", "triangles"], "an equilateral triangle is an isosceles triangle (at each vertex)"),
    (["isosceles right triangles", "isosceles triangles", "triangles"], "an isosceles right triangle is an isosceles triangle"),
    (["parallelograms", "trapezoids", "quadrilaterals"], "a parallelogram is a trapezoid whose two legs are parallel"),
]


def _b2_mc_chuoi(tap, ly, dang, ten_tex):
    """tap: ba tập (nhỏ -> lớn), gán tên ngẫu nhiên, phương án là các chuỗi hoán vị."""
    import itertools
    ten = random.sample(["A", "B", "C", "M", "P", "Q", "X", "Y"], 3)
    thu_tu = list(range(3))
    random.shuffle(thu_tu)                         # thứ tự giới thiệu trong đề
    gioi = ", ".join(r"$%s = %s$" % (ten[i], tap[i]) if ten_tex else r"$%s$ is the set of %s" % (ten[i], tap[i]) for i in thu_tu)
    dung = r"$%s \subset %s \subset %s$" % tuple(ten)
    hv = [p for p in itertools.permutations(range(3)) if list(p) != [0, 1, 2]]
    random.shuffle(hv)
    nhieu = [r"$%s \subset %s \subset %s$" % tuple(ten[i] for i in p) for p in hv[:3]]
    debai = r"Suppose %s. Which of the following is true?" % gioi
    giai = ly + r" Hence $%s \subset %s \subset %s$." % tuple(ten)
    return MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)


def L10_C1_B2_NB017_MC_M_01(socau, dang=1):
    r"""Sắp xếp quan hệ bao hàm giữa ba tập hợp số (tập bội, tập ước, đoạn - khoảng - nửa đường thẳng, có thể
    có tập rỗng): chọn chuỗi $X \subset Y \subset Z$ đúng.

    CLAUDE THEM 01/10/2026 - theo cau 13 (phan dang) tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        tap, ly = _b2_chuoi_so()
        cau += _b2_mc_chuoi(tap, ly, dang, True)
    return cau


def L10_C1_B2_NB017_MC_M_02(socau, dang=1):
    r"""Cách hỏi khác của MC_M_01: ba tập hợp hình học (hình vuông, hình chữ nhật, hình thoi, hình bình hành,
    tứ giác; tam giác đều, cân...) - chọn chuỗi bao hàm đúng. Kho xoay vòng.

    CLAUDE THEM 01/10/2026 - theo MC 40 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        i = _c1_uu_tien("b2_chuoi_hinh", len(_B2_CHUOI_HINH))[0]
        _c1_danh_dau("b2_chuoi_hinh", [i])
        tap, ly = _B2_CHUOI_HINH[i]
        cau += _b2_mc_chuoi(tap, _c1_hoa(ly) + ".", dang, False)
    return cau


# ---------------------------------------------------------------------
# TH018_MC_C / SA_A: phép toán trên tập bội số, tập ước
# ---------------------------------------------------------------------
def _b2_boi(k):
    return r"\left\{n \in \mathbb{N} \mid n \text{ is divisible by } %d\right\}" % k


def _b2_uoc(k):
    return [d for d in range(1, k + 1) if k % d == 0]


_B2_CAP_BOI = [(4, 6), (6, 9), (4, 10), (6, 10), (6, 8), (9, 12), (10, 15), (8, 12), (6, 15), (4, 14), (12, 18),
               (2, 3), (3, 5), (4, 9), (3, 6), (4, 12), (5, 15), (2, 8), (8, 20), (12, 16), (14, 21), (6, 14),
               (9, 15), (15, 20), (2, 5), (3, 4), (5, 10), (6, 18), (4, 20)]


def L10_C1_B2_TH018_MC_C_01(socau, dang=1):
    r"""Phép toán trên tập bội số: $A = \{n \in \mathbb{N} \mid n \text{ chia hết cho } a\}$,
    $B = \{n \in \mathbb{N} \mid n \text{ chia hết cho } b\}$; xác định $A \cap B$ (tập bội của BCNN), hoặc
    $A \cup B$, $A \cap B$ khi $a$ là ước của $b$.

    CLAUDE THEM 01/10/2026 - theo cau 11, 12 (phan dang), TF 11 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        a, b = random.choice(_B2_CAP_BOI)
        if random.random() < 0.5:
            a, b = b, a
        g, L = math.gcd(a, b), a * b // math.gcd(a, b)
        chia = (b % a == 0) or (a % b == 0)
        hoi = random.choice([r"A \cap B", r"A \cup B"]) if chia else r"A \cap B"
        if hoi == r"A \cap B":
            dap_k = L
            ly = (r"$n \in A \cap B \Leftrightarrow n$ is divisible by both $%d$ and $%d$ $\Leftrightarrow n$ is divisible by $\mathrm{LCM}(%d, %d) = %d$." % (a, b, a, b, L))
        else:
            dap_k = g
            ly = (r"Since $%d$ is a divisor of $%d$, every number divisible by $%d$ is divisible by $%d$, that is, $%s \subset %s$. Hence $A \cup B = %s$." % (g, L, L, g, "B" if b == L else "A", "A" if b == L else "B", "A" if a == g else "B"))
        ung = [k for k in dict.fromkeys([a * b, g, a, b, a + b, L * 2, abs(a - b)]) if k != dap_k and k > 1]
        debai = r"Given two sets $A = %s$ and $B = %s$. The set $%s$ is" % (_b2_boi(a), _b2_boi(b), hoi)
        cau += MC_SA_answer_text(debai, "$%s$" % _b2_boi(dap_k), ["$%s$" % _b2_boi(k) for k in ung[:3]], ly, 0, 0, dang)
    return cau


def L10_C1_B2_TH018_MC_C_02(socau, dang=1):
    r"""Cách hỏi khác của TH018_MC_C_01: tập ước. $A$, $B$ là tập các ước tự nhiên của $a$, $b$; liệt kê $A \cap B$
    (các ước của ƯCLN) hoặc $A \setminus B$, $B \setminus A$.

    CLAUDE THEM 01/10/2026 - theo cau 1 (phan dang), TF 11 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        a, b = random.sample([12, 18, 20, 24, 30, 36, 15, 16, 28, 40, 42, 45], 2)
        A, B = _b2_uoc(a), _b2_uoc(b)
        hoi = random.choice([r"A \cap B", r"A \setminus B", r"B \setminus A"])
        kq = {r"A \cap B": [v for v in A if v in B], r"A \setminus B": [v for v in A if v not in B],
              r"B \setminus A": [v for v in B if v not in A]}[hoi]
        if not kq or len(kq) == len(A):
            continue
        cac = {r"A \cap B": [v for v in A if v in B], r"A \setminus B": [v for v in A if v not in B],
               r"B \setminus A": [v for v in B if v not in A], r"A \cup B": sorted(set(A) | set(B))}
        dap = "$%s$" % _tap(kq)
        ung = []
        for s_ in list(cac.values()) + [kq[1:], kq[:-1], [v for v in kq if v != 1]]:
            t_ = "$%s$" % _tap(s_) if s_ else r"$\varnothing$"
            if t_ != dap and t_ not in ung:
                ung.append(t_)
        if len(ung) < 3:
            continue
        so += 1
        debai = (r"Let $A$ and $B$ be the sets of positive divisors of $%d$ and of $%d$, respectively. The set $%s$ is"
                 % (a, b, hoi))
        giai = (r"$A = %s$, $B = %s$.\\ Hence $%s = %s$." % (_tap(A), _tap(B), hoi, _tap(kq)))
        if hoi == r"A \cap B":
            giai += r" (These are the divisors of $\text{GCD}(%d, %d) = %d$.)" % (a, b, math.gcd(a, b))
        cau += MC_SA_answer_text(debai, dap, ung[:3], giai, 0, 0, dang)
    return cau


def L10_C1_B2_TH018_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - tập bội số: có bao nhiêu số tự nhiên nhỏ hơn $N$ thuộc $A \cap B$ ($A \setminus B$,
    $A \cup B$) với $A$, $B$ là tập các số tự nhiên chia hết cho $a$, cho $b$ (kể cả số $0$).

    CLAUDE THEM 01/10/2026 - ban tra loi ngan cua TH018_MC_C (cung Dang), theo TF 11 d tai lieu CĐ day them Bai 2.
    Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        a, b = random.choice([c for c in _B2_CAP_BOI if c[1] % c[0] and c[0] % c[1]])
        N = random.choice([50, 60, 80, 100, 120, 150, 200])
        L = a * b // math.gcd(a, b)
        dem = lambda k: (N - 1) // k + 1
        nA, nB, nG = dem(a), dem(b), dem(L)
        hoi = random.choice([r"A \cap B", r"A \setminus B", r"A \cup B"])
        dap = {r"A \cap B": nG, r"A \setminus B": nA - nG, r"A \cup B": nA + nB - nG}[hoi]
        debai = (r"Given the sets $A = %s$ and $B = %s$. How many natural numbers less than $%d$ belong to the set $%s$?"
                 % (_b2_boi(a), _b2_boi(b), N, hoi))
        giai = (r"$A \cap B$ is the set of natural numbers divisible by $\mathrm{LCM}(%d, %d) = %d$.\\ Natural numbers less than $%d$ (including $0$): divisible by $%d$, there are $%d$ numbers; divisible by $%d$, there are $%d$ numbers; divisible by $%d$, there are $%d$ numbers.\\ " % (a, b, L, N, a, nA, b, nB, L, nG))
        giai += {r"A \cap B": r"Therefore there are $%d$ numbers in $A \cap B$." % nG,
                 r"A \setminus B": r"The number of elements in $A \setminus B$ is $%d - %d = %d$." % (nA, nG, nA - nG),
                 r"A \cup B": r"The number of elements in $A \cup B$ is $%d + %d - %d = %d$." % (nA, nB, nG, nA + nB - nG)}[hoi]
        ung = [nA, nB, nA + nB, nG - 1, nA - nG, nG, dap + 1]
        cau += MC_SA_answer_const(debai, str(dap), [str(x) for x in _b2_nhieu_so(dap, ung)], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH018_MC_D: đọc bảng kết quả thực tế -> giao, hợp, hiệu (kho bối cảnh xoay vòng, không trùng trong đề)
# ---------------------------------------------------------------------
_B2_BANG = [  # (tên, lời dẫn, tên cột đầu, kí hiệu đối tượng, tiêu chí 1, tiêu chí 2, kí hiệu đạt, kí hiệu không đạt, cụm "đạt")
    ("phong_van", r"A company interviews $%d$ candidates $a_{1}, a_{2}, \ldots, a_{%d}$; the results are given in the table below (the sign $+$: passed, the sign $-$: did not pass).", "Candidate", "a", "Technical skills", "Foreign language", "$+$", "$-$",
     ("meet the technical requirement", "meet the foreign-language requirement")),
    ("the_luc", r"The results of a fitness test for $%d$ students $h_{1}, h_{2}, \ldots, h_{%d}$ are given in the table below (P: pass, F: fail).", "Student", "h", "100 m run", "Standing long jump", "P", "F",
     ("passed the $100$ m run", "passed the standing long jump")),
    ("cau_lac_bo", r"The table below shows whether or not each of $%d$ students $s_{1}, s_{2}, \ldots, s_{%d}$ signed up to join the clubs (Y: yes, N: no).", "Student", "s", "Soccer Club", "Chess Club", "Y", "N",
     ("signed up for the soccer club", "signed up for the chess club")),
    ("tiem_chung", r"A health clinic records the two-dose vaccination of $%d$ people $p_{1}, p_{2}, \ldots, p_{%d}$ (the sign $+$: vaccinated, the sign $-$: not vaccinated).", "Person", "p", "Dose 1", "Dose 2", "$+$", "$-$",
     ("received dose $1$", "received dose $2$")),
]


def _b2_chon_bang():
    da = getattr(_DE_HIEN_TAI, "da_dung", None)
    if da is None:
        da = set()
    chua = [i for i in range(len(_B2_BANG)) if "bang:" + _B2_BANG[i][0] not in da]
    i = random.choice(chua or list(range(len(_B2_BANG))))
    da.add("bang:" + _B2_BANG[i][0])
    return _B2_BANG[i]


def L10_C1_B2_TH018_MC_D_01(socau, dang=1):
    r"""Đọc bảng kết quả thực tế (phỏng vấn, kiểm tra thể lực, đăng kí câu lạc bộ, tiêm chủng): $A$, $B$ là tập
    đối tượng đạt từng tiêu chí; xác định $A \cap B$, $A \cup B$, $A \setminus B$ hoặc $B \setminus A$.
    Bối cảnh không lặp lại trong một đề.

    CLAUDE THEM 01/10/2026 - theo TL 58 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        ten, mo, cot, ki, t1, t2, dat, khong, cum = _b2_chon_bang()
        n = random.randint(7, 9)
        h1 = [random.random() < 0.65 for _ in range(n)]
        h2 = [random.random() < 0.55 for _ in range(n)]
        A = [i + 1 for i in range(n) if h1[i]]
        B = [i + 1 for i in range(n) if h2[i]]
        if len(A) < 3 or len(B) < 3 or set(A) <= set(B) or set(B) <= set(A) or not set(A) & set(B):
            continue
        tex = lambda S: (r"\left\{%s\right\}" % "; ".join("%s_{%d}" % (ki, i) for i in sorted(S))) if S else r"\varnothing"
        cac = {r"A \cap B": set(A) & set(B), r"A \cup B": set(A) | set(B), r"A \setminus B": set(A) - set(B),
               r"B \setminus A": set(B) - set(A)}
        hoi = random.choice(list(cac))
        if not cac[hoi]:
            continue
        dap = "$%s$" % tex(cac[hoi])
        ung = [u for u in dict.fromkeys("$%s$" % tex(S) for S in list(cac.values()) + [set(A), set(B)]) if u != dap]
        if len(ung) < 3:
            continue
        so += 1
        bang = (r"\begin{center}\begin{tabular}{|c|%s|}\hline %s & %s \\ \hline %s & %s \\ \hline %s & %s \\ \hline"
                r"\end{tabular}\end{center}"
                % ("c" * n, cot, " & ".join("$%s_{%d}$" % (ki, i + 1) for i in range(n)),
                   t1, " & ".join(dat if v else khong for v in h1), t2, " & ".join(dat if v else khong for v in h2)))
        doi = {"a": "candidates", "h": "students", "s": "students", "p": "people"}[ki]
        debai = (mo % (n, n) + bang + r"Let $A$ be the set of %s that %s, and $B$ be the set of %s that %s. The set $%s$ is"
                 % (doi, cum[0], doi, cum[1], hoi))
        giai = (r"From the table: $A = %s$, $B = %s$.\\ Hence $%s = %s$." % (tex(A), tex(B), hoi, tex(cac[hoi])))
        cau += MC_SA_answer_text(debai, dap, random.sample(ung, 3), giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# TH021_SA_A: đếm số nguyên (số tự nhiên) thuộc kết quả phép toán trên khoảng, đoạn, nửa khoảng
# ---------------------------------------------------------------------
def _b2_so_nguyen(S, chi_tu_nhien=False):
    """Danh sách số nguyên thuộc tập S (hợp các khoảng bị chặn)."""
    ra = []
    for lo, lc, hi, hc in S:
        if lo == -_VC or hi == _VC:
            return None
        for v in range(math.floor(lo), math.ceil(hi) + 1):
            if _k_thuoc([(lo, lc, hi, hc)], v) and (not chi_tu_nhien or v >= 0):
                ra.append(v)
    return sorted(set(ra))


def _b2_hai_khoang():
    """Hai khoảng / đoạn / nửa khoảng (có thể một tia) chồng nhau, đầu mút nguyên."""
    p = sorted(random.sample(range(-9, 10), 4))
    kieu = random.randint(0, 2)
    ng = lambda: random.random() < .5
    if kieu == 0:
        A, B = (p[0], ng(), p[2], ng()), (p[1], ng(), p[3], ng())
    elif kieu == 1:
        A, B = (p[0], ng(), p[3], ng()), (p[1], ng(), p[2], ng())
    else:
        A = (p[0], ng(), p[2], ng())
        B = random.choice([(-_VC, False, p[1], ng()), (p[1], ng(), _VC, False)])
    if random.random() < .5:
        A, B = B, A
    return A, B


def L10_C1_B2_TH021_SA_A_01(socau, dang=2):
    r"""Trả lời ngắn - cho hai khoảng / đoạn / nửa khoảng (có thể cho bằng $\{x \in \mathbb{R} \mid \ldots\}$);
    tập $A \cap B$ ($A \cup B$, $A \setminus B$, $B \setminus A$) có bao nhiêu số nguyên (số tự nhiên)?

    CLAUDE THEM 01/10/2026 - theo TF 16 d, 18 d tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        A, B = _b2_hai_khoang()
        phep = random.choice(["giao", "hop", "hieu", "hieu_nguoc"])
        SA, SB = [A], [B]
        kq, ten = {"giao": (_k_phep(SA, SB, "giao"), r"A \cap B"), "hop": (_k_phep(SA, SB, "hop"), r"A \cup B"),
                   "hieu": (_k_phep(SA, SB, "hieu"), r"A \setminus B"),
                   "hieu_nguoc": (_k_phep(SB, SA, "hieu"), r"B \setminus A")}[phep]
        tn = random.random() < 0.3
        ds = _b2_so_nguyen(kq, tn) if kq else None
        if not ds or len(ds) > 25:
            continue
        so += 1
        deA, laiA = _k_tap_de(*A, random.random() < 0.4)
        deB, laiB = _k_tap_de(*B, random.random() < 0.4)
        loai = "natural number" if tn else "integer"
        debai = r"Given the sets $A = %s$ and $B = %s$. In the set $%s$, how many %ss are there?" % (deA, deB, ten, loai)
        vl = [r"$A = %s$" % laiA] if laiA else []
        vl += [r"$B = %s$" % laiB] if laiB else []
        giai = ((r"Rewrite: " + ", ".join(vl) + r".\\ " if vl else "")
                + r"On the number line: $%s = %s$.\\ The %ss in $%s$ are $%s$, for a total of $%d$."
                % (ten, _k_tex(kq), loai, ten, "; ".join(map(str, ds)), len(ds)))
        dap = len(ds)
        ung = [len(_b2_so_nguyen(_k_lat(kq, 0, 0), tn) or []), len(_b2_so_nguyen(_k_lat(kq, -1, 1), tn) or []), dap + 1, dap - 1]
        cau += MC_SA_answer_const(debai, str(dap), [str(x) for x in _b2_nhieu_so(dap, ung)], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# VD021_MC_C: biết phần bù của từng tập, tìm giao / hợp / phần bù của giao, hợp
# ---------------------------------------------------------------------
def L10_C1_B2_VD021_MC_C_01(socau, dang=1):
    r"""Biết $C_{\mathbb{R}}A$, $C_{\mathbb{R}}B$ (khoảng, đoạn, nửa khoảng hoặc hợp hai nửa đường thẳng); tìm
    $A \cap B$, $A \cup B$, $C_{\mathbb{R}}(A \cap B)$ hoặc $C_{\mathbb{R}}(A \cup B)$ - hai bước: tìm lại $A$, $B$
    rồi thực hiện phép toán.

    CLAUDE THEM 01/10/2026 - theo cau 22 (phan dang) tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        A, B = _b2_hai_khoang()
        SA, SB = [A], [B]
        CA, CB = _k_phep(SA, SA, "bu"), _k_phep(SB, SB, "bu")
        cac = {r"A \cap B": _k_phep(SA, SB, "giao"), r"A \cup B": _k_phep(SA, SB, "hop"),
               r"C_{\mathbb{R}}(A \cap B)": _k_phep(_k_phep(SA, SB, "giao"), [], "bu"),
               r"C_{\mathbb{R}}(A \cup B)": _k_phep(_k_phep(SA, SB, "hop"), [], "bu")}
        ten = random.choice(list(cac))
        kq = cac[ten]
        if not kq or kq == [(-_VC, False, _VC, False)]:
            continue
        dap = "$%s$" % _k_tex(kq)
        ung = []
        for t_, S_ in cac.items():
            u = "$%s$" % _k_tex(S_)
            if t_ != ten and u != dap and u not in ung and S_:
                ung.append(u)
        for i in range(len(kq)):
            for d_ in (0, 1):
                u = "$%s$" % _k_tex(_k_lat(kq, i, d_))
                if u != dap and u not in ung:
                    ung.append(u)
        if len(ung) < 3:
            continue
        so += 1
        debai = (r"Given sets $A$ and $B$ such that $C_{\mathbb{R}}A = %s$ and $C_{\mathbb{R}}B = %s$. The set $%s$ is"
                 % (_k_tex(CA), _k_tex(CB), ten))
        giai = (r"$A = C_{\mathbb{R}}\left(C_{\mathbb{R}}A\right) = %s$, $B = C_{\mathbb{R}}\left(C_{\mathbb{R}}B\right) = %s$.\\ On the number line: $A \cap B = %s$, $A \cup B = %s$.\\ Therefore $%s = %s$."
                % (_k_tex(SA), _k_tex(SB), _k_tex(cac[r"A \cap B"]), _k_tex(cac[r"A \cup B"]), ten, _k_tex(kq)))
        cau += MC_SA_answer_text(debai, dap, ung[:3], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# VD021_MC_A_03: điều kiện của tham số, hỏi qua phần bù / hiệu (tương đương với A giao B rỗng, khác rỗng, hợp bằng R)
# ---------------------------------------------------------------------
_B2_DOI_HOI = {
    r"$A \cap B = \varnothing$": [(r"$A \subset C_{\mathbb{R}}B$", r"$A \subset C_{\mathbb{R}}B$ if and only if no element of $A$ belongs to $B$, that is, $A \cap B = \varnothing$."),
                                  (r"$B \setminus A = B$", r"$B \setminus A = B$ if and only if no element of $B$ belongs to $A$, that is, $A \cap B = \varnothing$."),
                                  (r"$A \setminus B = A$", r"$A \setminus B = A$ if and only if no element of $A$ belongs to $B$, that is, $A \cap B = \varnothing$.")],
    r"$A \cap B \ne \varnothing$": [(r"$A \setminus B \ne A$", r"$A \setminus B \ne A$ if and only if some element of $A$ belongs to $B$, that is, $A \cap B \ne \varnothing$."),
                                    (r"$B \setminus A \ne B$", r"$B \setminus A \ne B$ if and only if some element of $B$ belongs to $A$, that is, $A \cap B \ne \varnothing$."),
                                    (r"$A \not\subset C_{\mathbb{R}}B$", r"$A \not\subset C_{\mathbb{R}}B$ if and only if some element of $A$ belongs to $B$, that is, $A \cap B \ne \varnothing$.")],
    r"$A \cup B = \mathbb{R}$": [(r"$C_{\mathbb{R}}A \subset B$", r"$C_{\mathbb{R}}A \subset B$ if and only if every real number not in $A$ is in $B$, that is, $A \cup B = \mathbb{R}$."),
                                 (r"$C_{\mathbb{R}}B \subset A$", r"$C_{\mathbb{R}}B \subset A$ if and only if every real number not in $B$ is in $A$, that is, $A \cup B = \mathbb{R}$.")],
}


def L10_C1_B2_VD021_MC_A_03(socau, dang=1):
    r"""Cách hỏi thứ ba của VD021_MC_A: tìm điều kiện của $m$ khi yêu cầu được viết qua phần bù, hiệu
    ($A \subset C_{\mathbb{R}}B$, $B \setminus A = B$, $A \setminus B \ne A$, $C_{\mathbb{R}}A \subset B$...) - học
    sinh phải đổi về $A \cap B = \varnothing$, $A \cap B \ne \varnothing$ hoặc $A \cup B = \mathbb{R}$.

    CLAUDE THEM 01/10/2026 - theo TF 10 d, TL 7, 21, 34, 35 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        de, dap, nhieu, giai, _k, _t = _vd021_tham_so()
        cu = next((c for c in _B2_DOI_HOI if c in de), None)
        if cu is None:
            continue
        moi, ly = random.choice(_B2_DOI_HOI[cu])
        so += 1
        cau += MC_SA_answer_text(de.replace(cu, moi), dap, nhieu, ly + r"\\ " + giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# VD021_SA_A_03: đếm số nguyên m để A con B khi A có độ dài thay đổi theo m (phải kèm điều kiện A khác rỗng)
# ---------------------------------------------------------------------
def _b2_bdt(trai, dau, phai):
    return r"%s %s %s" % (trai, dau, phai)


def _b2_lin(k, c):
    """k m + c viết gọn."""
    s = "m" if k == 1 else "%dm" % k
    return s + ((r" %s %d" % ("+" if c > 0 else "-", abs(c))) if c else "")


def _b2_sa_m_con():
    """A = [m + p; k m + q) (hoặc ngoặc khác), B = (c; d] cố định. Đếm số nguyên m để A ⊂ B (A khác rỗng)."""
    for _ in range(500):
        k = random.choice([2, 2, 3])
        p, q = random.randint(-4, 3), random.randint(-4, 4)
        c = random.randint(-8, -1)
        d = c + random.randint(6, 12)
        lcA, hcA = random.random() < .5, random.random() < .5
        lcB, hcB = random.random() < .5, random.random() < .5
        if lcA and hcA:
            hcA = False                         # tránh đoạn suy biến: A luôn có một đầu mở
        A = lambda m: [(m + p, lcA, k * m + q, hcA)] if m + p < k * m + q else []
        B = [(c, lcB, d, hcB)]
        dung = [m for m in range(-40, 41) if A(m) and _k_phep(A(m), B, "hieu") == []]
        if not (1 <= len(dung) <= 9):
            continue
        # các điều kiện (theo quy tắc đầu mút)
        d1 = "<" if (lcA and not lcB) else r"\le"          # c ... m + p
        d2 = "<" if (hcA and not hcB) else r"\le"          # k m + q ... d
        dk = [_b2_bdt(_b2_lin(1, p), "<", _b2_lin(k, q)), _b2_bdt("%d" % c, d1, _b2_lin(1, p)),
              _b2_bdt(_b2_lin(k, q), d2, "%d" % d)]
        L0 = _Fr(p - q, k - 1)
        L1 = _Fr(c - p)
        U = _Fr(d - q, k)
        theo = [m for m in range(-40, 41) if m > L0 and (m > L1 if d1 == "<" else m >= L1) and (m < U if d2 == "<" else m <= U)]
        if theo != dung:
            continue
        quen = [m for m in range(-40, 41) if (m > L1 if d1 == "<" else m >= L1) and (m < U if d2 == "<" else m <= U)]
        if len(quen) == len(dung) and random.random() < 0.6:
            continue                            # ưu tiên đề mà điều kiện A khác rỗng có tác dụng (bẫy)
        ngA = (r"\left[" if lcA else r"\left(") + _b2_lin(1, p) + ";\\ " + _b2_lin(k, q) + (r"\right]" if hcA else r"\right)")
        ngB = (r"\left[" if lcB else r"\left(") + "%d;\\ %d" % (c, d) + (r"\right]" if hcB else r"\right)")
        gt = r"m > %s" % _k_so(L0)
        g1 = r"m %s %s" % (">" if d1 == "<" else r"\ge", _k_so(L1))
        g2 = r"m %s %s" % ("<" if d2 == "<" else r"\le", _k_so(U))
        return ngA, ngB, dk, (gt, g1, g2), dung, len(quen)
    raise ValueError("khong sinh duoc")


def L10_C1_B2_VD021_SA_A_03(socau, dang=2):
    r"""Trả lời ngắn - cách hỏi thứ ba của VD021_SA_A: $A = [m + p;\ km + q)$ có độ dài THAY ĐỔI theo $m$,
    $B$ cố định; đếm số nguyên $m$ để $A \subset B$ (hoặc $A \cap B = A$). Bẫy: phải kèm điều kiện $A$ khác rỗng
    ($m + p < km + q$).

    CLAUDE THEM 01/10/2026 - theo TL 10, 11, 12 tai lieu CĐ day them Bai 2 (doi dap an "khoang" thanh "dem so
    nguyen" cho dung dinh dang tra loi ngan). Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        ngA, ngB, dk, (gt, g1, g2), dung, quen = _b2_sa_m_con()
        hoi = random.choice([r"A \subset B", r"A \cap B = A"])
        debai = (r"Given the sets $A = %s$ and $B = %s$, where $m$ is a parameter. How many integers $m$ are there such that $A$ is nonempty and $%s$?" % (ngA, ngB, hoi))
        giai = ((r"$A \cap B = A \Leftrightarrow A \subset B$.\\ " if hoi != r"A \subset B" else "")
                + r"$A$ is nonempty and $A \subset B$ if and only if $\begin{cases} %s \end{cases} \Leftrightarrow \begin{cases} %s \end{cases}$.\\ The integers $m$ that satisfy this are: $%s$. Therefore there are $%d$ of them."
                % (r" \\ ".join(dk), r" \\ ".join((gt, g1, g2)), "; ".join(map(str, dung)), len(dung)))
        dap = len(dung)
        ung = [quen, dap + 1, dap - 1, dap + 2]
        cau += MC_SA_answer_const(debai, str(dap), [str(x) for x in _b2_nhieu_so(dap, ung)], giai, 0, 0, dang)
    return cau


# ---------------------------------------------------------------------
# VD021_SA_C: tìm m để A giao B có đúng một phần tử
# ---------------------------------------------------------------------
def L10_C1_B2_VD021_SA_C_01(socau, dang=2):
    r"""Trả lời ngắn - $A = [\alpha m + \beta;\ \alpha m + \beta + L]$ (đoạn), $B$ là nửa khoảng có đúng một đầu
    mút được lấy; tìm $m$ để $A \cap B$ có đúng một phần tử (đáp số là số thập phân gọn).

    CLAUDE THEM 01/10/2026 - theo TL 1 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        al = random.choice([1, 2, 2, 3, 4])
        be = random.randint(-5, 5)
        L = random.randint(2, 6)
        c = random.randint(-8, 0)
        d = c + random.randint(4, 10)
        phai_dong = random.random() < 0.5                     # B = (c; d] hay [c; d)
        if phai_dong:
            m = _Fr(d - be, al)                                # đầu trái của A trùng d
            moc, ly_moc = d, r"the left endpoint of $A$ coincides with the right endpoint $%d$ (included) of $B$" % d
        else:
            m = _Fr(c - be - L, al)                            # đầu phải của A trùng c
            moc, ly_moc = c, r"the right endpoint of $A$ coincides with the left endpoint $%d$ (included) of $B$" % c
        s = _thap_phan_ngan(m)
        if s is None:
            continue
        A = lambda t: [(al * t + be, True, al * t + be + L, True)]
        B = [(c, not phai_dong, d, phai_dong)]
        G = _k_phep(A(m), B, "giao")
        if G != [(moc, True, moc, True)]:
            continue
        # chỉ một giá trị m cho giao một điểm (kiểm tra lưới)
        luoi = [m + _Fr(i, 8) for i in range(-80, 81) if i]
        if any(len(_k_phep(A(t), B, "giao")) == 1 and _k_phep(A(t), B, "giao")[0][0] == _k_phep(A(t), B, "giao")[0][2] for t in luoi):
            continue
        so += 1
        ngA = r"\left[%s;\ %s\right]" % (_b2_lin(al, be), _b2_lin(al, be + L))
        ngB = r"\left(%d;\ %d\right]" % (c, d) if phai_dong else r"\left[%d;\ %d\right)" % (c, d)
        debai = (r"Given the sets $A = %s$ and $B = %s$, where $m$ is a real parameter. Find $m$ such that the set $A \cap B$ has exactly one element." % (ngA, ngB))
        bt = _b2_lin(al, be) if phai_dong else _b2_lin(al, be + L)
        giai = (r"$A$ is a closed interval of length $%d$, and $B$ has %s, so $A \cap B$ has exactly one element if and only if %s, that is, $%s = %d \Leftrightarrow m = %s$. Then $A \cap B = \left\{%d\right\}$."
                % (L, "an open left endpoint" if phai_dong else "an open right endpoint", ly_moc, bt, moc,
                   _k_so(m), moc))
        ung = [_thap_phan_ngan(v) for v in (m + 1, -m, m - 1, _Fr(d - be - L, al), _Fr(c - be, al), m * 2)]
        ung = [u for u in dict.fromkeys(ung + ["0", "1", "-1", "2", "-2"]) if u and u != s]
        cau += MC_SA_answer_const(debai, s, ung[:3], giai, 0, 0, dang)
    return cau


# =====================================================================
# ĐÚNG/SAI BÀI 2 (TF_H .. TF_N) - mỗi ý >= 3 phát biểu đúng, >= 3 phát biểu sai (quy tắc cô Lan);
# a) NB, b) TH, c) VD, d) VDC. CLAUDE THEM 01/10/2026 - theo phan Dung/Sai tai lieu CĐ day them Bai 2.
# =====================================================================
def _b2_dem(mau, k, ly, sai_k):
    """Như _tf_dem (k >= 1) nhưng không sinh phát biểu ``Có đúng 0...'', ``Có không quá 0...'' (đọc không tự nhiên)."""
    dung = [(mau % ("There are exactly", k), ly), (mau % ("There are at most", k + 1), ly),
            (mau % ("There are at least", k - 1), ly) if k >= 2 else (mau % ("There are at most", k + 2), ly)]
    sai = [(mau % ("There are exactly", w), ly) for w in dict.fromkeys(sai_k) if w != k and w > 0]
    sai.append((mau % ("There are at least", k + 1), ly))
    if k >= 2:
        sai.append((mau % ("There are at most", k - 1), ly))
    return dung, sai


def _b2_bang_tap(ten, dung_S, ly, sai_S):
    """Phát biểu ``ten = S'' đúng và các ``ten = S'''' sai (S là chuỗi LaTeX)."""
    dung = [(r"$%s = %s$" % (ten, dung_S), ly)]
    sai = [(r"$%s = %s$" % (ten, s), ly) for s in dict.fromkeys(sai_S) if s != dung_S]
    return dung, sai


def _b2_tf_tap_con_bo():
    """A ⊂ B (tập số nguyên liền nhau), |A| = 2 hoặc 3, |B \\ A| = 1..3; A là tập nghiệm của phương trình tích
    trên N hoặc Z (có thêm một nghiệm bị loại)."""
    for _ in range(500):
        n = random.choice([2, 3])
        e = random.randint(1, 3)
        tap = random.choice([r"\mathbb{N}", r"\mathbb{Z}"])
        lo = random.randint(0, 4) if tap == r"\mathbb{N}" else random.randint(-4, 1)
        Bds = list(range(lo, lo + n + e))
        A = sorted(random.sample(Bds, n))
        loai = Rational(random.choice([-1, 1, 3, -3]), 2) if (tap == r"\mathbb{Z}" or random.random() < 0.5) \
            else Integer(-random.randint(1, 4))
        nghiem = [Integer(v) for v in A] + [loai]
        if any(-v in nghiem for v in nghiem if v != 0) or len(set(nghiem)) < len(nghiem):
            continue
        random.shuffle(nghiem)
        nghiem.sort(key=lambda v: v != 0)
        pt, giai_pt = _viet_pt_tich(nghiem)
        deA = r"\left\{x \in %s \mid %s\right\}" % (tap, pt)
        deB = (r"\left\{x \in \mathbb{N} \mid x \le %d\right\}" % Bds[-1]) if lo == 0 else \
            (r"\left\{x \in \mathbb{Z} \mid %d \le x \le %d\right\}" % (lo, Bds[-1]))
        return deA, deB, A, Bds, loai, tap, giai_pt
    raise ValueError("khong sinh duoc")


def L10_C1_TF_H_01(socau, socot=1):
    r"""Đúng/Sai - tập hợp cho bởi tính chất đặc trưng, tập con: $A$ là tập nghiệm (trên $\mathbb{N}$ hoặc
    $\mathbb{Z}$) của một phương trình tích, $B$ là tập các số nguyên liền nhau chứa $A$.
    a) (NB) phần tử thuộc / không thuộc, liệt kê $A$; b) (TH) số phần tử, quan hệ $A \subset B$;
    c) (VD) số tập con của $A$; d) (VDC) số tập $X$ thoả $A \subset X \subset B$, $A \cup X = B$.

    CLAUDE THEM 01/10/2026 - theo TF 1, 3, 6, 7, 42, 43 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        deA, deB, A, Bds, loai, tap, giai_pt = _b2_tf_tap_con_bo()
        n, m = len(A), len(Bds)
        debai = r"Given the sets $A = %s$ and $B = %s$. Determine whether each of the following statements is true or false." % (deA, deB)
        ly_A = r"%s. Since $x \in %s$, we reject $x = %s$, hence $A = %s$." % (giai_pt, tap, _tex_gt(loai), _tap(A))
        # a) NB
        ngoai = [v for v in Bds if v not in A]
        dung = [(r"$%d \in A$" % v, ly_A) for v in A] + [(r"$%s \notin A$" % _tex_gt(loai), ly_A),
                                                       (r"$A = %s$" % _tap(A), ly_A)]
        sai = [(r"$%s \in A$" % _tex_gt(loai), ly_A), (r"$%d \notin A$" % A[0], ly_A),
               (r"$A = %s$" % _tap(sorted([loai] + A, key=float)), ly_A)] + [(r"$%d \in A$" % v, ly_A) for v in ngoai[:1]]
        y1 = _phat_bieu(dung, sai)
        # b) TH
        ly_b = ly_A + r" $B = %s$." % _tap(Bds)
        dung = [(r"The set $A$ has exactly $%d$ elements" % n, ly_b), (r"Set $B$ has exactly $%d$ elements" % m, ly_b),
                (r"$A \subset B$", ly_b), (r"$B \not\subset A$", ly_b)]
        sai = [(r"The set $A$ has exactly $%d$ elements" % (n + 1), ly_b), (r"Set $B$ has exactly $%d$ elements" % (m - 1), ly_b),
               (r"$B \subset A$", ly_b), (r"$A = B$", ly_b), (r"$A \not\subset B$", ly_b)]
        y2 = _phat_bieu(dung, sai)
        # c) VD - số tập con của A
        ly_c = r"$A = %s$ has the following subsets: %s." % (_tap(A), _b2_liet_ke_tap_con(A))
        dung = [(r"The set $A$ has exactly $%d$ subsets" % 2 ** n, ly_c),
                (r"Set $A$ has exactly $%d$ nonempty subsets" % (2 ** n - 1), ly_c),
                (r"Set $A$ has exactly $%d$ subsets containing the element $%d$" % (2 ** (n - 1), A[0]), ly_c),
                (r"Set $A$ has exactly $%d$ subsets with exactly one element" % n, ly_c)]
        sai = [(r"The set $A$ has exactly $%d$ subsets" % (2 ** n - 1), ly_c), (r"The set $A$ has exactly $%d$ subsets" % (2 * n), ly_c),
               (r"Set $A$ has exactly $%d$ nonempty subsets" % 2 ** n, ly_c),
               (r"Set $A$ has exactly $%d$ subsets containing the element $%d$" % (2 ** n - 1, A[0]), ly_c)]
        y3 = _phat_bieu(dung, sai)
        # d) VDC - đếm tập X
        e = m - n
        cac_X = [_tap(A + list(c)) for j in range(e + 1) for c in _b2_tohop(ngoai, j)]
        ly_d = (r"$B \setminus A = %s$. $A \subset X \subset B$ if and only if $X = A \cup Y$ with $Y \subset B \setminus A$: the sets $X$ are $%s$ - there are $%d$ such sets. $A \cup X = B$ and $X \subset B$ if and only if $X$ contains $B \setminus A$ and may also contain some elements of $A$: there are $%d$ such sets." % (_tap(ngoai), "$, $".join(cac_X), 2 ** e, 2 ** n))
        d1, s1 = _b2_dem(r"%s $%d$ sets $X$ such that $A \subset X \subset B$", 2 ** e, ly_d, [2 ** e - 1, e, 2 ** m])
        d2, s2 = _b2_dem(r"%s $%d$ sets $X \subset B$ such that $A \cup X = B$", 2 ** n, ly_d, [2 ** n - 1, 2 ** e, e])
        y4 = _phat_bieu(d1 + d2[:1], s1 + s2[:2])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C1_TF_I_01(socau, socot=1):
    r"""Đúng/Sai - phép toán trên tập hợp liệt kê: $E = \{0; 1; \ldots; 9\}$, $A$, $B$ là hai tập con của $E$.
    a) (NB) $A \cap B$, phần tử thuộc giao; b) (TH) $A \cup B$, $A \setminus B$, $B \setminus A$;
    c) (VD) $C_EA$, $C_E(A \cup B)$, $(A \setminus B) \cup (B \setminus A)$; d) (VDC) đếm tập $X$ thoả
    $A \cap B \subset X \subset A$, $X \subset A$ và $X \cap B = \varnothing$.

    CLAUDE THEM 01/10/2026 - theo TF 8, 9, 21, 22, 24, 28, 47, 49 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        E = list(range(0, 10))
        A = set(random.sample(E, random.randint(4, 5)))
        B = set(random.sample(E, random.randint(4, 5)))
        G, H, AB, BA = A & B, A | B, A - B, B - A
        if not (2 <= len(G) <= 3) or not (1 <= len(AB) <= 3) or not BA or len(H) >= 10:
            continue
        so += 1
        T = lambda S: _tap(sorted(S)) if S else r"\varnothing"
        debai = (r"Given the set $E = \left\{x \in \mathbb{N} \mid x < 10\right\}$ and two subsets $A = %s$, $B = %s$ of $E$. Determine whether each of the following statements is true or false." % (T(A), T(B)))
        ly = (r"$A \cap B = %s$, $A \cup B = %s$, $A \setminus B = %s$, $B \setminus A = %s$."
              % (T(G), T(H), T(AB), T(BA)))
        # a) NB
        dung, sai = _b2_bang_tap(r"A \cap B", T(G), ly, [T(H), T(G - {min(G)}), T(G | {min(AB)}), T(AB)])
        dung += [(r"$%d \in A \cap B$" % v, ly) for v in sorted(G)[:2]]
        sai += [(r"$%d \in A \cap B$" % v, ly) for v in sorted(AB)[:1] + sorted(BA)[:1]]
        y1 = _phat_bieu(dung, sai)
        # b) TH
        d1, s1 = _b2_bang_tap(r"A \cup B", T(H), ly, [T(H - {max(H)}), T(G), T(A)])
        d2, s2 = _b2_bang_tap(r"A \setminus B", T(AB), ly, [T(BA), T(A), T(G)])
        d3, s3 = _b2_bang_tap(r"B \setminus A", T(BA), ly, [T(AB), T(B)])
        y2 = _phat_bieu(d1 + d2 + d3, s1 + s2 + s3)
        # c) VD
        CA, CH, DX = set(E) - A, set(E) - H, AB | BA
        ly_c = ly + r" $C_EA = E \setminus A = %s$, $C_E(A \cup B) = %s$, $(A \setminus B) \cup (B \setminus A) = %s$." % (T(CA), T(CH), T(DX))
        d1, s1 = _b2_bang_tap(r"C_EA", T(CA), ly_c, [T(set(E) - B), T(CA | {min(A)})])
        d2, s2 = _b2_bang_tap(r"C_E(A \cup B)", T(CH), ly_c, [T(set(E) - G), T(CH | {max(H)})])
        d3, s3 = _b2_bang_tap(r"(A \setminus B) \cup (B \setminus A)", T(DX), ly_c, [T(H), T(G)])
        y3 = _phat_bieu(d1 + d2 + d3, s1 + s2 + s3)
        # d) VDC
        k = len(AB)
        cac = [_tap(sorted(G | set(c))) for j in range(k + 1) for c in _b2_tohop(sorted(AB), j)]
        ly_d = (r"$A \cap B \subset X \subset A$ if and only if $X = (A \cap B) \cup Y$ with $Y \subset A \setminus B = %s$: the sets $X$ are $%s$, giving $%d$ sets. $X \subset A$ and $X \cap B = \varnothing$ if and only if $X \subset A \setminus B$: there are also $%d$ such sets." % (T(AB), "$, $".join(cac), 2 ** k, 2 ** k))
        dd, ss = _b2_dem(r"%s $%d$ sets $X$ such that $A \cap B \subset X \subset A$", 2 ** k, ly_d, [2 ** k - 1, k, 2 ** len(A)])
        d2, s2 = _b2_dem(r"%s $%d$ sets $X$ such that $X \subset A$ and $X \cap B = \varnothing$", 2 ** k, ly_d,
                         [2 ** len(A), 2 ** k + 1])
        y4 = _phat_bieu(dd + d2[:1], ss + s2[:1])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C1_TF_J_01(socau, socot=1):
    r"""Đúng/Sai - phép toán trên khoảng, đoạn, nửa khoảng: $A = \{x \in \mathbb{R} \mid \ldots\}$, $B$ cho bằng
    kí hiệu khoảng. a) (NB) viết $A$ dạng khoảng, phần tử thuộc $A$; b) (TH) $A \cap B$, $A \cup B$;
    c) (VD) $A \setminus B$, $B \setminus A$, $C_{\mathbb{R}}A$; d) (VDC) số nguyên thuộc các tập vừa tìm.

    CLAUDE THEM 01/10/2026 - theo TF 15, 16, 18, 25, 29, 40, 46, 50, 51 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        p = sorted(random.sample(range(-8, 9), 4))
        if p[3] - p[0] > 12 or p[2] - p[1] < 2:
            continue
        ng = lambda: random.random() < .5
        A = (p[0], ng(), p[2], ng())
        B = (p[1], ng(), p[3], ng())
        if random.random() < .5:
            A, B = B, A
        SA, SB = [A], [B]
        G, H = _k_phep(SA, SB, "giao"), _k_phep(SA, SB, "hop")
        AB, BA, CA = _k_phep(SA, SB, "hieu"), _k_phep(SB, SA, "hieu"), _k_phep(SA, SA, "bu")
        if not AB or not BA or not all(_b2_so_nguyen(S) for S in (G, AB, BA)):
            continue
        so += 1
        deA = _k_bdt(*A)
        debai = r"Given the sets $A = %s$ and $B = %s$. Determine whether each of the following statements is true or false." % (deA, _k_tex(SB))
        K = lambda S: _k_tex(S)
        # a) NB
        ly_a = r"$A = %s$." % K(SA)
        trong = [v for v in range(math.ceil(A[0]), math.floor(A[2]) + 1) if _k_thuoc(SA, v)]
        bien = [v for v in (A[0], A[2]) if not _k_thuoc(SA, v)]
        dung = [(r"$A = %s$" % K(SA), ly_a)] + [(r"$%d \in A$" % v, ly_a) for v in trong[:2]] + \
            [(r"$%d \notin A$" % v, ly_a) for v in bien[:1] + [A[2] + 1]]
        sai = [(r"$A = %s$" % K(_k_lat(SA, 0, 0)), ly_a), (r"$A = %s$" % K(_k_lat(SA, 0, 1)), ly_a),
               (r"$%d \in A$" % (A[0] - 1), ly_a)] + [(r"$%d \in A$" % v, ly_a) for v in bien[:1]]
        y1 = _phat_bieu(dung, sai)
        # b) TH
        ly_b = r"$A = %s$, $B = %s$. On the number line: $A \cap B = %s$, $A \cup B = %s$." % (K(SA), K(SB), K(G), K(H))
        d1, s1 = _b2_bang_tap(r"A \cap B", K(G), ly_b, [K(_k_lat(G, 0, 0)), K(_k_lat(G, 0, 1)), K(H)])
        d2, s2 = _b2_bang_tap(r"A \cup B", K(H), ly_b, [K(_k_lat(H, 0, 0)), K(_k_lat(H, -1, 1)), K(G)])
        vG = _b2_so_nguyen(G)[0]
        vAB = _b2_so_nguyen(AB)[0]
        d1 += [(r"$%d \in A \cap B$" % vG, ly_b), (r"$%d \in A \cup B$" % vAB, ly_b)]
        s1 += [(r"$%d \in A \cap B$" % vAB, ly_b), (r"$%d \in A \cup B$" % (p[3] + 1), ly_b)]
        y2 = _phat_bieu(d1 + d2, s1 + s2)
        # c) VD
        ly_c = (r"On the number line: $A \setminus B = %s$, $B \setminus A = %s$, $C_{\mathbb{R}}A = %s$."
                % (K(AB), K(BA), K(CA)))
        d1, s1 = _b2_bang_tap(r"A \setminus B", K(AB), ly_c, [K(_k_lat(AB, -1, 1)), K(BA)])
        d2, s2 = _b2_bang_tap(r"B \setminus A", K(BA), ly_c, [K(_k_lat(BA, 0, 0)), K(AB)])
        d3, s3 = _b2_bang_tap(r"C_{\mathbb{R}}A", K(CA), ly_c, [K(_k_lat(CA, 0, 1)), K(_k_lat(CA, -1, 0))])
        y3 = _phat_bieu(d1 + d2 + d3, s1 + s2 + s3)
        # d) VDC - số nguyên
        nG, nAB, nBA = (_b2_so_nguyen(S) for S in (G, AB, BA))
        ly_d = (r"$A \cap B = %s$ contains the integers $%s$; $A \setminus B = %s$ contains $%s$; $B \setminus A = %s$ contains $%s$."
                % (K(G), "; ".join(map(str, nG)) or r"\text{(none)}", K(AB), "; ".join(map(str, nAB)) or r"\text{(none)}",
                   K(BA), "; ".join(map(str, nBA)) or r"\text{(none)}"))
        dd, ss = _b2_dem(r"%s $%d$ integers in the set $A \cap B$", len(nG), ly_d, [len(nG) + 1, len(nG) - 1])
        d2, s2 = _b2_dem(r"%s $%d$ integers in the set $A \setminus B$", len(nAB), ly_d, [len(nAB) + 1])
        d3, s3 = _b2_dem(r"%s $%d$ integers in the set $B \setminus A$", len(nBA), ly_d, [len(nBA) + 1])
        y4 = _phat_bieu(dd[:1] + d2[:1] + d3[:1] + dd[1:], ss[:1] + s2[:1] + s3[:1] + ss[1:])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C1_TF_K_01(socau, socot=1):
    r"""Đúng/Sai - khoảng chứa tham số: $A$ cố định, $B = [m;\ m + L]$ (hoặc nửa khoảng).
    a) (NB) với $m = m_0$ viết $B$, phần tử thuộc $B$; b) (TH) với $m = m_0$ tìm $A \cap B$, $A \cup B$;
    c) (VD) điều kiện của $m$ để $B \subset A$, $A \cap B = \varnothing$; d) (VDC) số giá trị nguyên của $m$
    thuộc $[-10; 10]$ để $A \cap B \ne \varnothing$ ($B \subset A$).

    CLAUDE THEM 01/10/2026 - theo TF 10, 12, 17, 19, 35 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        a = random.randint(-6, 2)
        b = a + random.randint(4, 8)
        L = random.randint(1, b - a - 2)
        ng = lambda: random.random() < .5
        lcA, hcA, lcB, hcB = ng(), ng(), ng(), ng()
        SA = [(a, lcA, b, hcA)]
        Bm = lambda m: [(m, lcB, m + L, hcB)]
        tex_Bm = (r"\left[" if lcB else r"\left(") + r"m;\ m + %d" % L + (r"\right]" if hcB else r"\right)")
        # điều kiện (quy tắc đầu mút), kiểm tra lại bằng bộ máy trên lưới
        d_trai = r"\le" if not (lcB and not lcA) else "<"          # a ... m
        d_phai = r"\le" if not (hcB and not hcA) else "<"          # m + L ... b
        con = lambda m: (a <= m if d_trai == r"\le" else a < m) and (m + L <= b if d_phai == r"\le" else m + L < b)
        g_trai = "<" if (hcB and lcA) else r"\le"                 # m + L ... a (rời bên trái)
        g_phai = "<" if (hcA and lcB) else r"\le"                 # b ... m (rời bên phải)
        roi = lambda m: (m + L < a if g_trai == "<" else m + L <= a) or (b < m if g_phai == "<" else b <= m)
        luoi = [_Fr(i, 4) for i in range(-80, 81)]
        if any(con(t) != (_k_phep(Bm(t), SA, "hieu") == []) or roi(t) != (_k_phep(Bm(t), SA, "giao") == []) for t in luoi):
            continue
        ung_m0 = [v for v in range(a - L, b + 1) if _k_phep(Bm(v), SA, "hieu")
                  and _k_phep(Bm(v), SA, "giao") and _k_phep(Bm(v), SA, "giao")[0][0] < _k_phep(Bm(v), SA, "giao")[0][2]]
        if not ung_m0:
            continue
        m0 = random.choice(ung_m0)
        so += 1
        debai = (r"Given the sets $A = %s$ and $B = %s$, where $m$ is a real parameter. Determine whether each of the following statements is true or false."
                 % (_k_tex(SA), tex_Bm))
        B0 = Bm(m0)
        # a) NB
        ly_a = r"When $m = %d$, $B = %s$." % (m0, _k_tex(B0))
        dung = [(r"When $m = %d$, $B = %s$" % (m0, _k_tex(B0)), ly_a),
                (r"When $m = %d$, $%s \in B$" % (m0, _k_so(m0 + _Fr(L, 2))), ly_a),
                (r"When $m = %d$, $%d \notin B$" % (m0, m0 + L + 1), ly_a)]
        sai = [(r"When $m = %d$, $B = %s$" % (m0, _k_tex(_k_lat(B0, 0, 0))), ly_a),
               (r"When $m = %d$, $B = %s$" % (m0, _k_tex([(m0, lcB, m0 + L + 1, hcB)])), ly_a),
               (r"When $m = %d$, $%d \in B$" % (m0, m0 - 1), ly_a)]
        dung.append((r"When $m = %d$, $%d %s B$" % (m0, m0 + L, r"\in" if hcB else r"\notin"), ly_a))
        sai.append((r"When $m = %d$, $%d %s B$" % (m0, m0 + L, r"\notin" if hcB else r"\in"), ly_a))
        y1 = _phat_bieu(dung, sai)
        # b) TH
        G, H = _k_phep(B0, SA, "giao"), _k_phep(SA, B0, "hop")
        ly_b = ly_a + r" On the number line: $A \cap B = %s$, $A \cup B = %s$." % (_k_tex(G), _k_tex(H))
        pre = r"When $m = %d$, " % m0
        d1 = [(pre + r"$A \cap B = %s$" % _k_tex(G), ly_b), (pre + r"$A \cup B = %s$" % _k_tex(H), ly_b),
              (pre + r"$A \cap B \ne \varnothing$", ly_b)]
        s1 = [(pre + r"$A \cap B = %s$" % _k_tex(_k_lat(G, 0, 0)), ly_b), (pre + r"$A \cap B = %s$" % _k_tex(_k_lat(G, -1, 1)), ly_b),
              (pre + r"$A \cup B = %s$" % _k_tex(_k_lat(H, 0, 0)), ly_b), (pre + r"$A \cap B = \varnothing$", ly_b)]
        y2 = _phat_bieu(d1, s1)
        # c) VD - điều kiện
        tr = lambda d: {r"\le": r"\le", "<": "<"}[d]
        dk_con = r"$B \subset A \Leftrightarrow %d %s m %s %d$" % (a, d_trai, d_phai, b - L)
        dk_roi = (r"$A \cap B = \varnothing \Leftrightarrow m %s %d$ or $m %s %d$"
                  % ("<" if g_trai == "<" else r"\le", a - L, ">" if g_phai == "<" else r"\ge", b))
        ly_c = (r"$B \subset A$ if and only if $\begin{cases} %d %s m \\ m + %d %s %d \end{cases} \Leftrightarrow %d %s m %s %d$.\\ $A \cap B = \varnothing$ if and only if $m + %d %s %d$ or $%d %s m$, that is, $m %s %d$ or $m %s %d$; hence $A \cap B \ne \varnothing \Leftrightarrow %d %s m %s %d$."
                % (a, d_trai, L, d_phai, b, a, d_trai, d_phai, b - L, L, g_trai, a, b, g_phai,
                   "<" if g_trai == "<" else r"\le", a - L, ">" if g_phai == "<" else r"\ge", b,
                   a - L, "<" if g_trai == r"\le" else r"\le", "<" if g_phai == r"\le" else r"\le", b))
        doi = lambda d: "<" if d == r"\le" else r"\le"
        dung = [(dk_con, ly_c), (dk_roi, ly_c),
                (r"$A \cap B \ne \varnothing \Leftrightarrow %d %s m %s %d$" % (a - L, doi(g_trai), doi(g_phai), b), ly_c)]
        sai = [(r"$B \subset A \Leftrightarrow %d %s m %s %d$" % (a, doi(d_trai), d_phai, b - L), ly_c),
               (r"$B \subset A \Leftrightarrow %d %s m %s %d$" % (a, d_trai, d_phai, b), ly_c),
               (r"$B \subset A \Leftrightarrow %d %s m %s %d$" % (a - L, d_trai, d_phai, b), ly_c),
               (r"$A \cap B \ne \varnothing \Leftrightarrow %d %s m %s %d$" % (a, d_trai, d_phai, b - L), ly_c)]
        # kiểm tra phát biểu A giao B khác rỗng: a - L (<|<=) m (<|<=) b
        khac = lambda m: (a - L < m if g_trai == r"\le" else a - L <= m) and (m < b if g_phai == r"\le" else m <= b)
        if any(khac(t) == roi(t) for t in luoi):
            so -= 1
            continue
        y3 = _phat_bieu(dung, sai)
        # d) VDC - đếm m nguyên trong [-10; 10]
        n_khac = sum(1 for v in range(-10, 11) if not roi(v))
        n_con = sum(1 for v in range(-10, 11) if con(v))
        ly_d = ly_c + (r" On $[-10; 10]$: there are $%d$ integers $m$ for which $A \cap B \ne \varnothing$, and there are $%d$ integers $m$ for which $B \subset A$." % (n_khac, n_con))
        dd, ss = _b2_dem(r"%s $%d$ integer values of $m$ in the closed interval $[-10; 10]$ such that $A \cap B \ne \varnothing$", n_khac, ly_d,
                         [n_khac + 1, n_khac - 1, 21 - n_khac])
        d2, s2 = _b2_dem(r"%s $%d$ integer values of $m$ in the closed interval $[-10; 10]$ such that $B \subset A$", n_con, ly_d, [n_con + 1])
        y4 = _phat_bieu(dd + d2[:1], ss + s2[:1])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C1_TF_L_01(socau, socot=1):
    r"""Đúng/Sai - tập bội số $A = \{n \in \mathbb{N} \mid n \text{ chia hết cho } a\}$,
    $B = \{n \in \mathbb{N} \mid n \text{ chia hết cho } b\}$.
    a) (NB) phần tử thuộc / không thuộc; b) (TH) $A \cap B$ là tập bội của BCNN;
    c) (VD) phần tử của $A \setminus B$, $B \setminus A$; d) (VDC) số phần tử nhỏ hơn $N$ của $A \cap B$, $A \cup B$.

    CLAUDE THEM 01/10/2026 - theo TF 11 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        a, b = random.choice([c for c in _B2_CAP_BOI if c[1] % c[0] and c[0] % c[1] and math.gcd(*c) > 1])
        g, L = math.gcd(a, b), a * b // math.gcd(a, b)
        debai = r"Given the sets $A = %s$ and $B = %s$. Determine whether each of the following statements is true or false." % (_b2_boi(a), _b2_boi(b))
        # a) NB
        ly_a = r"$A$ consists of the natural numbers divisible by $%d$, and $B$ consists of the natural numbers divisible by $%d$." % (a, b)
        x1, x2 = a * random.randint(2, 6), b * random.randint(2, 6)
        y_ = a * random.randint(2, 6) + random.randint(1, a - 1)
        dung = [(r"$%d \in A$" % x1, ly_a), (r"$%d \in B$" % x2, ly_a), (r"$0 \in A$", ly_a), (r"$%d \notin A$" % y_, ly_a)]
        sai = [(r"$%d \notin A$" % x1, ly_a), (r"$%d \in A$" % y_, ly_a), (r"$%d \in B$" % a, ly_a), (r"$0 \notin B$", ly_a)]
        y1 = _phat_bieu(dung, sai)
        # b) TH
        ly_b = r"$n \in A \cap B \Leftrightarrow n$ is divisible by both $%d$ and $%d$ $\Leftrightarrow n$ is divisible by $\mathrm{LCM}(%d, %d) = %d$." % (a, b, a, b, L)
        z = a * random.choice([k for k in range(1, 8) if (a * k) % b])          # bội của a, không là bội của b
        dung = [(r"$A \cap B = %s$" % _b2_boi(L), ly_b), (r"$%d \in A \cap B$" % L, ly_b), (r"$%d \in A \cap B$" % (a * b), ly_b),
                (r"$%d \notin A \cap B$" % z, ly_b)]
        sai = [(r"$A \cap B = %s$" % _b2_boi(g), ly_b), (r"$A \cap B = \varnothing$", ly_b), (r"$%d \in A \cap B$" % (L + g), ly_b),
               (r"$%d \in A \cap B$" % z, ly_b)]
        if a * b != L:
            sai.append((r"$A \cap B = %s$" % _b2_boi(a * b), ly_b))
        y2 = _phat_bieu(dung, sai)
        # c) VD
        ly_c = ly_b + r" $A \setminus B$ consists of the numbers divisible by $%d$ but not by $%d$; $B \setminus A$ is the reverse." % (a, b)
        dung = [(r"$%d \in A \setminus B$" % a, ly_c), (r"$%d \in B \setminus A$" % b, ly_c), (r"$%d \notin A \setminus B$" % L, ly_c),
                (r"$%d \notin B \setminus A$" % (2 * L), ly_c)]
        sai = [(r"$%d \in A \setminus B$" % L, ly_c), (r"$%d \in B \setminus A$" % (3 * L), ly_c), (r"$%d \notin A \setminus B$" % a, ly_c),
               (r"$0 \in A \setminus B$", ly_c)]
        y3 = _phat_bieu(dung, sai)
        # d) VDC
        N = random.choice([50, 60, 80, 100, 120])
        dem = lambda k: (N - 1) // k + 1
        nA, nB, nG = dem(a), dem(b), dem(L)
        ly_d = (r"The natural numbers less than $%d$ (including $0$): divisible by $%d$, there are $%d$ numbers; divisible by $%d$, there are $%d$ numbers; divisible by $%d$, there are $%d$ numbers. Hence $A \cap B$ has $%d$ elements, and $A \cup B$ has $%d + %d - %d = %d$ elements less than $%d$."
                % (N, a, nA, b, nB, L, nG, nG, nA, nB, nG, nA + nB - nG, N))
        dd, ss = _b2_dem(r"%%s $%%d$ elements less than $%d$ in the set $A \cup B$" % N, nA + nB - nG, ly_d,
                         [nA + nB, nA + nB - nG + 1, nA + nB - 2 * nG])
        d2, s2 = _b2_dem(r"%%s $%%d$ elements less than $%d$ in the set $A \cap B$" % N, nG, ly_d, [nG - 1, dem(a * b)])
        y4 = _phat_bieu(dd + d2[:1], ss + s2[:1])
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C1_TF_M_01(socau, socot=1):
    r"""Đúng/Sai - tập nghiệm chứa tham số $A = \{x \in \mathbb{R} \mid (x^{2} - Sx + P)(x - m) = 0\}$ ($= \{r_1; r_2; m\}$).
    a) (NB) phần tử luôn thuộc $A$; b) (TH) số phần tử với $m$ cụ thể; c) (VD) số giá trị $m$ để $A$ có đúng
    hai phần tử; d) (VDC) số giá trị $m$ để tổng các phần tử của $A$ bằng một số cho trước.

    CLAUDE THEM 01/10/2026 - theo TF 2 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        r1, r2 = sorted(random.sample([v for v in range(-5, 8) if v], 2))
        pt = r"\left(%s\right)\left(x - m\right) = 0" % _tex_bac2(1, -(r1 + r2), r1 * r2)
        debai = (r"Given the set $A = \left\{x \in \mathbb{R} \mid %s\right\}$, where $m$ is a real parameter. Determine whether each of the following statements is true or false." % pt)
        ly0 = (r"$%s \Leftrightarrow x = %d$ or $x = %d$ or $x = m$, so $A = \left\{%d; %d; m\right\}$ (repeated elements are counted only once)." % (pt, r1, r2, r1, r2))
        # a) NB
        ngoai = [v for v in (-r1, -r2, r1 + r2, r1 * r2) if v not in (r1, r2)]
        dung = [(r"$%d \in A$ for every value of $m$" % r1, ly0), (r"$%d \in A$ for every value of $m$" % r2, ly0),
                (r"$m \in A$ for every value of $m$", ly0)]
        sai = [(r"$%d \in A$ for every value of $m$" % v, ly0) for v in ngoai[:2]] + \
            [(r"$A$ has exactly three elements for every value of $m$", ly0), (r"$A$ has exactly two elements for every value of $m$", ly0)]
        y1 = _phat_bieu(dung, sai)
        # b) TH
        mk = random.choice([v for v in range(-6, 9) if v not in (r1, r2)])
        ly_b = ly0 + r" For $m = %d$: $A = %s$; for $m = %d$: $A = %s$." % (r1, _tap([r1, r2]), mk, _tap([r1, r2, mk]))
        dung = [(r"When $m = %d$, $A$ has exactly $2$ elements" % r1, ly_b), (r"When $m = %d$, $A$ has exactly $3$ elements" % mk, ly_b),
                (r"When $m = %d$, $A = %s$" % (r2, _tap([r1, r2])), ly_b)]
        sai = [(r"When $m = %d$, $A$ has exactly $3$ elements" % r1, ly_b), (r"When $m = %d$, $A$ has exactly $2$ elements" % mk, ly_b),
               (r"When $m = %d$, $A = %s$" % (mk, _tap([r1, r2])), ly_b)]
        y2 = _phat_bieu(dung, sai)
        # c) VD
        ly_c = ly0 + r" $A$ has exactly two elements if and only if $m = %d$ or $m = %d$; if $m \ne %d$ and $m \ne %d$, then $A$ has three elements." % (r1, r2, r1, r2)
        dung = [(r"There are exactly $2$ values of $m$ for which $A$ has exactly two elements", ly_c),
                (r"$A$ has exactly three elements if and only if $m \ne %d$ and $m \ne %d$" % (r1, r2), ly_c),
                (r"There is no value of $m$ for which $A$ has exactly one element", ly_c)]
        sai = [(r"There is exactly $1$ value of $m$ for which $A$ has exactly two elements", ly_c),
               (r"There are exactly $3$ values of $m$ for which $A$ has exactly two elements", ly_c),
               (r"There is exactly one value of $m$ for which $A$ has exactly one element", ly_c),
               (r"$A$ has exactly three elements if and only if $m \ne %d$" % r1, ly_c)]
        y3 = _phat_bieu(dung, sai)
        # d) VDC - tổng các phần tử bằng T
        while True:
            T = random.choice([r1 + r2, r1 + r2 + random.choice([-3, -2, 2, 3, 5])])
            cac_m = [v for v in (r1, r2) if r1 + r2 == T]
            mt = T - r1 - r2
            if mt not in (r1, r2):
                cac_m.append(mt)
            cac_m = sorted(set(cac_m))
            if cac_m:
                break
        k = len(cac_m)
        ly_d = (ly0 + r" If $m = %d$ or $m = %d$, the sum of the elements is $%d$. If $m \ne %d$ and $m \ne %d$, the sum is $%d + m$. The sum equals $%d$ when $m \in \left\{%s\right\}$." % (r1, r2, r1 + r2, r1, r2, r1 + r2, T, "; ".join(map(str, cac_m))))
        dd, ss = _b2_dem(r"%%s $%%d$ values of $m$ such that the sum of all elements of $A$ equals $%d$" % T, k, ly_d,
                         [k + 1, k + 2, k - 1, 2])
        tong = lambda v: sum({r1, r2, v})
        khac_m = [v for v in range(-8, 10) if tong(v) != T]
        dd.append((r"When $m = %d$, the sum of all elements of $A$ equals $%d$" % (cac_m[0], T), ly_d))
        ss += [(r"When $m = %d$, the sum of all elements of $A$ equals $%d$" % (v, T), ly_d) for v in random.sample(khac_m, 2)]
        y4 = _phat_bieu(dd, ss)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


def L10_C1_TF_N_01(socau, socot=1):
    r"""Đúng/Sai - bài toán thực tế hai tập hợp (kho bối cảnh chung, không lặp trong một đề): biết tổng số, $n(A)$,
    $n(B)$ và số không thuộc tập nào. a) (NB) số thuộc ít nhất một tập; b) (TH) số thuộc cả hai;
    c) (VD) số chỉ thuộc $A$ (chỉ thuộc $B$); d) (VDC) số thuộc đúng một trong hai tập.

    CLAUDE THEM 01/10/2026 - theo TF 23, 52, TL 4, 15, 36, 59, 60 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    chon = _bo_chon_boi_canh()
    cau = ""
    for _ in range(socau):
        d = _de_hai_tap_vung(chon)
        dv, dt, loai = d["dv"], d["dt"], d["loai"]
        debai = (d["mo"] + r" %s$%d$ %s that %s, $%d$ %s that %s, and $%d$ %s that %s any %s from the two %s above. Determine whether each of the following statements is true or false." % (d["co"], d["nA"], dv, d["A"], d["nB"], dv, d["B"], d["khong"], dv, d["phu"], loai, loai))
        goi = r"Let $A$ and $B$ be the sets of %s that %s and that %s, respectively; $n(A) = %d$, $n(B) = %d$." % (d["tap"], d["A"], d["B"], d["nA"], d["nB"])
        # a) NB
        ly_a = goi + r" $n(A \cup B) = %d - %d = %d$." % (d["N"], d["khong"], d["nAuB"])
        dd, ss = _b2_dem(r"%%s $%%d$ %s that %s at least one of the two %s above" % (dv, dt, loai), d["nAuB"], ly_a,
                         [d["nA"] + d["nB"], d["N"], d["nAuB"] + 1])
        y1 = _phat_bieu(dd, ss)
        # b) TH
        ly_b = ly_a + r" $n(A \cap B) = n(A) + n(B) - n(A \cup B) = %d + %d - %d = %d$." % (d["nA"], d["nB"], d["nAuB"], d["nAB"])
        dd, ss = _b2_dem(r"%%s $%%d$ %s that %s both of the two %s above" % (dv, dt, loai), d["nAB"], ly_b,
                         [d["nA"] + d["nB"] - d["N"], d["nAB"] + 1, d["khong"]])
        y2 = _phat_bieu(dd, ss)
        # c) VD
        ly_c = ly_b + r" The number of elements only in $A$ is $%d - %d = %d$, and the number of elements only in $B$ is $%d - %d = %d$." % (
            d["nA"], d["nAB"], d["chi_A"], d["nB"], d["nAB"], d["chi_B"])
        hoiA = r"%s that %s but %s" % (dv, d["A"], d["B_phu"])
        hoiB = r"%s that %s but %s" % (dv, d["B"], d["A_phu"])
        dd, ss = _b2_dem(r"%%s $%%d$ %s" % hoiA, d["chi_A"], ly_c, [d["nA"], d["chi_A"] + 1, d["chi_B"]])
        d2, s2 = _b2_dem(r"%%s $%%d$ %s" % hoiB, d["chi_B"], ly_c, [d["nB"], d["chi_A"]])
        y3 = _phat_bieu(dd + d2[:1], ss + s2[:1])
        # d) VDC
        mot = d["chi_A"] + d["chi_B"]
        ly_d = ly_c + r" The number of elements in exactly one of the two sets is $%d + %d = %d$ (or $n(A \cup B) - n(A \cap B) = %d - %d$)." % (
            d["chi_A"], d["chi_B"], mot, d["nAuB"], d["nAB"])
        dd, ss = _b2_dem(r"%%s $%%d$ %s that %s exactly one of the two %s above" % (dv, dt, loai), mot, ly_d,
                         [d["nAuB"], mot + d["nAB"], d["nA"] + d["nB"] - d["nAB"], mot + 1])
        y4 = _phat_bieu(dd, ss)
        cau += TF_baitoan_du(debai, [y1, y2, y3, y4], 0, 0, socot)
    return cau


# =====================================================================
# TỰ LUẬN HAI Ý - HAI ĐƠN VỊ KIẾN THỨC CỦA BÀI 2 (CLAUDE THEM 01/10/2026 - co Lan duyet lai)
# =====================================================================
def _b2_khoang_ngau_nhien():
    """Hai khoảng / đoạn / nửa khoảng chồng nhau một phần (đầu mút nguyên)."""
    while True:
        p = sorted(random.sample(range(-8, 9), 4))
        if p[3] - p[0] <= 12:
            break
    ng = lambda: random.random() < .5
    A, B = (p[0], ng(), p[2], ng()), (p[1], ng(), p[3], ng())
    if random.random() < .5:
        A, B = B, A
    if random.random() < .3:                     # một tập là nửa đường thẳng
        B = random.choice([(-_VC, False, B[2], B[3]), (B[0], B[1], _VC, False)])
    return A, B


def L10_C1_NB017_TH021_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý: cho $A$, $B$ bằng tính chất đặc trưng (bất đẳng thức, $|x - c| \le r$).
    a) (NB017) Viết $A$, $B$ dưới dạng khoảng, đoạn, nửa khoảng;
    b) (TH021) Tìm $A \cap B$, $A \cup B$ và $C_{\mathbb{R}}A$.

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi theo co Lan; theo TL 37, 41, 52, 57 tai lieu CĐ day them Bai 2.
    Co Lan duyet lai.
    """
    cau = ""
    for _ in range(socau):
        A, B = _b2_khoang_ngau_nhien()
        deA, laiA = _k_tap_de(*A, True)
        deB, laiB = _k_tap_de(*B, True)
        SA, SB = [A], [B]
        G, H, CA = _k_phep(SA, SB, "giao"), _k_phep(SA, SB, "hop"), _k_phep(SA, SA, "bu")
        de = r"Given the sets $A = %s$ and $B = %s$." % (deA, deB)
        ds = [(r"Write the sets $A$ and $B$ as open intervals, closed intervals, or half-open intervals.",
               r"A = %s;\ B = %s" % (_k_tex(SA), _k_tex(SB)),
               r"Solve the inequalities in the conditions defining $A$ and $B$: $A = %s$, $B = %s$." % (_k_tex(SA), _k_tex(SB))),
              (r"Find $A \cap B$, $A \cup B$, and $C_{\mathbb{R}}A$.",
               r"A \cap B = %s;\ A \cup B = %s;\ C_{\mathbb{R}}A = %s" % (_k_tex(G), _k_tex(H), _k_tex(CA)),
               r"Represent $A$ and $B$ on the number line: $A \cap B = %s$, $A \cup B = %s$; $C_{\mathbb{R}}A = \mathbb{R} \setminus A = %s$."
               % (_k_tex(G), _k_tex(H), _k_tex(CA)))]
        cau += TL_answer_text(de, ds, 0, 0, dong)
    return cau


def L10_C1_B2_VD021_TL_B_01(socau, dong=1):
    r"""Tự luận (một đơn vị VD021: a) VD, b) VDC) - $A$ cố định, $B = [m;\ m + L]$ (hoặc nửa khoảng) chứa tham số.
    a) (VD) Tìm $m$ để $B \subset A$;
    b) (VDC) Tìm $m$ để $A \cap B \ne \varnothing$ nhưng $B \not\subset A$ (đáp án là hợp hai khoảng của $m$).

    CLAUDE THEM 01/10/2026 - theo TF 10, 12, 35, TL 2, 29 tai lieu CĐ day them Bai 2. Co Lan duyet lai.
    """
    cau = ""
    so = 0
    while so < socau:
        a = random.randint(-6, 2)
        b = a + random.randint(4, 8)
        L = random.randint(1, b - a - 2)
        ng = lambda: random.random() < .5
        lcA, hcA, lcB, hcB = ng(), ng(), ng(), ng()
        SA = [(a, lcA, b, hcA)]
        Bm = lambda m: [(m, lcB, m + L, hcB)]
        tex_Bm = (r"\left[" if lcB else r"\left(") + r"m;\ m + %d" % L + (r"\right]" if hcB else r"\right)")
        d_trai = "<" if (lcB and not lcA) else r"\le"
        d_phai = "<" if (hcB and not hcA) else r"\le"
        g_trai = "<" if (hcB and lcA) else r"\le"          # rời bên trái: m + L ... a
        g_phai = "<" if (hcA and lcB) else r"\le"          # rời bên phải: b ... m
        con = lambda m: (a <= m if d_trai == r"\le" else a < m) and (m + L <= b if d_phai == r"\le" else m + L < b)
        khac = lambda m: (m + L > a if g_trai == r"\le" else m + L >= a) and (m < b if g_phai == r"\le" else m <= b)
        t1 = "<" if g_trai == r"\le" else r"\le"
        t2 = "<" if g_phai == r"\le" else r"\le"
        S_khac = [(a - L, t1 == r"\le", b, t2 == r"\le")]
        S_con = [(a, d_trai == r"\le", b - L, d_phai == r"\le")]
        kq = _k_phep(S_khac, S_con, "hieu")
        luoi = [_Fr(i, 4) for i in range(-80, 81)]
        if any(con(t) != (_k_phep(Bm(t), SA, "hieu") == []) or khac(t) != (_k_phep(Bm(t), SA, "giao") != [])
               or (khac(t) and not con(t)) != _k_thuoc(kq, t) for t in luoi):
            continue
        if len(kq) != 2:
            continue
        so += 1
        de = r"Given the sets $A = %s$ and $B = %s$, where $m$ is a real parameter." % (_k_tex(SA), tex_Bm)
        y1 = (r"Find all values of $m$ such that $B \subset A$.",
              r"%d %s m %s %d" % (a, d_trai, d_phai, b - L),
              r"$B \subset A$ if and only if $\begin{cases} %d %s m \\ m + %d %s %d \end{cases} \Leftrightarrow %d %s m %s %d$."
              % (a, d_trai, L, d_phai, b, a, d_trai, d_phai, b - L))
        y2 = (r"Find all values of $m$ such that $A \cap B \ne \varnothing$ but $B \not\subset A$.",
              r"m \in %s" % _k_tex(kq),
              r"$A \cap B = \varnothing$ if and only if $m + %d %s %d$ or $%d %s m$, so $A \cap B \ne \varnothing \Leftrightarrow %d %s m %s %d$.\\ Combining with part a), $B \not\subset A$ when $m$ lies outside $%s$. On the number line: $m \in %s \setminus %s = %s$."
              % (L, g_trai, a, b, g_phai, a - L, t1, t2, b, _k_tex(S_con), _k_tex(S_khac), _k_tex(S_con), _k_tex(kq)))
        cau += TL_answer_text(de, [y1, y2], 0, 0, dong)
    return cau


def _b2_ven_tikz(a, c, b):
    return (r"\begin{tikzpicture}[scale=0.8, font=\footnotesize]" "\n"
            r"\draw (-2.7,-1.6) rectangle (2.7,1.75);" "\n"
            r"\draw (-0.65,0) circle (1.25); \draw (0.65,0) circle (1.25);" "\n"
            r"\node at (-1.25,0) {$%d$}; \node at (0,0) {$%d$}; \node at (1.25,0) {$%d$};" "\n"
            r"\node at (-1.55,1.25) {$A$}; \node at (1.55,1.25) {$B$};" "\n"
            r"\end{tikzpicture}" % (a, c, b))


def L10_C1_TH019_VD020_TL_A_01(socau, dong=1):
    r"""Tự luận hai ý - bối cảnh thực tế hai tập hợp (kho chung, không lặp trong đề); số phần tử mỗi phần cho trên
    biểu đồ Ven. a) (TH019) Đọc biểu đồ Ven: tính $n(A)$, $n(B)$, $n(A \cap B)$, $n(A \cup B)$;
    b) (VD020) Biết tổng số, tính số không thuộc tập nào và số thuộc đúng một tập.

    CLAUDE THEM 01/10/2026 - tu luan hai y hai don vi theo co Lan; theo TF 23, 52, TL 59, 60 tai lieu CĐ day them Bai 2.
    Co Lan duyet lai.
    """
    chon = _bo_chon_boi_canh()
    cau = ""
    for _ in range(socau):
        d = _de_hai_tap_vung(chon)
        dv, dt, loai = d["dv"], d["dt"], d["loai"]
        a, b, c, k, N = d["chi_A"], d["chi_B"], d["nAB"], d["khong"], d["N"]
        de = (d["mo"] + r" the number of %s in each region is given in the Venn diagram on the right, where $A$ is the set of %s that %s and $B$ is the set of %s that %s." % (dv, d["tap"], d["A"], d["tap"], d["B"]))
        ds = [(r"Compute $n(A)$, $n(B)$, $n(A \cap B)$, and $n(A \cup B)$.",
               r"n(A) = %d;\ n(B) = %d;\ n(A \cap B) = %d;\ n(A \cup B) = %d" % (a + c, b + c, c, a + b + c),
               r"From the Venn diagram: $n(A) = %d + %d = %d$, $n(B) = %d + %d = %d$, $n(A \cap B) = %d$, $n(A \cup B) = %d + %d + %d = %d$." % (a, c, a + c, b, c, b + c, c, a, c, b, a + b + c)),
              (r"How many %s %s any %s from the two %s above? How many %s %s exactly one of the two %s above?"
               % (dv, d["phu"], loai, loai, dv, dt, loai),
               _c1_tl_dap(r"$%d$ %s; $%d$ %s" % (k, dv, a + b, dv)),
               r"The number of %s that %s any %s is $%d - n(A \cup B) = %d - %d = %d$. The number of %s that %s exactly one of the two %s is $%d + %d = %d$."
               % (dv, d["phu"], loai, N, N, a + b + c, k, dv, dt, loai, a, b, a + b))]
        cau += TL_answer_text(de, ds, _b2_ven_tikz(a, c, b), 0, dong)
    return cau
