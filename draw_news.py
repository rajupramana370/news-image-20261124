#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world
news of Tuesday, 24 November 2026. Deterministic: no timestamps, no random
numbers, fixed fonts, fixed layout. Output: entry.png, 1024x1024."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (27, 58, 95)
GOLD = (184, 134, 11)
GREY = (96, 96, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rule(draw, y, x0=36, x1=988, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def headline_block(draw, x, y, max_w, kicker, head_lines, standfirst,
                   head_size=30, stand_size=19):
    """Kicker + headline lines + standfirst. Returns y below the block."""
    kf = font(SANS_B, 15)
    draw.text((x, y), kicker, font=kf, fill=RED)
    y += 22
    hf = font(SERIF_B, head_size)
    for line in head_lines:
        draw.text((x, y), line, font=hf, fill=INK)
        y += head_size + 4
    y += 2
    sf = font(SANS, stand_size)
    for line in wrap(draw, standfirst, sf, max_w):
        draw.text((x, y), line, font=sf, fill=(40, 40, 40))
        y += stand_size + 6
    return y


# ---------------- pictograms (simple geometric drawings) ----------------

def flame(d, cx, cy, s, outer=(255, 120, 0), inner=(255, 200, 60)):
    """One stylised flame centred at (cx, cy), height ~s."""
    d.polygon([(cx - s * 0.30, cy + s * 0.48), (cx, cy - s * 0.42),
               (cx + s * 0.30, cy + s * 0.48), (cx + s * 0.12, cy + s * 0.62),
               (cx - s * 0.12, cy + s * 0.62)], fill=outer)
    d.polygon([(cx - s * 0.15, cy + s * 0.42), (cx, cy + s * 0.06),
               (cx + s * 0.15, cy + s * 0.42)], fill=inner)


def pic_factory_fire(d, x, y, s):
    """Candy factory ablaze, smoke above, flame on the roof."""
    d.rectangle([x + s * 0.06, y + s * 0.52, x + s * 0.94, y + s * 0.94],
                fill=(120, 120, 120))
    d.polygon([(x + s * 0.06, y + s * 0.52), (x + s * 0.24, y + s * 0.40),
               (x + s * 0.42, y + s * 0.52), (x + s * 0.60, y + s * 0.40),
               (x + s * 0.78, y + s * 0.52), (x + s * 0.94, y + s * 0.40),
               (x + s * 0.94, y + s * 0.52)], fill=(90, 90, 90))
    d.rectangle([x + s * 0.78, y + s * 0.22, x + s * 0.88, y + s * 0.44],
                fill=(90, 90, 90))
    for i in range(4):
        wx = x + s * (0.14 + i * 0.20)
        d.rectangle([wx, y + s * 0.64, wx + s * 0.12, y + s * 0.78],
                    fill=(255, 220, 120))
    flame(d, x + s * 0.30, y + s * 0.30, s * 0.52)
    flame(d, x + s * 0.52, y + s * 0.26, s * 0.62)
    flame(d, x + s * 0.70, y + s * 0.34, s * 0.38)
    for (gx, gy, gr) in [(0.30, 0.06, 0.10), (0.48, 0.02, 0.13),
                         (0.66, 0.05, 0.09)]:
        d.ellipse([x + s * (gx - gr), y + s * (gy - gr * 0.6),
                   x + s * (gx + gr), y + s * (gy + gr * 0.6)],
                  fill=(170, 170, 170))
    d.line([(x + s * 0.02, y + s * 0.96), (x + s * 0.98, y + s * 0.96)],
           fill=GREY, width=4)


def pic_building_hit(d, x, y, s):
    """Apartment block with a jagged crack and smoke."""
    d.rectangle([x + s * 0.18, y + s * 0.14, x + s * 0.82, y + s * 0.92],
                fill=(120, 120, 120))
    for r in range(3):
        for c in range(3):
            wx = x + s * (0.26 + c * 0.19)
            wy = y + s * (0.24 + r * 0.20)
            d.rectangle([wx, wy, wx + s * 0.11, wy + s * 0.12],
                        fill=(255, 220, 120))
    crack = [(x + s * 0.55, y + s * 0.14), (x + s * 0.47, y + s * 0.34),
             (x + s * 0.60, y + s * 0.50), (x + s * 0.48, y + s * 0.70),
             (x + s * 0.56, y + s * 0.92)]
    d.line(crack, fill=RED, width=6, joint="curve")
    for (gx, gy, gr) in [(0.30, 0.02, 0.09), (0.44, -0.02, 0.12),
                         (0.60, 0.0, 0.08)]:
        d.ellipse([x + s * (gx - gr), y + s * (gy - gr * 0.6),
                   x + s * (gx + gr), y + s * (gy + gr * 0.6)],
                  fill=(170, 170, 170))
    d.line([(x + s * 0.05, y + s * 0.94), (x + s * 0.95, y + s * 0.94)],
           fill=GREY, width=4)


def pic_ship_fire(d, x, y, s):
    """Cargo ship on fire at sea, flames amidships, waves below."""
    d.polygon([(x + s * 0.08, y + s * 0.62), (x + s * 0.92, y + s * 0.62),
               (x + s * 0.82, y + s * 0.78), (x + s * 0.20, y + s * 0.78)],
              fill=NAVY)
    d.rectangle([x + s * 0.16, y + s * 0.48, x + s * 0.34, y + s * 0.62],
                fill=NAVY)
    d.rectangle([x + s * 0.66, y + s * 0.44, x + s * 0.80, y + s * 0.62],
                fill=NAVY)
    d.rectangle([x + s * 0.70, y + s * 0.34, x + s * 0.76, y + s * 0.44],
                fill=NAVY)
    for i in range(3):
        bx = x + s * (0.38 + i * 0.09)
        d.rectangle([bx, y + s * 0.52, bx + s * 0.06, y + s * 0.62],
                    fill=GOLD)
    flame(d, x + s * 0.50, y + s * 0.38, s * 0.55)
    for (gx, gy, gr) in [(0.42, 0.10, 0.08), (0.58, 0.06, 0.10)]:
        d.ellipse([x + s * (gx - gr), y + s * (gy - gr * 0.6),
                   x + s * (gx + gr), y + s * (gy + gr * 0.6)],
                  fill=(170, 170, 170))
    for r in range(2):
        yy = y + s * (0.86 + r * 0.08)
        pts = []
        for i in range(21):
            pts.append((x + s * i / 20,
                        yy + s * 0.02 * math.sin(i * 1.4 + r)))
        d.line(pts, fill=NAVY, width=4, joint="curve")


def pic_chart_up(d, x, y, s):
    """Stock chart surging up and to the right, chip above the line."""
    d.line([(x + s * 0.08, y + s * 0.10), (x + s * 0.08, y + s * 0.90)],
           fill=INK, width=4)
    d.line([(x + s * 0.08, y + s * 0.90), (x + s * 0.96, y + s * 0.90)],
           fill=INK, width=4)
    pts = [(0.12, 0.78), (0.30, 0.70), (0.44, 0.74), (0.58, 0.52),
           (0.72, 0.40), (0.86, 0.20)]
    line = [(x + s * a, y + s * b) for a, b in pts]
    d.line(line, fill=RED, width=7, joint="curve")
    ax, ay = x + s * 0.86, y + s * 0.20
    d.polygon([(ax, ay), (ax - s * 0.13, ay + s * 0.01),
               (ax - s * 0.02, ay + s * 0.12)], fill=RED)
    # chip / processor above the surge
    d.rectangle([x + s * 0.16, y + s * 0.06, x + s * 0.44, y + s * 0.34],
                outline=NAVY, width=5)
    d.rectangle([x + s * 0.23, y + s * 0.13, x + s * 0.37, y + s * 0.27],
                fill=NAVY)
    for i in range(3):
        px = x + s * (0.20 + i * 0.10)
        d.line([(px, y + s * 0.06), (px, y + s * 0.0)], fill=NAVY, width=4)
        d.line([(px, y + s * 0.34), (px, y + s * 0.40)], fill=NAVY, width=4)
    tf = font(SANS_B, 20)
    d.text((x + s * 0.30, y + s * 0.46), "+31%", font=tf, fill=RED)


def pic_train(d, x, y, s):
    """Front of a passenger train on rails, flags of two neighbours."""
    d.rectangle([x + s * 0.24, y + s * 0.16, x + s * 0.76, y + s * 0.80],
                fill=NAVY)
    d.rectangle([x + s * 0.32, y + s * 0.26, x + s * 0.68, y + s * 0.46],
                fill=(200, 225, 245))
    d.line([(x + s * 0.50, y + s * 0.26), (x + s * 0.50, y + s * 0.46)],
           fill=NAVY, width=4)
    for i in range(2):
        cx = x + s * (0.38 + i * 0.20)
        d.ellipse([cx - s * 0.045, cy := y + s * 0.60, cx + s * 0.045,
                   y + s * 0.69], fill=(255, 220, 120))
    d.rectangle([x + s * 0.24, y + s * 0.72, x + s * 0.76, y + s * 0.80],
                fill=GOLD)
    # rails converging
    d.line([(x + s * 0.34, y + s * 0.80), (x + s * 0.16, y + s * 0.98)],
           fill=INK, width=5)
    d.line([(x + s * 0.66, y + s * 0.80), (x + s * 0.84, y + s * 0.98)],
           fill=INK, width=5)
    for i, ry in enumerate([0.86, 0.92, 0.97]):
        half = 0.20 + i * 0.045
        d.line([(x + s * (0.50 - half), y + s * ry),
                (x + s * (0.50 + half), y + s * ry)], fill=GREY, width=4)
    # two small flags on the roof line
    d.line([(x + s * 0.30, y + s * 0.16), (x + s * 0.30, y + s * 0.02)],
           fill=INK, width=3)
    d.polygon([(x + s * 0.30, y + s * 0.02), (x + s * 0.42, y + s * 0.06),
               (x + s * 0.30, y + s * 0.10)], fill=(255, 140, 0))
    d.line([(x + s * 0.70, y + s * 0.16), (x + s * 0.70, y + s * 0.02)],
           fill=INK, width=3)
    d.polygon([(x + s * 0.70, y + s * 0.02), (x + s * 0.58, y + s * 0.06),
               (x + s * 0.70, y + s * 0.10)], fill=RED)


def pic_chequer(d, x, y, s):
    """Chequered flag waving on a pole: race day."""
    d.line([(x + s * 0.16, y + s * 0.06), (x + s * 0.16, y + s * 0.96)],
           fill=INK, width=6)
    fx, fy = x + s * 0.16, y + s * 0.08
    fw, fh = s * 0.74, s * 0.52
    rows, cols = 4, 6
    cw, ch = fw / cols, fh / rows
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                d.rectangle([fx + c * cw, fy + r * ch,
                             fx + (c + 1) * cw, fy + (r + 1) * ch],
                            fill=INK)
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=3)
    d.line([(x + s * 0.05, y + s * 0.96), (x + s * 0.95, y + s * 0.96)],
           fill=GREY, width=4)


# ---------------- page layout ----------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # Masthead
    draw_centered(d, 26, "THE WORLD IN ONE DAY", font(SERIF_B, 62))
    rule(d, 108, width=3)
    draw_centered(d, 118, "TUESDAY, 24 NOVEMBER 2026",
                  font(SANS_B, 26), fill=RED)
    rule(d, 156, width=2)

    # ---- Lead story: Indonesia factory fire ----
    pic_factory_fire(d, 806, 182, 160)
    headline_block(
        d, 36, 178, 750,
        "INDONESIA  \u2022  TOP STORY",
        ["Factory fire kills 24 in",
         "Indonesia, dozens missing"],
        "A blaze sweeps a candy factory in Banten province; "
        "rescuers search the ruins for around 30 workers still "
        "missing as the death toll reaches at least 24.",
        head_size=42)
    rule(d, 390, width=2)

    # ---- Grid: stories 2-5 ----
    cells = [
        (36, 408, pic_building_hit, "RUSSIA-UKRAINE  \u2022  STRIKES",
         ["Russian strikes hit", "Kyiv region homes"],
         "Drone and missile attacks damage a home in Dymer "
         "village; several people are reported missing."),
        (524, 408, pic_ship_fire, "BALTIC  \u2022  SEA WAR",
         ["Russian cargo ship", "ablaze off Finland"],
         "The military-linked Sparta II catches fire in the Gulf "
         "of Finland after a reported drone attack."),
        (36, 620, pic_chart_up, "MARKETS  \u2022  NVIDIA",
         ["Nvidia leaps 31% as", "Huang returns as CEO"],
         "Jensen Huang reinstated at the chip giant; the Nasdaq "
         "jumps 6.5% in an extraordinary Wall Street day."),
        (524, 620, pic_train, "INDIA-NEPAL  \u2022  RAIL",
         ["India and Nepal flag off", "cross-border express"],
         "PMs Modi and Balendra Shah launch the Saryu-Kamala "
         "Express, from Ayodhya to Janakpur Dham."),
    ]
    for (cx, cy, pic, kicker, heads, stand) in cells:
        pic(d, cx + 358, cy + 8, 102)
        headline_block(d, cx, cy, 330, kicker, heads, stand, head_size=24)
        if cx == 36:
            d.line([(500, cy), (500, cy + 186)], fill=GREY, width=1)
    rule(d, 604, width=1, fill=GREY)
    rule(d, 806, width=2)

    # ---- Story 6: Las Vegas Grand Prix ----
    pic_chequer(d, 872, 824, 100)
    headline_block(
        d, 36, 822, 820,
        "FORMULA ONE  \u2022  LAS VEGAS",
        ["Verstappen wins the",
         "Las Vegas Grand Prix"],
        "Max Verstappen takes the 2026 Las Vegas Grand Prix "
        "under the lights on the Strip circuit, another victory "
        "in the closing stretch of the Formula One season.",
        head_size=27)
    rule(d, 964, width=2)

    # ---- Footer: also today ----
    fnt = font(SANS, 16)
    footer = ("ALSO TODAY:  Alcaraz wins first ATP Finals title "
              "in Turin  \u2022  Gukesh opens chess world title defence "
              "in Geneva  \u2022  Sensex falls 1,484 points  \u2022  Lisbon "
              "marches over living costs  \u2022  Bangladesh vows to "
              "arrest Hasina if she returns.")
    y = 974
    for line in wrap(d, footer, fnt, 952):
        draw_centered(d, y, line, fnt, fill=(60, 60, 60))
        y += 20

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
