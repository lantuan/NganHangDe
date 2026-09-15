"""
Kiem tra CAU TRUC tep .tex sinh ra: 4 phan theo de cua Bo, va nhieu ma de.

Khong bien dich PDF o day (may nao cung chay duoc bai test nay); viec
bien dich that kiem tra tren VPS. Bai test soi CHUOI LaTeX sinh ra.
"""

from app.services import exam_assembler_service as A


def _cau(noi_dung):
    return r"\begin{ex}" + noi_dung + r"\end{ex}"


def _theo_phan_day_du(nhan=""):
    return {
        "MC": [_cau(f"{nhan} TN {i}") for i in range(1, 13)],
        "TF": [_cau(f"{nhan} DS {i}") for i in range(1, 3)],
        "SA": [_cau(f"{nhan} TLN {i}") for i in range(1, 5)],
        "TL": [_cau(f"{nhan} TL {i}") for i in range(1, 4)],
    }


def test_du_4_phan_dung_thu_tu():
    than = A._ghep_4_phan(_theo_phan_day_du())
    for so_la_ma in ("I", "II", "III", "IV"):
        assert f"PHẦN {so_la_ma}." in than
    # Dung thu tu MC -> TF -> SA -> TL
    assert (than.index("PHẦN I.") < than.index("PHẦN II.")
            < than.index("PHẦN III.") < than.index("PHẦN IV."))


def test_moi_phan_danh_so_lai_tu_1():
    than = A._ghep_4_phan(_theo_phan_day_du())
    # Truoc MOI tieu de phan phai co \setcounter{ex}{0}
    assert than.count(r"\setcounter{ex}{0}") == 4


def test_so_cau_trong_loi_dan_khop_thuc_te():
    than = A._ghep_4_phan(_theo_phan_day_du())
    assert "đến câu 12." in than          # 12 cau trac nghiem
    assert "đến câu 2." in than           # 2 cau dung/sai
    assert "đến câu 4." in than           # 4 cau tra loi ngan
    assert "đến bài 3." in than           # 3 bai tu luan


def test_phan_rong_thi_bo_han_va_khong_nhay_so_la_ma():
    # Chi co trac nghiem va tu luan -> phai la PHAN I va PHAN II,
    # KHONG duoc nhay thanh PHAN I roi PHAN IV.
    than = A._ghep_4_phan({"MC": [_cau("a")], "TL": [_cau("b")]})
    assert "PHẦN I." in than
    assert "PHẦN II." in than
    assert "PHẦN III." not in than
    assert "PHẦN IV." not in than


def test_loai_cau_suy_ra_dung_tu_generator_id():
    assert A._loai_cau_cua({"generator_id": "L10_C1_B2_VD020_TL_A"}) == "TL"
    assert A._loai_cau_cua({"generator_id": "L10_C1_TF_A"}) == "TF"
    assert A._loai_cau_cua({"generator_id": "L10_C1_B1_NB017_MC_A"}) == "MC"
    assert A._loai_cau_cua({"generator_id": "L10_C1_B1_VD014_SA_A"}) == "SA"
    # Truong loai_cau co san thi uu tien, khong phan biet hoa thuong
    assert A._loai_cau_cua({"loai_cau": "sa", "generator_id": "x_MC_A"}) == "SA"


def test_mot_ma_de_co_du_tieu_de_o_ho_ten_chan_trang_va_het_de():
    khung = A._khung_mot_ma_de("ĐỀ KIỂM TRA", 10, "teacher", "1001", "THAN")
    assert r"\tieude{\pageref{made1001}}{ĐỀ KIỂM TRA}{10}" in khung
    assert "Mã đề 1001" in khung
    assert r"\chantrang{\pageref{made1001}}" in khung
    assert r"\setcounter{page}{1}" in khung
    assert r"\hetde\label{made1001}" in khung
    assert "THAN" in khung


def test_hoc_sinh_khong_co_o_ho_ten_va_ma_de():
    khung = A._khung_mot_ma_de("ĐỀ", 10, "student", "1001", "THAN")
    assert "Họ tên thí sinh" not in khung
    assert "Mã đề" not in khung
    # Nhung van co tieu de va dong HET
    assert r"\hetde\label{made1001}" in khung


def test_nhieu_ma_de_thi_moi_ma_mot_khoi_rieng_va_sang_trang():
    khoi = [A._khung_mot_ma_de("ĐỀ", 10, "teacher", f"100{i}",
                               A._ghep_4_phan(_theo_phan_day_du(f"de{i}")))
            for i in range(1, 5)]
    noi_dung = "\n\\newpage\n\n".join(khoi)

    # 4 ma de khac nhau
    for i in range(1, 5):
        assert f"Mã đề 100{i}" in noi_dung
        assert rf"\hetde\label{{made100{i}}}" in noi_dung
    # 4 de -> 3 lan sang trang
    assert noi_dung.count(r"\newpage") == 3
    # Moi de du 4 phan
    assert noi_dung.count("PHẦN I.") == 4
    assert noi_dung.count("PHẦN IV.") == 4
    # Noi dung cac ma de KHAC nhau (moi ma de goi lai ham sinh)
    assert "de1 TN 1" in noi_dung and "de4 TN 1" in noi_dung


# ---------------------------------------------------------------------
# Chat phai phan biet vai tro: giao vien nhan de KEM loi giai
# ---------------------------------------------------------------------

def _tep_gia(tmp_path, ten):
    """Endpoint tra ve FileResponse nen duong dan phai ton tai that."""
    f = tmp_path / ten
    f.write_text("gia")
    return str(f)


def test_may_chu_ep_role_teacher_khi_user_la_giao_vien(monkeypatch, tmp_path):
    """
    n8n van gui role="student" (prompt cu), nhung may chu phai tu tra
    profiles.vai_tro theo user_id va ep thanh "teacher". Neu khong, giao
    vien dung Chat AI chi nhan de tran, khong co loi giai.
    """
    from app.routers import exam as router_exam

    da_goi = {}

    def gia_generate(**kw):
        da_goi.update(kw)
        return {"pdf_path": _tep_gia(tmp_path, "a.pdf"),
                "tex_path": _tep_gia(tmp_path, "a.tex"),
                "pdf_loigiai_path": _tep_gia(tmp_path, "lg.pdf"),
                "dap_an_json_path": None,
                "so_cau_da_sinh": 1, "so_cau_thieu": 0,
                "danh_sach_generator_id": []}

    monkeypatch.setattr(router_exam, "generate_exam_pdf_auto", gia_generate)
    monkeypatch.setattr(router_exam.profile_service, "la_giao_vien", lambda uid: True)
    monkeypatch.setattr(router_exam.history_service, "luu_de_da_sinh", lambda **kw: None)

    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)

    client.post("/api/exam/generate-pdf-auto", json={
        "lop": 10, "tieu_de": "DE", "role": "student",
        "loai_he_so": "HeSo1", "pham_vi_chuong": "chuong_1",
        "user_id": "77777777-7777-7777-7777-777777777777",
        "conversation_id": "hoi-thoai-1",
    })

    assert da_goi.get("role") == "teacher", \
        "Giao vien chat -> may chu phai ep role=teacher du n8n gui 'student'"


def test_hoc_sinh_van_giu_role_student(monkeypatch, tmp_path):
    from app.routers import exam as router_exam

    da_goi = {}

    def gia_generate(**kw):
        da_goi.update(kw)
        return {"pdf_path": _tep_gia(tmp_path, "a.pdf"),
                "tex_path": _tep_gia(tmp_path, "a.tex"),
                "pdf_loigiai_path": None, "dap_an_json_path": None,
                "so_cau_da_sinh": 1, "so_cau_thieu": 0,
                "danh_sach_generator_id": []}

    monkeypatch.setattr(router_exam, "generate_exam_pdf_auto", gia_generate)
    monkeypatch.setattr(router_exam.profile_service, "la_giao_vien", lambda uid: False)
    monkeypatch.setattr(router_exam.history_service, "luu_de_da_sinh", lambda **kw: None)

    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)

    client.post("/api/exam/generate-pdf-auto", json={
        "lop": 10, "tieu_de": "DE", "role": "student",
        "loai_he_so": "HeSo1", "pham_vi_chuong": "chuong_1",
        "user_id": "88888888-8888-8888-8888-888888888888",
        "conversation_id": "hoi-thoai-2",
    })

    assert da_goi.get("role") == "student", \
        "Hoc sinh KHONG duoc nhan de kem loi giai"
