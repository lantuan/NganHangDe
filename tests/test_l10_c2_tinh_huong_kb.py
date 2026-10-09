"""Tinh huong 2, 3, 4 (thuc an gia suc / phan xuong hai may / do uong an kieng) cua L10_C2.

Kiem lai DOC LAP: voi moi bo so sinh ra, vet can luoi nguyen de tim phuong an toi uu, roi so voi dap an
cua tung ham MC/SA/TL va nhan dung/sai cua TF. (co Lan 09/10/2026)
"""
import importlib.util
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "data" / "python_bank"))
sys.path.insert(0, str(GOC))
_spec = importlib.util.spec_from_file_location("L10_C2_kb_test", GOC / "data" / "python_bank" / "toan10" / "L10_C2.py")
M = importlib.util.module_from_spec(_spec)
sys.modules["L10_C2_kb_test"] = M
_spec.loader.exec_module(M)

SINH = {"2": M._kb2_sinh, "3": M._kb3_sinh, "4": M._kb4_sinh}
CHU = {"2": dict(nb="C", vd="D", vdc="E", tl="C", tf="D"), "3": dict(nb="D", vd="F", vdc="G", tl="D", tf="E"),
       "4": dict(nb="E", vd="H", vdc="I", tl="E", tf="F")}
_cap = {}


@pytest.fixture(autouse=True)
def _chup(monkeypatch):
    _cap.clear()
    monkeypatch.setattr(M, "MC_SA_answer_text", lambda d, dap, nh, g, *a: _cap.setdefault("mc", []).append((d, dap, list(nh), g)) or "")
    monkeypatch.setattr(M, "TL_answer_text", lambda d, ds, *a: _cap.setdefault("tl", []).append((d, ds)) or "")
    monkeypatch.setattr(M, "TF_baitoan_du", lambda d, ys, *a, **k: _cap.__setitem__("tf", (d, ys)) or "")


def _vet_can(t):
    """Vet can luoi nguyen: (cac diem thoa, gia tri F toi uu, tap phuong an toi uu)."""
    rb = t["rb"]
    K = max(max(v) for v in t["dinh"]) + 3
    ok = []
    for X in range(0, K + 1):
        for Y in range(0, K + 1):
            if all((r["a"] * X + r["b"] * Y <= r["c"]) if r["dau"] == r"\le" else (r["a"] * X + r["b"] * Y >= r["c"]) for r in rb):
                ok.append((X, Y))
    f = lambda P: t["cx"] * P[0] + t["cy"] * P[1]
    best = (max if t["kind"] == "max" else min)(f(P) for P in ok)
    return ok, best, [P for P in ok if f(P) == best]


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_sinh_toi_uu_duy_nhat_va_dung(k):
    for _ in range(80):
        t = SINH[k]()
        ok, best, opt = _vet_can(t)
        assert opt == [t["opt"]], (t["de"], opt, t["opt"])
        assert best == t["best"]
        assert t["kind"] == ("max" if k == "3" else "min")
        assert len(t["dinh"]) in (3, 4, 5)
        assert t["opt"] in t["dinh"]


def _chup_t(k):
    ghi = []

    def KB():
        t = SINH[k]()
        ghi.append(t)
        return t
    return KB, ghi


@pytest.mark.parametrize("k", ["2", "3", "4"])
@pytest.mark.parametrize("sa", [False, True])
def test_vdc_dap_an_doc_lap(k, sa):
    import re
    for hoi in ("gt", "x", "y"):
        for _ in range(40):
            _cap.clear()
            KB, ghi = _chup_t(k)
            M._kb_toi_uu(KB, 1, 2 if sa else 1, hoi, sa)
            t = ghi[0]
            debai, dap, nh, giai = _cap["mc"][0]
            ok, best, opt = _vet_can(t)
            mong = best if hoi == "gt" else opt[0][0 if hoi == "x" else 1]
            if hoi == "gt" and not sa:
                # "$1{,}95$ triệu đồng" -> đổi về nghìn đồng
                so = M.Fraction(re.search(r"\$([\d{},]+)\$", dap).group(1).replace("{,}", "."))
                assert so * t["chia"] == mong, (dap, mong)
            else:
                assert int(re.sub(r"\D", "", dap)) == mong, (dap, mong)
            assert dap not in nh and len(set(nh)) == len(nh)


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_vd_dap_an_doc_lap(k):
    for kieu in ("pa", "gt"):
        for _ in range(40):
            _cap.clear()
            KB, ghi = _chup_t(k)
            M._kb_mc_vd(KB, 1, 1, kieu)
            t = ghi[-1]
            debai, dap, nh, giai = _cap["mc"][0]
            ok, best, opt = _vet_can(t)
            if kieu == "pa":
                import re
                X, Y = map(int, re.findall(r"\d+", dap))
                assert (X, Y) in ok
                for d in nh:
                    X, Y = map(int, re.findall(r"\d+", d))
                    assert (X, Y) not in ok
            assert dap not in nh


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_sa_dinh_va_gioi_han(k):
    import re
    for hoi in ("dinh", "xcuc", "ycuc"):
        for _ in range(40):
            _cap.clear()
            KB, ghi = _chup_t(k)
            M._kb_sa_vd(KB, 1, 2, hoi)
            t = ghi[0]
            debai, dap, nh, giai = _cap["mc"][0]
            ok, best, opt = _vet_can(t)
            if hoi == "dinh":
                assert int(dap) == len(t["dinh"])
            else:
                i = 0 if hoi == "xcuc" else 1
                if t["kind"] == "max":
                    assert int(dap) == max(P[i] for P in ok if P[1 - i] == 0)
                else:
                    assert int(dap) == min(P[i] for P in ok if P[1 - i] == 0)


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_tl_hai_y(k):
    for _ in range(30):
        _cap.clear()
        getattr(M, "L10_C2_B4_VD028_TL_%s_01" % CHU[k]["tl"])(1)
        debai, ds = _cap["tl"][0]
        assert len(ds) == 2
        assert ds[0][0].startswith("Lập hệ bất phương trình")
        assert r"\heva" in ds[0][1]
        assert r"\left(" in ds[1][1]


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_tf_it_nhat_3_dung_3_sai(k):
    L = CHU[k]["tf"]
    for _ in range(60):
        _cap.clear()
        getattr(M, "L10_C2_TF_%s_01" % L)(1)
        debai, ys = _cap["tf"]
        assert len(ys) == 4
        for y in ys:
            dem_d = sum(1 for m in y if m[0].startswith(r"{\True"))
            dem_s = len(y) - dem_d
            assert dem_d >= 3 and dem_s >= 3, (dem_d, dem_s)


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_nb025_ba_dieu_kien(k):
    n = 3 if k != "3" else 2
    for i in range(1, n + 1):
        _cap.clear()
        getattr(M, "L10_C2_B3_NB025_MC_%s_%02d" % (CHU[k]["nb"], i))(1)
        debai, dap, nh, giai = _cap["mc"][0]
        assert dap not in nh and len(set(nh)) == len(nh)


@pytest.mark.parametrize("k", ["2", "3", "4"])
def test_tf_y_b_va_y_c_dung_sai_doc_lap(k):
    import re
    for _ in range(40):
        _cap.clear()
        KB, ghi = _chup_t(k)
        M._kb_tf(KB, 1, 1)
        t = ghi[0]
        ok, best, opt = _vet_can(t)
        ys = _cap["tf"][1]
        for txt, _ly in ys[1]:                                     # ý b: phương án thoả mãn / không thoả mãn
            X, Y = map(int, re.findall(r"\d+", txt.split("Phương án", 1)[1])[:2])
            dung = txt.startswith(r"{\True")
            thoa = (X, Y) in ok
            assert dung == (thoa if "không thoả" not in txt else not thoa), txt
        for txt, _ly in ys[2]:                                     # ý c: đỉnh của miền nghiệm
            dung = txt.startswith(r"{\True")
            m = re.search(r"Điểm \$\\left\((\d+); (\d+)\\right\)\$ là một đỉnh", txt)
            if m:
                P = (int(m.group(1)), int(m.group(2)))
                # đỉnh thật: thoả mọi ràng buộc và nằm trên ít nhất hai đường biên (kể cả trục)
                if P in ok:
                    bien = sum(1 for r in t["rb"] if r["a"] * P[0] + r["b"] * P[1] == r["c"]) + (P[0] == 0) + (P[1] == 0)
                else:
                    bien = 0
                assert dung == (bien >= 2), txt
            m = re.search(r"có đúng \$(\d+)\$ đỉnh", txt)
            if m:
                assert dung == (int(m.group(1)) == len(t["dinh"])), txt
