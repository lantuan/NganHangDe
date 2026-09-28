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
				Một đồng xu khi tung có hai trường hợp xảy ra là sấp hoặc ngửa. Nên khi tung đồng xu ${v[0]}$ lần liên tiếp thì $n(\\Omega) = 2^{v[0]}$.\\ \\
				Để ra tất cả các mặt đều {v[1]} thì chỉ có 1 trường hợp. Do đó, xác suất cần tìm là $P(E) = \\dfrac{{1}}{{ 2^{v[0]} }}$.
			"""
		else:
			giai = f"""
				Một đồng xu khi tung có hai trường hợp xảy ra là sấp hoặc ngửa. Nên đối với ${v[0]}$ đồng xu thì $n(\\Omega) = 2^{v[0]}$.\\ \\
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

			Chọn hai bạn từ tổ có ${boy}$ bạn nam và ${girl}$ bạn nữ.\\

			$A$: ``hai bạn được chọn đều là nam''; $B$: ``hai bạn được chọn đều là nữ''.\\

			$\\bullet$ Một kết quả không thể vừa là ``cả hai đều nam'' vừa là ``cả hai đều nữ'',

			nên hai biến cố $A$ và $B$ không bao giờ cùng xảy ra: $A \\cap B = \\varnothing$ (hai biến cố xung khắc).\\

			$\\bullet$ $A \\cup B \\ne \\Omega$ vì còn trường hợp chọn được một nam và một nữ.\\

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
            Không gian mẫu $n(\\Omega) = 6^{lan}$.\\
            Để không lần nào xuất hiện mặt ${mat}$ chấm thì mỗi lần gieo có $5$ khả năng xảy ra (các mặt khác mặt ${mat}$), nên có tất cả $5^{lan}$ trường hợp thuận lợi cho biến cố đối.\\
            Xác suất để không lần nào xuất hiện mặt ${mat}$ chấm là $\\left(\\dfrac{{5}}{{6}}\\right)^{lan}$.\\
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

		giai = f"""Ta có $\\Omega = \\left\\lbrace (x;y), {xA}\\le x \\le {xC} , {yA}\\le y \\le {yC} \\right\\rbrace$ với $x,y \\in \\mathbb{{Z}}$.\\
		Suy ra $n\\left( \\Omega \\right) = {xC - xA + 1} \\cdot {yC - yA + 1}={(xC - xA + 1) * (yC - yA + 1)}$. \\
		Ta có $x,y$ đều chia hết cho $2$ nên $A$ có số phần tử là ${count_even_numbers(xA,xC)} \\cdot {count_even_numbers(yA, yC)} = {count_even_numbers(xA,xC) * count_even_numbers(yA, yC)}$.\\
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
				$\\overline{{A}}$: ``Trong {vienbi_chu} viên bi {DK[0]}''.\\ \\ 
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

		giai = f"""Không gian mẫu $n(\\Omega) = 6^{lan}$.\\
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


# ---- Gieo dong thoi hai con xuc xac ----
# (tên cũ của cô: K10_9_DS_1_VD)
def L10_C9_TF_A_01(socau,socot):
	gt=[]
	dem=len(gt)
	while dem<socau:
		tong = np.randint(6,10)
		chan_le = np.choice(['chẵn', 'lẻ'])
		giong_khac = np.choice(['giống', 'khác'])

		v = [tong, chan_le, giong_khac]
		if v not in gt:
			gt.append(v)
			dem+=1

	cauTF = ''
	for v in gt:
		tong, chan_le, giong_khac = v[0], v[1], v[2]

		def probability_of_sum(target_sum):
			# Khởi tạo số lần xuất hiện của mỗi kết quả từ việc tung hai con xúc xắc
			dice_counts = {i: 0 for i in range(2, 13)}

			# Tính số lần xuất hiện của mỗi tổng có thể có
			for dice1 in range(1, 7):
				for dice2 in range(1, 7):
					dice_counts[dice1 + dice2] += 1

			# Tính xác suất của tổng có thể có
			total_outcomes = 6 * 6  # Tổng số kết quả có thể từ hai con xúc xắc
			probability = round(dice_counts[target_sum] / total_outcomes, 2)
			probability_str = str(probability).replace('.', ',')

			return probability_str

		def probability_sum_less_than(k):
			# Khởi tạo biến đếm cho số cặp có tổng nhỏ hơn 6
			count = 0

			# Đếm số cặp có tổng nhỏ hơn k
			for dice1 in range(1, 7):
				for dice2 in range(1, 7):
					if dice1 + dice2 < k:
						count += 1

			# Tính xác suất
			total_outcomes = 6 * 6  # Tổng số kết quả có thể từ hai con xúc xắc
			probability = round(count / total_outcomes, 2)
			probability_str = str(probability).replace('.', ',')

			return probability_str

		debai = f"""Gieo đồng thời hai con xúc xắc cân đối."""

		if chan_le == 'le':
			ds_chan_le = (
				   [
					   (f'''{{\\True Xác suất để tích số chấm trên hai con xúc xắc là một số lẻ là $\\dfrac{{1}}{{4}}$ }}''',
						f'''Đúng. Để tích là một số lẻ thì số chấm trên hai con xúc xắc đều ra số lẻ. Nên số trường hợp là $3 \\times 3 = 9$. Nên xác suất bằng $\\dfrac{{9}}{{36}} = \\dfrac{{1}}{{4}}.'''),
					   (f'''{{Xác suất để tích số chấm trên hai con xúc xắc là một số lẻ là $\\dfrac{{1}}{{2}}$ }}''',
					   f'''Sai. Để tích là một số lẻ thì số chấm trên hai con xúc xắc đều ra số lẻ. Nên số trường hợp là $3 \\times 3 = 9$. Nên xác suất bằng $\\dfrac{{9}}{{36}} = \\dfrac{{1}}{{4}}.'''),
				   ])
		else:
			ds_chan_le = (
				[
					(f'''{{\\True Xác suất để tích số chấm trên hai con xúc xắc là một số chẵn là $\\dfrac{{3}}{{4}}$ }}''',
					f'''Đúng. Để tích là một số lẻ thì số chấm trên hai con xúc xắc đều ra số lẻ, ta được số trường hợp là $3 \\times 3 = 9$. Nên xác suất để có tất cả là số lẻ bằng $\\dfrac{{9}}{{36}} = \\dfrac{{1}}{{4}}$. Do đó tích số chẵn là $\\dfrac{{3}}{{4}}$.'''),
					(f'''{{Xác suất để tích số chấm trên hai con xúc xắc là một số chẵn là $\\dfrac{{1}}{{2}}$ }}''',
					 f'''Sai. Để tích là một số lẻ thì số chấm trên hai con xúc xắc đều ra số lẻ, ta được số trường hợp là $3 \\times 3 = 9$. Nên xác suất để có tất cả là số lẻ bằng $\\dfrac{{9}}{{36}} = \\dfrac{{1}}{{4}}$. Do đó tích số chẵn là $\\dfrac{{3}}{{4}}$.'''),
				])

		if giong_khac == 'giống':
			ds_giong_khac = ([
					   (f'''{{\\True Xác suất để được cả hai con xúc xắc xuất hiện số chấm giống nhau là $\\dfrac{{1}}{{6}}$ }}''',
						f'''Đúng.'''),
					   (f'''{{Xác suất để được cả hai con xúc xắc xuất hiện số chấm giống nhau là $\\dfrac{{5}}{{6}}$ }}''',
					   f'''Sai.'''),
				   ])
		else:
			ds_giong_khac = ([
					   (f'''{{\\True Xác suất để được cả hai con xúc xắc xuất hiện số chấm khác nhau là $\\dfrac{{5}}{{6}}$ }}''',
						f'''Đúng.'''),
					   (f'''{{Xác suất để được cả hai con xúc xắc xuất hiện số chấm khác nhau là $\\dfrac{{1}}{{6}}$ }}''',
					   f'''Sai.'''),
				   ])
		ds1 = ([
				  (f'''{{\\True Xác suất để tổng số chấm trên hai con xúc sắc bằng ${tong}$ là ${probability_of_sum(tong)}$}}''',
					f'''Đúng. Xác suất là ${probability_of_sum(tong)}$.'''),
				   (f'''{{Xác suất để tổng số chấm trên hai con xúc sắc bằng ${tong}$ là ${probability_of_sum(tong+1)}$}}''',
				   f'''Sai. xắc xuất là ${probability_of_sum(tong)}$.'''),
			   ])
		ds2 = ([
				   (
				   f'''{{\\True Xác suất để tổng số chấm trên hai con xúc sắc nhỏ hơn ${tong}$ là ${probability_sum_less_than(tong)}$}}''',
				   f'''Đúng. Xác suất là ${probability_sum_less_than(tong)}$.'''),
				   (
				   f'''{{Xác suất để tổng số chấm trên hai con xúc sắc nhỏ hơn ${tong}$ là ${probability_sum_less_than(tong + 1)}$}}''',
				   f'''Sai. xắc xuất là ${probability_sum_less_than(tong)}$.'''),
			   ])

		ds_abcd = ds_chan_le , ds_giong_khac , ds1, ds2

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTF+=TF_baitoan_du(debai,ds_abcd,0,0,socot)#Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_DS_1_VD(16,0)) # câu này đang mới tối đa đưuoc 16 đề chọn.
# ##############################################


# ---- Day nhi phan 10 bit ----
# (tên cũ của cô: K10_9_DS_2_VD)
def L10_C9_TF_B_01(socau,socot):
	gt=[]
	dem=len(gt)
	while dem<socau:
		so_chon_1 = np.randint(300,500)
		so_chon_2 = np.randint(3,8)
		so_chon_2_chu = num2words(so_chon_2, lang='vi')
		khong_mot = np.choice([0, 1])
		saiso_2 = np.choice([-2,-1,1,2])
		so_chon_3 = np.randint(2,7)
		while so_chon_3 == so_chon_2:
			so_chon_3 = np.randint(2, 7)
		so_chon_3_chu = num2words(so_chon_3, lang='vi')

		v = [so_chon_1, so_chon_2, so_chon_2_chu, khong_mot, saiso_2, so_chon_3, so_chon_3_chu]
		if v not in gt:
			gt.append(v)
			dem+=1

	cauTF = ''
	for v in gt:
		so_chon_1, so_chon_2, so_chon_2_chu, khong_mot, saiso_2, so_chon_3, so_chon_3_chu = v[0], v[1], v[2], v[3], v[4], v[5], v[6]

		def binomial_coefficient(n, k):
				# Hàm này tính tổ hợp chập n lấy k.
				# Haram n: Số nguyên không âm
				# param k: Số nguyên không âm
				# return: Giá trị tổ hợp chập n lấy k
			return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))  # Sử dụng math.factorial()

		debai = f"""Dãy ($x_1, x_2, \\ldots, x_{{10}}$) trong đó mỗi kí tự $x_i$ ($i = 1, 2, \\ldots, 10$) chỉ nhận giá trị $0$ hoặc $1$ được gọi là dãy nhị phân $10$ bit."""

		ds_abcd = ([
				   (f'''{{\\True Có $1024$ dãy nhị phân $10$ bit }}''',
					f'''Đúng. Mỗi kí tự $x_i$ ($i = 1, 2, \\ldots, 10$) có hai cách chọn $0$ hoặc $1$. Suy ra có $2^{{10}}$ dãy nhị phân $10$ bit.'''),
				   (f'''{{Có $512$ dãy nhị phân $10$ bit }}''',
					f'''Sai. Mỗi kí tự $x_i$ ($i = 1, 2, \\ldots, 10$) có hai cách chọn $0$ hoặc $1$. Suy ra có $2^{{10}}$ dãy nhị phân $10$ bit.'''),
			   ],
			   [
				   (f'''{{\\True Chọn bất kì một số trong dãy nhị phân $10$ bit, xác suất để số đó khi đổi sang hệ thập phân nhỏ hơn ${so_chon_1}$ là ${str(round(so_chon_1/1024,5)).replace('.', ',')}$ }}''',
					f'''Đúng. '''),
				   (f'''{{Chọn bất kì một số trong dãy nhị phân $10$ bit, xác suất để số đó khi đổi sang hệ thập phân nhỏ hơn ${so_chon_1}$ là ${str(round((so_chon_1+1)/1024,5)).replace('.', ',')}$ }}''',
					f'''Sai. Chọn bất kì một số trong dãy nhị phân $10$ bit, xác suất để số đó khi đổi sang hệ thập phân nhỏ hơn ${so_chon_1}$ là ${str(round(so_chon_1/1024,5)).replace('.', ',')}$. '''),
			   ],
				[
				   (f'''{{\\True Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_2_chu} số ${khong_mot}$ là ${str(round((binomial_coefficient(10,so_chon_2))/1024,5)).replace('.', ',')}$ }}''',
					f'''Đúng. Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_2_chu} số ${khong_mot}$ là $\\dfrac{{C_{{10}}^{so_chon_2} }}{{1024}} = {str(round((binomial_coefficient(10,so_chon_2))/1024,5)).replace('.', ',')}$. '''),
				   (f'''{{Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_2_chu} số ${khong_mot}$ là ${str(round((binomial_coefficient(10,so_chon_2 + saiso_2))/1024,5)).replace('.', ',')}$ }}''',
					f'''Sai. Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_2_chu} số ${khong_mot}$ là $\\dfrac{{C_{{10}}^{so_chon_2} }}{{1024}} = {str(round((binomial_coefficient(10,so_chon_2))/1024,5)).replace('.', ',')}$ . '''),
			   ],
			   [
				   (f'''{{\\True Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_3_chu} số ${khong_mot}$, và các số ${khong_mot}$ này luôn đứng gần nhau là ${str(round((10-so_chon_3+1)/1024,5)).replace('.', ',')}$ }}''',
					f'''Đúng. Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_3_chu} số ${khong_mot}$, và các số ${khong_mot}$ này luôn đứng gần nhau là $\\dfrac{{10 - {so_chon_3} + 1 }}{{1024}} = {str(round((10-so_chon_3+1)/1024,5)).replace('.', ',')}$. '''),
				   (f'''{{Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_3_chu} số ${khong_mot}$, và các số ${khong_mot}$ này luôn đứng gần nhau là ${str(round((10-so_chon_3)/1024,5)).replace('.', ',')}$ }}''',
					f'''Sai. Xác suất để chọn được một số trong dãy nhị phân $10$ bit có đúng {so_chon_3_chu} số ${khong_mot}$, và các số ${khong_mot}$ này luôn đứng gần nhau là $\\dfrac{{10 - {so_chon_3} + 1 }}{{1024}} = {str(round((10-so_chon_3+1)/1024,5)).replace('.', ',')}$ . '''),
			   ])

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTF+=TF_baitoan_du(debai,ds_abcd,0,0,socot)#Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_DS_2_VD(16,0))
# ##############################################


# ---- Chiec non ki dieu (van dung cao) ----
# (tên cũ của cô: K10_9_DS_3_VDC)
def L10_C9_TF_C_01(socau,socot): #### không gian mẫu đang bị sai, chưa xét trường hợp mất lượt ở các lần quay nhỏ hơn k
	gt=[]
	dem=len(gt)
	while dem<socau:
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

		def simplify_fraction(numerator, denominator):
			# Hàm rút gọn phân số
			common_divisor = math.gcd(numerator, denominator)
			return numerator // common_divisor, denominator // common_divisor

		k = np.randint(3,5)
		k_chu = num2words(k, lang='vi')
		vitri_cong = np.choice([k + 1, k])
		vitri_cong_chu = num2words(vitri_cong, lang='vi')
		vitri_tru = np.choice([k + 1, k])
		vitri = vitri_cong + vitri_tru + 2
		vitri_chu = num2words(vitri, lang='vi')


		v = [k, k_chu, vitri_cong, vitri_cong_chu, vitri_tru, vitri, vitri_chu]
		if v not in gt:
			gt.append(v)
			dem+=1

	cauTF = ''
	for v in gt:
		k, k_chu, vitri_cong, vitri_cong_chu, vitri_tru, vitri, vitri_chu = v[0], v[1], v[2], v[3], v[4], v[5], v[6]

		khonggianmau = vitri ** k
		congdiem = vitri_cong ** k
		trudiem = vitri_tru ** k

		#phương án nhiễu của congdiem và trudiem
		nhieu_congdiem = calculate_permutations(vitri_cong, k)
		nhieu_trudiem = calculate_permutations(vitri_tru, k)

		P_congdiem_tu, P_congdiem_mau = simplify_fraction(congdiem, khonggianmau)
		P_trudiem_tu, P_trudiem_mau = simplify_fraction(trudiem, khonggianmau)

		# xác suất nhiễu
		P_nhieu_congdiem_tu, P_nhieu_congdiem_mau = simplify_fraction(nhieu_congdiem, khonggianmau)
		P_nhieu_trudiem_tu, P_nhieu_trudiem_mau = simplify_fraction(nhieu_trudiem, khonggianmau)

		khacnhau = calculate_permutations(vitri - 1, k - 1) * (vitri - (k - 1))
		nhieu_khacnhau = calculate_permutations(vitri, k)

		P_khacnhau_tu, P_khacnhau_mau = simplify_fraction(khacnhau, khonggianmau)
		P_nhieu_khacnhau_tu, P_nhieu_khacnhau_mau = simplify_fraction(nhieu_khacnhau, khonggianmau)# xác suất nhiễu

		debai = f"""Mũi tên của bánh xe trong trò chơi ``Chiếc nón kì diệu'' có thể dừng lại ở một trong {vitri_chu} vị trí. Người chơi được quay {k_chu} lần.
		Trong {vitri_chu} vị trí thì có một vị trí là mất lượt chơi (người chơi dừng tất cả lượt quay còn lại), một vị trí là thêm lượt chơi (người chơi được tăng thêm một lần quay), 
		{vitri_cong_chu} vị trí người chơi được cộng điểm với những điểm số khác nhau, còn lại là vị trí người chơi bị trừ điểm với những điểm số khác nhau."""

		ds_abcd = ([
				   (f'''{{\\True Số phần tử của không gian mẫu của phép thử là ${khonggianmau}$}}''',
					f'''Đúng. Số phần tử của không gian mẫu là ${khonggianmau}$.'''),
				   (f'''{{\\True Số phần tử của không gian mẫu của phép thử là ${khonggianmau}$}}''',
					f'''Đúng. Số phần tử của không gian mẫu là ${khonggianmau}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {P_congdiem_tu} }} {{ {P_congdiem_mau} }}$}}''',
				   f'''Đúng. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {vitri_cong} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_congdiem_tu} }} {{ {P_congdiem_mau} }}$.'''),
				   (f'''{{Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {P_nhieu_congdiem_tu} }} {{ {P_nhieu_congdiem_mau} }}$}}''',
				   f'''Sai. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {vitri_cong} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_congdiem_tu} }} {{ {P_congdiem_mau} }}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {P_trudiem_tu} }} {{ {P_trudiem_mau} }}$}}''',
				   f'''Đúng. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {vitri_tru} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_trudiem_tu} }} {{ {P_trudiem_mau} }}$.'''),
				   (f'''{{Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {P_nhieu_trudiem_tu} }} {{ {P_nhieu_trudiem_mau} }}$}}''',
				   f'''Sai. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {vitri_tru} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_trudiem_tu} }} {{ {P_trudiem_mau} }}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ {P_khacnhau_tu} }} {{ {P_khacnhau_mau} }}$}}''',
					f'''Đúng. Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ A_{{ {vitri - 1} }}^{k - 1} \\cdot {vitri - (k - 1)} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_khacnhau_tu} }} {{ {P_khacnhau_mau} }}$.'''),
				   (f'''{{Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ {P_nhieu_khacnhau_tu} }} {{ {P_nhieu_khacnhau_mau} }}$}}''',
				   f'''Sai. Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ A_{{{vitri - 1}}} ^ {k - 1} \\cdot {vitri - (k - 1)} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_khacnhau_tu} }} {{ {P_khacnhau_mau} }}$.'''),
				])

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTF+=TF_baitoan_du(debai,ds_abcd,0,0,socot)#Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_DS_3_VDC(8,0))
# ##############################################


# ---- Chiec non ki dieu ----
# (tên cũ của cô: K10_9_DS_4_VD)
def L10_C9_TF_D_01(socau,socot): #### không gian mẫu đang bị sai, chưa xét trường hợp mất lượt ở các lần quay nhỏ hơn k
	gt=[]
	dem=len(gt)
	while dem<socau:
		k = np.randint(3,6)
		k_chu = num2words(k, lang='vi')
		vitri_cong = np.choice([k + 2, k + 1, k])
		vitri_cong_chu = num2words(vitri_cong, lang='vi')
		vitri_tru = np.choice([k+2, k + 1, k])
		vitri = vitri_cong + vitri_tru
		vitri_chu = num2words(vitri, lang='vi')

		v = [k, k_chu, vitri_cong, vitri_cong_chu, vitri_tru, vitri, vitri_chu]
		if v not in gt:
			gt.append(v)
			dem+=1

	cauTF = ''
	for v in gt:
		k, k_chu, vitri_cong, vitri_cong_chu, vitri_tru, vitri, vitri_chu = v[0], v[1], v[2], v[3], v[4], v[5], v[6]

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

		def simplify_fraction(numerator, denominator):
			# Hàm rút gọn phân số
			common_divisor = math.gcd(numerator, denominator)
			return numerator // common_divisor, denominator // common_divisor

		def binomial_coefficient(n, k):
				# Hàm này tính tổ hợp chập n lấy k.
				# Haram n: Số nguyên không âm
				# param k: Số nguyên không âm
				# return: Giá trị tổ hợp chập n lấy k
			return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))  # Sử dụng math.factorial()

		khonggianmau = vitri ** k
		congdiem = vitri_cong ** k
		trudiem = vitri_tru ** k

		#phương án nhiễu của congdiem và trudiem
		nhieu_congdiem = calculate_permutations(vitri_cong, k)
		nhieu_trudiem = calculate_permutations(vitri_tru, k)

		P_congdiem_tu, P_congdiem_mau = simplify_fraction(congdiem, khonggianmau)
		P_trudiem_tu, P_trudiem_mau = simplify_fraction(trudiem, khonggianmau)

		# xác suất nhiễu
		P_nhieu_congdiem_tu, P_nhieu_congdiem_mau = simplify_fraction(nhieu_congdiem, khonggianmau)
		P_nhieu_trudiem_tu, P_nhieu_trudiem_mau = simplify_fraction(nhieu_trudiem, khonggianmau)

		khacnhau = calculate_permutations(vitri, k)
		nhieu_khacnhau = binomial_coefficient(vitri, k)

		P_khacnhau_tu, P_khacnhau_mau = simplify_fraction(khacnhau, khonggianmau)
		P_nhieu_khacnhau_tu, P_nhieu_khacnhau_mau = simplify_fraction(nhieu_khacnhau, khonggianmau)# xác suất nhiễu

		debai = f"""Mũi tên của bánh xe trong trò chơi ``Chiếc nón kì diệu'' có thể dừng lại ở một trong {vitri_chu} vị trí. Người chơi được quay {k_chu} lần.
		Trong {vitri_chu} vị trí thì có {vitri_cong_chu} vị trí người chơi được cộng điểm với những điểm số khác nhau, còn lại là vị trí người chơi bị trừ điểm với những điểm số khác nhau."""

		ds_abcd = ([
				   (f'''{{\\True Số phần tử của không gian mẫu của phép thử là ${khonggianmau}$}}''',
					f'''Đúng. Số phần tử của không gian mẫu là ${khonggianmau}$.'''),
				   (f'''{{\\True Số phần tử của không gian mẫu của phép thử là ${khonggianmau}$}}''',
					f'''Đúng. Số phần tử của không gian mẫu là ${khonggianmau}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {P_congdiem_tu} }} {{ {P_congdiem_mau} }}$}}''',
				   f'''Đúng. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {vitri_cong} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_congdiem_tu} }} {{ {P_congdiem_mau} }}$.'''),
				   (f'''{{Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {P_nhieu_congdiem_tu} }} {{ {P_nhieu_congdiem_mau} }}$}}''',
				   f'''Sai. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí cộng điểm là $\\dfrac{{ {vitri_cong} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_congdiem_tu} }} {{ {P_congdiem_mau} }}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {P_trudiem_tu} }} {{ {P_trudiem_mau} }}$}}''',
				   f'''Đúng. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {vitri_tru} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_trudiem_tu} }} {{ {P_trudiem_mau} }}$.'''),
				   (f'''{{Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {P_nhieu_trudiem_tu} }} {{ {P_nhieu_trudiem_mau} }}$}}''',
				   f'''Sai. Xác suất để mũi tên dừng lại ở {k_chu} vị trí đều là vị trí trừ điểm là $\\dfrac{{ {vitri_tru} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_trudiem_tu} }} {{ {P_trudiem_mau} }}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ {P_khacnhau_tu} }} {{ {P_khacnhau_mau} }}$}}''',
					f'''Đúng. Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ A_{{ {vitri} }}^{k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_khacnhau_tu} }} {{ {P_khacnhau_mau} }}$.'''),
				   (f'''{{Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ {P_nhieu_khacnhau_tu} }} {{ {P_nhieu_khacnhau_mau} }}$}}''',
				   f'''Sai. Xác suất để mũi tên dừng lại ở {k_chu} vị trí khác nhau là $\\dfrac{{ A_{{{vitri}}} ^ {k} }} {{ {vitri}^{k} }} = \\dfrac{{ {P_khacnhau_tu} }} {{ {P_khacnhau_mau} }}$.'''),
				])

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTF+=TF_baitoan_du(debai,ds_abcd,0,0,socot)#Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0
# print(K10_9_DS_4_VD(8,0))
# ##############################################


# ---- Cac lo dung dich axit / bazo ----
# (tên cũ của cô: K10_9_DS_5_VD)
def L10_C9_TF_E_01(socau,socot):
	gt=[]
	dem=len(gt)
	while dem<socau:
		axit = np.randint(4,10)
		axit_chu = num2words(axit, lang='vi')
		bazo = np.randint(4,10)
		while bazo == axit:
			bazo = np.randint(4,10)
		bazo_chu = num2words(bazo, lang='vi')
		trungtinh = np.randint(4,10)
		while (trungtinh == bazo) or (trungtinh == axit):
			trungtinh = np.randint(4,10)
		trungtinh_chu = num2words(trungtinh, lang='vi')

		v = [axit, axit_chu, bazo, bazo_chu, trungtinh, trungtinh_chu]
		if v not in gt:
			gt.append(v)
			dem+=1

	cauTF = ''
	for v in gt:
		axit, axit_chu, bazo, bazo_chu, trungtinh, trungtinh_chu = v[0], v[1], v[2], v[3], v[4], v[5]

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

		def simplify_fraction(numerator, denominator):
			# Hàm rút gọn phân số
			common_divisor = math.gcd(numerator, denominator)
			return numerator // common_divisor, denominator // common_divisor

		def binomial_coefficient(n, k):
				# Hàm này tính tổ hợp chập n lấy k.
				# Haram n: Số nguyên không âm
				# param k: Số nguyên không âm
				# return: Giá trị tổ hợp chập n lấy k
			return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))  # Sử dụng math.factorial()

		### có thứ tự, nhưng gì kết quả sẽ ra bằng không thứ tự nên làm công thức không thứ tự để ít trường hợp lại
		n = axit + bazo + trungtinh
		khonggianmau = binomial_coefficient(n,2)

		dodo = binomial_coefficient(axit,2)
		xanhxanh = binomial_coefficient(bazo,2)
		khongkhong = binomial_coefficient(trungtinh,2)
		cungmau = dodo + xanhxanh + khongkhong
		khacmau = khonggianmau - cungmau

		xanh = xanhxanh + bazo * trungtinh + bazo * axit
		xanh_nhieu1 = khonggianmau - dodo
		xanh_nhieu2 = khonggianmau - dodo - khongkhong

		do = dodo + axit * trungtinh + axit * bazo
		do_nhieu1 = khonggianmau - xanhxanh
		do_nhieu2 = khonggianmau - xanhxanh - khongkhong

		khong = khongkhong + trungtinh * axit + trungtinh * bazo
		khong_nhieu1 = khonggianmau - dodo - xanhxanh

		P_dodo_tu, P_dodo_mau = simplify_fraction(dodo, khonggianmau)
		P_xanhxanh_tu, P_xanhxanh_mau = simplify_fraction(xanhxanh, khonggianmau)
		P_khongkhong_tu, P_khongkhong_mau = simplify_fraction(khongkhong, khonggianmau)
		P_khongkhong_nhieu_tu, P_khongkhong_nhieu_mau = simplify_fraction(xanhxanh + dodo, khonggianmau)
		P_cungmau_tu, P_cungmau_mau = simplify_fraction(cungmau, khonggianmau)
		P_khacmau_tu, P_khacmau_mau = simplify_fraction(khacmau, khonggianmau)

		P_xanh_tu, P_xanh_mau = simplify_fraction(xanh, khonggianmau)
		P_xanh_nhieu1_tu, P_xanh_nhieu1_mau = simplify_fraction(xanh_nhieu1, khonggianmau)
		P_xanh_nhieu2_tu, P_xanh_nhieu2_mau = simplify_fraction(xanh_nhieu2, khonggianmau)

		P_do_tu, P_do_mau = simplify_fraction(do, khonggianmau)
		P_do_nhieu1_tu, P_do_nhieu1_mau = simplify_fraction(do_nhieu1, khonggianmau)
		P_do_nhieu2_tu, P_do_nhieu2_mau = simplify_fraction(do_nhieu2, khonggianmau)

		P_khong_tu, P_khong_mau = simplify_fraction(khong, khonggianmau)
		P_khong_nhieu1_tu, P_khong_nhieu1_mau = simplify_fraction(do_nhieu1, khonggianmau)

		debai = f"""Có các lọ thủy tinh chứa các dung dịch khác nhau ở bên trong. Trong đó có {axit_chu} lọ chứa dung dịch có tính axit, 
{bazo_chu} lọ chứa dung dịch có tính bazo và {trungtinh_chu} lọ chứa dung dịch trung tính. Nhúng hai mảnh giấy quỳ tím vào hai lọ bất kì khác nhau."""

		ds_abcd = ([(f'''{{\\True Không gian mẫu của phép thử là tập hợp tất cả các kết quả có thể xảy ra khi thự hiện phép thử}}''',
				   f'''Đúng.'''),
				   (f'''{{Phép thử ngẫu nhiên (gọi tắt là phép thử) là một thí nghiệm hay một hành động mà kết quả của nó có thể biết được trước khi phép thử được thực hiện}}''',
				   f'''Sai. Phép thử ngẫu nhiên (gọi tắt là phép thử) là một thí nghiệm hay một hành động mà kết quả của nó KHÔNG thể biết được trước khi phép thử được thực hiện.'''),
				],
				[
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím không đổi màu là $\\dfrac{{ {P_khongkhong_tu} }} {{ {P_khongkhong_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím không đổi màu là $\\dfrac{{ C_{trungtinh}^2 }} {{ C_{n}^2 }} = \\dfrac{{ {P_khongkhong_tu} }} {{ {P_khongkhong_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím không đổi màu là $\\dfrac{{ {P_khongkhong_nhieu_tu} }} {{ {P_khongkhong_nhieu_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím không đổi màu là $\\dfrac{{ C_{trungtinh}^2 }} {{ C_{n}^2 }} = \\dfrac{{ {P_khongkhong_tu} }} {{ {P_khongkhong_mau} }}$.'''),
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím đổi màu đỏ là $\\dfrac{{ {P_dodo_tu} }} {{ {P_dodo_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím đổi màu đỏ là $\\dfrac{{ C_{axit}^2 }} {{ C_{n}^2 }} = \\dfrac{{ {P_dodo_tu} }} {{ {P_khongkhong_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím đổi màu đỏ là $\\dfrac{{ {P_xanhxanh_tu} }} {{ {P_xanhxanh_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím đổi màu đỏ là $\\dfrac{{ C_{axit}^2 }} {{ C_{n}^2 }} = \\dfrac{{ {P_dodo_tu} }} {{ {P_khongkhong_mau} }}$.'''),
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím đổi màu xanh là $\\dfrac{{ {P_xanhxanh_tu} }} {{ {P_xanhxanh_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím đổi màu xanh là $\\dfrac{{ C_{bazo}^2 }} {{ C_{n}^2 }} = \\dfrac{{ {P_xanhxanh_tu} }} {{ {P_khongkhong_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím đổi màu xanh là $\\dfrac{{ {P_dodo_tu} }} {{ {P_dodo_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím đổi màu xanh là $\\dfrac{{ C_{bazo}^2 }} {{ C_{n}^2 }} = \\dfrac{{ {P_xanhxanh_tu} }} {{ {P_khongkhong_mau} }}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím khác màu nhau là $\\dfrac{{ {P_khacmau_tu} }} {{ {P_khacmau_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím khác màu nhau là $\\dfrac{{ {P_khacmau_tu} }} {{ {P_khacmau_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím khác màu nhau là $\\dfrac{{ {P_cungmau_tu} }} {{ {P_cungmau_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím khác màu nhau là $\\dfrac{{ {P_khacmau_tu} }} {{ {P_khacmau_mau} }}$.'''),
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím cùng màu nhau là $\\dfrac{{ {P_cungmau_tu} }} {{ {P_cungmau_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím cùng màu nhau là $\\dfrac{{ {P_cungmau_tu} }} {{ {P_cungmau_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím cùng màu nhau là $\\dfrac{{ {P_khacmau_tu} }} {{ {P_khacmau_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím cùng màu nhau là $\\dfrac{{ {P_cungmau_tu} }} {{ {P_cungmau_mau} }}$.'''),
				],
				[
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu đỏ là $\\dfrac{{ {P_do_tu} }} {{ {P_do_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu đỏ là $\\dfrac{{ {P_do_tu} }} {{ {P_do_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu đỏ là $\\dfrac{{ {P_do_nhieu1_tu} }} {{ {P_do_nhieu1_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu đỏ là $\\dfrac{{ {P_do_tu} }} {{ {P_do_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu đỏ là $\\dfrac{{ {P_do_nhieu2_tu} }} {{ {P_do_nhieu2_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu đỏ là $\\dfrac{{ {P_do_tu} }} {{ {P_do_mau} }}$.'''),
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu xanh là $\\dfrac{{ {P_xanh_tu} }} {{ {P_xanh_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu xanh là $\\dfrac{{ {P_xanh_tu} }} {{ {P_xanh_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu xanh là $\\dfrac{{ {P_xanh_nhieu1_tu} }} {{ {P_xanh_nhieu1_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu xanh là $\\dfrac{{ {P_xanh_tu} }} {{ {P_xanh_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu xanh là $\\dfrac{{ {P_xanh_nhieu2_tu} }} {{ {P_xanh_nhieu2_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy màu xanh là $\\dfrac{{ {P_xanh_tu} }} {{ {P_xanh_mau} }}$.'''),
				   (f'''{{\\True Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy không đổi màu là $\\dfrac{{ {P_khong_tu} }} {{ {P_khong_mau} }}$}}''',
				   f'''Đúng. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy không đổi màu là $\\dfrac{{ {P_khong_tu} }} {{ {P_khong_mau} }}$.'''),
				   (f'''{{Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy không đổi màu là $\\dfrac{{ {P_khong_nhieu1_tu} }} {{ {P_khong_nhieu1_mau} }}$}}''',
				   f'''Sai. Xác suất để hai mảnh giấy quỳ tím có ít nhất một mảnh giấy không đổi màu là $\\dfrac{{ {P_khong_tu} }} {{ {P_khong_mau} }}$.'''),
				])

		# Câu này không có hình vẽ nên chỉ cần gọi 1 hàm dưới đây để sinh code tex
		cauTF+=TF_baitoan_du(debai,ds_abcd,0,0,socot)#Đồ thị phần nào không có thì nhập 0, nếu có thì nhập tên đồ thị vào đúng vị trí của nó
	return cauTF
# ###==== Cách dùng: socau=4 và socot=0

# ##############################################

