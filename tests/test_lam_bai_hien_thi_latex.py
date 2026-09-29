# -*- coding: utf-8 -*-
r"""Trang lam bai phai doi nhung lenh LaTeX MathJax khong hieu.

Co Lan 29/09/2026 chup man hinh dien thoai:
  - Cau thong ke hien ra dong chu do "Unknown environment 'center'" thay
    cho bang so lieu (25 ham lop 10 chuong 5 dat so lieu trong
    \begin{center}...\end{center}).
  - Ngoac kep kieu LaTeX ``...'' hien nguyen hai dau huyen.
  - \quad o ngoai vung toan hien nguyen chu "\quad".
Chay that ham renderLatexText bang node de kiem.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

TRANG = (Path(__file__).resolve().parents[1] / "app" / "templates" / "chat"
         / "lam_bai.html").read_text(encoding="utf-8")


def _render(chuoi):
    if not shutil.which("node"):
        pytest.skip("may nay khong co node")
    i = TRANG.index("function xuLyDanhSach(")
    j = TRANG.index("async function taiDe(")
    js = TRANG[i:j] + "\nprocess.stdout.write(renderLatexText(%s));" % json.dumps(chuoi)
    return subprocess.run(["node", "-e", js], capture_output=True, text=True,
                          check=True).stdout


def test_center_thanh_div_can_giua():
    ra = _render(r"So lieu:\\ \begin{center}$60$\quad $44$\end{center}")
    assert "begin{center}" not in ra and 'class="can-giua"' in ra
    assert "\\quad" not in ra


def test_tabular_thanh_bang_html():
    ra = _render(r"\begin{tabular}{|c|c|}\hline A & $1,5$ \\ \hline B & $3$ \\ \hline\end{tabular}")
    assert "<table" in ra and ra.count("<tr>") == 2 and "$1{,}5$" in ra


def test_ngoac_kep_latex():
    ra = _render("Mệnh đề ``Nếu $a > 0$ thì $a^2 > 0$''.")
    assert "``" not in ra and "''" not in ra
    assert "“" in ra and "”" in ra
