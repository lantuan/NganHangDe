#!/usr/bin/env bash
# =====================================================================
#  day.sh  --  Day code len GitHub (va len VPS neu can)
#
#  Cach dung:
#     day          -> chi day len GitHub  (dung cho SKKN, tai lieu)
#     day web      -> day len GitHub + cap nhat VPS + kiem tra web
#     day -h       -> xem huong dan
#
#  Script tu tim thu muc du an nen goi tu dau cung duoc.
# =====================================================================
set -u

DOMAIN="nganhangdechv.tech"
VPS_USER="root"
VPS_DIR="/root/NganHangDe"
SERVICE="nganhangde"
NHANH="main"

xanh()  { printf "\033[1;32m%s\033[0m\n" "$*"; }
vang()  { printf "\033[1;33m%s\033[0m\n" "$*"; }
do_()   { printf "\033[1;31m%s\033[0m\n" "$*"; }
dam()   { printf "\033[1m%s\033[0m\n" "$*"; }

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  dam "day        -> day len GitHub"
  dam "day web    -> day len GitHub + cap nhat VPS + kiem tra web"
  exit 0
fi

# ---------- 1. Vao thu muc du an ----------
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$GOC" || { do_ "Khong vao duoc thu muc du an: $GOC"; exit 1; }
dam "Thu muc du an: $GOC"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  do_ "Thu muc nay khong phai kho git."; exit 1
fi

# ---------- 2. Kiem tra dang o nhanh nao ----------
HIENTAI="$(git branch --show-current)"
if [ "$HIENTAI" != "$NHANH" ]; then
  vang "Canh bao: dang o nhanh '$HIENTAI', khong phai '$NHANH'."
  read -r -p "Van day nhanh '$HIENTAI' len GitHub? (g/k) " tl
  [ "$tl" = "g" ] || { echo "Da dung."; exit 0; }
  NHANH="$HIENTAI"
fi

# ---------- 3. Con tep chua luu thi hoi ----------
if [ -n "$(git status --porcelain)" ]; then
  vang "Cac tep da sua nhung CHUA luu vao lich su (chua commit):"
  git status --short
  echo
  read -r -p "Luu tat ca roi day len? (g/k) " tl
  if [ "$tl" = "g" ]; then
    read -r -p "Mo ta ngan viec vua lam: " mota
    [ -n "$mota" ] || mota="Cap nhat $(date '+%d/%m/%Y %H:%M')"
    git add -A && git commit -q -m "$mota" || { do_ "Luu that bai."; exit 1; }
    xanh "Da luu: $mota"
  else
    vang "Bo qua cac tep chua luu -- chi day nhung gi da luu truoc do."
  fi
fi

# ---------- 4. Xem GitHub co thay doi moi hon khong ----------
echo "Dang kiem tra GitHub..."
if ! git fetch --quiet origin "$NHANH" 2>/dev/null; then
  vang "Khong hoi duoc GitHub (co the mang dang chap). Van thu day."
fi
SAU="$(git rev-list --count "origin/$NHANH..HEAD" 2>/dev/null || echo 0)"
TRUOC="$(git rev-list --count "HEAD..origin/$NHANH" 2>/dev/null || echo 0)"

if [ "$TRUOC" -gt 0 ]; then
  do_ "GitHub dang co $TRUOC thay doi moi hon may nay."
  vang "Phai lay ve truoc, neu khong se day that bai. Chay:  git pull --rebase origin $NHANH"
  exit 1
fi

if [ "$SAU" -eq 0 ]; then
  xanh "Khong co gi moi de day -- GitHub da khop voi may nay."
else
  dam "Sap day $SAU thay doi:"
  git --no-pager log --oneline "origin/$NHANH..HEAD" | sed 's/^/   /'
  echo
  if git push origin "$NHANH"; then
    xanh "Da day len GitHub xong."
  else
    do_ "Day len GitHub THAT BAI (xem loi o tren)."
    exit 1
  fi
fi

# ---------- 5. Neu khong yeu cau cap nhat web thi dung o day ----------
if [ "${1:-}" != "web" ]; then
  echo
  dam "Xong. Chua cap nhat VPS."
  echo "   (Chi khi sua code trong app/ data/ sql/ moi can chay:  day web)"
  exit 0
fi

# ---------- 6. Cap nhat VPS ----------
echo
dam "Dang cap nhat may chu $DOMAIN ..."
ssh -o ConnectTimeout=15 "$VPS_USER@$DOMAIN" bash -s <<VPSEOF
set -e
cd "$VPS_DIR"
git pull --ff-only
systemctl restart $SERVICE
sleep 3
echo "--- trang thai dich vu ---"
systemctl is-active $SERVICE
VPSEOF
KQ=$?

if [ $KQ -ne 0 ]; then
  do_ "Cap nhat VPS that bai. Ma nguon TREN GITHUB da moi, nhung web van dang chay ban cu."
  vang "Vao xem truc tiep:  ssh $VPS_USER@$DOMAIN  roi  journalctl -u $SERVICE -n 50"
  exit 1
fi

# ---------- 6b. Kiem tra do nghe ve hinh tren VPS ----------
# Cau co hinh ve chi hien duoc tren web khi VPS co xelatex VA mot cong cu
# doi PDF sang anh. Kiem ngay o day de khong phai nho chay tay, va nho
# dung thu muc (chay o /root se khong thay script).
echo
echo "Dang kiem tra do nghe ve hinh tren VPS..."
HINH="$(ssh -o ConnectTimeout=15 "$VPS_USER@$DOMAIN" \
  "cd $VPS_DIR && bash scripts/kiem_tra_hinh.sh 2>&1" || true)"
if echo "$HINH" | grep -q "Du do nghe"; then
  xanh "Hinh ve: du do nghe, hoc sinh xem duoc hinh tren web."
else
  vang "Hinh ve: VPS CHUA du do nghe -- cau co hinh se khong hien tren web."
  echo "$HINH" | sed 's/^/     /'
  vang "Cach sua:  ssh $VPS_USER@$DOMAIN  roi  apt-get install -y poppler-utils"
fi

# ---------- 7. Kiem tra web con song ----------
echo
echo "Dang kiem tra web..."
MA="$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAIN" || echo 000)"
if [ "$MA" = "200" ] || [ "$MA" = "302" ] || [ "$MA" = "307" ]; then
  xanh "Web tra ve $MA -- dang chay binh thuong."
  xanh "XONG: GitHub da moi, VPS da cap nhat, web da kiem tra."
else
  do_ "Web tra ve $MA -- co the dang loi."
  vang "Xem nhat ki:  ssh $VPS_USER@$DOMAIN  roi  journalctl -u $SERVICE -n 50"
  exit 1
fi
