import math

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
from sympy.solvers.inequalities import solve_rational_inequalities
from sympy.solvers.inequalities import reduce_rational_inequalities
from sympy.solvers.inequalities import solve_univariate_inequality
from sympy import Eq
from sympy.solvers import solve_undetermined_coeffs
from sympy.solvers import checksol
from sympy.solvers.polysys import solve_triangulated
from sympy.solvers.inequalities import reduce_abs_inequalities
from sympy import Poly, Symbol
import random
import numbers
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



def H11Y_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,4)
        de.write(r"\begin{ex}"+ os.linesep)
        if k == 0:
            de.write(r"Trong các khẳng định sau, khẳng định nào đúng?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True Phép dời hình là phép biến hình không làm thay đổi khoảng cách giữa hai điểm bất kì}" + os.linesep)
            de.write(r"{Phép dời hình là phép tịnh tiến không làm thay đổi khoảng cách giữa hai điểm bất kì}" + os.linesep)
            de.write(r"{Phép dời hình là phép vị tự không làm thay đổi khoảng cách giữa hai điểm bất kì}" + os.linesep)
            de.write(r"{Phép dời hình là phép đối xứng không làm thay đổi khoảng cách giữa hai điểm bất kì}" + os.linesep)
        elif k == 1:
            de.write(r"Trong các khẳng định sau, khẳng định nào đúng?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True Phép vị tự tỉ số $k = 1$ là phép đồng nhất}" + os.linesep)
            de.write(r"{Phép vị tự tỉ số $k = -1$ là phép đối xứng trục}" + os.linesep)
            de.write(r"{Phép đồng nhất là phép vị tự tỉ số $k = 1$}" + os.linesep)
            de.write(r"{Phép đối xứng trục là phép vị tự tỉ số $k = -1$}" + os.linesep)
        elif k == 2:
            de.write(r"Trong các khẳng định sau, khẳng định nào đúng?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True Hai hình gọi là bằng nhau nếu có phép dời hình biến hình này thành hình kia}" + os.linesep)
            de.write(r"{Hai hình gọi là bằng nhau nếu có phép biến hình biến hình này thành hình kia}" + os.linesep)
            de.write(r"{Hai hình gọi là bằng nhau nếu có phép đồng dạng biến hình này thành hình kia}" + os.linesep)
            de.write(r"{Hai hình gọi là bằng nhau nếu có phép vị tự biến hình này thành hình kia}" + os.linesep)
        else:
            de.write(r"Trong các khẳng định sau, khẳng định nào {\bf sai}?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{Phép quay là một phép dời hình}" + os.linesep)
            de.write(r"{Phép tịnh tiến là một phép dời hình}" + os.linesep)
            de.write(r"{Phép đối xứng tâm là một phép dời hình}" + os.linesep)
            de.write(r"{\True Phép vị tự là một phép dời hình}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)

def H11Y_2():
    with open(r"latex\data\de.tex", "a", encoding='utf-8') as de:
        k = np.randint(0, 4)
        de.write(r"\begin{ex}" + os.linesep)
        if k == 0:
            de.write(
                r"Trong mặt phẳng tọa độ $Oxy$, cho điểm $M(x;y)$. Phép đối xứng trục $Ox$ biến điểm $M$ thành điểm $M'(x';y')$. Tìm khẳng định đúng trong các khẳng định sau. " + os.linesep)
            de.write(r"\choice" + os.linesep)
            de.write(r"{\True $\heva{& x' = x \\& y' = -y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = -x \\& y' = y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = -x \\& y' = -y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = x \\& y' = y}$}" + os.linesep)
        elif k == 1:
            de.write(
                r"Trong mặt phẳng tọa độ $Oxy$, cho điểm $I(a;b)$. Phép đối xứng tâm $I$ biến điểm $M(x;y)$ thành điểm $M'(x';y')$. Tìm khẳng định đúng trong các khẳng định sau. " + os.linesep)
            de.write(r"\choice" + os.linesep)
            de.write(r"{\True $\heva{& x' = 2a - x \\& y' = 2b - y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = 2a + x \\& y' = 2b + y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = 2a - x \\& y' = 2b + y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = 2a + x \\& y' = 2b - y}$}" + os.linesep)
        elif k == 2:
            de.write(
                r"Trong mặt phẳng tọa độ $Oxy$, cho vectơ $\overrightarrow{u}$ có tọa độ $(a;b)$. Phép tịnh tiến theo vectơ $\overrightarrow{u}$ biến điểm $M(x;y)$ thành điểm $M'(x';y')$. Tìm khẳng định đúng trong các khẳng định sau. " + os.linesep)
            de.write(r"\choice" + os.linesep)
            de.write(r"{$\True \heva{& x' = x + a \\& y' = y + b}$}" + os.linesep)
            de.write(r"{$\heva{& x' = x - a \\& y' = y + b}$}" + os.linesep)
            de.write(r"{$\heva{& x' = x - a \\& y' = y - b}$}" + os.linesep)
            de.write(r"{$\heva{& x' = x + a \\& y' = y - b}$}" + os.linesep)
        else:
            de.write(
                r"Trong mặt phẳng tọa độ $Oxy$, cho điểm $M(x;y)$. Phép đối xứng trục $Oy$ biến điểm $M$ thành điểm $M'(x';y')$. Tìm khẳng định đúng trong các khẳng định sau. " + os.linesep)
            de.write(r"\choice" + os.linesep)
            de.write(r"{\True $\heva{& x' = -x \\& y' = y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = x \\& y' = y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = -x \\& y' = -y}$}" + os.linesep)
            de.write(r"{$\heva{& x' = x \\& y' = -y}$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}" + os.linesep)
        de.write(r"\end{ex}" + os.linesep)


def H11Y2_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,4)
        de.write(r"\begin{ex}"+ os.linesep)
        if k == 0:
            de.write(r"Cho hình vuông $ABCD$, phép tịnh tiến theo vectơ $\overrightarrow{AB}$ biến điểm $D$ thành điểm nào?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True $C$}" + os.linesep)
            de.write(r"{$A$}" + os.linesep)
            de.write(r"{$B$}" + os.linesep)
            de.write(r"{$D$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11G2_2():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        ### thuật toán: Tạo hình vuông ABCD số đẹp. phép tịnh tiến biến đường thẳng AB thành DC.
        # Trong các phép tinh tiên đó thì có 2 vecto u, v: vecto u có độ dài nhỏ nhất và goc giữa 2 vecto u,v bằng 45 độ. Tìm vecto v.
        # Có vecto u = vecto AD. vecto v = vecto AC.
        x = Symbol('x')
        y = Symbol('y')

        Diem = [[0,0],[0,0]] # hai điểm A,D
        u = [0,0] # vecto u - vecto có độ dài ngắn nhất
        while (u[0] == 0) or (u[1] == 0) or (u[0] == u[1]) or (u[0] == - u[1]):
            Diem = []
            for k in range(0,2):
                A = []
                for i in range(0,2):
                    i = np.randint(-3,3)
                    while i == 0:
                        i = np.randint(-3, 3)
                    A.append(i)

                Diem.append(A)
            u = [Diem[1][0] - Diem[0][0], Diem[1][1] - Diem[0][1]]

        # viết phương trình đường thẳng CD (đi qua điểm D, nhận vecto u làm vecto pháp tuyến): ax + by + c = 0 --> c = -ax_D - by_D
        c_CD = - u[0] * Diem[1][0] - u[1] * Diem[1][1]
        CD = u[0] * x + u[1] * y + c_CD

        # viết phương trình đường thẳng AB (đi qua điểm A, nhận vecto u làm vecto pháp tuyến): ax + by + c = 0 --> c = -ax_A - by_A
        c_AB = - u[0] * Diem[0][0] - u[1] * Diem[0][1]
        AB = u[0] * x + u[1] * y + c_AB

        DoDai_u = sqrt(u[0]**2 + u[1]**2)
        Diem_C = solve_poly_system([u[0]*x + u[1]*y + c_CD, (x - Diem[1][0])**2 + (y - Diem[1][1])**2 - DoDai_u**2], x, y)
        if Diem_C[0][0] < Diem[1][0]:
            C = Diem_C[1]
        else:
            C = Diem_C[0]
        v = [C[0] - Diem[0][0], C[1] - Diem[0][1]]
        print("A = ",Diem[0], "D = ", Diem[1])
        print(Diem_C)
        print(C)
        print(v)
        print(AB)
        print(CD)

        print('het---------------')

        z = dc.sum(v)
        Z = [dc.sum(v), v[0] - v[1], v[1] - v[0], -dc.sum(v)]
        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"Cho đường thẳng $d \colon %s = 0$ và đường thẳng $d' \colon %s = 0$. Tồn tại phép tịnh tiến theo vectơ $\overrightarrow{u} = (x_u; y_u)$ biến $d$ thành $d'$"
                 r" đồng thời độ dài của $\overrightarrow{u}$ nhỏ nhất. Cũng tồn tại phép tính tiến theo vectơ $\overrightarrow{v} = (x_v; y_v)$ biến $d$ thành $d'$"
                 r" mà góc giữa $\overrightarrow{u}$ và $\overrightarrow{v}$ bằng $\dfrac{\pi}{4}$. "
                 r" Biết rằng $x_v > x_u$. Tính $x_v + y_v$." % (latex(AB), latex(CD)) + os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
        de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
        de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
        de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
        de.write(r"\loigiai{Lấy một điểm $A(%s;%s) \in d$, với $D$ là ảnh $A$ lên đường thẳng $d'$. Suy ra $D$ có tọa độ là $(%s; %s)$\\" 
                 r"Vì $d'$ là ảnh của $d$ theo vectơ $\overrightarrow{u}$ có độ dài ngắn nhất. Nên độ dài của $\overrightarrow{u}$ chính là đoạn $AD$.\\"
                 r"Suy ra $\overrightarrow{u} = \overrightarrow{AD} = (%s ; %s)$.\\"
                 r"Vì $\left(\overrightarrow{u}; \overrightarrow{v} \right) = \dfrac{\pi}{4}$ nên "
                 r"$\cos \dfrac{\pi}{4} = \dfrac{\overrightarrow{u} \cdot \overrightarrow{v}}{\left| \overrightarrow{u} \right| \cdot \left| \overrightarrow{v} \right|}$. \hfill (1) \\"
                 r"Lấy điểm $C$ thuộc $d'$ sao cho $\overrightarrow{AC} = \overrightarrow{v}$, vì $C$ thuộc $d'$ nên $C(x_C; y_C) = (x_C ; %s)$."
                 r"Từ đó ta được $\overrightarrow{v} = (x_C - %s ; %s) $ \hfill (2)\\"
                 r"Từ (1) và (2) suy ra $\hoac{& \heva{& x_C = %s\\& y_C = %s} \\ & \heva{& x_C = %s\\& y_C = %s}} "
                 r"\Leftrightarrow \hoac{& v=(%s;%s) \\ &  v=(%s;%s)}$\\"
                 r"Theo giả thuyết thì $x_v > x_u$ nên  $v=(%s;%s)$}"
                 %(Diem[0][0], Diem[0][1], Diem[1][0], Diem[1][1],
                   u[0], u[1],
                   latex((-u[0] * x - c_CD)/u[1]),
                   Diem[0][0], latex((-u[0] * x - c_CD)/u[1] - Diem[0][1]),
                   Diem_C[0][0], Diem_C[0][1], Diem_C[1][0], Diem_C[1][1], Diem_C[0][0] - Diem[0][0], Diem_C[0][1] - Diem[0][1],
                   Diem_C[1][0] - Diem[0][0], Diem_C[1][1] - Diem[0][1],
                   v[0], v[1]) + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11Y3_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,4)
        de.write(r"\begin{ex}"+ os.linesep)
        if k == 0:
            de.write(r"Cho hình vuông $ABCD$, phép đối xứng trục $AC$ biến điểm $D$ thành điểm nào?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{$C$}" + os.linesep)
            de.write(r"{$A$}" + os.linesep)
            de.write(r"{\True $B$}" + os.linesep)
            de.write(r"{$D$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11Y4_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        ABCD = {'A': 'C', 'B': 'D', 'C': 'A', 'D': 'B'}
        MNPQ = {'M': 'P', 'N': 'Q', 'P': 'M', 'Q': 'N'}
        hv = random.choice([ABCD , MNPQ])
        print(hv.keys())
        print(hv.values())
#        k =
        de.write(r"\begin{ex}"+ os.linesep)
#        de.write(r"Cho hình vuông $%s$ tâm $O$, phép đối xứng tâm $O$ biến điểm $%s$ thành điểm nào?" % (hv, hv.get(k)) + os.linesep)
        de.write(r"\choice"+ os.linesep)
#        de.write(r"{\True $%s$}" % (hv[k]) + os.linesep)
        de.write(r"{$A$}" + os.linesep)
        de.write(r"{$B$}" + os.linesep)
        de.write(r"{$D$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11Y4_2():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,4)
        de.write(r"\begin{ex}"+ os.linesep)
        if k == 0:
            de.write(r"Cho hình vuông $ABCD$ tâm $O$, phép quay tâm $O$ góc quay $\dfrac{\pi}{2}$ biến điểm $B$ thành điểm nào?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{$C$}" + os.linesep)
            de.write(r"{\True $A$}" + os.linesep)
            de.write(r"{$B$}" + os.linesep)
            de.write(r"{$D$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11Y6_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,2)
        de.write(r"\begin{ex}"+ os.linesep)
        if k == 0:
            de.write(r"Cho hai đường tròn phân biệt có cùng bán kính $(O,R)$ và $(O',R)$. Phép vị tự tâm $I$ biến đường tròn $(O)$ thành đường tròn $(O')$ có tỉ số $k$ bằng" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{$1$}" + os.linesep)
            de.write(r"{\True $-1$}" + os.linesep)
            de.write(r"{$2$}" + os.linesep)
            de.write(r"{$\dfrac{1}{2}$}" + os.linesep)
        else:
            de.write(r"Cho hai đường tròn phân biệt có cùng bán kính $(O,R)$ và $(O',R)$. Phép vị tự tâm $I$ biến đường tròn $(O)$ thành đường tròn $(O')$. Khẳng định nào sau đây đúng?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True $\overrightarrow{IO'} = - \overrightarrow{IO}$}" + os.linesep)
            de.write(r"{$\overrightarrow{IO'} = \overrightarrow{IO}$}" + os.linesep)
            de.write(r"{$\overrightarrow{IO'} = 2\overrightarrow{IO}$}" + os.linesep)
            de.write(r"{$\overrightarrow{IO'} = \dfrac{1}{2}\overrightarrow{IO}$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11Y6_2():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        de.write(r"\begin{ex}"+ os.linesep)
        k = random.choice([-2,-1/2, -3, -1/3])
        print(k)
        inNumberint = int(k)
        if k == inNumberint:
            Goc = ['B','C','D']
            Anh = ['P','N','M','A']
        else:
            Goc = ['P','N','M']
            Anh = ['B','C','D','A']
        Diem_Goc = random.choice(Goc)
        z = Goc.index(Diem_Goc)
        Z = [0,1,2,3]
        de.write(r"\immini{Cho hình vuông $ABCD$ và $AMNP$ như hình vẽ. Biết rằng $A$, $B$, $P$ thẳng hàng và $AP = %s AB$. Tìm ảnh của điểm $%s$ qua phép vị tự tâm $A$ tỉ số $k = %s$."
                 % (latex(abs(k)), Diem_Goc,latex(k)) + os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True $%s$}" %(Anh[dc.check(z,Z)[0]]))
        de.write(r"{$%s$}" %(Anh[dc.check(z,Z)[1]]))
        de.write(r"{$%s$}" %(Anh[dc.check(z,Z)[2]]))
        de.write(r"{$%s$}" %(Anh[dc.check(z,Z)[3]]))
        de.write(r"}{" + os.linesep)
        de.write(r"\begin{tikzpicture}[scale=.3, line join=round, line cap=round]" + os.linesep)
        de.write(r"                \tkzDefPoints{0/0/A}" + os.linesep)
        de.write(r"                \tkzDefShiftPoint[A](90:2){B}" + os.linesep)
        de.write(r"                \tkzDrawSquare(A,B)\tkzGetPoints{C}{D}" + os.linesep)
        de.write(r"                \tkzDefShiftPoint[A](-90:2* %s ){P}" %(abs(k)) + os.linesep)
        de.write(r"                \tkzDrawSquare(A,P)\tkzGetPoints{N}{M}" + os.linesep)
        de.write(r"                \tkzDrawPoints[fill=black,size=4](A,B,C,D,M,N,P)" + os.linesep)
        de.write(r"                \tkzLabelPoints[above right](A,B,M)" + os.linesep)
        de.write(r"                \tkzLabelPoints[above left](C)" + os.linesep)
        de.write(r"                \tkzLabelPoints[below right](N)" + os.linesep)
        de.write(r"                \tkzLabelPoints[below left](D,P)" + os.linesep)
        de.write(r"            \end{tikzpicture}" + os.linesep)
        de.write(r"}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11K6_3():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        a = Symbol('a')
        b = Symbol('b')
        c = Symbol('c')
        xA = np.randint(-3,3)# tâm vị tự
        yA = np.randint(-3,3)
        k = random.choice([-2,2])
        HBH = dc.hambachai()
        while (xA == 0) and (yA == 0):
            xA = np.randint(-3,3)
            yA = np.randint(-3,3)
        xx = lambda x: k * (x - xA) + xA
        yy = lambda y: k * (y - yA) + yA
        fx = lambda x: HBH['a']*x**2 + HBH['b']*x + HBH['c']
        HeSo = solve_linear_system_LU(Matrix([
            [xx(0)**2, xx(0), 1, yy(fx(0))],
            [xx(1)**2, xx(1), 1, yy(fx(1))],
            [xx(2)**2, xx(2), 1, yy(fx(2))]]), [a, b, c])

        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"Trong mặt phẳng tọa độ $Oxy$, cho đường Parabol $(P)$ có phương trình $y = %s$. Phép vị tự tâm $A(%s; %s)$, tỉ số $k = %s$ biến đường Parabol $(P)$ thành đường Parabol $(P')$.\
                 Tìm phương trình của đường Parabol $(P')$."
                 % (latex(HBH['a']*x**2 + HBH['b']*x + HBH['c']), xA, yA, latex(k)) + os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True $y = %s$}" % (latex(HeSo[a]*x**2 + HeSo[b]*x + HeSo[c])) + os.linesep)
        de.write(r"{$y = %s$}" % (latex(-HeSo[a]*x**2 + HeSo[b]*x + HeSo[c])) + os.linesep)
        de.write(r"{$y = %s$}" % (latex(2*HeSo[a]*x**2 + HeSo[b]*x + 2*HeSo[c])) + os.linesep)
        de.write(r"{$y = %s$}" % (latex(-2*HeSo[a]*x**2 + HeSo[b]*x + 2*HeSo[c])) + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H11Y7_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,2)
        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"Trong các khẳng định sau, khẳng định nào đúng?" + os.linesep)
        de.write(r"\choice"+ os.linesep)
        if k == 0:
            de.write(r"{\True Hợp thành của một phép vị tự và một phép tịnh tiến biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
            de.write(r"{Hợp thành của một phép vị tự và một phép đối xứng trục biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
            de.write(r"{Hợp thành của một phép vị tự và một phép quay biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
            de.write(r"{Hợp thành của một phép vị tự và một phép dời hình biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
        else:
            de.write(r"{\True Hợp thành của một phép vị tự và một phép đối xứng tâm biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
            de.write(r"{Hợp thành của một phép vị tự và một phép đối xứng trục biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
            de.write(r"{Hợp thành của một phép vị tự và một phép quay biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
            de.write(r"{Hợp thành của một phép vị tự và một phép dời hình biến đường thẳng thành đường thẳng song song hoặc trùng với đường thẳng đó}"  + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)



def H11G7_2():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        a = Symbol('a')
        b = Symbol('b')
        c = Symbol('c')
        xI = np.randint(-3,3) # Tâm đường tròn
        yI = np.randint(-3,3)
        R = np.randint(2,9)
        xx = lambda x: k * (x - xA) + xA
        yy = lambda y: k * (y - yA) + yA
        fx = lambda x: HBH['a']*x**2 + HBH['b']*x + HBH['c']
        HeSo = solve_linear_system_LU(Matrix([
            [xx(0)**2, xx(0), 1, yy(fx(0))],
            [xx(1)**2, xx(1), 1, yy(fx(1))],
            [xx(2)**2, xx(2), 1, yy(fx(2))]]), [a, b, c])

        de.write(r"\begin{ex}"+ os.linesep)
 #       de.write(r"Trong mặt phẳng $Oxy$, cho điểm $A(a ; b)$ $(a + b > 0)$ thuộc đường tròn $(\mathscr C) \colon (%s)^2 + (%s)^2 = %s$. Dựng điểm $B$ bên ngoài đường tròn sao cho tam giác $OAB$ vuông cân tại $B$." + os.linesep
 #                r" Khi đó điểm $B$ thuộc đường tròn $(\mathscr C') \colon (x + a)^2 + (y + b)^2 = r^2$. Tính $a + b$."
 #                % (latex(HBH['a']*x**2 + HBH['b']*x + HBH['c']), xA, yA, latex(k)) + os.linesep)
 #       de.write(r"\choice"+ os.linesep)
 #       de.write(r"{\True $y = %s$}" % (latex(HeSo[a]*x**2 + HeSo[b]*x + HeSo[c])) + os.linesep)
 #       de.write(r"{$y = %s$}" % (latex(-HeSo[a]*x**2 + HeSo[b]*x + HeSo[c])) + os.linesep)
 #       de.write(r"{$y = %s$}" % (latex(2*HeSo[a]*x**2 + HeSo[b]*x + 2*HeSo[c])) + os.linesep)
  #      de.write(r"{$y = %s$}" % (latex(-2*HeSo[a]*x**2 + HeSo[b]*x + 2*HeSo[c])) + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)



def H11K7_3():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(2,4)
        LamTron = {'trăm': 2, 'nghìn': 3}
        i = random.choice(['trăm', 'nghìn'])
        ### thuật toán: từ 2 cạnh và 1 góc (để tam giác ra hợp lí, ko bị lỗi, nếu chọn 3 cạnh dễ bị tình traạng tổng 2 cạnh nhỏ hơn cạnh còn lại)
        # tìm cạnh thứ 3, sau đó tìm ra đưuòng trung tuyến, Rồi lấy phần nguyên của đường trung tuyến để ra đề cho đẹp. Nên góc lấy từ đầu ko còn đúng nữa.
        # Từ phần nguyên của đường trung tuyến tìm cạnh thứ 3 theo phần nguyên đó.
        A = random.choice([math.pi/6, math.pi/4, math.pi/3, math.pi * 2/3, math.pi * 5/6])
        nguyen = 1
        AC = 1
        AB = 1
        while (nguyen == AB) or (nguyen == AC):
            AB = np.randint(3, 9)
            AC = np.randint(3, 9)
            if AC == AB:
                AC = np.randint(3, 9)

            a = lambda a,b,A: sqrt(a**2 + b**2 - 2*a*b*math.cos(A)) # cạnh theo định lí cos
            DuongTrungTuyen_a = lambda a,b,c: sqrt((b**2 + c**2)/2 - a**2/4) # đường trung tuyến
            nguyen, le = divmod(DuongTrungTuyen_a(a(AB,AC,A),AB,AC),1)# tách lấy phần nguyên của đường trung tuyến, để ra đề tròn số
            aa = lambda ma,b,c: math.sqrt(2*(b**2 + c**2) - 4*ma**2) # cạnh theo trung tuyến
            BC = aa(nguyen,AB,AC)
        S = lambda a,b,c: math.sqrt(dc.sum([a,b,c])/2 * ((dc.sum([a,b,c])/2) - a) * ((dc.sum([a,b,c])/2) - b) * ((dc.sum([a,b,c])/2) - c)) #công thức Heroong

        z = round(k**2*S(AB,AC,BC),LamTron[i])
        Z = [round(k**2*S(AB,AC,BC),LamTron[i]), round(k**2*S(AB,AC,BC),LamTron[i]+1), round(k*S(AB,AC,BC),LamTron[i]), round(k*S(AB,AC,BC),LamTron[i]+1)]
        print(AB,AC,BC,nguyen,A,S(AB,AC,BC),k**2*S(AB,AC,BC),k)
        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"Cho tam giác $ABC$ có $AB = %s$, $AC = %s$, và đường trung tuyến ứng với cạnh $BC$ bằng $%s$. Phép đồng dạng tỉ số $k = %s$  biến $A$  thành  $A'$, biến  $B$ thành  $B'$, biến  $C$ thành  $C'$. "
                 r"Khi đó diện tích tam giác $A'B'C'$ bằng bao nhiêu? "
                 r"(Hãy viết giá trị gần đúng của diện tích chính xác đến hàng phần %s)."
                 % (AB, AC, nguyen, k, i) + os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True $%s$}" %(dc.check(z,Z)[0]) + os.linesep)
        de.write(r"{$%s$}" %(dc.check(z,Z)[1]) + os.linesep)
        de.write(r"{$%s$}" %(dc.check(z,Z)[2]) + os.linesep)
        de.write(r"{$%s$}" %(dc.check(z,Z)[3]) + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)

#31	Nhận biết: Phép dời hình
#H11Y_1()
#32	Nhận biết: Phép dời hình
#H11Y_3()
#33	Nhận biết: Tìm ảnh qua phép dời hình
#đã có
#34	Nhận biết: Tìm ảnh qua phép vị tự
#H11Y6_2()
#35	Thông hiểu: Tìm ảnh qua phép đống dạng
#H11Y7_1(1)
#36	Thông hiểu : Phép dời hình
#H11B_2()
#37	Thông hiểu: Phép vị tự
#H11Y_7()
#38	Vận dụng: Phép vị tự
#H11Y6_3()
#39	Vận dụng : Phép dời hình
#H11K7_3()
#40	Vận dụng cao: Phép dời hình
H11G2_2()
