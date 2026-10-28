"""Xuất danh mục ID cho Gem "Soạn dạng" (cô Lan 28/10/2026).

Gem Gemini (do cô chia sẻ cho giáo viên) cần biết ngân hàng ĐANG CÓ gì để đề xuất đúng ID:
đơn vị kiến thức (Curriculum - YCCĐ của Bộ) và các dạng đã có (Mapping) cùng số biến thể trong Python.

Chạy:  python3 scripts/xuat_tai_lieu_gem.py
Ra:    docs/gem_soan_dang/danh_muc_ID_lop10.md, _lop11.md, _lop12.md
Sau mỗi lần thêm dạng mới vào ngân hàng, chạy lại rồi tải các tệp này lên Gem (thay bản cũ).
Chỉ ĐỌC data/, không sửa gì.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs" / "gem_soan_dang"
MUC = {"NB": "Biết", "TH": "Hiểu", "VD": "Vận dụng", "VDC": "Vận dụng cao"}


def _doc(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []


def _bien_the(lop, ten_tep):
    """{generator_id: [số biến thể _NN]} đọc từ tên hàm trong tệp Python của chương."""
    tep = GOC / "data" / "python_bank" / ("toan%d" % lop) / (ten_tep + ".py")
    kq = defaultdict(list)
    if tep.exists():
        for m in re.finditer(r"^def (L\d+_C\d+\w*?)_(\d{2})\(", tep.read_text(encoding="utf-8"), re.M):
            kq[m.group(1)].append(m.group(2))
    return kq


def _o(s):
    return str(s or "").replace("|", "/").replace("\n", " ").strip()


def xuat_lop(lop):
    dong = ["# Danh mục ID ngân hàng đề - Lớp %d" % lop, "",
            "Tự sinh bằng scripts/xuat_tai_lieu_gem.py từ data/curriculum + data/mapping + data/python_bank. "
            "Dùng để đề xuất ID: chọn ĐƠN VỊ KIẾN THỨC (Curriculum ID) đúng bài và đúng mức độ; nếu bài toán "
            "cùng dạng với một dòng đã có thì là BIẾN THỂ (số _NN kế tiếp), khác dạng thì là DẠNG MỚI "
            "(chữ cái kế tiếp chưa dùng của đơn vị đó, MC và SA cùng dạng dùng CÙNG chữ cái).", ""]
    for tep_cur in sorted((GOC / "data" / "curriculum" / ("toan%d" % lop)).glob("L*_C*.json"),
                          key=lambda p: int(re.search(r"_C(\d+)", p.stem).group(1))):
        cur = _doc(tep_cur)
        if not cur:
            continue
        mp = _doc(GOC / "data" / "mapping" / ("toan%d" % lop) / tep_cur.name)
        bt = _bien_the(lop, tep_cur.stem)
        dong += ["## Chương %s. %s" % (cur[0].get("chuong_so"), cur[0].get("chuong")), ""]
        theo_cur = defaultdict(list)
        tf, tl_nhieu = [], []
        for r in mp:
            i = r.get("id", "")
            if "_TF_" in i:
                tf.append(r)
            elif r.get("cac_y"):
                tl_nhieu.append(r)
            else:
                m = re.match(r"(L\d+_C\d+_B\d+_[A-Z]+\d+[A-Z]?)_", i)
                if m:
                    theo_cur[m.group(1)].append(r)
        bai_dang = None
        for u in cur:
            if u.get("bai_so") != bai_dang:
                bai_dang = u.get("bai_so")
                dong += ["### Bài %s. %s" % (bai_dang, u.get("bai")), ""]
            dong.append("- **%s** (%s): %s" % (u["id"], MUC.get(u.get("MucDo"), u.get("MucDo")), _o(u.get("content"))))
            for r in sorted(theo_cur.get(u["id"], []), key=lambda r: r["id"]):
                so = sorted(bt.get(r["id"], []))
                ghi = []
                if r.get("ngoai_yccd"):
                    ghi.append("ngoài YCCĐ")
                if r.get("boi_canh"):
                    ghi.append("bối cảnh: %s" % (", ".join(r["boi_canh"]) if isinstance(r["boi_canh"], list)
                                                 else r["boi_canh"]))
                dong.append("    - `%s` [%s] %s - biến thể: %s%s" % (
                    r["id"], _o(r.get("Loai")), _o(r.get("Dang")), ", ".join("_" + s for s in so) or "chưa có hàm",
                    (" (" + "; ".join(ghi) + ")") if ghi else ""))
        if tf:
            dong += ["", "### Đúng/Sai (theo chương)", ""]
            for r in sorted(tf, key=lambda r: r["id"]):
                dong.append("- `%s` %s - biến thể: %s" % (r["id"], _o(r.get("Dang")),
                                                          ", ".join("_" + s for s in sorted(bt.get(r["id"], []))) or "chưa có hàm"))
        if tl_nhieu:
            dong += ["", "### Tự luận nhiều đơn vị (theo chương)", ""]
            for r in sorted(tl_nhieu, key=lambda r: r["id"]):
                dong.append("- `%s` %s - biến thể: %s" % (r["id"], _o(r.get("Dang")),
                                                          ", ".join("_" + s for s in sorted(bt.get(r["id"], []))) or "chưa có hàm"))
        dong.append("")
    return "\n".join(dong) + "\n"


def main():
    RA.mkdir(parents=True, exist_ok=True)
    for lop in (10, 11, 12):
        p = RA / ("danh_muc_ID_lop%d.md" % lop)
        p.write_text(xuat_lop(lop), encoding="utf-8")
        print("Đã ghi", p.relative_to(GOC), "-", p.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
