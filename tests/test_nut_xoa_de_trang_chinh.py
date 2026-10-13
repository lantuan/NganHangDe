"""
Trang chinh giao vien (/gv) phai co nut Xoa tung de o muc "De tao gan day",
giong trang "De da tao" (/gv/de-da-tao). Truoc 13/10/2026 chi trang "Xem tat ca"
moi co nut Xoa.

Gia lap dang nhap giao vien va danh sach de, KHONG can mang / Supabase.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import teacher


class _User:
    id = "gv-1"
    email = "gv@example.com"


DE = [
    {"id": "de-aaa", "lop": 10, "ki_thi": None, "pham_vi_chuong": "chuong_2",
     "blueprint": {"tieu_de": "ĐỀ KIỂM TRA MÔN TOÁN"}},
    {"id": "de-bbb", "lop": 10, "ki_thi": "thuong_xuyen", "pham_vi_chuong": None,
     "blueprint": {"tieu_de": "Đề kiểm tra - Toán 10"}},
]


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(teacher, "get_current_user", lambda request: _User())
    monkeypatch.setattr(teacher, "yeu_cau_giao_vien", lambda request, user: None)
    monkeypatch.setattr(teacher.profile_service, "lay_ho_so", lambda uid: {"ho_ten": "Lan"})
    monkeypatch.setattr(teacher.history_service, "lay_de_cua_giao_vien",
                        lambda uid, limit=None: DE)
    monkeypatch.setattr(teacher.classroom_service, "lay_refresh_token", lambda uid: "x")
    return TestClient(app)


def test_trang_chinh_co_nut_xoa_tung_de(client):
    html = client.get("/gv").text
    assert html.count('class="nut-xoa-de') == len(DE)
    assert 'data-de-id="de-aaa"' in html and 'data-de-id="de-bbb"' in html
    assert 'data-ten="ĐỀ KIỂM TRA MÔN TOÁN"' in html
    # hop xac nhan + script co mat, goi dung duong dan xoa
    assert 'id="hop-xoa"' in html
    assert "/gv/de-da-tao/xoa" in html
    # Khong dua "Xoa tat ca" ra trang chinh (bang chi hien 5 de gan nhat)
    assert 'id="nut-xoa-tat-ca"' not in html


def test_trang_de_da_tao_van_day_du(client, monkeypatch):
    html = client.get("/gv/de-da-tao").text
    assert html.count('class="nut-xoa-de') == len(DE)
    assert 'id="nut-xoa-tat-ca"' in html
    assert 'id="hop-xoa"' in html and "/gv/de-da-tao/xoa" in html


def test_trang_chinh_chua_co_de_khong_co_hop_xoa(monkeypatch, client):
    monkeypatch.setattr(teacher.history_service, "lay_de_cua_giao_vien",
                        lambda uid, limit=None: [])
    html = client.get("/gv").text
    assert "Chưa tạo đề nào" in html
    assert 'id="hop-xoa"' not in html
