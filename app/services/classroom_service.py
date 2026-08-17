"""
Dong bo danh sach email hoc sinh tu Google Classroom, dung de tu dong
ghep lop khi hoc sinh dang ky/dang nhap (khong can chon tay o /chon-lop,
khong can giao vien xac nhan).

Luong hoat dong:
1. Giao vien vao GET /gv/classroom/connect (1 lan duy nhat, hoac lam
   lai neu refresh_token bi Google thu hoi) - dang nhap Google, cho
   phep quyen doc danh sach lop + email -> Google tra ve "code" ->
   GET /gv/classroom/callback doi code lay refresh_token, luu vao
   bang public.classroom_oauth (chi 1 dong, id=1).
2. GET /gv/classroom/sync - dung refresh_token da luu de xin
   access_token moi, goi Classroom API cho tung lop trong
   MA_LOP_CLASSROOM (app/core/lop_config.py), ghi ket qua (email, khoi,
   lop, ho_ten) vao bang public.classroom_roster - chay lai duoc nhieu
   lan (vd giao vien them hoc sinh moi tren Classroom), moi lan upsert
   de cap nhat.
3. tim_lop_theo_email() - app/routers/chat.py goi ham nay khi hoc sinh
   chua co lop, de tu dong ghep truoc khi roi ve /chon-lop tu chon.
"""

import base64
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests

from app.core.config import GOOGLE_CLASSROOM_CLIENT_ID, GOOGLE_CLASSROOM_CLIENT_SECRET
from app.core.lop_config import MA_LOP_CLASSROOM
from app.core.supabase import supabase

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
CLASSROOM_API_BASE = "https://classroom.googleapis.com/v1"

REDIRECT_URI = "https://nganhangdechv.tech/gv/classroom/callback"

# classroom.rosters (KHONG phai .readonly) - can quyen GHI de tu dong
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
)


def _thoi_gian_hien_tai() -> str:
    return datetime.now(timezone.utc).isoformat()


def tao_url_xac_thuc() -> str:
    """
    Tra ve URL de giao vien bam vao, dang nhap Google va cho phep quyen.
    access_type=offline + prompt=consent de Google LUON tra ve
    refresh_token (khong chi tra 1 lan dau tien) - can vi luong nay co
    the phai lam lai neu refresh_token cu bi thu hoi/het han.
    """
    tham_so = {
        "client_id": GOOGLE_CLASSROOM_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(tham_so)}"


def doi_code_lay_token(code: str) -> dict:
    """
    Doi authorization code (Google redirect ve /gv/classroom/callback
    kem ?code=...) lay access_token + refresh_token that.
    """
    res = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": GOOGLE_CLASSROOM_CLIENT_ID,
            "client_secret": GOOGLE_CLASSROOM_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    res.raise_for_status()
    return res.json()


def lam_moi_access_token(refresh_token: str) -> str:
    """Dung refresh_token da luu de xin access_token moi (song ~1 gio)."""
    res = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "refresh_token": refresh_token,
            "client_id": GOOGLE_CLASSROOM_CLIENT_ID,
            "client_secret": GOOGLE_CLASSROOM_CLIENT_SECRET,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    res.raise_for_status()
    return res.json()["access_token"]


def luu_refresh_token(refresh_token: str):
    """Ghi de refresh_token vao bang public.classroom_oauth (chi 1 dong, id=1)."""
    supabase.table("classroom_oauth").upsert({
        "id": 1,
        "refresh_token": refresh_token,
        "updated_at": _thoi_gian_hien_tai(),
    }).execute()


def lay_refresh_token():
    """Doc refresh_token da luu, None neu chua ket noi Classroom lan nao."""
    try:
        ket_qua = (
            supabase.table("classroom_oauth")
            .select("refresh_token")
            .eq("id", 1)
            .single()
            .execute()
        )
        return ket_qua.data.get("refresh_token") if ket_qua.data else None
    except Exception as e:
        print("LOI DOC REFRESH TOKEN CLASSROOM:", e)
        return None


def _lay_danh_sach_hoc_sinh_1_lop(access_token: str, course_id: str) -> list[dict]:
    """
    Goi Classroom API lay toan bo hoc sinh cua 1 lop (co xu ly phan
    trang). Tra ve list [{"email": ..., "ho_ten": ...}, ...] - bo qua
    hoc sinh khong co email (truong hop hiem, thieu quyen xem).
    """
    hoc_sinh = []
    page_token = None
    while True:
        params = {"pageSize": 100}
        if page_token:
            params["pageToken"] = page_token
        res = requests.get(
            f"{CLASSROOM_API_BASE}/courses/{course_id}/students",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            timeout=30,
        )
        if res.status_code != 200:
            print(f"LOI DOC HOC SINH LOP (course_id={course_id}):", res.status_code, res.text[:300])
            break
        du_lieu = res.json()
        for hs in du_lieu.get("students", []):
            ho_so = hs.get("profile", {}) or {}
            email = ho_so.get("emailAddress")
            if email:
                hoc_sinh.append({
                    "email": email.strip().lower(),
                    "ho_ten": (ho_so.get("name") or {}).get("fullName", ""),
                })
        page_token = du_lieu.get("nextPageToken")
        if not page_token:
            break
    return hoc_sinh


def dong_bo_toan_bo() -> dict:
    """
    Dong bo TOAN BO danh sach email hoc sinh tu Classroom (dung
    MA_LOP_CLASSROOM) vao bang public.classroom_roster. An toan chay
    lai nhieu lan (vd giao vien them hoc sinh moi vao Classroom, chi
    can vao lai /gv/classroom/sync). Tra ve dict thong ke
    {"khoi-lop": so_luong_email} de kiem tra bang mat.
    """
    refresh_token = lay_refresh_token()
    if not refresh_token:
        raise RuntimeError("Chua ket noi Classroom - vao /gv/classroom/connect truoc.")

    access_token = lam_moi_access_token(refresh_token)

    thong_ke = {}
    for (khoi, lop), course_id in MA_LOP_CLASSROOM.items():
        danh_sach = _lay_danh_sach_hoc_sinh_1_lop(access_token, course_id)
        thong_ke[f"{khoi}-{lop}"] = len(danh_sach)

        for hs in danh_sach:
            try:
                supabase.table("classroom_roster").upsert({
                    "email": hs["email"],
                    "khoi": khoi,
                    "lop": lop,
                    "ho_ten": hs["ho_ten"],
                    "synced_at": _thoi_gian_hien_tai(),
                }).execute()
            except Exception as e:
                print(f"LOI GHI ROSTER ({hs['email']}, {khoi}-{lop}):", e)

    return thong_ke


def tim_lop_theo_email(email: str):
    """
    Tra ve {"khoi":..., "lop":...} neu email nay co trong danh sach da
    dong bo tu Classroom, None neu khong tim thay (hoc sinh se roi ve
    /chon-lop tu chon nhu binh thuong - vd chua dong bo, hoc sinh dung
    email khac email dang ky tren Classroom...).
    """
    if not email:
        return None
    try:
        ket_qua = (
            supabase.table("classroom_roster")
            .select("khoi, lop")
            .eq("email", email.strip().lower())
            .limit(1)
            .execute()
        )
        if ket_qua.data:
            return ket_qua.data[0]
    except Exception as e:
        print("LOI TIM LOP THEO EMAIL:", e)
    return None


def lay_toan_bo_roster():
    """Tra ve toan bo du lieu bang classroom_roster (dung de debug/kiem tra)."""
    ket_qua = (
        supabase.table("classroom_roster")
        .select("email, khoi, lop, ho_ten, synced_at")
        .order("khoi")
        .order("lop")
        .execute()
    )
    return ket_qua.data


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
        return {"success": False, "message": "Không lấy được mã đăng ký của lớp trên Classroom."}

    res = requests.post(
        f"{CLASSROOM_API_BASE}/courses/{course_id}/students",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"enrollmentCode": ma_dang_ky},
        json={"userId": email},
        timeout=30,
    )
    if res.status_code == 200:
        return {"success": True, "message": "Đã thêm vào lớp trên Classroom."}

    # Da la thanh vien san roi (Google tra ve 409/ALREADY_EXISTS) - coi la thanh cong, khong phai loi that.
    if res.status_code == 409:
        return {"success": True, "message": "Học sinh đã là thành viên lớp này trên Classroom."}

    print(f"LOI THEM HOC SINH VAO CLASSROOM (course_id={course_id}, email={email}):", res.status_code, res.text[:300])
    return {"success": False, "message": f"Google Classroom từ chối (mã lỗi {res.status_code})."}


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
        return {"success": False, "message": f"Chưa có mã lớp Classroom cho {khoi}-{lop}."}

    refresh_token = lay_refresh_token()
    if not refresh_token:
        return {"success": False, "message": "Chưa kết nối Classroom (vào /gv/classroom/connect)."}

    try:
        access_token = lam_moi_access_token(refresh_token)
    except Exception as e:
        print("LOI LAM MOI ACCESS TOKEN (tu dong ghi danh Classroom):", e)
        return {"success": False, "message": "Không làm mới được access token."}

    try:
        return them_hoc_sinh_vao_lop(access_token, course_id, email)
    except Exception as e:
        print(f"LOI TU DONG GHI DANH CLASSROOM ({email}, {khoi}-{lop}):", e)
        return {"success": False, "message": "Lỗi không xác định khi ghi danh Classroom."}


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
            "message": f"Chưa có mã lớp Classroom cho {khoi}-{lop}.",
        }

    refresh_token = lay_refresh_token()
    if not refresh_token:
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": "Chưa kết nối Classroom (vào /gv/classroom/connect).",
        }

    try:
        access_token = lam_moi_access_token(refresh_token)
    except Exception as e:
        print("LOI LAM MOI ACCESS TOKEN (tao link gia nhap lop):", e)
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": "Không làm mới được access token.",
        }

    try:
        ma_dang_ky = lay_enrollment_code(access_token, course_id)
    except Exception as e:
        print(f"LOI LAY ENROLLMENT CODE (tao link gia nhap, course_id={course_id}):", e)
        ma_dang_ky = None

    if not ma_dang_ky:
        return {
            "success": False, "link_tham_gia": None, "ma_dang_ky": None,
            "message": "Không lấy được mã đăng ký của lớp trên Classroom.",
        }

    slug = base64.urlsafe_b64encode(str(course_id).encode()).decode().rstrip("=")
    link = f"https://classroom.google.com/c/{slug}?cjc={ma_dang_ky}"

    return {
        "success": True, "link_tham_gia": link, "ma_dang_ky": ma_dang_ky,
        "message": "OK",
    }
