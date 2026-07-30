import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "data" / "exports"
CONFIG_DIR = BASE_DIR / "data" / "config"


class PdfCompileError(Exception):
    pass


def _texinputs_env() -> dict:
    """
    Them data/config (noi chua ex_test.sty, latex_template.tex) vao duong
    tim kiem cua pdflatex, de khong phu thuoc thu muc lam viec hien tai
    (working directory) luc goi subprocess.
    """
    env = os.environ.copy()
    sep = ":" if os.name != "nt" else ";"
    env["TEXINPUTS"] = f"{CONFIG_DIR}{os.sep}{sep}{env.get('TEXINPUTS', '')}"
    return env


def compile_pdf(tex_path: Path) -> Path:
    """
    Bien dich file .tex thanh .pdf bang pdflatex.
    Chay 2 lan de muc luc/tham chieu (neu co) duoc cap nhat du.
    """
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    env = _texinputs_env()

    result = None
    for _ in range(2):
        try:
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory", str(EXPORTS_DIR),
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

    pdf_path = EXPORTS_DIR / f"{tex_path.stem}.pdf"

    if not pdf_path.exists():
        log = result.stdout[-3000:] if result else "(khong chay duoc pdflatex)"
        raise PdfCompileError(
            f"Bien dich PDF that bai.\n--- LOG PDFLATEX ---\n{log}"
        )

    return pdf_path
