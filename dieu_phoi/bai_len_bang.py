"""Tạo JSON cho tài liệu bai_viet/<id> trên Bảng điều phối HLB.

Dùng: python dieu_phoi/bai_len_bang.py Bai_<slug>.md|DM_<slug>.md [--thay-doi "markdown"] > /tmp/bai.json
Sau đó ghi bằng ArtifactData action "set" (collection bai_viet, doc_id = id từ khóa, file_path = file JSON).
Lấy phần B (nội dung bài) và phần C (ghi chú cho người duyệt, trường ghi_chu), bỏ phần A. Số vòng lấy từ phiếu
.danh_gia/<file>.json. Trường sha là mã nội dung file bài: ghi kèm vào nhap_khop.sha khi đẩy nháp, để lượt sau biết
bản nháp và bài trên bảng có khớp file hiện tại không (dieu_phoi/doi_chieu_bang.py).
Dừng khi bài chưa có phiếu khớp nội dung hiện tại: bảng chỉ hiện bài đã chấm.
"""
import argparse
import datetime
import hashlib
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
ghi_chu = "\n".join(lines[end + 1:]).strip() if end is not None else ""
# Bỏ H1 (bảng đã hiện tiêu đề)
tieu_de = ""
for i, line in enumerate(body):
    if line.startswith("# "):
        tieu_de = line[2:].strip()
        body = body[:i] + body[i + 1:]
        break
loai = "danh_muc" if p.name.startswith("DM_") else "blog"
if loai == "danh_muc":
    # Noi dung danh muc khong co H1: tieu de lay ten danh muc (nghien_cuu/DM_x/danh_muc.json), khong co thi SEO title
    a_rows = {}
    for line in lines[:start]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            a_rows[cells[0]] = cells[1]
    dm_json = p.parent / "nghien_cuu" / p.stem / "danh_muc.json"
    if dm_json.exists():
        tieu_de = "Danh mục: " + json.loads(dm_json.read_text(encoding="utf-8")).get("ten", "")
    if tieu_de in ("", "Danh mục: "):
        tieu_de = "Danh mục: " + a_rows.get("SEO title", p.stem)
    nhan = {"[KHỐI TRÊN]": "*Khối trên (hiện trên lưới sản phẩm):*", "[KHỐI DƯỚI]": "*Khối dưới (hiện dưới lưới sản phẩm):*"}
    body = [nhan.get(line.strip(), line) for line in body]

sha = hashlib.sha256(p.read_bytes()).hexdigest()
phieu = p.parent / ".danh_gia" / (p.stem + ".json")
if not phieu.exists():
    sys.exit("Chưa có phiếu duyệt cho %s: chấm bài trước khi đưa lên bảng" % p.name)
pd = json.loads(phieu.read_text(encoding="utf-8"))
if pd.get("sha256") != sha:
    sys.exit("%s đã sửa sau lần chấm cuối (%s): chấm lại trước khi đưa lên bảng" % (p.name, pd.get("thoi_gian")))
vong = pd.get("vong")

out = {
    "tieu_de": tieu_de,
    "loai": loai,
    "noi_dung": "\n".join(body).strip(),
    "vong": vong,
    "file_bai": p.name,
    "thay_doi": a.thay_doi,
    "ghi_chu": ghi_chu,
    "sha": sha,
    "diem": pd.get("diem_tinh"),
    "ket_luan": pd.get("ket_luan"),
    "cap_nhat": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}
json.dump(out, sys.stdout, ensure_ascii=False)
