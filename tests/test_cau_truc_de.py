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
    # cau thuong (I, II, III) dung ex; tu luan (IV) dung bt -> in "Bai 1." (co Lan 13/10/2026)
    assert than.count(r"\setcounter{ex}{0}") == 3
    assert than.count(r"\setcounter{bt}{0}") == 1


def test_so_cau_trong_loi_dan_khop_thuc_te():
    than = A._ghep_4_phan(_theo_phan_day_du())
    assert "đến câu 12." in than          # 12 cau trac nghiem
    assert "đến câu 2." in than           # 2 cau dung/sai
    assert "đến câu 4." in than           # 4 cau tra loi ngan
    assert "đến bài 3." in than           # 3 bai tu luan


def test_phan_rong_thi_bo_han_nhung_so_La_Ma_GIU_NGUYEN():
    """Số La Mã gắn chết vào LOẠI CÂU, phần rỗng không kéo số tụt xuống.

    ĐỔI 28/09/2026 - cô Lan chốt. Bản cũ dồn số liên tục cho khỏi
    "nhảy cóc". Nhưng cô Lan tạo đề hệ số 1 chương 3 (đề thiếu phần
    Trả lời ngắn) rồi đối chiếu PDF với trang làm bài trên web thì
    thấy cùng một câu tự luận mà PDF gọi là PHẦN III, web gọi là
    PHẦN IV - vì web dùng bảng TEN_PHAN gán số cố định theo loại câu.
    Nay cả hai nơi đều theo khuôn đề của Bộ (QĐ 764): Trắc nghiệm
    luôn I, Đúng/Sai luôn II, Trả lời ngắn luôn III, Tự luận luôn IV.
    """
    than = A._ghep_4_phan({"MC": [_cau("a")], "TL": [_cau("b")]})
    assert "PHẦN I." in than
    assert "PHẦN IV." in than
    # Hai phan khong co cau nao thi bo han, khong in ra
    assert "PHẦN II." not in than
    assert "PHẦN III." not in than


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


# ---------------------------------------------------------------------
# /gv/ra-de: conversation_id PHAI la UUID hop le
# ---------------------------------------------------------------------

def test_ra_de_luu_conversation_id_la_uuid_hop_le(monkeypatch, tmp_path):
    """
    Loi that ngay 15/09/2026: conversation_id dat la f"gv-{uuid4()}".
    Cot nay kieu UUID trong Postgres nen tien to "gv-" lam ca lenh ghi
    that bai (22P02 invalid input syntax for type uuid) -> de sinh xong
    bi vut, bang "De da tao" khong bao gio co dong moi, va man hinh
    khong bao gi ca.
    """
    import uuid as _uuid
    from app.routers import teacher as router_gv

    class UserGia:
        id = "99999999-9999-9999-9999-999999999999"
        email = "co@example.com"

    da_luu = {}

    monkeypatch.setattr(router_gv, "get_current_user", lambda request: UserGia())
    monkeypatch.setattr(router_gv, "yeu_cau_giao_vien", lambda request, user=None: None)
    monkeypatch.setattr(router_gv, "generate_exam_pdf_auto", lambda **kw: {
        "pdf_path": _tep_gia(tmp_path, "de.pdf"),
        "tex_path": _tep_gia(tmp_path, "de.tex"),
        "pdf_loigiai_path": None, "dap_an_json_path": None,
        "so_cau_da_sinh": 1, "so_cau_thieu": 0, "danh_sach_generator_id": [],
    })

    def gia_luu(**kw):
        da_luu.update(kw)
        return "de-id-gia"

    monkeypatch.setattr(router_gv.history_service, "luu_de_da_sinh", gia_luu)
    monkeypatch.setattr(router_gv.history_service, "luu_file_de", lambda *a, **k: None)

    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)

    res = client.post("/gv/ra-de", data={
        "lop": 10, "ki_thi": "thuong_xuyen", "pham_vi_chuong": "chuong_1",
        "socau_ma_de": 4, "tieu_de": "DE THU", "cho_phep_thieu": "1",
    }, follow_redirects=False)

    assert res.status_code == 303
    # Phai parse duoc thanh UUID - khong duoc co tien to gi
    _uuid.UUID(da_luu["conversation_id"])
    assert da_luu["role"] == "teacher"
    assert da_luu["blueprint"]["socau_ma_de"] == 4


def test_phan_chi_mot_cau_khong_ghi_tu_cau_1_den_cau_1():
    """Co Lan 13/10/2026: phan chi co 1 cau thi ghi "cau 1" / "bai 1", nhieu cau moi "tu ... den ...". Ap dung ca PDF va Word."""
    kh = {"MC": [_cau("a")], "TF": [_cau("b")], "SA": [_cau("c")], "TL": [_cau("d")]}
    than = A._ghep_4_phan(kh)
    assert "từ câu 1 đến câu 1" not in than and "từ bài 1 đến bài 1" not in than
    assert "Thí sinh trả lời câu 1. Thí sinh chỉ chọn một phương án." in than
    assert "Thí sinh trình bày tự luận bài 1." in than
    assert "Thí sinh trả lời câu 1.\n" in than                      # phan tra loi ngan
    en = A._ghep_4_phan(kh, "en")
    assert "1 to 1" not in en and "Write out the full solution for problem 1." in en and "Answer question 1." in en
    # nhieu cau thi giu "tu ... den ..."
    nhieu = A._ghep_4_phan({"MC": [_cau("a"), _cau("b")], "TL": [_cau("c"), _cau("d"), _cau("e")]})
    assert "từ câu 1 đến câu 2." in nhieu and "từ bài 1 đến bài 3." in nhieu


def test_tu_luan_dung_moi_truong_bt_hien_chu_Bai():
    """Co Lan 13/10/2026: tu luan la "Bai 1" chu khong phai "Cau 1" -> phan IV dung \\begin{bt} (ex_test in Bai)."""
    kh = {"MC": [_cau("a")], "TL": [_cau("b"), _cau("c")]}
    than = A._ghep_4_phan(kh)
    iv = than[than.index("PHẦN IV."):]
    assert iv.count(r"\begin{bt}") == 2 and iv.count(r"\end{bt}") == 2 and r"\begin{ex}" not in iv
    i = than[:than.index("PHẦN IV.")]
    assert r"\begin{ex}" in i and r"\begin{bt}" not in i
    assert r"\setcounter{bt}{0}" + "\n" + r"\noindent\textbf{PHẦN IV.}" in than


def test_sty_co_moi_truong_bt_hien_Bai():
    from pathlib import Path
    cfg = Path(__file__).resolve().parent.parent / "data" / "config"
    assert r"\newtheorem{bt}{\namebt}" in (cfg / "ex_test.sty").read_text(encoding="utf-8")
    assert r"\newtheorem{bt}{\namebt}" in (cfg / "ex_test_en.sty").read_text(encoding="utf-8")
    assert r"\newcommand{\namebt}{Bài}" in (cfg / "ex_test.sty").read_text(encoding="utf-8")
    assert r"\newcommand{\namebt}{Problem}" in (cfg / "ex_test_en.sty").read_text(encoding="utf-8")


def test_word_doc_duoc_khoi_bt():
    from app.services import word_service as W
    tex = ("\\begin{document}\n\\tieude{a}{b}{c}\n\\noindent\\textbf{PHẦN I.} x\n\\begin{ex}c1\\end{ex}\n"
           "\\noindent\\textbf{PHẦN IV.} Thí sinh trình bày tự luận bài 1.\n\\begin{bt}t1\\end{bt}\n\\end{document}")
    muc = W._doc_nhom(tex)[1][0]["muc"]
    assert [("cau" in m) for m in muc] == [False, True, False, True]
    assert muc[3]["cau"].startswith(r"\begin{bt}")
