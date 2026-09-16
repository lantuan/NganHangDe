from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Khoa service_role - CHI dung o phia may chu, KHONG BAO GIO gui ra trinh
# duyet. Lay o Supabase > Project Settings > API Keys > service_role.
# Khoa nay bo qua Row Level Security nen lo ra la mat toan bo du lieu.
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

N8N_WEBHOOK_DOC_PHIEU = os.getenv("N8N_WEBHOOK_DOC_PHIEU")
N8N_WEBHOOK_CHAM_TU_LUAN = os.getenv("N8N_WEBHOOK_CHAM_TU_LUAN")

# OAuth Client rieng cho dong bo danh sach hoc sinh tu Google Classroom
# (khac Client dang dung cho nut "Dang nhap bang Google" qua Supabase).
GOOGLE_CLASSROOM_CLIENT_ID = os.getenv("GOOGLE_CLASSROOM_CLIENT_ID")
GOOGLE_CLASSROOM_CLIENT_SECRET = os.getenv("GOOGLE_CLASSROOM_CLIENT_SECRET")

# Ma moi de dang ky tai khoan GIAO VIEN (/register/teacher). De trong thi
# KHONG ai dang ky duoc giao vien - an toan mac dinh, tranh truong hop
# quen dat bien moi truong ma ai cung tu nang minh len giao vien.
MA_MOI_GIAO_VIEN = os.getenv("MA_MOI_GIAO_VIEN", "").strip()

# ======================================================
# GIA SU AI - MUC A (docs/23_GIA_SU_AI.md)
# ======================================================
# Webhook n8n chi lam DUY NHAT viec goi mo hinh ngon ngu: toan bo cau
# lenh (de bai + dap an + loi giai chuan do Python sinh ra) duoc dung
# san o phia FastAPI roi gui sang, n8n khong tu lay du lieu o dau khac.
# De TRONG thi gia su van chay duoc nhung o "che do khong AI": chi hien
# lai loi giai chuan - khong bao gio hong trang cua hoc sinh.
N8N_WEBHOOK_GIA_SU = os.getenv("N8N_WEBHOOK_GIA_SU", "").strip()

# So luot hoi mac dinh cho MOI hoc sinh MOI ngay (dung tai khoan mo hinh
# mien phi nen phai chan tran). Giao vien nang rieng cho tung em o
# /gv/gia-su (ghi vao cot gia_su_luot.gioi_han).
def _so_nguyen_moi_truong(ten: str, mac_dinh: int) -> int:
    try:
        return int(os.getenv(ten, "").strip() or mac_dinh)
    except ValueError:
        print(f"CANH BAO: bien moi truong {ten} khong phai so nguyen, dung mac dinh {mac_dinh}")
        return mac_dinh


GIA_SU_LUOT_MOI_NGAY = _so_nguyen_moi_truong("GIA_SU_LUOT_MOI_NGAY", 20)

# Do dai toi da cau hoi hoc sinh go (chan spam/day lenh dai vao mo hinh).
GIA_SU_DO_DAI_CAU_HOI = _so_nguyen_moi_truong("GIA_SU_DO_DAI_CAU_HOI", 500)
