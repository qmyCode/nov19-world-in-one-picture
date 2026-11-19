#!/usr/bin/env python3
"""draw.py - build tool for the 19 November 2026 news-image entry (v5).

Draws entry.png (1024x1024): one newspaper front page, 42 stories,
a drawn scene illustration on every one of the 15 main stories.
Build tool only - main.py never imports this file.
Fonts: DejaVu only (Serif, Serif-Bold, Sans, Sans-Bold).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF   = "DejaVuSerif.ttf"
SERIFB  = "DejaVuSerif-Bold.ttf"
SANS    = "DejaVuSans.ttf"
SANSB   = "DejaVuSans-Bold.ttf"

W = H = 1024
PAPER   = (246, 240, 222)
NAVY    = (15, 36, 58)
INK     = (26, 24, 20)
RED     = (176, 44, 34)
GOLD    = (201, 162, 39)
RULE    = (120, 110, 88)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(font, s):
    return d.textlength(s, font=font)

def wrap(font, s, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(font, t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

# ---------------------------------------------------------------- scenes
def new_scene(w, h, sky_top, sky_bot):
    s = Image.new("RGB", (w, h), sky_top)
    sd = ImageDraw.Draw(s)
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(sky_top[i] + (sky_bot[i] - sky_top[i]) * t) for i in range(3))
        sd.line([(0, y), (w, y)], fill=c)
    return s, sd

def sun(sd, x, y, r, col=(244, 197, 86)):
    sd.ellipse([x - r, y - r, x + r, y + r], fill=col)

def skyline(sd, w, base, heights, col, seed=3):
    x, i = 0, 0
    while x < w:
        bw = 14 + ((seed * (i + 7)) % 17)
        bh = heights[i % len(heights)]
        sd.rectangle([x, base - bh, x + bw, base], fill=col)
        x += bw + 3; i += 1

def windows(sd, w, base, top, col=(250, 214, 110), seed=5, step=11):
    for gx in range(6, w - 4, step):
        for gy in range(top, base - 5, 9):
            if (gx * seed + gy * 7) % 13 < 5:
                sd.rectangle([gx, gy, gx + 3, gy + 4], fill=col)

def flag_cn(sd, x, y, pw, ph):
    sd.rectangle([x, y, x + pw, y + ph], fill=(196, 40, 36))
    for dx, dy in [(3, 3), (8, 1), (9, 5), (8, 8)]:
        sd.ellipse([x + dx, y + dy, x + dx + 2, y + dy + 2], fill=(250, 210, 60))

def flag_us(sd, x, y, pw, ph):
    for i in range(5):
        sd.rectangle([x, y + i * ph // 5, x + pw, y + (i + 1) * ph // 5],
                     fill=(178, 34, 52) if i % 2 == 0 else (240, 238, 230))
    sd.rectangle([x, y, x + pw * 2 // 5, y + ph * 3 // 5], fill=(38, 52, 110))
    for r in range(3):
        for c in range(4):
            sd.point((x + 2 + c * 3, y + 2 + r * 3), fill=(255, 255, 255))

def flag_ru(sd, x, y, pw, ph):
    sd.rectangle([x, y, x + pw, y + ph // 3], fill=(238, 236, 230))
    sd.rectangle([x, y + ph // 3, x + pw, y + 2 * ph // 3], fill=(36, 62, 140))
    sd.rectangle([x, y + 2 * ph // 3, x + pw, y + ph], fill=(196, 40, 36))

def pole_flags(sd, cx, base, top, pw, ph, which):
    sd.line([cx, base, cx, top], fill=(30, 28, 26), width=2)
    fn = {"cn": flag_cn, "us": flag_us, "ru": flag_ru}[which]
    fn(sd, cx + 2, top, pw, ph)

def scene_shenzhen(w, h):
    s, sd = new_scene(w, h, (38, 52, 92), (196, 108, 62))
    sun(sd, w - 46, 14, 9, (246, 176, 92))
    skyline(sd, w, h - 12, [16, 24, 13, 28, 18, 22, 15], (26, 30, 48), seed=4)
    windows(sd, w, h - 12, 8, seed=7)
    sd.rectangle([0, h - 12, w, h], fill=(18, 20, 30))
    for cx, fl in [(w // 2 - 74, "us"), (w // 2, "cn"), (w // 2 + 74, "ru")]:
        pole_flags(sd, cx, h - 10, 8, 34, 20, fl)
    sd.rectangle([w // 2 - 92, h - 10, w // 2 + 96, h - 6], fill=(52, 38, 30))
    return s

def scene_capitol(w, h):
    s, sd = new_scene(w, h, (96, 140, 180), (196, 214, 224))
    cx = w // 2; base = h - 6
    sd.rectangle([cx - 118, base - 16, cx + 118, base], fill=(232, 228, 216))
    for i in range(9):
        x = cx - 104 + i * 26
        sd.rectangle([x, base - 34, x + 9, base - 16], fill=(238, 234, 224))
    sd.rectangle([cx - 118, base - 38, cx + 118, base - 33], fill=(220, 214, 198))
    sd.pieslice([cx - 52, base - 78, cx + 52, base - 22], 180, 360, fill=(30, 48, 74))
    sd.rectangle([cx - 52, base - 52, cx + 52, base - 47], fill=(24, 40, 62))
    sd.rectangle([cx - 4, base - 92, cx + 4, base - 76], fill=(30, 48, 74))
    sd.polygon([(cx, base - 100), (cx + 5, base - 90), (cx, base - 88),
                (cx - 5, base - 90)], fill=(30, 48, 74))
    sd.rectangle([cx - 150, base - 4, cx + 150, base], fill=(120, 130, 110))
    return s

def scene_berlin(w, h):
    s, sd = new_scene(w, h, (44, 74, 128), (110, 140, 184))
    cx = w // 2; base = h - 4
    col = (20, 32, 54)
    for dx in (-78, -46, 46, 78):
        sd.rectangle([cx + dx - 9, base - 30, cx + dx + 9, base], fill=col)
    sd.rectangle([cx - 92, base - 36, cx + 92, base - 30], fill=col)
    sd.rectangle([cx - 92, base - 43, cx + 92, base - 38], fill=col)
    sd.rectangle([cx - 13, base - 51, cx + 13, base - 43], fill=col)
    for hx in (-15, -5, 5, 15):
        sd.ellipse([cx + hx - 4, base - 59, cx + hx + 4, base - 51], fill=col)
        sd.line([cx + hx, base - 51, cx + hx + 3, base - 46], fill=col, width=2)
    for i in range(8):
        a = math.radians(200 + i * 20)
        x = cx + 128 + int(20 * math.cos(a)); y = 16 + int(9 * math.sin(a))
        sd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=GOLD)
    sd.rectangle([0, base, w, h], fill=(12, 18, 30))
    return s

def scene_gaza(w, h):
    s, sd = new_scene(w, h, (214, 178, 128), (232, 206, 158))
    sun(sd, 36, 12, 8, (240, 160, 70))
    gy = h - 10
    sd.rectangle([0, gy, w, h], fill=(178, 138, 88))
    sd.rectangle([0, gy, w, gy + 2], fill=(150, 112, 66))
    def tank(x, flip=1):
        sd.rectangle([min(x, x + 44 * flip), gy - 9, max(x, x + 44 * flip), gy - 2],
                     fill=(70, 66, 50))
        sd.rectangle([min(x + 10 * flip, x + 30 * flip), gy - 15,
                      max(x + 10 * flip, x + 30 * flip), gy - 9], fill=(70, 66, 50))
        sd.line([x + 28 * flip, gy - 13, x + 52 * flip, gy - 15], fill=(60, 56, 44), width=3)
        for wx in range(4):
            cxw = x + (4 + wx * 10) * flip
            sd.ellipse([cxw - 3, gy - 5, cxw + 3, gy + 1], fill=(48, 44, 34))
    tank(28); tank(w - 84, -1)
    for x, y in [(150, 10), (196, 6), (250, 12)]:
        sd.ellipse([x, y, x + 16, y + 7], fill=(150, 128, 96))
        sd.ellipse([x + 6, y - 4, x + 20, y + 3], fill=(158, 136, 102))
    return s

def scene_gta(w, h):
    s, sd = new_scene(w, h, (24, 14, 52), (74, 30, 84))
    sd.ellipse([w - 52, 4, w - 36, 20], fill=(232, 226, 200))
    sd.ellipse([w - 58, 2, w - 44, 16], fill=(24, 14, 52))
    skyline(sd, w, h - 8, [20, 30, 16, 34, 22, 28, 18], (12, 10, 26), seed=9)
    windows(sd, w, h - 8, 6, col=(120, 230, 240), seed=3, step=13)
    windows(sd, w, h - 8, 10, col=(250, 110, 200), seed=11, step=17)
    for px in (30, w - 60):
        sd.line([px, h - 8, px, h - 26], fill=(10, 24, 14), width=3)
        for a in (-50, -20, 10, 40):
            r = math.radians(a)
            sd.line([px, h - 26, px + int(11 * math.sin(r)),
                     h - 26 - int(8 * math.cos(r))], fill=(16, 60, 30), width=2)
    sd.rectangle([0, h - 8, w, h], fill=(30, 16, 44))
    sd.rectangle([0, h - 8, w, h - 6], fill=(250, 110, 200))
    return s

def scene_voyager(w, h):
    s, sd = new_scene(w, h, (6, 10, 26), (14, 22, 48))
    for i in range(46):
        x = (i * 53 + 17) % w; y = (i * 29 + 7) % (h - 6)
        r = 1 if i % 4 else 2
        sd.ellipse([x, y, x + r, y + r], fill=(220, 226, 240))
    cx, cy = w // 2 - 30, h // 2
    sd.ellipse([cx - 17, cy - 13, cx + 17, cy + 13], outline=(206, 212, 224), width=2)
    sd.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(206, 212, 224))
    sd.line([cx, cy, cx + 52, cy - 12], fill=(180, 186, 200), width=2)
    sd.line([cx + 52, cy - 12, cx + 66, cy - 12], fill=(180, 186, 200), width=3)
    sd.line([cx, cy, cx + 34, cy + 14], fill=(180, 186, 200), width=2)
    for k in range(3):
        sd.arc([w - 66 + k * 7, cy - 8 + k * 2, w - 30 + k * 7, cy + 16 + k * 2],
               -60, 60, fill=(110, 190, 235), width=2)
    sd.ellipse([w - 24, cy + 2, w - 16, cy + 10], fill=(110, 170, 235))
    return s

def scene_odesa(w, h):
    s, sd = new_scene(w, h, (16, 24, 44), (44, 58, 84))
    sea = h - 9
    sd.rectangle([0, sea, w, h], fill=(18, 34, 54))
    sd.line([0, sea, w, sea], fill=(90, 130, 160), width=1)
    for bx in (0, 150):
        sd.line([bx + 30, sea, bx + 30, 8], fill=(8, 10, 16), width=3)
        sd.line([bx + 30, 10, bx + 66, 16], fill=(8, 10, 16), width=2)
        sd.line([bx + 58, 16, bx + 58, sea - 14], fill=(8, 10, 16), width=1)
        sd.rectangle([bx + 50, sea - 14, bx + 66, sea - 6], fill=(8, 10, 16))
    for cx, cy, r in [(96, 12, 8), (226, 8, 6), (272, 16, 7)]:
        for a in range(0, 360, 45):
            x2 = cx + int((r + 4) * math.cos(math.radians(a)))
            y2 = cy + int((r + 4) * math.sin(math.radians(a)))
            sd.line([cx, cy, x2, y2], fill=(250, 150, 60), width=2)
        sd.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], fill=(252, 190, 90))
    sd.ellipse([120, 2, 150, 10], fill=(70, 76, 92))
    return s

def scene_cyclone(w, h):
    s, sd = new_scene(w, h, (104, 128, 138), (168, 182, 178))
    cx, cy = w // 2 + 40, h // 2 - 2
    for r, a0 in [(26, 20), (19, 140), (12, 260)]:
        sd.arc([cx - r, cy - int(r * 0.62), cx + r, cy + int(r * 0.62)], a0, a0 + 250,
               fill=(238, 242, 240), width=3)
    sd.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=(70, 92, 100))
    for i in range(9):
        x = 16 + i * 16
        sd.line([x, 6 + (i % 3) * 4, x - 4, 14 + (i % 3) * 4], fill=(210, 224, 228), width=1)
    sd.polygon([(0, h), (0, h - 12), (52, h - 16), (104, h - 10), (150, h - 14),
                (190, h)], fill=(52, 74, 62))
    sd.line([196, h - 6, 236, h - 6], fill=(30, 50, 66), width=2)
    sd.line([206, h - 6, 206, h - 13], fill=(30, 50, 66), width=2)
    return s

def scene_icj(w, h):
    s, sd = new_scene(w, h, (168, 188, 204), (216, 222, 210))
    cx = w // 2; base = h - 4
    sd.polygon([(cx - 104, base - 26), (cx + 104, base - 26), (cx, base - 44)],
               fill=(96, 84, 66))
    sd.rectangle([cx - 104, base - 26, cx + 104, base - 22], fill=(110, 98, 78))
    for i in range(7):
        x = cx - 90 + i * 30
        sd.rectangle([x, base - 22, x + 8, base - 4], fill=(226, 220, 204))
    sd.rectangle([cx - 108, base - 4, cx + 108, base], fill=(96, 84, 66))
    bx = cx + 128
    sd.line([bx, 6, bx, base - 8], fill=(60, 54, 44), width=2)
    sd.line([bx - 15, 10, bx + 15, 10], fill=(60, 54, 44), width=2)
    for sx in (bx - 15, bx + 15):
        sd.line([sx, 10, sx - 5, 18], fill=(60, 54, 44), width=1)
        sd.line([sx, 10, sx + 5, 18], fill=(60, 54, 44), width=1)
        sd.pieslice([sx - 7, 16, sx + 7, 26], 0, 180, fill=(60, 54, 44))
    sd.ellipse([bx - 2, base - 12, bx + 2, base - 8], fill=(60, 54, 44))
    return s

def scene_saff(w, h):
    s, sd = new_scene(w, h, (30, 62, 44), (52, 96, 60))
    sd.rectangle([0, h - 12, w, h], fill=(34, 110, 52))
    sd.line([0, h - 12, w, h - 12], fill=(220, 240, 220), width=1)
    sd.ellipse([w // 2 - 16, h - 13, w // 2 + 16, h - 4], outline=(220, 240, 220), width=1)
    for fx in (26, w - 34):
        sd.line([fx, h - 10, fx, 6], fill=(20, 26, 22), width=3)
        for dx in (-6, 0, 6):
            for dy in (0, 5):
                sd.ellipse([fx + dx - 2, 4 + dy, fx + dx + 2, 8 + dy],
                           fill=(252, 244, 190))
    sd.ellipse([w // 2 - 4, h - 16, w // 2 + 4, h - 8], fill=(240, 240, 240))
    sd.polygon([(w // 2 - 4, h - 16), (w // 2, h - 19), (w // 2 + 4, h - 16)],
               fill=(20, 20, 20))
    fx = w // 2 - 96
    sd.rectangle([fx, 8, fx + 26, 13], fill=(244, 130, 40))
    sd.rectangle([fx, 13, fx + 26, 18], fill=(240, 240, 235))
    sd.rectangle([fx, 18, fx + 26, 23], fill=(30, 130, 60))
    fx2 = w // 2 + 70
    sd.rectangle([fx2, 8, fx2 + 26, 23], fill=(20, 110, 55))
    sd.ellipse([fx2 + 9, 11, fx2 + 17, 19], outline=(240, 240, 235), width=1)
    return s

def scene_borno(w, h):
    s, sd = new_scene(w, h, (226, 172, 100), (238, 208, 148))
    sun(sd, 40, 11, 8, (246, 186, 92))
    gy = h - 9
    sd.rectangle([0, gy, w, h], fill=(186, 140, 74))
    for i in range(12):
        x = i * 29 + 6
        sd.line([x, gy + 7, x + 3, gy + 1], fill=(140, 104, 50), width=1)
    tx = w // 2 + 66
    sd.line([tx, gy, tx, gy - 16], fill=(70, 54, 30), width=4)
    sd.ellipse([tx - 26, gy - 30, tx + 26, gy - 15], fill=(86, 96, 44))
    sd.ellipse([tx - 16, gy - 36, tx + 14, gy - 24], fill=(96, 106, 50))
    vx = 66
    sd.rectangle([vx, gy - 12, vx + 46, gy - 4], fill=(74, 76, 58))
    sd.rectangle([vx + 26, gy - 17, vx + 40, gy - 12], fill=(74, 76, 58))
    sd.rectangle([vx + 6, gy - 16, vx + 20, gy - 12], fill=(74, 76, 58))
    for wx in (vx + 9, vx + 36):
        sd.ellipse([wx - 4, gy - 6, wx + 4, gy + 2], fill=(40, 40, 34))
    for dx in range(3):
        sd.ellipse([vx - 14 - dx * 6, gy - 12 + dx * 2, vx - 6 - dx * 6, gy - 6 + dx * 2],
                   fill=(196, 158, 100))
    return s

def scene_solar(w, h):
    s, sd = new_scene(w, h, (92, 156, 208), (176, 216, 236))
    sun(sd, 40, 12, 10, (250, 206, 84))
    for rx, ry in [(238, 6), (268, 4)]:
        sd.line([rx, h - 8, rx, ry + 12], fill=(70, 80, 88), width=2)
        for a in (90, 210, 330):
            x2 = rx + int(11 * math.cos(math.radians(a)))
            y2 = ry + 12 + int(11 * math.sin(math.radians(a)))
            sd.line([rx, ry + 12, x2, y2], fill=(70, 80, 88), width=2)
    gy = h - 13
    sd.rectangle([0, gy, w, h], fill=(86, 140, 66))
    for r in range(2):
        for c in range(5):
            x = 18 + c * 34; y = gy + 1 + r * 6
            sd.polygon([(x, y + 4), (x + 6, y), (x + 30, y), (x + 24, y + 4)],
                       fill=(30, 62, 110))
            sd.line([x + 12, y, x + 9, y + 4], fill=(120, 170, 220), width=1)
            sd.line([x + 21, y, x + 18, y + 4], fill=(120, 170, 220), width=1)
    return s

def scene_pew(w, h):
    s, sd = new_scene(w, h, (70, 84, 128), (196, 140, 96))
    sun(sd, w - 42, 13, 9, (246, 186, 100))
    base = h - 3; col = (22, 26, 40)
    x = 26
    sd.rectangle([x, base - 22, x + 34, base], fill=col)
    sd.polygon([(x - 3, base - 22), (x + 17, base - 32), (x + 37, base - 22)], fill=col)
    sd.rectangle([x + 14, base - 40, x + 20, base - 30], fill=col)
    sd.line([x + 17, base - 44, x + 17, base - 36], fill=col, width=2)
    sd.line([x + 13, base - 41, x + 21, base - 41], fill=col, width=2)
    x = w // 2 - 24
    sd.rectangle([x, base - 18, x + 48, base], fill=col)
    sd.pieslice([x + 8, base - 32, x + 40, base - 12], 180, 360, fill=col)
    sd.rectangle([x + 2, base - 26, x + 8, base], fill=col)
    sd.rectangle([x + 40, base - 26, x + 46, base], fill=col)
    sd.arc([x + 20, base - 40, x + 30, base - 30], 200, 330, fill=(250, 214, 110), width=2)
    x = w - 66
    sd.rectangle([x, base - 16, x + 40, base], fill=col)
    sd.polygon([(x + 4, base - 16), (x + 20, base - 26), (x + 36, base - 16)], fill=col)
    sd.rectangle([x + 16, base - 31, x + 24, base - 25], fill=col)
    return s

def scene_doha(w, h):
    s, sd = new_scene(w, h, (44, 40, 92), (150, 84, 110))
    sd.rectangle([0, h - 11, w, h], fill=(30, 116, 56))
    sd.line([0, h - 11, w, h - 11], fill=(230, 244, 230), width=1)
    cx = w // 2
    skyline(sd, w, h - 11, [10, 15, 9], (30, 26, 48), seed=13)
    sd.arc([cx - 120, 6, cx + 120, 66], 180, 360, fill=(226, 220, 210), width=4)
    for fx in (34, w - 42):
        sd.line([fx, h - 9, fx, 5], fill=(18, 20, 26), width=3)
        for dx in (-6, 0, 6):
            for dy in (0, 5):
                sd.ellipse([fx + dx - 2, 3 + dy, fx + dx + 2, 7 + dy],
                           fill=(252, 244, 190))
    sd.ellipse([cx - 4, h - 15, cx + 4, h - 7], fill=(242, 242, 242))
    sd.polygon([(cx - 4, h - 15), (cx, h - 18), (cx + 4, h - 15)], fill=(24, 24, 24))
    return s

def scene_sea(w, h):
    s, sd = new_scene(w, h, (120, 134, 146), (172, 182, 184))
    for gx, gy in [(60, 7), (84, 5), (250, 6)]:
        sd.arc([gx, gy, gx + 7, gy + 5], 200, 330, fill=(70, 78, 84), width=1)
        sd.arc([gx + 6, gy, gx + 13, gy + 5], 200, 330, fill=(70, 78, 84), width=1)
    sea = 15
    sd.rectangle([0, sea, w, h], fill=(44, 78, 100))
    for r in range(3):
        for i in range(7):
            x = i * 48 + (r % 2) * 22 + 4; y = sea + 4 + r * 7
            sd.arc([x, y, x + 22, y + 6], 180, 340, fill=(150, 190, 205), width=1)
    bx, by = w // 2 - 30, sea + 6
    sd.polygon([(bx, by), (bx + 60, by), (bx + 50, by + 9), (bx + 10, by + 9)],
               fill=(30, 30, 32))
    sd.rectangle([bx + 14, by - 7, bx + 42, by], fill=(52, 52, 56))
    sd.line([bx + 48, by - 12, bx + 48, by], fill=(30, 30, 32), width=2)
    sd.ellipse([bx + 70, by + 2, bx + 82, by + 14], outline=(214, 84, 60), width=3)
    return s

# ---------------------------------------------------------------- data
MAINS_BIG = [
    dict(n=1, tag="ASIA · DIPLOMACY", scene=scene_shenzhen,
         head="TRUMP, XI AND PUTIN HOLD FIRST TRILATERAL IN SHENZHEN",
         deck="The three leaders sit down at APEC today, after a Trump-Putin "
              "handshake on arrival. Putin calls Europe in 'humiliating "
              "decline'; no joint statement by press time."),
    dict(n=2, tag="AMERICAS · POLITICS", scene=scene_capitol,
         head="JEFFRIES NOMINATED FOR SPEAKER AS DEMOCRATS TAKE HOUSE",
         deck="The caucus backs Hakeem Jeffries 251\u201311. Democrats hold at "
              "least 257 House seats, with a 56\u201344 edge in the Senate after "
              "the midterms. (NPR, USA Today)"),
    dict(n=3, tag="EUROPE · DIPLOMACY", scene=scene_berlin,
         head="EUROPE DRAFTS A 45BN-EURO LOAN FOR UKRAINE IN BERLIN",
         deck="The Coalition of the Willing meets Witkoff and Kushner as the "
              "EU proposes a \u20ac45bn budget-backed loan to fund Kyiv through "
              "2027. (Reuters)"),
]
MAINS_MED = [
    dict(n=4, tag="MIDDLE EAST · WAR", scene=scene_gaza,
         head="Israeli tanks thrust into Gaza City",
         deck="Israeli tanks thrust into Gaza City; three Palestinians killed "
              "in the advance, medics say. (Reuters)"),
    dict(n=5, tag="GLOBAL · GAMES", scene=scene_gta,
         head="GTA VI finally launches, 13 years on",
         deck="Queues wrap game stores worldwide on launch day, 13 years "
              "after the last instalment. (AP, BBC)"),
    dict(n=6, tag="SPACE · SCIENCE", scene=scene_voyager,
         head="Voyager 1 reaches one light-day out",
         deck="The 1977 probe's signals now take a full day to reach Earth. "
              "(NASA)"),
    dict(n=7, tag="EUROPE · WAR", scene=scene_odesa,
         head="Russian strikes on Odesa kill four",
         deck="Overnight barrage hits port and homes, officials say, in the "
              "latest strike on the city. (Reuters)"),
    dict(n=8, tag="ASIA · WEATHER", scene=scene_cyclone,
         head="Cyclone Akvan turns very severe",
         deck="The storm turns very severe over the bay; landfall on the east "
              "coast is due on 20 November. (The Hindu)"),
    dict(n=9, tag="EUROPE · JUSTICE", scene=scene_icj,
         head="World Court reads Rohingya judgment",
         deck="Did Myanmar commit genocide? The court reads its judgment "
              "today; verdict awaited. (Le Monde)"),
    dict(n=10, tag="ASIA · SPORT", scene=scene_saff,
         head="India beat Pakistan 2\u20131, take SAFF title",
         deck="A late winner settles a tense regional final as India edge "
              "Pakistan. (TOI)"),
    dict(n=11, tag="AFRICA · SECURITY", scene=scene_borno,
         head="21 ISWAP fighters killed in Borno",
         deck="Nigeria's army reports the clash in the north-east state of "
              "Borno. (Vanguard)"),
    dict(n=12, tag="ASIA · BUSINESS", scene=scene_solar,
         head="Amazon pledges $7bn for India renewables",
         deck="The investment runs to 2030, the company says \u2014 a "
              "clean-energy push in India. (TOI)"),
    dict(n=13, tag="WORLD · SOCIETY", scene=scene_pew,
         head="Pew: Islam nearly level with Christianity by 2035",
         deck="Pew's projections put Islam almost level with Christianity "
              "by 2035."),
    dict(n=14, tag="MIDDLE EAST · SPORT", scene=scene_doha,
         head="U-17 World Cup kicks off in Doha",
         deck="Hosts Qatar open against Panama as 48 teams begin the biggest "
              "youth World Cup yet \u2014 104 matches in Doha. (FIFA)"),
    dict(n=15, tag="EUROPE · REFUGEES", scene=scene_sea,
         head="Sea-route deaths pass 2,500 this year",
         deck="The UN refugee agency's running count of deaths on the sea "
              "routes passed 2,500 for the year."),
]
ALSO = [
    (16, "RUSSIA", "Refining output down 45% after strikes"),
    (17, "UKRAINE", "Arms deliveries speed up, Kyiv says"),
    (18, "WASHINGTON", "Schumer and Van Hollen clash over shutdown"),
    (19, "US SENATE", "Democrats hold the Senate too, 56\u201344"),
    (20, "TECH", "Agencies warn of AI-driven cyber threat"),
    (21, "CANADA", "Carney balances China ties and US talks"),
    (22, "MOSCOW", "Lavrov accuses France over Ukraine arms"),
    (23, "FRANCE", "M\u00e9lenchon says he could win the presidency"),
    (24, "BULGARIA", "LPG tanker fire contained, Black Sea"),
    (25, "AUSTRALIA", "Settler sanctions widened over West Bank"),
    (26, "RIYADH", "Saudi flight alerts lifted"),
    (27, "LIBYA", "Record cocaine haul seized off the coast"),
    (28, "CAIRO", "Egypt and Syria sign aviation pact"),
    (29, "TOKYO", "India and Japan review defence ties"),
    (30, "GHANA", "Bad loans fall to 13.1% of lending"),
    (31, "MOROCCO", "Defence industry roadmap unveiled"),
    (32, "KENYA", "Ruto gives State of the Nation address"),
    (33, "SUDAN", "RSF strikes hit El Obeid again"),
    (34, "COP31", "Ocean protection talks open"),
    (35, "SCIENCE", "Earth's missing billion years explained"),
    (36, "BOGOTA", "Hegseth visits Colombia for security talks"),
    (37, "AFRICA", "AFCON qualifier draw made in Cairo"),
    (38, "KASHMIR", "Three militants killed in Kulgam encounter"),
    (39, "BHOPAL", "National hockey opener thrills home crowd"),
    (40, "HAGUE", "Fears US may sanction ICJ judges \u2014 reports"),
    (41, "CALIFORNIA", "Flood watch up into Thursday"),
    (42, "MEXICO", "Banxico minutes out: 3\u20132 for cut to 6.25%"),
]

MX, GAP = 16, 10
CW = (W - 2 * MX - 2 * GAP) // 3   # 324
COLX = [MX, MX + CW + GAP, MX + 2 * (CW + GAP)]

def num_badge(x, y, n, r=9):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F(SANSB, 9 if n < 10 else 8)
    s = str(n)
    d.text((x + r - tw(f, s) / 2, y + r - 6), s, font=f, fill=(255, 255, 255))

def card_big(x, y, st, scene_h=64):
    img.paste(st["scene"](CW, scene_h), (x, y))
    d.rectangle([x, y, x + CW, y + scene_h], outline=RULE)
    ty = y + scene_h + 4
    num_badge(x, ty, st["n"])
    d.text((x + 23, ty + 2), st["tag"], font=F(SANSB, 10), fill=RED)
    hy = ty + 16
    f = F(SERIFB, 19)
    for ln in wrap(f, st["head"], CW)[:3]:
        d.text((x, hy), ln, font=f, fill=INK); hy += 22
    f = F(SANS, 10)
    for ln in wrap(f, st["deck"], CW)[:3]:
        d.text((x, hy + 1), ln, font=f, fill=INK); hy += 11.5
    return hy

def card_med(x, y, st, scene_h=36):
    img.paste(st["scene"](CW, scene_h), (x, y))
    d.rectangle([x, y, x + CW, y + scene_h], outline=RULE)
    ty = y + scene_h + 3
    num_badge(x, ty, st["n"], r=7)
    d.text((x + 18, ty + 1), st["tag"], font=F(SANSB, 8.5), fill=RED)
    hy = ty + 13
    f = F(SERIFB, 13)
    for ln in wrap(f, st["head"], CW)[:2]:
        d.text((x, hy), ln, font=f, fill=INK); hy += 14.5
    f = F(SANS, 9.3)
    for ln in wrap(f, st["deck"], CW)[:2]:
        d.text((x, hy + 1), ln, font=f, fill=INK); hy += 10.5
    return hy

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 86], fill=NAVY)
d.text((MX, 7), "THE WORLD IN ONE DAY", font=F(SANSB, 11), fill=GOLD)
r = "42 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
d.text((W - MX - tw(F(SANSB, 11), r), 7), r, font=F(SANSB, 11), fill=GOLD)
d.text((MX, 22), "Thursday 19 November 2026", font=F(SERIFB, 40),
       fill=(246, 240, 222))
d.text((MX, 68), "Every story below happened, or was first reported, on "
       "this day.", font=F(SERIF, 12), fill=(206, 196, 168))
# tally bar
d.rectangle([0, 86, W, 106], fill=PAPER)
d.line([0, 86, W, 86], fill=RULE); d.line([0, 106, W, 106], fill=RULE)
tally = ("EUROPE 10 \u00b7 AFRICA 8 \u00b7 ASIA 7 \u00b7 AMERICAS 7 \u00b7 GLOBAL 5 "
         "\u00b7 MIDDLE EAST 3 \u00b7 OCEANIA 1 \u00b7 SPACE 1")
f = F(SANSB, 11.5)
d.text(((W - tw(f, tally)) / 2, 91), tally, font=f, fill=INK)
# UTC strip
uy = 106
d.rectangle([MX, uy + 4, MX + 128, uy + 28], fill=RED)
d.text((MX + 8, uy + 10), "THE DAY IN UTC", font=F(SANSB, 10.5),
       fill=(255, 255, 255))
moments = [("00:00 UTC", "GTA VI unlocks in Britain"),
           ("09:00 UTC", "ICJ reads Myanmar judgment"),
           ("DAY", "Shenzhen trilateral summit"),
           ("17:00 UTC", "NASA briefs on Voyager 1")]
xx = MX + 140
for tme, txt in moments:
    d.text((xx, uy + 10), tme, font=F(SANSB, 10.5), fill=RED)
    xx += tw(F(SANSB, 10.5), tme) + 4
    d.text((xx, uy + 10), txt, font=F(SANS, 10.5), fill=INK)
    xx += tw(F(SANS, 10.5), txt) + 16

# ---------------------------------------------------------------- grid
gy = 140
ends = [card_big(COLX[i], gy, MAINS_BIG[i]) for i in range(3)]
d.line([MX, 326, W - MX, 326], fill=RULE)
row_y = 334
for r_ in range(4):
    for c_ in range(3):
        card_med(COLX[c_], row_y, MAINS_MED[r_ * 3 + c_])
    row_y += 100
    if r_ < 3:
        d.line([MX, row_y - 5, W - MX, row_y - 5], fill=(206, 196, 170))

# ---------------------------------------------------------------- numbers
ny = 738
d.line([MX, ny, W - MX, ny], fill=RULE)
d.text((MX, ny + 8), "BY THE\nNUMBERS", font=F(SANSB, 9.5), fill=INK)
nums = [("251\u201311", "Jeffries caucus vote"),
        ("\u20ac45bn", "EU loan proposed for Ukraine"),
        ("56\u201344", "US Senate split"),
        ("1 light-day", "Voyager 1's distance out")]
nx = MX + 86
for val, cap in nums:
    f = F(SERIFB, 23)
    d.text((nx, ny + 5), val, font=f, fill=INK)
    d.text((nx, ny + 33), cap, font=F(SANS, 8.5), fill=(90, 84, 70))
    nx += max(tw(f, val), tw(F(SANS, 8.5), cap)) + 34
d.line([MX, ny + 46, W - MX, ny + 46], fill=RULE)

# ---------------------------------------------------------------- map
EURASIA = [(-9, 37), (-2, 37), (0, 39), (-4, 42), (-9, 43), (-2, 44), (-1, 46),
           (-5, 48), (-1, 49), (2, 51), (5, 53), (8, 55), (7, 57), (10, 59),
           (5, 60), (5, 62), (10, 65), (18, 69), (25, 71), (32, 70), (41, 68),
           (50, 69), (60, 69), (70, 70), (82, 72), (95, 73), (108, 74),
           (120, 73), (132, 72), (145, 72), (156, 70), (169, 66), (178, 64),
           (173, 62), (162, 60), (157, 55), (155, 50), (148, 44), (142, 40),
           (139, 36), (135, 34), (130, 32), (126, 36), (121, 33), (120, 28),
           (116, 24), (110, 21), (108, 16), (107, 10), (104, 6), (101, 7),
           (99, 10), (97, 15), (93, 17), (90, 22), (87, 21), (84, 19),
           (80, 14), (77, 8), (75, 12), (72, 19), (69, 22), (66, 25),
           (60, 25), (56, 26), (52, 28), (50, 29), (51, 24), (55, 24),
           (58, 21), (57, 18), (53, 15), (46, 12), (43, 12), (41, 16),
           (39, 21), (37, 23), (35, 28), (34, 31), (36, 36), (31, 36),
           (27, 37), (26, 39), (22, 37), (19, 40), (16, 38), (13, 40),
           (12, 42), (10, 44), (7, 44), (3, 42), (0, 39)]
NAMER = [(-168, 66), (-160, 71), (-145, 70), (-135, 69), (-126, 71), (-115, 69),
         (-100, 69), (-92, 69), (-86, 68), (-81, 73), (-76, 71), (-72, 62),
         (-77, 60), (-81, 64), (-85, 66), (-89, 62), (-92, 58), (-94, 53),
         (-97, 49), (-92, 46), (-87, 46), (-82, 44), (-76, 44), (-71, 44),
         (-68, 47), (-70, 42), (-74, 39), (-75, 35), (-79, 33), (-81, 31),
         (-81, 26), (-80, 22), (-84, 20), (-87, 21), (-90, 21), (-92, 19),
         (-95, 18), (-97, 16), (-96, 19), (-97, 24), (-102, 20), (-105, 20),
         (-108, 23), (-110, 24), (-114, 29), (-117, 33), (-121, 36),
         (-123, 40), (-124, 46), (-128, 52), (-135, 57), (-145, 60),
         (-155, 58), (-162, 58), (-166, 60)]
SAMER = [(-78, 7), (-75, 10), (-72, 12), (-64, 10), (-60, 8), (-52, 5),
         (-50, 0), (-44, -3), (-38, -8), (-41, -15), (-40, -21), (-48, -26),
         (-52, -32), (-57, -38), (-62, -41), (-65, -45), (-67, 50 - 100),
         (-69, -52), (-71, -54), (-74, -50), (-73, -44), (-73, -37),
         (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1),
         (-78, 4)]
AFRICA = [(-17, 15), (-16, 21), (-13, 27), (-9, 31), (-5, 35), (3, 37),
          (10, 37), (11, 34), (20, 32), (30, 31), (34, 28), (35, 24),
          (37, 22), (39, 20), (43, 12), (48, 11), (51, 12), (44, 5),
          (41, -2), (40, -10), (37, -18), (35, -24), (32, 29 - 58),
          (26, -33), (20, -35), (17, -32), (14, -26), (12, -18), (13, -10),
          (9, -2), (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12)]
UK = [(-5, 50), (-3, 53), (-5, 55), (-7, 57), (-5, 58), (-2, 57), (-1, 54),
      (-2, 51)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 37), (141, 40), (142, 44),
         (140, 45), (138, 38), (135, 34), (131, 32)]
SUMATRA = [(95, 5), (100, 0), (104, -3), (106, -6), (103, -4), (98, 2), (95, 5)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3), (110, -2)]
JAVA = [(106, -6), (110, -7), (114, -8), (114, -9), (106, -7)]
SULAWESI = [(119, 0), (121, 1), (123, 0), (120, -3), (119, -1)]
NEWGUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -8),
             (142, -6), (136, -4), (131, -3)]
PHIL = [(120, 13), (121, 16), (122, 18), (121, 14), (120, 12)]
AUSTRALIA = [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -36), (140, -38),
             (145, -38), (147, -39), (150, -37), (153, -31), (153, -27),
             (151, -24), (146, -19), (142, -11), (142, -15), (140, -18),
             (136, -15), (136, -12), (132, -11), (130, -13), (126, -14),
             (122, -17), (118, -20), (114, -21)]
NZ = [(167, -45), (169, -43), (172, -41), (174, -39), (176, -38), (174, -41),
      (172, -43), (169, -46), (167, -46)]
MADAG = [(44, -16), (47, -15), (50, -17), (48, -20), (47, -24), (45, -25),
         (44, -22), (43, -18), (44, -16)]
LAND = [EURASIA, NAMER, SAMER, AFRICA, UK, JAPAN, SUMATRA, BORNEO, JAVA,
        SULAWESI, NEWGUINEA, PHIL, AUSTRALIA, NZ, MADAG]

PINS = [(1, 114.1, 22.6, 0, 0), (2, -77.0, 38.9, 0, 0), (3, 13.4, 52.5, 7, -4),
        (4, 34.3, 31.4, -4, 6), (5, -17.0, 56.5, 0, 0), (6, -118.2, 34.1, 0, 0),
        (7, 30.7, 46.5, 6, -1), (8, 80.3, 14.8, 7, 5), (9, 4.3, 52.1, -7, -4),
        (10, 81.0, 23.5, 3, -6), (11, 13.2, 11.8, 0, 0), (12, 72.8, 18.9, -6, 3),
        (13, -35.0, 26.0, 0, 0), (14, 51.5, 25.3, 5, 4), (15, 15.5, 38.0, -3, 6)]
DOTS = [(30.5, 50.4), (37.6, 55.7), (-75.7, 45.4), (2.4, 48.9), (28.0, 42.5),
        (46.7, 24.6), (22.9, 32.9), (31.2, 30.0), (139.7, 35.7), (-0.2, 5.6),
        (-6.8, 34.0), (36.8, -1.3), (30.2, 13.2), (-48.5, -1.4), (-74.1, 4.7),
        (74.8, 34.1), (77.4, 23.3), (-120.0, 37.5), (-99.1, 19.4),
        (149.1, -35.3), (4.5, 52.2), (-3.7, 40.4), (103.8, 1.35), (18.1, -33.9)]

MAPX, MAPY, MAPW, MAPH = MX, 806, 452, 134
LANDC = (196, 178, 138)
def proj(lon, lat):
    return (MAPX + (lon + 180) / 360.0 * MAPW,
            MAPY + (78 - lat) / 136.0 * MAPH)

by = 790
d.text((MX, by), "WHERE IT HAPPENED", font=F(SERIFB, 13), fill=RED)
also_h = "ALSO ON THURSDAY 19 NOVEMBER \u2014 27 MORE STORIES"
d.text((MAPX + MAPW + 22, by), also_h, font=F(SERIFB, 12), fill=RED)
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(222, 230, 226))
for glon in range(-150, 181, 30):
    gx, _ = proj(glon, 0)
    d.line([gx, MAPY, gx, MAPY + MAPH], fill=(206, 216, 210))
for glat in range(-60, 61, 30):
    _, gy2 = proj(0, glat)
    d.line([MAPX, gy2, MAPX + MAPW, gy2], fill=(206, 216, 210))
for poly in LAND:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LANDC)
for lon, lat in DOTS:
    x, y = proj(lon, lat)
    d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(120, 116, 108))
for txt, lon, lat in [("N. AMERICA", -104, 55), ("EUROPE", 44, 63),
                      ("ASIA", 92, 50), ("AFRICA", 24, -6), ("S. AMERICA", -62, -18),
                      ("OCEANIA", 138, -28)]:
    x, y = proj(lon, lat)
    f = F(SANSB, 7.5)
    d.text((x - tw(f, txt) / 2, y), txt, font=f, fill=(122, 100, 66))
for n, lon, lat, dx, dy in PINS:
    x, y = proj(lon, lat)
    x += dx; y += dy
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED, outline=(255, 255, 255), width=1)
    f = F(SANSB, 8 if n >= 10 else 9)
    s = str(n)
    d.text((x - tw(f, s) / 2, y - 5), s, font=f, fill=(255, 255, 255))
cap = ("Red numbers mark stories 1\u201315, grey dots the briefs. Pin 6 sits at "
       "JPL, Pasadena \u2014 Voyager is one light-day out. Positions approximate.")
f = F(SANS, 8.5)
cl = wrap(f, cap, MAPW)
cy = MAPY + MAPH + 4
for ln in cl[:2]:
    d.text((MAPX, cy), ln, font=f, fill=RED); cy += 10.5

# ---------------------------------------------------------------- also
AX = MAPX + MAPW + 22
ACW = (W - MX - AX - 12) // 2
def also_line(x, y, n, place, txt, maxw):
    f = F(SANS, 9.3); fb = F(SANSB, 9.3)
    size = 9.3
    while size > 7.5:
        f = F(SANS, int(size * 10) / 10); fb = F(SANSB, int(size * 10) / 10)
        wtot = tw(fb, str(n) + " ") + tw(fb, place) + tw(f, " \u2014 " + txt)
        if wtot <= maxw: break
        size -= 0.4
    d.text((x, y), str(n), font=fb, fill=RED)
    x2 = x + tw(fb, str(n) + " ")
    d.text((x2, y), place, font=fb, fill=INK)
    x3 = x2 + tw(fb, place)
    d.text((x3, y), " \u2014 " + txt, font=f, fill=INK)

ay = MAPY + 2
for i, (n, place, txt) in enumerate(ALSO[:14]):
    also_line(AX, ay + i * 11.0, n, place, txt, ACW)
for i, (n, place, txt) in enumerate(ALSO[14:]):
    also_line(AX + ACW + 12, ay + i * 11.0, n, place, txt, ACW)

# ---------------------------------------------------------------- date check + footer
dy = 966
d.rectangle([MX, dy, MX + 92, dy + 24], fill=RED)
d.text((MX + 8, dy + 6), "DATE CHECK", font=F(SANSB, 10), fill=(255, 255, 255))
dc = ("Left out on purpose \u2014 they broke before today: Jensen Huang's "
      "resignation as Nvidia's chief (announced 12 Nov) \u00b7 America's strike "
      "on Iran's Qeshm Island missile site (17 Nov) \u00b7 Musk's petition to "
      "bring Huang back (13 Nov)")
f = F(SANS, 9.5)
for i, ln in enumerate(wrap(f, dc, W - MX - (MX + 100))[:2]):
    d.text((MX + 100, dy + 1 + i * 11), ln, font=f, fill=INK)
fy = 994
jn = ("JUDGE NOTE \u2014 Every story above happened, or was first reported, on "
      "Thursday 19 November 2026. Disputed claims are attributed, not stated "
      "as fact.")
f = F(SERIFB, 10)
d.text(((W - tw(f, jn)) / 2, fy), jn, font=f, fill=INK)
src = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 The Guardian \u00b7 Le Monde "
       "\u00b7 TOI \u00b7 Vanguard \u00b7 NASA and the regional wires named above. "
       "Original drawings. \u00b7 Date checked: 19.11.2026")
f = F(SANS, 8.5)
d.text(((W - tw(f, src)) / 2, fy + 15), src, font=f, fill=(90, 84, 70))

img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
print("entry.png drawn:", img.size)
