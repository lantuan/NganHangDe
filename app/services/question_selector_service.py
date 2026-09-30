"""
CN_QuestionSelector

Chọn Generator ID cuối cùng, dựa trên Blueprint (đã có curriculum_id cho
MC/SA/TL, chuong_so cho TF) + Mapping. Đây là node DUY NHẤT chọn Generator
ID cuối cùng — không có AI nào tham gia bước này (doc 08_CODE_NODES.md).

File này có 2 chế độ:

1. select_questions(lop, blueprint, cho_phep_thieu=False)
   Chế độ CHÍNH THỨC, dùng trong WF001 (build_and_select). Khớp Mapping
   theo đúng curriculum_id do CN_BuildBlueprint chọn.

   cho_phep_thieu=False (mặc định, dùng khi ra đề THẬT cho học sinh):
   thiếu Mapping ở đâu -> dừng ngay, báo lỗi SelectorError.

   cho_phep_thieu=True (chế độ NHÁP, dùng khi ngân hàng đề chưa đầy đủ):
   thiếu Mapping ở đâu -> chèn 1 mục "thieu": True vào kết quả (không
   dừng), để CN_ExamAssembler tự in ra placeholder trong PDF và tiếp
   tục sinh phần còn lại. KHÔNG dùng chế độ này khi phát đề thật.

2. select_questions_by_level(lop, yeu_cau)
   Chế độ THỦ CÔNG — giữ lại để test/debug nhanh qua API
   /api/exam/select-questions khi muốn chỉ định thẳng
   (chuong_so, loai_cau, muc_do, so_luong) mà KHÔNG cần đi qua Curriculum.
   Không dùng trong luồng WF001 chính thức.
"""

import random
from collections import Counter
import re

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


def _xoay_vong_bien_the(candidates: list[dict], so_luong: int, da_dung_id: set,
                        dang_da_dung: set | None = None) -> list[dict]:
    """
    Chọn so_luong Generator ID trong candidates (các phiên bản A/B/C của
    cùng 1 curriculum_id + loại câu). Ưu tiên phiên bản CHƯA dùng trong
    đề hiện tại (da_dung_id) để tăng đa dạng — xoay vòng thay vì random
    thuần. Hết phiên bản khác mới dùng lại (cho phép lặp).
    """
    if not candidates:
        return []

    # SỬA 30/09/2026 (cô Lan): hết dạng chưa dùng thì lấy dạng DÙNG ÍT NHẤT
    # trong đề (vd chỉ có A, B mà cần 3 câu thì ra A, B rồi A hoặc B - không
    # bao giờ A, A, A). Số lần dùng đếm trong _DEM_DANG gắn với da_dung_id.
    dem = _DEM_DANG.setdefault(id(da_dung_id), Counter())
    chon = []
    for _ in range(so_luong):
        chua_dung = [c for c in candidates if c["id"] not in da_dung_id]
        if dang_da_dung is not None:
            # Uu tien dang ma MO TA ("Dang" trong Mapping) chua gap o loai cau khac
            # cua cung don vi (vd VD014_MC_A va VD014_SA_A cung "Menh de chua bien"
            # thi ra hai cau gan nhu giong het).
            khac_mo_ta = [c for c in chua_dung if _khoa_mo_ta(c) not in dang_da_dung]
            chua_dung = khac_mo_ta or chua_dung
        if chua_dung:
            item = random.choice(chua_dung)
        else:
            it_nhat = min(dem[c["id"]] for c in candidates)
            item = random.choice([c for c in candidates if dem[c["id"]] == it_nhat])
        chon.append(item)
        da_dung_id.add(item["id"])
        dem[item["id"]] += 1
        if dang_da_dung is not None:
            dang_da_dung.add(_khoa_mo_ta(item))

    return chon


def _khoa_mo_ta(row: dict) -> tuple:
    """(đơn vị kiến thức, mô tả dạng đã chuẩn hoá) của một dòng Mapping."""
    g = _CURRICULUM_TU_GENERATOR.match(row.get("id", ""))
    dv = _don_vi(g.group(1)) if g else row.get("id", "")
    return dv, " ".join(str(row.get("Dang", "")).lower().split())


# Đếm số lần mỗi dạng (Generator ID) đã được chọn, theo từng tập da_dung_id
# của một lần chọn đề (khoá = id() của tập). select_questions xoá khi xong.
_DEM_DANG: dict[int, Counter] = {}


_CURRICULUM_TU_GENERATOR = re.compile(r"^(L\d+_C\d+_B\d+_(NB|TH|VD|VDC)\d+[A-Z]?)_(MC|SA|TL)_[A-Z]+$")
_DON_VI = re.compile(r"_(?:NB|TH|VD|VDC)(\d+[A-Z]?)$")


def _don_vi(curriculum_id: str) -> str:
    """L10_C1_B1_TH014 -> L10_C1_B1_014 (bỏ mức độ, như exam_blueprint_service)."""
    return _DON_VI.sub(lambda m: "_" + m.group(1), curriculum_id)


def _thay_don_vi_khac(curriculum_id: str, loai_cau: str, mapping: list[dict],
                      dem_don_vi: Counter) -> tuple[str, list[dict]] | None:
    """Curriculum ID được chia chưa có dạng nào cho loại câu này trong Mapping:
    đổi sang một đơn vị kiến thức KHÁC của CÙNG bài, CÙNG mức độ có dạng cho
    loại câu đó - ưu tiên đơn vị chưa dùng / dùng ít nhất trong đề.

    Cô Lan 30/09/2026: "lọc trong toàn bộ TH của bài 1 ... phải chọn SA khác
    014 (trừ khi đã chọn hết)". Không có đơn vị nào thay được thì trả None.
    """
    m = re.match(r"^(L\d+_C\d+_B\d+_)(NB|TH|VD|VDC)\d+[A-Z]?$", curriculum_id)
    if not m:
        return None
    theo_cid: dict[str, list[dict]] = {}
    for row in mapping:
        g = _CURRICULUM_TU_GENERATOR.match(row["id"])
        if not g or phan_loai_cau(row) != loai_cau:
            continue
        cid = g.group(1)
        if cid.startswith(m.group(1) + m.group(2)) and re.match(r"^\d", cid[len(m.group(1) + m.group(2)):]):
            theo_cid.setdefault(cid, []).append(row)
    if not theo_cid:
        return None
    it_nhat = min(dem_don_vi[_don_vi(c)] for c in theo_cid)
    cid = random.choice([c for c in theo_cid if dem_don_vi[_don_vi(c)] == it_nhat])
    return cid, theo_cid[cid]


def _muc_placeholder(chuong_so: int, loai_cau: str, muc_do, curriculum_id: str | None,
                     ghi_chu: str, thieu_o: str = "mapping", ma_thieu: str | None = None) -> dict:
    """
    Mục kết quả dùng khi câu hỏi chưa có sẵn.

    KHÔNG coi đây là lỗi: ngân hàng đề được xây dần, nên chỗ nào chưa có thì
    ghi rõ THIẾU Ở ĐÂU và MÃ NÀO để giáo viên bổ sung, rồi vẫn ra đề tiếp.

    thieu_o : "mapping" — chưa khai dạng câu hỏi nào cho yêu cầu cần đạt này
              "python"  — đã có dạng trong Mapping nhưng chưa viết hàm sinh
    ma_thieu: mã cần bổ sung (Curriculum ID hoặc Generator ID)
    """
    return {
        "generator_id": None,
        "thieu": True,
        "thieu_o": thieu_o,
        "ma_thieu": ma_thieu or curriculum_id,
        "chuong_so": chuong_so,
        "curriculum_id": curriculum_id,
        "loai_cau": loai_cau,
        "muc_do": muc_do,
        "ghi_chu": ghi_chu,
    }


# ============================================================
# CHẾ ĐỘ CHÍNH THỨC — theo Blueprint (curriculum_id)
# ============================================================

def select_questions(lop: int, blueprint: dict, cho_phep_thieu: bool = True) -> list[dict]:
    """
    blueprint cần có các khoá: dung_sai, trac_nghiem, tra_loi_ngan, tu_luan
    đúng cấu trúc doc 03_DATA_STRUCTURE.md (mục Blueprint).

    cho_phep_thieu: xem docstring đầu file. Mặc định False (nghiêm ngặt).
    """
    cache: dict[int, list[dict]] = {}
    # da_dung tách riêng theo loại câu: cùng 1 curriculum_id vẫn có thể
    # được dùng cho cả MC lẫn TL trong cùng 1 đề (2 dạng câu khác nhau).
    da_dung: dict[str, set] = {
        "trac_nghiem": set(), "tra_loi_ngan": set(), "tu_luan": set(),
        "dung_sai_cau_lon": set(),
    }
    # đơn vị kiến thức đã dùng trong đề (chung cho MC / SA / TL)
    dem_don_vi: Counter = Counter()
    mo_ta_da_dung: set = set()
    for loai in ("trac_nghiem", "tra_loi_ngan", "tu_luan"):
        for item in blueprint.get(loai, []):
            dem_don_vi[_don_vi(item["curriculum_id"])] += item.get("tong_so_cau", 1)
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
            ma = f"L{lop}_C{chuong_so}_TF_A"
            ghi_chu = f"Chưa khai câu Đúng/Sai cho chương {chuong_so} trong Mapping."
            if cho_phep_thieu:
                for _ in range(so_luong):
                    ket_qua.append(_muc_placeholder(
                        chuong_so, "dung_sai_cau_lon", None, None, ghi_chu,
                        thieu_o="mapping", ma_thieu=ma))
                continue
            raise SelectorError(ghi_chu)

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
                # thử đơn vị kiến thức khác cùng bài, cùng mức độ có dạng câu này
                thay = _thay_don_vi_khac(curriculum_id, loai_cau, _mapping_chuong(chuong_so), dem_don_vi)
                if thay:
                    dem_don_vi[_don_vi(curriculum_id)] -= so_luong
                    curriculum_id, candidates = thay
                    dem_don_vi[_don_vi(curriculum_id)] += so_luong
            if not candidates:
                ma = f"{curriculum_id}_{LOAI_KY_HIEU[loai_cau]}_A"
                ghi_chu = f"Chưa khai dạng {LOAI_KY_HIEU[loai_cau]} nào cho {curriculum_id} trong Mapping."
                if cho_phep_thieu:
                    for _ in range(so_luong):
                        ket_qua.append(_muc_placeholder(
                            chuong_so, loai_cau, item.get("muc_do"), curriculum_id, ghi_chu,
                            thieu_o="mapping", ma_thieu=ma))
                    continue
                raise SelectorError(ghi_chu)

            chosen = _xoay_vong_bien_the(candidates, so_luong, da_dung[loai_cau], mo_ta_da_dung)
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

    # Sap xep lai theo dung thu tu Phan I/II/III/IV cua Phieu TLTN chuan
    # (Bo GD&DT) va mau de cua giao vien: MC -> TF -> SA -> TL. sorted() on
    # dinh (stable) nen khong xao tron thu tu trong cung 1 loai cau.
    _THU_TU_LOAI = {
        "trac_nghiem": 0,
        "dung_sai_cau_lon": 1,
        "tra_loi_ngan": 2,
        "tu_luan": 3,
    }
    for s in da_dung.values():
        _DEM_DANG.pop(id(s), None)
    return sorted(ket_qua, key=lambda c: _THU_TU_LOAI.get(c["loai_cau"], 99))


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