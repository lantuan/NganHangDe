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



===============================================================================

# Cập nhật 2026-08-16 — Google Classroom OAuth (Version 2.20 → 2.22)

## Biến môi trường mới (.env trên VPS — KHÔNG qua git, sửa trực tiếp
bằng SSH, xem mục "Quy trình sửa code" ở trên chỉ áp dụng cho code)

- GOOGLE_CLASSROOM_CLIENT_ID
- GOOGLE_CLASSROOM_CLIENT_SECRET

OAuth Client RIÊNG cho tính năng đồng bộ/tham gia lớp Classroom, KHÁC
Client đang dùng cho nút "Đăng nhập bằng Google" qua Supabase (2 Client
độc lập trong cùng 1 project Google Cloud Console).

## Google Cloud Console — cấu hình bắt buộc

- Bật Google Classroom API.
- Scope: classroom.rosters, classroom.profile.emails,
  classroom.courses.readonly (đủ 3 scope — chi tiết lý do từng scope
  xem docs/16_CHANGELOG.md Version 2.20/2.21).
  >>> ĐÃ THAY ĐỔI: từ Version 2.44 cần 6 scope và phải bật thêm Google
  >>> Drive API. Xem mục "Cập nhật 2026-09-13" ở cuối file này.
- Authorized redirect URI: https://nganhangdechv.tech/gv/classroom/callback
- App đang ở chế độ Testing (chưa verify với Google) — CHỈ tài khoản
  được thêm làm Test user mới kết nối được; tài khoản khác bị Google
  chặn ngay ở màn hình đồng ý quyền.

## Giới hạn đã biết — không sửa được bằng cấu hình

Google KHÔNG cho phép thêm thẳng học sinh vào lớp qua API
(courses.students.create) trừ khi tài khoản gọi API là quản trị viên
domain Google Workspace for Education. Vì Classroom ở đây dùng tài
khoản Gmail cá nhân, tính năng chỉ dừng ở mức tạo link + mã lớp để học
sinh tự tham gia (xem docs/16_CHANGELOG.md Version 2.22).


===============================================================================

# Cập nhật 2026-09-13 — Classroom: scope + Drive API (Version 2.43 → 2.44)

Mục 2026-08-16 ở trên viết "đủ 3 scope" — điều đó CHỈ đúng khi tính năng
mới dừng ở đồng bộ danh sách lớp. Từ Version 2.43 hệ thống còn phải ĐĂNG
đề + đáp án + điểm lên Classroom, nên cấu hình bắt buộc thay đổi như sau.

## 6 scope hiện tại (app/services/classroom_service.py, hằng SCOPES)

| Scope | Dùng để làm gì |
|---|---|
| classroom.rosters | đọc danh sách học sinh trong lớp |
| classroom.profile.emails | lấy email học sinh để khớp với profiles |
| classroom.courses.readonly | liệt kê lớp của giáo viên |
| classroom.coursework.students | courses.courseWork — bài tập CÓ hạn nộp |
| classroom.courseworkmaterials | courses.courseWorkMaterials — TÀI LIỆU |
| drive.file | tải PDF lên Drive của giáo viên (chỉ file app tự tạo) |

Hai scope coursework Google tách RIÊNG, không bao nhau. Hàm
`_tao_coursework_material()` gọi `.../courses/{id}/courseWorkMaterials`
nên bắt buộc phải có `classroom.courseworkmaterials`. Thiếu nó Google
trả về 403 `"Request had insufficient authentication scopes"`
(reason: `ACCESS_TOKEN_SCOPE_INSUFFICIENT`) — lỗi thật gặp ngày 13/09.

## Google Cloud Console — phải bật CẢ HAI API

- Google Classroom API
- **Google Drive API** — dễ quên. Thiếu nó, VPS log ra 403
  `"Google Drive API has not been used in project 299388243103 before
  or it is disabled"`. Bật ở Console > APIs & Services > Library, chờ
  khoảng 1–2 phút cho lan truyền rồi thử lại.

Project Google Cloud đang dùng: **299388243103**.

## Quy trình BẮT BUỘC mỗi khi đổi scope

Đổi scope trong code là CHƯA đủ. refresh_token cũ chỉ mang quyền cũ, có
pull code mới vẫn 403 y như trước. Phải làm đủ 3 bước, đúng thứ tự:

1. Deploy code mới lên VPS (git pull + `systemctl restart nganhangde`).
2. Console > APIs & Services > **Data Access** (OAuth consent screen) >
   Add or remove scopes > thêm scope mới > Update > Save.
3. Vào lại `https://nganhangdechv.tech/gv/classroom/connect`, bấm đồng ý
   quyền lại từ đầu để Google cấp refresh_token MỚI. Bảng `profiles`
   ghi đè token cũ.

Bỏ bước 3 là nguyên nhân phổ biến nhất của "đã sửa rồi mà vẫn 403".

## Cách đọc lỗi khi đăng không lên

Từ Version 2.43 trang làm bài có ô `#trang-thai-classroom` hiện lý do
ngay trên web thay vì im lặng. Log chi tiết vẫn ở VPS:

    journalctl -u nganhangde -f | grep -i classroom

Ba lỗi đã gặp và cách phân biệt:

- `403 ... has not been used in project` → chưa bật Drive API (bước Console).
- `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT` → thiếu scope, hoặc còn dùng
  refresh_token cũ (làm lại bước 2 + 3).
- Không thấy dòng log nào → request chưa tới router, xem lại phía
  frontend/`/api/chat/dang-classroom`.
