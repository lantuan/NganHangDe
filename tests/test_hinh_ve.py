"""
Hinh ve cua cau hoi phai hien duoc tren web.

Ly do (co Lan neu 27/09/2026): "phai co hinh ca tren web. ko the ko co
hinh. se bi sai muc do cua cau. co hinh muc do se de hon. hoac phuc tap
hon (vi du bai ham bac 2 - ko co hinh sao lam cac muc do nhin hinh ra
dinh, truc doi xung)". Bo hinh la doi luon muc do cua cau.

Bai test nay KHONG dich LaTeX (cham va phu thuoc may), chi soi phan
logic: tim dung doan TikZ, ma bam on dinh, va de bai van giu duoc chu.
"""

import re

from app.services.answer_parser_service import trich_de_bai
from app.services.hinh_ve_service import ma_hinh, tim_tikz

KHOI_CO_HINH = r"""\begin{ex}%%[?]
\immini{
Cho tam giac $ABC$ nhu hinh ben. Tinh $AB$.}
{\begin{tikzpicture}
\draw (0,0) -- (2,0) -- (1,1.5) -- cycle;
\end{tikzpicture}}
\choice{\True $5$}
{$6$}
{$7$}
{$8$}
\loigiai{
Dinh li cosin.
}
\end{ex}
"""


def test_tim_dung_doan_tikz():
    assert len(tim_tikz(KHOI_CO_HINH)) == 1
    assert r"\draw (0,0)" in tim_tikz(KHOI_CO_HINH)[0]


def test_de_bai_giu_lai_ma_nguon_hinh():
    kq = trich_de_bai(KHOI_CO_HINH)
    assert kq["co_hinh_ve"] is True
    assert len(kq["hinh_tikz"]) == 1, "phai giu lai ma nguon hinh de con dich ra anh"
    # chu cua de bai van con, khong bi hinh nuot mat
    assert "Tinh $AB$" in kq["de_bai"]
    # nhung ma TikZ thi khong duoc lot vao phan chu hien cho hoc sinh
    assert "tikzpicture" not in kq["de_bai"]


def test_ma_hinh_on_dinh_va_phan_biet():
    a = tim_tikz(KHOI_CO_HINH)[0]
    b = a.replace("(2,0)", "(3,0)")
    assert ma_hinh(a) == ma_hinh(a), "cung mot hinh phai ra cung mot ma"
    assert ma_hinh(a) != ma_hinh(b), "hinh khac nhau phai ra ma khac nhau"
    assert re.fullmatch(r"[0-9a-f]{20}", ma_hinh(a))


def test_khoi_khong_co_hinh_thi_danh_sach_rong():
    kq = trich_de_bai(r"""\begin{ex}%%[?]
Cho $A = 1$. Tinh $A + 1$.
\shortans{$2$}
\loigiai{$2$}
\end{ex}
""")
    assert kq["co_hinh_ve"] is False
    assert kq["hinh_tikz"] == []
