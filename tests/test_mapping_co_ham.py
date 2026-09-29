# -*- coding: utf-8 -*-
"""Moi dong mapping (cua chuong da co tep Python) phai co it nhat mot ham
<id>_01, <id>_02 ... Bat loi khi doi ID ma quen doi ten ham (hoac nguoc
lai) - xem docs/26_CHAY_NHAP_VA_SUA_CAU.md buoc 4b.
"""
import json
import pathlib
import re

GOC = pathlib.Path(__file__).resolve().parents[1]


def test_moi_dong_mapping_co_ham_python():
    thieu = []
    for mp in sorted((GOC / "data" / "mapping").rglob("L*_C*.json")):
        py = GOC / "data" / "python_bank" / mp.parent.name / (mp.stem + ".py")
        if not py.exists():
            continue
        src = py.read_text(encoding="utf-8")
        co_ham = set(re.findall(r"^def (L\d+_C\d+_\w+?)_\d\d\(", src, re.M))
        for dong in json.loads(mp.read_text(encoding="utf-8")):
            if dong["id"] not in co_ham:
                thieu.append("%s: %s (chua co ham %s_01)" % (mp.name, dong["id"], dong["id"]))
    assert not thieu, "\n".join(thieu)
