# CẤU TRÚC THƯ MỤC DỰ ÁN

Version: 1.0

Trạng thái:

🟡 Đang triển khai

---

# Mục tiêu

Quy định thống nhất cấu trúc thư mục của toàn bộ dự án Ngân Hàng Đề AI.

Mọi thành viên và AI khi phát triển đều phải tuân theo cấu trúc này.

Không tạo thư mục hoặc đặt file theo cảm hứng.

---

# Nguyên tắc

## 1. Phân tách theo chức năng

Mỗi thư mục chỉ phục vụ một mục đích.

Ví dụ

app/

chỉ chứa source code Web.

data/

chỉ chứa dữ liệu.

generator/

chỉ chứa Python Generator.

docs/

chỉ chứa tài liệu.

---

## 2. Không lưu dữ liệu lẫn với source code

Sai

app/

curriculum.json

Đúng

data/curriculum/

...

---

## 3. Không lưu file tạm

Không commit

__pycache__

.pyc

.aux

.log

.pdf tạm

temp/

output/

...

---

## 4. Source code phải độc lập dữ liệu

Source code không được hardcode nội dung chương trình.

Mọi dữ liệu đều đọc từ

data/

hoặc

Supabase

---

## 5. Một loại dữ liệu chỉ có một nơi lưu

PPCT

↓

data/ppct

Curriculum

↓

data/curriculum

Mapping

↓

data/mapping

Python Bank

↓

data/python_bank

---

# Cấu trúc tổng thể

```
NganHangDe/

app/

data/

generator/

n8n/

docs/

tests/

```

---

# app/

Chứa toàn bộ Web.

Ví dụ

```
app/

main.py

routers/

services/

models/

templates/

static/

core/

```

Không lưu

JSON

PDF

LaTeX

Curriculum

PPCT

---

# data/

Chứa toàn bộ dữ liệu.

```
data/

config/

curriculum/

mapping/

ppct/

python_bank/

uploads/

exports/

temp/

prompts/

```

---

## data/config

Cấu hình hệ thống.

Ví dụ

```
config.json

exam_rule.json

difficulty.json
```

TODO

---

## data/ppct

Lưu Phân phối chương trình.

Hiện tại

```
toan10.json

toan11.json

toan12.json
```

Một khối

=

Một file JSON.

---

## data/curriculum

Lưu chuẩn năng lực.

```
toan10/

L10_C1.json

L10_C2.json

...

toan11/

...

toan12/

...
```

Một chương

=

Một file.

---

## data/mapping

Lưu Mapping năng lực.

```
toan10/

L10_C1.json

...

toan11/

...

toan12/
```

Một chương

=

Một file.

---

## data/python_bank

Lưu Python Generator.

```
toan10/

L10_C1.py

L10_C2.py

...

toan11/

...

toan12/
```

Một chương

=

Một file Python.

Không chia theo bài.

---

## data/prompts

Lưu Prompt chuẩn.

TODO.

---

## data/uploads

Lưu file người dùng tải lên.

Ví dụ

Ảnh

Word

Excel

PDF

Không commit Git.

---

## data/exports

Lưu file sinh ra.

Ví dụ

PDF

LaTeX

DOCX

Không commit Git.

---

## data/temp

Lưu file tạm.

Có thể xóa bất kỳ lúc nào.

Không commit Git.

---

# generator/

Chứa Engine sinh câu hỏi.

Ví dụ

```
generator/

latex/

python/

utils/

...
```

TODO.

---

# n8n/

Lưu Workflow.

Ví dụ

```
workflow.json

credential_template.json

README.md
```

TODO.

---

# docs/

Toàn bộ Sổ tay kỹ thuật.

Không lưu tài liệu linh tinh.

---

# tests/

Toàn bộ Test.

Ví dụ

```
API Test

Python Test

Generator Test

Integration Test
```

TODO.

---

# Quy tắc mở rộng

Khi thêm module mới

Không tạo thư mục ở Root.

Ví dụ

Sai

```
lesson/

AI/

exam/

```

Đúng

```
app/

data/

generator/

```

hoặc

tạo module con đúng chức năng.

---

# Không được phép

Không lưu JSON trong app/

Không lưu Python trong data/curriculum

Không lưu PDF trong Git

Không lưu file build

Không lưu file cache

---

# TODO

Hoàn thiện cấu trúc generator.

Hoàn thiện cấu trúc tests.

Hoàn thiện cấu trúc n8n.

Hoàn thiện cấu trúc frontend.