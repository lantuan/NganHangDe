import json
import zipfile
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.exam_scope_service import load_scope_heso1, load_scope_heso23
from app.services.generator_service import call_generator, GeneratorNotFoundError
from app.services.exam_rules_service import resolve_cau_truc_de, ExamRulesError
from app.services.exam_blueprint_service import build_blueprint, build_and_select, BlueprintError
from app.services.question_selector_service import (
    select_questions_by_level,
    SelectorError,
)
from app.services.exam_assembler_service import (
    generate_exam_pdf,
    generate_exam_pdf_auto,
    AssembleError,
)

from app.services import history_service
from app.services.answer_parser_service import (
    trich_dap_an,
    AnswerParseError,
    chuan_hoa_dap_an_ngan,
)
from app.services.mapping_service import trich_chuong_bai
from app.services.grade_photo_service import cham_bai_bang_anh, GradePhotoError
from app.services.latex_service import save_tex_file
from app.services.pdf_service import compile_pdf, PdfCompileError
router = APIRouter(prefix="/api/exam", tags=["Exam"])


@router.get("/scope")
def get_exam_scope(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
):
    if loai_he_so == "HeSo1":
        if not pham_vi_chuong:
            raise HTTPException(400, "Thiếu pham_vi_chuong cho HeSo1")
        return load_scope_heso1(lop, pham_vi_chuong)

    if loai_he_so == "HeSo2_HeSo3":
        if not ki_thi:
            raise HTTPException(400, "Thiếu ki_thi cho HeSo2_HeSo3")
        result = load_scope_heso23(lop, ki_thi)
        if "error" in result:
            raise HTTPException(404, detail=result["error"])
        return result

    raise HTTPException(400, "loai_he_so không hợp lệ")


class YeuCauItem(BaseModel):
    chuong_so: int
    muc_do: str  # "NB" | "TH" | "VD" | "VDC"
    so_luong: int


# ======================================================
# GENERATOR
# ======================================================

class GeneratorRequest(BaseModel):
    generator_id: str
    lop: int
    chuong_so: int
    role: str  # "student" | "teacher"
    socau: int | None = None
    socot: int | None = None
    dong: int | None = None


@router.post("/generator")
def generate_question(payload: GeneratorRequest):
    if payload.role not in ("student", "teacher"):
        raise HTTPException(status_code=400, detail="role phải là 'student' hoặc 'teacher'")

    try:
        result = call_generator(
            generator_id=payload.generator_id,
            lop=payload.lop,
            chuong_so=payload.chuong_so,
            role=payload.role,
            socau_yeu_cau=payload.socau,
            socot=payload.socot,
            dong=payload.dong,
        )
    except GeneratorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"success": True, "message": "", "data": result}


# ======================================================
# RESOLVE RULES (bảng hệ số -> so_luong/ty_le theo mức độ)
# ======================================================

class ResolveExamRulesRequest(BaseModel):
    loai_he_so: str
    cau_truc_tu_hoc_sinh: dict | None = None


@router.post("/resolve-rules")
def resolve_exam_rules(payload: ResolveExamRulesRequest):
    try:
        ket_qua = resolve_cau_truc_de(
            loai_he_so=payload.loai_he_so,
            cau_truc_tu_hoc_sinh=payload.cau_truc_tu_hoc_sinh,
        )
    except ExamRulesError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "message": "", "data": ket_qua}


# ======================================================
# BLUEPRINT (chính thức — đi qua Curriculum, có curriculum_id)
# ======================================================

class BuildBlueprintRequest(BaseModel):
    lop: int
    loai_he_so: str
    ki_thi: str | None = None
    pham_vi_chuong: str | None = None
    cau_truc_tu_hoc_sinh: dict | None = None
    # Chế độ NHÁP: True = thiếu Mapping/Generator ở đâu chỉ đánh dấu "thieu",
    # không dừng cả đề. Dùng khi ngân hàng đề chưa đầy đủ. KHÔNG dùng khi
    # ra đề thật cho học sinh (để False).
    cho_phep_thieu: bool = False


@router.post("/blueprint")
def build_blueprint_endpoint(payload: BuildBlueprintRequest):
    try:
        result = build_blueprint(
            lop=payload.lop,
            loai_he_so=payload.loai_he_so,
            ki_thi=payload.ki_thi,
            pham_vi_chuong=payload.pham_vi_chuong,
            cau_truc_tu_hoc_sinh=payload.cau_truc_tu_hoc_sinh,
        )
    except BlueprintError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "message": "", "data": result}


@router.post("/blueprint-and-select")
def build_and_select_endpoint(payload: BuildBlueprintRequest):
    try:
        result = build_and_select(
            lop=payload.lop,
            loai_he_so=payload.loai_he_so,
            ki_thi=payload.ki_thi,
            pham_vi_chuong=payload.pham_vi_chuong,
            cau_truc_tu_hoc_sinh=payload.cau_truc_tu_hoc_sinh,
            cho_phep_thieu=payload.cho_phep_thieu,
        )
    except BlueprintError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "message": "", "data": result}


# ======================================================
# SELECT QUESTIONS — chế độ THỦ CÔNG (debug), không qua Curriculum
# ======================================================

class SelectQuestionsRequest(BaseModel):
    lop: int
    yeu_cau: list[YeuCauItem]


@router.post("/select-questions")
def select_questions_endpoint(payload: SelectQuestionsRequest):
    try:
        result = select_questions_by_level(
            lop=payload.lop,
            yeu_cau=[yc.model_dump() for yc in payload.yeu_cau],
        )
    except (FileNotFoundError, SelectorError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": "",
        "data": {"so_luong_da_chon": len(result), "danh_sach": result},
    }


# ======================================================
# GENERATE PDF — chế độ THỦ CÔNG (debug), không qua Curriculum
# ======================================================

class GenerateExamRequest(BaseModel):
    lop: int
    tieu_de: str
    role: str
    yeu_cau: list[YeuCauItem]
    socau_ma_de: int | None = None


@router.post("/generate-pdf")
def generate_exam_pdf_endpoint(payload: GenerateExamRequest):
    if payload.role not in ("student", "teacher"):
        raise HTTPException(400, "role phải là 'student' hoặc 'teacher'")

    try:
        result = generate_exam_pdf(
            lop=payload.lop,
            tieu_de=payload.tieu_de,
            yeu_cau=[yc.model_dump() for yc in payload.yeu_cau],
            role=payload.role,
            socau_ma_de=payload.socau_ma_de,
        )
    except AssembleError as e:
        raise HTTPException(400, detail=str(e))

    return FileResponse(
        path=result["pdf_path"],
        filename="de_thi.pdf",
        media_type="application/pdf",
    )


# ======================================================
# GENERATE PDF — chế độ CHÍNH THỨC (WF001, qua Curriculum)
# ======================================================

class GenerateExamAutoRequest(BaseModel):
    lop: int
    tieu_de: str
    role: str
    loai_he_so: str
    ki_thi: str | None = None
    pham_vi_chuong: str | None = None
    cau_truc_tu_hoc_sinh: dict | None = None
    socau_ma_de: int | None = None
    # Chế độ NHÁP — xem chú thích ở BuildBlueprintRequest. Mặc định False
    # (nghiêm ngặt) để không lỡ phát đề có chữ "THIẾU" cho học sinh.
    cho_phep_thieu: bool = False
    # Switch_OutputFormat: "pdf" (mặc định) | "tex" | "zip" (PDF + TEX cùng 1 đề)
    dinh_dang: str = "pdf"
    user_id: str | None = None
    conversation_id: str | None = None


@router.post("/generate-pdf-auto")
def generate_exam_pdf_auto_endpoint(payload: GenerateExamAutoRequest):
    if payload.role not in ("student", "teacher"):
        raise HTTPException(400, "role phải là 'student' hoặc 'teacher'")

    if payload.dinh_dang not in ("pdf", "tex", "zip"):
        raise HTTPException(400, "dinh_dang phải là 'pdf', 'tex' hoặc 'zip'")

    try:
        result = generate_exam_pdf_auto(
            lop=payload.lop,
            tieu_de=payload.tieu_de,
            role=payload.role,
            loai_he_so=payload.loai_he_so,
            ki_thi=payload.ki_thi,
            pham_vi_chuong=payload.pham_vi_chuong,
            cau_truc_tu_hoc_sinh=payload.cau_truc_tu_hoc_sinh,
            socau_ma_de=payload.socau_ma_de,
            cho_phep_thieu=payload.cho_phep_thieu,
        )
    except AssembleError as e:
        raise HTTPException(400, detail=str(e))

    if payload.user_id and payload.conversation_id:
        de_id = history_service.luu_de_da_sinh(
            user_id=payload.user_id,
            conversation_id=payload.conversation_id,
            lop=payload.lop,
            role=payload.role,
            loai_he_so=payload.loai_he_so,
            ki_thi=payload.ki_thi,
            pham_vi_chuong=payload.pham_vi_chuong,
        )
        if de_id:
            history_service.luu_file_de(de_id, "de", result["pdf_path"])
            history_service.luu_file_de(de_id, "tex", result["tex_path"])
            if result.get("pdf_loigiai_path"):
                history_service.luu_file_de(de_id, "loigiai", result["pdf_loigiai_path"])
            if result.get("dap_an_json_path"):
                history_service.luu_file_de(de_id, "dapan_json", result["dap_an_json_path"])
    # Switch_OutputFormat: cùng 1 lần sinh đề (result) -> trả về đúng định
    # dạng người dùng chọn. Không sinh lại đề mới, nên PDF và TEX luôn khớp
    # nhau (cùng bộ câu hỏi/biến thể đã chọn ở generate_exam_pdf_auto).
    if payload.dinh_dang == "tex":
        return FileResponse(
            path=result["tex_path"],
            filename="de_thi.tex",
            media_type="application/x-tex",
        )

    if payload.dinh_dang == "zip":
        pdf_path = Path(result["pdf_path"])
        tex_path = Path(result["tex_path"])
        zip_path = pdf_path.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.write(pdf_path, arcname="de_thi.pdf")
            if result.get("pdf_loigiai_path"):
                zf.write(Path(result["pdf_loigiai_path"]), arcname="loigiai.pdf")
            zf.write(tex_path, arcname="de_thi.tex")
        return FileResponse(
            path=zip_path,
            filename="de_thi.zip",
            media_type="application/zip",
        )

    return FileResponse(
        path=result["pdf_path"],
        filename="de_thi.pdf",
        media_type="application/pdf",
    )


# ======================================================
# XUAT DAP AN — tai su dung file .tex da luu trong cuoc hoi
# thoai, doi option dethi -> loigiai, khong sinh lai cau hoi
# ======================================================

class ExportLoiGiaiRequest(BaseModel):
    conversation_id: str


@router.post("/export-loigiai")
def export_loigiai_endpoint(payload: ExportLoiGiaiRequest):
    de = history_service.lay_de_gan_nhat(payload.conversation_id)
    if de is None:
        raise HTTPException(404, "Chua co de nao duoc tao trong cuoc hoi thoai nay.")

    files = de.get("files", {})

    loigiai_path = files.get("loigiai")
    if loigiai_path and Path(loigiai_path).exists():
        return FileResponse(
            path=loigiai_path,
            filename="loigiai.pdf",
            media_type="application/pdf",
        )

    tex_path = files.get("tex")
    if not tex_path or not Path(tex_path).exists():
        raise HTTPException(
            410,
            "De cu da bi don dep khoi may chu (qua 1 ngay). Vui long yeu cau tao de moi.",
        )

    noi_dung = Path(tex_path).read_text(encoding="utf-8")
    noi_dung_loigiai = noi_dung.replace(
        "\\usepackage[dethi]{ex_test}", "\\usepackage[loigiai]{ex_test}"
    )
    if noi_dung_loigiai == noi_dung:
        raise HTTPException(500, "Khong doi duoc file .tex sang ban loi giai.")

    ten_file_moi = f"{Path(tex_path).stem}_loigiai"
    tex_path_moi = save_tex_file(noi_dung_loigiai, ten_file_moi)

    try:
        pdf_path_moi = compile_pdf(tex_path_moi)
    except PdfCompileError as e:
        raise HTTPException(500, detail=f"Loi bien dich PDF loi giai: {e}")

    history_service.luu_file_de(de["id"], "loigiai", str(pdf_path_moi))

    return FileResponse(
        path=str(pdf_path_moi),
        filename="loigiai.pdf",
        media_type="application/pdf",
    )


# ======================================================
# DEBUG: trich dap an tu 1 cau hoi (chua dung trong cham bai that,
# chi de kiem tra bo trich dap an truoc khi noi vao WF007)
# ======================================================

@router.post("/debug-parse-answer")
def debug_parse_answer_endpoint(payload: GeneratorRequest):
    if payload.role not in ("student", "teacher"):
        raise HTTPException(status_code=400, detail="role phải là 'student' hoặc 'teacher'")
    try:
        result = call_generator(
            generator_id=payload.generator_id,
            lop=payload.lop,
            chuong_so=payload.chuong_so,
            role=payload.role,
            socau_yeu_cau=payload.socau,
            socot=payload.socot,
            dong=payload.dong,
        )
    except GeneratorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        dap_an = trich_dap_an(result["latex_block"])
    except AnswerParseError as e:
        raise HTTPException(status_code=500, detail=f"Loi trich dap an: {e}")
    return {
        "success": True,
        "message": "",
        "data": {
            "generator_id": result["generator_id"],
            "variant_used": result["variant_used"],
            "dap_an": dap_an,
            "latex_block": result["latex_block"],
        },
    }


# ======================================================
# CHAM BAI (buoc dau — WF007): cham tu dong cau MC/SA bang cach so
# khop voi file JSON dap an da luu san khi sinh de (buoc A2). Cau tu
# luan (TL) chua cham duoc o day, tra ve trang_thai="can_cham_tay"
# (se lam CHV_Grader o buoc sau).
# ======================================================

class CauTraLoiHocSinh(BaseModel):
    so_thu_tu: int
    cau_tra_loi: str


class ChamBaiRequest(BaseModel):
    de_id: str | None = None
    conversation_id: str | None = None
    user_id: str | None = None
    bai_lam: list[CauTraLoiHocSinh]


@router.post("/grade")
def grade_endpoint(payload: ChamBaiRequest):
    if not payload.de_id and not payload.conversation_id:
        raise HTTPException(400, "Can co de_id hoac conversation_id")

    if payload.de_id:
        de = history_service.lay_de_theo_id(payload.de_id)
    else:
        de = history_service.lay_de_gan_nhat(payload.conversation_id)

    if de is None:
        raise HTTPException(404, "Khong tim thay de.")

    files = de.get("files", {})
    dapan_path = files.get("dapan_json")
    if not dapan_path or not Path(dapan_path).exists():
        raise HTTPException(
            410,
            "Khong tim thay file dap an cua de nay (co the da bi don dep "
            "sau 1 ngay, hoac de nay sinh truoc khi co tinh nang cham bai). "
            "Vui long tao de moi.",
        )

    danh_sach_dap_an = json.loads(Path(dapan_path).read_text(encoding="utf-8"))
    dap_an_theo_stt = {cau["so_thu_tu"]: cau for cau in danh_sach_dap_an}

    tong_so_cau = len(danh_sach_dap_an)
    # Diem toi da moi cau (chia deu 10 diem cho tong so cau trong de). Chi
    # la gia tri THAM KHAO/chuan hoa theo doc 03 (diem_toi_da) — tong diem
    # chinh thuc cua bai lam van tinh theo ty le so cau dung o duoi, khong
    # cong don truc tiep tu day (tranh lech do lam tron 2 chu so).
    diem_moi_cau = round(10 / tong_so_cau, 2) if tong_so_cau else 0.0

    chi_tiet = []
    so_cau_da_cham = 0
    so_cau_dung = 0

    for bl in payload.bai_lam:
        cau = dap_an_theo_stt.get(bl.so_thu_tu)
        if cau is None:
            chi_tiet.append({
                "question_id": None,
                "loai_cau": None,
                "dung_sai_hoac_diem": None,
                "diem_toi_da": 0,
                "nhan_xet": "Khong tim thay cau hoi nay trong de da luu (kiem tra lai so_thu_tu).",
                "chuong": None,
                "bai": None,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "trang_thai": "khong_tim_thay_cau",
            })
            continue

        loai_cau = cau.get("loai_cau")
        generator_id = cau.get("generator_id")
        chuong, bai_so = trich_chuong_bai(generator_id)

        if loai_cau == "MC":
            dung = (bl.cau_tra_loi or "").strip().upper() == (
                cau.get("dap_an_dung") or ""
            ).strip().upper()
            so_cau_da_cham += 1
            so_cau_dung += 1 if dung else 0
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": "MC",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_moi_cau,
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "dap_an_hoc_sinh": bl.cau_tra_loi,
                "dap_an_dung": cau.get("dap_an_dung"),
            })
        elif loai_cau == "SA":
            dung = chuan_hoa_dap_an_ngan(bl.cau_tra_loi) == chuan_hoa_dap_an_ngan(
                cau.get("dap_an_dung")
            )
            so_cau_da_cham += 1
            so_cau_dung += 1 if dung else 0
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": "SA",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_moi_cau,
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "dap_an_hoc_sinh": bl.cau_tra_loi,
                "dap_an_dung": cau.get("dap_an_dung"),
            })
        else:
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": loai_cau or "TL",
                "dung_sai_hoac_diem": None,
                "diem_toi_da": diem_moi_cau,
                "nhan_xet": "Cau tu luan can cham tay hoac CHV_Grader (chua lam xong).",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "trang_thai": "can_cham_tay",
                "dap_an_hoc_sinh": bl.cau_tra_loi,
                "loi_giai": cau.get("loi_giai"),
            })

    diem_tam_tinh = round((so_cau_dung / tong_so_cau) * 10, 2) if tong_so_cau else 0.0

    if payload.user_id:
        history_service.luu_ket_qua_cham_bai(
            student_id=payload.user_id,
            de_thi_id=de["id"],
            diem=diem_tam_tinh,
            chi_tiet_bai_lam=chi_tiet,
        )

    return {
        "success": True,
        "message": "",
        "data": {
            "tong_so_cau": tong_so_cau,
            "so_cau_da_cham_tu_dong": so_cau_da_cham,
            "so_cau_dung": so_cau_dung,
            "diem_tren_10_tam_tinh": diem_tam_tinh,
            "ghi_chu": (
                "Diem tam tinh chi tren cac cau MC/SA da cham tu dong. "
                "Cau tu luan (TL) can cham tay hoac CHV_Grader (chua lam xong)."
            ),
            "chi_tiet": chi_tiet,
        },
    }


# ======================================================
# CHAM BAI BANG ANH (WF007 nhanh ANH): hoc sinh chup anh Phieu tra loi
# (Bo GD&DT, cho MC/TF/SA) va/hoac anh bai lam tu luan viet tay, goi 2
# webhook n8n (DocPhieuTraLoi + CHV_Grader) de doc va cham, gop ket qua
# theo dung schema Grade Result (doc 03), luu vao exam_history.
# ======================================================

class ChamBaiAnhRequest(BaseModel):
    de_id: str | None = None
    conversation_id: str | None = None
    user_id: str | None = None
    anh_phieu_base64: str | None = None
    anh_tuluan_base64: str | None = None


@router.post("/grade-photo")
def grade_photo_endpoint(payload: ChamBaiAnhRequest):
    if not payload.de_id and not payload.conversation_id:
        raise HTTPException(400, "Can co de_id hoac conversation_id")
    if not payload.anh_phieu_base64 and not payload.anh_tuluan_base64:
        raise HTTPException(400, "Can it nhat 1 trong 2: anh_phieu_base64 hoac anh_tuluan_base64")

    if payload.de_id:
        de = history_service.lay_de_theo_id(payload.de_id)
    else:
        de = history_service.lay_de_gan_nhat(payload.conversation_id)

    if de is None:
        raise HTTPException(404, "Khong tim thay de.")

    files = de.get("files", {})
    dapan_path = files.get("dapan_json")
    if not dapan_path or not Path(dapan_path).exists():
        raise HTTPException(
            410,
            "Khong tim thay file dap an cua de nay (co the da bi don dep "
            "sau 1 ngay, hoac de nay sinh truoc khi co tinh nang cham bai). "
            "Vui long tao de moi.",
        )

    danh_sach_dap_an = json.loads(Path(dapan_path).read_text(encoding="utf-8"))

    try:
        ket_qua = cham_bai_bang_anh(
            danh_sach_dap_an=danh_sach_dap_an,
            anh_phieu_base64=payload.anh_phieu_base64,
            anh_tuluan_base64=payload.anh_tuluan_base64,
        )
    except GradePhotoError as e:
        raise HTTPException(502, detail=str(e))

    if payload.user_id:
        history_service.luu_ket_qua_cham_bai(
            student_id=payload.user_id,
            de_thi_id=de["id"],
            diem=ket_qua["diem_tren_10_tam_tinh"],
            chi_tiet_bai_lam=ket_qua["chi_tiet"],
        )

    return {"success": True, "message": "", "data": ket_qua}
