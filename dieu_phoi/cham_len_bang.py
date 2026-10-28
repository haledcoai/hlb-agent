"""Gộp kết quả `tools/phieu_duyet.py xuat` thành một tài liệu cho tab Lịch sử chấm điểm trên Bảng điều phối HLB.

Dùng: python tools/phieu_duyet.py xuat && python dieu_phoi/cham_len_bang.py > /tmp/cham.json
Sau đó ArtifactData "set" collection cham_bai, doc_id tong_hop, file_path = file JSON.
"""
import datetime
import json
import pathlib
import sys

goc = pathlib.Path(__file__).resolve().parent.parent / ".danh_gia" / "xuat"
out = {}
for ten in ("cham", "van_de", "bac_bo", "tieu_chi"):
    f = goc / f"{ten}.json"
    out[ten] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
out["cap_nhat"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
json.dump(out, sys.stdout, ensure_ascii=False)
