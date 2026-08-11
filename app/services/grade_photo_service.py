"""
CN_GradeAnswer (nhanh ANH) - cham bai bang cach goi 2 webhook n8n:
- DocPhieuTraLoi (doc-phieu-tra-loi): doc anh Phieu TLTN (MC/TF/SA).
- CHV_Grader (cham-tu-luan): doc anh bai lam tay (Tu luan that su).

GHI CHU QUAN TRONG (bug da biet, hoan lai xu ly sau theo yeu cau):
answer_parser_service.trich_dap_an() CHUA nhan dien duoc cau Dung/Sai
(TF, dung \\choiceTFn/\\choiceTFt) -> moi cau TF hien dang bi luu nham
loai_cau="TL", dap_an_dung=None trong file *_dapan.json. Ham duoi day
dung generator_id (chua "_TF_") de tach rieng cau TF ra khoi cau TL
that su, nhung VAN CHUA the tu cham dung/sai cho TF (vi khong co dap
an dung de so sanh) -> cau TF luon tra ve trang_thai="can_cham_tay".
"""
import httpx

from app.core.config import N8N_WEBHOOK_DOC_PHIEU, N8N_WEBHOOK_CHAM_TU_LUAN
from app.services.mapping_service import trich_chuong_bai


class GradePhotoError(Exception):
    pass


def _goi_webhook(url: str | None, payload: dict, ten_buoc: str) -> dict:
    if not url:
        raise GradePhotoError(f"Chua cau hinh URL webhook cho {ten_buoc} (thieu bien moi truong).")
    try:
        resp = httpx.post(url, json=payload, timeout=60.0)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        raise GradePhotoError(f"Loi goi webhook {ten_buoc}: {e}")
    try:
        return resp.json()
    except Exception as e:
        raise GradePhotoError(f"Webhook {ten_buoc} tra ve khong phai JSON hop le: {e}")


def _la_cau_tf(cau: dict) -> bool:
    """TF hien bi luu nham loai_cau='TL' (xem docstring dau file).
    Phan biet bang generator_id co chua '_TF_'."""
    generator_id = cau.get("generator_id") or ""
    return "_TF_" in generator_id


def cham_bai_bang_anh(
    danh_sach_dap_an: list[dict],
    anh_phieu_base64: str | None,
    anh_tuluan_base64: str | None,
) -> dict:
    tong_so_cau = len(danh_sach_dap_an)
    diem_moi_cau = round(10 / tong_so_cau, 2) if tong_so_cau else 0.0

    mc_list = [c for c in danh_sach_dap_an if c.get("loai_cau") == "MC"]
    sa_list = [c for c in danh_sach_dap_an if c.get("loai_cau") == "SA"]
    tf_list = [c for c in danh_sach_dap_an if c.get("loai_cau") == "TL" and _la_cau_tf(c)]
    tl_list = [c for c in danh_sach_dap_an if c.get("loai_cau") == "TL" and not _la_cau_tf(c)]

    ket_qua_theo_stt: dict[int, dict] = {}

    # ---- Nhanh 1: Phieu tra loi (MC/TF/SA) qua DocPhieuTraLoi ----
    if anh_phieu_base64 and (mc_list or tf_list or sa_list):
        so_luong = {"mc": len(mc_list), "tf": len(tf_list), "sa": len(sa_list)}
        doc_phieu = _goi_webhook(
            N8N_WEBHOOK_DOC_PHIEU,
            {"anh_base64": anh_phieu_base64, "so_luong": so_luong},
            "doc-phieu-tra-loi",
        )

        for vi_tri, cau in enumerate(mc_list, start=1):
            generator_id = cau.get("generator_id")
            chuong, bai_so = trich_chuong_bai(generator_id)
            dap_an_doc = (doc_phieu.get("mc") or {}).get(str(vi_tri))
            dung = bool(
                dap_an_doc
                and (dap_an_doc or "").strip().upper() == (cau.get("dap_an_dung") or "").strip().upper()
            )
            ket_qua_theo_stt[cau["so_thu_tu"]] = {
                "question_id": generator_id,
                "loai_cau": "MC",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_moi_cau,
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": cau["so_thu_tu"],
                "dap_an_hoc_sinh": dap_an_doc,
                "dap_an_dung": cau.get("dap_an_dung"),
            }

        for vi_tri, cau in enumerate(sa_list, start=1):
            generator_id = cau.get("generator_id")
            chuong, bai_so = trich_chuong_bai(generator_id)
            dap_an_doc = (doc_phieu.get("sa") or {}).get(str(vi_tri))
            dung = bool(
                dap_an_doc
                and (dap_an_doc or "").strip().replace(" ", "").lower()
                == (cau.get("dap_an_dung") or "").strip().replace(" ", "").lower()
            )
            ket_qua_theo_stt[cau["so_thu_tu"]] = {
                "question_id": generator_id,
                "loai_cau": "SA",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_moi_cau,
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": cau["so_thu_tu"],
                "dap_an_hoc_sinh": dap_an_doc,
                "dap_an_dung": cau.get("dap_an_dung"),
            }

        for vi_tri, cau in enumerate(tf_list, start=1):
            generator_id = cau.get("generator_id")
            chuong, bai_so = trich_chuong_bai(generator_id)
            dap_an_doc = (doc_phieu.get("tf") or {}).get(str(vi_tri))
            ket_qua_theo_stt[cau["so_thu_tu"]] = {
                "question_id": generator_id,
                "loai_cau": "TF",
                "dung_sai_hoac_diem": None,
                "diem_toi_da": diem_moi_cau,
                "nhan_xet": (
                    "Cau Dung/Sai: da doc duoc bai lam nhung chua tu cham dung/sai "
                    "(answer_parser_service chua ho tro trich dap an dung TF). Can cham tay."
                ),
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": cau["so_thu_tu"],
                "trang_thai": "can_cham_tay",
                "dap_an_hoc_sinh": dap_an_doc,
            }

    # ---- Nhanh 2: Bai lam tu luan qua CHV_Grader ----
    if anh_tuluan_base64 and tl_list:
        danh_sach_cau_tl = []
        for cau in tl_list:
            generator_id = cau.get("generator_id")
            chuong, bai_so = trich_chuong_bai(generator_id)
            danh_sach_cau_tl.append({
                "question_id": generator_id,
                "bai": bai_so,
                "diem_toi_da": diem_moi_cau,
                "dap_an_mau": cau.get("loi_giai") or "",
                "chuong": chuong,
            })

        cham_tu_luan = _goi_webhook(
            N8N_WEBHOOK_CHAM_TU_LUAN,
            {"anh_base64": anh_tuluan_base64, "danh_sach_cau": danh_sach_cau_tl},
            "cham-tu-luan",
        )
        ket_qua_theo_generator_id = {kq.get("question_id"): kq for kq in cham_tu_luan}
        for cau in tl_list:
            generator_id = cau.get("generator_id")
            kq = ket_qua_theo_generator_id.get(generator_id)
            if kq is None:
                chuong, bai_so = trich_chuong_bai(generator_id)
                kq = {
                    "question_id": generator_id,
                    "loai_cau": "TL",
                    "dung_sai_hoac_diem": None,
                    "diem_toi_da": diem_moi_cau,
                    "nhan_xet": "CHV_Grader khong tra ve ket qua cho cau nay.",
                    "chuong": chuong,
                    "bai": bai_so,
                    "tags": [],
                    "trang_thai": "loi_cham",
                }
            kq["so_thu_tu"] = cau["so_thu_tu"]
            ket_qua_theo_stt[cau["so_thu_tu"]] = kq

    # ---- Cac cau chua duoc cham (thieu anh, hoac loai cau khac) ----
    for cau in danh_sach_dap_an:
        stt = cau["so_thu_tu"]
        if stt in ket_qua_theo_stt:
            continue
        generator_id = cau.get("generator_id")
        chuong, bai_so = trich_chuong_bai(generator_id)
        ket_qua_theo_stt[stt] = {
            "question_id": generator_id,
            "loai_cau": "TF" if _la_cau_tf(cau) else (cau.get("loai_cau") or "TL"),
            "dung_sai_hoac_diem": None,
            "diem_toi_da": diem_moi_cau,
            "nhan_xet": "Chua co anh de cham cau nay.",
            "chuong": chuong,
            "bai": bai_so,
            "tags": [],
            "so_thu_tu": stt,
            "trang_thai": "can_cham_tay",
        }

    chi_tiet = [ket_qua_theo_stt[stt] for stt in sorted(ket_qua_theo_stt)]

    tong_diem_dat = 0.0
    tong_diem_toi_da_da_cham = 0.0
    for kq in chi_tiet:
        gia_tri = kq.get("dung_sai_hoac_diem")
        if gia_tri is None:
            continue
        tong_diem_toi_da_da_cham += kq.get("diem_toi_da") or 0
        if isinstance(gia_tri, bool):
            tong_diem_dat += (kq.get("diem_toi_da") or 0) if gia_tri else 0
        else:
            tong_diem_dat += float(gia_tri)

    diem_tam_tinh = (
        round(tong_diem_dat / tong_diem_toi_da_da_cham * 10, 2)
        if tong_diem_toi_da_da_cham else 0.0
    )

    return {
        "tong_so_cau": tong_so_cau,
        "diem_tren_10_tam_tinh": diem_tam_tinh,
        "ghi_chu": (
            "Diem tam tinh chi tren cac cau da cham duoc (co dung_sai_hoac_diem "
            "khac null). Cau TF luon can cham tay (xem ghi chu dau file)."
        ),
        "chi_tiet": chi_tiet,
    }
