#!/usr/bin/env bash
# Kiem tra may nay co du do nghe de dich hinh TikZ ra anh cho web hay khong.
# Chay tren VPS:   bash scripts/kiem_tra_hinh.sh
set -u
echo "== Cong cu =="
thieu=0
for t in xelatex pdfcrop; do
  if command -v "$t" >/dev/null; then printf "  %-12s co\n" "$t"
  else printf "  %-12s THIEU\n" "$t"; [ "$t" = xelatex ] && thieu=1; fi
done
echo "== Doi PDF sang anh (can it nhat MOT cai) =="
co_doi=0
for t in pdftocairo pdf2svg dvisvgm pdftoppm; do
  if command -v "$t" >/dev/null; then printf "  %-12s co\n" "$t"; co_doi=1
  else printf "  %-12s khong co\n" "$t"; fi
done
if [ "$co_doi" = 0 ]; then
  echo "  -> KHONG co cai nao. Cai dat:  apt-get install -y poppler-utils"
  thieu=1
fi
echo "== Dich thu mot hinh that =="
python3 - <<'PY'
import sys
sys.path.insert(0, ".")
from app.services.hinh_ve_service import dich_hinh, HinhVeError
tikz = r"\begin{tikzpicture}\draw (0,0)--(2,0)--(1,1.5)--cycle;\end{tikzpicture}"
try:
    p = dich_hinh(tikz)
    print("  OK ->", p, "(%d byte)" % p.stat().st_size)
except HinhVeError as e:
    print("  HONG:", e); sys.exit(1)
except Exception as e:
    print("  HONG:", type(e).__name__, e); sys.exit(1)
PY
ket=$?
[ "$thieu" = 1 ] && echo "=> Con thieu do nghe, hinh se KHONG hien tren web."
exit $ket
