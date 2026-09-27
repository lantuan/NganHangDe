"""
Canh cho Curriculum luon danh so chuong/bai DUNG NHU PPCT.

Vi sao phai canh: he thong noi PPCT voi Curriculum bang chuoi ma
L{lop}_C{chuong}_B{bai}. Neu hai ben danh so lech nhau thi ma VAN KHOP CHUOI
nhung tro vao BAI KHAC - may khong bao loi, chi lang le lay yeu cau can dat
cua bai khac, va hoc sinh nhan de sai pham vi ma khong ai biet.

Da tung lech that: L10_C5_B12 ben PPCT la "So gan dung va sai so", ben
Curriculum lai la "Phuong trinh quy ve phuong trinh bac hai" (sua 27/09/2026).
"""

import glob
import json

import pytest

LOP = [10, 11, 12]


def _ppct(lop):
    with open("data/ppct/toan%d.json" % lop, encoding="utf-8") as f:
        return {("%s" % it["chuong_so"], "%s" % it["bai_so"]): it["bai"]
                for it in json.load(f)}


def _curriculum(lop):
    ra = {}
    for f in glob.glob("data/curriculum/toan%d/*.json" % lop):
        with open(f, encoding="utf-8") as fh:
            for r in json.load(fh):
                ra[(r["chuong_so"], r["bai_so"])] = r["bai"]
    return ra


@pytest.mark.parametrize("lop", LOP)
def test_ten_bai_khop_ppct(lop):
    """Cung mot ma chuong/bai thi hai ben phai la CUNG MOT BAI."""
    pp, cu = _ppct(lop), _curriculum(lop)
    lech = [(k, pp[k], cu[k]) for k in set(pp) & set(cu)
            if pp[k].strip().lower()[:12] != cu[k].strip().lower()[:12]]
    assert not lech, "\n".join(
        "  C%s_B%s  PPCT: %s  |  Curriculum: %s" % (k[0], k[1], a, b)
        for k, a, b in sorted(lech))


@pytest.mark.parametrize("lop", LOP)
def test_khong_co_bai_nao_cua_ppct_bi_bo_quen(lop):
    """
    Bai nao PPCT co day ma Curriculum khong co yeu cau can dat nao thi hoc
    sinh on den bai do se khong ra duoc cau hoi nao.
    """
    pp, cu = _ppct(lop), _curriculum(lop)
    thieu = sorted(set(pp) - set(cu), key=lambda k: (int(k[0]), int(k[1])))
    assert not thieu, "Bai co trong PPCT nhung Curriculum chua co:\n" + "\n".join(
        "  C%s_B%s  %s" % (c, b, pp[(c, b)]) for c, b in thieu)


@pytest.mark.parametrize("lop", LOP)
def test_bao_bai_chua_co_trong_ppct(lop):
    """
    Nguoc lai: bai co trong Curriculum ma PPCT chua co thi chi BAO THIEU,
    khong bao loi - PPCT duoc bo sung dan theo hoc ki.
    """
    pp, cu = _ppct(lop), _curriculum(lop)
    thieu = sorted(set(cu) - set(pp), key=lambda k: (int(k[0]), int(k[1])))
    if thieu:
        print("\nLop %d - PPCT chua co cac bai sau (Curriculum da co):" % lop)
        for c, b in thieu:
            print("  C%s_B%s  %s" % (c, b, cu[(c, b)]))
