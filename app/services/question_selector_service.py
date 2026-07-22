import random

from app.services.mapping_service import load_mapping, phan_loai_cau


class SelectorError(Exception):
    pass


def _chon_uu_tien_khong_trung(candidates: list[dict], so_luong: int) -> list[dict]:
    """
    Cấp 1: nếu đủ ID khác nhau, chọn không trùng.
    Nếu KHÔNG đủ: dùng hết toàn bộ ID có sẵn (mỗi ID 1 lần) trước,
    sau đó mới lặp lại ngẫu nhiên cho đủ số lượng còn thiếu.
    (Việc chọn khác/trùng BIẾN THỂ Python của cùng 1 ID xử lý ở generator_service,
    không xử lý ở đây.)
    """
    if not candidates:
        return []

    if len(candidates) >= so_luong:
        return random.sample(candidates, so_luong)

    da_dung_het = candidates[:]
    random.shuffle(da_dung_het)
    con_thieu = so_luong - len(da_dung_het)
    for _ in range(con_thieu):
        da_dung_het.append(random.choice(candidates))
    return da_dung_het


def select_questions(lop: int, yeu_cau: list[dict]) -> list[dict]:
    """
    yeu_cau: list các mục, mỗi mục có dạng:
        {"chuong_so": 1, "loai_cau": "trac_nghiem", "muc_do": "NB", "so_luong": 3}
        {"chuong_so": 1, "loai_cau": "dung_sai_cau_lon", "so_luong": 1}
    """
    cache: dict[int, list[dict]] = {}
    ket_qua = []

    for yc in yeu_cau:
        chuong_so = yc["chuong_so"]
        loai_cau = yc["loai_cau"]
        muc_do = yc.get("muc_do")
        so_luong = yc["so_luong"]

        if so_luong <= 0:
            continue

        if chuong_so not in cache:
            cache[chuong_so] = load_mapping(lop, chuong_so)

        candidates = [
            item for item in cache[chuong_so]
            if phan_loai_cau(item) == loai_cau
            and (loai_cau == "dung_sai_cau_lon" or item["muc_do"] == muc_do)
        ]

        if not candidates:
            raise SelectorError(
                f"Chương {chuong_so}, loại '{loai_cau}'"
                + (f" mức {muc_do}" if muc_do else "")
                + f": không có câu nào trong Mapping (0 câu, không thể chọn)."
            )

        chosen = _chon_uu_tien_khong_trung(candidates, so_luong)
        for item in chosen:
            ket_qua.append({
                "generator_id": item["id"],
                "chuong_so": chuong_so,
                "loai_cau": loai_cau,
                "muc_do": muc_do,
                "loai": item.get("Loai"),
                "dang": item.get("Dang"),
            })

    return ket_qua