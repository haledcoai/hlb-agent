# QUY TẮC CHẤM BÀI HLB (BẢN RÚT GỌN CHO AGENT ĐÁNH GIÁ)

Phiên bản: 28/10/2026. Rút từ `1_Project_Instructions_Auto_Blog_HLB.md` (Instructions) và `2_Knowledge_Du_lieu_tham_chieu_HLB.md` (Knowledge), chỉ giữ phần dùng để chấm. Khi file này khác file gốc, file gốc đúng. File này chỉ chép lại quy tắc của file gốc, không thêm điều kiện, ví dụ hay mức nghiêm mới.
Mã nguồn: 1_Project_Instructions_Auto_Blog_HLB.md 1131b8aa2dc4; 2_Knowledge_Du_lieu_tham_chieu_HLB.md 6d7e23c41fd6

Cách dùng: agent đánh giá đọc file này thay cho hai file gốc. `kiem_tra_bai.py` báo "quy_tac_cham.md làm từ bản Instructions/Knowledge cũ" thì lần chấm đó đọc hai file gốc. Cần tra chi tiết (danh sách URL danh mục, bài đã có, bảng bảo hành hãng) thì Grep đúng mục trong Knowledge, không đọc cả file.

Ai sửa Instructions hoặc Knowledge thì sửa luôn file này nếu quy tắc chấm đổi, rồi chạy `python tools/kiem_tra_bai.py --cap-nhat-quy-tac`.

## 1. Bốn quy tắc cốt lõi (vi phạm là lỗi bắt buộc)

1. Không bịa thông số, giá, chứng nhận, bảo hành, dự án. Thiếu dữ liệu thì placeholder.
2. So sánh công bằng, không nói xấu thương hiệu nào, không phán hãng nào "tốt nhất".
3. Không link, không nhắc haledco.com.
4. Heading đúng outline đã chốt. `kiem_tra_bai.py` so với `nghien_cuu/<bài>/outline.md` khi có file (lệch là LỖI, lệch ở FAQ là cảnh báo).

## 2. Thông tin HLB được phép dùng (Knowledge mục 1, 1.1)

- Vai trò (chốt 23/10/2026): **HLB phân phối đèn LED của nhiều thương hiệu, gồm HALEDCO, Philips, Rạng Đông, Điện Quang.** HALEDCO là đơn vị sản xuất và phân phối đèn LED (nhắc lại 26/10/2026): "đèn do HALEDCO sản xuất" cho sản phẩm HALEDCO là đúng, không bắt lỗi. Dòng cao cấp gọi là "dòng đèn cao cấp HLB phân phối", dòng này gồm đèn của nhiều thương hiệu, không gán cho riêng một hãng sản xuất (người dùng chốt 26/10/2026). Sai: "HLB sản xuất", "HLB lắp ráp", "nhà máy/xưởng của chúng tôi", giới thiệu dài về HALEDCO.
- Mốc: HALEDCO sản xuất đèn LED từ 2011; HLB phân phối đèn LED nhà xưởng từ 2018. Không cộng gộp, không tự tính "X năm kinh nghiệm".
- Pháp nhân: trực thuộc Công ty TNHH Công nghệ và Xúc tiến Thương mại HALEDCO.
- Liên hệ: hotline bán hàng, Zalo 0967569588 (dùng trong bài, CTA); kỹ thuật, bảo hành 02437 918 122 (phần bảo hành, sự cố); email denlednhaxuongcaocap@gmail.com. Số khác là lỗi.
- Bảo hành dòng cao cấp HLB phân phối: 2 năm, linh kiện driver (bộ nguồn) và chip LED, cần giấy tờ bảo hành. Đèn HALEDCO: 2 năm. Các hãng khác thường 2 năm (viết chung được), Philips cụ thể theo từng model.
- Mức lỗi bảo hành (26/10/2026): sai thời hạn là bắt buộc; thêm điều kiện không có trong nguồn là nên sửa.
- Rạng Đông, Điện Quang: 24 tháng theo chính sách hãng. Philips: theo từng model trên signify.com, **không viết chung 24 tháng**.
- Đổi trả theo nhu cầu (đổi công suất, model, linh kiện): trong vòng 15 ngày, khách chịu phí 10% giá trị hàng (người dùng xác nhận 04/11/2026). Áp dụng chung mọi thương hiệu (11/11/2026). Lỗi trong 15 ngày đầu, còn mới, còn tem: đổi mới. Hàng lỗi do nhà sản xuất: đổi trả hoàn toàn miễn phí, không tính 10%. Xử lý bảo hành khoảng 10-15 ngày. Giao từ kho Hà Nội.
- HLB không nhận lắp đặt (11/11/2026): bài nhắc dịch vụ lắp đặt, "HLB lắp đặt", "thi công trọn gói" là lỗi bắt buộc. Được nhắc khảo sát tại công trình và hàng mẫu miễn phí cho dự án.
- Giao hàng toàn quốc, không nêu số ngày. Miễn phí khi đơn trên 5 triệu đồng trong bán kính 10 km tính từ văn phòng Xuân Đỉnh.
- Chiết khấu: chỉ nói "có chính sách chiết khấu cho dự án, đại lý, đơn số lượng lớn", không nêu mức.
- Dịch vụ đã công bố trên trang sản phẩm dòng cao cấp: hàng mẫu miễn phí cho dự án, kiểm định chất lượng tại nhà máy (câu công bố của trang, không biến thành "nhà máy của HLB"), đặt hàng theo yêu cầu, giao toàn quốc, tính bố trí đèn bằng DIALux khi khách gửi kích thước. Chọn hãng chip, driver chỉ với model có ghi trên trang sản phẩm.
- Chỉ dùng khi người dùng cung cấp: số dự án, tên công trình, khách hàng, chứng nhận từng model, giá đại lý, năng lực sản xuất, thời gian giao cụ thể. Không dùng nhận xét khách hàng ở trang chủ.

## 3. Câu cấm chép từ website (Knowledge mục 5)

"Tiết kiệm 70% điện", "tăng hiệu quả làm mát 30%", "không nên chiếu sáng liên tục quá 10 tiếng", ghép "ISO 9001:2015: TCVN 7722-1:2009/IEC 60598-1:2008" thành chứng nhận sản phẩm, "Graphene, TCPlus" khi không ghi "theo công bố trên trang sản phẩm", "đổi trả trong vòng tuần", "bảo hành 24 tháng" cho Philips.

## 4. Dữ liệu và giá (Instructions mục 6, Knowledge mục 3, 6, 8.2)

- Nguồn theo thứ tự: trang sản phẩm trên website (CSV `du_lieu_san_pham_HLB_*.csv` mới nhất, làm mới bằng `tools/lam_moi_csv.py`), website chính thức của hãng, người dùng. Phần C phải có URL và ngày.
- Thông số là của một model, không áp cho cả dòng hoặc cả mức công suất. Hiệu suất lm/W được tính từ quang thông chia công suất nếu ghi "tính từ thông số công bố".
- Số suy ra không được trình bày như số công bố. Ước tính trong ví dụ phải ghi "ước tính".
- Giá: giá đang bán ở khối đầu trang của chính sản phẩm (hoặc API `wc/store/v1/products?slug=`), ghi "giá tham khảo tại thời điểm [ngày]", nhắc giá đổi theo số lượng, thời điểm. Không lấy giá ở "Sản phẩm liên quan". Không nhắc % giảm giá.
- Philips, Rạng Đông, Điện Quang (26/10/2026): thông số theo hãng công bố được (có nguồn), giá ghi khoảng giá thị trường có nguồn và ngày ở phần C. Dòng cao cấp HLB phân phối: giá, thông số đúng trang sản phẩm.
- Mã tiêu chuẩn (TCVN, QCVN, IEC), giá trị độ rọi theo tiêu chuẩn, giá điện, số liệu thị trường: phải có nguồn hoặc `[CẦN KIỂM TRA]`. Mã có trong `tieu_chuan_da_kiem.csv` là đã có nguồn; giá trị cụ thể (mức lux) vẫn phải đúng văn bản. Dùng bản đã bị thay thế (ví dụ TCVN 4255:2008) là nên sửa.
- Kiến thức chung được viết không cần nguồn nhưng phải đúng: IP theo IEC 60529 (số đầu chống bụi, số sau chống nước; IP54 nước bắn tóe, IP65 tia nước, IP66 tia nước mạnh); Ra trên 70 cho kho, xưởng thô, trên 80 khi cần phân biệt màu; PF càng gần 1 càng ít tổn hao; tuổi thọ là giờ tới khi quang thông giảm tới mức quy định; góc chiếu theo chiều cao chỉ nêu là kinh nghiệm phổ biến.
- Ví dụ tính: ghi đủ giả định; N = (E x S) / (Φ x UF x MF); UF và MF thường giả định khoảng 0,8 (người dùng chốt 26/10/2026), xưởng nhiều bụi lấy MF thấp hơn; làm tròn lên; ưu tiên quang thông của một model cụ thể; kết bằng lưu ý cần mô phỏng DIALux theo mặt bằng thật. Đơn giá điện có nguồn và ngày hoặc ghi giả định.

- Không chép nguyên câu, đoạn, bảng của bài đối thủ (Instructions mục 6). Nghi chép thì ghi nên sửa kèm câu nghi ngờ. `kiem_tra_bai.py` so với văn bản bài top đã lưu ở `nghien_cuu/<bài>/serp/`: đoạn từ 25 từ liền nhau trùng là LỖI, từ 10 từ là cảnh báo.

## 5. Thương hiệu (Instructions mục 7, Knowledge 8.5)

- Philips, Rạng Đông, Điện Quang được so sánh: cùng mức công suất, cùng loại đèn, cùng bộ tiêu chí, có nguồn; ô thiếu ghi "không công bố"; nêu ưu điểm và giới hạn của từng bên kể cả HLB; kết luận "Chọn A khi..., chọn B khi...", không có hãng thắng chung cuộc.
- Hãng không bán trên website: chỉ nêu điểm tốt khi cần, ghi "theo thông tin công bố của hãng", không so với HLB.
- Không link website hãng đèn hoặc cửa hàng, chỉ dẫn tên và ghi URL ở phần C.
- Toplist: mỗi mục cùng cấu trúc, không chấm điểm, không xếp hạng.

## 6. Cách triển khai và giọng văn (Instructions mục 4, 5; Knowledge 7, 8.1, 8.3, 8.4)

- Trình bày theo Instructions mục 4 (người dùng chốt 28/10/2026, blog và danh mục).
- Một chủ đề, đúng intent, mở rộng thông tin hơn bài top. Câu trả lời chính trong 2-3 đoạn đầu.
- Sapo: từ khóa chính ở câu đầu tiên (script, thiếu là LỖI), 2,5-3 dòng (khoảng 40-80 từ), nhấn ý tiêu đề, khái quát cả bài, không giới thiệu chung về LED hay công ty, không mở bằng định nghĩa sách giáo khoa.
- Đoạn trả lời nhanh: ngay sau sapo (hoặc gộp), 40-60 từ, có con số hoặc tiêu chí kèm điều kiện, đọc tách riêng vẫn hiểu. Theo loại truy vấn: "là gì" thì 1-2 câu định nghĩa; "bao nhiêu" thì số kèm điều kiện; "giá" thì khoảng giá kèm ngày; "cách chọn" thì 3-5 tiêu chí gạch đầu dòng; "so sánh" thì "Chọn A khi..., chọn B khi...". Không mở bằng "Câu trả lời là", không lặp H1, không "tùy nhu cầu" mà không nói tùy gì.
- Phương án phù hợp nhất với trường hợp phổ biến đưa trước. Câu khoảng 20 từ (từ 35 từ phải ngắt). Đoạn 2,5-3 dòng, không quá 4 dòng (khoảng 80 từ). Quan hệ từ dùng đa dạng để nối mạch. Liệt kê từ 3 ý dùng gạch đầu dòng, ý chính in đậm (không dày đặc). Bảng khi so sánh từ 3 tiêu chí, tối đa 5 cột.
- Mỗi H2 (trừ FAQ, kết bài) có câu kết chốt ý và gợi ra câu hỏi H2 sau trả lời, có thông tin, không phải câu dẫn rỗng.
- Kết bài (H2 cuối, sau FAQ): tóm tắt, đánh giá cả bài, khuyến nghị theo từng trường hợp, ưu tiên có từ khóa chính, không mở bằng "Tóm lại", "Nhìn chung", không chép nguyên câu thân bài. Mọi bài có CTA ở cuối kết bài, 1-2 câu, nói khách gửi gì và nhận gì, chỉ nhắc dịch vụ ở mục 2.
- Giọng chuyên gia 7-10 năm, tiếng Việt đơn giản, xưng "chúng tôi" hoặc "HLB", gọi "bạn". Bài lắp đặt có lưu ý an toàn đúng ở bước có rủi ro.
- Thuật ngữ: quang thông (lm), độ rọi (lux), hiệu suất chiếu sáng (lm/W), chỉ số hoàn màu (Ra), hệ số công suất (PF), cấp bảo vệ IP, driver (bộ nguồn), góc chiếu, chiếu sáng phủ đều, chiếu sáng mạnh. "Highbay", "UFO" chỉ khi nói kiểu dáng. Thuật ngữ kỹ thuật giải thích ngắn ở lần đầu.
- Cấm (script bắt phần lớn): em dash, en dash, emoji, từ tuyệt đối, cụm văn mẫu AI, câu nối "Điều này", "Ngoài ra", "Bên cạnh đó", "Việc...", "Không chỉ... mà còn" quá 1-2 lần mỗi kiểu.
- Số: 1.000 m², 0,95, 100W, 6500K, IP54, 130 lm/W, 300 lux, 6-8 m, 1.599.000 đồng.

## 7. SEO và đầu ra (Knowledge mục 9, 10)

- Từ khóa chính ở SEO title, H1, câu đầu sapo, 100 chữ đầu, ít nhất một H2, meta (phần đầu), slug, kết bài. Từ khóa phụ tối đa 5, đặt tự nhiên.
- Một H1 dài 55-65 ký tự, không nhảy cấp, H4 chỉ khi H3 có từ 2 ý con, heading cụ thể.
- Link nội bộ 3-5 (1-3 về danh mục), link ngoài 0-3 tới nguồn có thẩm quyền. Anchor mô tả đúng trang đích, đặt trong câu có ngữ cảnh, một URL một lần. URL chưa kiểm tra dùng `[LINK: ...]`.
- SEO title 55-65 ký tự; meta 150-155 ký tự, từ khóa chính trong 30 ký tự đầu, không lặp quá 2 lần, theo 5W1H hợp intent, có từ gợi hành động; slug không dấu, 3-6 từ, không năm (từ khóa chính trên 6 từ: slug lấy 3-6 từ lõi của từ khóa, đúng thứ tự); excerpt dưới 200 ký tự, không trùng meta; tag 3-5.
- Ảnh: H2 không có H3 có 1 ảnh, mỗi H3 ưu tiên 1 ảnh (trừ FAQ, kết bài); ảnh hướng dẫn ở trên hoặc cạnh đoạn mô tả, ảnh chứng minh kết quả sau đoạn. `[ẢNH: chú thích | alt | tên file]`, alt dưới 125 ký tự, tên file .jpg không trùng slug bài hoặc slug đã có trên website, mô tả khớp đoạn chứa ảnh.
- FAQ 3-5 câu, trước kết bài, mỗi câu trả lời 40-80 từ, trả lời thẳng ở câu đầu, không lặp thân bài.
- Phần C: placeholder còn lại kèm vị trí, nguồn (URL, ngày), link chưa xác minh, đề xuất link từ bài cũ, ảnh, schema, chênh lệch trên website, điểm cần người dùng quyết, (bài viết lại) ý bài gốc đã bỏ và lý do.
