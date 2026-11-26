"""Front page for Thursday 26 November 2026, drawn with Pillow.

Layout, top to bottom: a navy masthead with the paper name and the
date, a dateline, five numbered stories (colour badge, kicker, headline,
two-line standfirst), an ALSO TODAY box, and a footer line. Run this file
locally to regenerate entry.png; the submitted program (main.py) only
copies the finished PNG to the output directory.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 40
RIGHT = PAGE_W - MARGIN

PAPER = (255, 255, 255)
NAVY = (15, 42, 68)
RED = (178, 34, 34)
INK = (20, 20, 20)
MUTED = (90, 90, 90)
BODY = (60, 60, 60)
RULE = (210, 210, 210)
PANEL = (240, 244, 248)
GOLD = (255, 210, 80)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load(bold, size):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def wrap_text(draw, text, fnt, width):
    """Split text into lines that fit width, word by word."""
    words = text.split()
    lines = []
    line = ""
    for word in words:
        nxt = f"{line} {word}".strip()
        if draw.textlength(nxt, font=fnt) <= width:
            line = nxt
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


STORIES = [
    dict(
        color=(178, 34, 34),
        kicker="UNITED STATES  /  TRADE",
        headline="US proposes new tariffs; China hit hardest",
        stand="Washington moves against what it calls structural excess industrial "
              "capacity; India faces a 17% rate and Brazil 10% on aircraft.",
    ),
    dict(
        color=(15, 42, 68),
        kicker="UNITED STATES",
        headline="Macy\u2019s parade postponed for first time by storm",
        stand="The 100th parade moves to Saturday as a nor\u2019easter brings high "
              "winds and heavy rain to New York City.",
    ),
    dict(
        color=(0, 110, 80),
        kicker="NORTH KOREA",
        headline="Kim orders wider rollout of tactical nuclear weapons",
        stand="Kim Jong Un inspects warheads in a rare public display and "
              "dismisses Trump\u2019s offer to resume talks.",
    ),
    dict(
        color=(150, 90, 0),
        kicker="EGYPT",
        headline="Fuel tanker fire on Cairo ring road kills at least 30",
        stand="A tanker overturns and catches fire in Giza; at least 30 dead and "
              "15 injured, the Health Ministry says.",
    ),
    dict(
        color=(70, 70, 160),
        kicker="SPACE  /  PAKISTAN",
        headline="Pakistan\u2019s first astronaut boards Tiangong",
        stand="The first Pakistani in orbit becomes the first foreign astronaut "
              "to visit the Tiangong space station.",
    ),
]

ALSO = [
    "Australia and Solomon Islands sign a security pact; no foreign bases allowed.",
    "Duran Duran guitarist Andy Taylor dies at 65.",
    "Russia\u2019s Murmansk governor detained in a corruption probe; Putin fires him.",
]


def masthead(draw):
    draw.rectangle([MARGIN, 28, RIGHT, 112], fill=NAVY)
    draw.text((MARGIN + 20, 44), "WORLD NEWS", font=load(True, 52), fill=PAPER)
    draw.text((RIGHT - 20, 62), "26 NOV 2026", font=load(True, 30), fill=GOLD, anchor="ra")
    draw.text((MARGIN, 128), "THURSDAY  26  NOVEMBER  2026", font=load(True, 30), fill=NAVY)
    draw.text((MARGIN, 168), "The day in five stories \u2014 from Washington to Tiangong",
              font=load(False, 22), fill=MUTED)
    draw.line([MARGIN, 200, RIGHT, 200], fill=RED, width=4)


def story(draw, index, item, y):
    """Draw one numbered story; return the y where the next block starts."""
    color = item["color"]
    draw.rounded_rectangle([MARGIN, y, MARGIN + 54, y + 54], radius=10, fill=color)
    draw.text((MARGIN + 27, y + 26), str(index), font=load(True, 30), fill=PAPER, anchor="mm")
    tx = MARGIN + 74
    width = RIGHT - tx
    draw.text((tx, y + 2), item["kicker"], font=load(True, 17), fill=color)
    head = wrap_text(draw, item["headline"], load(True, 27), width)
    hy = y + 24
    for ln in head:
        draw.text((tx, hy), ln, font=load(True, 27), fill=INK)
        hy += 32
    stand = wrap_text(draw, item["stand"], load(False, 20), width)
    by = hy + 4
    for ln in stand:
        draw.text((tx, by), ln, font=load(False, 20), fill=BODY)
        by += 25
    return by + 12


def also_today(draw, y):
    draw.rounded_rectangle([MARGIN, y + 2, RIGHT, y + 104], radius=10, fill=PANEL)
    draw.text((MARGIN + 16, y + 12), "ALSO TODAY", font=load(True, 18), fill=NAVY)
    ay = y + 38
    for item in ALSO:
        draw.text((MARGIN + 16, ay), "\u2022  " + item, font=load(False, 18), fill=(50, 50, 50))
        ay += 24


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    y = 222
    for i, item in enumerate(STORIES, start=1):
        y = story(draw, i, item, y)
        if i < len(STORIES):
            # Divider sits 10px below the standfirst (story() adds 12, we go back 2).
            draw.line([MARGIN, y - 2, RIGHT, y - 2], fill=RULE, width=2)
    also_today(draw, y)
    draw.line([MARGIN, 968, RIGHT, 968], fill=RULE, width=2)
    draw.text((MARGIN, 978), "Headlines as reported on 26 November 2026",
              font=load(False, 18), fill=MUTED)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
