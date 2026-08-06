# DEPLOYMENT

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Triển khai toàn bộ hệ thống Ngân Hàng Đề AI lên VPS.

---

# Kiến trúc triển khai

Internet → Nginx → FastAPI → n8n → Python Generator → LaTeX Engine
→ Supabase

---

# Thành phần

## VPS

Chạy FastAPI, n8n, Python, LaTeX.

## FastAPI

Cung cấp API. Giao tiếp Frontend. Giao tiếp n8n.

## n8n

Chạy toàn bộ Workflow:
WF000_Gateway, WF001_GenerateExam, WF002_GenerateExamByAbility,
WF003_StudentAnalysis, WF004_DownloadFile, WF005_Help,
WF006_Reject, WF007_GradeExam.

## Python Generator

Sinh Question Object.

## LaTeX Engine

Sinh .tex, .pdf.

## Supabase

Lưu User, Class, Learning History, Exam History, Metadata.

---

# Thư mục dự án

/root/NganHangDe

---

# Dữ liệu / Kết quả sinh / Log

data/ , output/ , logs/

---

# Khởi động hệ thống

Nginx → FastAPI → n8n → Python

---

# Luồng hoạt động

User → Frontend → FastAPI → WF000_Gateway → Workflow → Python
→ LaTeX → Response

---

# Backup

Source Code, Database, data/, output/

---

# Không triển khai

- Python riêng lẻ.
- n8n riêng lẻ.
- Frontend gọi trực tiếp n8n hoặc Python.

---

# Quy tắc

- Mọi yêu cầu đi qua FastAPI.
- Mọi Workflow chạy trong n8n.
- Python chỉ sinh Question Object.
- LaTeX chỉ sinh PDF.
- Database chỉ lưu dữ liệu.
- Source Code quản lý bằng GitHub.


===============================================================================

# Thông tin vận hành thực tế (cập nhật 2026-08-06)

## Truy cập

- VPS: 103.82.27.226 (Ubuntu 24.04), SSH bằng `ssh root@103.82.27.226`.
- Thư mục dự án trên VPS: /root/NganHangDe
- Service systemd: `nganhangde`
  Lệnh thường dùng:
  - `sudo systemctl restart nganhangde`
  - `sudo systemctl status nganhangde --no-pager`
  - `sudo journalctl -u nganhangde -n 60 --no-pager` (xem log lỗi)
- GitHub repo: https://github.com/lantuan/NganHangDe (nhánh `main`)
- n8n: https://fqrpl.n8npanel.com (chứa Webhook + Switch + các node xử lý)
- Web công khai: https://nganhangdechv.tech (HTTPS qua Let's Encrypt/Certbot)
- Supabase project: https://supabase.com/dashboard/project/myrpporibfjiaculsjbm
  (SQL Editor dùng để chạy migration/sửa bảng thủ công khi cần)

## Quy trình sửa code (BẮT BUỘC — không sửa trực tiếp trên VPS)

1. Sửa code trên Mac (VS Code / Terminal), trong thư mục repo local.
2. Kiểm tra cú pháp: `python3 -c "import py_compile; py_compile.compile('duong_dan_file.py', doraise=True)"`
3. `git add ...` → `git commit -m "..."` → `git push`
4. SSH vào VPS (`ssh root@103.82.27.226`), vào thư mục dự án
   (`cd ~/NganHangDe` hoặc `cd /root/NganHangDe`), chạy `git pull`.
5. `sudo systemctl restart nganhangde`
6. Nếu có lỗi, xem `sudo journalctl -u nganhangde -n 60 --no-pager`.

## Ngoại lệ — cấu hình Nginx

Nginx được sửa TRỰC TIẾP trên VPS (không qua git), vì đây là cấu hình hạ
tầng, không phải code ứng dụng. File cấu hình:
- /etc/nginx/sites-available/nganhangdechv.tech
- /etc/nginx/sites-available/fqrpl.n8npanel.com

Sau khi sửa trực tiếp trên VPS, PHẢI sao lưu lại bản sao vào git (không
sửa ngược từ git ra VPS, chỉ sao lưu 1 chiều VPS → git để có bản lưu):
xem deploy/nginx/*.conf trong repo, cập nhật thủ công (copy nội dung
file thật trên VPS vào file .conf tương ứng trong deploy/nginx/) mỗi
khi có thay đổi cấu hình nginx.

## Test API thủ công

Swagger UI: https://nganhangdechv.tech/docs — dùng để test trực tiếp
từng endpoint (vd /api/exam/generate-pdf-auto, /api/exam/export-loigiai,
/api/exam/grade, /api/exam/debug-parse-answer) mà không cần qua n8n/chat.

## n8n — cấu trúc thực tế (khác với sơ đồ WF000-WF007 mục tiêu ở trên)

Xem chi tiết ở docs/06_N8N_WORKFLOW.md, mục "Trạng thái triển khai thực
tế". Tóm tắt: hiện chỉ có 1 Workflow gộp (không tách WF001-WF007 riêng),
Switch có 2 nhánh hoạt động (generate_exam, download_file), phần Business
Logic (Blueprint, Question Selector, Generator, Assembler) nằm trong
FastAPI (app/services/), n8n chỉ gọi 1 API duy nhất cho mỗi nhánh.
