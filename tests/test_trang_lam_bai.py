# -*- coding: utf-8 -*-
"""Trang "Làm bài trực tiếp" phải KHỚP với file PDF đề.

Vì sao có file này (28/09/2026): cô Lan tạo đề hệ số 1 chương 3, mở
trang làm bài rồi đối chiếu với PDF tải về thì thấy ba chỗ lệch:

1. PDF ghi "PHẦN III. Thí sinh trình bày tự luận" còn web ghi
   "PHẦN IV. Tự luận" cho cùng một câu. Nguyên nhân: _ghep_4_phan dồn
   số La Mã liên tục (phần rỗng không chiếm số), trong khi bảng
   TEN_PHAN của gia_su_service gán số CỐ ĐỊNH theo loại câu.
   Cô Lan chốt: số La Mã gắn chết vào loại câu, giống đề của Bộ.

2. Câu có hình vẽ thì PDF có hình, web không có gì cả - chỉ hiện ô
   vuông dấu hỏi (ảnh hỏng của Safari). Nguyên nhân: API trả về
   "/hinh/<mã>" nhưng router khai prefix="/api/exam" nên địa chỉ thật
   là "/api/exam/hinh/<mã>" -> 404. Câu có hình mà mất hình là ĐỔI
   LUÔN MỨC ĐỘ của câu.

3. Trang làm bài không in tiêu đề PHẦN nào cả, và đánh số câu 1 mạch
   trong khi PDF đánh lại từ 1 ở mỗi phần.
"""
import re
from pathlib import Path

import pytest

from app.services.exam_assembler_service import CAC_PHAN_DE, _ghep_4_phan
from app.services.gia_su_service import TEN_PHAN, THU_TU_PHAN

GOC = Path(__file__).resolve().parent.parent


def test_so_la_ma_cua_pdf_va_cua_web_phai_giong_nhau():
    """PHẦN I/II/III/IV phải chỉ cùng một loại câu ở cả hai nơi."""
    for ma_loai, so_la_ma, _loi_dan in CAC_PHAN_DE:
        ten_web = TEN_PHAN[ma_loai]
        assert ten_web.startswith("PHẦN %s." % so_la_ma), (
            "Loại câu %s: PDF ghi PHẦN %s nhưng web ghi %r"
            % (ma_loai, so_la_ma, ten_web)
        )


def test_bon_phan_du_va_dung_thu_tu():
    assert [ma for ma, _, _ in CAC_PHAN_DE] == THU_TU_PHAN


def test_phan_rong_khong_lam_tut_so_cua_phan_sau():
    """Đề thiếu Trả lời ngắn thì tự luận VẪN phải là PHẦN IV."""
    than = _ghep_4_phan({
        "MC": [r"\begin{ex}A\end{ex}"],
        "TF": [r"\begin{ex}B\end{ex}"],
        # KHÔNG có "SA" - đúng tình huống cô Lan gặp
        "TL": [r"\begin{ex}C\end{ex}"],
    })
    cac_so = re.findall(r"PHẦN (\w+)\.", than)
    assert cac_so == ["I", "II", "IV"], cac_so
    assert "PHẦN III" not in than


@pytest.mark.parametrize("ma_loai,so_la_ma", [(m, s) for m, s, _ in CAC_PHAN_DE])
def test_moi_phan_giu_dung_so_cua_minh_du_dung_mot_minh(ma_loai, so_la_ma):
    than = _ghep_4_phan({ma_loai: [r"\begin{ex}X\end{ex}"]})
    assert re.findall(r"PHẦN (\w+)\.", than) == [so_la_ma]


def test_duong_dan_anh_hinh_ve_phai_khop_voi_router():
    """URL hình trong API phải gọi được thật, không phải 404."""
    from app.routers import exam as router_exam

    nguon = Path(router_exam.__file__).read_text(encoding="utf-8")
    mau = re.search(r'"hinh": \[\s*"([^"]+)" %', nguon)
    assert mau, "Không tìm thấy chỗ dựng URL hình trong app/routers/exam.py"
    duong_dan = mau.group(1)

    duong_dan_that = None
    for route in router_exam.router.routes:
        if "/hinh/" in getattr(route, "path", ""):
            # FastAPI da gan san prefix vao route.path roi.
            duong_dan_that = route.path
            break
    assert duong_dan_that, "Không tìm thấy route phục vụ ảnh hình vẽ"

    # duong_dan dang "/api/exam/hinh/%s", route that dang "/api/exam/hinh/{ma}"
    assert duong_dan.replace("%s", "") == duong_dan_that.replace("{ma}", ""), (
        "API trả URL %r nhưng địa chỉ thật của ảnh là %r - trình duyệt sẽ "
        "nhận 404 và học sinh mất hình." % (duong_dan, duong_dan_that)
    )


def test_trang_lam_bai_co_in_tieu_de_phan_va_danh_so_theo_phan():
    html = (GOC / "app/templates/chat/lam_bai.html").read_text(encoding="utf-8")
    assert "tieu-de-phan" in html, "Trang làm bài chưa in tiêu đề PHẦN nào"
    assert "cau.ten_phan" in html
    assert "so_trong_phan" in html, "Trang làm bài chưa đánh số câu theo phần"
    # Nut nop bai / cham diem VAN phai dung so_thu_tu 1 mach lam khoa,
    # neu doi sang so hien thi thi hai cau khac phan se trung ten o input.
    assert "cau_' + cau.so_thu_tu" in html, (
        "Khóa nộp bài phải là so_thu_tu (số 1 mạch), không phải số hiển thị"
    )


def test_api_lam_bai_tra_ve_du_thong_tin_phan():
    nguon = (GOC / "app/routers/exam.py").read_text(encoding="utf-8")
    for truong in ('"ma_phan"', '"ten_phan"', '"so_trong_phan"'):
        assert truong in nguon, "API trang làm bài còn thiếu trường %s" % truong
