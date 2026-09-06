# -*- coding: utf-8 -*-
"""Kiem tra answer_parser_service tren TOAN BO ngan hang de that.

Chay moi ham generator trong data/python_bank/toan10/*.py mot lan, dua
latex_block ra trich_dap_an() roi doi chieu loai cau parser doc duoc voi
loai cau ghi trong TEN HAM (_MC_ / _TF_ / _SA_ / _TL_).

Bat duoc 2 nhom loi:
  1. Parser doc sai loai cau (vd cau Dung/Sai bi doc thanh Tu luan) ->
     cham diem sai phan, vi diem chia theo phan (xem diem_service.py).
  2. Ham generator bi loi hoac quen `return cauTN` -> de sinh ra cau
     rong. Da bat duoc that: L10_C1_B2_NB017_MC_B_02 (sua 2026-09-04).

Chay: python3 tests/test_answer_parser_bank.py
"""
import contextlib
import importlib.util
import inspect
import io
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "data" / "python_bank"))

from app.services.answer_parser_service import trich_dap_an  # noqa: E402

BANK_DIR = BASE_DIR / "data" / "python_bank"


def loai_cau_theo_ten_ham(ten: str) -> str | None:
    for khoa in ("_MC_", "_TF_", "_SA_", "_TL_"):
        if khoa in ten:
            return khoa.strip("_")
    return None


def goi_generator(ham):
    """Goi generator voi socau=1, giu nguyen gia tri mac dinh cua cac
    tham so khac (vd dang=2 o cac ham SA - truyen dang=1 se ra dang MC)."""
    tham_so = list(inspect.signature(ham).parameters.values())
    args = [1]  # socau
    for ts in tham_so[1:]:
        if ts.default is inspect.Parameter.empty:
            args.append(1)  # tham so bat buoc khong co mac dinh (vd socot)
        else:
            break
    with contextlib.redirect_stdout(io.StringIO()):
        return ham(*args)


class ThieuThuVien(Exception):
    """Chay bang python3 he thong thay vi python trong .venv."""


def kiem_tra_file(duong_dan: Path) -> list[str]:
    spec = importlib.util.spec_from_file_location(duong_dan.stem, duong_dan)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ModuleNotFoundError as e:
        # numpy/sympy chi co trong .venv cua du an, khong co o python3 he
        # thong -> bao ro cach chay thay vi de traceback kho hieu.
        raise ThieuThuVien(
            f"Thieu thu vien '{e.name}'. Nho kich hoat moi truong ao truoc:\n"
            f"    cd {BASE_DIR}\n"
            f"    source .venv/bin/activate\n"
            f"    python3 tests/test_answer_parser_bank.py"
        ) from e
    ten_ham = re.findall(r"^def ([A-Za-z0-9_]+)\(", duong_dan.read_text(encoding="utf-8"), re.M)

    loi = []
    thong_ke = {}
    for ten in ten_ham:
        mong_doi = loai_cau_theo_ten_ham(ten)
        if mong_doi is None:
            continue
        try:
            khoi = goi_generator(getattr(mod, ten))
            while isinstance(khoi, (list, tuple)):
                khoi = khoi[0]
            if not khoi:
                loi.append(f"{ten}: generator tra ve rong (quen `return cauTN`?)")
                continue
            ket_qua = trich_dap_an(str(khoi))
        except Exception as e:  # noqa: BLE001
            loi.append(f"{ten}: {type(e).__name__}: {str(e)[:80]}")
            continue

        thuc_te = ket_qua["loai_cau"]
        thong_ke[thuc_te] = thong_ke.get(thuc_te, 0) + 1
        if thuc_te != mong_doi:
            loi.append(f"{ten}: ten ham bao {mong_doi} nhung parser doc ra {thuc_te}")
        elif thuc_te == "TF" and sorted(ket_qua["dap_an_dung"]) != ["a", "b", "c", "d"]:
            loi.append(f"{ten}: cau TF thieu y - {ket_qua['dap_an_dung']}")
        elif thuc_te in ("MC", "SA") and not ket_qua["dap_an_dung"]:
            loi.append(f"{ten}: khong trich duoc dap an dung")

    print(f"  {duong_dan.name}: {len(ten_ham)} ham | parser phan loai {thong_ke}")
    return loi


def main() -> int:
    tat_ca_loi = []
    try:
        for duong_dan in sorted(BANK_DIR.glob("toan*/L*.py")):
            tat_ca_loi += kiem_tra_file(duong_dan)
    except ThieuThuVien as e:
        print(e)
        return 2

    if tat_ca_loi:
        print(f"\nCO {len(tat_ca_loi)} VAN DE:")
        for dong in tat_ca_loi:
            print("  -", dong)
        return 1
    print("\nTAT CA GENERATOR DEU DUOC PARSER DOC DUNG LOAI CAU")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
