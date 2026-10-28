#!/usr/bin/env python3
"""Chạy thử bài giáo viên GỬI DẠNG (cô Lan 28/10/2026) - trên MÁY CÔ, trước khi đưa vào ngân hàng.

Dùng (đứng ở thư mục gốc dự án):

    python3 scripts/thu_dang_gui.py nhap/gui_dang/20261028-091500-a1b2c3.py
    python3 scripts/thu_dang_gui.py nhap/gui_dang/<mã>.py -n 50          # chạy 50 bộ số
    python3 scripts/thu_dang_gui.py nhap/gui_dang/<mã>.py --khong-pdf

Tệp .py tải ở trang /gv/duyet-dang (nút "Tải .py" hoặc "Tải tất cả", giải nén vào nhap/gui_dang/).
Script KHÔNG sửa ngân hàng. Với mỗi hàm tên theo ID:
  - chạy nhiều bộ số (mặc định 30), bắt lỗi;
  - kiểm đúng loại câu (như lúc ra đề: generator_service.kiem_tra_dung_loai_cau);
  - tham số thứ hai đúng tên/mặc định (MC dang=1, SA dang=2/3, TF socot, TL dong);
  - SA: đáp số tối đa 4 kí tự;  TF: mỗi ý >= 3 phát biểu đúng, >= 3 sai, có bốn mốc "# a) NB"... ;
  - đề có thật sự đổi số không (ít bản khác nhau = "đề chết");
rồi ghi bản nháp nhap/gui_dang/<mã>_dethi.tex/.pdf và _loigiai.tex/.pdf để soi bằng mắt.
"""
import argparse
import importlib.util
import inspect
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "data" / "python_bank"))

import math_type  # noqa: E402
from app.services.generator_service import _call_generator_function, kiem_tra_dung_loai_cau  # noqa: E402
from app.services.lam_dep_bieu_thuc import lam_dep  # noqa: E402
from app.services.latex_service import build_latex_document  # noqa: E402

MAU_TEN = re.compile(r"^L(1[0-2])_C(\d+)_[A-Z0-9_]+_\d{2}$")
MOC_TF = ("# a) NB", "# b) TH", "# c) VD", "# d) VDC")


def _nap(tep: Path):
    spec = importlib.util.spec_from_file_location("gui_dang_" + re.sub(r"\W", "_", tep.stem), tep)
    mo = importlib.util.module_from_spec(spec)
    mo.__dict__.update({k: v for k, v in vars(math_type).items() if not k.startswith("__")})
    spec.loader.exec_module(mo)
    return mo


def _seed(s):
    random.seed(s)
    try:
        import numpy as np
        np.random.seed(s)
    except ImportError:
        pass


def _dap_so_sa(latex):
    kq = []
    for m in re.finditer(r"\\shortans(?:\[\d+\])?\{\s*(.*?)\}\s*$", latex, re.M):
        t = m.group(1).strip().strip("$").replace("{,}", ",").replace(" ", "")
        kq.append(t)
    return kq


def kiem_ham(mo, ten, so_lan):
    loi, canh_bao = [], []
    f = getattr(mo, ten)
    gid = ten[:-3]
    ts = list(inspect.signature(f).parameters.values())
    loai = re.search(r"_(MC|SA|TF|TL)_", ten)
    loai = loai.group(1) if loai else "?"
    mong = {"MC": ("dang", 1), "SA": ("dang", (2, 3)), "TF": ("socot", None), "TL": ("dong", None)}.get(loai)
    if mong and (len(ts) < 2 or ts[1].name != mong[0]
                 or (mong[1] is not None and ts[1].default not in (mong[1] if isinstance(mong[1], tuple) else (mong[1],)))):
        loi.append("tham số thứ hai phải là %s%s" % (mong[0], "" if mong[1] is None else "=%s" % (mong[1],)))
    nguon = inspect.getsource(f)
    if loai == "TF":
        thieu = [m for m in MOC_TF if m not in nguon]
        if thieu:
            loi.append("thiếu mốc độ khó trong thân hàm: %s" % ", ".join(thieu))

    bat_tf = []
    goc_tf = mo.__dict__.get("TF_baitoan_du")
    if goc_tf is not None:
        def _tf(debai, ds_abcd, *a, **k):
            bat_tf.append(ds_abcd)
            return goc_tf(debai, ds_abcd, *a, **k)
        mo.TF_baitoan_du = _tf
    khac = set()
    try:
        for s in range(so_lan):
            _seed(s)
            try:
                out = _call_generator_function(f, 1, None, None)
                kiem_tra_dung_loai_cau(gid, out)
            except Exception as e:  # noqa: BLE001 - báo mọi lỗi cho người duyệt
                loi.append("bộ số %d: %s: %s" % (s, type(e).__name__, str(e)[:200]))
                continue
            khac.add(out)
            if loai == "SA":
                for d in _dap_so_sa(out):
                    if len(d) > 4:
                        loi.append("bộ số %d: đáp số trả lời ngắn '%s' quá 4 kí tự" % (s, d))
    finally:
        if goc_tf is not None:
            mo.TF_baitoan_du = goc_tf
    if loai == "TF":
        for ds in bat_tf[:1]:
            for i, y in enumerate(ds):
                dung = sum(1 for p in y if "\\True" in p[0])
                sai = len(y) - dung
                if dung < 3 or sai < 3:
                    loi.append("ý %s) có %d phát biểu đúng, %d sai (cần >= 3 mỗi loại)" % ("abcd"[i], dung, sai))
    if so_lan >= 10 and len(khac) < min(5, so_lan // 3):
        canh_bao.append("chỉ ra %d đề khác nhau sau %d lần chạy - số liệu có thật sự ngẫu nhiên?" % (len(khac), so_lan))
    # gộp lỗi trùng nội dung (khác mỗi số bộ) cho dễ đọc: "(gặp ở 12/30 bộ số) ..."
    dem = {}
    for x in loi:
        k = re.sub(r"^bộ số \d+: ", "", x)
        dem[k] = dem.get(k, 0) + (1 if k != x else 0)
    gon = [("(gặp ở %d/%d bộ số) %s" % (n, so_lan, k)) if n else k for k, n in dem.items()]
    return gon[:15], canh_bao


def main():
    ap = argparse.ArgumentParser(description="Chạy thử bài giáo viên gửi dạng")
    ap.add_argument("tep", help="tệp .py tải từ trang Duyệt dạng")
    ap.add_argument("-n", "--so-lan", type=int, default=30, help="số bộ số chạy thử (mặc định 30)")
    ap.add_argument("--khong-pdf", action="store_true", help="chỉ kiểm, không ghi bản nháp .tex/.pdf")
    ts = ap.parse_args()
    tep = Path(ts.tep).resolve()
    if not tep.exists():
        sys.exit("Không thấy tệp %s" % ts.tep)
    try:
        mo = _nap(tep)
    except Exception as e:  # noqa: BLE001
        sys.exit("Không nạp được tệp (lỗi khi đọc code): %s: %s" % (type(e).__name__, e))
    cac_ham = [t for t, v in vars(mo).items() if callable(v) and MAU_TEN.match(t) and getattr(v, "__module__", "") == mo.__name__]
    if not cac_ham:
        sys.exit("Tệp không có hàm nào đặt tên theo ID (L10_C3_..._01).")

    dat = True
    for ten in cac_ham:
        loi, cb = kiem_ham(mo, ten, ts.so_lan)
        print(("ĐẠT       " if not loi else "CHƯA ĐẠT  ") + ten)
        for x in loi:
            print("   - " + x)
        for x in cb:
            print("   ~ " + x)
        dat = dat and not loi

    if not ts.khong_pdf:
        sys.path.insert(0, str(GOC / "scripts"))
        import nhap  # dùng lại hàm biên dịch của scripts/nhap.py
        lop = int(MAU_TEN.match(cac_ham[0]).group(1))
        khoi = []
        for ten in cac_ham:
            _seed(1)
            try:
                latex = lam_dep(_call_generator_function(getattr(mo, ten), 3, None, None))
            except Exception as e:  # noqa: BLE001
                print("   (không ghi nháp %s: %s)" % (ten, e))
                continue
            khoi.append("\\noindent\\textbf{NHÁP: %s}\\par\\medskip\n%s" % (ten.replace("_", r"\_"), latex))
        if khoi:
            ra = GOC / "nhap" / "gui_dang"
            ra.mkdir(parents=True, exist_ok=True)
            for kieu in ("dethi", "loigiai"):
                t = ra / ("%s_%s.tex" % (tep.stem, kieu))
                t.write_text(build_latex_document("NHAP", "\n\\bigskip\n".join(khoi), lop=lop, role="teacher",
                                                  ex_test_option=kieu), encoding="utf-8")
                print("Đã ghi %s" % t.relative_to(GOC), end="")
                print(" + .pdf" if nhap._bien_dich(t) else "")
    print("\nKẾT LUẬN: %s" % ("ĐẠT - đưa vào ngân hàng như mọi lần (tệp chương, Mapping, test)." if dat
                             else "CHƯA ĐẠT - trả lại giáo viên kèm lỗi ở trên."))
    sys.exit(0 if dat else 1)


if __name__ == "__main__":
    main()
