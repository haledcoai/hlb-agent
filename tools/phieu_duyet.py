"""Phieu duyet bai viet: agent danh-gia-noi-dung ghi phieu, hook kiem tra phieu truoc khi dang ban nhap.

Cach dung:
  python tools/phieu_duyet.py ghi <file_bai.md> --diem 93 --diem-cho 2 --loi-bat-buoc 0 --vong 1 \
      --tieu-chi "intent=14,du_lieu=23,eeat=14,thuong_hieu=15,giong_van=13,cau_truc=14" \
      --van-de "tra-loi-nhanh-qua-dai|nen_sua|intent|Doan tra loi nhanh 66 tu"
  python tools/phieu_duyet.py bac-bo <file_bai.md> --vong 1 --nhan <nhan> --ly-do "..."
  python tools/phieu_duyet.py nhan        # cac nhan van de da dung, de dung lai cho thong nhat
  python tools/phieu_duyet.py xuat        # nhat ky -> .danh_gia/xuat/{cham,van_de,bac_bo,tieu_chi}.json cho trang theo doi
  python tools/phieu_duyet.py xem <file_bai.md>
  python tools/phieu_duyet.py hook        # PreToolUse hook, doc JSON tu stdin
  python tools/phieu_duyet.py da-sua      # PostToolUse hook (Edit|Write): ghi nhan file Bai_*.md vua sua
  python tools/phieu_duyet.py stop        # Stop hook: chua cho ket thuc luot khi bai vua sua chua duoc cham lai
  python tools/phieu_duyet.py bat-dau-cham  # PreToolUse hook (Agent|Task): danh dau dang co luot cham chay
  python tools/phieu_duyet.py xong-cham     # SubagentStop hook: bo danh dau khi sub agent danh gia ket thuc

Phieu luu o .danh_gia/<ten_file>.json, kem ma SHA-256 cua file bai luc cham.
Sua bai sau khi cham thi ma khong khop, phieu het hieu luc, phai cham lai.
Bai DAT khi: khong con loi bat buoc va (diem + diem tru vi cho nguoi dung quyet) >= NGUONG.
Hook chan "wp_draft.py ... --post" khi chua co phieu DAT khop noi dung hoac script kiem tra con LOI.
Hook chan "phieu_duyet.py ghi" khi lenh khong do sub agent danh-gia-noi-dung chay (xem chi_agent_danh_gia_ghi).
Khi dang co luot cham chay (ke ca chay nen), Stop hook khong nhac cham lai.

Nhat ky: moi lan "ghi" va "bac-bo" them mot dong vao .danh_gia/nhat_ky.jsonl (khong ghi de),
lam du lieu cho trang theo doi lich su danh gia va de hoan thien thang cham.
Doi thang cham (tieu chi, diem, nguong) thi tang THANG_CHAM de diem cu va moi khong bi so lan.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

NGUONG = 95
THANG_CHAM = "v2"  # v1: nguong 80 (21/10/2026), v2: nguong 95, diem cho nguoi dung
MAX_NHAC = 3  # so lan Stop hook chan toi da cho mot file, tranh vong lap khi khong cham duoc
AGENT_DANH_GIA = "danh-gia-noi-dung"
AGENT_DU_PHONG = "general-purpose"  # dung khi phien khong nap duoc .claude/agents (CLAUDE.md)
HAN_DANG_CHAM = 30 * 60  # giay; danh dau "dang cham" qua han nay coi nhu luot cham da hong, Stop hook nhac lai
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHIEU_DIR = os.path.join(ROOT, ".danh_gia")
CAN_CHAM = os.path.join(PHIEU_DIR, "_can_cham.json")
NHAT_KY = os.path.join(PHIEU_DIR, "nhat_ky.jsonl")
DANG_CHAM = os.path.join(PHIEU_DIR, "_dang_cham.json")

# Tieu chi cua thang cham trong .claude/agents/danh-gia-noi-dung.md: ma -> (ten, diem toi da)
TIEU_CHI = {
    "intent": ("Đáp ứng search intent", 15),
    "du_lieu": ("Chính xác dữ liệu và nguồn", 25),
    "eeat": ("Chuyên môn và EEAT", 15),
    "thuong_hieu": ("Thương hiệu và tuân thủ", 15),
    "giong_van": ("Giọng văn", 15),
    "cau_truc": ("Cấu trúc và SEO", 15),
}
MUC = ("bat_buoc", "nen_sua", "cho_nguoi_dung")
KET_LUAN = {"DAT": "Đạt", "CAN_SUA": "Cần sửa", "KHONG_DAT": "Không đạt"}
BAI = re.compile(r"(^|[\\/])Bai_[^\\/]*\.md$")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def phieu_path(article):
    return os.path.join(PHIEU_DIR, os.path.splitext(os.path.basename(article))[0] + ".json")


def them_nhat_ky(dong):
    os.makedirs(PHIEU_DIR, exist_ok=True)
    with open(NHAT_KY, "a", encoding="utf-8") as f:
        f.write(json.dumps(dong, ensure_ascii=False) + "\n")


def doc_nhat_ky():
    try:
        with open(NHAT_KY, encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
    except OSError:
        return []


def doc_tieu_chi(text):
    """"intent=14,du_lieu=23,..." -> dict. Bao loi khi sai ma hoac vuot diem toi da."""
    diem = {}
    for part in filter(None, (p.strip() for p in (text or "").split(","))):
        key, _, val = part.partition("=")
        key = key.strip()
        if key not in TIEU_CHI:
            sys.exit("Mã tiêu chí '%s' không có. Dùng: %s" % (key, ", ".join(TIEU_CHI)))
        diem[key] = int(val)
        if not 0 <= diem[key] <= TIEU_CHI[key][1]:
            sys.exit("Điểm %s = %d vượt khoảng 0-%d" % (key, diem[key], TIEU_CHI[key][1]))
    return diem


def doc_van_de(items):
    """"nhan|muc|tieu_chi|mo ta" -> dict."""
    out = []
    for raw in items or []:
        parts = [p.strip() for p in raw.split("|", 3)]
        if len(parts) < 4 or parts[1] not in MUC or parts[2] not in TIEU_CHI:
            sys.exit("--van-de sai dạng: '%s'. Cần \"nhan|%s|<mã tiêu chí>|mô tả\"" % (raw, "/".join(MUC)))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", parts[0]):
            sys.exit("Nhãn '%s' phải không dấu, chữ thường, nối bằng hyphen" % parts[0])
        out.append({"nhan": parts[0], "muc": parts[1], "tieu_chi": parts[2], "mo_ta": parts[3]})
    return out


def ghi(args):
    if not os.path.isfile(args.article):
        sys.exit("Không thấy file bài: %s" % args.article)
    tieu_chi = doc_tieu_chi(args.tieu_chi)
    van_de = doc_van_de(args.van_de)
    diem_tinh = min(100, args.diem + args.diem_cho)
    dat = args.loi_bat_buoc == 0 and diem_tinh >= NGUONG
    phieu = {
        "file": os.path.basename(args.article),
        "sha256": sha256(args.article),
        "diem": args.diem,
        "diem_cho_nguoi_dung": args.diem_cho,
        "diem_tinh": diem_tinh,
        "loi_bat_buoc": args.loi_bat_buoc,
        "nguong": NGUONG,
        "ket_luan": "DAT" if dat else "CAN_SUA",
        "vong": args.vong,
        "thoi_gian": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    os.makedirs(PHIEU_DIR, exist_ok=True)
    with open(phieu_path(args.article), "w", encoding="utf-8") as f:
        json.dump(phieu, f, ensure_ascii=False, indent=2)
    them_nhat_ky(dict(phieu, loai="cham", thang_cham=THANG_CHAM, tieu_chi=tieu_chi, van_de=van_de))
    luu_dang_cham({})  # cham xong, Stop hook duoc nhac lai neu bai bi sua tiep
    print("Đã ghi phiếu: %s (và một dòng nhật ký)" % phieu_path(args.article))
    print("Kết luận: %s (điểm %d/100, điểm tính ngưỡng %d/100, cần từ %d; lỗi bắt buộc %d; vòng %d)"
          % (phieu["ket_luan"], args.diem, diem_tinh, NGUONG, args.loi_bat_buoc, args.vong))
    if tieu_chi and len(tieu_chi) == len(TIEU_CHI) and sum(tieu_chi.values()) != args.diem:
        print("Cảnh báo: tổng điểm tiêu chí %d khác --diem %d" % (sum(tieu_chi.values()), args.diem))
    if not tieu_chi:
        print("Cảnh báo: thiếu --tieu-chi, trang theo dõi sẽ không có điểm từng tiêu chí cho lần chấm này")


def bac_bo(args):
    """Agent chinh ghi lai mot nhan dinh cua agent danh gia ma doi chieu nguon thay sai."""
    them_nhat_ky({
        "loai": "bac_bo",
        "file": os.path.basename(args.article),
        "vong": args.vong,
        "nhan": args.nhan,
        "ly_do": args.ly_do,
        "thang_cham": THANG_CHAM,
        "thoi_gian": datetime.datetime.now().isoformat(timespec="seconds"),
    })
    print("Đã ghi nhật ký: bác bỏ '%s' ở vòng %d của %s" % (args.nhan, args.vong, os.path.basename(args.article)))


def xuat(args):
    """Tach nhat ky thanh 3 file JSON (mang dong) cho trang theo doi: cham, van_de, bac_bo."""
    cham, van_de, bac_bo = [], [], []
    for i, d in enumerate(doc_nhat_ky(), 1):
        if d.get("loai") == "cham":
            ma = "L%03d" % i
            tc = d.get("tieu_chi") or {}
            cham.append({
                "ma": ma, "bai": d["file"].replace("Bai_", "").replace(".md", ""), "vong": d.get("vong"),
                "ngay": (d.get("thoi_gian") or "")[:10], "thang_cham": d.get("thang_cham", "v1"),
                "nguong": d.get("nguong"), "diem": d.get("diem"), "diem_tinh": d.get("diem_tinh"),
                "loi_bat_buoc": d.get("loi_bat_buoc"), "ket_luan": d.get("ket_luan"),
                "ket_luan_ten": KET_LUAN.get(d.get("ket_luan"), d.get("ket_luan")),
                **{k: tc.get(k) for k in TIEU_CHI},
            })
            for v in d.get("van_de", []):
                van_de.append(dict(v, ma=ma, bai=cham[-1]["bai"], vong=d.get("vong"),
                                   ten_tieu_chi=TIEU_CHI[v["tieu_chi"]][0]))
        elif d.get("loai") == "bac_bo":
            bac_bo.append({"ma": "B%03d" % i, "bai": d["file"].replace("Bai_", "").replace(".md", ""), "vong": d.get("vong"),
                           "nhan": d.get("nhan"), "ly_do": d.get("ly_do"),
                           "ngay": (d.get("thoi_gian") or "")[:10]})
    tieu_chi = [{"ma": k, "ten": ten, "toi_da": toi_da} for k, (ten, toi_da) in TIEU_CHI.items()]
    os.makedirs(args.thu_muc, exist_ok=True)
    for ten, rows in (("cham", cham), ("van_de", van_de), ("bac_bo", bac_bo), ("tieu_chi", tieu_chi)):
        with open(os.path.join(args.thu_muc, ten + ".json"), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
    print("Đã xuất vào %s: cham.json (%d lần chấm), van_de.json (%d vấn đề), bac_bo.json (%d lần bác bỏ)"
          % (args.thu_muc, len(cham), len(van_de), len(bac_bo)))


def nhan(_args):
    dem = {}
    for d in doc_nhat_ky():
        for v in d.get("van_de", []):
            k = (v["nhan"], v["tieu_chi"])
            dem[k] = dem.get(k, 0) + 1
    if not dem:
        print("Chưa có nhãn nào trong nhật ký.")
        return
    print("Nhãn vấn đề đã dùng (dùng lại đúng nhãn khi gặp lại cùng loại vấn đề):")
    for (n, tc), c in sorted(dem.items(), key=lambda x: -x[1]):
        print("- %s (%s): %d lần" % (n, tc, c))


def kiem(article):
    """Tra ve danh sach ly do chua duoc dang. Rong = duoc dang."""
    if not os.path.isfile(article):
        return ["Không thấy file bài %s" % article]
    path = phieu_path(article)
    if not os.path.isfile(path):
        return ["Chưa có phiếu duyệt cho %s. Gọi agent danh-gia-noi-dung chấm bài trước." % os.path.basename(article)]
    with open(path, encoding="utf-8") as f:
        phieu = json.load(f)
    reasons = []
    if phieu.get("sha256") != sha256(article):
        reasons.append("File bài đã bị sửa sau lần chấm lúc %s, phiếu hết hiệu lực. Chấm lại." % phieu.get("thoi_gian"))
    if phieu.get("ket_luan") != "DAT" or phieu.get("diem_tinh", 0) < NGUONG or phieu.get("loi_bat_buoc", 1):
        reasons.append("Phiếu chưa ĐẠT: điểm tính ngưỡng %s/100, cần từ %d; lỗi bắt buộc %s."
                       % (phieu.get("diem_tinh"), NGUONG, phieu.get("loi_bat_buoc")))
    check = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "kiem_tra_bai.py"), article],
                           capture_output=True, text=True, encoding="utf-8")
    if check.returncode != 0:
        reasons.append("tools/kiem_tra_bai.py còn LỖI (mã thoát %d)." % check.returncode)
    return reasons


def xem(args):
    reasons = kiem(args.article)
    if reasons:
        print("CHƯA ĐƯỢC ĐĂNG:")
        for r in reasons:
            print("- " + r)
        sys.exit(1)
    print("Được đăng bản nháp: phiếu ĐẠT và khớp nội dung hiện tại.")


def hook(_args):
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except ValueError:
        return
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if re.search(r"phieu_duyet\.py[\"']?\s+ghi(\s|$)", cmd):
        chi_agent_danh_gia_ghi(data)
        return
    if not re.search(r"wp_draft\.py", cmd) or not re.search(r"(^|\s)--post(\s|$)", cmd):
        return
    m = re.search(r"wp_draft\.py[\"']?\s+(\"[^\"]+\.md\"|'[^']+\.md'|\S+\.md)", cmd)
    if not m:
        print("Hook phiếu duyệt: không đọc được file bài trong lệnh wp_draft.py --post, chặn để an toàn.", file=sys.stderr)
        sys.exit(2)
    article = m.group(1).strip("\"'")
    if not os.path.isabs(article):
        article = os.path.join(data.get("cwd") or ROOT, article)
    reasons = kiem(article)
    if reasons:
        print("Chặn đăng bản nháp (cần phiếu duyệt từ %d điểm, khớp nội dung bài):" % NGUONG, file=sys.stderr)
        for r in reasons:
            print("- " + r, file=sys.stderr)
        print("Làm theo vòng duyệt trong CLAUDE.md. Không tự ghi phiếu thay agent đánh giá.", file=sys.stderr)
        sys.exit(2)


def chi_agent_danh_gia_ghi(data):
    """Chi sub agent danh-gia-noi-dung duoc ghi phieu.

    Ban Claude Code moi gui agent_type trong du lieu hook khi lenh chay trong sub agent: dung no.
    Ban cu khong gui truong nay: cho ghi khi dang co luot cham chay (danh dau boi bat-dau-cham).
    """
    agent = data.get("agent_type")
    if agent == AGENT_DANH_GIA:
        return
    # Phien khong nap duoc .claude/agents thi agent general-purpose doc file agent danh gia de cham (CLAUDE.md):
    # cho ghi khi bat-dau-cham da danh dau luot cham do
    if agent in (None, AGENT_DU_PHONG) and dang_cham():
        return
    print("Chặn ghi phiếu duyệt: chỉ sub agent %s được chạy 'phieu_duyet.py ghi' sau khi chấm. "
          "Gọi agent đánh giá chấm bài. Muốn đăng khi bài chưa đạt thì người dùng tự chạy lệnh trong terminal."
          % AGENT_DANH_GIA, file=sys.stderr)
    sys.exit(2)


# ---------- Danh dau dang cham (PreToolUse Agent|Task + SubagentStop) ----------

def doc_dang_cham():
    try:
        with open(DANG_CHAM, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def luu_dang_cham(state):
    os.makedirs(PHIEU_DIR, exist_ok=True)
    with open(DANG_CHAM, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def dang_cham():
    """Co luot cham bat dau chua qua HAN_DANG_CHAM giay khong (o bat ky phien nao)."""
    now = datetime.datetime.now().timestamp()
    return any(now - t < HAN_DANG_CHAM for t in doc_dang_cham().values())


def la_luot_cham(tool_input):
    """Loi goi Agent nay la luot cham: dung agent danh gia, hoac agent du phong duoc yeu cau doc file agent danh gia."""
    kieu = tool_input.get("subagent_type")
    if kieu == AGENT_DANH_GIA:
        return True
    return kieu in (None, "", AGENT_DU_PHONG) and AGENT_DANH_GIA in (tool_input.get("prompt") or "")


def bat_dau_cham(_args):
    data = doc_stdin()
    if not la_luot_cham(data.get("tool_input") or {}):
        return
    state = doc_dang_cham()
    state[data.get("session_id") or "khong-ro"] = datetime.datetime.now().timestamp()
    luu_dang_cham(state)


def xong_cham(_args):
    data = doc_stdin()
    if data.get("agent_type") not in (None, AGENT_DANH_GIA, AGENT_DU_PHONG):
        return  # sub agent khac (vi du tao-anh) ket thuc, luot cham van dang chay
    state = doc_dang_cham()
    if state.pop(data.get("session_id") or "khong-ro", None) is not None:
        luu_dang_cham(state)


# ---------- Nhac cham lai sau khi sua bai (PostToolUse + Stop) ----------

def doc_stdin():
    try:
        return json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except ValueError:
        return {}


def doc_can_cham():
    try:
        with open(CAN_CHAM, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def luu_can_cham(state):
    os.makedirs(PHIEU_DIR, exist_ok=True)
    with open(CAN_CHAM, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def phieu_khop(article):
    """Da cham sau lan sua cuoi: co phieu va ma noi dung khop (khong xet diem)."""
    try:
        with open(phieu_path(article), encoding="utf-8") as f:
            return json.load(f).get("sha256") == sha256(article)
    except (OSError, ValueError):
        return False


def da_sua(_args):
    data = doc_stdin()
    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not BAI.search(path):
        return
    if not os.path.isabs(path):
        path = os.path.join(data.get("cwd") or ROOT, path)
    state = doc_can_cham()
    files = state.setdefault(data.get("session_id") or "khong-ro", {})
    files[os.path.normpath(path)] = 0
    luu_can_cham(state)


def stop(_args):
    data = doc_stdin()
    sid = data.get("session_id") or "khong-ro"
    if dang_cham():
        return  # luot cham dang chay (thuong la chay nen), khi xong phien duoc goi lai va Stop hook chay lai
    state = doc_can_cham()
    files = state.get(sid, {})
    chua, bo_qua = [], []
    for path in list(files):
        if not os.path.isfile(path) or phieu_khop(path):
            del files[path]
        elif files[path] >= MAX_NHAC:
            bo_qua.append(os.path.basename(path))
            del files[path]
        else:
            files[path] += 1
            chua.append(os.path.basename(path))
    if files:
        state[sid] = files
    else:
        state.pop(sid, None)
    luu_can_cham(state)
    if chua:
        print(json.dumps({
            "decision": "block",
            "reason": "Bài vừa sửa chưa được chấm lại (chưa có phiếu duyệt khớp nội dung): %s. "
                      "Chạy vòng duyệt trong CLAUDE.md: gọi agent danh-gia-noi-dung (agent ghi phiếu), "
                      "chưa đạt 95 thì tự sửa và chấm lại, tối đa 3 vòng, rồi mới kết thúc lượt. "
                      "Nếu người dùng chỉ hỏi chuyện khác, vẫn chấm lại bài vừa sửa trước." % ", ".join(chua),
        }, ensure_ascii=False))
    elif bo_qua:
        print(json.dumps({
            "systemMessage": "Đã nhắc %d lần nhưng bài chưa được chấm lại: %s. Bài này sẽ không đăng được cho tới khi có phiếu ĐẠT."
                             % (MAX_NHAC, ", ".join(bo_qua)),
        }, ensure_ascii=False))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("ghi", help="ghi phieu sau khi cham")
    g.add_argument("article")
    g.add_argument("--diem", type=int, required=True, help="tong diem /100")
    g.add_argument("--diem-cho", type=int, default=0, help="diem bi tru chi vi diem cho nguoi dung quyet")
    g.add_argument("--loi-bat-buoc", type=int, required=True)
    g.add_argument("--vong", type=int, default=1)
    g.add_argument("--tieu-chi", help="diem tung tieu chi: %s" % ",".join("%s=x" % k for k in TIEU_CHI))
    g.add_argument("--van-de", action="append", help="nhan|muc|tieu_chi|mo ta, lap lai cho moi van de")
    g.set_defaults(func=ghi)
    b = sub.add_parser("bac-bo", help="ghi nhan dinh sai cua agent danh gia")
    b.add_argument("article")
    b.add_argument("--vong", type=int, required=True)
    b.add_argument("--nhan", required=True)
    b.add_argument("--ly-do", required=True)
    b.set_defaults(func=bac_bo)
    sub.add_parser("nhan", help="liet ke nhan van de da dung").set_defaults(func=nhan)
    e = sub.add_parser("xuat", help="xuat nhat ky thanh file JSON cho trang theo doi")
    e.add_argument("--thu-muc", default=os.path.join(PHIEU_DIR, "xuat"))
    e.set_defaults(func=xuat)
    x = sub.add_parser("xem", help="kiem tra bai co duoc dang khong")
    x.add_argument("article")
    x.set_defaults(func=xem)
    h = sub.add_parser("hook", help="PreToolUse hook")
    h.set_defaults(func=hook)
    sub.add_parser("da-sua", help="PostToolUse hook").set_defaults(func=da_sua)
    sub.add_parser("stop", help="Stop hook").set_defaults(func=stop)
    sub.add_parser("bat-dau-cham", help="PreToolUse hook (Agent|Task)").set_defaults(func=bat_dau_cham)
    sub.add_parser("xong-cham", help="SubagentStop hook").set_defaults(func=xong_cham)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
