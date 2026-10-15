"""L10_C2_B3_VD025 (15/10/2026, co Lan: Bai 3 muc VD, de thuc te): lap mot bat phuong trinh bac nhat hai an tu tinh huong
+ dieu kien them -> gia tri nguyen lon nhat.

Dap so TINH LAI DOC LAP tu chinh van ban de bai: doc so lieu bang regex roi VET CAN cac so tu nhien (khong giai bat phuong
trinh), kiem tra phuong an nhieu, boi canh dung danh sach trong Mapping.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
_spec = importlib.util.spec_from_file_location("L10_C2_vd025", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_vd025"] = M
_spec.loader.exec_module(M)

SO_LAN = 400


def _bat(ham, seed, dang):
    cap = []
    goc = M.MC_SA_answer_const
    M.MC_SA_answer_const = lambda debai, dap, nhieu, giai, *a, **k: cap.append((debai, str(dap), list(nhieu), giai)) or ""
    try:
        M._rd.seed(seed)
        ham(1, dang=dang)
    finally:
        M.MC_SA_answer_const = goc
    assert len(cap) == 1
    return cap[0]


def _so(s):
    return int(s.replace(r"\,", ""))


def _lon_nhat(dieu_kien, tren=2000):
    """Vet can: so tu nhien lon nhat thoa dieu_kien."""
    ok = [v for v in range(tren + 1) if dieu_kien(v)]
    assert ok and ok[-1] < tren
    return ok[-1]


def _dap_so_doc_lap(debai):
    m = re.search(r"tải trọng tối đa \$(\d+)\$ kg\. Coi mỗi người có khối lượng \$(\d+)\$ kg, mỗi thùng hàng có khối "
                  r"lượng \$(\d+)\$ kg\.", debai)
    if m:
        T, p, q = map(int, m.groups())
        y = re.search(r"Thang máy đang chở \$(\d+)\$ thùng hàng", debai)
        if y:
            y0 = int(y.group(1))
            return "thang_may", _lon_nhat(lambda x: p * x + q * y0 <= T)
        k = {"một": 1, "hai": 2}[re.search(r"mang theo (một|hai) thùng hàng", debai).group(1)]
        return "thang_may", _lon_nhat(lambda x: p * x + q * k * x <= T)
    m = re.search(r"mua \$(\d+)\$ vé xem phim, gồm vé thường giá \$(\d+)\$ nghìn đồng/vé và vé VIP giá \$(\d+)\$ nghìn "
                  r"đồng/vé\. Số tiền mua vé không vượt quá \$([\d\\,]+)\$ nghìn đồng", debai)
    if m:
        N, a, b, T = int(m.group(1)), int(m.group(2)), int(m.group(3)), _so(m.group(4))
        return "ve_xem_phim", _lon_nhat(lambda y: y <= N and a * (N - y) + b * y <= T, tren=N + 1)
    m = re.search(r"có \$35\$ học sinh, dùng quỹ lớp không quá \$([\d\\,]+)\$ nghìn đồng .+ nước giá \$(\d+)\$ nghìn "
                  r"đồng/chai, bánh giá \$(\d+)\$ nghìn đồng/hộp\. Lớp mua cho mỗi bạn đúng một chai nước", debai)
    if m:
        T, b, a = _so(m.group(1)), int(m.group(2)), int(m.group(3))
        return "quy_lop_lien_hoan", _lon_nhat(lambda y: b * 35 + a * y <= T)
    m = re.search(r"mua \$(\d+)\$ cuốn sách, gồm sách tham khảo giá \$(\d+)\$ nghìn đồng/cuốn và truyện giá \$(\d+)\$ "
                  r"nghìn đồng/cuốn, với kinh phí không quá \$([\d\\,]+)\$ nghìn đồng", debai)
    assert m, debai
    N, a, b, T = int(m.group(1)), int(m.group(2)), int(m.group(3)), _so(m.group(4))
    return "thu_vien_mua_sach", _lon_nhat(lambda x: x <= N and a * x + b * (N - x) <= T, tren=N + 1)


def test_sa_dap_so_doc_lap_va_du_boi_canh():
    thay = set()
    for s in range(SO_LAN):
        debai, dap, nhieu, giai = _bat(M.L10_C2_B3_VD025_SA_A_01, s, 2)
        bc, n = _dap_so_doc_lap(debai)
        assert int(dap) == n and n >= 3, (s, debai)
        assert "nhiều nhất $%d$" % n in giai
        assert len({v for v in nhieu if v != dap}) >= 3 and all(int(v) > 0 for v in nhieu)
        thay.add(bc)
    assert thay == {"thang_may", "ve_xem_phim", "quy_lop_lien_hoan", "thu_vien_mua_sach"}


def test_mc_cung_de_voi_sa():
    for s in range(60):
        M._rd.seed(s)
        o_mc = M.L10_C2_B3_VD025_MC_A_01(1)
        M._rd.seed(s)
        o_sa = M.L10_C2_B3_VD025_SA_A_01(1)
        assert r"\choice" in o_mc and r"\shortans" not in o_mc and r"\shortans" in o_sa and r"\choice" not in o_sa
        assert o_mc.split(r"\choice")[0].strip() == o_sa.split(r"\shortans")[0].strip()


def test_mapping_boi_canh_va_curriculum():
    m = {r["id"]: r for r in json.load(open(GOC / "data" / "mapping" / "toan10" / "L10_C2.json", encoding="utf-8"))}
    for i in ("L10_C2_B3_VD025_MC_A", "L10_C2_B3_VD025_SA_A"):
        assert set(m[i]["boi_canh"]) == {"thang_may", "ve_xem_phim", "quy_lop_lien_hoan", "thu_vien_mua_sach"}
        assert not m[i].get("ngoai_yccd")
    assert m["L10_C2_B3_VD025_MC_A"]["Dang"] == m["L10_C2_B3_VD025_SA_A"]["Dang"]
    # boi canh moi: khong trung boi canh nao khac trong ca ngan hang lop 10
    khac = set()
    for f in (GOC / "data" / "mapping" / "toan10").glob("*.json"):
        for r in json.load(open(f, encoding="utf-8")):
            if "VD025" in r["id"]:
                continue
            bc = r.get("boi_canh")
            khac.update(bc if isinstance(bc, list) else [bc] if bc else [])
    assert not khac & set(m["L10_C2_B3_VD025_MC_A"]["boi_canh"])
    cur = {u["id"]: u for u in json.load(open(GOC / "data" / "curriculum" / "toan10" / "L10_C2.json", encoding="utf-8"))}
    assert cur["L10_C2_B3_VD025"]["MucDo"] == "VD"
