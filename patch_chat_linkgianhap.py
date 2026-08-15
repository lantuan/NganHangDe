import unicodedata

FILE = "app/routers/chat.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "tao_link_gia_nhap_lop" not in content, "Da co doan nay - khong chay lai script."

old_block = '''    supabase_service.cap_nhat_lop_hoc_sinh(user.id, khoi, lop)
    # Tu dong ghi danh (join) hoc sinh vao dung lop that tren Google
    # Classroom bang chinh email dang nhap web - chi thanh cong neu email
    # la tai khoan Google that va giao vien da ket noi Classroom (xem
    # app/services/classroom_service.py). Loi gi cung KHONG duoc chan
    # hoc sinh vao /chat, nen khong kiem tra ket qua o day.
    classroom_service.tu_dong_ghi_danh_classroom(user.email, khoi, lop)
    return RedirectResponse("/chat", status_code=303)'''

assert content.count(old_block) == 1, "Khong tim thay khoi chon_lop_submit (ban V2.21) goc."

new_block = '''    supabase_service.cap_nhat_lop_hoc_sinh(user.id, khoi, lop)
    # Google chan cach them thang hoc sinh qua API (403 PERMISSION_DENIED
    # voi tai khoan Gmail ca nhan - xem app/services/classroom_service.py:
    # tao_link_gia_nhap_lop). Thay vao do tao san link + ma dang ky, hoc
    # sinh tu bam THAM GIA 1 lan tren Classroom. Khong tao duoc link (vd
    # giao vien chua ket noi Classroom) thi bo qua, vao thang /chat nhu
    # cu - khong duoc chan hoc sinh du Classroom co loi gi.
    ket_qua_classroom = classroom_service.tao_link_gia_nhap_lop(khoi, lop)
    if not ket_qua_classroom["success"]:
        return RedirectResponse("/chat", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="chat/tham_gia_lop_classroom.html",
        context={
            "khoi": khoi,
            "lop": lop,
            "link_tham_gia": ket_qua_classroom["link_tham_gia"],
            "ma_dang_ky": ket_qua_classroom["ma_dang_ky"],
        },
    )'''

content = content.replace(old_block, new_block)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
