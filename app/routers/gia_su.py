"""
API GIA SU AI - MUC A (docs/23_GIA_SU_AI.md).

  POST /api/giasu/hoi   - hoi ve DUNG 1 cau trong de vua lam
  GET  /api/giasu/luot  - con bao nhieu luot hom nay

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
from app.services import gia_su_service
from app.services.gia_su_service import GiaSuError

router = APIRouter(prefix="/api/giasu", tags=["GiaSu"])


class HoiRequest(BaseModel):
    de_id: str
    so_thu_tu: int
    cau_hoi: str
    # Vai luot hoi truoc do cua CHINH cau nay, de hoc sinh hoi tiep duoc
    # ("em van chua hieu buoc 2"). Dang [{"vai": "hs"|"ai", "noi": "..."}].
    lich_su: list[dict] | None = None


@router.get("/luot")
def luot_con_lai_endpoint(request: Request):
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Em cần đăng nhập để dùng phần này.")
    return {"success": True, "message": "", "data": gia_su_service.lay_luot(user.id)}


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
        )
    except GiaSuError as e:
        # Loi "hien duoc cho hoc sinh doc": tra 200 kem success=False de
        # Frontend in thang ra khung chat thay vi bao "loi ket noi".
        # Kem luon loi giai chuan neu lay duoc - het luot/AI hong thi hoc
        # sinh van con cai de doc.
        du_phong = _loi_giai_du_phong(payload.de_id, payload.so_thu_tu, user.id)
        return {"success": False, "message": str(e), "data": du_phong}

    return {"success": True, "message": "", "data": ket_qua}


def _loi_giai_du_phong(de_id: str, so_thu_tu: int, user_id: str) -> dict | None:
    """Lay loi giai chuan de kem vao thong bao loi. Nuot moi loi: day chi
    la phan 'co thi tot', khong duoc lam hong duong bao loi chinh."""
    try:
        ngu_canh = gia_su_service.lay_ngu_canh_cau(de_id, so_thu_tu, user_id)
    except Exception:
        return None
    return {
        "tra_loi": None,
        "che_do": "du_phong",
        "dap_an_python": ngu_canh["dap_an"],
        "loi_giai_python": ngu_canh["loi_giai"],
    }
