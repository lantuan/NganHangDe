"""
Canh tinh nhat quan giua ba lop du lieu cua ngan hang de:

    curriculum  ->  yeu cau can dat cua Bo
    mapping     ->  cac DANG cau hoi kiem tra duoc yeu cau do
    Python      ->  ham sinh ra cau hoi that

Mapping la BAN KE HOACH nen duoc phep co dang chua viet ham. Nhung moi dong
mapping BUOC phai tro vao mot yeu cau can dat co that, va noi dung phai khop
- neu khong, khi ra de se chon trung mot ma khong sinh duoc cau nao.
"""

import glob
import json
import re

import pytest

from app.services.mapping_service import load_mapping, dem_dang_co_ham

CHUONG = list(range(1, 9))
HAU_TO = re.compile(r"_(MC|SA|TL)_[A-Z]$")


def _curriculum():
    ra = {}
    for f in glob.glob("data/curriculum/toan10/*.json"):
        with open(f, encoding="utf-8") as fh:
            for r in json.load(fh):
                ra[r["id"]] = r
    return ra


CUR = _curriculum()


@pytest.mark.parametrize("chuong", CHUONG)
def test_moi_dong_mapping_tro_vao_yeu_cau_co_that(chuong):
    for m in load_mapping(10, chuong):
        if m["id"].startswith("L10_C%d_TF_" % chuong):
            continue                      # cau Dung/Sai ra theo chuong, khong gan bai
        goc = HAU_TO.sub("", m["id"])
        assert goc in CUR, "%s tro vao yeu cau khong ton tai: %s" % (m["id"], goc)


@pytest.mark.parametrize("chuong", CHUONG)
def test_content_mapping_khop_curriculum(chuong):
    for m in load_mapping(10, chuong):
        if m["id"].startswith("L10_C%d_TF_" % chuong):
            continue
        goc = HAU_TO.sub("", m["id"])
        assert m["content"] == CUR[goc]["content"], (
            "%s: content lech voi curriculum" % m["id"])


@pytest.mark.parametrize("chuong", CHUONG)
def test_khong_trung_id_trong_mapping(chuong):
    ids = [m["id"] for m in load_mapping(10, chuong)]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("chuong", CHUONG)
def test_moi_yeu_cau_deu_co_it_nhat_mot_dang(chuong):
    co = {HAU_TO.sub("", m["id"]) for m in load_mapping(10, chuong)}
    thieu = [i for i in CUR if i.startswith("L10_C%d_" % chuong) and i not in co]
    assert not thieu, "yeu cau chua co dang cau hoi nao: %s" % thieu


@pytest.mark.parametrize("chuong", CHUONG)
def test_moi_chuong_co_cau_dung_sai(chuong):
    """Cau Dung/Sai ra theo chuong nen chuong nao cung phai co it nhat mot cai."""
    loai = [m for m in load_mapping(10, chuong)
            if m["id"].startswith("L10_C%d_TF_" % chuong)]
    assert loai, "chuong %d khong co dang cau Dung/Sai nao" % chuong


def test_co_du_cau_dem_theo_ham_python_khong_phai_dong_mapping():
    """
    Cho nay tung la bay: neu dem so dong mapping thi web se bao hoc sinh rang
    chuong 2-8 da san sang trong khi chua co ham nao, va ra de that se vo ca de.
    """
    assert dem_dang_co_ham(10, 1) > 0            # C1 da co 46 ham
    for c in range(2, 9):
        assert len(load_mapping(10, c)) > 0      # da co ban ke hoach
        assert dem_dang_co_ham(10, c) == 0       # nhung chua co ham -> chua san sang
