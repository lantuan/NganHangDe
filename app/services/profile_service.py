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

from app.core.supabase import supabase_admin as supabase
from app.core.bo_nho_tam import BoNhoTam

_VAI_TRO = BoNhoTam(300)        # user_id -> vai_tro (5 phút), xem app/core/bo_nho_tam.py

VAI_TRO_MAC_DINH = "hoc_sinh"
# Tai khoan vua tao, CHUA tra loi cau hoi "ban la hoc sinh hay giao vien".
# Can trang thai rieng nay vi neu tai khoan moi mac dinh la 'hoc_sinh' thi
# khong the phan biet "da chon hoc sinh" voi "chua duoc hoi bao gio" ->
# khong biet luc nao nen hien man hinh chon vai tro.
VAI_TRO_CHUA_CHON = "chua_chon"
VAI_TRO_CHUA_CAU_HINH = "chua_cau_hinh"
VAI_TRO_GIAO_VIEN = ("giao_vien", "quan_tri")


def lay_vai_tro(user_id: str) -> str:
    """Tra ve vai_tro cua 1 tai khoan. Xem docstring dau file ve loi."""
    if not user_id:
        return VAI_TRO_MAC_DINH
    co, vt = _VAI_TRO.lay(user_id)
    if co:
        return vt
    try:
        ket_qua = (
            supabase.table("profiles")
            .select("vai_tro")
            .eq("id", user_id)
            .single()
            .execute()
        )
    except Exception as e:
        # Tai khoan KHONG CO dong profiles (dang ki truoc khi co trigger handle_new_user - docs/12_DATABASE.md):
        # .single() bao PGRST116. Truoc day roi vao 'chua_cau_hinh' -> bi hien trang Chon lop, chon xong ghi
        # vao 0 dong -> /chat lai day ve /chon-lop mai, bam "Toi la giao vien" cung khong ghi duoc gi
        # (co Lan 28/10/2026, tai khoan nganhangdetoanchv). Nay: tao dong profiles roi hoi chon vai tro.
        if _khong_co_dong(e) and tao_ho_so_thieu(user_id):
            return VAI_TRO_CHUA_CHON
        # Thuong la: column profiles.vai_tro does not exist -> chua chay SQL.
        print("LOI DOC vai_tro (da chay SQL them cot chua?):", e)
        return VAI_TRO_CHUA_CAU_HINH

    if not ket_qua.data:
        return VAI_TRO_MAC_DINH
    vt = ket_qua.data.get("vai_tro") or VAI_TRO_MAC_DINH
    _VAI_TRO.dat(user_id, vt)              # nhớ 5 phút (chỉ khi đọc được); đổi vai trò thì dat_vai_tro xoá ngay
    return vt


def _khong_co_dong(e) -> bool:
    """Loi .single() khi KHONG co dong nao (PostgREST PGRST116 / '0 rows')."""
    t = "%s %s" % (getattr(e, "code", "") or "", e)
    return "PGRST116" in t or "0 rows" in t


def tao_ho_so_thieu(user_id: str) -> bool:
    """Tao dong profiles cho tai khoan con thieu (giong trigger handle_new_user: id, email, ho_ten; vai_tro de mac
    dinh cot = 'chua_chon' -> nguoi dung duoc hoi lai la hoc sinh hay giao vien). Khong ghi de dong da co."""
    try:
        u = supabase.auth.admin.get_user_by_id(user_id).user
        md = getattr(u, "user_metadata", None) or {}
        email = getattr(u, "email", None)
        ten = md.get("fullname") or md.get("full_name") or md.get("name") or email
        supabase.table("profiles").upsert({"id": user_id, "email": email, "ho_ten": ten},
                                          on_conflict="id", ignore_duplicates=True).execute()
        print("DA TAO DONG profiles CON THIEU cho", email)
        return True
    except Exception as e:
        print("LOI TAO DONG profiles CON THIEU (%s):" % user_id, e)
        return False


def la_giao_vien(user_id: str) -> bool:
    return lay_vai_tro(user_id) in VAI_TRO_GIAO_VIEN


def dat_vai_tro(user_id: str, vai_tro: str) -> bool:
    """
    Ghi vai_tro cho 1 tai khoan. Dung sau khi dang ky giao vien thanh cong
    (trigger handle_new_user chi dat duoc vai_tro neu da sua trigger; ham
    nay la duong chac chan, khong phu thuoc trigger).
    """
    if vai_tro not in ("chua_chon", "hoc_sinh", "giao_vien", "quan_tri"):
        raise ValueError(f"vai_tro khong hop le: {vai_tro}")
    _VAI_TRO.xoa(user_id)
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
