# PROMPT LIBRARY

Version: 2.0

Trạng thái

🟢 Chuẩn chính thức

---

# Mục tiêu

Lưu trữ Prompt chính thức của toàn bộ AI trong hệ thống. Mỗi AI
chỉ có một Prompt chính thức, quản lý theo phiên bản. Toàn hệ
thống chỉ có 3 AI.

---

# Danh sách Prompt

| AI | Prompt |
|-----|--------|
| CHV_Fun | Điều phối hệ thống + phân tích yêu cầu sinh đề |
| CHV_Grader | Chấm câu tự luận |
| CHV_Analyzer | Phân tích học tập + gợi ý luyện tập |

---

===============================================================================

CHV_Fun

-------------------------------------------------------------------------------

Workflow

WF000_Gateway (+ WF001/WF002 khi task=generate_exam)

-------------------------------------------------------------------------------

Prompt

Điều phối toàn bộ hệ thống. Phân loại yêu cầu. Khi task=
generate_exam, đồng thời xác định cấu trúc đề (tra Table Tool
nếu học sinh chưa tự quy định).

Trả về:

{
    "task":"",
    "message":"",
    "cau_truc_de": {}
}

Không sinh đề. Không giải toán. Không trả lời kiến thức.
Không tự tạo ID.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Fun.md

---

===============================================================================

CHV_Grader

-------------------------------------------------------------------------------

Workflow

WF007_GradeExam

-------------------------------------------------------------------------------

Prompt

Chấm câu tự luận bằng cách so sánh bài làm học sinh với
answer/solution có sẵn trong Question Object. Không tự đặt đáp án.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Grader.md

---

===============================================================================

CHV_Analyzer

-------------------------------------------------------------------------------

Workflow

WF003_StudentAnalysis, WF007_GradeExam

-------------------------------------------------------------------------------

Prompt

Nhận Analysis Result (số liệu weak_points/strong_points đã tính
sẵn). Viết nhận xét khích lệ và đề xuất một lệnh luyện tập cụ thể
kèm tham số sẵn.

-------------------------------------------------------------------------------

File

data/prompts/CHV_Analyzer.md

---

# Cập nhật 17/09/2026 — CHV_Fun phải chỉ đường khi từ chối (Version 2.60)

## Việc đã xảy ra

Học sinh gõ "giải cho tôi bài 3" trong Chat AI. CHV_Fun trả lời đại ý
"mình không có chức năng giải đâu nha" rồi dừng. Từ chối là ĐÚNG — bài
lẻ ngoài web không có đáp án Python nào để bám, giảng là phải tự tính,
mà mô hình tính số học rất hay sai.

Nhưng từ chối XONG THÌ BỎ EM ẤY GIỮA ĐƯỜNG. Hệ thống giờ ĐÃ CÓ gia sư
AI (v2.58) giảng lại từng bước — chỉ là em ấy không biết lối vào.

## Đã sửa

`data/prompts/CHV_Fun.md` thêm mục "Cách từ chối". Từ nay `message` của
task `reject_math_solution` phải có đủ 3 ý:

1. Từ chối giải bài lẻ (giữ giọng vui — cô Lan cố ý làm vui, giữ nguyên).
2. Nói rõ MÌNH GIẢNG ĐƯỢC, với câu trong đề em vừa làm trên web.
3. Chỉ đúng 3 bước: tạo đề → làm bài, nộp → bấm nút
   "💬 Hỏi thầy/cô AI về câu này" dưới câu chưa hiểu.

`reject_out_of_scope`: từ chối + chỉ lại 2 việc làm được.

Sửa kèm ở giao diện (không phụ thuộc AI, luôn chạy):
- `chat.html` lời chào mở đầu: thêm dòng "Chưa hiểu bài? Làm xong đề rồi
  bấm Hỏi thầy/cô AI về câu này".
- `chat.html` `addAIMessageLoi()`: mọi tin nhắn lỗi giờ chỉ CẢ HAI đường
  — nút "Tạo đề nhanh" và cách hỏi bài.
- `chat.py`: thông báo khi n8n trả JSON hỏng cũng chỉ đường tương tự.

## CẢNH BÁO — prompt trong repo đang LỆCH với n8n

`data/prompts/*.md` là BẢN GHI, không phải bản đang chạy. Prompt thật
nằm trong node AI trên n8n. Sửa tệp trong repo rồi thì PHẢI dán sang n8n
mới có tác dụng.

Hiện `CHV_Fun.md` NGẮN HƠN bản chạy thật (bản thật có thêm phần giọng
điệu, cách xưng hô — nhìn câu trả lời trên web là thấy). Lần tới mở n8n,
chép nguyên bản thật về đây để hết lệch. Đây là việc tồn đọng.

---

===============================================================================

# Quy tắc

- Một AI chỉ có một Prompt chính thức.
- Prompt lưu dưới dạng Markdown trong data/prompts.
- data/prompts là BẢN GHI; bản chạy thật nằm trên n8n. Sửa bên nào cũng
  phải đồng bộ sang bên kia ngay, không để lệch.
- Không sửa Prompt trực tiếp trong n8n.
- Ưu tiên đưa dữ liệu liệt kê (bảng tra cứu, ví dụ lặp lại) vào
  Table Tool thay vì viết cứng trong Prompt, để giảm token.
- Phần rule định dạng output (chỉ JSON, không markdown, không
  backtick, ký tự đầu {, ký tự cuối }) dùng chung 1 System Prompt
  cho cả 3 AI, không lặp lại trong từng Prompt riêng.
- Khi thay đổi Prompt phải cập nhật CHANGELOG.