from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PPCT_DIR = BASE_DIR / "data" / "ppct"


def _load_ppct(lop: int):
    file = PPCT_DIR / f"toan{lop}.json"
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_exam_scope(lop: int, ki_thi: str, pham_vi_chuong: str | None = None):
    """
    lop: 10, 11, 12
    ki_thi: "giua_ky_1" | "cuoi_ky_1" | "giua_ky_2" | "cuoi_ky_2" | "on_tap"
    pham_vi_chuong: vd "chuong_1" (chỉ dùng khi ki_thi = on_tap kiểu HeSo1)
    """
    ppct = _load_ppct(lop)

    boundary_map = {
        "giua_ky_1": "GK1_EXAM",
        "cuoi_ky_1": "CK1_EXAM",
        "giua_ky_2": "GK2_EXAM",
        "cuoi_ky_2": "CK2_EXAM",
    }

    # Trường hợp: chỉ lấy 1 chương cụ thể
    if pham_vi_chuong:
        so_chuong = int(pham_vi_chuong.replace("chuong_", ""))
        bai_list = [b for b in ppct if b["chuong_so"] == so_chuong]
        return {
            "pham_vi_chuong": [so_chuong],
            "pham_vi_bai": [b["id"] for b in bai_list],
        }

    # Trường hợp: ôn tập toàn bộ học kỳ
    if ki_thi == "on_tap":
        hoc_ky = 1  # có thể mở rộng sau
        bai_list = [b for b in ppct if b["hoc_ky"] == hoc_ky]
        return {
            "pham_vi_chuong": sorted({b["chuong_so"] for b in bai_list}),
            "pham_vi_bai": [b["id"] for b in bai_list],
        }

    # Trường hợp: thi giữa kỳ / cuối kỳ -> lấy từ đầu đến bài có boundary_after tương ứng
    boundary = boundary_map.get(ki_thi)
    if not boundary:
        return {"error": "PPCT_NOT_FOUND"}

    bai_list = []
    for b in ppct:
        bai_list.append(b)
        if b.get("boundary_after") == boundary:
            break
    else:
        return {"error": "PPCT_NOT_FOUND"}

    return {
        "pham_vi_chuong": sorted({b["chuong_so"] for b in bai_list}),
        "pham_vi_bai": [b["id"] for b in bai_list],
    }