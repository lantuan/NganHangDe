"""
Kiem tra GIA SU AI - MUC A.

Trong tam la BA LOP KHOA chong "AI tu tinh toan" (xem docstring dau
app/services/gia_su_service.py):
  LOP 1 - cau lenh phai chua de bai + dap an + loi giai chuan, va phai
          co cac cau cam tinh toan.
  LOP 2 - ket qua tra ve LUON kem dap_an_python + loi_giai_python.
  LOP 3 - moi luot hoi deu ghi nhat ki.

Va mot dieu quan trong khong kem: KHONG BAO GIO goi mo hinh khi chua co
loi giai chuan - vi luc do AI bat buoc phai tu nghi ra, dung cai bi cam.
"""

import pytest

from app.services import gia_su_service as G


# ======================================================
# LOP KHOA 1: CAU LENH
# ======================================================

NGU_CANH_MAU = {
    "de_bai": "Cho hàm số $y = 2x + 1$. Tính $y(3)$.",
    "dap_an": "A. $7$",
    "loi_giai": "Thay $x = 3$ vào ta được $y = 2 \\cdot 3 + 1 = 7$.",
    "question_id": "L10_C1_B2_TH01_MC_v1",
}


def test_cau_lenh_chua_du_de_bai_dap_an_loi_giai():
    payload = G.dung_lenh(NGU_CANH_MAU, "em chưa hiểu bước thay số")
    lenh = payload["lenh_he_thong"]
    assert NGU_CANH_MAU["de_bai"] in lenh
    assert NGU_CANH_MAU["dap_an"] in lenh
    assert NGU_CANH_MAU["loi_giai"] in lenh


def test_cau_lenh_cam_tu_tinh_toan():
    lenh = G.dung_lenh(NGU_CANH_MAU, "hỏi gì đó")["lenh_he_thong"]
    assert "KHÔNG TỰ TÍNH TOÁN" in lenh
    assert "KHÁC với" in lenh          # cam ra ket qua khac loi giai mau
    assert "CHỈ nói về đúng câu hỏi này" in lenh


def test_cau_lenh_co_san_cau_tu_choi_de_mo_hinh_dung_lai():
    lenh = G.dung_lenh(NGU_CANH_MAU, "hỏi gì đó")["lenh_he_thong"]
    assert G.CAU_TU_CHOI in lenh


def test_mat_de_bai_thi_cam_doan_lai_de_bai():
    """Khi chi con loi giai (de cu, file dapan_json da bi don), cau lenh
    phai noi ro: khong duoc doan lai de bai."""
    ngu_canh = dict(NGU_CANH_MAU, de_bai="")
    lenh = G.dung_lenh(ngu_canh, "hỏi gì đó")["lenh_he_thong"]
    assert "TUYỆT ĐỐI không đoán lại đề bài" in lenh


def test_cau_lenh_gui_kem_dap_an_python_de_doi_chieu():
    payload = G.dung_lenh(NGU_CANH_MAU, "hỏi gì đó")
    assert payload["dap_an_python"] == NGU_CANH_MAU["dap_an"]
    assert payload["muc"] == "A"


# ======================================================
# DOC DAP AN / DE BAI TU dapan_json (khong tinh toan lai)
# ======================================================

def test_mo_ta_dap_an_mc_ghep_nhan_va_noi_dung():
    cau = {"loai_cau": "MC", "dap_an": "B", "phuong_an": {"A": "$1$", "B": "$7$"}}
    assert G._mo_ta_dap_an(cau) == "B. $7$"


def test_mo_ta_dap_an_tf_du_4_y_dung_thu_tu():
    cau = {"loai_cau": "TF", "dap_an": {"b": False, "a": True, "d": False, "c": True}}
    assert G._mo_ta_dap_an(cau) == "a) Đúng; b) Sai; c) Đúng; d) Sai"


def test_mo_ta_dap_an_sa_giu_nguyen_van():
    assert G._mo_ta_dap_an({"loai_cau": "SA", "dap_an": "12,5"}) == "12,5"


def test_mo_ta_de_bai_mc_kem_du_phuong_an():
    cau = {"loai_cau": "MC", "de_bai": "Tính $1+1$.",
           "phuong_an": {"A": "$1$", "B": "$2$"}}
    mo_ta = G._mo_ta_de_bai(cau)
    assert "Tính $1+1$." in mo_ta and "A. $1$" in mo_ta and "B. $2$" in mo_ta


def test_mo_ta_de_bai_tf_kem_du_4_y():
    cau = {"loai_cau": "TF", "de_bai": "Xét các mệnh đề:",
           "phat_bieu": {"a": "P", "b": "Q", "c": "R", "d": "S"}}
    mo_ta = G._mo_ta_de_bai(cau)
    for y in ("a) P", "b) Q", "c) R", "d) S"):
        assert y in mo_ta


# ======================================================
# KHONG DU DU LIEU -> BAO LOI, TUYET DOI KHONG GOI MO HINH
# ======================================================

def test_khong_tim_thay_de_thi_bao_loi(monkeypatch):
    monkeypatch.setattr(G.history_service, "lay_de_theo_id", lambda _: None)
    with pytest.raises(G.GiaSuError):
        G.lay_ngu_canh_cau("de-khong-co", 1)


def test_cau_khong_co_loi_giai_thi_bao_loi_chu_khong_goi_mo_hinh(monkeypatch, tmp_path):
    tep = tmp_path / "dapan.json"
    tep.write_text('[{"so_thu_tu": 1, "loai_cau": "MC", "de_bai": "x", "dap_an": "A", "loi_giai": ""}]',
                   encoding="utf-8")
    monkeypatch.setattr(G.history_service, "lay_de_theo_id",
                        lambda _: {"id": "d1", "files": {"dapan_json": str(tep)}})
    with pytest.raises(G.GiaSuError):
        G.lay_ngu_canh_cau("d1", 1)


def test_hoi_khong_goi_mo_hinh_khi_thieu_ngu_canh(monkeypatch):
    """Diem quan trong nhat: thieu du lieu thi DUNG LAI, khong goi AI."""
    da_goi = []
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: da_goi.append(p) or "khong duoc goi")
    monkeypatch.setattr(G.history_service, "lay_de_theo_id", lambda _: None)

    with pytest.raises(G.GiaSuError):
        G.hoi("u1", "d1", 1, "em chưa hiểu")
    assert da_goi == []


def test_hoi_khong_goi_mo_hinh_khi_cau_hoi_rong(monkeypatch):
    da_goi = []
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: da_goi.append(p) or "x")
    with pytest.raises(G.GiaSuError):
        G.hoi("u1", "d1", 1, "   ")
    assert da_goi == []


def test_cau_hoi_qua_dai_bi_chan(monkeypatch):
    da_goi = []
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: da_goi.append(p) or "x")
    with pytest.raises(G.GiaSuError):
        G.hoi("u1", "d1", 1, "a" * (G.GIA_SU_DO_DAI_CAU_HOI + 1))
    assert da_goi == []


# ======================================================
# LOP KHOA 2 + 3 tren duong di day du
# ======================================================

@pytest.fixture
def gia_su_gia_lap(monkeypatch, tmp_path):
    """Dung 1 de gia co 1 cau MC day du, va thay Supabase bang bo nho."""
    tep = tmp_path / "dapan.json"
    tep.write_text(
        '[{"so_thu_tu": 1, "loai_cau": "MC", "de_bai": "Tính $2+2$.",'
        ' "phuong_an": {"A": "$3$", "B": "$4$"}, "dap_an": "B",'
        ' "loi_giai": "Cộng trực tiếp: $2+2=4$.",'
        ' "generator_id": "L10_C1_B1_NB01_MC_v1"}]',
        encoding="utf-8",
    )
    monkeypatch.setattr(G.history_service, "lay_de_theo_id",
                        lambda _: {"id": "d1", "files": {"dapan_json": str(tep)}})

    trang_thai = {"luot": {"da_dung": 0, "gioi_han": 5, "con_lai": 5}, "nhat_ki": []}
    monkeypatch.setattr(G, "lay_luot", lambda uid: dict(trang_thai["luot"]))

    def _tru(uid):
        trang_thai["luot"]["da_dung"] += 1
        trang_thai["luot"]["con_lai"] -= 1
    monkeypatch.setattr(G, "tru_luot", _tru)

    def _ghi(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, tra_loi, tt):
        trang_thai["nhat_ki"].append({
            "cau_hoi": cau_hoi, "tra_loi": tra_loi, "trang_thai": tt,
            "dap_an_python": (ngu_canh or {}).get("dap_an"),
        })
    monkeypatch.setattr(G, "ghi_nhat_ki", _ghi)
    return trang_thai


def test_luon_tra_ve_dap_an_va_loi_giai_python(monkeypatch, gia_su_gia_lap):
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: "Em cộng hai số lại là ra.")

    kq = G.hoi("u1", "d1", 1, "em chưa hiểu")
    assert kq["dap_an_python"] == "B. $4$"
    assert kq["loi_giai_python"] == "Cộng trực tiếp: $2+2=4$."
    assert kq["tra_loi"] == "Em cộng hai số lại là ra."


def test_ghi_nhat_ki_kem_dap_an_python(monkeypatch, gia_su_gia_lap):
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: "Trả lời.")

    G.hoi("u1", "d1", 1, "em chưa hiểu")
    assert len(gia_su_gia_lap["nhat_ki"]) == 1
    dong = gia_su_gia_lap["nhat_ki"][0]
    assert dong["cau_hoi"] == "em chưa hiểu"
    assert dong["tra_loi"] == "Trả lời."
    assert dong["dap_an_python"] == "B. $4$"
    assert dong["trang_thai"] == "ok"


def test_chua_cau_hinh_webhook_van_tra_loi_giai_chuan(monkeypatch, gia_su_gia_lap):
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "")
    kq = G.hoi("u1", "d1", 1, "em chưa hiểu")
    assert kq["che_do"] == "khong_ai"
    assert kq["tra_loi"] is None
    assert kq["loi_giai_python"] == "Cộng trực tiếp: $2+2=4$."


def test_khong_tru_luot_khi_mo_hinh_loi(monkeypatch, gia_su_gia_lap):
    import httpx
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")

    def _hong(p):
        raise httpx.ConnectError("mat mang")
    monkeypatch.setattr(G, "_goi_mo_hinh", _hong)

    with pytest.raises(G.GiaSuError):
        G.hoi("u1", "d1", 1, "em chưa hiểu")
    assert gia_su_gia_lap["luot"]["da_dung"] == 0     # khong mat luot vi loi mang
    assert gia_su_gia_lap["nhat_ki"][0]["trang_thai"] == "loi"


def test_het_luot_thi_khong_goi_mo_hinh(monkeypatch, gia_su_gia_lap):
    gia_su_gia_lap["luot"].update({"da_dung": 5, "con_lai": 0})
    da_goi = []
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: da_goi.append(p) or "x")

    with pytest.raises(G.GiaSuError):
        G.hoi("u1", "d1", 1, "em chưa hiểu")
    assert da_goi == []
    assert gia_su_gia_lap["nhat_ki"][0]["trang_thai"] == "het_luot"


def test_danh_dau_ngoai_pham_vi_khi_mo_hinh_tu_choi(monkeypatch, gia_su_gia_lap):
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: G.CAU_TU_CHOI)

    kq = G.hoi("u1", "d1", 1, "cho em hỏi thời tiết hôm nay")
    assert kq["trang_thai"] == "ngoai_pham_vi"
    assert gia_su_gia_lap["nhat_ki"][0]["trang_thai"] == "ngoai_pham_vi"


def test_hoi_cau_khong_co_trong_de_thi_bao_loi(monkeypatch, gia_su_gia_lap):
    monkeypatch.setattr(G, "N8N_WEBHOOK_GIA_SU", "https://vi-du/webhook")
    monkeypatch.setattr(G, "_goi_mo_hinh", lambda p: "khong duoc goi")
    with pytest.raises(G.GiaSuError):
        G.hoi("u1", "d1", 99, "em chưa hiểu")


# ======================================================
# TANG API: /api/giasu/* phai chan o SERVER
# ======================================================

from fastapi.testclient import TestClient      # noqa: E402

from app.main import app                        # noqa: E402
from app.routers import gia_su as R             # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)


def test_chua_dang_nhap_thi_khong_hoi_duoc(client, monkeypatch):
    monkeypatch.setattr(R, "get_current_user", lambda request: None)
    r = client.post("/api/giasu/hoi",
                    json={"de_id": "d1", "so_thu_tu": 1, "cau_hoi": "em chưa hiểu"})
    assert r.status_code == 401


def test_chua_dang_nhap_thi_khong_xem_duoc_luot(client, monkeypatch):
    monkeypatch.setattr(R, "get_current_user", lambda request: None)
    assert client.get("/api/giasu/luot").status_code == 401


class _UserGia:
    id = "user-that-su-dang-nhap"


def test_user_id_lay_tu_phien_chu_khong_lay_tu_body(client, monkeypatch):
    """Neu lay user_id tu body thi ai cung tieu het luot cua nguoi khac."""
    da_nhan = {}
    monkeypatch.setattr(R, "get_current_user", lambda request: _UserGia())

    def _hoi(user_id, de_id, so_thu_tu, cau_hoi, lich_su=None):
        da_nhan["user_id"] = user_id
        return {"tra_loi": "ok", "che_do": "ai", "dap_an_python": "B",
                "loi_giai_python": "...", "luot": {}, "trang_thai": "ok"}
    monkeypatch.setattr(R.gia_su_service, "hoi", _hoi)

    r = client.post("/api/giasu/hoi", json={
        "de_id": "d1", "so_thu_tu": 1, "cau_hoi": "em chưa hiểu",
        "user_id": "ke-mao-danh",      # co tinh gui them - phai bi bo qua
    })
    assert r.status_code == 200
    assert da_nhan["user_id"] == "user-that-su-dang-nhap"


def test_loi_doc_duoc_tra_200_kem_loi_giai_du_phong(client, monkeypatch):
    """Het luot/AI hong -> hoc sinh VAN doc duoc loi giai chuan."""
    monkeypatch.setattr(R, "get_current_user", lambda request: _UserGia())

    def _hoi(**kwargs):
        raise R.GiaSuError("Hôm nay em đã dùng hết lượt hỏi rồi.")
    monkeypatch.setattr(R.gia_su_service, "hoi", _hoi)
    monkeypatch.setattr(R.gia_su_service, "lay_ngu_canh_cau",
                        lambda de_id, so_thu_tu, user_id: dict(NGU_CANH_MAU))

    r = client.post("/api/giasu/hoi",
                    json={"de_id": "d1", "so_thu_tu": 1, "cau_hoi": "em chưa hiểu"})
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is False
    assert "hết lượt" in body["message"]
    assert body["data"]["loi_giai_python"] == NGU_CANH_MAU["loi_giai"]


def test_khong_lay_duoc_loi_giai_du_phong_thi_van_bao_loi_binh_thuong(client, monkeypatch):
    monkeypatch.setattr(R, "get_current_user", lambda request: _UserGia())

    def _hoi(**kwargs):
        raise R.GiaSuError("Không tìm thấy đề này.")
    monkeypatch.setattr(R.gia_su_service, "hoi", _hoi)

    def _hong(de_id, so_thu_tu, user_id):
        raise RuntimeError("hong")
    monkeypatch.setattr(R.gia_su_service, "lay_ngu_canh_cau", _hong)

    r = client.post("/api/giasu/hoi",
                    json={"de_id": "d1", "so_thu_tu": 1, "cau_hoi": "em chưa hiểu"})
    assert r.status_code == 200
    assert r.json()["success"] is False
    assert r.json()["data"] is None
