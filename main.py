#!/usr/bin/env python3
"""Entry program: copy the front-page image to /output/entry.png.

Standard library only. The image is drawn at build time and shipped in
the repository (assets/entry.png); this program copies it byte for byte,
so two runs always write identical bytes. It verifies the PNG header,
its dimensions (at most 1024x1024) and its size (at most 1 MiB).
"""
import os
import shutil
import struct


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, out)
    with open(out, "rb") as f:
        head = f.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    width, height = struct.unpack(">II", head[16:24])
    assert width <= 1024 and height <= 1024, f"image too big: {width}x{height}"
    size = os.path.getsize(out)
    assert size <= 1048576, f"image over 1 MiB: {size} bytes"
    print(f"wrote {out} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()
