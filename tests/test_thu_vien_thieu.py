# -*- coding: utf-8 -*-
"""Soat thu vien tren may chu: CHI cai goi thieu han, khong dung goi APT.

Vi sao co tep nay (29/09/2026): tren VPS chay dung lenh ma day.sh goi y

    python3 -m pip install --break-system-packages -r requirements.txt

thi dut giua chung:

    ERROR: Cannot uninstall urllib3 2.0.7, RECORD file not found.
           Hint: The package was installed by debian.

Ubuntu cai san urllib3 bang APT; goi APT khong co tep RECORD nen pip
khong go duoc. requirements.txt lai ghim urllib3==2.7.0 nen pip buoc
phai go ban cu -> dut ca lenh, cac goi dang sau khong duoc cai. Ma
nguon cua minh khong he import urllib3 truc tiep (chi la goi phu cua
requests) nen ep dung ban ghim vua vo ich vua nguy hiem.
"""
import subprocess
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "scripts"))

import thu_vien_thieu as tvt  # noqa: E402


def test_doc_duoc_requirements_that():
    yeu_cau = tvt.doc_yeu_cau()
    assert len(yeu_cau) > 20
    ten = [t for t, _ in yeu_cau]
    assert "num2words" in ten          # chuong 9 can, day.sh van kiem
    assert "urllib3" in ten            # chinh la goi gay dut lenh


def test_goi_chua_cai_thi_bao_THIEU(tmp_path):
    tep = tmp_path / "requirements.txt"
    tep.write_text("goi-khong-bao-gio-co-that==9.9.9\n", encoding="utf-8")
    thieu, lech = tvt.soat(tep)
    assert [t for t, _ in thieu] == ["goi-khong-bao-gio-co-that"]
    assert lech == []


def test_goi_LECH_BAN_khong_bi_coi_la_thieu(tmp_path):
    """Đây là điểm mấu chốt: urllib3 bản APT chỉ lệch bản, phải ĐỂ YÊN."""
    ban_that = tvt._ban_dang_co("pytest")
    assert ban_that, "moi truong test phai co pytest"
    tep = tmp_path / "requirements.txt"
    tep.write_text("pytest==0.0.1\n", encoding="utf-8")
    thieu, lech = tvt.soat(tep)
    assert thieu == [], "goi da cai roi thi KHONG duoc xui cai lai"
    assert lech == [("pytest", "0.0.1", ban_that)]


def test_ten_goi_co_gach_ngang_hay_gach_duoi_deu_nhan_ra(tmp_path):
    tep = tmp_path / "requirements.txt"
    tep.write_text("typing_extensions\ntyping-extensions\n", encoding="utf-8")
    thieu, _ = tvt.soat(tep)
    assert thieu == [], thieu


def test_bo_qua_dong_trong_va_dong_chu_thich(tmp_path):
    tep = tmp_path / "requirements.txt"
    tep.write_text("\n# chu thich\n   \npytest\n", encoding="utf-8")
    assert [t for t, _ in tvt.doc_yeu_cau(tep)] == ["pytest"]


def test_chay_duoc_tu_dong_lenh():
    kq = subprocess.run(
        [sys.executable, str(GOC / "scripts" / "thu_vien_thieu.py")],
        capture_output=True, text=True, timeout=120)
    assert kq.returncode in (0, 1), kq.stderr
    assert "python dang soat" in kq.stdout


def test_day_sh_KHONG_con_xui_chay_ca_requirements():
    """Lệnh -r requirements.txt là thứ làm đứt việc cài trên VPS."""
    noi_dung = (GOC / "scripts" / "day.sh").read_text(encoding="utf-8")
    for dong in noi_dung.splitlines():
        khong_chu_thich = dong.split("#", 1)[0]
        if "pip install" in khong_chu_thich and "requirements.txt" in khong_chu_thich:
            pytest.fail(
                "day.sh còn xui cài cả requirements.txt - lệnh đó đứt giữa "
                "chừng trên VPS vì urllib3 do APT cài:\n    %s" % dong.strip()
            )


def test_day_sh_co_goi_tep_soat_thu_vien():
    noi_dung = (GOC / "scripts" / "day.sh").read_text(encoding="utf-8")
    assert "thu_vien_thieu.py" in noi_dung
