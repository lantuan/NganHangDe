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
