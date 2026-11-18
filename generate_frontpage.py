#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Tuesday 17 November 2026.

One image, 1024x1024 PNG, summing up the day's world news. Pure Pillow,
no network, no timestamps, no randomness: the same run always writes the
same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (28, 68, 120)
GREY = (110, 108, 100)
LIGHT = (232, 226, 212)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y below the last line."""
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, fill=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def draw_bridge(draw, x, y, w, h):
    """Kerch-style bridge with a collapsed middle span over water."""
    water_y = y + h - 26
    draw.rectangle([x, water_y, x + w, y + h], fill=(58, 110, 158))
    for i in range(5):
        wx = x + 12 + i * (w - 24) // 5
        draw.arc([wx, water_y + 4, wx + 34, water_y + 18], 0, 180, fill=(210, 225, 240), width=2)
    deck_y = y + h - 78
    # left and right spans, middle collapsed
    draw.rectangle([x, deck_y, x + w * 0.38, deck_y + 12], fill=(90, 88, 84))
    draw.rectangle([x + w * 0.62, deck_y, x + w, deck_y + 12], fill=(90, 88, 84))
    # fallen middle span, tilted into the water
    draw.polygon([(x + w * 0.40, deck_y + 4), (x + w * 0.60, deck_y + 4),
                  (x + w * 0.58, water_y - 4), (x + w * 0.48, water_y - 4)],
                 fill=(100, 98, 94))
    # towers
    for tx in (x + w * 0.18, x + w * 0.80):
        draw.rectangle([tx, deck_y - 62, tx + 10, deck_y], fill=(90, 88, 84))
    # cables
    draw.line([(x + w * 0.18 + 5, deck_y - 62), (x + w * 0.38, deck_y)], fill=(120, 118, 112), width=2)
    draw.line([(x + w * 0.80 + 5, deck_y - 62), (x + w * 0.62, deck_y)], fill=(120, 118, 112), width=2)
    # explosion bursts at the gap
    cx, cy = x + w // 2, deck_y - 6
    for r, col in ((34, (240, 140, 40)), (22, (250, 200, 60)), (12, (255, 240, 180))):
        pts = []
        for k in range(12):
            import math
            ang = k * math.pi / 6
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=col)
    # smoke
    for sx, sy, sr in ((cx - 30, cy - 34, 14), (cx + 26, cy - 40, 17), (cx + 2, cy - 52, 12)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 148, 142))


def draw_tanker(draw, x, y, w, h):
    """Oil tanker with a fire on deck, on the sea."""
    sea_y = y + h - 24
    draw.rectangle([x, sea_y, x + w, y + h], fill=(58, 110, 158))
    draw.rectangle([x + 8, sea_y - 26, x + w - 8, sea_y - 6], fill=(40, 40, 44))
    draw.rectangle([x + 8, sea_y - 44, x + w * 0.30, sea_y - 26], fill=(163, 18, 18))
    draw.rectangle([x + w * 0.34, sea_y - 44, x + w * 0.56, sea_y - 26], fill=(28, 68, 120))
    # bridge tower
    draw.rectangle([x + w - 26, sea_y - 58, x + w - 10, sea_y - 26], fill=(230, 228, 220))
    # flame
    fx = x + w * 0.45
    draw.polygon([(fx - 16, sea_y - 44), (fx, sea_y - 74), (fx + 16, sea_y - 44)],
                 fill=(240, 140, 40))
    draw.polygon([(fx - 8, sea_y - 44), (fx, sea_y - 62), (fx + 8, sea_y - 44)],
                 fill=(250, 210, 80))
    # smoke
    draw.ellipse([fx - 22, sea_y - 92, fx + 2, sea_y - 68], fill=(150, 148, 142))
    draw.ellipse([fx - 6, sea_y - 100, fx + 18, sea_y - 76], fill=(170, 168, 160))


def draw_summit(draw, x, y, w, h):
    """Three flags over a table: China, USA, Russia."""
    # table
    draw.ellipse([x + 8, y + h - 34, x + w - 8, y + h - 8], fill=(120, 84, 48))
    draw.rectangle([x + w // 2 - 4, y + h - 34, x + w // 2 + 4, y + h - 6], fill=(90, 62, 34))
    flags = [
        (x + 6, (200, 30, 30)),    # China red
        (x + w // 2 - 16, (28, 68, 120)),  # USA blue
        (x + w - 38, (220, 220, 220)),     # Russia white
    ]
    for fx, col in flags:
        draw.line([(fx + 16, y + 8), (fx + 16, y + h - 34)], fill=(90, 88, 84), width=3)
        draw.rectangle([fx + 16, y + 8, fx + 46, y + 34], fill=col, outline=INK, width=1)
    # stripes on the US flag
    for i in range(3):
        draw.line([(x + w // 2, y + 14 + i * 8), (x + w // 2 + 30, y + 14 + i * 8)],
                  fill=(240, 240, 240), width=3)
    # blue stripe on the Russia flag
    draw.rectangle([x + w - 22, y + 17, x + w + 8, y + 25], fill=(28, 68, 120))


def draw_chip(draw, x, y, w, h):
    """AI chip: dark square, gold pins, glowing core."""
    cx, cy = x + w // 2, y + h // 2
    s = 58
    # pins
    for i in range(4):
        off = -21 + i * 14
        draw.line([(cx + off, y + 8), (cx + off, y + h - 8)], fill=(200, 160, 60), width=4)
        draw.line([(x + 8, cy + off), (x + w - 8, cy + off)], fill=(200, 160, 60), width=4)
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=(30, 30, 36), outline=(200, 160, 60), width=3)
    draw.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(28, 68, 120))
    draw.text((cx, cy), "AI", font=font(SANS_B, 18), fill=(255, 255, 255), anchor="mm")


def draw_audit(draw, x, y, w, h):
    """Ledger page stamped with a red X: the failed audit."""
    draw.rectangle([x + 14, y + 6, x + w - 14, y + h - 6], fill=(255, 255, 255),
                   outline=INK, width=2)
    for i in range(4):
        ly = y + 22 + i * 16
        draw.line([(x + 26, ly), (x + w - 26, ly)], fill=(150, 148, 142), width=2)
    cx, cy = x + w // 2, y + h // 2 + 6
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=RED, width=5)
    draw.line([(cx - 14, cy - 14), (cx + 14, cy + 14)], fill=RED, width=5)
    draw.line([(cx - 14, cy + 14), (cx + 14, cy - 14)], fill=RED, width=5)


def draw_gavel(draw, x, y, w, h):
    """Gavel over a block: sanctions."""
    draw.rectangle([x + 12, y + h - 26, x + w - 12, y + h - 8], fill=(120, 84, 48))
    draw.line([(x + 30, y + h - 28), (x + w - 34, y + 22)], fill=(90, 62, 34), width=7)
    draw.rectangle([x + w - 52, y + 8, x + w - 8, y + 40], fill=(60, 44, 30))
    draw.rectangle([x + w - 58, y + 14, x + w - 46, y + 34], fill=(90, 62, 34))


def story_block(draw, x, y, w, h, kicker, headline, body, icon=None):
    """One story cell: kicker, headline, body text, optional icon at left."""
    pad = 14
    tx = x + pad
    tw = w - 2 * pad
    if icon is not None:
        icon(draw, x + pad, y + 34, 104, 104)
        tx = x + pad + 118
        tw = w - pad - 118 - pad
    draw.text((tx, y + 6), kicker, font=font(SANS_B, 15), fill=RED)
    y2 = para(draw, tx, y + 28, headline, font(SERIF_B, 23), tw, leading=27)
    para(draw, tx, y2 + 4, body, font(SANS, 16), tw, leading=21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((W // 2, 52), "THE WORLD TODAY", font=font(SERIF_B, 66), fill=INK, anchor="mm")
    rule(d, 28, 96, W - 56, width=3)
    d.text((28, 108), "TUESDAY, 17 NOVEMBER 2026", font=font(SANS_B, 19), fill=INK)
    d.text((W - 28, 108), "ONE DAY  ·  SIX STORIES", font=font(SANS_B, 19), fill=RED, anchor="ra")
    rule(d, 28, 138, W - 56, width=1)

    # ---- Lead story: the bridge war ----
    lx, ly, lw = 28, 152, W - 56
    d.text((lx, ly), "UKRAINE WAR  —  LEAD STORY", font=font(SANS_B, 17), fill=RED)
    hy = para(d, lx, ly + 28, "BRIDGES BECOME THE BATTLEFIELD",
              font(SERIF_B, 44), lw, leading=50)
    # text left, bridge illustration right
    ty = hy + 10
    tw = 560
    ty = para(d, lx, ty,
              "Ukraine struck the Kerch Bridge to occupied Crimea for a second day "
              "running, collapsing a section of the road link. President Zelenskyy "
              "hailed an \u201cunprecedented operation\u201d.",
              font(SANS, 20), tw, leading=26)
    para(d, lx, ty + 8,
         "Hours earlier, Russian missiles hit Kyiv\u2019s two bridges over the "
         "Dnipro, cutting heating, water and power in the capital.",
         font(SANS, 20), tw, leading=26)
    draw_bridge(d, lx + 584, hy + 4, 384, 150)
    rule(d, 28, 462, W - 56, width=2)

    # ---- Middle grid: 2 x 2 ----
    gy = 476
    gh = 188
    gw = (W - 56 - 16) // 2
    story_block(d, 28, gy, gw, gh, "MIDDLE EAST  ·  GULF",
                "Iran hits US radar; tankers burn at Hormuz",
                "Drones fired at a US radar base in Bahrain \u2014 intercepted, no "
                "casualties. Mines hit tankers near Hormuz as a third US carrier "
                "arrived. US intelligence reports an Iranian \u201cdirty bomb\u201d plot.",
                icon=draw_tanker)
    story_block(d, 28 + gw + 16, gy, gw, gh, "DIPLOMACY  ·  ASIA",
                "Xi, Trump and Putin to meet in Shenzhen",
                "China confirmed the first three-way summit of the three leaders, "
                "set for Thursday on the sidelines of APEC. Trump is travelling to "
                "Asia as the war in Ukraine and Gulf tensions deepen.",
                icon=draw_summit)
    story_block(d, 28, gy + gh + 12, gw, gh, "BUSINESS  ·  TECH",
                "Nvidia beats forecasts amid CEO turmoil",
                "Revenue $115.8bn, up 103% on a year ago, in its first results since "
                "Jensen Huang resigned. The board will not reinstate him; the SEC is "
                "reportedly investigating. Shares rose after hours.",
                icon=draw_chip)
    story_block(d, 28 + gw + 16, gy + gh + 12, gw, gh, "WASHINGTON",
                "Pentagon fails its audit for a ninth year",
                "Auditors again refused to sign off the Pentagon\u2019s books, unable "
                "to verify accounts covering more than $4.8 trillion in assets.",
                icon=draw_audit)
    rule(d, 28, 876, W - 56, width=2)

    # ---- Bottom row: sanctions + also-on-Tuesday ----
    by = 890
    story_block(d, 28, by, 600, 84, "WEST BANK",
                "UK sanctions Israeli settlement firms",
                "Britain blacklisted eight construction firms building settlements and "
                "a group blocking Gaza aid, as election-day arrests roil Israel.",
                icon=None)
    bx = 28 + 600 + 16
    bw = W - 28 - bx
    d.rectangle([bx, by - 4, bx + bw, by + 96], outline=INK, width=2)
    d.text((bx + 12, by + 4), "ALSO ON TUESDAY", font=font(SANS_B, 15), fill=RED)
    para(d, bx + 12, by + 26,
         "EU sanctions 12 people, 101 entities over Russia  ·  Japan scrambles jets "
         "as Russian planes enter its airspace  ·  US moves to close the AI-chip "
         "loophole  ·  COP31 opens in Antalya",
         font(SANS, 13), bw - 24, leading=17)

    # ---- Footer ----
    rule(d, 28, 1002, W - 56, width=1)
    d.text((W // 2, 1008), "THE WORLD TODAY  ·  TUESDAY 17 NOVEMBER 2026",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
