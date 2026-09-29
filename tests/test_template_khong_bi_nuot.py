# -*- coding: utf-8 -*-
r"""Soi cho template HTML khong bi Jinja "nuot" mat mot khuc.

Ngay 29/09/2026 trang /chat ra TRANG TRON. Nguyen nhan: trong khoi cau
hinh MathJax co tham so cua macro \vv, viet lien nhau la dau mo ngoac
nhon roi dau thang. Jinja doc hai ky tu do la MO CHU THICH, nen no nuot
tu cho do cho toi dau dong chu thich gan nhat - mat luon </script>, mat
<style>, mat <body>, mat ca thanh ben. Trinh duyet nhan ve mot the
<script> khong bao gio dong nen nuot not phan con lai thanh ma JS ->
khong ve duoc gi ca.

May chu van tra ve 200 OK nen nhin nhat ky khong thay gi bat thuong. Vi
vay phai co bai kiem tra nay: no dung Jinja dich THAT moi template roi
dem the mo/the dong. Lech mot cai la bao ngay.
"""
import re
from pathlib import Path

import jinja2
import pytest

THU_MUC = Path(__file__).resolve().parents[1] / "app" / "templates"
DANH_SACH = sorted(p.relative_to(THU_MUC).as_posix() for p in THU_MUC.rglob("*.html"))


class _Trong(jinja2.ChainableUndefined):
    """Bien thieu thi coi nhu chuoi rong / danh sach rong, khong vang loi.

    Bai kiem tra nay chi soi CAU TRUC tep, khong soi noi dung, nen khong
    can dung bien that. Phai cho phep lap ({% for %}) va .keys() thi moi
    dich duoc nhung trang nhu thong_ke.html hay chon_lop.html.
    """

    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

    def keys(self):
        return ()

    def items(self):
        return ()

    def values(self):
        return ()


def _moi_truong():
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(THU_MUC)),
        undefined=_Trong,
    )


def _dem(chuoi, the):
    return len(re.findall(the, chuoi, re.IGNORECASE))


@pytest.mark.parametrize("ten", DANH_SACH)
def test_template_dich_ra_du_the(ten):
    env = _moi_truong()
    goc = (THU_MUC / ten).read_text(encoding="utf-8")

    # 1. Dich duoc da. Neu dau chu thich mo ma khong dong thi Jinja bao
    #    TemplateSyntaxError ngay tu day (lam_bai.html da dinh nhu vay).
    ra = env.get_template(ten).render()

    # 2. The mo va the dong phai bang nhau SAU KHI DICH.
    for the in ("script", "style"):
        assert _dem(ra, "<%s[ >]" % the) == _dem(ra, "</%s>" % the), (
            "%s: so the <%s> va </%s> lech nhau sau khi Jinja dich - "
            "nhieu kha nang co mot doan bi nuot lam chu thich." % (ten, the, the)
        )

    # 3. Cai gi co trong tep goc thi phai con trong ban dich.
    for moc in ("<body", "</body>", "</head>"):
        if moc in goc.lower():
            assert moc in ra.lower(), (
                "%s: mat '%s' sau khi Jinja dich - mot khuc template da bi "
                "nuot." % (ten, moc)
            )


def test_cau_hinh_mathjax_duoc_boc_raw():
    """Khoi MathJax phai nam trong raw thi moi an toan."""
    for ten in ("chat/chat.html", "chat/lam_bai.html"):
        txt = (THU_MUC / ten).read_text(encoding="utf-8")
        if "window.MathJax" not in txt:
            continue
        truoc = txt[: txt.index("window.MathJax")]
        assert truoc.count("{% raw %}") > truoc.count("{% endraw %}"), (
            "%s: khoi cau hinh MathJax chua duoc boc trong raw. Trong do co "
            "tham so macro viet lien (mo ngoac nhon + dau thang) ma Jinja "
            "hieu la mo chu thich." % ten
        )
