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
    """Chỉ được dùng lại một chương khi đã hết chương trong phạm vi.
    (Từ 29/09/2026 bài bốc NGẪU NHIÊN có trọng số - kiểm bằng nhiều seed.)"""
    tiet = {
        "L10_C1_B1": 8, "L10_C1_B2": 7,
        "L10_C2_B4": 6, "L10_C2_B3": 3,
        "L10_C3_B5": 5,
    }
    chuong = lambda kq: [b.split("_")[1] for b, n in kq.items() for _ in range(n)]
    for s in range(200):
        random.seed(s)
        hai = _chon_bai_dung_sai(tiet, 2)
        assert len(set(chuong(hai))) == 2, hai
        ba = _chon_bai_dung_sai(tiet, 3)
        assert sorted(set(chuong(ba))) == ["C1", "C2", "C3"], ba
        bon = _chon_bai_dung_sai(tiet, 4)
        assert sum(bon.values()) == 4 and max(bon.values()) == 1, bon


def test_van_uu_tien_bai_nhieu_tiet_trong_moi_chuong():
    """Chọn ngẫu nhiên nhưng KHÔNG bỏ quy định ưu tiên số tiết: bài nhiều
    tiết được chọn nhiều hơn (tính trên nhiều đề)."""
    tiet = {"L10_C1_B1": 2, "L10_C1_B2": 9, "L10_C2_B3": 4}
    dem = collections.Counter()
    for s in range(3000):
        random.seed(s)
        dem.update(_chon_bai_dung_sai(tiet, 1))
    assert dem["L10_C1_B2"] > dem["L10_C2_B3"] > dem["L10_C1_B1"] > 0, dem


def test_moi_de_khong_con_giong_het_nhau():
    """Cô Lan 29/09/2026: chia xong phải chọn ngẫu nhiên - không được đề nào
    cũng rơi đúng một bài."""
    tiet = {"L10_C1_B1": 4, "L10_C1_B2": 4, "L10_C2_B3": 2, "L10_C2_B4": 3}
    ket = set()
    for s in range(50):
        random.seed(s)
        ket.add(tuple(sorted(_chon_bai_dung_sai(tiet, 2))))
    assert len(ket) >= 3, ket
