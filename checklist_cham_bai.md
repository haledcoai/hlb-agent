# CHECKLIST CHẤM BÀI BLOG HLB

Phiên bản: 28/10/2026 (thêm quy tắc trình bày người dùng chốt 28/10), thang chấm v3. Agent đánh giá (Leader Content) dùng file này cùng `quy_tac_cham.md` mỗi lần chấm bài blog `Bai_*.md`.

Checklist không đặt quy tắc mới. Mỗi mục là một quy tắc đã có trong Instructions hoặc Knowledge (số trong ngoặc là mục của `quy_tac_cham.md`), xếp theo 6 tiêu chí chấm để biết trừ điểm ở đâu. Khi Instructions hoặc Knowledge đổi một quy tắc có trong đây, sửa luôn mục tương ứng.

## Cách dùng

- Rà đủ mọi mục ở mỗi lần chấm, kể cả vòng 2, 3 và khi chấm lại sau góp ý của người dùng. Không bỏ mục nào vì "vòng trước đã đạt".
- Mỗi mục nhận một trong bốn kết quả:
  - **Đạt**
  - **Chưa đạt**: phải thành một vấn đề ở mục 1, 2 hoặc 2b của báo cáo, ghi kèm mã mục (ví dụ "D4").
  - **Không áp dụng**: bài không có phần đó, ví dụ bài không so sánh hãng thì bỏ T4.
  - **Chưa kiểm tra**: không mở được nguồn. Ghi ở mục 4 của báo cáo, không tính là Đạt.
- Cột Mức: **BB** là lỗi bắt buộc sửa, **NS** là nên sửa, **2b** là việc người dùng quyết. Lỗi chỉ dựa trên trí nhớ mà chưa mở được nguồn thì không xếp BB, xếp NS kèm `[CẦN KIỂM TRA]`.

## Quy tắc chấm khắt khe

1. Một tiêu chí chỉ được điểm tối đa khi mọi mục của tiêu chí đó là Đạt hoặc Không áp dụng.
2. Mỗi vấn đề nên sửa trừ ít nhất 1 điểm, mỗi lỗi bắt buộc trừ ít nhất 2 điểm, ở đúng tiêu chí của mục. Một vấn đề chỉ trừ ở một tiêu chí.
3. Cùng một lỗi lặp ở nhiều chỗ: ghi một vấn đề, liệt kê đủ mọi vị trí để agent viết sửa hết một lần.
4. ĐẠT nghĩa là bài đăng được mà người dùng không phải sửa thêm câu chữ hay số liệu. Còn nghi ngờ về một con số thì kiểm tra cho xong, hoặc xếp vấn đề, không cho qua.

## 1. Search intent (intent, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| I1 | Câu trả lời chính nằm trong 2-3 đoạn đầu (6) | NS |
| I2 | Sapo 2,5-3 dòng (khoảng 40-80 từ), từ khóa chính ở câu đầu tiên, nhấn đúng ý tiêu đề, khái quát cả bài, không giới thiệu chung về đèn LED hay về công ty, không mở bằng định nghĩa sách giáo khoa (4) | Thiếu từ khóa ở câu đầu BB (script); còn lại NS |
| I3 | Đoạn trả lời nhanh ngay sau sapo (hoặc gộp với sapo), 40-60 từ, đúng dạng theo loại truy vấn, có số hoặc tiêu chí kèm điều kiện, đọc tách riêng vẫn hiểu (6) | NS |
| I4 | Bài đáp đúng ý định tìm kiếm của từ khóa chính. Từ khóa hợp làm trang danh mục, sản phẩm, hoặc trùng bài đã có thì không tự đổi (CLAUDE.md, Nhóm từ khóa) | 2b |
| I5 | Phương án phù hợp nhất với trường hợp phổ biến được đưa trước (6) | NS |

## 2. Dữ liệu và nguồn (du_lieu, 25 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| D1 | Mọi thông số khớp CSV hoặc trang sản phẩm của đúng model, không áp cho cả dòng hay cả mức công suất (4). Tra bằng `kiem_tra_bai.py --tra`, đếm model bằng script | BB |
| D2 | Số suy ra không trình bày như số công bố. Ước tính ghi "ước tính", lm/W tự tính ghi "tính từ thông số công bố" (4) | BB |
| D3 | Giá lấy ở khối đầu trang của chính sản phẩm, ghi "giá tham khảo tại thời điểm [ngày]", nhắc giá đổi theo số lượng và thời điểm, không nêu % giảm giá. Hãng khác: khoảng giá thị trường có nguồn (4) | Sai giá BB, thiếu ngày hoặc thiếu câu lưu ý NS |
| D4 | Tính lại mọi phép tính bằng Python. Đủ giả định; UF, MF khoảng 0,8 (xưởng bụi MF thấp hơn) hoặc nêu lý do dùng số khác; số đèn làm tròn lên; có lưu ý cần mô phỏng DIALux theo mặt bằng thật (4) | Tính sai BB, thiếu giả định hoặc lưu ý NS |
| D5 | Mã tiêu chuẩn có trong `tieu_chuan_da_kiem.csv` hoặc có nguồn, hoặc `[CẦN KIỂM TRA]`. Giá trị cụ thể (mức lux) đúng văn bản. Không dùng bản đã bị thay thế (4) | Sai giá trị (đã mở nguồn) BB, bản cũ NS |
| D6 | Bảo hành: HALEDCO và dòng cao cấp HLB phân phối 2 năm; hãng khác thường 2 năm; Philips theo từng model, không viết chung 24 tháng (2) | Sai thời hạn BB, thêm điều kiện ngoài nguồn NS |
| D7 | Chính sách, dịch vụ chỉ dùng những gì được phép (2). Điểm đang chờ xác nhận để `[CHỜ XÁC NHẬN]` hoặc không nêu | BB |
| D8 | Không có câu cấm chép từ website (3) | BB |
| D9 | Không bịa dự án, khách hàng, chứng nhận, số liệu thị trường. Kiến thức chung (IP, Ra, PF, tuổi thọ, góc chiếu) viết đúng (4) | BB |
| D10 | Không chép câu, đoạn, bảng của bài đối thủ. Script: trùng từ 25 từ liền nhau là LỖI, từ 10 từ là cảnh báo (4) | 25 từ BB, 10 từ NS |

## 3. Chuyên môn và EEAT (eeat, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| E1 | Mỗi khuyến nghị có lý do đi kèm, người đọc hiểu vì sao chọn như vậy | NS |
| E2 | Có nói khi nào phương án KHÔNG phù hợp | NS |
| E3 | Có ít nhất một điểm chuyên sâu mà bài top chưa có. Đối chiếu `nghien_cuu/<bài>/serp/`; thư mục trống thì ghi Chưa kiểm tra | NS |
| E4 | Có kinh nghiệm thực tế: tình huống phổ biến, lỗi hay gặp, cách xử lý tại công trình, ví dụ cụ thể dùng được ngay; không bịa tên dự án, khách hàng (Instructions mục EEAT) | NS (bịa dự án: D9) |

## 4. Thương hiệu và tuân thủ (thuong_hieu, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| T1 | HLB phân phối đèn LED của nhiều thương hiệu (HALEDCO, Philips, Rạng Đông, Điện Quang). Không "HLB sản xuất", "HLB lắp ráp", "nhà máy của chúng tôi". "Đèn do HALEDCO sản xuất" là đúng. Dòng cao cấp không gán cho riêng một hãng (2) | BB |
| T2 | Mốc 2011 gắn HALEDCO, 2018 gắn HLB; không cộng gộp, không tự tính "X năm kinh nghiệm" (2) | BB |
| T3 | Chỉ dùng hotline 0967569588, 02437 918 122 và email denlednhaxuongcaocap@gmail.com, đúng chỗ dùng (2) | BB |
| T4 | So sánh hãng: cùng công suất, cùng loại đèn, cùng tiêu chí, có nguồn; ô thiếu ghi "không công bố"; nêu cả giới hạn của HLB; kết "Chọn A khi..., chọn B khi..."; không hãng thắng chung cuộc, không nói xấu (5) | BB |
| T5 | Không link, không nhắc haledco.com; không link website hãng đèn hay cửa hàng (1, 5) | BB |
| T6 | Hãng không bán trên website: chỉ nêu điểm tốt khi cần, ghi "theo thông tin công bố của hãng", không so với HLB (5) | NS |
| T7 | Mọi bài có CTA ở cuối kết bài, 1-2 câu, nói khách gửi gì và nhận gì, có từ gợi hành động, chỉ nhắc dịch vụ được phép (4) | Thiếu CTA NS |

## 5. Giọng văn (giong_van, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| G1 | Đọc như chuyên gia 7-10 năm: câu cụ thể, không câu rỗng, câu lấp chỗ, không quảng cáo quá đà (6) | NS |
| G2 | Không lặp ý giữa các phần; mỗi phần đúng phạm vi của heading (6) | NS |
| G3 | Thuật ngữ theo Knowledge mục 7, giải thích ngắn ở lần đầu, thống nhất cả bài (6) | NS |
| G4 | Xưng "chúng tôi" hoặc "HLB", gọi người đọc là "bạn"; tiếng Việt đơn giản, không dịch gượng (6) | NS |
| G5 | Câu khoảng 20 từ (từ 35 từ phải ngắt); đoạn 2,5-3 dòng, không quá 4 dòng (khoảng 80 từ); quan hệ từ dùng đa dạng để nối mạch, câu nối mỗi kiểu không quá 1-2 lần; định dạng số đúng (4) | NS |
| G8 | Liệt kê từ 3 ý dùng gạch đầu dòng; ý chính, con số quan trọng in đậm, không in đậm dày đặc (4) | NS |
| G6 | Bài lắp đặt, đấu nối có lưu ý an toàn điện và làm việc trên cao đúng ở bước có rủi ro (6) | NS |
| G7 | Không em dash, en dash, emoji, từ tuyệt đối, cụm văn mẫu AI (6) | BB |

## 6. Cấu trúc và SEO (cau_truc, 15 điểm)

| Mã | Kiểm tra | Mức |
|---|---|---|
| S1 | Heading khớp outline đã chốt: đủ, đúng thứ tự, đúng cấp, đúng chữ (1) | BB (lệch ở FAQ: NS) |
| S2 | Một H1 dài 55-65 ký tự, không nhảy cấp, không H5, H6, H4 chỉ khi H3 có từ 2 ý con, heading cụ thể (7) | Theo script |
| S3 | Từ khóa chính ở SEO title, H1, câu đầu sapo, 100 chữ đầu, ít nhất một H2, meta (phần đầu), slug, kết bài; từ khóa phụ tối đa 5, đặt tự nhiên (7) | Thiếu ở title, H1, câu đầu sapo, 100 chữ đầu, phần đầu meta BB; còn lại NS |
| S4 | SEO title 55-65 ký tự; meta 150-155 ký tự, từ khóa không lặp quá 2 lần, trả lời theo 5W1H hợp intent, có từ gợi hành động; slug không dấu, 3-6 từ, không năm; excerpt dưới 200, không trùng meta; tag 3-5 (7) | Theo script |
| S5 | Link nội bộ 3-5 (1-3 về danh mục), link ngoài 0-3 tới nguồn có thẩm quyền; anchor mô tả đúng trang đích, đặt trong câu có ngữ cảnh; một URL một lần; không link 404; URL chưa kiểm tra dùng `[LINK: ...]` (7) | BB |
| S6 | Bảng dùng khi so sánh từ 3 tiêu chí, tối đa 5 cột, hàng xếp theo thứ tự dễ đọc (6) | NS |
| S7 | Ảnh `[ẢNH: chú thích \| alt \| tên file]`, alt dưới 125 ký tự, tên file không trùng slug, mô tả khớp đoạn chứa ảnh. Số lượng: H2 không có H3 có 1 ảnh, mỗi H3 ưu tiên 1 ảnh (trừ FAQ, kết bài). Vị trí: ảnh hướng dẫn, giải thích ở trên hoặc cạnh đoạn mô tả; ảnh minh họa, chứng minh kết quả sau đoạn nội dung (4, 7) | Thiếu alt, trùng slug BB; còn lại NS |
| S8 | FAQ 3-5 câu, trước kết bài, mỗi câu trả lời 40-80 từ, trả lời thẳng ở câu đầu, không lặp thân bài (7) | NS |
| S9 | Kết bài là H2 cuối (sau FAQ): tóm tắt, đánh giá cả bài, khuyến nghị theo từng trường hợp, có từ khóa chính, không mở bằng "Tóm lại", "Nhìn chung", không chép nguyên câu thân bài, không mâu thuẫn thân bài (4) | NS |
| S12 | Mỗi H2 (trừ FAQ, kết bài) có câu kết chốt ý và gợi ra câu hỏi H2 sau trả lời, có thông tin, không phải câu dẫn rỗng (4) | NS |
| S10 | Phần C đủ: placeholder kèm vị trí, nguồn (URL, ngày), link chưa xác minh, đề xuất link từ bài cũ, ảnh, schema, chênh lệch trên website, điểm cần người dùng quyết; bài viết lại có ý bài gốc đã bỏ và lý do (7) | Placeholder phần B thiếu ở C: BB; thiếu mục khác: NS |
| S11 | Phần B không quá 5 chỗ `[CẦN BỔ SUNG]`. Quá thì hook chặn đăng nháp: gom danh sách dữ liệu cần bổ sung | 2b |

## Ghi checklist vào báo cáo

Đặt ngay sau bảng điểm, mỗi tiêu chí một dòng, chỉ liệt kê mã mục chưa đạt (chi tiết nằm ở mục 1, 2, 2b):

```
## Checklist (mục đạt / mục áp dụng)
- Intent: 5/5
- Dữ liệu: 9/10, chưa đạt D4
- EEAT: 3/4, chưa đạt E2; chưa kiểm tra E3
- Thương hiệu: 6/6 (T4 không áp dụng)
- Giọng văn: 6/7, chưa đạt G2
- Cấu trúc và SEO: 11/11
```
