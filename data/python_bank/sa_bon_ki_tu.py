# ==========================================
# TRẢ LỜI NGẮN: ĐÁP SỐ TỐI ĐA 4 KÍ TỰ (cô Lan chốt lại 28/10/2026: "vẫn áp dụng 4 kí tự, chỉnh sửa lại hết cho tôi")
#
# Phiếu trả lời trắc nghiệm phần III chỉ có 4 ô (mỗi ô một chữ số, dấu "-" hoặc dấu ","). Một số hàm SA cũ sinh
# đáp số 5 kí tự trở lên với một phần bộ số ngẫu nhiên (ví dụ -0,96; 21,79; 10300). Không sửa toán, không sửa câu
# dẫn: bộ lọc @sa_bon_ki_tu bọc hàm SA, gọi hàm gốc từng câu một và CHỈ GIỮ câu có đáp số vừa 4 ô (bộ số khác vẫn
# đúng nhưng không ghi được lên phiếu). Hàm nào không ra nổi câu vừa 4 ô thì báo lỗi rõ (bộ ráp đề báo thiếu câu,
# không vỡ đề) - gặp thì phải sửa lại số liệu của hàm đó.
#
# Tệp dùng chung cho mọi chương (không sửa math_type.py). Dùng:
#     from sa_bon_ki_tu import sa_bon_ki_tu
#     @sa_bon_ki_tu
#     def L10_C3_B5_NB029_SA_C_01(socau, dang=2): ...
# ==========================================
import functools
import re

from math_type import CauHongError

TOI_DA_KI_TU = 4
SO_LAN_THU_MOI_CAU = 80


class DapSoQuaDaiError(CauHongError):
    """Hàm trả lời ngắn không sinh được câu có đáp số vừa 4 ô."""


_SHORTANS = re.compile(r"\\shortans(?:\[\d+\])?\{\s*(.*?)\}\s*$", re.M)


def dap_so_tra_loi_ngan(latex: str) -> list:
    """Đáp số trong các khối \\shortans{...} (bỏ $, {,} -> ",", bỏ khoảng trắng)."""
    return [m.group(1).strip().strip("$").replace("{,}", ",").replace(" ", "") for m in _SHORTANS.finditer(latex)]


def vua_bon_o(latex: str) -> bool:
    return all(len(d) <= TOI_DA_KI_TU for d in dap_so_tra_loi_ngan(latex))


def sa_bon_ki_tu(ham):
    """Bọc hàm SA: trả đúng socau câu KHÁC NHAU, mỗi câu đáp số tối đa 4 kí tự."""
    @functools.wraps(ham)
    def boc(socau, *a, **k):
        cac_cau, da_co, thu = [], set(), 0
        while len(cac_cau) < socau and thu < SO_LAN_THU_MOI_CAU * max(1, socau):
            thu += 1
            cau = ham(1, *a, **k)
            if cau not in da_co and vua_bon_o(cau):
                da_co.add(cau)
                cac_cau.append(cau)
        if len(cac_cau) < socau:
            raise DapSoQuaDaiError("%s: chỉ sinh được %d/%d câu có đáp số vừa 4 ô sau %d lần thử - cần sửa số liệu "
                                   "của hàm." % (ham.__name__, len(cac_cau), socau, thu))
        return "".join(cac_cau)
    boc.sa_bon_ki_tu = True
    return boc
