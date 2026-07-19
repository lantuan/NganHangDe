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