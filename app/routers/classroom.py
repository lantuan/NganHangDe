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

from app.core.deps import get_current_user
from app.services import classroom_service

router = APIRouter()


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
