"""Câu có hình vẽ phải có ảnh trên trang làm bài (lỗi cô Lan phát hiện 24/10/2026).

Lỗi: commit 23/10/2026 (khoá sinh câu) dời bước dịch hình ra sau khoá, nhưng đưa vào hàng chờ cái dict
`dap_an` trong khi tệp đáp án ghi `ban_ghi = {**dap_an}` - một dict KHÁC. Ảnh vẫn được dịch vào
data/hinh_cache nhưng tệp đáp án không có trường "hinh" -> MỌI câu có hình đều hiện
"Câu này có hình vẽ, web chưa hiển thị được" và mất luôn các phương án.
"""
import json
from pathlib import Path

from app.services import exam_assembler_service as A
from app.routers import exam as R

# Một câu MC có hình đúng dạng math_type.MC_SA_answer_text sinh ra (\immini{đề}{hình}).
KHOI_CO_HINH = r"""\begin{ex}%%[L10_C3_B5_NB029_MC_F_01]
\immini{
Cho điểm $M$ như hình vẽ. Khẳng định nào sau đây \textbf{đúng}?}
{\begin{tikzpicture}
\draw (0,0) -- (1,1);
\end{tikzpicture}}
\choice{\True $a$}{$b$}{$c$}{$d$}

\loigiai{
Giải.
}
\end{ex}
"""


def test_tep_dap_an_co_truong_hinh(monkeypatch, tmp_path):
    monkeypatch.setattr(A, "TEMP_DIR", tmp_path)
    monkeypatch.setattr(A, "dich_hinh_trong_khoi", lambda *_a: ["mahinhgia"])
    monkeypatch.setattr(A, "call_generator",
                        lambda **k: {"latex_block": KHOI_CO_HINH, "generator_id": "L10_C3_B5_NB029_MC_F_01"})
    ds = [{"generator_id": "L10_C3_B5_NB029_MC_F", "loai_cau": "MC", "chuong_so": 3}]
    kq = A._sinh_pdf_tu_danh_sach(10, "T", "student", ds, 1, lang="vi", seed=1, chi_dap_an=True)
    dap_an = json.loads(Path(kq["dap_an_json_path"]).read_text(encoding="utf-8"))
    assert dap_an[0]["hinh"] == ["mahinhgia"]


def test_de_cu_thieu_hinh_lay_lai_anh_trong_kho(monkeypatch):
    """Đề đã tạo trong lúc lỗi: tệp đáp án có hinh_tikz mà thiếu "hinh" -> trang làm bài lấy ảnh có sẵn."""
    monkeypatch.setattr(R, "duong_dan_anh", lambda ma: Path("/x.svg"))
    tikz = "\\begin{tikzpicture}\n\\draw (0,0) -- (1,1);\n\\end{tikzpicture}"
    cau = {"loai_cau": "MC", "co_hinh_ve": True, "hinh_tikz": [tikz]}
    assert R._bu_anh_tu_kho(cau)["hinh"] == [R.ma_hinh(tikz)]
    # Không có ảnh trong kho thì để nguyên (web vẫn báo xem PDF như cũ)
    monkeypatch.setattr(R, "duong_dan_anh", lambda ma: None)
    assert not R._bu_anh_tu_kho({"hinh_tikz": [tikz]}).get("hinh")


# ---------------------------------------------------------------------------------------------------------------
# Chấm bài khi web chưa hiện được hình (cô Lan 24/10/2026): câu đó không tính điểm (không trừ oan), vẫn có dòng
# kết quả để học sinh bấm hỏi thầy/cô AI; máy chủ tự kiểm lại, không tin cờ của trình duyệt.
# ---------------------------------------------------------------------------------------------------------------
def _de_gia(monkeypatch, tmp_path, cau_mc1_co_anh: bool):
    tikz = "\\begin{tikzpicture}\n\\draw (0,0) -- (1,1);\n\\end{tikzpicture}"
    ds = [
        {"so_thu_tu": 1, "loai_cau": "MC", "dap_an_dung": "A", "generator_id": "L10_C3_B5_NB029_MC_F_01",
         "co_hinh_ve": True, "hinh_tikz": [tikz], "loi_giai": "g"},
        {"so_thu_tu": 2, "loai_cau": "MC", "dap_an_dung": "B", "generator_id": "L10_C3_B6_NB032_MC_A_01",
         "loi_giai": "g"},
        {"so_thu_tu": 3, "loai_cau": "TF", "dap_an_dung": {"a": True, "b": False, "c": True, "d": False},
         "generator_id": "L10_C3_TF_T_01", "co_hinh_ve": True, "hinh_tikz": [tikz], "loi_giai": "g"},
    ]
    p = tmp_path / "x_dapan.json"
    p.write_text(json.dumps(ds), encoding="utf-8")
    monkeypatch.setattr(R.history_service, "lay_de_theo_id", lambda _i: {"id": "d1", "files": {"dapan_json": str(p)}})
    monkeypatch.setattr(R.history_service, "luu_ket_qua_cham_bai", lambda **k: None)
    monkeypatch.setattr(R, "duong_dan_anh", lambda ma: Path("/x.svg") if cau_mc1_co_anh else None)


def _cham(bai_lam):
    from fastapi.testclient import TestClient
    from app.main import app
    r = TestClient(app).post("/api/exam/grade", json={"de_id": "d1", "bai_lam": bai_lam})
    assert r.status_code == 200, r.text
    return r.json()["data"]


def test_cau_chua_hien_hinh_khong_tinh_diem(monkeypatch, tmp_path):
    _de_gia(monkeypatch, tmp_path, cau_mc1_co_anh=False)
    kq = _cham([{"so_thu_tu": 1, "cau_tra_loi": None, "chua_hien_hinh": True},
                {"so_thu_tu": 2, "cau_tra_loi": "B"},
                {"so_thu_tu": 3, "cau_tra_loi": None, "chua_hien_hinh": True}])
    theo = {c["so_thu_tu"]: c for c in kq["chi_tiet"]}
    assert theo[1]["trang_thai"] == "chua_hien_hinh" and theo[1]["diem_toi_da"] == 0
    assert theo[3]["trang_thai"] == "chua_hien_hinh" and theo[3]["loai_cau"] == "TF"
    # chỉ còn câu 2 được tính: làm đúng thì đạt TRỌN điểm tối đa còn lại
    assert kq["diem_tren_10_tam_tinh"] == kq["diem_toi_da_tu_dong"] > 0


def test_khong_cho_tu_danh_dau_cau_da_co_hinh(monkeypatch, tmp_path):
    """Hình đã hiện (có ảnh) mà trình duyệt vẫn gửi cờ chua_hien_hinh -> chấm như thường."""
    _de_gia(monkeypatch, tmp_path, cau_mc1_co_anh=True)
    kq = _cham([{"so_thu_tu": 1, "cau_tra_loi": None, "chua_hien_hinh": True},
                {"so_thu_tu": 2, "cau_tra_loi": "B"}])
    theo = {c["so_thu_tu"]: c for c in kq["chi_tiet"]}
    assert theo[1].get("trang_thai") != "chua_hien_hinh" and theo[1]["dung_sai_hoac_diem"] is False
    # cờ giả của câu không có hình cũng bị bỏ qua
    kq2 = _cham([{"so_thu_tu": 2, "cau_tra_loi": "A", "chua_hien_hinh": True}])
    assert kq2["chi_tiet"][0]["dung_sai_hoac_diem"] is False
