# Bước 1 (danh mục): Nghiên cứu "đèn led nhà xưởng 150w"

Ngày làm: 05/11/2026. Chế độ `nghien-cuu` của Agent Danh mục (`6_Agent_Danh_muc_HLB.md` Bước 0, 1). Người dùng chốt 05/11/2026: viết lại nội dung danh mục 150W, bản xem trước đăng lên Trang nháp, không viết bài blog mới.

Nguồn dùng lại (không gọi lại SerpApi, vì kết quả cùng ngày):
- SERP top Google Việt Nam qua SerpApi, lưu ở `nghien_cuu/Bai_den-led-nha-xuong-150w/serp/_ket_qua_den-led-nha-xuong-150w.json` (8 kết quả tự nhiên, không có "Mọi người cũng hỏi", "Tìm kiếm liên quan"). Phân tích loại trang ở `nghien_cuu/Bai_den-led-nha-xuong-150w/serp_bao_cao.md`.
- Dữ liệu danh mục đọc bằng `danh_muc.py doc` lúc 05/11/2026 11:45: `danh_muc.json`, `san_pham.json`, `san_pham.md` (CSV `du_lieu_san_pham_HLB_05-11-2026.csv`), `noi_dung_cu.md`.
- Văn bản trang top đã lưu cho DM bằng `nghien_cuu.py luu-serp DM_den-led-nha-xuong-150w.md ... --tu-file` (chép từ bản đã lưu ở thư mục Bai_): `serp/01-congtydenled.com.vn.txt` (#6, trang danh mục), `serp/02-haledco.com.txt` (#2, trang sản phẩm).
- Không lưu được #1 silamp.com.vn, #4 lightingviet.com.vn, #5 dailydenled.vn, #8 dentrangtri.thanhdathn.com: `luu-serp` bị proxy chặn (403), WebFetch báo `lightingviet.com.vn` ngoài danh sách mạng được phép (ENOTFOUND). Muốn đọc thì cần cho phép các tên miền này trong cài đặt mạng của phiên.

## Bước 0: Chọn danh mục

- Người dùng đưa link danh mục, từ khóa chính không có tên hãng: làm **danh mục cha** https://denlednhaxuongcaocap.com/den-led-nha-xuong-150w/ (ID 70, slug `den-led-nha-xuong-150w`, không có danh mục cha).
- Sản phẩm (API cửa hàng 05/11/2026): **21 mẫu**, gồm 14 mẫu dòng đèn cao cấp HLB phân phối (danh mục con `cao-cap-150w`, ID 106), 3 mẫu Philips (`philips-150w`, ID 104), 4 mẫu Rạng Đông (`rang-dong-150w`, ID 108).
- Danh mục con `dien-quang-150w` có trong `danh_muc.json` nhưng API cửa hàng không liệt kê (không có sản phẩm nào). Nội dung danh mục cha **không nêu Điện Quang** là hãng đang có ở mức 150W. Danh mục con này nên được người dùng kiểm tra (thêm sản phẩm hoặc ẩn), ghi vào phần C khi viết.

## 1. Search intent

Người tìm đã chọn xong mức 150W, nên ý định chính là **chọn mua**: xem các mẫu 150W đang bán, so quang thông, cấp IP, góc chiếu, giá theo hãng, rồi hỏi báo giá. Ý định phụ là kiểm tra 150W có hợp chiều cao trần và diện tích xưởng của mình không. SERP không có bài nào trả lời riêng ý phụ này.

## 2. Định dạng nội dung

- **Bằng chứng:** 7/8 kết quả là trang bán hàng (trang sản phẩm #1, #2, #3, #7; trang danh mục #4, #6; trang báo giá dạng bán hàng #5). Chỉ #8 có thể là bài blog, tiêu đề cũng nghiêng về mua ("So Sánh & Mua Ngay").
- **Định dạng: trang danh mục**, đúng việc người dùng giao. Trang danh mục đang lên top (#6 congtydenled.com.vn, đã đọc văn bản):
  - Khối trên gần như không có chữ: vào thẳng lưới khoảng 20 sản phẩm có giá.
  - Khối dưới dài (khoảng 2.600 từ cả trang): giới thiệu chung, ưu điểm, thông số chung theo khoảng ("18.000 - 22.500 lm", "IP65, IP67, IP68"), báo giá 6 model dạng danh sách gạch đầu dòng, ứng dụng theo loại xưởng, mẫu theo kiểu dáng (UFO, dạng chóa, module), kinh nghiệm chọn, giới thiệu đơn vị, FAQ 3 câu (tuổi thọ, điện tiêu thụ, có nên thay đèn cao áp).
  - **Không có:** bảng so sánh model theo cùng tiêu chí, bảng chọn theo chiều cao trần, giá ghi ngày, phần "khi nào không nên chọn". Thông số ghi chung cho cả mức 150W, không gắn model.
- Trang sản phẩm #2 (haledco.com, HLHB9-150): bảng thông số đầy đủ, giá bán lẻ dạng khoảng, nút giỏ hàng, dịch vụ (giao toàn quốc, đặt theo yêu cầu, kiểm định tại nhà máy). Cho thấy người tìm cần thấy thông số theo từng model và giá ngay.
- **Kết luận cho trang của chúng tôi:** khối trên ngắn (80-150 từ) để lưới sản phẩm hiện sớm; khối dưới ưu tiên bảng chọn nhanh theo chiều cao trần, môi trường, bảng so sánh model theo hãng (đúng 21 mẫu đang bán), giá tham khảo có ngày, cách nhận báo giá. Đây là phần trang top đang thiếu.

## 3. Gộp hay tách

SerpApi không trả truy vấn liên quan. Xếp các từ khóa phụ người dùng nạp:

| Từ khóa phụ | Xử lý | Lý do |
|---|---|---|
| giá đèn led nhà xưởng 150w | **Gộp**, đặt ở H2 giá | Cùng intent mua; #4, #5, #6 đều gộp báo giá ngay trên trang bán hàng |
| đèn led highbay 150w | **Gộp**, SEO title và thân bài | Cùng sản phẩm, website và trang top dùng chung; "highbay" chỉ dùng khi nói kiểu dáng (Knowledge mục 7) |
| đèn led ufo 150w | **Gộp**, ở phần so sánh kiểu dáng | Danh mục có mẫu dạng UFO (BUFO1-150 "kiểu dáng đĩa bay", Rạng Đông BD HB03L 350/150W, Philips BY239P theo trang sản phẩm). Bài 4397 "đèn LED nhà xưởng UFO" là toplist nhiều mức công suất, link sang |
| đèn nhà xưởng 150w | **Gộp**, biến thể tự nhiên trong câu | Cùng nghĩa với từ khóa chính, không cần đặt riêng |
| đèn led công nghiệp 150w | **Bỏ khỏi trang này** (không ép vào) | Knowledge mục 7 không dùng xen "đèn công nghiệp"; bài 5742 đã nhắm đúng cụm này, để bài đó giữ (mục 4) |

Tối đa 4 cụm giữ: giá đèn led nhà xưởng 150w, đèn led highbay 150w, đèn led ufo 150w, đèn nhà xưởng 150w.

Không làm trong trang này:
- "bảng giá đèn led nhà xưởng 150w": bài 1529 đang giữ, nên viết lại bài 1529 sau (đề xuất ở thư mục Bai_).
- "đèn led nhà xưởng 150w philips / rạng đông / cao cấp": thuộc danh mục con, nạp riêng khi cần.
- "đèn 150w treo cao bao nhiêu mét", "đèn 150w chiếu được bao nhiêu m2": intent tìm hiểu, có thể thành bài blog riêng (chưa chạy SERP).

## 4. Kiểm tra trùng chủ đề trên website

Tìm bằng REST API `/wp-json/wp/v2/posts?search=...` ngày 05/11/2026 (`150w`, `cách chọn đèn`, `tính số lượng đèn`, `UFO`).

| ID | Trang | URL | Trùng | Phân vai đề xuất |
|---|---|---|---|---|
| 1529 | Bảng giá đèn LED nhà xưởng 150W trên thị trường | https://denlednhaxuongcaocap.com/tu-van/bang-gia-den-led-nha-xuong-150w/ | Intent giá 150W. Bài nêu model BMKT1-150 đến BMKT11-150, không còn trong CSV 05/11/2026 | Danh mục giữ "đèn led nhà xưởng 150w", "giá đèn led nhà xưởng 150w" (giá của mẫu đang bán). Bài 1529 giữ "bảng giá đèn led nhà xưởng 150w" (giá thị trường, yếu tố làm giá chênh). Danh mục link sang 1529 ở H2 giá; bài 1529 link về danh mục với anchor "đèn LED nhà xưởng 150W" |
| 5742 | TOP 14 đèn LED công nghiệp 150w tiết kiệm điện rẻ nhất 2023 | https://denlednhaxuongcaocap.com/tu-van/den-led-cong-nghiep-150w/ | Toplist cùng các mẫu B1 đến B11, BUFO, Philips, Rạng Đông; trùng ý danh sách sản phẩm của danh mục. Tiêu đề có "rẻ nhất", năm 2023 | Bài 5742 giữ "đèn led công nghiệp 150w". Danh mục không link sang 5742 cho tới khi bài được viết lại (tiêu đề vi phạm từ tuyệt đối); bài 5742 nên link về danh mục. Người dùng quyết: viết lại góc khác hay chuyển hướng 301 về danh mục |
| 4397 | TOP 10 đèn LED nhà xưởng UFO phổ biến, Báo giá 2026 | https://denlednhaxuongcaocap.com/tu-van/den-led-nha-xuong-ufo/ | Trùng một phần với từ khóa phụ "đèn led ufo 150w" | Bài 4397 giữ "đèn led nhà xưởng ufo" (nhiều mức). Danh mục link sang ở phần kiểu dáng; bài 4397 link về danh mục ở mục 150W |
| 7268 | Các loại đèn LED nhà xưởng: 99+ mẫu đèn 50w 100w 150w 200w giá rẻ | https://denlednhaxuongcaocap.com/tu-van/cac-loai-den-led-nha-xuong-2/ | Có phần 150W trong toplist nhiều mức | Không link từ danh mục; bài này nên link về danh mục ở phần 150W |
| 4881 | TOP 8 phần mềm tính toán chiếu sáng | https://denlednhaxuongcaocap.com/tu-van/phan-mem-tinh-toan-chieu-sang/ | Không trùng | Dùng làm link cho phần tính số đèn (danh mục chỉ tóm 1-2 câu) |

Không có bài blog nào dùng slug `den-led-nha-xuong-150w`. Bài `Bai_cach-chon-den-led-nha-xuong.md` (nháp WP 8514) chưa đăng, không dùng làm link.

## 5. Kiểm tra phạm vi

Đúng phạm vi: đèn LED nhà xưởng mức 150W, danh mục đang bán 21 mẫu. Không lệch phạm vi.

## Nội dung cũ: Giữ / Bỏ

Nội dung cũ (đọc 05/11/2026): khối trên khoảng 100 từ, khối dưới 15 H2 khoảng 2.300 từ, SEO title "30+ đèn LED nhà xưởng 150w highbay GIÁ RẺ 2024".

| Nhóm | Ý trong nội dung cũ | Xử lý, lý do |
|---|---|---|
| **Giữ** (viết lại theo dữ liệu mới) | Bảng giá từng model 150W (mục 1, bảng thứ hai) | Giữ ý bảng giá theo model, nhưng lấy giá đang bán ở `san_pham.md` (một mức, ghi ngày 05/11/2026), không dùng khoảng giá cũ |
| Giữ | Chọn góc chiếu: chóa 120 độ cho kho, bãi cần phủ đều; 90 độ cho xưởng cần độ rọi cao (mục 10) | Giữ dạng kinh nghiệm phổ biến, kèm điều kiện chiều cao treo (Knowledge mục 6), chỉ cho model có góc đó |
| Giữ | Cách treo: xích, móc hợp kim, cáp chịu lực; treo thẳng đứng (mục 9) | Giữ ngắn ở phần lắp đặt, thêm lưu ý an toàn (ngắt điện, làm việc trên cao) |
| Giữ | Ứng dụng: nhà xưởng sản xuất, nhà kho, bãi xe (mục 8) | Đưa vào bảng chọn theo loại xưởng, không để thành H2 riêng |
| Giữ | Khoảng cách 6-8 m, treo 8-10 m (mục 9) | Giữ dạng "kinh nghiệm thường gặp, cần tính theo độ rọi", link bài phần mềm tính toán; không trình bày như tiêu chuẩn |
| Giữ | Bảo hành 2 năm dòng cao cấp; có chiết khấu theo số lượng (mục 1, 12) | Giữ theo Knowledge mục 1, 1.1: dòng cao cấp 2 năm (driver, chip LED), Rạng Đông 24 tháng, Philips theo từng model; chiết khấu chỉ nói chung |
| **Bỏ vì sai, lỗi thời** | SEO title "30+ ... GIÁ RẺ 2024"; khối trên, mục 1 "30 model" | Danh mục có 21 mẫu; năm cũ; "GIÁ RẺ" viết hoa kiểu quảng cáo |
| Bỏ | Meta và khối trên nêu HALEDCO, "Tuổi thọ 65000h", "CRI 85Ra", chip Cree, Osram, Philips | Danh mục không có mẫu thương hiệu HALEDCO; tuổi thọ thực tế 25.000-65.000 giờ, Ra 70-90 tùy model; hãng chip không có trong `san_pham.md` |
| Bỏ | "Công nghệ tản nhiệt Graphene tăng tuổi thọ ... lên 60%" (khối trên, mục 3 cấu tạo) | Knowledge mục 5, chưa có tài liệu kỹ thuật |
| Bỏ | Hotline 0332599699, địa chỉ và Tel HALEDCO (mục 15) | Dùng hotline bán hàng 0967569588, kỹ thuật 02437 918 122 (Knowledge mục 1); không giới thiệu HALEDCO |
| Bỏ | Bảng giá theo thương hiệu: HALEDCO, Daxinco, Duhal; Rạng Đông 3.021.000-5.673.000, Philips 3.519.000-4.525.000 | Ba hãng không bán trong danh mục; khoảng giá Rạng Đông, Philips không khớp giá đang bán (Philips 1.900.000-3.299.000, Rạng Đông 2.887.500-3.819.000 đồng) |
| Bỏ | Khoảng giá cũ từng model (ví dụ B1 3.829.500-6.482.500) | Không rõ mức trên là giá gì; dùng giá đang bán |
| Bỏ | "Chiết khấu từ 25% - 45% so với giá bìa" | Knowledge mục 1: không nêu mức chiết khấu |
| Bỏ | Bảng thông số chung: 19.500 lm, 130 lm/W, 65.000 giờ, 85Ra, IP65, driver Meanwell, Done | Áp chung cho cả mức 150W là sai: quang thông 12.000-19.500 lm, chỉ có IP40, IP54, IP66; không model nào ghi IP65 |
| Bỏ | H2 "So sánh ... thương hiệu nào tốt nhất?", bảng có Duhal, Paragon, kết luận "vượt trội hơn hẳn Rạng Đông, Philips", "tuổi thọ gấp 2-3 lần", "tiết kiệm điện gấp 2 lần" | Từ tuyệt đối, so sánh không công bằng (Instructions mục 7); Duhal, Paragon không bán; số Philips trong bảng cũ (70Ra, 60 độ) khác `san_pham.md` (Ra 80, góc 45/60/90/120 với BY239P, BPLCE-150) |
| Bỏ | "Tiết kiệm 70% điện năng"; "ISO, CE, RoHS ... TCVN 7722-1:2009/IEC 60598-1:2008" (mục 5) | Knowledge mục 5; TCVN 7722-1:2009 đã có bản 2017 (`tieu_chuan_da_kiem.csv`) |
| Bỏ | Bảng LED 150W so với cao áp 150W (mục 6) | Tiêu đề hai cột bị đảo so với số liệu; số áp chung 130 lm/W, 65.000 giờ |
| Bỏ | "Quy trình sản xuất ... của công ty HLB", "Sản xuất trực tiếp" (mục 7, 12) | Sai vai trò: HLB phân phối, không sản xuất |
| Bỏ | "Hỗ trợ chi phí vận chuyển", "hỗ trợ 24/7" (mục 12) | Không có trong Knowledge; giao hàng theo mục 1.1 (miễn phí khi đơn trên 5 triệu đồng và trong 10 km từ văn phòng Xuân Đỉnh) |
| Bỏ | "Không gian rộng > 2000m2 nên dùng đèn 180w" (mục 9) | Quy tắc chung không có cơ sở; số đèn và công suất phụ thuộc chiều cao, độ rọi. Thay bằng câu "trần cao hơn thì xem 200W" có điều kiện |
| Bỏ | 5 dự án (JY Plasteel Vina, Thiên Tân, Bridgestone Long Biên, Nitori, INOAC) (mục 13) | Knowledge mục 1: dự án chỉ dùng khi người dùng xác nhận (câu hỏi ở outline) |
| **Bỏ vì không hợp trang danh mục** | Cấu tạo 6 bộ phận (mục 3), 7 tiêu chuẩn (mục 5), so sánh LED với cao áp (mục 6) | Nội dung kiến thức, hợp bài blog; danh mục chỉ giữ phần giúp chọn mua |
| Bỏ | Video (mục 4, 10), catalogue Google Drive (mục 11), danh sách chính sách bảo mật (mục 14) | Không thấy nội dung video, file catalogue chưa kiểm tra; chính sách thay bằng link trang Bảo hành, Mua hàng và vận chuyển. Video, catalogue hỏi người dùng |
