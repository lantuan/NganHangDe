"""
Các hàm đếm dùng chung cho ngân hàng đề.

Dựng lại từ mô-đun DefChung mà các tệp gốc của cô Lan vẫn `import`. Chỉ
giữ những hàm ngân hàng thật sự cần; tên hàm giữ nguyên để mã cũ của cô
chuyển sang không phải sửa.
"""

import math


def calculate_coefficient(n, k):
    """Tổ hợp chập k của n phần tử: $C_n^k$ (chọn k, không kể thứ tự)."""
    n, k = int(n), int(k)
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def calculate_permutations(n, k):
    """Chỉnh hợp chập k của n phần tử: $A_n^k$ (chọn k, CÓ kể thứ tự)."""
    n, k = int(n), int(k)
    if k < 0 or k > n:
        return 0
    return math.perm(n, k)


def UCLN(a, b):
    """Ước chung lớn nhất."""
    return math.gcd(int(a), int(b))
