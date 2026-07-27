"""
CN_LoadCurriculum

Đọc dữ liệu Curriculum (data/curriculum/toan{lop}/L{lop}_C{chuong}.json)
và cung cấp cho CN_BuildBlueprint đúng phạm vi bài (pham_vi_bai) đã được
CN_LoadExamScope xác định.

Không được: chọn câu, đọc PPCT, đọc Mapping (theo doc 08_CODE_NODES.md).
"""

from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CURRICULUM_DIR = BASE_DIR / "data" / "curriculum"

_BAI_ID_PATTERN = re.compile(r"^L(\d+)_C(\d+)_B(\d+)$")


class CurriculumError(Exception):
    pass


def load_curriculum(lop: int, chuong_so: int) -> list[dict]:
    """
    Đọc toàn bộ năng lực (competency) của 1 chương, không lọc theo bài.
    """
    file = CURRICULUM_DIR / f"toan{lop}" / f"L{lop}_C{chuong_so}.json"
    if not file.exists():
        raise CurriculumError(f"Không tìm thấy Curriculum: {file}")
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_curriculum_for_scope(lop: int, pham_vi_bai: list[str]) -> list[dict]:
    """
    Đọc Curriculum đúng phạm vi bài (pham_vi_bai lấy từ CN_LoadExamScope,
    dạng id "L10_C1_B2").

    Tự suy ra các chương liên quan từ pham_vi_bai, đọc file Curriculum
    tương ứng từng chương, rồi lọc lại đúng các bài nằm trong phạm vi.
    """
    chuong_can_doc: dict[int, int] = {}  # chuong_so -> lop (để mở đúng file)
    for bai_id in pham_vi_bai:
        match = _BAI_ID_PATTERN.match(bai_id)
        if not match:
            continue
        lop_id, chuong_so, _bai_so = match.groups()
        chuong_can_doc[int(chuong_so)] = int(lop_id)

    if not chuong_can_doc:
        raise CurriculumError(
            f"Không suy ra được chương nào từ pham_vi_bai: {pham_vi_bai}"
        )

    ket_qua = []
    for chuong_so, lop_khoi in chuong_can_doc.items():
        entries = load_curriculum(lop_khoi, chuong_so)
        for e in entries:
            bai_id = f"L{lop_khoi}_C{chuong_so}_B{e['bai_so']}"
            if bai_id in pham_vi_bai:
                ket_qua.append(e)

    return ket_qua


def group_by_muc_do(entries: list[dict]) -> dict[str, list[dict]]:
    """
    Nhóm Curriculum entries theo MucDo (NB/TH/VD). Curriculum không có
    mức VDC (Ngoại lệ 2, doc 04_ID_STANDARD.md) nên không xuất hiện ở đây.
    """
    ket_qua: dict[str, list[dict]] = {"NB": [], "TH": [], "VD": []}
    for e in entries:
        muc_do = e.get("MucDo")
        if muc_do in ket_qua:
            ket_qua[muc_do].append(e)
    return ket_qua