import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RULES_FILE = BASE_DIR / "data" / "config" / "exam_rules.json"


class ExamRulesError(Exception):
    pass


def _load_rules() -> dict:
    if not RULES_FILE.exists():
        raise ExamRulesError(f"Không tìm thấy file quy định: {RULES_FILE}")
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _phan_bo_muc_do(tong_so_cau: int, ty_le: dict) -> dict:
    """
    Chia tổng số câu theo tỉ lệ NB/TH/VD/VDC.
    Làm tròn xuống trước, phần dư cộng vào NB để đảm bảo tổng khớp.
    """
    ket_qua = {
        muc_do: math.floor(tong_so_cau * ty_le_muc_do)
        for muc_do, ty_le_muc_do in ty_le.items()
    }
    da_phan_bo = sum(ket_qua.values())
    con_thieu = tong_so_cau - da_phan_bo
    if con_thieu > 0:
        ket_qua["NB"] += con_thieu
    return ket_qua


def resolve_cau_truc_de(
    loai_he_so: str,
    cau_truc_tu_hoc_sinh: dict | None = None,
) -> dict:
    """
    Input:
        loai_he_so: "HeSo1" | "HeSo2_HeSo3"
        cau_truc_tu_hoc_sinh: phần học sinh/giáo viên tự quy định (có thể None,
            hoặc chỉ có 1 vài trường trong {trac_nghiem, dung_sai_cau_lon,
            tra_loi_ngan, tu_luan, ty_le_muc_do})

    Output:
        {
            "cau_truc_tong_quat": {...},
            "ty_le_muc_do_goc": {...},
            "nguon_cau_truc": "table" | "mixed" | "user"
        }
    """
    rules = _load_rules()

    if loai_he_so not in rules:
        raise ExamRulesError(
            f"loai_he_so '{loai_he_so}' không hợp lệ. "
            f"Chỉ chấp nhận: {list(rules.keys())}"
        )

    mac_dinh = rules[loai_he_so]
    yeu_cau = cau_truc_tu_hoc_sinh or {}

    cac_truong_cau_truc = ["trac_nghiem", "dung_sai_cau_lon", "tra_loi_ngan", "tu_luan"]

    cau_truc_tong_quat = {}
    da_dung_bang = False
    da_dung_yeu_cau = False

    for truong in cac_truong_cau_truc:
        if truong in yeu_cau and yeu_cau[truong] is not None:
            cau_truc_tong_quat[truong] = yeu_cau[truong]
            da_dung_yeu_cau = True
        else:
            cau_truc_tong_quat[truong] = mac_dinh[truong]
            da_dung_bang = True

    if "ty_le_muc_do" in yeu_cau and yeu_cau["ty_le_muc_do"]:
        ty_le_muc_do_goc = yeu_cau["ty_le_muc_do"]
        da_dung_yeu_cau = True
    else:
        ty_le_muc_do_goc = mac_dinh["ty_le_muc_do"]
        da_dung_bang = True

    if da_dung_bang and da_dung_yeu_cau:
        nguon_cau_truc = "mixed"
    elif da_dung_bang:
        nguon_cau_truc = "table"
    else:
        nguon_cau_truc = "user"

    return {
        "cau_truc_tong_quat": cau_truc_tong_quat,
        "ty_le_muc_do_goc": ty_le_muc_do_goc,
        "nguon_cau_truc": nguon_cau_truc,
    }


def phan_bo_so_cau_theo_muc_do(cau_truc_tong_quat: dict, ty_le_muc_do: dict) -> dict:
    """
    Với mỗi loại câu (trắc nghiệm, trả lời ngắn, tự luận),
    chia theo tỉ lệ mức độ NB/TH/VD/VDC.
    Riêng dung_sai_cau_lon mỗi câu mặc định đủ 4 ý NB-TH-VD-VDC (đúng luồng cũ),
    không cần chia theo tỉ lệ.
    """
    return {
        "trac_nghiem": _phan_bo_muc_do(cau_truc_tong_quat["trac_nghiem"], ty_le_muc_do),
        "tra_loi_ngan": _phan_bo_muc_do(cau_truc_tong_quat["tra_loi_ngan"], ty_le_muc_do),
        "tu_luan": _phan_bo_muc_do(cau_truc_tong_quat["tu_luan"], ty_le_muc_do),
        "dung_sai_cau_lon": cau_truc_tong_quat["dung_sai_cau_lon"],
    }