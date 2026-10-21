# -*- coding: utf-8 -*-
r"""Ảnh chụp thật (bản đồ, sơ đồ, ảnh vệ tinh...) làm NỀN cho hình vẽ TikZ trong câu hỏi - cô Lan duyệt 21/10/2026.

Ảnh đặt trong data/hinh_anh/ (tên snake_case theo docs/17, ví dụ ltr_ban_do.jpg). LaTeX tìm thấy ảnh nhờ TEXINPUTS:
app/services/pdf_service.py (đề PDF), app/services/hinh_ve_service.py (hình cho web và Word), scripts/nhap.py (chạy nháp)
đều thêm thư mục này vào đường tìm kiếm. Vì ảnh nằm TRONG đoạn \begin{tikzpicture}...\end{tikzpicture} nên web, PDF, Word
đều hiện được như mọi hình TikZ khác; tải .tex về thì có kèm ảnh (tệp .zip).

Cách dùng trong hàm sinh câu hỏi:

    from hinh_anh import anh_nen
    hinh = anh_nen("ltr_ban_do.jpg", 13, r"\draw[white, dashed] (570,492) -- (661,749);")

Toạ độ trong phần vẽ chồng là TOẠ ĐỘ ĐIỂM ẢNH của chính tệp ảnh: gốc (0,0) ở góc TRÊN BÊN TRÁI, x sang phải, y đi XUỐNG
(giống toạ độ khi mở ảnh bằng phần mềm xem ảnh), nên đo trên ảnh là dùng được ngay.

Quy ước: ảnh rộng khoảng 1000 điểm ảnh, dưới 300 KB (trang làm bài mở bằng điện thoại); chỉ dùng ảnh có nguồn rõ ràng;
số liệu trên ảnh mà là đáp số thì phải che (vẽ chữ nhật trắng đè lên).
"""
import struct
from pathlib import Path

THU_MUC_ANH = Path(__file__).resolve().parent.parent / "hinh_anh"


def kich_thuoc(ten):
    """(rộng, cao) tính bằng điểm ảnh của tệp PNG hoặc JPEG trong data/hinh_anh/ - đọc thẳng phần đầu tệp, không cần PIL."""
    b = (THU_MUC_ANH / ten).read_bytes()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b):
            if b[i] != 0xFF:
                i += 1
                continue
            loai = b[i + 1]
            if loai in (0xD8, 0x01) or 0xD0 <= loai <= 0xD7:
                i += 2
                continue
            dai = struct.unpack(">H", b[i + 2:i + 4])[0]
            if loai in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                cao, rong = struct.unpack(">HH", b[i + 5:i + 9])
                return rong, cao
            i += 2 + dai
    raise ValueError("Không đọc được kích thước ảnh %s (chỉ nhận PNG, JPEG)" % ten)


def anh_nen(ten, rong_cm, ve="", co_chu=r"\footnotesize"):
    r"""Một hình TikZ hoàn chỉnh: ảnh `ten` rộng `rong_cm` cm làm nền, rồi các lệnh vẽ `ve` dùng toạ độ ĐIỂM ẢNH."""
    rong_px, _cao_px = kich_thuoc(ten)
    k = rong_cm / rong_px
    return ("\\begin{tikzpicture}[x=%.6fcm, y=-%.6fcm, font=%s]\n" % (k, k, co_chu)
            + "\\node[anchor=north west, inner sep=0] at (0,0) {\\includegraphics[width=%scm]{%s}};\n" % (rong_cm, ten)
            + ve.rstrip("\n") + ("\n" if ve else "")
            + "\\end{tikzpicture}")
