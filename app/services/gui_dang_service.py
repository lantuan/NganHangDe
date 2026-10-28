"""GỬI DẠNG - giáo viên gửi hàm Python (do Gem "Soạn dạng" viết) để cô Lan duyệt (28/10/2026).

Luồng (cô Lan chốt): giáo viên dùng Gem Gemini cô chia sẻ -> chép PHIẾU + CODE vào trang /gv/gui-dang ->
bài nằm ở hàng chờ -> cô vào /gv/duyet-dang tải code về máy, chạy thử (scripts/thu_dang_gui.py), tự đưa vào
ngân hàng như mọi lần rồi bấm "Đã duyệt" hoặc "Trả lại" kèm lời nhắn; giáo viên xem trạng thái ở trang của mình.

AN TOÀN: máy chủ KHÔNG BAO GIỜ chạy code giáo viên gửi. Chỉ đọc cú pháp (ast.parse) để lấy tên hàm và báo
những chỗ đáng ngờ cho người duyệt. Không ghi gì vào data/python_bank, data/mapping.

Lưu mỗi bài một tệp JSON trong data/gui_dang/ (không đẩy lên GitHub, xem .gitignore) - không cần bảng Supabase mới.
"""
import ast
import io
import json
import os
import re
import secrets
import threading
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent.parent
THU_MUC = GOC / "data" / "gui_dang"

# Tài khoản được duyệt: biến môi trường EMAIL_DUYET_DANG (nhiều email cách nhau dấu phẩy).
NGUOI_DUYET = {e.strip().lower() for e in os.environ.get("EMAIL_DUYET_DANG", "maihalan2605@gmail.com").split(",")
               if e.strip()}

# Đường liên kết Gem "Soạn dạng" cô chia sẻ (đặt GEM_SOAN_DANG_URL trong .env); trống thì trang không hiện nút.
GEM_URL = os.environ.get("GEM_SOAN_DANG_URL", "").strip()

TOI_DA_KI_TU_CODE = 200_000
TOI_DA_KI_TU_PHIEU = 5_000
TOI_DA_KI_TU_DE_GOC = 10_000
TOI_DA_MOI_NGAY = 30                     # mỗi giáo viên gửi tối đa 30 bài / ngày (chặn gửi nhầm hàng loạt)

TRANG_THAI = {"cho_duyet": "Chờ duyệt", "da_duyet": "Đã duyệt", "tra_lai": "Trả lại"}
MAU_TEN_HAM = re.compile(r"^L1[0-2]_C\d+_[A-Z0-9_]+_\d{2}$")
MAU_MA = re.compile(r"^\d{8}-\d{6}-[0-9a-f]{6}$")
# Chỉ là CẢNH BÁO cho người duyệt đọc kĩ (code không bao giờ chạy trên máy chủ).
DANG_NGO = ("open(", "eval(", "exec(", "compile(", "__import__", "subprocess", "os.", "sys.", "socket",
            "requests", "urllib", "shutil", "pathlib", "input(", "globals(", "setattr(")
MUI_VN = timezone(timedelta(hours=7))
_KHOA = threading.Lock()


class GuiDangError(ValueError):
    """Bài gửi không hợp lệ - thông báo đọc được cho giáo viên."""


def la_nguoi_duyet(email) -> bool:
    return bool(email) and str(email).strip().lower() in NGUOI_DUYET


def kiem_code(code: str) -> dict:
    """Đọc cú pháp (KHÔNG chạy). Trả {ten_ham, ten_khac, canh_bao}; sai thì raise GuiDangError."""
    code = (code or "").replace("\r\n", "\n").strip()
    if not code:
        raise GuiDangError("Chưa dán code Python.")
    if len(code) > TOI_DA_KI_TU_CODE:
        raise GuiDangError("Code dài quá (tối đa %d kí tự)." % TOI_DA_KI_TU_CODE)
    try:
        cay = ast.parse(code)
    except SyntaxError as e:
        raise GuiDangError("Code chưa đúng cú pháp Python (dòng %s: %s). Thầy/cô nhờ Gem sửa lại rồi gửi."
                           % (e.lineno, e.msg))
    ten = [n.name for n in cay.body if isinstance(n, ast.FunctionDef)]
    ten_ham = [t for t in ten if MAU_TEN_HAM.match(t)]
    if not ten_ham:
        raise GuiDangError("Không thấy hàm nào đặt tên theo ID ngân hàng (ví dụ L10_C3_B6_TH032_MC_H_01). "
                           "Thầy/cô chép đúng phần code Gem trả về.")
    canh_bao = sorted({d for d in DANG_NGO if d in code})
    la = [type(n).__name__ for n in cay.body
          if not isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom))
          and not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
    if la:
        canh_bao.append("có lệnh chạy ngoài hàm: " + ", ".join(sorted(set(la))))
    return {"ten_ham": ten_ham, "ten_khac": [t for t in ten if t not in ten_ham], "canh_bao": canh_bao}


def _tep(ma: str) -> Path:
    if not MAU_MA.match(ma or ""):
        raise GuiDangError("Mã bài gửi không hợp lệ.")
    return THU_MUC / (ma + ".json")


def _ghi(ban_ghi: dict):
    THU_MUC.mkdir(parents=True, exist_ok=True)
    p = _tep(ban_ghi["ma"])
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(ban_ghi, ensure_ascii=False, indent=1), encoding="utf-8")
    tam.replace(p)


def lay(ma: str) -> dict | None:
    try:
        return json.loads(_tep(ma).read_text(encoding="utf-8"))
    except (OSError, ValueError, GuiDangError):
        return None


def danh_sach(gv_id: str | None = None, trang_thai: str | None = None) -> list[dict]:
    if not THU_MUC.exists():
        return []
    kq = []
    for p in THU_MUC.glob("*.json"):
        try:
            b = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if gv_id and b.get("gv_id") != gv_id:
            continue
        if trang_thai and b.get("trang_thai") != trang_thai:
            continue
        kq.append(b)
    return sorted(kq, key=lambda b: b.get("ma", ""), reverse=True)


def gui(gv_id: str, gv_email: str, phieu: str, code: str, de_goc: str = "") -> dict:
    """Kiểm rồi lưu một bài gửi. Trả bản ghi."""
    phieu = (phieu or "").replace("\r\n", "\n").strip()
    de_goc = (de_goc or "").replace("\r\n", "\n").strip()
    if len(phieu) > TOI_DA_KI_TU_PHIEU or len(de_goc) > TOI_DA_KI_TU_DE_GOC:
        raise GuiDangError("Phiếu hoặc đề gốc dài quá.")
    kiem = kiem_code(code)
    bay_gio = datetime.now(MUI_VN)
    hom_nay = bay_gio.strftime("%Y%m%d")
    with _KHOA:
        da_gui = [b for b in danh_sach(gv_id=gv_id) if b.get("ma", "").startswith(hom_nay)]
        if len(da_gui) >= TOI_DA_MOI_NGAY:
            raise GuiDangError("Hôm nay thầy/cô đã gửi %d bài, mai gửi tiếp nhé." % len(da_gui))
        ban_ghi = {
            "ma": bay_gio.strftime("%Y%m%d-%H%M%S-") + secrets.token_hex(3),
            "luc_gui": bay_gio.strftime("%Y-%m-%d %H:%M"),
            "gv_id": gv_id, "gv_email": gv_email,
            "phieu": phieu, "code": code.replace("\r\n", "\n").strip() + "\n", "de_goc": de_goc,
            "ten_ham": kiem["ten_ham"], "ten_khac": kiem["ten_khac"], "canh_bao": kiem["canh_bao"],
            "trang_thai": "cho_duyet", "loi_nhan": "", "nguoi_duyet": "", "luc_duyet": "",
        }
        _ghi(ban_ghi)
    return ban_ghi


def dat_trang_thai(ma: str, trang_thai: str, loi_nhan: str, nguoi_duyet: str) -> dict:
    if trang_thai not in TRANG_THAI:
        raise GuiDangError("Trạng thái không hợp lệ.")
    with _KHOA:
        b = lay(ma)
        if b is None:
            raise GuiDangError("Không tìm thấy bài gửi %s." % ma)
        b.update(trang_thai=trang_thai, loi_nhan=(loi_nhan or "").strip()[:2000], nguoi_duyet=nguoi_duyet,
                 luc_duyet=datetime.now(MUI_VN).strftime("%Y-%m-%d %H:%M"))
        _ghi(b)
    return b


def tep_python(b: dict) -> str:
    """Tệp .py tải về máy cô: đầu tệp là phiếu (chú thích) + import như tệp chương, rồi code giáo viên gửi.
    Chạy thử: python3 scripts/thu_dang_gui.py nhap/gui_dang/<ma>.py"""
    dau = ["# BÀI GỬI DUYỆT %s - %s - %s" % (b["ma"], b.get("luc_gui", ""), b.get("gv_email", "")),
           "# Trạng thái: %s" % TRANG_THAI.get(b.get("trang_thai"), b.get("trang_thai")), "#"]
    dau += ["# " + d for d in (b.get("phieu") or "(không có phiếu)").splitlines()]
    if b.get("de_goc"):
        dau += ["#", "# ĐỀ GỐC:"] + ["#   " + d for d in b["de_goc"].splitlines()]
    if b.get("canh_bao"):
        dau += ["#", "# !! CẢNH BÁO (đọc kĩ trước khi chạy): " + "; ".join(b["canh_bao"])]
    dau += ["", "import math", "import random", "import numpy as np", "from math_type import *", "", ""]
    return "\n".join(dau) + b.get("code", "")


def zip_cho_duyet() -> bytes:
    bo = io.BytesIO()
    with zipfile.ZipFile(bo, "w", zipfile.ZIP_DEFLATED) as z:
        for b in danh_sach(trang_thai="cho_duyet"):
            z.writestr(b["ma"] + ".py", tep_python(b))
    return bo.getvalue()
