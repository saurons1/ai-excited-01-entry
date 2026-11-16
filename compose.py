#!/usr/bin/env python3
"""Compose the ai-excited-01 v1 entry image (1024x1024) with PIL only.

Concept: "A colossal koi leaping out of a tiny goldfish bowl" — one giant
white-and-orange koi arcs diagonally out of a small round fishbowl on a
windowsill, water exploding toward the viewer, golden-hour sun, deep teal
background. Flat vector-style illustration: bold shapes, clean edges, no
photorealism, no text. Deterministic: fixed seed, no timestamps.

Run:  python3 compose.py   -> writes entry.png beside this file.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
OUT = "entry.png"

ORANGE = (255, 122, 26)
ORANGE_D = (232, 84, 8)
ORANGE_L = (255, 176, 92)
WHITE = (255, 250, 240)
CREAM = (255, 226, 170)
TEAL_D = (4, 42, 51)
AQUA = (64, 199, 214)
AQUA_L = (150, 230, 238)
FOAM = (235, 251, 252)
GOLD = (255, 201, 77)
GOLD_L = (255, 226, 150)
SUN = (255, 214, 110)
WOOD = (146, 94, 48)
WOOD_D = (110, 66, 30)
WOOD_L = (190, 132, 74)
INK = (6, 38, 46)

rng = random.Random(20261116)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bezier(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
    return (x, y)


def tangent(p0, p1, p2, t):
    x = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    y = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    return (x, y)


def ellipse(draw, cx, cy, rx, ry, fill=None, outline=None, width=1):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                 fill=fill, outline=outline, width=width)


def petal(draw, tip, base, w, fill):
    """A tapered droplet/petal from base point to tip point."""
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    mid = ((tip[0] + base[0]) / 2 + nx * w * 0.55,
           (tip[1] + base[1]) / 2 + ny * w * 0.55)
    mid2 = ((tip[0] + base[0]) / 2 - nx * w * 0.55,
            (tip[1] + base[1]) / 2 - ny * w * 0.55)
    draw.polygon([base, mid, tip, mid2], fill=fill)


def rot_ellipse(base_img, cx, cy, rx, ry, angle_deg, fill):
    """Paste a rotated ellipse onto base_img (RGB), returns new image."""
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill + (255,))
    tmp = tmp.rotate(angle_deg, center=(cx, cy), resample=Image.BICUBIC)
    return Image.alpha_composite(base_img.convert("RGBA"), tmp).convert("RGB")


img = Image.new("RGB", (W, H), TEAL_D)
d = ImageDraw.Draw(img)

# ---- 1. deep teal vertical gradient -------------------------------------
for y in range(H):
    t = y / H
    col = lerp((6, 52, 64), (12, 98, 110), t ** 1.15)
    d.line([(0, y), (W, y)], fill=col)

# ---- 2. golden-hour glow behind the leap (transparent layer, no black) ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, col, al in ((430, (255, 190, 80), 60), (330, (255, 200, 100), 90),
                   (230, (255, 210, 120), 120)):
    ellipse(gd, 640, 330, r, r, fill=col + (al,))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img)

# ---- 3. sun disc + rays (top right) --------------------------------------
ellipse(d, 830, 140, 96, 96, fill=SUN)
ellipse(d, 830, 140, 78, 78, fill=GOLD_L)
for ang in range(0, 360, 18):
    a = math.radians(ang)
    x0, y0 = 830 + math.cos(a) * 108, 140 + math.sin(a) * 108
    x1, y1 = 830 + math.cos(a) * 150, 140 + math.sin(a) * 150
    d.line([(x0, y0), (x1, y1)], fill=GOLD, width=10)
ellipse(d, 830, 140, 62, 62, fill=(255, 232, 160))

# faint diagonal light beams
beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
for x0, wdt, al in ((120, 90, 26), (300, 60, 20), (560, 110, 24)):
    bd.polygon([(x0, 0), (x0 + wdt, 0), (x0 + wdt + 260, H), (x0 + 260, H)],
               fill=(255, 220, 130, al))
beam = beam.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB")
d = ImageDraw.Draw(img)

# ---- 4. windowsill + wall + window frame ---------------------------------
d.rectangle([0, 838, W, H], fill=(7, 58, 68))
d.rectangle([0, 838, W, 872], fill=WOOD)
d.rectangle([0, 838, W, 846], fill=WOOD_L)
d.rectangle([0, 868, W, 872], fill=WOOD_D)
d.rectangle([0, 0, 46, 838], fill=(10, 66, 76))
d.rectangle([978, 0, W, 838], fill=(10, 66, 76))
d.rectangle([46, 0, 56, 838], fill=GOLD)
d.rectangle([968, 0, 978, 838], fill=GOLD)

# ---- 5. splash crown bursting out of the bowl (behind the koi) -----------
BX, BY, BR = 400, 768, 106  # bowl centre / radius
for ang, ln, wdt in ((-160, 130, 30), (-135, 170, 36), (-110, 190, 40),
                     (-80, 185, 38), (-55, 165, 34), (-30, 130, 28)):
    a = math.radians(ang)
    tip = (BX + math.cos(a) * ln, BY - 30 + math.sin(a) * ln * 0.9)
    petal(d, tip, (BX + math.cos(a) * 50, BY - 40 + math.sin(a) * 42),
          wdt, AQUA_L if ang % 2 else FOAM)

# ---- 6. the koi — tapered body along a leaping bezier --------------------
P0, P1, P2 = (400, 790), (330, 300), (760, 235)  # tail -> head
N = 90
pts = [bezier(P0, P1, P2, i / N) for i in range(N + 1)]


def radius(t):
    # tail thin -> fat mid-body -> slightly narrower head
    return 32 + 88 * math.sin(math.pi * min(1.0, 0.12 + 0.88 * t)) ** 0.9


# tail fin first (behind the body): two flowing lobes, rotated ellipses
img = rot_ellipse(img, 312, 836, 112, 40, -30, ORANGE)
img = rot_ellipse(img, 346, 856, 90, 28, -12, WHITE)
img = rot_ellipse(img, 264, 812, 90, 32, -52, ORANGE_L)
d = ImageDraw.Draw(img)
d.line([(400, 790), (312, 836)], fill=ORANGE_D, width=4)
d.line([(400, 790), (346, 856)], fill=ORANGE_D, width=4)
d.line([(400, 790), (264, 812)], fill=ORANGE_D, width=4)

# body silhouette mask
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
for i, (x, y) in enumerate(pts):
    r = radius(i / N)
    ellipse(md, x, y, r, r * 0.94, fill=255)
# head blob at the end, angled along the tangent
hx, hy = pts[-1]
tx, ty = tangent(P0, P1, P2, 1.0)
tl = math.hypot(tx, ty)
ux, uy = tx / tl, ty / tl
head_c = (hx + ux * 58, hy + uy * 58)
for k in range(5):
    ellipse(md, head_c[0] - ux * k * 14, head_c[1] - uy * k * 14,
            94 - k * 6, 86 - k * 5, fill=255)

# koi skin: white base + FEW orange patches (kohaku), clipped by the mask
skin = Image.new("RGB", (W, H), WHITE)
# soft cream shading on the belly side (transparent layer — no black bleed)
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(shade)
for i, (x, y) in enumerate(pts):
    t = i / N
    r = radius(t)
    ellipse(shd, x + 30, y + 34, r * 0.8, r * 0.78, fill=CREAM + (110,))
shade = shade.filter(ImageFilter.GaussianBlur(12))
skin = Image.alpha_composite(skin.convert("RGBA"), shade).convert("RGB")
# three orange patches on the back + orange cap on the head
for t, rx, ry, rot in ((0.38, 88, 56, -28), (0.60, 96, 62, -16),
                       (0.78, 78, 52, -4)):
    x, y = pts[int(t * N)]
    img2 = rot_ellipse(skin, x, y - 16, rx, ry, rot, ORANGE)
    skin = img2
skin = rot_ellipse(skin, head_c[0] - 6, head_c[1] - 34, 72, 46, 18, ORANGE)

img.paste(skin, (0, 0), mask)
d = ImageDraw.Draw(img)

# outline + golden rim light along the TRUE upper edge.
# travel direction is up-right; upper side normal is (ty, -tx).
upper = []
for i in range(N + 1):
    t = i / N
    x, y = pts[i]
    tx2, ty2 = tangent(P0, P1, P2, t)
    l2 = math.hypot(tx2, ty2) or 1
    nx, ny = ty2 / l2, -tx2 / l2
    r = radius(t)
    upper.append((x + nx * r * 0.94, y + ny * r * 0.94))
d.line(upper, fill=INK, width=7, joint="curve")
inner = []
for i in range(N + 1):
    t = i / N
    x, y = pts[i]
    tx2, ty2 = tangent(P0, P1, P2, t)
    l2 = math.hypot(tx2, ty2) or 1
    nx, ny = ty2 / l2, -tx2 / l2
    r = radius(t)
    inner.append((x + nx * r * 0.78, y + ny * r * 0.78))
d.line(inner, fill=GOLD_L, width=8, joint="curve")

# ---- 7. dorsal fins along the mid-back + pectoral fin --------------------
for t, ln, ang in ((0.45, 80, -38), (0.62, 88, -26)):
    x, y = pts[int(t * N)]
    tx2, ty2 = tangent(P0, P1, P2, t)
    l2 = math.hypot(tx2, ty2) or 1
    nx, ny = ty2 / l2, -tx2 / l2
    r = radius(t)
    img = rot_ellipse(img, x + nx * (r + ln * 0.12), y + ny * (r + ln * 0.12),
                      62, 26, ang, ORANGE)
    d = ImageDraw.Draw(img)
px, py = pts[int(0.86 * N)]
img = rot_ellipse(img, px + 8, py + 88, 62, 26, 24, ORANGE_L)
d = ImageDraw.Draw(img)
d.line([(px, py + 40), (px + 8, py + 88)], fill=ORANGE_D, width=4)

# ---- 8. head details: eye, mouth, gill, barbels -------------------------
ex, ey = head_c[0] + 30, head_c[1] - 12
ellipse(d, ex, ey, 28, 28, fill=WHITE, outline=INK, width=5)
ellipse(d, ex + 6, ey + 2, 14, 14, fill=INK)
ellipse(d, ex + 11, ey - 4, 5, 5, fill=WHITE)
# open joyful mouth at the front tip
mx, my = head_c[0] + ux * 78, head_c[1] + uy * 78
ellipse(d, mx, my, 20, 13, fill=(200, 60, 60), outline=INK, width=5)
# gill curve
d.arc([head_c[0] - 52, head_c[1] - 46, head_c[0] + 22, head_c[1] + 62],
      start=300, end=90, fill=ORANGE_D, width=6)
# short barbels streaming back from the mouth
for dy0, ln2 in ((18, 62), (34, 76)):
    d.line([(mx - 8, my + dy0 - 10),
            (mx - 8 - ln2, my + dy0 + 22)],
           fill=INK, width=5)

# ---- 9. fishbowl in FRONT (glass over the tail base — bowl stays visible) -
d.pieslice([BX - BR, BY - BR, BX + BR, BY + BR], 0, 180, fill=(24, 140, 158))
for cx, cy, rx, ry, col in ((352, 836, 24, 13, (120, 120, 120)),
                            (400, 846, 28, 14, (90, 90, 96)),
                            (448, 836, 22, 12, (140, 140, 140))):
    ellipse(d, cx, cy, rx, ry, fill=col)
d.line([(388, 836), (378, 778), (370, 748)], fill=(30, 160, 90), width=6)
d.line([(400, 840), (402, 776), (410, 740)], fill=(46, 190, 110), width=6)
d.line([(412, 836), (424, 780), (436, 752)], fill=(30, 160, 90), width=6)
d.ellipse([BX - BR, BY - BR, BX + BR, BY + BR], outline=AQUA_L, width=7)
d.arc([BX - BR + 14, BY - BR + 18, BX + BR - 60, BY + BR - 40],
      start=200, end=330, fill=(255, 255, 255), width=12)
d.arc([BX - BR + 8, BY - BR + 8, BX + BR - 8, BY + BR - 8],
      start=195, end=345, fill=AQUA, width=6)
ellipse(d, BX, 876, 140, 15, fill=(0, 0, 0))
# foam ring at the bowl rim where the koi bursts out
d.arc([BX - BR - 6, BY - BR - 6, BX + BR + 6, BY + BR + 6],
      start=180, end=360, fill=FOAM, width=10)

# ---- 10. water trailing the koi + droplets toward the viewer -------------
drop_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(drop_layer)
for i in range(0, N, 4):
    t = i / N
    x, y = pts[i]
    tx2, ty2 = tangent(P0, P1, P2, t)
    l2 = math.hypot(tx2, ty2) or 1
    nx, ny = -ty2 / l2, tx2 / l2  # underside
    r = radius(t)
    bx, by = x + nx * (r + 10), y + ny * (r + 10)
    rr = rng.randint(6, 13)
    ellipse(dd, bx + rng.randint(-5, 5), by + rng.randint(-5, 5),
            rr, rr, fill=AQUA_L + (230,))
drops = []
for _ in range(58):
    ang = rng.uniform(-170, -5)
    dist = rng.uniform(150, 500)
    cx = BX + math.cos(math.radians(ang)) * dist
    cy = BY - 40 + math.sin(math.radians(ang)) * dist * 0.85
    if 60 < cx < 964 and 40 < cy < 830:
        drops.append((cx, cy, rng.uniform(3, 14)))
for _ in range(6):  # a few big foreground drops, bottom corners
    side = rng.choice((-1, 1))
    cx = 512 + side * rng.uniform(320, 460)
    cy = rng.uniform(720, 980)
    drops.append((cx, cy, rng.uniform(16, 22)))
for cx, cy, r in drops:
    col = (FOAM if r > 15 else AQUA_L if r > 8 else AQUA) + (235,)
    ellipse(dd, cx, cy, r, r * 1.12, fill=col)
    if r > 10:
        ellipse(dd, cx - r * 0.3, cy - r * 0.35, r * 0.26, r * 0.26,
                fill=(255, 255, 255, 235))
img = Image.alpha_composite(img.convert("RGBA"), drop_layer).convert("RGB")
d = ImageDraw.Draw(img)
# speed lines radiating from the bowl
for ang, ln, wdt in ((-150, 220, 6), (-125, 270, 7), (-100, 250, 6),
                     (-70, 280, 7), (-45, 240, 6)):
    a = math.radians(ang)
    x0, y0 = BX + math.cos(a) * 150, BY - 30 + math.sin(a) * 140
    x1, y1 = BX + math.cos(a) * (150 + ln), BY - 30 + math.sin(a) * (140 + ln * 0.85)
    d.line([(x0, y0), (x1, y1)], fill=FOAM, width=wdt)

# ---- 11. sparkles + vignette ----------------------------------------------
for _ in range(34):
    cx, cy = rng.uniform(70, 954), rng.uniform(60, 800)
    s = rng.uniform(5, 12)
    col = GOLD_L if rng.random() < 0.5 else FOAM
    d.line([(cx - s, cy), (cx + s, cy)], fill=col, width=3)
    d.line([(cx, cy - s), (cx, cy + s)], fill=col, width=3)
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-180, -180, W + 180, H + 180], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(120))
black = Image.new("RGB", (W, H), (2, 20, 26))
img = Image.composite(img, black, vig)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
