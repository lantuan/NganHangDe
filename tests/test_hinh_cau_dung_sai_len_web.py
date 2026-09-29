# -*- coding: utf-8 -*-
r"""Cau Dung/Sai CO HINH phai hien duoc hinh tren web.

math_type.TF_baitoan_du xep cau Dung/Sai co hinh theo kieu
    \immini[thm]{ de bai ... \choiceTFt{a}{b}{c}{d} }{ HINH }
tuc HINH nam SAU \choiceTFt. Truoc 29/09/2026, answer_parser_service chi
tim hinh trong phan de bai - ma phan nay bi cat ngay tai \choiceTFt - nen
MOI cau Dung/Sai co hinh (9 cau trong ca ngan hang luc do) deu mat hinh
tren trang lam bai. Co Lan: "phai co hinh ca tren web. ko the ko co hinh.
se bi sai muc do cua cau."
"""
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from app.services.answer_parser_service import trich_dap_an  # noqa: E402
from toan12 import L12_C6  # noqa: E402


def _cau(out):
    return re.findall(r"\\begin\{ex\}.*?\\end\{ex\}", out, re.S)


def test_cau_dung_sai_co_hinh_lay_duoc_hinh():
    for ham in (L12_C6.L12_C6_TF_A_01, L12_C6.L12_C6_TF_B_01):
        random.seed(5)
        for k in _cau(ham(3, 1)):
            assert "tikzpicture" in k.split("\\loigiai")[0]
            d = trich_dap_an(k)
            assert d["loai_cau"] == "TF"
            assert d.get("hinh_tikz"), "Cau Dung/Sai co hinh ma web khong lay duoc hinh"


def test_khong_lay_nham_hinh_cua_loi_giai():
    """Hinh chi co trong \\loigiai thi KHONG duoc dua len de bai."""
    k = ("\\begin{ex}%%[?]\nDe bai.\n\\choice{\\True $1$}{$2$}{$3$}{$4$}\n"
         "\\loigiai{\nGiai.\n\\begin{tikzpicture}\\draw (0,0)--(1,1);"
         "\\end{tikzpicture}\n}\n\\end{ex}")
    assert not trich_dap_an(k).get("hinh_tikz")
