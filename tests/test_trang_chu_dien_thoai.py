# -*- coding: utf-8 -*-
"""Trang chu tren dien thoai (co Lan 21/10/2026: "bi loi tran man hinh doi voi dien thoai").

Nguyen nhan: header fixed cao co dinh h-20, khong cho xuong dong; man hinh hep (hoac dien thoai dat chu to) thi tieu de
xuong 3 dong, nut Dang ky / Dang nhap lot ra ngoai mep phai, trang rong hon man hinh nen nut Tieng Viet | English bi cat.
Da sua: header sticky + flex-wrap, le 16px tren dien thoai, nut khong ngat chu, trang khong cuon ngang.
Da chup thu bang Chromium o be rong 300, 320, 360, 412 px: scrollWidth bang be rong man hinh.
"""
import re
from pathlib import Path

HTML = (Path(__file__).resolve().parent.parent / "app" / "templates" / "index.html").read_text(encoding="utf-8")


def test_header_sticky_va_xuong_dong():
    hd = re.search(r"<header[^>]*>\s*<div[^>]*>", HTML).group(0)
    assert "sticky top-0" in hd and "fixed top-0" not in hd
    assert "flex-wrap" in hd and "md:h-20" in hd and " h-20" not in hd       # cao co dinh chi tu man hinh vua tro len
    assert re.search(r'<main class="flex-grow">', HTML)                 # khong con pt-20 bu cho header fixed


def test_le_dien_thoai_va_nut_khong_ngat_chu():
    assert "mx-auto px-margin-desktop" not in HTML                      # moi khoi deu co le 16px tren dien thoai
    nut = re.findall(r'class="([^"]*bg-primary text-on-primary rounded-lg[^"]*)"', HTML)
    assert nut and all("whitespace-nowrap" in c for c in nut)
    assert "whitespace-nowrap" in re.search(r"<h1[^>]*>", HTML).group(0)


def test_khong_cuon_ngang():
    assert re.search(r"html, body \{ overflow-x: hidden; overflow-x: clip; \}", HTML)
    assert "break-all" in re.search(r'<p[^>]*>nganhangdetoanchv@gmail.com</p>', HTML).group(0)
