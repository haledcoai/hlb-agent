"""Kiem tra loi co hoc cua bai viet (file .md co phan A, B, C) truoc khi dua ban nhap len website.

Cach dung:
  python tools/kiem_tra_bai.py <file_bai.md>
  python tools/kiem_tra_bai.py <file_bai.md> --csv du_lieu_san_pham_HLB_21-10-2026.csv

Chi bat loi may kiem tra duoc: dau gach, emoji, tu cam, link, do dai SEO, dinh dang so,
doi chieu so lieu voi file CSV san pham. Chat luong noi dung do agent danh-gia-noi-dung danh gia.
Ma thoat: 0 = khong co LOI, 1 = co LOI can sua, 2 = file sai cau truc.
"""
import argparse
import csv
import glob
import os
import re
import sys
import unicodedata

SITE_HOST = "denlednhaxuongcaocap.com"
HOTLINES = {"0967569588", "02437918122"}

LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
PLACEHOLDER = re.compile(r"\[(CẦN BỔ SUNG|CẦN KIỂM TRA|CHỜ XÁC NHẬN|LINK|ẢNH)[^\]]*\]")
IMAGE = re.compile(r"\[ẢNH:([^\]]*)\]")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")

# Khong link toi cac domain nay (Instructions muc 2, muc 7; Knowledge 9.3)
BANNED_DOMAINS = ("haledco.com", "philips.", "signify.com", "rangdong", "dienquang",
                  "shopee.", "lazada.", "tiki.vn", "sendo.vn")
GENERIC_ANCHOR = ("tại đây", "xem thêm", "click", "bấm vào", "link này")

# Tu tuyet doi (Instructions muc 5, Knowledge 8.4)
ABSOLUTE = ["100%", "duy nhất", r"số 1(?![\d.,])", "hoàn hảo", "tốt nhất", "rẻ nhất", "hot nhất",
            "hàng đầu", "vượt trội", "siêu sáng", "đứng đầu"]

# Cum van mau kieu AI (Knowledge 8.4)
AI_PHRASES = [
    "trong thời đại công nghệ", r"(^|[.!?]\s+)ngày nay", r"hiện nay,.*ngày càng phổ biến",
    "không còn xa lạ", "bạn đang băn khoăn", "hãy cùng tìm hiểu", "bài viết dưới đây sẽ giúp",
    "trong bài viết này", "đóng vai trò quan trọng", "không thể phủ nhận", "có thể nói",
    "đáng chú ý là", "một cách hiệu quả", "đáp ứng mọi nhu cầu", "giải pháp tối ưu",
    "lựa chọn hàng đầu", "nâng tầm", "trải nghiệm tuyệt vời", "xu hướng tất yếu", "chìa khóa",
    "bí quyết", "khám phá", "tất tần tật", r"(^|[.!?]\s+)tóm lại", r"(^|[.!?]\s+)nhìn chung",
    "như vậy có thể thấy", "hy vọng bài viết", "đừng ngần ngại",
]

# Cau quang cao chua kiem chung tren website (Knowledge muc 5)
UNVERIFIED = {
    r"70\s*%.{0,20}điện": "\"tiết kiệm 70% điện\" không nêu so với đèn nào",
    r"làm mát.{0,20}30\s*%": "\"tăng hiệu quả làm mát 30%\" không có nguồn",
    r"chiếu sáng liên tục quá 10": "câu \"không nên chiếu sáng quá 10 tiếng\" mâu thuẫn thực tế",
    r"trong vòng tuần": "\"đổi trả trong vòng tuần\" thiếu số ngày",
    r"graphene|tcplus": "công nghệ tản nhiệt chưa có tài liệu, chỉ nêu dạng \"theo công bố trên trang sản phẩm\"",
}

# Vai tro thuong hieu (Knowledge muc 1)
BRAND_ROLE = {
    r"hlb\s+(tự\s+)?sản xuất": "HLB phân phối đèn LED nhiều thương hiệu, không viết \"HLB sản xuất\"",
    r"nhà máy của (chúng tôi|hlb)": "HLB là đơn vị phân phối, không có nhà máy",
    r"(do|của)\s+haledco\s+(sản xuất|lắp ráp)|haledco\s+sản xuất\s*(và lắp ráp)?\s*,\s*hlb": "không gán dòng cao cấp cho HALEDCO sản xuất; viết \"HLB phân phối\" (HALEDCO là một thương hiệu HLB phân phối)",
    r"chúng tôi (tự\s+)?sản xuất": "HLB là đơn vị phân phối, không sản xuất",
    r"hlb.{0,40}từ (năm )?2011": "mốc 2011 là của HALEDCO, HLB phân phối từ 2018",
    r"\d+\s+năm kinh nghiệm": "không tự tính số năm kinh nghiệm, ghi năm bắt đầu",
    r"haledco\.com": "không nhắc hoặc link haledco.com",
}

# Thuat ngu thong nhat (Knowledge muc 7)
TERMS = {
    "cos phi": "hệ số công suất (PF)", "rửa sáng": "chiếu sáng phủ đều", "mạnh mẽ": "chiếu sáng mạnh",
    "hiệu suất phát quang": "hiệu suất chiếu sáng", "hiệu quả phát sáng": "hiệu suất chiếu sáng",
    "cường độ sáng": "độ rọi", "nguồn led": "driver (bộ nguồn)", "nguồn đèn": "driver (bộ nguồn)",
    "góc mở": "góc chiếu", "độ trung thực màu": "chỉ số hoàn màu (Ra)",
    "chỉ số chống nước": "cấp bảo vệ IP",
}

# Cau noi toi da 2 lan moi kieu (Instructions muc 5)
CONNECTORS = {
    "Điều này": r"\bđiều này\b", "Ngoài ra": r"\bngoài ra\b", "Bên cạnh đó": r"\bbên cạnh đó\b",
    "Không chỉ... mà còn": r"\bkhông chỉ\b.*\bmà còn\b", "Việc... (đầu câu)": r"(^|[.!?]\s+)việc\s",
}

# Dinh dang so (Knowledge 8.3)
NUMBER_RULES = [
    (re.compile(r"\b\d+ W\b(?!/)"),"công suất viết liền, ví dụ 100W"),
    (re.compile(r"\b\d{4} K\b"), "nhiệt độ màu viết liền, ví dụ 6500K"),
    (re.compile(r"(?<![\d.\w])\d+\.\d{1,2}(?![\d.])"), "số thập phân dùng dấu phẩy, ví dụ 0,98"),
    (re.compile(r"(?<![\d.,/\w-])\d{5,}(?![\d.,])\s*(lm|giờ|đồng|lux|m²)"), "hàng nghìn dùng dấu chấm, ví dụ 19.500 lm"),
    (re.compile(r"(?<![\d.,])\d{1,3},\d{3}(?![\d,])"), "nếu là hàng nghìn thì dùng dấu chấm (1.200), dấu phẩy chỉ cho thập phân"),
    (re.compile(r"\d\s+-\s+\d"), "khoảng giá trị dùng hyphen không dấu cách, ví dụ 6-8 m"),
    (re.compile(r"\d(lm/W|lm|lux)\b"), "đơn vị có dấu cách, ví dụ 130 lm/W, 300 lux"),
]


class Report:
    def __init__(self):
        self.items = {"LỖI": [], "CẢNH BÁO": [], "THÔNG TIN": []}

    def add(self, level, line, msg):
        self.items[level].append((line, msg))

    def error(self, line, msg):
        self.add("LỖI", line, msg)

    def warn(self, line, msg):
        self.add("CẢNH BÁO", line, msg)

    def info(self, line, msg):
        self.add("THÔNG TIN", line, msg)


def no_accent(text):
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def norm(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def to_int(num):
    return int(re.sub(r"[.,\s]", "", num))


def short(text, n=70):
    text = text.strip()
    return text if len(text) <= n else text[:n] + "..."


# ---------- Doc file bai viet ----------

def parse(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    sections, current = {}, None
    for no, line in enumerate(lines, 1):
        m = re.match(r"^# ([ABC])\.", line)
        if m:
            current = m.group(1)
            sections[current] = []
        elif current:
            sections[current].append((no, line))
    return sections


def seo_fields(section_a):
    seo = {}
    for no, line in section_a:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] not in ("Trường", "") and not set(cells[0]) <= set("-: "):
            seo[cells[0]] = (no, cells[1])
    return seo


def strip_markup(text):
    text = PLACEHOLDER.sub(" ", text)
    text = LINK.sub(r"\1", text)
    return re.sub(r"[*`#|]", " ", text)


# ---------- Cac nhom kiem tra ----------

def check_text(rep, lines):
    """Dau gach, emoji, tu cam, thuat ngu, so dien thoai. Ap dung cho phan A va B."""
    for no, line in lines:
        if "—" in line or "–" in line:
            rep.error(no, "Có em dash/en dash, thay bằng dấu phẩy, dấu chấm hoặc hyphen (-): " + short(line))
        if EMOJI.search(line):
            rep.error(no, "Có emoji: " + short(line))
        text = norm(strip_markup(line))
        for pat in ABSOLUTE:
            m = re.search(pat, text)
            if m:
                rep.error(no, "Từ tuyệt đối \"%s\": %s" % (m.group(0), short(line)))
        for pat in AI_PHRASES:
            m = re.search(pat, text)
            if m:
                rep.error(no, "Cụm văn mẫu kiểu AI \"%s\": %s" % (m.group(0).strip(" .!?"), short(line)))
        for pat, why in UNVERIFIED.items():
            if re.search(pat, text):
                rep.error(no, "Câu quảng cáo chưa kiểm chứng (Knowledge mục 5), %s" % why)
        for pat, why in BRAND_ROLE.items():
            if re.search(pat, norm(line)):
                rep.error(no, "Sai vai trò thương hiệu: %s" % why)
        for bad, good in TERMS.items():
            if bad in text:
                rep.warn(no, "Thuật ngữ \"%s\" nên thống nhất thành \"%s\"" % (bad, good))
        if "philips" in text and re.search(r"(bảo hành|bh).{0,20}24 tháng", text):
            rep.warn(no, "Philips bảo hành theo từng model, không viết chung 24 tháng")
        for m in re.finditer(r"(?<![\d,.])0[\d .]{8,13}\d(?![\d,])", line):
            digits = re.sub(r"\D", "", m.group(0))
            if len(digits) in (10, 11) and digits not in HOTLINES:
                rep.error(no, "Số điện thoại %s không phải hotline đã xác nhận (0967569588, 02437 918 122)" % m.group(0).strip())


def check_connectors(rep, body):
    text = norm(" ".join(strip_markup(l) for _, l in body))
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for name, pat in CONNECTORS.items():
        n = sum(1 for s in sentences if re.search(pat, s))
        if n > 2:
            rep.warn(None, "Câu nối \"%s\" dùng %d lần, tối đa 1-2 lần mỗi bài" % (name, n))


def check_numbers(rep, body):
    for no, line in body:
        text = LINK.sub(r"\1", PLACEHOLDER.sub(" ", line))
        if re.match(r"^#{1,4} ", line):
            continue
        for pat, why in NUMBER_RULES:
            m = pat.search(text)
            if m:
                rep.warn(no, "Định dạng số \"%s\": %s" % (m.group(0).strip(), why))


def check_structure(rep, body):
    h1 = [(no, l) for no, l in body if re.match(r"^# ", l)]
    if len(h1) != 1:
        rep.error(h1[1][0] if len(h1) > 1 else None, "Phần B phải có đúng 1 H1, đang có %d" % len(h1))
    prev, h3_children, last_h3 = 1, {}, None
    for no, line in body:
        m = re.match(r"^(#{1,6}) ", line)
        if not m:
            continue
        level = len(m.group(1))
        if level > prev + 1:
            rep.error(no, "Nhảy cấp heading từ H%d xuống H%d: %s" % (prev, level, short(line)))
        if level > 4:
            rep.error(no, "Không dùng heading cấp H%d" % level)
        if level == 3:
            last_h3 = no
            h3_children[no] = 0
        elif level == 4 and last_h3:
            h3_children[last_h3] += 1
        elif level <= 2:
            last_h3 = None
        prev = level
    for no, n in h3_children.items():
        if n == 1:
            rep.warn(no, "H3 này chỉ có 1 H4, H4 chỉ dùng khi có từ 2 ý con trở lên")

    # Doan van 2-4 cau, bang toi da 5 cot
    para, start = [], None

    def flush():
        nonlocal para, start
        if para:
            text = strip_markup(" ".join(para))
            n = len([s for s in re.split(r"[.!?](?:\s+|$)", text) if len(s.strip()) > 3])
            if n > 4:
                rep.warn(start, "Đoạn văn có %d câu, nên 2-4 câu: %s" % (n, short(para[0])))
        para, start = [], None

    for no, line in body:
        s = line.strip()
        if s.startswith("|"):
            flush()
            cells = s.strip("|").split("|")
            if len(cells) > 5 and not re.fullmatch(r"\|[\s:|-]+\|", s):
                rep.error(no, "Bảng có %d cột, tối đa 5 cột để đọc được trên điện thoại" % len(cells))
        elif not s or s == "---" or re.match(r"^(#{1,6} |- |\d+\. )", s) or PLACEHOLDER.fullmatch(s):
            flush()
        else:
            if not para:
                start = no
            para.append(s)
    flush()


def check_links(rep, body):
    internal, external, seen_url, seen_anchor = [], [], {}, {}
    for no, line in body:
        for anchor, url in LINK.findall(line):
            host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0].lower()
            low = url.lower()
            if any(d in low for d in BANNED_DOMAINS):
                rep.error(no, "Link bị cấm (haledco.com, website hãng đèn hoặc cửa hàng): " + url)
            if norm(anchor) in GENERIC_ANCHOR:
                rep.error(no, "Anchor chung chung \"%s\", cần mô tả đúng trang đích" % anchor)
            if url in seen_url:
                rep.error(no, "URL đã link ở dòng %d, mỗi URL chỉ link 1 lần: %s" % (seen_url[url], url))
            seen_url.setdefault(url, no)
            key = norm(anchor)
            if key in seen_anchor and seen_anchor[key] != url:
                rep.error(no, "Anchor \"%s\" đã dùng cho URL khác" % anchor)
            seen_anchor.setdefault(key, url)
            if host.endswith(SITE_HOST):
                internal.append(url)
            else:
                external.append(url)

    content = [u for u in set(internal) if "/lien-he/" not in u]
    category = [u for u in content if re.search(r"/den-led-nha-xuong-\d+w/", u)]
    if not 3 <= len(content) <= 5:
        rep.error(None, "Link nội bộ (không tính trang Liên hệ ở CTA): %d, cần 3-5" % len(content))
    if not 1 <= len(category) <= 3:
        rep.error(None, "Link về trang danh mục sản phẩm: %d, cần 1-3" % len(category))
    if len(set(external)) > 3:
        rep.error(None, "Link ngoài: %d, tối đa 3" % len(set(external)))
    rep.info(None, "Link nội bộ %d (danh mục %d), link ngoài %d, link CTA Liên hệ %d"
             % (len(content), len(category), len(set(external)), len(set(internal)) - len(content)))


def check_images(rep, body, slug=""):
    goc_slug = re.sub(r"-\d+$", "", slug)
    for no, line in body:
        for m in IMAGE.finditer(line):
            parts = {}
            for p in m.group(1).split("|"):
                k, _, v = p.partition(":")
                parts[k.strip().lower()] = v.strip()
            alt = parts.get("alt", "")
            name = parts.get("tên file", "")
            if not alt:
                rep.error(no, "Ảnh thiếu alt text")
            elif len(alt) > 125:
                rep.error(no, "Alt text dài %d ký tự, tối đa 125" % len(alt))
            if not name:
                rep.warn(no, "Ảnh thiếu tên file gợi ý")
            elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.jpg", name):
                rep.warn(no, "Tên file ảnh \"%s\" nên không dấu, chữ thường, nối bằng hyphen, đuôi .jpg (Knowledge 9.5)" % name)
            if name and goc_slug and re.sub(r"-\d+$", "", name[:-4] if name.endswith(".jpg") else name) == goc_slug:
                rep.error(no, "Tên ảnh \"%s\" trùng slug bài, WordPress có thể chuyển hướng link bài sang ảnh. "
                              "Thêm từ mô tả nội dung ảnh (Knowledge 9.5)" % name)


def check_seo(rep, seo, body):
    def field(name):
        return seo.get(name, (None, ""))

    kw_no, kw = field("Focus keyword")
    if not kw:
        rep.error(None, "Phần A thiếu Focus keyword")
        return
    kwn = norm(kw)

    no, title = field("SEO title")
    if not title:
        rep.error(None, "Phần A thiếu SEO title")
    else:
        if len(title) >= 60:
            rep.error(no, "SEO title dài %d ký tự, cần dưới 60" % len(title))
        if kwn not in norm(title):
            rep.error(no, "SEO title không chứa từ khóa chính \"%s\"" % kw)

    no, meta = field("Meta description")
    if not meta:
        rep.error(None, "Phần A thiếu Meta description")
    else:
        if not 120 <= len(meta) <= 160:
            rep.error(no, "Meta description dài %d ký tự, cần 120-160" % len(meta))
        if kwn not in norm(meta):
            rep.warn(no, "Meta description không chứa nguyên cụm từ khóa chính")

    no, slug_raw = field("Slug")
    slug = slug_raw.split(" ")[0] if slug_raw else ""
    if not slug:
        rep.error(None, "Phần A thiếu Slug")
    else:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            rep.error(no, "Slug \"%s\" phải không dấu, chữ thường, nối bằng hyphen" % slug)
        if not 3 <= len(slug.split("-")) <= 6:
            rep.warn(no, "Slug có %d từ, nên 3-6 từ" % len(slug.split("-")))
        if re.search(r"20\d\d", slug):
            rep.warn(no, "Slug không gắn năm")
        if no_accent(kwn).replace(" ", "-") not in slug:
            rep.warn(no, "Slug không chứa từ khóa chính%s" % (" (đã ghi giữ URL cũ)" if "giữ" in slug_raw else ""))

    no, excerpt = field("Excerpt")
    if excerpt and len(excerpt) >= 200:
        rep.error(no, "Excerpt dài %d ký tự, cần dưới 200" % len(excerpt))
    if excerpt and excerpt == meta:
        rep.error(no, "Excerpt trùng nguyên văn meta description")
    no, tags = field("Tag")
    n_tags = len([t for t in tags.split(",") if t.strip()])
    if not 3 <= n_tags <= 5:
        rep.warn(no, "Có %d tag, cần 3-5" % n_tags)
    if not field("Category")[1]:
        rep.warn(None, "Phần A thiếu Category")

    h1 = next(((n, l) for n, l in body if re.match(r"^# ", l)), None)
    if h1 and kwn not in norm(h1[1]):
        rep.error(h1[0], "H1 không chứa từ khóa chính \"%s\"" % kw)
    if not any(kwn in norm(l) for _, l in body if re.match(r"^## ", l)):
        rep.warn(None, "Không có H2 nào chứa nguyên cụm từ khóa chính")
    after = [l for _, l in body[body.index(h1) + 1:]] if h1 else []
    words = norm(strip_markup(" ".join(l for l in after if not re.match(r"^#", l)))).split()
    if kwn not in " ".join(words[:100]):
        rep.error(None, "Từ khóa chính không có trong 100 chữ đầu bài")


def check_placeholders(rep, body, notes):
    counts = {}
    for no, line in body:
        for m in PLACEHOLDER.finditer(line):
            counts.setdefault(m.group(1), []).append(no)
    for kind, nos in counts.items():
        if kind == "ẢNH":
            continue
        rep.info(None, "[%s] còn %d chỗ trong phần B, dòng %s" % (kind, len(nos), ", ".join(map(str, nos))))
    if not notes:
        rep.error(None, "Thiếu phần C. Ghi chú cho người duyệt")
    elif any(k in counts for k in ("CẦN BỔ SUNG", "CẦN KIỂM TRA", "LINK")):
        text = " ".join(l for _, l in notes)
        for kind in ("CẦN BỔ SUNG", "CẦN KIỂM TRA", "LINK"):
            if kind in counts and kind not in text:
                rep.error(None, "Phần B có [%s] nhưng phần C không liệt kê" % kind)


# ---------- Doi chieu voi file CSV san pham ----------

MODEL = re.compile(r"\b[A-Z]{2,}[A-Z0-9]*-\d+W?\b|\bHB0\dL \d+/\d+W\b")


def load_csv(path):
    models = {}
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            for code in MODEL.findall(row["name"]):
                models[code] = row
    return models


def check_against_csv(rep, body, models, csv_name):
    prices = {to_int(r["price"]) for r in models.values() if r["price"].strip("0 ")}
    for no, line in body:
        text = PLACEHOLDER.sub(" ", line)
        for m in re.finditer(r"(\d{1,3}(?:\.\d{3})+)\s*(đồng|đ\b|vnđ)", text, re.I):
            if to_int(m.group(1)) not in prices:
                rep.warn(no, "Giá %s không khớp sản phẩm nào trong %s" % (m.group(0), csv_name))
        codes = set(MODEL.findall(text))
        if len(codes) != 1:
            continue
        code = codes.pop()
        row = models.get(code)
        if not row:
            rep.warn(no, "Model %s không có trong %s, kiểm tra lại tên model" % (code, csv_name))
            continue
        lms = [to_int(x) for x in re.findall(r"(\d{1,3}(?:\.\d{3})+|\d{4,})\s*lm\b", text)]
        if lms and row["lm"] and to_int(row["lm"]) not in lms:
            rep.error(no, "%s: quang thông trong bài %s lm, CSV ghi %s lm" % (code, lms, row["lm"]))
        # Mot dong co the co nhieu gia tri (vi du "PF tu 0,9 tro len. BUFO4-150 cong bo PF 0,98"),
        # chi bao loi khi khong gia tri nao khop CSV
        pfs = [x.replace(",", ".") for x in re.findall(r"PF\D{0,10}(\d[,.]\d+)", text)]
        if pfs and row["pf"] and row["pf"] not in pfs:
            rep.error(no, "%s: PF trong bài %s, CSV ghi %s" % (code, ", ".join(pfs), row["pf"]))
        ras = re.findall(r"\bRa\D{0,10}(\d{2})\b", text)
        if ras and row["ra"] and row["ra"] not in ras:
            rep.error(no, "%s: Ra trong bài %s, CSV ghi %s" % (code, ", ".join(ras), row["ra"]))


# ---------- Chay ----------

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("--csv", help="file CSV san pham (mac dinh: file du_lieu_san_pham_*.csv moi nhat)")
    args = ap.parse_args()

    sections = parse(args.article)
    missing = [k for k in "AB" if k not in sections]
    if missing:
        print("File sai cấu trúc: thiếu phần %s (tiêu đề dạng \"# A.\", \"# B.\", \"# C.\")" % ", ".join(missing))
        sys.exit(2)
    a, b, c = sections["A"], sections["B"], sections.get("C", [])

    rep = Report()
    check_text(rep, a + b)
    check_connectors(rep, b)
    check_numbers(rep, b)
    check_structure(rep, b)
    check_links(rep, b)
    seo = seo_fields(a)
    check_images(rep, b, (seo.get("Slug", (None, ""))[1] or " ").split(" ")[0])
    check_seo(rep, seo, b)
    check_placeholders(rep, b, c)

    csv_path = args.csv
    if not csv_path:
        found = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(args.article)), "du_lieu_san_pham_*.csv")))
        csv_path = found[-1] if found else None
    if csv_path:
        check_against_csv(rep, b, load_csv(csv_path), os.path.basename(csv_path))
    else:
        rep.info(None, "Không tìm thấy file CSV sản phẩm, bỏ qua đối chiếu thông số và giá")

    print("KIỂM TRA CƠ HỌC: %s" % args.article)
    for level, items in rep.items.items():
        print("\n## %s (%d)" % (level, len(items)))
        for line, msg in sorted(items, key=lambda x: x[0] or 0):
            print("- %s%s" % ("[dòng %d] " % line if line else "", msg))
    n_err, n_warn = len(rep.items["LỖI"]), len(rep.items["CẢNH BÁO"])
    print("\nTổng: %d lỗi, %d cảnh báo. %s" % (
        n_err, n_warn, "Sửa hết LỖI trước khi đăng bản nháp." if n_err else "Không có lỗi cơ học."))
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
