"""
Doc/ghi vai tro (vai_tro) cua nguoi dung trong bang public.profiles.

Ba vai tro: 'hoc_sinh' (mac dinh), 'giao_vien', 'quan_tri'.

LUU Y VAN HANH: cot vai_tro duoc them bang SQL (xem docs/21_TAI_KHOAN_
GIAO_VIEN.md muc "Buoc 1"). PHAI chay SQL do TRUOC khi deploy ban nay,
neu khong moi tai khoan deu bi coi la hoc_sinh va chinh giao vien cung
khong vao duoc /gv/*. Ham lay_vai_tro() phan biet ro 2 truong hop:
- Doc duoc nhung khong co dong  -> 'hoc_sinh' (an toan, chan cua).
- Doc LOI vi chua co cot vai_tro -> 'chua_cau_hinh' (van chan cua,
  nhung bao loi ro rang de biet duong chay SQL, khong im lang).
"""

from app.core.supabase import supabase

VAI_TRO_MAC_DINH = "hoc_sinh"
VAI_TRO_CHUA_CAU_HINH = "chua_cau_hinh"
VAI_TRO_GIAO_VIEN = ("giao_vien", "quan_tri")


def lay_vai_tro(user_id: str) -> str:
    """Tra ve vai_tro cua 1 tai khoan. Xem docstring dau file ve loi."""
    if not user_id:
        return VAI_TRO_MAC_DINH
    try:
        ket_qua = (
            supabase.table("profiles")
            .select("vai_tro")
            .eq("id", user_id)
            .single()
            .execute()
        )
    except Exception as e:
        # Thuong la: column profiles.vai_tro does not exist -> chua chay SQL.
        print("LOI DOC vai_tro (da chay SQL them cot chua?):", e)
        return VAI_TRO_CHUA_CAU_HINH

    if not ket_qua.data:
        return VAI_TRO_MAC_DINH
    return ket_qua.data.get("vai_tro") or VAI_TRO_MAC_DINH


def la_giao_vien(user_id: str) -> bool:
    return lay_vai_tro(user_id) in VAI_TRO_GIAO_VIEN


def dat_vai_tro(user_id: str, vai_tro: str) -> bool:
    """
    Ghi vai_tro cho 1 tai khoan. Dung sau khi dang ky giao vien thanh cong
    (trigger handle_new_user chi dat duoc vai_tro neu da sua trigger; ham
    nay la duong chac chan, khong phu thuoc trigger).
    """
    if vai_tro not in ("hoc_sinh", "giao_vien", "quan_tri"):
        raise ValueError(f"vai_tro khong hop le: {vai_tro}")
    try:
        supabase.table("profiles").update({"vai_tro": vai_tro}).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"LOI GHI vai_tro ({user_id} -> {vai_tro}):", e)
        return False


def lay_ho_so(user_id: str) -> dict | None:
    """Doc ho so day du cua 1 tai khoan (dung o khu lam viec giao vien)."""
    try:
        ket_qua = (
            supabase.table("profiles")
            .select("id, ho_ten, khoi, lop, vai_tro")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return ket_qua.data
    except Exception as e:
        print("LOI DOC HO SO:", e)
        return None
