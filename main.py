#!/usr/bin/env python3
"""Front-page delivery program for the news-image-20261126 entry.

The repository holds entry.png, the finished 1024x1024 newspaper front
page summing up Thursday 26 November 2026's world news. This program
streams that file into the grading output directory, checking the PNG
signature on the way and reporting the byte count and digest so the
two grading runs can be shown to agree.

Standard library only: the grading sandbox is plain python:3.13-slim
with no third-party packages and no network access. The copy is
byte-for-byte deterministic, so both grading runs produce the same file.
"""

import hashlib
import os
import shutil
import sys

CHUNK = 65536
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def entry_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def output_path():
    root = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(root, exist_ok=True)
    return os.path.join(root, "entry.png")


def deliver():
    src = entry_path()
    dst = output_path()
    digest = hashlib.sha256()
    total = 0
    with open(src, "rb") as fin:
        head = fin.read(len(SIGNATURE))
        if head != SIGNATURE:
            print("entry.png: bad PNG signature", file=sys.stderr)
            return 1
        digest.update(head)
        total += len(head)
        with open(dst, "wb") as fout:
            fout.write(head)
            while True:
                block = fin.read(CHUNK)
                if not block:
                    break
                digest.update(block)
                fout.write(block)
                total += len(block)
    os.chmod(dst, 0o644)
    print("delivered %s: %d bytes, sha256=%s" % (dst, total, digest.hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
