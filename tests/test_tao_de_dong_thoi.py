"""Cả lớp tạo đề cùng lúc (cô Lan 23/10/2026: "36 máy vào một lúc và web không thể tạo ra đề đồng loạt được").

1. Biên dịch LaTeX xếp hàng (pdf_service.luot_bien_dich): không quá SO_BIEN_DICH_CUNG_LUC bản cùng lúc.
2. Sinh câu giữ KHOA_SINH: nhiều luồng sinh cùng lúc vẫn ra ĐÚNG đề mà hạt giống + trạng thái xoay vòng quy định
   (bản Anh song sinh khớp bản Việt).
3. Học sinh tạo đề trên web (bien_dich_sau): không chờ PDF - trả {de_id} ngay, PDF dịch ở nền / khi bấm tải.
"""
import json
import threading
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.services import exam_assembler_service as A
from app.services import generator_service as G
from app.services import pdf_service as P


def test_bien_dich_xep_hang(monkeypatch, tmp_path):
    dang, cao_nhat, khoa = [0], [0], threading.Lock()

    class _KQ:
        stdout = ""

    def _chay(*a, **k):
        with khoa:
            dang[0] += 1
            cao_nhat[0] = max(cao_nhat[0], dang[0])
        time.sleep(0.05)
        with khoa:
            dang[0] -= 1
        return _KQ()
    monkeypatch.setattr(P.subprocess, "run", _chay)
    monkeypatch.setattr(P, "EXPORTS_DIR", tmp_path)
    luong = [threading.Thread(target=lambda i=i: pytest.raises(P.PdfCompileError, P.compile_pdf,
                                                                tmp_path / ("d%d.tex" % i))) for i in range(8)]
    [t.start() for t in luong]
    [t.join() for t in luong]
    assert 1 <= cao_nhat[0] <= P.SO_BIEN_DICH_CUNG_LUC


def _danh_sach():
    from app.services.exam_blueprint_service import build_blueprint
    from app.services.question_selector_service import select_questions
    bp = build_blueprint(lop=10, loai_he_so="HeSo1", ki_thi="kiem_tra_thuong_xuyen", pham_vi_chuong="chuong_1")
    return select_questions(lop=10, blueprint=bp, cho_phep_thieu=True)


def test_sinh_cung_luc_van_dung_hat_giong(monkeypatch, tmp_path):
    monkeypatch.setattr(A, "dich_hinh_trong_khoi", lambda *_a: [])
    monkeypatch.setattr(A, "TEMP_DIR", tmp_path)
    ds = _danh_sach()
    goc = G.chup_trang_thai_xoay()
    ket_qua = {}

    def _sinh(i):
        kq = A._sinh_pdf_tu_danh_sach(10, "T", "student", ds, 1, lang="vi", seed=12345, chi_dap_an=True,
                                      trang_thai_xoay=goc)
        ket_qua[i] = [(c.get("generator_id"), c.get("dap_an_dung")) for c in
                      json.loads(Path(kq["dap_an_json_path"]).read_text(encoding="utf-8"))]

    def _tao_de_khac():                              # đề khác (hạt giống khác) sinh xen vào cùng lúc
        A._sinh_pdf_tu_danh_sach(10, "T", "student", ds, 1, lang="vi", seed=999, chi_dap_an=True)
    luong = [threading.Thread(target=f, args=a) for i in range(6) for f, a in ((_sinh, (i,)), (_tao_de_khac, ()))]
    [t.start() for t in luong]
    [t.join() for t in luong]
    assert len(ket_qua) == 6 and all(v == ket_qua[0] for v in ket_qua.values())
    assert len(ket_qua[0]) >= 3


def test_hoc_sinh_khong_cho_bien_dich(monkeypatch, tmp_path):
    def _cam(*_a, **_k):
        raise AssertionError("không được biên dịch PDF khi bien_dich_ngay=False")
    monkeypatch.setattr(A, "_bien_dich", _cam)
    monkeypatch.setattr(A, "dich_hinh_trong_khoi", lambda *_a: [])
    kq = A.generate_exam_pdf_auto(lop=10, tieu_de="T", role="student", loai_he_so="HeSo1",
                                  ki_thi="kiem_tra_thuong_xuyen", pham_vi_chuong="chuong_1", bien_dich_ngay=False)
    assert kq["cho_bien_dich"] and Path(kq["tex_path"]).exists() and Path(kq["dap_an_json_path"]).exists()
    assert kq["pdf_path"] == str(A.duong_pdf_de(kq["tex_path"]))
    with pytest.raises(AssertionError):                              # giáo viên vẫn chờ PDF như cũ
        A.generate_exam_pdf_auto(lop=10, tieu_de="T", role="teacher", loai_he_so="HeSo1",
                                 ki_thi="kiem_tra_thuong_xuyen", pham_vi_chuong="chuong_1", bien_dich_ngay=False)


def test_endpoint_tra_de_id_ngay_roi_dich_nen(monkeypatch, tmp_path):
    from app.main import app
    from app.routers import exam as E
    tex = tmp_path / "exam_abc.tex"
    tex.write_text("x", encoding="utf-8")
    monkeypatch.setattr(E.profile_service, "la_giao_vien", lambda uid: False)
    monkeypatch.setattr(E.history_service, "luu_de_da_sinh", lambda **kw: "de-1")
    luu = []
    monkeypatch.setattr(E.history_service, "luu_file_de", lambda *a: luu.append(a))
    nhan = {}
    monkeypatch.setattr(E, "generate_exam_pdf_auto",
                        lambda **kw: nhan.update(kw) or {"cho_bien_dich": not kw["bien_dich_ngay"],
                                                         "tex_path": str(tex), "pdf_path": str(tmp_path / "exam_abc.pdf"),
                                                         "dap_an_json_path": str(tmp_path / "d.json")})
    nen = []
    monkeypatch.setattr(E, "_bien_dich_nen_de_hoc_sinh", lambda t: nen.append(t))
    than = {"lop": 10, "tieu_de": "T", "role": "student", "loai_he_so": "HeSo1", "pham_vi_chuong": "chuong_1",
            "user_id": "u", "conversation_id": "c", "kem_tieng_anh": False, "chi_yccd": True}
    r = TestClient(app).post("/api/exam/generate-pdf-auto", json=dict(than, bien_dich_sau=True))
    assert r.status_code == 200 and r.json()["de_id"] == "de-1" and nhan["bien_dich_ngay"] is False
    assert nen == [str(tex)] and ("de-1", "de", str(tmp_path / "exam_abc.pdf")) in luu
    # n8n không gửi bien_dich_sau -> chờ PDF như cũ
    (tmp_path / "exam_abc.pdf").write_bytes(b"%PDF")
    nhan.clear()
    TestClient(app).post("/api/exam/generate-pdf-auto", json=than)
    assert nhan["bien_dich_ngay"] is True


def test_giao_dien_gui_bien_dich_sau():
    html = (Path(__file__).resolve().parent.parent / "app/templates/chat/chat.html").read_text(encoding="utf-8")
    assert html.count("bien_dich_sau: true") == 2


# ---------------------------------------------------------------- 23/10/2026: đề giữa kỳ ra câu Bài 10
def _bai(ds):
    import re
    ra = set()
    for d in ds:
        m = re.match(r"L10_C\d+_B\d+", d.get("generator_id") or "")
        if m:
            ra.add(m.group(0))
    return ra


def test_de_chuong_kem_ky_thi_chi_lay_bai_trong_ky():
    """Cô Lan: "tại sao bài diện tích lại ra trong đề thi giữa kỳ. Giữa kì chỉ tới bài 8 mà"."""
    from app.services.exam_blueprint_service import build_blueprint, BlueprintError
    from app.services.question_selector_service import select_questions
    gap = set()
    for _ in range(15):
        bp = build_blueprint(lop=10, loai_he_so="HeSo1", ki_thi="giua_ky_1", pham_vi_chuong="chuong_4")
        gap |= _bai(select_questions(lop=10, blueprint=bp, cho_phep_thieu=True))
    assert gap and gap <= {"L10_C4_B7", "L10_C4_B8"}
    with pytest.raises(BlueprintError, match="giữa kỳ 1"):
        build_blueprint(lop=10, loai_he_so="HeSo1", ki_thi="giua_ky_1", pham_vi_chuong="chuong_5")


def test_hinh_hai_luc_goc_vuong_ki_hieu_o_vuong():
    import importlib.util
    import sys
    goc = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(goc / "data" / "python_bank"))
    sp = importlib.util.spec_from_file_location("L10_C4_hinh_test", goc / "data/python_bank/toan10/L10_C4.py")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    vuong = m._b8_hinh_hai_luc(1, 3, 90, -15)
    assert "arc" not in vuong and "90^\\circ" not in vuong and vuong.count("--") == 4   # 2 mũi tên + ô vuông
    assert "arc" in m._b8_hinh_hai_luc(3, 5, 120, 0)
