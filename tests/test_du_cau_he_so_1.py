# -*- coding: utf-8 -*-
"""Đề hệ số 1 phải ra ĐỦ số câu và ĐÚNG mức độ ma trận yêu cầu.

Vì sao có file này (28/09/2026): đề hệ số 1 chương 3 chỉ ra 5/12 câu mà
KHÔNG báo thiếu gì cả. Hai nguyên nhân:

1. Số câu chia về từng bài theo tỉ lệ số tiết, không kiểm tra bài đó trong
   Curriculum có yêu cầu nào ở mức độ đang xét không. Chương 3 chỉ có 1 yêu
   cầu mức NB (bài 5) và 1 yêu cầu mức VD (bài 6), nhưng bộ chia vẫn rải câu
   NB cho bài 6 và câu VD cho bài 5 -> những câu ấy rơi mất lặng lẽ.
2. Mỗi câu Đúng/Sai trừ 1 suất VD + 1 suất VDC của các phần khác.

Cô Lan chốt 28/09/2026: "cứ làm theo đúng mức độ là được, vì mức độ ảnh
hưởng điểm số - mức độ khác đi sẽ làm điểm số không phản ánh đúng cái người
kiểm tra mong muốn." Nên nay mỗi phần ra đúng số câu từng mức độ ma trận
ghi, và phần chia lệch bài được dồn về bài có yêu cầu.
"""
import collections
import random

import pytest

from app.services.exam_blueprint_service import (
    _don_ve_bai_co_cau,
    _don_vd_ve_bai_co_cau,
    build_blueprint,
)
from app.services.question_selector_service import select_questions

# Các chương lớp 10 đã có đủ hàm Python để bắt được đề hệ số 1.
CHUONG_DA_DU_HAM = [1, 2, 3, 8, 9]

# Ma trận hệ số 1 (doc 07): tổng 12 câu.
DOI_HOI = {
    "trac_nghiem": 6,
    "dung_sai_cau_lon": 1,
    "tra_loi_ngan": 2,
    "tu_luan": 3,
}


@pytest.mark.parametrize("chuong", CHUONG_DA_DU_HAM)
@pytest.mark.parametrize("seed", range(5))
def test_de_he_so_1_ra_du_cau(chuong, seed):
    random.seed(seed)
    blueprint = build_blueprint(10, "HeSo1", pham_vi_chuong=str(chuong))
    danh_sach = select_questions(10, blueprint)

    dem = collections.Counter(it.get("loai_cau") or "?" for it in danh_sach)
    for loai, can in DOI_HOI.items():
        assert dem.get(loai, 0) >= can, (
            "Chuong %d seed %d: phan %s chi ra %d/%d cau. "
            "Phan bo: %s"
            % (chuong, seed, loai, dem.get(loai, 0), can,
               blueprint.get("bao_cao_phan_bo"))
        )


@pytest.mark.parametrize("chuong", CHUONG_DA_DU_HAM)
def test_khong_mat_cau_lang_le(chuong):
    """Nếu có câu không xếp được vào bài nào thì PHẢI được ghi vào báo cáo."""
    for seed in range(5):
        random.seed(seed)
        blueprint = build_blueprint(10, "HeSo1", pham_vi_chuong=str(chuong))
        danh_sach = select_questions(10, blueprint)
        bao_cao = blueprint.get("bao_cao_phan_bo", {})
        thieu = sum(m["so_cau_mat"] for m in bao_cao.get("khong_du_yeu_cau", []))
        tong_doi = sum(DOI_HOI.values())
        assert len(danh_sach) + thieu >= tong_doi, (
            "Chuong %d seed %d: ra %d cau, bao thieu %d, ma tran doi %d "
            "-> co cau bien mat ma khong bao gi"
            % (chuong, seed, len(danh_sach), thieu, tong_doi)
        )


def test_don_ve_bai_co_cau_don_dung_cho():
    theo_bai = {("B5", "NB"): [{"id": "x"}]}
    # 2 câu chia cho B6 nhưng B6 không có yêu cầu NB nào
    phan_bo, mat = _don_ve_bai_co_cau({"B5": 1, "B6": 2}, theo_bai, "NB")
    assert phan_bo == {"B5": 3}
    assert mat == 0


def test_don_ve_bai_co_cau_mo_rong_ra_bai_chua_duoc_chia():
    theo_bai = {("B6", "NB"): [{"id": "x"}]}
    # cả phân bổ chỉ có B5, mà yêu cầu NB lại nằm ở B6 -> phải dồn sang B6
    phan_bo, mat = _don_ve_bai_co_cau(
        {"B5": 1}, theo_bai, "NB", danh_sach_bai=["B5", "B6"])
    assert phan_bo == {"B6": 1}
    assert mat == 0


def test_don_ve_bai_co_cau_bao_khi_ca_chuong_khong_co():
    phan_bo, mat = _don_ve_bai_co_cau(
        {"B5": 2}, {}, "VDC", danh_sach_bai=["B5", "B6"])
    assert phan_bo == {}
    assert mat == 2


def test_don_vd_ve_bai_co_cau():
    theo_bai = {("B6", "VD"): [{"id": "x"}]}
    phan_bo, mat = _don_vd_ve_bai_co_cau(
        {"B5": {"vd": 1, "vdc": 0}}, theo_bai, danh_sach_bai=["B5", "B6"])
    assert phan_bo == {"B6": {"vd": 1, "vdc": 0}}
    assert mat == 0


def test_don_vd_giu_quy_uoc_moi_bai_toi_da_1_vdc():
    theo_bai = {("B6", "VD"): [{"id": "x"}], ("B7", "VD"): [{"id": "y"}]}
    phan_bo, _mat = _don_vd_ve_bai_co_cau(
        {"B5": {"vd": 0, "vdc": 2}}, theo_bai, danh_sach_bai=["B5", "B6", "B7"])
    assert all(v["vdc"] <= 1 for v in phan_bo.values())
