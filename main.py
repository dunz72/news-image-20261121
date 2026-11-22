#!/usr/bin/env python3
"""The World in One Day - Saturday 21 November 2026.

Draws a single 1024x1024 newspaper front page entirely in code with
Pillow: masthead, lead story, four feature stories, a world-in-brief
column and a sources footer. Every panel, chart, globe, skyline and
scale of justice is an original vector illustration.

No network access, no system fonts (Pillow's bundled default font
only), fully deterministic: two runs produce byte-identical PNGs.

Usage: python3 main.py
Output: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (96, 90, 80)
RED = (163, 22, 33)
NAVY = (15, 30, 51)
GOLD = (232, 163, 23)
ORANGE = (233, 116, 44)
CREAM_BAND = (238, 232, 216)
BLUE_BAND = (214, 231, 233)
GREEN = (46, 160, 90)
CANDLE_RED = (214, 69, 65)
MAGENTA = (214, 38, 140)


def font(size):
    """Pillow's bundled default font at the requested size.

    No system font files are touched: load_default() renders from a
    font embedded inside the Pillow package itself.
    """
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def text_block(draw, x, y, width, text, fnt, fill=INK, leading=None):
    """Draw wrapped text; returns the y coordinate below the block."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, weight=2):
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)


def double_rule(draw, x0, x1, y):
    rule(draw, x0, x1, y, 3)
    rule(draw, x0, x1, y + 6, 1)


# ---------------------------------------------------------------------------
# Illustrations (all drawn from fixed coordinates - no randomness)
# ---------------------------------------------------------------------------

def draw_night_sky(draw, x0, y0, x1, y1):
    """Kyiv under fire: night sky, moon, two missile bursts, skyline."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    span_x, span_y = x1 - x0, y1 - y0
    # Stars at fixed positions.
    stars = [
        (0.06, 0.12), (0.16, 0.30), (0.24, 0.10), (0.33, 0.22),
        (0.44, 0.08), (0.55, 0.26), (0.66, 0.12), (0.76, 0.30),
        (0.86, 0.10), (0.94, 0.24), (0.12, 0.44), (0.38, 0.40),
        (0.58, 0.42), (0.82, 0.44),
    ]
    for fx, fy in stars:
        sx, sy = x0 + fx * span_x, y0 + fy * span_y
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(235, 235, 220))
    # Moon.
    mx, my, mr = x0 + 0.86 * span_x, y0 + 0.20 * span_y, 17
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(238, 230, 196))
    draw.ellipse([mx - mr + 6, my - mr + 4, mx - mr + 13, my - mr + 11],
                 fill=(214, 204, 168))
    # Two explosion starbursts.
    for cx, cy, radius, colour in [
        (x0 + 0.38 * span_x, y0 + 0.34 * span_y, 26, GOLD),
        (x0 + 0.62 * span_x, y0 + 0.50 * span_y, 18, ORANGE),
    ]:
        for k in range(12):
            ang = math.radians(k * 30.0)
            dx = math.cos(ang) * radius
            dy = math.sin(ang) * radius
            draw.line([(cx + dx * 0.35, cy + dy * 0.35), (cx + dx, cy + dy)],
                      fill=colour, width=3)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)
    # Skyline silhouettes with a few lit windows.
    base = y1 - 26
    buildings = [
        (0.00, 0.52, 0.09), (0.10, 0.70, 0.08), (0.19, 0.58, 0.07),
        (0.27, 0.78, 0.09), (0.37, 0.62, 0.08), (0.46, 0.74, 0.07),
        (0.54, 0.56, 0.08), (0.63, 0.72, 0.09), (0.73, 0.60, 0.07),
        (0.81, 0.76, 0.08), (0.90, 0.64, 0.10),
    ]
    for fx, fh, fw in buildings:
        bx0 = x0 + fx * span_x
        bx1 = bx0 + fw * span_x
        by0 = base - fh * (y1 - y0 - 26) * 0.55
        draw.rectangle([bx0, by0, bx1, base], fill=(8, 14, 26))
        for wy in (by0 + 12, by0 + 30):
            if wy < base - 4:
                draw.rectangle([bx0 + 5, wy, bx0 + 9, wy + 4],
                               fill=(240, 200, 90))
    draw.rectangle([x0, base, x1, y1], fill=(8, 14, 26))
    # Caption strip.
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(10, 38, 66))
    draw.text((x0 + 10, y1 - 22), "KYIV UNDER FIRE - NIGHT OF 19-20 NOV",
              font=font(14), fill=(255, 255, 255))


def draw_scales(draw, x0, y0, x1, y1):
    """A balanced scale of justice on a cream band."""
    draw.rectangle([x0, y0, x1, y1], fill=CREAM_BAND)
    cx = (x0 + x1) // 2
    top = y0 + 6
    bottom = y1 - 8
    beam_y = top + 8
    # Pillar and base.
    draw.line([(cx, top + 6), (cx, bottom)], fill=NAVY, width=4)
    draw.line([(cx - 26, bottom), (cx + 26, bottom)], fill=NAVY, width=4)
    # Beam.
    draw.line([(cx - 78, beam_y), (cx + 78, beam_y)], fill=NAVY, width=4)
    # Finial.
    draw.ellipse([cx - 6, top - 6, cx + 6, top + 6], fill=RED)
    # Pans hanging from the beam ends.
    for side in (-1, 1):
        px = cx + side * 78
        draw.line([(px, beam_y), (px, beam_y + 18)], fill=NAVY, width=2)
        draw.line([(px - 26, beam_y + 18), (px, beam_y + 32)], fill=NAVY,
                  width=2)
        draw.line([(px + 26, beam_y + 18), (px, beam_y + 32)], fill=NAVY,
                  width=2)
        draw.arc([px - 26, beam_y + 22, px + 26, beam_y + 42],
                 start=0, end=180, fill=NAVY, width=3)


def draw_market_chart(draw, x0, y0, x1, y1):
    """Falling candlesticks with a descending trend line."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.text((x0 + 10, y0 + 8), "S&P 500  -3.7%", font=font(17),
              fill=(255, 255, 255))
    candles = [
        (0.06, 0.16, 0.32), (0.16, 0.28, 0.14), (0.26, 0.36, 0.24),
        (0.36, 0.30, 0.46), (0.46, 0.44, 0.32), (0.56, 0.50, 0.38),
        (0.66, 0.44, 0.58), (0.76, 0.58, 0.46), (0.86, 0.54, 0.68),
    ]
    span_x = x1 - x0
    top = y0 + 28
    bottom = y1 - 6
    pts = []
    for fx, fo, fc in candles:
        cx = x0 + fx * span_x
        yo = top + fo * (bottom - top)
        yc = top + fc * (bottom - top)
        colour = GREEN if fc < fo else CANDLE_RED
        draw.line([(cx, top + (fo - 0.06) * (bottom - top)),
                   (cx, top + (fc + 0.06) * (bottom - top))],
                  fill=(200, 200, 200), width=1)
        draw.rectangle([cx - 9, min(yo, yc), cx + 9, max(yo, yc)],
                       fill=colour)
        pts.append((cx, (yo + yc) / 2))
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        draw.line([(ax, ay), (bx, by)], fill=GOLD, width=2)


def draw_globe(img, draw, x0, y0, x1, y1):
    """A wireframe globe and a small sun on a pale blue band."""
    draw.rectangle([x0, y0, x1, y1], fill=BLUE_BAND)
    draw.text((x0 + 10, y0 + 8), "1.5°C LIMIT SET TO BE OVERSHOT",
              font=font(13), fill=NAVY)
    # Sun, top right.
    sx, sy, sr = x1 - 34, y0 + 26, 11
    for k in range(8):
        ang = math.radians(k * 45.0)
        dx, dy = math.cos(ang), math.sin(ang)
        draw.line([(sx + dx * (sr + 3), sy + dy * (sr + 3)),
                   (sx + dx * (sr + 9), sy + dy * (sr + 9))],
                  fill=GOLD, width=2)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD)
    # Globe: draw meridians/parallels on a layer, then mask to a disc.
    cx, cy, r = (x0 + x1) // 2 + 10, (y0 + y1) // 2 + 2, 30
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gl = ImageDraw.Draw(layer)
    gl.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    for dy in (-r // 2, 0, r // 2):
        half = int(math.sqrt(max(r * r - dy * dy, 0)))
        gl.line([(cx - half, cy + dy), (cx + half, cy + dy)],
                fill=NAVY, width=2)
    for rx in (r // 2, r // 4):
        gl.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=NAVY,
                   width=2)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.paste(layer, (0, 0), mask)
    merged = Image.alpha_composite(img.convert("RGBA"), base).convert("RGB")
    img.paste(merged, (0, 0))


def draw_gta_skyline(draw, x0, y0, x1, y1):
    """Sunset skyline: orange bands, dark towers, lit windows."""
    bands = [
        (244, 178, 84), (240, 158, 62), (236, 138, 52),
        (232, 120, 46), (228, 104, 44), (224, 92, 46),
    ]
    span_y = y1 - y0
    for i, colour in enumerate(bands):
        by0 = y0 + i * span_y // len(bands)
        by1 = y0 + (i + 1) * span_y // len(bands)
        draw.rectangle([x0, by0, x1, by1], fill=colour)
    # Low sun.
    sx, sy, sr = x0 + 0.78 * (x1 - x0), y0 + 0.42 * span_y, 24
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                 fill=(250, 226, 160))
    # Towers with deterministic lit windows.
    span_x = x1 - x0
    towers = [
        (0.00, 0.46, 0.10), (0.11, 0.66, 0.09), (0.21, 0.52, 0.08),
        (0.30, 0.74, 0.10), (0.41, 0.58, 0.08), (0.50, 0.70, 0.09),
        (0.60, 0.50, 0.08), (0.69, 0.68, 0.09), (0.79, 0.56, 0.08),
        (0.88, 0.72, 0.12),
    ]
    base = y1
    for fx, fh, fw in towers:
        tx0 = x0 + fx * span_x
        tx1 = tx0 + fw * span_x
        ty0 = base - fh * span_y * 0.72
        draw.rectangle([tx0, ty0, tx1, base], fill=(24, 20, 38))
        row = 0
        wy = ty0 + 10
        while wy < base - 8:
            for col in range(3):
                wx = tx0 + 6 + col * 12
                if (row * 3 + col) % 3 != 0 and wx + 5 < tx1 - 4:
                    draw.rectangle([wx, wy, wx + 5, wy + 6],
                                   fill=(250, 214, 110))
            wy += 16
            row += 1
    # Label.
    draw.rectangle([x0 + 10, y0 + 10, x0 + 96, y0 + 36], fill=MAGENTA)
    draw.text((x0 + 18, y0 + 14), "GTA VI", font=font(17),
              fill=(255, 255, 255))


# ---------------------------------------------------------------------------
# Page composition
# ---------------------------------------------------------------------------

def build_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    right = W - mx

    # ---- Masthead ------------------------------------------------------
    double_rule(d, mx, right, 20)
    d.text((W // 2, 32), "THE WORLD IN ONE DAY", font=font(62),
           fill=INK, anchor="ma")
    d.text((W // 2, 100),
           "SATURDAY 21 NOVEMBER 2026  |  ONE PAGE  |  THE STORIES THAT "
           "SHAPED THE DAY",
           font=font(16), fill=MUTED, anchor="ma")
    double_rule(d, mx, right, 120)

    # ---- Lead story ----------------------------------------------------
    lead_y = 138
    lead_w = 556
    d.text((mx, lead_y), "WAR IN EUROPE  |  KYIV  |  WARSAW",
           font=font(16), fill=RED)
    y = text_block(d, mx, lead_y + 22, lead_w,
                   "Russia's biggest November barrage hits Kyiv - and "
                   "spills into Poland",
                   font(29), leading=34)
    y = text_block(d, mx, y + 6, lead_w,
                   "Russia fired 404 drones and 111 missiles at Ukraine "
                   "overnight on 19-20 November - its largest strike "
                   "package of the month. At least eight people were "
                   "killed in Kyiv, three bridges over the Dnipro were "
                   "damaged and power was cut in ten regions.",
                   font(16), leading=20)
    text_block(d, mx, y + 6, lead_w,
               "Two missiles and a jet-powered drone came down in eastern "
               "Poland. No one was hurt, but Warsaw called it an "
               "\"intentional provocation\" and NATO condemned a grave "
               "violation of allied airspace.",
               font(16), leading=20)
    draw_night_sky(d, 620, lead_y, right, lead_y + 196)

    # ---- Feature rows --------------------------------------------------
    rule(d, mx, right, 392, 2)
    col_w = 452
    lx, rx = mx, 536

    # Row 1: Justice | Markets
    fy = 404
    d.text((lx, fy), "JUSTICE  |  THE HAGUE", font=font(16), fill=RED)
    draw_scales(d, lx, fy + 22, lx + col_w, fy + 86)
    y = text_block(d, lx, fy + 94, col_w,
                   "World Court: Myanmar guilty of genocide against the "
                   "Rohingya", font(23), leading=26)
    text_block(d, lx, y + 6, col_w,
               "In a landmark 9-6 judgment on 19 November, the "
               "International Court of Justice held Myanmar responsible "
               "for genocide - the first time a state has been found "
               "guilty of it. It ordered reparations and a safe, "
               "voluntary return for the Rohingya.",
               font(15), leading=19)

    d.text((rx, fy), "MARKETS  |  NEW YORK  |  TOKYO", font=font(16),
           fill=RED)
    draw_market_chart(d, rx, fy + 22, rx + col_w, fy + 86)
    y = text_block(d, rx, fy + 94, col_w,
                   "AI sell-off sinks Wall Street; Nasdaq negative for "
                   "the year", font(23), leading=26)
    text_block(d, rx, y + 6, col_w,
               "The S&P 500 fell 3.7% and the Nasdaq closed negative for "
               "2026 as investors questioned sky-high AI valuations. "
               "Japan's Nikkei slid 5.1%. Anthropic fell 9.1% a day after "
               "its Wall Street debut.",
               font(15), leading=19)

    rule(d, mx, right, 644, 2)

    # Row 2: Climate | Culture
    fy = 656
    d.text((lx, fy), "CLIMATE  |  ANTALYA", font=font(16), fill=RED)
    draw_globe(img, d, lx, fy + 22, lx + col_w, fy + 86)
    y = text_block(d, lx, fy + 94, col_w,
                   "COP31 passes deadline as fossil-fuel language drops",
                   font(23), leading=26)
    text_block(d, lx, y + 6, col_w,
               "UN climate talks in Antalya passed their Friday deadline "
               "with no deal. A new draft removed promises to move away "
               "from coal, oil and gas - while admitting for the first "
               "time that the 1.5°C limit will be overshot.",
               font(15), leading=19)

    d.text((rx, fy), "CULTURE  |  LOS SANTOS", font=font(16), fill=RED)
    draw_gta_skyline(d, rx, fy + 22, rx + col_w, fy + 86)
    y = text_block(d, rx, fy + 94, col_w,
                   "GTA VI: $3.8bn in a day, the biggest launch ever",
                   font(23), leading=26)
    text_block(d, rx, y + 6, col_w,
               "Grand Theft Auto VI sold about 32.5 million copies on its "
               "first day, Take-Two estimates - roughly $3.8 billion in "
               "24 hours. No film, album or game has ever opened bigger.",
               font(15), leading=19)

    rule(d, mx, right, 898, 2)

    # ---- The day in brief ----------------------------------------------
    by = 908
    d.text((mx, by), "THE DAY IN BRIEF", font=font(15), fill=RED)
    briefs = [
        ("SHENZHEN",
         "Xi hosted Trump and Putin for a trilateral summit in Shenzhen."),
        ("WASHINGTON",
         "Trump weighs new Iran strikes; FBI probes breach of crime "
         "database."),
        ("BRUSSELS",
         "UK-EU signed three post-Brexit deals on mobility, trade, "
         "energy."),
        ("SCIENCE",
         "Daily pill shrank pancreatic tumours; BepiColombo reached "
         "Mercury."),
    ]
    for i, (place, text) in enumerate(briefs):
        col = i % 2
        row = i // 2
        x = lx if col == 0 else rx
        yy = by + 20 + row * 34
        d.text((x, yy), "> " + place, font=font(13), fill=RED)
        text_block(d, x, yy + 15, col_w, text, font(12), leading=15)

    # ---- Footer --------------------------------------------------------
    rule(d, mx, right, 998, 1)
    d.text((mx, 1004),
           "Sources: BBC News, Associated Press, The New York Times, "
           "Reuters, UN News, Institute for the Study of War, Human "
           "Rights Watch",
           font=font(11), fill=MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img = build_page()
    img.save(out_path, format="PNG")
    with open(out_path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"wrote {out_path}  {img.size[0]}x{img.size[1]}  sha256={digest}")


if __name__ == "__main__":
    main()
