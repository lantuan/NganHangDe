#!/usr/bin/env bash
# =====================================================================
#  ma_moi.sh  --  Xem MA MOI dang ky tai khoan GIAO VIEN dat tren VPS
#
#  Cach dung:
#     mamoi        -> in ra ma moi giao vien hien dang dat tren VPS
#     mamoi -h     -> xem huong dan
#
#  Ma moi KHONG nam trong kho ma nguon va KHONG nam trong tai lieu -
#  co y nhu vay. No chi nam trong tep .env tren VPS (bien
#  MA_MOI_GIAO_VIEN, xem app/core/config.py va app/routers/auth.py).
#  De trong thi KHONG ai dang ky duoc giao vien.
#
#  Script tu tim thu muc du an nen goi tu dau cung duoc.
# =====================================================================
set -u

DOMAIN="nganhangdechv.tech"
VPS_USER="root"
VPS_DIR="/root/NganHangDe"
SERVICE="nganhangde"

xanh()  { printf "\033[1;32m%s\033[0m\n" "$*"; }
vang()  { printf "\033[1;33m%s\033[0m\n" "$*"; }
do_()   { printf "\033[1;31m%s\033[0m\n" "$*"; }
dam()   { printf "\033[1m%s\033[0m\n" "$*"; }

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  dam "mamoi      -> in ra ma moi giao vien dang dat tren VPS"
  echo
  echo "Doi ma moi: sua dong MA_MOI_GIAO_VIEN trong $VPS_DIR/.env tren"
  echo "VPS roi chay  systemctl restart $SERVICE  - khong can day ma nguon."
  exit 0
fi

dam "Dang hoi may chu $DOMAIN ..."

# KHONG dat heredoc ben trong $( ... ): bash 3.2 (ban di kem macOS) doc ca
# than heredoc de tim dau ) dong lai. Ghi ra tep tam roi moi ssh - giong
# cach day.sh dang lam.
TEP_LENH="$(mktemp "${TMPDIR:-/tmp}/nhd_mamoi.XXXXXX")"
trap 'rm -f "$TEP_LENH"' EXIT

cat > "$TEP_LENH" <<VPSEOF
set -u
TEN="MA_MOI_GIAO_VIEN"

# 1. Bien moi truong systemd dat THANG trong unit (Environment=...)
GT="\$(systemctl show -p Environment --value $SERVICE 2>/dev/null \\
      | tr ' ' '\n' | sed -n "s/^\${TEN}=//p" | head -1)"

# 2. Chua thay thi lan theo cac tep EnvironmentFile ma systemd dang doc,
#    cong them .env cua du an.
if [ -z "\$GT" ]; then
  TEPS="\$(systemctl show -p EnvironmentFile --value $SERVICE 2>/dev/null \\
          | tr ' ' '\n' | sed 's/^-//' | sed 's/(ignore_errors=.*)//' \\
          | grep -v '^\$')"
  TEPS="\$TEPS
$VPS_DIR/.env"
  for f in \$TEPS; do
    [ -f "\$f" ] || continue
    D="\$(grep -m1 "^[[:space:]]*\${TEN}[[:space:]]*=" "\$f" 2>/dev/null)"
    if [ -n "\$D" ]; then
      GT="\${D#*=}"
      # bo khoang trang va dau nhay bao quanh
      GT="\$(printf '%s' "\$GT" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*\$//' \\
             -e 's/^"//' -e 's/"\$//' -e "s/^'//" -e "s/'\$//")"
      NOI="\$f"
      break
    fi
  done
else
  NOI="unit systemd ($SERVICE)"
fi

if [ -z "\$GT" ]; then
  echo "KHONG_THAY"
  echo "--- cac tep moi truong systemd dang doc ---"
  systemctl show -p EnvironmentFile --value $SERVICE 2>/dev/null
  echo "--- co tep $VPS_DIR/.env khong ---"
  ls -l "$VPS_DIR/.env" 2>/dev/null || echo "(khong co)"
else
  echo "THAY \$GT"
  echo "NOI \$NOI"
fi
VPSEOF

KQ="$(ssh "$VPS_USER@$DOMAIN" 'bash -s' < "$TEP_LENH")" || {
  do_ "Khong ket noi duoc toi $DOMAIN."; exit 1; }

case "$KQ" in
  THAY*)
    MA="$(printf '%s\n' "$KQ" | sed -n '1s/^THAY //p')"
    NOI="$(printf '%s\n' "$KQ" | sed -n '2s/^NOI //p')"
    echo
    dam "Ma moi dang ky tai khoan GIAO VIEN:"
    xanh "    $MA"
    echo
    echo "Luu tai: $NOI  (tren VPS)"
    vang "Chi dua ma nay cho giao vien minh tin. Ai co ma la tu nang"
    vang "minh len tai khoan giao vien duoc."
    echo
    echo "Doi ma: sua dong MA_MOI_GIAO_VIEN trong tep tren roi chay"
    echo "        systemctl restart $SERVICE"
    ;;
  *)
    do_ "Khong tim thay bien MA_MOI_GIAO_VIEN tren VPS."
    echo "$KQ" | sed '1d'
    echo
    vang "Chua dat bien nay thi trang /register/teacher se tu chan het,"
    vang "khong ai dang ky duoc giao vien (xem app/routers/auth.py)."
    ;;
esac
