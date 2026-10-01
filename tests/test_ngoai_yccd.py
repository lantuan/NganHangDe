"""Dạng "luyện tập thêm, ngoài YCCĐ" (docs/04 Ngoại lệ 4, cô Lan 01/10/2026).

- Dòng Mapping có "ngoai_yccd": true phải có ghi_chu bắt đầu "LUYEN TAP THEM" và được
  liệt kê trong "dang_luyen_tap_them" của đúng mục Curriculum (không tạo curriculum ID mới).
- tim_dang_ngoai_yccd nhận ra generator_id có hậu tố biến thể.
- Bộ chọn câu gắn cờ ngoai_yccd vào câu được chọn.
"""
import json
from pathlib import Path

from app.services.mapping_service import tim_dang_ngoai_yccd, la_ngoai_yccd

GOC = Path(__file__).resolve().parents[1] / "data"


def _tat_ca():
    for lop in (10, 11, 12):
        for f in sorted((GOC / "mapping" / ("toan%d" % lop)).glob("L*_C*.json")):
            cur = GOC / "curriculum" / ("toan%d" % lop) / f.name
            yield lop, json.loads(f.read_text(encoding="utf-8")), (
                json.loads(cur.read_text(encoding="utf-8")) if cur.exists() else [])


def test_dong_ngoai_yccd_co_ghi_chu_va_nam_trong_curriculum():
    co = 0
    for lop, mapping, cur in _tat_ca():
        theo_id = {r["id"]: r for r in cur}
        for r in mapping:
            if not la_ngoai_yccd(r):
                continue
            co += 1
            assert r.get("ghi_chu", "").startswith("LUYEN TAP THEM"), r["id"]
            cid = "_".join(r["id"].split("_")[:4])
            assert cid in theo_id, r["id"]
            ds = [g for d in theo_id[cid].get("dang_luyen_tap_them", []) for g in d["mapping_id"]]
            assert r["id"] in ds, r["id"]
    assert co >= 8


def test_tim_dang_ngoai_yccd():
    assert tim_dang_ngoai_yccd(10, 3, "L10_C3_B5_TH030_MC_E_02")["id"] == "L10_C3_B5_TH030_MC_E"
    assert tim_dang_ngoai_yccd(10, 3, "L10_C3_B5_TH030_MC_A_01") is None
    assert tim_dang_ngoai_yccd(10, None, "L10_C3_B5_TH030_MC_E_01") is None


def test_bo_chon_gan_co(monkeypatch):
    from app.services import question_selector_service as q
    bp = {"trac_nghiem": [{"curriculum_id": "L10_C3_B5_TH030", "muc_do": "TH", "tong_so_cau": 1,
                            "chuong_so": 3}]}
    thay = False
    for _ in range(60):
        ds = q.select_questions(lop=10, blueprint=bp, cho_phep_thieu=True)
        for c in ds:
            if c["generator_id"].startswith(("L10_C3_B5_TH030_MC_E", "L10_C3_B5_TH030_MC_F",
                                             "L10_C3_B5_TH030_MC_G")):
                assert c.get("ngoai_yccd") is True
                thay = True
            else:
                assert not c.get("ngoai_yccd")
    assert thay


def test_de_co_canh_bao_va_chu_thich_ban_gv(monkeypatch):
    from app.services import exam_assembler_service as a
    monkeypatch.setattr(a, "compile_pdf", lambda p: str(p).replace(".tex", ".pdf"))
    ds = [{"generator_id": "L10_C3_B5_TH030_MC_E", "chuong_so": 3, "loai_cau": "trac_nghiem"},
          {"generator_id": "L10_C3_B5_TH030_MC_A", "chuong_so": 3, "loai_cau": "trac_nghiem"}]
    kq = a._sinh_pdf_tu_danh_sach(10, "De thu", "teacher", ds, 1)
    cb = kq["canh_bao_ngoai_yccd"]
    assert len(cb) == 1 and cb[0]["phan"] == "I" and cb[0]["cau"] == 1
    assert cb[0]["generator_id"].startswith("L10_C3_B5_TH030_MC_E")
    tex = Path(kq["tex_path"]).read_text(encoding="utf-8")
    assert tex.count("LUU Y GIAO VIEN") == 1
    kq_hs = a._sinh_pdf_tu_danh_sach(10, "De thu", "student", ds, 1)
    assert "LUU Y GIAO VIEN" not in Path(kq_hs["tex_path"]).read_text(encoding="utf-8")
    assert len(kq_hs["canh_bao_ngoai_yccd"]) == 1
