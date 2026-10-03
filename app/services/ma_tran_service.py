"""
Ma trận mức độ do NGƯỜI DÙNG đặt (cô Lan 03/10/2026).

Trước đây form giáo viên và nút "Đồng ý, tạo đề" của chat không truyền tỉ lệ
mức độ xuống bộ chọn, nên đề luôn theo bảng mặc định (SA, TL mặc định toàn VD,
VDC): chọn 100% NB, TH vẫn ra VD. File này gom việc đọc / chuẩn hoá ma trận.

- Chỉ MC, SA, TL đặt được số câu và tỉ lệ. Câu Đúng/Sai GIỮ NGUYÊN cấu trúc
  (mỗi câu 4 ý NB-TH-VD-VDC), số câu Đúng/Sai lấy theo bảng mặc định.
- Tự luận: so_luong là số CÂU, mỗi câu 2 ý (ma trận tính theo từng ý).
"""
from app.services.exam_rules_service import (
    ExamRulesError, MUC_DO, _load_rules, chuan_hoa_ty_le)

# tiền tố trường form -> loại câu
LOAI_FORM = {"mc": "trac_nghiem", "sa": "tra_loi_ngan", "tl": "tu_luan"}
LOAI_DAT_DUOC = tuple(LOAI_FORM.values())


def ma_tran_mac_dinh(loai_he_so: str) -> dict:
    """Bảng mặc định của loại bài kiểm tra, để điền sẵn vào form."""
    rules = _load_rules()
    if loai_he_so not in rules:
        raise ExamRulesError(f"loai_he_so '{loai_he_so}' không hợp lệ.")
    kq = {}
    for loai, v in rules[loai_he_so].items():
        kq[loai] = {"so_luong": v["so_luong"],
                    "ty_le_muc_do": {m: round(float(v["ty_le_muc_do"].get(m, 0)) * 100) for m in MUC_DO}}
        if loai == "tu_luan":
            kq[loai]["so_y_moi_cau"] = v.get("so_y_moi_cau", 1)
    return kq


def doc_ma_tran_tu_form(form) -> dict | None:
    """Đọc ma trận từ form giáo viên. Trả None nếu không bật "tự đặt ma trận".

    Trường: tuy_chinh_ma_tran, <mc|sa|tl>_so, <mc|sa|tl>_<nb|th|vd|vdc> (phần trăm).
    Trả về cau_truc_tu_hoc_sinh cho build_blueprint (chỉ MC, SA, TL).
    """
    if not form.get("tuy_chinh_ma_tran"):
        return None
    kq = {}
    for tt, loai in LOAI_FORM.items():
        try:
            so = int(str(form.get(f"{tt}_so", "")).strip() or 0)
        except ValueError:
            raise ExamRulesError(f"Số câu {tt.upper()} phải là số nguyên.")
        if so < 0 or so > 60:
            raise ExamRulesError(f"Số câu {tt.upper()} phải từ 0 đến 60.")
        if so == 0:
            kq[loai] = {"so_luong": 0}
            continue
        ty_le = {}
        for m in MUC_DO:
            raw = str(form.get(f"{tt}_{m.lower()}", "")).strip().replace(",", ".")
            ty_le[m] = float(raw) if raw else 0.0
        kq[loai] = {"so_luong": so, "ty_le_muc_do": chuan_hoa_ty_le(ty_le, tt.upper())}
    return kq
