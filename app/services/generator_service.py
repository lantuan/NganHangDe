import importlib.util
import inspect
import random
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PYTHON_BANK_DIR = BASE_DIR / "data" / "python_bank"

if str(PYTHON_BANK_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_BANK_DIR))


class GeneratorNotFoundError(Exception):
    pass


def _load_chapter_module(lop: int, chuong_so: int):
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
    pattern = re.compile(rf"^{re.escape(generator_id)}_\d{{2}}$")
    return [
        name for name in dir(module)
        if pattern.match(name) and callable(getattr(module, name))
    ]


def _chon_bien_the(variants: list[str], used_variants: dict | None, generator_id: str) -> str:
    """
    Cấp 2: ưu tiên biến thể CHƯA dùng cho generator_id này (trong cùng 1 lần build đề).
    Cấp 3: hết biến thể khác thì đành dùng lại biến thể đã dùng.
    Nếu used_variants=None (không theo dõi), chọn ngẫu nhiên như cũ.
    """
    if used_variants is None:
        return random.choice(variants)

    da_dung = used_variants.setdefault(generator_id, set())
    chua_dung = [v for v in variants if v not in da_dung]

    chosen = random.choice(chua_dung) if chua_dung else random.choice(variants)
    da_dung.add(chosen)
    return chosen


def _call_generator_function(func, socau: int, socot: int | None, dong: int | None):
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())

    if len(params) == 1:
        return func(socau)

    second_param = params[1]
    if second_param == "socot":
        return func(socau, socot if socot is not None else 4)
    elif second_param == "dong":
        return func(socau, dong if dong is not None else 1)
    elif second_param == "dang":
        # Moi ham MC/SA trong data/python_bank da tu khai bao dung mac
        # dinh ngay trong dinh nghia ham (MC -> dang=1, SA -> dang=2/3,
        # xem math_type.py). Chi can goi func(socau) de Python tu ap
        # dung mac dinh DUNG cua ham do - khong con hardcode dang=1 (MC)
        # cho tat ca nhu bug cu (goi nham ca cau SA thanh MC).
        return func(socau)
    else:
        return func(socau, 1)


def resolve_socau(role: str, socau_yeu_cau: int | None) -> int:
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
    used_variants: dict | None = None,
) -> dict:
    """
    used_variants: dict dùng chung xuyên suốt 1 LẦN SINH ĐỀ (1 lần gọi
    generate_exam_pdf), để tránh chọn trùng biến thể khi cùng 1 generator_id
    bị chọn nhiều lần (do Mapping thiếu ID khác). Truyền None nếu không cần
    theo dõi (gọi lẻ 1 câu độc lập).
    """
    module = _load_chapter_module(lop, chuong_so)
    variants = _find_variant_functions(module, generator_id)

    if not variants:
        raise GeneratorNotFoundError(
            f"Generator ID '{generator_id}' không có biến thể nào trong "
            f"toan{lop}/L{lop}_C{chuong_so}.py"
        )

    chosen_name = _chon_bien_the(variants, used_variants, generator_id)
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

def resolve_variant(generator_id: str, lop: int, chuong_so: int) -> str:
    """
    Chọn 1 biến thể Python duy nhất cho generator_id này.
    Gọi 1 LẦN DUY NHẤT cho mỗi generator_id trong 1 lần build đề,
    dùng chung cho mọi mã đề (không đổi biến thể giữa các mã đề).
    """
    module = _load_chapter_module(lop, chuong_so)
    variants = _find_variant_functions(module, generator_id)

    if not variants:
        raise GeneratorNotFoundError(
            f"Generator ID '{generator_id}' không có biến thể nào trong "
            f"toan{lop}/L{lop}_C{chuong_so}.py"
        )

    return random.choice(variants)


def call_locked_variant(
    generator_id: str,
    variant_name: str,
    lop: int,
    chuong_so: int,
    socot: int | None = None,
    dong: int | None = None,
) -> str:
    """
    Gọi ĐÚNG biến thể đã khóa (variant_name) với socau=1,
    dùng cho từng mã đề riêng lẻ. Mỗi lần gọi, hàm tự random số liệu
    bên trong nên nội dung khác nhau giữa các mã đề.
    """
    module = _load_chapter_module(lop, chuong_so)
    func = getattr(module, variant_name)
    return _call_generator_function(func, 1, socot, dong)