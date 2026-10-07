"""Diagrams for this deck. Edit the functions below, then run from this folder:

    python diagrams.py

Each function returns one SVG; DIAGRAMS maps the marker name to the function. The deck
carries <!--DIAG:name--><!--/DIAG:name--> inside a <div class="dgwrap">. Never hand-edit
the SVG between the markers: it is overwritten on every run.
Read the skill's references/diagrams.md before drawing a new one.
"""
from pathlib import Path

from dg import C, D, H, V, hv, vh, vhv, hvh, inject, load_theme  # theme colours: C.ink, C.muted, C.accent, C.link ...

HERE = Path(__file__).resolve().parent
load_theme(HERE.parent / "assets" / "theme.json")
DECKS = sorted(HERE.parent.glob("*.html"))  # every deck (and handout) in the project folder


def d_sample():
    d = D("sample", 1032, 300, "สาขาส่งข้อมูลเข้าระบบเดียว",
          "สามสาขาบันทึกลงระบบ ERP เดียว ผู้บริหารเห็นรายงานจากฐานข้อมูลเดียวกัน")
    for i, name in enumerate(["สาขา 1", "สาขา 2", "สาขา 3"]):
        y = 20 + i * 96
        d.arrow(hvh(200, y + 32, 380, 150, 290), "muted")
        d.node(0, y, 200, 64, name, "บันทึกเอกสารประจำวัน", "backend")
    d.arrow(H(620, 150, 760), "accent")
    d.label(690, 150, "ทันที", "above")
    d.node(380, 104, 240, 92, "ระบบ ERP", "ฐานข้อมูลเดียว", "focal", tag="ERP")
    d.node(760, 112, 272, 76, "รายงานผู้บริหาร", "ตัวเลขล่าสุด", "dark")
    return d.render()


DIAGRAMS = {"sample": d_sample}

if __name__ == "__main__":
    for deck in DECKS:
        inject(deck, DIAGRAMS)
