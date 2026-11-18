#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Programmatic drawing only (Pillow): no photos, no fetched assets, no
external files. Deterministic: one fixed random seed, so every run writes
identical bytes. Layout: masthead, tall main panel (Gulf escalation) on
the left, three stacked panels (APEC Shenzhen / Kerch Bridge / Cyclone
Akvan) on the right, and a ticker strip of smaller stories at the bottom.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "entry.png")

DEJAVU = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(DEJAVU, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(DEJAVU, "DejaVuSans-Bold.ttf")
SANS = os.path.join(DEJAVU, "DejaVuSans.ttf")

rng = random.Random(20261118)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(text, fnt, max_w):
    """Split text into lines that fit max_w (greedy word wrap)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / span
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def stars(draw, box, n, color=(255, 255, 220)):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rng.randint(x0 + 4, x1 - 4)
        y = rng.randint(y0 + 4, y1 - 4)
        r = rng.choice([1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


def skyline(draw, x0, x1, base, heights, color, lit=(255, 214, 120)):
    """Blocky city silhouette with a few lit windows."""
    x = x0
    i = 0
    while x < x1:
        w = heights[i % len(heights)][0]
        h = heights[i % len(heights)][1]
        draw.rectangle([x, base - h, min(x + w, x1), base], fill=color)
        for _ in range(max(1, w // 14)):
            wx = rng.randint(x + 3, min(x + w - 4, x1 - 4))
            wy = rng.randint(base - h + 4, base - 6)
            if rng.random() < 0.5:
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=lit)
        x += w + rng.randint(2, 6)
        i += 1


def burst(draw, cx, cy, r, core=(255, 240, 180), mid=(255, 150, 40), edge=(255, 90, 20)):
    """Starburst explosion: spiky polygon + glowing core."""
    pts = []
    for k in range(24):
        ang = k * math.pi / 12
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=edge)
    pts2 = []
    for k in range(16):
        ang = k * math.pi / 8
        rr = r * 0.62 if k % 2 == 0 else r * 0.3
        pts2.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts2, fill=mid)
    draw.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28], fill=core)


def drone(draw, cx, cy, s, body=(30, 30, 34), light=(255, 60, 60)):
    """Small quadcopter silhouette with one red light."""
    draw.ellipse([cx - s, cy - s * 0.45, cx + s, cy + s * 0.45], fill=body)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ex, ey = cx + dx * s * 1.7, cy + dy * s * 0.7
        draw.line([(cx, cy), (ex, ey)], fill=body, width=max(2, s // 3))
        draw.line([(ex - s * 0.9, ey), (ex + s * 0.9, ey)], fill=body, width=max(2, s // 4))
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=light)


def jet(draw, cx, cy, s, color=(200, 205, 215)):
    """Fighter jet silhouette flying right, slight climb."""
    pts = [
        (cx - 3 * s, cy),
        (cx - 1.2 * s, cy - 0.35 * s),
        (cx + 2.2 * s, cy - 0.25 * s),
        (cx + 3.4 * s, cy),
        (cx + 2.2 * s, cy + 0.25 * s),
        (cx - 1.2 * s, cy + 0.35 * s),
    ]
    draw.polygon(pts, fill=color)
    draw.polygon([(cx - 0.4 * s, cy - 0.3 * s), (cx + 0.6 * s, cy - 1.5 * s),
                  (cx + 1.1 * s, cy - 0.25 * s)], fill=color)
    draw.polygon([(cx - 1.6 * s, cy + 0.2 * s), (cx - 0.9 * s, cy + 1.3 * s),
                  (cx - 0.4 * s, cy + 0.25 * s)], fill=color)
    draw.polygon([(cx + 3.4 * s, cy - 0.12 * s), (cx + 4.6 * s, cy),
                  (cx + 3.4 * s, cy + 0.12 * s)], fill=(255, 170, 60))


def smoke(draw, x, y, puffs, base_r, color=(120, 120, 125)):
    for i in range(puffs):
        px = x + rng.randint(-26, 26) - i * 4
        py = y - i * 14
        r = base_r + i * 5
        draw.ellipse([px - r, py - r, px + r, py + r], fill=color)


def headline_bar(draw, x0, x1, y_bottom, head, sub, head_size=34, sub_size=19):
    """Dark caption band rising from a panel's bottom; wraps text to fit.

    The head wraps to at most 2 lines, the sub to at most 2 lines; the band
    height grows to hold them, so nothing is ever cut off at the edge.
    """
    inner = x1 - x0 - 28
    head_lines = wrap_text(head, font(SANS_B, head_size), inner)[:2]
    sub_lines = wrap_text(sub, font(SANS, sub_size), inner)[:2]
    height = 12 + len(head_lines) * (head_size + 2) + 6 + len(sub_lines) * (sub_size + 4) + 10
    y0 = y_bottom - height
    draw.rectangle([x0, y0, x1, y_bottom], fill=(12, 12, 16))
    y = y0 + 10
    for line in head_lines:
        draw.text((x0 + 14, y), line, font=font(SANS_B, head_size), fill=(255, 255, 255))
        y += head_size + 2
    y += 4
    for line in sub_lines:
        draw.text((x0 + 14, y), line, font=font(SANS, sub_size), fill=(220, 220, 220))
        y += sub_size + 4
    return y0


def panel_frame(draw, box):
    draw.rectangle(box, outline=(20, 20, 20), width=3)


def draw_gulf(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (8, 14, 42), (58, 40, 84))
    stars(draw, (x0, y0, x1, y0 + 260), 60)
    # distant island (Qeshm) with strike plume
    draw.polygon([(x0 + 380, y1 - 150), (x0 + 470, y1 - 190), (x0 + 560, y1 - 150),
                  (x0 + 640, y1 - 150), (x0 + 640, y1), (x0 + 380, y1)], fill=(16, 20, 30))
    smoke(draw, x0 + 500, y1 - 210, 5, 16, color=(90, 80, 90))
    burst(draw, x0 + 500, y1 - 185, 46)
    # sea
    draw.rectangle([x0, y1 - 150, x1, y1], fill=(10, 26, 52))
    for _ in range(26):
        wx = rng.randint(x0 + 6, x1 - 40)
        wy = rng.randint(y1 - 140, y1 - 12)
        draw.line([(wx, wy), (wx + rng.randint(14, 34), wy)], fill=(70, 110, 160), width=2)
    # Bahrain skyline on the near shore
    skyline(draw, x0 + 10, x0 + 360, y1 - 150, [(26, 90), (34, 130), (22, 70), (40, 150), (28, 100)], (8, 12, 24))
    # drones + intercept bursts in the sky
    drone(draw, x0 + 130, y0 + 130, 11)
    drone(draw, x0 + 250, y0 + 90, 9)
    drone(draw, x0 + 330, y0 + 200, 8)
    burst(draw, x0 + 180, y0 + 210, 34)
    burst(draw, x0 + 300, y0 + 150, 26)
    jet(draw, x0 + 470, y0 + 110, 13)
    headline_bar(draw, x0, x1, y1, "GULF ON EDGE",
                 "Iran drones target US radar in Bahrain — US jets hit Qeshm Island",
                 head_size=40, sub_size=20)


def draw_apec(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (122, 18, 22), (60, 10, 16))
    # Shenzhen towers
    skyline(draw, x0 + 6, x1 - 6, y1 - 96, [(20, 60), (26, 96), (18, 48), (30, 110), (22, 72)], (30, 6, 10), lit=(255, 200, 90))
    # three flags on poles
    poles = [(x0 + 52, (206, 20, 20)), (x0 + 108, (40, 70, 170)), (x0 + 164, (210, 210, 210))]
    for px, col in poles:
        draw.line([(px, y1 - 96), (px, y1 - 150)], fill=(240, 230, 200), width=3)
        draw.rectangle([px, y1 - 150, px + 42, y1 - 128], fill=col, outline=(240, 230, 200))
    # leaders at a table (three silhouettes)
    draw.rectangle([x0 + 200, y1 - 96, x1 - 14, y1 - 78], fill=(40, 8, 10))
    for lx in (x0 + 226, x0 + 258, x0 + 290):
        draw.ellipse([lx - 9, y1 - 132, lx + 9, y1 - 114], fill=(15, 5, 6))
        draw.polygon([(lx - 13, y1 - 114), (lx + 13, y1 - 114), (lx + 17, y1 - 96), (lx - 17, y1 - 96)], fill=(15, 5, 6))
    headline_bar(draw, x0, x1, y1, "APEC OPENS IN SHENZHEN",
                 "Xi, Trump, Putin to meet Thursday", head_size=23, sub_size=16)


def draw_kerch(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (96, 118, 148), (52, 70, 96))
    # sea
    draw.rectangle([x0, y1 - 90, x1, y1], fill=(30, 52, 78))
    for _ in range(14):
        wx = rng.randint(x0 + 6, x1 - 30)
        wy = rng.randint(y1 - 84, y1 - 12)
        draw.line([(wx, wy), (wx + rng.randint(12, 28), wy)], fill=(90, 130, 170), width=2)
    # bridge deck with a broken, tilted span
    deck_y = y0 + 92
    draw.rectangle([x0, deck_y, x0 + 130, deck_y + 10], fill=(40, 42, 48))
    draw.rectangle([x0 + 190, deck_y, x1, deck_y + 10], fill=(40, 42, 48))
    for px in (x0 + 34, x0 + 96, x0 + 240, x0 + 292):
        draw.rectangle([px, deck_y - 52, px + 8, deck_y], fill=(40, 42, 48))
        draw.line([(px + 4, deck_y - 52), (px - 26, deck_y)], fill=(90, 92, 98), width=2)
        draw.line([(px + 4, deck_y - 52), (px + 34, deck_y)], fill=(90, 92, 98), width=2)
    # tilted fallen span + fire + smoke at the gap
    draw.polygon([(x0 + 130, deck_y), (x0 + 190, deck_y), (x0 + 178, deck_y + 46), (x0 + 142, deck_y + 40)], fill=(52, 50, 46))
    burst(draw, x0 + 160, deck_y + 26, 26)
    smoke(draw, x0 + 160, deck_y - 6, 4, 13)
    headline_bar(draw, x0, x1, y1, "KERCH BRIDGE HIT AGAIN",
                 "Second day of strikes on the Crimea link", head_size=23, sub_size=16)


def draw_cyclone(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (16, 48, 66), (8, 26, 44))
    # coastline at the bottom
    draw.polygon([(x0, y1 - 46), (x0 + 90, y1 - 70), (x0 + 190, y1 - 52), (x0 + 320, y1 - 66),
                  (x1, y1 - 46), (x1, y1), (x0, y1)], fill=(14, 40, 30))
    # spiral storm
    cx, cy = x0 + 160, y0 + 78
    pts = []
    for k in range(220):
        t = k / 220.0
        ang = t * math.pi * 5.2
        r = 8 + t * 62
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.82))
    draw.line(pts, fill=(235, 245, 250), width=7)
    draw.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=(20, 30, 40))
    # rain streaks
    for _ in range(40):
        rx = rng.randint(x0 + 8, x1 - 8)
        ry = rng.randint(y0 + 8, y1 - 90)
        draw.line([(rx, ry), (rx - 4, ry + 12)], fill=(150, 190, 215), width=2)
    headline_bar(draw, x0, x1, y1, "CYCLONE AKVAN",
                 "Bears down on India's east coast", head_size=23, sub_size=16)


def main():
    img = Image.new("RGB", (W, H), (247, 243, 232))
    d = ImageDraw.Draw(img)
    # masthead: title left, date right — sizes shrink until both fit
    title = "THE WORLD"
    date = "WEDNESDAY 18 NOVEMBER 2026"
    t_size, d_size = 62, 26
    while (font(SERIF_B, t_size).getlength(title) + 40
           + font(SANS_B, d_size).getlength(date) > W - 48) and t_size > 40:
        t_size -= 2
        d_size -= 1
    d.text((24, 30), title, font=font(SERIF_B, t_size), fill=(12, 12, 12))
    dw = font(SANS_B, d_size).getlength(date)
    d.text((W - 24 - dw, 30 + (t_size - d_size) // 2), date,
           font=font(SANS_B, d_size), fill=(150, 20, 20))
    d.line([(24, 128), (W - 24, 128)], fill=(12, 12, 12), width=4)
    d.text((24, 134), "SUMMING UP THE DAY'S WORLD NEWS", font=font(SANS_B, 15), fill=(90, 90, 90))
    # main panel: Gulf
    gulf = (24, 160, 664, 850)
    draw_gulf(d, gulf)
    panel_frame(d, gulf)
    # right column panels
    apec = (680, 160, 1000, 380)
    draw_apec(d, apec)
    panel_frame(d, apec)
    kerch = (680, 396, 1000, 626)
    draw_kerch(d, kerch)
    panel_frame(d, kerch)
    cyc = (680, 642, 1000, 850)
    draw_cyclone(d, cyc)
    panel_frame(d, cyc)
    # ticker strip: smaller stories
    d.rectangle([24, 866, 1000, 1000], fill=(232, 226, 208), outline=(20, 20, 20), width=3)
    d.text((40, 880), "ALSO TODAY", font=font(SANS_B, 20), fill=(150, 20, 20))
    items = [
        ("UK sanctions Israeli\nsettlement firms", (40, 912)),
        ("Dhoni retires from\nthe IPL", (380, 912)),
        ("Nvidia posts $115.8bn\nquarter", (700, 912)),
    ]
    for text, (tx, ty) in items:
        d.text((tx, ty), text, font=font(SANS_B, 21), fill=(20, 20, 20))
    d.text((40, 972), "Sources: Reuters · Al Jazeera · AFP · CNA", font=font(SANS, 14), fill=(90, 90, 90))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
