# Themes

A theme is one JSON file: colours, fonts, logos. `make_theme.py` turns it into `assets/theme.css`
(CSS custom properties) and `assets/theme.json` (read by the diagram code), so slides, handout
and diagrams always share one palette. Layout (`studio.css`) never names a colour.

## Presets

Show the user `assets/previews/index.html` (cover, a status table and a diagram per preset).

| Preset | Mood | Recommend for |
|---|---|---|
| `emerald-gold` | calm, premium, trustworthy | hospitals, premium services, corporate training |
| `navy-amber` | formal, solid, consulting | boards, finance, proposals |
| `charcoal-coral` | modern, sharp, tech | software pre-sales, product demos, IT |
| `teal-orange` | bright, friendly, professional | status reports, workshops, operations teams |
| `burgundy-sand` | dignified, highly formal | government, legal, ceremonial |

## Token roles (what each colour does)

| Key | Role | Rule of thumb |
|---|---|---|
| `brand` | cover and title colour, dark fills, footer chips | the logo's darkest colour; white text must read on it (≥ 4.5:1) |
| `brand2` | section-divider background | `brand` one step lighter |
| `accent` | kicker, table headers, demo label, diagram links | a mid tone of the brand hue; white text on it ≥ 4.5:1 |
| `hl` | highlight: rule under the title, numbers, focal diagram node, lab label | the brand's second colour; used sparingly |
| `hl_dk` / `hl_lt` | highlight for text on light / on dark backgrounds | |
| `tint`, `tint_border` | light fill of the accent hue (bands, tags, cards) | ~10% of accent on white |
| `hl_tint`, `hl_border` | light fill of the highlight (takeaway strip, focus cards) | ~10% of hl on white |
| `ink`, `muted`, `soft` | body text, secondary text, tertiary text | near-black tinted with the brand hue |
| `line`, `grey`, `row_alt` | rules and borders, chip background, zebra rows | |
| `paper`, `surface` | slide background, card background | off-white, white |
| `on_brand`, `on_brand_2`, `on_brand_rule` | text, secondary text, rules on brand-coloured slides | |
| `on_accent`, `on_hl` | text on accent / highlight fills | usually white |
| `backdrop` | page colour around the slide in the browser | dark brand |
| `good`, `warn`, `bad` | RAG and deltas | keep green / amber / red recognisable |

## Building a custom theme

1. Copy the closest preset: `themes/<preset>.json` → `<project>/theme-<client>.json`
   (keep custom themes in the project, not in the skill).
2. Get the brand colours, in this order of trust:
   - the user's brand guide or pasted hex codes;
   - the client website: fetch the page and its CSS, collect the colours actually used for
     the logo, headers and buttons (ignore one-off colours);
   - the logo file: read the SVG fills, or sample the PNG.
3. Map them: darkest brand colour → `brand`; a lighter tone of it → `brand2` and `accent`;
   the second brand colour → `hl`; derive tints at ~10% on white; ink = near-black with a
   touch of the brand hue.
4. Contrast: `make_theme.py` warns when white on `brand` / `accent` / `hl` or `ink` on `paper`
   falls below 4.5:1. Darken until the warning goes.
5. Fonts: keep `"bundled": "sarabun"` (Thai + Latin, offline). For a brand font set
   `"google"` to its Google Fonts CSS URL and put the family first in `sans` / `display`
   (good Thai-capable choices: Noto Sans Thai, IBM Plex Sans Thai, Anuphan, Prompt and Kanit for
   display). A Google font needs internet while presenting and while rendering.
6. Logos: `"main"` (for light slides), `"main_dark"` (white version for cover and dividers),
   `"partner"` / `"partner_dark"` (presenter or consultant logo after the page number).
   Paths are relative to the JSON file. SVG preferred; PNG at least 400px wide.
7. Preview: `python scripts/preview_theme.py <project>/theme-<client>.json <out>.png`, open it
   for the user, iterate. Then build with `--theme <project>/theme-<client>.json`.

## Re-skinning a finished deck

Re-run `new_deck.py "<project>" --theme <other> --name "<Deck>"`: it rewrites `assets/theme.css`
and keeps the deck. Then re-run `diagrams/diagrams.py` (diagram colours are baked into the
SVG) and re-check overflow (a different font can change line breaks).
