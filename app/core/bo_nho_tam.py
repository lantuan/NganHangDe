"""
BỘ NHỚ TẠM NGẮN HẠN (cô Lan 24/10/2026: "tôi muốn tốc độ của web nhanh hơn ... sửa sao cho an toàn").

Trước đây MỖI yêu cầu đều gọi Supabase để xác thực phiên đăng nhập (`supabase.auth.get_user`), rồi gọi tiếp để đọc vai
trò, lớp của người dùng - mỗi lần là một lượt đi về qua mạng (thường 0,1 - 0,4 giây). Ở đây nhớ kết quả THÀNH CÔNG trong
vài phút, theo từng khoá (token đăng nhập / user_id). Lỗi, không tìm thấy thì KHÔNG nhớ (lần sau hỏi lại như cũ).

An toàn:
  - hết hạn sau `giay` giây; tối đa `toi_da` khoá (đầy thì bỏ các khoá cũ nhất);
  - khoá luồng (threading.Lock) vì FastAPI chạy hàm đồng bộ trong nhiều luồng;
  - khi chạy test (pytest đặt PYTEST_CURRENT_TEST) thì KHÔNG nhớ gì, để các test độc lập như trước.
"""
from __future__ import annotations

import os
import threading
import time


class BoNhoTam:
    def __init__(self, giay: float, toi_da: int = 5000):
        self.giay = giay
        self.toi_da = toi_da
        self._du_lieu: dict = {}
        self._khoa = threading.Lock()

    @staticmethod
    def _dang_test() -> bool:
        return bool(os.environ.get("PYTEST_CURRENT_TEST"))

    def lay(self, khoa):
        """(co, gia_tri): co = False khi chưa nhớ hoặc đã hết hạn."""
        if khoa is None or self._dang_test():
            return False, None
        with self._khoa:
            muc = self._du_lieu.get(khoa)
            if muc is None:
                return False, None
            het_han, gia_tri = muc
            if het_han < time.monotonic():
                self._du_lieu.pop(khoa, None)
                return False, None
            return True, gia_tri

    def dat(self, khoa, gia_tri) -> None:
        if khoa is None or self._dang_test():
            return
        with self._khoa:
            if len(self._du_lieu) >= self.toi_da:
                # bỏ một nửa số khoá sắp hết hạn nhất (rẻ, không cần cấu trúc phức tạp)
                for k, _ in sorted(self._du_lieu.items(), key=lambda kv: kv[1][0])[: self.toi_da // 2]:
                    self._du_lieu.pop(k, None)
            self._du_lieu[khoa] = (time.monotonic() + self.giay, gia_tri)

    def xoa(self, khoa) -> None:
        with self._khoa:
            self._du_lieu.pop(khoa, None)

    def xoa_het(self) -> None:
        with self._khoa:
            self._du_lieu.clear()
