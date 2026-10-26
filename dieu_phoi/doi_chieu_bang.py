"""Đối chiếu Bảng điều phối HLB với file bài trên repo, tìm chỗ bảng hiện sai (bản nháp cũ, điểm cũ, bài không có trên bảng).

Dùng (mỗi lượt điều phối, DIEU_PHOI.md mục 4 bước 2, và sau khi một thread sửa bài):
  ArtifactData list collection tu_khoa (và bai_viet) với out_dir=<thư mục tạm>
  python dieu_phoi/doi_chieu_bang.py <thư mục tạm>

Thư mục tạm là thư mục ArtifactData ghi ra, có tu_khoa/<id>.json và bai_viet/<id>.json.
In từng việc cần làm; không ghi gì lên bảng. Thoát mã 1 khi có chỗ lệch.
"""
import datetime
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def doc(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("data", d)


def gio(iso):
    try:
        return datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    goc = sys.argv[1]
    rows = {os.path.splitext(os.path.basename(p))[0]: doc(p) for p in glob.glob(os.path.join(goc, "tu_khoa", "*.json"))}
    bai_viet = {os.path.splitext(os.path.basename(p))[0]: doc(p) for p in glob.glob(os.path.join(goc, "bai_viet", "*.json"))}
    lech = 0
    co_tren_bang = set()
    for rid, r in sorted(rows.items()):
        fb = r.get("file_bai")
        if not fb or r.get("trang_thai") == "bo_qua":
            continue
        co_tren_bang.add(fb)
        path = os.path.join(ROOT, fb)
        viec = []
        if not os.path.isfile(path):
            viec.append("không thấy file %s trên repo" % fb)
        else:
            with open(path, "rb") as f:
                sha = hashlib.sha256(f.read()).hexdigest()
            try:
                phieu = doc(os.path.join(ROOT, ".danh_gia", os.path.splitext(fb)[0] + ".json"))
            except OSError:
                phieu = {}
            khop = phieu.get("sha256") == sha
            if not khop:
                viec.append("file bài sửa sau lần chấm cuối: chấm lại (vòng duyệt CLAUDE.md)")
            dv = r.get("diem_vong") or []
            if khop and (not dv or dv[-1].get("diem") != phieu.get("diem_tinh") or dv[-1].get("vong") != phieu.get("vong")):
                viec.append("diem_vong trên bảng (%s) khác phiếu mới nhất (vòng %s, %s điểm): thêm vòng mới, cập nhật bao_cao"
                            % (dv[-1] if dv else "trống", phieu.get("vong"), phieu.get("diem_tinh")))
            nk = r.get("nhap_khop")
            if nk:
                if nk.get("sha"):
                    nhap_cu = nk["sha"] != sha
                else:  # nhap_khop cu chua ghi sha: so gio day nhap voi gio cham cuoi
                    t_nk, t_ph = gio(nk.get("luc")), gio(phieu.get("thoi_gian", "") + ("" if "+" in phieu.get("thoi_gian", "") else "+07:00"))
                    nhap_cu = bool(t_nk and t_ph and t_ph > t_nk)
                if nhap_cu:
                    viec.append("bản nháp WP %s là bản cũ nhưng bảng ghi đã cập nhật: xóa nhap_khop, đẩy lại nháp khi phiếu ĐẠT"
                                % r.get("draft_id"))
            elif r.get("draft_id") and khop and phieu.get("ket_luan") == "DAT":
                viec.append("phiếu ĐẠT nhưng bản nháp %s chưa cập nhật: đẩy lại nháp (DIEU_PHOI mục 3a)" % r.get("draft_id"))
            bv = bai_viet.get(rid)
            if bv and bv.get("sha") != sha and khop:
                viec.append("bài trên bảng (bai_viet) là bản cũ: chạy bai_len_bang.py rồi set bai_viet/%s" % rid)
            elif not bv and khop:
                viec.append("chưa có bai_viet/%s: chạy bai_len_bang.py rồi set" % rid)
        if viec:
            lech += 1
            print("- %s (%s, %s):" % (rid, fb, r.get("trang_thai")))
            for v in viec:
                print("    * " + v)
    for path in sorted(glob.glob(os.path.join(ROOT, "Bai_*.md"))):
        if os.path.basename(path) not in co_tren_bang:
            lech += 1
            print("- %s: có trên repo, không có dòng tu_khoa trên bảng. Nạp lên bảng (DIEU_PHOI mục 2) để duyệt và theo dõi"
                  % os.path.basename(path))
    print("Bảng khớp repo." if not lech else "%d bài cần cập nhật bảng." % lech)
    sys.exit(1 if lech else 0)


if __name__ == "__main__":
    main()
