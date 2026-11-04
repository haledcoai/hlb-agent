"""Dang ban nhap bai viet len denlednhaxuongcaocap.com qua WordPress REST API.

Cach dung:
  python tools/wp_draft.py <file_bai.md> --new                 # bai moi, chi tao file xem truoc
  python tools/wp_draft.py <file_bai.md> --update 2323         # viet lai bai cu ID 2323, chi xem truoc
  them --post de gui len website (luon o trang thai draft, khong bao gio dang cong khai)
  them --khong-anh de bo qua anh trong anh/<ten bai>/anh.json (giu nguyen cho [ANH: ...])
  --post chi chay khi bai co phieu DAT khop noi dung (tools/phieu_duyet.py kiem); --bo-qua-phieu chi nguoi dung tu dung

Neu co anh/<ten bai>/anh.json (do tools/tao_anh.py ghi): xem truoc chen anh trong may;
--post tai anh len thu vien Media (anh nguon website thi dung lai URL co san), dien alt,
chen vao dung cho [ANH] va dat anh dai dien. Anh da tai luu media_id vao anh.json de khong tai lai.

Thong tin dang nhap doc tu bien moi truong WP_USER va WP_APP_PASSWORD
(Application Password tao trong wp-admin > Nguoi dung > Ho so).
"""
import argparse
import base64
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE = "https://denlednhaxuongcaocap.com"
API = SITE + "/wp-json"

PLACEHOLDER = re.compile(r"\[(?:CẦN BỔ SUNG|CẦN KIỂM TRA|CHỜ XÁC NHẬN|LINK|ẢNH|Ghi chú)[^\]]*\]")
IMAGE_LINE = re.compile(r"^(?:\*\*)?\[ẢNH:[^\]]*\|\s*tên file:\s*([^\]|]+?)\s*\](?:\*\*)?$")  # dong [ANH] co the in dam **...**
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BOLD = re.compile(r"\*\*(.+?)\*\*")


# ---------- Markdown -> HTML (chi cac the duoc phep o file Knowledge muc 10) ----------

def inline(text):
    out = html.escape(text, quote=False)
    out = out.replace("`", "")
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = LINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), out)
    out = PLACEHOLDER.sub(lambda m: "<strong>%s</strong>" % m.group(0), out)
    return out


def md_to_html(lines, headings=True):
    """headings=False: bien heading thanh doan in dam (dung cho khoi ghi chu bien tap)."""
    out, para, items, list_tag, table = [], [], [], None, []

    def flush():
        nonlocal para, items, list_tag, table
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            para = []
        if items:
            out.append("<%s>%s</%s>" % (list_tag, "".join("<li>%s</li>" % inline(i) for i in items), list_tag))
            items, list_tag = [], None
        if table:
            rows = [r for r in table if not re.fullmatch(r"\|[\s:|-]+\|", r)]
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            head = "".join("<th>%s</th>" % inline(c) for c in cells[0])
            body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in cells[1:])
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, body))
            table = []

    for raw in lines:
        line = raw.rstrip()
        m = re.match(r"^(#{2,4}) (.+)$", line)
        if not line.strip() or line.strip() == "---":
            flush()
        elif m:
            flush()
            if headings:
                level = len(m.group(1))
                out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            else:
                out.append("<p><strong>%s</strong></p>" % inline(m.group(2)))
        elif line.startswith("|"):
            if para or items:
                flush()
            table.append(line.strip())
        elif re.match(r"^- ", line):
            if para or table or list_tag == "ol":
                flush()
            list_tag = "ul"
            items.append(line[2:])
        elif re.match(r"^\d+\. ", line):
            if para or table or list_tag == "ul":
                flush()
            list_tag = "ol"
            items.append(re.sub(r"^\d+\. ", "", line))
        else:
            if items or table:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


# ---------- Doc file bai viet (phan A, B, C) ----------

def parse_article(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    sections, current = {}, None
    for line in lines:
        m = re.match(r"^# ([ABC])\.", line)
        if m:
            current = m.group(1)
            sections[current] = []
        elif current:
            sections[current].append(line)
    for key in "ABC":
        if key not in sections:
            sys.exit("Thieu phan %s trong file %s" % (key, path))

    seo = {}
    for line in sections["A"]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] not in ("Trường", "") and not set(cells[0]) <= set("-: "):
            seo[cells[0]] = cells[1]

    body = sections["B"]
    title_idx = next(i for i, l in enumerate(body) if l.startswith("# "))
    title = body[title_idx][2:].strip()
    return seo, title, body[title_idx + 1:], sections["C"]


# ---------- REST API ----------

def credentials():
    user = os.environ.get("WP_USER")
    pwd = os.environ.get("WP_APP_PASSWORD")
    if (not user or not pwd) and sys.platform == "win32":
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            def read(name):
                try:
                    return winreg.QueryValueEx(k, name)[0]
                except FileNotFoundError:
                    return None
            user, pwd = user or read("WP_USER"), pwd or read("WP_APP_PASSWORD")
    if not user or not pwd:
        sys.exit("Chua co WP_USER va WP_APP_PASSWORD. Xem huong dan trong tools/HUONG_DAN_DANG_NHAP.md")
    return base64.b64encode(("%s:%s" % (user, pwd)).encode()).decode()


def call(method, path, data=None, auth=None):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("User-Agent", "HLB-draft-agent/1.0")
    if auth:
        req.add_header("Authorization", "Basic " + auth)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urllib.request.urlopen(req, body, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError("%s %s -> HTTP %s: %s" % (method, path, e.code, detail))


def category_id(name):
    slug = re.sub(r"\s+", "-", name.strip().lower())
    known = {"tư-vấn": "tu-van", "tin-tức": "tin-tuc", "công-nghệ": "cong-nghe", "dự-án": "du-an"}
    slug = known.get(slug, slug)
    res = call("GET", "/wp/v2/categories?slug=%s&_fields=id" % urllib.parse.quote(slug))
    return [res[0]["id"]] if res else []


def upload_media(path, alt, title, description, auth):
    """Tai mot file anh len thu vien Media, dien Alt, Tieu de, Mo ta; tra ve (id, source_url)."""
    name = os.path.basename(path)
    req = urllib.request.Request(API + "/wp/v2/media", method="POST")
    req.add_header("User-Agent", "HLB-draft-agent/1.0")
    req.add_header("Authorization", "Basic " + auth)
    req.add_header("Content-Type", "image/webp" if name.endswith(".webp") else "image/jpeg")
    req.add_header("Content-Disposition", 'attachment; filename="%s"' % name)
    with open(path, "rb") as f:
        body = f.read()
    try:
        with urllib.request.urlopen(req, body, timeout=120) as r:
            media = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("POST /wp/v2/media -> HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:500]))
    call("POST", "/wp/v2/media/%d" % media["id"], {"alt_text": alt, "title": title, "description": description}, auth=auth)
    return media["id"], media["source_url"]


def hoa_dau(text):
    """Viet hoa chu dau (mo ta, alt trong dong [ANH] co the viet thuong, vi du bai 8524), giu nguyen phan con lai."""
    text = text.strip()
    return text[:1].upper() + text[1:]


def media_description(a):
    """Mo ta anh trong thu vien Media: noi dung anh theo [ANH], ghi ro anh minh hoa neu tao bang AI."""
    desc = hoa_dau(a["mo_ta"]).rstrip(".") + "."
    if a["nguon"] in ("canva", "kho-anh"):
        desc += " Ảnh minh họa."
    if a.get("tac_gia"):
        desc += " Ảnh: %s." % a["tac_gia"]
    elif a["nguon"] == "python":
        desc += " Sơ đồ minh họa theo số liệu trong bài."
    return desc


# ---------- Anh trong bai ----------

def manifest_path(article):
    return os.path.join(ROOT, "anh", os.path.splitext(os.path.basename(article))[0], "anh.json")


def load_images(article):
    try:
        with open(manifest_path(article), encoding="utf-8") as f:
            return {a["ten"]: a for a in json.load(f)["anh"]}
    except (OSError, ValueError):
        return {}


def mark_images(body_lines, images):
    """Thay dong [ANH: ... | ten file: x] co anh trong danh sach bang token @@ANH:x@@."""
    out = []
    for line in body_lines:
        m = IMAGE_LINE.match(line.strip())
        out.append("@@ANH:%s@@" % m.group(1) if m and m.group(1) in images else line)
    return out


def image_caption(a):
    """Chu thich hien duoi anh: noi dung anh theo [ANH]; anh tao bang AI ghi ro la anh minh hoa."""
    cap = hoa_dau(a["mo_ta"]).rstrip(".")
    # Ten tac gia anh kho (Unsplash) chi ghi trong mo ta Media, chu thich chi ghi "anh minh hoa" (nguoi dung chot 23/10/2026)
    return cap + " (ảnh minh họa)" if a["nguon"] in ("canva", "kho-anh") else cap


def insert_images(content, images, src_of, preview=False):
    """Chen anh can giua kem chu thich ben duoi, theo kieu [caption] cac bai cu tren website dang dung
    (theme co CSS .aligncenter va .wp-caption). Xem truoc trong may thi doi sang <figure>."""
    def repl(m):
        a = images[m.group(1)]
        w = h = None
        if a["nguon"] != "website":
            try:
                from PIL import Image
                with Image.open(os.path.join(ROOT, a["file"])) as im:
                    w, h = im.size
            except (OSError, ImportError):
                pass
        size = ' width="%d" height="%d"' % (w, h) if w else ""
        cap = html.escape(image_caption(a))
        if preview:
            return ('<figure class="aligncenter"><img src="%s" alt="%s"%s><figcaption>%s</figcaption></figure>'
                    % (html.escape(src_of(a)), html.escape(hoa_dau(a["alt"])), size, cap))
        mid = a.get("media_id")
        img = '<img class="size-full%s" src="%s" alt="%s"%s>' % (
            " wp-image-%d" % mid if mid else "", html.escape(src_of(a)), html.escape(hoa_dau(a["alt"])), size)
        return '[caption id="%s" align="aligncenter" width="%d"]%s %s[/caption]' % (
            "attachment_%d" % mid if mid else "", w or 820, img, cap)
    return re.sub(r"<p>@@ANH:([^@]+)@@</p>", repl, content)


def split_images(images, body_lines):
    """Tach anh dung duoc va cac cho [ANH] con thieu (khong co anh, chua duoc duyet tren trang Duyet anh HLB,
    hoac anh sai chuan JPG 800-850 x 400-800)."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from tao_anh import loi_chuan
    valid, missing = {}, []
    for ten, a in images.items():
        if a.get("trang_thai") != "duyet":
            ok = False
        elif a["nguon"] == "website":
            ok = bool(a.get("url_website"))
        else:
            path = os.path.join(ROOT, a["file"])
            ok = os.path.isfile(path) and not loi_chuan(path)
        if ok:
            valid[ten] = a
    for line in body_lines:
        m = IMAGE_LINE.match(line.strip())
        if m and m.group(1) not in valid:
            missing.append(m.group(1))
    if valid and not any(a.get("dai_dien") for a in valid.values()):
        next(iter(valid.values()))["dai_dien"] = True  # anh dai dien thieu thi lay anh dau tien co san
    return valid, missing


def note_missing(content, missing):
    if not missing:
        return content
    items = "".join("<li>%s</li>" % html.escape(t) for t in missing)
    note = ("<p><strong>ẢNH CÒN THIẾU (%d):</strong> giữ nguyên chỗ [ẢNH] in đậm trong bài, cần chuẩn bị:</p><ul>%s</ul>\n"
            % (len(missing), items))
    marker = "<p><strong>NỘI DUNG BÀI BẮT ĐẦU TỪ ĐÂY</strong></p>"
    return content.replace(marker, note + marker, 1)


# ---------- Ghep noi dung ban nhap ----------

def build(seo, title, body_lines, notes_lines, mode, original):
    rows = [
        ("Focus keyword", seo.get("Focus keyword", "")),
        ("SEO title", seo.get("SEO title", "")),
        ("Meta description", seo.get("Meta description", "")),
        ("Slug", seo.get("Slug", "")),
        ("Tag đề xuất", seo.get("Tag", "")),
    ]
    if mode == "update":
        kind = (
            "<p><strong>LOẠI: CẬP NHẬT BÀI CŨ.</strong> Bài gốc ID %d: <a href=\"%s\">%s</a>, "
            "tiêu đề hiện tại \"%s\".</p>"
            "<p><strong>Cách đăng:</strong> không bấm Đăng bản nháp này. Mở bài gốc ID %d, thay toàn bộ nội dung "
            "bằng phần dưới dòng NỘI DUNG BÀI, sửa tiêu đề thành tiêu đề mới, cập nhật SEO title và meta "
            "description trong Rank Math, bấm Cập nhật, rồi chuyển bản nháp này vào thùng rác.</p>"
            % (original["id"], original["link"], original["link"], html.escape(original["title"]), original["id"])
        )
        rows.insert(0, ("Tiêu đề mới cho bài gốc", title))
    else:
        kind = (
            "<p><strong>LOẠI: BÀI MỚI.</strong> Chủ đề chưa có trên website.</p>"
            "<p><strong>Cách đăng:</strong> xử lý hết các chỗ in đậm [CẦN BỔ SUNG], [CẦN KIỂM TRA], [LINK], [ẢNH], "
            "xóa toàn bộ phần ghi chú này, bỏ tiền tố [MỚI] ở tiêu đề, rồi bấm Đăng.</p>"
        )
    seo_table = "<table><tbody>%s</tbody></table>" % "".join(
        "<tr><td><strong>%s</strong></td><td>%s</td></tr>" % (html.escape(k), inline(v)) for k, v in rows
    )
    note = (
        "<p><strong>GHI CHÚ BIÊN TẬP. XÓA TOÀN BỘ PHẦN NÀY TRƯỚC KHI ĐĂNG.</strong></p>\n%s\n%s\n%s\n"
        "<p><strong>NỘI DUNG BÀI BẮT ĐẦU TỪ ĐÂY</strong></p>\n<hr>\n"
        % (kind, seo_table, md_to_html(notes_lines, headings=False))
    )
    return note + md_to_html(body_lines)


def fill_rank_math(post_id, seo, auth):
    """Dien focus keyword, SEO title, meta description vao Rank Math (ca khi tao moi lan ghi de ban nhap)."""
    meta = {
        "rank_math_focus_keyword": seo.get("Focus keyword", ""),
        "rank_math_title": seo.get("SEO title", ""),
        "rank_math_description": seo.get("Meta description", ""),
    }
    try:
        call("POST", "/rankmath/v1/updateMeta",
             {"objectType": "post", "objectID": post_id, "meta": meta}, auth=auth)
        print("Da dien SEO title, meta description, focus keyword vao Rank Math.")
    except RuntimeError as e:
        print("Chua dien duoc Rank Math tu dong (thong tin SEO van nam trong khoi ghi chu):", e)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--new", action="store_true", help="chu de moi")
    group.add_argument("--update", type=int, metavar="POST_ID", help="viet lai bai da co")
    ap.add_argument("--post", action="store_true", help="gui len website (mac dinh chi tao file xem truoc)")
    ap.add_argument("--force", action="store_true", help="van tao du da co ban nhap trung tieu de")
    ap.add_argument("--draft-id", type=int, help="ghi de noi dung len ban nhap da tao (chi ap dung cho ban nhap)")
    ap.add_argument("--khong-anh", action="store_true", help="bo qua anh trong anh/<ten bai>/anh.json")
    ap.add_argument("--bo-qua-phieu", action="store_true",
                    help="chi nguoi dung tu chay: dang du bai chua co phieu DAT (agent khong duoc dung)")
    args = ap.parse_args()

    if args.post and not args.bo_qua_phieu:
        # Kiem tra ngay trong script, khong chi dua vao hook PreToolUse: phien cloud co the khong nap hook
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import phieu_duyet
        reasons = phieu_duyet.kiem(os.path.abspath(args.article))
        if reasons:
            print("Chua duoc dang ban nhap:", file=sys.stderr)
            for r in reasons:
                print("- " + r, file=sys.stderr)
            sys.exit("Lam theo vong duyet trong CLAUDE.md. Nguoi dung muon dang khi bai chua dat thi tu chay lenh voi --bo-qua-phieu.")

    seo, title, body, notes = parse_article(args.article)
    images = {} if args.khong_anh else load_images(args.article)
    all_images = images
    images, missing = split_images(images, body) if images else ({}, [])
    body = mark_images(body, images)
    mode = "update" if args.update else "new"

    original = None
    if mode == "update":
        o = call("GET", "/wp/v2/posts/%d?_fields=id,link,title,status" % args.update)
        original = {"id": o["id"], "link": o["link"], "title": html.unescape(o["title"]["rendered"])}
        draft_title = "[CẬP NHẬT #%d] %s" % (o["id"], title)
        draft_slug = "ban-nhap-cap-nhat-%d" % o["id"]
    else:
        slug = seo.get("Slug", "").split(" ")[0]
        if slug and call("GET", "/wp/v2/posts?slug=%s&_fields=id,link" % urllib.parse.quote(slug)):
            sys.exit("Slug '%s' da co bai cong khai tren website. Day la bai cu, hay dung --update." % slug)
        draft_title = "[MỚI] " + title
        draft_slug = slug

    content = note_missing(build(seo, title, body, notes, mode, original), missing)
    preview = os.path.splitext(args.article)[0] + ".preview.html"
    preview_dir = os.path.dirname(os.path.abspath(preview))

    def local_src(a):
        if a["nguon"] == "website":
            return a["url_website"]
        return os.path.relpath(os.path.join(ROOT, a["file"]), preview_dir).replace("\\", "/")

    with open(preview, "w", encoding="utf-8", newline="\n") as f:
        f.write("<!doctype html><meta charset=utf-8><title>%s</title>"
                "<style>img{max-width:100%%;height:auto}.aligncenter{display:block;margin:1em auto;text-align:center}"
                "figcaption{font-size:14px;color:#555;margin-top:6px}</style><h1>%s</h1>\n%s"
                % (html.escape(draft_title), html.escape(draft_title), insert_images(content, images, local_src, preview=True)))
    print("Tieu de ban nhap:", draft_title)
    print("File xem truoc:", preview)
    if all_images:
        print("Anh: chen %d anh tu %s" % (len(images), os.path.relpath(manifest_path(args.article), ROOT)))
    if missing:
        print("Anh con thieu hoac sai chuan (giu cho [ANH], ghi vao ghi chu bien tap):", ", ".join(missing))

    if not args.post:
        print("Chua gui len website. Them --post de tao ban nhap.")
        return

    auth = credentials()

    # Tai anh len thu vien Media; anh nguon website dung lai URL co san; anh da tai va chua doi thi khong tai lai
    featured = None
    if images:
        import hashlib
        for a in images.values():
            if a["nguon"] != "website":
                path = os.path.join(ROOT, a["file"])
                with open(path, "rb") as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
                if a.get("media_id") and a.get("url_da_tai") and a.get("sha_da_tai") == digest:
                    print("Dung lai anh da tai:", a["url_da_tai"])
                else:
                    a["media_id"], a["url_da_tai"] = upload_media(path, hoa_dau(a["alt"]), hoa_dau(a["alt"]),
                                                                  media_description(a), auth)
                    a["sha_da_tai"] = digest
                    print("Da tai anh len Media ID %d: %s" % (a["media_id"], a["url_da_tai"]))
                # Anh dung lai tu bai khac: media dung chung, khong ghi de chu thich cua bai goc
                if not a.get("dung_lai_tu") and a.get("chu_thich_da_ghi") != image_caption(a):
                    call("POST", "/wp/v2/media/%d" % a["media_id"], {
                        "caption": image_caption(a), "alt_text": hoa_dau(a["alt"]), "title": hoa_dau(a["alt"]),
                        "description": media_description(a)}, auth=auth)
                    a["chu_thich_da_ghi"] = image_caption(a)
            if a.get("dai_dien"):
                featured = a.get("media_id")
        with open(manifest_path(args.article), encoding="utf-8") as f:
            manifest = json.load(f)
        manifest["anh"] = [images.get(t, a) for t, a in all_images.items()]
        with open(manifest_path(args.article), "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        content = insert_images(content, images, lambda a: a.get("url_da_tai") or a["url_website"])

    if args.draft_id:
        cur = call("GET", "/wp/v2/posts/%d?context=edit&_fields=id,status" % args.draft_id, auth=auth)
        if cur["status"] != "draft":
            sys.exit("Bai ID %d khong phai ban nhap (status=%s). Khong ghi de." % (args.draft_id, cur["status"]))
        # Phan A co the da doi sau lan tao ban nhap: cap nhat ca excerpt va Rank Math, khong chi noi dung
        update = {"title": draft_title, "content": content, "excerpt": seo.get("Excerpt", "")}
        if featured:
            update["featured_media"] = featured
        call("POST", "/wp/v2/posts/%d" % args.draft_id, update, auth=auth)
        print("Da cap nhat ban nhap ID", args.draft_id)
        fill_rank_math(args.draft_id, seo, auth)
        print("Mo de duyet:", "%s/wp-admin/post.php?post=%d&action=edit" % (SITE, args.draft_id))
        return
    same = call("GET", "/wp/v2/posts?status=draft&context=edit&search=%s&_fields=id,title"
                % urllib.parse.quote(title[:60]), auth=auth)
    dup = [p for p in same if p["title"]["raw"] == draft_title]
    if dup and not args.force:
        sys.exit("Da co ban nhap trung tieu de (ID %s). Them --force neu van muon tao them." % dup[0]["id"])

    new_post = {
        "title": draft_title,
        "content": content,
        "status": "draft",
        "slug": draft_slug,
        "excerpt": seo.get("Excerpt", ""),
        "categories": category_id(seo.get("Category", "Tư vấn")),
    }
    if featured:
        new_post["featured_media"] = featured
    post = call("POST", "/wp/v2/posts", new_post, auth=auth)
    print("Da tao ban nhap ID", post["id"])
    print("Mo de duyet:", "%s/wp-admin/post.php?post=%d&action=edit" % (SITE, post["id"]))

    fill_rank_math(post["id"], seo, auth)


if __name__ == "__main__":
    main()
