import io
import json
import zipfile
from pathlib import Path

import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, Response
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

from app.core.deps import yeu_cau_giao_vien
from app.services import history_service, profile_service
from app.services import diem_service
from app.services.answer_parser_service import (
    trich_dap_an,
    AnswerParseError,
    chuan_hoa_dap_an_ngan,
    chuan_hoa_dap_an_tf,
    loi_giai_cho_web,
)
from app.services.hinh_ve_service import duong_dan_anh
# Ten 4 phan lay tu gia_su_service de CHI CO MOT nguon - PDF, trang lam
# bai va bang chon cau cua gia su luon goi ten phan giong nhau.
from app.services.gia_su_service import TEN_PHAN, TEN_PHAN_EN
from app.services.mapping_service import trich_chuong_bai, load_mapping, dem_dang_co_ham
from app.services.grade_photo_service import cham_bai_bang_anh, GradePhotoError
from app.services.latex_service import save_tex_file
from app.services.pdf_service import compile_pdf, PdfCompileError, EXPORTS_DIR_EN
from app.services.exam_assembler_service import duong_dapan_en, duong_tex_en
from app.services.i18n_service import lay_ngon_ngu

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


@router.get("/ma-tran-mac-dinh")
def ma_tran_mac_dinh_api(loai_he_so: str = "HeSo2_HeSo3"):
    """Bảng số câu / tỉ lệ mặc định, để form giáo viên điền sẵn ma trận."""
    from app.services.ma_tran_service import ma_tran_mac_dinh
    from app.services.exam_rules_service import ExamRulesError
    try:
        return {"success": True, "message": "", "data": ma_tran_mac_dinh(loai_he_so)}
    except ExamRulesError as e:
        raise HTTPException(400, detail=str(e))


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
    cho_phep_thieu: bool = True


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
    cho_phep_thieu: bool = True
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

    # Chan som lop khong hop le (vd AI trich nham so trong "chuong 1"
    # thanh lop=1) - khong co du lieu THPT cho lop ngoai 10/11/12, de
    # cho roi vao cac ham ben duoi se crash 500 kho hieu thay vi loi
    # 400 ro rang the nay. Xem 16_CHANGELOG Version 2.26.
    if payload.lop not in (10, 11, 12):
        raise HTTPException(
            400,
            f"lop={payload.lop} không hợp lệ - hệ thống chỉ có dữ liệu cho lớp 10, 11, 12.",
        )

    # ------------------------------------------------------------------
    # VAI TRO do MAY CHU quyet dinh, khong tin theo "role" n8n gui len.
    #
    # Truoc day luong chat luon gui role="student", nen giao vien dung
    # Chat AI cung chi nhan de tran, khong co loi giai. Nay tra bang
    # profiles.vai_tro theo user_id: la giao vien thi ep role="teacher"
    # -> xuat CA de VA loi giai, va de co o "Ho ten thi sinh / Ma de".
    #
    # Dat o day (khong sua n8n) vi dung nguyen tac trong docs/00: nghiep
    # vu thuoc ve Code, AI/n8n khong duoc quyet dinh. Sua n8n cung duoc
    # nhung ai lo tay doi prompt la hong, con cho nay thi chac chan.
    # ------------------------------------------------------------------
    role_that = payload.role
    if payload.user_id and profile_service.la_giao_vien(payload.user_id):
        role_that = "teacher"
        if payload.role != "teacher":
            print(f"VAI TRO: ep role=teacher cho user {payload.user_id} "
                  f"(n8n gui '{payload.role}')")

    try:
        result = generate_exam_pdf_auto(
            lop=payload.lop,
            tieu_de=payload.tieu_de,
            role=role_that,
            loai_he_so=payload.loai_he_so,
            ki_thi=payload.ki_thi,
            pham_vi_chuong=payload.pham_vi_chuong,
            cau_truc_tu_hoc_sinh=payload.cau_truc_tu_hoc_sinh,
            socau_ma_de=payload.socau_ma_de,
            cho_phep_thieu=payload.cho_phep_thieu,
            dapan_tieng_anh=True,     # trang làm bài bằng tiếng Anh lấy đề từ ngân hàng Anh (cùng ID, cùng seed)
        )
    except AssembleError as e:
        raise HTTPException(400, detail=str(e))

    if payload.user_id and payload.conversation_id:
        de_id = history_service.luu_de_da_sinh(
            user_id=payload.user_id,
            conversation_id=payload.conversation_id,
            lop=payload.lop,
            role=role_that,
            loai_he_so=payload.loai_he_so,
            ki_thi=payload.ki_thi,
            pham_vi_chuong=payload.pham_vi_chuong,
            # Luu lai cau truc nguoi dung tu quy dinh (neu co) de sau nay
            # POST /api/exam/lam-de-khac tai tao duoc de moi Y HET cau
            # truc nay, khong roi ve cau truc mac dinh trong exam_rules.
            blueprint={
                "tieu_de": payload.tieu_de,
                "cau_truc_tu_hoc_sinh": payload.cau_truc_tu_hoc_sinh,
                "socau_ma_de": payload.socau_ma_de,
                # Luu lai de /api/exam/lam-de-khac tao de moi voi DUNG che
                # do cua de goc. Truoc day nut do de cung False nen khat
                # khe hon ca luong chat (form tao de nhanh gui true) -> de
                # goc ra duoc ma bam "Lam de khac" lai bao loi.
                "cho_phep_thieu": payload.cho_phep_thieu,
                # Cau "luyen tap them, ngoai YCCD" (docs/04 Ngoai le 4) de
                # trang De da tao / chat bao cho giao vien.
                "canh_bao_ngoai_yccd": result.get("canh_bao_ngoai_yccd") or [],
            },
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
# LAM DE KHAC CUNG CAU TRUC (nut "Lam de khac" o cuoi trang ket qua)
#
# Khong qua AI/n8n: doc lai chinh cac tham so da luu cua de cu trong
# bang de_da_sinh roi goi thang generate_exam_pdf_auto. Nho vay hoc
# sinh bam la co de moi ngay (cung chuong, cung so cau, cung muc do -
# chi khac so lieu do generator random lai), khong phu thuoc vao viec
# CHV_Fun co hieu dung cau "cho toi them de nua" hay khong.
# ======================================================

class LamDeKhacRequest(BaseModel):
    de_id: str
    user_id: str | None = None
    conversation_id: str | None = None


@router.post("/lam-de-khac")
def lam_de_khac_endpoint(payload: LamDeKhacRequest):
    de_cu = history_service.lay_de_theo_id(payload.de_id)
    if de_cu is None:
        raise HTTPException(404, "Khong tim thay de cu de tao de tuong tu.")

    blueprint = de_cu.get("blueprint") or {}
    lop = de_cu.get("lop")
    if lop not in (10, 11, 12):
        raise HTTPException(
            400,
            f"De cu khong ro lop (lop={lop}) nen khong tao lai duoc. "
            "Vui long tao de moi tu dau.",
        )

    tieu_de = blueprint.get("tieu_de") or f"Đề luyện tập lớp {lop}"

    try:
        result = generate_exam_pdf_auto(
            lop=lop,
            tieu_de=tieu_de,
            role=de_cu.get("role") or "student",
            loai_he_so=de_cu.get("loai_he_so") or "HeSo1",
            ki_thi=de_cu.get("ki_thi"),
            pham_vi_chuong=de_cu.get("pham_vi_chuong"),
            cau_truc_tu_hoc_sinh=blueprint.get("cau_truc_tu_hoc_sinh"),
            socau_ma_de=blueprint.get("socau_ma_de"),
            # De sinh truoc Version 2.41 khong luu cho_phep_thieu -> mac
            # dinh True cho giong luong chat (form tao de nhanh), khong
            # khat khe hon de goc.
            cho_phep_thieu=bool(blueprint.get("cho_phep_thieu", True)),
            dapan_tieng_anh=True,
        )
    except AssembleError as e:
        raise HTTPException(400, detail=str(e))

    # Luu de moi giong het duong di cua /generate-pdf-auto - phai co
    # dapan_json thi trang lam bai va POST /grade moi cham duoc.
    de_id_moi = history_service.luu_de_da_sinh(
        user_id=payload.user_id or de_cu.get("user_id"),
        conversation_id=payload.conversation_id or de_cu.get("conversation_id"),
        lop=lop,
        role=de_cu.get("role") or "student",
        loai_he_so=de_cu.get("loai_he_so"),
        ki_thi=de_cu.get("ki_thi"),
        pham_vi_chuong=de_cu.get("pham_vi_chuong"),
        # De moi co bo cau khac -> canh bao "ngoai YCCD" tinh lai theo de moi.
        blueprint={**blueprint, "canh_bao_ngoai_yccd": result.get("canh_bao_ngoai_yccd") or []},
    )
    if not de_id_moi:
        raise HTTPException(500, "Da sinh duoc de moi nhung khong luu duoc. Thu lai.")

    history_service.luu_file_de(de_id_moi, "de", result["pdf_path"])
    history_service.luu_file_de(de_id_moi, "tex", result["tex_path"])
    if result.get("pdf_loigiai_path"):
        history_service.luu_file_de(de_id_moi, "loigiai", result["pdf_loigiai_path"])
    if result.get("dap_an_json_path"):
        history_service.luu_file_de(de_id_moi, "dapan_json", result["dap_an_json_path"])

    return {
        "success": True,
        "message": "",
        "data": {
            "de_id": de_id_moi,
            "url_lam_bai": f"/lam-bai/{de_id_moi}",
            "so_cau_da_sinh": result.get("so_cau_da_sinh"),
            "canh_bao_ngoai_yccd": result.get("canh_bao_ngoai_yccd") or [],
        },
    }


# ======================================================
# LAY DE VUA TAO GAN NHAT TRONG 1 CUOC HOI THOAI (dung de khoi phuc
# nut "Lam bai truc tiep" khi quay lai chat, hoac sau khi tao de qua
# luong xac nhan cau truc / form tao de nhanh)
# ======================================================

@router.get("/de-gan-nhat")
def de_gan_nhat_endpoint(conversation_id: str):
    de = history_service.lay_de_gan_nhat(conversation_id)
    if de is None or not de.get("id"):
        raise HTTPException(404, "Chua co de nao duoc tao trong cuoc hoi thoai nay.")
    # Chi bao canh bao "ngoai YCCD" cho de cua giao vien - hoc sinh khong can.
    canh_bao = []
    if de.get("role") == "teacher":
        canh_bao = (de.get("blueprint") or {}).get("canh_bao_ngoai_yccd") or []
    return {"success": True, "de_id": de["id"], "canh_bao_ngoai_yccd": canh_bao}


# ======================================================
# TAI FILE DE THEO de_id - URL ON DINH (khong phai blob), dung cho
# luong xac nhan cau truc / form tao de nhanh de link tai file + tin
# nhan luu lai trong chat_history van con dung sau khi tai lai trang
# (khac voi URL.createObjectURL truoc day, se mat khi reload).
# ======================================================

def _pdf_en_tu_tex(de: dict, ban: str) -> Path | None:
    """PDF TIẾNG ANH của đề (ban = "de" | "loigiai") cho trang đang ở English, biên dịch khi cần từ .tex
    tiếng Anh nằm cạnh .tex tiếng Việt (data/temp_en/, cùng tên) rồi lưu lại. Không có .tex tiếng Anh
    (đề cũ, chương chưa dịch) -> None, nơi gọi dùng bản tiếng Việt."""
    tex_vi = (de.get("files") or {}).get("tex")
    if not tex_vi:
        return None
    tex_en = duong_tex_en(tex_vi)
    if not tex_en.exists():
        return None
    goc = tex_en.stem[:-len("_loigiai")] if tex_en.stem.endswith("_loigiai") else tex_en.stem
    ten = goc if ban == "de" else goc + "_loigiai"
    pdf = EXPORTS_DIR_EN / (ten + ".pdf")
    if pdf.exists():
        return pdf
    dang, can = ("[loigiai]{ex_test_en}", "[dethi]{ex_test_en}") if ban == "de" else ("[dethi]{ex_test_en}", "[loigiai]{ex_test_en}")
    noi_dung = tex_en.read_text(encoding="utf-8").replace(dang, can)
    if can not in noi_dung:
        return None
    tex_moi = save_tex_file(noi_dung, ten, "en")
    try:
        return compile_pdf(tex_moi, "en")
    except PdfCompileError as e:
        print("LOI BIEN DICH PDF TIENG ANH:", e)
        return None


def _pdf_vi_de(de: dict) -> Path:
    duong_dan = de.get("files", {}).get("de")
    if not duong_dan or not Path(duong_dan).exists():
        raise HTTPException(404, "File de khong con ton tai (co the da bi xoa sau 10 ngay).")
    return Path(duong_dan)


def _chon_ban_ngon_ngu(request: Request, ban: str | None) -> str:
    """ban = "vi" | "en" | "ca-hai" (hai ban cung luc, nen thanh .zip). Khong truyen -> theo ngon ngu cua trang."""
    if ban in ("vi", "en", "ca-hai"):
        return ban
    return lay_ngon_ngu(request)


def _zip_song_ngu(de_id: str, pdf_vi: Path, pdf_en: Path | None, ten: str) -> Response:
    """Gom ban tieng Viet + ban tieng Anh (neu de co ban tieng Anh) vao MOT tep .zip. Hoc sinh tick
    "tai kem ca hai thu tieng" thi nhan dung hai tep song song, cung de, cung so lieu, cung dap an."""
    bo_nho = io.BytesIO()
    with zipfile.ZipFile(bo_nho, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(pdf_vi, "%s_TiengViet.pdf" % ten)
        if pdf_en is not None:
            z.write(pdf_en, "%s_English.pdf" % ten)
    return Response(
        content=bo_nho.getvalue(), media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="%s_%s.zip"' % (ten, de_id[:8])},
    )


@router.get("/tai-de/{de_id}")
def tai_de_endpoint(request: Request, de_id: str, ban: str | None = None):
    """ban=vi|en|ca-hai. Mac dinh theo ngon ngu trang dang chon (cookie lang); ca-hai -> .zip co ca hai ban."""
    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise HTTPException(404, "Khong tim thay de nay.")
    chon = _chon_ban_ngon_ngu(request, ban)
    if chon == "ca-hai":
        return _zip_song_ngu(de_id, _pdf_vi_de(de), _pdf_en_tu_tex(de, "de"), "de")
    if chon == "en":
        pdf_en = _pdf_en_tu_tex(de, "de")
        if pdf_en is not None:
            return FileResponse(path=str(pdf_en), filename="exam.pdf", media_type="application/pdf")
    return FileResponse(
        path=str(_pdf_vi_de(de)),
        filename="de_thi.pdf",
        media_type="application/pdf",
    )


# ======================================================
# DE TIENG ANH TUONG UNG (co Lan 03/10/2026): sinh cung luc voi de tieng Viet khi giao vien tich
# "Tao kem de tieng Anh". Tep nam trong thu muc tieng Anh rieng (data/exports_en, data/temp_en);
# file_de ghi loai_file = de_en / loigiai_en / tex_en.
# ======================================================

def _tep_tieng_anh(de_id: str, khoa: str, mo_ta: str) -> str:
    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise HTTPException(404, "Khong tim thay de nay.")
    duong_dan = de.get("files", {}).get(khoa)
    if not duong_dan or not Path(duong_dan).exists():
        raise HTTPException(
            404, "De nay khong co ban tieng Anh (%s) hoac file da bi don dep." % mo_ta)
    return duong_dan


@router.get("/tai-de-en/{de_id}")
def tai_de_tieng_anh_endpoint(de_id: str, request: Request):
    chan = yeu_cau_giao_vien(request)
    if chan is not None:
        return chan
    return FileResponse(path=_tep_tieng_anh(de_id, "de_en", "PDF de"),
                        filename="exam_en_%s.pdf" % de_id[:8], media_type="application/pdf")


@router.get("/tai-loigiai-en/{de_id}")
def tai_loigiai_tieng_anh_endpoint(de_id: str, request: Request):
    chan = yeu_cau_giao_vien(request)
    if chan is not None:
        return chan
    return FileResponse(path=_tep_tieng_anh(de_id, "loigiai_en", "PDF loi giai"),
                        filename="solutions_en_%s.pdf" % de_id[:8], media_type="application/pdf")


@router.get("/tai-tex-en/{de_id}")
def tai_tex_tieng_anh_endpoint(de_id: str, request: Request):
    chan = yeu_cau_giao_vien(request)
    if chan is not None:
        return chan
    return FileResponse(path=_tep_tieng_anh(de_id, "tex_en", ".tex"),
                        filename="exam_en_%s.tex" % de_id[:8], media_type="application/x-tex")


# ======================================================
# TAI MA NGUON LATEX CUA DE (CHI GIAO VIEN)
#
# Giao vien quen dung LaTeX muon lay file .tex ve tu chinh: them mot cau
# rieng, doi cach trinh bay, ghep vao mau de cua truong. He thong da luu
# san file .tex ngay luc sinh de (file_de, loai_file="tex") nen chi viec
# tra ve - KHONG sinh lai de, de file .tex luon dung khop voi ban PDF da
# phat. Xem docs/21_TAI_KHOAN_GIAO_VIEN.md Buoc 5.
#
# Hoc sinh KHONG duoc tai: file .tex chua ca \loigiai (loi giai chi
# tiet) va cac dau \True danh dau phuong an dung.
# ======================================================

@router.get("/tai-tex/{de_id}")
def tai_tex_endpoint(de_id: str, request: Request):
    chan = yeu_cau_giao_vien(request)
    if chan is not None:
        return chan

    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise HTTPException(404, "Khong tim thay de nay.")

    duong_dan = de.get("files", {}).get("tex")
    if not duong_dan or not Path(duong_dan).exists():
        raise HTTPException(
            410,
            "File .tex cua de nay da bi don (cron xoa sau 1 ngay). "
            "Tao lai de roi tai .tex ngay trong phien do.",
        )

    # MOT tep duy nhat. De sinh cho giao vien la ban LOI GIAI; muon ban de
    # thi doi [loigiai] thanh [dethi] o dong \usepackage{ex_test}. Hai ban
    # chi khac nhau dung tham so do nen khong can tai ve ca hai.
    return FileResponse(
        path=duong_dan,
        filename=f"de_{de_id[:8]}.tex",
        media_type="application/x-tex",
    )


# ======================================================
# TAI DE / LOI GIAI DANG WORD (.docx) - CHI GIAO VIEN
#
# Doi chinh tep .tex da luu cua de (khong sinh lai de) sang Word bang
# pandoc; cong thuc la phuong trinh goc cua Word (Office Math) nen giao
# vien bam vao sua duoc. KHONG goi AI. Xem app/services/word_service.py
# va docs/21_TAI_KHOAN_GIAO_VIEN.md Buoc 6.
#   ban=de      : de thi (khong dap an, khong loi giai)
#   ban=loigiai : de + dap an + loi giai chi tiet
# ======================================================

@router.get("/tai-word/{de_id}")
def tai_word_endpoint(de_id: str, request: Request, ban: str = "de"):
    chan = yeu_cau_giao_vien(request)
    if chan is not None:
        return chan
    if ban not in ("de", "loigiai"):
        raise HTTPException(400, "ban phai la 'de' hoac 'loigiai'.")

    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise HTTPException(404, "Khong tim thay de nay.")
    duong_dan = de.get("files", {}).get("tex")
    if not duong_dan or not Path(duong_dan).exists():
        raise HTTPException(
            410,
            "File .tex cua de nay da bi don (cron xoa sau 1 ngay). "
            "Tao lai de roi tai Word ngay trong phien do.",
        )

    # Trang đang ở English và đề có .tex tiếng Anh (data/temp_en/, cùng tên): xuất Word TIẾNG ANH.
    lang = "vi"
    if lay_ngon_ngu(request) == "en" and duong_tex_en(duong_dan).exists():
        lang, duong_dan = "en", str(duong_tex_en(duong_dan))
    hau_to = "_en" if lang == "en" else ""
    ten_goc = "%s%s_%s" % ("solutions" if lang == "en" and ban == "loigiai" else
                           "exam" if lang == "en" else "loigiai" if ban == "loigiai" else "de",
                           "", de_id[:8])

    from app.services.word_service import xuat_word, WordExportError
    try:
        ra = xuat_word(Path(duong_dan), ban == "loigiai", ten_goc + hau_to, lang)
    except WordExportError as e:
        raise HTTPException(500, detail=f"Loi xuat Word: {e}")

    return FileResponse(
        path=str(ra),
        filename="%s.docx" % ten_goc,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# ======================================================
# DANH SACH CHUONG THEO LOP (theo dung phan phoi chuong trinh that
# trong data/ppct/), kem co_du_cau de FE biet chuong nao da co
# ngan hang cau hoi that (data/mapping/) va chuong nao chua co
# ======================================================

@router.get("/danh-sach-chuong")
def danh_sach_chuong_endpoint(lop: int):
    if lop not in (10, 11, 12):
        raise HTTPException(400, "lop phai la 10, 11 hoac 12.")

    ppct_file = Path("data/ppct") / f"toan{lop}.json"
    if not ppct_file.exists():
        raise HTTPException(404, f"Chua co phan phoi chuong trinh cho lop {lop}.")

    with open(ppct_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    ten_chuong_theo_so: dict[int, str] = {}
    for it in items:
        cs = it.get("chuong_so")
        if cs is not None and cs not in ten_chuong_theo_so:
            ten_chuong_theo_so[cs] = it.get("chuong", f"Chuong {cs}")

    ket_qua = []
    for cs in sorted(ten_chuong_theo_so.keys()):
        # co_du_cau phai tinh theo so dang DA CO HAM Python, khong phai so
        # dong Mapping. Mapping la ban ke hoach (co ca dang chua viet ham);
        # bao "san sang" chi vi co dong Mapping se moi hoc sinh vao mot
        # chuong chua co cau hoi nao, va ra de that se vo ca de.
        try:
            so_dang_co_ham = dem_dang_co_ham(lop, cs)
        except FileNotFoundError:
            so_dang_co_ham = 0
        ket_qua.append({
            "chuong_so": cs,
            "ten_chuong": ten_chuong_theo_so[cs],
            "co_du_cau": so_dang_co_ham > 0,
            "so_dang_co_cau_hoi": so_dang_co_ham,
        })

    return {"success": True, "data": ket_qua}


# ======================================================
# XUAT DAP AN — tai su dung file .tex da luu trong cuoc hoi
# thoai, doi option dethi -> loigiai, khong sinh lai cau hoi
# ======================================================

class ExportLoiGiaiRequest(BaseModel):
    conversation_id: str


def _xuat_loigiai(de: dict, lang: str = "vi") -> Response:
    """Tra ve PDF loi giai cua 1 de. Neu chua co san thi bien dich tu file
    .tex da luu (doi [dethi] -> [loigiai] trong ex_test) roi luu lai de
    lan sau khoi dich lai.

    Dung chung cho:
    - POST /api/exam/export-loigiai  (theo conversation_id - de MOI NHAT)
    - GET  /api/exam/tai-loigiai/{de_id} (theo dung 1 de - dung cho nut
      "Loi giai" gan duoi tung de trong hoi thoai, de hoc sinh lam nhieu
      de van xin dung loi giai cua de minh muon).
    """
    if lang == "ca-hai":
        return _zip_song_ngu(de["id"], _pdf_loigiai_vi(de), _pdf_en_tu_tex(de, "loigiai"), "loigiai")

    if lang == "en":
        pdf_en = _pdf_en_tu_tex(de, "loigiai")
        if pdf_en is not None:
            return FileResponse(path=str(pdf_en), filename="solutions.pdf", media_type="application/pdf")

    return FileResponse(
        path=str(_pdf_loigiai_vi(de)),
        filename="loigiai.pdf",
        media_type="application/pdf",
    )


def _pdf_loigiai_vi(de: dict) -> Path:
    """PDF loi giai tieng Viet; chua co thi bien dich tu .tex da luu roi luu lai."""
    files = de.get("files", {})
    loigiai_path = files.get("loigiai")
    if loigiai_path and Path(loigiai_path).exists():
        return Path(loigiai_path)

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

    return Path(pdf_path_moi)


@router.post("/export-loigiai")
def export_loigiai_endpoint(request: Request, payload: ExportLoiGiaiRequest):
    de = history_service.lay_de_gan_nhat(payload.conversation_id)
    if de is None:
        raise HTTPException(404, "Chua co de nao duoc tao trong cuoc hoi thoai nay.")
    return _xuat_loigiai(de, lay_ngon_ngu(request))


@router.get("/tai-loigiai/{de_id}")
def tai_loigiai_endpoint(request: Request, de_id: str, ban: str | None = None):
    """URL on dinh cho nut "Loi giai" gan duoi TUNG de trong hoi thoai.

    Khac /export-loigiai o cho: chi dich danh 1 de theo de_id, khong lay
    "de moi nhat". Hoc sinh lam 2-3 de lien tiep van xin duoc dung loi
    giai cua de minh muon.
    """
    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise HTTPException(404, "Khong tim thay de nay.")
    return _xuat_loigiai(de, _chon_ban_ngon_ngu(request, ban))


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
    # MC/SA: string dap an. TF: dict 4 y {"a":bool,"b":bool,"c":bool,"d":bool}
    # (thieu y nao thi coi nhu y do sai/chua tra loi).
    cau_tra_loi: str | dict | None = None


class ChamBaiRequest(BaseModel):
    de_id: str | None = None
    conversation_id: str | None = None
    user_id: str | None = None
    bai_lam: list[CauTraLoiHocSinh]


@router.post("/grade")
def grade_endpoint(request: Request, payload: ChamBaiRequest):
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

    # Trang làm bài đang ở English thì đề hiển thị là bản Anh: chấm và hiện lời giải theo đúng bản đó
    # (cùng câu, cùng đáp án với bản Việt; chỉ khác chữ và dấu thập phân).
    if lay_ngon_ngu(request) == "en" and duong_dapan_en(dapan_path).exists():
        dapan_path = str(duong_dapan_en(dapan_path))

    danh_sach_dap_an = json.loads(Path(dapan_path).read_text(encoding="utf-8"))
    dap_an_theo_stt = {cau["so_thu_tu"]: cau for cau in danh_sach_dap_an}

    tong_so_cau = len(danh_sach_dap_an)
    # Thang diem 10 theo quy dinh cua giao vien (data/config/diem_rules.json):
    # MC 3d - TF 2d - SA 2d - TL 3d. Diem cua MOI PHAN duoc chia DEU cho so
    # cau co that trong de o phan do; cau TF chia tiep deu cho 4 y. Trong so
    # CO DINH: de thieu phan nao thi diem toi da giam dung phan do.
    thang = diem_service.tinh_thang_diem(danh_sach_dap_an)

    chi_tiet = []
    so_cau_da_cham = 0
    so_cau_dung = 0
    # Cong don bang so THUC chua lam tron, chi lam tron o buoc cuoi cung
    # (tranh lech kieu 3 cau SA x 0.67 = 2.01 diem).
    tong_diem_tu_dong = 0.0

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
            tong_diem_tu_dong += (
                diem_service.diem_toi_da_cua_cau_goc(thang, "MC") if dung else 0.0
            )
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": "MC",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_service.diem_toi_da_cua_cau(thang, "MC"),
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
            tong_diem_tu_dong += (
                diem_service.diem_toi_da_cua_cau_goc(thang, "SA") if dung else 0.0
            )
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": "SA",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_service.diem_toi_da_cua_cau(thang, "SA"),
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "dap_an_hoc_sinh": bl.cau_tra_loi,
                "dap_an_dung": cau.get("dap_an_dung"),
            })
        elif loai_cau == "TF":
            # dap_an_dung: {"a":True/False,...}. Diem cua cau TF duoc chia
            # DEU cho 4 y (khong theo thang Bo GD&DT 0.1/0.25/0.5/1) -
            # thong nhat voi giao vien luc xay tinh nang.
            dap_an_dung_tf = cau.get("dap_an_dung") or {}
            tra_loi_hs = bl.cau_tra_loi if isinstance(bl.cau_tra_loi, dict) else {}
            chi_tiet_tung_y = {}
            so_y_dung = 0
            for y in ("a", "b", "c", "d"):
                hs = chuan_hoa_dap_an_tf(tra_loi_hs.get(y))
                dung_y = hs is not None and hs == dap_an_dung_tf.get(y)
                chi_tiet_tung_y[y] = dung_y
                so_y_dung += 1 if dung_y else 0
            diem_goc, diem_dat_duoc = diem_service.diem_cau_tf(thang, so_y_dung)
            so_cau_da_cham += 1
            so_cau_dung += 1 if so_y_dung == 4 else 0
            tong_diem_tu_dong += diem_goc
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": "TF",
                "dung_sai_hoac_diem": so_y_dung == 4,
                "diem_toi_da": diem_service.diem_toi_da_cua_cau(thang, "TF"),
                "diem_moi_y": thang["theo_phan"]["TF"]["diem_moi_y"],
                "diem_dat_duoc": diem_dat_duoc,
                "so_y_dung": so_y_dung,
                "chi_tiet_tung_y": chi_tiet_tung_y,
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "dap_an_hoc_sinh": tra_loi_hs,
                "dap_an_dung": dap_an_dung_tf,
            })
        else:
            # loai_cau_chuan() nhan ra ca cau TF bi answer_parser_service luu
            # nham thanh loai_cau='TL' (phan biet qua '_TF_' trong generator_id)
            # de khong tinh nham cau do vao diem phan Tu luan.
            loai_chuan = diem_service.loai_cau_chuan(cau)
            if loai_chuan == "TL":
                nhan_xet_cau = (
                    "Phần tự luận ("
                    + diem_service.so_dep(thang["diem_phan_tu_luan"])
                    + "đ) — đang xây dựng."
                )
                trang_thai_cau = "dang_xay_dung"
            else:
                nhan_xet_cau = (
                    "Câu Đúng/Sai chưa trích được đáp án đúng khi sinh đề "
                    "(answer_parser_service) nên phải chấm tay."
                )
                trang_thai_cau = "can_cham_tay"
            chi_tiet.append({
                "question_id": generator_id,
                "loai_cau": loai_chuan,
                "dung_sai_hoac_diem": None,
                "diem_toi_da": diem_service.diem_toi_da_cua_cau_theo_id(thang, loai_chuan, generator_id),
                "nhan_xet": nhan_xet_cau,
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": bl.so_thu_tu,
                "trang_thai": trang_thai_cau,
                "dap_an_hoc_sinh": bl.cau_tra_loi,
                "loi_giai": loi_giai_cho_web(cau.get("loi_giai")),
            })

    lam_tron = thang.get("lam_tron", 2)
    diem_tam_tinh = round(tong_diem_tu_dong, lam_tron) if tong_so_cau else 0.0

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
            "thang_diem": thang,
            "diem_toi_da_tu_dong": thang["diem_toi_da_tu_dong"],
            "diem_toi_da_tong": thang["diem_toi_da_tong"],
            "diem_phan_tu_luan": thang["diem_phan_tu_luan"],
            "mo_ta_thang_diem": diem_service.mo_ta_thang_diem(thang),
            "ghi_chu": (
                f"Điểm các phần chấm tự động: {diem_service.so_dep(diem_tam_tinh)}/"
                f"{diem_service.so_dep(thang['diem_toi_da_tu_dong'])} điểm. "
                f"Phần tự luận ({diem_service.so_dep(thang['diem_phan_tu_luan'])}đ): "
                "đang xây dựng."
            ),
            "chi_tiet": chi_tiet,
        },
    }


# ======================================================
# XEM DE DE LAM BAI TRUC TIEP TREN WEB (an dap an) - dung chung de_id/
# conversation_id voi /grade, /grade-photo, /export-loigiai (deu doc tu
# 1 file dapan_json duy nhat da luu khi sinh de). Chi tra ve cau MC/TF/
# SA (co the tra loi truc tiep tren web); cau TL van phai lam giay + chup
# anh gui qua /grade-photo nhu cu. Cau co hinh ve (co_hinh_ve=True, xem
# answer_parser_service.trich_de_bai) khong the ve lai bang MathJax nen
# danh dau rieng de Frontend hien ghi chu, khong bat lam truc tiep.
# ======================================================

@router.get("/hinh/{ma}")
def xem_hinh_ve_endpoint(ma: str):
    """Tra ve anh hinh ve da dich san (xem app/services/hinh_ve_service.py)."""
    if not re.fullmatch(r"[0-9a-f]{8,40}", ma):
        raise HTTPException(404, "Ma hinh khong hop le.")
    duong = duong_dan_anh(ma)
    if duong is None:
        raise HTTPException(404, "Khong tim thay hinh.")
    kieu = "image/svg+xml" if duong.suffix == ".svg" else "image/png"
    return FileResponse(duong, media_type=kieu,
                        headers={"Cache-Control": "public, max-age=31536000"})


@router.get("/quiz/{de_id}")
def xem_de_lam_bai_endpoint(request: Request, de_id: str):
    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise HTTPException(404, "Khong tim thay de.")

    files = de.get("files", {})
    dapan_path = files.get("dapan_json")
    if not dapan_path or not Path(dapan_path).exists():
        raise HTTPException(
            410,
            "Khong tim thay du lieu cau hoi cua de nay (co the da bi don "
            "dep sau 1 ngay). Vui long tao de moi.",
        )

    # Ngôn ngữ nền là TIẾNG VIỆT: đề luôn được chọn/sinh trên bản Việt (cùng ID hàm, cùng hạt giống).
    # Trang đang ở English thì lấy bản Anh của đúng đề đó (tệp đáp án tiếng Anh nằm cạnh, tên giống bản Việt);
    # không có (đề cũ, chương chưa dịch) thì dùng bản Việt.
    ngon_ngu = lay_ngon_ngu(request)
    dung_ban_anh = False
    if ngon_ngu == "en":
        duong_en = duong_dapan_en(dapan_path)
        if duong_en.exists():
            dapan_path = str(duong_en)
            dung_ban_anh = True

    danh_sach_dap_an = json.loads(Path(dapan_path).read_text(encoding="utf-8"))

    # Dem so cau da ra trong TUNG PHAN, de danh so lai tu 1 giong het
    # file PDF (co Lan chot 28/09/2026). Truoc day web danh 1 mach
    # 1..12 con PDF danh lai tu 1 moi phan -> hoc sinh cam de giay doi
    # chieu voi man hinh thi khong khop cau nao voi cau nao.
    #
    # so_thu_tu VAN GIU nguyen la so 1 mach: day la khoa dung de nop bai,
    # cham diem va hoi gia su. Chi them so_trong_phan de HIEN THI.
    dem_trong_phan: dict[str, int] = {}

    danh_sach_cau_hoi = []
    for cau in danh_sach_dap_an:
        loai_cau = cau.get("loai_cau")
        ma_phan = (loai_cau or "MC").upper()
        if ma_phan not in TEN_PHAN:
            ma_phan = "MC"
        dem_trong_phan[ma_phan] = dem_trong_phan.get(ma_phan, 0) + 1
        muc = {
            "so_thu_tu": cau.get("so_thu_tu"),
            "loai_cau": loai_cau,
            # Phan cua cau (PHAN I/II/III/IV theo khuon de cua Bo) va so
            # thu tu CUA CAU TRONG PHAN do - de trang lam bai in tieu de
            # phan va danh so cau y het file PDF.
            "ma_phan": ma_phan,
            "ten_phan": TEN_PHAN_EN[ma_phan] if ngon_ngu == "en" else TEN_PHAN[ma_phan],
            "so_trong_phan": dem_trong_phan[ma_phan],
            "de_bai": cau.get("de_bai") or "",
            "co_hinh_ve": bool(cau.get("co_hinh_ve")),
            # Duong dan anh hinh ve (neu da dich duoc). Con co_hinh_ve giu
            # lai de Frontend biet cau NAY CO hinh nhung chua dich duoc.
            #
            # SUA 28/09/2026: truoc ghi "/hinh/<ma>" nhung router nay khai
            # prefix="/api/exam" nen dia chi that la "/api/exam/hinh/<ma>".
            # Trinh duyet goi "/hinh/..." -> 404, tren trang lam bai chi
            # thay o vuong dau hoi (icon anh hong). Cau co hinh ma mat hinh
            # la doi luon muc do cua cau.
            "hinh": ["/api/exam/hinh/%s" % m for m in (cau.get("hinh") or [])],
        }
        if loai_cau == "MC":
            muc["phuong_an"] = cau.get("phuong_an") or {}
            # anh hinh ve nam TRONG tung phuong an (vd "hinh nao bieu dien mien nghiem")
            muc["hinh_phuong_an"] = {k: "/api/exam/hinh/%s" % m
                                     for k, m in (cau.get("hinh_phuong_an") or {}).items()}
        elif loai_cau == "TF":
            muc["phat_bieu"] = cau.get("phat_bieu") or {}
            muc["hinh_phat_bieu"] = {k: "/api/exam/hinh/%s" % m
                                     for k, m in (cau.get("hinh_phat_bieu") or {}).items()}
        elif loai_cau == "SA":
            pass  # chi can de_bai, hoc sinh tu go dap an
        else:
            muc["ghi_chu"] = (
                "Free-response question: work it out on paper and hand it to your teacher. "
                "Automatic grading of free-response questions is under construction."
                if ngon_ngu == "en" else
                "Câu tự luận — em làm ra giấy và nộp cho thầy/cô. "
                "Chức năng chấm tự luận tự động đang được xây dựng."
            )
        danh_sach_cau_hoi.append(muc)

    return {
        "success": True,
        "message": "",
        "data": {
            "de_id": de["id"],
            "tong_so_cau": len(danh_sach_cau_hoi),
            "cau_hoi": danh_sach_cau_hoi,
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
