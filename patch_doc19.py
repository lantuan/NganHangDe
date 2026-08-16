import unicodedata

FILE = "docs/19_SYSTEM_MAP.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "classroom_service.py" not in content, "Da co addendum nay - khong chay lai script."

expected_tail = """# TODO

Cập nhật khi có AI mới, Workflow mới, API mới, Database mới."""

assert content.rstrip().endswith(expected_tail), (
    "Noi dung cuoi file khac du kien - dung lai, kiem tra thu cong "
    "truoc khi them addendum."
)

addendum = '''


===============================================================================

# Cập nhật 2026-08-16 — Google Classroom (Version 2.17 → 2.22)

Nhánh RIÊNG, không đi qua CHV_Fun/n8n (khác luồng sinh đề/chat ở trên):

User (học sinh) → /chon-lop → FastAPI (app/routers/chat.py)
→ app/services/classroom_service.py → Google Classroom REST API
→ (đọc roster / lấy mã lớp — không ghi thẳng được, xem doc 14)

| Thành phần | Vai trò | Tài liệu |
|------------|---------|----------|
| app/core/lop_config.py | DANH_SACH_LOP, MA_LOP_CLASSROOM | 02 |
| app/services/classroom_service.py | OAuth + gọi Google Classroom API | 14 |
| app/routers/classroom.py | /gv/classroom/connect,callback,sync,debug-roster | 05 |
| classroom_oauth, classroom_roster | Lưu refresh_token, roster đồng bộ | 12 |

Chi tiết đầy đủ xem docs/16_CHANGELOG.md, Version 2.17 → 2.22.
'''

content = content + addendum

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them addendum vao {FILE} ({goc} -> {len(content)} ky tu)")
