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
