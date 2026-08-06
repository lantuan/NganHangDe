from app.core.supabase import supabase


def luu_tin_nhan(user_id, conversation_id, role, noi_dung=None,
                  loai_phan_hoi=None, duong_dan_file=None):
    """Luu 1 dong vao chat_history. Khong lam crash chat neu Supabase loi."""
    try:
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "conversation_id": conversation_id,
            "role": role,
            "noi_dung": noi_dung,
            "loai_phan_hoi": loai_phan_hoi,
            "duong_dan_file": duong_dan_file,
        }).execute()
    except Exception as e:
        print("LOI LUU CHAT_HISTORY:", e)


def luu_de_da_sinh(user_id, conversation_id, lop=None, role=None,
                    loai_he_so=None, ki_thi=None, pham_vi_chuong=None,
                    blueprint=None):
    """Luu 1 lan sinh de thanh cong vao de_da_sinh. Tra ve id (uuid) hoac None."""
    try:
        result = supabase.table("de_da_sinh").insert({
            "user_id": user_id,
            "conversation_id": conversation_id,
            "lop": lop,
            "role": role,
            "loai_he_so": loai_he_so,
            "ki_thi": ki_thi,
            "pham_vi_chuong": pham_vi_chuong,
            "blueprint": blueprint,
        }).execute()
        if result.data:
            return result.data[0]["id"]
    except Exception as e:
        print("LOI LUU DE_DA_SINH:", e)
    return None


def luu_file_de(de_id, loai_file, duong_dan):
    """Luu duong dan 1 file (de/loigiai/tex) gan voi 1 de_da_sinh."""
    if not de_id:
        return
    try:
        supabase.table("file_de").insert({
            "de_id": de_id,
            "loai_file": loai_file,
            "duong_dan": duong_dan,
        }).execute()
    except Exception as e:
        print("LOI LUU FILE_DE:", e)


def lay_danh_sach_hoi_thoai(user_id, limit=30):
    """Lay danh sach cac cuoc hoi thoai cua 1 user, moi cuoc hoi thoai 1 dong,
    tieu de = tin nhan dau tien cua user, sap xep moi nhat truoc."""
    try:
        result = (
            supabase.table("chat_history")
            .select("conversation_id, role, noi_dung, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(300)
            .execute()
        )
    except Exception as e:
        print("LOI LAY DANH SACH HOI THOAI:", e)
        return []

    theo_hoi_thoai = {}
    for row in result.data:
        cid = row["conversation_id"]
        if cid not in theo_hoi_thoai:
            theo_hoi_thoai[cid] = {
                "conversation_id": cid,
                "created_at": row["created_at"],
                "tieu_de": None,
            }
        if row["role"] == "user":
            theo_hoi_thoai[cid]["tieu_de"] = row["noi_dung"]

    danh_sach = list(theo_hoi_thoai.values())
    danh_sach.sort(key=lambda x: x["created_at"], reverse=True)
    return danh_sach[:limit]


def lay_tin_nhan_hoi_thoai(user_id, conversation_id):
    """Lay toan bo tin nhan cua 1 cuoc hoi thoai, chi cua dung user_id do
    (khong cho xem hoi thoai cua nguoi khac)."""
    try:
        result = (
            supabase.table("chat_history")
            .select("role, noi_dung, loai_phan_hoi, duong_dan_file, created_at")
            .eq("user_id", user_id)
            .eq("conversation_id", conversation_id)
            .order("created_at")
            .execute()
        )
        return result.data
    except Exception as e:
        print("LOI LAY TIN NHAN HOI THOAI:", e)
        return []


def lay_de_theo_id(de_id):
    """Lay 1 de_da_sinh theo dung id (khong can biet conversation_id),
    kem cac file da co. Dung cho cham bai khi da biet chinh xac de_id."""
    try:
        de_result = (
            supabase.table("de_da_sinh")
            .select("*")
            .eq("id", de_id)
            .limit(1)
            .execute()
        )
        if not de_result.data:
            return None
        de = de_result.data[0]

        files_result = (
            supabase.table("file_de")
            .select("*")
            .eq("de_id", de["id"])
            .execute()
        )
        de["files"] = {f["loai_file"]: f["duong_dan"] for f in files_result.data}
        return de
    except Exception as e:
        print("LOI LAY DE THEO ID:", e)
        return None


def luu_ket_qua_cham_bai(student_id, de_thi_id, diem, chi_tiet_bai_lam):
    """Luu 1 lan cham bai vao exam_history (dong vai tro learning_history
    trong doc 12: diem so + chi tiet dung/sai tung cau). Khong lam crash
    API cham bai neu Supabase loi."""
    try:
        supabase.table("exam_history").insert({
            "student_id": student_id,
            "de_thi_id": de_thi_id,
            "diem": diem,
            "chi_tiet_bai_lam": chi_tiet_bai_lam,
        }).execute()
    except Exception as e:
        print("LOI LUU KET QUA CHAM BAI:", e)


def lay_de_gan_nhat(conversation_id):
    """Lay de duoc sinh gan nhat trong 1 cuoc hoi thoai, kem cac file da co.
    Tra ve dict {id, lop, role, ..., files: {"de": "...", "tex": "...", "loigiai": "..."}}
    hoac None neu chua sinh de nao trong hoi thoai nay."""
    try:
        de_result = (
            supabase.table("de_da_sinh")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if not de_result.data:
            return None
        de = de_result.data[0]

        files_result = (
            supabase.table("file_de")
            .select("*")
            .eq("de_id", de["id"])
            .execute()
        )
        de["files"] = {f["loai_file"]: f["duong_dan"] for f in files_result.data}
        return de
    except Exception as e:
        print("LOI LAY DE GAN NHAT:", e)
        return None
