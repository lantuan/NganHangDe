from app.core.supabase import supabase

print("Đang kết nối...")

response = (
    supabase
    .table("profiles")
    .select("*")
    .limit(1)
    .execute()
)

print(response)