#!/usr/bin/env python3
"""XOA TAI KHOAN HOC SINH da ra truong - CHI DANH CHO ADMIN (co Lan).

CLAUDE THEM 09/10/2026 (co Lan duyet): chay tay trong terminal, khong co trang
web nao de lo chuc nang nay. Xoa SACH moi du lieu cua tung hoc sinh duoc chon:
  gia_su_hoi_dap, gia_su_luot, chat_history, exam_history (bai lam, diem),
  de_da_sinh + file_de + file tren dia, classroom_coursework, classroom_roster,
  profiles, va tai khoan dang nhap (Supabase Auth).

CHON hoc sinh theo KHOI (bat buoc) va tuy chon theo LOP. Chi chon tai khoan co
vai_tro = 'hoc_sinh' - KHONG BAO GIO dong vao giao vien / quan tri.

Mac dinh chi XEM TRUOC danh sach se xoa (khong xoa gi). Muon xoa that phai co
--xoa-that, roi go lai dung SO LUONG hoc sinh de xac nhan. KHONG hoan tac duoc.

Vi du (chay o THU MUC GOC project, can doc duoc .env):
  python3 scripts/xoa_hoc_sinh.py --khoi 12                      # xem truoc
  python3 scripts/xoa_hoc_sinh.py --khoi 12 --lop C1A,C1B        # xem truoc
  python3 scripts/xoa_hoc_sinh.py --khoi 12 --lop C1A --xoa-that # xoa that
"""
import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.supabase import supabase_admin as supabase  # noqa: E402
from app.services import history_service  # noqa: E402

# (bang, cot dinh danh hoc sinh) - xoa theo user_id
_BANG_THEO_USER_ID = [
    ("gia_su_hoi_dap", "user_id"),
    ("gia_su_luot", "user_id"),
    ("chat_history", "user_id"),
    ("exam_history", "student_id"),
]
# (bang, cot email) - xoa theo email hoc sinh
_BANG_THEO_EMAIL = [
    ("classroom_coursework", "student_email"),
    ("classroom_roster", "email"),
]


def tim_hoc_sinh(khoi: str, ds_lop: list[str] | None) -> list[dict]:
    """Moi phan tu: {id, ho_ten, khoi, lop}. Chi vai_tro = 'hoc_sinh'."""
    ket_qua, tu = [], 0
    while True:
        q = (supabase.table("profiles").select("id, ho_ten, khoi, lop, vai_tro")
             .eq("vai_tro", "hoc_sinh").eq("khoi", khoi))
        if ds_lop:
            q = q.in_("lop", ds_lop)
        lo = q.order("lop").range(tu, tu + 999).execute().data or []
        ket_qua += lo
        if len(lo) < 1000:
            return ket_qua
        tu += 1000


def lay_email(user_id: str) -> str | None:
    try:
        return supabase.auth.admin.get_user_by_id(user_id).user.email
    except Exception:
        return None


def xoa_mot_hoc_sinh(hs: dict) -> bool:
    """Xoa sach du lieu 1 hoc sinh. Tra ve True neu xoa xong ca tai khoan."""
    uid, email = hs["id"], hs.get("email")
    ok = True
    for bang, cot in _BANG_THEO_USER_ID:
        try:
            supabase.table(bang).delete().eq(cot, uid).execute()
        except Exception as e:
            print("    ! loi xoa %s: %s" % (bang, e)); ok = False
    if email:
        for bang, cot in _BANG_THEO_EMAIL:
            try:
                supabase.table(bang).delete().eq(cot, email).execute()
            except Exception as e:
                print("    ! loi xoa %s: %s" % (bang, e)); ok = False
    # de hoc sinh tu sinh (+ file_de + file tren dia)
    kq = history_service.xoa_de_cua_giao_vien(uid, None)
    if kq["khong_xoa_duoc"]:
        print("    ! %d de khong xoa duoc" % kq["khong_xoa_duoc"]); ok = False
    if not ok:
        print("    -> GIU lai profile/tai khoan vi con du lieu chua xoa het.")
        return False
    try:
        supabase.table("profiles").delete().eq("id", uid).execute()
        supabase.auth.admin.delete_user(uid)
    except Exception as e:
        print("    ! loi xoa profile / tai khoan dang nhap: %s" % e)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Xoa tai khoan hoc sinh da ra truong (admin).")
    ap.add_argument("--khoi", required=True, help='khoi can xoa, vd "12"')
    ap.add_argument("--lop", help='gioi han theo lop, cach nhau dau phay, vd "C1A,C1B"')
    ap.add_argument("--xoa-that", action="store_true", help="xoa that (mac dinh chi xem truoc)")
    a = ap.parse_args()
    ds_lop = [x.strip() for x in a.lop.split(",") if x.strip()] if a.lop else None

    ds = tim_hoc_sinh(a.khoi, ds_lop)
    if not ds:
        print("Khong co hoc sinh nao khop (khoi=%s, lop=%s)." % (a.khoi, ds_lop or "tat ca"))
        return 0
    for h in ds:
        h["email"] = lay_email(h["id"])
    print("Se xoa %d hoc sinh (khoi %s, lop %s):" % (len(ds), a.khoi, ", ".join(ds_lop) if ds_lop else "tat ca"))
    for h in ds:
        print("  - %-28s lop %-6s %s" % (h.get("ho_ten") or "(chua co ten)", h.get("lop") or "?", h.get("email") or "(khong doc duoc email)"))

    if not a.xoa_that:
        print("\nDAY CHI LA XEM TRUOC - chua xoa gi. Them --xoa-that de xoa that.")
        return 0
    if not sys.stdin.isatty():
        print("Can chay trong terminal de xac nhan. Dung lai."); return 1
    go = input("\nKHONG HOAN TAC DUOC. Go lai so luong hoc sinh (%d) de xac nhan xoa: " % len(ds)).strip()
    if go != str(len(ds)):
        print("Khong khop - HUY, chua xoa gi."); return 1

    xong = 0
    for i, h in enumerate(ds, 1):
        print("[%d/%d] %s (%s)" % (i, len(ds), h.get("ho_ten") or "?", h.get("email") or h["id"]))
        if xoa_mot_hoc_sinh(h):
            xong += 1
    print("\nDa xoa xong %d/%d hoc sinh." % (xong, len(ds)))
    return 0 if xong == len(ds) else 2


if __name__ == "__main__":
    sys.exit(main())
