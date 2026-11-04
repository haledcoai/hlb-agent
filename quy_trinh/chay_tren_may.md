# Chạy trên máy Windows (người dùng chốt 03/11/2026)

Đọc khi phiên chạy trên máy người dùng (folder `AI Agent denlednhaxuong`) và cần cài đặt git, lấy giờ, đặt biến môi trường. Ba việc đầu lượt, cuối lượt, khóa từ khóa nằm ở `CLAUDE.md` mục Đồng bộ code.

Repo trên máy đặt `git config core.autocrlf false`, để file bài giữ xuống dòng LF như cloud; không thì mã sha256 của phiếu duyệt lệch.

Giờ Việt Nam lấy bằng `TZ=UTC-7 date -Iseconds` (chạy đúng cả Git Bash trên Windows lẫn Linux; `TZ=Asia/Ho_Chi_Minh` trên Git Bash trả về giờ UTC vì thiếu dữ liệu múi giờ).

Nút "Chạy Agent ngay" trên bảng luôn gọi lượt chạy trên cloud, không gọi máy. Máy chỉ chạy khi người dùng mở Claude Code trong folder.

Biến môi trường (`WP_USER`, `WP_APP_PASSWORD`, `SERPAPI_KEY`, `PIXABAY_API_KEY`) đặt làm biến môi trường người dùng của Windows (`setx TEN "giá trị"`, mở lại Claude Code sau khi đặt). Các script đọc `os.environ`, không đọc file `.env`.
