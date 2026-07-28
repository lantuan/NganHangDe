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
    Thêm data/config (nơi chứa ex_test.sty, latex_template.tex) vào đường
    tìm kiếm của pdflatex, để không phụ thuộc thư mục làm việc hiện tại
    (working directory) lúc gọi subprocess. "//" ở cuối = tìm cả thư mục con.
    """
    env = os.environ.copy()
    sep = ":" if os.name != "nt" else ";"
    env["TEXINPUTS"] = f"{CONFIG_DIR}{os.sep}{sep}{env.get('TEXINPUTS', '')}"
    return env


def compile_pdf(tex_path: Path) -> Path:
    """
    Biên dịch file .tex thành .pdf bằng pdflatex.
    Chạy 2 lần để mục lục/tham chiếu (nếu có) được cập nhật đủ.
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
                text=True,
                timeout=60,
                env=env,
            )
        except FileNotFoundError:
            # Máy chủ chưa cài pdflatex (chương trình LaTeX), hoặc systemd
            # service không thấy được PATH có pdflatex (xem doc 14, kiểm tra
            # Environment="PATH=..." trong file .service).
            raise PdfCompileError(
                "Không tìm thấy chương trình 'pdflatex'. Kiểm tra: (1) đã cài "
                "LaTeX chưa (sudo apt install texlive-latex-base texlive-latex-extra); "
                "(2) PATH trong systemd service có trỏ đúng thư mục cài pdflatex không."
            )
        except subprocess.TimeoutExpired:
            raise PdfCompileError(
                "Biên dịch PDF quá thời gian cho phép (60s) — có thể do LaTeX "
                "bị treo (thiếu package, lỗi cú pháp gây vòng lặp...)."
            )

    pdf_path = EXPORTS_DIR / f"{tex_path.stem}.pdf"

    if not pdf_path.exists():
        log = result.stdout[-3000:] if result else "(không chạy được pdflatex)"
        raise PdfCompileError(
            f"Biên dịch PDF thất bại.\n--- LOG PDFLATEX ---\n{log}"
        )

    return pdf_path
