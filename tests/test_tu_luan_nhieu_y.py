# -*- coding: utf-8 -*-
r"""Câu TỰ LUẬN hai ý thuộc HAI đơn vị kiến thức của cùng một chương (cô Lan
30/09/2026) - Ngoại lệ 3, docs/04:

- ID ghi cả hai đơn vị theo thứ tự ý a) -> ý b), không ghi bài (như câu Đúng/Sai):
  L10_C3_TH031_TH032_TL_A = ý a) TH031 (Bài 5), ý b) TH032 (Bài 6).
- Ma trận tính theo TỪNG Ý: câu chiếm một suất tự luận cho mỗi ý, ở đúng mức
  độ của ý đó; điểm phần tự luận chia theo suất.
- Hai đơn vị phải nằm trong phạm vi bài của đề.
"""
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC / "data" / "python_bank" / "toan10"))

from app.services import diem_service  # noqa: E402
from app.services.mapping_service import cac_y_tu_luan, so_suat_tu_luan, load_mapping  # noqa: E402
from app.services.question_selector_service import select_questions  # noqa: E402

B5_B6 = ["L10_C3_B5", "L10_C3_B6"]


def _bp(tl, pham_vi=B5_B6):
    return {"pham_vi_bai": pham_vi, "dung_sai": [], "trac_nghiem": [], "tra_loi_ngan": [], "tu_luan": tl}


def _suat(cid, md="TH"):
    return {"curriculum_id": cid, "chuong_so": 3, "muc_do": md, "tong_so_cau": 1}


def test_doc_id_nhieu_y():
    assert cac_y_tu_luan("L10_C3_TH031_TH032_TL_A") == [("TH", "031"), ("TH", "032")]
    assert cac_y_tu_luan("L10_C3_TH031_TH032_TL_A_01") == [("TH", "031"), ("TH", "032")]
    assert cac_y_tu_luan("L10_C1_NB017_TH018_TL_A") == [("NB", "017"), ("TH", "018")]
    assert cac_y_tu_luan("L10_C3_B6_TH032_TL_A") is None
    assert cac_y_tu_luan("L10_C3_TF_A") is None
    assert so_suat_tu_luan("L10_C3_TH031_TH033_TL_A") == 2
    assert so_suat_tu_luan("L10_C3_B6_TH032_TL_A") == 2
    assert so_suat_tu_luan("L10_C3_B6_VD036_TL_A") == 2


def test_hai_suat_TH_thi_chon_cau_hai_y():
    for sd in range(30):
        random.seed(sd)
        kq = select_questions(10, _bp([_suat("L10_C3_B5_TH031"), _suat("L10_C3_B6_TH033")]))
        tl = [c for c in kq if c["loai_cau"] == "tu_luan"]
        assert len(tl) == 1, tl
        c = tl[0]
        assert cac_y_tu_luan(c["generator_id"]), c
        assert c["so_suat"] == 2 and c["cac_muc_do"] == ["TH", "TH"]
        assert c["cac_curriculum_id"][0] == "L10_C3_B5_TH031"


def test_mot_suat_thi_khong_dung_cau_hai_y():
    for sd in range(30):
        random.seed(sd)
        kq = select_questions(10, _bp([_suat("L10_C3_B6_TH032")]))
        tl = [c for c in kq if c["loai_cau"] == "tu_luan"]
        assert len(tl) == 1 and cac_y_tu_luan(tl[0]["generator_id"]) is None, tl


def test_khac_muc_do_thi_khong_ghep():
    """Một suất TH và một suất VD: câu TH + TH không được lấp (sai % mức độ)."""
    for sd in range(20):
        random.seed(sd)
        bp = _bp([_suat("L10_C3_B5_TH031"),
                  {"curriculum_id": "L10_C3_B6_VD036", "chuong_so": 3, "muc_do": "VD",
                   "tong_so_cau": 1, "so_cau_VD": 1, "so_cau_VDC": 0}])
        kq = select_questions(10, bp)
        assert all(cac_y_tu_luan(c["generator_id"] or "") is None for c in kq)


def test_don_vi_ngoai_pham_vi_bai_thi_khong_ghep():
    """Đề chỉ kiểm tra Bài 5: không được ra ý b) của Bài 6."""
    for sd in range(20):
        random.seed(sd)
        kq = select_questions(10, _bp([_suat("L10_C3_B5_TH031"), _suat("L10_C3_B5_TH030")],
                                      pham_vi=["L10_C3_B5"]))
        assert all(cac_y_tu_luan(c["generator_id"] or "") is None for c in kq)


def test_diem_tu_luan_chia_theo_suat():
    de = [{"so_thu_tu": 1, "loai_cau": "TL", "generator_id": "L10_C3_TH031_TH032_TL_A"},
          {"so_thu_tu": 2, "loai_cau": "TL", "generator_id": "L10_C3_B6_TH032_TL_A"}]
    t = diem_service.tinh_thang_diem(de)
    assert t["theo_phan"]["TL"]["so_cau"] == 2 and t["theo_phan"]["TL"]["so_suat"] == 4
    assert diem_service.diem_toi_da_cua_cau_theo_id(t, "TL", de[0]["generator_id"]) == 1.5
    assert diem_service.diem_toi_da_cua_cau_theo_id(t, "TL", de[1]["generator_id"]) == 1.5
    assert "2 câu, 4 ý" in diem_service.mo_ta_thang_diem(t)


def test_ham_sinh_cau_nhieu_y_chay_va_co_du_y():
    import L10_C3 as m
    ids = [r["id"] for r in load_mapping(10, 3) if cac_y_tu_luan(r["id"])]
    assert len(ids) >= 3
    for gid in ids:
        ham = [getattr(m, n) for n in dir(m) if re.match(r"^%s_\d{2}$" % gid, n)]
        assert ham, gid
        for f in ham:
            for sd in range(20):
                random.seed(sd)
                t = f(1)
                assert t.count(r"\item") >= 2 * len(cac_y_tu_luan(gid)), (gid, t)


def test_mac_dinh_moi_cau_tu_luan_vd_gom_y_a_vd_y_b_vdc():
    """Hệ số 1 mặc định: 3 câu tự luận = 6 ý; mỗi câu ý a) VD, ý b) VDC."""
    from app.services.exam_blueprint_service import build_blueprint
    for chuong in (1, 3, 6):
        for sd in range(5):
            random.seed(sd)
            bp = build_blueprint(10, "HeSo1", pham_vi_chuong=str(chuong))
            assert sum(x["tong_so_cau"] for x in bp["tu_luan"]) == 6
            kq = select_questions(10, bp)
            tl = [c for c in kq if c["loai_cau"] == "tu_luan"]
            assert len(tl) == 3, (chuong, sd, tl)
            assert all(c.get("cac_muc_do") == ["VD", "VDC"] for c in tl), tl
            assert sum(so_suat_tu_luan(c["generator_id"]) for c in tl) == 6


def test_thu_tu_chon_dung_sai_tu_luan_roi_moi_mc_sa():
    """Blueprint chia đơn vị cho TỰ LUẬN trước MC, SA: gọi hàm chọn curriculum
    theo thứ tự tu_luan -> trac_nghiem -> tra_loi_ngan."""
    import app.services.exam_blueprint_service as B
    thu_tu = []
    goc = B._chon_curriculum_id

    def ghi(entries, so_luong, da_dung, dem_dung):
        kq = goc(entries, so_luong, da_dung, dem_dung)
        thu_tu.append(entries[0]["id"] if entries else None)
        return kq
    B._chon_curriculum_id = ghi
    try:
        random.seed(0)
        bp = B.build_blueprint(10, "HeSo1", pham_vi_chuong="3")
    finally:
        B._chon_curriculum_id = goc
    assert bp["tu_luan"] and bp["trac_nghiem"]
    # lượt đầu tiên gọi cho tự luận (mức VD của chương 3 chỉ có VD036)
    assert "VD036" in thu_tu[0], thu_tu
