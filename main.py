#!/usr/bin/env python3
"""Copy the pre-rendered entry.png into MAKEFUN_OUTPUT_DIR.

Stdlib only (os / shutil / hashlib): the grader runs with no third-party
packages installed, so this file must never import PIL, numpy or anything
else. The image itself is rendered at build time by gen.py (PIL) and
committed to this repo as entry.png; this script only copies it.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1024 * 1024


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("entry.png too big: %d bytes > 1 MiB" % size, file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        magic = f.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    if sha256_of(dst) != sha256_of(src):
        print("copy hash mismatch", file=sys.stderr)
        return 1
    print("copied entry.png (%d bytes, sha256 %s) to %s"
          % (size, sha256_of(dst)[:12], dst))
    print("entry is deterministic: re-running gen.py reproduces this file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
