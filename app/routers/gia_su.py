"""
API GIA SU AI - MUC A (docs/23_GIA_SU_AI.md).

  POST /api/giasu/hoi          - hoi ve DUNG 1 cau trong de vua lam
  GET  /api/giasu/luot         - con bao nhieu luot hom nay
  GET  /api/giasu/de-gan-nhat  - liet ke cac cau cua de gan nhat, chia
                                 4 phan, de Frontend ve nut bam tung cau

Moi thao tac deu yeu cau da dang nhap: user_id lay tu COOKIE (phien dang
nhap), KHONG lay tu body - neu khong thi ai cung gui user_id nguoi khac
len de tieu luot cua ho.

Ham xu ly khai bao `def` (khong phai `async def`) de FastAPI tu day sang
threadpool: ben trong co goi httpx dong bo sang n8n (toi 60 giay), de
`async def` se chan event loop nhu loi da gap o /gv/ra-de (docs v2.56).
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.deps import get_current_user
from app.services.i18n_service import lay_ngon_ngu
from app.services import gia_su_service, history_service
from app.services.gia_su_service import GiaSuError

router = APIRouter(prefix="/api/giasu", tags=["GiaSu"])


class HoiRequest(BaseModel):
    de_id: str
    so_thu_tu: int
    cau_hoi: str
    # Vai luot hoi truoc do cua CHINH cau nay, de hoc sinh hoi tiep duoc
    # ("em van chua hieu buoc 2"). Dang [{"vai": "hs"|"ai", "noi": "..."}].
    lich_su: list[dict] | None = None
    # Hội thoại chat đang mở (cô Lan 22/10/2026: đổi Việt/Anh -> tải lại trang -> mất phần hỏi lại câu): có thì
    # lưu cả câu hỏi lẫn câu trả lời vào chat_history (loai_phan_hoi "gia_su") để mở lại hội thoại vẫn còn.
    conversation_id: str | None = None
    cau_hien_thi: str | None = None


@router.get("/luot")
def luot_con_lai_endpoint(request: Request):
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Em cần đăng nhập để dùng phần này.")
    return {"success": True, "message": "", "data": gia_su_service.lay_luot(user.id)}


@router.get("/de-gan-nhat")
def de_gan_nhat_endpoint(request: Request, conversation_id: str):
    """
    Cho nut "Hoi lai de cu": tra ve de gan nhat trong cuoc hoi thoai,
    chia thanh PHAN I/II/III/IV, moi cau kem `hoi_duoc`.

    Hoc sinh vua tao de xong thi trong dau da co ngu canh, khong ai nghi
    phai go lai "cau 3 cua de vua nay". Bam nut thi may chu BIET CHAC de
    nao, cau nao - khong phai doan.
    """
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Em cần đăng nhập để dùng phần này.")
    try:
        du_lieu = gia_su_service.liet_ke_cau_de_gan_nhat(user.id, conversation_id, lay_ngon_ngu(request))
    except GiaSuError as e:
        return {"success": False, "message": str(e), "data": None}
    du_lieu["luot"] = gia_su_service.lay_luot(user.id)
    return {"success": True, "message": "", "data": du_lieu}


@router.post("/hoi")
def hoi_endpoint(request: Request, payload: HoiRequest):
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Em cần đăng nhập để hỏi thầy/cô AI.")

    try:
        ket_qua = gia_su_service.hoi(
            user_id=user.id,
            de_id=payload.de_id,
            so_thu_tu=payload.so_thu_tu,
            cau_hoi=payload.cau_hoi,
            lich_su=payload.lich_su,
            lang=lay_ngon_ngu(request),
        )
    except GiaSuError as e:
        # Loi "hien duoc cho hoc sinh doc": tra 200 kem success=False de
        # Frontend in thang ra khung chat thay vi bao "loi ket noi".
        # Kem luon loi giai chuan neu lay duoc - het luot/AI hong thi hoc
        # sinh van con cai de doc.
        du_phong = _loi_giai_du_phong(payload.de_id, payload.so_thu_tu, user.id, lay_ngon_ngu(request))
        kq = {"success": False, "message": str(e), "data": du_phong}
        _luu_vao_hoi_thoai(user.id, payload, kq)
        return kq

    kq = {"success": True, "message": "", "data": ket_qua}
    _luu_vao_hoi_thoai(user.id, payload, kq)
    return kq


def _luu_vao_hoi_thoai(user_id: str, payload: "HoiRequest", kq: dict) -> None:
    """Ghi câu hỏi + câu trả lời của gia sư vào chat_history (khi gọi từ khung chat, có conversation_id). Câu trả
    lời lưu NGUYÊN gói JSON {success, message, data} để chat.html vẽ lại y hệt lúc vừa hỏi (htmlTraLoiGiaSu)."""
    if not payload.conversation_id:
        return
    import json
    try:
        history_service.luu_tin_nhan(user_id=user_id, conversation_id=payload.conversation_id, role="user",
                                     noi_dung=payload.cau_hien_thi or payload.cau_hoi)
        history_service.luu_tin_nhan(user_id=user_id, conversation_id=payload.conversation_id, role="assistant",
                                     noi_dung=json.dumps(kq, ensure_ascii=False), loai_phan_hoi="gia_su")
    except Exception as e:                    # lưu lịch sử hỏng không được làm hỏng câu trả lời
        print("LOI LUU GIA SU VAO CHAT_HISTORY:", e)


def _loi_giai_du_phong(de_id: str, so_thu_tu: int, user_id: str, lang: str = "vi") -> dict | None:
    """Lay loi giai chuan de kem vao thong bao loi. Nuot moi loi: day chi
    la phan 'co thi tot', khong duoc lam hong duong bao loi chinh."""
    try:
        ngu_canh = gia_su_service.lay_ngu_canh_cau(de_id, so_thu_tu, user_id, lang)
    except Exception:
        return None
    return {
        "tra_loi": None,
        "che_do": "du_phong",
        "de_bai_python": ngu_canh["de_bai"],
        "dap_an_python": ngu_canh["dap_an"],
        "loi_giai_python": ngu_canh["loi_giai"],
    }
