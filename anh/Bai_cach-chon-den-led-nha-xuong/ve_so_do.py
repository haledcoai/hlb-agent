"""Ve 2 so do cho bai cach-chon-den-led-nha-xuong. So lieu lay dung theo bai va Knowledge muc 6.
Kho 8,2 inch, dpi 200 (1640 px), tao_anh.py chuan-hoa doi ve 820 px: chu nhin nhu ve o dpi 100.
Chay: python anh/Bai_cach-chon-den-led-nha-xuong/ve_so_do.py
"""
import os
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.join(OUT, "_goc")
ROOT = os.path.dirname(os.path.dirname(OUT))
plt.rcParams["font.family"] = ["Segoe UI", "Arial", "DejaVu Sans"]

NAVY, AMBER, GRAY, LIGHT = "#1f3a5f", "#f2a71b", "#5b6573", "#eef2f7"


def luu(fig, ten):
    os.makedirs(GOC, exist_ok=True)
    png = os.path.join(GOC, ten.replace(".jpg", ".png"))
    fig.savefig(png, dpi=200, facecolor="white")
    plt.close(fig)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "tao_anh.py"), "chuan-hoa", png, os.path.join(OUT, ten)], check=True)


def cap_bao_ve_ip():
    fig = plt.figure(figsize=(8.2, 5.1))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 75)
    ax.axis("off")

    ax.text(60, 68.5, "Cách đọc cấp bảo vệ IP của đèn LED nhà xưởng", ha="center", fontsize=17, weight="bold", color=NAVY)

    ax.text(42, 52, "IP", ha="center", va="center", fontsize=40, weight="bold", color=GRAY)
    for x, d, color, nhan, mau_nhan in ((60, "5", NAVY, "Số thứ nhất\nchống bụi", NAVY),
                                         (78, "4", AMBER, "Số thứ hai\nchống nước", "#b5770a")):
        ax.add_patch(FancyBboxPatch((x - 6, 45), 12, 15, boxstyle="round,pad=0.4", fc=color, ec="none"))
        ax.text(x, 52.5, d, ha="center", va="center", fontsize=38, weight="bold", color="white")
        ax.text(x, 39, nhan, ha="center", va="center", fontsize=11.5, color=mau_nhan, weight="bold", linespacing=1.25)

    def bang(x0, title, color, rows):
        ax.add_patch(Rectangle((x0, 5), 54, 28, fc=LIGHT, ec="none"))
        ax.add_patch(Rectangle((x0, 27.5), 54, 5.5, fc=color, ec="none"))
        ax.text(x0 + 27, 30.2, title, ha="center", va="center", fontsize=12, weight="bold", color="white")
        for i, (so, nghia) in enumerate(rows):
            y = 23.3 - i * 5.2
            ax.text(x0 + 3.5, y, so, ha="center", va="center", fontsize=13, weight="bold", color=color)
            ax.text(x0 + 7.5, y, nghia, va="center", fontsize=11, color="#222222")

    bang(5, "Số thứ nhất (bụi, vật rắn)", NAVY, [
        ("4", "Chặn vật trên 1 mm, chưa chống bụi"),
        ("5", "Chống bụi một phần"),
        ("6", "Kín bụi hoàn toàn"),
    ])
    bang(61, "Số thứ hai (nước)", "#d48f0c", [
        ("0", "Không chống nước"),
        ("4", "Chịu nước bắn tóe"),
        ("5", "Chịu tia nước"),
        ("6", "Chịu tia nước mạnh"),
    ])
    ax.text(60, 1.3, "IP54: xưởng khô trong nhà.  IP65, IP66: xưởng bụi, ẩm, có rửa sàn.  Theo IEC 60529.",
            ha="center", fontsize=10, color=GRAY)
    luu(fig, "cap-bao-ve-ip-den-nha-xuong.jpg")


def so_do_bo_tri():
    # Mat bang 40 m (dai) x 30 m (rong), 8 den theo chieu dai x 5 hang theo chieu rong
    dai, rong, n_dai, n_rong = 40, 30, 8, 5
    kc_dai, kc_rong = dai / n_dai, rong / n_rong  # 5 m va 6 m
    fig = plt.figure(figsize=(8.2, 6.2))
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.74])
    ax.set_xlim(-4, dai + 5)
    ax.set_ylim(-4.5, rong + 3)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), dai, rong, fc=LIGHT, ec=NAVY, lw=2))
    for i in range(n_dai):
        for j in range(n_rong):
            x, y = kc_dai / 2 + i * kc_dai, kc_rong / 2 + j * kc_rong
            ax.add_patch(plt.Circle((x, y), 1.7, fc=AMBER, alpha=0.18, ec="none"))
            ax.add_patch(plt.Circle((x, y), 0.75, fc=AMBER, ec=NAVY, lw=1))

    ax.annotate("", (0, -2), (dai, -2), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
    ax.text(dai / 2, -4, "40 m", ha="center", fontsize=12, color=GRAY, weight="bold")
    ax.annotate("", (-2, 0), (-2, rong), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
    ax.text(-3.8, rong / 2, "30 m", va="center", rotation=90, fontsize=12, color=GRAY, weight="bold")
    ax.annotate("", (kc_dai / 2, rong + 1.2), (kc_dai * 1.5, rong + 1.2), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.2))
    ax.text(kc_dai, rong + 1.7, "5 m", ha="center", fontsize=11, color=NAVY, weight="bold")
    ax.annotate("", (dai + 1.2, kc_rong / 2), (dai + 1.2, kc_rong * 1.5), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.2))
    ax.text(dai + 1.8, kc_rong, "6 m", va="center", fontsize=11, color=NAVY, weight="bold")

    fig.text(0.5, 0.94, "Sơ đồ bố trí 40 đèn LED nhà xưởng cho mặt bằng 1.200 m²", ha="center", fontsize=16, weight="bold", color=NAVY)
    fig.text(0.5, 0.885, "Lưới 5 hàng x 8 đèn 150W (BUFO4-150, 19.500 lm), trần 9 m, độ rọi mục tiêu 300 lux",
             ha="center", fontsize=10.5, color=GRAY)
    fig.text(0.5, 0.035, "Sơ đồ ước lượng ban đầu. Vị trí chính xác cần tính bằng DIALux theo mặt bằng thực tế.",
             ha="center", fontsize=9.5, color=GRAY, style="italic")
    luu(fig, "so-do-bo-tri-den-nha-xuong-1200m2.jpg")


if __name__ == "__main__":
    cap_bao_ve_ip()
    so_do_bo_tri()
