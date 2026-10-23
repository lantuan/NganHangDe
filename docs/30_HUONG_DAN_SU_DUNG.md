# 30. HƯỚNG DẪN SỬ DỤNG NGÂN HÀNG ĐỀ AI

Bản cập nhật 22/10/2026 · Tác giả: Mai Hà Lan

> Ảnh minh hoạ đặt trong thư mục `docs/hinh_huong_dan/`, đặt đúng tên tệp ghi trong
> `docs/hinh_huong_dan/README.md` thì GitHub tự hiện ảnh ở đúng chỗ.
> Mã mời giáo viên KHÔNG ghi ở đây (xem docs/21, mục "Quên mã mời thì tìm ở đâu").

## 1. Giới thiệu

Ngân Hàng Đề AI là website luyện đề và ra đề Toán THPT. Đề, đáp án và lời giải được sinh bằng Python từ ngân hàng câu hỏi do giáo viên biên soạn; AI chỉ hiểu yêu cầu, giảng lại lời giải và không tự tính đáp án.

- **Tác giả:** cô Mai Hà Lan, Trường THPT Chuyên Hùng Vương, tỉnh Gia Lai.
- **Đối tượng:** học sinh luyện đề, làm bài trực tuyến; giáo viên ra đề nhiều mã, tải file, giao bài qua Google Classroom.
- **Song ngữ:** nút Tiếng Việt | English ở góc phải trên. Ngân hàng tiếng Anh hiện có Lớp 10, Chương 1–4.

| Nội dung ngân hàng (22/10/2026) | Số lượng |
| --- | --- |
| Dạng câu đã có hàm sinh | 1.113 / 1.204 dạng khai báo |
| Lớp 10 · Lớp 11 | đủ 100% dạng |
| Lớp 12 | 24 / 115 dạng, đang bổ sung |
| Yêu cầu cần đạt (YCCĐ) bám theo | 382 |
| Loại câu | Trắc nghiệm, Đúng/Sai, Trả lời ngắn, Tự luận |

![Trang chủ](hinh_huong_dan/01_trang_chu.png)

## 2. Truy cập và đăng nhập

Mở trình duyệt (máy tính hoặc điện thoại) và vào **nganhangdechv.tech**. Mọi tính năng đều cần đăng nhập.

**Học sinh**

1. Bấm **Đăng ký** → chọn **Học sinh**, điền họ tên, email, mật khẩu; hoặc bấm **Đăng ký bằng Google**.
2. Lần đầu vào, chọn **lớp Toán** em đang học. Chọn nhầm thì quay lại trang Chọn lớp để đổi.
3. Nếu lớp đã nối Google Classroom, trang tiếp theo hiện **mã lớp**: mở Classroom bằng đúng tài khoản Google của em → bấm **+** → **Tham gia lớp học** → nhập mã. Bước này có thể bỏ qua.

**Giáo viên**

1. Bấm **Đăng ký** → chọn **Giáo viên**. Nên dùng đúng Gmail đang dùng cho Google Classroom.
2. Nhập **mã mời giáo viên** do quản trị cấp (xin mã qua email nganhangdetoanchv@gmail.com).
3. Đăng nhập xong, hệ thống mở **Khu làm việc giáo viên** (đường dẫn /gv).

Quên mật khẩu: bấm **Quên mật khẩu?** ở trang Đăng nhập. Tích **Ghi nhớ đăng nhập** để giữ đăng nhập 7 ngày trên máy đó.

![Trang đăng ký chọn Học sinh / Giáo viên](hinh_huong_dan/02_dang_ky.png)

## 3. Dành cho giáo viên

Khu giáo viên có thanh điều hướng: **Trang chính · Ra đề · Đề đã tạo · Lớp · Thống kê · Gia sư AI · Chat AI**. Nút Việt/Anh nằm dưới thanh tài khoản.

### 3.1. Ra đề kiểm tra (mục Ra đề)

1. Nhập **Tiêu đề đề thi**, chọn **Lớp** và **Số mã đề**. Nhiều mã đề cùng cấu trúc, cùng đơn vị kiến thức, chỉ khác số liệu.
2. Chọn **Loại bài kiểm tra** (thường xuyên, giữa kì, cuối kì). Kiểm tra thường xuyên thì chọn thêm **Chương**; chương chưa có ngân hàng sẽ được ghi chú.
3. Chọn **Phạm vi câu hỏi**: chỉ theo YCCĐ của Bộ, hoặc cho thêm câu luyện tập (câu ngoài YCCĐ vào đề sẽ được ghi chú để thầy/cô giữ hoặc thay).
4. Ma trận mức độ (chọn một trong ba cách):
    - Không tích gì: dùng bảng ma trận mặc định của loại bài kiểm tra.
    - **Tự đặt ma trận mức độ**: nhập số câu và tỉ lệ NB / TH / VD / VDC cho trắc nghiệm, trả lời ngắn, tự luận; mỗi hàng phải đủ 100%. Câu Đúng/Sai giữ cấu trúc 4 ý.
    - **Đặt số câu cụ thể theo bài**: điền bảng giống ma trận đề của Bộ; số nhỏ dưới mỗi ô là số hàm sinh câu có sẵn, ô gạch ngang là chưa có. Tỉ lệ % điểm tự tính.
5. Tùy chọn: **Chế độ nháp** (thiếu câu thì chèn dòng [THIẾU CÂU HỎI] thay vì báo lỗi) và **Tạo kèm đề tiếng Anh tương ứng** (cùng câu, cùng số liệu, cùng thứ tự).
6. Bấm **Tạo đề** một lần và chờ khoảng 30–60 giây cho mỗi mã đề (hệ thống biên dịch LaTeX ra PDF). Không bấm lại nhiều lần.

![Biểu mẫu Ra đề và bảng ma trận](hinh_huong_dan/03_ra_de.png)

### 3.2. Tải đề (mục Đề đã tạo)

Mỗi đề có các liên kết tải: **PDF đề · PDF lời giải · Word đề · Word lời giải · .tex**. Đề có tích tiếng Anh thì có thêm hàng *Tiếng Anh* cùng 5 loại tệp.

- Tích **Tải kèm bản tiếng Anh** để nhận một tệp .zip có cả bản Việt và bản Anh.
- Tệp .tex tải về là bản có lời giải; muốn bản đề thì đổi `[loigiai]` thành `[dethi]` ở dòng `\usepackage{ex_test}`.
- Tệp PDF và Word được dọn sau 10 ngày, .tex sau 1 ngày: cần giữ lâu thì tải về máy.

### 3.3. Giao bài và theo dõi lớp

- **Lớp**: bấm **Lấy mã** để nhận mã lớp Google Classroom phát cho học sinh; **Mở lớp** để vào thẳng lớp trên Classroom. Tài khoản chưa kết nối Classroom thì bấm **Kết nối ngay** ở Trang chính.
- Khi học sinh nộp bài trên web, đề, lời giải và điểm tự đăng lên Google Classroom của lớp.
- **Thống kê**: điểm trung bình và những chương, bài học sinh hay sai, lọc theo khối, lớp, từng em.
- **Gia sư AI**: nhật kí mọi lượt học sinh hỏi, đặt cạnh đáp án Python để thầy/cô đối chiếu xem AI có nói lệch không. Mặc định 20 lượt/em/ngày; có thể nâng riêng cho một em trong ngày.

![Trang Đề đã tạo và trang Thống kê](hinh_huong_dan/04_de_da_tao_thong_ke.png)

## 4. Dành cho học sinh

Học sinh làm mọi việc trong trang **Chat AI**: tạo đề, làm bài trên web, xem điểm và lời giải ngay, hỏi lại câu chưa hiểu, rồi luyện tiếp đề cùng cấu trúc.

```
Tạo đề → Làm bài trên web → Nộp bài (có điểm ngay) → Xem lời giải, hỏi gia sư AI
   ↑                                                          │
   └────────── Làm đề khác cùng cấu trúc, khác số liệu ───────┘
```

### 4.1. Tạo đề

1. Bấm **📝 Tạo đề mới**, chọn **Lớp**, **Loại kiểm tra**, **Chương**; **Số câu** để trống là theo chuẩn.
2. Hoặc gõ yêu cầu bình thường, ví dụ: *“Cho em đề 15 phút chương 2 lớp 10”*. AI hiểu yêu cầu và lấy đề từ ngân hàng, không tự nghĩ ra đề.
3. Muốn có bản tiếng Anh thì tích **Kèm bản tiếng Anh** trước khi tạo (hiện có Lớp 10, Chương 1–4).
4. Đề tạo xong có nút **📄 Tải file** (PDF) và liên kết **Làm bài trực tiếp trên web**.

### 4.2. Làm bài và xem kết quả

1. Bấm **Làm bài trực tiếp trên web**, làm các câu trắc nghiệm, Đúng/Sai, trả lời ngắn.
2. Bấm **Nộp bài**: có điểm ngay, kèm đáp án và **lời giải chuẩn của thầy/cô** từng câu.
3. Phần tự luận (nếu có) em làm ra giấy và nộp cho thầy/cô như bình thường.
4. Nếu lớp đã nối Classroom, đề, bài giải và điểm tự đăng lên Google Classroom của em.

![Trang kết quả sau khi nộp bài](hinh_huong_dan/05_ket_qua.png)

### 4.3. Hỏi gia sư AI và luyện tiếp

- Câu nào chưa hiểu, bấm **💬 Hỏi thầy/cô AI về câu này** và gõ câu hỏi. AI chỉ giảng lại theo đáp án và lời giải có sẵn; lời giải chuẩn luôn hiện ngay bên cạnh để em đối chiếu.
- Với các chương Lớp 10 đã học, mục **📚 Tài liệu lí thuyết thầy/cô đã dùng** chỉ đúng chỗ cần học lại.
- Mỗi em có 20 lượt hỏi mỗi ngày.
- Bấm **🔄 Làm đề khác cùng cấu trúc** để có đề mới cùng dạng, khác số liệu.
- Bấm **💬 Hỏi lại đề cũ** để mở lại đề đã làm; gõ *“cho tôi lời giải”* để nhận file lời giải của đề vừa tạo.

![Gia sư AI trả lời cạnh lời giải chuẩn](hinh_huong_dan/06_gia_su_ai.png)

## 5. Lưu ý và câu hỏi thường gặp

| Tình huống | Cách xử lý |
| --- | --- |
| Ra đề Lớp 12 báo thiếu câu | Lớp 12 mới có 24/115 dạng. Bật **Chế độ nháp** để vẫn ra đề với dòng [THIẾU CÂU HỎI], hoặc giảm số câu ô đó. |
| Đề tiếng Anh có dòng [MISSING] | Chương đó chưa có bản tiếng Anh (hiện có Lớp 10, Chương 1–4). |
| Trang đang ở English mà đề vẫn hiện tiếng Việt | Đề đó không tích Kèm bản tiếng Anh khi tạo. Tạo đề mới có tích, hoặc bấm Làm đề khác và tích ô này. |
| Hết lượt hỏi gia sư AI | Em vẫn xem được lời giải chuẩn; lượt được cấp lại ngày hôm sau. |
| AI từ chối trả lời | Câu hỏi nằm ngoài câu đang xem. Hỏi đúng về câu đó hoặc bước giải trong câu đó. |
| Không tải được file đề cũ | File được dọn sau 10 ngày (.tex sau 1 ngày). Tạo lại đề hoặc tải về máy ngay sau khi tạo. |
| Chọn nhầm vai trò Học sinh / Giáo viên | Vai trò chọn một lần; báo giáo viên phụ trách để đổi lại. |

Mục **Đánh giá học lực** và ra đề theo năng lực đang xây dựng, chưa dùng được.

**Liên hệ hỗ trợ:** cô Mai Hà Lan · nganhangdetoanchv@gmail.com · website nganhangdechv.tech
