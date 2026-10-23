"""Ghep anh tong hop 8 mau nha xuong 200m2 tu 8 anh mau da co cua bai.
Chay: python anh/Bai_mau-nha-xuong-200m2/ghep_tong_hop.py
"""
import os
import sys

from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "tools"))
from mau_anh import NAVY, chan_trang, hinh, luu, tieu_de  # noqa: E402

MAU = [
    ("nha-xuong-200m2-khung-thep-mai-ton.jpg", "Khung thép mái tôn"),
    ("nha-xuong-200m2-be-tong-cot-thep.jpg", "Bê tông cốt thép"),
    ("nha-xuong-200m2-gac-lung.jpg", "Có gác lửng"),
    ("nha-xuong-200m2-ket-hop-van-phong.jpg", "Kết hợp văn phòng"),
    ("nha-xuong-200m2-2-tang.jpg", "Nhà xưởng 2 tầng"),
    ("nha-xuong-200m2-mai-vom.jpg", "Mái vòm một nhịp"),
    ("nha-kho-200m2.jpg", "Nhà kho có kệ hàng"),
    ("nha-xuong-200m2-khu-boc-xep.jpg", "Có khu bốc xếp"),
]


def cat_169(im):
    w, h = im.size
    muc = w / h
    if muc > 16 / 9:
        nw = int(h * 16 / 9)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w * 9 / 16)
    return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


fig = hinh(4.5)
tieu_de(fig, "8 mẫu nhà xưởng 200m2 phổ biến")
so_cot, le, khe = 4, 0.15, 0.12
rong_o = (8.2 - 2 * le - (so_cot - 1) * khe) / so_cot
cao_o = rong_o * 9 / 16
H = fig.get_figheight()
for i, (ten, nhan) in enumerate(MAU):
    c, r = i % so_cot, i // so_cot
    x = le + c * (rong_o + khe)
    y_top = 0.85 + r * (cao_o + 0.55)
    ax = fig.add_axes([x / 8.2, 1 - (y_top + cao_o) / H, rong_o / 8.2, cao_o / H])
    ax.imshow(cat_169(Image.open(os.path.join(OUT, ten)).convert("RGB")))
    ax.axis("off")
    fig.text((x + rong_o / 2) / 8.2, 1 - (y_top + cao_o + 0.22) / H, nhan,
             ha="center", va="center", fontsize=11, weight="bold", color=NAVY)
chan_trang(fig, "Ảnh minh họa, không phải công trình thật")
luu(fig, OUT, "mau-nha-xuong-200m2-tong-hop.jpg")
