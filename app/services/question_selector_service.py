"""
CN_QuestionSelector

Chọn Generator ID cuối cùng, dựa trên Blueprint (đã có curriculum_id cho
MC/SA/TL, chuong_so cho TF) + Mapping. Đây là node DUY NHẤT chọn Generator
ID cuối cùng — không có AI nào tham gia bước này (doc 08_CODE_NODES.md).

File này có 2 chế độ:

1. select_questions(lop, blueprint)
   Chế độ CHÍNH THỨC, dùng trong WF001 (build_and_select). Khớp Mapping
   theo đúng curriculum_id do CN_BuildBlueprint chọn.

2. select_questions_by_level(lop, yeu_cau)
   Chế độ THỦ CÔNG — giữ lại để test/debug nhanh qua API
   /api/exam/select-questions khi muốn chỉ định thẳng
   (chuong_so, loai_cau, muc_do, so_luong) mà KHÔNG cần đi qua Curriculum.
   Không dùng trong luồng WF001 chính thức.
"""

import random
import re
from collections import Counter

from app.services.mapping_service import load_mapping, phan_loai_cau

_CHUONG_PATTERN = re.compile(r"^L\d+_C(\d+)_")

LOAI_KY_HIEU = {
    "trac_nghiem": "MC",
    "dung_sai_cau_lon": "TF",
    "tra_loi_ngan": "SA",
    "tu_luan": "TL",
}


class SelectorError(Exception):
    pass


def _chuong_tu_curriculum_id(curriculum_id: str) -> int:
    match = _CHUONG_PATTERN.match(curriculum_id)
    if not match:
        raise SelectorError(f"curriculum_id không đúng định dạng: {curriculum_id}")
    return int(match.group(1))


def _xoay_vong_bien_the(candidates: list[dict], so_luong: int, da_dung_id: set) -> list[dict]:
    """
    Chọn so_luong Generator ID trong candidates (các phiên bản A/B/C của
    cùng 1 curriculum_id + loại câu). Ưu tiên phiên bản CHƯA dùng trong
    đề hiện tại (da_dung_id) để tăng đa dạng — xoay vòng thay vì random
    thuần. Hết phiên bản khác mới dùng lại (cho phép lặp).
    """
    if not candidates:
        return []

    chua_dung = [c for c in candidates if c["id"] not in da_dung_id]
    random.shuffle(chua_dung)

    chon = []
    con_thieu = so_luong
    pool = chua_dung[:]
    while con_thieu > 0:
        if not pool:
            pool = candidates[:]
            random.shuffle(pool)
        item = pool.pop()
        chon.append(item)
        da_dung_id.add(item["id"])
        con_thieu -= 1

    return chon


# ============================================================
# CHẾ ĐỘ CHÍNH THỨC — theo Blueprint (curriculum_id)
# ============================================================

def select_questions(lop: int, blueprint: dict) -> list[dict]:
    """
    blueprint cần có các khoá: dung_sai, trac_nghiem, tra_loi_ngan, tu_luan
    đúng cấu trúc doc 03_DATA_STRUCTURE.md (mục Blueprint).
    """
    cache: dict[int, list[dict]] = {}
    # da_dung tách riêng theo loại câu: cùng 1 curriculum_id vẫn có thể
    # được dùng cho cả MC lẫn TL trong cùng 1 đề (2 dạng câu khác nhau).
    da_dung: dict[str, set] = {"trac_nghiem": set(), "tra_loi_ngan": set(), "tu_luan": set()}
    ket_qua = []

    def _mapping_chuong(chuong_so: int) -> list[dict]:
        if chuong_so not in cache:
            cache[chuong_so] = load_mapping(lop, chuong_so)
        return cache[chuong_so]

    # ---- TF (Đúng/Sai) — theo chuong_so, KHÔNG qua Curriculum (Ngoại lệ 1, doc 04) ----
    for item in blueprint.get("dung_sai", []):
        chuong_so = item["chuong_so"]
        so_luong = item["so_cau"]
        if so_luong <= 0:
            continue

        candidates = [
            m for m in _mapping_chuong(chuong_so)
            if phan_loai_cau(m) == "dung_sai_cau_lon"
        ]
        if not candidates:
            raise SelectorError(f"Chương {chuong_so}: không có câu Đúng/Sai nào trong Mapping.")

        # TF dùng chung 1 "sổ" da_dung riêng (không lẫn với MC/SA/TL)
        da_dung.setdefault("dung_sai_cau_lon", set())
        chosen = _xoay_vong_bien_the(candidates, so_luong, da_dung["dung_sai_cau_lon"])
        for c in chosen:
            ket_qua.append({
                "generator_id": c["id"],
                "chuong_so": chuong_so,
                "loai_cau": "dung_sai_cau_lon",
                "muc_do": None,
                "loai": c.get("Loai"),
                "dang": c.get("Dang"),
            })

    # ---- MC / SA / TL — theo curriculum_id ----
    for loai_cau in ("trac_nghiem", "tra_loi_ngan", "tu_luan"):
        for item in blueprint.get(loai_cau, []):
            curriculum_id = item["curriculum_id"]
            so_luong = item.get("tong_so_cau", 1)
            if so_luong <= 0:
                continue

            chuong_so = item.get("chuong_so") or _chuong_tu_curriculum_id(curriculum_id)

            candidates = [
                m for m in _mapping_chuong(chuong_so)
                if m["id"].startswith(curriculum_id + "_") and phan_loai_cau(m) == loai_cau
            ]
            if not candidates:
                raise SelectorError(
                    f"{curriculum_id} ({LOAI_KY_HIEU[loai_cau]}): "
                    f"không có Generator nào khớp trong Mapping."
                )

            chosen = _xoay_vong_bien_the(candidates, so_luong, da_dung[loai_cau])
            for c in chosen:
                ket_qua.append({
                    "generator_id": c["id"],
                    "chuong_so": chuong_so,
                    "curriculum_id": curriculum_id,
                    "loai_cau": loai_cau,
                    "muc_do": item.get("muc_do"),
                    "loai": c.get("Loai"),
                    "dang": c.get("Dang"),
                })

    return ket_qua


# ============================================================
# CHẾ ĐỘ THỦ CÔNG — theo (chuong_so, loai_cau, muc_do), KHÔNG qua Curriculum
# Giữ lại cho test/debug nhanh (API /api/exam/select-questions cũ).
# ============================================================

def _chon_uu_tien_khong_trung(candidates: list[dict], so_luong: int) -> list[dict]:
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


def select_questions_by_level(lop: int, yeu_cau: list[dict]) -> list[dict]:
    """
    yeu_cau: list các mục dạng:
        {"chuong_so": 1, "loai_cau": "trac_nghiem", "muc_do": "NB", "so_luong": 3}
        {"chuong_so": 1, "loai_cau": "dung_sai_cau_lon", "so_luong": 1}

    CHỈ dùng để test/debug thủ công. Luồng WF001 chính thức phải dùng
    select_questions(lop, blueprint) ở trên.
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