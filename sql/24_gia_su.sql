-- ======================================================
-- GIA SU AI - MUC A (giang lai chinh cau trong de vua lam)
-- Chay 1 lan trong Supabase > SQL Editor.
-- Xem docs/23_GIA_SU_AI.md.
-- ======================================================

-- 1) Bang dem luot hoi moi hoc sinh moi ngay.
--    Khoa chinh (user_id, ngay) -> moi em moi ngay dung 1 dong duy nhat,
--    khong can don dep, ngay hom sau tu dong co dong moi = het luot moi.
--    gioi_han NULL = dung han muc mac dinh trong config (GIA_SU_LUOT_MOI_NGAY).
--    Giao vien co the ghi gioi_han rieng cho 1 em o trang /gv/gia-su.
create table if not exists public.gia_su_luot (
    user_id    uuid not null references auth.users(id) on delete cascade,
    ngay       date not null default (now() at time zone 'Asia/Ho_Chi_Minh')::date,
    so_luot    integer not null default 0,
    gioi_han   integer,
    updated_at timestamptz not null default now(),
    primary key (user_id, ngay)
);

-- 2) Nhat ki hoi dap - LUU DU, khong xoa.
--    Day la 1 trong 3 lop khoa chong "AI tu tinh toan": moi cau tra loi
--    cua AI deu duoc luu nguyen van kem dap an Python da dua vao lenh,
--    de giao vien doc lai va phat hien ngay neu AI noi lech.
create table if not exists public.gia_su_hoi_dap (
    id             uuid primary key default gen_random_uuid(),
    user_id        uuid not null references auth.users(id) on delete cascade,
    de_id          uuid,
    so_thu_tu      integer,
    question_id    text,           -- generator_id (vd L10_C1_B2_VD01_MC_v1)
    muc            text not null default 'A',   -- 'A' = giang lai de, 'B' = chi ve li thuyet (lam sau)
    cau_hoi        text not null,  -- cau hoc sinh go
    tra_loi        text,           -- nguyen van cau tra loi cua AI
    dap_an_python  text,           -- dap an chuan da dua vao lenh (de doi chieu)
    trang_thai     text not null default 'ok',  -- ok | loi | ngoai_pham_vi | het_luot
    created_at     timestamptz not null default now()
);

create index if not exists gia_su_hoi_dap_user_idx
    on public.gia_su_hoi_dap (user_id, created_at desc);
create index if not exists gia_su_hoi_dap_de_idx
    on public.gia_su_hoi_dap (de_id);

-- 3) Bat RLS, KHONG tao policy (giong sql/22_bat_rls.sql):
--    trinh duyet khong bao gio truy cap thang 2 bang nay, moi thao tac
--    deu di qua FastAPI bang khoa service_role.
alter table public.gia_su_luot     enable row level security;
alter table public.gia_su_hoi_dap  enable row level security;
