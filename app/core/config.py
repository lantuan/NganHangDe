from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

N8N_WEBHOOK_DOC_PHIEU = os.getenv("N8N_WEBHOOK_DOC_PHIEU")
N8N_WEBHOOK_CHAM_TU_LUAN = os.getenv("N8N_WEBHOOK_CHAM_TU_LUAN")