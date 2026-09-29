# -*- coding: utf-8 -*-
"""Thong diep tren web: AI KHONG ra de.

Co Lan chot 29/09/2026: de sinh bang Python tu ngan hang de; AI chi dan
duong (chon dung de, giai thich loi giai, ho tro cham tu luan theo dap an
co san). De do AI tu nghi rat de vuot khung chuong trinh va ngo nhan sai
kien thuc, nen khong duoc de trang nao noi "AI sinh de / AI tao de".
"""
import pathlib
import re

GOC = pathlib.Path(__file__).resolve().parents[1] / "app" / "templates"

CAM = [
    r"AI\s+để\s+tự\s+động\s+sinh\s+đề",
    r"AI\s+tạo\s+đề",
    r"AI\s+sinh\s+đề",
    r"Sinh đề &amp; chấm bài tự động",
    r"tối ưu hóa bởi trí tuệ nhân tạo",
    r"chấm bài AI",
]


def _doc(ten):
    return (GOC / ten).read_text(encoding="utf-8")


def test_khong_trang_nao_noi_ai_ra_de():
    loi = []
    for p in GOC.rglob("*.html"):
        s = p.read_text(encoding="utf-8")
        for mau in CAM:
            if re.search(mau, s):
                loi.append("%s: %s" % (p.relative_to(GOC), mau))
    assert not loi, "\n".join(loi)


def test_trang_chu_giai_thich_vi_sao():
    s = _doc("index.html")
    assert "Vì sao AI không ra đề?" in s
    assert "Python" in s and "vượt khung chương trình" in s


def test_loi_chao_chat_noi_ro():
    s = _doc("chat/chat.html")
    i = s.index("const LOI_CHAO_MO_DAU = [")
    khoi = s[i:s.index("];", i)]
    # ca 4 loi chao deu phai co dong nay
    assert khoi.count("Mình KHÔNG tự nghĩ ra đề") == 4
