"""Render a deck to one PNG per slide plus a PDF, so you can LOOK at every slide.

    python render_slides.py "<deck>.html" <out-dir> [first last]

PNG i is the deck opened at ?preview=i (one slide, no transition) in a 1920x1080 headless
window. Never screenshot #/N: the slide fade gets caught half-way and comes out blank.
The PDF is the deck printed (one slide per page) and lands next to the PNGs.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import CHROME  # noqa: E402


def run(args):
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", *args], capture_output=True, timeout=180)


def main(deck, out, first=None, last=None):
    deck, out = Path(deck).resolve(), Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    n = len(re.findall(r'<section class="slide\b', deck.read_text(encoding="utf-8")))
    first, last = int(first or 1), int(last or n)
    for i in range(first, last + 1):
        run(["--window-size=1920,1080", "--virtual-time-budget=4000",
             f"--screenshot={out / f'slide-{i:02d}.png'}", deck.as_uri() + f"?preview={i}"])
    pdf = out / (deck.stem + ".pdf")
    run(["--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", deck.as_uri()])
    try:
        import pypdf
        pages = len(pypdf.PdfReader(str(pdf)).pages)
    except Exception as e:
        pages = f"? ({e})"
    print(f"{deck.name}: {n} slides, rendered {first}-{last} to {out}, PDF pages {pages}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
