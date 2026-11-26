# Dự án AI Agent viết bài cho denlednhaxuongcaocap.com

Quy trình viết bài, giọng văn và quy tắc dữ liệu nằm ở `1_Project_Instructions_Auto_Blog_HLB.md` và `2_Knowledge_Du_lieu_tham_chieu_HLB.md`. Trạng thái từng từ khóa nằm trên Bảng điều phối và `dieu_phoi/TRANG_THAI.md`; danh sách file, chi tiết việc dở và lịch sử nằm ở `0_TONG_HOP_DU_AN_AI_AGENT_HLB.md`. Đọc file 1, file 2 trước khi làm việc với bài viết. Thông tin công ty và chính sách (bảo hành, đổi trả, giao hàng) chỉ ghi ở file 2 mục 1, 1.1; file khác trỏ về đó, không chép lại.

**Một nguồn quy tắc (người dùng chốt 26/10/2026):** file `1_Project_Instructions_Auto_Blog_HLB.md` trên repo là bản gốc. Project settings chỉ giữ bản ngắn trỏ về file này. Đổi quy tắc thì sửa file repo (và `quy_tac_cham.md` nếu quy tắc chấm đổi), không sửa Project settings.

## Đọc thêm khi cần

- Nhận một nhóm từ khóa (một bài; dòng đầu là từ khóa chính, các dòng sau là phụ): `1_Project_Instructions_Auto_Blog_HLB.md` mục 3, Nhóm từ khóa.
- Nội dung danh mục sản phẩm (`DM_*.md`, Trang nháp, ghi lên danh mục): `6_Agent_Danh_muc_HLB.md`.
- Cài đặt máy Windows, giờ Việt Nam, biến môi trường: `quy_trinh/chay_tren_may.md`.
- Kết thúc vòng duyệt (ghi nhật ký, cập nhật Lịch sử chấm, chạy `doi_chieu_bang.py`), đổi thang chấm, gặp hook nhắc, lệnh cho agent đánh giá: `quy_trinh/nhat_ky_cham_va_bang.md`.
- Đặt `[ẢNH]`, gọi `tao-anh`, đưa ảnh lên bảng, xử lý ảnh đã duyệt: `quy_trinh/anh.md`.
- Sắp chạy `wp_draft.py --post`: `quy_trinh/dang_ban_nhap.md`.
- Lượt Agent điều phối: `DIEU_PHOI.md`. Lịch sử thay đổi quy tắc: `0_TONG_HOP_DU_AN_AI_AGENT_HLB.md` mục 8.

## Đồng bộ code (người dùng chốt 23/10/2026)

- GitHub (`haledcoai/hlb-agent`, nhánh `main`) là bản gốc. Mỗi khi người dùng chốt một phương án làm đổi code, agent, CLAUDE.md hay quy trình, đẩy thay đổi lên GitHub ngay trong lượt đó, không chờ nhắc.
- Máy Windows (folder `AI Agent denlednhaxuong`) là bản clone của `main`. Không chép file tay giữa máy và repo.

### Chạy trên máy (người dùng chốt 03/11/2026)

Agent điều phối và các Agent con chạy được cả trên máy lẫn cloud. Phiên trên máy làm đúng ba việc:
1. **Đầu lượt:** `git pull` trên `main`. Folder còn thay đổi chưa commit thì xem đó là việc dở của lượt trước: commit và push trước, không xóa.
2. **Cuối lượt:** commit và push lên `main` ngay khi xong việc, kể cả khi dừng giữa chừng. Push bị từ chối vì cloud đã đẩy trước thì `git pull --rebase` rồi push lại; gặp xung đột thì dừng và báo người dùng, không ghi đè.
3. **Không chạy song song với cloud trên cùng một bài:** trước khi làm một từ khóa, kiểm tra và ghi `khoa_luc` trên Bảng điều phối như phiên cloud (`DIEU_PHOI.md`). Từ khóa đang có khóa còn hạn thì bỏ qua.

## Vòng duyệt tự động (bắt buộc)

Mỗi khi viết xong một bài mới hoặc sửa một file bài (`Bai_*.md`) hoặc file nội dung danh mục (`DM_*.md`, chấm theo thang danh mục ở `quy_tac_cham_danh_muc.md`), tự chạy vòng sau, không chờ người dùng nhắc. Phiên cloud không có hook nhắc, vẫn phải tự chạy.

1. **Chấm:** gọi sub agent `danh-gia-noi-dung` cho bài blog `Bai_*.md`, `danh-gia-danh-muc` cho nội dung danh mục `DM_*.md` (người dùng chốt 27/10/2026: danh mục có agent chấm riêng). Truyền: đường dẫn file bài, số vòng (bắt đầu từ 1), outline đã chốt (nếu có), các điểm người dùng đã nói để sau.
2. **Đọc kết luận** ở đầu báo cáo:
   - **ĐẠT** (điểm tính ngưỡng từ 95, không còn lỗi bắt buộc): dừng vòng, gọi agent `tao-anh` (`quy_trinh/anh.md`), rồi báo người dùng.
   - **CẦN SỬA** hoặc **KHÔNG ĐẠT**: sang bước 3.
3. **Tự sửa** file bài theo báo cáo (phiên Agent điều phối giao bước này cho `agent-blog` hoặc `agent-danh-muc` chế độ `sua`, người dùng chốt 28/10/2026; trưởng phòng vẫn ghi `bac-bo` và chạy lại `kiem_tra_bai.py` để kiểm):
   - Sửa hết mục 1 (lỗi bắt buộc) và mục 2 (nên sửa).
   - Không tự sửa mục 2b (cần người dùng quyết định). Gom lại để hỏi ở bước 5.
   - Mỗi điểm sửa phải đúng nguồn: số liệu mới thì kiểm tra lại CSV hoặc trang sản phẩm, phép tính mới thì tính lại bằng Python. Không bịa để lấy điểm.
   - Nếu thấy agent đánh giá nhận định sai (đối chiếu nguồn thấy khác), không sửa theo; ghi vào nhật ký bằng `python tools/phieu_duyet.py bac-bo <file_bai.md> --vong <n> --nhan <nhãn agent đã dùng cho vấn đề đó> --ly-do "<nguồn nói gì>"`, rồi báo người dùng. Gợi ý sửa của vòng trước mà vòng sau bị chấm là lỗi cũng ghi như vậy.
   - Chạy `python tools/kiem_tra_bai.py <file_bai.md>` cho tới khi 0 lỗi.
4. **Chấm lại:** quay về bước 1 với số vòng tăng thêm 1. **Tối đa 3 vòng chấm.**
5. **Dừng và báo người dùng** khi bài ĐẠT, hoặc hết 3 vòng mà vẫn chưa đạt, hoặc chỉ còn các điểm ở mục 2b. Trước khi báo, cập nhật Lịch sử chấm và đồng bộ Bảng điều phối theo `quy_trinh/nhat_ky_cham_va_bang.md`. Báo gồm:
   - Điểm từng vòng.
   - Những gì đã sửa.
   - Những điểm agent đánh giá nói sai và đã bỏ qua.
   - Câu hỏi cho người dùng (mục 2b), đánh số để trả lời một lần.

**Luôn chấm đủ cả bài** (người dùng chốt 26/10/2026): mỗi lần bài bị sửa, kể cả vòng 2, 3 và sửa theo góp ý người dùng, agent đánh giá chấm lại toàn bài theo đủ 6 tiêu chí. Từ vòng 2, agent còn đối chiếu với lần chấm trước (`phieu_duyet.py lan-truoc`, `phieu_duyet.py khac`) để giữ điểm nhất quán: ghi rõ từng vấn đề cũ đã sửa hay chưa, và vấn đề nào mới thấy ở phần không đổi.

Chỉ chấm, không tự sửa, khi người dùng chỉ yêu cầu "đánh giá" hoặc "chấm" một bài.

**Hook nhắc (Stop, chỉ chạy trên máy):** khi kết thúc lượt mà bài vừa sửa chưa được chấm lại, hook không cho dừng. Gặp nhắc này thì chấm lại bài, không kết thúc lượt bằng cách khác.

## Agent điều phối và Agent con (người dùng chốt 28/10/2026)

Mô hình phòng ban: người dùng giao việc qua Bảng điều phối, Agent điều phối là trưởng phòng, giao việc cho Agent con và không tự viết bài. Agent con: `agent-blog` (nghiên cứu, viết, sửa bài blog), `agent-danh-muc` (nghiên cứu, viết, sửa nội dung danh mục), `danh-gia-noi-dung`, `danh-gia-danh-muc` (chấm), `tao-anh` (ảnh). Mỗi Agent con khai báo `model:` (viết, chấm blog: `sonnet`; chấm danh mục: `opus` vì nội dung danh mục lên công khai ngay; tạo ảnh: `haiku`) và `memory: project` (ghi nhớ ở `.claude/agent-memory/<tên>/`, trưởng phòng commit cùng việc của lượt) trong frontmatter, người dùng chốt 09/11/2026. Chi tiết ở `DIEU_PHOI.md` đầu file. Khi người dùng giao việc viết bài trực tiếp trong thread chat, phiên chat cũng đóng vai trưởng phòng và giao cho Agent con như trên.

**Khi không gọi được sub agent theo tên** (phiên thread trên cloud có thể không nạp `.claude/agents/`, danh sách agent không có `danh-gia-noi-dung`, `danh-gia-danh-muc`, `tao-anh`, `agent-blog`, `agent-danh-muc`): gọi agent `general-purpose`, trong lời gọi yêu cầu agent đọc và làm đúng theo file `.claude/agents/<tên>.md`, kèm các thông tin cần truyền như thường, và truyền tham số `model` đúng như dòng `model:` trong file agent đó (để giữ mức tiết kiệm token). Ghi trong báo cáo cho người dùng là đã dùng cách này.

**Không báo trong chat (người dùng chốt 29/10/2026):** lượt Điều phối và sub agent chỉ ghi hoạt động, kết quả, câu hỏi lên Bảng điều phối; chỉ nhắn chat khi có lỗi hệ thống cần người dùng sửa. Chi tiết ở `DIEU_PHOI.md` đầu file.

## Điều cấm

- **Không tự chạy `tools/phieu_duyet.py ghi`.** Phiếu chỉ do agent đánh giá (`danh-gia-noi-dung` hoặc `danh-gia-danh-muc`) ghi sau khi chấm. Khi bị hook chặn, chạy lại vòng duyệt, không tìm cách vượt hook.
- Chỉ chạy `python tools/wp_draft.py <file_bai.md> ... --post` khi người dùng đã đồng ý đăng và bài có phiếu ĐẠT. Agent không bao giờ dùng `--bo-qua-phieu` (chỉ người dùng tự chạy trong terminal của họ).
- **Không ghi lên danh mục (người dùng chốt 26/11/2026).** Nội dung danh mục sau khi duyệt chỉ để ở Trang nháp (`danh_muc.py nhap --post`). Agent không ghi mô tả, SEO title, meta vào danh mục sản phẩm; `danh_muc.py ap-dung --post` đã tắt. Người dùng tự chép từ Trang nháp vào danh mục trong wp-admin.
- Ảnh tải lên thư viện Media của WordPress là công khai ngay, dù bài còn ở trạng thái nháp. Chỉ ảnh có `trang_thai: "duyet"` trong `anh.json` được chèn vào bài.
