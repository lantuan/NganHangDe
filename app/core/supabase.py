"""
Hai client Supabase, dung cho hai muc dich KHAC NHAU - khong duoc dung lan.

  supabase        -> khoa ANON. CHI dung cho Xac thuc (dang nhap, dang ky,
                     doc user tu token, doi mat khau). Day cung chinh la
                     khoa duoc nhung vao trang dang nhap cho trinh duyet
                     dung, nen phai coi nhu CONG KHAI.

  supabase_admin  -> khoa SERVICE ROLE. Dung cho MOI thao tac doc/ghi BANG
                     (profiles, de_da_sinh, exam_history, classroom_*...).
                     Khoa nay bo qua Row Level Security nen TUYET DOI khong
                     duoc gui ra trinh duyet.

LY DO TACH (sua 2026-09-13): truoc day ca he thong dung chung mot khoa
SUPABASE_KEY, va chinh khoa do duoc nhung vao ma nguon trang dang nhap
(bien supabase_anon_key trong app/routers/auth.py). Cong them viec moi
bang deu tat Row Level Security, hau qua la BAT KY AI xem ma nguon trang
cung co the doc/ghi thang vao cac bang - tu dat vai_tro='giao_vien' cho
chinh minh, hoac doc refresh_token Google Classroom trong bang
classroom_oauth. Xem docs/22_BAO_MAT_RLS.md.

Sau khi bat RLS (khong tao policy nao cho anon), khoa anon khong con doc
ghi duoc bang nao nua; chi supabase_admin lam duoc.
"""

from supabase import create_client, Client

from app.core.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_SERVICE_KEY,
)

# Client cho XAC THUC (khoa anon - cong khai)
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)

# Client cho DU LIEU (khoa service role - bi mat)
#
# Neu chua dat SUPABASE_SERVICE_KEY trong .env thi tam thoi lui ve khoa
# anon de web khong chet ngay luc deploy, nhung in canh bao that to. Khi
# da bat RLS ma van con chay bang khoa anon thi moi truy van deu tra ve
# rong -> nhin log se hieu ngay tai sao.
if SUPABASE_SERVICE_KEY:
    supabase_admin: Client = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_KEY,
    )
else:
    print(
        "CANH BAO BAO MAT: chua co SUPABASE_SERVICE_KEY trong .env - dang "
        "dung tam khoa anon cho ca thao tac du lieu. Xem docs/22_BAO_MAT_RLS.md."
    )
    supabase_admin = supabase
