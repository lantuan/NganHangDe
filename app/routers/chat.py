from pathlib import Path
import uuid

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
import requests

from app.core.deps import get_current_user
from app.core.lop_config import DANH_SACH_LOP
from app.services import history_service
from app.services import supabase_service
from app.services import classroom_service

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

N8N_WEBHOOK_URL = "https://fqrpl.n8npanel.com/webhook/chat"

# Noi luu file (PDF/TEX/ZIP) do n8n tra ve, de Frontend tai qua /static
DOWNLOAD_DIR = Path("app/static/downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

_EXT_THEO_CONTENT_TYPE = {
    "application/pdf": "pdf",
    "application/zip": "zip",
    "application/x-tex": "tex",
}


@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    ho_so = supabase_service.lay_lop_hoc_sinh(user.id)
    if not ho_so or not ho_so.get("lop"):
        # Thu tu dong ghep lop bang email da dong bo tu Google Classroom
        # (xem app/services/classroom_service.py) truoc khi bat hoc sinh
        # tu chon o /chon-lop. Khong tim thay (chua dong bo, hoac email
        # dang nhap khac email tren Classroom) thi roi ve /chon-lop nhu cu.
        khop = classroom_service.tim_lop_theo_email(user.email)
        if khop:
            supabase_service.cap_nhat_lop_hoc_sinh(user.id, khop["khoi"], khop["lop"])
            ho_so = khop
        else:
            return RedirectResponse("/chon-lop", status_code=303)

    metadata = user.user_metadata or {}
    ten_hien_thi = (
        metadata.get("fullname")
        or metadata.get("full_name")
        or metadata.get("name")
        or user.email
    )

    return templates.TemplateResponse(
        request=request,
        name="chat/chat.html",
        context={
            "title": "Chat AI",
            "user_email": user.email,
            "user_display_name": ten_hien_thi,
            "user_khoi": ho_so.get("khoi"),
            "user_lop": ho_so.get("lop"),
        },
    )


@router.get("/chon-lop", response_class=HTMLResponse)
async def chon_lop_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="chat/chon_lop.html",
        context={
            "danh_sach_lop": DANH_SACH_LOP,
        },
    )


@router.post("/chon-lop")
async def chon_lop_submit(request: Request, lop_full: str = Form(...)):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    if "-" not in lop_full:
        return RedirectResponse("/chon-lop", status_code=303)

    khoi, lop = lop_full.split("-", 1)
    if khoi not in DANH_SACH_LOP or lop not in DANH_SACH_LOP[khoi]:
        return RedirectResponse("/chon-lop", status_code=303)

    supabase_service.cap_nhat_lop_hoc_sinh(user.id, khoi, lop)
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
    )


@router.get("/api/chat/history")
async def lay_lich_su_chat(request: Request):
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Chua dang nhap")
    danh_sach = history_service.lay_danh_sach_hoi_thoai(user.id)
    return {"success": True, "data": danh_sach}


@router.get("/api/chat/history/{conversation_id}")
async def lay_tin_nhan(request: Request, conversation_id: str):
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Chua dang nhap")
    tin_nhan = history_service.lay_tin_nhan_hoi_thoai(user.id, conversation_id)
    return {"success": True, "data": tin_nhan}


def _goi_n8n(message: str, user_id: str, conversation_id: str):
    """Ham dong bo (blocking) - se duoc chay trong threadpool rieng,
    khong chan event loop chinh cua uvicorn trong luc cho n8n xu ly lau."""
    return requests.post(
        N8N_WEBHOOK_URL,
        json={
            "message": message,
            "user_id": user_id,
            "conversation_id": conversation_id,
        },
        timeout=300,
    )


@router.post("/chat")
async def chat_post(
    request: Request,
    message: str = Form(...),
    conversation_id: str = Form(...),
):
    user = get_current_user(request)
    if user is None:
        return {
            "success": False,
            "message": "Ban chua dang nhap hoac phien da het han. Vui long dang nhap lai.",
            "data": None,
            "need_login": True,
        }

    print("========== CHAT ==========")
    print(message)
    print("==========================")

    history_service.luu_tin_nhan(
        user_id=user.id,
        conversation_id=conversation_id,
        role="user",
        noi_dung=message,
    )

    r = None
    loi_cuoi = None
    for lan_thu in range(2):
        try:
            r = await run_in_threadpool(_goi_n8n, message, user.id, conversation_id)
            break
        except requests.exceptions.Timeout as e:
            loi_cuoi = e
            print(f"LOI CHAT: n8n qua thoi gian cho (lan {lan_thu + 1}/2)")
        except requests.exceptions.RequestException as e:
            loi_cuoi = e
            print(f"LOI CHAT: khong ket noi duoc n8n (lan {lan_thu + 1}/2) ->", e)

    if r is None:
        loi = "Khong ket noi duoc voi AI sau 2 lan thu, vui long thu lai."
        history_service.luu_tin_nhan(
            user_id=user.id, conversation_id=conversation_id,
            role="assistant", noi_dung=loi, loai_phan_hoi="error",
        )
        return {"success": False, "message": loi, "data": None}

    print(r.status_code)

    content_type = r.headers.get("content-type", "").split(";")[0].strip()

    # n8n tra JSON binh thuong (cau tra loi chat thuong, khong sinh de)
    if content_type == "application/json":
        try:
            ket_qua = r.json()
        except ValueError:
            print("LOI CHAT: n8n tra ve JSON rong/khong hop le. Body:", repr(r.text[:500]))
            ket_qua = {
                "success": False,
                "message": "AI chua xu ly duoc yeu cau nay. Vui long thu lai voi yeu cau tao de cu the (lop/chuong/so cau...).",
                "data": None,
            }

        history_service.luu_tin_nhan(
            user_id=user.id, conversation_id=conversation_id,
            role="assistant",
            noi_dung=ket_qua.get("message") or ket_qua.get("reply"),
            loai_phan_hoi="text" if ket_qua.get("success", True) else "error",
        )
        return ket_qua

    # n8n tra file nhi phan (PDF/TEX/ZIP tu /api/exam/generate-pdf-auto)
    if content_type in _EXT_THEO_CONTENT_TYPE:
        ext = _EXT_THEO_CONTENT_TYPE[content_type]
        filename = f"{uuid.uuid4().hex[:10]}.{ext}"
        file_path = DOWNLOAD_DIR / filename
        file_path.write_bytes(r.content)
        file_url = f"/static/downloads/{filename}"

        history_service.luu_tin_nhan(
            user_id=user.id, conversation_id=conversation_id,
            role="assistant", noi_dung="Da tao de xong.",
            loai_phan_hoi="file", duong_dan_file=file_url,
        )

        return {
            "success": True,
            "message": "Da tao de xong.",
            "data": {
                "type": "file",
                "url": file_url,
                "filename": filename,
            },
        }

    # Truong hop la khac (n8n loi, tra HTML/text...) - khong de 500 lang le
    print("LOI CHAT: content-type khong xac dinh ->", content_type)
    print(r.text[:1000])
    loi = "Khong hieu phan hoi tu n8n."
    history_service.luu_tin_nhan(
        user_id=user.id, conversation_id=conversation_id,
        role="assistant", noi_dung=loi, loai_phan_hoi="error",
    )
    return {"success": False, "message": loi, "data": None}
