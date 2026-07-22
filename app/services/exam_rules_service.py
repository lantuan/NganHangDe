import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RULES_FILE = BASE_DIR / "data" / "config" / "exam_rules.json"

CAC_LOAI_CAU = ["trac_nghiem", "dung_sai_cau_lon", "tra_loi_ngan", "tu_luan"]


class ExamRulesError(Exception):
    pass


def _load_rules() -> dict:
    if not RULES_FILE.exists():
        raise ExamRulesError(f"Không tìm thấy file quy định: {RULES_FILE}")
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _chia_theo_ty_le(tong_so_cau: int, ty_le: dict) -> dict:
    """
    Dùng cho trac_nghiem / tra_loi_ngan / tu_luan:
    chia tổng số câu theo tỉ lệ mức độ (NB/TH/VD/VDC).
    Làm tròn xuống trước, phần dư cộng vào mức có tỉ lệ cao nhất.
    """
    ket_qua = {
        muc_do: math.floor(tong_so_cau * ty_le_muc_do)
        for muc_do, ty_le_muc_do in ty_le.items()
    }
    da_phan_bo = sum(ket_qua.values())
    con_thieu = tong_so_cau - da_phan_bo

    if con_thieu > 0:
        muc_uu_tien = max(ty_le, key=ty_le.get)
        ket_qua[muc_uu_tien] += con_thieu

    return ket_qua


def _phan_bo_dung_sai(so_cau_lon: int) -> dict:
    """
    Đúng/Sai: mỗi câu lớn LUÔN gồm đủ 4 ý NB-TH-VD-VDC.
    Không chia theo tỉ lệ phần trăm.
    """
    return {"NB": so_cau_lon, "TH": so_cau_lon, "VD": so_cau_lon, "VDC": so_cau_lon}


def resolve_cau_truc_de(
    loai_he_so: str,
    cau_truc_tu_hoc_sinh: dict | None = None,
) -> dict:
    """
    Input:
        loai_he_so: "HeSo1" | "HeSo2_HeSo3"
        cau_truc_tu_hoc_sinh: phần tự quy định, dạng:
            {
                "trac_nghiem": {"so_luong": 20, "ty_le_muc_do": {...}},
                ...
            }
    Output:
        {
            "cau_truc_tong_quat": {loai_cau: so_luong},
            "phan_bo_muc_do": {loai_cau: {NB, TH, VD, VDC}},
            "nguon_cau_truc": "table" | "mixed" | "user"
        }
    """
    rules = _load_rules()

    if loai_he_so not in rules:
        raise ExamRulesError(
            f"loai_he_so '{loai_he_so}' không hợp lệ. Chỉ chấp nhận: {list(rules.keys())}"
        )

    mac_dinh = rules[loai_he_so]
    yeu_cau = cau_truc_tu_hoc_sinh or {}

    cau_truc_tong_quat = {}
    phan_bo_muc_do = {}
    da_dung_bang = False
    da_dung_yeu_cau = False

    for loai_cau in CAC_LOAI_CAU:
        yc_loai_cau = yeu_cau.get(loai_cau, {}) or {}

        so_luong = yc_loai_cau.get("so_luong")
        ty_le = yc_loai_cau.get("ty_le_muc_do")

        if so_luong is None:
            so_luong = mac_dinh[loai_cau]["so_luong"]
            da_dung_bang = True
        else:
            da_dung_yeu_cau = True

        cau_truc_tong_quat[loai_cau] = so_luong

        if loai_cau == "dung_sai_cau_lon":
            phan_bo_muc_do[loai_cau] = _phan_bo_dung_sai(so_luong)
        else:
            if ty_le is None:
                ty_le = mac_dinh[loai_cau]["ty_le_muc_do"]
                da_dung_bang = True
            else:
                da_dung_yeu_cau = True
            phan_bo_muc_do[loai_cau] = _chia_theo_ty_le(so_luong, ty_le)

    if da_dung_bang and da_dung_yeu_cau:
        nguon_cau_truc = "mixed"
    elif da_dung_bang:
        nguon_cau_truc = "table"
    else:
        nguon_cau_truc = "user"

    return {
        "cau_truc_tong_quat": cau_truc_tong_quat,
        "phan_bo_muc_do": phan_bo_muc_do,
        "nguon_cau_truc": nguon_cau_truc,
    }