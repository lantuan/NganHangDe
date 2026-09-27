import random
from sympy import symbols, S, pi, sqrt, diff, integrate,sin,cos,gamma,simplify,latex,expand,apart,gcd,log,vector
from sympy.physics.vector import vlatex
from sympy.abc import x, y, z
from sympy import*
import os,codecs,re
from sympy.solvers.solveset import linsolve #Giải hệ phương trình tuyến tính


# #########====================================================
TF_dothi_khong=lambda debai,text_choice,giai:f'''\\begin{{ex}}%%[?]\n{debai}\n{text_choice}\n\\loigiai{{\n\\begin{{itemchoice}}\n\\itemch {giai[0]}\n\\itemch {giai[1]}\n\\itemch {giai[2]}\n\\itemch {giai[3]}\n\\end{{itemchoice}}\n}}\n\\end{{ex}}\n'''
TF_dothi_giai=lambda debai,text_choice,giai,dothi_giai:f'''\\begin{{ex}}%%[?]\n{debai}\n{text_choice}\n\\loigiai{{\n\\immini[thm]{{\n\\begin{{itemchoice}}\n\\itemch {giai[0]}\n\\itemch {giai[1]}\n\\itemch {giai[2]}\n\\itemch {giai[3]}\n\\end{{itemchoice}}\n}}\n{{\n{dothi_giai}\n}}\n}}\n\\end{{ex}}\n'''
TF_dothi_de=lambda debai,text_choice,giai,dothi_de:f'''\\begin{{ex}}%%[?]\n\\immini[thm]{{\n{debai}\n{text_choice}\n}}{{\n{dothi_de}\n}}\n\\loigiai{{\n\\begin{{itemchoice}}\t\n\\itemch {giai[0]}\t\n\\itemch {giai[1]}\t\n\\itemch {giai[2]}\t\n\\itemch {giai[3]}\n\\end{{itemchoice}}\n}}\n\\end{{ex}}\n'''
TF_dothi_de_giai=lambda debai,text_choice,giai,dothi_de,dothi_giai:f'''\\begin{{ex}}%%[?]\n\\immini[thm]{{\n{debai}\n{text_choice}\n}}{{\n{dothi_de}\n}}\n\\loigiai{{\n\\immini[thm]{{\n\\begin{{itemchoice}}\n\\itemch {giai[0]}\n\\itemch {giai[1]}\n\\itemch {giai[2]}\n\\itemch {giai[3]}\n\\end{{itemchoice}}\n}}\n{{\n{dothi_giai}\n}}\n}}\n\\end{{ex}}\n'''
# ##############################################
def phatbieu_giai(ds_abcd,socot):###Dùng cho câu TRUE FALSE mà đồ thị thay đổi nét vẽ, phối hợp với hàm TF_baitoan
	cau_a,cau_b,cau_c,cau_d=[random.choice(ds_abcd[i]) for i in range(len(ds_abcd))]
	while "True" not in cau_a[0] and "True" not in cau_b[0] and "True" not in cau_c[0] and "True" not in cau_d[0]:
		cau_a,cau_b,cau_c,cau_d=[random.choice(ds_abcd[i]) for i in range(len(ds_abcd))]
	cau=[cau_a[0],cau_b[0],cau_c[0],cau_d[0]]
	# SUA: \choiceTFn[N] KHONG TON TAI trong data/config/ex_test.sty (chi co
	# \choiceTFt duoc dinh nghia that su) - dung \choiceTFn lam LaTeX bo qua
	# lenh khong xac dinh roi in cac khoi {...} thanh 1 doan van chay lien,
	# mat het dinh dang Dung/Sai khi xuat PDF (socot mac dinh la 4 nen loi
	# nay xay ra o TAT CA cau TF khi ra PDF - xem 16_CHANGELOG Version 2.27).
	# Luon dung \choiceTFt (macro duy nhat co that), bo tham so socot cu.
	text_choice='\\choiceTFt'
	for i in range(len(cau)):
		text_choice=text_choice+cau[i]+"\n"
	giai=[cau_a[1],cau_b[1],cau_c[1],cau_d[1]]
	return text_choice,giai
# ####===Đồ thị nào không có thì nhập số 0
TF_baitoan=lambda debai,text_choice,giai,dothi_de,dothi_giai:TF_dothi_khong(debai,text_choice,giai) if (dothi_de==0 and dothi_giai==0) else TF_dothi_de(debai,text_choice,giai,dothi_de) if (dothi_de!=0 and dothi_giai==0) else TF_dothi_giai(debai,text_choice,giai,dothi_giai) if (dothi_de==0 and dothi_giai!=0) else TF_dothi_de_giai(debai,text_choice,giai,dothi_de,dothi_giai)
# ======================================================
# Dùng def này cho bài toán không có đồ thị hoặc đồ thị giữ nguyên (không đổi nét vẽ).
# ####===Đồ thị nào không có thì nhập số 0
def TF_baitoan_du(debai,ds_abcd,dothi_de,dothi_giai,socot):
	cau_a,cau_b,cau_c,cau_d=[random.choice(ds_abcd[i]) for i in range(len(ds_abcd))]
	while "True" not in cau_a[0] and "True" not in cau_b[0] and "True" not in cau_c[0] and "True" not in cau_d[0]:
		cau_a,cau_b,cau_c,cau_d=[random.choice(ds_abcd[i]) for i in range(len(ds_abcd))]
	cau=[cau_a[0],cau_b[0],cau_c[0],cau_d[0]]
	# SUA: \choiceTFn[N] KHONG TON TAI trong data/config/ex_test.sty (chi co
	# \choiceTFt duoc dinh nghia that su) - dung \choiceTFn lam LaTeX bo qua
	# lenh khong xac dinh roi in cac khoi {...} thanh 1 doan van chay lien,
	# mat het dinh dang Dung/Sai khi xuat PDF (socot mac dinh la 4 nen loi
	# nay xay ra o TAT CA cau TF khi ra PDF - xem 16_CHANGELOG Version 2.27).
	# Luon dung \choiceTFt (macro duy nhat co that), bo tham so socot cu.
	text_choice='\\choiceTFt'
	for i in range(len(cau)):
		text_choice=text_choice+cau[i]+"\n"
	giai=[cau_a[1],cau_b[1],cau_c[1],cau_d[1]]
	return TF_dothi_khong(debai,text_choice,giai) if (dothi_de==0 and dothi_giai==0) else TF_dothi_de(debai,text_choice,giai,dothi_de) if (dothi_de!=0 and dothi_giai==0) else TF_dothi_giai(debai,text_choice,giai,dothi_giai) if (dothi_de==0 and dothi_giai!=0) else TF_dothi_de_giai(debai,text_choice,giai,dothi_de,dothi_giai)
# ===========================================================================================
# QUY ƯỚC BẮT BUỘC VỀ LOẠI CÂU (chốt 27/09/2026)
#
#   Trả lời ngắn (TLN, dang=2 hoặc 3): MỘT câu hỏi -> MỘT đáp án.
#                                      KHÔNG được chia ý a), b).
#   Tự luận (TL):                      phải có TỪ HAI Ý trở lên.
#
# Hai hàm dưới đây chặn ngay lúc viết hàm sinh câu hỏi, để không lọt vào đề.
# Tầng khoá thứ hai nằm ở app/services/generator_service.py, kiểm theo TÊN HÀM
# (có _SA_ hay _TL_) nên dù ai viết kiểu gì cũng không lách được.
# ===========================================================================================
class LoaiCauSaiError(ValueError):
	"""Câu sinh ra không đúng loại mà TÊN HÀM đã hứa.

	Kế thừa ValueError để hàm cũ nào đang bắt ValueError vẫn bắt được, nhưng
	có tên riêng để lúc ra đề phân biệt được: đây là câu SAI LOẠI (bỏ qua,
	báo thiếu) chứ không phải hàm tính toán bị lỗi số liệu (phải dừng).
	"""


def _khoa_loai_cau_TLN(debai, dang):
	"""Chặn câu trả lời ngắn bị chia ý a), b)."""
	if dang not in (2, 3):
		return
	dau_hieu = ("\\begin{listEX}", "\\item ", "\\SA[")
	for d in dau_hieu:
		if d in str(debai):
			raise LoaiCauSaiError(
				"Câu TRẢ LỜI NGẮN không được chia ý a), b): đề bài đang chứa %r. "
				"Một câu trả lời ngắn chỉ có MỘT câu hỏi và MỘT đáp án. "
				"Muốn nhiều ý thì viết thành câu TỰ LUẬN (tên hàm có _TL_)." % d)


def _khoa_loai_cau_TL(ds_abcd):
	"""Chặn câu tự luận chỉ có một ý."""
	if len(ds_abcd) < 2:
		raise LoaiCauSaiError(
			"Câu TỰ LUẬN phải có từ HAI ý trở lên, đang chỉ có %d ý. "
			"Nếu chỉ hỏi một ý thì đó là câu TRẢ LỜI NGẮN (tên hàm có _SA_)."
			% len(ds_abcd))


# ===========================================================================================
# Hàm này dùng cho câu MC_SA mà đáp số là hằng số
# Nếu không có đồ thị thì tại vị trí đồ thị nhập số 0
def MC_SA_answer_const(debai,dapso,dsnhieu,giai,dothi_de,dothi_giai,dang):
	_khoa_loai_cau_TLN(debai,dang)
	nhieuda=random.sample(dsnhieu,3)
	while len(set([dapso,nhieuda[0],nhieuda[1],nhieuda[2]]))<4:
		nhieuda=random.sample(dsnhieu,3)
	ketqua=f"{{\\True ${dapso}$}}\n"
	nhieu1=f"{{$ {nhieuda[0]}$}}\n"
	nhieu2=f"{{${nhieuda[1]}$}}\n"
	nhieu3=f"{{${nhieuda[2]}$}}\n"
	# Đảo đáp án trắc nghiệm
	list_choice=[ketqua,nhieu1,nhieu2,nhieu3]
	random.shuffle(list_choice)
	text_choice='\\choice'
	for i in range(len(list_choice)):
		text_choice=text_choice+list_choice[i]
	text_choice=text_choice if dang==1 else ''
	TLngan=f"\\shortans[7]{ketqua}" if dang==3 else f"\\shortans{ketqua}" if dang==2 else ""
	TLngan=TLngan.replace("\\True","")
	MC_SA_dothi_khong=f'''\\begin{{ex}}%%[?]\n{debai}\n{text_choice}\n{TLngan}\n\\loigiai{{\n{giai}\n}}\n\\end{{ex}}\n'''
	MC_SA_dothi_de=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai}}}\n{{{dothi_de}}}\n{text_choice}\n{TLngan}\n\\loigiai{{\n{giai}\n}}\n\\end{{ex}}\n'''
	MC_SA_dothi_giai=f'''\\begin{{ex}}%%[?]\n{debai}\n{text_choice}\n{TLngan}\n\\loigiai{{\n\\immini{{\n{giai}}}\n{{{dothi_giai}}}\n}}\n\\end{{ex}}\n'''
	MC_SA_dothi_de_giai=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai}}}\n{{{dothi_de}}}\n{text_choice}\n{TLngan}\n\\loigiai{{\n\\immini{{\n{giai}}}\n{{{dothi_giai}}}\n}}\n\\end{{ex}}\n'''
	return MC_SA_dothi_khong if (dothi_de==0 and dothi_giai==0) else MC_SA_dothi_de if (dothi_de!=0 and dothi_giai==0) else MC_SA_dothi_giai if (dothi_de==0 and dothi_giai!=0) else MC_SA_dothi_de_giai
# =============================================================
# Hàm này dùng cho câu MC_SA mà đáp số là dạng kí tự - Bên ham bài toán để sẵn dấu f"$đáp án $" nếu là kí hiệu toán học
# Nếu không có đồ thị thì tại vị trí đồ thị nhập số 0
def MC_SA_answer_text(debai,dapso,dsnhieu,giai,dothi_de,dothi_giai,dang):
	_khoa_loai_cau_TLN(debai,dang)
	nhieuda=random.sample(dsnhieu,3)
	while len(set([dapso,nhieuda[0],nhieuda[1],nhieuda[2]]))<4:
		nhieuda=random.sample(dsnhieu,3)
	ketqua=f"{{\\True {dapso}}}\n"
	nhieu1=f"{{{nhieuda[0]}}}\n"
	nhieu2=f"{{{nhieuda[1]}}}\n"
	nhieu3=f"{{{nhieuda[2]}}}\n"
	# Đảo đáp án trắc nghiệm
	list_choice=[ketqua,nhieu1,nhieu2,nhieu3]
	random.shuffle(list_choice)
	text_choice='\\choice'
	for i in range(len(list_choice)):
		text_choice=text_choice+list_choice[i]
	text_choice=text_choice if dang==1 else ''
	TLngan=f"\\shortans[7]{ketqua}" if dang==3 else f"\\shortans{ketqua}" if dang==2 else ""
	TLngan=TLngan.replace("\\True","")
	MC_SA_dothi_khong=f'''\\begin{{ex}}%%[?]\n{debai}\n{text_choice}\n{TLngan}\n\\loigiai{{\n{giai}\n}}\n\\end{{ex}}\n'''
	MC_SA_dothi_de=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai}}}\n{{{dothi_de}}}\n{text_choice}\n{TLngan}\n\\loigiai{{\n{giai}\n}}\n\\end{{ex}}\n'''
	MC_SA_dothi_giai=f'''\\begin{{ex}}%%[?]\n{debai}\n{text_choice}\n{TLngan}\n\\loigiai{{\n\\immini{{\n{giai}}}\n{{{dothi_giai}}}\n}}\n\\end{{ex}}\n'''
	MC_SA_dothi_de_giai=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai}}}\n{{{dothi_de}}}\n{text_choice}\n{TLngan}\n\\loigiai{{\n\\immini{{\n{giai}}}\n{{{dothi_giai}}}\n}}\n\\end{{ex}}\n'''
	return MC_SA_dothi_khong if (dothi_de==0 and dothi_giai==0) else MC_SA_dothi_de if (dothi_de!=0 and dothi_giai==0) else MC_SA_dothi_giai if (dothi_de==0 and dothi_giai!=0) else MC_SA_dothi_de_giai
# #########====================================================

def TL_answer_const(debai,ds_abcd,dothi_de,dothi_giai,dong):##
	_khoa_loai_cau_TL(ds_abcd)
	hoi_item=f"\\begin{{listEX}}[{dong}]\n"
	for j in range(len(ds_abcd)):
		hoi_item+=f"\\item {ds_abcd[j][0]} \\SA[4]{{${vlatex(ds_abcd[j][1])}$}}\n"
	hoi_item+=f"\\end{{listEX}}\n"
	giai_item=f"\\begin{{listEX}}[1]\n"
	for j in range(len(ds_abcd)):
		giai_item+=f"\\item {ds_abcd[j][2]}\n"
	giai_item+=f"\\end{{listEX}}\n"
	TL_dothi_not=f'''\\begin{{ex}}%%[?]\n{debai} \n{hoi_item}\n \\loigiai{{\n{giai_item}\n}}\n\\end{{ex}}\n'''
	TL_dothi_de=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai} \n{hoi_item}\n}}{{\n{dothi_de}\n}} \\loigiai{{\n{giai_item}\n}}\n\\end{{ex}}\n'''
	TL_dothi_giai=f'''\\begin{{ex}}%%[?]\n{debai} \n{hoi_item}\n \\loigiai{{\n\\immini{{\n{giai_item}\n}}{{\n{dothi_giai}\n}}\n}}\n\\end{{ex}}\n'''
	TL_dothi_de_giai=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai}\n{hoi_item}\n}}{{\n{dothi_de}\n}}\n \\loigiai{{\n\\immini{{\n{giai_item}\n}}{{\n{dothi_giai}\n}}\n}}\n\\end{{ex}}\n'''
	return TL_dothi_not if (dothi_de==0 and dothi_giai==0) else TL_dothi_de if (dothi_de!=0 and dothi_giai==0) else TL_dothi_giai if (dothi_de==0 and dothi_giai!=0) else TL_dothi_de_giai
# #########====================================================
def TL_answer_text(debai,ds_abcd,dothi_de,dothi_giai,dong):##
	_khoa_loai_cau_TL(ds_abcd)
	hoi_item=f"\\begin{{listEX}}[{dong}]\n"
	for j in range(len(ds_abcd)):
		hoi_item+=f"\\item {ds_abcd[j][0]} \\SA[4]{{${ds_abcd[j][1]}$}}\n"
	hoi_item+=f"\\end{{listEX}}\n"
	giai_item=f"\\begin{{listEX}}[1]\n"
	for j in range(len(ds_abcd)):
		giai_item+=f"\\item {ds_abcd[j][2]}\n"
	giai_item+=f"\\end{{listEX}}\n"
	TL_dothi_not=f'''\\begin{{ex}}%%[?]\n{debai} \n{hoi_item}\n \\loigiai{{\n{giai_item}\n}}\n\\end{{ex}}\n'''
	TL_dothi_de=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai} \n{hoi_item}\n}}{{\n{dothi_de}\n}} \\loigiai{{\n{giai_item}\n}}\n\\end{{ex}}\n'''
	TL_dothi_giai=f'''\\begin{{ex}}%%[?]\n{debai} \n{hoi_item}\n \\loigiai{{\n\\immini{{\n{giai_item}\n}}{{\n{dothi_giai}\n}}\n}}\n\\end{{ex}}\n'''
	TL_dothi_de_giai=f'''\\begin{{ex}}%%[?]\n\\immini{{\n{debai}\n{hoi_item}\n}}{{\n{dothi_de}\n}}\n \\loigiai{{\n\\immini{{\n{giai_item}\n}}{{\n{dothi_giai}\n}}\n}}\n\\end{{ex}}\n'''
	return TL_dothi_not if (dothi_de==0 and dothi_giai==0) else TL_dothi_de if (dothi_de!=0 and dothi_giai==0) else TL_dothi_giai if (dothi_de==0 and dothi_giai!=0) else TL_dothi_de_giai
# =======================================================
