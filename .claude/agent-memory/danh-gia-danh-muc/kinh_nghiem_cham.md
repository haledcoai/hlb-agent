---
name: kinh-nghiem-cham-danh-muc
description: Kinh nghiệm thực tế khi chấm DM_*.md (dương tính giả của script, chỗ hay sót, cách kiểm nhanh)
metadata:
  type: project
---

- Script báo "0.6" sai định dạng số ở câu có từ khóa chính: dương tính giả khi outline chốt giữ nguyên dạng từ khóa ("0.6m").
- Script báo FAQ H3 "không có trong outline" khi outline ghi câu hỏi FAQ dạng gạch đầu dòng: đối chiếu tay, thường là dương tính giả.
- Danh mục đề xuất: URL dự kiến có thể bị WordPress chuyển 301 sang bài blog cùng slug ở /tu-van/ (kiểm bằng curl -L -w url_effective); nhắc ghi vào phần C.
- Hay sót: bảng chọn của danh mục mâu thuẫn với bài blog anh em đã đăng (ví dụ bài 1m2): luôn so bảng chọn với Bai_*.md cùng nhóm.
- Hay sót: từ khóa phụ outline chỉ nằm trong tên file ảnh, alt, không có trong chữ: đếm bằng Python trên phần B.
- Câu gợi ý viết sẵn ở vòng trước phải tự đếm từ (~20) và so với khối trên trước khi đưa, tránh vòng sau tự bắt lỗi chính câu mình gợi ý.
- Lệnh nhanh: kiem_tra_bai.py --gon; curl các link nội bộ; phieu_duyet.py nhan trước khi đặt nhãn.

**Why:** rút từ lần chấm DM_den-chong-chay-no-0-6m vòng 1 (25/11/2026).
**How to apply:** dùng ở bước kiểm tra cơ học và đối chiếu dữ liệu của mỗi lần chấm danh mục.
