-- =====================================================================
--  MAN HINH CHON VAI TRO SAU KHI DANG NHAP LAN DAU
--  Version 2.51 - 2026-09-15
--
--  Them trang thai 'chua_chon' cho cot profiles.vai_tro.
--
--  VI SAO CAN: neu tai khoan moi mac dinh la 'hoc_sinh' thi he thong
--  KHONG phan biet duoc "da chon hoc sinh" voi "chua duoc hoi bao gio",
--  nen khong biet luc nao phai hien man hinh chon vai tro. Nguoi dang
--  nhap bang Google khong di qua trang dang ky nen chua he duoc hoi.
--
--  CHAY TRUOC khi deploy code moi. Chay truoc cung khong hong gi: cac
--  tai khoan cu giu nguyen hoc_sinh/giao_vien, chi tai khoan TAO MOI
--  tu luc nay moi mang 'chua_chon'.
-- =====================================================================

-- 1) Cho phep them gia tri 'chua_chon'
alter table profiles drop constraint if exists profiles_vai_tro_check;

alter table profiles add constraint profiles_vai_tro_check
  check (vai_tro in ('chua_chon', 'hoc_sinh', 'giao_vien', 'quan_tri'));

-- 2) Tai khoan tao moi tu nay: chua chon vai tro
alter table profiles alter column vai_tro set default 'chua_chon';

-- 3) Kiem tra lai
select vai_tro, count(*) as so_tai_khoan
from profiles
group by vai_tro
order by vai_tro;

-- Ket qua mong doi: cac tai khoan cu van la hoc_sinh / giao_vien nhu truoc.
-- Chua co dong 'chua_chon' nao - dung, vi no chi xuat hien khi co nguoi
-- dang ky moi sau khi chay cau lenh nay.

-- ---------------------------------------------------------------------
-- MUON THU MAN HINH CHON VAI TRO BANG TAI KHOAN DANG CO:
--   update profiles set vai_tro = 'chua_chon' where email = 'dia-chi-cua-ban';
-- roi vao lai /chat - se thay man hinh chon vai tro.
-- ---------------------------------------------------------------------
