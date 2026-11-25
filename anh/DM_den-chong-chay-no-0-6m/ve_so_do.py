"""Ve 3 hinh cho danh muc den-chong-chay-no-0-6m bang mau trong tools/mau_anh.py.
Chi dung so lieu co trong bai DM_den-chong-chay-no-0-6m.md (bang chon loai theo chieu cao, ky hieu Ex, 0,6 m / 1,2 m).
Khong ve mau san pham cu the, khong them thong so.
Chay: python anh/DM_den-chong-chay-no-0-6m/ve_so_do.py
"""
import os
import sys
import textwrap

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "tools"))
from mau_anh import hinh, tieu_de, chan_trang, luu, NAVY, AMBER, GRAY, LIGHT  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402


def so_do_chon_theo_chieu_cao():
    """Thanh tren moi dong: khoang chieu cao lap thuong gap cua khu, theo bang trong bai."""
    fig = hinh(5.2)
    h = fig.get_figheight()
    ax = fig.add_axes([0.03, 0.5 / h, 0.94, (h - 1.9) / h])
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-1.5, 4.7)
    ax.axis("off")

    def x(m):
        return 3.2 + m * 0.6  # truc chieu cao 0-8 m nam ben phai nhan

    rows = [
        ("Tủ, gian kỹ thuật hẹp, gầm kệ", "Loại đơn hoặc đôi 0,6 m", 0, 2.5, "Dưới 2,5 m"),
        ("Hành lang, lối đi, phòng ắc quy", "Loại đơn", 2.5, 3.5, "2,5-3,5 m"),
        ("Phòng pha chế, kho kệ thấp", "Loại đôi, đọc kỹ nhãn", 2.5, 3.5, "2,5-3,5 m"),
        ("Kho hóa chất, kho sơn rộng", "Chuyển sang bộ 1,2 m", 3, 6, "3-6 m"),
        ("Nhà xưởng, kho cao", "Xem đèn highbay chống nổ", 6, 8, "Trên 6 m"),
    ]
    for i, (nhan, goi_y, a, b, khoang) in enumerate(rows):
        yc = 4 - i
        ax.text(0.1, yc + 0.18, nhan, fontsize=10.5, weight="bold", color=NAVY, va="center")
        ax.text(0.1, yc - 0.2, goi_y, fontsize=10.5, color=GRAY, va="center")
        ax.add_patch(Rectangle((x(a), yc - 0.22), x(b) - x(a), 0.44, fc=AMBER, ec=NAVY, lw=1.2))
        ax.text(x(a), yc + 0.33, khoang, fontsize=10, color=GRAY, va="center")

    ax.plot([x(0), x(8)], [-0.5, -0.5], color=GRAY, lw=1)
    for m, chu in [(0, "0 m"), (2.5, "2,5 m"), (3.5, "3,5 m"), (6, "6 m")]:
        ax.plot([x(m), x(m)], [-0.5, -0.35], color=GRAY, lw=1)
        ax.text(x(m), -0.75, chu, ha="center", va="center", fontsize=10, color=GRAY)
    ax.text(x(4), -1.2, "Chiều cao lắp đặt", ha="center", va="center", fontsize=10.5, color=GRAY)

    tieu_de(fig, "Chọn đèn 0,6 m theo chiều cao lắp", "Mỗi thanh là khoảng chiều cao thường gặp của khu lắp đặt")
    chan_trang(fig, "Kinh nghiệm tư vấn, không phải quy định bắt buộc. Số bộ tính theo độ rọi và diện tích.")
    return fig


def so_do_ky_hieu_ex():
    """Cau truc nhan Ex va cac ky hieu thuong gap, theo muc 'Kiem tra ky hieu Ex' cua bai."""
    fig = hinh(5.0)
    h = fig.get_figheight()
    ax = fig.add_axes([0.03, 0.5 / h, 0.94, (h - 1.9) / h])
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-0.3, 4.9)
    ax.axis("off")

    rows = [
        ("Kiểu bảo vệ", "d, e, m",
         "d: vỏ chịu nổ. e: tăng cường an toàn. m: bọc kín bằng nhựa đúc."),
        ("Nhóm khí", "IIA, IIB, IIC",
         "IIC khắt khe nhất (nhóm có hydro, axetylen). Đèn IIC dùng được cho khu IIB và IIA."),
        ("Cấp nhiệt độ", "T1 đến T6",
         "Nhiệt độ bề mặt đèn phải thấp hơn nhiệt độ tự bốc cháy của chất có trong khu."),
        ("Mức bảo vệ thiết bị", "Ga, Gb",
         "Gb dùng cho vùng 1 và vùng 2. Ga dùng cho vùng 0."),
        ("Cấp IP", "IP54, IP65",
         "Chống bụi, chống nước. Không thay cho ký hiệu Ex. IP54 chỉ dùng trong nhà."),
    ]
    for i, (nhan, ky_hieu, mo_ta) in enumerate(rows):
        yc = 4 - i * 0.95
        ax.add_patch(FancyBboxPatch((0.1, yc - 0.4), 8.0, 0.8, boxstyle="round,pad=0.02",
                                    fc=LIGHT, ec="none"))
        ax.text(0.35, yc, nhan, fontsize=10.5, weight="bold", color=GRAY, va="center", ha="left")
        ax.text(2.6, yc, ky_hieu, fontsize=12.5, weight="bold", color=NAVY, va="center", ha="left")
        ax.text(4.3, yc, textwrap.fill(mo_ta, 44), fontsize=10, color="#222222", va="center", ha="left")

    tieu_de(fig, "Đọc ký hiệu Ex trên nhãn đèn chống nổ 0,6 m", "Cấu trúc chung của nhãn, không phải nhãn của mẫu cụ thể")
    chan_trang(fig, "Đối chiếu nhãn và giấy chứng nhận Ex của đúng mẫu trước khi đặt mua.")
    return fig


def so_sanh_kich_thuoc():
    """Bo 0,6 m loai don va doi, ve ty le theo chieu dai (1 m = 6 don vi). Bo 1,2 m net dut de so sanh."""
    fig = hinh(5.0)
    h = fig.get_figheight()
    ax = fig.add_axes([0.03, 0.5 / h, 0.94, (h - 1.9) / h])
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-0.6, 4.8)
    ax.axis("off")

    x0, dai_06, dai_12, cao_bo = 0.5, 3.6, 7.2, 0.7

    def bo(y, so_bong, nhan):
        ax.add_patch(FancyBboxPatch((x0, y - cao_bo / 2), dai_06, cao_bo,
                                    boxstyle="round,pad=0,rounding_size=0.15", fc="white", ec=NAVY, lw=2))
        for k in range(so_bong):
            yk = y + (k - (so_bong - 1) / 2) * 0.26
            ax.add_patch(Rectangle((x0 + 0.3, yk - 0.08), dai_06 - 0.6, 0.16, fc=AMBER, ec="none"))
        ax.text(x0, y + cao_bo / 2 + 0.22, nhan, fontsize=12, weight="bold", color=NAVY, va="bottom")
        ax.text(x0 + dai_06 + 0.25, y, "0,6 m", fontsize=11, color=GRAY, va="center")

    bo(3.6, 1, "Loại đơn: 1 bóng")
    bo(2.1, 2, "Loại đôi: 2 bóng")

    ax.add_patch(Rectangle((x0, 0.2 - cao_bo / 2), dai_12, cao_bo, fc="none", ec=GRAY, lw=1.5, ls="--"))
    ax.text(x0, 0.2 + cao_bo / 2 + 0.22, "Bộ 1,2 m (để so sánh)", fontsize=10.5, color=GRAY, va="bottom")

    tieu_de(fig, "Bộ 0,6 m loại đơn và loại đôi so với bộ 1,2 m", "Hình tỷ lệ theo chiều dài, không vẽ đúng từng mẫu")
    chan_trang(fig, "Minh họa, không phải ảnh sản phẩm. Thông số từng mẫu xem trên nhãn và trang sản phẩm.")
    return fig


if __name__ == "__main__":
    luu(so_do_chon_theo_chieu_cao(), OUT, "so-do-chon-bo-den-chong-no-don-doi-6-tac.jpg")
    luu(so_do_ky_hieu_ex(), OUT, "cach-doc-ky-hieu-ex-tren-nhan-den-tuyp-6-tac.jpg")
    luu(so_sanh_kich_thuoc(), OUT, "bo-den-chong-no-tuyp-6-tac-don-va-doi-canh-nhau.jpg")
