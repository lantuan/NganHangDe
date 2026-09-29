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



def H12Y1_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,1)
        if k == 0:
            m = 0.5
            Diem_D = 'D'
            n = 0.8
            Diem_N = 'N'
        else:
            m = 0.8
            Diem_D = 'B'
            n = 0.5
            Diem_N = 'M'

        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"\immini{Cho tứ diện $ABCD$, các điểm $M$, $N$ nằm trên các cạnh $AB$, $AD$ (như hình vẽ bên). "
                     r"Đường thẳng $MN$ \textbf{không} cắt mặt phẳng nào trong các mặt phẳng sau?" + os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True $(ABD)$}" + os.linesep)
        de.write(r"{$(ABC)$}" + os.linesep)
        de.write(r"{$(BCD)$}" + os.linesep)
        de.write(r"{$(ACD)$}}" + os.linesep)
        de.write(r"{{\qquad \begin{tikzpicture}[line width=0.8pt, scale=0.5]" + os.linesep)
        de.write(        r"\tkzDefPoints{0/5/A, -2/0/B,-.5/-1/C,4/0/D}" + os.linesep)
        de.write(        r"\coordinate (M) at ($(A)!%s!(B)$);" %(m) + os.linesep)
        de.write(        r"\coordinate (N) at ($(A)!%s!(D)$);" %(n) + os.linesep)
        de.write(        r"\tkzInterLL(M,N)(B,D) \tkzGetPoint{P}" + os.linesep)
        de.write(        r"\draw (A)--(B)--(C)--(D)--(A)--(C) (%s)--(P)--(%s);" %(Diem_N, Diem_D)+ os.linesep)
        de.write(        r"\draw [dashed] (B)--(D) (M)--(N);" + os.linesep)
        de.write(        r"\draw (A) circle (1.5pt) node[above] {$A$} (B) node[below left] {$B$} (C) node[below] {$C$} (D) node[below] {$D$} ")
        de.write(        r"(M) node[above left] {$M$} (N) node[above right] {$N$} (P) node[below] {$P$};" + os.linesep)
        de.write(        r"\end{tikzpicture}}}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H12Y2_1():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
#        k = np.randint(0,1)

        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"Cho ba đường thẳng phân biệt $a,b,c$ trong đó $a\parallel b$. Mệnh đề nào dưới đây đúng?" + os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True Nếu $c \parallel a$ thì $c\parallel b$}" + os.linesep)
        de.write(r"{Nếu $c$ cắt $a$ thì $c$ cắt $b$}" + os.linesep)
        de.write(r"{Nếu $c$ và $a$ chéo nhau thì $c$ và $b$ chéo nhau}" + os.linesep)
        de.write(r"{Nếu $c$ cắt $a$ thì $c$ và $b$ chéo nhau}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H12Y2_2():
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
        k = np.randint(0,1)
        if k == 0:
            mp = 'ACD'
            dt = 'BD'
            dt_sai1 = 'AD'
            dt_sai2 = 'CD'

        else:
            mp = 'ABD'
            dt = 'CD'
            dt_sai1 = 'AB'
            dt_sai2 = 'BD'

        de.write(r"\begin{ex}"+ os.linesep)
        de.write(r"Cho tứ diện $ABCD$. Gọi $M$, $N$ lần lượt là trọng tâm của tam giác $ABC$ và $%s$. Khi đó, khẳng định nào dưới đây đúng?"
                 % (mp)+ os.linesep)
        de.write(r"\choice"+ os.linesep)
        de.write(r"{\True $MN \parallel %s$}" %(dt) + os.linesep)
        de.write(r"{$MN$ cắt $%s$}" % (dt_sai1) + os.linesep)
        de.write(r"{$MN \parallel %s$}" % (dt_sai2) + os.linesep)
        de.write(r"{$MN$ cắt $BC$}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)


def H12Y3_1(k):
    with open(r"latex\data\de.tex","a",encoding='utf-8') as de:
#        k = np.randint(0,1)
        de.write(r"\begin{ex}"+ os.linesep)
        if k == 0:
            de.write(r"Chọn khẳng định đúng trong các khẳng định sau?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True Đường thẳng $\Delta \parallel (P)$ thì tồn tại đường thẳng $\Delta'$ nằm trong $(P)$ để $\Delta \parallel \Delta'$}" + os.linesep)
            de.write(r"{Hai đường thẳng phân biệt cùng song song với  một mặt phẳng thì song song với nhau}" + os.linesep)
            de.write(r"{Nếu đường thẳng $a$ nằm trong $(P)$ và $(P) \parallel \Delta$ thì $a \parallel \Delta$}" + os.linesep)
            de.write(r"{Nếu đường thẳng $\Delta \parallel (P)$ và $(P)$ cắt đường thẳng $a$ thì hai đường thẳng $a$ và $\Delta$ cắt nhau}" + os.linesep)
        else:
            de.write(r"Cho mặt phẳng $(P)$ và hai đường thẳng $a$, $b$ với $a$ song song $(P)$. Chọn mệnh đề đúng trong các mệnh đề sau?" + os.linesep)
            de.write(r"\choice"+ os.linesep)
            de.write(r"{\True Nếu $b$ nằm trong $(P)$ thì $a$ và $ b$ không có điểm chung}" + os.linesep)
            de.write(r"{Nếu $b$ nằm trong $(P)$ thì $a \parallel b$}" + os.linesep)
            de.write(r"{Nếu $b$ nằm trong $(P)$ thì $a$ và $b$ chéo nhau}" + os.linesep)
            de.write(r"{Nếu $b$ nằm trong $(P)$ thì $a $ và $ b$ cắt nhau}" + os.linesep)
        de.write(r"\loigiai{}" + os.linesep)
        de.write(r"\dotlineEX{5}"+ os.linesep)
        de.write(r"\end{ex}"+ os.linesep)

#41	Nhận biết: Đại cương về đường thẳng và mặt phẳng
#H12Y1_1(1)
#42	Nhận biết: Hai đường thẳng song song
#H12Y2_1()
#43	Nhận biết: Hai đường thẳng song song

#44	Nhận biết: Đường thẳng song song mặt phẳng
#H12Y3_1(1)
#45	Thông hiểu: Thiết diện
#46	Thông hiểu: Đường thẳng song song mặt phẳng
#47	Thông hiểu: Hai đường thẳng song song
#H12Y2_2(1)
#48	Vận dụng: giao tuyến của hai mặt phẳng
#49	Vận dụng: Đường thẳng song song mặt phẳng
#50	Vận dụng cao : Thiết diện

