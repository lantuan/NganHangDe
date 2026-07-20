import random

from app.services.mapping_service import load_mapping


class SelectorError(Exception):
    pass


def select_questions(lop: int, yeu_cau: list[dict]) -> list[dict]:
    """
    yeu_cau: [{"chuong_so": 1, "muc_do": "NB", "so_luong": 3}, ...]
    Trả về danh sách Generator ID đã chọn, kèm nguồn (chuong_so, muc_do).
    """
    # Cache mapping theo chương để tránh đọc file lặp lại
    cache: dict[int, list[dict]] = {}
    ket_qua = []

    for yc in yeu_cau:
        chuong_so = yc["chuong_so"]
        muc_do = yc["muc_do"]
        so_luong = yc["so_luong"]

        if chuong_so not in cache:
            cache[chuong_so] = load_mapping(lop, chuong_so)

        candidates = [
            item for item in cache[chuong_so]
            if item["muc_do"] == muc_do
        ]

        if len(candidates) < so_luong:
            raise SelectorError(
                f"Chương {chuong_so}, mức độ {muc_do}: chỉ có {len(candidates)} "
                f"câu trong Mapping, không đủ {so_luong} câu yêu cầu."
            )

        chosen = random.sample(candidates, so_luong)
        for item in chosen:
            ket_qua.append({
                "generator_id": item["id"],
                "chuong_so": chuong_so,
                "muc_do": muc_do,
                "loai": item.get("Loai"),
                "dang": item.get("Dang"),
            })

    return ket_qua