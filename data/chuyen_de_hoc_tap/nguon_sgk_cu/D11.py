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



def D11B1_1(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
	    x = Symbol('x')
	    if condition == 0:
	    	dau = ['-', '+']
	    	gtlg_ = '\cot'
	    else:
	    	dau = ['+', '-']
	    	gtlg_ = '\\tan'
	    gtlg = ['\sin', '\cos']
	    de.write(r"\begin{ex}"+ os.linesep)
	    de.write(r"Trong các hàm số sau, hàm số nào có tập xác định là $\mathbb{R}$?"+ os.linesep)
	    de.write(r"\choice"+ os.linesep)
	    de.write(r"{$ %s \dfrac{1}{x} $}" %(gtlg[0])+ os.linesep)
	    de.write(r"{$ %s (x - 2019)$}" %(gtlg_)+ os.linesep)
	    if condition == 0:
	    	de.write(r"{$ %s \sqrt{x^2 %s %s} $}" %(gtlg[0], dau[0], np.choice([2,3]))+ os.linesep)
	    	de.write(r"{\True $ %s \dfrac{1}{x^2 %s %s} $}" %(gtlg[1], dau[1], np.choice([2,3])) + os.linesep )
	    else:
	    	de.write(r"{\True $ %s \sqrt{x^2 %s %s} $}" %(gtlg[0], dau[0], np.choice([2,3]))+ os.linesep )
	    	de.write(r"{$ %s \dfrac{1}{x^2 %s %s} $}" %(gtlg[1], dau[1], np.choice([2,3]))+  os.linesep)
	    de.write(r"\loigiai{}"+ os.linesep)
	    de.write(r"\dotlineEX{10}"+ os.linesep)
	    de.write(r"\end{ex}"+ os.linesep)


def D11B1_2(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
	    x = Symbol('x')
	    k = Symbol('k')
	    m = np.choice([2,3])
	    if condition == 0:
	    	gtlg = r'\tan'
	    	z = pi/2 + k * pi
	    else:
	    	gtlg = '\cot'
	    	z = k * pi
	    de.write(r"\begin{ex}"+ os.linesep)
	    de.write(r"Tìm tập xác định $\mathscr D$ của hàm số $y=%s \dfrac{x}{%s}$." %(gtlg, m) + os.linesep )
	    de.write(r"\choice"+ os.linesep)
	    de.write(r"{$\mathscr D = \mathbb{R} \setminus \left\{ %s \right\}$}" %(latex( z )) +  os.linesep )
	    de.write(r"{\True $\mathscr D = \mathbb{R} \setminus \left\{ %s \right\}$}" %(latex( m*z ) ) + os.linesep )
	    de.write(r"{$\mathscr D = \mathbb{R} \setminus \left\{ %s \right\}$}" %(latex( z/m ))  + os.linesep )
	    de.write(r"{$\mathscr D = \mathbb{R} \setminus \left\{ %s \right\}$}" %(latex( m ))  + os.linesep )
	    de.write(r"\loigiai{}"+ os.linesep)
	    de.write(r"\dotlineEX{10}"+ os.linesep)
	    de.write(r"\end{ex}"+ os.linesep)

def D11B1_3(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		dau = np.choice(['dương', 'âm'])
		z = pi/4
		m = pi/2
		Z = [(z,z+m), (z+m,z+2*m), (z-m,z), (z-2*m,z-m)]
		if condition == 0:
			gtlg = '\sin'
			if dau == 'dương':
				nghiem = Z[0]
			else:
				nghiem = Z[3]
			Z.remove(nghiem)
		else:
			gtlg = '\cos'
			if dau == 'dương':
				nghiem = Z[2]
			else:
				nghiem = Z[1]
			Z.remove(nghiem)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Hàm số $y = %s x$ nhận giá trị %s với mọi $x$ thuộc khoảng nào trong các khoảng sau?" %(gtlg, dau) + os.linesep )
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s$}" %(latex((nghiem))) + os.linesep )
		de.write(r"{$%s$}" %(latex((Z[0]))) + os.linesep )
		de.write(r"{$%s$}" %(latex((Z[1]))) + os.linesep )
		de.write(r"{$%s$}" %(latex((Z[2]))) + os.linesep )
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B1_4(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = ['\\tan', '\cot', '\sin']
		choice1 = np.choice(gtlg)
		gtlg.remove(choice1)
		choice2 = np.choice(gtlg)
		gtlg.remove(choice2)
		if condition == 0:
			dk = 'chẵn'
		else:
			dk = 'lẻ'
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các hàm số sau, hàm số nào là hàm số %s?" %(dk) + os.linesep )
		de.write(r"\choice"+ os.linesep)
		if condition == 0:
			de.write(r"{\True $y = x %s x$}" %(choice1) + os.linesep ) ### chẵn
			de.write(r"{$y = x^2 %s x + x$}" %(choice2) + os.linesep )  ### lẻ
			de.write(r"{$y = %s$}" %(latex((cos(2*x))/x))+ os.linesep)  ### lẻ
			de.write(r"{$y = | %s 3x | + x$}" %(gtlg[0])+ os.linesep) ### không chẵn không lẻ
		else: 
			de.write(r"{$y = x %s x$}" %(choice1) + os.linesep ) ### chẵn
			de.write(r"{$y = x^2 %s x + 1$}" %(choice2) + os.linesep )  ### không chẵn không lẻ
			de.write(r"{\True $y = %s$}" %(latex((cos(2*x))/x))+ os.linesep)  ### lẻ
			de.write(r"{$y = | %s 3x | + 1$}" %(gtlg[0]) + os.linesep ) ## chẵn
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11K1_5(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = ['sin', 'cos']
		dk = np.choice(['nhỏ', 'lớn'])
		alpha = pi/6
		k = np.randint(1,3)
		l = np.randint(4,6)
		t = np.randint(2,6)
		if dk == 'lớn':
			symbol = 'M'
			a = -alpha*k
			b = alpha*l
			z = 1
		else:
			symbol = 'm'
			a = alpha*l
			b = alpha*(12-k)
			z = -1
		doan = [a,b]
		if condition == 0:
			gtlg = 'sin'
			Z = [sin(a), sin(b), -1, 1]
		else:
			gtlg = 'cos'
			Z = [cos(a), cos(b), -1, 1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm giá trị %s nhất $%s$ của hàm số $y = \%s %s x$ trên đoạn $%s$." %(dk, symbol, gtlg, t,
			latex(doan))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s = %s$}" %(symbol, latex(dc.check(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s = %s$}" %(symbol, latex(dc.check(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s = %s$}" %(symbol, latex(dc.check(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $%s = %s$}" %(symbol, latex(dc.check(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11G1_6():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		A = np.choice([-3,-2,2,3])
		B = np.randint(-3,3)
		while B == 0:
			B = np.randint(-3,3)
		while abs(A)+B <= 0 or -abs(A)+B >= 0:
			A = np.choice([-3,-2,2,3])
			B = np.randint(-3,3)
			while B == 0:
				B = np.randint(-3,3)
		alpha = np.choice([pi/2,pi/3,pi/4,pi/6,2*pi/3,3*pi/4,5*pi/6,-pi/2,-pi/3,-pi/4,-pi/6,-2*pi/3,-3*pi/4,-5*pi/6])
		if alpha > 0:
			ppi = r'\left[ 0; \pi \right]'
		else:
			ppi = r'\left[ -\pi ; 0 \right]'
		fx = A*sin(x+alpha)+B
		y_min = -abs(A)+B
		y_max = abs(A)+B
		x_minn = solve(fx-y_min)
		x_minn.append(x_minn[0]+2*pi)
		x_minn.append(x_minn[0]-2*pi)
		### lấy 2 nghiệm gần trục tung nhất của x_min
		ABS = []
		for i in set(x_minn):
			ABS.append(abs(i))
		ABS.sort()
		x_min = []
		while len(x_min) <= 1:
			for i in [ABS[0],ABS[1]]:
				if i in x_minn and i not in x_min:
					x_min.append(i)
				else:
					pass
				if -i in x_minn and -i not in x_min:
					x_min.append(-i)
				else:
					pass
		x_min.sort()

		### lấy x_max
		x_max = (x_min[0]+x_min[1])/2

		S = A+B-(3*alpha)/pi
		z = S
		Z = [z, z + pi, z - pi, z + pi/2]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"\immini{Đường cong trong hình dưới mô tả đồ thị của hàm số \
			$y=A\sin(x+\alpha)+B$ ($A, B, \alpha$ là các hằng số, $\alpha\in[-\pi;0]$).\
			Tính $S=A+B-\dfrac{3\alpha}{\pi}.$"+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$S = %s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$S = %s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$S = %s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $S = %s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"	}{\
			\begin{tikzpicture}[thick,>=stealth,scale=.6]\
				\def\A{%s} \def\B{%s} \def\alpha{%s}\
				\draw[->](%s,0) --(%s,0)node[above]{$%s$} --(0,0) node[below left]{$O$}--(%s,0) node[below]{$%s$}--(%s,0) node[above]{$%s$}-- (%s,0) node[above]{$x$};\
				\draw[-][dashed](%s,0)--(%s,%s)--(0,%s) node[below left]{$%s$}--(%s,%s)--(%s,0);\
				\draw[-][dashed](%s,0)--(%s,%s)--(0,%s) node[left]{$%s$};\
				\draw[->](0,%s) -- (0, %s) node[right]{$y$};\
				\draw[smooth, domain=%s:%s] plot({\x}, {\A*sin((\x+\alpha) r)+\B});\
			\end{tikzpicture}\
			}"
			%(A,B,alpha,
				x_min[0]-.5, x_min[0],latex(x_min[0]), x_max, latex(x_max), x_min[1], latex(x_min[1]), x_min[1]+.5,
				x_min[0], x_min[0],y_min, y_min, latex(y_min),x_min[1],y_min,x_min[1],
				x_max,x_max, y_max, y_max, latex(y_max),
				y_min-.5,y_max+.5,
				x_min[0]-.5, x_min[1]+.5)+ os.linesep)
		de.write(r"\loigiai{GTLN và GTNN của hàm số lần lượt là $|A|+B$ và $-|A|+B$. Kết hợp với đồ thị đã cho, \
			ta suy ra $|A|=%s, B=%s$. Hơn nữa, GTLN của hàm số đạt tại $x=%s$ nên \
			$\sin\left(%s+\alpha\right)=\pm 1,$ mà $\alpha\in %s$ nên ta suy ra \
			$\sin\left(%s+\alpha\right)=-1$ và $\alpha= %s$. Vậy $S=%s$.}"
			%(abs(A),B, latex(x_max),latex(x_max), ppi, latex(x_max), latex(alpha), latex(S)) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11K1_7():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([tan(x), cot(x), sin(x), cos(x)])
		truc = np.choice(['hoành', 'tung'])
		dvi = np.choice([pi, pi/2, pi/3, pi/4, pi/6, 2*pi/3, 3*pi/4, 5*pi/6])
		fx = gtlg
		if truc == 'hoành':
			n = 0
			phia = np.choice(['về phía bên phải', 'về phía bên trái'])
			if phia == 'về phía bên phải':
				m = - dvi
			else:
				m = dvi
		else:
			m = 0
			phia = np.choice(['lên trên', 'xuống dưới'])
			if phia == 'lên trên':
				n = dvi
			else:
				n = - dvi
		if fx == tan(x):
			gx = tan(x + m) + n
			g_sai1 = tan(x + n) + m
			g_sai2 = tan(x - m) -n
			g_sai3 = tan(x - n) - m
		elif fx == cot(x):
			gx = cot(x + m) + n
			g_sai1 = cot(x + n) + m
			g_sai2 = cot(x - m) -n
			g_sai3 = cot(x - n) - m
		elif fx == sin(x):
			gx = sin(x + m) + n
			g_sai1 = sin(x + n) + m
			g_sai2 = sin(x - m) -n
			g_sai3 = sin(x - n) - m
		else:
			gx = cos(x + m) + n
			g_sai1 = cos(x + n) + m
			g_sai2 = cos(x - m) -n
			g_sai3 = cos(x - n) - m

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tịnh tiến đồ thị hàm số  $y=%s$ theo phương song song trục %s %s $%s$ đơn vị thì được đồ thị của hàm số nào trong các hàm số cho dưới đây?" 
			%(latex(fx), truc, phia, latex(dvi))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $y = %s$}" %(latex(gx))+ os.linesep)
		de.write(r"{$y = %s$}" %(latex(g_sai1))+ os.linesep)
		de.write(r"{$y = %s$}" %(latex(g_sai2))+ os.linesep)
		de.write(r"{$y = %s$}" %(latex(g_sai3))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B1_8():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice(['sin', 'cos', '-sin', '-cos'])
		gtlg_doi = {'sin': 'cos', 'cos': 'sin', '-cos': '-sin', '-sin': '-cos'}

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Đồ thị sau là đồ thị của hàm số nào trong các hàm số dưới đây?" + os.linesep)
		de.write(r"\begin{center}\
			\definecolor{cqcqcq}{rgb}{0.75,0.75,0.75}\
			\begin{tikzpicture}[line cap=round,line join=round,>=stealth,x=1.0cm,y=1.0cm]\
			\draw [color=cqcqcq,, xstep=3.14cm,ystep=1.0cm] (-1.36,-1.24) grid (13.62,1.3);\
			\draw[->] (-1.36,0.) -- (13.62,0.);\
			\draw[shift={(3.14,0)}] (0pt,2pt) -- (0pt,-2pt) node[below right] {\footnotesize $\pi$};\
			\draw[shift={(6.28,0)}] (0pt,2pt) -- (0pt,-2pt) node[below right] {\footnotesize $2\pi$};\
			\draw[shift={(9.42,0)}] (0pt,2pt) -- (0pt,-2pt) node[below right] {\footnotesize $3\pi$};\
			\draw[shift={(12.56,0)}] (0pt,2pt) -- (0pt,-2pt) node[below left] {\footnotesize $4\pi$};\
			\draw (13.3,0.08) node [above right] { $x$};\
			\draw[->] (0.,-1.24) -- (0.,1.3);\
			\foreach \y in {-1,1}\
			\draw[shift={(0,\y)}] (2pt,0pt) -- (-2pt,0pt) node[below left] {\footnotesize $\y$};\
			\draw (0.1,0.86) node [above right] { $y$};\
			\draw (0pt,-10pt) node[left] {\footnotesize $O$};\
			\clip(-1.36,-1.24) rectangle (13.62,1.3);\
			\draw[line width=1.2pt,smooth,samples=100,domain=-1.36:13.62] plot(\x,{0+ %s (((\x)/2.0)*180/pi)});\
			\end{tikzpicture}\
			\end{center}" 
			%(gtlg) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $y = \%s \dfrac{x}{2}$}" %(gtlg)+ os.linesep)
		de.write(r"{$y = \%s x$}" %(gtlg)+ os.linesep)
		de.write(r"{$y = \%s \dfrac{x}{2}$}" %(gtlg_doi[gtlg])+ os.linesep)
		de.write(r"{$y = \%s 2x$}" %(gtlg)+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B1_9():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		GTLG = [r'\sin 2x', r'\cos 2x', r'-\sin 2x', r'-\cos 2x']
		gtlg = np.choice(GTLG)
		de.write(r"\begin{ex}"+ os.linesep)
		if gtlg == r'\cos 2x' or gtlg == r'\cos 2x':
			de.write(r"\immini{Bảng biến thiên ở hình bên là của hàm số nào dưới đây, xét trên đoạn $[0;\pi]$?" + os.linesep)
		else:
			de.write(r"\immini{Bảng biến thiên ở hình bên là của hàm số nào dưới đây, xét trên đoạn $\left[\dfrac{\pi}{4};\dfrac{5\pi}{4} \right]$?" + os.linesep)

		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $y = %s $}" %(gtlg) + os.linesep)
		GTLG.remove(gtlg)
		de.write(r"{$y = %s $}" %(GTLG[0])+ os.linesep)
		de.write(r"{$y = %s $}" %(GTLG[1])+ os.linesep)
		de.write(r"{$y = %s $}" %(GTLG[2])+ os.linesep)
		de.write(r"}{" + os.linesep)
		if gtlg == r'\cos 2x':
			de.write(r"\begin{tikzpicture}\tkzTabInit[lgt=1.0,espcl=3.0]{$x$  /1, $y$  /2.2}{$0$ , $\dfrac{\pi}{2}$, $\pi$}\tkzTabVar{-/$-1$ ,+/$1$, -/$-1$}\end{tikzpicture}" + os.linesep)
		elif gtlg == r'-\cos 2x':
			de.write(r"\begin{tikzpicture}\tkzTabInit[lgt=1.0,espcl=3.0] {$x$  /1, $y$  /2.2} {$0$ , $\dfrac{\pi}{2}$, $\pi$}\tkzTabVar{+/$1$ ,-/$-1$, +/$1$}\end{tikzpicture}"  + os.linesep)
		elif gtlg == r'\sin 2x':
			de.write(r"\begin{tikzpicture} \tkzTabInit[lgt=1.0,espcl=3.0] {$x$  /1, $y$  /2.2} {$\dfrac{\pi}{4}$, $\dfrac{3\pi}{4}$, $\dfrac{5\pi}{4}$} \tkzTabVar{+/$1$ ,-/$-1$, +/$1$} \end{tikzpicture}"  + os.linesep)
		else:
			de.write(r"\begin{tikzpicture} \tkzTabInit[lgt=1.0,espcl=3.0] {$x$  /1, $y$  /2.2} {$\dfrac{\pi}{4}$, $\dfrac{3\pi}{4}$, $\dfrac{5\pi}{4}$} \tkzTabVar{-/$-1$ ,+/$+1$, -/$-1$} \end{tikzpicture}"  + os.linesep)
		de.write(r"}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y1_10():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice(['sin', 'cos'])
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tập xác định $\mathscr D$ của hàm số $y= \%s \sqrt{x}$." %(gtlg) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\mathscr D = \mathbb{R}$}" + os.linesep)
		de.write(r"{$\mathscr D = \mathbb{R} \setminus \{0\}$}" + os.linesep)
		de.write(r"{\True $\mathscr D = [0;+\infty)$}" + os.linesep)
		de.write(r"{$\mathscr D = (0;+\infty)$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y1_11():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice(['sin', 'cos'])
		m = np.randint(1,9)
		n = np.randint(1,4)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tập xác định $\mathscr D$ của hàm số $y= \%s \dfrac{%s}{x^2- %s}$." %(gtlg, m, latex(n**2)) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\mathscr D = \mathbb{R}$}" + os.linesep)
		de.write(r"{$\mathscr D = \mathbb{R} \setminus \{ %s \}$}" %(latex(n**2)) + os.linesep)
		de.write(r"{$\mathscr D = \mathbb{R} \setminus \{ %s ; %s \}$}" %(latex(-n**2), latex(n**2)) + os.linesep)
		de.write(r"{\True $\mathscr D = \mathbb{R} \setminus \{ %s ; %s \}$}" %(latex(-n), latex(n)) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y1_12():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		m = np.randint(1,9)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các hàm số sau, hàm số nào là hàm số chẵn?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $y = \cos %s x$}" %(m) + os.linesep)
		de.write(r"{$y = \sin %s x$}" %(m) + os.linesep)
		de.write(r"{$y = \tan %s x$}" %(m) + os.linesep)
		de.write(r"{$y = \cot %s x$}" %(m) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B1_13():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg1 = np.choice(['cot', 'tan'])
		gtlg2 = {'cot': 'sin', 'tan': 'cos'}
		don_dieu = {'cot': 'nghịch', 'tan': 'đồng'}
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Hàm số $y=\%s x$ và hàm số $y=\%s x$ cùng %s biến trên khoảng nào dưới đây?" %(gtlg1, gtlg2[gtlg1], don_dieu[gtlg1]) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$\left(0;\dfrac{\pi}{2}\right)$}" + os.linesep)
		if gtlg1 == 'cot':
			de.write(r"{$\left(\dfrac{3\pi}{2};2\pi\right)$}" + os.linesep)
			de.write(r"{$\left(\dfrac{\pi}{2};\dfrac{3\pi}{2}\right)$}" + os.linesep)
			de.write(r"{\True $\left(\pi;\dfrac{3\pi}{2}\right)$}" + os.linesep)
		else:
			de.write(r"{$\left(\dfrac{\pi}{2} ; \pi\right)$}" + os.linesep)
			de.write(r"{$\left(-\pi;0\right)$}" + os.linesep)
			de.write(r"{\True $\left(\dfrac{3\pi}{2};2\pi\right)$}" + os.linesep)
		de.write(r"\loigiai{Lưu ý về khoảng đi qua giá trị không xác định của hàm $%s$.}" %(gtlg1) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y1_14():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice(['cot', 'tan'])
		don_dieu = {'cot': 'nghịch', 'tan': 'đồng'}
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Hàm số $y=\%s x$ %s biến trong khoảng nào sau đây?" %(gtlg, don_dieu[gtlg]) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		if gtlg == 'cot':
			de.write(r"{$\left(-\pi ;\pi \right)$}" + os.linesep)
			de.write(r"{\True $\left(0 ;\pi \right)$}" + os.linesep)
			de.write(r"{$\left(-\dfrac{\pi}{2} ;\dfrac{\pi}{2} \right)$}" + os.linesep)
			de.write(r"{$\left(0 ;2\pi \right)$}" + os.linesep)
		else:
			de.write(r"{\True $\left(0 ;\dfrac{\pi}{2} \right)$}" + os.linesep)
			de.write(r"{$\left(0 ;\pi \right)$}" + os.linesep)
			de.write(r"{$\left(0 ;4\pi \right)$}" + os.linesep)
			de.write(r"{$\left(0 ;2\pi\right)$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y1_15():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice(['cot', 'tan', 'sin', 'cos'])
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Gọi $T$ là chu kỳ tuần hoàn của hàm số $y=\%s x$. Tìm $T$." %(gtlg) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		if gtlg == 'sin' or gtlg == 'cos':
			de.write(r"{$\pi$}" + os.linesep)
			de.write(r"{\True $2\pi$}" + os.linesep)
			de.write(r"{$4\pi$}" + os.linesep)
			de.write(r"{$k2\pi$}" + os.linesep)
		else:
			de.write(r"{\True $\pi$}" + os.linesep)
			de.write(r"{$2\pi$}" + os.linesep)
			de.write(r"{$\dfrac{\pi}{2}$}" + os.linesep)
			de.write(r"{$k\pi$}" + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B1_16():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([sin, cos])
		m = np.randint(1,9)
		while m == 0:
			m = np.randint(1,9)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tập giá trị của hàm số $y=%s-|\%s x|$" %(m,gtlg) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$T = \left[ %s ; %s \right]$}" %(latex(m-1), latex(m+1)) + os.linesep)
		de.write(r"{$T = \left[ %s ; %s \right]$}" %(latex(-1), latex(1)) + os.linesep)
		de.write(r"{\True $T = \left[ %s ; %s \right]$}" %(latex(m - 1), latex(m)) + os.linesep)
		de.write(r"{$T = \left[ %s ; %s \right]$}" %(latex(m), latex(m+1)) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B1_17():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([sin, cos])
		n = np.randint(1,9)
		m = np.randint(-9,9)
		while m == 0:
			m = np.randint(1,9)
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tập giá trị của hàm số $y=%s$." %(latex(n* gtlg(x) + m)) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$T = \left[ %s ; %s \right]$}" %(latex(-n + m), latex(-n + m)) + os.linesep)
		de.write(r"{$T = \left[ %s ; %s \right]$}" %(latex(-n + m), latex(n + m)) + os.linesep)
		de.write(r"{\True $T = \left[ %s ; %s \right]$}" %(latex(-n + m), latex(n + m)) + os.linesep)
		de.write(r"{$T = \left[ %s ; %s \right]$}" %(latex(-n + m-1), latex(n + m+1)) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B1_18():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice(['sin', 'cos'])
		gtlg_ham = {'sin': sin, 'cos': cos}
		alpha = np.choice([pi/4, pi/3, pi/2, -pi/4, -pi/3, -pi/2])
		fx = gtlg_ham[gtlg](x + alpha) + 1
		nghiem = solve(fx,x)
		while 0 in nghiem:
			alpha = np.choice([pi/4, pi/3, pi/2, -pi/4, -pi/3, -pi/2])
			fx = gtlg_ham[gtlg](x + alpha) + 1
			nghiem = solve(fx,x)
		while len(nghiem) < 2:
			nghiem.append(nghiem[0]-2*pi)
		nghiem.sort()
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"\immini{Đồ thị trong hình vẽ là của hàm số nào sau đây?" + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$y = 2\%s x$}" %(gtlg) + os.linesep)
		de.write(r"{$y = 1 + \%s x$}" %(gtlg) + os.linesep)
		de.write(r"{\True $y = 1 + \%s \left( %s \right)$}" %(gtlg, latex(x + alpha)) + os.linesep)
		de.write(r"{$y = 1 + \%s \left( %s \right)$}" %(gtlg, latex(x - alpha)) + os.linesep)
		de.write(r"}{"+ os.linesep)
		if (nghiem[0]+nghiem[1])/2 == 0:
			de.write(r"\begin{tikzpicture}[thick,>=stealth,x=1cm,y=1cm,scale=0.7]"+ os.linesep)
		else:
			de.write(r"\begin{tikzpicture}[thick,>=stealth,x=1cm,y=1cm,scale=0.7] \
					\draw [fill=white,draw=black] (0,0) circle (1pt)node[below left] {\footnotesize $O$};"+ os.linesep)
		de.write(r"\draw[->] (%s,0) -- (%s,0) node[below] {\small $x$};\
			\draw[->] (0,-1.4) -- (0,3) node[right] {\small $y$};\
			\draw[thick,smooth,samples=100,domain=%s:%s] plot(\x,{1+%s(((\x+%s))*180/pi)});\
			\draw[dashed] (%s,0)--(%s,2)--(0,2)node[above right]{$2$};\
			\draw[fill=black] (%s,0)node[below right]{$%s$} circle(0.04);\
			\draw[fill=black] (%s,0)node[below left]{$%s$} circle(0.04);\
			\draw[fill=black] (%s,0)node[below right]{$%s$} circle(0.04);\
			\end{tikzpicture}}"
			%(nghiem[0]-pi-.5, nghiem[1]+pi+.5,
				nghiem[0]-pi, nghiem[1]+pi, gtlg, alpha,
				(nghiem[0]+nghiem[1])/2,(nghiem[0]+nghiem[1])/2,
				nghiem[1],latex(nghiem[1]),
				nghiem[0], latex(nghiem[0]),
				(nghiem[0]+nghiem[1])/2, latex((nghiem[0]+nghiem[1])/2)) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)



def D11K1_19():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([sin, cos])
		a = np.randint(-9,9)
		b = np.randint(-9,9)
		c = np.randint(-9,9)
		while a == 0:
			a = np.randint(-9,9)
		fx = lambda x: a*(x)**2 + b*(x) + c
		while (-20<fx(-1) and fx(-1)<=20) or (-20<fx(1) and fx(1)<=20):
			b = np.randint(-9,9)
			c = np.randint(-20,20)
			fx = lambda x: a*(x)**2 + b*(x) + c
		dk = np.choice(['nhỏ', 'lớn'])
		ki_hieu = {'nhỏ': 'm', 'lớn': 'M'}
		if -1 < dc.Dinh(a,b,c)[0] < 1:
			S = [fx(-1), fx(1), dc.DinhHBH(a,b,c)[1]]
		else:
			S = [fx(-1), fx(1)]
		S.sort()
		if dk == 'nhỏ':
			z = S[0]
		else:
			z = S[len(S)-1]
		sai1 = dc.DinhHBH(a,b,c)[0]
		sai2 = dc.DinhHBH(a,b,c)[1]
		if -1 < dc.Dinh(a,b,c)[0] < 1:
			S.append(sai1)
		else:
			S.append(sai1)
			S.append(sai2)
		Z = S
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm giá trị %s nhất $%s$ của hàm số $y=%s $." %(dk, ki_hieu[dk], latex(a*(gtlg(x))**2 + b*(gtlg(x)) + c)) + os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $%s = %s$}" %(ki_hieu[dk], dc.check(z,Z)[0]) + os.linesep)
		de.write(r"{$%s = %s$}" %(ki_hieu[dk], dc.check(z,Z)[1]) + os.linesep)
		de.write(r"{$%s = %s$}" %(ki_hieu[dk], dc.check(z,Z)[2]) + os.linesep)
		de.write(r"{$%s = %s$}" %(ki_hieu[dk], dc.check(z,Z)[3]) + os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)




def D11G2_1(condition,k):### k là số vòng chạy lấy nghiệm
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = ['sin', 'cos']
		if condition == 0:
			gtlg = 'sin'
			a = -k*pi 
		else:
			gtlg = 'cos'
			a = -(pi/2)*(2*k-1)
		b = a + 2*k*pi
		doan = [a,b]
		z = 4*k+1
		Z = [z, z-1, z - 2, z + 1]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm số nghiệm thuộc khoảng $%s$ của phương trình $\%s x+\sin2x=0$." 
			%(latex(doan), gtlg)+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		if condition == 0:
			de.write(r"\loigiai{\
		    \begin{eqnarray*}\
		        \sin{x}+\sin2x=0 \Leftrightarrow \sin x (1 + 2 \cos x) = 0\
		        \Leftrightarrow \hoac{& \sin x =0 \\ & \cos x = -\dfrac{1}{2}}\
		        \Leftrightarrow \hoac{& x = k\pi \\& x = \pm \dfrac{2 \pi}{3} + k2\pi}\
		        \end{eqnarray*}}"+ os.linesep)
		else:
			de.write(r"\loigiai{\
		    \begin{eqnarray*}\
		        \cos{x}+\sin2x=0 \Leftrightarrow \cos x (1 + 2 \sin x) = 0 \
		        \Leftrightarrow \hoac{& \cos x =0 \\ & \sin x = -\dfrac{1}{2}}\
		        \Leftrightarrow \hoac{& x = \dfrac{\pi}{2} + k\pi \\& x = - \dfrac{ \pi}{6}+k2\pi \\ \
		         & x = \dfrac{7\pi}{6} + k2\pi}\
		    \end{eqnarray*}}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11G2_2(condition,k):### k là số vòng chạy lấy nghiệm            ############################ LỖI
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([sin(x),cos(x)])
		a = -k*pi
		b = a + 2*k*pi
		doan = [a,b]
		t = np.randint(1,10)
		y = np.randint(1,10)
		de.write(r"\begin{ex}"+ os.linesep)

		### đường thẳng luôn cắt đường tròn tại hai điểm
		if condition == 0:
			if t < y:
				m = t/y
				de.write(r"Phương trình $|%s|=%s$ có bao nhiêu nghiệm trên đoạn $\left[%s;%s\right]$?" 
					%(latex(gtlg), Fraction(t,y), latex(a), latex(b))+ os.linesep)
			else:
				m = y/t
				de.write(r"Phương trình $|%s|=%s$ có bao nhiêu nghiệm trên đoạn $\left[%s;%s\right]$?" 
					%(latex(gtlg), Fraction(y,t), latex(a), latex(b))+ os.linesep)

		### đường thẳng cắt đường tròn tại một điểm
		else:
			if gtlg == sin(x):
				m = 0
			else:
				m = 1
			de.write(r"Phương trình $|%s|=%s$ có bao nhiêu nghiệm trên đoạn $\left[%s;%s\right]$?" 
				%(latex(gtlg), m, latex(a), latex(b))+ os.linesep)

		### giải phương trình lượng giác này lấy nghiệm như sau: 
		### sin(x) = sin(alpha) thì x = alpha hoặc x = pi - alpha
		### cos(x) = cos(alpha) thì x = alpha hoặc x = -alpha + 2*pi
		### vì vậy với cos(x) = 1 thì x = 0 hoặc x = 2*pi
		nghiem1 = solve(gtlg - m,x)
		nghiem2 = solve(gtlg + m,x)
		if condition == 0:
			z = (len(nghiem1) + len(nghiem2))*k
		else:
			if gtlg == cos(x):
				z = (len(nghiem1) - 1 + len(nghiem2))*k + 1 ### trừ bớt đi nghiệm trung 0 và 2*pi, sau đó cộng thêm 1 nghiệm vì đoạn xét nghiệm lấy cả 2 đầu mút
			else:
				z = (len(nghiem1) + len(nghiem2))*k + 1 ### cộng thêm 1 nghiệm vì đoạn lấy nghiệm lấy cả 2 đầu mút
		Z = [z, z-1, z - 2, z + 1]
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[1])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[2])+ os.linesep)
		de.write(r"{\True $%s$}" %(dc.check(z,Z)[0])+ os.linesep)
		de.write(r"{$%s$}" %(dc.check(z,Z)[3])+ os.linesep)
		if gtlg == sin(x):
			de.write(r"\loigiai{\immini{$|%s|= %s \Leftrightarrow \hoac{& %s = %s \\ & %s = -%s .}$\\ \
				}{ \
				\begin{tikzpicture}[>=stealth, x=1cm, y=1cm, scale=1.2]\
					\begin{scriptsize}\
					\def\xmin{-1.4} \def\xmax{1.4} \def\ymin{-1.4} \def\ymax{1.4}\
					\draw [->] (\xmin-.2, 0)--(\xmax+.2, 0) node[below]{$\cos x$};\
					\draw [->] (0, \ymin-.2)--(0, \ymax+.2) node[right]{$\sin x$};\
					\draw node [below right]{$O$};\
					\draw(0,0) circle (1cm);\
					\draw(0,0) circle (1.05cm);\
					\draw (0,%s) node [below right]{$%s$};\
					\draw (0,%s) node [below left]{$%s$};\
					\draw[ultra thick] (-1.2,%s)--(1.2,%s) (-1.2,%s)--(1.2,%s);\
					\end{scriptsize}\
				\end{tikzpicture} } }"
				%(latex(gtlg), latex(m), latex(gtlg), latex(m), latex(gtlg), latex(m),
					m, latex(m), -m, latex(-m),
					m,m,-m,-m) + os.linesep)
		else:
			de.write(r"\loigiai{\immini{$|%s|= %s \Leftrightarrow \hoac{& %s = %s \\ & %s = -%s .}$\\ \
				}{ \
				\begin{tikzpicture}[>=stealth, x=1cm, y=1cm, scale=1.2]\
					\begin{scriptsize}\
					\def\xmin{-1.4} \def\xmax{1.4} \def\ymin{-1.4} \def\ymax{1.4}\
					\draw [->] (\xmin-.2, 0)--(\xmax+.2, 0) node[below]{$\cos x$};\
					\draw [->] (0, \ymin-.2)--(0, \ymax+.2) node[right]{$\sin x$};\
					\draw node [below right]{$O$};\
					\draw(0,0) circle (1cm);\
					\draw(0,0) circle (1.05cm);\
					\draw (%s,0) node [below right]{$%s$};\
					\draw (%s,0) node [below left]{$%s$};\
					\draw[ultra thick] (%s,-1.2)--(%s,1.2) (%s,-1.2)--(%s,1.2);\
					\end{scriptsize}\
				\end{tikzpicture} } }"
				%(latex(gtlg), latex(m), latex(gtlg), latex(m), latex(gtlg), latex(m),
					m, latex(m), -m, latex(-m),
					m,m,-m,-m) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y2_3_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([sin, cos, tan])
		Alpha = [0,pi/6,pi/4,pi/3,pi/2]
		if gtlg == tan:
			Alpha.remove(pi/2)
			alpha = np.choice(Alpha)
		else:
			alpha = np.choice(Alpha)
		Alpha.remove(alpha)
		z = alpha
		Z = [z, Alpha[0], Alpha[1], Alpha[2]]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các giá trị sau, giá trị nào là nghiệm của phương trình $%s = %s$?" 
			%(latex(gtlg(x)), latex(gtlg(alpha)))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B2_3_2():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = np.choice([sin, cos, tan])
		Alpha = [0,pi/6,pi/4,pi/3,pi/2]
		if gtlg == tan:
			Alpha.remove(pi/2)
			alpha = np.choice(Alpha)
		else:
			alpha = np.choice(Alpha)
		k = np.randint(-5,5)
		while k == 0:
			k = np.randint(-5,5)
		Alpha.remove(alpha)
		z = alpha + k*2*pi
		Z = [z, Alpha[0] + k*2*pi, Alpha[1] + k*2*pi, Alpha[2] + k*2*pi]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các giá trị sau, giá trị nào là nghiệm của phương trình $%s = %s$?" 
			%(latex(gtlg(x)), latex(gtlg(alpha + k*2*pi)))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B2_3_3():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = cot
		Alpha = [pi/6,pi/4,pi/3,pi/2]
		Alpha.remove(alpha)
		z = alpha
		Z = [z, Alpha[0], Alpha[1], Alpha[2]]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các giá trị sau, giá trị nào là nghiệm của phương trình $%s = %s$?" 
			%(latex(gtlg(x)), latex(gtlg(alpha)))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B2_3_4():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		gtlg = cot
		Alpha = [pi/6,pi/4,pi/3,pi/2]
		k = np.randint(-5,5)
		while k == 0:
			k = np.randint(-5,5)
		Alpha.remove(alpha)
		z = alpha + k*2*pi
		Z = [z, Alpha[0] + k*2*pi, Alpha[1] + k*2*pi, Alpha[2] + k*2*pi]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các giá trị sau, giá trị nào là nghiệm của phương trình $%s = %s$?" 
			%(latex(gtlg(x)), latex(gtlg(alpha + k*2*pi)))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11Y2_4():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		num = []
		for i in range(0,4):
			i = np.randint(1,9)
			num.append(i)
		t = np.randint(1,9)
		dk = np.choice(['vô nghiệm', 'có nghiệm'])

		### tìm vp để phương trình có nghiệm, vô nghiệm
		have_sol = []
		no_sol = []
		for i in range(0,6):
			T = []
			m = np.randint(1,20)
			n = np.randint(1,20)
			while m == n:
				n = np.randint(1,20)
			T.append(m)
			T.append(n)
			T.sort()
			if i %2 == 0:
				have_sol.append(Fraction(T[0],T[1]))
			else:
				no_sol.append(Fraction(T[1],T[0]))
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các phương trình sau, phương trình nào %s?" %(dk)+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		if dk == 'vô nghiệm':
			de.write(r"{$\sin(x + %s) = %s$}" %(num[0], have_sol[0])+ os.linesep)
			de.write(r"{$\cos(x + %s) = %s$}" %(num[1], have_sol[1])+ os.linesep)
			de.write(r"{$\sin(x + %s) = %s$}" %(num[2], have_sol[2])+ os.linesep)
			de.write(r"{\True $\cos(x + %s) = %s$}" %(num[3], no_sol[0])+ os.linesep)
		else:
			de.write(r"{\True $\sin(x + %s) = %s$}" %(num[0], have_sol[0])+ os.linesep)
			de.write(r"{$\cos(x + %s) = %s$}" %(num[1], no_sol[1])+ os.linesep)
			de.write(r"{$\sin(x + %s) = %s$}" %(num[2], no_sol[2])+ os.linesep)
			de.write(r"{$\cos(x + %s) = %s$}" %(num[3], no_sol[0])+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B2_5():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		k = Symbol('k')
		m = np.randint(2,9)
		gtlg = np.choice([tan, cot])
		Alpha = [pi/6,pi/4,pi/3, 2*pi/3, 3*pi/4, 5*pi/6]
		alpha = np.choice(Alpha)
		Alpha.remove(alpha)

		z = (alpha)/m 
		Z = [z, (Alpha[0])/m, (Alpha[1])/m, (Alpha[2])/m]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm họ nghiệm của phương trình $%s = %s$." 
			%(latex(gtlg(m*x)), latex(gtlg(alpha)))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$x = %s + %s$}" %(latex(dc.check_radian(z,Z)[1]), latex(k*pi/m))+ os.linesep)
		de.write(r"{$x = %s + %s$}" %(latex(dc.check_radian(z,Z)[2]), latex(k*pi/m))+ os.linesep)
		de.write(r"{$x = %s + %s$}" %(latex(dc.check_radian(z,Z)[3]), latex(k*pi/m))+ os.linesep)
		de.write(r"{\True $x = %s + %s$}" %(latex(dc.check_radian(z,Z)[0]), latex(k*pi/m))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B2_6():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		k = Symbol('k')
		m = np.randint(2,9)
		gtlg = np.choice([tan, cot])
		Alpha = [pi/6,pi/4,pi/3, 2*pi/3, 3*pi/4, 5*pi/6]
		alpha = np.choice(Alpha)

		nghiem = alpha/m
		Nghiem = [nghiem]
		while nghiem < alpha/m + 2*pi:
			nghiem += pi/m
			Nghiem.append(nghiem)
		for i in Nghiem:
			if gtlg == tan:
				while cos(m*i) == 0:
					alpha = np.choice(Alpha)
			else:
				while sin(m*i) == 0:
					alpha = np.choice(Alpha)
		Alpha.remove(alpha)


		z = (alpha)/m 
		Z = [z, (Alpha[0])/m, (Alpha[1])/m, (Alpha[2])/m]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm họ nghiệm của phương trình $%s = %s$." 
			%(latex(gtlg(m*x)), latex(gtlg(alpha)))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$x = %s + %s$}" %(latex(dc.check_radian(z,Z)[1]), latex(k*pi/m))+ os.linesep)
		de.write(r"{$x = %s + %s$}" %(latex(dc.check_radian(z,Z)[0]), latex((k*2*pi)/m))+ os.linesep)
		de.write(r"{$x = %s + %s$}" %(latex(dc.check_radian(z,Z)[1]), latex((k*2*pi)/m))+ os.linesep)
		de.write(r"{\True $x = %s + %s$}" %(latex(dc.check_radian(z,Z)[0]), latex(k*pi/m))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11K2_7():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		k = Symbol('k')
		m = np.randint(2,9)
		gtlg = np.choice([sin, cos])

		### góc beta, gamma
		num = []
		for i in range(0,2):
			p = np.randint(-9,9)
			while p == 0:
				p = np.randint(-9,9)
			num.append(Fraction(1,p))
		beta = num[0]*pi
		gamma = num[1]*pi

		fx = gtlg(x+beta)
		gx = gtlg(m*x+gamma)
		nghiem = []
		if gtlg == sin:
			for k in range(-3,4):
				nghiem1 = (beta-gamma + k*2*pi)/(m-1)
				nghiem2 = (pi - gamma - beta + k*2*pi)/(m+1)
				if nghiem1 in nghiem:
					pass
				else:
					nghiem.append(nghiem1)
				if nghiem2 in nghiem:
					pass
				else:
					nghiem.append(nghiem2)
		else:
			for k in range(-3,4):
				nghiem1 = (beta-gamma + k*2*pi)/(m-1)
				nghiem2 = (- gamma - beta + k*2*pi)/(m+1)
				if nghiem1 in nghiem:
					pass
				else:
					nghiem.append(nghiem1)
				if nghiem2 in nghiem:
					pass
				else:
					nghiem.append(nghiem2)


		### tách ra tập nghiệm âm, tập nghiệm dương. trong đó tập dương xếp tăng dần, âm xếp giảm dần
		S_duong = []
		S_am = []
		S_0 = []
		for i in nghiem:
			if i > 0:
				S_duong.append(i)
			elif i < 0:
				S_am.append(i)
			else:
				S_0.append(i)
		S_duong.sort()
		S_am.sort()
		S_am.reverse()

		so_nghiem = 2
		songhiem = 'hai'
		
		### không dương lớn nhất	
		z1 = 0
		if len(S_0) != 0:
			z1 += S_0[0]
			for i in range(0,so_nghiem):
				z1 += S_am[i]
		else:
			for i in range(0,so_nghiem):
				z1 += S_am[i]

		### 	không âm nhỏ nhất
		z2 = 0
		if len(S_0) != 0:
			z2 += S_0[0]
			for i in range(0,so_nghiem):
				z2 += S_duong[i]
		else:
			for i in range(0,so_nghiem):
				z2 += S_duong[i]

		### dương nhỏ nhất
		z3 = 0
		for i in range(0,so_nghiem):
			z3 += S_duong[i]

	 	### âm lớn nhất
		z4 = 0
		for i in range(0,so_nghiem):
			z4 += S_am[i]

		dk = np.choice(['không dương lớn nhất', 'không âm nhỏ nhất', 'dương nhỏ nhất', 'âm lớn nhất'])
		if dk == 'không dương lớn nhất':
			z = z1
			Z= [z,S_am[0],z3,z-2*pi]
		elif dk == 'không âm nhỏ nhất':
			z = z2
			Z= [z,S_duong[0],z4,z+2*pi]
		elif dk == 'dương nhỏ nhất':
			z = z3
			Z= [z,S_duong[0],z1,z+2*pi]
		else:
			z = z4
			Z= [z,S_am[0],z3,z-2*pi]


		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm tổng %s nghiệm %s của phương trình $%s \left( %s \right) = %s \left( %s \right)$." 
			%(songhiem, dk, latex(gtlg), latex(x + beta), latex(gtlg), latex(m*x + gamma))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11K2_8():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		k = Symbol('k')
		gtlg = np.choice([sin, cos])
		t = np.randint(1,10)
		l = np.randint(1,10)
		while t == l:
			t = np.randint(1,10)
			l = np.randint(1,10)
		if t>l:
			m = Fraction(l,t)
		else:
			m = Fraction(t,l)

		fx = sin(2019*x) + cos(2020*x)
		gx = abs(gtlg(x)) - m

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có bao nhiêu điểm trên đường tròn lượng giác mà tại đó hàm số $y = %s$ không xác định?" 
			%(latex(fx/gx))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$1$ điểm}"+ os.linesep)
		de.write(r"{$2$ điểm}"+ os.linesep)
		de.write(r"{\True $4$ điểm}"+ os.linesep)
		de.write(r"{$3$ điểm}"+ os.linesep)
		de.write(r"\loigiai{}"+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11B3_1():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		y = Symbol('y')
		z = Symbol('z')
		a = np.choice([1,-1,sqrt(3),-sqrt(3)])
		b = np.choice([1,-1])
		VP = np.choice([sqrt(1)/2,-sqrt(1)/2,sqrt(2)/2,-sqrt(2)/2,sqrt(3)/2,-sqrt(3)/2,1,-1])
		c = VP*sqrt(a**2+b**2)

		### để tìm ra góc alpha để được cos(x - alpha) = c/sqrt(a^2+b^2)
		alpha1 = solve(sin(y)-(a/sqrt(a**2+b**2)))
		alpha2 = solve(cos(y)-(b/sqrt(a**2+b**2)))
		for i in alpha1:
			if i in alpha2:
				alpha = i
			else:
				if i + 2*pi in alpha2:
					alpha = i +2*pi
		
		### để được c/sqrt(a^2+b^2) = cos(beta)
		beta = solve(cos(z)-VP)

		nghiem = solve(cos(x - alpha) - VP)
		k = np.randint(-3,3)
		z = nghiem[0] + 2*k*pi
		Z = [nghiem[0]+pi, alpha1[0] + 2*pi, z, beta[0]]

		#### để lọc lấy một nghiệm trong đáp án, còn các kết quả còn lại không phải nghiệm
		fx = lambda x: cos(x - alpha) - VP
		for i in Z:
			if fx(i) == 0 and i != z:
				Z.remove(i)
				Z.append(i+pi/3)

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các giá trị sau, giá trị nào là nghiệm của phương trình $%s = 0$?" 
			%(latex(a*sin(x) + b*cos(x) - c))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{Ta có \
			\begin{eqnarray*}\
				&& %s = 0\\ \
				&\Leftrightarrow& %s \sin(x) + %s \cos(x) = %s\\ \
				&\Leftrightarrow& \sin \left( %s \right) \sin(x) + \cos \left( %s \right) \cos(x) = %s\\ \
				&\Leftrightarrow& \cos \left( %s \right) = \cos %s \\"
			%(latex(a*sin(x) + b*cos(x) - c), 
			latex(sin(alpha)), latex(cos(alpha)), latex(VP),
			latex(alpha), latex(alpha), latex(VP),
			latex(x - alpha), latex(beta[0]))+ os.linesep)
		if len(nghiem) == 1:
			de.write(r"&\Leftrightarrow& x = %s + k2\pi \
				\end{eqnarray*}}"
				%(latex(nghiem[0])))
		else:
			de.write(r"&\Leftrightarrow& \hoac{& x = %s + k2\pi \\& x = %s + k2\pi} \
				\end{eqnarray*}}"
				%(latex(nghiem[0]), latex(nghiem[1])))
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11K3_2(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		y = Symbol('y')
		t = Symbol('t')
		k = Symbol('k')
		a = np.choice([1,-1,sqrt(3),-sqrt(3)])
		b = np.choice([1,-1])
		VP = np.choice([sqrt(1)/2,-sqrt(1)/2,sqrt(2)/2,-sqrt(2)/2,sqrt(3)/2,-sqrt(3)/2,1,-1])
		c = VP*sqrt(a**2+b**2)

		### để tìm ra góc alpha để được cos(x - alpha) = c/sqrt(a^2+b^2)
		alpha1 = solve(sin(y)-(a/sqrt(a**2+b**2)))
		alpha2 = solve(cos(y)-(b/sqrt(a**2+b**2)))
		for i in alpha1:
			if i in alpha2:
				alpha = i
			else:
				if i + 2*pi in alpha2:
					alpha = i +2*pi
		
		### để được c/sqrt(a^2+b^2) = cos(beta)
		beta = solve(cos(t)-VP)

		nghiem = solve(cos(x - alpha) - VP)
		### loại trừ trường hợp nghiệm trùng khi thêm k2pi
		if (len(nghiem) != 1) and ((nghiem[0] + 2*pi == nghiem[1]) or (nghiem[0] - 2*pi == nghiem[1])):
			nghiem.remove(nghiem[1])

		### tách ra tập nghiệm âm, tập nghiệm dương. trong đó tập dương xếp tăng dần, âm xếp giảm dần
		S = []
		S_duong = []
		S_am = []
		S_0 = []
		for i in nghiem:
			for k in range(-3,4):
				S.append(i + k*2*pi)
		for i in S:
			if i > 0:
				S_duong.append(i)
			elif i < 0:
				S_am.append(i)
			else:
				S_0.append(i)
		S_duong.sort()
		S_am.sort()
		S_am.reverse()

		### tổng hai hoặc ba nghiệm 
		songhiem = np.choice(['hai', 'ba'])
		so_nghiem = {'hai': 2, 'ba': 3}
		
		### không dương lớn nhất	
		z1 = 0
		if len(S_0) != 0:
			z1 += S_0[0]
			for i in range(0,so_nghiem[songhiem]):
				z1 += S_am[i]
		else:
			for i in range(0,so_nghiem[songhiem]):
				z1 += S_am[i]

		### 	không âm nhỏ nhất
		z2 = 0
		if len(S_0) != 0:
			z2 += S_0[0]
			for i in range(0,so_nghiem[songhiem]):
				z2 += S_duong[i]
		else:
			for i in range(0,so_nghiem[songhiem]):
				z2 += S_duong[i]

		### dương nhỏ nhất
		z3 = 0
		for i in range(0,so_nghiem[songhiem]):
			z3 += S_duong[i]

	 	### âm lớn nhất
		z4 = 0
		for i in range(0,so_nghiem[songhiem]):
			z4 += S_am[i]


		if condition == 0:
			dk = 'không dương lớn nhất'
			z = z1
		elif condition == 1:
			dk = 'không âm nhỏ nhất'
			z = z2
		elif condition == 2:
			dk = 'dương nhỏ nhất'
			z = z3
		else:
			dk = 'âm lớn nhất'
			z = z4

		Z= [z,S_duong[0],S_am[0],z+2*pi]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng %s nghiệm %s của phương trình $%s = 0$." 
			%(songhiem, dk, latex(a*sin(x) + b*cos(x) - c))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"\loigiai{Ta có \
			\begin{eqnarray*}\
				&& %s = 0\\ \
				&\Leftrightarrow& %s \sin(x) + %s \cos(x) = %s\\ \
				&\Leftrightarrow& \sin \left( %s \right) \sin(x) + \cos \left( %s \right) \cos(x) = %s\\ \
				&\Leftrightarrow& \cos \left( %s \right) = \cos %s \\"
			%(latex(a*sin(x) + b*cos(x) - c), 
			latex(sin(alpha)), latex(cos(alpha)), latex(VP),
			latex(alpha), latex(alpha), latex(VP),
			latex(x - alpha), latex(beta[0]))+ os.linesep)
		if len(nghiem) == 1:
			de.write(r"&\Leftrightarrow& x = %s + k2\pi \
				\end{eqnarray*}}"
				%(latex(nghiem[0]))+ os.linesep)
		else:
			de.write(r"&\Leftrightarrow& \hoac{& x = %s + k2\pi \\& x = %s + k2\pi} \
				\end{eqnarray*}}"
				%(latex(nghiem[0]), latex(nghiem[1]))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B3_3():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		t = Symbol('t')
		a = np.randint(-2,3)
		while a == 0:
			a = np.randint(-2,3)
		X = [pi/6, pi/4, pi/3, 2*pi/3, 3*pi/4, 5*pi/6]
		x1 = np.choice(X)
		x2 = np.choice(X)
		while tan(x1)+tan(x2) == 0: ### để phương trình luôn có số hạng sin(x) * cos(x)
			x1 = np.choice(X)
			x2 = np.choice(X)		
		t1 = tan(x1)
		t2 = tan(x2)
		fx = a*t**2 - a*(t1 + t2)*t + a*t1*t2
		fx_gtlg = a*(sin(x))**2 - a*(t1 + t2)*sin(x)*cos(x) + (a*t1*t2)*(cos(x))**2
		z = x1 + pi/2
		Z = [z, x1, x2 - 2*pi, x2]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Trong các giá trị sau, giá trị nào không phải là nghiệm của phương trình $%s = 0$." 
			%(latex(fx_gtlg))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{\begin{itemize}			\item Xét $\cos x = 0$, thì phương trình trở thành $%s = 0$ \
				(sai, vì $\sin^2 x = 1$). Loại trường hợp $\cos x = 0$.\
				\item Xét $\cos x \ne 0$, chia cả hai vế của phương trình với $\cos ^2 x$. Đặt $t =\tan x$, \
				ta được phương trình"
		        %(latex(a*(sin(x))**2))+ os.linesep)
		if x1 != x2:
			de.write(r"\begin{eqnarray*}\
		        %s = 0 \Leftrightarrow \hoac{& t = %s \\ & t = %s}\
		        \Leftrightarrow \hoac{& x = %s + k \pi \\& x = %s + k \pi}\
		        \end{eqnarray*}\
		        \end{itemize}}"
		        %(latex(fx), latex(t1), latex(t2),
		        	latex(x1), latex(x2))+ os.linesep)
		else:
			de.write(r"\begin{eqnarray*}\
		        %s = 0 \Leftrightarrow t = %s\
		        \Leftrightarrow  x = %s + k \pi\
		        \end{eqnarray*}\
		        \end{itemize}}"
		        %(latex(fx), latex(t1),
		        	latex(x1))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11K3_4(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		t = Symbol('t')
		a = np.randint(-2,3)
		while a == 0:
			a = np.randint(-2,3)
		X = [pi/6, pi/4, pi/3, 2*pi/3, 3*pi/4, 5*pi/6]
		x1 = np.choice(X)
		x2 = np.choice(X)
		while tan(x1)+tan(x2) == 0: ### để phương trình luôn có số hạng sin(x) * cos(x)
			x1 = np.choice(X)
			x2 = np.choice(X)		
		t1 = tan(x1)
		t2 = tan(x2)
		fx = a*t**2 - a*(t1 + t2)*t + a*t1*t2
		fx_gtlg = a*(sin(x))**2 - a*(t1 + t2)*sin(x)*cos(x) + (a*t1*t2)*(cos(x))**2

		### tách ra tập nghiệm âm, tập nghiệm dương. trong đó tập dương xếp tăng dần, âm xếp giảm dần
		if x1 != x2:
			nghiem = [x1,x2]
		else:
			nghiem = [x1]
		S = []
		S_duong = []
		S_am = []
		S_0 = []
		for i in nghiem:
			for k in range(-3,4):
				S.append(i + k*pi)
		for i in S:
			if i > 0:
				S_duong.append(i)
			elif i < 0:
				S_am.append(i)
			else:
				S_0.append(i)
		S_duong.sort()
		S_am.sort()
		S_am.reverse()

		### tổng hai hoặc ba nghiệm 
		songhiem = np.choice(['hai', 'ba'])
		so_nghiem = {'hai': 2, 'ba': 3}
		
		### không dương lớn nhất	
		z1 = 0
		if len(S_0) != 0:
			z1 += S_0[0]
			for i in range(0,so_nghiem[songhiem]):
				z1 += S_am[i]
		else:
			for i in range(0,so_nghiem[songhiem]):
				z1 += S_am[i]

		### 	không âm nhỏ nhất
		z2 = 0
		if len(S_0) != 0:
			z2 += S_0[0]
			for i in range(0,so_nghiem[songhiem]):
				z2 += S_duong[i]
		else:
			for i in range(0,so_nghiem[songhiem]):
				z2 += S_duong[i]

		### dương nhỏ nhất
		z3 = 0
		for i in range(0,so_nghiem[songhiem]):
			z3 += S_duong[i]

	 	### âm lớn nhất
		z4 = 0
		for i in range(0,so_nghiem[songhiem]):
			z4 += S_am[i]


		if condition == 0:
			dk = 'không dương lớn nhất'
			z = z1
		elif condition == 1:
			dk = 'không âm nhỏ nhất'
			z = z2
		elif condition == 2:
			dk = 'dương nhỏ nhất'
			z = z3
		else:
			dk = 'âm lớn nhất'
			z = z4

		Z= [z,S_duong[0],S_am[0],z+pi]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tính tổng %s nghiệm %s của phương trình $%s = 0$." 
			%(songhiem, dk, latex(fx_gtlg))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{\begin{itemize}			\item Xét $\cos x = 0$, thì phương trình trở thành $%s = 0$ \
				(sai, vì $\sin^2 x = 1$). Loại trường hợp $\cos x = 0$.\
				\item Xét $\cos x \ne 0$, chia cả hai vế của phương trình với $\cos ^2 x$. Đặt $t =\tan x$, \
				ta được phương trình"
		        %(latex(a*(sin(x))**2))+ os.linesep)
		if x1 != x2:
			de.write(r"\begin{eqnarray*}\
		        %s = 0 \Leftrightarrow \hoac{& t = %s \\ & t = %s}\
		        \Leftrightarrow \hoac{& x = %s + k \pi \\& x = %s + k \pi}\
		        \end{eqnarray*}\
		        \end{itemize}}"
		        %(latex(fx), latex(t1), latex(t2),
		        	latex(x1), latex(x2))+ os.linesep)
		else:
			de.write(r"\begin{eqnarray*}\
		        %s = 0 \Leftrightarrow t = %s\
		        \Leftrightarrow  x = %s + k \pi\
		        \end{eqnarray*}\
		        \end{itemize}}"
		        %(latex(fx), latex(t1),
		        	latex(x1))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)



def D11G3_5(condition):
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		y = Symbol('y')
		num = []
		for i in range(0,6):
			i = np.randint(-5,5)
			num.append(i)

		##### 2 điều kiện đầu để tử mẫu phải có sin hoặc cos, điều kiện thứ ba để hàm số có giá trị cả nhỏ và lớn nhất (vì a của hy < 0, mà hy >= 0), điều kiện cuối là để  phương trình hy có nghiệm
		while (num[0]**2 + num[1]**2 + num[2]**2 == 0) or (num[3]**2 + num[4]**2 == 0) or (num[3]**2 + num[4]**2 - num[5]**2) >= 0 or (dc.Delta((num[3]**2 + num[4]**2 - num[5]**2),(num[2]*num[5] - num[0]*num[3] - num[1]*num[4])*2,num[0]**2 + num[1]**2 - num[2]**2) < 0):
			num = []
			for i in range(0,6):
				i = np.randint(-5,5)
				num.append(i)

		fx = num[0]*sin(x) + num[1]*cos(x) + num[2] 
		gx = num[3]*sin(x) + num[4]*cos(x) + num[5] 

		### hàm số sau khi đưa về phương trình được phương trình cuối cùng là
		VT = sin(x)*(num[0]-num[3]*y) + cos(x)*(num[1]-num[4]*y)
		VP = num[5]*y - num[2]

		### đưa về điều kiện để có nghiệm, và bất phương trình cuối cùng là hy >= 0
		dkVT = (num[0]-num[3]*y)**2 + (num[1]-num[4]*y)**2
		dkVP = (num[5]*y - num[2])**2
		hy = ((num[3])**2 + (num[4])**2 - (num[5])**2)*y**2 + 2*y*((num[2])*(num[5]) - num[0]*num[3] - num[1]*num[4]) + (num[0])**2 + (num[1])**2 - (num[2])**2

			
		### miền giá trị của y y1< y2 (do a <0 nên + sqrt(Delta) < - sqrt(Delta))
		y2 = dc.NghiemBH(((num[3])**2 + (num[4])**2 - (num[5])**2),(num[2]*num[5] - num[0]*num[3] - num[1]*num[4])*2,(num[0])**2 + (num[1])**2 - (num[2])**2)[0]
		y1 = dc.NghiemBH(((num[3])**2 + (num[4])**2 - (num[5])**2),(num[2]*num[5] - num[0]*num[3] - num[1]*num[4])*2,(num[0])**2 + (num[1])**2 - (num[2])**2)[1]

		de.write(r"\begin{ex}"+ os.linesep)
		if condition == 0:
			z = y1 + y2
			Z = [z, z+1, z-1, z-2]
			de.write(r"Cho hàm số $y=\dfrac{%s}{%s}$, biết hàm số đó có giá trị lớn nhất là $M$ và giá trị nhỏ nhất là $m$. Tính $M+m$." %(latex(fx), latex(gx)) + os.linesep )
			de.write(r"\choice"+ os.linesep)
			de.write(r"{$%s$}" %(latex(dc.check(z,Z)[3]))+ os.linesep)
			de.write(r"{$%s$}" %(latex(dc.check(z,Z)[2]))+ os.linesep)
			de.write(r"{$%s$}" %(latex(dc.check(z,Z)[1]))+ os.linesep)
			de.write(r"{\True $%s$}" %(latex(dc.check(z,Z)[0]))+ os.linesep)
		else:
			de.write(r"Cho hàm số $y=\dfrac{%s}{%s}$, giá trị lớn nhất và giá trị nhỏ nhất của hàm số thuộc khoảng nào trong các khoảng sau?" %(latex(fx), latex(gx)) + os.linesep )
			de.write(r"\choice"+ os.linesep)
			de.write(r"{\True $\left( %s ; %s \right)$}" %(latex(floor(y1)), latex(floor(y2)+1))+ os.linesep)
			de.write(r"{$\left( %s ; %s \right)$}" %(latex(floor(y1)-2), latex(floor(y2)-2))+ os.linesep)
			de.write(r"{$\left( %s ; %s \right)$}" %(latex(floor(y1)+1), latex(floor(y2)))+ os.linesep)
			de.write(r"{$\left( %s ; %s \right)$}" %(latex(floor(y1)-3), latex(floor(y2)-3))+ os.linesep)

		de.write(r"\loigiai{$y=\dfrac{%s}{%s}\Leftrightarrow %s = %s$ \hfill (1)\\ \
			Phương trình $(1)$ có nghiệm khi và chỉ khi $%s \geq %s$\\ \
			$\Leftrightarrow %s \ge 0 \Leftrightarrow %s \le y \le %s$.\\ \
			Vậy $\max y=%s$, $\min y=%s$}"
			%(latex(fx), latex(gx), latex(VT), latex(VP),
				latex(dkVT), latex(dkVP), latex(hy), latex(y1), latex(y2), latex(y1), latex(y2)) + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y3_6():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		dk = np.choice(['có nghiệm', 'vô nghiệm'])
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm điều kiện của $a$, $b$, $c$ để phương trình $a \sin x + b \cos x = c$ %s." %(dk) + os.linesep )
		de.write(r"\choice"+ os.linesep)
		if dk == 'có nghiệm':
			de.write(r"{$a^2 + b^2 > c^2$}" + os.linesep) 
			de.write(r"{$a^2 + b^2 < c^2$}" + os.linesep) 
			de.write(r"{\True $a^2 + b^2 \ge c^2$}" + os.linesep) 
			de.write(r"{$a^2 + b^2 \le c^2$}" + os.linesep) 
		else:
			de.write(r"{$a^2 + b^2 > c^2$}" + os.linesep) 
			de.write(r"{\True $a^2 + b^2 < c^2$}" + os.linesep) 
			de.write(r"{$a^2 + b^2 \ge c^2$}" + os.linesep) 
			de.write(r"{$a^2 + b^2 \le c^2$}" + os.linesep) 
		de.write(r"\loigiai{}" + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B3_7():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		y = Symbol('y')
		t = Symbol('t')
		k = Symbol('k')
		a = np.choice([1,-1,sqrt(3),-sqrt(3)])
		b = np.choice([1,-1])
		VP = np.choice([sqrt(1)/2,-sqrt(1)/2,sqrt(2)/2,-sqrt(2)/2,sqrt(3)/2,-sqrt(3)/2,1,-1])
		c = VP*sqrt(a**2+b**2)

		### để tìm ra góc alpha để được cos(x - alpha) = c/sqrt(a^2+b^2)
		alpha1 = solve(sin(y)-(a/sqrt(a**2+b**2)))
		alpha2 = solve(cos(y)-(b/sqrt(a**2+b**2)))
		for i in alpha1:
			if i in alpha2:
				alpha = i
			else:
				if i + 2*pi in alpha2:
					alpha = i +2*pi
		
		### để được c/sqrt(a^2+b^2) = cos(beta)
		beta = solve(cos(t)-VP)

		nghiem = solve(cos(x - alpha) - VP)
		### loại trừ trường hợp nghiệm trùng khi thêm k2pi
		if (len(nghiem) != 1) and ((nghiem[0] + 2*pi == nghiem[1]) or (nghiem[0] - 2*pi == nghiem[1])):
			nghiem.remove(nghiem[1])

		### tách ra tập nghiệm âm, tập nghiệm dương. trong đó tập dương xếp tăng dần, âm xếp giảm dần
		S = []
		S_duong = []
		S_am = []
		S_0 = []
		for i in nghiem:
			for k in range(-4,4):
				S.append(i + k*2*pi)
		for i in S:
			if i > 0:
				S_duong.append(i)
			elif i < 0:
				S_am.append(i)
			else:
				S_0.append(i)
		S_duong.sort()
		S_am.sort()
		S_am.reverse()

		dk = np.choice(['không dương lớn nhất', 'không âm nhỏ nhất', 'dương nhỏ nhất', 'âm lớn nhất'])
		if dk == 'không dương lớn nhất':
			if 0 in S_0:
				z = 0
			else:
				z = S_am[0]
			Z= [z,-z/2,S_am[1],0]
		elif dk == 'không âm nhỏ nhất':
			if 0 in S_0:
				z = 0
			else:
				z = S_duong[0]
			Z= [z,z/2,S_duong[1],0]
		elif dk == 'dương nhỏ nhất':
			z = S_duong[0]
			Z= [z,z/2,S_duong[1],0]
		else:
			z = S_am[0]
			Z= [z,-z/2,S_am[1],0]

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm nghiệm %s của phương trình $%s = 0$." 
			%(dk, latex(a*sin(x) + b*cos(x) - c))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"\loigiai{Ta có \
			\begin{eqnarray*}\
				&& %s = 0\\ \
				&\Leftrightarrow& %s \sin(x) + %s \cos(x) = %s\\ \
				&\Leftrightarrow& \sin \left( %s \right) \sin(x) + \cos \left( %s \right) \cos(x) = %s\\ \
				&\Leftrightarrow& \cos \left( %s \right) = \cos %s \\"
			%(latex(a*sin(x) + b*cos(x) - c), 
			latex(sin(alpha)), latex(cos(alpha)), latex(VP),
			latex(alpha), latex(alpha), latex(VP),
			latex(x - alpha), latex(beta[0]))+ os.linesep)
		if len(nghiem) == 1:
			de.write(r"&\Leftrightarrow& x = %s + k2\pi \
				\end{eqnarray*}}"
				%(latex(nghiem[0]))+ os.linesep)
		else:
			de.write(r"&\Leftrightarrow& \hoac{& x = %s + k2\pi \\& x = %s + k2\pi} \
				\end{eqnarray*}}"
				%(latex(nghiem[0]), latex(nghiem[1]))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B3_8():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		t = Symbol('t')
		a = np.randint(-2,3)
		while a == 0:
			a = np.randint(-2,3)
		X = [pi/6, pi/4, pi/3, 2*pi/3, 3*pi/4, 5*pi/6]
		x1 = np.choice(X)
		x2 = np.choice(X)
		while tan(x1)+tan(x2) == 0: ### để phương trình luôn có số hạng sin(x) * cos(x)
			x1 = np.choice(X)
			x2 = np.choice(X)		
		t1 = tan(x1)
		t2 = tan(x2)
		fx = a*t**2 - a*(t1 + t2)*t + a*t1*t2
		fx_gtlg = a*(sin(x))**2 - a*(t1 + t2)*sin(x)*cos(x) + (a*t1*t2)*(cos(x))**2

		### tách ra tập nghiệm âm, tập nghiệm dương. trong đó tập dương xếp tăng dần, âm xếp giảm dần
		if x1 != x2:
			nghiem = [x1,x2]
		else:
			nghiem = [x1]
		S = []
		S_duong = []
		S_am = []
		S_0 = []
		for i in nghiem:
			for k in range(-4,4):
				S.append(i + k*pi)
		for i in S:
			if i > 0:
				S_duong.append(i)
			elif i < 0:
				S_am.append(i)
			else:
				S_0.append(i)
		S_duong.sort()
		S_am.sort()
		S_am.reverse()
		
		dk = np.choice(['không dương lớn nhất', 'không âm nhỏ nhất', 'dương nhỏ nhất', 'âm lớn nhất'])
		if dk == 'không dương lớn nhất':
			if 0 in S_0:
				z = 0
			else:
				z = S_am[0]
			Z= [z,-z/2,S_am[1],0]
		elif dk == 'không âm nhỏ nhất':
			if 0 in S_0:
				z = 0 
			else:
				z = S_duong[0]
			Z= [z,z/2,S_duong[1],0]
		elif dk == 'dương nhỏ nhất':
			z = S_duong[0]
			Z= [z,z/2,S_duong[1],0]
		else:
			z = S_am[0]
			Z= [z,-z/2,S_am[1],0]

		Z= [z,S_duong[0],S_am[0],z+pi]
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm nghiệm %s của phương trình $%s = 0$." 
			%(dk, latex(fx_gtlg))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{$%s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{\True $%s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"\loigiai{\begin{itemize}			\item Xét $\cos x = 0$, thì phương trình trở thành $%s = 0$ \
				(sai, vì $\sin^2 x = 1$). Loại trường hợp $\cos x = 0$.\
				\item Xét $\cos x \ne 0$, chia cả hai vế của phương trình với $\cos ^2 x$. Đặt $t =\tan x$, \
				ta được phương trình"
		        %(latex(a*(sin(x))**2))+ os.linesep)
		if x1 != x2:
			de.write(r"\begin{eqnarray*}\
		        %s = 0 \Leftrightarrow \hoac{& t = %s \\ & t = %s}\
		        \Leftrightarrow \hoac{& x = %s + k \pi \\& x = %s + k \pi}\
		        \end{eqnarray*}\
		        \end{itemize}}"
		        %(latex(fx), latex(t1), latex(t2),
		        	latex(x1), latex(x2))+ os.linesep)
		else:
			de.write(r"\begin{eqnarray*}\
		        %s = 0 \Leftrightarrow t = %s\
		        \Leftrightarrow  x = %s + k \pi\
		        \end{eqnarray*}\
		        \end{itemize}}"
		        %(latex(fx), latex(t1),
		        	latex(x1))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)



def D11B3_9():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		y = Symbol('y')
		t = Symbol('t')
		k = Symbol('k')
		a = np.choice([1,-1,sqrt(3),-sqrt(3)])
		b = np.choice([1,-1])
		VP = np.choice([sqrt(1)/2,-sqrt(1)/2,sqrt(2)/2,-sqrt(2)/2,sqrt(3)/2,-sqrt(3)/2,1,-1])
		c = VP*sqrt(a**2+b**2)

		### để tìm ra góc alpha để được cos(x - alpha) = c/sqrt(a^2+b^2)
		alpha1 = solve(sin(y)-(a/sqrt(a**2+b**2)))
		alpha2 = solve(cos(y)-(b/sqrt(a**2+b**2)))
		for i in alpha1:
			if i in alpha2:
				alpha = i
			else:
				if i + 2*pi in alpha2:
					alpha = i +2*pi
		
		### để được c/sqrt(a^2+b^2) = cos(beta)
		beta = solve(cos(t)-VP)

		nghiem = solve(cos(x - alpha) - VP)
		### loại trừ trường hợp nghiệm trùng khi thêm k2pi
		if (len(nghiem) != 1) and ((nghiem[0] + 2*pi == nghiem[1]) or (nghiem[0] - 2*pi == nghiem[1])):
			nghiem.remove(nghiem[1])

		### tập nghiệm
		S = []
		for i in nghiem:
			for l in range(-3,3):
				S.append(i + l*2*pi)
		S.sort()

		### Tìm đoạn chứa z, đoạn có độ lớn d
		index = np.randint(2,len(S)-2)
		z = S[index]
		if (VP == sqrt(2)/2) or (VP == -sqrt(2)/2): 
			d = pi/3
		else:
			d = pi/2
		l = floor(z/d)
		h = l*d
		hh = (l+1)*pi/2

		### đáp án nhiễu
		Z = [z,(z+h)/2]
		i = 1
		while len(Z) < 4:
			if z > 0:
				z1 = S[index+i]
				if (h <= z1) and (z1 <= hh):
					Z.append((z+z1)/2)
				else:
					Z.append(z1)
				i += 1
			else:
				z1 = S[index-i]
				if (h <= z1) and (z1 <= hh):
					Z.append((z+z1)/2)
				else:
					Z.append(z1)
				i += -1			

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm số $x$ thõa mãn phương trình $%s = 0$ và $x$ thuộc đoạn $\left[ %s; %s \right]$." 
			%(latex(a*sin(x) + b*cos(x) - c), latex(h), latex(hh))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$x = %s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$x = %s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{\True $x = %s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"{$x = %s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"\loigiai{Ta có \
			\begin{eqnarray*}\
				&& %s = 0\\ \
				&\Leftrightarrow& %s \sin(x) + %s \cos(x) = %s\\ \
				&\Leftrightarrow& \sin \left( %s \right) \sin(x) + \cos \left( %s \right) \cos(x) = %s\\ \
				&\Leftrightarrow& \cos \left( %s \right) = \cos %s \\"
			%(latex(a*sin(x) + b*cos(x) - c), 
			latex(sin(alpha)), latex(cos(alpha)), latex(VP),
			latex(alpha), latex(alpha), latex(VP),
			latex(x - alpha), latex(beta[0]))+ os.linesep)
		if len(nghiem) == 1:
			de.write(r"&\Leftrightarrow& x = %s + k2\pi \
				\end{eqnarray*}}"
				%(latex(nghiem[0]))+ os.linesep)
		else:
			de.write(r"&\Leftrightarrow& \hoac{& x = %s + k2\pi \\& x = %s + k2\pi} \
				\end{eqnarray*}}"
				%(latex(nghiem[0]), latex(nghiem[1]))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y3_10():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		y = Symbol('y')
		t = Symbol('t')
		k = Symbol('k')
		a = np.choice([1,-1,sqrt(3),-sqrt(3)])
		b = np.choice([1,-1])
		VP = np.choice([sqrt(1)/2,-sqrt(1)/2,sqrt(2)/2,-sqrt(2)/2,sqrt(3)/2,-sqrt(3)/2,1,-1])
		c = VP*sqrt(a**2+b**2)

		### để tìm ra góc alpha để được cos(x - alpha) = c/sqrt(a^2+b^2)
		alpha1 = solve(sin(y)-(a/sqrt(a**2+b**2)))
		alpha2 = solve(cos(y)-(b/sqrt(a**2+b**2)))
		for i in alpha1:
			if i in alpha2:
				alpha = i
			else:
				if i + 2*pi in alpha2:
					alpha = i +2*pi
		
		### để được c/sqrt(a^2+b^2) = cos(beta)
		beta = solve(cos(t)-VP)

		nghiem = solve(cos(x - alpha) - VP)
		### loại trừ trường hợp nghiệm trùng khi thêm k2pi
		if (len(nghiem) != 1) and ((nghiem[0] + 2*pi == nghiem[1]) or (nghiem[0] - 2*pi == nghiem[1])):
			nghiem.remove(nghiem[1])

		### tập nghiệm
		S = []
		for i in nghiem:
			for l in range(-3,3):
				S.append(i + l*2*pi)
		S.sort()

		### Tìm đoạn chứa z, đoạn có độ lớn d
		index = np.randint(2,len(S)-2)
		z = S[index]
		if (VP == sqrt(2)/2) or (VP == -sqrt(2)/2): 
			d = pi/3
		else:
			d = pi/2
		l = floor(z/d)
		h = l*d
		hh = (l+1)*pi/2

		### đáp án nhiễu
		Z = [z,(z+h)/2]
		i = 1
		while len(Z) < 4:
			if z > 0:
				z1 = S[index+i]
				if (h <= z1) and (z1 <= hh):
					Z.append((z+z1)/2)
				else:
					Z.append(z1)
				i += 1
			else:
				z1 = S[index-i]
				if (h <= z1) and (z1 <= hh):
					Z.append((z+z1)/2)
				else:
					Z.append(z1)
				i += -1			

		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Tìm số $x$ thõa mãn phương trình $%s = 0$ và $x$ thuộc đoạn $\left[ %s; %s \right]$." 
			%(latex(a*sin(x) + b*cos(x) - c), latex(h), latex(hh))+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$x = %s$}" %(latex(dc.check_radian(z,Z)[1]))+ os.linesep)
		de.write(r"{$x = %s$}" %(latex(dc.check_radian(z,Z)[2]))+ os.linesep)
		de.write(r"{\True $x = %s$}" %(latex(dc.check_radian(z,Z)[0]))+ os.linesep)
		de.write(r"{$x = %s$}" %(latex(dc.check_radian(z,Z)[3]))+ os.linesep)
		de.write(r"\loigiai{Ta có \
			\begin{eqnarray*}\
				&& %s = 0\\ \
				&\Leftrightarrow& %s \sin(x) + %s \cos(x) = %s\\ \
				&\Leftrightarrow& \sin \left( %s \right) \sin(x) + \cos \left( %s \right) \cos(x) = %s\\ \
				&\Leftrightarrow& \cos \left( %s \right) = \cos %s \\"
			%(latex(a*sin(x) + b*cos(x) - c), 
			latex(sin(alpha)), latex(cos(alpha)), latex(VP),
			latex(alpha), latex(alpha), latex(VP),
			latex(x - alpha), latex(beta[0]))+ os.linesep)
		if len(nghiem) == 1:
			de.write(r"&\Leftrightarrow& x = %s + k2\pi \
				\end{eqnarray*}}"
				%(latex(nghiem[0]))+ os.linesep)
		else:
			de.write(r"&\Leftrightarrow& \hoac{& x = %s + k2\pi \\& x = %s + k2\pi} \
				\end{eqnarray*}}"
				%(latex(nghiem[0]), latex(nghiem[1]))+ os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11Y3_11():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Phương trình nào sau đây là phương trình bậc hai theo một hàm số lượng giác?" 
			+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $2\cos^22x-\cos 2x=0$}" + os.linesep)
		de.write(r"{$2\sin^2x+\sin 2x-1=0$}" + os.linesep)
		de.write(r"{$\cot^2x+\cos 2x-7=0$}" + os.linesep)
		de.write(r"{$\tan^25 x+\cot x-5=0$}" + os.linesep)
		de.write(r"\loigiai{}" + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B3_12():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Giải phương trình $\tan x+\tan \left(x+\dfrac{\pi}{4}\right)=1$." 
			+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $x=k\pi, x=\arctan 3+k\pi, k \in \mathbb{Z}$}" + os.linesep)
		de.write(r"{$x=k2\pi, x=\arctan 3+k2\pi, k \in \mathbb{Z}$}" + os.linesep)
		de.write(r"{$x=k\pi, x=-\arctan 3+k\pi, k \in \mathbb{Z}$}" + os.linesep)
		de.write(r"{$x=k\pi, x=\arctan \dfrac{1}{3}+k\pi, k \in \mathbb{Z}$}" + os.linesep)
		de.write(r"\loigiai{}" + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11G3_13():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có tất cả bao nhiêu giá trị nguyên của tham số $m$ để phương trình $\cos 4x+6\sin x\cos x=m$ có hai nghiệm phân biệt trên đoạn $\left[0;\dfrac{\pi}{4}\right]$?" 
			+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{\True $1$}" + os.linesep)
		de.write(r"{$2$}" + os.linesep)
		de.write(r"{$3$}" + os.linesep)
		de.write(r"{$4$}" + os.linesep)
		de.write(r"\loigiai{Biến đổi phương trình đã cho về dạng $2\sin^2 2x-3\sin 2x+m-1=0$. Đặt $t=\sin 2x,\ t\in [-1;1]$, thì phương trình trở thành $2t^2-3t+m-1=0\ (1)$.\\\
		Từ giả thiết suy ra để phương trình ban đầu có hai nghiệm thuộc $\left[0;\dfrac{\pi}{4}\right]$ tức $2x \in \left[0;\dfrac{\pi}{2}\right]$ hay phương trình (1) phải có hai nghiệm phân biệt thuộc $[0;1]$.\\\
		Phương trình (1) tương đương với $2t^2-3t-1=-m$. Suy ra đồ thị của hàm số $y = 2t^2-3t-1$ phải cắt đường thẳng $y = -m$ tại hai điểm phân biệt thuộc đoạn $[0;1]$. Tức $-\dfrac{17}{8} < -m \le -2$, vậy $m = 2$ là $m$ nguyên cần tìm.}" + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)

def D11G3_14():
	with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
		x = Symbol('x')
		de.write(r"\begin{ex}"+ os.linesep)
		de.write(r"Có bao nhiêu giá trị nguyên của tham số $m$ để phương trình $|\sin x+\cos 2x|=m$ có nghiệm?" 
			+ os.linesep)
		de.write(r"\choice"+ os.linesep)
		de.write(r"{$1$}" + os.linesep)
		de.write(r"{$2$}" + os.linesep)
		de.write(r"{\True $3$}" + os.linesep)
		de.write(r"{$0$}" + os.linesep)
		de.write(r"\loigiai{Đặt $t=\sin x$, ta có phương trình $m=|2t^2-t-1|$.\\\
			Xét hàm số $f(t)=|2t^2-t-1|$ với $t\in [-1;1]$, được miền giá trị của $f(t)$ là $[0;2]$.\\\
			Do đó, có 3 giá trị nguyên của $m$ để phương trình có nghiệm.}" + os.linesep)
		de.write(r"\dotlineEX{10}"+ os.linesep)
		de.write(r"\end{ex}"+ os.linesep)


def D11B_TL_1():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Xét tính chẵn - lẻ của hàm số $y = \dfrac{\cos x}{2019}$." + os.linesep)
		TL.write(r"\loigiai{\begin{itemize} \item Tập xác định $\mathscr D = \mathbb{R}$. \
			\item Với mọi $x \in \mathscr D \Rightarrow -x \in \mathscr D$. \dotfill 0.25 điểm\
			\item Với mọi $x \in \mathscr D$, ta có $f(-x) = \dfrac{\cos (-x)}{2019} = \dfrac{\cos x}{2019} = f(x)$. \
			\end{itemize}\
			Suy ra hàm số là hàm số chẵn. \dotfill 0.25 điểm\\ }"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)
def D11B_TL_2():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Giải phương trình $\tan \dfrac{1}{2}x = 2$." + os.linesep)
		TL.write(r"\loigiai{$\tan \dfrac{1}{2}x = 2 \Leftrightarrow \dfrac{1}{2}x = \arctan 2 + k\pi$ \dotfill 0.25 điểm\\\
			$\Leftrightarrow x = 2 \arctan 2 + 2k\pi$. \dotfill 0.25 điểm\\}"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep)
def D11B_TL_3():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Giải phương trình $\sin \dfrac{1}{2}x + \dfrac{5}{4} = 0$." + os.linesep)
		TL.write(r"\loigiai{$\sin \dfrac{1}{2}x + \dfrac{5}{4} = 0  \Leftrightarrow \sin \dfrac{1}{2}x = -\dfrac{5}{4} $. \dotfill 0.25 điểm\\ \
			Mà $- \dfrac{5}{4} < -1$ nên phương trình đã cho vô nghiệm. \dotfill 0.25 điểm\\}"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep) 
def D11B_TL_4():
	with open(r"latex\data\TL.tex","a",encoding='utf-8') as TL:
		TL.write(r"\begin{bt}"+ os.linesep)
		TL.write(r"Giải phương trình $\cot^2 x - 2\cot x +1 =0$." + os.linesep)
		TL.write(r"\loigiai{Điều kiện $\sin x \ne 0$. \dotfill 0.25 điểm\\ \
			$\cot^2 x - 2\cot x +1 =0 \Leftrightarrow \cot x = 1 \Leftrightarrow x = \dfrac{\pi}{4} + k\pi$ (Thõa điều kiện) Kết luận. \dotfill 0.25 điểm\\}"+ os.linesep)
		TL.write(r"\dotlineEX{10}"+ os.linesep)
		TL.write(r"\end{bt}"+ os.linesep) 