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

Cau Dung/Sai (TF, dung \choiceTFn/\choiceTFt) CHUA xu ly trong file nay —
can xem them 1 vi du generator TF that de xac dinh dung macro danh dau
tung y dung/sai truoc khi viet them.
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
    hoac None neu latex_block nay khong co \choice (vd la cau SA/TL).
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


def trich_dap_an(latex_block: str) -> dict:
    r"""
    Ham tong hop dung cho 1 latex_block (1 cau hoi) — tu nhan dien loai cau:
    - Co \choice  -> MC (trac nghiem 4 phuong an)
    - Co \shortans -> SA (tra loi ngan)
    - Khong co ca 2 -> TL (tu luan) hoac loai chua ho tro (vd TF)
    """
    choice = trich_dap_an_choice(latex_block)
    if choice is not None:
        return {
            "loai_cau": "MC",
            "dap_an_dung": choice["dap_an_dung"],
            "phuong_an": choice["phuong_an"],
            "loi_giai": trich_loi_giai(latex_block),
        }
    shortans = trich_dap_an_shortans(latex_block)
    if shortans is not None:
        return {
            "loai_cau": "SA",
            "dap_an_dung": shortans,
            "loi_giai": trich_loi_giai(latex_block),
        }
    return {
        "loai_cau": "TL",
        "dap_an_dung": None,
        "loi_giai": trich_loi_giai(latex_block),
    }
