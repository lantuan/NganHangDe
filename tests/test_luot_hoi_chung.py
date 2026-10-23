"""30 lượt hỏi AI mỗi ngày, tính CHUNG thầy/cô AI và khung chat (cô Lan 23/10/2026: "giới hạn lại số lần hỏi luôn. mỗi
ngày hỏi 30 lượt cả đề và chatbox ngoài"). Giáo viên không giới hạn. Câu máy chủ tự xử lí (không gọi mô hình) không
tính lượt."""
import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.main import app
from app.routers import chat as C
from app.services import gia_su_service as GS


def test_mac_dinh_30():
    import importlib
    import os
    cu = os.environ.pop("GIA_SU_LUOT_MOI_NGAY", None)
    try:
        assert importlib.reload(config).GIA_SU_LUOT_MOI_NGAY == 30
    finally:
        if cu is not None:
            os.environ["GIA_SU_LUOT_MOI_NGAY"] = cu
        importlib.reload(config)


class _U:
    id = "99999999-9999-9999-9999-999999999999"


class _JsonOk:
    status_code = 200
    headers = {"content-type": "application/json"}
    text = "{}"

    def json(self):
        return {"success": True, "message": "Chào bạn!", "data": None}


@pytest.fixture
def gia(monkeypatch, tmp_path):
    from app.services import tuy_chon_de_service as TC
    monkeypatch.setattr(TC, "TEP", tmp_path / "tc.json")
    monkeypatch.setattr(C, "get_current_user", lambda request: _U)
    monkeypatch.setattr(C.history_service, "luu_tin_nhan", lambda **kw: None)
    monkeypatch.setattr(C.history_service, "lay_de_gan_nhat", lambda cid: None)
    trang = {"da_dung": 0, "gioi_han": 30, "goi_n8n": 0, "vai_tro": "hoc_sinh"}
    monkeypatch.setattr(C.profile_service, "lay_vai_tro", lambda uid: trang["vai_tro"])
    monkeypatch.setattr(GS, "lay_luot", lambda uid: {"da_dung": trang["da_dung"], "gioi_han": 30,
                                                    "con_lai": max(0, 30 - trang["da_dung"])})
    monkeypatch.setattr(GS, "tru_luot", lambda uid: trang.__setitem__("da_dung", trang["da_dung"] + 1))

    def _n8n(*a, **k):
        trang["goi_n8n"] += 1
        return _JsonOk()
    monkeypatch.setattr(C, "_goi_n8n", _n8n)
    return trang


def _gui(cau, lang="vi"):
    return TestClient(app).post("/chat", data={"message": cau, "conversation_id": "h"}, cookies={"lang": lang}).json()


def test_moi_tin_nhan_goi_ai_tru_mot_luot(gia):
    _gui("chào bạn")
    _gui("bạn khỏe không")
    assert gia["da_dung"] == 2 and gia["goi_n8n"] == 2


def test_het_luot_thi_khong_goi_ai(gia):
    gia["da_dung"] = 30
    kq = _gui("chào bạn")
    assert kq["success"] and kq["data"]["type"] == "het_luot" and "30 lượt" in kq["message"]
    assert gia["goi_n8n"] == 0 and gia["da_dung"] == 30
    en = _gui("hello", "en")
    assert "30 AI questions" in en["message"]


def test_giao_vien_khong_gioi_han(gia):
    gia["vai_tro"], gia["da_dung"] = "giao_vien", 30
    kq = _gui("chào bạn")
    assert kq["message"] == "Chào bạn!" and gia["goi_n8n"] == 1 and gia["da_dung"] == 30


def test_gia_su_mien_luot_cho_giao_vien(monkeypatch):
    goi = []
    monkeypatch.setattr(GS, "lay_ngu_canh_cau", lambda *a, **k: {"de_bai": "D", "dap_an": "A", "loi_giai": "L",
                                                                 "question_id": "L10_C1_B1_NB001_MC_A"})
    monkeypatch.setattr(GS, "_cac_cau_da_lam", lambda uid, de: {1})
    monkeypatch.setattr(GS, "lay_luot", lambda uid: {"da_dung": 30, "gioi_han": 30, "con_lai": 0})
    monkeypatch.setattr(GS, "tru_luot", lambda uid: goi.append("tru"))
    monkeypatch.setattr(GS, "ghi_nhat_ki", lambda *a, **k: None)
    monkeypatch.setattr(GS, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(GS, "_goi_mo_hinh", lambda p: "Trả lời.")
    with pytest.raises(GS.GiaSuError):
        GS.hoi("u", "d", 1, "em chưa hiểu")                                  # học sinh hết lượt
    assert GS.hoi("u", "d", 1, "em chưa hiểu", mien_luot=True)["tra_loi"] == "Trả lời."
    assert goi == []                                                        # giáo viên không bị trừ
