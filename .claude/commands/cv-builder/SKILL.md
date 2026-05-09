---
description: Tạo CV chuyên nghiệp từ template Markdown, lưu kết quả vào output/
---

Hãy giúp người dùng tạo một CV chuyên nghiệp dựa trên template có sẵn.

## Thông tin đầu vào
$ARGUMENTS

## Quy trình thực hiện

### Bước 1 — Đọc template
Đọc file template tại: `.claude/commands/cv-builder/cv-template.md`

### Bước 2 — Thu thập thông tin
Hỏi người dùng lần lượt từng mục (hoặc xử lý nếu đã cung cấp trong $ARGUMENTS):

1. **Thông tin cá nhân:** Họ tên, email, số điện thoại, địa chỉ, LinkedIn/GitHub
2. **Ảnh đại diện:** Đường dẫn file ảnh (JPG/PNG). Ảnh chân dung 3x4, nền trắng/xám. Nếu không có, CV sẽ hiển thị ô placeholder. Lưu file ảnh vào `.claude/commands/cv-builder/output/` và ghi `![Photo](photo.jpg)` vào CV.
3. **Mục tiêu nghề nghiệp:** 2-3 câu tóm tắt bản thân và mục tiêu
4. **Kinh nghiệm làm việc:** Công ty, vị trí, thời gian, mô tả công việc (từ gần nhất)
5. **Học vấn:** Trường, ngành, năm tốt nghiệp, GPA (nếu có)
6. **Kỹ năng:** Kỹ năng kỹ thuật, kỹ năng mềm, ngoại ngữ
7. **Dự án nổi bật:** Tên dự án, mô tả, công nghệ sử dụng, link (nếu có)
8. **Chứng chỉ & Giải thưởng:** (tùy chọn)
9. **Hoạt động ngoại khóa:** CLB, tình nguyện, vai trò (tùy chọn)

### Bước 3 — Tạo CV

Điền thông tin vào template, đảm bảo:
- Ngôn ngữ nhất quán (tiếng Việt hoặc tiếng Anh theo yêu cầu)
- Dùng động từ hành động mạnh cho phần kinh nghiệm (Phát triển, Triển khai, Tối ưu, Quản lý...)
- Định lượng thành tích khi có thể (tăng 30%, quản lý 5 người,...)
- Giữ CV trong 1-2 trang

### Bước 4 — Lưu file Markdown

Lưu CV hoàn chỉnh vào: `.claude/commands/cv-builder/output/cv-{HoTen}-{YYYY-MM-DD}.md`

### Bước 5 — Xuất PDF

Cập nhật 2 dòng đầu trong `cv_to_pdf.py` để trỏ đúng vào file vừa tạo:
```python
MD_FILE  = r"...đường dẫn tuyệt đối đến file .md vừa lưu..."
PDF_FILE = r"...đường dẫn tuyệt đối đến file .pdf đầu ra..."
```
Sau đó chạy:
```
python "C:\Users\ADMIN\Desktop\Claude Code\cv_to_pdf.py"
```
PDF sẽ được lưu cùng thư mục với file `.md`.

Thông báo cho người dùng đường dẫn cả 2 file `.md` và `.pdf`.

## Lưu ý
- Nếu người dùng muốn chỉnh sửa một mục, cập nhật trực tiếp vào file `.md` rồi chạy lại script PDF
- Có thể tạo nhiều phiên bản CV cho các vị trí khác nhau bằng cách lưu với tên file khác
- Ảnh đại diện phải nằm cùng thư mục với file `.md` (trong `output/`)
