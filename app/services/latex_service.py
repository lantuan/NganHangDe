from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_FILE = BASE_DIR / "data" / "config" / "latex_template.tex"
TEMP_DIR = BASE_DIR / "data" / "temp"


def build_latex_document(tieu_de: str, noi_dung: str) -> str:
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    return template.replace("__TIEU_DE__", tieu_de).replace("__NOI_DUNG__", noi_dung)


def save_tex_file(content: str, filename: str) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = TEMP_DIR / f"{filename}.tex"
    tex_path.write_text(content, encoding="utf-8")
    return tex_path