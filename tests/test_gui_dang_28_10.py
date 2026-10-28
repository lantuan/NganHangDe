"""Gửi dạng / Duyệt dạng (cô Lan 28/10/2026): giáo viên dùng Gem Gemini cô chia sẻ để viết hàm Python, dán vào
/gv/gui-dang; cô tải về máy chạy thử (scripts/thu_dang_gui.py), đưa vào ngân hàng như mọi lần rồi bấm Đã duyệt.
Máy chủ KHÔNG chạy code gửi lên, chỉ đọc cú pháp."""
import importlib.util
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import teacher as R
from app.services import gui_dang_service as G

GOC = Path(__file__).resolve().parent.parent
MAU = (GOC / "docs" / "gem_soan_dang" / "ham_mau.py").read_text(encoding="utf-8")
CODE = MAU.split("if __name__ ==")[0].replace("from math_type import *", "")


@pytest.fixture
def kho(monkeypatch, tmp_path):
    monkeypatch.setattr(G, "THU_MUC", tmp_path / "gui_dang")
    return tmp_path / "gui_dang"


def test_kiem_code():
    with pytest.raises(G.GuiDangError, match="cú pháp"):
        G.kiem_code("def L10_C3_B6_TH032_MC_X_01(socau, dang=1)\n  return 1")
    with pytest.raises(G.GuiDangError, match="theo ID"):
        G.kiem_code("def ham(socau):\n    return ''")
    with pytest.raises(G.GuiDangError, match="Chưa dán"):
        G.kiem_code("   ")
    k = G.kiem_code(CODE)
    assert k["ten_ham"] == ["L10_C3_B6_TH032_MC_X_01", "L10_C3_B6_TH032_SA_X_01", "L10_C3_TF_X_01",
                            "L10_C3_TH031_TH032_TL_X_01"] and not k["canh_bao"]
    xau = G.kiem_code("import os\nos.system('x')\ndef L10_C1_B1_NB001_MC_Z_01(socau, dang=1):\n    open('a')\n")
    assert "open(" in xau["canh_bao"] and "os." in xau["canh_bao"]
    assert any("ngoài hàm" in c for c in xau["canh_bao"])


def test_gui_luu_va_duyet(kho, monkeypatch):
    b = G.gui("gv1", "gv1@x", "PHIẾU GỬI DUYỆT\n- Hàm: ...", CODE, "Đề gốc")
    assert (kho / (b["ma"] + ".json")).exists() and b["trang_thai"] == "cho_duyet"
    assert [x["ma"] for x in G.danh_sach(gv_id="gv1")] == [b["ma"]] and G.danh_sach(gv_id="gv2") == []
    G.dat_trang_thai(b["ma"], "tra_lai", "Sai đáp số câu SA", "co@x")
    assert G.lay(b["ma"])["loi_nhan"] == "Sai đáp số câu SA" and G.danh_sach(trang_thai="cho_duyet") == []
    with pytest.raises(G.GuiDangError):
        G.dat_trang_thai("../../etc/passwd", "da_duyet", "", "co@x")       # mã lạ không đọc ngoài thư mục
    monkeypatch.setattr(G, "TOI_DA_MOI_NGAY", 1)
    with pytest.raises(G.GuiDangError, match="mai gửi tiếp"):
        G.gui("gv1", "gv1@x", "", CODE)


def test_tep_tai_ve_chay_thu_duoc(kho, tmp_path):
    """Tệp .py tải về (phiếu + import + code) chạy được bằng scripts/thu_dang_gui.py và các hàm mẫu ĐẠT."""
    b = G.gui("gv1", "gv1@x", "PHIẾU", CODE, "")
    tep = tmp_path / (b["ma"] + ".py")
    tep.write_text(G.tep_python(b), encoding="utf-8")
    sp = importlib.util.spec_from_file_location("thu_dang_gui", GOC / "scripts" / "thu_dang_gui.py")
    T = importlib.util.module_from_spec(sp)
    sys.modules["thu_dang_gui"] = T
    sp.loader.exec_module(T)
    mo = T._nap(tep)
    for ten in b["ten_ham"]:
        loi, _cb = T.kiem_ham(mo, ten, 15)
        assert loi == [], (ten, loi)
    # hàm hỏng thì bắt được
    hong = tmp_path / "hong.py"
    hong.write_text("def L10_C3_B6_TH032_SA_Y_01(socau, dang=2):\n"
                    "    return MC_SA_answer_const('x', '12{,}345', ['1','2','3'], 'g', 0, 0, dang)\n", encoding="utf-8")
    loi, _ = T.kiem_ham(T._nap(hong), "L10_C3_B6_TH032_SA_Y_01", 3)
    assert any("quá 4 kí tự" in x for x in loi)
    assert len(G.zip_cho_duyet()) > 100


class _U:
    def __init__(self, email):
        self.id, self.email = "gv-" + email, email


def _client(monkeypatch, email):
    monkeypatch.setattr(R, "get_current_user", lambda request: _U(email))
    monkeypatch.setattr(R, "yeu_cau_giao_vien", lambda request, user=None: None)
    return TestClient(app)


def test_trang_va_quyen(kho, monkeypatch):
    monkeypatch.setattr(G, "NGUOI_DUYET", {"co@x"})
    c = _client(monkeypatch, "gv@x")
    r = c.get("/gv/gui-dang")
    assert r.status_code == 200 and 'action="/gv/gui-dang"' in r.text and "Trang duyệt dạng" not in r.text
    r = c.post("/gv/gui-dang", data={"phieu": "P", "code": "x = (", "de_goc": ""})
    assert r.status_code == 200 and "cú pháp" in r.text and "x = (" in r.text              # giữ lại code đã dán
    r = c.post("/gv/gui-dang", data={"phieu": "P", "code": CODE, "de_goc": "D"}, follow_redirects=False)
    assert r.status_code == 303 and "/gv/gui-dang?da_gui=" in r.headers["location"]
    ma = G.danh_sach()[0]["ma"]
    assert ma in c.get(r.headers["location"]).text
    # giáo viên thường không vào được trang duyệt / tải code
    assert c.get("/gv/duyet-dang", follow_redirects=False).headers["location"] == "/gv/gui-dang"
    assert c.get("/gv/duyet-dang/%s.py" % ma, follow_redirects=False).status_code == 303
    # người duyệt
    c = _client(monkeypatch, "co@x")
    r = c.get("/gv/duyet-dang")
    assert r.status_code == 200 and ma in r.text and "L10_C3_TF_X_01" in r.text
    r = c.get("/gv/duyet-dang/%s.py" % ma)
    assert r.status_code == 200 and "from math_type import *" in r.text and "def L10_C3_TF_X_01" in r.text
    assert c.get("/gv/duyet-dang/tai-cho-duyet.zip").content[:2] == b"PK"
    r = c.post("/gv/duyet-dang/" + ma, data={"trang_thai": "da_duyet", "loi_nhan": "Đã thêm vào L10_C3"},
               follow_redirects=False)
    assert r.status_code == 303 and G.lay(ma)["trang_thai"] == "da_duyet"
    assert "(0 bài chờ duyệt)" in c.get("/gv/gui-dang").text                         # người duyệt thấy số bài chờ
    trang_gv = _client(monkeypatch, "gv@x").get("/gv/gui-dang").text                   # giáo viên thấy kết quả
    assert "Đã thêm vào L10_C3" in trang_gv and "Đã duyệt" in trang_gv


def test_khong_chay_code_tren_may_chu(kho, monkeypatch):
    """Code có lệnh chạy ngoài hàm vẫn chỉ được ĐỌC, không bao giờ chạy."""
    da_chay = GOC / "nhap" / "_khong_duoc_tao.txt"
    code = "open(%r, 'w').write('x')\ndef L10_C1_B1_NB001_MC_Z_01(socau, dang=1):\n    return ''\n" % str(da_chay)
    b = G.gui("gv1", "gv1@x", "", code)
    assert not da_chay.exists() and "open(" in b["canh_bao"]


def test_menu_co_gui_dang():
    html = (GOC / "app/templates/teacher/_base_gv.html").read_text(encoding="utf-8")
    assert '<a href="/gv/gui-dang"' in html
    assert "data/gui_dang/" in (GOC / ".gitignore").read_text(encoding="utf-8")
