"""Ve cac so do va bang cho bai den-chong-chay-no-250w bang mau trong tools/mau_anh.py.
So lieu lay dung theo bai (muc Cach chon, Vi du tinh chon cong suat, Lap dat). Khong them so lieu nao.
Anh kho hoa chat (1) lay tu Unsplash, khong ve lai o day.
Chay: python anh/Bai_den-chong-chay-no-250w/ve_so_do.py
"""
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "tools"))
from mau_anh import (AMBER, DIALUX, GRAY, LIGHT, NAVY, RONG_IN, _mui_ten, bang_ip,  # noqa: E402
                     bang_so_sanh, cac_buoc, chan_trang, hinh, luu, tieu_de)
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle  # noqa: E402


def _truc_inch(h):
    """Truc toa do theo inch, toan khung hinh."""
    fig = hinh(h)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, RONG_IN)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def highbay():
    fig, ax = _truc_inch(4.6)
    ax.add_patch(Rectangle((0, 0), RONG_IN, 0.7, fc=LIGHT, ec="none"))
    ax.text(0.3, 0.35, "Sàn kho", fontsize=10.5, color=GRAY, va="center")
    ax.add_patch(Rectangle((0.3, 3.3), 7.6, 0.15, fc=NAVY, ec="none"))  # kèo thép
    ax.text(0.3, 3.1, "Kèo thép", fontsize=10.5, color=GRAY, va="bottom")
    ax.plot([4.1, 4.1], [3.3, 2.75], color=GRAY, lw=1.5)  # dây treo
    ax.add_patch(FancyBboxPatch((3.0, 1.95), 2.2, 0.8, boxstyle="round,pad=0,rounding_size=0.12", fc=NAVY, ec="none"))
    ax.add_patch(Polygon([(3.2, 1.95), (5.0, 1.95), (7.4, 0.7), (0.8, 0.7)], closed=True, fc=AMBER, alpha=0.22, ec="none"))
    ax.text(5.5, 2.35, "Đèn highbay 250W", fontsize=11, weight="bold", color=NAVY, va="center")
    ax.text(0.3, 1.9, "Chùm sáng xuống sàn", fontsize=10.5, color=NAVY, va="center")
    tieu_de(fig, "Đèn highbay chống cháy nổ 250W treo dưới kèo kho",
            "Minh họa cách treo, không thể hiện model cụ thể")
    chan_trang(fig, "Sơ đồ minh họa. Chọn đèn theo ký hiệu Ex và giấy chứng nhận của đúng model.")
    return fig


def den_pha():
    fig, ax = _truc_inch(4.6)
    ax.add_patch(Rectangle((0, 0), RONG_IN, 0.7, fc=LIGHT, ec="none"))
    ax.add_patch(Rectangle((1.6, 0.7), 0.22, 2.4, fc=GRAY, ec="none"))  # cột thép
    ax.add_patch(Rectangle((1.2, 3.0), 1.1, 0.35, fc=NAVY, ec="none"))  # đèn pha
    ax.add_patch(Polygon([(2.3, 3.3), (2.3, 2.95), (5.5, 1.4), (5.5, 2.7)], closed=True, fc=AMBER, alpha=0.25, ec="none"))
    ax.add_patch(Rectangle((5.6, 0.7), 2.1, 1.6, fc="#dfe6ef", ec=NAVY, lw=1.2))  # bồn chứa
    ax.add_patch(Ellipse((6.65, 2.3), 2.1, 0.45, fc="#eef2f7", ec=NAVY, lw=1.2))
    ax.text(0.15, 2.6, "Đèn pha 250W", fontsize=10.5, weight="bold", color=NAVY, va="center")
    ax.text(0.15, 1.6, "Cột thép", fontsize=10.5, color=GRAY, va="center")
    ax.text(4.9, 3.25, "Chùm sáng hướng vào bồn", fontsize=10.5, color=NAVY, va="center")
    ax.text(6.65, 2.95, "Bồn chứa", fontsize=11, weight="bold", color=NAVY, ha="center", va="center")
    tieu_de(fig, "Đèn pha chống cháy nổ 250W chiếu bồn chứa ngoài trời",
            "Minh họa hướng chiếu đèn pha gắn cột, không thể hiện model cụ thể")
    chan_trang(fig, "Sơ đồ minh họa. Vùng tối sau vật cản cần kiểm tra ngoài thực tế.")
    return fig


def cao_ap_va_led():
    return bang_so_sanh(
        cot=["Tiêu chí (theo ví dụ trong bài)", "Bộ cao áp 250W (bóng truyền thống)", "Đèn LED chống nổ"],
        dong=[
            ["Công suất cả bộ", "280W, gồm chấn lưu (giả định)", "250W"],
            ["Điện năng mỗi tháng (16 giờ/ngày, 26 ngày)", "116,48 kWh", "104 kWh"],
            ["Tuổi thọ nguồn sáng", "Ngắn hơn bóng LED", "Dài hơn bóng cao áp"],
        ],
        tieu_de_anh="Bộ đèn chống nổ bóng cao áp 250W và đèn LED thay thế",
        phu_de="Số liệu là ví dụ tính trong bài, không phải số công bố của hãng",
        ghi_chu="Đèn LED 250W dùng để so sánh cùng công suất. Thay bằng LED công suất thấp hơn cần kiểm độ rọi.",
    )


def ky_hieu_ex():
    return bang_so_sanh(
        cot=["Phần ký hiệu", "Ý nghĩa"],
        dong=[
            ["Ex", "Thiết bị có chứng nhận dùng trong môi trường khí nổ"],
            ["d", "Kiểu bảo vệ: vỏ chịu nổ, nếu có cháy bên trong thì vỏ giữ lửa không lan ra ngoài. Khác: e là tăng cường an toàn, m là đúc kín"],
            ["IIB", "Nhóm khí: IIA, IIB, IIC. IIC khắt khe nhất, đèn IIC dùng được cho khu IIB và IIA"],
            ["T4", "Cấp nhiệt độ (T1 đến T6): nhiệt độ bề mặt cao nhất của đèn, phải thấp hơn nhiệt độ tự bốc cháy của chất trong khu"],
            ["Gb", "Mức bảo vệ thiết bị: cho biết đèn dùng được ở vùng nào"],
        ],
        tieu_de_anh="Cách đọc ký hiệu Ex trên nhãn đèn chống cháy nổ",
        phu_de='Ví dụ "Ex d IIB T4 Gb", minh họa, không phải nhãn của model cụ thể',
        ghi_chu="Bảng đầy đủ các ký hiệu xem bài tiêu chuẩn đèn chống cháy nổ.",
    )


def mat_bang_kho():
    """Kho 20 x 30 m, 7 bo den 250W xep so le thanh hai hang (4 + 3)."""
    dai, rong = 30, 20
    fig = hinh(5.2)
    h = fig.get_figheight()
    ax = fig.add_axes([0.04, 0.5 / h, 0.92, 1 - 1.75 / h])
    ax.set_xlim(-5, dai + 5)
    ax.set_ylim(-5, rong + 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), dai, rong, fc=LIGHT, ec=NAVY, lw=2))
    vi_tri = [(3.75, 6.67), (11.25, 6.67), (18.75, 6.67), (26.25, 6.67),
              (7.5, 13.33), (15, 13.33), (22.5, 13.33)]
    for x, y in vi_tri:
        ax.add_patch(Circle((x, y), 1.9, fc=AMBER, alpha=0.18, ec="none"))
        ax.add_patch(Circle((x, y), 0.6, fc=AMBER, ec=NAVY, lw=1))
    _mui_ten(ax, (0, -2), (dai, -2))
    ax.text(dai / 2, -3.6, "30 m", ha="center", fontsize=12, color=GRAY, weight="bold")
    _mui_ten(ax, (-2, 0), (-2, rong))
    ax.text(-3.6, rong / 2, "20 m", va="center", ha="center", rotation=90, fontsize=12, color=GRAY, weight="bold")
    tieu_de(fig, "Sơ đồ bố trí 7 bộ đèn chống cháy nổ 250W trong kho 20 x 30 m",
            "Hai hàng so le, tổng 1.750W. Mỗi bộ 250W, quang thông giả định")
    chan_trang(fig, DIALUX)
    return fig


def ip65():
    return bang_ip(
        cap="65",
        tieu_de_anh="Cấp bảo vệ IP65 của vỏ đèn chống cháy nổ",
        ghi_chu="IP65: kín bụi hoàn toàn và chịu được tia nước. Theo TCVN 4255:2025, dựa trên IEC 60529.",
    )


def bang_hoi_ncc():
    return bang_so_sanh(
        cot=["Nên hỏi", "Vì sao", "SH-HB5-250SMD", "SH-FL1EX-250W"],
        dong=[
            ["Ký hiệu Ex đúng model", "Khớp vùng nguy hiểm", "Chưa công bố", "Chưa công bố"],
            ["Bản sao giấy chứng nhận", "Chứng minh ghi đúng model", "Chưa công bố", "Chưa công bố"],
            ["Quang thông (lm)", "Tính số bộ cần dùng", "Chưa công bố", "Chưa công bố"],
            ["Cấp IP", "Hợp bụi, nước", "IP65", "IP65"],
            ["Bảo hành", "So sánh giữa các nhà cung cấp", "24 tháng", "24 tháng"],
            ["Giá", "So sánh báo giá", '"Liên hệ"', '"Liên hệ"'],
            ["Thời gian giao", "Lên kế hoạch lắp", "Hỏi nhà cung cấp", "Hỏi nhà cung cấp"],
        ],
        tieu_de_anh="Hỏi nhà cung cấp trước khi mua đèn chống nổ 250W",
        phu_de="Cột Soho: thông tin trên trang bán hàng đọc ngày 25/11/2026",
        ghi_chu="Chưa công bố: trang bán hàng không ghi. Hỏi nhà cung cấp trước khi đặt hàng.",
    )


def cac_buoc_lap():
    return cac_buoc(
        buoc=[
            ("Ngắt nguồn và khóa cầu dao", "Khóa cầu dao của mạch đèn, treo biển cảnh báo trước khi làm việc."),
            ("Chọn đầu cáp đúng cỡ", "Đầu cáp chống nổ đúng cỡ cáp. Lỗ thừa trên thân bịt bằng nút bịt chống nổ."),
            ("Siết đầu cáp đủ chặt", "Siết chặt trước khi đóng nắp. Không dùng băng keo hay silicone thay nút bịt."),
            ("Kiểm tra trước khi cấp điện", "Gá treo chắc chắn, đóng nắp đúng rồi mới cấp điện."),
        ],
        tieu_de_anh="Lắp đèn chống cháy nổ 250W: siết đầu cáp trước khi đóng nắp",
        phu_de="Thợ điện có chuyên môn về thiết bị chống nổ thực hiện",
        canh_bao=(1, 3),
        ghi_chu="Bước có ô vàng là lưu ý an toàn. Làm việc trên cao có người giữ thang.",
    )


if __name__ == "__main__":
    luu(highbay(), OUT, "den-highbay-chong-chay-no-250w-kho-hoa-chat.jpg")
    luu(den_pha(), OUT, "den-pha-chong-chay-no-250w-chieu-bon-be.jpg")
    luu(cao_ap_va_led(), OUT, "bo-den-cao-ap-chong-no-va-den-led-thay-the.jpg")
    luu(ky_hieu_ex(), OUT, "cach-doc-ky-hieu-ex-tren-nhan-den-chong-no.jpg")
    luu(ip65(), OUT, "cap-bao-ve-ip65-vo-den-chong-no.jpg")
    luu(mat_bang_kho(), OUT, "so-do-bo-tri-7-den-chong-no-kho-20x30m.jpg")
    luu(bang_hoi_ncc(), OUT, "bang-kiem-hoi-nha-cung-cap-den-chong-no-250w.jpg")
    luu(cac_buoc_lap(), OUT, "siet-dau-cap-khi-lap-den-chong-no-250w.jpg")
