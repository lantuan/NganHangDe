# -*- coding: utf-8 -*-
"""Trang dang ky GIAO VIEN phai co nut "Dang ky bang Google".

Co Lan 29/09/2026: "toi can trang dang ky cua giao vien cung co nut
dang ky bang gmail nhu ben hoc sinh".

Diem then chot ve BAO MAT: luong Google khong mang theo duoc ma moi, va
ma moi thi TUYET DOI khong duoc lot ra trinh duyet - no chi nam trong
.env tren VPS va chi may chu duoc kiem. Vi vay nut Google chi danh dau
mot DUONG DAN vo hai vao sessionStorage roi goi Google; dang nhap xong,
callback.html dua thang toi /toi-la-giao-vien de nguoi dung nhap ma moi
MOT lan, may chu kiem roi moi nang vai tro.

Bai kiem tra nay giu ba thu:
  1. Nut Google con do, va trang duoc cap khoa Supabase (thieu khoa thi
     nut chet lang, bam khong an).
  2. Khong co cho nao ghi ma moi vao bo nho trinh duyet.
  3. callback.html chi nhan duong dan trong danh sach cho phep - khong
     de ai sua sessionStorage thanh trang ngoai roi lua nguoi khac.
"""
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

GOC = Path(__file__).resolve().parents[1]
CLIENT = TestClient(app)


def _trang_gv():
    r = CLIENT.get("/register/teacher")
    assert r.status_code == 200
    return r.text


def test_co_nut_dang_ky_bang_google():
    html = _trang_gv()
    assert 'id="google-register-btn"' in html
    assert "Đăng ký bằng Google" in html


def test_trang_duoc_cap_khoa_supabase():
    """Thieu khoa thi createClient vang loi, nut bam khong an."""
    html = _trang_gv()
    assert "{{ supabase_url }}" not in html, "Jinja chua thay gia tri that"
    assert "createClient(" in html
    # Khoa anon that su da duoc dien (khong phai chuoi rong).
    m = re.search(r'createClient\(\s*"([^"]*)"', html)
    assert m and m.group(1).strip(), "supabase_url dang rong"


def test_ma_moi_khong_bi_ghi_vao_bo_nho_trinh_duyet():
    """Ma moi chi duoc go vao o nhap roi gui thang len may chu."""
    html = _trang_gv()
    for xau in ("setItem('nhd_ma_moi", 'setItem("nhd_ma_moi',
                "localStorage", "ma_moi')", 'ma_moi")'):
        assert xau not in html, (
            "Trang dang ky giao vien dang dinh ghi ma moi vao bo nho "
            "trinh duyet (%s) - khong duoc phep." % xau
        )
    # Chi duoc luu duong dan dieu huong.
    assert "sessionStorage.setItem('nhd_sau_dang_nhap', '/toi-la-giao-vien')" in html


def test_callback_chi_nhan_duong_dan_trong_danh_sach():
    cb = (GOC / "app" / "templates" / "auth" / "callback.html").read_text(
        encoding="utf-8")
    assert "CHO_PHEP" in cb and "'/toi-la-giao-vien'" in cb
    assert "CHO_PHEP.indexOf(luu) !== -1" in cb, (
        "callback.html phai loc duong dan truoc khi chuyen trang, "
        "khong thi thanh lo hong chuyen huong."
    )


def test_trang_hoc_sinh_van_con_nut_google():
    r = CLIENT.get("/register/student")
    assert r.status_code == 200
    assert 'id="google-register-btn"' in r.text
