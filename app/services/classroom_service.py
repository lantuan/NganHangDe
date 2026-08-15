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

# Chi can quyen doc danh sach lop + quyen xem email (Google an email hoc
# sinh mac dinh, phai xin rieng scope profile.emails moi thay duoc).
SCOPES = (
    "https://www.googleapis.com/auth/classroom.rosters.readonly "
    "https://www.googleapis.com/auth/classroom.profile.emails"
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
