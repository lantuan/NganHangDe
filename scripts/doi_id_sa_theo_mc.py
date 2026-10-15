# -*- coding: utf-8 -*-
r"""Đổi chữ cái SA cho KHỚP chữ MC cùng "Dang" (cô Lan 14/10/2026) - chỉ đổi TÊN ID, không đổi thân hàm.

Chỉ xử lý nhóm "Dang" mà MC và SA cùng có nhưng KHÁC chữ (lỗi LECH của scripts/kiem_id_mc_sa.py), gồm cả chéo MC_G/SA_D.
Không đụng các dạng "chỉ MC" / "chỉ SA" (cần cô xem: cùng dạng khác cách ghi, hay thiếu thật).

  python scripts/doi_id_sa_theo_mc.py L10_C3            # in kế hoạch (không ghi)
  python scripts/doi_id_sa_theo_mc.py L10_C3 --ap-dung  # áp dụng toàn dự án (mapping, curriculum, ngân hàng vi/en, test, docs)

Đổi hai pha (qua thẻ tạm) để hoán vị chữ không đè nhau; ghi bảng cũ -> mới vào data/mapping/doi_id/<chương>_<ngày>.json.
"""
import json
import re
import string
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kiem_id_mc_sa as K  # noqa: E402

GOC = K.GOC


def chu_cai():
    for c in string.ascii_uppercase:
        yield c
    for a in string.ascii_uppercase:
        for b in string.ascii_uppercase:
            yield a + b


def ke_hoach(chuong: str) -> dict:
    """{ID SA cũ: ID SA mới}."""
    doi = {}
    for dv, cac_dang in K.nhom_theo_dang(chuong).items():
        tat_ca_mc = {l for g in cac_dang.values() for l in g["MC"]}
        tat_ca_sa = {l for g in cac_dang.values() for l in g["SA"]}
        moi = {}   # chữ SA cũ -> chữ SA mới
        for dang, g in cac_dang.items():
            chung = set(g["MC"]) & set(g["SA"])
            con_mc = sorted(set(g["MC"]) - chung)
            con_sa = sorted(set(g["SA"]) - chung)
            if not con_mc or not con_sa:
                continue
            if len(con_mc) != len(con_sa):
                # chữ MC và SA còn lại không bằng số lượng: ghép được bao nhiêu hay bấy nhiêu cần cô xác nhận -> bỏ qua
                if len(con_mc) != 1 or len(con_sa) < 1:
                    continue
            for s, l in zip(con_sa, con_mc):
                moi[s] = l
        # SA không đổi mà chữ bị chiếm làm đích bởi SA khác -> cấp chữ mới (không trùng MC nào, không trùng đích)
        dich = set(moi.values())
        cam = tat_ca_mc | dich | {s for s in tat_ca_sa if s not in moi}
        for s in sorted(tat_ca_sa):
            if s not in moi and s in dich:
                n = next(c for c in chu_cai() if c not in cam)
                moi[s] = n
                cam.add(n)
        # kiểm: ánh xạ đơn ánh trên toàn bộ SA của đơn vị
        cuoi = [moi.get(s, s) for s in tat_ca_sa]
        assert len(set(cuoi)) == len(cuoi), (dv, moi)
        for s, t in moi.items():
            if s != t:
                doi["%s_SA_%s" % (dv, s)] = "%s_SA_%s" % (dv, t)
    return doi


# Tệp được đổi: mọi nơi dùng ID của chương, TRỪ lịch sử (changelog, diff, patch, đề đã xuất, thư mục tạm, .git).
BO_QUA_THU_MUC = {".git", "__pycache__", ".pytest_cache", "exports", "exports_en", "temp", "temp_en", "uploads", "node_modules",
                  "Claude outputs", "skkn", "hinh_cache", "doi_id"}
BO_QUA_TEP = {"16_CHANGELOG.md"}
HAU_TO = {".py", ".json", ".md", ".tex", ".txt", ".html", ".js"}


def tep_can_doi():
    ra = []
    for f in GOC.rglob("*"):
        if not f.is_file() or f.suffix not in HAU_TO or f.name in BO_QUA_TEP:
            continue
        rel = f.relative_to(GOC).parts
        if any(p in BO_QUA_THU_MUC for p in rel) or f.name.endswith(".diff") or f.name.endswith(".patch"):
            continue
        ra.append(f)
    return ra


def ap_dung(doi: dict) -> dict:
    """Đổi hai pha trong mọi tệp. Trả về {tệp: số lần thay}."""
    cu = sorted(doi, key=len, reverse=True)
    the = {o: "@@DOIID%d@@" % i for i, o in enumerate(cu)}
    mau = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(re.escape(o) for o in cu) + r")(?![A-Za-z])")
    mau2 = re.compile("|".join(re.escape(t) for t in the.values()))
    nguoc = {t: doi[o] for o, t in the.items()}
    kq = {}
    for f in tep_can_doi():
        try:
            s = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if not mau.search(s):
            continue
        s2, n = mau.subn(lambda m: the[m.group(1)], s)
        s2 = mau2.sub(lambda m: nguoc[m.group(0)], s2)
        f.write_text(s2, encoding="utf-8")
        kq[str(f.relative_to(GOC))] = n
    return kq


if __name__ == "__main__":
    chuongs = [a for a in sys.argv[1:] if not a.startswith("--")]
    tong = {}
    for c in chuongs:
        d = ke_hoach(c)
        print(c, "số ID SA đổi:", len(d))
        tong[c] = d
    if "--ap-dung" in sys.argv:
        ra = GOC / "data" / "mapping" / "doi_id"
        ra.mkdir(parents=True, exist_ok=True)
        for c, d in tong.items():
            (ra / ("%s_%s.json" % (c, date.today().strftime("%Y%m%d")))).write_text(
                json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        gop = {o: n for d in tong.values() for o, n in d.items()}
        kq = ap_dung(gop)
        for f, n in sorted(kq.items()):
            print("  %4d  %s" % (n, f))
    else:
        for c, d in tong.items():
            for o, n in list(d.items())[:8]:
                print("   ", o, "->", n)
