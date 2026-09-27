#!/usr/bin/env bash
# Kiem tra may nay co du do nghe de dich hinh TikZ ra anh cho web hay khong.
#
# LUU Y: web chay tren VPS, nen cai can kiem tra la VPS chu khong phai may
# Mac. Chay tren VPS:
#     ssh root@nganhangdechv.tech
#     cd /root/NganHangDe && bash scripts/kiem_tra_hinh.sh
set -u

echo "== May dang kiem tra =="
echo "  ten may : $(hostname)"
echo "  thu muc : $(pwd)"
if [ -d /root/NganHangDe ] && [ "$(id -u)" = 0 ]; then
  echo "  -> trong nhu VPS. Dung may can kiem tra."
else
  echo "  -> KHONG PHAI VPS. Web chay tren VPS, nho chay lai lenh nay o do:"
  echo "     ssh root@nganhangdechv.tech"
  echo "     cd /root/NganHangDe && bash scripts/kiem_tra_hinh.sh"
fi

echo
echo "== Cong cu =="
thieu=0
for t in xelatex pdfcrop; do
  if command -v "$t" >/dev/null; then printf "  %-12s co\n" "$t"
  else
    printf "  %-12s THIEU\n" "$t"
    [ "$t" = xelatex ] && thieu=1
  fi
done

echo
echo "== Doi PDF sang anh =="
co_doi=0
for t in pdftocairo pdf2svg dvisvgm pdftoppm; do
  if command -v "$t" >/dev/null; then printf "  %-12s co\n" "$t"; co_doi=$((co_doi+1))
  else printf "  %-12s khong co\n" "$t"; fi
done
if [ "$co_doi" = 0 ]; then
  echo "  -> KHONG co cai nao, hinh se KHONG hien tren web."
  echo "     Cai dat:  apt-get install -y poppler-utils"
  thieu=1
elif [ "$co_doi" = 1 ]; then
  echo "  -> Chi co MOT cong cu. Van chay duoc, nhung:"
  echo "     . khong co cai du phong neu no dich hong mot hinh nao do"
  echo "     . khong chon duoc dinh dang nhe nhat cho hoc sinh mo bang 3G"
  echo "     Nen cai them:  apt-get install -y poppler-utils   (Mac: brew install poppler)"
fi

echo
echo "== Dich thu mot hinh that =="
python3 - <<'PY'
import sys
sys.path.insert(0, ".")
from app.services.hinh_ve_service import dich_hinh, HinhVeError
tikz = r"\begin{tikzpicture}\draw (0,0)--(2,0)--(1,1.5)--cycle;\end{tikzpicture}"
try:
    p = dich_hinh(tikz)
    print("  OK -> %s (%d byte, dinh dang %s)" % (p.name, p.stat().st_size, p.suffix[1:]))
except HinhVeError as e:
    print("  HONG:", e); sys.exit(1)
except Exception as e:
    print("  HONG:", type(e).__name__, e); sys.exit(1)
PY
ket=$?

echo
if [ "$thieu" = 1 ] || [ "$ket" != 0 ]; then
  echo "=> CHUA XONG: hinh se khong hien tren web."
else
  echo "=> Du do nghe. Hinh se hien duoc tren web."
fi
exit $ket
