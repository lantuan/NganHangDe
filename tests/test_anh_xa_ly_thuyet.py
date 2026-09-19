"""
Canh BANG ANH XA bai <-> tep ly thuyet (data/ly_thuyet/anh_xa.json).

Vi sao can canh: bang nay viet TAY (quan he nhieu-nhieu, khong khop tu
dong duoc). Doi ten mot tep, them mot bai vao curriculum, hay go nham mot
ma bai - deu lam gia su AI muc B im lang tra ve rong thay vi bao loi.
Bai kiem tra nay bat ngay, khong can chay web.
"""

import json
import re
from pathlib import Path

import pytest

THU_MUC = Path("data/ly_thuyet")
TEP_ANH_XA = THU_MUC / "anh_xa.json"


@pytest.fixture(scope="module")
def anh_xa():
    return json.loads(TEP_ANH_XA.read_text(encoding="utf-8"))["anh_xa"]


@pytest.fixture(scope="module")
def bai_curriculum():
    ds = {}
    for tep in Path("data/curriculum").glob("*/*.json"):
        for m in json.loads(tep.read_text(encoding="utf-8")):
            ds[f"L{m['lop']}_C{m['chuong_so']}_B{m['bai_so']}"] = m["bai"]
    return ds


def test_tep_anh_xa_ton_tai_va_hop_le():
    assert TEP_ANH_XA.exists(), "Thieu data/ly_thuyet/anh_xa.json"
    json.loads(TEP_ANH_XA.read_text(encoding="utf-8"))


def test_moi_tep_trong_bang_deu_co_that(anh_xa):
    """Go nham ten tep -> muc B im lang khong tra ve gi."""
    thieu = [
        f"{ma} -> {ten_tep}"
        for ma, m in anh_xa.items()
        for ten_tep in m["tep"]
        if not (THU_MUC / ten_tep).exists()
    ]
    assert not thieu, "Tep ghi trong anh_xa.json nhung KHONG co tren dia:\n" + "\n".join(thieu)


def test_moi_ma_bai_deu_co_trong_curriculum(anh_xa, bai_curriculum):
    """Go nham ma bai -> khong bao gio tra ra tep."""
    la = [ma for ma in anh_xa if ma not in bai_curriculum]
    assert not la, f"Ma bai khong co trong curriculum: {la}"


def test_moi_bai_trong_curriculum_deu_co_ly_thuyet(anh_xa, bai_curriculum):
    """Bai nao chua co tep ly thuyet thi muc B chua phuc vu duoc bai do."""
    thieu = sorted(ma for ma in bai_curriculum if ma not in anh_xa)
    assert not thieu, (
        "Bai co trong curriculum nhung CHUA co tep ly thuyet:\n"
        + "\n".join(f"  {ma}  {bai_curriculum[ma]}" for ma in thieu)
    )


def test_ten_bai_trong_bang_khop_curriculum(anh_xa, bai_curriculum):
    """Cot ten_bai chi de NGUOI doc/ra soat - nhung sai thi gay hieu nham."""
    lech = [
        f"{ma}: bang ghi {m['ten_bai']!r}, curriculum ghi {bai_curriculum[ma]!r}"
        for ma, m in anh_xa.items()
        if ma in bai_curriculum and m["ten_bai"].strip() != bai_curriculum[ma].strip()
    ]
    assert not lech, "ten_bai lech so voi curriculum:\n" + "\n".join(lech)


def test_khong_tep_nao_bi_khai_hai_lan_cho_cung_mot_bai(anh_xa):
    for ma, m in anh_xa.items():
        assert len(m["tep"]) == len(set(m["tep"])), f"{ma} khai trung tep"


def test_moi_tep_deu_co_section_va_phan_ly_thuyet(anh_xa):
    """Tep phai co \\section (ten bai) va mot muc ly thuyet - do la 2 moc
    ma ly_thuyet_service se cat theo."""
    hong = []
    for ma, m in anh_xa.items():
        for ten_tep in m["tep"]:
            duong_dan = THU_MUC / ten_tep
            if not duong_dan.exists():
                continue
            noi = duong_dan.read_text(encoding="utf-8", errors="replace")
            if not re.search(r"\\section\{[^}]+\}", noi):
                hong.append(f"{ten_tep}: khong co \\section")
            if not re.search(r"\\subsection\{[^}]*(?:LÝ THUYẾT|KIẾN THỨC|Lý thuyết)[^}]*\}", noi):
                hong.append(f"{ten_tep}: khong tim thay muc ly thuyet")
    assert not hong, "\n".join(hong)
