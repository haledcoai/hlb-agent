"""Lam moi file du lieu san pham tu website denlednhaxuongcaocap.com.

Cach dung:
  python tools/lam_moi_csv.py            # doc lai gia, thong so 113 san pham, ghi du_lieu_san_pham_HLB_<dd-mm-yyyy>.csv
  python tools/lam_moi_csv.py --xem      # chi in khac biet so voi file CSV moi nhat, khong ghi file

Gia lay tu API WooCommerce Store (truong prices.price, gia dang ban cua chinh san pham).
Thong so lay tu 2 bang tren trang san pham (khoi dau trang va bang "Thong so ky thuat").
Ghi file moi va xoa file cu (lich su con trong git). In danh sach thay doi gia, thong so,
san pham moi, san pham bi go de agent biet bai nao co the da cu.
Chay dau moi luot dieu phoi (DIEU_PHOI.md muc 4) va truoc khi viet bai co gia.
"""
import argparse
import concurrent.futures
import csv
import datetime
import glob
import html
import json
import os
import re
import sys
import urllib.request

SITE = "https://denlednhaxuongcaocap.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["name", "price", "brand", "bh", "ip", "w", "pf", "lm", "life", "cct", "ra", "cert", "goc", "url"]
# Ten dong trong bang tren trang san pham -> cot CSV. Trang khac nhau ghi nhan khac nhau
# ("Công suất (W)", "Công suất (w)", "Quang thông (lm)", "Quang thông"), nen so theo dau nhan, thu tu quan trong
NHAN = [
    ("hệ số công suất", "pf"), ("công suất", "w"), ("quang thông", "lm"), ("tuổi thọ", "life"),
    ("nhiệt độ màu", "cct"), ("chỉ số hoàn màu", "ra"), ("chứng nhận", "cert"), ("góc", "goc"),
    ("bảo hành", "bh"), ("hãng sản xuất", "brand"),
]
# Cot chi giu so (bo don vi viet lien: "26000lm", "50000 giờ", "85Ra", "250W")
CHI_SO = {"w", "lm", "life", "ra"}


def cot(label):
    low = label.lower().strip()
    for prefix, key in NHAN:
        if low.startswith(prefix):
            return key
    return None


def gia_tri(key, val):
    if key in CHI_SO:
        m = re.fullmatch(r"([\d.,]+)\s*(w|lm|giờ|h|ra)?", val.strip(), re.I)
        if m:
            return m.group(1)
    return val


def get(url, as_json=False):
    req = urllib.request.Request(url, headers={"User-Agent": "HLB-lam-moi-csv/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8")
    return json.loads(body) if as_json else body


def ngay_file(path):
    m = re.search(r"(\d{2})-(\d{2})-(\d{4})\.csv$", path)
    return (m.group(3), m.group(2), m.group(1)) if m else ("0", "0", "0")


def csv_moi_nhat():
    found = sorted(glob.glob(os.path.join(ROOT, "du_lieu_san_pham_*.csv")), key=ngay_file)
    return found[-1] if found else None


def doc_trang(url):
    """Hai bang dau trang san pham -> dict cot CSV."""
    page = get(url)
    row = {}
    tables = re.findall(r"<table.*?</table>", page, re.S)
    for i, t in enumerate(tables[:2]):
        for tr in re.findall(r"<tr.*?</tr>", t, re.S):
            cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip()
                     for c in re.findall(r"<t[dh].*?</t[dh]>", tr, re.S)]
            if len(cells) != 2:
                continue
            key, val = cells
            if key == "Tiêu chuẩn" and i == 0:
                row["ip"] = val  # khoi dau trang: "IP54, CE, RoHS", giong cot ip cua file cu
            elif cot(key) and cot(key) not in row and val:
                row[cot(key)] = gia_tri(cot(key), val)
    return row


def lay_san_pham():
    items, page = [], 1
    while True:
        batch = get("%s/wp-json/wc/store/v1/products?per_page=100&page=%d" % (SITE, page), as_json=True)
        items += batch
        if len(batch) < 100:
            break
        page += 1
    rows = []

    def one(p):
        row = {k: "" for k in COLS}
        row.update(name=html.unescape(p["name"]), price=p["prices"]["price"] or "0", url=p["permalink"])
        try:
            row.update(doc_trang(p["permalink"]))
        except OSError as e:
            row["_loi"] = str(e)
        return row

    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(one, items))
    return rows


def khac_biet(old_rows, new_rows):
    old = {r["url"]: r for r in old_rows}
    new = {r["url"]: r for r in new_rows}
    out = []
    for url, r in new.items():
        o = old.get(url)
        if not o:
            out.append("Mới: %s" % r["name"])
            continue
        for k in COLS:
            if k in ("url",):
                continue
            if (o.get(k) or "").strip() != (r.get(k) or "").strip():
                out.append("%s: %s %s -> %s" % (r["name"], k, o.get(k) or "(trống)", r.get(k) or "(trống)"))
    for url, o in old.items():
        if url not in new:
            out.append("Không còn trên website: %s" % o["name"])
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--xem", action="store_true", help="chi in khac biet, khong ghi file")
    args = ap.parse_args()

    rows = lay_san_pham()
    loi = [r for r in rows if r.pop("_loi", None)]
    cu = csv_moi_nhat()
    old_rows = list(csv.DictReader(open(cu, encoding="utf-8-sig"))) if cu else []
    diff = khac_biet(old_rows, rows)
    print("Đọc %d sản phẩm từ website%s." % (len(rows), ", %d trang không mở được" % len(loi) if loi else ""))
    print("So với %s: %d thay đổi" % (os.path.basename(cu) if cu else "(chưa có file)", len(diff)))
    for d in diff:
        print("- " + d)
    if args.xem:
        return
    if loi:
        sys.exit("Có trang sản phẩm không mở được, giữ nguyên file cũ. Chạy lại sau.")
    ten = "du_lieu_san_pham_HLB_%s.csv" % datetime.date.today().strftime("%d-%m-%Y")
    path = os.path.join(ROOT, ten)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in sorted(rows, key=lambda r: r["url"]):
            w.writerow({k: r.get(k, "") for k in COLS})
    if cu and os.path.abspath(cu) != os.path.abspath(path):
        os.remove(cu)
    print("Đã ghi %s%s" % (ten, ", xóa %s" % os.path.basename(cu) if cu and os.path.basename(cu) != ten else ""))


if __name__ == "__main__":
    main()
