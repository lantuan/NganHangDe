"""Kéo pháo ở Điện Biên Phủ (cô Lan 23/10/2026, duyệt kế hoạch): MC_C/SA_C _02 (bổ sung người), _03 (dây kéo xiên -
định lí sin), _04 (kéo pháo ra, ghìm bằng dây), TL L10_C4_VD040_VD060_TL_A, TF L10_C4_TF_D. Kiểm ĐỘC LẬP: đọc số liệu
trong đề, tự tính lại đáp số; góc dốc trong khoảng có nguồn (kéo lên 30-50 độ, ghìm xuống tới 60 độ); thông tin thật chỉ
ở câu dẫn; Mapping cùng bối cảnh."""
import importlib.util
import json
import math
import random
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_sp = importlib.util.spec_from_file_location("L10_C4_dbp_test", GOC / "data" / "python_bank" / "toan10" / "L10_C4.py")
M = importlib.util.module_from_spec(_sp)
sys.modules["L10_C4_dbp_test"] = M
_sp.loader.exec_module(M)


def _de(t):
    return t.split("\\loigiai")[0]


def _so(s):
    return float(s.replace("\\,", "").replace(",", "."))


def _doc(de):
    P = _so(re.search(r"trọng lượng \$([\d\\,]+)\$ N", de).group(1))
    a = int(re.search(r"dốc nghiêng \$(\d+)\^\\circ\$", de).group(1))
    return P, a


def _dap_mc(t):
    return re.search(r"\{\\True \$([^$]*)\$", t).group(1)


def _dap_sa(t):
    return re.search(r"\\shortans\{\s*\$([^$]*)\$\}", t).group(1).strip()


def test_bo_sung_nguoi():
    for sd in range(80):
        random.seed(sd)
        for f, dap in ((M.L10_C4_B8_VD040_MC_C_02, _dap_mc), (M.L10_C4_B8_VD040_SA_C_02, _dap_sa)):
            t = f(1)
            de = _de(t)
            P, a = _doc(de)
            assert 30 <= a <= 50 and "$40^\\circ$ đến $50^\\circ$" in de and "$30$ người" in de
            fn = int(re.search(r"mỗi người kéo được một lực \$(\d+)\$ N", de).group(1))
            n = math.ceil(P * math.sin(math.radians(a)) / fn - 1e-9)
            assert int(dap(t)) == n - 30, (sd, de)


def test_day_keo_xien_dinh_li_sin():
    for sd in range(80):
        random.seed(sd)
        for f, dap in ((M.L10_C4_B8_VD040_MC_C_03, _dap_mc), (M.L10_C4_B8_VD040_SA_C_03, _dap_sa)):
            t = f(1)
            de = _de(t)
            P, a = _doc(de)
            b = int(re.search(r"hợp với mặt dốc một góc \$(\d+)\^\\circ\$", de).group(1))
            fn = int(re.search(r"lực \$(\d+)\$ N theo phương của dây", de).group(1))
            n = math.ceil(P * math.sin(math.radians(a)) / math.cos(math.radians(b)) / fn - 1e-9)
            assert int(dap(t)) == n and "định lí sin" in t


def test_keo_phao_ra_ghim_bang_day():
    gap = set()
    for sd in range(120):
        random.seed(sd)
        for f, dap in ((M.L10_C4_B8_VD040_MC_C_04, _dap_mc), (M.L10_C4_B8_VD040_SA_C_04, _dap_sa)):
            t = f(1)
            de = _de(t)
            P, a = _doc(de)
            assert 30 <= a <= 60 and "Tô Vĩnh Diện" in de and "dốc Chuối" in de
            Fk = P * math.sin(math.radians(a))
            m_t0 = re.search(r"lực căng tối đa \$([\d\\,]+)\$ N", de)
            if m_t0:
                gap.add("so_day")
                assert int(dap(t)) == math.ceil(Fk / _so(m_t0.group(1)) - 1e-9)
            else:
                gap.add("dut_day")
                k = int(re.search(r"ghìm bằng \$(\d+)\$ sợi dây", de).group(1))
                assert abs(int(dap(t)) - Fk / (k - 1)) <= 0.5 + 1e-6
    assert gap == {"so_day", "dut_day"}


def test_tu_luan_so_nguoi_va_cong():
    for sd in range(60):
        random.seed(sd)
        t = M.L10_C4_VD040_VD060_TL_A_01(1)
        de = _de(t)
        P = _so(re.search(r"trọng lượng \$([\d\\,]+)\$ N", de).group(1))
        a = int(re.search(r"nghiêng \$(\d+)\^\\circ\$", de).group(1))
        d = int(re.search(r"dài \$(\d+)\$ m, nghiêng", de).group(1))
        fn = int(re.search(r"lực \$(\d+)\$ N\. Cần", de).group(1))
        ys = re.findall(r"\\SA\[4\]\{\$([^$]*)\$\}", t)
        assert int(ys[0]) == math.ceil(P * math.sin(math.radians(a)) / fn - 1e-9)
        A = P * math.sin(math.radians(a)) * d / 1000
        assert abs(int(re.search(r"approx (\d+)", ys[1]).group(1)) - A) <= 0.5 + 1e-6
        assert "Dốc Bảy Tời" in de and "$7$ tời" in de and d == 350


def test_dung_sai_moi_y_du_dung_sai():
    for sd in range(40):
        random.seed(sd)
        t = M.L10_C4_TF_D_01(1)
        assert t.count("\\True") >= 1 and "Điện Biên Phủ" in t


def test_mapping_cung_boi_canh():
    rows = {r["id"]: r for r in json.load(open(GOC / "data/mapping/toan10/L10_C4.json", encoding="utf-8"))}
    for i in ("L10_C4_B8_VD040_MC_C", "L10_C4_B8_VD040_SA_C", "L10_C4_VD040_VD060_TL_A", "L10_C4_TF_D"):
        assert "keo_phao_dien_bien_phu" in rows[i]["boi_canh"] and rows[i]["ngoai_yccd"]
    assert rows["L10_C4_B8_VD040_MC_C"]["Dang"] == rows["L10_C4_B8_VD040_SA_C"]["Dang"]
    assert [y["curriculum_id"] for y in rows["L10_C4_VD040_VD060_TL_A"]["cac_y"]] == ["L10_C4_B8_VD040", "L10_C4_B11_VD060"]


def test_dung_sai_ngoai_pham_vi_bai_khong_vao_de_giua_ky():
    """L10_C4_TF_B (toạ độ, tích vô hướng - Bài 10, 11) không vào đề giữa kỳ 1 (chương 4 tới Bài 8)."""
    from app.services.question_selector_service import select_questions, _bai_cua_tf
    rows = {r["id"]: r for r in json.load(open(GOC / "data/mapping/toan10/L10_C4.json", encoding="utf-8"))}
    assert _bai_cua_tf(10, 4, rows["L10_C4_TF_B"]) == {"L10_C4_B10", "L10_C4_B11"}
    bp = {"pham_vi_bai": ["L10_C4_B7", "L10_C4_B8"], "dung_sai": [{"chuong_so": 4, "so_cau": 1}],
          "trac_nghiem": [], "tra_loi_ngan": [], "tu_luan": []}
    gap = {select_questions(10, bp)[0]["generator_id"] for _ in range(40)}
    assert gap and gap <= {"L10_C4_TF_C", "L10_C4_TF_D"}
