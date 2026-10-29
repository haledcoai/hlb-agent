<!-- Lưu 2026-10-29T01:49. Sửa outline đã chốt thì lưu lại bằng tools/nghien_cuu.py luu-outline --ly-do -->

**Bước 2: Outline đề xuất, viết lại bài #3904** (lập lại 29/10/2026 sau khi người dùng trả lời 4 câu hỏi của lần nghiên cứu trước)

- `id_bai_cu` = 3904, giữ URL https://denlednhaxuongcaocap.com/tu-van/den-chong-chay-no-1m2/ (đăng nháp bằng `wp_draft.py --update 3904`).
- Trả lời của người dùng đã áp dụng: (1) đồng ý viết lại 3904; (2) HLB không có model 1m2 (đã kiểm REST, Store API, CSV ngày 29/10: 0 sản phẩm), nên lấy dữ liệu HALEDCO từ haledco.com, không link; (3) dữ liệu Rạng Đông, Philips, Điện Quang theo link người dùng gửi; (4) giữ Duhal, Paragon, Athaco vì bài là tổng hợp.
- SERP giữ nguyên lần 29/10/2026 (`serp_bao_cao.md`). Dữ liệu mẫu và kết quả đọc nguồn: `du_lieu_mau.md`.

**1. Loại bài:** toplist tổng hợp mẫu theo hãng, kết hợp hướng dẫn chọn và giá tham khảo. Lý do: SERP nghiêng về chọn mua (5/8 kết quả là trang danh mục, trang bán hàng, nơi người đọc xem nhiều mẫu nhiều hãng), hai bài blog trong top là hướng dẫn lắp ráp và báo giá. Người dùng muốn bài liệt kê đủ các hãng người đọc quan tâm. Vì vậy phần thân là danh sách mẫu theo hãng (cùng một bộ tiêu chí), phần sau là hướng dẫn chọn làm góc khác biệt. Không xếp hạng, không chấm điểm; số thứ tự hãng chỉ để đánh mục, ghi rõ trong bài.

**2. Phân tích bài đang xếp hạng** (không mở được trang top, rút ý từ tiêu đề, đoạn trích và bài 3904):
- Ý bắt buộc:
  - Đèn chống cháy nổ 1m2 là bộ đèn dùng bóng tuýp dài 1,2 m, vỏ kín chống nổ; có loại đơn và đôi.
  - Danh sách mẫu theo hãng (Rạng Đông, Philips, Duhal, Paragon, Athaco... đều xuất hiện ở "Tìm kiếm liên quan" hoặc top) với thông số chính: công suất, ký hiệu Ex, IP, kích thước.
  - Giá bộ đèn hoặc giá máng chưa gồm bóng (bài #7 athaco).
  - Nơi dùng và độ cao lắp khoảng 3-4 m (bài #6 ambee).
- Góc khác biệt:
  1. **Mọi hãng cùng một bộ tiêu chí, có nguồn, ô thiếu ghi "không công bố"**, kèm cách đọc ký hiệu Ex trên nhãn (nhóm khí, cấp nhiệt độ) để người mua tự đối chiếu mẫu với khu vực của mình. Bài top và bài cũ chép trùng thông số giữa các hãng, ký hiệu Ex thiếu nhóm khí và cấp nhiệt độ.
  2. **Bảng chọn đơn hay đôi theo chiều cao lắp, ví dụ tính số bộ cho kho 6 x 10 m (Python, ghi "ước tính"), khi nào không nên dùng đèn 1m2, và lỗi hay gặp khi mua, lắp** (lắp bóng thường vào máng chống nổ, nhầm đèn kín nước IP65 với đèn chống nổ, so giá máng chưa gồm bóng với giá cả bộ).

**3. Từ khóa phụ** (người dùng đã chọn ở lần trước, giữ cả 5):
- Giữ trong bài:
  - "đèn chống nổ 1m2": biến thể cùng intent, dùng ở H2 danh sách mẫu và FAQ.
  - "đèn chống cháy nổ 1.2m": biến thể cách viết, dùng ở H2 định nghĩa.
  - "đèn chống cháy nổ 1m2 đôi": H3 loại đơn và đôi, H3 chọn đơn hay đôi.
  - "đèn tuýp LED chống cháy nổ 1m2": H3 bóng LED hay huỳnh quang.
  - "giá đèn chống cháy nổ 1m2": H2 giá.
- Tách: "máng đèn chống cháy nổ" (bài 3922), "đèn tuýp LED chống cháy nổ" mọi chiều dài (bài 7308), "đèn chống cháy nổ 0.6m" (bài 4147), từ khóa theo công suất highbay (50W, 100W) và theo hãng (bài riêng hoặc đang chờ trên bảng): chỉ link sang.
- Bỏ: "đèn pin chống cháy nổ" (thiết bị cầm tay). Không còn bỏ "Duhal", "Paragon" (người dùng chốt giữ, nêu trong bài, không làm từ khóa phụ riêng).

**4. Outline**

H1: Đèn chống cháy nổ 1m2: tổng hợp mẫu theo hãng, cách chọn và giá (63 ký tự)

SEO title đề xuất: Đèn chống cháy nổ 1m2: mẫu đơn, đôi các hãng, thông số Ex và giá (64 ký tự)

Mở bài (sapo + trả lời nhanh): đèn chống cháy nổ 1m2 là bộ đèn tuýp dài 1,2 m vỏ kín chống nổ, có loại đơn và đôi; bài tổng hợp mẫu của các hãng (HALEDCO, Rạng Đông, Philips, Điện Quang, Duhal, Paragon, Athaco, theo nguồn đọc được), và 3-4 điều phải kiểm tra trên nhãn trước khi mua (ký hiệu Ex đúng vùng, đơn hay đôi theo chiều cao, giá cả bộ hay giá máng).

H2: Đèn chống cháy nổ 1m2 là gì, khác đèn tuýp kín nước thế nào
- Cấu tạo bộ đèn 1,2 m (thân, kính, đầu cáp, bóng), vì sao đèn IP65 thường không thay được đèn chống nổ.

H3: Loại đơn và loại đôi
- Khác nhau về số bóng, quang thông, khu nên dùng của từng loại.

H3: Bóng tuýp LED hay huỳnh quang chống nổ 1m2
- Ưu, nhược công bằng, không dùng số "tiết kiệm 70%", link bài đèn huỳnh quang chống cháy nổ.

H2: Các mẫu đèn chống cháy nổ 1m2 của hãng HLB phân phối
- Một bộ tiêu chí cho mọi mẫu: model, đơn/đôi, công suất, quang thông, ký hiệu Ex, IP, giá tham khảo, phù hợp khu nào, lưu ý khi chọn; nguồn ghi ở phần C. Mở H2 bằng bảng tóm tắt tối đa 5 cột (hãng và model, loại, công suất, Ex và IP, giá).

H3: Đèn chống cháy nổ 1m2 HALEDCO
- Các model đơn, đôi theo haledco.com ("đèn do HALEDCO sản xuất", không link, không giới thiệu dài về hãng).

H3: Đèn chống cháy nổ 1m2 Rạng Đông
- Bộ đèn LED chống nổ theo trang hãng (pr1928).

H3: Đèn chống cháy nổ 1m2 Philips
- Mẫu đơn và đôi theo nguồn đọc được; nói rõ thông số theo trang hãng hay trang bán hàng.

H3: Đèn chống cháy nổ 1m2 Điện Quang
- Chỉ giữ heading khi xác nhận được model có ký hiệu Ex (xem câu hỏi 2); không có thì bỏ H3 này trước khi lưu outline.

H2: Mẫu đèn chống nổ 1m2 của Duhal, Paragon, Athaco
- Hãng không bán trên website: nêu thông số và giá theo thông tin công bố của hãng, cùng bộ tiêu chí, không so sánh với nhóm hãng HLB phân phối, không đánh giá hơn kém.

H3: Đèn chống nổ 1m2 Duhal
- Mẫu đơn, đôi theo trang Duhal (bài cũ nêu LSC 240, chỉ giữ khi nguồn xác nhận).

H3: Đèn chống nổ 1m2 Paragon
- Mẫu 1m2 và mẫu phòng sạch theo trang Paragon.

H3: Đèn chống nổ 1m2 Athaco
- Loại đơn, đôi và giá máng theo trang Athaco.

H2: Cách chọn đèn chống cháy nổ 1m2 cho kho và xưởng
- Cách đối chiếu các mẫu ở trên với khu vực của mình.

H3: Đọc nhanh ký hiệu Ex trên nhãn
- Kiểu bảo vệ, nhóm khí, cấp nhiệt độ, vùng được dùng; chỉ tóm tắt, chi tiết link bài tiêu chuẩn đèn chống cháy nổ (mã IEC 60079 [CẦN KIỂM TRA] tới khi thêm vào `tieu_chuan_da_kiem.csv`).

H3: Chọn đơn hay đôi theo chiều cao lắp và độ rọi
- Bảng chọn nhanh theo chiều cao 3-6 m và loại khu (kho, hành lang, phòng pha chế).

H3: Ví dụ tính số bộ cho kho hóa chất 6 x 10 m
- Công thức Knowledge 8.2, UF = MF = 0,8, quang thông lấy từ một model có nguồn ở H2 trên, tính bằng Python, ghi "ước tính".

H3: Khi nào không nên dùng đèn 1m2
- Trần cao, cần độ rọi lớn thì chuyển sang highbay chống nổ (link bài đèn LED highbay chống cháy nổ); mua máng rời thì bóng và đầu cáp phải đúng chuẩn chống nổ (link bài máng).

H2: Giá đèn chống cháy nổ 1m2 tham khảo
- Bảng khoảng giá theo hãng và loại đơn/đôi, ghi ngày kiểm tra; tách giá cả bộ và giá máng chưa gồm bóng; giá đổi theo số lượng, thời điểm.

H2: Lỗi hay gặp khi mua và lắp đèn chống cháy nổ 1m2
- Lắp bóng thường vào máng chống nổ, chọn sai cấp nhiệt độ, đầu cáp và ống luồn dây không kín, mở nắp thay bóng khi còn điện; lưu ý an toàn đặt đúng ở bước thay bóng, việc cần thợ điện có chuyên môn.

H2: Câu hỏi thường gặp về đèn chống cháy nổ 1m2
- Đèn chống cháy nổ 1m2 lắp cao bao nhiêu là hợp lý?
- Có dùng bóng tuýp LED thường thay bóng trong máng chống nổ được không?
- Đèn chống nổ 1m2 có dùng ngoài trời được không? (theo IP và thông tin hãng)
- Đèn chống cháy nổ 1m2 đôi tốn bao nhiêu điện mỗi tháng? (chỉ khi có công suất model có nguồn, ghi "ước tính")

H2: Chọn đèn chống cháy nổ 1m2 theo từng khu vực
- Kết bài: khuyến nghị dạng "chọn ... khi ...": kho nhỏ trần 3-4 m, hành lang và phòng pha chế, khu trần trên 5-6 m; không kết luận hãng nào hơn; CTA ở cuối.

**5. Dữ liệu cần dùng và nguồn** (chi tiết, trạng thái từng nguồn ở `du_lieu_mau.md`):
- HALEDCO: model, thông số, ký hiệu Ex, giá từ haledco.com (không link trong bài, ghi URL ở phần C). Phiên 29/10 **không vào được** haledco.com (proxy 403).
- Rạng Đông: https://rangdong.com.vn/bo-den-led-chong-no-pr1928.html. **Không đọc được** (tên miền ngoài danh sách mạng được phép).
- Philips: https://congtydenled.com.vn/blog/tu-van/den-chong-no/den-chong-no-philips.html (trang bán hàng, không phải trang hãng). **Không đọc được**.
- Điện Quang: https://dienquang.com/products/bo-den-led-mica-dien-quang-dq-ledmf02-36-nguon-tich-hop. **Không đọc được**; theo slug là "bộ đèn LED mica", nhiều khả năng không phải đèn chống nổ.
- Duhal, Paragon, Athaco: website chính thức của hãng, chưa có link, chưa đọc.
- Giá hãng khác: khoảng giá thị trường, nguồn và ngày ở phần C, không link.
- Mã IP: TCVN 4255:2025 / IEC 60529 (đã kiểm). Độ rọi: TCVN 7114-1:2008, QCVN 22:2016/BYT (đã kiểm), trích đúng bảng.
- Ký hiệu Ex: IEC 60079 và TCVN tương đương chưa có trong `tieu_chuan_da_kiem.csv`, tra và thêm trước khi viết, không được thì [CẦN KIỂM TRA].
- Không dùng bất kỳ số nào của bài 3904.

**6. Câu hỏi cho người dùng:**
1. Phiên cloud không vào được haledco.com, rangdong.com.vn, congtydenled.com.vn, dienquang.com (mạng phiên chặn). Bạn mở các tên miền này (và trang chính thức của Duhal, Paragon, Athaco) trong cài đặt mạng của môi trường cloud, hoặc dán thông số, giá của từng mẫu vào bảng? Nếu không, phần lớn bảng mẫu sẽ là [CẦN BỔ SUNG], vượt 5 chỗ ở phần B nên chưa đăng nháp được.
2. Link Điện Quang (DQ LEDMF02 36) theo tên là "bộ đèn LED mica nguồn tích hợp", có thể không phải đèn chống cháy nổ. Bạn có model Điện Quang chống nổ 1m2 khác không? Không có thì bỏ H3 Điện Quang.
3. Thông số Philips lấy từ trang bán hàng congtydenled.com.vn (không phải trang Philips) có được không, hay chỉ dùng trang này cho khoảng giá?

**7. Gợi ý link:**
- Link nội bộ trong bài:
  - "đèn huỳnh quang chống cháy nổ" -> /tu-van/den-huynh-quang-chong-chay-no/ (H3 bóng LED hay huỳnh quang)
  - "tiêu chuẩn đèn chống cháy nổ" -> /tu-van/tieu-chuan-den-chong-chay-no/ (H3 đọc ký hiệu Ex)
  - "đèn LED highbay chống cháy nổ" -> /tu-van/den-led-highbay-chong-chay-no/ (H3 khi nào không nên dùng 1m2)
  - "máng đèn chống cháy nổ" -> /tu-van/mang-den-chong-chay-no/ (H3 khi nào không nên dùng 1m2, đoạn máng rời)
  - Danh mục: "đèn LED nhà xưởng 50W" -> https://denlednhaxuongcaocap.com/den-led-nha-xuong-50w/ (kết bài, khu không có khí, hơi dễ cháy). Website chưa có danh mục chống cháy nổ nên chỉ 1 link danh mục.
- Link ngoài: trang IEC về IEC 60079 [CẦN KIỂM TRA URL], chỉ khi bài nêu tiêu chuẩn. Không link trang hãng hay cửa hàng.
- Link từ bài cũ về bài này (phần C khi viết):
  - /tu-van/mang-den-chong-chay-no/: mục "Máng đèn chống cháy nổ 1m2 đơn", anchor "đèn chống cháy nổ 1m2"
  - /tu-van/den-tuyp-led-chong-chay-no/: mục "Bóng đèn chống cháy nổ 1 2m", anchor "đèn tuýp LED chống cháy nổ 1m2"
  - /tu-van/den-chong-chay-no-0-6m/: đoạn so sánh chiều dài, anchor "đèn chống nổ 1m2"
  - /tu-van/bang-bao-gia-den-led-chong-chay-no/: phần đèn tuýp, anchor "giá đèn chống cháy nổ 1m2"

**8. CTA:** bạn gửi loại khu vực (khí, hơi, bụi, vùng nguy hiểm nếu đã có), kích thước phòng, chiều cao lắp; HLB gợi ý loại đơn hay đôi, số bộ, cách bố trí và báo giá các mẫu HLB phân phối, gọi hoặc Zalo 0967569588.

**9. Chủ đề nên viết bài riêng:** không có chủ đề mới; "máng đèn chống cháy nổ" (3922), "đèn tuýp LED chống cháy nổ" (7308), "đèn chống cháy nổ 0.6m" (4147) đã có bài, nên cập nhật dần theo cùng chuẩn sau khi bài 1m2 xong. Nếu người dùng muốn từ khóa theo hãng ("đèn chống cháy nổ Duhal", "Paragon") thì để bài riêng sau.
