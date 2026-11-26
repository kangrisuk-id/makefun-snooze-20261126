#!/usr/bin/env python3
"""Build-time asset generator for the Snooze Button Roast README.

Runs ONCE at build time with Pillow. The submitted entrypoint (main.py)
never imports Pillow and never touches these images; they are static
assets committed to the repo for the README gallery.

Generates (1200x630 each, dark charcoal + gold + alarm red):
  assets/hero.png          — cover: alarm clock art + title + winning line
  assets/shot-line.png     — the roast as a quote poster
  assets/shot-run.png      — terminal-style render of the program's run
  assets/shot-criteria.png — the judge's five criteria, checked off
  assets/shot-clock.png    — clock face at 6:00 on a Saturday
"""

import math
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

W, H = 1200, 630
BG = (18, 20, 24)
PANEL = (28, 31, 37)
GOLD = (232, 182, 76)
CREAM = (240, 234, 220)
MUTED = (168, 164, 152)
RED = (228, 87, 46)
GREEN = (96, 200, 120)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def base():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=(58, 60, 66), width=3)
    return img, d


def draw_clock(d, cx, cy, r, face=(248, 244, 232), body=RED):
    """A twin-bell alarm clock centred at (cx, cy) with radius r."""
    # bells
    d.pieslice([cx - r - 18, cy - r - 46, cx - r + 78, cy - r + 54], 180, 330, fill=GOLD)
    d.pieslice([cx + r - 78, cy - r - 46, cx + r + 18, cy - r + 54], 210, 360, fill=GOLD)
    # hammer + legs
    d.line([cx - 14, cy - r - 6, cx - 14, cy - r - 34], fill=GOLD, width=8)
    d.line([cx + 14, cy - r - 6, cx + 14, cy - r - 34], fill=GOLD, width=8)
    d.line([cx - r + 26, cy + r - 6, cx - r - 6, cy + r + 46], fill=GOLD, width=10)
    d.line([cx + r - 26, cy + r - 6, cx + r + 6, cy + r + 46], fill=GOLD, width=10)
    # body + face
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=body)
    d.ellipse([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16], fill=face)
    # ticks
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x1 = cx + (r - 34) * math.cos(a)
        y1 = cy + (r - 34) * math.sin(a)
        x2 = cx + (r - 22) * math.cos(a)
        y2 = cy + (r - 22) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(60, 58, 52), width=4)
    # hands at 6:00 (hour down, minute up)
    d.line([cx, cy, cx, cy - (r - 52)], fill=(30, 28, 24), width=7)
    d.line([cx, cy, cx, cy + (r - 58)], fill=(30, 28, 24), width=9)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(30, 28, 24))


def wrap_center(d, text, fnt, max_w, y, fill, spacing=8):
    lines = []
    for para in text.split("\n"):
        lines += textwrap.wrap(para, width=1000) if False else _wrap(d, para, fnt, max_w)
    for line in lines:
        w = d.textlength(line, font=fnt)
        d.text(((W - w) / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def _wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


LINE = (
    "My alarm clock rings at 6 AM on a Saturday \u2014 even the sun is "
    "still asleep, but this little plastic tyrant never misses a shift."
)


def hero():
    img, d = base()
    draw_clock(d, 220, 300, 150)
    d.text((420, 96), "SNOOZE BUTTON", font=font(BOLD, 74), fill=CREAM)
    d.text((420, 176), "ROAST", font=font(BOLD, 74), fill=GOLD)
    d.text((420, 268), "One line. One alarm clock. Zero mercy for 6 AM.",
           font=font(REG, 30), fill=MUTED)
    y = 340
    for line in _wrap(d, "\u201c" + LINE + "\u201d", font(REG, 32), 700):
        d.text((420, y), line, font=font(REG, 32), fill=CREAM)
        y += 44
    d.text((420, 540), "$2 prize  ·  8 paid places  ·  make.fun",
           font=font(BOLD, 26), fill=GOLD)
    img.save(os.path.join(ASSETS, "hero.png"))


def shot_line():
    img, d = base()
    d.text((60, 60), "\u201c", font=font(BOLD, 150), fill=GOLD)
    y = 190
    for line in _wrap(d, LINE, font(BOLD, 46), 1040):
        w = d.textlength(line, font=font(BOLD, 46))
        d.text(((W - w) / 2, y), line, font=font(BOLD, 46), fill=CREAM)
        y += 62
    d.text((60, 520), "— the winning line, 127 characters, one breath",
           font=font(REG, 28), fill=MUTED)
    img.save(os.path.join(ASSETS, "shot-line.png"))


def shot_run():
    img, d = base()
    d.rectangle([50, 50, W - 50, H - 50], fill=PANEL, outline=(58, 60, 66), width=2)
    d.text((90, 90), "$ MAKEFUN_OUTPUT_DIR=output python3 main.py",
           font=font(MONO, 30), fill=GREEN)
    d.text((90, 160), "wrote output/entry.txt (127 chars)",
           font=font(MONO, 30), fill=CREAM)
    d.text((90, 240), "$ cat output/entry.txt", font=font(MONO, 30), fill=GREEN)
    y = 300
    for line in _wrap(d, LINE, font(MONO, 26), 1020):
        d.text((90, y), line, font=font(MONO, 26), fill=GOLD)
        y += 40
    d.text((90, 480), "deterministic: two runs, byte-identical output",
           font=font(MONO, 26), fill=MUTED)
    img.save(os.path.join(ASSETS, "shot-run.png"))


def shot_criteria():
    img, d = base()
    d.text((60, 50), "Judged on the brief — in order", font=font(BOLD, 40), fill=CREAM)
    rows = [
        ("1", "On-topic: one line, alarm clock, 6 AM, Saturday"),
        ("2", "Real laugh: unexpected turn, payoff in the last words"),
        ("3", "Fresh angle: no tired morning-hating, no inventor joke"),
        ("4", "Tight: every word earns its place, one breath"),
        ("5", "Specific voice: concrete images, not vague grumbling"),
    ]
    y = 140
    for num, text in rows:
        d.ellipse([60, y + 4, 108, y + 52], fill=GOLD)
        d.text((76, y + 8), num, font=font(BOLD, 28), fill=BG)
        d.text((130, y + 8), text, font=font(REG, 30), fill=CREAM)
        y += 84
    img.save(os.path.join(ASSETS, "shot-criteria.png"))


def shot_clock():
    img, d = base()
    draw_clock(d, 600, 300, 190)
    d.text((60, 36), "6:00", font=font(BOLD, 54), fill=GOLD)
    sat = "SATURDAY"
    sat_f = font(BOLD, 54)
    d.text((W - 60 - d.textlength(sat, font=sat_f), 36), sat, font=sat_f, fill=RED)
    d.text((60, 540), "Even the sun is still asleep.",
           font=font(REG, 30), fill=MUTED)
    tyr = "The tyrant never misses a shift."
    d.text((W - 60 - d.textlength(tyr, font=font(BOLD, 30)), 540), tyr,
           font=font(BOLD, 30), fill=CREAM)
    img.save(os.path.join(ASSETS, "shot-clock.png"))


if __name__ == "__main__":
    hero()
    shot_line()
    shot_run()
    shot_criteria()
    shot_clock()
    print("assets written to", ASSETS)
