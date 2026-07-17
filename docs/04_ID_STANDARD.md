# TIÊU CHUẨN ID TOÀN HỆ THỐNG

Version: 1.0

---

# Mục tiêu

ID là xương sống của toàn bộ hệ thống.

Mọi thành phần đều làm việc bằng ID thay vì tên hiển thị.

Không được để AI suy luận tên bài, chương hoặc dạng toán.

Tất cả đều phải quy đổi thành ID chuẩn.

---

# Cấu trúc chung

Một ID đầy đủ có dạng:

L10_C1_B2_NB017A_MC_A

Ý nghĩa:

L10

↓

Khối

C1

↓

Chương

B2

↓

Bài

NB

↓

Mức độ

017A

↓

Mã năng lực

MC

↓

Loại câu

A

↓

Phiên bản

---

# Khối

L10

L11

L12

---

# Chương

C1

C2

C3

...

---

# Bài

B1

B2

B3

...

---

# Mức độ

NB

Nhận biết

TH

Thông hiểu

VD

Vận dụng

VDC

Vận dụng cao

---

# Mã năng lực

Ví dụ

001

002

017A

018

...

Mã này lấy từ Curriculum.

Không được tự sinh.

---

# Loại câu

MC

Trắc nghiệm nhiều lựa chọn

DS

Đúng Sai

TL

Tự luận

SA

Trả lời ngắn

Có thể mở rộng thêm trong tương lai.

---

# Phiên bản

A

B

C

...

Một năng lực có thể có nhiều câu hỏi khác nhau.

Ví dụ

L10_C1_B2_NB017A_MC_A

L10_C1_B2_NB017A_MC_B

L10_C1_B2_NB017A_MC_C

---

# PPCT

PPCT sử dụng ID

Ví dụ

L10_C1_B2

Không cần mức độ.

Không cần loại câu.

---

# Curriculum

Ví dụ

L10_C1_B2_TH014

Trong đó

TH014

là năng lực.

---

# Mapping

Ví dụ

L10_C1_B2_VD020_TL_A

Mapping là cầu nối giữa

Curriculum

↓

Python Generator

---

# Python

Tên file

L10_C1.py

Tên hàm

L10_C1_B2_NB017A_MC_A()

Không đặt tên theo tiếng Việt.

---

# API

Mọi API đều trả ID.

Không trả text trước.

Ví dụ

{
    "lesson_id":"L10_C1_B2"
}

Không dùng

{
    "lesson":"Mệnh đề"
}

---

# n8n

Toàn bộ Workflow làm việc bằng ID.

Không dùng tên bài.

---

# AI

AI không được tự suy luận ID.

AI chỉ nhận ID.

Hoặc sinh Request để Code đổi sang ID.

---

# Database

Các bảng chỉ lưu ID.

Ví dụ

lesson_id

question_id

curriculum_id

mapping_id

Không lưu tên bài nếu không cần thiết.

---

# Quy tắc bất biến

ID là chuẩn duy nhất.

Không sửa ID sau khi phát hành.

Nếu thay đổi nội dung chỉ tạo Version mới.

Ví dụ

L10_C1_B2_NB017A_MC_B

Không sửa

L10_C1_B2_NB017A_MC_A

---

# Mục tiêu cuối cùng

Toàn bộ hệ thống:

FastAPI

↓

n8n

↓

Python

↓

LaTeX

↓

Dashboard

↓

AI

↓

Database

đều giao tiếp bằng ID.

Tên hiển thị chỉ dùng ở giao diện người dùng.