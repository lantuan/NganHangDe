import unicodedata

FILE = "app/routers/chat.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "tu_dong_ghi_danh_classroom" not in content, "Da co doan nay - khong chay lai script."

old_block = '''    supabase_service.cap_nhat_lop_hoc_sinh(user.id, khoi, lop)
    return RedirectResponse("/chat", status_code=303)'''

assert content.count(old_block) == 1, "Khong tim thay khoi chon_lop_submit goc."

new_block = '''    supabase_service.cap_nhat_lop_hoc_sinh(user.id, khoi, lop)
    # Tu dong ghi danh (join) hoc sinh vao dung lop that tren Google
    # Classroom bang chinh email dang nhap web - chi thanh cong neu email
    # la tai khoan Google that va giao vien da ket noi Classroom (xem
    # app/services/classroom_service.py). Loi gi cung KHONG duoc chan
    # hoc sinh vao /chat, nen khong kiem tra ket qua o day.
    classroom_service.tu_dong_ghi_danh_classroom(user.email, khoi, lop)
    return RedirectResponse("/chat", status_code=303)'''

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
