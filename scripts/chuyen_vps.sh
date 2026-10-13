#!/usr/bin/env bash
# =====================================================================
#  chuyen_vps.sh  --  Dung lai TOAN BO web tren mot VPS MOI
#
#  Chay tren MAC (double-click "2_CHUYEN_VPS.command" cung duoc):
#     bash scripts/chuyen_vps.sh              # hoi IP VPS moi
#     bash scripts/chuyen_vps.sh 1.2.3.4      # IP da biet
#     bash scripts/chuyen_vps.sh --https 1.2.3.4
#                                             # chi lam buoc DNS + HTTPS
#                                             # (dung khi lan truoc chua tro DNS kip)
#
#  Can truoc:
#   - VPS moi: Ubuntu 24.04, co IP + mat khau root (nha cung cap gui).
#   - Ban sao luu rieng:  bash scripts/sao_luu_rieng.sh  (chay khi VPS cu
#     con song). Script se tu hoi neu chua co.
#
#  Script lam (tren VPS moi), theo thu tu:
#   0. dang nhap bang khoa ssh (hoi mat khau root DUNG MOT LAN)
#   1. cai git, python, nginx, certbot
#   2. keo ma nguon tu GitHub ve /root/NganHangDe
#   3. khoi phuc .env tu ban sao luu rieng
#   4. tao venv, cai thu vien, tao dich vu systemd "nganhangde"
#   5. cau hinh nginx (HTTP)
#   6. cai xelatex + pandoc (hinh ve, xuat Word) - mat vai phut
#   7. DOI Lan tro DNS, roi xin chung chi HTTPS (Let's Encrypt)
#
#  An toan khi chay lai: moi buoc deu kiem tra "da co chua".
#  Script KHONG sua VPS cu, KHONG xoa gi tren Mac.
# =====================================================================
set -u

DOMAIN="${NHD_DOMAIN:-nganhangdechv.tech}"
VPS_USER="root"
VPS_DIR="/root/NganHangDe"
SERVICE="nganhangde"
PORT="8000"
REPO_URL="https://github.com/lantuan/NganHangDe.git"
KHO="${NHD_SAOLUU:-$HOME/NganHangDe_SaoLuu}"
SL="$KHO/moi_nhat"
SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"

xanh() { printf "\033[1;32m%s\033[0m\n" "$*"; }
vang() { printf "\033[1;33m%s\033[0m\n" "$*"; }
do_()  { printf "\033[1;31m%s\033[0m\n" "$*"; }
dam()  { printf "\033[1m%s\033[0m\n" "$*"; }

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

CHI_HTTPS=0
if [ "${1:-}" = "--https" ]; then CHI_HTTPS=1; shift; fi
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  sed -n '2,32p' "$0"; exit 0
fi

# ---------- IP ----------
IP="${1:-}"
if [ -z "$IP" ]; then
  read -r -p "Dia chi IP cua VPS MOI: " IP
fi
case "$IP" in
  ""|*[!0-9A-Fa-f.:]*) do_ "IP khong hop le: '$IP'"; exit 1 ;;
esac

dam "============================================================"
dam " CHUYEN NGAN HANG DE AI SANG VPS MOI:  $IP"
dam " Ten mien: $DOMAIN"
dam "============================================================"

# ---------- 0. Ban sao luu rieng ----------
if [ "$CHI_HTTPS" = 0 ]; then
  if [ ! -d "$SL" ]; then
    vang "Chua co ban sao luu rieng ($SL)."
    if ssh -o BatchMode=yes -o ConnectTimeout=8 "$VPS_USER@$DOMAIN" true 2>/dev/null; then
      read -r -p "VPS cu van vao duoc. Sao luu tu VPS cu ngay bay gio? (g/k) " tl
      if [ "$tl" = "g" ]; then
        bash "$GOC/scripts/sao_luu_rieng.sh" || { do_ "Sao luu that bai."; exit 1; }
      fi
    fi
  fi
  if [ -d "$SL" ]; then
    echo "Dung ban sao luu:  $(readlink "$SL" 2>/dev/null || echo "$SL")"
    [ -f "$SL/env" ] || vang "   CANH BAO: ban nay KHONG co .env cua VPS."
    [ -f "$SL/nganhangde.service" ] || vang "   (khong co file service - se dung mau trong deploy/)"
    read -r -p "Dung ban sao luu nay? (g/k) " tl
    [ "$tl" = "g" ] || { echo "Da dung."; exit 0; }
  else
    vang "Khong co ban sao luu. Se dung .env mau - sau do PHAI tu dien khoa vao .env tren VPS."
    read -r -p "Van tiep tuc? (g/k) " tl
    [ "$tl" = "g" ] || { echo "Da dung."; exit 0; }
  fi
fi

# ---------- 1. Dang nhap bang khoa ssh ----------
echo
dam "[0] Ket noi toi VPS moi..."
ssh-keygen -R "$IP" >/dev/null 2>&1
if ! ssh $SSH_OPTS -o BatchMode=yes "$VPS_USER@$IP" true 2>/dev/null; then
  if [ ! -f "$HOME/.ssh/id_ed25519.pub" ] && [ ! -f "$HOME/.ssh/id_rsa.pub" ]; then
    echo "Chua co khoa ssh tren Mac - tao khoa moi (khong dat mat khau)."
    mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"
    ssh-keygen -t ed25519 -N "" -f "$HOME/.ssh/id_ed25519" -q
  fi
  vang "Nhap mat khau root cua VPS MOI mot lan (go chu se KHONG hien len man hinh):"
  ssh-copy-id $SSH_OPTS "$VPS_USER@$IP" || { do_ "Khong dang nhap duoc. Kiem tra IP / mat khau."; exit 1; }
  ssh $SSH_OPTS -o BatchMode=yes "$VPS_USER@$IP" true \
    || { do_ "Van chua dang nhap bang khoa duoc."; exit 1; }
fi
xanh "   Da ket noi."

# ---------- Email cho Let's Encrypt ----------
EMAIL=""
[ -f "$KHO/email_certbot.txt" ] && EMAIL="$(head -1 "$KHO/email_certbot.txt")"
if [ -z "$EMAIL" ]; then
  read -r -p "Email nhan thong bao het han chung chi HTTPS (Let's Encrypt): " EMAIL
  mkdir -p "$KHO" && printf '%s\n' "$EMAIL" > "$KHO/email_certbot.txt"
fi

# ---------- Ham chay mot doan lenh tren VPS (qua tep tam - bash 3.2 an toan) ----------
chay_tren_vps() {   # $1 = tep chua than lenh
  local tep
  tep="$(mktemp "${TMPDIR:-/tmp}/nhd_cv.XXXXXX")"
  {
    printf 'DOMAIN=%s\nDIR=%s\nSVC=%s\nPORT=%s\nREPO=%s\nEMAIL=%s\n' \
      "$DOMAIN" "$VPS_DIR" "$SERVICE" "$PORT" "$REPO_URL" "$EMAIL"
    cat "$1"
  } > "$tep"
  ssh $SSH_OPTS "$VPS_USER@$IP" bash -s < "$tep"
  local kq=$?
  rm -f "$tep"
  return $kq
}

# =====================================================================
#  PHAN A: dung may chu
# =====================================================================
if [ "$CHI_HTTPS" = 0 ]; then
  echo
  dam "[1] Chep ban sao luu rieng len VPS moi..."
  ssh $SSH_OPTS "$VPS_USER@$IP" "mkdir -p /root/nhd_chuyen && chmod 700 /root/nhd_chuyen" || exit 1
  for f in env nganhangde.service; do
    if [ -f "$SL/$f" ]; then
      scp -q $SSH_OPTS "$SL/$f" "$VPS_USER@$IP:/root/nhd_chuyen/$f" && echo "   da chep: $f"
    fi
  done

  TEP_A="$(mktemp "${TMPDIR:-/tmp}/nhd_cv_a.XXXXXX")"
  cat > "$TEP_A" <<'VPSEOF'
set -e
export DEBIAN_FRONTEND=noninteractive

echo; echo "[2] Cai phan mem he thong (git, python, nginx, certbot)..."
apt-get update -qq
apt-get install -y -qq git curl python3 python3-venv python3-pip nginx certbot python3-certbot-nginx dnsutils >/dev/null
echo "   xong."

echo; echo "[3] Lay ma nguon tu GitHub..."
if [ -d "$DIR/.git" ]; then
  git -C "$DIR" pull --ff-only
else
  git clone -q "$REPO" "$DIR"
fi
echo "   ban: $(git -C "$DIR" log -1 --format='%h %s')"

echo; echo "[4] Khoi phuc .env..."
if [ -f /root/nhd_chuyen/env ]; then
  cp /root/nhd_chuyen/env "$DIR/.env"
  echo "   da khoi phuc .env tu ban sao luu."
elif [ -f "$DIR/.env" ]; then
  echo "   giu .env dang co."
else
  [ -f "$DIR/.env.example" ] && cp "$DIR/.env.example" "$DIR/.env"
  echo "   !! KHONG co ban sao luu .env - da tao .env mau."
  echo "   !! PHAI dien khoa that:  nano $DIR/.env   roi:  systemctl restart $SVC"
fi
chmod 600 "$DIR/.env" 2>/dev/null || true

echo; echo "[5] Python + dich vu systemd..."
SVCFILE=/root/nhd_chuyen/nganhangde.service
VENV=""
USE=mau
if [ -f "$SVCFILE" ]; then
  EX="$(grep -m1 '^ExecStart=' "$SVCFILE" | sed -E 's/^ExecStart=[-@+!:]*//' | awk '{print $1}')"
  case "$EX" in
    "$DIR"/*/bin/*) VENV="${EX%/bin/*}"; USE=sao_luu ;;
  esac
fi
if [ -z "$VENV" ]; then VENV="$DIR/venv"; fi
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$DIR/requirements.txt"
echo "   venv: $VENV  (thu vien da cai)"

if [ "$USE" = sao_luu ]; then
  cp "$SVCFILE" "/etc/systemd/system/$SVC.service"
  echo "   dich vu: dung file service cua VPS cu."
else
  cp "$DIR/deploy/nganhangde.service" "/etc/systemd/system/$SVC.service"
  echo "   dich vu: dung MAU deploy/nganhangde.service (VPS cu khong co ban sao luu service dung duong dan)."
fi
systemctl daemon-reload
systemctl enable "$SVC" >/dev/null 2>&1
systemctl restart "$SVC"

echo "   cho web khoi dong (nap ngan hang cau hoi mat vai chuc giay)..."
OK=0
for i in $(seq 1 24); do
  MA="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:$PORT/" || true)"
  case "$MA" in 200|302|303|307) OK=1; break ;; esac
  sleep 5
done
if [ "$OK" = 1 ]; then echo "   web chay duoc tren cong $PORT (ma $MA)."
else
  echo "   !! web CHUA tra loi. Xem:  journalctl -u $SVC -n 60 --no-pager"
fi

echo; echo "[6] Nginx (HTTP truoc, HTTPS sau khi tro DNS)..."
rm -f /etc/nginx/sites-enabled/default
if [ -d "/etc/letsencrypt/live/$DOMAIN" ] && [ -f "/etc/nginx/sites-available/$DOMAIN" ]; then
  echo "   da co chung chi + cau hinh, giu nguyen."
else
  cat > "/etc/nginx/sites-available/$DOMAIN" <<'NGX'
server {
    listen 80;
    listen [::]:80;
    server_name __DOMAIN__ www.__DOMAIN__;
    location / {
        proxy_pass http://127.0.0.1:__PORT__;
        proxy_connect_timeout 320s;
        proxy_send_timeout 320s;
        proxy_read_timeout 320s;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGX
  sed -i "s/__DOMAIN__/$DOMAIN/g; s/__PORT__/$PORT/g" "/etc/nginx/sites-available/$DOMAIN"
  ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
fi
nginx -t
systemctl reload nginx
echo "   nginx san sang."

echo; echo "[7] Cai xelatex + pandoc (hinh ve, xuat Word) - khoang 2,5 GB, mat vai phut..."
if command -v xelatex >/dev/null 2>&1 && command -v pandoc >/dev/null 2>&1; then
  echo "   da co, bo qua."
else
  printf 'g\n' | bash "$DIR/scripts/cai_xelatex_vps.sh" 2>&1 | tail -n 12
fi

echo; echo "[8] Kiem tra thu vien + hinh ve..."
"$VENV/bin/python" "$DIR/scripts/thu_vien_thieu.py" 2>&1 | tail -n 8 || true
bash "$DIR/scripts/kiem_tra_hinh.sh" 2>&1 | tail -n 6 || true
rm -rf /root/nhd_chuyen
VPSEOF
  chay_tren_vps "$TEP_A"
  KQ=$?
  rm -f "$TEP_A"
  if [ $KQ -ne 0 ]; then
    do_ "Co buoc that bai tren VPS moi (ma $KQ). Xem thong bao o tren."
    vang "Co the chay lai script - cac buoc da lam se duoc bo qua."
    exit 1
  fi
  xanh "Phan may chu da dung xong."
fi

# =====================================================================
#  PHAN B: DNS + HTTPS
# =====================================================================
echo
dam "[9] Tro ten mien $DOMAIN ve VPS moi"
cat <<HD
   Vao trang quan ly ten mien (noi ban mua $DOMAIN), sua ban ghi DNS:
       Loai A   Ten @     ->  $IP
       Loai A   Ten www   ->  $IP     (neu co)
   Sua xong, DNS mat tu vai phut den vai gio de cap nhat.
HD

ip_dns() {
  if command -v dig >/dev/null 2>&1; then
    dig +short A "$DOMAIN" @8.8.8.8 2>/dev/null | tail -1
  else
    nslookup "$DOMAIN" 8.8.8.8 2>/dev/null | awk '/^Address: /{a=$2} END{print a}'
  fi
}

DNS_OK=0
while true; do
  read -r -p "Da sua DNS xong chua? (g = kiem tra ngay, k = de sau): " tl
  [ "$tl" = "g" ] || break
  HIEN="$(ip_dns)"
  if [ "$HIEN" = "$IP" ]; then DNS_OK=1; break; fi
  vang "   DNS dang tro ve: '${HIEN:-chua co}'  (can: $IP). Co the can doi them chut."
done

if [ "$DNS_OK" = 0 ]; then
  echo
  vang "Chua xin HTTPS. Web da chay bang HTTP tren VPS moi."
  vang "Khi DNS da tro xong, chay lai CHI buoc nay:"
  vang "     bash scripts/chuyen_vps.sh --https $IP"
  exit 0
fi

TEP_B="$(mktemp "${TMPDIR:-/tmp}/nhd_cv_b.XXXXXX")"
cat > "$TEP_B" <<'VPSEOF'
set -e
if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
  echo "   da co chung chi HTTPS cho $DOMAIN."
else
  certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos \
          -m "$EMAIL" --redirect \
  || certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos \
          -m "$EMAIL" --redirect
fi
nginx -t && systemctl reload nginx
systemctl is-active "$SVC"
VPSEOF
chay_tren_vps "$TEP_B"
KQ=$?
rm -f "$TEP_B"
if [ $KQ -ne 0 ]; then
  do_ "Xin chung chi HTTPS that bai (thuong do DNS chua tro kip hoac www chua co ban ghi)."
  vang "Cho them roi chay lai:  bash scripts/chuyen_vps.sh --https $IP"
  exit 1
fi

# ---------- Don dau van tay ssh cu cua ten mien (tranh canh bao khi chay "day web") ----------
ssh-keygen -R "$DOMAIN" >/dev/null 2>&1

# ---------- Kiem tra cuoi ----------
echo
dam "[10] Kiem tra web tu Mac..."
MA=000
for lan in 1 2 3 4 5 6; do
  MA="$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAIN" || echo 000)"
  case "$MA" in 200|302|307) break ;; esac
  [ "$lan" = 6 ] || { echo "   lan $lan: $MA - cho 5 giay roi thu lai..."; sleep 5; }
done
if [ "$MA" = "200" ] || [ "$MA" = "302" ] || [ "$MA" = "307" ]; then
  xanh "Web tra ve $MA tai https://$DOMAIN -- DA CHUYEN XONG."
else
  do_ "Web tra ve $MA. Xem nhat ki:  ssh $VPS_USER@$IP  roi  journalctl -u $SERVICE -n 60"
  exit 1
fi

echo
dam "Con lai (lam tay, chi vai phut - xem docs/29_CHUYEN_VPS.md muc 4):"
echo "   - Dang nhap thu 1 tai khoan that tren https://$DOMAIN (dang nhap, tao de thu)."
echo "   - Thay IP cu bang $IP trong docs/14_DEPLOYMENT.md (chi la ghi chu)."
echo "   - Chay  day web  mot lan de chac cong cu cap nhat van chay."
echo "   - Chay lai  1_SAO_LUU_VPS.command  de co ban sao luu cua VPS MOI."
echo "   - Co the huy VPS cu."
