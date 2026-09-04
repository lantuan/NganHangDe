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
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests

from app.core.config import GOOGLE_CLASSROOM_CLIENT_ID, GOOGLE_CLASSROOM_CLIENT_SECRET
from app.core.lop_config import MA_LOP_CLASSROOM
from app.core.supabase import supabase
from app.services import history_service

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
    "https://www.googleapis.com/auth/classroom.courses.readonly "
    "https://www.googleapis.com/auth/classroom.coursework.students "
    "https://www.googleapis.com/auth/drive.file"
)

# Them 2 scope tren de dang bai (de/bai giai/diem) len "Bai tap tren lop"
# rieng cho tung hoc sinh sau khi lam bai online (xem
# dang_ket_qua_len_classroom o cuoi file). classroom.coursework.students:
# tao/xoa courseWorkMaterial. drive.file: tai PDF len Drive cua giao vien
# (app chi thay duoc file no tu tao ra, khong dong den file khac trong
# Drive that). LUU Y: doi scope nhu the nay thi PHAI vao lai Google Cloud
# Console > Data Access them 2 scope moi, ROI lam lai /gv/classroom/connect
# de xin refresh_token moi (refresh_token cu chi mang quyen cu).
DRIVE_API_UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"


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


# ======================================================
# DANG DE/BAI GIAI/DIEM LEN "BAI TAP TREN LOP" CUA CLASSROOM (rieng cho
# tung hoc sinh) - chay TU DONG ngay sau khi hoc sinh nop bai lam truc
# tiep tren web (xem app/routers/chat.py::dang_classroom_endpoint, goi
# tu app/templates/chat/lam_bai.html). Day la tien ich THEM, khong duoc
# phep lam gian doan/chan luong xem ket qua cua hoc sinh du Classroom co
# loi gi - moi ham deu tra ve {"success": bool, "message": str}, KHONG
# raise loi ra ngoai.
# ======================================================

def _html_sang_text(html: str) -> str:
    """Doi HTML don gian (cua xayHtmlTomTatKetQua ben lam_bai.html) sang
    text thuan, vi mo ta (description) cua courseWorkMaterial khong hien
    the HTML."""
    text = re.sub(r"<br\s*/?>", "\n", html or "")
    text = re.sub(r"</(div|p)>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )
    dong = [d.strip() for d in text.splitlines()]
    return "\n".join(d for d in dong if d)


def _tai_len_drive(access_token: str, duong_dan_file: str, ten_file: str):
    """Tai 1 file PDF len Google Drive cua giao vien (dung quyen drive.file
    - app CHI thay/quan ly duoc file no tu tao ra, khong dong den file
    khac trong Drive that cua giao vien). Tra ve file id hoac None neu loi."""
    metadata = {"name": ten_file, "mimeType": "application/pdf"}
    try:
        with open(duong_dan_file, "rb") as f:
            files = {
                "data": (None, json.dumps(metadata), "application/json; charset=UTF-8"),
                "file": (ten_file, f, "application/pdf"),
            }
            res = requests.post(
                f"{DRIVE_API_UPLOAD}?uploadType=multipart",
                headers={"Authorization": f"Bearer {access_token}"},
                files=files,
                timeout=60,
            )
        if res.status_code in (200, 201):
            return res.json().get("id")
        print("LOI TAI FILE LEN DRIVE:", res.status_code, res.text[:300])
    except Exception as e:
        print("LOI TAI FILE LEN DRIVE (exception):", e)
    return None


def _tao_coursework_material(access_token: str, course_id: str, title: str,
                              description: str, file_ids: list[str], student_email: str):
    """Tao 1 courseWorkMaterial (dang 'tai lieu', khong phai bai tap co
    han nop) tren dung course_id, CHI giao rieng cho 1 hoc sinh
    (individualStudentsOptions) - cac ban khac trong lop khong thay bai
    nay. Tra ve coursework id hoac None neu loi."""
    body = {
        "title": title,
        "description": description,
        "materials": [
            {"driveFile": {"driveFile": {"id": fid}, "shareMode": "VIEW"}}
            for fid in file_ids
        ],
        "state": "PUBLISHED",
        "assigneeMode": "INDIVIDUAL_STUDENTS",
        "individualStudentsOptions": {"studentIds": [student_email]},
    }
    try:
        res = requests.post(
            f"{CLASSROOM_API_BASE}/courses/{course_id}/courseWorkMaterials",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
            timeout=30,
        )
        if res.status_code in (200, 201):
            return res.json().get("id")
        print("LOI TAO COURSEWORK MATERIAL:", res.status_code, res.text[:300])
    except Exception as e:
        print("LOI TAO COURSEWORK MATERIAL (exception):", e)
    return None


def dang_ket_qua_len_classroom(de_id: str, student_email: str, khoi: str, lop: str,
                                diem_html: str, diem_so, diem_toi_da=None) -> dict:
    """
    Ham cap cao: goi tu app/routers/chat.py::dang_classroom_endpoint ngay
    sau khi hoc sinh nop bai lam truc tiep tren web. Tai file de (PDF) +
    loi giai (PDF, neu co) len Drive cua giao vien, dang 1 courseWorkMaterial
    RIENG cho dung hoc sinh do (khong ai khac trong lop thay duoc), tieu
    de dat theo ngay gio + ghi chu "Đề, bài giải, điểm". Ghi 1 dong vao
    bang classroom_coursework de scripts/cleanup_classroom_coursework.py
    biet duong ma xoa sau 10 ngay.
    """
    if not khoi or not lop:
        return {"success": False, "message": "Chưa xác định được lớp của học sinh."}

    course_id = MA_LOP_CLASSROOM.get((khoi, lop))
    if not course_id:
        return {"success": False, "message": f"Chưa có mã lớp Classroom cho {khoi}-{lop}."}

    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        return {"success": False, "message": "Không tìm thấy đề."}

    files = de.get("files", {}) or {}
    duong_dan_de = files.get("de")
    duong_dan_loigiai = files.get("loigiai")
    if not duong_dan_de or not Path(duong_dan_de).exists():
        return {"success": False, "message": "Không tìm thấy file đề để đăng lên Classroom."}

    refresh_token = lay_refresh_token()
    if not refresh_token:
        return {"success": False, "message": "Chưa kết nối Classroom (vào /gv/classroom/connect)."}

    try:
        access_token = lam_moi_access_token(refresh_token)
    except Exception as e:
        print("LOI LAM MOI ACCESS TOKEN (dang Classroom):", e)
        return {"success": False, "message": "Không làm mới được access token."}

    file_ids = []
    ma_de_ngan = str(de_id)[:8]

    fid_de = _tai_len_drive(access_token, duong_dan_de, f"De_{ma_de_ngan}.pdf")
    if fid_de:
        file_ids.append(fid_de)

    if duong_dan_loigiai and Path(duong_dan_loigiai).exists():
        fid_lg = _tai_len_drive(access_token, duong_dan_loigiai, f"BaiGiai_{ma_de_ngan}.pdf")
        if fid_lg:
            file_ids.append(fid_lg)

    if not file_ids:
        return {"success": False, "message": "Không tải được file lên Drive."}

    thoi_gian = datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y %H:%M")
    tieu_de = f"{thoi_gian} - Đề, bài giải, điểm"
    mo_ta = f"Điểm: {diem_so}/{diem_toi_da or 10}\n\n{_html_sang_text(diem_html)}"

    coursework_id = _tao_coursework_material(
        access_token, course_id, tieu_de, mo_ta, file_ids, student_email,
    )
    if not coursework_id:
        return {"success": False, "message": "Không tạo được bài đăng trên Classroom."}

    try:
        supabase.table("classroom_coursework").insert({
            "de_id": de_id,
            "student_email": student_email,
            "course_id": course_id,
            "coursework_id": coursework_id,
            "drive_file_ids": file_ids,
        }).execute()
    except Exception as e:
        print("LOI LUU CLASSROOM_COURSEWORK:", e)

    return {"success": True, "message": "Đã đăng lên Classroom."}


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
