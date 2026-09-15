from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_FILE = BASE_DIR / "data" / "config" / "latex_template.tex"
TEMP_DIR = BASE_DIR / "data" / "temp"


def tinh_nam_hoc() -> str:
    """
    Nam hoc theo thoi diem hien tai:
    Thang 1-6  -> nam truoc - nam nay   (vd 2026 -> "2025-2026")
    Thang 7-12 -> nam nay - nam sau     (vd 2026 -> "2026-2027")
    """
    now = datetime.now()
    if 1 <= now.month <= 6:
        return f"{now.year - 1}-{now.year}"
    return f"{now.year}-{now.year + 1}"


def tinh_ma_de(lop: int, so_thu_tu: int = 1) -> str:
    """Ma de = lop*100 + so thu tu. Vi du lop 10 -> 1001, 1002..."""
    return str(lop * 100 + so_thu_tu)


def build_latex_document(
    tieu_de: str,
    noi_dung: str,
    *,
    lop: int,
    role: str,
    ex_test_option: str = "dethi",
    ma_de: str | None = None,
) -> str:
    """
    Ghep noi dung da dung san (co the gom NHIEU ma de) vao khung tai lieu.

    SUA 2026-09-15: phan tieu de / ho ten - ma de / chan trang / het de da
    chuyen sang exam_assembler_service.py, vi mot tep .tex nay co the chua
    nhieu ma de, moi ma de can mot bo day du rieng. Ham nay gio chi con
    thay cac bien o PHAN DAU tai lieu (goi ex_test, nam hoc).

    Cac tham so tieu_de / lop / role / ma_de giu lai cho tuong thich nguoc
    (khong con dung den o day) - noi dung da duoc dung san o tang tren.
    """
    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    return (
        template
        .replace("__EX_TEST_OPTION__", ex_test_option)
        .replace("__NAM_HOC__", tinh_nam_hoc())
        .replace("__NOI_DUNG__", noi_dung)
    )


def save_tex_file(content: str, filename: str) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = TEMP_DIR / f"{filename}.tex"
    tex_path.write_text(content, encoding="utf-8")
    return tex_path
