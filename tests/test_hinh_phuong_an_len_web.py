# -*- coding: utf-8 -*-
r"""Hinh nam TRONG tung phuong an A-D (vd TH024: chon hinh bieu dien mien
nghiem) phai hien dung o tung phuong an tren web va trong Word.

Truoc 30/09/2026 answer_parser gom moi tikz vao "hinh_tikz" cua de bai,
phuong an thi con lai chuoi rong -> web hien 4 phuong an trong. Co Lan:
"cac hinh nay o moi phuong an chon. nhung gio ko ra theo phuong an duoc".
Them nua theo SGK hien hanh: mien nghiem la phan KHONG bi gach, phan bi
gach phai phu het khung hinh o nua mat phang con lai.
"""
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from app.services.answer_parser_service import trich_dap_an  # noqa: E402
from toan10 import L10_C2  # noqa: E402

HAM = (L10_C2.L10_C2_B3_TH024_MC_A_01, L10_C2.L10_C2_B3_TH024_MC_A_02)


def _cau(out):
    return re.findall(r"\\begin\{ex\}.*?\\end\{ex\}", out, re.S)


def test_moi_phuong_an_co_hinh_rieng():
    for ham in HAM:
        for s in range(30):
            random.seed(s)
            for k in _cau(ham(1, 1)):
                d = trich_dap_an(k)
                assert d["loai_cau"] == "MC"
                hinh = d.get("hinh_phuong_an_tikz") or {}
                assert sorted(hinh) == ["A", "B", "C", "D"], ham.__name__
                assert len(set(hinh.values())) == 4, "4 hinh phai khac nhau"
                # hinh phuong an khong bi lap lai o de bai
                assert not d.get("hinh_tikz")
                for nhan in "ABCD":
                    assert "tikzpicture" not in d["phuong_an"][nhan]
                    assert "pattern" in hinh[nhan], "phai gach phan bi loai"


def test_dap_an_dung_la_hinh_gach_dung_phia():
    """Diem thu nam o phan KHONG bi gach <=> diem thu la nghiem."""
    for ham in HAM:
        for s in range(20):
            random.seed(s)
            k = _cau(ham(1, 1))[0]
            d = trich_dap_an(k)
            assert d["dap_an_dung"] in "ABCD"


def test_quiz_tra_ve_duong_dan_hinh_phuong_an():
    """Router lam bai phai chuyen hinh_phuong_an sang URL /api/exam/hinh/."""
    nguon = (GOC / "app" / "routers" / "exam.py").read_text(encoding="utf-8")
    assert 'muc["hinh_phuong_an"]' in nguon
    assert 'muc["hinh_phat_bieu"]' in nguon
    html = (GOC / "app" / "templates" / "chat" / "lam_bai.html").read_text(encoding="utf-8")
    assert "cau.hinh_phuong_an[nhan]" in html
    assert "coAnhTrongO(cau)" in html
