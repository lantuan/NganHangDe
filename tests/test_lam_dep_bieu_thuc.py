# -*- coding: utf-8 -*-
r"""Bo loc chung lam_dep (app/services/lam_dep_bieu_thuc.py).

Muc dich: de tu sinh khong con "1x", "+ -3", "- -3", "\cdot -2", "+ 0x"
va khong con co so am thieu ngoac trong luy thua ("-3^{8}" la SAI:
no bang -(3^8)). Bo loc chi sua TRONG $...$, khong dung vao tikz.
"""
import importlib
import pathlib
import random
import re
import sys

import pytest

GOC = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))

from app.services.lam_dep_bieu_thuc import lam_dep  # noqa: E402


@pytest.mark.parametrize("vao, ra", [
    ("$1x + 2 = 0$", "$x + 2 = 0$"),
    ("$y = -1x^{2} + 3$", "$y = -x^{2} + 3$"),
    ("$2x + -3$", "$2x - 3$"),
    ("$5 - -3 = 8$", "$5 + 3 = 8$"),
    ("$2\\cdot -3$", "$2\\cdot \\left(-3\\right)$"),
    ("$x^{2} + 0x + 1$", "$x^{2} + 1$"),
    ("$y = 3x + 1 t$", "$y = 3x + t$"),
])
def test_quy_tac(vao, ra):
    assert lam_dep(vao) == ra


@pytest.mark.parametrize("giu", [
    "$1\\dfrac{1}{2}$",          # hon so
    "$1\\cdot x$",               # co y viet phep nhan voi 1
    "$21x$", "$0{,}1x$", "$x_1x_2$", "$10x$",
    "Chữ 1 a ngoài công thức",   # ngoai $...$ khong dung toi
    "$\\left(-3\\right)^{8}$",
])
def test_khong_dung_vao(giu):
    assert lam_dep(giu) == giu


def test_bo_qua_tikz():
    s = "\\begin{tikzpicture}\\node at (0,0) {$1x$};\\end{tikzpicture}"
    assert lam_dep(s) == s


MAU = {
    "he so 1": re.compile(r"(?<![\d.,{}\w\\^_])(?:[-+]\s*)?1\s*"
                          r"([a-zA-Z](?![a-zA-Z])|\\sqrt|\\left\()"),
    "+ -": re.compile(r"\+\s*-\s*[\d\\]"),
    "- -": re.compile(r"[\w})]\s*-\s*-\s*[\d\\]"),
    "he so 0": re.compile(r"(?<![\d.,])\b0\s*[a-z](?![a-z])"),
    "cdot -": re.compile(r"\\cdot\s*-"),
    # -3^{8} = -(3^8): so am lam co so voi so mu la SO thi phai co ngoac.
    # ("y = -2^{x}" la ham so khac, viet dung y do nen khong bat.)
    "co so am": re.compile(r"(?:^\$|[=(,]|\\cdot)\s*-\s*\d+\s*\^\s*\{?\s*\d"),
}


def test_ca_ngan_hang_sach():
    """Chay moi ham voi vai seed, qua lam_dep: khong con mau xau nao."""
    np = pytest.importorskip("numpy")
    loi = []
    for p in sorted((GOC / "data" / "python_bank").rglob("L1*_C*.py")):
        mod = importlib.import_module("%s.%s" % (p.parent.name, p.stem))
        for ten in [n for n in dir(mod) if re.match(r"L1\d_C\d+_.*_\d\d$", n)]:
            for seed in range(3):
                random.seed(seed)
                np.random.seed(seed)
                try:
                    ham = getattr(mod, ten)
                    out = ham(2) if "_SA_" in ten else ham(2, 1)
                except Exception:
                    continue
                out = lam_dep(out)
                out = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                             "", out, flags=re.S)
                toan_list = [t for dong in out.split("\n")
                             for t in re.findall(r"\$[^$]+\$", dong)]
                for toan in toan_list:
                    for loai, rx in MAU.items():
                        if rx.search(toan):
                            loi.append("%s [%s]: %s" % (ten, loai, toan[:80]))
    assert not loi, "\n".join(sorted(set(loi))[:30])
