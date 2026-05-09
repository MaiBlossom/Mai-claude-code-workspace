---
description: Tóm tắt tin tức mới nhất theo chủ đề sử dụng NewsAPI hoặc WebSearch
---

Hãy tìm và tóm tắt tin tức mới nhất theo chủ đề người dùng yêu cầu.

## Chủ đề
$ARGUMENTS

## Quy trình thực hiện

### Bước 1 — Xác định chủ đề
Nếu $ARGUMENTS rỗng, hỏi người dùng: "Bạn muốn đọc tin tức về chủ đề gì?"

### Bước 2 — Lấy tin tức

**Ưu tiên 1 — Dùng NewsAPI** (nếu có biến môi trường NEWSAPI_KEY):
```
GET https://newsapi.org/v2/everything?q={topic}&language=vi&sortBy=publishedAt&pageSize=10&apiKey={NEWSAPI_KEY}
```
Nếu không có kết quả tiếng Việt, thử lại với `language=en`.

**Ưu tiên 2 — Dùng WebSearch** (nếu không có API key):
Tìm kiếm: `{chủ đề} tin tức mới nhất site:vnexpress.net OR site:tuoitre.vn OR site:thanhnien.vn`

### Bước 3 — Lọc kết quả

Từ trang đầu kết quả tìm kiếm, chỉ lấy **tối đa 10 kết quả đầu tiên**.

Với mỗi kết quả, đánh giá mức độ liên quan đến chủ đề yêu cầu theo thang 0–100%:
- Xét tiêu đề, mô tả, và URL của bài báo
- **Chỉ giữ lại các bài có độ liên quan từ 60% trở lên**
- Loại bỏ hoàn toàn các bài không đủ ngưỡng, không đề cập trong output

Nếu sau lọc còn ít hơn 3 bài, thực hiện thêm 1 lượt tìm kiếm với từ khóa hẹp hơn (thêm từ khóa cụ thể hơn hoặc tên địa điểm) rồi lọc lại. Nếu vẫn không đủ 3 bài sau vòng 2, xuất toàn bộ bài đã lọc được và ghi chú: *"Chỉ tìm thấy {M} bài đủ độ liên quan cho chủ đề này."*

### Bước 4 — Tóm tắt và xuất kết quả

Xuất kết quả theo định dạng sau:

```
# Tin tức: {Chủ đề} — {Ngày hôm nay}

## 1. {Tiêu đề bài báo}
- **Nguồn:** {tên báo}
- **Thời gian:** {giờ/ngày đăng}
- **Độ liên quan:** {X}%
- **Tóm tắt:** {2-3 câu tóm tắt nội dung chính}
- **Link:** {URL}

## 2. ...

---
*Đã kiểm tra {N} kết quả, giữ lại {M} bài đạt ngưỡng ≥ 60% liên quan.*
```

Lưu kết quả vào file: `news-output/{slug-chu-de}-{YYYY-MM-DD}.md`
(slug: chuyển chủ đề thành chữ thường, bỏ dấu tiếng Việt, thay space bằng `-`. Ví dụ: "Dịch bệnh" → `dich-benh`)

## Lưu ý
- Chỉ lấy bài đăng trong vòng 7 ngày gần nhất
- Tóm tắt khách quan, không thêm ý kiến cá nhân
- Nếu chủ đề nhạy cảm, ưu tiên nguồn báo chính thống
- Không hiển thị danh sách bài bị loại — chỉ show bài đã qua lọc
