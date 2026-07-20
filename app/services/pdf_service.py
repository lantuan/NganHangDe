import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "data" / "exports"


class PdfCompileError(Exception):
    pass


def compile_pdf(tex_path: Path) -> Path:
    """
    Biên dịch file .tex thành .pdf bằng pdflatex.
    Chạy 2 lần để mục lục/tham chiếu (nếu có) được cập nhật đủ.
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
            text=True,
            timeout=60,
        )

    pdf_path = EXPORTS_DIR / f"{tex_path.stem}.pdf"

    if not pdf_path.exists():
        raise PdfCompileError(
            f"Biên dịch PDF thất bại.\n--- LOG PDFLATEX ---\n{result.stdout[-3000:]}"
        )

    return pdf_path