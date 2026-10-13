#!/usr/bin/env bash
# =====================================================================
#  sao_luu_rieng.sh  --  Sao luu NHUNG THU KHONG CO TREN GITHUB
#
#  Chay tren MAC (double-click "1_SAO_LUU_VPS.command" cung duoc):
#     bash scripts/sao_luu_rieng.sh            # lay tu nganhangdechv.tech
#     bash scripts/sao_luu_rieng.sh 1.2.3.4    # lay tu mot IP cu the
#
#  Keo tu VPS ve MAC (KHONG dua len GitHub, vi co mat khau/khoa):
#     - .env                      (khoa Supabase, Google, n8n, ma moi GV)
#     - nganhangde.service        (cach VPS chay web)
#     - cau hinh nginx
#     - crontab, danh sach tep chua co tren GitHub, phien ban dang chay
#  va chep them .env tren Mac (neu co).
#
#  Noi luu:  ~/NganHangDe_SaoLuu/<ngay_gio>/   (+ lien ket "moi_nhat")
#  Doi noi luu bang bien moi truong NHD_SAOLUU (khong bat buoc).
#
#  Chay ngay sau MOI LAN sua .env hoac sua cau hinh tren VPS, va chay
#  them mot lan khoang 1 tuan truoc khi VPS het han.
# =====================================================================
set -u

DOMAIN="${NHD_DOMAIN:-nganhangdechv.tech}"
VPS_USER="root"
HOST="${1:-$DOMAIN}"
KHO="${NHD_SAOLUU:-$HOME/NganHangDe_SaoLuu}"
NGAY="$(date '+%Y-%m-%d_%H%M')"
DICH="$KHO/$NGAY"

xanh() { printf "\033[1;32m%s\033[0m\n" "$*"; }
vang() { printf "\033[1;33m%s\033[0m\n" "$*"; }
do_()  { printf "\033[1;31m%s\033[0m\n" "$*"; }
dam()  { printf "\033[1m%s\033[0m\n" "$*"; }

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$DICH" || { do_ "Khong tao duoc thu muc $DICH"; exit 1; }
chmod 700 "$KHO" "$DICH" 2>/dev/null

dam "Sao luu tu $VPS_USER@$HOST  ->  $DICH"

# ---------- Lenh chay tren VPS: gom tep vao thu muc tam roi nen thanh tar ----------
# Ghi ra TEP TAM roi moi ssh (khong dat heredoc trong $( ... ), vi bash 3.2
# cua macOS doc sai - xem ghi chu trong day.sh).
# Tar di ra STDOUT nen moi thong bao phai di ra STDERR (>&2).
TEP_LENH="$(mktemp "${TMPDIR:-/tmp}/nhd_sl_lenh.XXXXXX")"
cat > "$TEP_LENH" <<'VPSEOF'
set -u
D=/root/NganHangDe
T="$(mktemp -d /tmp/nhd_sl.XXXXXX)"

if [ -f "$D/.env" ]; then cp "$D/.env" "$T/env"; else echo "!! khong thay $D/.env" >&2; fi

systemctl cat nganhangde > "$T/nganhangde.service.day_du.txt" 2>/dev/null || true
F="$(systemctl show -p FragmentPath --value nganhangde 2>/dev/null)"
if [ -n "$F" ] && [ -f "$F" ]; then cp "$F" "$T/nganhangde.service"; else echo "!! khong thay file service nganhangde" >&2; fi

mkdir -p "$T/nginx"
for f in /etc/nginx/sites-available/*; do
  [ -f "$f" ] || continue
  [ "$(basename "$f")" = "default" ] && continue
  cp "$f" "$T/nginx/"
done

crontab -l > "$T/crontab.txt" 2>/dev/null || echo "(khong co crontab)" > "$T/crontab.txt"

if [ -d "$D/.git" ]; then
  ( cd "$D" && git log -1 --format='%H  %cd  %s' ) > "$T/ban_dang_chay.txt" 2>/dev/null
  # Cac tep CHI co tren VPS (chua commit / bi gitignore) - de biet con gi se mat
  ( cd "$D" && git status --short --ignored ) > "$T/chua_co_tren_github.txt" 2>/dev/null
fi

{
  echo "--- he dieu hanh ---"; (lsb_release -d 2>/dev/null || head -2 /etc/os-release)
  echo "--- python ---"; python3 --version 2>&1
  echo "--- dung luong cac thu muc lon ---"
  du -sh "$D" "$D/data" "$D/output" "$D/logs" 2>/dev/null
  echo "--- o dia ---"; df -h / | sed -n '1,2p'
} > "$T/may_chu.txt" 2>&1

tar czf - -C "$T" .
rm -rf "$T"
VPSEOF

TEP_TAR="$(mktemp "${TMPDIR:-/tmp}/nhd_sl_tar.XXXXXX")"
ssh -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new "$VPS_USER@$HOST" bash -s \
    < "$TEP_LENH" > "$TEP_TAR"
KQ=$?
rm -f "$TEP_LENH"

if [ $KQ -ne 0 ] || [ ! -s "$TEP_TAR" ]; then
  rm -f "$TEP_TAR"
  do_ "Khong ket noi / khong lay duoc du lieu tu $HOST (ma loi $KQ)."
  vang "Neu VPS cu da het han thi khong sao luu duoc nua - dung ban sao luu truoc do:"
  vang "   $KHO/moi_nhat"
  rmdir "$DICH" 2>/dev/null
  exit 1
fi

tar xzf "$TEP_TAR" -C "$DICH" || { do_ "Giai nen that bai."; rm -f "$TEP_TAR"; exit 1; }
rm -f "$TEP_TAR"

# ---------- Chep them nhung gi o tren MAC ----------
if [ -f "$GOC/.env" ]; then cp "$GOC/.env" "$DICH/env_tren_mac"; fi
printf '%s\n' "$HOST" > "$DICH/lay_tu_may.txt"

ln -sfn "$DICH" "$KHO/moi_nhat"

# ---------- Ghi chu doc lai ----------
cat > "$DICH/DOC_TOI_DAY.txt" <<'GHICHU'
BAN SAO LUU RIENG CUA NGAN HANG DE AI  (KHONG dua len GitHub!)

Trong thu muc nay:
  env                       .env tren VPS  (QUAN TRONG NHAT - co khoa bi mat)
  env_tren_mac              .env tren Mac (thuong chi co 2 dong Supabase)
  nganhangde.service        cach systemd chay web (cong 8000, venv...)
  nganhangde.service.day_du.txt   ban day du (ke ca drop-in)
  nginx/                    cau hinh nginx cua VPS (da gom doan SSL cua certbot;
                            khi chuyen VPS script se tu cap lai SSL moi)
  crontab.txt               cac lenh hen gio tren VPS
  ban_dang_chay.txt         commit dang chay tren VPS
  chua_co_tren_github.txt   tep chi co tren VPS (dau ?? = chua commit,
                            dau !! = bi gitignore). Xem co gi quan trong khong.
  may_chu.txt               he dieu hanh, dung luong

CACH DUNG KHI CHUYEN VPS:
  Double-click "2_CHUYEN_VPS.command" o thu muc du an, nhap IP VPS moi.
  Script tu doc ban sao luu "moi_nhat" nay.

CHUA SAO LUU DUOC (phai lam tay - xem docs/29_CHUYEN_VPS.md):
  - Workflow n8n (export JSON tu https://fqrpl.n8npanel.com)
  - Cau hinh Google Cloud Console / Supabase (dang luu o dich vu cua ho)

NHAC: thu muc nay co MAT KHAU/KHOA. Hay chep mot ban vao noi an toan
(trinh quan ly mat khau, o USB ma hoa, Google Drive rieng tu) - dung gui
len GitHub, dung gui qua chat/email.
GHICHU

chmod -R go-rwx "$DICH" 2>/dev/null

echo
xanh "Da sao luu xong:"
ls -1 "$DICH" | sed 's/^/   /'
echo
if [ ! -f "$DICH/env" ]; then
  do_ "CANH BAO: khong lay duoc .env tu VPS - ban sao luu NAY THIEU phan quan trong nhat."
fi
vang "Con 2 viec phai lam tay (khong tu dong duoc):"
vang "   1. Export workflow n8n ra JSON (xem docs/29_CHUYEN_VPS.md muc 4)."
vang "   2. Chep thu muc  $KHO  vao noi an toan khac (khong len GitHub)."
