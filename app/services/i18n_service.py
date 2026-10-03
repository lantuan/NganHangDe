"""
Đa ngôn ngữ Việt / Anh (cô Lan 03/10/2026).

Cách làm: KHÔNG sửa từng template. Mỗi trang HTML (và các thông báo JSON) đi qua
một bước dịch theo từ điển khi người dùng chọn tiếng Anh; chữ nào chưa có trong từ
điển thì giữ nguyên tiếng Việt (web vẫn chạy, đầy dần theo từ điển).

Từ điển (Việt -> Anh, thuật ngữ Toán của Mỹ, hướng SAT) nằm trong data/i18n/:
  en_ui.json          chữ trên giao diện web (template)
  en_curriculum.json  tên chương, tên bài, yêu cầu cần đạt
  (sau này) en_bank_*.json  chữ trong các hàm sinh câu của ngân hàng đề

Ngôn ngữ lưu trong cookie "lang" (vi | en); nút chuyển ở góc phải trên mọi trang.
Chữ được cắt thành ĐOẠN giống scripts/i18n_trich_chuoi.py (ngắt ở thẻ HTML, {}, nháy,
xuống dòng) rồi tra từ điển; đoạn ghép từ biến (vd "Xin chào, Lan!") dịch theo cụm
trong đoạn. Dấu nháy, ngoặc nhọn... không được xuất hiện thêm trong bản dịch (test).
"""
import json
import re
from functools import lru_cache
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
THU_MUC = GOC / "data" / "i18n"
NGON_NGU = ("vi", "en")
MAC_DINH = "vi"

_DAU = "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"
CO_DAU = re.compile("[" + _DAU + _DAU.upper() + "]")
DOAN = re.compile(r"[^<>{}\"'`\n\\$]+")          # phải khớp scripts/i18n_trich_chuoi.py
_TU = r"[0-9A-Za-z_" + _DAU + _DAU.upper() + "]"
KHOA_JSON_DICH = ("message", "detail", "tra_loi", "loi", "error", "thong_bao", "ten_chuong")


@lru_cache(maxsize=4)
def tu_dien(ngon_ngu: str) -> dict:
    """Từ điển Việt -> ngôn ngữ đích (gộp mọi file en_*.json)."""
    if ngon_ngu == "vi":
        return {}
    kq = {}
    for f in sorted(THU_MUC.glob(f"{ngon_ngu}_*.json")):
        kq.update(json.loads(f.read_text(encoding="utf-8")))
    return kq


@lru_cache(maxsize=4)
def _khoa_theo_do_dai(ngon_ngu: str) -> tuple:
    return tuple(sorted(tu_dien(ngon_ngu), key=len, reverse=True))


def _dich_trong_doan(d: str, td: dict, khoa: tuple) -> str:
    """Dịch các cụm từ điển nằm TRONG đoạn (đoạn ghép từ biến, vd 'Lớp 10 - Toán')."""
    ra, i = [], 0
    while i < len(d):
        tim = None
        if i == 0 or not re.match(_TU, d[i - 1]):
            for k in khoa:
                if len(k) >= 2 and d.startswith(k, i) and (i + len(k) == len(d) or not re.match(_TU, d[i + len(k)])):
                    tim = k
                    break
        if tim:
            ra.append(td[tim])
            i += len(tim)
        else:
            ra.append(d[i])
            i += 1
    return "".join(ra)


def dich_doan(d: str, ngon_ngu: str) -> str:
    """Dịch một đoạn chữ (không chứa xuống dòng). Không có trong từ điển -> giữ nguyên."""
    td = tu_dien(ngon_ngu)
    if not td or not CO_DAU.search(d):
        return d
    gon = " ".join(d.split())
    if gon in td:
        dau = d[: len(d) - len(d.lstrip())]
        cuoi = d[len(d.rstrip()):]
        return dau + td[gon] + cuoi
    return _dich_trong_doan(d, td, _khoa_theo_do_dai(ngon_ngu))


def tieu_de_tieng_anh(tieu_de: str) -> str:
    """Tiêu đề đề thi bản tiếng Anh: dịch theo từ điển giao diện; còn sót chữ Việt thì dùng tiêu đề chung."""
    en = dich_doan(tieu_de or "", "en")
    return en if en and not CO_DAU.search(en) else "MATHEMATICS TEST"


def dich_html(html: str, ngon_ngu: str) -> str:
    if ngon_ngu == "vi" or not tu_dien(ngon_ngu):
        return html
    return DOAN.sub(lambda m: dich_doan(m.group(0), ngon_ngu), html)


def dich_json(obj, ngon_ngu: str, khoa: str | None = None):
    """Dịch các giá trị chuỗi của khoá thông báo (message, detail, tra_loi, ...)."""
    if isinstance(obj, dict):
        return {k: dich_json(v, ngon_ngu, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [dich_json(v, ngon_ngu, khoa) for v in obj]
    if isinstance(obj, str) and khoa in KHOA_JSON_DICH:
        return "\n".join(dich_html(dong, ngon_ngu) for dong in obj.split("\n"))
    return obj


def lay_ngon_ngu(request) -> str:
    """Ngôn ngữ của yêu cầu: ?lang=en > cookie lang > mặc định vi."""
    ma = request.query_params.get("lang") or request.cookies.get("lang") or MAC_DINH
    return ma if ma in NGON_NGU else MAC_DINH


NUT_CHUYEN = """
<div id="chv-lang" style="position:fixed;top:8px;right:12px;z-index:2147483000;display:flex;gap:0;
border:1px solid rgba(0,0,0,.25);border-radius:999px;overflow:hidden;font:600 12px/1 system-ui,sans-serif;
background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.2)" role="group" aria-label="Language">
<a href="#" data-lang="vi" style="padding:6px 10px;text-decoration:none;color:%(cvi)s;background:%(bvi)s">Tiếng Việt</a>
<a href="#" data-lang="en" style="padding:6px 10px;text-decoration:none;color:%(cen)s;background:%(ben)s">English</a>
</div>
<script>
(function () {
  var nut = document.getElementById('chv-lang');
  nut.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      document.cookie = 'lang=' + a.dataset.lang + '; path=/; max-age=31536000; SameSite=Lax';
      var u = new URL(location.href); u.searchParams.delete('lang'); location.href = u.toString();
    });
  });
  // Tai khoan / Dang xuat o goc phai tren van o NGOAI CUNG; nut Viet-Anh xich sang trai
  // (co Lan 03/10/2026). Tim cac phan tu o dai tren cung, sat mep phai, lay mep trai nhat.
  function datViTri() {
    var W = window.innerWidth, trai = W, giua = null, duoi = 0;
    nut.style.right = '12px'; nut.style.top = '8px';
    // Khu giao vien (thanh dau trang day chu): dat nut NGAY DUOI thanh dau trang, sat mep phai, khong che menu.
    if (document.body && document.body.getAttribute('data-chv-lang') === 'duoi') {
      var hd = document.querySelector('header');
      nut.style.right = '12px';
      nut.style.top = ((hd ? hd.getBoundingClientRect().bottom : 56) + 6) + 'px';
      return;
    }
    document.querySelectorAll('body *').forEach(function (el) {
      if (nut.contains(el) || el.contains(nut) || el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
      var r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (r.width < 8 || r.height < 8 || r.width > Math.min(460, W * 0.7) || r.top > 70 || r.bottom < 0) return;
      if (cs.visibility === 'hidden' || cs.display === 'none' || cs.opacity === '0') return;
      if (r.left < W - 480 || r.right < W - 480) return;
      if (el.children.length && !(el.childNodes.length && Array.prototype.some.call(el.childNodes,
          function (n) { return n.nodeType === 3 && n.textContent.trim(); }))
          && !/^(A|BUTTON|IMG|INPUT|SELECT)$/.test(el.tagName) && !/badge|account|user/i.test(el.className + '')) return;
      if (r.left < trai) { trai = r.left; giua = (r.top + r.bottom) / 2; }
      duoi = Math.max(duoi, r.bottom);
    });
    if (trai < W - 12 - 4) {
      var phai = Math.max(12, W - trai + 10);
      if (W - phai - nut.offsetWidth >= 8) {            // du cho: xich sang trai, canh giua theo hang
        nut.style.right = phai + 'px';
        if (giua !== null) nut.style.top = Math.max(4, giua - nut.offsetHeight / 2) + 'px';
      } else {                                           // man hinh hep: dat ngay DUOI tai khoan
        nut.style.top = (duoi + 4) + 'px';
      }
    }
  }
  window.addEventListener('load', function () { datViTri(); setTimeout(datViTri, 400); setTimeout(datViTri, 1500); });
  window.addEventListener('resize', datViTri);
})();
</script>
"""


def chen_nut_chuyen(html: str, ngon_ngu: str) -> str:
    """Chèn nút Tiếng Việt | English cố định ở góc phải trên; đặt <html lang>."""
    if "</body>" not in html:
        return html
    # (màu chữ, màu nền): được chọn = chữ trắng nền xanh; không chọn = chữ xanh nền trắng
    sel, ns = ("#fff", "#1a56db"), ("#1a56db", "#fff")
    cvi, bvi = sel if ngon_ngu == "vi" else ns
    cen, ben = sel if ngon_ngu == "en" else ns
    nut = NUT_CHUYEN % {"cvi": cvi, "bvi": bvi, "cen": cen, "ben": ben}
    html = html.replace("</body>", nut + "</body>", 1)
    return re.sub(r'<html([^>]*?)\blang="[^"]*"', r'<html\1lang="%s"' % ngon_ngu, html, count=1)
