# API SPECIFICATION

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Toàn bộ Frontend, n8n và Python chỉ giao tiếp qua FastAPI.
Không Node nào được đọc file trực tiếp nếu đã có API.

---

# Kiến trúc

Frontend → FastAPI → Data → n8n → Python

---

# Response chuẩn (bắt buộc cho MỌI API)

{
    "success": true,
    "message": "",
    "data": {}
}

Nếu lỗi:

{
    "success": false,
    "message": "Error message",
    "data": null
}

---

# PPCT

GET /api/data/ppct/{subject}
Ví dụ: /api/data/ppct/toan10
Output: PPCT JSON (bọc trong Response chuẩn)

---

# Curriculum

GET /api/data/curriculum/{subject}/{chapter}
Ví dụ: /api/data/curriculum/toan10/L10_C1

---

# Mapping

GET /api/data/mapping/{subject}/{chapter}
Ví dụ: /api/data/mapping/toan10/L10_C1

---

## Exam Scope

GET
/api/data/exam-scope/{lop}/{ki_thi}

Query param (bắt buộc khi `ki_thi = thuong_xuyen`)
pham_vi_chuong

Ví dụ
/api/data/exam-scope/10/thuong_xuyen?pham_vi_chuong=chuong_1
/api/data/exam-scope/10/cuoi_ky_1

`ki_thi` hợp lệ
thuong_xuyen
giua_ky_1
cuoi_ky_1
giua_ky_2
cuoi_ky_2

Output

HeSo1 (thuong_xuyen)

```json
{
    "loai_he_so": "HeSo1",
    "chuong_so": 1,
    "pham_vi_bai": ["L10_C1_B1", "L10_C1_B2"]
}
```

HeSo2_HeSo3 (giữa kỳ / cuối kỳ)

```json
{
    "loai_he_so": "HeSo2_HeSo3",
    "ki_thi": "cuoi_ky_1",
    "pham_vi_chuong": [1, 2, 3, 4, 5],
    "pham_vi_bai": ["..."],
    "phan_bo_ty_le": {
        "truoc_giua_ky": {"ti_le": 0.3, "pham_vi_bai": ["..."]},
        "sau_giua_ky": {"ti_le": 0.7, "pham_vi_bai": ["..."]}
    }
}
```

Giữa kỳ không có `phan_bo_ty_le` (trả về `null`).

---

# Python Bank

GET /api/data/python_bank/{subject}/{chapter}
Output: Generator Information (không trả source code)

---

# Generate Exam

POST /api/exam/generate
Input: Blueprint
Output: Exam Object

---

# Generate PDF / LaTeX / Web Test

POST /api/exam/pdf
POST /api/exam/latex
POST /api/exam/web
Input: Exam Object

---

# Grade Exam (mới)

POST /api/exam/grade

Input:

{
  "exam_id": "",
  "answers": [
    {"question_id":"", "answer":""}
  ]
}

Output: Kết quả chấm từng câu (MC/TF/SA chấm ngay, TL do
CHV_Grader chấm) + tổng điểm.

---

# Student Analysis

POST /api/student/analysis
Input: Student ID
Output: Learning Report (weak_points, strong_points, nhận xét,
gợi ý lệnh luyện tập tiếp theo)

---

# Download

GET /api/download/{file_id}
Output: PDF, LaTeX, JSON

---

# Upload

POST /api/upload
Output: File ID

---

# Authentication

POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout
GET /api/auth/me

---

# Admin

GET /api/admin/users
GET /api/admin/classes
POST /api/admin/create_class

---

# Quy tắc

- Frontend không đọc file trực tiếp.
- n8n không đọc file trực tiếp nếu có API.
- Python không trả dữ liệu cho Frontend.
- Mọi dữ liệu đều đi qua FastAPI.
- API chỉ trả JSON hoặc File, luôn bọc theo Response chuẩn.
- Không trả HTML.
- Validate whitelist tham số path (subject, chapter) trước khi
  ghép vào đường dẫn file — không cho phép path traversal.
===============================================================================

# Hiện trạng triển khai (Version 2.3 — 2026-07-28)

Các route dưới đây là API THẬT đang chạy trên VPS, thay thế phần
"Generate Exam / Generate PDF" dự kiến ở trên (chưa xây theo đúng
tên đó). Response vẫn theo cấu trúc chuẩn ở phần trên khi trả JSON;
khi trả file thì trả thẳng file nhị phân (không bọc JSON).

## Exam — chính thức (qua Curriculum, dùng cho Chat/n8n)

POST /api/exam/blueprint
POST /api/exam/blueprint-and-select
POST /api/exam/generate-pdf-auto

Input chung (generate-pdf-auto):
{
  "lop": 10,
  "tieu_de": "",
  "role": "teacher" | "student",
  "loai_he_so": "HeSo1" | "HeSo2_HeSo3",
  "ki_thi": null,
  "pham_vi_chuong": "chuong_1",
  "cau_truc_tu_hoc_sinh": null,
  "socau_ma_de": null,
  "cho_phep_thieu": false,
  "dinh_dang": "pdf"
}

Output: file PDF/TEX/ZIP (theo `dinh_dang`).

## Exam — thủ công / debug (không qua Curriculum)

GET  /api/exam/scope
POST /api/exam/generator
POST /api/exam/resolve-rules
POST /api/exam/select-questions
POST /api/exam/generate-pdf

## Đăng nhập / Đăng ký (KHÔNG theo /api/auth/* như dự kiến)

Triển khai thực tế dùng Supabase Auth + trang HTML (Jinja2), không
phải API JSON riêng:

GET  /login              (trang đăng nhập)
POST /login               (form, redirect /chat)
GET  /register            (chọn vai trò)
GET  /register/student
POST /register/student
GET  /register/teacher    (coming soon)

## Chat

GET  /chat                (trang chat)
POST /chat                (form message → n8n webhook → kết quả)

## Chưa triển khai (vẫn là TODO thật, không phải chỉ thiếu tài liệu)

- /api/exam/grade, /api/student/analysis, /api/admin/*
- /api/auth/* dạng JSON (hiện dùng cookie/session của Supabase qua
  trang HTML thay vì API JSON riêng — cần quyết định lại nếu sau
  này tách Frontend riêng khỏi Jinja2)
- Switch_OutputFormat "web_test", "json" (chỉ có "pdf"/"tex"/"zip")
- CN_QuestionValidator (không có bước kiểm tra trùng lặp câu hỏi)


===============================================================================

# Trạng thái triển khai thực tế (cập nhật 2026-08-06)

Xem chi tiết ở docs/16_CHANGELOG.md, Version 2.4. Doc 16 (v2.3)
đã ghi nhận trước đó là các route trong doc này chưa khớp thực tế.
Danh sách endpoint ĐANG HOẠT ĐỘNG (khác với danh sách mục tiêu ở
trên):

- POST /chat — nhận {message, conversation_id} (form), yêu cầu đã
  đăng nhập (cookie), gọi n8n, trả {success, message, data}.
- GET /api/chat/history — danh sách hội thoại của user đang đăng
  nhập.
- GET /api/chat/history/{conversation_id} — toàn bộ tin nhắn của
  1 hội thoại.
- POST /api/exam/generate-pdf-auto — sinh đề tự động theo lop/role/
  loai_he_so/ki_thi/pham_vi_chuong, trả file (PDF/zip). Có
  user_id/conversation_id tuỳ chọn để lưu lịch sử.
- POST /api/exam/export-loigiai — nhận {conversation_id}, tái sử
  dụng đề đã sinh gần nhất trong hội thoại đó để xuất PDF lời giải.
- POST /login, /logout, GET/POST /register — Supabase Auth, set/xoá
  cookie sb_access_token, sb_refresh_token.

Các route generate/pdf/latex/web/grade/student/download/admin ở
trên vẫn là mục tiêu kiến trúc, chưa triển khai đúng path đó.


===============================================================================

# Cập nhật 2026-08-07 — Grade API (MC/SA)

POST /api/exam/grade nay ĐÃ hoạt động thật trên VPS cho câu MC/SA (chấm tự
động bằng so khớp với JSON đáp án lưu ở bước sinh đề), lưu kết quả vào bảng
exam_history. Câu TL trả về trạng thái can_cham_tay, chờ CHV_Grader (chưa
làm). Chi tiết xem docs/16_CHANGELOG.md, Version 2.6.


===============================================================================

# Cập nhật 2026-08-12 — Grade API bằng ẢNH (grade-photo)

POST /api/exam/grade-photo (mới) ĐÃ hoạt động thật trên VPS: nhận ảnh chụp
Phiếu trả lời trắc nghiệm (MC/TF/SA) và/hoặc ảnh bài làm Tự luận viết tay,
gọi 2 webhook n8n (DocPhieuTraLoi đọc phiếu, CHV_Grader chấm tự luận), gộp
kết quả theo đúng schema Grade Result (doc 03), lưu exam_history. Input:

```json
{
  "de_id": null,
  "conversation_id": "",
  "user_id": "",
  "anh_phieu_base64": "",
  "anh_tuluan_base64": ""
}
```

Câu TF (Đúng/Sai) hiện luôn trả về trạng thái can_cham_tay dù đã đọc được
ảnh (answer_parser_service chưa trích được đáp án đúng cho TF). Chi tiết
xem docs/16_CHANGELOG.md, Version 2.8. Đã kiểm chứng end-to-end trên
production bằng ảnh giả (không lỗi, đúng schema); chưa kiểm chứng độ
chính xác đọc bằng ảnh chụp thật.



===============================================================================

# Cập nhật 2026-08-16 — Chọn lớp + Google Classroom (Version 2.17 → 2.22)

Chi tiết đầy đủ xem docs/16_CHANGELOG.md. Route THẬT đang chạy:

## Chọn lớp (học sinh tự chọn, không cần giáo viên xác nhận)

GET  /chon-lop   — trang chọn lớp (yêu cầu đã đăng nhập)
POST /chon-lop   — lưu khoi/lop vào profiles, thử tạo link tham gia
                   Classroom (xem dưới), rồi vào /chat

## Google Classroom (giáo viên kết nối 1 lần, không phải API JSON)

GET /gv/classroom/connect       — chuyển hướng màn hình đồng ý Google
GET /gv/classroom/callback      — nhận code, đổi lấy refresh_token, lưu
GET /gv/classroom/sync          — đồng bộ toàn bộ roster (email học
                                   sinh) từ Classroom về classroom_roster
GET /gv/classroom/debug-roster  — xem dữ liệu đã đồng bộ (debug)

Cả 4 route yêu cầu đã đăng nhập web. Không có API JSON riêng cho
Classroom — toàn bộ là route redirect/HTML, gọi trực tiếp Google
Classroom REST API qua app/services/classroom_service.py (không dùng
SDK google-api-python-client).

GHI CHÚ QUAN TRỌNG: courses.students.create (thêm thẳng học sinh vào
lớp) bị Google chặn 403 PERMISSION_DENIED với tài khoản Gmail cá nhân
(chỉ quản trị viên domain Google Workspace mới thêm thẳng được) — xem
Version 2.22. Cách đang dùng: tạo link + mã lớp (enrollment code) để
học sinh tự bấm "Tham gia" trên Classroom, không gọi API ghi (write)
nào thành công thật trên Classroom ngoài đọc roster/enrollment code.


===============================================================================

# Cập nhật 2026-08-17 — Làm bài trực tiếp trên web (Version 2.23)

Chi tiết đầy đủ xem docs/16_CHANGELOG.md, Version 2.23.

## Xem đề để làm bài (ẩn đáp án)

GET /api/exam/quiz/{de_id}

Trả về danh sách câu hỏi KHÔNG có đáp án đúng (đề_bai + phương_án cho
MC, phát_biểu cho TF, không thêm gì cho SA, ghi_chú cho TL). Đọc từ
file dapan_json đã lưu lúc sinh đề — file này cùng vòng đời dọn dẹp
1 ngày với các file PDF/TEX (cron cleanup_old_files.py có sẵn), trả
410 nếu đã bị dọn.

## Trang làm bài (HTML, không phải JSON)

GET /lam-bai/{de_id}     — yêu cầu đăng nhập, gọi GET /api/exam/quiz/
                            {de_id} rồi POST /api/exam/grade khi nộp
GET /gv/thong-ke          — trang thống kê năng lực (GV)
GET /gv/thong-ke/data     — API JSON cho trang trên, lọc ?khoi=&lop=

## POST /api/exam/grade — cập nhật câu TF

Câu TF nay ĐÃ chấm tự động (trước đó luôn can_cham_tay) — chấm theo
tỉ lệ tuyến tính, xem docs/03_DATA_STRUCTURE.md mục Grade Result mở
rộng cho TF.

## POST /api/exam/grade-photo — dùng thêm cho câu tự luận trong trang
   làm bài web

Trang /lam-bai/{de_id} có thể gọi endpoint này (đã có sẵn từ Version
2.8, không đổi API) chỉ với anh_tuluan_base64 (không anh_phieu_base64)
để chấm riêng phần tự luận qua CHV_Grader, gộp kết quả với /grade ở
phía Frontend (JS thuần, không thêm API mới).
