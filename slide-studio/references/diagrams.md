# Diagrams in decks

The whole diagram-design skill is bundled in `references/diagram/` (`DIAGRAM-DESIGN.md` is its
original SKILL.md; 42 `type-*.md` layout references; primitives, semantic patterns, layout
budget). In a deck you use its **judgement and grammar**, drawn with this skill's `dg.py` in
the deck's theme. Its style-guide gate and onboarding do not apply: the deck theme is the
style guide.

## When to draw

Ask diagram-design's question: would the reader learn more from this than from a sentence
or a 3-column table? If a table says it, use the table. Good deck diagrams: architecture and
integration, process and handoffs, before / after, data flow, hierarchy, timelines.

## Choosing the type

1. Open `references/diagram/DIAGRAM-DESIGN.md` §3 and pick the visual type (and the semantic
   pattern if behaviour carries the meaning).
2. Read that `type-*.md` for its layout grammar, and `layout-budget.md` for the complexity
   budget. Skip their HTML-template and export sections; `dg.py` replaces them.
3. State the plan in one line to the user when the diagram is central to the deck.

## Drawing with dg.py

`diagrams/diagrams.py` in the project (from the template) loads the theme and defines one
function per diagram:

```python
def d_flow():
    d = D("flow", 1032, 300, "short title", "one-sentence description for screen readers")
    d.zone(0, 10, 420, 280, "สาขา")                       # boundaries first
    d.arrow(H(200, 150, 252), "muted")                   # connectors before nodes
    d.label(226, 150, "ทุกคืน", "above")                 # masked label, 8px off the line
    d.node(0, 112, 200, 76, "ระบบ HIS", "ส่งรายการขาย", "input")
    d.node(252, 100, 192, 100, "ERP", "ฐานข้อมูลเดียว", "focal", tag="ERP")
    return d.render()

DIAGRAMS = {"flow": d_flow}
```

- Canvas: width 1032 (viewBox units); height to fit. In the slide `.dgwrap` scales it to the
  free body height (about 1.6x), so 13-unit text shows at about 21px. Keep text ≥ 10 units.
- Node kinds (theme-mapped): `backend` default, `focal` the one thing the slide is about
  (max 2), `store`, `external`, `input`, `link` (integration), `dark` (end result),
  `optional` (dashed: future / manual / not built).
- Connectors: `H`, `V`, `hv`, `vh`, `vhv`, `hvh` give orthogonal paths with r=8 corners.
  Kinds `muted` (default), `link`, `accent` (max 2 per diagram). `dashed=True` for manual or
  planned flows.
- Budget: about 9 nodes; more is two diagrams (overview + detail). Delete before adding.
- Thai widths: `text_w()` ignores combining marks; leave 16 units of padding inside nodes.
- For chart and timeline types (bar, line, waterfall, Gantt...), write the SVG elements into
  `d.extra` following the type reference. Take colours from the live palette `C` (`C.ink`,
  `C.muted`, `C.soft`, `C.accent`, `C.accent_tint`, `C.link`, `C.paper`, `C.sans`). Do not
  `from dg import INK`: that copies the default colour before the theme loads.
- Axis labels and annotations: `d.text(x, y, "...", mask=True)` keeps them readable over
  grid lines.

## Placing and injecting

Put `<div class="dgwrap"><!--DIAG:flow--><!--/DIAG:flow--></div>` in the slide body (and in the
handout, same marker, if it shows the diagram). Run `python diagrams.py` from `diagrams/`: it
injects into every `.html` in the project. Never edit between the markers by hand.

## Checking

- Render the slide and look: labels clear of lines, no text over node edges, arrows end at
  node borders, one or two accents only.
- `scripts/diagram_self_check.py` is diagram-design's checker for **standalone** diagram pages
  (one diagram per HTML file, its own controls script). It fails on any deck by design; use it
  only when the user asks for a standalone diagram file built the diagram-design way.
