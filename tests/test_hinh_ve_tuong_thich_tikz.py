# -*- coding: utf-8 -*-
r"""Hình TikZ phải DỊCH ĐƯỢC trên cả TeX Live cũ (VPS, máy ảo), không chỉ trên máy cô Lan.

Lỗi 10/10/2026: câu biểu đồ Ven chương 1 xuất Word ra dòng "[Hình vẽ: xem bản PDF]" vì hàm
`_ven_tikz` viết `\clip[even odd rule] ...`; TikZ cũ (pgf 3.1.9) báo "Extra options not allowed
for clipping path command", còn PDF trên máy cô (TeX mới) thì vẫn ra hình.

Ba lớp chặn:
1. mã nguồn bộ đề không được viết `\clip[...]` (dùng `\path[clip, ...]` hoặc đặt tuỳ chọn ở scope);
2. `hinh_ve_service.tuong_thich_tikz` tự đổi `\clip[...]` -> `\path[clip,...]` khi dịch ảnh, phòng hàm mới viết lại kiểu cũ;
3. dịch THẬT các hình Ven chương 1 bằng phần đầu RÚT GỌN (mô phỏng máy TeX cũ) — bỏ qua nếu máy không có xelatex.
"""
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from app.services import hinh_ve_service as H  # noqa: E402


def test_tuong_thich_doi_clip_co_tuy_chon():
    s = r"\clip[even odd rule] (-8,-8) rectangle (9,9) (1,2) circle (3); \clip \vongA; \clip [x] (0,0);"
    kq = H.tuong_thich_tikz(s)
    assert r"\clip[" not in kq and r"\clip [" not in kq
    assert r"\path[clip,even odd rule] (-8,-8)" in kq
    assert r"\clip \vongA;" in kq  # \clip khong tuy chon giu nguyen


def test_ma_hinh_khong_doi_khi_chuan_hoa():
    s = r"\begin{tikzpicture}\clip[even odd rule] (0,0) rectangle (1,1);\end{tikzpicture}"
    # ma bam tinh tren TikZ goc nen anh da cache khong bi dich lai chi vi ham chuan hoa
    assert H.ma_hinh(s) == H.ma_hinh(s)
    assert H.tuong_thich_tikz(s) != s


def test_ma_nguon_bo_de_khong_viet_clip_co_tuy_chon():
    loi = []
    for f in sorted((GOC / "data" / "python_bank").rglob("*.py")):
        for i, dong in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\\\\?clip\s*\[", dong):
                loi.append("%s:%d" % (f.relative_to(GOC), i))
    assert not loi, "TikZ cu khong cho tuy chon tren \\clip, dung \\path[clip,...]: %s" % loi


def _ven_tikz_chuong1():
    import importlib.util
    spec = importlib.util.spec_from_file_location("L10_C1_tuong_thich", GOC / "data" / "python_bank" / "toan10" / "L10_C1.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["L10_C1_tuong_thich"] = m
    spec.loader.exec_module(m)
    ds = {}
    for ten in sorted(dir(m)):
        if not re.match(r"L10_C1_B2_(NB|TH|VD)019_", ten):
            continue
        for seed in range(6):
            random.seed(seed)
            try:
                out = getattr(m, ten)(2)
            except Exception:
                continue
            for t in H.tim_tikz(out):
                ds.setdefault(t, ten)
    return ds


@pytest.mark.skipif(shutil.which("xelatex") is None, reason="may khong co xelatex")
def test_hinh_ven_chuong1_dich_duoc_bang_phan_dau_rut_gon():
    ds = _ven_tikz_chuong1()
    assert ds, "khong tim thay hinh Ven nao"
    hong = []
    for t, ten in ds.items():
        with tempfile.TemporaryDirectory() as tm:
            tm = Path(tm)
            (tm / "a.tex").write_text(H.PREAMBLE_GON + "\n\\pagestyle{empty}\\begin{document}\n"
                                      + H.tuong_thich_tikz(t) + "\n\\end{document}\n", encoding="utf-8")
            subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "a.tex"],
                           cwd=tm, capture_output=True, text=True, timeout=120)
            if not (tm / "a.pdf").exists():
                hong.append(ten)
    assert not hong, "hinh Ven khong dich duoc: %s" % sorted(set(hong))
