# Trạng thái Điều phối HLB (bàn giao cho lượt chạy phiên riêng)

Cập nhật: 30/10/2026 16:27 giờ VN. Mỗi lượt chạy đọc file này sau `DIEU_PHOI.md`. Lượt nào đổi trạng thái lớn (bài mới ĐẠT, người dùng chốt quyết định mới) thì sửa file này và commit.

## Cách chạy từ 28/10/2026

- **Không trả lời trong chat (người dùng chốt 29/10/2026):** lượt Điều phối và mọi sub agent không nhắn, không báo kết quả trong chat project hay thread. Mọi hoạt động, kết quả, câu hỏi chỉ ghi lên Bảng điều phối (`tien_do`, `ly_do` + `can_xu_ly`, `cau_hoi`, `lich_su`, `cau_hinh/chung.moi_truong`). Chỉ nhắn chat khi có lỗi hệ thống cần người dùng sửa (ví dụ thiếu biến môi trường, mất quyền GitHub, bảng không ghi được). Phiên chạy trong thread mà bắt buộc kết thúc bằng một công cụ chat thì dùng `no_reply_needed`, không `post_message`.
- Lịch "Điều phối HLB" chạy **mỗi lượt một phiên mới** (người dùng chốt 28/10, lý do: chạy chung thread chat thì lỡ lệnh và tốn giới hạn sử dụng). Phiên mới không nhắn được vào thread chat: mọi báo cáo cho người dùng ghi lên Bảng điều phối (`tien_do`, `ly_do` + `can_xu_ly`, `cau_hoi`, `cau_hinh/chung.moi_truong`).
- Bảng: https://claude.ai/artifact/3wRDGsubs7s2Kb75vpypmG. Nút "Chạy Agent ngay" gọi lịch theo `cau_hinh/chung.trigger_id`.
- Phiên chạy trong environment "HLB Agent" (có `WP_USER`, `WP_APP_PASSWORD`, mạng tới website). Thiếu `SERPAPI_KEY` thì không dừng cả lượt: chuyển từ khóa cần SERP sang `can_xu_ly` với `ly_do` "Phiên chạy thiếu SERPAPI_KEY, bạn thêm key vào environment HLB Agent" và làm tiếp việc khác.
- Giờ ghi lên bảng luôn lấy bằng `TZ=UTC-7 date -Iseconds` ngay trước khi ghi (người dùng bắt lỗi giờ ước lượng 28/10).
- Mỗi lượt có việc: ghi `agent_nhan_luc` + `tien_do` cho mọi dòng chờ Agent trước (DIEU_PHOI mục 4 bước 3a). Bảng sáng lại nút sau 10 phút (gọi ngay) hoặc 65 phút (gọi không được) nếu chưa xác nhận.
- Chỉ một phiên ghi lên một từ khóa tại một thời điểm (`khoa_luc`).
- Lịch hiện dùng: "Điều phối HLB (phiên riêng)" `trig_01WH9a4VRDCSW6az6Hofrcvd` (tạo 31/10 với prompt mới, PR #36). **Chỉ chạy khi có việc** (người dùng chốt 28/10, bớt tốn token): bảng gọi khi người dùng thao tác, lượt còn việc tự gọi lượt sau, một lượt dự phòng 8:04 sáng. **Từ 31/10 lượt 8:04 chỉ làm khi còn việc dở** (người dùng chốt): lượt nào có việc thì ghi dấu `cau_hinh/chung.dang_do` trước mỗi bước, xóa khi xong; lượt sau thấy dấu cũ hơn 1 giờ thì làm tiếp, không có dấu và mọi từ khóa tạm dừng hoặc chờ người dùng thì dừng ngay, không lấy repo (DIEU_PHOI mục 4 bước 1a). Lịch cũ `trig_01VuSkTwAngCyM4hvdkjoi8u` (28/10, prompt cũ) và `trig_01SNtA1v6Q62TrgSaCBvidMU` đã tắt; lịch hằng giờ `trig_01SZCoQZmxvcGUWbHodVv2Fx` đã xóa.
- **Mô hình phòng ban (người dùng chốt 28/10):** phiên điều phối là trưởng phòng, không tự viết bài. Nghiên cứu, viết, sửa giao `agent-blog` hoặc `agent-danh-muc`; chấm giao `danh-gia-noi-dung`, `danh-gia-danh-muc`; ảnh giao `tao-anh`. Chi tiết `DIEU_PHOI.md` đầu file.

## Quyết định cốt lõi đã chốt

- Thương hiệu "Đèn LED Nhà Xưởng HLB", thuộc Cty TNHH Công nghệ và Xúc tiến Thương mại HALEDCO (HALEDCO từ 2011, HLB từ 2018). HALEDCO là đơn vị sản xuất và phân phối. HLB phân phối đèn LED nhiều thương hiệu: HALEDCO, Philips, Rạng Đông, Điện Quang. Dòng cao cấp gọi "dòng đèn cao cấp HLB phân phối", không gán cho một hãng.
- Không link haledco.com. Không bịa thông số; thiếu thì `[CẦN BỔ SUNG]`. Quá 5 chỗ ở phần B thì không đăng nháp.
- Bảo hành: dòng cao cấp HLB phân phối và HALEDCO 2 năm; Rạng Đông, Điện Quang 24 tháng; Philips tra theo model. Đổi trả theo nhu cầu 15 ngày, phí 10%. Miễn phí giao đơn trên 5 triệu trong 10 km tính từ Xuân Đỉnh. Chiết khấu: nhắc có, không nêu mức.
- Hotline/Zalo 0967569588; kỹ thuật, bảo hành 02437 918 122; email denlednhaxuongcaocap@gmail.com.
- UF và MF giả định khoảng 0,8 (xưởng bụi lấy MF thấp hơn).
- Một dòng từ khóa = một bài; từ đầu dòng là từ khóa chính, không tự đổi.
- Bài ĐẠT thì tự đẩy bản nháp WordPress (chỉ nháp, không đăng công khai). Ghi lên danh mục chỉ khi người dùng bấm "Duyệt, cập nhật lên danh mục".
- Tên file ảnh không trùng slug bài hay slug đã có trên website.
- Repo `haledcoai/hlb-agent` nhánh `main` là bản gốc; thread được tự merge PR.

## Trạng thái từ khóa trên bảng (28/10 14:05)

5 từ khóa đầu đang `tam_dung` do người dùng bấm. Lượt chạy bỏ qua cho tới khi người dùng bấm Tiếp tục.

| Từ khóa | Dừng ở | File, ghi chú |
|---|---|---|
| cách chọn đèn LED nhà xưởng | `cho_duyet_bai` | `Bai_cach-chon-den-led-nha-xuong.md`, nháp WP 8514, vòng 3 = 99 ĐẠT. Người dùng nói bỏ qua nháp này (27/10) |
| mẫu nhà xưởng 200m2 | `cho_duyet_bai` | `Bai_mau-nha-xuong-200m2.md`, nháp WP 8524, vòng 2 = 99 ĐẠT. Người dùng nói bỏ qua nháp này (27/10) |
| đèn chống cháy nổ 20w | `can_xu_ly` | Danh mục. Website chưa có danh mục đèn chống cháy nổ: chờ người dùng tạo (đề xuất `den-chong-chay-no` / `den-chong-chay-no-20w`) và gửi link |
| đèn chống cháy nổ 40w | `cho_duyet_outline` | Blog (người dùng chọn). `nghien_cuu/Bai_den-chong-chay-no-40w/`. SERP 9/9 là trang sản phẩm. Câu hỏi: cập nhật bài 7308 thay vì viết mới? HLB có báo giá đèn chống cháy nổ? model 40W? |
| đèn led chống cháy nổ 50w | `cho_duyet_outline` | Blog. `nghien_cuu/Bai_den-led-chong-chay-no-50w/`. Trùng một phần bài 3821; đề xuất gộp với 40W; hỏi bài 3821 (HLEP4-50W, giá 1,55-3,05 triệu) còn đúng không |
| đèn led chống cháy nổ 100w | `can_xu_ly` (quay về `moi`) | Blog Toplist (người dùng muốn). `nghien_cuu/Bai_den-led-chong-chay-no-100w/`, outline đã lập. Trùng bài 3874 (cùng slug): đề xuất viết lại 3874, chờ 9 câu trả lời (hãng HLB phân phối, nguồn thông số 6 mẫu, giá HLEP). Website có bài đúng từ khóa 20W 4069, 40W 4077, 50W 4082: outline 40W, 50W cần tính lại |
| đèn chống cháy nổ 0.6m (nạp 30/10) | `can_xu_ly` (quay về `moi`) | Danh mục (người dùng chọn). `danh_muc.py tim` không khớp: website chưa có danh mục đèn chống cháy nổ. Chờ người dùng tạo (đề xuất cha `den-chong-chay-no`, con `den-chong-chay-no-0-6m`) và gửi link |
| đèn chống cháy nổ 1m2 (nạp 29/10) | `cho_duyet_anh` | `Bai_den-chong-chay-no-1m2.md`, viết lại bài 3904, nháp WP **8546**. 30/10: mạng mở 7 tên miền hãng (signify.com vẫn chặn), Agent Blog bổ sung dữ liệu HALEDCO, Rạng Đông, Duhal, Paragon, Athaco; vòng 3 = 93 CẦN SỬA, vòng 4 = 97 ĐẠT (tổng 95). Phần B còn 3 [CẦN BỔ SUNG]. Chờ người dùng: Điện Quang (không có model chống nổ, khuyến nghị bỏ), nguồn Philips, mở trang tiêu chuẩn cho IEC 60079. Còn 2 điểm nên sửa nhỏ (Paragon CT5/IP, "Ra 82") làm cùng lần sửa sau. 30/10 14:48 người dùng bấm Duyệt bài; 15:01 đủ 15/15 ảnh (4 ảnh bài cũ, 11 hình vẽ), đã lên tab Kiểm duyệt hình ảnh, từ khóa ở `cho_duyet_anh` |
| đèn chống cháy nổ 250w (nạp 30/10) | `can_xu_ly` (quay về `moi`) | SERP 8/8 trang bán hàng. Trùng bài **4098** cùng slug `den-chong-chay-no-250w`: đề xuất viết lại 4098, rút gọn mục 250W bài 3821. `nghien_cuu/Bai_den-chong-chay-no-250w/serp_bao_cao.md`. Chờ 5 câu trả lời ở `cau_hoi` |
| đèn pha chống cháy nổ (nạp 30/10) | `can_xu_ly` (quay về `moi`) | Không khớp danh mục. SERP 6/8 trang bán hàng. Trùng bài **4018** cùng slug `den-pha-chong-chay-no`: đề xuất viết lại 4018 (`Bai_den-pha-chong-chay-no.md`). `nghien_cuu/Bai_den-pha-chong-chay-no/serp_bao_cao.md`. Chờ 5 câu trả lời. SerpApi trả cache sai lần đầu, phải gọi lại `no_cache=true` (nên thêm vào `nghien_cuu.py`) |

## Việc còn chờ người dùng

- Bảng hỏi thông tin cố định: nhóm 2 còn chờ (lỗi NSX có mất phí, ai chịu ship/tháo lắp bảo hành); nhóm 3-8 chưa trả lời. Rà soát Knowledge 27/10 ở `/mnt/project-files/ra-soat/ra_soat_knowledge_2710.md`.
- Phát hiện website cần người dùng sửa: BUFO1-200, BUFO3-200 ghi IP40; 4 model 150W hãng khác chung 16.500 lm; Philips ghi chung "BH 24 tháng"; trang bảo hành thiếu số ngày đổi trả; danh mục Điện Quang 150W trống.
- Agent Danh mục (PR #16) chưa chạy thử với danh mục thật.

## Lịch sử thay đổi bảng gần đây

- PR #26: Agent xác nhận nhận việc, nút Chạy Agent ngay mờ khi đã giao, nút cố định vị trí.
- PR #27: nạp trùng từ khóa thì mở sẵn từ khóa cũ; "Tất cả" gồm cả tạm dừng.
- PR #28: gọi ngay mà 10 phút chưa xác nhận thì nút sáng lại.
- PR #29: giờ ghi lên bảng lấy giờ thật.
