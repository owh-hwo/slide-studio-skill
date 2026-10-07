# Work type: training course / workshop

The audience must be able to *do* something afterwards. Slides carry the concept and the
example; the trainer's notes carry the explanation; demos and labs carry the practice; the
handout carries everything the attendee takes home.

## Extra interview questions

- Sessions: how many, how long each; one deck per session (yes, if over ~3 hours).
- Format per session: lecture only, lecture + trainer demo, or hands-on workshop (labs).
- Attendee level and role (end users vs admins vs executives); class size.
- Environment for demos/labs: which system or account, what test data, what each attendee
  needs prepared (logins, sample files). Unknowns → open items in chat.
- Naming convention for things attendees create in labs (e.g. prefix `[TRN01]`), so their
  work never collides with real data.
- Handout: yes by default; same order as the deck; slides cite handout pages.
- Is the schedule (dates, times, breaks) confirmed? If not, keep times off the slides.

## Storyline skeleton (per session)

| Part | Slides | Pattern |
|---|---|---|
| Cover with 4 key messages | 1 | cover |
| Agenda (topics; session 1 dimmed in later sessions) | 1 | agenda / agenda2 |
| Objectives: what you will be able to do | 1 | objs |
| (session 2+) Recap of the previous session | 1 | principles or table |
| Per section: divider → concept → example from the client's own system → demo or lab | 4 to 8 | section, table, cards, diagram, steps + `.mode.demo` / `.mode.lab` |
| Case studies or exercises (answers in notes only) | 1 to 2 | cases |
| Summary: what each part gives the client | 1 | table.big |
| Q&A / close | 1 | section |

## Sizing

- Put `data-min` on every slide (invisible) and sum it: the deck should fill 90 to 95% of
  the slot. Concept slides 3 to 5 min, demos 8 to 15, labs 15 to 40, dividers 1.
- Lecture runs about 1 slide per 4 minutes; a 3-hour session is roughly 25 to 35 slides
  including demos and labs.

## Demo and lab slides

- Demo: kicker `<span class="mode demo">สาธิตบนระบบ</span>`, title = what we will show,
  `.steps` with 4 to 6 steps, menu paths in `<span class="path">Setup › Users › New</span>`.
  Notes: minute-by-minute script ("minute 0 to 2: ...") and how to reset afterwards.
- Lab: `<span class="mode lab">ฝึกปฏิบัติ</span>`, steps, a dashed `.out` box "what you should
  see at the end". Notes: the answer key and common mistakes.
- Examples come from the client's real setup (verified); exercises must not duplicate an
  object that already exists; copy the client's own patterns instead.

## Handout

`new_deck.py --handout`. One A4 page roughly per 2 to 3 slides; same section order, same
action titles where they match; the deck's section dividers cite handout page ranges
(`<div class="ref">เอกสารประกอบ หน้า 6 ถึง 9</div>`), so renumber both together.
Check the handout PDF page count equals its number of `.page` sections.

## Pitfalls

- Teaching menus instead of decisions: every concept slide needs the client's own example.
- Answer keys on the slide: keep them in notes.
- Times and dates on slides before the schedule is confirmed.
