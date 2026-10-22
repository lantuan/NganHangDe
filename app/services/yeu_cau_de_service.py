"""
ĐỌC YÊU CẦU TẠO ĐỀ BẰNG PYTHON KHI n8n KHÔNG TRẢ LỜI ĐƯỢC (cô Lan 22/10/2026).

Cô gõ "Lớp 10, thi giữa kỳ 1" (trước đó "cho tôi đề lớp 10 chương 2") thì chat báo "AI chưa xử lý được yêu cầu
này": n8n trả về JSON rỗng / hỏng (máy chủ không gọi tới n8n được để xem Execution, chỉ biết thân phản hồi không đọc
được). Yêu cầu loại này rất rõ ràng - lớp + kỳ thi, hoặc lớp + chương - nên theo nguyên tắc "Ưu tiên Code hơn AI"
(docs/00) máy chủ tự đọc được, KHÔNG đoán gì thêm:

  - phải có LỚP (10/11/12) nói rõ - không có thì thôi (giữ báo lỗi cũ, như Quy tắc 3 của RequestParser);
  - "giữa kỳ / cuối kỳ / học kỳ 1|2"  -> HeSo2_HeSo3, ki_thi tương ứng;
  - "chương N" (không nói kỳ thi) hoặc "kiểm tra miệng / 15 phút / thường xuyên chương N" -> HeSo1,
    kiem_tra_thuong_xuyen, pham_vi_chuong = chuong_N;
  - KHÔNG đọc số câu / tỉ lệ mức độ: cấu trúc để trống -> máy chủ dùng cấu trúc mặc định (exam_rules.json), và
    câu xác nhận nói rõ điều đó. Muốn số câu khác thì học sinh nhắn lại (lại qua n8n như thường).

Chỉ dùng khi n8n hỏng; kết quả là khung "xac_nhan_de" (nút "Đồng ý, tạo đề") như RequestParser trả, nên người dùng
vẫn bấm đồng ý trước khi tạo đề.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_RULES = Path(__file__).resolve().parents[2] / "data" / "config" / "exam_rules.json"

_LOP = re.compile(r"(?:l[oớơ]p|kh[oố]i|to[aá]n|grade)\s*(10|11|12)\b", re.IGNORECASE)
_SO = r"(1|2|i{1,2}|một|mot|hai)\b"
_GIUA = re.compile(r"gi[uữ]a\s*(?:h[oọ]c\s*)?k[iìyỳ]\s*" + _SO, re.IGNORECASE)
_CUOI = re.compile(r"(?:cu[oố]i\s*(?:h[oọ]c\s*)?k[iìyỳ]|h[oọ]c\s*k[iìyỳ])\s*" + _SO, re.IGNORECASE)
_CHUONG = re.compile(r"ch[uư][oơ]ng\s*(\d{1,2})\b", re.IGNORECASE)
_SO_KY = {"1": "1", "i": "1", "một": "1", "mot": "1", "2": "2", "ii": "2", "hai": "2"}
_TEN_KY = {"giua_ky_1": ("giữa kỳ 1", "midterm 1"), "giua_ky_2": ("giữa kỳ 2", "midterm 2"),
           "cuoi_ky_1": ("cuối kỳ 1", "final exam 1"), "cuoi_ky_2": ("cuối kỳ 2", "final exam 2")}


def _mac_dinh(loai_he_so: str) -> dict:
    try:
        rules = json.loads(_RULES.read_text(encoding="utf-8"))[loai_he_so]
        return {k: (v.get("so_luong") if isinstance(v, dict) else v)
                for k, v in rules.items() if k in ("trac_nghiem", "dung_sai_cau_lon", "tra_loi_ngan", "tu_luan")}
    except Exception:
        return {}


def doc_yeu_cau_de(message: str, lang: str = "vi") -> dict | None:
    """Khung "xac_nhan_de" đọc từ tin nhắn, hoặc None khi tin nhắn không đủ rõ (thiếu lớp, thiếu kỳ thi/chương)."""
    if not message:
        return None
    t = message.strip()
    m_lop = _LOP.search(t)
    if not m_lop:
        return None
    lop = int(m_lop.group(1))
    m_g, m_c, m_ch = _GIUA.search(t), _CUOI.search(t), _CHUONG.search(t)
    if m_g or m_c:
        m = m_g or m_c
        ki_thi = ("giua_ky_" if m_g else "cuoi_ky_") + _SO_KY[m.group(1).lower()]
        loai, pham_vi = "HeSo2_HeSo3", None
    elif m_ch:
        ki_thi, loai, pham_vi = "kiem_tra_thuong_xuyen", "HeSo1", "chuong_%d" % int(m_ch.group(1))
    else:
        return None
    ct = _mac_dinh(loai)
    so = ("%d câu: %d trắc nghiệm, %d câu đúng/sai, %d trả lời ngắn, %d tự luận"
          % (sum(ct.values()), ct.get("trac_nghiem", 0), ct.get("dung_sai_cau_lon", 0), ct.get("tra_loi_ngan", 0),
             ct.get("tu_luan", 0))) if ct else ""
    so_en = ("%d questions: %d multiple choice, %d true/false, %d short answer, %d free response"
             % (sum(ct.values()), ct.get("trac_nghiem", 0), ct.get("dung_sai_cau_lon", 0), ct.get("tra_loi_ngan", 0),
                ct.get("tu_luan", 0))) if ct else ""
    if lang == "en":
        pham = (_TEN_KY[ki_thi][1] if pham_vi is None else "chapter %s test" % pham_vi.split("_")[1])
        tra_loi = ("You need a grade %d %s, using the default structure (%s). Click Agree to create it, or tell me "
                   "the number of questions you want." % (lop, pham, so_en))
    else:
        pham = ("đề " + _TEN_KY[ki_thi][0] if pham_vi is None else "đề kiểm tra chương %s" % pham_vi.split("_")[1])
        tra_loi = ("Bạn cần %s lớp %d, theo cấu trúc mặc định (%s). Đồng ý thì bấm nút bên dưới để tạo đề, "
                   "hoặc nhắn lại số câu bạn muốn nhé." % (pham, lop, so))
    return {"type": "xac_nhan_de", "can_xac_nhan": True, "tra_loi": tra_loi, "lop": lop, "loai_he_so": loai,
            "ki_thi": ki_thi, "pham_vi_chuong": pham_vi, "nguon_cau_truc": "python_du_phong",
            "cau_truc_tong_quat": None, "ty_le_muc_do_goc": None}
