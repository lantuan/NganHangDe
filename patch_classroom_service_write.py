import unicodedata

FILE = "app/services/classroom_service.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "them_hoc_sinh_vao_lop" not in content, "Da co ham nay - khong chay lai script."

# ---- 1) Mo rong SCOPES: can quyen GHI (khong chi doc) + quyen doc courses de lay enrollment code ----
old_scopes = '''# Chi can quyen doc danh sach lop + quyen xem email (Google an email hoc
# sinh mac dinh, phai xin rieng scope profile.emails moi thay duoc).
SCOPES = (
    "https://www.googleapis.com/auth/classroom.rosters.readonly "
    "https://www.googleapis.com/auth/classroom.profile.emails"
)'''

assert content.count(old_scopes) == 1, "Khong tim thay khoi SCOPES goc."

new_scopes = '''# classroom.rosters (KHONG phai .readonly) - can quyen GHI de tu dong
# them hoc sinh vao lop that tren Classroom (khong chi doc danh sach).
# classroom.profile.emails - xem email hoc sinh (Google an mac dinh).
# classroom.courses.readonly - doc thong tin lop (lay ma dang ky/
# enrollmentCode, can de them hoc sinh vao dung lop).
# LUU Y: doi scope thi phai vao lai Google Cloud Console > Data Access
# them 2 scope moi nay, ROI phai lam lai /gv/classroom/connect de xin
# refresh_token moi (refresh_token cu chi mang quyen doc, khong the tu
# nhien co them quyen ghi).
SCOPES = (
    "https://www.googleapis.com/auth/classroom.rosters "
    "https://www.googleapis.com/auth/classroom.profile.emails "
    "https://www.googleapis.com/auth/classroom.courses.readonly"
)'''

content = content.replace(old_scopes, new_scopes)

# ---- 2) Them ham lay enrollment code + them hoc sinh vao lop + ham cap cao goi tu /chon-lop ----
old_tail_anchor = '''def lay_toan_bo_roster():
    """Tra ve toan bo du lieu bang classroom_roster (dung de debug/kiem tra)."""
    ket_qua = (
        supabase.table("classroom_roster")
        .select("email, khoi, lop, ho_ten, synced_at")
        .order("khoi")
        .order("lop")
        .execute()
    )
    return ket_qua.data'''

assert content.count(old_tail_anchor) == 1, "Khong tim thay ham lay_toan_bo_roster goc."

new_tail = old_tail_anchor + '''


def lay_enrollment_code(access_token: str, course_id: str):
    """
    Doc ma dang ky (enrollment code) cua 1 lop - can de them hoc sinh
    vao lop bang API (khong the them truc tiep neu khong co ma nay, tru
    khi la quan tri vien domain). Tra ve None neu loi (vd het quyen).
    """
    res = requests.get(
        f"{CLASSROOM_API_BASE}/courses/{course_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if res.status_code != 200:
        print(f"LOI DOC ENROLLMENT CODE (course_id={course_id}):", res.status_code, res.text[:300])
        return None
    return res.json().get("enrollmentCode")


def them_hoc_sinh_vao_lop(access_token: str, course_id: str, email: str) -> dict:
    """
    Them 1 hoc sinh (theo email) vao dung lop that tren Google Classroom,
    dung ma dang ky (enrollment code) cua lop do. Tra ve dict {"success":
    bool, "message": str} - KHONG raise loi ra ngoai, de goi tu
    /chon-lop ma khong lam gian doan luong dang ky/chon lop cua hoc sinh
    du Classroom co loi (vd email khong phai tai khoan Google that, da
    la thanh vien lop roi...).
    """
    ma_dang_ky = lay_enrollment_code(access_token, course_id)
    if not ma_dang_ky:
        return {"success": False, "message": "Khong lay duoc ma dang ky cua lop tren Classroom."}

    res = requests.post(
        f"{CLASSROOM_API_BASE}/courses/{course_id}/students",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"enrollmentCode": ma_dang_ky},
        json={"userId": email},
        timeout=30,
    )
    if res.status_code == 200:
        return {"success": True, "message": "Da them vao lop tren Classroom."}

    # Da la thanh vien san roi (Google tra ve 409/ALREADY_EXISTS) - coi la thanh cong, khong phai loi that.
    if res.status_code == 409:
        return {"success": True, "message": "Hoc sinh da la thanh vien lop nay tren Classroom."}

    print(f"LOI THEM HOC SINH VAO CLASSROOM (course_id={course_id}, email={email}):", res.status_code, res.text[:300])
    return {"success": False, "message": f"Google Classroom tu choi (ma loi {res.status_code})."}


def tu_dong_ghi_danh_classroom(email: str, khoi: str, lop: str) -> dict:
    """
    Ham cap cao: goi tu app/routers/chat.py ngay sau khi hoc sinh chon
    lop o /chon-lop - tu dong ghi danh (join) hoc sinh do vao dung lop
    that tren Google Classroom bang chinh email dang nhap web.

    CHI thanh cong neu email nay la tai khoan Google that (hoc sinh
    dang nhap bang Google, hoac dang ky bang dia chi Gmail that). Neu
    khong, Google Classroom se tu choi va ham nay tra ve success=False
    - KHONG raise loi, vi day chi la tien ich them, khong duoc phep
    chan hoc sinh vao duoc /chat cua web du Classroom co loi gi.
    """
    course_id = MA_LOP_CLASSROOM.get((khoi, lop))
    if not course_id:
        return {"success": False, "message": f"Chua co ma lop Classroom cho {khoi}-{lop}."}

    refresh_token = lay_refresh_token()
    if not refresh_token:
        return {"success": False, "message": "Chua ket noi Classroom (vao /gv/classroom/connect)."}

    try:
        access_token = lam_moi_access_token(refresh_token)
    except Exception as e:
        print("LOI LAM MOI ACCESS TOKEN (tu dong ghi danh Classroom):", e)
        return {"success": False, "message": "Khong lam moi duoc access token."}

    try:
        return them_hoc_sinh_vao_lop(access_token, course_id, email)
    except Exception as e:
        print(f"LOI TU DONG GHI DANH CLASSROOM ({email}, {khoi}-{lop}):", e)
        return {"success": False, "message": "Loi khong xac dinh khi ghi danh Classroom."}'''

content = content.replace(old_tail_anchor, new_tail)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
