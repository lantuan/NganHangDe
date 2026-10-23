"""
TRÒ CHUYỆN TRONG KHUNG CHAT (cô Lan 23/10/2026): "tôi cần chat được bình thường như chatbox bình thường khác. Chỉ là các
nội dung bên ngoài thì không giải quyết mà hướng người dùng về tạo đề và nội dung toán. Nếu hỏi về kiến thức toán thì AI
có thể đọc ngay phần lý thuyết có sẵn để trả lời, chỉ trả lời trong đó."

Hai việc, đều gọi mô hình qua webhook GIA SƯ đã có (n8n `gia-su`: nhận `lenh_he_thong` + `cau_hoi`, không Memory, không
Tool) - KHÔNG phải sửa n8n, không thêm node:

1. tra_loi_kien_thuc: câu hỏi kiến thức ("tập rỗng là gì", "định lý sin", "phương sai là gì") -> tìm đúng đoạn trong tài
   liệu lí thuyết của cô (ly_thuyet_service.tim_doan_tu_do) -> mô hình CHỈ được trả lời theo đoạn đó (dẫn nguyên văn,
   không tự tính, không giải bài cụ thể). Không tìm thấy đoạn nào -> không gọi mô hình (None), để luồng cũ lo.
2. tro_chuyen: trò chuyện thường khi CHV_Fun (n8n) hỏng - thân thiện, ngắn; chuyện ngoài lề thì đáp vui một câu rồi
   hướng về tạo đề / ôn Toán. Bình thường CHV_Fun vẫn trả lời như cũ.

Lỗi gì (chưa cấu hình webhook, mạng, mô hình) -> None, nơi gọi đi đường cũ. Không trừ lượt hỏi gia sư.
"""
from __future__ import annotations

import re

from app.services import gia_su_service, pham_vi_service
from app.services.ly_thuyet_service import tim_doan_tu_do, thanh_van_ban_lenh

# Hỏi kiến thức: "là gì", "định nghĩa", "công thức", "tính chất"... (không phải yêu cầu tạo đề, không nhắc câu nào của đề)
_KIEN_THUC = re.compile(
    r"l[aà]\s*g[iì]\b|l[aà]\s*sao\b|ngh[iĩ]a\s*l[aà]|[dđ][iị]nh\s*ngh[iĩ]a|kh[aá]i\s*ni[eệ]m|c[oô]ng\s*th[uứ]c"
    r"|t[ií]nh\s*ch[aấ]t|[dđ][iị]nh\s*l[yýií]|h[eệ]\s*qu[aả]|th[eế]\s*n[aà]o\s*l[aà]|k[ií]\s*hi[eệ]u|c[aá]ch\s*t[ií]nh"
    r"|c[aá]ch\s*t[iì]m|c[aá]ch\s*x[aá]c\s*[dđ][iị]nh|ph[aâ]n\s*bi[eệ]t|kh[aá]c\s*nhau|\bwhat\s+is\b|\bdefin",
    re.IGNORECASE)
_NHAC_DE = re.compile(r"\b(c[aâ]u|b[aà]i)\s*\d+|gi[aả]ng\s*l[aạ]i|[dđ][eề]\s*(v[uừ]a|n[aà]y|c[uũ])|trong\s*[dđ][eề]",
                      re.IGNORECASE)
_TAO_DE = re.compile(r"t[aạ]o\s*[dđ][eề]|ra\s*[dđ][eề]|cho\s*(t[oô]i|em|m[iì]nh)\s*([0-9]+\s*)?[dđ][eề]"
                     r"|[dđ][eề]\s*(l[oớ]p|ki[eể]m\s*tra|gi[uữ]a|cu[oố]i|thi)|l[oờ]i\s*gi[aả]i|[dđ][aá]p\s*[aá]n",
                     re.IGNORECASE)


def la_cau_hoi_kien_thuc(message: str) -> bool:
    """Câu hỏi kiến thức Toán tự do (không gắn câu nào của đề, không xin tạo đề / lời giải)."""
    t = (message or "").strip()
    return bool(t) and bool(_KIEN_THUC.search(t)) and not _NHAC_DE.search(t) and not _TAO_DE.search(t)


def _xung_ho(vai_tro: str | None, en: bool) -> str:
    gv = bool(vai_tro) and vai_tro not in ("hoc_sinh", "student")
    if en:
        return "Call yourself \"I\" and address the user as \"you\"."
    return ('Xưng "em", gọi người dùng là "thầy/cô".' if gv else 'Xưng "mình", gọi người dùng là "bạn".')


LENH_KIEN_THUC = """Bạn là trợ giảng Toán THPT của trang Ngân Hàng Đề. Người dùng hỏi một câu KIẾN THỨC.

QUY TẮC BẮT BUỘC:
1. CHỈ trả lời bằng nội dung trong TÀI LIỆU LÍ THUYẾT CỦA THẦY/CÔ bên dưới. Dẫn lại đúng định nghĩa, công thức,
   tính chất như trong tài liệu (có thể diễn đạt lại cho dễ hiểu, thêm một ví dụ ngắn ĐÃ CÓ trong tài liệu).
2. KHÔNG dùng kiến thức ngoài tài liệu, KHÔNG tự tính toán ra số mới, KHÔNG giải bài toán cụ thể người dùng đưa ra.
3. Tài liệu không nói tới điều được hỏi thì trả lời đúng ý: "Phần này chưa có trong tài liệu lí thuyết của thầy/cô"
   rồi gợi ý tạo đề luyện tập hoặc hỏi trực tiếp thầy/cô trên lớp.
4. Ngắn gọn (dưới 120 chữ), thân thiện. {xung_ho} Công thức viết LaTeX trong $...$.
5. Kết thúc bằng một dòng: "Xem lại: bài <tên bài>, mục <tên mục>." (lấy từ tài liệu đã dùng).
6. Trả lời văn bản thường, KHÔNG JSON.

TÀI LIỆU LÍ THUYẾT CỦA THẦY/CÔ:
{ly_thuyet}
"""

LENH_KIEN_THUC_EN = """You are a high school math teaching assistant on the Ngan Hang De website. The user asks a KNOWLEDGE
question.

MANDATORY RULES:
1. Answer ONLY from YOUR TEACHER'S THEORY NOTES below (they are in Vietnamese: translate faithfully into English, quoting
   the definition, formula or property as written).
2. Do NOT use knowledge outside the notes, do NOT compute new numbers, do NOT solve a specific problem.
3. If the notes do not cover the question, say "This is not in your teacher's theory notes yet" and suggest creating a
   practice exam or asking the teacher in class.
4. Short (under 120 words), friendly. {xung_ho} Write formulas in LaTeX inside $...$.
5. End with one line: "Review: lesson <lesson name>, section <section name>." (from the notes you used).
6. Plain text, NOT JSON.

YOUR TEACHER'S THEORY NOTES:
{ly_thuyet}
"""

LENH_TRO_CHUYEN = """Bạn là trợ lý vui vẻ của trang Ngân Hàng Đề Toán THPT (tạo đề Toán, làm bài trên web, chấm điểm,
thầy/cô AI giảng lại câu trong đề đã làm, có bản tiếng Anh cho Lớp 10 Chương 1-4).
Trò chuyện TỰ NHIÊN như một người bạn: chào hỏi, đùa nhẹ, động viên học tập đều được. {xung_ho}
- Chuyện ngoài Toán / ngoài trang (giải trí, đời tư, chính trị, bài môn khác...): đáp vui MỘT câu, KHÔNG đi sâu, rồi khéo
  léo hướng về việc tạo đề luyện tập hoặc ôn Toán.
- KHÔNG giải bài toán, KHÔNG tự tính toán (kể cả phép tính dễ như 7 x 7), KHÔNG bịa tính năng. Muốn học kiến thức
  thì gợi ý hỏi kiểu "tập rỗng là gì" (chỉ trả lời theo tài liệu lí thuyết của thầy/cô); muốn được giảng bài thì làm
  đề, nộp bài rồi bấm "💬 Hỏi thầy/cô AI về câu này".
- PHẠM VI (thầy/cô tạo trang này chốt): đề CHỈ lấy từ ngân hàng đề của thầy/cô, gồm các chương: {chuong}.
  TUYỆT ĐỐI KHÔNG rủ / hứa tạo đề hay dạy nội dung ngoài danh sách đó (bảng cửu chương, Toán tiểu học, THCS, môn
  khác...). Muốn rủ luyện tập thì nêu đúng một chương trong danh sách và bảo gõ "đề chương <số>" hoặc bấm "📝 Tạo đề
  mới". KHÔNG hỏi người dùng số câu, chủ đề, phép tính... (bạn không tự tạo đề được).
- Ngắn (2-4 câu), có thể dùng 1-2 emoji. Trả lời văn bản thường, KHÔNG JSON.
{lich_su}"""

LENH_TRO_CHUYEN_EN = """You are the cheerful assistant of the Ngan Hang De high school math website (create math exams, take
them on the web with automatic grading, the AI teacher explains questions of exams you took, English versions for Grade 10
Chapters 1-4). Chat NATURALLY like a friend: greetings, light jokes, encouragement are fine. {xung_ho} Reply in ENGLISH.
- Topics outside math / the website: reply playfully in ONE sentence, do not go deeper, then gently steer back to creating
  a practice exam or studying math.
- Do NOT solve problems, do NOT compute (not even 7 x 7), do NOT invent features.
- SCOPE (set by the teacher who runs this site): exams come ONLY from the teacher's question bank, chapters: {chuong}
  (Vietnamese names; translate them). NEVER offer or promise exams or lessons outside that list (multiplication table,
  primary or middle school math, other subjects...). To suggest practice, name one chapter from the list and tell the
  user to type "chapter <number> test" or click "📝 Create a new exam". Do NOT ask for number of questions or topics (you
  cannot create exams yourself).
- Short (2-4 sentences), 1-2 emoji at most. Plain text, NOT JSON.
{lich_su}"""


def co_tai_lieu(message: str, lop: int | None) -> bool:
    """Tài liệu lí thuyết của thầy/cô có đoạn nào nói tới câu hỏi này không."""
    try:
        return bool(tim_doan_tu_do(lop, message))
    except Exception:                                                # noqa: BLE001
        return True                                                  # không chắc thì để đường cũ lo


KHONG_CO_TAI_LIEU = ("Phần này chưa có trong tài liệu lí thuyết của thầy/cô, nên mình không giảng được (mình chỉ dạy "
                     "theo tài liệu thầy/cô đưa, thuộc Toán THPT lớp 10-12). Bạn hỏi trực tiếp thầy/cô trên lớp, "
                     "hoặc tạo một đề luyện tập theo chương nhé.")
KHONG_CO_TAI_LIEU_EN = ("This is not in your teacher's theory notes yet, so I cannot teach it (I only teach from the "
                        "notes your teacher provides, high school math grades 10-12). Ask your teacher in class, or "
                        "create a practice exam by chapter.")


def tra_loi_kien_thuc(message: str, lop: int | None, lang: str = "vi", vai_tro: str | None = None) -> dict | None:
    """{"tra_loi", "ly_thuyet"} hoặc None (không thấy đoạn tài liệu nào / chưa cấu hình / mô hình lỗi)."""
    if not gia_su_service.N8N_WEBHOOK_GIA_SU:
        return None
    doan = tim_doan_tu_do(lop, message)
    if not doan:
        return None
    en = lang == "en"
    lenh = (LENH_KIEN_THUC_EN if en else LENH_KIEN_THUC).format(xung_ho=_xung_ho(vai_tro, en),
                                                                 ly_thuyet=thanh_van_ban_lenh(doan))
    try:
        tra_loi = gia_su_service._goi_mo_hinh({"muc": "kien_thuc", "lenh_he_thong": lenh, "cau_hoi": message,
                                               "lich_su": []})
    except Exception as e:                                           # noqa: BLE001
        print("LOI TRA LOI KIEN THUC:", e)
        return None
    return {"tra_loi": tra_loi, "ly_thuyet": doan} if tra_loi else None


def tro_chuyen(message: str, lich_su: list[tuple[str, str]] | None = None, lang: str = "vi",
               vai_tro: str | None = None, lop: int | None = None) -> str | None:
    """Câu trả lời trò chuyện (khi CHV_Fun hỏng). lich_su: vài cặp (vai, nội dung) gần nhất. Lỗi -> None."""
    if not gia_su_service.N8N_WEBHOOK_GIA_SU or not (message or "").strip():
        return None
    en = lang == "en"
    dong = ["%s: %s" % ("Người dùng" if v == "user" else "Trợ lý", (n or "")[:200]) for v, n in (lich_su or [])[-4:]]
    ls = ("\nMấy tin nhắn trước (để hiểu ngữ cảnh, không cần nhắc lại):\n" + "\n".join(dong)) if dong else ""
    lenh = (LENH_TRO_CHUYEN_EN if en else LENH_TRO_CHUYEN).format(xung_ho=_xung_ho(vai_tro, en), lich_su=ls,
                                                                   chuong=pham_vi_service.chuong_cho_lenh(lop))
    try:
        return gia_su_service._goi_mo_hinh({"muc": "tro_chuyen", "lenh_he_thong": lenh, "cau_hoi": message,
                                            "lich_su": []}) or None
    except Exception as e:                                           # noqa: BLE001
        print("LOI TRO CHUYEN:", e)
        return None
