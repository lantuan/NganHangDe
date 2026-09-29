# -*- coding: utf-8 -*-
"""Trang chat phai dung duoc tren DIEN THOAI.

Co Lan 29/09/2026 chup man hinh iPhone: thanh ben rong co dinh 280px
chiem gan het man hinh, khung chat chi con mot dai hep ~110px, chu bi bop
thanh tung chu mot, o nhap lieu bi day ra ngoai. Nguyen nhan: chat.html
KHONG co mot quy tac @media nao, va ham toggleSidebar() co san nhung
KHONG co nut nao goi toi.

Bai kiem tra nay giu ba thu khong cho ai go mat:
  1. Khoi @media cho man hinh hep.
  2. Nut ba gach goi toggleSidebar() (neu khong thi tren dien thoai khong
     co cach nao mo menu - khong dang xuat, khong vao khu giao vien duoc).
  3. Dung 100dvh - 100vh tren iPhone tinh ca thanh dia chi nen day mat
     o nhap lieu o day man hinh.
"""
from pathlib import Path

CHAT = (Path(__file__).resolve().parents[1] / "app" / "templates" / "chat"
        / "chat.html").read_text(encoding="utf-8")


def test_co_quy_tac_cho_man_hinh_hep():
    assert "@media (max-width: 767px)" in CHAT


def test_co_nut_mo_menu_tren_dien_thoai():
    assert 'class="nut-menu" onclick="toggleSidebar()"' in CHAT
    assert "function toggleSidebar()" in CHAT


def test_thanh_ben_an_san_khi_mo_tren_dien_thoai():
    assert 'window.innerWidth < 768' in CHAT
    assert 'classList.add("hidden-mobile")' in CHAT


def test_dung_chieu_cao_that_cua_man_hinh():
    assert "100dvh" in CHAT
