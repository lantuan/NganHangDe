# -*- coding: utf-8 -*-
r"""Ảnh chụp thật làm nền cho hình TikZ (cô Lan duyệt 21/10/2026): data/hinh_anh/ + data/python_bank/hinh_anh.py.

Kiểm: đọc kích thước ảnh; hình TikZ có ảnh; mọi nơi dịch LaTeX (PDF đề, hình cho web/Word, chạy nháp) tìm thấy ảnh;
mã băm hình đổi khi đổi ảnh; tải .tex kèm ảnh; mọi \includegraphics trong ngân hàng trỏ tới ảnh có thật, nhẹ;
câu đầu tiên dùng ảnh L10_C3_B6_VD036_TL_I_02 (trước 22/10/2026 là ID riêng TL_P; tính lại Heron độc lập từ số đo trong đề, đường chéo vẽ khớp đề).
"""
import importlib.util
import math
import random
import re
import shutil
import struct
import sys
import zlib
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "data" / "python_bank"))
import hinh_anh  # noqa: E402
from app.services import hinh_ve_service, pdf_service  # noqa: E402

ANH = GOC / "data" / "hinh_anh"


def _png(w, h):
    tho = b"".join(b"\x00" + b"\xff\xff\xff" * w for _ in range(h))
    khoi = lambda loai, d: struct.pack(">I", len(d)) + loai + d + struct.pack(">I", zlib.crc32(loai + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + khoi(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + khoi(b"IDAT", zlib.compress(tho)) + khoi(b"IEND", b""))


def test_kich_thuoc_jpeg_png(tmp_path, monkeypatch):
    assert hinh_anh.kich_thuoc("ltr_ban_do.jpg") == (1000, 1080)
    (tmp_path / "x.png").write_bytes(_png(37, 21))
    monkeypatch.setattr(hinh_anh, "THU_MUC_ANH", tmp_path)
    assert hinh_anh.kich_thuoc("x.png") == (37, 21)


def test_anh_nen_toa_do_diem_anh():
    t = hinh_anh.anh_nen("ltr_ban_do.jpg", 10, r"\draw (0,0) -- (1000,1080);")
    assert t.startswith(r"\begin{tikzpicture}[x=0.010000cm, y=-0.010000cm") and t.endswith(r"\end{tikzpicture}")
    assert r"\includegraphics[width=10cm]{ltr_ban_do.jpg}" in t and r"\draw (0,0) -- (1000,1080);" in t


def test_moi_noi_dich_latex_deu_tim_thay_anh():
    assert str(ANH) in pdf_service._texinputs_env()["TEXINPUTS"]
    assert "HINH_ANH_DIR" in (GOC / "app" / "services" / "hinh_ve_service.py").read_text(encoding="utf-8")
    assert "'data' / 'hinh_anh'" in (GOC / "scripts" / "nhap.py").read_text(encoding="utf-8")


def test_ma_hinh_doi_khi_doi_anh(tmp_path, monkeypatch):
    shutil.copy(ANH / "ltr_ban_do.jpg", tmp_path / "a.jpg")
    monkeypatch.setattr(hinh_ve_service, "HINH_ANH_DIR", tmp_path)
    t = r"\begin{tikzpicture}\node{\includegraphics[width=2cm]{a.jpg}};\end{tikzpicture}"
    assert hinh_ve_service.anh_trong(t) == [tmp_path / "a.jpg"]
    m1 = hinh_ve_service.ma_hinh(t)
    (tmp_path / "a.jpg").write_bytes((tmp_path / "a.jpg").read_bytes() + b"\x00")
    assert hinh_ve_service.ma_hinh(t) != m1
    assert hinh_ve_service.anh_trong(r"\begin{tikzpicture}\draw (0,0)--(1,1);\end{tikzpicture}") == []


@pytest.mark.skipif(not shutil.which("xelatex"), reason="may khong co xelatex")
def test_dich_hinh_co_anh_cho_web_va_word(tmp_path, monkeypatch):
    monkeypatch.setattr(hinh_ve_service, "KHO_ANH", tmp_path)
    t = hinh_anh.anh_nen("ltr_ban_do.jpg", 4, r"\fill[white] (0,0) rectangle (100,100);")
    p = hinh_ve_service.dich_hinh(t)
    assert p.exists() and p.stat().st_size > 20000                 # có ảnh thật bên trong, không phải hình rỗng
    q = hinh_ve_service.dich_hinh(t, chi_png=True)
    assert q.suffix == ".png" and q.stat().st_size > 20000


def test_tai_tex_kem_anh(tmp_path):
    from app.routers import exam
    tex = tmp_path / "de.tex"
    tex.write_text(hinh_anh.anh_nen("ltr_ban_do.jpg", 10) + "\n" + hinh_anh.anh_nen("ltr_ban_do.jpg", 5), encoding="utf-8")
    assert exam._anh_kem_tex(tex) == [(ANH / "ltr_ban_do.jpg", "ltr_ban_do.jpg")]       # mỗi ảnh một lần
    tex.write_text(r"\begin{tikzpicture}\draw (0,0)--(1,1);\end{tikzpicture}", encoding="utf-8")
    assert exam._anh_kem_tex(tex) == []


def test_moi_anh_trong_ngan_hang_co_that_va_nhe():
    dung = set()
    for f in (GOC / "data" / "python_bank").rglob("*.py"):
        for ten in re.findall(r'_ANH = "([^"]+)"|anh_nen\("([^"]+)"', f.read_text(encoding="utf-8")):
            dung.update(t for t in ten if t)
    assert "ltr_ban_do.jpg" in dung
    for ten in dung:
        p = ANH / ten
        assert p.exists(), ten
        assert p.stat().st_size <= 400 * 1024, (ten, p.stat().st_size)
        assert hinh_anh.kich_thuoc(ten)[0] <= 1200, ten
        assert re.fullmatch(r"[a-z0-9_]+\.(jpg|png)", ten), ten                   # snake_case (docs/17)


# ---------------------------------------------------------------- L10_C3_B6_VD036_TL_I_02
_spec = importlib.util.spec_from_file_location("L10_C3_tlp", GOC / "data" / "python_bank" / "toan10" / "L10_C3.py")
C3 = importlib.util.module_from_spec(_spec)
sys.modules["L10_C3_tlp"] = C3
_spec.loader.exec_module(C3)
VI_TRI = {"M": (570, 492), "N": (689, 523), "P": (661, 749), "Q": (593, 786), "R": (480, 755), "S": (463, 570)}


def _heron(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def test_tl_i_02_anh_that_tinh_lai_doc_lap():
    dinh_thay = set()
    for s in range(200):
        random.seed(s)
        o = C3.L10_C3_B6_VD036_TL_I_02(1)
        de = o.split(r"\loigiai")[0]
        do = {t: int(v) for t, v in re.findall(r"\$([MNPQRS]{2}) = (\d+)\$ m", de)}
        assert len(do) == 9, de
        canh = ["MN", "NP", "PQ", "QR", "RS", "SM"]
        assert all(c in do for c in canh)
        cheo = [t for t in do if t not in canh]
        dinh = {cheo[0][0]} & {cheo[1][0]} & {cheo[2][0]}
        assert len(dinh) == 1                                      # ba đường chéo cùng một đỉnh
        A = dinh.pop()
        dinh_thay.add(A)
        # hình: ba nét đứt đúng ba đường chéo đó
        net = re.search(r"\\draw\[white, very thick, dashed\] (.+);", de).group(1)
        doan = {tuple(map(int, re.findall(r"-?\d+", d))) for d in net.split(") (")}
        assert doan == {VI_TRI[A] + VI_TRI[c[1]] for c in cheo}, (de, net)
        # tính lại: quạt tam giác từ A theo thứ tự vòng
        vong = "MNPQRS"
        i = vong.index(A)
        thu = [vong[(i + j) % 6] for j in range(6)]
        dl = lambda u, v: do.get(u + v, do.get(v + u))
        S = [_heron(dl(A, thu[j]), dl(thu[j], thu[j + 1]), dl(thu[j + 1], A)) for j in range(1, 5)]
        tong = sum(S)
        dap_b = int(re.findall(r"S \\approx (\d+)\\,\\text\{m\}", o)[-1])
        assert dap_b == round(tong) and abs(tong - 5800) <= 0.025 * 5800, (dap_b, tong)
        ten_a, dap_a = re.search(r"\\SA\[4\]\{\$S_\{([MNPQRS]{3})\} \\approx (\d+)", o).groups()
        u, v = ten_a[1], ten_a[2]
        assert ten_a[0] == A and abs(int(dap_a) - _heron(dl(A, u), dl(u, v), dl(v, A))) <= 0.5
        assert "- Diện tích: ?" in de and r"\includegraphics[width=14cm]{ltr_ban_do.jpg}" in de
        assert "5.800" not in de and "5\\,800" not in de                 # đề không nêu đáp số
    assert dinh_thay == set("MNPQRS")
