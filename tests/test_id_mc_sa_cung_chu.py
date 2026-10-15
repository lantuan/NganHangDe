# -*- coding: utf-8 -*-
r"""Chặn ID MC/SA sai chuẩn (cô Lan 14/10/2026): chữ cái là danh tính của dạng; MC_x và SA_x cùng dạng, cùng chữ.

Các lỗi CŨ được ghi trong tests/id_mc_sa_ton_dong.json (chờ cô duyệt cách sửa từng chương). Test này:
  1. FAIL nếu xuất hiện lỗi MỚI (lỗi không có trong tệp tồn đọng) -> ID mới thêm phải đúng chuẩn ngay;
  2. FAIL nếu một lỗi trong tệp tồn đọng đã được sửa mà chưa xoá khỏi tệp -> tệp tồn đọng chỉ giảm, không phình.
Báo cáo đầy đủ: python scripts/kiem_id_mc_sa.py
"""
import json
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "scripts"))

import kiem_id_mc_sa as K  # noqa: E402

TON = json.loads(K.TON_DONG.read_text(encoding="utf-8")) if K.TON_DONG.exists() else {}


@pytest.mark.parametrize("chuong", K.cac_chuong())
def test_khong_them_loi_id_mc_sa_moi(chuong):
    moi = sorted(set(K.kiem(chuong)) - set(TON.get(chuong, [])))
    assert not moi, "ID sai quy ước MC_x/SA_x (cùng chữ = cùng dạng): %s" % moi[:10]


@pytest.mark.parametrize("chuong", K.cac_chuong())
def test_ton_dong_chi_giam(chuong):
    da_sua = sorted(set(TON.get(chuong, [])) - set(K.kiem(chuong)))
    assert not da_sua, "đã sửa xong, hãy xoá khỏi tests/id_mc_sa_ton_dong.json: %s" % da_sua[:10]
