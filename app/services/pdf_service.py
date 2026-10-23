import os
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "data" / "exports"
EXPORTS_DIR_EN = BASE_DIR / "data" / "exports_en"   # PDF của đề tiếng Anh
CONFIG_DIR = BASE_DIR / "data" / "config"
HINH_ANH_DIR = BASE_DIR / "data" / "hinh_anh"   # ảnh chụp làm nền cho hình TikZ (data/python_bank/hinh_anh.py)


class PdfCompileError(Exception):
    pass


# ======================================================
# HANG CHO BIEN DICH (co Lan 23/10/2026: "36 may vao mot luc, web khong the tao de dong loat")
# Moi lan dich LaTeX an tron mot nhan CPU trong nhieu giay. VPS 2 nhan ma 36 em cung bam tao de thi 36 tien
# trinh pdflatex/xelatex tranh nhau 2 nhan: ban nao cung cham gap ~18 lan, vuot gioi han 60 giay -> bi cat,
# ca lop deu bao loi. Nay XEP HANG: moi luc chi dich toi da SO_BIEN_DICH_CUNG_LUC ban (mac dinh = so nhan CPU),
# ban khac cho den luot - cham hon chut nhung ban nao cung xong. Dung chung cho PDF de/loi giai va anh hinh ve.
# ======================================================
try:
    SO_BIEN_DICH_CUNG_LUC = max(1, int(os.environ.get("SO_BIEN_DICH_CUNG_LUC") or (os.cpu_count() or 1)))
except ValueError:
    SO_BIEN_DICH_CUNG_LUC = max(1, os.cpu_count() or 1)
_HANG_BIEN_DICH = threading.BoundedSemaphore(SO_BIEN_DICH_CUNG_LUC)


@contextmanager
def luot_bien_dich():
    """Giu mot cho trong hang bien dich LaTeX trong khoi with."""
    with _HANG_BIEN_DICH:
        yield


def _texinputs_env() -> dict:
    """
    Them data/config (noi chua ex_test.sty, latex_template.tex) vao duong
    tim kiem cua pdflatex, de khong phu thuoc thu muc lam viec hien tai
    (working directory) luc goi subprocess.
    Them ca data/hinh_anh (21/10/2026): lenh includegraphics{ten.jpg} trong hinh TikZ
    cua cau co anh chup (bản đồ, sơ đồ) tim thay anh o day.
    """
    env = os.environ.copy()
    sep = ":" if os.name != "nt" else ";"
    env["TEXINPUTS"] = f"{CONFIG_DIR}{os.sep}{sep}{HINH_ANH_DIR}{os.sep}{sep}{env.get('TEXINPUTS', '')}"
    return env


def compile_pdf(tex_path: Path, lang: str = "vi") -> Path:
    """
    Bien dich file .tex thanh .pdf bang pdflatex.
    Chay 2 lan de muc luc/tham chieu (neu co) duoc cap nhat du.
    """
    exports_dir = EXPORTS_DIR_EN if lang == "en" else EXPORTS_DIR
    exports_dir.mkdir(parents=True, exist_ok=True)
    env = _texinputs_env()

    result = None
    with luot_bien_dich():
        result = _chay_hai_lan(tex_path, exports_dir, env)

    pdf_path = exports_dir / f"{tex_path.stem}.pdf"

    if not pdf_path.exists():
        log = result.stdout[-3000:] if result else "(khong chay duoc pdflatex)"
        raise PdfCompileError(
            f"Bien dich PDF that bai.\n--- LOG PDFLATEX ---\n{log}"
        )

    return pdf_path


def _chay_hai_lan(tex_path: Path, exports_dir: Path, env: dict):
    result = None
    for _ in range(2):
        try:
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory", str(exports_dir),
                    str(tex_path),
                ],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
                env=env,
            )
        except FileNotFoundError:
            raise PdfCompileError(
                "Khong tim thay chuong trinh 'pdflatex'. Kiem tra: (1) da cai "
                "LaTeX chua (sudo apt install texlive-latex-base texlive-latex-extra); "
                "(2) PATH trong systemd service co tro dung thu muc cai pdflatex khong."
            )
        except subprocess.TimeoutExpired:
            raise PdfCompileError(
                "Bien dich PDF qua thoi gian cho phep (60s) - co the do LaTeX "
                "bi treo (thieu package, loi cu phap gay vong lap...)."
            )
    return result
