# Đăng bản nháp bài blog

Đọc khi sắp chạy `tools/wp_draft.py ... --post`. Các điều cấm nằm ở `CLAUDE.md` mục Điều cấm; cách đặt tiêu đề, slug bản nháp ở `1_Project_Instructions_Auto_Blog_HLB.md` mục 10.

- Chỉ chạy `python tools/wp_draft.py <file_bai.md> ... --post` khi người dùng đã đồng ý đăng và bài có phiếu ĐẠT.
- `wp_draft.py --post` và hook (khi có) chặn lệnh đăng nếu thiếu phiếu ĐẠT, phiếu không khớp nội dung hiện tại (bài bị sửa sau lần chấm), hoặc `kiem_tra_bai.py` còn lỗi. Kiểm tra trước bằng `python tools/phieu_duyet.py xem <file_bai.md>`.
- **Không tự chạy `tools/phieu_duyet.py ghi`.** Phiếu chỉ do agent đánh giá (`danh-gia-noi-dung` hoặc `danh-gia-danh-muc`) ghi sau khi chấm. Khi bị hook chặn, chạy lại vòng duyệt, không tìm cách vượt hook.
- Lệnh đăng cũng bị chặn khi phần B còn quá 5 chỗ `[CẦN BỔ SUNG]` (người dùng chốt 26/10/2026): gửi người dùng danh sách dữ liệu cần bổ sung thay vì đăng.
- `wp_draft.py --post` tự kiểm tra phiếu như hook (phiên cloud không nạp hook). Người dùng muốn đăng khi bài chưa đạt 95 thì người dùng tự chạy lệnh trong terminal của họ, thêm `--bo-qua-phieu`. Agent không bao giờ dùng cờ này.
