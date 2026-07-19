from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PPCT_DIR = BASE_DIR / "data" / "ppct"

# ki_thi -> (học kỳ, mốc dừng chính, mốc phụ để chia 30/70)
# mốc phụ = None nghĩa là không cần chia tỷ lệ (giữa kỳ)
KI_THI_MAP = {
    "giua_ky_1": (1, "GK1_EXAM", None),
    "cuoi_ky_1": (1, "CK1_EXAM", "GK1_EXAM"),
    "giua_ky_2": (2, "GK2_EXAM", None),
    "cuoi_ky_2": (2, "CK2_EXAM", "GK2_EXAM"),
}


def _load_ppct(lop: int) -> list[dict]:
    file = PPCT_DIR / f"toan{lop}.json"
    if not file.exists():
        raise FileNotFoundError(f"Không tìm thấy PPCT cho khối {lop}")
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


# ======================================================
# CASE A: HeSo1 - kiểm tra thường xuyên, trong 1 chương
# ======================================================

def load_scope_heso1(lop: int, pham_vi_chuong: str) -> dict:
    """
    pham_vi_chuong: vd "chuong_1" -> chuong_so = 1

    Luật:
    - Chỉ lấy bài trong đúng chương đó.
    - Nếu gặp bài có boundary_after khác null -> lấy bài đó rồi dừng
      (không lấy các bài sau, dù cùng chương).
    """
    ppct = _load_ppct(lop)
    so_chuong = int(pham_vi_chuong.replace("chuong_", ""))

    bai_trong_chuong = [b for b in ppct if b["chuong_so"] == so_chuong]

    ket_qua = []
    for b in bai_trong_chuong:
        ket_qua.append(b)
        if b.get("boundary_after") is not None:
            break

    return {
        "loai_he_so": "HeSo1",
        "chuong_so": so_chuong,
        "pham_vi_bai": [b["id"] for b in ket_qua],
    }


# ======================================================
# CASE B: HeSo2_HeSo3 - giữa kỳ / cuối kỳ
# ======================================================

def load_scope_heso23(lop: int, ki_thi: str) -> dict:
    """
    ki_thi: "giua_ky_1" | "cuoi_ky_1" | "giua_ky_2" | "cuoi_ky_2"

    Luật:
    - Quét PPCT trong đúng học kỳ tương ứng, từ đầu.
    - Dừng khi gặp bài có boundary_after = mốc dừng chính.
    - Nếu là cuối kỳ (có mốc phụ):
        + phần từ đầu đến bài có boundary_after = mốc phụ  -> 30%
        + phần còn lại (sau mốc phụ đến mốc chính)         -> 70%
    - Nếu là giữa kỳ (không có mốc phụ): không chia tỷ lệ.
    """
    info = KI_THI_MAP.get(ki_thi)
    if not info:
        return {"error": "KI_THI_KHONG_HOP_LE"}

    hoc_ky, moc_chinh, moc_phu = info

    try:
        ppct = _load_ppct(lop)
    except FileNotFoundError as e:
        return {"error": "PPCT_NOT_FOUND", "message": str(e)}

    bai_trong_ky = [b for b in ppct if b["hoc_ky"] == hoc_ky]

    ket_qua = []
    tim_thay_moc_chinh = False
    for b in bai_trong_ky:
        ket_qua.append(b)
        if b.get("boundary_after") == moc_chinh:
            tim_thay_moc_chinh = True
            break

    if not tim_thay_moc_chinh:
        return {"error": "KHONG_TIM_THAY_MOC_DUNG", "moc_can_tim": moc_chinh}

    phan_bo_ty_le = None

    if moc_phu:
        truoc_moc_phu = []
        sau_moc_phu = []
        dang_truoc = True

        for b in ket_qua:
            if dang_truoc:
                truoc_moc_phu.append(b["id"])
            else:
                sau_moc_phu.append(b["id"])
            if b.get("boundary_after") == moc_phu:
                dang_truoc = False

        if dang_truoc:
            # Quét hết mà không gặp mốc phụ -> dữ liệu PPCT có vấn đề
            return {
                "error": "KHONG_TIM_THAY_MOC_PHU",
                "moc_can_tim": moc_phu,
            }

        phan_bo_ty_le = {
            "truoc_giua_ky": {"ti_le": 0.3, "pham_vi_bai": truoc_moc_phu},
            "sau_giua_ky": {"ti_le": 0.7, "pham_vi_bai": sau_moc_phu},
        }

    return {
        "loai_he_so": "HeSo2_HeSo3",
        "ki_thi": ki_thi,
        "pham_vi_chuong": sorted({b["chuong_so"] for b in ket_qua}),
        "pham_vi_bai": [b["id"] for b in ket_qua],
        "phan_bo_ty_le": phan_bo_ty_le,
    }

def load_exam_scope(lop: int, ki_thi: str, pham_vi_chuong: str | None = None) -> dict:
    """
    Hàm điều phối (dispatcher) cho API /api/data/exam-scope.

    - ki_thi == "thuong_xuyen": HeSo1, bắt buộc có pham_vi_chuong.
    - ki_thi in KI_THI_MAP: HeSo2_HeSo3 (giữa kỳ / cuối kỳ).
    """
    if ki_thi == "thuong_xuyen":
        if not pham_vi_chuong:
            return {
                "error": "THIEU_PHAM_VI_CHUONG",
                "message": "HeSo1 (thuong_xuyen) yêu cầu tham số pham_vi_chuong",
            }
        return load_scope_heso1(lop, pham_vi_chuong)

    if ki_thi in KI_THI_MAP:
        return load_scope_heso23(lop, ki_thi)

    return {
        "error": "KI_THI_KHONG_HOP_LE",
        "ki_thi_hop_le": ["thuong_xuyen", *KI_THI_MAP.keys()],
    }