#!/usr/bin/env python3
"""Variant B (visual-led) for make.fun news-image-20261121.

Same 37 verified stories as gen.py, different composition: a full-width
lead row (big illustration + world map side by side), a 6-column
illustrated grid with larger pictures, and compact stories as two-column
one-liners. Deterministic like gen.py. Run: python3 gen_b.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen import (  # noqa: E402
    W, H, PAPER, PAPER2, INK, GREY, LINE, RED, MAP_SEA,
    F_SERIF_B, F_SANS_B, F_SANS, font, wrap, panel, num_badge,
    SCENES, LEAD, ILLUSTRATED, COMPACT, draw_map,
)
from PIL import Image, ImageDraw  # noqa: E402

# Short subheads for the narrow 6-column grid (max 46 chars).
B_SUB = {
    2: "FBI most-wanted boss seized; 11 dead.",
    3: "Draft drops 'fossil fuels'; EU holds out.",
    4: "Two killed, about 60 hurt in hometown.",
    5: "One dead, 16 hurt; 152 homes wrecked.",
    6: "S&P -3.7%; Nasdaq erases 2026 gains.",
    7: "Three-way talks; Zelensky blasts Putin.",
    8: "AI helped solve 160-year-old problem.",
    9: "First state held responsible: Myanmar.",
    10: "Russian cargo ship ablaze in Baltic.",
    11: "Food vehicle hit; three Palestinians die.",
    12: "Eight-year journey ends at Mercury.",
    13: "Four dead, 35 hurt at Iraqi plant.",
}

COL6_X = [14 + i * 167 for i in range(6)]   # 159 wide, 8 gap
COL6_W = 159


def masthead_b(d):
    f_title = font(F_SERIF_B, 52)
    d.text((W / 2, 6), "THE WORLD IN ONE DAY", font=f_title, fill=INK, anchor="ma")
    d.rectangle([14, 62, W - 14, 65], fill=RED)
    f_date = font(F_SANS_B, 21)
    d.text((14, 69), "SATURDAY 21 NOVEMBER 2026", font=f_date, fill=INK)
    f_meta = font(F_SANS_B, 13)
    d.text((W - 14, 72), "37 STORIES  ·  9 REGIONS", font=f_meta, fill=GREY, anchor="ra")


def lead_row_b(d):
    # Big illustration left, world map right.
    panel(d, [14, 88, 634, 238], fill=PAPER2)
    SCENES["lead"](d, 18, 92, 612, 142)
    num_badge(d, 36, 110, 1, r=12)
    panel(d, [642, 88, 1010, 238], fill=PAPER2)
    draw_map(d, 646, 92, 360, 122)
    f_cap = font(F_SANS_B, 10)
    d.text((646, 220), "WORLD MAP — PINS MARK THE ILLUSTRATED STORIES",
           font=f_cap, fill=GREY)


def lead_head_b(d):
    f_kick = font(F_SANS_B, 12)
    d.text((14, 246), "LEAD  ·  " + LEAD["place"], font=f_kick, fill=RED)
    f_head = font(F_SERIF_B, 30)
    d.text((14, 262), LEAD["headline"], font=f_head, fill=INK)
    f_sub = font(F_SANS, 15)
    for i, ln in enumerate(wrap(d, LEAD["subhead"], f_sub, 996)):
        d.text((14, 298 + i * 18), ln, font=f_sub, fill=INK)


def grid_cell_b(d, x, y, story):
    panel(d, [x, y, x + COL6_W, y + 132], fill=PAPER2)
    SCENES[story["kind"]](d, x + 3, y + 3, COL6_W - 6, 66)
    num_badge(d, x + 14, y + 14, story["n"], r=10, size=10)
    f_head = font(F_SANS_B, 15)
    lines = wrap(d, story["b_head"], f_head, COL6_W - 6)
    hy = y + 72
    for i, ln in enumerate(lines[:2]):
        d.text((x + 3, hy + i * 16), ln, font=f_head, fill=INK)
    f_sub = font(F_SANS, 11)
    slines = wrap(d, B_SUB[story["n"]], f_sub, COL6_W - 6)
    for i, ln in enumerate(slines[:2]):
        d.text((x + 3, hy + len(lines[:2]) * 16 + 2 + i * 12), ln, font=f_sub, fill=GREY)


def compact_line_b(d, x, y, n, headline, subhead):
    f_num = font(F_SANS_B, 13)
    d.text((x, y), str(n), font=f_num, fill=RED)
    f_head = font(F_SANS_B, 13)
    d.text((x + 22, y), headline, font=f_head, fill=INK)
    hw = d.textlength(headline, font=f_head)
    f_sub = font(F_SANS, 12)
    d.text((x + 22 + hw + 8, y + 1), "—  " + subhead, font=f_sub, fill=GREY)
    d.line([x, y + 25, x + 486, y + 25], fill=LINE, width=1)


def bottom_band_b(d):
    d.rectangle([0, 990, W, H], fill=INK)
    f = font(F_SANS_B, 13)
    d.text((W / 2, 997), "ALL 37 STORIES WERE REPORTED ON SATURDAY 21 NOVEMBER 2026",
           font=f, fill=(240, 236, 224), anchor="ma")
    f2 = font(F_SANS, 11)
    d.text((W / 2, 1013),
           "SOURCES: REUTERS, AP, BBC, AFP, UPI, CNN  ·  MARKETS: S&P 500 -3.7%  ·  "
           "NIKKEI -5.1%  ·  BRENT $89.95",
           font=f2, fill=(200, 196, 184), anchor="ma")


def render_b(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead_b(d)
    lead_row_b(d)
    lead_head_b(d)
    rows_y = [326, 464]
    for i, story in enumerate(ILLUSTRATED):
        grid_cell_b(d, COL6_X[i % 6], rows_y[i // 6], story)
    # compact: two columns of 12 one-liners
    for i, (n, headline, subhead) in enumerate(COMPACT):
        col = i // 12
        row = i % 12
        x = 14 + col * 508
        y = 602 + row * 32
        compact_line_b(d, x, y, n, headline, subhead)
    bottom_band_b(d)
    img.save(path, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry-b.png")
    render_b(out)
    print("wrote", out)
