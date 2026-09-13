from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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
