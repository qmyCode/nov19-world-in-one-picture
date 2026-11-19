#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 entry (v4).

The picture itself is committed next to this file as ``entry.png``.
At run time this program only has to deliver that picture: it checks
the file really is a PNG and no larger than the 1 MiB the competition
allows, then copies it, byte for byte, to ``/output/entry.png``.

Standard library only. The drawing program (``draw.py``) is a build
tool and is never imported or run here.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = os.path.join("/output", "entry.png")
MAX_BYTES = 1024 * 1024  # 1 MiB cap from the competition rules
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"missing entry picture: {SOURCE}", file=sys.stderr)
        return 1

    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1

    with open(SOURCE, "rb") as fh:
        head = fh.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        print("entry.png does not start with a PNG signature", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print(f"entry.png delivered: {size} bytes -> {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
