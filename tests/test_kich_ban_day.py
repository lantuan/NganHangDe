# -*- coding: utf-8 -*-
"""scripts/*.sh phải chạy được bằng bash 3.2 - bản đi kèm macOS.

Vì sao có file này (29/09/2026): cô Lan chạy "day web" thì đứt ngay ở
bước cập nhật VPS:

    day.sh: line 123: syntax error near unexpected token `('
    day.sh: line 123: `  */uvicorn) PY="\\$(dirname "\\$PY")/python" ;;'

Nguyên nhân: cả khối lệnh gửi sang VPS nằm trong $( ... ) và bên trong
lại có heredoc. Bash 3.2 (bản macOS dùng - /bin/bash, từ 2007) ĐỌC CẢ
THÂN heredoc để tìm dấu ) đóng lại. Thân heredoc có nhãn của case là
"*/uvicorn)" - một dấu ) lẻ - nên bash 3.2 tưởng lệnh thay thế đã hết
ngay tại đó rồi đọc phần còn lại như mã lệnh, sinh ra lỗi trên.

Bash 5 (Linux, máy chủ, CI) đọc đúng nên KHÔNG hề báo gì - lỗi chỉ lộ
ra trên máy Mac của cô Lan, đúng lúc cần đẩy code lên. Vì vậy phải khoá
bằng bài test tĩnh, không trông vào việc chạy thử.
"""
import re
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parent.parent
CAC_KICH_BAN = sorted((GOC / "scripts").glob("*.sh"))


def test_co_kich_ban_de_kiem():
    assert CAC_KICH_BAN, "Không tìm thấy scripts/*.sh nào"


@pytest.mark.parametrize("tep", CAC_KICH_BAN, ids=lambda p: p.name)
def test_khong_dat_heredoc_ben_trong_lenh_thay_the(tep):
    """$( ... <<EOF ... ) - bash 3.2 đọc sai, cấm hẳn."""
    for so_dong, dong in enumerate(
            tep.read_text(encoding="utf-8").splitlines(), start=1):
        khong_chu_thich = dong.split("#", 1)[0]
        if "$(" in khong_chu_thich and "<<" in khong_chu_thich:
            pytest.fail(
                "%s dòng %d đặt heredoc bên trong $( ): bash 3.2 trên macOS "
                "đọc sai chỗ này. Hãy ghi lệnh ra tệp tạm rồi mới gọi.\n"
                "    %s" % (tep.name, so_dong, dong.strip())
            )


@pytest.mark.parametrize("tep", CAC_KICH_BAN, ids=lambda p: p.name)
def test_khong_dung_cu_phap_chi_co_tu_bash_4(tep):
    """macOS chỉ có bash 3.2, không có declare -A, ${x^^}, mapfile..."""
    CAM = {
        r"declare\s+-A": "mảng liên kết (bash 4+)",
        r"local\s+-A": "mảng liên kết (bash 4+)",
        r"\$\{[A-Za-z_][A-Za-z_0-9]*\^\^": "${x^^} đổi hoa (bash 4+)",
        r"\$\{[A-Za-z_][A-Za-z_0-9]*,,": "${x,,} đổi thường (bash 4+)",
        r"\bmapfile\b": "mapfile (bash 4+)",
        r"\breadarray\b": "readarray (bash 4+)",
        r"\|&": "|& (bash 4+)",
        r"&>>": "&>> (bash 4+)",
    }
    noi_dung = tep.read_text(encoding="utf-8")
    for mau, ten in CAM.items():
        tim = re.search(mau, noi_dung)
        if tim:
            pytest.fail(
                "%s dùng %s - máy Mac của cô Lan chỉ có bash 3.2: %r"
                % (tep.name, ten, tim.group(0))
            )
