"""
KHU LAM VIEC CUA GIAO VIEN (them 2026-09-13).

Truoc day tep nay rong: giao vien khong co trang lam viec rieng, chi co
2 duong dan le /gv/classroom/* va /gv/thong-ke. Nay gom lai thanh mot khu:

  GET  /gv              - trang chinh
  GET  /gv/ra-de        - bieu mau ra de danh cho giao vien
  POST /gv/ra-de        - sinh de (co SO MA DE), roi ve /gv/de-da-tao
  GET  /gv/de-da-tao    - danh sach de da tao, tai PDF / loi giai / .tex
  GET  /gv/lop          - danh sach lop, ma lop Classroom, giao vien phu trach

MOI route deu goi yeu_cau_giao_vien() truoc tien - chan o TANG SERVER,
khong chi an nut tren giao dien. Xem docs/21_TAI_KHOAN_GIAO_VIEN.md.

Khac bieu mau "Tao de nhanh" cua hoc sinh o 3 diem:
  1. role="teacher" -> xuat CA de VA loi giai (xem exam_assembler_service).
  2. Co o nhap SO MA DE: mot lan bam ra nhieu de cung cau truc, cung don
     vi kien thuc, chi khac so lieu.
  3. Tai duoc ma nguon .tex ve tu chinh (GET /api/exam/tai-tex/{de_id}).
"""

import uuid

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.deps import get_current_user, yeu_cau_giao_vien
from app.core.lop_config import DANH_SACH_LOP, MA_LOP_CLASSROOM
from app.services import classroom_service, history_service, profile_service
from app.services.exam_assembler_service import generate_exam_pdf_auto, AssembleError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Nhan hien thi cho cac ky thi (HeSo2_HeSo3). "thuong_xuyen" la HeSo1.
KI_THI_HIEN_THI = [
    ("thuong_xuyen", "Kiểm tra thường xuyên (hệ số 1) — theo chương"),
    ("giua_ky_1", "Giữa kỳ 1 (hệ số 2)"),
    ("cuoi_ky_1", "Cuối kỳ 1 (hệ số 3)"),
    ("giua_ky_2", "Giữa kỳ 2 (hệ số 2)"),
    ("cuoi_ky_2", "Cuối kỳ 2 (hệ số 3)"),
]


@router.get("/gv", response_class=HTMLResponse)
async def khu_lam_viec(request: Request):
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    ho_so = profile_service.lay_ho_so(user.id) or {}
    danh_sach_de = history_service.lay_de_cua_giao_vien(user.id, limit=5)
    da_ket_noi_classroom = bool(classroom_service.lay_refresh_token(user.id))

    return templates.TemplateResponse(
        request=request,
        name="teacher/khu_lam_viec.html",
        context={
            "ho_so": ho_so,
            "de_gan_day": danh_sach_de,
            "da_ket_noi_classroom": da_ket_noi_classroom,
        },
    )


@router.get("/gv/ra-de", response_class=HTMLResponse)
async def ra_de_form(request: Request, loi: str | None = None):
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    return templates.TemplateResponse(
        request=request,
        name="teacher/ra_de.html",
        context={"ki_thi_hien_thi": KI_THI_HIEN_THI, "loi": loi},
    )


@router.post("/gv/ra-de")
async def ra_de_submit(
    request: Request,
    lop: int = Form(...),
    ki_thi: str = Form(...),
    pham_vi_chuong: str | None = Form(default=None),
    socau_ma_de: int = Form(default=1),
    tieu_de: str = Form(default="ĐỀ KIỂM TRA MÔN TOÁN"),
    cho_phep_thieu: str | None = Form(default=None),
):
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    if lop not in (10, 11, 12):
        return RedirectResponse("/gv/ra-de?loi=Lop+phai+la+10,+11+hoac+12.", status_code=303)

    if socau_ma_de < 1 or socau_ma_de > 8:
        return RedirectResponse("/gv/ra-de?loi=So+ma+de+phai+tu+1+den+8.", status_code=303)

    # HeSo1 = kiem tra thuong xuyen theo chuong; con lai la HeSo2_HeSo3.
    if ki_thi == "thuong_xuyen":
        loai_he_so = "HeSo1"
        ki_thi_gui = None
        if not pham_vi_chuong:
            return RedirectResponse(
                "/gv/ra-de?loi=Kiem+tra+thuong+xuyen+phai+chon+chuong.",
                status_code=303,
            )
    else:
        loai_he_so = "HeSo2_HeSo3"
        ki_thi_gui = ki_thi
        pham_vi_chuong = None

    try:
        ket_qua = generate_exam_pdf_auto(
            lop=lop,
            tieu_de=tieu_de,
            role="teacher",
            loai_he_so=loai_he_so,
            ki_thi=ki_thi_gui,
            pham_vi_chuong=pham_vi_chuong,
            cau_truc_tu_hoc_sinh=None,
            socau_ma_de=socau_ma_de,
            cho_phep_thieu=bool(cho_phep_thieu),
        )
    except AssembleError as e:
        return RedirectResponse(f"/gv/ra-de?loi={e}", status_code=303)
    except Exception as e:
        print("LOI RA DE (giao vien):", e)
        return RedirectResponse(f"/gv/ra-de?loi=Loi+sinh+de:+{e}", status_code=303)

    de_id = history_service.luu_de_da_sinh(
        user_id=user.id,
        conversation_id=f"gv-{uuid.uuid4()}",
        lop=lop,
        role="teacher",
        loai_he_so=loai_he_so,
        ki_thi=ki_thi_gui,
        pham_vi_chuong=pham_vi_chuong,
        blueprint={
            "tieu_de": tieu_de,
            "cau_truc_tu_hoc_sinh": None,
            "socau_ma_de": socau_ma_de,
            "cho_phep_thieu": bool(cho_phep_thieu),
        },
    )
    if de_id:
        history_service.luu_file_de(de_id, "de", ket_qua["pdf_path"])
        history_service.luu_file_de(de_id, "tex", ket_qua["tex_path"])
        if ket_qua.get("tex_loigiai_path"):
            history_service.luu_file_de(de_id, "tex_loigiai", ket_qua["tex_loigiai_path"])
        if ket_qua.get("pdf_loigiai_path"):
            history_service.luu_file_de(de_id, "loigiai", ket_qua["pdf_loigiai_path"])
        if ket_qua.get("dap_an_json_path"):
            history_service.luu_file_de(de_id, "dapan_json", ket_qua["dap_an_json_path"])

    return RedirectResponse("/gv/de-da-tao", status_code=303)


@router.get("/gv/de-da-tao", response_class=HTMLResponse)
async def de_da_tao(request: Request):
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    return templates.TemplateResponse(
        request=request,
        name="teacher/de_da_tao.html",
        context={"danh_sach_de": history_service.lay_de_cua_giao_vien(user.id)},
    )


@router.get("/gv/lop", response_class=HTMLResponse)
async def danh_sach_lop(request: Request):
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    # Moi lop: co ma Classroom chua, va dang do giao vien nao phu trach.
    dong = []
    for khoi, ds_lop in DANH_SACH_LOP.items():
        for lop in ds_lop:
            gv_id = classroom_service.lay_giao_vien_cua_lop(khoi, lop)
            dong.append({
                "khoi": khoi,
                "lop": lop,
                "co_ma_classroom": (khoi, lop) in MA_LOP_CLASSROOM,
                "la_lop_cua_toi": gv_id == user.id,
                "da_gan_giao_vien": gv_id is not None,
            })

    return templates.TemplateResponse(
        request=request,
        name="teacher/lop.html",
        context={"danh_sach": dong},
    )


@router.get("/gv/lop/ma")
async def lay_ma_lop(request: Request, khoi: str, lop: str):
    """
    Lay MA LOP (enrollment code) + link tham gia cua mot lop tren Google
    Classroom, de giao vien phat cho hoc sinh - dung cai ma hoc sinh se
    nhap o buoc "Tham gia lop".

    Goi rieng tung lop (khong lay ca loat luc mo trang) vi moi lop la mot
    luot goi sang Google, mo trang ma goi ca chuc lan thi rat lau.
    """
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    ket_qua = classroom_service.tao_link_gia_nhap_lop(khoi, lop)
    return {
        "thanh_cong": bool(ket_qua.get("success")),
        "ma_lop": ket_qua.get("ma_dang_ky"),
        "link": ket_qua.get("link_tham_gia"),
        "thong_bao": ket_qua.get("message"),
    }
