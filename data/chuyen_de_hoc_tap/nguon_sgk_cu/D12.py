from sympy import Symbol,solve,sqrt,factor,cancel,Poly,Eq,Function,exp
from sympy.abc import x,y,z,a,b
from sympy import init_printing
from sympy import *
import numpy.random as np
from sympy.solvers.solvers import unrad
from sympy import nroots
from sympy.solvers.solvers import solve_linear
from sympy import cos, sin, tan
from sympy import solve_poly_system
from sympy import Matrix, solve_linear_system
from sympy.solvers.solvers import solve_linear_system_LU
from sympy import Eq
from sympy.solvers import solve_undetermined_coeffs
from sympy.solvers import checksol
from sympy.solvers.polysys import solve_triangulated

import random
from fractions import Fraction

#from __future__ import print_function, division

from sympy.core import Symbol, Dummy, sympify
from sympy.core.compatibility import iterable
from sympy.core.exprtools import factor_terms
from sympy.core.relational import Relational, Eq, Ge, Lt, Ne
from sympy.sets import Interval
from sympy.sets.sets import FiniteSet, Union, EmptySet, Intersection
from sympy.sets.fancysets import ImageSet
from sympy.core.singleton import S
from sympy.core.function import expand_mul
from sympy.core.power import Pow
from sympy.polys.polytools import cancel

from sympy.functions import Abs
from sympy.logic import And
from sympy.polys import Poly, PolynomialError, parallel_poly_from_expr
from sympy.polys.polyutils import _nsort
from sympy.utilities.iterables import sift
from sympy.utilities.misc import filldedent

import DefChung as dc


import io
import os
import itertools ### tổ hợp, chỉnh hợp, hoán vị


import inspect
import sys


def D12Y1_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
	  a = np.randint(10,15)
	  b = np.randint(5,10)
	  z = a+b
	  Z = [z,a*b,z+1,a*b+1]
	  de.write(r"\begin{ex}"+ os.linesep)
	  de.write(r"Một bạn muốn đi từ tỉnh $A$ tới tỉnh $B$ trong một ngày nhất định. "+ os.linesep)
	  de.write(r"Biết rằng trong ngày hôm đó từ tỉnh $A$ đến tỉnh $B$ có $%s$ chuyến ô tô, $%s$ chuyến tàu. " %(a,b) + os.linesep)
	  de.write(r"Hỏi bạn đó có bao nhiêu sự lựa chọn để đi từ $A$ đến $B$?"+ os.linesep)
	  de.write(r"\choice"+ os.linesep)
	  de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
	  de.write(r"\loigiai{}"+ os.linesep)
	  de.write(r"\dotlineEX{10}"+ os.linesep)
	  de.write(r"\end{ex}"+ os.linesep)


def D12Y1_2():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
	  a = np.randint(5,15)
	  b = np.randint(5,15)
	  c = np.randint(5,15)
	  z = a+b+c
	  Z = [z,a*b*c,z+1,a*b*c+1]
	  de.write(r"\begin{ex}"+ os.linesep)
	  de.write(r"Một cửa hàng có $%s$ bó hoa Ly, $%s$ bó hoa Huệ, $%s$ bó hoa Lan. " %(a,b,c) + os.linesep)
	  de.write(r"Một bạn muốn mua $1$ bó hoa tại cửa hàng này. Hỏi bạn đó có bao nhiêu sự lựa chọn?"+ os.linesep)
	  de.write(r"\choice"+ os.linesep)
	  de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
	  de.write(r"\loigiai{}"+ os.linesep)
	  de.write(r"\dotlineEX{10}"+ os.linesep)
	  de.write(r"\end{ex}"+ os.linesep)



def D12Y1_3(): # đã chuyển sang sgk mưới
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
	  lop = np.choice([30,35,40,45])
	  nu = np.randint(10,20)
	  nam = lop - nu
	  z = nam + nu
	  Z = [z,nam * nu,z+1,nam * nu + 1]
	  de.write(r"\begin{ex}"+ os.linesep)
	  de.write(r"Một lớp có $%s$ học sinh nam, $%s$ học sinh nữ. " %(nam, nu) + os.linesep)
	  de.write(r"Hỏi giáo viên có bao nhiêu cách chọn ngẫu nhiên một bạn trong lớp để làm lớp trưởng?" + os.linesep)
	  de.write(r"\choice"+ os.linesep)
	  de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
	  de.write(r"\loigiai{}"+ os.linesep)
	  de.write(r"\dotlineEX{10}"+ os.linesep)
	  de.write(r"\end{ex}"+ os.linesep)



def D12Y1_4():# đã chuyển qua sgk mới
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
	  a = np.randint(3,7)
	  b = np.randint(3,7)
	  c = np.randint(3,7)
	  z = a+b+c
	  Z = [z,a*b*c,z+1,a*b*c+1]
	  de.write(r"\begin{ex}"+ os.linesep)
	  de.write(r"Một nhà hàng có $%s$ loại rượu, $%s$ loại bia, $%s$ loại nước uống khác. " %(a,b,c) + os.linesep)
	  de.write(r"Một thực khách muốn lựa chọn một loại đồ uống thì có bao nhiêu cách chọn?"+ os.linesep)
	  de.write(r"\choice"+ os.linesep)
	  de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
	  de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
	  de.write(r"\loigiai{}"+ os.linesep)
	  de.write(r"\dotlineEX{10}"+ os.linesep)
	  de.write(r"\end{ex}"+ os.linesep)


def D12Y1_5(): # đã chuyển sang sgk mới
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		abc = []
		k = np.randint(2,4)
		for i in range(0,10):
			if i % k == 0:
				abc.append(i)
			else:
				pass
		z = len(abc)
		Z= [z,z-1,10-z,10-z+1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tập hợp $A=\{0;1;2;3;\cdots;8;9\}$ và số có ba chữ số $\overline{abc}$, với $a,b,c$ là các chữ số được lấy từ tập $A$. "+ os.linesep)
		de.write(r"Hỏi có bao nhiêu cách chọn giá trị của $c$ để $\overline{abc}$ chia hết cho $%s$?" %(k) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)



def D12B1_6():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		dk = np.randint(2,5)
		dk_dict = {2: "hai", 3: "ba", 4: "bốn"}
		z1 = 0
		for i in range(0,dk):
			z1 += 9*10**i
		z2 = 10**(dk-1) 
		z = int((z1 - z2 + 1)/2)
		Z= [z,z-1,int((z1 - z2 - 1)/2),int((z1 - z2 - 1)/2 + 1)]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có bao nhiêu số tự nhiên chẵn có %s chữ số?" %(dk_dict[dk]) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12B1_6_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		dk = np.randint(2,5)
		dk_dict = {2: "hai", 3: "ba", 4: "bốn"}
		z1 = 0
		for i in range(0,dk):
			z1 += 9*10**i
		z2 = 10**(dk-1)
		z = (z1 - z2 + 1)
		Z= [z,z-1,(z1 - z2 - 1),(z1 - z2 - 1) + 1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có bao nhiêu số tự nhiên có %s chữ số?" %(dk_dict[dk]) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B1_7():# đã chuyển sang sgk mới
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Một bài thi trắc nghiệm khách quan gồm $10$ câu. " + os.linesep)
		de.write(r"Mỗi câu có 4 phương án trả lời. Một học sinh chọn ngẫu nhiên các phương án và làm hết thi. " + os.linesep)
		de.write(r"Hỏi có bao nhiêu cách để học sinh chọn các phương án trong bài thi của mình?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$10^4$}" + os.linesep)
		de.write(r"{\True $4^{10}$}" + os.linesep)
		de.write(r"{$40$}" + os.linesep)
		de.write(r"{$400$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B1_8():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có bao nhiêu số tự nhiên có $5$ chữ số trong đó các chữ số cách đều chữ số đứng giữa thì giống nhau?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$81000$ số}" + os.linesep)
		de.write(r"{\True $900$ số}" + os.linesep)
		de.write(r"{$720$ số}" + os.linesep)
		de.write(r"{$29$ số}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K1_9():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có bao nhiêu số tự nhiên có hai chữ số mà chữ số hàng chục lớn hơn chữ số hàng đơn vị?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$40$}{$50$}{$35$}{\True $45$}" + os.linesep)
		de.write(r"\loigiai{+ Gọi số cần tìm có dạng $\overline{ab}$ với $a>b$.\\ " + os.linesep)
		de.write(r"+ Ta thấy số tự nhiên có hai chữ số là 90 số. Trong 90 số này thì có 45 số thỏa mãn đề bài và " + os.linesep)
		de.write(r"	45 số mà chữ số hàng đơn vị lớn hơn chữ số hàng chục.}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K1_10():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		n = np.randint(4,9)
		A = []
		for index in range(0,n):
			A.append(index+1)
		m = np.randint(2,5)
		num = 10**(m)
		z = 0
		for index in range(0,m):
			z += n**(index+1)
		Z = [z,z-n,dc.chinhhop(n,m-1),dc.chinhhop(n,m-1)+n]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Từ các chữ số $%s$ có thể lập được bao nhiêu số tự nhiên bé hơn $%s$?" %(A,num) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{Ta xét các trường hợp sau\\" + os.linesep)
		for index in range(0,m):
			de.write(r"TH%s. Số tạo thành có %s chữ số. Trường hợp này có $%s$ số thỏa mãn. \\" %(index+1,index+1,n**(index+1)) + os.linesep)
		de.write(r"Vậy có $%s$ số thỏa mãn đề bài.}" %(z) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12Y1_11():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(3,6)
		b = np.randint(4,7)
		z = a*b
		Z = [z, a+b, z + 1, a+b+1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Nhà Bình ở giữa nhà An và nhà Dũng. An muốn qua nhà Bình để cùng Bình đến nhà Dũng chơi. " + os.linesep)
		de.write(r"Từ nhà An đến nhà Bình có $%s$ đường đi, từ nhà Bình đến nhà Dũng có $%s$ đường đi. " %(a,b) + os.linesep)
		de.write(r"Hỏi có bao nhiêu cách đi từ nhà An đến nhà Dũng?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12G1_12():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(4,9)
		A = []
		S = 0
		ex = 0
		xe = 0
		for index in range(0,a):
			A.append(index + 1)
			S += (1+a)*10**(index)
			ex += (a-index)*10**(index)
			xe += (index+1)*10**(index)
		z = (dc.giaithua(a)/2)*S
		Z = [z, z+1, (dc.giaithua(a))*S,(dc.giaithua(a))*S+1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng của tất cả các số tự nhiên có $%s$ chữ số đôi một khác nhau được lập thành từ các chữ số $%s$." %(a,A) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{Dễ thấy có $%s ! = %s$ số tạo thành mà các chữ số đôi một phân biêt.\\" %(a, dc.giaithua(a)) + os.linesep)
		de.write(r"Trong $%s$ số đó luôn tồn tại một cặp sao tổng của nó bằng $%s$ giả sử như cặp $%s$ và $%s$.\\" %(a,S,ex,xe) + os.linesep)
		de.write(r"Vậy tổng các chữ số được tạo thành là $%s \cdot %s = %s$.}" %(dc.giaithua(a)/2, S, z) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K1_13():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có  bao nhiêu số  tự nhiên có  ba chữ số đôi một khác  nhau chia hết cho $5$ được tạo thành từ các  số $0,1,2,3,4,5$?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$25$}{\True $36$}{$55$}{$60$}" + os.linesep)
		de.write(r"\loigiai{Để số tạo thành chia  hết cho $5$  thì  chữ số tận cùng  là  $0$ hoặc $5$.\\" + os.linesep)
		de.write(r"+ Giả  sử  số tạo thành  có dạng $\overline{abc}$." + os.linesep)
		de.write(r"TH1. Nếu $c=0$ có  $5$ cách chọn chữ số $a$ và $4$ cách chọn  $b$. Trường  hợp này có  $4.5=20$ số.\\" + os.linesep)
		de.write(r"TH2. Nếu $c=5$ có  $4$ cách chọn chữ số $a$ và 4 cách chọn $b$. Trường  hợp này có  $4.4=16$ số.\\" + os.linesep)
		de.write(r"Vậy có  $36$ số thỏa mãn.}" + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K2_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		A = []
		n = np.randint(5,10)
		for index in range(0,n):
			A.append(index)
		dk1 = np.randint(4,len(A))
		while dk1 == 0:
			dk1 = np.randint(4,len(A))
		dk2 = np.choice(A)
		while dk2 == 0:
			dk2 = np.choice(A)
		z = dk1 * dc.chinhhop(len(A)-1, dk1-1) - (dk1 - 1) * dc.chinhhop(len(A)-2, dk1-2)
		Z= [z,dk1 * dc.chinhhop(len(A)-1, dk1-1), dk1 * dc.tohop(len(A)-1, dk1-1) - (dk1 - 1) * dc.tohop(len(A)-2, dk1-2), dk1 * dc.tohop(len(A)-1, dk1-1)]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Từ các chữ số $ %s $ có thể lập được bao nhiêu số tự nhiên có " %(latex(A)) + os.linesep)
		de.write(r"	%s chữ số đôi một khác nhau, trong đó nhất thiết phải có mặt chữ số $%s$?" %(dk1, dk2) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{Vị trí đầu tiên là số $0$ có $%s \times \mathrm{A}_{%s}^{%s}$ cách.\\" %(dk1-1, len(A)-2, dk1-2) + os.linesep)
		de.write(r"Chỉ cần có mặt chữ số $%s$ có $%s \times \mathrm{A}_{%s}^{%s}$ cách." %(dk2, dk1, len(A)-1, dk1-1) + os.linesep)
		de.write(r"Suy ra có số cách là $%s \times \mathrm{A}_{%s}^{%s} - %s \times \mathrm{A}_{%s}^{%s}$.}" 
			%(dk1, len(A)-1, dk1-1, dk1-1, len(A)-2, dk1-2) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K2_2():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(15,26)
		z = dc.chinhhop(a,2)
		Z = [z,dc.tohop(a,2),z-1,dc.tohop(a,2)-1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong một giải bóng đá vô địch quốc gia có $%s$ câu lạc bộ tham gia thi đấu. " %(a) + os.linesep)
		de.write(r"	Trong một mùa giải mỗi câu lạc bộ sẽ thi đấu với các đối thủ khác hai lần (vòng tròn hai lượt), " + os.linesep)
		de.write(r"	một trên sân nhà của họ và một trận sân đối phương. " + os.linesep)
		de.write(r"Hỏi ban tổ chức phải tổ chức tất cả bao nhiêu trận đấu trong một mùa giải?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{Giả sử $%s$ đội đó là $D_1$, $D_2$, $\dots$, $D_{%s}$. " %(a,a) + os.linesep)
		de.write(r"Chọn hai đội $D_i$ và $D_j$ $(i\ne j)$ từ $%s$ đội ở trên và sắp xếp hai đội đó thành một bộ $(D_i,D_j)$ (quy ước bộ $(D_i,D_j)$ khác bộ $(D_j,D_i)$). " %(a) + os.linesep)
		de.write(r"Trước hết ta chọn đội xếp vào vị trí thứ nhất có $%s$ cách. " %(a) + os.linesep)
		de.write(r"Sau đó ta chọn đội xếp vào vị trí thứ hai có $%s$ cách. " %(a-1) + os.linesep)
		de.write(r"Do đó có $%s \cdot %s$ cách." %(a,a-1) + os.linesep)
		de.write(r"Vậy ban tổ chức phải tổ chức tất cả $%s$ trận đấu trong một mùa giải." %(a*(a-1)) + os.linesep)
		de.write(r"Hoặc, chọn $2$ trong số $%s$ thi đấu, có phân biệt thứ tự: $\mathrm{A}_{%s}^{2}$}" %(a,a) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K2_3():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Hỏi có bao nhiêu cách xếp $6$ cặp vợ chồng xung quanh một bàn tròn có $12$ ghế sao cho nam " + os.linesep)
		de.write(r"và nữ ngồi xen kẽ nhau và mỗi người ngồi đúng một ghế?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $86400$ cách xếp}" + os.linesep)
		de.write(r"{$720$ cách xếp}" + os.linesep)
		de.write(r"{$172800$ cách xếp}" + os.linesep)
		de.write(r"{$840$ cách xếp}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K2_4():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Một đa giác lồi có $n$ cạnh thì có bao nhiêu đường chéo?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\dfrac{n(n-1)}{2}$} {$\dfrac{n(n-2)}{2}$} {\True $\dfrac{n(n-3)}{2}$} {$n(n-3)$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12B2_5():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tất cả các số nguyên dương $n$ thỏa mãn $\dfrac{1}{\mathrm{C}^1_n}-\dfrac{1}{\mathrm{C}^2_{n+1}}=\dfrac{7}{6\mathrm{C}^1_{n+4}}$." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$n=3$} {$n=8$} {\True $n=3$ hoặc $n=8$} {$n=5$ hoặc $n=7$} " + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B2_6():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Cho tập $S$ có $n$ điểm phân biệt ($n$ nguyên dương). Biết rằng có $90$ vec-tơ khác vectơ " + os.linesep)
		de.write(r"	$\overrightarrow{0}$ có điểm đầu và điểm cuối thuộc $S$. Tìm $n$." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $10$}{$11$}{$12$}{$9$} " + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B2_7():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Cho 2016 điểm phân biệt trong mặt phẳng trong đó không có 3 điểm nào thẳng hàng. " + os.linesep)
		de.write(r"Hỏi có thể lập được tất cả bao nhiêu tam giác từ các điểm trên?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\mathrm{A}_{2016}^3$}	{\True $\mathrm{C}_{2016}^3$}	{$672$}	{Vô số}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K2_8():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(4,7)
		b = np.randint(4,7)
		z = 2 * dc.tohop(a,2) + dc.tohop(b,2) + 2*a*b
		Z = [z, 2 * dc.tohop(a,2) + b + 2*a*b, 2 * dc.tohop(a,2) + dc.tohop(b,2) + a*b, dc.tohop(a,2) + dc.tohop(b,2) + 2*a*b, dc.tohop(a,2) + dc.tohop(b,2) + a*b]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có $%s$ đường tròn và $%s$ đường thẳng phân biệt. Hỏi tất cả các đường tròn, " %(a,b) + os.linesep)
		de.write(r"các đường thẳng đã cho có tối đa bao nhiêu giao điểm?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{Số giao điểm tối đa của $%s$ đường tròn : $2 \cdot \mathrm{C}_{%s}^2$ (Do lấy $2$ trong $%s$ đường tròn thì cắt tại $2$ điểm)\\" %(a,a,a) + os.linesep)
		de.write(r"Số giao điểm tối đa của $%s$ đường thẳng : $\mathrm{C}_{%s}^2$\\ (Do lấy $2$ trong $%s$ đường thẳng thì cắt tại $1$ điểm)\\" %(b,b,b) + os.linesep)
		de.write(r"Số giao điểm tối đa của đường tròn và đường thẳng : $2 \cdot %s \cdot %s$. (Do chọn $1$ đường tròn thì có thể chọn được $%s$ đường thẳng " %(b,a,b) + os.linesep)
		de.write(r"	, số giao điểm là $2$. Ta được $2 \cdot %s$. Mà có thể chọn được $%s$ đường tròn nên số giao điểm là $2 \cdot %s \cdot %s$)}" %(b,a,b,a) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12B2_9():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		n = np.randint(10,20)
		k = np.randint(3,n-3)
		l = np.randint(3,n-3)
		while k == l:
			l = np.randint(3,n-3)
		z = dc.tohop(n,l)
		Z = [z, dc.chinhhop(n,l), dc.tohop(n,k), dc.chinhhop(n,k)]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Nếu $\mathrm{C}_{n}^{%s}=\mathrm{C}_{n}^{%s}$ thì $\mathrm{C}_{n}^{%s}$ bằng" %(k,n-k,l) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B2_9_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		n = np.randint(10,20)
		k = np.randint(3,n-3)
		l = np.randint(3,5)
		while k == l:
			l = np.randint(3,5)
		z = int(dc.tohop(n,l) + dc.chinhhop(n,l))
		Z = [z, int(dc.chinhhop(n,l)), int(dc.tohop(n,l)), int(dc.chinhhop(n,k))]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Nếu $\mathrm{C}_{n}^{%s}=\mathrm{C}_{n}^{%s}$ thì $\mathrm{C}_{n}^{%s} + \mathrm{A}_{n}^{%s}$ bằng" %(k,n-k,l,l) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K2_10():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(10,20)
		b = np.randint(10,20)
		while a == b:
			b = np.randint(10,20)
		z = a*dc.tohop(b,2) + b*dc.tohop(a,2)
		Z = [z, a*dc.chinhhop(b,2) + b*dc.chinhhop(a,2), a*dc.chinhhop(b,2) + b*dc.tohop(a,2), a*dc.tohop(b,2) + b*dc.chinhhop(a,2)]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Cho hai đường thẳng $a\parallel b$, trên đường thẳng $a$ lấy $%s$ điểm phân biệt, " %(a) + os.linesep)
		de.write(r"trên đường thẳng $b$ lấy $%s$ điểm phân biệt. Tính số tam giác có đỉnh là $3$ điểm trong số " %(b) + os.linesep)
		de.write(r"	$%s$ điểm đã chọn trên đường thẳng $a$ và $b$." %(a+b) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{\textbf{TH1.} Tam giác được tạo thành từ một đỉnh thuộc đường thẳng $a$ và $2$ đỉnh thuộc đường thẳng $b$. 	Khi đó trên $a$ có "+ os.linesep)
		de.write(r"$%s$ cách chọn đỉnh, trên $b$ có $\mathrm{C}_{%s}^2$ cách chọn đỉnh. Vậy có $%s \cdot \mathrm{C}_{%s}^2$ tam giác.\\" %(a,b,a,b) + os.linesep)
		de.write(r"\textbf{TH2.} Tam giác được tạo thành từ một đỉnh thuộc đường thẳng $b$ và $2$ đỉnh thuộc đường thẳng $a$. Khi đó trên $b$ có "+ os.linesep)
		de.write(r"$%s$ cách chọn đỉnh, trên $a$ có $\mathrm{C}_{%s}^2$ cách chọn đỉnh. Vậy có $%s \cdot \mathrm{C}_{%s}^2$ tam giác.\\" %(b,a,b,a) + os.linesep)
		de.write(r"Vậy có tất cả $%s \cdot \mathrm{C}_{%s}^2 + %s \cdot \mathrm{C}_{%s}^2 = %s$ tam giác." %(a,b,b,a,z) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K2_10():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(10,20)
		b = np.randint(10,20)
		while a == b:
			b = np.randint(10,20)
		tamgiac = a*dc.tohop(b,2) + b*dc.tohop(a,2)
		z = b
		Z = [z, b+1, b-1, b-2]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Cho hai đường thẳng $a\parallel b$, trên đường thẳng $a$ lấy $%s$ điểm phân biệt, " %(a))
		de.write(r"trên đường thẳng $b$ lấy $n$ điểm phân biệt $(n\geq 2)$. Biết rằng có $%s$ tam giác có đỉnh là các điểm đã cho. " %(tamgiac))
		de.write(r"Tìm $n$ thỏa mãn điều kiện trên." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{\textbf{TH1.} Tam giác được tạo thành từ một đỉnh thuộc đường thẳng $a$ và $2$ đỉnh thuộc đường thẳng $b$. 	Khi đó trên $a$ có "+ os.linesep)
		de.write(r"$%s$ cách chọn đỉnh, trên $b$ có $\mathrm{C}_{n}^2$ cách chọn đỉnh. Vậy có $%s \cdot \mathrm{C}_{n}^2$ tam giác.\\" %(a,a) + os.linesep)
		de.write(r"\textbf{TH2.} Tam giác được tạo thành từ một đỉnh thuộc đường thẳng $b$ và $2$ đỉnh thuộc đường thẳng $a$. Khi đó trên $b$ có "+ os.linesep)
		de.write(r"$n$ cách chọn đỉnh, trên $a$ có $\mathrm{C}_{%s}^2$ cách chọn đỉnh. Vậy có $n \cdot \mathrm{C}_{%s}^2$ tam giác.\\" %(a,a) + os.linesep)
		de.write(r"Vậy có $%s \cdot \mathrm{C}_{n}^2 + n \cdot \mathrm{C}_{%s}^2 = %s \Rightarrow n = %s$}." %(a,a,tamgiac,b) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B2_11():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		gai = np.randint(3,6)
		trai = np.randint(3,7)
		z = dc.giaithua(gai + trai)
		Z = [z, gai*trai, z+1, gai*trai-1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Xếp $%s$ bé trai và $%s$ bé gái trên một ghế dài. Hỏi có bao nhiêu cách xếp?" %(trai,gai) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B2_12():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		lop = np.randint(30,45)
		truc = np.randint(2,6)
		truc_dict = {2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm'}
		z = int(dc.tohop(lop,truc))
		Z = [z, int(dc.chinhhop(lop,truc)), int(dc.giaithua(truc)), lop*truc]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Lớp $11A$ có $%s$ học sinh. Hỏi có bao nhiêu cách phân công %s bạn " %(lop, truc_dict[truc]) )
		de.write(r"	từ các học sinh thuộc lớp $11A$ để làm trực tuần?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B2_13():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		M = np.randint(5,11)
		m = np.randint(2,5)
		m_dict = {2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm'}
		z = int(dc.tohop(M,m))
		Z = [z, int(dc.chinhhop(M,m)), dc.giaithua(m), M*m]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có $%s$ bút chì màu khác nhau, có bao nhiêu cách chọn %s chiếc?" %(M,m_dict[m]))
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12B2_14():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		M = np.randint(8,15)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có $%s$ giáo viên làm giám thị coi $%s$ phòng thi. Biết rằng mỗi phòng thi có hai giám thị gồm một giám thị một " %(2*M,M) + os.linesep )
		de.write(r"	và một giám thị hai. Hỏi có bao nhiêu cách phân công giám thị "  + os.linesep )
		de.write(r"một và  giám thị hai vào mỗi phòng thi?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s !$}" %(2*M) + os.linesep)
		de.write(r"{$\mathrm{C}_{%s}^2$}" %(2*M) + os.linesep)
		de.write(r"{$\mathrm{A}_{%s}^2$}" %(2*M) + os.linesep)
		de.write(r"{$\mathrm{C}_{%s}^{%s}$}" %(2*M,M) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K2_15():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		z = 2
		Z = [z,3,17,15]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tổng tất cả các giá trị của $x$ thỏa phương trình $\dfrac{1}{\mathrm{C}_4^x} - \dfrac{1}{\mathrm{C}_5^x}=\dfrac{1}{\mathrm{C}_6^x}$.")
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K2_16():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Cho $n$ điểm trong đó có $m$ điểm nằm trên đường thẳng $d$ ($n>m\ge3$). ")
		de.write(r"Biết ba điểm bất kì không cùng thuộc $d$ thì đều không thẳng hàng. ")
		de.write(r"Hỏi có thể nối được bao nhiêu tam giác từ $n$ điểm đã cho?   ")
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\mathrm{C}_n^3$}{$\mathrm{C}_m^3$}{\True $\mathrm{C}_n^3-\mathrm{C}_m^3$}{$\mathrm{C}_n^3+\mathrm{C}_m^3$}" + os.linesep)
		de.write(r"\loigiai{Số cách lấy 3 điểm trong $n$ điểm tạo thành tam giác là $\mathrm{C}_n^3$.\\"+ os.linesep)
		de.write(r"Số cách lấy 3 điểm trong $m$ điểm là $\mathrm{C}_n^3$. Các cách này không tạo ra tam giác.\\"+ os.linesep)
		de.write(r"Vậy số tam giác là $\mathrm{C}_n^3-\mathrm{C}_m^3$.}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12Y2_17(k):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
#		k = np.randint(0,1)
		de.write(r"\begin{ex}" + os.linesep)
		if k == 0:
			de.write(r"Với $n$ thuộc tập số tự nhiên, khẳng định nào sau đây đúng?" + os.linesep)
			de.write(r"\choice"+ os.linesep)
			de.write(r"{\True $A_n^n = P_n$}" + os.linesep)
			de.write(r"{$A^0_n = P_n$}" + os.linesep)
			de.write(r"{$C^n_n = P_n$}" + os.linesep)
			de.write(r"{$C^0_n = P_n$}" + os.linesep)
		else:
			de.write(r"Với $n$ thuộc tập số tự nhiên, khẳng định nào sau đây đúng?" + os.linesep)
			de.write(r"\choice"+ os.linesep)
			de.write(r"{\True $C_n^0 = A_n^0$}" + os.linesep)
			de.write(r"{$C_n^1 = A_n^0$}" + os.linesep)
			de.write(r"{$A_n^n = A_n^0$}" + os.linesep)
			de.write(r"{$P_n = A_n^0$}" + os.linesep)

		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)



def D12Y2_18(k):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
#		k = np.randint(0,1)
		de.write(r"\begin{ex}" + os.linesep)
		if k == 0:
			de.write(r"Có bao nhiêu cách sắp xếp $n$ cuốn sách khác nhau lên một giá sách theo một hàng ngang?" + os.linesep)
		else:
			de.write(r"Có bao nhiêu cách sắp xếp $n$ học sinh đứng vào một hàng ngnag?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $P_n$}" + os.linesep)
		de.write(r"{$n(n-1)$}" + os.linesep)
		de.write(r"{$C^n_n$}" + os.linesep)
		de.write(r"{$C^0_n$}" + os.linesep)

		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12B3_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		n = np.randint(10,20)
		a = np.randint(2,5)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Ba số hạng đầu tiên theo lũy thừa tăng dần của $x$ trong khai triển $(1+%sx)^{%s}$ là" %(a,n) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$; $%s$; $%s$}" %(latex(dc.NT_Newton_list(1,a*x,n)[0]),latex(dc.NT_Newton_list(1,a*x,n)[1]),latex(dc.NT_Newton_list(1,a*x,n)[2])) + os.linesep)
		de.write(r"{\True $%s$; $%s$; $%s$}" %(latex(dc.NT_Newton_list(1,(a+1)*x,n)[0]),latex(dc.NT_Newton_list(1,(a+1)*x,n)[1]),latex(dc.NT_Newton_list(1,(a+1)*x,n)[2])) + os.linesep)
		de.write(r"{$%s$; $%s$; $%s$}" %(latex(dc.NT_Newton_list(1,a*x,n)[0]),latex(dc.NT_Newton_list(1,(a+1)*x,n)[1]),latex(dc.NT_Newton_list(1,a*x,n)[2])) + os.linesep)
		de.write(r"{$%s$; $%s$; $%s$}" %(latex(dc.NT_Newton_list(1,a*x,n)[0]),latex(dc.NT_Newton_list(1,a*x,n)[1]),latex(dc.NT_Newton_list(1,(a+1)*x,n)[2])) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K3_2():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng $S = \mathrm{C}_{20}^0-\mathrm{C}_{20}^1+\mathrm{C}_{20}^2- \ldots +\mathrm{C}_{20}^{20}.$" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $S = 0 $}	{$S=1 $}	{$S =-2$}	{$S = (-2)^{20} $}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K3_3():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng $S = \mathrm{C}_{20}^0+2\mathrm{C}_{20}^1+2^2\mathrm{C}_{20}^2+ \ldots +2^{20}\mathrm{C}_{20}^{20}.$" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$ S=2^{21}$}	{$S=3^{21} $}	{\True $S=3^{20} $}	{$ S=2^{20}$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K3_4():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng $S = \mathrm{C}_{21}^0-2\mathrm{C}_{21}^1+2^2\mathrm{C}_{21}^2-...-2^{21}\mathrm{C}_{21}^{21}.$" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $S= -1 $}	{$S=1 $}	{$S = (-3)^{21} $}	{$S = 3^{21} $}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K3_4():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng $S = \mathrm{C}_{21}^0-2\mathrm{C}_{21}^1+2^2\mathrm{C}_{21}^2-...-2^{21}\mathrm{C}_{21}^{21}.$" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$ S =\left(- \dfrac{1}{2}\right)^{21}$}	{$S = \dfrac{1}{2} $}	{\True $S = \dfrac{1}{2^{21}} $}	{$S = -\dfrac{1}{2} $}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K3_5():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong khai triển $\left(3x^3-\dfrac{2}{x^2}\right)^5$ tìm hệ số của số hạng chứa $x^{10}$." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$810$}	{\True $-810$}	{$405$}	{$-405$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K3_6():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm hệ số $ x^{1008} $ trong khai triển $ \left( x^2+\dfrac{1}{x^3}\right)^{2009} $." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $\mathrm{C}_{2009}^{602} $}	{$\mathrm{C}_{2009}^{603} $}	{$\mathrm{C}_{2009}^{604} $}	{$\mathrm{C}_{2009}^{605} $}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K3_7():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm số hạng không chứa $ x $ trong khai triển nhị thức $ \left( x^2+\dfrac{1}{x^3}\right) ^n $, biết rằng $ \mathrm{C}_n^1+\mathrm{C}_n^3=13n .$" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$ \mathrm{C}_{10}^3 $}	{\True $ \mathrm{C}_{10}^4 $}	{$ \mathrm{C}_{10}^5 $}	{$ \mathrm{C}_{10}^6 $}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12G3_8():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm hệ số $ x^{8} $ trong khai triển đa thức của $\left[1+x^2(1-x) \right]^8 $." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$ 148$}	{$ 192$}	{\True $238 $}	{$245 $}" + os.linesep)
		de.write(r"\loigiai{Ta có: $ f(x)=\mathrm{C}_8^0+\dots+\mathrm{C}_8^3[x^2(1-x)]^3+\mathrm{C}_8^4[x^2(1-x)]^4+\dots+\mathrm{C}_8^8[x^2(1-x)]^8 $.\\" + os.linesep)
		de.write(r"Nhận thấy $ x^8 $ chỉ có trong các số hạng: " + os.linesep)
		de.write(r"\begin{itemize}" + os.linesep)
		de.write(r"	\item Số hạng thứ tư: $ \mathrm{C}_8^3[x^2(1-x)]^3 $." + os.linesep)
		de.write(r"	\item Số hạng thứ năm: $ \mathrm{C}_8^4[x^2(1-x)]^4 $." + os.linesep)
		de.write(r"\end{itemize}" + os.linesep)
		de.write(r"Vậy hệ số cần tìm là $ A_8=\mathrm{C}_8^3 \mathrm{C}_3^2+\mathrm{C}_8^4 \mathrm{C}_4^0=238 $.}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12G3_9():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm hệ số của $ x^6 $ trong khai triển biểu thức $ (1+x^2)^4(3-x)^2 $ thành đa thức bậc $ 10 $." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $42 $}	{$56 $}	{$83 $}	{$105 $}" + os.linesep)
		de.write(r"\loigiai{Số hạng tổng quát trong khai triển Newton của biểu thức $ (1+x^2)^4 $ là "+ os.linesep)
		de.write(r"$$ \mathrm{C}_4^k(x^2)^k=\mathrm{C}_4^kx^{2k}\,\, (k\in \mathbb{N}, 0 \le k \le 4) .$$"+ os.linesep)
		de.write(r"Số hạng tổng quát trong khai triển Newton của biểu thức $ (3-x)^2 $ là "+ os.linesep)
		de.write(r"$$ \mathrm{C}_2^i 3^{2-i}(-x)^i=\mathrm{C}_2^i 3^{2-i}(-1)^ix^i,\, (i\in \mathbb{N}, 0 \le i \le 2) $$"+ os.linesep)
		de.write(r"Nhân hai số hạng ta được biểu thức $ \mathrm{C}_4^k.\mathrm{C}_2^i(-1)^i3^{2-i}x^{2k+i} $. "+ os.linesep)
		de.write(r"Ta tìm tất cả các cặp số tự nhiên $ k, i $ thoả $ k \le 4 $ và $ i \le 2 $ sao cho $ 2k+i=6 $ thì được "+ os.linesep)
		de.write(r"$\heva{&k=3\\&i=0}$ hay $ \heva{&k=2\\&i=2} $.\\"+ os.linesep)
		de.write(r"Suy ra hệ số của $ x^6 $ là $ \mathrm{C}_4^3\mathrm{C}_2^0(-1)^03^2+\mathrm{C}_4^2\mathrm{C}_2^2(-1)^23^0=42 $.}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12G3_10():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển $ P(x)=(2x+1)^4+(2x+1)^5+(2x+1)^6+(2x+1)^7 $ thành đa thức, ta được " + os.linesep)
		de.write(r"$P(x)=a_0+a_1x+a_2x^2+a_3x^3+a_4x^4+a_5x^5+a_6x^6+a_7x^7$. Tìm $ a_5 $." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$321 $}	{$ 956$}	{$ 415$}	{\True $ 896$}" + os.linesep)
		de.write(r"\loigiai{Các số hạng chứa $ x^5 $ chỉ xuất hiện trong khai triển Newton của các biểu thức "+ os.linesep)
		de.write(r"$ (2x+1)^5, (2x+1)^6, (2x+1)^7 $ và chúng lần lượt là $ \mathrm{C}_5^0(2x)^5, \mathrm{C}_6^1(2x)^5 $ "+ os.linesep)
		de.write(r"và $ \mathrm{C}_7^2(2x)^5 $. Suy ra hệ số $ a_5 $ của $ x^5 $ trong khai triển của $ P(x) $ là "+ os.linesep)
		de.write(r"$ a_5=\mathrm{C}_5^0 2^5+\mathrm{C}_6^1 2^5+\mathrm{C}_7^2 2^5=896 $. }"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12G3_11():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển $ Q(x)=(1+x)^9+(1+x)^{10}+\dots+(1+x)^{14} $ thành đa thức, ta được" + os.linesep)
		de.write(r"$ Q(x)=a_0+a_1x+\dots+a_{14}x^{14} $. Tìm hệ số $ a_9 $." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $3003 $}	{$3004 $}	{$3005 $}	{$3006 $}" + os.linesep)
		de.write(r"\loigiai{Hệ số $ x^9 $ trong các đa thức $ (1+x)^9, (1+x)^{10}, \dots, (1+x)^{14}$ lần lượt là: "+ os.linesep)
		de.write(r"$ \mathrm{C}_9^9, \mathrm{C}_{10}^9,\dots,\mathrm{C}_{14}^9 $. Do đó: "+ os.linesep)
		de.write(r"$ a_9= \mathrm{C}_9^9+ \mathrm{C}_{10}^9+\dots+\mathrm{C}_{14}^9=3003$.}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K3_12():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		a = np.randint(2,7)
		n = np.randint(7,15)
		k = np.randint(3,n-2)
		C = dc.NT_Newton_list(1,-a*x,n)[k]
		z = n
		Z = [z,z+1,z-1,z+2]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Biết hệ số của $x^{%s}$ trong khai triển $(1-%s x)^n$ là $%s$. Tìm $n$." %(k,a,C) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K3_13():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính hệ số của $x^3$ trong khai triển $(x+1)^5+(x-2)^7$." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $570$}	{$-622$}	{$10$}	{$560$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12K3_13():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển biểu thức $P(x)=(x+1)^{2n}$ đến số hạng đứng giữa theo lũy thừa giảm dần của $x$. " + os.linesep)
		de.write(r"	Tổng hệ số của các số hạng ghi được là" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$2^{2n-1}$}	{$\dfrac{2^{2n}-\mathrm{C}_{2n}^n}{2}$}	{$2^{2n-2}$}	{\True $\dfrac{2^{2n}+\mathrm{C}_{2n}^n}{2}$}" + os.linesep)
		de.write(r"\loigiai{Ta có tổng hệ số các số hạng ghi được là: "+ os.linesep)
		de.write(r"	$S=\mathrm{C}_{2n}^0+\mathrm{C}_{2n}^1+\mathrm{C}_{2n}^2+\cdots+\mathrm{C}_{2n}^{n-1}+\mathrm{C}_{2n}^n$\\"+ os.linesep)
		de.write(r"Mà ta có $\mathrm{C}_{2n}^0+\mathrm{C}_{2n}^1+\mathrm{C}_{2n}^2+\cdots+\mathrm{C}_{2n}^{n-1}"+ os.linesep)
		de.write(r"+\mathrm{C}_{2n}^n+\mathrm{C}_{2n}^{n+1}+\cdots+\mathrm{C}_{2n}^{2n}=2^{2n}$\\"+ os.linesep)
		de.write(r"$\Leftrightarrow2\left(\mathrm{C}_{2n}^0+\mathrm{C}_{2n}^1+\mathrm{C}_{2n}^2+\cdots"+ os.linesep)
		de.write(r"+\mathrm{C}_{2n}^{n-1}\right)+\mathrm{C}_{2n}^n=2^{2n}\Leftrightarrow\mathrm{C}_{2n}^0+"+ os.linesep)
		de.write(r"\mathrm{C}_{2n}^1+\mathrm{C}_{2n}^2+\cdots+\mathrm{C}_{2n}^{n-1}=\dfrac{2^{2n}-\mathrm{C}_{2n}^n}{2}\\"+ os.linesep)
		de.write(r"\Rightarrow S=\dfrac{2^{2n}-\mathrm{C}_{2n}^n}{2}+\mathrm{C}_{2n}^n=\dfrac{2^{2n}+\mathrm{C}_{2n}^n}{2}$}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B3_14():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(2,5)
		n = np.randint(4,6)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển nhị thức $P(x)=(%s x-1)^{%s}$ theo lũy thừa tăng dần của $x$." %(a,n) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.NT_Newton(a*x,-1,n)) + os.linesep)
		de.write(r"{$%s$}" %(dc.NT_Newton(a*x,-1,n)) + os.linesep)
		de.write(r"{$%s$}" %(dc.NT_Newton(-a*x,-1,n)) + os.linesep)
		de.write(r"{$%s$}" %(dc.NT_Newton(-a*x,1,n)) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B3_14_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		n = Symbol('n')
		k = np.randint(2,5)
		z = n-k + 1
		Z = [n-k + 1,n-k,n-k-1,n-k+2]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển $(a+b)^n$, ($n \ge 5$) theo lũy thừa giảm dần của $b$ đến số hạng chứa $a^{n-%s}$ thì ta được bao nhiêu số hạng?" %(k) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B3_15():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(-9,9)
		b = np.randint(2015,2025)
		n = np.randint(10,21)
		fx = a*x + b*y
		z = n+1
		Z = [z,n,n+2,n-1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển $(%s)^{%s}$ có tất cả bao nhiêu số hạng?" %(latex(fx), n) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12G3_16():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		m = np.randint(15,20)
		n = 2*m+1
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng $S = \mathrm{C}_{%s}^3+2^2\mathrm{C}_{%s}^5+\cdots+2^{%s}\mathrm{C}_{%s}^{%s}+2^{%s}\mathrm{C}_{%s}^{%s}.$" 
			%(n,n,n-5,n,n-2,n-3,n,n) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\dfrac{3^{%s} - %s}{16}$}" %(n,2*n-1) + os.linesep)
		de.write(r"{$\dfrac{3^{%s} - %s}{16}$}" %(n,2*2*n+1) + os.linesep)
		de.write(r"{$\dfrac{3^{%s} - 1}{16}$}" %(n) + os.linesep)
		de.write(r"{\True $\dfrac{3^{%s} - %s}{16}$}" %(n,2*2*n-1) + os.linesep)
		de.write(r"\loigiai{$S = \mathrm{C}_{%s}^3+2^2\mathrm{C}_{%s}^5+\cdots+2^{%s}\mathrm{C}_{%s}^{%s}+2^{%s}\mathrm{C}_{%s}^{%s}$\\"
			%(n,n,n-5,n,n-2,n-3,n,n) + os.linesep)
		de.write(r" $= \dfrac{1}{2^3} \left( 2^3\mathrm{C}_{%s}^3+2^5\mathrm{C}_{%s}^5+\cdots+2^{%s}\mathrm{C}_{%s}^{%s}+2^{%s}\mathrm{C}_{%s}^{%s} \right)$\\"
			%(n,n,n-2,n,n-2,n,n,n) + os.linesep)
		de.write(r" $= \dfrac{1}{2^3} \left( 2\mathrm{C}_{%s}^1 + 2^3\mathrm{C}_{%s}^3+2^5\mathrm{C}_{%s}^5+\cdots+2^{%s}\mathrm{C}_{%s}^{%s}\
			+2^{%s}\mathrm{C}_{%s}^{%s} \right) - \dfrac{2\mathrm{C}_{%s}^1}{2^3}$\\"
			%(n,n,n,n-2,n,n-2,n,n,n,n) + os.linesep)
		de.write(r" $= \dfrac{(1+2)^{%s} + (-1+2)^{%s}}{2 \cdot 2^3}  - \dfrac{2\mathrm{C}_{%s}^1}{2^3} = \dfrac{3^{%s} - %s}{16}$}"
			%(n,n,n,n,-1+2*2*n) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B3_17():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		a = np.randint(2,9)
		b = np.randint(-9,9)
		n = np.randint(2015,2026)
		fx = (a + b*x)**(n)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm số hạng không chứa $x$ trong khai triển $%s$." %(latex(fx)) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s^{%s}$}" %(a,n)+ os.linesep)
		de.write(r"{$%s^{%s}\mathrm{C}_{%s}^{%s}$}" %(a,n,n,1)+ os.linesep)
		de.write(r"{$%s^{%s}\mathrm{C}_{%s}^{%s}$}" %(a,n-1,n,1)+ os.linesep)
		de.write(r"{$%s^{%s}$}" %(a,n-1)+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12B3_18():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		m = np.randint(9,15)
		n = 2*m
		b = np.randint(-9,9)
		a = np.randint(2015,2026)
		fx = (a + b*x)**(n)
		z = m+1
		Z = [z,z+1,z-1,z+2]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong khai triển $%s$ theo số mũ tăng dần của $x$ thì số hạng đứng giữa là số hạng thứ mấy?" %(latex(fx)) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B3_15():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		n = Symbol('n')
		k = np.randint(0,3)
		z = n - k + 1
		Z = [z,, n - k, n, n - k - 1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Khai triển $(a+b)^n$ (n > %s) theo lũy thừa giảm dần của $b$ đến số hạng chứa $a^{%s}$ thì ta được bao nhiêu số hạng?" %(k,n - k) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12Y4_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Xác suất $\mathrm{P}(A)$ của biến cố $A$ được tính theo công thức nào dưới đây?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $\mathrm{P}(A)=\dfrac{ |\Omega_{A}|}{|\Omega|}$}{$\mathrm{P}(A)=\dfrac{|\Omega|}"+ os.linesep)
		de.write(r"{ |\Omega_{A}|}$}{$\mathrm{P}(A)= |\Omega_{A}|\cdot |\Omega|$}{$\mathrm{P}(A)= |\Omega_{A}|+|\Omega|$}"+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D12Y4_2():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Cho $A$ và $B$ là hai biến cố xung khắc. Khẳng định nào dưới đây đúng?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\mathrm{P}(A)=1-\mathrm{P}(B)$}{\True $\mathrm{P}(A\cup B)=\mathrm{P}(A)+\mathrm{P}(B)$}{$\mathrm{P}(A).\mathrm{P}(B)=1$}{$\mathrm{P}(A)=\mathrm{P}(B)$}"+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12Y4_3():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		dk = np.choice(['chẵn', 'lẻ'])
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Gieo một con súc sắc cân đối. Tính xác suất để số chấm trên mặt xuất hiện là số %s." %(dk) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $\dfrac{1}{2} $}{$\dfrac{1}{6}$}{$\dfrac{2}{3}$}{$ \dfrac{1}{3}$}"+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12B4_4():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		A = []
		for index in range(0,10):
			index = np.randint(0,26)
			while index in A:
				index = np.randint(0,26)
			A.append(index)

		dc.sapxep(A)
		print(dc.SoNguyenTo(A))
		print(A)
		a = len(dc.SoNguyenTo(A))
		z = Fraction(a,len(A))
		Z = [z,Fraction(a+1,len(A)),Fraction(a-1,len(A)),Fraction(a+2,len(A))]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Từ các chữ số $%s$, chọn ngẫu nhiên một số. Tính xác suất chọn được số nguyên tố." %(set(A)) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D12K4_5():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		A = np.randint(26,size=8)
		a = len(dc.SoNguyenTo(A))
		z = Fraction(a,len(A))
		Z = [z,Fraction(a+1,len(A)),Fraction(a-1,len(A)),Fraction(a+2,len(A))]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Từ cỗ bài tú lơ khơ $52$ con, rút ngẫu nhiên cùng một lúc bốn con. Tính xác suất để rút được hai con K và hai con Át." + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{ $\dfrac{6}{270725}$} { \True $\dfrac{36}{270725}$} { $\dfrac{67}{270725}$} { $\dfrac{36}{27072}$} " + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)



def D12Y_TL_1():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Cuộc cách mạng công nghiệp $4.0$ hội tụ nhiều công nghệ, trong đó cốt lõi là công nghệ thông tin. Vì vậy bạn An quyết định đi học ngôn ngữ lập trình. " + os.linesep)
		TL.write(r"Bạn An dự định chọn một trong các ngôn ngữ lập trình được nêu sau:\\" + os.linesep)
		TL.write(r"- Lập trình hướng đối tượng gồm Java, C\#, Python, Ruby, Swift, Object-C; \\" + os.linesep)
		TL.write(r"- Lập trình hướng cấu trúc gồm Pascal, C.\\" + os.linesep)
		TL.write(r"Hỏi bạn An có bao nhiêu lựa chọn?" + os.linesep)
		TL.write(r"\loigiai{Tổng số ngôn ngữ lập trình là $6+2=8$.\\"+ os.linesep)
		TL.write(r"Vậy bạn An có $8$ cách chọn.	\dotfill 0.5 điểm\\ }"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)

def D12Y_TL_2():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Một phòng thi có $24$ bộ bàn ghế để $24$ thí sinh ngồi làm bài thi, mỗi thí sinh ngồi một bàn. Hỏi có tất cả bao nhiêu cách sắp xếp các thí sinh vào phòng thi?" + os.linesep)
		TL.write(r"\loigiai{Số cách sắp xếp là $24!$.	\dotfill 0.5 điểm\\ }"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)


def D12B_TL_3():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Ở năm học $2018-2019$, bạn Hương đạt danh hiệu học sinh giỏi nên được thưởng $30$ cuốn vở. " + os.linesep)
		TL.write(r"Năm học $2019-2020$, Hương cần chuẩn bị $15$ cuốn vở để vào năm học mới. Hỏi bạn Hương muốn lựa chọn $15$ cuốn vở thì có bao nhiêu cách chọn?" + os.linesep)
		TL.write(r"\loigiai{Số cách chọn là $\mathrm{C}_{30}^{15} = 155117520$.	\dotfill 0.5 điểm\\ }"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)


def D12B_TL_4():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Khai triển $(4x-2)^{10}$ cho tới $x^2$ theo số mũ tăng dần của $x$." + os.linesep)
		TL.write(r"\loigiai{$\mathrm{C}_{10}^0 (4x)^0 \cdot (-2)^{10} + \mathrm{C}_{10}^1 (4x)^1 \cdot (-2)^{10-1} + \mathrm{C}_{10}^2 (4x)^2 \cdot (-2)^{10-2}$	\dotfill 0.25 điểm\\ "+ os.linesep)
		TL.write(r"$ = 1024 - 20480x + 184320x^2$	\dotfill 0.25 điểm\\ }"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)


def D12B_TL_5_1():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Bạn Hoàng có $5$ cuốn sách tham khảo Toán khác nhau và $3$ cuốn sách tham khảo Lý khác nhau. Hỏi:" + os.linesep)
		TL.write(r"\begin{enumerate}[a)]" + os.linesep)
		TL.write(r"\item Có tất cả bao nhiêu cách chọn nếu bạn Hoàng chọn một cuốn sách?" + os.linesep)
		TL.write(r"\item Có tất cả bao nhiêu cách chọn nếu bạn Hoàng chọn năm cuốn sách, trong đó có ba cuốn sách Toán và hai cuốn sách Lý?" + os.linesep)
		TL.write(r"\item Có bao nhiêu cách sắp xếp các cuốn sách đó lên một kệ sách dài?" + os.linesep)
		TL.write(r"\end{enumerate}" + os.linesep)
		TL.write(r"\loigiai{"+ os.linesep)
		TL.write(r"\begin{enumerate}[a)]" + os.linesep)
		TL.write(r"\item Hoàng lấy ngẫu nhiên một cuốn trong số các cuốn sách đó thì có $3+5=8$ cách. 	\dotfill 0.5 điểm\\ " + os.linesep)
		TL.write(r"\item Hoàng lấy ngẫu nhiên ba cuốn sách Toán và hai cuốn sách Lý thì có $\mathrm{C}_5^3 \times \mathrm{C}_3^2 = 30$ cách. 	\dotfill 0.5 điểm\\ " + os.linesep)
		TL.write(r"\item Số cách sắp xếp các cuốn sách đó lên một kệ sách dài là $8! = 40320$. 	\dotfill 0.5 điểm\\ " + os.linesep)
		TL.write(r"\end{enumerate}}" + os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)



def D12B_TL_5_2():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Bạn Hoàng có $6$ cuốn sách tham khảo Toán khác nhau và $3$ cuốn sách tham khảo Lý khác nhau. Hỏi" + os.linesep)
		TL.write(r"\begin{enumerate}[a)]" + os.linesep)
		TL.write(r"\item Có tất cả bao nhiêu cách chọn nếu bạn Hoàng chọn một cuốn sách?" + os.linesep)
		TL.write(r"\item Có tất cả bao nhiêu cách chọn nếu bạn Hoàng chọn năm cuốn sách, trong đó có ba cuốn sách Toán và hai cuốn sách Lý?" + os.linesep)
		TL.write(r"\item Có bao nhiêu cách sắp xếp các cuốn sách đó lên một kệ sách dài?" + os.linesep)
		TL.write(r"\end{enumerate}" + os.linesep)
		TL.write(r"\loigiai{"+ os.linesep)
		TL.write(r"\begin{enumerate}[a)]" + os.linesep)
		TL.write(r"\item Hoàng lấy ngẫu nhiên một cuốn trong số các cuốn sách đó thì có $3+6=9$ cách. 	\dotfill 0.5 điểm\\ " + os.linesep)
		TL.write(r"\item Hoàng lấy ngẫu nhiên ba cuốn sách Toán và hai cuốn sách Lý thì có $\mathrm{C}_6^3 \times \mathrm{C}_3^2 = 60$ cách. 	\dotfill 0.5 điểm\\ " + os.linesep)
		TL.write(r"\item Số cách sắp xếp các cuốn sách đó lên một kệ sách dài là $9! = 362880$. 	\dotfill 0.5 điểm\\ " + os.linesep)
		TL.write(r"\end{enumerate}}" + os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)


#11	Nhận biết: Hoán vị (Đ/n, T/c, công thức,…)
#D12Y2_18(0)
#12	Nhận biết: Chỉnh hợp, Tổ hợp (Đ/n, T/c, công thức,…)
#13	Nhận biết: Nhị thức Niu tơn (Đ/n, T/c, công thức khai triển đơn giản,…)
D12B3_15()
#14	Nhận biết: Xác suất (Đ/n, T/c, công thức, bài tập đơn giản,….)
#15	Thông hiểu: Hai qui tắc đếm hoặc phối hợp hai quy tắc đếm
#D12Y1_4()
#16	Thông hiểu: Hoán vị, chỉnh hợp, tổ hợp
#xong
#17	Thông hiểu: Xác suất
#D12B4_4()
#18	Vận dụng: Nhị thức Niutơn
#19	Vận dụng : Chỉnh hợp, tổ hợp
#20	Vận dụng cao: Xác suất/ Hoán vị/ chỉnh hợp/ tổ hợp
