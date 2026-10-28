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
NGUOI_DUYET = {e.strip().lower() for e in os.environ.get("EMAIL_DUYET_DANG", "nganhangdetoanchv@gmail.com").split(",")
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
    loi = kiem_chuan(cay, ten_ham)
    if loi:
        raise GuiDangError("Code chưa đúng chuẩn ngân hàng. Thầy/cô chép NGUYÊN các dòng dưới đây gửi lại Gem để sửa, "
                           "rồi dán code mới:\n- " + "\n- ".join(loi))
    canh_bao = sorted({d for d in DANG_NGO if d in code})
    la = [type(n).__name__ for n in cay.body
          if not isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom))
          and not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
    if la:
        canh_bao.append("có lệnh chạy ngoài hàm: " + ", ".join(sorted(set(la))))
    return {"ten_ham": ten_ham, "ten_khac": [t for t in ten if t not in ten_ham], "canh_bao": canh_bao}


# ---------------------------------------------------------------- kiểm chuẩn TĨNH (đọc cây cú pháp, không chạy)
# Cô Lan 28/10/2026: Gem trả code sai chuẩn (ID "L10_C2_B2_MC_A_01" không có đơn vị kiến thức, hàm không có socau,
# gọi MC_SA_answer_const(question=..., options=...) - tham số không tồn tại, import math_type ở đầu tệp). Bắt ngay lúc
# giáo viên gửi để giáo viên đưa lỗi lại cho Gem, không phải đợi cô tải về mới thấy.
_DV = r"(?:NB|TH|VD)\d{3}[A-Z]?"
MAU_ID_BAI = re.compile(r"^L(1[0-2])_C(\d+)_(B\d+)_(%s)_(MC|SA|TL)_[A-Z]_\d{2}$" % _DV)
MAU_ID_TF = re.compile(r"^L(1[0-2])_C(\d+)_TF_[A-Z]_\d{2}$")
MAU_ID_TL_HAI = re.compile(r"^L(1[0-2])_C(\d+)_(%s)_(%s)_TL_[A-Z]_\d{2}$" % (_DV, _DV))
THAM_SO = {"MC": ("dang", (1,)), "SA": ("dang", (2, 3)), "TF": ("socot", None), "TL": ("dong", None)}
SO_THAM_SO_HAM_CO_SAN = {"MC_SA_answer_const": 7, "MC_SA_answer_text": 7, "TF_baitoan_du": 5,
                         "TL_answer_text": 5, "TL_answer_const": 5}


def _curriculum(lop: str, chuong: str) -> set:
    tep = GOC / "data" / "curriculum" / ("toan" + lop) / ("L%s_C%s.json" % (lop, chuong))
    try:
        return {u["id"] for u in json.loads(tep.read_text(encoding="utf-8"))}
    except (OSError, ValueError, KeyError, TypeError):
        return set()


def _ham_da_co(lop: str, chuong: str) -> set:
    tep = GOC / "data" / "python_bank" / ("toan" + lop) / ("L%s_C%s.py" % (lop, chuong))
    try:
        return set(re.findall(r"^def (L\w+_\d{2})\(", tep.read_text(encoding="utf-8"), re.M))
    except OSError:
        return set()


def kiem_chuan(cay, ten_ham) -> list:
    """Các lỗi chuẩn (danh sách câu tiếng Việt); rỗng là đạt. Chỉ đọc cây cú pháp + data/ (không chạy code)."""
    loi = []
    ham = {n.name: n for n in cay.body if isinstance(n, ast.FunctionDef)}
    for n in cay.body:
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            ten_mod = n.module if isinstance(n, ast.ImportFrom) else ", ".join(a.name for a in n.names)
            if "math_type" in (ten_mod or ""):
                loi.append("Bỏ dòng import math_type: các hàm MC_SA_answer_const, TF_baitoan_du, TL_answer_text... "
                           "đã có sẵn trong tệp chương.")
            else:
                loi.append("Đặt lệnh import %s BÊN TRONG thân hàm, không để ở đầu tệp." % ten_mod)
    for ten in ten_ham:
        m = MAU_ID_BAI.match(ten) or MAU_ID_TF.match(ten) or MAU_ID_TL_HAI.match(ten)
        if not m:
            loi.append("Tên hàm %s sai chuẩn ID. Đúng: L10_C3_B6_TH032_MC_D_03 (lớp_chương_bài_mức độ + số yêu cầu cần "
                       "đạt_loại câu_chữ cái_số biến thể), Đúng/Sai: L10_C3_TF_A_03, Tự luận hai đơn vị: "
                       "L10_C3_TH031_TH032_TL_A_01. Tra số yêu cầu cần đạt trong danh_muc_ID." % ten)
        lop, chuong = (m.group(1), m.group(2)) if m else ("", "")
        cur = _curriculum(lop, chuong) if m else set()
        if not m:
            dv = []
        elif m.re is MAU_ID_BAI:
            dv = ["L%s_C%s_%s_%s" % (lop, chuong, m.group(3), m.group(4))]
        elif m.re is MAU_ID_TL_HAI:
            dv = []
            for don_vi in (m.group(3), m.group(4)):
                co = [d for d in cur if d.endswith("_" + don_vi)]
                dv.append(co[0] if co else "L%s_C%s_?_%s" % (lop, chuong, don_vi))
        else:
            dv = []
        for d in dv:
            if d not in cur:
                loi.append("%s: đơn vị kiến thức %s không có trong chương trình lớp %s chương %s. Chọn đúng mã trong "
                           "danh_muc_ID_lop%s.md." % (ten, d.replace("_?_", " ... "), lop, chuong, lop))
        if m and ten in _ham_da_co(lop, chuong):
            loi.append("%s: ngân hàng ĐÃ CÓ hàm tên này. Dùng số biến thể kế tiếp chưa có (hoặc chữ cái mới)." % ten)
        lc = re.search(r"_(MC|SA|TL|TF)_", ten)
        if not lc:
            continue
        loai = lc.group(1)
        f = ham[ten]
        ts = [a.arg for a in f.args.args]
        mac_dinh = f.args.defaults
        ten2, gt = THAM_SO[loai]
        mau = "(socau, %s%s)" % (ten2, "=%d" % gt[0] if gt else "=1")
        dung = len(ts) == 2 and ts[0] == "socau" and ts[1] == ten2 and len(mac_dinh) == 1
        if dung and gt:
            dung = isinstance(mac_dinh[0], ast.Constant) and mac_dinh[0].value in gt
        if not dung:
            loi.append("%s: khai báo phải là def %s%s:" % (ten, ten, mau))
        for c in ast.walk(f):
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in SO_THAM_SO_HAM_CO_SAN:
                can = SO_THAM_SO_HAM_CO_SAN[c.func.id]
                if c.keywords or len(c.args) != can:
                    mau_goi = {7: "(debai, dapso, dsnhieu, giai, 0, 0, dang)",
                               5: "(debai, ds_y, 0, 0, %s)" % ("socot" if c.func.id.startswith("TF") else "dong")}[can]
                    loi.append("%s: gọi %s sai tham số. Đúng: %s%s - đủ %d tham số theo thứ tự, không dùng tên=giá trị."
                               % (ten, c.func.id, c.func.id, mau_goi, can))
        if "socau" in ts and not any(isinstance(x, ast.Name) and x.id == "socau" for x in ast.walk(f)):
            loi.append("%s: phải sinh đủ socau câu (vòng lặp theo socau)." % ten)
    gon = []
    for x in loi:
        if x not in gon:
            gon.append(x)
    return gon[:20]


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
