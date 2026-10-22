"""Ve 2 so do cho bai cach-chon-den-led-nha-xuong bang mau trong tools/mau_anh.py.
So lieu lay dung theo bai va Knowledge muc 6.
Chay: python anh/Bai_cach-chon-den-led-nha-xuong/ve_so_do.py
"""
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "tools"))
from mau_anh import bang_ip, luoi_bo_tri, luu  # noqa: E402

if __name__ == "__main__":
    luu(bang_ip(cap="54"), OUT, "cap-bao-ve-ip-den-nha-xuong.jpg")
    luu(luoi_bo_tri(40, 30, 8, 5, "Sơ đồ bố trí 40 đèn LED nhà xưởng cho mặt bằng 1.200 m²",
                    phu_de="Lưới 5 hàng x 8 đèn 150W (BUFO4-150, 19.500 lm), trần 9 m, độ rọi mục tiêu 300 lux"),
        OUT, "so-do-bo-tri-den-nha-xuong-1200m2.jpg")
