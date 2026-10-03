"""Ma trận mức độ người dùng tự đặt (cô Lan 03/10/2026).

Yêu cầu: chọn 100% NB, TH thì MC, SA, TL KHÔNG được ra VD, VDC; Đúng/Sai giữ nguyên
cấu trúc 4 ý NB-TH-VD-VDC. Bộ chọn đúng sẵn; lỗi cũ là form giáo viên và nút
"Đồng ý, tạo đề" của chat không truyền tỉ lệ xuống.
"""
import re
from pathlib import Path

import pytest

from app.services.exam_rules_service import (
    ExamRulesError, _chia_theo_ty_le, chuan_hoa_ty_le, resolve_cau_truc_de)
from app.services.ma_tran_service import doc_ma_tran_tu_form, ma_tran_mac_dinh

GOC = Path(__file__).resolve().parents[1]
FORM = {"tuy_chinh_ma_tran": "1", "mc_so": "12", "mc_nb": "50", "mc_th": "50",
        "sa_so": "4", "sa_nb": "50", "sa_th": "50", "tl_so": "2", "tl_nb": "0", "tl_th": "100"}


def test_chuan_hoa_ty_le():
    assert chuan_hoa_ty_le({"NB": 50, "TH": 50}) == {"NB": .5, "TH": .5, "VD": 0, "VDC": 0}
    assert chuan_hoa_ty_le({"NB": .4, "TH": .3, "VD": .2, "VDC": .1})["VDC"] == pytest.approx(.1)
    with pytest.raises(ExamRulesError):
        chuan_hoa_ty_le({"NB": 50, "TH": 40})
    with pytest.raises(ExamRulesError):
        chuan_hoa_ty_le({"NB": 100, "XX": 0})


def test_muc_ty_le_0_khong_bao_gio_nhan_cau():
    for tong in range(1, 40):
        kq = _chia_theo_ty_le(tong, {"NB": .5, "TH": .5, "VD": 0, "VDC": 0}, True)
        assert kq["VD"] == kq["VDC"] == 0 and sum(kq.values()) == tong
        kq = _chia_theo_ty_le(tong, {"NB": .4, "TH": .3, "VD": .2, "VDC": .1}, True)
        assert sum(kq.values()) == tong
        assert all(abs(kq[m] - tong * t) < 1 for m, t in {"NB": .4, "TH": .3, "VD": .2, "VDC": .1}.items())


def test_bang_mac_dinh_khong_doi():
    kq = resolve_cau_truc_de("HeSo1")["phan_bo_muc_do"]
    assert kq["tra_loi_ngan"] == {"NB": 0, "TH": 0, "VD": 1, "VDC": 1}
    assert kq["dung_sai_cau_lon"] == {"NB": 1, "TH": 1, "VD": 1, "VDC": 1}


def test_doc_form():
    assert doc_ma_tran_tu_form({}) is None
    ct = doc_ma_tran_tu_form(FORM)
    assert set(ct) == {"trac_nghiem", "tra_loi_ngan", "tu_luan"}      # khong dong vao Dung/Sai
    assert ct["trac_nghiem"]["ty_le_muc_do"]["NB"] == .5
    with pytest.raises(ExamRulesError):
        doc_ma_tran_tu_form({**FORM, "mc_th": "40"})


def test_mac_dinh_dien_san_form():
    d = ma_tran_mac_dinh("HeSo1")
    assert d["tu_luan"]["so_y_moi_cau"] == 2 and d["trac_nghiem"]["ty_le_muc_do"]["NB"] == 40


def test_de_chi_NB_TH_khong_ra_VD():
    from app.services.exam_blueprint_service import build_and_select
    ct = doc_ma_tran_tu_form(FORM)
    for _ in range(12):
        r = build_and_select(10, "HeSo1", pham_vi_chuong="chuong_3", cau_truc_tu_hoc_sinh=ct, cho_phep_thieu=True)
        dem = {"trac_nghiem": 0, "tra_loi_ngan": 0, "tu_luan": 0, "dung_sai_cau_lon": 0}
        for c in r["danh_sach_generator_id"]:
            dem[c["loai_cau"]] += 1
            if c["loai_cau"] == "dung_sai_cau_lon":
                continue                                              # TF giu nguyen 4 y
            muc = [c.get("muc_do_cau") or c.get("muc_do")] + list(c.get("cac_muc_do", []))
            assert all(m in ("NB", "TH") for m in muc if m), c
            if c.get("generator_id"):
                assert re.search(r"_(NB|TH)\d+", c["generator_id"] + "_"), c["generator_id"]
        assert dem["trac_nghiem"] == 12 and dem["tra_loi_ngan"] == 4 and dem["dung_sai_cau_lon"] == 1


def test_form_va_chat_truyen_ty_le():
    ra_de = (GOC / "app/templates/teacher/ra_de.html").read_text(encoding="utf-8")
    assert "tuy_chinh_ma_tran" in ra_de and 'name="{{ tt }}_so"' in ra_de
    chat = (GOC / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert "ty_le_muc_do = ty" in chat
    teacher = (GOC / "app/routers/teacher.py").read_text(encoding="utf-8")
    assert "doc_ma_tran_tu_form" in teacher and "cau_truc_tu_hoc_sinh=cau_truc_tu_gv" in teacher
