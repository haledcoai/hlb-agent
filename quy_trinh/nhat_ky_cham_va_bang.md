# Nhật ký chấm, Bảng điều phối và hook

Đọc khi kết thúc vòng duyệt (`CLAUDE.md` bước 5), khi đổi thang chấm, hoặc khi gặp hook nhắc. Agent đánh giá đọc thêm phần lệnh và file nghiên cứu.

## Nhật ký chấm và trang theo dõi

Mỗi lần agent đánh giá ghi phiếu, `tools/phieu_duyet.py` thêm một dòng vào `.danh_gia/nhat_ky.jsonl` (điểm từng tiêu chí, các vấn đề có nhãn). Agent chính ghi thêm các lần bác bỏ (bước 3). Không sửa tay file nhật ký.

Lịch sử chấm hiện ở tab **Lịch sử chấm điểm** của **Bảng điều phối HLB**: https://claude.ai/artifact/57apPM1U3HKFqe2PVvFsXM. Cập nhật một lần khi kết thúc vòng duyệt (bước 5), trước khi báo người dùng:
1. `python tools/phieu_duyet.py xuat` rồi `python dieu_phoi/cham_len_bang.py > <file tạm>.json`.
2. `ArtifactData` `set` collection `cham_bai`, doc_id `tong_hop`, `file_path` là file tạm, kèm `if_version` (đọc `get` trước để lấy version).

`tieu_chi.json` chỉ đổi khi thang chấm đổi. Khi đổi tiêu chí, điểm tối đa hoặc ngưỡng trong `.claude/agents/danh-gia-noi-dung.md`, sửa luôn `TIEU_CHI`, `NGUONG` và tăng `THANG_CHAM` trong `tools/phieu_duyet.py`, để trang không so lẫn điểm của hai thang.

## Đồng bộ Bảng điều phối sau khi sửa bài (bắt buộc, 26/10/2026)

Phiên nào sửa một `Bai_*.md` đã có dòng trên Bảng điều phối, khi kết thúc vòng duyệt phải `ArtifactData list` collection `tu_khoa`, `bai_viet` với `out_dir`, chạy `python dieu_phoi/doi_chieu_bang.py <out_dir>` và làm hết việc script in ra (thêm `diem_vong`, cập nhật `bao_cao`, `cau_hoi`, `bai_viet`, xóa `nhap_khop` cũ, đẩy lại nháp theo `DIEU_PHOI.md` mục 3a khi phiếu ĐẠT). Script báo khớp mới coi là xong. Không làm bước này thì bảng hiện điểm, bài và trạng thái bản nháp cũ.

## Hook

**Hook nhắc (Stop):** mỗi file `Bai_*.md` bị sửa bằng Edit/Write được ghi nhận. Khi kết thúc lượt mà file đó chưa có phiếu duyệt khớp nội dung (chưa được chấm lại sau lần sửa cuối), hook không cho dừng và yêu cầu chạy vòng duyệt. Hook nhắc tối đa 3 lần cho một file, sau đó cho dừng kèm cảnh báo. Khi agent đánh giá (`danh-gia-noi-dung` hoặc `danh-gia-danh-muc`) đang chấm (kể cả chạy nền), hook không nhắc; dấu "đang chấm" xóa khi agent ghi phiếu hoặc kết thúc, quá 30 phút thì tự hết hạn. Gặp nhắc này thì chấm lại bài, không kết thúc lượt bằng cách khác.

**Hook không chạy ở phiên cloud:** phiên thread trong project và phiên chạy theo lịch trên cloud không nạp `.claude/settings.json` của repo, nên các hook nhắc và chặn ở đây không chạy. Quy tắc vẫn giữ nguyên: sửa `Bai_*.md` xong thì tự chạy vòng duyệt, không chờ hook nhắc. Các chặn quan trọng đã nằm trong script: `wp_draft.py --post` tự kiểm phiếu, `bai_len_bang.py` dừng khi phiếu không khớp. Hook chỉ chắc chạy khi người dùng mở Claude Code trên máy trong folder dự án. Muốn thử lại sau khi nền tảng đổi thì chạy `python tools/kiem_hook.py xem` ở đầu một lượt cloud (hook SessionStart ghi dấu `.danh_gia/_hook_da_chay.json`).

## Cho agent đánh giá

**Agent đánh giá là Leader Content, chỉ chấm bài blog** (người dùng chốt 27/10/2026): rà đủ `checklist_cham_bai.md` mỗi lần chấm, chấm khắt khe theo quy tắc trong file đó. Nội dung danh mục có agent chấm riêng `danh-gia-danh-muc`, cũng là Leader Content (7 năm kinh nghiệm, hiểu kỹ thuật chiếu sáng, technical SEO, kỹ thuật viết), rà đủ `checklist_cham_danh_muc.md` mỗi lần chấm.

**Lệnh cho agent đánh giá:** `python tools/kiem_tra_bai.py <bài> --gon` (bản in gọn), `python tools/kiem_tra_bai.py --tra <model hoặc số>` (tra và đếm trên CSV). `phieu_duyet.py ghi` chỉ chạy khi `kiem_tra_bai.py` vừa chạy trên đúng nội dung bài.

**File nghiên cứu (người dùng chốt 26/10/2026):** `nghien_cuu/<tên bài>/outline.md` (outline đã chốt) và `nghien_cuu/<tên bài>/serp/` (văn bản bài top), lưu bằng `tools/nghien_cuu.py`. `kiem_tra_bai.py` báo LỖI khi heading lệch outline hoặc có đoạn từ 25 từ liền nhau trùng bài top (từ 10 từ là cảnh báo). Mã tiêu chuẩn đối chiếu `tieu_chuan_da_kiem.csv`.
