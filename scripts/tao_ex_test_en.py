#!/usr/bin/env python3
"""Sinh data/config/ex_test_en.sty (nhãn tiếng Anh) từ data/config/ex_test.sty.

KHÔNG sửa ex_test_en.sty bằng tay: sửa ex_test.sty (hoặc bảng THAY dưới đây) rồi chạy lại
    python3 scripts/tao_ex_test_en.py
Chỉ thay các NHÃN hiển thị (Câu, Lời giải, Đáp án, Đúng/Sai ...); mọi phần còn lại giống hệt bản Việt.
Mỗi mục có "so_lan" tối thiểu - nếu ex_test.sty đổi làm mục nào không còn khớp, script báo lỗi để biết mà cập nhật.
"""
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NGUON = GOC / "data" / "config" / "ex_test.sty"
DICH = GOC / "data" / "config" / "ex_test_en.sty"

# (tìm, thay, số lần tối thiểu)
THAY = [
    (r"\renewcommand{\circT}[1]{Đ}", r"\renewcommand{\circT}[1]{T}", 1),
    (r"\centering Đúng\;}", r"\centering True\;}", 1),
    (r"\squareEX{Đ}", r"\squareEX{T}", 1),
    (r"\color{red}Đ}", r"\color{red}T}", 1),
    (r"\color{white}Đ}", r"\color{white}T}", 1),
    (r"\def\selectchoice{Chọn đáp án}", r"\def\selectchoice{Select answer}", 1),
    (r"\def\selectchoiceTF{Chọn đáp án}", r"\def\selectchoiceTF{Select answer}", 1),
    (r"\def\selectshortans{Đáp án:}", r"\def\selectshortans{Answer:}", 1),
    (r"\centering\color{blue}Lời giải.}", r"\centering\color{blue}Solution.}", 1),
    (r"\newcommand{\nameex}{Câu}", r"\newcommand{\nameex}{Question}", 1),
    (r"\newcommand{\namebt}{Bài}", r"\newcommand{\namebt}{Problem}", 1),
    (r"\newcommand{\namevd}{Ví dụ}", r"\newcommand{\namevd}{Example}", 1),
    (r"\ đúng}", r"\ true}", 3),
    (r"\def\phatbieu{Phát biểu}", r"\def\phatbieu{Statement}", 1),
    (r"\def\Dung{Đúng/Sai}", r"\def\Dung{True/False}", 1),
    (r"\def\Dung{Đúng}\def\Sai{Sai}", r"\def\Dung{True}\def\Sai{False}", 1),
    (r"\def\Dung{Đ/S}", r"\def\Dung{T/F}", 1),
    (r"\def\Dung{Đ}\def\Sai{S}", r"\def\Dung{T}\def\Sai{F}", 1),
    (r"phatbieu=Phát biểu", r"phatbieu=Statement", 1),
    (r"\gdef\TrueX{Đ}", r"\gdef\TrueX{T}", 1),
    (r") Đ\newline}", r") T\newline}", 1),
    (r"\bfseries Câu \\", r"\bfseries Question \\", 2),
    (r"\bfseries Chọn \\", r"\bfseries Choice \\", 2),
    (r"\bfseries Câu ##2.", r"\bfseries Question ##2.", 1),
    (r"\newtheorem{exrd}{Câu}", r"\newtheorem{exrd}{Question}", 1),
    (r"\newtheorem{vdex}{Ví dụ}", r"\newtheorem{vdex}{Example}", 1),
]


# ---- khung tài liệu (latex_template.tex -> latex_template_en.tex) ----
MAU_NGUON = GOC / "data" / "config" / "latex_template.tex"
MAU_DICH = GOC / "data" / "config" / "latex_template_en.tex"
THAY_MAU = [
    (r"\usepackage[__EX_TEST_OPTION__]{ex_test}", r"\usepackage[__EX_TEST_OPTION__]{ex_test_en}", 1),
    # Dấu thập phân kiểu Mỹ (0.7): bỏ gói icomma (gói đó là để in 0,7 kiểu Việt)
    (r"\IfFileExists{icomma.sty}{\usepackage{icomma}}{}", "", 1),
    (r"HẾT", "END", 1),
    (r"TRƯỜNG THPT CHUYÊN HÙNG VƯƠNG", "HUNG VUONG HIGH SCHOOL FOR THE GIFTED", 1),
    (r"(\textit{Đề thi có #1\ trang})", r"(\textit{This exam has #1\ pages})", 1),
    (r"NĂM HỌC __NAM_HOC__", "SCHOOL YEAR __NAM_HOC__", 1),
    (r"MÔN TOÁN, LỚP #3", "MATHEMATICS, GRADE #3", 1),
    (r"\rfoot{Trang \thepage/#1#2}", r"\rfoot{Page \thepage/#1#2}", 1),
]


def tao_mau():
    s = MAU_NGUON.read_text(encoding="utf-8")
    loi = []
    for tim, thay, toi_thieu in THAY_MAU:
        n = s.count(tim)
        if n < toi_thieu:
            loi.append("tìm thấy %d (cần >= %d): %s" % (n, toi_thieu, tim))
            continue
        s = s.replace(tim, thay)
    if loi:
        sys.exit("latex_template.tex đã đổi, cập nhật bảng THAY_MAU:\n  " + "\n  ".join(loi))
    MAU_DICH.write_text(s, encoding="utf-8")
    print("ghi", MAU_DICH, len(s), "ký tự")


def main():
    s = NGUON.read_text(encoding="utf-8")
    loi = []
    for tim, thay, toi_thieu in THAY:
        n = s.count(tim)
        if n < toi_thieu:
            loi.append("tìm thấy %d (cần >= %d): %s" % (n, toi_thieu, tim))
            continue
        s = s.replace(tim, thay)
    if loi:
        sys.exit("ex_test.sty đã đổi, cập nhật bảng THAY:\n  " + "\n  ".join(loi))
    # Tên gói: ex_test -> ex_test_en (để \usepackage[...]{ex_test_en} nạp bản này)
    s = s.replace("{ex_test}", "{ex_test_en}")
    DICH.write_text(s, encoding="utf-8")
    print("ghi", DICH, len(s), "ký tự")
    tao_mau()


if __name__ == "__main__":
    main()
