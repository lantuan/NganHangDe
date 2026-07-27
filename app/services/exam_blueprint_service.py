"""
CN_BuildBlueprint

Input : cau_truc_tong_quat, ty_le_muc_do (qua CN_LoadExamRules),
        pham_vi_bai (qua CN_LoadExamScope), Curriculum (qua CN_LoadCurriculum,
        đã lọc theo pham_vi_bai).
Output: Blueprint (đúng cấu trúc doc 03_DATA_STRUCTURE.md — có curriculum_id
        cụ thể cho MC/SA/TL, chuong_so cho TF).

Không được: đọc PPCT, đọc Mapping, gọi Python, sinh PDF, tự tạo/sửa
curriculum_id, tạo curriculum_id mức VDC (không tồn tại — doc 04, Ngoại lệ 2).
"""

import math
import random
import re
from collections import Counter

from app.services.exam_scope_service import load_scope_heso1, load_scope_heso23
from app.services.exam_rules_service import resolve_cau_truc_de, ExamRulesError
from app.services.curriculum_service import load_curriculum_for_scope, CurriculumError
from app.services.question_selector_service import select_questions, SelectorError

_CHUONG_PATTERN = re.compile(r"_C(\d+)_B")

# "tối đa 2 câu SA/chương; tối đa 2 câu TL/chương" — doc 08_CODE_NODES.md
MAX_SA_PER_CHUONG = 2
MAX_TL_PER_CHUONG = 2


class BlueprintError(Exception):
    pass


# ============================================================
# Helper — phạm vi / số bài theo chương (không đổi so với bản cũ)
# ============================================================

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
    Chia so_luong câu cho các chương theo tỉ lệ số bài học (dùng để xác
    định CẦN BAO NHIÊU câu mỗi chương — bước riêng biệt với việc CHỌN
    curriculum_id cụ thể, làm ở _chon_curriculum_id bên dưới).
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


def _chon_chuong_dung_sai(so_bai_theo_chuong: dict[int, int], so_cau_lon: int) -> dict[int, int]:
    """
    TF: chọn N chương (N = so_cau_lon), ưu tiên chương có nhiều bài hơn.
    Nếu N > số chương, lặp lại chương theo đúng thứ tự ưu tiên đó.
    """
    if so_cau_lon <= 0:
        return {}

    chuong_sap_xep = sorted(so_bai_theo_chuong.keys(), key=lambda c: -so_bai_theo_chuong[c])

    ket_qua = {}
    for i in range(so_cau_lon):
        chuong = chuong_sap_xep[i % len(chuong_sap_xep)]
        ket_qua[chuong] = ket_qua.get(chuong, 0) + 1

    return ket_qua


def _phan_bo_vd_vdc(
    chapters: list[int],
    so_vd: int,
    so_vdc: int,
    max_per_chuong: int | None = None,
) -> dict[int, dict]:
    """
    Quy tắc:
    1. VDC: mỗi chương tối đa 1 (rải đều các chương khác nhau), tôn trọng
       max_per_chuong nếu có. Nếu so_vdc > số chương, mới lặp lại chương.
    2. VD: ưu tiên rải vào các chương CHƯA có VDC (mỗi chương 1 câu trước),
       cũng tôn trọng max_per_chuong.
    3. Hết chương còn chỗ mới quay lại chương đã đầy (chấp nhận vượt cap
       như phương án cuối cùng, để không bị kẹt khi ít chương).

    max_per_chuong dùng cho tra_loi_ngan / tu_luan (tối đa 2 câu/chương —
    doc 08_CODE_NODES.md). trac_nghiem không giới hạn (max_per_chuong=None).
    """
    chapters = chapters[:]
    random.shuffle(chapters)
    ket_qua = {c: {"vd": 0, "vdc": 0} for c in chapters}

    def tong(c):
        return ket_qua[c]["vd"] + ket_qua[c]["vdc"]

    def con_cho(c):
        return max_per_chuong is None or tong(c) < max_per_chuong

    # Bước 1 — VDC
    i, con, an_toan = 0, so_vdc, 0
    gioi_han = (so_vdc + so_vd + 1) * len(chapters) * 2 + 20
    while con > 0 and an_toan < gioi_han:
        an_toan += 1
        c = chapters[i % len(chapters)]
        i += 1
        if ket_qua[c]["vdc"] == 0 and con_cho(c):
            ket_qua[c]["vdc"] += 1
            con -= 1

    vdc_chapters = {c for c in chapters if ket_qua[c]["vdc"] > 0}
    other_chapters = [c for c in chapters if c not in vdc_chapters]

    # Bước 2 — VD, ưu tiên chương khác
    con = so_vd
    for c in other_chapters:
        if con <= 0:
            break
        if con_cho(c):
            ket_qua[c]["vd"] += 1
            con -= 1

    # Bước 3 — hết chỗ trống mới quay lại chương đã đầy (chấp nhận vượt cap)
    fallback = [c for c in chapters if con_cho(c)] or chapters
    idx, an_toan = 0, 0
    while con > 0 and an_toan < gioi_han:
        an_toan += 1
        if not fallback:
            fallback = chapters
        c = fallback[idx % len(fallback)]
        idx += 1
        ket_qua[c]["vd"] += 1
        con -= 1
        fallback = [x for x in fallback if con_cho(x)] or chapters

    return {c: v for c, v in ket_qua.items() if v["vd"] > 0 or v["vdc"] > 0}


def _chon_curriculum_id(entries_muc_do: list[dict], so_luong: int, da_dung: set) -> list[dict]:
    """
    Chọn so_luong Curriculum entries (không nhất thiết distinct nếu hết
    lựa chọn) từ danh sách entries CÙNG 1 mức độ trong 1 chương.

    Quy tắc (doc 08_CODE_NODES.md, mục CN_BuildBlueprint bước 4):
    - Ưu tiên rải ĐỀU giữa các bài (không dồn hết vào 1 bài).
    - Không lặp competency cùng mức nếu còn lựa chọn khác (da_dung).
    - Chỉ lặp khi đã dùng hết toàn bộ competency khác trong đề hiện tại.
    """
    if so_luong <= 0 or not entries_muc_do:
        return []

    theo_bai: dict[str, list[dict]] = {}
    for e in entries_muc_do:
        theo_bai.setdefault(e["bai_so"], []).append(e)

    danh_sach_bai = list(theo_bai.keys())
    random.shuffle(danh_sach_bai)
    for ds in theo_bai.values():
        random.shuffle(ds)

    chon: list[dict] = []
    con_thieu = so_luong

    # Vòng 1 — rải đều theo bài, ưu tiên competency CHƯA dùng trong đề
    while con_thieu > 0:
        lay_duoc_vong_nay = False
        for bai in danh_sach_bai:
            if con_thieu <= 0:
                break
            ung_vien = [
                e for e in theo_bai[bai]
                if e["id"] not in da_dung and e not in chon
            ]
            if ung_vien:
                e = ung_vien[0]
                chon.append(e)
                da_dung.add(e["id"])
                con_thieu -= 1
                lay_duoc_vong_nay = True
        if not lay_duoc_vong_nay:
            break  # hết competency chưa dùng ở mức này -> sang vòng 2

    # Vòng 2 — hết lựa chọn mới, chấp nhận lặp lại (ngẫu nhiên)
    while con_thieu > 0:
        chon.append(random.choice(entries_muc_do))
        con_thieu -= 1

    return chon


# ============================================================
# CN_BuildBlueprint
# ============================================================

def build_blueprint(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
) -> dict:
    # BƯỚC 1 — xác định phạm vi bài (CN_LoadExamScope)
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

    # BƯỚC 2 — số câu mỗi mức độ theo hệ số (bảng exam_rules.json)
    try:
        rules_result = resolve_cau_truc_de(loai_he_so, cau_truc_tu_hoc_sinh)
    except ExamRulesError as e:
        raise BlueprintError(str(e))
    phan_bo_muc_do = rules_result["phan_bo_muc_do"]

    # BƯỚC 3 — đọc Curriculum đúng phạm vi bài (CN_LoadCurriculum),
    # group theo (chương, MucDo)
    try:
        curriculum_entries = load_curriculum_for_scope(lop, pham_vi_bai)
    except CurriculumError as e:
        raise BlueprintError(f"CURRICULUM_NOT_FOUND: {e}")
    if not curriculum_entries:
        raise BlueprintError("CURRICULUM_NOT_FOUND")

    theo_chuong_muc_do: dict[tuple, list[dict]] = {}
    for e in curriculum_entries:
        key = (int(e["chuong_so"]), e["MucDo"])
        theo_chuong_muc_do.setdefault(key, []).append(e)

    # "chưa dùng" tách riêng theo loại câu (MC/SA/TL không đụng nhau)
    da_dung: dict[str, set] = {"trac_nghiem": set(), "tra_loi_ngan": set(), "tu_luan": set()}
    blueprint = {"dung_sai": [], "trac_nghiem": [], "tra_loi_ngan": [], "tu_luan": []}
    bao_cao_phan_bo: dict = {}

    # ---- TF (Đúng/Sai) — theo chương, KHÔNG qua Curriculum (Ngoại lệ 1, doc 04) ----
    so_cau_lon = phan_bo_muc_do.get("dung_sai_cau_lon", {}).get("NB", 0)  # 4 mức bằng nhau
    phan_bo_chuong_ds = _chon_chuong_dung_sai(so_bai_theo_chuong, so_cau_lon)
    bao_cao_phan_bo["dung_sai_cau_lon"] = phan_bo_chuong_ds
    for chuong_so, sl in phan_bo_chuong_ds.items():
        blueprint["dung_sai"].append({"chuong_so": chuong_so, "so_cau": sl})

    # ---- trac_nghiem: NB, TH (không giới hạn số câu/chương) ----
    for muc_do in ("NB", "TH"):
        so_luong = phan_bo_muc_do.get("trac_nghiem", {}).get(muc_do, 0)
        phan_bo_chuong = _chia_theo_so_bai(so_luong, so_bai_theo_chuong)
        for chuong_so, sl in phan_bo_chuong.items():
            entries = theo_chuong_muc_do.get((chuong_so, muc_do), [])
            chon = _chon_curriculum_id(entries, sl, da_dung["trac_nghiem"])
            for e in chon:
                blueprint["trac_nghiem"].append({
                    "curriculum_id": e["id"],
                    "chuong_so": chuong_so,
                    "muc_do": muc_do,
                    "tong_so_cau": 1,
                })

    # ---- trac_nghiem / tra_loi_ngan / tu_luan mức VD (+VDC dùng chung
    # curriculum_id mức VD — Ngoại lệ 2, doc 04) ----
    gioi_han_theo_loai = {
        "trac_nghiem": None,
        "tra_loi_ngan": MAX_SA_PER_CHUONG,
        "tu_luan": MAX_TL_PER_CHUONG,
    }
    for loai_cau, cap in gioi_han_theo_loai.items():
        so_vd = phan_bo_muc_do.get(loai_cau, {}).get("VD", 0)
        so_vdc = phan_bo_muc_do.get(loai_cau, {}).get("VDC", 0)
        if so_vd <= 0 and so_vdc <= 0:
            continue

        phan_bo_chuong_vdvdc = _phan_bo_vd_vdc(danh_sach_chuong, so_vd, so_vdc, max_per_chuong=cap)
        bao_cao_phan_bo.setdefault(loai_cau, {})["vd_vdc"] = phan_bo_chuong_vdvdc

        for chuong_so, v in phan_bo_chuong_vdvdc.items():
            tong = v["vd"] + v["vdc"]
            if tong <= 0:
                continue

            entries_vd = theo_chuong_muc_do.get((chuong_so, "VD"), [])
            chon = _chon_curriculum_id(entries_vd, tong, da_dung[loai_cau])

            # Gộp theo curriculum_id (nếu vòng lặp bên trên phải lặp lại
            # 1 competency do hết lựa chọn khác), rồi chia VD/VDC theo
            # chỉ tiêu còn lại — curriculum_id GIỮ NGUYÊN, không đổi thành VDC.
            dem = Counter(e["id"] for e in chon)
            vdc_con, vd_con = v["vdc"], v["vd"]
            for curriculum_id, so_luong_id in dem.items():
                so_vdc_id = min(so_luong_id, vdc_con)
                vdc_con -= so_vdc_id
                so_vd_id = so_luong_id - so_vdc_id
                vd_con -= so_vd_id
                blueprint[loai_cau].append({
                    "curriculum_id": curriculum_id,
                    "chuong_so": chuong_so,
                    "muc_do": "VD",
                    "tong_so_cau": so_luong_id,
                    "so_cau_VD": so_vd_id,
                    "so_cau_VDC": so_vdc_id,
                })

    return {
        "pham_vi_bai": pham_vi_bai,
        "so_bai_theo_chuong": so_bai_theo_chuong,
        "cau_truc_tong_quat": rules_result["cau_truc_tong_quat"],
        "nguon_cau_truc": rules_result["nguon_cau_truc"],
        "bao_cao_phan_bo": bao_cao_phan_bo,
        **blueprint,
    }


def build_and_select(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
    cho_phep_thieu: bool = False,
) -> dict:
    """
    Ghép build_blueprint() + select_questions() (chế độ chính thức, theo
    curriculum_id) thành 1 bước — dùng cho luồng WF001 đầy đủ.

    cho_phep_thieu=True: chế độ NHÁP, dùng khi ngân hàng đề (Mapping/
    Python Generator) chưa đầy đủ — thiếu ở đâu sẽ đánh dấu "thieu": True
    trong danh_sach_generator_id thay vì dừng hẳn. KHÔNG dùng khi ra đề
    thật cho học sinh (xem question_selector_service.py).
    """
    blueprint = build_blueprint(
        lop=lop,
        loai_he_so=loai_he_so,
        ki_thi=ki_thi,
        pham_vi_chuong=pham_vi_chuong,
        cau_truc_tu_hoc_sinh=cau_truc_tu_hoc_sinh,
    )

    try:
        danh_sach_id = select_questions(lop=lop, blueprint=blueprint, cho_phep_thieu=cho_phep_thieu)
    except SelectorError as e:
        raise BlueprintError(str(e))

    blueprint["danh_sach_generator_id"] = danh_sach_id
    return blueprint