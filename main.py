#!/usr/bin/env python3
"""Entry for news-image-20261117: copy the front-page image to the output.

Standard library only. No network, no timestamps, no randomness: every run
writes the same bytes.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    # The variable names a directory in some harnesses: accept either form.
    if out.endswith(os.sep) or os.path.isdir(out):
        out = os.path.join(out, "entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    shutil.copyfile(SOURCE, out)
    # Verify the copy is byte-identical to the shipped image.
    if sha256(out) != sha256(SOURCE):
        print("error: copied entry.png does not match the source", file=sys.stderr)
        return 1
    print("wrote", out, os.path.getsize(out), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
