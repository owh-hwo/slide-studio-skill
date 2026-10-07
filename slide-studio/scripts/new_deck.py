"""Scaffold a new slide-studio deck folder (or add a deck to an existing one).

    python new_deck.py <project-dir> --theme navy-amber --name "Board Update Q3" \
        --title "..." [--subtitle ...] [--eyebrow ...] [--footer ...] [--lang th] \
        [--take-label ประเด็นสำคัญ] [--page-label หน้า] [--gallery]

Creates (never overwrites an existing deck file):
  <project>/<name>.html            the deck (shell with cover + one content slide, or the
                                   full pattern gallery with --gallery)
  <project>/assets/                html-ppt runtime + studio.css/js + theme.css/json + fonts + logos
  <project>/diagrams/dg.py         diagram primitives (theme-aware)
  <project>/diagrams/diagrams.py   this project's diagrams (starts with one sample)
  <project>/<name> Handout.html    with --handout: A4 landscape companion document
  <project>/brief.md               written by the interview (not by this script)

--theme takes a preset name (themes/*.json in the skill) or a path to a custom theme JSON.
Re-running with another --theme only regenerates assets/theme.css: decks keep their content.
"""
import argparse
import html
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import make_theme  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--theme", default="emerald-gold")
    ap.add_argument("--name", default="Deck")
    ap.add_argument("--title", default="Title that states the conclusion")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--footer", default="")
    ap.add_argument("--lang", default="th")
    ap.add_argument("--take-label", default="ประเด็นสำคัญ")
    ap.add_argument("--page-label", default="หน้า")
    ap.add_argument("--gallery", action="store_true", help="start from the full pattern gallery")
    ap.add_argument("--handout", action="store_true", help="also create '<name> Handout.html' (A4 landscape companion)")
    a = ap.parse_args()

    proj = Path(a.project).resolve()
    assets = proj / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for f in (SKILL / "assets" / "runtime").iterdir():
        shutil.copy(f, assets / f.name)
    for f in ("studio.css", "studio.js") + (("handout.css",) if a.handout else ()):
        shutil.copy(SKILL / "assets" / f, assets / f)
    make_theme.main(a.theme, assets)

    dg_dir = proj / "diagrams"
    dg_dir.mkdir(exist_ok=True)
    shutil.copy(HERE / "dg.py", dg_dir / "dg.py")
    if not (dg_dir / "diagrams.py").exists():
        shutil.copy(SKILL / "assets" / "templates" / "diagrams.py", dg_dir / "diagrams.py")

    if a.handout:
        ho = proj / f"{a.name} Handout.html"
        if not ho.exists():
            shutil.copy(SKILL / "assets" / "templates" / "handout.html", ho)
            print(f"created {ho}")

    deck = proj / f"{a.name}.html"
    if deck.exists():
        print(f"{deck.name} exists: kept as is (theme refreshed)")
        return
    theme = json.loads((assets / "theme.json").read_text(encoding="utf-8"))
    logos = theme.get("logos") or {}
    e = html.escape
    if a.gallery:
        src = (SKILL / "assets" / "templates" / "gallery.html").read_text(encoding="utf-8")
        src = src.replace("ประเด็นสำคัญ", a.take_label).replace('data-page-label="หน้า"', f'data-page-label="{e(a.page_label)}"')
    else:
        src = (SKILL / "assets" / "templates" / "deck-shell.html").read_text(encoding="utf-8")
        cover_logo = (f'<img class="logo" src="assets/logos/{Path(logos["main_dark"] or logos["main"]).name}" alt="">'
                      if (logos.get("main_dark") or logos.get("main")) else "")
        partner = logos.get("partner_dark") or logos.get("partner")
        cover_partner = f'<img src="assets/logos/{Path(partner).name}" alt="">' if partner else "<span></span>"
        for k, v in {"LANG": e(a.lang), "TITLE": e(a.title), "SUBTITLE": e(a.subtitle), "EYEBROW": e(a.eyebrow),
                     "FOOTER": e(a.footer), "TAKE_LABEL": e(a.take_label), "PAGE_LABEL": e(a.page_label),
                     "COVER_TITLE": "cover", "COVER_LOGO": cover_logo, "COVER_PARTNER": cover_partner}.items():
            src = src.replace("{{" + k + "}}", v)
    deck.write_text(src, encoding="utf-8")
    print(f"created {deck}")
    print(f"next: edit slides, then  python \"{HERE / 'check_overflow.py'}\" \"{deck}\"")


if __name__ == "__main__":
    main()
