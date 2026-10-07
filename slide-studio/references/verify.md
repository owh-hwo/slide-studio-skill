# Verify and export

## The loop (after every batch of edits)

```bash
S=~/.claude/skills/slide-studio/scripts
python $S/check_overflow.py "<Deck>.html"                 # deck: also checks the footer rule gap
python $S/check_overflow.py "<Deck> Handout.html"         # if there is a handout
python $S/render_slides.py "<Deck>.html" <tmp>/r [first last]
```

`check_overflow.py` reports three things: content clipped by the slide, an element clipping
itself, and content crossing or touching the footer rule (the `.take` strip is the usual
culprit; normal position is 16px above the rule). Exit code 1 = fix before moving on.

Then LOOK: `python $S/contact_sheet.py <tmp>/r` writes `<tmp>/r/sheet.png` (all slides as
thumbnails, 3 per row). Read it, then open single slides at full size for anything doubtful.

## Look checklist

- Title: at most two lines, no one-word orphan line, agrees with the body.
- Body: nothing clipped; no half-empty slide; table rows readable; numbers aligned right.
- Takeaway: present on every content slide, one line where possible.
- Kicker and chips: the right section is highlighted.
- Diagrams: text readable at slide size, labels off the lines, ≤ 2 accent elements.
- Footer: page numbers run 1..N; logos present on light and dark slides.
- Notes: present on every slide that needs explanation.

## Sizing

Sum `data-min` and compare with the slot in the brief:

```bash
python -c "import re,sys;s=open(sys.argv[1],encoding='utf-8').read();print(sum(map(int,re.findall(r'data-min=\"(\d+)\"',s))))" "<Deck>.html"
```

## Handout

Print to PDF and check the page count equals the number of `.page` sections:

```bash
"<chrome>" --headless=new --no-pdf-header-footer --print-to-pdf=out.pdf "<file:// URI>"
```

Build the URI with `pathlib.Path(f).resolve().as_uri()` (paths with spaces and Thai names).
Count with `pypdf`; look at pages with `pypdfium2` (`PdfDocument(p)[i].render(scale=1.2).to_pil()`).

## Export

```bash
python $S/build_pptx.py "<Deck>.html"     # PPTX next to the deck; one picture per slide + notes
```

The PDF from `render_slides.py` is one slide per page. Present from Chrome: S presenter window
(allow pop-ups), F fullscreen, O overview; Ctrl+P prints one slide per page.

## Known traps

- **Blank screenshots**: never screenshot `deck.html#/N`; the fade transition is caught
  half-way. The scripts use `?preview=N`, which shows one slide without transition.
- **PermissionError from build_pptx** = the .pptx is open in PowerPoint (a `~$` lock file
  shows it). Close it and re-run.
- **Fonts**: a Google font that fails to load falls back silently and changes line breaks;
  re-run the overflow check after any font change.
- **Thai in shell one-liners**: `python -c "..."` with Thai text can be mangled by the shell;
  write a script file or use a quoted heredoc, and set `PYTHONIOENCODING=utf-8` to print Thai.
- **Large heredocs** (over ~8 KB) can fail in some shells; write big files with the file tool.
- **Diagram colours** are baked into the SVG: after a theme change re-run `diagrams.py`.
- **Chrome not found**: set the `CHROME` environment variable to the browser binary.
