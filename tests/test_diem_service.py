# -*- coding: utf-8 -*-
"""Kiem thu thang diem 10: MC 3d - TF 2d - SA 2d - TL 3d.

Chay: python3 tests/test_diem_service.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services import diem_service as ds


def de_mau(so_mc=12, so_tf=2, so_sa=3, so_tl=3):
    de, stt = [], 0
    for _ in range(so_mc):
        stt += 1
        de.append({"so_thu_tu": stt, "loai_cau": "MC", "generator_id": "L10_C1_B1_NB001_MC_A"})
    for _ in range(so_tf):
        stt += 1
        # TF hien bi answer_parser luu nham loai_cau='TL' -> test luon truong hop nay
        de.append({"so_thu_tu": stt, "loai_cau": "TL", "generator_id": "L10_C1_TF_A"})
    for _ in range(so_sa):
        stt += 1
        de.append({"so_thu_tu": stt, "loai_cau": "SA", "generator_id": "L10_C1_B1_VD014_SA_A"})
    for _ in range(so_tl):
        stt += 1
        de.append({"so_thu_tu": stt, "loai_cau": "TL", "generator_id": "L10_C1_B2_VD020_TL_A"})
    return de


def test_du_4_phan():
    t = ds.tinh_thang_diem(de_mau())
    assert t["diem_toi_da_tong"] == 10.0, t["diem_toi_da_tong"]
    assert t["diem_toi_da_tu_dong"] == 7.0
    assert t["theo_phan"]["MC"]["diem_moi_cau"] == 0.25
    assert t["theo_phan"]["TF"]["diem_moi_cau"] == 1.0
    assert t["theo_phan"]["TF"]["diem_moi_y"] == 0.25
    assert t["theo_phan"]["SA"]["diem_moi_cau"] == 0.67
    assert t["theo_phan"]["TL"]["diem_moi_cau"] == 1.0
    print("OK du 4 phan: tong 10, tu dong 7")


def test_cong_don_khong_lech():
    """3 cau SA x 0.67 phai ra dung 2.0 diem chu khong phai 2.01."""
    t = ds.tinh_thang_diem(de_mau())
    tong = sum(ds.diem_toi_da_cua_cau_goc(t, "SA") for _ in range(3))
    assert round(tong, 2) == 2.0, tong
    tong_het = (
        12 * ds.diem_toi_da_cua_cau_goc(t, "MC")
        + 2 * ds.diem_toi_da_cua_cau_goc(t, "TF")
        + 3 * ds.diem_toi_da_cua_cau_goc(t, "SA")
    )
    assert round(tong_het, 2) == 7.0, tong_het
    print("OK lam tron: lam dung het phan tu dong = 7.0")


def test_tf_theo_y():
    t = ds.tinh_thang_diem(de_mau())
    assert ds.diem_cau_tf(t, 4)[1] == 1.0
    assert ds.diem_cau_tf(t, 3)[1] == 0.75
    assert ds.diem_cau_tf(t, 0)[1] == 0.0
    print("OK cau TF chia deu 4 y")


def test_thieu_phan_giu_trong_so():
    """De chi co MC + TF -> toi da 5.0 (khong chia lai cho phan con lai)."""
    t = ds.tinh_thang_diem(de_mau(so_mc=10, so_tf=2, so_sa=0, so_tl=0))
    assert t["diem_toi_da_tong"] == 5.0, t["diem_toi_da_tong"]
    assert t["diem_toi_da_tu_dong"] == 5.0
    assert t["theo_phan"]["MC"]["diem_moi_cau"] == 0.3
    assert t["theo_phan"]["SA"]["diem_moi_cau"] == 0.0
    print("OK de thieu phan: trong so co dinh, toi da 5.0")


def test_de_heso1():
    """HeSo1 mac dinh: 6 MC, 1 TF, 2 SA, 3 TL."""
    t = ds.tinh_thang_diem(de_mau(so_mc=6, so_tf=1, so_sa=2, so_tl=3))
    assert t["theo_phan"]["MC"]["diem_moi_cau"] == 0.5
    assert t["theo_phan"]["TF"]["diem_moi_cau"] == 2.0
    assert t["theo_phan"]["TF"]["diem_moi_y"] == 0.5
    assert t["theo_phan"]["SA"]["diem_moi_cau"] == 1.0
    assert t["diem_toi_da_tong"] == 10.0
    print("OK de HeSo1 (15 phut/1 tiet)")


if __name__ == "__main__":
    test_du_4_phan()
    test_cong_don_khong_lech()
    test_tf_theo_y()
    test_thieu_phan_giu_trong_so()
    test_de_heso1()
    print("\nTAT CA TEST DEU PASS")
