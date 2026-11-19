#!/usr/bin/env python3
"""Entry point for the news-image-20261119 v3 entry.

The front page is committed in this repository as entry.png; it was
drawn ahead of time by draw.py, a build tool that is not run here.
This program delivers that committed image to /output/entry.png,
byte for byte, after checking it carries a PNG or JPEG signature and
fits within 1 MiB. Standard library only; no network; deterministic.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
DEST = os.path.join(OUT_DIR, "entry.png")
LIMIT = 1024 * 1024
PNG_HEAD = b"\x89PNG\r\n\x1a\n"
JPEG_HEAD = b"\xff\xd8\xff"


def deliver() -> int:
    if not os.path.isfile(SOURCE):
        print("committed entry.png not found", file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    if size == 0 or size > LIMIT:
        print(f"entry.png size {size} outside 1..{LIMIT}", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as fh:
        head = fh.read(len(PNG_HEAD))
    if head != PNG_HEAD and not head.startswith(JPEG_HEAD):
        print("entry.png has no PNG/JPEG signature", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    if os.path.getsize(DEST) != size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    print(f"entry.png delivered: {size} bytes -> {DEST}")
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
