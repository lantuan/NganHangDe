# -*- coding: utf-8 -*-
"""L10_C4_TF_C (16/10/2026, theo cau mau co Lan gui): kiem chung DOC LAP chan tri MOI phat bieu trong kho cua ca bon y.

Doc toa do cac diem tu chinh hinh TikZ cua cau hoi, doc phat bieu bang tests/_tinh_tex.py (vecto, tong, hieu, do dai,
a = canh luc giac do tu hinh), tinh lai dung / sai roi so voi dau \\True. Moi y >= 3 dung, >= 3 sai; y c, d phai co tong /
hieu (Bai 8), y a, b khong co (Bai 7).
"""
import importlib.util
import math
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC / "tests"))
from _tinh_tex import V, bang, tinh  # noqa: E402

_spec = importlib.util.spec_from_file_location("L10_C4_tf_c", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C4_tf_c"] = M
_spec.loader.exec_module(M)

E = 2e-3      # toa do trong TikZ lam tron 3 chu so


def _bat(seed):
    cap = []
    goc = M.TF_baitoan_du
    M.TF_baitoan_du = lambda debai, ds, hinh, h2, socot: cap.append((debai, ds, hinh)) or ""
    try:
        random.seed(seed)
        M.L10_C4_TF_C_01(1)
    finally:
        M.TF_baitoan_du = goc
    assert len(cap) == 1
    return cap[0]


def _gan(x, y):
    if isinstance(x, V) or isinstance(y, V):
        x = x if isinstance(x, V) else V(0, 0)
        y = y if isinstance(y, V) else V(0, 0)
        return abs(x - y) < E
    return abs(x - y) < E * max(1.0, abs(x), abs(y))


def _chan_tri(phat, P, a):
    m = re.fullmatch(r"\$\\overrightarrow\{(\w)(\w)\}\$ và \$\\overrightarrow\{(\w)(\w)\}\$ (.+)", phat)
    if m:
        u = P[m.group(2)] - P[m.group(1)]
        w = P[m.group(4)] - P[m.group(3)]
        cheo = u.x * w.y - u.y * w.x
        cp = abs(cheo) < E * abs(u) * abs(w)
        qh = m.group(5)
        if qh == "cùng phương":
            return cp
        if qh == "cùng hướng":
            return cp and u * w > 0
        if qh == "ngược hướng":
            return cp and u * w < 0
        if qh == "là hai vectơ đối nhau":
            return _gan(u, -1 * w)
        raise AssertionError(qh)
    m = re.fullmatch(r"\$(.+) = (.+)\$", phat)
    trai, phai = m.groups()
    return _gan(tinh(trai, P=P, a=a), tinh(phai, P=P, a=a))


def test_moi_phat_bieu_dung_chan_tri():
    loai = set()
    for s in range(150):
        debai, ds, hinh = _bat(s)
        P = {t: V(float(x), float(y)) for t, x, y in re.findall(r"\\coordinate \((\w)\) at \(([-\d.]+),([-\d.]+)\)", hinh)}
        a = None
        m = re.search(r"lục giác đều \$(\w{6})\$", debai)
        if m:
            loai.add("luc_giac")
            a = abs(P[m.group(1)[1]] - P[m.group(1)[0]])
        else:
            loai.add("hbh" if "bình hành" in debai else "tam_giac")
        assert len(ds) == 4
        for k, y in enumerate(ds):
            dung = [t for t, _ in y if r"\True" in t]
            sai = [t for t, _ in y if r"\True" not in t]
            assert len(set(dung)) >= 3 and len(set(sai)) >= 3, (s, k)
            for t, ly in y:
                phat = t[len(r"{\True "):-1] if r"\True" in t else t[1:-1]
                assert _chan_tri(phat, P, a) == (r"\True" in t), (s, "abcd"[k], phat, ly)
                assert ly.startswith("Đúng. " if r"\True" in t else "Sai. ")
                co_tong = bool(re.search(r"\} [+-] \\overrightarrow", phat))
                assert co_tong == (k >= 2), (k, phat)          # a, b: Bai 7; c, d: tong hieu (Bai 8)
                if k == 3:
                    assert r"\left|" in phat
    assert loai == {"luc_giac", "hbh", "tam_giac"}


def test_da_dang():
    de = set()
    for s in range(60):
        random.seed(s)
        de.add(re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", M.L10_C4_TF_C_01(1), flags=re.S))
    assert len(de) >= 55
