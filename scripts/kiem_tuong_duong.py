#!/usr/bin/env python3
"""So sánh ngân hàng Việt và Anh cùng hạt giống: phần TOÁN ($...$), cấu trúc (\\item, \\True, số dòng) phải y hệt.

Dùng: python3 scripts/kiem_tuong_duong.py L10_C1 [soseed] [tiền_tố_hàm]
"""
import importlib.util, inspect, random, re, sys, traceback
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BANK = GOC / "data" / "python_bank"
BANK_EN = GOC / "data" / "python_bank_en"
sys.path.insert(0, str(BANK))


def nap(duong, ten):
    spec = importlib.util.spec_from_file_location(ten, duong)
    m = importlib.util.module_from_spec(spec)
    sys.modules[ten] = m
    spec.loader.exec_module(m)
    return m


def reset():
    mod = sys.modules.get("_ngan_hang_xoay_vong")
    if mod is not None:
        mod.da_dung = {}


def goi(f):
    ps = list(inspect.signature(f).parameters)
    if len(ps) == 1:
        return f(1)
    if ps[1] == "socot":
        return f(1, 4)
    if ps[1] == "dong":
        return f(1, 1)
    if ps[1] == "dang":
        return f(1)
    return f(1, 1)


def bo_text(s):
    # bỏ nội dung \text{...} (có lồng ngoặc đơn giản)
    out, i = [], 0
    while True:
        j = s.find(r"\text{", i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])
        d, k = 1, j + 6
        while k < len(s) and d:
            d += (s[k] == "{") - (s[k] == "}")
            k += 1
        i = k
        out.append(r"\text{}")
    return "".join(out)


def toan(s):
    s = s.replace("{,}", ".").replace("BCNN", "LCM").replace("UCLN", "GCD")
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)          # dấu thập phân Việt 2,5 = Mỹ 2.5
    return sorted(bo_text(x).replace(" ", "") for x in re.findall(r"\$(.*?)\$", s, flags=re.S))


def cau_truc(s):
    return (s.count(r"\item"), s.count("\\True"), s.count("\\choice"), s.count("\n"))


def vi_tri_true(s):
    return [m.start() for m in re.finditer(r"\\True", s)] and [
        len(re.findall(r"\\item|\\choice|\\loigiai|\\True", s[: m.start()])) for m in re.finditer(r"\\True", s)]


def so_sanh(stem, n=8, tt=None):
    """So sánh bản Anh với bản Việt của một tệp chương. Trả về (số hàm, {tên hàm: [mô tả lệch]})."""
    tt = tt or stem + "_"
    lop = stem.split("_")[0][1:]
    mv = nap(BANK / f"toan{lop}" / f"{stem}.py", "vi_" + stem)
    me = nap(BANK_EN / f"toan{lop}" / f"{stem}.py", "en_" + stem)
    ten = sorted(x for x in dir(mv) if x.startswith(tt) and callable(getattr(mv, x)))
    bad = {}
    for t in ten:
        if not hasattr(me, t):
            bad[t] = ["THIẾU hàm trong bản Anh"]
            continue
        for seed in range(n):
            res = []
            for m in (mv, me):
                reset()
                random.seed(seed * 7919 + 13)
                try:
                    import numpy as _np
                    _np.random.seed(seed)
                except Exception:
                    pass
                try:
                    res.append(("ok", goi(getattr(m, t))))
                except Exception as e:
                    res.append(("err", type(e).__name__ + ": " + str(e)[:80]))
            (kv, rv), (ke, re_) = res
            if kv != ke:
                bad.setdefault(t, []).append(f"seed{seed}: vi={kv}:{rv if kv=='err' else ''} en={ke}:{re_ if ke=='err' else ''}")
            elif kv == "err":
                if rv != re_:
                    bad.setdefault(t, []).append(f"seed{seed}: lỗi khác {rv} | {re_}")
            else:
                if cau_truc(rv) != cau_truc(re_):
                    bad.setdefault(t, []).append(f"seed{seed}: cấu trúc {cau_truc(rv)} != {cau_truc(re_)}")
                elif vi_tri_true(rv) != vi_tri_true(re_):
                    bad.setdefault(t, []).append(f"seed{seed}: vị trí \\True khác {vi_tri_true(rv)} vs {vi_tri_true(re_)}")
                elif toan(rv) != toan(re_):
                    a, b = toan(rv), toan(re_)
                    d = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
                    bad.setdefault(t, []).append(f"seed{seed}: toán khác tại #{d}: {a[d:d+1]} vs {b[d:d+1]}")
    return len(ten), bad


def main():
    stem = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    tt = sys.argv[3] if len(sys.argv) > 3 else stem + "_"
    tong, bad = so_sanh(stem, n, tt)
    print(f"Tổng {tong} hàm, lệch {len(bad)}")
    for t, l in bad.items():
        print(f"- {t} ({len(l)}/{n}): {l[0]}")


if __name__ == "__main__":
    main()
