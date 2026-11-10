# TỔNG HỢP DỰ ÁN AI AGENT VIẾT BÀI CHO DENLEDNHAXUONGCAOCAP.COM

Cập nhật: 04/11/2026. File này tóm tắt các quyết định, trạng thái và việc còn dở, để tiếp tục ở phiên làm việc khác mà không cần đọc lại toàn bộ cuộc trò chuyện.

## 1. Mục tiêu

Agent nhận bộ từ khóa, nghiên cứu SERP, lập outline gửi duyệt, viết bài, rồi đưa bản nháp lên website denlednhaxuongcaocap.com (WordPress) để người dùng duyệt và tự đăng.

## 2. Các file trong dự án

| File | Vai trò |
|---|---|
| 1_Project_Instructions_Auto_Blog_HLB.md | Quy trình 4 bước, giọng văn, quy tắc dữ liệu, cách viết về thương hiệu, quy tắc đăng bản nháp. Dán vào ô Instructions của Claude Project |
| 2_Knowledge_Du_lieu_tham_chieu_HLB.md | Thông tin HLB đã xác nhận, URL danh mục và bài Tư vấn, cách đọc trang sản phẩm, chuẩn SEO, checklist. Tải lên Project Knowledge |
| 6_Agent_Danh_muc_HLB.md | Quy tắc Agent Danh mục (27/10/2026): viết lại nội dung danh mục sản phẩm đã có, file `DM_<slug>.md`, Trang nháp xem trước, chỉ ghi lên danh mục khi người dùng duyệt. Agent `danh-gia-danh-muc` chấm theo `quy_tac_cham_danh_muc.md` |
| tools/danh_muc.py | Công cụ Agent Danh mục: `ds`, `tim` (nhận diện từ khóa danh mục), `doc` (lưu danh mục, sản phẩm, nội dung cũ vào `nghien_cuu/DM_<slug>/`), `nhap` (Trang nháp), `ap-dung` (sao lưu rồi ghi mô tả, Rank Math), `kiem-trang`, `khoi-phuc` |
| 4_Agent_danh_gia_noi_dung_HLB.md | Hồ sơ agent đánh giá: kiểm tra cơ học làm tay, phần chạy trong Claude Code (phiếu, nhật ký, hook), lịch sử, bài học, việc còn mở. Cách chấm nằm ở `.claude/agents/danh-gia-noi-dung.md` |
| 5_Agent_danh_gia_ban_claude_ai.md | Bản chấm cho Claude Project trên claude.ai, ngừng cập nhật từ 04/11/2026 (còn thang v2) |
| 3_Bang_hoi_thong_tin_co_dinh_HLB.md | Bảng hỏi thông tin cố định (8 nhóm). Đã trả lời nhóm 1 và phần lớn nhóm 2 |
| du_lieu_san_pham_HLB_<ngày>.csv | Thông số và giá 113 sản phẩm đọc từ website. Làm mới bằng `python tools/lam_moi_csv.py` (giữ một file mới nhất, bản cũ trong git) |
| Bai_cach-chon-den-led-nha-xuong.md | Bài viết lại "cách chọn đèn LED nhà xưởng" (phần A, B, C) |
| tools/wp_draft.py | Script đưa bản nháp lên WordPress qua REST API |
| tools/HUONG_DAN_DANG_NHAP.md | Hướng dẫn tạo Application Password, cách đánh dấu bản nháp |
| tools/kiem_tra_bai.py | Kiểm tra lỗi cơ học của bài (dấu gạch, từ cấm, link, độ dài SEO, định dạng số, thông số so với CSV). Thoát mã 1 khi còn LỖI |
| .claude/agents/danh-gia-danh-muc.md | Sub agent đánh giá nội dung danh mục (27/10/2026, tách khỏi agent chấm blog): Leader Content 7 năm kinh nghiệm duyệt file `DM_*.md` theo `quy_tac_cham_danh_muc.md` và `checklist_cham_danh_muc.md`, ghi phiếu, không sửa bài |
| quy_tac_cham_danh_muc.md, checklist_cham_danh_muc.md | Quy tắc, thang chấm và checklist có mã mục cho nội dung danh mục (agent `danh-gia-danh-muc`) |
| quy_tac_cham.md, checklist_cham_bai.md | Bản rút gọn quy tắc và checklist chấm bài blog (agent `danh-gia-noi-dung`) |
| .claude/agents/danh-gia-noi-dung.md | Sub agent đánh giá chất lượng bài blog: chạy script trên, đối chiếu dữ liệu, chấm 100 điểm (ĐẠT từ 95), ghi phiếu duyệt, trả báo cáo. Không sửa bài |
| CLAUDE.md | Quy tắc lúc nào cũng cần: đồng bộ code, vòng duyệt tự động (chấm, sửa, tối đa 3 vòng), mô hình phòng ban, điều cấm, và dòng chỉ đường tới `quy_trinh/` |
| quy_trinh/ | Quy trình đọc khi cần (04/11/2026): `chay_tren_may.md` (cài đặt máy Windows), `nhat_ky_cham_va_bang.md` (nhật ký chấm, cập nhật bảng, hook, lệnh cho agent đánh giá), `anh.md` (ảnh, trang duyệt ảnh), `dang_ban_nhap.md` (thủ tục đăng nháp) |
| tools/phieu_duyet.py | Ghi và kiểm tra phiếu duyệt (`.danh_gia/<bài>.json`, kèm mã kiểm tra nội dung). Kiêm các hook: chặn `wp_draft.py --post` khi chưa có phiếu ĐẠT; chỉ agent đánh giá được chạy `ghi`; đánh dấu đang chấm khi gọi agent đánh giá; ghi nhận bài vừa sửa; không cho kết thúc lượt khi bài vừa sửa chưa được chấm lại (trừ khi đang có lượt chấm) |
| .claude/agents/tao-anh.md | Sub agent chuẩn bị ảnh: ảnh sản phẩm lấy ảnh thật trên website, sơ đồ và bảng vẽ bằng Python, ảnh minh họa không gian tạo bằng Canva. Không sửa bài, không tải lên website |
| tools/tao_anh.py | Liệt kê chỗ [ẢNH], gợi ý nguồn ảnh (`phan-loai`, đối chiếu CSV), lấy ảnh sản phẩm thật, chuẩn hóa JPG 820 px (rộng 800-850, cao 400-800), ghi trạng thái duyệt, ghi danh sách `anh/<bài>/anh.json` (ảnh Canva lưu cả prompt), kiểm tra đủ ảnh, tên ảnh không trùng slug, alt (cần Pillow, matplotlib) |
| tools/mau_anh.py | Thư viện 6 mẫu sơ đồ dùng chung: lưới bố trí, bảng IP, bảng so sánh, biểu đồ cột, mặt cắt chiều cao treo và góc chiếu, các bước. Tự kiểm tra chữ trên hình (đè, tràn, dưới 13 px, em dash) trước khi lưu |
| anh/_prompt_canva.md | 6 prompt Canva mẫu cho cảnh nhà xưởng, cách sửa prompt khi ảnh bị trả về, cách tạo và xuất ảnh Canva (agent chỉ đọc khi dùng Canva) |
| tools/tao_anh.py thu-vien, dung-lai | Thư viện ảnh đã duyệt và đã tải lên website ở mọi bài: tìm theo từ khóa, dùng lại media có sẵn cho bài mới, không tạo mới, không tải lại (24/10/2026) |
| dieu_phoi/anh_len_bang.py | Tạo sẵn dữ liệu đưa ảnh chờ duyệt của cả bài lên tab Kiểm duyệt hình ảnh: danh sách file cần tải và mảng `writes` cho một lần ArtifactData batch |
| anh/<bài>/ | Ảnh của từng bài, `anh.json` và script vẽ sơ đồ `ve_so_do.py` (gọi mẫu trong `tools/mau_anh.py`). `wp_draft.py` đọc `anh.json`: `--post` tải ảnh lên Media, chèn vào bài và đặt ảnh đại diện |
| .danh_gia/nhat_ky.jsonl | Nhật ký chấm, chỉ thêm không ghi đè: mỗi lần chấm (điểm 6 tiêu chí, vấn đề có nhãn, phiên bản thang chấm) và mỗi lần agent đánh giá bị bác bỏ. Đã nhập lại 3 lần chấm bài "cách chọn đèn" ngày 21/10/2026 (thang v1) |
| Lịch sử chấm bài | Tab Lịch sử chấm của Bảng điều phối HLB https://claude.ai/artifact/3wRDGsubs7s2Kb75vpypmG (trang cũ JVfjfAmGtDAtZr49TFodBc ngừng cập nhật từ 22/10/2026): điểm qua các lần chấm, điểm mất theo tiêu chí, vấn đề lặp lại, lần agent bị bác bỏ, bảng lịch sử. Dữ liệu từ `phieu_duyet.py xuat`, cập nhật cuối mỗi vòng duyệt (`quy_trinh/nhat_ky_cham_va_bang.md`) |
| .claude/settings.json | Cho phép lệnh `phieu_duyet.py ghi`, `nhan`. Khai báo 5 hook: PreToolUse Bash (chặn đăng, chặn ghi phiếu ngoài agent đánh giá), PreToolUse Agent (đánh dấu đang chấm), SubagentStop (bỏ đánh dấu), PostToolUse (ghi nhận sửa bài), Stop (nhắc chấm lại) |

## 3. Quyết định đã chốt

Không chép lại ở đây để tránh lệch. Nguồn duy nhất:
- Thương hiệu, vai trò HLB và HALEDCO, mốc năm, liên hệ, bảo hành, đổi trả, giao hàng, chiết khấu: `2_Knowledge_Du_lieu_tham_chieu_HLB.md` mục 1, 1.1.
- Quy tắc nội dung (không link haledco.com, so sánh công bằng, không bịa, duyệt SERP và outline), cách đặt tiêu đề, slug bản nháp: `1_Project_Instructions_Auto_Blog_HLB.md` mục 2, 3, 10.
- Đăng nhập WordPress, khối ghi chú biên tập: `tools/HUONG_DAN_DANG_NHAP.md`.

## 4. Trạng thái công việc

Trạng thái từng từ khóa và bài: Bảng điều phối HLB (https://claude.ai/artifact/3wRDGsubs7s2Kb75vpypmG) và `dieu_phoi/TRANG_THAI.md`. Mục 5 dưới đây chỉ giữ chi tiết để tra cứu.

## 5. Việc còn dở (chi tiết tra cứu)

**Agent Danh mục (27/10/2026, đã xây xong, chưa chạy thử theo yêu cầu người dùng)**
- Khối trên lưới sản phẩm nằm ở trường riêng của theme, REST chưa mở: cần tên trường (hoặc nhờ người làm web mở `show_in_rest`) để ghi `khoi_tren_meta` vào `danh_muc/cau_hinh.json`. Chưa có thì người dùng dán tay.
- Chờ trả lời: có viết nội dung cho danh mục con theo hãng (Philips 150W...) không; từ khóa "đèn chống cháy nổ 20w" (không có danh mục) chuyển viết lại bài blog ID 4069?
- Chạy thử đầu tiên khi người dùng yêu cầu (đề xuất danh mục đèn LED nhà xưởng 150W).

**Chờ người dùng xác nhận (nhóm 2)**
- Đổi trả do lỗi sản phẩm có mất phí 10% không? Ai chịu phí vận chuyển, tháo lắp khi bảo hành?
- Đã trả lời 04/11/2026: đổi trả theo nhu cầu trong 15 ngày, phí 10%; miễn phí giao hàng tính từ văn phòng Xuân Đỉnh. Điều kiện đổi mới trong 15 ngày đầu của dòng cao cấp đã có ở Knowledge mục 1.1 (xác nhận 21/10/2026).

**Chưa trả lời:** nhóm 3 (dịch vụ) đến nhóm 8 (người duyệt, ảnh) trong file 3.

**Placeholder còn trong bài 8514** (5 chỗ, kiểm tra 22/10/2026)
- `[CẦN KIỂM TRA]` Đối chiếu bảng độ rọi với TCVN 7114-1:2008, kèm `[LINK]` trang tra cứu (Agent tự làm). 26/10/2026: mã và tên TCVN 7114-1:2008 đã tra nguồn (có trong `tieu_chuan_da_kiem.csv`, link bản PDF thư viện Rạng Đông); giá trị lux trong bảng chưa đối chiếu vì mạng cloud chặn trang văn bản, lần sửa bài tới đọc bản PDF bằng WebFetch.
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

**Công cụ chống lỗi thêm ngày 26/10/2026:** `tieu_chuan_da_kiem.csv` (12 mã tiêu chuẩn đã tra nguồn, có bản thay thế), `tools/nghien_cuu.py` lưu outline đã chốt và văn bản bài top SERP; `kiem_tra_bai.py` báo LỖI khi heading lệch outline hoặc có đoạn 25 từ liền nhau trùng bài top. Hai bài cũ chưa có file outline, SERP nên chưa được so.

## 6. Phát hiện trên website cần người dùng xử lý

- ~~47 model dòng cao cấp có bảng thông số trống~~: sai do cách đọc cũ (26/10/2026). Các trang này ghi nhãn khác ("Quang thông" thay vì "Quang thông (lm)"), `lam_moi_csv.py` đọc được đủ thông số cả 113 model.
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

## 8. Lịch sử thay đổi quy tắc (chuyển từ CLAUDE.md 04/11/2026)

- **Chế độ chấm:** 22/10/2026 "chấm phần", 24/10 "kiểm lại", từ 26/10 luôn chấm đủ cả bài theo 6 tiêu chí.
- **Trang theo dõi:** từ 22/10/2026 tab Lịch sử chấm điểm và tab Kiểm duyệt hình ảnh của Bảng điều phối HLB thay trang Lịch sử chấm bài HLB cũ (JVfjfAmGtDAtZr49TFodBc) và trang Duyệt ảnh HLB cũ (`anh/trang-duyet-anh.html`). Trang cũ không cập nhật nữa.
- **Hook trên cloud:** 26/10/2026 thấy phiên thread và phiên chạy theo lịch không nạp `.claude/settings.json`. Kiểm lại 04/11/2026 bằng `tools/kiem_hook.py`: lượt lịch "Điều phối HLB" có repo sẵn ở `/home/user/hlb-agent` trước khi Claude Code khởi động, nhưng vẫn không có dấu SessionStart, tức không nạp hook.
- **Máy Windows:** trước 03/11/2026 chưa cài git, file trong `.claude/` chép tay qua `cap_nhat_agent/`. Từ 03/11 folder là bản clone của `main`, không chép tay nữa.
- **CLAUDE.md gọn lại (04/11/2026):** chỉ giữ quy tắc lúc nào cũng cần. Nhóm từ khóa chuyển vào file 1 mục 3, nội dung danh mục vào file 6, phần còn lại vào `quy_trinh/` (`chay_tren_may.md`, `nhat_ky_cham_va_bang.md`, `anh.md`, `dang_ban_nhap.md`).
- **Lượt điều phối tự gọi nối tiếp:** thêm ở PR #34 (lượt còn việc tự `fire_trigger` lượt sau). Bỏ từ 05/11/2026 (người dùng chốt) vì mỗi lượt làm hệ thống đăng một dòng vào project chat. Việc còn lại để lượt dự phòng 8:04 hoặc lần người dùng thao tác trên bảng.
- **Danh mục chưa có trên website:** 27/10/2026 dừng chờ người dùng tạo danh mục. Từ 05/11/2026 (người dùng trả lời trên bảng "Đưa bài nháp lên trang") Agent Danh mục vẫn viết với danh mục đề xuất (`danh_muc.py de-xuat`) và đưa lên Trang nháp; chỉ `ap-dung` chờ người dùng tạo danh mục.
- **Tắt lượt dự phòng 8:04 (09/11/2026, người dùng chốt):** Agent tạm không cần điều phối tự động. Lịch `trig_015wH6yUw1ZwT6sW57KQANC2` tắt, giữ lại để người dùng bật lại khi cần.
- **Ô Nạp từ khóa (10/11/2026, người dùng chốt):** trước đó bảng ghi "mỗi dòng là một bài", sai với quy ước. Đúng là một nhóm từ khóa là một bài SEO: mỗi dòng một từ khóa, dòng đầu là từ khóa chính, các dòng sau là phụ, liên quan. Nhiều bài một lần thì cách nhóm bằng dòng trống; `#ID` (viết lại bài cũ) và link danh mục ghi ở dòng đầu của nhóm.
