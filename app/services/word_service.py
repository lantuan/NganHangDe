r"""
XUAT DE / LOI GIAI RA FILE WORD (.docx) - CHI TAI KHOAN GIAO VIEN.

Nguon: dung tep .tex DA LUU luc sinh de (ban loi giai, xem
exam_assembler_service) - KHONG sinh lai de, nen file Word khop tung chu
voi ban PDF da phat.

Cong thuc toan ra dang PHUONG TRINH GOC CUA WORD (Office Math / OMML - loai
bam vao sua duoc bang Equation cua Word, khong phai anh). Viec doi cong thuc
do pandoc lam (pandoc -f latex -t docx). KHONG goi AI, khong ton token: chi
la Python + pandoc chay tren VPS, moi de vai giay.

Hinh ve TikZ (va bang bien thien tabvar) Word khong ve duoc -> dich ra anh
PNG bang chinh bo dich hinh cua web (hinh_ve_service, co bo nho dem) roi
chen vao.

Cach lam:
  1. Tach than tep .tex thanh tung ma de (moi ma de bat dau bang \tieude).
  2. Trong moi ma de: tieu de PHAN I/II/III/IV va tung khoi \begin{ex}.
  3. Moi khoi cau hoi -> answer_parser_service.trich_dap_an (dung chung voi
     trang lam bai tren web): de bai, phuong an, dap an, loi giai.
  4. Doi cac lenh rieng cua ex_test / khung de (\heva, \hoac, \vv, listEX,
     \immini, ...) sang LaTeX chuan ma pandoc hieu.
  5. pandoc -> .docx; chinh lai phong chu Times New Roman 12 va chen ngat
     trang giua cac ma de.

Xem docs/21_TAI_KHOAN_GIAO_VIEN.md (Buoc 6).
"""
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from app.services.answer_parser_service import (
    _tim_khoi_dong,
    trich_dap_an,
)
from app.services import hinh_ve_service

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "data" / "exports"
DAU_NGAT_TRANG = "@@NGATTRANG@@"
DAU_GIUA = "@@GIUA@@"          # doan nao co dau nay se duoc can giua
_MOC_CAU = "% @@CAU@@"         # dong chu thich bao quanh moi cau (pandoc bo qua)


class WordExportError(Exception):
    pass


# Nhãn của khung đề theo ngôn ngữ (đề tiếng Anh: khung ex_test_en / latex_template_en, xem docs/28)
_CHU = {
    "vi": {
        "phan": "PHẦN", "nam_hoc_re": r"NĂM HỌC ([0-9]{4}-[0-9]{4})", "ma_re": r"Mã đề (\d+)",
        "ma_de": "Mã đề", "truong": "TRƯỜNG THPT CHUYÊN HÙNG VƯƠNG",
        "nam_hoc_dong": "NĂM HỌC %s -- MÔN TOÁN, LỚP %s",
        "thi_sinh": "Họ tên thí sinh: ........................................ Lớp: .......... Phòng kiểm tra: ..........",
        "cau": "Câu", "bai": "Bài", "dung": "Đúng", "sai": "Sai", "chon_dap_an": "Chọn đáp án",
        "dap_so": "Đáp số:", "loi_giai": "Lời giải.", "het": "--- HẾT ---",
        "chua_chuyen": "[Câu này chưa chuyển được sang Word - xem bản PDF.]",
        "loi_re": r"\\textbf\{(Câu|Bài) (\d+)",
    },
    "en": {
        "phan": "PART", "nam_hoc_re": r"SCHOOL YEAR ([0-9]{4}-[0-9]{4})", "ma_re": r"Exam code (\d+)",
        "ma_de": "Exam code", "truong": "HUNG VUONG GIFTED HIGH SCHOOL",
        "nam_hoc_dong": "SCHOOL YEAR %s -- MATHEMATICS, GRADE %s",
        "thi_sinh": "Name: ........................................ Class: .......... Room: ..........",
        "cau": "Question", "bai": "Problem", "dung": "True", "sai": "False", "chon_dap_an": "Correct answer:",
        "dap_so": "Answer:", "loi_giai": "Solution.", "het": "--- END ---",
        "chua_chuyen": "[This question could not be converted to Word - see the PDF version.]",
        "loi_re": r"\\textbf\{(Question|Problem) (\d+)",
    },
}


# ----------------------------------------------------------------------
# 1. Doi lenh rieng sang LaTeX chuan
# ----------------------------------------------------------------------

_MOI_TRUONG_HINH = re.compile(
    r"\\begin\{(tikzpicture|tabvar)\}.*?\\end\{\1\}", re.S)


def _thay_lenh_mot_doi(text: str, ten: str, ham) -> str:
    """Thay moi \\ten{X} bang ham(X) (dem ngoac long nhau)."""
    pat = re.compile(re.escape(ten) + r"(?![A-Za-z])\s*")
    ra, i = [], 0
    while True:
        m = pat.search(text, i)
        if not m:
            ra.append(text[i:])
            break
        j = m.end()
        if j >= len(text) or text[j] != "{":
            ra.append(text[i:j])
            i = j
            continue
        ra.append(text[i:m.start()])
        noi, i = _tim_khoi_dong(text, j)
        ra.append(ham(noi))
    return "".join(ra)


def _thay_immini(text: str) -> str:
    r"""\immini{CHU}{HINH} -> CHU roi HINH (xuong dong)."""
    pat = re.compile(r"\\immini(?![A-Za-z])(\[[^\]]*\])?\s*")
    ra, i = [], 0
    while True:
        m = pat.search(text, i)
        if not m:
            ra.append(text[i:])
            break
        j = m.end()
        if j >= len(text) or text[j] != "{":
            ra.append(text[i:j])
            i = j
            continue
        ra.append(text[i:m.start()])
        try:
            chu, k = _tim_khoi_dong(text, j)
        except Exception:
            # de bai bi cat ngang giua \immini{...} (cau Dung/Sai: \choiceTFt
            # nam TRONG \immini) - bo lenh, giu phan chu con lai
            ra.append(text[j + 1:])
            break
        while k < len(text) and text[k] in " \t\r\n":
            k += 1
        hinh = ""
        if k < len(text) and text[k] == "{":
            hinh, k = _tim_khoi_dong(text, k)
        ra.append(chu + "\n\n" + hinh + "\n\n")
        i = k
    return "".join(ra)


# itemchoice: loi giai cau Dung/Sai (math_type) - moi \itemch la mot y a), b)...
_DS_CHU = ("listEX", "listEXV", "enumEX", "tasks", "taskEX", "itemchoice")
_DS_SO = ("enumerate",)
_DS_CHAM = ("itemize",)
_DS = _DS_CHU + _DS_SO + _DS_CHAM
_MO_DS = re.compile(r"\\begin\{(%s)\}" % "|".join(_DS))


def _nhan(kieu: str, k: int) -> str:
    if kieu == "chu":
        return "%s)" % "abcdefghijklmnopqrstuvwxyz"[k]
    if kieu == "so":
        return "%d." % (k + 1)
    return "$\\bullet$"


def _doi_danh_sach(text: str) -> str:
    r"""Doi cac moi truong danh sach thanh cac doan co nhan a), 1., o.

    Lam tu TRONG ra NGOAI (danh sach long nhau). Pandoc khong hieu listEX,
    tasks, enumEX cua goi ex_test nen phai tu viet nhan.
    """
    for _ in range(50):
        mo = list(_MO_DS.finditer(text))
        if not mo:
            return text
        # tim danh sach trong cung: lay cai mo cuoi cung truoc \end dau tien
        m = mo[-1]
        ten = m.group(1)
        dong = re.search(r"\\end\{%s\}" % re.escape(ten), text[m.end():])
        if not dong:
            return text
        than = text[m.end(): m.end() + dong.start()]
        het = m.end() + dong.end()
        # bo tham so tuy chon ngay sau \begin{..}: [..], (..), {..} (so cot)
        than = re.sub(r"^\s*(\[[^\]]*\]|\([^)]*\))*\s*(\{\d+\})?", "", than)
        kieu = "chu" if ten in _DS_CHU else ("so" if ten in _DS_SO else "cham")
        if ten == "enumerate":
            tuy = re.match(r"\s*\[([^\]]*)\]", text[m.end():])
            if tuy and "a" in tuy.group(1):
                kieu = "chu"
        phan = re.split(r"\\(?:item|task|itemch)(?![A-Za-z])", than)
        cac_y = []
        k = 0
        for p in phan[1:]:
            nhan_rieng = re.match(r"\s*\[([^\]]*)\]", p)
            if nhan_rieng:
                nhan = nhan_rieng.group(1)
                p = p[nhan_rieng.end():]
            else:
                nhan = _nhan(kieu, k)
            k += 1
            cac_y.append("\\textbf{%s} %s" % (nhan, p.strip()))
        text = text[:m.start()] + "\n\n" + "\n\n".join(cac_y) + "\n\n" + text[het:]
    return text


def _lam_sach(text: str, thu_muc_anh: Path | None, anh: list, lang: str = "vi") -> str:
    """Doi mot doan LaTeX cua cau hoi sang LaTeX chuan cho pandoc."""
    if not text:
        return ""
    t = text.replace(r"\True", "")
    # "\%%" = dau phan tram + dau chu thich (loi go o ham sinh cau) -> chi giu \%
    t = t.replace(r"\%%", r"\%")
    # dau ngoac kep kieu LaTeX ``...'' - co cau de dau mo NAM TRONG $...$, pandoc
    # se khong doc duoc cong thuc; doi han sang ngoac kep Unicode
    # (chi doi CAP ``...''; dau '' dung mot minh la dao ham cap hai f''(x), giu nguyen)
    t = re.sub(r"``(.*?)''", "\u201c\\1\u201d", t, flags=re.S)
    t = re.sub(r"\\lq\\lq(.*?)\\rq\\rq", "\u201c\\1\u201d", t, flags=re.S)
    t = _thay_immini(t)
    # hinh ve bi boc trong $...$ (co ham sinh cau viet "hinh anh ${\begin{tikzpicture}...}$")
    t = re.sub(r"\$\s*\{?\s*(\\begin\{(tikzpicture|tabvar)\}.*?\\end\{\2\})\s*\}?\s*\$", r"\1", t, flags=re.S)
    # Word/LibreOffice hay thieu ki tu U+2216 cua \setminus; SGK viet dau "\" thuong
    t = t.replace(r"\setminus", r"\backslash ")

    # hinh ve -> anh PNG
    def ve(m):
        try:
            duong = hinh_ve_service.dich_hinh(m.group(0), chi_png=True)
        except Exception:
            return (r"\textit{[Figure: see the PDF version]}" if lang == "en"
                    else r"\textit{[Hình vẽ: xem bản PDF]}")
        anh.append(duong)
        return "\n\n\\includegraphics{%s}\n\n" % duong
    t = _MOI_TRUONG_HINH.sub(ve, t)

    t = _thay_lenh_mot_doi(t, r"\heva", lambda x: r"\begin{cases}%s\end{cases}" % x.replace("&", ""))
    t = _thay_lenh_mot_doi(t, r"\hoac", lambda x: r"\left[\begin{matrix}%s\end{matrix}\right." % x.replace("&", ""))
    t = _thay_lenh_mot_doi(t, r"\vv", lambda x: r"\overrightarrow{%s}" % x)
    for ten in (r"\centerline", r"\indam", r"\indamm"):
        t = _thay_lenh_mot_doi(t, ten, lambda x: x)
    for ten in (r"\SA", r"\shortans", r"\dongcham", r"\cham", r"\label"):
        t = re.sub(re.escape(ten) + r"(?![A-Za-z])(\[[^\]]*\])?\{[^{}]*\}", "", t)
    t = re.sub(r"\\(noindent|hfill|allowdisplaybreaks|GiamKhoangTrangThua)(?![A-Za-z])", "", t)
    t = re.sub(r"\\(vspace|hspace)\*?\{[^{}]*\}", " ", t)
    t = t.replace(r"\dotfill", "..........")
    t = re.sub(r"%%\[\?\]", "", t)
    t = _doi_danh_sach(t)
    t = _khoang_trang_ngoai_toan(t)
    return t.strip()


# Phan cong thuc: $..$, $$..$$, \(..\), \[..\] va cac moi truong toan hien thi.
_DOAN_TOAN = re.compile(
    r"(\$\$.*?\$\$|(?<!\\)\$.*?(?<!\\)\$|\\\(.*?\\\)|\\\[.*?\\\]"
    r"|\\begin\{(align|equation|gather|eqnarray|multline)\*?\}.*?\\end\{\2\*?\})",
    re.S)
# Lenh cach chu NGOAI cong thuc -> ki tu cach Unicode (pandoc 2.9 bo mat
# \quad o ngoai cong thuc, nen mau so lieu "$5$\quad $8$\quad $9$" bi dinh
# thanh "589" trong Word - loi co Lan bao 30/09/2026 o bai thong ke).
_CACH_CHU = (
    (re.compile(r"(?<!\\)\\qquad(?![A-Za-z])\s*"), "\u2003\u2003"),
    (re.compile(r"(?<!\\)\\quad(?![A-Za-z])\s*"), "\u2003"),
    (re.compile(r"(?<!\\)\\enspace(?![A-Za-z])\s*"), "\u2002"),
    (re.compile(r"(?<!\\)\\[;:>]\s*"), "\u2005"),
    (re.compile(r"(?<!\\)\\,\s*"), "\u2009"),
)


def _khoang_trang_ngoai_toan(t: str) -> str:
    r"""Doi \quad, \qquad, \enspace, \; \, o NGOAI cong thuc thanh khoang
    trang Unicode; ben trong cong thuc giu nguyen (pandoc doi dung sang OMML)."""
    manh = _DOAN_TOAN.split(t)
    ra = []
    # split voi 2 nhom bat: [chu, cong_thuc, ten_moi_truong, chu, cong_thuc, ...]
    for i in range(0, len(manh), 3):
        doan = manh[i]
        for mau, thay in _CACH_CHU:
            doan = mau.sub(thay, doan)
        ra.append(doan)
        if i + 1 < len(manh):
            ra.append(manh[i + 1])
    return "".join(ra)


# ----------------------------------------------------------------------
# 2. Doc tep .tex -> cau truc
# ----------------------------------------------------------------------

def _mau_phan(lang: str):
    return re.compile(r"\\noindent\\textbf\{%s ([IVX]+)\.\}\s*(.*?)\n" % _CHU[lang]["phan"])
_CAU = re.compile(r"\\begin\{ex\}.*?\\end\{ex\}", re.S)


def _doc_nhom(tex: str, lang: str = "vi") -> tuple[str, list[dict]]:
    """Tra ve (nam_hoc, [ma_de...]); moi ma de: tieu_de, lop, ma, cac_muc."""
    _PHAN = _mau_phan(lang)
    m = re.search(_CHU[lang]["nam_hoc_re"], tex)
    nam_hoc = m.group(1) if m else ""
    than = tex[tex.index(r"\begin{document}") + len(r"\begin{document}"):]
    than = than[: than.rindex(r"\end{document}")] if r"\end{document}" in than else than
    cac_khuc = re.split(r"(?=\\tieude\{)", than)
    ds = []
    for khuc in cac_khuc:
        if not khuc.strip().startswith(r"\tieude"):
            continue
        j = khuc.index("{")
        _, j = _tim_khoi_dong(khuc, j)
        tieu_de, j = _tim_khoi_dong(khuc, j)
        lop, _ = _tim_khoi_dong(khuc, j)
        mm = re.search(_CHU[lang]["ma_re"], khuc)
        muc = []
        for mt in re.finditer(r"%s|%s" % (_PHAN.pattern, _CAU.pattern), khuc, flags=re.S):
            if mt.group(0).startswith(r"\begin{ex}"):
                muc.append({"cau": mt.group(0)})
            else:
                muc.append({"phan": mt.group(1), "loi_dan": mt.group(2)})
        ds.append({"tieu_de": tieu_de, "lop": lop, "ma": mm.group(1) if mm else "", "muc": muc})
    return nam_hoc, ds


# ----------------------------------------------------------------------
# 3. Dung LaTeX chuan cho pandoc
# ----------------------------------------------------------------------

def _tieu_de_ma(ma: dict, nam_hoc: str, lang: str = "vi") -> str:
    g = DAU_GIUA
    c = _CHU[lang]
    ma_de = ("\\quad\\textbf{%s %s}" % (c["ma_de"], ma["ma"])) if ma["ma"] else ""
    return (
        "%s\\textbf{%s}\n\n"
        "%s\\textbf{%s}\n\n"
        "%s\\textbf{%s}\n\n"
        "%s%s\n\n"
        % (g, c["truong"], g, ma["tieu_de"], g, c["nam_hoc_dong"] % (nam_hoc, ma["lop"]), c["thi_sinh"], ma_de)
    )


def _cau_sang_latex(khoi: str, so: int, co_loi_giai: bool, anh: list, lang: str = "vi") -> str:
    try:
        return _cau_sang_latex_chinh(khoi, so, co_loi_giai, anh, lang)
    except Exception:
        # "bao thieu, khong lam vo de": cau nao doi loi thi van co mat trong file
        return "\\textbf{%s %d.} \\textit{%s}" % (_CHU[lang]["cau"], so, _CHU[lang]["chua_chuyen"])


def _cau_sang_latex_chinh(khoi: str, so: int, co_loi_giai: bool, anh: list, lang: str = "vi") -> str:
    ch = _CHU[lang]
    try:
        c = trich_dap_an(khoi)
    except Exception:
        c = {"loai_cau": "TL", "de_bai": khoi, "loi_giai": None}
    loai = c["loai_cau"]
    de = _lam_sach(c.get("de_bai") or "", None, anh, lang)
    # hinh cua de bai nam ngoai phan de_bai (cau Dung/Sai co \immini bao quanh)
    if c.get("hinh_tikz") and "\\includegraphics" not in de:
        cho_khac = " ".join(list((c.get("phuong_an") or {}).values())
                            + list((c.get("phat_bieu") or {}).values()))
        for h in c["hinh_tikz"]:
            if h not in cho_khac:          # hinh nam trong phuong an thi de phuong an tu ve
                de += "\n\n" + _lam_sach(h, None, anh, lang)
    ten = ch["bai"] if loai == "TL" else ch["cau"]
    ra = ["\\textbf{%s %d.} %s" % (ten, so, de)]
    if loai == "MC":
        hinh_pa = c.get("hinh_phuong_an_tikz") or {}
        for k in "ABCD":
            noi = _lam_sach(c["phuong_an"][k], None, anh, lang)
            # goi ex_test tu them "." sau moi phuong an tren PDF -> Word lam giong
            if noi and "\\includegraphics" not in noi and not noi.endswith((".", "?", "!", ":")):
                noi += "."
            if hinh_pa.get(k):
                noi += "\n\n" + _lam_sach(hinh_pa[k], None, anh, lang)
            ra.append("\\textbf{%s.} %s" % (k, noi))
    elif loai == "TF":
        hinh_y = c.get("hinh_phat_bieu_tikz") or {}
        for k in "abcd":
            noi_y = _lam_sach(c["phat_bieu"][k], None, anh, lang)
            if hinh_y.get(k):
                noi_y += "\n\n" + _lam_sach(hinh_y[k], None, anh, lang)
            dong = "\\textbf{%s)} %s" % (k, noi_y)
            if co_loi_giai:
                dong += " \\quad \\textbf{(%s)}" % (ch["dung"] if c["dap_an_dung"][k] else ch["sai"])
            ra.append(dong)
    if co_loi_giai:
        if loai == "MC":
            ra.append("\\textbf{%s %s.}" % (ch["chon_dap_an"], c["dap_an_dung"]))
        elif loai == "SA":
            ra.append("\\textbf{%s} %s" % (ch["dap_so"], _lam_sach(c["dap_an_dung"] or "", None, anh, lang)))
        if c.get("loi_giai"):
            ra.append("\\textit{%s}\n\n" % ch["loi_giai"] + _lam_sach(c["loi_giai"], None, anh, lang))
    return "\n\n".join(ra)


def dung_latex_chuan(tex: str, co_loi_giai: bool, anh: list, lang: str = "vi") -> str:
    nam_hoc, cac_ma = _doc_nhom(tex, lang)
    ch = _CHU[lang]
    if not cac_ma:
        raise WordExportError("Khong doc duoc ma de nao trong tep .tex.")
    phan_than = []
    for i, ma in enumerate(cac_ma):
        khoi = [_tieu_de_ma(ma, nam_hoc, lang)]
        so = 0
        for muc in ma["muc"]:
            if "phan" in muc:
                so = 0
                khoi.append("\\textbf{%s %s.} %s" % (ch["phan"], muc["phan"], muc["loi_dan"]))
            else:
                so += 1
                khoi.append(_MOC_CAU + "\n" + _cau_sang_latex(muc["cau"], so, co_loi_giai, anh, lang)
                            + "\n" + _MOC_CAU)
        khoi.append(DAU_GIUA + ch["het"])
        if i < len(cac_ma) - 1:
            khoi.append(DAU_NGAT_TRANG)
        phan_than.append("\n\n".join(khoi))
    return ("\\documentclass{article}\n\\usepackage{amsmath,amssymb,graphicx}\n\\begin{document}\n"
            + "\n\n".join(phan_than) + "\n\\end{document}\n")


# ----------------------------------------------------------------------
# 4. pandoc + chinh phong chu, ngat trang
# ----------------------------------------------------------------------

def _chinh_docx(duong: Path) -> None:
    """Times New Roman 12pt cho toan van ban; doi dau ngat trang thanh ngat trang that."""
    tam = duong.with_suffix(".tmp.docx")
    with zipfile.ZipFile(duong) as vao, zipfile.ZipFile(tam, "w", zipfile.ZIP_DEFLATED) as ra:
        for muc in vao.infolist():
            du_lieu = vao.read(muc.filename)
            if muc.filename == "word/styles.xml":
                x = du_lieu.decode("utf-8")
                phong = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
                         'w:eastAsia="Times New Roman" w:cs="Times New Roman" />')
                x = re.sub(r"<w:rFonts [^>]*/>", phong, x)
                x = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="24" />', x, count=1)
                du_lieu = x.encode("utf-8")
            elif muc.filename == "word/document.xml":
                x = du_lieu.decode("utf-8")
                x = re.sub(r"<w:p>(?:(?!</w:p>).)*?%s(?:(?!</w:p>).)*?</w:p>" % DAU_NGAT_TRANG,
                           '<w:p><w:r><w:br w:type="page" /></w:r></w:p>', x, flags=re.S)

                def giua(m):
                    doan = m.group(0).replace(DAU_GIUA, "")
                    if "<w:pPr>" in doan:
                        return doan.replace("<w:pPr>", '<w:pPr><w:jc w:val="center" />', 1)
                    return re.sub(r"^<w:p>", '<w:p><w:pPr><w:jc w:val="center" /></w:pPr>', doan)
                x = re.sub(r"<w:p>(?:(?!</w:p>).)*?%s(?:(?!</w:p>).)*?</w:p>" % DAU_GIUA, giua, x, flags=re.S)
                du_lieu = x.encode("utf-8")
            ra.writestr(muc, du_lieu)
    tam.replace(duong)


def _pandoc_doc_duoc(doan: str, tm: str) -> bool:
    """pandoc co doc duoc mot doan LaTeX nay khong (dung de tim cau hong)."""
    vao = Path(tm) / "thu.tex"
    vao.write_text("\\begin{document}\n%s\n\\end{document}\n" % doan, encoding="utf-8")
    chay = subprocess.run(["pandoc", "-f", "latex", "-t", "native", str(vao)],
                          capture_output=True, text=True, timeout=60, cwd=tm)
    return chay.returncode == 0


def xuat_word(tex_path: Path, co_loi_giai: bool, ten_ra: str, lang: str = "vi") -> Path:
    """Doi tep .tex da luu cua de thanh .docx. Tra ve duong dan file Word."""
    if not shutil.which("pandoc"):
        raise WordExportError(
            "May chu chua cai pandoc (cong cu doi sang Word). Cai bang: "
            "sudo apt install pandoc")
    tex = Path(tex_path).read_text(encoding="utf-8")
    anh: list = []
    chuan = dung_latex_chuan(tex, co_loi_giai, anh, lang)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ra = EXPORTS_DIR / ("%s.docx" % ten_ra)
    with tempfile.TemporaryDirectory() as tm:
        vao = Path(tm) / "de.tex"

        def chay_pandoc(van):
            vao.write_text(van, encoding="utf-8")
            return subprocess.run(["pandoc", "-f", "latex", "-t", "docx", str(vao), "-o", str(ra)],
                                  capture_output=True, text=True, timeout=180, cwd=tm)
        chay = chay_pandoc(chuan)
        if chay.returncode != 0:
            # Mot cau loi LaTeX (vd thieu dau $) lam pandoc bo ca de. Tim tung
            # cau hong, thay bang dong bao "xem ban PDF" roi dich lai.
            manh = chuan.split(_MOC_CAU)
            for k in range(1, len(manh), 2):          # manh le = mot cau hoi
                if not _pandoc_doc_duoc(manh[k], tm):
                    so = re.search(_CHU[lang]["loi_re"], manh[k])
                    manh[k] = ("\n\\textbf{%s %s.} \\textit{%s}\n" % (so.group(1), so.group(2), _CHU[lang]["chua_chuyen"])
                               if so else "\n")
            chay = chay_pandoc("".join(manh))
        if chay.returncode != 0 or not ra.exists():
            raise WordExportError("pandoc loi: %s" % (chay.stderr[-1500:] or "khong ro"))
    _chinh_docx(ra)
    return ra
