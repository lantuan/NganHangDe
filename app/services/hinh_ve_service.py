r"""
Dich hinh ve TikZ trong de bai thanh anh de HIEN DUOC TREN WEB.

Vi sao can: cau co hinh ve khong the bo hinh di. Bo hinh la doi luon MUC
DO cua cau - vi du bai ham so bac hai, nhin do thi doc ra dinh va truc doi
xung la mot chuyen, khong co do thi lai la chuyen khac han. Truoc day web
danh dau co_hinh_ve roi bao hoc sinh "xem trong PDF", tuc la cau do bien
mat khoi phan lam bai truc tiep.

Cach lam: lay doan \begin{tikzpicture}...\end{tikzpicture} trong de bai,
ghep vao DUNG phan dau (preamble) cua khung de - data/config/latex_template.tex,
phan tu dau tep den truoc \begin{document} - roi dich ra anh. Dung chung
preamble nen hinh tren web giong het hinh trong PDF.

Anh duoc luu theo MA BAM (sha1) cua chinh doan TikZ: hai cau cung hinh thi
chi dich mot lan; de ra lai lan sau van dung lai anh cu.
"""

import hashlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE = BASE_DIR / "data" / "config" / "latex_template.tex"
KHO_ANH = BASE_DIR / "data" / "hinh_cache"

# Thu lan luot cac cong cu doi PDF -> anh. SVG dat truoc vi net o moi co
# chu; khong co SVG thi lui ve PNG.
BO_DOI = [
    ("svg", lambda pdf, ra: ["pdftocairo", "-svg", str(pdf), str(ra)]),
    ("svg", lambda pdf, ra: ["pdf2svg", str(pdf), str(ra)]),
    ("svg", lambda pdf, ra: ["dvisvgm", "--pdf", "--no-fonts", "-o", str(ra), str(pdf)]),
    ("png", lambda pdf, ra: ["pdftoppm", "-png", "-r", "160", "-singlefile",
                             str(pdf), str(ra.with_suffix(""))]),
]


class HinhVeError(Exception):
    """Khong dich duoc hinh - de bai van dung duoc, chi la khong co anh."""


def tim_tikz(latex_block: str) -> list[str]:
    r"""Lay moi doan \begin{tikzpicture}...\end{tikzpicture} trong mot khoi."""
    return re.findall(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                      latex_block, flags=re.S)


# Doi so nay khi cach dung hinh thay doi, de anh cu bi dich lai.
# v2 (29/09/2026): them goi icomma nen dau phay thap phan doi cach
# hien thi -> phai doi phien ban de moi hinh cu deu duoc dich lai.
PHIEN_BAN = "v2"

# Phan dau RUT GON: chi nhung goi ma hinh ve thuc su can. Dung khi may
# khong co du goi cua khung de day du (may ao cua Claude thieu tabvar,
# bclogo, esvect; VPS thi co du).
PREAMBLE_GON = r"""\documentclass[12pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{tkz-euclide,tkz-tab,tikz,tikz-3dplot}
\usepackage{pgfplots}
\usepgfplotslibrary{fillbetween}
\usetikzlibrary{shapes.geometric,arrows,snakes,calc,intersections,angles,patterns}
\pgfplotsset{compat=1.9}
% Dau phay thap phan kieu Viet Nam, giong het trong latex_template.tex:
% $0,7$ phai in ra "0,7" chu khong phai "0, 7".
\IfFileExists{icomma.sty}{\usepackage{icomma}}{}
"""


def _preamble_day() -> str:
    r"""Phan dau cua CHINH khung de, den truoc \begin{document}.

    Dung cai nay truoc de hinh tren web giong het hinh trong PDF: cung
    goi, cung lenh tu che, cung co chu.

    NHUNG phai doi hai thu, neu khong anh se hong:
      - \documentclass{book} -> standalone[preview]: khung de la sach kho
        A4, dich mot hinh ra se duoc ca trang giay voi hinh be ti o goc.
        standalone cat sat vien hinh, khong phu thuoc pdfcrop co hay khong.
      - bo goi geometry: no dat le trang, vo nghia voi mot hinh roi va con
        keo hinh lech di.
    """
    van = TEMPLATE.read_text(encoding="utf-8")
    van = van[:van.index(r"\begin{document}")]
    van = van.replace("__EX_TEST_OPTION__", "dethi")
    van = re.sub(r"\\documentclass(\[[^\]]*\])?\{[^}]*\}",
                 r"\\documentclass[preview,border=4pt]{standalone}", van, count=1)
    van = re.sub(r"\\usepackage(\[[^\]]*\])?\{geometry\}\s*", "", van)
    return van


def ma_hinh(tikz: str) -> str:
    """Ma bam cua mot hinh, tinh tu chinh doan TikZ."""
    return hashlib.sha1((PHIEN_BAN + "\n" + tikz).encode("utf-8")).hexdigest()[:20]


def duong_dan_anh(ma: str) -> Path | None:
    """Duong dan anh da dich san, hoac None neu chua co."""
    for duoi in ("svg", "png"):
        p = KHO_ANH / ("%s.%s" % (ma, duoi))
        if p.exists() and p.stat().st_size > 0:
            return p
    return None


def dich_hinh(tikz: str, chi_png: bool = False) -> Path:
    """Dich mot doan TikZ ra anh, tra ve duong dan. Co san thi dung lai.

    chi_png=True: bat buoc ra PNG (dung cho file Word - Word cu khong doc
    duoc SVG). Anh PNG luu rieng voi duoi .png nen khong dung cham anh
    SVG cua web.
    """
    ma = ma_hinh(tikz)
    if chi_png:
        p = KHO_ANH / ("%s.png" % ma)
        if p.exists() and p.stat().st_size > 0:
            return p
    else:
        da_co = duong_dan_anh(ma)
        if da_co:
            return da_co

    KHO_ANH.mkdir(parents=True, exist_ok=True)
    import os
    # ex_test.sty nam trong repo chu khong nam trong TeX Live; noi them vao
    # TEXINPUTS san co (neu may da dat) chu khong de len no.
    moi_truong = dict(os.environ,
                      TEXINPUTS="%s:%s" % (BASE_DIR / "data" / "config",
                                           os.environ.get("TEXINPUTS", "")))
    with tempfile.TemporaryDirectory() as thu_muc:
        tm = Path(thu_muc)
        pdf = None
        loi_dau = ""
        # Thu phan dau DAY DU truoc (hinh giong het trong PDF); may nao
        # thieu goi thi lui ve phan dau RUT GON.
        for dau in (_preamble_day(), PREAMBLE_GON):
            (tm / "hinh.tex").write_text(
                dau + "\n\\pagestyle{empty}\n\\begin{document}\n"
                + tikz + "\n\\end{document}\n", encoding="utf-8")
            for cu in tm.glob("hinh.pdf"):
                cu.unlink()
            chay = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "hinh.tex"],
                cwd=tm, capture_output=True, text=True, timeout=120, env=moi_truong)
            if (tm / "hinh.pdf").exists():
                pdf = tm / "hinh.pdf"
                break
            if not loi_dau:
                dong = [d for d in chay.stdout.splitlines() if d.startswith("!")]
                loi_dau = dong[0] if dong else "khong ro"
        if pdf is None:
            raise HinhVeError("xelatex khong dich duoc hinh: %s" % loi_dau)
        # cat trang cho vua hinh
        if shutil.which("pdfcrop"):
            subprocess.run(["pdfcrop", "hinh.pdf", "hinh-cat.pdf"],
                           cwd=tm, capture_output=True, timeout=60)
            if (tm / "hinh-cat.pdf").exists():
                pdf = tm / "hinh-cat.pdf"

        # Dich ra moi dinh dang lam duoc roi GIU CAI NHE NHAT. Hinh nhieu
        # duong cong (vi du con song ve bang plot[smooth]) cho ra SVG toi
        # vai megabyte - nang hon anh PNG rat nhieu, ma trang lam bai cua
        # hoc sinh thuong mo bang 3G tren dien thoai.
        ung_vien = []
        for duoi, lenh in BO_DOI:
            if chi_png and duoi != "png":
                continue
            if not shutil.which(lenh(pdf, tm / "x")[0]):
                continue
            ra = tm / ("ket_qua_%d.%s" % (len(ung_vien), duoi))
            subprocess.run(lenh(pdf, ra), cwd=tm, capture_output=True, timeout=60)
            # pdftoppm tu them duoi .png vao ten da bo duoi
            if not ra.exists():
                thay = tm / (ra.with_suffix("").name + ".png")
                if thay.exists():
                    ra = thay
            if ra.exists() and ra.stat().st_size > 0:
                ung_vien.append((ra.stat().st_size, ra))
        if ung_vien:
            _, ra = min(ung_vien)
            dich = KHO_ANH / ("%s%s" % (ma, ra.suffix))
            shutil.copyfile(ra, dich)
            return dich
        raise HinhVeError(
            "Khong co cong cu doi PDF sang anh. Can mot trong: "
            "pdftocairo (goi poppler-utils), pdf2svg, dvisvgm.")


def dich_hinh_trong_khoi(latex_block: str) -> list[str]:
    """Dich moi hinh trong mot khoi cau hoi, tra ve danh sach MA hinh.

    Khong nem loi ra ngoai: hinh hong thi cau hoi van phai ra duoc de,
    chi la thieu anh - dung nguyen tac "bao thieu, khong lam vo de".
    """
    ra = []
    for tikz in tim_tikz(latex_block):
        try:
            dich_hinh(tikz)
            ra.append(ma_hinh(tikz))
        except Exception:
            continue
    return ra
