# Bước 1: Nghiên cứu SERP "đèn pha chống cháy nổ"

Ngày kiểm tra: 30/10/2026. Nguồn: top Google Việt Nam qua SerpApi (desktop, `google.com.vn`, `gl=vn`, `hl=vi`), lưu ở `serp/_ket_qua_den-pha-chong-chay-no.json`.

**Lưu ý về dữ liệu SERP:** lần chạy `tools/nghien_cuu.py serp` lúc 09:22 nhận về kết quả cache sai của SerpApi (PHA trong mỹ phẩm, đèo Pha Đin, máy pha cà phê, không liên quan). Đã gọi lại SerpApi với `no_cache=true` lúc 09:30 (trang 1 và trang 2), file JSON trên đã được thay bằng kết quả mới này. Google chỉ trả 8 kết quả tự nhiên ở trang 1 (tổng khoảng 125 kết quả, "Results for exact spelling"), không có "Mọi người cũng hỏi"; "Tìm kiếm liên quan" chỉ có 2 cụm chung chung ("Đèn LED công nghiệp", "Công ty đèn"). Link SerpApi trả dạng chuyển hướng `/goto?url=...`, tên miền lấy từ trường `displayed_link`.

**Kết luận nhanh: CAN_XU_LY.** Website đã có bài **4018** đúng từ khóa, đúng slug `den-pha-chong-chay-no`, cùng dạng toplist kèm giá. Viết bài mới với tên file `Bai_den-pha-chong-chay-no.md` sẽ ra slug `den-pha-chong-chay-no-2` và hai bài cùng nhắm một từ khóa. Đề xuất viết lại bài 4018 trên URL cũ (mục 4).

## Top Google VN (trang 1)

| # | Trang | Loại |
|---|---|---|
| 1 | ledmart.vn `/den-chong-chay-no`, "Đèn chống cháy nổ tốt nhất, Giá ưu đãi nhất tại Ledmart" | Trang danh mục (đã mở, HTTP 200: lưới sản phẩm chống nổ, có 5 đèn pha Soho Lighting SH-FL1EX 60W, 100W, 150W, 200W, 250W, cùng highbay, máng, đèn sự cố) |
| 2 | denledviet.com.vn `/den-led-chong-chay-no`, "ĐÈN LED CHỐNG CHÁY NỔ" | Trang danh mục (theo đường dẫn và đoạn trích; proxy chặn, chưa mở được) |
| 3 | tranphucable.com.vn `/tin-thi-truong/...`, "Đèn led chống cháy nổ: Khái niệm, tiêu chuẩn, phân loại" | Bài blog kiến thức chung về đèn chống nổ (đoạn trích có nhắc đèn pha LED chống nổ). Không mở được (máy và WebFetch đều bị chặn tên miền) |
| 4 | thanhdatled.com (chuyên mục Đèn pha led), "Đèn led chống nổ 50w 100w 150w 200w 250w 300w 400w" | Trang sản phẩm đèn pha chống nổ nhiều công suất |
| 5 | Facebook, "ĐÈN PHA CHỐNG NỔ, GIẢI PHÁP CHIẾU SÁNG AN..." | Bài đăng quảng cáo của nhà phân phối (Soho Lighting) |
| 6 | thietbidienhaidang.vn, "Đèn pha chống cháy nổ LED Tích điện, dùng trong hầm mỏ" | Trang sản phẩm, thực chất là **đèn báo** (xanh, đỏ, vàng), lệch nghĩa |
| 7 | hasoco.vn (chuyên mục ĐÈN LED CHỐNG CHÁY NỔ), "Đèn Led pha chống cháy nổ" | Trang danh mục hoặc sản phẩm đèn pha chống nổ |
| 8 | hasoco.vn, "Đèn chiếu sáng sự cố phòng nổ HASOCO" | Trang sản phẩm đèn sự cố, lệch loại đèn |

Trang 2 (vị trí 11-19): 8/9 là trang sản phẩm hoặc danh mục (polyled, hasoco 50W Philips, vinalighting, hoangphatlighting, Warom HRT82, tuvaco...), 1 bài Facebook. Ảnh inline của Google toàn ảnh sản phẩm đèn pha chống nổ (Duhal DCN2200, Lizuvi BAT95T, EFL02, PVN19, BAT86, HASOCO 400W, HALEDCO HLEP FL3-250W...).

## 1. Search intent

Người tìm "đèn pha chống cháy nổ" đã biết loại đèn cần (đèn pha, vỏ phòng nổ) và muốn **chọn mua**: xem mẫu, công suất, ký hiệu chống nổ, giá, nơi bán. Một phần nhỏ muốn tìm hiểu khái niệm, tiêu chuẩn chống nổ (kết quả #3). Google hiểu truy vấn khá rộng, gộp chung với "đèn chống cháy nổ" nói chung (đèn sự cố, đèn báo, đèn tuýp cũng vào top).

## 2. Định dạng nội dung

- **Bằng chứng:** trang 1 có 6/8 kết quả là trang bán hàng (3 danh mục #1, #2, #7; 3 sản phẩm #4, #6, #8), 1 bài Facebook, **chỉ 1 bài blog** (#3, kiến thức chung, không phải toplist đèn pha). Trang 2 có 8/9 là trang bán hàng. Định dạng Google ưu tiên: **trang danh mục sản phẩm đèn chống nổ**, lọc được dạng đèn pha.
- **Website chưa có chỗ chuyển sang Agent Danh mục:** `python tools/danh_muc.py tim "đèn pha chống cháy nổ"`: **KHÔNG KHỚP**. REST WooCommerce (`/wc/store/v1/products?search=chống cháy nổ`, `?search=pha`): 0 sản phẩm; 30 danh mục, không có danh mục nào về chống nổ hoặc đèn pha. CSV `du_lieu_san_pham_HLB_30-10-2026.csv`: 0 dòng chứa "chống nổ", "chống cháy", "HLEP", "Ex d", "pha". Làm danh mục thì phải tạo danh mục và đăng sản phẩm đèn pha chống nổ trước, ngoài phạm vi Agent Blog.
- **Nếu làm blog:** dạng gần intent mua nhất là toplist (5 mẫu đèn pha chống nổ có model, ký hiệu Ex, thông số, giá) kèm phần chọn đèn theo khu vực nguy hiểm. Khả năng lên top 3 thấp (SERP gần như toàn trang bán hàng), vào top 10 ở mức trung bình (SERP chỉ 8 kết quả tự nhiên, 3 kết quả lệch loại đèn: #6, #8, #5). Bằng chứng ngược chiều: bài 4018 đúng từ khóa có từ 2020 nhưng không có mặt trong 19 kết quả của 2 trang đầu.

## 3. Gộp hay tách

SerpApi không trả truy vấn liên quan hữu ích. Đề xuất từ khóa phụ theo tiêu đề, đoạn trích SERP và bài đã có trên website (tối đa 5, dùng khi viết lại bài 4018):

- **Giữ trong bài:**
  1. "đèn pha led chống cháy nổ" (cách gọi đầy đủ, #3, #7 và ảnh inline dùng)
  2. "đèn pha chống nổ" (cách gọi ngắn, #4, #5 dùng)
  3. "đèn pha phòng nổ" (cách gọi theo ký hiệu "phòng nổ", ledmart và Facebook dùng "đèn pha phòng cháy nổ")
  4. "giá đèn pha chống cháy nổ" (bài 4018 và SERP đều có giá, cùng intent mua; một bảng giá trong bài, không tách bài)
  5. "đèn pha chống cháy nổ 100w 150w 200w" (SERP #4, ledmart, ảnh inline chia theo công suất; dùng làm cột công suất trong bảng, không làm H2 riêng từng mức)
- **Tách hoặc không làm:**
  - "đèn báo pha chống cháy nổ" (đèn báo hiệu, intent khác; đã có bài 5309 `den-bao-pha-chong-chay-no`)
  - "đèn sự cố, đèn khẩn cấp chống cháy nổ" (đã có bài 3949, 3886)
  - "đèn highbay chống cháy nổ" (đã có bài 3821)
  - "đèn pha led nhà xưởng" thường, không chống nổ (đã có bài 7251)
  - "đèn pha chống cháy nổ tích điện, hầm mỏ" (#6, hầm mỏ ngoài trọng tâm nhà xưởng)

## 4. Kiểm tra trùng chủ đề trên website

Tìm bằng REST API ngày 30/10/2026: `/wp-json/wp/v2/posts?slug=den-pha-chong-chay-no`, `/wp-json/wp/v2/pages?slug=den-pha-chong-chay-no`, `?search=pha chống cháy nổ`, `?search=chống cháy nổ`, `?search=đèn pha`, `?search=chống nổ`, `?search=phòng nổ`.

**Trùng trực tiếp:**

| ID | Bài | URL | Ngày | Mức trùng |
|---|---|---|---|---|
| **4018** | TOP 5 đèn pha chống cháy nổ tốt, Báo giá chi tiết 2026 | https://denlednhaxuongcaocap.com/tu-van/den-pha-chong-chay-no/ | đăng 28/04/2020, sửa 23/07/2026 | **Trùng hoàn toàn**: cùng từ khóa, cùng dạng toplist kèm giá, slug trùng đúng slug dự kiến của `Bai_den-pha-chong-chay-no.md` |

Không có trang (page) hay sản phẩm nào cùng slug hoặc nhắm từ khóa này.

**Trùng một phần:**

| ID | Bài | URL | Phần trùng |
|---|---|---|---|
| 5309 | TOP 7 đèn báo pha chống cháy nổ chuẩn Exd II... | /tu-van/den-bao-pha-chong-chay-no/ | Chữ "pha" trùng, nhưng là đèn báo hiệu, khác intent; cần phân biệt rõ trong bài |
| 3821 | TOP 5 công suất đèn LED Highbay chống cháy nổ bán chạy | /tu-van/den-led-highbay-chong-chay-no/ | Cùng nhóm đèn chống nổ công suất lớn, khác dạng đèn |
| 3979 | Bảng báo giá đèn LED chống cháy nổ các thương hiệu lớn | /tu-van/bang-bao-gia-den-led-chong-chay-no/ | Có thể có giá đèn pha chống nổ, cần đối chiếu để giá hai bài không mâu thuẫn |
| 3874, 4098 | Đèn LED chống cháy nổ 100W, đèn chống cháy nổ 250W | /tu-van/den-led-chong-chay-no-100w/, /tu-van/den-chong-chay-no-250w/ | Cùng nêu các mẫu đèn pha (HLEP FL3, BZD129, Duhal DCN) theo công suất |
| 7251 | 150+ đèn pha LED nhà xưởng 50w 100w 150w 200w giá rẻ | /tu-van/den-pha-led-nha-xuong/ | Đèn pha nhà xưởng thường, không chống nổ |

**Đề xuất:** không viết bài mới song song. **Viết lại bài 4018** trên URL cũ (đặt `id_bai_cu = 4018`, đăng bản nháp dạng cập nhật bài 4018), giữ URL đã có tuổi từ 2020 và liên kết nội bộ. Tên file `Bai_den-pha-chong-chay-no.md` giữ được vì trùng đúng slug bài cũ. Cách làm giống hướng đã đề xuất cho bài 100W (3874) và 250W (4098).

### Bảng Giữ/Bỏ ý của bài 4018 (đọc toàn bài qua REST API ngày 30/10/2026, khoảng 1.710 từ, 5 H2, 15 H3)

| Nhóm | Ý trong bài 4018 | Lý do |
|---|---|---|
| **Giữ** | Khung toplist: mỗi mẫu có thông số, giá, ưu nhược điểm | Đúng dạng gần intent mua, viết lại theo Knowledge mục 8.5 |
| **Giữ** | Phân biệt đèn pha chống nổ LED với bộ đèn pha chống nổ bóng cao áp | Dùng cho đoạn so sánh và thay đèn cao áp bằng LED (Knowledge mục 4) |
| **Giữ** | Giá phụ thuộc linh kiện: chip LED, nguồn (driver), vật liệu vỏ | Đúng về bản chất; viết lại không xếp hạng hãng chip, không khẳng định chênh giá cụ thể khi chưa có nguồn |
| **Giữ (cần xác minh lại)** | EEW BZD129-100/120: ký hiệu Ex nA e mc IIC T6 Gc / Ex tD A21 IP66 T80°C, giá 14.399.000 và 15.118.000 đồng | Có model và ký hiệu Ex đầy đủ; bài không ghi nguồn, ngày giá, phải đối chiếu tài liệu hãng |
| **Giữ (cần xác minh lại)** | Duhal DCN2050/2100/2150/2200: quang thông 5.500/11.000/16.500/21.000 lm, IP65, Ra 83, giá 6.154.000-11.672.000 đồng; nhận xét trang sản phẩm không ghi ký hiệu Ex | Có model, thông số theo công suất; phải đối chiếu trang Duhal (DCN2200 cũng xuất hiện trong ảnh inline SERP) |
| **Giữ** | Nhắc các khu vực nguy hiểm: lọc hóa dầu, xử lý chất thải, sản xuất giấy | Viết lại theo góc kho hóa chất, xưởng sơn, nhà máy có hơi dung môi, bụi dễ cháy |
| **Bỏ vì sai hoặc lỗi thời** | Mở bài "đèn pha chống cháy nổ ... chiếu sáng công cộng" | Sai bản chất: đèn chống nổ dùng cho khu vực nguy hiểm, không phải chiếu sáng công cộng |
| **Bỏ vì sai hoặc lỗi thời** | HALEDCO HLEP FL3: thông số chung cho cả dải 30-500W (130 lm/W, 65.000 giờ, Ra 85, IP66, IECEx), giá 1.850.000-5.990.000 đồng | Không gắn model, công suất cụ thể (Knowledge mục 3.2); giá không nguồn, không ngày |
| **Bỏ vì sai hoặc lỗi thời** | "Tiết kiệm 70% điện năng", "chiếu sáng hiệu quả tốt nhất" | Câu cấm ở Knowledge mục 5, từ tuyệt đối |
| **Bỏ vì sai hoặc lỗi thời** | "Philips Exd IIC T6" không có mã model, thông số dải 30-300W, giá 1.450.000-4.500.000 đồng; nhược điểm "Hàng OEM lắp ráp trong nước chất lượng không đồng đều" | Không kiểm được model; câu nhược điểm mơ hồ, dễ thành hạ thấp (Instructions mục 7). Philips bảo hành và thông số lấy theo model trên signify.com |
| **Bỏ vì sai hoặc lỗi thời** | Mục "Đèn pha chống cháy nổ cao áp": không có hãng, model; "Chứng nhận ISO, CE, RoHS, IECEx", nặng 16,10 kg, giá 2.570.000-3.500.000 đồng | Không kiểm được nguồn |
| **Bỏ vì sai hoặc lỗi thời** | Câu dẫn "HALEDCO còn cung cấp đèn LED highbay 100w và đèn chống cháy nổ 0.6m" | Dẫn khách sang hãng khác thay vì HLB; viết lại theo vai trò HLB phân phối (Knowledge mục 1) |
| **Bỏ vì sai hoặc lỗi thời** | Link "Xem thêm: 9+ bóng đèn led chống cháy nổ" về bài 4031 (tiêu đề "HOT giá rẻ nhất 2023") | Anchor và bài đích lỗi thời; chọn link nội bộ lại ở Bước 2 |
| **Bỏ vì ngoài phạm vi** | Ứng dụng "chiếu sáng ngoài trời, đường phố", "chiếu sáng trên tàu" | Ngoài trọng tâm nhà xưởng, nhà kho, nhà máy (Knowledge mục 4) |

Bài 4018 không có link sang haledco.com (đã kiểm danh sách link trong bài). SEO title và meta description không đọc được qua REST (trường `yoast_head_json` trống).

## 5. Kiểm tra phạm vi

Thuộc phạm vi: đèn chống cháy nổ là chủ đề phụ đã có bài (Knowledge mục 4), đèn pha chống nổ dùng cho kho hóa chất, xưởng sơn, kho dung môi, nhà máy có khí hoặc bụi dễ cháy. Hầm mỏ, giàn khoan, tàu biển, trạm xăng ngoài trọng tâm, không làm phần riêng.

## Dữ liệu model: tình trạng xác minh

- CSV 30/10/2026: không có model chống nổ. Website không có danh mục, trang sản phẩm đèn chống nổ.
- Tên model đèn pha chống nổ thật đã thấy (chưa xác minh thông số trong phiên này, proxy chặn hầu hết trang hãng):

| Model | Hãng | Thấy ở | Dữ liệu đã thấy |
|---|---|---|---|
| SH-FL1EX-60W/100W/150W/200W/250W | Soho Lighting | SERP #1 (ledmart, đã mở) | tên, công suất |
| BZD129-100, BZD129-120 | EEW | bài 4018 | ký hiệu Ex, PF, Ra, giá (không nguồn) |
| DCN2050, DCN2100, DCN2150, DCN2200 | Duhal | bài 4018, ảnh inline SERP | quang thông, IP65, Ra 83, giá (không nguồn) |
| HLEP FL3 (dải 30-500W) | HALEDCO | bài 4018, ảnh inline SERP | thông số chung cả dải, không theo model |
| HRT82 | Warom | SERP trang 2 | tên |
| BAT95T, EFL02, BAT86, PVN19 | Lizuvi, DPKT, khác | ảnh inline SERP | tên |

Cần catalogue hoặc trang hãng cho từng mẫu trước khi lập outline; mẫu nào không có nguồn thì bỏ. Tối thiểu 5 mẫu có nguồn mới giữ dạng toplist; không đủ thì đổi sang dạng hướng dẫn chọn đèn pha chống nổ (ít mẫu, nhiều phần cách chọn theo vùng nguy hiểm, ký hiệu Ex, IP, công suất).

## Văn bản bài top đã lưu

Chưa lưu được: bài blog duy nhất trong top (#3 tranphucable.com.vn) bị chặn cả khi tải bằng máy (proxy 403) lẫn WebFetch (tên miền chưa nằm trong danh sách mạng cho phép của phiên). Các trang còn lại là danh mục, sản phẩm, Facebook, không cần lưu.

## Câu hỏi cho người dùng

1. Website đã có bài 4018 "TOP 5 đèn pha chống cháy nổ tốt, Báo giá chi tiết 2026" trùng hoàn toàn từ khóa và slug. Bạn đồng ý viết lại bài này (`id_bai_cu = 4018`, bản nháp cập nhật trên URL cũ) thay vì viết bài mới không?
2. SERP 6/8 trang 1 là trang bán hàng, chỉ 1 bài blog, và bài 4018 không vào top 19. Bạn vẫn làm blog (chấp nhận khả năng top 3 thấp), hay muốn hướng danh mục: "Danh mục chưa có sẵn trên website, bạn cần tạo danh mục để Agent viết bài." Đề xuất tên "Đèn pha LED chống cháy nổ", slug `den-pha-led-chong-chay-no`, cha là danh mục mới "Đèn LED chống cháy nổ" (slug `den-led-chong-chay-no`, cấp 1, ngang các danh mục theo công suất); cả hai slug chưa bị bài nào dùng (kiểm REST 30/10/2026). Hướng này cần đăng sản phẩm đèn pha chống nổ trước (hiện website 0 sản phẩm chống nổ), rồi mới chuyển Agent Danh mục.
3. HLB có phân phối hoặc nhận báo giá đèn pha chống nổ của hãng nào (HALEDCO HLEP FL3, Duhal DCN, EEW BZD129, Soho Lighting SH-FL1EX, hãng khác) không? Có catalogue, datasheet (quang thông, ký hiệu Ex đầy đủ, IP, bảo hành) và giá theo từng model không?
4. Muốn giữ dạng toplist (cần tối thiểu 5 mẫu có nguồn) hay đổi sang dạng hướng dẫn chọn đèn pha chống nổ (ít mẫu hơn)?
5. Đồng ý bộ từ khóa phụ ở mục 3 (đèn pha led chống cháy nổ, đèn pha chống nổ, đèn pha phòng nổ, giá đèn pha chống cháy nổ, đèn pha chống cháy nổ 100w 150w 200w) không?
