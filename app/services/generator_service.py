import importlib.util
import inspect
import random
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PYTHON_BANK_DIR = BASE_DIR / "data" / "python_bank"

# Đảm bảo "from math_type import *" trong các file L{lop}_C{chuong}.py
# hoạt động được, vì math_type.py đặt tại gốc python_bank/ (dùng chung mọi khối).
if str(PYTHON_BANK_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_BANK_DIR))


class GeneratorNotFoundError(Exception):
    pass


def _load_chapter_module(lop: int, chuong_so: int):
    """
    Import module tương ứng 1 chương.
    Ví dụ: data/python_bank/toan10/L10_C1.py -> module "toan10.L10_C1"
    """
    module_name = f"toan{lop}.L{lop}_C{chuong_so}"
    file_path = PYTHON_BANK_DIR / f"toan{lop}" / f"L{lop}_C{chuong_so}.py"

    if not file_path.exists():
        raise GeneratorNotFoundError(
            f"Không tìm thấy file Python cho khối {lop} chương {chuong_so}: {file_path}"
        )

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _find_variant_functions(module, generator_id: str) -> list[str]:
    """
    Tìm tất cả hàm khớp {generator_id}_01, {generator_id}_02, ...
    theo quy tắc Content Variant (docs/04_ID_STANDARD.md).
    """
    pattern = re.compile(rf"^{re.escape(generator_id)}_\d{{2}}$")
    return [
        name for name in dir(module)
        if pattern.match(name) and callable(getattr(module, name))
    ]


def _call_generator_function(func, socau: int, socot: int | None, dong: int | None):
    """
    Tự khớp tham số thứ 2 (socot hoặc dong) theo chữ ký thực tế của hàm,
    vì các hàm trong ngân hàng có thể đặt tên tham số khác nhau.
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())

    if len(params) == 1:
        return func(socau)

    second_param = params[1]
    if second_param == "socot":
        return func(socau, socot if socot is not None else 4)
    elif second_param == "dong":
        return func(socau, dong if dong is not None else 1)
    else:
        return func(socau, 1)


def resolve_socau(role: str, socau_yeu_cau: int | None) -> int:
    """
    Quy tắc phân quyền số câu (docs/10_PYTHON_GENERATOR.md):
    - Học sinh: luôn = 1, không cho đổi (server tự ép, không tin request).
    - Giáo viên: theo yêu cầu, mặc định 1 nếu không truyền.
    """
    if role == "student":
        return 1
    return socau_yeu_cau if socau_yeu_cau else 1


def call_generator(
    generator_id: str,
    lop: int,
    chuong_so: int,
    role: str,
    socau_yeu_cau: int | None = None,
    socot: int | None = None,
    dong: int | None = None,
) -> dict:
    """
    Input: Generator ID gốc (không hậu tố _NN), lop, chuong_so, role tài khoản.
    Output: dict gồm latex_block + metadata (docs/03_DATA_STRUCTURE.md).
    """
    module = _load_chapter_module(lop, chuong_so)
    variants = _find_variant_functions(module, generator_id)

    if not variants:
        raise GeneratorNotFoundError(
            f"Generator ID '{generator_id}' không có biến thể nào trong "
            f"toan{lop}/L{lop}_C{chuong_so}.py"
        )

    chosen_name = random.choice(variants)
    func = getattr(module, chosen_name)

    socau = resolve_socau(role, socau_yeu_cau)
    latex_block = _call_generator_function(func, socau, socot, dong)

    return {
        "generator_id": generator_id,
        "variant_used": chosen_name,
        "latex_block": latex_block,
        "so_ma_de": socau,
        "metadata": {
            "lop": lop,
            "chuong_so": chuong_so,
        },
    }