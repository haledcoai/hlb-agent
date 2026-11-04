"""Thu xem phien co nap hook trong .claude/settings.json khong (bai thu 04/11/2026).

Cach dung:
  python tools/kiem_hook.py ghi   # SessionStart hook: ghi dau .danh_gia/_hook_da_chay.json
  python tools/kiem_hook.py xem   # in mot cau ket qua de ghi len Bang dieu phoi

File dau nam trong .gitignore, nen phien cloud clone repo moi chi co file nay khi hook that su chay.
Co file dau la phien da nap .claude/settings.json, tuc ca 5 hook cua phieu_duyet.py cung chay.
"""
import datetime
import json
import os
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAU = ROOT / ".danh_gia" / "_hook_da_chay.json"


def gio_vn():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(timespec="seconds")


def ghi(_args):
    try:
        vao = json.load(sys.stdin)
    except Exception:
        vao = {}
    DAU.parent.mkdir(exist_ok=True)
    DAU.write_text(json.dumps({
        "luc": gio_vn(),
        "may": platform.node(),
        "he_dieu_hanh": platform.system(),
        "nguon": vao.get("source"),
        "claude_code_remote": os.environ.get("CLAUDE_CODE_REMOTE"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Hook SessionStart da chay (kiem_hook.py): phien nay co nap .claude/settings.json.")


def xem(_args):
    if not DAU.exists():
        print("Hook KHONG chay: chua co %s, phien nay khong nap .claude/settings.json." % DAU.relative_to(ROOT).as_posix())
        return
    d = json.loads(DAU.read_text(encoding="utf-8"))
    print("Hook CO chay: SessionStart ghi dau luc %s, may %s (%s), CLAUDE_CODE_REMOTE=%s."
          % (d.get("luc"), d.get("may"), d.get("he_dieu_hanh"), d.get("claude_code_remote")))


def main():
    lenh = {"ghi": ghi, "xem": xem}
    if len(sys.argv) < 2 or sys.argv[1] not in lenh:
        sys.exit(__doc__)
    lenh[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
