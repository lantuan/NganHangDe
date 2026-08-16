import unicodedata

FILE = "docs/02_FOLDER_STRUCTURE.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "classroom_service.py" not in content, "Da co addendum nay - khong chay lai script."

expected_tail = """- Không tạo thư mục ngoài tài liệu này.
- Một loại dữ liệu chỉ nằm tại một thư mục.
- Curriculum, Mapping và Python Bank luôn tách theo lớp và chương.
- Mọi Prompt AI nằm trong data/prompts.
- Mọi file sinh ra nằm trong output.
- Không commit temp.
- Không commit logs."""

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong "
    "truoc khi them addendum."
)

addendum = '''


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
'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them addendum vao {FILE} ({goc} -> {len(content)} ky tu)")
