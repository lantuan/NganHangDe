"""
Routes danh cho giao vien: ket noi tai khoan Google Classroom (1 lan),
dong bo danh sach email hoc sinh, va xem thu danh sach da dong bo de
kiem tra. Tat ca deu yeu cau da dang nhap (get_current_user) - ngoai ra
con duoc Google tu chan mot lop nua vi app dang o che do "Testing" ben
Google Cloud Console: chi tai khoan giao vien (da them lam Test user)
moi hoan tat duoc buoc dang nhap Google o day, tai khoan khac se bi
Google bao loi ngay tu man hinh dong y quyen.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.deps import get_current_user
from app.core.lop_config import DANH_SACH_LOP
from app.services import classroom_service, history_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/gv/classroom/connect")
async def classroom_connect(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return RedirectResponse(classroom_service.tao_url_xac_thuc(), status_code=303)


@router.get("/gv/classroom/callback", response_class=HTMLResponse)
async def classroom_callback(request: Request, code: str = None, error: str = None):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    if error:
        return HTMLResponse(f"<h1>Loi ket noi Classroom</h1><p>{error}</p>")

    if not code:
        return HTMLResponse("<h1>Loi ket noi Classroom</h1><p>Thieu ma xac thuc (code).</p>")

    try:
        token_data = classroom_service.doi_code_lay_token(code)
    except Exception as e:
        return HTMLResponse(f"<h1>Loi doi code lay token</h1><p>{e}</p>")

    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        return HTMLResponse(
            "<h1>Khong nhan duoc refresh_token</h1>"
            "<p>Co the tai khoan nay da tung cho phep app truoc do (Google chi "
            "tra refresh_token o lan dau tien). Vao Google Account &gt; Security "
            "&gt; Third-party access, go quyen truy cap cua app "
            "\"NganHangDe Classroom Sync\", roi vao lai "
            "<a href='/gv/classroom/connect'>/gv/classroom/connect</a> de thu lai.</p>"
        )

    classroom_service.luu_refresh_token(refresh_token)

    return HTMLResponse(
        "<h1>Da ket noi Classroom thanh cong!</h1>"
        "<p>Vao <a href='/gv/classroom/sync'>/gv/classroom/sync</a> "
        "de dong bo danh sach hoc sinh.</p>"
    )


@router.get("/gv/classroom/sync")
async def classroom_sync(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    try:
        thong_ke = classroom_service.dong_bo_toan_bo()
    except Exception as e:
        raise HTTPException(500, f"Loi dong bo: {e}")

    return {"success": True, "thong_ke_so_email_moi_lop": thong_ke}


@router.get("/gv/classroom/debug-roster")
async def classroom_debug_roster(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)

    data = classroom_service.lay_toan_bo_roster()
    return {"success": True, "so_luong": len(data), "data": data}


# ======================================================
# THONG KE NANG LUC HOC TAP (danh cho GV) - doc tu exam_history (da co
# san, luu diem + chi_tiet_bai_lam moi lan cham bai qua /api/exam/grade
# hoac /api/exam/grade-photo), khong can bang moi. Xem history_service.
# lay_thong_ke_nang_luc.
# ======================================================

@router.get("/gv/thong-ke", response_class=HTMLResponse)
async def thong_ke_nang_luc_page(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="teacher/thong_ke.html",
        context={"danh_sach_lop": DANH_SACH_LOP},
    )


@router.get("/gv/thong-ke/data")
async def thong_ke_nang_luc_data(request: Request, khoi: str | None = None, lop: str | None = None):
    user = get_current_user(request)
    if user is None:
        raise HTTPException(401, "Chua dang nhap")

    danh_sach = history_service.lay_thong_ke_nang_luc(khoi=khoi, lop=lop)

    theo_hoc_sinh: dict = {}
    loi_theo_chuong_bai: dict = {}

    for dong in danh_sach:
        sid = dong["student_id"]
        if sid not in theo_hoc_sinh:
            theo_hoc_sinh[sid] = {
                "student_id": sid, "ho_ten": dong["ho_ten"],
                "khoi": dong["khoi"], "lop": dong["lop"],
                "so_bai_da_lam": 0, "tong_diem": 0.0, "loi_hay_sai": {},
            }
        hs = theo_hoc_sinh[sid]
        hs["so_bai_da_lam"] += 1
        hs["tong_diem"] += dong["diem"] or 0

        for cau in dong["chi_tiet_bai_lam"] or []:
            chuong = cau.get("chuong")
            if chuong is None:
                continue
            bai = cau.get("bai")
            key = f"{chuong}-{bai}"

            # "Sai" ap dung cho ca cau dung/sai ro rang (MC/SA) lan cau
            # cham theo diem (TF/TL qua CHV_Grader): duoi 50% diem toi da
            # thi tinh la chua vung, dong vai tro nhu "sai" trong thong ke.
            sai = False
            dung_sai = cau.get("dung_sai_hoac_diem")
            diem_dat_duoc = cau.get("diem_dat_duoc")
            diem_toi_da = cau.get("diem_toi_da") or 0
            if dung_sai is False:
                sai = True
            elif isinstance(dung_sai, (int, float)) and not isinstance(dung_sai, bool):
                sai = diem_toi_da > 0 and dung_sai < diem_toi_da * 0.5
            elif diem_dat_duoc is not None:
                sai = diem_toi_da > 0 and diem_dat_duoc < diem_toi_da * 0.5

            if key not in loi_theo_chuong_bai:
                loi_theo_chuong_bai[key] = {"chuong": chuong, "bai": bai, "so_lan_sai": 0, "so_lan_lam": 0}
            loi_theo_chuong_bai[key]["so_lan_lam"] += 1
            if sai:
                loi_theo_chuong_bai[key]["so_lan_sai"] += 1
                hs["loi_hay_sai"][key] = hs["loi_hay_sai"].get(key, 0) + 1

    danh_sach_hoc_sinh = []
    for hs in theo_hoc_sinh.values():
        diem_tb = round(hs["tong_diem"] / hs["so_bai_da_lam"], 2) if hs["so_bai_da_lam"] else 0
        top_loi = sorted(hs["loi_hay_sai"].items(), key=lambda x: -x[1])[:3]
        danh_sach_hoc_sinh.append({
            "student_id": hs["student_id"], "ho_ten": hs["ho_ten"],
            "khoi": hs["khoi"], "lop": hs["lop"],
            "so_bai_da_lam": hs["so_bai_da_lam"], "diem_trung_binh": diem_tb,
            "top_loi": [{"chuong_bai": k, "so_lan_sai": v} for k, v in top_loi],
        })
    danh_sach_hoc_sinh.sort(key=lambda x: x["diem_trung_binh"])

    danh_sach_loi_ca_lop = [
        x for x in loi_theo_chuong_bai.values()
        if x["so_lan_sai"] > 0 and x["so_lan_lam"] >= 2
    ]
    danh_sach_loi_ca_lop.sort(key=lambda x: -(x["so_lan_sai"] / x["so_lan_lam"]))
    danh_sach_loi_ca_lop = danh_sach_loi_ca_lop[:10]

    diem_tb_ca_lop = (
        round(sum(h["diem_trung_binh"] for h in danh_sach_hoc_sinh) / len(danh_sach_hoc_sinh), 2)
        if danh_sach_hoc_sinh else 0
    )

    return {
        "success": True,
        "data": {
            "tong_so_hoc_sinh": len(danh_sach_hoc_sinh),
            "tong_so_bai_da_cham": len(danh_sach),
            "diem_trung_binh_ca_lop": diem_tb_ca_lop,
            "hoc_sinh": danh_sach_hoc_sinh,
            "loi_ca_lop": danh_sach_loi_ca_lop,
        },
    }
