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
