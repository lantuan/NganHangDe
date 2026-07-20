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