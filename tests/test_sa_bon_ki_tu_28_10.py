"""Trả lời ngắn: đáp số tối đa 4 kí tự (cô Lan 28/10/2026: "vẫn áp dụng 4 kí tự, chỉnh sửa lại hết cho tôi").

Trước khi sửa: 90 hàm SA (L10_C2, C3, C5, C6, C7, C8, L11_C1, C2, C3, C4, C6) có lúc sinh đáp số 5 kí tự trở lên
(-0,96; 21,79; 1083,2; 10300...). Đã sửa:
  - L10_C3 bộ sinh chung _ms_chon_n: câu SA tự làm tròn ít chữ số hơn (câu dẫn, lời giải đổi theo) cho vừa 4 ô;
  - một số hàm đổi hàng làm tròn (phần trăm -> phần mười / đơn vị) hoặc số liệu; L11_C1_B2_TH011 hỏi T = 25 sin 2a;
  - mọi hàm đó bọc @sa_bon_ki_tu (data/python_bank/sa_bon_ki_tu.py): chỉ giữ câu có đáp số vừa 4 ô.
Test này chạy MỌI hàm SA của ngân hàng (Việt + Anh) để không lọt câu mới quá 4 kí tự.
"""
import random
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from app.services.generator_service import _call_generator_function, _load_chapter_module  # noqa: E402
import sa_bon_ki_tu as S  # noqa: E402

SO_LAN = 12


def _cac_chuong():
    kq = []
    for lang, thu_muc in (("vi", "python_bank"), ("en", "python_bank_en")):
        for tep in sorted((GOC / "data" / thu_muc).glob("toan1*/L*_C*.py")):
            m = re.match(r"L(\d+)_C(\d+)$", tep.stem)
            kq.append((lang, int(m.group(1)), int(m.group(2))))
    return kq


@pytest.mark.parametrize("lang, lop, chuong", _cac_chuong())
def test_moi_cau_tra_loi_ngan_vua_bon_o(lang, lop, chuong):
    import numpy as np
    mo = _load_chapter_module(lop, chuong, lang)
    dai = {}
    for ten in sorted(n for n in dir(mo) if re.match(r"^L\d+_C\d+_.*_SA_[A-Z]_\d{2}$", n)):
        f = getattr(mo, ten)
        for s in range(SO_LAN):
            random.seed(s)
            np.random.seed(s)
            try:
                out = _call_generator_function(f, 1, None, None)
            except Exception:  # noqa: BLE001 - hàm hỏng do test khác soi; ở đây chỉ soi độ dài đáp số
                continue
            for d in S.dap_so_tra_loi_ngan(out):
                if len(d) > S.TOI_DA_KI_TU:
                    dai.setdefault(ten, d)
    assert not dai, "Đáp số trả lời ngắn quá 4 kí tự: %s" % dai


def test_bo_loc_giu_dung_so_cau_va_bao_loi_ro():
    goi = []

    def _sa(socau, dang=2):
        goi.append(1)
        n = len(goi)
        return "\\begin{ex}\n\\shortans{ $%s$}\n\\end{ex}\n" % ("12,345" if n % 2 else str(n))
    boc = S.sa_bon_ki_tu(_sa)
    out = boc(3)
    assert S.dap_so_tra_loi_ngan(out) == ["2", "4", "6"]
    import inspect
    assert list(inspect.signature(boc).parameters) == ["socau", "dang"]     # generator_service đọc đúng tham số

    def _luon_dai(socau, dang=2):
        return "\\shortans{ $-0,961$}\n"
    with pytest.raises(S.DapSoQuaDaiError, match="vừa 4 ô"):
        S.sa_bon_ki_tu(_luon_dai)(1)


def test_ms_chon_n_lam_tron_it_hon_cho_vua():
    """L10_C3 bộ sinh chung: đáp số 16,97 (hàng phần trăm) -> câu hỏi đổi thành hàng phần mười, đáp số 17."""
    mo = _load_chapter_module(10, 3)
    from sympy import Float, Rational
    q = {"v": Float(16.9706), "xap": True, "n": 2, "goc": False}
    assert mo._ms_chon_n(q, "SA") == 1 and mo._ms_chon_n(q, "MC") == 2
    q = {"v": Rational(-24, 25), "xap": False, "n": 2, "goc": False}
    with pytest.raises(mo._MsLai):                       # giá trị chính xác -0,96: không ép làm tròn, chọn bộ số khác
        mo._ms_chon_n(q, "SA")
