# Trạng thái Điều phối HLB (bàn giao cho lượt chạy phiên riêng)

Cập nhật: 26/11/2026 giờ VN (đối chiếu bảng trên máy). Mỗi lượt chạy đọc file này sau `DIEU_PHOI.md`. Lượt nào đổi trạng thái lớn (bài mới ĐẠT, người dùng chốt quyết định mới) thì sửa file này và commit.

## Cách chạy từ 28/10/2026

Quy trình mỗi lượt (không nhắn chat, mỗi lượt một phiên mới, giờ lấy bằng lệnh, xác nhận nhận việc, `khoa_luc`, mô hình phòng ban): `DIEU_PHOI.md`. Ở đây chỉ giữ thông tin môi trường và lịch:

- Phiên chạy trong environment "HLB Agent" (có `WP_USER`, `WP_APP_PASSWORD`, mạng tới website). Thiếu `SERPAPI_KEY` thì không dừng cả lượt: chuyển từ khóa cần SERP sang `can_xu_ly` với `ly_do` "Phiên chạy thiếu SERPAPI_KEY, bạn thêm key vào environment HLB Agent" và làm tiếp việc khác.
- Bảng sáng lại nút sau 10 phút (gọi ngay) hoặc 65 phút (gọi không được) nếu chưa xác nhận.
- **09/11/2026 người dùng chốt TẮT lượt dự phòng 8:04** (Agent tạm không cần điều phối tự động, người dùng sẽ tự bật lại khi cần trên claude.ai). Lịch dưới đây đang ở trạng thái tắt; công cụ Claude không bật lại được.
- Lịch hiện dùng: "Điều phối HLB (phiên riêng)" `trig_015wH6yUw1ZwT6sW57KQANC2` (tạo lại 05/11 với prompt bỏ tự gọi lượt sau; lịch 31/10 `trig_01WH9a4VRDCSW6az6Hofrcvd` đã tắt). **Chỉ chạy khi có việc** (người dùng chốt 28/10, bớt tốn token): bảng gọi khi người dùng thao tác và một lượt dự phòng 8:04 sáng. **Từ 05/11 lượt còn việc không tự gọi lượt sau** (người dùng chốt, vì mỗi lượt đăng một dòng vào project chat); việc còn lại để lượt 8:04 hoặc lần người dùng thao tác kế tiếp. **Từ 31/10 lượt 8:04 chỉ làm khi còn việc dở** (người dùng chốt): lượt nào có việc thì ghi dấu `cau_hinh/chung.dang_do` trước mỗi bước, xóa khi xong; lượt sau thấy dấu cũ hơn 1 giờ thì làm tiếp, không có dấu và mọi từ khóa tạm dừng hoặc chờ người dùng thì dừng ngay, không lấy repo (DIEU_PHOI mục 4 bước 1a). Lịch cũ `trig_01VuSkTwAngCyM4hvdkjoi8u` (28/10, prompt cũ) và `trig_01SNtA1v6Q62TrgSaCBvidMU` đã tắt; lịch hằng giờ `trig_01SZCoQZmxvcGUWbHodVv2Fx` đã xóa.

## Quyết định cốt lõi đã chốt

- Thông tin công ty, vai trò HALEDCO và HLB, liên hệ, bảo hành, đổi trả, giao hàng, chiết khấu: `2_Knowledge_Du_lieu_tham_chieu_HLB.md` mục 1, 1.1 (không chép lại ở đây).
- Không link haledco.com. Không bịa thông số; thiếu thì `[CẦN BỔ SUNG]`. Quá 5 chỗ ở phần B thì không đăng nháp.
- UF và MF giả định khoảng 0,8 (xưởng bụi lấy MF thấp hơn).
- Một nhóm từ khóa = một bài (nhóm cách nhau bằng dòng trống); mỗi dòng một từ khóa, dòng đầu là từ khóa chính, không tự đổi.
- Bài ĐẠT thì tự đẩy bản nháp WordPress (chỉ nháp, không đăng công khai). Nội dung danh mục chỉ để ở Trang nháp, Agent không ghi lên danh mục (người dùng chốt 26/11/2026).
- Tên file ảnh không trùng slug bài hay slug đã có trên website.
- Repo `haledcoai/hlb-agent` nhánh `main` là bản gốc; thread được tự merge PR.

## Trạng thái từ khóa trên bảng

**26/11/2026 người dùng chốt: xóa sạch dữ liệu cũ trên bảng mới, từ nay chỉ làm việc mới trên bảng mới.** Bảng mới không còn từ khóa nào. 11 từ khóa dưới đây có dấu `da_xoa/<id>` trên bảng (để `doi_chieu_bang.py` không nạp lại bài lên bảng). File bài, `nghien_cuu/`, `anh/`, `.danh_gia/` trên repo và bản nháp WordPress giữ nguyên. Bảng dưới chỉ để tra lại; muốn làm tiếp từ khóa nào thì người dùng nạp lại trên bảng.

| Từ khóa (lưu trữ) | Dừng ở | File, ghi chú |
|---|---|---|
| cách chọn đèn LED nhà xưởng | `cho_duyet_bai` | `Bai_cach-chon-den-led-nha-xuong.md`, nháp WP 8514, vòng 3 = 99 ĐẠT. Người dùng nói bỏ qua nháp này (27/10) |
| mẫu nhà xưởng 200m2 | `cho_duyet_bai` | `Bai_mau-nha-xuong-200m2.md`, nháp WP 8524, vòng 2 = 99 ĐẠT. Người dùng nói bỏ qua nháp này (27/10) |
| đèn chống cháy nổ 20w | `can_xu_ly` (tạm dừng) | Danh mục. Website chưa có danh mục. Từ 05/11 quy tắc mới: khi người dùng bấm Tiếp tục thì viết với danh mục đề xuất `den-chong-chay-no-20w`, đưa lên Trang nháp |
| đèn chống cháy nổ 40w | `cho_duyet_outline` | Blog (người dùng chọn). `nghien_cuu/Bai_den-chong-chay-no-40w/`. SERP 9/9 là trang sản phẩm. Câu hỏi: cập nhật bài 7308 thay vì viết mới? HLB có báo giá đèn chống cháy nổ? model 40W? |
| đèn led chống cháy nổ 50w | `cho_duyet_outline` | Blog. `nghien_cuu/Bai_den-led-chong-chay-no-50w/`. Trùng một phần bài 3821; đề xuất gộp với 40W; hỏi bài 3821 (HLEP4-50W, giá 1,55-3,05 triệu) còn đúng không |
| đèn led chống cháy nổ 100w | `can_xu_ly` (quay về `moi`) | Blog Toplist (người dùng muốn). `nghien_cuu/Bai_den-led-chong-chay-no-100w/`, outline đã lập. Trùng bài 3874 (cùng slug): đề xuất viết lại 3874, chờ 9 câu trả lời (hãng HLB phân phối, nguồn thông số 6 mẫu, giá HLEP). Website có bài đúng từ khóa 20W 4069, 40W 4077, 50W 4082: outline 40W, 50W cần tính lại |
| đèn chống cháy nổ 0.6m (nạp 30/10) | `san_sang_ap_dung` (26/11 09:45) | Danh mục đề xuất (website chưa có danh mục, chưa có sản phẩm chống cháy nổ), `DM_den-chong-chay-no-0-6m.md`. 25/11 người dùng duyệt outline; vòng 1: 90 CẦN SỬA, vòng 2: 98 ĐẠT. Trang nháp **8549** (chưa ghi lên danh mục, `ap-dung` chờ người dùng tạo danh mục cha `den-chong-chay-no` và con `den-chong-chay-no-0-6m`; URL dự kiến đang 301 sang bài 4147). Phần B còn 3 [CẦN BỔ SUNG] (model, bảng mẫu, giá). Còn 2 điểm nên sửa nhỏ (câu đầu H2 1, giải thích "quang thông") làm cùng lần sửa sau. 25/11 14:51 người dùng bấm "Duyệt, cập nhật lên danh mục" (giữ `duyet_ap_dung_luc`), chưa ghi được vì danh mục chưa có trên website: Agent xem là duyệt bài, làm đủ 5/5 ảnh (3 hình vẽ, 2 Unsplash), chờ duyệt ảnh; sau đó người dùng tạo danh mục và bấm lại nút. 26/11 09:40 (bảng cũ): người dùng đã duyệt 5/5 ảnh, Agent chèn ảnh vào Trang nháp 8549 (Media 8551-8555); website vẫn chưa có danh mục chống cháy nổ, chờ người dùng tạo rồi bấm lại nút. 26/11 người dùng chốt bỏ bước ghi lên danh mục: nội dung giữ ở Trang nháp 8549, bảng hiện nút "Duyệt, giữ ở Trang nháp"; không cần tạo danh mục để Agent ghi |
| đèn chống cháy nổ 1m2 (nạp 29/10) | `cho_duyet_anh` | `Bai_den-chong-chay-no-1m2.md`, viết lại bài 3904, nháp WP **8546**. 30/10: mạng mở 7 tên miền hãng (signify.com vẫn chặn), Agent Blog bổ sung dữ liệu HALEDCO, Rạng Đông, Duhal, Paragon, Athaco; vòng 3 = 93 CẦN SỬA, vòng 4 = 97 ĐẠT (tổng 95). Phần B còn 3 [CẦN BỔ SUNG]. Chờ người dùng: Điện Quang (không có model chống nổ, khuyến nghị bỏ), nguồn Philips, mở trang tiêu chuẩn cho IEC 60079. Còn 2 điểm nên sửa nhỏ (Paragon CT5/IP, "Ra 82") làm cùng lần sửa sau. 30/10 14:48 người dùng bấm Duyệt bài; 15:01 đủ 15/15 ảnh (4 ảnh bài cũ, 11 hình vẽ), đã lên tab Kiểm duyệt hình ảnh, từ khóa ở `cho_duyet_anh` |
| đèn chống cháy nổ 250w (nạp 30/10) | `san_sang_dang` (27/11 08:38) | 26/11 người dùng duyệt outline (dạng hướng dẫn chọn, `id_bai_cu = 4098`). Viết `Bai_den-chong-chay-no-250w.md`, chấm 89 -> 91 -> 94 (tính ngưỡng 92 -> 94 -> 97) ĐẠT vòng 3. Bản nháp riêng 8557 "[CẬP NHẬT #4098]", bài 4098 giữ nguyên (publish). Còn 4 [CẦN BỔ SUNG]; chờ duyệt bài và 3 câu hỏi (catalogue/giá HLB, báo giá dự án, giữ 2 mẫu Soho). 26/11 15:12 người dùng duyệt bài (bảng cũ); 15:19 đủ 9/9 ảnh (1 Unsplash, 8 hình vẽ), đã lên tab Kiểm duyệt hình ảnh. 27/11 08:34 người dùng duyệt 9/9 ảnh; 08:38 đã chèn vào nháp 8557 (Media 8558-8566). Còn 4 [CẦN BỔ SUNG] và 3 câu hỏi trước khi đăng |
| đèn pha chống cháy nổ (nạp 30/10) | `can_xu_ly` (quay về `moi`) | Không khớp danh mục. SERP 6/8 trang bán hàng. Trùng bài **4018** cùng slug `den-pha-chong-chay-no`: đề xuất viết lại 4018 (`Bai_den-pha-chong-chay-no.md`). `nghien_cuu/Bai_den-pha-chong-chay-no/serp_bao_cao.md`. Chờ 5 câu trả lời. SerpApi trả cache sai lần đầu, phải gọi lại `no_cache=true` (nên thêm vào `nghien_cuu.py`) |
| đèn led nhà xưởng 150w (nạp 05/11) | `cho_duyet_bai` | Danh mục (`loai: danh_muc`), `DM_den-led-nha-xuong-150w.md`. Outline duyệt 05/11. Vòng 1: 88 CẦN SỬA, vòng 2: 99 ĐẠT (ngưỡng 100). Trang nháp 8548 (chưa ghi lên danh mục). Phần B còn 4 [CẦN KIỂM TRA] IP Philips BY239P (thông số IP66, mô tả trang IP40): phải xử lý trước `ap-dung`. Chờ duyệt bài và 6 câu hỏi; 7 [ẢNH] làm sau khi duyệt |

## Việc còn chờ người dùng

- Bảng hỏi thông tin cố định: nhóm 2 còn chờ (lỗi NSX có mất phí, ai chịu ship/tháo lắp bảo hành); nhóm 3-8 chưa trả lời.
- Phát hiện website cần người dùng sửa: BUFO1-200, BUFO3-200 ghi IP40; 4 model 150W hãng khác chung 16.500 lm; Philips ghi chung "BH 24 tháng"; trang bảo hành thiếu số ngày đổi trả; danh mục Điện Quang 150W trống.
- Agent Danh mục (PR #16) chưa chạy thử với danh mục thật.

## Lịch sử thay đổi bảng gần đây

- 26/11/2026 14:50 (cloud, bảng cũ 3wRD): người dùng bấm duyệt 3 dòng lúc 14:33-14:34: 0.6m và 150W "Duyệt, giữ ở Trang nháp" (`da_duyet_nhap`, không còn việc Agent), 250W duyệt outline. Lượt này viết và chấm xong 250W, đẩy nháp 8557.

- 26/11/2026 (đối chiếu trên máy): bảng mới không còn `tu_khoa`, `bai_viet`, `anh`, `yeu_cau`; còn 11 `da_xoa` (9 `da_xu_ly`, 2 `cho_xu_ly`: `den-chong-chay-no-1m2`, `den-chong-chay-no-0-6m`) và 16 tài sản ảnh cũ chờ xóa, logo giữ. Trang bảng đang chạy là bản trước PR #54 (nút "Duyệt, cập nhật lên danh mục"): đã đăng lại từ `dieu_phoi/bang-dieu-phoi.html`, nay hiện "Duyệt, giữ ở Trang nháp". Sửa `bang-dieu-phoi.html` ở phiên cloud thì phiên trên máy phải đăng lại bảng (cloud không ghi được bảng mới).

- 26/11/2026 (sau): người dùng chốt xóa sạch dữ liệu cũ trên bảng mới (11 từ khóa, 5 bài, 20 dòng ảnh, `cham_bai/tong_hop`), từ nay làm trên bảng mới. Đã ghi `da_xoa` cho cả 11 từ khóa, `xoa_nhap: false` (không đụng nháp WP). Hai mục `da_xoa` còn `cho_xu_ly` (`den-chong-chay-no-1m2`, `den-chong-chay-no-0-6m`): lượt Agent kế tiếp xóa 16 tài sản ảnh trên bảng (DIEU_PHOI mục 3b), giữ logo `68bc4a52...`. Lần chấm kế tiếp `cham_len_bang.py` gộp mọi phiếu nên tab Lịch sử chấm điểm sẽ hiện lại điểm các bài cũ.

- 26/11/2026: chuyển sang bảng mới https://claude.ai/artifact/57apPM1U3HKFqe2PVvFsXM (bảng cũ ở tổ chức Claude khác). Dữ liệu dựng lại từ repo, id từ khóa là slug. Chưa có `trigger_id`, chưa có quyền `mcp`: nút gọi Agent ngay chưa chạy (`0_TONG_HOP` mục 8). Phiên cloud (lịch `trig_015wH6yUw1ZwT6sW57KQANC2`) KHÔNG đọc được bảng mới (khác tổ chức), vẫn chỉ thấy bảng cũ; 26/11 09:37 người dùng còn bấm nút trên bảng cũ. Cần người dùng chọn một bảng dùng chung cho cả máy và cloud.

- PR #26: Agent xác nhận nhận việc, nút Chạy Agent ngay mờ khi đã giao, nút cố định vị trí.
- PR #27: nạp trùng từ khóa thì mở sẵn từ khóa cũ; "Tất cả" gồm cả tạm dừng.
- PR #28: gọi ngay mà 10 phút chưa xác nhận thì nút sáng lại.
- PR #29: giờ ghi lên bảng lấy giờ thật.
