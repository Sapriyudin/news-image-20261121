#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261121.

Front page: "THE WORLD IN ONE DAY" — Saturday 21 November 2026.
37 stories, 9 regions. Every story was verified against live sources
(oneturn.news/day/2026-11-21, Reuters, AP, BBC, AFP, UPI, CNN, Xinhua)
on 22 Nov 2026. Only events that happened or were first reported on
21 November 2026 are used; dates are exact (see SOURCES.md).

Deterministic: no clock, no randomness, fixed palette and geometry.
Run: python3 gen.py  ->  writes entry.png (1024x1024, PNG).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 244, 230)      # newsprint cream
PAPER2 = (244, 236, 218)     # slightly darker cream for panels
INK = (26, 26, 24)           # near-black ink
GREY = (96, 92, 84)          # secondary text
LINE = (180, 172, 156)       # hairline rules
RED = (158, 27, 31)          # one accent: deep red
RED_LT = (196, 64, 58)
NAVY = (28, 42, 66)          # lead illustration sky
SEA = (64, 96, 122)
SAND = (214, 196, 150)
MAP_LAND = (206, 192, 158)
MAP_SEA = (214, 226, 232)
GOLD = (176, 132, 44)

FD = "/usr/share/fonts/truetype/dejavu"
F_SERIF_B = f"{FD}/DejaVuSerif-Bold.ttf"
F_SANS_B = f"{FD}/DejaVuSans-Bold.ttf"
F_SANS = f"{FD}/DejaVuSans.ttf"
F_SERIF = f"{FD}/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# Fields: n, kind, headline, subhead, place, b_head (short headline for
# the 6-column variant B grid, max 36 chars).
LEAD = {
    "n": 1, "kind": "lead",
    "headline": "Iran strikes US bases in Bahrain",
    "subhead": ("IRGC claims hits on two Patriot radars at al-Riffa and Awali; "
                "Bahrain reports fire at an industrial site."),
    "place": "MANAMA, BAHRAIN",
}

ILLUSTRATED = [
    {"n": 2, "kind": "mexico",
     "headline": "Mexico captures 'El Chapo Isidro'",
     "subhead": "FBI most-wanted boss seized in Guasave; 11 dead in gun battles.",
     "place": "GUASAVE, MEXICO", "b_head": "Mexico captures 'El Chapo Isidro'"},
    {"n": 3, "kind": "cop",
     "headline": "COP31 talks run into overtime",
     "subhead": "Draft drops 'fossil fuels'; EU says good deal or no deal at all.",
     "place": "ANTALYA, TURKIYE", "b_head": "COP31 talks run into overtime"},
    {"n": 4, "kind": "kryvyi",
     "headline": "Russian missile hits Zelensky's hometown",
     "subhead": "Two killed, about 60 hurt in Kryvyi Rih; a boy of 7 among the dead.",
     "place": "KRYVYI RIH, UKRAINE", "b_head": "Missile hits Zelensky's hometown"},
    {"n": 5, "kind": "peru",
     "headline": "Magnitude 6.7 quake shakes Peru",
     "subhead": "One dead, 16 hurt near Junin; 152 homes left uninhabitable.",
     "place": "JUNIN, PERU", "b_head": "Magnitude 6.7 quake shakes Peru"},
    {"n": 6, "kind": "stocks",
     "headline": "AI sell-off rattles world markets",
     "subhead": "S&P 500 falls 3.7%; Nasdaq erases its 2026 gains; Nikkei down 5%.",
     "place": "NEW YORK, USA", "b_head": "AI sell-off rattles markets"},
    {"n": 7, "kind": "summit",
     "headline": "Trump defends Putin ties at summit",
     "subhead": "Three-way talks with Xi; Zelensky calls Putin a killer.",
     "place": "SHENZHEN, CHINA", "b_head": "Trump defends Putin ties"},
    {"n": 8, "kind": "riemann",
     "headline": "Mathematician claims Riemann proof",
     "subhead": "Levent Alpoge says AI helped him solve the 160-year-old problem.",
     "place": "SAN FRANCISCO, USA", "b_head": "Mathematician claims Riemann proof"},
    {"n": 9, "kind": "icj",
     "headline": "UN court: Myanmar guilty of genocide",
     "subhead": "First time the court holds a state responsible, over the Rohingya.",
     "place": "THE HAGUE, NETHERLANDS", "b_head": "Myanmar guilty of genocide"},
    {"n": 10, "kind": "sparta",
     "headline": "Drones hit Russian ship in Baltic",
     "subhead": "Cargo ship Sparta II catches fire in the Gulf of Finland.",
     "place": "GULF OF FINLAND", "b_head": "Drones hit Russian ship"},
    {"n": 11, "kind": "gaza",
     "headline": "Israeli strike kills three in Gaza",
     "subhead": "Food vehicle hit in Gaza City; Israel says victims were militants.",
     "place": "GAZA CITY", "b_head": "Strike kills three in Gaza"},
    {"n": 12, "kind": "mercury",
     "headline": "BepiColombo reaches Mercury orbit",
     "subhead": "European-Japanese craft ends an eight-year, 10-billion-km journey.",
     "place": "MERCURY ORBIT", "b_head": "BepiColombo reaches Mercury"},
    {"n": 13, "kind": "basra",
     "headline": "Fire at Basra power station kills four",
     "subhead": "Blaze at Iraqi plant leaves 35 hurt and strains the power grid.",
     "place": "BASRA, IRAQ", "b_head": "Basra power station fire kills 4"},
]

COMPACT = [
    (14, "Houthis, Saudis trade blows", "Three missiles at Riyadh stopped"),
    (15, "EU-Indonesia sign trade deal", "98.5% of tariffs on EU goods go"),
    (16, "Trump vows data-centre tax", "Firms building AI hubs abroad"),
    (17, "FBI crime database 'hacked'", "Police records system breached"),
    (18, "UN to keep AI weapons talks", "100 states back rules by 2028"),
    (19, "Measles kills Virginia child", "US lost elimination status"),
    (20, "Dengue cut by mosquitoes", "Wolbachia trial shields children"),
    (21, "Bolsonaro in intensive care", "Bowel obstruction, doctors say"),
    (22, "Nigeria boat sinks, 24 dead", "Mourners capsize in Bayelsa"),
    (23, "Saudi, Japan agree oil deal", "Stockpile in Japan to triple"),
    (24, "Gulf economies hit by war", "Recession as Hormuz is disrupted"),
    (25, "Argentina bonds in distress", "First time in two years"),
    (26, "Gupta jailed 19 years in US", "Plot to kill Sikh leader in NY"),
    (27, "Uganda curbs over Ebola", "Congo outbreak may be worst yet"),
    (28, "Fighting widens in E. Congo", "Truce at risk as rebels return"),
    (29, "GTA VI earns $3.8bn in a day", "Biggest entertainment launch ever"),
    (30, "CERN finds ultra-rare decay", "First evidence of rare particle"),
    (31, "700,000 flee in S. Ethiopia", "Troops mass on Eritrea border"),
    (32, "Voyager 1 farthest ever", "Now 24 light-hours from Earth"),
    (33, "M6.8 quake strikes off Timor", "Sea north-east of Dili shakes"),
    (34, "England beat All Blacks 37-12", "Record margin at Twickenham"),
    (35, "BTS win five at MAMA Awards", "K-pop night in Osaka, Japan"),
    (36, "Java factory fire kills 3", "Dozens missing after candy blaze"),
    (37, "Iran to ration electricity", "Rolling cuts from Sunday, 2 hours"),
]

MARKETS = ("MARKETS - 21 NOV", "S&P 500 -3.7%  ·  Nasdaq wipes out 2026 gains",
           "Nikkei -5.1%  ·  Brent $89.95  ·  Gold -4.6%")

TOTAL_STORIES = 37


# ---------------------------------------------------------------- helpers
def wrap(d, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, fnt, fill=INK, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def panel(d, box, fill=PAPER2, outline=LINE, width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)


def num_badge(d, cx, cy, n, r=11, size=None):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=1)
    f = font(F_SANS_B, size if size else (13 if n < 10 else 11))
    d.text((cx, cy), str(n), font=f, fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- scenes
def scene_bahrain(d, x, y, w, h):
    """Night over the Gulf: missile arcs, island, refinery, tanker."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy, r in [(0.12, 0.18, 2), (0.3, 0.1, 1), (0.55, 0.22, 2),
                      (0.72, 0.08, 1), (0.88, 0.16, 2), (0.45, 0.3, 1)]:
        d.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r, y + sy * h + r],
                  fill=(220, 220, 200))
    # missile arcs
    for x0, x1, peak in [(0.08, 0.42, 0.22), (0.55, 0.9, 0.16)]:
        pts = []
        for i in range(21):
            t = i / 20.0
            px = x + (x0 + (x1 - x0) * t) * w
            py = y + (0.78 - math.sin(t * math.pi) * peak * 3.2) * h
            pts.append((px, py))
        d.line(pts, fill=(255, 176, 66), width=3)
        d.line(pts, fill=(255, 120, 40), width=1)
        hx, hy = pts[-1]
        d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(255, 200, 90))
    # sea
    d.rectangle([x, y + int(h * 0.78), x + w, y + h], fill=SEA)
    d.line([x, y + int(h * 0.78), x + w, y + int(h * 0.78)], fill=(140, 180, 200), width=1)
    # island + refinery
    ix, iy = x + int(w * 0.60), y + int(h * 0.62)
    d.polygon([(ix, iy), (ix + 150, iy), (ix + 165, y + int(h * 0.80)),
               (ix - 15, y + int(h * 0.80))], fill=(52, 66, 52))
    for tx in (ix + 22, ix + 52, ix + 82):
        d.rectangle([tx, iy - 26, tx + 8, iy + 4], fill=(40, 40, 36))
        d.ellipse([tx + 1, iy - 32, tx + 7, iy - 26], fill=(255, 150, 50))
    # explosion burst on island
    bx, by = ix + 120, iy - 6
    for ang in range(0, 360, 45):
        ex = bx + int(16 * math.cos(math.radians(ang)))
        ey = by + int(10 * math.sin(math.radians(ang)))
        d.line([bx, by, ex, ey], fill=(255, 190, 80), width=3)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 220, 120))
    # tanker
    tx0, ty0 = x + int(w * 0.10), y + int(h * 0.82)
    d.rectangle([tx0, ty0, tx0 + 120, ty0 + 14], fill=(30, 30, 30))
    d.rectangle([tx0 + 88, ty0 - 12, tx0 + 112, ty0], fill=(30, 30, 30))
    d.rectangle([tx0 + 92, ty0 - 20, tx0 + 96, ty0 - 12], fill=(200, 60, 50))


def scene_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 196, 138))
    d.ellipse([x + int(w * 0.78), y + int(h * 0.08), x + int(w * 0.94), y + int(h * 0.38)],
              fill=(240, 180, 80))
    d.polygon([(x, y + h), (x + int(w * 0.35), y + int(h * 0.55)),
               (x + int(w * 0.7), y + h)], fill=(196, 148, 92))
    d.polygon([(x + int(w * 0.5), y + h), (x + w, y + int(h * 0.62)), (x + w, y + h)],
              fill=(180, 132, 80))
    # cactus
    cx, cy = x + int(w * 0.14), y + int(h * 0.55)
    d.rectangle([cx, cy, cx + 8, y + h], fill=(74, 120, 66))
    d.rectangle([cx - 12, cy + 12, cx, cy + 22], fill=(74, 120, 66))
    d.rectangle([cx - 12, cy + 12, cx - 4, cy + 34], fill=(74, 120, 66))
    # helicopter
    hx, hy = x + int(w * 0.55), y + int(h * 0.22)
    d.ellipse([hx, hy, hx + 34, hy + 14], fill=(40, 40, 40))
    d.rectangle([hx + 30, hy + 5, hx + 52, hy + 9], fill=(40, 40, 40))
    d.line([hx + 4, hy - 6, hx + 30, hy - 6], fill=(40, 40, 40), width=2)
    d.line([hx + 17, hy + 14, hx + 17, hy + 26], fill=(40, 40, 40), width=2)


def scene_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(176, 214, 228))
    d.ellipse([x + int(w * 0.72), y + int(h * 0.06), x + int(w * 0.92), y + int(h * 0.42)],
              fill=(250, 200, 90))
    # globe
    gx, gy, gr = x + int(w * 0.30), y + int(h * 0.52), int(h * 0.34)
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 120, 170),
              outline=(255, 255, 255), width=2)
    d.ellipse([gx - int(gr * 0.55), gy - int(gr * 0.5), gx - int(gr * 0.1), gy + int(gr * 0.1)],
              fill=(96, 160, 96))
    d.ellipse([gx + int(gr * 0.05), gy + int(gr * 0.15), gx + int(gr * 0.6), gy + int(gr * 0.55)],
              fill=(96, 160, 96))
    # hills + turbines
    d.polygon([(x, y + h), (x + int(w * 0.4), y + int(h * 0.72)), (x + int(w * 0.8), y + h)],
              fill=(96, 160, 96))
    for tx in (0.62, 0.82):
        px, py = x + int(tx * w), y + int(h * 0.78)
        d.line([px, py, px, py - 26], fill=(255, 255, 255), width=2)
        for ang in (90, 210, 330):
            ex = px + int(12 * math.cos(math.radians(ang)))
            ey = py - 26 + int(12 * math.sin(math.radians(ang)))
            d.line([px, py - 26, ex, ey], fill=(255, 255, 255), width=2)


def scene_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 48, 66))
    d.ellipse([x + int(w * 0.8), y + int(h * 0.1), x + int(w * 0.9), y + int(h * 0.28)],
              fill=(220, 210, 190))
    # skyline
    for bx, bw, bh in [(0.02, 0.16, 0.42), (0.2, 0.12, 0.55), (0.34, 0.18, 0.38),
                       (0.54, 0.14, 0.5), (0.7, 0.16, 0.44), (0.88, 0.1, 0.36)]:
        d.rectangle([x + bx * w, y + h - int(bh * h), x + (bx + bw) * w, y + h],
                    fill=(30, 28, 40))
        for wy in range(2):
            for wx in range(2):
                d.rectangle([x + (bx + 0.03 + wx * 0.05) * w,
                             y + h - int(bh * h) + 6 + wy * 12,
                             x + (bx + 0.05 + wx * 0.05) * w,
                             y + h - int(bh * h) + 10 + wy * 12], fill=(250, 200, 90))
    # explosion
    bx, by = x + int(w * 0.45), y + int(h * 0.42)
    for ang in range(0, 360, 30):
        ex = bx + int(20 * math.cos(math.radians(ang)))
        ey = by + int(13 * math.sin(math.radians(ang)))
        d.line([bx, by, ex, ey], fill=(255, 150, 40), width=3)
    d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(255, 210, 90))
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 240, 180))


def scene_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 200, 222))
    # mountains
    d.polygon([(x, y + h), (x + int(w * 0.28), y + int(h * 0.25)), (x + int(w * 0.55), y + h)],
              fill=(90, 110, 130))
    d.polygon([(x + int(w * 0.2), y + int(h * 0.25)), (x + int(w * 0.28), y + int(h * 0.25)),
               (x + int(w * 0.36), y + int(h * 0.25)), (x + int(w * 0.28), y + int(h * 0.42))],
              fill=(240, 244, 248))
    d.polygon([(x + int(w * 0.45), y + h), (x + int(w * 0.72), y + int(h * 0.32)),
               (x + w, y + h)], fill=(70, 92, 112))
    d.polygon([(x + int(w * 0.64), y + int(h * 0.32)), (x + int(w * 0.72), y + int(h * 0.32)),
               (x + int(w * 0.8), y + int(h * 0.32)), (x + int(w * 0.72), y + int(h * 0.48))],
              fill=(240, 244, 248))
    # seismograph strip
    sy = y + int(h * 0.74)
    d.rectangle([x + 6, sy - 8, x + w - 6, sy + 12], fill=(255, 255, 255),
                outline=INK, width=1)
    pts = []
    for i in range(41):
        px = x + 10 + i * (w - 20) / 40.0
        amp = [0, 0, 2, -2, 1, 0, 0, 6, -9, 12, -7, 3, 0, 0, 4, -6, 9, -4, 1, 0,
               0, 3, -3, 2, 0, 0, 8, -11, 14, -9, 4, 0, 0, 2, -2, 1, 0, 0, 0, 0, 0][i]
        pts.append((px, sy + amp))
    d.line(pts, fill=RED, width=2)


def scene_stocks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # grid
    for gy in range(1, 4):
        d.line([x + 6, y + gy * h / 4, x + w - 6, y + gy * h / 4], fill=(226, 226, 226), width=1)
    # candles
    cw = int(w * 0.09)
    for i, (cx, top, bot, up) in enumerate([(0.1, 0.3, 0.5, True), (0.26, 0.36, 0.58, False),
                                            (0.42, 0.5, 0.72, False), (0.58, 0.62, 0.82, False),
                                            (0.74, 0.68, 0.9, False)]):
        px = x + cx * w
        col = (60, 140, 80) if up else RED
        d.line([px + cw / 2, y + top * h - 6, px + cw / 2, y + bot * h + 6], fill=col, width=2)
        d.rectangle([px, y + top * h, px + cw, y + bot * h], fill=col)
    # down arrow
    d.line([(x + int(w * 0.08), y + int(h * 0.22)), (x + int(w * 0.9), y + int(h * 0.82))],
           fill=RED, width=4)
    d.polygon([(x + int(w * 0.9), y + int(h * 0.82)), (x + int(w * 0.78), y + int(h * 0.78)),
               (x + int(w * 0.88), y + int(h * 0.66))], fill=RED)


def scene_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 208, 224))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(150, 120, 84))
    # table
    d.rectangle([x + int(w * 0.18), y + int(h * 0.66), x + int(w * 0.82), y + int(h * 0.74)],
                fill=(120, 84, 56))
    # three flags
    flags = [("US", (200, 60, 60)), ("CN", (220, 40, 40)), ("RU", (40, 80, 160))]
    for i, (code, col) in enumerate(flags):
        px = x + int((0.2 + i * 0.3) * w)
        d.line([px, y + int(h * 0.18), px, y + int(h * 0.68)], fill=INK, width=2)
        if code == "US":
            d.rectangle([px, y + int(h * 0.18), px + 34, y + int(h * 0.38)], fill=(200, 60, 60))
            for sy in range(4):
                d.rectangle([px, y + int(h * 0.18) + sy * 5, px + 34, y + int(h * 0.18) + sy * 5 + 2],
                            fill=(255, 255, 255))
            d.rectangle([px, y + int(h * 0.18), px + 14, y + int(h * 0.18) + 9], fill=(40, 60, 140))
        elif code == "CN":
            d.rectangle([px, y + int(h * 0.18), px + 34, y + int(h * 0.38)], fill=(220, 40, 40))
            d.ellipse([px + 4, y + int(h * 0.2), px + 12, y + int(h * 0.28)], fill=(250, 220, 60))
        else:
            for j, c in enumerate([(255, 255, 255), (40, 80, 180), (200, 40, 40)]):
                d.rectangle([px, y + int(h * 0.18) + j * 7, px + 34, y + int(h * 0.18) + (j + 1) * 7],
                            fill=c)


def scene_riemann(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 84, 62))
    d.rectangle([x + 4, y + 4, x + w - 4, y + h - 4], outline=(150, 130, 90), width=2)
    f = font(F_SERIF, max(13, int(h * 0.24)))
    while d.textlength("ζ(s) = Σ 1/nˢ", font=f) > w - 10 and f.size > 8:
        f = font(F_SERIF, f.size - 1)
    d.text((x + w / 2, y + int(h * 0.30)), "ζ(s) = Σ 1/nˢ", font=f,
           fill=(245, 245, 235), anchor="mm")
    f2 = font(F_SERIF, max(11, int(h * 0.17)))
    while d.textlength("Re(s) = ½  ·  all non-trivial zeros", font=f2) > w - 10 and f2.size > 8:
        f2 = font(F_SERIF, f2.size - 1)
    d.text((x + w / 2, y + int(h * 0.62)), "Re(s) = ½  ·  all non-trivial zeros",
           font=f2, fill=(220, 220, 205), anchor="mm")
    d.line([x + int(w * 0.2), y + int(h * 0.82), x + int(w * 0.8), y + int(h * 0.82)],
           fill=(245, 245, 235), width=1)


def scene_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 52, 86))
    cx, cy = x + w / 2, y + int(h * 0.3)
    d.line([cx, cy, cx, y + int(h * 0.78)], fill=GOLD, width=3)
    d.line([cx - int(w * 0.3), cy, cx + int(w * 0.3), cy], fill=GOLD, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    for sx in (-1, 1):
        px = cx + sx * int(w * 0.3)
        d.line([px, cy, px, cy + 16], fill=GOLD, width=2)
        d.arc([px - 18, cy + 12, px + 18, cy + 44], 0, 180, fill=GOLD, width=3)
        d.line([px - 18, cy + 28, px + 18, cy + 28], fill=GOLD, width=3)
    d.rectangle([cx - 22, y + int(h * 0.78), cx + 22, y + int(h * 0.84)], fill=GOLD)


def scene_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 180, 205))
    d.ellipse([x + int(w * 0.76), y + int(h * 0.06), x + int(w * 0.9), y + int(h * 0.3)],
              fill=(250, 230, 170))
    # sea
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(52, 96, 138))
    for wy in (0.62, 0.78, 0.92):
        for wx in range(0, 10):
            px = x + wx * w / 10
            d.arc([px, y + wy * h - 4, px + 16, y + wy * h + 4], 180, 360,
                  fill=(180, 210, 230), width=2)
    # ship
    sx, sy = x + int(w * 0.18), y + int(h * 0.5)
    d.polygon([(sx, sy), (sx + int(w * 0.6), sy), (sx + int(w * 0.52), sy + 16),
               (sx + 8, sy + 16)], fill=(40, 40, 44))
    d.rectangle([sx + int(w * 0.3), sy - 14, sx + int(w * 0.42), sy], fill=(200, 200, 200))
    # smoke + fire on ship (kept inside the box)
    for i, r in enumerate((3, 5, 7)):
        d.ellipse([sx + int(w * 0.34) - r, sy - 10 - i * 4 - r, sx + int(w * 0.34) + r,
                   sy - 10 - i * 4 + r], fill=(120, 120, 120))
    d.polygon([(sx + int(w * 0.34), sy - 24), (sx + int(w * 0.3), sy - 10),
               (sx + int(w * 0.38), sy - 10)], fill=(255, 150, 40))
    # drone
    dx, dy = x + int(w * 0.74), y + int(h * 0.24)
    d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=(30, 30, 30))
    d.line([dx - 10, dy - 4, dx + 10, dy - 4], fill=(30, 30, 30), width=2)
    d.line([dx - 10, dy + 4, dx + 10, dy + 4], fill=(30, 30, 30), width=2)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 200, 160))
    d.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(190, 160, 120))
    # buildings
    for bx, bw, bh in [(0.05, 0.2, 0.4), (0.3, 0.16, 0.52), (0.5, 0.22, 0.36), (0.76, 0.18, 0.46)]:
        d.rectangle([x + bx * w, y + int(h * 0.68) - int(bh * h * 0.6),
                     x + (bx + bw) * w, y + int(h * 0.68)], fill=(150, 128, 100))
    # aid truck
    tx, ty = x + int(w * 0.18), y + int(h * 0.56)
    d.rectangle([tx, ty, tx + int(w * 0.5), ty + 18], fill=(240, 240, 235),
                outline=INK, width=1)
    d.rectangle([tx + int(w * 0.5), ty + 4, tx + int(w * 0.62), ty + 18], fill=(200, 60, 50))
    d.ellipse([tx + 8, ty + 18, tx + 20, ty + 30], fill=(30, 30, 30))
    d.ellipse([tx + int(w * 0.5), ty + 18, tx + int(w * 0.5) + 12, ty + 30], fill=(30, 30, 30))
    d.text((tx + int(w * 0.25), ty + 9), "+", font=font(F_SANS_B, 14), fill=RED, anchor="mm")


def scene_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 28))
    for sx, sy in [(0.1, 0.15), (0.25, 0.3), (0.85, 0.12), (0.92, 0.5), (0.15, 0.7), (0.6, 0.85)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1],
                  fill=(255, 255, 255))
    # Mercury
    mx, my, mr = x + int(w * 0.32), y + int(h * 0.55), int(h * 0.32)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(168, 152, 132))
    for cx, cy, cr in [(-0.4, -0.3, 0.16), (0.3, 0.1, 0.2), (-0.1, 0.4, 0.12), (0.45, -0.35, 0.1)]:
        d.ellipse([mx + cx * mr - cr * mr, my + cy * mr - cr * mr,
                   mx + cx * mr + cr * mr, my + cy * mr + cr * mr], fill=(140, 126, 108))
    # spacecraft
    sx, sy = x + int(w * 0.68), y + int(h * 0.34)
    d.rectangle([sx - 8, sy - 6, sx + 8, sy + 6], fill=(200, 200, 210), outline=INK, width=1)
    d.rectangle([sx - 30, sy - 4, sx - 10, sy + 4], fill=(60, 90, 180))
    d.rectangle([sx + 10, sy - 4, sx + 30, sy + 4], fill=(60, 90, 180))
    d.line([sx, sy + 6, sx, sy + 14], fill=(200, 200, 210), width=2)


def scene_basra(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 168))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(170, 150, 120))
    # cooling towers
    for tx, tw in [(0.12, 0.2), (0.42, 0.22), (0.7, 0.18)]:
        px = x + tx * w
        d.polygon([(px, y + int(h * 0.72)), (px + 4, y + int(h * 0.3)),
                   (px + tw * w - 4, y + int(h * 0.3)), (px + tw * w, y + int(h * 0.72))],
                  fill=(200, 190, 170), outline=(120, 110, 95), width=1)
        d.ellipse([px + 2, y + int(h * 0.28), px + tw * w - 2, y + int(h * 0.36)],
                  fill=(120, 110, 95))
    # flames + smoke (kept inside the box)
    fx, fy = x + int(w * 0.52), y + int(h * 0.62)
    d.polygon([(fx - 8, fy), (fx, fy - 18), (fx + 8, fy)], fill=(255, 150, 40))
    d.polygon([(fx - 4, fy), (fx, fy - 10), (fx + 4, fy)], fill=(255, 220, 90))
    for i, r in enumerate((4, 6, 8)):
        d.ellipse([fx + 26 - r, fy - 12 - i * 5 - r, fx + 26 + r, fy - 12 - i * 5 + r],
                  fill=(110, 110, 110))


SCENES = {
    "lead": scene_bahrain, "mexico": scene_mexico, "cop": scene_cop,
    "kryvyi": scene_kryvyi, "peru": scene_peru, "stocks": scene_stocks,
    "summit": scene_summit, "riemann": scene_riemann, "icj": scene_icj,
    "sparta": scene_sparta, "gaza": scene_gaza, "mercury": scene_mercury,
    "basra": scene_basra,
}


# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
     (-65, 45), (-80, 32), (-90, 21), (-105, 20), (-115, 28), (-125, 40),
     (-145, 60), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-58, 76)],
    # South America
    [(-80, 10), (-70, 12), (-55, 5), (-35, -8), (-40, -22), (-55, -35),
     (-70, -52), (-73, -40), (-75, -20), (-80, -5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 11), (40, 0), (35, -18), (28, -33), (18, -35), (12, -18), (8, 4), (-8, 5)],
    # Eurasia
    [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (10, 57), (18, 56),
     (21, 60), (28, 71), (40, 68), (55, 70), (70, 73), (90, 75), (110, 76),
     (130, 72), (160, 70), (178, 66), (170, 60), (160, 52), (142, 50),
     (140, 40), (130, 35), (120, 22), (108, 12), (100, 8), (95, 16),
     (80, 8), (72, 20), (60, 25), (52, 27), (48, 30), (43, 36), (36, 36),
     (30, 36), (22, 38), (12, 44), (0, 40)],
    # SE Asia islands
    [(95, 5), (104, 2), (110, -4), (118, -6), (126, -4), (132, -2), (140, -8),
     (138, -2), (128, 2), (118, 6), (104, 8)],
    # Australia
    [(113, -22), (114, -30), (124, -33), (135, -35), (142, -38), (150, -37),
     (153, -28), (146, -19), (142, -11), (135, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # UK
    [(-5, 50), (-2, 53), (-1, 58), (-4, 58), (-5, 54)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44), (140, 40),
     (136, 35), (132, 33)],
]

PINS = [  # story number, lon, lat, label offset px (0,0 = badge on the dot)
    (1, 50.5, 26.2, 18, 24), (2, -108.5, 25.6, -8, 20), (3, 30.7, 36.9, -22, 26),
    (4, 33.4, 47.9, 26, -14), (5, -76.0, -11.0, 0, 0), (6, -74.0, 40.7, 0, 0),
    (7, 114.0, 22.5, 0, 0), (8, -122.4, 37.8, -18, -14), (9, 4.3, 52.1, -20, -12),
    (10, 26.0, 60.0, 4, -18), (11, 34.5, 31.5, 12, 16), (13, 47.8, 30.5, 26, 2),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MAP_SEA)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360.0 * w, y + (85 - lat) / 140.0 * h)
               for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=(150, 138, 110))
    for n, lon, lat, dx, dy in PINS:
        px = x + (lon + 180) / 360.0 * w
        py = y + (85 - lat) / 140.0 * h
        bx, by = px + dx, py + dy
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=(255, 255, 255), width=1)
        if dx or dy:
            d.line([px, py, bx, by], fill=GREY, width=1)
        num_badge(d, bx, by, n, r=8, size=10)


# ---------------------------------------------------------------- variant A
MX = 14                      # side margin
CW = 243                     # grid column width
CG = 8                       # grid column gap
COL_X = [MX, MX + CW + CG, MX + 2 * (CW + CG), MX + 3 * (CW + CG)]


def masthead(d):
    f_title = font(F_SERIF_B, 52)
    d.text((W / 2, 6), "THE WORLD IN ONE DAY", font=f_title, fill=INK, anchor="ma")
    d.rectangle([MX, 62, W - MX, 65], fill=RED)
    f_date = font(F_SANS_B, 21)
    d.text((MX, 69), "SATURDAY 21 NOVEMBER 2026", font=f_date, fill=INK)
    f_meta = font(F_SANS_B, 13)
    d.text((W - MX, 72), "37 STORIES  ·  9 REGIONS  ·  ALL REPORTED 21 NOV",
           font=f_meta, fill=GREY, anchor="ra")


def lead_panel(d):
    x0, y0, x1, y1 = MX, 88, 634, 326
    panel(d, [x0, y0, x1, y1], fill=PAPER2)
    SCENES["lead"](d, x0 + 4, y0 + 4, 612, 136)
    num_badge(d, x0 + 22, y0 + 22, 1, r=12)
    f_kick = font(F_SANS_B, 12)
    d.text((x0 + 4, y0 + 146), "LEAD  ·  " + LEAD["place"], font=f_kick, fill=RED)
    f_head = font(F_SERIF_B, 26)
    d.text((x0 + 4, y0 + 162), LEAD["headline"], font=f_head, fill=INK)
    f_sub = font(F_SANS, 14)
    for i, ln in enumerate(wrap(d, LEAD["subhead"], f_sub, 612)):
        d.text((x0 + 4, y0 + 196 + i * 17), ln, font=f_sub, fill=INK)


def map_panel(d):
    x0, y0, x1, y1 = 642, 88, 1010, 232
    panel(d, [x0, y0, x1, y1], fill=PAPER2)
    draw_map(d, x0 + 4, y0 + 4, 360, 118)
    f_cap = font(F_SANS_B, 10)
    d.text((x0 + 4, y1 - 16), "WORLD MAP — PINS MARK THE ILLUSTRATED STORIES",
           font=f_cap, fill=GREY)


def mexico_mini(d):
    s = ILLUSTRATED[0]
    x0, y0, x1, y1 = 642, 238, 1010, 326
    panel(d, [x0, y0, x1, y1], fill=PAPER2)
    SCENES["mexico"](d, x0 + 4, y0 + 4, 100, 80)
    num_badge(d, x0 + 16, y0 + 16, 2, r=11)
    tx = x0 + 112
    f_kick = font(F_SANS_B, 11)
    d.text((tx, y0 + 6), "2  ·  " + s["place"], font=f_kick, fill=RED)
    f_head = font(F_SANS_B, 17)
    lines = wrap(d, s["headline"], f_head, x1 - tx - 4)
    for i, ln in enumerate(lines[:2]):
        d.text((tx, y0 + 22 + i * 18), ln, font=f_head, fill=INK)
    f_sub = font(F_SANS, 12)
    slines = wrap(d, s["subhead"], f_sub, x1 - tx - 4)
    for i, ln in enumerate(slines[:2]):
        d.text((tx, y0 + 59 + i * 13), ln, font=f_sub, fill=GREY)


def grid_cell(d, x, y, story):
    panel(d, [x, y, x + CW, y + 128], fill=PAPER2)
    SCENES[story["kind"]](d, x + 4, y + 4, CW - 8, 50)
    num_badge(d, x + 16, y + 16, story["n"], r=11)
    f_head = font(F_SANS_B, 17)
    lines = wrap(d, story["headline"], f_head, CW - 8)
    hy = y + 58
    for i, ln in enumerate(lines[:2]):
        d.text((x + 4, hy + i * 18), ln, font=f_head, fill=INK)
    f_sub = font(F_SANS, 12)
    slines = wrap(d, story["subhead"], f_sub, CW - 8)
    sy = hy + len(lines[:2]) * 18 + 2
    for i, ln in enumerate(slines[:2]):
        d.text((x + 4, sy + i * 13), ln, font=f_sub, fill=GREY)


def markets_cell(d, x, y):
    d.rectangle([x, y, x + CW, y + 128], fill=INK)
    f_t = font(F_SANS_B, 13)
    d.text((x + 10, y + 8), MARKETS[0], font=f_t, fill=(240, 200, 90))
    f_l = font(F_SANS, 12)
    for i, ln in enumerate(wrap(d, MARKETS[1], f_l, CW - 20)):
        d.text((x + 10, y + 30 + i * 15), ln, font=f_l, fill=(235, 235, 230))
    for i, ln in enumerate(wrap(d, MARKETS[2], f_l, CW - 20)):
        d.text((x + 10, y + 62 + i * 15), ln, font=f_l, fill=(235, 235, 230))
    # down arrow
    ax, ay = x + CW - 34, y + 96
    d.line([(ax, ay), (ax + 22, ay + 22)], fill=RED_LT, width=4)
    d.polygon([(ax + 22, ay + 22), (ax + 10, ay + 20), (ax + 20, ay + 8)], fill=RED_LT)


def compact_cell(d, x, y, n, headline, subhead):
    f_num = font(F_SANS_B, 14)
    d.text((x, y + 1), str(n), font=f_num, fill=RED)
    f_head = font(F_SANS_B, 13)
    d.text((x + 24, y + 2), headline, font=f_head, fill=INK)
    f_sub = font(F_SANS, 12)
    d.text((x + 24, y + 19), subhead, font=f_sub, fill=GREY)
    d.line([x, y + 37, x + CW, y + 37], fill=LINE, width=1)


def bottom_band(d):
    d.rectangle([0, 995, W, H], fill=INK)
    f = font(F_SANS_B, 13)
    d.text((W / 2, 1003), "ALL 37 STORIES WERE REPORTED ON SATURDAY 21 NOVEMBER 2026  ·  "
           "SOURCES: REUTERS, AP, BBC, AFP, UPI, CNN",
           font=f, fill=(240, 236, 224), anchor="ma")


def render_a(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead_panel(d)
    map_panel(d)
    mexico_mini(d)
    grid_stories = ILLUSTRATED[1:]  # 11 stories + markets box = 12 cells
    rows_y = [332, 466, 600]
    cells = grid_stories + [None]
    for i, story in enumerate(cells):
        x = COL_X[i % 4]
        y = rows_y[i // 4]
        if story is None:
            markets_cell(d, x, y)
        else:
            grid_cell(d, x, y, story)
    compact_rows_y = [734, 777, 820, 863, 906, 949]
    for i, (n, headline, subhead) in enumerate(COMPACT):
        x = COL_X[i % 4]
        y = compact_rows_y[i // 4]
        compact_cell(d, x, y, n, headline, subhead)
    bottom_band(d)
    img.save(path, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render_a(out)
    print("wrote", out)
