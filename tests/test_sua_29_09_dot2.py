# -*- coding: utf-8 -*-
"""Cac sua theo gop y cua co Lan 29/09/2026 (dot anh chup de cuoi ky 1):
1. De cuoi ky: 30% so cau o phan truoc giua ky, 70% phan sau; cau Dung/Sai
   chi dat o chuong chua kiem tra giua ky.
2. Web: dau < > trong cong thuc khong duoc nuot noi dung.
3. Goc giua hai vecto tach muc do: NB chung diem dau, TH khac diem dau,
   TH chung diem cuoi.
4. P(x) voi x thuoc R (khong dung n); dau < / <= khong con luon ra 0.
5. Gia tri bat thuong: NB070 de thay, TH080_MC_B sat nguong.
"""
import json
import pathlib
import random
import re
import subprocess
import sys

GOC = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))

from app.services.exam_blueprint_service import build_blueprint  # noqa: E402
from app.services.exam_scope_service import load_scope_heso23  # noqa: E402


def _ti_le_truoc(lop, ki_thi, so_de=40):
    sc = load_scope_heso23(lop, ki_thi)
    truoc = set(sc["phan_bo_ty_le"]["truoc_giua_ky"]["pham_vi_bai"])
    tong = tr = 0
    chuong_tf = set()
    for s in range(so_de):
        random.seed(900 + s)
        bp = build_blueprint(lop, "HeSo2_HeSo3", ki_thi=ki_thi)
        for l in ("trac_nghiem", "tra_loi_ngan", "tu_luan"):
            for it in bp[l]:
                k = it.get("tong_so_cau", 1)
                tong += k
                tr += k * ("L%d_C%s_B%s" % (lop, it["chuong_so"], it["bai_so"]) in truoc)
        for it in bp["dung_sai"]:
            tong += it["so_cau"]
            chuong_tf.add(it["chuong_so"])
            assert it["bai_id"] not in truoc, "cau Dung/Sai roi vao phan truoc giua ky"
    chuong_truoc = {int(b.split("_")[1][1:]) for b in truoc}
    return tr / tong, chuong_tf, chuong_truoc


def test_cuoi_ky_30_70_va_dung_sai():
    for lop, ki in [(10, "cuoi_ky_1"), (10, "cuoi_ky_2"), (11, "cuoi_ky_2")]:
        tl, chuong_tf, chuong_truoc = _ti_le_truoc(lop, ki)
        assert 0.25 <= tl <= 0.35, (lop, ki, tl)
    # lop 10 cuoi ky 2: chuong 8, 9 chua kiem tra giua ky -> Dung/Sai chi o do
    _tl, chuong_tf, chuong_truoc = _ti_le_truoc(10, "cuoi_ky_2", 20)
    assert chuong_tf <= {8, 9} and not (chuong_tf & chuong_truoc)


def _ve_web(latex):
    trang = GOC / "app" / "templates" / "chat" / "lam_bai.html"
    js = r"""
const fs = require('fs');
const html = fs.readFileSync(%s, 'utf8');
const js = html.split('<script>').pop().split('</script>')[0];
const lay = (ten) => { const i = js.indexOf('function ' + ten + '(');
  let d = 0, j = js.indexOf('{', i);
  for (let k = j; k < js.length; k++) { if (js[k] === '{') d++;
    else if (js[k] === '}') { d--; if (!d) return js.slice(i, k + 1); } } };
eval(lay('xuLyDanhSach') + '\n' + lay('tachDoanToan') + '\n' + lay('xuLyCanGiuaVaBang') + '\n' + lay('renderLatexText'));
process.stdout.write(renderLatexText(%s));
""" % (json.dumps(str(trang)), json.dumps(latex))
    kq = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    assert kq.returncode == 0, kq.stderr
    return kq.stdout


def test_web_dau_be_hon_khong_nuot_cong_thuc():
    ra = _ve_web(r"$\forall x\in\mathbb R,\ x^2+1<0$ và $a>b$")
    assert "&lt;0" in ra and "&gt;b" in ra and "<0" not in ra


def _cap(o):
    """Cap vecto trong DE BAI (bo phan phuong an va loi giai)."""
    de = [c.split("\\choice")[0] for c in o.split("\\begin{ex}")[1:]]
    return [re.search(r"\\overrightarrow\{(\w\w)\}\$ và \$\\overrightarrow\{(\w\w)\}", d).groups()
            for d in de]


def test_goc_vecto_dung_muc_do():
    from toan10 import L10_C4 as m
    for ten, dk in [("L10_C4_B11_NB057_MC_A_01", lambda a, b: a[0] == b[0]),
                    ("L10_C4_B11_NB057_MC_A_02", lambda a, b: a[0] == b[0]),
                    ("L10_C4_B11_TH057_MC_A_01", lambda a, b: a[0] != b[0] and a[1] != b[1]),
                    ("L10_C4_B11_TH057_MC_A_02", lambda a, b: a[0] != b[0] and a[1] != b[1]),
                    ("L10_C4_B11_TH057_MC_B_01", lambda a, b: a[0] != b[0] and a[1] == b[1]),
                    ("L10_C4_B11_TH057_MC_B_02", lambda a, b: a[0] != b[0] and a[1] == b[1])]:
        random.seed(3)
        cap = _cap(getattr(m, ten)(8))
        assert cap and all(dk(a, b) for a, b in cap), (ten, cap)


def test_menh_de_chua_bien_x_thuc():
    import numpy as np
    from toan10 import L10_C1 as m
    so_khac_0 = 0
    for sd in range(60):
        np.random.seed(sd)
        random.seed(sd)
        o = m.L10_C1_B1_VD014_MC_A_01(2) + m.L10_C1_B1_VD014_SA_A_01(2)
        assert "P(n)" not in o and "n \\in \\mathbb" not in o
        so_khac_0 += len(re.findall(r"\\True \$[1-9]", o))
    assert so_khac_0 > 30   # dau < va <= khong con luon ra 0


def test_gia_tri_bat_thuong_sat_nguong():
    from toan10 import L10_C5 as m
    for sd in range(100):
        random.seed(sd)
        Z, la, bay = m._mau_ngoai_le_sat_nguong()
        q1, _q2, q3 = m._tu_phan_vi(Z)
        d = q3 - q1
        tren, duoi = q3 + 1.5 * d, q1 - 1.5 * d
        assert [x for x in Z if x < duoi or x > tren] == [la]
        ng = tren if la > q3 else duoi
        assert abs(la - ng) <= 2 and abs(bay - ng) <= 2
