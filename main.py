#!/usr/bin/env python3
"""main.py - entrypoint for the 19 November 2026 news-image entry (v5).

Stdlib-only copier: validates the committed entry.png (PNG signature,
size <= 1 MiB) and copies it to /output/entry.png. draw.py is the build
tool that produced entry.png; it is never imported here.
"""
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # 1 MiB


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_SIGNATURE):
        print("entry.png: bad PNG signature", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png: exceeds 1 MiB cap", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    if os.path.getsize(dst) != len(data):
        print("entry.png: copy size mismatch", file=sys.stderr)
        return 1
    print("entry.png delivered: %d bytes -> %s" % (len(data), dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
