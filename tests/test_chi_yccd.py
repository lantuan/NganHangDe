"""Nút "Phạm vi câu hỏi" ở trang ra đề giáo viên (cô Lan 15/10/2026).

"Cho thêm câu ngoài YCCĐ" (mặc định, như cũ): mọi dạng đều được chọn, câu luyện tập thêm có cảnh báo.
"Chỉ theo YCCĐ" (chi_yccd): bảng ma trận theo bài KHÔNG đếm dạng luyện tập thêm ("ngoai_yccd": true),
blueprint không chọn đơn vị chỉ có dạng luyện tập thêm, bộ chọn câu không chọn dạng luyện tập thêm.
"""
import random
from collections import Counter

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import ma_tran_bai_service as MTB
from app.services.exam_blueprint_service import BlueprintError, build_blueprint
from app.services.mapping_service import la_ngoai_yccd, load_mapping
from app.services.question_selector_service import select_questions

NGOAI = {r["id"] for c in (1, 2, 3, 4) for r in load_mapping(10, c) if la_ngoai_yccd(r)}


def _la_ngoai(gid: str) -> bool:
    return any(gid == i or gid.startswith(i + "_") for i in NGOAI)


def test_co_dang_ngoai_yccd_de_kiem():
    assert any("_B6_NB03" in i for i in NGOAI) and any("_B5_VD030_" in i for i in NGOAI)


def test_bang_ma_tran_bo_cau_ngoai_yccd():
    co = MTB.so_cau_ngan_hang(10, ["L10_C3_B5", "L10_C3_B6"])
    chi = MTB.so_cau_ngan_hang(10, ["L10_C3_B5", "L10_C3_B6"], chi_yccd=True)
    # Bai 6 muc Biet chi co dang luyen tap them (NB032-NB034)
    assert co["o"]["L10_C3_B6"]["trac_nghiem"]["NB"] > 0 and co["o"]["L10_C3_B6"]["tra_loi_ngan"]["NB"] > 0
    assert chi["o"]["L10_C3_B6"]["trac_nghiem"]["NB"] == 0 and chi["o"]["L10_C3_B6"]["tra_loi_ngan"]["NB"] == 0
    # Bai 5 muc VD: VD030, VD031 la luyen tap them -> chi con it hon
    assert chi["o"]["L10_C3_B5"]["trac_nghiem"]["VD"] < co["o"]["L10_C3_B5"]["trac_nghiem"]["VD"]
    # khong o nao tang len
    for b in co["o"]:
        for l in co["o"][b]:
            for m in co["o"][b][l]:
                assert chi["o"][b][l][m] <= co["o"][b][l][m]


def test_endpoint_khung_nhan_tham_so():
    c = TestClient(app)
    p = {"lop": 10, "ki_thi": "thuong_xuyen", "pham_vi_chuong": "chuong_3"}
    r0 = c.get("/api/exam/ma-tran-bai-khung", params=p).json()["data"]
    r1 = c.get("/api/exam/ma-tran-bai-khung", params={**p, "chi_yccd": 1}).json()["data"]
    b6 = lambda d: next(b for b in d["bai"] if b["bai_id"] == "L10_C3_B6")["toi_da"]
    assert r0["chi_yccd"] is False and r1["chi_yccd"] is True
    assert b6(r0)["trac_nghiem"]["NB"] > 0 and b6(r1)["trac_nghiem"]["NB"] == 0


def test_ma_tran_dat_o_chi_co_ngoai_yccd_thi_chan():
    mt = {"tong": {"NB": 1, "TH": 0, "VD": 0}, "tf": {}, "tl": {},
          "o": {"L10_C3_B6": {"trac_nghiem": {"NB": 1}}}}
    assert MTB.kiem_tra_ma_tran_bai(mt, 10, ["L10_C3_B5", "L10_C3_B6"]) == []
    loi = MTB.kiem_tra_ma_tran_bai(mt, 10, ["L10_C3_B5", "L10_C3_B6"], chi_yccd=True)
    assert loi and "L10_C3_B6" in loi[0] and "YCCĐ" in loi[0]
    with pytest.raises(BlueprintError):
        build_blueprint(10, "HeSo1", None, "chuong_3", ma_tran_bai=mt, chi_yccd=True)


@pytest.mark.parametrize("pham_vi", [("HeSo1", None, "chuong_3"), ("HeSo2_HeSo3", "giua_ky_1", None)])
def test_chi_yccd_khong_ra_cau_luyen_tap_them(pham_vi):
    he_so, ki, chuong = pham_vi
    co_ngoai = 0
    for sd in range(25):
        random.seed(sd)
        bp = build_blueprint(10, he_so, ki, chuong, chi_yccd=True)
        assert bp["chi_yccd"] is True
        ds = select_questions(10, bp, cho_phep_thieu=True)
        assert not [c["generator_id"] for c in ds if c.get("generator_id") and _la_ngoai(c["generator_id"])]
        assert not [c for c in ds if c.get("ngoai_yccd")]
        random.seed(sd)
        bp0 = build_blueprint(10, he_so, ki, chuong)
        assert bp0["chi_yccd"] is False
        co_ngoai += sum(1 for c in select_questions(10, bp0, cho_phep_thieu=True) if c.get("ngoai_yccd"))
    assert co_ngoai > 0          # mac dinh (cho them) van co the ra cau luyen tap them


def test_ma_tran_theo_bai_chi_yccd():
    mt = {"tong": {"NB": 2, "TH": 4, "VD": 3}, "tf": {}, "tl": {},
          "o": {"L10_C3_B5": {"trac_nghiem": {"NB": 2, "TH": 2}},          # Bai 5 muc VD chi co VD030, VD031 (luyen tap them)
                "L10_C3_B6": {"trac_nghiem": {"TH": 2, "VD": 3}}}}
    for sd in range(20):
        random.seed(sd)
        bp = build_blueprint(10, "HeSo1", None, "chuong_3", ma_tran_bai=mt, chi_yccd=True)
        ds = select_questions(10, bp, cho_phep_thieu=False)
        assert len(ds) == 9 and not [c for c in ds if c.get("ngoai_yccd") or _la_ngoai(c["generator_id"])]
        assert Counter(c["muc_do"] for c in ds) == Counter({"NB": 2, "TH": 4, "VD": 3})


@pytest.mark.parametrize("gia_tri,mong", [("1", True), ("0", False), (None, False)])
def test_form_giao_vien_truyen_co_chi_yccd(monkeypatch, tmp_path, gia_tri, mong):
    from app.routers import teacher as router_gv

    class UserGia:
        id = "99999999-9999-9999-9999-999999999999"
        email = "co@example.com"

    goi, da_luu = {}, {}
    tep = tmp_path / "de.pdf"
    tep.write_bytes(b"%PDF-1.4")
    tex = tmp_path / "de.tex"
    tex.write_text("x")

    def gia_generate(**kw):
        goi.update(kw)
        return {"pdf_path": str(tep), "tex_path": str(tex), "pdf_loigiai_path": None, "dap_an_json_path": None,
                "so_cau_da_sinh": 1, "so_cau_thieu": 0, "danh_sach_generator_id": []}

    monkeypatch.setattr(router_gv, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_gv, "yeu_cau_giao_vien", lambda request, user=None: None)
    monkeypatch.setattr(router_gv, "generate_exam_pdf_auto", gia_generate)
    monkeypatch.setattr(router_gv.history_service, "luu_de_da_sinh", lambda **kw: da_luu.update(kw) or "de-id")
    monkeypatch.setattr(router_gv.history_service, "luu_file_de", lambda *a, **k: None)
    data = {"lop": 10, "ki_thi": "thuong_xuyen", "pham_vi_chuong": "chuong_3", "socau_ma_de": 1, "tieu_de": "DE"}
    if gia_tri is not None:
        data["chi_yccd"] = gia_tri
    res = TestClient(app).post("/gv/ra-de", data=data, follow_redirects=False)
    assert res.status_code == 303
    assert goi["chi_yccd"] is mong and da_luu["blueprint"]["chi_yccd"] is mong


def test_trang_ra_de_co_nut_chon():
    from pathlib import Path
    html = (Path(__file__).resolve().parents[1] / "app" / "templates" / "teacher" / "ra_de.html").read_text(encoding="utf-8")
    assert 'name="chi_yccd" type="radio" value="0" checked' in html and 'name="chi_yccd" type="radio" value="1"' in html
    assert "chi_yccd: chiYccd" in html
