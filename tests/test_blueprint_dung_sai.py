# -*- coding: utf-8 -*-
"""Kiem thu quy dinh phan bo de cua giao vien (Version 2.38).

1. Cau Dung/Sai = 4 cau (1 NB + 1 TH + 1 VD + 1 VDC), chon bai TRUOC TIEN.
2. Tru 1 cau moi muc ngay tai BAI ma Dung/Sai da chon.
3. Chia so cau ve tung bai theo TI LE SO TIET.
4. Moi bai toi da 1 cau VDC; VD uu tien bai chua co VDC.
5. Cau Dung/Sai chi duoc tru MOT LAN o muc VD/VDC du VD nam o ca 3 phan.

Chay: source .venv/bin/activate && python3 tests/test_blueprint_dung_sai.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.exam_scope_service import dem_so_tiet  # noqa: E402
from app.services.exam_blueprint_service import (  # noqa: E402
    _chia_theo_so_tiet,
    _chon_bai_dung_sai,
    _tru_phan_dung_sai,
    _phan_bo_vd_vdc,
)


def test_dem_so_tiet():
    assert dem_so_tiet("23, 25-26") == 3
    assert dem_so_tiet("29-30") == 2
    assert dem_so_tiet("31, 37") == 2
    assert dem_so_tiet("45-47") == 3
    assert dem_so_tiet(None) == 1, "bai thieu du lieu tiet phai tinh 1, khong duoc loai bo"
    print("OK dem so tiet tu PPCT")


def test_chia_theo_ti_le_so_tiet():
    # B1 2 tiet, B2 6 tiet -> 8 cau chia 2/6
    tiet = {"B1": 2, "B2": 6}
    assert _chia_theo_so_tiet(8, tiet) == {"B1": 2, "B2": 6}
    # Tong luon khop du lam tron the nao
    for so_cau in range(1, 20):
        assert sum(_chia_theo_so_tiet(so_cau, tiet).values()) == so_cau, so_cau
    print("OK chia theo ti le so tiet, tong luon khop")


def test_chon_bai_dung_sai_uu_tien_nhieu_tiet():
    tiet = {"B1": 2, "B2": 6, "B3": 4}
    assert _chon_bai_dung_sai(tiet, 1) == {"B2": 1}
    assert _chon_bai_dung_sai(tiet, 2) == {"B2": 1, "B3": 1}
    # Nhieu cau hon so bai -> moi quay vong
    assert _chon_bai_dung_sai(tiet, 4) == {"B2": 2, "B3": 1, "B1": 1}
    print("OK chon bai Dung/Sai theo so tiet giam dan")


def test_tru_ngay_tai_bai_dung_sai():
    """Don vi kien thuc duoc chia 3 cau, Dung/Sai lay 1 -> con 2."""
    phan_bo, du = _tru_phan_dung_sai({"B1": 3, "B2": 2}, {"B1": 1})
    assert phan_bo == {"B1": 2, "B2": 2}, phan_bo
    assert du == 0
    # Bai khong duoc chia cau nao o muc nay -> bo qua, KHONG day sang bai khac
    phan_bo, du = _tru_phan_dung_sai({"B2": 2}, {"B1": 1})
    assert phan_bo == {"B2": 2}, phan_bo
    assert du == 1
    print("OK tru 1 cau ngay tai bai Dung/Sai da chon")


def test_vdc_khong_don_chung_mot_bai():
    """Con DU bai trong: khong duoc co cau VD nao roi vao bai da co VDC."""
    bai = ["B1", "B2", "B3", "B4", "B5"]
    kq = _phan_bo_vd_vdc(bai, so_vd=2, so_vdc=2)
    for b, v in kq.items():
        assert v["vdc"] <= 1, f"{b} co {v['vdc']} cau VDC - phai toi da 1"
    assert sum(v["vdc"] for v in kq.values()) == 2
    assert sum(v["vd"] for v in kq.values()) == 2
    bai_co_vdc = {b for b, v in kq.items() if v["vdc"] > 0}
    bai_co_vd = {b for b, v in kq.items() if v["vd"] > 0}
    assert not (bai_co_vd & bai_co_vdc), "con bai trong ma VD lai don vao bai da co VDC"
    print("OK con bai trong: moi bai toi da 1 VDC, VD khong dung chung bai voi VDC")


def test_het_bai_trong_moi_quay_lai():
    """HET bai trong thi MOI duoc quay lai bai da co VDC - va phai lap
    het bai trong truoc da (quy dinh cua giao vien)."""
    bai = ["B1", "B2", "B3", "B4"]
    kq = _phan_bo_vd_vdc(bai, so_vd=2, so_vdc=3)
    assert sum(v["vdc"] for v in kq.values()) == 3
    assert sum(v["vd"] for v in kq.values()) == 2

    bai_co_vdc = {b for b, v in kq.items() if v["vdc"] > 0}
    bai_trong = [b for b in bai if b not in bai_co_vdc]
    # 4 bai - 3 bai da co VDC -> chi con 1 bai trong, ma can dat 2 cau VD
    assert len(bai_trong) == 1
    for b in bai_trong:
        assert kq.get(b, {}).get("vd", 0) >= 1, "bai trong phai duoc lap truoc"
    so_vd_phai_quay_lai = 2 - len(bai_trong)
    so_vd_o_bai_co_vdc = sum(kq[b]["vd"] for b in bai_co_vdc if b in kq)
    assert so_vd_o_bai_co_vdc == so_vd_phai_quay_lai, (
        f"quay lai {so_vd_o_bai_co_vdc} cau, dang le chi {so_vd_phai_quay_lai}"
    )
    print("OK het bai trong moi quay lai bai da co VDC, khong quay lai som")


if __name__ == "__main__":
    test_dem_so_tiet()
    test_chia_theo_ti_le_so_tiet()
    test_chon_bai_dung_sai_uu_tien_nhieu_tiet()
    test_tru_ngay_tai_bai_dung_sai()
    test_vdc_khong_don_chung_mot_bai()
    test_het_bai_trong_moi_quay_lai()
    print("\nTAT CA TEST DEU PASS")
