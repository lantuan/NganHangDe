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
    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    if ma_de is None:
        ma_de = tinh_ma_de(lop)

    if role == "teacher":
        khoi_ho_ten_ma_de = (
            "\\noindent\n"
            "\\begin{minipage}[b]{8.5cm}\n"
            "\\fontsize{11}{0}\\selectfont Họ tên thí sinh:....................................... "
            "Lớp:.......... Phòng kiểm tra:...........\n"
            "\\end{minipage}\\hspace{1.5cm}\n"
            "\\begin{minipage}[b]{4cm}\n"
            f"\\hfill\\fbox{{\\bf Mã đề {ma_de}}}\n"
            "\\end{minipage}\\vspace{4pt}\n"
        )
        chan_trang_ma_de = f" $-$ Mã đề {ma_de}"
    else:
        khoi_ho_ten_ma_de = ""
        chan_trang_ma_de = ""

    return (
        template
        .replace("__EX_TEST_OPTION__", ex_test_option)
        .replace("__NAM_HOC__", tinh_nam_hoc())
        .replace("__TIEU_DE__", tieu_de)
        .replace("__LOP__", str(lop))
        .replace("__KHOI_HO_TEN_MA_DE__", khoi_ho_ten_ma_de)
        .replace("__CHAN_TRANG_MA_DE__", chan_trang_ma_de)
        .replace("__NOI_DUNG__", noi_dung)
    )


def save_tex_file(content: str, filename: str) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = TEMP_DIR / f"{filename}.tex"
    tex_path.write_text(content, encoding="utf-8")
    return tex_path
