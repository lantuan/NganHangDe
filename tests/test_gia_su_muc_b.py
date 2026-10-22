"""Gia sư AI - MỨC B (cô Lan 22/10/2026): học sinh hỏi tiếp "tập rỗng là tập gì" ở câu giải phương trình chứa căn thì
bị từ chối vì Mức A chỉ cho AI dùng đề + đáp án + lời giải mẫu. Nay AI được dùng THÊM đúng đoạn tài liệu lí thuyết
của cô (data/ly_thuyet, tra qua anh_xa.json) - vẫn không tự tính, không kiến thức ngoài tài liệu.
"""
import re

import pytest

from app.services import gia_su_service as G
from app.services import ly_thuyet_service as L

PT_CAN = "L10_C6_B18_TH001_MC_A"          # câu giải phương trình chứa căn (ảnh cô Lan gửi)


def _cac_tep():
    return sorted({t for bai in L._anh_xa().values() for t in bai["tep"]})


# ---------------------------------------------------------------- đọc tài liệu
def test_moi_tep_lop_10_deu_cat_duoc_muc_ly_thuyet():
    tep = _cac_tep()
    assert len(tep) == 28
    for t in tep:
        khoi = L.cac_khoi_cua_tep(t)
        assert khoi, t
        assert sum(len("\n".join(d)) for _m, d in khoi) > 300, t


@pytest.mark.parametrize("t", _cac_tep())
def test_lam_sach_khong_vo_cong_thuc(t):
    for ten, dong in L.cac_khoi_cua_tep(t):
        for d in [ten, *dong]:
            ngoai = re.sub(r"\$\$.*?\$\$", "", d)
            assert ngoai.count("$") % 2 == 0, (t, d)                    # mỗi dòng đủ cặp $...$
            assert "tikz" not in d and "\\indam" not in d and "\\immini" not in d, (t, d)
            assert not re.search(r"\\(begin|end)\{(itemize|enumerate|listEX|boxkn|khung\d*|tcolorbox)\}", d), (t, d)
            ngoai_toan = re.sub(r"\$\$.*?\$\$|\$[^$]*\$|\\begin\{(\w+\*?)\}.*?\\end\{\1\}", "", d)
            assert "{" not in ngoai_toan and "}" not in ngoai_toan, (t, d)


def test_dinh_nghia_tap_rong_co_trong_tai_lieu():
    noi = "\n".join(d for _m, khoi in L.cac_khoi_cua_tep("0D1-CD2.tex") for d in khoi)
    assert "Tập rỗng: là tập hợp không chứa phần tử nào, kí hiệu $\\varnothing $." in noi


# ---------------------------------------------------------------- tìm đúng chỗ
@pytest.mark.parametrize("qid, cau, bai, muc, chu", [
    (PT_CAN, "tập rỗng là tập gì", "L10_C1_B2", "Nhắc lại về tập hợp", "Tập rỗng"),
    ("L10_C3_B6_NB034_MC_A_01", "định lý sin là gì", "L10_C3_B6", "Định lý sin", "2R"),
    ("L10_C8_B24_TH001_MC_A", "tổ hợp chập k là gì", "L10_C8_B24", "Tổ hợp", "tổ hợp chập"),
    ("L10_C7_B19_NB001_MC_A", "vectơ pháp tuyến là gì", "L10_C7_B19", None, "pháp tuyến"),
    ("L10_C1_TF_B_02", "tập con là gì", "L10_C1_B2", "Tập con và hai tập hợp bằng nhau", "tập con"),
    (PT_CAN, "vì sao phải thử lại nghiệm", "L10_C6_B18", None, "Thay từng nghiệm"),
])
def test_tim_dung_doan(qid, cau, bai, muc, chu):
    doan = L.tim_doan(qid, cau, dang_hoi_tiep=True)
    assert doan, cau
    dau = doan[0]
    assert dau["ma_bai"] == bai and (muc is None or dau["muc"] == muc) and chu in dau["noi_dung"], (cau, doan)
    assert sum(len(d["noi_dung"]) for d in doan) <= L.TOI_DA_KY_TU + 600 and len(doan) <= L.TOI_DA_DOAN


def test_tu_le_khong_keo_sang_bai_khac():
    # "thử" trùng "phép thử" (xác suất) - từ lẻ ở bài khác không được lấy
    assert all(d["ma_bai"] == "L10_C6_B18" for d in L.tim_doan(PT_CAN, "vì sao phải thử lại nghiệm", True))


@pytest.mark.parametrize("cau", ["Giảng lại PHẦN I câu 2 cho em, em chưa hiểu.", "em vẫn chưa hiểu", "ok"])
def test_cau_chung_chung_lan_dau_khong_nap_tai_lieu(cau):
    assert L.tim_doan(PT_CAN, cau, dang_hoi_tiep=False) == []


def test_hoi_tiep_chung_chung_nap_muc_ly_thuyet_cua_bai():
    doan = L.tim_doan(PT_CAN, "em vẫn chưa hiểu", dang_hoi_tiep=True)
    assert doan and {d["ma_bai"] for d in doan} == {"L10_C6_B18"}
    assert sum(len(d["noi_dung"]) for d in doan) <= L.TOI_DA_KY_TU_CA_MUC


def test_id_la_hoac_khong_co_tai_lieu():
    assert L.tim_doan(None, "tập rỗng") == [] and L.tim_doan("abc", "tập rỗng") == []
    assert L.tim_doan("L11_C1_B1_NB001_MC_A", "tập rỗng", True) == []        # lớp 11 chưa ánh xạ


# ---------------------------------------------------------------- câu lệnh
NGU_CANH = {"de_bai": "Giải phương trình $\\sqrt{2x^2-3x-16}=x-2$.", "dap_an": "C. $S=\\{4\\}$",
            "loi_giai": "Bình phương hai vế ... Vậy $S=\\{4\\}$.", "question_id": PT_CAN}


def test_muc_a_giu_nguyen_khi_khong_co_tai_lieu():
    p = G.dung_lenh(NGU_CANH, "vì sao bình phương")
    assert p["muc"] == "A" and "TÀI LIỆU LÍ THUYẾT" not in p["lenh_he_thong"]
    assert "Nếu lời giải mẫu không nói tới điều học sinh hỏi" in p["lenh_he_thong"]


@pytest.mark.parametrize("lang, nhan", [("vi", "TÀI LIỆU LÍ THUYẾT CỦA THẦY/CÔ"), ("en", "THEORY NOTES")])
def test_muc_b_dua_doan_tai_lieu_va_van_khoa(lang, nhan):
    doan = L.tim_doan(PT_CAN, "tập rỗng là tập gì", True)
    p = G.dung_lenh(NGU_CANH, "tập rỗng là tập gì", [{"vai": "ai", "noi": "..."}], lang, doan)
    lenh = p["lenh_he_thong"]
    assert p["muc"] == "B" and nhan in lenh
    assert "không chứa phần tử nào" in lenh and "Tập hợp và các phép toán trên tập hợp" in lenh
    assert ("KHÔNG TỰ TÍNH TOÁN" in lenh) if lang == "vi" else ("DO NOT DO ANY CALCULATION" in lenh)
    assert (G.CAU_TU_CHOI if lang == "vi" else G.CAU_TU_CHOI_EN) in lenh       # ngoài cả hai nguồn: vẫn từ chối
    assert NGU_CANH["loi_giai"] in lenh


def test_hoi_tra_ve_doan_tai_lieu_cho_giao_dien(monkeypatch):
    goi = []
    monkeypatch.setattr(G, "lay_ngu_canh_cau", lambda *a, **k: dict(NGU_CANH))
    monkeypatch.setattr(G, "_cac_cau_da_lam", lambda uid, de: {1})
    monkeypatch.setattr(G, "lay_luot", lambda uid: {"da_dung": 0, "gioi_han": 5, "con_lai": 5})
    monkeypatch.setattr(G, "tru_luot", lambda uid: None)
    monkeypatch.setattr(G, "ghi_nhat_ki", lambda *a, **k: None)
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: goi.append(p) or "Tập rỗng là tập hợp không chứa phần tử nào.")
    kq = G.hoi("u1", "d1", 1, "tập rỗng là tập gì", [{"vai": "ai", "noi": "..."}])
    assert goi[0]["muc"] == "B" and kq["ly_thuyet"] and kq["ly_thuyet"][0]["ma_bai"] == "L10_C1_B2"
    kq = G.hoi("u1", "d1", 1, "Giảng lại PHẦN I câu 1 cho em, em chưa hiểu.")
    assert goi[1]["muc"] == "A" and kq["ly_thuyet"] == []


def test_giao_dien_hien_doan_tai_lieu():
    from pathlib import Path
    goc = Path(__file__).resolve().parent.parent / "app/templates/chat"
    chat = (goc / "chat.html").read_text(encoding="utf-8")
    lam = (goc / "lam_bai.html").read_text(encoding="utf-8")
    assert "html += htmlLyThuyet(d.ly_thuyet);" in chat
    assert "renderMarkdownAI(d.tra_loi) + htmlLyThuyet(d.ly_thuyet)" in chat
    assert "veLyThuyet(soThuTu, d.ly_thuyet);" in lam
    for html in (chat, lam):
        assert "function htmlLyThuyet(ds)" in html and 'replace(/&/g, "&amp;")' in html


# ---------------------------------------------------------------- chỉ chương đã học (cô Lan 22/10/2026)
def test_chi_tim_trong_cac_chuong_da_hoc():
    """Ảnh cô Lan: hỏi "tập rỗng là tập gì" ở câu Chương 6 ra thêm đoạn "Tổ hợp" (Chương 8, chưa học)."""
    doan = L.tim_doan(PT_CAN, "tập rỗng là tập gì", True)
    assert doan and doan[0]["ma_bai"] == "L10_C1_B2"                        # Chương 1 đã học: vẫn có định nghĩa
    assert all(L._so_chuong(d["ma_bai"]) <= 6 for d in doan), doan
    assert not any("Tổ hợp" in d["muc"] for d in doan)


@pytest.mark.parametrize("qid, cau", [("L10_C1_B2_NB001_MC_A", "tổ hợp chập k là gì"),
                                      ("L10_C3_B5_NB001_MC_A", "vectơ pháp tuyến là gì"),
                                      ("L10_C1_TF_B_02", "định lý sin là gì")])
def test_khong_lay_chuong_chua_hoc(qid, cau):
    chuong = L._so_chuong(qid)
    assert all(L._so_chuong(d["ma_bai"]) <= chuong for d in L.tim_doan(qid, cau, True))
