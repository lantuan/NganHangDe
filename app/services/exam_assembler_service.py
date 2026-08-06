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
   cho_phep_thieu=True: chế độ NHÁP — khi ngân hàng đề (Mapping/Python
   Generator) chưa đủ, thay vì dừng cả đề, chèn 1 dòng cảnh báo
   "[THIẾU CÂU HỎI: ...]" vào đúng vị trí đó trong PDF rồi sinh tiếp
   phần còn lại. Dùng để test khung đề/luồng web trong khi bổ sung dần
   ngân hàng đề. KHÔNG dùng khi ra đề thật cho học sinh (để mặc định
   cho_phep_thieu=False lúc đó).

Ghi chú Switch_OutputFormat theo role (2026-07-29):
- role=teacher: xuất CẢ đề thi (ẩn lời giải, option "dethi") VÀ lời giải
  (hiện lời giải, option "loigiai") + file .tex — cùng 1 lần chọn câu,
  chỉ khác option gọi gói ex_test khi biên dịch.
- role=student: chỉ xuất đề thi (option "dethi"). Lời giải sau khi nộp
  bài (web làm bài online + tự chấm) là tính năng riêng, CHƯA làm ở đây.
"""
import uuid
from app.services.question_selector_service import (
    select_questions_by_level,
    SelectorError,
)
from app.services.exam_blueprint_service import build_blueprint, BlueprintError
from app.services.generator_service import call_generator, GeneratorNotFoundError
import json
from app.services.latex_service import build_latex_document, save_tex_file, TEMP_DIR
from app.services.answer_parser_service import trich_dap_an, AnswerParseError
from app.services.pdf_service import compile_pdf, PdfCompileError
class AssembleError(Exception):
    pass
_LATEX_DAC_BIET = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
def _escape_latex(text: str) -> str:
    """
    Escape các ký tự đặc biệt của LaTeX (_, %, &, #, $, {, }, ~, ^, \\)
    trước khi chèn text thô (curriculum_id, thông báo lỗi...) vào tài liệu.
    Không escape thì LaTeX sẽ lỗi biên dịch (ví dụ dấu "_" trong
    "L10_C1_B2_VD020" bị hiểu là ký hiệu chỉ số dưới của công thức toán).
    """
    if not text:
        return ""
    # Escape dấu \ trước tiên để không escape chồng lên các ký tự vừa thêm
    ket_qua = text.replace("\\", "\x00BACKSLASH\x00")
    for ky_tu, thay_the in _LATEX_DAC_BIET.items():
        if ky_tu == "\\":
            continue
        ket_qua = ket_qua.replace(ky_tu, thay_the)
    return ket_qua.replace("\x00BACKSLASH\x00", r"\textbackslash{}")
def _dong_placeholder_thieu(item: dict, ghi_chu: str | None = None) -> str:
    """
    Dòng LaTeX hiển thị khi 1 câu bị THIẾU (không có Mapping hoặc không có
    hàm Python), dùng ở chế độ nháp (cho_phep_thieu=True). Chỉ dùng
    \\textbf, \\fbox, \\center — không cần package LaTeX phụ, an toàn với
    mọi document class. Mọi text thô đều phải escape qua _escape_latex
    trước khi chèn vào (curriculum_id có dấu "_", ghi_chu có thể có "_", "%"...).
    """
    nhan = item.get("curriculum_id") or f"chương {item.get('chuong_so')}"
    loai = item.get("loai_cau", "")
    chi_tiet = ghi_chu or item.get("ghi_chu") or ""
    dong = (
        r"\begin{center}\fbox{\textbf{[THIẾU CÂU HỎI: " + _escape_latex(str(nhan)) +
        r" - " + _escape_latex(str(loai)) + r"]}}\end{center}"
    )
    if chi_tiet:
        dong += "\n\n" + r"\begin{center}{\small\textit{" + _escape_latex(chi_tiet) + r"}}\end{center}"
    return dong + "\n"
def _sinh_pdf_tu_danh_sach(
    lop: int,
    tieu_de: str,
    role: str,
    danh_sach_id: list[dict],
    socau_ma_de: int | None,
    cho_phep_thieu: bool = False,
) -> dict:
    """Phần dùng chung: gọi Python Generator -> ghép LaTeX -> biên dịch PDF."""
    used_variants: dict = {}
    noi_dung = ""
    so_cau_thieu = 0
    so_thu_tu = 0
    danh_sach_dap_an: list[dict] = []
    for item in danh_sach_id:
        if item.get("thieu"):
            noi_dung += _dong_placeholder_thieu(item) + "\n"
            so_cau_thieu += 1
            continue
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
            so_thu_tu += 1
            try:
                dap_an = trich_dap_an(ket_qua["latex_block"])
            except AnswerParseError as e:
                dap_an = {
                    "loai_cau": None,
                    "dap_an_dung": None,
                    "loi_giai": None,
                    "loi_trich_dap_an": str(e),
                }
            danh_sach_dap_an.append({
                "so_thu_tu": so_thu_tu,
                "generator_id": ket_qua["generator_id"],
                **dap_an,
            })
        except GeneratorNotFoundError as e:
            if cho_phep_thieu:
                noi_dung += _dong_placeholder_thieu(item, ghi_chu=str(e)) + "\n"
                so_cau_thieu += 1
                continue
            raise AssembleError(f"Lỗi sinh câu hỏi cho {item['generator_id']}: {e}")
        except Exception as e:
            if cho_phep_thieu:
                noi_dung += _dong_placeholder_thieu(
                    item, ghi_chu=f"Lỗi khi chạy hàm sinh câu ({type(e).__name__}): {e}"
                ) + "\n"
                so_cau_thieu += 1
                continue
            raise AssembleError(
                f"Hàm sinh câu cho {item.get('generator_id')} bị lỗi khi chạy "
                f"({type(e).__name__}): {e}"
            )

    tieu_de_an_toan = _escape_latex(tieu_de)
    filename = f"exam_{uuid.uuid4().hex[:8]}"
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    dap_an_json_path = TEMP_DIR / f"{filename}_dapan.json"
    dap_an_json_path.write_text(
        json.dumps(danh_sach_dap_an, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if role == "teacher":
        # Giáo viên: xuất CẢ đề thi (ẩn lời giải) VÀ lời giải (hiện lời
        # giải) — cùng 1 nội dung câu hỏi, chỉ khác option gọi ex_test.
        loigiai_content = build_latex_document(
            tieu_de_an_toan, noi_dung, lop=lop, role=role, ex_test_option="loigiai",
        )
        loigiai_tex_path = save_tex_file(loigiai_content, f"{filename}_loigiai")
        try:
            loigiai_pdf_path = compile_pdf(loigiai_tex_path)
        except PdfCompileError as e:
            raise AssembleError(str(e))

        dethi_content = build_latex_document(
            tieu_de_an_toan, noi_dung, lop=lop, role=role, ex_test_option="dethi",
        )
        dethi_tex_path = save_tex_file(dethi_content, filename)
        try:
            dethi_pdf_path = compile_pdf(dethi_tex_path)
        except PdfCompileError as e:
            raise AssembleError(str(e))

        return {
            "so_cau_da_sinh": len(danh_sach_id) - so_cau_thieu,
            "so_cau_thieu": so_cau_thieu,
            "danh_sach_generator_id": [d.get("generator_id") for d in danh_sach_id],
            "tex_path": str(loigiai_tex_path),
            "pdf_path": str(dethi_pdf_path),
            "pdf_loigiai_path": str(loigiai_pdf_path),
            "dap_an_json_path": str(dap_an_json_path),
        }

    # Học sinh: chỉ xuất đề thi, luôn ẩn lời giải
    latex_content = build_latex_document(
        tieu_de_an_toan, noi_dung, lop=lop, role=role, ex_test_option="dethi",
    )
    tex_path = save_tex_file(latex_content, filename)
    try:
        pdf_path = compile_pdf(tex_path)
    except PdfCompileError as e:
        raise AssembleError(str(e))

    return {
        "so_cau_da_sinh": len(danh_sach_id) - so_cau_thieu,
        "so_cau_thieu": so_cau_thieu,
        "danh_sach_generator_id": [d.get("generator_id") for d in danh_sach_id],
        "tex_path": str(tex_path),
        "pdf_path": str(pdf_path),
        "pdf_loigiai_path": None,
        "dap_an_json_path": str(dap_an_json_path),
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
    cho_phep_thieu: bool = False,
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
        danh_sach_id = select_questions(lop=lop, blueprint=blueprint, cho_phep_thieu=cho_phep_thieu)
    except SelectorError as e:
        raise AssembleError(f"Lỗi chọn câu hỏi: {e}")
    ket_qua = _sinh_pdf_tu_danh_sach(
        lop, tieu_de, role, danh_sach_id, socau_ma_de, cho_phep_thieu=cho_phep_thieu
    )
    ket_qua["blueprint"] = blueprint
    return ket_qua
