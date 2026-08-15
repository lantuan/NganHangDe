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