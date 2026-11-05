# AGENT DANH MỤC: VIẾT NỘI DUNG DANH MỤC SẢN PHẨM CHO DENLEDNHAXUONGCAOCAP.COM

Phiên bản: 28/10/2026 (27/10 người dùng yêu cầu tách Agent Blog và Agent Danh mục; 28/10 thêm quy tắc trình bày dùng chung). Plan đã chốt: https://claude.ai/artifact/EPoxW1TE4xB6oQWyhdvSNj

Agent Danh mục viết lại nội dung cho **danh mục sản phẩm đã có** trên website (trang `/den-led-nha-xuong-150w/`, `/den-led-nha-xuong-150w/philips-150w/`...). Không tạo danh mục mới, không sửa sản phẩm, chưa làm trang sản phẩm. Công cụ `tools/danh_muc.py`, file `DM_<slug danh mục>.md`, chấm bởi agent riêng `danh-gia-danh-muc` (thang `quy_tac_cham_danh_muc.md`). Điều phối tự nhận diện từ khóa danh mục (`DIEU_PHOI.md` mục 3c).

Dùng chung với Agent Blog, giữ nguyên: bốn quy tắc cốt lõi, giọng văn, thương hiệu, bảo hành, cấm (em dash, emoji, từ tuyệt đối, văn mẫu AI), cách viết số, so sánh thương hiệu ở `1_Project_Instructions_Auto_Blog_HLB.md` mục 2, 5, 6, 7 và `2_Knowledge_Du_lieu_tham_chieu_HLB.md`. File này chỉ ghi phần khác. Khi hai file khác nhau ở phần riêng của danh mục, theo file này.

**Quy tắc trình bày dùng chung** (người dùng chốt 28/10/2026, Instructions mục 4): sapo có từ khóa chính ở câu đầu; câu khoảng 20 từ; đoạn 2,5-3 dòng, không quá 4 dòng; quan hệ từ nối mạch; gạch đầu dòng, in đậm ý chính, bảng; câu kết mỗi H2 dẫn sang H2 sau; ảnh theo từng phần; kết bài tóm tắt, đánh giá, có từ khóa chính và lời kêu gọi hành động; meta description 150-155 ký tự, từ khóa ở đầu. Áp vào danh mục như sau: đoạn đầu khối trên là sapo; quy tắc H2, ảnh, kết bài áp cho khối dưới.

## 1. Khác bài blog ở đâu

| | Bài blog (Agent Blog) | Nội dung danh mục (Agent Danh mục) |
|---|---|---|
| Người đọc | Đang tìm hiểu, so sánh | Đã ở bước chọn mua, muốn xem sản phẩm |
| Vị trí | Bài riêng ở mục Tư vấn | Hai khối quanh lưới sản phẩm của danh mục |
| Độ dài | Đủ trả lời intent | Khối trên 80-150 từ, khối dưới ngắn hơn bài blog, không lan man |
| Thông số | CSV và trang sản phẩm | Chỉ sản phẩm đang bán trong chính danh mục |
| Đưa lên web | Bản nháp bài viết | Trang nháp để xem trước; duyệt xong mới ghi vào danh mục (công khai ngay) |
| File | `Bai_<slug>.md` | `DM_<slug danh mục>.md` |

## 2. Quy trình

### Bước 0: Chọn đúng danh mục (người dùng chốt 27/10/2026)

- **Danh mục cha hay danh mục con theo hãng:** Agent tự phân tích, không hỏi lại. Người dùng đưa link danh mục thì làm đúng danh mục đó. Không có link thì theo từ khóa chính: có tên hãng (Philips, Rạng Đông, Điện Quang, HALEDCO...) thì danh mục con của hãng đó; không có tên hãng thì danh mục cha cùng công suất, loại đèn. SERP cho thấy intent khác (ví dụ người tìm từ khóa chung nhưng top toàn trang một hãng) thì vẫn làm theo quy tắc trên, ghi nhận xét vào `serp`.
- Danh mục con theo hãng (ví dụ Philips 150W) thuộc phạm vi Agent Danh mục, có viết như danh mục cha (người dùng chốt 27/10/2026). Mỗi lần viết theo một từ khóa hoặc link được nạp. Thấy danh mục khác (cha hoặc con) nội dung đang trống hoặc yếu thì ghi ở phần C từ khóa nên nạp tiếp, để người dùng đưa lên bảng.
- **Website chưa có danh mục** (`danh_muc.py tim` không KHỚP, không có danh mục GẦN đúng loại đèn; người dùng chốt 05/11/2026): không dừng chờ người dùng tạo danh mục. Agent tự đề xuất theo SEO tên danh mục, slug (không dấu, 2-5 từ, có từ khóa chính), danh mục cha, chạy `python tools/danh_muc.py de-xuat <slug> --ten "<tên>" [--cha <slug cha>] [--tim "<cụm tìm sản phẩm>"]` (ghi `nghien_cuu/DM_<slug>/` với `de_xuat: true`, sản phẩm đang bán có tên khớp), rồi làm tiếp Bước 1-4 như danh mục có sẵn. Phần A ghi `Danh mục: <tên> (đề xuất, chưa có trên website)`, `Term ID: 0`, `Link danh mục: <link dự kiến>`. Bài ĐẠT thì vẫn đưa lên Trang nháp (`danh_muc.py nhap --post`), trang ghi rõ danh mục chưa tạo, chỗ lưới sản phẩm để trống. Chỉ nêu model có trong `san_pham.json` (thường là 0, khi đó viết theo cách chọn đèn, không nêu model, sản phẩm để `[CẦN BỔ SUNG]`). Ghi lên danh mục (`ap-dung`) chỉ khi người dùng đã tạo danh mục đúng slug: script tự dừng nếu chưa có; khi đã có, chạy lại `danh_muc.py doc <slug>`, giao `agent-danh-muc` chế độ `sua` nếu sản phẩm thay đổi, chấm lại rồi mới áp dụng. Không tự tạo danh mục, không chuyển sang viết blog khi người dùng không yêu cầu.

### Bước 1: Đọc danh mục và SERP (gộp duyệt với Bước 2 trên Bảng điều phối)

1. `python tools/danh_muc.py doc <slug hoặc link danh mục>`: lưu vào `nghien_cuu/DM_<slug>/`:
   - `danh_muc.json`: ID, link, danh mục cha/con, khối trên, khối dưới, SEO title, meta description hiện tại.
   - `san_pham.json`, `san_pham.md`: các sản phẩm đang bán trong danh mục, giá, thông số theo trang sản phẩm (qua file CSV mới nhất). Sản phẩm chưa có trong CSV: chạy `python tools/lam_moi_csv.py` rồi đọc lại.
   - `noi_dung_cu.md`: chữ của nội dung cũ để chia ý.
2. **Chia ý nội dung cũ** thành Giữ / Bỏ vì sai hoặc lỗi thời (thông số, giá, câu ở Knowledge mục 5) / Bỏ vì không hợp trang danh mục (phần nên nằm ở bài blog). Danh sách ý bỏ và lý do ghi vào phần C.
3. **SERP** cho từ khóa chính: đọc 5-10 kết quả đầu như Instructions Bước 1, chú ý các trang danh mục đang lên top: khối trên dài bao nhiêu, có bảng so sánh model, bảng giá, FAQ không. Lưu văn bản các trang top bằng `python tools/nghien_cuu.py luu-serp DM_<slug>.md <url> ...` (không mở được thì WebFetch rồi `--tu-file`).
4. **Kiểm tra trùng:** tìm bài blog trên website nhắm cùng từ khóa (ô tìm kiếm của website, Knowledge 2.4). Có bài blog cùng intent thì ghi URL, đề xuất phân vai: danh mục giữ từ khóa mua hàng, bài blog giữ từ khóa tìm hiểu, hai bên link qua lại.

Báo 5 mục như Instructions Bước 1 (intent, định dạng, gộp/tách, trùng, phạm vi), kèm bảng Giữ/Bỏ.

### Bước 2: Outline

Đúng 7 mục:
1. **Từ khóa:** từ khóa chính (không tự đổi, `1_Project_Instructions_Auto_Blog_HLB.md` mục 3, Nhóm từ khóa), từ khóa phụ giữ/tách/bỏ, tối đa 4 cụm giữ.
2. **Phân tích trang top:** ý bắt buộc, 1-2 góc khác biệt (ví dụ bảng chọn nhanh model theo chiều cao trần, so sánh các hãng trong danh mục theo cùng tiêu chí).
3. **Khối trên:** 1 dòng nội dung chính cần nói. Kèm đề xuất SEO title 55-65 ký tự (đếm bằng công cụ, ghi số ký tự).
4. **Khối dưới:** các H2, H3 (không có H1, theme tự hiện tên danh mục làm H1), dưới mỗi heading 1 dòng nội dung. Cách trình bày do Agent quyết theo search intent và các trang danh mục đang lên top, như một người làm SEO 10 năm: người tìm muốn chọn mua thì ưu tiên bảng chọn model, giá, cách đặt hàng; muốn so sánh hãng thì ưu tiên bảng so sánh cùng tiêu chí. Không đưa phần không phục vụ intent chỉ để đủ khung. Gợi ý khung, không bắt buộc đủ:
   - Chọn công suất, model theo chiều cao trần và diện tích
   - So sánh các dòng đèn đang có trong danh mục (bảng tối đa 5 cột)
   - Giá tham khảo và cách nhận báo giá theo số lượng
   - Lưu ý lắp đặt, môi trường (bụi, nóng, ẩm)
   - Bảo hành, giao hàng, mua hàng
   - Câu hỏi thường gặp (3-5 câu, không lặp phần trên)
5. **Dữ liệu cần dùng:** model, số liệu nào lấy từ `san_pham.md`.
6. **Câu hỏi cho người dùng:** đánh số, không có thì ghi "Không có".
7. **Link nội bộ:** 2-6 link: bài blog liên quan (Knowledge 2.4), danh mục cha/con hoặc công suất gần. Không link về chính danh mục này.

### Bước 3: Viết

- Lưu outline đã duyệt: `python tools/nghien_cuu.py luu-outline DM_<slug>.md --tu <file>` (heading khối dưới phải đúng outline).
- Viết file `DM_<slug>.md` theo mục 3. Chỉ dùng số liệu trong `san_pham.md`, Knowledge mục 1 và người dùng trả lời. Chỗ thiếu để `[CẦN BỔ SUNG: ...]`.
- **Khối trên:** 80-150 từ, 1-2 đoạn, không heading. Đoạn đầu là sapo: **từ khóa chính ở câu đầu tiên**, 2,5-3 dòng, nêu khái quát danh mục. Nói danh mục có những dòng đèn nào (theo hãng, kiểu đèn), hợp với xưởng nào, một câu mời gọi báo giá có hotline 0967569588. Không kể lịch sử công ty, không giới thiệu chung về đèn LED.
- **Khối dưới:** mở bằng 1-2 câu dẫn, rồi các H2 theo outline. Phương án hợp trường hợp phổ biến nói trước. Bảng so sánh dùng đúng sản phẩm đang bán trong danh mục, ô không có dữ liệu ghi "không công bố". Giá ghi "giá tham khảo tại thời điểm [ngày]" (hãng khác theo Instructions mục 6).
- Phần giải thích dài (cách tính số đèn, tiêu chuẩn độ rọi) tóm 1-2 câu rồi link sang bài blog, không chép lại bài blog.
- Mỗi H2 khối dưới (trừ FAQ, kết) có câu kết chốt ý, dẫn sang H2 sau (Instructions mục 4).
- **Kết khối dưới** (H2 cuối, sau FAQ): tóm tắt, đánh giá các lựa chọn trong danh mục theo trường hợp, có từ khóa chính, rồi CTA: hotline, Zalo 0967569588, email, link trang Liên hệ.
- **Ảnh** (28/10/2026, thay quy tắc "thường không cần ảnh"): khối dưới theo Instructions mục 4, H2 không có H3 có 1 ảnh, mỗi H3 ưu tiên 1 ảnh, trừ FAQ và kết. Ảnh hợp danh mục: ảnh sản phẩm đang bán trong danh mục (lấy từ trang sản phẩm), sơ đồ chọn công suất, ảnh lắp đặt minh họa. Đặt `[ẢNH: ... | alt: ... | tên file: ....jpg]`, ảnh làm như bài blog (agent `tao-anh`). Khối trên không đặt ảnh (đẩy lưới sản phẩm xuống).

### Bước 4: Tự kiểm tra và chấm

`python tools/kiem_tra_bai.py DM_<slug>.md` (tự chạy chế độ danh mục) tới khi 0 lỗi, rồi vòng duyệt CLAUDE.md: agent `danh-gia-danh-muc` (Leader Content duyệt riêng nội dung danh mục) chấm theo thang danh mục (`quy_tac_cham_danh_muc.md`), ngưỡng 95, tối đa 3 vòng.

## 3. File `DM_<slug>.md`

```
# A. Thông tin SEO

| Trường | Nội dung |
|---|---|
| Danh mục | den-led-nha-xuong-150w |
| Term ID | 70 |
| Link danh mục | https://denlednhaxuongcaocap.com/den-led-nha-xuong-150w/ |
| Focus keyword | <từ khóa chính> |
| SEO title | <55-65 ký tự, có từ khóa chính> |
| Meta description | <150-155 ký tự, từ khóa chính ở đầu> |

# B. Nội dung danh mục

[KHỐI TRÊN]
<80-150 từ>

[KHỐI DƯỚI]
<1-2 câu dẫn>

## <H2 theo outline>
...

# C. Ghi chú cho người duyệt
- Nội dung cũ: ý giữ, ý bỏ và lý do
- Nguồn số liệu, ngày đọc
- [CẦN BỔ SUNG], [CẦN KIỂM TRA] còn lại
```

Ba dòng Danh mục, Term ID, Link danh mục chép từ `nghien_cuu/DM_<slug>/danh_muc.json`. Không có Slug, Excerpt, Tag, Category như bài blog: slug danh mục giữ nguyên.

## 4. Đưa lên website

Danh mục không có bản nháp, ghi vào là công khai ngay. Vì vậy có hai bước, bước sau chỉ chạy khi người dùng bấm duyệt:

1. **Trang nháp** (sau khi bài ĐẠT, giống đăng nháp bài blog): `python tools/danh_muc.py nhap DM_<slug>.md` (xem trước), rồi `--post`. Script tạo hoặc cập nhật Trang (Page) nháp "[Nháp danh mục] <tên>": ghi chú SEO, khối trên, lưới sản phẩm thật của danh mục (shortcode WooCommerce), khối dưới. Trạng thái nháp nên khách không thấy. Ghi `link_xem`, `link_nhap` lên Bảng điều phối.
2. **Áp dụng vào danh mục** (chỉ khi trên bảng người dùng bấm "Duyệt, cập nhật lên danh mục", trường `duyet_ap_dung_luc`): `python tools/danh_muc.py ap-dung DM_<slug>.md --duyet-luc <duyet_ap_dung_luc>` (chạy thử), rồi thêm `--post`. Script:
   - Kiểm tra phiếu ĐẠT khớp nội dung, ảnh đã duyệt đủ.
   - Sao lưu mô tả, khối trên, SEO title, meta description cũ vào `danh_muc/sao_luu/<slug>_<giờ>.json` (commit file này).
   - Ghi khối dưới vào mô tả danh mục, ghi SEO title, meta description, focus keyword vào Rank Math.
   - **Khối trên** nằm ở trường riêng của theme, REST API chưa mở. Khi `danh_muc/cau_hinh.json` có `khoi_tren_meta` (tên trường theme đã mở cho REST) thì ghi luôn; chưa có thì ghi file `danh_muc/DM_<slug>.khoi_tren.html`, đưa lên bảng để người dùng chép, dán vào ô khối trên trong wp-admin, bấm "Đã dán khối trên".
   - Tải lại trang danh mục kiểm tra, khớp thì chuyển Trang nháp vào Thùng rác.
3. **Kiểm tra lại:** `python tools/danh_muc.py kiem-trang DM_<slug>.md` (sau khi người dùng dán khối trên, hoặc khi trang còn bộ nhớ đệm).
4. **Khôi phục** khi người dùng yêu cầu: `python tools/danh_muc.py khoi-phuc <slug> --post` (ghi lại bản sao lưu mới nhất; script sao lưu bản hiện tại trước khi ghi).

Không bao giờ chạy `ap-dung --post` khi người dùng chưa bấm duyệt trên bảng hoặc chưa đồng ý trong chat. Không tự điền `--duyet-luc`.

## 5. Ranh giới

- Chỉ sửa mô tả danh mục và Rank Math của đúng danh mục trong phần A. Không đổi tên, slug, danh mục cha, ảnh, thứ tự, sản phẩm.
- Tài khoản WordPress cần quyền Quản lý cửa hàng (người dùng đã cấp cho `quoc-viet` ngày 27/10/2026).
- Không link về haledco.com. Không nêu sản phẩm không có trong danh mục.
