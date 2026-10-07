"""Find clipped or colliding content on fixed-size slides (decks) or pages (handouts).

Slides and pages use overflow:hidden, so text that does not fit is cut off silently.
This loads the file in headless Chrome and reports, per slide/page:
  - overflow : an element sticks out of the box (it is being clipped)
  - clips    : an element with overflow hidden is cutting its own content
  - rule     : content crosses the footer rule (deck: 92px from the bottom; handout: the
               <footer>) or comes closer than --gap. The overflow test cannot see this,
               because the content is still inside the box.

    python check_overflow.py "<deck or handout>.html" [--gap 10]

Exit code 1 when anything is reported. Covers and section dividers have no rule.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import CHROME  # noqa: E402

PROBE = r"""
<script>
window.addEventListener('load', () => setTimeout(() => {
  const GAP = __GAP__;
  const out = [];
  const deck = document.querySelector('.deck');
  const boxes = deck ? [...document.querySelectorAll('.deck > .slide')] : [...document.querySelectorAll('.page')];
  boxes.forEach((box, i) => {
    if (deck) { boxes.forEach(b => b.classList.remove('is-active')); box.classList.add('is-active'); }
    const r = box.getBoundingClientRect();
    const plain = deck && !box.classList.contains('cover') && !box.classList.contains('section');
    const foot = deck ? null : box.querySelector(':scope > footer');
    const ruleY = deck ? (plain ? r.bottom - 92 : null) : (foot ? foot.getBoundingClientRect().top : null);
    let worst = 0, who = '', near = -1e9, nearWho = '';
    box.querySelectorAll('*').forEach(el => {
      if (el.closest('.notes, aside.notes, .deck-footer, .deck-header, .foot, footer')) return;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const e = el.getBoundingClientRect();
      if (!e.width || !e.height) return;
      const name = el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '');
      const over = Math.max(e.bottom - r.bottom, e.right - r.right, 0);
      if (over > worst + 0.5) { worst = over; who = name; }
      if (ruleY !== null && e.bottom - ruleY > near) { near = e.bottom - ruleY; nearWho = name; }
      if (el.scrollHeight > el.clientHeight + 2 && /hidden|clip/.test(cs.overflowY) && el !== box && el.tagName !== 'svg') {
        out.push(`${i + 1}: ${name} clips ${el.scrollHeight - el.clientHeight}px`);
      }
    });
    if (box.scrollHeight > box.clientHeight + 1) worst = Math.max(worst, box.scrollHeight - box.clientHeight);
    if (worst > 1) out.push(`${i + 1}: overflows by ${Math.round(worst)}px (${who})`);
    if (ruleY !== null && near > -GAP) out.push(`${i + 1}: ${nearWho} ` + (near > 0 ? `crosses the footer rule by ${Math.round(near)}px` : `ends ${Math.round(-near)}px above the footer rule (need ${GAP})`));
  });
  document.title = 'OVERFLOW[' + boxes.length + ']' + (out.length ? out.join(' | ') : 'none');
}, 1500));
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--gap", type=int, default=None, help="min px between content and footer rule (deck 10: the pinned .take sits 16px above it; handout 8)")
    a = ap.parse_args()
    src = Path(a.file).resolve()
    text = src.read_text(encoding="utf-8")
    gap = a.gap if a.gap is not None else (10 if 'class="deck"' in text else 8)
    tmp = src.with_name(".overflow-probe-" + src.name)
    tmp.write_text(text.replace("</body>", PROBE.replace("__GAP__", str(gap)) + "</body>"), encoding="utf-8")
    try:
        res = subprocess.run([CHROME, "--headless=new", "--window-size=1920,1080", "--virtual-time-budget=6000",
                              "--dump-dom", tmp.as_uri()], capture_output=True, text=True, encoding="utf-8", timeout=180)
    finally:
        tmp.unlink(missing_ok=True)
    m = re.search(r"<title>OVERFLOW\[(\d+)\](.*?)</title>", res.stdout, re.S)
    if not m:
        print("probe did not run")
        return 2
    print(f"{src.name}: {m.group(1)} boxes")
    if m.group(2) == "none":
        print("  no overflow, nothing near the footer rule")
        return 0
    for line in m.group(2).split(" | "):
        print("  " + line)
    return 1


if __name__ == "__main__":
    sys.exit(main())
