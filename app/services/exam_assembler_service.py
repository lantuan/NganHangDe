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
from app.services.latex_service import (
    build_latex_document, save_tex_file, tinh_ma_de, TEMP_DIR,
)
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
# ---------------------------------------------------------------------
# DUNG NOI DUNG DE THEO CAU TRUC 4 PHAN CUA BO (them 2026-09-15)
#
# Truoc day moi cau hoi duoc noi duoi nhau thanh mot mach, khong co
# "PHAN I / II / III / IV" gi ca. De cua Bo (Quyet dinh 764/QD-BGDDT)
# chia ro 4 phan theo DANG CAU, moi phan danh so cau lai tu 1. Giao vien
# in ra la dung duoc ngay, khong phai tu chen tieu de tung phan.
# ---------------------------------------------------------------------

# Thu tu 4 phan + cach ghi loi dan. {n} la so cau cua phan do.
CAC_PHAN_DE = [
    ("MC", "Thí sinh trả lời từ câu 1 đến câu {n}. Mỗi câu hỏi thí sinh "
           "chỉ chọn một phương án."),
    ("TF", "Thí sinh trả lời từ câu 1 đến câu {n}. Trong mỗi ý "
           "\\textbf{{a), b), c), d)}} ở mỗi câu, thí sinh chọn đúng hoặc sai."),
    ("SA", "Thí sinh trả lời từ câu 1 đến câu {n}."),
    ("TL", "Thí sinh trình bày tự luận từ bài 1 đến bài {n}."),
]

SO_LA_MA = ["I", "II", "III", "IV", "V", "VI"]


def _loai_cau_cua(item: dict) -> str:
    """
    Doc loai cau (MC/TF/SA/TL) tu item. Uu tien truong loai_cau; khong co
    thi suy ra tu Generator ID (xem docs/04_ID_STANDARD.md: ...._MC_A).
    """
    loai = (item.get("loai_cau") or "").upper()
    if loai in ("MC", "TF", "SA", "TL"):
        return loai
    gid = item.get("generator_id") or ""
    for ma in ("MC", "TF", "SA", "TL"):
        if f"_{ma}_" in gid or gid.endswith(f"_{ma}"):
            return ma
    return "MC"


def _ghep_4_phan(theo_phan: dict[str, list[str]]) -> str:
    """
    Ghep cac khoi LaTeX da gom theo dang cau thanh than mot ma de, co
    tieu de PHAN I/II/III/IV. Phan nao khong co cau nao thi BO HAN va
    khong chiem so La Ma (de khong bi nhay coc "PHAN I" roi "PHAN III").
    \\setcounter{ex}{0} truoc moi phan de moi phan danh so lai tu 1.
    """
    cac_khoi = []
    thu_tu = 0
    for ma_loai, loi_dan in CAC_PHAN_DE:
        khoi_cau = theo_phan.get(ma_loai) or []
        if not khoi_cau:
            continue
        so_la_ma = SO_LA_MA[thu_tu] if thu_tu < len(SO_LA_MA) else str(thu_tu + 1)
        thu_tu += 1
        cac_khoi.append(
            "\\setcounter{ex}{0}\n"
            "\\noindent\\textbf{PHẦN " + so_la_ma + ".} "
            + loi_dan.format(n=len(khoi_cau)) + "\n\n"
            + "\n".join(khoi_cau)
        )
    return "\n\n".join(cac_khoi)


def _khung_mot_ma_de(tieu_de: str, lop: int, role: str, ma_de: str,
                     than_de: str) -> str:
    """
    Mot ma de hoan chinh: tieu de truong/ky thi, o ho ten + ma de, chan
    trang, than de 4 phan, va dong "HET".

    Moi ma de co nhan rieng (\\label{made<ma>}) de \\pageref dem dung so
    trang CUA CHINH ma de do, va \\setcounter{page}{1} de moi ma de danh
    so trang lai tu 1 - giong het cach lam trong bo de mau cua giao vien.
    """
    nhan = f"made{ma_de}"

    if role == "teacher":
        o_ho_ten = (
            "\\noindent\n"
            "\\begin{minipage}[b]{8.5cm}\n"
            "\\fontsize{11}{0}\\selectfont Họ tên thí sinh:....................................... "
            "Lớp:.......... Phòng kiểm tra:...........\n"
            "\\end{minipage}\\hspace{1.5cm}\n"
            "\\begin{minipage}[b]{4cm}\n"
            f"\\hfill\\fbox{{\\bf Mã đề {ma_de}}}\n"
            "\\end{minipage}\\vspace{4pt}\n"
        )
        chan_ma_de = f" $-$ Mã đề {ma_de}"
    else:
        o_ho_ten = ""
        chan_ma_de = ""

    return (
        f"\\tieude{{\\pageref{{{nhan}}}}}{{{tieu_de}}}{{{lop}}}\n\n"
        f"{o_ho_ten}\n"
        f"\\chantrang{{\\pageref{{{nhan}}}}}{{{chan_ma_de}}}\n"
        f"\\setcounter{{page}}{{1}}\n\n"
        f"{than_de}\n\n"
        f"\\hetde\\label{{{nhan}}}\n"
    )


def _sinh_pdf_tu_danh_sach(
    lop: int,
    tieu_de: str,
    role: str,
    danh_sach_id: list[dict],
    socau_ma_de: int | None,
    cho_phep_thieu: bool = False,
) -> dict:
    """
    Phần dùng chung: gọi Python Generator -> ghép LaTeX -> biên dịch PDF.

    SUA 2026-09-15 - hai thay doi lon:

    1. NHIEU MA DE THAT SU. Truoc day socau_ma_de duoc truyen xuong ham
       sinh cau (socau_yeu_cau) roi ghep tat ca vao MOT de -> ra mot de ma
       moi cau lap lai N lan, khong phai N de. Nay lap N VONG, moi vong
       goi lai toan bo ham sinh de co bo so lieu moi -> N ma de that su,
       cung cau truc, cung don vi kien thuc, chi khac so lieu.

    2. CAU TRUC 4 PHAN theo de cua Bo: gom cau theo dang (MC/TF/SA/TL),
       moi phan mot tieu de "PHAN I/II/III/IV" va danh so lai tu 1.
    """
    tieu_de_an_toan = _escape_latex(tieu_de)
    so_ma_de = max(1, int(socau_ma_de or 1))

    cac_khoi_ma_de = []
    danh_sach_dap_an: list[dict] = []
    so_cau_thieu = 0

    for chi_so in range(so_ma_de):
        ma_de = tinh_ma_de(lop, chi_so + 1)
        # used_variants rieng cho tung ma de: trong CUNG mot ma de thi
        # khong lap lai bien the, nhung giua cac ma de thi duoc phep -
        # cac ma de von phai tuong duong nhau ve dang toan.
        used_variants: dict = {}
        theo_phan: dict[str, list[str]] = {}
        so_thu_tu = 0

        for item in danh_sach_id:
            loai = _loai_cau_cua(item)

            if item.get("thieu"):
                theo_phan.setdefault(loai, []).append(_dong_placeholder_thieu(item))
                so_cau_thieu += 1
                continue

            try:
                ket_qua = call_generator(
                    generator_id=item["generator_id"],
                    lop=lop,
                    chuong_so=item["chuong_so"],
                    role=role,
                    # MOI LAN goi chi lay 1 cau. So ma de xu ly bang vong
                    # lap ben ngoai, KHONG truyen xuong ham sinh nua.
                    socau_yeu_cau=1,
                    used_variants=used_variants,
                )
                theo_phan.setdefault(loai, []).append(ket_qua["latex_block"])
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
                ban_ghi = {
                    "so_thu_tu": so_thu_tu,
                    "generator_id": ket_qua["generator_id"],
                    **dap_an,
                }
                if so_ma_de > 1:
                    ban_ghi["ma_de"] = ma_de
                danh_sach_dap_an.append(ban_ghi)

            except GeneratorNotFoundError as e:
                if cho_phep_thieu:
                    theo_phan.setdefault(loai, []).append(
                        _dong_placeholder_thieu(item, ghi_chu=str(e)))
                    so_cau_thieu += 1
                    continue
                raise AssembleError(f"Lỗi sinh câu hỏi cho {item['generator_id']}: {e}")
            except Exception as e:
                if cho_phep_thieu:
                    theo_phan.setdefault(loai, []).append(_dong_placeholder_thieu(
                        item, ghi_chu=f"Lỗi khi chạy hàm sinh câu ({type(e).__name__}): {e}"))
                    so_cau_thieu += 1
                    continue
                raise AssembleError(
                    f"Hàm sinh câu cho {item.get('generator_id')} bị lỗi khi chạy "
                    f"({type(e).__name__}): {e}"
                )

        cac_khoi_ma_de.append(_khung_mot_ma_de(
            tieu_de_an_toan, lop, role, ma_de, _ghep_4_phan(theo_phan),
        ))

    # Moi ma de mot trang moi.
    noi_dung = "\n\\newpage\n\n".join(cac_khoi_ma_de)
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

        # CHI luu MOT ban .tex, va la ban LOI GIAI. Khong can luu ca hai:
        # hai ban chi khac nhau dung mot tham so cua goi ex_test, doi
        # [loigiai] thanh [dethi] o dong \usepackage la an het loi giai -
        # giao vien nao dung LaTeX cung biet. Luu ban loi giai vi tu do
        # suy ra ban de duoc, nguoc lai thi khong.
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
