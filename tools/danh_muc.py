"""Cong cu cua Agent Danh muc: doc danh muc san pham tren denlednhaxuongcaocap.com, dang Trang nhap de xem truoc,
ap dung noi dung moi vao danh muc (sao luu truoc), khoi phuc ban cu.

Cach dung:
  python tools/danh_muc.py ds                              # liet ke danh muc san pham (id, slug, so san pham, do dai mo ta)
  python tools/danh_muc.py tim "<tu khoa>"                 # tu khoa co khop danh muc nao khong (dieu phoi tu nhan dien)
  python tools/danh_muc.py doc <slug|id|link>              # lay noi dung cu + san pham trong danh muc vao nghien_cuu/DM_<slug>/
  python tools/danh_muc.py nhap DM_<slug>.md               # tao file xem truoc DM_<slug>.preview.html
  python tools/danh_muc.py nhap DM_<slug>.md --post        # tao/cap nhat Trang nhap "[Nhap danh muc] <ten>" tren WordPress
  python tools/danh_muc.py ap-dung DM_<slug>.md --duyet-luc <ISO>            # chay thu: in nhung gi se ghi
  python tools/danh_muc.py ap-dung DM_<slug>.md --duyet-luc <ISO> --post     # sao luu, ghi danh muc + Rank Math, kiem tra
  python tools/danh_muc.py kiem-trang DM_<slug>.md         # trang danh muc cong khai da hien noi dung moi chua (ca khoi tren)
  python tools/danh_muc.py khoi-phuc <slug> [--ban <file sao luu>] --post   # ghi lai ban sao luu gan nhat

File bai DM_<slug>.md co 3 phan nhu bai blog (# A., # B., # C.). Phan B co 2 dong danh dau rieng mot dong:
[KHỐI TRÊN] (doan ngan hien tren luoi san pham) va [KHỐI DƯỚI] (hien sau luoi san pham, la truong "description" cua danh muc).

Danh muc khong co ban nhap: ghi vao la cong khai ngay. Vi vay:
- nhap --post va ap-dung --post chi chay khi bai co phieu DAT khop noi dung (tools/phieu_duyet.py kiem).
- ap-dung --post can --duyet-luc: gio nguoi dung bam "Duyet, cap nhat len danh muc" tren Bang dieu phoi (truong
  duyet_ap_dung_luc). Agent chi chep gia tri do, khong tu dien.
- ap-dung luon sao luu mo ta, SEO title, meta description cu vao danh_muc/sao_luu/ truoc khi ghi.
Khoi tren nam o truong rieng cua theme, REST API chua mo: dat ten truong vao danh_muc/cau_hinh.json ("khoi_tren_meta")
khi theme da dang ky truong do cho REST; chua co thi script ghi file HTML khoi tren de nguoi dung dan tay, roi kiem-trang.
Can WP_USER, WP_APP_PASSWORD cua tai khoan co quyen Quan ly cua hang (shop_manager) de doc/ghi danh muc.
"""
import argparse
import csv
import datetime
import hashlib
import html
import html.parser
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_draft  # noqa: E402  (call, credentials, md_to_html, inline, anh)

SITE = wp_draft.SITE
ROOT = wp_draft.ROOT
THU_MUC = os.path.join(ROOT, "danh_muc")
SAO_LUU = os.path.join(THU_MUC, "sao_luu")
CAU_HINH = os.path.join(THU_MUC, "cau_hinh.json")
NGHIEN_CUU = os.path.join(ROOT, "nghien_cuu")
KHOI_TREN, KHOI_DUOI = "[KHỐI TRÊN]", "[KHỐI DƯỚI]"
TIEN_TO_NHAP = "[Nháp danh mục] "
UA = {"User-Agent": "HLB-danh-muc/1.0"}


# ---------- Chung ----------

def gio_vn():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(timespec="seconds")


def get(url, as_json=True):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8")
    return json.loads(body) if as_json else body


def auth_hoac_none():
    if os.environ.get("WP_USER") and os.environ.get("WP_APP_PASSWORD"):
        return wp_draft.credentials()
    return None


def khong_dau(text):
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn").lower()


def tu(text):
    return re.findall(r"[a-z0-9]+", khong_dau(text))


def doc_json(path, mac_dinh=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return mac_dinh


def ghi_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ten_file(article):
    return os.path.splitext(os.path.basename(article))[0]


def trang_thai_path(article):
    return os.path.join(THU_MUC, ten_file(article) + ".json")


# ---------- Danh muc tren website ----------

def tat_ca_danh_muc():
    out, page = [], 1
    while True:
        res = get(wp_draft.API + "/wp/v2/product_cat?per_page=100&page=%d&_fields=id,slug,name,count,parent,link,description" % page)
        out += res
        if len(res) < 100:
            return out
        page += 1


def ten_day_du(c, by_id):
    """Ten danh muc con kem cong suat cua danh muc cha, vi du 'Đèn LED nhà xưởng Philips' + '150w'."""
    p = by_id.get(c["parent"])
    if not p:
        return html.unescape(c["name"])
    cong_suat = re.findall(r"\d+\s*w\b", p["name"].lower())
    return html.unescape(c["name"]) + (" " + cong_suat[0] if cong_suat and cong_suat[0] not in c["name"].lower() else "")


def tim_danh_muc(ref, ds=None):
    ds = ds or tat_ca_danh_muc()
    ref = str(ref).strip()
    m = re.search(r"/([a-z0-9-]+)/?$", ref)
    for c in ds:
        if ref == str(c["id"]) or ref == c["slug"] or (m and m.group(1) == c["slug"]):
            return c
    sys.exit("Không thấy danh mục '%s'. Chạy python tools/danh_muc.py ds để xem danh sách." % ref)


def diem_khop(tu_khoa, ten):
    a, b = set(tu(tu_khoa)), set(tu(ten))
    so_a = {x for x in a if re.search(r"\d", x)}
    so_b = {x for x in b if re.search(r"\d", x)}
    if so_a != so_b:  # cong suat khac nhau (150w vs 200w) thi khong phai cung danh muc
        return 0.0
    bo_qua = {"led"}  # "đèn nhà xưởng 150w" va "đèn LED nhà xưởng 150w" la mot
    a2, b2 = a - bo_qua, b - bo_qua
    return len(a2 & b2) / len(a2 | b2) if a2 | b2 else 0.0


def cmd_ds(_args):
    ds = tat_ca_danh_muc()
    by_id = {c["id"]: c for c in ds}
    for c in sorted(ds, key=lambda c: (c["parent"] or c["id"], c["parent"] != 0, c["slug"])):
        print("%5d %s%-26s %3d sp, mô tả %6d ký tự  %s" % (
            c["id"], "  " if c["parent"] else "", c["slug"], c["count"], len(c.get("description") or ""), ten_day_du(c, by_id)))


def cmd_tim(args):
    ds = tat_ca_danh_muc()
    by_id = {c["id"]: c for c in ds}
    kq = sorted(((diem_khop(args.tu_khoa, ten_day_du(c, by_id)), c) for c in ds if c["count"]), key=lambda x: -x[0])
    # KHOP: cung bo tu (bo qua "led"), giao ngay cho Agent Danh muc. GAN: khac 1 tu (hang, "gia"...), de SERP quyet
    tot = [(d, c) for d, c in kq if d >= 0.9]
    gan = [(d, c) for d, c in kq if 0.5 <= d < 0.9][:3]
    for d, c in tot + gan:
        print("%s %.2f  %s  %s (%d sp)" % ("KHỚP" if d >= 0.9 else "GẦN ", d, c["slug"], c["link"], c["count"]))
    if not tot and not gan:
        print("KHÔNG KHỚP: website không có danh mục sản phẩm nào gần với \"%s\"." % args.tu_khoa)
    sys.exit(0 if tot else 1)


# ---------- Doc noi dung cu ----------

class KhoiMoTa(html.parser.HTMLParser):
    """Lay HTML ben trong cac the <div class="... term-description ..."> cua trang danh muc (theme co 2 khoi)."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.khoi, self.sau, self.buf = [], 0, None

    def handle_starttag(self, tag, attrs):
        if self.buf is not None:
            if tag == "div":
                self.sau += 1
            self.buf.append(self.get_starttag_text())
        elif tag == "div" and "term-description" in (dict(attrs).get("class") or "").split():
            self.buf, self.sau = [], 1

    def handle_startendtag(self, tag, attrs):
        if self.buf is not None:
            self.buf.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.buf is None:
            return
        if tag == "div":
            self.sau -= 1
            if self.sau == 0:
                self.khoi.append("".join(self.buf).strip())
                self.buf = None
                return
        self.buf.append("</%s>" % tag)

    def handle_data(self, data):
        if self.buf is not None:
            self.buf.append(data)

    def handle_entityref(self, name):
        if self.buf is not None:
            self.buf.append("&%s;" % name)

    def handle_charref(self, name):
        if self.buf is not None:
            self.buf.append("&#%s;" % name)


def van_ban(h):
    h = re.sub(r"<div id=\"ez-toc-container\".*?</nav>\s*</div>", " ", h, flags=re.S)  # bo muc luc tu dong
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"</(p|h[1-6]|li|tr|div)>|<br\s*/?>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return "\n".join(re.sub(r"[ \t\xa0]+", " ", l).strip() for l in t.splitlines() if l.strip())


def doc_trang(link):
    """Trang danh muc cong khai: khoi tren, khoi duoi (HTML), title, meta description."""
    h = get(link, as_json=False)
    p = KhoiMoTa()
    p.feed(h)
    title = re.search(r"<title>(.*?)</title>", h, re.S)
    meta = re.search(r'<meta name="description" content="([^"]*)"', h)
    return {
        "khoi": p.khoi,
        "title": html.unescape(title.group(1).strip()) if title else "",
        "meta": html.unescape(meta.group(1)) if meta else "",
    }


def tach_khoi_trang(trang, description):
    """Khoi nao la description (khoi duoi): khoi co doan van ban dau tien cua description."""
    mau = van_ban(description)[:80]
    tren, duoi = "", ""
    for k in trang["khoi"]:
        if mau and mau[:40] in van_ban(k):
            duoi = k
        elif not tren:
            tren = k
    return tren, duoi


def doc_csv():
    found = sorted((f for f in os.listdir(ROOT) if re.match(r"du_lieu_san_pham_.*\.csv$", f)),
                   key=lambda f: re.findall(r"(\d{2})-(\d{2})-(\d{4})", f)[-1][::-1] if re.findall(r"(\d{2})-(\d{2})-(\d{4})", f) else ())
    if not found:
        return {}, None
    with open(os.path.join(ROOT, found[-1]), encoding="utf-8-sig") as f:
        return {r["url"].rstrip("/"): r for r in csv.DictReader(f)}, found[-1]


def san_pham_danh_muc(term_id):
    out, page = [], 1
    while True:
        res = get(wp_draft.API + "/wc/store/v1/products?category=%d&per_page=100&page=%d" % (term_id, page))
        out += res
        if len(res) < 100:
            return out
        page += 1


def gia(p):
    pr = p.get("prices") or {}
    try:
        return int(pr.get("price") or 0) // (10 ** int(pr.get("currency_minor_unit") or 0))
    except ValueError:
        return 0


def cmd_doc(args):
    ds = tat_ca_danh_muc()
    c = tim_danh_muc(args.ref, ds)
    by_id = {x["id"]: x for x in ds}
    auth = auth_hoac_none()
    desc = c.get("description") or ""
    if auth:
        try:
            desc = wp_draft.call("GET", "/wp/v2/product_cat/%d?context=edit" % c["id"], auth=auth)["description"]
        except RuntimeError as e:
            print("Chưa đọc được bản gốc (context=edit), dùng bản hiển thị:", e)
    trang = doc_trang(c["link"])
    tren, duoi = tach_khoi_trang(trang, desc)
    rows, csv_name = doc_csv()
    sp = []
    for p in san_pham_danh_muc(c["id"]):
        r = rows.get(p["permalink"].rstrip("/"))
        sp.append({
            "id": p["id"], "ten": html.unescape(p["name"]), "link": p["permalink"], "gia": gia(p),
            "thong_so": {k: r[k] for k in ("brand", "bh", "ip", "w", "pf", "lm", "life", "cct", "ra", "cert", "goc")} if r else None,
        })
    thu_muc = os.path.join(NGHIEN_CUU, "DM_" + c["slug"])
    info = {
        "id": c["id"], "slug": c["slug"], "ten": html.unescape(c["name"]), "ten_day_du": ten_day_du(c, by_id),
        "link": c["link"], "cha": by_id[c["parent"]]["slug"] if c["parent"] in by_id else "",
        "con": [x["slug"] for x in ds if x["parent"] == c["id"]],
        "khoi_tren_html": tren, "khoi_duoi_html": desc, "seo_title": trang["title"], "meta_description": trang["meta"],
        "csv": csv_name, "doc_luc": gio_vn(),
    }
    ghi_json(os.path.join(thu_muc, "danh_muc.json"), info)
    ghi_json(os.path.join(thu_muc, "san_pham.json"), sp)
    with open(os.path.join(thu_muc, "noi_dung_cu.md"), "w", encoding="utf-8") as f:
        f.write("# Nội dung cũ: %s\n\nĐọc lúc %s từ %s\n\nSEO title: %s\n\nMeta description: %s\n\n## Khối trên\n\n%s\n\n## Khối dưới\n\n%s\n"
                % (info["ten_day_du"], info["doc_luc"], c["link"], trang["title"], trang["meta"],
                   van_ban(tren) or "(trống)", van_ban(desc) or "(trống)"))
    with open(os.path.join(thu_muc, "san_pham.md"), "w", encoding="utf-8") as f:
        f.write("# Sản phẩm trong danh mục %s (%d)\n\nNguồn: API cửa hàng của website và %s, đọc lúc %s. "
                "Chỉ dùng số liệu trong bảng này, ô trống là trang sản phẩm chưa công bố.\n\n"
                "| Sản phẩm | Giá (đồng) | Hãng | W | lm | IP | Ra | Tuổi thọ (giờ) | Bảo hành |\n|---|---|---|---|---|---|---|---|---|\n"
                % (info["ten_day_du"], len(sp), csv_name or "(không có CSV)", info["doc_luc"]))
        for s in sp:
            t = s["thong_so"] or {}
            f.write("| [%s](%s) | %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
                s["ten"], s["link"], "{:,}".format(s["gia"]).replace(",", ".") if s["gia"] else "Liên hệ",
                t.get("brand", ""), t.get("w", ""), t.get("lm", ""), t.get("ip", ""), t.get("ra", ""), t.get("life", ""), t.get("bh", "")))
    thieu = [s["ten"] for s in sp if not s["thong_so"]]
    print("Danh mục %s (ID %d): %d sản phẩm, khối trên %d ký tự, khối dưới %d ký tự."
          % (info["ten_day_du"], c["id"], len(sp), len(van_ban(tren)), len(van_ban(desc))))
    print("Đã lưu vào %s: danh_muc.json, san_pham.json, san_pham.md, noi_dung_cu.md" % os.path.relpath(thu_muc, ROOT))
    if thieu:
        print("Sản phẩm chưa có trong CSV (chạy tools/lam_moi_csv.py rồi đọc lại, hoặc để [CẦN BỔ SUNG]): " + "; ".join(thieu))


# ---------- File bai DM_<slug>.md ----------

def doc_bai(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    sections, cur = {}, None
    for line in lines:
        m = re.match(r"^# ([ABC])\.", line)
        if m:
            cur = m.group(1)
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    for k in "ABC":
        if k not in sections:
            sys.exit("Thiếu phần %s trong %s" % (k, path))
    seo = {}
    for line in sections["A"]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] not in ("Trường", "") and not set(cells[0]) <= set("-: "):
            seo[cells[0]] = cells[1].strip("` ")
    tren, duoi, cur = [], [], None
    for line in sections["B"]:
        s = line.strip().strip("*")
        if s == KHOI_TREN:
            cur = tren
        elif s == KHOI_DUOI:
            cur = duoi
        elif cur is not None:
            cur.append(line)
    if not tren or not duoi:
        sys.exit("Phần B cần 2 dòng đánh dấu %s và %s" % (KHOI_TREN, KHOI_DUOI))
    return seo, tren, duoi, sections["C"]


def html_khoi(lines, images):
    body = wp_draft.mark_images(lines, images)
    return wp_draft.md_to_html(body)


def chuan_bi_anh(article, tren, duoi, auth=None):
    """Anh da duyet trong anh/DM_<slug>/anh.json: tai len Media khi --post (giong wp_draft.py). Tra ve (images, thieu, src_of)."""
    images = wp_draft.load_images(article)
    if not images:
        return {}, [], None
    images, missing = wp_draft.split_images(images, tren + duoi)
    if auth and images:
        all_images = wp_draft.load_images(article)
        for a in images.values():
            if a["nguon"] == "website":
                continue
            path = os.path.join(ROOT, a["file"])
            with open(path, "rb") as f:
                digest = hashlib.sha256(f.read()).hexdigest()
            if not (a.get("media_id") and a.get("url_da_tai") and a.get("sha_da_tai") == digest):
                a["media_id"], a["url_da_tai"] = wp_draft.upload_media(
                    path, wp_draft.hoa_dau(a["alt"]), wp_draft.hoa_dau(a["alt"]), wp_draft.media_description(a), auth)
                a["sha_da_tai"] = digest
                print("Đã tải ảnh lên Media ID %d: %s" % (a["media_id"], a["url_da_tai"]))
        manifest = doc_json(wp_draft.manifest_path(article), {})
        manifest["anh"] = [images.get(t, a) for t, a in all_images.items()]
        ghi_json(wp_draft.manifest_path(article), manifest)
    return images, missing, (lambda a: a.get("url_da_tai") or a.get("url_website") or a["file"])


def noi_dung(article, auth=None):
    seo, tren, duoi, ghi_chu = doc_bai(article)
    images, missing, src_of = chuan_bi_anh(article, tren, duoi, auth)
    h_tren, h_duoi = html_khoi(tren, images), html_khoi(duoi, images)
    if images:
        h_tren = wp_draft.insert_images(h_tren, images, src_of)
        h_duoi = wp_draft.insert_images(h_duoi, images, src_of)
    return seo, h_tren, h_duoi, ghi_chu, missing


def danh_muc_cua_bai(seo):
    ref = seo.get("Term ID") or seo.get("Danh mục") or seo.get("Link danh mục")
    if not ref:
        sys.exit("Phần A thiếu dòng Term ID hoặc Danh mục (slug)")
    return tim_danh_muc(ref)


def kiem_phieu(article):
    import phieu_duyet
    reasons = phieu_duyet.kiem(os.path.abspath(article))
    if reasons:
        print("Chưa được ghi lên website:", file=sys.stderr)
        for r in reasons:
            print("- " + r, file=sys.stderr)
        sys.exit("Làm theo vòng duyệt trong CLAUDE.md (bài DM_*.md chấm như bài blog, thang danh mục).")


# ---------- Trang nhap ----------

def ghi_chu_nhap(c, seo, ghi_chu, missing):
    rows = [("Danh mục", '<a href="%s">%s</a> (ID %d)' % (c["link"], html.escape(html.unescape(c["name"])), c["id"])),
            ("Focus keyword", html.escape(seo.get("Focus keyword", ""))),
            ("SEO title", html.escape(seo.get("SEO title", ""))),
            ("Meta description", html.escape(seo.get("Meta description", "")))]
    bang = "<table><tbody>%s</tbody></table>" % "".join(
        "<tr><td><strong>%s</strong></td><td>%s</td></tr>" % (k, v) for k, v in rows)
    thieu = ("<p><strong>ẢNH CÒN THIẾU:</strong> %s</p>" % html.escape(", ".join(missing))) if missing else ""
    return ("<p><strong>BẢN NHÁP NỘI DUNG DANH MỤC, KHÔNG ĐĂNG TRANG NÀY.</strong> Trang này chỉ để xem trước. "
            "Khi bạn bấm \"Duyệt, cập nhật lên danh mục\" trên Bảng điều phối, Agent chép nội dung vào danh mục thật "
            "(sao lưu bản cũ trước) rồi chuyển trang nháp này vào Thùng rác.</p>\n%s\n%s\n%s\n<hr>\n"
            % (bang, wp_draft.md_to_html(ghi_chu, headings=False), thieu))


def ghep_trang(c, seo, h_tren, h_duoi, ghi_chu, missing):
    return (ghi_chu_nhap(c, seo, ghi_chu, missing)
            + "<p><strong>KHỐI TRÊN (hiện trên lưới sản phẩm)</strong></p>\n" + h_tren
            + '\n[products category="%s" limit="8" columns="4" paginate="false"]\n' % c["slug"]
            + "<p><strong>KHỐI DƯỚI (hiện sau lưới sản phẩm)</strong></p>\n" + h_duoi)


def cmd_nhap(args):
    if args.post:
        kiem_phieu(args.article)
    auth = wp_draft.credentials() if args.post else None
    seo, h_tren, h_duoi, ghi_chu, missing = noi_dung(args.article, auth)
    c = danh_muc_cua_bai(seo)
    content = ghep_trang(c, seo, h_tren, h_duoi, ghi_chu, missing)
    title = TIEN_TO_NHAP + html.unescape(c["name"]) + (" (%s)" % c["slug"] if c["parent"] else "")
    preview = os.path.splitext(args.article)[0] + ".preview.html"
    with open(preview, "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8><title>%s</title><h1>%s</h1>\n%s"
                % (html.escape(title), html.escape(title), content))
    print("File xem trước:", preview)
    if not args.post:
        print("Chưa gửi lên website. Thêm --post để tạo hoặc cập nhật Trang nháp.")
        return
    st = doc_json(trang_thai_path(args.article), {})
    page_id = st.get("trang_nhap_id")
    if page_id:
        try:
            cur = wp_draft.call("GET", "/wp/v2/pages/%d?context=edit&_fields=id,status" % page_id, auth=auth)
        except RuntimeError:
            cur = {"status": "mat"}
        if cur["status"] != "draft":
            print("Trang nháp cũ ID %s không còn ở trạng thái nháp (%s), tạo trang mới." % (page_id, cur["status"]))
            page_id = None
    data = {"title": title, "content": content, "status": "draft"}
    if page_id:
        wp_draft.call("POST", "/wp/v2/pages/%d" % page_id, data, auth=auth)
        print("Đã cập nhật Trang nháp ID", page_id)
    else:
        page_id = wp_draft.call("POST", "/wp/v2/pages", dict(data, slug="nhap-danh-muc-%s" % c["slug"]), auth=auth)["id"]
        print("Đã tạo Trang nháp ID", page_id)
    with open(args.article, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    st.update({"term_id": c["id"], "slug": c["slug"], "link": c["link"], "trang_nhap_id": page_id,
               "link_nhap": "%s/wp-admin/post.php?post=%d&action=edit" % (SITE, page_id),
               "link_xem": "%s/?page_id=%d&preview=true" % (SITE, page_id),
               "nhap_khop": {"luc": gio_vn(), "sha": sha}})
    ghi_json(trang_thai_path(args.article), st)
    print("Xem trước (cần đăng nhập wp-admin):", st["link_xem"])
    print("Sửa trong wp-admin:", st["link_nhap"])


# ---------- Ap dung, sao luu, khoi phuc ----------

def ghi_rank_math(term_id, meta, auth):
    wp_draft.call("POST", "/rankmath/v1/updateMeta", {"objectType": "term", "objectID": term_id, "meta": meta}, auth=auth)


def sao_luu(c, auth):
    desc = wp_draft.call("GET", "/wp/v2/product_cat/%d?context=edit" % c["id"], auth=auth)["description"]
    trang = doc_trang(c["link"])
    tren, _ = tach_khoi_trang(trang, desc)
    ban = {"term_id": c["id"], "slug": c["slug"], "link": c["link"], "luc": gio_vn(), "description": desc,
           "khoi_tren_html": tren, "seo_title": trang["title"], "meta_description": trang["meta"]}
    path = os.path.join(SAO_LUU, "%s_%s.json" % (c["slug"], datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))
    ghi_json(path, ban)
    return path, ban


def mau_cau(h, n=1):
    """Vai doan van ban dai cua noi dung moi, de kiem tra trang cong khai da hien dung ban nay."""
    cau = [l for l in van_ban(h).splitlines() if len(l) > 60]
    return [c[:60] for c in cau[:n]]


def cmd_ap_dung(args):
    if not args.duyet_luc:
        sys.exit("Thiếu --duyet-luc: giờ người dùng bấm \"Duyệt, cập nhật lên danh mục\" trên Bảng điều phối "
                 "(trường duyet_ap_dung_luc). Chưa có thì không áp dụng.")
    if args.post:
        kiem_phieu(args.article)
    auth = wp_draft.credentials()
    seo, h_tren, h_duoi, _ghi_chu, missing = noi_dung(args.article, auth if args.post else None)
    if missing:
        sys.exit("Còn ảnh chưa duyệt hoặc thiếu: %s. Duyệt đủ ảnh (hoặc bỏ dòng [ẢNH]) trước khi áp dụng." % ", ".join(missing))
    c = danh_muc_cua_bai(seo)
    khoa_tren = (doc_json(CAU_HINH, {}) or {}).get("khoi_tren_meta")
    meta = {"rank_math_title": seo.get("SEO title", ""), "rank_math_description": seo.get("Meta description", ""),
            "rank_math_focus_keyword": seo.get("Focus keyword", "")}
    print("Danh mục %s (ID %d), %s" % (html.unescape(c["name"]), c["id"], c["link"]))
    print("Ghi: khối dưới (description) %d ký tự; Rank Math: SEO title, meta description, focus keyword." % len(h_duoi))
    print("Khối trên: %s" % ("ghi vào trường " + khoa_tren if khoa_tren else
                             "theme chưa mở trường này qua REST, ghi file HTML để dán tay"))
    if not args.post:
        print("Chạy thử, chưa ghi gì. Thêm --post để áp dụng.")
        return
    path, _ban = sao_luu(c, auth)
    print("Đã sao lưu bản cũ:", os.path.relpath(path, ROOT))
    data = {"description": h_duoi}
    if khoa_tren:
        data["meta"] = {khoa_tren: h_tren}
    res = wp_draft.call("POST", "/wp/v2/product_cat/%d" % c["id"], data, auth=auth)
    if khoa_tren and (res.get("meta") or {}).get(khoa_tren) != h_tren:
        print("Cảnh báo: trường %s không nhận qua REST, khối trên vẫn cần dán tay." % khoa_tren)
        khoa_tren = None
    ghi_rank_math(c["id"], meta, auth)
    print("Đã ghi khối dưới và Rank Math.")
    st = doc_json(trang_thai_path(args.article), {})
    with open(args.article, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    st.update({"term_id": c["id"], "slug": c["slug"], "link": c["link"],
               "ap_dung": {"luc": gio_vn(), "sha": sha, "duyet_luc": args.duyet_luc, "sao_luu": os.path.relpath(path, ROOT),
                           "khoi_tren": "da_ghi" if khoa_tren else "cho_dan"}})
    if not khoa_tren:
        f_tren = os.path.join(THU_MUC, ten_file(args.article) + ".khoi_tren.html")
        with open(f_tren, "w", encoding="utf-8") as f:
            f.write(h_tren)
        st["ap_dung"]["file_khoi_tren"] = os.path.relpath(f_tren, ROOT)
        print("Khối trên chờ dán tay: %s (đưa lên bảng để người dùng chép)." % os.path.relpath(f_tren, ROOT))
    ghi_json(trang_thai_path(args.article), st)
    ok = kiem_trang(args.article, in_ra=True)
    if ok.get("duoi") and st.get("trang_nhap_id"):
        try:
            wp_draft.call("DELETE", "/wp/v2/pages/%d" % st["trang_nhap_id"], auth=auth)  # khong force: vao Thung rac
            print("Đã chuyển Trang nháp ID %d vào Thùng rác." % st["trang_nhap_id"])
            st["trang_nhap_id"] = None
            ghi_json(trang_thai_path(args.article), st)
        except RuntimeError as e:
            print("Chưa chuyển được Trang nháp vào Thùng rác:", e)


def kiem_trang(article, in_ra=False):
    seo, h_tren, h_duoi, _g, _m = noi_dung(article)
    c = danh_muc_cua_bai(seo)
    trang = doc_trang(c["link"] + ("&" if "?" in c["link"] else "?") + "kiem=%d" % int(datetime.datetime.now().timestamp()))
    toan_bo = van_ban("".join(trang["khoi"]))
    kq = {"duoi": all(m in toan_bo for m in mau_cau(h_duoi, 2)),
          "tren": all(m in toan_bo for m in mau_cau(h_tren, 1)),
          "title": trang["title"].strip() == seo.get("SEO title", "").strip(),
          "meta": trang["meta"].strip() == seo.get("Meta description", "").strip()}
    if in_ra:
        ten = {"duoi": "Khối dưới", "tren": "Khối trên", "title": "SEO title", "meta": "Meta description"}
        for k, v in kq.items():
            print("- %s: %s" % (ten[k], "khớp bản mới" if v else "CHƯA khớp (có thể do bộ nhớ đệm, thử lại sau vài phút)"))
    return kq


def cmd_kiem_trang(args):
    kq = kiem_trang(args.article, in_ra=True)
    st = doc_json(trang_thai_path(args.article), {})
    if st.get("ap_dung"):
        st["ap_dung"]["kiem_luc"] = gio_vn()
        st["ap_dung"]["kiem"] = kq
        if kq["tren"]:
            st["ap_dung"]["khoi_tren"] = "da_ghi"
        ghi_json(trang_thai_path(args.article), st)
    sys.exit(0 if all(kq.values()) else 1)


def cmd_khoi_phuc(args):
    c = tim_danh_muc(args.slug)
    if args.ban:
        path = args.ban
    else:
        bans = sorted(f for f in os.listdir(SAO_LUU) if f.startswith(c["slug"] + "_")) if os.path.isdir(SAO_LUU) else []
        if not bans:
            sys.exit("Không có bản sao lưu nào của %s trong danh_muc/sao_luu/" % c["slug"])
        path = os.path.join(SAO_LUU, bans[-1])
    ban = doc_json(path)
    print("Khôi phục %s từ %s (lưu lúc %s)" % (c["slug"], os.path.relpath(path, ROOT), ban["luc"]))
    if not args.post:
        print("Chạy thử, chưa ghi gì. Thêm --post để khôi phục.")
        return
    auth = wp_draft.credentials()
    sao_luu(c, auth)  # luu ca ban hien tai truoc khi ghi lai, de khoi phuc nham van quay lai duoc
    wp_draft.call("POST", "/wp/v2/product_cat/%d" % c["id"], {"description": ban["description"]}, auth=auth)
    ghi_rank_math(c["id"], {"rank_math_title": ban["seo_title"], "rank_math_description": ban["meta_description"]}, auth)
    print("Đã ghi lại khối dưới, SEO title, meta description cũ.")
    if ban.get("khoi_tren_html"):
        print("Khối trên cũ (dán tay nếu đã đổi): xem trường khoi_tren_html trong", os.path.relpath(path, ROOT))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ds").set_defaults(func=cmd_ds)
    t = sub.add_parser("tim")
    t.add_argument("tu_khoa")
    t.set_defaults(func=cmd_tim)
    d = sub.add_parser("doc")
    d.add_argument("ref", help="slug, ID hoac link danh muc")
    d.set_defaults(func=cmd_doc)
    n = sub.add_parser("nhap")
    n.add_argument("article")
    n.add_argument("--post", action="store_true")
    n.set_defaults(func=cmd_nhap)
    a = sub.add_parser("ap-dung")
    a.add_argument("article")
    a.add_argument("--duyet-luc", help="gio nguoi dung bam Duyet tren bang (truong duyet_ap_dung_luc)")
    a.add_argument("--post", action="store_true")
    a.set_defaults(func=cmd_ap_dung)
    k = sub.add_parser("kiem-trang")
    k.add_argument("article")
    k.set_defaults(func=cmd_kiem_trang)
    r = sub.add_parser("khoi-phuc")
    r.add_argument("slug")
    r.add_argument("--ban", help="file sao luu cu the (mac dinh: ban moi nhat)")
    r.add_argument("--post", action="store_true")
    r.set_defaults(func=cmd_khoi_phuc)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
