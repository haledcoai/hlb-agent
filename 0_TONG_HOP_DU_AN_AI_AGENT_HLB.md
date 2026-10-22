# TỔNG HỢP DỰ ÁN AI AGENT VIẾT BÀI CHO DENLEDNHAXUONGCAOCAP.COM

Cập nhật: 22/10/2026. File này tóm tắt các quyết định, trạng thái và việc còn dở, để tiếp tục ở phiên làm việc khác mà không cần đọc lại toàn bộ cuộc trò chuyện.

## 1. Mục tiêu

Agent nhận bộ từ khóa, nghiên cứu SERP, lập outline gửi duyệt, viết bài, rồi đưa bản nháp lên website denlednhaxuongcaocap.com (WordPress) để người dùng duyệt và tự đăng.

## 2. Các file trong dự án

| File | Vai trò |
|---|---|
| 1_Project_Instructions_Auto_Blog_HLB.md | Quy trình 4 bước, giọng văn, quy tắc dữ liệu, cách viết về thương hiệu, quy tắc đăng bản nháp. Dán vào ô Instructions của Claude Project |
| 2_Knowledge_Du_lieu_tham_chieu_HLB.md | Thông tin HLB đã xác nhận, URL danh mục và bài Tư vấn, cách đọc trang sản phẩm, chuẩn SEO, checklist. Tải lên Project Knowledge |
| 4_Agent_danh_gia_noi_dung_HLB.md | Tóm tắt agent đánh giá chất lượng: vai trò, kiểm tra cơ học (làm tay được khi không có script), thang 100 điểm cần từ 95, mẫu báo cáo, vòng duyệt, phiếu và nhật ký, bài học, việc còn mở. Dùng được cả trong Claude Project trên claude.ai |
| 3_Bang_hoi_thong_tin_co_dinh_HLB.md | Bảng hỏi thông tin cố định (8 nhóm). Đã trả lời nhóm 1 và phần lớn nhóm 2 |
| du_lieu_san_pham_HLB_21-10-2026.csv | Thông số và giá 113 sản phẩm đọc từ website ngày 21/10/2026 |
| Bai_cach-chon-den-led-nha-xuong.md | Bài viết lại "cách chọn đèn LED nhà xưởng" (phần A, B, C) |
| tools/wp_draft.py | Script đưa bản nháp lên WordPress qua REST API |
| tools/HUONG_DAN_DANG_NHAP.md | Hướng dẫn tạo Application Password, cách đánh dấu bản nháp |
| tools/kiem_tra_bai.py | Kiểm tra lỗi cơ học của bài (dấu gạch, từ cấm, link, độ dài SEO, định dạng số, thông số so với CSV). Thoát mã 1 khi còn LỖI |
| .claude/agents/danh-gia-noi-dung.md | Sub agent đánh giá chất lượng bài: chạy script trên, đối chiếu dữ liệu, chấm 100 điểm (ĐẠT từ 95), ghi phiếu duyệt, trả báo cáo. Không sửa bài |
| CLAUDE.md | Vòng duyệt tự động: viết hoặc sửa bài xong thì gọi agent đánh giá, chưa đạt 95 thì agent chính tự sửa và chấm lại, tối đa 3 vòng |
| tools/phieu_duyet.py | Ghi và kiểm tra phiếu duyệt (`.danh_gia/<bài>.json`, kèm mã kiểm tra nội dung). Kiêm các hook: chặn `wp_draft.py --post` khi chưa có phiếu ĐẠT; ghi nhận bài vừa sửa; không cho kết thúc lượt khi bài vừa sửa chưa được chấm lại |
| .claude/agents/tao-anh.md | Sub agent chuẩn bị ảnh: ảnh sản phẩm lấy ảnh thật trên website, sơ đồ và bảng vẽ bằng Python, ảnh minh họa không gian tạo bằng Canva. Không sửa bài, không tải lên website |
| tools/tao_anh.py | Liệt kê chỗ [ẢNH], gợi ý nguồn ảnh (`phan-loai`, đối chiếu CSV), lấy ảnh sản phẩm thật, chuẩn hóa JPG 820 px (rộng 800-850, cao 400-800), ghi trạng thái duyệt, ghi danh sách `anh/<bài>/anh.json` (ảnh Canva lưu cả prompt), kiểm tra đủ ảnh, tên ảnh không trùng slug, alt (cần Pillow, matplotlib) |
| tools/mau_anh.py | Thư viện 6 mẫu sơ đồ dùng chung: lưới bố trí, bảng IP, bảng so sánh, biểu đồ cột, mặt cắt chiều cao treo và góc chiếu, các bước. Tự kiểm tra chữ trên hình (đè, tràn, dưới 13 px, em dash) trước khi lưu |
| anh/_prompt_canva.md | 6 prompt Canva mẫu cho cảnh nhà xưởng, cách sửa prompt khi ảnh bị trả về |
| anh/<bài>/ | Ảnh của từng bài, `anh.json` và script vẽ sơ đồ `ve_so_do.py` (gọi mẫu trong `tools/mau_anh.py`). `wp_draft.py` đọc `anh.json`: xem trước dùng ảnh trong máy, `--post` tải ảnh lên Media, chèn vào bài và đặt ảnh đại diện |
| anh/trang-duyet-anh.html | Trang Duyệt ảnh HLB cũ (từ 22/10/2026 chuyển sang tab Duyệt ảnh của Bảng điều phối HLB https://claude.ai/artifact/3wRDGsubs7s2Kb75vpypmG): người dùng bấm Duyệt hoặc Làm lại từng ảnh, ghi ảnh còn thiếu. Agent đọc qua ArtifactData, chỉ ảnh đã duyệt được đăng. Quy trình ở CLAUDE.md |
| .danh_gia/nhat_ky.jsonl | Nhật ký chấm, chỉ thêm không ghi đè: mỗi lần chấm (điểm 6 tiêu chí, vấn đề có nhãn, phiên bản thang chấm) và mỗi lần agent đánh giá bị bác bỏ. Đã nhập lại 3 lần chấm bài "cách chọn đèn" ngày 21/10/2026 (thang v1) |
| Lịch sử chấm bài | Tab Lịch sử chấm của Bảng điều phối HLB https://claude.ai/artifact/3wRDGsubs7s2Kb75vpypmG (trang cũ JVfjfAmGtDAtZr49TFodBc ngừng cập nhật từ 22/10/2026): điểm qua các lần chấm, điểm mất theo tiêu chí, vấn đề lặp lại, lần agent bị bác bỏ, bảng lịch sử. Dữ liệu từ `phieu_duyet.py xuat`, cập nhật cuối mỗi vòng duyệt (CLAUDE.md) |
| .claude/settings.json | Khai báo 3 hook: PreToolUse (chặn đăng), PostToolUse (ghi nhận sửa bài), Stop (nhắc chấm lại) |

## 3. Quyết định đã chốt

**Thương hiệu và vai trò**
- Website vệ tinh xưng "Đèn LED Nhà Xưởng HLB" (gọi tắt HLB), thuộc Công ty TNHH Công nghệ và Xúc tiến Thương mại HALEDCO.
- Dòng đèn cao cấp: HALEDCO sản xuất và lắp ráp, HLB phân phối. Không viết "HLB sản xuất".
- Mốc thời gian: HALEDCO sản xuất từ 2011, HLB phân phối từ 2018. Không cộng gộp số năm.

**Liên hệ**
- Hotline bán hàng, ưu tiên trong bài và CTA: 0967569588 (có Zalo).
- Hotline kỹ thuật và bảo hành: 02437 918 122.
- Email: denlednhaxuongcaocap@gmail.com.

**Quy tắc nội dung**
- Không link về haledco.com.
- Được so sánh công bằng Philips, Rạng Đông, Điện Quang và dòng cao cấp (cùng tiêu chí, có nguồn), không nói xấu, không kết luận hãng nào tốt nhất.
- Duyệt 2 lần: sau Bước 1 (SERP) và sau Bước 2 (outline). Bước 3 viết trọn bài một lần.
- Không em dash, en dash, emoji, từ tuyệt đối.

**Chính sách**
- Dòng cao cấp bảo hành 2 năm (driver, chip LED). Hãng khác theo chính sách hãng: Rạng Đông 24 tháng, Điện Quang 24 tháng, Philips theo từng model trên signify.com.
- Đổi trả theo nhu cầu: khách chịu phí 10% giá trị hàng.
- Miễn phí giao hàng khi đơn trên 5 triệu đồng, trong bán kính 10 km.
- Chiết khấu: được nhắc là có, không nêu mức.

**Đăng bản nháp**
- Bài viết lại bài cũ: tiêu đề `[CẬP NHẬT #ID] ...`, slug `ban-nhap-cap-nhat-ID`, không đụng bài gốc. Người dùng chép nội dung sang bài gốc để giữ URL.
- Chủ đề mới: tiêu đề `[MỚI] ...`.
- Đầu mỗi bản nháp có khối "GHI CHÚ BIÊN TẬP", xóa trước khi đăng.
- Thông tin đăng nhập ở biến môi trường WP_USER (hiện là `quoc-viet`, vai trò Biên tập viên) và WP_APP_PASSWORD trên máy người dùng. Không lưu mật khẩu trong file.

## 4. Trạng thái công việc

| Việc | Trạng thái |
|---|---|
| Bài "cách chọn đèn LED nhà xưởng" (viết lại bài ID 2323) | Đã đẩy lên bản nháp ID 8514 ngày 21/10/2026 (14:38), phiếu ĐẠT 95, kèm 3 ảnh đã duyệt (Media 8518, 8519, 8520; ảnh đại diện 8520). Chờ người dùng duyệt trong wp-admin và chép sang bài gốc 2323 |
| Bảng hỏi thông tin cố định | Xong nhóm 1. Nhóm 2 còn 4 điểm chờ xác nhận. Nhóm 3 đến 8 chưa trả lời |

## 5. Việc còn dở

**Chờ người dùng xác nhận (nhóm 2)**
1. 15 ngày đầu: sản phẩm lỗi, còn mới, còn tem thì được đổi mới 1 đổi 1?
2. Thời hạn đổi trả theo nhu cầu bao nhiêu ngày?
3. Đổi trả do lỗi sản phẩm có mất phí 10% không? Ai chịu phí vận chuyển khi bảo hành?
4. Bán kính 10 km tính từ văn phòng Xuân Đỉnh hay trụ sở Sơn Tây?

**Chưa trả lời:** nhóm 3 (dịch vụ) đến nhóm 8 (người duyệt, ảnh) trong file 3.

**Placeholder còn trong bài 8514** (5 chỗ, kiểm tra 22/10/2026)
- `[CẦN KIỂM TRA]` Đối chiếu bảng độ rọi với TCVN 7114-1:2008, kèm `[LINK]` trang tra cứu (Agent tự làm).
- `[CẦN KIỂM TRA]` Website có bán đèn dạng dài không.
- `[CẦN BỔ SUNG]` Phần xưởng bụi: dòng cao cấp chưa có model từ IP65; có gợi ý đèn IP65/IP66 của hãng khác đang bán (Philips BY239P, BPLCE-200, BPLCE-250, Rạng Đông BD HB03L 390/250W) hay để trung lập.
- `[CẦN BỔ SUNG]` Dải nhiệt độ làm việc của dòng BUFO (trang BUFO4-150 không ghi).
- Đã giải: tùy chọn hãng chip, driver của BUFO4-150 (trang sản phẩm mục 1.1, 1.2 có ghi).

**Câu hỏi chờ người dùng từ lần chấm ĐẠT (21/10/2026):** đổi một H2 để chứa nguyên cụm từ khóa chính; hệ số MF 0,8 trong ví dụ hay thấp hơn; phần xưởng bụi như trên.

**Phần C của bài còn ghi chưa đúng thực tế** (chỉ là ghi chú cho người duyệt, xóa khi đăng): mục 4 "Ảnh cần chuẩn bị" vẫn ghi cần người dùng cung cấp ảnh, trong khi 3 ảnh đã làm xong. Sửa khi sửa bài lần tới (sửa bài phải chấm lại).

**Sau khi có đủ trả lời:** cập nhật Knowledge, sửa bài, gọi agent `danh-gia-noi-dung` chấm lại (cần ĐẠT), rồi đẩy lên bản nháp 8514 bằng lệnh:

```bash
python tools/wp_draft.py Bai_cach-chon-den-led-nha-xuong.md --update 2323 --post --draft-id 8514
```

**Ảnh bài 8514 (đã tải lên website 21/10/2026, Media 8518-8520, có alt, tiêu đề, mô tả):**
- Chuẩn ảnh (chốt 21/10/2026): JPG, rộng 800-850 px, cao 400-800 px, tên file như gợi ý trong bài, nội dung khớp đoạn văn. Agent `tao-anh` tự chạy sau khi bài ĐẠT.
- 2 sơ đồ vẽ bằng Python (cấp bảo vệ IP 820 x 510, lưới 5 x 8 đèn 820 x 620): xong, JPG.
- Ảnh toàn cảnh nhà xưởng (ảnh đại diện): tạo bằng Canva (media `MAHYng0gjEU`), xuất bản đầy đủ 1680 x 944 qua thiết kế Canva `DAHYnysKTTQ` trang 2, chuẩn hóa còn 820 x 461. Là ảnh minh họa AI, không phải công trình thật.
- Ảnh thiếu: agent tự tạo (kể cả ảnh minh họa thay ảnh công trình, có ghi chú). Vẫn thiếu thì `wp_draft.py` đăng với ảnh có sẵn, liệt kê ảnh thiếu trong ghi chú biên tập.
- Khâu tải ảnh lên Media (`--post`) đã chạy thật lần đầu ngày 21/10/2026, kiểm tra lại: 3 thẻ ảnh đúng URL, alt, kích thước; ảnh tải được (200, image/jpeg).
- Lưu ý khi chép sang bài gốc 2323: ảnh đại diện đang gắn ở bản nháp 8514, cần đặt lại ảnh đại diện (Media 8520) cho bài 2323.

**Việc người dùng tự làm (rà soát 22/10/2026)**
- Duyệt bản nháp 8514 trong wp-admin, xử lý các placeholder in đậm, chép sang bài gốc 2323 (bài 2323 đang công khai với tiêu đề cũ "8 Kinh nghiệm chọn đèn LED cho nhà xưởng tốt, giá rẻ"), đặt ảnh đại diện Media 8520, rồi chuyển bản nháp 8514 vào thùng rác.
- Nếu còn dùng Claude Project trên claude.ai: tải lại file 1 và file 2 bản mới (đã đổi chuẩn ảnh, thẻ ảnh có chú thích, ngưỡng 95), và file 4 nếu muốn chấm bài ở đó.
- Canva: thiết kế `DAHYnysKTTQ` ("HLB anh bai - cach-chon-den-led-nha-xuong") có trang 1 là mẫu quảng cáo Canva tự sinh, không dùng, có thể xóa trang đó.
- Việc còn mở của agent đánh giá: xem file 4 mục 11 (lệnh ghi phiếu từng bị chế độ tự động chặn, hook nhắc khi đang chấm nền, tiêu chí nên bổ sung).

## 6. Phát hiện trên website cần người dùng xử lý

- 47 model dòng cao cấp (B1, B2, B3, B5, B11 và phần lớn B4) có bảng thông số trống.
- BUFO1-200, BUFO3-200 ghi IP40, các model BUFO khác ghi IP54.
- 4 model 150W của hãng khác cùng ghi 16.500 lm, PF 0,9, Ra 80, có thể dùng chung mẫu bảng.
- Tất cả sản phẩm Philips ghi "Bảo hành 24 tháng", trong khi Philips bảo hành theo từng model.
- Trang chính sách bảo hành ghi "đổi trả trong vòng tuần", thiếu số ngày.
- Danh mục Điện Quang 150W trống.
- Mục Tư vấn có 249 bài, file Knowledge mới liệt kê một phần.

## 7. Bài học kỹ thuật

- Giá sản phẩm lấy từ khối đầu trang của chính sản phẩm hoặc API `wc/store/v1/products?slug=...`. Không lấy từ khối "Sản phẩm liên quan" (đã từng đọc nhầm giá).
- Bảng thông số sản phẩm nằm trong thẻ `<table>` của trang, lớp CSS `table-bordered` được thêm bằng JavaScript nên không có trong HTML gốc.
- Lệnh `site:` trên Google không trả kết quả đúng cho website này, dùng ô tìm kiếm của website (`/?s=từ khóa&post_type=post`) để kiểm tra trùng chủ đề.
