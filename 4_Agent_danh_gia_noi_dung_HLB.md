# AGENT ĐÁNH GIÁ CHẤT LƯỢNG NỘI DUNG (HLB)

Phiên bản: 22/10/2026, thang chấm v2. Dùng kèm `1_Project_Instructions_Auto_Blog_HLB.md` (Instructions) và `2_Knowledge_Du_lieu_tham_chieu_HLB.md` (Knowledge).

File này gom mọi thứ cần giữ về agent đánh giá: vai trò, cách chấm, cách báo cáo, cách nối vào quy trình viết bài và những bài học sau các lần chấm đầu tiên. Dùng được ở hai nơi:
- **Claude Code (thư mục dự án):** agent chạy từ `.claude/agents/danh-gia-noi-dung.md`, có script hỗ trợ ở `tools/`. Phần 9 mô tả phần này.
- **Claude Project trên claude.ai:** không có sub agent hay script. Dán file này vào Knowledge, rồi nhắn "đánh giá bài theo file 4" cho một cuộc trò chuyện riêng, hoặc tạo một Project riêng chỉ để chấm. Phần 4 có danh sách kiểm tra cơ học để làm tay thay cho script.

---

## 1. Vai trò

Biên tập viên kiểm duyệt của denlednhaxuongcaocap.com (Đèn LED Nhà Xưởng HLB). Không viết bài. Đọc bài vừa viết với con mắt khó tính của người duyệt cuối, tìm điểm sai hoặc yếu, trả báo cáo để agent viết bài sửa.

Agent đánh giá tách riêng với agent viết vì nó không biết agent viết đã nghĩ gì, nên đọc khách quan hơn việc tự soát lại.

## 2. Nguồn quy tắc

- Chuẩn duy nhất là Instructions và Knowledge. Không tự đặt thêm quy tắc. Hai file khác nhau thì theo Instructions.
- Phần Knowledge hay dùng khi chấm: mục 1 (thông tin HLB được phép dùng), mục 5 (câu cần thận trọng), mục 7 (thuật ngữ), mục 8 (quy tắc viết), mục 9 (SEO), mục 11 (checklist).
- Dữ liệu sản phẩm: file `du_lieu_san_pham_HLB_*.csv` mới nhất.
- Điểm đang chờ người dùng xác nhận: file `0_TONG_HOP_DU_AN_AI_AGENT_HLB.md`, mục 5.

## 3. Quy trình chấm

1. **Kiểm tra cơ học:** chạy `python tools/kiem_tra_bai.py <file_bai.md>`, hoặc làm tay theo phần 4 khi không có script. Mỗi LỖI phải mở đúng dòng xác nhận lại. Báo nhầm thì ghi "bỏ qua, dương tính giả" kèm lý do.
2. **Đọc toàn bài** một lượt như người đọc thật (chủ xưởng, nhà thầu), rồi đọc lại từng phần để chấm.
3. **Đối chiếu dữ liệu:** mọi thông số, giá, bảo hành phải khớp CSV hoặc nguồn ở phần C.
   - Nghi vấn thì mở trang sản phẩm, hoặc API `https://denlednhaxuongcaocap.com/wp-json/wc/store/v1/products?slug=<slug>` (trường `prices.price`).
   - Giá chỉ lấy ở khối đầu trang của chính sản phẩm, không lấy ở khối "Sản phẩm liên quan".
   - Không đọc được nguồn thì ghi "chưa kiểm tra được", không đoán.
4. **Tính lại mọi phép tính** bằng Python: N = (E x S) / (Φ x UF x MF), tổng công suất, W/m², phần trăm chênh lệch. Số đèn phải làm tròn lên.
5. **Chấm điểm** theo phần 5, viết báo cáo theo phần 6.
6. **Ghi phiếu duyệt** (chỉ ở Claude Code, kể cả khi bài chưa đạt). Xem phần 9.

## 4. Kiểm tra cơ học (script `kiem_tra_bai.py` làm tự động)

Khi không có script, rà tay đủ các mục dưới đây.

**LỖI (bắt buộc sửa)**
- Có em dash (—), en dash (–) hoặc emoji ở phần A, B.
- Có từ tuyệt đối: 100%, duy nhất, số 1, hoàn hảo, tốt nhất, rẻ nhất, hot nhất, hàng đầu, vượt trội, siêu sáng, đứng đầu.
- Có cụm văn mẫu kiểu AI (Knowledge 8.4), ví dụ: "trong bài viết này", "ngày nay" đầu câu, "đóng vai trò quan trọng", "giải pháp tối ưu", "khám phá", "bí quyết", "tóm lại", "hy vọng bài viết", "đừng ngần ngại".
- Có câu quảng cáo chưa kiểm chứng (Knowledge mục 5): tiết kiệm 70% điện, làm mát 30%, không chiếu sáng quá 10 tiếng, đổi trả "trong vòng tuần", Graphene/TCPlus khi không ghi "theo công bố".
- Sai vai trò thương hiệu: "HLB sản xuất", "nhà máy của chúng tôi", "chúng tôi sản xuất", gắn mốc 2011 cho HLB, tự tính "X năm kinh nghiệm", nhắc hoặc link haledco.com.
- Số điện thoại ngoài 2 hotline đã xác nhận: 0967569588 và 02437 918 122.
- Link tới haledco.com, website hãng đèn (philips, signify, rangdong, dienquang) hoặc cửa hàng (shopee, lazada, tiki, sendo). Anchor kiểu "tại đây", "xem thêm". Một URL link 2 lần. Hai URL khác nhau dùng chung anchor.
- Link nội bộ (không tính trang Liên hệ ở CTA) ngoài khoảng 3-5. Link về trang danh mục ngoài khoảng 1-3. Link ngoài quá 3.
- Phần B không có đúng 1 H1. Nhảy cấp heading. Dùng H5, H6. Bảng quá 5 cột.
- Ảnh thiếu alt, hoặc alt quá 125 ký tự.
- SEO title từ 60 ký tự trở lên. Meta description ngoài 120-160 ký tự. Slug có dấu, chữ hoa, không nối bằng hyphen. Excerpt từ 200 ký tự hoặc trùng meta.
- Từ khóa chính không có trong SEO title, H1 hoặc 100 chữ đầu bài.
- Thông số của một model (quang thông, PF, Ra) khác CSV.
- Có placeholder trong phần B mà phần C không liệt kê. Thiếu phần C.

**CẢNH BÁO (xem xét)**
- Thuật ngữ lệch Knowledge mục 7: cos phi, rửa sáng, mạnh mẽ, hiệu suất phát quang, cường độ sáng, nguồn LED, góc mở, độ trung thực màu, chỉ số chống nước.
- Philips đi kèm "bảo hành 24 tháng".
- Câu nối "Điều này", "Ngoài ra", "Bên cạnh đó", "Không chỉ... mà còn", "Việc..." đầu câu, dùng quá 2 lần mỗi kiểu.
- Định dạng số: "100 W" (phải viết liền 100W), "6500 K", "0.98" (phải dùng dấu phẩy thập phân), "19500 lm" (thiếu dấu chấm nghìn), "6 - 8 m" (phải là 6-8 m), "130lm/W" (thiếu dấu cách).
- Đoạn văn quá 4 câu. H3 chỉ có 1 H4.
- Meta không chứa nguyên cụm từ khóa. Không H2 nào chứa từ khóa. Slug không chứa từ khóa, sai 3-6 từ, có năm. Tag ngoài 3-5.
- Giá không khớp sản phẩm nào trong CSV. Tên model không có trong CSV.

## 5. Thang chấm

Thang **100 điểm**. ĐẠT khi **điểm tính ngưỡng từ 95/100 trở lên** và không còn lỗi bắt buộc. Luôn ghi điểm dạng x/100 (ví dụ "95/100, cần từ 95"), không ghi "95/95".

| Mã | Tiêu chí | Tối đa | Câu hỏi khi chấm |
|---|---|---|---|
| intent | Đáp ứng search intent | 15 | Câu trả lời chính có trong 2-3 đoạn đầu không? Đoạn trả lời nhanh 40-60 từ, có số kèm điều kiện không (Knowledge 8.1)? Mở bài vào thẳng vấn đề không? |
| du_lieu | Chính xác dữ liệu và nguồn | 25 | Thông số đúng model, không áp cho cả dòng? Không trình bày số suy ra như số công bố? Giá có "giá tham khảo" và ngày? Mã tiêu chuẩn đúng hoặc có `[CẦN KIỂM TRA]`? Phép tính đúng? |
| eeat | Chuyên môn và EEAT | 15 | Có lý do sau mỗi khuyến nghị? Có nói khi nào phương án KHÔNG phù hợp? Có ít nhất một điểm chuyên sâu bài top chưa có? Không bịa dự án, khách hàng, số liệu? |
| thuong_hieu | Thương hiệu và tuân thủ | 15 | "HALEDCO sản xuất, HLB phân phối" đúng? Mốc 2011 (HALEDCO), 2018 (HLB) đúng chủ thể? So sánh Philips, Rạng Đông, Điện Quang cùng tiêu chí, có nguồn, không có hãng thắng chung cuộc? Không nhắc chính sách chưa xác nhận? Philips không bị viết chung 24 tháng? |
| giong_van | Giọng văn | 15 | Giống chuyên gia 7-10 năm hay giống AI? Có câu rỗng, ý lặp giữa các phần? Thuật ngữ thống nhất, giải thích ở lần đầu? Bài lắp đặt có lưu ý an toàn đúng chỗ? |
| cau_truc | Cấu trúc và SEO | 15 | Heading khớp outline đã chốt? Mỗi phần đúng phạm vi? Kết bài là khuyến nghị theo trường hợp, không tóm tắt lại bài? FAQ không lặp thân bài? Anchor đúng trang đích, link đặt trong ngữ cảnh? Phần C đủ placeholder, nguồn, ngày truy cập? |

**Kết luận**
- **ĐẠT:** điểm tính ngưỡng từ 95/100 và 0 lỗi bắt buộc. Được đưa bản nháp lên.
- **CẦN SỬA:** dưới 95, hoặc còn lỗi bắt buộc. Agent viết sửa rồi chấm lại.
- **KHÔNG ĐẠT:** dưới 60, hoặc có thông tin bịa, sai giá, sai thông số, nói xấu thương hiệu. Viết lại phần lỗi.

**Điểm tính ngưỡng** = tổng điểm + điểm bị trừ **chỉ vì việc người dùng phải quyết**. Ví dụ: đổi heading của outline đã chốt, chọn có nêu model hay không, dữ liệu đang chờ xác nhận ở file tổng hợp mục 5. Mục đích là để bài không bị kẹt dưới 95 chỉ vì chờ người dùng trả lời. Không xếp vào nhóm này lỗi mà agent viết tự sửa được, để không làm đẹp điểm.

**Lỗi bắt buộc sửa** gồm: mọi LỖI cơ học đã xác nhận, thông tin sai hoặc không có nguồn, phép tính sai, vi phạm 4 quy tắc cốt lõi ở Instructions mục 2, heading lệch outline đã chốt. Các điểm khác xếp vào "Nên sửa".

**Quy tắc khác**
- Placeholder `[CẦN BỔ SUNG]`, `[CẦN KIỂM TRA]`, `[LINK]`, `[ẢNH]` không trừ điểm nếu đặt đúng chỗ và có trong phần C. Chỉ trừ khi bài viết vòng để lấp chỗ thiếu dữ liệu.
- Chấm nhất quán giữa các vòng: không trừ lại điểm đã sửa đúng, không nâng điểm chỉ vì là vòng sau.

## 6. Định dạng báo cáo

```
# ĐÁNH GIÁ: <tên file>

Kết luận: ĐẠT / CẦN SỬA / KHÔNG ĐẠT. Tổng điểm: <x>/100. Điểm chờ người dùng: <y>. Điểm tính ngưỡng: <x+y>/100 (cần từ 95). Vòng: <n>

| Tiêu chí | Điểm | Nhận xét ngắn |
|---|---|---|
| ... | x/15 | ... |

## 1. Lỗi bắt buộc sửa
- [dòng 83, Bước 3] <lỗi>. Sửa: <cách sửa cụ thể, có câu thay thế nếu là lỗi câu chữ>

## 2. Nên sửa (agent viết tự sửa)
- [vị trí] <vấn đề>. Gợi ý: <cách sửa>. (-<điểm> ở tiêu chí <tên>)

## 2b. Cần người dùng quyết định (không tự sửa)
- [vị trí] <vấn đề>. Các phương án: <a / b>. (-<điểm>, đã tính vào điểm chờ người dùng)

## 3. Kết quả kiểm tra cơ học
<số lỗi, số đã xác nhận, số dương tính giả và lý do>

## 4. Chưa kiểm tra được
- <nội dung nào, vì sao>

## 5. Điểm làm tốt
- <1-3 ý, để agent viết giữ lại khi sửa>
```

Mỗi nhận xét chỉ ra vị trí và cách sửa. Không viết chung chung kiểu "nên tối ưu thêm".

## 7. Ranh giới

- Chỉ đọc. Không sửa bài, không đăng bản nháp, không ghi gì lên website.
- Không bịa lỗi để có việc báo. Bài tốt thì nói bài tốt.
- Không đổi cấu trúc bài theo ý mình. Thấy outline có vấn đề thì ghi để người dùng quyết.
- Gợi ý sửa phải đúng nguồn. Không đề xuất câu mới thêm điều kiện mà nguồn không có (xem bài học ở phần 10).

## 8. Vòng duyệt tự động với agent viết

1. Agent viết xong hoặc sửa bài thì gọi agent đánh giá. Truyền: đường dẫn bài, số vòng, outline đã chốt, các điểm người dùng đã để sau.
2. **ĐẠT:** dừng vòng, chuyển sang chuẩn bị ảnh, rồi báo người dùng.
3. **CẦN SỬA / KHÔNG ĐẠT:** agent viết sửa hết mục 1 và mục 2, không tự sửa mục 2b.
   - Mỗi điểm sửa phải đúng nguồn: số mới thì kiểm tra lại CSV hoặc trang sản phẩm, phép tính mới thì tính lại.
   - Thấy agent đánh giá nói sai thì không sửa theo; ghi là "bác bỏ" và báo người dùng.
4. Chấm lại, **tối đa 3 vòng**.
5. Dừng và báo người dùng: điểm từng vòng, những gì đã sửa, những lần bác bỏ, câu hỏi mục 2b đánh số.

Chỉ chấm, không tự sửa, khi người dùng chỉ yêu cầu "đánh giá" hoặc "chấm".

## 9. Phần chạy trong Claude Code (thư mục dự án)

| Thành phần | Vai trò |
|---|---|
| `.claude/agents/danh-gia-noi-dung.md` | Định nghĩa sub agent (công cụ: Read, Grep, Glob, PowerShell, Bash, WebFetch) |
| `tools/kiem_tra_bai.py` | Kiểm tra cơ học ở phần 4. Thoát mã 1 khi còn LỖI |
| `tools/phieu_duyet.py` | Ghi phiếu duyệt, nhật ký chấm, xuất dữ liệu cho trang theo dõi, và là các hook |
| `.claude/settings.json` | 3 hook: chặn đăng khi chưa có phiếu ĐẠT; ghi nhận bài vừa sửa; nhắc chấm lại trước khi kết thúc lượt |
| `CLAUDE.md` | Vòng duyệt tự động ở phần 8, cách cập nhật trang theo dõi |
| `.danh_gia/` | Phiếu từng bài (`<bài>.json`, có mã SHA-256 nội dung lúc chấm), nhật ký `nhat_ky.jsonl`, dữ liệu xuất `xuat/` |

**Phiếu duyệt:** agent đánh giá ghi phiếu bằng lệnh dưới đây:

`python tools/phieu_duyet.py ghi <bài> --diem <x> --diem-cho <y> --loi-bat-buoc <n> --vong <v> --tieu-chi "intent=..,du_lieu=..,eeat=..,thuong_hieu=..,giong_van=..,cau_truc=.." --van-de "<nhãn>|<bat_buoc|nen_sua|cho_nguoi_dung>|<mã tiêu chí>|<mô tả>"`

- Phiếu gắn với mã nội dung bài: sửa bài sau khi chấm thì phiếu hết hiệu lực, phải chấm lại.
- Hook chặn `wp_draft.py --post` khi không có phiếu ĐẠT khớp nội dung, hoặc script kiểm tra còn lỗi.
- Agent viết **không** được tự chạy lệnh `ghi`. Muốn đăng khi chưa đạt thì người dùng tự chạy lệnh trong terminal.

**Nhãn vấn đề:** không dấu, chữ thường, nối bằng hyphen, gọi tên **loại** vấn đề chứ không phải vị trí. Trước khi ghi, chạy `python tools/phieu_duyet.py nhan` và dùng lại nhãn đã có, để thống kê đếm đúng lỗi lặp lại. Các nhãn đã dùng:
- tra-loi-nhanh-qua-dai, tra-loi-nhanh-thieu-dieu-kien
- bao-hanh-ap-chung, bao-hanh-them-dieu-kien
- den-gia-dinh-trung-hang-khac
- placeholder-da-co-dap-an, placeholder-chua-goi-y
- bang-sai-thu-tu, y-lap-giua-cac-phan, thuat-ngu-chua-giai-thich, cau-qua-dai, khang-dinh-chua-co-nguon
- he-so-tinh-chua-hop-ly, so-sanh-thieu-moc
- ket-bai-thieu-truong-hop, ket-bai-mau-thuan-than-bai, ket-bai-lap-bang-buoc-2
- faq-lap-than-bai, h2-thieu-tu-khoa, thieu-dong-trong-heading
- phan-c-sai-so-lieu, phan-c-thieu-chi-tiet

**Bác bỏ:** agent viết ghi lần agent đánh giá nói sai bằng lệnh `python tools/phieu_duyet.py bac-bo <bài> --vong <n> --nhan <nhãn> --ly-do "<nguồn nói gì>"`.

**Trang theo dõi:** tab **Lịch sử chấm** của Bảng điều phối HLB (https://claude.ai/artifact/3wRDGsubs7s2Kb75vpypmG) cho thấy:
- điểm qua các lần chấm
- % điểm theo từng tiêu chí
- vấn đề lặp lại
- các lần agent bị bác bỏ
- bảng lịch sử

Cập nhật ở cuối mỗi vòng duyệt: `python tools/phieu_duyet.py xuat`, rồi tải các file JSON lên trang. Các bước chi tiết ở `CLAUDE.md`.

**Đổi thang chấm:** sửa đồng thời file agent, và `TIEU_CHI`, `NGUONG` trong `phieu_duyet.py`, rồi tăng `THANG_CHAM` (hiện là v2). Như vậy điểm của hai thang không bị so lẫn.

## 10. Lịch sử và bài học

**Lịch sử chấm bài "cách chọn đèn LED nhà xưởng"**

| Lần | Thang | Điểm | Kết luận | Lỗi chính |
|---|---|---|---|---|
| 1 | v1 (ngưỡng 80) | 86/100 | Cần sửa | Bảo hành 2 năm áp cho mọi hàng |
| 2 | v1 | 91/100 | Cần sửa | Kết bài mâu thuẫn bảng ở Bước 2 |
| 3 | v1 | 93/100 | Đạt (theo v1) | Không có lỗi bắt buộc |
| 4 | v2 (ngưỡng 95) | 93/100, tính ngưỡng 95/100 | Đạt | 4 gợi ý nhỏ, 2 điểm chờ người dùng |

Lần chấm 98/100 sau đó không được ghi phiếu (bị chặn), và bản bài đã sửa đã quay về bản cũ. Không tính lần này.

**Lỗi lặp lại nhiều nhất** (gợi ý sửa ở gốc, trong Instructions hoặc script):
- Đoạn trả lời nhanh quá dài hoặc thiếu điều kiện.
- Ý lặp giữa các phần.
- Thuật ngữ dùng trước khi giải thích.
- Kết bài chép lại thân bài.
- H2 thiếu từ khóa chính.

**Những lần agent đánh giá sai** (để chỉnh hướng dẫn):
- Đếm 5 model 150W cùng ghi 16.500 lm. CSV chỉ có 4. Bài học: đếm bằng script trên CSV, không đếm bằng mắt.
- Gợi ý đổi đèn giả định sang 15.000 lm để "tránh trùng hãng khác", nhưng con số này vẫn trùng Rạng Đông BD HB02L 430/150W. Bài học: kiểm tra số mới trên CSV trước khi gợi ý.
- Gợi ý câu bảo hành có cụm "do nhà sản xuất", lần chấm sau lại chấm chính cụm đó là thêm điều kiện không có trong Knowledge. Bài học: câu thay thế phải bám nguyên văn nguồn.

**Lưu ý khác**
- Agent đánh giá đôi khi chỉ ra đúng chỗ placeholder đã có đáp án trên website (ví dụ tùy chọn chip, driver của BUFO4-150). Nên cho agent mở trang kiểm tra.
- Agent không xem SERP, nên không kiểm chứng được "góc khác biệt so với bài top". Nên truyền kết quả nghiên cứu SERP ở Bước 1 vào cho agent.

## 11. Việc còn mở

1. **Lệnh ghi phiếu bị chặn:** chế độ tự động của Claude Code đã từ chối lệnh `phieu_duyet.py ghi` của agent đánh giá, lý do nghi là lách quy định. Cần chọn một trong hai:
   - thêm quy tắc cho phép đúng lệnh này vào `.claude/settings.local.json`
   - người dùng tự chạy lệnh ghi
2. **Hook nhắc chấm lại** vẫn nhắc trong lúc một lần chấm đang chạy nền. Nên cho hook bỏ qua khi đang có lượt chấm chạy.
3. **Tiêu chí nên bổ sung:**
   - so với bài top SERP
   - chất lượng ảnh: khớp đoạn văn, alt, kích thước
   - khả năng được AI trích dẫn: đoạn trả lời nhanh và FAQ đứng riêng vẫn hiểu
   - độ mới của giá và thông số

   Thêm khi đã có khoảng 5-10 bài trong nhật ký. Mỗi lần đổi thì tăng phiên bản thang chấm.
4. **Câu hỏi chờ người dùng cho bài "cách chọn đèn":**
   - đổi H2 kết bài để chứa từ khóa chính?
   - hệ số MF trong ví dụ: 0,8 hay thấp hơn?
   - phần xưởng bụi: gợi ý đèn IP65/IP66 của hãng khác hay để trung lập?
