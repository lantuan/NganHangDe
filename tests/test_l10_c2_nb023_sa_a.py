"""NB023_SA_A_01: F(x; y) = ax + by (KHONG hang so); M phai la mot nghiem nguyen THUOC mien nghiem (co Lan 12/10/2026)."""
import importlib.util
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C2_nb023_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_nb023_test"] = M
_spec.loader.exec_module(M)

SO = r"-?\d+"


def _he_so(tex):
    """'-3x + 4y' / 'x - y' / '-2x - 2y' -> (a, b)."""
    t = tex.replace(" ", "")
    m = re.fullmatch(r"(-?\d*)x([+-]\d*)y", t)
    assert m, tex                                    # dung dang ax + by, khong co hang so
    f = lambda s: -1 if s == "-" else 1 if s in ("", "+") else int(s)
    return f(m.group(1)), f(m.group(2))


def test_f_dang_ax_by_va_m_thuoc_mien_nghiem():
    thoa = {r"\le": lambda v, c: v <= c, r"\ge": lambda v, c: v >= c, "<": lambda v, c: v < c, ">": lambda v, c: v > c}
    dem = 0
    for seed in range(400):
        M._rd.seed(seed)
        cap = []
        orig = M.MC_SA_answer_text
        M.MC_SA_answer_text = lambda debai, dap, *a, **k: cap.append((debai, dap)) or ""
        try:
            M.L10_C2_B3_NB023_SA_A_01(1)
        finally:
            M.MC_SA_answer_text = orig
        debai, dap = cap[0]
        m = re.search(r"Cho bất phương trình \$(.+?) (\\le|\\ge|<|>) (%s)\$\. Điểm \$M\\left\((%s); (%s)\\right\)\$" % (SO, SO, SO), debai)
        assert m, debai
        a, b = _he_so(m.group(1))
        dau, c, x0, y0 = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
        f = re.search(r"F\\left\(x; y\\right\) = (.+?)\$ tại", debai).group(1)
        assert _he_so(f) == (a, b)                   # F chi co dang ax + by
        assert thoa[dau](a * x0 + b * y0, c), debai  # M thuoc mien nghiem
        assert int(dap) == a * x0 + b * y0
        dem += 1
    assert dem == 400
