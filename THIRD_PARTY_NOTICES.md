# Third-party notices

slide-studio bundles the following third-party components. Each keeps its own licence.

## html-ppt runtime

Files: `slide-studio/assets/runtime/base.css`, `runtime.js`, `animations.css`
Licence: MIT. Full text: `slide-studio/assets/runtime/html-ppt-LICENSE.txt`.
`runtime.js` is modified: preview mode (`?preview=N`) disables the slide transition so headless
screenshots never catch a slide mid-fade.

## diagram-design skill

Files: `slide-studio/references/diagram/` (including `DIAGRAM-DESIGN.md`, the original SKILL.md)
and `slide-studio/scripts/diagram_self_check.py`.
Licence: MIT (declared in the skill's metadata, version 2.6). Bundled unmodified.
`slide-studio/scripts/dg.py` re-implements its drawing grammar (orthogonal connectors with r=8
corners, masked labels, accent budget) for theme-aware SVG inside decks.

## Sarabun

Files: `slide-studio/assets/fonts/Sarabun-*.ttf`
Licence: SIL Open Font License 1.1. Full text: `slide-studio/assets/fonts/OFL.txt`.
