# -*- coding: utf-8 -*-
"""Câu hỏi phải HIỆN ĐÚNG trên web, không chỉ đúng trong file PDF.

Vì sao có file này (29/09/2026): cô Lan mở trang "Làm bài trực tiếp" và
thấy bốn kiểu hỏng, tất cả đều KHÔNG lộ ra trong file PDF:

1. Câu có hệ bất phương trình hiện ra ô đỏ "Misplaced &".
   Lệnh \\heva (hệ và) và \\hoac (hệ hoặc) do latex_template.tex tự định
   nghĩa; MathJax trên web không biết nên \\begin{aligned} không bao giờ
   mở ra, dấu & thành & trần. Sửa: khai báo lại các lệnh ấy trong phần
   macros của MathJax. Bài test dưới soi cho hai bên không lệch nhau.

2. Hệ phương trình hiện thành một mạch "x >= -6x <= 34x - 9y <= ...".
   renderLatexText đổi MỌI "\\\\" thành <br>, kể cả "\\\\" nằm trong công
   thức - mà ở đó nó là dấu xuống dòng CỦA công thức.

3. Các ý của câu tự luận dính liền nhau và có "......" ở sau mỗi ý.

4. Phương án trả lời bằng chữ hiện thành "Miềnngũgiác" - chữ tiếng Việt
   bị đặt trong $...$ (dùng nhầm MC_SA_answer_const thay vì
   MC_SA_answer_text) nên mất hết dấu cách.

Ngoài ra còn hai lỗi cùng họ tìm được khi soát cả ngân hàng: chữ đậm
viết kiểu Markdown (**đậm**) lọt vào LaTeX, và dấu "\\\\" cuối dòng trong
f-string KHÔNG có tiền tố r (nên chỉ ra MỘT dấu gạch chéo, mất luôn
dấu xuống dòng trong lời giải).
"""
import glob
import importlib
import random
import re
import subprocess
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))

TRANG_WEB = [GOC / "app/templates/chat/lam_bai.html",
             GOC / "app/templates/chat/chat.html"]
MAU_TEMPLATE = GOC / "data/config/latex_template.tex"

CO_DAU = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
    r"ùúủũụưừứửữựỳýỷỹỵđ]", re.I)
TOAN = re.compile(r"\$\$[\s\S]*?\$\$|\$[^$]*\$")
LENH_CHU = re.compile(
    r"\\(?:text|textbf|textit|mathrm|operatorname|widehat|overline)\s*\{[^{}]*\}")


def _cac_ham():
    ra = []
    for tep in sorted(glob.glob(str(GOC / "data/python_bank/toan1*/L*.py"))):
        ten_mod = "%s.%s" % (Path(tep).parent.name, Path(tep).stem)
        mod = importlib.import_module(ten_mod)
        tien_to = Path(tep).stem.split("_")[0]
        for t in sorted(n for n in dir(mod) if n.startswith(tien_to + "_")):
            if callable(getattr(mod, t)):
                ra.append((t, getattr(mod, t)))
    return ra


CAC_HAM = _cac_ham()


def _sinh(f, ten):
    random.seed(20260929)
    return f(1) if "_SA_" in ten else f(1, 1)


def test_co_ham_de_soat():
    assert len(CAC_HAM) > 300, len(CAC_HAM)


@pytest.mark.parametrize("ten,f", CAC_HAM, ids=[t for t, _ in CAC_HAM])
def test_khong_de_chu_tieng_viet_tran_trong_cong_thuc(ten, f):
    """Chữ tiếng Việt trong $...$ sẽ mất hết dấu cách và in nghiêng."""
    s = _sinh(f, ten)
    for m in TOAN.finditer(s):
        con_lai = LENH_CHU.sub("", m.group(0))
        assert not CO_DAU.search(con_lai), (
            "%s: chữ tiếng Việt nằm trần trong công thức %r - phải bọc "
            "\\text{...} hoặc dùng MC_SA_answer_text thay cho "
            "MC_SA_answer_const." % (ten, m.group(0)[:80])
        )


@pytest.mark.parametrize("ten,f", CAC_HAM, ids=[t for t, _ in CAC_HAM])
def test_khong_dung_chu_dam_kieu_markdown(ten, f):
    s = _sinh(f, ten)
    m = re.search(r"\*\*[^*\n]+\*\*", s)
    assert not m, ("%s: %r là chữ đậm kiểu Markdown, LaTeX không hiểu - "
                   "dùng \\textbf{...}" % (ten, m.group(0)[:50] if m else ""))


@pytest.mark.parametrize("ten,f", CAC_HAM, ids=[t for t, _ in CAC_HAM])
def test_khong_co_dau_gach_cheo_le_cuoi_dong(ten, f):
    r"""f-string quên tiền tố r: "\\" chỉ ra MỘT gạch chéo, mất xuống dòng."""
    s = _sinh(f, ten)
    assert not re.search(r"(?<!\\)\\\s*\n", s), (
        "%s: có dấu \\ đứng một mình cuối dòng. Trong f-string KHÔNG có "
        "tiền tố r thì phải viết \\\\\\\\ mới ra được dấu xuống dòng "
        "\\\\ của LaTeX." % ten)


def _macro_cua_template():
    noi_dung = MAU_TEMPLATE.read_text(encoding="utf-8")
    return set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}\[\d+\]", noi_dung))


# Cac lenh cua template ma MathJax da biet san (khong can khai bao lai).
MATHJAX_BIET_SAN = {"tieude", "chantrang", "hetde", "circletext",
                    "fillcircletext", "loigiai"}


@pytest.mark.parametrize("trang", TRANG_WEB, ids=lambda p: p.name)
def test_macro_rieng_cua_de_phai_khai_bao_cho_MathJax(trang):
    """Lệnh nào latex_template.tex tự định nghĩa mà câu hỏi có dùng thì
    MathJax cũng phải biết - nếu không, trên web hiện ra 'Misplaced &'."""
    html = trang.read_text(encoding="utf-8")
    assert "macros:" in html, "%s chưa khai báo macros cho MathJax" % trang.name
    for ten in _macro_cua_template() - MATHJAX_BIET_SAN:
        # Chi bat buoc voi lenh THUC SU duoc dung trong ngan hang de
        if not _lenh_co_dung_trong_ngan_hang(ten):
            continue
        assert re.search(r"\b%s\s*:" % ten, html), (
            "%s: lệnh \\%s có dùng trong ngân hàng đề và do "
            "latex_template.tex định nghĩa, nhưng MathJax chưa biết -> "
            "trên web sẽ hỏng." % (trang.name, ten))


def _lenh_co_dung_trong_ngan_hang(ten):
    for tep in glob.glob(str(GOC / "data/python_bank/toan1*/L*.py")):
        if re.search(r"\\\\?%s\b" % ten, Path(tep).read_text(encoding="utf-8")):
            return True
    return False


def test_trang_lam_bai_khong_doi_gach_cheo_trong_cong_thuc():
    """renderLatexText phải tách vùng công thức ra trước khi đổi \\\\."""
    js = (GOC / "app/templates/chat/lam_bai.html").read_text(encoding="utf-8")
    assert "function tachDoanToan(" in js, (
        "lam_bai.html thiếu hàm tách vùng công thức - đổi \\\\ thành <br> "
        "trên cả chuỗi sẽ làm vỡ mọi hệ phương trình")
    than = js.split("function renderLatexText(")[1].split("\n}")[0]
    assert "tachDoanToan(" in than, "renderLatexText chưa dùng tachDoanToan"


def test_trang_lam_bai_hieu_moi_truong_listEX():
    js = (GOC / "app/templates/chat/lam_bai.html").read_text(encoding="utf-8")
    assert "'listEX'" in js, (
        "ngân hàng đề dùng \\begin{listEX} cho các ý của câu tự luận; "
        "không xử lý thì các ý dính liền một mạch")


NODE = None
try:
    NODE = subprocess.run(["node", "--version"], capture_output=True,
                          timeout=20).returncode == 0
except Exception:
    NODE = False


@pytest.mark.skipif(not NODE, reason="máy này không có node")
def test_chay_that_ham_render_tren_de_bai_that():
    """Nạp y nguyên hàm render của trang web rồi chạy trên đề bài thật."""
    from app.services.answer_parser_service import trich_dap_an
    mau = []
    for ten, f in CAC_HAM[:60]:
        try:
            d = trich_dap_an(_sinh(f, ten))
        except Exception:
            continue
        if d.get("de_bai"):
            mau.append([ten, d["de_bai"]])
    assert mau

    import json
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tep_mau = Path(tmp) / "mau.json"
        tep_mau.write_text(json.dumps(mau, ensure_ascii=False), encoding="utf-8")
        kich_ban = Path(tmp) / "thu.js"
        kich_ban.write_text(_KICH_BAN_JS % (
            GOC / "app/templates/chat/lam_bai.html", tep_mau), encoding="utf-8")
        kq = subprocess.run(["node", str(kich_ban)], capture_output=True,
                            text=True, timeout=120)
    assert kq.returncode == 0, kq.stdout + kq.stderr
    assert "SACH" in kq.stdout, kq.stdout


_KICH_BAN_JS = r"""
const fs = require('fs');
const html = fs.readFileSync('%s', 'utf8');
const js = html.split('<script>').pop().split('</script>')[0];
const lay = (ten) => { const i = js.indexOf('function ' + ten + '(');
  let d = 0, j = js.indexOf('{', i);
  for (let k = j; k < js.length; k++) { if (js[k] === '{') d++;
    else if (js[k] === '}') { d--; if (!d) return js.slice(i, k + 1); } } };
eval(lay('xuLyDanhSach') + '\n' + lay('tachDoanToan') + '\n' + lay('xuLyCanGiuaVaBang') + '\n' + lay('renderLatexText'));
const mau = JSON.parse(fs.readFileSync('%s', 'utf8'));
let loi = 0;
for (const [ten, de] of mau) {
  const ra = renderLatexText(de);
  const toan = tachDoanToan(ra).filter(d => d.toan).map(d => d.chu).join('');
  const canh = [];
  if (toan.includes('<br>')) canh.push('co <br> lot vao trong cong thuc');
  if (ra.includes('\\begin{listEX}') || ra.includes('\\item')) canh.push('con listEX/item tho');
  if (ra.includes('......')) canh.push('con dau cham ......');
  if (/\\(SA|shortans)\b/.test(ra)) canh.push('con \\SA/\\shortans (lo dap an)');
  if (canh.length) { loi++; console.log('LOI', ten, canh.join(' | ')); }
}
console.log(loi ? ('CO ' + loi + ' cau loi') : 'SACH');
process.exit(loi ? 1 : 0);
"""
