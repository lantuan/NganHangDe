
# QUY TẮC CHUNG
- Dùng UTF-8
- Dùng $$ thay cho \[
- Dùng $ thay cho \(
- Không đổi môi trường
- Không đổi cấu trúc đề

---

# MÔI TRƯỜNG BÀI TẬP
Mọi bài dùng:
\begin{ex}
...
\end{ex}

---

# LỜI GIẢI
Mọi bài đều bắt buộc có:
\loigiai{
...
}

---

# TRẮC NGHIỆM NHIỀU LỰA CHỌN

## Format
\begin{ex}%[NB]
...
\choice
{A}
{\True B}
{C}
{D}
\loigiai{
...
}
\end{ex}

## Quy tắc
- Chỉ đáp án đúng dùng \True
- Đúng 4 đáp án
- Không dùng enumerate

---

# PHẦN ĐÚNG SAI

## Format chuẩn
\begin{ex}%[TH]
Xét tính đúng sai của các mệnh đề sau:
\choiceTF
{\True Mệnh đề A}
{Mệnh đề B}
{\True Mệnh đề C}
{Mệnh đề D}
\loigiai{
...
}
\end{ex}

## Ghi chú quan trọng
Môi trường \choiceTF tự động sinh nhãn a), b), c), d).
AI KHÔNG được tự viết thêm nhãn vào nội dung.

Sai:
{\True a) Mệnh đề A}

Đúng:
{\True Mệnh đề A}

## Cấu trúc bắt buộc
Mỗi câu đúng sai gồm đúng 4 ý.
Không được thiếu ý, không được thừa ý.

## Quan hệ giữa các ý
Các ý phải liên kết logic theo cấu trúc:
- Ý a) : Khởi tạo dữ kiện
- Ý b) : Khai thác dữ kiện hoặc Khởi tạo dữ kiện 2
- Ý c) : Vận dụng dữ kiện
- Ý d) : Tổng hợp nâng cao

Không được tạo 4 ý độc lập, rời rạc.

## Yêu cầu ý d)
Ý d) bắt buộc sử dụng dữ kiện từ a), b), c).
Ý d) là ý tổng hợp cuối cùng.

## Quy tắc đúng sai
Không được:
- Cả 4 ý đều đúng
- Cả 4 ý đều sai

---

# PHẦN TRẢ LỜI NGẮN

## Format
\begin{ex}%[VD]
...
\shortans{$1,5$}
\loigiai{
...
}
\end{ex}

## Quy tắc đáp án
Đáp án phải là số thực.
Độ dài tối đa: 4 ký tự.
Các ký tự cho phép: - , 0 1 2 3 4 5 6 7 8 9

Hợp lệ  : 2 / -3 / 1,5 / 0,25
Không hợp lệ: 12345 / \frac{1}{2} / sqrt2 / x=2

## Ví dụ hoàn chỉnh
\begin{ex}%[VD]
Cho hàm số $f(x) = 2x + 1$. Tính $f(0{,}25)$.
\shortans{$1,5$}
\loigiai{
$f(0{,}25) = 2 \cdot 0{,}25 + 1 = 0{,}5 + 1 = 1{,}5$
}
\end{ex}

\begin{ex}%[VD]
Cho hàm số $f(x) = 2x + 1$. Tính $f\left( \dfrac{1}{3} \right)$. (Làm tròn kết quả đến hàng phần trăm)
\shortans{$1,67$}
\loigiai{
$f\left( \dfrac{1}{3} \right) = 2 \cdot \dfrac{1}{3} + 1 \approx 1{,}67$
}
\end{ex}

---

# TỰ LUẬN

## Format
\begin{ex}%[VDC]
...
\loigiai{
...
}
\end{ex}

## Quy tắc đáp án
Phải chia barem điểm. 
Mỗi câu tự luận 1 điểm.
Ý nhỏ nhất 0.25 điểm.

## Ví dụ hoàn chỉnh

\begin{ex}%[TH]
    Trong mặt phẳng tọa độ $Oxy$, cho parabol $(P)$ có phương trình chính tắc là $y^2 = 16x$. Với $M(x_M; y_M)$ là điểm thuộc parabol $(P)$. Tính độ dài đoạn thẳng $MF$, với $x_M = 1$. 
    \loigiai{
    Parabol $(P)$ có dạng $y^2 = 2px$ nên $2p = 16 \Rightarrow p = 8$. \dotfill 0.25 điểm

    Suy ra: Tiêu điểm $F\left(\dfrac{p}{2};0\right) = (4;0)$. Đường chuẩn $\Delta: x = -\dfrac{p}{2} = -4$. \dotfill 0.25 điểm

    Với $M \in (P)$ thì $MF = d(M,\Delta)$. \dotfill 0.25 điểm

    Do $x_M = 1$ nên:
    $$
    MF = d(M,\Delta) = |1 - (-4)| = 5.
    $$

    Vậy $MF = 5$. \dotfill 0.25 điểm\\

    \textbf{Cách 2.} Parabol $(P)$ có dạng $y^2 = 2px$ nên $2p = 16 \Rightarrow p = 8$. \dotfill 0.25 điểm

    Suy ra tiêu điểm $F\left(\dfrac{p}{2};0\right) = (4;0)$. \dotfill 0.25 điểm

    Với $x_M = 1$, ta có:
    $$y_M^2 = 16 \Rightarrow y_M = \pm 4.$$

    Do đó $M(1;\pm 4)$. \dotfill 0.25 điểm

    Khi đó:
    $$
    MF = \sqrt{(1 - 4)^2 + (\pm 4)^2}
    = \sqrt{9 + 16} = 5.
    $$

    Vậy $MF = 5$. \dotfill 0.25 điểm
    }
\end{ex}


---

# KÝ HIỆU ĐẶC BIỆT

## Hệ phương trình
Dùng:
\heva{
  & phương trình 1 \\
  & phương trình 2 \\
...
}

Không dùng:
\begin{cases}

## Tuyển
Dùng:
\hoac{
  & phương trình 1 \\
  & phương trình 2 \\
...
}

## Tập rỗng
Dùng: \varnothing

## Góc
Dùng: ^{\circ}
Không dùng: ^0

## Dấu ba chấm
Dùng: \ldots

## Phân số
- Display : \dfrac{...}{...}
- Inline  : \frac{...}{...}

## Căn thức
Dùng: \sqrt{...} hoặc \sqrt[n]{...}
Ví dụ: \sqrt{2}, \sqrt[3]{x}

---

# LIỆT KÊ
## Liệt kê bài tập ý a), b), ...
Dùng:
\begin{enumerate}[a)]
...
\end{enumerate}

Không dùng:
\begin{itemize}

## Liệt kê các ý nhỏ
Dùng:
\begin{itemize}
...
\end{itemize}

Không dùng:
- ... \\
- ...
- 

---

# HÌNH VẼ
Nếu bài cần hình vẽ, dùng TikZ:
\begin{tikzpicture}
...
\end{tikzpicture}

Không dùng:
- \includegraphics nếu không có file ảnh
- Mô tả hình bằng text thay cho hình thật
