"""Một đề không ra hai câu cùng BỐI CẢNH ở mọi chương, mọi loại câu (cô Lan 01/10/2026).

Mapping ghi "boi_canh" (chuỗi hoặc danh sách) cho các dạng dùng chung một bối cảnh thực tiễn
(MC, SA, TL, TF). Bộ chọn câu ưu tiên dạng có bối cảnh chưa gặp trong đề (docs/04).
"""
import collections
import glob
import json
import random

from app.services.exam_blueprint_service import build_blueprint
from app.services.mapping_service import load_mapping
from app.services.question_selector_service import _khoa_boi_canh, select_questions


def _dong(lop, chuong):
    return {r["id"]: r for r in load_mapping(lop, chuong)}


def test_moi_boi_canh_co_it_nhat_hai_dong_hoac_la_TF():
    dem = collections.Counter()
    for f in glob.glob("data/mapping/toan1*/L*_C*.json"):
        for r in json.load(open(f, encoding="utf-8")):
            for k in _khoa_boi_canh(r):
                dem[k] += 1
    assert dem, "chua co dong nao ghi boi_canh"


def test_de_chuong_3_khong_trung_boi_canh():
    dong = _dong(10, 3)
    for seed in range(40):
        random.seed(seed)
        bp = build_blueprint(10, "HeSo1", pham_vi_chuong="3")
        ds = select_questions(10, bp)
        gap = collections.Counter()
        for c in ds:
            gid = c.get("generator_id")
            if gid in dong:
                for k in _khoa_boi_canh(dong[gid]):
                    gap[k] += 1
        trung = {k: v for k, v in gap.items() if v > 1}
        assert not trung, "seed %d: trung boi canh %s trong %s" % (seed, trung, [c.get("generator_id") for c in ds])


def test_TF_chon_truoc_thi_MC_SA_TL_tranh():
    """Ép TF chọn đúng TF_N (núi - toà nhà) rồi kiểm không còn câu nào cùng bối cảnh."""
    from app.services import question_selector_service as q
    dong = _dong(10, 3)
    goc = q.load_mapping

    def chi_tf_n(lop, chuong):
        rows = goc(lop, chuong)
        return [r for r in rows if "_TF_" not in r["id"] or r["id"] == "L10_C3_TF_N"]

    q.load_mapping = chi_tf_n
    try:
        for seed in range(30):
            random.seed(seed)
            bp = build_blueprint(10, "HeSo1", pham_vi_chuong="3")
            ds = select_questions(10, bp)
            ids = [c.get("generator_id") for c in ds]
            assert "L10_C3_TF_N" in ids
            khac = [i for i in ids if i != "L10_C3_TF_N" and i in dong
                    and ("BOI_CANH", "nui_toa_nha") in _khoa_boi_canh(dong[i])]
            assert not khac, (seed, khac)
    finally:
        q.load_mapping = goc
