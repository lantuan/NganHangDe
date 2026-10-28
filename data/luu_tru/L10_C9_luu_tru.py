# -*- coding: utf-8 -*-
r"""LƯU TRỮ - bản CŨ năm câu Đúng/Sai chương 9 lớp 10 (KHÔNG ra đề; web và bộ ráp đề không đọc data/luu_tru/).

Thay ngày 28/10/2026 theo yêu cầu cô Lan ("cần, bổ sung luôn cho tôi"): bản cũ (cô nhập 28/09/2026 từ LopXChuong9.py)
chưa xếp bốn ý theo bậc NB -> TH -> VD -> VDC, mỗi ý chỉ 1 phát biểu đúng + 1 phát biểu sai (TF_C, TF_D ý a chỉ có
phát biểu đúng), vài lời giải chỉ ghi "Đúng." / "Sai.", TF_E có lời giải ghi sai mẫu số. Bản mới cùng ID, cùng bối
cảnh nằm trong data/python_bank/toan10/L10_C9.py. Giữ bản cũ ở đây để cô đối chiếu; tệp này không chạy được độc lập
(thiếu phần import của tệp chương).
"""

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


