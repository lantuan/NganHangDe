"""
Dong nhat cac truong GenerateExam_RequestParser (n8n) <-> may chu (co Lan 21/10/2026: "dong nhat cac
truong voi nhau, khong de mau thuan xay ra"). Doc THANG ban ghi prompt data/prompts/GenerateExam_RequestParser.md
nen sau nay sua prompt (them slug, doi ten truong) ma may chu chua theo thi test bao.
"""

import json
import re
from pathlib import Path

import pytest

from app.routers.exam import GenerateExamAutoRequest
from app.services.exam_blueprint_service import BlueprintError, build_blueprint

GOC = Path(__file__).resolve().parent.parent
PROMPT = (GOC / "data/prompts/GenerateExam_RequestParser.md").read_text(encoding="utf-8")


def _slug_ki_thi():
    phan = PROMPT.split("SLUG KỲ THI", 1)[1].split("QUY TẮC QUAN TRỌNG", 1)[0]
    return re.findall(r"^([a-z0-9_]+)$", phan, re.M)


def test_prompt_liet_ke_du_slug():
    assert len(_slug_ki_thi()) == 9


@pytest.mark.parametrize("slug", _slug_ki_thi())
def test_moi_slug_ki_thi_cua_prompt_may_chu_deu_nhan(slug):
    loai = "HeSo1" if slug.startswith("kiem_tra") else "HeSo2_HeSo3"
    bp = build_blueprint(lop=10, loai_he_so=loai, ki_thi=slug, pham_vi_chuong="chuong_1")
    assert bp


def test_hoc_ky_la_cuoi_ky():
    a = build_blueprint(lop=10, loai_he_so="HeSo2_HeSo3", ki_thi="hoc_ky_1")
    b = build_blueprint(lop=10, loai_he_so="HeSo2_HeSo3", ki_thi="cuoi_ky_1")
    assert a["pham_vi_bai"] and a["pham_vi_bai"] == b["pham_vi_bai"]


@pytest.mark.parametrize("chuong", ["chua_xac_dinh", "chương 2", "null"])
def test_chuong_chua_ro_bao_loi_ro_rang(chuong):
    with pytest.raises(BlueprintError, match="Chưa rõ chương"):
        build_blueprint(lop=10, loai_he_so="HeSo1", ki_thi="kiem_tra_thuong_xuyen", pham_vi_chuong=chuong)


def test_ki_thi_la_bao_loi_ro_rang():
    with pytest.raises(BlueprintError, match="giữa kỳ hay cuối kỳ"):
        build_blueprint(lop=10, loai_he_so="HeSo2_HeSo3", ki_thi="kiem_tra_dinh_ky")


def test_ten_truong_cau_truc_trung_voi_exam_rules():
    rules = json.loads((GOC / "data/config/exam_rules.json").read_text(encoding="utf-8"))
    khoa_prompt = set(re.findall(r'^\s*"(trac_nghiem|dung_sai_cau_lon|tra_loi_ngan|tu_luan|\w+)": <số>', PROMPT, re.M))
    assert {"trac_nghiem", "dung_sai_cau_lon", "tra_loi_ngan", "tu_luan"} <= khoa_prompt
    assert {"NB", "TH", "VD", "VDC"} <= khoa_prompt
    for loai in ("HeSo1", "HeSo2_HeSo3"):
        assert loai in PROMPT
        assert set(rules[loai]) >= {"trac_nghiem", "dung_sai_cau_lon", "tra_loi_ngan", "tu_luan"}
    # Cac truong prompt xuat ma API sinh de doc
    for truong in ("lop", "loai_he_so", "ki_thi", "pham_vi_chuong"):
        assert '"%s"' % truong in PROMPT and truong in GenerateExamAutoRequest.model_fields
