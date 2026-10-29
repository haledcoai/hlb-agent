# Bước 1: Nghiên cứu SERP "đèn chống cháy nổ 1m2"

Ngày kiểm tra: 29/10/2026. Nguồn: top Google Việt Nam qua SerpApi (`tools/nghien_cuu.py serp`, lưu ở `serp/_ket_qua_den-chong-chay-no-1m2.json`). Google chỉ trả 8 kết quả tự nhiên, có mục "Tìm kiếm liên quan", không có "Mọi người cũng hỏi".

Loại bài người dùng chọn trên bảng: blog. Lần đầu không có `id_bai_cu`, không có ghi chú.

**Cập nhật 29/10/2026 sau khi người dùng trả lời 4 câu hỏi:** người dùng đồng ý viết lại bài 3904 (giữ URL), `id_bai_cu` = 3904; giữ Duhal, Paragon, Athaco vì bài là tổng hợp; dữ liệu HALEDCO lấy từ haledco.com vì HLB không có model 1m2; dữ liệu hãng khác theo link người dùng gửi. SERP giữ nguyên, không chạy lại. Bảng Giữ/Bỏ ở cuối đã sửa theo trả lời này. Kết quả đọc nguồn sản phẩm ở `du_lieu_mau.md`.

## Top 8 Google VN

| # | Trang | Loại (theo URL, tiêu đề, đoạn trích) |
|---|---|---|
| 1 | rangdongstore.vn, "Bộ Đèn Chống Nổ" (`/bo-den-chong-no-c-...`) | Trang danh mục cửa hàng Rạng Đông |
| 2 | ambee.com.vn, "Đèn Led Chống Cháy Nổ, Tiêu Chuẩn ATEX" (`/collections/`) | Trang danh mục (có nhóm "đèn chống cháy nổ 1m2") |
| 3 | dailydenled.vn, "Đèn chống cháy nổ 1m2 - Địa chỉ mua hàng uy tín..." | Trang bán hàng hoặc bài PR bán hàng (đoạn trích nói chất liệu, thi công) |
| 4 | facebook.com, bài đăng "Đèn chống nổ 1m2 (1.2 mét) là loại đèn tuýp LED hoặc máng đèn..." | Bài mạng xã hội, dạng giới thiệu sản phẩm |
| 5 | athaco.vn, "Đèn phòng chống cháy nổ chất lượng giá rẻ tại TpHCM" | Trang bán hàng (loại 1m2 đơn và đôi, bảo hành 2 năm theo đoạn trích) |
| 6 | ambee.com.vn, "Lắp ráp đèn chống cháy nổ 1m2 bóng led đơn" (`/blogs/`) | Bài blog hướng dẫn (lắp ráp, ứng dụng kho, độ cao 3-4 m) |
| 7 | athaco.vn, "Báo giá bóng đèn chống cháy nổ 1.2m mới nhất năm 2026" | Bài blog báo giá (máng đôi 700.000 - 750.000 đồng chưa gồm bóng, theo đoạn trích) |
| 8 | denledthienloc.vn, "Máng đèn tuýp led chống nổ 1 bóng 1m2" (`/den-chong-chay-no/...-sp2552`) | Trang sản phẩm |

Phiên này không mở được các trang trên: proxy chặn rangdongstore.vn, ambee.com.vn, dailydenled.vn, athaco.vn, denledthienloc.vn (lỗi 403 hoặc không phân giải tên miền, cả `luu-serp` lẫn WebFetch). Phân loại dựa trên URL, tiêu đề, đoạn trích. **Chưa lưu được văn bản bài top** (2 bài blog #6, #7), nên `kiem_tra_bai.py` chưa có dữ liệu so đoạn chép. Muốn lưu, cần mở quyền mạng cho ambee.com.vn và athaco.vn rồi chạy lại `luu-serp`.

Bài 3904 của website (đúng slug `den-chong-chay-no-1m2`) **không có trong top 8**.

## 1. Search intent

Người tìm "đèn chống cháy nổ 1m2" đã biết cần loại bộ đèn tuýp dài 1,2 m chống nổ, nên ý định chính là **chọn mua**: xem có loại đơn, đôi nào, thông số chống nổ, giá bộ đèn hoặc giá máng. Ý định phụ là tìm hiểu cách chọn và lắp (bài #6) và tra giá (bài #7). Người đọc thường là bộ phận mua hàng, nhà thầu cơ điện của kho hóa chất, kho sơn, phòng pha chế, trạm bơm, khu có trần thấp 3-5 m.

## 2. Định dạng nội dung

- **Bằng chứng:** 5/8 kết quả là trang danh mục hoặc trang bán hàng (#1, #2, #3, #5, #8), 1 bài mạng xã hội (#4), **2/8 là bài blog** (#6 hướng dẫn lắp ráp, #7 báo giá).
- **Định dạng phù hợp nhất theo SERP:** trang danh mục hoặc trang sản phẩm. Tuy vậy `python tools/danh_muc.py tim "đèn chống cháy nổ 1m2"`: **KHÔNG KHỚP**, website không có danh mục chống cháy nổ; REST API không có sản phẩm, trang nào chứa "chống nổ", "tuýp", "1m2"; CSV `du_lieu_san_pham_HLB_28-10-2026.csv` không có model chống nổ hay đèn tuýp. Không chuyển được sang Agent Danh mục.
- **Blog vẫn có chỗ:** SERP chỉ 8 kết quả, có 2 bài blog đứng #6, #7, nên một bài hướng dẫn chọn kèm báo giá tham khảo có thể vào top 10. Lên top 3 khó vì top đầu là trang danh mục của hãng và cửa hàng.

## 3. Gộp hay tách

Chỉ có từ khóa chính, chưa có từ khóa phụ. "Tìm kiếm liên quan" gợi ý: đèn chống cháy nổ Rạng Đông, Philips, Duhal, Paragon, 100W, 50W, đèn LED chống cháy nổ, đèn pin chống cháy nổ. Phần lớn là từ khóa khác intent (theo hãng, theo công suất highbay), nên tách. Đề xuất từ khóa phụ ở `outline_de_xuat.md` mục 3.

## 4. Kiểm tra trùng chủ đề trên website

Tìm qua REST API (`wp-json/wp/v2/search`, posts, pages, product, product_cat; Store API) ngày 29/10/2026:

| ID | Bài | URL | Mức trùng |
|---|---|---|---|
| **3904** | TOP 16 đèn chống cháy nổ 1m2 tốt nhất - Báo giá đèn tuýp LED rẻ nhất (đăng 21/04/2020, sửa 22/12/2023, khoảng 2.400 từ) | https://denlednhaxuongcaocap.com/tu-van/den-chong-chay-no-1m2/ | **Trùng hoàn toàn**: cùng từ khóa chính, cùng slug với tên file `Bai_den-chong-chay-no-1m2.md` |
| 3922 | TOP 7 máng đèn chống cháy nổ 0.6m 1m2 GIÁ RẺ (sửa 16/07/2026) | https://denlednhaxuongcaocap.com/tu-van/mang-den-chong-chay-no/ | Trùng một phần (máng 1m2 đơn, đôi, cách lắp máng) |
| 7308 | TOP 7 đèn tuýp LED chống cháy nổ chính hãng - giá rẻ nhất 2023 | https://denlednhaxuongcaocap.com/tu-van/den-tuyp-led-chong-chay-no/ | Trùng một phần (có mục "bóng đèn chống cháy nổ 1 2m", tuýp đôi 2x18W, 60W) |
| 4147 | TOP 8 đèn chống cháy nổ 0.6m | https://denlednhaxuongcaocap.com/tu-van/den-chong-chay-no-0-6m/ | Khác chiều dài, dùng làm link |
| 3941 | TOP 4 đèn huỳnh quang chống cháy nổ | https://denlednhaxuongcaocap.com/tu-van/den-huynh-quang-chong-chay-no/ | Liên quan (bài 3904 có bảng LED và huỳnh quang 1m2) |
| 3509, 6121, 3979 | Đèn chống cháy nổ là gì; Tiêu chuẩn đèn chống cháy nổ; Bảng báo giá đèn LED chống cháy nổ | /tu-van/den-chong-chay-no-la-gi/, /tu-van/tieu-chuan-den-chong-chay-no/, /tu-van/bang-bao-gia-den-led-chong-chay-no/ | Liên quan, dùng làm link |

Các bài 3874, 4069, 4077, 4082, 3821 (highbay, đèn tròn theo công suất) và các từ khóa 20W, 40W, 50W, 100W đang tạm dừng trên bảng **không trùng** với bài 1m2: đó là đèn highbay, đèn pha, đèn tròn; bài 1m2 là bộ đèn tuýp dài. Cần tránh nhắc lại phần đọc ký hiệu Ex dài như outline 50W, chỉ tóm tắt và link bài 6121.

**Đề xuất:** **cập nhật (viết lại) bài 3904**, giữ URL `/tu-van/den-chong-chay-no-1m2/`, không viết bài mới. Lý do:
- Bài mới cùng từ khóa chính sẽ cạnh tranh trực tiếp với bài 3904 (ăn thịt từ khóa), và WordPress sẽ đặt slug `den-chong-chay-no-1m2-2`.
- Bài 3904 có tuổi đời từ 2020 nhưng không vào top 8, nội dung nhiều điểm sai và lỗi thời (bảng dưới), nên viết lại có lợi hơn.
- Đăng nháp theo Instructions mục 10: `wp_draft.py --update 3904`, bản nháp `[CẬP NHẬT #3904]`, không ghi đè bài gốc.
- Bài 3922 và 7308 giữ nguyên ở bài này; bài mới chỉ link sang (máng rời và cách lắp máng sang 3922; bóng tuýp chống nổ các chiều dài sang 7308) để mỗi bài giữ một intent.

## 5. Kiểm tra phạm vi

Thuộc phạm vi: đèn chống cháy nổ là chủ đề phụ đã có bài (Knowledge mục 4), dùng cho kho, xưởng, nhà máy có khí, hơi dễ cháy. Gắn bài với kho và xưởng trần thấp để đúng trọng tâm nhà xưởng.

## Bảng Giữ / Bỏ cho bài 3904 (đọc qua REST API ngày 29/10/2026)

| Nhóm | Ý trong bài 3904 | Lý do |
|---|---|---|
| **Giữ** | Đèn chống cháy nổ 1m2 là bộ đèn dùng bóng tuýp dài 1,2 m, có loại đơn và đôi | Đúng intent, khớp SERP (#4, #5, #8) |
| **Giữ** | Có loại LED và loại huỳnh quang chống nổ 1m2, so sánh hai loại | Ý hữu ích, nhưng viết lại không dùng số không nguồn |
| **Giữ** (chờ nguồn) | Các model HALEDCO: tuýp đơn, tuýp đôi, 40W, 60W, 80W | Người dùng chốt: HLB không có model 1m2 trên website (đã kiểm REST, CSV), lấy model, thông số, Ex, giá từ haledco.com (không link). Phiên 29/10 chưa vào được haledco.com |
| **Giữ** (chờ nguồn) | Mẫu Rạng Đông, Philips 1m2 | Hãng đang bán trên website; thông số lấy lại theo link người dùng gửi (rangdong.com.vn pr1928, congtydenled.com.vn), phiên 29/10 chưa mở được |
| **Giữ** (chờ xác nhận) | Mẫu Điện Quang | Link người dùng gửi có slug "bo-den-led-mica-...-dq-ledmf02-36", theo tên là bộ đèn mica, có thể không phải đèn chống nổ; chỉ giữ khi tìm được model Điện Quang có ký hiệu Ex |
| **Giữ** (người dùng chốt) | Duhal LSC 240, Duhal đôi, Paragon 1m2, Paragon phòng sạch, Athaco | Bài tổng hợp, người dùng muốn liệt kê. Viết theo Instructions mục 7 "thương hiệu không bán trên website": nêu theo thông tin công bố của hãng, tách nhóm riêng, không so sánh với hãng HLB phân phối, không kết luận hãng nào hơn. Số trong bài cũ không dùng lại (xem các dòng Bỏ vì sai) |
| **Giữ** | Mục "nơi mua" | Chuyển thành CTA ngắn ở kết bài |
| **Bỏ vì sai** | HALEDCO tuýp đơn 18W ghi quang thông 13.000 lm và 130 lm/W; tuýp đôi 36W cũng 13.000 lm | Mâu thuẫn: 18 W x 130 lm/W = 2.340 lm, 36 W x 130 lm/W = 4.680 lm, không ra 13.000 lm |
| **Bỏ vì sai** | Ký hiệu chống nổ ghi "Exd II BT", "EXD II BT" | Ký hiệu thiếu nhóm khí (IIA, IIB, IIC) và cấp nhiệt độ (T1-T6), không đọc được |
| **Bỏ vì sai** | "Khả năng chịu nhiệt 450 độ C" | Không rõ là gì (có thể nhầm nhiệt độ bốc cháy ứng với cấp T1), không nguồn |
| **Bỏ vì sai** | Rạng Đông IP65 "sử dụng được cho cả không gian ngoài trời" | Kết luận vượt nguồn, cần thông tin công bố của hãng |
| **Bỏ vì sai** | Paragon 36W, Duhal đôi ghi "thời gian sạc 24 giờ, dùng 1,5 giờ" | Đây là thông số đèn sự cố, lệch với bộ đèn chiếu sáng thường; nhiều bảng chép trùng kích thước 1342x168x109 mm cho 3 hãng |
| **Bỏ vì lỗi thời** | Toàn bộ giá 2023 (1.280.000 - 9.714.000 đồng) | Giá cũ, không có trang sản phẩm trên website để đối chiếu; giá mới lấy theo nguồn ở `du_lieu_mau.md` |
| **Bỏ vì sai** | Điện Quang, Athaco, Paragon 72W cùng kích thước 1342x168x109 mm; bảng so sánh LED và huỳnh quang ghi "tiêu chuẩn chống nổ ATEX" cho cả hai, "IP50-IP54" cho huỳnh quang | Chép trùng, không nguồn; ATEX là chỉ thị EU, không phải tính chất chung của mọi đèn |
| **Bỏ vì lỗi thời** | "Tiết kiệm điện 70%", "tiết kiệm 60%", "tốt hơn gấp 3-5 lần" | Câu cấm ở Knowledge mục 5, không có điều kiện so sánh |
| **Bỏ vì lỗi thời** | Tiêu đề "tốt nhất", "rẻ nhất"; câu "chống cháy nổ tốt nhất" ở sapo | Từ tuyệt đối bị cấm |
| **Bỏ vì lỗi thời** | Địa chỉ "Q. Bắc Từ Liêm", "Ngô Quyền - Sơn Tây" | Địa chỉ đã đổi theo Knowledge mục 1 |
| **Bỏ vì ngoài phạm vi** | Danh sách hãng chip, driver kèm link ngoài (Cree, Nichia, Osram, Bridgelux, Philips, Meanwell) | Không liên quan cách chọn đèn 1m2, link website hãng bị cấm |
| **Bỏ vì ngoài phạm vi** | Đoạn "HALEDCO còn cung cấp đèn panel, âm trần..." | Giới thiệu HALEDCO, lệch chủ đề |

Lỗi kỹ thuật khác của bài cũ: đánh số nhảy từ mục 9 sang 11, ảnh đặt tên trùng nhiều từ khóa ("chiếu sáng hoàn hảo").
