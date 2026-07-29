import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "data" / "exports"


class PdfCompileError(Exception):
    pass


def compile_pdf(tex_path: Path) -> Path:
    """
    Bien dich file .tex thanh .pdf bang pdflatex.
    Chay 2 lan de muc luc/tham chieu (neu co) duoc cap nhat du.
    """
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    for _ in range(2):
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
        )

    pdf_path = EXPORTS_DIR / f"{tex_path.stem}.pdf"

    if not pdf_path.exists():
        raise PdfCompileError(
            f"Bien dich PDF that bai.\n--- LOG PDFLATEX ---\n{result.stdout[-3000:]}"
        )

    return pdf_path
