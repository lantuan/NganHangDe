# -*- coding: utf-8 -*-
"""BÀI TOÁN BA TẬP HỢP - để dành cho ngân hàng CHUYÊN ĐỀ HỌC TẬP.

Cô Lan 30/09/2026: "trong sách giáo khoa bài toán thực tế chỉ dừng ở hai tập
hợp thôi. câu này ... để lại phần cùng chỗ với chuyên đề học tập để dùng sau".
Chuyển nguyên từ data/python_bank/toan10/L10_C1.py (cùng hằng số bối cảnh):

    L10_C1_B2_VD020_MC_A_03   số người dùng ít nhất một trong ba ứng dụng
    L10_C1_B2_VD020_SA_A_02   ba câu lạc bộ, biết số tham gia đúng hai -> cả ba

(TH019_TL_A_01 - biểu đồ Ven ba tập hợp - cô Lan cho GIỮ LẠI trong ngân hàng, đã trả về L10_C1.)
Trong ngân hàng, VD020_MC_A_03 và VD020_SA_A_02 đã viết lại thành HAI tập hợp.

CHƯA nối vào hệ thống (không có Mapping trỏ tới). Khi làm ngân hàng chuyên đề thì
đổi tên hàm theo ID của chuyên đề và thêm dòng Mapping tương ứng.
"""
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python_bank"))
from math_type import *  # noqa: E402,F401,F403


def _ba_nhieu(dung, ung_vien, buoc=None):
    """Bản sao _ba_nhieu của L10_C1 (lấy đúng ba phương án nhiễu khác nhau)."""
    ds = []
    for v in ung_vien:
        if v != dung and v not in ds:
            ds.append(v)
        if len(ds) == 3:
            return ds
    k = 1
    while len(ds) < 3:
        v = buoc(k) if buoc else str(k)
        if v != dung and v not in ds:
            ds.append(v)
        k += 1
    return ds


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
