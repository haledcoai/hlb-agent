"""Đưa ảnh chờ duyệt của một bài lên tab Duyệt ảnh (collection `anh`) của Bảng điều phối HLB, một lần cho cả bài.

Bước 1: python dieu_phoi/anh_len_bang.py Bai_<slug>.md
        In danh sách file JPG cần tải lên trang (Artifact publish, asset: true, file_paths).
        Ảnh dùng lại hoặc ảnh có sẵn trên website không cần tải, trang hiện bằng URL website.
Bước 2: ghi kết quả tải lên vào một file JSON {"<tên file>.jpg": {"url": "...", "asset_id": "..."}}, rồi
        python dieu_phoi/anh_len_bang.py Bai_<slug>.md --tai-san <file.json> --out <thư mục tạm>
        Script ghi mỗi ảnh một file JSON và in mảng `writes` để dán vào ArtifactData batch.
Chỉ tạo dòng mới (ảnh chưa có trên trang). Ảnh làm lại cập nhật dòng cũ theo CLAUDE.md (cần if_version, ghi_chu_truoc).
"""
import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import tao_anh  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("article")
ap.add_argument("--tai-san", help="JSON ket qua tai anh len trang: {ten: {url, asset_id}}")
ap.add_argument("--out", help="thu muc ghi file JSON tung dong")
a = ap.parse_args()
sys.stdout.reconfigure(encoding="utf-8")

bai = os.path.splitext(os.path.basename(a.article))[0]
cho = tao_anh.doc_cho_anh(a.article)
thu_tu = {c["ten"]: (i + 1, c["heading"]) for i, c in enumerate(cho)}
m = {x["ten"]: x for x in tao_anh.doc_manifest(a.article)["anh"]}
ds = [m[c["ten"]] for c in cho if c["ten"] in m and m[c["ten"]].get("trang_thai") == "cho_duyet"]
if not ds:
    sys.exit("Bài không có ảnh chờ duyệt")


def url_san(x):
    """Anh da co URL cong khai (dung lai, nguon website) thi trang hien bang URL do, khong tai len trang."""
    return x.get("url_da_tai") if x.get("dung_lai_tu") else (x.get("url_website") if x["nguon"] == "website" else None)


if not a.tai_san:
    can_tai = [os.path.join(tao_anh.ROOT, x["file"]) for x in ds if not url_san(x)]
    print(json.dumps(can_tai, ensure_ascii=False))
    print("%d ảnh cần tải lên trang, %d ảnh dùng URL có sẵn." % (len(can_tai), len(ds) - len(can_tai)), file=sys.stderr)
    sys.exit(0)

if not a.out:
    sys.exit("Thiếu --out")
with open(a.tai_san, encoding="utf-8") as f:
    tai_san = json.load(f)
with open(a.article, encoding="utf-8") as f:
    tieu_de = next((l[2:].strip() for l in f.read().splitlines()
                    if l.startswith("# ") and not l.startswith(("# A.", "# B.", "# C."))), bai)
os.makedirs(a.out, exist_ok=True)
luc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
writes, thieu = [], []
from PIL import Image  # noqa: E402

for x in ds:
    if url_san(x):
        url, asset = url_san(x), ""
    elif x["ten"] in tai_san:
        url, asset = tai_san[x["ten"]]["url"], tai_san[x["ten"]].get("asset_id", "")
    else:
        thieu.append(x["ten"])
        continue
    with Image.open(os.path.join(tao_anh.ROOT, x["file"])) as im:
        rong, cao = im.size
    so, muc = thu_tu[x["ten"]]
    doc = {"bai": bai, "tieu_de_bai": tieu_de, "ten": x["ten"], "thu_tu": so, "muc": muc, "alt": x["alt"],
           "nguon": x["nguon"], "url": url, "asset_id": asset, "rong": rong, "cao": cao, "vong": 1,
           "trang_thai": "cho_duyet", "ghi_chu": "",
           "ghi_chu_agent": ("Dùng lại ảnh đã duyệt %s. " % x["dung_lai_tu"] if x.get("dung_lai_tu") else "")
           + x.get("ghi_chu", ""), "cap_nhat": luc}
    p = os.path.abspath(os.path.join(a.out, "%s--%s.json" % (bai, x["ten"])))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False)
    writes.append({"op": "set", "collection": "anh", "doc_id": "%s--%s" % (bai, x["ten"]), "file_path": p})
print(json.dumps(writes, ensure_ascii=False))
if thieu:
    sys.exit("Chưa có URL tải lên trang cho: " + ", ".join(thieu))
