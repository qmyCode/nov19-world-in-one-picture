#!/usr/bin/env python3
"""Entry point for the news-image-20261119 entry.

Renders the front page with draw.py and writes it to entry.png next to
this file and to /output/entry.png (the path the grader reads).
"""

import os
import shutil

import draw


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(here, "entry.png")
    draw.render(local)
    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(local, os.path.join(out_dir, "entry.png"))
    except OSError:
        pass
    print("wrote", local)


if __name__ == "__main__":
    main()
