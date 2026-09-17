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
import json
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

# Gio Viet Nam - dung de chot "ngay" cho han muc luot hoi. Neu dung UTC
# thi tu 7h sang den 0h (gio VN) bi tinh sang ngay hom sau, hoc sinh mat
# luot giua buoi hoc.
MUI_GIO_VN = timezone(timedelta(hours=7))

CAU_TU_CHOI = (
    "Câu này nằm ngoài phần thầy/cô đã chuẩn bị nên em hỏi trực tiếp "
    "thầy/cô nhé. Ở đây thầy/cô chỉ giảng lại đúng các câu trong đề em vừa làm."
)


class GiaSuError(Exception):
    """Loi co the hien thang cho hoc sinh doc (da viet bang tieng Viet)."""


# ======================================================
# 1. NGU CANH: de bai + dap an + loi giai CHUAN (do Python sinh)
# ======================================================

def _doc_dapan_json(de: dict) -> list[dict] | None:
    duong_dan = (de.get("files") or {}).get("dapan_json")
    if not duong_dan:
        return None
    tep = Path(duong_dan)
    if not tep.exists():
        return None
    try:
        return json.loads(tep.read_text(encoding="utf-8"))
    except Exception as e:
        print("LOI DOC dapan_json cho gia su:", e)
        return None


def _mo_ta_dap_an(cau: dict) -> str:
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
                f"{y}) {'Đúng' if gt else 'Sai'}" for y, gt in sorted(dap_an.items())
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


def lay_ngu_canh_cau(de_id: str, so_thu_tu: int, user_id: str | None = None) -> dict:
    """
    Tra ve {de_bai, dap_an, loi_giai, question_id, loai_cau, chuong, bai,
    nguon}. Nem GiaSuError neu khong du du lieu - KHONG BAO GIO tra ve
    ngu canh rong roi van goi mo hinh.
    """
    de = history_service.lay_de_theo_id(de_id)
    if de is None:
        raise GiaSuError("Không tìm thấy đề này. Em thử tạo đề mới rồi hỏi lại nhé.")

    # --- Nguon 1: file dap an goc do Python sinh ---
    danh_sach = _doc_dapan_json(de)
    if danh_sach:
        for cau in danh_sach:
            if int(cau.get("so_thu_tu") or 0) != int(so_thu_tu):
                continue
            loi_giai = str(cau.get("loi_giai") or "").strip()
            if not loi_giai:
                raise GiaSuError(
                    f"Câu {so_thu_tu} chưa có lời giải mẫu trong ngân hàng nên "
                    "chưa giảng lại được. Em hỏi trực tiếp thầy/cô nhé."
                )
            return {
                "de_bai": _mo_ta_de_bai(cau),
                "dap_an": _mo_ta_dap_an(cau),
                "loi_giai": loi_giai,
                "question_id": cau.get("generator_id") or cau.get("question_id"),
                "loai_cau": cau.get("loai_cau"),
                "chuong": cau.get("chuong"),
                "bai": cau.get("bai"),
                "nguon": "dapan_json",
            }
        raise GiaSuError(f"Đề này không có câu {so_thu_tu}.")

    # --- Nguon 2: lich su cham bai (khi file dapan_json da bi don dep) ---
    if user_id:
        cau = _tim_trong_lich_su(user_id, de_id, so_thu_tu)
        if cau:
            return cau

    raise GiaSuError(
        "Dữ liệu chi tiết của đề này đã được dọn dẹp (đề cũ hơn 1 ngày) nên "
        "chưa giảng lại được. Em tạo đề mới cùng dạng rồi hỏi lại nhé."
    )


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
            "dap_an": str(cau.get("dap_an_dung") or ""),
            "loi_giai": loi_giai,
            "question_id": cau.get("question_id"),
            "loai_cau": cau.get("loai_cau"),
            "chuong": cau.get("chuong"),
            "bai": cau.get("bai"),
            "nguon": "exam_history",
        }
    return None


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


def liet_ke_cau_de_gan_nhat(user_id: str, conversation_id: str) -> dict:
    """
    Tra ve de gan nhat trong 1 cuoc hoi thoai, chia thanh 4 phan, moi cau
    kem co hoi duoc hay khong.
      {de_id, tieu_de, da_lam_bai, cac_phan: [{ma, ten, cau: [...]}]}
    Nem GiaSuError neu chua co de / du lieu da bi don dep.
    """
    de = history_service.lay_de_gan_nhat(conversation_id)
    if de is None:
        raise GiaSuError(
            "Cuộc trò chuyện này chưa có đề nào. Em tạo một đề rồi quay lại nhé."
        )

    danh_sach = _doc_dapan_json(de)
    if not danh_sach:
        raise GiaSuError(
            "Dữ liệu chi tiết của đề này đã được dọn dẹp (đề cũ hơn 1 ngày) nên "
            "chưa hỏi lại được. Em tạo đề mới cùng dạng nhé."
        )

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
        cac_phan.append({
            "ma": ma,
            "ten": TEN_PHAN[ma],
            "cau": sorted(theo_phan[ma], key=lambda c: c["so_thu_tu"]),
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

LENH_KHI_MAT_DE_BAI = (
    "(Không còn lưu đề bài gốc. TUYỆT ĐỐI không đoán lại đề bài; chỉ giảng "
    "lại các bước trong lời giải mẫu.)"
)


def dung_lenh(ngu_canh: dict, cau_hoi: str, lich_su: list[dict] | None = None) -> dict:
    """Dung payload gui sang n8n. Tach rieng ra 1 ham de test duoc ma
    khong can mang, va de doc lai duoc chinh xac cai gi da gui di."""
    de_bai = ngu_canh.get("de_bai") or LENH_KHI_MAT_DE_BAI
    he_thong = LENH_HE_THONG.format(
        cau_tu_choi=CAU_TU_CHOI,
        de_bai=de_bai,
        dap_an=ngu_canh.get("dap_an") or "(không có)",
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
        lich_su: list[dict] | None = None) -> dict:
    """
    Tra ve dict san de tra thang cho Frontend:
      {tra_loi, dap_an_python, loi_giai_python, che_do, luot, trang_thai}
    `dap_an_python` + `loi_giai_python` LUON co mat (lop khoa 2) - giao
    dien bat buoc phai hien chung canh `tra_loi`.
    """
    cau_hoi = (cau_hoi or "").strip()
    if not cau_hoi:
        raise GiaSuError("Em chưa nhập câu hỏi.")
    if len(cau_hoi) > GIA_SU_DO_DAI_CAU_HOI:
        raise GiaSuError(
            f"Câu hỏi dài quá (tối đa {GIA_SU_DO_DAI_CAU_HOI} kí tự). "
            "Em hỏi ngắn gọn một ý thôi nhé."
        )

    # Lay ngu canh TRUOC khi tru luot: khong du du lieu thi bao loi ngay,
    # hoc sinh khong mat luot.
    ngu_canh = lay_ngu_canh_cau(de_id, so_thu_tu, user_id)

    # PHAI NOP BAI ROI MOI HOI DUOC (co Lan chot 17/09/2026). Chan o
    # TANG SERVER chu khong chi lam mo nut: chan o giao dien thi ai cung
    # goi thang API duoc. Neu khong chan, hoc sinh bam luot ca de de lay
    # loi giai ma khong chiu nghi - vi giang lai luon kem dap an chuan.
    if int(so_thu_tu) not in _cac_cau_da_lam(user_id, de_id):
        raise GiaSuError(
            f"Em làm và nộp bài câu {so_thu_tu} trước đã nhé, rồi thầy/cô "
            "giảng lại cho. Tự nghĩ trước thì lúc nghe giảng mới vào đầu."
        )

    luot = lay_luot(user_id)
    if luot["con_lai"] <= 0:
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "het_luot")
        raise GiaSuError(
            f"Hôm nay em đã dùng hết {luot['gioi_han']} lượt hỏi rồi. "
            "Em đọc lại lời giải mẫu bên dưới, mai có lượt mới nhé."
        )

    # --- Che do khong AI: chua cau hinh webhook -> van tra loi giai chuan ---
    if not N8N_WEBHOOK_GIA_SU:
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "chua_cau_hinh")
        return {
            "tra_loi": None,
            "che_do": "khong_ai",
            "dap_an_python": ngu_canh["dap_an"],
            "loi_giai_python": ngu_canh["loi_giai"],
            "luot": luot,
            "trang_thai": "chua_cau_hinh",
        }

    payload = dung_lenh(ngu_canh, cau_hoi, lich_su)
    try:
        tra_loi = _goi_mo_hinh(payload)
    except httpx.HTTPError as e:
        print("LOI GOI WEBHOOK gia su:", e)
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "loi")
        raise GiaSuError(
            "Thầy/cô AI đang bận, em đọc tạm lời giải mẫu bên dưới rồi thử lại sau nhé."
        )

    if not tra_loi:
        ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, None, "loi")
        raise GiaSuError("Chưa nhận được câu trả lời, em thử lại giúp thầy/cô nhé.")

    tru_luot(user_id)
    trang_thai = "ngoai_pham_vi" if CAU_TU_CHOI[:30] in tra_loi else "ok"
    ghi_nhat_ki(user_id, de_id, so_thu_tu, ngu_canh, cau_hoi, tra_loi, trang_thai)

    return {
        "tra_loi": tra_loi,
        "che_do": "ai",
        "dap_an_python": ngu_canh["dap_an"],
        "loi_giai_python": ngu_canh["loi_giai"],
        "luot": lay_luot(user_id),
        "trang_thai": trang_thai,
    }
