"""Tài khoản thiếu dòng profiles (cô Lan 28/10/2026: "cứ vào bằng tài khoản nganhangdetoanchv là bị thế này, chọn lớp
không được, không làm gì được hết"). Tài khoản đăng kí trước khi có trigger handle_new_user không có dòng profiles:
.single() báo PGRST116 -> trước đây rơi vào 'chua_cau_hinh' -> trang Chọn lớp lặp mãi. Nay tạo dòng rồi hỏi vai trò."""
from types import SimpleNamespace

from app.services import profile_service as P


class _Loi(Exception):
    def __init__(self, code):
        super().__init__("loi")
        self.code = code


class _Bang:
    def __init__(self, kho, loi_doc):
        self.kho, self.loi_doc = kho, loi_doc

    def select(self, *a):
        return self

    def eq(self, *a):
        return self

    def single(self):
        return self

    def upsert(self, du_lieu, **k):
        self.kho["ghi"] = (du_lieu, k)
        return self

    def execute(self):
        if "ghi" in self.kho:
            return SimpleNamespace(data=[self.kho["ghi"][0]])
        raise self.loi_doc


def _gia(monkeypatch, loi_doc):
    kho = {}
    u = SimpleNamespace(email="nganhangdetoanchv@gmail.com", user_metadata={"full_name": "Ngân hàng đề"})
    sb = SimpleNamespace(table=lambda t: _Bang(kho, loi_doc),
                         auth=SimpleNamespace(admin=SimpleNamespace(get_user_by_id=lambda i: SimpleNamespace(user=u))))
    monkeypatch.setattr(P, "supabase", sb)
    return kho


def test_thieu_dong_thi_tao_va_hoi_vai_tro(monkeypatch):
    kho = _gia(monkeypatch, _Loi("PGRST116"))
    assert P.lay_vai_tro("u-1") == P.VAI_TRO_CHUA_CHON
    du_lieu, k = kho["ghi"]
    assert du_lieu == {"id": "u-1", "email": "nganhangdetoanchv@gmail.com", "ho_ten": "Ngân hàng đề"}
    assert k == {"on_conflict": "id", "ignore_duplicates": True}          # không ghi đè dòng đã có


def test_loi_khac_van_bao_chua_cau_hinh(monkeypatch):
    kho = _gia(monkeypatch, _Loi("42703"))                                # cột vai_tro chưa có
    assert P.lay_vai_tro("u-2") == P.VAI_TRO_CHUA_CAU_HINH and "ghi" not in kho
