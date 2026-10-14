"""Ma trận cụ thể THEO BÀI do giáo viên đặt (cô Lan 14/10/2026).

Tổng NB/TH/VD của đề; mỗi câu Đúng/Sai tự trừ 1 NB + 1 TH + 2 VD, mỗi câu Tự luận tự trừ 2 VD;
phần còn lại chia vào từng bài cho trắc nghiệm / trả lời ngắn; VDC = round(VD của MC+SA / 3).
"""
from collections import Counter

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import ma_tran_bai_service as MTB
from app.services.exam_blueprint_service import build_blueprint
from app.services.exam_rules_service import ExamRulesError
from app.services.question_selector_service import select_questions

# Tổng 2 NB, 8 TH, 8 VD. TF chương 3 = 1 (tự trừ 1 NB, 1 TH, 2 VD); TL chương 3 = 1 (tự trừ 2 VD);
# các ô MC+SA dùng 1 NB, 7 TH, 4 VD. Một câu tự luận có 2 ý (VD và VDC) nên đếm là 1 câu.
MT = {"tong": {"NB": 2, "TH": 8, "VD": 8}, "tf": {3: 1}, "tl": {3: 1},
      "o": {"L10_C3_B5": {"trac_nghiem": {"NB": 1, "TH": 2, "VD": 1}, "tra_loi_ngan": {"TH": 1}},
            "L10_C3_B6": {"trac_nghiem": {"TH": 3, "VD": 2}, "tra_loi_ngan": {"TH": 1, "VD": 1}}}}
FORM = {"ma_tran_bai": "1", "mtb_tong_nb": "2", "mtb_tong_th": "8", "mtb_tong_vd": "8",
        "mtb_tf_3": "1", "mtb_tl_3": "1", "mtb_tf_1": "0",
        "mtb_o_L10_C3_B5_mc_nb": "1", "mtb_o_L10_C3_B5_mc_th": "2", "mtb_o_L10_C3_B5_mc_vd": "1",
        "mtb_o_L10_C3_B5_sa_th": "1", "mtb_o_L10_C3_B5_sa_vd": "",
        "mtb_o_L10_C3_B6_mc_th": "3", "mtb_o_L10_C3_B6_mc_vd": "2",
        "mtb_o_L10_C3_B6_sa_th": "1", "mtb_o_L10_C3_B6_sa_vd": "1"}


def test_doc_form():
    assert MTB.doc_ma_tran_bai_tu_form({}) is None
    assert MTB.doc_ma_tran_bai_tu_form(FORM) == MT
    with pytest.raises(ExamRulesError):
        MTB.doc_ma_tran_bai_tu_form({**FORM, "mtb_tong_nb": "abc"})


def test_form_bang_ma_tran_khong_khai_tong_thi_tong_tu_tinh():
    """Bảng kiểu ma trận đề (cô Lan 14/10/2026): không có ô khai tổng; tổng = những gì cô đã điền."""
    form = {k: v for k, v in FORM.items() if not k.startswith("mtb_tong_")}
    mt = MTB.doc_ma_tran_bai_tu_form(form)
    assert mt["tong"] == {"NB": 2, "TH": 8, "VD": 8} and MTB.con_lai(mt) == {"NB": 0, "TH": 0, "VD": 0}
    assert MTB.kiem_tra_ma_tran_bai(mt, 10, ["L10_C3_B5", "L10_C3_B6"]) == []
    rong = MTB.doc_ma_tran_bai_tu_form({"ma_tran_bai": "1"})
    assert MTB.kiem_tra_ma_tran_bai(rong, 10, ["L10_C3_B5"]) == ["Chưa nhập số câu nào vào bảng ma trận."]


def test_tru_tf_tl_va_con_lai():
    assert MTB.da_dung(MT) == {"NB": 2, "TH": 8, "VD": 8}
    assert MTB.con_lai(MT) == {"NB": 0, "TH": 0, "VD": 0}
    assert MTB.so_vdc(MT) == 1                     # VD của ô = 4 -> round(4/3) = 1
    mt = {**MT, "tong": {"NB": 3, "TH": 8, "VD": 7}}
    assert MTB.con_lai(mt) == {"NB": 1, "TH": 0, "VD": -1}


def test_kiem_tra_bao_dung_o_lech():
    pv = ["L10_C3_B5", "L10_C3_B6"]
    assert MTB.kiem_tra_ma_tran_bai(MT, 10, pv) == []
    loi = MTB.kiem_tra_ma_tran_bai({**MT, "tong": {"NB": 3, "TH": 8, "VD": 7}}, 10, pv)
    assert any("Còn thiếu 1 câu NB" in x for x in loi) and any("phân dư 1 câu VD" in x for x in loi)
    assert MTB.kiem_tra_ma_tran_bai({"tong": {"NB": 0, "TH": 0, "VD": 0}, "tf": {}, "tl": {}, "o": {}}, 10, pv)
    ngoai = {**MT, "o": {**MT["o"], "L10_C1_B1": {"trac_nghiem": {}}}}
    assert any("không nằm trong phạm vi" in x for x in MTB.kiem_tra_ma_tran_bai(ngoai, 10, pv))
    # B6 chưa có hàm MC mức NB trong ngân hàng Python -> chặn, nêu rõ ô
    mt = {"tong": {"NB": 1, "TH": 0, "VD": 0}, "tf": {}, "tl": {},
          "o": {"L10_C3_B6": {"trac_nghiem": {"NB": 1}}}}
    loi = MTB.kiem_tra_ma_tran_bai(mt, 10, pv)
    assert loi and "L10_C3_B6" in loi[0] and "chưa có hàm" in loi[0]


def test_dem_theo_ham_python_khong_theo_dong_mapping():
    """Cô Lan 14/10/2026: số có sẵn = số hàm (dạng x biến thể) trong ngân hàng Python."""
    import re
    from app.services.mapping_service import PYTHON_BANK_DIR, load_mapping, phan_loai_cau
    ng = MTB.so_cau_ngan_hang(10, ["L10_C3_B5"])
    src = (PYTHON_BANK_DIR / "toan10" / "L10_C3.py").read_text(encoding="utf-8")
    ham = Counter(re.findall(r"^def (L\d+_[A-Za-z0-9_]+?)_\d{2}\s*\(", src, re.M))
    mong = sum(ham.get(r["id"], 0) for r in load_mapping(10, 3)
               if r["id"].startswith("L10_C3_B5_") and phan_loai_cau(r) == "trac_nghiem" and r["muc_do"] == "NB")
    assert ng["o"]["L10_C3_B5"]["trac_nghiem"]["NB"] == mong > 0
    assert ng["tf"][3] == sum(ham.get(r["id"], 0) for r in load_mapping(10, 3) if phan_loai_cau(r) == "dung_sai_cau_lon")


def test_dat_hon_so_ham_chi_canh_bao_khong_chan():
    pv = ["L10_C3_B5"]
    co = MTB.so_cau_ngan_hang(10, pv)["o"]["L10_C3_B5"]["tra_loi_ngan"]["NB"]
    mt = {"tong": {"NB": co + 1, "TH": 0, "VD": 0}, "tf": {}, "tl": {},
          "o": {"L10_C3_B5": {"tra_loi_ngan": {"NB": co + 1}}}}
    assert MTB.kiem_tra_ma_tran_bai(mt, 10, pv) == []
    cb = MTB.canh_bao_ma_tran_bai(mt, 10, pv)
    assert len(cb) == 1 and "lặp lại" in cb[0]


def test_khung_cho_form():
    kh = MTB.khung_ma_tran_bai(10, "HeSo1", None, "chuong_3")
    assert [b["bai_id"] for b in kh["bai"]] == ["L10_C3_B5", "L10_C3_B6"]
    assert kh["chuong"][0]["chuong_so"] == 3 and kh["chuong"][0]["tf_toi_da"] > 0
    assert set(kh["bai"][0]["toi_da"]) == {"trac_nghiem", "tra_loi_ngan"}
    assert kh["trong_so"] == {"MC": 3.0, "TF": 2.0, "SA": 2.0, "TL": 3.0} and kh["thang_diem"] == 10   # cột % điểm
    with pytest.raises(ExamRulesError):
        MTB.khung_ma_tran_bai(10, "HeSo1", None, None)


def test_endpoint_khung():
    r = TestClient(app).get("/api/exam/ma-tran-bai-khung", params={"lop": 10, "ki_thi": "thuong_xuyen",
                                                                   "pham_vi_chuong": "chuong_3"})
    assert r.status_code == 200 and r.json()["data"]["pham_vi_bai"] == ["L10_C3_B5", "L10_C3_B6"]


@pytest.mark.parametrize("seed", range(12))
def test_blueprint_va_chon_cau_dung_tung_o(seed):
    import random
    random.seed(seed)
    bp = build_blueprint(10, "HeSo1", None, "chuong_3", ma_tran_bai=MT)
    assert bp["nguon_cau_truc"] == "ma_tran_bai"
    ds = select_questions(10, bp, cho_phep_thieu=False)
    assert not [c for c in ds if c.get("thieu")]
    dem = Counter(c["loai_cau"] for c in ds)
    assert dem["dung_sai_cau_lon"] == 1 and dem["tu_luan"] == 1 and dem["trac_nghiem"] == 9 and dem["tra_loi_ngan"] == 3
    mc_sa = [c for c in ds if c["loai_cau"] in ("trac_nghiem", "tra_loi_ngan")]
    theo_o = Counter((c["curriculum_id"][:9], c["loai_cau"], c["muc_do"]) for c in mc_sa)
    for bai, loais in MT["o"].items():
        for loai, muc in loais.items():
            for m, n in muc.items():
                assert theo_o[(bai, loai, m)] == n, (bai, loai, m)
    assert sum(1 for c in mc_sa if c.get("muc_do_cau") == "VDC") == 1
