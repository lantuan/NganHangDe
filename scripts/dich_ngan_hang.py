"""
Dịch ngân hàng câu hỏi sang tiếng Anh (cô Lan 03/10/2026) - dịch THEO NGUỒN, không đoán lúc chạy.

Quy trình:
  1. trich(file)        -> các "đơn vị dịch": chuỗi chữ (str) hoặc f-string có tiếng Việt, mỗi đơn vị là
                           ĐÚNG đoạn mã nguồn của nó (vd  r"Cho $%s$ và $%s$."  hoặc  f"Cho {a} và {b}").
  2. Người / AI dịch     -> data/i18n/bank/en_<tệp>.json : {đoạn nguồn tiếng Việt: đoạn nguồn tiếng Anh}.
                           Đoạn tiếng Anh phải là biểu thức chuỗi Python hợp lệ, GIỮ NGUYÊN %s %d {biểu thức} và LaTeX.
  3. dich(file)          -> thay từng đoạn nguồn bằng bản dịch, GIỮ NGUYÊN định dạng phần còn lại của tệp ->
                           data/python_bank_en/<khối>/<tệp>.py  (thư mục tiếng Anh riêng, khác tiếng Việt).

Logic (so sánh, khoá từ điển, thứ tự random) không đổi vì chỉ đổi chữ. Test so hai bản cùng hạt giống.
"""
import ast
import json
import re
import sys
from pathlib import Path

DAU = "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"
CO_DAU = re.compile("[" + DAU + DAU.upper() + "]")
GOC = Path(__file__).resolve().parents[1]
TU_DIEN_DIR = GOC / "data" / "i18n" / "bank"
NGUON_DIR = GOC / "data" / "python_bank"
DICH_DIR = GOC / "data" / "python_bank_en"


def _docstrings(tree):
    ds = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = n.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                ds.add(id(b[0].value))
    return ds


def _co_tieng_viet(n) -> bool:
    if isinstance(n, ast.Constant):
        return isinstance(n.value, str) and bool(CO_DAU.search(n.value))
    if isinstance(n, ast.JoinedStr):
        return any(isinstance(v, ast.Constant) and CO_DAU.search(v.value) for v in n.values)
    return False


def _doan(bd, n) -> str:
    """Đoạn mã nguồn của nút n (bd: các dòng dạng bytes)."""
    if n.lineno == n.end_lineno:
        return bd[n.lineno - 1][n.col_offset:n.end_col_offset].decode("utf-8")
    d = [bd[n.lineno - 1][n.col_offset:]] + bd[n.lineno:n.end_lineno - 1] + [bd[n.end_lineno - 1][:n.end_col_offset]]
    return b"\n".join(d).decode("utf-8")


def don_vi(src: str):
    """[(node, đoạn nguồn, kiểu 'str'|'fstr')] theo thứ tự xuất hiện; bỏ docstring và
    chuỗi con nằm TRONG f-string (đã tính chung vào f-string)."""
    tree = ast.parse(src)
    doc = _docstrings(tree)
    trong_f = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.JoinedStr):
            for c in ast.walk(n):
                if c is not n:
                    trong_f.add(id(c))
    kq = []
    bd = [d.encode("utf-8") for d in src.split("\n")]
    for n in ast.walk(tree):
        if id(n) in doc or id(n) in trong_f or not _co_tieng_viet(n):
            continue
        seg = _doan(bd, n)
        if seg:
            kq.append((n, seg, "fstr" if isinstance(n, ast.JoinedStr) else "str"))
    kq.sort(key=lambda t: (t[0].lineno, t[0].col_offset))
    return kq


def trich(duong_dan):
    """{đoạn nguồn: {'lines': [dòng đầu...], 'kieu': ...}} duy nhất."""
    src = Path(duong_dan).read_text(encoding="utf-8")
    kq = {}
    for n, seg, kieu in don_vi(src):
        e = kq.setdefault(seg, {"lines": [], "kieu": kieu})
        if len(e["lines"]) < 3:
            e["lines"].append(n.lineno)
    return kq


# ---------- kiểm tra bản dịch ----------
_PH = re.compile(r"%[-+ 0#]*\d*(?:\.\d+)?[sdfrxXeEgGi%]")


def _gia_tri(seg: str):
    """Giá trị chuỗi của một đoạn nguồn (str) -> str; (f-string) -> (các phần chữ, các biểu thức)."""
    seg = "(" + seg.strip() + ")"
    nut = ast.parse(seg, mode="eval").body
    if isinstance(nut, ast.Constant):
        return nut.value, []
    if isinstance(nut, ast.JoinedStr):
        chu = "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in nut.values)
        # chuỗi chữ nằm TRONG biểu thức (vd {"đúng" if x else "sai"}) được phép dịch: so sánh sau khi che chuỗi
        bt = sorted(re.sub(r"\"[^\"]*\"|'[^']*'", '""', ast.get_source_segment(seg, v.value))
                    for v in nut.values if isinstance(v, ast.FormattedValue))
        return chu, bt
    raise ValueError("không phải chuỗi")


def kiem_tra(vi_seg: str, en_seg: str) -> list[str]:
    """Danh sách lỗi (rỗng = hợp lệ): cùng %s %d, cùng biểu thức f-string, cùng $...$ về số lượng,
    cùng lệnh LaTeX (trừ trong \\text{}), không còn dấu tiếng Việt."""
    loi = []
    try:
        vv, vb = _gia_tri(vi_seg)
        ev, eb = _gia_tri(en_seg)
    except Exception as e:
        return ["không phải biểu thức chuỗi hợp lệ: %s" % e]
    if _PH.findall(vv) != _PH.findall(ev):
        loi.append("%%-placeholder khác: %s -> %s" % (_PH.findall(vv), _PH.findall(ev)))
    if vb != eb:
        loi.append("biểu thức f-string khác: %s -> %s" % (vb, eb))
    if vv.count("$") != ev.count("$"):
        loi.append("số dấu $ khác (%d -> %d)" % (vv.count("$"), ev.count("$")))
    if vv.count("{}") != ev.count("{}") and "{}" in vv:
        loi.append("số {} khác")
    lenh = lambda s: sorted(re.findall(r"(?<!\\)\\[A-Za-z]+", re.sub(r"\\text\{[^{}]*\}|\\mathrm\{[^{}]*\}", "", s)))
    if lenh(vv) != lenh(ev):
        loi.append("lệnh LaTeX khác: %s -> %s" % (lenh(vv), lenh(ev)))
    if CO_DAU.search(ev):
        loi.append("còn dấu tiếng Việt")
    return loi


# ---------- áp dụng ----------
def dich(duong_dan, tu_dien: dict, ra=None):
    """Trả về mã nguồn đã thay chữ. tu_dien: {nguồn Việt: nguồn Anh}. Đoạn chưa dịch giữ nguyên
    và được liệt kê trong biến trả về thứ hai."""
    src = Path(duong_dan).read_text(encoding="utf-8")
    dong = src.split("\n")
    # vị trí byte -> dòng/cột: dùng (lineno, col_offset) theo UTF-8, nên làm việc trên bytes từng dòng
    bd = [d.encode("utf-8") for d in dong]
    thay = []
    chua = []
    for n, seg, kieu in don_vi(src):
        en = tu_dien.get(seg)
        if en is None:
            chua.append(seg)
            continue
        thay.append((n.lineno - 1, n.col_offset, n.end_lineno - 1, n.end_col_offset, en))
    for l0, c0, l1, c1, en in sorted(thay, reverse=True):
        dau = bd[l0][:c0]
        cuoi = bd[l1][c1:]
        bd[l0:l1 + 1] = [dau + en.encode("utf-8") + cuoi]
    kq = b"\n".join(bd).decode("utf-8")
    if ra:
        Path(ra).parent.mkdir(parents=True, exist_ok=True)
        Path(ra).write_text(kq, encoding="utf-8")
    return kq, chua


def tai_tu_dien(stem: str):
    """(từ điển, danh sách sửa tay). Sửa tay = chỗ MÃ phụ thuộc chữ Việt không có dấu (vd "sai", cắt chuỗi
    theo "cho } ") nên không tự trích được: [{"tim": nguồn, "thay": nguồn Anh, "so_lan": n}]."""
    f = TU_DIEN_DIR / ("en_%s.json" % stem)
    td = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    # patch_<stem>.json rồi patch_<stem>_2.json, _3... (áp dụng lần lượt, mỗi tệp một đợt rà soát)
    patch = []
    ds = [TU_DIEN_DIR / ("patch_%s.json" % stem)] + sorted(TU_DIEN_DIR.glob("patch_%s_*.json" % stem))
    for fp in ds:
        if fp.exists():
            patch += json.loads(fp.read_text(encoding="utf-8"))
    return td, patch


def dich_tep(nguon: Path, ra: Path | None = None):
    """Dịch một tệp ngân hàng. Trả về (mã nguồn Anh, đoạn chưa dịch, lỗi)."""
    td, patch = tai_tu_dien(nguon.stem)
    giu = {k for k, v in td.items() if v == "__GIU__"}
    td = {k: v for k, v in td.items() if v != "__GIU__"}
    loi = []
    for k, v in td.items():
        for e in kiem_tra(k, v):
            loi.append((k[:70].replace("\n", " "), e))
    src, chua = dich(nguon, td)
    chua = [c for c in chua if c not in giu]
    for p in patch:
        n = src.count(p["tim"])
        if p.get("tat_ca"):          # thay MỌI chỗ (cần ít nhất một)
            if n < 1:
                loi.append((p["tim"][:70], "sửa tay: không tìm thấy"))
                continue
            src = src.replace(p["tim"], p["thay"])
            continue
        if n != p.get("so_lan", 1):
            loi.append((p["tim"][:70], "sửa tay: tìm thấy %d chỗ, cần %d" % (n, p.get("so_lan", 1))))
            continue
        src = src.replace(p["tim"], p["thay"])
    try:
        ast.parse(src)
    except SyntaxError as e:
        loi.append(("<tệp>", "bản dịch không biên dịch được: %s" % e))
    if ra:
        Path(ra).parent.mkdir(parents=True, exist_ok=True)
        Path(ra).write_text(src, encoding="utf-8")
    return src, chua, loi


def duong_dan_dich(nguon: Path) -> Path:
    return DICH_DIR / nguon.parent.name / nguon.name


if __name__ == "__main__":
    lenh, f = (sys.argv[1], Path(sys.argv[2])) if len(sys.argv) > 2 else ("trich", Path(sys.argv[1]))
    if lenh == "trich":
        t = trich(f)
        print(len(t), "đoạn duy nhất;", sum(1 for v in t.values() if v["kieu"] == "fstr"), "f-string;",
              sum(len(k) for k in t), "ký tự nguồn")
    elif lenh == "dich":
        src, chua, loi = dich_tep(f, duong_dan_dich(f))
        print("ghi", duong_dan_dich(f), "| chưa dịch:", len(chua), "| lỗi:", len(loi))
        for c in chua[:20]:
            print("  CHUA:", c[:100].replace("\n", " "))
        for k, e in loi[:30]:
            print("  LOI:", k, "->", e)
    else:
        sys.exit("dùng: dich_ngan_hang.py [trich|dich] <tệp ngân hàng>")
