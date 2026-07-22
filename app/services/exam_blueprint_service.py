import math
import random
import re

from app.services.exam_scope_service import load_scope_heso1, load_scope_heso23
from app.services.exam_rules_service import resolve_cau_truc_de, ExamRulesError

_CHUONG_PATTERN = re.compile(r"_C(\d+)_B")


class BlueprintError(Exception):
    pass


def _dem_so_bai_theo_chuong(pham_vi_bai: list[str]) -> dict[int, int]:
    dem = {}
    for bai_id in pham_vi_bai:
        match = _CHUONG_PATTERN.search(bai_id)
        if not match:
            continue
        chuong_so = int(match.group(1))
        dem[chuong_so] = dem.get(chuong_so, 0) + 1
    return dem


def _chia_theo_so_bai(so_luong: int, so_bai_theo_chuong: dict[int, int]) -> dict[int, int]:
    """
    Phương án C: chia so_luong câu cho các chương theo tỉ lệ số bài học.
    Dùng cho NB, TH (không có phân biệt VD/VDC).
    """
    if so_luong <= 0:
        return {}

    tong_so_bai = sum(so_bai_theo_chuong.values())
    if tong_so_bai == 0:
        return {}

    ket_qua = {
        chuong_so: math.floor(so_luong * so_bai / tong_so_bai)
        for chuong_so, so_bai in so_bai_theo_chuong.items()
    }
    da_phan_bo = sum(ket_qua.values())
    con_thieu = so_luong - da_phan_bo

    if con_thieu > 0:
        chuong_uu_tien = max(so_bai_theo_chuong, key=so_bai_theo_chuong.get)
        ket_qua[chuong_uu_tien] = ket_qua.get(chuong_uu_tien, 0) + con_thieu

    return {c: sl for c, sl in ket_qua.items() if sl > 0}


def _phan_bo_vd_vdc(chapters: list[int], so_vd: int, so_vdc: int) -> dict[int, dict]:
    """
    Quy tắc:
    1. VDC: mỗi chương chỉ nhận tối đa 1 (rải đều các chương khác nhau).
       Nếu so_vdc > số chương, mới lặp lại chương.
    2. VD: ưu tiên rải vào các chương CHƯA có VDC (mỗi chương 1 câu trước).
       Chỉ khi hết chương khác mới quay lại dùng chương đã có VDC.
    Lưu ý: cả VD và VDC đều lấy chung 1 pool "muc_do=VD" trong Mapping
    (Mapping không có nhãn VDC riêng) — hàm này chỉ quyết định PHÂN BỔ
    theo chương, không ảnh hưởng đến việc chọn ID.
    """
    chapters = chapters[:]
    random.shuffle(chapters)

    ket_qua = {c: {"vd": 0, "vdc": 0} for c in chapters}

    # Bước 1 — gán VDC, mỗi chương tối đa 1, lặp vòng nếu thiếu chương
    for i in range(so_vdc):
        chuong = chapters[i % len(chapters)]
        ket_qua[chuong]["vdc"] += 1

    vdc_chapters = {c for c in chapters if ket_qua[c]["vdc"] > 0}
    other_chapters = [c for c in chapters if c not in vdc_chapters]

    # Bước 2 — gán VD, ưu tiên chương khác (mỗi chương 1 câu trước)
    remaining = so_vd
    for c in other_chapters:
        if remaining <= 0:
            break
        ket_qua[c]["vd"] += 1
        remaining -= 1

    # Bước 3 — hết chương khác, mới quay lại chương đã có VDC (cho phép lặp)
    fallback_chapters = list(vdc_chapters) if vdc_chapters else chapters
    idx = 0
    while remaining > 0 and fallback_chapters:
        c = fallback_chapters[idx % len(fallback_chapters)]
        ket_qua[c]["vd"] += 1
        remaining -= 1
        idx += 1

    return {c: v for c, v in ket_qua.items() if v["vd"] > 0 or v["vdc"] > 0}


def _chon_chuong_dung_sai(so_bai_theo_chuong: dict[int, int], so_cau_lon: int) -> dict[int, int]:
    """
    Quy tắc (theo luồng cũ): chọn N chương, mỗi chương tối đa 1 câu Đúng/Sai lớn,
    ưu tiên chương có nhiều bài hơn. Nếu N > số chương, mới lặp lại chương
    (ưu tiên lại theo thứ tự nhiều bài hơn).
    """
    if so_cau_lon <= 0:
        return {}

    chuong_sap_xep = sorted(so_bai_theo_chuong.keys(), key=lambda c: -so_bai_theo_chuong[c])

    ket_qua = {}
    for i in range(so_cau_lon):
        chuong = chuong_sap_xep[i % len(chuong_sap_xep)]
        ket_qua[chuong] = ket_qua.get(chuong, 0) + 1

    return ket_qua


def build_blueprint(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
) -> dict:
    # BƯỚC 1 — xác định phạm vi bài
    if loai_he_so == "HeSo1":
        if not pham_vi_chuong:
            raise BlueprintError("Thiếu pham_vi_chuong cho HeSo1")
        scope = load_scope_heso1(lop, pham_vi_chuong)
        pham_vi_bai = scope["pham_vi_bai"]
    elif loai_he_so == "HeSo2_HeSo3":
        if not ki_thi:
            raise BlueprintError("Thiếu ki_thi cho HeSo2_HeSo3")
        scope = load_scope_heso23(lop, ki_thi)
        if "error" in scope:
            raise BlueprintError(scope["error"])
        pham_vi_bai = scope["pham_vi_bai"]
    else:
        raise BlueprintError(f"loai_he_so '{loai_he_so}' không hợp lệ")

    so_bai_theo_chuong = _dem_so_bai_theo_chuong(pham_vi_bai)
    if not so_bai_theo_chuong:
        raise BlueprintError("Không xác định được chương nào trong phạm vi bài")

    danh_sach_chuong = list(so_bai_theo_chuong.keys())

    # BƯỚC 2 — số câu mỗi mức độ theo hệ số
    try:
        rules_result = resolve_cau_truc_de(loai_he_so, cau_truc_tu_hoc_sinh)
    except ExamRulesError as e:
        raise BlueprintError(str(e))

    phan_bo_muc_do = rules_result["phan_bo_muc_do"]

    # BƯỚC 3 — ghép: phân bổ theo chương cho từng loại câu
    yeu_cau = []
    bao_cao_phan_bo = {}

    for loai_cau, phan_bo in phan_bo_muc_do.items():
        if loai_cau == "dung_sai_cau_lon":
            so_cau_lon = phan_bo["NB"]  # 4 giá trị bằng nhau, lấy 1 đại diện
            phan_bo_chuong = _chon_chuong_dung_sai(so_bai_theo_chuong, so_cau_lon)
            bao_cao_phan_bo[loai_cau] = phan_bo_chuong
            for chuong_so, sl in phan_bo_chuong.items():
                yeu_cau.append({
                    "chuong_so": chuong_so,
                    "loai_cau": "dung_sai_cau_lon",
                    "muc_do": None,
                    "so_luong": sl,
                })
            continue

        # NB, TH: chia theo tỉ lệ số bài (Phương án C)
        for muc_do in ("NB", "TH"):
            so_luong = phan_bo.get(muc_do, 0)
            phan_bo_chuong = _chia_theo_so_bai(so_luong, so_bai_theo_chuong)
            for chuong_so, sl in phan_bo_chuong.items():
                yeu_cau.append({
                    "chuong_so": chuong_so,
                    "loai_cau": loai_cau,
                    "muc_do": muc_do,
                    "so_luong": sl,
                })

        # VD + VDC: rải theo quy tắc "1 VDC/chương, VD ưu tiên chương khác"
        so_vd = phan_bo.get("VD", 0)
        so_vdc = phan_bo.get("VDC", 0)
        if so_vd > 0 or so_vdc > 0:
            phan_bo_vd_vdc = _phan_bo_vd_vdc(danh_sach_chuong, so_vd, so_vdc)
            bao_cao_phan_bo.setdefault(loai_cau, {})["vd_vdc"] = phan_bo_vd_vdc

            for chuong_so, v in phan_bo_vd_vdc.items():
                tong = v["vd"] + v["vdc"]
                if tong > 0:
                    yeu_cau.append({
                        "chuong_so": chuong_so,
                        "loai_cau": loai_cau,
                        "muc_do": "VD",  # Mapping chỉ có nhãn VD, không có VDC riêng
                        "so_luong": tong,
                    })

    return {
        "pham_vi_bai": pham_vi_bai,
        "so_bai_theo_chuong": so_bai_theo_chuong,
        "cau_truc_tong_quat": rules_result["cau_truc_tong_quat"],
        "nguon_cau_truc": rules_result["nguon_cau_truc"],
        "bao_cao_phan_bo": bao_cao_phan_bo,
        "yeu_cau": yeu_cau,
    }

from app.services.question_selector_service import select_questions, SelectorError


def build_and_select(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
) -> dict:
    """
    Ghép build_blueprint() + select_questions() thành 1 bước.
    """
    blueprint = build_blueprint(
        lop=lop,
        loai_he_so=loai_he_so,
        ki_thi=ki_thi,
        pham_vi_chuong=pham_vi_chuong,
        cau_truc_tu_hoc_sinh=cau_truc_tu_hoc_sinh,
    )

    try:
        danh_sach_id = select_questions(lop=lop, yeu_cau=blueprint["yeu_cau"])
    except SelectorError as e:
        raise BlueprintError(str(e))

    blueprint["danh_sach_generator_id"] = danh_sach_id
    return blueprint