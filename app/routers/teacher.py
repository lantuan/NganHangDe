"""
KHU LAM VIEC CUA GIAO VIEN (them 2026-09-13).

Truoc day tep nay rong: giao vien khong co trang lam viec rieng, chi co
2 duong dan le /gv/classroom/* va /gv/thong-ke. Nay gom lai thanh mot khu:

  GET  /gv              - trang chinh
  GET  /gv/ra-de        - bieu mau ra de danh cho giao vien
  POST /gv/ra-de        - sinh de (co SO MA DE), roi ve /gv/de-da-tao
  GET  /gv/de-da-tao    - danh sach de da tao, tai PDF / loi giai / .tex
  GET  /gv/lop          - danh sach lop, ma lop Classroom, giao vien phu trach
  GET  /gv/gia-su       - nhat ki hoi dap Gia su AI + nang luot cho hoc sinh
  POST /gv/gia-su/luot  - dat lai han muc luot hoi trong ngay cho 1 em

MOI route deu goi yeu_cau_giao_vien() truoc tien - chan o TANG SERVER,
khong chi an nut tren giao dien. Xem docs/21_TAI_KHOAN_GIAO_VIEN.md.

Khac bieu mau "Tao de nhanh" cua hoc sinh o 3 diem:
  1. role="teacher" -> xuat CA de VA loi giai (xem exam_assembler_service).
  2. Co o nhap SO MA DE: mot lan bam ra nhieu de cung cau truc, cung don
     vi kien thuc, chi khac so lieu.
  3. Tai duoc ma nguon .tex ve tu chinh (GET /api/exam/tai-tex/{de_id}).
"""

import uuid
from urllib.parse import quote

from fastapi import APIRouter, Request, Form
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.deps import get_current_user, yeu_cau_giao_vien
from app.core.lop_config import DANH_SACH_LOP, MA_LOP_CLASSROOM
from app.services import classroom_service, gia_su_service, history_service, profile_service
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

    print(f"RA DE (GV): lop={lop} ki_thi={ki_thi} chuong={pham_vi_chuong} "
          f"so_ma_de={socau_ma_de} nhap={bool(cho_phep_thieu)}")

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

    # PHAI chay trong threadpool. generate_exam_pdf_auto() la ham DONG BO
    # va rat lau (moi ma de mot lan bien dich LaTeX, ~30-60 giay). Goi
    # thang trong "async def" se CHAN han event loop cua uvicorn: ca web
    # dung hinh trong luc sinh de, va voi nhieu ma de thi nginx cat ket
    # noi truoc khi xong -> khong luu duoc de nao, bang "De da tao" van
    # y nguyen. Endpoint /api/exam/generate-pdf-auto khong dinh loi nay
    # vi no khai bang "def" nen FastAPI tu day sang threadpool.
    try:
        ket_qua = await run_in_threadpool(
            generate_exam_pdf_auto,
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
        return RedirectResponse("/gv/ra-de?loi=" + quote(str(e)), status_code=303)
    except Exception as e:
        print("LOI RA DE (giao vien):", e)
        return RedirectResponse("/gv/ra-de?loi=" + quote(f"Lỗi sinh đề: {e}"), status_code=303)

    # LOI DA SUA 2026-09-15: truoc day dat conversation_id = f"gv-{uuid4()}".
    # Cot conversation_id trong bang de_da_sinh co kieu UUID, them tien to
    # "gv-" vao la khong con hop le -> Postgres tu choi voi
    # 22P02 "invalid input syntax for type uuid" -> de sinh xong bi vut,
    # bang "De da tao" khong bao gio co dong moi. Khong can tien to: cot
    # role da ghi "teacher" de phan biet de do giao vien tao.
    de_id = history_service.luu_de_da_sinh(
        user_id=user.id,
        conversation_id=str(uuid.uuid4()),
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
    if not de_id:
        # Sinh de xong ma khong luu duoc thi nguoi dung PHAI biet, khong
        # duoc im lang day ve bang trong - truoc day chinh cho nay lam mat
        # ca buoi do tim.
        print("RA DE (GV): SINH DE XONG NHUNG KHONG LUU DUOC de_da_sinh "
              "-> de se KHONG hien trong bang 'De da tao'.")
        return RedirectResponse(
            "/gv/ra-de?loi=" + quote(
                "Đã sinh đề xong nhưng không lưu được vào cơ sở dữ liệu, "
                "nên đề không hiện trong bảng. Xem log máy chủ "
                "(journalctl -u nganhangde | grep 'LOI LUU DE_DA_SINH') "
                "để biết lý do."
            ),
            status_code=303,
        )

    if de_id:
        print(f"RA DE (GV): xong, de_id={de_id}, so ma de={socau_ma_de}")
        history_service.luu_file_de(de_id, "de", ket_qua["pdf_path"])
        history_service.luu_file_de(de_id, "tex", ket_qua["tex_path"])
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


# ======================================================
# GIA SU AI (them 2026-09-16, docs/23_GIA_SU_AI.md)
# Day la LOP KHOA thu 3 chong "AI tu tinh toan": moi cau tra loi cua AI
# deu duoc luu kem dap an Python da dua vao lenh, giao vien doc lai o
# day va thay ngay neu AI noi lech so voi dap an chuan.
# ======================================================

@router.get("/gv/gia-su")
def trang_gia_su(request: Request, hoc_sinh: str | None = None):
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    nhat_ki = gia_su_service.lay_nhat_ki(gioi_han=200, user_id=hoc_sinh)

    # Gan ten hoc sinh vao tung dong (nhat ki chi luu user_id).
    ten_theo_id = {}
    for dong in nhat_ki:
        uid = dong.get("user_id")
        if uid and uid not in ten_theo_id:
            ho_so = profile_service.lay_ho_so(uid) or {}
            ten_theo_id[uid] = (
                ho_so.get("ho_ten") or uid[:8],
                f"{ho_so.get('khoi') or ''}{ho_so.get('lop') or ''}",
            )
    for dong in nhat_ki:
        ten, lop = ten_theo_id.get(dong.get("user_id"), ("(không rõ)", ""))
        dong["ho_ten"] = ten
        dong["lop_hien_thi"] = lop
        # Dap an AI co khop dap an Python khong - chi la GOI Y de mat
        # giao vien luot nhanh, khong phai ket luan may moc.
        dap_an = (dong.get("dap_an_python") or "").strip()
        tra_loi = dong.get("tra_loi") or ""
        dong["co_nhac_dap_an"] = bool(dap_an) and dap_an[:20] in tra_loi

    return templates.TemplateResponse(
        request=request,
        name="teacher/gia_su.html",
        context={
            "nhat_ki": nhat_ki,
            "loc_hoc_sinh": hoc_sinh,
            "luot_mac_dinh": gia_su_service.GIA_SU_LUOT_MOI_NGAY,
        },
    )


@router.post("/gv/gia-su/luot")
def dat_luot_gia_su(request: Request, hoc_sinh: str = Form(...), gioi_han: int = Form(...)):
    """Nang/ha han muc luot hoi TRONG NGAY HOM NAY cho 1 em."""
    user = get_current_user(request)
    chan = yeu_cau_giao_vien(request, user)
    if chan is not None:
        return chan

    gia_su_service.dat_gioi_han(hoc_sinh, max(0, int(gioi_han)))
    return RedirectResponse(f"/gv/gia-su?hoc_sinh={quote(hoc_sinh)}", status_code=303)
