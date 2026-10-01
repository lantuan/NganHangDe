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
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        # Tep chuong co that nhung KHONG nap duoc - hay gap nhat la may chu
        # thieu mot thu vien ma tep do can (vi du num2words cho chuong 9).
        # Truoc day loi nay bay thang ra ngoai va lam VO CA DE. Nay coi nhu
        # "chua co ham", de he thong bao thieu dung cho, con cac chuong khac
        # van ra de binh thuong.
        sys.modules.pop(module_name, None)
        raise GeneratorNotFoundError(
            f"Không nạp được file Python của khối {lop} chương {chuong_so} "
            f"({file_path.name}): {type(e).__name__}: {e}. "
            f"Nếu là thiếu thư viện thì cài theo requirements.txt."
        ) from e
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
    # SỬA 30/09/2026: hết biến thể chưa dùng thì lấy biến thể DÙNG ÍT NHẤT
    # (đếm trong used_variants["__dem__"]), không random thuần.
    dem = used_variants.setdefault("__dem__", {})
    if chua_dung:
        chosen = random.choice(chua_dung)
    else:
        it_nhat = min(dem.get(v, 0) for v in variants)
        chosen = random.choice([v for v in variants if dem.get(v, 0) == it_nhat])
    da_dung.add(chosen)
    dem[chosen] = dem.get(chosen, 0) + 1
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


# Dùng LẠI đúng lớp lỗi mà math_type đã định nghĩa, để hai lớp khoá (lúc viết
# hàm và lúc ra đề) cùng ném MỘT loại lỗi - nếu tách thành hai lớp khác nhau thì
# bộ ráp đề chỉ bắt được một nửa, nửa còn lại vẫn làm vỡ cả đề.
from math_type import CauHongError, LoaiCauSaiError  # noqa: E402
from app.services.lam_dep_bieu_thuc import lam_dep  # noqa: E402
from app.services.tu_luan_hai_y import giu_hai_y  # noqa: E402


def kiem_tra_dung_loai_cau(generator_id: str, latex_block: str) -> None:
    """
    Khoá loại câu theo TÊN HÀM. Quy ước của ngân hàng (chốt 27/09/2026):

        _SA_  trả lời ngắn : MỘT câu hỏi -> MỘT đáp án, KHÔNG chia ý a), b)
        _TL_  tự luận      : phải có TỪ HAI Ý trở lên
        _MC_  trắc nghiệm  : phải có \\choice, không được có \\shortans
        _TF_  đúng/sai     : phải có \\choiceTFt

    Vì sao khoá ở đây chứ không chỉ ở math_type: math_type chặn lúc viết hàm,
    còn chỗ này chặn lúc RA ĐỀ - ai viết hàm kiểu gì, bỏ qua math_type hay
    tự ghép chuỗi LaTeX, vẫn không lọt được câu sai loại vào đề của học sinh.
    """
    khoi = re.findall(r"\\begin\{ex\}.*?\\end\{ex\}", latex_block, re.S) or [latex_block]

    for i, cau in enumerate(khoi, 1):
        so_shortans = cau.count("\\shortans")
        so_y = cau.count("\\begin{listEX}")

        if "_SA_" in generator_id:
            if so_shortans != 1:
                raise LoaiCauSaiError(
                    "%s (câu %d): câu trả lời ngắn phải có đúng MỘT đáp án "
                    "(\\shortans), đang có %d." % (generator_id, i, so_shortans))
            if so_y:
                raise LoaiCauSaiError(
                    "%s (câu %d): câu trả lời ngắn KHÔNG được chia ý a), b). "
                    "Muốn nhiều ý thì đổi sang câu tự luận (_TL_)."
                    % (generator_id, i))
        elif "_TL_" in generator_id:
            if cau.count("\\item ") < 2:
                raise LoaiCauSaiError(
                    "%s (câu %d): câu tự luận phải có từ HAI ý trở lên. "
                    "Nếu chỉ hỏi một ý thì đó là câu trả lời ngắn (_SA_)."
                    % (generator_id, i))
        elif "_TF_" in generator_id:
            if "\\choiceTFt" not in cau:
                raise LoaiCauSaiError(
                    "%s (câu %d): câu đúng/sai phải dùng \\choiceTFt."
                    % (generator_id, i))
        elif "_MC_" in generator_id:
            if "\\choice" not in cau:
                raise LoaiCauSaiError(
                    "%s (câu %d): câu trắc nghiệm phải có \\choice."
                    % (generator_id, i))
            if so_shortans:
                raise LoaiCauSaiError(
                    "%s (câu %d): câu trắc nghiệm không được có \\shortans."
                    % (generator_id, i))


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
    # Bối cảnh đề đã dùng trong MÃ ĐỀ đang sinh (vd kho bối cảnh bài toán thực
    # tế hai tập hợp của L10_C1): các câu cùng dùng một kho bối cảnh thì không
    # trùng bối cảnh. Tệp chương khai báo _DE_HIEN_TAI = threading.local().
    ngu_canh = getattr(module, "_DE_HIEN_TAI", None)
    if ngu_canh is not None:
        ngu_canh.da_dung = used_variants.setdefault("__boi_canh__", set()) if used_variants is not None else None
    try:
        latex_block = _call_generator_function(func, socau, socot, dong)
    finally:
        if ngu_canh is not None:
            ngu_canh.da_dung = None
    # Bo loc chung: 1x -> x, + -5 -> - 5... (xem lam_dep_bieu_thuc.py)
    latex_block = lam_dep(latex_block)
    # Tự luận chỉ đưa ra HAI ý (cô Lan 01/10/2026) - xem tu_luan_hai_y.py
    latex_block = giu_hai_y(latex_block, generator_id)
    kiem_tra_dung_loai_cau(generator_id, latex_block)

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
    latex_block = _call_generator_function(func, 1, socot, dong)
    # Bo loc chung: 1x -> x, + -5 -> - 5... (xem lam_dep_bieu_thuc.py)
    latex_block = lam_dep(latex_block)
    latex_block = giu_hai_y(latex_block, generator_id)
    kiem_tra_dung_loai_cau(generator_id, latex_block)
    return latex_block