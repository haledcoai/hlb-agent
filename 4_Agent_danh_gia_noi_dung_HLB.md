# AGENT ĐÁNH GIÁ CHẤT LƯỢNG NỘI DUNG (HLB)

Phiên bản: 27/10/2026, thang chấm v3 (checklist, chấm khắt khe). Dùng kèm `1_Project_Instructions_Auto_Blog_HLB.md` (Instructions) và `2_Knowledge_Du_lieu_tham_chieu_HLB.md` (Knowledge).

File này giữ phần kiểm tra cơ học làm tay, phần chạy trong Claude Code, lịch sử, bài học và việc còn mở của agent đánh giá. Cách chấm nằm ở file agent (xem mục 1-3). Dùng được ở hai nơi:
- **Claude Code (thư mục dự án):** agent chạy từ `.claude/agents/danh-gia-noi-dung.md`, có script hỗ trợ ở `tools/`. Phần 9 mô tả phần này.
- **Claude Project trên claude.ai:** file gọn `5_Agent_danh_gia_ban_claude_ai.md` ngừng cập nhật từ 04/11/2026 (còn thang v2). Muốn chấm trên claude.ai thì tạo lại từ `.claude/agents/danh-gia-noi-dung.md` và `checklist_cham_bai.md`.

---

## 1-3, 4b-8. Vai trò, nguồn quy tắc, quy trình, checklist, thang chấm, báo cáo, ranh giới, vòng duyệt

Không chép lại ở đây (gọn lại 04/11/2026 để không lệch với bản chạy). Nguồn:
- Vai trò, nguồn quy tắc, quy trình chấm, thang 6 tiêu chí (ĐẠT từ 95), mẫu báo cáo, ranh giới: `.claude/agents/danh-gia-noi-dung.md`.
- Checklist từng mục và quy tắc chấm khắt khe: `checklist_cham_bai.md`. Quy tắc rút gọn: `quy_tac_cham.md`.
- Vòng duyệt tự động (chấm, sửa, tối đa 3 vòng, bác bỏ): `CLAUDE.md` mục Vòng duyệt tự động.
- Điểm đang chờ người dùng xác nhận: `0_TONG_HOP_DU_AN_AI_AGENT_HLB.md` mục 5.

## 4. Kiểm tra cơ học (script `kiem_tra_bai.py` làm tự động)

Khi không có script, rà tay đủ các mục dưới đây.

**LỖI (bắt buộc sửa)**
- Có em dash (—), en dash (–) hoặc emoji ở phần A, B.
- Có từ tuyệt đối: 100%, duy nhất, số 1, hoàn hảo, tốt nhất, rẻ nhất, hot nhất, hàng đầu, vượt trội, siêu sáng, đứng đầu.
- Có cụm văn mẫu kiểu AI (Knowledge 8.4), ví dụ: "trong bài viết này", "ngày nay" đầu câu, "đóng vai trò quan trọng", "giải pháp tối ưu", "khám phá", "bí quyết", "tóm lại", "hy vọng bài viết", "đừng ngần ngại".
- Có câu quảng cáo chưa kiểm chứng (Knowledge mục 5): tiết kiệm 70% điện, làm mát 30%, không chiếu sáng quá 10 tiếng, đổi trả "trong vòng tuần", Graphene/TCPlus khi không ghi "theo công bố".
- Sai vai trò thương hiệu: "HLB sản xuất", "HLB lắp ráp", "HLB là nhà sản xuất", "nhà máy, xưởng của chúng tôi", "chúng tôi sản xuất, lắp ráp", "dòng cao cấp" (mọi cách viết, 11/11/2026), gắn mốc 2011 cho HLB, tự tính "X năm kinh nghiệm", nhắc hoặc link haledco.com.
- Số điện thoại ngoài 2 hotline đã xác nhận: 0967569588 và 02437 918 122.
- Link tới haledco.com, website hãng đèn (philips, signify, rangdong, dienquang) hoặc cửa hàng (shopee, lazada, tiki, sendo). Anchor kiểu "tại đây", "xem thêm". Một URL link 2 lần. Hai URL khác nhau dùng chung anchor.
- Link nội bộ (không tính trang Liên hệ ở CTA) ngoài khoảng 3-5. Link về trang danh mục ngoài khoảng 1-3. Link ngoài quá 3.
- Phần B không có đúng 1 H1. Nhảy cấp heading. Dùng H5, H6. Bảng quá 5 cột.
- Ảnh thiếu alt, hoặc alt quá 125 ký tự.
- SEO title hoặc H1 ngoài 55-65 ký tự. Meta description ngoài 150-155 ký tự, từ khóa chính không ở 30 ký tự đầu hoặc lặp quá 2 lần. Câu đầu sapo thiếu từ khóa chính. Slug có dấu, chữ hoa, không nối bằng hyphen. Excerpt từ 200 ký tự hoặc trùng meta.
- Từ khóa chính không có trong SEO title, H1 hoặc 100 chữ đầu bài.
- Thông số của một model (quang thông, PF, Ra) khác CSV.
- Có placeholder trong phần B mà phần C không liệt kê. Thiếu phần C.

**CẢNH BÁO (xem xét)**
- Thuật ngữ lệch Knowledge mục 7: cos phi, rửa sáng, mạnh mẽ, hiệu suất phát quang, cường độ sáng, nguồn LED, góc mở, độ trung thực màu, chỉ số chống nước.
- Philips đi kèm "bảo hành 24 tháng".
- Câu nối "Điều này", "Ngoài ra", "Bên cạnh đó", "Không chỉ... mà còn", "Việc..." đầu câu, dùng quá 2 lần mỗi kiểu.
- Định dạng số: "100 W" (phải viết liền 100W), "6500 K", "0.98" (phải dùng dấu phẩy thập phân), "19500 lm" (thiếu dấu chấm nghìn), "6 - 8 m" (phải là 6-8 m), "130lm/W" (thiếu dấu cách).
- Đoạn văn quá 4 câu. H3 chỉ có 1 H4.
- Trình bày (28/10/2026): sapo ngoài 40-80 từ, câu từ 35 từ, đoạn quá 80 từ, bài không có chỗ in đậm, H2 không có H3 mà thiếu ảnh, kết bài thiếu từ khóa chính hoặc CTA, meta thiếu từ gợi hành động.
- Không H2 nào chứa từ khóa. Slug không chứa từ khóa, sai 3-6 từ, có năm. Tag ngoài 3-5.
- Giá không khớp sản phẩm nào trong CSV. Tên model không có trong CSV.

## 9. Phần chạy trong Claude Code (thư mục dự án)

| Thành phần | Vai trò |
|---|---|
| `.claude/agents/danh-gia-noi-dung.md` | Định nghĩa sub agent (công cụ: Read, Grep, Glob, PowerShell, Bash, WebFetch) |
| `quy_tac_cham.md` | Bản rút gọn quy tắc chấm, có dòng "Mã nguồn" để phát hiện lệch với file gốc |
| `checklist_cham_bai.md` | Checklist 44 mục có mã theo 6 tiêu chí, mức lỗi, quy tắc chấm khắt khe (27/10/2026) |
| `tools/kiem_tra_bai.py` | Kiểm tra cơ học ở phần 4, kiểm đoạn trả lời nhanh 40-60 từ. `--gon` in gọn, `--tra` tra và đếm trên CSV, `--cap-nhat-quy-tac`. Thoát mã 1 khi còn LỖI |
| `tools/phieu_duyet.py` | Ghi phiếu duyệt, nhật ký chấm, xuất dữ liệu cho trang theo dõi, các hook. `lan-truoc`, `khac` để đối chiếu với lần chấm trước |
| `.claude/settings.json` | Cho phép lệnh `phieu_duyet.py ghi`, `nhan` chạy không hỏi. 5 hook: chặn đăng khi chưa có phiếu ĐẠT và chặn ghi phiếu khi không phải agent đánh giá; đánh dấu đang chấm khi gọi agent đánh giá; bỏ đánh dấu khi sub agent kết thúc; ghi nhận bài vừa sửa; nhắc chấm lại trước khi kết thúc lượt (bỏ qua khi đang có lượt chấm) |
| `CLAUDE.md` | Vòng duyệt tự động; cách cập nhật trang theo dõi ở `quy_trinh/nhat_ky_cham_va_bang.md` |
| `.danh_gia/` | Phiếu từng bài (`<bài>.json`, có mã SHA-256 nội dung lúc chấm), bản bài lúc chấm `ban_cham/`, nhật ký `nhat_ky.jsonl`, dữ liệu xuất `xuat/` |

**Phiếu duyệt:** agent đánh giá ghi phiếu bằng lệnh dưới đây:

`python tools/phieu_duyet.py ghi <bài> --che-do du --diem <x> --diem-cho <y> --loi-bat-buoc <n> --vong <v> --tieu-chi "intent=..,du_lieu=..,eeat=..,thuong_hieu=..,giong_van=..,cau_truc=.." --van-de "<nhãn>|<bat_buoc|nen_sua|cho_nguoi_dung>|<mã tiêu chí>|<mô tả>"`

- Phiếu gắn với mã nội dung bài: sửa bài sau khi chấm thì phiếu hết hiệu lực, phải chấm lại.
- Lệnh `ghi` chỉ chạy khi `kiem_tra_bai.py` đã chạy trên đúng nội dung bài trong 2 giờ gần nhất (thêm 24/10/2026, sau hai phiếu ngày 23/10 ghi cách nhau 32 giây mà không có dấu hiệu chấm lại).
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

**Bác bỏ:** trưởng phòng (agent chính) ghi lần agent đánh giá nói sai bằng lệnh `python tools/phieu_duyet.py bac-bo <bài> --vong <n> --nhan <nhãn> --ly-do "<nguồn nói gì>"`.

**Trang theo dõi:** tab **Lịch sử chấm điểm** của Bảng điều phối HLB (https://claude.ai/artifact/57apPM1U3HKFqe2PVvFsXM) cho thấy:
- điểm qua các lần chấm
- % điểm theo từng tiêu chí
- vấn đề lặp lại
- các lần agent bị bác bỏ
- bảng lịch sử

Cập nhật ở cuối mỗi vòng duyệt: `python tools/phieu_duyet.py xuat`, rồi tải các file JSON lên trang. Các bước chi tiết ở `quy_trinh/nhat_ky_cham_va_bang.md`.

**Đổi thang chấm:** sửa đồng thời file agent, và `TIEU_CHI`, `NGUONG` trong `phieu_duyet.py`, rồi tăng `THANG_CHAM` (hiện là v3). Như vậy điểm của hai thang không bị so lẫn.

## 10. Lịch sử và bài học

Các bài viết trước khi hoàn thiện Agent sẽ được chấm lại theo thang v3 (người dùng chốt 27/10/2026). Lịch sử dưới đây là thang cũ, giữ lại để tham khảo bài học.

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

- Lần chấm 24/10 bài 200m2 xếp "bắt buộc sửa" mức 300 lux văn phòng theo QCVN 22:2016/BYT, dựa trên trí nhớ, khi không mở được bản tiêu chuẩn. Bài học: chưa mở được nguồn thì chỉ xếp "nên sửa" kèm `[CẦN KIỂM TRA]`.

**Lưu ý khác**
- Agent đánh giá đôi khi chỉ ra đúng chỗ placeholder đã có đáp án trên website (ví dụ tùy chọn chip, driver của BUFO4-150). Nên cho agent mở trang kiểm tra.
- Agent không xem SERP, nên không kiểm chứng được "góc khác biệt so với bài top". Nên truyền kết quả nghiên cứu SERP ở Bước 1 vào cho agent.

## 11. Việc còn mở

1. **Lệnh ghi phiếu bị chặn:** đã xử lý (23/10/2026). `.claude/settings.json` cho phép đúng lệnh `phieu_duyet.py ghi`, đồng thời hook chỉ cho agent đánh giá (hoặc agent `general-purpose` đang chấm thay theo CLAUDE.md) chạy lệnh này.
2. **Hook nhắc chấm lại khi đang chấm nền:** đã xử lý (23/10/2026). Gọi agent đánh giá thì hook đánh dấu "đang chấm", Stop hook không nhắc cho tới khi sub agent kết thúc hoặc quá 30 phút.
3. **Rút gọn để chạy nhanh, ít token:** đã xử lý (24/10/2026; chế độ kiểm lại vòng 2-3 bỏ ngày 26/10 theo yêu cầu người dùng, luôn chấm đủ): bản quy tắc rút gọn, script đếm và tra CSV, in gọn. Sửa luôn mẫu vai trò thương hiệu theo câu chuẩn 23/10 (trước đó script sót 6/8 câu sai trong bài thử) và bỏ cảnh báo giá cho đơn giá theo m², kWh.
4. **Tiêu chí nên bổ sung:** từ 27/10/2026 checklist đã có mục cho phần lớn ý dưới đây (so với bài top: E3, D10; ảnh: S7; đoạn đứng riêng vẫn hiểu: I3, S8), nhưng chưa có điểm riêng.
   - so với bài top SERP
   - chất lượng ảnh: khớp đoạn văn, alt, kích thước
   - khả năng được AI trích dẫn: đoạn trả lời nhanh và FAQ đứng riêng vẫn hiểu
   - độ mới của giá và thông số

   Tách thành tiêu chí có điểm riêng khi đã có khoảng 5-10 bài chấm theo v3. Mỗi lần đổi thì tăng phiên bản thang chấm.
5. **Câu hỏi chờ người dùng cho bài "cách chọn đèn":** đổi H2 kết bài và MF 0,8 đã chốt 26/10/2026. Còn: phần xưởng bụi gợi ý đèn IP65/IP66 của hãng khác hay để trung lập?
