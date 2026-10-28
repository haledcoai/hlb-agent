"""Luu outline da chot va van ban bai top SERP canh bai viet, de kiem_tra_bai.py so heading va tim doan chep.

Cach dung:
  python tools/nghien_cuu.py luu-outline Bai_<slug>.md --tu <file>        # file .md/.txt chua outline, hoac file JSON
                                                                           # cua bang dieu phoi (lay truong "outline")
  python tools/nghien_cuu.py luu-outline Bai_<slug>.md --tu <file> --ly-do "nguoi dung doi H2 thu 3 ngay 27/10"
  python tools/nghien_cuu.py serp Bai_<slug>.md "<tu khoa>" [--luu]       # top 10 Google VN qua SerpApi (bien SERPAPI_KEY),
                                                                           # --luu tai luon van ban cac bai top
  python tools/nghien_cuu.py luu-serp Bai_<slug>.md <url> [<url> ...]     # tai va luu van ban bai top (may co mang)
  python tools/nghien_cuu.py luu-serp Bai_<slug>.md <url> --tu-file <file> # luu van ban da lay bang WebFetch
  python tools/nghien_cuu.py xem Bai_<slug>.md

Thu muc: nghien_cuu/<ten bai>/outline.md va nghien_cuu/<ten bai>/serp/NN-<ten mien>.txt.
Outline doc cac dong "H2: ..." (dang bullet cua bang dieu phoi) hoac "## ..." (markdown).
"""
import argparse
import datetime
import difflib
import glob
import html
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THU_MUC = os.path.join(ROOT, "nghien_cuu")
HEADING_OUTLINE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)?\**H([1-4])\**\s*[:.)-]\s*(.+?)\s*$")
HEADING_MD = re.compile(r"^(#{1,4})\s+(.+?)\s*$")
FAQ = re.compile(r"câu hỏi thường gặp|hỏi đáp|\bfaq\b", re.I)
# Doan trung voi bai top: tu 10 tu lien tiep la canh bao, tu 25 tu (gan mot doan van) la LOI
N_CANH_BAO = 10
N_LOI = 25


def ten_bai(article):
    return os.path.splitext(os.path.basename(article))[0]


def thu_muc_bai(article):
    return os.path.join(THU_MUC, ten_bai(article))


def chuan(text):
    text = unicodedata.normalize("NFC", text).lower()
    text = re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# ---------- Outline ----------

# ghi chu "(63 ky tu)" canh heading trong outline, khong phai chu cua heading
SO_KY_TU = re.compile(r"\s*\(\d+ ký tự\)\s*$")


def heading_outline(text):
    """Danh sach (cap, chu) tu outline. Uu tien dang 'H2: ...'; khong co thi doc heading markdown."""
    out = [(int(m.group(1)), SO_KY_TU.sub("", m.group(2)).strip("* ")) for m in map(HEADING_OUTLINE.match, text.splitlines()) if m]
    if not out:
        out = [(len(m.group(1)), m.group(2).strip()) for m in map(HEADING_MD.match, text.splitlines()) if m]
    return out


def doc_outline(article):
    path = os.path.join(thu_muc_bai(article), "outline.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return heading_outline(f.read())


def vung_faq(heads):
    """Danh dau heading nam duoi H2 cau hoi thuong gap."""
    out, trong = [], False
    for level, text in heads:
        if level <= 2:
            trong = bool(FAQ.search(text))
            out.append(False)
        else:
            out.append(trong)
    return out


def so_outline(bai, outline):
    """So heading bai voi outline. Tra ve danh sach (muc, chi_so_trong_bai hoac None, thong_bao).
    muc 'LỖI' khi them, bot, doi thu tu, doi cap, doi chu han; 'CẢNH BÁO' khi chi khac vai chu, hoac lech o phan FAQ."""
    ka = ["%d|%s" % (l, chuan(t)) for l, t in outline]
    kb = ["%d|%s" % (l, chuan(t)) for l, t in bai]
    faq_a, faq_b = vung_faq(outline), vung_faq(bai)
    out = []

    def muc(loi, la_faq):
        return "CẢNH BÁO" if la_faq or not loi else "LỖI"

    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        cap = list(zip(range(a1, a2), range(b1, b2))) if op == "replace" else []
        for i, j in cap:
            (la, ta), (lb, tb) = outline[i], bai[j]
            ty_le = difflib.SequenceMatcher(None, chuan(ta), chuan(tb)).ratio()
            if la != lb:
                out.append((muc(True, faq_a[i] and faq_b[j]), j, "Đổi cấp heading: outline H%d \"%s\", bài H%d" % (la, ta, lb)))
            elif ty_le >= 0.85:
                out.append(("CẢNH BÁO", j, "Heading khác vài chữ so với outline: \"%s\" (outline: \"%s\")" % (tb, ta)))
            else:
                out.append((muc(True, faq_a[i] and faq_b[j]), j, "Heading khác outline: \"%s\" (outline H%d: \"%s\")" % (tb, la, ta)))
        for i in range(a1 + len(cap), a2):
            la, ta = outline[i]
            out.append((muc(True, faq_a[i]), None, "Thiếu heading của outline: H%d \"%s\" (hoặc đã đổi thứ tự)" % (la, ta)))
        for j in range(b1 + len(cap), b2):
            lb, tb = bai[j]
            out.append((muc(True, faq_b[j]), j, "Heading không có trong outline: H%d \"%s\" (hoặc đã đổi thứ tự)" % (lb, tb)))
    return out


def doc_nguon_vao(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.lower().endswith(".json"):
        data = json.loads(text)
        data = data.get("data", data)
        if not isinstance(data.get("outline"), str):
            sys.exit("File JSON không có trường outline")
        return data["outline"]
    return text


def luu_outline(args):
    text = doc_nguon_vao(args.tu)
    heads = heading_outline(text)
    if not heads:
        sys.exit("Không thấy heading nào (dạng \"H2: ...\" hoặc \"## ...\") trong %s" % args.tu)
    folder = thu_muc_bai(args.bai)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "outline.md")
    cu = doc_outline(args.bai)
    dau = "<!-- Lưu %s%s. Sửa outline đã chốt thì lưu lại bằng tools/nghien_cuu.py luu-outline --ly-do -->\n\n" % (
        datetime.datetime.now().isoformat(timespec="minutes"), "; lý do: " + args.ly_do if args.ly_do else "")
    if cu and not args.ly_do and cu != heads:
        sys.exit("Đã có outline khác cho bài này. Lưu đè phải có --ly-do (ví dụ người dùng duyệt đổi heading ngày nào)")
    with open(path, "w", encoding="utf-8") as f:
        # bo dong ghi lan luu cu khi luu lai tu chinh file outline.md
        f.write(dau + re.sub(r"\A\s*<!-- Lưu .*?-->\s*", "", text.strip()) + "\n")
    for level, text in heads:
        if level == 1 and not 55 <= len(text) <= 65:
            print("CẢNH BÁO: H1 dài %d ký tự, cần 55-65 (người dùng chốt 28/10/2026): %s" % (len(text), text))
    print("Đã lưu %s: %d heading (%s)" % (os.path.relpath(path, ROOT), len(heads),
                                          ", ".join("H%d %d" % (l, sum(1 for x, _ in heads if x == l)) for l in (1, 2, 3, 4)
                                                    if any(x == l for x, _ in heads))))


# ---------- Van ban bai top SERP ----------

def trich_van_ban(page):
    page = re.sub(r"(?is)<(script|style|noscript|svg|nav|header|footer|aside|form)\b.*?</\1>", " ", page)
    for pat in (r"(?is)<article\b.*?</article>", r"(?is)<main\b.*?</main>",
                r"(?is)<div[^>]+class=\"[^\"]*(entry-content|post-content|article-content|content-detail)[^\"]*\".*"):
        m = re.search(pat, page)
        if m:
            page = m.group(0)
            break
    page = re.sub(r"(?i)<br\s*/?>|</(p|h\d|li|tr|div)>", "\n", page)
    text = html.unescape(re.sub(r"<[^>]+>", " ", page))
    lines = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in text.splitlines()]
    return "\n".join(l for l in lines if len(l) > 1)


def tai(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (HLB-nghien-cuu)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


def luu_serp(args):
    folder = os.path.join(thu_muc_bai(args.bai), "serp")
    os.makedirs(folder, exist_ok=True)
    if args.tu_file and len(args.url) != 1:
        sys.exit("--tu-file đi với đúng 1 URL")
    loi = 0
    for url in args.url:
        host = urllib.parse.urlparse(url).netloc.replace("www.", "") or "nguon"
        da_co = [p for p in glob.glob(os.path.join(folder, "*.txt")) if open(p, encoding="utf-8").readline().strip() == "URL: " + url]
        path = da_co[0] if da_co else os.path.join(folder, "%02d-%s.txt" % (len(glob.glob(os.path.join(folder, "*.txt"))) + 1, host))
        try:
            if args.tu_file:
                with open(args.tu_file, encoding="utf-8") as f:
                    text = f.read()
            else:
                text = trich_van_ban(tai(url))
        except (OSError, ValueError) as e:
            loi += 1
            print("- Không tải được %s (%s). Lấy văn bản bằng WebFetch rồi chạy lại với --tu-file" % (url, e))
            continue
        so_tu = len(chuan(text).split())
        if so_tu < 150:
            print("- %s: chỉ có %d từ, có thể trang chặn hoặc lấy sai phần thân bài" % (url, so_tu))
        with open(path, "w", encoding="utf-8") as f:
            f.write("URL: %s\nLưu: %s\n\n%s\n" % (url, datetime.date.today().isoformat(), text.strip()))
        print("- Đã lưu %s (%d từ)" % (os.path.relpath(path, ROOT), so_tu))
    if loi:
        sys.exit(1)


# Trang danh muc, san pham, san TMDT: khong phai bai blog, khong luu van ban (Instructions buoc 1)
KHONG_PHAI_BAI = re.compile(r"/(products?|san-pham|danh-muc[^/]*|product-category|categor(y|ies)|collections?|shop|cua-hang)(/|$)|"
                            r"-c\d+(\.html?)?/?$|shopee\.|lazada\.|tiki\.|youtube\.|facebook\.", re.I)
# Duong dan kieu bai viet. Con lai la "chua ro": mo trang de xac nhan truoc khi ket luan dinh dang
LA_BAI = re.compile(r"/(tin-tuc|blog|tu-van|kien-thuc|bai-viet|news|huong-dan|cam-nang)/", re.I)


def khong_dau(text):
    text = unicodedata.normalize("NFD", chuan(text).replace("đ", "d"))
    return re.sub(r"[^a-z0-9]+", "-", "".join(c for c in text if not unicodedata.combining(c))).strip("-")


def serp(args):
    """Top 10 Google Viet Nam qua SerpApi: in vi tri, tieu de, link, doan trich, cau hoi 'Moi nguoi cung hoi', luu JSON."""
    key = os.environ.get("SERPAPI_KEY")
    if not key:
        sys.exit("Chưa có biến SERPAPI_KEY. Người dùng thêm key vào cloud environment (không dán vào chat)")
    q = urllib.parse.urlencode({"engine": "google", "q": args.tu_khoa, "google_domain": "google.com.vn", "gl": "vn",
                                "hl": "vi", "num": 10, "api_key": key})
    try:
        data = json.loads(tai("https://serpapi.com/search.json?" + q))
    except (OSError, ValueError) as e:
        sys.exit("Không gọi được SerpApi (%s). Kiểm tra serpapi.com trong Allowed domains" % e)
    if data.get("error"):
        sys.exit("SerpApi báo lỗi: %s" % data["error"])
    folder = os.path.join(thu_muc_bai(args.bai), "serp")
    os.makedirs(folder, exist_ok=True)
    kq = {"tu_khoa": args.tu_khoa, "luc": datetime.datetime.now().isoformat(timespec="minutes"),
          "top": [{k: r.get(k) for k in ("position", "title", "link", "snippet")} for r in data.get("organic_results", [])[:10]],
          "hoi": [r.get("question") for r in data.get("related_questions", [])],
          "lien_quan": [r.get("query") for r in data.get("related_searches", [])]}
    print("Top Google VN cho \"%s\" (%s):" % (args.tu_khoa, kq["luc"]))
    bai = []
    for r in kq["top"]:
        link = r["link"] or ""
        r["loai"] = "danh mục/SP" if KHONG_PHAI_BAI.search(link) else "bài" if LA_BAI.search(link) else "chưa rõ"
        if r["loai"] != "danh mục/SP":
            bai.append(link)
        print("%2s. [%s] %s\n    %s\n    %s" % (r["position"], r["loai"], r["title"], link, (r["snippet"] or "")[:200]))
    with open(os.path.join(folder, "_ket_qua_%s.json" % khong_dau(args.tu_khoa)), "w", encoding="utf-8") as f:
        json.dump(kq, f, ensure_ascii=False, indent=1)
    if kq["hoi"]:
        print("\nMọi người cũng hỏi (gợi ý FAQ):\n" + "\n".join("- " + x for x in kq["hoi"] if x))
    if kq["lien_quan"]:
        print("\nTìm kiếm liên quan (gợi ý từ khóa phụ):\n" + "\n".join("- " + x for x in kq["lien_quan"] if x))
    dem = {k: sum(1 for r in kq["top"] if r["loai"] == k) for k in ("bài", "danh mục/SP", "chưa rõ")}
    print("\nPhân loại theo đường dẫn, chỉ là gợi ý: %d bài, %d danh mục/sản phẩm, %d chưa rõ. Mở trang \"chưa rõ\" "
          "để xác định trước khi kết luận định dạng nội dung (Instructions bước 1)." % (dem["bài"], dem["danh mục/SP"], dem["chưa rõ"]))
    if args.luu and bai:
        print("\nLưu văn bản bài top:")
        args.url, args.tu_file = bai, None
        try:
            luu_serp(args)
        except SystemExit:
            pass  # trang khong tai duoc da in huong dan WebFetch


def doc_serp(article):
    """Danh sach (url, van ban) cac bai top da luu."""
    out = []
    for path in sorted(glob.glob(os.path.join(thu_muc_bai(article), "serp", "*.txt"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        dau, _, than = text.partition("\n\n")
        if not dau.startswith("URL: "):
            out.append((os.path.basename(path), text))
        else:
            out.append((dau.splitlines()[0][5:], than))
    return out


def doan_trung(dong_bai, nguon):
    """dong_bai: [(so dong, van ban)]. Tra ve [(so dong, so tu, doan, url)] cho cac doan tu N_CANH_BAO tu trung bai top."""
    tu, dong = [], []
    for no, text in dong_bai:
        for w in chuan(text).split():
            tu.append(w)
            dong.append(no)
    out = []
    for url, text in nguon:
        src = chuan(text).split()
        grams = {tuple(src[i:i + N_CANH_BAO]) for i in range(len(src) - N_CANH_BAO + 1)}
        i = 0
        while i <= len(tu) - N_CANH_BAO:
            if tuple(tu[i:i + N_CANH_BAO]) not in grams:
                i += 1
                continue
            j = i
            while j + 1 <= len(tu) - N_CANH_BAO and tuple(tu[j + 1:j + 1 + N_CANH_BAO]) in grams:
                j += 1
            n = j - i + N_CANH_BAO
            out.append((dong[i], n, " ".join(tu[i:i + n]), url))
            i = j + N_CANH_BAO
    return out


def xem(args):
    folder = thu_muc_bai(args.bai)
    heads = doc_outline(args.bai)
    print("Outline: %s" % ("%d heading" % len(heads) if heads else "chưa lưu"))
    for url, text in doc_serp(args.bai):
        print("- SERP %s: %d từ" % (url, len(chuan(text).split())))
    if not os.path.isdir(folder):
        print("Chưa có thư mục %s" % os.path.relpath(folder, ROOT))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="lenh", required=True)
    p = sub.add_parser("luu-outline")
    p.add_argument("bai")
    p.add_argument("--tu", required=True, help="file outline (.md/.txt) hoặc JSON từ bảng điều phối")
    p.add_argument("--ly-do", help="bắt buộc khi lưu đè outline khác")
    p = sub.add_parser("luu-serp")
    p.add_argument("bai")
    p.add_argument("url", nargs="+")
    p.add_argument("--tu-file", help="văn bản đã lấy sẵn cho 1 URL")
    p = sub.add_parser("serp")
    p.add_argument("bai")
    p.add_argument("tu_khoa")
    p.add_argument("--luu", action="store_true", help="tải và lưu văn bản các bài blog trong top")
    p = sub.add_parser("xem")
    p.add_argument("bai")
    args = ap.parse_args()
    {"luu-outline": luu_outline, "luu-serp": luu_serp, "serp": serp, "xem": xem}[args.lenh](args)


if __name__ == "__main__":
    main()
