# QUY TẮC CHẤM BÀI HLB (BẢN RÚT GỌN CHO AGENT ĐÁNH GIÁ)

Phiên bản: 24/10/2026. Rút từ `1_Project_Instructions_Auto_Blog_HLB.md` (Instructions) và `2_Knowledge_Du_lieu_tham_chieu_HLB.md` (Knowledge), chỉ giữ phần dùng để chấm. Khi file này khác file gốc, file gốc đúng.
Mã nguồn: 1_Project_Instructions_Auto_Blog_HLB.md 56d9f88a19ba; 2_Knowledge_Du_lieu_tham_chieu_HLB.md 42dacec854c4

Cách dùng: agent đánh giá đọc file này thay cho hai file gốc. `kiem_tra_bai.py` báo "quy_tac_cham.md làm từ bản Instructions/Knowledge cũ" thì lần chấm đó đọc hai file gốc. Cần tra chi tiết (danh sách URL danh mục, bài đã có, bảng bảo hành hãng) thì Grep đúng mục trong Knowledge, không đọc cả file.

Ai sửa Instructions hoặc Knowledge thì sửa luôn file này nếu quy tắc chấm đổi, rồi chạy `python tools/kiem_tra_bai.py --cap-nhat-quy-tac`.

## 1. Bốn quy tắc cốt lõi (vi phạm là lỗi bắt buộc)

1. Không bịa thông số, giá, chứng nhận, bảo hành, dự án. Thiếu dữ liệu thì placeholder.
2. So sánh công bằng, không nói xấu thương hiệu nào, không phán hãng nào "tốt nhất".
3. Không link, không nhắc haledco.com.
4. Heading đúng outline đã chốt.

## 2. Thông tin HLB được phép dùng (Knowledge mục 1, 1.1)

- Vai trò (chốt 23/10/2026): **HLB phân phối đèn LED của nhiều thương hiệu, gồm HALEDCO, Philips, Rạng Đông, Điện Quang.** Dòng cao cấp gọi là "dòng đèn cao cấp HLB phân phối", không gán hãng sản xuất. Sai: "HLB sản xuất", "HLB lắp ráp", "nhà máy/xưởng của chúng tôi", "dòng cao cấp do HALEDCO sản xuất", giới thiệu dài về HALEDCO.
- Mốc: HALEDCO sản xuất đèn LED từ 2011; HLB phân phối đèn LED nhà xưởng từ 2018. Không cộng gộp, không tự tính "X năm kinh nghiệm".
- Pháp nhân: trực thuộc Công ty TNHH Công nghệ và Xúc tiến Thương mại HALEDCO.
- Liên hệ: hotline bán hàng, Zalo 0967569588 (dùng trong bài, CTA); kỹ thuật, bảo hành 02437 918 122 (phần bảo hành, sự cố); email denlednhaxuongcaocap@gmail.com. Số khác là lỗi.
- Bảo hành dòng cao cấp HLB phân phối: 2 năm, linh kiện driver (bộ nguồn) và chip LED, cần giấy tờ bảo hành. Không thêm điều kiện ngoài câu này (ví dụ "lỗi do nhà sản xuất").
- Rạng Đông, Điện Quang: 24 tháng theo chính sách hãng. Philips: theo từng model trên signify.com, **không viết chung 24 tháng**.
- Đổi trả theo nhu cầu: phí 10% giá trị hàng. Thời hạn đổi trả, điều kiện 15 ngày, phí khi lỗi sản phẩm: đang chờ xác nhận, bài phải để `[CHỜ XÁC NHẬN]` hoặc không nêu.
- Giao hàng toàn quốc, không nêu số ngày. Miễn phí khi đơn trên 5 triệu đồng trong bán kính 10 km (điểm tính đang chờ xác nhận).
- Chiết khấu: chỉ nói "có chính sách chiết khấu cho dự án, đại lý, đơn số lượng lớn", không nêu mức.
- Dịch vụ đã công bố trên trang sản phẩm dòng cao cấp: hàng mẫu miễn phí cho dự án, kiểm định chất lượng tại nhà máy (câu công bố của trang, không biến thành "nhà máy của HLB"), đặt hàng theo yêu cầu, giao toàn quốc, tính bố trí đèn bằng DIALux khi khách gửi kích thước. Chọn hãng chip, driver chỉ với model có ghi trên trang sản phẩm.
- Chỉ dùng khi người dùng cung cấp: số dự án, tên công trình, khách hàng, chứng nhận từng model, giá đại lý, năng lực sản xuất, thời gian giao cụ thể. Không dùng nhận xét khách hàng ở trang chủ.

## 3. Câu cấm chép từ website (Knowledge mục 5)

"Tiết kiệm 70% điện", "tăng hiệu quả làm mát 30%", "không nên chiếu sáng liên tục quá 10 tiếng", ghép "ISO 9001:2015: TCVN 7722-1:2009/IEC 60598-1:2008" thành chứng nhận sản phẩm, "Graphene, TCPlus" khi không ghi "theo công bố trên trang sản phẩm", "đổi trả trong vòng tuần", "bảo hành 24 tháng" cho Philips.

## 4. Dữ liệu và giá (Instructions mục 6, Knowledge mục 3, 6, 8.2)

- Nguồn theo thứ tự: trang sản phẩm trên website (CSV là bản chụp ngày 21/10/2026), website chính thức của hãng, người dùng. Phần C phải có URL và ngày.
- Thông số là của một model, không áp cho cả dòng hoặc cả mức công suất. Hiệu suất lm/W được tính từ quang thông chia công suất nếu ghi "tính từ thông số công bố".
- Số suy ra không được trình bày như số công bố. Ước tính trong ví dụ phải ghi "ước tính".
- Giá: giá đang bán ở khối đầu trang của chính sản phẩm (hoặc API `wc/store/v1/products?slug=`), ghi "giá tham khảo tại thời điểm [ngày]", nhắc giá đổi theo số lượng, thời điểm. Không lấy giá ở "Sản phẩm liên quan". Không nhắc % giảm giá.
- Mã tiêu chuẩn (TCVN, QCVN, IEC), giá trị độ rọi theo tiêu chuẩn, giá điện, số liệu thị trường: phải có nguồn hoặc `[CẦN KIỂM TRA]`.
- Kiến thức chung được viết không cần nguồn nhưng phải đúng: IP theo IEC 60529 (số đầu chống bụi, số sau chống nước; IP54 nước bắn tóe, IP65 tia nước, IP66 tia nước mạnh); Ra trên 70 cho kho, xưởng thô, trên 80 khi cần phân biệt màu; PF càng gần 1 càng ít tổn hao; tuổi thọ là giờ tới khi quang thông giảm tới mức quy định; góc chiếu theo chiều cao chỉ nêu là kinh nghiệm phổ biến.
- Ví dụ tính: ghi đủ giả định; N = (E x S) / (Φ x UF x MF); UF giả định 0,5-0,7, MF 0,7-0,8, xưởng nhiều bụi lấy thấp; làm tròn lên; ưu tiên quang thông của một model cụ thể; kết bằng lưu ý cần mô phỏng DIALux theo mặt bằng thật. Đơn giá điện có nguồn và ngày hoặc ghi giả định.

## 5. Thương hiệu (Instructions mục 7, Knowledge 8.5)

- Philips, Rạng Đông, Điện Quang được so sánh: cùng mức công suất, cùng loại đèn, cùng bộ tiêu chí, có nguồn; ô thiếu ghi "không công bố"; nêu ưu điểm và giới hạn của từng bên kể cả HLB; kết luận "Chọn A khi..., chọn B khi...", không có hãng thắng chung cuộc.
- Hãng không bán trên website: chỉ nêu điểm tốt khi cần, ghi "theo thông tin công bố của hãng", không so với HLB.
- Không link website hãng đèn hoặc cửa hàng, chỉ dẫn tên và ghi URL ở phần C.
- Toplist: mỗi mục cùng cấu trúc, không chấm điểm, không xếp hạng.

## 6. Cách triển khai và giọng văn (Instructions mục 4, 5; Knowledge 7, 8.1, 8.3, 8.4)

- Câu trả lời chính trong 2-3 đoạn đầu. Mở bài 2-4 câu, có từ khóa chính, không giới thiệu chung về LED hay công ty, không mở bằng định nghĩa sách giáo khoa.
- Đoạn trả lời nhanh: ngay sau mở bài, 40-60 từ, có con số hoặc tiêu chí kèm điều kiện, đọc tách riêng vẫn hiểu. Theo loại truy vấn: "là gì" thì 1-2 câu định nghĩa; "bao nhiêu" thì số kèm điều kiện; "giá" thì khoảng giá kèm ngày; "cách chọn" thì 3-5 tiêu chí gạch đầu dòng; "so sánh" thì "Chọn A khi..., chọn B khi...". Không mở bằng "Câu trả lời là", không lặp H1, không "tùy nhu cầu" mà không nói tùy gì.
- Phương án phù hợp nhất với trường hợp phổ biến đưa trước. Đoạn 2-4 câu. Bảng khi so sánh từ 3 tiêu chí, tối đa 5 cột.
- Kết bài: khuyến nghị theo từng trường hợp, 2-4 câu, không tóm tắt lại bài. CTA sau kết bài, 1-2 câu, nói khách gửi gì và nhận gì, chỉ nhắc dịch vụ ở mục 2.
- Giọng chuyên gia 7-10 năm, tiếng Việt đơn giản, xưng "chúng tôi" hoặc "HLB", gọi "bạn". Bài lắp đặt có lưu ý an toàn đúng ở bước có rủi ro.
- Thuật ngữ: quang thông (lm), độ rọi (lux), hiệu suất chiếu sáng (lm/W), chỉ số hoàn màu (Ra), hệ số công suất (PF), cấp bảo vệ IP, driver (bộ nguồn), góc chiếu, chiếu sáng phủ đều, chiếu sáng mạnh. "Highbay", "UFO" chỉ khi nói kiểu dáng. Thuật ngữ kỹ thuật giải thích ngắn ở lần đầu.
- Cấm (script bắt phần lớn): em dash, en dash, emoji, từ tuyệt đối, cụm văn mẫu AI, câu nối "Điều này", "Ngoài ra", "Bên cạnh đó", "Việc...", "Không chỉ... mà còn" quá 1-2 lần mỗi kiểu.
- Số: 1.000 m², 0,95, 100W, 6500K, IP54, 130 lm/W, 300 lux, 6-8 m, 1.599.000 đồng.

## 7. SEO và đầu ra (Knowledge mục 9, 10)

- Từ khóa chính ở SEO title, H1, 100 chữ đầu, ít nhất một H2, meta, slug. Từ khóa phụ tối đa 5, đặt tự nhiên.
- Một H1, không nhảy cấp, H4 chỉ khi H3 có từ 2 ý con, heading cụ thể.
- Link nội bộ 3-5 (1-3 về danh mục), link ngoài 0-3 tới nguồn có thẩm quyền. Anchor mô tả đúng trang đích, đặt trong câu có ngữ cảnh, một URL một lần. URL chưa kiểm tra dùng `[LINK: ...]`.
- SEO title dưới 60 ký tự; meta 120-160 ký tự; slug không dấu, 3-6 từ, không năm; excerpt dưới 200 ký tự, không trùng meta; tag 3-5.
- Ảnh: `[ẢNH: chú thích | alt | tên file]`, alt dưới 125 ký tự, tên file .jpg không trùng slug bài hoặc slug đã có trên website, mô tả khớp đoạn chứa ảnh.
- FAQ 3-5 câu, trước kết bài, mỗi câu trả lời 40-80 từ, trả lời thẳng ở câu đầu, không lặp thân bài.
- Phần C: placeholder còn lại kèm vị trí, nguồn (URL, ngày), link chưa xác minh, đề xuất link từ bài cũ, ảnh, schema, chênh lệch trên website, điểm cần người dùng quyết, (bài viết lại) ý bài gốc đã bỏ và lý do.
