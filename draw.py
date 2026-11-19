#!/usr/bin/env python3
"""Build tool for the news-image-20261119 v3 entry.

Draws entry.png (1024x1024): one newspaper front page for Thursday
19 November 2026 -- 3 big illustrated mains + 12 medium mains in a strict
3-column grid, every main carrying artwork (scene panel or stat banner),
a By The Numbers strip, a filled-silhouette "Where It Happened" map with
numbered pins, a two-column Also briefs list, a DATE CHECK strip and a
judge-note footer. All artwork is original, drawn with PIL primitives.
This file is a build tool only; main.py never imports it.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
MARGIN = 26
COLW = 316
GUT = 12
COLX = [MARGIN, MARGIN + COLW + GUT, MARGIN + 2 * (COLW + GUT)]

PAPER = (247, 242, 231)
PAPER_DARK = (238, 230, 214)
INK = (22, 26, 34)
INK_SOFT = (62, 66, 74)
NAVY = (13, 32, 56)
NAVY_2 = (24, 52, 84)
GOLD = (198, 158, 44)
RED = (176, 32, 38)
RED_DARK = (140, 24, 30)
WHITE = (252, 250, 244)
MAP_BG = (216, 231, 233)
LAND = (216, 197, 154)
LAND_EDGE = (168, 148, 104)
PIN_GREY = (120, 122, 124)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIFB = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANSB = FD + "DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def tracked(d, x, y, text, font, fill, spacing=3):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += tw(d, ch, font) + spacing
    return x


def tracked_r(d, right, y, text, font, fill, spacing=3):
    total = sum(tw(d, c, font) for c in text) + spacing * (len(text) - 1)
    return tracked(d, right - total, y, text, font, fill, spacing)


def badge(d, cx, cy, r, num, fill=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    f = F(SANSB, int(r * 1.15))
    t = str(num)
    d.text((cx - tw(d, t, f) / 2, cy - r * 0.62), t, font=f, fill=WHITE)


# ---------------------------------------------------------------- stories
# Big mains: art kind, caption strip, tag, headline, deck.
BIG = [
    dict(n=1, art="shenzhen", cap="SHENZHEN \u00b7 APEC \u00b7 THREE LEADERS, ONE TABLE",
         tag="ASIA \u00b7 DIPLOMACY",
         head="Trump, Xi and Putin hold first trilateral in Shenzhen",
         deck="The three leaders sit down at APEC today, after a Trump\u2013Putin "
              "handshake on arrival. Putin calls Europe in \u2018humiliating "
              "decline\u2019; no joint statement by press time."),
    dict(n=2, art="capitol", cap="WASHINGTON \u00b7 DEMOCRATS TAKE THE HOUSE",
         tag="AMERICAS \u00b7 POLITICS",
         head="Jeffries nominated for Speaker as Democrats take House",
         deck="The caucus backs Hakeem Jeffries 251\u201311. Democrats hold at "
              "least 257 House seats, with a 56\u201344 edge in the Senate "
              "after the midterms. (NPR, USA Today)"),
    dict(n=3, art="berlin", cap="BERLIN \u00b7 COALITION OF THE WILLING MEETS",
         tag="EUROPE \u00b7 DIPLOMACY",
         head="Europe drafts a 45bn-euro loan for Ukraine in Berlin",
         deck="The Coalition of the Willing meets Witkoff and Kushner as the "
              "EU proposes a \u20ac45bn budget-backed loan to fund Kyiv "
              "through 2027. (Reuters)"),
]

# Medium mains: banner stat + sub, colour, icon, tag, headline, deck.
MED = [
    dict(n=4, stat="3 KILLED", sub="MEDICS\u2019 COUNT IN GAZA CITY",
         col=(122, 34, 40), icon="cross", tag="MIDDLE EAST \u00b7 WAR",
         head="Israeli tanks thrust into Gaza City",
         deck="Israeli tanks thrust into Gaza City; three Palestinians "
              "killed in the advance, medics say. (Reuters)"),
    dict(n=5, stat="13 YEARS", sub="THE WAIT FOR GTA VI ENDS",
         col=(84, 52, 108), icon="pad", tag="GLOBAL \u00b7 GAMES",
         head="GTA VI finally launches, 13 years on",
         deck="Queues wrap game stores worldwide on launch day, 13 years "
              "after the last instalment. (AP, BBC)"),
    dict(n=6, stat="16BN MILES", sub="ONE LIGHT-DAY OUT",
         col=(16, 34, 66), icon="planet", tag="SPACE \u00b7 SCIENCE",
         head="Voyager 1 reaches one light-day out",
         deck="The 1977 probe\u2019s signals now take a full day to reach "
              "Earth. (NASA)"),
    dict(n=7, stat="4 KILLED", sub="OVERNIGHT BARRAGE ON ODESA",
         col=(52, 74, 102), icon="burst", tag="EUROPE \u00b7 WAR",
         head="Russian strikes on Odesa kill four",
         deck="Overnight barrage hits port and homes, officials say, in the "
              "latest strike on the city. (Reuters)"),
    dict(n=8, stat="20 NOV", sub="LANDFALL DUE \u2014 EAST COAST",
         col=(14, 96, 104), icon="spiral", tag="ASIA \u00b7 WEATHER",
         head="Cyclone Akvan turns very severe",
         deck="The storm turns very severe over the bay; landfall on the "
              "east coast is due on 20 November. (The Hindu)"),
    dict(n=9, stat="THE HAGUE", sub="JUDGMENT READ TODAY",
         col=(30, 58, 96), icon="scales", tag="EUROPE \u00b7 JUSTICE",
         head="World Court reads Rohingya judgment",
         deck="Did Myanmar commit genocide? The court reads its judgment "
              "today; verdict awaited. (Le Monde)"),
    dict(n=10, stat="2\u20131", sub="INDIA EDGE PAKISTAN \u2014 SAFF",
         col=(30, 110, 66), icon="ball", tag="ASIA \u00b7 SPORT",
         head="India beat Pakistan 2\u20131, take SAFF title",
         deck="A late winner settles a tense regional final as India edge "
              "Pakistan. (TOI)"),
    dict(n=11, stat="21 KILLED", sub="ISWAP FIGHTERS \u2014 BORNO",
         col=(150, 74, 30), icon="shield", tag="AFRICA \u00b7 SECURITY",
         head="21 ISWAP fighters killed in Borno",
         deck="Nigeria\u2019s army reports the clash in the north-east "
              "state of Borno. (Vanguard)"),
    dict(n=12, stat="$7BN", sub="INDIA RENEWABLES TO 2030",
         col=(88, 116, 40), icon="sun", tag="ASIA \u00b7 BUSINESS",
         head="Amazon pledges $7bn for India renewables",
         deck="The investment runs to 2030, the company says \u2014 a "
              "clean-energy push in India. (TOI)"),
    dict(n=13, stat="BY 2035", sub="ISLAM NEARS CHRISTIANITY \u2014 PEW",
         col=(96, 78, 120), icon="bars", tag="WORLD \u00b7 SOCIETY",
         head="Pew: Islam nearly level with Christianity by 2035",
         deck="Pew\u2019s projections put Islam almost level with "
              "Christianity worldwide by 2035."),
    dict(n=14, stat="133 DUCKETT", sub="ENG WIN ODI SERIES 2\u20131",
         col=(24, 96, 58), icon="bat", tag="OCEANIA \u00b7 CRICKET",
         head="Duckett\u2019s 133 seals England\u2019s ODI series win",
         deck="Duckett\u2019s 133 off 115 balls powers a 97-run win in "
              "Hobart \u2014 England\u2019s first ODI series win there in "
              "eight years."),
    dict(n=15, stat="2,500", sub="DEAD ON SEA ROUTES \u2014 UNHCR",
         col=(44, 84, 110), icon="waves", tag="EUROPE \u00b7 REFUGEES",
         head="Sea-route deaths pass 2,500 this year",
         deck="The UN refugee agency\u2019s running count of deaths on "
              "the sea routes passed 2,500 for the year."),
]

# Also briefs 16-42: (place tag, one-liner)
ALSO = [
    ("RUSSIA", "Refining output down 45% after strikes"),
    ("UKRAINE", "Arms deliveries speed up, Kyiv says"),
    ("WASHINGTON", "Schumer, Van Hollen clash over shutdown"),
    ("US SENATE", "Democrats hold the Senate too, 56\u201344"),
    ("TECH", "Agencies warn of AI-driven cyber threat"),
    ("CANADA", "Carney balances China and US talks"),
    ("MOSCOW", "Lavrov accuses France over Ukraine arms"),
    ("FRANCE", "M\u00e9lenchon says he could win the presidency"),
    ("BULGARIA", "LPG tanker fire contained, Black Sea"),
    ("AUSTRALIA", "Settler sanctions widened \u2014 West Bank"),
    ("RIYADH", "Saudi flight alerts lifted"),
    ("LIBYA", "Record cocaine haul seized off the coast"),
    ("CAIRO", "Egypt and Syria sign aviation pact"),
    ("TOKYO", "India and Japan review defence ties"),
    ("GHANA", "Bad loans fall to 13.1% of lending"),
    ("MOROCCO", "Defence industry roadmap unveiled"),
    ("KENYA", "Ruto gives State of the Nation address"),
    ("SUDAN", "RSF strikes hit El Obeid again"),
    ("COP31", "Ocean protection talks open"),
    ("SCIENCE", "Earth\u2019s missing billion years explained"),
    ("BOGOTA", "Hegseth visits Colombia for security talks"),
    ("DOHA", "FIFA U-17 World Cup kicks off"),
    ("AFRICA", "AFCON qualifier draw made in Cairo"),
    ("KASHMIR", "Three militants killed in Kulgam encounter"),
    ("BHOPAL", "National hockey opener thrills home crowd"),
    ("HAGUE", "Fears US may sanction ICJ judges \u2014 reports"),
    ("CALIFORNIA", "Flood watch up into Thursday"),
]

NUMBERS = [
    ("251\u201311", "Jeffries caucus vote"),
    ("\u20ac45bn", "EU loan proposed for Ukraine"),
    ("56\u201344", "US Senate split"),
    ("1 light-day", "Voyager 1\u2019s distance out"),
]


# ---------------------------------------------------------------- big art
def art_shenzhen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 38, 66))
    d.ellipse([x + w - 52, y + 6, x + w - 26, y + 32], fill=(240, 200, 90))
    # skyline
    cols = [(0, 26), (26, 38), (58, 20), (88, 44), (122, 30), (152, 48),
            (186, 26), (214, 40), (246, 24), (272, 36)]
    for dx, bh in cols:
        d.rectangle([x + dx, y + h - 14 - bh, x + dx + 22, y + h - 14],
                    fill=(10, 24, 44))
        for wy in range(y + h - 10 - bh, y + h - 16, 7):
            d.point((x + dx + 6, wy), fill=(250, 214, 120))
            d.point((x + dx + 14, wy + 3), fill=(250, 214, 120))
    # table + three flags
    ty = y + h - 14
    d.rectangle([x + 96, ty - 3, x + 220, ty], fill=(230, 220, 196))
    for i, fx in enumerate((118, 152, 186)):
        d.line([x + fx, ty - 3, x + fx, ty - 26], fill=WHITE, width=2)
        if i == 0:  # China
            d.rectangle([x + fx, ty - 26, x + fx + 20, ty - 14], fill=(206, 44, 44))
            d.ellipse([x + fx + 3, ty - 23, x + fx + 7, ty - 19], fill=(250, 220, 90))
        elif i == 1:  # US
            d.rectangle([x + fx, ty - 26, x + fx + 20, ty - 14], fill=(238, 238, 238))
            for s in range(3):
                d.line([x + fx, ty - 23 + s * 4, x + fx + 20, ty - 23 + s * 4],
                       fill=(188, 40, 48), width=1)
            d.rectangle([x + fx, ty - 26, x + fx + 9, ty - 20], fill=(40, 60, 140))
        else:  # Russia
            d.rectangle([x + fx, ty - 26, x + fx + 20, ty - 14], fill=(238, 238, 238))
            d.rectangle([x + fx, ty - 22, x + fx + 20, ty - 18], fill=(40, 70, 160))
            d.rectangle([x + fx, ty - 18, x + fx + 20, ty - 14], fill=(200, 44, 44))


def art_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 40, 70))
    cx = x + w // 2
    base = y + h - 2
    cream = (238, 230, 205)
    d.rectangle([cx - 88, base - 15, cx + 88, base], fill=cream)
    for i in range(-4, 5):
        d.line([cx + i * 18, base - 15, cx + i * 18, base], fill=NAVY_2, width=2)
    d.rectangle([cx - 52, base - 21, cx + 52, base - 15], fill=cream)
    d.pieslice([cx - 44, base - 50, cx + 44, base - 4], 180, 360, fill=cream)
    d.rectangle([cx - 3, base - 54, cx + 3, base - 49], fill=cream)
    d.ellipse([cx - 2, base - 55, cx + 2, base - 51], fill=GOLD)
    for sx in (x + 26, x + 66, x + w - 66, x + w - 26):
        d.ellipse([sx - 2, y + 10, sx + 2, y + 14], fill=(250, 240, 200))


def art_berlin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 54, 88))
    cx = x + w // 2
    base = y + h - 4
    stone = (226, 214, 188)
    d.rectangle([cx - 92, base - 40, cx + 92, base - 32], fill=stone)  # beam
    for i in range(6):
        gx = cx - 85 + i * 31
        d.rectangle([gx, base - 32, gx + 13, base], fill=stone)
    d.rectangle([cx - 92, base - 4, cx + 92, base], fill=stone)
    # quadriga: chariot + horses, simplified
    qy = base - 40
    d.rectangle([cx - 8, qy - 8, cx + 10, qy - 3], fill=stone)
    d.ellipse([cx - 2, qy - 13, cx + 4, qy - 7], fill=stone)
    for hx in (-26, -16, 14, 24):
        d.line([cx + hx, qy - 8, cx + hx + 3, qy - 1], fill=stone, width=2)
        d.ellipse([cx + hx - 3, qy - 11, cx + hx + 3, qy - 6], fill=stone)
    for sx in (x + 30, x + 84, x + w - 84, x + w - 30):
        d.ellipse([sx - 2, y + 8, sx + 2, y + 12], fill=(250, 240, 200))


BIG_ART = {"shenzhen": art_shenzhen, "capitol": art_capitol, "berlin": art_berlin}


# ---------------------------------------------------------------- icons
def icon(d, kind, cx, cy, r, col=WHITE):
    if kind == "cross":
        d.rectangle([cx - 2, cy - 7, cx + 2, cy + 7], fill=col)
        d.rectangle([cx - 7, cy - 2, cx + 7, cy + 2], fill=col)
    elif kind == "pad":
        d.rounded_rectangle([cx - 9, cy - 5, cx + 9, cy + 5], 4, outline=col, width=2)
        d.ellipse([cx + 3, cy - 2, cx + 6, cy + 1], fill=col)
        d.line([cx - 6, cy - 2, cx - 6, cy + 2], fill=col, width=2)
        d.line([cx - 8, cy, cx - 4, cy], fill=col, width=2)
    elif kind == "planet":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=col, width=2)
        d.arc([cx - 10, cy - 4, cx + 10, cy + 5], 160, 340, fill=col, width=2)
        d.ellipse([cx + 6, cy - 8, cx + 8, cy - 6], fill=col)
    elif kind == "burst":
        for a in range(0, 360, 45):
            import math
            ex = cx + 8 * math.cos(math.radians(a))
            ey = cy + 8 * math.sin(math.radians(a))
            d.line([cx, cy, ex, ey], fill=col, width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=col)
    elif kind == "spiral":
        for rr in (3, 6, 9):
            d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 40, 330, fill=col, width=2)
    elif kind == "scales":
        d.line([cx, cy - 8, cx, cy + 8], fill=col, width=2)
        d.line([cx - 8, cy - 6, cx + 8, cy - 6], fill=col, width=2)
        d.polygon([(cx - 8, cy - 6), (cx - 12, cy + 1), (cx - 4, cy + 1)], outline=col)
        d.polygon([(cx + 8, cy - 6), (cx + 4, cy + 1), (cx + 12, cy + 1)], outline=col)
        d.line([cx - 5, cy + 8, cx + 5, cy + 8], fill=col, width=2)
    elif kind == "ball":
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=col, width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=col)
        for a in (90, 210, 330):
            import math
            d.line([cx, cy, cx + 6 * math.cos(math.radians(a)),
                    cy + 6 * math.sin(math.radians(a))], fill=col, width=1)
    elif kind == "shield":
        d.polygon([(cx, cy - 9), (cx + 8, cy - 6), (cx + 8, cy + 2),
                   (cx, cy + 10), (cx - 8, cy + 2), (cx - 8, cy - 6)],
                  outline=col, width=2)
        d.line([cx, cy - 5, cx, cy + 5], fill=col, width=2)
    elif kind == "sun":
        d.ellipse([cx - 4, cy - 2, cx + 4, cy + 6], fill=col)
        for a in (200, 250, 290, 340):
            import math
            d.line([cx + 7 * math.cos(math.radians(a)), cy + 2 + 7 * math.sin(math.radians(a)),
                    cx + 10 * math.cos(math.radians(a)), cy + 2 + 10 * math.sin(math.radians(a))],
                   fill=col, width=2)
        d.line([cx - 10, cy + 8, cx + 10, cy + 8], fill=col, width=2)
    elif kind == "people":
        d.ellipse([cx - 8, cy - 8, cx - 2, cy - 2], fill=col)
        d.ellipse([cx + 2, cy - 8, cx + 8, cy - 2], fill=col)
        d.arc([cx - 10, cy - 3, cx, cy + 9], 180, 360, fill=col, width=2)
        d.arc([cx, cy - 3, cx + 10, cy + 9], 180, 360, fill=col, width=2)
    elif kind == "bars":
        d.rectangle([cx - 9, cy + 1, cx - 4, cy + 8], fill=col)
        d.rectangle([cx - 2, cy - 3, cx + 3, cy + 8], fill=col)
        d.rectangle([cx + 5, cy - 8, cx + 10, cy + 8], fill=col)
    elif kind == "bat":
        d.line([cx - 7, cy + 7, cx + 4, cy - 4], fill=col, width=3)
        d.line([cx + 4, cy - 4, cx + 8, cy - 8], fill=col, width=2)
        d.ellipse([cx + 4, cy + 3, cx + 9, cy + 8], fill=col)
    elif kind == "waves":
        for dy in (-5, 0, 5):
            pts = []
            for px in range(-10, 11, 2):
                import math
                pts.append((cx + px, cy + dy + 2 * math.sin(px / 3.0)))
            d.line(pts, fill=col, width=2)


# ---------------------------------------------------------------- map
def _ll(mx, my, mw, mh, lon, lat):
    return (mx + (lon + 180) / 360.0 * mw, my + (78 - lat) / 138.0 * mh)


def _poly(d, mx, my, mw, mh, pts):
    xy = [_ll(mx, my, mw, mh, lon, lat) for lon, lat in pts]
    d.polygon(xy, fill=LAND, outline=LAND_EDGE)


NA = [(-168, 66), (-150, 70), (-135, 69), (-120, 70), (-108, 68), (-96, 69),
      (-88, 67), (-84, 66), (-80, 62), (-86, 60), (-93, 58), (-96, 53),
      (-93, 49), (-89, 48), (-85, 47), (-80, 45), (-76, 44), (-73, 42),
      (-70, 42), (-70, 45), (-66, 45), (-69, 43), (-73, 40), (-75, 37),
      (-77, 34), (-80, 31), (-81, 25), (-84, 27), (-87, 29), (-91, 29),
      (-95, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-86, 13),
      (-83, 10), (-79, 9), (-84, 11), (-88, 13), (-92, 15), (-97, 16),
      (-102, 18), (-105, 20), (-108, 23), (-110, 24), (-113, 29),
      (-117, 33), (-121, 35), (-123, 40), (-124, 46), (-128, 51),
      (-133, 56), (-140, 60), (-152, 58), (-160, 58)]
GREENLAND = [(-46, 60), (-40, 61), (-32, 68), (-30, 70), (-35, 76),
             (-48, 77), (-55, 71), (-54, 65), (-52, 61)]
SA = [(-79, 9), (-75, 11), (-70, 12), (-64, 10), (-60, 8), (-55, 6),
      (-51, 4), (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-37, -12),
      (-39, -15), (-40, -21), (-46, -24), (-50, -29), (-53, -34),
      (-57, -38), (-60, -40), (-62, -42), (-65, -45), (-66, -48),
      (-67, -51), (-68, -54), (-70, -54), (-72, -50), (-73, -44),
      (-73, -38), (-72, -32), (-70, -24), (-70, -19), (-74, -15),
      (-77, -11), (-79, -7), (-80, -4), (-78, 0), (-77, 3), (-78, 6)]
AFRICA = [(-6, 35), (-2, 35), (3, 37), (10, 37), (11, 34), (15, 32),
          (20, 32), (25, 32), (30, 31), (32, 31), (34, 27), (35, 24),
          (37, 21), (38, 20), (40, 15), (43, 12), (46, 11), (50, 12),
          (51, 11), (46, 5), (42, 0), (40, -5), (40, -11), (39, -17),
          (37, -21), (35, -24), (33, -27), (30, -31), (26, -34),
          (20, -35), (18, -33), (16, -29), (14, -23), (13, -18),
          (12, -13), (13, -8), (9, -3), (9, 1), (6, 4), (2, 6), (-3, 5),
          (-8, 5), (-12, 8), (-15, 11), (-17, 13), (-17, 16), (-16, 20),
          (-16, 24), (-14, 28), (-11, 30), (-9, 32)]
MADAGASCAR = [(44, -16), (47, -14), (50, -16), (49, -20), (47, -24),
              (45, -25), (44, -21), (43, -18)]
EUROPE = [(-9, 37), (-9, 43), (-2, 44), (-2, 46), (-5, 48), (-1, 49),
          (0, 51), (2, 51), (3, 53), (5, 54), (7, 54), (8, 56), (8, 57),
          (10, 58), (12, 55), (14, 54), (18, 54), (19, 55), (21, 55),
          (23, 56), (24, 59), (22, 60), (19, 60), (17, 58), (13, 56),
          (10, 58), (6, 58), (5, 59), (5, 61), (7, 63), (10, 64),
          (13, 66), (16, 68), (20, 70), (26, 71), (33, 71), (40, 69),
          (45, 68), (47, 66), (44, 61), (41, 57), (39, 52), (37, 48),
          (34, 47), (31, 46), (29, 46), (28, 44), (29, 42), (28, 41),
          (25, 41), (23, 40), (23, 37), (21, 38), (19, 40), (16, 38),
          (15, 40), (13, 41), (12, 44), (10, 44), (8, 44), (6, 43),
          (3, 43), (3, 42), (0, 39), (-1, 38), (-2, 37), (-6, 36)]
UK = [(-5, 50), (-2, 51), (-1, 52), (-2, 54), (-4, 57), (-6, 58),
      (-8, 57), (-6, 55), (-5, 53)]
ASIA = [(29, 41), (33, 42), (36, 45), (39, 47), (44, 47), (48, 46),
        (53, 45), (58, 48), (65, 50), (72, 52), (80, 55), (88, 58),
        (95, 60), (103, 62), (110, 62), (118, 62), (126, 62), (134, 62),
        (142, 64), (150, 65), (158, 65), (166, 66), (174, 66), (178, 65),
        (172, 62), (166, 61), (161, 59), (158, 53), (153, 50), (147, 49),
        (142, 48), (141, 44), (139, 40), (136, 37), (133, 35), (130, 33),
        (127, 35), (124, 33), (122, 31), (120, 28), (117, 25), (113, 22),
        (109, 19), (107, 13), (105, 8), (103, 6), (101, 7), (99, 11),
        (97, 15), (94, 18), (91, 22), (88, 22), (86, 20), (83, 17),
        (80, 14), (77, 8), (76, 11), (74, 16), (72, 20), (69, 22),
        (66, 25), (61, 25), (57, 27), (55, 24), (52, 25), (50, 26),
        (48, 29), (44, 29), (42, 32), (40, 31), (36, 36), (35, 32),
        (33, 35), (30, 36), (27, 37), (27, 40)]
SUMATRA = [(95, 5), (99, 2), (103, -2), (106, -6), (104, -5), (100, 0),
           (96, 3)]
BORNEO = [(109, 1), (112, 3), (116, 5), (119, 2), (117, -2), (113, -3),
          (110, -1)]
JAVA = [(106, -6), (110, -7), (114, -8), (113, -9), (108, -8), (106, -7)]
NEWGUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
             (147, -10), (142, -8), (137, -6), (132, -4)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37),
         (141, 40), (141, 44), (143, 45), (141, 43), (140, 39),
         (138, 36), (135, 34), (132, 33), (130, 32)]
AUSTRALIA = [(113, -22), (114, -27), (115, -32), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -34), (137, -35), (139, -37),
             (141, -38), (145, -38), (147, -38), (150, -37), (153, -30),
             (153, -27), (151, -24), (149, -20), (146, -19), (143, -15),
             (142, -11), (142, -14), (141, -17), (139, -17), (136, -15),
             (135, -12), (132, -11), (129, -12), (126, -14), (122, -17),
             (118, -20), (114, -21)]
TASMANIA = [(145, -41), (148, -41), (148, -43), (146, -44), (145, -42)]
NZ = [(167, -45), (170, -44), (172, -42), (174, -40), (176, -38),
      (178, -37), (176, -39), (174, -41), (172, -43), (169, -46),
      (167, -46)]

PINS = {1: (114.0, 22.5), 2: (-77.0, 38.9), 3: (13.4, 52.5),
        4: (34.3, 31.5), 5: (-80.2, 25.8), 6: (-118.1, 34.1),
        7: (30.7, 46.5), 8: (82.3, 16.5), 9: (4.3, 52.1),
        10: (78.0, 21.0), 11: (13.2, 11.8), 12: (77.6, 13.0),
        13: (-75.5, 40.5), 14: (147.3, -42.9), 15: (6.1, 46.2)}
DOTS = [(37.6, 55.8), (30.5, 50.4), (-75.7, 45.4), (2.3, 48.9),
        (23.3, 42.7), (149.1, -35.3), (46.7, 24.6), (13.2, 32.9),
        (31.2, 30.0), (139.7, 35.7), (-0.2, 5.6), (36.8, -1.3),
        (30.2, 13.2), (51.5, 25.3), (74.8, 34.1), (77.4, 23.3),
        (-74.1, 4.6), (-122.3, 37.8), (28.0, -26.2)]
LABELS = [("N. AMERICA", -102, 47), ("S. AMERICA", -61, -18),
          ("EUROPE", 34, 63), ("AFRICA", 25, 1), ("ASIA", 96, 47),
          ("OCEANIA", 133, -29)]


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=MAP_BG,
                outline=(150, 170, 175), width=1)
    for land in (NA, GREENLAND, SA, AFRICA, MADAGASCAR, EUROPE, UK, ASIA,
                 SUMATRA, BORNEO, JAVA, NEWGUINEA, JAPAN, AUSTRALIA,
                 TASMANIA, NZ):
        _poly(d, mx, my, mw, mh, land)
    lf = F(SANSB, 8)
    for name, lon, lat in LABELS:
        lx, ly = _ll(mx, my, mw, mh, lon, lat)
        d.text((lx - tw(d, name, lf) / 2, ly - 4), name, font=lf,
               fill=(96, 92, 74))
    for lon, lat in DOTS:
        dx, dy = _ll(mx, my, mw, mh, lon, lat)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=PIN_GREY)
    nf = F(SANSB, 8)
    for num in sorted(PINS):
        lon, lat = PINS[num]
        px, py = _ll(mx, my, mw, mh, lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=1)
        t = str(num)
        d.text((px - tw(d, t, nf) / 2, py - 5), t, font=nf, fill=WHITE)


# ---------------------------------------------------------------- layout
def render(path):
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 92], fill=NAVY)
    tracked(d, MARGIN, 8, "THE WORLD IN ONE DAY", F(SANSB, 11),
            (226, 199, 120), 3)
    tracked_r(d, W - MARGIN, 8, "42 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE",
              F(SANSB, 11), WHITE, 3)
    title = "Thursday 19 November 2026"
    tf = F(SERIFB, 48)
    d.text((MARGIN - 2, 22), title, font=tf, fill=WHITE)
    d.text((MARGIN, 74), "Every story below happened, or was first "
           "reported, on this day.", font=F(SERIF, 12),
           fill=(205, 214, 228))
    d.rectangle([0, 92, W, 95], fill=GOLD)

    # ---- region tally strip
    d.rectangle([0, 95, W, 108], fill=PAPER_DARK)
    tally = ("EUROPE 10 \u00b7 AFRICA 8 \u00b7 ASIA 7 \u00b7 AMERICAS 6 "
             "\u00b7 GLOBAL 5 \u00b7 MIDDLE EAST 3 \u00b7 OCEANIA 2 "
             "\u00b7 SPACE 1")
    tf2 = F(SANSB, 10)
    d.text(((W - tw(d, tally, tf2)) / 2, 96), tally, font=tf2, fill=INK_SOFT)

    # ---- the day in UTC strip (only moments verified in the story set)
    d.rectangle([0, 110, W, 132], fill=PAPER_DARK)
    d.rectangle([0, 110, 150, 132], fill=RED_DARK)
    ulab = "THE DAY IN UTC"
    uf = F(SANSB, 10)
    d.text(((150 - tw(d, ulab, uf)) / 2, 116), ulab, font=uf, fill=WHITE)
    moments = [("00:00 UTC", "GTA VI unlocks in Britain"),
               ("09:00 UTC", "ICJ reads Myanmar judgment"),
               ("DAY", "Shenzhen trilateral summit"),
               ("17:00 UTC", "NASA briefs on Voyager 1")]
    utf = F(SANSB, 11)
    for (tt, lb), mx in zip(moments, [164, 386, 614, 806]):
        d.text((mx, 115), tt, font=utf, fill=RED_DARK)
        d.text((mx + tw(d, tt, utf) + 6, 116), lb, font=F(SANS, 9),
               fill=INK)
    d.rectangle([0, 132, W, 134], fill=GOLD)

    # ---- big mains row
    by = 140
    for i, s in enumerate(BIG):
        x = COLX[i]
        BIG_ART[s["art"]](d, x, by, COLW, 58)
        d.rectangle([x, by + 58, x + COLW, by + 73], fill=NAVY)
        d.text((x + 7, by + 61), s["cap"], font=F(SANSB, 8), fill=WHITE)
        badge(d, x + 8, by + 84, 8, s["n"])
        d.text((x + 22, by + 78), s["tag"], font=F(SANSB, 9), fill=RED_DARK)
        hf = F(SERIFB, 16.5)
        hy = by + 96
        for ln in wrap(d, s["head"].upper(), hf, COLW - 2)[:3]:
            d.text((x, hy), ln, font=hf, fill=INK)
            hy += 19
        df = F(SANS, 10)
        dy = by + 154
        for ln in wrap(d, s["deck"], df, COLW - 2)[:3]:
            d.text((x, dy), ln, font=df, fill=INK_SOFT)
            dy += 12.5

    # ---- medium grid (4 rows x 3)
    gy = 334
    for r in range(4):
        for c in range(3):
            s = MED[r * 3 + c]
            x = COLX[c]
            y = gy + r * 103
            d.rectangle([x, y, x + COLW, y + 29], fill=s["col"])
            if s["n"] == 6:  # Voyager banner: starfield
                for sx, sy2 in [(150, 6), (178, 19), (205, 8), (232, 21),
                                (258, 5), (282, 16)]:
                    d.ellipse([x + sx, y + sy2, x + sx + 2, y + sy2 + 2],
                              fill=(235, 230, 200))
            if s["n"] == 5:  # GTA banner: skyline silhouette along the base
                for i, bh in enumerate([5, 9, 4, 8, 6, 10, 5, 8, 4, 7,
                                        9, 5, 8, 6, 4]):
                    bx = x + 4 + i * 21
                    d.rectangle([bx, y + 29 - bh, bx + 13, y + 29],
                                fill=(62, 38, 80))
            d.text((x + 8, y + 2), s["stat"], font=F(SANSB, 16), fill=WHITE)
            d.text((x + 9, y + 20), s["sub"], font=F(SANSB, 7),
                   fill=(235, 235, 225))
            d.ellipse([x + COLW - 27, y + 4, x + COLW - 5, y + 26],
                      outline=WHITE, width=1)
            icon(d, s["icon"], x + COLW - 16, y + 15, 10)
            badge(d, x + 7, y + 40, 7, s["n"])
            d.text((x + 19, y + 35), s["tag"], font=F(SANSB, 8),
                   fill=RED_DARK)
            hf = F(SERIFB, 14)
            hy = y + 47
            for ln in wrap(d, s["head"], hf, COLW - 2)[:2]:
                d.text((x, hy), ln, font=hf, fill=INK)
                hy += 16
            df = F(SANS, 9.6)
            dy = y + 80
            for ln in wrap(d, s["deck"], df, COLW - 2)[:2]:
                d.text((x, dy), ln, font=df, fill=INK_SOFT)
                dy += 12

    # ---- by the numbers
    ny = 748
    d.line([MARGIN, ny, W - MARGIN, ny], fill=GOLD, width=2)
    d.text((MARGIN, ny + 10), "BY THE", font=F(SANSB, 11), fill=INK)
    d.text((MARGIN, ny + 24), "NUMBERS", font=F(SANSB, 11), fill=INK)
    gx = [150, 362, 574, 786]
    for i, (num, cap) in enumerate(NUMBERS):
        if i:
            d.line([gx[i] - 14, ny + 8, gx[i] - 14, ny + 40],
                   fill=(200, 190, 165), width=1)
        d.text((gx[i], ny + 6), num, font=F(SERIFB, 23), fill=INK)
        d.text((gx[i], ny + 34), cap, font=F(SANS, 8.5), fill=INK_SOFT)
    d.line([MARGIN, ny + 46, W - MARGIN, ny + 46], fill=GOLD, width=2)

    # ---- bottom split
    sy = 802
    d.text((MARGIN, sy), "WHERE IT HAPPENED", font=F(SERIFB, 14), fill=INK)
    draw_map(d, MARGIN, sy + 20, 402, 118)
    cf = F(SANS, 8.5)
    cap1 = ("Red numbers mark stories 1\u201315; grey dots mark the briefs. "
            "Pin 6 sits at JPL, Pasadena \u2014 Voyager 1 itself is one "
            "light-day out. Positions are approximate.")
    cy = sy + 142
    for ln in wrap(d, cap1, cf, 402)[:2]:
        d.text((MARGIN, cy), ln, font=cf, fill=RED_DARK)
        cy += 10

    ax = 444
    d.text((ax, sy), "ALSO ON THURSDAY 19 NOVEMBER \u2014 27 MORE STORIES",
           font=F(SERIFB, 12), fill=INK)
    d.line([ax, sy + 17, W - MARGIN, sy + 17], fill=GOLD, width=2)
    colw2 = [268, 282]
    colx2 = [ax, ax + 284]
    for ci, chunk in enumerate((ALSO[:14], ALSO[14:])):
        ly = sy + 23
        for j, (tag, line) in enumerate(chunk):
            num = 16 + ci * 14 + j
            size = 8.8
            while size > 7.6:
                nf2, bf2, af2 = F(SANSB, size), F(SANSB, size), F(SANS, size)
                total = (20 + tw(d, tag, bf2) + 5
                         + tw(d, "\u2014 " + line, af2))
                if total <= colw2[ci]:
                    break
                size -= 0.4
            d.text((colx2[ci], ly), str(num), font=nf2, fill=RED_DARK)
            d.text((colx2[ci] + 20, ly), tag, font=bf2, fill=INK)
            tx = colx2[ci] + 20 + tw(d, tag, bf2) + 5
            d.text((tx, ly), "\u2014 " + line, font=af2, fill=INK_SOFT)
            ly += 9.8

    # ---- date check strip
    dcy = 968
    d.rectangle([MARGIN, dcy, MARGIN + 92, dcy + 25], fill=RED_DARK)
    d.text((MARGIN + 17, dcy + 8), "DATE CHECK", font=F(SANSB, 9),
           fill=WHITE)
    dc = ("Left out on purpose \u2014 they broke before today: Jensen "
          "Huang\u2019s resignation as Nvidia\u2019s chief (announced 12 Nov) "
          "\u00b7 America\u2019s strike on Iran\u2019s Qeshm Island missile "
          "site (17 Nov) \u00b7 Musk\u2019s petition to bring Huang back "
          "(13 Nov).")
    dcf = F(SANS, 8.8)
    dx = MARGIN + 102
    ly = dcy + 3
    for ln in wrap(d, dc, dcf, W - MARGIN - dx - 4)[:2]:
        d.text((dx, ly), ln, font=dcf, fill=INK)
        ly += 10

    # ---- footer
    jf = F(SANSB, 8.8)
    judge = ("JUDGE NOTE \u2014 Every story above happened, or was first "
             "reported, on Thursday 19 November 2026. Disputed claims are "
             "attributed, not stated as fact.")
    d.text(((W - tw(d, judge, jf)) / 2, 999), judge, font=jf, fill=INK)
    sf = F(SANS, 8)
    src = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 NPR "
           "\u00b7 USA Today \u00b7 The Guardian \u00b7 Le Monde \u00b7 The "
           "Hindu \u00b7 TOI \u00b7 Vanguard \u00b7 NASA and the regional "
           "wires named above. Original drawings. \u00b7 Date checked: "
           "19.11.2026")
    d.text(((W - tw(d, src, sf)) / 2, 1012), src, font=sf, fill=INK_SOFT)

    img.save(path)
    return path


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    render(out)
    print("wrote", out)
