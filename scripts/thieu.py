#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liet ke nhung cho CHUA CO trong ngan hang de, kem MA can bo sung.

    python3 scripts/thieu.py              tom tat ca ba khoi
    python3 scripts/thieu.py 10           chi tiet lop 10
    python3 scripts/thieu.py 11 5         chi tiet lop 11 chuong 5
    python3 scripts/thieu.py 10 --tomtat  chi dem, khong liet ke ma

Hai loai thieu:
    THIEU O MAPPING  yeu cau can dat chua duoc khai dang cau hoi nao
    THIEU O PYTHON   da khai dang trong Mapping nhung chua viet ham sinh
"""
import glob
import json
import os
import re
import sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(GOC)
sys.path.insert(0, GOC)

SO_CHUONG = {10: 8, 11: 9, 12: 6}
HAU_TO = re.compile(r"_(MC|SA|TL)_[A-Z]$")
LOAI_TEN = {"MC": "trắc nghiệm", "SA": "trả lời ngắn", "TL": "tự luận", "TF": "đúng/sai"}


def ham_da_co(lop, chuong):
    """Tap ten ham sinh da viet trong ngan hang Python cua chuong nay."""
    f = os.path.join("data", "python_bank", "toan%d" % lop, "L%d_C%d.py" % (lop, chuong))
    if not os.path.exists(f):
        return set()
    with open(f, encoding="utf-8") as fh:
        src = fh.read()
    return set(re.findall(r"^def (L\d+_[A-Za-z0-9_]+?)_\d{2}\s*\(", src, re.M))


def soat(lop, chuong):
    """Tra ve (thieu_mapping, thieu_python) cua mot chuong."""
    fc = os.path.join("data", "curriculum", "toan%d" % lop, "L%d_C%d.json" % (lop, chuong))
    fm = os.path.join("data", "mapping", "toan%d" % lop, "L%d_C%d.json" % (lop, chuong))
    cur = json.load(open(fc, encoding="utf-8")) if os.path.exists(fc) else []
    mp = json.load(open(fm, encoding="utf-8")) if os.path.exists(fm) else []

    co_dang = {HAU_TO.sub("", m["id"]) for m in mp}
    thieu_mapping = [(r["id"], r["content"]) for r in cur if r["id"] not in co_dang]

    co_ham = ham_da_co(lop, chuong)
    thieu_python = [(m["id"], m.get("Dang", ""), m.get("Loai", ""))
                    for m in mp if m["id"] not in co_ham]
    return thieu_mapping, thieu_python


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tomtat = "--tomtat" in sys.argv
    lops = [int(args[0])] if args else sorted(SO_CHUONG)
    chuongs = [int(args[1])] if len(args) > 1 else None

    tong_m = tong_p = 0
    for lop in lops:
        ds = chuongs or range(1, SO_CHUONG[lop] + 1)
        print("\n" + "=" * 68)
        print("LOP %d" % lop)
        print("=" * 68)
        for c in ds:
            tm, tp = soat(lop, c)
            tong_m += len(tm)
            tong_p += len(tp)
            if not tm and not tp:
                print("\nChuong %d: DU -- khong thieu gi." % c)
                continue
            print("\nChuong %d: thieu %d cho o Mapping, %d cho o Python"
                  % (c, len(tm), len(tp)))
            if tm and not tomtat:
                print("  --- THIEU O MAPPING (chua khai dang cau hoi nao) ---")
                for ma, nd in tm:
                    print("    %-28s %s" % (ma, nd[:52]))
            if tp and not tomtat:
                print("  --- THIEU O PYTHON (da khai dang, chua viet ham) ---")
                for ma, dang, loai in tp:
                    kl = LOAI_TEN.get(ma.rsplit("_", 2)[-2] if "_TF_" not in ma else "TF", "")
                    print("    %-34s %-13s %s" % (ma, kl, dang[:38]))

    print("\n" + "=" * 68)
    print("TONG: thieu %d cho o Mapping, %d cho o Python" % (tong_m, tong_p))
    print("Ham Python viet theo ten dang mapping + duoi _01, vi du:")
    print("    def L10_C2_B3_NB022_MC_A_01(socau, dang=1):")
    print("=" * 68)


if __name__ == "__main__":
    main()
