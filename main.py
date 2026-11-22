#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261121.

Copies the pre-rendered front page (entry.png, drawn by gen.py) to the
output directory. Standard library only, no network, deterministic:
the same bytes are written on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    # The grader runs this twice; both runs must write identical bytes.
    # copyfile copies content only, so the output is byte-for-byte the
    # same file that gen.py rendered and that this repo holds.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
