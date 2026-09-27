"""
Kiem tra quy uoc: CUNG mot don vi kien thuc thi CUNG so, chi khac muc do.

Y dinh cua giao vien khi dat quy uoc nay: neu mot de lay ca hai muc cua cung
mot don vi (vi du L10_C1_B2_TH021 va L10_C1_B2_VD021) thi hai cau se cung mot
dang toan, chi khac do kho -- hoc sinh nhin vao la thay trung. Vi vay thuat
toan dung blueprint phai coi hai ban ghi do la MOT, khong lay ca hai khi van
con lua chon khac.
"""

from app.services.exam_blueprint_service import (
    _don_vi_kien_thuc,
    _chon_curriculum_id,
)


def _entry(ma, bai_so, muc_do):
    return {"id": ma, "bai_so": bai_so, "MucDo": muc_do}


# ---------------------------------------------------------------- khoa

def test_bo_muc_do_khoi_ma():
    assert _don_vi_kien_thuc("L10_C1_B2_TH021") == "L10_C1_B2_021"
    assert _don_vi_kien_thuc("L10_C1_B1_NB001") == "L10_C1_B1_001"
    assert _don_vi_kien_thuc("L10_C6_B15_VDC090") == "L10_C6_B15_090"


def test_hai_muc_cung_so_cho_cung_mot_khoa():
    assert _don_vi_kien_thuc("L10_C1_B2_TH021") == _don_vi_kien_thuc("L10_C1_B2_VD021")
    assert _don_vi_kien_thuc("L10_C1_B1_TH014") == _don_vi_kien_thuc("L10_C1_B1_VD014")


def test_khac_so_thi_khac_khoa():
    """104 va 104A la HAI don vi kien thuc khac nhau, khong duoc gop."""
    assert _don_vi_kien_thuc("L10_C7_B19_VD104") != _don_vi_kien_thuc("L10_C7_B19_VD104A")


def test_ma_khong_dung_dinh_dang_thi_giu_nguyen():
    """Cau Dung/Sai ra theo chuong, khong co muc do -- khong duoc bien dang."""
    assert _don_vi_kien_thuc("L10_C1_TF_A") == "L10_C1_TF_A"


# ---------------------------------------------------------------- chon cau

def test_khong_lay_ca_hai_muc_cua_cung_mot_don_vi():
    """
    Da dung TH021 o muc thong hieu; sang muc van dung, con lua chon khac
    (VD020) thi phai lay VD020, khong duoc lay VD021.
    """
    da_dung = {_don_vi_kien_thuc("L10_C1_B2_TH021")}
    chon = _chon_curriculum_id(
        [_entry("L10_C1_B2_VD020", "2", "VD"), _entry("L10_C1_B2_VD021", "2", "VD")],
        1,
        da_dung,
    )
    assert [e["id"] for e in chon] == ["L10_C1_B2_VD020"]


def test_het_lua_chon_thi_van_phai_lay_du_so_cau():
    """
    Vong 2: khi khong con don vi nao chua dung, tha chap nhan lap con hon
    la tra ve thieu cau -- de van phai du so cau theo ma tran.
    """
    da_dung = {_don_vi_kien_thuc("L10_C1_B2_TH021")}
    chon = _chon_curriculum_id([_entry("L10_C1_B2_VD021", "2", "VD")], 2, da_dung)
    assert len(chon) == 2


def test_van_rai_deu_giua_cac_bai():
    """Khong dom het cau vao mot bai khi nhieu bai cung co lua chon."""
    chon = _chon_curriculum_id(
        [_entry("L10_C1_B1_NB001", "1", "NB"), _entry("L10_C1_B1_NB005", "1", "NB"),
         _entry("L10_C1_B2_NB017", "2", "NB")],
        2,
        set(),
    )
    assert len({e["bai_so"] for e in chon}) == 2
