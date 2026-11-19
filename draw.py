#!/usr/bin/env python3
"""THE WORLD IN ONE PICTURE — front page for Thursday 19 November 2026.

Original renderer written for the make.fun news-image-20261119 entry.
Draws a 1024x1024 newspaper front page with PIL: navy masthead with a
gold rule, three large illustrated mains, a dotted world map with pins,
a slim Day in Numbers strip, nine medium mains and an ALSO one-liner tier.
All stories were verified against the sources named in the decks and in
the footer on 19 November 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (24, 26, 32)
NAVY = (13, 33, 62)
NAVY2 = (22, 52, 92)
GOLD = (201, 152, 46)
GOLD_LT = (226, 190, 105)
RED = (178, 34, 44)
GREY = (96, 98, 104)
PANEL = (238, 231, 211)
PANEL2 = (233, 224, 198)
LINE = (178, 168, 142)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS_O = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    """Greedy word wrap returning a list of lines."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def text_block(d, x, y, text, font, fill, maxw, lh, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (kicker, headline, deck, pin lat, pin lon, illustration key)
LARGE = [
    (
        "SHENZHEN, CHINA · APEC SUMMIT",
        "Three Presidents, One Table: Trump, Xi and Putin Meet in Shenzhen",
        "The first trilateral ever held by the US, Chinese and Russian leaders caps "
        "the APEC summit. Trump presses nuclear arms control; the Kremlin allots "
        "one hour and says no full-scale talks are planned. (Reuters)",
        22.5, 114.1, "shenzhen",
    ),
    (
        "WASHINGTON · US POLITICS",
        "Jeffries Nominated for Speaker in Democrats' Midterm Landslide",
        "House Democrats pick Hakeem Jeffries 251-11: he would be the first Black "
        "Speaker. The party holds at least 257 House seats and a 56-44 Senate "
        "majority after the midterms. (NPR, USA Today)",
        38.9, -77.0, "capitol",
    ),
    (
        "BERLIN · UKRAINE WAR",
        "Europe Closes Ranks for Kyiv as US Envoys Join Berlin Talks",
        "Germany, France, Britain, Poland and Italy meet Zelenskiy alongside Trump's "
        "envoys Witkoff and Kushner, seeking binding security guarantees. Brussels "
        "proposes a EUR 45bn loan. (Reuters)",
        52.5, 13.4, "berlin",
    ),
]

MEDIUM = [
    (
        "GAZA CITY · MIDDLE EAST",
        "Israeli Tanks Push Into Central Gaza; Three Killed, Medics Say",
        "Tanks reach the Salahudeen road as Trump's Board of Peace faults both "
        "sides; 1,600+ killed since the Oct 2025 ceasefire, Gaza medics say. (Reuters)",
        31.5, 34.5, "gaza",
    ),
    (
        "VICE CITY · GAMING",
        "After 13 Years, Grand Theft Auto VI Finally Arrives",
        "The decade's most anticipated game begins its global rollout. Burna Boy "
        "is the first African to host an in-game radio station. (AP, BBC)",
        25.8, -80.2, "gta",
    ),
    (
        "DEEP SPACE · SCIENCE",
        "Voyager 1 Reaches One Light-Day From Earth",
        "Nearly 50 years after launch, the probe is so far out its signal takes "
        "a full day to reach home; NASA confirms Thursday. (NASA)",
        62.0, 168.0, "voyager",
    ),
    (
        "ODESA · UKRAINE",
        "Russian Strikes on Odesa Kill Four, Officials Say",
        "Three waves hit the Black Sea port's centre, wounding at least seven "
        "and damaging a school, the regional governor says. (Reuters)",
        46.5, 30.7, "odesa",
    ),
    (
        "ANDHRA PRADESH · WEATHER",
        "Cyclone Akvan Bears Down on India's East Coast",
        "Set to intensify into a very severe cyclonic storm before crossing "
        "between Machilipatnam and Puri on 20 November. (The Hindu)",
        16.3, 80.7, "cyclone",
    ),
    (
        "THE HAGUE · WORLD COURT",
        "ICJ Rules on Whether Myanmar Committed Genocide",
        "The Gambia's case over the Rohingya, backed by 57 OIC states, reaches "
        "judgment; the UN says 10,000+ Rohingya were killed in 2017. (Le Monde)",
        52.1, 4.3, "icj",
    ),
    (
        "DHAKA · SPORT",
        "India Beat Pakistan 2-1 to Lift the SAFF Championship",
        "A Dhaka final settles South Asia's football crown in India's favour. "
        "(Times of India)",
        23.8, 90.4, "saff",
    ),
    (
        "BORNO · NIGERIA",
        "Troops Kill 21 Suspected ISWAP Fighters in Borno",
        "The army reports the operation in Nigeria's north-east, where the "
        "insurgency has now run for over a decade. (Vanguard)",
        11.8, 13.2, "borno",
    ),
    (
        "BENGALURU · BUSINESS",
        "Amazon Pledges $7bn for Renewable Energy in India",
        "Running to 2030, it ranks among the largest clean-energy pledges by a "
        "technology firm in the country. (Times of India)",
        13.0, 77.6, "solar",
    ),
]

ALSO = [
    "Ukraine's drone campaign cuts Russian oil refining ~45% since late Oct; 15 of 35 big refineries disrupted (Reuters)",
    "Ukraine defence contact group agrees fresh arms deliveries for the winter (Reuters)",
    "Schumer faces a Van Hollen challenge for Senate majority leader (NPR)",
    "Pew: Islam on track to become the world's largest religion by 2035 (NDTV)",
    "Canada's Carney adjusts China ties while seeking 'the right deal' with the US (AP)",
    "US senators warn AI-enabled cyber threats are outpacing defences (reports)",
    "Russia accuses France of deploying troops to Ukraine, via Lavrov (AFP)",
    "France's justice minister says far-left leader Melenchon could win the presidency (reports)",
    "LPG tanker that sank off Bulgaria was hit by projectiles, an official says (reports)",
    "Australia sanctions Israeli settlers over West Bank expansion (reports)",
    "Saudi Arabia says danger has passed in three southern cities after alerts (reports)",
    "Cocaine and millions of pills seized in eastern Libya, officials say (reports)",
    "Egypt and Syria sign an aviation pact ahead of resumed flights (Daily News Egypt)",
    "India and Japan review defence ties as Rajnath Singh and Jaishankar arrive in Tokyo (reports)",
    "Ghana banks' bad-loan ratio falls to 13.1% in October (MyJoyOnline)",
    "Morocco's defence-industry roadmap targets 50,000 jobs by 2035 (Hespress)",
    "Kenya's Ruto delivers his fourth State of the Nation address (Daily Nation)",
    "Rights group: RSF drone strikes on civilians in Sudan's El Obeid may be war crimes (PANA)",
    "Nearly 2,500 dead or missing on sea routes to Europe in nine months, UNHCR says (PANA)",
    "COP31 in Antalya takes up protection of the warming oceans (PANA)",
    "Scientists may have solved Earth's 'missing' billion years of rock (Space.com)",
    "US defence chief Hegseth to visit Colombia for security talks (reports)",
    "FIFA U-17 World Cup opens in Doha; hosts Qatar face Panama (reports)",
    "Duckett hits 133 as England take control of the third ODI v Australia (reports)",
    "Cote d'Ivoire snatch a late draw against Gambia in AFCON 2027 qualifying (PANA)",
    "LeT militant Lateef Bhat killed in a Kulgam encounter in Kashmir (Times of India)",
    "India's women open their Asian Champions Trophy hockey campaign v Malaysia in Bhopal (TOI)",
]

# small map dots for ALSO stories: (lat, lon)
ALSO_PINS = [
    (54.0, 50.0), (50.4, 30.5), (38.9, -77.0), (21.0, 78.0), (45.4, -75.7),
    (38.9, -77.0), (48.9, 2.3), (48.9, 2.3), (42.7, 27.7), (-35.3, 149.1),
    (24.6, 46.7), (32.9, 13.2), (30.0, 31.2), (35.7, 139.7), (5.6, -0.2),
    (34.0, -6.8), (-1.3, 36.8), (13.2, 30.2), (36.0, 15.0), (36.9, 30.7),
    (39.0, -98.0), (4.7, -74.1), (25.3, 51.5), (-25.0, 133.0), (13.5, -16.6),
    (33.6, 75.0), (23.3, 77.4),
]

NUMBERS = [
    ("251-11", "Jeffries' nomination vote among House Democrats"),
    ("EUR 45bn", "EU loan proposed for Ukraine, to be repaid from reparations"),
    ("45%", "Russian oil refining cut by Ukrainian drone strikes since late Oct"),
    ("56-44", "Democrats' new majority in the US Senate"),
    ("13 yrs", "the wait for Grand Theft Auto VI, over at last"),
    ("1", "light-day: the distance Voyager 1's signal now travels"),
]

N_STORIES = len(LARGE) + len(MEDIUM) + len(ALSO)


# ------------------------------------------------------------ illustrations
def _sky(d, box, top, bot):
    x0, y0, x1, y1 = box
    steps = 24
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        yy = y0 + (y1 - y0) * i // steps
        d.rectangle([x0, yy, x1, y0 + (y1 - y0) * (i + 1) // steps + 1], fill=c)


def ill_shenzhen(d, b):
    _sky(d, b, (16, 42, 84), (96, 138, 186))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * .78, y0 + h * .08, x0 + w * .92, y0 + h * .30], fill=(244, 205, 105))
    rng = [(.02, .55, .10), (.13, .38, .09), (.24, .62, .12), (.38, .45, .08),
           (.50, .58, .11), (.63, .40, .09), (.74, .60, .10), (.87, .48, .09)]
    for fx, fh, fw in rng:
        d.rectangle([x0 + w * fx, y1 - h * fh, x0 + w * (fx + fw), y1], fill=(13, 28, 54))
    for i, col in enumerate([(178, 34, 44), (36, 84, 160), (178, 34, 44)]):
        px = x0 + w * (.18 + .24 * i)
        d.line([px, y0 + h * .16, px, y0 + h * .52], fill=(230, 230, 220), width=3)
        d.rectangle([px, y0 + h * .16, px + w * .13, y0 + h * .30], fill=col)
        if i == 0:
            d.text((px + 3, y0 + h * .17), "*", font=F(SANS_B, 11), fill=(250, 220, 90))


def ill_capitol(d, b):
    _sky(d, b, (24, 52, 102), (120, 152, 196))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) // 2
    d.rectangle([x0 + w * .12, y1 - h * .34, x1 - w * .12, y1], fill=(226, 220, 200))
    for i in range(7):
        px = x0 + w * (.17 + .105 * i)
        d.rectangle([px, y1 - h * .34, px + w * .035, y1 - h * .06], fill=(168, 160, 140))
    d.pieslice([cx - w * .17, y1 - h * .72, cx + w * .17, y1 - h * .10], 180, 360, fill=(238, 233, 214))
    d.rectangle([cx - w * .015, y1 - h * .78, cx + w * .015, y1 - h * .58], fill=(238, 233, 214))
    d.ellipse([cx - 3, y1 - h * .84, cx + 3, y1 - h * .76], fill=GOLD_LT)


def ill_berlin(d, b):
    _sky(d, b, (28, 58, 108), (128, 158, 198))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0 + w * .16, y1 - h * .78, x1 - w * .16, y1 - h * .68], fill=(196, 172, 118))
    for i in range(6):
        px = x0 + w * (.18 + .115 * i)
        d.rectangle([px, y1 - h * .68, px + w * .055, y1], fill=(206, 184, 130))
    d.rectangle([x0 + w * .40, y1 - h * .86, x0 + w * .60, y1 - h * .78], fill=(150, 128, 84))
    d.rectangle([x0 + w * .47, y1 - h * .94, x0 + w * .53, y1 - h * .86], fill=(150, 128, 84))
    for i in range(5):
        sx = x0 + w * (.70 + .055 * i)
        d.text((sx, y0 + h * .10), "*", font=F(SANS_B, 13), fill=GOLD_LT)


def ill_gaza(d, b):
    _sky(d, b, (120, 116, 110), (196, 186, 168))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * .06, y0 + h * .08, x0 + w * .20, y0 + h * .30], fill=(232, 214, 170))
    blocks = [(.02, .52), (.14, .70), (.27, .44), (.38, .64), (.52, .50), (.64, .72), (.78, .46), (.88, .60)]
    for fx, fh in blocks:
        d.rectangle([x0 + w * fx, y1 - h * fh, x0 + w * (fx + .11), y1], fill=(104, 98, 92))
    d.line([x0 + w * .30, y1 - h * .44, x0 + w * .36, y1 - h * .20], fill=(88, 82, 76), width=3)
    d.line([x0 + w * .68, y1 - h * .72, x0 + w * .74, y1 - h * .50], fill=(88, 82, 76), width=3)
    for fx, fy in [(.33, .82), (.70, .30)]:
        d.ellipse([x0 + w * fx, y0 + h * fy, x0 + w * (fx + .10), y0 + h * (fy + .16)], fill=(150, 144, 134))


def ill_gta(d, b):
    _sky(d, b, (252, 140, 90), (120, 60, 140))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * .36, y0 + h * .22, x0 + w * .64, y0 + h * .62], fill=(255, 196, 86))
    d.rectangle([x0, y1 - h * .18, x1, y1], fill=(30, 22, 48))
    for fx in (.08, .84):
        px = x0 + w * fx
        d.line([px, y1 - h * .18, px, y0 + h * .30], fill=(24, 18, 36), width=4)
        for a in range(6):
            import math
            ang = a * 3.14159 / 3
            d.line([px, y0 + h * .30, px + 16 * math.cos(ang), y0 + h * .30 - 9 * abs(math.sin(ang)) - 2],
                   fill=(24, 18, 36), width=3)
    d.rounded_rectangle([x0 + w * .38, y1 - h * .30, x0 + w * .64, y1 - h * .17], 6, fill=(16, 14, 26))
    d.ellipse([x0 + w * .41, y1 - h * .21, x0 + w * .46, y1 - h * .13], fill=(200, 200, 210))
    d.ellipse([x0 + w * .56, y1 - h * .21, x0 + w * .61, y1 - h * .13], fill=(200, 200, 210))


def ill_voyager(d, b):
    d.rectangle(b, fill=(6, 8, 20))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    import random
    random.seed(19)
    for _ in range(60):
        sx, sy = x0 + random.random() * w, y0 + random.random() * h
        r = random.choice([1, 1, 2])
        d.ellipse([sx, sy, sx + r, sy + r], fill=(230, 232, 240))
    cx, cy = x0 + w * .42, y0 + h * .58
    d.arc([cx - w * .20, cy - h * .34, cx + w * .20, cy + h * .30], 300, 130, fill=(226, 190, 105), width=4)
    d.line([cx, cy, cx + w * .16, cy - h * .30], fill=(226, 190, 105), width=3)
    d.ellipse([cx + w * .145, cy - h * .33, cx + w * .175, cy - h * .27], fill=(240, 220, 150))
    for i in range(3):
        d.arc([cx + w * .20 + i * 9, cy - h * .42 - i * 6, cx + w * .44 + i * 9, cy - h * .02 + i * 4],
              280, 60, fill=(120, 170, 240), width=2)


def ill_odesa(d, b):
    _sky(d, b, (70, 110, 160), (170, 196, 220))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y1 - h * .30, x1, y1], fill=(44, 92, 138))
    for fx in (.12, .55):
        px = x0 + w * fx
        d.line([px, y1 - h * .30, px, y0 + h * .18], fill=(40, 44, 52), width=4)
        d.line([px, y0 + h * .18, px + w * .26, y0 + h * .30], fill=(40, 44, 52), width=3)
        d.line([px + w * .10, y0 + h * .24, px + w * .10, y1 - h * .42], fill=(40, 44, 52), width=2)
    d.rectangle([x0 + w * .30, y1 - h * .34, x0 + w * .52, y1 - h * .26], fill=(120, 40, 40))
    d.rectangle([x0 + w * .36, y1 - h * .40, x0 + w * .46, y1 - h * .34], fill=(90, 90, 96))


def ill_cyclone(d, b):
    _sky(d, b, (88, 108, 128), (168, 182, 192))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * .5, y0 + h * .42
    import math
    for r in (34, 25, 16, 8):
        d.arc([cx - r, cy - r * .62, cx + r, cy + r * .62], 20, 300, fill=(240, 244, 248), width=4)
    d.rectangle([x0, y1 - h * .22, x1, y1], fill=(38, 84, 124))
    for i in range(5):
        wx = x0 + w * (.06 + .19 * i)
        d.arc([wx, y1 - h * .26, wx + w * .12, y1 - h * .12], 180, 360, fill=(210, 230, 244), width=3)


def ill_icj(d, b):
    _sky(d, b, (30, 62, 110), (110, 142, 188))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) // 2
    d.polygon([(cx, y0 + h * .10), (x0 + w * .14, y1 - h * .62), (x1 - w * .14, y1 - h * .62)], fill=(232, 226, 206))
    d.rectangle([x0 + w * .14, y1 - h * .62, x1 - w * .14, y1 - h * .56], fill=(200, 190, 160))
    for i in range(5):
        px = x0 + w * (.20 + .14 * i)
        d.rectangle([px, y1 - h * .56, px + w * .05, y1 - h * .08], fill=(226, 220, 198))
    d.rectangle([x0 + w * .10, y1 - h * .08, x1 - w * .10, y1], fill=(180, 168, 138))
    d.line([cx, y0 + h * .30, cx, y0 + h * .48], fill=GOLD_LT, width=3)
    d.line([cx - w * .10, y0 + h * .34, cx + w * .10, y0 + h * .34], fill=GOLD_LT, width=3)


def ill_saff(d, b):
    _sky(d, b, (34, 110, 62), (96, 176, 110))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y1 - h * .26, x1, y1], fill=(26, 92, 50))
    cx, cy = x0 + w * .36, y0 + h * .46
    d.ellipse([cx - 21, cy - 21, cx + 21, cy + 21], fill=(245, 245, 245), outline=(30, 30, 30), width=2)
    d.polygon([(cx, cy - 8), (cx + 8, cy - 2), (cx + 5, cy + 7), (cx - 5, cy + 7), (cx - 8, cy - 2)], fill=(30, 30, 30))
    gx = x0 + w * .68
    d.rectangle([gx - 14, y0 + h * .22, gx + 14, y0 + h * .34], fill=GOLD_LT)
    d.arc([gx - 20, y0 + h * .20, gx - 4, y0 + h * .36], 90, 270, fill=GOLD_LT, width=3)
    d.arc([gx + 4, y0 + h * .20, gx + 20, y0 + h * .36], 270, 90, fill=GOLD_LT, width=3)
    d.rectangle([gx - 3, y0 + h * .34, gx + 3, y0 + h * .44], fill=GOLD_LT)
    d.rectangle([gx - 11, y0 + h * .44, gx + 11, y0 + h * .50], fill=GOLD_LT)


def ill_borno(d, b):
    _sky(d, b, (196, 138, 52), (232, 190, 110))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * .76, y0 + h * .06, x0 + w * .94, y0 + h * .28], fill=(250, 226, 150))
    d.rectangle([x0, y1 - h * .18, x1, y1], fill=(150, 104, 52))
    cx = (x0 + x1) // 2
    d.polygon([(cx, y0 + h * .16), (cx + w * .14, y0 + h * .24), (cx + w * .14, y0 + h * .52),
               (cx, y1 - h * .14), (cx - w * .14, y0 + h * .52), (cx - w * .14, y0 + h * .24)],
              fill=(46, 110, 62))
    d.text((cx - 7, y0 + h * .32), "*", font=F(SANS_B, 26), fill=(250, 240, 210))


def ill_solar(d, b):
    _sky(d, b, (44, 100, 168), (140, 186, 226))
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * .06, y0 + h * .06, x0 + w * .24, y0 + h * .30], fill=(252, 216, 100))
    d.rectangle([x0, y1 - h * .14, x1, y1], fill=(74, 130, 74))
    for r in range(2):
        for c in range(3):
            px = x0 + w * (.14 + .26 * c)
            py = y1 - h * (.52 - .20 * r)
            d.polygon([(px, py), (px + w * .20, py - h * .05), (px + w * .23, py + h * .11), (px + w * .03, py + h * .16)],
                      fill=(26, 60, 130), outline=(160, 200, 240))
    d.polygon([(x0 + w * .80, y1 - h * .40), (x0 + w * .86, y1 - h * .62), (x0 + w * .92, y1 - h * .40)], fill=(52, 118, 62))


ILL = {
    "shenzhen": ill_shenzhen, "capitol": ill_capitol, "berlin": ill_berlin,
    "gaza": ill_gaza, "gta": ill_gta, "voyager": ill_voyager, "odesa": ill_odesa,
    "cyclone": ill_cyclone, "icj": ill_icj, "saff": ill_saff, "borno": ill_borno,
    "solar": ill_solar,
}


# ------------------------------------------------------------------- map
# Coarse land model: (lat_min, lat_max, lon_min, lon_max) boxes. The dots
# only need to read as a world map at front-page scale.
LAND_BOXES = [
    (50, 72, -168, -125), (42, 70, -125, -85), (35, 55, -85, -55),
    (28, 42, -100, -70), (24, 33, -107, -87), (14, 28, -112, -90),
    (7, 18, -92, -77), (60, 80, -58, -32),
    (5, 11, -77, -62), (-2, 5, -80, -50), (-12, -2, -70, -38),
    (-24, -12, -66, -40), (-38, -24, -70, -52), (-52, -38, -73, -62),
    (58, 71, 5, 31), (48, 60, -6, 28), (43, 49, -2, 30), (36, 44, -9, 3),
    (38, 46, 8, 19), (50, 59, -5, 2),
    (15, 32, -17, 32), (5, 15, -17, 40), (-5, 5, -12, 42),
    (-18, -5, 12, 40), (-30, -18, 12, 36), (-35, -29, 17, 33),
    (-25, -12, 43, 50),
    (50, 70, 30, 180), (42, 52, 30, 135), (30, 42, 35, 63),
    (12, 30, 35, 59), (25, 38, 44, 75), (20, 35, 68, 89), (8, 20, 73, 80),
    (10, 28, 92, 108), (5, 20, 98, 105), (35, 50, 78, 122),
    (22, 35, 90, 122), (42, 50, 88, 120), (35, 42, 126, 130),
    (35, 45, 129, 142), (6, 18, 117, 126),
    (0, 6, 95, 120), (-8, 0, 105, 120), (-5, 0, 119, 141), (-9, -1, 131, 147),
    (-12, -25, 113, 150), (-25, -39, 114, 153), (-46, -34, 167, 178),
]


def is_land(lat, lon):
    return any(a <= lat <= b and c <= lon <= e for a, b, c, e in LAND_BOXES)


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 218, 190))
    d.rectangle(box, outline=LINE, width=1)
    lon_step, lat_step = 3.0, 3.3
    pw = (x1 - x0) / (360 / lon_step)
    ph = (y1 - y0) / (140 / lat_step)
    r = max(1.4, min(pw, ph) * 0.30)
    lat = 76.0
    row = 0
    while lat > -64:
        lon = -180.0
        col = 0
        while lon < 180:
            if is_land(lat, lon):
                cx = x0 + (col + 0.5) * pw
                cy = y0 + (row + 0.5) * ph
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 128, 84))
            lon += lon_step
            col += 1
        lat -= lat_step
        row += 1

    def pin(lat_, lon_, num=None, big=True):
        px = x0 + (lon_ + 180) / 360 * (x1 - x0)
        py = y0 + (76 - lat_) / 140 * (y1 - y0)
        if big:
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 245, 230), width=1)
            if num is not None:
                t = str(num)
                f = F(SANS_B, 9)
                tw = d.textlength(t, font=f)
                d.text((px - tw / 2, py - 5), t, font=f, fill=(255, 250, 240))
        else:
            d.ellipse([px - 2.4, py - 2.4, px + 2.4, py + 2.4], fill=NAVY2)

    for la, lo in ALSO_PINS:
        pin(la, lo, big=False)
    mains = LARGE + MEDIUM
    for i, s in enumerate(mains, 1):
        if s[5] == "voyager":
            continue
        pin(s[3], s[4], num=i)
    # Voyager 1: a star beyond the map's top-right corner (deep space).
    sx, sy = x1 - 26, y0 + 16
    d.text((sx, sy), "*", font=F(SANS_B, 20), fill=RED)
    d.text((sx - 64, sy + 2), "6", font=F(SANS_B, 9), fill=RED)


# ----------------------------------------------------------------- render
def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=GOLD)
    title = "THE WORLD IN ONE PICTURE"
    tf = F(SERIF_B, 39)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=GOLD_LT)
    sub = F(SANS_B, 13)
    left = "Thursday, 19 November 2026"
    mid = "%d STORIES · SIX CONTINENTS · ONE DAY" % N_STORIES
    right = "ONE IMAGE · ONE DAY"
    d.text((18, 58), left, font=sub, fill=(235, 238, 244))
    mw = d.textlength(mid, font=sub)
    d.text(((W - mw) / 2, 58), mid, font=sub, fill=(255, 255, 255))
    rw = d.textlength(right, font=sub)
    d.text((W - 18 - rw, 58), right, font=sub, fill=(235, 238, 244))

    # Large mains
    ly, lh = 94, 272
    colw, gap = 325, 8
    for i, (kick, head, deck, la, lo, key) in enumerate(LARGE):
        x = 16 + i * (colw + gap)
        ILL[key](d, (x, ly, x + colw, ly + 118))
        d.rectangle([x, ly, x + colw, ly + 118], outline=LINE)
        y = ly + 124
        d.text((x, y), "%d · %s" % (i + 1, kick), font=F(SANS_B, 11), fill=RED)
        y = text_block(d, x, y + 15, head, F(SERIF_B, 20), INK, colw, 23, 3)
        text_block(d, x, y + 3, deck, F(SANS, 12), (52, 54, 60), colw, 15, 4)
    d.line([16, ly + lh + 4, W - 16, ly + lh + 4], fill=LINE, width=1)

    # Map + Day in Numbers
    my = ly + lh + 12
    draw_map(d, (16, my, 664, my + 160))
    d.rectangle([672, my, W - 16, my + 160], fill=NAVY)
    d.text((688, my + 7), "THE DAY IN NUMBERS", font=F(SANS_B, 14), fill=GOLD_LT)
    ny = my + 30
    for num, lab in NUMBERS:
        nf = F(SERIF_B, 21)
        d.text((688, ny), num, font=nf, fill=(255, 255, 255))
        nw = d.textlength(num, font=nf)
        text_block(d, 688 + nw + 10, ny + 4, lab, F(SANS, 10.5), (214, 220, 232),
                   W - 16 - (688 + nw + 10), 12.5, 2)
        ny += 21

    # Medium mains: 3 x 3 cards
    gy = my + 168
    cardh = 73
    for idx, (kick, head, deck, la, lo, key) in enumerate(MEDIUM):
        r, c = divmod(idx, 3)
        x = 16 + c * (colw + gap)
        y = gy + r * (cardh + 4)
        d.rectangle([x, y, x + colw, y + cardh], fill=PANEL, outline=LINE)
        ILL[key](d, (x + 4, y + 4, x + 66, y + cardh - 4))
        tx = x + 74
        d.text((tx, y + 3), "%d · %s" % (idx + 4, kick), font=F(SANS_B, 8.5), fill=RED)
        yy = text_block(d, tx, y + 14, head, F(SERIF_B, 12.5), INK, colw - 80, 13.5, 2)
        text_block(d, tx, yy + 1, deck, F(SANS, 9), (52, 54, 60), colw - 80, 10, 3)

    # ALSO tier
    ay = gy + 3 * cardh + 2 * 4 + 4
    d.rectangle([16, ay, W - 16, ay + 18], fill=NAVY2)
    d.text((24, ay + 3), "ALSO ON THURSDAY", font=F(SANS_B, 12), fill=(255, 255, 255))
    d.text((300, ay + 4), "the rest of the day, in one line each", font=F(SANS_O, 10), fill=(205, 214, 232))
    col_w3 = (W - 32 - 16) // 3
    per = (len(ALSO) + 2) // 3
    af = F(SANS, 9)
    for ci in range(3):
        x = 16 + ci * (col_w3 + 8)
        y = ay + 24
        for j in range(per):
            k = ci * per + j
            if k >= len(ALSO):
                break
            num = "%2d." % (k + 13)
            d.text((x, y), num, font=F(SANS_B, 9), fill=RED)
            text_block(d, x + 20, y, ALSO[k], af, (40, 42, 48), col_w3 - 20, 9.8, 2)
            y += 19.5

    # Footer
    fy = H - 34
    d.line([16, fy - 4, W - 16, fy - 4], fill=GOLD, width=2)
    d.text((16, fy + 2),
           "Sources: Reuters · AP · AFP · BBC · NPR · USA Today · Le Monde · The Hindu · Times of India · "
           "PANA · Vanguard · Daily Nation · Hespress · MyJoyOnline · Space.com · NASA",
           font=F(SANS, 9.5), fill=GREY)
    d.text((16, fy + 15),
           "Original drawings; no photographs. Figures as reported by the sources named; disputed claims are attributed. "
           "Map pins: numbered = main stories, dots = also-covered.",
           font=F(SANS_O, 9.5), fill=GREY)

    img.save(path)
    return path


if __name__ == "__main__":
    render("entry.png")
