# Bước 1: Nghiên cứu SERP "đèn chống cháy nổ 250w"

Ngày kiểm tra: 30/10/2026. Nguồn: top Google Việt Nam qua SerpApi (`tools/nghien_cuu.py serp`, lưu ở `serp/_ket_qua_den-chong-chay-no-250w.json`). Google chỉ trả 8 kết quả tự nhiên (tổng 133 kết quả, "Results for exact spelling"), không có mục "Mọi người cũng hỏi" và "Tìm kiếm liên quan". SerpApi trả link dạng chuyển hướng `/goto?url=...`, nên tên miền lấy từ trường `displayed_link` của cùng lần gọi.

**Kết luận nhanh: CAN_XU_LY.** Website đã có bài **4098** đúng từ khóa, đúng slug `den-chong-chay-no-250w`, cùng dạng toplist. Viết bài mới cùng slug sẽ thành `den-chong-chay-no-250w-2` và hai bài cùng nhắm một từ khóa. Đề xuất viết lại bài 4098 (mục 4).

## Top 8 Google VN

| # | Trang | Loại |
|---|---|---|
| 1 | ledmart.vn `/den-chong-chay-no`, "Đèn chống cháy nổ tốt nhất, Giá ưu đãi nhất tại Ledmart" | Trang danh mục (đã mở: lưới sản phẩm chống nổ Soho Lighting, có SH-FL1EX-250W đèn pha, SH-HB5-250SMD highbay, giá "Liên hệ") |
| 2 | shopee.vn, "Vỏ Đèn Chống Cháy Nổ Tròn 250W 400W" | Trang sản phẩm (vỏ đèn dùng bóng truyền thống, không phải đèn LED) |
| 3 | vattudienpower.com `/thuong-hieu/soho-lighting`, "Đại lý phân phối đèn Led chống cháy nổ Soho Lighting" | Trang danh mục theo thương hiệu |
| 4 | thanhdatled.com (chuyên mục Đèn pha led), "Đèn led chống nổ 50w 100w 150w 200w 250w 300w 400w" | Trang sản phẩm (nhiều mức công suất) |
| 5 | lightingviet.com (chuyên mục Đèn Công Nghiệp), "Đèn chống cháy nổ chính hãng" | Trang danh mục (theo đường dẫn chuyên mục và đoạn trích) |
| 6 | hasoco.vn, "Đèn phòng chống cháy nổ model BCD-250 bóng LED 50w Rạng Đông" | Trang sản phẩm. "250" là mã vỏ BCD-250, công suất bóng 50W, không phải đèn 250W |
| 7 | elmall.vn `/den-chong-chay-no-250w-tron-bcd-250-paragon/`, "Đèn chống cháy nổ 250W tròn BCD 250 Paragon" | Trang sản phẩm (đoạn trích nói "bóng đèn ... 250W ... 220V/50Hz", nhiều khả năng vỏ chống nổ cho bóng truyền thống) |
| 8 | elmall.vn `/den-chong-chay-no`, "Đèn chống cháy nổ, Elmall Electric & Lighting" | Trang danh mục |

Mở được: ledmart.vn (HTTP 200). Proxy chặn elmall.vn, lightingviet.com, hasoco.vn (403); thanhdatled.com chỉ mở được trang chủ, link bài trong SERP là link chuyển hướng không giải được. Phân loại các trang còn lại dựa trên đường dẫn hiển thị, tiêu đề, đoạn trích. **Không có bài blog nào trong top**, nên không có văn bản bài top để lưu bằng `luu-serp`.

## 1. Search intent

Người tìm "đèn chống cháy nổ 250w" đã biết cần đèn chống nổ công suất lớn, nên ý định chính là **chọn mua (giao dịch)**: xem mẫu, thông số chống nổ, giá, nơi bán. SERP còn cho thấy một nhóm người mua **thay thế bộ đèn chống nổ dùng bóng truyền thống 250W** (vỏ tròn BCD 250, vỏ Shopee 250W/400W), tức là đang dò đèn LED thay cho bóng cao áp 250W cũ.

## 2. Định dạng nội dung

- **Bằng chứng:** 8/8 kết quả là trang bán hàng: 4 trang danh mục (#1, #3, #5, #8), 4 trang sản phẩm (#2, #4, #6, #7). **0 bài blog, 0 bài toplist.** Google hiểu truy vấn là ý định mua.
- **Định dạng phù hợp nhất theo SERP:** trang danh mục "đèn chống cháy nổ" có lọc theo công suất. `python tools/danh_muc.py tim "đèn chống cháy nổ 250w"`: **KHÔNG KHỚP**, website không có danh mục chống cháy nổ. CSV `du_lieu_san_pham_HLB_30-10-2026.csv` (113 model) không có model chống nổ nào (tìm "chống nổ", "chống cháy", "HLEP", "Ex d": 0 dòng). Không chuyển được sang Agent Danh mục; làm danh mục thì phải tạo danh mục và đăng sản phẩm, ngoài phạm vi Agent Blog.
- **Danh mục 250W hiện có không thay được:** `den-led-nha-xuong-250w` (10 sản phẩm) là đèn nhà xưởng thường, không có mẫu chống nổ, không tối ưu cho từ khóa này được.
- **Nếu vẫn làm blog:** dạng gần ý định mua nhất là toplist (nhiều mẫu 250W có tên, thông số, giá) kèm hướng dẫn chọn. Khả năng lên top 3 thấp (SERP 100% trang bán hàng); vào top 10 ở mức trung bình (SERP chỉ 8 kết quả, nhiều trang lệch: #2, #6, #7 là vỏ đèn hoặc "250" là mã vỏ). Bằng chứng ngược chiều: bài 4098 đúng từ khóa đã có từ 2020 nhưng không có mặt trong 8 kết quả.

## 3. Gộp hay tách

SerpApi không trả truy vấn liên quan. Đề xuất theo SERP và bài đã có trên website:
- **Gộp vào bài (từ khóa phụ đề xuất, tối đa 5):**
  - "đèn led chống cháy nổ 250w" (cùng ý định, cách gọi đầy đủ)
  - "đèn chống nổ 250w" (cách gọi ngắn, #4 dùng)
  - "đèn highbay chống cháy nổ 250w" (#1 có highbay 250W; bài 3821 có mục này)
  - "đèn pha chống cháy nổ 250w" (#1, #4 là đèn pha)
  - "giá đèn chống cháy nổ 250w" (người mua cần giá trong cùng trang)
- **Tách hoặc không làm:**
  - "vỏ đèn chống cháy nổ 250w", "đèn chống cháy nổ BCD 250" (vỏ dùng bóng truyền thống, sản phẩm khác; có thể nhắc một đoạn "thay bộ đèn chống nổ bóng cao áp 250W bằng LED", không làm H2 riêng)
  - "đèn chống cháy nổ cao áp 250w" (đã có bài 3984 `den-cao-ap-chong-chay-no`)
  - Các mức 20W, 40W, 50W, 80W, 100W, 150W, 200W (mỗi mức một bài, mục 4)

## 4. Kiểm tra trùng chủ đề trên website

Tìm bằng REST API `/wp-json/wp/v2/posts?search=250w`, `?search=chống cháy nổ`, `?slug=den-chong-chay-no-250w` ngày 30/10/2026.

**Trùng trực tiếp:**

| ID | Bài | URL | Ngày | Mức trùng |
|---|---|---|---|---|
| **4098** | TOP 9 đèn chống cháy nổ 250w tốt nhất, Báo giá chi tiết 2023 | https://denlednhaxuongcaocap.com/tu-van/den-chong-chay-no-250w/ | đăng 06/05/2020, sửa 08/12/2023 | **Trùng hoàn toàn**: cùng từ khóa, cùng dạng toplist, slug trùng đúng slug dự kiến `Bai_den-chong-chay-no-250w` |

**Trùng một phần:**

| ID | Bài | URL | Phần trùng |
|---|---|---|---|
| 3821 | TOP 5 công suất đèn LED Highbay chống cháy nổ bán chạy (sửa 23/07/2026) | /tu-van/den-led-highbay-chong-chay-no/ | H2 "5. Đèn LED highbay chống cháy nổ 250W", nêu HLEP2-250W, HLEP1-250W, giá 3.350.000-8.050.000 đồng |
| 3979 | Bảng báo giá đèn LED chống cháy nổ các thương hiệu lớn (sửa 20/07/2026) | /tu-van/bang-bao-gia-den-led-chong-chay-no/ | Dòng "Đèn chống cháy nổ cao áp 250W 1.300.000-1.900.000" |
| 3984 | Đèn cao áp chống cháy nổ | /tu-van/den-cao-ap-chong-chay-no/ | Bộ đèn chống nổ bóng cao áp (trùng ý "thay bóng 250W truyền thống") |

**Đề xuất:** không viết bài mới song song. **Viết lại bài 4098** trên URL cũ (đặt `id_bai_cu = 4098`, đăng bản nháp `--update 4098`), giữ URL đã có tuổi từ 2020 và liên kết. Tên file `Bai_den-chong-chay-no-250w.md` giữ được vì trùng đúng slug bài cũ. Cách làm giống hướng đã đề xuất cho bài 100W (3874). Bài 3821 nên rút gọn mục 250W và trỏ link về bài 4098 viết lại để không mâu thuẫn giá.

### Bảng Giữ/Bỏ ý của bài 4098 (đọc toàn bài qua REST API ngày 30/10/2026, khoảng 1.690 từ, 10 H2)

| Nhóm | Ý trong bài 4098 | Lý do |
|---|---|---|
| **Giữ** | Khung toplist: mỗi mẫu có thông số, giá, ưu nhược | Đúng dạng gần intent mua, viết lại theo Knowledge 8.5 |
| **Giữ** | Phân loại 250W theo dạng: highbay (COB, SMD), đèn pha, bộ đèn bóng cao áp metal halide E40 | Dùng làm cách nhóm danh sách; dạng bóng cao áp dùng cho đoạn "thay đèn cao áp 250W bằng LED" |
| **Giữ** | Ý "250W là công suất lớn, ít đơn vị sản xuất, khó tìm mua" và dùng cho xưởng rộng, trần cao | Viết lại có điều kiện chiều cao lắp, không khẳng định chung |
| **Giữ** | Nhược điểm bộ đèn chống nổ bóng cao áp: tuổi thọ thấp, tốn điện, phải thay bóng | Đúng về bản chất, viết lại không kèm số "gấp 3 lần" |
| **Bỏ vì sai hoặc lỗi thời** | Mục 1, 2, 5, 9 không có tên hãng, mã model ("chip COB", "pha led", "LED bulb", "nhà xưởng 250w"), thông số không nguồn | Vi phạm quy tắc dữ liệu: không có model thì không kiểm được |
| **Bỏ vì sai hoặc lỗi thời** | Bảng HALEDCO 250W và Paragon 250W giống hệt nhau (85-265V, 32.500 lm, 130 lm/W, IP66, 50.000 giờ) | Hai hãng trùng từng con số, nhiều khả năng chép; mục 5 LED bulb cũng 32.500 lm, 130 lm/W |
| **Bỏ vì sai hoặc lỗi thời** | Toàn bộ giá (542.000-9.755.000 đồng) | Không nguồn, không ngày, mâu thuẫn bài 3821 (3.350.000-8.050.000) |
| **Bỏ vì sai hoặc lỗi thời** | Duhal LSC250: IP54, 75Ra, giá 542.000-1.430.000 đồng | IP54 và giá này không giống đèn chống nổ, cần xác minh model; không có ký hiệu Ex |
| **Bỏ vì sai hoặc lỗi thời** | "Rạng Đông 250w" không có mã model, 30.000 giờ, IP65 | Không kiểm được; CSV không có model chống nổ Rạng Đông |
| **Bỏ vì sai hoặc lỗi thời** | "Exd II BT4", "Exd IIC T6", "Ex demb IIC T6 Gb" ghi như tiêu chuẩn, "Chứng nhận Exd II, CE, RoHS, IEC" | Ký hiệu Ex chỉ ghi khi có nguồn của đúng model; "IEC" không phải chứng nhận |
| **Bỏ vì sai hoặc lỗi thời** | Mục 10 "Công ty HALEDCO ... uy tín hàng đầu", "đạt chuẩn ATEX", "tiết kiệm điện gấp 3 lần", "tuổi thọ trên 65000 giờ", "bảo hành 2 năm; chiết khấu 45%", câu "Haledco là đơn vị bán ... uy tín hàng đầu" ở mục 1.3 | Dẫn khách sang HALEDCO, từ tuyệt đối, số liệu và chính sách không nguồn |
| **Bỏ vì sai hoặc lỗi thời** | Link "Xem thêm: Top 7 đèn chống cháy nổ Philips ... 2022" | Anchor lỗi thời; bài 3865 không có mã model, không nên trỏ tới |
| **Bỏ vì ngoài phạm vi** | Trạm xăng diện tích rộng (ảnh "ứng dụng tại trạm xăng") | Giữ một dòng nếu cần, trọng tâm là kho, xưởng, nhà máy |

## 5. Kiểm tra phạm vi

Thuộc phạm vi: đèn chống cháy nổ là chủ đề phụ đã có bài (Knowledge mục 4), dùng cho kho hóa chất, xưởng sơn, nhà máy có hơi dung môi, kho xăng dầu. Giàn khoan, tàu, nhà máy lọc dầu (bài 3821 có nhắc) ngoài trọng tâm, không đưa vào bài.

## Dữ liệu model: tình trạng xác minh

- CSV 30/10/2026: không có model chống nổ. Website không có danh mục, trang sản phẩm chống nổ.
- Tên model 250W thật đã thấy (chưa xác minh thông số trong phiên này):

| Model | Hãng | Dạng | Thấy ở | Dữ liệu đã thấy |
|---|---|---|---|---|
| SH-HB5-250SMD | Soho Lighting | highbay SMD | SERP #1 (ledmart) | tên, giá "Liên hệ" |
| SH-FL1EX-250W | Soho Lighting | đèn pha | SERP #1 (ledmart) | tên, giá "Liên hệ" |
| HLEP2-250W, HLEP1-250W | HALEDCO | highbay | bài 3821 | tên; thông số trong bài không gắn model |
| BCD 250 | Paragon | vỏ chống nổ bóng truyền thống | SERP #7 | không mở được |
| LSC250 | Duhal | không rõ | bài 4098 | IP54, 75Ra (nghi sai) |

Nếu người dùng chọn viết lại bài 4098, cần catalogue hoặc trang hãng cho từng mẫu trước khi lập outline; mẫu nào không có nguồn thì bỏ khỏi danh sách. Tối thiểu 5 mẫu có nguồn mới viết dạng toplist; không đủ thì đổi sang dạng hướng dẫn chọn đèn chống nổ 250W (ít mẫu, nhiều phần cách chọn).

## Câu hỏi cho người dùng

1. Website đã có bài 4098 "TOP 9 đèn chống cháy nổ 250w tốt nhất" trùng hoàn toàn từ khóa và slug. Bạn đồng ý viết lại bài này (`id_bai_cu = 4098`, bản nháp cập nhật) thay vì bài mới không?
2. SERP 8/8 là trang bán hàng, 0 bài blog, và bài 4098 cũng không vào top. Bạn vẫn làm blog (chấp nhận khả năng top 3 thấp), hay tạm dừng từ khóa này?
3. HLB có phân phối hoặc nhận báo giá đèn chống nổ 250W của hãng nào không (HALEDCO, Soho Lighting, Paragon, Duhal, hãng khác)? Có catalogue, datasheet (quang thông, ký hiệu Ex đầy đủ, IP, bảo hành) và giá cho từng mẫu không?
4. Muốn giữ dạng toplist (cần tối thiểu 5 mẫu có nguồn) hay đổi sang dạng hướng dẫn chọn đèn chống nổ 250W (ít mẫu hơn)?
5. Bạn có muốn gom các bài theo công suất (20W, 40W, 50W, 80W, 100W, 250W) thành một kế hoạch viết lại trên URL cũ, và rút gọn mục 250W trong bài 3821 để không trùng giá không?

## Bổ sung ngày 25/11/2026

- CSV mới `du_lieu_san_pham_HLB_25-11-2026.csv`: vẫn 0 model chống nổ; `danh_muc.py tim "đèn chống cháy nổ 250w"` vẫn KHÔNG KHỚP.
- Đã mở 2 trang sản phẩm Soho trên ledmart.vn (trang bán hàng, không phải trang hãng). SH-HB5-250SMD: 250W, D320mm, IP65, bảo hành 24 tháng, giá "Liên Hệ". SH-FL1EX-250W: 250W, D330mm, IP65, bảo hành 24 tháng, giá "Liên Hệ". Cả hai không có quang thông, điện áp, ký hiệu Ex, vật liệu, chứng nhận. Không đủ 5 mẫu có nguồn, nên outline dùng dạng hướng dẫn chọn.
- Người dùng trả lời câu 1-2: "Giữ nội dung bài Blog cũ, viết nháp bản mới" (hiểu: bản nháp cập nhật cho 4098, bài cũ giữ nguyên). Câu 3-5 chưa trả lời.
- Không có bài blog trong top nên không có văn bản để `luu-serp`.
