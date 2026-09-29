#!/usr/bin/env bash
# Cai xelatex cho VPS de HINH VE hien duoc tren web.
#
# Chay TREN VPS:   bash /root/NganHangDe/scripts/cai_xelatex_vps.sh
#
# Vi sao can: app/services/hinh_ve_service.py dich ma TikZ cua tung cau
# ra anh PNG/SVG bang xelatex. VPS khong co xelatex thi cau co hinh se
# hien ra trong tron - hoc sinh mat mot nua de bai, cham diem sai muc do.
#
# Ban GON, khong cai texlive-full (khoang 5,5 GB). Danh sach duoi day du
# cho data/config/latex_template.tex va data/config/ex_test.sty:
#   texlive-xetex             xelatex
#   texlive-latex-extra       standalone, tcolorbox, ntheorem, xtab,
#                             paracol, answers, probsoln, cntformats,
#                             icomma (bo 'was')
#   texlive-pictures          tikz, pgfplots, tkz-euclide, tkz-tab,
#                             tikz-3dplot, bclogo
#   texlive-science           tabvar
#   texlive-fonts-recommended wasysym, rsfs
#   texlive-fonts-extra       esvect, yhmath (yhex), txfonts (txsyc),
#                             fontawesome
#   texlive-extra-utils       pdfcrop
#   poppler-utils             pdftocairo, pdftoppm (doi PDF sang anh)
set -e

echo "=== Cho trong o dia truoc da ==="
df -h / | sed -n '1,2p'
echo
echo "Bo goi nay chiem khoang 2,5 GB. Neu cot Avail con duoi 4 GB thi"
echo "DUNG lai, don dia truoc roi hay chay tiep."
echo
read -r -p "Cai tiep? (g/k) " tra_loi
case "$tra_loi" in
  g|G|y|Y) ;;
  *) echo "Da dung, chua cai gi."; exit 0 ;;
esac

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  texlive-xetex \
  texlive-latex-extra \
  texlive-pictures \
  texlive-science \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  texlive-extra-utils \
  poppler-utils

echo
echo "=== Kiem tra lai ==="
for lenh in xelatex pdfcrop pdftocairo pdftoppm; do
  if command -v "$lenh" >/dev/null 2>&1; then
    echo "  $lenh   co"
  else
    echo "  $lenh   VAN THIEU"
  fi
done

echo
echo "=== Dich thu mot hinh that ==="
THU_MUC_DU_AN="$(cd "$(dirname "$0")/.." && pwd)"
cd "$THU_MUC_DU_AN"
if [ -f scripts/kiem_tra_hinh.sh ]; then
  bash scripts/kiem_tra_hinh.sh || true
else
  echo "(khong thay scripts/kiem_tra_hinh.sh - bo qua buoc nay)"
fi

echo
echo "Xong. Neu van con bao thieu goi nao, cai rieng goi do bang:"
echo "   apt-get install -y texlive-full      # nang nhung chac chan du"
