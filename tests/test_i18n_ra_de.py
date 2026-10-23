"""Trang /gv/ra-de ở tiếng Anh (cô Lan 23/10/2026: "tên đã chuyển sang tiếng Anh được rồi, sao phần có phần không"):
loại kiểm tra trong ô chọn, tên BÀI trong bảng ma trận theo bài, cột "Vận dụng"."""
import json
from pathlib import Path

from app.routers.teacher import KI_THI_HIEN_THI
from app.services import i18n_service as I
from app.services.exam_scope_service import _load_ppct

GOC = Path(__file__).resolve().parent.parent


def test_loai_kiem_tra_co_ban_dich():
    td = I.tu_dien("en")
    for _ma, nhan in KI_THI_HIEN_THI:
        assert nhan in td and not I.CO_DAU.search(td[nhan]), nhan
    assert I.dich_html("<option>Giữa kỳ 1 (hệ số 2)</option>", "en") == "<option>Midterm 1 (weight 2)</option>"


def test_moi_ten_bai_lop_10_11_12_co_ban_dich():
    bd = I.ten_bai_dich("en")
    ax = json.loads((GOC / "data/ly_thuyet/anh_xa.json").read_text(encoding="utf-8"))["anh_xa"]
    ten = {b.get("bai") for lop in (10, 11, 12) for b in _load_ppct(lop)} | {v["ten_bai"] for v in ax.values()}
    thieu = sorted(t for t in ten if t and t not in bd)
    assert not thieu, thieu
    for v in bd.values():
        assert not I.CO_DAU.search(v) and not any(c in v for c in "\"`<>{}\\$"), v


def test_dich_json_ten_bai_nguyen_ten():
    goi = {"data": {"bai": [{"ten_bai": "Mệnh đề"}, {"ten_bai": "Tên lạ chưa có"}], "chuong": [{"ten_chuong": "x"}]}}
    en = I.dich_json(goi, "en")
    assert en["data"]["bai"][0]["ten_bai"] == "Statements"
    assert en["data"]["bai"][1]["ten_bai"] == "Tên lạ chưa có"                  # chưa có thì giữ nguyên
    assert I.dich_json(goi, "vi") == goi


def test_ten_bai_ngan_khong_vao_tu_dien_chung():
    # "Hàm số", "Khoảng cách"... nằm trong tệp riêng, không bị dịch nửa vời trong đoạn văn khác
    assert "Khoảng cách" not in I.tu_dien("en") or I.tu_dien("en")["Khoảng cách"] != "Distance"
    assert not (GOC / "data/i18n/en_ten_bai.json").exists()


def test_cot_van_dung_dich_duoc():
    html = (GOC / "app/templates/teacher/ra_de.html").read_text(encoding="utf-8")
    assert "<th>VD</th>" not in html and "<th>Vận dụng</th>" in html
    assert I.tu_dien("en")["Vận dụng"] == "Apply"
