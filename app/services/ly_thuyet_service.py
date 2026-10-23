"""
GIA SU AI - MUC B: lay DUNG CHO trong tai lieu li thuyet cua co Lan (data/ly_thuyet/*.tex) de thay/co AI giai thich
khai niem, dinh nghia, ki hieu, cong thuc ma loi giai mau khong noi toi (docs/23_GIA_SU_AI.md muc 8, 8d).

Vi sao co (co Lan 22/10/2026): hoc sinh hoi tiep "tap rong la tap gi" o cau giai phuong trinh chua can (phuong an
A la S = rong) thi bi tu choi "nam ngoai phan thay/co da chuan bi", vi Muc A chi cho AI dung de bai + dap an + loi
giai mau. Khai niem do CO trong tai lieu cua co (0D1-CD2.tex: "Tap rong: la tap hop khong chua phan tu nao...").

Nguyen tac "khong ra ngoai bat ki cai nao" van giu: AI chi duoc dung THEM dung doan tai lieu cua co lay o day, khong
dung kien thuc rieng cua no. Khong goi them mo hinh nao, khong vecto: tra bang anh_xa.json + dem tu khoa.

Cach lay:
  1. Moi tep .tex: cat dung muc li thuyet (\\subsection TOM TAT LY THUYET / LY THUYET CAN NHO / KIEN THUC CAN NHO,
     den \\subsection ke tiep), bo hinh TikZ va lenh trinh bay, chia theo \\subsubsection thanh cac "khoi" dong.
  2. Tim theo tu khoa cua cau hoc sinh hoi trong cac bai cung lop thuoc CAC CHUONG DA HOC (chuong 1 den chuong cua
     cau dang hoi - khai niem nhu tap rong o chuong 1 dung o moi chuong sau; chuong chua hoc thi khong lay), uu
     tien bai cua chinh cau dang hoi. Cum hai tu ("tap rong") nang diem hon tu don; tu nao cang hiem cang nang diem.
  3. Tra ve toi da vai doan ngan (dong trung + vai dong quanh), kem ten bai / ten muc de chi cho hoc sinh hoc lai.
  4. Khong trung tu khoa nao ma hoc sinh dang hoi TIEP (da nghe giang roi van chua hieu): tra muc li thuyet cua
     chinh bai do (cat ngan).
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

THU_MUC = Path(__file__).resolve().parents[2] / "data" / "ly_thuyet"
TEP_ANH_XA = THU_MUC / "anh_xa.json"

# Ten muc li thuyet trong cac tep cua co (da dem tren 28 tep lop 10: 18 "TOM TAT", 10 "LY THUYET CAN NHO").
_MUC_LY_THUYET = re.compile(r"\\subsection\*?\s*\{\s*(T[ÓO]M T[ẮA]T L[ÝY] THUY[ẾE]T|L[ÝY] THUY[ẾE]T C[ẦA]N NH[ỚO]"
                            r"|KI[ẾE]N TH[ỨU]C C[ẦA]N NH[ỚO])\s*\}", re.IGNORECASE)
_SUBSECTION = re.compile(r"\\subsection\*?\s*\{")
_SUBSUB = re.compile(r"\\subsubsection\*?\s*\{")


def _nhom_ngoac(s: str, mo: int) -> int:
    """Vi tri NGAY SAU dau } dong cua nhom { bat dau tai s[mo] (dem ngoac long nhau, vd ten muc co $\\sqrt{...}$).
    \\{ \\} (dau ngoac in ra) khong tinh; "\\\\}" (xuong dong roi dong ngoac) thi van tinh."""
    sau = 0
    for i in range(mo, len(s)):
        if s[i] not in "{}":
            continue
        k = i - 1
        while k >= 0 and s[k] == "\\":
            k -= 1
        if (i - 1 - k) % 2:                       # so dau \ le ngay truoc -> ngoac bi thoat
            continue
        sau += 1 if s[i] == "{" else -1
        if sau == 0:
            return i + 1
    return len(s)


TOI_DA_DOAN = 3          # so doan toi da dua vao lenh
TOI_DA_KY_TU = 2600      # tong do dai cac doan (khoang 700 token)
TOI_DA_KY_TU_CA_MUC = 3500
DIEM_TOI_THIEU = 3.0     # duoi nguong nay coi nhu khong trung (chi trung tu pho bien nhu "tap", "ham")

# Tu hay gap trong cau hoi, khong mang noi dung toan hoc.
_TU_DUNG = set("""
là gì sao tại vì thế nào em anh chị mình tôi tớ chưa hiểu cho của có không ko được này đó ở và thì mà với bước
câu làm ra như vậy nhỉ ạ à hả hỏi giải thích lại một các những khi nếu ta bằng nên cái chỗ phần đây kia sự theo
trong từ đến để về hay hoặc sẽ đã đang rồi nữa thầy cô thêm giúp nói rõ cách tính ý nghĩa nghĩa tại
bao nhiêu mấy kiểu chi vẫn còn đâu luôn ơi nha nhé đi xem biết dùng phải cần muốn thấy hiểu giảng lời đề bài
vừa phần i ii iii iv
what is the a an of why how does do mean meaning in to and or this that it please explain part question
""".split())


def _bo_dau(s: str) -> str:
    """Chu thuong NFC + gop cach viet khac nhau cua cung mot tu (tai lieu viet "véc-tơ", hoc sinh go "vectơ";
    "định lí" / "định lý", "kí hiệu" / "ký hiệu")."""
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"v[eé]c[\s-]?t[oơ]", "vectơ", s)
    return re.sub(r"(?<![0-9a-zà-ỹđ])(l|k|m|t|s|h|qu)ý(?![0-9a-zà-ỹđ])", r"\1í", s)


def _tu(van_ban: str) -> list[str]:
    """Tach am tiet (chu thuong, giu dau tieng Viet). Ki hieu LaTeX trong cau hoi (\\varnothing...) giu thanh tu."""
    van_ban = _bo_dau(van_ban)
    return re.findall(r"\\[a-z]+|[0-9a-zà-ỹđ]+", van_ban)


# Thuat ngu co mot am tiet nam trong _TU_DUNG ("đề" vi "đề bài", "cách" vi "cách tính"...): giu nguyen cum, neu khong
# "mệnh đề là gì" chi con "mệnh" (gap khap tai lieu, diem thap) -> bao nham "chua co trong tai lieu" (co Lan 23/10/2026).
_CUM_GIU = {"mệnh đề", "khoảng cách", "tính chất", "phần tử", "phần bù", "bằng nhau", "chủ đề", "giải tích"}


def _cac_cum(van_ban: str) -> list[str]:
    """Tu don co nghia + cum hai tu lien nhau (ca hai deu co nghia, hoac la thuat ngu trong _CUM_GIU) cua cau hoi."""
    tu = _tu(van_ban)
    don = [t for t in tu if t not in _TU_DUNG and len(t) > 1]
    cum = [a + " " + b for a, b in zip(tu, tu[1:])
           if (a not in _TU_DUNG and b not in _TU_DUNG) or (a + " " + b) in _CUM_GIU]
    return list(dict.fromkeys(cum + don))


# ------------------------------------------------------------------ lam sach LaTeX cua tai lieu

_MOI_TRUONG_TOAN = {
    "align", "align*", "aligned", "alignat", "alignat*", "array", "cases", "matrix", "pmatrix", "bmatrix",
    "vmatrix", "split", "equation", "equation*", "gather", "gather*", "eqnarray", "eqnarray*",
}


def _bo_khoi(van_ban: str, ten: str) -> str:
    return re.sub(r"\\begin\{%s\}.*?\\end\{%s\}" % (re.escape(ten), re.escape(ten)), " ", van_ban, flags=re.S)


_TOAN = re.compile(r"(\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\]"
                   r"|\\begin\{(?:%s)\}.*?\\end\{(?:%s)\})" % ("|".join(map(re.escape, sorted(_MOI_TRUONG_TOAN))),
                                                          "|".join(map(re.escape, sorted(_MOI_TRUONG_TOAN)))), re.S)


def _thay_lenh_mot_doi_so(s: str, ten: str, truoc: str, sau: str) -> str:
    """\\ten{X} -> truoc + X + sau (X co the chua ngoac long nhau)."""
    while True:
        m = re.search(r"\\%s\s*\{" % ten, s)
        if not m:
            return s
        het = _nhom_ngoac(s, m.end() - 1)
        s = s[:m.start()] + truoc + s[m.end():het - 1] + sau + s[het:]


def lam_sach(van_ban: str) -> str:
    """LaTeX trinh bay cua tai lieu -> chu doc duoc (cho cau lenh AI va hien tren web bang MathJax). Giu nguyen cong
    thuc; bo hinh TikZ, khung, co chu, khoang cach; doi lenh rieng cua co (\\heva, \\hoac, \\R) ve lenh MathJax hieu."""
    s = re.sub(r"(?<!\\)%.*", "", van_ban)                          # chu thich
    for ten in ("tikzpicture", "figure", "center", "minipage"):
        s = _bo_khoi(s, ten)
    s = _thay_lenh_mot_doi_so(s, "heva", "\\begin{cases}", "\\end{cases}")
    s = _thay_lenh_mot_doi_so(s, "hoac", "\\left[\\begin{aligned}", "\\end{aligned}\\right.")
    s = re.sub(r"\\R\b", r"\\mathbb{R}", s)
    s = re.sub(r"(\\lq)+", "“", s)
    s = re.sub(r"(\\rq)+", "”", s)
    s = re.sub(r"\\(hspace|vspace)\*?\s*\{[^}]*\}", " ", s)
    s = re.sub(r"\\fontsize\{[^}]*\}\{[^}]*\}|\\color\{[^}]*\}", " ", s)
    s = re.sub(r"\\item\s*\[[^\]]*\]", "\n• ", s)                   # \item [\ding{172}]
    s = re.sub(r"\\item\b", "\n• ", s)

    def _moi_truong(m):
        return m.group(0) if m.group(2) in _MOI_TRUONG_TOAN else "\n"
    s = re.sub(r"\\(begin|end)\s*\{([a-zA-Z0-9*]+)\}(\[[^\]]*\])?(\{[^}]*\})?", _moi_truong, s)
    s = re.sub(r"\\(indam\w*|textbf|textit|emph|underline|boxmini|fbox|centerline|text(?:sf|rm))\s*\{", "{", s)
    s = re.sub(r"\\(immini|icon[A-Z]+|faPencilSquareO|noindent|hfill|newline|newpage|centering|ding\{\d+\}|par"
               r"|medskip|smallskip|bigskip|footnotesize|scriptsize|small|selectfont|sf|rm|bf|hline|quad|qquad)\b", " ", s)
    # Bo { } con sot NGOAI cong thuc; trong cong thuc giu nguyen va noi lai thanh MOT dong (cat doan khong lam vo $...$).
    phan = _TOAN.split(s)
    s = "".join((p.replace("\n", " ") if i % 2 else p.replace("{", "").replace("}", "")) for i, p in enumerate(phan))
    dong = []
    for d in s.split("\n"):
        d = re.sub(r"[ \t]+", " ", d).strip()
        d = re.sub(r"\s*\\\\$", "", d).strip()                       # \\ cuoi dong
        if d and d not in ("•", "\\\\", "&"):
            dong.append(d)
    return "\n".join(dong)


# ------------------------------------------------------------------ doc tai lieu

@lru_cache(maxsize=1)
def _anh_xa() -> dict:
    try:
        return json.loads(TEP_ANH_XA.read_text(encoding="utf-8")).get("anh_xa") or {}
    except Exception as e:                                           # thieu tep: Muc B tat, Muc A van chay
        print("LOI DOC anh_xa ly thuyet:", e)
        return {}


@lru_cache(maxsize=128)
def cac_khoi_cua_tep(ten_tep: str) -> tuple:
    """((ten_muc, (dong, ...)), ...) - muc li thuyet cua 1 tep, chia theo \\subsubsection. Khong co muc -> ()."""
    tep = THU_MUC / ten_tep
    if not tep.exists():
        return ()
    goc = tep.read_text(encoding="utf-8", errors="ignore")
    m = _MUC_LY_THUYET.search(goc)
    if not m:
        return ()
    con = goc[m.end():]
    ket = _SUBSECTION.search(con)
    muc = con[:ket.start()] if ket else con
    tieu_de = re.search(r"\\section\*?\s*\{", goc)
    ten_chung = (goc[tieu_de.end():_nhom_ngoac(goc, tieu_de.end() - 1) - 1].strip().capitalize() if tieu_de else "")
    khoi = []
    vi_tri = []
    for mm in _SUBSUB.finditer(muc):
        het = _nhom_ngoac(muc, mm.end() - 1)
        vi_tri.append((mm.start(), het, muc[mm.end():het - 1].strip()))
    if not vi_tri or vi_tri[0][0] > 0:
        dau = muc[:vi_tri[0][0]] if vi_tri else muc
        khoi.append((ten_chung, dau))
    for i, (_bd, kt, ten) in enumerate(vi_tri):
        cuoi = vi_tri[i + 1][0] if i + 1 < len(vi_tri) else len(muc)
        khoi.append((ten, muc[kt:cuoi]))
    return tuple((ten, tuple(lam_sach(noi).split("\n"))) for ten, noi in khoi if lam_sach(noi).strip())


def _so_chuong(ma: str | None) -> int:
    """Số chương trong mã bài / ID câu ("L10_C6_B18..." -> 6). Không đọc được -> 0 (không tìm gì)."""
    m = re.match(r"^L\d+_C(\d+)", ma or "")
    return int(m.group(1)) if m else 0


def _bai_cua_cau(question_id: str | None) -> tuple[str | None, list[str]]:
    """(lop "L10", [ma bai cua cau]) tu ID cau. Cau ra theo chuong (TF, ID khong co _B) -> moi bai cua chuong."""
    m = re.match(r"^(L\d+)_C(\d+)(?:_B(\d+))?", question_id or "")
    if not m:
        return None, []
    lop, chuong, bai = m.group(1), m.group(2), m.group(3)
    if bai:
        return lop, [f"{lop}_C{chuong}_B{bai}"]
    return lop, [k for k in _anh_xa() if k.startswith(f"{lop}_C{chuong}_B")]


@lru_cache(maxsize=8)
def _kho_dong(lop: str) -> tuple:
    """Moi dong li thuyet cua 1 lop: (ma_bai, ten_bai, tep, ten_muc, chi_so_khoi, chi_so_dong). Tep dung cho nhieu bai
    (vd 0H4-B2.tex cho B8, B9, B11) chi doc 1 lan, gan cho bai DAU TIEN."""
    da_doc, kho = set(), []
    for ma, bai in _anh_xa().items():
        if not ma.startswith(lop + "_"):
            continue
        for tep in bai.get("tep") or []:
            if tep in da_doc:
                continue
            da_doc.add(tep)
            for i, (ten_muc, dong) in enumerate(cac_khoi_cua_tep(tep)):
                for j in range(len(dong)):
                    kho.append((ma, bai.get("ten_bai") or "", tep, ten_muc, i, j))
    return tuple(kho)


def _dong(muc) -> str:
    _ma, _ten, tep, _m, i, j = muc
    return cac_khoi_cua_tep(tep)[i][1][j]


def _trung(cum: str, dong_thuong: str) -> bool:
    if cum.startswith("\\"):
        return cum in dong_thuong
    return re.search(r"(?<![0-9a-zà-ỹđ])%s(?![0-9a-zà-ỹđ])" % re.escape(cum), dong_thuong) is not None


def _doan_quanh(muc, truoc: int = 1, sau: int = 3) -> tuple[int, int]:
    _ma, _ten, tep, _m, i, j = muc
    n = len(cac_khoi_cua_tep(tep)[i][1])
    return max(0, j - truoc), min(n, j + sau + 1)


def tim_doan(question_id: str | None, cau_hoi: str, dang_hoi_tiep: bool = False) -> list[dict]:
    """Cac doan tai lieu li thuyet cua co lien quan toi cau hoi:
       [{"ma_bai", "ten_bai", "tep", "muc", "noi_dung"}]. Khong co gi -> [].

    Diem moi dong = tong trong so (idf) cac cum cua cau hoi co trong dong (ten muc tinh nua diem). Dong o BAI KHAC
    chi duoc lay khi trung CUM HAI TU / ki hieu (vd "tap rong", "dinh ly sin") - trung mot tu le ("tap", "thu") thi
    de lac sang "to hop", "phep thu". Chi giu cac dong dat it nhat nua diem dong cao nhat."""
    lop, bai_cua_cau = _bai_cua_cau(question_id)
    if not lop:
        return []
    # Cô Lan 22/10/2026: hỏi "tập rỗng" ở câu Chương 6 thì kéo cả đoạn "Tổ hợp" (Chương 8, chưa học). Chỉ tìm trong
    # các chương ĐÃ HỌC: Chương 1 đến chương của câu đang hỏi (chương đánh số theo PPCT nên nhỏ hơn là đã học).
    chuong = _so_chuong(question_id)
    kho = tuple(m for m in _kho_dong(lop) if _so_chuong(m[0]) <= chuong)
    ket_qua = _tim_trong_kho(kho, bai_cua_cau, cau_hoi)
    if not ket_qua and dang_hoi_tiep:
        ket_qua = ca_muc_cua_bai(bai_cua_cau[:1])
    return ket_qua


def tim_doan_tu_do(lop: int | None, cau_hoi: str) -> list[dict]:
    """Câu hỏi KIẾN THỨC gõ thẳng trong khung chat, không gắn với câu nào của đề (cô Lan 23/10/2026: "nếu hỏi về kiến
    thức toán thì AI có thể đọc ngay phần lý thuyết có sẵn để trả lời, chỉ trả lời trong đó"). Tìm trong mọi bài của
    lớp (theo hồ sơ; không có thì lớp 10); mọi bài ngang nhau nên trùng một từ hiếm ("tan", "trung vị") cũng lấy."""
    lop_ma = "L%d" % (lop if lop in (10, 11, 12) else 10)
    return _tim_trong_kho(_kho_dong(lop_ma), [], cau_hoi, tu_do=True)


def _thu_tu_bai(ma_bai: str) -> tuple:
    m = re.match(r"L\d+_C(\d+)_B(\d+)", ma_bai or "")
    return (int(m.group(1)), int(m.group(2))) if m else (99, 99)


def _tim_trong_kho(kho: tuple, bai_cua_cau: list, cau_hoi: str, tu_do: bool = False) -> list[dict]:
    cum = _cac_cum(cau_hoi or "")
    ket_qua: list[dict] = []
    if kho and cum:
        than = [_bo_dau(_dong(m)) for m in kho]
        tieu = [_bo_dau(m[3]) for m in kho]
        n = len(kho)
        trong_so = {}
        for c in cum:
            df = sum(1 for a, b in zip(than, tieu) if _trung(c, a) or _trung(c, b))
            if df:
                trong_so[c] = math.log(1 + n / df) * (2.0 if (" " in c or c.startswith("\\")) else 1.0)
        diem = []
        for k in range(n):
            o_than = [c for c in trong_so if _trung(c, than[k])]
            o_tieu = [c for c in trong_so if c not in o_than and _trung(c, tieu[k])]
            s = sum(trong_so[c] for c in o_than) + 0.5 * sum(trong_so[c] for c in o_tieu)
            if not s:
                continue
            cung_bai = kho[k][0] in bai_cua_cau
            if not tu_do and not cung_bai and not any(" " in c or c.startswith("\\") for c in o_than + o_tieu):
                continue
            if cung_bai:
                s *= 1.5                                              # uu tien bai cua chinh cau dang hoi
            if tu_do and any(" " in c for c in trong_so if _trung(c, tieu[k])):
                s *= 1.5                                              # ten muc chua dung thuat ngu duoc hoi
            if s >= DIEM_TOI_THIEU:
                diem.append((s, k))
        diem.sort(key=lambda x: (-x[0], _thu_tu_bai(kho[x[1]][0]), x[1]))
        if diem:
            nguong = diem[0][0] * 0.5
            diem = [x for x in diem if x[0] >= nguong]
            if tu_do:
                # Hoi kien thuc tu do: chi lay MOT bai - bai co diem cao nhat (bang diem thi bai hoc truoc, noi khai
                # niem duoc dinh nghia). Co Lan 23/10/2026: "dang giai thich ve tap rong, tai sao lai loi kien thuc
                # to hop vao" (bai To hop co cau "to hop chap 0 la tap rong" nen trung diem voi bai Tap hop).
                bai_dau = kho[diem[0][1]][0]
                diem = [x for x in diem if kho[x[1]][0] == bai_dau]
        da_lay, tong = [], 0
        for _s, k in diem:
            m = kho[k]
            bd, kt = _doan_quanh(m)
            khoa = (m[2], m[4])
            if any(k2 == khoa and not (kt <= b2 or bd >= k3) for k2, b2, k3 in da_lay):
                continue                                              # trung doan da lay
            noi = "\n".join(cac_khoi_cua_tep(m[2])[m[4]][1][bd:kt])
            if tong + len(noi) > TOI_DA_KY_TU and ket_qua:
                break
            da_lay.append((khoa, bd, kt))
            tong += len(noi)
            ket_qua.append({"ma_bai": m[0], "ten_bai": m[1], "tep": m[2], "muc": m[3], "noi_dung": noi})
            if len(ket_qua) >= TOI_DA_DOAN:
                break
    return ket_qua


def ca_muc_cua_bai(cac_bai: list[str]) -> list[dict]:
    """Muc li thuyet cua bai (cat ngan theo tung khoi, toi da TOI_DA_KY_TU_CA_MUC ki tu)."""
    ket, tong = [], 0
    for ma in cac_bai:
        bai = _anh_xa().get(ma) or {}
        for tep in bai.get("tep") or []:
            for ten_muc, dong in cac_khoi_cua_tep(tep):
                noi = "\n".join(dong)
                if tong + len(noi) > TOI_DA_KY_TU_CA_MUC:
                    return ket
                tong += len(noi)
                ket.append({"ma_bai": ma, "ten_bai": bai.get("ten_bai") or "", "tep": tep, "muc": ten_muc,
                            "noi_dung": noi})
    return ket


def thanh_van_ban_lenh(doan: list[dict]) -> str:
    """Ghep cac doan thanh mot khoi chu de dua vao cau lenh he thong."""
    return "\n\n".join("[Bài: %s — mục: %s]\n%s" % (d["ten_bai"], d["muc"], d["noi_dung"]) for d in doan)
