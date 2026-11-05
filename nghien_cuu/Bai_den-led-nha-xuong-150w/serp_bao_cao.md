# Bước 1: Nghiên cứu SERP "đèn led nhà xưởng 150w"

Ngày kiểm tra: 05/11/2026. Nguồn: top Google Việt Nam qua SerpApi (`tools/nghien_cuu.py serp`, lưu ở `serp/_ket_qua_den-led-nha-xuong-150w.json`). Google chỉ trả 8 kết quả tự nhiên, không có mục "Mọi người cũng hỏi" và "Tìm kiếm liên quan". Loại đèn: blog (người dùng chọn khi nạp).

**Kết luận nhanh: CAN_XU_LY.** Từ khóa này là từ khóa của trang danh mục: 7/8 kết quả là trang bán hàng, và website đã có danh mục khớp đúng 100% (`danh_muc.py tim`: KHỚP 1,00, `den-led-nha-xuong-150w`, 21 sản phẩm). Knowledge mục 9.1 ghi bài blog không nhắm trùng từ khóa "đèn LED nhà xưởng [công suất]" của trang danh mục. Một bài blog có H1 và từ khóa chính đúng cụm này sẽ cạnh tranh trực tiếp với danh mục. Ngoài ra website đã có 2 bài blog cùng mức 150W (1529 bảng giá, 5742 toplist). Đề xuất ở mục 4 và cuối file.

## Top 8 Google VN

| # | Trang | Loại |
|---|---|---|
| 1 | silamp.com.vn `/products/den-led-nha-xuong-150w/` | Trang sản phẩm (đường dẫn `/products/`, đoạn trích là bảng thông số) |
| 2 | haledco.com `/den-led-nha-xuong/150w-hlhb/hlhb9-150.html` | Trang sản phẩm HLHB9-150 (đã lưu văn bản: thông số, giá bán lẻ, nút giỏ hàng) |
| 3 | denchieusangled.vn, "Đèn led highbay nhà xưởng 150w, mã sp ZHB150-COB" | Trang sản phẩm (theo tiêu đề có mã sản phẩm, đoạn trích driver, chip, bảo hành) |
| 4 | lightingviet.com.vn `/danh-muc/.../den-led-nha-xuong-150w/` | Trang danh mục |
| 5 | dailydenled.vn, "Báo giá đèn led nhà xưởng công nghiệp Highbay 150W" | Trang bán hàng dạng báo giá, liệt kê mã DLNX150WSMD (theo tiêu đề và đoạn trích) |
| 6 | congtydenled.com.vn `/den-led-nha-xuong/150w-hb` | Trang danh mục có bài mô tả bên dưới (đã lưu văn bản: lưới khoảng 20 sản phẩm có giá, sau đó phần giới thiệu, ưu điểm, báo giá) |
| 7 | philipsvietnam.com `/den-led-nha-xuong-150w-philips/` | Nhiều khả năng trang sản phẩm (đoạn trích chỉ là thông số, bảo hành) |
| 8 | dentrangtri.thanhdathn.com, "Đèn Nhà Xưởng 150W Highbay: So Sánh & Mua Ngay" | Bài blog hoặc trang đích bán hàng (đoạn trích "Tại sao nên chọn...") |

Đã mở và lưu văn bản: #2 (`serp/01-haledco.com.txt`), #6 (`serp/02-congtydenled.com.vn.txt`). Không mở được #3, #5, #7, #8: `luu-serp` bị proxy chặn (403), WebFetch báo tên miền ngoài danh sách mạng được phép của phiên (ENOTFOUND). #1, #4 là trang danh mục/sản phẩm nên không cần lưu. Phân loại #3, #5, #7, #8 dựa trên đường dẫn, tiêu đề, đoạn trích. Muốn mở các trang này thì cần cho phép tên miền dailydenled.vn, dentrangtri.thanhdathn.com, philipsvietnam.com, denchieusangled.vn trong cài đặt mạng của phiên.

## 1. Search intent

Người tìm "đèn led nhà xưởng 150w" đã chọn xong mức công suất, nên ý định chính là **chọn mua (giao dịch)**: xem các mẫu 150W đang bán, so thông số (quang thông, IP, góc chiếu), giá theo hãng và nơi mua. Ý định tìm hiểu (150W dùng cho trần cao bao nhiêu, chiếu được bao nhiêu m²) chỉ là phụ, SERP không có bài nào trả lời riêng ý này.

## 2. Định dạng nội dung

- **Bằng chứng:** 7/8 kết quả là trang bán hàng (4 trang sản phẩm #1, #2, #3, #7; 2 trang danh mục #4, #6; 1 trang báo giá dạng bán hàng #5). Chỉ #8 có thể là bài blog, và tiêu đề của nó cũng nghiêng về mua ("So Sánh & Mua Ngay"). Không có bài hướng dẫn hay kiến thức nào trong top.
- **Định dạng phù hợp nhất: trang danh mục.** Kết quả #6 (danh mục có lưới sản phẩm, rồi phần nội dung giới thiệu, ưu điểm, báo giá) đúng mô hình danh mục của website.
- **Website đã có danh mục khớp:** `python tools/danh_muc.py tim "đèn led nhà xưởng 150w"` trả KHỚP 1,00 `https://denlednhaxuongcaocap.com/den-led-nha-xuong-150w/` (ID 70, 21 sản phẩm), kèm 3 danh mục con GẦN: `philips-150w` (0,80), `cao-cap-150w` (0,67), `rang-dong-150w` (0,67). Theo Instructions Bước 1 mục 2 và DIEU_PHOI.md mục 3c, từ khóa có danh mục khớp thì chuyển Agent Danh mục, không viết blog. Lần này người dùng đã chọn `loai: blog`, nên Agent Blog không tự chuyển, mà dừng để người dùng quyết.
- **Nội dung danh mục hiện tại** (đọc bằng `danh_muc.py doc` ngày 05/11/2026, khối trên 597 ký tự, khối dưới khoảng 2.300 từ): đã có báo giá từng model, thông số chung, cấu tạo, so sánh thương hiệu. Nhiều điểm cần viết lại theo quy tắc: SEO title "30+ đèn LED nhà xưởng 150w highbay GIÁ RẺ 2024", câu "Công nghệ tản nhiệt Graphene tăng tuổi thọ ... lên 60%" (Knowledge mục 5), H2 "So sánh đèn LED nhà xưởng thương hiệu nào tốt nhất?" (từ tuyệt đối), "30 model" trong khi danh mục có 21 sản phẩm.

## 3. Gộp hay tách

SerpApi không trả truy vấn liên quan. Đề xuất theo SERP và bài đã có:
- **Cùng intent với từ khóa chính, gộp vào trang danh mục 150W** (từ khóa phụ đề xuất): "đèn led highbay 150w", "đèn nhà xưởng 150w", "đèn led công nghiệp 150w", "đèn led ufo 150w", "giá đèn led nhà xưởng 150w" (#4, #5, #6 gộp báo giá ngay trên trang bán hàng). Các cụm này website đang dùng sẵn trong meta và khối trên của danh mục.
- **Tách hoặc không làm:**
  - "bảng giá đèn led nhà xưởng 150w": đã có bài 1529, nếu muốn giữ một bài blog về giá thì viết lại bài này (mục 4).
  - "đèn led nhà xưởng 150w Philips / Rạng Đông / cao cấp": đã có danh mục con theo hãng, để Agent Danh mục xử lý.
  - Góc kiến thức "đèn 150W treo cao bao nhiêu, chiếu được bao nhiêu m²": intent khác (tìm hiểu), có thể thành bài blog riêng với từ khóa chính khác (chưa kiểm tra SERP cho cụm này).

## 4. Kiểm tra trùng chủ đề trên website

Tìm bằng REST API `/wp-json/wp/v2/posts?search=150w`, `?search=nhà xưởng 150w`, `?slug=den-led-nha-xuong-150w` ngày 05/11/2026. Chưa có bài blog nào dùng slug `den-led-nha-xuong-150w`.

**Trùng trực tiếp:**

| Trang | URL | Mức trùng |
|---|---|---|
| Danh mục Đèn LED nhà xưởng 150w (ID 70, 21 sản phẩm) | https://denlednhaxuongcaocap.com/den-led-nha-xuong-150w/ | **Trùng hoàn toàn từ khóa**: tên danh mục, slug, H1 đều là "đèn LED nhà xưởng 150W". Bài `Bai_cach-chon-den-led-nha-xuong.md` đang link về danh mục này với anchor "đèn LED nhà xưởng 150W" |

**Trùng một phần (bài blog cùng mức 150W):**

| ID | Bài | URL | Ngày | Phần trùng |
|---|---|---|---|---|
| 1529 | Bảng giá đèn LED nhà xưởng 150W trên thị trường | /tu-van/bang-gia-den-led-nha-xuong-150w/ | sửa 15/05/2026, khoảng 2.700 từ | Intent giá 150W; nêu model BMKT1-150 đến BMKT11-150, các mã này không có trong CSV 05/11/2026 (website hiện dùng B1-150 đến B11-150, BUFO1-150 đến BUFO4-150); heading đánh số lộn xộn (H4 "1.2.3" dưới H2 "2.") |
| 5742 | TOP 14 đèn LED công nghiệp 150w tiết kiệm điện rẻ nhất 2023 | /tu-van/den-led-cong-nghiep-150w/ | sửa 29/08/2023 | Toplist 14 mẫu 150W (B1 đến B11, BUFO, Rạng Đông, Philips, chống nổ), trùng ý danh sách sản phẩm của danh mục; tiêu đề có "rẻ nhất", năm 2023 |
| 7268 | Các loại đèn LED nhà xưởng: 99+ mẫu đèn 50w 100w 150w 200w giá rẻ | /tu-van/cac-loai-den-led-nha-xuong-2/ | sửa 08/12/2023 | Có phần 150W trong toplist nhiều mức |
| 1197, 1205, 1288, 1337, 1345 | Các bài Dự án đèn LED nhà xưởng 150W (2019) | /du-an/... | 2019 | Chỉ trùng chữ, không cạnh tranh blog; có thể dùng làm link nội bộ khi người dùng xác nhận thông tin dự án |

**Đề xuất (theo thứ tự ưu tiên):**
1. **Khuyến nghị: chuyển từ khóa sang luồng danh mục.** Đổi `loai` thành `danh_muc`, `link_danh_muc` là `https://denlednhaxuongcaocap.com/den-led-nha-xuong-150w/`, giao Agent Danh mục viết lại nội dung danh mục (khối trên, khối dưới, SEO title, meta) với các từ khóa phụ ở mục 3. Đây là trang Google sẽ xếp cho từ khóa này, và nội dung hiện tại đang có nhiều câu vi phạm quy tắc (mục 2). Nội dung cũ đã được đọc sẵn ở `nghien_cuu/DM_den-led-nha-xuong-150w/`.
2. **Nếu người dùng vẫn muốn một bài blog về 150W:** không dùng từ khóa chính "đèn led nhà xưởng 150w". Chọn một trong hai:
   - Viết lại bài **1529** với từ khóa chính "bảng giá đèn led nhà xưởng 150w" (`id_bai_cu: 1529`, đăng `--update 1529`), cập nhật model và giá theo CSV 05/11/2026. Intent giá được Knowledge 9.1 cho phép tách khỏi danh mục.
   - Nạp từ khóa mới có intent tìm hiểu, ví dụ "đèn led nhà xưởng 150w chiếu sáng bao nhiêu m2" hoặc "đèn 150w treo cao bao nhiêu mét" (bảng chọn theo chiều cao lắp, ví dụ tính số đèn, khi nào 150W không hợp). Chưa chạy SERP cho các cụm này, cần chạy khi nạp.
3. **Bài 5742** (toplist 150W, 2023, "rẻ nhất") cạnh tranh với danh mục: nên viết lại thành bài khác góc hoặc gộp về danh mục (chuyển hướng 301), người dùng quyết.

## 5. Kiểm tra phạm vi

Đúng phạm vi: đèn LED nhà xưởng mức 150W, website đang bán 21 sản phẩm ở mức này (dòng cao cấp HLB phân phối, Philips, Rạng Đông). Không lệch phạm vi.
