import unicodedata

FILE = "app/services/supabase_service.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

old_tail = '''def get_user():
    """
    Lấy thông tin user hiện tại
    """

    return supabase.auth.get_user()'''

assert content.count(old_tail) == 1, "Khong tim thay get_user() cuoi file."

new_tail = old_tail + '''


def lay_lop_hoc_sinh(user_id: str):
    """
    Doc khoi/lop hoc sinh da tu chon o trang /chon-lop, tu bang
    public.profiles. Tra ve dict {"khoi":..., "lop":...} hoac None neu
    chua chon / co loi (khong lam crash luong /chat).
    """
    try:
        ket_qua = (
            supabase.table("profiles")
            .select("khoi, lop")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return ket_qua.data
    except Exception as e:
        print("LOI DOC PROFILE (lay_lop_hoc_sinh):", e)
        return None


def cap_nhat_lop_hoc_sinh(user_id: str, khoi: str, lop: str):
    """
    Ghi khoi/lop hoc sinh tu chon vao public.profiles.
    """
    return (
        supabase.table("profiles")
        .update({"khoi": khoi, "lop": lop})
        .eq("id", user_id)
        .execute()
    )'''

content = content.replace(old_tail, new_tail)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
