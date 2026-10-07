---
name: slide-studio
description: Build presentation decks as fixed 1920x1080 HTML slides in an executive "action title" style (kicker, a title that states the conclusion, one lead line, content, one takeaway strip, speaker notes), with selectable or custom brand themes, generated diagrams (the full diagram-design grammar is bundled), an optional A4 handout, and PNG / PDF / PPTX export. It starts by interviewing the user one question at a time (grill-me style, each question with a recommended answer) until theme, audience, storyline and content are settled, and only then builds. Use it for training courses and workshops, executive / board / steering-committee presentations, proposals and pre-sales pitches, and project status or go-live reports, and whenever the user asks for slides, a deck, a presentation, สไลด์, งานนำเสนอ, พรีเซนต์, เด็ค, เอกสารประกอบการอบรม or "ทำ PPT", even if they don't name the skill or mention HTML.
---

# Slide Studio

Decks that executives read in seconds and trainers can teach from: every slide makes one point,
states it in the title, proves it in the body and repeats it in one takeaway line. The same
layout works for four kinds of work (training, executive, proposal, status); only the theme
(colours, fonts, logos) and the storyline change.

What you produce, inside the user's project folder:

```
<project>/
  brief.md                  the interview result (theme, audience, storyline, rules)
  <Deck>.html               the deck: open in Chrome, S = presenter, F = fullscreen, O = overview
  <Deck> Handout.html       optional A4 landscape companion (same order as the deck)
  assets/                   runtime + studio.css (layout) + theme.css (colours, fonts, logos)
  diagrams/diagrams.py      this deck's diagrams (dg.py = primitives); run it to inject SVGs
  <Deck>.pptx / .pdf        exports (PPTX = one picture per slide + speaker notes)
```

Skill paths below are relative to this skill's folder (`~/.claude/skills/slide-studio`).
Run scripts with that full path; they work from any directory.

---

## The workflow: interview first, build second

Do the phases in order. The interview is the point of the skill: a deck built on guesses
gets rebuilt, and rebuilding 30 slides costs far more than ten questions.

### Phase 1 · Interview (grill until the brief is complete)

Read [`references/interview.md`](references/interview.md) now. It holds the decision tree.
The rules, in short:

- **Look before you ask.** If the answer is in the files, the codebase, a CLAUDE.md, an earlier
  deck or a connected system, read it instead of asking, and tell the user what you found.
- **One question per turn**, each with **your recommended answer and the reason** ("I suggest
  Navy & Amber because the audience is a board"). Use AskUserQuestion when the answer is a choice
  (2 to 4 options, recommended first, marked "(แนะนำ)" / "(Recommended)"); ask in plain text when
  it is open (key messages, the one decision you want). Ask in the user's language.
- **Walk the tree in dependency order**: work type → audience and goal → content and sources
  → storyline → theme → deliverables. Later answers depend on earlier ones (a board deck and a
  training deck get different defaults for length, notes and theme).
- **Show themes, don't describe them.** Open `assets/previews/index.html` in the user's browser
  (Windows `start "" "<path>"`, macOS `open`) so they see all presets. For a custom theme, write its
  JSON, run `scripts/preview_theme.py`, open the PNG for them, and iterate until they like it.
- **Stop when every branch is resolved**, or when the user says to go with the defaults (then
  list the defaults you applied). Write `brief.md` in the project (template in interview.md),
  show a short summary, and wait for an explicit go.

### Phase 2 · Storyline (the ghost deck)

Before any HTML, write the slide list into brief.md and show it as a table:
`# · section · action title · takeaway · pattern · minutes`. Read the titles top to bottom: they
must tell the whole story on their own. Use the skeleton for the work type in
`references/work-types/` (training, executive, proposal, status). Get approval; it is cheap to
reorder a table and expensive to reorder slides.

### Phase 3 · Scaffold and build

```bash
python scripts/new_deck.py "<project>" --theme <preset | path/to/theme.json> --name "<Deck>" \
  --title "..." --subtitle "..." --eyebrow "..." --footer "..." --lang th \
  --take-label "ประเด็นสำคัญ" --page-label "หน้า" [--handout] [--gallery]
```

Then write the slides. Copy markup from `assets/templates/gallery.html` (one working example of
every pattern) and pick patterns with [`references/components.md`](references/components.md).
Write titles, leads, takeaways and notes by [`references/writing.md`](references/writing.md).
Put deck-only CSS in the deck's `<style>`; never edit `assets/studio.css` or `theme.css` per deck
(re-run `new_deck.py` with another `--theme` to re-skin: content is kept).

Diagrams: read [`references/diagrams.md`](references/diagrams.md). Draw in
`diagrams/diagrams.py`, run it, never hand-edit SVG between `<!--DIAG:x-->` markers.

### Phase 4 · Verify (overflow is silent)

Slides are fixed-size with `overflow:hidden`: text that does not fit simply disappears. So:

```bash
python scripts/check_overflow.py "<Deck>.html"          # must say: no overflow, nothing near the footer rule
python scripts/render_slides.py "<Deck>.html" <tmp-dir>   # one PNG per slide + PDF
```

Then **look at every slide** (make a contact sheet of the PNGs and read it): one-word orphan
lines in titles, half-empty slides, crowded tables, unreadable diagram text. The checklist and
known traps are in [`references/verify.md`](references/verify.md). Sum `data-min` and compare
with the time slot from the brief.

### Phase 5 · Export and hand off

```bash
python scripts/build_pptx.py "<Deck>.html"   # needs python-pptx + Pillow; close the .pptx in PowerPoint first
```

The PPTX holds one 3840x2160 picture per slide plus the speaker notes (bold kept), so it shows
exactly like the HTML; text is edited in the HTML and re-exported. In the final message: where
the files are, slide count and minutes, how to present (Chrome: S, F, O), and in chat (never on
the slides) anything assumed rather than verified and any open questions.

---

## Rules that hold across every deck

- **One slide, one point.** The title states the conclusion as a sentence ("Testing is a week
  late; go-live is not at risk"), not a topic ("Testing status").
- **One takeaway strip per slide** (`.take`, label from the brief), pinned to the bottom.
  Covers and section dividers have none.
- **Facts are verified or labelled.** Numbers, names and examples come from the user's sources;
  anything illustrative is labelled as an example. Never invent client data.
- **The brief's content rules apply to notes too** (e.g. "no recommendations on slides",
  "never name the source system", "no em dashes").
- **The project's own conventions win.** If the project has a CLAUDE.md or an existing deck
  style, follow it and use this skill for the mechanics.

## Files in this skill

| Path | What it is |
|---|---|
| `references/interview.md` | Question tree, defaults per work type, brief.md template |
| `references/work-types/*.md` | Storyline skeletons: training, executive, proposal, status |
| `references/writing.md` | Titles, leads, takeaways, notes, language and number rules |
| `references/components.md` | Slide patterns, their classes and how much each holds |
| `references/themes.md` | Presets, token roles, building a custom theme, fonts, logos |
| `references/diagrams.md` | Diagrams in decks; bridges to the bundled diagram-design rules |
| `references/diagram/` | The full diagram-design skill: `DIAGRAM-DESIGN.md` + 42 type references |
| `references/verify.md` | Verify and export loop, look-checklist, known traps |
| `themes/*.json` | Five presets; copy one to start a custom theme |
| `assets/previews/` | Pre-rendered preset previews + `index.html` to show the user |
| `assets/templates/` | `gallery.html` (every pattern), `deck-shell.html`, `handout.html`, `diagrams.py` |
| `scripts/` | `new_deck`, `make_theme`, `preview_theme`, `dg`, `check_overflow`, `render_slides`, `build_pptx`; `diagram_self_check` is for standalone diagram pages only |

Licences: html-ppt runtime (MIT, `assets/runtime/html-ppt-LICENSE.txt`), diagram-design (MIT),
Sarabun font (OFL, `assets/fonts/OFL.txt`).
