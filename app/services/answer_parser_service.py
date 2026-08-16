r"""
CN_GradeAnswer (buoc chuan bi) — trich dap an tu latex_block co san,
KHONG can sua tung ham sinh cau trong ngan hang de (data/python_bank).

Dua vao cac macro dung chung do math_type.py tao ra (MC_SA_answer_text /
MC_SA_answer_const):
- \choice{...}{...}{...}{...} : cau trac nghiem 4 phuong an. Dap an dung
  duoc danh dau bang \True ngay dau noi dung, TRUOC khi 4 phuong an bi
  xao tron thu tu (random.shuffle) — nen \True luon di theo dung dap an
  bat ke no roi vao vi tri A/B/C/D nao.
- \shortans{...} hoac \shortans[N]{...} : cau tra loi ngan. Noi dung ben
  trong DA la dap an thuan (math_type.py da tu .replace("\True","") truoc
  khi ghep vao \shortans, xem MC_SA_answer_text).
- \loigiai{...} : loi giai chi tiet — dung lam ngu canh cham cau tu luan
  (CHV_Grader) va hien thi lai cho hoc sinh sau khi cham.
- \choiceTFn[N] hoac \choiceTFt, theo sau la 4 khoi {...} (a/b/c/d) : cau
  Dung/Sai. Moi khoi la 1 menh de doc lap, dung/sai rieng biet, danh dau
  bang \True o dau noi dung y HET nhu \choice (xem TF_baitoan_du /
  phatbieu_giai trong math_type.py — da kiem chung tren generator that
  L10_C1_TF_A_01 trong data/python_bank/toan10/L10_C1.py). Co the co 1-4
  y \True trong 4 y (khong bat buoc dung 1 y dung nhu \choice).
"""
import re


class AnswerParseError(Exception):
    pass


def _tim_khoi_dong(text: str, vi_tri_mo: int) -> tuple[str, int]:
    r"""
    vi_tri_mo phai tro dung vao ky tu '{'. Dem ngoac { } long nhau (vi noi
    dung LaTeX ben trong, vd \frac{a}{b}, co the co nhieu cap {} long nhau)
    de tim dung dau '}' dong khop voi dau '{' mo dau.
    Tra ve (noi_dung_ben_trong_khong_ke_ngoac, vi_tri_ngay_sau_dau_dong).
    """
    if vi_tri_mo >= len(text) or text[vi_tri_mo] != "{":
        raise AnswerParseError(f"Vi tri {vi_tri_mo} khong phai ky tu '{{'")
    do_sau = 0
    i = vi_tri_mo
    while i < len(text):
        if text[i] == "{":
            do_sau += 1
        elif text[i] == "}":
            do_sau -= 1
            if do_sau == 0:
                return text[vi_tri_mo + 1:i], i + 1
        i += 1
    raise AnswerParseError("Ngoac { } khong can bang, khong tim duoc dau dong khop")


def _tim_tat_ca_khoi_lien_tiep(text: str, tu: int) -> list[str]:
    """Tu vi tri `tu`, doc lien tiep cac khoi {...} (bo qua khoang trang,
    xuong dong giua cac khoi). Dung lai ngay khi gap ky tu khong phai '{'."""
    ket_qua = []
    i = tu
    while i < len(text):
        while i < len(text) and text[i] in " \t\r\n":
            i += 1
        if i >= len(text) or text[i] != "{":
            break
        noi_dung, i = _tim_khoi_dong(text, i)
        ket_qua.append(noi_dung)
    return ket_qua


def _tim_vi_tri_sau_lenh(text: str, ten_lenh: str) -> int | None:
    r"""
    Tim vi tri ngay sau 1 ten lenh LaTeX (vd tim \choice nhung KHONG duoc
    khop nham vao \choiceTF, \choiceTFn...). Tra ve None neu khong co.
    """
    pattern = re.compile(re.escape(ten_lenh) + r"(?![A-Za-z])")
    m = pattern.search(text)
    if not m:
        return None
    return m.end()


def trich_dap_an_choice(latex_block: str) -> dict | None:
    r"""
    Trich dap an cho cau trac nghiem 4 phuong an (\choice{..}{..}{..}{..}).
    Tra ve {"dap_an_dung": "A"|"B"|"C"|"D", "phuong_an": {"A":.., "B":.., ...}}
    hoac None neu latex_block nay khong co \choice (vd la cau SA/TL/TF).
    """
    vi_tri = _tim_vi_tri_sau_lenh(latex_block, r"\choice")
    if vi_tri is None:
        return None
    khoi = _tim_tat_ca_khoi_lien_tiep(latex_block, vi_tri)
    if len(khoi) != 4:
        raise AnswerParseError(
            f"\\choice phai co dung 4 phuong an, tim duoc {len(khoi)}: {khoi}"
        )
    nhan = ["A", "B", "C", "D"]
    phuong_an = {}
    dap_an_dung = None
    for ky_hieu, noi_dung in zip(nhan, khoi):
        sach = noi_dung.strip()
        if sach.startswith(r"\True"):
            dap_an_dung = ky_hieu
            sach = sach[len(r"\True"):].strip()
        phuong_an[ky_hieu] = sach
    if dap_an_dung is None:
        raise AnswerParseError("Khong tim thay \\True trong 4 phuong an cua \\choice")
    return {"dap_an_dung": dap_an_dung, "phuong_an": phuong_an}


def trich_dap_an_shortans(latex_block: str) -> str | None:
    r"""
    Trich dap an cho cau tra loi ngan (\shortans{..} hoac \shortans[N]{..}).
    Tra ve chuoi dap an (da la text thuan) hoac None neu khong co \shortans.
    """
    m = re.search(r"\\shortans(?:\[[^\]]*\])?", latex_block)
    if not m:
        return None
    vi_tri = m.end()
    while vi_tri < len(latex_block) and latex_block[vi_tri] in " \t\r\n":
        vi_tri += 1
    if vi_tri >= len(latex_block) or latex_block[vi_tri] != "{":
        raise AnswerParseError("\\shortans khong co khoi {..} dap an theo sau")
    noi_dung, _ = _tim_khoi_dong(latex_block, vi_tri)
    return noi_dung.strip()


def trich_dap_an_tf(latex_block: str) -> dict | None:
    r"""
    Trich dap an cho cau Dung/Sai (\choiceTFn[N]{..}{..}{..}{..} hoac
    \choiceTFt{..}{..}{..}{..}). 4 khoi tuong ung 4 y a/b/c/d, moi khoi
    danh dau dung bang \True o dau noi dung (giong het \choice), NHUNG
    khac \choice o cho: co the co 1 den 4 y \True trong 4 y (khong bat
    buoc dung 1 dap an dung nhu MC).

    Tra ve:
    {
        "dap_an_dung": {"a": True/False, "b": ..., "c": ..., "d": ...},
        "phat_bieu": {"a": "...", "b": "...", "c": "...", "d": "..."}
    }
    hoac None neu latex_block nay khong co \choiceTFn/\choiceTFt (vd la
    cau MC/SA/TL).
    """
    m = re.search(r"\\choiceTFn\[[1-4]\]|\\choiceTFt", latex_block)
    if not m:
        return None
    vi_tri = m.end()
    khoi = _tim_tat_ca_khoi_lien_tiep(latex_block, vi_tri)
    if len(khoi) != 4:
        raise AnswerParseError(
            f"\\choiceTFn/\\choiceTFt phai co dung 4 y a/b/c/d, tim duoc {len(khoi)}: {khoi}"
        )
    nhan = ["a", "b", "c", "d"]
    dap_an_dung = {}
    phat_bieu = {}
    for ky_hieu, noi_dung in zip(nhan, khoi):
        sach = noi_dung.strip()
        dung = sach.startswith(r"\True")
        if dung:
            sach = sach[len(r"\True"):].strip()
        dap_an_dung[ky_hieu] = dung
        phat_bieu[ky_hieu] = sach
    return {"dap_an_dung": dap_an_dung, "phat_bieu": phat_bieu}


_MOC_BAT_DAU_DAP_AN = [
    r"\\choiceTFn\[[1-4]\]",
    r"\\choiceTFt",
    r"\\shortans(?:\[[^\]]*\])?",
    r"\\choice(?![A-Za-z])",
]


def trich_de_bai(latex_block: str) -> dict:
    r"""
    Trich phan "de bai" (noi dung cau hoi hien thi cho hoc sinh, TRUOC khi
    co dap an) tu 1 latex_block — dung cho trang lam bai truc tiep tren
    web (khac PDF: PDF nhung nguyen latex_block vao document, web can
    tach rieng phan de bai vi \choice/\shortans/\choiceTFn KHONG hien thi
    y nguyen, ma render lai thanh nut bam/o nhap).

    Lay tu sau "\begin{ex}" (bo qua dong "%%[?]" neu co) den truoc lenh
    dap an dau tien gap duoc (\choice, \shortans, \choiceTFn, \choiceTFt).

    Tra ve {"de_bai": "...", "co_hinh_ve": True/False}. co_hinh_ve=True
    nghia la de bai co nhung phan khong the ve lai bang MathJax (hinh ve
    TikZ qua \immini, \includegraphics...) — cau nay TAM THOI khong dua
    vao lam bai truc tiep tren web, chi xuat PDF nhu cu.
    """
    m = re.search(r"\\begin\{ex\}", latex_block)
    bat_dau = m.end() if m else 0

    vi_tri_dap_an = [
        mm.start() + bat_dau
        for pat in _MOC_BAT_DAU_DAP_AN
        if (mm := re.search(pat, latex_block[bat_dau:]))
    ]
    ket_thuc = min(vi_tri_dap_an) if vi_tri_dap_an else len(latex_block)

    de_bai = latex_block[bat_dau:ket_thuc]
    de_bai = re.sub(r"^\s*%%\[\?\]\s*\n?", "", de_bai).strip()

    co_hinh_ve = bool(re.search(r"\\immini|\\includegraphics|\\begin\{tikzpicture\}", de_bai))

    return {"de_bai": de_bai, "co_hinh_ve": co_hinh_ve}


def trich_loi_giai(latex_block: str) -> str | None:
    r"""Trich noi dung trong \loigiai{...}. Tra ve None neu khong co."""
    vi_tri = _tim_vi_tri_sau_lenh(latex_block, r"\loigiai")
    if vi_tri is None:
        return None
    while vi_tri < len(latex_block) and latex_block[vi_tri] in " \t\r\n":
        vi_tri += 1
    if vi_tri >= len(latex_block) or latex_block[vi_tri] != "{":
        return None
    noi_dung, _ = _tim_khoi_dong(latex_block, vi_tri)
    return noi_dung.strip()


def chuan_hoa_dap_an_ngan(text: str | None) -> str:
    """
    Chuan hoa 1 chuoi dap an ngan (SA) de so sanh linh hoat giua dap an
    dung (trich tu latex_block) va dap an hoc sinh go tay: bo khoang
    trang dau/cuoi, bo dau $ (ky hieu cong thuc LaTeX), bo hoa/thuong,
    bo het khoang trang o giua.
    """
    if not text:
        return ""
    return text.strip().strip("$").replace(" ", "").lower()


def chuan_hoa_dap_an_tf(gia_tri) -> bool | None:
    """
    Chuan hoa 1 dap an TF hoc sinh gui len (tu Frontend, JSON) ve dung
    kieu bool de so sanh voi dap_an_dung (dict a/b/c/d -> True/False).
    Chap nhan: bool, "true"/"false", "dung"/"sai", "d"/"s", 1/0.
    Tra ve None neu khong nhan dien duoc (coi la chua tra loi).
    """
    if isinstance(gia_tri, bool):
        return gia_tri
    if gia_tri is None:
        return None
    if isinstance(gia_tri, (int, float)):
        return bool(gia_tri)
    text = str(gia_tri).strip().lower()
    if text in ("true", "dung", "đúng", "d", "1", "correct"):
        return True
    if text in ("false", "sai", "s", "0", "incorrect"):
        return False
    return None


def trich_dap_an(latex_block: str) -> dict:
    r"""
    Ham tong hop dung cho 1 latex_block (1 cau hoi) — tu nhan dien loai cau:
    - Co \choiceTFn/\choiceTFt -> TF (dung/sai 4 y doc lap) — kiem tra
      TRUOC \choice vi \choiceTFn cung chua chu "choice" (dung negative
      lookahead trong trich_dap_an_choice de khong khop nham, nhung kiem
      tra TF truoc van an toan hon va ro rang hon ve thu tu uu tien).
    - Co \choice  -> MC (trac nghiem 4 phuong an)
    - Co \shortans -> SA (tra loi ngan)
    - Khong co ca 3 -> TL (tu luan)
    """
    de_bai = trich_de_bai(latex_block)

    tf = trich_dap_an_tf(latex_block)
    if tf is not None:
        return {
            "loai_cau": "TF",
            "dap_an_dung": tf["dap_an_dung"],
            "phat_bieu": tf["phat_bieu"],
            "loi_giai": trich_loi_giai(latex_block),
            **de_bai,
        }
    choice = trich_dap_an_choice(latex_block)
    if choice is not None:
        return {
            "loai_cau": "MC",
            "dap_an_dung": choice["dap_an_dung"],
            "phuong_an": choice["phuong_an"],
            "loi_giai": trich_loi_giai(latex_block),
            **de_bai,
        }
    shortans = trich_dap_an_shortans(latex_block)
    if shortans is not None:
        return {
            "loai_cau": "SA",
            "dap_an_dung": shortans,
            "loi_giai": trich_loi_giai(latex_block),
            **de_bai,
        }
    return {
        "loai_cau": "TL",
        "dap_an_dung": None,
        "loi_giai": trich_loi_giai(latex_block),
        **de_bai,
    }