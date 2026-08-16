# FOLDER STRUCTURE

Version: 1.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Quy định toàn bộ cấu trúc thư mục của dự án Ngân Hàng Đề AI.

Không tự ý tạo thư mục ngoài tài liệu này.

---

# Root

```
NganHangDe/
```

```
app/
```

Backend FastAPI.

```
data/
```

Toàn bộ dữ liệu.

```
docs/
```

Sổ tay kỹ thuật.

```
scripts/
```

Script hỗ trợ.

```
templates/
```

Template LaTeX.

```
tests/
```

Kiểm thử.

```
output/
```

File sinh ra.

```
logs/
```

Log hệ thống.

---

# app/

```
app/

├── api/
├── core/
├── routers/
├── services/
├── models/
├── schemas/
├── utils/
├── static/
├── templates/
└── main.py
```

---

# data/

```
data/

├── curriculum/
├── mapping/
├── ppct/
├── python_bank/
├── prompts/
├── config/
├── uploads/
├── exports/
└── temp/
```

---

# curriculum/

```
curriculum/

toan10/

toan11/

toan12/
```

Mỗi chương một file.

Ví dụ

```
L10_C1.json

L10_C2.json
```

---

# mapping/

```
mapping/

toan10/

toan11/

toan12/
```

Mỗi chương một file.

---

# ppct/

```
ppct/

toan10.json

toan11.json

toan12.json
```

---

# python_bank/

```
python_bank/

toan10/

toan11/

toan12/
```

Trong mỗi lớp

```
L10_C1.py

L10_C2.py

...
```

---

# prompts/

```
prompts/

CHV_Fun.md

CHV_RequestParser.md

CHV_ExamPlanner.md

CHV_AbilityPlanner.md

CHV_Analyzer.md

CHV_Help.md

CHV_Reject.md
```

---

# config/

```
config/

settings.json

exam_rules.json

difficulty.json
```

---

# uploads/

Người dùng upload.

---

# exports/

PDF

LaTeX

JSON

Web Test

---

# temp/

File tạm.

---

# docs/

```
docs/

00_PROJECT_OVERVIEW.md

01_ARCHITECTURE.md

02_FOLDER_STRUCTURE.md

03_DATA_STRUCTURE.md

04_ID_STANDARD.md

05_API_SPECIFICATION.md

06_N8N_WORKFLOW.md

07_AI_AGENTS.md

08_CODE_NODES.md

09_EXAM_GENERATION.md

10_PYTHON_GENERATOR.md

11_LATEX_ENGINE.md

12_DATABASE.md

13_FRONTEND.md

14_DEPLOYMENT.md

15_DEVELOPMENT_ROADMAP.md

16_CHANGELOG.md

17_NAMING_CONVENTIONS.md

18_PROMPT_LIBRARY.md
```

---

# output/

```
output/

pdf/

latex/

json/

web_test/
```

---

# logs/

```
logs/

api/

n8n/

python/

latex/
```

---

# tests/

```
tests/

api/

python/

latex/

workflow/
```

---

# Quy tắc

- Không tạo thư mục ngoài tài liệu này.
- Một loại dữ liệu chỉ nằm tại một thư mục.
- Curriculum, Mapping và Python Bank luôn tách theo lớp và chương.
- Mọi Prompt AI nằm trong data/prompts.
- Mọi file sinh ra nằm trong output.
- Không commit temp.
- Không commit logs.


===============================================================================

# Cập nhật 2026-08-16 — file thực tế thêm cho tính năng lớp học / Classroom

Xem chi tiết ở docs/16_CHANGELOG.md, Version 2.17 → 2.22. Bổ sung các
file THẬT đang chạy trên VPS mà cấu trúc mục tiêu ở trên (app/api,
app/schemas, app/utils — hiện chưa dùng đến) chưa liệt kê:

```
app/
├── core/
│   ├── lop_config.py          (DANH_SACH_LOP, MA_LOP_CLASSROOM)
│   └── ...
├── services/
│   ├── classroom_service.py   (OAuth + Google Classroom API)
│   └── ...
├── routers/
│   ├── classroom.py           (/gv/classroom/*)
│   └── ...
└── templates/
    └── chat/
        ├── chon_lop.html                  (học sinh tự chọn lớp)
        └── tham_gia_lop_classroom.html    (xác nhận tham gia Classroom)
```

Thực tế app/ đang dùng đúng core/, services/, routers/, templates/,
static/, main.py — không có api/, schemas/, utils/ như liệt kê ở cấu
trúc mục tiêu phần trên (chưa cần tách, chưa gây vấn đề).
