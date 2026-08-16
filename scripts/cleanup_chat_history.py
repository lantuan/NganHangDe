#!/usr/bin/env python3
"""Xoa cac dong chat_history cu hon 10 ngay tren Supabase. Chay hang ngay
qua cron tren VPS (cung gio voi scripts/cleanup_old_files.py, 3h sang), o
DUNG thu muc goc project (can doc duoc .env qua app.core.config/supabase).

Ly do co script rieng, khong gop vao cleanup_old_files.py: file kia don
file vat ly tren dia (Path.iterdir), con day la xoa dong trong Database
(Supabase) - khac co che, khac quyen, nen tach rieng cho de theo doi log.
"""
import datetime
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.supabase import supabase  # noqa: E402

SO_NGAY_GIU = 10


def don_dep():
    han = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=SO_NGAY_GIU)
    han_iso = han.isoformat()

    try:
        ket_qua = (
            supabase.table("chat_history")
            .delete()
            .lt("created_at", han_iso)
            .execute()
        )
        so_dong = len(ket_qua.data) if ket_qua.data else 0
        print(
            f"[{time_now()}] Da xoa {so_dong} dong chat_history cu hon "
            f"{SO_NGAY_GIU} ngay (truoc {han_iso})."
        )
    except Exception as e:
        print(f"[{time_now()}] LOI XOA CHAT_HISTORY: {e}")


def time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    don_dep()