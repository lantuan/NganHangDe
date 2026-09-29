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
# MOT ket noi ssh duy nhat lam HET moi viec tren VPS: keo ma nguon, khoi
# dong lai dich vu, roi kiem tra do nghe. Truoc day buoc kiem tra hinh mo
# them mot ket noi ssh thu hai - lan do bi hoi mat khau roi dut (29/09),
# trong khi ket noi thu nhat van vao bang khoa binh thuong. Gop lai mot
# moi vua nhanh vua khong dinh chuyen xac thuc lan hai.
echo
dam "Dang cap nhat may chu $DOMAIN ..."
# KHONG dat heredoc ben trong $( ... ): bash 3.2 (ban di kem macOS) doc
# ca THAN heredoc de tim dau ) dong lai, nen mot dau ) le trong than -
# vi du nhan cua case "*/uvicorn)" - lam no tuong da het lenh thay the.
# Do dung la loi "syntax error near unexpected token '('" o dong 123 hom
# 29/09. Bash 5 (Linux) doc dung nen may chu khong he bao gi.
# Nay ghi lenh ra TEP TAM roi moi ssh - cach nay chay dung tren moi ban.
TEP_LENH_VPS="$(mktemp "${TMPDIR:-/tmp}/nhd_lenh_vps.XXXXXX")"
TEP_KQ_VPS="$(mktemp "${TMPDIR:-/tmp}/nhd_kq_vps.XXXXXX")"
cat > "$TEP_LENH_VPS" <<VPSEOF
set -e
cd "$VPS_DIR"
git pull --ff-only
systemctl restart $SERVICE
sleep 3
echo "--- trang thai dich vu ---"
systemctl is-active $SERVICE
echo "--- thu vien Python can thiet ---"
# Phai kiem bang DUNG con python ma dich vu dang chay, khong phai python3
# he thong: neu dich vu chay trong venv thi hai con nay khac nhau han.
PY="\$(systemctl show -p ExecStart --value $SERVICE 2>/dev/null \
       | tr ' ' '\n' | grep -m1 -E '(python[0-9.]*|uvicorn)\$' || true)"
# systemctl in ExecStart ra dang "path=/duong/dan/uvicorn" chu KHONG phai
# duong dan tran. Khong cat chu "path=" di thi test -x luon that bai,
# roi ve python3 he thong, roi bao "THIEU HAN 33 goi" - trong khi dich vu
# van chay ngon lanh bang python trong venv. Co Lan suyt chay lenh pip do
# len python he thong ngay 29/09/2026; lam vay la hong ca cong cu Ubuntu.
PY="\${PY##*=}"
case "\$PY" in
  */uvicorn) PY="\$(dirname "\$PY")/python" ;;
esac
[ -x "\$PY" ] || PY=python3
echo "python cua dich vu: \$PY"
# KHONG goi y chay ca requirements.txt nua (29/09/2026): tren VPS lenh
# do dut giua chung vi Ubuntu cai san urllib3 bang APT, pip khong go
# duoc goi apt (khong co tep RECORD) - cac goi dang sau khong duoc cai.
# scripts/thu_vien_thieu.py chi bao nhung goi THIEU HAN va in san lenh
# cai dung nhung goi ay.
if [ -f "$VPS_DIR/scripts/thu_vien_thieu.py" ]; then
  "\$PY" "$VPS_DIR/scripts/thu_vien_thieu.py" || true
else
  # Ban ma nguon cu chua co tep soat -> kiem tam nhu truoc
  if "\$PY" -c "import num2words" 2>/dev/null; then
    echo "num2words: co"
  else
    echo "num2words: THIEU - keo ma nguon moi roi chay lai de biet lenh cai"
  fi
fi
echo "--- do nghe ve hinh ---"
bash scripts/kiem_tra_hinh.sh 2>&1 || true
VPSEOF

ssh -o ConnectTimeout=15 "$VPS_USER@$DOMAIN" bash -s \
    < "$TEP_LENH_VPS" > "$TEP_KQ_VPS" 2>&1
KQ=$?
KQ_VPS="$(cat "$TEP_KQ_VPS")"
rm -f "$TEP_LENH_VPS" "$TEP_KQ_VPS"
echo "$KQ_VPS"

if [ $KQ -ne 0 ]; then
  do_ "Cap nhat VPS that bai. Ma nguon TREN GITHUB da moi, nhung web van dang chay ban cu."
  vang "Vao xem truc tiep:  ssh $VPS_USER@$DOMAIN  roi  journalctl -u $SERVICE -n 50"
  exit 1
fi

# ---------- 6b. Doc ket qua kiem tra tren VPS ----------
echo
CAN_SUA=0
if echo "$KQ_VPS" | grep -q "num2words: THIEU"; then
  do_ "THIEU thu vien num2words -- chuong 9 (xac suat) se KHONG nap duoc."
  vang "   Vao VPS:  ssh $VPS_USER@$DOMAIN"
  echo "$KQ_VPS" | grep "^lenh cai:" | sed 's/^lenh cai:/   Roi chay:/'
  CAN_SUA=1
fi
if echo "$KQ_VPS" | grep -q "Du do nghe"; then
  xanh "Hinh ve: du do nghe, hoc sinh xem duoc hinh tren web."
else
  vang "Hinh ve: VPS CHUA du do nghe -- cau co hinh se khong hien tren web."
  vang "   Sua:  ssh $VPS_USER@$DOMAIN  roi chay:"
  vang "         bash $VPS_DIR/scripts/cai_xelatex_vps.sh"
  CAN_SUA=1
fi

# ---------- 7. Kiem tra web con song ----------
echo
echo "Dang kiem tra web..."
MA="$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAIN" || echo 000)"
if [ "$MA" = "200" ] || [ "$MA" = "302" ] || [ "$MA" = "307" ]; then
  xanh "Web tra ve $MA -- dang chay binh thuong."
  if [ "$CAN_SUA" = 1 ]; then
    vang "XONG phan day code, NHUNG con viec phai lam tren VPS (xem o tren)."
  else
    xanh "XONG: GitHub da moi, VPS da cap nhat, web da kiem tra."
  fi
else
  do_ "Web tra ve $MA -- co the dang loi."
  vang "Xem nhat ki:  ssh $VPS_USER@$DOMAIN  roi  journalctl -u $SERVICE -n 50"
  exit 1
fi
