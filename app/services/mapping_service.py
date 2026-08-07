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
