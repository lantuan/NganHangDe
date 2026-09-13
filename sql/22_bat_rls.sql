-- =====================================================================
--  BAT ROW LEVEL SECURITY CHO TOAN BO BANG TRONG SCHEMA public
--  Version 2.47 - 2026-09-13. Xem docs/22_BAO_MAT_RLS.md
--
--  CHAY FILE NAY SAU CUNG, chi khi da:
--    1. Dat SUPABASE_SERVICE_KEY trong .env tren VPS
--    2. Deploy code moi (app/core/supabase.py tach 2 client)
--    3. Vao web thu: dang nhap, tao de, xem /gv/thong-ke -> deu chay
--
--  Chay truoc khi lam 3 buoc tren = WEB CHET NGAY (moi truy van tra ve
--  rong), vi luc do may chu van dang dung khoa anon.
-- =====================================================================


-- ---------------------------------------------------------------------
-- PHAN 1 - Xem hien trang truoc khi sua (chay rieng de doi chieu)
-- ---------------------------------------------------------------------
-- select tablename, rowsecurity from pg_tables
-- where schemaname = 'public' order by rowsecurity, tablename;


-- ---------------------------------------------------------------------
-- PHAN 2 - Bat RLS cho MOI bang trong schema public
--
-- Dung vong lap de khong sot bang nao, ke ca bang tao them ve sau.
-- Bat RLS ma KHONG tao policy nao = khoa anon (khoa nhung trong trang
-- dang nhap, ai cung lay duoc) khong doc/ghi duoc gi het. Khoa
-- service_role van di qua binh thuong vi no bo qua RLS.
--
-- An toan voi ung dung nay vi trinh duyet CHI dung supabase-js cho
-- XAC THUC, khong truy van bang nao truc tiep (da kiem tra toan bo
-- app/templates: khong co .from() hay .rpc() nao).
-- ---------------------------------------------------------------------

do $$
declare
    r record;
begin
    for r in
        select tablename
        from pg_tables
        where schemaname = 'public'
    loop
        execute format('alter table public.%I enable row level security;', r.tablename);
        raise notice 'Da bat RLS: %', r.tablename;
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- PHAN 3 - Xoa cac policy cu qua thoang (neu co)
--
-- Neu truoc day co policy kieu "cho phep tat ca" thi bat RLS cung vo
-- nghia. Doan nay liet ke ra de kiem tra bang mat - KHONG tu xoa, vi
-- xoa nham policy that thi hong.
-- ---------------------------------------------------------------------

-- select schemaname, tablename, policyname, roles, cmd, qual
-- from pg_policies where schemaname = 'public';


-- ---------------------------------------------------------------------
-- PHAN 4 - Chan them mot lop nua (khong bat buoc, nhung nen lam)
--
-- RLS da du chan roi. Doan nay go luon quyen cap bang cho anon va
-- authenticated - phong truong hop sau nay lo tay tao mot policy
-- qua thoang. service_role khong bi anh huong.
--
-- Bo dau -- de chay neu muon.
-- ---------------------------------------------------------------------

-- revoke all on all tables in schema public from anon, authenticated;
-- alter default privileges in schema public
--   revoke all on tables from anon, authenticated;


-- ---------------------------------------------------------------------
-- PHAN 5 - Kiem tra lai sau khi chay
-- ---------------------------------------------------------------------

select tablename,
       rowsecurity as da_bat_rls,
       (select count(*) from pg_policies p
        where p.schemaname = 'public' and p.tablename = t.tablename) as so_policy
from pg_tables t
where schemaname = 'public'
order by rowsecurity, tablename;

-- Ket qua mong doi: MOI dong da_bat_rls = true, so_policy = 0.
