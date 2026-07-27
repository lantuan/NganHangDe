"""
CN_ExamAssembler (+ Switch_OutputFormat nhánh PDF)

Có 2 hàm:

1. generate_exam_pdf(...)
   Chế độ THỦ CÔNG — nhận thẳng yeu_cau (chuong_so, loai_cau, muc_do,
   so_luong), dùng select_questions_by_level. Giữ lại cho test/debug
   nhanh qua API /api/exam/generate-pdf cũ.

2. generate_exam_pdf_auto(...)
   Chế độ CHÍNH THỨC (WF001) — tự build Blueprint qua Curriculum rồi
   chọn câu theo curriculum_id (select_questions). Dùng cho API mới
   /api/exam/generate-pdf-auto.
"""

import uuid

from app.services.question_selector_service import (
    select_questions_by_level,
    SelectorError,
)
from app.services.exam_blueprint_service import build_blueprint, BlueprintError
from app.services.generator_service import call_generator, GeneratorNotFoundError
from app.services.latex_service import build_latex_document, save_tex_file
from app.services.pdf_service import compile_pdf, PdfCompileError


class AssembleError(Exception):
    pass


def _sinh_pdf_tu_danh_sach(lop: int, tieu_de: str, role: str,
                            danh_sach_id: list[dict],
                            socau_ma_de: int | None) -> dict:
    """Phần dùng chung: gọi Python Generator -> ghép LaTeX -> biên dịch PDF."""
    used_variants: dict = {}
    noi_dung = ""

    for item in danh_sach_id:
        try:
            ket_qua = call_generator(
                generator_id=item["generator_id"],
                lop=lop,
                chuong_so=item["chuong_so"],
                role=role,
                socau_yeu_cau=socau_ma_de,
                used_variants=used_variants,
            )
            noi_dung += ket_qua["latex_block"] + "\n"
        except GeneratorNotFoundError as e:
            raise AssembleError(f"Lỗi sinh câu hỏi cho {item['generator_id']}: {e}")

    latex_content = build_latex_document(tieu_de, noi_dung)
    filename = f"exam_{uuid.uuid4().hex[:8]}"
    tex_path = save_tex_file(latex_content, filename)

    try:
        pdf_path = compile_pdf(tex_path)
    except PdfCompileError as e:
        raise AssembleError(str(e))

    return {
        "so_cau_da_sinh": len(danh_sach_id),
        "danh_sach_generator_id": [d["generator_id"] for d in danh_sach_id],
        "tex_path": str(tex_path),
        "pdf_path": str(pdf_path),
    }


def generate_exam_pdf(
    lop: int,
    tieu_de: str,
    yeu_cau: list[dict],
    role: str,
    socau_ma_de: int | None = None,
) -> dict:
    """Chế độ THỦ CÔNG: chọn câu theo (chuong_so, loai_cau, muc_do) trực tiếp."""
    try:
        danh_sach_id = select_questions_by_level(lop=lop, yeu_cau=yeu_cau)
    except (FileNotFoundError, SelectorError) as e:
        raise AssembleError(f"Lỗi chọn câu hỏi: {e}")

    return _sinh_pdf_tu_danh_sach(lop, tieu_de, role, danh_sach_id, socau_ma_de)


def generate_exam_pdf_auto(
    lop: int,
    tieu_de: str,
    role: str,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
    socau_ma_de: int | None = None,
) -> dict:
    """
    Chế độ CHÍNH THỨC (WF001): CN_LoadExamScope -> CN_LoadCurriculum ->
    CN_BuildBlueprint -> CN_QuestionSelector (theo curriculum_id) ->
    CN_CallPythonGenerator -> CN_ExamAssembler -> PDF.
    """
    try:
        blueprint = build_blueprint(
            lop=lop,
            loai_he_so=loai_he_so,
            ki_thi=ki_thi,
            pham_vi_chuong=pham_vi_chuong,
            cau_truc_tu_hoc_sinh=cau_truc_tu_hoc_sinh,
        )
    except BlueprintError as e:
        raise AssembleError(f"Lỗi xây Blueprint: {e}")

    from app.services.question_selector_service import select_questions
    try:
        danh_sach_id = select_questions(lop=lop, blueprint=blueprint)
    except SelectorError as e:
        raise AssembleError(f"Lỗi chọn câu hỏi: {e}")

    ket_qua = _sinh_pdf_tu_danh_sach(lop, tieu_de, role, danh_sach_id, socau_ma_de)
    ket_qua["blueprint"] = blueprint
    return ket_qua