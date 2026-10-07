"""Diagram primitives for slide-studio decks: inline SVG skinned from the deck's theme.

Copied into every new deck as <deck>/diagrams/dg.py, next to diagrams.py (the deck's own
diagram definitions). Grammar follows the diagram-design rules bundled with the skill
(references/diagram/): orthogonal connectors with r=8 corners, arrows drawn before nodes,
labels masked with a paper-coloured box sitting 8px off the line, at most two accent
elements per diagram, about 9 nodes, deletion before addition.

    from dg import C, D, H, V, hv, vh, vhv, inject, load_theme   # colours: C.ink, C.accent ...
    load_theme("../assets/theme.json")          # sets the palette below
    d = D("sys", 1032, 300, "title for screen readers", "longer description")
    d.arrow(H(200, 150, 252)); d.node(0, 112, 200, 76, "Branch", "sub line")
    svg = d.render()

Then put <!--DIAG:sys--><!--/DIAG:sys--> in the deck (inside a .dgwrap) and inject().
"""
import json
import re
from pathlib import Path
from types import SimpleNamespace

PAPER, INK, MUTED, SOFT = "#FDFDFB", "#214139", "#4F5B57", "#8A9792"
ACCENT, ACCENT_TINT, LINK, LINK_TINT = "#B18E50", "#F7F1E5", "#357A63", "#E3EFE9"
SANS = "Sarabun, Tahoma, 'Leelawadee UI', sans-serif"
MONO = "Consolas, monospace"
KINDS, STROKES = {}, {}
# Live palette. `from dg import INK` copies the value at import time (before load_theme runs),
# so in diagrams.py read colours as C.ink, C.accent ... (or dg.INK): those follow the theme.
C = SimpleNamespace()


def _rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"


def _rebuild():
    C.__dict__.update(paper=PAPER, ink=INK, muted=MUTED, soft=SOFT, accent=ACCENT, accent_tint=ACCENT_TINT,
                      link=LINK, link_tint=LINK_TINT, sans=SANS, mono=MONO)
    KINDS.clear(); STROKES.clear()
    KINDS.update({
        "backend":  ("#FFFFFF", INK, None),             # default box
        "focal":    (ACCENT_TINT, ACCENT, None),        # the one thing the slide is about (max 2)
        "store":    (_rgba(INK, .05), MUTED, None),     # database / file / table
        "external": (_rgba(INK, .03), _rgba(INK, .35), None),  # outside our control
        "input":    (_rgba(MUTED, .10), SOFT, None),    # source / trigger
        "link":     (LINK_TINT, LINK, None),            # integration / interface
        "dark":     (INK, INK, None),                   # end result, dashboard
        "optional": (_rgba(INK, .02), _rgba(INK, .30), "4,3"),  # future / not built / manual
    })
    STROKES.update({"muted": MUTED, "accent": ACCENT, "link": LINK})


def load_theme(path):
    """Map the deck theme onto the diagram roles (paper, ink, muted, soft, accent, link)."""
    global PAPER, INK, MUTED, SOFT, ACCENT, ACCENT_TINT, LINK, LINK_TINT, SANS, MONO
    t = json.loads(Path(path).read_text(encoding="utf-8"))
    c = t["colors"]
    PAPER, INK, MUTED, SOFT = c["paper"], c["brand"], c["muted"], c["soft"]
    ACCENT, ACCENT_TINT, LINK, LINK_TINT = c["hl"], c["hl_tint"], c["accent"], c["tint"]
    SANS, MONO = t["fonts"]["sans"], t["fonts"]["mono"]
    _rebuild()


_rebuild()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text_w(t, size, mono=False):
    """Rough text width. Thai combining marks take no width; Latin/Thai glyph ~0.56em."""
    marks = sum(1 for ch in t if ch in "ัิีึืฺุู็่้๊๋์ํ")
    return (len(t) - marks) * size * (0.6 if mono else 0.56)


class D:
    def __init__(self, slug, w, h, title, desc):
        self.slug, self.w, self.h = slug, w, h
        self.title, self.desc = title, desc
        self.zones, self.arrows, self.labels, self.nodes, self.extra = [], [], [], [], []

    def zone(self, x, y, w, h, label, dashed=False):
        """A boundary (team, system, network) with its label notched into the top edge."""
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        lw = text_w(label, 10) + 14
        self.zones.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{_rgba(INK, .025)}" '
            f'stroke="{_rgba(INK, .18)}" stroke-width="0.9"{dash}/>'
            f'<rect x="{x+12}" y="{y-7}" width="{lw:.0f}" height="14" rx="2" fill="{PAPER}"/>'
            f'<text x="{x+19}" y="{y+3.5}" fill="{MUTED}" font-size="10" font-weight="bold" '
            f'font-family="{SANS}" letter-spacing="0.4">{esc(label)}</text>')

    def node(self, x, y, w, h, name, sub=None, kind="backend", tag=None, size=13):
        """name / sub may be a list for several lines; tag is a small mono label (API, DB)."""
        fill, stroke, dash = KINDS[kind]
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        name_c = "#FFFFFF" if kind == "dark" else INK
        sub_c = _rgba("#FFFFFF", .85) if kind == "dark" else MUTED
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
               f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{1.4 if kind == "focal" else 1}"{dash_attr}/>']
        if tag:
            tw = text_w(tag, 8, mono=True) + 10
            out.append(f'<rect x="{x+8}" y="{y+7}" width="{tw:.0f}" height="13" rx="2" fill="none" '
                       f'stroke="{stroke}" stroke-opacity="0.5" stroke-width="0.8"/>'
                       f'<text x="{x+8+tw/2:.1f}" y="{y+16.5}" fill="{stroke}" font-size="8" '
                       f'font-family="{MONO}" text-anchor="middle" letter-spacing="0.6">{esc(tag)}</text>')
        names = name if isinstance(name, list) else [name]
        subs = [] if sub is None else (sub if isinstance(sub, list) else [sub])
        lh, slh = size + 4, 14
        block = len(names) * lh + len(subs) * slh
        top = y + (h - block) / 2 + (6 if tag else 0)
        cx = x + w / 2
        for i, n in enumerate(names):
            out.append(f'<text x="{cx}" y="{top + lh*(i+1) - 4:.1f}" fill="{name_c}" font-size="{size}" '
                       f'font-weight="bold" font-family="{SANS}" text-anchor="middle">{esc(n)}</text>')
        for i, sb in enumerate(subs):
            out.append(f'<text x="{cx}" y="{top + len(names)*lh + slh*(i+1) - 3:.1f}" fill="{sub_c}" '
                       f'font-size="10.5" font-family="{SANS}" text-anchor="middle">{esc(sb)}</text>')
        self.nodes.append("".join(out))

    def arrow(self, d, kind="muted", dashed=False, head=True):
        """d is an SVG path from the helpers below. kind: muted (default), link, accent (max 2)."""
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        mk = f' marker-end="url(#{self.slug}-ar-{kind})"' if head else ""
        self.arrows.append(f'<path d="{d}" fill="none" stroke="{STROKES[kind]}" '
                           f'stroke-width="{1.6 if kind == "accent" else 1.25}"{dash}{mk}/>')

    def label(self, x, y, t, side="above", mono=False, color=None):
        """(x, y) is a point on the connector; the masked label sits 8px off it."""
        size = 9 if mono else 10
        w, h = text_w(t, size, mono) + 12, 15
        if side == "above":
            rx, ry = x - w / 2, y - 8 - h
        elif side == "below":
            rx, ry = x - w / 2, y + 8
        elif side == "right":
            rx, ry = x + 8, y - h / 2
        else:
            rx, ry = x - 8 - w, y - h / 2
        fam = MONO if mono else SANS
        ls = ' letter-spacing="0.6"' if mono else ""
        self.labels.append(
            f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{w:.1f}" height="{h}" rx="2" fill="{PAPER}"/>'
            f'<text x="{rx + w/2:.1f}" y="{ry + 11:.1f}" fill="{color or MUTED}" font-size="{size}" '
            f'font-family="{fam}" text-anchor="middle"{ls}>{esc(t)}</text>')

    def text(self, x, y, t, size=11, color=None, bold=False, anchor="start", mask=False):
        """Free text (column headings, legends, axis labels). mask=True puts a paper-coloured box
        behind it so it stays readable where it crosses grid or connector lines."""
        fw = ' font-weight="bold"' if bold else ""
        if mask:
            w = text_w(t, size) + 8
            x0 = x - 4 if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w + 4)
            self.extra.append(f'<rect x="{x0:.1f}" y="{y - size:.1f}" width="{w:.1f}" height="{size + 5}" rx="2" fill="{PAPER}"/>')
        self.extra.append(f'<text x="{x}" y="{y}" fill="{color or INK}" font-size="{size}"{fw} '
                          f'font-family="{SANS}" text-anchor="{anchor}">{esc(t)}</text>')

    def render(self):
        markers = "".join(
            f'<marker id="{self.slug}-ar-{k}" markerWidth="8" markerHeight="6" refX="7" refY="3" '
            f'orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{c}"/></marker>'
            for k, c in STROKES.items())
        return (f'<svg class="dg" viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-labelledby="{self.slug}-title {self.slug}-desc" style="width:100%; height:auto; display:block;">'
                f'<title id="{self.slug}-title">{esc(self.title)}</title>'
                f'<desc id="{self.slug}-desc">{esc(self.desc)}</desc>'
                f'<defs>{markers}</defs>'
                + "".join(self.zones) + "".join(self.arrows) + "".join(self.labels)
                + "".join(self.nodes) + "".join(self.extra) + "</svg>")


# ---- path helpers: straight runs and single/double bends with r=8 corners ----
def _s(a, b):
    return 1 if b > a else -1


def H(x1, y, x2):
    return f"M{x1},{y} H{x2}"


def V(x, y1, y2):
    return f"M{x},{y1} V{y2}"


def hv(x1, y1, x2, y2):
    """horizontal, then vertical."""
    sx, sy = _s(x1, x2), _s(y1, y2)
    return f"M{x1},{y1} H{x2-8*sx} Q{x2},{y1} {x2},{y1+8*sy} V{y2}"


def vh(x1, y1, x2, y2):
    """vertical, then horizontal."""
    sx, sy = _s(x1, x2), _s(y1, y2)
    return f"M{x1},{y1} V{y2-8*sy} Q{x1},{y2} {x1+8*sx},{y2} H{x2}"


def vhv(x1, y1, x2, y2, my):
    """vertical to my, across, vertical again (fan-out from one node to a row)."""
    sx, s1, s2 = _s(x1, x2), _s(y1, my), _s(my, y2)
    return (f"M{x1},{y1} V{my-8*s1} Q{x1},{my} {x1+8*sx},{my} H{x2-8*sx} "
            f"Q{x2},{my} {x2},{my+8*s2} V{y2}")


def hvh(x1, y1, x2, y2, mx):
    """horizontal to mx, vertical, horizontal again (fan-in from a column)."""
    sy, s1, s2 = _s(y1, y2), _s(x1, mx), _s(mx, x2)
    return (f"M{x1},{y1} H{mx-8*s1} Q{mx},{y1} {mx},{y1+8*sy} V{y2-8*sy} "
            f"Q{mx},{y2} {mx+8*s2},{y2} H{x2}")


def inject(path, diagrams, required=False):
    """Replace every <!--DIAG:name-->...<!--/DIAG:name--> block in one HTML file.
    diagrams = {name: function returning svg}. required=True fails on a missing marker."""
    path = Path(path)
    html = path.read_text(encoding="utf-8")
    n = 0
    for name, fn in diagrams.items():
        pat = re.compile(rf"(<!--DIAG:{name}-->).*?(<!--/DIAG:{name}-->)", re.S)
        if not pat.search(html):
            if required:
                raise SystemExit(f"marker for {name} not found in {path.name}")
            continue
        html = pat.sub(lambda m: m.group(1) + fn() + m.group(2), html)
        n += 1
    path.write_text(html, encoding="utf-8")
    print(f"wrote {n} diagrams into {path.name}")
    return n
