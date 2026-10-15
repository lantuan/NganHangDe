# -*- coding: utf-8 -*-
r"""Kiểm quy ước ID MC/SA (cô Lan 14/10/2026) - CHỈ ĐỌC, không sửa Mapping.

Quy ước: trong MỘT đơn vị kiến thức (vd L10_C3_B6_TH032), chữ cái là danh tính của DẠNG:
  - MC_x và SA_x cùng chữ thì cùng dạng (cùng chữ "Dang" trong Mapping);
  - cùng một dạng (cùng "Dang") thì MC và SA phải CÙNG chữ (không chéo MC_G với SA_D);
  - mỗi dạng có cả MC lẫn SA, trừ khi bài toán vô lý ở một loại.

Ba loại lỗi (khoá lỗi dùng để so với tệp tồn đọng). Nhóm theo chữ "Dang" trong đơn vị; một "Dang" có thể do nhiều
chữ cùng mang (cùng bối cảnh, bộ chọn coi là một dạng); chữ có ở cả MC và SA là đúng, phần còn lại mới là lỗi:
  LECH   |<đơn vị>|MC_xy|SA_zt   cùng "Dang" mà chữ MC khác chữ SA (gồm cả chéo MC_G với SA_D)
  CHI_MC |<đơn vị>|x          dạng có MC mà chưa có SA
  CHI_SA |<đơn vị>|x          dạng có SA mà chưa có MC

Chạy:  python scripts/kiem_id_mc_sa.py [L10_C3 ...]   (không đối số: tất cả chương)
       python scripts/kiem_id_mc_sa.py --ghi-ton-dong   (ghi lại tệp tồn đọng cho test - chỉ khi cô duyệt)
"""
import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
TON_DONG = GOC / "tests" / "id_mc_sa_ton_dong.json"
NGOAI_LE = GOC / "data" / "mapping" / "id_mc_sa_ngoai_le.json"   # ID cô Lan duyệt "vô lý/không cần" bản MC hoặc SA cùng dạng
_ID = re.compile(r"^(L\d+_C\d+_B\d+_[A-Z]+\d+[A-Z]?)_(MC|SA)_([A-Z]+)$")


def _chuan(s: str) -> str:
    return " ".join(str(s).lower().split())


def cac_chuong() -> list[str]:
    return sorted(Path(f).stem for f in glob.glob(str(GOC / "data" / "mapping" / "toan*" / "L*_C*.json")))


def doc_mapping(chuong: str) -> list[dict]:
    f = glob.glob(str(GOC / "data" / "mapping" / "toan*" / ("%s.json" % chuong)))[0]
    return json.loads(Path(f).read_text(encoding="utf-8"))


def nhom_theo_dang(chuong: str) -> dict:
    """{đơn vị: {Dang chuẩn hoá: {"MC": [chữ...], "SA": [chữ...]}}}. Nhiều chữ có thể CÙNG "Dang" (cùng dạng, nhiều
    chữ: bộ chọn coi là một dạng); khi đó tập chữ MC phải bằng tập chữ SA."""
    ra = defaultdict(lambda: defaultdict(lambda: {"MC": [], "SA": []}))
    for x in doc_mapping(chuong):
        m = _ID.match(x.get("id", ""))
        if m:
            ra[m.group(1)][_chuan(x.get("Dang", ""))][m.group(2)].append(m.group(3))
    return ra


def ngoai_le(chuong: str) -> set:
    """Các ID (đầy đủ) được miễn kiểm vì cô Lan duyệt là vô lý/không cần bản kia."""
    if not NGOAI_LE.exists():
        return set()
    return set(json.loads(NGOAI_LE.read_text(encoding="utf-8")).get(chuong, {}))


def kiem(chuong: str) -> list[str]:
    """Danh sách khoá lỗi (đã sắp xếp) của một chương. Mỗi nhóm "Dang" trong một đơn vị phải có tập chữ MC = tập chữ SA."""
    loi = []
    mien = ngoai_le(chuong)
    for dv, cac_dang in nhom_theo_dang(chuong).items():
        for dang, g in cac_dang.items():
            chung = set(g["MC"]) & set(g["SA"])          # chữ có ở cả MC lẫn SA trong nhóm: đã đúng
            mc = sorted(set(g["MC"]) - chung)
            sa = sorted(set(g["SA"]) - chung)
            if not mc and not sa:
                continue
            if not sa:
                loi += ["CHI_MC|%s|%s" % (dv, l) for l in mc if "%s_MC_%s" % (dv, l) not in mien]
            elif not mc:
                loi += ["CHI_SA|%s|%s" % (dv, l) for l in sa if "%s_SA_%s" % (dv, l) not in mien]
            else:
                loi.append("LECH|%s|MC_%s|SA_%s" % (dv, "".join(mc), "".join(sa)))
    return sorted(loi)


def kiem_tat_ca(chuongs=None) -> dict:
    return {c: kiem(c) for c in (chuongs or cac_chuong())}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    kq = kiem_tat_ca(args or None)
    if "--ghi-ton-dong" in sys.argv:
        TON_DONG.write_text(json.dumps({c: v for c, v in kq.items() if v}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("đã ghi", TON_DONG)
    for c, v in kq.items():
        dem = {k: sum(1 for x in v if x.startswith(k + "|")) for k in ("LECH", "CHI_MC", "CHI_SA")}
        print("%-8s lệch/chéo %3d | chỉ MC %3d | chỉ SA %3d" % (c, dem["LECH"], dem["CHI_MC"], dem["CHI_SA"]))
