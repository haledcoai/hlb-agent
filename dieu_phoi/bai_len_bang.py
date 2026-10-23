"""Tạo JSON cho tài liệu bai_viet/<id> trên Bảng điều phối HLB.

Dùng: python dieu_phoi/bai_len_bang.py Bai_<slug>.md [--thay-doi "markdown"] > /tmp/bai.json
Sau đó ghi bằng ArtifactData action "set" (collection bai_viet, doc_id = id từ khóa, file_path = file JSON).
Chỉ lấy phần B (nội dung bài), bỏ phần A và C. Số vòng lấy từ phiếu .danh_gia/<file>.json.
"""
import argparse
import datetime
import json
import pathlib
import sys

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("--thay-doi", default="")
a = ap.parse_args()

p = pathlib.Path(a.file)
lines = p.read_text(encoding="utf-8").splitlines()
start = end = None
for i, line in enumerate(lines):
    if line.startswith("# B.") and start is None:
        start = i + 1
    elif line.startswith("# C.") and start is not None:
        end = i
        break
if start is None:
    sys.exit("Không thấy dòng '# B.' trong bài")
body = lines[start:end]
# Bỏ H1 (bảng đã hiện tiêu đề)
tieu_de = ""
for i, line in enumerate(body):
    if line.startswith("# "):
        tieu_de = line[2:].strip()
        body = body[:i] + body[i + 1:]
        break

phieu = p.parent / ".danh_gia" / (p.stem + ".json")
vong = None
if phieu.exists():
    vong = json.loads(phieu.read_text(encoding="utf-8")).get("vong")

out = {
    "tieu_de": tieu_de,
    "noi_dung": "\n".join(body).strip(),
    "vong": vong,
    "file_bai": p.name,
    "thay_doi": a.thay_doi,
    "cap_nhat": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}
json.dump(out, sys.stdout, ensure_ascii=False)
