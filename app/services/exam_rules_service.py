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


MUC_DO = ("NB", "TH", "VD", "VDC")


def chuan_hoa_ty_le(ty_le: dict, ten: str = "") -> dict:
    """Tỉ lệ người dùng đặt (cô Lan 03/10/2026): chấp nhận phân số (0.5) hoặc
    phần trăm (50); thiếu mức nào coi là 0; tổng phải bằng 100%. Trả về phân số."""
    if not isinstance(ty_le, dict):
        raise ExamRulesError(f"Tỉ lệ mức độ {ten} không hợp lệ.")
    thua = [k for k in ty_le if str(k).upper() not in MUC_DO]
    if thua:
        raise ExamRulesError(f"Tỉ lệ mức độ {ten}: mức không hợp lệ {thua} (chỉ NB, TH, VD, VDC).")
    try:
        v = {m: float(ty_le.get(m, ty_le.get(m.lower(), 0)) or 0) for m in MUC_DO}
    except (TypeError, ValueError):
        raise ExamRulesError(f"Tỉ lệ mức độ {ten} phải là số.")
    if any(x < 0 for x in v.values()):
        raise ExamRulesError(f"Tỉ lệ mức độ {ten} không được âm.")
    tong = sum(v.values())
    if tong <= 0:
        raise ExamRulesError(f"Tỉ lệ mức độ {ten}: tổng bằng 0.")
    if tong > 1.5:                      # phần trăm
        v = {m: x / 100 for m, x in v.items()}
        tong /= 100
    if abs(tong - 1) > 0.005:
        raise ExamRulesError(f"Tỉ lệ mức độ {ten} phải có tổng 100% (đang là {round(tong * 100, 1)}%).")
    return v


def _chia_theo_ty_le(tong_so_cau: int, ty_le: dict, chinh_xac: bool = False) -> dict:
    """
    Dùng cho trac_nghiem / tra_loi_ngan / tu_luan:
    chia tổng số câu theo tỉ lệ mức độ (NB/TH/VD/VDC).
    Mặc định (bảng exam_rules.json): làm tròn xuống trước, phần dư cộng vào mức
    có tỉ lệ cao nhất.
    chinh_xac=True (ma trận do người dùng đặt): phương pháp phần dư lớn nhất -
    mức có tỉ lệ 0 KHÔNG BAO GIỜ nhận câu; số câu mỗi mức lệch tỉ lệ không quá 1.
    """
    if chinh_xac:
        goc = {m: tong_so_cau * ty_le.get(m, 0) for m in ty_le}
        ket_qua = {m: math.floor(x + 1e-9) for m, x in goc.items()}
        con = tong_so_cau - sum(ket_qua.values())
        theo_du = sorted((m for m in goc if ty_le[m] > 0), key=lambda m: -(goc[m] - ket_qua[m]))
        for i in range(con):
            ket_qua[theo_du[i % len(theo_du)]] += 1
        return ket_qua
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
            chinh_xac = ty_le is not None
            if ty_le is None:
                ty_le = mac_dinh[loai_cau]["ty_le_muc_do"]
                da_dung_bang = True
            else:
                ty_le = chuan_hoa_ty_le(ty_le, loai_cau)
                da_dung_yeu_cau = True
            # Tự luận (cô Lan 30/09/2026): so_luong là số CÂU, mỗi câu gồm
            # so_y_moi_cau ý (mặc định 2: ý a mức VD, ý b mức VDC). Ma trận
            # tính theo TỪNG Ý (suất) - phan_bo_muc_do["tu_luan"] đếm suất.
            so_y = mac_dinh[loai_cau].get("so_y_moi_cau", 1) if loai_cau == "tu_luan" else 1
            phan_bo_muc_do[loai_cau] = _chia_theo_ty_le(so_luong * so_y, ty_le, chinh_xac)

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