"""Phạm vi khung chat (cô Lan 23/10/2026): chat tự tính "7 x 7 = 49", rủ "tạo đề ôn bảng cửu chương", học sinh đồng ý
("vâng. tạo cho tôi", "bảng cửu chương mà", "mấy cũng được. miễn tôi rèn luyện được") thì AI hỏi lại mãi mà không làm
được. Chốt: đề chỉ theo ngân hàng đề của thầy/cô (Toán THPT 10-12), kiến thức chỉ theo tài liệu lí thuyết thầy/cô
đưa. Xem app/services/pham_vi_service.py."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat as C
from app.services import gia_su_service as GS
from app.services import i18n_service as I
from app.services import pham_vi_service as P
from app.services import tro_chuyen_service as T


@pytest.mark.parametrize("cau, ly_do", [
    ("bảng cửu chương mà", "cuu_chuong"), ("tạo đề bảng cửu chương", "cuu_chuong"),
    ("7 nhân 7 bằng mấy", "tinh_toan"), ("7x7=?", "tinh_toan"), ("tính 15 + 27", "tinh_toan"),
    ("cho tôi đề toán lớp 5", "lop_duoi"), ("dạy tôi toán THCS", "lop_duoi"),
    ("dạy tôi vật lý", "mon_khac"), ("tôi muốn ôn môn hóa", "mon_khac"),
])
def test_ngoai_pham_vi(cau, ly_do):
    assert P.ngoai_pham_vi(cau) == ly_do


@pytest.mark.parametrize("cau", ["mình thích môn văn hơn", "xin chào", "tôi được 7 điểm", "giải phương trình 2x+1=0",
                                 "cho tôi đề lớp 10 chương 2", "tôi học lớp 10", "cho tôi đề tiếng Anh lớp 10 chương 1",
                                 "tập rỗng là gì"])
def test_khong_chan_nham(cau):
    assert P.ngoai_pham_vi(cau) is None


@pytest.mark.parametrize("cau", ["vâng. tạo cho tôi", "mấy cũng được. miễn tôi rèn luyện được", "tạo đề lớp 10",
                                 "cho em đề kiểm tra 15 phút", "create a test"])
def test_muon_de_chua_noi_chuong(cau):
    assert P.muon_de_chung_chung(cau)


@pytest.mark.parametrize("cau", ["cho tôi đề lớp 10 chương 2", "Lớp 10, thi giữa kỳ 1", "tạo đề hàm số bậc hai",
                                 "tạo đề về phương trình bậc hai", "ôn tập xác suất", "give me an exam on vectors",
                                 "tôi không biết cách tạo đề", "cho tôi lời giải", "em đang yếu hàm số",
                                 "đề vừa rồi khó quá", "tôi cần đề luyện tập thêm chương 3, phần tự luận"])
def test_da_noi_ro_thi_de_n8n(cau):
    assert not P.muon_de_chung_chung(cau)


def test_danh_sach_chuong_chi_chuong_co_ngan_hang():
    assert [c for c, _t in P.danh_sach_chuong(10)] == list(range(1, 10))
    assert [c for c, _t in P.danh_sach_chuong(12)] == [2, 6]                  # lớp 12 mới có chương 2, 6
    vi = P.tra_loi_ngoai_pham_vi("cuu_chuong", 10)
    assert "Bảng cửu chương" in vi and "1. Mệnh đề và tập hợp" in vi and "đề chương 3" in vi
    en = P.tra_loi_chon_chuong("tạo đề lớp 11", 10, "en")
    assert "Grade 11" in en and not I.CO_DAU.search(en)
    assert "lớp (ví dụ" in P.tra_loi_chon_chuong("vâng. tạo cho tôi", None)  # không biết lớp thì hỏi lớp


def test_lenh_tro_chuyen_khoa_pham_vi(monkeypatch):
    goi = []
    monkeypatch.setattr(GS, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(GS, "_goi_mo_hinh", lambda p: goi.append(p) or "ok")
    T.tro_chuyen("chào", lop=10)
    lenh = goi[0]["lenh_he_thong"]
    assert "Chương 4. Vectơ" in lenh and "bảng cửu chương" in lenh and "kể cả phép tính dễ" in lenh
    assert "Lớp 11" not in lenh


class _U:
    id = "99999999-9999-9999-9999-999999999999"


@pytest.fixture
def chat_gia(monkeypatch, tmp_path):
    from app.services import tuy_chon_de_service as TC

    def _khong(*a, **k):
        raise AssertionError("không được gọi n8n")
    monkeypatch.setattr(TC, "TEP", tmp_path / "tc.json")
    monkeypatch.setattr(C, "get_current_user", lambda request: _U)
    monkeypatch.setattr(C.profile_service, "lay_vai_tro", lambda uid: "hoc_sinh")
    monkeypatch.setattr(C.supabase_service, "lay_lop_hoc_sinh", lambda uid: {"khoi": "10", "lop": "C9"})
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: None)
    monkeypatch.setattr(C, "_goi_n8n", _khong)
    monkeypatch.setattr(GS, "_goi_mo_hinh", _khong)
    luu = []
    monkeypatch.setattr(C.history_service, "luu_tin_nhan", lambda **kw: luu.append(kw))
    return luu


def _gui(cau):
    return TestClient(app).post("/chat", data={"message": cau, "conversation_id": "h"}).json()


@pytest.mark.parametrize("cau, loai", [("bảng cửu chương mà", "ngoai_pham_vi"), ("7x7=?", "ngoai_pham_vi"),
                                       ("vâng. tạo cho tôi", "chon_chuong"),
                                       ("mấy cũng được. miễn tôi rèn luyện được", "chon_chuong")])
def test_chat_tra_loi_ngay_khong_goi_ai(chat_gia, cau, loai):
    kq = _gui(cau)
    assert kq["success"] and kq["data"]["type"] == loai and "Ngân hàng đề lớp 10" in kq["message"]
    assert chat_gia[-1]["noi_dung"] == kq["message"]


def test_kien_thuc_ngoai_tai_lieu_khong_day(chat_gia, monkeypatch):
    monkeypatch.setattr(GS, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    kq = _gui("xyzabc là gì")
    assert kq["data"]["type"] == "ngoai_tai_lieu" and "chưa có trong tài liệu lí thuyết" in kq["message"]


# ---------------------------------------------------------------- 23/10/2026 (chiều): trang English, tìm tài liệu
def test_trang_tieng_anh_tra_loi_tieng_anh(monkeypatch):
    """Cô Lan: "chuyển sang tiếng Anh thì chat trả lời, giải thích không phải tiếng Anh"."""
    goi = []
    tra = iter(["Chào bạn! Tập rỗng là tập hợp không chứa phần tử nào.", "The empty set has no elements."])
    monkeypatch.setattr(GS, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(GS, "_goi_mo_hinh", lambda p: goi.append(p) or next(tra))
    kq = T.tra_loi_kien_thuc("tập rỗng là gì", 10, "en")
    assert kq["tra_loi"] == "The empty set has no elements." and len(goi) == 2       # trả tiếng Việt -> gọi lại 1 lần
    assert goi[0]["cau_hoi"].startswith("tập rỗng là gì") and "Reply in ENGLISH" in goi[0]["cau_hoi"]
    assert goi[1]["lenh_he_thong"].startswith("IMPORTANT")
    goi.clear()
    monkeypatch.setattr(GS, "_goi_mo_hinh", lambda p: goi.append(p) or "Tập rỗng là gì nhỉ")
    assert T.tra_loi_kien_thuc("tập rỗng là gì", 10, "vi") and goi[0]["cau_hoi"] == "tập rỗng là gì"


def test_la_tieng_viet():
    assert GS.la_tieng_viet("Tập rỗng là tập hợp không chứa phần tử nào.")
    assert not GS.la_tieng_viet("The empty set has no elements. Review: lesson Bài 2. Tập hợp, section Empty set.")


@pytest.mark.parametrize("cau, bai", [("tập rỗng là gì", "L10_C1_B2"), ("mệnh đề là gì", "L10_C1_B1"),
                                      ("mệnh đề phủ định là gì", "L10_C1_B1"), ("khoảng cách là gì", "L10_C7_B19"),
                                      ("tập con là gì", "L10_C1_B2")])
def test_hoi_kien_thuc_chi_lay_mot_bai(cau, bai):
    """"đang giải thích về tập rỗng, tại sao lại lôi kiến thức tổ hợp vào"; "mệnh đề là gì" từng báo chưa có tài liệu."""
    from app.services.ly_thuyet_service import tim_doan_tu_do
    r = tim_doan_tu_do(10, cau)
    assert r and {d["ma_bai"] for d in r} == {bai}
