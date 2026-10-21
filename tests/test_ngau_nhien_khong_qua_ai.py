"""
Tinh ngau nhien cua de KHONG phu thuoc vao cac AI tren n8n (co Lan hoi 21/10/2026).

GenerateExam_RequestParser chi xuat CAU TRUC de (lop, chuong, ki thi, so cau, ti le muc do).
Mo hinh hay tra lai Y HET mot JSON cho cung mot yeu cau, nen phai bao dam:
  1. API sinh de khong co truong hat giong nao de AI (hay Ghep_Tham_So) dien vao;
     gui thua "seed" thi bi bo qua.
  2. Cung mot JSON cau truc gui nhieu lan -> moi lan mot bo cau va mot bo so lieu khac.
  3. Prompt cua cac AI tren n8n co ban ghi trong data/prompts (docs/18_PROMPT_LIBRARY.md).
"""

import hashlib
import secrets
from pathlib import Path

from app.routers.exam import GenerateExamAutoRequest
from app.services.exam_blueprint_service import build_blueprint
from app.services.generator_service import call_generator, dat_hat_giong
from app.services.question_selector_service import select_questions

GOC = Path(__file__).resolve().parent.parent

# Dung dang JSON ma chat.html (xacNhanTaoDe) / Ghep_Tham_So ghep tu dau ra cua RequestParser (bang HeSo1).
TY_LE = {"NB": 40, "TH": 30, "VD": 20, "VDC": 10}
CAU_TRUC = {
    "trac_nghiem": {"so_luong": 6, "ty_le_muc_do": TY_LE},
    "dung_sai_cau_lon": {"so_luong": 1},
    "tra_loi_ngan": {"so_luong": 2, "ty_le_muc_do": TY_LE},
    "tu_luan": {"so_luong": 3, "ty_le_muc_do": TY_LE},
}


def test_api_sinh_de_khong_nhan_hat_giong_tu_ngoai():
    for ten in GenerateExamAutoRequest.model_fields:
        assert "seed" not in ten and "hat_giong" not in ten, ten
    yeu_cau = GenerateExamAutoRequest(lop=10, tieu_de="De", role="student", loai_he_so="HeSo1", seed=1)
    assert "seed" not in yeu_cau.model_dump()


def _mot_lan_sinh(chuong: str) -> tuple:
    bp = build_blueprint(lop=10, loai_he_so="HeSo1", ki_thi="kiem_tra_thuong_xuyen",
                         pham_vi_chuong=chuong, cau_truc_tu_hoc_sinh=CAU_TRUC)
    ds = select_questions(lop=10, blueprint=bp, cho_phep_thieu=True)
    dat_hat_giong(secrets.randbelow(2 ** 31))          # nhu _sinh_pdf_tu_danh_sach
    noi_dung = ""
    for x in ds:
        if x.get("thieu"):
            continue
        noi_dung += call_generator(generator_id=x["generator_id"], lop=10, chuong_so=x["chuong_so"],
                                   role="student", socau_yeu_cau=1, used_variants={})["latex_block"]
    return tuple(x.get("generator_id") for x in ds), hashlib.md5(noi_dung.encode()).hexdigest()


def test_cung_json_cau_truc_ra_de_khac_nhau():
    for chuong in ("chuong_1", "chuong_3"):
        ket_qua = [_mot_lan_sinh(chuong) for _ in range(5)]
        so_bo_so_lieu = len({so for _ids, so in ket_qua})
        so_bo_cau = len({ids for ids, _so in ket_qua})
        assert so_bo_so_lieu == 5, (chuong, ket_qua)
        assert so_bo_cau >= 3, (chuong, ket_qua)


def test_prompt_cac_ai_tren_n8n_co_ban_ghi():
    for ten in ("CHV_Fun", "GenerateExam_RequestParser", "DocPhieuTraLoi", "CHV_Grader"):
        tep = GOC / "data" / "prompts" / (ten + ".md")
        assert tep.exists(), tep
        assert "BẢN CHÍNH THỨC" in tep.read_text(encoding="utf-8"), tep
