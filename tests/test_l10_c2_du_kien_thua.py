"""Cau dan chuong 2 (tinh huong thuc te) CHI chua du kien duoc dung de giai.

Co Lan 11/10/2026: "cau hoi ko co tien thi dua tien vao lam gi. chi dua du lieu co su dung de giai bai".
 - NB025 (bat phuong trinh cua MOT dieu kien): dung 3 so (he so cua x, y va gioi han); khong co gia / lai / diem thuong.
 - Cau lap he, chon phuong an, so dinh, gioi han khi chi dung mot loai: khong co gia / lai / diem thuong.
 - Cau tinh gia tri (chi phi / tien lai / diem thuong) cua MOT phuong an cho truoc: chi co gia + phuong an, khong co dieu kien.
"""
import importlib.util
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C2_dkt_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_dkt_test"] = M
_spec.loader.exec_module(M)

_SRC = (GOC / "data" / "python_bank" / "toan10" / "L10_C2.py").read_text(encoding="utf-8")
HAM = sorted(set(
    re.findall(r"^def (L10_C2_B3_NB025_MC_[B-E]_\d\d)\(", _SRC, flags=re.M)
    + re.findall(r"^def (L10_C2_B4_VD028_(?:MC|SA)_[B-I]_\d\d)\(", _SRC, flags=re.M)))

TU_GIA = re.compile(r"\b(giá|Giá|lãi|điểm thưởng|nghìn đồng|triệu đồng)\b")      # \b: "đa giác" không phải "giá"
TU_DIEU_KIEN = ("tối thiểu", "tối đa", "không quá", "ít nhất", "làm việc")
SO = re.compile(r"\$\d+(?:\{,\}\d+)?\$")


def _cau_dan(ten, n=40):
    cap = []
    orig_mc, orig_tl = M.MC_SA_answer_text, M.TL_answer_text
    M.MC_SA_answer_text = lambda debai, *a, **k: cap.append(debai) or ""
    M.TL_answer_text = lambda debai, *a, **k: cap.append(debai) or ""
    try:
        for seed in range(n):
            random.seed(seed)
            M._rd.seed(seed)
            getattr(M, ten)(1)
    finally:
        M.MC_SA_answer_text, M.TL_answer_text = orig_mc, orig_tl
    return cap


def _loai(de):
    hoi = de.split("$y$")[-1]
    if "Bất phương trình nào sau đây" in de:
        return "mot_dk"
    if re.search(r"Một (phương án|đội pha chế \$)", de):
        return "gia_tri_pa"
    if re.search(r"(?i)(chi phí|tiền lãi|điểm thưởng cao nhất|giá trị tối ưu|để (chi phí|tiền lãi|nhận được số điểm))", hoi):
        return "toi_uu"
    return "dieu_kien"                                                   # he / phuong an kha thi / dinh / gioi han


@pytest.mark.parametrize("ten", HAM)
def test_cau_dan_khong_co_du_kien_thua(ten):
    cac = _cau_dan(ten)
    assert cac
    for de in cac:
        loai = _loai(de)
        if loai == "mot_dk":
            phan = de.split("Gọi")[0]
            assert not TU_GIA.search(phan), de
            phan = phan.replace("$1$ lít nước A cần", "").replace("$1$ lít nước B cần", "")   # '1 lit' la don vi san pham
            assert len(SO.findall(phan)) == 3, de                        # he so cua x, he so cua y, gioi han
        elif loai == "gia_tri_pa":
            assert not any(t in de for t in TU_DIEU_KIEN), de
            assert "Gọi $x$" not in de, de
        elif loai == "dieu_kien":
            assert not TU_GIA.search(de), de
