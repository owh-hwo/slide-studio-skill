# Slide patterns

Every pattern below has a working example in `assets/templates/gallery.html`; copy the
`<section>` and edit. Classes live in `assets/studio.css` (layout only; colours come from the
theme). Capacity = what fits at the default font size without crowding.

## Frames

| Pattern | Markup | Use for |
|---|---|---|
| Cover | `section.slide.cover` with `.course` (eyebrow), `h1`, `.sub`, `ul.msgs` (4 messages), `.meta` | first slide; title = the answer |
| Content | `section.slide` → `.top` (`.kicker` + `.prog` chips, `span.on` = current) → `h2.title` → `.lead` → `hr.rule` → `.body` (content + `.take` last) → `.foot` (text + `span.pg`) → `aside.notes` | every normal slide |
| Section divider | `section.slide.section` with `.no` (01), `h2`, `p`, optional `.ref` (handout pages); `.opts` (2 option cards, `.win` = recommended) for the ask | between sections; closing / decision slide |

Every slide carries `data-title` (presenter view) and `data-min` (minutes, for sizing).

## Content patterns

| Pattern | Classes | Capacity | Use for |
|---|---|---|---|
| Table | `table` / `table.big` / `table.big.tight`; `td.c` `td.r`; `td.band` group rows | 6 rows big, 8 normal | comparisons, matrices, registers |
| Matrix | `table` with `th.c`/`td.c` cells of levels | 6 roles × 6 columns | permission / responsibility matrices |
| Cards row | `.row` > `.col.card` (`.tint`, `.hl`, `.brand`) | 3 (4 if short) | parallel points under a table or diagram |
| Numbered grid | `.objs` > `.card` (`span.num` + h3 + `p.small`); `.card.wide` spans both | 4 (5 with wide) | objectives, outcomes, patterns |
| Principles | `.principles` > div (`.n`, h3, p) | 3 (4 max) | rules, pillars |
| KPI tiles | `.kpis` > div (`.k`, `b`, `.u`, `.d.up/.down/.flat`); `div.focus` for the one that matters | 4 | status, results |
| Target bar | `span.meter` > `i` (actual width %) + `s` (target position) inside a KPI tile | | actual vs target |
| RAG status | `span.rag.g/.a/.r/.n` inside a table cell | | workstream status |
| Phases | `.phases` > div (`.done`, `.now`, plain = future) | 5 to 6 | plan, roadmap, where we are |
| Compare | `.compare` > div (`.win` = recommended), `.hd` label | 2 | options, before / after |
| Price | `table.big.price`, `td.r` numbers, `tr.total` | 6 lines | commercials, budget |
| Steps | `ol.steps` > li (numbered automatically) | 6 | demo, lab, procedure |
| Checklist | `ul.ck` | 8 | readiness, onboarding |
| Cases | `.cases` > `.card` (`.hd` with num + `.tag.hl`, `p.sit`) | 3 | case studies, exercises |
| Agenda | `.agenda` grid (`.t` number, text, `.d` page); `.hl` current, `.dim` done | 6 rows | agenda |
| Diagram | `.dgwrap` > `<!--DIAG:name--><!--/DIAG:name-->`; `.dgwrap.fix` = natural height | 1 per slide | architecture, flow, process |
| Quote | `p.quote` | 1 | a principle or client statement |
| Inline | `span.path` (menu path), `span.tag` (`.hl`, `.brand`), `span.num`, `b` | | |
| Mode label | `span.mode.demo` / `span.mode.lab` in the kicker | | training demo / lab slides |
| Output box | `.out` (dashed) | 1 | "what you should see" in labs |

## Combining

- Body = one main visual + optional cards row + `.take`. Two main visuals on one slide is two
  slides.
- Diagram slides: `.dgwrap` takes the free height and letterboxes the SVG; keep the lead
  short so the diagram gets room.
- Sparse slide (body more than a third empty)? Add `roomy` to the `<section>` class: it scales up
  KPI tiles, compare cards, big tables, numbered grids and principles. For anything else add a
  per-slide class and a rule in the deck's `<style>`; do not edit studio.css.

## Per-deck CSS

Deck-only additions go in the deck's `<style>` block, prefixed `.ss` so they beat studio.css.
Use theme tokens (`var(--brand)`, `var(--hl)`, `var(--tint)`...), never hex values, so the
deck re-skins cleanly. Token roles are listed in themes.md.
