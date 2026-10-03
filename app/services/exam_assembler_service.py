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
from app.services.hinh_ve_service import dich_hinh_trong_khoi
from app.services.mapping_service import tim_dang_ngoai_yccd
from app.services.generator_service import (
    call_generator, GeneratorNotFoundError, LoaiCauSaiError, CauHongError,
    chup_trang_thai_xoay, khoi_phuc_trang_thai_xoay, dat_hat_giong,
)
import secrets
import threading
import json
import shutil
from pathlib import Path
from app.services.latex_service import (
    build_latex_document, save_tex_file, tinh_ma_de, TEMP_DIR, TEMP_DIR_EN,
)
from app.services.answer_parser_service import trich_dap_an, AnswerParseError
from app.services.pdf_service import compile_pdf, PdfCompileError, EXPORTS_DIR_EN
class AssembleError(Exception):
    pass


def _bien_dich(tex_path, lang: str = "vi"):
    """Biên dịch PDF; bản tiếng Việt gọi compile_pdf(tex) như cũ, bản Anh thêm lang để ghi vào thư mục tiếng Anh."""
    return compile_pdf(tex_path, lang) if lang == "en" else compile_pdf(tex_path)
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
def _dong_placeholder_thieu(item: dict, ghi_chu: str | None = None, lang: str = "vi") -> str:
    """
    Dòng LaTeX hiển thị khi 1 câu bị THIẾU (không có Mapping hoặc không có
    hàm Python), dùng ở chế độ nháp (cho_phep_thieu=True). Chỉ dùng
    \\textbf, \\fbox, \\center — không cần package LaTeX phụ, an toàn với
    mọi document class. Mọi text thô đều phải escape qua _escape_latex
    trước khi chèn vào (curriculum_id có dấu "_", ghi_chu có thể có "_", "%"...).
    """
    thieu_o = item.get("thieu_o") or "python"
    o_dau = "MAPPING" if thieu_o == "mapping" else "PYTHON"
    nhan = (item.get("ma_thieu") or item.get("generator_id")
            or item.get("curriculum_id") or f"chương {item.get('chuong_so')}")
    chi_tiet = ghi_chu or item.get("ghi_chu") or ""
    dong = (
        (r"\begin{center}\fbox{\textbf{[MISSING IN " + o_dau + r" --- ID: " if lang == "en"
         else r"\begin{center}\fbox{\textbf{[THIẾU Ở " + o_dau + r" --- ID: ") +
        _escape_latex(str(nhan)) + r"]}}\end{center}"
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

# Thu tu 4 phan + so La Ma + cach ghi loi dan. {n} la so cau cua phan do.
#
# SO LA MA GAN CHET VAO LOAI CAU (co Lan chot 28/09/2026): Trac nghiem
# luon la PHAN I, Dung/Sai luon PHAN II, Tra loi ngan luon PHAN III, Tu
# luan luon PHAN IV - dung khuon de cua Bo (QD 764/QD-BGDDT). Phan nao
# khong co cau nao thi bo han, nhung KHONG don so cua cac phan sau len.
#
# Vi sao doi: ban cu don so lien tuc, nen de thieu phan Tra loi ngan thi
# tu luan in ra "PHAN III" trong khi trang lam bai tren web (bang TEN_PHAN
# trong gia_su_service.py) van goi no la "PHAN IV" - hoc sinh cam de giay
# doi chieu voi man hinh thi lech nhau. Nay hai ben dung chung mot chuan.
CAC_PHAN_DE = [
    ("MC", "I", "Thí sinh trả lời từ câu 1 đến câu {n}. Mỗi câu hỏi thí sinh "
                "chỉ chọn một phương án."),
    ("TF", "II", "Thí sinh trả lời từ câu 1 đến câu {n}. Trong mỗi ý "
                 "\\textbf{{a), b), c), d)}} ở mỗi câu, thí sinh chọn đúng "
                 "hoặc sai."),
    ("SA", "III", "Thí sinh trả lời từ câu 1 đến câu {n}."),
    ("TL", "IV", "Thí sinh trình bày tự luận từ bài 1 đến bài {n}."),
]


# Bản tiếng Anh của khung đề (cùng thứ tự, cùng số La Mã).
CAC_PHAN_DE_EN = [
    ("MC", "I", "Answer questions 1 to {n}. For each question, choose only one option."),
    ("TF", "II", "Answer questions 1 to {n}. In each statement "
                 "\\textbf{{a), b), c), d)}} of each question, choose true or false."),
    ("SA", "III", "Answer questions 1 to {n}."),
    ("TL", "IV", "Write out full solutions for problems 1 to {n}."),
]


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


def _ghep_4_phan(theo_phan: dict[str, list[str]], lang: str = "vi") -> str:
    """
    Ghep cac khoi LaTeX da gom theo dang cau thanh than mot ma de, co
    tieu de PHAN I/II/III/IV. So La Ma GAN CHET vao loai cau (xem
    CAC_PHAN_DE): phan nao khong co cau nao thi bo han, nhung cac phan
    con lai VAN GIU dung so cua minh.
    \\setcounter{ex}{0} truoc moi phan de moi phan danh so lai tu 1.
    """
    cac_khoi = []
    ten_phan = "PART" if lang == "en" else "PHẦN"
    for ma_loai, so_la_ma, loi_dan in (CAC_PHAN_DE_EN if lang == "en" else CAC_PHAN_DE):
        khoi_cau = theo_phan.get(ma_loai) or []
        if not khoi_cau:
            continue
        cac_khoi.append(
            "\\setcounter{ex}{0}\n"
            "\\noindent\\textbf{" + ten_phan + " " + so_la_ma + ".} "
            + loi_dan.format(n=len(khoi_cau)) + "\n\n"
            + "\n".join(khoi_cau)
        )
    return "\n\n".join(cac_khoi)


def _khung_mot_ma_de(tieu_de: str, lop: int, role: str, ma_de: str,
                     than_de: str, lang: str = "vi") -> str:
    """
    Mot ma de hoan chinh: tieu de truong/ky thi, o ho ten + ma de, chan
    trang, than de 4 phan, va dong "HET".

    Moi ma de co nhan rieng (\\label{made<ma>}) de \\pageref dem dung so
    trang CUA CHINH ma de do, va \\setcounter{page}{1} de moi ma de danh
    so trang lai tu 1 - giong het cach lam trong bo de mau cua giao vien.
    """
    nhan = f"made{ma_de}"

    if role == "teacher":
        if lang == "en":
            o_ho_ten = (
                "\\noindent\n"
                "\\begin{minipage}[b]{8.5cm}\n"
                "\\fontsize{11}{0}\\selectfont Name:.................................. "
                "Class:........ Room:........\n"
                "\\end{minipage}\\hspace{1.5cm}\n"
                "\\begin{minipage}[b]{4cm}\n"
                f"\\hfill\\fbox{{\\bf Exam code {ma_de}}}\n"
                "\\end{minipage}\\vspace{4pt}\n"
            )
            chan_ma_de = f" $-$ Exam code {ma_de}"
        else:
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
    cho_phep_thieu: bool = True,
    lang: str = "vi",
    seed: int | None = None,
    chi_dap_an: bool = False,
) -> dict:
    """
    chi_dap_an=True: chỉ sinh câu hỏi + tệp đáp án json (không ghép LaTeX, không biên dịch PDF) - dùng cho
    trang làm bài trực tuyến bằng tiếng Anh của học sinh.
    lang="en": sinh bản TIẾNG ANH (ngân hàng data/python_bank_en, khung ex_test_en, tệp vào data/temp_en
    và data/exports_en). seed: hạt giống; cùng seed + cùng danh_sach_id + cùng trạng thái xoay vòng thì đề
    tiếng Anh có CÙNG số liệu, cùng biến thể với đề tiếng Việt (đã kiểm bằng scripts/kiem_tuong_duong.py).
    seed=None: chọn ngẫu nhiên và trả về trong kết quả ("seed").

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
    if seed is None:
        seed = secrets.randbelow(2 ** 31)

    cac_khoi_ma_de = []
    danh_sach_dap_an: list[dict] = []
    so_cau_thieu = 0
    # Câu thuộc dạng "luyện tập thêm, ngoài YCCĐ" (cô Lan 01/10/2026): vẫn vào
    # đề nhưng báo cho giáo viên (trang Đề đã tạo + dòng chú thích % trong .tex
    # bản giáo viên) để họ quyết định giữ hay làm đề khác. Ghi theo mã đề đầu.
    canh_bao_ngoai_yccd: list[dict] = []
    so_la_ma = {ma: la for ma, la, _ in CAC_PHAN_DE}

    for chi_so in range(so_ma_de):
        ma_de = tinh_ma_de(lop, chi_so + 1)
        # Mỗi mã đề một hạt giống riêng, suy ra từ seed chung: bản Anh dùng lại đúng dãy này.
        dat_hat_giong(seed + chi_so * 104729)
        # used_variants rieng cho tung ma de: trong CUNG mot ma de thi
        # khong lap lai bien the, nhung giua cac ma de thi duoc phep -
        # cac ma de von phai tuong duong nhau ve dang toan.
        used_variants: dict = {}
        theo_phan: dict[str, list[str]] = {}
        so_thu_tu = 0

        for item in danh_sach_id:
            loai = _loai_cau_cua(item)

            if item.get("thieu"):
                theo_phan.setdefault(loai, []).append(_dong_placeholder_thieu(item, lang=lang))
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
                    lang=lang,
                )
                theo_phan.setdefault(loai, []).append(ket_qua["latex_block"])
                so_thu_tu += 1
                dong_lt = tim_dang_ngoai_yccd(lop, item.get("chuong_so"), ket_qua["generator_id"])
                if dong_lt:
                    if role == "teacher":
                        theo_phan[loai][-1] = (
                            "% LUU Y GIAO VIEN: cau nay thuoc dang LUYEN TAP THEM - khong co trong "
                            "yeu cau can dat cua Bo (" + dong_lt["id"] + "). Giu hoac thay tuy GV.\n"
                            + theo_phan[loai][-1])
                    if chi_so == 0:
                        canh_bao_ngoai_yccd.append({
                            "phan": so_la_ma.get(loai, loai),
                            "cau": len(theo_phan[loai]),
                            "generator_id": ket_qua["generator_id"],
                            "dang": dong_lt.get("Dang"),
                        })
                try:
                    dap_an = trich_dap_an(ket_qua["latex_block"])
                    # Dich hinh ve ra anh NGAY LUC SINH DE (may dang chay
                    # LaTeX san roi), de trang lam bai cua hoc sinh khong
                    # phai cho. Hinh hong thi bo qua, cau van ra binh thuong.
                    if dap_an.get("hinh_tikz"):
                        dap_an["hinh"] = dich_hinh_trong_khoi(
                            "\n".join(dap_an["hinh_tikz"]))
                    # Hinh nam TRONG phuong an / y (cau "hinh nao bieu dien...")
                    for khoa_tikz, khoa_ma in (("hinh_phuong_an_tikz", "hinh_phuong_an"),
                                               ("hinh_phat_bieu_tikz", "hinh_phat_bieu")):
                        if dap_an.get(khoa_tikz):
                            ma_theo_o = {}
                            for nhan_o, tikz_o in dap_an[khoa_tikz].items():
                                ds_ma = dich_hinh_trong_khoi(tikz_o)
                                if ds_ma:
                                    ma_theo_o[nhan_o] = ds_ma[0]
                            dap_an[khoa_ma] = ma_theo_o
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

            except CauHongError as e:
                # Hàm có thật nhưng sinh ra câu KHÔNG ĐÚNG LOẠI mà tên nó hứa
                # (ví dụ tên có _TL_ nhưng chỉ sinh một ý). Không cho câu đó vào
                # đề của học sinh, nhưng cũng không dừng cả đề - báo ra để sửa.
                if cho_phep_thieu:
                    ma = item.get("generator_id")
                    item = dict(item, thieu_o="python", ma_thieu=ma)
                    theo_phan.setdefault(loai, []).append(_dong_placeholder_thieu(
                        item, ghi_chu=str(e), lang=lang))
                    so_cau_thieu += 1
                    continue
                raise AssembleError(f"Câu sai loại: {e}")

            except GeneratorNotFoundError:
                if cho_phep_thieu:
                    ma = item.get("generator_id")
                    item = dict(item, thieu_o="python", ma_thieu=ma)
                    theo_phan.setdefault(loai, []).append(_dong_placeholder_thieu(
                        item, lang=lang, ghi_chu=(
                            "This question type has no English version yet (the chapter has not been translated)."
                            if lang == "en" else
                            "Đã khai dạng này trong Mapping nhưng chưa có hàm sinh trong ngân hàng Python.")))
                    so_cau_thieu += 1
                    continue
                raise AssembleError(f"Lỗi sinh câu hỏi cho {item['generator_id']}: {e}")
            except Exception as e:
                if cho_phep_thieu:
                    theo_phan.setdefault(loai, []).append(_dong_placeholder_thieu(
                        item, lang=lang, ghi_chu=f"Lỗi khi chạy hàm sinh câu ({type(e).__name__}): {e}"))
                    so_cau_thieu += 1
                    continue
                raise AssembleError(
                    f"Hàm sinh câu cho {item.get('generator_id')} bị lỗi khi chạy "
                    f"({type(e).__name__}): {e}"
                )

        cac_khoi_ma_de.append(_khung_mot_ma_de(
            tieu_de_an_toan, lop, role, ma_de, _ghep_4_phan(theo_phan, lang), lang,
        ))

    # Moi ma de mot trang moi.
    noi_dung = "\n\\newpage\n\n".join(cac_khoi_ma_de)
    filename = f"exam_{uuid.uuid4().hex[:8]}"
    thu_muc_tam = TEMP_DIR_EN if lang == "en" else TEMP_DIR
    thu_muc_tam.mkdir(parents=True, exist_ok=True)
    dap_an_json_path = thu_muc_tam / f"{filename}_dapan.json"
    dap_an_json_path.write_text(
        json.dumps(danh_sach_dap_an, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if chi_dap_an:
        # Không biên dịch PDF (tốn thời gian): chỉ ghi .tex; PDF được biên dịch khi người dùng bấm tải
        # (app/routers/exam.py, _pdf_en_tu_tex). Tên tệp .tex giống tệp .tex của bản Việt (xem _sinh_kem_tieng_anh).
        gv = role == "teacher"
        noi_tex = build_latex_document(
            tieu_de_an_toan, noi_dung, lop=lop, role=role,
            ex_test_option="loigiai" if gv else "dethi", lang=lang,
        )
        tex_chi = save_tex_file(noi_tex, f"{filename}_loigiai" if gv else filename, lang)
        return {
            "so_cau_da_sinh": len(danh_sach_id) - so_cau_thieu,
            "so_cau_thieu": so_cau_thieu,
            "danh_sach_generator_id": [d.get("generator_id") for d in danh_sach_id],
            "tex_path": str(tex_chi),
            "dap_an_json_path": str(dap_an_json_path),
            "seed": seed,
        }

    if role == "teacher":
        # Giáo viên: xuất CẢ đề thi (ẩn lời giải) VÀ lời giải (hiện lời
        # giải) — cùng 1 nội dung câu hỏi, chỉ khác option gọi ex_test.
        loigiai_content = build_latex_document(
            tieu_de_an_toan, noi_dung, lop=lop, role=role, ex_test_option="loigiai", lang=lang,
        )
        loigiai_tex_path = save_tex_file(loigiai_content, f"{filename}_loigiai", lang)
        try:
            loigiai_pdf_path = _bien_dich(loigiai_tex_path, lang)
        except PdfCompileError as e:
            raise AssembleError(str(e))

        dethi_content = build_latex_document(
            tieu_de_an_toan, noi_dung, lop=lop, role=role, ex_test_option="dethi", lang=lang,
        )
        dethi_tex_path = save_tex_file(dethi_content, filename, lang)
        try:
            dethi_pdf_path = _bien_dich(dethi_tex_path, lang)
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
            "canh_bao_ngoai_yccd": canh_bao_ngoai_yccd,
            "seed": seed,
        }

    # Học sinh: chỉ xuất đề thi, luôn ẩn lời giải
    latex_content = build_latex_document(
        tieu_de_an_toan, noi_dung, lop=lop, role=role, ex_test_option="dethi", lang=lang,
    )
    tex_path = save_tex_file(latex_content, filename, lang)
    try:
        pdf_path = _bien_dich(tex_path, lang)
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
        "canh_bao_ngoai_yccd": canh_bao_ngoai_yccd,
        "seed": seed,
    }


def duong_tex_en(tex_vi) -> Path:
    """Tệp .tex tiếng Anh ứng với tệp .tex tiếng Việt của đề (cùng tên, trong data/temp_en/)."""
    return TEMP_DIR_EN / Path(tex_vi).name


_KHOA_BIEN_DICH_EN: dict = {}
_KHOA_CHUNG = threading.Lock()


def bien_dich_pdf_tieng_anh(tex_vi, ban: str):
    """PDF TIẾNG ANH của đề (ban = "de" | "loigiai") từ .tex tiếng Anh nằm cạnh .tex tiếng Việt (data/temp_en/,
    CÙNG TÊN). PDF đã có thì trả ngay (kể cả khi .tex đã bị dọn); chưa có thì biên dịch rồi lưu lại. Mỗi PDF
    có một khoá riêng: lần tải bấm đúng lúc luồng nền đang biên dịch chỉ chờ rồi lấy kết quả, không biên dịch
    hai lần đè lên nhau. Không có .tex tiếng Anh (đề cũ, chương chưa dịch, không tick) -> None."""
    if not tex_vi:
        return None
    tex_en = duong_tex_en(tex_vi)
    goc = tex_en.stem[:-len("_loigiai")] if tex_en.stem.endswith("_loigiai") else tex_en.stem
    ten = goc if ban == "de" else goc + "_loigiai"
    pdf = EXPORTS_DIR_EN / (ten + ".pdf")
    if pdf.exists():
        return pdf
    if not tex_en.exists():
        return None
    with _KHOA_CHUNG:
        khoa = _KHOA_BIEN_DICH_EN.setdefault(ten, threading.Lock())
    with khoa:
        if pdf.exists():                      # luồng khác vừa biên dịch xong
            return pdf
        dang, can = (("[loigiai]{ex_test_en}", "[dethi]{ex_test_en}") if ban == "de"
                     else ("[dethi]{ex_test_en}", "[loigiai]{ex_test_en}"))
        noi_dung = tex_en.read_text(encoding="utf-8").replace(dang, can)
        if can not in noi_dung:
            return None
        tex_moi = save_tex_file(noi_dung, ten, "en")
        try:
            return compile_pdf(tex_moi, "en")
        except PdfCompileError as e:
            print("LOI BIEN DICH PDF TIENG ANH:", e)
            return None


def bien_dich_nen_tieng_anh(tex_vi) -> None:
    """Chạy trong luồng nền sau khi giáo viên tạo đề kèm tiếng Anh: biên dịch PDF đề rồi PDF lời giải bản Anh,
    để lúc giáo viên bấm tải thì đã có sẵn. Lỗi chỉ ghi log (bấm tải sẽ tự biên dịch lại)."""
    for ban in ("de", "loigiai"):
        try:
            bien_dich_pdf_tieng_anh(tex_vi, ban)
        except Exception as e:                # noqa: BLE001
            print("LOI BIEN DICH NEN PDF TIENG ANH (%s): %s" % (ban, e))


def duong_dapan_en(dapan_vi) -> Path:
    """Tệp đáp án tiếng Anh ứng với tệp đáp án tiếng Việt (cùng tên, nằm trong data/temp_en/).
    Không cần ghi vào cơ sở dữ liệu: trang làm bài suy ra đường dẫn từ tệp đáp án tiếng Việt của đề."""
    return TEMP_DIR_EN / Path(dapan_vi).name


def _sinh_kem_tieng_anh(lop, tieu_de, role, danh_sach_id, socau_ma_de, cho_phep_thieu,
                        kem_tieng_anh, tieu_de_en=None, chi_dap_an_en=False) -> dict:
    """Sinh đề tiếng Việt; nếu kem_tieng_anh thì sinh THÊM đề tiếng Anh tương ứng (cùng câu, cùng biến
    thể, cùng số liệu) vào thư mục tiếng Anh riêng. Bản Anh lỗi (vd chương chưa dịch) KHÔNG làm hỏng đề
    Việt: lỗi được ghi trong kết quả["tieng_anh_loi"]."""
    seed = secrets.randbelow(2 ** 31)
    trang_thai_dau = chup_trang_thai_xoay() if kem_tieng_anh else None
    kq = _sinh_pdf_tu_danh_sach(lop, tieu_de, role, danh_sach_id, socau_ma_de,
                                cho_phep_thieu=cho_phep_thieu, lang="vi", seed=seed)
    if not kem_tieng_anh:
        return kq
    trang_thai_sau = chup_trang_thai_xoay()
    khoi_phuc_trang_thai_xoay(trang_thai_dau)      # bản Anh bắt đầu từ ĐÚNG trạng thái của bản Việt
    try:
        kq["tieng_anh"] = _sinh_pdf_tu_danh_sach(
            lop, tieu_de_en or tieu_de, role, danh_sach_id, socau_ma_de,
            cho_phep_thieu=True, lang="en", seed=seed,
            # Bản Anh KHÔNG biên dịch PDF lúc tạo (mỗi PDF mất 30-60 giây, hai bản Việt + hai bản Anh làm
            # người dùng chờ rất lâu, có lúc nginx cắt kết nối): chỉ ghi .tex + đáp án. PDF Anh được biên dịch
            # ở nền ngay sau khi tạo (giáo viên) hoặc khi bấm tải lần đầu, xem bien_dich_pdf_tieng_anh.
            chi_dap_an=True)
        # Bản Anh đủ câu (chương đã dịch) thì để đáp án Anh cạnh đáp án Việt cho trang làm bài; thiếu câu
        # thì thôi (trang làm bài rơi về tiếng Việt, không hiện dòng [MISSING]).
        if kq["tieng_anh"].get("so_cau_thieu", 0) == 0 and kq.get("dap_an_json_path"):
            dich = duong_dapan_en(kq["dap_an_json_path"])
            dich.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(kq["tieng_anh"]["dap_an_json_path"], dich)
            kq["dapan_en_path"] = str(dich)
            if kq["tieng_anh"].get("tex_path") and kq.get("tex_path"):
                shutil.copyfile(kq["tieng_anh"]["tex_path"], duong_tex_en(kq["tex_path"]))
    except Exception as e:                           # noqa: BLE001
        kq["tieng_anh_loi"] = "%s: %s" % (type(e).__name__, e)
    finally:
        khoi_phuc_trang_thai_xoay(trang_thai_sau)    # sau cùng như thể chỉ sinh bản Việt
    return kq


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
    cho_phep_thieu: bool = True,
    kem_tieng_anh: bool = False,
    tieu_de_en: str | None = None,
    dapan_tieng_anh: bool = False,
) -> dict:
    """
    dapan_tieng_anh=True: (đề trực tuyến của học sinh) sinh thêm đáp án tiếng Anh cùng câu, cùng số liệu
    (không biên dịch PDF); kết quả["dapan_en_path"] nếu chương đã có bản Anh đủ câu.
    kem_tieng_anh=True: sinh THÊM đề tiếng Anh tương ứng (kết quả["tieng_anh"], thư mục tiếng Anh riêng).

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
    ket_qua = _sinh_kem_tieng_anh(
        lop, tieu_de, role, danh_sach_id, socau_ma_de, cho_phep_thieu,
        kem_tieng_anh or dapan_tieng_anh, tieu_de_en,
        chi_dap_an_en=dapan_tieng_anh and not kem_tieng_anh,
    )
    if dapan_tieng_anh and not kem_tieng_anh:
        ket_qua.pop("tieng_anh", None)              # chỉ có đáp án, không có PDF tiếng Anh
    ket_qua["blueprint"] = blueprint
    return ket_qua
