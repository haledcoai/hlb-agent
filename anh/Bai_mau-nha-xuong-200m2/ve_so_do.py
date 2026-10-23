"""Ve so do bo tri den cho bai mau-nha-xuong-200m2: hai truong hop tren mat bang 10 x 20 m.
So lieu theo bai: TH1 BUFO4-50, luoi 3 x 7 = 21 den, 300 lux, tran 5 m; TH2 BUFO4-100, luoi 2 x 3 = 6 den, 150 lux, tran 7-8 m.
Chay: python anh/Bai_mau-nha-xuong-200m2/ve_so_do.py
"""
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "tools"))
from mau_anh import AMBER, GRAY, LIGHT, NAVY, Circle, Rectangle, chan_trang, hinh, luu, so_vn, tieu_de  # noqa: E402


def mat_bang(ax, so_cot, so_hang, ten, chi_tiet):
    dai, rong = 20, 10
    kc_dai, kc_rong = dai / so_cot, rong / so_hang
    ax.set_xlim(-2.2, dai + 0.8)
    ax.set_ylim(-3.6, rong + 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), dai, rong, fc=LIGHT, ec=NAVY, lw=2))
    for i in range(so_cot):
        for j in range(so_hang):
            x, y = kc_dai / 2 + i * kc_dai, kc_rong / 2 + j * kc_rong
            ax.add_patch(Circle((x, y), 0.95, fc=AMBER, alpha=0.18, ec="none"))
            ax.add_patch(Circle((x, y), 0.42, fc=AMBER, ec=NAVY, lw=1))
    ax.annotate("", (0, -0.9), (dai, -0.9), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
    ax.text(dai / 2, -2.3, "20 m", ha="center", fontsize=11, color=GRAY, weight="bold")
    ax.annotate("", (-0.9, 0), (-0.9, rong), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
    ax.text(-1.9, rong / 2, "10 m", va="center", rotation=90, fontsize=11, color=GRAY, weight="bold")
    ax.text(dai / 2, rong + 2.4, ten, ha="center", fontsize=12, weight="bold", color=NAVY)
    ax.text(dai / 2, rong + 0.9, chi_tiet, ha="center", fontsize=10, color=GRAY)


if __name__ == "__main__":
    fig = hinh(4.6)
    tieu_de(fig, "Sơ đồ bố trí đèn cho mẫu nhà xưởng 200m2 (10 x 20 m)")
    mat_bang(fig.add_axes([0.02, 0.12, 0.47, 0.7]), 7, 3, "Xưởng trần 5 m: 21 đèn 50W",
             "Lưới 3 x 7, BUFO4-50, mục tiêu 300 lux")
    mat_bang(fig.add_axes([0.51, 0.12, 0.47, 0.7]), 3, 2, "Kho trần 7-8 m: 6 đèn 100W",
             "Lưới 2 x 3, BUFO4-100, mục tiêu 150 lux")
    chan_trang(fig, "Sơ đồ ước lượng ban đầu. Vị trí chính xác cần tính bằng DIALux theo mặt bằng thực tế.")
    luu(fig, OUT, "so-do-bo-tri-den-nha-xuong-200m2.jpg")
