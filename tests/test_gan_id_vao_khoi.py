"""Co Lan 13/10/2026: sau moi \\begin{ex} (va \\begin{bt} cua tu luan) la %%[ID ham sinh ra cau do], thay cho dau ?."""
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "data" / "python_bank"))

from app.services import exam_assembler_service as A
from app.services import generator_service as G
from app.services.answer_parser_service import trich_de_bai


def test_gan_id_thay_dau_hoi_va_giu_nguyen_phan_con_lai():
    khoi = "\\begin{ex}%%[?]\nDe bai 1\n\\end{ex}\n\\begin{ex}%%[?]\nDe bai 2\n\\end{ex}\n"
    kq = G.gan_id_vao_khoi(khoi, "L10_C3_B6_VD036_MC_J_02")
    assert kq.count("\\begin{ex}%%[L10_C3_B6_VD036_MC_J_02]\n") == 2 and "?" not in kq
    # khoi chua co dong chu thich thi them vao; dat lai lan nua khong nhan doi
    assert G.gan_id_vao_khoi("\\begin{ex}\nx\\end{ex}", "ID_1").startswith("\\begin{ex}%%[ID_1]\n")
    assert G.gan_id_vao_khoi(kq, "ID_2").count("%%[ID_2]") == 2
    assert G.gan_id_vao_khoi("\\begin{bt}%%[?]\nx\\end{bt}", "ID_3").startswith("\\begin{bt}%%[ID_3]")


def _thu(gid, lop=10, chuong=3):
    import random
    random.seed(1)
    kq = G.call_generator(gid, lop, chuong, "teacher", 1)
    return kq["variant_used"], kq["latex_block"]


def test_call_generator_ghi_dung_ten_ham():
    for gid in ("L10_C3_B6_VD036_MC_J", "L10_C3_B6_VD036_SA_L", "L10_C3_B6_VD036_TL_I"):
        ten, khoi = _thu(gid)
        assert ten.startswith(gid + "_")
        assert re.search(r"\\begin\{ex\}%%\[" + re.escape(ten) + r"\]\n", khoi), khoi[:80]


def test_id_di_theo_sang_te_phan_tu_luan_bt():
    ten, khoi = _thu("L10_C3_B6_VD036_TL_I")
    than = A._ghep_4_phan({"TL": [khoi]})
    assert "\\begin{bt}%%[" + ten + "]" in than and "\\begin{ex}" not in than


def test_web_van_cat_duoc_de_bai_khi_co_id():
    ten, khoi = _thu("L10_C3_B6_VD036_SA_L")
    kq = trich_de_bai(khoi)
    assert "%%[" not in kq["de_bai"] and ten not in kq["de_bai"]
