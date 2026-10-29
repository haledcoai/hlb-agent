# Dữ liệu mẫu đèn chống cháy nổ 1m2 (để viết bài viết lại #3904)

Ngày thu thập: 29/10/2026. Người thu thập: Agent Blog (phiên cloud).

Quy tắc dùng: chỉ số nào có dòng "Đọc được" kèm URL nguồn mới được đưa vào bài. Số trong bài cũ 3904 chỉ để đối chiếu, **không dùng** (xem `serp_bao_cao.md`, bảng Bỏ). Ô thiếu để `[CẦN BỔ SUNG]` hoặc "không công bố".

## 1. Kết quả đọc nguồn

| Nguồn | URL | Kết quả ngày 29/10/2026 |
|---|---|---|
| Website HLB, REST `wp/v2/search` (subtype product, từ "chống nổ", "chống cháy nổ", "tuýp") | https://denlednhaxuongcaocap.com/wp-json/wp/v2/search | Đọc được: **0 sản phẩm** |
| Website HLB, Store API `wc/store/v1/products?search=chống nổ` | https://denlednhaxuongcaocap.com/wp-json/wc/store/v1/products | Đọc được: **0 sản phẩm** |
| CSV `du_lieu_san_pham_HLB_28-10-2026.csv` (tìm "nổ", "tuýp", "1m2") | file repo | **0 dòng** |
| Bài gốc 3904 (REST) | https://denlednhaxuongcaocap.com/wp-json/wp/v2/posts/3904 | Đọc được, sửa lần cuối 22/12/2023 (dùng cho bảng Giữ/Bỏ, không lấy số) |
| haledco.com (REST search) | https://haledco.com/wp-json/wp/v2/search | **Không đọc được**: proxy phiên từ chối kết nối (CONNECT 403) |
| Rạng Đông, link người dùng gửi | https://rangdong.com.vn/bo-den-led-chong-no-pr1928.html | **Không đọc được**: curl CONNECT 403, WebFetch không phân giải tên miền (ngoài danh sách mạng được phép) |
| Philips, link người dùng gửi (trang bán hàng congtydenled) | https://congtydenled.com.vn/blog/tu-van/den-chong-no/den-chong-no-philips.html | **Không đọc được**: như trên |
| Điện Quang, link người dùng gửi | https://dienquang.com/products/bo-den-led-mica-dien-quang-dq-ledmf02-36-nguon-tich-hop | **Không đọc được**: như trên |
| Duhal, Paragon, Athaco | chưa có link | Chưa thử (cần tên miền được mở hoặc người dùng gửi link) |

Kết luận: **HLB không có model đèn chống cháy nổ 1m2** trên website và CSV. Theo trả lời của người dùng (câu 2), dữ liệu HALEDCO phải lấy từ haledco.com, nhưng phiên này không vào được.

## 2. Bảng dữ liệu theo hãng (điền khi đọc được nguồn)

Cột cố định cho mọi hãng (cùng bộ tiêu chí, Knowledge 8.5): model, loại (đơn/đôi), công suất, quang thông, ký hiệu Ex (kiểu bảo vệ, nhóm khí, cấp nhiệt độ), IP, chiều dài/kích thước, giá hoặc khoảng giá, nguồn URL, ngày đọc.

### HALEDCO (HLB phân phối, nguồn haledco.com, không đặt link trong bài)

| Model | Loại | Công suất | Quang thông | Ex | IP | Giá | Nguồn | Ngày |
|---|---|---|---|---|---|---|---|---|
| [CẦN BỔ SUNG] | đơn | | | | | | haledco.com | |
| [CẦN BỔ SUNG] | đôi | | | | | | haledco.com | |

Ghi chú: bài cũ có 5 model HALEDCO (18W đơn, 36W đôi, 40W, 60W đôi, 80W đôi). Số quang thông 18W và 36W cùng 13.000 lm là sai (18 x 130 = 2.340 lm). Không dùng lại, chờ đọc trang haledco.com.

### Rạng Đông (HLB phân phối, nguồn trang hãng)

| Model | Loại | Công suất | Quang thông | Ex | IP | Giá | Nguồn | Ngày |
|---|---|---|---|---|---|---|---|---|
| [CẦN BỔ SUNG, trang pr1928 "Bộ đèn LED chống nổ"] | | | | | | | rangdong.com.vn/bo-den-led-chong-no-pr1928.html | chưa đọc được |

### Philips (HLB phân phối, nguồn trang bán hàng người dùng gửi)

| Model | Loại | Công suất | Quang thông | Ex | IP | Giá | Nguồn | Ngày |
|---|---|---|---|---|---|---|---|---|
| [CẦN BỔ SUNG] | | | | | | | congtydenled.com.vn/.../den-chong-no-philips.html | chưa đọc được |

Lưu ý: đây là trang của đơn vị bán hàng, không phải website chính thức Philips. Instructions mục 6 cho dùng trang bán hàng để lấy khoảng giá; thông số ưu tiên trang hãng (xem câu hỏi 3 trong outline).

### Điện Quang (HLB phân phối)

| Model | Loại | Công suất | Quang thông | Ex | IP | Giá | Nguồn | Ngày |
|---|---|---|---|---|---|---|---|---|
| DQ LEDMF02 36 (theo slug URL) | [CẦN KIỂM TRA] | 36W theo tên | | | | | dienquang.com/products/bo-den-led-mica-... | chưa đọc được |

**Cảnh báo:** slug URL là "bo-den-led-mica-dien-quang-dq-ledmf02-36-nguon-tich-hop", tức "Bộ đèn LED mica ... nguồn tích hợp". Theo tên, đây nhiều khả năng là bộ đèn LED máng mica thông thường, **không phải đèn chống cháy nổ**. Chưa mở được trang để xác nhận. Không đưa model này vào bài như đèn chống nổ cho tới khi trang ghi ký hiệu Ex.

### Duhal, Paragon, Athaco (hãng không bán trên website, chỉ nêu theo thông tin công bố, không so sánh với HLB)

| Hãng | Model | Loại | Công suất | Ex | IP | Giá | Nguồn | Ngày |
|---|---|---|---|---|---|---|---|---|
| Duhal | [CẦN BỔ SUNG] (bài cũ nêu LSC 240, 2x18W) | | | | | | chưa có | |
| Paragon | [CẦN BỔ SUNG] (bài cũ nêu 1m2 72W, 36W, phòng sạch 2x36W "Exedmb II CT5") | | | | | | chưa có | |
| Athaco | [CẦN BỔ SUNG] (SERP #5, #7: loại 1m2 đơn và đôi; máng đôi 700.000-750.000 đồng chưa gồm bóng, bảo hành 2 năm theo đoạn trích Google) | | | | | | athaco.vn (SERP, chưa mở được trang) | 29/10/2026 |

Số Athaco ở trên chỉ là đoạn trích Google trong `serp/_ket_qua_den-chong-chay-no-1m2.json`, chưa mở trang, dùng trong bài phải ghi "theo trang của hãng" sau khi mở được, hoặc để [CẦN KIỂM TRA].

## 3. Dữ liệu chung đã có nguồn

- Mã IP: TCVN 4255:2025 / IEC 60529 (`tieu_chuan_da_kiem.csv`).
- Độ rọi nơi làm việc: TCVN 7114-1:2008, QCVN 22:2016/BYT (`tieu_chuan_da_kiem.csv`), trích đúng bảng khi viết.
- Ký hiệu Ex, phân vùng nguy hiểm: IEC 60079 và TCVN tương đương **chưa có** trong `tieu_chuan_da_kiem.csv`; tra và thêm dòng trước khi viết, không tra được thì [CẦN KIỂM TRA].
