# -*- coding: utf-8 -*-
"""Các câu Đúng/Sai trong một đề phải nằm ở CÁC CHƯƠNG KHÁC NHAU.

Cô Lan chốt (nhắc lại 29/09/2026): "tôi có chốt đề câu đúng sai phải ở
2 chương khác nhau cơ mà".

Vì sao luật này từng bị mất: bản 2.38 (12/09/2026) đổi từ
_chon_chuong_dung_sai (chọn theo CHƯƠNG) sang _chon_bai_dung_sai (chọn
theo BÀI, xếp theo số tiết giảm dần) để làm đúng quy định "chia câu về
từng bài theo tỉ lệ số tiết". Nhưng bản mới xếp TẤT CẢ các bài trong
phạm vi chung một hàng, nên lấy N bài nhiều tiết nhất là rơi trúng cùng
một chương. Đo được 29/09/2026: đề giữa kỳ 1 và cuối kỳ 1 lớp 10 ra
30/30 đề đều có CẢ HAI câu Đúng/Sai ở chương 1 (bài 1 và bài 2), đề nào
cũng y hệt đề nào.

Lưu ý: CN_QuestionSelector chọn câu Đúng/Sai theo CHƯƠNG chứ không theo
bài (Ngoại lệ 1, docs/04_ID_STANDARD.md), nên chương mới là thứ quyết
định câu nào ra đề.
"""
import collections
import random

import pytest

from app.services.exam_blueprint_service import (
    _chon_bai_dung_sai,
    build_blueprint,
)

KI_THI = ["giua_ky_1", "cuoi_ky_1", "giua_ky_2", "cuoi_ky_2"]


def _chuong_cac_cau_dung_sai(blueprint) -> list[int]:
    chuong = []
    for item in blueprint.get("dung_sai", []):
        chuong += [item["chuong_so"]] * item["so_cau"]
    return chuong


@pytest.mark.parametrize("ki_thi", KI_THI)
@pytest.mark.parametrize("seed", range(6))
def test_de_giua_ky_cuoi_ky_khong_co_hai_cau_dung_sai_cung_chuong(ki_thi, seed):
    random.seed(seed)
    blueprint = build_blueprint(10, "HeSo2_HeSo3", ki_thi=ki_thi)
    chuong = _chuong_cac_cau_dung_sai(blueprint)
    assert chuong, "Đề %s không có câu Đúng/Sai nào" % ki_thi
    trung = [c for c, n in collections.Counter(chuong).items() if n > 1]
    assert not trung, (
        "Đề %s (seed %d): chương %s có TỚI %d câu Đúng/Sai. Phân bổ: %s"
        % (ki_thi, seed, trung,
           max(collections.Counter(chuong).values()),
           [(i["bai_id"], i["so_cau"]) for i in blueprint["dung_sai"]])
    )


def test_rai_moi_chuong_mot_cau_truoc_khi_quay_vong():
    """Chỉ được dùng lại một chương khi đã hết chương trong phạm vi."""
    tiet = {
        "L10_C1_B1": 8, "L10_C1_B2": 7,   # chương 1: hai bài nhiều tiết nhất
        "L10_C2_B4": 6, "L10_C2_B3": 3,
        "L10_C3_B5": 5,
    }
    # 1 câu -> bài nhiều tiết nhất
    assert _chon_bai_dung_sai(tiet, 1) == {"L10_C1_B1": 1}
    # 2 câu -> KHÔNG được lấy cả hai bài của chương 1
    hai = _chon_bai_dung_sai(tiet, 2)
    assert hai == {"L10_C1_B1": 1, "L10_C2_B4": 1}, hai
    # 3 câu -> đủ ba chương
    ba = _chon_bai_dung_sai(tiet, 3)
    assert sorted(ba) == ["L10_C1_B1", "L10_C2_B4", "L10_C3_B5"], ba
    # 4 câu -> hết chương mới quay vòng, và phải sang BÀI KHÁC của chương 1
    bon = _chon_bai_dung_sai(tiet, 4)
    assert bon.get("L10_C1_B2") == 1, bon
    assert bon.get("L10_C1_B1") == 1, bon
    assert sum(bon.values()) == 4


def test_van_uu_tien_bai_nhieu_tiet_trong_moi_chuong():
    """Sửa luật chương nhưng KHÔNG được bỏ quy định ưu tiên số tiết."""
    tiet = {"L10_C1_B1": 2, "L10_C1_B2": 9, "L10_C2_B3": 4}
    assert _chon_bai_dung_sai(tiet, 1) == {"L10_C1_B2": 1}
    assert _chon_bai_dung_sai(tiet, 2) == {"L10_C1_B2": 1, "L10_C2_B3": 1}


def test_bai_id_khong_doc_duoc_chuong_thi_van_chay_nhu_cu():
    """Bài không theo khuôn L<lớp>_C<chương>_B<bài> thì coi như một nhóm."""
    tiet = {"B1": 2, "B2": 6, "B3": 4}
    assert _chon_bai_dung_sai(tiet, 1) == {"B2": 1}
    assert _chon_bai_dung_sai(tiet, 2) == {"B2": 1, "B3": 1}
    assert _chon_bai_dung_sai(tiet, 4) == {"B2": 2, "B3": 1, "B1": 1}
