"""
PHẠM VI CỦA KHUNG CHAT (cô Lan 23/10/2026).

Chat hỏi "7 nhân 7 bằng mấy", AI tự tính rồi rủ "tạo vài đề ôn bảng cửu chương"; học sinh đồng ý ("vâng, tạo cho
tôi", "bảng cửu chương mà", "mấy cũng được") thì AI cứ hỏi lại số câu, chủ đề... mãi mà không làm được, vì ngân hàng
đề KHÔNG có bảng cửu chương. Cô Lan chốt:
  - kiến thức: AI chỉ dạy trong tài liệu lí thuyết thầy/cô (người tạo) đưa cho;
  - đề: chỉ theo ngân hàng đề của thầy/cô - đơn vị kiến thức Toán THPT lớp 10-12 (data/ppct/, chương nào đã có
    tệp ngân hàng data/python_bank/toan<lop>/L<lop>_C<n>.py).

Máy chủ tự trả lời bằng câu soạn sẵn (không gọi mô hình, không tính lượt hỏi AI) TRƯỚC khi tới n8n:
  1. ngoai_pham_vi: xin đề / học nội dung ngoài ngân hàng (bảng cửu chương, Toán tiểu học / THCS, lớp 1-9, môn
     khác) hoặc nhờ tính một phép tính ("7x7=?") -> nói rõ không làm được, kèm danh sách chương đang có;
  2. muon_de_chung_chung: muốn tạo đề nhưng không nói chương / kỳ thi / chủ đề nào ("vâng, tạo cho tôi", "mấy cũng
     được, miễn tôi rèn luyện được", "tạo đề lớp 10") -> danh sách chương của lớp + cách gõ, thay vì để AI hỏi vòng.
Yêu cầu có chương, kỳ thi hoặc tên chủ đề ("đề hàm số bậc hai") vẫn đi n8n như cũ.

Cô Lan 30/10/2026 (ảnh): tài khoản hồ sơ "Khối 10" xin đề -> được danh sách chương lớp 10; gõ tiếp "lớp 11 mà" thì
câu này lọt xuống n8n -> trò chuyện dự phòng chỉ được đưa danh sách chương LỚP 10 -> mô hình trả lời "em chỉ hỗ trợ
đề Toán Lớp 10 thôi", trong khi ngân hàng có lớp 11 (C1-C9), lớp 12 (C2, C6). Sửa:
  - tin nhắn CHỈ nêu lớp ("lớp 11", "lớp 11 mà", "còn khối 12 thì sao", "grade 11") -> coi như muon_de_chung_chung,
    trả danh sách chương của đúng lớp đó (chi_noi_lop);
  - chuong_cho_lenh luôn đưa đủ lớp 10, 11, 12 (lớp trong hồ sơ đứng đầu, chỉ là mặc định, không phải giới hạn).
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

_GOC = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------- danh sách chương có trong ngân hàng
@lru_cache(maxsize=None)
def _ppct(lop: int) -> tuple:
    try:
        return tuple(json.loads((_GOC / "data" / "ppct" / f"toan{lop}.json").read_text(encoding="utf-8")))
    except Exception:
        return ()


def danh_sach_chuong(lop: int) -> list[tuple[int, str]]:
    """[(số chương, tên chương)] của lớp, chỉ chương đã có tệp ngân hàng câu hỏi."""
    ten: dict[int, str] = {}
    for b in _ppct(lop):
        ten.setdefault(int(b["chuong_so"]), b.get("chuong") or "")
    return [(c, t) for c, t in sorted(ten.items())
            if (_GOC / "data" / "python_bank" / f"toan{lop}" / f"L{lop}_C{c}.py").exists()]


def _bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower()).replace("đ", "d")
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


@lru_cache(maxsize=1)
def _cap_tu_chu_de() -> frozenset:
    """Các cặp âm tiết liền nhau (bỏ dấu) trong tên chương + tên bài lớp 10-12: "ham so", "bat phuong", "xac suat"...
    Tin nhắn có một cặp như vậy là đã nói chủ đề -> để n8n đọc như cũ."""
    cap = set()
    for lop in (10, 11, 12):
        for b in _ppct(lop):
            for ten in (b.get("chuong") or "", b.get("bai") or ""):
                tu = re.findall(r"[a-z0-9]+", _bo_dau(ten))
                cap.update(" ".join(tu[i:i + 2]) for i in range(len(tu) - 1))
    return frozenset(cap)


@lru_cache(maxsize=1)
def _tu_chu_de_en() -> frozenset:
    """Từ (>= 5 chữ cái) trong tên chương + tên bài bản tiếng Anh: "vectors", "probability", "derivatives"..."""
    from app.services.i18n_service import tu_dien, ten_bai_dich
    td, tb = tu_dien("en"), ten_bai_dich("en")
    tu = set()
    for lop in (10, 11, 12):
        for b in _ppct(lop):
            for ten in (td.get(b.get("chuong") or ""), tb.get((b.get("bai") or "").strip())):
                tu.update(w for w in re.findall(r"[a-z]+", (ten or "").lower()) if len(w) >= 5)
    return frozenset(tu - {"lesson", "chapter", "their", "using", "practice"})


def _co_chu_de(t: str) -> bool:
    tu = re.findall(r"[a-z0-9]+", _bo_dau(t))
    return (any(" ".join(tu[i:i + 2]) in _cap_tu_chu_de() for i in range(len(tu) - 1))
            or any(w in _tu_chu_de_en() for w in tu))


# ---------------------------------------------------------------- nhận diện
_CUU_CHUONG = re.compile(r"b[aả]ng\s*c[uử]u\s*ch[uư][oơ]ng|multiplication\s*table|times\s*table", re.IGNORECASE)
_LOP_DUOI = re.compile(r"(?:l[oớ]p|kh[oố]i|grade)\s*([1-9])(?!\d)|ti[eể]u\s*h[oọ]c|\bthcs\b|c[aấ]p\s*[12](?!\d)"
                       r"|m[aầ]m\s*non|primary\s*school|middle\s*school", re.IGNORECASE)
_MON_KHAC = re.compile(
    r"m[oô]n\s*(?:v[aă]n|anh|l[yý]|h[oó]a|sinh|s[uử]|[dđ][iị]a|tin|gdcd|c[oô]ng\s*ngh[eệ])\b|ng[uữ]\s*v[aă]n"
    r"|v[aậ]t\s*l[yý]|h[oó]a\s*h[oọ]c|sinh\s*h[oọ]c|l[iị]ch\s*s[uử]|[dđ][iị]a\s*l[yý]|tin\s*h[oọ]c|\bgdcd\b"
    r"|\b(?:physics|chemistry|biology|history|geography|literature)\b", re.IGNORECASE)
_LOP_THPT = re.compile(r"(?:l[oớơ]p|kh[oố]i|to[aá]n|grade)\s*(10|11|12)\b", re.IGNORECASE)
# Muốn học / muốn đề (để chuyện "mình thích môn văn hơn" vẫn là trò chuyện, không bị chặn)
_MUON = re.compile(r"\b[dđ][eề]\b|b[aà]i\s*t[aậ]p|luy[eệ]n|\b[oô]n\s*(?:t[aậ]p|l[aạ]i|thi)?\b|\bd[aạ]y\b"
                   r"|gi[aả]ng|\bh[oọ]c\b|\bt[aạ]o\b|ki[eể]m\s*tra|exam|test|quiz|practi[cs]e|teach|learn|study", re.IGNORECASE)
# Nhờ tính một phép tính: "7x7=?", "7 nhân 7 bằng mấy", "12 : 4 là bao nhiêu", "tính 15 + 27"
_PHEP = r"(?:[x×*+\-/:÷]|nh[aâ]n|chia|c[oộ]ng|tr[uừ]|times|plus|minus|divided\s*by)"
_TINH = re.compile(r"^\s*(?:t[ií]nh|calculate|compute|what\s*is)?\s*\d+(?:[.,]\d+)?\s*" + _PHEP + r"\s*\d+(?:[.,]\d+)?"
                   r"(?:\s*" + _PHEP + r"\s*\d+(?:[.,]\d+)?)*\s*(?:=|b[aằ]ng|l[aà]|is|equals?)?\s*"
                   r"(?:m[aấ]y|bao\s*nhi[eê]u|\?|g[iì])*\s*[?.!]*\s*$", re.IGNORECASE)
# Muốn tạo đề / luyện tập (không nói chương, kỳ thi, chủ đề)
_MUON_DE = re.compile(
    r"(?:t[aạ]o|ra|cho|l[aà]m|mu[oố]n|c[aầ]n|xin)\b.{0,25}?(?:[dđ][eề]\b|b[aà]i\s*t[aậ]p|cho\s*(?:t[oô]i|em|m[iì]nh)\b)"
    r"|luy[eệ]n\s*t[aậ]p|r[eè]n\s*luy[eệ]n|[oô]n\s*t[aậ]p|\b(?:create|make|give\s*me)\b.{0,20}?\b(?:exam|test|quiz)"
    r"|\bpractice\b", re.IGNORECASE)
_DA_RO = re.compile(r"ch[uư][oơ]ng\s*\d|chapter\s*\d|gi[uữ]a\s*(?:h[oọ]c\s*)?k[iìyỳ]|cu[oố]i\s*(?:h[oọ]c\s*)?k[iìyỳ]"
                    r"|h[oọ]c\s*k[iìyỳ]|midterm|final|n[aă]ng\s*l[uự]c|y[eế]u|l[oờ]i\s*gi[aả]i|[dđ][aá]p\s*[aá]n"
                    r"|t[aả]i|h[oọ]c\s*l[uự]c|th[oố]ng\s*k[eê]|c[aá]ch\s*(?:t[aạ]o|d[uù]ng|l[aà]m)|h[uư][oớ]ng\s*d[aẫ]n"
                    r"|\b(?:c[aâ]u|b[aà]i)\s*\d", re.IGNORECASE)


def ngoai_pham_vi(message: str) -> str | None:
    """"cuu_chuong" | "lop_duoi" | "mon_khac" | "tinh_toan" hoặc None (trong phạm vi / chỉ là trò chuyện)."""
    t = (message or "").strip()
    if not t:
        return None
    if _CUU_CHUONG.search(t):
        return "cuu_chuong"
    if _TINH.match(t):
        return "tinh_toan"
    if _MUON.search(t) and not _LOP_THPT.search(t):
        if _LOP_DUOI.search(t):
            return "lop_duoi"
        if _MON_KHAC.search(t):
            return "mon_khac"
    return None


# Từ đệm đi kèm khi chỉ nêu lớp: "lớp 11 mà", "còn lớp 12 thì sao", "khối 11 ạ", "what about grade 11"
# (không có "học", "đang" để câu kể "tôi đang học lớp 10" vẫn là trò chuyện)
_TU_DEM = frozenset(
    "ma a chu nhe nha nhi ne di thoi con the thi sao vay em toi minh la o do day co oi phai chi cua cho voi"
    " what about and then how please i m in ok okay".split())


def chi_noi_lop(message: str) -> int | None:
    """Tin nhắn chỉ nêu một lớp THPT ("lớp 11 mà", "khối 12 ạ", "grade 11") -> số lớp; còn lại -> None."""
    t = (message or "").strip()
    m = _LOP_THPT.search(t)
    if not m or len(t) > 40:
        return None
    con_lai = re.findall(r"[a-z0-9]+", _bo_dau(t[:m.start()] + " " + t[m.end():]))
    return int(m.group(1)) if len(con_lai) <= 4 and all(w in _TU_DEM for w in con_lai) else None


def muon_de_chung_chung(message: str) -> bool:
    """Muốn tạo đề / luyện tập mà chưa nói chương, kỳ thi hay chủ đề nào; hoặc chỉ nêu lớp ("lớp 11 mà")."""
    t = (message or "").strip()
    if chi_noi_lop(t):
        return True
    return bool(t) and bool(_MUON_DE.search(t)) and not _DA_RO.search(t) and not _co_chu_de(t)


# ---------------------------------------------------------------- câu trả lời soạn sẵn
def _ds_chuong_van_ban(lop: int | None, lang: str) -> str:
    en = lang == "en"
    if lop not in (10, 11, 12):
        return ("The question bank covers high school math, grades 10, 11 and 12. Tell me your grade "
                "(e.g. \"grade 10\") and I will list its chapters."
                if en else
                "Ngân hàng đề có Toán THPT lớp 10, 11, 12. Bạn cho mình biết lớp (ví dụ \"lớp 10\") để mình liệt kê "
                "các chương nhé.")
    td = {}
    if en:
        from app.services.i18n_service import tu_dien
        td = tu_dien("en")
    dong = ["%d. %s" % (c, td.get(t, t) if en else t) for c, t in danh_sach_chuong(lop)]
    if en:
        return ("Grade %d chapters in the question bank:\n%s\n\nType e.g. \"chapter 3 test\" or \"grade %d midterm 1\", "
                "or click **📝 Create a new exam**." % (lop, "\n".join(dong), lop))
    return ("Ngân hàng đề lớp %d hiện có các chương:\n%s\n\nBạn gõ ví dụ \"đề chương 3\" (kiểm tra theo chương) hoặc "
            "\"lớp %d giữa kỳ 1\", hoặc bấm **📝 Tạo đề mới** nhé." % (lop, "\n".join(dong), lop))


_LY_DO = {
    "cuu_chuong": ("Bảng cửu chương là Toán tiểu học, không có trong ngân hàng đề của thầy/cô (chỉ có Toán THPT lớp "
                   "10-12), nên mình không tạo đề hay dạy phần này được.",
                   "The multiplication table is primary school math and is not in your teacher's question bank (high "
                   "school math, grades 10-12 only), so I cannot make exams or teach it."),
    "lop_duoi": ("Ngân hàng đề của thầy/cô chỉ có Toán THPT lớp 10-12, chưa có Toán tiểu học / THCS, nên mình không tạo "
                 "đề hay dạy phần này được.",
                 "Your teacher's question bank only has high school math (grades 10-12), not primary or middle "
                 "school, so I cannot make exams or teach that."),
    "mon_khac": ("Mình chỉ hỗ trợ môn Toán THPT theo ngân hàng đề và tài liệu của thầy/cô, môn khác mình không làm "
                 "được.",
                 "I only support high school math, using your teacher's question bank and notes; I cannot help with "
                 "other subjects."),
    "tinh_toan": ("Mình không tự tính hay giải bài mới (để tránh sai): đề và lời giải đều lấy từ ngân hàng đề của "
                  "thầy/cô, kiến thức chỉ theo tài liệu lí thuyết của thầy/cô. Muốn luyện thì tạo một đề nhé.",
                  "I do not compute or solve new problems (to avoid mistakes): exams and solutions come from your "
                  "teacher's question bank, and knowledge only from your teacher's theory notes. Create an exam to "
                  "practice."),
}


def tra_loi_ngoai_pham_vi(ly_do: str, lop: int | None, lang: str = "vi") -> str:
    i = 1 if lang == "en" else 0
    return _LY_DO[ly_do][i] + "\n\n" + _ds_chuong_van_ban(lop, lang)


def tra_loi_chon_chuong(message: str, lop_ho_so: int | None, lang: str = "vi") -> str:
    """Muốn đề nhưng chưa nói chương: lớp lấy trong tin nhắn ("tạo đề lớp 11"), không có thì lấy hồ sơ."""
    m = _LOP_THPT.search(message or "")
    lop = int(m.group(1)) if m else lop_ho_so
    mo = "Okay! Pick a chapter for your exam." if lang == "en" else "Được luôn! Bạn chọn chương để mình tạo đề nhé."
    return mo + "\n\n" + _ds_chuong_van_ban(lop, lang)


# Gợi ý chương cho lệnh trò chuyện (tro_chuyen_service): mô hình chỉ được rủ tạo đề trong các chương này.
# Luôn đủ lớp 10, 11, 12 (cô Lan 30/10/2026: trước chỉ đưa lớp trong hồ sơ -> mô hình nói "chỉ hỗ trợ Lớp 10");
# lớp trong hồ sơ đứng đầu.
def chuong_cho_lenh(lop: int | None) -> str:
    lops = ((lop,) if lop in (10, 11, 12) else ()) + tuple(l for l in (10, 11, 12) if l != lop)
    return "; ".join("Lớp %d: %s" % (l, ", ".join("Chương %d. %s" % ct for ct in danh_sach_chuong(l)))
                     for l in lops if danh_sach_chuong(l))
