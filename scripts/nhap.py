#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chay NHAP mot ham trong ngan hang de -> file .tex va .pdf de soi.

Dung (dung o thu muc goc cua du an):

    python3 scripts/nhap.py L10_C1_B2_NB017_SA_C_01
    python3 scripts/nhap.py L10_C1_B2_NB017_SA_C_01 -n 10
    python3 scripts/nhap.py L10_C1_B2_NB017_SA_C_01 --seed 7
    python3 scripts/nhap.py L10_C1_B2_NB017_SA_C          (moi bien the _01, _02...)
    python3 scripts/nhap.py L10_C1_B2_NB017_SA_C_01 --khong-pdf

Ket qua nam trong thu muc nhap/ (khong day len GitHub):
    nhap/<TEN>_dethi.tex    nhap/<TEN>_dethi.pdf     de, khong loi giai
    nhap/<TEN>_loigiai.tex  nhap/<TEN>_loigiai.pdf   de kem dap an, loi giai

Sinh cau DUNG NHU TREN WEB: cung cach goi ham (generator_service), cung bo
loc lam_dep, cung khung data/config/latex_template.tex va ex_test.sty.
Chi doc - khong sua ngan hang de, khong ghi gi vao mapping.
"""
import argparse
import os
import random
import re
import subprocess
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))

from app.services.generator_service import (  # noqa: E402
    _call_generator_function, _find_variant_functions, _load_chapter_module,
    kiem_tra_dung_loai_cau)
from app.services.lam_dep_bieu_thuc import lam_dep  # noqa: E402
from app.services.latex_service import build_latex_document  # noqa: E402

CONFIG = GOC / "data" / "config"
NHAP = GOC / "nhap"


def _dat_seed(seed):
    if seed is None:
        return
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass


def _bien_dich(tex: Path) -> bool:
    """pdflatex 2 lan (giong app/services/pdf_service.py). In loi neu co."""
    env = os.environ.copy()
    env["TEXINPUTS"] = f"{CONFIG}{os.sep}:{env.get('TEXINPUTS', '')}"
    kq = None
    for _ in range(2):
        try:
            kq = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex.name],
                cwd=tex.parent, env=env, capture_output=True,
                encoding="utf-8", errors="replace", timeout=120)
        except FileNotFoundError:
            print("  !! Khong tim thay pdflatex - may chua cai LaTeX. "
                  "File .tex van dung duoc: mo bang TeXstudio/VS Code.")
            return False
    loi = [d for d in kq.stdout.splitlines() if d.startswith("!")]
    pdf = tex.with_suffix(".pdf")
    if loi:
        print("  !! LaTeX bao loi (xem day du trong %s):"
              % tex.with_suffix(".log").name)
        for d in loi[:8]:
            print("     " + d)
    return pdf.exists()


def main():
    ap = argparse.ArgumentParser(description="Chay nhap mot ham ra .tex/.pdf")
    ap.add_argument("ten", help="Ten ham (…_01) hoac ID dang (bo _01 -> chay moi bien the)")
    ap.add_argument("-n", "--socau", type=int, default=5, help="So cau moi ham (mac dinh 5)")
    ap.add_argument("--seed", type=int, default=None, help="Co dinh so ngau nhien de chay lai y het")
    ap.add_argument("--khong-pdf", action="store_true", help="Chi ghi .tex, khong bien dich")
    ts = ap.parse_args()

    m = re.match(r"^L(\d+)_C(\d+)_", ts.ten)
    if not m:
        sys.exit("Ten ham phai bat dau bang L<lop>_C<chuong>_ , vi du L10_C1_B2_NB017_SA_C_01")
    lop, chuong = int(m.group(1)), int(m.group(2))
    module = _load_chapter_module(lop, chuong)

    if re.search(r"_\d{2}$", ts.ten):
        cac_ham = [ts.ten]
        generator_id = ts.ten[:-3]
    else:
        generator_id = ts.ten
        cac_ham = sorted(_find_variant_functions(module, generator_id))
    if not cac_ham or not all(hasattr(module, h) for h in cac_ham):
        sys.exit("Khong tim thay ham %s trong toan%d/L%d_C%d.py" % (ts.ten, lop, lop, chuong))

    _dat_seed(ts.seed)
    khoi = []
    for ten in cac_ham:
        latex = lam_dep(_call_generator_function(getattr(module, ten), ts.socau, None, None))
        try:
            kiem_tra_dung_loai_cau(generator_id, latex)
        except Exception as e:  # chi canh bao, van xuat nhap de soi
            print("  !! Canh bao loai cau: %s" % e)
        tieu = ten.replace("_", r"\_")
        khoi.append("\\noindent\\textbf{NHÁP: %s} (%d câu%s)\\par\\medskip\n%s"
                    % (tieu, ts.socau, "" if ts.seed is None else ", seed %d" % ts.seed, latex))
    noi_dung = "\n\\bigskip\n".join(khoi)

    NHAP.mkdir(exist_ok=True)
    for kieu in ("dethi", "loigiai"):
        tex = NHAP / ("%s_%s.tex" % (ts.ten, kieu))
        tex.write_text(build_latex_document("NHAP", noi_dung, lop=lop, role="teacher",
                                            ex_test_option=kieu), encoding="utf-8")
        print("Da ghi %s" % tex.relative_to(GOC))
        if not ts.khong_pdf:
            if _bien_dich(tex):
                print("Da ghi %s" % tex.with_suffix(".pdf").relative_to(GOC))
            for duoi in (".aux", ".out", ".log") if tex.with_suffix(".pdf").exists() else ():
                pass  # giu .log de soi loi; .aux/.out vo hai


if __name__ == "__main__":
    main()
