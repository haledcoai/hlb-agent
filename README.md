# HLB Agent: hệ thống viết bài tự động cho denlednhaxuongcaocap.com

Cập nhật: 11/11/2026.

Repo này chứa toàn bộ quy trình, agent và công cụ để Claude tự viết bài blog và nội dung danh mục sản phẩm cho website **Đèn LED Nhà Xưởng HLB** (denlednhaxuongcaocap.com). Người dùng nạp nhóm từ khóa trên Bảng điều phối, các agent nghiên cứu SERP, lập outline, viết, tự chấm, tạo ảnh rồi đưa lên WordPress ở dạng **bản nháp**. Không có bài nào được đăng công khai tự động.

HLB là đơn vị trung gian phân phối đèn LED nhà xưởng của nhiều thương hiệu: HALEDCO, Rạng Đông, Philips, Điện Quang và các hãng khác. Không viết "HLB sản xuất". Từ 11/11/2026 không còn khái niệm "dòng cao cấp": các dòng BUFO1-4, B1-B11, B8 DX gọi theo tên dòng, không gán hãng (PR #50). Thông tin công ty, liên hệ, bảo hành, đổi trả, giao hàng chỉ ghi ở `2_Knowledge_Du_lieu_tham_chieu_HLB.md` mục 1, 1.1.

## Đọc gì trước

| Việc | File |
|---|---|
| Quy tắc chung cho mọi phiên | `CLAUDE.md` |
| Quy trình viết bài, giọng văn, quy tắc dữ liệu (bản gốc, Project settings chỉ trỏ về đây) | `1_Project_Instructions_Auto_Blog_HLB.md` |
| Dữ liệu tham chiếu: công ty, chính sách, URL danh mục, chuẩn SEO | `2_Knowledge_Du_lieu_tham_chieu_HLB.md` |
| Danh sách file, việc dở, lịch sử thay đổi quy tắc | `0_TONG_HOP_DU_AN_AI_AGENT_HLB.md` |
| Quy trình Agent điều phối | `DIEU_PHOI.md`, rồi `dieu_phoi/TRANG_THAI.md` |
| Viết nội dung danh mục sản phẩm | `6_Agent_Danh_muc_HLB.md` |

## Cấu trúc thư mục

| Đường dẫn | Nội dung |
|---|---|
| `0_` đến `6_*.md` | Tổng hợp dự án, Project Instructions, Knowledge, bảng hỏi thông tin cố định, hồ sơ agent đánh giá, quy tắc Agent Danh mục |
| `CLAUDE.md`, `DIEU_PHOI.md` | Quy tắc chung, quy trình điều phối |
| `quy_tac_cham.md`, `checklist_cham_bai.md` | Thang chấm và checklist bài blog |
| `quy_tac_cham_danh_muc.md`, `checklist_cham_danh_muc.md` | Thang chấm và checklist nội dung danh mục |
| `Bai_<slug>.md` | Bài blog (phần A, B, C) |
| `DM_<slug>.md` | Nội dung danh mục sản phẩm |
| `du_lieu_san_pham_HLB_<ngày>.csv` | Thông số, giá 113 sản phẩm đọc từ website. Làm mới bằng `tools/lam_moi_csv.py` |
| `tieu_chuan_da_kiem.csv` | Tiêu chuẩn kỹ thuật đã kiểm nguồn |
| `.claude/agents/` | 5 agent con (xem mục dưới) |
| `.claude/settings.json` | Quyền lệnh và hook (chặn đăng khi chưa có phiếu ĐẠT, nhắc chấm lại) |
| `.danh_gia/` | Phiếu duyệt từng bài, nhật ký chấm `nhat_ky.jsonl` (chỉ thêm, không ghi đè) |
| `nghien_cuu/<bài>/` | Kết quả SERP, outline đã chốt, văn bản bài top để kiểm trùng |
| `anh/<bài>/` | Ảnh của bài, `anh.json` (trạng thái duyệt), `ve_so_do.py` |
| `danh_muc/` | Dữ liệu danh mục đã đọc từ website |
| `dieu_phoi/` | Trạng thái điều phối, mã nguồn Bảng điều phối, script đưa bài, ảnh, điểm lên bảng, đối chiếu bảng |
| `quy_trinh/` | Quy trình đọc khi cần: chạy trên máy, nhật ký chấm, ảnh, đăng bản nháp |
| `tools/` | Script Python (xem mục Công cụ) |

## Các agent

Mô hình phòng ban: người dùng giao việc qua Bảng điều phối, **Agent điều phối** là trưởng phòng. Trưởng phòng đọc bảng, giao việc cho agent con, kiểm kết quả, ghi bảng, commit, đăng bản nháp. Trưởng phòng không tự viết bài.

| Agent | Việc | Model |
|---|---|---|
| `agent-blog` | Bài blog: `nghien-cuu` (SERP + outline 9 mục), `viet`, `sua` | sonnet |
| `agent-danh-muc` | Nội dung danh mục: `nghien-cuu` (outline 7 mục), `viet`, `sua` | sonnet |
| `danh-gia-noi-dung` | Chấm bài blog 100 điểm, ngưỡng ĐẠT 95, ghi phiếu, không sửa bài | sonnet |
| `danh-gia-danh-muc` | Chấm nội dung danh mục, ngưỡng ĐẠT 95 (dùng opus vì nội dung lên công khai ngay) | opus |
| `tao-anh` | Ảnh: ảnh sản phẩm thật, sơ đồ vẽ Python, ảnh minh họa Canva | haiku |

Mỗi agent có `memory: project`, ghi nhớ ở `.claude/agent-memory/<tên>/`. Phiên không gọi được agent theo tên thì gọi `general-purpose`, yêu cầu đọc và làm đúng `.claude/agents/<tên>.md`, truyền `model` đúng như file.

## Luồng một bài

1. Người dùng nạp nhóm từ khóa trên bảng. Một nhóm là một bài, dòng đầu là từ khóa chính, các dòng sau là từ khóa phụ.
2. Agent nghiên cứu SERP, lập outline. Người dùng duyệt SERP và outline một lần trên bảng. Bấm "Duyệt outline" là đồng ý viết và đăng bản nháp khi bài ĐẠT.
3. Agent viết bài, rồi chạy vòng duyệt tự động: chấm, sửa, chấm lại, tối đa 3 vòng (`CLAUDE.md` mục Vòng duyệt tự động).
4. Bài ĐẠT thì đẩy bản nháp lên WordPress. Nội dung danh mục lên Trang nháp để xem trước.
5. Người dùng bấm "Duyệt bài" thì agent tạo ảnh, đưa lên tab Kiểm duyệt hình ảnh.
6. Ảnh duyệt xong, agent chèn ảnh vào bản nháp, kiểm lần cuối, chuyển `san_sang_dang`. Người dùng tự đăng.

Trạng thái chi tiết (`moi`, `cho_duyet_outline`, `cho_viet`, `cho_tao_anh`, `cho_hoan_thien`, `can_xu_ly`, `tam_dung`...) ở `DIEU_PHOI.md` mục 3.

## Bảng điều phối

https://claude.ai/artifact/57apPM1U3HKFqe2PVvFsXM, mã nguồn ở `dieu_phoi/bang-dieu-phoi.html`. Bốn tab: Tổng quan, Trung tâm Agent, Kiểm duyệt hình ảnh, Lịch sử chấm điểm.

- Người dùng nạp từ khóa, duyệt outline, duyệt bài, duyệt ảnh, tạm dừng, xóa ngay trên bảng.
- Agent điều phối và agent con chỉ ghi kết quả, câu hỏi lên bảng, không nhắn trong chat (chốt 29/10, 30/10/2026).
- Lịch chạy tự động đang tắt (chốt 09/11/2026). Agent chạy khi người dùng thao tác trên bảng; nút "Gọi lại Agent" chỉ hiện khi một từ khóa quá hạn.
- Cuối mỗi vòng duyệt chạy `python dieu_phoi/doi_chieu_bang.py` để bảng khớp repo (`quy_trinh/nhat_ky_cham_va_bang.md`).

## Chạy trên máy Windows và cloud

GitHub (`haledcoai/hlb-agent`, nhánh `main`) là bản gốc. Folder `AI Agent denlednhaxuong` trên máy Windows là bản clone của `main`. Không chép file tay giữa máy và repo.

Phiên trên máy làm ba việc (`CLAUDE.md` mục Chạy trên máy):

1. **Đầu lượt:** `git pull` trên `main`. Còn thay đổi chưa commit thì commit và push trước, không xóa.
2. **Cuối lượt:** commit và push ngay khi xong việc, kể cả khi dừng giữa chừng. Push bị từ chối thì `git pull --rebase` rồi push lại; gặp xung đột thì dừng, báo người dùng.
3. **Không làm cùng bài với cloud:** kiểm tra và ghi `khoa_luc` trên bảng trước khi làm một từ khóa.

Cài đặt máy (`quy_trinh/chay_tren_may.md`):

- `git config core.autocrlf false` để file giữ xuống dòng LF, không thì mã kiểm tra của phiếu duyệt lệch.
- Python 3, cài thêm `Pillow`, `matplotlib`.
- Giờ Việt Nam lấy bằng `TZ=UTC-7 date -Iseconds`.

Biến môi trường (script đọc `os.environ`, không đọc file `.env`):

| Biến | Dùng cho |
|---|---|
| `WP_USER`, `WP_APP_PASSWORD` | Đăng nhập WordPress REST API (`tools/HUONG_DAN_DANG_NHAP.md`) |
| `SERPAPI_KEY` | Nghiên cứu SERP |
| `PIXABAY_API_KEY` | Ảnh kho Pixabay |

Trên Windows đặt bằng `setx TEN "giá trị"`, rồi mở lại Claude Code. Trên cloud, các biến đặt trong environment "HLB Agent", setup script để trống.

## Công cụ

| Lệnh | Việc |
|---|---|
| `python tools/kiem_tra_bai.py <file.md>` | Kiểm lỗi cơ học (dấu gạch, từ cấm, link, độ dài SEO, thông số so với CSV). Phải về 0 lỗi |
| `python tools/phieu_duyet.py ...` | Phiếu duyệt, nhật ký chấm, hook. Lệnh `ghi` chỉ agent đánh giá được chạy |
| `python tools/nghien_cuu.py luu-outline ...` | Lưu outline đã chốt và bài top SERP để kiểm heading, kiểm trùng |
| `python tools/wp_draft.py <file.md> --new` hoặc `--update <ID>` | Xem trước bản nháp; thêm `--post` để đưa lên WordPress (chỉ khi có phiếu ĐẠT) |
| `python tools/danh_muc.py ds, tim, doc, nhap, ap-dung` | Đọc danh mục, đưa Trang nháp (`ap-dung` chỉ in phần cần chép, không ghi lên danh mục) |
| `python tools/tao_anh.py ...` | Liệt kê chỗ [ẢNH], lấy ảnh sản phẩm, chuẩn hóa JPG (rộng 800-850 px, cao 400-800 px, tối đa 200 KB), ghi `anh.json`, kiểm đủ ảnh |
| `tools/mau_anh.py` | Thư viện mẫu sơ đồ dùng chung |
| `python tools/lam_moi_csv.py` | Làm mới CSV sản phẩm từ website |

## Quy tắc chính

- Không bịa thông số, giá, chứng nhận, bảo hành, dự án. Thiếu dữ liệu thì ghi `[CẦN BỔ SUNG: ...]`. Quá 5 chỗ ở phần B thì không đăng nháp.
- So sánh công bằng, không nói xấu thương hiệu nào, không kết luận hãng nào "tốt nhất".
- Không link về haledco.com.
- Bám đúng outline đã chốt. Heading lệch outline hoặc đoạn trùng bài top SERP là lỗi.
- Không dùng em dash, không emoji trong bài.
- Mọi bài chỉ là bản nháp. `wp_draft.py --post` chỉ chạy khi bài có phiếu ĐẠT; agent không bao giờ dùng `--bo-qua-phieu`.
- Nội dung danh mục chỉ để ở Trang nháp, Agent không ghi lên danh mục (người dùng chốt 26/11/2026).
- Ảnh tải lên Media là công khai ngay. Chỉ ảnh `trang_thai: "duyet"` trong `anh.json` được chèn vào bài. Tên file ảnh không trùng slug bài hay slug đã có trên website.
- Đổi quy tắc thì sửa file trong repo, không sửa Project settings. Lịch sử thay đổi ghi ở `0_TONG_HOP_DU_AN_AI_AGENT_HLB.md` mục 8.
