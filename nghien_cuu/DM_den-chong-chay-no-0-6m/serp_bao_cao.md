# Bước 1 (danh mục): Nghiên cứu "đèn chống cháy nổ 0.6m"

Ngày làm: 05/11/2026. Chế độ `nghien-cuu` của Agent Danh mục (`6_Agent_Danh_muc_HLB.md` Bước 0, 1). Người dùng chốt 05/11/2026: danh mục chưa có trên website thì vẫn viết theo danh mục đề xuất và đưa lên Trang nháp.

Nguồn đã dùng:
- SERP top Google Việt Nam qua SerpApi (`nghien_cuu.py serp ... --luu`, 05/11/2026 09:15): `serp/_ket_qua_den-chong-chay-no-0-6m.json`. Google trả 8 kết quả tự nhiên, **không có** "Mọi người cũng hỏi", "Tìm kiếm liên quan".
- Danh mục đề xuất do trưởng phòng tạo bằng `danh_muc.py de-xuat` (05/11/2026 16:13): `danh_muc.json` (`de_xuat: true`, id 0), `san_pham.json` (**0 sản phẩm** khớp "chống cháy nổ"), `noi_dung_cu.md` (không có nội dung cũ). `danh_muc.py tim "chống cháy nổ"`: KHÔNG KHỚP.
- Văn bản trang top đã lưu: `serp/01-athaco.vn.txt` (#2, khoảng 1.900 từ).
- **Không lưu được** #1 diennuocquocdung.com, #3 ledmart.vn (trang trả 0 từ, đã xóa file rỗng), #5 lizuvi.com, #6 lotuslighting.vn, #7 pkled.vn, #8 thanhdathn.com: `luu-serp` bị proxy chặn (403), WebFetch báo tên miền ngoài danh sách mạng được phép (ENOTFOUND). #4 shopee.vn không thử (trang sản phẩm sàn). Phân loại các trang này dựa trên URL, tiêu đề, đoạn trích.
- Bài blog trên website: REST API `wp/v2/search` ("0.6m", "0,6m", "6 tấc", "chống cháy nổ", "chống nổ") và `wp/v2/posts/<ID>` (4147, 3922, 4069, 4077, 4082) ngày 05/11/2026. Dữ liệu nghiên cứu bài 1m2: `nghien_cuu/Bai_den-chong-chay-no-1m2/` và `Bai_den-chong-chay-no-1m2.md`.

## Top 8 Google VN

| # | Trang | Loại (theo URL, tiêu đề, đoạn trích) |
|---|---|---|
| 1 | diennuocquocdung.com, "Bộ đèn Led chống nổ 20W, 0.6m LE-60T, LE-60V" | Trang sản phẩm (bộ đèn chống nổ "6 tấc" 20W) |
| 2 | athaco.vn, "Báo Giá đèn Led Chống Cháy Nổ Mới Nhất Năm 2025" | Bài blog báo giá tổng của một hãng (highbay, 1m2, bóng tròn E27); không có mục riêng 0,6 m (đã đọc văn bản) |
| 3 | ledmart.vn, "Máng đèn chống cháy nổ đôi 0,6m LM-MCN-600D" | Trang sản phẩm (máng đôi 0,6 m) |
| 4 | shopee.vn, "Đèn LED tuýp chống cháy nổ 18W/36W, máng ... Ex d IIC T6" | Trang sản phẩm sàn thương mại điện tử |
| 5 | lizuvi.com, "Đèn khẩn cấp chống nổ Starslite SLE-EX" | Trang sản phẩm, lệch intent (đèn khẩn cấp) |
| 6 | lotuslighting.vn, "Đèn chống nổ đơn 0,6m LTMCN0,6" | Trang sản phẩm, đoạn trích có bảng giá nhiều mẫu (đôi 0,6 m 640.000, đôi 1,2 m 750.000) |
| 7 | pkled.vn, "Đèn chống cháy nổ - Công ty TNHH Điện PK" (`/danh-muc-san-pham/...`) | Trang danh mục chung đèn chống cháy nổ |
| 8 | thanhdathn.com, "Đèn tuýp máng chống cháy nổ 9W x 2 0,6m đôi (TDL-MCN206)" | Trang sản phẩm (máng đôi 0,6 m 2x9W) |

Bài 4147 của website (đúng slug `den-chong-chay-no-0-6m`) **không có trong top 8**.

## 1. Search intent

Người tìm "đèn chống cháy nổ 0.6m" đã biết cần loại bộ đèn tuýp ngắn dài 0,6 m có vỏ chống nổ, nên ý định chính là **chọn mua**: xem mẫu đơn, đôi, công suất, ký hiệu Ex, giá cả bộ hay giá máng. Ý định phụ là tra giá (#2, #6). Người dùng thường là bộ phận mua hàng, nhà thầu cơ điện cho hành lang, phòng ắc quy, phòng kỹ thuật, kho hóa chất nhỏ, trạm bơm có trần thấp, nơi bộ 1,2 m quá dài hoặc quá sáng.

## 2. Định dạng nội dung

- **Bằng chứng:** 7/8 kết quả là trang bán hàng (6 trang sản phẩm #1, #3, #4, #5, #6, #8 và 1 trang danh mục #7). Chỉ #2 là bài blog, và là bài báo giá của một hãng, không nói riêng 0,6 m.
- **Định dạng: trang danh mục**, đúng loại người dùng chọn. Đoạn trích cho thấy trang top thường có: tên mẫu kèm chiều dài và số bóng (đơn, đôi), công suất (8W, 9W x 2, 18W, 20W), ký hiệu Ex (ví dụ "Ex d IIC T6"), IP65, giá từng mẫu hoặc bảng giá nhiều mẫu, phân biệt giá máng và giá bộ.
- **Trang top chưa có** (theo đoạn trích và văn bản #2): bảng chọn đơn hay đôi theo loại khu và chiều cao lắp; hướng dẫn đối chiếu ký hiệu Ex trên nhãn với vùng nguy hiểm trước khi mua; khi nào nên chọn 1,2 m hoặc đèn highbay chống nổ thay cho 0,6 m.
- **Giới hạn của trang chúng tôi:** danh mục chưa có sản phẩm, nên khối dưới viết theo cách chọn đèn (người dùng chốt 05/11/2026), chỗ bảng mẫu và giá để `[CẦN BỔ SUNG]`. Trang mỏng hơn trang top cho tới khi có sản phẩm thật, nên khó lên top trước khi người dùng gắn sản phẩm. Khi có sản phẩm: chạy lại `danh_muc.py doc`, giao chế độ `sua` để thêm bảng model, giá.

## 3. Gộp hay tách

Không có từ khóa phụ, SerpApi không trả truy vấn liên quan. Tự đề xuất theo tiêu đề, đoạn trích top 8 (tối đa 4 cụm giữ):

| Cụm | Xử lý | Lý do |
|---|---|---|
| đèn chống nổ 0.6m (đèn chống nổ 0,6m) | **Gộp** | Biến thể bỏ chữ "cháy", #1, #3, #6 dùng; cùng sản phẩm |
| đèn chống cháy nổ 0.6m đôi | **Gộp**, H2 chọn đơn hay đôi | #3, #6, #8 là mẫu đôi; cùng intent mua |
| máng đèn chống cháy nổ 0.6m | **Gộp một câu** ở H2 giá (giá máng chưa gồm bóng) | #3, #8 bán máng; bài 3922 đang giữ cụm "máng đèn chống cháy nổ", nên danh mục chỉ nhắc và link sang |
| đèn chống cháy nổ 6 tấc | **Gộp**, biến thể trong câu | Cách gọi thị trường (#1 "6 tấc") |
| đèn tuýp LED chống cháy nổ 0.6m | **Bỏ khỏi trang này** (không ép) | Gần bài 7308 (đèn tuýp LED chống cháy nổ mọi chiều dài); dùng tự nhiên trong câu nếu cần |
| đèn khẩn cấp chống nổ | **Bỏ** | Intent khác (#5), website có bài 3949, 3886 |

Không làm trong trang này: "đèn chống cháy nổ 1m2" (bài 3904, đang viết lại, nháp 8546), các từ khóa theo công suất 20W, 40W, 50W (bài 4069, 4077, 4082, đang trên bảng).

## 4. Kiểm tra trùng chủ đề trên website

| ID | Bài | URL | Mức trùng | Phân vai đề xuất |
|---|---|---|---|---|
| **4147** | TOP 8 đèn chống cháy nổ 0.6m giá rẻ - bán chạy nhất 2023 (sửa 08/12/2023, khoảng 1.650 từ; toplist theo hãng HALEDCO, Rạng Đông, Philips, Điện Quang, mẫu đôi, Paragon 30W, bộ 20W, tuýp 8W) | https://denlednhaxuongcaocap.com/tu-van/den-chong-chay-no-0-6m/ | **Trùng hoàn toàn từ khóa**, cùng slug với danh mục đề xuất (khác đường dẫn: bài nằm ở `/tu-van/`, nên WordPress không chặn slug) | Xem quyết định dưới bảng |
| 3922 | TOP 7 máng đèn chống cháy nổ 0.6m 1m2 GIÁ RẺ (sửa 16/07/2026) | https://denlednhaxuongcaocap.com/tu-van/mang-den-chong-chay-no/ | Một phần (máng T8 đơn, đôi 0,6 m) | Bài giữ "máng đèn chống cháy nổ". Danh mục link sang ở phần lắp đặt, máng rời; bài link về danh mục ở mục máng 0,6 m |
| 3904 | TOP 16 đèn chống cháy nổ 1m2 (đang viết lại, nháp 8546 `cho_duyet_anh`) | https://denlednhaxuongcaocap.com/tu-van/den-chong-chay-no-1m2/ | Khác chiều dài, cùng loại đèn | Danh mục link sang ở phần "khi nào chọn 1,2 m". Bài 1m2 bản mới không link sang 0,6 m (phần C chỉ đề xuất 4147 link về bài 1m2); khi danh mục có sản phẩm, thêm vào bài 1m2 một link về danh mục ở H3 "Khi nào không nên dùng đèn 1m2" hoặc đoạn loại đơn, anchor "đèn chống cháy nổ 0.6m" |
| 7308 | TOP 7 đèn tuýp LED chống cháy nổ chính hãng - giá rẻ nhất 2023 | https://denlednhaxuongcaocap.com/tu-van/den-tuyp-led-chong-chay-no/ | Một phần (bóng tuýp chống nổ các chiều dài) | Không link từ danh mục (tiêu đề có "rẻ nhất"); bài nên link về danh mục |
| 4069, 4077, 4082 | Đèn chống cháy nổ 20W, 40W, 50W | /tu-van/den-chong-chay-no-20w/, /tu-van/den-chong-chay-no-40w/, /tu-van/den-led-chong-chay-no-50w/ | **Không trùng**: các H2 là highbay, đèn pha, đèn đường, bộ 1,2 m theo công suất; không bài nào nhắc 0,6 m (đã đếm trong nội dung) | Không link từ danh mục. Sau này nếu có danh mục 20W (đề xuất trên bảng) thì là danh mục anh em, link qua lại |
| 6121, 3509, 3821 | Tiêu chuẩn đèn chống cháy nổ; Đèn chống cháy nổ là gì; Đèn LED highbay chống cháy nổ | /tu-van/tieu-chuan-den-chong-chay-no/, /tu-van/den-chong-chay-no-la-gi/, /tu-van/den-led-highbay-chong-chay-no/ | Liên quan | Dùng làm link nội bộ |

**Quyết định phân vai với bài 4147 (Agent tự quyết theo SEO):**
- SERP 7/8 là trang bán hàng, nên **danh mục giữ từ khóa chính "đèn chống cháy nổ 0.6m"** (mua: mẫu đang bán, giá HLB, đặt hàng).
- **Bài 4147 không chuyển hướng 301 lúc này**: danh mục chưa có sản phẩm, và chưa tạo trên website; 4147 đang là trang duy nhất của website cho cụm này.
- Khi danh mục đã tạo và có sản phẩm: viết lại 4147 (giữ URL) theo góc tìm hiểu như bài 1m2 (tổng hợp mẫu các hãng theo cùng bộ tiêu chí, cách chọn), bỏ "giá rẻ", "bán chạy nhất 2023", focus keyword chuyển sang cụm tìm hiểu (chạy SERP khi nạp lên bảng), link về danh mục với anchor "đèn chống cháy nổ 0.6m". Nếu SERP lúc đó vẫn không còn chỗ cho bài blog thì 301 bài 4147 về danh mục.
- Trong lúc chờ, danh mục **không link sang 4147** (tiêu đề có từ tuyệt đối, dữ liệu sai, xem bảng dưới).

## 5. Kiểm tra phạm vi

Thuộc phạm vi: đèn chống cháy nổ là chủ đề phụ đã có bài (Knowledge mục 4), dùng ở kho, xưởng, nhà máy có khí, hơi, bụi dễ cháy. Gắn nội dung với kho hóa chất, phòng kỹ thuật, trạm bơm của nhà máy. Đoạn trích #1 nêu "nhà phố, căn hộ" là dùng ngoài phạm vi, không theo.

## Nội dung cũ: Giữ / Bỏ

Danh mục chưa có trên website, **không có nội dung cũ** (`noi_dung_cu.md`). Bảng dưới ghi các ý của bài 4147 (cùng từ khóa) để khi viết **không lấy lại** số liệu sai:

| Nhóm | Ý trong bài 4147 | Xử lý, lý do |
|---|---|---|
| Giữ ý | Có loại đơn và đôi; dùng bóng tuýp dài 0,6 m | Đúng, khớp SERP; viết lại bằng lời mới |
| Bỏ vì sai | Philips 0,6 m "Tiêu chuẩn chống cháy nổ: IP54" | IP là cấp chống bụi nước, không phải ký hiệu chống nổ |
| Bỏ vì sai | HALEDCO "Tiêu chuẩn chống cháy nổ EZ2-4012GT-060-X21", IP67 | Chuỗi này giống mã sản phẩm, không phải ký hiệu Ex; không có nguồn |
| Bỏ vì sai | Điện Quang 0,6 m chống nổ (Exd II BT6, 120-130 lm/W) | Sitemap dienquang.com đọc ngày 30/10/2026 không có sản phẩm chống nổ (`Bai_den-chong-chay-no-1m2/du_lieu_mau.md`) |
| Bỏ vì sai | Ký hiệu "Exd II BT6", "EXD II BT6" | Thiếu hoặc ghép sai nhóm khí, không đọc được đủ |
| Bỏ vì lỗi thời | Khoảng giá 2023 (850.000-1.500.000 đồng) | Giá cũ, không có trang sản phẩm trên website |
| Bỏ (Knowledge mục 5) | "Tiết kiệm điện năng tới 70%", "chất lượng hàng đầu", "bán chạy nhất" | Câu cấm, từ tuyệt đối |
| Bỏ vì ngoài trang danh mục | Danh sách chip Osram, Cree, Nichia, Bridgelux; đoạn giới thiệu HALEDCO bán đèn 150W | Không có nguồn cho model, lệch chủ đề |
