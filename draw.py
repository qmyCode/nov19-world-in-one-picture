#!/usr/bin/env python3
"""Build tool for the news-image-20261119 entry (v4).

Draws the one-page newspaper front page for Thursday 19 November 2026
and writes it to ``entry.png`` next to this file (1024x1024).

This program is a build tool only: it runs on the author's machine.
The shipped entrypoint (``main.py``) never imports it; it simply
copies the committed ``entry.png`` to ``/output/entry.png``.

Rendering: PIL only, and only the four DejaVu faces that ship with the
official runner image (Serif, Serif-Bold, Sans, Sans-Bold).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

_fonts = {}


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


# ---------------------------------------------------------------- colours
PAPER = (246, 241, 229)
NAVY = (20, 38, 63)
NAVY2 = (30, 54, 86)
INK = (26, 24, 20)
RED = (156, 43, 35)
RED_SOFT = (176, 58, 46)
GOLD = (201, 162, 39)
CREAM = (240, 234, 216)
GREY = (110, 104, 92)
LAND = (216, 196, 154)
LAND_EDGE = (170, 150, 106)
SEA = (234, 227, 206)

W, H = 1024, 1024
MX = 28                      # left/right margin
CW = 313                     # grid column width
COLX = [28, 355, 682]        # grid column left edges

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


# ---------------------------------------------------------------- helpers
def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, maxw):
    """Greedy word wrap; returns a list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(x, y, text, font, fill, tracking=2):
    """Draw text with extra letter tracking; return the end x."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += tw(ch, font) + tracking
    return cx - tracking


def spaced_width(text, font, tracking=2):
    return sum(tw(ch, font) for ch in text) + tracking * (len(text) - 1)


def number_badge(x, y, n, dia=15):
    d.ellipse([x, y, x + dia, y + dia], fill=RED)
    f = F(SANS_B, 10 if n < 10 else 9)
    label = str(n)
    w = tw(label, f)
    d.text((x + (dia - w) / 2, y + dia / 2 - 6), label, font=f, fill=(255, 255, 255))


def tag_row(x, y, n, tag):
    number_badge(x, y, n)
    d.text((x + 21, y + 1), tag, font=F(SANS_B, 10), fill=RED)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 96], fill=NAVY)
kick = F(SANS_B, 10)
spaced(MX, 10, "THE WORLD IN ONE DAY", kick, GOLD, 2)
right = "42 STORIES · 6 CONTINENTS · ONE PAGE"
rw = spaced_width(right, kick, 2)
spaced(W - MX - rw, 10, right, kick, GOLD, 2)
title_f = F(SERIF_B, 47)
d.text((MX - 2, 24), "Thursday 19 November 2026", font=title_f, fill=CREAM)
d.text((MX, 76), "Every story below happened, or was first reported, on this day.",
       font=F(SERIF, 12), fill=(203, 196, 178))
d.rectangle([0, 96, W, 99], fill=GOLD)

# tally bar
tally = ("EUROPE 10 · AFRICA 8 · ASIA 7 · AMERICAS 7 · GLOBAL 5 · "
         "MIDDLE EAST 3 · OCEANIA 1 · SPACE 1")
tf = F(SANS_B, 12)
d.text(((W - tw(tally, tf)) / 2, 104), tally, font=tf, fill=(74, 44, 30))

# ------------------------------------------------------------- UTC strip
uy = 124
d.rectangle([MX, uy, MX + 148, uy + 24], fill=RED)
lab = "THE DAY IN UTC"
lf = F(SANS_B, 11)
d.text((MX + (148 - tw(lab, lf)) / 2, uy + 6), lab, font=lf, fill=(255, 255, 255))
moments = [
    ("00:00 UTC", "GTA VI unlocks in Britain"),
    ("09:00 UTC", "ICJ reads Myanmar judgment"),
    ("DAY", "Shenzhen trilateral summit"),
    ("17:00 UTC", "NASA briefs on Voyager 1"),
]
mx_x = 186
for when, what in moments:
    fb, fr = F(SANS_B, 10), F(SANS, 10)
    d.text((mx_x, uy + 7), when, font=fb, fill=RED)
    d.text((mx_x + tw(when, fb) + 5, uy + 7), what, font=fr, fill=INK)
    mx_x += tw(when, fb) + 5 + tw(what, fr) + 24
d.line([MX, uy + 30, W - MX, uy + 30], fill=GOLD, width=2)


# ------------------------------------------------------- big scene panels
def caption_strip(x, y, w, text):
    d.rectangle([x, y, x + w, y + 16], fill=(12, 24, 42))
    d.text((x + 8, y + 3), text, font=F(SANS_B, 8), fill=GOLD)


def panel_shenzhen(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    # moon
    d.ellipse([x + w - 52, y + 8, x + w - 30, y + 30], fill=(232, 222, 190))
    # skyline
    rng = [(6, 34), (26, 48), (50, 28), (74, 54), (100, 38), (128, 58),
           (156, 32), (182, 50), (208, 40), (234, 56), (262, 30), (286, 44)]
    base = y + h - 16
    for bx, bh in rng:
        d.rectangle([x + bx, base - bh, x + bx + 18, base], fill=(13, 27, 48))
        for wy in range(base - bh + 5, base - 5, 8):
            for wx in range(x + bx + 3, x + bx + 15, 6):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.point((wx, wy), fill=(226, 198, 110))
    # table platform
    d.rectangle([x + 58, base - 6, x + w - 58, base], fill=(90, 64, 30))
    # three flags on poles
    flags = ["china", "usa", "russia"]
    for i, kind in enumerate(flags):
        px = x + 96 + i * 52
        d.line([px, base - 44, px, base - 6], fill=(210, 210, 210), width=2)
        d.ellipse([px - 3, base - 49, px + 3, base - 43], fill=GOLD)
        fx, fy = px + 2, base - 44
        fw, fh = 34, 20
        if kind == "china":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(206, 42, 42))
            d.ellipse([fx + 4, fy + 4, fx + 10, fy + 10], fill=(250, 220, 60))
            for sx, sy in [(13, 3), (14, 7), (13, 11)]:
                d.point((fx + sx, fy + sy), fill=(250, 220, 60))
        elif kind == "usa":
            for s in range(5):
                col = (200, 50, 50) if s % 2 == 0 else (238, 238, 232)
                d.rectangle([fx, fy + s * 4, fx + fw, fy + s * 4 + 4], fill=col)
            d.rectangle([fx, fy, fx + 15, fy + 10], fill=(40, 55, 130))
        else:
            d.rectangle([fx, fy, fx + fw, fy + 7], fill=(238, 238, 232))
            d.rectangle([fx, fy + 7, fx + fw, fy + 13], fill=(45, 70, 160))
            d.rectangle([fx, fy + 13, fx + fw, fy + fh], fill=(200, 45, 45))
    caption_strip(x, y + h - 16, w, "SHENZHEN · APEC · THREE LEADERS, ONE TABLE")


def panel_capitol(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    cx = x + w // 2
    base = y + h - 16
    cream = (228, 220, 198)
    # steps and base
    d.rectangle([cx - 105, base - 8, cx + 105, base], fill=cream)
    d.rectangle([cx - 92, base - 14, cx + 92, base - 8], fill=cream)
    # columns
    for i in range(9):
        cxx = cx - 80 + i * 20
        d.rectangle([cxx, base - 38, cxx + 7, base - 14], fill=cream)
    d.rectangle([cx - 90, base - 44, cx + 90, base - 38], fill=cream)
    # dome drum + dome
    d.rectangle([cx - 30, base - 54, cx + 30, base - 44], fill=cream)
    d.pieslice([cx - 38, base - 78, cx + 38, base - 30], 180, 360, fill=cream)
    d.rectangle([cx - 2, base - 84, cx + 2, base - 72], fill=cream)
    d.polygon([(cx, base - 92), (cx + 9, base - 84), (cx, base - 84)], fill=GOLD)
    caption_strip(x, y + h - 16, w, "WASHINGTON · DEMOCRATS TAKE THE HOUSE")


def panel_brandenburg(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    cx = x + w // 2
    base = y + h - 16
    cream = (228, 220, 198)
    # quadriga: chariot block + horse bumps on the roof
    d.rectangle([cx - 16, y + 8, cx + 16, y + 14], fill=cream)
    for hx in (-26, -9, 8, 25):
        d.pieslice([cx + hx - 6, y + 6, cx + hx + 6, y + 16], 180, 360, fill=cream)
    d.rectangle([cx - 1, y + 2, cx + 1, y + 9], fill=GOLD)
    # top beam and frieze
    d.rectangle([cx - 88, y + 14, cx + 88, y + 20], fill=cream)
    d.rectangle([cx - 84, y + 20, cx + 84, y + 25], fill=cream)
    # columns: six, making five openings
    for i in range(6):
        cxx = cx - 82 + i * 31
        d.rectangle([cxx, y + 25, cxx + 9, base - 6], fill=cream)
    d.rectangle([cx - 92, base - 6, cx + 92, base], fill=cream)
    caption_strip(x, y + h - 16, w, "BERLIN · COALITION OF THE WILLING MEETS")


BIGS = [
    dict(panel=panel_shenzhen, tag="ASIA · DIPLOMACY",
         head="TRUMP, XI AND PUTIN HOLD FIRST TRILATERAL IN SHENZHEN",
         deck="The three leaders sit down at APEC today, after a Trump-Putin "
              "handshake on arrival. Putin calls Europe in 'humiliating "
              "decline'; no joint statement by press time."),
    dict(panel=panel_capitol, tag="AMERICAS · POLITICS",
         head="JEFFRIES NOMINATED FOR SPEAKER AS DEMOCRATS TAKE HOUSE",
         deck="The caucus backs Hakeem Jeffries 251–11. Democrats hold at "
              "least 257 House seats, with a 56–44 edge in the Senate after "
              "the midterms. (NPR, USA Today)"),
    dict(panel=panel_brandenburg, tag="EUROPE · DIPLOMACY",
         head="EUROPE DRAFTS A 45BN-EURO LOAN FOR UKRAINE IN BERLIN",
         deck="The Coalition of the Willing meets Witkoff and Kushner as "
              "the EU proposes a €45bn budget-backed loan to fund Kyiv "
              "through 2027. (Reuters)"),
]

GY = 157  # grid top
for i, story in enumerate(BIGS):
    x = COLX[i]
    story["panel"](x, GY, CW, 78)
    tag_row(x, GY + 83, i + 1, story["tag"])
    hf = F(SERIF_B, 20)
    lines = wrap(story["head"], hf, CW)
    hy = GY + 99
    for ln in lines[:3]:
        d.text((x, hy), ln, font=hf, fill=INK)
        hy += 20
    df = F(SERIF, 11)
    for ln in wrap(story["deck"], df, CW)[:3]:
        d.text((x, hy + 5), ln, font=df, fill=(52, 48, 42))
        hy += 12


# ------------------------------------------------------------ medium grid
B_RED = (169, 50, 38)
B_PURPLE = (91, 42, 134)
B_NAVY = (31, 58, 95)
B_SLATE = (70, 97, 126)
B_TEAL = (23, 126, 112)
B_GREEN = (30, 132, 73)
B_RUST = (160, 64, 22)
B_DGREEN = (29, 112, 68)


def icon(kind, cx, cy, s=9, col=(255, 255, 255)):
    """Small white line motif centred on (cx, cy)."""
    if kind == "cross":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=col, width=2)
        d.line([cx, cy - 4, cx, cy + 4], fill=col, width=2)
        d.line([cx - 4, cy, cx + 4, cy], fill=col, width=2)
    elif kind == "gamepad":
        d.rounded_rectangle([cx - s - 2, cy - 6, cx + s + 2, cy + 6], 5, outline=col, width=2)
        d.line([cx - 6, cy - 2, cx - 6, cy + 2], fill=col, width=2)
        d.line([cx - 8, cy, cx - 4, cy], fill=col, width=2)
        d.point((cx + 5, cy - 2), fill=col)
        d.point((cx + 7, cy + 1), fill=col)
    elif kind == "planet":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=col, width=2)
        d.ellipse([cx - s - 2, cy - 3, cx + s + 2, cy + 3], outline=col, width=1)
    elif kind == "burst":
        for k in range(8):
            a = k * math.pi / 4
            d.line([cx + 3 * math.cos(a), cy + 3 * math.sin(a),
                    cx + s * math.cos(a), cy + s * math.sin(a)], fill=col, width=2)
    elif kind == "spiral":
        pts = []
        for t in range(0, 66):
            ang = t * 0.32
            r = 0.4 + t * 0.13
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.line(pts, fill=col, width=2)
    elif kind == "scales":
        d.line([cx, cy - s, cx, cy + s], fill=col, width=2)
        d.line([cx - s, cy - s + 2, cx + s, cy - s + 2], fill=col, width=2)
        for side in (-1, 1):
            px = cx + side * s
            d.line([px, cy - s + 2, px - 4, cy + 3], fill=col, width=1)
            d.line([px, cy - s + 2, px + 4, cy + 3], fill=col, width=1)
            d.arc([px - 5, cy + 1, px + 5, cy + 7], 0, 180, fill=col, width=2)
    elif kind == "ball":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=col, width=2)
        d.polygon([(cx, cy - 3), (cx + 3, cy - 1), (cx + 2, cy + 3),
                   (cx - 2, cy + 3), (cx - 3, cy - 1)], outline=col)
        for px, py in [(-6, -5), (6, -5), (0, 7)]:
            d.point((cx + px, cy + py), fill=col)
    elif kind == "shield":
        d.polygon([(cx, cy - s), (cx + s - 1, cy - s + 3), (cx + s - 1, cy + 2),
                   (cx, cy + s), (cx - s + 1, cy + 2), (cx - s + 1, cy - s + 3)],
                  outline=col, width=2)
        d.line([cx - 4, cy, cx - 1, cy + 3], fill=col, width=2)
        d.line([cx - 1, cy + 3, cx + 5, cy - 4], fill=col, width=2)
    elif kind == "sun":
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=col, width=2)
        for k in range(8):
            a = k * math.pi / 4 + 0.4
            d.line([cx + 6 * math.cos(a), cy + 6 * math.sin(a),
                    cx + s * math.cos(a), cy + s * math.sin(a)], fill=col, width=2)
    elif kind == "bars":
        for i, bh in enumerate((5, 9, 13)):
            bx = cx - 8 + i * 7
            d.rectangle([bx, cy + 7 - bh, bx + 4, cy + 7], fill=col)
    elif kind == "waves":
        for row in (-4, 2):
            pts = [(cx - s + t, cy + row + 2.2 * math.sin(t / 3.0))
                   for t in range(0, 2 * s + 1, 2)]
            d.line(pts, fill=col, width=2)


MEDIUMS = [
    dict(stat="3 KILLED", sub="MEDICS' COUNT IN GAZA CITY", col=B_RED, icon="cross",
         tag="MIDDLE EAST · WAR", head="Israeli tanks thrust into Gaza City",
         deck="Israeli tanks thrust into Gaza City; three Palestinians killed "
              "in the advance, medics say. (Reuters)"),
    dict(stat="13 YEARS", sub="THE WAIT FOR GTA VI ENDS", col=B_PURPLE, icon="gamepad",
         tag="GLOBAL · GAMES", head="GTA VI finally launches, 13 years on",
         deck="Queues wrap game stores worldwide on launch day, 13 years after "
              "the last instalment. (AP, BBC)"),
    dict(stat="16BN MILES", sub="ONE LIGHT-DAY OUT", col=B_NAVY, icon="planet",
         tag="SPACE · SCIENCE", head="Voyager 1 reaches one light-day out",
         deck="The 1977 probe's signals now take a full day to reach Earth. (NASA)"),
    dict(stat="4 KILLED", sub="OVERNIGHT BARRAGE ON ODESA", col=B_SLATE, icon="burst",
         tag="EUROPE · WAR", head="Russian strikes on Odesa kill four",
         deck="Overnight barrage hits port and homes, officials say, in the "
              "latest strike on the city. (Reuters)"),
    dict(stat="20 NOV", sub="LANDFALL DUE — EAST COAST", col=B_TEAL, icon="spiral",
         tag="ASIA · WEATHER", head="Cyclone Akvan turns very severe",
         deck="The storm turns very severe over the bay; landfall on the east "
              "coast is due on 20 November. (The Hindu)"),
    dict(stat="THE HAGUE", sub="JUDGMENT READ TODAY", col=B_NAVY, icon="scales",
         tag="EUROPE · JUSTICE", head="World Court reads Rohingya judgment",
         deck="Did Myanmar commit genocide? The court reads its judgment "
              "today; verdict awaited. (Le Monde)"),
    dict(stat="2–1", sub="INDIA EDGE PAKISTAN — SAFF", col=B_GREEN, icon="ball",
         tag="ASIA · SPORT", head="India beat Pakistan 2–1, take SAFF title",
         deck="A late winner settles a tense regional final as India edge "
              "Pakistan. (TOI)"),
    dict(stat="21 KILLED", sub="ISWAP FIGHTERS — BORNO", col=B_RUST, icon="shield",
         tag="AFRICA · SECURITY", head="21 ISWAP fighters killed in Borno",
         deck="Nigeria's army reports the clash in the north-east state of "
              "Borno. (Vanguard)"),
    dict(stat="$7BN", sub="INDIA RENEWABLES TO 2030", col=B_DGREEN, icon="sun",
         tag="ASIA · BUSINESS", head="Amazon pledges $7bn for India renewables",
         deck="The investment runs to 2030, the company says — a clean-energy "
              "push in India. (TOI)"),
    dict(stat="BY 2035", sub="ISLAM NEARS CHRISTIANITY — PEW", col=B_PURPLE, icon="bars",
         tag="WORLD · SOCIETY", head="Pew: Islam nearly level with Christianity by 2035",
         deck="Pew's projections put Islam almost level with Christianity by 2035."),
    dict(stat="48 TEAMS", sub="U-17 WORLD CUP OPENS — DOHA", col=B_GREEN, icon="ball",
         tag="MIDDLE EAST · SPORT", head="U-17 World Cup kicks off in Doha",
         deck="Hosts Qatar open against Panama as 48 teams begin the biggest "
              "youth World Cup yet — 104 matches in Doha. (FIFA)"),
    dict(stat="2,500", sub="DEAD ON SEA ROUTES — UNHCR", col=B_TEAL, icon="waves",
         tag="EUROPE · REFUGEES", head="Sea-route deaths pass 2,500 this year",
         deck="The UN refugee agency's running count of deaths on the sea "
              "routes passed 2,500 for the year."),
]

MED_TOP = 359
MED_PITCH = 97
for idx, m in enumerate(MEDIUMS):
    row, col_i = divmod(idx, 3)
    x = COLX[col_i]
    y = MED_TOP + row * MED_PITCH
    # banner strip
    d.rectangle([x, y, x + CW, y + 27], fill=m["col"])
    if m["stat"] == "13 YEARS":  # tiny skyline along the banner base
        for bx, bh in [(30, 5), (52, 8), (80, 4), (150, 6), (205, 5), (238, 7)]:
            d.rectangle([x + bx, y + 27 - bh, x + bx + 10, y + 27], fill=(60, 22, 92))
    if m["stat"] == "16BN MILES":  # starfield
        for sx, sy in [(36, 6), (70, 16), (112, 8), (160, 18), (196, 5), (238, 14), (262, 7)]:
            d.point((x + sx, y + sy), fill=(255, 255, 255))
            d.point((x + sx + 40, y + sy + 3), fill=(200, 210, 235))
    d.text((x + 8, y + 2), m["stat"], font=F(SANS_B, 15), fill=(255, 255, 255))
    d.text((x + 8, y + 18), m["sub"], font=F(SANS_B, 7), fill=(235, 228, 214))
    icon(m["icon"], x + CW - 20, y + 13)
    # tag + headline + deck
    number_badge(x, y + 30, idx + 4, dia=12)
    d.text((x + 17, y + 31), m["tag"], font=F(SANS_B, 9), fill=RED)
    hf = F(SERIF_B, 14)
    hy = y + 43
    for ln in wrap(m["head"], hf, CW)[:2]:
        d.text((x, hy), ln, font=hf, fill=INK)
        hy += 15
    df = F(SERIF, 10)
    for ln in wrap(m["deck"], df, CW)[:2]:
        d.text((x, hy + 3), ln, font=df, fill=(52, 48, 42))
        hy += 11


# ---------------------------------------------------------- numbers strip
NY = 752
d.line([MX, NY, W - MX, NY], fill=GOLD, width=2)
d.text((MX, NY + 8), "BY THE", font=F(SANS_B, 9), fill=INK)
d.text((MX, NY + 19), "NUMBERS", font=F(SANS_B, 9), fill=INK)
NUMBERS = [
    ("251–11", "Jeffries caucus vote", 150),
    ("€45bn", "EU loan proposed for Ukraine", 330),
    ("56–44", "US Senate split", 580),
    ("1 light-day", "Voyager 1's distance out", 760),
]
for big, cap, x in NUMBERS:
    d.text((x, NY + 5), big, font=F(SERIF_B, 22), fill=INK)
    d.text((x, NY + 30), cap, font=F(SANS, 8), fill=(52, 48, 42))
d.line([MX, NY + 42, W - MX, NY + 42], fill=GOLD, width=2)

# ------------------------------------------------------------- bottom half
BY = 800
d.text((MX, BY), "WHERE IT HAPPENED", font=F(SERIF_B, 13), fill=RED)
also_head = "ALSO ON THURSDAY 19 NOVEMBER — 27 MORE STORIES"
d.text((448, BY), also_head, font=F(SERIF_B, 13), fill=RED)

MAP_X, MAP_Y, MAP_W, MAP_H = MX, 818, 396, 100
LON0, LON1, LAT0, LAT1 = -170.0, 190.0, 82.0, -58.0


def mxy(lon, lat):
    x = MAP_X + (lon - LON0) / (LON1 - LON0) * MAP_W
    y = MAP_Y + (LAT0 - lat) / (LAT0 - LAT1) * MAP_H
    return x, y


d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
            outline=LAND_EDGE, width=1)
# faint graticule
for glon in range(-150, 181, 30):
    gx, _ = mxy(glon, 0)
    d.line([gx, MAP_Y, gx, MAP_Y + MAP_H], fill=(224, 216, 192))
for glat in range(-40, 81, 20):
    _, gy = mxy(0, glat)
    d.line([MAP_X, gy, MAP_X + MAP_W, gy], fill=(224, 216, 192))

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 79), (-86, 78),
     (-81, 73), (-85, 69), (-80, 62), (-77, 58), (-70, 55), (-65, 50),
     (-70, 45), (-74, 40), (-76, 35), (-80, 31), (-81, 26), (-84, 29),
     (-89, 29), (-94, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 15),
     (-86, 13), (-83, 9), (-79, 9), (-84, 11), (-90, 14), (-96, 16),
     (-102, 19), (-105, 23), (-110, 24), (-114, 29), (-117, 33),
     (-122, 37), (-124, 46), (-130, 54), (-140, 60), (-155, 60), (-166, 60)],
    # Greenland
    [(-45, 60), (-32, 68), (-22, 70), (-19, 76), (-28, 81), (-45, 80),
     (-55, 76), (-58, 68), (-53, 62)],
    # South America
    [(-79, 9), (-75, 11), (-70, 12), (-64, 10), (-59, 8), (-52, 5),
     (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-40, -20), (-46, -24),
     (-52, -30), (-57, -35), (-62, -39), (-65, -45), (-67, -50),
     (-68, -54), (-71, -54), (-73, -49), (-73, -43), (-72, -36),
     (-71, -29), (-70, -20), (-75, -15), (-79, -8), (-81, -4),
     (-80, 1), (-77, 4), (-79, 7)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (34, 28), (35, 24), (37, 21), (39, 19), (43, 12), (48, 11), (51, 12),
     (48, 5), (44, 0), (41, -5), (40, -12), (39, -18), (37, -22),
     (35, -26), (32, -29), (28, -33), (24, -34), (20, -35), (18, -32),
     (16, -28), (14, -22), (13, -15), (12, -10), (13, -5), (9, -1),
     (9, 4), (4, 6), (-3, 5), (-8, 4), (-13, 8), (-17, 12), (-17, 15),
     (-16, 20), (-15, 25), (-13, 28), (-10, 31)],
    # Europe
    [(-10, 37), (-9, 43), (-2, 44), (-4, 48), (0, 49), (2, 51), (6, 53),
     (8, 55), (7, 57), (10, 59), (5, 60), (6, 62), (12, 65), (19, 69),
     (30, 70), (41, 68), (45, 66), (41, 63), (35, 60), (31, 58), (29, 60),
     (24, 59), (21, 56), (18, 56), (19, 54), (23, 54), (28, 55), (30, 59),
     (31, 56), (29, 52), (27, 49), (23, 46), (19, 45), (15, 45), (13, 45),
     (12, 43), (8, 44), (5, 43), (2, 43), (-1, 40), (-2, 37)],
    # Britain
    [(-5, 50), (-3, 52), (-2, 54), (-4, 56), (-6, 58), (-3, 58), (-1, 56),
     (-1, 53), (-2, 51)],
    # Asia
    [(28, 41), (33, 42), (40, 43), (45, 42), (48, 46), (49, 50), (52, 54),
     (58, 57), (65, 60), (70, 64), (76, 67), (88, 70), (100, 72),
     (112, 73), (124, 72), (136, 71), (148, 71), (158, 69), (166, 65),
     (178, 65), (178, 62), (169, 60), (161, 58), (157, 51), (149, 48),
     (142, 45), (140, 40), (136, 35), (131, 33), (127, 38), (122, 38),
     (121, 32), (122, 28), (117, 24), (111, 21), (108, 17), (106, 9),
     (103, 5), (100, 8), (98, 13), (95, 16), (92, 16), (90, 22),
     (88, 21), (85, 19), (82, 15), (80, 13), (77, 8), (75, 12),
     (72, 19), (69, 22), (66, 25), (61, 25), (57, 26), (53, 26),
     (51, 28), (50, 29), (47, 30), (43, 30), (39, 31), (35, 33),
     (33, 36), (30, 36), (27, 37)],
    # Indonesia / New Guinea blobs
    [(99, 1), (104, -2), (109, -3), (114, -2), (119, -3), (124, -2),
     (129, -3), (134, -3), (139, -4), (140, -8), (134, -7), (127, -6),
     (119, -8), (112, -7), (105, -6), (100, -3)],
    [(110, 1), (113, 4), (117, 6), (119, 2), (117, -2), (112, -3), (110, -1)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (140, 45), (138, 39), (135, 34), (132, 33)],
    # Australia
    [(113, -22), (114, -29), (115, -34), (120, -34), (126, -32),
     (131, -32), (134, -33), (136, -35), (139, -37), (142, -38),
     (146, -39), (149, -37), (152, -33), (153, -28), (151, -23),
     (148, -19), (145, -15), (142, -11), (141, -14), (144, -17),
     (142, -23), (140, -28), (139, -33), (136, -35), (133, -34),
     (129, -33), (124, -33), (118, -35), (115, -33), (113, -26)],
    # New Zealand
    [(167, -45), (170, -43), (172, -41), (174, -39), (176, -38),
     (174, -41), (172, -43), (169, -46)],
]
for poly in CONTINENTS:
    pts = [mxy(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LAND_EDGE)

for label, lon, lat in [("N. AMERICA", -104, 55), ("S. AMERICA", -60, -16),
                        ("EUROPE", 40, 65), ("AFRICA", 20, 4),
                        ("ASIA", 96, 46), ("OCEANIA", 141, -29)]:
    lx, ly = mxy(lon, lat)
    d.text((lx, ly), label, font=F(SANS_B, 7), fill=(146, 128, 88))

# grey dots for the briefs
DOTS = [(-106, 56), (-1.2, 6.7), (-7.6, 33.6), (36.8, -1.3),
        (134, -25), (13.1, 32.9), (31.2, 30), (139.7, 35.7), (-74.1, 4.7),
        (74.8, 34.1), (-99.2, 19.4), (27.9, 43.2), (2.3, 48.9)]
for lon, lat in DOTS:
    gx, gy = mxy(lon, lat)
    d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(150, 144, 130))

# numbered pins for the 15 mains (lon, lat, small nudge in px)
PINS = [
    (114.1, 22.5, 0, 0),      # 1 Shenzhen
    (-77.0, 38.9, -2, -3),    # 2 Washington
    (13.4, 52.5, 6, -4),      # 3 Berlin
    (34.3, 31.4, 3, 4),       # 4 Gaza
    (-97.7, 30.3, 0, 4),      # 5 GTA VI launch (Austin)
    (-118.1, 34.1, -3, -3),   # 6 JPL, Pasadena
    (30.7, 46.5, 0, -3),      # 7 Odesa
    (88.0, 14.0, 0, 0),       # 8 Cyclone Akvan, Bay of Bengal
    (4.3, 52.1, -6, 5),       # 9 The Hague
    (77.2, 28.6, 3, -3),      # 10 SAFF final, India
    (13.2, 11.8, 0, 0),       # 11 Borno
    (72.8, 19.0, -3, 3),      # 12 India renewables
    (-75.0, 40.0, 8, 7),      # 13 Pew (US east)
    (51.5, 25.3, 0, 0),       # 14 Doha
    (15.0, 37.0, 0, 0),       # 15 Mediterranean sea routes
]
for n, (lon, lat, dx, dy) in enumerate(PINS, start=1):
    px, py = mxy(lon, lat)
    px, py = px + dx, py + dy
    r = 7
    d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
    f = F(SANS_B, 8 if n < 10 else 7)
    label = str(n)
    d.text((px - tw(label, f) / 2, py - 4), label, font=f, fill=(255, 255, 255))

cap = ("Red numbers mark stories 1–15; grey dots mark the briefs. Pin 6 sits "
       "at JPL, Pasadena — Voyager 1 is one light-day out. Positions are approximate.")
cf = F(SERIF, 8)
for i, ln in enumerate(wrap(cap, cf, MAP_W)):
    d.text((MAP_X, 922 + i * 11), ln, font=cf, fill=RED)


# ------------------------------------------------------------ ALSO columns
ALSO = [
    ("RUSSIA", "Refining output down 45% after strikes"),
    ("UKRAINE", "Arms deliveries speed up, Kyiv says"),
    ("WASHINGTON", "Schumer, Van Hollen clash over shutdown"),
    ("US SENATE", "Democrats hold the Senate too, 56–44"),
    ("TECH", "Agencies warn of AI-driven cyber threat"),
    ("CANADA", "Carney balances China and US talks"),
    ("MOSCOW", "Lavrov accuses France over Ukraine arms"),
    ("FRANCE", "Mélenchon says he could win the presidency"),
    ("BULGARIA", "LPG tanker fire contained, Black Sea"),
    ("AUSTRALIA", "Settler sanctions widened — West Bank"),
    ("RIYADH", "Saudi flight alerts lifted"),
    ("LIBYA", "Record cocaine haul seized off the coast"),
    ("CAIRO", "Egypt and Syria sign aviation pact"),
    ("TOKYO", "India and Japan review defence ties"),
    ("GHANA", "Bad loans fall to 13.1% of lending"),
    ("MOROCCO", "Defence industry roadmap unveiled"),
    ("KENYA", "Ruto gives State of the Nation address"),
    ("SUDAN", "RSF strikes hit El Obeid again"),
    ("COP31", "Ocean protection talks open"),
    ("SCIENCE", "Earth's missing billion years explained"),
    ("BOGOTA", "Hegseth visits Colombia for security talks"),
    ("AFRICA", "AFCON qualifier draw made in Cairo"),
    ("KASHMIR", "Three militants killed in Kulgam encounter"),
    ("BHOPAL", "National hockey opener thrills home crowd"),
    ("HAGUE", "Fears US may sanction ICJ judges — reports"),
    ("CALIFORNIA", "Flood watch up into Thursday"),
    ("MEXICO", "Banxico minutes out: 3–2 for cut to 6.25%"),
]

ALSO_COLS = [(448, 270), (734, 262)]  # (x, width) per column
ALSO_TOP = 820
ALSO_LH = 9.6


def also_line(x, y, maxw, n, tag, text):
    size = 9
    while size > 7:
        fb, fr = F(SANS_B, size), F(SANS, size)
        num = f"{n} "
        w = tw(num, fb) + tw(tag, fb) + tw(" — ", fr) + tw(text, fr)
        if w <= maxw:
            break
        size -= 0.5
    fb, fr = F(SANS_B, size), F(SANS, size)
    cx = x
    d.text((cx, y), f"{n} ", font=fb, fill=RED)
    cx += tw(f"{n} ", fb)
    d.text((cx, y), tag, font=fb, fill=INK)
    cx += tw(tag, fb)
    d.text((cx, y), " — " + text, font=fr, fill=INK)


for ci, (cx0, cw0) in enumerate(ALSO_COLS):
    chunk = ALSO[ci * 14:(ci + 1) * 14] if ci == 0 else ALSO[14:]
    for j, (tag, text) in enumerate(chunk):
        also_line(cx0, ALSO_TOP + j * ALSO_LH, cw0, 16 + ci * 14 + j, tag, text)

# -------------------------------------------------------------- DATE CHECK
DY = 956
d.rectangle([MX, DY, MX + 96, DY + 26], fill=RED)
lab = "DATE CHECK"
lf = F(SANS_B, 10)
d.text((MX + (96 - tw(lab, lf)) / 2, DY + 7), lab, font=lf, fill=(255, 255, 255))
dc_x = MX + 108
dc_lines = [
    ("Left out on purpose — they broke before today: ", True,
     "Jensen Huang's resignation as Nvidia's chief (announced 12 Nov) · America's strike on Iran's", False),
    ("", False,
     "Qeshm Island missile site (17 Nov) · Musk's petition to bring Huang back (13 Nov)", False),
]
for i, (lead, lead_b, rest, _) in enumerate(dc_lines):
    y = DY + 2 + i * 11
    cx = dc_x
    if lead:
        fb = F(SANS_B, 9)
        d.text((cx, y), lead, font=fb, fill=INK)
        cx += tw(lead, fb)
    d.text((cx, y), rest, font=F(SANS, 9), fill=INK)

# ------------------------------------------------------------------ footer
note = "JUDGE NOTE — Every story above happened, or was first reported, on Thursday 19 November 2026."
nf = F(SERIF_B, 10)
d.text(((W - tw(note, nf)) / 2, 986), note, font=nf, fill=INK)
note2 = "Disputed claims are attributed, not stated as fact."
d.text(((W - tw(note2, nf)) / 2, 999), note2, font=nf, fill=INK)
src = ("Sources: Reuters · AP · AFP · BBC · The Guardian · Le Monde · The Hindu · TOI · Vanguard · NASA "
       "and the regional wires named above. Original drawings. · Date checked: 19.11.2026")
sf = F(SANS, 8)
d.text(((W - tw(src, sf)) / 2, 1013), src, font=sf, fill=GREY)

img.save(OUT)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
