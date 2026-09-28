#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soat thu vien Python: thieu han nhung goi nao, lech ban nhung goi nao.

Vi sao co tep nay (29/09/2026): tren VPS chay lenh
"pip install --break-system-packages -r requirements.txt" thi dut giua
chung:

    ERROR: Cannot uninstall urllib3 2.0.7, RECORD file not found.
           Hint: The package was installed by debian.

Ubuntu cai san urllib3 bang APT (goi python3-urllib3). Goi do khong co
tep RECORD nen pip KHONG go duoc, va vi requirements.txt ghim
urllib3==2.7.0 nen pip buoc phai go ban cu truoc -> dut ca lenh, cac goi
dang sau khong duoc cai.

Bai hoc: tren may chu dung python he thong, KHONG chay ca
requirements.txt. Chi cai nhung goi THIEU HAN. Goi chi lech ban ma van
chay duoc (urllib3 la goi phu cua requests, ma nguon cua minh khong he
import truc tiep) thi de yen - dong vao la co nguy co hong ca cac cong
cu he thong khac cung dung goi do.

Cach dung:
    python3 scripts/thu_vien_thieu.py           # bao cao
    python3 scripts/thu_vien_thieu.py --lenh    # in ra lenh cai san
    python3 scripts/thu_vien_thieu.py --ten     # chi in ten goi thieu

Ma thoat: 0 = du, 1 = con goi thieu han.
"""
import sys
from pathlib import Path

try:
    from importlib import metadata as md
except ImportError:                                   # python < 3.8
    import importlib_metadata as md                   # type: ignore

GOC = Path(__file__).resolve().parent.parent
TEP_YEU_CAU = GOC / "requirements.txt"


def _chuan_hoa(ten: str) -> str:
    return ten.lower().replace("_", "-")


def _ban_dang_co(ten: str):
    """Ban dang cai cua mot goi, None neu chua cai."""
    for thu in (ten, _chuan_hoa(ten), ten.replace("-", "_")):
        try:
            return md.version(thu)
        except md.PackageNotFoundError:
            continue
        except Exception:
            continue
    return None


def doc_yeu_cau(tep: Path = TEP_YEU_CAU) -> list[tuple[str, str]]:
    ket_qua = []
    for dong in tep.read_text(encoding="utf-8").splitlines():
        dong = dong.split("#", 1)[0].strip()
        if not dong or dong.startswith("-"):
            continue
        ten, dau, ban = dong.partition("==")
        ket_qua.append((ten.strip(), ban.strip() if dau else ""))
    return ket_qua


def soat(tep: Path = TEP_YEU_CAU):
    thieu, lech = [], []
    for ten, ban in doc_yeu_cau(tep):
        dang_co = _ban_dang_co(ten)
        if dang_co is None:
            thieu.append((ten, ban))
        elif ban and dang_co != ban:
            lech.append((ten, ban, dang_co))
    return thieu, lech


def _lenh_cai(thieu) -> str:
    goi = " ".join("%s==%s" % (t, b) if b else t for t, b in thieu)
    return "%s -m pip install --break-system-packages %s" % (sys.executable, goi)


def main() -> int:
    if not TEP_YEU_CAU.exists():
        print("Khong tim thay %s" % TEP_YEU_CAU)
        return 2
    thieu, lech = soat()

    if "--ten" in sys.argv:
        print(" ".join(t for t, _ in thieu))
        return 1 if thieu else 0
    if "--lenh" in sys.argv:
        print(_lenh_cai(thieu) if thieu else "")
        return 1 if thieu else 0

    print("python dang soat: %s" % sys.executable)
    if not thieu:
        print("Thu vien: DU (khong goi nao thieu han)")
    else:
        print("Thu vien THIEU HAN %d goi:" % len(thieu))
        for ten, ban in thieu:
            print("   - %s%s" % (ten, ("==" + ban) if ban else ""))
        print()
        print("Lenh cai (CHI cai cac goi thieu, khong dung den goi cua he thong):")
        print("   " + _lenh_cai(thieu))

    if lech:
        print()
        print("Lech ban %d goi - DE YEN, khong can dong vao:" % len(lech))
        for ten, can, co in lech:
            print("   - %-22s requirements ghi %-12s dang co %s" % (ten, can, co))
        print("   (Goi do Ubuntu cai bang APT thi pip khong go duoc. Ep cai")
        print("    de ban ghim se lam dut ca lenh va co the hong cong cu he thong.)")

    return 1 if thieu else 0


if __name__ == "__main__":
    raise SystemExit(main())
