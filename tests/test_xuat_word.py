# -*- coding: utf-8 -*-
"""
Xuat de / loi giai ra Word (.docx) cho tai khoan giao vien.

Co Lan (30/09/2026): "tai khoan gv duoc xuat them dang word. cong thuc thi ra
cong thuc cua word". Kiem tra:
  - cong thuc la phuong trinh goc cua Word (the <m:oMath>), khong phai chu tho;
  - ban de KHONG lo dap an, ban loi giai CO dap an + loi giai;
  - nhieu ma de -> ngat trang; phong Times New Roman;
  - mot cau LaTeX hong khong lam hong ca file (thay bang dong bao xem PDF);
  - chi giao vien moi tai duoc;
  - khong ham sinh cau nao con sot "%d", "%s" chua dien so hay "\\%%".
"""
import importlib
import pkgutil
import random
import re
import shutil
import sys
import zipfile
from pathlib import Path

import numpy as np
import pytest

GOC = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(GOC / "data" / "python_bank"), str(GOC / "data" / "python_bank" / "toan10")]

co_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="may khong co pandoc")

CAU_MC = r"""\begin{ex}%%[?]
Cho $\cos A = \dfrac{3}{5}$ và tập $A = \left\{x \in \mathbb{R} \mid x \ge 2\right\}$. Khẳng định nào đúng?
\choice{\True $\sin A = \dfrac{4}{5}$}
{$\sin A = \dfrac{3}{4}$}
{$\sin A = \dfrac{5}{4}$}
{$\sin A = -\dfrac{4}{5}$}
\loigiai{
$\sin A = \sqrt{1 - \cos^2 A} = \dfrac{4}{5}$ (vì $\sin A > 0$).
}
\end{ex}
"""

CAU_TF = r"""\begin{ex}%%[?]
Cho hệ $\heva{&x + y = 3\\&x - y = 1}$. Xét tính đúng sai:
\choiceTFt
{\True $x = 2$}
{$y = 2$}
{\True $x + y = 3$}
{$\vv{AB} = \vv{0}$}
\loigiai{
\begin{itemchoice}
\itemch Đúng.
\itemch Sai.
\itemch Đúng.
\itemch Sai.
\end{itemchoice}
}
\end{ex}
"""

CAU_SA = r"""\begin{ex}%%[?]
Tính $\dfrac{1}{2} + \dfrac{1}{4}$ (viết dạng số thập phân).
\shortans{0,75}
\loigiai{
$\dfrac{3}{4} = 0{,}75$.
}
\end{ex}
"""


def _tep_de(tmp_path, cau_mc=CAU_MC, so_ma=2):
    from app.services.exam_assembler_service import _ghep_4_phan, _khung_mot_ma_de
    from app.services.latex_service import build_latex_document
    ma = [_khung_mot_ma_de("KIỂM TRA THỬ", 10, "teacher", str(1000 + i),
                           _ghep_4_phan({"MC": [cau_mc], "TF": [CAU_TF], "SA": [CAU_SA]}))
          for i in range(1, so_ma + 1)]
    tex = build_latex_document("X", "\n\\newpage\n".join(ma), lop=10, role="teacher",
                               ex_test_option="loigiai")
    p = tmp_path / "de.tex"
    p.write_text(tex, encoding="utf-8")
    return p


def _xml(docx):
    with zipfile.ZipFile(docx) as z:
        return z.read("word/document.xml").decode("utf-8"), z.read("word/styles.xml").decode("utf-8")


def _chu(xml):
    x = re.sub(r"<m:oMath>.*?</m:oMath>", "", xml, flags=re.S)
    return re.sub(r"<[^>]+>", "", x)


@co_pandoc
def test_cong_thuc_la_phuong_trinh_word(tmp_path):
    from app.services import word_service as w
    ra = w.xuat_word(_tep_de(tmp_path), True, "test_word_lg")
    xml, styles = _xml(ra)
    assert xml.count("<m:oMath>") > 20
    assert "<m:f>" in xml                       # phan so \dfrac -> phan so cua Word
    chu = _chu(xml)
    assert not re.search(r"\\[a-zA-Z]+", chu), "con lenh LaTeX lot ra thanh chu: %s" % re.findall(r"\\[a-zA-Z]+", chu)
    assert "@@" not in xml
    assert "Times New Roman" in styles
    assert xml.count('w:type="page"') == 1      # 2 ma de -> 1 lan ngat trang
    ra.unlink()


@co_pandoc
def test_ban_de_khong_lo_dap_an(tmp_path):
    from app.services import word_service as w
    de = w.xuat_word(_tep_de(tmp_path, so_ma=1), False, "test_word_de")
    lg = w.xuat_word(_tep_de(tmp_path, so_ma=1), True, "test_word_lg2")
    chu_de, chu_lg = _chu(_xml(de)[0]), _chu(_xml(lg)[0])
    for lo in ("Chọn đáp án", "Lời giải", "Đáp số", "(Đúng)", "(Sai)"):
        assert lo not in chu_de, lo
    for co in ("Chọn đáp án A", "Lời giải", "Đáp số", "(Đúng)", "(Sai)"):
        assert co in chu_lg, co
    assert "PHẦN I." in chu_de and "PHẦN II." in chu_de and "PHẦN III." in chu_de
    de.unlink(); lg.unlink()


@co_pandoc
def test_cau_hong_khong_lam_hong_ca_file(tmp_path):
    from app.services import word_service as w
    hong = CAU_MC.replace("Khẳng định nào đúng?", "Chọn S_1 đáp án đúng.")
    ra = w.xuat_word(_tep_de(tmp_path, cau_mc=hong, so_ma=1), True, "test_word_hong")
    chu = _chu(_xml(ra)[0])
    assert "chưa chuyển được sang Word" in chu
    assert "Đáp số" in chu                      # cac cau khac van con
    ra.unlink()


def test_danh_sach_listEX_thanh_a_b():
    from app.services.word_service import _doi_danh_sach
    ra = _doi_danh_sach(r"\begin{listEX}[1]\item Tính $x$. \item Tính $y$.\end{listEX}")
    assert r"\textbf{a)} Tính $x$." in ra and r"\textbf{b)} Tính $y$." in ra
    ra = _doi_danh_sach(r"\begin{enumerate}\item P. \item Q.\end{enumerate}")
    assert r"\textbf{1.} P." in ra and r"\textbf{2.} Q." in ra


def test_chi_giao_vien_tai_duoc_word():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    r = client.get("/api/exam/tai-word/khong-co-id?ban=de", follow_redirects=False)
    assert r.status_code in (303, 401, 403)


def test_khong_ham_nao_sot_ma_dinh_dang():
    """'%d', '%s' chua dien so hoac '\\%%' (dau phan tram + chu thich) lam hong
    ca PDF lan Word - da gap o L10_C5 TH080 va L11_C9 TH143 (30/09/2026)."""
    loi = []
    for lop in ("toan10", "toan11", "toan12"):
        for mi in pkgutil.iter_modules([str(GOC / "data" / "python_bank" / lop)]):
            M = importlib.import_module(lop + "." + mi.name)
            for ten in sorted(n for n in dir(M) if re.match(r"L1\d_C\d+_.*_\d\d$", n)):
                for sd in range(3):
                    random.seed(sd)
                    np.random.seed(sd)
                    f = getattr(M, ten)
                    try:
                        out = f(2)
                    except TypeError:
                        out = f(2, 1)
                    m = re.search(r"%[ds](?![a-zA-Z])|\\%%", out)
                    if m:
                        loi.append((ten, out[max(0, m.start() - 40): m.end() + 20]))
                        break
    assert not loi, loi


def test_quad_ngoai_cong_thuc_khong_lam_dinh_so():
    r"""Mau so lieu "$5$\quad $8$\quad $9$" (bai thong ke L10_C5) bi pandoc 2.9 bo
    mat \quad -> Word hien "589" (co Lan bao 30/09/2026)."""
    from app.services.word_service import _khoang_trang_ngoai_toan as k
    ra = k(r"An: \quad $5$\quad $8$\qquad $9$ và $a\quad b$ \\ x")
    assert "$5$\u2003$8$\u2003\u2003$9$" in ra
    assert r"$a\quad b$" in ra                 # trong cong thuc giu nguyen
    assert r"\\ x" in ra                        # xuong dong khong bi dong vao


@co_pandoc
def test_mau_so_lieu_tach_so_va_phuong_an_co_cham(tmp_path):
    from app.services import word_service as w
    cau = CAU_MC.replace("Khẳng định nào đúng?",
                         r"Điểm: \quad $5$\quad $8$\quad $9$\quad $10$. Khẳng định nào đúng?")
    ra = w.xuat_word(_tep_de(tmp_path, cau_mc=cau, so_ma=1), False, "test_word_quad")
    xml = _xml(ra)[0]
    # giua hai cong thuc $5$ va $8$ phai co ki tu cach (khong dinh thanh "58")
    assert re.search(r"<m:t>5</m:t>(?:(?!<m:t>).)*?</m:oMath>(?:(?!<m:oMath>).)*?\u2003"
                     r"(?:(?!<m:oMath>).)*?<m:oMath>(?:(?!</m:oMath>).)*?<m:t>8</m:t>", xml, re.S)
    ra.unlink()


def test_phuong_an_trac_nghiem_khong_tu_cham_cuoi():
    r"""Goi ex_test TU THEM "." sau moi phuong an \choice; ham sinh cau ma tu
    cham cuoi se ra ".." tren PDF (co Lan bao 30/09/2026)."""
    from app.services.answer_parser_service import trich_dap_an
    loi = []
    for lop in ("toan10", "toan11", "toan12"):
        for mi in pkgutil.iter_modules([str(GOC / "data" / "python_bank" / lop)]):
            M = importlib.import_module(lop + "." + mi.name)
            for ten in sorted(n for n in dir(M) if re.match(r"L1\d_C\d+_.*_MC_.*_\d\d$", n)):
                f = getattr(M, ten)
                for sd in range(2):
                    random.seed(sd)
                    np.random.seed(sd)
                    try:
                        out = f(2)
                    except TypeError:
                        out = f(2, 1)
                    for k in re.findall(r"\\begin\{ex\}.*?\\end\{ex\}", out, re.S):
                        d = trich_dap_an(k)
                        if d.get("loai_cau") != "MC":
                            continue
                        for v in d["phuong_an"].values():
                            s = re.sub(r"\$\s*$", "", v.strip()).rstrip()
                            if s.endswith(".") and not s.endswith(r"\right."):
                                loi.append((ten, v.strip()[-40:]))
    assert not loi, loi[:10]
