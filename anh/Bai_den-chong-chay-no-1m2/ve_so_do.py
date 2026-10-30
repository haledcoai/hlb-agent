"""Ve so do, anh ghep cho bai den-chong-chay-no-1m2 bang tools/mau_anh.py.
So lieu lay dung theo bai (Bai_den-chong-chay-no-1m2.md). Anh ghep dung anh bai cu 3904 tren website.
Chay: python anh/Bai_den-chong-chay-no-1m2/ve_so_do.py [ten file ...]   (khong truyen ten thi ve tat ca)
"""
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "tools"))
from mau_anh import (AMBER, AMBER_DAM, CHU, GRAY, LIGHT, NAVY, RONG_IN, chan_trang, hinh,  # noqa: E402
                     luu, tieu_de, _mui_ten)
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle  # noqa: E402
import matplotlib.image as mpimg  # noqa: E402

GOC = os.path.join(OUT, "_goc")
MINH_HOA = "Hình vẽ minh họa, không theo tỷ lệ, không phải sản phẩm của một hãng cụ thể."
XAM_THAN, XANH_KINH = "#9aa3ad", "#dbe9f4"


def truc(fig, trai=0.0, duoi=0.0, rong=1.0, cao=1.0):
    h = fig.get_figheight()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, RONG_IN)
    ax.set_ylim(0, h)
    ax.axis("off")
    return ax, h


def nhan(ax, x, y, chu, co=11, mau=NAVY, dam=True, **kw):
    ax.text(x, y, chu, fontsize=co, color=mau, weight="bold" if dam else "normal", **kw)


def bo_den(ax, x, y, dai, so_bong=2, cao=0.42, dau_cap=True):
    """Ve nhin ngang mot bo den chong no 1m2: than, kinh, bong, dau cap."""
    ax.add_patch(FancyBboxPatch((x, y), dai, cao, boxstyle="round,pad=0,rounding_size=0.06", fc=XAM_THAN, ec=NAVY, lw=1.4))
    ax.add_patch(Rectangle((x + 0.18, y + 0.07), dai - 0.36, cao - 0.14, fc=XANH_KINH, ec=NAVY, lw=0.8))
    for i in range(so_bong):
        yy = y + cao * (i + 1) / (so_bong + 1)
        ax.plot([x + 0.24, x + dai - 0.24], [yy, yy], color=AMBER, lw=4, solid_capstyle="round")
    if dau_cap:
        ax.add_patch(Rectangle((x + dai, y + cao / 2 - 0.08), 0.16, 0.16, fc=GRAY, ec=NAVY, lw=1))
        ax.plot([x + dai + 0.16, x + dai + 0.45], [y + cao / 2, y + cao / 2], color="#333333", lw=2.2)


# 1. Don va doi (ghep anh bai cu)
def don_doi():
    fig = hinh(4.6)
    ax, h = truc(fig)
    for (f, x, ten, mo) in [("den-tuyp-led-chong-chay-no-bong-don-hang-philips.jpg", 0.3, "Loại đơn: 1 bóng",
                             "Hành lang, phòng nhỏ, trạm bơm"),
                            ("den-tuyp-led-chong-chay-no-1m2-bong-doi.jpg", 4.2, "Loại đôi: 2 bóng",
                             "Kho có kệ, phòng pha chế")]:
        img = mpimg.imread(os.path.join(GOC, f))
        a = fig.add_axes([x / RONG_IN, 0.85 / h, 3.7 / RONG_IN, 2.75 / h])
        a.imshow(img)
        a.axis("off")
        ax.text(x + 1.85, 3.7, ten, ha="center", fontsize=13, weight="bold", color=NAVY)
        ax.text(x + 1.85, 0.62, mo, ha="center", fontsize=10.5, color=CHU)
    ax.plot([4.1, 4.1], [0.9, 3.6], color=LIGHT, lw=2)
    tieu_de(fig, "Đèn chống cháy nổ 1m2 loại đơn và loại đôi")
    chan_trang(fig, "Ảnh sản phẩm từ bài cũ trên website, dùng để so sánh hình dáng.")
    return fig


# 2. Bong LED va huynh quang
def led_huynh_quang():
    fig = hinh(4.8)
    ax, h = truc(fig)
    cot = [(0.35, "Bóng tuýp LED 1,2 m", ["Không cần chấn lưu", "Bật sáng ngay", "Không chứa thủy ngân",
                                             "Ít nhiệt tỏa ra trong thân kín"]),
           (4.25, "Bóng huỳnh quang 1,2 m", ["Cần chấn lưu trong máng", "Chứa thủy ngân",
                                               "Tốn điện hơn ở cùng mức sáng",
                                               "Không tự tháo chấn lưu để lắp LED"])]
    for x, ten, y_list in cot:
        ax.add_patch(FancyBboxPatch((x, 0.65), 3.6, 3.25, boxstyle="round,pad=0,rounding_size=0.08", fc=LIGHT, ec="none"))
        ax.text(x + 1.8, 3.6, ten, ha="center", fontsize=13, weight="bold", color=NAVY)
        # bong
        ax.add_patch(FancyBboxPatch((x + 0.3, 2.85), 3.0, 0.26, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc="#fff3d6" if "LED" in ten else "#f4f7fb", ec=NAVY, lw=1.2))
        for dx in (0.18, 3.12):
            ax.plot([x + dx, x + dx + 0.12], [2.94, 2.94], color=GRAY, lw=2)
            ax.plot([x + dx, x + dx + 0.12], [3.02, 3.02], color=GRAY, lw=2)
        if "LED" in ten:
            for i in range(14):
                ax.add_patch(Rectangle((x + 0.45 + i * 0.2, 2.94), 0.09, 0.08, fc=AMBER, ec="none"))
        else:
            ax.add_patch(Rectangle((x + 1.3, 2.3), 1.0, 0.32, fc=GRAY, ec=NAVY, lw=1))
            ax.text(x + 1.8, 2.46, "chấn lưu", ha="center", va="center", fontsize=10, color="white", weight="bold")
            ax.plot([x + 1.8, x + 1.8], [2.62, 2.85], color=NAVY, lw=1)
        for i, d in enumerate(y_list):
            ax.add_patch(Circle((x + 0.42, 1.95 - i * 0.36), 0.05, fc=AMBER if "LED" in ten else GRAY, ec="none"))
            ax.text(x + 0.58, 1.95 - i * 0.36, d, va="center", fontsize=10.5, color=CHU)
    tieu_de(fig, "Bóng tuýp LED và huỳnh quang trong đèn chống cháy nổ 1m2")
    chan_trang(fig, "Mức chênh điện năng tùy model, cần so trên thông số hãng công bố.")
    return fig


# 6. Mang mica thuong va den chong no
def mica_va_chong_no():
    fig = hinh(4.8)
    ax, h = truc(fig)
    # trai: mica
    x = 0.35
    ax.add_patch(FancyBboxPatch((x, 0.65), 3.6, 3.25, boxstyle="round,pad=0,rounding_size=0.08", fc=LIGHT, ec="none"))
    ax.text(x + 1.8, 3.6, "Máng LED mica thường", ha="center", fontsize=13, weight="bold", color=NAVY)
    ax.add_patch(FancyBboxPatch((x + 0.3, 2.6), 3.0, 0.36, boxstyle="round,pad=0,rounding_size=0.16", fc="white", ec=GRAY, lw=1.2))
    ax.plot([x + 0.1, x + 0.3], [2.78, 2.78], color="#333333", lw=1.8)
    for i, d in enumerate(["Vỏ thường, nắp mica", "Dây điện luồn qua lỗ thường",
                           "Không có ký hiệu Ex", "Không dùng ở khu có khí dễ cháy"]):
        ax.add_patch(Circle((x + 0.42, 1.95 - i * 0.36), 0.05, fc=GRAY, ec="none"))
        ax.text(x + 0.58, 1.95 - i * 0.36, d, va="center", fontsize=10.5, color=CHU)
    # phai: chong no
    x = 4.25
    ax.add_patch(FancyBboxPatch((x, 0.65), 3.6, 3.25, boxstyle="round,pad=0,rounding_size=0.08", fc="#fff6e5", ec=AMBER, lw=1.4))
    ax.text(x + 1.8, 3.6, "Đèn chống cháy nổ 1m2", ha="center", fontsize=13, weight="bold", color=NAVY)
    bo_den(ax, x + 0.25, 2.55, 2.85, so_bong=2, cao=0.46)
    for i, d in enumerate(["Thân kim loại, kính chịu lực", "Cáp vào qua đầu cáp chống nổ",
                           "Nhãn có ký hiệu Ex, nhóm khí, cấp T", "Dùng theo vùng nguy hiểm"]):
        ax.add_patch(Circle((x + 0.42, 1.95 - i * 0.36), 0.05, fc=AMBER, ec="none"))
        ax.text(x + 0.58, 1.95 - i * 0.36, d, va="center", fontsize=10.5, color=CHU)
    tieu_de(fig, "Máng LED mica thường và đèn chống cháy nổ 1m2")
    chan_trang(fig, MINH_HOA)
    return fig


# 10. Ky hieu Ex
def ky_hieu_ex():
    fig = hinh(5.4)
    ax, h = truc(fig)
    phan = [("Ex", "Có chứng nhận\ndùng trong\nkhí nổ"),
            ("d", "Kiểu bảo vệ:\nd vỏ chịu nổ,\ne tăng cường\nan toàn, m đúc kín"),
            ("IIB", "Nhóm khí:\nIIA, IIB, IIC\n(IIC khắt khe\nnhất)"),
            ("T4", "Cấp nhiệt độ:\nT1 đến T6\n(T6 bề mặt\nnguội nhất)"),
            ("Gb", "Mức bảo vệ:\nGb dùng cho\nvùng 1, vùng 2")]
    rong = 1.42
    x0 = (RONG_IN - 5 * rong - 4 * 0.1) / 2
    for i, (k, m) in enumerate(phan):
        x = x0 + i * (rong + 0.1)
        ax.add_patch(FancyBboxPatch((x, 3.35), rong, 0.75, boxstyle="round,pad=0,rounding_size=0.08",
                                    fc=NAVY if i % 2 == 0 else AMBER, ec="none"))
        ax.text(x + rong / 2, 3.72, k, ha="center", va="center", fontsize=22, weight="bold", color="white")
        ax.annotate("", (x + rong / 2, 2.75), (x + rong / 2, 3.33), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.3))
        ax.add_patch(FancyBboxPatch((x, 1.3), rong, 1.42, boxstyle="round,pad=0,rounding_size=0.06", fc=LIGHT, ec="none"))
        ax.text(x + rong / 2, 2.62, m, ha="center", va="top", fontsize=9.6, color=CHU, linespacing=1.35)
    ax.text(RONG_IN / 2, 0.85, "Gặp nhãn rút gọn như \"Exd II BT\" (thiếu cấp nhiệt độ): xin bản chứng nhận của model.",
            ha="center", fontsize=10.5, color=AMBER_DAM, weight="bold")
    tieu_de(fig, "Cách đọc ký hiệu Ex trên nhãn đèn chống cháy nổ",
            "Ví dụ minh họa \"Ex d IIB T4 Gb\", không phải nhãn của model cụ thể")
    chan_trang(fig, "Vùng nguy hiểm do đơn vị thiết kế hoặc bộ phận an toàn của nhà máy xác định.")
    return fig


# 12. Bo tri kho 6 x 10 m
def bo_tri_kho():
    fig = hinh(5.4)
    ax, h = truc(fig)
    s = 0.5  # inch / m
    x0, y0 = (RONG_IN - 10 * s) / 2, 1.0
    ax.add_patch(Rectangle((x0, y0), 10 * s, 6 * s, fc=LIGHT, ec=NAVY, lw=2))
    xs = [10 / 6 + i * 10 / 3 for i in range(3)]
    for xm in xs:
        cx, cy = x0 + xm * s, y0 + 3 * s
        ax.add_patch(Circle((cx, cy), 1.0, fc=AMBER, alpha=0.15, ec="none"))
        ax.add_patch(Rectangle((cx - 0.6 * s, cy - 0.1), 1.2 * s, 0.2, fc=NAVY, ec=AMBER, lw=1.2))
    _mui_ten(ax, (x0, y0 - 0.25), (x0 + 10 * s, y0 - 0.25))
    ax.text(x0 + 5 * s, y0 - 0.55, "10 m", ha="center", fontsize=12, weight="bold", color=GRAY)
    _mui_ten(ax, (x0 - 0.25, y0), (x0 - 0.25, y0 + 6 * s))
    ax.text(x0 - 0.55, y0 + 3 * s, "6 m", rotation=90, va="center", ha="center", fontsize=12, weight="bold", color=GRAY)
    _mui_ten(ax, (x0 + xs[0] * s, y0 + 6 * s + 0.2), (x0 + xs[1] * s, y0 + 6 * s + 0.2), NAVY)
    ax.text(x0 + (xs[0] + xs[1]) / 2 * s, y0 + 6 * s + 0.3, "khoảng 3,3 m", ha="center", fontsize=10.5, weight="bold", color=NAVY)
    ax.text(x0 + 10 * s + 0.2, y0 + 3 * s + 0.75, "3 bộ đôi\nHLEP TL2-60", fontsize=10.5, weight="bold", color=NAVY, va="center")
    ax.text(x0 + 10 * s + 0.2, y0 + 3 * s - 0.45, "Tổng 180W\n3 W/m²", fontsize=10.5, color=CHU, va="center")
    tieu_de(fig, "Bố trí đèn chống cháy nổ 1m2 cho kho hóa chất 6 x 10 m",
            "3 bộ đôi 60W (7.800 lm) theo 1 hàng giữa kho, trần 4 m, độ rọi giả định 200 lux")
    chan_trang(fig, "Sơ đồ ước lượng ban đầu. Vị trí chính xác cần tính bằng DIALux theo mặt bằng thực tế.")
    return fig


# 14. Cac phan tinh gia
def cac_phan_gia():
    fig = hinh(5.0)
    ax, h = truc(fig)
    # may
    ax.add_patch(FancyBboxPatch((0.5, 2.9), 4.2, 0.6, boxstyle="round,pad=0,rounding_size=0.08", fc=XAM_THAN, ec=NAVY, lw=1.4))
    ax.add_patch(Rectangle((0.7, 2.98), 3.8, 0.44, fc=XANH_KINH, ec=NAVY, lw=0.8))
    ax.text(5.0, 3.2, "1. Máng (thân, kính)", va="center", fontsize=11.5, weight="bold", color=NAVY)
    # bong
    for yy in (2.35, 2.05):
        ax.add_patch(FancyBboxPatch((0.7, yy), 3.8, 0.16, boxstyle="round,pad=0,rounding_size=0.07", fc="#fff3d6", ec=NAVY, lw=1))
    ax.text(5.0, 2.2, "2. Bóng LED (2 bóng với loại đôi)", va="center", fontsize=11.5, weight="bold", color=NAVY)
    # dau cap
    for xx in (1.0, 1.7):
        ax.add_patch(Rectangle((xx, 1.35), 0.35, 0.3, fc=GRAY, ec=NAVY, lw=1))
        ax.add_patch(Rectangle((xx + 0.07, 1.65), 0.21, 0.12, fc=GRAY, ec=NAVY, lw=1))
    ax.add_patch(Circle((2.6, 1.5), 0.13, fc=GRAY, ec=NAVY, lw=1))
    ax.text(5.0, 1.5, "3. Đầu cáp, nút bịt lỗ thừa", va="center", fontsize=11.5, weight="bold", color=NAVY)
    # gia treo
    for xx in (1.0, 3.6):
        ax.plot([xx, xx, xx + 0.5, xx + 0.5], [0.95, 0.75, 0.75, 0.95], color=NAVY, lw=2.2)
    ax.text(5.0, 0.85, "4. Giá treo", va="center", fontsize=11.5, weight="bold", color=NAVY)
    ax.text(RONG_IN / 2, 3.85, "Hỏi rõ báo giá gồm phần nào: có nơi chỉ báo giá máng, chưa gồm bóng",
            ha="center", fontsize=10.5, color=AMBER_DAM, weight="bold")
    tieu_de(fig, "Các phần tính giá của bộ đèn chống cháy nổ 1m2")
    chan_trang(fig, MINH_HOA + " Phụ kiện có thể tính riêng.")
    return fig


VE = {
    "den-chong-no-1m2-don-va-doi-so-sanh.jpg": don_doi,
    "bong-tuyp-led-va-huynh-quang-chong-no-1m2.jpg": led_huynh_quang,
    "den-mang-mica-thuong-canh-den-chong-no-1m2.jpg": mica_va_chong_no,
    "cach-doc-ky-hieu-ex-den-chong-no.jpg": ky_hieu_ex,
    "so-do-bo-tri-den-chong-no-kho-6x10m.jpg": bo_tri_kho,
    "cac-phan-tinh-gia-bo-den-chong-no-1m2.jpg": cac_phan_gia,
}


# ---------- Canh minh hoa (mat cat) ----------

PHONG = []


def khung_phong(ax, x0, x1, y0, cao, nhan_cao):
    """San, tran, tuong mat cat; cao la chieu cao ve (inch). Ghi lai khung de cat vung sang."""
    PHONG[:] = [x0 + 0.1, y0, x1 - x0 - 0.2, cao]
    ax.add_patch(Rectangle((x0, y0 - 0.12), x1 - x0, 0.12, fc=GRAY, ec="none"))
    ax.add_patch(Rectangle((x0, y0 + cao), x1 - x0, 0.1, fc=GRAY, ec="none"))
    for x in (x0, x1 - 0.1):
        ax.add_patch(Rectangle((x, y0), 0.1, cao, fc="#c9d0d8", ec="none"))
    _mui_ten(ax, (x0 - 0.2, y0), (x0 - 0.2, y0 + cao))
    ax.text(x0 - 0.4, y0 + cao / 2, nhan_cao, rotation=90, va="center", ha="center", fontsize=11.5, weight="bold", color=GRAY)


def den_tran(ax, x, y_tran, dai=0.9, treo=0.0, rong_sang=1.4, y_san=0.0, doi=True):
    y = y_tran - treo - 0.16
    if treo:
        for dx in (0.15, dai - 0.15):
            ax.plot([x - dai / 2 + dx] * 2, [y + 0.16, y_tran], color=NAVY, lw=1)
    sang = ax.add_patch(Polygon([(x - dai / 2 + 0.1, y), (x + dai / 2 - 0.1, y), (x + rong_sang / 2, y_san),
                                 (x - rong_sang / 2, y_san)], closed=True, fc=AMBER, alpha=0.16, ec="none"))
    if PHONG:
        sang.set_clip_path(Rectangle(PHONG[:2], PHONG[2], PHONG[3], transform=ax.transData))
    ax.add_patch(FancyBboxPatch((x - dai / 2, y), dai, 0.16, boxstyle="round,pad=0,rounding_size=0.03", fc=XAM_THAN, ec=NAVY, lw=1))
    for i in range(2 if doi else 1):
        yy = y + 0.16 * (i + 1) / (3 if doi else 2)
        ax.plot([x - dai / 2 + 0.08, x + dai / 2 - 0.08], [yy, yy], color=AMBER, lw=2)


def ke(ax, x, y0, rong, cao, tang=4, mau="#7a8899"):
    ax.add_patch(Rectangle((x, y0), 0.05, cao, fc=mau, ec="none"))
    ax.add_patch(Rectangle((x + rong - 0.05, y0), 0.05, cao, fc=mau, ec="none"))
    for i in range(tang):
        y = y0 + 0.1 + i * (cao - 0.1) / tang
        ax.add_patch(Rectangle((x, y), rong, 0.04, fc=mau, ec="none"))
        for j in range(int(rong / 0.22)):
            ax.add_patch(Rectangle((x + 0.08 + j * 0.22, y + 0.04), 0.16, 0.2, fc="#d9a441" if (i + j) % 2 else "#c0c8d2",
                                   ec=NAVY, lw=0.5))


def canh_kho_rang_dong():
    fig = hinh(5.0)
    ax, h = truc(fig)
    x0, x1, y0, cao = 0.9, 7.6, 0.75, 2.85
    khung_phong(ax, x0, x1, y0, cao, "khoảng 4 m")
    for x in (1.3, 3.4, 5.5):
        ke(ax, x, y0, 1.3, 1.7, tang=4)
    for x in (2.95, 5.05, 7.0):
        den_tran(ax, x, y0 + cao, dai=0.8, rong_sang=1.5, y_san=y0, doi=False)
    ax.text(RONG_IN / 2, y0 + cao + 0.32, "Bộ đèn LED chống nổ dài khoảng 1,2 m gắn trần, đặt trên lối đi giữa các kệ",
            ha="center", fontsize=10.5, color=NAVY, weight="bold")
    tieu_de(fig, "Đèn chống cháy nổ 1m2 lắp trong kho có kệ",
            "Mẫu Rạng Đông CN01 1200/40W.PLUS theo trang hãng: 40W, 4.000 lm, IP54 (dùng trong nhà)")
    chan_trang(fig, "Hình vẽ minh họa vị trí lắp, không theo tỷ lệ, không phải ảnh sản phẩm hay công trình thật.")
    return fig


def canh_kho_son():
    fig = hinh(5.0)
    ax, h = truc(fig)
    x0, x1, y0, cao = 0.9, 7.6, 0.75, 3.2
    khung_phong(ax, x0, x1, y0, cao, "khoảng 4 m")
    for x in (1.1, 3.25, 5.4):
        ke(ax, x, y0, 1.5, 2.0, tang=4)
        # thung son
    for x in (2.92, 5.07, 7.1):
        den_tran(ax, x, y0 + cao, dai=0.85, treo=0.35, rong_sang=1.7, y_san=y0, doi=True)
    ax.text(RONG_IN / 2, y0 + cao + 0.32, "Bộ đôi treo trên lối đi để ánh sáng chiếu vào mặt kệ, dễ đọc nhãn thùng",
            ha="center", fontsize=10.5, color=NAVY, weight="bold")
    tieu_de(fig, "Đèn chống nổ 1m2 loại đôi trong kho sơn có kệ hàng")
    chan_trang(fig, "Hình vẽ minh họa, không theo tỷ lệ, không phải sản phẩm Duhal hay công trình thật.")
    return fig


def canh_pha_che():
    fig = hinh(5.0)
    ax, h = truc(fig)
    x0, x1, y0, cao = 0.9, 7.6, 0.75, 2.9
    khung_phong(ax, x0, x1, y0, cao, "3-4 m")
    # ban pha che
    for bx in (1.5, 4.6):
        ax.add_patch(Rectangle((bx, y0 + 0.75), 2.0, 0.08, fc=NAVY, ec="none"))
        for lx in (bx + 0.1, bx + 1.85):
            ax.add_patch(Rectangle((lx, y0), 0.06, 0.75, fc=NAVY, ec="none"))
        for k in range(4):
            ax.add_patch(Rectangle((bx + 0.3 + k * 0.42, y0 + 0.83), 0.22, 0.3 - 0.05 * k, fc="#c0c8d2", ec=NAVY, lw=0.6))
    for x in (2.5, 5.6):
        den_tran(ax, x, y0 + cao, dai=1.0, rong_sang=2.4, y_san=y0, doi=True)
    ax.text(RONG_IN / 2, y0 + cao + 0.32, "Gắn sát trần phẳng ngay trên bàn cân, trộn; thân đèn cần dễ lau chùi",
            ha="center", fontsize=10.5, color=NAVY, weight="bold")
    tieu_de(fig, "Đèn chống nổ 1m2 gắn trần phòng pha chế")
    chan_trang(fig, "Hình vẽ minh họa, không theo tỷ lệ, không phải sản phẩm Paragon hay công trình thật.")
    return fig


def canh_hanh_lang():
    fig = hinh(4.6)
    ax, h = truc(fig)
    x0, x1, y0, y1 = 0.5, 7.7, 1.55, 3.05
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=LIGHT, ec="none"))
    for y in (y0 - 0.5, y1):
        ax.add_patch(Rectangle((x0, y), x1 - x0, 0.5, fc="#c9d0d8", ec=NAVY, lw=1))
    for i in range(5):
        x = x0 + 0.45 + i * 1.45
        ax.add_patch(Rectangle((x, y1), 0.8, 0.5, fc="#e6d3a8", ec=NAVY, lw=1))
        ax.text(x + 0.4, y1 + 0.25, "kho", ha="center", va="center", fontsize=9.6, color=NAVY)
    for i in range(4):
        cx = x0 + 0.9 + i * 1.8
        ax.add_patch(Circle((cx, (y0 + y1) / 2), 0.7, fc=AMBER, alpha=0.15, ec="none"))
        ax.add_patch(Rectangle((cx - 0.35, (y0 + y1) / 2 - 0.07), 0.7, 0.14, fc=NAVY, ec=AMBER, lw=1))
    ax.text(RONG_IN / 2, y0 - 0.8, "Mặt bằng hành lang trần 3-4 m: bộ đơn lắp 1 hàng dọc giữa lối đi",
            ha="center", fontsize=11, color=NAVY, weight="bold")
    tieu_de(fig, "Đèn chống cháy nổ 1m2 loại đơn lắp hành lang kho")
    chan_trang(fig, "Hình vẽ minh họa, không theo tỷ lệ. Số bộ và khoảng cách cần tính theo độ rọi cần đạt.")
    return fig


def canh_tran_cao():
    fig = hinh(5.2)
    ax, h = truc(fig)
    y0, cao = 0.8, 3.0
    khung_phong(ax, 0.75, 3.95, y0, cao, "trên 6 m")
    ax.text(2.35, y0 + cao + 0.3, "Bộ 1m2 ở trần trên 6 m", ha="center", fontsize=12, weight="bold", color=NAVY)
    for i in range(6):
        den_tran(ax, 1.1 + i * 0.5, y0 + cao, dai=0.4, rong_sang=0.9, y_san=y0, doi=True)
    khung_phong(ax, 4.65, 7.85, y0, cao, "trên 6 m")
    ax.text(6.25, y0 + cao + 0.3, "Highbay chống nổ", ha="center", fontsize=12, weight="bold", color=NAVY)
    for x in (5.45, 7.05):
        y = y0 + cao - 0.5
        ax.plot([x, x], [y + 0.3, y0 + cao], color=NAVY, lw=1)
        sang = ax.add_patch(Polygon([(x - 0.25, y + 0.3), (x + 0.25, y + 0.3), (x + 0.95, y0), (x - 0.95, y0)],
                                    closed=True, fc=AMBER, alpha=0.18, ec="none"))
        sang.set_clip_path(Rectangle(PHONG[:2], PHONG[2], PHONG[3], transform=ax.transData))
        ax.add_patch(Polygon([(x - 0.12, y + 0.3), (x + 0.12, y + 0.3), (x + 0.28, y), (x - 0.28, y)], closed=True,
                             fc=XAM_THAN, ec=NAVY, lw=1))
    ax.text(2.35, y0 + 0.35, "Phải lắp dày, tốn đầu cáp\nvà công lắp", ha="center", fontsize=10.5, color=AMBER_DAM,
            weight="bold")
    ax.text(6.25, y0 + 0.35, "Thường hợp hơn cho\nkho, xưởng trần cao", ha="center", fontsize=10.5, color=NAVY,
            weight="bold")
    tieu_de(fig, "Kho trần cao: dùng highbay chống nổ thay đèn 1m2")
    chan_trang(fig, "Hình vẽ minh họa, không theo tỷ lệ. Số bộ chính xác cần tính bằng DIALux.")
    return fig


VE.update({
    "den-chong-no-1m2-rang-dong-lap-kho.jpg": canh_kho_rang_dong,
    "den-chong-no-1m2-lap-kho-son.jpg": canh_kho_son,
    "den-chong-no-1m2-phong-pha-che.jpg": canh_pha_che,
    "den-chong-no-1m2-don-lap-hanh-lang.jpg": canh_hanh_lang,
    "kho-tran-cao-dung-highbay-chong-no.jpg": canh_tran_cao,
})

if __name__ == "__main__":
    for ten in (sys.argv[1:] or list(VE)):
        luu(VE[ten](), OUT, ten)
        print("Đã vẽ", ten)
