# Bước 1: Nghiên cứu SERP "đèn led chống cháy nổ 100w"

Ngày kiểm tra: 28/10/2026. Nguồn: top Google Việt Nam qua SerpApi (`tools/nghien_cuu.py serp`, lưu ở `serp/_ket_qua_den-led-chong-chay-no-100w.json`). Google chỉ trả 8 kết quả tự nhiên, không có mục "Mọi người cũng hỏi" và "Tìm kiếm liên quan".

Loại bài người dùng chọn: blog dạng Toplist (ghi chú người dùng: "Từ khóa này thường sẽ SEO cho danh mục, nhưng nếu tôi muốn viết cho Blog dạng Toplist thì sao?").

## Top 8 Google VN

| # | Trang | Loại (theo URL, tiêu đề, đoạn trích) |
|---|---|---|
| 1 | tdllighting.com, "Đèn LED nhà xưởng chống nổ 100w" (`/san-pham/`) | Trang sản phẩm |
| 2 | denhoanggia.vn, "Đèn pha led chống cháy nổ" (`/danh-muc/`) | Trang danh mục |
| 3 | denchieusangled.vn, "Đèn led highbay chống chảy nổ 100w SMD ... mã SP ZHB-CCN-100 ZALAA" | Trang sản phẩm |
| 4 | Trang danh mục đèn LED chống cháy nổ của HALEDCO | Trang danh mục (có đoạn tư vấn công suất) |
| 5 | Trang sản phẩm HLEP2-100W của HALEDCO | Trang sản phẩm |
| 6 | zalaa.vn, "Đèn led Highbay nhà xưởng UFO chống cháy nổ 100w mã ZHB150COB-CCN" | Trang sản phẩm |
| 7 | hasoco.vn, "Đèn led chống cháy nổ Duhal dạng pha 100W FCN1001" | Trang sản phẩm |
| 8 | hasoco.vn, "Đèn led chống cháy nổ 100w giá cả cạnh tranh, cung cấp toàn quốc uy tín" | Nhiều khả năng là trang sản phẩm (tiêu đề và đoạn trích kiểu trang bán hàng, có hotline mua hàng) |

Phiên này không mở được các trang trên: proxy chặn tdllighting.com, denchieusangled.vn, zalaa.vn, hasoco.vn, haledco.com (lỗi 403, không phân giải tên miền). Phân loại dựa trên URL, tiêu đề, đoạn trích. Vì không có bài blog nào trong top nên không có văn bản bài top để lưu bằng `luu-serp`; `kiem_tra_bai.py` sẽ không có dữ liệu để so đoạn chép (chấp nhận được, vì không có bài blog đối thủ).

## 1. Search intent

Người tìm "đèn led chống cháy nổ 100w" đã biết cần đèn chống nổ và đã chọn mức công suất, nên ý định chính là **chọn mua (giao dịch thương mại)**: xem mẫu cụ thể, thông số chống nổ, giá, nơi bán. Ý định phụ là so sánh vài mẫu 100W trước khi hỏi giá. Người đọc thường là bộ phận mua hàng, nhà thầu cơ điện của kho hóa chất, xưởng sơn, trạm xăng dầu, nhà máy có hơi dung môi.

## 2. Định dạng nội dung

- **Bằng chứng:** 8/8 kết quả là trang sản phẩm hoặc danh mục (6 trang sản phẩm, 2 trang danh mục), **0 bài blog, 0 bài toplist**. Google đang hiểu truy vấn là ý định mua hàng.
- **Định dạng phù hợp nhất theo SERP:** trang danh mục "đèn chống cháy nổ 100W". `python tools/danh_muc.py tim "đèn led chống cháy nổ 100w"`: **KHÔNG KHỚP**, website không có danh mục sản phẩm chống cháy nổ nào. CSV `du_lieu_san_pham_HLB_28-10-2026.csv` (113 model) cũng không có model chống cháy nổ nào. Vì vậy không chuyển được sang Agent Danh mục; muốn làm danh mục thì phải tạo danh mục và đăng sản phẩm mới, ngoài phạm vi Agent Blog.
- **Nhận xét về hướng blog Toplist (người dùng đã chọn):**
  - Toplist là dạng blog gần với ý định mua nhất: người đọc vẫn được xem từng mẫu, thông số, giá, chỉ khác là nhiều hãng trên một trang. Một số SERP thương mại ở Việt Nam vẫn chen 1-2 bài "top mẫu" khi các trang bán hàng mỏng nội dung.
  - **Khả năng lên top 3 thấp**, vì SERP hiện 100% trang bán hàng. **Khả năng vào top 10 ở mức trung bình**: SERP chỉ có 8 kết quả, đối thủ chủ yếu là trang sản phẩm ít nội dung, chưa trang nào so sánh nhiều mẫu cùng bộ tiêu chí hay giải thích ký hiệu Ex của từng mẫu.
  - Bằng chứng ngược chiều: website **đã có bài toplist đúng từ khóa này** (ID 3874, mục 4 bên dưới) nhưng bài đó **không có mặt trong 8 kết quả**. Nguyên nhân có thể là nội dung cũ (cập nhật lần cuối 14/12/2023), model không có tên, số liệu không nguồn, chưa chắc do Google chỉ ưu tiên trang bán hàng.
  - **Kết luận định dạng:** viết blog Toplist là khả thi nếu có đủ model thật có nguồn (tối thiểu 5 mẫu) và giá tham khảo. Đổi lại phải chấp nhận rủi ro: thứ hạng chủ yếu đến từ truy vấn dài ("so sánh", "mẫu", "loại nào", "giá") hơn là từ khóa chính, và có thể dừng ở trang 1 vị trí thấp.

## 3. Gộp hay tách

SerpApi không trả truy vấn liên quan. Đề xuất theo SERP và các bài đã có trên website:
- **Gộp vào bài:** "đèn chống cháy nổ 100w", "đèn chống nổ 100w", "đèn highbay chống cháy nổ 100w", "đèn pha led chống cháy nổ 100w", "giá đèn led chống cháy nổ 100w" (top 1, 3, 5, 6, 7 đều là đèn 100W dạng highbay hoặc pha, cùng ý định mua).
- **Tách hoặc không làm:** đèn chống cháy nổ 20W, 40W, 50W, 80W, 150W, 250W (công suất khác, mỗi mức đã có bài riêng trên website, xem mục 4); "đèn pin chống cháy nổ", "đèn sạc chống cháy nổ" (thiết bị cầm tay, lệch chủ đề).

## 4. Kiểm tra trùng chủ đề trên website

Tìm bằng REST API của website (`/wp-json/wp/v2/posts?search=...`, `/wp-json/wc/store/v1/products?search=...`) ngày 28/10/2026.

**Trùng trực tiếp:**

| ID | Bài | URL | Cập nhật | Mức trùng |
|---|---|---|---|---|
| **3874** | TOP 8 đèn LED chống cháy nổ 100w bán chạy nhất- Báo giá 2024 | https://denlednhaxuongcaocap.com/tu-van/den-led-chong-chay-no-100w/ | 14/12/2023 | **Trùng hoàn toàn**: cùng từ khóa, cùng dạng toplist, slug trùng đúng slug dự kiến của bài mới |

**Trùng một phần (có mục 100W):**

| ID | Bài | URL | Phần trùng |
|---|---|---|---|
| 3821 | TOP 5 công suất đèn LED Highbay chống cháy nổ bán chạy | /tu-van/den-led-highbay-chong-chay-no/ | H2 "Đèn LED highbay chống cháy nổ 100W", nêu HLEP4-100W, HLEP2-100W, giá 1.980.000-3.950.000 đồng |
| 4018 | TOP 5 đèn pha chống cháy nổ tốt - Báo giá chi tiết 2026 | /tu-van/den-pha-chong-chay-no/ | Nêu EEW BZD129-100, Duhal DCN2100 (100W), HALEDCO HLEP FL3 |
| 3979 | Bảng báo giá đèn LED chống cháy nổ các thương hiệu lớn | /tu-van/bang-bao-gia-den-led-chong-chay-no/ | Dòng giá đèn chống cháy nổ 100W HALEDCO 5.800.000-6.000.000 đồng (khác hẳn bài 3821 và 3874) |
| 3865 | TOP 7 đèn chống cháy nổ Philips bán chạy nhất 2024 | /tu-van/den-chong-chay-no-philips/ | H2 "Đèn led chống cháy nổ Philips 100w", không có mã model, thông số giống hệt mẫu HALEDCO ở bài 3874 |

**Đề xuất:** không viết bài mới song song. **Viết lại bài 3874 theo dạng Toplist** (đăng `--update 3874`, giữ URL đã có tuổi và liên kết), đặt `id_bai_cu = 3874` trên bảng. Viết bài mới cùng slug thì WordPress tự đổi thành `den-led-chong-chay-no-100w-2` và hai bài ăn thịt từ khóa của nhau. Tên file `Bai_den-led-chong-chay-no-100w.md` vẫn dùng được, vì slug bài đã có trùng đúng tên này.

### Bảng Giữ/Bỏ ý của bài 3874 (đọc toàn bài qua REST API ngày 28/10/2026)

| Nhóm | Ý trong bài 3874 | Lý do |
|---|---|---|
| **Giữ** | Khung toplist: mỗi mẫu có thông số, giá, ưu nhược | Đúng dạng người dùng chọn, viết lại theo cùng cấu trúc ở Knowledge 8.5 |
| **Giữ** | Phân loại 100W theo dạng: highbay hoặc UFO, đèn pha, bóng bulb E40, đèn đường | Dùng làm cách nhóm danh sách (highbay trước, pha sau). Đèn đường chống nổ chỉ nhắc một dòng (ngoài phạm vi nhà xưởng) |
| **Giữ** | Ứng dụng: kho hóa chất, xưởng có chất dễ cháy, trạm xăng, khu ngoài trời có khí dễ cháy | Viết lại theo từng mẫu, bỏ giàn khoan, tàu dầu, quân sự (ngoài phạm vi nhà xưởng) |
| **Bỏ vì sai hoặc lỗi thời** | 7/8 mẫu không có tên hãng, mã model ("Đèn LED chống cháy nổ 100w LED SMD", "chip LED COB", "Highbay"...), thông số không nguồn | Vi phạm quy tắc dữ liệu: không có model thì không kiểm được thông số |
| **Bỏ vì sai hoặc lỗi thời** | Giá các mẫu (1.285.000-9.567.000 đồng) và bảng báo giá mục 9 | Không có nguồn, không ngày, mâu thuẫn với bài 3821 và 3979 cho cùng đèn HALEDCO 100W |
| **Bỏ vì sai hoặc lỗi thời** | "tiết kiệm điện năng cao hơn 70%", "tiêu chuẩn chống cháy nổ tuyệt đối", "an toàn tối đa", "tiết kiệm điện năng tối ưu", "tốt nhất", "bán chạy nhất" | Câu ở Knowledge mục 5, từ tuyệt đối |
| **Bỏ vì sai hoặc lỗi thời** | Mục 11 "Nơi bán ... HALEDCO", "liên hệ website của HALEDCO" | Dẫn khách sang HALEDCO, trái quy tắc không nhắc, không link haledco.com; "tuổi thọ 50000 giờ tương đương 10-15 năm" không có điều kiện |
| **Bỏ vì sai hoặc lỗi thời** | Đèn tiêu chuẩn "Exd II BT4", "Exd IIC T6", "IECEx" ghi như tiêu chuẩn, không rõ mẫu nào | Ký hiệu Ex chỉ ghi khi có nguồn của đúng model |
| **Bỏ vì ngoài phạm vi** | Đèn đường LED chống cháy nổ 100W (mục 7), chiếu sáng giàn khoan, tàu chở dầu, công nghiệp quân sự | Ngoài phạm vi chiếu sáng nhà xưởng, nhà kho, nhà máy |

### Nguy cơ ăn thịt từ khóa giữa các bài 20W, 40W, 50W, 100W

Website đã có **một loạt bài toplist theo công suất từ 2023**, không chỉ các bài ghi trên bảng:

| Từ khóa trên bảng | Bài đã có đúng từ khóa (REST API 28/10/2026) | Ghi chú cho trưởng phòng |
|---|---|---|
| đèn chống cháy nổ 20w | **4069** "TOP 9 đèn chống cháy nổ 20w bán chạy nhất - Báo giá 2023", /tu-van/den-chong-chay-no-20w/ | Bảng ghi "danh mục chưa có", nhưng bài blog đúng từ khóa đã có |
| đèn chống cháy nổ 40w | **4077** "Top 3 đèn chống cháy nổ 40w tốt nhất - Báo giá 2023", /tu-van/den-chong-chay-no-40w/ | Outline 40W hiện chỉ ghi bài 7308 (tuýp), **chưa thấy bài 4077 trùng đúng slug** |
| đèn led chống cháy nổ 50w | **4082** "TOP 5 đèn led chống cháy nổ 50w tốt nhất - Báo giá 2023", /tu-van/den-led-chong-chay-no-50w/ | Outline 50W hiện ghi trùng một phần bài 3821, **chưa thấy bài 4082 trùng đúng slug** |
| đèn led chống cháy nổ 100w | **3874** (trên) | |
| (chưa có trên bảng) | 3935 (80W), 4098 (250W) | Cùng loạt |

Nhận xét:
- Bốn từ khóa khác nhau ở con số công suất, Google tách SERP theo công suất (top 100W toàn sản phẩm 100W), nên **các bài theo từng mức không ăn thịt nhau nếu mỗi bài chỉ nói mẫu đúng công suất của mình**.
- Rủi ro thật nằm ở hai chỗ: (1) viết bài mới cùng slug với bài cũ 4069, 4077, 4082, 3874, làm hai bài cùng nhắm một từ khóa; (2) bài 3821 (highbay chống cháy nổ theo công suất) và bài 3979 (bảng giá) có mục 100W với giá khác nhau, Google và người đọc thấy số liệu mâu thuẫn.
- Đề xuất: mỗi mức công suất là **một bài, viết lại trên URL cũ**; bài 3821 giữ vai trò bài tổng (trỏ link sang từng bài công suất, rút gọn mục 100W); các bài 40W, 50W, 100W dùng chung khung "đọc ký hiệu Ex" nhưng chỉ giải thích ngắn và trỏ về bài tiêu chuẩn 6121, tránh ba bài lặp cùng đoạn dài.
- Ý đã có trong outline 40W và 50W (dạng đèn, khu phù hợp, đọc nhãn Ex, lỗi khi lắp): bài 100W không lặp lại thành H2 riêng. Bài 100W khác ở chỗ là danh sách mẫu có tên, bảng so sánh cùng tiêu chí, và so sánh 100W với 2 bộ 50W hoặc 150W ở trần 6-10 m.

## 5. Kiểm tra phạm vi

Thuộc phạm vi: đèn chống cháy nổ là chủ đề phụ đã có bài (Knowledge mục 4), dùng cho nhà xưởng, kho hóa chất, nhà máy sơn, kho xăng dầu. Phần đèn đường chống nổ, giàn khoan, tàu dầu ngoài phạm vi, không đưa vào bài.

## Dữ liệu model: tình trạng xác minh

- CSV 28/10/2026 (113 model): **không có** model chống cháy nổ. Website: **không có** trang sản phẩm chống cháy nổ (Store API, tìm "chống cháy nổ", "chống nổ", "chong chay no": 0 kết quả).
- Website chính thức của hãng (rangdong.com.vn, signify.com, dienquang.com, paragon, duhal, zalaa, haledco.com): **proxy của phiên chặn toàn bộ**, không mở được. Công cụ tìm kiếm có sẵn chỉ cho kết quả Mỹ, không thấy model chống nổ 100W nào của Rạng Đông, Điện Quang, Philips (Việt Nam), Paragon.
- **Tên model có thật xuất hiện trong SERP hoặc bài cũ trên website** (chưa xác minh thông số trong phiên này):

| Model | Hãng | Dạng | Thấy ở | Dữ liệu đã thấy (chưa xác minh) |
|---|---|---|---|---|
| HLEP2-100W | HALEDCO | highbay | SERP #5, bài 3821 | đoạn trích: chip SMD Cree, Osram, Philips, Samsung; 130 lm/W |
| HLEP4-100W | HALEDCO | highbay | bài 3821 | không có thông số riêng |
| HLEP FL3 (dải 30-500W) | HALEDCO | đèn pha | bài 4018 | 130 lm/W, IP66, IECEx (cả dải, không riêng 100W) |
| BZD129-100 | EEW | đèn pha | bài 4018 | Ex nA e mc IIC T6 Gc / Ex tD A21 IP66 T80°C, PF ≥0,95, Ra ≥75, 14.399.000 đồng |
| DCN2100 | Duhal | đèn pha | bài 4018 | 11.000 lm, IP65, Ra 83, 150-250 V; bài không ghi ký hiệu Ex |
| FCN1001 | Duhal | đèn pha | SERP #7 | không có thông số |
| ZHB-CCN-100 | ZALAA | highbay SMD | SERP #3 | đoạn trích: lớp bảo vệ Class 2, chống ăn mòn WF2 |
| ZHB150COB-CCN (bản 100W) | ZALAA | UFO COB | SERP #6 | 100W, 100-240 V AC |

Kết luận dữ liệu: **có đủ tên model thật để lập danh sách 5-7 mẫu**, nhưng **chưa model nào có thông số xác minh được từ nguồn hợp lệ trong phiên này**. Outline vẫn lập được; khi viết, mọi ô thông số chưa có nguồn sẽ là `[CẦN BỔ SUNG]` cho tới khi người dùng cung cấp catalogue hoặc mở được trang hãng. Mục "Philips 100w" ở bài 3865 không có mã model và trùng số liệu với mẫu HALEDCO ở bài 3874, không dùng.
