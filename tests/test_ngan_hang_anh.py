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


def test_ban_anh_L10_C1_tuong_duong_ban_viet():
    kt = _nap_script("kiem_tuong_duong")
    tong, bad = kt.so_sanh("L10_C1", n=4)
    bad = {t: v for t, v in bad.items() if t not in CHO_PHEP_LECH}
    assert tong >= 160
    assert not bad, "Ban Anh lech ban Viet: %s" % list(bad.items())[:3]


def test_ban_anh_sinh_ra_tu_ban_viet_khong_sua_tay():
    """data/python_bank_en/... phải đúng bằng kết quả của scripts/dich_ngan_hang.py (từ điển + patch)."""
    dich = _nap_script("dich_ngan_hang")
    nguon = GOC / "data" / "python_bank" / "toan10" / "L10_C1.py"
    src, chua, loi = dich.dich_tep(nguon)
    assert not chua, "Con %d doan chua dich" % len(chua)
    assert not loi, "Loi dich: %s" % loi[:3]
    hien_co = (GOC / "data" / "python_bank_en" / "toan10" / "L10_C1.py").read_text(encoding="utf-8")
    assert src == hien_co, "Ban Anh khac ket qua dich - chay: python3 scripts/dich_ngan_hang.py dich <tep>"


def test_ban_anh_khong_con_chu_viet():
    src = (GOC / "data" / "python_bank_en" / "toan10" / "L10_C1.py").read_text(encoding="utf-8")
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
