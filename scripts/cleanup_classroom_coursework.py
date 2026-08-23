#!/usr/bin/env python3
"""Xoa cac bai da dang len Google Classroom (de/bai giai/diem cua hoc
sinh, xem app/services/classroom_service.py::dang_ket_qua_len_classroom)
cu hon 10 ngay - ca file tren Drive lan courseWorkMaterial tren Classroom,
dong thoi xoa dong tuong ung trong bang classroom_coursework. Chay hang
ngay qua cron tren VPS (cung 3h sang voi cleanup_chat_history.py va
cleanup_old_files.py), o DUNG thu muc goc project (can doc duoc .env qua
app.core.config/supabase)."""
import datetime
import sys
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.supabase import supabase  # noqa: E402
from app.services.classroom_service import (  # noqa: E402
    lay_refresh_token,
    lam_moi_access_token,
    CLASSROOM_API_BASE,
    DRIVE_API_BASE,
)

SO_NGAY_GIU = 10


def time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def don_dep():
    han = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=SO_NGAY_GIU)

    try:
        ket_qua = (
            supabase.table("classroom_coursework")
            .select("*")
            .lt("created_at", han.isoformat())
            .execute()
        )
    except Exception as e:
        print(f"[{time_now()}] LOI DOC CLASSROOM_COURSEWORK: {e}")
        return

    dong_can_xoa = ket_qua.data or []
    if not dong_can_xoa:
        print(f"[{time_now()}] Khong co bai Classroom nao can don dep.")
        return

    refresh_token = lay_refresh_token()
    if not refresh_token:
        print(f"[{time_now()}] Chua ket noi Classroom, bo qua don dep.")
        return

    try:
        access_token = lam_moi_access_token(refresh_token)
    except Exception as e:
        print(f"[{time_now()}] LOI LAM MOI ACCESS TOKEN: {e}")
        return

    so_xoa_ok = 0
    for dong in dong_can_xoa:
        # 1. Xoa courseWorkMaterial tren Classroom (khong chan neu loi -
        # van xoa tiep file Drive + dong Supabase, tranh ket qua don dep
        # dang do dang mai khong het).
        try:
            res = requests.delete(
                f"{CLASSROOM_API_BASE}/courses/{dong['course_id']}/courseWorkMaterials/{dong['coursework_id']}",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30,
            )
            if res.status_code not in (200, 204, 404):
                print(f"[{time_now()}] LOI XOA COURSEWORK {dong['coursework_id']}: {res.status_code} {res.text[:200]}")
        except Exception as e:
            print(f"[{time_now()}] LOI XOA COURSEWORK (exception) {dong['coursework_id']}: {e}")

        # 2. Xoa tung file tren Drive (de + loi giai).
        for fid in (dong.get("drive_file_ids") or []):
            try:
                res = requests.delete(
                    f"{DRIVE_API_BASE}/files/{fid}",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=30,
                )
                if res.status_code not in (200, 204, 404):
                    print(f"[{time_now()}] LOI XOA DRIVE FILE {fid}: {res.status_code} {res.text[:200]}")
            except Exception as e:
                print(f"[{time_now()}] LOI XOA DRIVE FILE (exception) {fid}: {e}")

        # 3. Xoa dong theo doi trong Supabase.
        try:
            supabase.table("classroom_coursework").delete().eq("id", dong["id"]).execute()
            so_xoa_ok += 1
        except Exception as e:
            print(f"[{time_now()}] LOI XOA DONG SUPABASE {dong['id']}: {e}")

    print(f"[{time_now()}] Da don dep {so_xoa_ok}/{len(dong_can_xoa)} bai Classroom cu hon {SO_NGAY_GIU} ngay.")


if __name__ == "__main__":
    don_dep()
