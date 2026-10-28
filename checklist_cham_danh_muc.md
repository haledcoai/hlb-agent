# CHECKLIST CHẤM NỘI DUNG DANH MỤC HLB

Phiên bản: 28/10/2026 (thêm quy tắc trình bày người dùng chốt 28/10), thang chấm dm1. Agent `danh-gia-danh-muc` dùng file này mỗi lần chấm file `DM_*.md`, cùng `quy_tac_cham_danh_muc.md` và các mục dùng chung ở `quy_tac_cham.md`. Vai trò của agent là Leader Content 7 năm kinh nghiệm (người dùng chốt 27/10/2026). Agent hiểu kỹ thuật chiếu sáng nhà xưởng, technical SEO của trang danh mục WooCommerce, và biết thế nào là một trang danh mục viết hay, bán được hàng.

Phần lớn các mục lấy từ quy tắc đã có. Số trong ngoặc là mục của `quy_tac_cham_danh_muc.md`, chữ QC kèm số là mục của `quy_tac_cham.md`. Các mục ghi "(Leader Content)" là chuẩn chuyên môn người dùng giao cho vai trò này. Những mục đó chỉ bắt cái sai, cái yếu thấy được trong bài, không đặt thêm thông số hay chính sách mới. Khi quy tắc gốc đổi, sửa luôn mục tương ứng ở đây.

## Cách dùng

- Rà đủ mọi mục ở mỗi lần chấm, kể cả vòng 2, 3 và khi chấm lại sau góp ý của người dùng.
- Mỗi mục nhận một trong bốn kết quả:
  - **Đạt**
  - **Chưa đạt**: thành một vấn đề ở mục 1, 2 hoặc 2b của báo cáo, kèm mã mục (ví dụ "K3").
  - **Không áp dụng**: ví dụ danh mục chỉ có một hãng thì bỏ T3.
  - **Chưa kiểm tra**: không mở được nguồn. Ghi ở mục 4 của báo cáo, không tính là Đạt.
- Cột Mức: **BB** là lỗi bắt buộc sửa, **NS** là nên sửa, **2b** là việc người dùng quyết. Lỗi chỉ dựa trên trí nhớ, chưa mở được nguồn, thì xếp NS kèm `[CẦN KIỂM TRA]`, không xếp BB.

## Quy tắc chấm khắt khe

1. Một tiêu chí chỉ được điểm tối đa khi mọi mục của nó là Đạt hoặc Không áp dụng.
2. Mỗi vấn đề nên sửa trừ ít nhất 1 điểm, mỗi lỗi bắt buộc trừ ít nhất 2 điểm, ở đúng tiêu chí của mục. Một vấn đề chỉ trừ ở một tiêu chí.
3. Cùng một lỗi lặp ở nhiều chỗ thì ghi thành một vấn đề, liệt kê đủ mọi vị trí.
4. ĐẠT nghĩa là nội dung ghi lên danh mục được ngay mà người dùng không phải sửa thêm câu chữ hay số liệu. Nội dung danh mục hiện công khai ngay khi áp dụng, nên mọi nghi ngờ về số liệu phải kiểm tra cho xong, hoặc xếp thành vấn đề.
5. Đọc như người mua thật: chủ xưởng hoặc nhà thầu vào trang danh mục, lướt khối trên, nhìn lưới sản phẩm, kéo xuống khối dưới. Chỗ nào khiến họ phải đoán, phải tự tính, hoặc phải rời trang để tìm câu trả lời đều là điểm yếu cần ghi.

## 1. Chính xác dữ liệu và kỹ thuật (du_lieu, 25 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| D1 | Mọi model nêu trong bài có trong `san_pham.json` của chính danh mục, còn bán (2) | BB |
| D2 | Thông số (công suất, lumen, hiệu suất, góc chiếu, IP, Ra, nhiệt độ màu, kích thước) khớp `san_pham.md` của đúng model, không áp cho cả dòng hay cả hãng. Tra bằng `kiem_tra_bai.py --tra` (2, QC4) | BB |
| D3 | Số đếm ("21 mẫu", "4 thương hiệu", "từ ... đến ... lm") đếm lại bằng script trên `san_pham.json` (2) | BB |
| D4 | Giá ghi "giá tham khảo tại thời điểm [ngày]", lấy ở khối đầu trang của chính sản phẩm; hãng khác theo QC4 (2) | Sai giá BB, thiếu ngày NS |
| D5 | Ý giữ lại từ nội dung cũ vẫn đúng nguồn hiện tại; thông số, giá, câu cấm (Knowledge mục 5) trong nội dung cũ đã bỏ và ghi ở phần C (2) | BB |
| D6 | Số suy ra (lm/W tự tính, số đèn ước tính) ghi rõ "ước tính" hoặc "tính từ thông số công bố"; tính lại bằng Python (QC4) | Tính sai BB, thiếu ghi chú NS |
| K1 | (Leader Content) Kiến thức chiếu sáng viết đúng: ý nghĩa IP, Ra, góc chiếu, nhiệt độ màu, hiệu suất lm/W, driver, tản nhiệt; không nhầm công suất với độ sáng; không hứa tuổi thọ, độ bền vượt thông số công bố (QC4) | Sai kiến thức BB |
| K2 | (Leader Content) Gợi ý chọn đèn hợp lý về kỹ thuật: công suất đi với chiều cao lắp và diện tích, góc chiếu đi với chiều cao trần, cấp IP đi với môi trường bụi, ẩm, nhiệt độ cao. Mỗi gợi ý có điều kiện đi kèm, không đưa một con số áp cho mọi xưởng | Gợi ý sai BB, thiếu điều kiện NS |
| K3 | (Leader Content) Mức độ rọi, tiêu chuẩn nêu trong bài đúng `tieu_chuan_da_kiem.csv` hoặc có nguồn; phần giải thích dài chỉ tóm 1-2 câu rồi link bài blog (4, QC4) | Sai giá trị BB, thiếu nguồn NS |
| K4 | Không bịa dự án, khách hàng, chứng nhận, số liệu thị trường (QC4) | BB |

## 2. Giúp chọn mua (chon_mua, 20 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| C1 | Khối trên trả lời ngay: danh mục có những dòng đèn nào (theo hãng, kiểu đèn), hợp xưởng nào; đoạn đầu là sapo, từ khóa chính ở câu đầu tiên; 80-150 từ, 1-2 đoạn, không heading (3) | Thiếu từ khóa ở câu đầu BB; độ dài, heading theo script; còn lại NS |
| C2 | Khối dưới có chỗ giúp chọn model cụ thể: bảng chọn nhanh theo chiều cao trần, diện tích, môi trường, hoặc so sánh các dòng trong danh mục. Phương án hợp trường hợp phổ biến nói trước (4) | NS |
| C3 | Có nói khi nào một dòng đèn KHÔNG hợp (ví dụ xưởng nóng, trần thấp, cần chống bụi), để khách tự loại phương án | NS |
| C4 | Bố cục phục vụ search intent của từ khóa chính, đối chiếu trang top trong `nghien_cuu/DM_<slug>/serp/`; phần chỉ để đủ khung mà không giúp chọn mua là nên sửa (4). Thư mục trống thì ghi Chưa kiểm tra | NS |
| C5 | (Leader Content) Có ít nhất một góc giá trị mà trang danh mục top chưa có, dùng được ngay khi chọn đèn (ví dụ bảng chọn nhanh model theo trần 6 m, 8 m, 10 m, lưu ý xưởng bụi) | NS |
| C6 | FAQ (nếu có) 3-5 câu, hỏi đúng thắc mắc trước khi mua (giá theo số lượng, bảo hành, giao hàng, chọn công suất), trả lời thẳng ở câu đầu, không lặp phần trên (4) | NS |

## 3. SEO và technical (seo, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| S1 | Phần A khớp `danh_muc.json` (Danh mục, Term ID, Link); chọn đúng danh mục cha hay con theo hãng theo `6_Agent_Danh_muc_HLB.md` Bước 0 (4) | BB |
| S2 | SEO title dưới 60 ký tự, có từ khóa chính, đọc như tên trang bán hàng; meta 150-155 ký tự, từ khóa chính ở phần đầu, không lặp quá 2 lần, theo 5W1H hợp intent, có từ gợi hành động và lý do để bấm (5) | Theo script; thiếu từ khóa hoặc không ở đầu BB |
| S3 | Không H1 trong phần B; H2, H3 đúng outline đã chốt, không nhảy cấp; ít nhất một H2 có từ khóa chính hoặc biến thể gần (1, 4, 5) | Lệch outline BB, còn lại NS |
| S4 | Link nội bộ 2-6: bài blog liên quan, danh mục cha, con hoặc công suất gần; không link về chính danh mục; anchor mô tả đúng trang đích, đặt trong câu có ngữ cảnh; link ngoài tối đa 2; không haledco.com, không website hãng (5) | BB |
| S5 | (Leader Content) Không ăn thịt từ khóa với bài blog: có bài blog cùng intent thì phần C ghi URL và phân vai, danh mục giữ từ khóa mua hàng, hai bên link qua lại (5) | NS |
| S6 | (Leader Content) Định dạng hợp với mô tả danh mục của theme: bảng tối đa 5 cột, đọc được trên điện thoại; không chèn shortcode, script, HTML lạ; ô thiếu dữ liệu ghi "không công bố" (4) | NS |
| S7 | (Leader Content) Từ khóa phụ đặt tự nhiên, không nhồi; cùng một cụm từ khóa không lặp liên tục ở các câu sát nhau | NS |

## 4. Gọn, đúng phạm vi (gon, 10 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| G1 | Không giới thiệu chung về đèn LED, không kể lịch sử công ty ở khối trên (3) | NS |
| G2 | Không chép lại đoạn bài blog; giải thích dài chỉ tóm 1-2 câu rồi link (4) | NS |
| G3 | Không lặp ý giữa khối trên, khối dưới, FAQ (3, 4) | NS |
| G4 | (Leader Content) Mỗi câu có việc: không câu rỗng, câu lấp chỗ, câu dẫn dài trước khi vào ý; câu khoảng 20 từ, đoạn 2,5-3 dòng (không quá 4 dòng), quan hệ từ nối mạch; liệt kê dùng gạch đầu dòng, ý chính in đậm; khách lướt vẫn bắt được ý chính (Instructions 4) | NS |
| G5 | Mỗi H2 khối dưới (trừ FAQ, kết) có câu kết chốt ý, dẫn sang H2 sau, có thông tin; kết khối dưới tóm tắt, đánh giá các lựa chọn theo trường hợp, có từ khóa chính (Instructions 4) | NS |
| G6 | Ảnh khối dưới: H2 không có H3 có 1 ảnh, mỗi H3 ưu tiên 1 ảnh (trừ FAQ, kết), ảnh khớp đoạn, đúng vị trí theo vai trò; khối trên không có ảnh (Instructions 4) | NS |

## 5. Thương hiệu, giọng văn (thuong_hieu, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| T1 | HLB phân phối đèn LED của nhiều thương hiệu (HALEDCO, Philips, Rạng Đông, Điện Quang); không "HLB sản xuất"; "đèn do HALEDCO sản xuất" là đúng; dòng cao cấp không gán cho riêng một hãng (QC2) | BB |
| T2 | Bảo hành đúng: HALEDCO và dòng cao cấp HLB phân phối 2 năm; hãng khác thường 2 năm; Philips theo từng model. Chính sách, dịch vụ chỉ dùng những gì được phép (QC2) | Sai thời hạn BB, thêm điều kiện ngoài nguồn NS |
| T3 | So sánh hãng trong danh mục: cùng công suất, cùng tiêu chí, có nguồn; nêu cả giới hạn của HLB; kết "Chọn A khi..., chọn B khi..."; không hãng thắng chung cuộc, không nói xấu (QC5) | BB |
| T4 | Không câu cấm, không em dash, en dash, emoji, từ tuyệt đối, cụm văn mẫu AI (QC3, QC6) | BB |
| T5 | (Leader Content) Giọng người bán hàng có chuyên môn 7-10 năm: câu cụ thể, có số, có điều kiện; xưng "chúng tôi" hoặc "HLB", gọi khách là "bạn"; tiếng Việt đơn giản, không dịch gượng, không quảng cáo quá đà (QC6) | NS |
| T6 | Thuật ngữ theo Knowledge mục 7, giải thích ngắn ở lần đầu, thống nhất cả trang (QC6) | NS |

## 6. Mời mua hàng (cta, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| A1 | Khối trên có một câu mời báo giá kèm hotline 0967569588 (3) | BB |
| A2 | CTA cuối khối dưới đủ hotline, Zalo 0967569588, email denlednhaxuongcaocap@gmail.com, link trang Liên hệ; đúng số, đúng chỗ dùng (4, QC2) | BB |
| A3 | (Leader Content) CTA nói rõ khách gửi gì (diện tích, chiều cao trần, môi trường, số lượng) và nhận gì (báo giá theo số lượng, gợi ý model, tính số đèn), chỉ nhắc dịch vụ đã được phép | NS |
| A4 | (Leader Content) Lời mời gắn với nhu cầu vừa đọc, không chung chung kiểu "liên hệ ngay"; không tạo áp lực giả (khuyến mãi, số lượng có hạn) | NS |

## Ghi checklist vào báo cáo

Đặt ngay sau bảng điểm, mỗi tiêu chí một dòng, chỉ liệt kê mã mục chưa đạt (chi tiết nằm ở mục 1, 2, 2b):

```
## Checklist (mục đạt / mục áp dụng)
- Dữ liệu và kỹ thuật: 9/10, chưa đạt K2
- Giúp chọn mua: 5/6, chưa đạt C3; chưa kiểm tra C4
- SEO và technical: 7/7
- Gọn: 4/4
- Thương hiệu, giọng văn: 5/5 (T3 không áp dụng)
- Mời mua hàng: 3/4, chưa đạt A3
```
