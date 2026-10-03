"""
GIA SU AI - MUC A: giang lai CHINH cau hoi trong de hoc sinh vua lam.

NGUYEN TAC BAT BIEN (yeu cau cua co Lan, khong duoc noi long):
  "Khong ra ngoai bat ki cai nao. Dap an thi phai lay ngay dap an Python
   toi da chuan bi theo de. Khong duoc de AI tu tinh toan."

Ba lop khoa doc lap, hong 1 lop thi 2 lop con lai van con:

  LOP 1 - CAU LENH (dung_lenh o duoi): mo hinh nhan de bai, dap an dung
          va loi giai chuan DA CO SAN; nhiem vu duy nhat la dien dat lai
          loi giai do cho de hieu. Cam tinh toan, cam doi so, cam noi
          sang cau khac hay kien thuc ngoai de.

  LOP 2 - HIEN THI: API luon tra ve `dap_an_python` + `loi_giai_python`
          NGUYEN VAN (doc tu file dapan_json do generator Python sinh),
          va giao dien hien no NGAY CANH cau tra loi cua AI. Neu AI noi
          lech, hoc sinh nhin thay ngay o hai cot.

  LOP 3 - NHAT KI: moi luot hoi deu ghi vao gia_su_hoi_dap ca cau tra
          loi cua AI lan dap an Python da dua vao lenh. Giao vien doc
          lai o /gv/gia-su.

NGUON DU LIEU (theo thu tu uu tien):
  1. file dapan_json cua de (file_de.loai_file='dapan_json') - day la
     ban goc do Python sinh, co de_bai + dap_an + loi_giai day du.
  2. exam_history.chi_tiet_bai_lam - dung khi file dapan_json da bi don
     dep (sau 1 ngay). Chi con loi_giai, khong con de_bai day du.
  Khong tim thay ca hai -> BAO LOI, tuyet doi khong goi mo hinh, vi luc
  do AI se phai tu nghi ra de bai = dung cai ma nguyen tac cam.

MUC B (chi dung cho hoc sinh van chua hieu -> tro ve dung cho trong tai
lieu li thuyet .tex cua co) chua lam o ban nay, xem docs/23_GIA_SU_AI.md.
"""
from app.services.answer_parser_service import loi_giai_cho_web
import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

from app.core.config import (
    GIA_SU_DO_DAI_CAU_HOI,
    GIA_SU_LUOT_MOI_NGAY,
    N8N_WEBHOOK_GIA_SU,
)
from app.core.supabase import supabase_admin as supabase
from app.services import history_service
from app.services.latex_service import TEMP_DIR_EN

# Gio Viet Nam - dung de chot "ngay" cho han muc luot hoi. Neu dung UTC
# thi tu 7h sang den 0h (gio VN) bi tinh sang ngay hom sau, hoc sinh mat
# luot giua buoi hoc.
MUI_GIO_VN = timezone(timedelta(hours=7))

def _t(lang: str, vi: str, en: str) -> str:
    """Thông báo cho học sinh theo ngôn ngữ trang (nền là tiếng Việt)."""
    return en if lang == "en" else vi


CAU_TU_CHOI_EN = (
    "This question is outside what your teacher has prepared, so please ask your teacher directly. "
    "Here your teacher only reviews the questions from the exam you just took."
)

CAU_TU_CHOI = (
    "Câu này nằm ngoài phần thầy/cô đã chuẩn bị nên em hỏi trực tiếp "
    "thầy/cô nhé. Ở đây thầy/cô chỉ giảng lại đúng các câu trong đề em vừa làm."
)


class GiaSuError(Exception):
    """Loi co the hien thang cho hoc sinh doc (da viet bang tieng Viet)."""


# ======================================================
# 1. NGU CANH: de bai + dap an + loi giai CHUAN (do Python sinh)
# ======================================================

def _doc_dapan_json(de: dict, lang: str = "vi") -> list[dict] | None:
    duong_dan = (de.get("files") or {}).get("dapan_json")
    if not duong_dan:
        return None
    tep = Path(duong_dan)
    # Nền là tiếng Việt; trang ở English thì lấy bản Anh của ĐÚNG đề đó (tệp cạnh, cùng tên) nếu có.
    if lang == "en" and (TEMP_DIR_EN / tep.name).exists():
        tep = TEMP_DIR_EN / tep.name
    if not tep.exists():
        return None
    try:
        return json.loads(tep.read_text(encoding="utf-8"))
    except Exception as e:
        print("LOI DOC dapan_json cho gia su:", e)
        return None


def _mo_ta_dap_an(cau: dict, lang: str = "vi") -> str:
    """Bien dap an cua 1 cau thanh 1 dong chu de doc, dung cho ca 3 loai.
    KHONG tinh toan gi - chi doc lai nhung gi generator da ghi san."""
    loai = (cau.get("loai_cau") or "").upper()
    if loai == "MC":
        nhan = cau.get("dap_an") or cau.get("dap_an_dung") or ""
        phuong_an = cau.get("phuong_an") or {}
        noi_dung = phuong_an.get(nhan, "")
        return f"{nhan}. {noi_dung}".strip(". ") if noi_dung else str(nhan)
    if loai == "TF":
        dap_an = cau.get("dap_an") or cau.get("dap_an_dung") or {}
        if isinstance(dap_an, dict):
            return "; ".join(
                f"{y}) {('True' if gt else 'False') if lang == 'en' else ('Đúng' if gt else 'Sai')}"
                for y, gt in sorted(dap_an.items())
            )
        return str(dap_an)
    return str(cau.get("dap_an") or cau.get("dap_an_dung") or "")


def _mo_ta_de_bai(cau: dict) -> str:
    """De bai day du: than cau + cac phuong an / cac y a,b,c,d."""
    phan = [str(cau.get("de_bai") or "").strip()]
    loai = (cau.get("loai_cau") or "").upper()
    if loai == "MC":
        for nhan, noi in sorted((cau.get("phuong_an") or {}).items()):
            phan.append(f"{nhan}. {noi}")
    elif loai == "TF":
        for y, noi in sorted((cau.get("phat_bieu") or {}).items()):
            phan.append(f"{y}) {noi}")
    return "\n".join(p for p in phan if p)


def lay_ngu_canh_cau(de_id: str, so_thu_tu: int, user_id: str | None = None, lang: str = "vi") -> dict:
    """
    Tra ve {de_bai, dap_an, loi_giai, question_id, loai_cau, chuong, bai,
    nguon}. Nem GiaSuError neu khong du du lieu - KHONG BAO GIO tra ve
    ngu canh rong roi van goi mo hinh.
    """
    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise GiaSuError(_t(lang, "Không tìm thấy đề này. Em thử tạo đề mới rồi hỏi lại nhé.",
                            "We could not find this exam. Please create a new one and ask again."))

    # --- Nguon 1: file dap an goc do Python sinh ---
    danh_sach = _doc_dapan_json(de, lang)
    if danh_sach:
        for cau in danh_sach:
            if int(cau.get("so_thu_tu") or 0) != int(so_thu_tu):
                continue
            loi_giai = str(cau.get("loi_giai") or "").strip()
            if not loi_giai:
                raise GiaSuError(_t(
                    lang,
                    f"Câu {so_thu_tu} chưa có lời giải mẫu trong ngân hàng nên "
                    "chưa giảng lại được. Em hỏi trực tiếp thầy/cô nhé.",
                    f"Question {so_thu_tu} has no model solution in the bank yet, so it cannot be "
                    "reviewed here. Please ask your teacher directly."))
            return {
                "de_bai": _lam_sach_latex(_mo_ta_de_bai(cau)),
                "dap_an": _lam_sach_latex(_mo_ta_dap_an(cau, lang)),
                "loi_giai": _lam_sach_latex(loi_giai_cho_web(loi_giai, lang)),
                "question_id": cau.get("generator_id") or cau.get("question_id"),
                "loai_cau": cau.get("loai_cau"),
                "chuong": cau.get("chuong"),
                "bai": cau.get("bai"),
                "nguon": "dapan_json",
            }
        raise GiaSuError(_t(lang, f"Đề này không có câu {so_thu_tu}.",
                            f"This exam has no question {so_thu_tu}."))

    # --- Nguon 2: lich su cham bai (khi file dapan_json da bi don dep) ---
    if user_id:
        cau = _tim_trong_lich_su(user_id, de_id, so_thu_tu)
        if cau:
            return cau

    raise GiaSuError(_t(
        lang,
        "Dữ liệu chi tiết của đề này đã được dọn dẹp (đề cũ hơn 1 ngày) nên "
        "chưa giảng lại được. Em tạo đề mới cùng dạng rồi hỏi lại nhé.",
        "The details of this exam have been cleaned up (exams older than 1 day), so it cannot be "
        "reviewed. Please create a new exam of the same type and ask again."))


def _tim_trong_lich_su(user_id: str, de_id: str, so_thu_tu: int) -> dict | None:
    try:
        ket_qua = (
            supabase.table("exam_history")
            .select("chi_tiet_bai_lam")
            .eq("student_id", user_id)
            .eq("de_thi_id", de_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception as e:
        print("LOI DOC exam_history cho gia su:", e)
        return None
    if not ket_qua.data:
        return None
    for cau in ket_qua.data[0].get("chi_tiet_bai_lam") or []:
        if int(cau.get("so_thu_tu") or 0) != int(so_thu_tu):
            continue
        loi_giai = str(cau.get("loi_giai") or "").strip()
        if not loi_giai:
            return None
        return {
            # exam_history khong luu de_bai -> de trong, cau lenh se noi ro
            # cho mo hinh la CHI duoc bam vao loi giai, khong doan de bai.
            "de_bai": "",
            "dap_an": _lam_sach_latex(str(cau.get("dap_an_dung") or "")),
            "loi_giai": _lam_sach_latex(loi_giai_cho_web(loi_giai)),
            "question_id": cau.get("question_id"),
            "loai_cau": cau.get("loai_cau"),
            "chuong": cau.get("chuong"),
            "bai": cau.get("bai"),
            "nguon": "exam_history",
        }
    return None


# ======================================================
# 1. LAM SACH LATEX TRUOC KHI DUA RA WEB / DUA VAO LENH
# ======================================================
# Loi giai do Python sinh ra la LaTeX danh cho goi ex_test (de bien dich
# PDF). Tren web, MathJax KHONG biet cac moi truong rieng cua goi do nen
# in thang loi ra man hinh hoc sinh:
#     Unknown environment 'itemchoice'
# (co Lan gap 24/09/2026). Va dua nguyen van sang mo hinh cung khong hay:
# no tuong \begin{itemchoice} la mot phan cua de bai.
#
# Cach lam: giu DANH SACH TRANG cac moi truong MathJax that su hieu; moi
# thu khac thi BO CAP \begin{}/\end{} nhung GIU NGUYEN RUOT - noi dung
# toan hoc ben trong khong duoc mat.

# Cac moi truong MathJax ho tro (khong dung den goi ngoai).
MOI_TRUONG_MATHJAX = {
    "align", "align*", "aligned", "alignat", "alignat*",
    "array", "cases", "dcases", "rcases",
    "matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix", "Bmatrix",
    "smallmatrix", "subarray", "split",
    "equation", "equation*", "gather", "gather*", "eqnarray", "eqnarray*",
}

# Lenh cua ex_test chi co nghia khi bien dich PDF - bo han tren web.
_LENH_BO_HAN = re.compile(
    r"\\(?:loigiai|choiceTFt|choiceTF|choice|shortans|True|immini"
    r"|hetde|tieude|chantrang|dapan)\b"
)

# \itemch danh dau TUNG Y a) b) c) d) cua cau Dung/Sai. Xoa han thi 4 y
# dinh lien nhau thanh mot doan dai kho doc (co Lan 24/09/2026: "nhin rat
# kho chiu") - nen doi thanh XUONG DONG: vua sach, vua de doc.
_LENH_XUONG_DONG = re.compile(r"\\(?:itemch|itemTF)\b")
_MOI_TRUONG = re.compile(r"\\(begin|end)\{([a-zA-Z*]+)\}")


def _lam_sach_latex(van_ban: str) -> str:
    """Bo cac lenh/moi truong LaTeX rieng cua ex_test, GIU nguyen phan
    toan hoc. Dung cho ca phan hien thi lan phan dua vao cau lenh."""
    if not van_ban:
        return ""
    s = str(van_ban)
    s = _LENH_XUONG_DONG.sub("\n", s)
    s = _LENH_BO_HAN.sub("", s)
    s = _MOI_TRUONG.sub(
        lambda m: m.group(0) if m.group(2) in MOI_TRUONG_MATHJAX else "", s
    )
    # Gon lai khoang trang thua sinh ra sau khi bo lenh.
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ======================================================
# 1a. NHAN DIEN Y DINH "HOI BAI" NGAY TRONG CHAT
# ======================================================
# Hoc sinh vua nop bai xong, go "toi khong hieu bai 1" trong chat. CHV_Fun
# khong co cach nao biet trong hoi thoai nay da co de - no chi doc moi cau
# chu - nen tu choi va bao em ay di TAO DE, trong khi em ay vua lam xong.
# Vo li voi nguoi dung, va la loi cua chung ta chu khong phai cua prompt.
#
# May chu thi BIET CHAC: conversation_id -> de gan nhat -> da nop bai chua.
# Nen bat ngay o Python TRUOC khi goi n8n: mot bieu thuc chinh quy thay cho
# mot luot goi mo hinh doan sai ("Uu tien Code hon AI", docs/00).
#
# CO Y KHONG DOAN SO CAU (co Lan chot 18/09/2026): "bai 1" co the la cau 1
# cua de, cung co the la bai 1 trong sach. Doan sai thi giang nham cau -
# te hon nhieu so voi viec bat hoc sinh bam them mot nut. Nhan ra y dinh
# thi MO BANG CHON CAU, de chinh em ay chi dung cau minh can.

_TU_HOI_BAI = (
    r"kh[oô]ng hi[eể]u|ch[uư]a hi[eể]u|kh[oô]ng bi[eế]t l[aà]m|kh[oô]ng l[aà]m [dđ][uư][oơ]?[cợ]"
    r"|gi[aả]ng( l[aạ]i)?|gi[aả]i th[ií]ch|h[uư][oơ]?[nớ]ng d[aẫ]n|ch[ỉi] gi[uú]p|ch[ỉi] c[aá]ch"
    r"|gi[aả]i (gi[uú]p|h[oộ]|d[uù]m|gi[uù]m)|l[aà]m sao ra|v[iì] sao (l[aạ]i )?ra|t[aạ]i sao"
    r"|h[oỏ]i b[aà]i|sai [oở] [dđ][aâ]u"
)
# "huong dan su dung", "cach dung he thong"... la Rule 5 (help), khong phai
# hoi bai - loai ra de khong cuop mat cua CHV_Fun.
_TU_LOAI_TRU = r"s[uử] d[uụ]ng|d[uù]ng (web|h[eệ] th[oố]ng|trang)|c[aá]ch t[aạ]o [dđ][eề]|t[ií]nh n[aă]ng"

_MAU_HOI_BAI = re.compile(_TU_HOI_BAI, re.IGNORECASE)
_MAU_LOAI_TRU = re.compile(_TU_LOAI_TRU, re.IGNORECASE)


def la_y_dinh_hoi_bai(message: str) -> bool:
    """
    True khi tin nhan NGHE NHU dang hoi bai / nho giang lai.
    KHONG tra ve so cau: xem ghi chu o tren, co y khong doan.
    Ham nay chi la mot nua dieu kien - nua con lai la hoi thoai PHAI co de
    da nop bai (xem chat.py), neu khong thi van de CHV_Fun tra loi nhu cu.
    """
    if not message:
        return False
    van_ban = message.strip()
    if _MAU_LOAI_TRU.search(van_ban):
        return False
    return bool(_MAU_HOI_BAI.search(van_ban))


def co_de_da_nop_bai(user_id: str, conversation_id: str) -> bool:
    """Hoi thoai nay da co de VA hoc sinh da nop bai chua. Nuot moi loi:
    khong chac thi tra False de di duong cu (CHV_Fun), khong chan nham."""
    try:
        de = history_service.lay_de_gan_nhat(conversation_id)
        if de is None:
            return False
        return bool(_cac_cau_da_lam(user_id, de["id"]))
    except Exception as e:
        print("LOI KIEM TRA de da nop bai:", e)
        return False


# ======================================================
# 1b. LIET KE CAC CAU CUA DE GAN NHAT (cho nut "Hoi lai de cu")
# ======================================================
# Vi sao co ham nay: hoc sinh vua tao de xong thi trong dau da co ngu
# canh roi, khong ai nghi phai noi lai "cau 3 cua de vua nay". Bat mo
# hinh doan cho do la sai tu goc. Bam nut thi CODE BIET CHAC de nao,
# cau nao - dung nguyen tac "Uu tien Code hon AI" (docs/00).

# Ten 4 phan, dung thu tu nhu de cua Bo (xem exam_assembler_service).
TEN_PHAN = {
    "MC": "PHẦN I. Trắc nghiệm nhiều phương án",
    "TF": "PHẦN II. Đúng/Sai",
    "SA": "PHẦN III. Trả lời ngắn",
    "TL": "PHẦN IV. Tự luận",
}
TEN_PHAN_EN = {
    "MC": "PART I. Multiple choice",
    "TF": "PART II. True/False",
    "SA": "PART III. Short answer",
    "TL": "PART IV. Free response",
}
THU_TU_PHAN = ["MC", "TF", "SA", "TL"]


def _cac_cau_da_lam(user_id: str, de_id: str) -> set[int]:
    """So thu tu cac cau hoc sinh DA NOP BAI. Cau chua lam thi khong cho
    hoi (co Lan chot): neu khong, hoc sinh bam luot ca de de lay loi giai
    ma khong chiu nghi - vi giang lai luon kem dap an chuan."""
    try:
        ket_qua = (
            supabase.table("exam_history")
            .select("chi_tiet_bai_lam")
            .eq("student_id", user_id)
            .eq("de_thi_id", de_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception as e:
        print("LOI DOC exam_history (cac cau da lam):", e)
        return set()
    if not ket_qua.data:
        return set()
    da_lam = set()
    for cau in ket_qua.data[0].get("chi_tiet_bai_lam") or []:
        try:
            da_lam.add(int(cau.get("so_thu_tu")))
        except (TypeError, ValueError):
            continue
    return da_lam


def liet_ke_cau_de_gan_nhat(user_id: str, conversation_id: str, lang: str = "vi") -> dict:
    """
    Tra ve de gan nhat trong 1 cuoc hoi thoai, chia thanh 4 phan, moi cau
    kem co hoi duoc hay khong.
      {de_id, tieu_de, da_lam_bai, cac_phan: [{ma, ten, cau: [...]}]}
    Nem GiaSuError neu chua co de / du lieu da bi don dep.
    """
    de = history_service.lay_de_gan_nhat(conversation_id)
    if de is None:
        raise GiaSuError(_t(lang, "Cuộc trò chuyện này chưa có đề nào. Em tạo một đề rồi quay lại nhé.",
                            "This conversation has no exam yet. Create one and come back."))

    danh_sach = _doc_dapan_json(de, lang)
    if not danh_sach:
        raise GiaSuError(_t(
            lang,
            "Dữ liệu chi tiết của đề này đã được dọn dẹp (đề cũ hơn 1 ngày) nên "
            "chưa hỏi lại được. Em tạo đề mới cùng dạng nhé.",
            "The details of this exam have been cleaned up (exams older than 1 day). "
            "Please create a new exam of the same type."))

    da_lam = _cac_cau_da_lam(user_id, de["id"])

    theo_phan: dict[str, list[dict]] = {ma: [] for ma in THU_TU_PHAN}
    for cau in danh_sach:
        loai = (cau.get("loai_cau") or "MC").upper()
        if loai not in theo_phan:
            loai = "MC"
        try:
            stt = int(cau.get("so_thu_tu"))
        except (TypeError, ValueError):
            continue
        co_loi_giai = bool(str(cau.get("loi_giai") or "").strip())
        theo_phan[loai].append({
            "so_thu_tu": stt,
            "da_lam": stt in da_lam,
            "co_loi_giai": co_loi_giai,
            # Chi cho bam khi DA NOP BAI va cau do co loi giai chuan.
            "hoi_duoc": (stt in da_lam) and co_loi_giai,
        })

    cac_phan = []
    for ma in THU_TU_PHAN:
        if not theo_phan[ma]:
            continue
        # Danh so lai TU 1 trong moi phan, y het file PDF va trang lam bai
        # (co Lan chot 28/09/2026). so_thu_tu van giu nguyen la so 1 mach -
        # do la khoa gui len may chu khi hoc sinh bam hoi mot cau.
        cau_sap_xep = sorted(theo_phan[ma], key=lambda c: c["so_thu_tu"])
        for vi_tri, cau in enumerate(cau_sap_xep, start=1):
            cau["so_trong_phan"] = vi_tri
        cac_phan.append({
            "ma": ma,
            "ten": TEN_PHAN_EN[ma] if lang == "en" else TEN_PHAN[ma],
            "cau": cau_sap_xep,
        })

    blueprint = de.get("blueprint") or {}
    return {
        "de_id": de["id"],
        "tieu_de": blueprint.get("tieu_de") or "Đề vừa tạo",
        "da_lam_bai": bool(da_lam),
        "cac_phan": cac_phan,
    }


# ======================================================
# 2. CAU LENH (LOP KHOA 1)
# ======================================================

LENH_HE_THONG = """Bạn là trợ giảng Toán của một lớp THPT Việt Nam, đang giảng lại
MỘT câu hỏi cụ thể cho học sinh vừa làm bài xong.

QUY TẮC BẮT BUỘC - vi phạm bất kì điều nào là hỏng nhiệm vụ:
1. KHÔNG TỰ TÍNH TOÁN. Đáp án đúng và lời giải mẫu đã được cho sẵn bên dưới.
   Việc của bạn là DIỄN ĐẠT LẠI lời giải đó cho dễ hiểu, không phải giải lại.
2. KHÔNG ĐƯỢC đưa ra con số, kết quả trung gian hay kết luận nào KHÁC với
   lời giải mẫu. Nếu lời giải mẫu không nói tới điều học sinh hỏi, hãy trả lời
   đúng câu này: "{cau_tu_choi}"
3. CHỈ nói về đúng câu hỏi này. Không nhắc câu khác, không mở rộng sang kiến
   thức ngoài đề, không gợi ý tài liệu bên ngoài.
4. Xưng "thầy/cô", gọi học sinh là "em". Tiếng Việt, ngắn gọn, thân thiện.
5. Trình bày công thức bằng LaTeX trong dấu $...$ như lời giải mẫu.
6. Nếu học sinh hỏi chuyện ngoài Toán hoặc ngoài câu này, trả lời đúng câu ở
   quy tắc 2 và dừng lại.

ĐỀ BÀI (nguyên văn):
{de_bai}

ĐÁP ÁN ĐÚNG (do chương trình Python sinh đề tính sẵn - đây là đáp án duy nhất đúng):
{dap_an}

LỜI GIẢI MẪU (nguồn duy nhất bạn được dùng):
{loi_giai}
"""

LENH_HE_THONG_EN = """You are a math teaching assistant for a high school class, reviewing ONE specific
question with a student who has just finished the exam.

MANDATORY RULES - breaking any one of them means failing the task:
1. DO NOT DO ANY CALCULATION YOURSELF. The correct answer and the model solution are given below.
   Your job is to RE-EXPLAIN that solution so it is easy to understand, not to solve the problem again.
2. NEVER give any number, intermediate result or conclusion that DIFFERS from the model solution. If the
   model solution does not cover what the student asks, reply with exactly this sentence: "{cau_tu_choi}"
3. Talk ONLY about this question. Do not mention other questions, do not go beyond the exam material, and
   do not point to outside resources.
4. Refer to yourself as "your teacher" and address the student as "you". Reply in ENGLISH (US math
   terminology), short and friendly.
5. Write formulas in LaTeX inside $...$ as in the model solution.
6. If the student asks about anything outside math or outside this question, reply with exactly the
   sentence in rule 2 and stop.

QUESTION (verbatim):
{de_bai}

CORRECT ANSWER (computed by the Python generator - this is the only correct answer):
{dap_an}

MODEL SOLUTION (the only source you may use):
{loi_giai}
"""

LENH_KHI_MAT_DE_BAI_EN = (
    "(The original question text is no longer stored. NEVER guess the question; only re-explain "
    "the steps of the model solution.)"
)

LENH_KHI_MAT_DE_BAI = (
    "(Không còn lưu đề bài gốc. TUYỆT ĐỐI không đoán lại đề bài; chỉ giảng "
    "lại các bước trong lời giải mẫu.)"
)


def dung_lenh(ngu_canh: dict, cau_hoi: str, lich_su: list[dict] | None = None, lang: str = "vi") -> dict:
    """Dung payload gui sang n8n. Tach rieng ra 1 ham de test duoc ma
    khong can mang, va de doc lai duoc chinh xac cai gi da gui di."""
    en = lang == "en"
    de_bai = ngu_canh.get("de_bai") or (LENH_KHI_MAT_DE_BAI_EN if en else LENH_KHI_MAT_DE_BAI)
    he_thong = (LENH_HE_THONG_EN if en else LENH_HE_THONG).format(
        cau_tu_choi=CAU_TU_CHOI_EN if en else CAU_TU_CHOI,
        de_bai=de_bai,
        dap_an=ngu_canh.get("dap_an") or ("(none)" if en else "(không có)"),
        loi_giai=ngu_canh.get("loi_giai") or "",
    )
    return {
        "muc": "A",
        "lenh_he_thong": he_thong,
        "cau_hoi": cau_hoi,
        "lich_su": lich_su or [],
        # Gui kem de n8n ghi log doi chieu, KHONG de n8n tu di lay du lieu.
        "question_id": ngu_canh.get("question_id"),
        "dap_an_python": ngu_canh.get("dap_an"),
    }


# ======================================================
# 3. HAN MUC LUOT HOI
# ======================================================

def _ngay_hom_nay() -> str:
    return datetime.now(MUI_GIO_VN).date().isoformat()


def lay_luot(user_id: str) -> dict:
    """Tra ve {da_dung, gioi_han, con_lai} cua hom nay."""
    ngay = _ngay_hom_nay()
    da_dung, gioi_han = 0, GIA_SU_LUOT_MOI_NGAY
    try:
        ket_qua = (
            supabase.table("gia_su_luot")
            .select("so_luot, gioi_han")
            .eq("user_id", user_id)
            .eq("ngay", ngay)
            .execute()
        )
        if ket_qua.data:
            dong = ket_qua.data[0]
            da_dung = int(dong.get("so_luot") or 0)
            if dong.get("gioi_han") is not None:
                gioi_han = int(dong["gioi_han"])
    except Exception as e:
        # Chua chay sql/24_gia_su.sql -> khong chan hoc sinh, nhung bao
        # ro rang trong log de biet duong chay SQL.
        print("LOI DOC gia_su_luot (da chay sql/24_gia_su.sql chua?):", e)
    return {"da_dung": da_dung, "gioi_han": gioi_han, "con_lai": max(0, gioi_han - da_dung)}


def tru_luot(user_id: str) -> None:
    """Cong 1 vao so luot da dung hom nay. Goi SAU khi da co cau tra loi
    (hoi thanh cong moi tru) de hoc sinh khong mat luot vi loi mang."""
    ngay = _ngay_hom_nay()
    hien_tai = lay_luot(user_id)
    try:
        supabase.table("gia_su_luot").upsert(
            {
                "user_id": user_id,
                "ngay": ngay,
                "so_luot": hien_tai["da_dung"] + 1,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            on_conflict="user_id,ngay",
        ).execute()
    except Exception as e:
        print("LOI TRU LUOT gia su:", e)


def dat_gioi_han(user_id: str, gioi_han: int) -> bool:
    """Giao vien nang/ha han muc cho 1 em trong ngay hom nay (/gv/gia-su)."""
    try:
        supabase.table("gia_su_luot").upsert(
            {
                "user_id": user_id,
                "ngay": _ngay_hom_nay(),
                "gioi_han": int(gioi_han),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            on_conflict="user_id,ngay",
        ).execute()
        return True
    except Exception as e:
        print("LOI DAT GIOI HAN gia su:", e)
        return False


# ======================================================
# 4. NHAT KI (LOP KHOA 3)
# ======================================================

def ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, tra_loi, trang_thai):
    try:
        supabase.table("gia_su_hoi_dap").insert({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "de_id": de_id,
            "so_thu_tu": so_thu_tu,
            "question_id": (ngu_canh or {}).get("question_id"),
            "muc": "A",
            "cau_hoi": cau_hoi,
            "tra_loi": tra_loi,
            "dap_an_python": (ngu_canh or {}).get("dap_an"),
            "trang_thai": trang_thai,
        }).execute()
    except Exception as e:
        print("LOI GHI NHAT KI gia su:", e)


def lay_nhat_ki(gioi_han: int = 100, user_id: str | None = None) -> list[dict]:
    """Doc nhat ki cho trang /gv/gia-su."""
    try:
        cau_lenh = (
            supabase.table("gia_su_hoi_dap")
            .select("*")
            .order("created_at", desc=True)
            .limit(gioi_han)
        )
        if user_id:
            cau_lenh = cau_lenh.eq("user_id", user_id)
        return cau_lenh.execute().data or []
    except Exception as e:
        print("LOI DOC NHAT KI gia su:", e)
        return []


# ======================================================
# 5. GOI MO HINH
# ======================================================

def _goi_mo_hinh(payload: dict) -> str:
    """Goi webhook n8n. Nem GiaSuError neu loi - KHONG tra loi bia."""
    resp = httpx.post(N8N_WEBHOOK_GIA_SU, json=payload, timeout=60.0)
    resp.raise_for_status()
    try:
        du_lieu = resp.json()
    except Exception:
        return resp.text.strip()
    if isinstance(du_lieu, list) and du_lieu:
        du_lieu = du_lieu[0]
    if isinstance(du_lieu, dict):
        for khoa in ("tra_loi", "output", "text", "message", "answer"):
            if du_lieu.get(khoa):
                return str(du_lieu[khoa]).strip()
    return str(du_lieu).strip()


# ======================================================
# 6. HAM CHINH
# ======================================================

def hoi(user_id: str, de_id: str, so_thu_tu: int, cau_hoi: str,
        lich_su: list[dict] | None = None, lang: str = "vi") -> dict:
    """
    Tra ve dict san de tra thang cho Frontend:
      {tra_loi, dap_an_python, loi_giai_python, che_do, luot, trang_thai}
    `dap_an_python` + `loi_giai_python` LUON co mat (lop khoa 2) - giao
    dien bat buoc phai hien chung canh `tra_loi`.
    """
    cau_hoi = (cau_hoi or "").strip()
    if not cau_hoi:
        raise GiaSuError(_t(lang, "Em chưa nhập câu hỏi.", "You have not typed a question."))
    if len(cau_hoi) > GIA_SU_DO_DAI_CAU_HOI:
        raise GiaSuError(_t(
            lang,
            f"Câu hỏi dài quá (tối đa {GIA_SU_DO_DAI_CAU_HOI} kí tự). "
            "Em hỏi ngắn gọn một ý thôi nhé.",
            f"Your question is too long (at most {GIA_SU_DO_DAI_CAU_HOI} characters). "
            "Please ask one short question at a time."))

    # Lay ngu canh TRUOC khi tru luot: khong du du lieu thi bao loi ngay,
    # hoc sinh khong mat luot.
    ngu_canh = lay_ngu_canh_cau(de_id, so_thu_tu, user_id, lang)

    # PHAI NOP BAI ROI MOI HOI DUOC (co Lan chot 17/09/2026). Chan o
    # TANG SERVER chu khong chi lam mo nut: chan o giao dien thi ai cung
    # goi thang API duoc. Neu khong chan, hoc sinh bam luot ca de de lay
    # loi giai ma khong chiu nghi - vi giang lai luon kem dap an chuan.
    if int(so_thu_tu) not in _cac_cau_da_lam(user_id, de_id):
        raise GiaSuError(_t(
            lang,
            f"Em làm và nộp bài câu {so_thu_tu} trước đã nhé, rồi thầy/cô "
            "giảng lại cho. Tự nghĩ trước thì lúc nghe giảng mới vào đầu.",
            f"Please answer and submit question {so_thu_tu} first, then your teacher will go over it "
            "with you. Thinking it through yourself first makes the explanation stick."))

    luot = lay_luot(user_id)
    if luot["con_lai"] <= 0:
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "het_luot")
        raise GiaSuError(_t(
            lang,
            f"Hôm nay em đã dùng hết {luot['gioi_han']} lượt hỏi rồi. "
            "Em đọc lại lời giải mẫu bên dưới, mai có lượt mới nhé.",
            f"You have used all {luot['gioi_han']} questions for today. "
            "Read the model solution below; you get new ones tomorrow."))

    # --- Che do khong AI: chua cau hinh webhook -> van tra loi giai chuan ---
    if not N8N_WEBHOOK_GIA_SU:
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "chua_cau_hinh")
        return {
            "tra_loi": None,
            "che_do": "khong_ai",
            "de_bai_python": ngu_canh["de_bai"],
            "dap_an_python": ngu_canh["dap_an"],
            "loi_giai_python": ngu_canh["loi_giai"],
            "luot": luot,
            "trang_thai": "chua_cau_hinh",
        }

    payload = dung_lenh(ngu_canh, cau_hoi, lich_su, lang)
    try:
        tra_loi = _goi_mo_hinh(payload)
    except httpx.HTTPError as e:
        print("LOI GOI WEBHOOK gia su:", e)
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "loi")
        raise GiaSuError(_t(
            lang,
            "Thầy/cô AI đang bận, em đọc tạm lời giải mẫu bên dưới rồi thử lại sau nhé.",
            "The AI teacher is busy. Read the model solution below and try again later."))

    if not tra_loi:
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "loi")
        raise GiaSuError(_t(lang, "Chưa nhận được câu trả lời, em thử lại giúp thầy/cô nhé.",
                            "No answer was received. Please try again."))

    tru_luot(user_id)
    trang_thai = "ngoai_pham_vi" if (CAU_TU_CHOI[:30] in tra_loi or CAU_TU_CHOI_EN[:30] in tra_loi) else "ok"
    ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, tra_loi, trang_thai)

    return {
        "tra_loi": tra_loi,
        "che_do": "ai",
        "de_bai_python": ngu_canh["de_bai"],
        "dap_an_python": ngu_canh["dap_an"],
        "loi_giai_python": ngu_canh["loi_giai"],
        "luot": lay_luot(user_id),
        "trang_thai": trang_thai,
    }


# ======================================================
# 7. TU KIEM TRA KET NOI n8n (them 24/09/2026)
# ======================================================
# Vi sao can: co Lan mat nhieu ngay vi mot loi KHONG NHIN THAY DUOC -
# node CHV_GiaSu khong nap lenh_he_thong, nen mo hinh khong co de bai va
# TU BIA ra ngu canh (tam li hoc, marketing, phan phoi ngan sach...).
# Nhin tu ngoai thi "AI tra loi lung tung", khong biet hong o dau.
#
# Ham nay tra lai cau hoi do bang MOT phep thu: gui mot cau lenh chua
# MA NGAU NHIEN va bao mo hinh doc lai ma do. Ma quay ve = lenh_he_thong
# CO toi mo hinh. Khong quay ve = KHONG toi. Khong can doc Executions,
# khong can hieu n8n.

MA_KIEM_TRA_DAI = 6

LENH_KIEM_TRA = """Đây là một phép thử kết nối, không phải câu hỏi của học sinh.
Hãy trả lời DUY NHẤT bằng mã sau, không thêm bất kì chữ nào khác:

{ma}
"""


def tu_kiem_tra() -> dict:
    """
    Tra ve {ket_luan, chi_tiet, ma_gui, tra_loi} - ket_luan la mot trong:
      chua_cau_hinh | khong_goi_duoc | khong_nap_lenh | ok
    Khong tru luot cua ai, khong ghi nhat ki hoc sinh.
    """
    if not N8N_WEBHOOK_GIA_SU:
        return {
            "ket_luan": "chua_cau_hinh",
            "chi_tiet": ("Chưa đặt N8N_WEBHOOK_GIA_SU trong tệp .env trên máy chủ. "
                         "Gia sư đang chạy ở chế độ không AI (chỉ hiện lời giải chuẩn)."),
            "ma_gui": None, "tra_loi": None,
        }

    ma = uuid.uuid4().hex[:MA_KIEM_TRA_DAI].upper()
    payload = {
        "muc": "kiem_tra",
        "lenh_he_thong": LENH_KIEM_TRA.format(ma=ma),
        "cau_hoi": "Đọc lại mã trong phần hướng dẫn hệ thống.",
        "lich_su": [],
        "question_id": None,
        "dap_an_python": None,
    }

    try:
        tra_loi = _goi_mo_hinh(payload)
    except httpx.HTTPError as e:
        return {
            "ket_luan": "khong_goi_duoc",
            "chi_tiet": (f"Không gọi được webhook n8n: {e}. Kiểm tra URL trong .env, "
                         "và workflow đã bấm Save/Active chưa."),
            "ma_gui": ma, "tra_loi": None,
        }

    if ma in (tra_loi or ""):
        return {
            "ket_luan": "ok",
            "chi_tiet": ("Tốt. Câu lệnh hệ thống ĐÃ tới mô hình — mã kiểm tra quay về "
                         "nguyên vẹn. Gia sư AI hoạt động đúng."),
            "ma_gui": ma, "tra_loi": tra_loi,
        }

    return {
        "ket_luan": "khong_nap_lenh",
        "chi_tiet": (
            "Webhook gọi được, nhưng câu lệnh hệ thống KHÔNG tới mô hình: mã kiểm tra "
            "không quay về. Vào n8n, node CHV_GiaSu, ô System Message phải ở chế độ "
            "Expression và bằng đúng: {{ $json.body.lenh_he_thong }} — đây chính là "
            "nguyên nhân AI trả lời lạc đề."
        ),
        "ma_gui": ma, "tra_loi": tra_loi,
    }
