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
# Loại câu nói trong tin nhắn ("phần tự luận", "chỉ trắc nghiệm", "5 câu tự luận"...)
_LOAI = [("trac_nghiem", r"tr[aắ]c\s*nghi[eệ]m"), ("dung_sai_cau_lon", r"[dđ][uú]ng\s*[/-]?\s*sai"),
         ("tra_loi_ngan", r"tr[aả]\s*l[oờ]i\s*ng[aắ]n"), ("tu_luan", r"t[uự]\s*lu[aậ]n")]
_CHI = r"(?:ch[iỉ]|ph[aầ]n|to[aà]n|ri[eê]ng)\s*(?:c[oó]\s*)?(?:c[aâ]u\s*)?"
_TEN_LOAI = {"trac_nghiem": ("trắc nghiệm", "multiple choice"), "dung_sai_cau_lon": ("câu đúng/sai", "true/false"),
             "tra_loi_ngan": ("trả lời ngắn", "short answer"), "tu_luan": ("tự luận", "free response")}
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


def _doc_loai_cau(t: str, mac_dinh: dict) -> dict | None:
    """Số câu từng loại học sinh nói rõ. "phần/chỉ <loại>" -> chỉ loại đó (loại khác 0, loại đó lấy số mặc định nếu
    không nói số); "<n> câu <loại>" -> đúng n câu, loại khác mặc định. Không nhắc loại nào -> None (cấu trúc mặc định)."""
    ct, chi = {}, False
    for khoa, mau in _LOAI:
        m_so = re.search(r"(\d{1,2})\s*(?:c[aâ]u\s*)?" + mau, t, re.IGNORECASE)
        if m_so:
            ct[khoa] = int(m_so.group(1))
        if re.search(_CHI + mau, t, re.IGNORECASE):
            chi = True
            ct.setdefault(khoa, mac_dinh.get(khoa) or 0)
    if not ct:
        return None
    if chi:
        return {k: ct.get(k, 0) for k, _m in _LOAI}
    return {k: ct.get(k, mac_dinh.get(k, 0)) for k, _m in _LOAI}


def _mo_ta(ct: dict, lang: str) -> str:
    i = 1 if lang == "en" else 0
    phan = ["%d %s" % (ct[k], _TEN_LOAI[k][i]) for k, _m in _LOAI if ct.get(k)]
    tong = sum(ct.get(k) or 0 for k, _m in _LOAI)
    return ("%d %s: %s" % (tong, "questions" if i else "câu", ", ".join(phan))) if phan else ""


def doc_yeu_cau_de(message: str, lang: str = "vi", lop_mac_dinh: int | None = None) -> dict | None:
    """Khung "xac_nhan_de" đọc từ tin nhắn, hoặc None khi tin nhắn không đủ rõ (thiếu kỳ thi/chương, hoặc thiếu lớp mà
    hồ sơ cũng không có). lop_mac_dinh = lớp trong hồ sơ (cô Lan 23/10/2026: "tôi cần đề luyện tập thêm chương 3, phần
    tự luận" không nói lớp, nhưng hồ sơ ghi Khối 10)."""
    if not message:
        return None
    t = message.strip()
    m_lop = _LOP.search(t)
    if m_lop:
        lop = int(m_lop.group(1))
    elif lop_mac_dinh in (10, 11, 12):
        lop = lop_mac_dinh
    else:
        return None
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
    rieng = _doc_loai_cau(t, ct)
    if rieng is not None:
        ct = rieng
    if lang == "en":
        pham = (_TEN_KY[ki_thi][1] if pham_vi is None else "chapter %s test" % pham_vi.split("_")[1])
        tra_loi = ("You need a grade %d %s, %s (%s). Click Agree to create it, or tell me the number of questions you "
                   "want." % (lop, pham, "as you asked" if rieng else "using the default structure", _mo_ta(ct, "en")))
    else:
        pham = ("đề " + _TEN_KY[ki_thi][0] if pham_vi is None else "đề kiểm tra chương %s" % pham_vi.split("_")[1])
        tra_loi = ("Bạn cần %s lớp %d, %s (%s). Đồng ý thì bấm nút bên dưới để tạo đề, hoặc nhắn lại số câu bạn muốn "
                   "nhé." % (pham, lop, "theo đúng yêu cầu của bạn" if rieng else "theo cấu trúc mặc định", _mo_ta(ct, "vi")))
    return {"type": "xac_nhan_de", "can_xac_nhan": True, "tra_loi": tra_loi, "lop": lop, "loai_he_so": loai,
            "ki_thi": ki_thi, "pham_vi_chuong": pham_vi, "nguon_cau_truc": "python_du_phong",
            "cau_truc_tong_quat": ct if rieng else None, "ty_le_muc_do_goc": None}


# Hỏi cách dùng ("tôi không biết cách tạo đề", "hướng dẫn tạo đề"...): n8n hỏng thì máy chủ trả lời bằng câu soạn sẵn
# đúng với các tính năng đang có (như Rule 5 của CHV_Fun) thay vì "AI chưa xử lý được" (cô Lan 23/10/2026).
_HOI_CACH_DUNG = re.compile(
    r"kh[oô]ng\s*bi[eế]t\s*(c[aá]ch|l[aà]m\s*sao|l[aà]m\s*th[eế]\s*n[aà]o)"
    r"|h[uư][oớ]ng\s*d[aẫ]n\s*(s[uử]\s*d[uụ]ng|t[aạ]o|c[aá]ch|d[uù]ng)"
    r"|c[aá]ch\s*(t[aạ]o|ra|l[aà]m|d[uù]ng|s[uử]\s*d[uụ]ng)\b"
    r"|l[aà]m\s*(sao|th[eế]\s*n[aà]o)\s*([dđ][eể]\s*)?(t[aạ]o|ra|c[oó])\s*[dđ][eề]"
    r"|\bhow\s*(do|to|can)\b|\bhelp\b", re.IGNORECASE)


def tra_loi_cach_dung(message: str, lang: str = "vi") -> str | None:
    """Câu hướng dẫn soạn sẵn khi tin nhắn hỏi cách dùng; không phải câu hỏi cách dùng -> None."""
    if not message or not _HOI_CACH_DUNG.search(message):
        return None
    if lang == "en":
        return ("Creating an exam is easy:\n"
                "1. Click **📝 Create a new exam** below, choose the grade, test type and chapter, then create it. "
                "Or just type what you need, e.g. \"grade 10, chapter 2 test\" or \"grade 10 midterm 1\".\n"
                "2. Choose **📘 Standard curriculum** or **🚀 Extra challenge**; tick **Include the English version** "
                "if you want both languages.\n"
                "3. Download the exam, or click **✅ Yes, take it now!** to do it on the web and get it graded right away.\n"
                "4. After submitting, click **💬 Ask the AI teacher about this question** (or **💬 Review a past exam**) "
                "to have any question explained.")
    return ("Tạo đề dễ lắm nè:\n"
            "1. Bấm **📝 Tạo đề mới** ở dưới, chọn lớp, loại kiểm tra, chương rồi bấm tạo. Hoặc gõ tự nhiên, ví dụ "
            "\"đề kiểm tra chương 2 lớp 10\", \"lớp 10 giữa kỳ 1\", \"chương 3 phần tự luận\".\n"
            "2. Chọn **📘 Đúng chương trình** hoặc **🚀 Nâng cao thêm**; muốn có cả bản tiếng Anh thì tick "
            "**Kèm bản tiếng Anh**.\n"
            "3. Tải đề về làm trên giấy, hoặc bấm **✅ Có, làm luôn!** để làm trên web và được chấm điểm ngay.\n"
            "4. Nộp bài xong, câu nào chưa hiểu thì bấm **💬 Hỏi thầy/cô AI về câu này** (hoặc **💬 Hỏi lại đề cũ**) "
            "để được giảng lại.")
