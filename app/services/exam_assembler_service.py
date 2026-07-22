import uuid

from app.services.question_selector_service import select_questions, SelectorError
from app.services.generator_service import call_generator, GeneratorNotFoundError
from app.services.latex_service import build_latex_document, save_tex_file
from app.services.pdf_service import compile_pdf, PdfCompileError


class AssembleError(Exception):
    pass


def generate_exam_pdf(
    lop: int,
    tieu_de: str,
    yeu_cau: list[dict],
    role: str,
    socau_ma_de: int | None = None,
) -> dict:
    """
    Luồng đầy đủ: chọn câu -> gọi Python sinh nội dung -> ghép LaTeX -> biên dịch PDF.
    """
    try:
        danh_sach_id = select_questions(lop=lop, yeu_cau=yeu_cau)
    except (FileNotFoundError, SelectorError) as e:
        raise AssembleError(f"Lỗi chọn câu hỏi: {e}")

    # Theo dõi biến thể Python đã dùng, tránh trùng khi 1 generator_id
    # bị chọn nhiều lần trong CÙNG 1 lần sinh đề này.
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