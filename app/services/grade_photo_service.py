"""
CN_GradeAnswer (nhanh ANH) - cham bai bang cach goi 2 webhook n8n:
- DocPhieuTraLoi (doc-phieu-tra-loi): doc anh Phieu TLTN (MC/TF/SA).
- CHV_Grader (cham-tu-luan): doc anh bai lam tay (Tu luan that su).

CAP NHAT 2026-09-04: ghi chu cu ("answer_parser_service chua nhan dien
duoc cau Dung/Sai") DA LOI THOI. Da kiem chung bang
tests/test_answer_parser_bank.py tren toan bo 46 generator that cua
data/python_bank/toan10/L10_C1.py: trich_dap_an() doc DUNG ca 4 loai cau,
cau TF duoc luu dung loai_cau="TF" kem dap_an_dung {a,b,c,d} day du.
(Bug \\choiceTFn[N] khong ton tai trong ex_test.sty da duoc sua o Version
2.27 - tu do generator luon sinh \\choiceTFt, dung dinh dang parser doc
duoc.)

CAP NHAT 21/10/2026 - DONG NHAT CAC TRUONG giua prompt n8n va Python (co
Lan: "dong nhat cac truong voi nhau, khong de mau thuan xay ra"; ban ghi
prompt: data/prompts/DocPhieuTraLoi.md, data/prompts/CHV_Grader.md):
- MOI truong ket qua do PYTHON dat (loai_cau MC/TF/SA/TL, diem_toi_da,
  chuong, bai, question_id). Tu AI chi lay dung phan no "doc" duoc: o hoc
  sinh to (DocPhieuTraLoi) va so diem + nhan xet (CHV_Grader). AI ghi
  "tu_luan" hay "TL", diem_toi_da dung hay sai deu khong anh huong.
- Diem CHV_Grader: doc khoa dung_sai_hoac_diem (chap nhan ca "diem"), ep
  ve so, chan trong [0; diem_toi_da], lam tron 0,25. Khong doc duoc ->
  None + trang_thai "loi_cham" (khong cong bua).
- Tra loi ngan: so bang chuan_hoa_dap_an_ngan (chung voi /grade): bo $,
  coi dau cham va dau phay thap phan nhu nhau.
- Cau Dung/Sai: nay CHAM luon tu phieu ("D"/"S" -> chuan_hoa_dap_an_tf),
  cung cach tinh diem theo so y dung nhu /grade (diem_service.diem_cau_tf).
- n8n tra JSON boc trong {"output": "..."} (mac dinh cua AI Agent) hay
  co ``` cung doc duoc (_boc_json).
Ca nhanh cham bang anh van dang tam dung tren giao dien (xem thong bao
"dang xay dung" o app/templates/chat/lam_bai.html).
"""
import json
import re

import httpx

from app.core.config import N8N_WEBHOOK_DOC_PHIEU, N8N_WEBHOOK_CHAM_TU_LUAN
from app.services.mapping_service import trich_chuong_bai
from app.services import diem_service
from app.services.answer_parser_service import chuan_hoa_dap_an_ngan, chuan_hoa_dap_an_tf


class GradePhotoError(Exception):
    pass


def _boc_json(du_lieu):
    """Lay phan JSON that tu cau tra loi cua n8n. Node AI Agent thuong tra
    {"output": "<chuoi JSON>"} (co khi boc trong mang mot phan tu, co khi
    kem ```json ... ```). Da la dict/list "that" thi giu nguyen."""
    for _ in range(3):
        if isinstance(du_lieu, list) and len(du_lieu) == 1 and isinstance(du_lieu[0], dict) \
                and set(du_lieu[0]) & {"output", "text", "message", "answer"}:
            du_lieu = du_lieu[0]
        if isinstance(du_lieu, dict):
            for khoa in ("output", "text", "message", "answer"):
                if khoa in du_lieu and len(du_lieu) <= 2:
                    du_lieu = du_lieu[khoa]
                    break
            else:
                return du_lieu
        if isinstance(du_lieu, str):
            chu = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", du_lieu.strip())
            try:
                du_lieu = json.loads(chu)
            except ValueError:
                raise GradePhotoError("AI tra ve khong phai JSON hop le: " + chu[:120])
        elif not isinstance(du_lieu, dict):
            return du_lieu
    return du_lieu


def _diem_tu_luan(kq: dict, diem_toi_da: float):
    """Diem CHV_Grader cham -> so trong [0; diem_toi_da], lam tron 0,25. None neu khong doc duoc."""
    gia_tri = kq.get("dung_sai_hoac_diem", kq.get("diem"))
    if isinstance(gia_tri, bool) or gia_tri is None:
        return None
    try:
        so = float(str(gia_tri).replace(",", ".").strip())
    except ValueError:
        return None
    so = min(max(so, 0.0), float(diem_toi_da or 0))
    return round(so * 4) / 4


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
    Phan biet bang generator_id co chua '_TF_'. Dung chung mot logic
    voi diem_service de thang diem va viec cham khong lech nhau."""
    return diem_service.loai_cau_chuan(cau) == "TF"


def cham_bai_bang_anh(
    danh_sach_dap_an: list[dict],
    anh_phieu_base64: str | None,
    anh_tuluan_base64: str | None,
) -> dict:
    tong_so_cau = len(danh_sach_dap_an)
    # Thang diem 10 dung chung voi POST /api/exam/grade:
    # MC 3d - TF 2d - SA 2d - TL 3d, chia deu trong tung phan
    # (xem app/services/diem_service.py + data/config/diem_rules.json).
    thang = diem_service.tinh_thang_diem(danh_sach_dap_an)
    diem_mc = diem_service.diem_toi_da_cua_cau(thang, "MC")
    diem_sa = diem_service.diem_toi_da_cua_cau(thang, "SA")
    diem_tf = diem_service.diem_toi_da_cua_cau(thang, "TF")

    mc_list = [c for c in danh_sach_dap_an if diem_service.loai_cau_chuan(c) == "MC"]
    sa_list = [c for c in danh_sach_dap_an if diem_service.loai_cau_chuan(c) == "SA"]
    tf_list = [c for c in danh_sach_dap_an if diem_service.loai_cau_chuan(c) == "TF"]
    tl_list = [c for c in danh_sach_dap_an if diem_service.loai_cau_chuan(c) == "TL"]

    ket_qua_theo_stt: dict[int, dict] = {}

    # ---- Nhanh 1: Phieu tra loi (MC/TF/SA) qua DocPhieuTraLoi ----
    if anh_phieu_base64 and (mc_list or tf_list or sa_list):
        so_luong = {"mc": len(mc_list), "tf": len(tf_list), "sa": len(sa_list)}
        doc_phieu = _boc_json(_goi_webhook(
            N8N_WEBHOOK_DOC_PHIEU,
            {"anh_base64": anh_phieu_base64, "so_luong": so_luong},
            "doc-phieu-tra-loi",
        ))
        if not isinstance(doc_phieu, dict):
            raise GradePhotoError("DocPhieuTraLoi khong tra ve dang {mc, tf, sa}.")

        for vi_tri, cau in enumerate(mc_list, start=1):
            generator_id = cau.get("generator_id")
            chuong, bai_so = trich_chuong_bai(generator_id)
            dap_an_doc = (doc_phieu.get("mc") or {}).get(str(vi_tri))
            dung = bool(
                dap_an_doc
                and str(dap_an_doc).strip().upper() == (cau.get("dap_an_dung") or "").strip().upper()
            )
            ket_qua_theo_stt[cau["so_thu_tu"]] = {
                "question_id": generator_id,
                "loai_cau": "MC",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_mc,
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
                dap_an_doc is not None
                and chuan_hoa_dap_an_ngan(str(dap_an_doc))
                and chuan_hoa_dap_an_ngan(str(dap_an_doc)) == chuan_hoa_dap_an_ngan(cau.get("dap_an_dung"))
            )
            ket_qua_theo_stt[cau["so_thu_tu"]] = {
                "question_id": generator_id,
                "loai_cau": "SA",
                "dung_sai_hoac_diem": dung,
                "diem_toi_da": diem_sa,
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
            dap_an_doc = dap_an_doc if isinstance(dap_an_doc, dict) else {}
            dap_an_dung_tf = cau.get("dap_an_dung")
            kq_tf = {
                "question_id": generator_id,
                "loai_cau": "TF",
                "diem_toi_da": diem_tf,
                "diem_moi_y": thang["theo_phan"]["TF"]["diem_moi_y"],
                "nhan_xet": "",
                "chuong": chuong,
                "bai": bai_so,
                "tags": [],
                "so_thu_tu": cau["so_thu_tu"],
                "dap_an_hoc_sinh": dap_an_doc,
                "dap_an_dung": dap_an_dung_tf,
            }
            if not isinstance(dap_an_dung_tf, dict) or not dap_an_dung_tf:
                kq_tf.update({
                    "dung_sai_hoac_diem": None,
                    "nhan_xet": "Cau Dung/Sai chua co dap an dung trong tep dap an cua de. Can cham tay.",
                    "trang_thai": "can_cham_tay",
                })
            else:
                # Cung cach cham voi POST /api/exam/grade: diem theo so y dung.
                chi_tiet_tung_y, so_y_dung = {}, 0
                for y in ("a", "b", "c", "d"):
                    hs = chuan_hoa_dap_an_tf(dap_an_doc.get(y))
                    dung_y = hs is not None and hs == dap_an_dung_tf.get(y)
                    chi_tiet_tung_y[y] = dung_y
                    so_y_dung += 1 if dung_y else 0
                _goc, diem_dat_duoc = diem_service.diem_cau_tf(thang, so_y_dung)
                kq_tf.update({
                    "dung_sai_hoac_diem": so_y_dung == 4,
                    "diem_dat_duoc": diem_dat_duoc,
                    "so_y_dung": so_y_dung,
                    "chi_tiet_tung_y": chi_tiet_tung_y,
                })
            ket_qua_theo_stt[cau["so_thu_tu"]] = kq_tf

    # ---- Nhanh 2: Bai lam tu luan qua CHV_Grader ----
    if anh_tuluan_base64 and tl_list:
        danh_sach_cau_tl = []
        for cau in tl_list:
            generator_id = cau.get("generator_id")
            chuong, bai_so = trich_chuong_bai(generator_id)
            danh_sach_cau_tl.append({
                "question_id": generator_id,
                "bai": bai_so,
                "diem_toi_da": diem_service.diem_toi_da_cua_cau_theo_id(thang, "TL", generator_id),
                "dap_an_mau": cau.get("loi_giai") or "",
                "chuong": chuong,
            })

        cham_tu_luan = _boc_json(_goi_webhook(
            N8N_WEBHOOK_CHAM_TU_LUAN,
            {"anh_base64": anh_tuluan_base64, "danh_sach_cau": danh_sach_cau_tl},
            "cham-tu-luan",
        ))
        if isinstance(cham_tu_luan, dict):
            cham_tu_luan = [cham_tu_luan]
        if not isinstance(cham_tu_luan, list):
            raise GradePhotoError("CHV_Grader khong tra ve mang ket qua.")
        ket_qua_theo_generator_id = {
            kq.get("question_id"): kq for kq in cham_tu_luan if isinstance(kq, dict)
        }
        thong_tin_tl = {c["question_id"]: c for c in danh_sach_cau_tl}
        for cau in tl_list:
            generator_id = cau.get("generator_id")
            kq_ai = ket_qua_theo_generator_id.get(generator_id)
            if kq_ai is not None:
                # Moi truong do Python dat; tu AI chi lay diem + nhan xet.
                tt = thong_tin_tl[generator_id]
                diem = _diem_tu_luan(kq_ai, tt["diem_toi_da"])
                kq = {
                    "question_id": generator_id,
                    "loai_cau": "TL",
                    "dung_sai_hoac_diem": diem,
                    "diem_toi_da": tt["diem_toi_da"],
                    "nhan_xet": str(kq_ai.get("nhan_xet") or ""),
                    "chuong": tt["chuong"],
                    "bai": tt["bai"],
                    "tags": kq_ai.get("tags") if isinstance(kq_ai.get("tags"), list) else [],
                }
                if diem is None:
                    kq["trang_thai"] = "loi_cham"
                    kq["nhan_xet"] = ("CHV_Grader tra ve diem khong doc duoc. " + kq["nhan_xet"]).strip()
            else:
                chuong, bai_so = trich_chuong_bai(generator_id)
                kq = {
                    "question_id": generator_id,
                    "loai_cau": "TL",
                    "dung_sai_hoac_diem": None,
                    "diem_toi_da": diem_service.diem_toi_da_cua_cau_theo_id(thang, "TL", generator_id),
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
        loai_chuan = diem_service.loai_cau_chuan(cau)
        ket_qua_theo_stt[stt] = {
            "question_id": generator_id,
            "loai_cau": loai_chuan,
            "dung_sai_hoac_diem": None,
            "diem_toi_da": diem_service.diem_toi_da_cua_cau(thang, loai_chuan),
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
        if kq.get("loai_cau") == "TF" and isinstance(kq.get("diem_dat_duoc"), (int, float)):
            tong_diem_dat += kq["diem_dat_duoc"]
        elif isinstance(gia_tri, bool):
            tong_diem_dat += (kq.get("diem_toi_da") or 0) if gia_tri else 0
        else:
            tong_diem_dat += float(gia_tri)

    lam_tron = thang.get("lam_tron", 2)
    diem_tam_tinh = round(tong_diem_dat, lam_tron)

    return {
        "tong_so_cau": tong_so_cau,
        "diem_tren_10_tam_tinh": diem_tam_tinh,
        "thang_diem": thang,
        "diem_toi_da_da_cham": round(tong_diem_toi_da_da_cham, lam_tron),
        "diem_toi_da_tong": thang["diem_toi_da_tong"],
        "ghi_chu": (
            "Diem cong don tren thang 10 (MC 3d - TF 2d - SA 2d - TL 3d), "
            "chi tinh cac cau da cham duoc. Cau TF tinh theo so y dung "
            "nhu cham tren web."
        ),
        "chi_tiet": chi_tiet,
    }
