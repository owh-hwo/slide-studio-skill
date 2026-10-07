"""Render a theme as one preview image (cover + status table + diagram slide), for choosing a theme.

    python preview_theme.py <preset-name | theme.json> <out.png>
    python preview_theme.py --all <out-dir>          # every preset in themes/, plus index.html

Use it in the interview: show the presets (assets/previews/ holds pre-rendered ones), and
after the user describes a custom theme, write its JSON and preview it before building.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SLIDES = (1, 5, 7)  # cover, RAG table, diagram in the gallery


def preview(theme, out):
    out = Path(out)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        subprocess.run([sys.executable, str(HERE / "new_deck.py"), str(tmp), "--theme", str(theme),
                        "--name", "g", "--gallery"], check=True, capture_output=True)
        subprocess.run([sys.executable, "diagrams.py"], cwd=tmp / "diagrams", check=True, capture_output=True)
        r = tmp / "r"
        for i in SLIDES:
            subprocess.run([sys.executable, str(HERE / "render_slides.py"), str(tmp / "g.html"), str(r), str(i), str(i)],
                           check=True, capture_output=True)
        ims = [Image.open(r / f"slide-{i:02d}.png").convert("RGB").resize((960, 540)) for i in SLIDES]
        sheet = Image.new("RGB", (len(ims) * 960 + (len(ims) + 1) * 12, 564), "#9AA0A6")
        for k, im in enumerate(ims):
            sheet.paste(im, (12 + k * 972, 12))
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out)
    print(f"preview -> {out}")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    if sys.argv[1] == "--all":
        import json
        outdir = Path(sys.argv[2])
        rows = []
        for t in sorted((SKILL / "themes").glob("*.json")):
            preview(t.stem, outdir / f"{t.stem}.png")
            meta = json.loads(t.read_text(encoding="utf-8"))
            rows.append(f'<h2>{meta["label"]} <small>({t.stem})</small></h2><p>{meta["mood"]} · เหมาะกับ {meta["fit"]}</p>'
                        f'<img src="{t.stem}.png">')
        (outdir / "index.html").write_text(
            '<!doctype html><meta charset="utf-8"><title>slide-studio themes</title>'
            '<style>body{font-family:Sarabun,Tahoma,sans-serif;background:#eee;margin:24px}img{width:100%;max-width:1500px;'
            'display:block;margin-bottom:28px;box-shadow:0 2px 10px rgba(0,0,0,.2)}small{color:#777}</style>'
            + "".join(rows), encoding="utf-8")
        print(f"index -> {outdir / 'index.html'}")
    else:
        preview(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
