"""
CN_BuildBlueprint

Input : cau_truc_tong_quat, ty_le_muc_do (qua CN_LoadExamRules),
        pham_vi_bai (qua CN_LoadExamScope), Curriculum (qua CN_LoadCurriculum,
        đã lọc theo pham_vi_bai).
Output: Blueprint (đúng cấu trúc doc 03_DATA_STRUCTURE.md — có curriculum_id
        cụ thể cho MC/SA/TL, chuong_so cho TF).

Không được: đọc PPCT, đọc Mapping, gọi Python, sinh PDF, tự tạo/sửa
curriculum_id, tạo curriculum_id mức VDC (không tồn tại — doc 04, Ngoại lệ 2).
"""

import math
import random
import re
from collections import Counter

from app.services.exam_scope_service import load_scope_heso1, load_scope_heso23
from app.services.exam_rules_service import resolve_cau_truc_de, ExamRulesError
from app.services.curriculum_service import load_curriculum_for_scope, CurriculumError
from app.services.question_selector_service import select_questions, SelectorError

_CHUONG_PATTERN = re.compile(r"_C(\d+)_B")
_CHUONG_BAI_PATTERN = re.compile(r"_C(\d+)_B(\d+)")

# "tối đa 2 câu SA/chương; tối đa 2 câu TL/chương" — doc 08_CODE_NODES.md
MAX_SA_PER_CHUONG = 2
MAX_TL_PER_CHUONG = 2


class BlueprintError(Exception):
    pass


# ============================================================
# Helper — phạm vi / số bài theo chương (không đổi so với bản cũ)
# ============================================================

def _dem_so_bai_theo_chuong(pham_vi_bai: list[str]) -> dict[int, int]:
    dem = {}
    for bai_id in pham_vi_bai:
        match = _CHUONG_PATTERN.search(bai_id)
        if not match:
            continue
        chuong_so = int(match.group(1))
        dem[chuong_so] = dem.get(chuong_so, 0) + 1
    return dem


def _chia_theo_so_bai(so_luong: int, so_bai_theo_chuong: dict[int, int]) -> dict[int, int]:
    """
    Chia so_luong câu cho các chương theo tỉ lệ số bài học (dùng để xác
    định CẦN BAO NHIÊU câu mỗi chương — bước riêng biệt với việc CHỌN
    curriculum_id cụ thể, làm ở _chon_curriculum_id bên dưới).
    """
    if so_luong <= 0:
        return {}

    tong_so_bai = sum(so_bai_theo_chuong.values())
    if tong_so_bai == 0:
        return {}

    ket_qua = {
        chuong_so: math.floor(so_luong * so_bai / tong_so_bai)
        for chuong_so, so_bai in so_bai_theo_chuong.items()
    }
    da_phan_bo = sum(ket_qua.values())
    con_thieu = so_luong - da_phan_bo

    if con_thieu > 0:
        chuong_uu_tien = max(so_bai_theo_chuong, key=so_bai_theo_chuong.get)
        ket_qua[chuong_uu_tien] = ket_qua.get(chuong_uu_tien, 0) + con_thieu

    return {c: sl for c, sl in ket_qua.items() if sl > 0}


def _tach_chuong_bai(bai_id: str) -> tuple[int, int] | None:
    """'L10_C1_B2' -> (1, 2). Tra ve None neu khong doc duoc."""
    m = _CHUONG_BAI_PATTERN.search(bai_id)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _lam_tron_ngau_nhien(phan: dict, so_luong: int) -> dict:
    """Làm tròn các phần (số thực, tổng = so_luong) thành số nguyên, tổng
    vẫn đúng so_luong, và MỖI phần được làm tròn lên với xác suất ĐÚNG BẰNG
    phần lẻ của nó (lấy mẫu hệ thống, thứ tự ngẫu nhiên).

    Nhờ vậy tính trung bình nhiều đề, mỗi bài được đúng tỉ lệ số tiết,
    nhưng mỗi đề chia khác nhau - không bài nào bị bỏ rơi mãi.
    """
    ket = {k: math.floor(v + 1e-9) for k, v in phan.items()}
    con = so_luong - sum(ket.values())
    if con <= 0:
        return ket
    khoa = list(phan.keys())
    random.shuffle(khoa)
    le = [(k, phan[k] - ket[k]) for k in khoa]
    tong_le = sum(x for _k, x in le)
    if tong_le <= 1e-9:
        for k in khoa[:con]:
            ket[k] += 1
        return ket
    # dieu chinh cho tong phan le dung bang so cau con thieu
    he = con / tong_le
    u = random.random()
    tich = 0.0
    for k, x in le:
        truoc = tich
        tich += x * he
        # so diem u, u+1, u+2... roi vao [truoc; tich)
        ket[k] += math.floor(tich - u + 1) - math.floor(truoc - u + 1)
    # an toan so hoc: bu/tru cho dung tong
    chenh = so_luong - sum(ket.values())
    while chenh > 0:
        ket[random.choice(khoa)] += 1
        chenh -= 1
    while chenh < 0:
        k = random.choice([k for k in khoa if ket[k] > math.floor(phan[k] + 1e-9)] or khoa)
        if ket[k] > 0:
            ket[k] -= 1
            chenh += 1
    return ket


def _chia_theo_so_tiet(so_luong: int, so_tiet_theo_bai: dict[str, int]) -> dict[str, int]:
    """Chia so_luong câu về TỪNG BÀI theo TỈ LỆ SỐ TIẾT của bài đó.

    Quy định của giáo viên (thay cho cách chia đều theo số bài trước đây):
    bài dạy nhiều tiết hơn thì được nhiều câu hơn. Làm tròn xuống trước,
    phần dư dồn cho bài nhiều tiết nhất (nếu bằng tiết thì lấy bài đứng
    trước trong PPCT) để tổng luôn khớp đúng so_luong.
    """
    if so_luong <= 0 or not so_tiet_theo_bai:
        return {}

    tong_tiet = sum(so_tiet_theo_bai.values())
    if tong_tiet <= 0:
        return {}

    # SUA 29/09/2026 (co Lan: "neu da chia xong thi phai chon ngau nhien"):
    # truoc day phan du chia theo PHAN DU LON NHAT - bai nao phan le lon
    # hon thi LAN NAO cung thang, bai phan le nho KHONG BAO GIO duoc chia.
    # Do duoc: de giua ky 1 lop 10, bai 7 va bai 8 khong duoc cau trac
    # nghiem TH nao o ca 80/80 de. Nay bai duoc lam tron len voi xac suat
    # dung bang phan le cua no (_lam_tron_ngau_nhien): trung binh nhieu de
    # van dung ti le so tiet, moi de chia mot khac.
    ket_qua = _lam_tron_ngau_nhien(
        {b: so_luong * t / tong_tiet for b, t in so_tiet_theo_bai.items()}, so_luong)
    return {b: sl for b, sl in ket_qua.items() if sl > 0}


def _chon_bai_dung_sai(so_tiet_theo_bai: dict[str, int], so_cau_lon: int) -> dict[str, int]:
    """Chọn bài (đơn vị kiến thức) cho các câu Đúng/Sai — LÀM TRƯỚC TIÊN.

    HAI CÂU ĐÚNG/SAI PHẢI Ở HAI CHƯƠNG KHÁC NHAU (cô Lan chốt, nhắc lại
    29/09/2026). Nên chia CHƯƠNG trước, trong chương mới chọn bài.

    Vì sao phải sửa (đo được 29/09/2026): bản cũ chỉ xếp TẤT CẢ các bài
    trong phạm vi theo số tiết giảm dần rồi lấy N bài đầu. Lớp 10 có
    bài 1 và bài 2 của chương 1 nhiều tiết nhất, nên đề giữa kỳ 1 và
    cuối kỳ 1 ra 30/30 đề đều có CẢ HAI câu Đúng/Sai ở chương 1 - và
    luôn đúng hai bài ấy, không đề nào khác đề nào.

    Cách làm bây giờ:
    - Xếp các chương theo bài nhiều tiết nhất của chương đó, giảm dần
      (vẫn giữ tinh thần "bài dạy nhiều tiết hơn thì được nhiều câu hơn"
      mà cô Lan chốt 12/09/2026).
    - Rải lần lượt mỗi chương một câu. Chỉ khi số câu Đúng/Sai NHIỀU HƠN
      số chương trong phạm vi mới quay lại chương đã dùng - lúc ấy lấy
      bài KHÁC trong chương đó, không lặp lại đúng bài cũ.

    Mỗi câu Đúng/Sai lớn gồm đủ 4 ý NB-TH-VD-VDC lấy trong CÙNG một bài.
    Lưu ý: CN_QuestionSelector chọn câu Đúng/Sai theo CHƯƠNG, không theo
    bài (Ngoại lệ 1, docs/04) - nên chương mới là thứ quyết định câu nào
    ra đề, còn bài dùng để trừ suất ở các phần khác.
    """
    if so_cau_lon <= 0 or not so_tiet_theo_bai:
        return {}

    # SUA 29/09/2026 (co Lan: chia xong phai chon NGAU NHIEN): truoc day
    # xep chuong/bai theo so tiet giam dan roi lay dau danh sach - de nao
    # cung dung chuong ay, bai ay. Nay boc NGAU NHIEN, trong so = so tiet
    # (bai nhieu tiet van de duoc chon hon), khong lap chuong khi con
    # chuong khac (hai cau Dung/Sai phai khac chuong).
    def _chuong_cua(bai_id: str):
        cb = _tach_chuong_bai(bai_id)
        return cb[0] if cb else None

    theo_chuong: dict = {}
    for bai_id in so_tiet_theo_bai:
        theo_chuong.setdefault(_chuong_cua(bai_id), []).append(bai_id)

    def _boc(ds, trong_so):
        tong = sum(trong_so[x] for x in ds)
        r = random.random() * tong
        for x in ds:
            r -= trong_so[x]
            if r < 0:
                return x
        return ds[-1]

    tiet_chuong = {c: sum(so_tiet_theo_bai[b] for b in ds) for c, ds in theo_chuong.items()}
    ket_qua: dict[str, int] = {}
    chuong_con = list(theo_chuong)
    bai_da_dung: set = set()
    for _ in range(so_cau_lon):
        if not chuong_con:
            # het chuong moi quay vong - uu tien chuong con bai chua dung
            chuong_con = [c for c in theo_chuong
                          if any(b not in bai_da_dung for b in theo_chuong[c])] \
                or list(theo_chuong)
        c = _boc(chuong_con, tiet_chuong)
        chuong_con.remove(c)
        ds = [b for b in theo_chuong[c] if b not in bai_da_dung] or theo_chuong[c]
        b = _boc(ds, so_tiet_theo_bai)
        bai_da_dung.add(b)
        ket_qua[b] = ket_qua.get(b, 0) + 1
    return ket_qua


def _tru_phan_dung_sai(
    phan_bo_bai: dict[str, int],
    phan_bo_bai_ds: dict[str, int],
) -> tuple[dict[str, int], int]:
    """Trừ phần câu Đúng/Sai đã chiếm ra khỏi phân bổ của 1 mức độ.

    Quy định của giáo viên: câu Đúng/Sai được tính là 4 câu (1 NB + 1 TH
    + 1 VD + 1 VDC). Sau khi đã chọn bài cho Đúng/Sai thì ở CHÍNH bài đó
    phải trừ đi 1 câu cho mỗi mức - "đơn vị kiến thức đó chia ra được 3
    câu thì phải tính 1 ở đúng sai, chỉ còn 2".

    Trừ ở cấp BÀI như vậy đồng thời làm tổng chỉ tiêu của mức đó giảm
    đúng bằng số câu Đúng/Sai (doc 08: "chỉ tiêu còn lại = tổng - so_cau
    _dung_sai") - KHÔNG được trừ thêm lần nữa ở cấp tổng, sẽ thành trừ 2 lần.

    Tra ve (phan_bo_moi, so_cau_chua_tru_duoc). so_cau_chua_tru_duoc > 0
    khi bài đó vốn không được chia câu nào ở mức này - phần đó bỏ qua,
    không đẩy sang bài khác (tránh bài khác bị hụt câu vô cớ).
    """
    ket_qua = dict(phan_bo_bai)
    con_du = 0
    for bai_id, so_cau_ds in phan_bo_bai_ds.items():
        co = ket_qua.get(bai_id, 0)
        tru = min(co, so_cau_ds)
        if tru:
            ket_qua[bai_id] = co - tru
        con_du += so_cau_ds - tru
    return {b: sl for b, sl in ket_qua.items() if sl > 0}, con_du


def _chon_chuong_dung_sai(so_bai_theo_chuong: dict[int, int], so_cau_lon: int) -> dict[int, int]:
    """
    TF: chọn N chương (N = so_cau_lon), ưu tiên chương có nhiều bài hơn.
    Nếu N > số chương, lặp lại chương theo đúng thứ tự ưu tiên đó.
    """
    if so_cau_lon <= 0:
        return {}

    chuong_sap_xep = sorted(so_bai_theo_chuong.keys(), key=lambda c: -so_bai_theo_chuong[c])

    ket_qua = {}
    for i in range(so_cau_lon):
        chuong = chuong_sap_xep[i % len(chuong_sap_xep)]
        ket_qua[chuong] = ket_qua.get(chuong, 0) + 1

    return ket_qua


def _phan_bo_vd_vdc(
    chapters: list[int],
    so_vd: int,
    so_vdc: int,
    max_per_chuong: int | None = None,
) -> dict[int, dict]:
    """
    Quy tắc:
    1. VDC: mỗi chương tối đa 1 (rải đều các chương khác nhau), tôn trọng
       max_per_chuong nếu có. Nếu so_vdc > số chương, mới lặp lại chương.
    2. VD: ưu tiên rải vào các chương CHƯA có VDC (mỗi chương 1 câu trước),
       cũng tôn trọng max_per_chuong.
    3. Hết chương còn chỗ mới quay lại chương đã đầy (chấp nhận vượt cap
       như phương án cuối cùng, để không bị kẹt khi ít chương).

    max_per_chuong dùng cho tra_loi_ngan / tu_luan (tối đa 2 câu/chương —
    doc 08_CODE_NODES.md). trac_nghiem không giới hạn (max_per_chuong=None).
    """
    chapters = chapters[:]
    random.shuffle(chapters)
    ket_qua = {c: {"vd": 0, "vdc": 0} for c in chapters}

    def tong(c):
        return ket_qua[c]["vd"] + ket_qua[c]["vdc"]

    def con_cho(c):
        return max_per_chuong is None or tong(c) < max_per_chuong

    # Bước 1 — VDC
    i, con, an_toan = 0, so_vdc, 0
    gioi_han = (so_vdc + so_vd + 1) * len(chapters) * 2 + 20
    while con > 0 and an_toan < gioi_han:
        an_toan += 1
        c = chapters[i % len(chapters)]
        i += 1
        if ket_qua[c]["vdc"] == 0 and con_cho(c):
            ket_qua[c]["vdc"] += 1
            con -= 1

    vdc_chapters = {c for c in chapters if ket_qua[c]["vdc"] > 0}
    other_chapters = [c for c in chapters if c not in vdc_chapters]

    # Bước 2 — VD, ưu tiên chương khác
    con = so_vd
    for c in other_chapters:
        if con <= 0:
            break
        if con_cho(c):
            ket_qua[c]["vd"] += 1
            con -= 1

    # Bước 3 — hết chỗ trống mới quay lại chương đã đầy (chấp nhận vượt cap)
    fallback = [c for c in chapters if con_cho(c)] or chapters
    idx, an_toan = 0, 0
    while con > 0 and an_toan < gioi_han:
        an_toan += 1
        if not fallback:
            fallback = chapters
        c = fallback[idx % len(fallback)]
        idx += 1
        ket_qua[c]["vd"] += 1
        con -= 1
        fallback = [x for x in fallback if con_cho(x)] or chapters

    return {c: v for c, v in ket_qua.items() if v["vd"] > 0 or v["vdc"] > 0}


def _tach_theo_ti_le(n: int, ti_le: list[float]) -> list[int]:
    """Chia n câu cho các nhóm theo tỉ lệ (vd [0.3, 0.7]), làm tròn ngẫu
    nhiên (trung bình nhiều đề đúng tỉ lệ). Tổng luôn bằng n."""
    if n <= 0:
        return [0] * len(ti_le)
    tong = sum(ti_le) or 1
    kq = _lam_tron_ngau_nhien({i: n * t / tong for i, t in enumerate(ti_le)}, n)
    return [kq[i] for i in range(len(ti_le))]


def _chuong_cua_bai(bai_id: str):
    cb = _tach_chuong_bai(bai_id)
    return cb[0] if cb else None


def _bai_cho_dung_sai(nhom_bai: list[tuple[float, list[str]]],
                      danh_sach_bai: list[str], so_cau_lon: int) -> list[str]:
    """Bài được phép đặt câu Đúng/Sai.

    Cô Lan chốt 29/09/2026: đề CUỐI KỲ thì câu Đúng/Sai chỉ đặt ở CHƯƠNG
    CHƯA KIỂM TRA ở thi giữa kỳ. Ưu tiên chương mà MỌI bài đều sau giữa
    kỳ; nếu số chương ấy ít hơn số câu Đúng/Sai (hai câu Đúng/Sai phải ở
    hai chương khác nhau) thì mới lấy thêm chương có một phần sau giữa kỳ,
    và chỉ lấy các bài SAU giữa kỳ của chương đó.
    Đề không chia hai phần (giữa kỳ, hệ số 1) -> mọi bài.
    """
    if len(nhom_bai) < 2:
        return list(danh_sach_bai)
    truoc = set(nhom_bai[0][1])
    sau = [b for b in danh_sach_bai if b not in truoc]
    chuong_truoc = {_chuong_cua_bai(b) for b in truoc}
    sach = [b for b in sau if _chuong_cua_bai(b) not in chuong_truoc]
    so_chuong_sach = len({_chuong_cua_bai(b) for b in sach})
    if so_chuong_sach >= so_cau_lon and sach:
        return sach
    return sau or list(danh_sach_bai)


_DON_VI_PATTERN = re.compile(r"_(?:NB|TH|VD|VDC)(\d+[A-Z]?)$")


def _don_vi_kien_thuc(curriculum_id: str) -> str:
    """
    Khoá "đơn vị kiến thức": bỏ mức độ ra khỏi Curriculum ID.

        L10_C1_B2_TH021  ->  L10_C1_B2_021
        L10_C1_B2_VD021  ->  L10_C1_B2_021

    Quy ước của ngân hàng: CÙNG một đơn vị kiến thức thì CÙNG số, chỉ khác
    mức độ. Nếu một đề lấy cả hai mức của cùng một số thì hai câu sẽ cùng
    một dạng toán, chỉ khác độ khó -- nhìn vào là thấy trùng.

    Vì vậy khi đã dùng một mức của đơn vị nào thì không lấy mức còn lại của
    chính đơn vị đó nữa, trừ khi đã hết sạch lựa chọn khác (vòng 2).
    """
    return _DON_VI_PATTERN.sub(lambda m: "_" + m.group(1), curriculum_id)


def _don_ve_bai_co_cau(phan_bo_bai: dict[str, int],
                       theo_bai_muc_do: dict, muc_do: str,
                       danh_sach_bai: list[str] | None = None,
                       so_tiet_theo_bai: dict[str, int] | None = None) -> tuple[dict[str, int], int]:
    """Dồn số câu đã chia cho BÀI KHÔNG CÓ yêu cầu nào ở mức độ này sang bài có.

    Vì sao cần: số câu được chia về từng bài theo TỈ LỆ SỐ TIẾT, hoàn toàn
    không biết bài đó trong Curriculum có yêu cầu nào ở mức độ đang xét hay
    không. Ví dụ chương 3 lớp 10 chỉ có ĐÚNG MỘT yêu cầu mức NB và nó nằm ở
    bài 5; nhưng ma trận lại chia 2 câu NB cho bài 6. Bài 6 không có yêu cầu
    NB nào nên _chon_curriculum_id trả về rỗng, và hai câu ấy BIẾN MẤT lặng
    lẽ - đề ra thiếu câu mà không báo gì (đo được: đề hệ số 1 chương 3 chỉ
    có 5 câu trong khi ma trận đòi 12).

    Nay: phần của bài không có yêu cầu được dồn sang các bài có, chia theo
    tỉ lệ số câu sẵn có. Trả về (phân bổ mới, số câu KHÔNG dồn được đi đâu).
    """
    co_cau = {b: sl for b, sl in phan_bo_bai.items()
              if theo_bai_muc_do.get((b, muc_do))}
    khong_co = sum(sl for b, sl in phan_bo_bai.items()
                   if not theo_bai_muc_do.get((b, muc_do)))
    if khong_co == 0:
        return dict(phan_bo_bai), 0
    if not co_cau:
        # Không bài nào TRONG PHÂN BỔ có yêu cầu ở mức độ này. Mở rộng ra
        # mọi bài thuộc phạm vi đề: bài có yêu cầu nhưng không được chia
        # câu nào vẫn là chỗ dồn hợp lệ. (Thiếu bước này thì chương 3 mất
        # câu trắc nghiệm mức VD, vì cả suất VD rơi vào bài 5 trong khi
        # yêu cầu mức VD duy nhất nằm ở bài 6.)
        co_cau = {b: 0 for b in (danh_sach_bai or [])
                  if theo_bai_muc_do.get((b, muc_do))}
    if not co_cau:
        # cả chương thật sự không có yêu cầu nào ở mức độ này
        return {}, khong_co

    # CHIA LẠI TOÀN BỘ số câu của mức độ này theo tỉ lệ số tiết, nhưng
    # chỉ trên những bài THẬT SỰ có yêu cầu ở mức độ ấy.
    #
    # SỬA 28/09/2026. Cách cũ dồn phần thừa cho bài đang được chia nhiều
    # câu nhất - mà bài ấy gần như luôn là bài của chương đầu (nhiều tiết
    # nhất, lại nhiều yêu cầu nhất), nên chương đầu càng ngày càng phình.
    # Đo được ở đề giữa kỳ 1: chương 1 chiếm 62% số câu trong khi chỉ
    # chiếm 36% số tiết.
    #
    # Chia lại theo số tiết thì phần của bài không có yêu cầu được san
    # đều theo đúng quy định "bài dạy nhiều tiết hơn thì nhiều câu hơn",
    # thay vì dồn hết vào một bài.
    tong_cau = sum(phan_bo_bai.values())
    if so_tiet_theo_bai:
        tiet_hop_le = {b: so_tiet_theo_bai.get(b, 1) for b in co_cau}
        return _chia_theo_so_tiet(tong_cau, tiet_hop_le), 0

    thu_tu = sorted(co_cau, key=lambda b: co_cau[b])
    i = 0
    while khong_co > 0:
        co_cau[thu_tu[i % len(thu_tu)]] += 1
        khong_co -= 1
        i += 1
    return co_cau, 0


def _don_vd_ve_bai_co_cau(phan_bo_vdvdc: dict[str, dict],
                          theo_bai_muc_do: dict,
                          danh_sach_bai: list[str] | None = None,
                          cap: int | None = None) -> tuple[dict[str, dict], int]:
    """Như _don_ve_bai_co_cau nhưng cho khối VD/VDC (trắc nghiệm, trả lời
    ngắn, tự luận). Cùng một lỗi: chương 3 lớp 10 chỉ có yêu cầu mức VD ở
    bài 6, nhưng _phan_bo_vd_vdc vẫn chia câu cho bài 5 - những câu ấy rơi
    mất, không báo thiếu. Đo được: đề hệ số 1 chương 3 mất 1 câu trả lời
    ngắn và 2 câu tự luận vì lý do này.
    """
    co = {b: dict(v) for b, v in phan_bo_vdvdc.items()
          if theo_bai_muc_do.get((b, "VD"))}
    du_vd = sum(v["vd"] for b, v in phan_bo_vdvdc.items()
                if not theo_bai_muc_do.get((b, "VD")))
    du_vdc = sum(v["vdc"] for b, v in phan_bo_vdvdc.items()
                 if not theo_bai_muc_do.get((b, "VD")))
    if du_vd == 0 and du_vdc == 0:
        return {b: dict(v) for b, v in phan_bo_vdvdc.items()}, 0

    # CHIA LẠI toàn bộ số câu VD/VDC trên MỌI bài thuộc phạm vi đề mà
    # thật sự có yêu cầu mức VD, thay vì chỉ dồn quanh những bài đã được
    # chia sẵn.
    #
    # SỬA 28/09/2026. Cách cũ chỉ dồn trong đám bài ĐÃ CÓ trong phân bổ.
    # Đề giữa kỳ 1 lớp 10 có bốn bài mang yêu cầu mức VD (B1, B2, B4,
    # B6), nhưng phân bổ ban đầu chỉ chạm tới B1, nên cả bốn câu trả lời
    # ngăn dồn hết về B1; mà quy ước là mỗi bài tối đa MỘT câu VDC, nên
    # câu thứ tư rơi mất. Đo được: 3/20 đề giữa kỳ chỉ ra 20 câu thay vì
    # 21, luôn hụt đúng một câu trả lời ngắn.
    hop_le = [b for b in (danh_sach_bai or list(phan_bo_vdvdc))
              if theo_bai_muc_do.get((b, "VD"))]
    if not hop_le:
        return {}, du_vd + du_vdc

    tong_vd = sum(v["vd"] for v in phan_bo_vdvdc.values())
    tong_vdc = sum(v["vdc"] for v in phan_bo_vdvdc.values())
    moi_phan_bo = _phan_bo_vd_vdc(hop_le, tong_vd, tong_vdc,
                                  max_per_chuong=cap)
    da_xep = sum(v["vd"] + v["vdc"] for v in moi_phan_bo.values())
    return moi_phan_bo, (tong_vd + tong_vdc) - da_xep


def _chon_curriculum_id(entries_muc_do: list[dict], so_luong: int, da_dung: set,
                        dem_dung: Counter | None = None) -> list[dict]:
    """
    Chọn so_luong Curriculum entries (không nhất thiết distinct nếu hết
    lựa chọn) từ danh sách entries CÙNG 1 mức độ trong 1 chương.

    Quy tắc (doc 08_CODE_NODES.md, mục CN_BuildBlueprint bước 4):
    - Ưu tiên rải ĐỀU giữa các bài (không dồn hết vào 1 bài).
    - Không lặp ĐƠN VỊ KIẾN THỨC nếu còn lựa chọn khác (da_dung) -- kể cả
      khi hai bản ghi khác mức độ nhưng cùng số (L10_C1_B2_TH021 và
      L10_C1_B2_VD021 là cùng một đơn vị, không lấy cả hai).
    - Chỉ lặp khi đã dùng hết toàn bộ competency khác trong đề hiện tại.
    - SỬA 30/09/2026 (cô Lan): da_dung và dem_dung DÙNG CHUNG cho cả ba loại
      câu MC / SA / TL. MC đã lấy đơn vị 014 thì SA phải lấy đơn vị khác, trừ
      khi hết. Khi buộc phải lặp (vòng 2) thì lấy đơn vị ĐANG DÙNG ÍT NHẤT
      (ngẫu nhiên giữa các đơn vị bằng nhau), không dồn vào một đơn vị.
    """
    if dem_dung is None:
        dem_dung = Counter()
    if so_luong <= 0 or not entries_muc_do:
        return []

    theo_bai: dict[str, list[dict]] = {}
    for e in entries_muc_do:
        theo_bai.setdefault(e["bai_so"], []).append(e)

    danh_sach_bai = list(theo_bai.keys())
    random.shuffle(danh_sach_bai)
    for ds in theo_bai.values():
        random.shuffle(ds)

    chon: list[dict] = []
    con_thieu = so_luong

    # Vòng 1 — rải đều theo bài, ưu tiên competency CHƯA dùng trong đề
    while con_thieu > 0:
        lay_duoc_vong_nay = False
        for bai in danh_sach_bai:
            if con_thieu <= 0:
                break
            ung_vien = [
                e for e in theo_bai[bai]
                if _don_vi_kien_thuc(e["id"]) not in da_dung and e not in chon
            ]
            if ung_vien:
                e = ung_vien[0]
                chon.append(e)
                da_dung.add(_don_vi_kien_thuc(e["id"]))
                dem_dung[_don_vi_kien_thuc(e["id"])] += 1
                con_thieu -= 1
                lay_duoc_vong_nay = True
        if not lay_duoc_vong_nay:
            break  # hết competency chưa dùng ở mức này -> sang vòng 2

    # Vòng 2 — hết lựa chọn mới, chấp nhận lặp lại: lấy đơn vị DÙNG ÍT NHẤT
    while con_thieu > 0:
        it_nhat = min(dem_dung[_don_vi_kien_thuc(e["id"])] for e in entries_muc_do)
        e = random.choice([e for e in entries_muc_do
                           if dem_dung[_don_vi_kien_thuc(e["id"])] == it_nhat])
        chon.append(e)
        dem_dung[_don_vi_kien_thuc(e["id"])] += 1
        con_thieu -= 1

    return chon


# ============================================================
# CN_BuildBlueprint
# ============================================================

def build_blueprint(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
) -> dict:
    # BƯỚC 1 — xác định phạm vi bài (CN_LoadExamScope)
    if loai_he_so == "HeSo1":
        if not pham_vi_chuong:
            raise BlueprintError("Thiếu pham_vi_chuong cho HeSo1")
        scope = load_scope_heso1(lop, pham_vi_chuong)
        pham_vi_bai = scope["pham_vi_bai"]
    elif loai_he_so == "HeSo2_HeSo3":
        if not ki_thi:
            raise BlueprintError("Thiếu ki_thi cho HeSo2_HeSo3")
        scope = load_scope_heso23(lop, ki_thi)
        if "error" in scope:
            raise BlueprintError(scope["error"])
        pham_vi_bai = scope["pham_vi_bai"]
    else:
        raise BlueprintError(f"loai_he_so '{loai_he_so}' không hợp lệ")

    so_bai_theo_chuong = _dem_so_bai_theo_chuong(pham_vi_bai)
    if not so_bai_theo_chuong:
        raise BlueprintError("Không xác định được chương nào trong phạm vi bài")
    danh_sach_chuong = list(so_bai_theo_chuong.keys())

    # Số tiết từng bài do CN_LoadExamScope đọc sẵn từ PPCT (blueprint
    # KHÔNG được đọc PPCT - doc 08). Bài thiếu dữ liệu tính 1 tiết.
    so_tiet_theo_bai = scope.get("so_tiet_theo_bai") or {}
    so_tiet_theo_bai = {b: so_tiet_theo_bai.get(b, 1) for b in pham_vi_bai}
    danh_sach_bai = list(so_tiet_theo_bai.keys())

    # Đề CUỐI KỲ: 30% số câu lấy từ phần trước giữa kỳ, 70% từ phần sau
    # (CN_LoadExamScope đã tách sẵn trong phan_bo_ty_le). SỬA 29/09/2026:
    # trước đây blueprint BỎ QUA phan_bo_ty_le, chia theo số tiết cả học
    # kỳ - đo được đề cuối kỳ 1 lớp 10 lấy 60% số câu ở phần trước giữa kỳ.
    # Đề giữa kỳ / hệ số 1: một nhóm duy nhất, tỉ lệ 1.
    pbtl = scope.get("phan_bo_ty_le") if isinstance(scope, dict) else None
    if pbtl:
        nhom_bai = []
        for khoa in ("truoc_giua_ky", "sau_giua_ky"):
            ds = [b for b in pbtl[khoa]["pham_vi_bai"] if b in so_tiet_theo_bai]
            if ds:
                nhom_bai.append((float(pbtl[khoa]["ti_le"]), ds))
    else:
        nhom_bai = [(1.0, danh_sach_bai)]

    # BƯỚC 2 — số câu mỗi mức độ theo hệ số (bảng exam_rules.json)
    try:
        rules_result = resolve_cau_truc_de(loai_he_so, cau_truc_tu_hoc_sinh)
    except ExamRulesError as e:
        raise BlueprintError(str(e))
    phan_bo_muc_do = rules_result["phan_bo_muc_do"]

    # BƯỚC 3 — đọc Curriculum đúng phạm vi bài (CN_LoadCurriculum),
    # group theo (chương, MucDo)
    try:
        curriculum_entries = load_curriculum_for_scope(lop, pham_vi_bai)
    except CurriculumError as e:
        raise BlueprintError(f"CURRICULUM_NOT_FOUND: {e}")
    if not curriculum_entries:
        raise BlueprintError("CURRICULUM_NOT_FOUND")

    # Group Curriculum theo (bài, mức độ) - trước đây group theo (chương,
    # mức độ). Đổi vì mọi phân bổ giờ làm ở cấp BÀI (đơn vị kiến thức).
    theo_bai_muc_do: dict[tuple, list[dict]] = {}
    for e in curriculum_entries:
        bai_id = f"L{lop}_C{int(e['chuong_so'])}_B{int(e['bai_so'])}"
        theo_bai_muc_do.setdefault((bai_id, e["MucDo"]), []).append(e)

    # "Đã dùng" DÙNG CHUNG cho MC / SA / TL (sửa 30/09/2026, cô Lan): MC đã lấy
    # đơn vị kiến thức 014 thì SA, TL phải lấy đơn vị khác, trừ khi hết lựa
    # chọn. Trước đây tách riêng theo loại câu nên SA hay lấy lại đúng đơn vị
    # của MC, đề ra nhiều câu na ná nhau.
    _chung, _dem = set(), Counter()
    da_dung: dict[str, set] = {"trac_nghiem": _chung, "tra_loi_ngan": _chung, "tu_luan": _chung}
    dem_dung: Counter = _dem
    blueprint = {"dung_sai": [], "trac_nghiem": [], "tra_loi_ngan": [], "tu_luan": []}
    bao_cao_phan_bo: dict = {}

    # ---- BƯỚC 4a — Đúng/Sai LÀM TRƯỚC TIÊN (quy định của giáo viên) ----
    # Chọn BÀI cho câu Đúng/Sai trước, vì mỗi câu Đúng/Sai chiếm sẵn
    # 1 NB + 1 TH + 1 VD + 1 VDC ngay tại bài đó; các phần còn lại chia
    # sau và phải trừ đi phần đã bị chiếm này.
    so_cau_lon = phan_bo_muc_do.get("dung_sai_cau_lon", {}).get("NB", 0)  # 4 mức bằng nhau
    bai_ds_hop_le = _bai_cho_dung_sai(nhom_bai, danh_sach_bai, so_cau_lon)
    # Câu Đúng/Sai của đề cuối kỳ nằm hết ở phần SAU giữa kỳ, nên nâng nhẹ
    # tỉ lệ phần TRƯỚC ở các phần còn lại để CẢ ĐỀ (tính theo số câu) vẫn
    # đúng 30/70.
    if len(nhom_bai) == 2 and so_cau_lon > 0:
        tong_cau = so_cau_lon + sum(
            sum(v for k, v in phan_bo_muc_do.get(l, {}).items())
            for l in ("trac_nghiem", "tra_loi_ngan", "tu_luan"))
        con_lai = tong_cau - so_cau_lon
        if con_lai > 0:
            t0 = min(1.0, nhom_bai[0][0] * tong_cau / con_lai)
            nhom_bai = [(t0, nhom_bai[0][1]), (1.0 - t0, nhom_bai[1][1])]
    phan_bo_bai_ds = _chon_bai_dung_sai(
        {b: so_tiet_theo_bai[b] for b in bai_ds_hop_le}, so_cau_lon)
    bao_cao_phan_bo["dung_sai_cau_lon"] = {"theo_bai": phan_bo_bai_ds}
    for bai_id, sl in phan_bo_bai_ds.items():
        cb = _tach_chuong_bai(bai_id)
        blueprint["dung_sai"].append({
            "chuong_so": cb[0] if cb else None,
            "bai_so": cb[1] if cb else None,
            "bai_id": bai_id,
            "so_cau": sl,
        })

    # ---- BƯỚC 4b — mức NB, TH của MC, SA, TL: chia về BÀI theo TỈ LỆ SỐ TIẾT ----
    # SỬA 30/09/2026: trước đây chỉ làm cho trắc nghiệm, nên ma trận ghi câu
    # trả lời ngắn / tự luận ở mức NB, TH (vd 1 SA + 1 TL mức TH) bị BỎ MẤT,
    # đề ra thiếu câu mà không báo. Thứ tự MC -> SA -> TL để SA, TL tránh
    # các đơn vị kiến thức MC đã lấy.
    for muc_do, loai_nbth in [(m, l) for m in ("NB", "TH")
                              for l in ("trac_nghiem", "tra_loi_ngan", "tu_luan")]:
        so_luong = phan_bo_muc_do.get(loai_nbth, {}).get(muc_do, 0)
        if so_luong <= 0 and loai_nbth != "trac_nghiem":
            continue
        # KHÔNG trừ phần Đúng/Sai ra khỏi ngân sách NB/TH của trắc nghiệm.
        # Cô Lan chốt 28/09/2026: "cứ làm theo đúng mức độ là được, vì mức độ
        # ảnh hưởng điểm số - mức độ khác đi sẽ làm điểm số không phản ánh
        # đúng cái người kiểm tra mong muốn". Mỗi phần phải ra ĐÚNG số câu
        # từng mức độ mà ma trận ghi, không bù trừ chéo giữa các phần.
        # (_tru_phan_dung_sai giữ lại để tham khảo, không còn được gọi.)
        # Chia số câu cho từng NHÓM (30/70 với đề cuối kỳ), rồi trong
        # nhóm chia theo tỉ lệ số tiết. Nhóm nào không có yêu cầu ở mức
        # này thì phần của nó chuyển sang nhóm sau (không để rơi câu).
        phan_bo_bai, mat_cau = {}, 0
        chia_nhom = _tach_theo_ti_le(so_luong, [t for t, _ in nhom_bai])
        for (_t, ds_bai_nhom), sl_nhom in zip(nhom_bai, chia_nhom):
            sl_nhom += mat_cau
            tiet_nhom = {b: so_tiet_theo_bai[b] for b in ds_bai_nhom}
            pb = _chia_theo_so_tiet(sl_nhom, tiet_nhom)
            pb, mat_cau = _don_ve_bai_co_cau(
                pb, theo_bai_muc_do, muc_do, ds_bai_nhom, tiet_nhom)
            for b, k in pb.items():
                phan_bo_bai[b] = phan_bo_bai.get(b, 0) + k
        if mat_cau:
            # nhóm cuối cũng không có -> thử cả phạm vi như trước đây
            pb, mat_cau = _don_ve_bai_co_cau(
                _chia_theo_so_tiet(mat_cau, so_tiet_theo_bai), theo_bai_muc_do,
                muc_do, danh_sach_bai, so_tiet_theo_bai)
            for b, k in pb.items():
                phan_bo_bai[b] = phan_bo_bai.get(b, 0) + k
        bao_cao_phan_bo.setdefault(loai_nbth, {})[muc_do] = phan_bo_bai
        if mat_cau:
            bao_cao_phan_bo.setdefault("khong_du_yeu_cau", []).append(
                {"loai_cau": loai_nbth, "muc_do": muc_do, "so_cau_mat": mat_cau})
        for bai_id, sl in phan_bo_bai.items():
            cb = _tach_chuong_bai(bai_id)
            entries = theo_bai_muc_do.get((bai_id, muc_do), [])
            chon = _chon_curriculum_id(entries, sl, da_dung[loai_nbth], dem_dung)
            for e in chon:
                blueprint[loai_nbth].append({
                    "curriculum_id": e["id"],
                    "chuong_so": cb[0] if cb else None,
                    "bai_so": cb[1] if cb else None,
                    "muc_do": muc_do,
                    "tong_so_cau": 1,
                })

    # ---- trac_nghiem / tra_loi_ngan / tu_luan mức VD (+VDC dùng chung
    # curriculum_id mức VD — Ngoại lệ 2, doc 04) ----
    gioi_han_theo_loai = {
        "trac_nghiem": None,
        "tra_loi_ngan": MAX_SA_PER_CHUONG,
        "tu_luan": MAX_TL_PER_CHUONG,
    }
    # Câu Đúng/Sai KHÔNG trừ vào ngân sách VD/VDC của các phần khác.
    # Cô Lan chốt 28/09/2026: mức độ quyết định điểm số nên mỗi phần phải ra
    # đúng số câu từng mức độ ma trận ghi. Trước đây mỗi câu Đúng/Sai ăn
    # 1 suất VD + 1 suất VDC của phần đứng trước, làm đề chương 3 mất cả
    # câu trắc nghiệm mức VD lẫn câu trả lời ngắn mức VDC.
    for loai_cau, cap in gioi_han_theo_loai.items():
        so_vd = phan_bo_muc_do.get(loai_cau, {}).get("VD", 0)
        so_vdc = phan_bo_muc_do.get(loai_cau, {}).get("VDC", 0)

        if so_vd <= 0 and so_vdc <= 0:
            continue

        # Rải trên BÀI (đơn vị kiến thức) chứ không phải chương: mỗi bài
        # tối đa 1 câu VDC, câu VD ưu tiên bài chưa có VDC.
        phan_bo_chuong_vdvdc, mat_vd = {}, 0
        ti_le_nhom = [t for t, _ in nhom_bai]
        chia_vd = _tach_theo_ti_le(so_vd, ti_le_nhom)
        chia_vdc = _tach_theo_ti_le(so_vdc, ti_le_nhom)
        du_vd = du_vdc = 0
        for (_t, ds_bai_nhom), vd_n, vdc_n in zip(nhom_bai, chia_vd, chia_vdc):
            vd_n += du_vd
            vdc_n += du_vdc
            if vd_n <= 0 and vdc_n <= 0:
                continue
            pb = _phan_bo_vd_vdc(ds_bai_nhom, vd_n, vdc_n, max_per_chuong=cap)
            pb, mat = _don_vd_ve_bai_co_cau(pb, theo_bai_muc_do, ds_bai_nhom, cap)
            if mat and pb == {}:
                # nhóm không có yêu cầu mức VD nào -> dồn sang nhóm sau
                du_vd, du_vdc = vd_n, vdc_n
                continue
            du_vd = du_vdc = 0
            mat_vd += mat
            for b, v in pb.items():
                cu = phan_bo_chuong_vdvdc.setdefault(b, {"vd": 0, "vdc": 0})
                cu["vd"] += v["vd"]
                cu["vdc"] += v["vdc"]
        if du_vd or du_vdc:
            pb = _phan_bo_vd_vdc(danh_sach_bai, du_vd, du_vdc, max_per_chuong=cap)
            pb, mat = _don_vd_ve_bai_co_cau(pb, theo_bai_muc_do, danh_sach_bai, cap)
            mat_vd += mat
            for b, v in pb.items():
                cu = phan_bo_chuong_vdvdc.setdefault(b, {"vd": 0, "vdc": 0})
                cu["vd"] += v["vd"]
                cu["vdc"] += v["vdc"]
        bao_cao_phan_bo.setdefault(loai_cau, {})["vd_vdc"] = phan_bo_chuong_vdvdc
        if mat_vd:
            bao_cao_phan_bo.setdefault("khong_du_yeu_cau", []).append(
                {"loai_cau": loai_cau, "muc_do": "VD/VDC", "so_cau_mat": mat_vd})

        for bai_id, v in phan_bo_chuong_vdvdc.items():
            cb = _tach_chuong_bai(bai_id)
            chuong_so = cb[0] if cb else None
            tong = v["vd"] + v["vdc"]
            if tong <= 0:
                continue

            entries_vd = theo_bai_muc_do.get((bai_id, "VD"), [])
            chon = _chon_curriculum_id(entries_vd, tong, da_dung[loai_cau], dem_dung)

            # Gộp theo curriculum_id (nếu vòng lặp bên trên phải lặp lại
            # 1 competency do hết lựa chọn khác), rồi chia VD/VDC theo
            # chỉ tiêu còn lại — curriculum_id GIỮ NGUYÊN, không đổi thành VDC.
            dem = Counter(e["id"] for e in chon)
            vdc_con, vd_con = v["vdc"], v["vd"]
            for curriculum_id, so_luong_id in dem.items():
                so_vdc_id = min(so_luong_id, vdc_con)
                vdc_con -= so_vdc_id
                so_vd_id = so_luong_id - so_vdc_id
                vd_con -= so_vd_id
                blueprint[loai_cau].append({
                    "curriculum_id": curriculum_id,
                    "chuong_so": chuong_so,
                    "bai_so": cb[1] if cb else None,
                    "muc_do": "VD",
                    "tong_so_cau": so_luong_id,
                    "so_cau_VD": so_vd_id,
                    "so_cau_VDC": so_vdc_id,
                })

    return {
        "pham_vi_bai": pham_vi_bai,
        "so_bai_theo_chuong": so_bai_theo_chuong,
        "so_tiet_theo_bai": so_tiet_theo_bai,
        "cau_truc_tong_quat": rules_result["cau_truc_tong_quat"],
        "nguon_cau_truc": rules_result["nguon_cau_truc"],
        "bao_cao_phan_bo": bao_cao_phan_bo,
        **blueprint,
    }


def build_and_select(
    lop: int,
    loai_he_so: str,
    ki_thi: str | None = None,
    pham_vi_chuong: str | None = None,
    cau_truc_tu_hoc_sinh: dict | None = None,
    cho_phep_thieu: bool = True,
) -> dict:
    """
    Ghép build_blueprint() + select_questions() (chế độ chính thức, theo
    curriculum_id) thành 1 bước — dùng cho luồng WF001 đầy đủ.

    cho_phep_thieu=True: chế độ NHÁP, dùng khi ngân hàng đề (Mapping/
    Python Generator) chưa đầy đủ — thiếu ở đâu sẽ đánh dấu "thieu": True
    trong danh_sach_generator_id thay vì dừng hẳn. KHÔNG dùng khi ra đề
    thật cho học sinh (xem question_selector_service.py).
    """
    blueprint = build_blueprint(
        lop=lop,
        loai_he_so=loai_he_so,
        ki_thi=ki_thi,
        pham_vi_chuong=pham_vi_chuong,
        cau_truc_tu_hoc_sinh=cau_truc_tu_hoc_sinh,
    )

    try:
        danh_sach_id = select_questions(lop=lop, blueprint=blueprint, cho_phep_thieu=cho_phep_thieu)
    except SelectorError as e:
        raise BlueprintError(str(e))

    blueprint["danh_sach_generator_id"] = danh_sach_id
    return blueprint