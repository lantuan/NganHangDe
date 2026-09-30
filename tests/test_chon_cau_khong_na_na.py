# -*- coding: utf-8 -*-
r"""Quy tắc chọn câu để đề KHÔNG na ná nhau (cô Lan 30/09/2026).

Ví dụ của cô: mức TH của bài 1, ma trận có 5 MC, 1 SA, 1 TL.
1. Lọc trong toàn bộ yêu cầu TH của bài 1. Đơn vị 014 đã dùng cho MC (vì hết
   số khác) thì SA, TL phải lấy đơn vị KHÁC 014 - trừ khi đã hết.
2. Trong các câu cùng đơn vị 014: lấy các DẠNG khác nhau (A, B, D...). Chỉ có
   A, B mà cần 3 câu thì 2 câu A + 1 câu B, không bao giờ 3 câu A.
3. Hai câu cùng dạng A thì khác BIẾN THỂ (A_01 và A_04).
"""
import random
import sys
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from app.services.exam_blueprint_service import _chon_curriculum_id, build_blueprint  # noqa: E402
from app.services.question_selector_service import _xoay_vong_bien_the  # noqa: E402
from app.services.generator_service import _chon_bien_the  # noqa: E402


def _e(so):
    return {"id": "L10_C1_B1_TH%s" % so, "bai_so": 1}


def test_sa_tl_tranh_don_vi_mc_da_dung():
    for sd in range(50):
        random.seed(sd)
        da_dung, dem = set(), Counter()
        ds = [_e("003"), _e("014"), _e("015")]
        mc = _chon_curriculum_id(ds[:2], 3, da_dung, dem)          # MC chi co 003, 014
        sa = _chon_curriculum_id(ds, 1, da_dung, dem)               # SA con 015 chua dung
        assert sa[0]["id"].endswith("015"), (mc, sa)


def test_het_don_vi_thi_lap_don_vi_dung_it_nhat():
    for sd in range(50):
        random.seed(sd)
        da_dung, dem = set(), Counter()
        ds = [_e("003"), _e("014")]
        chon = _chon_curriculum_id(ds, 5, da_dung, dem)
        c = Counter(e["id"] for e in chon)
        assert sorted(c.values()) == [2, 3], c                     # khong don 4-1, 5-0


def test_trong_cung_don_vi_lay_dang_khac_nhau():
    ung_vien = [{"id": "L10_C1_B1_TH014_MC_A"}, {"id": "L10_C1_B1_TH014_MC_B"}]
    for sd in range(50):
        random.seed(sd)
        da_dung = set()
        chon = []
        for _ in range(3):                                         # blueprint goi tung cau mot
            chon += _xoay_vong_bien_the(ung_vien, 1, da_dung)
        c = Counter(x["id"] for x in chon)
        assert sorted(c.values()) == [1, 2], c                     # 2 A + 1 B, khong 3 A
    ba = ung_vien + [{"id": "L10_C1_B1_TH014_MC_D"}]
    random.seed(1)
    da_dung = set()
    chon = [x["id"] for _ in range(3) for x in _xoay_vong_bien_the(ba, 1, da_dung)]
    assert len(set(chon)) == 3


def test_cung_dang_thi_khac_bien_the():
    for sd in range(50):
        random.seed(sd)
        used = {}
        bt = [_chon_bien_the(["X_01", "X_02", "X_03", "X_04"], used, "X") for _ in range(2)]
        assert bt[0] != bt[1]
        used = {}
        bt = [_chon_bien_the(["X_01", "X_02"], used, "X") for _ in range(4)]
        assert sorted(Counter(bt).values()) == [2, 2]


def test_ma_tran_co_sa_tl_muc_th_khong_bi_bo_mat():
    """Trước 30/09/2026 câu SA, TL ở mức NB/TH bị bỏ mất khỏi đề."""
    ct = {"trac_nghiem": {"so_luong": 5, "ty_le_muc_do": {"NB": 0, "TH": 1, "VD": 0, "VDC": 0}},
          "tra_loi_ngan": {"so_luong": 1, "ty_le_muc_do": {"NB": 0, "TH": 1, "VD": 0, "VDC": 0}},
          "tu_luan": {"so_luong": 1, "ty_le_muc_do": {"NB": 0, "TH": 1, "VD": 0, "VDC": 0}},
          "dung_sai_cau_lon": {"so_luong": 0}}
    random.seed(0)
    bp = build_blueprint(lop=10, loai_he_so="HeSo1", pham_vi_chuong="1", cau_truc_tu_hoc_sinh=ct)
    assert sum(x["tong_so_cau"] for x in bp["trac_nghiem"]) == 5
    assert [x["muc_do"] for x in bp["tra_loi_ngan"]] == ["TH"]
    assert [x["muc_do"] for x in bp["tu_luan"]] == ["TH"]


def test_khong_chon_hai_dang_cung_mo_ta_o_hai_loai_cau():
    """VD014_MC_A va VD014_SA_A cung mo ta 'Menh de chua bien' (cung mot bai toan):
    MC da lay MC_A thi SA phai uu tien SA_B."""
    from app.services.question_selector_service import _xoay_vong_bien_the
    mo_ta = set()
    random.seed(0)
    _xoay_vong_bien_the([{"id": "L10_C1_B1_VD014_MC_A", "Dang": "Mệnh đề chưa biến"}], 1, set(), mo_ta)
    for sd in range(30):
        random.seed(sd)
        m = set(mo_ta)
        c = _xoay_vong_bien_the([{"id": "L10_C1_B1_VD014_SA_A", "Dang": "Mệnh đề chưa biến"},
                                 {"id": "L10_C1_B1_VD014_SA_B", "Dang": "Đếm số mệnh đề đúng"}], 1, set(), m)
        assert c[0]["id"].endswith("SA_B")


def test_bai_toan_hai_tap_khong_trung_boi_canh_trong_mot_ma_de():
    """Cô Lan 30/09/2026: các câu thực tế hai tập hợp trong cùng một đề không
    được trùng bối cảnh (generator_service gán _DE_HIEN_TAI.da_dung theo mã đề)."""
    from app.services.generator_service import call_generator
    ids = ["L10_C1_B2_VD020_TL_A", "L10_C1_B2_VD020_SA_A", "L10_C1_B2_VD020_MC_A",
           "L10_C1_B2_VD020_TL_A", "L10_C1_B2_VD020_MC_A", "L10_C1_B2_VD020_SA_A"]
    for sd in range(20):
        random.seed(sd)
        used = {}
        for g in ids:
            call_generator(generator_id=g, lop=10, chuong_so=1, role="teacher", socau_yeu_cau=1,
                           used_variants=used)
        # moi cau dung kho boi canh them dung mot boi canh moi (tru bien the ba tap hop)
        so_cau_hai_tap = len(used["__boi_canh__"])
        assert so_cau_hai_tap >= 4, used


def test_kho_boi_canh_so_lieu_hop_li():
    import sys as _s
    _s.path.insert(0, str(GOC / "data" / "python_bank"))
    from toan10 import L10_C1 as M
    for sd in range(300):
        random.seed(sd)
        chon = M._bo_chon_boi_canh()
        d = M._de_hai_tap(chon)
        assert 0 < d["nAB"] < min(d["nA"], d["nB"])
        assert d["khong"] >= 2 and d["nAuB"] <= d["N"]
        if d["bc"]["lop"]:
            assert d["N"] == 35


def test_tam_cau_hai_tap_trong_mot_de_la_tam_boi_canh_khac_nhau():
    import sys as _s
    _s.path.insert(0, str(GOC / "data" / "python_bank"))
    from toan10 import L10_C1 as M
    ham = [M.L10_C1_B2_VD020_TL_A_01, M.L10_C1_B2_VD020_TL_A_02, M.L10_C1_B2_VD020_SA_A_01,
           M.L10_C1_B2_VD020_SA_A_03, M.L10_C1_B2_VD020_MC_A_01, M.L10_C1_B2_VD020_MC_A_02,
           M.L10_C1_B2_VD020_MC_A_04, M.L10_C1_B2_VD020_TL_A_01, M.L10_C1_B2_VD020_MC_A_03,
           M.L10_C1_B2_VD020_SA_A_02]
    for sd in range(20):
        random.seed(sd)
        s = set()
        for f in ham:
            M._DE_HIEN_TAI.da_dung = s
            try:
                f(1)
            finally:
                M._DE_HIEN_TAI.da_dung = None
        assert len(s) == len(ham), s
