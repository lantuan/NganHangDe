"""
Ma trận CỤ THỂ THEO BÀI do giáo viên đặt (cô Lan 14/10/2026).

Khác ma_tran_service.py (đặt số câu + tỉ lệ % theo LOẠI câu), chế độ này cho giáo viên khai
báo CỤ THỂ: bài nào có mấy câu NB / TH / VD, loại MC hay SA; chương nào có mấy câu Đúng/Sai
(TF) và Tự luận (TL).

Cách khai báo (cô Lan chốt 14/10/2026):
1. Giáo viên nhập TỔNG toàn đề: NB, TH, VD (VD gồm cả VDC).
2. Mỗi câu Đúng/Sai (chọn theo CHƯƠNG) tự trừ 1 NB + 1 TH + 2 VD (ý VD và ý VDC).
   Mỗi câu Tự luận (chọn theo CHƯƠNG) tự trừ 2 VD (ý a mức VD, ý b mức VDC, như logic cũ).
3. Phần còn lại giáo viên chia vào từng BÀI cho trắc nghiệm (MC) và trả lời ngắn (SA).
   Phần VD của MC + SA được hệ thống chia 2 VD : 1 VDC (làm tròn: VDC = round(VD / 3));
   Tự luận giữ nguyên 1 VD + 1 VDC mỗi câu; mapping không có câu VDC riêng, VDC là suất của câu VD.
4. Tạo đề chỉ khi tổng khớp ĐÚNG và mọi ô đủ câu trong ngân hàng.

Cấu trúc ma trận (dict):
    {"tong": {"NB": n, "TH": n, "VD": n},
     "tf": {chuong_so: so_cau}, "tl": {chuong_so: so_cau},
     "o": {"L10_C3_B5": {"trac_nghiem": {"NB": n, "TH": n, "VD": n}, "tra_loi_ngan": {...}}}}
"""
import random
import re
from collections import Counter

from app.services.exam_rules_service import ExamRulesError

MUC = ("NB", "TH", "VD")
LOAI_O = {"mc": "trac_nghiem", "sa": "tra_loi_ngan"}
TEN_LOAI = {"trac_nghiem": "trắc nghiệm", "tra_loi_ngan": "trả lời ngắn"}
_BAI = re.compile(r"^L(\d+)_C(\d+)_B(\d+)$")
_ROW_BAI = re.compile(r"^L\d+_C\d+_B(\d+)_")


def _so_nguyen(gt, ten: str) -> int:
    s = str(gt if gt is not None else "").strip()
    if s == "":
        return 0
    try:
        v = int(s)
    except ValueError:
        raise ExamRulesError(f"{ten} phải là số nguyên.")
    if v < 0 or v > 100:
        raise ExamRulesError(f"{ten} phải từ 0 đến 100.")
    return v


def doc_ma_tran_bai_tu_form(form) -> dict | None:
    """Đọc từ form giáo viên. Trả None nếu không bật chế độ "đặt số câu cụ thể theo bài".

    Trường: ma_tran_bai (bật), mtb_tong_nb|th|vd, mtb_tf_<chương>, mtb_tl_<chương>,
    mtb_o_<L10_C3_B5>_<mc|sa>_<nb|th|vd>."""
    if not form.get("ma_tran_bai"):
        return None
    mt = {"tong": {m: _so_nguyen(form.get(f"mtb_tong_{m.lower()}"), f"Tổng {m}") for m in MUC},
          "tf": {}, "tl": {}, "o": {}}
    for k in list(form.keys()):
        m = re.fullmatch(r"mtb_(tf|tl)_(\d+)", k)
        if m:
            n = _so_nguyen(form.get(k), f"Số câu {m.group(1).upper()} chương {m.group(2)}")
            if n:
                mt[m.group(1)][int(m.group(2))] = n
            continue
        m = re.fullmatch(r"mtb_o_(L\d+_C\d+_B\d+)_(mc|sa)_(nb|th|vd)", k)
        if m:
            n = _so_nguyen(form.get(k), f"Ô {m.group(1)} {m.group(2).upper()} {m.group(3).upper()}")
            if n:
                mt["o"].setdefault(m.group(1), {}).setdefault(LOAI_O[m.group(2)], {})[m.group(3).upper()] = n
    if not any(f"mtb_tong_{m.lower()}" in form for m in MUC):
        # Bảng kiểu ma trận đề (cô Lan 14/10/2026): không khai tổng riêng, tổng = đúng những gì
        # cô đã điền (TF, TL theo chương tự trừ 1+1+2 và 0+0+2).
        mt["tong"] = da_dung(mt)
    return mt


def da_dung(mt: dict) -> dict:
    """Số NB / TH / VD đã dùng: các ô MC + SA, cộng phần tự trừ của TF (1+1+2) và TL (0+0+2)."""
    d = {"NB": 0, "TH": 0, "VD": 0}
    for loai in mt["o"].values():
        for muc in loai.values():
            for m, n in muc.items():
                d[m] += n
    tf = sum(mt["tf"].values())
    tl = sum(mt["tl"].values())
    d["NB"] += tf
    d["TH"] += tf
    d["VD"] += 2 * tf + 2 * tl
    return d


def con_lai(mt: dict) -> dict:
    d = da_dung(mt)
    return {m: mt["tong"][m] - d[m] for m in MUC}


def so_vdc(mt: dict) -> int:
    """VDC của MC + SA: một phần ba số câu VD của các ô (tỉ lệ 2 VD : 1 VDC), làm tròn."""
    vd = sum(muc.get("VD", 0) for loai in mt["o"].values() for muc in loai.values())
    return int(vd / 3 + 0.5)


def _tong_o(mt: dict, loai: str, muc: str) -> int:
    return sum(l.get(loai, {}).get(muc, 0) for l in mt["o"].values())


def cau_truc_tong_quat(mt: dict) -> dict:
    return {"trac_nghiem": sum(_tong_o(mt, "trac_nghiem", m) for m in MUC),
            "dung_sai_cau_lon": sum(mt["tf"].values()),
            "tra_loi_ngan": sum(_tong_o(mt, "tra_loi_ngan", m) for m in MUC),
            "tu_luan": sum(mt["tl"].values())}


# ----------------------------------------------------------------------------------------
# Số câu tối đa ngân hàng có (để hiện trên form và để chặn trước khi tạo đề)
# ----------------------------------------------------------------------------------------
def _dem_ham_theo_id(lop: int, chuong: int) -> dict[str, int]:
    """{ID dạng (Generator ID trong Mapping): số HÀM (biến thể _01, _02...) thật trong ngân hàng Python}.
    Đọc thẳng tệp .py bằng văn bản (không import). Dạng chỉ có trong Mapping mà chưa viết hàm thì không có."""
    from app.services.mapping_service import PYTHON_BANK_DIR
    f = PYTHON_BANK_DIR / f"toan{lop}" / f"L{lop}_C{chuong}.py"
    if not f.exists():
        return {}
    try:
        src = f.read_text(encoding="utf-8")
    except OSError:
        return {}
    return dict(Counter(re.findall(r"^def (L\d+_[A-Za-z0-9_]+?)_\d{2}\s*\(", src, re.M)))


def _bai_tu_curriculum(cid: str):
    m = re.match(r"^(L\d+_C\d+_B\d+)", cid or "")
    return m.group(1) if m else None


def _tl_co_vd_trong_pham_vi(r: dict, pham_vi: set) -> bool:
    """Dòng Mapping Tự luận có ý mức VD ở bài nằm trong phạm vi đề."""
    if r.get("cac_y"):
        cap = [(_bai_tu_curriculum(y.get("curriculum_id", "")), y.get("muc_do")) for y in r["cac_y"]]
    else:
        cap = [(_bai_tu_curriculum(r["id"]), r.get("muc_do"))]
    return any(muc == "VD" and bai in pham_vi for bai, muc in cap)


def so_cau_ngan_hang(lop: int, pham_vi_bai: list[str]) -> dict:
    """{"o": {bai_id: {loai: {muc: n}}}, "tf": {chuong: n}, "tl": {chuong: n}}.

    n = số HÀM sinh câu thật trong ngân hàng Python (mỗi dạng x biến thể _01, _02... là một hàm),
    không phải số dòng Mapping: Mapping chỉ khai dạng, biến thể chỉ có trong Python (cô Lan 14/10/2026).
    Số này không phải trần cứng: đặt nhiều hơn thì bộ chọn dùng lại biến thể với số liệu khác."""
    from app.services.mapping_service import load_mapping, phan_loai_cau
    chuong = sorted({int(_BAI.match(b).group(2)) for b in pham_vi_bai if _BAI.match(b)})
    kq = {"o": {b: {l: {m: 0 for m in MUC} for l in LOAI_O.values()} for b in pham_vi_bai},
          "tf": {}, "tl": {}}
    for c in chuong:
        try:
            rows = load_mapping(lop, c)
        except (FileNotFoundError, ValueError):
            rows = []
        ham = _dem_ham_theo_id(lop, c)
        kq["tf"][c] = 0
        kq["tl"][c] = 0
        for r in rows:
            n_ham = ham.get(r["id"], 0)
            if not n_ham:
                continue
            loai = phan_loai_cau(r)
            if loai == "dung_sai_cau_lon":
                kq["tf"][c] += n_ham
                continue
            m = _ROW_BAI.match(r["id"])
            bai_id = f"L{lop}_C{c}_B{int(m.group(1))}" if m else None
            if loai == "tu_luan":
                # Chỉ tính dạng Tự luận có ý mức VD thuộc BÀI TRONG PHẠM VI đề (bộ dựng blueprint cũng lọc
                # theo bài): vd giữa kỳ 1 lớp 10 chỉ có Chương 4 bài 7, 8 nên TL VD của bài 10, 11 không tính.
                if _tl_co_vd_trong_pham_vi(r, set(pham_vi_bai)):
                    kq["tl"][c] += n_ham
                continue
            if loai in TEN_LOAI and bai_id in kq["o"] and r.get("muc_do") in MUC:
                kq["o"][bai_id][loai][r["muc_do"]] += n_ham
    return kq


def kiem_tra_ma_tran_bai(mt: dict, lop: int, pham_vi_bai: list[str]) -> list[str]:
    """Danh sách lỗi tiếng Việt (rỗng = hợp lệ)."""
    loi = []
    tong = mt["tong"]
    if sum(tong.values()) <= 0:
        return ["Chưa nhập số câu nào vào bảng ma trận."]
    cl = con_lai(mt)
    for m in MUC:
        if cl[m] > 0:
            loi.append(f"Còn thiếu {cl[m]} câu {m} chưa phân vào bài (tổng khai báo {tong[m]}).")
        elif cl[m] < 0:
            loi.append(f"Đã phân dư {-cl[m]} câu {m} so với tổng khai báo {tong[m]} "
                       f"(câu Đúng/Sai và Tự luận đã tự trừ một phần).")
    phamvi = set(pham_vi_bai)
    for bai in mt["o"]:
        if bai not in phamvi:
            loi.append(f"Bài {bai} không nằm trong phạm vi đề.")
    chuong = {int(_BAI.match(b).group(2)) for b in pham_vi_bai if _BAI.match(b)}
    for k in ("tf", "tl"):
        for c in mt[k]:
            if c not in chuong:
                loi.append(f"Chương {c} không nằm trong phạm vi đề.")
    if loi:
        return loi
    for ten, n, co in _o_dang_dat(mt, so_cau_ngan_hang(lop, pham_vi_bai)):
        if co == 0:
            loi.append(f"{ten}: ngân hàng Python chưa có hàm sinh câu loại này, cô đặt {n}.")
    return loi


def _o_dang_dat(mt: dict, ng: dict):
    """(tên ô, số câu cô đặt, số hàm có sẵn) cho mọi ô cô đặt > 0."""
    for bai, loais in mt["o"].items():
        for loai, muc in loais.items():
            for m, n in muc.items():
                if n > 0:
                    yield (f"{bai}, {TEN_LOAI[loai]} {m}", n, ng["o"].get(bai, {}).get(loai, {}).get(m, 0))
    for c, n in mt["tf"].items():
        if n > 0:
            yield (f"Chương {c}, Đúng/Sai", n, ng["tf"].get(c, 0))
    for c, n in mt["tl"].items():
        if n > 0:
            yield (f"Chương {c}, Tự luận", n, ng["tl"].get(c, 0))


def canh_bao_ma_tran_bai(mt: dict, lop: int, pham_vi_bai: list[str]) -> list[str]:
    """Ô đặt NHIỀU HƠN số hàm có sẵn: vẫn tạo được đề (hết hàm thì bộ chọn dùng lại biến thể
    với số liệu khác, quy định của cô Lan), chỉ báo để cô biết câu sẽ lặp dạng."""
    return [f"{ten}: ngân hàng có {co} hàm, cô đặt {n} câu nên sẽ lặp lại dạng với số liệu khác."
            for ten, n, co in _o_dang_dat(mt, so_cau_ngan_hang(lop, pham_vi_bai)) if 0 < co < n]


# ----------------------------------------------------------------------------------------
# Khung hiển thị cho form (danh sách bài, số hàm có sẵn)
# ----------------------------------------------------------------------------------------
def khung_ma_tran_bai(lop: int, loai_he_so: str, ki_thi: str | None, pham_vi_chuong: str | None) -> dict:
    from app.services.exam_scope_service import load_scope_heso1, load_scope_heso23, _load_ppct
    if loai_he_so == "HeSo1":
        if not pham_vi_chuong:
            raise ExamRulesError("Kiểm tra thường xuyên phải chọn chương.")
        scope = load_scope_heso1(lop, pham_vi_chuong)
    else:
        scope = load_scope_heso23(lop, ki_thi or "")
    if "error" in scope:
        raise ExamRulesError(str(scope.get("message") or scope["error"]))
    pham_vi_bai = scope["pham_vi_bai"]
    ten = {}
    for b in _load_ppct(lop):
        ten[f"L{lop}_C{int(b['chuong_so'])}_B{int(b['bai_so'])}"] = (b.get("chuong"), b.get("bai"))
    ng = so_cau_ngan_hang(lop, pham_vi_bai)
    bai = []
    for b in pham_vi_bai:
        m = _BAI.match(b)
        c, bs = (int(m.group(2)), int(m.group(3))) if m else (None, None)
        bai.append({"bai_id": b, "chuong_so": c, "bai_so": bs, "ten_bai": (ten.get(b) or (None, None))[1],
                    "toi_da": ng["o"][b]})
    chuong = []
    for c in sorted(ng["tf"]):
        ten_c = next((v[0] for k, v in ten.items() if k.startswith(f"L{lop}_C{c}_B")), None)
        chuong.append({"chuong_so": c, "ten_chuong": ten_c, "tf_toi_da": ng["tf"][c], "tl_toi_da": ng["tl"][c]})
    # Trọng số điểm theo data/config/diem_rules.json (MC 3, TF 2, SA 2, TL 3 / thang 10): cột "Tỉ lệ % điểm"
    from app.services.diem_service import _load_rules
    quy_dinh = _load_rules()
    return {"pham_vi_bai": pham_vi_bai, "bai": bai, "chuong": chuong,
            "trong_so": quy_dinh["trong_so"], "thang_diem": quy_dinh["thang_diem"]}


# ----------------------------------------------------------------------------------------
# Dựng Blueprint từ ma trận (thay cho phần chia theo tỉ lệ của build_blueprint)
# ----------------------------------------------------------------------------------------
def xay_blueprint(mt: dict, pham_vi_bai: list[str], so_bai_theo_chuong: dict, so_tiet_theo_bai: dict,
                  theo_bai_cho_loai, da_dung_loai: dict, dem_dung: Counter) -> dict:
    """Trả về phần blueprint {dung_sai, trac_nghiem, tra_loi_ngan, tu_luan} + bao_cao_phan_bo.
    theo_bai_cho_loai(loai) -> {(bai_id, muc_do): [entries Curriculum]} (đã lọc theo Mapping)."""
    from app.services.exam_blueprint_service import (
        BlueprintError, _chon_bai_dung_sai, _chon_curriculum_id, _tach_chuong_bai)
    bp = {"dung_sai": [], "trac_nghiem": [], "tra_loi_ngan": [], "tu_luan": []}
    bao_cao = {"nguon": "ma_tran_bai"}

    def _bai_chuong(c):
        return [b for b in pham_vi_bai if (_tach_chuong_bai(b) or (None,))[0] == c]

    # 1. Đúng/Sai: theo CHƯƠNG (bộ chọn câu chọn theo chương; bài chỉ để ghi nhận)
    for c, n in sorted(mt["tf"].items()):
        ds = {b: so_tiet_theo_bai.get(b, 1) for b in _bai_chuong(c)}
        for bai_id, sl in _chon_bai_dung_sai(ds, n).items():
            cb = _tach_chuong_bai(bai_id)
            bp["dung_sai"].append({"chuong_so": cb[0], "bai_so": cb[1], "bai_id": bai_id, "so_cau": sl})

    # 2. Tự luận: theo chương, mỗi câu = 1 suất VD (ý a) + 1 suất VDC (ý b) trong CÙNG đơn vị
    tl_map = theo_bai_cho_loai("tu_luan")
    for c, n in sorted(mt["tl"].items()):
        bai_co = [b for b in _bai_chuong(c) if tl_map.get((b, "VD"))]
        if not bai_co:
            raise BlueprintError(f"Chương {c} không có dạng Tự luận mức VD trong ngân hàng.")
        random.shuffle(bai_co)
        chia = Counter(bai_co[i % len(bai_co)] for i in range(n))
        for bai_id, k in chia.items():
            cb = _tach_chuong_bai(bai_id)
            chon = _chon_curriculum_id(tl_map[(bai_id, "VD")], k, da_dung_loai["tu_luan"], dem_dung)
            for cid, cnt in Counter(e["id"] for e in chon).items():
                bp["tu_luan"].append({"curriculum_id": cid, "chuong_so": cb[0], "bai_so": cb[1],
                                      "muc_do": "VD", "tong_so_cau": 2 * cnt,
                                      "so_cau_VD": cnt, "so_cau_VDC": cnt})

    # 3. MC / SA: chia VDC (2 VD : 1 VDC) rải đều theo BÀI, mỗi bài một suất trước
    o_vd = [(loai, bai, n) for bai, ls in mt["o"].items() for loai, mm in ls.items()
            for m, n in mm.items() if m == "VD" and n > 0]
    vdc = {(loai, bai): 0 for loai, bai, _ in o_vd}
    cap = {(loai, bai): n for loai, bai, n in o_vd}
    con = so_vdc(mt)
    bai_co_vd = list({bai for _, bai, _ in o_vd})
    while con > 0 and any(vdc[k] < cap[k] for k in cap):
        random.shuffle(bai_co_vd)
        for bai in bai_co_vd:
            if con <= 0:
                break
            ung = [k for k in cap if k[1] == bai and vdc[k] < cap[k]]
            if ung:
                vdc[random.choice(ung)] += 1
                con -= 1
    bao_cao["vdc_theo_o"] = {f"{b}:{l}": v for (l, b), v in vdc.items() if v}

    for loai in ("trac_nghiem", "tra_loi_ngan"):
        mp = theo_bai_cho_loai(loai)
        for bai_id in pham_vi_bai:
            cells = mt["o"].get(bai_id, {}).get(loai, {})
            cb = _tach_chuong_bai(bai_id)
            for muc in ("NB", "TH"):
                n = cells.get(muc, 0)
                if n <= 0:
                    continue
                if not mp.get((bai_id, muc)):
                    raise BlueprintError(f"{bai_id}: không có dạng {TEN_LOAI[loai]} mức {muc} trong ngân hàng.")
                for e in _chon_curriculum_id(mp[(bai_id, muc)], n, da_dung_loai[loai], dem_dung):
                    bp[loai].append({"curriculum_id": e["id"], "chuong_so": cb[0], "bai_so": cb[1],
                                     "muc_do": muc, "tong_so_cau": 1})
            n = cells.get("VD", 0)
            if n <= 0:
                continue
            if not mp.get((bai_id, "VD")):
                raise BlueprintError(f"{bai_id}: không có dạng {TEN_LOAI[loai]} mức VD trong ngân hàng.")
            chon = _chon_curriculum_id(mp[(bai_id, "VD")], n, da_dung_loai[loai], dem_dung)
            vdc_con = vdc.get((loai, bai_id), 0)
            for cid, cnt in Counter(e["id"] for e in chon).items():
                so_vdc_id = min(cnt, vdc_con)
                vdc_con -= so_vdc_id
                bp[loai].append({"curriculum_id": cid, "chuong_so": cb[0], "bai_so": cb[1], "muc_do": "VD",
                                 "tong_so_cau": cnt, "so_cau_VD": cnt - so_vdc_id, "so_cau_VDC": so_vdc_id})
    return {"blueprint": bp, "bao_cao_phan_bo": bao_cao}
