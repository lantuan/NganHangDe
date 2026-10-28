# ==========================================
# CHƯƠNG 9 (lớp 10): TÍNH XÁC SUẤT THEO ĐỊNH NGHĨA CỔ ĐIỂN
#   Bài 26. Biến cố và định nghĩa cổ điển của xác suất
#   Bài 27. Thực hành tính xác suất theo định nghĩa cổ điển
#
# Nguồn: tệp LopXChuong9.py của cô Lan, chuyển sang chuẩn ngân hàng
# (đổi tên hàm theo ID, bỏ lệnh gọi ở mức mô-đun, vá ký tự thoát).
# Nội dung toán và lời giải giữ NGUYÊN như cô viết.
# ==========================================
import math
import re
import random
import numpy.random as np
from sympy import *

from num2words import num2words   # viet so bang chu tieng Viet

from math_type import *
from DefChung import calculate_coefficient, calculate_permutations
import DefChung as dc



# ---- Gieo dong xu n lan, tat ca cung mot mat (thi nghiem lap) ----
# (tên cũ của cô: K10_9_TN_1_H)
def L10_C9_B27_TH154_MC_A_01(socau,dang=1):
	gt = []
	dem = len(gt)
	while dem < socau:
		tung_xu = np.randint(3, 5)
		SN = np.choice(['sấp', 'ngửa'])
		trang_thai = np.choice(['liên tiếp', 'đồng thời'])

		v = [tung_xu, SN, trang_thai]
		if v not in gt:
			gt.append(v)
			dem += 1

	cauTN = ''
	for v in gt:
		tung_xu, SN, trang_thai = v[0], v[1], v[2]

		if v[2] == 'liên tiếp':
			debai = f"""Gieo một đồng xu cân đối liên tiếp {v[0]} lần. Gọi $E$ là biến cố: ``Tất cả các mặt đều là mặt {v[1]}''. Tính xác suất của biến cố $E$."""
		else:
			debai = f"""Gieo đồng thời {v[0]} đồng xu cân đối. Gọi $E$ là biến cố: ``Tất cả các mặt đều là mặt {v[1]}''. Tính xác suất của biến cố $E$."""

		dapso = f"""P(E)= \\dfrac{{1}}{{ { 2 ** v[0]} }}"""

		nhieu1 = f"""P(E) = \\dfrac{{1}}{{ {dc.calculate_permutations(int(v[0]),int(v[0]))}  }}"""
		nhieu2 = f"""P(E) = \\dfrac{{1}}{{ {v[0]} }}"""
		nhieu3 = f"""P(E) = \\dfrac{{1}}{{ {dc.calculate_coefficient(int(v[0]),2)} }}"""

		# Gom vào danh sách
		dsnhieu = [nhieu1, nhieu2, nhieu3]

		# Đảm bảo các phần tử trong dsnhieu là khác nhau
		i = 1
		while len(set(dsnhieu)) < len(dsnhieu):
			seen = set()
			for idx in range(len(dsnhieu)):
				if dsnhieu[idx] in seen:
					# Nếu trùng, sửa mẫu số để khác đi bằng cách cộng thêm i
					# Lấy mẫu số hiện tại từ chuỗi latex
					match = re.search(r'\{1\}\{\s*(\d+)\s*\}', dsnhieu[idx])
					if match:
						value = int(match.group(1)) + i
						dsnhieu[idx] = f"""P(E) = \\dfrac{{1}}{{ {value} }}"""
				seen.add(dsnhieu[idx])
			i += 1

		if v[2] == 'liên tiếp':
			giai = f"""
				Một đồng xu khi tung có hai trường hợp xảy ra là sấp hoặc ngửa. Nên khi tung đồng xu ${v[0]}$ lần liên tiếp thì $n(\\Omega) = 2^{v[0]}$.\\ \\\\
				Để ra tất cả các mặt đều {v[1]} thì chỉ có 1 trường hợp. Do đó, xác suất cần tìm là $P(E) = \\dfrac{{1}}{{ 2^{v[0]} }}$.
			"""
		else:
			giai = f"""
				Một đồng xu khi tung có hai trường hợp xảy ra là sấp hoặc ngửa. Nên đối với ${v[0]}$ đồng xu thì $n(\\Omega) = 2^{v[0]}$.\\ \\\\
				Để ra tất cả các mặt đều {v[1]} thì chỉ có 1 trường hợp. Do đó, xác suất cần tìm là $P(E) = \\dfrac{{1}}{{ 2^{v[0]} }}$.
			"""

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)  # Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTN
# ###==== Cách dùng: socau=4, dang = 0 tự luận, dạng = 1 trắc nghiệm
# print(K10_9_TN_1_H(socau,dang))
# ##############################################


# ---- Lap so tu cac chu so, chon so, xac suat tich le ----
# (tên cũ của cô: K10_9_TN_2_VD)
def L10_C9_B27_VD155_MC_A_01(socau,dang=1):
	gt = []
	dem = len(gt)
	while dem < socau:
		len_nums = np.randint(5,8)
		Nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

		while True:
			nums = random.sample(Nums, len_nums)
			num_odd = len([x for x in nums if x % 2 == 1])
			num_even = len(nums) - num_odd
			if abs(num_odd - num_even) <= 1:  # Chênh lệch giữa số lẻ và chẵn không quá 1
				break

		nums.sort()

		chu_so = np.choice(['ba', 'bốn'])
		chon = np.choice(['hai', 'ba'])

		lam_tron = np.choice(['chục', 'trăm'])

		v = [len_nums, nums, chu_so, chon, lam_tron]
		if v not in gt:
			gt.append(v)
			dem += 1

	cauTN = ''

	for v in gt:
		len_nums, nums, chu_so, chon, lam_tron = v[0], v[1], v[2], v[3], v[4]

		if v[2] == 'ba':
			num_chu_so = 3
		else:
			num_chu_so = 4

		if v[3] == 'hai':
			num_chon = 2
		else:
			num_chon = 3

		if v[4] == 'chục':
			num_lam_tron = 1
		else:
			num_lam_tron = 2

		odd_count = sum(1 for n in nums if n % 2 == 1)
		len_odd_count = odd_count * dc.calculate_permutations(v[0]-1,num_chu_so-1)

		debai = f"""Từ các chữ số {", ".join(str(num) for num in v[1])}, lập các số có {num_chu_so} chữ số khác nhau. 
			Chọn {v[3]} số trong các số có {v[2]} chữ số đó.
			Tính xác suất để tích {v[3]} số được chọn là số lẻ. (Làm tròn đến hàng phần {v[4]})"""
		dapso = f"""{round(dc.calculate_coefficient(len_odd_count, num_chon)/dc.calculate_coefficient(dc.calculate_permutations(v[0], num_chu_so), num_chon), num_lam_tron)}"""

		dapso = float(dapso)
		Sai_so = [round(i * 0.01, 2) for i in range(-50, 51) if i != 0]  # sai số từ -0.5 đến 0.5, bỏ 0

		# Lọc ra các sai số thỏa điều kiện khi cộng vào dapso sẽ ra giá trị nằm trong [0.2, 0.8]
		Sai_so_hop_le = [x for x in Sai_so if 0.2 <= (dapso + x) <= 0.8]

		# Chọn 3 sai số ngẫu nhiên từ danh sách hợp lệ
		if len(Sai_so_hop_le) >= 3:
			sai_so = random.sample(Sai_so_hop_le, 3)
		else:
			raise ValueError("Không đủ sai số hợp lệ để tạo các lựa chọn nhiễu")

		# Tạo các đáp án nhiễu
		nhieu1 = f"{round(dapso + sai_so[0], 4)}".replace(".", ",")
		nhieu2 = f"{round(dapso + sai_so[1], 4)}".replace(".", ",")
		nhieu3 = f"{round(dapso + sai_so[2], 4)}".replace(".", ",")

		dapso = f"{round(dapso, 4)}".replace(".", ",")

		# Gom vào danh sách
		dsnhieu = [nhieu1, nhieu2, nhieu3]

		giai = f"""
			Số các số có {v[2]} khác nhau là $A_{v[0]}^{num_chu_so} = {dc.calculate_permutations(v[0], num_chu_so)}$.\\\\
			Nên số phần tử của không gian mẫu bằng 
			$n(\\Omega) = C_{dc.calculate_permutations(v[0], num_chu_so)}^{num_chon} = {dc.calculate_coefficient(dc.calculate_permutations(v[0], num_chu_so), num_chon)}$.\\\\
			Trong đó có các số lẻ là ${odd_count} \\times A_{v[0]-1}^{num_chu_so - 1} = {len_odd_count}$.\\\\
			Để tích các số được chọn là số lẻ thì các số chọn phải là số lẻ. Tức ta được số cách chọn là\\\\
			$C_{{ {len_odd_count} }}^{{ {num_chon} }} = {dc.calculate_coefficient(len_odd_count, num_chon)}$.\\\\
			Vậy xác suất cần tìm là $\\dfrac{{ {dc.calculate_coefficient(len_odd_count, num_chon)} }}{{ {dc.calculate_coefficient(dc.calculate_permutations(v[0], num_chu_so), num_chon)} }}
			\\approx {dapso}$.
		"""

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)  # Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTN
# ###==== Cách dùng: socau=4
# print(K10_9_TN_1_H(socau,dang))
# ##############################################


# ---- Lap so tu nhien, chon so, xac suat ----
# (tên cũ của cô: K10_9_TN_3_VD)
def L10_C9_B27_VD155_MC_B_01(socau,dang=1):
	gt = []
	dem = len(gt)
	while dem < socau:
		len_nums = np.randint(5,8)
		Nums = [1,2,3,4,5,6,7,8,9]
		nums = random.sample(Nums, len_nums)
		nums.sort()

		chu_so = np.choice(['ba', 'bốn'])
		chon = np.choice(['hai', 'ba'])

		lam_tron = np.choice(['chục', 'trăm'])

		v = [len_nums, nums, chu_so, chon, lam_tron]
		if v not in gt:
			gt.append(v)
			dem += 1

	cauTN = ''

	for v in gt:
		len_nums, nums, chu_so, chon, lam_tron = v[0], v[1], v[2], v[3], v[4]

		if v[2] == 'ba':
			num_chu_so = 3
		else:
			num_chu_so = 4

		if v[3] == 'hai':
			num_chon = 2
		else:
			num_chon = 3

		if v[4] == 'chục':
			num_lam_tron = 1
		else:
			num_lam_tron = 2

		debai = f"""Từ các chữ số {", ".join(str(num) for num in v[1])}, lập các số tự nhiên có {num_chu_so} chữ số. 
			Chọn {v[3]} số trong các số có {num_chu_so} chữ số đó. 
			Tính xác suất để {v[3]} số được chọn này, mỗi số đều là số có {num_chu_so} chữ số khác nhau. (Làm tròn đến hàng phần {v[4]})"""
		dapso = f"""{round(dc.calculate_coefficient(dc.calculate_permutations(v[0], num_chu_so),num_chon) / dc.calculate_coefficient(len_nums ** num_chu_so, num_chon), num_lam_tron)}"""

		dapso = float(dapso)
		Sai_so = [i * 0.1 for i in range(-5, 6) if i != 0]

		# Lọc ra các sai số thỏa điều kiện khi cộng vào dapso sẽ ra giá trị nằm trong [0.2, 0.8]
		Sai_so_hop_le = [x for x in Sai_so if 0.2 <= (dapso + x) <= 0.8]

		# Chọn 3 sai số ngẫu nhiên từ danh sách hợp lệ
		if len(Sai_so_hop_le) >= 3:
			sai_so = random.sample(Sai_so_hop_le, 3)
		else:
			raise ValueError("Không đủ sai số hợp lệ để tạo các lựa chọn nhiễu")

		# Tạo các đáp án nhiễu
		nhieu1 = f"{dapso + sai_so[0]:.{num_lam_tron}f}".replace(".", ",")
		nhieu2 = f"{dapso + sai_so[1]:.{num_lam_tron}f}".replace(".", ",")
		nhieu3 = f"{dapso + sai_so[2]:.{num_lam_tron}f}".replace(".", ",")

		dapso  = f"{dapso:.{num_lam_tron}f}".replace(".", ",")

		# Gom vào danh sách
		dsnhieu = [nhieu1, nhieu2, nhieu3]

		giai = f"""
			Ta có $n(\\Omega) = {len_nums}^{num_chu_so} = {len_nums ** num_chu_so}$.\\\\
			Số các số có {v[2]} khác nhau là $A_{v[0]}^{num_chu_so} = {dc.calculate_permutations(v[0], num_chu_so)}$.\\\\
			Vậy xác suất cần tìm là $\\dfrac{{ C_{{ {dc.calculate_permutations(v[0], num_chu_so)} }}^{{ {num_chon} }} }}{{ C_{{ {len_nums ** num_chu_so } }}^{{ {num_chon} }} }}
			= \\dfrac{{ {dc.calculate_coefficient(dc.calculate_permutations(v[0], num_chu_so),num_chon)} }}{{ {dc.calculate_coefficient(len_nums ** num_chu_so, num_chon)} }}
			\\approx {dapso}$.
		"""

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)  # Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTN
# ###==== Cách dùng: socau=4
# print(K10_9_TN_1_H(socau,dang))
# ##############################################


# ---- Nhan biet quan he giua hai bien co (chon hai ban truc co do) ----
# (tên cũ của cô: K10_9_TN_4_B)
def L10_C9_B26_NB144_MC_A_01(socau,dang=1):
	gt = []
	dem = len(gt)
	while dem < socau:
		Nums = [7,8,9,10,11,12]
		nums = np.choice(Nums)
		boy = np.randint(3,nums-3)
		girl = nums - boy

		v = [Nums, boy, girl]
		if v not in gt:
			gt.append(v)
			dem += 1

	cauTN = ''

	for v in gt:
		Nums, boy, girl = v[0], v[1], v[2]

		debai = f"""
			Tổ 1 lớp 10C1A của trường THPT chuyên Hùng Vương cần chọn ra hai bạn đi trực cờ đỏ trái buổi. 
			Biết rằng tổ có {boy} bạn nam và {girl} bạn nữ. Gọi $A$ là biến cố: ``Hai bạn được chọn đều là nam'', 
			$B$ là biến cố: ``Hai bạn được chọn đều là nữ''. Trong các khẳng định sau, khẳng định nào đúng?
		"""
		dapso = f"""A \\cap B = \\varnothing """

		# Tạo các đáp án nhiễu
		nhieu1 = f""" A = C_{{ \\Omega }}B """
		nhieu2 = f""" A \\cup B = \\Omega """
		nhieu3 = f""" \\overline{{ A }} = B """

		# Gom vào danh sách
		dsnhieu = [nhieu1, nhieu2, nhieu3]

		giai = f"""

			Chọn hai bạn từ tổ có ${boy}$ bạn nam và ${girl}$ bạn nữ.\\\\

			$A$: ``hai bạn được chọn đều là nam''; $B$: ``hai bạn được chọn đều là nữ''.\\\\

			$\\bullet$ Một kết quả không thể vừa là ``cả hai đều nam'' vừa là ``cả hai đều nữ'',

			nên hai biến cố $A$ và $B$ không bao giờ cùng xảy ra: $A \\cap B = \\varnothing$ (hai biến cố xung khắc).\\\\

			$\\bullet$ $A \\cup B \\ne \\Omega$ vì còn trường hợp chọn được một nam và một nữ.\\\\

			$\\bullet$ $A \\ne B$ và $A$ cũng không phải biến cố đối của $B$, vì biến cố đối của $B$

			còn chứa trường hợp một nam một nữ.

		"""

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTN += MC_SA_answer_const(debai, dapso, dsnhieu, giai, 0, 0, dang)  # Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTN
# ###==== Cách dùng: socau=4
# print(K10_9_TN_1_H(socau,dang))
# ##############################################


# ---- It nhat mot lan xuat hien mat m (bien co doi) ----
# (tên cũ của cô: K10_C9_B26_XacSuatBienCo_MC_VD)
# SUA 28/09/2026: ban goc goi np.random.randint(...) nhung o tep nay
# np CHINH LA numpy.random, nen np.random la ham random() - khong co
# .randint -> ham nem AttributeError, khong ra duoc cau nao. Doi thanh
# np.randint(...) cho dung.
def L10_C9_B27_TH152_MC_A_01(socau, dang=1):
    gt = []
    dem = len(gt)

    while dem < socau:
        lan = np.randint(5, 10)
        mat = np.randint(1, 7)

        v = [lan, mat]
        if v not in gt:
            gt.append(v)
            dem += 1

    cauTN = ''
    for v in gt:
        lan, mat = v[0], v[1]

        # Tính toán xác suất: 1 - (5/6)^lan
        # Sử dụng math.pow hoặc lũy thừa trực tiếp
        xac_suat = 1 - (5 / 6) ** lan
        dapso = str(round(xac_suat, 2)).replace('.', ',')

        # Các đáp án nhiễu
        nhieu1 = str(round((5 / 6) ** lan, 2)).replace('.', ',')
        nhieu2 = str(round((5 * lan) / (6 * lan), 2)).replace('.', ',')  # Ví dụ nhiễu
        nhieu3 = str(round(1 - (5 * lan) / (6 * lan), 2)).replace('.', ',')
        dsnhieu = [nhieu1, nhieu2, nhieu3]

        debai = f"""Gieo một con xúc xắc cân đối liên tiếp ${lan}$ lần. Tính xác suất để có ít nhất một lần xuất hiện mặt ${mat}$ chấm."""

        giai = f"""
            Không gian mẫu $n(\\Omega) = 6^{lan}$.\\\\
            Để không lần nào xuất hiện mặt ${mat}$ chấm thì mỗi lần gieo có $5$ khả năng xảy ra (các mặt khác mặt ${mat}$), nên có tất cả $5^{lan}$ trường hợp thuận lợi cho biến cố đối.\\\\
            Xác suất để không lần nào xuất hiện mặt ${mat}$ chấm là $\\left(\\dfrac{{5}}{{6}}\\right)^{lan}$.\\\\
            Vậy xác suất cần tìm là $1 - \\left(\\dfrac{{5}}{{6}}\\right)^{lan} \\approx {dapso}$.
        """

        cauTN += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)
    return cauTN
# ###==== Cách dùng: socau=4 và socot=0

# ##############################################


# ---- Chon diem nguyen trong hinh, tinh xac suat ----
# (tên cũ của cô: K10_9_Ngan_1_VD)
def L10_C9_B27_VD155_SA_A_01(socau):
	gt=[]
	dem=len(gt)

	def count_even_numbers(x_A, x_C):
		# Tìm số lớn nhất chia hết cho 2 trong khoảng từ x_A đến x_C
		x_max = x_C // 2 * 2

		# Tìm số nhỏ nhất chia hết cho 2 trong khoảng từ x_A đến x_C
		x_min = (x_A + 1) // 2 * 2

		# Tính số phần tử chia hết cho 2 trong khoảng từ x_min đến x_max
		count = (x_max - x_min) // 2 + 1

		return count

	while dem<socau:
		xA = np.randint(-5,-1)
		yA = 0
		xB = xA
		yB = np.randint(2,5)
		xC = np.randint(2,6)
		yC = yB
		xD = xC
		yD = yA

		v = [xA, yA, xB, yB, xC, yC, xD, yD]
		if v not in gt:
			gt.append(v)
			dem+=1
	cauTF = ''
	for v in gt:
		xA, yA, xB, yB, xC, yC, xD, yD = v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]

		kq = round((count_even_numbers(xA,xC) * count_even_numbers(yA, yC)) / ((xC - xA + 1) * (yC - yA + 1)),2)
		dapso = str(kq).replace('.', ',')

		debai = f"""Trong hệ trục tọa độ $Oxy$ cho $A({xA};{yA})$, $B({xB};{yB})$, $C({xC};{yC})$, $D({xD};{yD})$. Chọn ngẫu nhiên một điểm có tọa độ $(x;y)$; 
		(với $x,y$ là các số nguyên) nằm trong hình chữ nhật $ABCD$ (kể cả các điểm nằm trên cạnh).
		 Tính xác suất để $x$ và $y$ chia hết cho $2$."""

		giai = f"""Ta có $\\Omega = \\left\\lbrace (x;y), {xA}\\le x \\le {xC} , {yA}\\le y \\le {yC} \\right\\rbrace$ với $x,y \\in \\mathbb{{Z}}$.\\\\
		Suy ra $n\\left( \\Omega \\right) = {xC - xA + 1} \\cdot {yC - yA + 1}={(xC - xA + 1) * (yC - yA + 1)}$. \\\\
		Ta có $x,y$ đều chia hết cho $2$ nên $A$ có số phần tử là ${count_even_numbers(xA,xC)} \\cdot {count_even_numbers(yA, yC)} = {count_even_numbers(xA,xC) * count_even_numbers(yA, yC)}$.\\\\
		Suy ra $\\mathrm{{P}}(A)=\\dfrac{{ {count_even_numbers(xA,xC) * count_even_numbers(yA, yC)} }}{{ {(xC - xA + 1) * (yC - yA + 1)}  }} = {dapso} $."""

		dsnhieu = ((count_even_numbers(xA,xC) * count_even_numbers(yA, yC)) / ((xC - xA) * (yC - yA)),
				   (count_even_numbers(xA,xC-2) * count_even_numbers(yA, yC-2)) / ((xC - xA + 1) * (yC - yA + 1)),
				   (count_even_numbers(xA,xC-2) * count_even_numbers(yA, yC-2)) / ((xC - xA) * (yC - yA)))
		cauTF+= MC_SA_answer_text(debai,dapso,dsnhieu,giai,0,0,2)
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_Ngan_1_VD(24))
# ##############################################


# ---- Chon bi tu tui bi do va bi xanh ----
# (tên cũ của cô: K10_9_Ngan_3_VD)
def L10_C9_B27_TH151_SA_A_01(socau): ####bị lỗi xác suất rất nhỏ
	gt=[]
	dem=len(gt)

	while dem<socau:
		vienbi = np.randint(3,7)
		vienbi_chu = num2words(vienbi, lang='vi')
		red = np.randint(vienbi,10)
		blue = np.randint(vienbi,10)
		while blue == red:
			blue = np.randint(vienbi,10)
		DK = ['chỉ có toàn bi đỏ hoặc toàn bi xanh', 'có cả bi đỏ và bi xanh']
		dk = np.choice(DK)
		DK.remove(dk)

		v = [vienbi, vienbi_chu, red, blue, dk, DK]
		if v not in gt:
			gt.append(v)
			dem+=1
	cauTF = ''
	for v in gt:
		vienbi, vienbi_chu, red, blue, dk, DK = v[0], v[1], v[2], v[3], v[4], v[5]

		def binomial_coefficient(n, k):
				# Hàm này tính tổ hợp chập n lấy k.
				# Haram n: Số nguyên không âm
				# param k: Số nguyên không âm
				# return: Giá trị tổ hợp chập n lấy k
			return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))  # Sử dụng math.factorial()

		khonggianmau = binomial_coefficient(red+blue, vienbi)
		cungmau = binomial_coefficient(red, vienbi) + binomial_coefficient(blue, vienbi)
		khacmau = khonggianmau - cungmau

		if dk == 'chỉ có toàn bi đỏ hoặc toàn bi xanh':
			kq = round(khacmau / khonggianmau, 2)
			nhieu = round(cungmau / khonggianmau, 5)
		else:
			kq = round(cungmau / khonggianmau, 2)
			nhieu = round(khacmau / khonggianmau, 5)
		dapso = str(kq).replace('.', ',')

		debai = f"""Chọn ngẫu nhiên {vienbi_chu} viên bi từ một túi đựng ${red}$ viên bi đỏ và ${blue}$ viên bi xanh đôi một khác nhau. 
				Gọi $A$ là biến cố: ``Trong {vienbi_chu} viên bi {dk}''. Tính $P(\\overline{{A}})$."""

		giai = f"""Không gian mẫu $n(\\Omega) = C_{{{blue + red}}}^{vienbi} = {khonggianmau}$. 
				$\\overline{{A}}$: ``Trong {vienbi_chu} viên bi {DK[0]}''.\\ \\\\ 
				Nên kết quả là ${dapso}$.
				"""

		dsnhieu = (str(nhieu).replace('.', ','),
				   str(round(binomial_coefficient(red, vienbi) / khonggianmau,5)).replace('.', ','),
				   str(round(binomial_coefficient(blue, vienbi) / khonggianmau,5)).replace('.', ','))
		cauTF+= MC_SA_answer_text(debai,dapso,dsnhieu,giai,0,0,2)
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_Ngan_3_VD(24))
# ##############################################


# ---- Gieo xuc xac, dung mot lan mat m1 va mot lan mat m2 ----
# (tên cũ của cô: K10_9_Ngan_4_VD)
def L10_C9_B27_TH154_SA_A_01(socau):
	gt=[]
	dem=len(gt)

	while dem<socau:
		lan = np.randint(5,10)
		while lan == 6:
			lan = np.randint(5,10)

		mat1 = np.randint(1,7)
		mat2 = np.randint(1,7)
		while mat1 == mat2:
			mat2 = np.randint(1,7)

		v = [lan, mat1, mat2]
		if v not in gt:
			gt.append(v)
			dem+=1
	cauTF = ''
	for v in gt:
		lan, mat1, mat2 = v[0], v[1], v[2]

		def calculate_permutations(n, k):
			"""
			Tính số chỉnh hợp chập k của n phần tử.

			Args:
				n (int): Số phần tử trong tập hợp.
				k (int): Kích thước của các chỉnh hợp.

			Returns:
				int: Số chỉnh hợp chập k của n phần tử.
			"""
			# Tính số chỉnh hợp chập k
			permutations = math.factorial(n) // math.factorial(n - k)
			return permutations

		def binomial_coefficient(n, k):
				# Hàm này tính tổ hợp chập n lấy k.
				# Haram n: Số nguyên không âm
				# param k: Số nguyên không âm
				# return: Giá trị tổ hợp chập n lấy k
			return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))  # Sử dụng math.factorial()

		kq = round((calculate_permutations(lan,2) * (4 ** (lan-2)))/ (6 ** lan),2)
		dapso = str(kq).replace('.', ',')

		debai = f"""Gieo một con xúc xắc cân đối liên tiếp ${lan}$ lần. Tính xác suất để luôn xuất hiện đúng một lần mặt ${mat1}$ chấm và một lần mặt ${mat2}$ chấm."""

		giai = f"""Không gian mẫu $n(\\Omega) = 6^{lan}$.\\\\
		Để có đúng một lần mặt ${mat1}$ chấm và ${mat2}$ chấm thì có tất cả số trường hợp là $A_{lan}^2 \\cdot 4^{lan - 2} = {calculate_permutations(6,2) * 4 ** (lan-2)}$. 
		Nên xác suất cần tìm là $\\dfrac{{ {calculate_permutations(lan,2) * 4 ** (lan-2)} }} {{ 6^{lan} }} = {dapso}$."""

		dsnhieu = (str(round((calculate_permutations(6,2) * (4 ** (lan-2))) / (6 ** lan),2)).replace('.', ','),
				   str(round((4**(lan-2)) / (6 * lan),2)).replace('.', ','),
				   str(round((calculate_permutations(6,2)) / (6 * lan),2)).replace('.', ','))
		cauTF+= MC_SA_answer_text(debai,dapso,dsnhieu,giai,0,0,2)
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_Ngan_4_VD(24))
# ##############################################


# =====================================================================
# CÂU ĐÚNG/SAI CHƯƠNG 9 - VIẾT LẠI 28/10/2026 (cô Lan: "cần, bổ sung luôn cho tôi")
# ---------------------------------------------------------------------
# Bản cũ (cô nhập 28/09/2026 từ LopXChuong9.py) giữ nguyên bối cảnh nhưng: bốn ý chưa xếp bậc NB -> TH -> VD -> VDC,
# mỗi ý chỉ 1 phát biểu đúng + 1 sai (có ý chỉ có phát biểu đúng), vài lời giải chỉ ghi "Đúng." / "Sai.", và một
# lỗi mẫu số trong lời giải (bài lọ dung dịch). Bản cũ lưu ở data/luu_tru/L10_C9_luu_tru.py.
# Bản mới: cùng ID, cùng bối cảnh; mỗi ý >= 3 phát biểu đúng, >= 3 phát biểu sai (sai theo các lỗi khác nhau), lời
# giải đủ; xác suất tính bằng phân số chính xác (Fraction) theo định nghĩa cổ điển (Bài 26, 27 SGK KNTT 10).
# =====================================================================
from fractions import Fraction as _Fr9


def _tf9_ps(x):
    """Phân số tối giản dạng LaTeX (không có $)."""
    x = _Fr9(x)
    if x.denominator == 1:
        return "%d" % x.numerator
    return r"\dfrac{%d}{%d}" % (x.numerator, x.denominator)


def _tf9_C(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


class _Tf9Lai(Exception):
    """Bộ số này không tạo đủ phát biểu sai khác phát biểu đúng - chọn bộ số khác."""


def _tf9_y(dung, sai):
    """Một ý: dung/sai là danh sách (phát biểu, lời giải). Cần >= 3 mỗi loại, phát biểu không trùng nhau."""
    da, d2, s2 = set(), [], []
    for ds, ra in ((dung, d2), (sai, s2)):
        for p, g in ds:
            if p not in da:
                da.add(p)
                ra.append((p, g))
    if len(d2) < 3 or len(s2) < 3:
        raise _Tf9Lai()
    return ([(r"{\True %s}" % p, "Đúng. " + g) for p, g in d2] +
            [(r"{%s}" % p, "Sai. " + g) for p, g in s2])


def _tf9_xs(mo_ta, dung, sai_ds, ly):
    """Phát biểu "Xác suất để <mo_ta> bằng X": một phát biểu đúng + các phát biểu sai có giá trị KHÁC giá trị đúng."""
    mau = r"Xác suất để %s bằng $%s$"
    d = [(mau % (mo_ta, _tf9_ps(dung)), ly)]
    s = [(mau % (mo_ta, _tf9_ps(x)), ly) for x in dict.fromkeys(_Fr9(v) for v in sai_ds)
         if x != _Fr9(dung) and 0 <= x <= 1]
    return d, s


def _tf9_gop(*cap):
    d, s = [], []
    for a, b in cap:
        d += a
        s += b
    return d, s


# ---- Gieo dong thoi hai con xuc xac ----
# (tên cũ của cô: K10_9_DS_1_VD)
def L10_C9_TF_A_01(socau, socot=1):
    """Đúng/Sai - gieo đồng thời hai con xúc xắc cân đối."""
    cau, da_co, lan = "", set(), 0
    while len(da_co) < socau:
        lan += 1
        if lan > 500:
            raise RuntimeError("L10_C9_TF_A_01: không sinh đủ %d câu khác nhau" % socau)
        k = random.choice([5, 6, 8, 9, 10])          # tổng cần xét
        m = random.randint(1, 6)                     # mặt chấm cần xét
        t = random.choice([4, 5, 6, 8, 9])           # tổng "nhỏ hơn t"
        if (k, m, t) in da_co:
            continue
        dem = {s: 6 - abs(s - 7) for s in range(2, 13)}
        try:
            debai = r"Gieo đồng thời hai con xúc xắc cân đối và đồng chất. Xét tính đúng sai của các khẳng định sau:"
            # a) NB - nhận biết khái niệm: biến cố không thể, chắc chắn, biến cố đối, tính chất của xác suất
            y_a = _tf9_y(
                [(r"Biến cố ``Tổng số chấm bằng $13$'' là biến cố không thể",
                  r"Tổng số chấm lớn nhất là $6 + 6 = 12$ nên biến cố không bao giờ xảy ra."),
                 (r"Biến cố ``Tổng số chấm không vượt quá $12$'' là biến cố chắc chắn",
                  r"Tổng số chấm luôn thuộc $\{2; 3; \ldots; 12\}$ nên biến cố luôn xảy ra."),
                 (r"Biến cố ``Tổng số chấm là số chẵn'' và biến cố ``Tổng số chấm là số lẻ'' là hai biến cố đối nhau",
                  r"Mỗi kết quả có tổng hoặc chẵn hoặc lẻ, không thể cả hai."),
                 (r"Với mọi biến cố $A$ của phép thử thì $0 \le P(A) \le 1$",
                  r"Đây là tính chất cơ bản của xác suất.")],
                [(r"Biến cố ``Tổng số chấm bằng $13$'' là biến cố chắc chắn",
                  r"Tổng số chấm lớn nhất là $12$ nên đây là biến cố không thể."),
                 (r"Biến cố ``Tổng số chấm lớn hơn $1$'' là biến cố không thể",
                  r"Tổng số chấm nhỏ nhất là $2 > 1$ nên đây là biến cố chắc chắn."),
                 (r"Biến cố ``Tổng số chấm bằng $7$'' và biến cố ``Tổng số chấm bằng $8$'' là hai biến cố đối nhau",
                  r"Hai biến cố này không cùng xảy ra nhưng có kết quả (ví dụ tổng bằng $2$) không thuộc biến cố "
                  r"nào, nên chúng không phải hai biến cố đối nhau."),
                 (r"Nếu $\overline{A}$ là biến cố đối của $A$ thì $P(\overline{A}) = P(A) - 1$",
                  r"Đúng phải là $P(\overline{A}) = 1 - P(A)$.")])
            # b) TH - một bước: đếm không gian mẫu, đếm kết quả thuận lợi đơn giản
            ly_om = r"Mỗi con có $6$ kết quả nên $n(\Omega) = 6\cdot 6 = 36$."
            y_b = _tf9_y(
                [(r"Không gian mẫu có $36$ phần tử", ly_om),
                 (r"Biến cố ``Hai mặt xuất hiện có số chấm bằng nhau'' có $6$ kết quả thuận lợi",
                  r"Các kết quả là $(1;1), (2;2), \ldots, (6;6)$."),
                 (r"Xác suất để con xúc xắc thứ nhất xuất hiện mặt $%d$ chấm bằng $\dfrac{1}{6}$" % m,
                  r"Có $6$ kết quả $(%d; j)$ với $j = 1, \ldots, 6$ nên xác suất bằng $\dfrac{6}{36} = \dfrac{1}{6}$." % m)],
                [(r"Không gian mẫu có $12$ phần tử", ly_om),
                 (r"Không gian mẫu có $21$ phần tử", ly_om + r" Hai con xúc xắc là khác nhau nên $(1;2)$ và $(2;1)$ là hai kết quả khác nhau."),
                 (r"Biến cố ``Hai mặt xuất hiện có số chấm bằng nhau'' có $12$ kết quả thuận lợi",
                  r"Chỉ có $6$ kết quả $(1;1), (2;2), \ldots, (6;6)$."),
                 (r"Xác suất để con xúc xắc thứ nhất xuất hiện mặt $%d$ chấm bằng $\dfrac{1}{36}$" % m,
                  r"Có $6$ kết quả $(%d; j)$ nên xác suất bằng $\dfrac{6}{36} = \dfrac{1}{6}$." % m)])
            # c) VD - đếm kết quả thuận lợi của biến cố về tổng, tích rồi tính xác suất
            ly_k = (r"Tổng bằng $%d$ có $%d$ kết quả thuận lợi nên xác suất bằng $\dfrac{%d}{36} = %s$."
                    % (k, dem[k], dem[k], _tf9_ps(_Fr9(dem[k], 36))))
            ly_le = (r"Tích lẻ khi cả hai mặt đều lẻ: $3\cdot 3 = 9$ kết quả, xác suất $\dfrac{9}{36} = \dfrac{1}{4}$; "
                     r"tích chẵn có xác suất $1 - \dfrac{1}{4} = \dfrac{3}{4}$.")
            y_c = _tf9_y(*_tf9_gop(
                _tf9_xs(r"tổng số chấm bằng $%d$" % k, _Fr9(dem[k], 36),
                        [_Fr9(dem.get(k + 1, 0), 36), _Fr9(dem[k], 21), _Fr9(1, 11)], ly_k),
                _tf9_xs(r"tích số chấm là một số lẻ", _Fr9(1, 4), [_Fr9(1, 2), _Fr9(3, 4)], ly_le),
                _tf9_xs(r"tích số chấm là một số chẵn", _Fr9(3, 4), [_Fr9(1, 2), _Fr9(1, 4)], ly_le)))
            # d) VDC - nhiều bước: cộng nhiều trường hợp, dùng biến cố đối
            nho = sum(dem[s] for s in range(2, t))
            ly_t = (r"Tổng nhỏ hơn $%d$ gồm các tổng $2, \ldots, %d$ với $%s = %d$ kết quả, xác suất $%s$."
                    % (t, t - 1, " + ".join(str(dem[s]) for s in range(2, t)), nho, _tf9_ps(_Fr9(nho, 36))))
            ly_m = (r"Biến cố đối ``không con nào xuất hiện mặt $%d$ chấm'' có $5\cdot 5 = 25$ kết quả, nên xác suất "
                    r"cần tìm bằng $1 - \dfrac{25}{36} = \dfrac{11}{36}$." % m)
            ly_3 = (r"Tổng chia hết cho $3$ là $3, 6, 9, 12$ với $2 + 5 + 4 + 1 = 12$ kết quả, xác suất "
                    r"$\dfrac{12}{36} = \dfrac{1}{3}$.")
            y_d = _tf9_y(*_tf9_gop(
                _tf9_xs(r"tổng số chấm nhỏ hơn $%d$" % t, _Fr9(nho, 36),
                        [_Fr9(nho + dem[t], 36), _Fr9(t - 2, 36)], ly_t),
                _tf9_xs(r"có ít nhất một con xúc xắc xuất hiện mặt $%d$ chấm" % m, _Fr9(11, 36),
                        [_Fr9(1, 3), _Fr9(1, 6), _Fr9(25, 36)], ly_m),
                _tf9_xs(r"tổng số chấm chia hết cho $3$", _Fr9(1, 3), [_Fr9(1, 4), _Fr9(11, 36)], ly_3)))
        except _Tf9Lai:
            continue
        da_co.add((k, m, t))
        cau += TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], 0, 0, socot)
    return cau


# ---- Day nhi phan n bit ----
# (tên cũ của cô: K10_9_DS_2_VD)
def L10_C9_TF_B_01(socau, socot=1):
    """Đúng/Sai - chọn ngẫu nhiên một dãy nhị phân n bit."""
    cau, da_co, lan = "", set(), 0
    while len(da_co) < socau:
        lan += 1
        if lan > 500:
            raise RuntimeError("L10_C9_TF_B_01: không sinh đủ %d câu khác nhau" % socau)
        n = random.choice([6, 8, 10])
        k = random.randint(2, n - 2)                 # "đúng k chữ số 1"
        j = random.randint(2, n - 2)                 # "j chữ số 1 đứng liền nhau"
        if (n, k, j) in da_co:
            continue
        N = 2 ** n
        try:
            debai = (r"Dãy $\left(x_1, x_2, \ldots, x_{%d}\right)$, trong đó mỗi $x_i$ $(i = 1, 2, \ldots, %d)$ chỉ nhận "
                     r"giá trị $0$ hoặc $1$, được gọi là dãy nhị phân $%d$ bit. Chọn ngẫu nhiên một dãy nhị phân $%d$ bit. "
                     r"Xét tính đúng sai của các khẳng định sau:" % (n, n, n, n))
            # a) NB - nhận biết biến cố không thể, chắc chắn, biến cố đối
            y_a = _tf9_y(
                [(r"Biến cố ``Dãy có đúng $%d$ chữ số $1$'' là biến cố không thể" % (n + 1),
                  r"Dãy chỉ có $%d$ chữ số nên không thể có $%d$ chữ số $1$." % (n, n + 1)),
                 (r"Biến cố ``Dãy có không quá $%d$ chữ số $1$'' là biến cố chắc chắn" % n,
                  r"Dãy có $%d$ chữ số nên số chữ số $1$ luôn không quá $%d$." % (n, n)),
                 (r"Biến cố ``Dãy có ít nhất một chữ số $0$'' là biến cố đối của biến cố ``Dãy gồm toàn chữ số $1$''",
                  r"Một dãy hoặc gồm toàn chữ số $1$, hoặc có ít nhất một chữ số $0$, không thể cả hai.")],
                [(r"Biến cố ``Dãy có đúng $%d$ chữ số $1$'' là biến cố chắc chắn" % (n + 1),
                  r"Dãy chỉ có $%d$ chữ số nên đây là biến cố không thể." % n),
                 (r"Biến cố ``Dãy có không quá $%d$ chữ số $1$'' là biến cố không thể" % n,
                  r"Biến cố này luôn xảy ra, là biến cố chắc chắn."),
                 (r"Biến cố ``Dãy có ít nhất một chữ số $0$'' là biến cố đối của biến cố ``Dãy có ít nhất một chữ số $1$''",
                  r"Hai biến cố này cùng xảy ra với dãy $1\,0\,0\ldots 0$; biến cố đối của ``có ít nhất một chữ số $0$'' "
                  r"là ``gồm toàn chữ số $1$''.")])
            # b) TH - một bước: quy tắc nhân đếm số dãy
            ly_N = r"Mỗi vị trí có $2$ cách chọn nên có $2^{%d} = %d$ dãy." % (n, N)
            y_b = _tf9_y(
                [(r"Có $%d$ dãy nhị phân $%d$ bit" % (N, n), ly_N),
                 (r"Có đúng $1$ dãy gồm toàn chữ số $0$", r"Đó là dãy $0\,0\ldots 0$."),
                 (r"Có $%d$ dãy có $x_1 = 1$" % (N // 2), r"$x_1 = 1$, mỗi vị trí còn lại có $2$ cách nên có $2^{%d} = %d$ dãy."
                  % (n - 1, N // 2))],
                [(r"Có $%d$ dãy nhị phân $%d$ bit" % (2 * n, n), ly_N),
                 (r"Có $%d$ dãy nhị phân $%d$ bit" % (n * n, n), ly_N),
                 (r"Có $%d$ dãy có $x_1 = 1$" % (n - 1),
                  r"$x_1 = 1$, mỗi vị trí còn lại có $2$ cách nên có $2^{%d} = %d$ dãy." % (n - 1, N // 2))])
            # c) VD - xác suất theo định nghĩa cổ điển, đếm bằng tổ hợp
            ck = _tf9_C(n, k)
            ly_k = (r"Chọn $%d$ vị trí trong $%d$ vị trí để đặt chữ số $1$: $C_{%d}^{%d} = %d$ dãy, xác suất "
                    r"$\dfrac{%d}{%d} = %s$." % (k, n, n, k, ck, ck, N, _tf9_ps(_Fr9(ck, N))))
            ly_dx = (r"Chọn tuỳ ý $x_1, \ldots, x_{%d}$, các chữ số còn lại xác định theo đối xứng: $2^{%d}$ dãy, xác suất "
                     r"$%s$." % (n // 2, n // 2, _tf9_ps(_Fr9(2 ** (n // 2), N))))
            ly_dc = r"Chọn tuỳ ý $x_1, \ldots, x_{%d}$ rồi lấy $x_{%d} = x_1$: $2^{%d}$ dãy, xác suất $\dfrac{1}{2}$." % (n - 1, n, n - 1)
            y_c = _tf9_y(*_tf9_gop(
                _tf9_xs(r"dãy có đúng $%d$ chữ số $1$" % k, _Fr9(ck, N),
                        [_Fr9(math.perm(n, k), N), _Fr9(_tf9_C(n, k - 1), N), _Fr9(k, n)], ly_k),
                _tf9_xs(r"đọc dãy từ trái sang phải hay từ phải sang trái đều như nhau", _Fr9(2 ** (n // 2), N),
                        [_Fr9(1, N), _Fr9(1, 2), _Fr9(n // 2, N)], ly_dx),
                _tf9_xs(r"$x_1 = x_{%d}$" % n, _Fr9(1, 2), [_Fr9(1, 4), _Fr9(2, N)], ly_dc)))
            # d) VDC - đếm có điều kiện (liền nhau, không kề nhau), biến cố đối
            ly_j = (r"$%d$ chữ số $1$ đứng liền nhau tạo một khối, khối đó bắt đầu ở một trong $%d - %d + 1 = %d$ vị trí, "
                    r"xác suất $%s$." % (j, n, j, n - j + 1, _tf9_ps(_Fr9(n - j + 1, N))))
            kk = _tf9_C(n - 1, 2)
            ly_kk = (r"Có $C_{%d}^{2} = %d$ cách chọn hai vị trí cho hai chữ số $1$, trong đó $%d$ cách hai vị trí kề nhau, "
                     r"còn $%d$ cách, xác suất $%s$." % (n, _tf9_C(n, 2), n - 1, kk, _tf9_ps(_Fr9(kk, N))))
            ly_1 = r"Biến cố đối là ``dãy gồm toàn chữ số $0$'' (một dãy), nên xác suất bằng $1 - \dfrac{1}{%d} = %s$." % (
                N, _tf9_ps(_Fr9(N - 1, N)))
            y_d = _tf9_y(*_tf9_gop(
                _tf9_xs(r"dãy có đúng $%d$ chữ số $1$ và các chữ số $1$ đứng liền nhau" % j, _Fr9(n - j + 1, N),
                        [_Fr9(n - j, N), _Fr9(_tf9_C(n, j), N), _Fr9(n, N)], ly_j),
                _tf9_xs(r"dãy có đúng hai chữ số $1$ và hai chữ số $1$ này không đứng cạnh nhau", _Fr9(kk, N),
                        [_Fr9(_tf9_C(n, 2), N), _Fr9(n - 1, N)], ly_kk),
                _tf9_xs(r"dãy có ít nhất một chữ số $1$", _Fr9(N - 1, N), [_Fr9(1, N), _Fr9(1, 2)], ly_1)))
        except _Tf9Lai:
            continue
        da_co.add((n, k, j))
        cau += TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], 0, 0, socot)
    return cau


def _tf9_banh_xe(socau, socot, k_lan):
    """Quay bánh xe k_lan lần (mỗi lần mũi tên dừng ngẫu nhiên ở một trong n vị trí như nhau, các lần độc lập)."""
    cau, da_co, lan = "", set(), 0
    CHU = {2: "hai", 3: "ba"}
    while len(da_co) < socau:
        lan += 1
        if lan > 500:
            raise RuntimeError("bánh xe: không sinh đủ %d câu khác nhau" % socau)
        n = random.choice([6, 8, 10, 12])
        m = random.randint(2, n - 2)
        if (n, m) in da_co:
            continue
        k, t = k_lan, n - m
        Om = n ** k
        try:
            debai = (r"Mũi tên của bánh xe trong một trò chơi có thể dừng lại ở một trong $%d$ vị trí với khả năng như "
                     r"nhau; trong đó $%d$ vị trí được cộng điểm, $%d$ vị trí bị trừ điểm. Một người chơi quay bánh xe "
                     r"%s lần. Xét tính đúng sai của các khẳng định sau:" % (n, m, t, CHU[k]))
            # a) NB - nhận biết phép thử ngẫu nhiên, biến cố đối, tính chất xác suất
            y_a = _tf9_y(
                [(r"Việc quay bánh xe %s lần là một phép thử ngẫu nhiên" % CHU[k],
                  r"Không biết trước mũi tên sẽ dừng ở đâu."),
                 (r"Biến cố ``Cả %s lần đều được cộng điểm'' và biến cố ``Có ít nhất một lần bị trừ điểm'' là hai biến cố "
                  r"đối nhau" % CHU[k], r"Mỗi kết quả thuộc đúng một trong hai biến cố đó."),
                 (r"Nếu $A$ là một biến cố thì $P(\overline{A}) = 1 - P(A)$", r"Đây là công thức xác suất của biến cố đối.")],
                [(r"Việc quay bánh xe %s lần không phải là phép thử ngẫu nhiên vì đã biết bánh xe có $%d$ vị trí"
                  % (CHU[k], n), r"Biết các kết quả có thể nhưng không biết trước kết quả nào xảy ra."),
                 (r"Biến cố ``Cả %s lần đều được cộng điểm'' và biến cố ``Cả %s lần đều bị trừ điểm'' là hai biến cố đối "
                  r"nhau" % (CHU[k], CHU[k]), r"Còn các kết quả vừa có lần cộng vừa có lần trừ không thuộc biến cố nào."),
                 (r"Nếu $A$ là một biến cố thì $P(\overline{A}) = P(A) - 1$", r"Đúng phải là $P(\overline{A}) = 1 - P(A)$.")])
            # b) TH - một bước: quy tắc nhân đếm không gian mẫu và kết quả thuận lợi
            ly_om = r"Mỗi lần quay có $%d$ kết quả nên $n(\Omega) = %d^{%d} = %d$." % (n, n, k, Om)
            ly_c = r"Mỗi lần quay có $%d$ vị trí cộng điểm nên có $%d^{%d} = %d$ kết quả." % (m, m, k, m ** k)
            y_b = _tf9_y(
                [(r"Không gian mẫu có $%d$ phần tử" % Om, ly_om),
                 (r"Biến cố ``Cả %s lần đều được cộng điểm'' có $%d$ kết quả thuận lợi" % (CHU[k], m ** k), ly_c),
                 (r"Xác suất để lần quay đầu tiên được cộng điểm bằng $%s$" % _tf9_ps(_Fr9(m, n)),
                  r"Lần đầu có $%d$ vị trí cộng điểm trong $%d$ vị trí." % (m, n))],
                [x for x in [(r"Không gian mẫu có $%d$ phần tử" % (k * n), ly_om),
                             (r"Không gian mẫu có $%d$ phần tử" % math.perm(n, k), ly_om + r" Các lần quay có thể dừng ở cùng một vị trí."),
                             (r"Biến cố ``Cả %s lần đều được cộng điểm'' có $%d$ kết quả thuận lợi" % (CHU[k], k * m), ly_c),
                             (r"Xác suất để lần quay đầu tiên được cộng điểm bằng $%s$" % _tf9_ps(_Fr9(m, Om)),
                              r"Lần đầu có $%d$ vị trí cộng điểm trong $%d$ vị trí, xác suất $%s$." % (m, n, _tf9_ps(_Fr9(m, n))))]
                 if not (r"$%d$ phần tử" % Om in x[0]) and not (r"$%d$ kết quả thuận lợi" % m ** k in x[0])])
            # c) VD - xác suất các biến cố "đều cộng", "đều trừ", "các vị trí đôi một khác nhau"
            ly_cc = r"$P = \dfrac{%d^{%d}}{%d^{%d}} = %s$." % (m, k, n, k, _tf9_ps(_Fr9(m ** k, Om)))
            ly_tt = r"$P = \dfrac{%d^{%d}}{%d^{%d}} = %s$." % (t, k, n, k, _tf9_ps(_Fr9(t ** k, Om)))
            kn = math.perm(n, k)
            ly_kn = (r"Số kết quả các lần dừng ở các vị trí đôi một khác nhau là $A_{%d}^{%d} = %d$, nên "
                     r"$P = \dfrac{%d}{%d} = %s$." % (n, k, kn, kn, Om, _tf9_ps(_Fr9(kn, Om))))
            y_c = _tf9_y(*_tf9_gop(
                _tf9_xs(r"cả %s lần đều được cộng điểm" % CHU[k], _Fr9(m ** k, Om), [_Fr9(m, n), _Fr9(k * m, Om)], ly_cc),
                _tf9_xs(r"cả %s lần đều bị trừ điểm" % CHU[k], _Fr9(t ** k, Om), [_Fr9(t, n), _Fr9(k * t, Om)], ly_tt),
                _tf9_xs(r"%s lần quay dừng ở %s vị trí đôi một khác nhau" % (CHU[k], CHU[k]), _Fr9(kn, Om),
                        [_Fr9(_tf9_C(n, k), Om), _Fr9(1, n)], ly_kn)))
            # d) VDC - nhiều bước: biến cố đối, đếm theo vị trí của lần trừ điểm
            ly_it = (r"Biến cố đối là ``cả %s lần đều được cộng điểm'' nên $P = 1 - %s = %s$."
                     % (CHU[k], _tf9_ps(_Fr9(m ** k, Om)), _tf9_ps(1 - _Fr9(m ** k, Om))))
            mot = k * m ** (k - 1) * t
            ly_mot = (r"Chọn lần bị trừ điểm: $%d$ cách; lần đó có $%d$ vị trí, %s có $%d$ vị trí cộng điểm: "
                      r"$%d\cdot %d\cdot %d^{%d} = %d$ kết quả, $P = %s$."
                      % (k, t, "lần còn lại" if k == 2 else "mỗi lần trong hai lần còn lại", m, k, t, m, k - 1, mot,
                         _tf9_ps(_Fr9(mot, Om))))
            cung = m ** k + t ** k
            ly_cung = (r"Cùng loại là ``đều cộng'' hoặc ``đều trừ'': $%d^{%d} + %d^{%d} = %d$ kết quả, $P = %s$."
                       % (m, k, t, k, cung, _tf9_ps(_Fr9(cung, Om))))
            y_d = _tf9_y(*_tf9_gop(
                _tf9_xs(r"có ít nhất một lần bị trừ điểm", 1 - _Fr9(m ** k, Om),
                        [_Fr9(t ** k, Om), _Fr9(t, n), 1 - _Fr9(m, n)], ly_it),
                _tf9_xs(r"có đúng một lần bị trừ điểm", _Fr9(mot, Om),
                        [_Fr9(m ** (k - 1) * t, Om), _Fr9(t, n), _Fr9(k * t, Om)], ly_mot),
                _tf9_xs(r"các lần quay đều cùng một loại (cùng được cộng điểm hoặc cùng bị trừ điểm)", _Fr9(cung, Om),
                        [_Fr9(m ** k, Om), _Fr9(cung, 2 * Om), _Fr9(2, n)], ly_cung)))
        except _Tf9Lai:
            continue
        da_co.add((n, m))
        cau += TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], 0, 0, socot)
    return cau


# ---- Quay banh xe ba lan (van dung cao) ----
# (tên cũ của cô: K10_9_DS_3_VDC)
def L10_C9_TF_C_01(socau, socot=1):
    """Đúng/Sai - quay bánh xe ba lần (vận dụng cao). Các ý viết trong _tf9_banh_xe (dùng chung với TF_D)."""
    # a) NB - phép thử ngẫu nhiên, biến cố đối, P(A đối) = 1 - P(A)
    # b) TH - đếm không gian mẫu n^3 và số kết quả thuận lợi bằng quy tắc nhân
    # c) VD - xác suất "đều cộng", "đều trừ", "ba vị trí đôi một khác nhau"
    # d) VDC - "ít nhất một lần trừ" (biến cố đối), "đúng một lần trừ", "cùng một loại"
    return _tf9_banh_xe(socau, socot, 3)


# ---- Quay banh xe hai lan ----
# (tên cũ của cô: K10_9_DS_4_VD)
def L10_C9_TF_D_01(socau, socot=1):
    """Đúng/Sai - quay bánh xe hai lần."""
    # a) NB - phép thử ngẫu nhiên, biến cố đối, P(A đối) = 1 - P(A)
    # b) TH - đếm không gian mẫu n^2 và số kết quả thuận lợi bằng quy tắc nhân
    # c) VD - xác suất "đều cộng", "đều trừ", "hai vị trí khác nhau"
    # d) VDC - "ít nhất một lần trừ" (biến cố đối), "đúng một lần trừ", "cùng một loại"
    return _tf9_banh_xe(socau, socot, 2)


# ---- Cac lo dung dich axit / bazo ----
def L10_C9_TF_E_01(socau, socot=1):
    """Đúng/Sai - chọn hai lọ dung dịch, nhúng giấy quỳ tím."""
    cau, da_co, lan = "", set(), 0
    while len(da_co) < socau:
        lan += 1
        if lan > 500:
            raise RuntimeError("L10_C9_TF_E_01: không sinh đủ %d câu khác nhau" % socau)
        a, b, c = random.sample(range(3, 10), 3)
        if (a, b, c) in da_co:
            continue
        N = a + b + c
        Om = _tf9_C(N, 2)
        try:
            debai = (r"Có $%d$ lọ dung dịch có tính axit, $%d$ lọ dung dịch có tính bazơ và $%d$ lọ dung dịch trung tính. "
                     r"Chọn ngẫu nhiên đồng thời hai lọ rồi nhúng vào mỗi lọ một mảnh giấy quỳ tím (giấy quỳ tím hoá đỏ "
                     r"trong dung dịch axit, hoá xanh trong dung dịch bazơ, không đổi màu trong dung dịch trung tính). "
                     r"Xét tính đúng sai của các khẳng định sau:" % (a, b, c))
            # a) NB - nhận biết phép thử, không gian mẫu, biến cố chắc chắn / không thể
            y_a = _tf9_y(
                [(r"Không gian mẫu của phép thử là tập hợp tất cả các kết quả có thể xảy ra của phép thử",
                  r"Đó là định nghĩa không gian mẫu."),
                 (r"Phép thử ngẫu nhiên là phép thử mà ta không biết trước được kết quả của nó",
                  r"Đó là định nghĩa phép thử ngẫu nhiên."),
                 (r"Xác suất của biến cố chắc chắn bằng $1$", r"Đó là tính chất cơ bản của xác suất.")],
                [(r"Phép thử ngẫu nhiên là phép thử mà ta biết trước được kết quả của nó",
                  r"Phép thử ngẫu nhiên là phép thử mà ta KHÔNG biết trước được kết quả."),
                 (r"Xác suất của biến cố không thể bằng $1$", r"Xác suất của biến cố không thể bằng $0$."),
                 (r"Biến cố ``Cả hai mảnh giấy quỳ đều hoá đỏ'' là biến cố chắc chắn",
                  r"Có thể chọn được lọ không phải axit, nên biến cố không phải lúc nào cũng xảy ra.")])
            # b) TH - một bước: đếm bằng tổ hợp chập 2
            ly_om = r"Chọn $2$ lọ trong $%d$ lọ: $n(\Omega) = C_{%d}^{2} = %d$." % (N, N, Om)
            y_b = _tf9_y(
                [(r"Không gian mẫu có $%d$ phần tử" % Om, ly_om),
                 (r"Biến cố ``Cả hai mảnh giấy quỳ đều hoá đỏ'' có $%d$ kết quả thuận lợi" % _tf9_C(a, 2),
                  r"Chọn $2$ lọ trong $%d$ lọ axit: $C_{%d}^{2} = %d$." % (a, a, _tf9_C(a, 2))),
                 (r"Biến cố ``Cả hai mảnh giấy quỳ đều không đổi màu'' có $%d$ kết quả thuận lợi" % _tf9_C(c, 2),
                  r"Chọn $2$ lọ trong $%d$ lọ trung tính: $C_{%d}^{2} = %d$." % (c, c, _tf9_C(c, 2)))],
                [(r"Không gian mẫu có $%d$ phần tử" % (N * N), ly_om),
                 (r"Không gian mẫu có $%d$ phần tử" % (2 * N), ly_om),
                 (r"Biến cố ``Cả hai mảnh giấy quỳ đều hoá đỏ'' có $%d$ kết quả thuận lợi" % (a * a),
                  r"Chọn $2$ lọ khác nhau trong $%d$ lọ axit: $C_{%d}^{2} = %d$." % (a, a, _tf9_C(a, 2))),
                 (r"Biến cố ``Cả hai mảnh giấy quỳ đều không đổi màu'' có $%d$ kết quả thuận lợi" % (2 * c),
                  r"Chọn $2$ lọ trong $%d$ lọ trung tính: $C_{%d}^{2} = %d$." % (c, c, _tf9_C(c, 2)))])
            # c) VD - xác suất theo định nghĩa cổ điển
            dd, xx, kk = _tf9_C(a, 2), _tf9_C(b, 2), _tf9_C(c, 2)
            ly = lambda so, ten: r"%s: $P = \dfrac{%d}{%d} = %s$." % (ten, so, Om, _tf9_ps(_Fr9(so, Om)))
            y_c = _tf9_y(*_tf9_gop(
                _tf9_xs(r"cả hai mảnh giấy quỳ đều hoá đỏ", _Fr9(dd, Om), [_Fr9(xx, Om), _Fr9(a, N), _Fr9(dd, N * N)],
                        ly(dd, r"Có $C_{%d}^{2} = %d$ cách chọn hai lọ axit" % (a, dd))),
                _tf9_xs(r"cả hai mảnh giấy quỳ đều hoá xanh", _Fr9(xx, Om), [_Fr9(dd, Om), _Fr9(b, N), _Fr9(xx, N * N)],
                        ly(xx, r"Có $C_{%d}^{2} = %d$ cách chọn hai lọ bazơ" % (b, xx))),
                _tf9_xs(r"hai mảnh giấy quỳ có cùng màu", _Fr9(dd + xx + kk, Om), [_Fr9(dd + xx, Om), _Fr9(3, N)],
                        ly(dd + xx + kk, r"Cùng màu khi hai lọ cùng loại: $%d + %d + %d = %d$ cách" % (dd, xx, kk, dd + xx + kk)))))
            # d) VDC - nhiều bước: biến cố đối, đếm hai loại khác nhau
            kd = _tf9_C(N - a, 2)
            ly_it = (r"Biến cố đối ``không mảnh nào hoá đỏ'' (hai lọ đều không phải axit) có $C_{%d}^{2} = %d$ kết quả, "
                     r"nên $P = 1 - \dfrac{%d}{%d} = %s$." % (N - a, kd, kd, Om, _tf9_ps(1 - _Fr9(kd, Om))))
            ly_kh = (r"Biến cố đối là ``hai mảnh cùng màu'' có $%d$ kết quả, nên $P = 1 - \dfrac{%d}{%d} = %s$."
                     % (dd + xx + kk, dd + xx + kk, Om, _tf9_ps(1 - _Fr9(dd + xx + kk, Om))))
            ly_dx = r"Chọn một lọ axit và một lọ bazơ: $%d\cdot %d = %d$ cách, $P = %s$." % (a, b, a * b, _tf9_ps(_Fr9(a * b, Om)))
            y_d = _tf9_y(*_tf9_gop(
                _tf9_xs(r"có ít nhất một mảnh giấy quỳ hoá đỏ", 1 - _Fr9(kd, Om), [_Fr9(dd, Om), _Fr9(kd, Om), _Fr9(a, N)], ly_it),
                _tf9_xs(r"hai mảnh giấy quỳ có màu khác nhau", 1 - _Fr9(dd + xx + kk, Om),
                        [_Fr9(a * b, Om), _Fr9(dd + xx + kk, Om)], ly_kh),
                _tf9_xs(r"một mảnh hoá đỏ và một mảnh hoá xanh", _Fr9(a * b, Om), [_Fr9(2 * a * b, Om), _Fr9(a * b, N * N),
                                                                                 _Fr9(a + b, Om)], ly_dx)))
        except _Tf9Lai:
            continue
        da_co.add((a, b, c))
        cau += TF_baitoan_du(debai, [y_a, y_b, y_c, y_d], 0, 0, socot)
    return cau


# =====================================================================
# BỔ SUNG CÁC DẠNG NHẬN BIẾT CHO CHƯƠNG 9 (29/09/2026)
# ---------------------------------------------------------------------
# Ma trận đề hệ số 1 đòi các câu nhận biết khái niệm xác suất, nhưng
# ngân hàng mới chỉ có các câu tính toán mức TH/VD. Khối này viết đủ
# các câu nhận biết còn thiếu, nhờ đó chương 9 ra được đề hệ số 1.
# =====================================================================
import random as _rd


def _ba_nhieu9(dapso, ung_vien, buoc=None):
    """Ba phương án nhiễu đôi một khác nhau và khác đáp số."""
    ds = []
    for v in ung_vien:
        if v != dapso and v not in ds:
            ds.append(v)
        if len(ds) == 3:
            return ds
    k = 1
    while len(ds) < 3:
        v = buoc(k) if buoc else str(k)
        if v != dapso and v not in ds:
            ds.append(v)
        k += 1
    return ds


def L10_C9_B26_NB142_MC_A_01(socau, dang=1):
    """Nhận biết phép thử ngẫu nhiên."""
    NGAU_NHIEN = ["Gieo một con xúc xắc cân đối và quan sát số chấm xuất hiện",
                  "Tung một đồng xu và quan sát mặt xuất hiện",
                  "Rút ngẫu nhiên một tấm thẻ từ hộp có 10 tấm thẻ đánh số",
                  "Chọn ngẫu nhiên một học sinh trong lớp và xem bạn đó là nam hay nữ"]
    KHONG = ["Đun nước ở điều kiện thường đến $100^{\\circ}\\mathrm{C}$ và quan sát nước có sôi hay không",
             "Tính tổng hai số tự nhiên $3$ và $5$",
             "Đo chiều dài của một chiếc bàn bằng thước",
             "Thả một hòn đá từ trên cao và quan sát nó rơi xuống hay bay lên",
             "Cộng hai số chẵn và xét xem kết quả có chẵn không"]
    gt = []
    while len(gt) < socau:
        v = (_rd.randrange(len(NGAU_NHIEN)), tuple(_rd.sample(range(len(KHONG)), 3)))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for i, bo in gt:
        dung = NGAU_NHIEN[i]
        giai = (r"Phép thử ngẫu nhiên là phép thử mà ta \textbf{không đoán trước được} "
                r"kết quả của nó, tuy vẫn biết tập hợp tất cả các kết quả có thể xảy ra.\\ "
                r"$\bullet$ ``%s'': không biết trước kết quả nào sẽ xảy ra, nên đây là "
                r"phép thử ngẫu nhiên.\\ "
                r"$\bullet$ Các hoạt động còn lại đều cho kết quả \textbf{biết trước}, "
                r"không phải phép thử ngẫu nhiên." % dung)
        cauTN += MC_SA_answer_text(
            r"Trong các hoạt động sau, hoạt động nào là một \textbf{phép thử ngẫu nhiên}?",
            dung, [KHONG[j] for j in bo], giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_NB143_MC_A_01(socau, dang=1):
    """Nhận biết không gian mẫu của một phép thử đơn giản."""
    gt = []
    while len(gt) < socau:
        v = _rd.choice(["xucxac", "dongxu", "the"])
        n = _rd.randint(5, 12)
        if (v, n) not in gt:
            gt.append((v, n))

    cauTN = ''
    for loai, n in gt:
        if loai == "xucxac":
            debai = (r"Gieo một con xúc xắc cân đối và quan sát số chấm xuất hiện. "
                     r"Không gian mẫu của phép thử là")
            dung = r"$\Omega = \left\{1; 2; 3; 4; 5; 6\right\}$"
            nhieu = [r"$\Omega = \left\{1; 2; 3; 4; 5\right\}$",
                     r"$\Omega = \left\{0; 1; 2; 3; 4; 5; 6\right\}$",
                     r"$\Omega = \left\{2; 4; 6\right\}$"]
            giai = (r"Không gian mẫu là tập hợp \textbf{tất cả} các kết quả có thể xảy ra "
                    r"của phép thử.\\ Con xúc xắc có sáu mặt, số chấm từ $1$ đến $6$, nên "
                    r"$\Omega = \left\{1; 2; 3; 4; 5; 6\right\}$ và $n\left(\Omega\right) = 6$.")
        elif loai == "dongxu":
            debai = (r"Tung một đồng xu cân đối và quan sát mặt xuất hiện "
                     r"($S$: mặt sấp, $N$: mặt ngửa). Không gian mẫu của phép thử là")
            dung = r"$\Omega = \left\{S; N\right\}$"
            nhieu = [r"$\Omega = \left\{S\right\}$", r"$\Omega = \left\{N\right\}$",
                     r"$\Omega = \left\{S; N; SN\right\}$"]
            giai = (r"Tung một đồng xu chỉ có hai kết quả có thể xảy ra là sấp hoặc ngửa, "
                    r"nên $\Omega = \left\{S; N\right\}$ và $n\left(\Omega\right) = 2$.")
        else:
            debai = (r"Một hộp có $%d$ tấm thẻ được đánh số từ $1$ đến $%d$. Rút ngẫu nhiên "
                     r"một tấm thẻ. Số phần tử của không gian mẫu là" % (n, n))
            dung = r"$%d$" % n
            nhieu = [r"$%d$" % (n - 1), r"$%d$" % (n + 1), r"$%d$" % (2 * n)]
            giai = (r"Mỗi kết quả của phép thử là rút được một tấm thẻ, mà có $%d$ tấm thẻ "
                    r"khác nhau nên $n\left(\Omega\right) = %d$." % (n, n))
        cauTN += MC_SA_answer_text(debai, dung, _ba_nhieu9(dung, nhieu), giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_NB145_MC_A_01(socau, dang=1):
    """Nhận biết biến cố không thể."""
    gt = []
    while len(gt) < socau:
        m = _rd.randint(7, 12)
        if m not in gt:
            gt.append(m)

    cauTN = ''
    for m in gt:
        debai = (r"Gieo một con xúc xắc cân đối. Biến cố nào sau đây là "
                 r"\textbf{biến cố không thể}?")
        dung = r"``Số chấm xuất hiện bằng $%d$''" % m
        nhieu = [r"``Số chấm xuất hiện là số chẵn''",
                 r"``Số chấm xuất hiện lớn hơn $4$''",
                 r"``Số chấm xuất hiện nhỏ hơn $7$''"]
        giai = (r"Biến cố không thể là biến cố \textbf{không bao giờ xảy ra}.\\ "
                r"Con xúc xắc chỉ có số chấm từ $1$ đến $6$, nên ``số chấm bằng $%d$'' "
                r"không bao giờ xảy ra: đó là biến cố không thể.\\ "
                r"Các biến cố còn lại đều có thể xảy ra (riêng ``nhỏ hơn $7$'' thì luôn "
                r"xảy ra, là biến cố chắc chắn)." % m)
        cauTN += MC_SA_answer_text(debai, dung, _ba_nhieu9(dung, nhieu), giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_NB146_MC_A_01(socau, dang=1):
    """Nhận biết biến cố chắc chắn."""
    gt = []
    while len(gt) < socau:
        m = _rd.randint(7, 12)
        if m not in gt:
            gt.append(m)

    cauTN = ''
    for m in gt:
        debai = (r"Gieo một con xúc xắc cân đối. Biến cố nào sau đây là "
                 r"\textbf{biến cố chắc chắn}?")
        dung = r"``Số chấm xuất hiện nhỏ hơn $%d$''" % m
        nhieu = [r"``Số chấm xuất hiện là số lẻ''",
                 r"``Số chấm xuất hiện lớn hơn $%d$''" % m,
                 r"``Số chấm xuất hiện bằng $6$''"]
        giai = (r"Biến cố chắc chắn là biến cố \textbf{luôn xảy ra} trong mọi kết quả của "
                r"phép thử.\\ "
                r"Số chấm của con xúc xắc chỉ từ $1$ đến $6$, mà $6 < %d$, nên ``số chấm "
                r"nhỏ hơn $%d$'' luôn đúng: đó là biến cố chắc chắn.\\ "
                r"Còn ``lớn hơn $%d$'' thì không bao giờ xảy ra (biến cố không thể), hai "
                r"biến cố kia thì lúc xảy ra lúc không." % (m, m, m))
        cauTN += MC_SA_answer_text(debai, dung, _ba_nhieu9(dung, nhieu), giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_NB147_MC_A_01(socau, dang=1):
    """Nhận biết biến cố đối."""
    CAP = [("số chấm xuất hiện là số chẵn", "số chấm xuất hiện là số lẻ"),
           ("số chấm xuất hiện lớn hơn $4$", "số chấm xuất hiện nhỏ hơn hoặc bằng $4$"),
           ("số chấm xuất hiện là $6$", "số chấm xuất hiện khác $6$"),
           ("số chấm xuất hiện chia hết cho $3$", "số chấm xuất hiện không chia hết cho $3$")]
    gt = []
    while len(gt) < socau:
        i = _rd.randrange(len(CAP))
        if i not in gt:
            gt.append(i)

    cauTN = ''
    for i in gt:
        A, doi = CAP[i]
        khac = [CAP[j][0] for j in range(len(CAP)) if j != i]
        debai = (r"Gieo một con xúc xắc cân đối. Gọi $A$ là biến cố ``%s''. "
                 r"Biến cố đối $\overline{A}$ của $A$ là" % A)
        dung = r"``%s''" % doi
        nhieu = [r"``%s''" % t for t in khac] + [r"``số chấm xuất hiện bằng $7$''"]
        giai = (r"Biến cố đối $\overline{A}$ gồm \textbf{tất cả} các kết quả của không gian "
                r"mẫu mà $A$ \textbf{không} xảy ra.\\ "
                r"$A$ là ``%s'' nên $\overline{A}$ là ``%s''.\\ "
                r"Lưu ý: $\overline{A}$ phải phủ kín phần còn lại của không gian mẫu, "
                r"chứ không phải một biến cố tuỳ ý khác." % (A, doi))
        cauTN += MC_SA_answer_text(debai, dung, _ba_nhieu9(dung, nhieu), giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_NB148_MC_A_01(socau, dang=1):
    """Nhận biết nguyên lí xác suất bé."""
    gt = list(range(socau))
    cauTN = ''
    for _ in gt:
        debai = (r"Theo \textbf{nguyên lí xác suất bé}, khẳng định nào sau đây đúng?")
        dung = (r"Nếu một biến cố có xác suất rất bé thì trong một phép thử, "
                r"biến cố đó \textbf{gần như không xảy ra}")
        nhieu = [r"Nếu một biến cố có xác suất rất bé thì biến cố đó \textbf{không bao giờ} xảy ra",
                 r"Nếu một biến cố có xác suất rất bé thì biến cố đó \textbf{chắc chắn} xảy ra",
                 r"Nếu một biến cố có xác suất rất bé thì xác suất của biến cố đối của nó cũng rất bé"]
        giai = (r"Nguyên lí xác suất bé: nếu một biến cố có xác suất \textbf{rất bé} thì "
                r"trong một phép thử, biến cố đó \textbf{gần như không xảy ra}.\\ "
                r"$\bullet$ Không được nói ``không bao giờ xảy ra'': xác suất bé vẫn khác $0$, "
                r"biến cố vẫn có thể xảy ra.\\ "
                r"$\bullet$ Nếu $P\left(A\right)$ rất bé thì $P\left(\overline{A}\right) "
                r"= 1 - P\left(A\right)$ lại rất \textbf{gần} $1$, không hề bé.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_NB149_MC_A_01(socau, dang=1):
    """Nhận biết định nghĩa cổ điển của xác suất."""
    gt = list(range(socau))
    cauTN = ''
    for _ in gt:
        debai = (r"Cho phép thử có không gian mẫu $\Omega$ gồm hữu hạn kết quả \textbf{đồng "
                 r"khả năng}, và $E$ là một biến cố. Theo định nghĩa cổ điển, xác suất của "
                 r"biến cố $E$ được tính bằng")
        dung = r"$P\left(E\right) = \dfrac{n\left(E\right)}{n\left(\Omega\right)}$"
        nhieu = [r"$P\left(E\right) = \dfrac{n\left(\Omega\right)}{n\left(E\right)}$",
                 r"$P\left(E\right) = n\left(E\right)\cdot n\left(\Omega\right)$",
                 r"$P\left(E\right) = n\left(\Omega\right) - n\left(E\right)$"]
        giai = (r"Định nghĩa cổ điển của xác suất: khi các kết quả của phép thử là đồng khả "
                r"năng thì\\ "
                r"$P\left(E\right) = \dfrac{n\left(E\right)}{n\left(\Omega\right)} "
                r"= \dfrac{\text{số kết quả thuận lợi cho } E}{\text{số kết quả có thể xảy ra}}$.\\ "
                r"Vì $n\left(E\right) \le n\left(\Omega\right)$ nên luôn có "
                r"$0 \le P\left(E\right) \le 1$; các công thức còn lại không bảo đảm điều này.")
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C9_B27_NB153_MC_A_01(socau, dang=1):
    """Mô tả các tính chất cơ bản của xác suất."""
    DUNG = [r"$0 \le P\left(E\right) \le 1$ với mọi biến cố $E$",
            r"$P\left(\Omega\right) = 1$",
            r"$P\left(\varnothing\right) = 0$",
            r"$P\left(\overline{E}\right) = 1 - P\left(E\right)$"]
    SAI = [r"$P\left(E\right)$ có thể lớn hơn $1$",
           r"$P\left(\Omega\right) = 0$",
           r"$P\left(\varnothing\right) = 1$",
           r"$P\left(\overline{E}\right) = P\left(E\right) - 1$",
           r"$P\left(E\right)$ có thể là một số âm"]
    gt = []
    while len(gt) < socau:
        v = (_rd.randrange(len(DUNG)), tuple(_rd.sample(range(len(SAI)), 3)))
        if v not in gt:
            gt.append(v)

    cauTN = ''
    for i, bo in gt:
        dung = DUNG[i]
        giai = (r"Các tính chất cơ bản của xác suất:\\ "
                r"$\bullet$ $0 \le P\left(E\right) \le 1$ với mọi biến cố $E$;\\ "
                r"$\bullet$ $P\left(\Omega\right) = 1$ (biến cố chắc chắn) và "
                r"$P\left(\varnothing\right) = 0$ (biến cố không thể);\\ "
                r"$\bullet$ $P\left(\overline{E}\right) = 1 - P\left(E\right)$.\\ "
                r"Đối chiếu thì chỉ có %s là đúng." % dung)
        cauTN += MC_SA_answer_text(
            r"Khẳng định nào sau đây về xác suất là \textbf{đúng}?",
            dung, [SAI[j] for j in bo], giai, 0, 0, dang)
    return cauTN


def L10_C9_B27_VD155_TL_A_01(socau, dong=1):
    """Tự luận: gieo hai con xúc xắc - mô tả không gian mẫu và tính xác suất."""
    gt = []
    while len(gt) < socau:
        tong = _rd.randint(4, 10)
        if tong not in gt:
            gt.append(tong)

    cauTN = ''
    for tong in gt:
        thuan_loi = [(i, j) for i in range(1, 7) for j in range(1, 7) if i + j == tong]
        k = len(thuan_loi)
        from math import gcd as _gcd
        g = _gcd(k, 36)
        debai = (r"Gieo đồng thời hai con xúc xắc cân đối. Gọi $E$ là biến cố "
                 r"``tổng số chấm xuất hiện trên hai con xúc xắc bằng $%d$''." % tong)
        ds_abcd = [
            (r"Tính số phần tử của không gian mẫu.", r"36",
             r"Mỗi con xúc xắc có $6$ kết quả, hai con gieo đồng thời nên mỗi kết quả của "
             r"phép thử là một cặp $\left(i; j\right)$.\\ "
             r"Vậy $n\left(\Omega\right) = 6\cdot 6 = 36$."),
            (r"Tính xác suất của biến cố $E$.",
             r"\dfrac{%d}{%d}" % (k // g, 36 // g),
             r"Các kết quả thuận lợi cho $E$ là các cặp có tổng bằng $%d$:\\ "
             r"$%s$, tất cả có $n\left(E\right) = %d$ cặp.\\ "
             r"Vậy $P\left(E\right) = \dfrac{n\left(E\right)}{n\left(\Omega\right)} "
             r"= \dfrac{%d}{36} = \dfrac{%d}{%d}$."
             % (tong, ", ".join(r"\left(%d; %d\right)" % c for c in thuan_loi),
                k, k, k // g, 36 // g)),
        ]
        cauTN += TL_answer_text(debai, ds_abcd, 0, 0, dong)
    return cauTN


def L10_C9_B27_TH151_MC_A_01(socau, dang=1):
    """Tính xác suất của biến cố bằng định nghĩa cổ điển.

    Gieo hai con xúc xắc cân đối - thí nghiệm đơn giản nhất mà học sinh
    lập được không gian mẫu đầy đủ ($n(\\Omega)=36$), đúng mức Thông hiểu:
    chỉ cần đếm số kết quả thuận lợi rồi chia.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta
    (mapping L10_C9_B27_TH151_MC_A da co san nhung chua co ham).
    """
    def _phan_so(tu, mau):
        g = math.gcd(tu, mau)
        tu, mau = tu // g, mau // g
        if mau == 1:
            return "$%d$" % tu
        return "$\\dfrac{%d}{%d}$" % (tu, mau)

    da_ra = []
    ket_qua = ""
    while len(da_ra) < socau:
        # tong tu 3 den 11 de so ket qua thuan loi luon >= 2
        tong = random.randint(3, 11)
        if tong in da_ra:
            if len(set(range(3, 12))) <= len(da_ra):
                break
            continue
        da_ra.append(tong)

        # so cap (a;b) voi a+b = tong, 1 <= a,b <= 6
        cap = [(a, tong - a) for a in range(1, 7) if 1 <= tong - a <= 6]
        thuan_loi = len(cap)
        dapso = _phan_so(thuan_loi, 36)

        liet_ke = "; ".join("$(%d;%d)$" % (a, b) for a, b in cap)
        debai = ("Gieo đồng thời hai con xúc xắc cân đối và đồng chất. "
                 "Tính xác suất của biến cố $A$: ``Tổng số chấm xuất hiện "
                 "trên hai con xúc xắc bằng $%d$''." % tong)

        giai = ("Mỗi con xúc xắc có $6$ mặt nên số kết quả có thể xảy ra là\\\\\n"
                "$n(\\Omega) = 6 \\cdot 6 = 36$.\\\\\n"
                "Các kết quả thuận lợi cho $A$ là: %s.\\\\\n"
                "Do đó $n(A) = %d$.\\\\\n"
                "Vậy $P(A) = \\dfrac{n(A)}{n(\\Omega)} = \\dfrac{%d}{36} = %s$."
                % (liet_ke, thuan_loi, thuan_loi,
                   dapso.strip("$")))

        # nhieu: dem thua/thieu mot cap, hoac chia nham cho 6 (so mat mot con)
        ung_vien = [_phan_so(thuan_loi + 1, 36),
                    _phan_so(thuan_loi - 1, 36),
                    _phan_so(thuan_loi, 6),
                    _phan_so(thuan_loi + 2, 36),
                    _phan_so(thuan_loi, 12)]
        dsnhieu = _ba_nhieu9(dapso, ung_vien,
                             buoc=lambda k: _phan_so(thuan_loi + 2 + k, 36))
        ket_qua += MC_SA_answer_text(debai, dapso, dsnhieu, giai, 0, 0, dang)
    return ket_qua


# ==========================================================
# Bốn dạng còn thiếu hàm của chương 9 (Mapping đã khai từ trước).
# CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
# ==========================================================

def _so_tp(x, n=2):
    """Số thập phân theo cách viết Việt Nam (dấu phẩy), bỏ đuôi 0 thừa."""
    s = ("%%.%df" % n) % float(x)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def L10_C9_B26_NB143_SA_A_01(socau):
    """Số phần tử của không gian mẫu.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.
    """
    PHEP_THU = [
        ("Tung một đồng xu liên tiếp {n_chu} lần", lambda n: 2 ** n,
         [2, 3, 4, 5],
         r"Mỗi lần tung có $2$ kết quả (sấp hoặc ngửa). Tung {n_chu} lần nên "
         r"$n(\Omega) = 2^{{{n}}} = {kq}$."),
        ("Gieo một con xúc xắc cân đối {n_chu} lần", lambda n: 6 ** n,
         [1, 2],
         r"Mỗi lần gieo có $6$ kết quả. Gieo {n_chu} lần nên "
         r"$n(\Omega) = 6^{{{n}}} = {kq}$."),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(PHEP_THU))
        n = random.choice(PHEP_THU[i][2])
        if (i, n) not in gt:
            gt.append((i, n))

    cau = ""
    for i, n in gt:
        mau, tinh, _ds, mau_giai = PHEP_THU[i]
        kq = tinh(n)
        n_chu = num2words(n, lang="vi")
        debai = (mau.format(n_chu=n_chu) +
                 r" và quan sát kết quả. Số phần tử của không gian mẫu "
                 r"$n(\Omega)$ bằng bao nhiêu?")
        giai = mau_giai.format(n_chu=n_chu, n=n, kq=kq)
        # math_type luôn dựng bốn phương án rồi mới bỏ đi khi dang=2, nên
        # câu trả lời ngắn vẫn phải truyền đủ ba phương án nhiễu.
        nhieu = _ba_nhieu9(kq, [kq * 2, kq // 2, kq + n, kq - n],
                           buoc=lambda t: kq + 10 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C9_B26_TH150_MC_A_01(socau, dang=1):
    r"""Mô tả không gian mẫu và biến cố khi tung đồng xu, gieo xúc xắc.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Phương án nhiễu là các TẬP HỢP khác của cùng phép thử, nên chắc chắn
    chỉ có một phương án đúng.
    """
    DONG_XU = {
        "Kết quả hai lần tung giống nhau": r"\{SS;\ NN\}",
        "Kết quả hai lần tung khác nhau": r"\{SN;\ NS\}",
        "Có ít nhất một lần xuất hiện mặt ngửa": r"\{SN;\ NS;\ NN\}",
        "Lần tung thứ nhất xuất hiện mặt sấp": r"\{SS;\ SN\}",
    }
    XUC_XAC = {
        "Số chấm xuất hiện là số nguyên tố": r"\{2;\ 3;\ 5\}",
        "Số chấm xuất hiện là số chẵn": r"\{2;\ 4;\ 6\}",
        "Số chấm xuất hiện lớn hơn $4$": r"\{5;\ 6\}",
        "Số chấm xuất hiện là ước của $6$": r"\{1;\ 2;\ 3;\ 6\}",
    }

    gt = []
    while len(gt) < socau:
        loai = random.choice(["xu", "xx"])
        bang = DONG_XU if loai == "xu" else XUC_XAC
        mo_ta = random.choice(list(bang.keys()))
        if (loai, mo_ta) not in gt:
            gt.append((loai, mo_ta))

    cauTN = ""
    for loai, mo_ta in gt:
        bang = DONG_XU if loai == "xu" else XUC_XAC
        dung = "$A = %s$" % bang[mo_ta]
        nhieu = ["$A = %s$" % v for k, v in bang.items() if k != mo_ta]

        if loai == "xu":
            debai = (r"Tung một đồng xu liên tiếp hai lần, kí hiệu $S$ là mặt "
                     r"sấp và $N$ là mặt ngửa. Không gian mẫu là "
                     r"$\Omega = \{SS;\ SN;\ NS;\ NN\}$. Gọi $A$ là biến cố "
                     r"``%s''. Khẳng định nào sau đây \textbf{đúng}?" % mo_ta)
            giai = (r"Liệt kê các kết quả của $\Omega = \{SS;\ SN;\ NS;\ NN\}$ "
                    r"thoả mãn ``%s'', ta được" % mo_ta)
            nhieu.append(r"$A = \{SS;\ SN;\ NS;\ NN\}$")
        else:
            debai = (r"Gieo một con xúc xắc cân đối và đồng chất, quan sát số "
                     r"chấm xuất hiện. Không gian mẫu là "
                     r"$\Omega = \{1;\ 2;\ 3;\ 4;\ 5;\ 6\}$. Gọi $A$ là biến "
                     r"cố ``%s''. Khẳng định nào sau đây \textbf{đúng}?" % mo_ta)
            giai = (r"Xét từng phần tử của $\Omega = \{1;\ 2;\ 3;\ 4;\ 5;\ 6\}$ "
                    r"xem có thoả mãn ``%s'' hay không, ta được" % mo_ta)
            nhieu.append(r"$A = \{1;\ 2;\ 3;\ 4;\ 5;\ 6\}$")

        giai = giai + "\\\\\n" + dung + "."
        cauTN += MC_SA_answer_text(debai, dung, nhieu, giai, 0, 0, dang)
    return cauTN


def L10_C9_B26_TH150_SA_A_01(socau):
    r"""Số phần tử của biến cố.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Gieo hai con xúc xắc nên $n(\Omega) = 36$; học sinh phải đếm được số
    cặp $(a; b)$ thoả mãn điều kiện - đúng mức Thông hiểu.
    """
    DIEU_KIEN = [
        ("Tổng số chấm trên hai con xúc xắc bằng $%d$",
         lambda s: lambda a, b: a + b == s, [5, 6, 7, 8, 9]),
        ("Tổng số chấm trên hai con xúc xắc là số chia hết cho $%d$",
         lambda k: lambda a, b: (a + b) % k == 0, [3, 4, 5]),
        ("Số chấm trên hai con xúc xắc hơn kém nhau $%d$ đơn vị",
         lambda d: lambda a, b: abs(a - b) == d, [1, 2, 3]),
    ]
    gt = []
    while len(gt) < socau:
        i = random.randrange(len(DIEU_KIEN))
        t = random.choice(DIEU_KIEN[i][2])
        if (i, t) not in gt:
            gt.append((i, t))

    cau = ""
    for i, t in gt:
        mau, tao, _ds = DIEU_KIEN[i]
        kiem = tao(t)
        cap = [(a, b) for a in range(1, 7) for b in range(1, 7) if kiem(a, b)]
        kq = len(cap)
        mo_ta = mau % t

        debai = (r"Gieo đồng thời hai con xúc xắc cân đối và đồng chất. Gọi "
                 r"$A$ là biến cố ``%s''. Tính số phần tử $n(A)$ của biến cố "
                 r"$A$." % mo_ta)

        liet_ke = "; ".join("$(%d;%d)$" % (a, b) for a, b in cap)
        giai = (r"Mỗi kết quả là một cặp $(a; b)$ với $a$, $b$ lần lượt là số "
                r"chấm trên con thứ nhất và con thứ hai, nên "
                r"$n(\Omega) = 6\cdot 6 = 36$."
                "\\\\\n"
                r"Các kết quả thuận lợi cho $A$ là: %s."
                "\\\\\n"
                r"Vậy $n(A) = %d$." % (liet_ke, kq))

        nhieu = _ba_nhieu9(kq, [36 - kq, kq * 2, kq + 1, kq - 1],
                           buoc=lambda t: kq + 2 * t)
        cau += MC_SA_answer_const(debai, kq, nhieu, giai, 0, 0, 2)
    return cau


def L10_C9_B27_TH152_SA_A_01(socau):
    r"""Xác suất của biến cố đối.

    CLAUDE THEM 28/09/2026 - co Lan kiem tra lai ID va mo ta.

    Số liệu chọn sao cho $P(\overline{A})$ là SỐ THẬP PHÂN HỮU HẠN: câu
    trả lời ngắn chấm bằng cách so khớp đúng chuỗi, nếu đáp số là phân số
    vô hạn tuần hoàn như $\dfrac{5}{6}$ thì học sinh làm đúng vẫn có thể
    gõ ra số khác.
    """
    BO = []
    for N in (20, 25, 40, 50):
        for k in range(3, 10):
            m = N // k                      # số bội của k trong [1; N]
            p = 1 - m / N
            if abs(p * 100 - round(p * 100)) < 1e-9 and 0 < m < N:
                BO.append((N, k, m, p))

    gt = []
    thu = 0
    while len(gt) < socau and thu < 200:
        thu += 1
        i = random.randrange(len(BO))
        if i not in gt:
            gt.append(i)

    cau = ""
    for i in gt:
        N, k, m, p = BO[i]
        debai = (r"Chọn ngẫu nhiên một số nguyên dương không vượt quá $%d$. "
                 r"Gọi $A$ là biến cố ``Số được chọn chia hết cho $%d$''. "
                 r"Tính xác suất của biến cố đối $\overline{A}$ (viết kết quả "
                 r"dưới dạng số thập phân)." % (N, k))

        giai = (r"Không gian mẫu gồm các số $1;\ 2;\ \ldots;\ %d$ nên "
                r"$n(\Omega) = %d$." % (N, N) +
                "\\\\\n"
                r"Các số chia hết cho $%d$ và không vượt quá $%d$ là "
                r"$%d;\ %d;\ \ldots;\ %d$, gồm $%d$ số, nên $n(A) = %d$."
                % (k, N, k, 2 * k, m * k, m, m) +
                "\\\\\n"
                r"Do đó $P(A) = \dfrac{%d}{%d} = %s$."
                % (m, N, _so_tp(m / N, 3)) +
                "\\\\\n"
                r"Vì $\overline{A}$ là biến cố đối của $A$ nên"
                "\\\\\n"
                r"$P\left(\overline{A}\right) = 1 - P(A) = 1 - %s = %s$."
                % (_so_tp(m / N, 3), _so_tp(p, 3)))

        nhieu = _ba_nhieu9(_so_tp(p, 3),
                           [_so_tp(1 - p, 3), _so_tp(p / 2, 3),
                            _so_tp(m / k / N, 4), _so_tp(1 - p / 2, 3)],
                           buoc=lambda t: _so_tp(p - t / 100.0, 3))
        cau += MC_SA_answer_text(debai, _so_tp(p, 3), nhieu, giai, 0, 0, 2)
    return cau
