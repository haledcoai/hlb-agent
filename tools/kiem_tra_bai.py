"""Kiem tra loi co hoc cua bai viet (file .md co phan A, B, C) truoc khi dua ban nhap len website.

Cach dung:
  python tools/kiem_tra_bai.py <file_bai.md>
  python tools/kiem_tra_bai.py <file_bai.md> --gon      # chi in LOI, CANH BAO va mot dong tom tat (agent danh gia dung)
  python tools/kiem_tra_bai.py <file_bai.md> --csv du_lieu_san_pham_HLB_26-10-2026.csv
  python tools/kiem_tra_bai.py --tra 16.500             # tra CSV: model, quang thong, gia, cong suat; dem so dong khop
  python tools/kiem_tra_bai.py --cap-nhat-quy-tac       # ghi lai ma file goc vao quy_tac_cham.md sau khi da cap nhat file nay

Chi bat loi may kiem tra duoc: dau gach, emoji, tu cam, link, do dai SEO, dinh dang so,
doi chieu so lieu voi file CSV san pham, ma tieu chuan voi tieu_chuan_da_kiem.csv,
heading voi outline da chot va doan trung voi bai top SERP (tools/nghien_cuu.py). Chat luong noi dung do agent danh-gia-noi-dung danh gia.
Ma thoat: 0 = khong co LOI, 1 = co LOI can sua, 2 = file sai cau truc.
"""
import argparse
import csv
import datetime
import glob
import hashlib
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nghien_cuu  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUY_TAC = os.path.join(ROOT, "quy_tac_cham.md")
NGUON_QUY_TAC = ("1_Project_Instructions_Auto_Blog_HLB.md", "2_Knowledge_Du_lieu_tham_chieu_HLB.md")
DA_KIEM = os.path.join(ROOT, ".danh_gia", "_da_kiem.json")
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
    r"hlb\s+(tự\s+)?(sản xuất|lắp ráp)": "HLB phân phối đèn LED nhiều thương hiệu, không viết \"HLB sản xuất\"",
    r"(hlb|chúng tôi)\s+là\s+(nhà|đơn vị|công ty|hãng)\s+sản xuất": "HLB là đơn vị phân phối, không phải nhà sản xuất",
    r"(do|của)\s+(hlb|chúng tôi)\s+(tự\s+)?(sản xuất|lắp ráp)": "HLB là đơn vị phân phối, không sản xuất, không lắp ráp",
    r"(xưởng|nhà máy)\s+(sản xuất\s+)?(của|thuộc)\s+(hlb|chúng tôi)": "HLB là đơn vị phân phối, không có xưởng, nhà máy",
    r"nhà máy của (chúng tôi|hlb)": "HLB là đơn vị phân phối, không có nhà máy",
    r"chúng tôi (tự\s+)?(sản xuất|lắp ráp)": "HLB là đơn vị phân phối, không sản xuất, không lắp ráp",
    r"hlb.{0,40}(từ|năm|thành lập|ra đời)\s*(năm\s*)?2011": "mốc 2011 là của HALEDCO, HLB phân phối từ 2018",
    r"\d+\s+năm kinh nghiệm": "không tự tính số năm kinh nghiệm, ghi năm bắt đầu",
    r"haledco\.com": "không nhắc hoặc link haledco.com",
}

# HALEDCO la don vi san xuat va phan phoi (nhac lai 26/10/2026): "den do HALEDCO san xuat" la dung.
# Chi canh bao khi gan hang san xuat cho dong cao cap (chua xac nhan).
BRAND_ROLE_WARN = {
    r"cao cấp[^.;:]{0,40}\b(của|do)?\s*haledco\s+(sản xuất|lắp ráp)|cao cấp[^.;:]{0,20}\b(của|do)\s+haledco\b":
        "dòng cao cấp gọi là \"dòng đèn cao cấp HLB phân phối\", dòng này gồm đèn của nhiều thương hiệu, không gán cho riêng một hãng sản xuất (người dùng chốt 26/10/2026)",
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
        for pat, why in BRAND_ROLE_WARN.items():
            if re.search(pat, norm(line)):
                rep.warn(no, "Kiểm tra vai trò thương hiệu: %s" % why)
        for bad, good in TERMS.items():
            if bad in text:
                rep.warn(no, "Thuật ngữ \"%s\" nên thống nhất thành \"%s\"" % (bad, good))
        # Thoi han bao hanh da xac nhan: 2 nam (24 thang). Philips theo tung model tren signify.com (Knowledge muc 1)
        for m in re.finditer(r"(bảo hành|bh)\D{0,20}?(\d+)\s*(năm|tháng)", text):
            months = int(m.group(2)) * (12 if m.group(3) == "năm" else 1)
            if months != 24:
                msg = "Thời hạn bảo hành \"%s\" khác 2 năm đã xác nhận (Knowledge mục 1)" % m.group(0)
                if "philips" in text:
                    rep.warn(no, msg + ", Philips thì kiểm tra theo model trên signify.com")
                else:
                    rep.error(no, msg)
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

    for url in sorted(set(external)):
        host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0].lower()
        if not re.search(r"\.(gov|gov\.vn|edu|edu\.vn|int|org)$|(^|\.)(iec\.ch|iso\.org|tcvn\.gov\.vn|cie\.co\.at)$", host):
            rep.warn(None, "Link ngoài %s không phải nguồn có thẩm quyền (cơ quan nhà nước, tổ chức tiêu chuẩn, hiệp hội), "
                           "kiểm tra lại hoặc bỏ (Knowledge 9.3)" % host)
    if MANG:
        check_urls_live(rep, sorted(set(internal) | set(external)))

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


MANG = True  # tat bang --khong-mang


def check_urls_live(rep, urls):
    """Mo tung link: 404/410 la LOI (link doan, bai da xoa), chuyen huong sang trang khac la CANH BAO."""
    import urllib.error
    import urllib.request
    loi_mang = []
    for url in urls:
        req = urllib.request.Request(url, headers={"User-Agent": "HLB-kiem-tra/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                final = r.geturl()
            if final.rstrip("/") != url.rstrip("/"):
                rep.warn(None, "Link %s chuyển hướng sang %s, dùng URL đích" % (url, final))
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                rep.error(None, "Link không tồn tại (HTTP %d): %s. Không tự ghép URL, dùng URL đã mở được "
                                "hoặc [LINK: tên trang]" % (e.code, url))
            else:
                loi_mang.append("%s (HTTP %d)" % (url, e.code))
        except (urllib.error.URLError, OSError) as e:
            loi_mang.append(url)
    if loi_mang:
        rep.info(None, "Chưa mở được để kiểm tra link: " + ", ".join(loi_mang))


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
    if re.fullmatch(r"đèn led nhà xưởng( [a-zà-ỹđ ]+)? \d+\s?w", kwn):
        rep.warn(kw_no, "Từ khóa chính \"%s\" trùng kiểu từ khóa của trang danh mục công suất, bài blog dễ cạnh tranh "
                        "với trang danh mục (Knowledge 9.1). Chỉ viết khi intent khác rõ (giá, cách chọn, so sánh)" % kw)

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


def check_faq(rep, body):
    """FAQ 3-5 cau (Knowledge 9.6): dem H3 duoi H2 co "câu hỏi thường gặp" hoac "FAQ"."""
    start, n = None, 0
    for no, line in body:
        if re.match(r"^## ", line):
            if start is not None:
                break
            if re.search(r"câu hỏi thường gặp|\bfaq\b", line.lower()):
                start = no
        elif start is not None and re.match(r"^### ", line):
            n += 1
    if start is None:
        rep.info(None, "Không thấy mục FAQ (H2 \"Câu hỏi thường gặp\"), kiểm tra outline đã chốt có FAQ không")
    elif not 3 <= n <= 5:
        rep.warn(start, "FAQ có %d câu, nên 3-5 câu (ít hơn chỉ khi không đủ câu có giá trị)" % n)


def check_quick_answer(rep, body):
    """Doan tra loi nhanh 40-60 tu (Knowledge 8.1): khoi cuoi truoc H2 dau tien (gop voi mo bai neu chi co 1 khoi)."""
    blocks, cur = [], []
    for no, line in body:
        s = line.strip()
        if re.match(r"^## ", s):
            break
        if re.match(r"^# ", s) or not s or IMAGE.fullmatch(s) or PLACEHOLDER.fullmatch(s):
            if cur:
                blocks.append(cur)
            cur = []
            continue
        cur.append((no, s))
    if cur:
        blocks.append(cur)
    if not blocks:
        rep.warn(None, "Không thấy mở bài và đoạn trả lời nhanh trước H2 đầu tiên")
        return
    qa = blocks[-1]
    n = len(norm(strip_markup(" ".join(s for _, s in qa))).split())
    gop = " (gộp với mở bài)" if len(blocks) == 1 else ""
    if not 40 <= n <= 60:
        rep.warn(qa[0][0], "Đoạn trả lời nhanh%s có %d từ, cần 40-60 (Knowledge 8.1)" % (gop, n))
    else:
        rep.info(qa[0][0], "Đoạn trả lời nhanh%s %d từ" % (gop, n))


def check_price_note(rep, body):
    """Gia phai ghi "giá tham khảo" kem thoi diem (Instructions muc 6)."""
    price_lines = [no for no, line in body if re.search(r"\d{1,3}(?:\.\d{3})+\s*(đồng|đ\b|vnđ)", line, re.I)]
    text = norm(" ".join(l for _, l in body))
    if price_lines and "tham khảo" not in text:
        rep.warn(price_lines[0], "Bài có giá nhưng không ghi \"giá tham khảo tại thời điểm [ngày]\"")


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
    elif any(k in counts for k in ("CẦN BỔ SUNG", "CẦN KIỂM TRA", "CHỜ XÁC NHẬN", "LINK")):
        text = " ".join(l for _, l in notes)
        for kind in ("CẦN BỔ SUNG", "CẦN KIỂM TRA", "CHỜ XÁC NHẬN", "LINK"):
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


PRICE = re.compile(r"(\d{1,3}(?:\.\d{3})+)\s*(đồng|đ\b|vnđ)(\s*/\s*(m²|m2|m³|m\b|kwh|tháng|năm|giờ))?", re.I)
# Chung nhan hay bi bia: chi duoc neu khi co trong cot cert/ip cua CSV (Instructions muc 2, quy tac 1)
CERTS = ["UL", "cUL", "DLC", "ENEC", "TÜV", "TUV", "SASO", "ETL", "CB", "GS", "SAA", "PSE", "KC", "BIS",
         "ISO", "CE", "RoHS", "FCC", "ERP", "LM-80", "TM-21"]
# Ma tieu chuan da kiem tra nguon (Knowledge muc 6). Ma khac phai ghi nguon o phan C hoac dat trong [CAN KIEM TRA]
STANDARD = re.compile(r"\b(TCVN|QCVN|IEC|EN|ISO|CIE)\s?\d[\d.\-]*(?:-\d+)?(?::\d{4})?")
TIEU_CHUAN = os.path.join(ROOT, "tieu_chuan_da_kiem.csv")


def load_tieu_chuan():
    """Danh sach tieu chuan da tra nguon chinh thuc (tieu_chuan_da_kiem.csv): ma (bo hau to /BYT, /BXD) -> dong."""
    try:
        rows = list(csv.DictReader(open(TIEU_CHUAN, encoding="utf-8-sig")))
    except OSError:
        return {}
    return {re.sub(r"/\w+$", "", r["ma"].strip()): r for r in rows if r.get("ma")}


def check_standard(rep, no, code, verified, notes_text):
    base = code.split(":")[0]
    row = verified.get(code)
    if row:
        if row.get("tinh_trang", "").startswith("đã thay thế"):
            rep.warn(no, "%s đã bị thay thế bởi %s (tieu_chuan_da_kiem.csv), dùng bản mới" % (code, row.get("thay_the_boi")))
        return
    cung_so = [k for k in verified if k.split(":")[0] == base]
    if cung_so and ":" not in code:
        return  # viet ma khong kem nam, vi du "IEC 60529"
    if cung_so:
        rep.warn(no, "%s: năm ban hành khác danh sách đã kiểm tra (%s)" % (code, ", ".join(cung_so)))
        return
    if code not in notes_text and base not in notes_text:
        rep.warn(no, "Mã tiêu chuẩn %s chưa có trong tieu_chuan_da_kiem.csv và phần C không ghi nguồn. "
                     "Tra nguồn chính thức rồi thêm vào danh sách, hoặc để [CẦN KIỂM TRA]" % code)


def nums(pattern, text):
    return [to_int(x) for x in re.findall(pattern, text)]


def check_against_csv(rep, body, models, csv_name, notes_text=""):
    prices = {to_int(r["price"]) for r in models.values() if r["price"].strip("0 ")}
    verified = load_tieu_chuan()
    certs_csv = set()
    for r in models.values():
        for tok in re.split(r"[,.;\s]+", "%s %s" % (r.get("cert", ""), r.get("ip", ""))):
            if tok:
                certs_csv.add(tok.lower())
    for no, line in body:
        text = PLACEHOLDER.sub(" ", line)
        if re.match(r"^#{1,4} ", line):
            heading = True
        else:
            heading = False
        line_prices = []
        for m in PRICE.finditer(text):
            if m.group(3):
                continue  # don gia xay dung, gia dien... khong phai gia den
            line_prices.append(to_int(m.group(1)))
            if to_int(m.group(1)) not in prices:
                rep.warn(no, "Giá %s không khớp sản phẩm nào trong %s" % (m.group(0), csv_name))

        # Chung nhan khong co trong du lieu san pham
        for c in CERTS:
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(c), text) and c.lower() not in certs_csv:
                ma = [models.get(x) for x in MODEL.findall(text) if models.get(x)]
                if re.search(r"philips|rạng đông|điện quang|signify", text, re.I) and \
                        not any(re.search(r"cao cấp|haledco", r.get("brand", ""), re.I) for r in ma):
                    rep.warn(no, "Chứng nhận \"%s\" của hãng khác: chỉ giữ khi hãng công bố, ghi nguồn ở phần C" % c)
                    continue
                rep.error(no, "Chứng nhận \"%s\" không có trong %s. Chỉ nêu chứng nhận trang sản phẩm công bố, "
                              "chưa có nguồn thì để [CẦN KIỂM TRA]" % (c, csv_name))
        # Ma tieu chuan chua co nguon
        for m in STANDARD.finditer(text):
            check_standard(rep, no, re.sub(r"\s+", " ", m.group(0)), verified, notes_text)
        # Ten du an, khach hang (Knowledge muc 1: chi dung khi nguoi dung cung cap)
        if re.search(r"(dự án|công trình|nhà máy|khách hàng|tập đoàn|công ty)\s+(của\s+)?[A-ZĐ][\wÀ-ỹ]*\s+[A-ZĐ]", text) \
                or re.search(r"\bđã (lắp|cung cấp|thi công|lắp đặt)( đặt)? (cho|tại)\b", text, re.I):
            rep.warn(no, "Nêu dự án, khách hàng cụ thể: chỉ dùng khi người dùng đã cung cấp (Knowledge mục 1)")

        codes = sorted(set(MODEL.findall(text)))
        if not codes:
            continue
        known = {}
        for code in codes:
            if code in models:
                known[code] = models[code]
            else:
                rep.warn(no, "Model %s không có trong %s, kiểm tra lại tên model" % (code, csv_name))
        if not known:
            continue
        names = ", ".join(known)
        # Hang khac (Philips, Rang Dong, Dien Quang): thong so duoc lay theo hang cong bo, gia ghi khoang gia thi truong
        # (nguoi dung chot 26/10/2026), nen lech CSV chi canh bao, nguon ghi o phan C
        hang_khac = all(not re.search(r"cao cấp|haledco", r.get("brand", ""), re.I) for r in known.values())
        # Mot dong co the co nhieu gia tri va nhieu model: bao loi khi khong gia tri nao khop model nao trong dong
        def cmp(label, found, values, error=True, fmt=str):
            values = {v for v in values if v not in (None, "")}
            if found and values and not set(found) & values:
                msg = "%s: %s trong bài %s, CSV ghi %s" % (names, label, ", ".join(fmt(x) for x in found),
                                                           ", ".join(sorted(fmt(v) for v in values)))
                if hang_khac and error:
                    rep.warn(no, msg + ". Hãng khác: dùng được số hãng công bố hoặc khoảng giá thị trường, ghi nguồn ở phần C")
                else:
                    (rep.error if error else rep.warn)(no, msg)

        cmp("quang thông (lm)", nums(r"(\d{1,3}(?:\.\d{3})+|\d{4,})\s*lm\b", text),
            {to_int(r["lm"]) for r in known.values() if r["lm"]})
        cmp("PF", [x.replace(",", ".") for x in re.findall(r"PF\D{0,10}(\d[,.]\d+)", text)],
            {r["pf"] for r in known.values()})
        cmp("Ra", re.findall(r"\bRa\D{0,10}(\d{2})\b", text), {r["ra"] for r in known.values()})
        cmp("cấp bảo vệ", re.findall(r"\bIP\s?(\d{2})\b", text),
            {x for r in known.values() for x in re.findall(r"IP(\d{2})", r["ip"])}, fmt=lambda x: "IP" + x)
        if line_prices:
            listed = {to_int(r["price"]) for r in known.values() if r["price"].strip("0 ")}
            if not listed and not hang_khac:
                rep.error(no, "%s: trang sản phẩm ghi giá Liên hệ (CSV giá 0), bài không được nêu giá" % names)
            elif not listed:
                rep.warn(no, "%s: website ghi giá Liên hệ, giá trong bài phải là khoảng giá thị trường có nguồn ở phần C" % names)
            else:
                cmp("giá (đồng)", line_prices, listed, fmt=lambda x: "{:,}".format(x).replace(",", "."))
        # Cong suat, tuoi tho: dong co the nhac den den cu (cao ap 250W, 10.000 gio) nen chi canh bao
        no_codes = MODEL.sub(" ", text)
        cmp("công suất (W)", [int(x) for x in re.findall(r"(?<![\d.,/])(\d{2,3})\s?W\b(?!/)", no_codes)],
            {to_int(r["w"]) for r in known.values() if r["w"].strip()}, error=False)
        cmp("tuổi thọ (giờ)", [x for x in nums(r"(\d{1,3}(?:\.\d{3})+|\d{5,})\s*giờ", text) if x >= 10000],
            {to_int(r["life"]) for r in known.values() if r["life"].strip()}, error=False)
        eff = [float(x.replace(",", ".")) for x in re.findall(r"(\d{2,3}(?:,\d+)?)\s*lm/W", text)]
        calc = [to_int(r["lm"]) / to_int(r["w"]) for r in known.values() if r["lm"] and r["w"].strip()]
        if eff and calc and not any(abs(e - c) <= 1 for e in eff for c in calc):
            rep.warn(no, "%s: hiệu suất trong bài %s lm/W, tính từ CSV %s lm/W" % (
                names, ", ".join("%g" % e for e in eff), ", ".join("%.0f" % c for c in calc)))


def check_outline(rep, article, body):
    """Heading bai phai dung outline da chot (Instructions buoc 3), luu o nghien_cuu/<bai>/outline.md."""
    outline = nghien_cuu.doc_outline(article)
    if outline is None:
        rep.info(None, "Chưa lưu outline đã chốt (tools/nghien_cuu.py luu-outline), chưa so heading với outline")
        return
    heads = [(no, len(m.group(1)), m.group(2)) for no, l in body for m in [re.match(r"^(#{1,4}) (.+?)\s*$", l)] if m]
    for level, j, msg in nghien_cuu.so_outline([(l, t) for _, l, t in heads], outline):
        rep.add(level, heads[j][0] if j is not None else None, msg)


def check_chep_bai(rep, article, body):
    """Doan trung dai voi bai top SERP da luu (nghien_cuu/<bai>/serp/)."""
    nguon = nghien_cuu.doc_serp(article)
    if not nguon:
        rep.info(None, "Chưa lưu văn bản bài top SERP (tools/nghien_cuu.py luu-serp), chưa kiểm tra chép bài")
        return
    lines = [(no, strip_markup(l)) for no, l in body if not IMAGE.search(l)]
    for no, n, doan, url in nghien_cuu.doan_trung(lines, nguon):
        msg = "%d từ liền nhau trùng bài %s: \"%s\". Viết lại bằng ý và lời của mình" % (n, url, short(doan, 90))
        (rep.error if n >= nghien_cuu.N_LOI else rep.warn)(no, msg)
    rep.info(None, "Đã so với %d bài top SERP" % len(nguon))


# ---------- File quy tac cham rut gon ----------

def ma_nguon():
    out = []
    for name in NGUON_QUY_TAC:
        with open(os.path.join(ROOT, name), "rb") as f:
            out.append("%s %s" % (name, hashlib.sha256(f.read()).hexdigest()[:12]))
    return out


def check_quy_tac(rep):
    """quy_tac_cham.md phai duoc lam tu dung ban Instructions, Knowledge hien tai (dong 'Ma nguon:')."""
    if not os.path.isfile(QUY_TAC):
        return
    with open(QUY_TAC, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^Mã nguồn: (.*)$", text, re.M)
    if not m or m.group(1).strip() != "; ".join(ma_nguon()):
        rep.warn(None, "quy_tac_cham.md làm từ bản Instructions/Knowledge cũ. Agent đánh giá đọc file gốc cho lần chấm này; "
                       "cập nhật quy_tac_cham.md rồi chạy --cap-nhat-quy-tac")


def cap_nhat_quy_tac():
    with open(QUY_TAC, encoding="utf-8") as f:
        text = f.read()
    line = "Mã nguồn: " + "; ".join(ma_nguon())
    text, n = re.subn(r"^Mã nguồn: .*$", line, text, flags=re.M)
    if not n:
        sys.exit("quy_tac_cham.md thiếu dòng 'Mã nguồn: ...'")
    with open(QUY_TAC, "w", encoding="utf-8") as f:
        f.write(text)
    print("Đã ghi: " + line)


def tim_csv(base):
    # sap theo ngay trong ten file (dd-mm-yyyy), sap theo chu thi 01-11 dung truoc 21-10
    found = sorted(glob.glob(os.path.join(base, "du_lieu_san_pham_*.csv")), key=lambda f: re.findall(r"(\d{2})-(\d{2})-(\d{4})", f)[-1][::-1] if re.findall(r"(\d{2})-(\d{2})-(\d{4})", f) else ())
    return found[-1] if found else None


def tra(value, csv_path):
    """Tim trong CSV theo ma model (mot phan ten) hoac so (quang thong, gia, cong suat). In cac dong khop va so dong."""
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    q = value.strip()
    digits = re.sub(r"[.,\s]", "", q)
    hits = []
    for r in rows:
        if digits.isdigit():
            vals = [re.sub(r"[.,\s]", "", r.get(k) or "") for k in ("lm", "price", "regular_price")]
            if digits in vals or re.fullmatch(digits + r"W?", re.sub(r"\s", "", r.get("w") or "")):
                hits.append(r)
        elif q.lower() in r["name"].lower():
            hits.append(r)
    keys = [k for k in ("name", "w", "lm", "pf", "ra", "price") if k in (rows[0] if rows else {})]
    print("Tra \"%s\" trong %s: %d dòng khớp" % (q, os.path.basename(csv_path), len(hits)))
    for r in hits:
        print("- " + " | ".join("%s=%s" % (k, r.get(k, "")) for k in keys))


def ghi_da_kiem(article, n_err):
    """Ghi lai lan chay tren noi dung nay, de phieu_duyet.py ghi biet da kiem tra co hoc dung ban dang cham."""
    try:
        with open(DA_KIEM, encoding="utf-8") as f:
            state = json.load(f)
    except (OSError, ValueError):
        state = {}
    with open(article, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    state[os.path.basename(article)] = {"sha256": sha, "loi": n_err,
                                        "luc": datetime.datetime.now().isoformat(timespec="seconds")}
    os.makedirs(os.path.dirname(DA_KIEM), exist_ok=True)
    with open(DA_KIEM, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)


# ---------- Chay ----------

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("article", nargs="?")
    ap.add_argument("--csv", help="file CSV san pham (mac dinh: file du_lieu_san_pham_*.csv moi nhat)")
    ap.add_argument("--gon", action="store_true", help="chi in LOI, CANH BAO va dong tom tat")
    ap.add_argument("--tra", help="tra CSV theo ma model hoac so")
    ap.add_argument("--cap-nhat-quy-tac", action="store_true")
    ap.add_argument("--khong-mang", action="store_true", help="khong mo link de kiem tra (khi khong co mang)")
    args = ap.parse_args()
    if args.cap_nhat_quy_tac:
        return cap_nhat_quy_tac()
    if args.tra:
        csv_path = args.csv or tim_csv(ROOT)
        if not csv_path:
            sys.exit("Không thấy file CSV sản phẩm")
        return tra(args.tra, csv_path)
    if not args.article:
        ap.error("cần file bài")
    global MANG
    MANG = not args.khong_mang

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
    check_faq(rep, b)
    check_quick_answer(rep, b)
    check_price_note(rep, b)
    check_placeholders(rep, b, c)
    check_outline(rep, args.article, b)
    check_chep_bai(rep, args.article, b)
    check_quy_tac(rep)

    csv_path = args.csv or tim_csv(os.path.dirname(os.path.abspath(args.article)))
    if csv_path:
        check_against_csv(rep, b, load_csv(csv_path), os.path.basename(csv_path), " ".join(l for _, l in c))
    else:
        rep.info(None, "Không tìm thấy file CSV sản phẩm, bỏ qua đối chiếu thông số và giá")

    n_err, n_warn = len(rep.items["LỖI"]), len(rep.items["CẢNH BÁO"])
    ghi_da_kiem(args.article, n_err)
    print("KIỂM TRA CƠ HỌC: %s" % args.article)
    for level, items in rep.items.items():
        if args.gon and level == "THÔNG TIN":
            print("\n" + "Thông tin: " + "; ".join(m for _, m in items))
            continue
        if args.gon and not items:
            continue
        print("\n## %s (%d)" % (level, len(items)))
        for line, msg in sorted(items, key=lambda x: x[0] or 0):
            print("- %s%s" % ("[dòng %d] " % line if line else "", msg))
    print("\nTổng: %d lỗi, %d cảnh báo. %s" % (
        n_err, n_warn, "Sửa hết LỖI trước khi đăng bản nháp." if n_err else "Không có lỗi cơ học."))
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
