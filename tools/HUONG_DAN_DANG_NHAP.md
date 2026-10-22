# Kết nối Agent với denlednhaxuongcaocap.com để đăng bản nháp

Agent đăng bài qua WordPress REST API bằng **Application Password** (mật khẩu ứng dụng). Mật khẩu này chỉ dùng cho API, không đăng nhập được vào trang quản trị, và bạn thu hồi được bất cứ lúc nào.

## Bước 1: Tạo tài khoản riêng cho Agent (khuyến nghị)

1. Vào wp-admin, chọn **Thành viên** rồi **Thêm mới**.
2. Tên đăng nhập: ví dụ `ai-bien-tap`. Email: một email nội bộ.
3. Vai trò: **Cộng tác viên (Contributor)**. Vai trò này chỉ tạo và sửa được bản nháp của chính mình, không đăng công khai, không xóa hay sửa được bài của người khác. Dù script có lỗi, Agent cũng không thể làm thay đổi bài đang chạy trên web.

Nếu muốn Agent tự điền SEO title và meta description vào Rank Math mà vai trò Cộng tác viên không cho phép, thông tin SEO vẫn nằm trong khối ghi chú đầu bản nháp để bạn dán tay.

## Bước 2: Tạo Application Password

1. Đăng nhập wp-admin bằng tài khoản vừa tạo (hoặc vào hồ sơ của tài khoản đó).
2. Vào **Hồ sơ**, kéo xuống mục **Mật khẩu ứng dụng (Application Passwords)**.
3. Đặt tên, ví dụ `Agent viet bai`, bấm **Thêm mật khẩu ứng dụng mới**.
4. Sao chép chuỗi mật khẩu hiện ra. WordPress chỉ hiện chuỗi này một lần.

## Bước 3: Lưu vào máy, không dán vào chat

Mở PowerShell trên máy bạn và chạy 2 lệnh, thay giá trị trong ngoặc kép:

```bash
setx WP_USER "ai-bien-tap"
```

```bash
setx WP_APP_PASSWORD "xxxx xxxx xxxx xxxx xxxx xxxx"
```

Script đọc 2 biến này trực tiếp trên máy. Không gửi mật khẩu vào cuộc trò chuyện.

Thu hồi quyền: vào lại Hồ sơ, bấm **Thu hồi** cạnh mật khẩu ứng dụng.

## Cách Agent đăng bài

```bash
python tools/wp_draft.py Bai_xxx.md --update 2323 --post
```

```bash
python tools/wp_draft.py Bai_xxx.md --new --post
```

- Không có `--post`: chỉ tạo file `.preview.html` để xem trước, không gửi gì lên web.
- Bài luôn ở trạng thái **Bản nháp**, script không có lệnh đăng công khai.
- Script tự chặn: dùng `--new` cho slug đã có bài thì dừng lại, tạo trùng bản nháp cùng tiêu đề thì dừng lại.

## Cách nhận biết bản nháp trong wp-admin

Vào **Bài viết**, lọc **Bản nháp**.

| Loại | Tiêu đề bản nháp | Slug bản nháp | Cách đăng |
|---|---|---|---|
| Viết lại bài cũ | `[CẬP NHẬT #2323] Tiêu đề mới` (2323 là ID bài gốc) | `ban-nhap-cap-nhat-2323` | **Không đăng bản nháp.** Chép nội dung vào bài gốc ID 2323 để giữ URL, rồi xóa bản nháp |
| Chủ đề mới | `[MỚI] Tiêu đề bài` | slug chính thức | Bỏ tiền tố `[MỚI]`, xóa khối ghi chú, bấm Đăng |

Đầu mỗi bản nháp có khối **GHI CHÚ BIÊN TẬP** gồm: loại bài, link bài gốc (nếu là cập nhật), bảng SEO, danh sách placeholder, nguồn, ảnh cần chuẩn bị. Khối này kết thúc ở dòng **NỘI DUNG BÀI BẮT ĐẦU TỪ ĐÂY**. Xóa toàn bộ khối trước khi đăng.

Các chỗ cần xử lý trong thân bài được in đậm: **[CẦN BỔ SUNG: ...]**, **[CẦN KIỂM TRA: ...]**, **[LINK: ...]**, **[ẢNH: ...]**. Dùng Ctrl+F tìm "[CẦN" để rà nhanh.

Tag đề xuất không được tạo tự động, vì tag là trang công khai. Chọn tag trong khối ghi chú và gắn tay khi đăng.
