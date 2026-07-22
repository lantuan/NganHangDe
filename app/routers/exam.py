from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.exam_scope_service import load_scope_heso1, load_scope_heso23
from app.services.generator_service import call_generator, GeneratorNotFoundError


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

    return {
        "success": True,
        "message": "",
        "data": result,
    }

from fastapi.responses import FileResponse
from app.services.exam_assembler_service import generate_exam_pdf, AssembleError


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

from app.services.question_selector_service import select_questions, SelectorError


class SelectQuestionsRequest(BaseModel):
    lop: int
    yeu_cau: list[YeuCauItem]


@router.post("/select-questions")
def select_questions_endpoint(payload: SelectQuestionsRequest):
    try:
        result = select_questions(
            lop=payload.lop,
            yeu_cau=[yc.model_dump() for yc in payload.yeu_cau],
        )
    except (FileNotFoundError, SelectorError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": "",
        "data": {
            "so_luong_da_chon": len(result),
            "danh_sach": result,
        },
    }

from app.services.exam_rules_service import resolve_cau_truc_de, ExamRulesError

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