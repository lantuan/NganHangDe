# 29 — CHUYỂN SANG VPS MỚI (khi VPS hết hạn / đổi nhà cung cấp)

Cập nhật: 12/10/2026 — Version 2.xx

Tài liệu này để cô Lan tự đọc và tự làm lại, không cần nhớ gì. Làm theo đúng thứ tự.

---

## 1. Cái gì nằm ở đâu

| Thứ | Nằm ở đâu | Mất khi VPS hết hạn? | Cách lấy lại |
|---|---|---|---|
| Mã nguồn, ngân hàng câu hỏi (`data/`), `docs/`, `scripts/`, cấu hình nginx mẫu | GitHub `lantuan/NganHangDe` (nhánh `main`, kho công khai) | Không | `git clone` (script tự làm) |
| `.env` (khóa Supabase, Google, n8n, mã mời giáo viên) | Chỉ trên VPS + Mac | **Có** | Bản sao lưu riêng (mục 2) |
| File dịch vụ `nganhangde.service`, cấu hình nginx thật | Chỉ trên VPS | **Có** | Bản sao lưu riêng; nếu mất dùng `deploy/nganhangde.service` |
| Tài khoản, lớp, lịch sử, đề đã lưu | Supabase (dịch vụ riêng) | Không | Chỉ cần dán lại khóa vào `.env` |
| Workflow n8n | `fqrpl.n8npanel.com` (dịch vụ riêng) | Không | Nên export JSON dự phòng (mục 4) |
| Tên miền `nganhangdechv.tech` | Nhà đăng ký tên miền | Không | Trỏ lại DNS về IP mới |
| Chứng chỉ HTTPS | VPS (Let's Encrypt) | Có, nhưng miễn phí | Script xin lại |
| Tệp sinh ra `output/`, `logs/` | VPS | Có | Không cần, sinh lại được |
| Tệp chỉ có trên VPS (chưa commit) | VPS | Có | Xem `chua_co_tren_github.txt` trong bản sao lưu |

---

## 2. Làm TRƯỚC khi VPS hết hạn: sao lưu riêng

**Bấm đúp `1_SAO_LUU_VPS.command`** (ở thư mục dự án trên Mac).

Nếu bấm đúp báo "không có quyền chạy": mở Terminal tại thư mục dự án, gõ một lần `chmod +x *.command scripts/*.sh`. (Hoặc chạy thẳng: `bash scripts/sao_luu_rieng.sh`.)

Nó kéo từ VPS cũ về Mac vào `~/NganHangDe_SaoLuu/<ngày_giờ>/` (và liên kết `moi_nhat`):
`env`, `nganhangde.service`, `nginx/`, `crontab.txt`, `ban_dang_chay.txt`, `chua_co_tren_github.txt`, `may_chu.txt`, và `env_tren_mac`.

Chạy khi: (a) sau mỗi lần sửa `.env` hoặc cấu hình trên VPS; (b) khoảng 1 tuần trước hạn VPS.

**Bản sao lưu có mật khẩu/khóa. KHÔNG đưa lên GitHub, không gửi qua chat/email.**
Chép cả thư mục `~/NganHangDe_SaoLuu` vào một nơi an toàn khác: trình quản lý mật khẩu, ổ USB, hoặc Google Drive riêng tư.

Mẫu tên biến cần có trong `.env` (không có giá trị): file `.env.example` trong repo.

---

## 3. Khi đã mua VPS mới: 5 bước

1. Mua VPS **Ubuntu 24.04**, cấu hình tương đương cũ (nên ≥ 2 vCPU, 4 GB RAM, ≥ 40 GB ổ đĩa — xelatex chiếm khoảng 2,5 GB). Ghi lại **địa chỉ IP** và **mật khẩu root** nhà cung cấp gửi.
2. Trên Mac, **bấm đúp `2_CHUYEN_VPS.command`**.
3. Nhập IP VPS mới. Nhập mật khẩu root **một lần** (gõ chữ không hiện lên màn hình là bình thường).
4. Đợi script chạy (khoảng 10–20 phút, lâu nhất là cài xelatex). Khi nó hiện hướng dẫn DNS, vào trang quản lý tên miền, sửa bản ghi **A** (`@` và `www`) trỏ về IP mới, rồi gõ `g` để script kiểm tra DNS và xin HTTPS.
   - DNS chưa kịp cập nhật? Gõ `k`. Khi DNS đã đổi, chạy lại chỉ bước này:
     `bash scripts/chuyen_vps.sh --https <IP>`
5. Khi thấy dòng xanh **"DA CHUYEN XONG"**: đăng nhập thử trên https://nganhangdechv.tech, tạo thử một đề.

Script an toàn khi chạy lại: bước nào làm rồi thì bỏ qua. Script không sửa VPS cũ và không xóa gì trên Mac.

---

## 4. Việc phải làm tay (không tự động được)

1. **Export workflow n8n** (làm 1 lần, lặp lại mỗi khi sửa workflow): vào https://fqrpl.n8npanel.com → từng workflow → menu `...` → **Download** → lưu file JSON vào thư mục `n8n/` trong repo rồi `day`. Hiện thư mục `n8n/` đang trống, tức là workflow chưa có bản sao nào. Nếu n8n chạy ở nhà cung cấp riêng (không phải VPS này) thì VPS hết hạn không ảnh hưởng, nhưng vẫn nên có bản dự phòng.
2. **Giữ nguyên tên miền**: nếu vẫn dùng `nganhangdechv.tech` thì **không phải sửa** gì ở Google Cloud Console (redirect URI) hay Supabase (Site URL). Nếu ĐỔI tên miền thì phải sửa cả hai chỗ, đổi biến `NHD_DOMAIN` khi chạy script, sửa `DOMAIN` trong `scripts/day.sh`, và đổi `deploy/nginx/*.conf`.
3. **Webhook n8n trong `.env`**: nếu địa chỉ n8n đổi thì sửa `N8N_WEBHOOK_*` trong `.env` rồi `systemctl restart nganhangde`.
4. **Sau khi chuyển xong**:
   - Chạy `day web` một lần để chắc công cụ cập nhật vẫn chạy.
   - Chạy lại `1_SAO_LUU_VPS.command` để có bản sao lưu của VPS mới.
   - Thay IP cũ `103.82.27.226` bằng IP mới trong `docs/14_DEPLOYMENT.md` (chỉ là ghi chú).
   - Hủy VPS cũ khi đã chắc chắn.
5. **Cảnh báo `REMOTE HOST IDENTIFICATION HAS CHANGED`** khi ssh vào tên miền: script đã tự xóa dấu vân tay cũ; nếu vẫn gặp, chạy `ssh-keygen -R nganhangdechv.tech`.

---

## 5. Nếu script báo lỗi: làm tay từng bước

Trên VPS mới (đăng nhập `ssh root@<IP>`):

```bash
apt-get update
apt-get install -y git curl python3 python3-venv python3-pip nginx certbot python3-certbot-nginx dnsutils
git clone https://github.com/lantuan/NganHangDe.git /root/NganHangDe
cd /root/NganHangDe
python3 -m venv venv && venv/bin/pip install -r requirements.txt
cp .env.example .env && nano .env            # dán khóa từ bản sao lưu: ~/NganHangDe_SaoLuu/moi_nhat/env
cp deploy/nganhangde.service /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now nganhangde
bash scripts/cai_xelatex_vps.sh              # hình vẽ + xuất Word
# nginx: dùng deploy/nginx/nganhangdechv.tech.conf làm mẫu (bỏ đoạn SSL trước), sau đó:
certbot --nginx -d nganhangdechv.tech -d www.nganhangdechv.tech
```

Xem lỗi dịch vụ: `journalctl -u nganhangde -n 60 --no-pager`.
Thiếu thư viện Python (khi dịch vụ chạy bằng Python hệ thống, không phải venv): xem mục "CÀI THƯ VIỆN PYTHON TRÊN VPS" trong `docs/14_DEPLOYMENT.md` và `scripts/thu_vien_thieu.py`.

---

## 6. Những điều script giả định (cần biết)

- Kho GitHub **công khai** nên VPS mới `git clone` được mà không cần khóa. Nếu sau này chuyển kho sang riêng tư, phải tạo deploy key / token cho VPS.
- Cổng web là **8000** (khớp `proxy_pass` trong nginx), chạy bằng `uvicorn app.main:app`.
- Nếu bản sao lưu có file `nganhangde.service` của VPS cũ và nó chạy bằng venv nằm trong `/root/NganHangDe/...` thì script dùng đúng file đó; ngược lại dùng mẫu `deploy/nganhangde.service`.
- Script chưa từng chạy trên VPS thật (chỉ được thử với lệnh giả). Lần đầu dùng nên chạy lúc không gấp và để VPS cũ còn sống song song vài ngày.

---

## 7. Danh sách kiểm tra sau khi chuyển

- [ ] https://nganhangdechv.tech mở được, có ổ khóa HTTPS
- [ ] Đăng nhập bằng email + bằng Google đều được
- [ ] Tạo thử một đề có hình vẽ (kiểm tra xelatex)
- [ ] Xuất Word / PDF được (pandoc)
- [ ] Chấm tự luận / Gia sư AI chạy được (kiểm tra webhook n8n)
- [ ] `day web` chạy thành công
- [ ] Đã có bản sao lưu mới của VPS mới
