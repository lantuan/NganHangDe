"""Trích các đoạn chữ tiếng Việt hiển thị cho người dùng trong template (và router)
để dịch sang tiếng Anh. Kết quả: danh sách đoạn duy nhất, mỗi đoạn kèm số lần xuất hiện.

Dùng:  python3 scripts/i18n_trich_chuoi.py            # in thống kê
       python3 scripts/i18n_trich_chuoi.py --chua-dich # liệt kê đoạn chưa có trong data/i18n/en_ui.json
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
DAU = "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"
CO_DAU = re.compile("[" + DAU + DAU.upper() + "]")
# đoạn chữ liên tục, ngắt ở thẻ HTML, Jinja, nháy, xuống dòng, ${...}
DOAN = re.compile(r"[^<>{}\"'`\n\\$]+")


def trich_tu_van_ban(txt: str) -> list[str]:
    kq = []
    for m in DOAN.finditer(txt):
        d = " ".join(m.group(0).split())
        if CO_DAU.search(d) and len(d) >= 2:
            kq.append(d)
    return kq


def trich_template() -> Counter:
    c = Counter()
    for f in sorted((GOC / "app" / "templates").rglob("*.html")):
        txt = f.read_text(encoding="utf-8")
        txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)             # bỏ chú thích HTML
        txt = re.sub(r"(?m)^\s*//.*$", "", txt)                       # bỏ chú thích JS dòng đầu
        txt = re.sub(r"(?<![:\"'])//[^\n]*", "", txt)                 # bỏ chú thích JS cuối dòng
        txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
        txt = re.sub(r"\{#.*?#\}", "", txt, flags=re.S)               # chú thích Jinja
        c.update(trich_tu_van_ban(txt))
    return c


if __name__ == "__main__":
    c = trich_template()
    if "--chua-dich" in sys.argv:
        f = GOC / "data" / "i18n" / "en_ui.json"
        da = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        for k in sorted(c):
            if k not in da:
                print(k)
    else:
        print("đoạn duy nhất:", len(c), " tổng lần xuất hiện:", sum(c.values()))
