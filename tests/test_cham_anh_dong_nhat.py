"""
Dong nhat cac truong giua prompt n8n (DocPhieuTraLoi, CHV_Grader) va Python cham bang anh
(co Lan 21/10/2026: "dong nhat cac truong voi nhau, khong de mau thuan xay ra").

Gia lap hai webhook n8n bang monkeypatch, kiem:
- tra loi ngan: dau cham / dau phay / $...$ coi nhu nhau (chung voi cham tren web);
- cau Dung/Sai: "D"/"S" doc tu phieu duoc cham theo so y dung;
- tu luan: moi truong do Python dat, diem AI duoc ep so, chan, lam tron 0,25;
- JSON boc {"output": "```json ...```"} van doc duoc;
- ban ghi prompt trong data/prompts dung dung ten truong Python doc.
"""

import json
from pathlib import Path

import pytest

from app.services import diem_service
from app.services import grade_photo_service as G
from app.services.answer_parser_service import chuan_hoa_dap_an_ngan

GOC = Path(__file__).resolve().parent.parent

ID_MC = "L10_C3_B5_NB029_MC_A_01"
ID_TF = "L10_C3_TF_A_01"
ID_SA = "L10_C3_B5_NB029_SA_A_01"
ID_TL = "L10_C3_B6_VD036_TL_I_02"

DE = [
    {"so_thu_tu": 1, "loai_cau": "MC", "generator_id": ID_MC, "dap_an_dung": "B"},
    {"so_thu_tu": 2, "loai_cau": "TF", "generator_id": ID_TF,
     "dap_an_dung": {"a": True, "b": False, "c": True, "d": False}},
    {"so_thu_tu": 3, "loai_cau": "SA", "generator_id": ID_SA, "dap_an_dung": "$-5,5$"},
    {"so_thu_tu": 4, "loai_cau": "TL", "generator_id": ID_TL, "dap_an_dung": "", "loi_giai": "Heron ..."},
]


def _gia_lap(monkeypatch, doc_phieu, cham_tl):
    goi = []

    def gia(url, payload, ten_buoc):
        goi.append((ten_buoc, payload))
        return doc_phieu if ten_buoc == "doc-phieu-tra-loi" else cham_tl

    monkeypatch.setattr(G, "_goi_webhook", gia)
    return goi


@pytest.mark.parametrize("hs", ["-5.5", "-5,5", "$-5,5$", " -5 , 5 ", "-5{,}5", "−5,5"])
def test_tra_loi_ngan_dau_thap_phan_nhu_nhau(hs):
    assert chuan_hoa_dap_an_ngan(hs) == chuan_hoa_dap_an_ngan("$-5,5$")


def test_tra_loi_ngan_khac_so_van_sai():
    assert chuan_hoa_dap_an_ngan("-5,4") != chuan_hoa_dap_an_ngan("$-5,5$")
    assert chuan_hoa_dap_an_ngan("55") != chuan_hoa_dap_an_ngan("5,5")


def test_cham_anh_dong_nhat_moi_truong(monkeypatch):
    doc_phieu = {"mc": {"1": "b"}, "tf": {"1": {"a": "D", "b": "S", "c": "D", "d": "D"}}, "sa": {"1": "-5.5"}}
    # Dang n8n AI Agent hay tra: {"output": "<chuoi JSON trong ```json```>"}, ghi loai_cau, diem_toi_da sai.
    cham_tl = {"output": "```json\n" + json.dumps([{
        "question_id": ID_TL, "loai_cau": "tu_luan", "dung_sai_hoac_diem": "1,3", "diem_toi_da": 99,
        "nhan_xet": "Đúng công thức Heron.", "chuong": 9, "bai": 9, "tags": []}], ensure_ascii=False) + "\n```"}
    goi = _gia_lap(monkeypatch, doc_phieu, cham_tl)
    kq = G.cham_bai_bang_anh(DE, "anh_phieu", "anh_tl")
    thang = diem_service.tinh_thang_diem(DE)
    theo = {c["so_thu_tu"]: c for c in kq["chi_tiet"]}

    # Python gui dung khoa so_luong ma prompt DocPhieuTraLoi doc.
    assert goi[0][1]["so_luong"] == {"mc": 1, "tf": 1, "sa": 1}
    assert set(goi[1][1]["danh_sach_cau"][0]) == {"question_id", "bai", "diem_toi_da", "dap_an_mau", "chuong"}

    assert theo[1]["loai_cau"] == "MC" and theo[1]["dung_sai_hoac_diem"] is True
    assert theo[3]["loai_cau"] == "SA" and theo[3]["dung_sai_hoac_diem"] is True

    tf = theo[2]
    assert tf["loai_cau"] == "TF" and tf["so_y_dung"] == 3 and tf["dung_sai_hoac_diem"] is False
    assert tf["diem_dat_duoc"] == diem_service.diem_cau_tf(thang, 3)[1]
    assert "trang_thai" not in tf

    tl = theo[4]
    toi_da = diem_service.diem_toi_da_cua_cau_theo_id(thang, "TL", ID_TL)
    assert tl["loai_cau"] == "TL"                       # khong phai "tu_luan" cua AI
    assert tl["diem_toi_da"] == toi_da                  # khong phai 99 cua AI
    assert (tl["chuong"], tl["bai"]) != (9, 9)          # Python tu dat
    assert tl["dung_sai_hoac_diem"] == min(1.25, toi_da)
    assert tl["nhan_xet"] == "Đúng công thức Heron."

    tong = (diem_service.diem_toi_da_cua_cau(thang, "MC") + diem_service.diem_toi_da_cua_cau(thang, "SA")
            + tf["diem_dat_duoc"] + tl["dung_sai_hoac_diem"])
    assert kq["diem_tren_10_tam_tinh"] == pytest.approx(tong, abs=0.011)


@pytest.mark.parametrize("ai_cho, mong", [
    ({"diem": 100}, "toi_da"),                  # khoa cu "diem" van doc, chan tren
    ({"dung_sai_hoac_diem": -2}, 0.0),          # chan duoi
    ({"dung_sai_hoac_diem": 0.6}, 0.5),         # lam tron 0,25
    ({"dung_sai_hoac_diem": "khong ro"}, None),  # khong doc duoc -> cham tay
    ({}, None),
])
def test_diem_tu_luan_ai_duoc_ep_ve_thang(monkeypatch, ai_cho, mong):
    cham_tl = [dict({"question_id": ID_TL, "nhan_xet": ""}, **ai_cho)]
    _gia_lap(monkeypatch, {}, cham_tl)
    kq = G.cham_bai_bang_anh(DE, None, "anh_tl")
    tl = [c for c in kq["chi_tiet"] if c["so_thu_tu"] == 4][0]
    thang = diem_service.tinh_thang_diem(DE)
    toi_da = diem_service.diem_toi_da_cua_cau_theo_id(thang, "TL", ID_TL)
    if mong == "toi_da":
        mong = round(toi_da * 4) / 4
    assert tl["dung_sai_hoac_diem"] == mong
    if mong is None:
        assert tl["trang_thai"] == "loi_cham"


def test_json_hong_bao_loi_ro_rang(monkeypatch):
    _gia_lap(monkeypatch, {"output": "không phải JSON"}, [])
    with pytest.raises(G.GradePhotoError):
        G.cham_bai_bang_anh(DE, "anh_phieu", None)


def test_ban_ghi_prompt_dung_ten_truong_python_doc():
    doc = (GOC / "data/prompts/DocPhieuTraLoi.md").read_text(encoding="utf-8")
    for truong in ('"mc"', '"tf"', '"sa"', '"D"|"S"', '"-12,5"', "so_luong"):
        assert truong in doc, truong
    assert '"-12.5"' not in doc.split("\n---\n", 1)[1]       # phan prompt (sau khoi ghi chu)

    grader = (GOC / "data/prompts/CHV_Grader.md").read_text(encoding="utf-8")
    phan_prompt = grader.split("\n---\n", 1)[1]
    for truong in ('"question_id"', '"dung_sai_hoac_diem"', '"nhan_xet"', '"loai_cau": "TL"',
                   "question_id, bai, diem_toi_da, dap_an_mau, chuong"):
        assert truong in phan_prompt, truong
    assert "- diem:" not in phan_prompt and '"tu_luan"' not in phan_prompt
