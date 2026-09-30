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

from app.services.mapping_service import load_mapping, dem_dang_co_ham, cac_y_tu_luan

SO_CHUONG = {10: 9, 11: 9, 12: 6}
KHOI = [(lop, c) for lop, n in SO_CHUONG.items() for c in range(1, n + 1)]
HAU_TO = re.compile(r"_(MC|SA|TL)_[A-Z]$")


def _curriculum():
    ra = {}
    for f in glob.glob("data/curriculum/toan*/*.json"):
        with open(f, encoding="utf-8") as fh:
            for r in json.load(fh):
                ra[r["id"]] = r
    return ra


CUR = _curriculum()


def _nhieu_y(m):
    """Cau tu luan nhieu y (Ngoai le 3, doc 04) - kiem rieng o test_tu_luan_nhieu_y."""
    return cac_y_tu_luan(m["id"]) is not None


@pytest.mark.parametrize("lop,chuong", KHOI)
def test_tu_luan_nhieu_y_khop_curriculum(lop, chuong):
    """ID L10_C3_TH031_TH032_TL_A: moi don vi trong ID phai la mot yeu cau co that
    cua CUNG chuong, dung muc do, dung thu tu y; cac_y trong Mapping khop ID;
    hai don vi khac nhau; content = content cac yeu cau noi bang ' | '."""
    for m in load_mapping(lop, chuong):
        y_id = cac_y_tu_luan(m["id"])
        if y_id is None:
            assert not m.get("cac_y"), "%s co cac_y nhung ID khong theo dang nhieu y" % m["id"]
            continue
        assert "Tự luận" in m["Loai"], m["id"]
        cac_y = m.get("cac_y") or []
        assert len(cac_y) == len(y_id) >= 2, m["id"]
        so = [s for _, s in y_id]
        assert len(set(so)) == len(so), "%s: hai y cung mot don vi kien thuc" % m["id"]
        for (md, s), y in zip(y_id, cac_y):
            cid = y["curriculum_id"]
            assert cid in CUR, "%s tro vao yeu cau khong ton tai: %s" % (m["id"], cid)
            assert cid.startswith("L%d_C%d_B" % (lop, chuong)) and cid.endswith(md + s), (m["id"], cid)
            assert CUR[cid]["MucDo"] == md == y["muc_do"], (m["id"], cid)
        assert m["content"] == " | ".join(CUR[y["curriculum_id"]]["content"] for y in cac_y), m["id"]


@pytest.mark.parametrize("lop,chuong", KHOI)
def test_moi_dong_mapping_tro_vao_yeu_cau_co_that(lop, chuong):
    for m in load_mapping(lop, chuong):
        if m["id"].startswith("L%d_C%d_TF_" % (lop, chuong)) or _nhieu_y(m):
            continue                      # cau Dung/Sai ra theo chuong, khong gan bai
        goc = HAU_TO.sub("", m["id"])
        assert goc in CUR, "%s tro vao yeu cau khong ton tai: %s" % (m["id"], goc)


@pytest.mark.parametrize("lop,chuong", KHOI)
def test_content_mapping_khop_curriculum(lop, chuong):
    for m in load_mapping(lop, chuong):
        if m["id"].startswith("L%d_C%d_TF_" % (lop, chuong)) or _nhieu_y(m):
            continue
        goc = HAU_TO.sub("", m["id"])
        assert m["content"] == CUR[goc]["content"], (
            "%s: content lech voi curriculum" % m["id"])


@pytest.mark.parametrize("lop,chuong", KHOI)
def test_khong_trung_id_trong_mapping(lop, chuong):
    ids = [m["id"] for m in load_mapping(lop, chuong)]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("lop,chuong", KHOI)
def test_moi_yeu_cau_deu_co_it_nhat_mot_dang(lop, chuong):
    co = {HAU_TO.sub("", m["id"]) for m in load_mapping(lop, chuong)}
    thieu = [i for i in CUR if i.startswith("L%d_C%d_" % (lop, chuong)) and i not in co]
    assert not thieu, "yeu cau chua co dang cau hoi nao: %s" % thieu


@pytest.mark.parametrize("lop,chuong", KHOI)
def test_moi_chuong_co_cau_dung_sai(lop, chuong):
    """Cau Dung/Sai ra theo chuong nen chuong nao cung phai co it nhat mot cai."""
    loai = [m for m in load_mapping(lop, chuong)
            if m["id"].startswith("L%d_C%d_TF_" % (lop, chuong))]
    assert loai, "lop %d chuong %d khong co dang cau Dung/Sai nao" % (lop, chuong)


def test_co_du_cau_dem_theo_ham_python_khong_phai_dong_mapping():
    """
    Cho nay tung la bay: neu dem so dong Mapping thi web se bao hoc sinh rang
    chuong da san sang trong khi chua co ham nao, va ra de that se vo ca de.

    Bai test viet sao cho van dung khi co Lan them ham dan: khong ghim cung
    chuong nao da co ham, chi kiem tra dung QUAN HE giua ba lop du lieu.
    """
    co_ham_o_dau = False
    chua_co_ham_o_dau = False

    for lop, chuong in KHOI:
        mp = load_mapping(lop, chuong)
        n = dem_dang_co_ham(lop, chuong)
        assert mp, "lop %d chuong %d chua co ban ke hoach Mapping" % (lop, chuong)
        # so dang co ham khong bao gio duoc vuot so dong Mapping
        assert 0 <= n <= len(mp), (
            "lop %d chuong %d: dem duoc %d dang co ham nhung Mapping chi co %d dong"
            % (lop, chuong, n, len(mp)))
        if n:
            co_ham_o_dau = True
        else:
            chua_co_ham_o_dau = True

    assert co_ham_o_dau, "khong chuong nao co ham - kiem tra lai dem_dang_co_ham"
    assert chua_co_ham_o_dau, (
        "moi chuong deu co ham roi - hay bo bai test nay, no khong con canh duoc gi")


def test_chuong_chua_co_tep_python_thi_dem_ra_khong():
    """Chuong chua co tep .py thi phai bao 0, du Mapping da day du dang."""
    from pathlib import Path
    for lop, chuong in KHOI:
        tep = Path("data/python_bank/toan%d/L%d_C%d.py" % (lop, lop, chuong))
        if not tep.exists():
            assert load_mapping(lop, chuong), "chuong nay phai co Mapping de bai test co nghia"
            assert dem_dang_co_ham(lop, chuong) == 0, (
                "lop %d chuong %d khong co tep Python ma van dem ra dang co ham"
                % (lop, chuong))
