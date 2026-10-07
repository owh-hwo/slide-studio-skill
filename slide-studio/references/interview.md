# Interview: grill until the brief is complete

The interview turns a vague request ("make me slides for the steering committee") into a brief
that leaves nothing to guess. It is a decision tree: resolve each branch, in dependency order,
one question at a time.

## How to ask

1. **Explore first.** Before each question, check whether the answer is already available:
   files the user attached or named, the project folder, a CLAUDE.md, previous decks, a website,
   a connected system. If so, state what you found and ask only for confirmation if it matters.
2. **One question per turn.** Never stack five questions in one message; the user answers the
   first and skips the rest. (AskUserQuestion may carry up to 4 *independent* choice questions
   when they are quick and unrelated, e.g. footer text + page label + takeaway label.)
3. **Always recommend.** Every question carries your recommended answer and one line of why.
   Put the recommended option first in AskUserQuestion and mark it "(แนะนำ)" / "(Recommended)".
4. **Choice vs open.** Choices (theme, length, deliverables) → AskUserQuestion. Open content (the
   decision you want, the 4 key messages, who is in the room) → plain question with a drafted
   answer the user can accept or edit ("I'd put the four cover messages as: ... Change any?").
5. **Follow the dependencies.** If an answer changes earlier assumptions, say so and revisit.
6. **Know when to stop.** Done when every branch below is answered or defaulted. If the user
   says "use your judgement", apply the defaults for the work type and list them in the brief.
7. **Never fabricate content to fill a branch.** If the user does not know a number or fact, it
   becomes an open item (in chat), or the slide uses a labelled example.

## The tree (in order)

### A · The job

| # | Question | Default / recommendation |
|---|---|---|
| A1 | What kind of work is this? training · executive / board · proposal / pre-sales · status / go-live report · other | infer from the request; confirm |
| A2 | Who is in the room (role, seniority, how many, what they already know)? | executives: assume no system knowledge |
| A3 | What must the audience do or decide afterwards? (one sentence) | executive/status: a decision; training: perform tasks; proposal: choose us / next meeting |
| A4 | How is it delivered: live on a projector, online share, or read without a presenter? | live → fewer words, full notes; read-ahead → fuller leads, handout |
| A5 | How long is the slot? (minutes per deck / per session) | sets the slide budget, see work-type file |
| A6 | Language and terminology rules (Thai / English / mixed; technical terms translated or not) | Thai audience: Thai text, English technical terms, no translation |

Then load the matching `work-types/<type>.md` and use its defaults for everything below.

### B · Content

| # | Question | Notes |
|---|---|---|
| B1 | What source material exists? (documents, data, a system, earlier decks, notes) | read it all before continuing |
| B2 | The four key messages (they go on the cover and drive the storyline) | draft them from B1 and A3, ask the user to edit |
| B3 | Which numbers, examples and names must appear, and where each comes from (and its date) | every number needs a source; unknowns → open items |
| B4 | What must NOT appear? (confidential data, competitor names, internal gaps, prices, people's names, a system name) | becomes "content rules" in the brief; they apply to notes too |
| B5 | May the deck contain recommendations, risks and open questions, or only the current state? | ask explicitly for client-facing decks; it changes the tone |
| B6 | Work-type specifics (labs and demos for training, the ask for executive, pricing for proposal, reporting period for status) | see the work-type file |

### C · Storyline

| # | Question | Notes |
|---|---|---|
| C1 | Structure: confirm the skeleton from the work-type file, adapted to B2 | show it as a short section list |
| C2 | Sections and their names (they become the kicker and the chips in the top right) | 3 to 6 sections |
| C3 | Appendix or backup slides? | executive and proposal: yes, after the closing slide |

The full slide list (ghost deck) is Phase 2; C only fixes the frame.

### D · Theme

| # | Question | Notes |
|---|---|---|
| D1 | Preset or custom? Open `assets/previews/index.html` for the user first | recommend by audience: see the table in themes.md |
| D2 | If custom: from a website URL, a logo, a brand guide, or hex codes? | build the JSON (themes.md), preview, iterate |
| D3 | Logos: main logo (and a white version for dark slides), partner / presenter logo | files the user gives; none → the footer simply has no logo |
| D4 | Footer text (e.g. `Client · Course name · Presenter`) | |
| D5 | Takeaway label and page label | Thai: "ประเด็นสำคัญ" / "หน้า"; English: "Key takeaway" / "" |
| D6 | Font: bundled Sarabun (works offline, Thai + Latin) or another | Sarabun unless the brand mandates one |
| D7 | House-style rules: no em dashes? no dates on slides? no times or schedule? | ask once; record in the brief |

### E · Deliverables

| # | Question | Default |
|---|---|---|
| E1 | How many decks (one per session for multi-session training)? | one |
| E2 | Handout (A4 landscape companion)? | training: yes; read-ahead: yes; others: no |
| E3 | Exports: PPTX (picture per slide + notes), PDF? | both |
| E4 | Speaker notes: full spoken script, bullet cues, or none? | live delivery: full script |
| E5 | File names and folder | `<project>/<Deck name>.html` |

## brief.md template

```markdown
# Brief: <deck name>

## Job
- Work type: ...            - Audience: ...           - Delivery: ...
- Goal (what they do/decide after): ...
- Slot: ... min             - Language: ...

## Key messages (cover)
1. ...  2. ...  3. ...  4. ...

## Content rules
- Must include: ...
- Must not appear (slides AND notes): ...
- Recommendations / risks on slides: yes / no
- Sources: <file / system / person> (as of <date>)

## Theme
- Theme: <preset or path to custom JSON>   - Font: ...
- Logos: main ..., dark ..., partner ...
- Footer: "..."   - Takeaway label: "..."   - Page label: "..."
- House style: ...

## Deliverables
- Decks: ...   - Handout: yes/no   - Exports: PPTX, PDF   - Notes: full script / cues / none

## Storyline (ghost deck, Phase 2)
| # | Section | Action title | Takeaway | Pattern | Min |
|---|---|---|---|---|---|

## Open items (told to the user in chat, never on slides)
- ...
```
