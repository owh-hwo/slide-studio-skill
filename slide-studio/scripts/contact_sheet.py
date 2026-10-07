"""Put every rendered slide on one image so you can look at the whole deck at once.

    python contact_sheet.py <dir-with-slide-NN.png> [out.png] [--cols 3]

Writes <dir>/sheet.png by default (640x360 thumbnails). Read the sheet, then open single
slides at full size for anything doubtful.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--cols", type=int, default=3)
    a = ap.parse_args()
    d = Path(a.dir)
    fs = sorted(d.glob("slide-*.png"))
    if not fs:
        raise SystemExit(f"no slide-*.png in {d}")
    w, h, pad, cols = 640, 360, 10, a.cols
    rows = (len(fs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols + 1) * pad, rows * h + (rows + 1) * pad), "#8A8F96")
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(fs):
        x, y = pad + (i % cols) * (w + pad), pad + (i // cols) * (h + pad)
        sheet.paste(Image.open(f).convert("RGB").resize((w, h)), (x, y))
        draw.rectangle([x, y, x + 34, y + 22], fill="#000000")
        draw.text((x + 6, y + 5), str(i + 1), fill="#FFFFFF")
    out = Path(a.out) if a.out else d / "sheet.png"
    sheet.save(out)
    print(f"{len(fs)} slides -> {out}")


if __name__ == "__main__":
    main()
