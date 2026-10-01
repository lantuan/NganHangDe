r"""Câu TỰ LUẬN chỉ đưa ra HAI Ý (cô Lan 01/10/2026: "bài tự luận nào cũng đưa ra 2 ý thôi";
"các ý hiện nay đang 3 thì không cần xoá ý, mà chuyển thành random tuỳ bài để chọn các ý").

Hàm sinh câu tự luận (math_type.TL_answer_*) viết đề và lời giải thành hai danh sách
\begin{listEX}...\item...\end{listEX} cùng thứ tự. Câu có từ ba ý trở lên được rút còn
hai ý GIỮ THỨ TỰ, chọn ngẫu nhiên mỗi lần sinh; lời giải của ý bị bỏ ĐỨNG TRƯỚC một ý
được giữ thì ghép vào đầu lời giải ý đó (bước trung gian vẫn có trong lời giải), ý bị
bỏ đứng sau cùng thì bỏ hẳn.

Mức độ (cô Lan dặn đánh giá mức độ): các ý viết theo thứ tự khó dần. Câu tự luận mức VD
quy ước ý a) VD, ý b) VDC nên LUÔN giữ ý cuối (ý khó nhất); câu mức NB/TH lấy cặp bất kì.
Không sửa math_type (quy định của cô) - lọc ở tầng generator_service.
"""
import random
import re

from app.services.mapping_service import cac_y_tu_luan

_MO = re.compile(r"\\begin\{listEXV?\}(\[[^\]]*\])?")
_DONG = re.compile(r"\\end\{listEXV?\}")
_ITEM = re.compile(r"\\item(?![A-Za-z])")
_THAM_CHIEU = [
    (re.compile(r"\s*\((?:theo |ở |từ )?(?:câu|ý) [a-e]\)?\)"), ""),
    (re.compile(r"(?:Theo|Từ|Ở) (?:kết quả )?(?:câu|ý) [a-e]\)?,?\s*"), ""),
]


def _tim_listex(text: str, tu: int):
    """(vị trí bắt đầu thân, vị trí kết thúc thân) của listEX đầu tiên từ vị trí tu, có tính lồng nhau."""
    m = _MO.search(text, tu)
    if not m:
        return None
    do_sau, i = 1, m.end()
    while i < len(text):
        mo, dong = _MO.search(text, i), _DONG.search(text, i)
        if not dong:
            return None
        if mo and mo.start() < dong.start():
            do_sau += 1
            i = mo.end()
            continue
        do_sau -= 1
        if do_sau == 0:
            return m.end(), dong.start()
        i = dong.end()
    return None


def _tach_item(than: str):
    """Tách các \\item ở tầng ngoài cùng (bỏ qua \\item của danh sách lồng bên trong)."""
    vt, do_sau, i = [], 0, 0
    while i < len(than):
        mo, dong, it = _MO.search(than, i), _DONG.search(than, i), _ITEM.search(than, i)
        ung = [x for x in (mo, dong, it) if x]
        if not ung:
            break
        x = min(ung, key=lambda y: y.start())
        if x is mo:
            do_sau += 1
        elif x is dong:
            do_sau -= 1
        elif do_sau == 0:
            vt.append(x.start())
        i = x.end()
    if not vt:
        return than, []
    dau = than[:vt[0]]
    return dau, [than[a:b] for a, b in zip(vt, vt[1:] + [len(than)])]


def _bo_tham_chieu(s: str) -> str:
    for pat, thay in _THAM_CHIEU:
        s = pat.sub(thay, s)
    return s


def _chon_cap(n: int, muc_vd: bool):
    cap = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if muc_vd:
        cap = [c for c in cap if c[1] == n - 1]
    return random.choice(cap)


def _muc_vd(generator_id: str | None) -> bool:
    gid = generator_id or ""
    y = cac_y_tu_luan(gid)
    if y:
        return y[-1][0] in ("VD", "VDC")
    return bool(re.search(r"_VD\d+[A-Z]?_TL_", gid))


def _rut_mot_cau(ex: str, muc_vd: bool) -> str:
    lg = ex.find("\\loigiai")
    if lg == -1:
        return ex
    q = _tim_listex(ex, 0)
    s = _tim_listex(ex, lg)
    if not q or not s or q[1] > lg:
        return ex
    dau_q, item_q = _tach_item(ex[q[0]:q[1]])
    dau_s, item_s = _tach_item(ex[s[0]:s[1]])
    n = len(item_q)
    if n <= 2 or len(item_s) != n:
        return ex
    i, j = _chon_cap(n, muc_vd)
    giu_q = [item_q[i], _bo_tham_chieu(item_q[j])]
    if j - 1 != i:
        # ý ngay trước ý j đã bị bỏ: "Từ đó tính..." không còn chỗ dựa
        giu_q[1] = re.sub(r"(\\item\s*)Từ đó,?\s+(\w)", lambda m: m.group(1) + m.group(2).upper(), giu_q[1], count=1)

    def ghep(chi_so_bo, dich):
        if not chi_so_bo:
            return item_s[dich]
        than_bo = " ".join(_ITEM.sub("", item_s[k], count=1).strip() for k in chi_so_bo)
        goc = _ITEM.sub("", item_s[dich], count=1).strip()
        return "\\item " + than_bo + "\\\\\n" + goc + "\n"
    giu_s = [ghep(list(range(0, i)), i), _bo_tham_chieu(ghep(list(range(i + 1, j)), j))]
    if i > 0:
        giu_q[0] = _bo_tham_chieu(giu_q[0])
    than_q = dau_q + "".join(x if x.endswith("\n") else x + "\n" for x in giu_q)
    than_s = dau_s + "".join(x if x.endswith("\n") else x + "\n" for x in giu_s)
    # thay phần lời giải trước (vị trí sau) để không lệch chỉ số phần đề
    ex = ex[:s[0]] + than_s + ex[s[1]:]
    return ex[:q[0]] + than_q + ex[q[1]:]


def giu_hai_y(latex_block: str, generator_id: str | None) -> str:
    """Rút mọi câu tự luận trong latex_block (có thể nhiều \\begin{ex}) còn đúng hai ý."""
    if "_TL_" not in (generator_id or ""):
        return latex_block
    vd = _muc_vd(generator_id)
    phan = re.split(r"(\\begin\{ex\}.*?\\end\{ex\})", latex_block, flags=re.S)
    return "".join(_rut_mot_cau(p, vd) if p.startswith("\\begin{ex}") else p for p in phan)
