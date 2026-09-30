from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MAPPING_DIR = BASE_DIR / "data" / "mapping"

MUCDO_PATTERN = re.compile(r"_(NB|TH|VD|VDC)\d")


def _extract_muc_do(generator_id: str) -> str | None:
    """
    Suy ra mức độ từ Generator ID.
    VD: L10_C1_B1_NB001_MC_A -> "NB"
    Trường hợp đặc biệt (VD: L10_C1_TF_A) -> None (không gắn mức độ cụ thể)
    """
    match = MUCDO_PATTERN.search(generator_id)
    return match.group(1) if match else None


# Ngoai le 3 (doc 04): cau TU LUAN hai y thuoc HAI don vi kien thuc cua cung mot
# chuong. ID ghi ca hai don vi theo thu tu y a) -> y b), khong ghi bai (nhu TF):
#     L10_C3_TH031_TH032_TL_A   (y a: TH031 o Bai 5, y b: TH032 o Bai 6)
# Ma tran tinh theo TUNG Y: moi y la mot "suat" o dung muc do + don vi cua no.
TL_NHIEU_Y_PATTERN = re.compile(
    r"^L(\d+)_C(\d+)_((?:NB|TH|VD|VDC)\d+(?:_(?:NB|TH|VD|VDC)\d+)+)_TL_[A-Z]+(?:_\d{2})?$")
_MOT_Y = re.compile(r"(NB|TH|VD|VDC)(\d+)")


def cac_y_tu_luan(generator_id: str | None) -> list[tuple[str, str]] | None:
    """Cau tu luan nhieu y -> [(muc_do, so don vi), ...] theo thu tu y; cau khac -> None.
    VD: L10_C3_TH031_TH032_TL_A -> [("TH", "031"), ("TH", "032")]."""
    m = TL_NHIEU_Y_PATTERN.match(generator_id or "")
    if not m:
        return None
    return _MOT_Y.findall(m.group(3))


def so_suat_tu_luan(generator_id: str | None) -> int:
    """So suat (y) mot cau tu luan chiem trong ma tran / thang diem: cau nhieu
    don vi = so don vi, cau thuong = 1."""
    y = cac_y_tu_luan(generator_id)
    return len(y) if y else 1


def load_mapping(lop: int, chuong_so: int) -> list[dict]:
    file = MAPPING_DIR / f"toan{lop}" / f"L{lop}_C{chuong_so}.json"
    if not file.exists():
        raise FileNotFoundError(f"Không tìm thấy mapping: {file}")

    with open(file, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        item["muc_do"] = _extract_muc_do(item["id"])
        item["chuong_so"] = chuong_so

    return items

PYTHON_BANK_DIR = BASE_DIR / "data" / "python_bank"


def dem_dang_co_ham(lop: int, chuong_so: int) -> int:
    """
    Dem so dang cau hoi trong Mapping ma THUC SU da co ham sinh trong
    ngan hang Python.

    Vi sao can: Mapping la BAN KE HOACH -- liet ke cac dang cau hoi can co
    cho tung yeu cau can dat, ke ca dang chua viet ham. Ham Python moi la
    HANG CO THAT. Neu lay so dong Mapping de bao "chuong nay da san sang"
    thi web se moi hoc sinh vao mot chuong chua co cau hoi nao, va vi ra de
    that chay voi cho_phep_thieu=False nen se VO CA DE.

    Doc thang tep .py bang van ban, khong import module: nhanh, va khong
    keo theo sympy/numpy chi de dem.
    """
    file_py = PYTHON_BANK_DIR / f"toan{lop}" / f"L{lop}_C{chuong_so}.py"
    if not file_py.exists():
        return 0
    try:
        src = file_py.read_text(encoding="utf-8")
    except OSError:
        return 0

    co_ham = set(re.findall(r"^def (L\d+_[A-Za-z0-9_]+?)_\d{2}\s*\(", src, re.M))
    if not co_ham:
        return 0

    try:
        items = load_mapping(lop, chuong_so)
    except (FileNotFoundError, ValueError):
        return 0
    return sum(1 for it in items if it.get("id") in co_ham)


def phan_loai_cau(item: dict) -> str:
    """
    Phân loại theo trường 'Loai' trong Mapping.
    """
    loai_text = item.get("Loai", "") or ""
    if "Đúng sai" in loai_text:
        return "dung_sai_cau_lon"
    if "Tự luận" in loai_text:
        return "tu_luan"
    if "ngắn" in loai_text:
        return "tra_loi_ngan"
    return "trac_nghiem"

CHUONG_BAI_PATTERN = re.compile(r"^L\d+_C(\d+)(?:_B(\d+))?")


def trich_chuong_bai(generator_id: str | None) -> tuple[str | None, str | None]:
    """
    Suy ra (chuong, bai) tu Generator ID, dung cho Grade Result (doc 03).
    VD: L10_C1_B2_NB017_MC_A -> ("1", "2")
        L10_C1_TF_A          -> ("1", None)  (TF ra theo chuong, khong co bai)
    Tra ve (None, None) neu khong khop dinh dang ID chuan.
    """
    if not generator_id:
        return None, None
    match = CHUONG_BAI_PATTERN.match(generator_id)
    if not match:
        return None, None
    return match.group(1), match.group(2)
