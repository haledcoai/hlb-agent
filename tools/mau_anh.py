"""Thu vien mau so do cho anh bai viet HLB. Moi bai chi viet anh/<ten bai>/ve_so_do.py ngan,
goi mau voi so lieu cua bai, roi luu(). Xem mau o anh/Bai_cach-chon-den-led-nha-xuong/ve_so_do.py.

Mau co san:
  luoi_bo_tri(dai, rong, so_cot, so_hang, ...)   so do bo tri den tren mat bang
  bang_ip(cap="54", ...)                         cach doc cap bao ve IP
  bang_so_sanh(cot, dong, ...)                   bang so sanh 2-4 model, toi da 5 cot
  bieu_do_cot(nhan, gia_tri, don_vi, ...)        so sanh dien nang, chi phi, lumen
  mat_cat_lap_dat(chieu_cao, goc_chieu, khoang_cach, ...)  chieu cao treo, goc chieu, vung sang tren san
  cac_buoc(buoc, ...)                            quy trinh 3-6 buoc, buoc co rui ro co canh bao an toan

luu(fig, thu_muc, ten_file) tu kiem tra chu tren hinh (de nhau, tran khung, nho hon 13 px khi hien thi
o 820 px, co em dash/en dash). Co loi thi khong luu va bao loi de ve lai. Qua kiem tra thi luu PNG dpi 200
vao <thu_muc>/_goc/ roi goi tao_anh.py chuan-hoa ve JPG 820 px.

Moi con so truyen vao mau phai lay tu bai hoac Knowledge. Mau khong tu them so lieu nao.
"""
import math
import os
import re
import subprocess
import sys
import textwrap

import logging

try:
    import matplotlib
except ImportError:  # may cloud moi khong cai san matplotlib (setup script de trong)
    print("Chua co matplotlib, dang cai: pip install matplotlib", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "matplotlib"], check=True)
    import matplotlib

matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # may khong co Segoe UI thi dung font du phong
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from matplotlib.text import Text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plt.rcParams["font.family"] = ["Segoe UI", "Arial", "DejaVu Sans"]

NAVY, AMBER, GRAY, LIGHT = "#1f3a5f", "#f2a71b", "#5b6573", "#eef2f7"
AMBER_DAM, AMBER_TIEU_DE, CHU = "#b5770a", "#d48f0c", "#222222"

RONG_IN, DPI, RONG_PX = 8.2, 200, 820
MIN_CAO_IN, MAX_CAO_IN = 4.0, 8.0
MIN_PX = 13  # chu nho nhat khi hien thi o 820 px
GACH = re.compile("[\u2013\u2014]")
DIALUX = "Sơ đồ ước lượng ban đầu. Vị trí chính xác cần tính bằng DIALux theo mặt bằng thực tế."


# ---------- Dung chung ----------

def so_vn(x, le=0):
    """1200 -> 1.200; 2.5 -> 2,5 (Knowledge 8.3)."""
    s = ("{:,.%df}" % le).format(x)
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")


def hinh(cao_in):
    if not MIN_CAO_IN <= cao_in <= MAX_CAO_IN:
        raise SystemExit("Khổ hình cao %.1f inch, cần %.0f-%.0f inch (ảnh cao 400-800 px). Bớt nội dung hoặc tách ảnh."
                         % (cao_in, MIN_CAO_IN, MAX_CAO_IN))
    return plt.figure(figsize=(RONG_IN, cao_in), dpi=DPI)


def tieu_de(fig, chu, phu=None):
    h = fig.get_figheight()
    fig.text(0.5, 1 - 0.42 / h, chu, ha="center", va="center", fontsize=16, weight="bold", color=NAVY)
    if phu:
        fig.text(0.5, 1 - 0.78 / h, phu, ha="center", va="center", fontsize=10.5, color=GRAY)


def chan_trang(fig, chu):
    if chu:
        fig.text(0.5, 0.22 / fig.get_figheight(), chu, ha="center", va="center", fontsize=9.5, color=GRAY, style="italic")


def xuong_dong(chu, rong_in, co_chu):
    """Ngat dong theo do rong o (inch) va co chu (pt), uoc luong 0,52 em moi ky tu."""
    so_ky_tu = max(6, int(rong_in * 72 / (co_chu * 0.52)))
    return "\n".join(textwrap.wrap(str(chu), so_ky_tu)) or str(chu)


def kiem_chu(fig):
    """Loi chu tren hinh: de nhau, tran khung, qua nho, em dash/en dash."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    w, h = fig.bbox.width, fig.bbox.height
    ty_le = RONG_PX / w  # pixel hinh -> pixel anh 820
    chu = [t for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip() and t.figure is fig]
    loi, hop = [], []
    for t in chu:
        s = t.get_text().replace("\n", " ")
        px = t.get_fontsize() * fig.dpi / 72 * ty_le
        if px < MIN_PX - 0.5:
            loi.append("Chữ \"%s\" hiển thị %.0f px, cần từ %d px" % (s[:40], px, MIN_PX))
        if GACH.search(t.get_text()):
            loi.append("Chữ \"%s\" có em dash hoặc en dash, chỉ dùng hyphen" % s[:40])
        b = t.get_window_extent(r)
        if b.x0 < -1 or b.y0 < -1 or b.x1 > w + 1 or b.y1 > h + 1:
            loi.append("Chữ \"%s\" tràn ra ngoài khung ảnh" % s[:40])
        hop.append((b.shrunk(0.94, 0.8), s))
    for i in range(len(hop)):
        for j in range(i + 1, len(hop)):
            if hop[i][0].overlaps(hop[j][0]):
                loi.append("Chữ \"%s\" đè lên \"%s\"" % (hop[i][1][:30], hop[j][1][:30]))
    return loi


def luu(fig, thu_muc, ten):
    """Kiem tra chu, luu PNG goc, chuan hoa ve JPG 820 px trong thu_muc."""
    if not ten.endswith(".jpg"):
        raise SystemExit("Tên file phải có đuôi .jpg: %s" % ten)
    loi = kiem_chu(fig)
    if loi:
        plt.close(fig)
        raise SystemExit("Chưa lưu %s, chữ trên hình có lỗi, vẽ lại:\n- %s" % (ten, "\n- ".join(loi)))
    goc = os.path.join(thu_muc, "_goc")
    os.makedirs(goc, exist_ok=True)
    png = os.path.join(goc, ten[:-4] + ".png")
    fig.savefig(png, dpi=DPI, facecolor="white")
    plt.close(fig)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "tao_anh.py"), "chuan-hoa", png, os.path.join(thu_muc, ten)],
                   check=True)


def _mui_ten(ax, a, b, mau=GRAY):
    ax.annotate("", a, b, arrowprops=dict(arrowstyle="<->", color=mau, lw=1.2))


# ---------- Mau ----------

def luoi_bo_tri(dai, rong, so_cot, so_hang, tieu_de_anh, phu_de=None, ghi_chu=DIALUX):
    """Mat bang dai x rong (m), so_cot den theo chieu dai, so_hang theo chieu rong, den dat giua o luoi.
    Canh dai luon nam ngang."""
    if rong > dai:
        dai, rong, so_cot, so_hang = rong, dai, so_hang, so_cot
    kc_dai, kc_rong = dai / so_cot, rong / so_hang
    u = max(dai, rong) / 40  # don vi le, theo mat bang 40 m
    kc = min(kc_dai, kc_rong)
    x0, x1, y0, y1 = -4 * u, dai + 5 * u, -4.5 * u, rong + 3 * u
    cao_ax = RONG_IN * 0.9 * (y1 - y0) / (x1 - x0)
    fig = hinh(min(6.2, max(4.2, cao_ax + 1.55)))
    h = fig.get_figheight()
    ax = fig.add_axes([0.05, 0.42 / h, 0.9, 1 - 1.55 / h])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), dai, rong, fc=LIGHT, ec=NAVY, lw=2))
    for i in range(so_cot):
        for j in range(so_hang):
            x, y = kc_dai / 2 + i * kc_dai, kc_rong / 2 + j * kc_rong
            ax.add_patch(Circle((x, y), kc * 0.34, fc=AMBER, alpha=0.18, ec="none"))
            ax.add_patch(Circle((x, y), kc * 0.15, fc=AMBER, ec=NAVY, lw=1))

    _mui_ten(ax, (0, -2 * u), (dai, -2 * u))
    ax.text(dai / 2, -4 * u, "%s m" % so_vn(dai, 0 if dai == int(dai) else 1), ha="center", fontsize=12, color=GRAY, weight="bold")
    _mui_ten(ax, (-2 * u, 0), (-2 * u, rong))
    ax.text(-3.8 * u, rong / 2, "%s m" % so_vn(rong, 0 if rong == int(rong) else 1), va="center", rotation=90,
            fontsize=12, color=GRAY, weight="bold")
    if so_cot > 1:
        _mui_ten(ax, (kc_dai / 2, rong + 1.2 * u), (kc_dai * 1.5, rong + 1.2 * u), NAVY)
        ax.text(kc_dai, rong + 1.7 * u, "%s m" % so_vn(kc_dai, 0 if kc_dai == int(kc_dai) else 1), ha="center",
                fontsize=11, color=NAVY, weight="bold")
    if so_hang > 1:
        _mui_ten(ax, (dai + 1.2 * u, kc_rong / 2), (dai + 1.2 * u, kc_rong * 1.5), NAVY)
        ax.text(dai + 1.8 * u, kc_rong, "%s m" % so_vn(kc_rong, 0 if kc_rong == int(kc_rong) else 1), va="center",
                fontsize=11, color=NAVY, weight="bold")
    tieu_de(fig, tieu_de_anh, phu_de)
    chan_trang(fig, ghi_chu)
    return fig


BUI = [("4", "Chặn vật trên 1 mm, chưa chống bụi"), ("5", "Chống bụi một phần"), ("6", "Kín bụi hoàn toàn")]
NUOC = [("0", "Không chống nước"), ("4", "Chịu nước bắn tóe"), ("5", "Chịu tia nước"), ("6", "Chịu tia nước mạnh")]


def bang_ip(cap="54", tieu_de_anh="Cách đọc cấp bảo vệ IP của đèn LED nhà xưởng", bui=BUI, nuoc=NUOC,
            ghi_chu="IP54: xưởng khô trong nhà.  IP65, IP66: xưởng bụi, ẩm, có rửa sàn.  Theo IEC 60529."):
    """Hai chu so IP minh hoa (cap) va hai bang y nghia. Noi dung mac dinh theo Knowledge muc 6."""
    so_dong = max(len(bui), len(nuoc))
    fig = hinh(5.1 + max(0, so_dong - 4) * 0.4)
    ax = fig.add_axes([0, 0, 1, 1])
    cao = 75 * fig.get_figheight() / 5.1
    ax.set_xlim(0, 120)
    ax.set_ylim(0, cao)
    ax.axis("off")
    d = cao - 75  # day phan tren len khi bang dai hon
    ax.text(60, 68.5 + d, tieu_de_anh, ha="center", fontsize=17, weight="bold", color=NAVY)
    ax.text(42, 52 + d, "IP", ha="center", va="center", fontsize=40, weight="bold", color=GRAY)
    for x, so, mau, nhan, mau_nhan in ((60, cap[0], NAVY, "Số thứ nhất\nchống bụi", NAVY),
                                       (78, cap[1], AMBER, "Số thứ hai\nchống nước", AMBER_DAM)):
        ax.add_patch(FancyBboxPatch((x - 6, 45 + d), 12, 15, boxstyle="round,pad=0.4", fc=mau, ec="none"))
        ax.text(x, 52.5 + d, so, ha="center", va="center", fontsize=38, weight="bold", color="white")
        ax.text(x, 39 + d, nhan, ha="center", va="center", fontsize=11.5, color=mau_nhan, weight="bold", linespacing=1.25)

    cao_bang = 7.5 + so_dong * 5.2

    def bang(x0, ten, mau, dong):
        ax.add_patch(Rectangle((x0, 5), 54, cao_bang, fc=LIGHT, ec="none"))
        ax.add_patch(Rectangle((x0, 5 + cao_bang - 5.5), 54, 5.5, fc=mau, ec="none"))
        ax.text(x0 + 27, 5 + cao_bang - 2.8, ten, ha="center", va="center", fontsize=12, weight="bold", color="white")
        for i, (so, nghia) in enumerate(dong):
            y = 5 + cao_bang - 9.7 - i * 5.2
            ax.text(x0 + 3.5, y, so, ha="center", va="center", fontsize=13, weight="bold", color=mau)
            ax.text(x0 + 7.5, y, nghia, va="center", fontsize=11, color=CHU)

    bang(5, "Số thứ nhất (bụi, vật rắn)", NAVY, bui)
    bang(61, "Số thứ hai (nước)", AMBER_TIEU_DE, nuoc)
    ax.text(60, 1.3, ghi_chu, ha="center", fontsize=10, color=GRAY)
    return fig


def bang_so_sanh(cot, dong, tieu_de_anh, phu_de=None, ghi_chu=None, cot_dau_rong=0.3):
    """Bang toi da 5 cot. dong: list cac list, o trong (None, "") ghi "không công bố"."""
    if not 2 <= len(cot) <= 5:
        raise SystemExit("Bảng so sánh cần 2-5 cột, đang có %d" % len(cot))
    trai, phai = 0.35, RONG_IN - 0.35
    rong_bang = phai - trai
    rong_cot = [rong_bang * cot_dau_rong] + [rong_bang * (1 - cot_dau_rong) / (len(cot) - 1)] * (len(cot) - 1)
    o = [[xuong_dong(x if x not in (None, "") else "không công bố", rc - 0.15, 10.5) for x, rc in zip(r, rong_cot)]
         for r in dong]
    cao_dong = [0.22 + 0.2 * max(c.count("\n") + 1 for c in r) for r in o]
    tren = 1.15 if phu_de else 0.85
    cao_hinh = tren + 0.5 + sum(cao_dong) + (0.5 if ghi_chu else 0.25)
    fig = hinh(max(MIN_CAO_IN, cao_hinh))
    h = fig.get_figheight()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, RONG_IN)
    ax.set_ylim(0, h)
    ax.axis("off")
    y = h - tren
    x = trai
    ax.add_patch(Rectangle((trai, y - 0.5), rong_bang, 0.5, fc=NAVY, ec="none"))
    for ten, rc in zip(cot, rong_cot):
        ax.text(x + 0.1, y - 0.25, xuong_dong(ten, rc - 0.15, 11), va="center", fontsize=11, weight="bold", color="white")
        x += rc
    y -= 0.5
    for i, (r, cd) in enumerate(zip(o, cao_dong)):
        ax.add_patch(Rectangle((trai, y - cd), rong_bang, cd, fc=LIGHT if i % 2 == 0 else "white", ec="none"))
        x = trai
        for k, (c, rc) in enumerate(zip(r, rong_cot)):
            thieu = c == "không công bố"
            ax.text(x + 0.1, y - cd / 2, c, va="center", fontsize=10.5, linespacing=1.3,
                    weight="bold" if k == 0 else "normal", color=GRAY if thieu else (NAVY if k == 0 else CHU),
                    style="italic" if thieu else "normal")
            x += rc
        y -= cd
    ax.plot([trai, phai], [y, y], color=NAVY, lw=1.2)
    tieu_de(fig, tieu_de_anh, phu_de)
    chan_trang(fig, ghi_chu)
    return fig


def bieu_do_cot(nhan, gia_tri, don_vi, tieu_de_anh, phu_de=None, ghi_chu=None, noi_bat=None, le=0):
    """Cot dung, so tren dinh cot theo cach viet so VN. noi_bat: chi so cot to mau vang cam."""
    if not 2 <= len(nhan) <= 8:
        raise SystemExit("Biểu đồ cột cần 2-8 cột, đang có %d" % len(nhan))
    fig = hinh(4.8)
    h = fig.get_figheight()
    ax = fig.add_axes([0.1, 0.95 / h, 0.86, 1 - (2.0 if phu_de else 1.7) / h])
    mau = [AMBER if i == noi_bat else NAVY for i in range(len(nhan))]
    cot = ax.bar(range(len(nhan)), gia_tri, color=mau, width=0.6)
    tran = max(gia_tri) * 1.18
    ax.set_ylim(0, tran)
    for c, v in zip(cot, gia_tri):
        ax.text(c.get_x() + c.get_width() / 2, v + tran * 0.02, so_vn(v, le), ha="center", va="bottom",
                fontsize=11, weight="bold", color=CHU)
    rong_nhan = 7.0 / len(nhan)
    ax.set_xticks(range(len(nhan)), [xuong_dong(n, rong_nhan, 10.5) for n in nhan], fontsize=10.5, color=CHU)
    ax.set_ylabel(don_vi, fontsize=10.5, color=GRAY)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: so_vn(v)))
    ax.tick_params(axis="y", labelsize=10, colors=GRAY)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#c9d1dc")
    ax.spines["bottom"].set_color("#c9d1dc")
    ax.grid(axis="y", color="#e3e8ef", lw=0.8)
    ax.set_axisbelow(True)
    tieu_de(fig, tieu_de_anh, phu_de)
    chan_trang(fig, ghi_chu)
    return fig


def mat_cat_lap_dat(chieu_cao, goc_chieu, khoang_cach, tieu_de_anh, phu_de=None, so_den=3,
                    ghi_chu="Ước tính theo hình học góc chiếu, chưa tính phân bố quang của đèn. Cần kiểm tra bằng DIALux."):
    """Mat cat ngang: den treo o chieu_cao (m), goc chieu (do), cach nhau khoang_cach (m).
    Vung sang moi den tren san co duong kinh 2 x h x tan(goc/2). Ho giua hai vung sang thi to xam 'vùng tối'."""
    ban_kinh = chieu_cao * math.tan(math.radians(goc_chieu / 2))
    xs = [i * khoang_cach for i in range(so_den)]
    trai, phai = xs[0] - max(ban_kinh, khoang_cach / 2) - 1, xs[-1] + max(ban_kinh, khoang_cach / 2) + 1
    fig = hinh(5.0)
    h = fig.get_figheight()
    ax = fig.add_axes([0.04, 0.5 / h, 0.92, 1 - 1.75 / h])
    ax.set_xlim(trai - 1.5, phai + 0.5)
    ax.set_ylim(-chieu_cao * 0.22, chieu_cao * 1.18)
    ax.axis("off")
    ax.plot([trai, phai], [0, 0], color=NAVY, lw=2.5)
    ax.plot([trai, phai], [chieu_cao, chieu_cao], color=GRAY, lw=1, ls="--")
    for x in xs:
        ax.add_patch(Polygon([(x, chieu_cao), (x - ban_kinh, 0), (x + ban_kinh, 0)], closed=True, fc=AMBER, alpha=0.22, ec="none"))
        ax.add_patch(Rectangle((x - 0.35, chieu_cao - 0.12), 0.7, 0.24, fc=NAVY, ec="none"))
        ax.plot([x - ban_kinh, x + ban_kinh], [0.04, 0.04], color=AMBER, lw=5, solid_capstyle="butt")
    ho = khoang_cach - 2 * ban_kinh
    if ho > 0 and so_den > 1:
        a, b = xs[0] + ban_kinh, xs[1] - ban_kinh
        ax.add_patch(Rectangle((a, 0), b - a, chieu_cao * 0.06, fc=GRAY, alpha=0.35, ec="none"))
        ax.text((a + b) / 2, chieu_cao * 0.1, "vùng tối", ha="center", fontsize=10.5, color=GRAY, weight="bold")
    _mui_ten(ax, (trai - 0.8, 0), (trai - 0.8, chieu_cao))
    ax.text(trai - 1.2, chieu_cao / 2, "%s m" % so_vn(chieu_cao, 0 if chieu_cao == int(chieu_cao) else 1),
            rotation=90, va="center", ha="center", fontsize=12, weight="bold", color=GRAY)
    if so_den > 1:
        _mui_ten(ax, (xs[0], chieu_cao * 1.08), (xs[1], chieu_cao * 1.08), NAVY)
        ax.text((xs[0] + xs[1]) / 2, chieu_cao * 1.11, "%s m" % so_vn(khoang_cach, 0 if khoang_cach == int(khoang_cach) else 1),
                ha="center", fontsize=11, weight="bold", color=NAVY)
    x = xs[-1]
    _mui_ten(ax, (x - ban_kinh, -chieu_cao * 0.08), (x + ban_kinh, -chieu_cao * 0.08), AMBER_DAM)
    ax.text(x, -chieu_cao * 0.19, "vùng sáng khoảng %s m (ước tính)" % so_vn(2 * ban_kinh, 1),
            ha="center", fontsize=10.5, weight="bold", color=AMBER_DAM)
    ax.text(xs[0], chieu_cao * 0.55, "góc %s°" % so_vn(goc_chieu), ha="center", fontsize=11, weight="bold", color=NAVY)
    tieu_de(fig, tieu_de_anh, phu_de)
    chan_trang(fig, ghi_chu)
    return fig


def cac_buoc(buoc, tieu_de_anh, phu_de=None, canh_bao=(), ghi_chu=None):
    """buoc: list (ten buoc, mo ta ngan). canh_bao: so thu tu buoc (tu 1) co rui ro, ve vien vang cam
    va nhan 'Lưu ý an toàn' (bai lap dat, dau noi)."""
    if not 3 <= len(buoc) <= 6:
        raise SystemExit("Sơ đồ các bước cần 3-6 bước, đang có %d" % len(buoc))
    mo_ta = [xuong_dong(m, 5.6, 10.5) for _, m in buoc]
    cao_o = [0.7 + 0.2 * m.count("\n") for m in mo_ta]
    tren = 1.15 if phu_de else 0.85
    fig = hinh(max(MIN_CAO_IN, tren + sum(cao_o) + 0.14 * (len(buoc) - 1) + (0.5 if ghi_chu else 0.3)))
    h = fig.get_figheight()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, RONG_IN)
    ax.set_ylim(0, h)
    ax.axis("off")
    y = h - tren
    for i, ((ten, _), m, c) in enumerate(zip(buoc, mo_ta, cao_o), 1):
        nguy = i in canh_bao
        ax.add_patch(FancyBboxPatch((0.45, y - c), 7.3, c, boxstyle="round,pad=0,rounding_size=0.08",
                                    fc="#fff6e5" if nguy else LIGHT, ec=AMBER if nguy else "none", lw=1.5))
        ax.add_patch(Circle((0.85, y - c / 2), 0.2, fc=AMBER if nguy else NAVY, ec="none"))
        ax.text(0.85, y - c / 2, str(i), ha="center", va="center", fontsize=12, weight="bold", color="white")
        ax.text(1.25, y - 0.22, ten, va="center", fontsize=12, weight="bold", color=NAVY)
        if nguy:
            ax.text(7.6, y - 0.22, "Lưu ý an toàn", ha="right", va="center", fontsize=10, weight="bold", color=AMBER_DAM)
        ax.text(1.25, y - 0.4, m, va="top", fontsize=10.5, color=CHU, linespacing=1.3)
        y -= c + 0.14
    tieu_de(fig, tieu_de_anh, phu_de)
    chan_trang(fig, ghi_chu)
    return fig
