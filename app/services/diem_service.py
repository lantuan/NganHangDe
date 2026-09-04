"""
CN_TinhThangDiem - tinh thang diem 10 cho mot de thi.

Quy dinh (giao vien chot):
    - Trac nghiem nhieu lua chon (MC): 3 diem
    - Dung/Sai (TF):                   2 diem
    - Tra loi ngan (SA):               2 diem
    - Tu luan (TL):                    3 diem
    => Tong 10 diem khi de co du 4 phan.

Cach chia:
    - Diem cua MOT PHAN duoc chia DEU cho so cau co that trong de o
      phan do. Vi du de co 12 cau MC -> moi cau 3/12 = 0.25 diem.
    - Cau TF: diem cua cau duoc chia tiep DEU cho 4 y (a/b/c/d).
      Vi du de co 2 cau TF -> moi cau 2/2 = 1.0 diem -> moi y 0.25.

Trong so la CO DINH (chia_lai_khi_thieu_phan = false):
    de thieu phan nao thi diem toi da cua de giam dung phan do,
    KHONG chia lai diem cho cac phan con lai. Vi du de chi co MC va
    TF thi diem toi da la 5.0 chu khong phai 10.

Lam tron:
    Moi phep cong deu dung so THUC chua lam tron; chi lam tron 2 chu
    so thap phan o buoc cuoi (diem tung cau khi hien thi va tong diem).
    Lam nhu vay de tranh lech kieu 3 cau SA x 0.67 = 2.01 diem.
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RULES_FILE = BASE_DIR / "data" / "config" / "diem_rules.json"

CAC_LOAI_CAU = ["MC", "TF", "SA", "TL"]


class DiemRulesError(Exception):
    pass


def _load_rules() -> dict:
    if not RULES_FILE.exists():
        raise DiemRulesError(f"Khong tim thay file quy dinh diem: {RULES_FILE}")
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def loai_cau_chuan(cau: dict) -> str:
    """Tra ve loai cau chuan hoa: MC / TF / SA / TL.

    Can ham nay vi answer_parser_service hien CHUA nhan dien duoc cau
    Dung/Sai: cau TF dang bi luu nham loai_cau="TL" trong file
    *_dapan.json, chi phan biet duoc qua generator_id co chua "_TF_"
    (xem docstring dau app/services/grade_photo_service.py). Neu khong
    chuan hoa o day thi cau TF se bi tinh diem theo phan Tu luan.
    """
    loai = (cau.get("loai_cau") or "").strip().upper()
    generator_id = cau.get("generator_id") or ""
    if loai == "TF" or "_TF_" in generator_id:
        return "TF"
    if loai in CAC_LOAI_CAU:
        return loai
    return "TL"


def tinh_thang_diem(danh_sach_dap_an: list[dict]) -> dict:
    """Tinh thang diem cua de tu danh sach dap an da luu khi sinh de.

    Output:
        {
            "trong_so": {"MC": 3.0, ...},
            "theo_phan": {
                "MC": {
                    "ten": "Trac nghiem nhieu lua chon",
                    "so_cau": 12,
                    "diem_phan": 3.0,
                    "diem_moi_cau": 0.25,      # da lam tron, de hien thi
                    "diem_moi_cau_goc": 0.25,  # chua lam tron, de tinh toan
                    "diem_moi_y": None         # rieng TF moi co
                },
                ...
            },
            "diem_toi_da_tong": 10.0,      # chi tinh cac phan CO trong de
            "diem_toi_da_tu_dong": 7.0,    # MC + TF + SA (cham tu dong duoc)
            "diem_phan_tu_luan": 3.0,      # TL - hien dang xay dung
            "so_y_moi_cau_tf": 4
        }
    """
    rules = _load_rules()
    trong_so = rules["trong_so"]
    ten_phan = rules.get("ten_phan", {})
    so_y_tf = rules.get("so_y_moi_cau_tf", 4)
    lam_tron = rules.get("lam_tron", 2)

    so_cau_theo_phan = {loai: 0 for loai in CAC_LOAI_CAU}
    for cau in danh_sach_dap_an:
        so_cau_theo_phan[loai_cau_chuan(cau)] += 1

    theo_phan = {}
    diem_toi_da_tong = 0.0
    diem_toi_da_tu_dong = 0.0

    for loai in CAC_LOAI_CAU:
        so_cau = so_cau_theo_phan[loai]
        diem_phan = float(trong_so.get(loai, 0))

        if so_cau == 0:
            # De khong co phan nay -> khong cong vao diem toi da
            # (trong so co dinh, khong chia lai cho phan khac).
            theo_phan[loai] = {
                "ten": ten_phan.get(loai, loai),
                "so_cau": 0,
                "diem_phan": 0.0,
                "diem_moi_cau": 0.0,
                "diem_moi_cau_goc": 0.0,
                "diem_moi_y": None,
            }
            continue

        diem_moi_cau_goc = diem_phan / so_cau
        theo_phan[loai] = {
            "ten": ten_phan.get(loai, loai),
            "so_cau": so_cau,
            "diem_phan": diem_phan,
            "diem_moi_cau": round(diem_moi_cau_goc, lam_tron),
            "diem_moi_cau_goc": diem_moi_cau_goc,
            "diem_moi_y": (
                round(diem_moi_cau_goc / so_y_tf, lam_tron) if loai == "TF" else None
            ),
        }

        diem_toi_da_tong += diem_phan
        if loai != "TL":
            diem_toi_da_tu_dong += diem_phan

    return {
        "trong_so": trong_so,
        "theo_phan": theo_phan,
        "diem_toi_da_tong": round(diem_toi_da_tong, lam_tron),
        "diem_toi_da_tu_dong": round(diem_toi_da_tu_dong, lam_tron),
        "diem_phan_tu_luan": theo_phan["TL"]["diem_phan"],
        "so_y_moi_cau_tf": so_y_tf,
        "lam_tron": lam_tron,
    }


def diem_toi_da_cua_cau(thang: dict, loai: str) -> float:
    """Diem toi da cua 1 cau (da lam tron, dung de HIEN THI)."""
    return thang["theo_phan"].get(loai, {}).get("diem_moi_cau", 0.0)


def diem_toi_da_cua_cau_goc(thang: dict, loai: str) -> float:
    """Diem toi da cua 1 cau (CHUA lam tron, dung de CONG DON)."""
    return thang["theo_phan"].get(loai, {}).get("diem_moi_cau_goc", 0.0)


def diem_cau_tf(thang: dict, so_y_dung: int) -> tuple[float, float]:
    """Diem cua 1 cau Dung/Sai theo so y dung.

    Tra ve (diem_goc_de_cong_don, diem_da_lam_tron_de_hien_thi).
    """
    so_y = thang.get("so_y_moi_cau_tf", 4) or 4
    goc = diem_toi_da_cua_cau_goc(thang, "TF") * so_y_dung / so_y
    return goc, round(goc, thang.get("lam_tron", 2))


def so_dep(x) -> str:
    """3.0 -> '3', 0.25 -> '0.25' (bo duoi .0 cho de doc tren man hinh)."""
    if x is None:
        return "0"
    x = float(x)
    return str(int(x)) if x == int(x) else str(round(x, 2))


def mo_ta_thang_diem(thang: dict) -> str:
    """Mot dong mo ta thang diem, dung lam ghi_chu tra ve frontend."""
    phan = []
    for loai in CAC_LOAI_CAU:
        tp = thang["theo_phan"][loai]
        if tp["so_cau"] == 0:
            continue
        phan.append(
            f"{tp['ten']} {so_dep(tp['diem_phan'])}đ "
            f"({tp['so_cau']} câu × {so_dep(tp['diem_moi_cau'])}đ)"
        )
    return " · ".join(phan)
