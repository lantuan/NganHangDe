from pathlib import Path
import random
import uuid

from fastapi import APIRouter, Request, Form, HTTPException
from pydantic import BaseModel
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

# Cau dan vui nhon hien sau khi tao DE thanh cong (khong tinh AI token -
# random.choice thuan Python). "hoi lam truc tiep" (nut Co/Khong) se gan
# vao day sau khi trang lam bai truc tiep tren web xong (task rieng).
CAU_DAN_DE = [
    "Đề của em xong rồi nè! 📄",
    "Đề nóng hổi vừa ra lò! 🔥",
    "Xong đề rồi đó! ✨",
    "Đề đã sẵn sàng! 🎯",
    "Đề ra lò nóng hổi! 🍞",
    "Xong xuôi! Đề đây rồi. 🎉",
    "Đề đây rồi! Ting ting! 🔔",
    "Đề mới về, nóng hổi vừa thổi vừa ăn! 😄",
    "Đề xong! Nút tải đang chờ em nè. 📥",
    "Đề đã có! 🚀",
    "Xong rồi đó nha! 💪",
    "Đề mới toanh vừa in xong! 🖨️",
]

# Cau dan vui nhon hien sau khi xuat LOI GIAI thanh cong.
CAU_DAN_LOIGIAI = [
    "Lời giải nóng hổi đây, cầm lấy mà đối chiếu nha! 📖",
    "Đáp án ra lò rồi, xem thử làm đúng được mấy câu nào! 🎯",
    "Đây, lời giải chuẩn không cần chỉnh, ngó qua liền tay! ✅",
    "Xong! Đáp án đã sẵn sàng, đối chiếu xem mình \"cao thủ\" cỡ nào! 🏆",
    "Lời giải vừa in ra, thơm mùi mực, lấy liền kẻo nguội! 🖨️",
    "Đáp án đây rồi, tự chấm thử xem được bao nhiêu điểm nha! 📝",
    "Ting ting, lời giải đã về, mở ra dò đáp án liền! 🔔",
    "Đây, bí kíp đáp án đã trong tay, xem \"trúng tủ\" chưa nào! 😄",
]

_TU_KHOA_LOIGIAI = ("lời giải", "loi giai", "đáp án", "dap an", "giải")


def _la_yeu_cau_loi_giai(noi_dung_tin_nhan: str) -> bool:
    """Doan (khong can chinh xac tuyet doi, chi de chon dung bo cau vui
    nhon hien ra) xem tin nhan hoc sinh vua gui co phai xin loi giai hay
    khong, dua vao chinh tin nhan da co san trong FastAPI (khong can sua
    gi ben n8n)."""
    text = (noi_dung_tin_nhan or "").lower()
    return any(tu in text for tu in _TU_KHOA_LOIGIAI)

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


@router.get("/lam-bai/{de_id}", response_class=HTMLResponse)
async def lam_bai_page(request: Request, de_id: str):
    """Trang lam bai truc tiep (MC/TF/SA) - JS trong template tu goi
    GET /api/exam/quiz/{de_id} de lay cau hoi (an dap an) va POST
    /api/exam/grade de nop bai + cham diem. Khong tu doc de_id o day,
    de_id khong hop le/het han se bao loi ngay trong trang (fetch that
    bai) thay vi chan o server."""
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    metadata = user.user_metadata or {}
    ten_hien_thi = (
        metadata.get("fullname")
        or metadata.get("full_name")
        or metadata.get("name")
        or user.email
    )

    return templates.TemplateResponse(
        request=request,
        name="chat/lam_bai.html",
        context={
            "de_id": de_id,
            "user_id": user.id,
            "user_display_name": ten_hien_thi,
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


class LuuDeTrucTiepRequest(BaseModel):
    conversation_id: str
    user_message: str
    ai_caption: str


@router.post("/api/chat/luu-de-truc-tiep")
async def luu_de_truc_tiep_endpoint(request: Request, payload: LuuDeTrucTiepRequest):
    """Luu lai 1 cap tin nhan user/assistant vao chat_history cho cac luong
    tao de KHONG di qua CHV_Fun/n8n (nut "Dong y tao de" o luong xac nhan
    cau truc, va form "Tao de nhanh") - vi cac luong nay goi thang
    /api/exam/generate-pdf-auto tu trinh duyet nen truoc day khong duoc
    ghi lai, lam mat noi dung trao doi khi quay lai hoi thoai."""
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Ban chua dang nhap hoac phien da het han.")
    history_service.luu_tin_nhan(
        user_id=user.id,
        conversation_id=payload.conversation_id,
        role="user",
        noi_dung=payload.user_message,
    )
    history_service.luu_tin_nhan(
        user_id=user.id,
        conversation_id=payload.conversation_id,
        role="assistant",
        noi_dung=payload.ai_caption,
    )
    return {"success": True}


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
            "message": "Bạn chưa đăng nhập hoặc phiên đã hết hạn. Vui lòng đăng nhập lại.",
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
        loi = "Không kết nối được với AI sau 2 lần thử, vui lòng thử lại."
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
                "message": "AI chưa xử lý được yêu cầu này. Vui lòng thử lại với yêu cầu tạo đề cụ thể (lớp/chương/số câu...).",
                "data": None,
            }

        history_service.luu_tin_nhan(
            user_id=user.id, conversation_id=conversation_id,
            role="assistant",
            noi_dung=ket_qua.get("message") or ket_qua.get("reply"),
            loai_phan_hoi="text" if ket_qua.get("success", True) else "error",
        )
        return ket_qua

    # n8n tra file nhi phan (PDF/TEX/ZIP tu /api/exam/generate-pdf-auto
    # hoac /api/exam/export-loigiai)
    if content_type in _EXT_THEO_CONTENT_TYPE:
        ext = _EXT_THEO_CONTENT_TYPE[content_type]
        filename = f"{uuid.uuid4().hex[:10]}.{ext}"
        file_path = DOWNLOAD_DIR / filename
        file_path.write_bytes(r.content)
        file_url = f"/static/downloads/{filename}"

        de_id_de_hoi = None
        if _la_yeu_cau_loi_giai(message):
            cau_dan = random.choice(CAU_DAN_LOIGIAI)
        else:
            cau_dan = random.choice(CAU_DAN_DE)
            # Chi hoi "lam bai truc tiep" (nut Co/Khong, xu ly hoan toan
            # o chat.html bang JS) cho DE, khong hoi cho loi giai. Neu
            # chua tim thay de_id (VD Supabase loi) thi bo qua, nut se
            # khong hien ra - khong chan viec tra PDF cho hoc sinh.
            de_vua_sinh = history_service.lay_de_gan_nhat(conversation_id)
            if de_vua_sinh and de_vua_sinh.get("id"):
                de_id_de_hoi = de_vua_sinh["id"]

        history_service.luu_tin_nhan(
            user_id=user.id, conversation_id=conversation_id,
            role="assistant", noi_dung=cau_dan,
            loai_phan_hoi="file", duong_dan_file=file_url,
        )

        return {
            "success": True,
            "message": cau_dan,
            "data": {
                "type": "file",
                "url": file_url,
                "filename": filename,
                "de_id": de_id_de_hoi,
            },
        }

    # Truong hop la khac (n8n loi, tra HTML/text...) - khong de 500 lang le
    print("LOI CHAT: content-type khong xac dinh ->", content_type)
    print(r.text[:1000])
    loi = "Không hiểu phản hồi từ n8n."
    history_service.luu_tin_nhan(
        user_id=user.id, conversation_id=conversation_id,
        role="assistant", noi_dung=loi, loai_phan_hoi="error",
    )
    return {"success": False, "message": loi, "data": None}
