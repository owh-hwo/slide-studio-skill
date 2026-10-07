# Writing the slides

## The page pattern

```
kicker (section)                                   [chip][chip][CHIP][chip]
Action title: a full sentence that states the conclusion
Lead: one line of context (optional)
──────────────────────────────────────────────── (rule)
content: table / cards / diagram / steps
[ ประเด็นสำคัญ ] one sentence that the audience should remember
──────────────────────────────────────────────── (footer rule)
logo   footer text                                  หน้า n / N  logo
```

## Titles

- A sentence with a verb and the conclusion: "Role ของบริษัทแยกงานจัดซื้อ งานรายได้ และงานบัญชีออกจากกัน",
  not "Role ของบริษัท".
- Fit in two lines at 50px (about 55 to 60 Thai characters or 70 Latin per line).
- No one-word orphan on the second line: shorten the title, never shrink the font.
- Numbers in titles when the slide is about a number.
- Read all titles in order (the ghost deck): they must tell the story without the bodies.
- The title must agree with the body. If the table shows two kinds of answers, the title
  cannot promise only one (a real review comment: "the title said 'affects only the requester'
  while two rows affected everyone holding the role").

## Lead

One line, optional. Context the title cannot carry: the scope, the source, the rule behind
the table. Not a second title.

## Body

- One idea per slide; one visual (table, diagram, cards) per slide.
- Tables: header row + 3 to 6 rows on a main slide; group rows with `td.band` when the
  table has two kinds of rows (and say so in the title or lead).
- A column holds one kind of fact. Do not mix "who is affected" with "what happens" in the
  same column.
- Cards: 2 to 4; each card = heading + one or two short lines.
- Fill the slide: if more than about a third of the body is empty, enlarge (table.big, larger
  card text via a per-slide class) or merge with the neighbouring slide.

## Takeaway (`.take`)

- Exactly one per content slide; covers and dividers have none.
- One sentence; one `<b>` phrase that is the hook.
- It answers "so what?" for the slide; it does not repeat the title verbatim.

## Speaker notes (`<aside class="notes">`)

- Write what the presenter says, in the first person, in the presentation language.
- Order: what the slide shows → how to read it → the point → the bridge to the next slide.
- Bold (`<strong>`) the phrases to stress; bold survives into the PPTX notes pane.
- Demos: minute-by-minute steps and how to reset. Labs and case studies: the answer key lives
  here and only here.
- Brief content rules apply to notes as well (no forbidden names, no recommendations if
  ruled out, no em dashes if ruled out).

## Language (Thai audiences, unless the brief says otherwise)

- Thai text; technical terms in English without Thai translation (Role, Permission, Invoice,
  Saved Search, Dashboard...). A space between Thai and English words.
- Ordinary words stay Thai (ผู้ใช้, รายงาน, โรงพยาบาล).
- Define a Thai term once per slide at first use if the brief asks for it.
- Use the client's own names for their entities exactly as their system holds them.

## Facts, numbers, examples

- Every client fact comes from a source the user gave or a system you read, with a date.
  Re-check it before printing it.
- Illustrative content is labelled ("ตัวอย่าง", "Example").
- Units and currency on every number; consistent decimals within a table.
- Say in chat (not on slides) what was measured vs inferred, from which source and date.
- Derived numbers (sums, differences, percentages computed from given figures) are fine; show
  the inputs in the notes so the presenter can explain them.
- When the work-type skeleton wants a slide the user gave no data for (owners, dates, next
  period, appendix): ask in the interview (branch B3). If the data still does not exist, drop
  the slide, and list it under open items in brief.md and in chat. Never fill it with invented data.

## House style switches (from the brief)

Apply only what the brief chose; common ones: no em dashes; no document date; no clock times
or schedule; no data volumes; no recommendations / risks / open questions on slides (they go
to the user in chat); never name an internal system.
