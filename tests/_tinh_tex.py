# -*- coding: utf-8 -*-
r"""Đọc biểu thức LaTeX trong đề (dạng hẹp dùng ở ngân hàng đề) thành biểu thức Python để TÍNH LẠI ĐỘC LẬP đáp số.

Không dùng lại hàm sinh đề, không cần thư viện ngoài (sympy.parse_latex cần antlr). Hỗ trợ:
  \dfrac{..}{..}, \frac, \sqrt{..}, \left( \right), \left| \right|, ^{2}, ^{\circ}, \cdot, \sin \cos \tan \cot,
  \alpha, m_{a} / m_a, h_a, \overrightarrow{XY} (điểm), \overrightarrow{a} (vectơ tự do), \overrightarrow{0},
  nhân ngầm (2bc, 3\overrightarrow{a}, k\left(..\right)), số thập phân dấu phẩy.
Vectơ là đối tượng V (x, y): V + V, V - V, số * V, V * V = TÍCH VÔ HƯỚNG, V ** 2 = bình phương vô hướng, abs(V) = độ dài.

CLAUDE THEM 15/10/2026 - dung cho tests/test_l10_c3_sa_bo_sung.py, tests/test_l10_c4_sa_bo_sung.py.
"""
import math
import re


class V:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)

    def __add__(self, o):
        if isinstance(o, (int, float)) and o == 0:
            return self
        return V(self.x + o.x, self.y + o.y)

    __radd__ = __add__

    def __sub__(self, o):
        if isinstance(o, (int, float)) and o == 0:
            return self
        return V(self.x - o.x, self.y - o.y)

    def __rsub__(self, o):
        return V(-self.x, -self.y) if (isinstance(o, (int, float)) and o == 0) else NotImplemented

    def __neg__(self):
        return V(-self.x, -self.y)

    def __pos__(self):
        return self

    def __mul__(self, o):
        if isinstance(o, V):
            return self.x * o.x + self.y * o.y
        return V(self.x * o, self.y * o)

    def __rmul__(self, k):
        return V(self.x * k, self.y * k)

    def __truediv__(self, k):
        return V(self.x / k, self.y / k)

    def __pow__(self, n):
        assert n == 2
        return self * self

    def __abs__(self):
        return math.hypot(self.x, self.y)


def bang(u, v, eps=1e-7):
    """So sánh hai giá trị (số hoặc vectơ; vectơ-không viết là số 0)."""
    if isinstance(u, V) or isinstance(v, V):
        u = u if isinstance(u, V) else V(0, 0)
        v = v if isinstance(v, V) else V(0, 0)
        return abs(u - v) < eps
    return abs(u - v) < eps * max(1.0, abs(u), abs(v))


def _ngoac(s, i):
    """s[i] == '{' -> vị trí '}' tương ứng."""
    assert s[i] == "{", (s, i)
    d = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                return j
    raise ValueError(s)


def _bo_lenh(s):
    """\\dfrac, \\sqrt, ^{..}, \\overrightarrow -> cú pháp Python (đệ quy theo ngoặc nhọn)."""
    ra = ""
    i = 0
    while i < len(s):
        if s.startswith(r"\dfrac", i) or s.startswith(r"\frac", i):
            i += 6 if s.startswith(r"\dfrac", i) else 5
            j = _ngoac(s, i)
            k = _ngoac(s, j + 1)
            ra += "((%s)/(%s))" % (_bo_lenh(s[i + 1:j]), _bo_lenh(s[j + 2:k]))
            i = k + 1
        elif s.startswith(r"\sqrt", i):
            i += 5
            j = _ngoac(s, i)
            ra += " sqrt(%s)" % _bo_lenh(s[i + 1:j])
            i = j + 1
        elif s.startswith(r"\overrightarrow", i):
            i += len(r"\overrightarrow")
            j = _ngoac(s, i)
            ten = s[i + 1:j]
            if ten == "0":
                ra += " 0 "
            elif len(ten) == 2 and ten.isupper():
                ra += " (P['%s']-P['%s']) " % (ten[1], ten[0])
            else:
                ra += " W['%s'] " % ten
            i = j + 1
        elif s.startswith("^{", i):
            j = _ngoac(s, i + 1)
            ra += "**(%s)" % _bo_lenh(s[i + 2:j])
            i = j + 1
        else:
            ra += s[i]
            i += 1
    return ra


_HAM = ("sqrt", "sin", "cos", "tan", "cot", "abs")
_TEN_DAI = ("sqrt", "sin", "cos", "tan", "cot", "abs", "pi", "al", "ma", "mb", "mc", "ha", "hb", "hc")


def sang_python(tex):
    """LaTeX -> chuỗi biểu thức Python (biến: một chữ cái, al = alpha, ma, ha, P[...], W[...])."""
    s = tex.replace("$", "")
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)                     # số thập phân dấu phẩy
    s = re.sub(r"(\d+(?:\.\d+)?)\^\{\\circ\}", r"(\1*pi/180)", s)
    s = re.sub(r"m_\{([abc])\}|m_([abc])", lambda m: "m" + (m.group(1) or m.group(2)), s)
    s = re.sub(r"h_\{([abc])\}|h_([abc])", lambda m: "h" + (m.group(1) or m.group(2)), s)
    s = s.replace(r"\left|", " abs(").replace(r"\right|", ")")
    s = s.replace(r"\left(", "(").replace(r"\right)", ")").replace(r"\left[", "(").replace(r"\right]", ")")
    s = s.replace(r"\cdot", "*").replace(r"\,", " ").replace(r"\ ", " ").replace(r"\alpha", " al ")
    s = s.replace(r"\times", "*")
    s = _bo_lenh(s)
    for h in ("sin", "cos", "tan", "cot"):
        s = s.replace("\\" + h, " " + h + " ")
    assert "\\" not in s, (tex, s)
    # tách từ tố
    tok = re.findall(r"P\['[A-Z]'\]|W\['[a-z]'\]|\d+(?:\.\d+)?|[A-Za-z]+|\*\*|[-+*/()]", s)
    t2 = []
    for t in tok:
        if re.fullmatch(r"[A-Za-z]+", t) and t not in _TEN_DAI:
            t2 += list(t)                                       # bc -> b c
        else:
            t2.append(t)
    # hàm không có ngoặc: sin A, cos (..) -> sin(A)
    ra = []
    i = 0
    while i < len(t2):
        t = t2[i]
        if t in ("sin", "cos", "tan", "cot") and i + 1 < len(t2) and t2[i + 1] != "(":
            ra += [t, "(", t2[i + 1], ")"]
            i += 2
            continue
        ra.append(t)
        i += 1
    # nhân ngầm
    out = []
    for t in ra:
        if out:
            a = out[-1]
            trai = a == ")" or re.fullmatch(r"\d+(?:\.\d+)?", a) or (re.fullmatch(r"[A-Za-z]+|P\[.*\]|W\[.*\]", a) and a not in _HAM)
            phai = t == "(" or re.fullmatch(r"\d+(?:\.\d+)?", t) or re.fullmatch(r"[A-Za-z]+|P\[.*\]|W\[.*\]", t)
            if trai and phai:
                out.append("*")
        out.append(t)
    return " ".join(out)


MOI_TRUONG = dict(sin=math.sin, cos=math.cos, tan=math.tan, cot=lambda t: 1 / math.tan(t), sqrt=math.sqrt, abs=abs, pi=math.pi)


def tinh(tex, **bien):
    return eval(sang_python(tex), {"__builtins__": {}}, dict(MOI_TRUONG, **bien))


def so(chuoi):
    """'-0,25' -> -0.25"""
    return float(str(chuoi).replace("$", "").replace(",", ".").strip())
