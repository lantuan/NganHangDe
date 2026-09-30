# -*- coding: utf-8 -*-
r"""Dạng câu VẬN DỤNG CAO (cô Lan 30/09/2026).

Curriculum chỉ có mức VD (Ngoại lệ 2, doc 04) nên ID của dạng VDC vẫn mang VD
(L10_C3_B6_VD036_MC_F). Dòng Mapping đánh dấu "muc_do_dang": "VDC"; bộ chọn câu
lấy các suất VDC trong những dạng này TRƯỚC, suất VD lấy trong dạng còn lại.
MC/SA/TL cùng một bối cảnh ghi cùng mô tả "Dang" để không ra chung một đề.
"""
import json
import random

from app.services.mapping_service import load_mapping
from app.services.question_selector_service import select_questions


def _bp(mc=None, sa=None, tl=None):
    return {"pham_vi_bai": ["L10_C3_B6"], "dung_sai": [], "trac_nghiem": mc or [],
            "tra_loi_ngan": sa or [], "tu_luan": tl or []}


def _vd(vd, vdc):
    return {"curriculum_id": "L10_C3_B6_VD036", "chuong_so": 3, "muc_do": "VD",
            "tong_so_cau": vd + vdc, "so_cau_VD": vd, "so_cau_VDC": vdc}


def _vdc_ids(loai):
    return {r["id"] for r in load_mapping(10, 3) if r.get("muc_do_dang") == "VDC" and loai in r["Loai"]}


def test_mapping_danh_dau_vdc_hop_le():
    for f in ("toan10", "toan11", "toan12"):
        import glob
        for p in glob.glob("data/mapping/%s/*.json" % f):
            for r in json.load(open(p, encoding="utf-8")):
                if "muc_do_dang" in r:
                    assert r["muc_do_dang"] in ("VD", "VDC"), r["id"]
                    assert "_VD" in r["id"], "%s: chi dang muc VD moi danh dau VDC" % r["id"]


def test_suat_vdc_lay_dang_vdc_truoc():
    vdc_mc = _vdc_ids("nhiều lựa chọn")
    assert "L10_C3_B6_VD036_MC_F" in vdc_mc
    for sd in range(40):
        random.seed(sd)
        kq = select_questions(10, _bp(mc=[_vd(2, 1)]))
        mc = [c for c in kq if c["loai_cau"] == "trac_nghiem"]
        assert len(mc) == 3
        vdc = [c for c in mc if c["muc_do_cau"] == "VDC"]
        vd = [c for c in mc if c["muc_do_cau"] == "VD"]
        assert len(vdc) == 1 and vdc[0]["generator_id"] in vdc_mc
        assert all(c["generator_id"] not in vdc_mc for c in vd)


def test_mc_sa_tl_cung_boi_canh_cung_mo_ta():
    rows = [r for r in load_mapping(10, 3) if r.get("Dang", "").startswith("Khinh khí cầu")]
    assert len({r["Dang"] for r in rows}) == 1 and all(r.get("muc_do_dang") == "VDC" for r in rows)
    assert {r["Loai"] for r in rows} == {"Trắc nghiệm nhiều lựa chọn", "Trả lời ngắn", "Tự luận"}
