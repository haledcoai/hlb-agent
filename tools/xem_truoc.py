"""Xem truoc bai kem anh, chi doc file trong may: khong doc mat khau, khong goi website, khong tai gi len.
Dung khi khong chay duoc wp_draft.py (phien cloud o auto mode chan script dang bai).
Cach dung:
  python tools/xem_truoc.py <file_bai.md>              # ghi <file_bai>.preview.html canh file bai
Anh chen giong het khi dang (cung ham voi wp_draft.py): chi anh da duyet va dung chuan, kem chu thich;
cho [ANH] con thieu giu nguyen va liet ke o dau trang.
"""
import argparse
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wp_draft import ROOT, insert_images, load_images, mark_images, md_to_html, parse_article, split_images  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    args = ap.parse_args()

    seo, title, body, notes = parse_article(args.article)
    images, missing = split_images(load_images(args.article), body)
    body = mark_images(body, images)
    # Chi phan B nhu nguoi doc thay; bang SEO va ghi chu bien tap chi co trong ban nhap tao bang wp_draft.py
    content = md_to_html(body)
    if missing:
        content = ("<p class=thieu><strong>Ảnh còn thiếu hoặc chưa duyệt (%d):</strong> %s</p>\n"
                   % (len(missing), html.escape(", ".join(missing)))) + content

    preview = os.path.splitext(args.article)[0] + ".preview.html"
    preview_dir = os.path.dirname(os.path.abspath(preview))

    def local_src(a):
        if a["nguon"] == "website" or (a.get("dung_lai_tu") and not os.path.isfile(os.path.join(ROOT, a["file"]))):
            return a.get("url_website") or a.get("url_da_tai")
        return os.path.relpath(os.path.join(ROOT, a["file"]), preview_dir).replace("\\", "/")

    dai_dien = next((a for a in images.values() if a.get("dai_dien")), None)
    head = ""
    if dai_dien:
        head = '<p class=dd>Ảnh đại diện: %s</p>' % html.escape(dai_dien["ten"])
    with open(preview, "w", encoding="utf-8") as f:
        f.write("<!doctype html><html lang=vi><meta charset=utf-8>"
                "<meta name=viewport content=\"width=device-width,initial-scale=1\"><title>%s</title>"
                "<style>body{max-width:820px;margin:0 auto;padding:16px;font:17px/1.6 system-ui,sans-serif;"
                "color:#222;background:#fff}img{max-width:100%%;height:auto}"
                ".aligncenter{display:block;margin:1.2em auto;text-align:center}"
                "figcaption{font-size:14px;color:#555;margin-top:6px}table{border-collapse:collapse;width:100%%}"
                "td,th{border:1px solid #ccc;padding:6px 8px}.thieu{background:#fff4e0;padding:8px}"
                ".dd{font-size:14px;color:#555}</style><h1>%s</h1>%s\n%s"
                % (html.escape(title), html.escape(title), head,
                   insert_images(content, images, local_src, preview=True)))
    print("File xem trước:", preview)
    print("Ảnh: chèn %d ảnh đã duyệt%s" % (len(images), ", còn thiếu: " + ", ".join(missing) if missing else ""))


if __name__ == "__main__":
    main()
