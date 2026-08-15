import unicodedata

FILE = "app/routers/chat.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = unicodedata.normalize("NFC", content)
goc = len(content)

# ---- 1) Them import classroom_service ----
old_import = '''from app.core.deps import get_current_user
from app.core.lop_config import DANH_SACH_LOP
from app.services import history_service
from app.services import supabase_service'''

assert content.count(old_import) == 1, "Khong tim thay khoi import goc chat.py."

new_import = '''from app.core.deps import get_current_user
from app.core.lop_config import DANH_SACH_LOP
from app.services import history_service
from app.services import supabase_service
from app.services import classroom_service'''

content = content.replace(old_import, new_import)

# ---- 2) GET /chat: thu tu dong ghep lop bang email truoc khi roi ve /chon-lop ----
old_gate = '''    ho_so = supabase_service.lay_lop_hoc_sinh(user.id)
    if not ho_so or not ho_so.get("lop"):
        return RedirectResponse("/chon-lop", status_code=303)'''

assert content.count(old_gate) == 1, "Khong tim thay doan kiem tra ho_so/lop trong GET /chat."

new_gate = '''    ho_so = supabase_service.lay_lop_hoc_sinh(user.id)
    if not ho_so or not ho_so.get("lop"):
        # Thu tu dong ghep lop bang email da dong bo tu Google Classroom
        # (xem app/services/classroom_service.py) truoc khi bat hoc sinh
        # tu chon o /chon-lop. Khong tim thay (chua dong bo, hoac email
        # dang nhap khac email tren Classroom) thi roi ve /chon-lop nhu cu.
        khop = classroom_service.tim_lop_theo_email(user.email)
        if khop:
            supabase_service.cap_nhat_lop_hoc_sinh(user.id, khop["khoi"], khop["lop"])
            ho_so = khop
        else:
            return RedirectResponse("/chon-lop", status_code=303)'''

content = content.replace(old_gate, new_gate)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK - da sua {FILE} ({goc} -> {len(content)} ky tu)")
