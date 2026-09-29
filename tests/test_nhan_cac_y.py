# -*- coding: utf-8 -*-
"""Nhan cac y (co Lan chot 29/09/2026): KHONG dung gach dau dong.
- Cac y cua cau tu luan (listEX): a), b), c)... - ca PDF lan web.
- Cac y liet ke trong cau trac nghiem (enumerate): 1., 2., ...
"""
import json
import pathlib
import subprocess

from app.services.answer_parser_service import trich_de_bai

GOC = pathlib.Path(__file__).resolve().parents[1]
TRANG = GOC / "app" / "templates" / "chat" / "lam_bai.html"

TL = ("\\begin{ex}%%[?]\nDe bai.\n\\begin{listEX}[1]\n\\item Hoi a \\SA[4]{$1$}\n"
      "\\item Hoi b \\SA[4]{$2$}\n\\end{listEX}\n\\loigiai{\n\\begin{listEX}[1]\n"
      "\\item Giai a\n\\item Giai b\n\\end{listEX}\n}\n\\end{ex}\n")


def test_parser_giu_moi_truong_danh_sach():
    de = trich_de_bai(TL)["de_bai"]
    assert "\\begin{listEX}" in de and "\\item" in de
    assert "\n- " not in de
    assert "\\SA" not in de          # van khong lo dap an


def test_template_pdf_tu_luan_nhan_a():
    s = (GOC / "data" / "config" / "latex_template.tex").read_text(encoding="utf-8")
    assert "\\RenewDocumentEnvironment{listEX}" in s
    assert "counter-format=tsk[a])" in s


def _ve(latex):
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
""" % (json.dumps(str(TRANG)), json.dumps(latex))
    kq = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    assert kq.returncode == 0, kq.stderr
    return kq.stdout


def test_web_tu_luan_a_b_trac_nghiem_1_2():
    tl = _ve(trich_de_bai(TL)["de_bai"])
    assert '<ol class="ds-chu">' in tl and "<li>Hoi a" in tl
    mc = _ve("Cau hoi\n\\begin{enumerate}\n\\item $P(3)$.\n\\item $P(2)$.\n\\end{enumerate}")
    assert '<ol class="ds-so">' in mc and mc.count("<li>") == 2
    assert "- $P" not in mc
    css = TRANG.read_text(encoding="utf-8")
    assert 'counter(y-chu, lower-alpha) ")"' in css
    assert 'counter(y-so) "."' in css
