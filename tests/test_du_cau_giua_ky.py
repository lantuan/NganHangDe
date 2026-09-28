# -*- coding: utf-8 -*-
"""Đề giữa kỳ (hệ số 2) phải ra ĐỦ câu và trải đều các chương.

Vì sao có file này (28/09/2026): cô Lan yêu cầu kiểm tra đường ra đề hệ
số 2 trước khi dùng. Chạy thử phát hiện ba lỗi:

1. Đề giữa kỳ 1 có phạm vi 8 bài thuộc 4 chương, nhưng 20 câu rơi HẾT
   vào chương 1 và chương 2; chương 3 và chương 4 không có câu nào.
   Do _chia_theo_so_tiet dồn phần dư theo thứ tự (-số tiết, tên) - lần
   nào cũng cùng thứ tự - nên hai bài nhiều tiết nhất thắng ở MỌI loại
   câu. Đã đổi sang chia theo PHẦN DƯ LỚN NHẤT, bài bằng phần dư thì bốc
   ngẫu nhiên.

2. Bước dồn câu khi bài không có yêu cầu ở mức độ đang xét lại dồn cho
   bài đang nhiều câu nhất - luôn là bài của chương đầu - nên chương 1
   chiếm 62% số câu dù chỉ chiếm 36% số tiết. Đã đổi sang chia lại theo
   tỉ lệ số tiết trên những bài thật sự có yêu cầu.

3. Khối VD/VDC chỉ dồn trong đám bài ĐÃ CÓ trong phân bổ. Đề giữa kỳ 1
   có bốn bài mang yêu cầu mức VD nhưng phân bổ chỉ chạm tới một bài,
   nên bốn câu trả lời ngắn dồn hết về đó; mỗi bài tối đa MỘT câu VDC
   nên câu thứ tư rơi mất. Đo được: 3/20 đề chỉ ra 20 câu thay vì 21.
"""
import collections
import random

import pytest

from app.services.exam_blueprint_service import build_blueprint
from app.services.question_selector_service import select_questions

# Ma trận hệ số 2 (data/config/exam_rules.json): tổng 21 câu.
DOI_HOI = {
    "trac_nghiem": 12,
    "dung_sai_cau_lon": 2,
    "tra_loi_ngan": 4,
    "tu_luan": 3,
}

# Giữa kỳ 1 lớp 10 gồm chương 1, 2, 3 và bài 7-8 của chương 4 - tất cả
# đều đã có đủ hàm Python.
# 28/09/2026: xong chương 7 -> lớp 10 đủ hàm cho CẢ BỐN kỳ thi.
KI_THI_DA_DU_HAM = ["giua_ky_1", "cuoi_ky_1",
                    "giua_ky_2", "cuoi_ky_2"]


@pytest.mark.parametrize("ki_thi", KI_THI_DA_DU_HAM)
@pytest.mark.parametrize("seed", range(8))
def test_de_giua_ky_ra_du_cau(ki_thi, seed):
    random.seed(seed)
    blueprint = build_blueprint(10, "HeSo2_HeSo3", ki_thi=ki_thi)
    danh_sach = select_questions(10, blueprint)

    dem = collections.Counter(it.get("loai_cau") or "?" for it in danh_sach)
    for loai, can in DOI_HOI.items():
        assert dem.get(loai, 0) >= can, (
            "%s seed %d: phan %s chi ra %d/%d cau. Phan bo: %s"
            % (ki_thi, seed, loai, dem.get(loai, 0), can,
               blueprint.get("bao_cao_phan_bo"))
        )


@pytest.mark.parametrize("ki_thi", KI_THI_DA_DU_HAM)
def test_de_giua_ky_trai_deu_cac_chuong(ki_thi):
    """Không được để một chương trong phạm vi bị bỏ trắng hoàn toàn.

    Đây chính là lỗi đã bắt được: chương 3 và chương 4 không có câu nào
    trong suốt cả loạt đề.
    """
    dem_chuong = collections.Counter()
    for seed in range(12):
        random.seed(seed)
        blueprint = build_blueprint(10, "HeSo2_HeSo3", ki_thi=ki_thi)
        danh_sach = select_questions(10, blueprint)
        dem_chuong.update(it.get("chuong_so") for it in danh_sach)

    chuong_trong_pham_vi = set()
    for bai_id in blueprint.get("pham_vi_bai", []):
        chuong_trong_pham_vi.add(int(bai_id.split("_")[1][1:]))

    thieu = [c for c in chuong_trong_pham_vi if dem_chuong.get(c, 0) == 0]
    assert not thieu, (
        "Cac chuong %s nam trong pham vi de nhung khong ra duoc cau nao "
        "trong 12 de. Phan bo thuc te: %s" % (sorted(thieu), dict(dem_chuong))
    )


def test_khong_mat_cau_lang_le_o_de_giua_ky():
    """Câu không xếp được vào bài nào thì PHẢI được ghi vào báo cáo."""
    tong_doi = sum(DOI_HOI.values())
    for seed in range(8):
        random.seed(seed)
        blueprint = build_blueprint(10, "HeSo2_HeSo3", ki_thi="giua_ky_1")
        danh_sach = select_questions(10, blueprint)
        bao_cao = blueprint.get("bao_cao_phan_bo", {})
        thieu = sum(m["so_cau_mat"]
                    for m in bao_cao.get("khong_du_yeu_cau", []))
        assert len(danh_sach) + thieu >= tong_doi, (
            "seed %d: ra %d cau, bao thieu %d, ma tran doi %d -> co cau "
            "bien mat ma khong bao gi"
            % (seed, len(danh_sach), thieu, tong_doi)
        )
