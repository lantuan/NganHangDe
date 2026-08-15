import unicodedata

FILE = "app/services/classroom_service.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

assert "tao_link_gia_nhap_lop" not in content, "Da co ham nay - khong chay lai script."

# ---- 1) Them import base64 (dung de tu dung lai link Classroom tu course_id) ----
old_import = '''from datetime import datetime, timezone
from urllib.parse import urlencode

import requests'''

assert content.count(old_import) == 1, "Khong tim thay khoi import goc."

new_import = '''import base64
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests'''

content = content.replace(old_import, new_import)

# ---- 2) Them ham tao_link_gia_nhap_lop o cuoi file (thay the cho them_hoc_sinh_vao_lop -
#          cach do bi Google chan 403 PERMISSION_DENIED voi tai khoan Gmail ca nhan, chi
#          quan tri vien domain Google Workspace moi duoc phep them thang hoc sinh) ----
old_tail_anchor = '''    try:
        return them_hoc_sinh_vao_lop(access_token, course_id, email)
    except Exception as e:
        print(f"LOI TU DONG GHI DANH CLASSROOM ({email}, {khoi}-{lop}):", e)
        return {"success": False, "message": "Loi khong xac dinh khi ghi danh Classroom."}'''

assert content.count(old_tail_anchor) == 1, "Khong tim thay cuoi ham tu_dong_ghi_danh_classroom."

new_tail = old_tail_anchor + '''


def tao_link_gia_nhap_lop(khoi: str, lop: str) -> dict:
    """
    THAY THE cho them_hoc_sinh_vao_lop/tu_dong_ghi_danh_classroom o tren -
    Google tra ve 403 PERMISSION_DENIED khi goi truc tiep courses.students.
    create() bang tai khoan Gmail ca nhan (cach nay chi duoc phep khi goi
    boi quan tri vien domain Google Workspace for Education, khong ap
    dung cho Classroom tao boi tai khoan Gmail thuong).

    Thay vao do: lay ma dang ky (enrollment code) cua lop, tu dung lai
    link tham gia lop tren Classroom (dang https://classroom.google.com/
    c/<ma_hoa_course_id>?cjc=<ma_dang_ky>) - hoc sinh chi can bam vao,
    dang nhap dung tai khoan, bam THAM GIA la xong (khong can tu tim
    lop/nhap ma).

    Tra ve dict {"success": bool, "link_tham_gia": str|None,
    "ma_dang_ky": str|None, "message": str} - KHONG raise loi ra ngoai.
    """
    course_id = MA_LOP_CLASSROOM.get((khoi, lop))
    if not course_id:
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": f"Chua co ma lop Classroom cho {khoi}-{lop}.",
        }

    refresh_token = lay_refresh_token()
    if not refresh_token:
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": "Chua ket noi Classroom (vao /gv/classroom/connect).",
        }

    try:
        access_token = lam_moi_access_token(refresh_token)
    except Exception as e:
        print("LOI LAM MOI ACCESS TOKEN (tao link gia nhap lop):", e)
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": "Khong lam moi duoc access token.",
        }

    try:
        ma_dang_ky = lay_enrollment_code(access_token, course_id)
    except Exception as e:
        print(f"LOI LAY ENROLLMENT CODE (tao link gia nhap, course_id={course_id}):", e)
        ma_dang_ky = None

    if not ma_dang_ky:
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": "Khong lay duoc ma dang ky cua lop tren Classroom.",
        }

    slug = base64.urlsafe_b64encode(str(course_id).encode()).decode().rstrip("=")
    link = f"https://classroom.google.com/c/{slug}?cjc={ma_dang_ky}"

    return {
        "success": True, "link_tham_gia": link, "ma_dang_ky": ma_dang_ky,
        "message": "OK",
    }'''

content = content.replace(old_tail_anchor, new_tail)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
