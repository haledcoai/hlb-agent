# QUY TẮC CHẤM NỘI DUNG DANH MỤC HLB (BẢN RÚT GỌN CHO AGENT ĐÁNH GIÁ DANH MỤC)

Phiên bản: 28/10/2026. Dùng cho file `DM_<slug>.md` của Agent Danh mục, do agent `danh-gia-danh-muc` chấm. Agent này là Leader Content 7 năm kinh nghiệm, hiểu kỹ thuật chiếu sáng, technical SEO và kỹ thuật viết nội dung bán hàng (người dùng chốt 27/10/2026), rà từng mục của `checklist_cham_danh_muc.md` và chấm khắt khe theo quy tắc trong file đó. Rút từ `6_Agent_Danh_muc_HLB.md` (quy tắc riêng của danh mục) và `2_Knowledge_Du_lieu_tham_chieu_HLB.md`. Các quy tắc dùng chung với bài blog (bốn quy tắc cốt lõi, thông tin HLB, câu cấm, thương hiệu, giọng văn) giữ nguyên như `quy_tac_cham.md` mục 1, 2, 3, 5, 6: đọc các mục đó ở `quy_tac_cham.md`, file này chỉ ghi phần khác. Khi file này khác file gốc, file gốc đúng.
Mã nguồn: 6_Agent_Danh_muc_HLB.md 323af74f5cce; 2_Knowledge_Du_lieu_tham_chieu_HLB.md 0bc54e5a7b40

Ai sửa `6_Agent_Danh_muc_HLB.md` hoặc Knowledge thì sửa luôn file này nếu quy tắc chấm đổi, rồi chạy `python tools/kiem_tra_bai.py --cap-nhat-quy-tac --danh-muc`.

## 1. Khác bài blog

- Không có H1 (theme tự hiện tên danh mục). Phần B gồm `[KHỐI TRÊN]` rồi `[KHỐI DƯỚI]`, không có chữ trước `[KHỐI TRÊN]`.
- Không có đoạn trả lời nhanh 40-60 từ. Khối trên làm vai trò trả lời nhanh, đoạn đầu khối trên là sapo.
- Quy tắc trình bày chung (Instructions mục 4, người dùng chốt 28/10/2026) áp như blog: câu khoảng 20 từ, đoạn 2,5-3 dòng (không quá 4 dòng), quan hệ từ nối mạch, gạch đầu dòng, in đậm ý chính, câu kết mỗi H2 dẫn sang H2 sau, ảnh theo phần, kết có tóm tắt, đánh giá, từ khóa chính, CTA.
- Không có Slug, Excerpt, Tag, Category. Phần A có Danh mục, Term ID, Link danh mục (khớp `nghien_cuu/DM_<slug>/danh_muc.json`), Focus keyword, SEO title, Meta description.
- Ảnh (28/10/2026): khối dưới, H2 không có H3 có 1 ảnh, mỗi H3 ưu tiên 1 ảnh, trừ FAQ và kết; khối trên không đặt ảnh.

## 2. Dữ liệu (lỗi bắt buộc khi sai)

- Chỉ nêu sản phẩm đang bán trong chính danh mục: model phải có trong `nghien_cuu/DM_<slug>/san_pham.json` (`kiem_tra_bai.py` tự so). Nêu model của danh mục khác hoặc không còn bán là lỗi bắt buộc.
- Thông số, giá theo `san_pham.md` (đọc từ trang sản phẩm và CSV mới nhất). Giá ghi "giá tham khảo tại thời điểm [ngày]", hãng khác theo `quy_tac_cham.md` mục 4.
- Số model, số hãng trong danh mục ("danh mục có 21 mẫu", "4 thương hiệu") phải đếm đúng `san_pham.json`.
- Ý giữ lại từ nội dung cũ vẫn phải đúng nguồn hiện tại. Thông số, giá, câu ở Knowledge mục 5 trong nội dung cũ phải đã bị bỏ, và ghi ở phần C.

## 3. Khối trên

- 80-150 từ, 1-2 đoạn, không heading. Đoạn đầu là sapo: từ khóa chính ở câu đầu tiên (script, thiếu là lỗi bắt buộc), 2,5-3 dòng.
- Nói danh mục có những dòng đèn nào (theo hãng, kiểu đèn), hợp xưởng nào, một câu mời báo giá có hotline 0967569588.
- Không kể lịch sử công ty, không giới thiệu chung về đèn LED, không lặp ý khối dưới.

## 4. Khối dưới

- Mở bằng 1-2 câu dẫn, rồi các H2 đúng outline đã chốt (lệch là lỗi bắt buộc). Không nhảy cấp.
- Cách trình bày phải phục vụ search intent (Agent quyết, không theo khung cứng): người tìm chọn mua thì có chỗ chọn model, giá, đặt hàng; phần chỉ để đủ khung mà không phục vụ intent là nên sửa (tiêu chí gon, chon_mua).
- Đúng danh mục: danh mục cha hay con theo hãng chọn đúng `6_Agent_Danh_muc_HLB.md` Bước 0; từ khóa có tên hãng mà viết cho danh mục cha (hoặc ngược lại) là lỗi bắt buộc.
- Ngắn hơn bài blog, mỗi phần đúng phạm vi. Phần giải thích dài (cách tính số đèn, tiêu chuẩn độ rọi) chỉ tóm 1-2 câu rồi link sang bài blog. Chép lại cả đoạn bài blog là nên sửa.
- Phương án hợp trường hợp phổ biến nói trước. Bảng so sánh dùng đúng sản phẩm trong danh mục, tối đa 5 cột, ô thiếu ghi "không công bố".
- FAQ (nếu có) 3-5 câu, không lặp phần trên.
- Kết khối dưới (H2 cuối, sau FAQ): tóm tắt, đánh giá các lựa chọn theo trường hợp, có từ khóa chính. CTA ở cuối: hotline, Zalo 0967569588, email, link trang Liên hệ.

## 5. SEO, link

- SEO title 55-65 ký tự, có từ khóa chính. Meta 150-155 ký tự, từ khóa chính trong 30 ký tự đầu, không lặp quá 2 lần, theo 5W1H hợp intent, có từ gợi hành động. Ít nhất một H2 có từ khóa chính hoặc biến thể gần.
- Link nội bộ 2-6: bài blog liên quan, danh mục cha, con hoặc công suất gần. Không link về chính danh mục. Link ngoài tối đa 2. Không link haledco.com, không link website hãng.
- Có bài blog cùng intent trên website thì phần C phải ghi URL và cách phân vai (danh mục giữ từ khóa mua hàng, bài blog giữ từ khóa tìm hiểu, hai bên link qua lại).

## 6. Phần C

Ý cũ giữ, ý bỏ và lý do; nguồn số liệu, ngày đọc; placeholder còn lại; bài blog trùng intent (nếu có); điểm cần người dùng quyết.

## 7. Thang chấm danh mục (tổng 100, ngưỡng 95)

| Mã | Tiêu chí | Điểm |
|---|---|---|
| du_lieu | Chính xác dữ liệu và kỹ thuật: đúng sản phẩm trong danh mục, thông số, giá, số đếm, nội dung cũ sai đã bỏ, kiến thức chiếu sáng và gợi ý chọn đèn đúng | 25 |
| chon_mua | Giúp chọn mua: khối trên trả lời ngay danh mục có gì, hợp xưởng nào; khối dưới giúp chọn model, công suất, có phương án phổ biến trước | 20 |
| seo | SEO và technical: chọn đúng danh mục, SEO title, meta, từ khóa, heading đúng outline, link nội bộ, phân vai với bài blog, định dạng hợp theme | 15 |
| gon | Gọn, đúng phạm vi trang danh mục: không lan man, không chép bài blog, không lặp ý giữa khối trên, khối dưới, FAQ | 10 |
| thuong_hieu | Thương hiệu và giọng văn: vai trò HLB, bảo hành, so sánh hãng công bằng, câu cấm, giọng chuyên gia | 15 |
| cta | Mời mua hàng: CTA khối trên, khối dưới đúng số, đúng dịch vụ đã công bố, nói rõ khách gửi gì và nhận gì | 15 |
