from pathlib import Path
import random
import re
import uuid

from fastapi import APIRouter, Request, Form, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
import requests

from app.core.deps import get_current_user
from app.services.i18n_service import lay_ngon_ngu
from app.core.lop_config import DANH_SACH_LOP
from app.services import history_service, profile_service, tuy_chon_de_service
from app.services import gia_su_service
from app.services import supabase_service
from app.services import classroom_service
from app.services import yeu_cau_de_service
from app.services import tro_chuyen_service

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


def _la_tep_loi_giai_de_gan_nhat(noi_dung: bytes, conversation_id: str) -> bool:
    """Tệp n8n vừa trả có phải chính tệp LỜI GIẢI (PDF) của đề gần nhất trong hội thoại không (so từng byte).
    Lỗi gì cũng coi là không (chỉ dùng để chọn câu chào cho đúng)."""
    try:
        de = history_service.lay_de_gan_nhat(conversation_id) or {}
        p = Path((de.get("files") or {}).get("loigiai") or "")
        return bool(noi_dung) and p.is_file() and p.stat().st_size == len(noi_dung) and p.read_bytes() == noi_dung
    except Exception:
        return False


def dong_tuy_chon_da_ap_dung(thong_tin: dict, da_tick_anh: bool, lang: str = "vi") -> str:
    """Một câu ngắn: đề vừa tạo theo mức nào, có bản Anh không (thong_tin = exam.thong_tin_tai_de)."""
    en = lang == "en"
    if thong_tin.get("chi_yccd"):
        muc = "Level: 📘 Standard curriculum." if en else "Mức: 📘 Đúng chương trình."
    else:
        muc = "Level: 🚀 Extra challenge." if en else "Mức: 🚀 Nâng cao thêm."
    if thong_tin.get("co_ban_tieng_anh"):
        anh = (" English version included: the download is a .zip with both the Vietnamese and English files."
               if en else " Có kèm bản tiếng Anh: tải về là tệp .zip gồm cả bản Việt và bản Anh.")
    elif da_tick_anh:
        anh = (" This chapter has no English version yet, so only the Vietnamese file is available."
               if en else " Chương này chưa có bản tiếng Anh nên chỉ có bản Việt.")
    else:
        anh = ""
    return muc + anh


def lop_trong_ho_so(user_id: str) -> int | None:
    """Khối 10/11/12 học sinh đã chọn (profiles.khoi). Giáo viên / chưa chọn / lỗi -> None."""
    try:
        khoi = (supabase_service.lay_lop_hoc_sinh(user_id) or {}).get("khoi")
        m = re.search(r"\d+", str(khoi or ""))
        so = int(m.group(0)) if m else None
        return so if so in (10, 11, 12) else None
    except Exception:
        return None


def _du_phong_tao_de(request, message: str, user_id: str, conversation_id: str,
                     vai_tro: str | None = None) -> dict | None:
    """n8n hỏng (JSON rỗng/hỏng, không kết nối, phản hồi lạ): máy chủ tự trả lời những gì đọc chắc được, thay vì "AI chưa
    xử lý được" (cô Lan 22-23/10/2026):
      - yêu cầu tạo đề rõ ràng (kỳ thi hoặc chương; lớp lấy trong tin nhắn, không có thì lấy hồ sơ; "phần tự luận",
        "5 câu trắc nghiệm"...) -> khung xác nhận như RequestParser;
      - hỏi cách dùng ("tôi không biết cách tạo đề") -> hướng dẫn soạn sẵn.
    Không đọc được -> None (nơi gọi báo lỗi như cũ). Xem app/services/yeu_cau_de_service.py."""
    lang = lay_ngon_ngu(request)
    de_xuat = yeu_cau_de_service.doc_yeu_cau_de(message, lang, lop_trong_ho_so(user_id))
    if de_xuat:
        print("CHAT: n8n hong, may chu tu doc yeu cau tao de ->", de_xuat["lop"], de_xuat["ki_thi"],
              de_xuat["pham_vi_chuong"], de_xuat["cau_truc_tong_quat"])
        history_service.luu_tin_nhan(user_id=user_id, conversation_id=conversation_id, role="assistant",
                                     noi_dung=de_xuat["tra_loi"], loai_phan_hoi="text")
        return {"success": True, "message": de_xuat["tra_loi"], "data": de_xuat}
    huong_dan = yeu_cau_de_service.tra_loi_cach_dung(message, lang)
    if huong_dan:
        print("CHAT: n8n hong, may chu tra loi huong dan su dung")
        history_service.luu_tin_nhan(user_id=user_id, conversation_id=conversation_id, role="assistant",
                                     noi_dung=huong_dan, loai_phan_hoi="text")
        return {"success": True, "message": huong_dan, "data": {"type": "huong_dan"}}
    # Còn lại (trò chuyện, chuyện ngoài lề): trả lời tự nhiên qua webhook gia sư (cô Lan 23/10/2026: "tôi cần chat được
    # bình thường như chatbox bình thường khác"), thay vì câu báo lỗi.
    tra_loi = tro_chuyen_service.tro_chuyen(message, _lich_su_gan(user_id, conversation_id), lang, vai_tro)
    if tra_loi:
        print("CHAT: n8n hong, tra loi tro chuyen qua webhook gia su")
        history_service.luu_tin_nhan(user_id=user_id, conversation_id=conversation_id, role="assistant",
                                     noi_dung=tra_loi, loai_phan_hoi="text")
        _tru_luot(user_id, vai_tro)
        return {"success": True, "message": tra_loi, "data": {"type": "tro_chuyen"}}
    return None


def _mien_luot(vai_tro: str | None) -> bool:
    """Giáo viên / quản trị không giới hạn lượt hỏi AI."""
    return vai_tro in profile_service.VAI_TRO_GIAO_VIEN


def _het_luot(request, user_id: str, vai_tro: str | None, conversation_id: str) -> dict | None:
    """Học sinh hết lượt hỏi AI hôm nay (cô Lan 23/10/2026: "mỗi ngày hỏi 30 lượt cả đề và chatbox ngoài" - tính CHUNG
    với thầy/cô AI, bảng gia_su_luot) -> câu báo (không gọi mô hình). Còn lượt / giáo viên -> None."""
    if _mien_luot(vai_tro):
        return None
    luot = gia_su_service.lay_luot(user_id)
    if luot["con_lai"] > 0:
        return None
    if lay_ngon_ngu(request) == "en":
        loi = ("You have used all %d AI questions for today 😅 (shared between this chat and asking the AI teacher about "
               "exam questions). You can still create exams with **📝 Create a new exam** and take them as usual - "
               "that does not use any questions. See you tomorrow!" % luot["gioi_han"])
    else:
        loi = ("Hôm nay bạn đã dùng hết %d lượt hỏi AI rồi 😅 (tính chung cả khung chat và hỏi thầy/cô AI về câu "
               "trong đề). Bạn vẫn tạo đề bằng nút **📝 Tạo đề mới** và làm bài bình thường - phần đó không tính lượt. "
               "Mai mình gặp lại nha!" % luot["gioi_han"])
    history_service.luu_tin_nhan(user_id=user_id, conversation_id=conversation_id, role="assistant", noi_dung=loi,
                                 loai_phan_hoi="text")
    return {"success": True, "message": loi, "data": {"type": "het_luot", "luot": luot}}


def _tru_luot(user_id: str, vai_tro: str | None) -> None:
    """Trừ 1 lượt SAU khi mô hình đã trả lời (lỗi mạng / n8n hỏng không mất lượt). Giáo viên không trừ."""
    if not _mien_luot(vai_tro):
        gia_su_service.tru_luot(user_id)


def _lich_su_gan(user_id: str, conversation_id: str) -> list[tuple[str, str]]:
    """Vài tin nhắn gần nhất (bỏ tin nhắn vừa gửi - đã lưu trước khi gọi n8n) để trả lời trò chuyện có ngữ cảnh."""
    try:
        ds = history_service.lay_tin_nhan_hoi_thoai(user_id, conversation_id) or []
    except Exception:
        return []
    ra = [(m.get("role"), "[giảng bài]" if m.get("loai_phan_hoi") == "gia_su" else (m.get("noi_dung") or ""))
          for m in ds[:-1]]
    return ra[-4:]


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

    # Tai khoan moi (nhat la dang nhap bang Google - khong di qua trang
    # dang ky nen chua he duoc hoi) phai chon vai tro TRUOC. Neu bo qua
    # buoc nay thi giao vien bi hoi "chon lop cua em" ma khong hieu tai sao.
    vai_tro = profile_service.lay_vai_tro(user.id)
    if vai_tro == profile_service.VAI_TRO_CHUA_CHON:
        return RedirectResponse("/chon-vai-tro", status_code=303)

    # Giao vien KHONG co "lop cua minh" theo nghia hoc sinh - ho day nhieu
    # lop. Truoc day doan duoi day bat moi nguoi phai co lop moi vao duoc
    # chat, nen giao vien bam "Chat AI" lai bi hoi "Chon lop cua em".
    # Lay ma lop de phat cho hoc sinh la viec khac, nam o /gv/lop.
    la_giao_vien = vai_tro in profile_service.VAI_TRO_GIAO_VIEN

    ho_so = supabase_service.lay_lop_hoc_sinh(user.id) or {}
    if not la_giao_vien and not ho_so.get("lop"):
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
            "user_id": user.id,
            "user_email": user.email,
            "user_display_name": ten_hien_thi,
            "user_khoi": ho_so.get("khoi"),
            "user_lop": ho_so.get("lop"),
            "la_giao_vien": la_giao_vien,
        },
    )


@router.get("/chon-lop", response_class=HTMLResponse)
async def chon_lop_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    vai_tro = profile_service.lay_vai_tro(user.id)
    if vai_tro == profile_service.VAI_TRO_CHUA_CHON:
        return RedirectResponse("/chon-vai-tro", status_code=303)
    # Giao vien vao nham trang chon lop -> day ve khu lam viec.
    if vai_tro in profile_service.VAI_TRO_GIAO_VIEN:
        return RedirectResponse("/gv", status_code=303)

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


def _goi_n8n(message: str, user_id: str, conversation_id: str,
             vai_tro: str = "hoc_sinh"):
    """Ham dong bo (blocking) - se duoc chay trong threadpool rieng,
    khong chan event loop chinh cua uvicorn trong luc cho n8n xu ly lau.

    Gui kem vai_tro de CHV_Fun xung ho cho dung ("em" voi hoc sinh,
    "thay/co" voi giao vien) va hieu duoc cac yeu cau rieng cua giao vien
    (vi du "cho 4 ma de"). LUU Y: viec QUYET DINH xuat de kem loi giai
    hay khong KHONG phu thuoc truong nay - no do may chu tra bang
    profiles.vai_tro o /api/exam/generate-pdf-auto. Truong nay chi de AI
    noi nang cho dung.
    """
    return requests.post(
        N8N_WEBHOOK_URL,
        json={
            "message": message,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "vai_tro": vai_tro,
        },
        timeout=300,
    )


class LuuDeTrucTiepRequest(BaseModel):
    conversation_id: str
    user_message: str
    ai_caption: str
    # Tuy chon: URL on dinh (/api/exam/tai-de/{de_id}) cho de vua tao qua
    # luong xac nhan cau truc / form tao de nhanh. Khi co gia tri nay,
    # luu tin nhan AI o dang "file" (giong het luong chat binh thuong qua
    # n8n) de moHoiThoai() tu dong ve lai duoc link tai file + nut "Lam
    # bai truc tiep" khi quay lai hoi thoai - truoc day luu dang van ban
    # thuong nen link/nut bi mat het sau khi tai lai trang.
    file_url: str | None = None


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
        loai_phan_hoi="file" if payload.file_url else None,
        duong_dan_file=payload.file_url,
    )
    return {"success": True}


class DangClassroomRequest(BaseModel):
    de_id: str
    diem_html: str
    diem_so: float
    # Diem toi da cua lan cham nay. Chua chac bang 10: phan tu luan (3d)
    # dang xay dung nen bai lam tren web hien toi da 7d (MC 3 + TF 2 + SA 2).
    diem_toi_da: float | None = None


@router.post("/api/chat/dang-classroom")
async def dang_classroom_endpoint(request: Request, payload: DangClassroomRequest):
    """Dang de + loi giai + diem cua 1 lan lam bai truc tiep tren web len
    "Bai tap tren lop" cua Classroom, rieng cho dung hoc sinh do (khong ai
    khac trong lop thay duoc). Goi TU DONG tu lam_bai.html ngay sau khi
    nop bai (task hoc sinh yeu cau). Tien ich them - KHONG duoc raise loi
    lam gian doan trang xem ket qua, luon tra ve {"success":...}."""
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Ban chua dang nhap hoac phien da het han.")

    ho_so = supabase_service.lay_lop_hoc_sinh(user.id) or {}
    la_gv = profile_service.la_giao_vien(user.id)
    ket_qua = classroom_service.dang_ket_qua_len_classroom(
        de_id=payload.de_id,
        student_email=user.email,
        khoi=ho_so.get("khoi"),
        lop=ho_so.get("lop"),
        diem_html=payload.diem_html,
        diem_so=payload.diem_so,
        diem_toi_da=payload.diem_toi_da,
    )
    # Cô Lan 22/10/2026 "ra đáp án chưa đẩy lên được class": trước đây lí do thất bại chỉ ghi console trình duyệt.
    # Nay ghi log máy chủ, và trả kèm la_giao_vien để trang làm bài HIỆN lí do cho giáo viên (học sinh vẫn chỉ thấy
    # câu nhẹ nhàng). Tài khoản giáo viên không phải học sinh trong lớp Classroom nên không giao bài riêng được.
    if not ket_qua.get("success"):
        print("DANG CLASSROOM THAT BAI:", user.email, ho_so.get("khoi"), ho_so.get("lop"), ket_qua.get("message"))
    return {**ket_qua, "la_giao_vien": bool(la_gv)}


@router.post("/chat")
async def chat_post(
    request: Request,
    message: str = Form(...),
    conversation_id: str = Form(...),
    kem_tieng_anh: str | None = Form(default=None),
    chi_yccd: str | None = Form(default=None),
):
    user = get_current_user(request)
    if user is None:
        return {
            "success": False,
            "message": "Bạn chưa đăng nhập hoặc phiên đã hết hạn. Vui lòng đăng nhập lại.",
            "data": None,
            "need_login": True,
        }

    vai_tro = profile_service.lay_vai_tro(user.id)

    # Ô tick "Kèm bản tiếng Anh": n8n tự gọi /generate-pdf-auto nên không nhận được ô tick này; ghi lại theo
    # hội thoại để /generate-pdf-auto tra lại (n8n không phải sửa gì). Không tick -> chỉ sinh bản Việt.
    tuy_chon_de_service.dat_kem_tieng_anh(conversation_id, kem_tieng_anh == "1")
    # Nút "Đúng chương trình" (chi_yccd=1) / "Nâng cao thêm" (0): ghi theo hội thoại như trên. Lời gọi cũ không gửi
    # trường này thì không ghi gì (giữ như trước: có cả dạng luyện tập thêm).
    if chi_yccd in ("0", "1"):
        tuy_chon_de_service.dat_chi_yccd(conversation_id, chi_yccd == "1")

    print("========== CHAT ==========")
    print(f"[{vai_tro}] {message}")
    print("==========================")

    history_service.luu_tin_nhan(
        user_id=user.id,
        conversation_id=conversation_id,
        role="user",
        noi_dung=message,
    )

    # ======================================================
    # BAT Y DINH "HOI BAI" TRUOC KHI GOI n8n (v2.62)
    # ======================================================
    # Hoc sinh vua nop bai xong, go "toi khong hieu bai 1". CHV_Fun khong
    # co cach nao biet hoi thoai nay da co de - no chi doc moi cau chu -
    # nen tu choi va bao em ay di TAO DE, trong khi em ay vua lam xong.
    # May chu thi biet chac, nen chan ngay o day: khong goi n8n, khong ton
    # mot luot goi mo hinh nao. CO Y KHONG DOAN SO CAU - chi mo bang chon
    # cau de chinh em ay chi dung cau minh can (xem gia_su_service).
    # Cô Lan 22/10/2026 ("hỏi về toán nhưng không biết toán"): nhận RỘNG hơn (la_cau_hoi_toan: nhắc số câu, từ ngữ
    # toán học...) và không bắt buộc đã nộp bài mới chặn - hội thoại có đề thì mở bảng chọn câu (bảng tự nhắc "chưa nộp
    # bài" nếu chưa làm); chưa có đề thì nói rõ phần hỏi bài hoạt động thế nào, KHÔNG đẩy xuống CHV_Fun để bị từ chối.
    # Câu học sinh vừa gõ đi kèm (cau_hoi_goc): bấm câu nào thì gửi chính câu đó cho thầy/cô AI.
    # Cô Lan 23/10/2026: hỏi KIẾN THỨC Toán ("tập rỗng là gì", "phương sai là gì", "định lý sin") -> AI trả lời CHỈ
    # theo tài liệu lí thuyết có sẵn của cô (tro_chuyen_service.tra_loi_kien_thuc, qua webhook gia sư; không thấy đoạn
    # tài liệu nào thì đi tiếp đường cũ). Lưu như gói gia sư để mở lại hội thoại vẫn có khung tài liệu.
    if tro_chuyen_service.la_cau_hoi_kien_thuc(message):
        het = await run_in_threadpool(_het_luot, request, user.id, vai_tro, conversation_id)
        if het:
            return het
        kt = await run_in_threadpool(
            lambda: tro_chuyen_service.tra_loi_kien_thuc(message, lop_trong_ho_so(user.id), lay_ngon_ngu(request),
                                                         vai_tro))
        if kt:
            await run_in_threadpool(_tru_luot, user.id, vai_tro)
            import json as _json
            goi = {"success": True, "message": "", "data": {"tra_loi": kt["tra_loi"], "ly_thuyet": kt["ly_thuyet"],
                                                            "che_do": "kien_thuc"}}
            history_service.luu_tin_nhan(user_id=user.id, conversation_id=conversation_id, role="assistant",
                                         noi_dung=_json.dumps(goi, ensure_ascii=False), loai_phan_hoi="gia_su")
            return {"success": True, "message": kt["tra_loi"],
                    "data": {"type": "kien_thuc", "tra_loi": kt["tra_loi"], "ly_thuyet": kt["ly_thuyet"]}}

    if gia_su_service.la_cau_hoi_toan(message):
        en = lay_ngon_ngu(request) == "en"
        de_gan = await run_in_threadpool(history_service.lay_de_gan_nhat, conversation_id)
        if de_gan is None:
            loi_nhan = (
                "The AI teacher explains questions from an exam you have taken, using the official worked solution "
                "from the question bank (it does not solve new problems on its own, to avoid wrong explanations). "
                "Create an exam, take it on the web and submit, then click the question you want to ask "
                "about. Every answer has its own box for follow-up questions."
                if en else
                "Thầy/cô AI giảng bài theo đề bạn đã làm, dựa trên lời giải chuẩn của ngân hàng đề (không tự giải "
                "bài mới để tránh giảng sai). Bạn tạo đề, làm bài trên web và nộp, rồi bấm vào câu muốn hỏi. "
                "Mỗi câu trả lời đều có ô để hỏi tiếp ngay bên dưới."
            )
            history_service.luu_tin_nhan(user_id=user.id, conversation_id=conversation_id,
                                         role="assistant", noi_dung=loi_nhan)
            return {"success": True, "message": loi_nhan, "data": {"type": "huong_dan_hoi_bai"}}
        da_nop = await run_in_threadpool(gia_su_service.co_de_da_nop_bai, user.id, conversation_id)
        # Trang đang ở tiếng Anh thì trả cả câu tiếng Anh (trước đây bộ dịch theo cụm từ dịch nửa câu, ra
        # "Bạn muốn ask about the lesson trong đề vừa làm correct không?" - cô Lan 22/10/2026).
        if da_nop:
            loi_nhan = (
                "Which question of the exam you just took is this about? Click it below, "
                "and the AI teacher will answer right away."
                if en else
                "Bạn hỏi về câu nào trong đề vừa làm? Bấm vào câu đó bên dưới, "
                "thầy/cô AI trả lời ngay nhé."
            )
        else:
            loi_nhan = (
                "You have not submitted the latest exam yet. Take it on the web and submit, then click the "
                "question you want to ask about below."
                if en else
                "Bạn chưa nộp bài đề gần nhất. Làm bài trên web và nộp, rồi bấm vào câu muốn hỏi ở bảng bên dưới nhé."
            )
        history_service.luu_tin_nhan(
            user_id=user.id, conversation_id=conversation_id,
            role="assistant", noi_dung=loi_nhan,
        )
        return {
            "success": True,
            "message": loi_nhan,
            "data": {"type": "mo_bang_gia_su", "tra_loi": loi_nhan, "cau_hoi_goc": message},
        }

    # Hết lượt hỏi AI hôm nay -> không gọi n8n (các câu máy chủ tự xử lí ở trên vẫn chạy, không tính lượt)
    het = await run_in_threadpool(_het_luot, request, user.id, vai_tro, conversation_id)
    if het:
        return het

    r = None
    loi_cuoi = None
    for lan_thu in range(2):
        try:
            r = await run_in_threadpool(
                _goi_n8n, message, user.id, conversation_id, vai_tro)
            break
        except requests.exceptions.Timeout as e:
            loi_cuoi = e
            print(f"LOI CHAT: n8n qua thoi gian cho (lan {lan_thu + 1}/2)")
        except requests.exceptions.RequestException as e:
            loi_cuoi = e
            print(f"LOI CHAT: khong ket noi duoc n8n (lan {lan_thu + 1}/2) ->", e)

    if r is None:
        du_phong = await run_in_threadpool(_du_phong_tao_de, request, message, user.id, conversation_id, vai_tro)
        if du_phong:
            return du_phong
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
            if isinstance(ket_qua, dict) and ket_qua:
                await run_in_threadpool(_tru_luot, user.id, vai_tro)       # mô hình đã trả lời -> tính 1 lượt
        except ValueError:
            print("LOI CHAT: n8n tra ve JSON rong/khong hop le. Body:", repr(r.text[:500]))
            ket_qua = None
        # n8n hỏng (JSON rỗng/hỏng) mà tin nhắn là yêu cầu tạo đề rõ ràng (lớp + kỳ thi, hoặc lớp + chương): máy chủ tự
        # đọc rồi hiện khung xác nhận như RequestParser (cô Lan 22/10/2026: "Lớp 10, thi giữa kỳ 1" báo "AI chưa xử lý
        # được"). Xem app/services/yeu_cau_de_service.py.
        if not isinstance(ket_qua, dict) or not ket_qua:
            du_phong = await run_in_threadpool(_du_phong_tao_de, request, message, user.id, conversation_id, vai_tro)
            if du_phong:
                return du_phong
            ket_qua = {
                "success": False,
                "message": "AI chưa xử lý được yêu cầu này. Vui lòng thử lại với yêu cầu tạo đề cụ thể (lớp/chương/số câu...). Nếu bạn đang muốn hỏi bài: hãy làm một đề rồi bấm \"Hỏi thầy/cô AI về câu này\" ở câu chưa hiểu.",
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
        await run_in_threadpool(_tru_luot, user.id, vai_tro)               # tạo đề / lời giải qua n8n -> 1 lượt
        ext = _EXT_THEO_CONTENT_TYPE[content_type]
        filename = f"{uuid.uuid4().hex[:10]}.{ext}"
        file_path = DOWNLOAD_DIR / filename
        file_path.write_bytes(r.content)
        file_url = f"/static/downloads/{filename}"

        de_id_de_hoi = None
        # Cô Lan 22/10/2026: "có lúc xuất đề ra cả lời giải" - CHV_Fun hiểu nhầm yêu cầu tạo đề thành "tải lời
        # giải" thì n8n trả về LỜI GIẢI của đề gần nhất, mà trước đây máy chủ vẫn chào "Xong đề rồi đó!" và hiện nút
        # "Làm bài trực tiếp". Nay so nội dung tệp với tệp lời giải của đề gần nhất: trùng thì nói rõ đây là lời giải.
        tep_la_loi_giai = _la_tep_loi_giai_de_gan_nhat(r.content, conversation_id)
        if tep_la_loi_giai and not _la_yeu_cau_loi_giai(message):
            cau_dan = ("Đây là LỜI GIẢI của đề gần nhất (mình đã hiểu yêu cầu của bạn là xin lời giải). "
                       "Nếu bạn muốn một đề mới, bấm 📝 Tạo đề mới nhé.")
            print("CANH BAO CHAT: n8n tra LOI GIAI cho tin nhan khong xin loi giai:", message[:200])
        elif tep_la_loi_giai or _la_yeu_cau_loi_giai(message):
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

        # Cô Lan 22/10/2026: "chọn có tiếng Anh nhưng chỉ xuất ra tiếng Việt". n8n chỉ chuyển lại tệp PDF TIẾNG VIỆT
        # của /generate-pdf-auto, dù máy chủ đã sinh bản Anh song sinh. Nay đề có de_id thì đưa liên kết ổn định
        # /api/exam/tai-de/<id> (có bản Anh -> ?ngon_ngu=ca-hai, tải về .zip Việt + Anh) giống form tạo đề nhanh, và
        # ghi rõ hai lựa chọn đã áp dụng (mức luyện tập, tiếng Anh) để người dùng thấy nút có tác dụng.
        if de_id_de_hoi:
            from app.routers.exam import thong_tin_tai_de
            thong_tin = thong_tin_tai_de(de_vua_sinh)
            file_url = thong_tin["url_tai"]
            filename = "de_thi.zip" if thong_tin["co_ban_tieng_anh"] else "de_thi.pdf"
            cau_dan = cau_dan + " " + dong_tuy_chon_da_ap_dung(
                thong_tin, tuy_chon_de_service.lay_kem_tieng_anh(conversation_id), lay_ngon_ngu(request))

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
    du_phong = await run_in_threadpool(_du_phong_tao_de, request, message, user.id, conversation_id, vai_tro)
    if du_phong:
        return du_phong
    loi = "Không hiểu phản hồi từ n8n."
    history_service.luu_tin_nhan(
        user_id=user.id, conversation_id=conversation_id,
        role="assistant", noi_dung=loi, loai_phan_hoi="error",
    )
    return {"success": False, "message": loi, "data": None}
