#!/usr/bin/env python3
"""Xoa file de/PDF/tex cu hon 1 ngay trong data/exports, data/temp,
app/static/downloads. Chay hang ngay qua cron tren VPS. Khong xoa thu muc,
chi xoa file ben trong."""
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
THOI_GIAN_GIU = 24 * 60 * 60  # 1 ngay (tinh bang giay)

THU_MUC_CAN_DON = [
    BASE_DIR / "data" / "exports",
    BASE_DIR / "data" / "temp",
    BASE_DIR / "app" / "static" / "downloads",
]


def don_dep():
    bay_gio = time.time()
    tong_xoa = 0
    for thu_muc in THU_MUC_CAN_DON:
        if not thu_muc.exists():
            continue
        for f in thu_muc.iterdir():
            if not f.is_file():
                continue
            tuoi = bay_gio - f.stat().st_mtime
            if tuoi > THOI_GIAN_GIU:
                try:
                    f.unlink()
                    tong_xoa += 1
                except Exception as e:
                    print(f"Loi xoa {f}: {e}")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Da xoa {tong_xoa} file cu hon 1 ngay.")


if __name__ == "__main__":
    don_dep()
