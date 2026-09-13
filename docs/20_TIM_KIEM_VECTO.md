# TÌM KIẾM VECTO (EMBEDDING) CHO NGÂN HÀNG ĐỀ

Version: 1.0 — 2026-09-13

Trạng thái

🟡 Đánh giá + lộ trình (CHƯA triển khai)

---

# 0. Kết luận ngắn — đọc mục này trước

Ba câu trả lời cho ba câu hỏi đã đặt ra:

1. **Có tiết kiệm token không?** KHÔNG, với luồng hiện tại. Luồng chọn câu
   của hệ thống này không gọi AI lần nào (xem docs/09), nên không có token
   nào để tiết kiệm ở đó. Thêm vecto còn LÀM TỐN THÊM token (mỗi lần tìm
   kiếm phải gọi model nhúng một lần).

2. **Có dễ quản lý ngân hàng lớn hơn không?** Có, nhưng KHÔNG phải nhờ vecto.
   Việc quản lý ngân hàng lớn được giải bằng CHỈ MỤC (index) và bộ dò trùng —
   xem Giai đoạn 0, làm được ngay, không cần vecto.

3. **Có khả thi với người không chuyên tin học không?** Có, ở mức Giai đoạn 1,
   vì Supabase đang dùng sẵn có pgvector — không phải dựng thêm máy chủ nào.
   Nhưng chỉ nên làm SAU khi xong tài khoản giáo viên và sinh nhiều mã đề.

**Thứ tự ưu tiên đề nghị:** Tài khoản giáo viên → Sinh nhiều mã đề →
Giai đoạn 0 (chỉ mục + dò trùng) → mở rộng ngân hàng sang chương 2, 3 →
Giai đoạn 1 (vecto) khi ngân hàng vượt khoảng 500 mã câu hỏi.

---

# 1. Vecto ở đây nghĩa là gì

Nói bằng ngôn ngữ toán: một mô hình nhúng (embedding model) là một ánh xạ

```
f : (đoạn văn bản)  ->  R^n        (n thường là 768, 1024 hoặc 1536)
```

sao cho hai đoạn văn bản gần nhau về NGHĨA thì hai vecto ảnh gần nhau về
khoảng cách. Độ giống nhau đo bằng cô-sin góc giữa hai vecto:

```
sim(u, v) = (u . v) / (|u| * |v|)      thuộc [-1, 1]
```

"Tìm kiếm vecto" = nhúng câu truy vấn thành vecto q, rồi tìm trong kho những
vecto v có sim(q, v) lớn nhất.

Điểm mạnh: tìm được cả khi dùng từ khác ("xét dấu tam thức" vẫn ra câu ghi là
"bảng xét dấu của f(x) = ax^2+bx+c").

Điểm yếu, và là điểm quyết định với hệ thống này: kết quả là GẦN ĐÚNG và có
thứ hạng, KHÔNG phải đúng/sai tuyệt đối.

---

# 2. Vì sao KHÔNG dùng vecto cho luồng chọn câu hiện tại

Bốn lý do, theo đúng thứ tự quan trọng:

1. **Ngân hàng này đã có khóa chính xác.** Mỗi câu hỏi có một Generator ID
   (docs/04) mã hóa đủ lớp, chương, bài, mức độ, loại câu. Tra theo ID là tra
   từ điển: chính xác 100%, thời gian gần như bằng 0, không tốn token. Vecto
   sinh ra để giải bài toán "không có khóa"; ở đây khóa đã có sẵn.

2. **Ma trận đề đòi hỏi ĐÚNG, không phải GẦN ĐÚNG.** Blueprint yêu cầu "1 câu
   mức Thông hiểu, bài 1, loại trắc nghiệm". Tra ID cho đúng một câu như vậy.
   Tìm vecto cho ra câu "giống nhất" — có thể lệch mức độ hoặc lệch bài, và
   khi đó ma trận đề sai mà không ai biết. Đây là đúng loại lỗi mà nguyên tắc
   "Ưu tiên Code hơn AI" (docs/00) được đặt ra để tránh.

3. **Không lặp lại được.** Cùng một yêu cầu, tìm vecto có thể cho kết quả khác
   nhau khi kho thay đổi. Đề kiểm tra lấy điểm cần tính tái lập.

4. **Nội dung câu hỏi chưa tồn tại lúc chọn.** Câu hỏi ở đây là HÀM SINH, văn
   bản chỉ ra đời khi gọi hàm với số liệu ngẫu nhiên. Muốn nhúng thì phải nhúng
   một bản đại diện sinh sẵn — tức là nhúng cái bóng của câu hỏi, không phải
   câu hỏi.

Kết luận: giữ nguyên tra ID cho luồng sinh đề. Vecto, nếu làm, là một lớp
TÌM KIẾM PHỤ đặt bên cạnh, không thay thế.

---

# 3. Ba chỗ vecto thực sự có ích

| # | Chỗ dùng | Vì sao cần vecto | Khi nào đáng làm |
|---|---|---|---|
| 1 | Ô tìm kiếm câu hỏi cho giáo viên: gõ "câu về xét dấu tam thức bậc hai mức vận dụng" và nhận danh sách mã câu hỏi phù hợp | Giáo viên không thuộc mã ID; tìm theo từ khóa thường sẽ trượt vì cách diễn đạt khác nhau | Khi ngân hàng > ~500 mã câu hỏi |
| 2 | Dò câu hỏi trùng nghĩa khi nhiều giáo viên cùng đóng góp | Hai người viết cùng một dạng toán bằng hai cách diễn đạt, so sánh chữ không phát hiện được | Khi có từ 3 người trở lên cùng viết |
| 3 | Gia sư AI trả lời học sinh dựa trên tài liệu của chính giáo viên (RAG) | Đây mới đúng là bài toán vecto sinh ra để giải | Giai đoạn sau, sau khi xong CHV_Analyzer |

Ba việc này đều thuộc phần GIÁO VIÊN và phần GIA SƯ — tức là hướng phát triển,
không phải luồng đang chạy.

---

# 4. Giai đoạn 0 — Làm ngay, không cần vecto

Đây mới là câu trả lời thật cho "dễ quản lý khi ngân hàng lớn". Ba việc, mỗi
việc là một script Python ngắn, chạy được ngay hôm nay.

## 4.1. Chỉ mục ngân hàng (bank index)

Quét toàn bộ `data/python_bank/`, sinh ra một tệp JSON liệt kê mọi hàm sinh
kèm thông tin suy ra từ ID.

```
scripts/tao_chi_muc_ngan_hang.py   ->   data/config/bank_index.json
```

Mỗi dòng gồm: generator_id, biến thể (_01, _02...), lớp, chương, bài, mức độ,
loại câu, tên tệp, số dòng. Từ chỉ mục này trả lời được ngay các câu hỏi mà
hiện nay phải mở từng tệp ra đếm:

- Bài nào, mức độ nào đang THIẾU hàm sinh (chính là nguồn gốc của dòng
  "[THIẾU CÂU HỎI]" trong đề).
- Mã nào có trong Mapping nhưng chưa có hàm Python, và ngược lại.
- Mỗi bài hiện có bao nhiêu câu ở mỗi mức độ.

Lợi ích: khi ngân hàng lên vài nghìn câu, đây là thứ giữ cho nó không loạn.
Chi phí: một buổi làm, không tốn token, không phụ thuộc dịch vụ ngoài.

## 4.2. Bộ dò trùng bằng so sánh chữ

Gọi mỗi hàm sinh một lần với hạt ngẫu nhiên cố định, chuẩn hóa kết quả (bỏ
số, bỏ khoảng trắng thừa, bỏ lệnh LaTeX) rồi so sánh từng cặp bằng
`difflib.SequenceMatcher`. Cặp nào giống trên 90% thì in ra để xem lại.

Ở quy mô vài nghìn câu, cách này đủ dùng và KHÔNG cần vecto.

## 4.3. Kiểm thử phủ ma trận

Mở rộng bộ kiểm thử hiện có: với mỗi loại bài kiểm tra và mỗi chương, thử dựng
blueprint và kiểm tra có đủ câu cho mọi ô của ma trận không. Chạy trước mỗi
lần phát hành.

---

# 5. Giai đoạn 1 — Tìm kiếm vecto cho giáo viên

Chỉ làm khi đã xong Giai đoạn 0 và ngân hàng đã vượt khoảng 500 mã câu hỏi.

## 5.1. Vì sao dùng pgvector trên Supabase

Hệ thống đã dùng Supabase, mà Supabase là PostgreSQL có sẵn tiện ích mở rộng
`pgvector`. Nghĩa là KHÔNG phải dựng thêm máy chủ nào, không phải học thêm một
dịch vụ nào, không phải trả thêm tiền hạ tầng. Đây là lý do chính khiến việc
này khả thi với một giáo viên không chuyên tin học.

## 5.2. Bước 1 — Bật pgvector và tạo bảng

Vào Supabase > SQL Editor, chạy:

```sql
create extension if not exists vector;

create table cau_hoi_vecto (
  generator_id  text primary key,
  lop           int  not null,
  chuong        int  not null,
  bai           int,
  muc_do        text not null,          -- NB / TH / VD / VDC
  loai_cau      text not null,          -- MC / TF / SA / TL
  van_ban_mau   text not null,          -- ban sinh san de nhung
  nhung         vector(1024),           -- so chieu tuy model, xem 5.3
  cap_nhat_luc  timestamptz default now()
);

create index on cau_hoi_vecto using ivfflat (nhung vector_cosine_ops)
  with (lists = 100);
```

Lưu ý quan trọng: các cột `lop, chuong, bai, muc_do, loai_cau` được giữ lại
NGUYÊN VẸN bên cạnh cột vecto. Mọi truy vấn đều LỌC CỨNG bằng các cột này
trước, rồi mới xếp hạng bằng vecto. Nhờ vậy vecto không bao giờ có cơ hội trả
về câu sai lớp hoặc sai mức độ.

## 5.3. Bước 2 — Chọn mô hình nhúng

Hai lựa chọn, chọn một:

| | Gọi qua mạng (OpenAI / Gemini / Voyage) | Chạy tại máy chủ (sentence-transformers) |
|---|---|---|
| Cài đặt | Dễ nhất, thêm một khóa API | Phải cài thư viện, tải model ~500MB |
| Chi phí | Rất rẻ: nhúng 3000 câu tốn khoảng vài nghìn đồng, một lần | Miễn phí |
| Tốc độ | Phụ thuộc mạng | Nhanh, không cần mạng |
| Tiếng Việt | Tốt | Cần chọn model đa ngữ, ví dụ `intfloat/multilingual-e5-base` |
| Đề nghị | Dùng cho lần đầu, để thấy kết quả nhanh | Chuyển sang khi đã chắc là dùng lâu dài |

Số chiều của `vector(n)` phải khớp model. Đổi model thì phải nhúng lại toàn bộ.

## 5.4. Bước 3 — Sinh bản đại diện của từng câu hỏi

Đây là bước có tính chuyên môn nhất, và cũng là bước quyết định chất lượng tìm
kiếm. Với mỗi hàm sinh, gọi một lần rồi ghép thành một đoạn mô tả:

```
[Lớp 10 - Chương 1 - Bài 2 - Thông hiểu - Trắc nghiệm]
Tên yêu cầu cần đạt lấy từ Curriculum.
Đề bài mẫu (đã bỏ số liệu cụ thể, thay bằng dấu ...).
Các từ khóa toán học xuất hiện: mệnh đề, phủ định, ...
```

Ba điểm cần chú ý:

- **Bỏ số liệu cụ thể** trước khi nhúng. Số liệu là thứ thay đổi mỗi lần sinh,
  giữ lại chỉ làm nhiễu.
- **Ghép thêm tên yêu cầu cần đạt từ Curriculum.** Đây là phần mang nghĩa nhiều
  nhất, và là phần giáo viên thật sự tìm theo.
- **Nhúng lại khi sửa hàm.** Lưu ngày cập nhật để biết bản nhúng có cũ không.

## 5.5. Bước 4 — Truy vấn

```sql
-- $1: vecto cua cau tim kiem;  $2..$4: bo loc cung
select generator_id, muc_do, loai_cau,
       1 - (nhung <=> $1) as do_giong
from   cau_hoi_vecto
where  lop = $2
  and  chuong = $3
  and  muc_do = $4
order  by nhung <=> $1
limit  20;
```

`<=>` là toán tử khoảng cách cô-sin của pgvector.

## 5.6. Bước 5 — Nối vào hệ thống

- Thêm `app/services/vecto_service.py`: hai hàm `nhung_van_ban(text)` và
  `tim_cau_hoi(cau_tim, bo_loc)`.
- Thêm `GET /api/bank/tim-kiem?q=...&lop=...&chuong=...` trả về danh sách
  generator_id kèm độ giống.
- Thêm ô tìm kiếm ở khu làm việc của giáo viên (xem docs/21).
- Thêm script `scripts/nap_vecto.py` chạy lại mỗi khi bổ sung câu hỏi mới.

Giữ đúng nguyên tắc kiến trúc của hệ thống: Frontend gọi FastAPI, không gọi
thẳng Supabase, không gọi thẳng model nhúng.

## 5.7. Cách đo xem có đáng không

Trước khi tin là nó hoạt động, làm phép thử này: soạn 20 câu tìm kiếm bằng
tiếng Việt như giáo viên thật sẽ gõ, ghi sẵn đáp án mong muốn là mã câu hỏi
nào. Chạy tìm kiếm và đếm tỉ lệ câu đúng nằm trong 5 kết quả đầu. Dưới 80% thì
chưa dùng được, phải sửa lại bản đại diện ở Bước 3 (thường là do thiếu tên yêu
cầu cần đạt).

---

# 6. Chi phí, rủi ro và khi nào nên dừng

**Chi phí thời gian:** Giai đoạn 0 khoảng một đến hai buổi. Giai đoạn 1 khoảng
ba đến năm buổi cho người không chuyên, phần lớn thời gian nằm ở Bước 3.

**Chi phí tiền:** không đáng kể nếu chạy model tại máy chủ; vài nghìn đồng cho
mỗi lần nhúng lại toàn bộ nếu gọi qua mạng.

**Rủi ro chính:** thêm một thành phần nữa phải bảo trì. Mỗi lần sửa hàm sinh
mà quên nhúng lại thì kết quả tìm kiếm sai một cách âm thầm. Cách phòng: ghi
ngày cập nhật và cho script nạp vecto tự phát hiện hàm đã đổi.

**Khi nào NÊN DỪNG, không làm nữa:** nếu sau Giai đoạn 0, việc tra cứu ngân
hàng đã đủ nhanh bằng chỉ mục và bộ lọc thông thường thì DỪNG. Vecto không
phải mục tiêu, nó chỉ là công cụ cho bài toán tìm kiếm theo nghĩa. Không có
bài toán đó thì không cần công cụ đó.

---

# 7. Điều KHÔNG được làm

- Không thay tra ID bằng tìm vecto trong luồng sinh đề.
- Không để AI hoặc kết quả tìm vecto tự tạo ra Generator ID (docs/04).
- Không bỏ các cột lọc cứng (lop, chuong, muc_do, loai_cau) để "cho vecto tự
  hiểu" — đó là cách nhanh nhất để đề sai ma trận.
- Không nhúng văn bản còn nguyên số liệu ngẫu nhiên.
