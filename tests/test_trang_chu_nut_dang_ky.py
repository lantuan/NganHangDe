# -*- coding: utf-8 -*-
"""Trang chu phai co loi vao DANG KY nhin thay ngay.

Co Lan 29/09/2026: "nhieu nguoi vao khong biet nut dang ky o dau".
Truoc do goc phai trang chu chi co MOT nut "Dang nhap"; nguoi chua co
tai khoan phai bam vao do roi moi tim thay dong chu nho "Chua co tai
khoan? Dang ky ngay" o cuoi trang dang nhap.

Bai kiem tra nay giu cho nut "Dang ky" khong bi ai go mat, va giu cho
no tro dung ve /register (trang chon Hoc sinh / Giao vien).
"""
import re
from pathlib import Path

import jinja2
import pytest

THU_MUC = Path(__file__).resolve().parents[1] / "app" / "templates"


def _dich(da_dang_nhap):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(THU_MUC)))
    return env.get_template("index.html").render(
        da_dang_nhap=da_dang_nhap, user_display_name="Lan")


def test_khach_thay_ca_dang_ky_va_dang_nhap():
    ra = _dich(False)
    assert "window.location.href='/register'" in ra, (
        "Trang chu thieu nut dan toi /register - nguoi moi khong biet "
        "dang ky o dau."
    )
    assert "window.location.href='/login'" in ra
    assert "Đăng ký" in ra and "Đăng nhập" in ra


def test_nut_dang_ky_dung_truoc_nut_dang_nhap():
    """Dang ky dung ben trai, Dang nhap ben phai - doc tu trai sang."""
    ra = _dich(False)
    assert ra.index("/register'") < ra.index("/login'"), (
        "Nut Dang ky phai dung TRUOC nut Dang nhap tren thanh tieu de."
    )


def test_da_dang_nhap_thi_khong_con_moi_dang_ky():
    ra = _dich(True)
    dau = ra.index("<header")
    cuoi = ra.index("</header>")
    tieu_de = ra[dau:cuoi]
    assert "/register'" not in tieu_de, (
        "Dang nhap roi ma thanh tieu de van moi Dang ky."
    )
    assert "Vào Chat" in tieu_de


def test_nut_to_giua_trang_moi_dang_ky_truoc():
    """Nut to nhat giua trang phai la "Dang ky ngay", khong phai dang nhap.

    Do la thu bat mat nhat; nguoi chua co tai khoan nhin vao day truoc.
    """
    ra = _dich(False)
    i = ra.index("<section")           # dau khoi hero
    j = ra.index("gioi-thieu\" class=")  # het khoi ba nut
    hero = ra[i:j]
    assert "Đăng ký ngay" in hero, "Khoi giua trang thieu nut Dang ky ngay."
    assert hero.index("/register'") < hero.index("/login'"), (
        "Trong khoi giua trang, nut Dang ky phai dung TRUOC nut Dang nhap."
    )
    # Ba nut trong hang nay di CUNG MOT KIEU: nen nhat, chu xanh, vien mo
    # - giong "Gioi thieu chi tiet" (co Lan chot 29/09/2026). Rieng hai
    # nut o goc phai tren cung moi la nut nen xanh.
    kieu = "bg-surface-container-low text-primary"
    for nhan in ("Đăng ký ngay", "Đăng nhập", "Giới thiệu chi tiết"):
        assert kieu in hero.split(nhan)[0][-500:], (
            "Nút '%s' trong hàng giữa trang phải đi cùng kiểu với các nút "
            "còn lại (nền nhạt, chữ xanh)." % nhan
        )
