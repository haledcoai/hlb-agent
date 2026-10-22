"""Quan ly anh cho bai viet: doc cac cho [ANH: ...] trong bai kem ngu canh doan van, tai anh san pham that,
chuan hoa anh, ghi danh sach anh de wp_draft.py chen vao ban nhap.

Cach dung:
  python tools/tao_anh.py liet-ke <file_bai.md>                  # cac cho [ANH], ngu canh, trang thai
  python tools/tao_anh.py san-pham <slug>                        # anh that cua san pham tren website
  python tools/tao_anh.py tai <url> <file_ra>                    # tai mot anh ve may
  python tools/tao_anh.py chuan-hoa <file_vao> <file_ra.jpg> [--cat]
  python tools/tao_anh.py ghi <file_bai.md> --ten <ten file trong [ANH]> --file <anh.jpg> --nguon python|canva|website|nguoi-dung
                         [--url-website URL] [--media-id ID] [--dai-dien] [--ghi-chu "..."]
  python tools/tao_anh.py kiem <file_bai.md> [--khong-web]       # du anh, dung chuan, alt hop le, ten anh khong trung slug
  python tools/tao_anh.py duyet <file_bai.md> --ten <ten file> --trang-thai duyet|lam_lai|cho_duyet [--ghi-chu "..."]
                                                                 # chep quyet dinh tu trang Duyet anh HLB vao anh.json

wp_draft.py chi chen anh co trang_thai "duyet"; anh chua duyet duoc xu ly nhu anh thieu.

Chuan anh tao ra (nguoi dung chot 21/10/2026): JPG, rong 800-850 px (mac dinh 820), cao 400-800 px,
ten file dung nhu goi y trong [ANH].
Ten anh (bo .jpg) khong duoc trung slug cua bai dang viet, cung khong trung slug bai, trang, san pham, danh muc
hay anh da co tren website. WordPress tao trang dinh kem (attachment) theo ten file; trung slug thi link bai
co the bi chuyen huong sang trang anh hoac file anh. Anh nguon website dung lai URL co san tren website, khong ap chuan nay.
Anh luu o anh/<ten bai>/, danh sach o anh/<ten bai>/anh.json. File bai .md khong bi sua,
nen phieu duyet khong mat hieu luc khi them anh. Script nay khong tai gi len website.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://denlednhaxuongcaocap.com"
IMAGE = re.compile(r"\[ẢNH:([^\]]*)\]")
NGUON = ("python", "canva", "website", "nguoi-dung")
RONG, MIN_RONG, MAX_RONG = 820, 800, 850
MIN_CAO, MAX_CAO = 400, 800
MAX_KB = 300


TEN_HOP_LE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.jpg$")
# Cac loai noi dung tren website co slug co the dung voi trang dinh kem cua anh
LOAI_SLUG = (("bài viết", "wp/v2/posts"), ("trang", "wp/v2/pages"), ("sản phẩm", "wp/v2/product"),
             ("ảnh", "wp/v2/media"), ("chuyên mục", "wp/v2/categories"), ("danh mục sản phẩm", "wp/v2/product_cat"))


def thu_muc(article):
    return os.path.join(ROOT, "anh", os.path.splitext(os.path.basename(article))[0])


def manifest_path(article):
    return os.path.join(thu_muc(article), "anh.json")


def doc_cho_anh(article):
    """Cac cho [ANH: noi dung | alt: ... | ten file: ...] trong phan B, theo thu tu, kem ngu canh:
    heading gan nhat va doan van ngay truoc, ngay sau cho anh."""
    with open(article, encoding="utf-8") as f:
        lines = f.read().splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("# B.")), 0)
    end = next((i for i, l in enumerate(lines) if l.startswith("# C.")), len(lines))
    out, heading = [], ""

    def doan(rng):
        for j in rng:
            s = lines[j].strip()
            if s and not s.startswith(("#", "[", "|", "---")):
                return IMAGE.sub("", s)
        return ""

    for i in range(start, end):
        line = lines[i]
        if re.match(r"^#{1,4} ", line) and not line.startswith("# B."):
            heading = line.lstrip("#").strip()
        for m in IMAGE.finditer(line):
            parts = [p.strip() for p in m.group(1).split("|")]
            item = {"mo_ta": parts[0], "alt": "", "ten": "", "heading": heading,
                    "doan_truoc": doan(range(i - 1, start, -1)), "doan_sau": doan(range(i + 1, end))}
            for p in parts[1:]:
                k, _, v = p.partition(":")
                if k.strip().lower() == "alt":
                    item["alt"] = v.strip()
                elif k.strip().lower() == "tên file":
                    item["ten"] = v.strip()
            out.append(item)
    return out


def slug_bai(article):
    """Slug cua bai, lay o dong '| Slug | ... |' trong phan A."""
    with open(article, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\|\s*Slug\s*\|\s*([^|(]+)", line, re.I)
            if m:
                return m.group(1).strip().strip("`/").split("/")[-1]
    return ""


def bo_hau_to(slug):
    """WordPress them -2, -3 khi trung; so sanh ca ban da bo hau to so."""
    return re.sub(r"-\d+$", "", slug)


def slug_trung_website(goc):
    """Cac noi dung tren website co slug dung bang goc. Tra ve (danh sach trung, danh sach loai khong kiem tra duoc)."""
    trung, loi = [], []
    for nhan, duong in LOAI_SLUG:
        try:
            data = json.loads(get("%s/wp-json/%s?slug=%s&_fields=id,slug,link" % (SITE, duong, urllib.parse.quote(goc))))
        except Exception:
            loi.append(nhan)
            continue
        trung += ["%s %s (ID %s)" % (nhan, d.get("link", ""), d.get("id")) for d in data if isinstance(d, dict)]
    return trung, loi


def doc_manifest(article):
    try:
        with open(manifest_path(article), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"bai": os.path.basename(article), "anh": []}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HLB-anh/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def loi_chuan(path):
    """Danh sach loi so voi chuan anh tao ra."""
    from PIL import Image
    loi = []
    if not path.lower().endswith(".jpg"):
        loi.append("phải là file .jpg")
    with Image.open(path) as im:
        if im.format != "JPEG":
            loi.append("định dạng thật là %s, cần JPEG" % im.format)
        if not MIN_RONG <= im.width <= MAX_RONG:
            loi.append("rộng %d px, cần %d-%d px" % (im.width, MIN_RONG, MAX_RONG))
        if not MIN_CAO <= im.height <= MAX_CAO:
            loi.append("cao %d px, cần %d-%d px" % (im.height, MIN_CAO, MAX_CAO))
    if os.path.getsize(path) // 1024 > MAX_KB:
        loi.append("nặng %d KB, tối đa %d KB" % (os.path.getsize(path) // 1024, MAX_KB))
    return loi


# ---------- Lenh ----------

def liet_ke(args):
    m = {a["ten"]: a for a in doc_manifest(args.article)["anh"]}
    for i, c in enumerate(doc_cho_anh(args.article), 1):
        a = m.get(c["ten"])
        status = "CHƯA CÓ" if not a else "%s (%s)" % (a["file"], a["nguon"])
        print("%d. %s\n   alt: %s\n   tên file: %s\n   thuộc mục: %s\n   đoạn trước: %s\n   đoạn sau: %s\n   trạng thái: %s"
              % (i, c["mo_ta"], c["alt"], c["ten"], c["heading"], c["doan_truoc"], c["doan_sau"], status))


def san_pham(args):
    data = json.loads(get(SITE + "/wp-json/wc/store/v1/products?slug=" + urllib.parse.quote(args.slug)))
    if not data:
        sys.exit("Không thấy sản phẩm slug %s" % args.slug)
    seen = set()
    print("Sản phẩm:", data[0]["name"])
    for img in data[0].get("images", []):
        if img["src"] in seen:
            continue
        seen.add(img["src"])
        print("- media %s: %s\n  alt trên website: %s" % (img.get("id"), img["src"], img.get("alt")))


def tai(args):
    if not args.url.startswith("https://"):
        sys.exit("Chỉ tải qua https")
    data = get(args.url)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(data)
    print("Đã tải %d KB: %s" % (len(data) // 1024, args.out))


def chuan_hoa(args):
    """Doi ve JPG rong 820 px. Cao vuot 800 px: --cat thi cat giua (anh chup), khong thi bao loi (so do phai ve lai)."""
    from PIL import Image
    if not args.out.lower().endswith(".jpg"):
        sys.exit("File ra phải có đuôi .jpg")
    img = Image.open(args.src).convert("RGB")
    if img.width < MIN_RONG:
        sys.exit("Ảnh gốc rộng %d px, nhỏ hơn %d px. Không phóng to ảnh nhỏ, cần ảnh gốc lớn hơn." % (img.width, MIN_RONG))
    img = img.resize((RONG, round(img.height * RONG / img.width)), Image.LANCZOS)
    if img.height > MAX_CAO:
        if not args.cat:
            sys.exit("Sau khi đổi về rộng %d px, ảnh cao %d px, vượt %d px. Vẽ lại với tỷ lệ thấp hơn, hoặc thêm --cat để cắt giữa."
                     % (RONG, img.height, MAX_CAO))
        top = (img.height - MAX_CAO) // 2
        img = img.crop((0, top, RONG, top + MAX_CAO))
    if img.height < MIN_CAO:
        sys.exit("Ảnh cao %d px, thấp hơn %d px. Tạo hoặc vẽ lại với tỷ lệ cao hơn (16:9 cho ra 461 px)." % (img.height, MIN_CAO))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    quality = 88
    while True:
        img.save(args.out, "JPEG", quality=quality, optimize=True, progressive=True)  # khong giu EXIF
        kb = os.path.getsize(args.out) // 1024
        if kb <= MAX_KB or quality <= 60:
            break
        quality -= 4
    print("Đã lưu %s: %d x %d, %d KB, chất lượng %d" % (args.out, img.width, img.height, kb, quality))


def ghi(args):
    cho = {c["ten"]: c for c in doc_cho_anh(args.article)}
    if args.ten not in cho:
        sys.exit("Bài không có chỗ [ẢNH] với tên file %s. Các tên có: %s" % (args.ten, ", ".join(cho)))
    path = os.path.abspath(args.file)
    if not os.path.isfile(path):
        sys.exit("Không thấy file ảnh %s" % args.file)
    if args.nguon != "website" and os.path.basename(path) != args.ten:
        sys.exit("Tên file ảnh phải đúng như gợi ý trong bài: %s (đang là %s)" % (args.ten, os.path.basename(path)))
    m = doc_manifest(args.article)
    m["anh"] = [a for a in m["anh"] if a["ten"] != args.ten]  # anh moi hoac lam lai: quay ve cho duyet
    if args.dai_dien:
        for a in m["anh"]:
            a["dai_dien"] = False
    m["anh"].append({
        "ten": args.ten,
        "file": os.path.relpath(path, ROOT).replace("\\", "/"),
        "nguon": args.nguon,
        "alt": cho[args.ten]["alt"],
        "mo_ta": cho[args.ten]["mo_ta"],
        "url_website": args.url_website,
        "media_id": args.media_id,
        "dai_dien": bool(args.dai_dien),
        "ghi_chu": args.ghi_chu or "",
        "trang_thai": "cho_duyet",
    })
    os.makedirs(thu_muc(args.article), exist_ok=True)
    with open(manifest_path(args.article), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print("Đã ghi ảnh %s (%s) vào %s" % (args.ten, args.nguon, manifest_path(args.article)))


def duyet(args):
    m = doc_manifest(args.article)
    a = next((x for x in m["anh"] if x["ten"] == args.ten), None)
    if not a:
        sys.exit("Danh sách ảnh chưa có %s" % args.ten)
    a["trang_thai"] = args.trang_thai
    a["ghi_chu_duyet"] = args.ghi_chu or ""
    with open(manifest_path(args.article), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print("%s: %s" % (args.ten, args.trang_thai))


def kiem(args):
    m = {a["ten"]: a for a in doc_manifest(args.article)["anh"]}
    loi = []
    cho = doc_cho_anh(args.article)
    co = sum(1 for c in cho if c["ten"] in m)
    slug = slug_bai(args.article)
    if not slug:
        loi.append("Không đọc được slug bài ở phần A (dòng | Slug | ... |), chưa so được tên ảnh với slug bài")
    ten_da_gap = set()
    for c in cho:
        goc = c["ten"][:-4] if c["ten"].lower().endswith(".jpg") else c["ten"]
        if not TEN_HOP_LE.match(c["ten"]):
            loi.append("Tên file phải là chữ thường không dấu, số, nối bằng hyphen, đuôi .jpg: %s" % c["ten"])
        if c["ten"] in ten_da_gap:
            loi.append("Tên file bị lặp trong bài: %s" % c["ten"])
        ten_da_gap.add(c["ten"])
        if slug and bo_hau_to(goc) == bo_hau_to(slug):
            loi.append("Tên ảnh %s trùng slug bài (%s). Thêm từ mô tả nội dung ảnh, ví dụ %s-so-do.jpg"
                       % (c["ten"], slug, slug))
        a = m.get(c["ten"])
        if not args.khong_web and not (a and a.get("url_da_tai")):  # anh da tai len thi khong so voi chinh no
            trung, khong_kiem = slug_trung_website(goc)
            loi += ["Tên ảnh %s trùng slug đã có trên website: %s" % (c["ten"], t) for t in trung]
            if khong_kiem:
                print("Chưa kiểm tra được slug %s với: %s" % (goc, ", ".join(khong_kiem)))
        a = m.get(c["ten"])
        if not a:
            loi.append("Chưa có ảnh cho %s" % c["ten"])
            continue
        f = os.path.join(ROOT, a["file"])
        if not os.path.isfile(f):
            loi.append("Mất file %s" % a["file"])
        elif a["nguon"] != "website":
            loi += ["%s: %s" % (a["file"], x) for x in loi_chuan(f)]
        if not a["alt"] or len(a["alt"]) > 125:
            loi.append("Alt của %s trống hoặc quá 125 ký tự" % c["ten"])
        if a["nguon"] == "website" and not a.get("url_website"):
            loi.append("%s nguồn website nhưng thiếu url_website" % c["ten"])
    if sum(1 for a in m.values() if a.get("dai_dien")) > 1:
        loi.append("Có hơn một ảnh đại diện")
    if loi:
        print("CHƯA ĐỦ ẢNH: %d/%d chỗ [ẢNH] đã có ảnh" % (co, len(cho)))
        for x in loi:
            print("- " + x)
        sys.exit(1)
    print("Đủ ảnh: %d/%d, đúng chuẩn JPG %d-%d x %d-%d px, alt hợp lệ, tên ảnh không trùng slug." % (co, len(cho), MIN_RONG, MAX_RONG, MIN_CAO, MAX_CAO))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("liet-ke"); p.add_argument("article"); p.set_defaults(func=liet_ke)
    p = sub.add_parser("san-pham"); p.add_argument("slug"); p.set_defaults(func=san_pham)
    p = sub.add_parser("tai"); p.add_argument("url"); p.add_argument("out"); p.set_defaults(func=tai)
    p = sub.add_parser("chuan-hoa"); p.add_argument("src"); p.add_argument("out")
    p.add_argument("--cat", action="store_true", help="cat giua khi anh qua cao (chi dung cho anh chup)")
    p.set_defaults(func=chuan_hoa)
    p = sub.add_parser("ghi"); p.add_argument("article"); p.add_argument("--ten", required=True)
    p.add_argument("--file", required=True); p.add_argument("--nguon", required=True, choices=NGUON)
    p.add_argument("--url-website"); p.add_argument("--media-id", type=int)
    p.add_argument("--dai-dien", action="store_true"); p.add_argument("--ghi-chu")
    p.set_defaults(func=ghi)
    p = sub.add_parser("kiem"); p.add_argument("article")
    p.add_argument("--khong-web", action="store_true", help="bo qua so ten anh voi slug tren website (khi khong co mang)")
    p.set_defaults(func=kiem)
    p = sub.add_parser("duyet"); p.add_argument("article"); p.add_argument("--ten", required=True)
    p.add_argument("--trang-thai", required=True, choices=("duyet", "lam_lai", "cho_duyet")); p.add_argument("--ghi-chu")
    p.set_defaults(func=duyet)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
