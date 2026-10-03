"""Ngân hàng đề TIẾNG ANH (cô Lan 03/10/2026): bản Anh của chương phải ra ĐÚNG số liệu / cấu trúc như bản Việt
(cùng hạt giống), được sinh ra từ bản Việt (không sửa tay), và đề tiếng Anh ghép cùng đề tiếng Việt.

Chạy riêng: python3 -m pytest tests/test_ngan_hang_anh.py -q
(phần so sánh toàn chương chạy khoảng 30-60 giây)
"""
import importlib.util
import re
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "scripts"))


def _nap_script(ten):
    spec = importlib.util.spec_from_file_location(ten, GOC / "scripts" / (ten + ".py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules[ten] = m
    spec.loader.exec_module(m)
    return m


# Hàm lệch do bản Việt có chỗ KHÔNG ĐÚNG mà bản Anh đã sửa (không phải lỗi dịch):
CHO_PHEP_LECH = {
    # chữ \text{} cuối câu nằm khác chỗ do thứ tự câu tiếng Anh
    "L10_C1_NB015_TH014_TL_A_01",
}


def _cac_chuong_da_dich():
    return sorted(p.stem for p in (GOC / "data" / "python_bank_en" / "toan10").glob("L10_C*.py"))


def test_co_chuong_da_dich():
    assert "L10_C1" in _cac_chuong_da_dich()


@pytest.mark.parametrize("stem", _cac_chuong_da_dich())
def test_ban_anh_tuong_duong_ban_viet(stem):
    kt = _nap_script("kiem_tuong_duong")
    tong, bad = kt.so_sanh(stem, n=4)
    bad = {t: v for t, v in bad.items() if t not in CHO_PHEP_LECH}
    assert tong >= 20
    assert not bad, "Ban Anh lech ban Viet: %s" % list(bad.items())[:3]


@pytest.mark.parametrize("stem", _cac_chuong_da_dich())
def test_ban_anh_sinh_ra_tu_ban_viet_khong_sua_tay(stem):
    """data/python_bank_en/... phải đúng bằng kết quả của scripts/dich_ngan_hang.py (từ điển + patch)."""
    dich = _nap_script("dich_ngan_hang")
    nguon = GOC / "data" / "python_bank" / "toan10" / (stem + ".py")
    src, chua, loi = dich.dich_tep(nguon)
    assert not chua, "Con %d doan chua dich" % len(chua)
    assert not loi, "Loi dich: %s" % loi[:3]
    hien_co = (GOC / "data" / "python_bank_en" / "toan10" / (stem + ".py")).read_text(encoding="utf-8")
    assert src == hien_co, "Ban Anh khac ket qua dich - chay: python3 scripts/dich_ngan_hang.py dich <tep>"


@pytest.mark.parametrize("stem", _cac_chuong_da_dich())
def test_ban_anh_khong_con_chu_viet(stem):
    src = (GOC / "data" / "python_bank_en" / "toan10" / (stem + ".py")).read_text(encoding="utf-8")
    # bỏ chú thích và docstring (còn tiếng Việt - dành cho cô); chỉ xét chuỗi hiển thị
    import ast
    tree = ast.parse(src)
    docs = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.Module)) and n.body:
            d = n.body[0]
            if isinstance(d, ast.Expr) and isinstance(getattr(d, "value", None), ast.Constant):
                docs.add(id(d.value))
    co_dau = re.compile("[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.I)
    sot = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs:
            if co_dau.search(n.value):
                sot.append(n.value[:60])
    assert not sot, "Con chu Viet trong chuoi hien thi cua ban Anh: %s" % sot[:3]


def test_ex_test_en_va_mau_en_dung_voi_ban_viet():
    """ex_test_en.sty và latex_template_en.tex sinh từ bản Việt (scripts/tao_ex_test_en.py)."""
    tao = _nap_script("tao_ex_test_en")
    cu = {f: f.read_text(encoding="utf-8") for f in (tao.DICH, tao.MAU_DICH)}
    try:
        tao.main()
        for f, noi_dung in cu.items():
            assert f.read_text(encoding="utf-8") == noi_dung, "%s cu - chay scripts/tao_ex_test_en.py" % f.name
    finally:
        for f, noi_dung in cu.items():
            f.write_text(noi_dung, encoding="utf-8")


def test_de_tieng_anh_ghep_cung_de_viet(monkeypatch):
    """Đề Anh và đề Việt cùng hạt giống: cùng cấu trúc, cùng toán, khung tiếng Anh, tệp ở thư mục riêng."""
    import app.services.exam_assembler_service as A
    kt = _nap_script("kiem_tuong_duong")
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ KIỂM TRA", "teacher", "HeSo1", pham_vi_chuong="1",
                                  socau_ma_de=2, kem_tieng_anh=True, tieu_de_en="QUIZ")
    assert "tieng_anh_loi" not in kq, kq.get("tieng_anh_loi")
    en = kq["tieng_anh"]
    assert en["seed"] == kq["seed"]
    assert "temp_en" in en["tex_path"] and "temp_en" not in kq["tex_path"]
    assert "exports_en" not in kq["pdf_path"]
    vi_tex = Path(kq["tex_path"]).read_text(encoding="utf-8")
    en_tex = Path(en["tex_path"]).read_text(encoding="utf-8")
    assert "{ex_test_en}" in en_tex and "{ex_test_en}" not in vi_tex
    assert "PART I." in en_tex and "Exam code 1001" in en_tex and "Exam code 1002" in en_tex
    assert "PHẦN I." in vi_tex
    assert kt.cau_truc(vi_tex) == kt.cau_truc(en_tex)
    assert kt.vi_tri_true(vi_tex) == kt.vi_tri_true(en_tex)
    assert kt.toan(vi_tex) == kt.toan(en_tex)
    # không còn chữ Việt trong thân đề tiếng Anh (trừ tên người/địa danh không dấu)
    than = en_tex.split("\\begin{document}", 1)[1]
    assert not re.search("[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", than, re.I)


def test_chuong_chua_dich_thanh_dong_thieu_tieng_anh(monkeypatch):
    """Chương chưa có bản Anh: đề tiếng Anh hiện dòng [MISSING ...], đề tiếng Việt vẫn bình thường."""
    import app.services.exam_assembler_service as A
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ", "teacher", "HeSo1", pham_vi_chuong="3",
                                  socau_ma_de=1, kem_tieng_anh=True, tieu_de_en="QUIZ")
    en_tex = Path(kq["tieng_anh"]["tex_path"]).read_text(encoding="utf-8")
    assert "MISSING IN PYTHON" in en_tex
    assert kq["tieng_anh"]["so_cau_thieu"] > 0
    assert kq["so_cau_thieu"] == 0


def test_trang_lam_bai_hoc_sinh_lay_de_tieng_anh_cung_de_viet(monkeypatch):
    """Nền là tiếng Việt: đề chọn/sinh trên bản Việt; trang đang English thì /api/exam/quiz trả bản Anh
    của ĐÚNG đề đó (cùng số câu, loại câu, đáp án), trang Việt thì trả bản Việt."""
    from fastapi.testclient import TestClient
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="1", dapan_tieng_anh=True)
    assert "tieng_anh" not in kq                       # chỉ có đáp án, không biên dịch PDF tiếng Anh
    assert kq["dapan_en_path"] == str(A.duong_dapan_en(kq["dap_an_json_path"]))
    assert Path(kq["dapan_en_path"]).exists()
    de = {"id": "de-thu", "files": {"dapan_json": kq["dap_an_json_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    client = TestClient(app)
    vi = client.get("/api/exam/quiz/de-thu", cookies={"lang": "vi"}).json()["data"]
    en = client.get("/api/exam/quiz/de-thu", cookies={"lang": "en"}).json()["data"]
    assert vi["tong_so_cau"] == en["tong_so_cau"] > 0
    for cv, ce in zip(vi["cau_hoi"], en["cau_hoi"]):
        assert (cv["so_thu_tu"], cv["loai_cau"]) == (ce["so_thu_tu"], ce["loai_cau"])
        assert cv["de_bai"] != ce["de_bai"]
    # bản Anh không còn chữ có dấu tiếng Việt trong đề bài
    co_dau = re.compile("[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.I)
    assert not [c["de_bai"][:50] for c in en["cau_hoi"] if co_dau.search(c["de_bai"])]
    assert en["cau_hoi"][0]["ten_phan"].startswith("PART I")
    assert vi["cau_hoi"][0]["ten_phan"].startswith("PHẦN I")


def test_trang_lam_bai_chuong_chua_dich_roi_ve_tieng_viet(monkeypatch):
    from fastapi.testclient import TestClient
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="9", dapan_tieng_anh=True)
    assert "dapan_en_path" not in kq
    de = {"id": "de-thu", "files": {"dapan_json": kq["dap_an_json_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    en = TestClient(app).get("/api/exam/quiz/de-thu", cookies={"lang": "en"}).json()["data"]
    assert en["tong_so_cau"] > 0
    # đề không có bản Anh: trang English báo rõ (không im lặng rơi về tiếng Việt); trang Việt không báo gì
    assert "no English version" in en["thong_bao_ban_anh"]
    assert TestClient(app).get("/api/exam/quiz/de-thu", cookies={"lang": "vi"}).json()["data"]["thong_bao_ban_anh"] == ""


def test_gia_su_ai_giang_bang_tieng_anh_tu_de_goc_tieng_anh(monkeypatch):
    """Trang English: thầy/cô AI nhận đề bài, đáp án, lời giải mẫu BẢN ANH và lệnh hệ thống tiếng Anh."""
    import app.services.exam_assembler_service as A
    from app.services import gia_su_service as GS, history_service
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="1", dapan_tieng_anh=True)
    de = {"id": "de-thu", "files": {"dapan_json": kq["dap_an_json_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    co_dau = re.compile("[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.I)
    thu = 0
    for stt in range(1, 13):
        try:
            vi = GS.lay_ngu_canh_cau("de-thu", stt, None, "vi")
            en = GS.lay_ngu_canh_cau("de-thu", stt, None, "en")
        except GS.GiaSuError:
            continue
        thu += 1
        assert vi["de_bai"] != en["de_bai"]
        for khoa in ("de_bai", "dap_an", "loi_giai"):
            assert not co_dau.search(en[khoa]), (stt, khoa, en[khoa][:80])
        lenh = GS.dung_lenh(en, "why am I wrong?", None, "en")["lenh_he_thong"]
        assert "ENGLISH" in lenh and "thầy" not in lenh
    assert thu >= 5
    # đề chưa có bản Anh: rơi về tiếng Việt, không lỗi
    de["files"]["dapan_json"] = str(Path(kq["dap_an_json_path"]).with_name("khong_co_ban_anh_dapan.json"))
    import shutil
    shutil.copyfile(kq["dap_an_json_path"], de["files"]["dapan_json"])
    try:
        assert GS.lay_ngu_canh_cau("de-thu", 1, None, "en")["de_bai"]
    finally:
        Path(de["files"]["dapan_json"]).unlink()


def test_tai_de_pdf_hoc_sinh_ra_ban_tieng_anh_khi_trang_english(monkeypatch):
    """Nút tải PDF đề / lời giải: trang English thì biên dịch và trả PDF TIẾNG ANH (từ .tex tiếng Anh cạnh .tex Việt)."""
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app
    bien_dich = []

    def gia(tex, lang="vi"):
        from app.services.pdf_service import EXPORTS_DIR
        out = (R.EXPORTS_DIR_EN if lang == "en" else EXPORTS_DIR)
        out.mkdir(parents=True, exist_ok=True)
        pdf = out / (Path(tex).stem + ".pdf")
        pdf.write_bytes(b"%PDF-1.4 " + Path(tex).read_bytes()[:2000])
        bien_dich.append((Path(tex).name, lang))
        return pdf
    monkeypatch.setattr(A, "compile_pdf", gia)
    monkeypatch.setattr(R, "compile_pdf", gia)
    kq = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="1", dapan_tieng_anh=True)
    assert Path(A.duong_tex_en(kq["tex_path"])).exists()
    assert not any(l == "en" for _, l in bien_dich)         # lúc sinh đề CHƯA biên dịch PDF tiếng Anh
    de = {"id": "de-thu", "files": {"dapan_json": kq["dap_an_json_path"], "tex": kq["tex_path"], "de": kq["pdf_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    monkeypatch.setattr(history_service, "luu_file_de", lambda *a, **k: None)
    client = TestClient(app)
    r_vi = client.get("/api/exam/tai-de/de-thu", cookies={"lang": "vi"})
    r_en = client.get("/api/exam/tai-de/de-thu", cookies={"lang": "en"})
    assert r_vi.status_code == r_en.status_code == 200
    assert b"ex_test_en" in r_en.content and b"ex_test_en" not in r_vi.content   # PDF giả chứa đầu tệp .tex
    en_tex = A.duong_tex_en(kq["tex_path"]).read_text(encoding="utf-8")
    assert "[dethi]{ex_test_en}" in en_tex and "PART I." in en_tex
    assert ("%s.tex" % Path(kq["tex_path"]).stem, "en") in bien_dich    # biên dịch khi bấm tải
    # lời giải tiếng Anh: đổi [dethi] -> [loigiai] ở bản Anh, không đụng bản Việt
    r_lg = client.get("/api/exam/tai-loigiai/de-thu", cookies={"lang": "en"})
    assert r_lg.status_code == 200 and b"loigiai]{ex_test_en}" in r_lg.content
    # đề cũ (không có .tex tiếng Anh) rơi về tiếng Việt
    de["files"]["tex"] = str(Path(kq["tex_path"]).with_name("khong_co_ban_anh.tex"))
    Path(de["files"]["tex"]).write_text(Path(kq["tex_path"]).read_text(encoding="utf-8"), encoding="utf-8")
    try:
        assert client.get("/api/exam/tai-de/de-thu", cookies={"lang": "en"}).status_code == 200
    finally:
        Path(de["files"]["tex"]).unlink()


def test_tai_de_hoc_sinh_tick_ca_hai_thu_tieng_ra_zip(monkeypatch):
    """Học sinh tick "tải kèm cả hai thứ tiếng": /tai-de và /tai-loigiai?ngon_ngu=ca-hai trả .zip có CẢ bản Việt lẫn bản
    Anh, bất kể trang đang ở ngôn ngữ nào; ban=vi ép bản Việt dù trang English; đề không có bản Anh -> zip chỉ có bản Việt."""
    import io
    import zipfile
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app

    def gia(tex, lang="vi"):
        from app.services.pdf_service import EXPORTS_DIR
        out = (R.EXPORTS_DIR_EN if lang == "en" else EXPORTS_DIR)
        out.mkdir(parents=True, exist_ok=True)
        pdf = out / (Path(tex).stem + ".pdf")
        pdf.write_bytes(b"%PDF-1.4 " + Path(tex).read_bytes()[:2000])
        return pdf
    monkeypatch.setattr(A, "compile_pdf", gia)
    monkeypatch.setattr(R, "compile_pdf", gia)
    kq = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="1", dapan_tieng_anh=True)
    de = {"id": "de-thu-zip", "files": {"dapan_json": kq["dap_an_json_path"], "tex": kq["tex_path"], "de": kq["pdf_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    monkeypatch.setattr(history_service, "luu_file_de", lambda *a, **k: None)
    client = TestClient(app)
    for lang in ("vi", "en"):
        for duong in ("tai-de", "tai-loigiai"):
            r = client.get("/api/exam/%s/de-thu-zip?ngon_ngu=ca-hai" % duong, cookies={"lang": lang})
            assert r.status_code == 200 and r.headers["content-type"] == "application/zip"
            z = zipfile.ZipFile(io.BytesIO(r.content))
            ten = sorted(z.namelist())
            assert len(ten) == 2 and ten[0].endswith("_English.pdf") and ten[1].endswith("_TiengViet.pdf")
            assert b"ex_test_en" in z.read(ten[0]) and b"ex_test_en" not in z.read(ten[1])
    # ban=vi ép tiếng Việt dù trang đang English; ban=en ép tiếng Anh dù trang đang Việt
    assert b"ex_test_en" not in client.get("/api/exam/tai-de/de-thu-zip?ngon_ngu=vi", cookies={"lang": "en"}).content
    assert b"ex_test_en" in client.get("/api/exam/tai-de/de-thu-zip?ngon_ngu=en", cookies={"lang": "vi"}).content
    # đề không có bản Anh -> zip chỉ có bản Việt
    tex_cu = Path(kq["tex_path"]).with_name("de_cu_khong_co_ban_anh.tex")
    tex_cu.write_text(Path(kq["tex_path"]).read_text(encoding="utf-8"), encoding="utf-8")
    de["files"]["tex"] = str(tex_cu)
    try:
        r = client.get("/api/exam/tai-de/de-thu-zip?ngon_ngu=ca-hai", cookies={"lang": "en"})
        assert zipfile.ZipFile(io.BytesIO(r.content)).namelist() == ["de_TiengViet.pdf"]
    finally:
        tex_cu.unlink()


def test_word_tieng_anh_khi_trang_english(monkeypatch):
    """Tải Word: trang English thì file Word là TIẾNG ANH (nhãn khung + đề + lời giải); trang Việt giữ bản Việt."""
    import shutil
    import zipfile
    if not shutil.which("pandoc"):
        pytest.skip("không có pandoc")
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ KIỂM TRA", "teacher", "HeSo1", pham_vi_chuong="1",
                                  kem_tieng_anh=True, tieu_de_en="QUIZ")
    de = {"id": "de-thu-word", "files": {"tex": kq["tex_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    monkeypatch.setattr(R, "yeu_cau_giao_vien", lambda request, user=None: None)
    client = TestClient(app)
    co_dau = re.compile("[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.I)

    def chu(r):
        import io
        assert r.status_code == 200, r.text[:200]
        x = zipfile.ZipFile(io.BytesIO(r.content)).read("word/document.xml").decode("utf-8")
        return re.sub(r"<[^>]+>", " ", x)
    vi = chu(client.get("/api/exam/tai-word/de-thu-word?ban=loigiai", cookies={"lang": "vi"}))
    for ban in ("de", "loigiai"):
        en = chu(client.get("/api/exam/tai-word/de-thu-word?ban=%s" % ban, cookies={"lang": "en"}))
        assert "Question" in en and "PART" in en and "Exam code" in en
        assert not co_dau.search(en), co_dau.search(en).group(0) + " | " + en[max(0, co_dau.search(en).start() - 60):co_dau.search(en).start() + 60]
    assert "Solution." in en and "True" in en or "False" in en
    assert "Câu" in vi and "PHẦN" in vi and "Question" not in vi


def test_giao_vien_tick_ca_hai_thu_tieng_word_va_tex_ra_zip(monkeypatch):
    """Giáo viên tick "tải kèm bản tiếng Anh": Word và .tex (ngon_ngu=ca-hai) trả .zip có CẢ bản Việt lẫn bản Anh."""
    import io
    import shutil
    import zipfile
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app
    monkeypatch.setattr(A, "compile_pdf", lambda tex, lang="vi": Path(tex).with_suffix(".pdf"))
    kq = A.generate_exam_pdf_auto(10, "ĐỀ KIỂM TRA", "teacher", "HeSo1", pham_vi_chuong="1",
                                  kem_tieng_anh=True, tieu_de_en="QUIZ")
    de = {"id": "de-thu-gv", "files": {"tex": kq["tex_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    monkeypatch.setattr(R, "yeu_cau_giao_vien", lambda request, user=None: None)
    client = TestClient(app)
    r = client.get("/api/exam/tai-tex/de-thu-gv?ngon_ngu=ca-hai", cookies={"lang": "vi"})
    z = zipfile.ZipFile(io.BytesIO(r.content))
    assert sorted(n.rsplit("_", 1)[1] for n in z.namelist()) == ["English.tex", "TiengViet.tex"]
    en = [n for n in z.namelist() if n.endswith("English.tex")][0]
    assert "ex_test_en" in z.read(en).decode("utf-8")
    # không tick: vẫn là một tệp .tex tiếng Việt như cũ
    assert b"ex_test_en" not in client.get("/api/exam/tai-tex/de-thu-gv").content
    if shutil.which("pandoc"):
        for ban in ("de", "loigiai"):
            r = client.get("/api/exam/tai-word/de-thu-gv?ban=%s&ngon_ngu=ca-hai" % ban, cookies={"lang": "vi"})
            assert r.status_code == 200 and r.headers["content-type"] == "application/zip"
            ten = sorted(zipfile.ZipFile(io.BytesIO(r.content)).namelist())
            assert [n.rsplit("_", 1)[1] for n in ten] == ["English.docx", "TiengViet.docx"]


def test_tick_kem_tieng_anh_luc_tao_de_quyet_dinh_co_ban_anh_hay_khong(monkeypatch, tmp_path):
    """Ô tick "Kèm bản tiếng Anh" lúc tạo đề: không tick -> chỉ bản Việt (không sinh bản Anh); tick -> có cả hai.
    Lời gọi không nói rõ (n8n) thì tra lựa chọn đã ghi theo conversation_id."""
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    from app.services import tuy_chon_de_service as T
    from app.main import app
    monkeypatch.setattr(T, "TEP", tmp_path / "kem.json")
    goi = []

    def gia(**kw):
        goi.append(kw["dapan_tieng_anh"])
        raise R.AssembleError("dừng sớm")
    monkeypatch.setattr(R, "generate_exam_pdf_auto", gia)
    client = TestClient(app)
    base = {"lop": 10, "tieu_de": "ĐỀ", "role": "student", "loai_he_so": "HeSo1", "pham_vi_chuong": "chuong_1"}
    client.post("/api/exam/generate-pdf-auto", json=base)                                      # n8n, chưa ghi nhận gì
    client.post("/api/exam/generate-pdf-auto", json={**base, "kem_tieng_anh": True})           # người dùng tick
    client.post("/api/exam/generate-pdf-auto", json={**base, "kem_tieng_anh": False})
    T.dat_kem_tieng_anh("cuoc-1", True)
    client.post("/api/exam/generate-pdf-auto", json={**base, "conversation_id": "cuoc-1"})     # n8n sau khi /chat ghi tick
    T.dat_kem_tieng_anh("cuoc-1", False)
    client.post("/api/exam/generate-pdf-auto", json={**base, "conversation_id": "cuoc-1"})
    assert goi == [False, True, False, True, False]
    assert T.lay_kem_tieng_anh("khong-co") is False and T.lay_kem_tieng_anh(None) is False


def test_tai_de_hoc_sinh_da_tick_anh_ra_zip_mac_dinh(monkeypatch):
    """Đề của học sinh có bản Anh song sinh: /tai-de và /tai-loigiai mặc định ra .zip Việt+Anh dù trang ở ngôn ngữ nào;
    đề không có bản Anh ra PDF Việt thường; đề giáo viên vẫn theo ngôn ngữ trang."""
    import io
    import zipfile
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.main import app

    def gia(tex, lang="vi"):
        from app.services.pdf_service import EXPORTS_DIR
        out = (R.EXPORTS_DIR_EN if lang == "en" else EXPORTS_DIR)
        out.mkdir(parents=True, exist_ok=True)
        pdf = out / (Path(tex).stem + ".pdf")
        pdf.write_bytes(b"%PDF-1.4 " + Path(tex).read_bytes()[:2000])
        return pdf
    monkeypatch.setattr(A, "compile_pdf", gia)
    monkeypatch.setattr(R, "compile_pdf", gia)
    co_anh = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="1", dapan_tieng_anh=True)
    chi_viet = A.generate_exam_pdf_auto(10, "ĐỀ", "student", "HeSo1", pham_vi_chuong="1", dapan_tieng_anh=False)
    assert not A.duong_tex_en(chi_viet["tex_path"]).exists()          # không tick: không sinh gì của bản Anh
    de = {"id": "de-hs", "role": "student",
          "files": {"dapan_json": co_anh["dap_an_json_path"], "tex": co_anh["tex_path"], "de": co_anh["pdf_path"]}}
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    monkeypatch.setattr(history_service, "luu_file_de", lambda *a, **k: None)
    client = TestClient(app)
    for lang in ("vi", "en"):
        for duong in ("tai-de", "tai-loigiai"):
            r = client.get("/api/exam/%s/de-hs" % duong, cookies={"lang": lang})
            assert r.headers["content-type"] == "application/zip", (lang, duong)
            assert len(zipfile.ZipFile(io.BytesIO(r.content)).namelist()) == 2
    de["files"] = {"dapan_json": chi_viet["dap_an_json_path"], "tex": chi_viet["tex_path"], "de": chi_viet["pdf_path"]}
    r = client.get("/api/exam/tai-de/de-hs", cookies={"lang": "en"})
    assert r.headers["content-type"] == "application/pdf"             # không tick: chỉ có bản Việt
    q = client.get("/api/exam/quiz/de-hs", cookies={"lang": "en"}).json()["data"]
    assert q["co_ban_tieng_anh"] is False and "no English version" in q["thong_bao_ban_anh"]
    de["files"] = {"dapan_json": co_anh["dap_an_json_path"], "tex": co_anh["tex_path"], "de": co_anh["pdf_path"]}
    assert client.get("/api/exam/quiz/de-hs", cookies={"lang": "en"}).json()["data"]["co_ban_tieng_anh"] is True
    de["role"] = "teacher"                                              # giáo viên: vẫn theo ngôn ngữ trang
    assert client.get("/api/exam/tai-de/de-hs", cookies={"lang": "vi"}).headers["content-type"] == "application/pdf"


def test_giao_vien_tick_tieng_anh_ba_lien_ket_tieng_anh_tai_duoc_khong_can_file_de(monkeypatch):
    """Lỗi 03/10/2026: 3 liên kết tiếng Anh (PDF đề, PDF lời giải, .tex) báo "không có bản tiếng Anh" vì chúng
    đọc loại tệp de_en/loigiai_en/tex_en trong bảng file_de mà CHECK constraint từ chối. Nay bản Anh nằm cạnh bản
    Việt, cùng tên: chỉ cần files = {tex, de, ...} của đề (không có khoá *_en nào) là tải được."""
    from fastapi.testclient import TestClient
    import app.routers.exam as R
    import app.services.exam_assembler_service as A
    from app.services import history_service
    from app.services.pdf_service import EXPORTS_DIR
    from app.main import app

    def gia(tex, lang="vi"):
        out = (R.EXPORTS_DIR_EN if lang == "en" else EXPORTS_DIR)
        out.mkdir(parents=True, exist_ok=True)
        pdf = out / (Path(tex).stem + ".pdf")
        pdf.write_bytes(b"%PDF-1.4 " + lang.encode() + b" " + Path(tex).read_bytes()[:1500])
        return pdf
    monkeypatch.setattr(A, "compile_pdf", gia)
    monkeypatch.setattr(R, "compile_pdf", gia)
    kq = A.generate_exam_pdf_auto(10, "ĐỀ KIỂM TRA", "teacher", "HeSo1", pham_vi_chuong="1",
                                  kem_tieng_anh=True, tieu_de_en="QUIZ")
    files = {"de": kq["pdf_path"], "tex": kq["tex_path"]}
    if kq.get("pdf_loigiai_path"):
        files["loigiai"] = kq["pdf_loigiai_path"]
    de = {"id": "de-gv-anh", "role": "teacher", "files": files}
    assert not any(k.endswith("_en") for k in de["files"])
    monkeypatch.setattr(history_service, "lay_de_theo_id", lambda de_id: de)
    monkeypatch.setattr(history_service, "luu_file_de", lambda *a, **k: None)
    monkeypatch.setattr(R, "yeu_cau_giao_vien", lambda request, user=None: None)
    client = TestClient(app)
    for duong in ("tai-de-en", "tai-loigiai-en", "tai-tex-en"):
        r = client.get("/api/exam/%s/de-gv-anh" % duong)
        assert r.status_code == 200, (duong, r.text[:200])
    assert b"ex_test_en" in client.get("/api/exam/tai-tex-en/de-gv-anh").content
    # .tex bị dọn sau 1 ngày: PDF Anh đã lưu sẵn vẫn tải được, còn .tex Anh thì báo rõ
    A.duong_tex_en(kq["tex_path"]).unlink()
    assert client.get("/api/exam/tai-de-en/de-gv-anh").status_code == 200
    assert client.get("/api/exam/tai-tex-en/de-gv-anh").status_code == 404
