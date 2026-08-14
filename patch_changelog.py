"""Them Version 2.9 vao cuoi docs/16_CHANGELOG.md."""

FILE = "docs/16_CHANGELOG.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

goc = len(content)

anchor = '''- Đã kiểm chứng end-to-end trên production (sinh đề thật qua web, gọi
  POST /api/exam/grade-photo thật, cả 2 webhook n8n Production URL) —
  không lỗi 500/502, đúng schema Grade Result. Ảnh dùng để test là ảnh
  giả (không phải phiếu đã tô/bài làm thật) nên điểm ra 0 — CHƯA kiểm
  chứng độ chính xác đọc ảnh thật (cần bản in để tô/viết tay thật, để
  sau khi có điều kiện in ấn).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

assert content.count(anchor) == 1, "Khong tim thay cuoi Version 2.8."

addendum = '''


===============================================================================

Version 2.9

Ngày

2026-08-13

Nội dung

- Đơn giản hoá trang đăng nhập (app/templates/auth/login.html): xoá 4
  link nav placeholder (Tính năng/Giải pháp/Bảng giá/Tài liệu) không dẫn
  đi đâu, chỉ giữ logo + Đăng ký.
- "Ghi nhớ đăng nhập" chuyển từ checkbox trang trí sang có tác dụng thật:
  app/routers/auth.py::login() nhận thêm tham số remember (Form); nếu
  tick thì cookie sb_access_token/sb_refresh_token sống lâu như cũ (7/30
  ngày), không tick thì set session cookie (không truyền max_age — tự
  hết khi đóng trình duyệt).
- "Đăng nhập bằng Google" chuyển từ nút trang trí sang OAuth thật qua
  Supabase, theo mô hình client-side.
- CẦN NGƯỜI DÙNG TỰ CẤU HÌNH: bật Google provider trong Supabase
  Dashboard, tạo OAuth Client ID/Secret ở Google Cloud Console, khai báo
  Redirect URL https://nganhangdechv.tech/auth/callback trong Supabase
  Dashboard. Xác nhận SUPABASE_KEY trong .env là khoá "anon public".
- CHƯA kiểm chứng end-to-end (cần cấu hình Dashboard xong mới bấm thử
  được nút Google thật trên production).

Người thực hiện

Mai Hà Lan (cùng Claude)'''

content = content.replace(anchor, anchor + addendum)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da them Version 2.9 vao {FILE} ({goc} -> {len(content)} ky tu)")
