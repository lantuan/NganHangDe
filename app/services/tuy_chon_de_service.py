"""Lựa chọn "Kèm bản tiếng Anh" và "Đúng chương trình / Nâng cao thêm" của người dùng cho các đề tạo qua luồng chat tự do (có n8n ở giữa).

Vì sao cần: người dùng gõ yêu cầu trong chat -> /chat gửi sang n8n -> n8n tự gọi /api/exam/generate-pdf-auto
bằng dữ liệu n8n dựng, nên ô tick của người dùng không có đường nào chen vào lời gọi đó. Cách làm: /chat ghi
lựa chọn theo conversation_id vào một tệp nhỏ, /generate-pdf-auto đọc lại theo conversation_id khi lời gọi
không nói rõ. n8n KHÔNG phải sửa gì và không phải làm thêm bước nào.

Dùng tệp (không dùng biến trong bộ nhớ) để chạy đúng khi máy chủ có nhiều tiến trình. Mục cũ quá 6 giờ bị bỏ.
Mặc định (không có ghi nhận) là KHÔNG kèm tiếng Anh: đề chỉ có bản Việt, đỡ tốn công sinh bản Anh.
"""
import json
import os
import time
from pathlib import Path

TEP = Path(__file__).resolve().parent.parent.parent / "data" / "temp" / "kem_tieng_anh_hoi_thoai.json"
HAN_GIAY = 6 * 3600


def _doc() -> dict:
    try:
        return json.loads(TEP.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _dat(conversation_id: str | None, **gia_tri) -> None:
    """Ghi (gộp) các lựa chọn của một hội thoại: lựa chọn này không xoá lựa chọn kia."""
    if not conversation_id:
        return
    now = time.time()
    du_lieu = {k: v for k, v in _doc().items() if now - v.get("t", 0) < HAN_GIAY}
    muc = dict(du_lieu.get(conversation_id) or {})
    muc.update(gia_tri)
    muc["t"] = now
    du_lieu[conversation_id] = muc
    try:
        TEP.parent.mkdir(parents=True, exist_ok=True)
        tam = TEP.with_suffix(".tmp%d" % os.getpid())
        tam.write_text(json.dumps(du_lieu), encoding="utf-8")
        os.replace(tam, TEP)               # ghi nguyên tử: tiến trình khác đọc không bao giờ thấy tệp dở
    except OSError:
        pass                               # ghi hỏng thì coi như không chọn; đề vẫn ra bình thường


def _lay(conversation_id: str | None, khoa: str):
    if not conversation_id:
        return None
    muc = _doc().get(conversation_id)
    if not muc or time.time() - muc.get("t", 0) >= HAN_GIAY:
        return None
    return muc.get(khoa)


def dat_kem_tieng_anh(conversation_id: str | None, bat: bool) -> None:
    _dat(conversation_id, anh=bool(bat))


def lay_kem_tieng_anh(conversation_id: str | None) -> bool:
    return bool(_lay(conversation_id, "anh"))


# Nút "Đúng chương trình" / "Nâng cao thêm" ở khung chat (cô Lan 21/10/2026): Đúng chương trình = chỉ các dạng theo
# yêu cầu cần đạt của Bộ (chi_yccd=True), Nâng cao thêm = có cả dạng luyện tập thêm. Cùng cách ghi theo hội thoại
# như "Kèm bản tiếng Anh" để đề tạo bằng tin nhắn (n8n gọi /generate-pdf-auto) cũng theo đúng nút người dùng chọn.
def dat_chi_yccd(conversation_id: str | None, bat: bool) -> None:
    _dat(conversation_id, chi_yccd=bool(bat))


def lay_chi_yccd(conversation_id: str | None) -> bool:
    """Không có ghi nhận (lời gọi cũ) -> False: như trước đây, có cả dạng luyện tập thêm."""
    return bool(_lay(conversation_id, "chi_yccd"))
